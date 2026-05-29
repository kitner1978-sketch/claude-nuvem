#!/usr/bin/env python3
"""
Conferência de valores monetários e índices no livro.

Extrai todas as ocorrências de R$, SM, teto, SELIC etc. dos 23 MDs.
Compara com tabela de referência atualizada e sinaliza divergências.
Distingue valores correntes (que devem estar atualizados) de valores
históricos e exemplos hipotéticos.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

RASCUNHOS_DIR = Path(r"D:\Projeto Livro\output\rascunhos")

# ── Valores de referência (2026) ──────────────────────────────────────

VALORES_REF = {
    "SM": {
        "valor": "1.621,00",
        "valor_num": 1621.00,
        "label": "Salário Mínimo",
        "ano": 2026,
    },
    "TETO": {
        "valor": "8.475,55",
        "valor_num": 8475.55,
        "label": "Teto do RGPS",
        "ano": 2026,
    },
    "SELIC": {
        "valor": "14,50",
        "valor_num": 14.50,
        "label": "Taxa SELIC (a.a.)",
        "ano": 2026,
    },
}

# Valores históricos conhecidos (não devem gerar alerta)
VALORES_HISTORICOS = {
    # SM históricos
    "1.412,00",  # SM 2024
    "1.320,00",  # SM 2023
    "1.518,00",  # SM 2025
    "1.212,00",  # SM 2022
    "1.100,00",  # SM 2021
    "1.045,00",  # SM 2020
    # Tetos históricos
    "7.786,02",  # Teto 2024
    "7.507,49",  # Teto 2023
    "8.157,41",  # Teto 2025
    "2.400,00",  # Teto 2004 (mencionado no cap 17)
    # Valores claramente de exemplo
}


def parse_valor_br(s: str) -> float:
    """Converte '1.621,00' para 1621.00."""
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


# ── Extração ──────────────────────────────────────────────────────────

def extrair_valores_monetarios(filepath: Path) -> list:
    """Extrai todas as ocorrências de R$ valor do arquivo."""
    texto = filepath.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    achados = []

    for line_num, linha in enumerate(linhas, 1):
        # Pular headings, YAML, referências
        if linha.startswith("#") or linha.startswith("---") or linha.startswith("tags:"):
            continue

        # R$ X.XXX,XX
        for m in re.finditer(r"R\$\s*([\d.]+,\d{2})", linha):
            valor_str = m.group(1)
            valor_num = parse_valor_br(valor_str)
            achados.append({
                "linha": line_num,
                "valor_str": valor_str,
                "valor_num": valor_num,
                "contexto": linha.strip()[:120],
                "arquivo": filepath.name,
                "tipo": "R$",
            })

    return achados


def extrair_mencoes_indices(filepath: Path) -> list:
    """Extrai menções a SM, teto, SELIC com valores associados."""
    texto = filepath.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    achados = []

    for line_num, linha in enumerate(linhas, 1):
        if linha.startswith("#") or linha.startswith("---"):
            continue

        # "salário mínimo" / "SM" seguido de valor
        for m in re.finditer(
            r"(?:sal[aá]rio[\s-]m[ií]nimo|SM)\s*(?:de|=|:|\()\s*R\$\s*([\d.]+,\d{2})",
            linha,
            re.IGNORECASE,
        ):
            achados.append({
                "linha": line_num,
                "indice": "SM",
                "valor_str": m.group(1),
                "valor_num": parse_valor_br(m.group(1)),
                "contexto": linha.strip()[:120],
                "arquivo": filepath.name,
            })

        # "teto" seguido de valor
        for m in re.finditer(
            r"teto\s*(?:do RGPS|previdenci[aá]rio|de contribui[çc][ãa]o)?\s*(?:de|=|:|\(|,\s*(?:atualmente|em \d{4}),?\s*)\s*R\$\s*([\d.]+,\d{2})",
            linha,
            re.IGNORECASE,
        ):
            achados.append({
                "linha": line_num,
                "indice": "TETO",
                "valor_str": m.group(1),
                "valor_num": parse_valor_br(m.group(1)),
                "contexto": linha.strip()[:120],
                "arquivo": filepath.name,
            })

        # SELIC percentual
        for m in re.finditer(
            r"SELIC\s*(?:de|=|:|\(|,\s*atualmente\s*)?\s*([\d]+[,.][\d]+)\s*%",
            linha,
            re.IGNORECASE,
        ):
            achados.append({
                "linha": line_num,
                "indice": "SELIC",
                "valor_str": m.group(1),
                "valor_num": float(m.group(1).replace(",", ".")),
                "contexto": linha.strip()[:120],
                "arquivo": filepath.name,
            })

    return achados


# ── Classificação ─────────────────────────────────────────────────────

def eh_contexto_historico(contexto: str) -> bool:
    """Heurística para detectar se o valor está em contexto histórico."""
    indicadores = [
        r"em \d{4}",
        r"à época",
        r"na época",
        r"naquele per[ií]odo",
        r"historicamente",
        r"anterior",
        r"originalmente",
        r"Lei Eloy Chaves",
        r"Lei n[º°]\. \d",
        r"Decreto n",
        r"EC \d+/\d{4}",
        r"Portaria.*\d{4}",
        r"antes d[ae]",
        r"vigor em",
        r"fixou.* em R\$",
    ]
    for pat in indicadores:
        if re.search(pat, contexto, re.IGNORECASE):
            return True
    return False


def eh_exemplo_calculo(contexto: str) -> bool:
    """Heurística para detectar exemplos de cálculo."""
    indicadores = [
        r"exemplo",
        r"supon(ha|do)",
        r"hipot[eé]tic",
        r"imaginemos",
        r"considere",
        r"resultado",
        r"RMI.*=",
        r"×|x\s*\d+%",
        r"[Mm][eé]dia.*=",
        r"\d+%\s*=",
        r"[Cc]aso \d",
        r"Pedro|Maria|Jo[ãa]o|Ana|Carlos",
    ]
    for pat in indicadores:
        if re.search(pat, contexto, re.IGNORECASE):
            return True
    return False


# ── Análise ───────────────────────────────────────────────────────────

def analisar_valores(todos_valores: list) -> dict:
    """Analisa valores e classifica em: corrente, histórico, exemplo, suspeito."""
    resultado = {
        "corrente_ok": [],       # Valor corrente e correto
        "historico": [],         # Valor em contexto histórico
        "exemplo": [],           # Valor em exemplo de cálculo
        "possivelmente_desatualizado": [],  # Valor que parece corrente mas diverge
        "sm_encontrados": set(),
        "teto_encontrados": set(),
    }

    for v in todos_valores:
        valor = v["valor_str"]
        contexto = v["contexto"]

        # Checar se é valor de referência atual
        is_sm = abs(v["valor_num"] - VALORES_REF["SM"]["valor_num"]) < 0.01
        is_teto = abs(v["valor_num"] - VALORES_REF["TETO"]["valor_num"]) < 0.01

        if is_sm:
            resultado["sm_encontrados"].add(f"{v['arquivo']}:{v['linha']}")
            resultado["corrente_ok"].append(v)
            continue

        if is_teto:
            resultado["teto_encontrados"].add(f"{v['arquivo']}:{v['linha']}")
            resultado["corrente_ok"].append(v)
            continue

        if valor in VALORES_HISTORICOS:
            resultado["historico"].append(v)
            continue

        if eh_contexto_historico(contexto):
            resultado["historico"].append(v)
            continue

        if eh_exemplo_calculo(contexto):
            resultado["exemplo"].append(v)
            continue

        # Checar se é valor "quase" SM ou teto (desatualizado?)
        for ref_key, ref in VALORES_REF.items():
            if ref_key == "SELIC":
                continue
            tolerancia_pct = 0.15  # 15% de diferença
            if abs(v["valor_num"] - ref["valor_num"]) / ref["valor_num"] < tolerancia_pct:
                if v["valor_str"] != ref["valor"]:
                    resultado["possivelmente_desatualizado"].append({
                        **v,
                        "ref_esperada": ref["valor"],
                        "ref_label": ref["label"],
                    })

    return resultado


def analisar_indices(todos_indices: list) -> list:
    """Verifica se menções explícitas a SM/Teto/SELIC usam valor correto."""
    alertas = []

    for idx in todos_indices:
        ref = VALORES_REF.get(idx["indice"])
        if not ref:
            continue

        if eh_contexto_historico(idx["contexto"]):
            continue

        valor_esperado = ref["valor_num"]
        if abs(idx["valor_num"] - valor_esperado) > 0.01:
            alertas.append({
                **idx,
                "esperado": ref["valor"],
                "tipo_alerta": "INDICE_DIVERGENTE",
            })

    return alertas


# ── Contagem de ocorrências de 60 SM ─────────────────────────────────

def verificar_60sm(rascunhos_dir: Path) -> list:
    """Verifica se '60 SM' ou '60 salários mínimos' usa o valor correto."""
    alertas = []
    sm_atual = VALORES_REF["SM"]["valor_num"]
    valor_60sm = sm_atual * 60  # R$ 97.260,00

    for f in sorted(rascunhos_dir.glob("cap_*_rascunho.md")):
        texto = f.read_text(encoding="utf-8")
        linhas = texto.splitlines()

        for line_num, linha in enumerate(linhas, 1):
            if re.search(r"60\s*(?:SM|sal[aá]rios?\s*m[ií]nimos?)", linha, re.IGNORECASE):
                # Verificar se há valor R$ na mesma linha
                m_val = re.search(r"R\$\s*([\d.]+,\d{2})", linha)
                if m_val:
                    val = parse_valor_br(m_val.group(1))
                    if abs(val - valor_60sm) > 100 and not eh_contexto_historico(linha):
                        alertas.append({
                            "arquivo": f.name,
                            "linha": line_num,
                            "valor_encontrado": m_val.group(1),
                            "valor_esperado": f"{valor_60sm:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                            "contexto": linha.strip()[:120],
                        })

    return alertas


# ── Main ──────────────────────────────────────────────────────────────

def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print("CONFERÊNCIA DE VALORES MONETÁRIOS E ÍNDICES")
    print("=" * 70)
    print(f"\nValores de referência ({VALORES_REF['SM']['ano']}):")
    for k, v in VALORES_REF.items():
        print(f"  {v['label']}: R$ {v['valor']}" if k != "SELIC" else f"  {v['label']}: {v['valor']}%")

    # Extrair todos os valores
    todos_valores = []
    todos_indices = []
    for f in sorted(RASCUNHOS_DIR.glob("cap_*_rascunho.md")):
        todos_valores.extend(extrair_valores_monetarios(f))
        todos_indices.extend(extrair_mencoes_indices(f))

    print(f"\nValores R$ encontrados: {len(todos_valores)}")
    print(f"Menções a índices (SM/Teto/SELIC): {len(todos_indices)}")

    # Analisar
    resultado = analisar_valores(todos_valores)
    alertas_indices = analisar_indices(todos_indices)
    alertas_60sm = verificar_60sm(RASCUNHOS_DIR)

    # Relatório
    total_alertas = (
        len(resultado["possivelmente_desatualizado"])
        + len(alertas_indices)
        + len(alertas_60sm)
    )

    print(f"\n{'=' * 70}")
    print(f"CLASSIFICAÇÃO DOS VALORES R$")
    print("=" * 70)
    print(f"  Valor corrente (OK):          {len(resultado['corrente_ok'])}")
    print(f"  Contexto histórico:           {len(resultado['historico'])}")
    print(f"  Exemplo de cálculo:           {len(resultado['exemplo'])}")
    print(f"  Possivelmente desatualizado:  {len(resultado['possivelmente_desatualizado'])}")
    print(f"  SM (R$ {VALORES_REF['SM']['valor']}) encontrado em: {len(resultado['sm_encontrados'])} locais")
    print(f"  Teto (R$ {VALORES_REF['TETO']['valor']}) encontrado em: {len(resultado['teto_encontrados'])} locais")

    if resultado["possivelmente_desatualizado"]:
        print(f"\n{'=' * 70}")
        print("VALORES POSSIVELMENTE DESATUALIZADOS")
        print("=" * 70)
        for v in sorted(resultado["possivelmente_desatualizado"], key=lambda x: (x["arquivo"], x["linha"])):
            print(f"\n  {v['arquivo']}:{v['linha']}")
            print(f"    Encontrado: R$ {v['valor_str']}")
            print(f"    Esperado ({v['ref_label']}): R$ {v['ref_esperada']}")
            print(f"    Contexto: {v['contexto']}")

    if alertas_indices:
        print(f"\n{'=' * 70}")
        print("ÍNDICES DIVERGENTES (SM/Teto/SELIC explícitos)")
        print("=" * 70)
        for a in sorted(alertas_indices, key=lambda x: (x["arquivo"], x["linha"])):
            print(f"\n  {a['arquivo']}:{a['linha']}")
            print(f"    Índice: {a['indice']}")
            print(f"    Encontrado: {a['valor_str']}")
            print(f"    Esperado: {a['esperado']}")
            print(f"    Contexto: {a['contexto']}")

    if alertas_60sm:
        print(f"\n{'=' * 70}")
        print("ALERTAS 60 SM (competência JEF)")
        print("=" * 70)
        for a in alertas_60sm:
            print(f"\n  {a['arquivo']}:{a['linha']}")
            print(f"    Valor encontrado: R$ {a['valor_encontrado']}")
            print(f"    60 SM atual: R$ {a['valor_esperado']}")
            print(f"    Contexto: {a['contexto']}")

    if total_alertas == 0:
        print(f"\n{'=' * 70}")
        print("RESULTADO: Nenhum valor possivelmente desatualizado detectado!")
        print("=" * 70)

    # Listar todos os valores "não classificados" (que não são SM, teto, histórico nem exemplo)
    classificados = (
        set(id(v) for v in resultado["corrente_ok"])
        | set(id(v) for v in resultado["historico"])
        | set(id(v) for v in resultado["exemplo"])
    )
    nao_classificados = [v for v in todos_valores if id(v) not in classificados]

    # Salvar relatório completo
    relatorio = RASCUNHOS_DIR.parent / "relatorio_valores.txt"
    with open(relatorio, "w", encoding="utf-8") as f:
        f.write(f"Total de valores R$ encontrados: {len(todos_valores)}\n")
        f.write(f"Alertas: {total_alertas}\n\n")

        f.write("== VALORES NÃO CLASSIFICADOS (revisar manualmente) ==\n\n")
        for v in sorted(nao_classificados, key=lambda x: (x["arquivo"], x["linha"])):
            f.write(f"{v['arquivo']}:{v['linha']}  R$ {v['valor_str']}\n")
            f.write(f"  {v['contexto']}\n\n")

        if alertas_indices:
            f.write("\n== ÍNDICES DIVERGENTES ==\n\n")
            for a in alertas_indices:
                f.write(f"{a['arquivo']}:{a['linha']}  {a['indice']}: {a['valor_str']} (esperado: {a['esperado']})\n")

    print(f"\nRelatório completo salvo em: {relatorio}")
    print(f"  ({len(nao_classificados)} valores não classificados listados para revisão manual)")

    return total_alertas


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
