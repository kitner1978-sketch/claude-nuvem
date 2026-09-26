import io,sys
from pathlib import Path as _P
_RAIZ = _P(__file__).resolve().parents[2]   # raiz do repositório (…/projeto_livro)
BASE = str(_RAIZ / "output" / "rascunhos") + "/"
LOG=[]
def patch(cap,pairs):
    f=BASE+f"cap_{cap:02d}_rascunho.md"; s=open(f,encoding='utf8').read(); n0=len(s)
    for i,(old,new) in enumerate(pairs):
        c=s.count(old)
        if c!=1: raise SystemExit(f"cap {cap} patch #{i}: '{old[:60]}…' ocorre {c}x (esperado 1)")
        s=s.replace(old,new)
    open(f,'w',encoding='utf8',newline='\n').write(s)
    print(f"cap {cap:02d}: {len(pairs)} trechos aplicados ({len(s)-n0:+d} caracteres)")
