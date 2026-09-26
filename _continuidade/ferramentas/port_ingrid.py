import json,re,difflib,collections,sys
from pathlib import Path as _P
_RAIZ = _P(__file__).resolve().parents[2]   # raiz do repositório (…/projeto_livro)
B = str(_RAIZ / "output" / "rascunhos") + "/"
rows=json.load(open(str(_P(__file__).parent/'dados'/'edits_ingrid.json')))
APPLY='--apply' in sys.argv
QUO='["“”\'‘’]'
def tokre(t):
    t=re.escape(t); t=re.sub(r'\\?["“”]',QUO,t); t=t.replace('\\-','[-–—]')
    return r'[\*_`]*'+t+r'[\*_`]*'
SEP=r'[\s\*_]+'
def is_hyphen_only(o,n): return re.sub(r'-','',' '.join(n)).replace(' ','')==''.join(o).replace(' ','').replace('-','') and 'mínimo' in ' '.join(o+n).lower() or (re.sub(r'(?i)(sal[áa]rios?)-(m[íi]nimos?)',r'\1 \2',' '.join(n))==' '.join(o))
def is_renumber(o,n): return len(o)==1==len(n) and re.fullmatch(r'\d+\.',o[0] or '') and re.fullmatch(r'\d+\.',n[0] or '')
stats=collections.Counter(); unported=[]; texts={}
def load(c):
    if c not in texts: texts[c]=open(B+f"cap_{c:02d}_rascunho.md",encoding='utf8').read()
    return texts[c]
for cap,kind,a,b,i1,j1 in rows:
    if cap==0: stats['pré-textual']+=1; continue
    wa,wb=a.split(),b.split(); sm=difflib.SequenceMatcher(None,wa,wb,autojunk=False)
    for tag,x1,x2,y1,y2 in sm.get_opcodes():
        if tag=='equal': continue
        o,n=wa[x1:x2],wb[y1:y2]
        if is_renumber(o,n): stats['renumeração de lista (gerador)']+=1; continue
        if o and n and is_hyphen_only(o,n): stats['salário-mínimo (global)']+=1; continue
        s=load(cap); done=False
        for ctx in (4,6,2,8):
            L=wa[max(0,x1-ctx):x1]; R=wa[x2:x2+ctx]
            if not L and not R: break
            parts=[tokre(t) for t in L]; go=len(parts); parts+=[tokre(t) for t in o]; parts+=[tokre(t) for t in R]
            if not parts: break
            pat=SEP.join(parts)
            try: ms=list(re.finditer(pat,s))
            except re.error: break
            if len(ms)==1:
                m=ms[0]
                # localizar o trecho 'o' dentro do match
                if o:
                    sub=re.search(SEP.join(tokre(t) for t in o), s[m.start():m.end()] if not L else s[m.start():m.end()])
                    # posição: após o contexto esquerdo
                    if L:
                        lm=re.match(SEP.join(tokre(t) for t in L)+SEP, s[m.start():m.end()])
                        st=m.start()+lm.end()
                    else: st=m.start()
                    om=re.match(SEP.join(tokre(t) for t in o), s[st:])
                    if not om: break
                    en=st+om.end(); old_txt=s[st:en]
                    # preservar marcação markdown nas bordas
                    pre=re.match(r'[\*_`]*',old_txt)[0]; suf=re.search(r'[\*_`]*$',old_txt)[0]
                    new_txt=pre+' '.join(n)+suf if n else ''
                    if not n:  # deleção: remover também um espaço
                        if s[en:en+1]==' ': en+=1
                    s=s[:st]+new_txt+s[en:]
                else:  # inserção pura
                    lm=re.match(SEP.join(tokre(t) for t in L), s[m.start():m.end()]) if L else None
                    st=m.start()+(lm.end() if lm else 0)
                    if not L: break   # inserção sem contexto à esquerda: não transportar (numeração de títulos etc.)
                    s=s[:st]+' '+' '.join(n)+s[st:]
                if abs(len(s)-len(texts[cap]))>400: stats['rejeitada (salvaguarda)']+=1; break
                texts[cap]=s; stats['transportada']+=1; done=True; break
            if len(ms)>1: continue
        if not done:
            stats['não transportada']+=1; unported.append((cap,' '.join(o),' '.join(n),' '.join(wa[max(0,x1-5):x1]),' '.join(wa[x2:x2+5])))
print(dict(stats))
json.dump(unported,open(str(_P(__file__).parent/'dados'/'ingrid_nao_transportadas.json'),'w'),ensure_ascii=False,indent=0)
if APPLY:
    for c,s in texts.items(): open(B+f"cap_{c:02d}_rascunho.md",'w',encoding='utf8',newline='\n').write(s)
    print("gravado em",len(texts),"capítulos")
else:
    print("(simulação) amostra de não transportadas:")
    for u in unported[:25]: print(f"  c{u[0]:02d}: …{u[3][-40:]} [-{u[1][:60]}-]{{+{u[2][:60]}+}} {u[4][:40]}…")
