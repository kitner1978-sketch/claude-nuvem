"""Conferência reversa: cada trecho entre aspas do livro contra TODAS as teses oficiais.

O check_teses.py parte do número do Tema citado no texto e compara a tese entre aspas
com a tese oficial daquele número. Este script faz o caminho inverso: pega todo trecho
entre aspas com 90+ caracteres, procura a tese oficial mais parecida (STJ, STF, TNU) e
lista os casos parecidos mas não idênticos (semelhança entre 0,55 e 0,93). É o que acha
tese "modernizada" dentro das aspas mesmo quando o número do Tema está longe do trecho.

Bases usadas (oficiais, já baixadas no repositório, pasta jurisprudencia/):
  stj/precedentes/temas.csv · stf/temas_repercussao_geral_stf.xlsx · tnu/temas_representativos_tnu.json

Uso:  python3 conferir_aspas_reverso.py
Saída: lista no terminal. Nada é alterado nos capítulos.
Leitura dos resultados: semelhança alta (≥ 0,80) com o mesmo tema citado perto = quase
sempre paráfrase dentro das aspas (restaurar o literal). Semelhança baixa com tema de
assunto diverso = em geral aspas de outra coisa (lei, doutrina); conferir no contexto.
"""
import re, glob, csv, json, unicodedata, difflib, collections
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parents[2]
J = RAIZ / "jurisprudencia"
B = RAIZ / "output" / "rascunhos"


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()


def score(q, t):
    a, b = norm(q).split(), norm(t).split()
    if not a or not b:
        return 0.0
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(x.size for x in sm.get_matching_blocks()) / len(a)


def carregar_teses():
    off = {}
    with open(J / "stj/precedentes/temas.csv", encoding='utf8') as f:
        for row in csv.DictReader(f):
            if row['tipoPrecedente'] == 'Tema':
                try:
                    off[('STJ', int(row['numeroPrecedente']))] = row['teseFirmada']
                except ValueError:
                    pass
    for d in json.load(open(J / "tnu/temas_representativos_tnu.json", encoding='utf8')):
        try:
            off[('TNU', int(d['Tema']))] = d.get('Tese firmada', '')
        except (ValueError, KeyError):
            pass
    wb = openpyxl.load_workbook(J / "stf/temas_repercussao_geral_stf.xlsx", read_only=True)
    it = wb.active.iter_rows(values_only=True)
    h = [str(x) for x in next(it)]
    for r in it:
        try:
            off[('STF', int(r[h.index('Número tema')]))] = r[h.index('Tese')] or ''
        except (ValueError, TypeError):
            pass
    # teses ainda não publicadas vêm como "*Aguardando..." — fora da comparação
    return {k: v for k, v in off.items() if v and not v.startswith('*')}


def main():
    off = carregar_teses()
    toks = lambda s: [w for w in norm(s).split() if len(w) > 4]
    idx = collections.defaultdict(set)
    for k, t in off.items():
        for w in set(toks(t)):
            idx[w].add(k)
    aspas = re.compile(r'["“]([^"“”]{90,1600})["”]')
    res = []
    for f in sorted(glob.glob(str(B / "cap_[0-9][0-9]_rascunho.md"))):
        cap = int(Path(f).name[4:6])
        txt = open(f, encoding='utf8').read()
        corpo = re.split(r'(?m)^#{2,4} *Refer[êe]ncias', txt)[0]
        for m in aspas.finditer(corpo):
            q = m[1]
            ws = toks(q)
            if len(ws) < 8:
                continue
            cand = collections.Counter()
            for w in set(ws):
                if len(idx[w]) < 400:
                    for k in idx[w]:
                        cand[k] += 1
            melhor = (0, None)
            for k, _ in cand.most_common(6):
                s = max(score(q, off[k]), score(off[k], q) if len(off[k]) > 0.6 * len(q) else 0)
                if s > melhor[0]:
                    melhor = (s, k)
            if melhor[1] and 0.55 <= melhor[0] < 0.93:
                res.append((melhor[0], cap, txt.count('\n', 0, m.start()) + 1, melhor[1], q, off[melhor[1]]))
    res.sort()
    print("trechos entre aspas parecidos com uma tese oficial, mas não idênticos:", len(res))
    for s, cap, ln, k, q, t in res:
        print(f"\n### cap {cap:02d}, linha {ln} ~ {k[0]} Tema {k[1]} (semelhança {s:.2f})")
        print("  LIVRO  :", q[:340])
        print("  OFICIAL:", re.sub(r'\s+', ' ', t)[:340])


if __name__ == '__main__':
    main()
