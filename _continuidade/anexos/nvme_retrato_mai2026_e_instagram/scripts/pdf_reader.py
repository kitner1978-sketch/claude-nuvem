"""
Leitor de PDFs com suporte a nomes UTF-8 no Windows.
Uso:
  python pdf_reader.py list              — lista PDFs com índices
  python pdf_reader.py toc <idx>         — mostra sumário do PDF
  python pdf_reader.py read <idx> <p1> <p2> [saida.txt] — extrai páginas
"""
import sys
import os
import io
import fitz

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PDF_DIR = r"D:\Projeto Livro\pdf"

def list_pdfs():
    files = sorted([f for f in os.listdir(PDF_DIR) if f.lower().endswith(('.pdf', '.epub'))])
    for i, f in enumerate(files):
        size_mb = os.path.getsize(os.path.join(PDF_DIR, f)) / (1024*1024)
        print(f"  [{i}] {f}  ({size_mb:.1f} MB)")
    return files

def get_pdf_path(files, idx):
    return os.path.join(PDF_DIR, files[int(idx)])

def show_toc(path):
    doc = fitz.open(path)
    total = len(doc)
    toc = doc.get_toc()
    print(f"Arquivo: {os.path.basename(path)}")
    print(f"Total de paginas: {total}")
    if toc:
        print(f"\n=== SUMARIO ({len(toc)} entradas) ===")
        for level, title, page in toc[:120]:
            indent = "  " * (level - 1)
            print(f"  {indent}{title} ... p.{page}")
        if len(toc) > 120:
            print(f"  ... (+{len(toc)-120} entradas)")
    else:
        print("(sem sumario embutido)")
    doc.close()

def read_pages(path, p1, p2, output=None):
    doc = fitz.open(path)
    total = len(doc)
    start = max(0, p1 - 1)
    end = min(total, p2)
    parts = []
    for i in range(start, end):
        text = doc[i].get_text("text")
        parts.append(f"\n--- PAGINA {i+1} ---\n{text}")
    full = "\n".join(parts)
    if output:
        out_path = os.path.join(r"D:\Projeto Livro\pdf", output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full)
        print(f"Extraido: p.{p1}-{p2} de {total} -> {out_path}")
    else:
        print(full[:30000])
        if len(full) > 30000:
            print(f"\n[... TRUNCADO: {len(full)} chars total ...]")
    doc.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pdf_reader.py [list|toc|read] ...")
        sys.exit(1)

    cmd = sys.argv[1]
    files = sorted([f for f in os.listdir(PDF_DIR) if f.lower().endswith(('.pdf', '.epub'))])

    if cmd == "list":
        list_pdfs()
    elif cmd == "toc" and len(sys.argv) >= 3:
        show_toc(get_pdf_path(files, sys.argv[2]))
    elif cmd == "read" and len(sys.argv) >= 5:
        out = sys.argv[5] if len(sys.argv) > 5 else None
        read_pages(get_pdf_path(files, sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), out)
    else:
        print("Comando invalido. Use: list, toc <idx>, read <idx> <p1> <p2> [saida]")
