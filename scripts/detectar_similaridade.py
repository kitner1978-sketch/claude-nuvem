#!/usr/bin/env python3
"""
FASE 4 — Detecção de similaridade / risco de reprodução não atribuída
=====================================================================
Abordagem: como não temos acesso aos textos doutrinários originais para
comparação direta, usamos indicadores indiretos:

1. Densidade citacional por capítulo (citações / 1000 palavras)
2. Trechos longos sem qualquer citação (>400 palavras contínuas)
3. Definições doutrinárias sem atribuição (padrões "pode ser definido como",
   "segundo a doutrina", "classifica-se em" etc.)
4. Frases formulaicas de doutrina previdenciária conhecida
5. Análise de homogeneidade estilística (desvio de complexidade lexical)
6. Cobertura citacional vs. conteúdo doutrinário

Saída: output/relatorio_similaridade.txt
"""

import re
import os
import math
from pathlib import Path
from collections import Counter, defaultdict

# ── Caminhos ──────────────────────────────────────────────
BASE = Path(r"D:\Projeto Livro")
RASCUNHOS = BASE / "output" / "rascunhos"
OUTPUT = BASE / "output" / "relatorio_similaridade.txt"


# ── 1. Carregar capítulos ─────────────────────────────────
def load_chapters():
    chapters = {}
    for f in sorted(RASCUNHOS.glob("cap_*_rascunho.md")):
        num = int(re.search(r"cap_(\d+)", f.name).group(1))
        text = f.read_text(encoding="utf-8", errors="replace")
        chapters[num] = text
    return chapters


# ── 2. Densidade citacional ──────────────────────────────
# Padrões de citação doutrinária (ABNT autor-data)
CITE_PATTERNS = [
    r"\([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ]+(?:\s*;\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ]+)*,\s*\d{4}(?:\s*,\s*p\.\s*\d+(?:-\d+)?)?\)",
    # (IBRAHIM, 2025), (CASTRO; LAZZARI, 2025, p. 123)
    r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+\s+\(\d{4}(?:,\s*p\.\s*\d+(?:-\d+)?)?\)",
    # Ibrahim (2025), Savaris (2022, p. 342)
    r"(?:segundo|conforme|para|de acordo com|nos termos de|na lição de|nas palavras de|como ensina|como leciona)\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+",
    # "segundo Ibrahim", "conforme Savaris"
]

def count_citations(text):
    """Conta citações doutrinárias no texto."""
    total = 0
    positions = []
    for pat in CITE_PATTERNS:
        for m in re.finditer(pat, text):
            total += 1
            positions.append(m.start())
    return total, sorted(set(positions))


def word_count(text):
    """Conta palavras no texto."""
    # Remove markdown/formatação
    clean = re.sub(r'[#*_`|>~\[\]{}()]', ' ', text)
    clean = re.sub(r'https?://\S+', '', clean)
    clean = re.sub(r':::.*?:::', '', clean, flags=re.DOTALL)
    words = clean.split()
    return len(words)


def citation_density(chapters):
    """Calcula citações por 1000 palavras por capítulo."""
    results = {}
    for num, text in sorted(chapters.items()):
        cites, positions = count_citations(text)
        wc = word_count(text)
        density = (cites / wc * 1000) if wc > 0 else 0
        results[num] = {
            'citacoes': cites,
            'palavras': wc,
            'densidade': density,
            'posicoes': positions
        }
    return results


# ── 3. Trechos longos sem citação ────────────────────────
def find_uncited_stretches(text, min_words=400):
    """
    Encontra trechos de texto corrido com mais de min_words palavras
    sem nenhuma citação doutrinária.
    """
    # Dividir em parágrafos
    paragraphs = re.split(r'\n\s*\n', text)

    stretches = []
    current_stretch = []
    current_words = 0
    current_start_line = 0

    line_count = 0
    for para in paragraphs:
        para_stripped = para.strip()
        if not para_stripped:
            line_count += para.count('\n') + 1
            continue

        # Pular headers, boxes, tabelas, YAML frontmatter
        if (para_stripped.startswith('#') or
            para_stripped.startswith(':::') or
            para_stripped.startswith('|') or
            para_stripped.startswith('---') or
            para_stripped.startswith('tags:') or
            para_stripped.startswith('```') or
            len(para_stripped) < 50):
            # Reset stretch se encontrar separador
            if current_words >= min_words:
                stretches.append({
                    'inicio_linha': current_start_line,
                    'palavras': current_words,
                    'preview': ' '.join(' '.join(p.split()[:15]) for p in current_stretch[:2])[:200]
                })
            current_stretch = []
            current_words = 0
            line_count += para.count('\n') + 1
            continue

        # Verificar se tem citação
        has_cite = False
        for pat in CITE_PATTERNS:
            if re.search(pat, para_stripped):
                has_cite = True
                break

        if has_cite:
            # Citação encontrada — salvar stretch anterior se longo
            if current_words >= min_words:
                stretches.append({
                    'inicio_linha': current_start_line,
                    'palavras': current_words,
                    'preview': ' '.join(' '.join(p.split()[:15]) for p in current_stretch[:2])[:200]
                })
            current_stretch = []
            current_words = 0
        else:
            if not current_stretch:
                current_start_line = line_count
            current_stretch.append(para_stripped)
            current_words += len(para_stripped.split())

        line_count += para.count('\n') + 1

    # Último stretch
    if current_words >= min_words:
        stretches.append({
            'inicio_linha': current_start_line,
            'palavras': current_words,
            'preview': ' '.join(' '.join(p.split()[:15]) for p in current_stretch[:2])[:200]
        })

    return stretches


# ── 4. Definições doutrinárias sem atribuição ────────────
DEFINITION_PATTERNS = [
    (r"(?:pode ser |é )?defini[dr][oa]s?\s+como\s+", "definição sem atribuição"),
    (r"(?:classifica|divide|subdivide)-se\s+em\s+", "classificação doutrinária"),
    (r"(?:a |na )?doutrina\s+(?:majoritária\s+)?(?:entende|sustenta|defende|classifica|considera|denomina)", "posição doutrinária sem autor"),
    (r"(?:a |na )?(?:melhor |boa )?doutrina\s+", "referência genérica à doutrina"),
    (r"(?:segundo|conforme)\s+(?:a\s+)?(?:doutrina|maioria|corrente)\s+(?:majoritária|dominante|prevalecente)", "doutrina majoritária sem fonte"),
    (r"(?:há|existe)\s+(?:na doutrina\s+)?(?:divergência|controvérsia|discussão|debate)\s+(?:doutrinári[ao]|sobre|acerca|quanto)", "controvérsia doutrinária genérica"),
    (r"parte\s+da\s+doutrina\s+(?:entende|sustenta|defende|considera)", "parte da doutrina sem especificar"),
    (r"(?:conceitu[ao]|conceit[uo])\s+(?:como|de)\s+", "conceituação sem fonte"),
    (r"nas?\s+palavras?\s+d[eao]\s+(?:ilustre|renomado|consagrado)\s+", "citação com adjetivo sem identificar autor"),
    (r"o\s+(?:instituto|conceito|princípio)\s+(?:d[eao]\s+)?[\w\s]+(?:surgiu|originou|nasceu|tem origem)\s+", "origem histórica de instituto"),
]

def find_unattributed_definitions(text, cap_num):
    """Encontra padrões de definição/classificação doutrinária sem citação."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        line_lower = line.lower().strip()
        if not line_lower or line_lower.startswith('#') or line_lower.startswith('|'):
            continue

        for pattern, desc in DEFINITION_PATTERNS:
            match = re.search(pattern, line_lower)
            if match:
                # Verificar se há citação na mesma linha ou na próxima
                context = line
                if i < len(lines):
                    context += " " + lines[i]  # incluir próxima linha

                has_cite = False
                for cpat in CITE_PATTERNS:
                    if re.search(cpat, context):
                        has_cite = True
                        break

                if not has_cite:
                    # Extrair contexto legível
                    ctx = line.strip()
                    if len(ctx) > 150:
                        # Centralizar no match
                        start = max(0, match.start() - 40)
                        end = min(len(ctx), match.end() + 110)
                        ctx = ctx[start:end]

                    findings.append({
                        'linha': i,
                        'tipo': desc,
                        'contexto': ctx[:200]
                    })
                break  # uma detecção por linha basta

    return findings


# ── 5. Frases formulaicas de doutrina previdenciária ─────
FORMULAIC_PHRASES = [
    # Frases que aparecem textualmente em doutrina conhecida
    (r"a\s+previdência\s+social\s+(?:é|constitui)\s+(?:um\s+)?direito\s+social\s+fundamental",
     "definição padrão de previdência social"),
    (r"natureza\s+(?:eminentemente\s+)?(?:alimentar|pro\s*-?\s*misero|protetiva)\s+d[oa]s?\s+benefícios?",
     "natureza alimentar — fórmula doutrinária recorrente"),
    (r"in\s+dubio\s+pro\s+(?:misero|operario|segurado)",
     "princípio pro misero — verificar se contextualizado"),
    (r"caráter\s+(?:contributivo|solidário)\s+e\s+(?:de\s+filiação\s+)?obrigatóri[ao]",
     "definição constitucional — verificar se há citação do art. 201 CF"),
    (r"(?:princípio|regra)\s+d[ao]\s+(?:contrapartida|preexistência\s+d[eo]\s+custeio|precedência\s+da\s+fonte)",
     "princípio da contrapartida — conceito doutrinário"),
    (r"(?:tríplice|tripla)\s+forma\s+de\s+custeio",
     "tríplice custeio — conceito clássico"),
    (r"seletividade\s+e\s+distributividade\s+na\s+prestação",
     "princípio constitucional — verificar contextualização"),
    (r"universalidade\s+d[ae]\s+(?:cobertura|atendimento)\s+e\s+d[oe]\s+atendimento",
     "princípio constitucional — verificar contextualização"),
    (r"(?:teoria|tese)\s+d[ao]\s+(?:incapacidade\s+social|desamparo\s+social)",
     "teoria doutrinária — requer atribuição"),
    (r"a\s+(?:aposentadoria|pensão|auxílio)\s+(?:é|constitui|representa)\s+(?:um\s+)?(?:direito|prestação)\s+(?:de\s+)?(?:trato\s+sucessivo|prestação\s+continuada)",
     "classificação como trato sucessivo — doutrinária"),
]

def find_formulaic_phrases(text, cap_num):
    """Detecta frases formulaicas de doutrina previdenciária."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        line_lower = line.lower().strip()
        if not line_lower or line_lower.startswith('#'):
            continue

        for pattern, desc in FORMULAIC_PHRASES:
            match = re.search(pattern, line_lower)
            if match:
                ctx = line.strip()
                if len(ctx) > 200:
                    start = max(0, match.start() - 50)
                    end = min(len(ctx), match.end() + 150)
                    ctx = ctx[start:end]

                findings.append({
                    'linha': i,
                    'tipo': desc,
                    'contexto': ctx[:200]
                })
                break

    return findings


# ── 6. Homogeneidade estilística (TTR — Type-Token Ratio) ─
def compute_lexical_stats(text):
    """
    Calcula estatísticas lexicais para detectar variações de estilo.
    TTR baixo = texto repetitivo/formulaico
    TTR alto = vocabulário variado
    Grandes desvios entre seções podem indicar trechos de fontes diferentes.
    """
    # Limpar texto
    clean = re.sub(r'[#*_`|>~\[\]{}()""''"\']', ' ', text)
    clean = re.sub(r'https?://\S+', '', clean)
    clean = re.sub(r'R\$\s*[\d.,]+', '', clean)
    clean = re.sub(r'\d+', '', clean)
    clean = re.sub(r':::.*?:::', '', clean, flags=re.DOTALL)

    words = [w.lower() for w in clean.split() if len(w) > 2]
    if not words:
        return {'ttr': 0, 'avg_word_len': 0, 'hapax': 0, 'total': 0}

    types = set(words)
    total = len(words)

    # TTR normalizado (para janelas de 1000 palavras para comparabilidade)
    window = 1000
    ttr_samples = []
    for i in range(0, total - window + 1, window // 2):
        chunk = words[i:i+window]
        ttr_samples.append(len(set(chunk)) / len(chunk))

    avg_ttr = sum(ttr_samples) / len(ttr_samples) if ttr_samples else len(types) / total

    # Comprimento médio de palavra
    avg_len = sum(len(w) for w in words) / total

    # Hapax legomena (palavras que aparecem só 1 vez)
    freq = Counter(words)
    hapax = sum(1 for w, c in freq.items() if c == 1)
    hapax_ratio = hapax / len(types) if types else 0

    # Desvio padrão do TTR por janelas (alta variação = possível mistura de fontes)
    if len(ttr_samples) > 1:
        mean_ttr = sum(ttr_samples) / len(ttr_samples)
        variance = sum((x - mean_ttr)**2 for x in ttr_samples) / len(ttr_samples)
        ttr_std = math.sqrt(variance)
    else:
        ttr_std = 0

    return {
        'ttr': avg_ttr,
        'ttr_std': ttr_std,
        'avg_word_len': avg_len,
        'hapax_ratio': hapax_ratio,
        'total_words': total,
        'unique_words': len(types)
    }


# ── 7. Cobertura citacional por tipo de conteúdo ────────
CONTENT_TYPES = {
    'conceito': r'(?:conceito|definição|noção|acepção)\s+(?:de|do|da)\s+',
    'classificacao': r'(?:classifica|categoriza|tipifica|divide|subdivide)',
    'principio': r'(?:princípio|postulado)\s+(?:de|do|da)\s+',
    'historico': r'(?:históric|evolução|origem|gênese|surgimento)',
    'jurisprudencia': r'(?:STF|STJ|TNU|TRF|Súmula|Tema\s+\d|RE\s+\d|REsp|AgRg)',
    'legislacao': r'(?:art\.\s*\d|Lei\s+(?:n\.\s*)?\d|EC\s+\d|CF/88|Constituição)',
    'doutrina_explicita': r'(?:doutrina|doutrinador|autor|pensamento\s+jurídico)',
}

def analyze_content_coverage(text):
    """Analisa que tipos de conteúdo existem e se têm citações próximas."""
    results = {}
    for tipo, pattern in CONTENT_TYPES.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        cited = 0
        uncited = 0
        for m in matches:
            # Janela de 500 caracteres ao redor
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 300)
            window = text[start:end]

            has_cite = False
            for cpat in CITE_PATTERNS:
                if re.search(cpat, window):
                    has_cite = True
                    break

            if has_cite:
                cited += 1
            else:
                uncited += 1

        results[tipo] = {'total': len(matches), 'citados': cited, 'nao_citados': uncited}

    return results


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("DETECÇÃO DE SIMILARIDADE / RISCO DE REPRODUÇÃO — FASE 4")
    print("=" * 70)

    chapters = load_chapters()
    print(f"\n  {len(chapters)} capítulos carregados\n")

    report_lines = []
    report_lines.append("RELATÓRIO DE SIMILARIDADE — FASE 4")
    report_lines.append("=" * 70)
    report_lines.append(f"Data: 2026-05-15")
    report_lines.append(f"Capítulos analisados: {len(chapters)}")
    report_lines.append("")

    # ── Análise 1: Densidade citacional ───────────────────
    print("  1. Calculando densidade citacional...")
    density = citation_density(chapters)

    report_lines.append("ANÁLISE 1: DENSIDADE CITACIONAL")
    report_lines.append("-" * 40)
    report_lines.append(f"  {'Cap':>5}  {'Palavras':>8}  {'Citações':>8}  {'Cit/1000p':>10}  {'Avaliação'}")
    report_lines.append(f"  {'─'*5}  {'─'*8}  {'─'*8}  {'─'*10}  {'─'*20}")

    densities = []
    for num in sorted(density.keys()):
        d = density[num]
        densities.append(d['densidade'])

        if d['densidade'] < 0.5:
            avaliacao = "⚠ MUITO BAIXA"
        elif d['densidade'] < 1.5:
            avaliacao = "! BAIXA"
        elif d['densidade'] < 3.0:
            avaliacao = "~ ADEQUADA"
        else:
            avaliacao = "✓ BOA"

        report_lines.append(f"  {num:>5}  {d['palavras']:>8}  {d['citacoes']:>8}  {d['densidade']:>10.2f}  {avaliacao}")

    avg_density = sum(densities) / len(densities) if densities else 0
    report_lines.append(f"\n  Média geral: {avg_density:.2f} citações/1000 palavras")
    report_lines.append("")

    print(f"     Média: {avg_density:.2f} cit/1000 palavras")

    # ── Análise 2: Trechos longos sem citação ─────────────
    print("  2. Buscando trechos longos sem citação...")

    total_stretches = 0
    all_stretches = {}
    for num, text in sorted(chapters.items()):
        stretches = find_uncited_stretches(text)
        if stretches:
            all_stretches[num] = stretches
            total_stretches += len(stretches)

    report_lines.append("\nANÁLISE 2: TRECHOS LONGOS SEM CITAÇÃO (>400 palavras)")
    report_lines.append("-" * 40)
    report_lines.append(f"  Total de trechos encontrados: {total_stretches}")
    report_lines.append("")

    for num in sorted(all_stretches.keys()):
        for s in all_stretches[num]:
            severity = "[!!!]" if s['palavras'] > 800 else "[!!]" if s['palavras'] > 600 else "[!]"
            report_lines.append(f"  {severity} Cap {num} (linha ~{s['inicio_linha']}, {s['palavras']} palavras)")
            report_lines.append(f"      início: {s['preview'][:150]}...")
            report_lines.append("")

    print(f"     {total_stretches} trechos encontrados")

    # ── Análise 3: Definições sem atribuição ──────────────
    print("  3. Buscando definições doutrinárias sem atribuição...")

    total_defs = 0
    all_defs = {}
    for num, text in sorted(chapters.items()):
        defs = find_unattributed_definitions(text, num)
        if defs:
            all_defs[num] = defs
            total_defs += len(defs)

    report_lines.append("\nANÁLISE 3: DEFINIÇÕES/CLASSIFICAÇÕES SEM ATRIBUIÇÃO")
    report_lines.append("-" * 40)
    report_lines.append(f"  Total: {total_defs} ocorrências")
    report_lines.append("")

    for num in sorted(all_defs.keys()):
        report_lines.append(f"  Cap {num}:")
        for d in all_defs[num]:
            report_lines.append(f"    [!!] Linha {d['linha']}: {d['tipo']}")
            report_lines.append(f"         {d['contexto'][:150]}")
        report_lines.append("")

    print(f"     {total_defs} definições sem atribuição")

    # ── Análise 4: Frases formulaicas ─────────────────────
    print("  4. Buscando frases formulaicas de doutrina...")

    total_form = 0
    all_form = {}
    for num, text in sorted(chapters.items()):
        forms = find_formulaic_phrases(text, num)
        if forms:
            all_form[num] = forms
            total_form += len(forms)

    report_lines.append("\nANÁLISE 4: FRASES FORMULAICAS DE DOUTRINA PREVIDENCIÁRIA")
    report_lines.append("-" * 40)
    report_lines.append(f"  Total: {total_form} ocorrências")
    report_lines.append("")

    for num in sorted(all_form.keys()):
        report_lines.append(f"  Cap {num}:")
        for f in all_form[num]:
            report_lines.append(f"    [!] Linha {f['linha']}: {f['tipo']}")
            report_lines.append(f"        {f['contexto'][:150]}")
        report_lines.append("")

    print(f"     {total_form} frases formulaicas")

    # ── Análise 5: Estatísticas lexicais ──────────────────
    print("  5. Calculando estatísticas lexicais...")

    report_lines.append("\nANÁLISE 5: HOMOGENEIDADE ESTILÍSTICA (TTR)")
    report_lines.append("-" * 40)
    report_lines.append("  (TTR = Type-Token Ratio; desvio alto = possível mistura de fontes)")
    report_lines.append(f"  {'Cap':>5}  {'TTR':>6}  {'TTR σ':>7}  {'Tam.Pal':>8}  {'Hapax%':>7}  {'Observação'}")
    report_lines.append(f"  {'─'*5}  {'─'*6}  {'─'*7}  {'─'*8}  {'─'*7}  {'─'*25}")

    all_ttrs = []
    all_stds = []
    lex_stats = {}
    for num, text in sorted(chapters.items()):
        stats = compute_lexical_stats(text)
        lex_stats[num] = stats
        all_ttrs.append(stats['ttr'])
        all_stds.append(stats['ttr_std'])

        obs = ""
        if stats['ttr_std'] > 0.06:
            obs = "⚠ VARIAÇÃO ALTA"
        elif stats['ttr_std'] > 0.04:
            obs = "~ variação moderada"
        else:
            obs = "✓ homogêneo"

        report_lines.append(
            f"  {num:>5}  {stats['ttr']:.3f}  {stats['ttr_std']:.4f}  "
            f"{stats['avg_word_len']:.2f}  {stats['hapax_ratio']:.1%}  {obs}"
        )

    avg_ttr = sum(all_ttrs) / len(all_ttrs) if all_ttrs else 0
    avg_std = sum(all_stds) / len(all_stds) if all_stds else 0
    report_lines.append(f"\n  Média TTR: {avg_ttr:.3f}  |  Média desvio: {avg_std:.4f}")
    report_lines.append("")

    print(f"     TTR médio: {avg_ttr:.3f}, desvio médio: {avg_std:.4f}")

    # ── Análise 6: Cobertura por tipo de conteúdo ─────────
    print("  6. Analisando cobertura citacional por tipo de conteúdo...")

    report_lines.append("\nANÁLISE 6: COBERTURA CITACIONAL POR TIPO DE CONTEÚDO")
    report_lines.append("-" * 40)

    global_coverage = defaultdict(lambda: {'total': 0, 'citados': 0, 'nao_citados': 0})
    chapter_coverage = {}

    for num, text in sorted(chapters.items()):
        cov = analyze_content_coverage(text)
        chapter_coverage[num] = cov
        for tipo, vals in cov.items():
            global_coverage[tipo]['total'] += vals['total']
            global_coverage[tipo]['citados'] += vals['citados']
            global_coverage[tipo]['nao_citados'] += vals['nao_citados']

    report_lines.append(f"  {'Tipo':<25}  {'Total':>6}  {'Citados':>8}  {'S/Cit':>6}  {'Cobertura':>10}")
    report_lines.append(f"  {'─'*25}  {'─'*6}  {'─'*8}  {'─'*6}  {'─'*10}")

    for tipo in ['conceito', 'classificacao', 'principio', 'historico',
                 'doutrina_explicita', 'jurisprudencia', 'legislacao']:
        v = global_coverage[tipo]
        pct = (v['citados'] / v['total'] * 100) if v['total'] > 0 else 0
        flag = " ⚠" if tipo in ('conceito', 'classificacao', 'principio', 'doutrina_explicita') and pct < 30 else ""
        report_lines.append(
            f"  {tipo:<25}  {v['total']:>6}  {v['citados']:>8}  {v['nao_citados']:>6}  {pct:>9.1f}%{flag}"
        )

    report_lines.append("")

    # ── Consolidação ──────────────────────────────────────
    report_lines.append("\n" + "=" * 70)
    report_lines.append("CONSOLIDAÇÃO — CAPÍTULOS COM MAIOR RISCO")
    report_lines.append("=" * 70)

    # Scoring: densidade baixa + trechos longos + definições sem atribuição
    risk_scores = {}
    for num in chapters:
        score = 0
        details = []

        # Densidade citacional
        d = density[num]['densidade']
        if d < 0.5:
            score += 3
            details.append(f"densidade muito baixa ({d:.2f})")
        elif d < 1.5:
            score += 1
            details.append(f"densidade baixa ({d:.2f})")

        # Trechos sem citação
        n_stretches = len(all_stretches.get(num, []))
        if n_stretches > 5:
            score += 3
            details.append(f"{n_stretches} trechos longos sem citação")
        elif n_stretches > 2:
            score += 2
            details.append(f"{n_stretches} trechos longos sem citação")
        elif n_stretches > 0:
            score += 1
            details.append(f"{n_stretches} trecho(s) longo(s) sem citação")

        # Definições sem atribuição
        n_defs = len(all_defs.get(num, []))
        if n_defs > 5:
            score += 2
            details.append(f"{n_defs} definições sem atribuição")
        elif n_defs > 0:
            score += 1
            details.append(f"{n_defs} definição(ões) sem atribuição")

        # Variação estilística
        if num in lex_stats and lex_stats[num]['ttr_std'] > 0.06:
            score += 1
            details.append(f"variação estilística alta (σ={lex_stats[num]['ttr_std']:.4f})")

        risk_scores[num] = {'score': score, 'details': details}

    # Ordenar por risco
    sorted_risk = sorted(risk_scores.items(), key=lambda x: x[1]['score'], reverse=True)

    for num, info in sorted_risk:
        if info['score'] == 0:
            continue

        if info['score'] >= 5:
            level = "🔴 ALTO"
        elif info['score'] >= 3:
            level = "🟡 MÉDIO"
        else:
            level = "🔵 BAIXO"

        report_lines.append(f"\n  Cap {num:>2} — Risco {level} (score {info['score']})")
        for d in info['details']:
            report_lines.append(f"    • {d}")

    # Capítulos sem risco
    clean_caps = [num for num, info in sorted_risk if info['score'] == 0]
    if clean_caps:
        report_lines.append(f"\n  Sem risco detectado: Caps {', '.join(str(c) for c in sorted(clean_caps))}")

    # ── Recomendações ─────────────────────────────────────
    report_lines.append("\n\n" + "=" * 70)
    report_lines.append("RECOMENDAÇÕES")
    report_lines.append("=" * 70)

    high_risk = [(n, i) for n, i in sorted_risk if i['score'] >= 5]
    med_risk = [(n, i) for n, i in sorted_risk if 3 <= i['score'] < 5]

    report_lines.append("\n  PRIORIDADE ALTA:")
    if high_risk:
        for num, info in high_risk:
            report_lines.append(f"  → Cap {num}: adicionar referências doutrinárias nos trechos identificados")
            report_lines.append(f"     Motivos: {'; '.join(info['details'])}")
    else:
        report_lines.append("  → Nenhum capítulo com risco alto detectado.")

    report_lines.append("\n  PRIORIDADE MÉDIA:")
    if med_risk:
        for num, info in med_risk:
            report_lines.append(f"  → Cap {num}: revisar cobertura citacional")
            report_lines.append(f"     Motivos: {'; '.join(info['details'])}")
    else:
        report_lines.append("  → Nenhum capítulo com risco médio detectado.")

    report_lines.append("\n  OBSERVAÇÃO GERAL:")
    report_lines.append("  Este livro foi gerado por pipeline de IA. O risco de 'plágio' no sentido")
    report_lines.append("  tradicional é baixo, mas há risco de reprodução involuntária de formulações")
    report_lines.append("  doutrinárias absorvidas durante o treinamento do modelo. As recomendações")
    report_lines.append("  acima focam em trechos que se beneficiariam de citação explícita a fontes")
    report_lines.append("  doutrinárias para reforçar a credibilidade acadêmica do texto.")

    # ── Salvar ────────────────────────────────────────────
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text('\n'.join(report_lines), encoding='utf-8')

    print(f"\n  Relatório salvo: {OUTPUT}")

    # Sumário final
    total_findings = total_stretches + total_defs + total_form
    n_high = len(high_risk)
    n_med = len(med_risk)

    print(f"\n{'=' * 70}")
    print(f"SUMÁRIO")
    print(f"{'=' * 70}")
    print(f"  Trechos longos sem citação: {total_stretches}")
    print(f"  Definições sem atribuição:  {total_defs}")
    print(f"  Frases formulaicas:         {total_form}")
    print(f"  Capítulos risco ALTO:       {n_high}")
    print(f"  Capítulos risco MÉDIO:      {n_med}")
    print(f"  Densidade citacional média: {avg_density:.2f}/1000 palavras")


if __name__ == "__main__":
    main()
