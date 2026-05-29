#!/usr/bin/env python3
"""
fix_terminologia.py — Corrige terminologia proibida nos capítulos
  - "auxílio-doença" → "auxílio por incapacidade temporária"
  - "aposentadoria por invalidez" → "aposentadoria por incapacidade permanente"

Preserva o termo antigo quando está em contexto histórico, entre aspas
discutindo nomenclatura, ou já possui qualificador (atual/antigo).
"""

import re
import glob
import os


def should_protect_ad(text, match):
    """Decide se a ocorrência de 'auxílio-doença' deve ser preservada."""
    start = max(0, match.start() - 120)
    end = min(len(text), match.end() + 80)
    before = text[start:match.start()].lower()
    after = text[match.end():end].lower()

    # Contexto já qualificado
    if any(p in before for p in [
        'antigo ', 'anterior ', 'denominado ', 'conhecido como ',
        'chamado ', 'expressão "', 'expressão "', 'denominação "',
        'nomenclatura', 'de "', 'de "'
    ]):
        return True

    if any(p in after for p in [
        '(atual', '[atual', '" para', '" por', 'permanente',
        '— constitui a prestação',   # Cap 07 discussing the name
    ]):
        return True

    # Termo entre aspas duplas: "auxílio-doença"
    # Verificar se há aspas envolvendo
    char_before = text[match.start()-1] if match.start() > 0 else ''
    char_after = text[match.end()] if match.end() < len(text) else ''
    if char_before in '""«' or char_after in '""»':
        return True

    # Em linha que discute nomenclatura/terminologia
    # Pegar a linha inteira
    line_start = text.rfind('\n', 0, match.start()) + 1
    line_end = text.find('\n', match.end())
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].lower()
    if any(p in line for p in [
        'nomenclatura', 'terminologi', 'denominaç', 'renomeou',
        'passou a se chamar', 'passou a denominar',
        'alterou a', 'substituição terminológica',
        'redação original', 'expressão "', 'expressão "'
    ]):
        return True

    # YAML frontmatter (linhas com tags:)
    if 'tags:' in line or line.strip().startswith('---'):
        return True

    # "auxílio-doença permanente" (termo doutrinário específico)
    if 'permanente' in after[:20]:
        return True

    return False


def should_protect_ai(text, match):
    """Decide se a ocorrência de 'aposentadoria por invalidez' deve ser preservada."""
    start = max(0, match.start() - 120)
    end = min(len(text), match.end() + 80)
    before = text[start:match.start()].lower()
    after = text[match.end():end].lower()

    # Contexto já qualificado
    if any(p in before for p in [
        'antiga ', 'anterior ', 'denominad', 'conhecid',
        'chamad', 'expressão "', 'denominação "',
        'nomenclatura', 'de "', 'de "'
    ]):
        return True

    if any(p in after for p in [
        '(atual', '[atual', '" para', '" por',
        '— constitui',
    ]):
        return True

    # Termo entre aspas duplas
    char_before = text[match.start()-1] if match.start() > 0 else ''
    char_after = text[match.end()] if match.end() < len(text) else ''
    if char_before in '""«' or char_after in '""»':
        return True

    # Linha que discute nomenclatura
    line_start = text.rfind('\n', 0, match.start()) + 1
    line_end = text.find('\n', match.end())
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].lower()
    if any(p in line for p in [
        'nomenclatura', 'terminologi', 'denominaç', 'renomeou',
        'passou a se chamar', 'passou a denominar',
        'alterou a', 'substituição terminológica',
        'redação original', 'expressão "', 'expressão "'
    ]):
        return True

    # YAML
    if 'tags:' in line or line.strip().startswith('---'):
        return True

    return False


def fix_case(original, replacement):
    """Mantém capitalização do original no replacement."""
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def fix_terminology(text):
    """Aplica correções de terminologia no texto."""
    changes = {'ad_replaced': 0, 'ad_protected': 0,
               'ai_replaced': 0, 'ai_protected': 0}

    # ===== AUXÍLIO-DOENÇA =====
    def replace_ad(match):
        if should_protect_ad(text, match):
            changes['ad_protected'] += 1
            return match.group()
        changes['ad_replaced'] += 1
        return fix_case(match.group(), 'auxílio por incapacidade temporária')

    result = re.sub(r'auxílio-doença', replace_ad, text, flags=re.IGNORECASE)

    # Atualizar text reference para a segunda passada
    text2 = result

    # ===== APOSENTADORIA POR INVALIDEZ =====
    def replace_ai(match):
        if should_protect_ai(text2, match):
            changes['ai_protected'] += 1
            return match.group()
        changes['ai_replaced'] += 1
        return fix_case(match.group(), 'aposentadoria por incapacidade permanente')

    result = re.sub(r'aposentadoria por invalidez', replace_ai, result, flags=re.IGNORECASE)

    return result, changes


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'output', 'rascunhos')
    mds = sorted(glob.glob(os.path.join(base, 'cap_*_rascunho.md')))

    total = {'ad_replaced': 0, 'ad_protected': 0,
             'ai_replaced': 0, 'ai_protected': 0}

    for md in mds:
        cap = os.path.basename(md).split('_')[1]

        with open(md, 'r', encoding='utf-8') as f:
            text = f.read()

        result, changes = fix_terminology(text)

        if changes['ad_replaced'] + changes['ai_replaced'] > 0:
            with open(md, 'w', encoding='utf-8') as f:
                f.write(result)

            parts = []
            if changes['ad_replaced']:
                parts.append(f"AD: {changes['ad_replaced']} corrig/{changes['ad_protected']} preserv")
            if changes['ai_replaced']:
                parts.append(f"AI: {changes['ai_replaced']} corrig/{changes['ai_protected']} preserv")
            print(f"  Cap {cap}: {', '.join(parts)}")
        else:
            if changes['ad_protected'] + changes['ai_protected'] > 0:
                print(f"  Cap {cap}: nenhuma correção (todos protegidos)")

        for k in total:
            total[k] += changes[k]

    print(f"\n  TOTAL: auxílio-doença {total['ad_replaced']} corrigidos, {total['ad_protected']} preservados")
    print(f"         aposentadoria por invalidez {total['ai_replaced']} corrigidos, {total['ai_protected']} preservados")


if __name__ == '__main__':
    main()
