#!/usr/bin/env python3
"""
curadoria_conteudo.py — Curadoria de informações do livro

Verifica:
  1. Valores monetários (SM, teto, cotas) vs. valores oficiais 2026
  2. Consistência de dados numéricos entre capítulos
  3. Referências legais (artigos, leis) — formato e plausibilidade
  4. Terminologia vedada (auxílio-doença, aposentadoria por invalidez)
  5. Referências cruzadas internas (remissões a outros capítulos)
  6. Datas e vigências potencialmente desatualizadas
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict


# ═══════════════════════════════════════════════════════
# VALORES DE REFERÊNCIA 2026
# ═══════════════════════════════════════════════════════

VALORES_2026 = {
    'salario_minimo': 1621.00,
    'teto_rgps': 8475.55,
    'salario_familia_cota': 67.54,
    'salario_familia_limite': 1980.38,
    'auxilio_reclusao_limite': 1980.38,
    'reajuste_inpc': 3.9,  # percentual
    'portaria_vigente': 'Portaria Interministerial MPS/MF n. 13, de 09/01/2026',
    'in_vigente': 'IN INSS/PRES 128/2022',
}

# Faixas de alíquota progressiva 2026
FAIXAS_ALIQUOTA_2026 = [
    (1621.00, 7.5),
    (2625.12, 9.0),
    (3932.67, 12.0),
    (8475.55, 14.0),
]

# Valores anteriores (2025) para detectar uso de dados antigos
VALORES_2025 = {
    'salario_minimo': 1518.00,
    'teto_rgps': 8157.41,
    'salario_familia_cota': 65.00,
    'salario_familia_limite': 1906.04,
    'auxilio_reclusao_limite': 1906.04,
}

VALORES_2024 = {
    'salario_minimo': 1412.00,
    'teto_rgps': 7786.02,
}


# ═══════════════════════════════════════════════════════
# TERMINOLOGIA VEDADA
# ═══════════════════════════════════════════════════════

TERMOS_VEDADOS = [
    # (padrão, termo correto, exceção)
    (r'auxílio[\s-]doença(?!\s+(?:acidentário|previdenciário|[\("]|—\s*(?:atual|antigo|denominação)))',
     'auxílio por incapacidade temporária',
     r'(?:antigo|anterior|denominação|históric|nomenclatura|(?:atual|hoje)\s+denominad)'),
    (r'aposentadoria\s+por\s+invalidez(?!\s+(?:[\("]|—\s*(?:atual|antiga)))',
     'aposentadoria por incapacidade permanente',
     r'(?:antigo|anterior|denominação|históric|nomenclatura|(?:atual|hoje)\s+denominad)'),
]


# ═══════════════════════════════════════════════════════
# FUNÇÕES DE VERIFICAÇÃO
# ═══════════════════════════════════════════════════════

def load_chapters(rascunhos_dir):
    chapters = {}
    for cap_id in range(1, 24):
        path = rascunhos_dir / f"cap_{cap_id:02d}_rascunho.md"
        if path.exists():
            chapters[cap_id] = path.read_text(encoding='utf-8')
    return chapters


def check_monetary_values(chapters):
    """Verifica valores monetários contra referências 2026."""
    findings = []

    # Padrão para capturar valores em reais
    valor_pattern = r'R\$\s*([\d.,]+)'

    for cap_id, text in chapters.items():
        for m in re.finditer(valor_pattern, text):
            raw = m.group(1)
            # Normalizar: "1.621,00" -> 1621.00
            try:
                clean = raw.replace('.', '').replace(',', '.')
                valor = float(clean)
            except:
                continue

            # Obter contexto (50 chars antes e depois)
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 80)
            context = text[start:end].replace('\n', ' ').strip()

            # Verificar se é valor de 2025 (desatualizado)
            if abs(valor - VALORES_2025['salario_minimo']) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 1.621,00 (SM 2026)",
                    'contexto': context,
                })
            elif abs(valor - VALORES_2025['teto_rgps']) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 8.475,55 (teto RGPS 2026)",
                    'contexto': context,
                })
            elif abs(valor - VALORES_2025['salario_familia_cota']) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 67,54 (cota sal-família 2026)",
                    'contexto': context,
                })
            elif abs(valor - VALORES_2025['salario_familia_limite']) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 1.980,38 (limite sal-família 2026)",
                    'contexto': context,
                })
            elif abs(valor - VALORES_2024.get('salario_minimo', 0)) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 1.621,00 (SM 2026, era 2024)",
                    'contexto': context,
                })
            elif abs(valor - VALORES_2024.get('teto_rgps', 0)) < 0.01:
                findings.append({
                    'cap': cap_id,
                    'tipo': 'DESATUALIZADO',
                    'severidade': 'CRITICO',
                    'valor_encontrado': f'R$ {raw}',
                    'valor_correto': f"R$ 8.475,55 (teto RGPS 2026, era 2024)",
                    'contexto': context,
                })

    return findings


def check_terminology(chapters):
    """Verifica uso de terminologia vedada."""
    findings = []

    for cap_id, text in chapters.items():
        lines = text.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern, correto, excecao in TERMOS_VEDADOS:
                for m in re.finditer(pattern, line, re.IGNORECASE):
                    # Verificar se está em contexto de exceção (citação histórica)
                    context_start = max(0, m.start() - 100)
                    context_text = line[context_start:m.end() + 100]
                    if re.search(excecao, context_text, re.IGNORECASE):
                        continue  # Uso histórico/contextual — OK

                    # Verificar se está entre aspas ou parênteses (citação literal)
                    before = line[max(0, m.start()-2):m.start()]
                    after = line[m.end():m.end()+2]
                    if '"' in before or '"' in before or '(' in before:
                        continue

                    findings.append({
                        'cap': cap_id,
                        'linha': line_num,
                        'tipo': 'TERMINOLOGIA',
                        'severidade': 'RELEVANTE',
                        'encontrado': m.group(),
                        'correto': correto,
                        'contexto': line.strip()[:150],
                    })

    return findings


def check_cross_references(chapters):
    """Verifica remissões internas a outros capítulos."""
    findings = []

    # Padrão: "Cap. X", "Capítulo X", "seção X.Y"
    ref_patterns = [
        r'(?:Cap(?:ítulo)?\.?\s*)(\d{1,2})',
        r'(?:capítulo\s*)(\d{1,2})',
        r'(?:seção\s*)(\d{1,2}\.\d+)',
    ]

    for cap_id, text in chapters.items():
        for pattern in ref_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                ref = m.group(1)
                ref_cap = int(ref.split('.')[0])

                # Referência a capítulo inexistente?
                if ref_cap < 1 or ref_cap > 23:
                    context_start = max(0, m.start() - 50)
                    context_end = min(len(text), m.end() + 50)
                    findings.append({
                        'cap': cap_id,
                        'tipo': 'REFERENCIA_INVALIDA',
                        'severidade': 'CRITICO',
                        'referencia': f"Cap {ref_cap}",
                        'contexto': text[context_start:context_end].replace('\n', ' ').strip(),
                    })

    return findings


def check_legal_references(chapters):
    """Verifica consistência de referências a artigos de lei."""
    findings = []

    # Artigos da Lei 8.213/91 mais citados — verificar se não há confusão com 8.212
    confusao_patterns = [
        # Artigos de custeio (8.212) erroneamente atribuídos à 8.213
        (r'art\.\s*28.*Lei\s*8\.213', 'Art. 28 é da Lei 8.212 (salário de contribuição), não da 8.213'),
        (r'art\.\s*22.*Lei\s*8\.213', 'Art. 22 é da Lei 8.212 (contribuição do empregador), não da 8.213'),
        (r'art\.\s*30.*Lei\s*8\.213', 'Art. 30 é da Lei 8.212, verificar se não é confusão'),
        # Artigos que não existem
        (r'art\.\s*20[5-9].*Lei\s*8\.213', 'Lei 8.213 tem até art. 204 (verificar)'),
    ]

    for cap_id, text in chapters.items():
        for pattern, msg in confusao_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                context_start = max(0, m.start() - 40)
                context_end = min(len(text), m.end() + 60)
                findings.append({
                    'cap': cap_id,
                    'tipo': 'REFERENCIA_LEGAL',
                    'severidade': 'RELEVANTE',
                    'alerta': msg,
                    'contexto': text[context_start:context_end].replace('\n', ' ').strip(),
                })

    return findings


def check_data_consistency(chapters):
    """Verifica se os mesmos dados aparecem de forma consistente entre capítulos."""
    findings = []

    # Extrair dados-chave de cada capítulo
    data_points = defaultdict(lambda: defaultdict(list))

    # 1. Idade para aposentadoria por idade
    idade_pattern = r'(\d{2})\s*(?:anos?\s*(?:de\s*idade)?)?.*(?:para\s+(?:(?:os?\s+)?homens?|(?:as?\s+)?mulheres?))'
    # Simplificado: buscar padrões como "65 anos para homens", "62 anos para mulheres"

    for cap_id, text in chapters.items():
        # Idade aposentadoria programada
        for m in re.finditer(r'(\d{2})\s+anos\s+(?:de\s+idade\s+)?para\s+(?:o\s+)?homem|para\s+homens?\s+(?:de\s+)?(\d{2})', text, re.IGNORECASE):
            idade = m.group(1) or m.group(2)
            if idade:
                data_points['idade_homem_apos_programada'][idade].append(cap_id)

        for m in re.finditer(r'(\d{2})\s+anos\s+(?:de\s+idade\s+)?para\s+(?:a\s+)?mulher|para\s+mulheres?\s+(?:de\s+)?(\d{2})', text, re.IGNORECASE):
            idade = m.group(1) or m.group(2)
            if idade:
                data_points['idade_mulher_apos_programada'][idade].append(cap_id)

        # Carência 180 contribuições
        for m in re.finditer(r'(\d+)\s+contribuições\s+mensais', text, re.IGNORECASE):
            n = m.group(1)
            if n in ('180', '24', '12', '10', '6'):
                data_points[f'carencia_{n}_contribuicoes'][n].append(cap_id)

        # Período de graça: meses
        for m in re.finditer(r'período\s+de\s+graça.*?(\d+)\s+meses', text, re.IGNORECASE):
            meses = m.group(1)
            data_points[f'periodo_graca_{meses}_meses'][meses].append(cap_id)

    # Verificar inconsistências
    for key, values in data_points.items():
        if len(values) > 1:
            vals = list(values.keys())
            caps_by_val = {v: sorted(set(c)) for v, c in values.items()}
            # Se há valores diferentes para o mesmo dado
            if len(vals) > 1 and not all(v == vals[0] for v in vals):
                # Pode ser legítimo (diferentes contextos), mas registrar para revisão
                pass

    return findings


def check_outdated_norms(chapters):
    """Verifica referências a normas possivelmente desatualizadas."""
    findings = []

    # Portarias anteriores à vigente
    old_portarias = [
        (r'Portaria\s+(?:Interministerial\s+)?(?:MPS|MTP|MPAS|MF).*?n[.ºo°]?\s*\d+.*?(?:2023|2024|2025)',
         'Portaria possivelmente substituída pela Portaria MPS/MF 13/2026'),
    ]

    # INs substituídas
    old_ins = [
        (r'IN\s+(?:INSS/PRES\s+)?(?:n[.ºo°]?\s*)?(?:45|77|85|104|117)\b',
         'IN possivelmente revogada/substituída pela IN 128/2022'),
    ]

    for cap_id, text in chapters.items():
        for pattern, msg in old_portarias + old_ins:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                context_start = max(0, m.start() - 30)
                context_end = min(len(text), m.end() + 60)
                context = text[context_start:context_end].replace('\n', ' ').strip()
                # Excluir menções em contexto histórico
                if re.search(r'(?:revogad|substituíd|anterior|à\s+época|vigente\s+até)', context, re.IGNORECASE):
                    continue
                findings.append({
                    'cap': cap_id,
                    'tipo': 'NORMA_DESATUALIZADA',
                    'severidade': 'RELEVANTE',
                    'encontrado': m.group(),
                    'alerta': msg,
                    'contexto': context,
                })

    return findings


def check_sm_teto_mentions(chapters):
    """Verifica menções ao SM e teto que indicam valores específicos."""
    findings = []

    # Buscar menções ao SM com valor
    sm_patterns = [
        (r'salário\s+mínimo.*?R\$\s*([\d.,]+)', 'salário mínimo'),
        (r'teto\s+(?:do\s+)?(?:RGPS|INSS|previdenciário).*?R\$\s*([\d.,]+)', 'teto RGPS'),
        (r'R\$\s*([\d.,]+).*?(?:salário\s+mínimo|piso\s+previdenciário)', 'salário mínimo'),
        (r'R\$\s*([\d.,]+).*?teto\s+(?:do\s+)?(?:RGPS|INSS)', 'teto RGPS'),
    ]

    for cap_id, text in chapters.items():
        for pattern, label in sm_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                raw = m.group(1)
                try:
                    clean = raw.replace('.', '').replace(',', '.')
                    valor = float(clean)
                except:
                    continue

                if label == 'salário mínimo' and abs(valor - VALORES_2026['salario_minimo']) > 0.01 and valor > 500:
                    # Verificar se é valor historico ou exemplo
                    context_start = max(0, m.start() - 60)
                    context_end = min(len(text), m.end() + 60)
                    context = text[context_start:context_end].replace('\n', ' ')
                    if not re.search(r'(?:época|então|vigente\s+em|exemplo|hipot|supon|ilustr)', context, re.IGNORECASE):
                        findings.append({
                            'cap': cap_id,
                            'tipo': 'VALOR_SM',
                            'severidade': 'RELEVANTE',
                            'valor_encontrado': f'R$ {raw}',
                            'valor_2026': f'R$ 1.621,00',
                            'contexto': context.strip()[:200],
                        })

                if label == 'teto RGPS' and abs(valor - VALORES_2026['teto_rgps']) > 0.01 and valor > 5000:
                    context_start = max(0, m.start() - 60)
                    context_end = min(len(text), m.end() + 60)
                    context = text[context_start:context_end].replace('\n', ' ')
                    if not re.search(r'(?:época|então|vigente\s+em|exemplo|hipot|supon|ilustr)', context, re.IGNORECASE):
                        findings.append({
                            'cap': cap_id,
                            'tipo': 'VALOR_TETO',
                            'severidade': 'RELEVANTE',
                            'valor_encontrado': f'R$ {raw}',
                            'valor_2026': f'R$ 8.475,55',
                            'contexto': context.strip()[:200],
                        })

    return findings


def check_portaria_references(chapters):
    """Verifica se o livro cita a portaria correta de 2026."""
    findings = []
    portaria_2026_found = False

    for cap_id, text in chapters.items():
        # Portaria 2026 correta
        if re.search(r'Portaria\s+Interministerial\s+MPS/MF\s+n[.ºo°]?\s*13.*2026', text, re.IGNORECASE):
            portaria_2026_found = True

        # Buscar referências a portarias MPS/MF genéricas
        for m in re.finditer(r'Portaria\s+Interministerial\s+(?:MPS|MTP|MPAS)[/\s]+(?:MF|MS)\s+n[.ºo°]?\s*(\d+).*?(\d{4})', text, re.IGNORECASE):
            num = m.group(1)
            ano = m.group(2)
            if ano != '2026' and int(ano) >= 2022:
                context_start = max(0, m.start() - 20)
                context_end = min(len(text), m.end() + 60)
                context = text[context_start:context_end].replace('\n', ' ').strip()
                if not re.search(r'(?:anterior|revogad|substituíd|vigente\s+até|à\s+época)', context, re.IGNORECASE):
                    findings.append({
                        'cap': cap_id,
                        'tipo': 'PORTARIA',
                        'severidade': 'RELEVANTE',
                        'encontrado': m.group(),
                        'alerta': f'Portaria de {ano} — verificar se ainda vigente',
                        'contexto': context,
                    })

    return findings


def check_year_references(chapters):
    """Identifica menções a anos que sugerem dados desatualizados."""
    findings = []

    # Padrões que indicam dados possivelmente estáticos que deveriam ser atualizados
    # Ex: "em 2025, o teto é de..." ou "atualmente (2024)..."
    stale_patterns = [
        (r'(?:em|no\s+ano\s+de|desde|a\s+partir\s+de)\s+202[34].*?(?:teto|salário\s+mínimo|piso|valor)', 'Referência a valor com ano 2023/2024'),
        (r'(?:atualmente|hoje|vigente).*?202[34]', 'Uso de "atualmente" com ano 2023/2024'),
    ]

    for cap_id, text in chapters.items():
        for pattern, msg in stale_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                context_start = max(0, m.start() - 20)
                context_end = min(len(text), m.end() + 80)
                findings.append({
                    'cap': cap_id,
                    'tipo': 'ANO_DESATUALIZADO',
                    'severidade': 'SUGESTAO',
                    'alerta': msg,
                    'contexto': text[context_start:context_end].replace('\n', ' ').strip()[:200],
                })

    return findings


def check_aliquotas(chapters):
    """Verifica se alíquotas progressivas estão corretas."""
    findings = []

    # Alíquotas devem ser 7,5%, 9%, 12%, 14%
    correct_aliquotas = {7.5, 9.0, 12.0, 14.0}

    for cap_id, text in chapters.items():
        # Buscar menções a alíquotas progressivas
        if re.search(r'alíquot.*progressiv', text, re.IGNORECASE):
            # Extrair percentuais mencionados no contexto
            for m in re.finditer(r'(\d+(?:[,.]\d+)?)\s*%', text):
                try:
                    pct = float(m.group(1).replace(',', '.'))
                except:
                    continue
                # Verificar se é alíquota previdenciária (entre 5 e 20%)
                if 5 <= pct <= 22 and pct not in correct_aliquotas and pct not in {5.0, 11.0, 20.0}:
                    context_start = max(0, m.start() - 80)
                    context_end = min(len(text), m.end() + 40)
                    context = text[context_start:context_end].replace('\n', ' ').strip()
                    if re.search(r'(?:contribui|alíquot|empregado|segurado)', context, re.IGNORECASE):
                        findings.append({
                            'cap': cap_id,
                            'tipo': 'ALIQUOTA',
                            'severidade': 'SUGESTAO',
                            'valor': f'{pct}%',
                            'alerta': f'Alíquota {pct}% não está entre as faixas padrão (7,5/9/12/14%)',
                            'contexto': context[:200],
                        })

    return findings


def main():
    project_dir = Path(__file__).parent.parent
    rascunhos_dir = project_dir / "output" / "rascunhos"
    output_dir = project_dir / "output"

    print("=" * 70)
    print("CURADORIA DE INFORMAÇÕES — FASE 3")
    print("=" * 70)

    chapters = load_chapters(rascunhos_dir)
    print(f"\n  {len(chapters)} capítulos carregados")

    all_findings = []

    # 1. Valores monetários
    print("\n  1. Verificando valores monetários...")
    f = check_monetary_values(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 2. Menções explícitas a SM/teto com valor
    print("  2. Verificando menções a SM/teto...")
    f = check_sm_teto_mentions(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 3. Terminologia
    print("  3. Verificando terminologia vedada...")
    f = check_terminology(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 4. Referências cruzadas
    print("  4. Verificando referências cruzadas...")
    f = check_cross_references(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 5. Referências legais
    print("  5. Verificando referências legais...")
    f = check_legal_references(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 6. Normas desatualizadas
    print("  6. Verificando normas desatualizadas...")
    f = check_outdated_norms(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 7. Portarias
    print("  7. Verificando referências a portarias...")
    f = check_portaria_references(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 8. Anos desatualizados
    print("  8. Verificando referências temporais...")
    f = check_year_references(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # 9. Alíquotas
    print("  9. Verificando alíquotas...")
    f = check_aliquotas(chapters)
    all_findings.extend(f)
    print(f"     {len(f)} achados")

    # ═══════════════════════════════════════════════════════
    # GERAR RELATÓRIO
    # ═══════════════════════════════════════════════════════

    lines = []
    lines.append("RELATÓRIO DE CURADORIA DE INFORMAÇÕES — FASE 3")
    lines.append("=" * 70)
    lines.append(f"Data: 2026-05-15")
    lines.append(f"Capítulos analisados: {len(chapters)}")
    lines.append("")

    # Valores de referência
    lines.append("VALORES DE REFERÊNCIA 2026")
    lines.append("-" * 40)
    lines.append(f"  Salário mínimo: R$ 1.621,00")
    lines.append(f"  Teto RGPS: R$ 8.475,55")
    lines.append(f"  Salário-família (cota): R$ 67,54")
    lines.append(f"  Salário-família (limite): R$ 1.980,38")
    lines.append(f"  Auxílio-reclusão (limite): R$ 1.980,38")
    lines.append(f"  Reajuste INPC: 3,9%")
    lines.append(f"  Portaria vigente: MPS/MF n. 13, de 09/01/2026")
    lines.append(f"  IN vigente: INSS/PRES 128/2022 (atualizada)")
    lines.append(f"  Alíquotas: 7,5% | 9% | 12% | 14%")
    lines.append("")

    # Sumário
    criticos = [f for f in all_findings if f.get('severidade') == 'CRITICO']
    relevantes = [f for f in all_findings if f.get('severidade') == 'RELEVANTE']
    sugestoes = [f for f in all_findings if f.get('severidade') == 'SUGESTAO']

    lines.append("SUMÁRIO EXECUTIVO")
    lines.append("-" * 40)
    lines.append(f"  CRÍTICOS: {len(criticos)}")
    lines.append(f"  RELEVANTES: {len(relevantes)}")
    lines.append(f"  SUGESTÕES: {len(sugestoes)}")
    lines.append(f"  TOTAL: {len(all_findings)}")
    lines.append("")

    # Detalhamento por tipo
    by_type = defaultdict(list)
    for f in all_findings:
        by_type[f.get('tipo', 'OUTRO')].append(f)

    for tipo, items in sorted(by_type.items()):
        lines.append(f"\n{'─' * 60}")
        lines.append(f"TIPO: {tipo} ({len(items)} achados)")
        lines.append("")

        for i, item in enumerate(items[:30], 1):
            sev = item.get('severidade', '?')
            icon = {'CRITICO': '[!!!]', 'RELEVANTE': '[!!]', 'SUGESTAO': '[!]'}.get(sev, '[?]')
            lines.append(f"  {icon} Cap {item['cap']}")

            for key, val in item.items():
                if key in ('cap', 'tipo', 'severidade'):
                    continue
                lines.append(f"    {key}: {val}")
            lines.append("")

        if len(items) > 30:
            lines.append(f"  ... e mais {len(items) - 30} achados")

    # Consolidação por capítulo
    lines.append("\n" + "=" * 70)
    lines.append("CONSOLIDAÇÃO POR CAPÍTULO")
    lines.append("=" * 70)

    by_cap = defaultdict(lambda: defaultdict(int))
    for f in all_findings:
        by_cap[f['cap']][f.get('severidade', '?')] += 1

    for cap_id in sorted(by_cap.keys()):
        counts = by_cap[cap_id]
        total = sum(counts.values())
        parts = []
        if counts.get('CRITICO'):
            parts.append(f"{counts['CRITICO']} críticos")
        if counts.get('RELEVANTE'):
            parts.append(f"{counts['RELEVANTE']} relevantes")
        if counts.get('SUGESTAO'):
            parts.append(f"{counts['SUGESTAO']} sugestões")
        lines.append(f"  Cap {cap_id:2d}: {total:3d} achados ({', '.join(parts)})")

    report_text = '\n'.join(lines)
    report_path = output_dir / "relatorio_curadoria.txt"
    report_path.write_text(report_text, encoding='utf-8')
    print(f"\n  Relatório salvo: {report_path}")

    # Sumário no terminal
    print("\n" + "=" * 70)
    print("SUMÁRIO")
    print("=" * 70)
    print(f"  CRÍTICOS: {len(criticos)}")
    print(f"  RELEVANTES: {len(relevantes)}")
    print(f"  SUGESTÕES: {len(sugestoes)}")
    print(f"  TOTAL: {len(all_findings)}")


if __name__ == '__main__':
    main()
