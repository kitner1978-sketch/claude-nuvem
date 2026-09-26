"""
Extrator de texto de PDFs para pesquisa doutrinária.
Uso: python extract_pdf.py <arquivo.pdf> <pagina_inicio> <pagina_fim> [arquivo_saida.txt]
"""
import sys
import fitz  # PyMuPDF

def extract_pages(pdf_path, start_page, end_page, output_path=None):
    doc = fitz.open(pdf_path)
    total = len(doc)
    start = max(0, start_page - 1)  # 1-indexed to 0-indexed
    end = min(total, end_page)

    text_parts = []
    for i in range(start, end):
        page = doc[i]
        text = page.get_text("text")
        text_parts.append(f"\n--- PÁGINA {i+1} ---\n{text}")

    full_text = "\n".join(text_parts)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Extraído: páginas {start_page}-{end_page} de {total} → {output_path}")
    else:
        print(full_text)

    return full_text

def get_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    print(f"Total de páginas: {len(doc)}")
    if toc:
        print(f"\n=== SUMÁRIO ({len(toc)} entradas) ===")
        for level, title, page in toc:
            indent = "  " * (level - 1)
            print(f"{indent}{title} ... p.{page}")
    else:
        print("(sem sumário embutido no PDF)")
    return toc

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_pdf.py <arquivo.pdf> [pagina_inicio] [pagina_fim] [saida.txt]")
        print("  Sem páginas: mostra sumário/TOC")
        sys.exit(1)

    pdf = sys.argv[1]

    if len(sys.argv) == 2:
        get_toc(pdf)
    elif len(sys.argv) >= 4:
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        out = sys.argv[4] if len(sys.argv) > 4 else None
        extract_pages(pdf, start, end, out)
    else:
        print("Forneça página inicial e final, ou nenhuma para ver o sumário.")
