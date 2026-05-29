#!/usr/bin/env python3
"""
fix_frases_muleta.py — Reduz frases-muleta reveladoras de texto assistido por IA

Frases-alvo:
  - "Na pratica" -> variantes contextuais
  - "de fato" -> remover ou substituir
  - "com efeito" -> remover ou substituir

Estrategia:
  - Primeira ocorrencia em cada secao: preservar (uso legitimo)
  - Demais ocorrencias: substituir por variante ou remover
"""

import re
import glob
import os
from collections import defaultdict


# ═══════════════════════════════════════════════════════
# SUBSTITUIÇÕES
# ═══════════════════════════════════════════════════════

# "Na prática" — variantes cíclicas para evitar repetição
NA_PRATICA_ALTS = [
    'Na atuação forense',
    'No cotidiano dos JEFs',
    'Em termos operacionais',
    'Na experiência dos juizados',
    'Na rotina previdenciária',
    'Sob o aspecto prático',
    'No dia a dia processual',
    'Na dinâmica dos JEFs',
]

# "de fato" — na maioria dos casos é dispensável
DE_FATO_REMOVALS = [
    (r',\s*de fato,', ','),            # ", de fato," -> ","
    (r'\.\s*De fato,\s*', '. '),       # "De fato, X" -> "X"
    (r';\s*de fato,?\s*', '; '),       # "; de fato," -> "; "
]

# "com efeito" — dispensável na maioria dos contextos
COM_EFEITO_REMOVALS = [
    (r',\s*com efeito,', ','),
    (r'\.\s*Com efeito,\s*', '. '),
    (r';\s*com efeito,?\s*', '; '),
]


def count_in_body(text, phrase):
    """Conta ocorrências de frase excluindo headings e boxes."""
    count = 0
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('#') or s.startswith(':::') or s.startswith('---'):
            continue
        count += s.lower().count(phrase.lower())
    return count


def fix_na_pratica(text, max_per_section=1):
    """Reduz 'Na prática' mantendo max_per_section por seção ###."""
    section_re = re.compile(r'^(###+ .+)$', re.MULTILINE)
    pieces = section_re.split(text)

    alt_idx = 0
    total_replaced = 0

    new_pieces = []
    for piece in pieces:
        if piece.strip().startswith('#'):
            new_pieces.append(piece)
            continue

        occurrences = 0
        lines = piece.split('\n')
        new_lines = []
        for line in lines:
            s = line.strip()
            if s.startswith('#') or s.startswith(':::') or s.startswith('---'):
                new_lines.append(line)
                continue

            # Contar e substituir "Na prática" nesta linha
            matches = list(re.finditer(r'Na prática(?:\s+previdenciária)?', line, re.IGNORECASE))
            if not matches:
                new_lines.append(line)
                continue

            for m in reversed(matches):
                occurrences += 1
                if occurrences <= max_per_section:
                    continue  # Preservar primeira ocorrência
                # Substituir pela alternativa cíclica
                alt = NA_PRATICA_ALTS[alt_idx % len(NA_PRATICA_ALTS)]
                alt_idx += 1
                # Manter capitalização
                if m.group()[0].isupper():
                    replacement = alt
                else:
                    replacement = alt[0].lower() + alt[1:]
                line = line[:m.start()] + replacement + line[m.end():]
                total_replaced += 1

            new_lines.append(line)

        new_pieces.append('\n'.join(new_lines))

    return ''.join(new_pieces), total_replaced


def fix_de_fato(text):
    """Remove/substitui 'de fato' dispensável."""
    count = 0
    for pattern, replacement in DE_FATO_REMOVALS:
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        count += n
    return text, count


def fix_com_efeito(text):
    """Remove/substitui 'com efeito' dispensável."""
    count = 0
    for pattern, replacement in COM_EFEITO_REMOVALS:
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        count += n
    return text, count


def fix_frases_muleta(text):
    """Aplica todas as correções de frases-muleta."""
    stats = {}

    text, stats['na_pratica'] = fix_na_pratica(text)
    text, stats['de_fato'] = fix_de_fato(text)
    text, stats['com_efeito'] = fix_com_efeito(text)

    # Cleanup
    text = re.sub(r'  +', ' ', text)     # espaços duplos
    text = re.sub(r' ,', ',', text)      # espaço antes de vírgula
    text = re.sub(r',\s*,', ',', text)   # vírgula dupla
    text = re.sub(r'\.\s*\.', '.', text)  # ponto duplo

    stats['total'] = sum(stats.values())
    return text, stats


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'output', 'rascunhos')
    mds = sorted(glob.glob(os.path.join(base, 'cap_*_rascunho.md')))

    total_stats = defaultdict(int)

    for md in mds:
        cap = os.path.basename(md).split('_')[1]

        with open(md, 'r', encoding='utf-8') as f:
            text = f.read()

        # Contar antes
        before = {
            'na_pratica': count_in_body(text, 'na prática'),
            'de_fato': count_in_body(text, 'de fato'),
            'com_efeito': count_in_body(text, 'com efeito'),
        }

        result, stats = fix_frases_muleta(text)

        if stats['total'] > 0:
            with open(md, 'w', encoding='utf-8') as f:
                f.write(result)

            parts = []
            if stats['na_pratica']:
                parts.append(f"'na pratica':-{stats['na_pratica']}")
            if stats['de_fato']:
                parts.append(f"'de fato':-{stats['de_fato']}")
            if stats['com_efeito']:
                parts.append(f"'com efeito':-{stats['com_efeito']}")
            print(f"  Cap {cap}: {', '.join(parts)}")
        else:
            total_before = sum(before.values())
            if total_before > 0:
                print(f"  Cap {cap}: {total_before} ocorrencias (sem alteracao possivel)")

        for k, v in stats.items():
            total_stats[k] += v

    print(f"\n  TOTAL: {total_stats['total']} substituicoes")
    print(f"    'Na pratica': {total_stats['na_pratica']}")
    print(f"    'de fato': {total_stats['de_fato']}")
    print(f"    'com efeito': {total_stats['com_efeito']}")


if __name__ == '__main__':
    main()
