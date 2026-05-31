#!/usr/bin/env python3
"""
ingest_espelhos.py — Indexa os espelhos de acórdãos do STJ (jurisprudencia/stj/
espelhos-de-acordaos-*) num SQLite consultável por classe + número de processo.

Saída: jurisprudencia/stj/espelhos.sqlite  (tabela acordaos + índice e FTS na ementa)
"""
import os, re, json, glob, sqlite3

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "jurisprudencia", "stj")
DB = os.path.join(ROOT, "espelhos.sqlite")

dig = lambda s: re.sub(r"\D", "", str(s or ""))


def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE acordaos(
        classe TEXT, numero TEXT, registro TEXT, orgao TEXT, relator TEXT,
        data_decisao TEXT, data_pub TEXT, ementa TEXT, tese TEXT, tema TEXT,
        fonte TEXT)""")

    arquivos = []
    for sub in sorted(glob.glob(os.path.join(ROOT, "espelhos-de-acordaos-*"))):
        arquivos += glob.glob(os.path.join(sub, "*.json"))
    print(f"JSONs de espelhos: {len(arquivos)}")

    total, classes, datas = 0, {}, []
    for fp in arquivos:
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                data = json.load(f)
        except Exception as e:
            print("  erro lendo", os.path.basename(fp), e); continue
        if not isinstance(data, list):
            continue
        rows = []
        for r in data:
            if not isinstance(r, dict):
                continue
            classe = (r.get("siglaClasse") or "").strip()
            num = dig(r.get("numeroProcesso"))
            classes[classe] = classes.get(classe, 0) + 1
            dd = (r.get("dataDecisao") or "")
            if dd:
                datas.append(dd)
            rows.append((classe, num, dig(r.get("numeroRegistro")),
                         (r.get("nomeOrgaoJulgador") or "").strip(),
                         (r.get("ministroRelator") or "").strip(),
                         dd, (r.get("dataPublicacao") or "").strip(),
                         r.get("ementa") or "", r.get("teseJuridica") or "",
                         str(r.get("tema") or ""), os.path.basename(os.path.dirname(fp))))
        con.executemany("INSERT INTO acordaos VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
        total += len(rows)
    con.commit()

    con.execute("CREATE INDEX idx_classe_num ON acordaos(classe, numero)")
    con.execute("CREATE INDEX idx_num ON acordaos(numero)")
    # FTS5 na ementa (busca textual)
    try:
        con.execute("CREATE VIRTUAL TABLE ementa_fts USING fts5(ementa, content='acordaos', content_rowid='rowid')")
        con.execute("INSERT INTO ementa_fts(rowid, ementa) SELECT rowid, ementa FROM acordaos")
    except Exception as e:
        print("  (FTS indisponível:", e, ")")
    con.commit()

    datas = [d for d in datas if d.isdigit() and len(d) == 8]
    print(f"\nRegistros indexados: {total}")
    print(f"Processos REsp distintos: ", con.execute(
        "SELECT COUNT(DISTINCT numero) FROM acordaos WHERE classe='REsp'").fetchone()[0])
    if datas:
        print(f"Faixa dataDecisao: {min(datas)} a {max(datas)}")
    print("Classes mais frequentes:")
    for c, n in sorted(classes.items(), key=lambda x: -x[1])[:12]:
        print(f"  {c or '(vazio)'}: {n}")
    print(f"\nDB: {DB} ({os.path.getsize(DB)/1e6:.0f} MB)")
    con.close()


if __name__ == "__main__":
    main()
