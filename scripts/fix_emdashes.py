#!/usr/bin/env python3
"""
fix_emdashes.py — Reduz excesso de em-dashes (—) nos capítulos
Meta: máximo 2 em-dashes por seção (### N.X).

Fases:
  1. Pares de em-dash (aposto) → vírgulas
  2. Padrões com conjunção/advérbio → vírgulas
  3. Redução per-section dos excedentes
"""

import re
import glob
import os


def count_body_emdashes(text):
    """Conta em-dashes excluindo linhas de heading e box-marker."""
    count = 0
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('#') or s.startswith(':::'):
            continue
        count += s.count('—')
    return count


def fix_emdashes(text):
    """Aplica redução de em-dashes em três fases."""

    # Separar YAML frontmatter
    parts = text.split('---', 2)
    if len(parts) >= 3 and not parts[0].strip():
        frontmatter = parts[0] + '---' + parts[1] + '---'
        body = parts[2]
    else:
        frontmatter = ''
        body = text

    original_count = count_body_emdashes(body)

    # ═════════════════════════════════════════════
    # FASE 1: Pares de em-dash (aposto)
    # " — texto aposto — " → ", texto aposto, "
    # ═════════════════════════════════════════════
    def replace_pair(m):
        inner = m.group(1).strip()
        # Não substituir se texto interno tem ponto (pode ser frase separada)
        if '. ' in inner:
            return m.group()
        return f', {inner}, '

    body = re.sub(r' — ([^—\n]{3,120}?) — ', replace_pair, body)
    # Segunda passada para pares que ficaram após a primeira
    body = re.sub(r' — ([^—\n]{3,120}?) —([,.])', lambda m: f', {m.group(1).strip()},{m.group(2)}', body)

    phase1_count = count_body_emdashes(body)

    # ═════════════════════════════════════════════
    # FASE 2: Padrões com conjunção/advérbio
    # ═════════════════════════════════════════════
    conj_patterns = [
        (r' — mas\b', ', mas'),
        (r' — porém\b', ', porém'),
        (r' — contudo\b', ', contudo'),
        (r' — todavia\b', ', todavia'),
        (r' — entretanto\b', ', entretanto'),
        (r' — ou seja,?', ', ou seja,'),
        (r' — isto é,?', ', isto é,'),
        (r' — como\b', ', como'),
        (r' — e não\b', ', e não'),
        (r' — e sim\b', ', e sim'),
        (r' — e também\b', ', e também'),
        (r' — e ainda\b', ', e ainda'),
        (r' — especialmente\b', ', especialmente'),
        (r' — sobretudo\b', ', sobretudo'),
        (r' — principalmente\b', ', principalmente'),
        (r' — notadamente\b', ', notadamente'),
        (r' — particularmente\b', ', particularmente'),
        (r' — inclusive\b', ', inclusive'),
        (r' — ainda que\b', ', ainda que'),
        (r' — mesmo que\b', ', mesmo que'),
        (r' — mesmo\b', ', mesmo'),
        (r' — embora\b', ', embora'),
        (r' — conquanto\b', ', conquanto'),
        (r' — seja\b', ', seja'),
        (r' — além d', ', além d'),
        (r' — segundo\b', ', segundo'),
        (r' — conforme\b', ', conforme'),
        (r' — pois\b', ', pois'),
        (r' — já que\b', ', já que'),
        (r' — uma vez que\b', ', uma vez que'),
        (r' — desde que\b', ', desde que'),
    ]

    for pattern, replacement in conj_patterns:
        body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)

    phase2_count = count_body_emdashes(body)

    # ═════════════════════════════════════════════
    # FASE 3: Redução per-section
    # Para seções com >2 em-dashes, substituir excesso
    # ═════════════════════════════════════════════

    # Padrões Phase 3 (prioridade: mais facilmente substituíveis primeiro)
    p3_patterns = [
        (r' — que\b', ', que'),
        (r' — o qual\b', ', o qual'),
        (r' — a qual\b', ', a qual'),
        (r' — os quais\b', ', os quais'),
        (r' — as quais\b', ', as quais'),
        (r' — quando\b', ', quando'),
        (r' — onde\b', ', onde'),
        (r' — se\b', ', se'),
        (r' — no\b', ', no'),
        (r' — na\b', ', na'),
        (r' — nos\b', ', nos'),
        (r' — nas\b', ', nas'),
        (r' — em\b', ', em'),
        (r' — com\b', ', com'),
        (r' — de\b', ', de'),
        (r' — do\b', ', do'),
        (r' — da\b', ', da'),
        (r' — dos\b', ', dos'),
        (r' — das\b', ', das'),
        (r' — ao\b', ', ao'),
        (r' — à\b', ', à'),
        (r' — aos\b', ', aos'),
        (r' — às\b', ', às'),
        (r' — a\b', ', a'),
        (r' — o\b', ', o'),
        (r' — os\b', ', os'),
        (r' — as\b', ', as'),
        (r' — para\b', ', para'),
        (r' — por\b', ', por'),
        (r' — sem\b', ', sem'),
        (r' — um\b', ', um'),
        (r' — uma\b', ', uma'),
        (r' — entre\b', ', entre'),
        (r' — sobre\b', ', sobre'),
        (r' — sob\b', ', sob'),
        (r' — mediante\b', ', mediante'),
        (r' — cujo\b', ', cujo'),
        (r' — cuja\b', ', cuja'),
        (r' — não\b', ', não'),
        (r' — é\b', ', é'),
        (r' — são\b', ', são'),
        (r' — foi\b', ', foi'),
        (r' — era\b', ', era'),
        (r' — será\b', ', será'),
        (r' — pode\b', ', pode'),
        (r' — deve\b', ', deve'),
        (r' — tem\b', ', tem'),
        (r' — e\b', ', e'),
        (r' — art\.\b', ', art.'),
        (r' — exceto\b', ', exceto'),
        (r' — salvo\b', ', salvo'),
        (r' — basta\b', ', basta'),
        (r' — constitui\b', ', constitui'),
        (r' — cada\b', ', cada'),
        (r' — caso\b', ', caso'),
    ]

    # Catch-all: qualquer " — [minúscula]" não capturado acima
    p3_catchall = re.compile(r' — ([a-záéíóúâêîôûãõç])')

    def catchall_replace(m):
        return f', {m.group(1)}'

    # Dividir texto em seções no ### heading
    section_re = re.compile(r'^(###+ .+)$', re.MULTILINE)
    pieces = section_re.split(body)
    # pieces alterna entre conteúdo e headings: [pre, h1, body1, h2, body2, ...]

    new_pieces = []
    for piece in pieces:
        # Preservar headings intactos
        if piece.strip().startswith('#'):
            new_pieces.append(piece)
            continue

        em_count = count_body_emdashes(piece)
        if em_count <= 2:
            new_pieces.append(piece)
            continue

        # Precisa reduzir
        excess = em_count - 2
        modified = piece

        for pattern, replacement in p3_patterns:
            if excess <= 0:
                break

            # Encontrar matches que NÃO estão em linhas de heading/box
            matches = []
            for m in re.finditer(pattern, modified, re.IGNORECASE):
                line_start = modified.rfind('\n', 0, m.start()) + 1
                line_text = modified[line_start:m.start()].strip()
                if not line_text.startswith('#') and not line_text.startswith(':::'):
                    matches.append(m)

            # Substituir do fim para o início (preservar posições)
            for m in reversed(matches):
                if excess <= 0:
                    break
                modified = modified[:m.start()] + replacement + modified[m.end():]
                excess -= 1

        # Catch-all para os restantes se ainda acima de 2
        if excess > 0:
            matches = []
            for m in p3_catchall.finditer(modified):
                line_start = modified.rfind('\n', 0, m.start()) + 1
                line_text = modified[line_start:m.start()].strip()
                if not line_text.startswith('#') and not line_text.startswith(':::'):
                    matches.append(m)
            for m in reversed(matches):
                if excess <= 0:
                    break
                modified = modified[:m.start()] + catchall_replace(m) + modified[m.end():]
                excess -= 1

        new_pieces.append(modified)

    body = ''.join(new_pieces)
    phase3_count = count_body_emdashes(body)

    # ═════════════════════════════════════════════
    # CLEANUP
    # ═════════════════════════════════════════════
    body = re.sub(r',\s*,', ',', body)       # vírgula dupla
    body = re.sub(r',\s*\.', '.', body)      # vírgula antes de ponto
    body = re.sub(r'  +', ' ', body)         # espaço duplo
    body = re.sub(r' ,', ',', body)          # espaço antes de vírgula
    body = re.sub(r',\s*;', ';', body)       # vírgula antes de ponto-e-vírgula

    final_count = count_body_emdashes(body)

    stats = {
        'original': original_count,
        'after_pairs': phase1_count,
        'after_conj': phase2_count,
        'after_section': phase3_count,
        'final': final_count,
        'removed': original_count - final_count,
    }

    return frontmatter + body, stats


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'output', 'rascunhos')
    mds = sorted(glob.glob(os.path.join(base, 'cap_*_rascunho.md')))

    total_original = 0
    total_final = 0
    total_removed = 0

    for md in mds:
        cap = os.path.basename(md).split('_')[1]

        with open(md, 'r', encoding='utf-8') as f:
            text = f.read()

        result, stats = fix_emdashes(text)

        total_original += stats['original']
        total_final += stats['final']
        total_removed += stats['removed']

        if stats['removed'] > 0:
            with open(md, 'w', encoding='utf-8') as f:
                f.write(result)

            print(f"  Cap {cap}: {stats['original']:3d} -> {stats['final']:3d} "
                  f"(-{stats['removed']:3d})  "
                  f"[pares:-{stats['original']-stats['after_pairs']:d} "
                  f"conj:-{stats['after_pairs']-stats['after_conj']:d} "
                  f"secao:-{stats['after_conj']-stats['final']:d}]")
        else:
            print(f"  Cap {cap}: {stats['original']:3d} (sem alteração)")

    print(f"\n  TOTAL: {total_original} -> {total_final} (-{total_removed} em-dashes, "
          f"-{total_removed/max(total_original,1)*100:.1f}%)")

    # Verificar média per-section
    section_counts = []
    for md in mds:
        with open(md, 'r', encoding='utf-8') as f:
            text = f.read()
        sections = re.split(r'^### ', text, flags=re.MULTILINE)
        for sec in sections[1:]:  # skip pre-section content
            em = count_body_emdashes(sec)
            section_counts.append(em)

    if section_counts:
        avg = sum(section_counts) / len(section_counts)
        over3 = sum(1 for c in section_counts if c > 3)
        over2 = sum(1 for c in section_counts if c > 2)
        print(f"  Media por secao: {avg:.2f} em-dashes "
              f"({len(section_counts)} secoes, {over2} com >2, {over3} com >3)")


if __name__ == '__main__':
    main()
