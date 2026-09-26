#!/usr/bin/env python3
"""
md_to_docx.py — Converte capítulo Markdown em DOCX editorial
Design Code: Livro de Doutrina Jurídica v1.0

Uso: python md_to_docx.py <arquivo.md> [--no-strip-citations]

Etapas:
  1. Lê o Markdown
  2. Remove citações autorais do corpo (mantém seção Referências)
  3. Gera DOCX com design editorial (A5, margens espelhadas, boxes, etc.)
"""

import re
import sys
import os
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, Emu, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import copy


# ═══════════════════════════════════════════════════════
# CORES DO DESIGN CODE
# ═══════════════════════════════════════════════════════

COLORS = {
    "body_text":     "201B16",
    "title_text":    "2F2923",
    "heading_text":  "3A3128",
    "muted_text":    "6B6256",
    "gold_accent":   "B78B37",
    "gold_dark":     "8A6A2A",
    "rule_light":    "D7CDBB",
    "box_border":    "D2C9B8",
    "box_atencao_bg":    "F7F1E6",
    "box_juris_bg":      "EEF3F7",
    "box_pratica_bg":    "F0F4ED",
    "box_atencao_accent":  "B78B37",
    "box_juris_accent":    "4D6F8A",
    "box_pratica_accent":  "6E8563",
}

def hex_to_rgb(hex_str):
    return RGBColor(int(hex_str[:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))


# ═══════════════════════════════════════════════════════
# ETAPA 1 — REMOÇÃO DE CITAÇÕES AUTORAIS
# ═══════════════════════════════════════════════════════

def strip_citations(text: str) -> str:
    """Remove citações autorais do corpo do texto, preservando a seção Referências."""

    # Separar corpo e referências
    ref_split = re.split(r'^(## Referências)', text, maxsplit=1, flags=re.MULTILINE)
    if len(ref_split) >= 3:
        body = ref_split[0]
        refs = ref_split[1] + ref_split[2]
    else:
        body = text
        refs = ""

    # --- Padrão 1: Citações parentéticas (multi-autor com ;) ---
    # (SOBRENOME, ANO; SOBRENOME, ANO), (CASTRO; LAZZARI, 2024), etc.
    body = re.sub(
        r'\s*\([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ\s;,\d]+\d{4}[a-z]?\)\s*',
        ' ', body
    )

    # Padrão genérico para (Autor, ANO) com mixed case
    body = re.sub(
        r'\s*\([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][a-záéíóúâêîôûãõç]+(?:\s+[A-Za-záéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+)*,\s*\d{4}[a-z]?\)\s*',
        ' ', body
    )

    # Padrão para mixed case multi-autor: (Castro e Lazzari, 2025; Kertzman, 2024)
    body = re.sub(
        r'\s*\([A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*(?:;\s*[A-Z][a-záéíóúâêîôûãõç]+(?:\s+[A-Za-záéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+)*)*,\s*\d{4}[a-z]?\)\s*',
        ' ', body
    )

    # --- Padrão 2: Frases narrativas com autor ---
    # "Como ensina Autor (ANO)," / "Conforme leciona Autor (ANO)," etc.
    narrative_patterns = [
        r'[Cc]omo\s+(?:ensina|leciona|observa[m]?|destaca[m]?|afirma[m]?|registra[m]?|pontua[m]?|sintetiza[m]?|acrescenta[m]?|anota[m]?|sustenta[m]?|adverte[m]?|esclarece[m]?|aponta[m]?|assinala[m]?|explica[m]?)\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\),?\s*',
        r'[Cc]onforme\s+(?:leciona|ensina|observa[m]?|destaca[m]?|afirma[m]?)\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\),?\s*',
        r'[Nn]as\s+palavras\s+de\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\),?\s*',
        r'[Ss]egundo\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\),?\s*',
        r'[Pp]ara\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\),?\s*',
    ]
    for pat in narrative_patterns:
        body = re.sub(pat, '', body)

    # --- Padrão 3: Autor (ANO) como sujeito ---
    # "Ibrahim (2019) ensina que..." → remove "Ibrahim (2019) "
    body = re.sub(
        r'(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\)\s+(?=(?:ensina|leciona|destaca|afirma|sustenta|observa|pontua|assinala|esclarece|acrescenta|adverte|registra))',
        '', body
    )

    # --- Padrão 4: "conforme Autor (ANO)" inline ---
    body = re.sub(
        r',?\s*conforme\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\)',
        '', body, flags=re.IGNORECASE
    )

    # --- Padrão 5: ", como destaca Autor (ANO)" no final ---
    body = re.sub(
        r',?\s*como\s+(?:destaca|ensina|leciona|afirma|observa|pontua|sintetiza|acrescenta|registra|sustenta)[m]?\s+(?:[A-Z][a-záéíóúâêîôûãõç]+(?:\s+(?:e|Jr\.|Júnior|Filho|Neto|Sobrinho|dos|das|de|da|do)\s*)*(?:\s+[A-Z][a-záéíóúâêîôûãõç]+)*)\s*\(\d{4}[a-z]?\)',
        '', body
    )

    # --- Padrão 6: Citações restantes "(Autor, ANO)" ---
    body = re.sub(
        r'\s*\([A-Z][a-záéíóúâêîôûãõç]+(?:\s+[A-Za-záéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+)*(?:;\s*[A-Z][a-záéíóúâêîôûãõç]+(?:\s+[A-Za-záéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]+)*)*,\s*\d{4}[a-z]?\)',
        '', body
    )

    # --- Limpeza final ---
    # Remover espaços duplos
    body = re.sub(r'  +', ' ', body)
    # Remover espaço antes de pontuação
    body = re.sub(r' ([.,;:!?])', r'\1', body)
    # Corrigir início de frase em minúscula após remoção
    # (quando a citação era o início do período)
    body = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), body)
    # Remover linhas com apenas espaços
    body = re.sub(r'\n +\n', '\n\n', body)
    # Remover vírgulas duplicadas
    body = re.sub(r',\s*,', ',', body)
    # Remover vírgula antes de ponto
    body = re.sub(r',\s*\.', '.', body)

    return body + refs


# ═══════════════════════════════════════════════════════
# ETAPA 2 — PARSING DO MARKDOWN
# ═══════════════════════════════════════════════════════

def parse_markdown(text: str):
    """Transforma o Markdown em lista de blocos estruturados."""
    lines = text.split('\n')
    blocks = []
    i = 0

    # Remove YAML frontmatter
    if lines and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        i += 1  # pula o --- final

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Linha vazia
        if not stripped:
            i += 1
            continue

        # Título do capítulo: ## Capítulo X — Título
        if stripped.startswith('## Capítulo'):
            blocks.append({'type': 'chapter_title', 'text': stripped[3:]})
            i += 1
            continue

        # Referências
        if stripped.startswith('## Referências') or stripped.startswith('## REFERÊNCIAS'):
            blocks.append({'type': 'references_heading'})
            i += 1
            # Coletar entradas de referência
            while i < len(lines):
                ref_line = lines[i].strip()
                if ref_line:
                    blocks.append({'type': 'reference_entry', 'text': ref_line})
                i += 1
            continue

        # Seção principal: ### X.Y Título
        if stripped.startswith('### '):
            blocks.append({'type': 'section', 'text': stripped[4:]})
            i += 1
            continue

        # Subseção: #### X.Y.Z Título
        if stripped.startswith('#### '):
            blocks.append({'type': 'subsection', 'text': stripped[5:]})
            i += 1
            continue

        # Box
        box_match = re.match(r'^:::\s*(box-\w+|pratica|atencao|jurisprudencia)', stripped)
        if box_match:
            box_type = box_match.group(1)
            # Normalize to box- prefix
            if not box_type.startswith('box-'):
                box_type = f'box-{box_type}'
            i += 1
            box_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                box_lines.append(lines[i])
                i += 1
            i += 1  # pula o ::: de fechamento

            # Remover título interno do box (já será inserido pelo design)
            box_text = '\n'.join(box_lines).strip()
            # Remove linhas como **Atenção**, **Na Prática**, **Jurisprudência em Destaque**
            box_text = re.sub(
                r'^\*\*(?:Atenção|Na Prática|Jurisprudência em Destaque)\*\*\s*\n?',
                '', box_text
            ).strip()

            blocks.append({'type': 'box', 'box_type': box_type, 'text': box_text})
            continue

        # Parágrafo normal
        para_lines = [stripped]
        i += 1
        # Acumular linhas não-vazias que não sejam headings/boxes
        while i < len(lines):
            next_line = lines[i].strip()
            if (not next_line or
                next_line.startswith('#') or
                next_line.startswith(':::') or
                next_line.startswith('## ')):
                break
            para_lines.append(next_line)
            i += 1

        blocks.append({'type': 'paragraph', 'text': ' '.join(para_lines)})

    return blocks


# ═══════════════════════════════════════════════════════
# ETAPA 3 — GERAÇÃO DO DOCX
# ═══════════════════════════════════════════════════════

def set_page_a5_mirrored(doc):
    """Configura página A5 com margens espelhadas."""
    section = doc.sections[0]
    section.page_width = Cm(14.8)
    section.page_height = Cm(21.0)
    section.orientation = WD_ORIENT.PORTRAIT
    section.top_margin = Cm(1.65)
    section.bottom_margin = Cm(1.70)
    section.left_margin = Cm(2.05)   # inside
    section.right_margin = Cm(1.55)  # outside
    section.header_distance = Cm(0.80)
    section.footer_distance = Cm(0.75)

    # Mirror margins
    sectPr = section._sectPr
    pgMar = sectPr.find(qn('w:pgMar'))
    if pgMar is not None:
        pgMar.set(qn('w:mirrorMargins'), '1')
    # Also set on document level
    settings = doc.settings.element
    mirror = settings.find(qn('w:mirrorMargins'))
    if mirror is None:
        mirror = parse_xml(f'<w:mirrorMargins {nsdecls("w")} w:val="1"/>')
        settings.append(mirror)
    else:
        mirror.set(qn('w:val'), '1')


def add_run_with_style(paragraph, text, font_name="EB Garamond", size=Pt(10.7),
                       bold=False, italic=False, color=None, small_caps=False,
                       all_caps=False):
    """Adiciona run com formatação."""
    run = paragraph.add_run(text)
    run.font.name = font_name
    run.font.size = size
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = hex_to_rgb(color)
    if small_caps:
        run.font.small_caps = True
    if all_caps:
        run.font.all_caps = True
    # Set East Asian and Complex Script fonts too
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}/>')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    return run


def set_paragraph_spacing(paragraph, before=0, after=Pt(3.5), line_spacing=1.08):
    """Define espaçamento do parágrafo."""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before) if isinstance(before, (int, float)) else before
    pf.space_after = Pt(after) if isinstance(after, (int, float)) else after
    pf.line_spacing = line_spacing


def set_first_line_indent(paragraph, indent_cm=0.42):
    """Define recuo de primeira linha."""
    paragraph.paragraph_format.first_line_indent = Cm(indent_cm)


def add_paragraph_with_bold(doc_or_cell, text, font_name="EB Garamond", size=Pt(10.7),
                            color="201B16", alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                            first_indent=0.42, space_before=0, space_after=3.5,
                            line_spacing=1.08):
    """Adiciona parágrafo processando **negrito** inline."""
    p = doc_or_cell.add_paragraph()
    p.alignment = alignment
    set_paragraph_spacing(p, before=space_before, after=space_after, line_spacing=line_spacing)
    if first_indent > 0:
        set_first_line_indent(p, first_indent)

    # Parse bold markers
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            add_run_with_style(p, part[2:-2], font_name=font_name, size=size,
                             bold=True, color=color)
        else:
            add_run_with_style(p, part, font_name=font_name, size=size,
                             bold=False, color=color)
    return p


def add_section_border(paragraph, color_hex="B89B5E"):
    """Adiciona borda inferior dourada à seção."""
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="4" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


def keep_with_next(paragraph):
    """Mantém parágrafo junto ao seguinte."""
    pPr = paragraph._element.get_or_add_pPr()
    kwn = parse_xml(f'<w:keepNext {nsdecls("w")}/>')
    pPr.append(kwn)


def add_chapter_opening(doc, title_text):
    """Adiciona abertura do capítulo (etiqueta + título + ornamento)."""
    # Extrair número e título
    match = re.match(r'Capítulo\s+(\d+)\s*[—–-]\s*(.*)', title_text)
    if match:
        cap_num = match.group(1)
        cap_title = match.group(2).strip()
    else:
        cap_num = "X"
        cap_title = title_text

    # Etiqueta: CAPÍTULO X
    p_label = doc.add_paragraph()
    p_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_label, before=12, after=4, line_spacing=1.0)
    add_run_with_style(p_label, f"CAPÍTULO {cap_num}", font_name="Noto Sans",
                      size=Pt(9.5), bold=True, color="8A6A2A", all_caps=True)

    # Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_title, before=0, after=8, line_spacing=1.0)
    add_run_with_style(p_title, cap_title.upper(), font_name="EB Garamond",
                      size=Pt(20), bold=True, color="2F2923")

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
    add_run_with_style(p_orn, "◆", font_name="EB Garamond",
                      size=Pt(9), color="B78B37")

    return cap_num, cap_title


def add_header_footer(doc, cap_num, cap_title):
    """Configura cabeçalho e rodapé."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    # Cabeçalho (páginas comuns)
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.clear()
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = add_run_with_style(hp, f"Capítulo {cap_num}  |  {cap_title}",
                            font_name="EB Garamond", size=Pt(8.6),
                            color="6B6256", small_caps=True)
    # Borda inferior
    pPr = hp._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="2" w:color="D7CDBB"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

    # Rodapé (todas as páginas) — número centralizado
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.clear()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Inserir campo PAGE
    run = fp.add_run()
    run.font.name = "EB Garamond"
    run.font.size = Pt(9)
    run.font.color.rgb = hex_to_rgb("6B6256")
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run._element.append(fldChar1)
    run2 = fp.add_run()
    run2.font.name = "EB Garamond"
    run2.font.size = Pt(9)
    run2.font.color.rgb = hex_to_rgb("6B6256")
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run2._element.append(instrText)
    run3 = fp.add_run()
    run3.font.name = "EB Garamond"
    run3.font.size = Pt(9)
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run3._element.append(fldChar2)

    # Rodapé da primeira página (só número, sem cabeçalho)
    first_footer = section.first_page_footer
    first_footer.is_linked_to_previous = False
    ffp = first_footer.paragraphs[0] if first_footer.paragraphs else first_footer.add_paragraph()
    ffp.clear()
    ffp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = ffp.add_run()
    frun.font.name = "EB Garamond"
    frun.font.size = Pt(9)
    frun.font.color.rgb = hex_to_rgb("6B6256")
    fc1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    frun._element.append(fc1)
    frun2 = ffp.add_run()
    frun2.font.name = "EB Garamond"
    frun2.font.size = Pt(9)
    frun2.font.color.rgb = hex_to_rgb("6B6256")
    fi = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    frun2._element.append(fi)
    frun3 = ffp.add_run()
    frun3.font.name = "EB Garamond"
    frun3.font.size = Pt(9)
    fc2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    frun3._element.append(fc2)


def add_box(doc, box_type, text):
    """Adiciona box editorial como tabela de 1 célula."""
    config = {
        'box-atencao': {
            'label': 'ATENÇÃO',
            'bg': COLORS['box_atencao_bg'],
            'accent': COLORS['box_atencao_accent'],
        },
        'box-jurisprudencia': {
            'label': 'JURISPRUDÊNCIA EM DESTAQUE',
            'bg': COLORS['box_juris_bg'],
            'accent': COLORS['box_juris_accent'],
        },
        'box-pratica': {
            'label': 'NA PRÁTICA',
            'bg': COLORS['box_pratica_bg'],
            'accent': COLORS['box_pratica_accent'],
        },
    }

    cfg = config.get(box_type, config['box-atencao'])

    # Criar tabela 1x1
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Largura da tabela (quase toda a largura da página)
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    tblPr.append(tblW)

    # Impedir quebra da tabela entre páginas
    tblPr_cantSplit = parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>')

    cell = table.cell(0, 0)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

    # Padding da célula
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="150" w:type="dxa"/>'
        f'  <w:bottom w:w="150" w:type="dxa"/>'
        f'  <w:left w:w="220" w:type="dxa"/>'
        f'  <w:right w:w="180" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

    # Fundo da célula
    shading = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{cfg["bg"]}" w:val="clear"/>'
    )
    tcPr.append(shading)

    # Bordas da célula (left grossa = accent, demais finas = box_border)
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="7" w:space="0" w:color="{COLORS["box_border"]}"/>'
        f'  <w:bottom w:val="single" w:sz="7" w:space="0" w:color="{COLORS["box_border"]}"/>'
        f'  <w:right w:val="single" w:sz="7" w:space="0" w:color="{COLORS["box_border"]}"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{cfg["accent"]}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    # Limpar parágrafo padrão
    for p in cell.paragraphs:
        p._element.getparent().remove(p._element)

    # Etiqueta do box
    p_label = cell.add_paragraph()
    p_label.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(p_label, before=0, after=3, line_spacing=1.0)
    add_run_with_style(p_label, cfg['label'], font_name="Noto Sans",
                      size=Pt(8.2), bold=True, color=cfg['accent'], all_caps=True)

    # Conteúdo do box (pode ter múltiplos parágrafos)
    paragraphs = text.split('\n\n') if '\n\n' in text else [text]
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        add_paragraph_with_bold(cell, para_text, size=Pt(9.6), color="201B16",
                               first_indent=0, space_before=0, space_after=3,
                               line_spacing=1.03)

    # Espaço após o box
    p_after = doc.add_paragraph()
    set_paragraph_spacing(p_after, before=0, after=4, line_spacing=1.0)
    # Parágrafo vazio pequeno para espaçamento


def add_page_break(doc):
    """Adiciona quebra de página."""
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(docx.enum.text.WD_BREAK.PAGE)


def generate_docx(blocks, output_path):
    """Gera o DOCX a partir dos blocos parseados."""
    doc = Document()

    # Configurar página
    set_page_a5_mirrored(doc)

    # Definir estilo padrão
    style = doc.styles['Normal']
    style.font.name = "EB Garamond"
    style.font.size = Pt(10.7)
    style.font.color.rgb = hex_to_rgb("201B16")
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style.paragraph_format.space_after = Pt(3.5)
    style.paragraph_format.line_spacing = 1.08

    cap_num = "X"
    cap_title = "Título"
    is_first_paragraph = True
    in_references = False

    for block in blocks:
        btype = block['type']

        if btype == 'chapter_title':
            cap_num, cap_title = add_chapter_opening(doc, block['text'])
            add_header_footer(doc, cap_num, cap_title)
            is_first_paragraph = True

        elif btype == 'section':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=18, after=7, line_spacing=1.0)
            add_run_with_style(p, block['text'], font_name="EB Garamond",
                             size=Pt(15.5), bold=True, color="3A3128")
            add_section_border(p)
            keep_with_next(p)
            is_first_paragraph = True

        elif btype == 'subsection':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=13, after=4, line_spacing=1.0)
            add_run_with_style(p, block['text'], font_name="EB Garamond",
                             size=Pt(12.5), bold=True, color="3A3128")
            keep_with_next(p)
            is_first_paragraph = True

        elif btype == 'box':
            add_box(doc, block['box_type'], block['text'])
            is_first_paragraph = True

        elif btype == 'references_heading':
            # Quebra de página
            p_break = doc.add_paragraph()
            run = p_break.add_run()
            from docx.enum.text import WD_BREAK
            run.add_break(WD_BREAK.PAGE)

            # Título REFERÊNCIAS
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p, before=16, after=5, line_spacing=1.0)
            add_run_with_style(p, "REFERÊNCIAS", font_name="EB Garamond",
                             size=Pt(12.2), bold=True, color="3A3128",
                             small_caps=True)
            in_references = True

        elif btype == 'reference_entry':
            p = add_paragraph_with_bold(doc, block['text'],
                                       size=Pt(9.4), color="201B16",
                                       alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                       first_indent=0, space_before=0,
                                       space_after=2.4, line_spacing=1.0)
            # Recuo francês
            pf = p.paragraph_format
            pf.left_indent = Cm(0.48)
            pf.first_line_indent = Cm(-0.48)

        elif btype == 'paragraph':
            indent = 0 if is_first_paragraph else 0.42
            add_paragraph_with_bold(doc, block['text'],
                                   first_indent=indent)
            is_first_paragraph = False

    # Metadados
    core_props = doc.core_properties
    core_props.title = f"Capítulo {cap_num} — {cap_title}"
    core_props.subject = "Direito Previdenciário"
    core_props.comments = "Diagramação em formato de capítulo de livro jurídico."
    core_props.keywords = "direito previdenciário; seguridade social; doutrina"

    doc.save(output_path)
    return output_path


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Uso: python md_to_docx.py <arquivo.md> [--no-strip-citations]")
        sys.exit(1)

    md_path = sys.argv[1]
    strip = '--no-strip-citations' not in sys.argv

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    basename = Path(md_path).stem.replace('.formatado', '').replace('_rascunho', '')

    if strip:
        print(f"  Removendo citações autorais do corpo...")
        text = strip_citations(text)

    print(f"  Parseando Markdown...")
    blocks = parse_markdown(text)
    print(f"  Blocos encontrados: {len(blocks)}")

    output_dir = Path(md_path).parent.parent / 'docx'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{basename}.docx"

    print(f"  Gerando DOCX: {output_path}")
    generate_docx(blocks, str(output_path))
    print(f"  OK Concluido: {output_path}")


if __name__ == '__main__':
    import docx.enum.text
    main()
