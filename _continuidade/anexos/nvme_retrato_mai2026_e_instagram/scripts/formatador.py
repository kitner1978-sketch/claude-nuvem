"""
Agente Formatador — Pós-processamento determinístico (sem LLM).
Padroniza referências, boxes e bibliografia ABNT.
"""

import re
import json
from datetime import datetime
from pathlib import Path


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 1 — Padronização de referências legislativas
# ═══════════════════════════════════════════════════════

LEIS_CONHECIDAS = {
    r"Lei\s+n[ºo°]?\s*8\.?213,?\s+de\s+24\s+de\s+julho\s+de\s+1991": "Lei 8.213/91",
    r"Lei\s+n[ºo°]?\s*8\.?212,?\s+de\s+24\s+de\s+julho\s+de\s+1991": "Lei 8.212/91",
    r"Lei\s+n[ºo°]?\s*8\.?742,?\s+de\s+7\s+de\s+dezembro\s+de\s+1993": "Lei 8.742/93",
    r"Decreto\s+n[ºo°]?\s*3\.?048,?\s+de\s+6\s+de\s+maio\s+de\s+1999": "Decreto 3.048/99",
    r"Emenda\s+Constitucional\s+n[ºo°]?\s*103,?\s+de\s+12\s+de\s+novembro\s+de\s+2019": "EC 103/2019",
    r"Emenda\s+Constitucional\s+n[ºo°]?\s*20,?\s+de\s+15\s+de\s+dezembro\s+de\s+1998": "EC 20/1998",
    r"Emenda\s+Constitucional\s+n[ºo°]?\s*41,?\s+de\s+19\s+de\s+dezembro\s+de\s+2003": "EC 41/2003",
    r"Emenda\s+Constitucional\s+n[ºo°]?\s*47,?\s+de\s+5\s+de\s+julho\s+de\s+2005": "EC 47/2005",
}


def padronizar_referencias_legislativas(texto: str) -> str:
    ja_mencionadas = set()

    def substituir_se_repetido(match, forma_abreviada):
        chave = forma_abreviada.lower()
        if chave not in ja_mencionadas:
            ja_mencionadas.add(chave)
            return match.group(0)
        return forma_abreviada

    for padrao, abreviada in LEIS_CONHECIDAS.items():
        ocorrencias = list(re.finditer(padrao, texto, re.IGNORECASE))
        if len(ocorrencias) > 1:
            for oc in reversed(ocorrencias[1:]):
                texto = texto[:oc.start()] + abreviada + texto[oc.end():]
            ja_mencionadas.add(abreviada.lower())

    return texto


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 2 — Padronização de jurisprudência
# ═══════════════════════════════════════════════════════

def padronizar_jurisprudencia(texto: str) -> str:
    texto = re.sub(
        r"Tema\s+(?:Repetitivo\s+)?n[ºo°]?\s*(\d+)",
        r"Tema Repetitivo \1",
        texto
    )

    texto = re.sub(
        r"Súmula\s+n[ºo°]?\s*(\d+)",
        r"Súmula \1",
        texto
    )

    texto = re.sub(
        r"rel\.\s*Ministro\s",
        "rel. Min. ",
        texto
    )
    texto = re.sub(
        r"rel\.\s*Ministra\s",
        "rel. Min. ",
        texto
    )

    return texto


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 3 — Numeração de seções
# ═══════════════════════════════════════════════════════

SECOES_PROTEGIDAS = {"Referências", "REFERÊNCIAS", "Referências Bibliográficas"}

def numerar_secoes(texto: str, numero_capitulo: int) -> str:
    contador_secao = 0
    contador_subsecao = 0
    linhas = texto.split("\n")
    resultado = []

    for linha in linhas:
        if linha.startswith("#### "):
            contador_subsecao += 1
            titulo = linha[5:].strip()
            resultado.append(
                f"#### {numero_capitulo}.{contador_secao}.{contador_subsecao} {titulo}"
            )
        elif linha.startswith("### "):
            contador_secao += 1
            contador_subsecao = 0
            titulo = linha[4:].strip()
            resultado.append(
                f"### {numero_capitulo}.{contador_secao} {titulo}"
            )
        elif linha.startswith("## "):
            titulo = linha[3:].strip()
            if titulo in SECOES_PROTEGIDAS:
                resultado.append(linha)
            else:
                resultado.append(f"## Capítulo {numero_capitulo} — {titulo}")
        else:
            resultado.append(linha)

    return "\n".join(resultado)


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 4 — Verificação de boxes
# ═══════════════════════════════════════════════════════

def verificar_boxes(texto: str) -> dict:
    tipos = {
        "box-pratica": 0,
        "box-atencao": 0,
        "box-jurisprudencia": 0,
    }

    for tipo in tipos:
        tipos[tipo] = len(re.findall(rf":::\s*{tipo}", texto))

    aberturas = len(re.findall(r":::\s*box-\w+", texto))
    fechamentos = len(re.findall(r"^:::\s*$", texto, re.MULTILINE))

    alertas = []
    if aberturas != fechamentos:
        alertas.append(
            f"ALERTA: {aberturas} boxes abertos mas {fechamentos} fechamentos encontrados."
        )

    if tipos["box-pratica"] < 2:
        alertas.append(
            f"ALERTA: Apenas {tipos['box-pratica']} box(es) 'Na Prática' "
            f"(mínimo recomendado: 2)."
        )

    return {"contagem": tipos, "alertas": alertas}


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 5 — Bibliografia ABNT
# ═══════════════════════════════════════════════════════

def validar_bibliografia(texto: str) -> list:
    alertas = []

    if "## Referências" not in texto and "## REFERÊNCIAS" not in texto:
        alertas.append("ALERTA: Seção de Referências Bibliográficas não encontrada.")

    refs_no_texto = set(re.findall(r"\(([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ]+),\s*(\d{4})\)", texto))
    secao_refs = texto.split("## Referências")[-1] if "## Referências" in texto else ""

    for sobrenome, ano in refs_no_texto:
        if sobrenome.upper() not in secao_refs.upper():
            alertas.append(
                f"ALERTA: Referência ({sobrenome}, {ano}) citada no texto "
                f"mas não encontrada na bibliografia."
            )

    return alertas


# ═══════════════════════════════════════════════════════
# TRANSFORMAÇÃO 6 — Limpeza
# ═══════════════════════════════════════════════════════

def limpar_texto(texto: str) -> str:
    texto = re.sub(r"\[DADO_INSUFICIENTE:\s*[^\]]*\]", "", texto)

    texto = texto.replace('“', '"').replace('”', '"')

    texto = texto.replace(" - ", " — ")
    texto = texto.replace(" -- ", " — ")

    texto = re.sub(r"  +", " ", texto)

    texto = re.sub(r"\n{4,}", "\n\n\n", texto)

    return texto.strip()


# ═══════════════════════════════════════════════════════
# PIPELINE COMPLETO DO FORMATADOR
# ═══════════════════════════════════════════════════════

def formatar_capitulo(texto: str, numero_capitulo: int) -> dict:
    alertas = []

    texto = padronizar_referencias_legislativas(texto)
    texto = padronizar_jurisprudencia(texto)
    texto = numerar_secoes(texto, numero_capitulo)

    resultado_boxes = verificar_boxes(texto)
    alertas.extend(resultado_boxes["alertas"])

    alertas_bib = validar_bibliografia(texto)
    alertas.extend(alertas_bib)

    texto = limpar_texto(texto)

    palavras = len(texto.split())
    flags = re.findall(r"\[REVISAR_HUMANO:\s*([^\]]*)\]", texto)

    return {
        "texto_formatado": texto,
        "palavras": palavras,
        "boxes": resultado_boxes["contagem"],
        "flags_revisao": flags,
        "alertas_formatador": alertas,
        "formatado_em": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════
# EXECUÇÃO VIA CLI
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python formatador.py <arquivo.md> <numero_capitulo>")
        sys.exit(1)

    arquivo = Path(sys.argv[1])
    num_cap = int(sys.argv[2])

    if not arquivo.exists():
        print(f"Erro: arquivo {arquivo} nao encontrado.")
        sys.exit(1)

    texto = arquivo.read_text(encoding="utf-8")
    resultado = formatar_capitulo(texto, num_cap)

    saida = arquivo.with_suffix(".formatado.md")
    saida.write_text(resultado["texto_formatado"], encoding="utf-8")

    meta = arquivo.with_suffix(".formato_meta.json")
    meta_data = {k: v for k, v in resultado.items() if k != "texto_formatado"}
    meta.write_text(json.dumps(meta_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Formatado: {saida}")
    print(f"  Palavras: {resultado['palavras']}")
    print(f"  Boxes: {resultado['boxes']}")
    print(f"  Flags revisao: {len(resultado['flags_revisao'])}")
    if resultado["alertas_formatador"]:
        print(f"  Alertas:")
        for a in resultado["alertas_formatador"]:
            print(f"    - {a}")
