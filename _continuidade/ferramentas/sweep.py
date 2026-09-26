import re,glob,sys,json,os
from pathlib import Path as _P
_RAIZ = _P(__file__).resolve().parents[2]   # raiz do repositório (…/projeto_livro)
base = str(_RAIZ / "output" / "rascunhos") + "/"
files=sorted(glob.glob(base+"cap_[0-9][0-9]_rascunho.md"))
def sweep(pats,ctx=160,flags=re.I):
    out=[]
    for f in files:
        cap=int(os.path.basename(f)[4:6]); sec=''
        for n,line in enumerate(open(f,encoding='utf8'),1):
            if line.startswith('#'): sec=line.strip('# \n')[:70]
            for name,p in pats.items():
                for m in re.finditer(p,line,flags):
                    s=max(0,m.start()-ctx); e=min(len(line),m.end()+ctx)
                    out.append(dict(cap=cap,ln=n,sec=sec,pat=name,hit=m[0],ctx=line[s:e].strip()))
    return out
