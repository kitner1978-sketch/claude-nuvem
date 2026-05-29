#!/usr/bin/env python3
"""
antiIA_check.py — Detector de marcadores típicos de texto gerado por IA
Uso: python antiIA_check.py <arquivo.md> [--fix]

Detecta 8 categorias de marcadores. Com --fix, sugere correções automáticas
para os casos mais simples (advérbios, frases-moldura).
"""

import re
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# ═══════════════════════════════════════════════════════
# CONFIGURAÇÃO DOS FILTROS
# ═══════════════════════════════════════════════════════

# F1 — Travessões em excesso (pares — ... —)
DASH_PAIR_LIMIT_PER_500_WORDS = 3

# F3 — Advérbios intensificadores vazios
ADVERBIOS_VAZIOS = [
    "notadamente", "indubitavelmente", "inequivocamente", "inegavelmente",
    "certamente", "claramente", "evidentemente", "manifestamente",
    "incontroversamente", "incontestavelmente", "inelutavelmente",
    "irrefutavelmente", "indiscutivelmente", "inquestionavelmente",
    "inarredavelmente", "sobremaneira", "mormente",
]

# F4 — Conectivos repetitivos (máx 1 por seção)
CONECTIVOS_REPETITIVOS = [
    "nesse contexto", "nesse sentido", "sob essa perspectiva",
    "à luz do exposto", "nessa esteira", "nessa senda", "nessa toada",
    "por essa razão", "sob esse prisma", "sob esse viés",
    "dessa forma", "desse modo", "diante disso", "ante o exposto",
    "nessa linha", "por conseguinte", "em consequência",
]

# F5 — Frases-moldura (proibidas como abertura de parágrafo)
FRASES_MOLDURA = [
    r"[Cc]umpre ressaltar que",
    r"[Ii]mporta destacar que",
    r"[Rr]egistre-se que",
    r"[Ss]aliente-se que",
    r"[Dd]estaque-se que",
    r"[Cc]onvém observar que",
    r"[Cc]abe mencionar que",
    r"[Mm]erece destaque",
    r"[Vv]ale registrar que",
    r"[Ii]mperioso consignar que",
    r"[Nn]ão se pode olvidar que",
    r"[Ff]orçoso reconhecer que",
    r"[Éé] de se notar que",
    r"[Ii]mpende registrar que",
    r"[Aa]figura-se relevante",
    r"[Rr]eleva notar que",
    r"[Cc]umpre consignar que",
    r"[Éé] importante ressaltar que",
    r"[Cc]umpre destacar que",
    r"[Ii]nsta salientar que",
    r"[Cc]umpre observar que",
    r"[Cc]umpre registrar que",
    r"[Nn]ecessário se faz",
    r"[Mm]ister se faz",
]

# F7 — Adjetivação tripla: 3+ adjetivos coordenados por vírgula/e
# Sufixos mais restritos a adjetivos verdadeiros (exclui substantivos -ção, -mento, etc.)
TRIPLA_ADJ_PATTERN = re.compile(
    r'\b(\w+(?:vel|ivo|iva|oso|osa|nte|ico|ica|ido|ida|ual|vel|rio|ria)s?),\s+'
    r'(\w+(?:vel|ivo|iva|oso|osa|nte|ico|ica|ido|ida|ual|vel|rio|ria)s?)\s+e\s+'
    r'(\w+(?:vel|ivo|iva|oso|osa|nte|ico|ica|ido|ida|ual|vel|rio|ria)s?)\b',
    re.IGNORECASE
)

# F8 — "Portanto" e "Assim" como muletas (máx 1 por seção)
PORTANTO_PATTERN = re.compile(r'\bPortanto\b', re.IGNORECASE)
ASSIM_CONCLUSIVO = re.compile(r'(?:^|\.\s+)Assim,', re.MULTILINE)


def split_sections(text):
    """Divide o texto em seções (### headings)."""
    sections = []
    current_title = "(Abertura)"
    current_lines = []

    for line in text.split('\n'):
        if line.startswith('### '):
            if current_lines:
                sections.append((current_title, '\n'.join(current_lines)))
            current_title = line.strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, '\n'.join(current_lines)))

    return sections


def count_words(text):
    """Conta palavras em texto limpo."""
    clean = re.sub(r'[#|:\-{}\[\]>*_~`]', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return len(clean.split())


def check_f1_travessoes(sections):
    """F1 — Travessões em excesso (pares intercalados, não listas)."""
    findings = []
    for title, content in sections:
        # Contar pares intercalados de travessões (— texto — dentro de frase)
        # Excluir travessões no início de linha (listas, enumerações)
        pairs = 0
        for line in content.split('\n'):
            stripped = line.strip()
            # Pular linhas que começam com — (listas)
            if stripped.startswith('—') or stripped.startswith('-'):
                continue
            # Contar pares dentro da linha (intercalações)
            pairs += len(re.findall(r'(?<!^)\s—\s[^—\n]+\s—\s', line))
            # Também contar travessão no meio da frase seguido de outro
            pairs += max(0, line.count(' — ') - 1) // 2  # pares aproximados

        # Recalcular: contar ocorrências de " — " em linhas que não são de lista
        non_list_dashes = 0
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('—') or stripped.startswith('-'):
                continue
            non_list_dashes += line.count(' — ')

        # Pares = metade dos travessões inline (arredondado para baixo)
        inline_pairs = non_list_dashes // 2

        words = count_words(content)
        blocks_500 = max(1, words / 500)
        ratio = inline_pairs / blocks_500

        if ratio > DASH_PAIR_LIMIT_PER_500_WORDS:
            findings.append({
                'section': title,
                'count': inline_pairs,
                'words': words,
                'ratio_per_500': round(ratio, 1),
                'limit': DASH_PAIR_LIMIT_PER_500_WORDS,
            })

    return findings


def check_f2_sanduiche(sections):
    """F2 — Estrutura sanduíche (heurística: parágrafo que abre genérico e fecha reiterando)."""
    findings = []
    # Aberturas genéricas típicas de sanduíche
    generic_openers = [
        r'^[A-Z][\w\s]+ (?:é|constitui|representa|configura) (?:um|uma|o|a) (?:dos|das|tema|questão|aspecto|instituto|matéria|ponto)',
        r'^(?:No|Na|Em) (?:matéria|âmbito|contexto|seara) d[eao]s?\s',
        r'^(?:A|O) (?:temática|tema|assunto|questão|matéria|problema) d[eao]s?\s.*(?:é|reveste|assume|possui).*(?:relevância|importância|destaque|interesse)',
    ]
    # Fechamentos reiterativos
    reiteration_closers = [
        r'(?:portanto|assim|dessa forma|desse modo|nesse sentido),?\s.*(?:resta|fica|torna-se).*(?:claro|evidente|demonstrado|comprovado|inequívoco)',
        r'(?:portanto|assim),?\s.*(?:fundamental|essencial|imprescindível|indispensável)',
    ]

    for title, content in sections:
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith(('###', '####', ':::', '|', '---'))]
        for i, para in enumerate(paragraphs):
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', para) if s.strip()]
            if len(sentences) < 3:
                continue

            opens_generic = any(re.search(pat, sentences[0]) for pat in generic_openers)
            closes_reiterate = any(re.search(pat, sentences[-1], re.IGNORECASE) for pat in reiteration_closers)

            if opens_generic and closes_reiterate:
                preview = sentences[0][:80] + '...' if len(sentences[0]) > 80 else sentences[0]
                findings.append({
                    'section': title,
                    'paragraph': i + 1,
                    'preview': preview,
                })

    return findings


def check_f3_adverbios(text):
    """F3 — Advérbios intensificadores vazios."""
    findings = []
    text_lower = text.lower()
    for adv in ADVERBIOS_VAZIOS:
        count = text_lower.count(adv)
        if count > 0:
            # Encontrar as linhas
            lines = []
            for num, line in enumerate(text.split('\n'), 1):
                if adv in line.lower():
                    lines.append(num)
            findings.append({
                'adverbio': adv,
                'count': count,
                'lines': lines,
            })
    return findings


def check_f4_conectivos(sections):
    """F4 — Conectivos repetitivos (>1 do mesmo por seção)."""
    findings = []
    for title, content in sections:
        content_lower = content.lower()
        for conect in CONECTIVOS_REPETITIVOS:
            count = content_lower.count(conect.lower())
            if count > 1:
                findings.append({
                    'section': title,
                    'conectivo': conect,
                    'count': count,
                })
    return findings


def check_f5_molduras(text):
    """F5 — Frases-moldura como abertura de parágrafo."""
    findings = []
    paragraphs = text.split('\n\n')
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para or para.startswith(('#', ':::', '|', '---', '>')):
            continue
        for pattern in FRASES_MOLDURA:
            if re.match(pattern, para):
                preview = para[:80] + '...' if len(para) > 80 else para
                findings.append({
                    'paragraph': i + 1,
                    'pattern': pattern,
                    'preview': preview,
                })
                break
    return findings


def check_f6_paralelismo(text):
    """F6 — Paralelismo excessivo (heurística: 3+ alíneas com mesmo verbo inicial)."""
    findings = []
    # Palavras que iniciam alíneas de forma legítima (substantivos para listas naturais)
    legit_starters = {
        'segurado', 'deficiência', 'tempo', 'idade', 'aposentadoria',
        'benefício', 'para', 'por', 'lei', 'art', 'artigo', 'inciso',
    }
    # Procurar blocos com (a)/(b)/(c) ou alíneas letradas
    alinea_blocks = re.findall(
        r'(?:(?:^|\n)\s*\([a-z]\)\s+.+){3,}', text, re.MULTILINE
    )
    for block in alinea_blocks:
        items = re.findall(r'\([a-z]\)\s+(\w+)', block)
        if len(items) >= 3:
            # Verificar se o mesmo verbo inicia 3+ alíneas
            verb_counts = Counter(items)
            for verb, count in verb_counts.items():
                if count >= 3 and verb.lower() not in legit_starters:
                    findings.append({
                        'verb': verb,
                        'count': count,
                        'preview': block[:120] + '...',
                    })
    return findings


def check_f7_adjetivacao_tripla(text):
    """F7 — Adjetivação tripla (3 adjetivos coordenados)."""
    findings = []
    for match in TRIPLA_ADJ_PATTERN.finditer(text):
        adj1, adj2, adj3 = match.group(1), match.group(2), match.group(3)
        # Filtrar falsos positivos: verificar se são realmente adjetivos
        # (heurística: terminam em -o, -a, -os, -as, -e, -es, -al, -ar, -el, -vel)
        adj_endings = ('o', 'a', 'os', 'as', 'e', 'es', 'al', 'ar', 'el', 'vel', 'nte', 'ntes')
        if (adj1.lower().endswith(adj_endings) and
            adj2.lower().endswith(adj_endings) and
            adj3.lower().endswith(adj_endings)):
            findings.append({
                'match': match.group(0),
                'position': match.start(),
            })
    return findings


def check_f8_portanto_assim(sections):
    """F8 — 'Portanto' e 'Assim' como muletas (>1 por seção)."""
    findings = []
    for title, content in sections:
        portanto_count = len(PORTANTO_PATTERN.findall(content))
        assim_count = len(ASSIM_CONCLUSIVO.findall(content))

        if portanto_count > 1:
            findings.append({
                'section': title,
                'word': 'Portanto',
                'count': portanto_count,
            })
        if assim_count > 1:
            findings.append({
                'section': title,
                'word': 'Assim (conclusivo)',
                'count': assim_count,
            })
    return findings


def run_all_checks(filepath):
    """Executa todos os 8 filtros e retorna relatório."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remover frontmatter YAML
    if text.startswith('---'):
        end = text.find('---', 3)
        if end > 0:
            text = text[end + 3:]

    sections = split_sections(text)
    total_words = count_words(text)

    results = {
        'file': str(filepath),
        'words': total_words,
        'sections': len(sections),
        'filters': {}
    }

    # F1 — Travessões
    f1 = check_f1_travessoes(sections)
    results['filters']['F1_travessoes'] = f1

    # F2 — Sanduíche
    f2 = check_f2_sanduiche(sections)
    results['filters']['F2_sanduiche'] = f2

    # F3 — Advérbios
    f3 = check_f3_adverbios(text)
    results['filters']['F3_adverbios'] = f3

    # F4 — Conectivos
    f4 = check_f4_conectivos(sections)
    results['filters']['F4_conectivos'] = f4

    # F5 — Frases-moldura
    f5 = check_f5_molduras(text)
    results['filters']['F5_molduras'] = f5

    # F6 — Paralelismo
    f6 = check_f6_paralelismo(text)
    results['filters']['F6_paralelismo'] = f6

    # F7 — Adjetivação tripla
    f7 = check_f7_adjetivacao_tripla(text)
    results['filters']['F7_adj_tripla'] = f7

    # F8 — Portanto/Assim
    f8 = check_f8_portanto_assim(sections)
    results['filters']['F8_portanto_assim'] = f8

    return results


def print_report(results):
    """Imprime relatório formatado."""
    print(f"\n{'='*60}")
    print(f"  RELATÓRIO ANTI-IA: {Path(results['file']).name}")
    print(f"  {results['words']} palavras | {results['sections']} seções")
    print(f"{'='*60}\n")

    total_issues = 0
    severity_map = {
        'F1_travessoes': '[!]',
        'F2_sanduiche': '[X]',
        'F3_adverbios': '[X]',
        'F4_conectivos': '[!]',
        'F5_molduras': '[X]',
        'F6_paralelismo': '[!]',
        'F7_adj_tripla': '[!]',
        'F8_portanto_assim': '[!]',
    }

    filter_names = {
        'F1_travessoes': 'F1 — Travessões em excesso',
        'F2_sanduiche': 'F2 — Estrutura sanduíche',
        'F3_adverbios': 'F3 — Advérbios intensificadores vazios',
        'F4_conectivos': 'F4 — Conectivos repetitivos',
        'F5_molduras': 'F5 — Frases-moldura',
        'F6_paralelismo': 'F6 — Paralelismo excessivo',
        'F7_adj_tripla': 'F7 — Adjetivação tripla',
        'F8_portanto_assim': 'F8 — Portanto/Assim como muletas',
    }

    for key, findings in results['filters'].items():
        count = len(findings)
        total_issues += count
        icon = severity_map.get(key, '⚪')
        name = filter_names.get(key, key)

        if count == 0:
            print(f"  [OK] {name}: OK")
        else:
            print(f"  {icon} {name}: {count} ocorrencia(s)")

            if key == 'F1_travessoes':
                for f in findings:
                    print(f"     └─ {f['section']}: {f['count']} pares "
                          f"({f['ratio_per_500']}/500w, limite {f['limit']})")

            elif key == 'F2_sanduiche':
                for f in findings:
                    print(f"     └─ {f['section']}, §{f['paragraph']}: {f['preview']}")

            elif key == 'F3_adverbios':
                for f in findings:
                    print(f"     └─ \"{f['adverbio']}\" × {f['count']} "
                          f"(linhas {', '.join(map(str, f['lines'][:5]))})")

            elif key == 'F4_conectivos':
                for f in findings:
                    print(f"     └─ {f['section']}: \"{f['conectivo']}\" × {f['count']}")

            elif key == 'F5_molduras':
                for f in findings:
                    print(f"     └─ §{f['paragraph']}: {f['preview']}")

            elif key == 'F6_paralelismo':
                for f in findings:
                    print(f"     └─ verbo \"{f['verb']}\" × {f['count']}: {f['preview'][:80]}")

            elif key == 'F7_adj_tripla':
                for f in findings:
                    print(f"     └─ \"{f['match']}\"")

            elif key == 'F8_portanto_assim':
                for f in findings:
                    print(f"     └─ {f['section']}: \"{f['word']}\" × {f['count']}")

        print()

    # Score
    max_score = 100
    penalty = min(total_issues * 5, 80)  # cada issue perde 5 pontos, máx 80
    score = max_score - penalty

    print(f"{'─'*60}")
    print(f"  TOTAL: {total_issues} marcador(es) detectado(s)")
    print(f"  SCORE ANTI-IA: {score}/100", end='')
    if score >= 90:
        print(" [EXCELENTE]")
    elif score >= 70:
        print(" [BOM, REVISAR]")
    elif score >= 50:
        print(" [NECESSITA REVISAO]")
    else:
        print(" [REVISAO URGENTE]")
    print(f"{'─'*60}\n")

    return total_issues


def main():
    if len(sys.argv) < 2:
        print("Uso: python antiIA_check.py <arquivo.md>")
        print("     python antiIA_check.py D:\\Projeto Livro\\output\\rascunhos\\cap_06_rascunho.md")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"ERRO: Arquivo não encontrado: {filepath}")
        sys.exit(1)

    results = run_all_checks(filepath)
    issues = print_report(results)
    sys.exit(0 if issues == 0 else 1)


if __name__ == '__main__':
    main()
