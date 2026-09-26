import re,glob,csv,json,unicodedata,difflib,collections,openpyxl
from pathlib import Path as _P
_RAIZ = _P(__file__).resolve().parents[2]   # raiz do repositório (…/projeto_livro)
J = str(_RAIZ / "jurisprudencia") + "/"; B = str(_RAIZ / "output" / "rascunhos") + "/"
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().lower())).strip()
OFF={}
with open(J+"stj/precedentes/temas.csv",encoding='utf8') as f:
    for row in csv.DictReader(f):
        if row['tipoPrecedente']=='Tema':
            try: OFF[('STJ',int(row['numeroPrecedente']))]=row['teseFirmada']
            except: pass
for d in json.load(open(J+"tnu/temas_representativos_tnu.json",encoding='utf8')):
    try: OFF[('TNU',int(d['Tema']))]=d.get('Tese firmada','')
    except: pass
wb=openpyxl.load_workbook(J+"stf/temas_repercussao_geral_stf.xlsx",read_only=True); ws=wb.active
it=ws.iter_rows(values_only=True); h=[str(x) for x in next(it)]
for r in it:
    try: OFF[('STF',int(r[h.index('Número tema')]))]=r[h.index('Tese')] or ''
    except: pass
def score(q,t):
    a,b=norm(q).split(),norm(t).split()
    if not a or not b: return 0.0
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    return sum(x.size for x in sm.get_matching_blocks())/len(a)
Q=r'["“]([^"“”]{80,1500})["”]'
out=[]
for f in sorted(glob.glob(B+"cap_[0-9][0-9]_rascunho.md")):
    cap=int(f[-14:-12])
    for n,line in enumerate(open(f,encoding='utf8'),1):
        for m in re.finditer(r'Tema (\d{1,2}\.?\d{1,3}|\d{1,3})',line):
            num=int(m[1].replace('.',''))
            ctx=line[max(0,m.start()-40):m.end()+30]
            t=re.search(r'\b(STF|STJ|TNU)\b',line[m.end():m.end()+25]) or re.search(r'\b(STF|STJ|TNU)\b[^.;]{0,30}$',line[max(0,m.start()-40):m.start()])
            if not t: continue
            trib=t[1]; post=line[m.end():m.end()+1900]
            q=re.search(Q,post)
            if not q or q.start()>420: continue
            if re.search(r'Tema \d',post[:q.start()]): continue   # aspas pertencem a outro tema
            off=OFF.get((trib,num))
            if off is None: out.append((cap,n,trib,num,None,q[1])); continue
            if not off.strip(): continue
            out.append((cap,n,trib,num,round(score(q[1],off),2),q[1],off))
seen=set(); bad=[]
for o in out:
    k=(o[2],o[3],norm(o[5])[:80])
    if k in seen: continue
    seen.add(k)
    if o[4] is None or o[4]<0.82: bad.append(o)
print("citações de tese conferidas:",len(seen),"| abaixo de 0,82 ou tema ausente da base:",len(bad))
json.dump(bad,open(str(_P(__file__).parent/'dados'/'teses_suspeitas.json'),'w'),ensure_ascii=False)
for o in sorted(bad,key=lambda x:(x[4] is None, x[4] or 0)):
    print(f"\n### c{o[0]:02d}:{o[1]} {o[2]} Tema {o[3]} score={o[4]}")
    print("  LIVRO :",o[5][:330])
    if len(o)>6: print("  OFICIAL:",re.sub(r'\s+',' ',o[6])[:330])
