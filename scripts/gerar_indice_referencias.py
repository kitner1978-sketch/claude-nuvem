#!/usr/bin/env python3
"""
gerar_indice_referencias.py — Gera Índice Remissivo e lista de Referências

1. Índice Remissivo: extrai termos jurídicos-chave (legislação, institutos,
   súmulas, temas) de cada capítulo e mapeia para capítulos onde aparecem.

2. Referências: extrai citações autorais (SOBRENOME, ano) de cada capítulo
   e compila lista única para servir de base à bibliografia.

Saídas:
  - output/indice_remissivo.txt  — para uso no livro
  - output/referencias_extraidas.txt — para os autores completarem
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict


# ═══════════════════════════════════════════════════════
# ÍNDICE REMISSIVO
# ═══════════════════════════════════════════════════════

# Legislação federal com número/ano
LEGISLACAO_PATTERNS = [
    (r'Lei\s+(?:n[.ºo°]\s*)?(\d[\d.]+/\d{2,4})', 'Lei'),
    (r'Lei\s+Complementar\s+(?:n[.ºo°]\s*)?(\d+/\d{2,4})', 'LC'),
    (r'Decreto\s+(?:n[.ºo°]\s*)?(\d[\d.]+/\d{2,4})', 'Decreto'),
    (r'Decreto-Lei\s+(?:n[.ºo°]\s*)?(\d[\d.]+/\d{2,4})', 'Decreto-Lei'),
    (r'Instrução\s+Normativa\s+(?:INSS\s+)?(?:n[.ºo°]\s*)?(\d+/\d{2,4})', 'IN'),
    (r'Emenda\s+Constitucional\s+(?:n[.ºo°]\s*)?(\d+/?\d*)', 'EC'),
    (r'Medida\s+Provisória\s+(?:n[.ºo°]\s*)?(\d[\d.]+/?\d*)', 'MP'),
    (r'Portaria\s+(?:n[.ºo°]\s*)?(\d[\d.]+/\d{2,4})', 'Portaria'),
]

# Súmulas e enunciados
SUMULA_PATTERNS = [
    (r'Súmula\s+(?:Vinculante\s+)?(?:n[.ºo°]\s*)?(\d+)\s+do\s+(STF|STJ|TNU|TRF)', 'Súmula'),
    (r'Súmula\s+(?:n[.ºo°]\s*)?(\d+)\s+do\s+(STF|STJ|TNU|TRF)', 'Súmula'),
    (r'Súmula\s+Vinculante\s+(?:n[.ºo°]\s*)?(\d+)', 'Súmula Vinculante'),
    (r'Tema\s+(?:n[.ºo°]\s*)?(\d+)\s+(?:do\s+)?(STF|STJ|TNU)', 'Tema'),
    (r'Tema\s+(?:n[.ºo°]\s*)?(\d+)(?:\s+de\s+repercussão)?', 'Tema'),
]

# Institutos jurídicos previdenciários
INSTITUTOS = [
    "auxílio por incapacidade temporária",
    "aposentadoria por incapacidade permanente",
    "aposentadoria por idade",
    "aposentadoria por tempo de contribuição",
    "aposentadoria especial",
    "aposentadoria da pessoa com deficiência",
    "auxílio-acidente",
    "auxílio-reclusão",
    "pensão por morte",
    "salário-maternidade",
    "salário-família",
    "benefício de prestação continuada",
    "BPC",
    "LOAS",
    "carência",
    "qualidade de segurado",
    "período de graça",
    "fator previdenciário",
    "regra de transição",
    "direito adquirido",
    "decadência",
    "prescrição",
    "revisão de benefício",
    "atividade concomitante",
    "atividade especial",
    "conversão de tempo especial",
    "PPP",
    "LTCAT",
    "CNIS",
    "CTC",
    "desaposentação",
    "acumulação de benefícios",
    "dependente econômico",
    "união estável",
    "segurado facultativo",
    "contribuinte individual",
    "segurado especial",
    "trabalhador rural",
    "tempo de serviço militar",
    "certidão de tempo de contribuição",
    "prova emprestada",
    "reabilitação profissional",
    "incapacidade laborativa",
    "perícia médica",
    "data de início do benefício",
    "DIB",
    "DER",
    "DCB",
    "data de entrada do requerimento",
    "coisa julgada previdenciária",
    "tutela de urgência",
    "antecipação de tutela",
    "implantação de benefício",
    "juizados especiais federais",
    "turma recursal",
    "TNU",
    "pedido de uniformização",
    "INSS",
]


def _normalize_year(num_str):
    """Normaliza ano de 2 dígitos para 4 dígitos em referências legais.
    Ex: '8.213/91' -> '8.213/1991', '3.048/99' -> '3.048/1999'
    """
    if '/' not in num_str:
        return num_str
    parts = num_str.rsplit('/', 1)
    year = parts[1]
    if len(year) == 2:
        y = int(year)
        # Anos >= 30 são 1900s, < 30 são 2000s
        full_year = str(1900 + y) if y >= 30 else str(2000 + y)
        return f"{parts[0]}/{full_year}"
    return num_str


def extract_legislation(text):
    """Extrai referências a legislação com normalização de ano."""
    found = {}  # chave normalizada -> forma de exibição
    for pattern, prefix in LEGISLACAO_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            num = _normalize_year(m.group(1))

            # Normalizar ECs: "EC 103" e "EC 103/2019" -> "EC 103/2019"
            if prefix == 'EC' and '/' not in num:
                # EC sem ano — será mesclada com versão com ano se existir
                bare_key = f"ec {num}"
                # Verificar se já temos versão com ano
                existing_with_year = [k for k in found if k.startswith(bare_key + "/")]
                if existing_with_year:
                    continue  # Já temos versão mais completa
                key = f"{prefix} {num}"
                found[bare_key] = key
            elif prefix == 'EC' and '/' in num:
                # EC com ano — substituir versão bare se existir
                num_only = num.split('/')[0]
                bare_key = f"ec {num_only}"
                if bare_key in found:
                    del found[bare_key]
                key = f"{prefix} {num}"
                found[f"ec {num_only}/{num.split('/')[1]}".lower()] = key
            else:
                key = f"{prefix} {num}".strip()
                found[key.lower()] = key
    return list(found.values())


def extract_sumulas(text):
    """Extrai referências a súmulas e temas, normalizando duplicatas."""
    found = {}
    for pattern, prefix in SUMULA_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            groups = m.groups()
            num = groups[0]
            tribunal = groups[1].upper() if len(groups) > 1 and groups[1] else ""
            if tribunal:
                display = f"{prefix} {num}/{tribunal}"
                norm_key = f"{prefix.lower()} {num}/{tribunal}"
            else:
                display = f"{prefix} {num}"
                norm_key = f"{prefix.lower()} {num}"

            # Se já temos versão com tribunal, preferir essa
            bare_key = f"{prefix.lower()} {num}"
            if tribunal and bare_key in found:
                # Mover capítulos da versão bare para a versão com tribunal
                del found[bare_key]
            elif not tribunal and any(k.startswith(bare_key + "/") for k in found):
                # Já temos versão qualificada, pular a bare
                continue

            found[norm_key] = display
    return list(found.values())


def extract_institutos(text):
    """Extrai menções a institutos jurídicos."""
    text_lower = text.lower()
    found = []
    for inst in INSTITUTOS:
        if inst.lower() in text_lower:
            found.append(inst)
    return found


def build_remissive_index(rascunhos_dir):
    """Constrói índice remissivo a partir de todos os capítulos."""
    # termo -> set de capítulos
    index_leg = defaultdict(set)
    index_sum = defaultdict(set)
    index_inst = defaultdict(set)

    for cap_id in range(1, 24):
        cap_str = f"{cap_id:02d}"
        md_path = rascunhos_dir / f"cap_{cap_str}_rascunho.md"

        if not md_path.exists():
            continue

        text = md_path.read_text(encoding='utf-8')
        cap_label = str(cap_id)

        for leg in extract_legislation(text):
            index_leg[leg].add(cap_label)

        for sum_ in extract_sumulas(text):
            index_sum[sum_].add(cap_label)

        for inst in extract_institutos(text):
            index_inst[inst].add(cap_label)

    return index_leg, index_sum, index_inst


# ═══════════════════════════════════════════════════════
# REFERÊNCIAS BIBLIOGRÁFICAS
# ═══════════════════════════════════════════════════════

def extract_citations(text):
    """Extrai citações no formato (SOBRENOME, ano) ou (SOBRENOME; SOBRENOME, ano)."""
    citations = set()

    # Padrão: (SOBRENOME, 2020) ou (SOBRENOME, 2020, p. 15)
    pattern1 = r'\(([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ\s]+),\s*(\d{4})[^)]*\)'
    for m in re.finditer(pattern1, text):
        author = m.group(1).strip()
        year = m.group(2)
        # Filtrar falsos positivos (tribunais, números de processo)
        if author in ('TRU', 'TNU', 'TRF', 'STF', 'STJ', 'INSS'):
            continue
        if int(year) > 2030 or int(year) < 1900:
            continue
        citations.add(f"{author}, {year}")

    # Padrão: (SOBRENOME; OUTRO, 2020)
    pattern2 = r'\(([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ\s]+;\s*[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ\s]+),\s*(\d{4})[^)]*\)'
    for m in re.finditer(pattern2, text):
        authors = m.group(1).strip()
        year = m.group(2)
        citations.add(f"{authors}, {year}")

    return citations


def build_citation_list(rascunhos_dir):
    """Compila todas as citações de todos os capítulos."""
    all_citations = defaultdict(set)  # citação -> capítulos

    for cap_id in range(1, 24):
        cap_str = f"{cap_id:02d}"
        md_path = rascunhos_dir / f"cap_{cap_str}_rascunho.md"

        if not md_path.exists():
            continue

        text = md_path.read_text(encoding='utf-8')
        for cit in extract_citations(text):
            all_citations[cit].add(str(cap_id))

    return all_citations


def format_index(index_leg, index_sum, index_inst):
    """Formata o índice remissivo como texto."""
    lines = []
    lines.append("INDICE REMISSIVO")
    lines.append("=" * 50)

    # Legislação
    if index_leg:
        lines.append("")
        lines.append("LEGISLACAO")
        lines.append("-" * 40)
        for term in sorted(index_leg.keys()):
            caps = sorted(index_leg[term], key=int)
            lines.append(f"  {term}: Cap. {', '.join(caps)}")

    # Súmulas e Temas
    if index_sum:
        lines.append("")
        lines.append("SUMULAS E TEMAS REPETITIVOS")
        lines.append("-" * 40)
        for term in sorted(index_sum.keys()):
            caps = sorted(index_sum[term], key=int)
            lines.append(f"  {term}: Cap. {', '.join(caps)}")

    # Institutos
    if index_inst:
        lines.append("")
        lines.append("INSTITUTOS JURIDICOS")
        lines.append("-" * 40)
        for term in sorted(index_inst.keys(), key=str.lower):
            caps = sorted(index_inst[term], key=int)
            lines.append(f"  {term}: Cap. {', '.join(caps)}")

    return '\n'.join(lines)


def format_citations(all_citations):
    """Formata a lista de citações como texto."""
    lines = []
    lines.append("REFERENCIAS BIBLIOGRAFICAS EXTRAIDAS")
    lines.append("=" * 50)
    lines.append("(Lista de citacoes encontradas nos capitulos.")
    lines.append(" Completar com dados bibliograficos completos.)")
    lines.append("")

    for cit in sorted(all_citations.keys()):
        caps = sorted(all_citations[cit], key=int)
        lines.append(f"  {cit}  [Cap. {', '.join(caps)}]")

    lines.append("")
    lines.append(f"Total: {len(all_citations)} citacoes unicas")

    return '\n'.join(lines)


def main():
    project_dir = Path(__file__).parent.parent
    rascunhos_dir = project_dir / "output" / "rascunhos"
    output_dir = project_dir / "output"

    print("=" * 60)
    print("GERANDO INDICE REMISSIVO E REFERENCIAS")
    print("=" * 60)

    # Índice Remissivo
    print("\n1. Extraindo indice remissivo...")
    index_leg, index_sum, index_inst = build_remissive_index(rascunhos_dir)
    print(f"   Legislacao: {len(index_leg)} itens")
    print(f"   Sumulas/Temas: {len(index_sum)} itens")
    print(f"   Institutos: {len(index_inst)} itens")

    index_text = format_index(index_leg, index_sum, index_inst)
    index_path = output_dir / "indice_remissivo.txt"
    index_path.write_text(index_text, encoding='utf-8')
    print(f"   Salvo: {index_path}")

    # Referências
    print("\n2. Extraindo referencias bibliograficas...")
    all_citations = build_citation_list(rascunhos_dir)
    print(f"   {len(all_citations)} citacoes unicas encontradas")

    cit_text = format_citations(all_citations)
    cit_path = output_dir / "referencias_extraidas.txt"
    cit_path.write_text(cit_text, encoding='utf-8')
    print(f"   Salvo: {cit_path}")

    print("\n" + "=" * 60)
    print("CONCLUIDO!")
    print("=" * 60)

    return index_leg, index_sum, index_inst, all_citations


if __name__ == '__main__':
    main()
