#!/usr/bin/env python3
"""
gerar_livro_pdf.py — Gera PDF unificado do livro completo
Reutiliza o Design Code do md_to_docx.py (A5, EB Garamond, boxes editoriais)

Etapas:
  1. Lê todos os capítulos Markdown em ordem
  2. Gera um DOCX unificado com capa, sumário, partes e capítulos
  3. Usa Word via COM para atualizar campos (TOC) e salvar como PDF
"""

import re
import sys
import os
from pathlib import Path

# Importar funções do md_to_docx
sys.path.insert(0, str(Path(__file__).parent))
from design_code import (
    COLORS, hex_to_rgb, FONT_SERIF, FONT_SANS,
    SIZE_BODY, SIZE_SECTION, SIZE_SUBSECTION,
    MARGINS_A5, apply_a5_margins, add_page_field,
)
from md_to_docx import (
    parse_markdown, strip_citations,
    set_page_a5_mirrored, add_run_with_style, set_paragraph_spacing,
    set_first_line_indent, add_paragraph_with_bold, add_section_border,
    keep_with_next, add_box, add_table_block, add_list_item, add_blockquote,
    add_drop_cap, apply_normal_style,
    _enable_auto_hyphenation, _set_style_language,
    _set_compat_settings, _enable_w14_namespace
)

from docx import Document
from docx.shared import Pt, Cm, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml


# ═══════════════════════════════════════════════════════
# ESTRUTURA DO LIVRO
# ═══════════════════════════════════════════════════════

BOOK_TITLE = "Direito Previdenciário:\nTeoria e Prática nos Juizados\nEspeciais Federais"
AUTHORS = ["Claudio Kitner", "Luiz Bispo da Silva Neto"]

PARTS = [
    {
        "num": "I",
        "title": "Fundamentos do Regime Geral de Previdência Social",
        "chapters": ["01", "02", "03", "04", "05"]
    },
    {
        "num": "II",
        "title": "Benefícios por Incapacidade",
        "chapters": ["06", "07"]
    },
    {
        "num": "III",
        "title": "Aposentadorias Programadas",
        "chapters": ["08", "09", "10", "11", "12"]
    },
    {
        "num": "IV",
        "title": "Pensões, Auxílios e Benefício Assistencial",
        "chapters": ["13", "14", "15", "16", "17", "18", "19"]
    },
    {
        "num": "V",
        "title": "Temas Transversais",
        "chapters": ["20", "21"]
    },
    {
        "num": "VI",
        "title": "Processo Previdenciário nos JEFs",
        "chapters": ["22", "23"]
    },
]


# Campo PAGE: reutiliza design_code.add_page_field (antes duplicado aqui).
add_page_number_field = add_page_field


def setup_section(section, is_first=False):
    """Configura seção A5 com margens espelhadas."""
    apply_a5_margins(section)


def add_new_section(doc, start_type='NEW_PAGE'):
    """Adiciona nova seção com quebra de página (ou ODD_PAGE para partes).
    IMPORTANTE: remove pgNumType herdado para evitar que todas as seções
    reiniciem a numeração em 1 (bug do python-docx ao copiar sectPr).
    """
    from docx.enum.section import WD_SECTION_START
    st = getattr(WD_SECTION_START, start_type, WD_SECTION_START.NEW_PAGE)
    new_section = doc.add_section(st)
    setup_section(new_section)

    # Remover pgNumType herdado da seção anterior (causa do bug TOC página "1")
    sectPr = new_section._sectPr
    for old_pgNum in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(old_pgNum)

    return new_section


EVEN_HEADER_TEXT = "Direito Previdenciário"


def _add_header_content(paragraph, text, alignment=WD_ALIGN_PARAGRAPH.RIGHT):
    """Configura conteúdo de um parágrafo de cabeçalho."""
    paragraph.clear()
    paragraph.alignment = alignment
    if text:
        add_run_with_style(paragraph, text, font_name=FONT_SERIF,
                          size=Pt(8.6), color="6B6256", small_caps=True)
        pPr = paragraph._element.get_or_add_pPr()
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'  <w:bottom w:val="single" w:sz="4" w:space="2" w:color="D7CDBB"/>'
            f'</w:pBdr>'
        )
        pPr.append(pBdr)


def setup_header_footer(section, header_text="", first_page_no_header=True,
                        even_header_text=None):
    """Configura cabeçalho (par/ímpar) e rodapé com fólio alternado.
    - Páginas ímpares (direita): header=capítulo, rodapé=número à direita
    - Páginas pares (esquerda): header=livro, rodapé=número à esquerda
    - Primeira página: sem header, rodapé centralizado
    """
    section.different_first_page_header_footer = first_page_no_header
    if even_header_text is None:
        even_header_text = EVEN_HEADER_TEXT

    # Cabeçalho ímpar (páginas direitas) — nome do capítulo
    odd_header = section.header
    odd_header.is_linked_to_previous = False
    ohp = odd_header.paragraphs[0] if odd_header.paragraphs else odd_header.add_paragraph()
    _add_header_content(ohp, header_text, WD_ALIGN_PARAGRAPH.RIGHT)

    # Cabeçalho par (páginas esquerdas) — nome do livro
    even_header = section.even_page_header
    even_header.is_linked_to_previous = False
    ehp = even_header.paragraphs[0] if even_header.paragraphs else even_header.add_paragraph()
    _add_header_content(ehp, even_header_text, WD_ALIGN_PARAGRAPH.LEFT)

    # Rodapé ímpar (páginas direitas) — número à DIREITA
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.clear()
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_page_number_field(fp)

    # Rodapé par (páginas esquerdas) — número à ESQUERDA
    even_footer = section.even_page_footer
    even_footer.is_linked_to_previous = False
    efp = even_footer.paragraphs[0] if even_footer.paragraphs else even_footer.add_paragraph()
    efp.clear()
    efp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_page_number_field(efp)

    # Primeira página: sem cabeçalho, rodapé centralizado
    if first_page_no_header:
        first_header = section.first_page_header
        first_header.is_linked_to_previous = False
        fhp = first_header.paragraphs[0] if first_header.paragraphs else first_header.add_paragraph()
        fhp.clear()

        first_footer = section.first_page_footer
        first_footer.is_linked_to_previous = False
        ffp = first_footer.paragraphs[0] if first_footer.paragraphs else first_footer.add_paragraph()
        ffp.clear()
        ffp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_page_number_field(ffp)


def add_cover_page(doc):
    """Cria a capa do livro."""
    # Espaço superior
    for _ in range(4):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    # Ornamento superior
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=8, line_spacing=1.0)
    add_run_with_style(p_orn, "◆  ◆  ◆", font_name=FONT_SERIF,
                      size=Pt(11), color="B78B37")

    # Título
    for line in BOOK_TITLE.split('\n'):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=2, after=2, line_spacing=1.05)
        add_run_with_style(p, line, font_name=FONT_SERIF,
                          size=Pt(22), bold=True, color="2F2923")

    # Ornamento inferior
    p_orn2 = doc.add_paragraph()
    p_orn2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn2, before=12, after=6, line_spacing=1.0)
    add_run_with_style(p_orn2, "◆", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    # Autores
    for author in AUTHORS:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=4, after=2, line_spacing=1.0)
        add_run_with_style(p, author, font_name=FONT_SERIF,
                          size=Pt(14), color="3A3128", small_caps=True)

    # Ano
    for _ in range(4):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    p_year = doc.add_paragraph()
    p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_year, before=0, after=0, line_spacing=1.0)
    add_run_with_style(p_year, "2026", font_name=FONT_SERIF,
                      size=Pt(12), color="6B6256")


def add_title_page(doc):
    """Folha de rosto (repete capa com dados adicionais da publicação)."""
    # Espaço superior
    for _ in range(3):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    # Autores
    for author in AUTHORS:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=2, after=2, line_spacing=1.0)
        add_run_with_style(p, author, font_name=FONT_SERIF,
                          size=Pt(13), color="3A3128", small_caps=True)

    # Espaço
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=8, line_spacing=1.0)

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=8, line_spacing=1.0)
    add_run_with_style(p_orn, "━━━━  ◆  ━━━━", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    # Título
    for line in BOOK_TITLE.split('\n'):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=2, after=2, line_spacing=1.05)
        add_run_with_style(p, line, font_name=FONT_SERIF,
                          size=Pt(20), bold=True, color="2F2923")

    # Ornamento inferior
    p_orn2 = doc.add_paragraph()
    p_orn2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn2, before=8, after=12, line_spacing=1.0)
    add_run_with_style(p_orn2, "━━━━  ◆  ━━━━", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    # Subtítulo editorial
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_sub, before=4, after=2, line_spacing=1.05)
    add_run_with_style(p_sub, "Doutrina, Jurisprudência e Prática Forense",
                      font_name=FONT_SERIF, size=Pt(11),
                      italic=True, color="6B6256")

    # Edição
    p_ed = doc.add_paragraph()
    p_ed.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_ed, before=8, after=2, line_spacing=1.0)
    add_run_with_style(p_ed, "1a Edição", font_name=FONT_SERIF,
                      size=Pt(10), color="6B6256")

    # Ano
    for _ in range(3):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    p_year = doc.add_paragraph()
    p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_year, before=0, after=0, line_spacing=1.0)
    add_run_with_style(p_year, "2026", font_name=FONT_SERIF,
                      size=Pt(12), color="6B6256")


def add_copyright_page(doc):
    """Página de ficha catalográfica / dados editoriais (verso da folha de rosto)."""

    # Espaço superior (empurrar conteúdo para metade inferior)
    for _ in range(12):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    def _add_line(text, size=Pt(8.5), bold=False, italic=False, center=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p, before=0, after=1.5, line_spacing=1.0)
        add_run_with_style(p, text, font_name=FONT_SERIF, size=size,
                          bold=bold, italic=italic, color="3A3128")

    # Dados catalográficos
    _add_line("KITNER, Claudio; SILVA NETO, Luiz Bispo da.", size=Pt(8.5), bold=True)
    _add_line("Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais /",
              size=Pt(8.5))
    _add_line("Claudio Kitner, Luiz Bispo da Silva Neto. — 1. ed. — 2026.",
              size=Pt(8.5))

    # Espaço
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=4, line_spacing=1.0)

    _add_line("ISBN [a definir]", size=Pt(8.5))

    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=4, line_spacing=1.0)

    _add_line("1. Direito previdenciário — Brasil. 2. Juizados Especiais Federais.",
              size=Pt(8.5))
    _add_line("3. Seguridade social. 4. Benefícios previdenciários. I. Título.",
              size=Pt(8.5))

    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=4, line_spacing=1.0)

    _add_line("CDU 349.3(81)", size=Pt(8.5))
    _add_line("CDD 344.8102", size=Pt(8.5))

    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=8, line_spacing=1.0)

    # Aviso legal
    _add_line("Todos os direitos reservados. Nenhuma parte desta obra pode ser reproduzida,",
              size=Pt(7.5), italic=True)
    _add_line("armazenada ou transmitida por qualquer meio sem autorização prévia dos autores.",
              size=Pt(7.5), italic=True)


def add_dedication_page(doc):
    """Página de dedicatória e epígrafe."""
    # Espaço superior
    for _ in range(8):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    # Dedicatória
    p_ded = doc.add_paragraph()
    p_ded.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_paragraph_spacing(p_ded, before=0, after=4, line_spacing=1.15)
    add_run_with_style(p_ded, "Aos jurisdicionados dos Juizados Especiais Federais,",
                      font_name=FONT_SERIF, size=Pt(10.5),
                      italic=True, color="3A3128")

    p_ded2 = doc.add_paragraph()
    p_ded2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_paragraph_spacing(p_ded2, before=0, after=16, line_spacing=1.15)
    add_run_with_style(p_ded2, "que buscam na Justiça a proteção social que lhes é devida.",
                      font_name=FONT_SERIF, size=Pt(10.5),
                      italic=True, color="3A3128")

    # Espaço antes da epígrafe
    for _ in range(4):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    # Epígrafe
    p_epi = doc.add_paragraph()
    p_epi.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pf = p_epi.paragraph_format
    pf.right_indent = Cm(0.5)
    set_paragraph_spacing(p_epi, before=0, after=4, line_spacing=1.15)
    add_run_with_style(p_epi,
        "A previdência social é a mais importante conquista",
        font_name=FONT_SERIF, size=Pt(9.5), italic=True, color="6B6256")

    p_epi2 = doc.add_paragraph()
    p_epi2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pf2 = p_epi2.paragraph_format
    pf2.right_indent = Cm(0.5)
    set_paragraph_spacing(p_epi2, before=0, after=4, line_spacing=1.15)
    add_run_with_style(p_epi2,
        "do trabalhador no século XX.",
        font_name=FONT_SERIF, size=Pt(9.5), italic=True, color="6B6256")

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pf3 = p_author.paragraph_format
    pf3.right_indent = Cm(0.5)
    set_paragraph_spacing(p_author, before=0, after=0, line_spacing=1.0)
    add_run_with_style(p_author, "— Wladimir Novaes Martinez",
                      font_name=FONT_SERIF, size=Pt(8.5),
                      small_caps=True, color="6B6256")


def add_abbreviations_page(doc):
    """Lista de abreviaturas e siglas usadas na obra."""
    # Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_title, before=16, after=8, line_spacing=1.0)
    add_run_with_style(p_title, "LISTA DE ABREVIATURAS E SIGLAS",
                      font_name=FONT_SERIF, size=Pt(16), bold=True, color="2F2923")

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
    add_run_with_style(p_orn, "━━━━  ◆  ━━━━", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    # Abreviaturas (ordenadas alfabeticamente)
    ABBREVIATIONS = [
        ("ADI", "Ação Direta de Inconstitucionalidade"),
        ("APS", "Agência da Previdência Social"),
        ("BPC", "Benefício de Prestação Continuada"),
        ("CAP", "Caixa de Aposentadorias e Pensões"),
        ("CDA", "Certidão de Dívida Ativa"),
        ("CF/88", "Constituição Federal de 1988"),
        ("CLT", "Consolidação das Leis do Trabalho"),
        ("CNIS", "Cadastro Nacional de Informações Sociais"),
        ("COPES", "Cobertura Previdenciária Estimada"),
        ("CRPS", "Conselho de Recursos da Previdência Social"),
        ("CTC", "Certidão de Tempo de Contribuição"),
        ("DER", "Data de Entrada do Requerimento"),
        ("DIB", "Data de Início do Benefício"),
        ("DID", "Data de Início da Doença"),
        ("DII", "Data de Início da Incapacidade"),
        ("EC", "Emenda Constitucional"),
        ("EPI", "Equipamento de Proteção Individual"),
        ("FUNRURAL", "Fundo de Assistência ao Trabalhador Rural"),
        ("IAP", "Instituto de Aposentadorias e Pensões"),
        ("IF-BrA", "Índice de Funcionalidade Brasileiro Aplicado"),
        ("INPC", "Índice Nacional de Preços ao Consumidor"),
        ("INPS", "Instituto Nacional de Previdência Social"),
        ("INSS", "Instituto Nacional do Seguro Social"),
        ("JEF", "Juizado Especial Federal"),
        ("LC", "Lei Complementar"),
        ("LOAS", "Lei Orgânica da Assistência Social"),
        ("LOPS", "Lei Orgânica da Previdência Social"),
        ("MEI", "Microempreendedor Individual"),
        ("NTEP", "Nexo Técnico Epidemiológico Previdenciário"),
        ("PBC", "Período Básico de Cálculo"),
        ("PPP", "Perfil Profissiográfico Previdenciário"),
        ("RE", "Recurso Extraordinário"),
        ("REsp", "Recurso Especial"),
        ("RGPS", "Regime Geral de Previdência Social"),
        ("RMI", "Renda Mensal Inicial"),
        ("RPPS", "Regime Próprio de Previdência Social"),
        ("RPV", "Requisição de Pequeno Valor"),
        ("SELIC", "Sistema Especial de Liquidação e de Custódia"),
        ("SM", "Salário Mínimo"),
        ("STF", "Supremo Tribunal Federal"),
        ("STJ", "Superior Tribunal de Justiça"),
        ("TNU", "Turma Nacional de Uniformização"),
        ("TRF", "Tribunal Regional Federal"),
    ]

    for abbr, meaning in ABBREVIATIONS:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p, before=0, after=1.5, line_spacing=1.05)
        add_run_with_style(p, abbr, font_name=FONT_SERIF,
                          size=Pt(10), bold=True, color="2F2923")
        add_run_with_style(p, f"  —  {meaning}", font_name=FONT_SERIF,
                          size=Pt(10), color="3A3128")


def add_toc_page(doc):
    """Adiciona página de sumário com campo TOC do Word.
    Insere o campo TOC diretamente no XML — Word COM só precisa atualizar.
    """
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_title, before=16, after=16, line_spacing=1.0)
    add_run_with_style(p_title, "SUMÁRIO", font_name=FONT_SERIF,
                      size=Pt(18), bold=True, color="2F2923")

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
    add_run_with_style(p_orn, "◆", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    # Inserir campo TOC diretamente via XML
    # TOC \o "1-2" captura Heading 1 e Heading 2; \h hyperlinks; \z oculta tabs; \u usa estilos
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(p_toc, before=0, after=0, line_spacing=1.0)

    # fldChar begin
    r_begin = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'  <w:fldChar w:fldCharType="begin"/>'
        f'</w:r>'
    )
    p_toc._element.append(r_begin)

    # instrText com código do campo TOC
    r_instr = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'  <w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText>'
        f'</w:r>'
    )
    p_toc._element.append(r_instr)

    # fldChar separate
    r_sep = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'  <w:fldChar w:fldCharType="separate"/>'
        f'</w:r>'
    )
    p_toc._element.append(r_sep)

    # Texto placeholder (será substituído quando Word atualizar o campo)
    r_text = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'  <w:rPr><w:rFonts w:ascii="{FONT_SERIF}" w:hAnsi="{FONT_SERIF}"/>'
        f'  <w:sz w:val="20"/><w:color w:val="6B6256"/></w:rPr>'
        f'  <w:t>Atualize o sumário para ver as entradas.</w:t>'
        f'</w:r>'
    )
    p_toc._element.append(r_text)

    # fldChar end
    r_end = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'  <w:fldChar w:fldCharType="end"/>'
        f'</w:r>'
    )
    p_toc._element.append(r_end)


def add_part_page(doc, part_num, part_title):
    """Adiciona página divisória de parte."""
    # Espaço superior
    for _ in range(6):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=0, after=0, line_spacing=1.0)

    # Etiqueta PARTE
    p_label = doc.add_paragraph()
    p_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_label, before=0, after=6, line_spacing=1.0)
    add_run_with_style(p_label, f"PARTE {part_num}", font_name=FONT_SANS,
                      size=Pt(10), bold=True, color="8A6A2A", all_caps=True)

    # Usar Heading 1 para o TOC capturar
    # Texto mixed case para TOC legível; all_caps para exibição visual
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.style = doc.styles['Heading 1']
    # Limpar formatação do estilo e aplicar a nossa
    for run in p_title.runs:
        run.clear()
    set_paragraph_spacing(p_title, before=0, after=8, line_spacing=1.05)
    r = add_run_with_style(p_title, part_title, font_name=FONT_SERIF,
                          size=Pt(18), bold=True, color="2F2923",
                          all_caps=True)

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=8, after=0, line_spacing=1.0)
    add_run_with_style(p_orn, "━━━━━  ◆  ◆  ◆  ━━━━━", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")


def add_chapter_to_doc(doc, blocks, cap_num_str):
    """Adiciona um capítulo ao documento unificado."""
    cap_num = cap_num_str
    cap_title = "Título"
    is_first_paragraph = True

    for block in blocks:
        btype = block['type']

        if btype == 'chapter_title':
            # Extrair número e título
            match = re.match(r'Capítulo\s+(\d+)\s*[—–-]\s*(.*)', block['text'])
            if match:
                cap_num = match.group(1)
                cap_title = match.group(2).strip()
            else:
                cap_title = block['text']

            # Etiqueta CAPÍTULO N (decorativa, não é heading)
            p_label = doc.add_paragraph()
            p_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p_label, before=12, after=4, line_spacing=1.0)
            add_run_with_style(p_label, f"CAPÍTULO {cap_num}", font_name=FONT_SANS,
                              size=Pt(9.5), bold=True, color="8A6A2A", all_caps=True)
            keep_with_next(p_label)  # Nunca separar etiqueta do título

            # Título como Heading 2 (para TOC)
            p_title = doc.add_paragraph()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_title.style = doc.styles['Heading 2']
            for run in p_title.runs:
                run.clear()
            set_paragraph_spacing(p_title, before=0, after=8, line_spacing=1.0)
            r_title = add_run_with_style(p_title, cap_title, font_name=FONT_SERIF,
                              size=Pt(20), bold=True, color="2F2923",
                              all_caps=True)
            keep_with_next(p_title)  # Nunca separar título do ornamento

            # Ornamento — filête dourado
            p_orn = doc.add_paragraph()
            p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
            add_run_with_style(p_orn, "━━━━  ◆  ━━━━", font_name=FONT_SERIF,
                              size=Pt(9), color="B78B37")
            is_first_paragraph = True

        elif btype == 'section':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=18, after=7, line_spacing=1.0)
            add_run_with_style(p, block['text'], font_name=FONT_SERIF,
                             size=SIZE_SECTION, bold=True, color="3A3128")
            add_section_border(p)
            keep_with_next(p)
            is_first_paragraph = True

        elif btype == 'subsection':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=13, after=4, line_spacing=1.0)
            add_run_with_style(p, block['text'], font_name=FONT_SERIF,
                             size=SIZE_SUBSECTION, bold=True, color="3A3128")
            keep_with_next(p)
            is_first_paragraph = True

        elif btype == 'box':
            add_box(doc, block['box_type'], block['text'])
            is_first_paragraph = True

        elif btype == 'table':
            add_table_block(doc, block['headers'], block['rows'])
            is_first_paragraph = True

        elif btype == 'list':
            items = block['items']
            ordered = block['ordered']
            for idx, item_text in enumerate(items, 1):
                add_list_item(doc, item_text, ordered=ordered, number=idx)
            p_after = doc.add_paragraph()
            set_paragraph_spacing(p_after, before=0, after=3, line_spacing=1.0)
            is_first_paragraph = True

        elif btype == 'blockquote':
            add_blockquote(doc, block['text'])
            is_first_paragraph = True

        elif btype == 'table_note':
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=0, after=3, line_spacing=1.0)
            add_run_with_style(p, block['text'], font_name=FONT_SERIF,
                             size=Pt(8.5), italic=True, color="6B6256")

        elif btype == 'references_heading':
            p_break = doc.add_paragraph()
            run = p_break.add_run()
            run.add_break(WD_BREAK.PAGE)

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p, before=16, after=5, line_spacing=1.0)
            add_run_with_style(p, "REFERÊNCIAS", font_name=FONT_SERIF,
                             size=Pt(12.2), bold=True, color="3A3128",
                             small_caps=True)

        elif btype == 'reference_entry':
            p = add_paragraph_with_bold(doc, block['text'],
                                       size=Pt(9.4), color="201B16",
                                       alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                       first_indent=0, space_before=0,
                                       space_after=2.4, line_spacing=1.0)
            pf = p.paragraph_format
            pf.left_indent = Cm(0.48)
            pf.first_line_indent = Cm(-0.48)

        elif btype == 'paragraph':
            if is_first_paragraph:
                add_drop_cap(doc, block['text'])
            else:
                add_paragraph_with_bold(doc, block['text'], first_indent=0.42)
            is_first_paragraph = False

    return cap_num, cap_title


def _add_backmatter_section(doc, title, index_leg, index_sum, index_inst):
    """Adiciona seção de índice remissivo ao documento."""
    from docx.enum.text import WD_BREAK

    # Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_title, before=16, after=8, line_spacing=1.0)
    add_run_with_style(p_title, title, font_name=FONT_SERIF,
                      size=Pt(18), bold=True, color="2F2923")

    # Ornamento
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
    add_run_with_style(p_orn, "◆", font_name=FONT_SERIF,
                      size=Pt(9), color="B78B37")

    def _add_index_category(category_title, index_dict):
        if not index_dict:
            return
        # Subtítulo da categoria
        p_cat = doc.add_paragraph()
        p_cat.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(p_cat, before=12, after=4, line_spacing=1.0)
        add_run_with_style(p_cat, category_title, font_name=FONT_SERIF,
                          size=Pt(12), bold=True, color="3A3128")
        add_section_border(p_cat, color_hex="D7CDBB")

        # Entradas, duas colunas via tab stops
        for term in sorted(index_dict.keys(), key=str.lower):
            caps = sorted(index_dict[term], key=lambda x: int(x) if x.isdigit() else 0)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before=0, after=1.5, line_spacing=1.0)

            add_run_with_style(p, term, font_name=FONT_SERIF,
                              size=Pt(9.4), color="201B16")
            add_run_with_style(p, f"  Cap. {', '.join(caps)}",
                              font_name=FONT_SERIF,
                              size=Pt(9.4), color="6B6256")

    _add_index_category("Legislação", index_leg)
    _add_index_category("Súmulas e Temas Repetitivos", index_sum)
    _add_index_category("Institutos Jurídicos", index_inst)


def create_unified_docx(output_path):
    """Cria o DOCX unificado com todos os capítulos."""
    doc = Document()

    # Configurar estilo Normal (corpo)
    apply_normal_style(doc)

    # Configurar Heading 1 (Partes) — aparece no TOC nível 1
    h1 = doc.styles['Heading 1']
    h1.font.name = FONT_SERIF
    h1.font.size = Pt(18)
    h1.font.bold = True
    h1.font.color.rgb = hex_to_rgb("2F2923")
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(8)

    # Configurar Heading 2 (Capítulos) — aparece no TOC nível 2
    h2 = doc.styles['Heading 2']
    h2.font.name = FONT_SERIF
    h2.font.size = Pt(20)
    h2.font.bold = True
    h2.font.color.rgb = hex_to_rgb("2F2923")
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h2.paragraph_format.space_before = Pt(0)
    h2.paragraph_format.space_after = Pt(8)

    # Configurar TOC styles para formatação hierárquica
    try:
        toc1 = doc.styles['TOC 1'] if 'TOC 1' in [s.name for s in doc.styles] else None
        if toc1:
            toc1.font.name = FONT_SERIF
            toc1.font.size = Pt(11)
            toc1.font.bold = True
            toc1.font.color.rgb = hex_to_rgb("2F2923")
            toc1.paragraph_format.space_before = Pt(8)
            toc1.paragraph_format.space_after = Pt(2)

        toc2 = doc.styles['TOC 2'] if 'TOC 2' in [s.name for s in doc.styles] else None
        if toc2:
            toc2.font.name = FONT_SERIF
            toc2.font.size = Pt(10)
            toc2.font.bold = False
            toc2.font.color.rgb = hex_to_rgb("3A3128")
            toc2.paragraph_format.space_before = Pt(1)
            toc2.paragraph_format.space_after = Pt(1)
            toc2.paragraph_format.left_indent = Cm(0.5)
    except Exception as e:
        print(f"  Aviso: não foi possível configurar estilos TOC: {e}")

    # Mirror margins no documento
    settings = doc.settings.element
    mirror = settings.find(qn('w:mirrorMargins'))
    if mirror is None:
        mirror = parse_xml(f'<w:mirrorMargins {nsdecls("w")} w:val="1"/>')
        settings.append(mirror)

    # Habilitar cabeçalhos par/ímpar distintos
    eoh = settings.find(qn('w:evenAndOddHeaders'))
    if eoh is None:
        eoh = parse_xml(f'<w:evenAndOddHeaders {nsdecls("w")}/>')
        settings.append(eoh)

    # Hifenização automática (evita rios brancos em A5 justificado)
    _enable_auto_hyphenation(doc)
    # Compatibilidade para justificação aprimorada
    _set_compat_settings(doc)
    # Namespace w14 para ligaduras OpenType
    _enable_w14_namespace(doc)

    # ── CAPA ──
    section0 = doc.sections[0]
    setup_section(section0, is_first=True)
    # Sem cabeçalho/rodapé na capa
    section0.different_first_page_header_footer = True
    for h in [section0.header, section0.first_page_header, section0.even_page_header]:
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.clear()
    for f in [section0.footer, section0.first_page_footer, section0.even_page_footer]:
        f.is_linked_to_previous = False
        for p in f.paragraphs:
            p.clear()

    add_cover_page(doc)

    # Paginação romana para pré-textual (capa até lista de abreviaturas)
    sectPr0 = section0._sectPr
    pgNumType0 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
    sectPr0.append(pgNumType0)

    # ── FOLHA DE ROSTO ──
    sec_title = add_new_section(doc)
    # Sem header/footer na folha de rosto
    sec_title.different_first_page_header_footer = True
    for h in [sec_title.header, sec_title.first_page_header, sec_title.even_page_header]:
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.clear()
    for f in [sec_title.footer, sec_title.first_page_footer, sec_title.even_page_footer]:
        f.is_linked_to_previous = False
        for p in f.paragraphs:
            p.clear()
    # Manter romano
    sectPrTitle = sec_title._sectPr
    pgNumTypeTitle = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>')
    sectPrTitle.append(pgNumTypeTitle)
    add_title_page(doc)

    # ── FICHA CATALOGRÁFICA (verso da folha de rosto) ──
    sec_copy = add_new_section(doc)
    sec_copy.different_first_page_header_footer = True
    for h in [sec_copy.header, sec_copy.first_page_header, sec_copy.even_page_header]:
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.clear()
    for f in [sec_copy.footer, sec_copy.first_page_footer, sec_copy.even_page_footer]:
        f.is_linked_to_previous = False
        for p in f.paragraphs:
            p.clear()
    sectPrCopy = sec_copy._sectPr
    pgNumTypeCopy = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>')
    sectPrCopy.append(pgNumTypeCopy)
    add_copyright_page(doc)

    # ── DEDICATÓRIA E EPÍGRAFE ──
    sec_ded = add_new_section(doc)
    sec_ded.different_first_page_header_footer = True
    for h in [sec_ded.header, sec_ded.first_page_header, sec_ded.even_page_header]:
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.clear()
    for f in [sec_ded.footer, sec_ded.first_page_footer, sec_ded.even_page_footer]:
        f.is_linked_to_previous = False
        for p in f.paragraphs:
            p.clear()
    sectPrDed = sec_ded._sectPr
    pgNumTypeDed = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>')
    sectPrDed.append(pgNumTypeDed)
    add_dedication_page(doc)

    # ── LISTA DE ABREVIATURAS ──
    sec_abbr = add_new_section(doc)
    setup_header_footer(sec_abbr, header_text="Lista de Abreviaturas",
                       first_page_no_header=True)
    sectPrAbbr = sec_abbr._sectPr
    pgNumTypeAbbr = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>')
    sectPrAbbr.append(pgNumTypeAbbr)
    add_abbreviations_page(doc)

    # ── SUMÁRIO ──
    sec_toc = add_new_section(doc)
    setup_header_footer(sec_toc, header_text="Sumário", first_page_no_header=True)
    # Manter paginação romana no sumário
    sectPrToc = sec_toc._sectPr
    pgNumTypeToc = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman"/>')
    sectPrToc.append(pgNumTypeToc)
    add_toc_page(doc)

    # ── CAPÍTULOS ──
    base_dir = Path(__file__).parent.parent / "output" / "rascunhos"

    is_first_part = True

    for part in PARTS:
        # Página divisória da Parte (sempre em página ímpar)
        sec_part = add_new_section(doc, start_type='ODD_PAGE')
        setup_header_footer(sec_part, header_text=f"Parte {part['num']}",
                          first_page_no_header=True)

        # Iniciar paginação arábica na primeira Parte (página 1)
        if is_first_part:
            sectPrPart = sec_part._sectPr
            pgNumTypePart = parse_xml(
                f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>'
            )
            sectPrPart.append(pgNumTypePart)
            is_first_part = False

        add_part_page(doc, part['num'], part['title'])

        for cap_id in part['chapters']:
            md_path = base_dir / f"cap_{cap_id}_rascunho.md"
            if not md_path.exists():
                print(f"  AVISO: {md_path} nao encontrado, pulando...")
                continue

            print(f"  Processando Cap. {cap_id}...")

            # Ler e processar
            text = md_path.read_text(encoding='utf-8')
            text = strip_citations(text)
            blocks = parse_markdown(text)

            # Nova seção para o capítulo
            sec_cap = add_new_section(doc)

            # Extrair título do capítulo ANTES de inserir conteúdo
            cap_num_preview = cap_id
            cap_title_preview = "Título"
            for blk in blocks:
                if blk['type'] == 'chapter_title':
                    m = re.match(r'Capítulo\s+(\d+)\s*[—–-]\s*(.*)', blk['text'])
                    if m:
                        cap_num_preview = m.group(1)
                        cap_title_preview = m.group(2).strip()
                    break

            # Configurar header ANTES do conteúdo (fix: evita header errado)
            setup_header_footer(sec_cap,
                              header_text=f"Capítulo {cap_num_preview}  |  {cap_title_preview}",
                              first_page_no_header=True)

            # Adicionar conteúdo
            cap_num, cap_title = add_chapter_to_doc(doc, blocks, cap_id)

    # ── ÍNDICE REMISSIVO ──
    print("  Gerando indice remissivo...")
    try:
        from gerar_indice_referencias import build_remissive_index
        index_leg, index_sum, index_inst = build_remissive_index(base_dir)
        if any([index_leg, index_sum, index_inst]):
            sec_idx = add_new_section(doc, start_type='ODD_PAGE')
            setup_header_footer(sec_idx, header_text="Índice Remissivo",
                              first_page_no_header=True)
            _add_backmatter_section(doc, "ÍNDICE REMISSIVO",
                                   index_leg, index_sum, index_inst)
            print(f"    {len(index_leg)} leis, {len(index_sum)} sumulas, "
                  f"{len(index_inst)} institutos")
    except Exception as e:
        print(f"  Aviso indice: {e}")

    # Metadados
    core = doc.core_properties
    core.title = "Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais"
    core.subject = "Direito Previdenciário"
    core.author = "Claudio Kitner; Luiz Bispo da Silva Neto"

    doc.save(output_path)
    return output_path


def _convert_via_word(docx_path, pdf_path):
    """Conversão via Word COM: abre DOCX, atualiza campos (TOC), exporta PDF."""
    import win32com.client
    import pythoncom
    import time

    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        try:
            word.Visible = True
        except Exception:
            pass  # Alguns contextos bloqueiam Visible; Word funciona mesmo assim
        try:
            word.DisplayAlerts = 0  # wdAlertsNone
        except Exception:
            pass

        docx_abs = os.path.abspath(docx_path)
        pdf_abs = os.path.abspath(pdf_path)

        print(f"  Abrindo no Word: {docx_abs}")
        doc = word.Documents.Open(docx_abs, ReadOnly=False)

        # Forçar modo Print View (essencial para paginação correta)
        print("  Configurando Print View...")
        try:
            word.ActiveWindow.View.Type = 3  # wdPrintView
        except Exception as e:
            print(f"  Aviso view: {e}")

        print("  Aguardando carregamento completo...")
        time.sleep(5)

        # Forçar paginação: navegar ao final e voltar
        print("  Forçando paginação completa...")
        try:
            word.Selection.EndKey(Unit=6)  # wdStory = 6
            time.sleep(8)
            word.Selection.HomeKey(Unit=6)
            time.sleep(3)
            doc.Repaginate()
            time.sleep(5)
            pages = doc.ComputeStatistics(2)  # wdStatisticPages
            print(f"  Páginas detectadas: {pages}")
        except Exception as e:
            print(f"  Aviso paginação: {e}")

        # Atualizar todos os campos do documento (TOC, PAGE, etc.)
        print("  Atualizando todos os campos...")
        try:
            # Atualizar campos no corpo do documento
            for field in doc.Fields:
                field.Update()
            print(f"  {doc.Fields.Count} campos atualizados")
        except Exception as e:
            print(f"  Aviso fields: {e}")

        time.sleep(3)

        # Atualizar TOC especificamente (garante números de página corretos)
        print("  Atualizando TOC...")
        try:
            tc = doc.TablesOfContents
            if tc.Count > 0:
                for i in range(1, tc.Count + 1):
                    tc.Item(i).Update()
                print(f"  {tc.Count} TOC(s) atualizado(s)")
            else:
                print("  Nenhum TOC encontrado — tentando via campos...")
                # Fallback: atualizar via seleção de todos os campos
                doc.Content.Select()
                word.Selection.Fields.Update()
        except Exception as e:
            print(f"  Aviso TOC update: {e}")

        time.sleep(3)

        # Repaginar final
        doc.Repaginate()
        time.sleep(3)

        # Verificação final
        try:
            pages = doc.ComputeStatistics(2)
            print(f"  Páginas finais: {pages}")
        except:
            pass

        # Exportar como PDF
        print(f"  Exportando PDF: {pdf_abs}")
        doc.ExportAsFixedFormat(
            OutputFileName=pdf_abs,
            ExportFormat=17,  # wdExportFormatPDF
            OpenAfterExport=False,
            OptimizeFor=0,    # wdExportOptimizeForPrint
            Range=0,          # wdExportAllPages
            Item=0,           # wdExportDocumentContent
            IncludeDocProps=True,
            CreateBookmarks=1  # wdExportCreateHeadingBookmarks
        )
        print("  PDF exportado!")

        time.sleep(3)
        doc.Close(SaveChanges=False)
        print("  PDF gerado com sucesso via Word COM!")

    finally:
        if word:
            try:
                word.Quit()
            except:
                pass
        pythoncom.CoUninitialize()


def _convert_via_libreoffice(docx_path, pdf_path):
    """Conversão fallback via LibreOffice headless (sem TOC dinâmico)."""
    import subprocess
    import shutil

    soffice = shutil.which("soffice")
    if not soffice:
        # Tentar caminhos comuns no Windows
        for candidate in [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]:
            if os.path.isfile(candidate):
                soffice = candidate
                break

    if not soffice:
        raise FileNotFoundError(
            "LibreOffice nao encontrado. Instale o LibreOffice ou "
            "corrija a conversao via Word COM."
        )

    print(f"  Usando LibreOffice: {soffice}")
    out_dir = os.path.dirname(os.path.abspath(pdf_path))

    result = subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf",
         "--outdir", out_dir, os.path.abspath(docx_path)],
        capture_output=True, text=True, timeout=300
    )

    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice falhou: {result.stderr}")

    # LibreOffice gera com mesmo nome mas extensão .pdf
    generated = os.path.splitext(os.path.abspath(docx_path))[0] + ".pdf"
    target = os.path.abspath(pdf_path)
    if generated != target and os.path.isfile(generated):
        shutil.move(generated, target)

    print(f"  PDF gerado via LibreOffice (TOC pode nao estar atualizado)")


def _convert_via_powershell(docx_path, pdf_path):
    """Conversão via PowerShell COM (fallback quando Python COM falha)."""
    import subprocess

    docx_abs = os.path.abspath(docx_path)
    pdf_abs = os.path.abspath(pdf_path)

    ps_script = f'''
$word = New-Object -ComObject Word.Application
$word.Visible = $true
$word.DisplayAlerts = 0
$doc = $word.Documents.Open("{docx_abs}")
$word.ActiveWindow.View.Type = 3
Start-Sleep -Seconds 5
$word.Selection.EndKey(6) | Out-Null
Start-Sleep -Seconds 8
$word.Selection.HomeKey(6) | Out-Null
Start-Sleep -Seconds 3
$doc.Repaginate()
Start-Sleep -Seconds 5
$doc.Fields | ForEach-Object {{ $_.Update() }}
$tc = $doc.TablesOfContents
if ($tc.Count -gt 0) {{
    for ($i = 1; $i -le $tc.Count; $i++) {{ $tc.Item($i).Update() }}
}}
Start-Sleep -Seconds 3
$doc.Repaginate()
Start-Sleep -Seconds 3
$pages = $doc.ComputeStatistics(2)
Write-Output "Paginas: $pages"
$doc.ExportAsFixedFormat("{pdf_abs}", 17, $false, 0, 0, 1, 1, 0, $true, $true, 1)
Write-Output "PDF exportado"
$doc.Close(0)
$word.Quit()
'''
    print("  Convertendo via PowerShell COM...")
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_script],
        capture_output=True, text=True, timeout=600
    )
    output = result.stdout.strip()
    if output:
        for line in output.split('\n'):
            print(f"  {line.strip()}")
    if result.returncode != 0:
        raise RuntimeError(f"PowerShell COM falhou: {result.stderr.strip()}")
    if not os.path.isfile(pdf_abs):
        raise RuntimeError("PDF nao foi gerado")
    print("  PDF gerado com sucesso via PowerShell COM!")


def convert_to_pdf(docx_path, pdf_path):
    """Converte DOCX para PDF. Tenta Word COM, depois PowerShell COM, depois LibreOffice."""
    word_error = None

    # Método 1: Word COM via Python (preferido — atualiza TOC)
    try:
        _convert_via_word(docx_path, pdf_path)
        return
    except Exception as e:
        word_error = str(e)
        print(f"\n  AVISO: Word COM (Python) falhou: {word_error}")
        print("  Tentando via PowerShell COM...")

    # Método 2: Word COM via PowerShell (funciona em mais contextos)
    try:
        _convert_via_powershell(docx_path, pdf_path)
        return
    except Exception as e:
        ps_error = str(e)
        print(f"\n  AVISO: PowerShell COM falhou: {ps_error}")
        print("  Tentando fallback via LibreOffice...")

    # Método 3: LibreOffice headless
    try:
        _convert_via_libreoffice(docx_path, pdf_path)
    except Exception as e2:
        print(f"  ERRO: LibreOffice tambem falhou: {e2}")
        raise RuntimeError(
            f"Nenhum metodo de conversao disponivel. "
            f"Word: {word_error} | LibreOffice: {e2}"
        )


def main():
    project_dir = Path(__file__).parent.parent
    output_dir = project_dir / "output"
    output_dir.mkdir(exist_ok=True)

    docx_path = output_dir / "livro_completo.docx"
    pdf_path = output_dir / "livro_completo.pdf"

    print("=" * 60)
    print("GERANDO LIVRO COMPLETO")
    print("=" * 60)

    print("\n1. Criando DOCX unificado...")
    create_unified_docx(str(docx_path))
    print(f"  DOCX salvo: {docx_path}")

    print("\n2. Convertendo para PDF via Word...")
    convert_to_pdf(str(docx_path), str(pdf_path))

    print("\n" + "=" * 60)
    print(f"CONCLUIDO: {pdf_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()
