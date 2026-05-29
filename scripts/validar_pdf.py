#!/usr/bin/env python3
"""
validar_pdf.py — Validação automática pós-geração do PDF/DOCX

Verifica:
  1. Todos os 23 capítulos estão presentes
  2. Todas as 6 partes estão presentes
  3. Nenhum artefato Markdown residual (*, #, |, :::)
  4. Contagem de páginas razoável
  5. Metadados do documento
  6. Integridade dos DOCX individuais (23 arquivos)
"""

import re
import sys
import os
from pathlib import Path


def validate_docx_individual(docx_dir):
    """Valida os 23 DOCX individuais."""
    issues = []
    ok_count = 0

    for cap_id in range(1, 24):
        cap_str = f"{cap_id:02d}"
        docx_path = docx_dir / f"cap_{cap_str}.docx"

        if not docx_path.exists():
            issues.append(f"FALTANDO: cap_{cap_str}.docx")
            continue

        size_kb = docx_path.stat().st_size / 1024
        if size_kb < 10:
            issues.append(f"cap_{cap_str}.docx muito pequeno ({size_kb:.0f} KB)")
            continue

        ok_count += 1

    return ok_count, issues


def validate_markdown_sources(rascunhos_dir):
    """Verifica artefatos Markdown residuais nos MDs fonte."""
    issues = []
    stats = {'total_words': 0, 'chapters': 0}

    for cap_id in range(1, 24):
        cap_str = f"{cap_id:02d}"
        md_path = rascunhos_dir / f"cap_{cap_str}_rascunho.md"

        if not md_path.exists():
            issues.append(f"MD FALTANDO: cap_{cap_str}_rascunho.md")
            continue

        text = md_path.read_text(encoding='utf-8')
        stats['chapters'] += 1
        stats['total_words'] += len(text.split())

        lines = text.split('\n')
        for i, line in enumerate(lines, 1):
            s = line.strip()
            # Pular linhas legítimas de Markdown (headings, boxes, listas)
            if s.startswith('#') or s.startswith(':::') or s.startswith('|'):
                continue
            if s.startswith('- ') or s.startswith('> ') or re.match(r'^\d+\.\s', s):
                continue
            if s.startswith('---'):
                continue

            # Detectar asteriscos soltos (não em negrito/itálico válido)
            # Padrão: asterisco que não faz parte de **bold** ou *italic*
            orphan_asterisks = re.findall(r'(?<!\*)\*(?!\*)', s)
            # Filtrar: se tem par fechando, é itálico legítimo
            if s.count('*') % 2 != 0 and orphan_asterisks:
                issues.append(f"cap_{cap_str} L{i}: asterisco orfao -> {s[:60]}...")

            # Detectar pipes que não são tabela
            if '|' in s and not s.startswith('|'):
                # Pode ser pipe legítimo em texto — só avisar se parece tabela quebrada
                if s.count('|') >= 3:
                    issues.append(f"cap_{cap_str} L{i}: possiveis pipes de tabela -> {s[:60]}...")

            # Detectar hashes no meio do texto (heading quebrado)
            if re.search(r'(?<=\w)\s#{1,4}\s', s):
                issues.append(f"cap_{cap_str} L{i}: hash no meio do texto -> {s[:60]}...")

    return stats, issues


def validate_unified_docx(docx_path):
    """Valida o DOCX unificado do livro."""
    issues = []
    info = {}

    if not docx_path.exists():
        return info, ["DOCX unificado nao encontrado: " + str(docx_path)]

    from docx import Document
    doc = Document(str(docx_path))

    # Contar seções
    info['sections'] = len(doc.sections)

    # Verificar metadados
    core = doc.core_properties
    info['title'] = core.title or "(vazio)"
    info['author'] = core.author or "(vazio)"

    if not core.title:
        issues.append("Metadado 'title' esta vazio")
    if not core.author:
        issues.append("Metadado 'author' esta vazio")

    # Extrair texto e verificar conteúdo
    full_text = []
    heading_1_count = 0
    heading_2_count = 0

    for para in doc.paragraphs:
        full_text.append(para.text)
        if para.style and para.style.name == 'Heading 1':
            heading_1_count += 1
        elif para.style and para.style.name == 'Heading 2':
            heading_2_count += 1

    info['heading1_count'] = heading_1_count
    info['heading2_count'] = heading_2_count
    info['total_paragraphs'] = len(doc.paragraphs)

    all_text = '\n'.join(full_text)

    # Verificar que todas as partes estão presentes
    for part_num in ['I', 'II', 'III', 'IV', 'V', 'VI']:
        if f'PARTE {part_num}' not in all_text:
            issues.append(f"Parte {part_num} nao encontrada no DOCX")

    # Verificar que todos os capítulos estão presentes
    for cap_id in range(1, 24):
        cap_pattern = f'CAPITULO {cap_id}'
        cap_pattern2 = f'CAPÍTULO {cap_id}'
        if cap_pattern not in all_text.upper() and cap_pattern2 not in all_text.upper():
            issues.append(f"Capitulo {cap_id} nao encontrado no DOCX")

    # Verificar artefatos Markdown no DOCX
    md_artifacts = 0
    for para in doc.paragraphs:
        t = para.text.strip()
        if t.startswith(':::'):
            md_artifacts += 1
            issues.append(f"Artefato ::: encontrado: {t[:50]}...")
        if t.startswith('# ') or t.startswith('## ') or t.startswith('### '):
            md_artifacts += 1
            issues.append(f"Heading MD literal: {t[:50]}...")

    info['md_artifacts'] = md_artifacts

    # Verificar terminologia proibida
    termos_proibidos = []
    for para in doc.paragraphs:
        t = para.text.lower()
        if 'auxílio-doença' in t or 'auxilio-doenca' in t:
            # Verificar contexto — permitir se entre aspas ou contexto histórico
            if '"' not in para.text and '"' not in para.text:
                termos_proibidos.append(f"auxilio-doenca: {para.text[:60]}...")
        if 'aposentadoria por invalidez' in t:
            if '"' not in para.text and '"' not in para.text:
                termos_proibidos.append(f"apos. invalidez: {para.text[:60]}...")

    if termos_proibidos:
        info['termos_proibidos'] = len(termos_proibidos)
        for tp in termos_proibidos[:5]:  # Limitar a 5
            issues.append(f"Terminologia proibida: {tp}")
        if len(termos_proibidos) > 5:
            issues.append(f"  ... e mais {len(termos_proibidos) - 5} ocorrencias")

    return info, issues


def validate_pdf(pdf_path):
    """Valida o PDF gerado."""
    issues = []
    info = {}

    if not pdf_path.exists():
        return info, ["PDF nao encontrado: " + str(pdf_path)]

    info['size_mb'] = pdf_path.stat().st_size / (1024 * 1024)

    if info['size_mb'] < 1:
        issues.append(f"PDF muito pequeno ({info['size_mb']:.2f} MB)")
    elif info['size_mb'] > 50:
        issues.append(f"PDF muito grande ({info['size_mb']:.2f} MB)")

    # Tentar ler com PyPDF2 ou pypdf
    try:
        try:
            from pypdf import PdfReader
        except ImportError:
            from PyPDF2 import PdfReader

        reader = PdfReader(str(pdf_path))
        info['pages'] = len(reader.pages)

        if info['pages'] < 100:
            issues.append(f"PDF com poucas paginas ({info['pages']})")

        # Verificar metadados
        meta = reader.metadata
        if meta:
            info['pdf_title'] = meta.title or "(vazio)"
            info['pdf_author'] = meta.author or "(vazio)"

        # Amostra: verificar primeiras e últimas páginas
        if info['pages'] > 0:
            first_page_text = reader.pages[0].extract_text() or ""
            if len(first_page_text.strip()) < 10:
                issues.append("Primeira pagina parece vazia")

    except ImportError:
        issues.append("AVISO: pypdf/PyPDF2 nao instalado — validacao de PDF limitada")
    except Exception as e:
        issues.append(f"Erro ao ler PDF: {e}")

    return info, issues


def main():
    project_dir = Path(__file__).parent.parent
    output_dir = project_dir / "output"
    docx_dir = output_dir / "docx"
    rascunhos_dir = output_dir / "rascunhos"

    # Determinar qual PDF validar
    pdf_candidates = sorted(output_dir.glob("livro_completo*.pdf"),
                           key=lambda p: p.stat().st_mtime, reverse=True)
    pdf_path = pdf_candidates[0] if pdf_candidates else output_dir / "livro_completo.pdf"

    docx_candidates = sorted(output_dir.glob("livro_completo*.docx"),
                            key=lambda p: p.stat().st_mtime, reverse=True)
    docx_path = docx_candidates[0] if docx_candidates else output_dir / "livro_completo.docx"

    print("=" * 65)
    print("VALIDACAO POS-GERACAO DO LIVRO")
    print("=" * 65)

    all_issues = []

    # 1. DOCX individuais
    print("\n1. DOCX individuais...")
    ok_count, issues = validate_docx_individual(docx_dir)
    all_issues.extend(issues)
    print(f"   {ok_count}/23 arquivos OK")
    for iss in issues:
        print(f"   PROBLEMA: {iss}")

    # 2. Markdown fonte
    print("\n2. Markdown fonte...")
    stats, issues = validate_markdown_sources(rascunhos_dir)
    all_issues.extend([i for i in issues if 'FALTANDO' in i])  # Só erros críticos
    print(f"   {stats['chapters']}/23 capitulos, ~{stats['total_words']:,} palavras")
    warnings_md = [i for i in issues if 'FALTANDO' not in i]
    if warnings_md:
        print(f"   {len(warnings_md)} avisos de artefatos (possiveis falsos positivos)")
        for w in warnings_md[:5]:
            print(f"   AVISO: {w}")

    # 3. DOCX unificado
    print(f"\n3. DOCX unificado: {docx_path.name}")
    info, issues = validate_unified_docx(docx_path)
    all_issues.extend(issues)
    if info:
        print(f"   Secoes: {info.get('sections', '?')}")
        print(f"   Heading 1 (Partes): {info.get('heading1_count', '?')}")
        print(f"   Heading 2 (Capitulos): {info.get('heading2_count', '?')}")
        print(f"   Paragrafos: {info.get('total_paragraphs', '?'):,}")
        print(f"   Titulo: {info.get('title', '?')}")
        if info.get('termos_proibidos'):
            print(f"   Termos proibidos: {info['termos_proibidos']}")
    for iss in issues:
        print(f"   PROBLEMA: {iss}")

    # 4. PDF
    print(f"\n4. PDF: {pdf_path.name}")
    info, issues = validate_pdf(pdf_path)
    all_issues.extend(issues)
    if info:
        print(f"   Tamanho: {info.get('size_mb', 0):.2f} MB")
        print(f"   Paginas: {info.get('pages', '?')}")
        if 'pdf_title' in info:
            print(f"   Titulo PDF: {info['pdf_title']}")
    for iss in issues:
        print(f"   PROBLEMA: {iss}")

    # Resumo
    print("\n" + "=" * 65)
    critical = [i for i in all_issues if 'FALTANDO' in i or 'nao encontrad' in i]
    warnings = [i for i in all_issues if i not in critical]

    if not all_issues:
        print("RESULTADO: TUDO OK - Nenhum problema encontrado!")
    else:
        if critical:
            print(f"RESULTADO: {len(critical)} ERROS CRITICOS, {len(warnings)} avisos")
        else:
            print(f"RESULTADO: {len(warnings)} avisos (nenhum erro critico)")
    print("=" * 65)

    return 1 if critical else 0


if __name__ == '__main__':
    sys.exit(main())
