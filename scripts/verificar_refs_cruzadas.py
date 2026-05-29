#!/usr/bin/env python3
"""
Validação de referências cruzadas internas do livro.

Extrai todos os headings (capítulos e seções) dos 23 MDs e cruza com
todas as menções a "Cap. X", "Capítulo X", "seção X.Y" no corpo.
Reporta referências quebradas (seção que não existe, capítulo errado).
"""

import re
import sys
import os
from pathlib import Path
from collections import defaultdict

RASCUNHOS_DIR = Path(r"D:\Projeto Livro\output\rascunhos")

# ── Extração de headings ──────────────────────────────────────────────

def extrair_headings(filepath: Path) -> dict:
    """Retorna dict com cap_num e set de seções existentes (ex: {'10.8', '10.8.2'})."""
    texto = filepath.read_text(encoding="utf-8")

    cap_match = re.search(r"^##\s+Cap[ií]tulo\s+(\d+)", texto, re.MULTILINE)
    if not cap_match:
        return None

    cap_num = int(cap_match.group(1))
    secoes = set()

    for m in re.finditer(r"^#{2,4}\s+(\d+(?:\.\d+)+)", texto, re.MULTILINE):
        secoes.add(m.group(1))

    return {"cap": cap_num, "secoes": secoes, "arquivo": filepath.name}


def construir_mapa(rascunhos_dir: Path) -> dict:
    """Constrói mapa global: caps existentes + todas as seções."""
    mapa = {}  # cap_num -> {"secoes": set, "arquivo": str}

    for f in sorted(rascunhos_dir.glob("cap_*_rascunho.md")):
        info = extrair_headings(f)
        if info:
            mapa[info["cap"]] = {
                "secoes": info["secoes"],
                "arquivo": info["arquivo"],
            }

    return mapa

# ── Extração de referências cruzadas ──────────────────────────────────

REF_PATTERNS = [
    # "v. Cap. 10, seção 10.8.2" / "v. Cap. 10, secao 10.8.2"
    re.compile(
        r"v\.\s*Cap\.?\s*(\d+)\s*,\s*se[çc][ãa]o\s*(\d+(?:\.\d+)+)",
        re.IGNORECASE,
    ),
    # "Capítulo 10 (seção 10.8.2)" / "Capítulo 10, seção 10.8.2"
    re.compile(
        r"Cap[ií]tulo\s+(\d+)\s*[,(]\s*se[çc][ãa]o\s*(\d+(?:\.\d+)+)",
        re.IGNORECASE,
    ),
    # "v. seção 10.8.2" (sem menção explícita ao capítulo)
    re.compile(
        r"v\.\s*se[çc][ãa]o\s*(\d+(?:\.\d+)+)",
        re.IGNORECASE,
    ),
    # "seção 10.8.2" standalone (quando seguida de contexto de referência)
    re.compile(
        r"(?:conforme|tratad[oa]|analisad[oa]|examinad[oa]|objeto d[oa]|detalhad[oa])\s+(?:n[oa]\s+)?se[çc][ãa]o\s*(\d+(?:\.\d+)+)",
        re.IGNORECASE,
    ),
    # "v. Cap. 10" (sem seção)
    re.compile(
        r"v\.\s*Cap\.?\s*(\d+)(?!\s*[,\(]\s*se[çc])",
        re.IGNORECASE,
    ),
    # "Capítulo 10" em contexto de referência cruzada
    re.compile(
        r"(?:conforme|tratad[oa]|analisad[oa]|examinad[oa]|objeto d[oa]|detalhad[oa]|v(?:er|ide)?\.?\s+)(?:\s+n[oa]\s+)?Cap[ií]tulo\s+(\d+)(?!\s*[—\-])",
        re.IGNORECASE,
    ),
]


def extrair_refs(filepath: Path, cap_origem: int) -> list:
    """Extrai referências cruzadas de um arquivo. Retorna lista de dicts."""
    texto = filepath.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    refs = []

    for line_num, linha in enumerate(linhas, 1):
        # Pular headings do próprio capítulo e linhas de YAML/metadados
        if linha.startswith("#") or linha.startswith("---") or linha.startswith("tags:"):
            continue

        # Padrões com capítulo + seção
        for m in REF_PATTERNS[0].finditer(linha):
            refs.append({
                "linha": line_num,
                "cap_ref": int(m.group(1)),
                "secao_ref": m.group(2),
                "texto": m.group(0).strip(),
                "cap_origem": cap_origem,
                "arquivo": filepath.name,
            })

        for m in REF_PATTERNS[1].finditer(linha):
            refs.append({
                "linha": line_num,
                "cap_ref": int(m.group(1)),
                "secao_ref": m.group(2),
                "texto": m.group(0).strip(),
                "cap_origem": cap_origem,
                "arquivo": filepath.name,
            })

        # "v. seção X.Y" — capítulo inferido do prefixo numérico
        for m in REF_PATTERNS[2].finditer(linha):
            secao = m.group(1)
            cap_inferido = int(secao.split(".")[0])
            refs.append({
                "linha": line_num,
                "cap_ref": cap_inferido,
                "secao_ref": secao,
                "texto": m.group(0).strip(),
                "cap_origem": cap_origem,
                "arquivo": filepath.name,
            })

        # "conforme/tratado na seção X.Y"
        for m in REF_PATTERNS[3].finditer(linha):
            secao = m.group(1)
            cap_inferido = int(secao.split(".")[0])
            refs.append({
                "linha": line_num,
                "cap_ref": cap_inferido,
                "secao_ref": secao,
                "texto": m.group(0).strip(),
                "cap_origem": cap_origem,
                "arquivo": filepath.name,
            })

        # "v. Cap. X" (só capítulo)
        for m in REF_PATTERNS[4].finditer(linha):
            refs.append({
                "linha": line_num,
                "cap_ref": int(m.group(1)),
                "secao_ref": None,
                "texto": m.group(0).strip(),
                "cap_origem": cap_origem,
                "arquivo": filepath.name,
            })

        # "conforme/tratado no Capítulo X"
        for m in REF_PATTERNS[5].finditer(linha):
            cap = int(m.group(1))
            if cap != cap_origem:
                refs.append({
                    "linha": line_num,
                    "cap_ref": cap,
                    "secao_ref": None,
                    "texto": m.group(0).strip(),
                    "cap_origem": cap_origem,
                    "arquivo": filepath.name,
                })

    return refs


# ── Validação ─────────────────────────────────────────────────────────

def validar_refs(refs: list, mapa: dict) -> list:
    """Valida cada referência contra o mapa de headings. Retorna erros."""
    erros = []

    for ref in refs:
        cap = ref["cap_ref"]
        secao = ref["secao_ref"]

        if cap not in mapa:
            erros.append({
                **ref,
                "tipo": "CAP_INEXISTENTE",
                "detalhe": f"Capítulo {cap} não encontrado nos 23 MDs",
            })
            continue

        if secao:
            if secao not in mapa[cap]["secoes"]:
                # Verificar se é seção do próprio capítulo de origem
                if ref["cap_origem"] in mapa and secao in mapa[ref["cap_origem"]]["secoes"]:
                    erros.append({
                        **ref,
                        "tipo": "CAP_ERRADO",
                        "detalhe": f"Seção {secao} existe no Cap. {ref['cap_origem']} (origem), não no Cap. {cap} referenciado",
                    })
                else:
                    # Procurar em qual capítulo a seção existe
                    encontrada_em = None
                    for c, info in mapa.items():
                        if secao in info["secoes"]:
                            encontrada_em = c
                            break

                    if encontrada_em:
                        erros.append({
                            **ref,
                            "tipo": "SECAO_CAP_ERRADO",
                            "detalhe": f"Seção {secao} existe no Cap. {encontrada_em}, não no Cap. {cap}",
                        })
                    else:
                        erros.append({
                            **ref,
                            "tipo": "SECAO_INEXISTENTE",
                            "detalhe": f"Seção {secao} não encontrada em nenhum capítulo",
                        })

    return erros


# ── Main ──────────────────────────────────────────────────────────────

def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print("VALIDAÇÃO DE REFERÊNCIAS CRUZADAS INTERNAS")
    print("=" * 70)

    mapa = construir_mapa(RASCUNHOS_DIR)
    print(f"\nCapítulos encontrados: {len(mapa)}")

    total_secoes = sum(len(v["secoes"]) for v in mapa.values())
    print(f"Seções mapeadas: {total_secoes}")

    todas_refs = []
    for f in sorted(RASCUNHOS_DIR.glob("cap_*_rascunho.md")):
        info = extrair_headings(f)
        if info:
            refs = extrair_refs(f, info["cap"])
            todas_refs.extend(refs)

    print(f"Referências cruzadas encontradas: {len(todas_refs)}")

    erros = validar_refs(todas_refs, mapa)

    print(f"\n{'=' * 70}")
    if not erros:
        print("RESULTADO: Todas as referências cruzadas são válidas!")
        print("=" * 70)
    else:
        print(f"ERROS ENCONTRADOS: {len(erros)}")
        print("=" * 70)

        # Agrupar por tipo
        por_tipo = defaultdict(list)
        for e in erros:
            por_tipo[e["tipo"]].append(e)

        for tipo, lista in sorted(por_tipo.items()):
            print(f"\n--- {tipo} ({len(lista)} ocorrências) ---\n")
            for e in sorted(lista, key=lambda x: (x["cap_origem"], x["linha"])):
                print(f"  Cap. {e['cap_origem']:02d} (linha {e['linha']:4d}): {e['texto']}")
                print(f"    → {e['detalhe']}")

    # Estatísticas
    print(f"\n{'=' * 70}")
    print("ESTATÍSTICAS DE REFERÊNCIAS CRUZADAS")
    print("=" * 70)

    refs_por_cap = defaultdict(int)
    refs_recebidas = defaultdict(int)
    for r in todas_refs:
        refs_por_cap[r["cap_origem"]] += 1
        refs_recebidas[r["cap_ref"]] += 1

    print(f"\n{'Cap':>5} {'Faz refs':>10} {'Recebe refs':>12}")
    print("-" * 30)
    for cap in sorted(mapa.keys()):
        print(f"  {cap:02d}   {refs_por_cap.get(cap, 0):>8}   {refs_recebidas.get(cap, 0):>10}")

    # Salvar relatório
    relatorio = RASCUNHOS_DIR.parent / "relatorio_refs_cruzadas.txt"
    with open(relatorio, "w", encoding="utf-8") as f:
        f.write(f"Referências cruzadas: {len(todas_refs)}\n")
        f.write(f"Erros: {len(erros)}\n\n")
        for e in erros:
            f.write(f"Cap. {e['cap_origem']:02d} (linha {e['linha']}): {e['texto']}\n")
            f.write(f"  Tipo: {e['tipo']}\n")
            f.write(f"  Detalhe: {e['detalhe']}\n\n")

    print(f"\nRelatório salvo em: {relatorio}")

    return len(erros)


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
