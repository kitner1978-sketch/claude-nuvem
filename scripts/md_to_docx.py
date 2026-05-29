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
from lxml import etree
import copy

# Namespace Word 2010+ (ligaduras OpenType, efeitos de texto avançados)
W14_NS = 'http://schemas.microsoft.com/office/word/2010/wordml'
MC_NS = 'http://schemas.openxmlformats.org/markup-compatibility/2006'


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
    "box_quadro_bg":       "F5F3EF",
    "box_quadro_accent":   "6B6256",
    "box_quadro_border":   "A09882",
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

        # Tabela markdown: | col1 | col2 |
        if stripped.startswith('|'):
            table_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            # Parse: primeira linha = headers, pular separador, resto = dados
            headers = [c.strip() for c in table_lines[0].strip('|').split('|')]
            data_rows = []
            for tl in table_lines[1:]:
                # Pular linha separadora (|---|---|)
                if re.match(r'^[\|\s\-:]+$', tl):
                    continue
                cells = [c.strip() for c in tl.strip('|').split('|')]
                data_rows.append(cells)
            blocks.append({'type': 'table', 'headers': headers, 'rows': data_rows})
            continue

        # Lista não-ordenada: - item
        if stripped.startswith('- '):
            list_items = []
            while i < len(lines):
                item_line = lines[i].strip()
                if item_line.startswith('- '):
                    list_items.append(item_line[2:])
                elif item_line == '':
                    break
                else:
                    break
                i += 1
            blocks.append({'type': 'list', 'items': list_items, 'ordered': False})
            continue

        # Lista ordenada: 1. item
        ord_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if ord_match:
            list_items = []
            while i < len(lines):
                item_line = lines[i].strip()
                om = re.match(r'^\d+\.\s+(.+)', item_line)
                if om:
                    list_items.append(om.group(1))
                elif item_line == '':
                    break
                else:
                    break
                i += 1
            blocks.append({'type': 'list', 'items': list_items, 'ordered': True})
            continue

        # Nota de tabela: *texto sem fechamento de itálico (pós-tabela)
        if stripped.startswith('*') and not stripped.startswith('**') and stripped.count('*') == 1:
            note_text = stripped[1:].strip()
            blocks.append({'type': 'table_note', 'text': note_text})
            i += 1
            continue

        # Blockquote: > texto
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines):
                ql = lines[i].strip()
                if ql.startswith('> '):
                    quote_lines.append(ql[2:])
                elif ql == '>':
                    quote_lines.append('')
                elif ql == '':
                    break
                else:
                    break
                i += 1
            blocks.append({'type': 'blockquote', 'text': '\n'.join(quote_lines).strip()})
            continue

        # Parágrafo normal
        para_lines = [stripped]
        i += 1
        # Acumular linhas não-vazias que não sejam headings/boxes/tabelas/listas
        while i < len(lines):
            next_line = lines[i].strip()
            if (not next_line or
                next_line.startswith('#') or
                next_line.startswith(':::') or
                next_line.startswith('## ') or
                next_line.startswith('|') or
                next_line.startswith('- ') or
                next_line.startswith('> ') or
                re.match(r'^\d+\.\s', next_line)):
                break
            para_lines.append(next_line)
            i += 1

        blocks.append({'type': 'paragraph', 'text': ' '.join(para_lines)})

    return blocks


# ═══════════════════════════════════════════════════════
# ETAPA 3 — GERAÇÃO DO DOCX
# ═══════════════════════════════════════════════════════

# ── Hifenização pt-BR ──

def _set_style_language(style, lang_code='pt-BR'):
    """Define o idioma no estilo (Normal, Heading, etc.) via XML direto.
    Garante que o Word use o dicionário de hifenização correto.
    """
    rPr = style.element.find(qn('w:rPr'))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}/>')
        style.element.insert(0, rPr)
    lang = rPr.find(qn('w:lang'))
    if lang is None:
        lang = parse_xml(
            f'<w:lang {nsdecls("w")} w:val="{lang_code}" w:bidi="ar-SA"/>'
        )
        rPr.append(lang)
    else:
        lang.set(qn('w:val'), lang_code)


# Cache do dicionário pyphen (inicializado sob demanda)
_hyphenator = None

def _get_hyphenator():
    """Retorna instância pyphen pt_BR, ou None se indisponível."""
    global _hyphenator
    if _hyphenator is None:
        try:
            import pyphen
            _hyphenator = pyphen.Pyphen(lang='pt_BR')
        except (ImportError, Exception):
            _hyphenator = False  # Sentinela: tentou e falhou
    return _hyphenator if _hyphenator else None


# Palavras que NÃO devem ser hifenizadas (siglas, abreviações, nomes próprios curtos)
_NO_HYPHEN = {
    'INSS', 'RGPS', 'RPPS', 'LOAS', 'BPC', 'FGTS', 'CNIS', 'CJF', 'TRF',
    'TNU', 'STF', 'STJ', 'TST', 'JEF', 'JEFs', 'CRPS', 'CNAS', 'MPS',
    'IRPF', 'COFINS', 'PIS', 'CSLL', 'ICMS', 'ISS', 'IPTU', 'IPVA',
    'CPC', 'CLT', 'LEP', 'LINDB', 'ADCT', 'CDPD', 'OMS', 'CIF', 'OIT',
    'DOU', 'DIB', 'DII', 'DCB', 'DER', 'DAT', 'NIT', 'PIS', 'NB',
    'FAP', 'SAT', 'RAT', 'GILRAT', 'NTEP', 'PPP', 'LTCAT', 'CAT',
    'COPES', 'Atestmed', 'Sisperjud', 'IFBrA', 'IFBr',
    'art.', 'arts.', 'inc.', 'par.', 'n.', 'ed.', 'vol.', 'p.',
}

# Tamanho mínimo para hifenizar (palavras curtas não quebram)
_MIN_HYPHEN_LEN = 6


def _soft_hyphenate(text):
    """Insere soft hyphens (U+00AD) no texto usando dicionário pt_BR.
    Só hifeniza palavras com 6+ caracteres que não estejam na lista de exceções.
    Preserva pontuação, números, referências normativas e formatação Markdown.
    """
    hyph = _get_hyphenator()
    if hyph is None:
        return text  # Fallback: sem soft hyphens, Word decide sozinho

    SHY = '­'  # Soft hyphen

    def _hyphenate_word(word):
        # Ignorar palavras curtas
        if len(word) < _MIN_HYPHEN_LEN:
            return word
        # Ignorar se está na lista de exceções
        if word in _NO_HYPHEN or word.rstrip('.,:;)') in _NO_HYPHEN:
            return word
        # Ignorar se contém dígitos (art. 201, R$ 1.518,00, etc.)
        if any(c.isdigit() for c in word):
            return word
        # Ignorar se toda em maiúsculas (siglas não capturadas)
        if word.isupper() and len(word) <= 10:
            return word
        # Separar pontuação final
        trail = ''
        core = word
        while core and core[-1] in '.,;:!?)]\'"':
            trail = core[-1] + trail
            core = core[:-1]
        lead = ''
        while core and core[0] in '(["\'"':
            lead += core[0]
            core = core[1:]
        if len(core) < _MIN_HYPHEN_LEN:
            return word
        # Hifenizar via pyphen
        pairs = hyph.positions(core)
        if not pairs:
            return word
        # Inserir soft hyphens nas posições válidas
        result = []
        prev = 0
        for pos in pairs:
            # Mínimo 2 caracteres antes e depois da quebra
            if pos >= 2 and (len(core) - pos) >= 2:
                result.append(core[prev:pos])
                prev = pos
        result.append(core[prev:])
        return lead + SHY.join(result) + trail

    # Processar palavra por palavra, preservando espaços e quebras
    tokens = re.split(r'(\s+)', text)
    return ''.join(
        _hyphenate_word(t) if not t.isspace() else t
        for t in tokens
    )


def _enable_auto_hyphenation(doc):
    """Ativa hifenização automática no documento com idioma pt-BR.
    Essencial em A5 com justificação plena para evitar 'rios brancos'.
    """
    settings = doc.settings.element
    # autoHyphenation = true
    auto_hyph = settings.find(qn('w:autoHyphenation'))
    if auto_hyph is None:
        auto_hyph = parse_xml(f'<w:autoHyphenation {nsdecls("w")} w:val="1"/>')
        settings.append(auto_hyph)
    else:
        auto_hyph.set(qn('w:val'), '1')
    # Zona de hifenização: 350 twips (~0.62cm) — mais agressiva que o padrão
    # (425 twips). Em A5 justificado, zona menor força o Word a hifenizar
    # antes de esticar espaços entre palavras, reduzindo rios brancos.
    hyph_zone = settings.find(qn('w:hyphenationZone'))
    if hyph_zone is None:
        hyph_zone = parse_xml(f'<w:hyphenationZone {nsdecls("w")} w:val="350"/>')
        settings.append(hyph_zone)
    else:
        hyph_zone.set(qn('w:val'), '350')
    # Máximo de 3 linhas consecutivas com hífen (padrão editorial)
    consec = settings.find(qn('w:consecutiveHyphenLimit'))
    if consec is None:
        consec = parse_xml(f'<w:consecutiveHyphenLimit {nsdecls("w")} w:val="3"/>')
        settings.append(consec)
    else:
        consec.set(qn('w:val'), '3')
    # Não hifenizar CAPS (títulos, siglas)
    caps_hyph = settings.find(qn('w:doNotHyphenateCaps'))
    if caps_hyph is None:
        caps_hyph = parse_xml(f'<w:doNotHyphenateCaps {nsdecls("w")} w:val="1"/>')
        settings.append(caps_hyph)
    # Idioma do documento: pt-BR (crítico para o dicionário de hifenização)
    theme_lang = settings.find(qn('w:themeFontLang'))
    if theme_lang is None:
        theme_lang = parse_xml(
            f'<w:themeFontLang {nsdecls("w")} w:val="pt-BR" w:bidi="ar-SA"/>'
        )
        settings.append(theme_lang)
    else:
        theme_lang.set(qn('w:val'), 'pt-BR')
    # Compressão de pontuação em fim de linha — reduz espaçamento excessivo
    # quando ponto, vírgula ou parêntese cairiam no início da próxima linha
    char_spacing = settings.find(qn('w:characterSpacingControl'))
    if char_spacing is None:
        char_spacing = parse_xml(
            f'<w:characterSpacingControl {nsdecls("w")} w:val="compressPunctuation"/>'
        )
        settings.append(char_spacing)
    else:
        char_spacing.set(qn('w:val'), 'compressPunctuation')


def _set_compat_settings(doc):
    """Configura compatibilidade do Word para melhor justificação.
    Desativa espaçamento automático legado (Word 95) e ajusta
    altura de linha em tabelas para mancha tipográfica mais uniforme.
    """
    settings = doc.settings.element
    compat = settings.find(qn('w:compat'))
    if compat is None:
        compat = parse_xml(f'<w:compat {nsdecls("w")}/>')
        settings.append(compat)

    # Desativar autoSpaceLikeWord95 — impede espaçamento irregular
    # entre caracteres latinos e CJK (herança desnecessária)
    _ensure_compat_setting(compat, 'autoSpaceLikeWord95', '0')
    # Ajustar altura de linha em tabelas (boxes, quadros sinópticos)
    _ensure_compat_setting(compat, 'adjustLineHeightInTable', '1')
    # Usar espaçamento de parágrafo do Word 2013+ (mais preciso)
    _ensure_compat_setting(compat, 'compatibilityMode', '15')


def _ensure_compat_setting(compat_elem, name, val):
    """Insere ou atualiza um w:compatSetting dentro de w:compat."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    # Procurar setting existente pelo atributo w:name
    for cs in compat_elem.findall(qn('w:compatSetting')):
        if cs.get(qn('w:name')) == name:
            cs.set(qn('w:val'), val)
            return
    # Criar novo
    cs = parse_xml(
        f'<w:compatSetting {nsdecls("w")}'
        f' w:name="{name}" w:uri="http://schemas.microsoft.com/office/word"'
        f' w:val="{val}"/>'
    )
    compat_elem.append(cs)


def _enable_w14_namespace(doc):
    """Registra namespace w14 (Word 2010+) e mc:Ignorable no documento.
    Necessário para que w14:ligatures seja reconhecido pelo Word.
    Sem mc:Ignorable, versões anteriores podem rejeitar o arquivo.
    """
    doc_elem = doc.element  # <w:document>
    # Verificar se w14 já está declarado no nsmap
    nsmap = doc_elem.nsmap
    if 'w14' not in nsmap:
        # Adicionar declaração xmlns:w14
        doc_elem.set('{http://www.w3.org/2000/xmlns/}w14', W14_NS)
    # Garantir mc:Ignorable inclui w14
    ignorable = doc_elem.get(f'{{{MC_NS}}}Ignorable', '')
    parts = ignorable.split()
    if 'w14' not in parts:
        parts.append('w14')
        doc_elem.set(f'{{{MC_NS}}}Ignorable', ' '.join(parts))


def _add_ligatures_to_rPr(rPr):
    """Adiciona w14:ligatures standardContextual a um rPr.
    Ativa ligaduras OpenType padrão (fi, fl, ff, ffi, ffl) e contextuais
    no EB Garamond, que possui tabelas GSUB ricas.
    """
    lig = rPr.find(f'{{{W14_NS}}}ligatures')
    if lig is None:
        lig = etree.SubElement(rPr, f'{{{W14_NS}}}ligatures')
        lig.set(f'{{{W14_NS}}}val', 'standardContextual')


def set_page_a5_mirrored(doc):
    """Configura página A5 com margens espelhadas e hifenização."""
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

    # Hifenização automática
    _enable_auto_hyphenation(doc)
    # Compatibilidade para justificação aprimorada
    _set_compat_settings(doc)
    # Namespace w14 para ligaduras OpenType
    _enable_w14_namespace(doc)


def add_run_with_style(paragraph, text, font_name="EB Garamond", size=Pt(10.7),
                       bold=False, italic=False, color=None, small_caps=False,
                       all_caps=False, hyphenate=True):
    """Adiciona run com formatação. hyphenate=True insere soft hyphens pt-BR."""
    # Soft hyphens desativados: w:lang pt-BR no estilo Normal já garante
    # hifenização correta via dicionário do Word. Soft hyphens causam
    # quebras de linha prematuras (+10% páginas). Manter o código para
    # eventual uso futuro em palavras específicas via lista de exceções.
    # if hyphenate and not all_caps and not small_caps:
    #     text = _soft_hyphenate(text)
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
    # Idioma pt-BR em cada run (garante dicionário de hifenização correto)
    lang = rPr.find(qn('w:lang'))
    if lang is None:
        lang = parse_xml(f'<w:lang {nsdecls("w")} w:val="pt-BR" w:bidi="ar-SA"/>')
        rPr.append(lang)
    else:
        lang.set(qn('w:val'), 'pt-BR')
    # Kerning óptico: ativa micro-ajuste de espaçamento entre pares de
    # caracteres (AV, To, Wa, etc.) para fontes ≥ 8pt. O EB Garamond tem
    # tabelas kern ricas — sem isso o Word ignora os pares.
    # Valor em meio-pontos: 16 = 8pt (ativa para todo texto do livro).
    kern = rPr.find(qn('w:kern'))
    if kern is None:
        kern = parse_xml(f'<w:kern {nsdecls("w")} w:val="16"/>')
        rPr.append(kern)
    # Ligaduras OpenType: standard (fi, fl, ff, ffi, ffl) + contextuais.
    # EB Garamond tem tabelas GSUB ricas — sem ligaduras, pares como "fi"
    # aparecem com espaçamento irregular visível em impressão de qualidade.
    _add_ligatures_to_rPr(rPr)
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


def _parse_inline_formatting(text):
    """Parse **bold**, *italic* e ***bold italic*** no texto.
    Retorna lista de (texto, is_bold, is_italic)."""
    segments = []
    # Ordem: ***bold-italic*** antes de **bold** antes de *italic*
    pattern = r'\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(?!\*)(.+?)(?<!\*)\*(?!\*)'
    last_end = 0
    for m in re.finditer(pattern, text):
        if m.start() > last_end:
            segments.append((text[last_end:m.start()], False, False))
        if m.group(1) is not None:
            segments.append((m.group(1), True, True))
        elif m.group(2) is not None:
            # Verificar itálico aninhado dentro de negrito: **text *italic* text**
            inner = m.group(2)
            italic_pat = r'\*(?!\*)(.+?)(?<!\*)\*(?!\*)'
            ilast = 0
            has_nested = False
            for im in re.finditer(italic_pat, inner):
                has_nested = True
                if im.start() > ilast:
                    segments.append((inner[ilast:im.start()], True, False))
                segments.append((im.group(1), True, True))
                ilast = im.end()
            if has_nested:
                if ilast < len(inner):
                    segments.append((inner[ilast:], True, False))
            else:
                segments.append((inner, True, False))
        elif m.group(3) is not None:
            segments.append((m.group(3), False, True))
        last_end = m.end()
    if last_end < len(text):
        segments.append((text[last_end:], False, False))
    if not segments:
        segments.append((text, False, False))
    return segments


def add_paragraph_with_bold(doc_or_cell, text, font_name="EB Garamond", size=Pt(10.7),
                            color="201B16", alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                            first_indent=0.42, space_before=0, space_after=3.5,
                            line_spacing=1.08):
    """Adiciona parágrafo processando **negrito** e *itálico* inline."""
    p = doc_or_cell.add_paragraph()
    p.alignment = alignment
    set_paragraph_spacing(p, before=space_before, after=space_after, line_spacing=line_spacing)
    if first_indent > 0:
        set_first_line_indent(p, first_indent)

    # Parse bold + italic markers
    segments = _parse_inline_formatting(text)
    for seg_text, is_bold, is_italic in segments:
        if seg_text:
            add_run_with_style(p, seg_text, font_name=font_name, size=size,
                             bold=is_bold, italic=is_italic, color=color)
    return p


def add_drop_cap(doc, text, lines=3, cap_color="B78B37"):
    """Adiciona parágrafo com letra capitular real via w:framePr.

    Usa o mecanismo nativo do Word para drop caps: a primeira letra
    fica em um parágrafo separado com w:framePr dropCap="drop",
    e o Word faz o texto seguinte fluir ao redor dela automaticamente.
    Resultado: capitular tipográfica profissional que ocupa N linhas,
    alinhada à baseline da N-ésima linha do parágrafo adjacente.
    """
    if not text or len(text.strip()) < 2:
        return add_paragraph_with_bold(doc, text, first_indent=0)

    clean = text.strip()

    # Strip marcadores Markdown de abertura (**bold**, *italic*)
    leading_marks = ''
    while clean and clean[0] == '*':
        leading_marks += clean[0]
        clean = clean[1:]

    # Se primeiro caractere não é letra, fallback para parágrafo normal
    if not clean or not clean[0].isalpha():
        return add_paragraph_with_bold(doc, text.strip(), first_indent=0)

    first_letter = clean[0]
    rest_text = clean[1:]
    # Re-anexar marcadores ao restante para preservar formatação inline
    if leading_marks:
        rest_text = leading_marks + rest_text

    # ── Parágrafo 1: letra capitular com w:framePr ──
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(p_cap, before=0, after=0, line_spacing=1.0)

    # Inserir w:framePr nas propriedades do parágrafo
    pPr = p_cap._element.get_or_add_pPr()
    framePr = parse_xml(
        f'<w:framePr {nsdecls("w")}'
        f' w:dropCap="drop" w:lines="{lines}"'
        f' w:wrap="around" w:vAnchor="text" w:hAnchor="text"'
        f' w:hSpace="28"/>'
    )
    pPr.append(framePr)

    # Tamanho da capitular: ~3x a entrelinha do corpo
    # Corpo: 10.7pt × 1.08 spacing ≈ 11.56pt/linha
    # 3 linhas ≈ 34.7pt — com ajuste tipográfico → ~32pt
    cap_size = Pt(32)
    add_run_with_style(p_cap, first_letter, font_name="EB Garamond",
                       size=cap_size, bold=True, color=cap_color)

    # ── Parágrafo 2: restante do texto (flui ao redor da capitular) ──
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(p, before=0, after=3.5, line_spacing=1.08)

    segments = _parse_inline_formatting(rest_text)
    for seg_text, is_bold, is_italic in segments:
        if seg_text:
            add_run_with_style(p, seg_text, font_name="EB Garamond",
                             size=Pt(10.7), bold=is_bold, italic=is_italic,
                             color="201B16")
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
    keep_with_next(p_label)  # Nunca separar etiqueta do título

    # Título
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_title, before=0, after=8, line_spacing=1.0)
    add_run_with_style(p_title, cap_title.upper(), font_name="EB Garamond",
                      size=Pt(20), bold=True, color="2F2923")
    keep_with_next(p_title)  # Nunca separar título do ornamento

    # Ornamento — filête dourado
    p_orn = doc.add_paragraph()
    p_orn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p_orn, before=0, after=12, line_spacing=1.0)
    add_run_with_style(p_orn, "━━━━  ◆  ━━━━", font_name="EB Garamond",
                      size=Pt(9), color="B78B37")

    return cap_num, cap_title


def _add_page_field(paragraph, font_name="EB Garamond", size=Pt(9),
                    color="6B6256"):
    """Insere campo PAGE num parágrafo (helper para rodapés)."""
    run1 = paragraph.add_run()
    run1.font.name = font_name
    run1.font.size = size
    run1.font.color.rgb = hex_to_rgb(color)
    fld_begin = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run1._element.append(fld_begin)

    run2 = paragraph.add_run()
    run2.font.name = font_name
    run2.font.size = size
    run2.font.color.rgb = hex_to_rgb(color)
    instr = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run2._element.append(instr)

    run3 = paragraph.add_run()
    run3.font.name = font_name
    run3.font.size = size
    fld_end = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run3._element.append(fld_end)


def add_header_footer(doc, cap_num, cap_title):
    """Configura cabeçalho e rodapé com fólio alternado.
    Rodapé: número à direita (ímpar) / esquerda (par).
    """
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    # Habilitar cabeçalhos/rodapés par/ímpar distintos
    settings = doc.settings.element
    eoh = settings.find(qn('w:evenAndOddHeaders'))
    if eoh is None:
        eoh = parse_xml(f'<w:evenAndOddHeaders {nsdecls("w")}/>')
        settings.append(eoh)

    # Cabeçalho ímpar (páginas direitas) — capítulo
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.clear()
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_run_with_style(hp, f"Capítulo {cap_num}  |  {cap_title}",
                       font_name="EB Garamond", size=Pt(8.6),
                       color="6B6256", small_caps=True)
    pPr = hp._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="2" w:color="D7CDBB"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

    # Cabeçalho par (páginas esquerdas) — título do livro
    even_header = section.even_page_header
    even_header.is_linked_to_previous = False
    ehp = even_header.paragraphs[0] if even_header.paragraphs else even_header.add_paragraph()
    ehp.clear()
    ehp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_run_with_style(ehp, "Direito Previdenciário",
                       font_name="EB Garamond", size=Pt(8.6),
                       color="6B6256", small_caps=True)
    epPr = ehp._element.get_or_add_pPr()
    epBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="2" w:color="D7CDBB"/>'
        f'</w:pBdr>'
    )
    epPr.append(epBdr)

    # Rodapé ímpar (páginas direitas) — número à direita
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.clear()
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _add_page_field(fp)

    # Rodapé par (páginas esquerdas) — número à esquerda
    even_footer = section.even_page_footer
    even_footer.is_linked_to_previous = False
    efp = even_footer.paragraphs[0] if even_footer.paragraphs else even_footer.add_paragraph()
    efp.clear()
    efp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _add_page_field(efp)

    # Rodapé da primeira página — centralizado (abertura de capítulo)
    first_footer = section.first_page_footer
    first_footer.is_linked_to_previous = False
    ffp = first_footer.paragraphs[0] if first_footer.paragraphs else first_footer.add_paragraph()
    ffp.clear()
    ffp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_page_field(ffp)


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
        'box-quadro': {
            'label': 'QUADRO',
            'bg': COLORS['box_quadro_bg'],
            'accent': COLORS['box_quadro_accent'],
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
    tblLayout = parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>')
    tblPr.append(tblLayout)

    # cantSplit em todas as rows para manter box intacto
    for row in table.rows:
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        cantSplit = parse_xml(f'<w:cantSplit {nsdecls("w")}/>')
        trPr.append(cantSplit)

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

    # Bordas da célula (left grossa = accent, demais finas = borda do tipo ou genérica)
    border_key = f'box_{box_type.replace("box-", "")}_border'
    border_color = COLORS.get(border_key, COLORS['box_border'])
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="7" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="7" w:space="0" w:color="{border_color}"/>'
        f'  <w:right w:val="single" w:sz="7" w:space="0" w:color="{border_color}"/>'
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

    # Conteúdo do box (pode ter múltiplos parágrafos e listas)
    paragraphs = text.split('\n\n') if '\n\n' in text else [text]
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        # Detectar se o segmento é uma lista
        seg_lines = [l.strip() for l in para_text.split('\n') if l.strip()]
        if seg_lines and all(l.startswith('- ') for l in seg_lines):
            # Renderizar como lista bullet dentro do box
            for sl in seg_lines:
                item_text = sl[2:]
                p_item = cell.add_paragraph()
                p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                set_paragraph_spacing(p_item, before=0, after=1.5, line_spacing=1.0)
                pf = p_item.paragraph_format
                pf.left_indent = Cm(0.4)
                pf.first_line_indent = Cm(-0.25)
                segs = _parse_inline_formatting("• " + item_text)
                for s_text, is_bold, is_italic in segs:
                    if s_text:
                        add_run_with_style(p_item, s_text, font_name="EB Garamond",
                                         size=Pt(9.6), bold=is_bold,
                                         italic=is_italic, color="201B16")
        elif seg_lines and all(re.match(r'^\d+\.\s', l) for l in seg_lines):
            # Renderizar como lista numerada dentro do box
            for sl in seg_lines:
                item_text = re.sub(r'^\d+\.\s+', '', sl)
                num = re.match(r'^(\d+)\.', sl).group(1)
                p_item = cell.add_paragraph()
                p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                set_paragraph_spacing(p_item, before=0, after=1.5, line_spacing=1.0)
                pf = p_item.paragraph_format
                pf.left_indent = Cm(0.4)
                pf.first_line_indent = Cm(-0.25)
                segs = _parse_inline_formatting(f"{num}. " + item_text)
                for s_text, is_bold, is_italic in segs:
                    if s_text:
                        add_run_with_style(p_item, s_text, font_name="EB Garamond",
                                         size=Pt(9.6), bold=is_bold,
                                         italic=is_italic, color="201B16")
        else:
            # Parágrafo normal
            add_paragraph_with_bold(cell, para_text.replace('\n', ' '), size=Pt(9.6),
                                   color="201B16", first_indent=0, space_before=0,
                                   space_after=3, line_spacing=1.03)

    # Espaço após o box
    p_after = doc.add_paragraph()
    set_paragraph_spacing(p_after, before=0, after=4, line_spacing=1.0)
    # Parágrafo vazio pequeno para espaçamento


def add_blockquote(doc, text):
    """Adiciona citação em bloco com recuo bilateral, itálico e borda esquerda."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="4600" w:type="pct"/>')
    tblPr.append(tblW)

    cell = table.cell(0, 0)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # Padding
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="100" w:type="dxa"/>'
        f'  <w:bottom w:w="100" w:type="dxa"/>'
        f'  <w:left w:w="240" w:type="dxa"/>'
        f'  <w:right w:w="180" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

    # Bordas: só borda esquerda (accent gold)
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="{COLORS["gold_accent"]}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    # Limpar parágrafo padrão
    for p in cell.paragraphs:
        p._element.getparent().remove(p._element)

    # Conteúdo em itálico
    paragraphs = text.split('\n\n') if '\n\n' in text else [text]
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        p = cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_paragraph_spacing(p, before=0, after=3, line_spacing=1.05)
        # Processar formatação inline (o texto pode já ter *itálico*)
        segments = _parse_inline_formatting(para_text)
        for seg_text, is_bold, is_italic in segments:
            if seg_text:
                add_run_with_style(p, seg_text, font_name="EB Garamond",
                                 size=Pt(10), bold=is_bold,
                                 italic=True, color="3A3128")

    # Espaço após
    p_after = doc.add_paragraph()
    set_paragraph_spacing(p_after, before=0, after=4, line_spacing=1.0)


def add_table_block(doc, headers, rows):
    """Adiciona tabela formatada ao documento."""
    num_cols = len(headers)
    num_rows = 1 + len(rows)

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Largura 100%
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    tblPr.append(tblW)

    # Header row — marcar como tblHeader para repetição em multi-página
    header_row = table.rows[0]
    trPr = header_row._tr.get_or_add_trPr()
    tbl_header = parse_xml(f'<w:tblHeader {nsdecls("w")}/>')
    trPr.append(tbl_header)

    # Header row
    for j, header_text in enumerate(headers):
        cell = table.cell(0, j)
        for p in cell.paragraphs:
            p._element.getparent().remove(p._element)
        p = cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(p, before=2, after=2, line_spacing=1.0)
        add_run_with_style(p, header_text.strip(), font_name="EB Garamond",
                          size=Pt(9.2), bold=True, color="2F2923")
        # Fundo do header
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0EDE6" w:val="clear"/>')
        tcPr.append(shd)

    # Data rows
    for i, row_data in enumerate(rows):
        for j in range(num_cols):
            cell_text = row_data[j].strip() if j < len(row_data) else ""
            cell = table.cell(i + 1, j)
            for p in cell.paragraphs:
                p._element.getparent().remove(p._element)
            add_paragraph_with_bold(cell, cell_text, size=Pt(9.2),
                                   color="201B16", alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                   first_indent=0, space_before=1, space_after=1,
                                   line_spacing=1.0)

    # Bordas
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D2C9B8"/>'
                f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D2C9B8"/>'
                f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="D2C9B8"/>'
                f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D2C9B8"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    # Espaço após tabela
    p_after = doc.add_paragraph()
    set_paragraph_spacing(p_after, before=0, after=4, line_spacing=1.0)


def add_list_item(doc, text, ordered=False, number=1):
    """Adiciona item de lista com bullet (•) ou número."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(p, before=0, after=2, line_spacing=1.05)

    pf = p.paragraph_format
    pf.left_indent = Cm(0.6)
    pf.first_line_indent = Cm(-0.35)

    prefix = f"{number}. " if ordered else "• "

    # Prefixo com cor do heading
    add_run_with_style(p, prefix, font_name="EB Garamond", size=Pt(10.2),
                      color="3A3128")

    # Texto com formatação inline
    segments = _parse_inline_formatting(text)
    for seg_text, is_bold, is_italic in segments:
        if seg_text:
            add_run_with_style(p, seg_text, font_name="EB Garamond", size=Pt(10.2),
                             bold=is_bold, italic=is_italic, color="201B16")
    return p


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
    style.paragraph_format.widow_control = True
    # Idioma pt-BR no estilo Normal (hifenização correta)
    _set_style_language(style, 'pt-BR')

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
            add_run_with_style(p, block['text'], font_name="EB Garamond",
                             size=Pt(8.5), italic=True, color="6B6256")

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
            if is_first_paragraph:
                add_drop_cap(doc, block['text'])
            else:
                add_paragraph_with_bold(doc, block['text'],
                                       first_indent=0.42)
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
