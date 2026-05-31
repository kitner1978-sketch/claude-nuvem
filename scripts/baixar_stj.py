#!/usr/bin/env python3
"""
baixar_stj.py — Baixa datasets de jurisprudencia do Portal de Dados Abertos do STJ
(https://dadosabertos.web.stj.jus.br) para jurisprudencia/stj/<dataset>/.

Resumivel: pula arquivos ja baixados e usa .part para tolerar interrupcao.

Uso:
  python baixar_stj.py              # tudo (espelhos + integras) ~13 GB
  python baixar_stj.py --so-espelhos   # so os 10 datasets de espelhos (~1 GB)
  python baixar_stj.py <slug> ...   # datasets especificos
"""
import sys, os, json, time, shutil
from urllib.request import urlopen, Request

BASE = "https://dadosabertos.web.stj.jus.br/api/3/action/package_show?id="
UA = "Mozilla/5.0 (Projeto Livro - verificacao de jurisprudencia)"
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "jurisprudencia", "stj")

ESPELHOS = [f"espelhos-de-acordaos-{x}" for x in [
    "corte-especial", "primeira-secao", "segunda-secao", "terceira-secao",
    "primeira-turma", "segunda-turma", "terceira-turma",
    "quarta-turma", "quinta-turma", "sexta-turma"]]
INTEGRAS = ["integras-de-decisoes-terminativas-e-acordaos-do-diario-da-justica"]


def api(slug):
    req = Request(BASE + slug, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as r:
        return json.loads(r.read())["result"]


def safe_name(rid, url):
    base = os.path.basename(url.split("?")[0]) or "arquivo"
    return f"{(rid or 'x')[:8]}__{base}"


def download(url, out, retries=3):
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return "skip", 0
    tmp = out + ".part"
    for att in range(1, retries + 1):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=180) as r, open(tmp, "wb") as f:
                shutil.copyfileobj(r, f, 1024 * 256)
            sz = os.path.getsize(tmp)
            os.replace(tmp, out)
            return "ok", sz
        except Exception as e:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            if att == retries:
                return f"FAIL:{e}", 0
            time.sleep(2 * att)


def run(slugs):
    os.makedirs(ROOT, exist_ok=True)
    ok = skip = fail = 0
    nbytes = 0
    t0 = time.time()
    for slug in slugs:
        try:
            d = api(slug)
        except Exception as e:
            print(f"[{slug}] ERRO package_show: {e}", flush=True)
            continue
        res = d.get("resources", [])
        ddir = os.path.join(ROOT, slug)
        os.makedirs(ddir, exist_ok=True)
        print(f"\n=== {slug}: {len(res)} recursos ===", flush=True)
        for i, x in enumerate(res, 1):
            url = x.get("url")
            if not url:
                continue
            out = os.path.join(ddir, safe_name(x.get("id", ""), url))
            status, sz = download(url, out)
            if status == "ok":
                ok += 1
                nbytes += sz
            elif status == "skip":
                skip += 1
            else:
                fail += 1
                print(f"  [{slug}] {status}  ({url})", flush=True)
            if i % 50 == 0:
                print(f"  {slug}: {i}/{len(res)} | ok={ok} skip={skip} "
                      f"fail={fail} | {nbytes/1e9:.2f} GB | {int(time.time()-t0)}s",
                      flush=True)
    print(f"\n=== CONCLUIDO: ok={ok} skip={skip} fail={fail} | "
          f"{nbytes/1e9:.2f} GB | {int(time.time()-t0)}s ===", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--so-espelhos" in args:
        slugs = ESPELHOS
    elif not args or "--tudo" in args:
        slugs = ESPELHOS + INTEGRAS
    else:
        slugs = args
    print("Baixando:", slugs, flush=True)
    run(slugs)
