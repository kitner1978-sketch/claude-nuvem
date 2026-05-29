"""Find relevant chapter pages in PDFs."""
import sys, os, io, fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PDF_DIR = r"D:\Projeto Livro\pdf"
files = sorted([f for f in os.listdir(PDF_DIR) if f.lower().endswith('.pdf')])

def search_toc(idx, keywords):
    path = os.path.join(PDF_DIR, files[idx])
    doc = fitz.open(path)
    toc = doc.get_toc()
    print(f"=== {files[idx]} ({len(doc)} pgs) ===")
    if not toc:
        print("  (sem sumario)")
    else:
        for level, title, page in toc:
            tl = title.lower()
            if any(k in tl for k in keywords):
                indent = "  " * level
                print(f"  {indent}{title} ... p.{page}")
    doc.close()

def search_text(idx, keywords, page_range):
    path = os.path.join(PDF_DIR, files[idx])
    doc = fitz.open(path)
    start, end = page_range
    for i in range(max(0,start-1), min(len(doc), end)):
        text = doc[i].get_text("text")
        for kw in keywords:
            if kw.lower() in text.lower():
                # Get context
                pos = text.lower().find(kw.lower())
                snippet = text[max(0,pos-40):pos+60].replace('\n',' ').strip()
                print(f"  p.{i+1}: ...{snippet}...")
                break
    doc.close()

if __name__ == "__main__":
    kw = ['segurad', 'depend', 'carencia', 'qualidade de segurado', 'filia',
          'periodo de graca', 'beneficiar']

    # Santos [11]
    search_toc(11, kw)
    print()

    # Castro & Lazzari [3] - search text since no TOC
    print(f"=== {files[3]} - buscando capitulos ===")
    search_text(3, ['Segurados do Regime Geral', 'Segurados obrigat'],
                (200, 350))
    print()
    search_text(3, ['Manutenção e Perda da Qualidade'],
                (300, 500))
    print()
    search_text(3, ['Dependentes do Regime', 'Capítulo 16'],
                (350, 550))
    print()

    # Search for Carencia chapter in Castro
    print("Castro - carencia:")
    search_text(3, ['Período de carência', 'Da carência'],
                (400, 700))
