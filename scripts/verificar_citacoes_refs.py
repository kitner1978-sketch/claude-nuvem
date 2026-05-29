#!/usr/bin/env python3
"""
Verificação de completude: citações no corpo × seção de Referências.

Para cada capítulo:
- Extrai citações parentéticas do corpo: (AUTOR, ano) e Autor (ano)
- Extrai entradas da seção de Doutrina nas Referências
- Cruza as duas listas e reporta:
  1. Citações no corpo sem entrada nas Referências (autor citado mas não listado)
  2. Entradas nas Referências sem citação no corpo (referência fantasma)
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

RASCUNHOS_DIR = Path(r"D:\Projeto Livro\output\rascunhos")


def normalizar_sobrenome(nome: str) -> str:
    """Normaliza sobrenome para matching: uppercase, sem acentos."""
    import unicodedata
    nome = nome.strip().upper()
    # Remover acentos
    nfkd = unicodedata.normalize("NFKD", nome)
    nome = "".join(c for c in nfkd if not unicodedata.combining(c))
    return nome


# ── Extração de citações do corpo ─────────────────────────────────────

def extrair_citacoes_corpo(texto: str, cap_num: int) -> list:
    """Extrai citações doutrinárias do corpo do texto.

    Padrões reconhecidos:
    - (SOBRENOME, ano)
    - (SOBRENOME; SOBRENOME, ano)
    - (SOBRENOME; SOBRENOME; SOBRENOME, ano)
    - (SOBRENOME, ano, p. XX)
    - conforme Sobrenome (ano)
    - Segundo Sobrenome (ano)
    - na lição de Sobrenome (ano)
    """
    citacoes = []
    linhas = texto.splitlines()

    # Encontrar onde termina o corpo e começa a seção de Referências
    fim_corpo = len(linhas)
    for i, linha in enumerate(linhas):
        if re.match(r"^#{2,3}\s+\d+\.\d+\s+Refer[eê]ncias", linha):
            fim_corpo = i
            break

    corpo = "\n".join(linhas[:fim_corpo])

    # Padrão 1: (SOBRENOME, ano) — inclui variantes com ; e p.
    for m in re.finditer(
        r"\(([A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][A-ZÁÉÍÓÚÀÂÊÔÃÕÇ\s]+(?:;\s*[A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][A-ZÁÉÍÓÚÀÂÊÔÃÕÇ\s]+)*),\s*(\d{4})",
        corpo,
    ):
        autores_str = m.group(1)
        ano = m.group(2)
        # Separar múltiplos autores por ;
        for autor in autores_str.split(";"):
            autor = autor.strip()
            if autor and len(autor) > 2:
                citacoes.append({
                    "sobrenome": normalizar_sobrenome(autor),
                    "sobrenome_orig": autor.strip(),
                    "ano": ano,
                    "tipo": "parentetica",
                    "cap": cap_num,
                })

    # Padrão 2: Autor (ano) — inline
    # Ex: "conforme Ibrahim (2025)", "Savaris (2023, p. 215)"
    for m in re.finditer(
        r"(?:conforme|segundo|para|na li[çc][ãa]o de|no magistério de|como ensina|como observa|como aponta|como destaca)\s+"
        r"([A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][a-záéíóúàâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][a-záéíóúàâêôãõç]+)*)\s*\((\d{4})",
        corpo,
        re.IGNORECASE,
    ):
        autor = m.group(1).strip()
        ano = m.group(2)
        sobrenome = autor.split()[-1]  # Último nome
        citacoes.append({
            "sobrenome": normalizar_sobrenome(sobrenome),
            "sobrenome_orig": sobrenome,
            "ano": ano,
            "tipo": "inline",
            "cap": cap_num,
        })

    # Padrão 3: Sobrenome (ano) direto no início de frase ou após vírgula
    for m in re.finditer(
        r"(?:^|[,;]\s+)([A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][a-záéíóúàâêôãõç]+(?:\s+(?:Júnior|Filho|Neto|Sobrinho))?)\s*\((\d{4})",
        corpo,
        re.MULTILINE,
    ):
        autor = m.group(1).strip()
        ano = m.group(2)
        # Filtrar falsos positivos (palavras comuns que não são autores)
        falsos = {"Lei", "Art", "Decreto", "Emenda", "Portaria", "Tema",
                  "Súmula", "Constituição", "CF", "EC", "MP", "Capítulo",
                  "Seção", "Quadro", "Tabela", "Item", "Inciso", "Alínea",
                  "Parágrafo", "Janeiro", "Fevereiro", "Março", "Abril",
                  "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
                  "Novembro", "Dezembro", "Brasil", "Plano", "Regime",
                  "Sistema", "Programa", "Decreto", "Resolução", "Instrução",
                  "Nota", "Cap", "IN", "RPS", "CPC", "CLT", "LOPS", "SINPAS",
                  "INSS", "RGPS", "STF", "STJ", "TNU", "TRF", "Turma",
                  "Seção", "Plenário", "Relator", "Relatora", "Min",
                  "Ministro", "Ministra", "ADI", "ADIs", "REsp"}
        if autor not in falsos and len(autor) > 3:
            citacoes.append({
                "sobrenome": normalizar_sobrenome(autor.split()[-1]),
                "sobrenome_orig": autor,
                "ano": ano,
                "tipo": "inline_direto",
                "cap": cap_num,
            })

    return citacoes


# ── Extração de entradas de Referências ───────────────────────────────

def extrair_refs_doutrina(texto: str, cap_num: int) -> list:
    """Extrai entradas da seção Doutrina das Referências.

    Lida com 3 formatos encontrados nos capítulos:
    1. Subsecção `#### X.Y.3 Doutrina` com entradas sem prefixo
    2. Subsecção `#### X.Y.3 Doutrina` com entradas com bullet `- `
    3. Seção flat `### X.Y Referências` sem subsecções (tudo junto)
    """
    linhas = texto.splitlines()
    refs = []

    # Estratégia 1: procurar subsecção Doutrina
    in_doutrina = False
    # Estratégia 2: se não encontrar Doutrina, usar seção Referências inteira
    in_refs_flat = False
    refs_flat_start = None

    tem_doutrina = any(
        re.match(r"^#{3,4}\s+\d+\.\d+\.\d+\s+Doutrina", l) for l in linhas
    )

    for i, linha in enumerate(linhas):
        if tem_doutrina:
            if re.match(r"^#{3,4}\s+\d+\.\d+\.\d+\s+Doutrina", linha):
                in_doutrina = True
                continue
            if in_doutrina:
                if linha.startswith("#"):
                    break
                refs.extend(_parse_ref_line(linha, cap_num))
        else:
            # Seção flat: ### X.Y Referências (sem subsecções Legislação/Jurisprudência/Doutrina)
            if re.match(r"^#{2,3}\s+\d+\.\d+\s+Refer[eê]ncias", linha):
                in_refs_flat = True
                continue
            if in_refs_flat:
                if linha.startswith("#"):
                    break
                # Na seção flat, pular linhas de legislação/jurisprudência
                stripped = linha.strip().lstrip("- ")
                if stripped.startswith("BRASIL") or stripped.startswith("SUPREMO") or stripped.startswith("SUPERIOR"):
                    continue
                refs.extend(_parse_ref_line(linha, cap_num))

    return refs


def _parse_ref_line(linha: str, cap_num: int) -> list:
    """Parse uma linha de referência bibliográfica em qualquer formato."""
    stripped = linha.strip()
    if not stripped:
        return []

    # Remover bullet point
    stripped = re.sub(r"^-\s+", "", stripped)

    # Remover markdown bold/italic dos títulos para facilitar o parse
    cleaned = stripped.replace("**", "").replace("*", "")

    m = re.match(
        r"^([A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][A-ZÁÉÍÓÚÀÂÊÔÃÕÇ\s]+(?:JÚNIOR|FILHO|NETO|SOBRINHO)?)"
        r"(?:;\s*[A-ZÁÉÍÓÚÀÂÊÔÃÕÇ][^.]+)?"  # coautores opcionais
        r",\s*[^.]+\.\s*"  # primeiro nome
        r".+?(\d{4})",
        cleaned,
    )
    if m:
        sobrenome = m.group(1).strip()
        ano = m.group(2)
        return [{
            "sobrenome": normalizar_sobrenome(sobrenome),
            "sobrenome_orig": sobrenome,
            "ano": ano,
            "entrada_completa": stripped[:100],
            "cap": cap_num,
        }]

    return []


def extrair_refs_jurisprudencia(texto: str, cap_num: int) -> list:
    """Extrai Temas e Súmulas da seção de Jurisprudência."""
    linhas = texto.splitlines()
    refs = []

    in_jurisp = False
    for i, linha in enumerate(linhas):
        if re.match(r"^#{3,4}\s+\d+\.\d+\.\d+\s+Jurisprud[eê]ncia", linha):
            in_jurisp = True
            continue

        if in_jurisp:
            if re.match(r"^#{3,4}\s+\d+\.\d+\.\d+\s+Doutrina", linha):
                break
            if linha.startswith("#"):
                break

            # Extrair Temas
            for m in re.finditer(r"Tema\s+(\d+(?:\.\d+)?)", linha):
                refs.append({
                    "tipo": "tema",
                    "numero": m.group(1),
                    "cap": cap_num,
                })

            # Extrair Súmulas
            for m in re.finditer(r"S[úu]mula\s+(\d+)", linha):
                refs.append({
                    "tipo": "sumula",
                    "numero": m.group(1),
                    "cap": cap_num,
                })

    return refs


# ── Cruzamento ────────────────────────────────────────────────────────

def cruzar(citacoes: list, refs: list, cap_num: int) -> dict:
    """Cruza citações do corpo com entradas de Referências para um capítulo."""
    # Montar conjuntos normalizados
    citados = set()
    for c in citacoes:
        citados.add((c["sobrenome"], c["ano"]))

    referenciados = set()
    for r in refs:
        referenciados.add((r["sobrenome"], r["ano"]))

    # Citados no corpo mas ausentes nas Referências
    sem_ref = citados - referenciados
    # Nas Referências mas não citados no corpo
    sem_citacao = referenciados - citados

    # Tentar matching mais flexível (só sobrenome, sem ano)
    sobrenomes_citados = set(s for s, _ in citados)
    sobrenomes_refs = set(s for s, _ in referenciados)

    # Detalhes dos sem_ref
    sem_ref_detalhes = []
    for sob, ano in sorted(sem_ref):
        # Verificar se o sobrenome existe nas refs com outro ano
        if sob in sobrenomes_refs:
            ref_anos = [a for s, a in referenciados if s == sob]
            sem_ref_detalhes.append({
                "sobrenome": sob,
                "ano_citado": ano,
                "tipo": "ANO_DIVERGENTE",
                "anos_refs": ref_anos,
                "cap": cap_num,
            })
        else:
            # Obter o sobrenome original da citação
            orig = next((c["sobrenome_orig"] for c in citacoes if c["sobrenome"] == sob), sob)
            sem_ref_detalhes.append({
                "sobrenome": sob,
                "sobrenome_orig": orig,
                "ano_citado": ano,
                "tipo": "AUTOR_AUSENTE",
                "cap": cap_num,
            })

    sem_citacao_detalhes = []
    for sob, ano in sorted(sem_citacao):
        if sob in sobrenomes_citados:
            cit_anos = [a for s, a in citados if s == sob]
            sem_citacao_detalhes.append({
                "sobrenome": sob,
                "ano_ref": ano,
                "tipo": "ANO_DIVERGENTE_REF",
                "anos_citados": cit_anos,
                "cap": cap_num,
            })
        else:
            orig = next((r["sobrenome_orig"] for r in refs if r["sobrenome"] == sob), sob)
            sem_citacao_detalhes.append({
                "sobrenome": sob,
                "sobrenome_orig": orig,
                "ano_ref": ano,
                "tipo": "REF_FANTASMA",
                "cap": cap_num,
            })

    return {
        "total_citacoes": len(citados),
        "total_refs": len(referenciados),
        "sem_ref": sem_ref_detalhes,
        "sem_citacao": sem_citacao_detalhes,
    }


# ── Main ──────────────────────────────────────────────────────────────

def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print("VERIFICAÇÃO DE COMPLETUDE: CITAÇÕES × REFERÊNCIAS")
    print("=" * 70)

    total_sem_ref = 0
    total_sem_citacao = 0
    total_citacoes = 0
    total_refs = 0
    resultados_por_cap = {}

    for f in sorted(RASCUNHOS_DIR.glob("cap_*_rascunho.md")):
        texto = f.read_text(encoding="utf-8")
        cap_match = re.search(r"^##\s+Cap[ií]tulo\s+(\d+)", texto, re.MULTILINE)
        if not cap_match:
            continue

        cap_num = int(cap_match.group(1))
        citacoes = extrair_citacoes_corpo(texto, cap_num)
        refs = extrair_refs_doutrina(texto, cap_num)

        resultado = cruzar(citacoes, refs, cap_num)
        resultados_por_cap[cap_num] = resultado

        total_citacoes += resultado["total_citacoes"]
        total_refs += resultado["total_refs"]
        total_sem_ref += len(resultado["sem_ref"])
        total_sem_citacao += len(resultado["sem_citacao"])

    print(f"\nCapítulos analisados: {len(resultados_por_cap)}")
    print(f"Total de autores citados (únicos por cap): {total_citacoes}")
    print(f"Total de entradas em Referências/Doutrina: {total_refs}")

    # Resumo por capítulo
    print(f"\n{'=' * 70}")
    print(f"{'Cap':>5} {'Citações':>10} {'Refs':>6} {'Sem Ref':>8} {'Fantasma':>9}")
    print("-" * 45)
    for cap in sorted(resultados_por_cap.keys()):
        r = resultados_por_cap[cap]
        flag = ""
        if r["sem_ref"] or r["sem_citacao"]:
            flag = " ←"
        print(f"  {cap:02d}   {r['total_citacoes']:>8}   {r['total_refs']:>4}   {len(r['sem_ref']):>6}   {len(r['sem_citacao']):>7}{flag}")

    # Detalhes dos problemas
    if total_sem_ref > 0:
        print(f"\n{'=' * 70}")
        print(f"CITAÇÕES SEM ENTRADA NAS REFERÊNCIAS ({total_sem_ref})")
        print("=" * 70)
        for cap in sorted(resultados_por_cap.keys()):
            r = resultados_por_cap[cap]
            if r["sem_ref"]:
                print(f"\n  Cap. {cap:02d}:")
                for item in r["sem_ref"]:
                    if item["tipo"] == "ANO_DIVERGENTE":
                        print(f"    {item['sobrenome']} ({item['ano_citado']}) — "
                              f"nas refs com ano(s): {', '.join(item['anos_refs'])}")
                    else:
                        orig = item.get("sobrenome_orig", item["sobrenome"])
                        print(f"    {orig} ({item['ano_citado']}) — AUSENTE nas Referências")

    if total_sem_citacao > 0:
        print(f"\n{'=' * 70}")
        print(f"REFERÊNCIAS SEM CITAÇÃO NO CORPO ({total_sem_citacao})")
        print("=" * 70)
        for cap in sorted(resultados_por_cap.keys()):
            r = resultados_por_cap[cap]
            if r["sem_citacao"]:
                print(f"\n  Cap. {cap:02d}:")
                for item in r["sem_citacao"]:
                    if item["tipo"] == "ANO_DIVERGENTE_REF":
                        print(f"    {item['sobrenome']} ({item['ano_ref']}) — "
                              f"citado no corpo com ano(s): {', '.join(item['anos_citados'])}")
                    else:
                        orig = item.get("sobrenome_orig", item["sobrenome"])
                        print(f"    {orig} ({item['ano_ref']}) — NÃO citado no corpo")

    # Resultado final
    print(f"\n{'=' * 70}")
    if total_sem_ref == 0 and total_sem_citacao == 0:
        print("RESULTADO: Todas as citações têm referência correspondente!")
    else:
        print(f"RESULTADO: {total_sem_ref} citações sem referência, "
              f"{total_sem_citacao} referências fantasma")
    print("=" * 70)

    # Salvar relatório
    relatorio = RASCUNHOS_DIR.parent / "relatorio_citacoes.txt"
    with open(relatorio, "w", encoding="utf-8") as f:
        f.write(f"Citações sem referência: {total_sem_ref}\n")
        f.write(f"Referências fantasma: {total_sem_citacao}\n\n")

        for cap in sorted(resultados_por_cap.keys()):
            r = resultados_por_cap[cap]
            if r["sem_ref"] or r["sem_citacao"]:
                f.write(f"\n== Cap. {cap:02d} ==\n")
                for item in r["sem_ref"]:
                    f.write(f"  CORPO sem REF: {item['sobrenome']} ({item.get('ano_citado', '?')})\n")
                for item in r["sem_citacao"]:
                    f.write(f"  REF sem CORPO: {item['sobrenome']} ({item.get('ano_ref', '?')})\n")

    print(f"\nRelatório salvo em: {relatorio}")

    return total_sem_ref + total_sem_citacao


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
