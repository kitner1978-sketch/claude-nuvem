#!/usr/bin/env python3
"""Gera a Proposta de Divisão Editorial em DOCX, reusando o Design Code do livro."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT

from design_code import COLORS, FONT_SERIF, FONT_SANS, hex_to_rgb, add_page_field
from md_to_docx import (add_run_with_style, add_table_block, add_paragraph_with_bold,
                        add_box, add_section_border, set_paragraph_spacing, apply_normal_style)


def a4(section):
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.4)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.6)
    section.right_margin = Cm(2.6)
    section.header_distance = Cm(1.2)
    section.footer_distance = Cm(1.1)


def label(doc, text):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=2, after=2, line_spacing=1.0)
    add_run_with_style(p, text, font_name=FONT_SANS, size=Pt(8.5), bold=True,
                       color=COLORS['gold_dark'], all_caps=True)
    return p


def h1(doc, text, num=None):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=20, after=6, line_spacing=1.0)
    if num:
        add_run_with_style(p, f'{num}  ', font_name=FONT_SANS, size=Pt(13),
                           bold=True, color=COLORS['gold_accent'])
    add_run_with_style(p, text, font_name=FONT_SERIF, size=Pt(15.5), bold=True,
                       color=COLORS['heading_text'])
    add_section_border(p, color_hex=COLORS['gold_accent'])
    return p


def body(doc, text, after=6):
    p = add_paragraph_with_bold(doc, text, size=Pt(11), color=COLORS['body_text'],
                                first_indent=0, space_before=0, space_after=after,
                                line_spacing=1.18)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def bullet(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(p, before=0, after=3, line_spacing=1.15)
    pf = p.paragraph_format
    pf.left_indent = Cm(0.6); pf.first_line_indent = Cm(-0.45)
    add_run_with_style(p, '◆  ', font_name=FONT_SERIF, size=Pt(8), color=COLORS['gold_accent'])
    for seg, b, i in __import__('md_to_docx')._parse_inline_formatting(text):
        if seg:
            add_run_with_style(p, seg, font_name=FONT_SERIF, size=Pt(11), bold=b,
                               italic=i, color=COLORS['body_text'])
    return p


def proscons(doc, pros, contras):
    for lbl, txt, col in (('Prós', pros, COLORS['box_pratica_accent']),
                          ('Contras', contras, COLORS['box_atencao_accent'])):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_paragraph_spacing(p, before=2, after=3, line_spacing=1.15)
        add_run_with_style(p, f'{lbl}.  ', font_name=FONT_SANS, size=Pt(9.5),
                           bold=True, color=col)
        for seg, b, i in __import__('md_to_docx')._parse_inline_formatting(txt):
            if seg:
                add_run_with_style(p, seg, font_name=FONT_SERIF, size=Pt(10.7),
                                   italic=i or True, color=COLORS['muted_text'])


def main():
    out = Path(__file__).parent.parent / 'output' / 'Proposta_Divisao_Editorial.docx'
    doc = Document()
    apply_normal_style(doc)
    a4(doc.sections[0])

    # Rodapé com nº de página
    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(fp, font_name=FONT_SERIF, size=Pt(9), color=COLORS['muted_text'])

    # ── Cabeçalho do documento ──────────────────────────────
    label(doc, 'Proposta Editorial · Junho de 2026')
    pt = doc.add_paragraph()
    set_paragraph_spacing(pt, before=2, after=2, line_spacing=1.05)
    add_run_with_style(pt, 'Divisão da Obra em Volumes', font_name=FONT_SERIF,
                       size=Pt(26), bold=True, color=COLORS['title_text'])
    psub = doc.add_paragraph()
    set_paragraph_spacing(psub, before=0, after=2, line_spacing=1.15)
    add_run_with_style(psub, 'Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais',
                       font_name=FONT_SERIF, size=Pt(12.5), italic=True, color=COLORS['muted_text'])
    porn = doc.add_paragraph()
    set_paragraph_spacing(porn, before=4, after=10, line_spacing=1.0)
    add_run_with_style(porn, '━━━━  ◆  ━━━━', font_name=FONT_SERIF, size=Pt(10),
                       color=COLORS['gold_accent'])
    body(doc, 'Três cenários para fracionar a obra — hoje com **1.342 páginas de conteúdo** '
              '(1.359 no PDF, já com pré-textuais e índice) — em volumes de **até 250 páginas**, '
              'preservando a coerência didática e a identidade visual da coleção.')

    # ── 1. Premissas ────────────────────────────────────────
    h1(doc, 'Premissas do fracionamento', '1')
    body(doc, 'Qualquer divisão observa três condicionantes objetivas:')
    bullet(doc, '**Orçamento real de ~235 páginas de conteúdo por volume** — cada volume '
                'carrega capa, ficha catalográfica, sumário e, idealmente, índice próprios '
                '(8–12 páginas de pré-textual e pós-textual).')
    bullet(doc, '**As seis Partes da obra não servem de corte direto:** as Partes I (285 pp), '
                'III (309 pp) e IV (343 pp) já excedem, sozinhas, o teto de 250.')
    bullet(doc, '**Piso de 7 volumes** — como os capítulos (31 a 89 pp) permanecem inteiros e '
                'em sequência de leitura, o empacotamento real não comporta menos do que isso.')
    body(doc, '', after=2)

    add_table_block(doc,
        ['Parte', 'Capítulos', 'Páginas'],
        [['I — Fundamentos do RGPS', '1 a 5', '285'],
         ['II — Benefícios por Incapacidade', '6 a 7', '87'],
         ['III — Aposentadorias Programadas', '8 a 12', '309'],
         ['IV — Pensões, Auxílios e BPC', '13 a 18', '343'],
         ['V — Temas Transversais', '19 a 21', '177'],
         ['VI — Processo nos JEFs', '22 a 23', '141'],
         ['Total da obra', '1 a 23', '1.342']])

    # ── 2. Cenário 1 ────────────────────────────────────────
    h1(doc, 'Cenário 1 — Sete volumes equilibrados', '2')
    body(doc, 'Prioriza o **menor número de livros** com tamanhos semelhantes (141 a 220 páginas). '
              'É a divisão mais econômica em capas, ISBN e índices.')
    add_table_block(doc,
        ['Vol.', 'Caps.', 'Págs.', 'Título sugerido'],
        [['I', '1–4', '214', 'Fundamentos, Princípios e Custeio do RGPS'],
         ['II', '5–8', '210', 'Tempo de Contribuição, Incapacidade e Aposentadoria Especial'],
         ['III', '9–11', '185', 'Aposentadorias Rural, Programada e por Tempo de Contribuição'],
         ['IV', '12–14', '195', 'PcD, Salário-Maternidade e Auxílio-Reclusão'],
         ['V', '15–18', '220', 'Auxílio-Acidente, Cálculo, Revisão e BPC'],
         ['VI', '19–21', '177', 'Pensão por Morte, Acumulação e Decadência/Prescrição'],
         ['VII', '22–23', '141', 'Processo Administrativo e Procedimento nos JEFs']])
    proscons(doc,
        'menos livros e custo fixo menor; volumes de tamanho parecido.',
        'algumas costuras temáticas — o Vol. II reúne tempo de contribuição, incapacidade e '
        'aposentadoria especial; o Vol. V agrupa quatro temas distintos.')

    # ── 3. Cenário 2 ────────────────────────────────────────
    h1(doc, 'Cenário 2 — Nove volumes modulares', '3')
    body(doc, 'Cada volume corresponde a uma **família de benefícios fechada**, o que favorece a '
              '**venda avulsa** e o uso como **módulos de curso**.')
    add_table_block(doc,
        ['Vol.', 'Caps.', 'Págs.', 'Título sugerido'],
        [['1', '1–3', '125', 'Fundamentos: História, Princípios, Segurados e Carência'],
         ['2', '4–5', '160', 'Custeio e Tempo de Contribuição'],
         ['3', '6–7', '87', 'Benefícios por Incapacidade'],
         ['4', '8–9', '107', 'Aposentadoria Especial e Rural'],
         ['5', '10–12', '202', 'Aposentadorias Programada, por TC e da PcD'],
         ['6', '13–15', '173', 'Salário-Maternidade, Auxílio-Reclusão e Auxílio-Acidente'],
         ['7', '16–18', '170', 'Cálculo do Benefício, Revisão e BPC'],
         ['8', '19–21', '177', 'Temas Transversais'],
         ['9', '22–23', '141', 'Processo Previdenciário nos JEFs']])
    proscons(doc,
        'identidade temática nítida por volume; ótimo para coleção vendida por assunto e para cursos.',
        'mais livros, alguns finos (87 a 125 pp); maior custo fixo (capa, ISBN e índice por volume).')

    # ── 4. Cenário 3 ────────────────────────────────────────
    h1(doc, 'Cenário 3 — Coleção em duas obras, por finalidade', '4')
    body(doc, 'Separa a **teoria e os benefícios** da **prática processual**, criando um manual de '
              'foro autônomo. São duas obras-mãe com identidades próprias.')
    label(doc, 'Obra A — Direito Previdenciário: Fundamentos e Benefícios (caps. 1–21) · 6 tomos')
    add_table_block(doc,
        ['Tomo', 'Caps.', 'Págs.', 'Conteúdo'],
        [['I', '1–4', '214', 'Fundamentos, Princípios e Custeio'],
         ['II', '5–8', '210', 'Tempo de Contribuição, Incapacidade e Especial'],
         ['III', '9–11', '185', 'Aposentadorias Rural, Programada e por TC'],
         ['IV', '12–15', '245', 'PcD, Maternidade, Reclusão e Auxílio-Acidente'],
         ['V', '16–18', '170', 'Cálculo, Revisão e BPC'],
         ['VI', '19–21', '177', 'Temas Transversais']])
    label(doc, 'Obra B — Prática Processual Previdenciária nos JEFs (caps. 22–23) · volume único')
    add_table_block(doc,
        ['Volume', 'Caps.', 'Págs.', 'Conteúdo'],
        [['Único', '22–23', '141', 'Processo Administrativo e Procedimento nos JEFs']])
    proscons(doc,
        'a Obra B é um manual de prática vendável isoladamente ao advogado litigante; a Obra A '
        'é o tratado doutrinário em tomos, com marca própria.',
        'o tratado ainda exige 6 tomos; o Tomo IV fica no limite (245 pp), com pouca folga.')

    # ── 5. Considerações comuns ─────────────────────────────
    h1(doc, 'Considerações válidas para qualquer cenário', '5')
    add_box(doc, 'box-atencao',
        '**O fracionamento exige trabalho editorial além do simples recorte:**\n\n'
        '- **363 remissões cruzadas** ("v. Cap. X") no texto. Ao dividir, muitas passam a apontar '
        'para outro volume ("v. Vol. III, Cap. 9"): é preciso um passe de reescrita das remissões '
        'e a definição da nomenclatura (Volume ou Tomo).\n'
        '- **Pré-textuais e ISBN por volume** — cada livro recebe capa, ficha catalográfica e ISBN '
        'próprios; a coleção pode ter, ainda, um ISBN de coleção.\n'
        '- **Índice remissivo** — um por volume (mais útil ao leitor) ou um consolidado no volume final.\n'
        '- **Recapitulações** — conceitos-base (tempus regit actum, arquitetura da EC 103/2019) '
        'pedem breve retomada nos volumes que os empregam sem o volume de fundamentos à mão.')

    # ── 6. Esforço estimado ─────────────────────────────────
    h1(doc, 'Esforço estimado da divisão', '6')
    body(doc, 'A divisão é, em boa parte, **automatizável pelo próprio pipeline da obra** — recorte '
              'dos capítulos, geração dos pré-textuais, do índice remissivo e dos arquivos PDF/DOCX '
              'por volume. O esforço irredutível concentra-se na **reescrita das remissões** e em '
              'breves **recapitulações autorais**.')
    body(doc, 'Das remissões cruzadas, cerca de **160 apontam para um único capítulo** e formam o '
              'núcleo do trabalho. A medição por cenário mostra quantas passam a **cruzar fronteiras '
              'de volume** — quanto menos, menor o retrabalho:')
    add_table_block(doc,
        ['Cenário', 'Volumes', 'Remissões entre volumes', 'Esforço relativo'],
        [['1 — equilibrado', '7', '102  (63%)', 'Médio'],
         ['2 — modular', '9', '93  (58%)', 'Médio — menos remissões, mais pré-textuais'],
         ['3 — duas obras', '7', '102  (63%)', 'Médio']])
    body(doc, 'O **Cenário 2**, embora tenha mais volumes, é o que **menos fragmenta as remissões**, '
              'porque mantém juntos os capítulos que mais se citam (incapacidade, caps. 6–7; cálculo, '
              'revisão e BPC, caps. 16–18). Já os **pré-textuais e índices** escalam com o número de '
              'volumes — ponto em que o Cenário 2 é o mais intensivo.', after=4)
    bullet(doc, '**Recorte e geração por volume** — automatável pelo pipeline existente.')
    bullet(doc, '**Pré-textuais e índice por volume** — automatáveis; o custo cresce com o nº de volumes.')
    bullet(doc, '**Reescrita das remissões entre volumes** — semiautomatável (detecção por script + '
                'revisão humana dos casos de faixa e dos ambíguos).')
    bullet(doc, '**Recapitulações de conceitos-base** — trabalho autoral, poucas por volume.')
    bullet(doc, '**ISBN por volume** (e eventual ISBN de coleção) — providência junto à editora.')
    body(doc, '_Em síntese: recorte, pré-textuais, índices e a maior parte das remissões podem ser '
              'entregues em poucas sessões de trabalho automatizado; o tempo de calendário é dominado '
              'pela revisão humana das remissões e pelas recapitulações._', after=4)

    # ── 7. Recomendação ─────────────────────────────────────
    h1(doc, 'Recomendação', '7')
    body(doc, 'Para uma coleção com **apelo comercial e autonomia de cada título**, recomendam-se o '
              '**Cenário 2** (modular, vendável por assunto) ou o **Cenário 3** (manual de prática '
              'destacado do tratado). O **Cenário 1** é preferível se a prioridade for **reduzir custos '
              'e o número de volumes**. Em todos eles, o passe de remissões cruzadas é a etapa crítica '
              'e deve preceder a diagramação final.')

    doc.save(str(out))
    print('OK:', out)
    return str(out)


if __name__ == '__main__':
    main()
