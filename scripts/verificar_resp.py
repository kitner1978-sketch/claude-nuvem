#!/usr/bin/env python3
"""
verificar_resp.py — Verifica citacoes AVULSAS de REsp/AREsp/EREsp do livro
(as que nao sao leading case de Tema) contra o corpus de espelhos de acordaos
do STJ (jurisprudencia/stj/espelhos.sqlite), trazendo a ementa oficial.

Pre-requisito: rodar ingest_espelhos.py para construir o SQLite.
Saida: output/verif_resp_avulsos.md
"""
import os, re, csv, sqlite3, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPS = os.path.join(ROOT, "output", "rascunhos")
DB = os.path.join(ROOT, "jurisprudencia", "stj", "espelhos.sqlite")
PROCS = os.path.join(ROOT, "jurisprudencia", "stj", "precedentes", "processos.csv")
OUT = os.path.join(ROOT, "output", "verif_resp_avulsos.md")

dig = lambda s: re.sub(r"\D", "", str(s or ""))
RX = re.compile(r'\b(REsp|AREsp|EREsp)\b[^\d]{0,6}(\d[\d.]{4,})', re.I)


def main():
    if not os.path.exists(DB):
        print("ERRO: espelhos.sqlite ausente — rode ingest_espelhos.py primeiro.")
        return
    con = sqlite3.connect(DB)

    tema_procs = {}
    with open(PROCS, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            n = dig(r.get("Processo"))
            if n:
                tema_procs[n] = f"{r.get('tipoPrecedente')} {r.get('numeroPrecedente')}"

    cites = {}
    for fn in sorted(glob.glob(os.path.join(CAPS, "cap_*_rascunho.md"))):
        cap = re.search(r"cap_(\d+)_", fn).group(1)
        txt = open(fn, encoding="utf-8", errors="replace").read()
        for m in RX.finditer(txt):
            num = dig(m.group(2))
            if len(num) >= 5:
                cites.setdefault(num, set()).add(cap)

    avulsos, por_tema, nao_loc = [], 0, []
    for num, caps in sorted(cites.items()):
        if num in tema_procs:
            por_tema += 1
            continue
        row = con.execute(
            "SELECT classe,orgao,relator,data_decisao,ementa FROM acordaos "
            "WHERE numero=? ORDER BY data_decisao DESC LIMIT 1", (num,)).fetchone()
        if row:
            avulsos.append((num, sorted(caps), row))
        else:
            nao_loc.append((num, sorted(caps)))

    L = ["# Verificação de REsp avulsos contra o corpus de ementas do STJ\n"]
    L.append(f"> Corpus: espelhos de acórdãos (jurisprudencia/stj/espelhos.sqlite).\n")
    L.append(f"- Citações REsp/AREsp/EREsp distintas: {len(cites)}")
    L.append(f"- Já cobertas por Tema (verificadas na varredura): {por_tema}")
    L.append(f"- Avulsas com ementa no corpus: {len(avulsos)}")
    L.append(f"- Não localizadas (corpus amostral — conferência manual): {len(nao_loc)}\n")

    L.append("## Avulsas confirmadas (ementa oficial para conferência)\n")
    for num, caps, (cl, org, rel, dd, em) in avulsos:
        d = f"{dd[6:8]}/{dd[4:6]}/{dd[:4]}" if len(dd) == 8 else dd
        L.append(f"### {cl} {num} — caps. {', '.join(caps)}")
        L.append(f"- Órgão: {org} | Relator: {rel} | Decisão: {d}")
        L.append(f"- Ementa: {re.sub(chr(10),' ',em)[:500].strip()}…\n")

    if nao_loc:
        L.append("## Não localizadas no corpus (conferir manualmente)\n")
        for num, caps in nao_loc:
            L.append(f"- {num} — caps. {', '.join(caps)}")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(f"Relatório: {OUT}")
    print(f"  {len(cites)} REsp citados | {por_tema} via Tema | "
          f"{len(avulsos)} avulsos confirmados | {len(nao_loc)} nao localizados")
    con.close()


if __name__ == "__main__":
    main()
