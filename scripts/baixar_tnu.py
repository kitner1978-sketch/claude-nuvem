#!/usr/bin/env python3
"""
baixar_tnu.py — Raspa os Temas Representativos da TNU (CJF) para uma tabela
estruturada em jurisprudencia/tnu/.

A página do CJF é renderizada no servidor (Plone), sem WAF; cada tema é uma
<table class="auto-table tablesorter tg"> com células rotuladas (fundo_azul =
rótulo, célula seguinte = valor). Paginamos via ?b_size/b_start.

Saída: jurisprudencia/tnu/temas_representativos_tnu.csv (+ .json)
"""
import os, re, csv, json, time, html as ihtml
from urllib.request import urlopen, Request

BASE = ("https://www.cjf.jus.br/cjf/corregedoria-da-justica-federal/"
        "turma-nacional-de-uniformizacao/temas-representativos")
UA = "Mozilla/5.0 (Projeto Livro - verificacao de jurisprudencia)"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "jurisprudencia", "tnu")

CAMPOS = ["Tema", "Situação do tema", "Ramo do direito",
          "Questão submetida a julgamento", "Tese firmada", "Processo"]

RX_TABLE = re.compile(r'<table[^>]*class="[^"]*auto-table[^"]*"[^>]*>(.*?)</table>', re.S | re.I)
RX_CELL = re.compile(r'<(th|td)([^>]*)>(.*?)</\1>', re.S | re.I)


def limpa(frag):
    frag = re.sub(r"<[^>]+>", " ", frag)
    frag = ihtml.unescape(frag).replace("\xa0", " ")
    return re.sub(r"\s+", " ", frag).strip()


def parse_tema(tbl_html):
    fields, cur = {}, None
    for tag, attrs, inner in RX_CELL.findall(tbl_html):
        txt = limpa(inner)
        if "fundo_azul" in attrs:          # célula-rótulo
            cur = txt
            fields.setdefault(cur, "")
        elif cur is not None and txt:      # célula-valor
            fields[cur] = (fields[cur] + " " + txt).strip()
    return fields


def fetch_page(b_start, b_size=100):
    url = f"{BASE}?b_size:int={b_size}&b_start:int={b_start}"
    req = Request(url, headers={"User-Agent": UA})
    return urlopen(req, timeout=60).read().decode("utf-8", "replace")


def run():
    os.makedirs(OUT, exist_ok=True)
    vistos, registros = set(), []
    for b_start in range(0, 1000, 100):
        html = fetch_page(b_start)
        tabelas = RX_TABLE.findall(html)
        novos = 0
        for t in tabelas:
            f = parse_tema(t)
            num = re.sub(r"\D", "", f.get("Tema", ""))
            if not num or num in vistos:
                continue
            vistos.add(num)
            novos += 1
            registros.append(f)
        print(f"  b_start={b_start}: {len(tabelas)} tabelas, {novos} temas novos "
              f"(total {len(registros)})", flush=True)
        if novos == 0:
            break
        time.sleep(1)

    registros.sort(key=lambda r: int(re.sub(r"\D", "", r.get("Tema", "0")) or 0))

    # CSV (colunas principais) + extras
    extras = sorted({k for r in registros for k in r} - set(CAMPOS))
    csv_path = os.path.join(OUT, "temas_representativos_tnu.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["numero", "situacao", "ramo", "questao", "tese", "processo"] + extras)
        for r in registros:
            w.writerow([
                re.sub(r"\D", "", r.get("Tema", "")),
                r.get("Situação do tema", ""), r.get("Ramo do direito", ""),
                r.get("Questão submetida a julgamento", ""),
                r.get("Tese firmada", ""), r.get("Processo", ""),
            ] + [r.get(k, "") for k in extras])

    with open(os.path.join(OUT, "temas_representativos_tnu.json"), "w", encoding="utf-8") as fp:
        json.dump(registros, fp, ensure_ascii=False, indent=1)

    prev = sum(1 for r in registros if "PREVIDENC" in r.get("Ramo do direito", "").upper())
    com_tese = sum(1 for r in registros if r.get("Tese firmada", "").strip() not in ("", "-"))
    print(f"\n=== TNU: {len(registros)} temas salvos | com tese: {com_tese} | "
          f"previdenciários: {prev} ===")
    print("Campos extras capturados:", extras)
    print("CSV:", csv_path)


if __name__ == "__main__":
    run()
