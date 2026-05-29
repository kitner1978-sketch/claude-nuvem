#!/usr/bin/env python3
"""
detectar_repeticoes.py — Detecção de repetições cross-chapter e intra-chapter

Fase 1: Identifica conceitos jurídicos explicados redundantemente em múltiplos
capítulos, gerando relatório com severidade e recomendação de ação.

Estratégia:
  1. Definir conceitos-chave com palavras-sinal
  2. Extrair parágrafos relevantes de cada capítulo
  3. Calcular similaridade TF-IDF entre parágrafos cross-chapter
  4. Gerar relatório rankeado por impacto
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ═══════════════════════════════════════════════════════
# CONCEITOS-CHAVE E CAPÍTULOS-SEDE
# ═══════════════════════════════════════════════════════

CONCEITOS = {
    'qualidade_segurado': {
        'nome': 'Qualidade de segurado / Período de graça',
        'sede': 3,
        'termos': [
            r'qualidade de segurado',
            r'período de graça',
            r'art\.\s*15.*Lei\s*8\.213',
            r'manutenção da qualidade',
            r'perda da qualidade',
        ],
    },
    'carencia': {
        'nome': 'Carência',
        'sede': 3,
        'termos': [
            r'carência',
            r'art\.\s*2[4-7].*Lei\s*8\.213',
            r'art\.\s*142.*Lei\s*8\.213',
            r'180 contribuições',
            r'dispensa de carência',
        ],
    },
    'dependentes': {
        'nome': 'Dependentes (art. 16)',
        'sede': 2,
        'termos': [
            r'art\.\s*16.*Lei\s*8\.213',
            r'classes? de dependentes',
            r'dependência econômica',
            r'presunção de dependência',
            r'dependentes?\s+de\s+(?:primeira|segunda|terceira)\s+classe',
        ],
    },
    'categorias_segurados': {
        'nome': 'Categorias de segurados',
        'sede': 2,
        'termos': [
            r'segurado(?:s)?\s+obrigatório',
            r'contribuinte individual',
            r'segurado especial',
            r'segurado facultativo',
            r'art\.\s*1[1-4].*Lei\s*8\.213',
            r'empregado(?:\s+doméstico)?.*trabalhador avulso',
        ],
    },
    'regras_transicao': {
        'nome': 'Regras de transição EC 103',
        'sede': 11,
        'termos': [
            r'regra(?:s)? de transição',
            r'art\.\s*1[5-8].*EC\s*103',
            r'art\.\s*20.*EC\s*103',
            r'pedágio\s+(?:de\s+)?(?:50|100)\s*%',
            r'pontos?\s+(?:progressiv|mínimo)',
        ],
    },
    'calculo_sb_rmi': {
        'nome': 'Cálculo do salário de benefício / RMI',
        'sede': 16,
        'termos': [
            r'salário de benefício',
            r'renda mensal inicial',
            r'(?:RMI|PBC)',
            r'80\s*%\s*maiores',
            r'art\.\s*29.*Lei\s*8\.213',
            r'60\s*%\s*\+\s*2\s*%',
            r'art\.\s*26.*EC\s*103',
        ],
    },
    'fator_previdenciario': {
        'nome': 'Fator previdenciário',
        'sede': 16,
        'termos': [
            r'fator previdenciário',
            r'Lei\s*9\.876',
            r'(?:Tc|Es|Id).*fórmula',
            r'85/95',
        ],
    },
    'reafirmacao_der': {
        'nome': 'Reafirmação da DER (Tema 995/STJ)',
        'sede': 10,
        'termos': [
            r'reafirmação da DER',
            r'Tema\s*995',
            r'implementação posterior',
        ],
    },
    'decadencia_prescricao': {
        'nome': 'Decadência e prescrição',
        'sede': 21,
        'termos': [
            r'decadência\s+(?:decenal|do\s+direito|art\.\s*103)',
            r'prescrição\s+quinquenal',
            r'art\.\s*103.*Lei\s*8\.213',
            r'trato sucessivo',
            r'Súmula\s*85.*STJ',
        ],
    },
    'acumulacao': {
        'nome': 'Acumulação de benefícios',
        'sede': 20,
        'termos': [
            r'acumulação de benefícios',
            r'art\.\s*124.*Lei\s*8\.213',
            r'art\.\s*24.*EC\s*103',
            r'escalonamento.*100.*80.*60',
            r'vedação.*cumulação',
        ],
    },
    'biopsicossocial': {
        'nome': 'Modelo biopsicossocial',
        'sede': 6,
        'termos': [
            r'biopsicossocial',
            r'IF-Br[Aa]?',
            r'CIF',
            r'funcionalidade.*incapacidade',
        ],
    },
    'cnis_prova': {
        'nome': 'CNIS como prova',
        'sede': 5,
        'termos': [
            r'CNIS',
            r'art\.\s*29-?A',
            r'Cadastro Nacional de Informações Sociais',
            r'retificação.*CNIS',
        ],
    },
    'ec103_geral': {
        'nome': 'EC 103/2019 (explicação geral da Reforma)',
        'sede': 1,
        'termos': [
            r'EC\s*103/2019.*(?:redesenhou|reformou|alterou profundamente|promoveu)',
            r'Reforma da Previdência.*2019',
            r'13\s*(?:de\s*)?novembro\s*(?:de\s*)?2019',
        ],
    },
    'uniao_estavel': {
        'nome': 'União estável (prova para previdenciário)',
        'sede': 19,
        'termos': [
            r'união estável',
            r'companheiro.*companheira',
            r'entidade familiar',
            r'início de prova material.*(?:união|convivência)',
        ],
    },
    'tutela_urgencia': {
        'nome': 'Tutela de urgência / antecipação',
        'sede': 23,
        'termos': [
            r'tutela\s+(?:de\s+)?urgência',
            r'antecipação\s+(?:de\s+)?tutela',
            r'tutela\s+provisória',
            r'implantação\s+(?:imediata|do\s+benefício)',
        ],
    },
    'direito_adquirido': {
        'nome': 'Direito adquirido previdenciário',
        'sede': 11,
        'termos': [
            r'direito adquirido',
            r'art\.\s*3º.*EC\s*103',
            r'tempus regit actum',
        ],
    },
}


def load_chapters(rascunhos_dir):
    """Carrega todos os capítulos, retornando dict {cap_id: texto}."""
    chapters = {}
    for cap_id in range(1, 24):
        path = rascunhos_dir / f"cap_{cap_id:02d}_rascunho.md"
        if path.exists():
            chapters[cap_id] = path.read_text(encoding='utf-8')
    return chapters


def extract_paragraphs(text):
    """Divide texto em parágrafos substanciais (>50 palavras), excluindo YAML, headings e boxes."""
    # Remover YAML frontmatter
    text = re.sub(r'^---.*?---', '', text, count=1, flags=re.DOTALL)

    paragraphs = []
    current = []

    for line in text.split('\n'):
        stripped = line.strip()

        # Ignorar headings, box delimiters, tabelas
        if (stripped.startswith('#') or stripped.startswith(':::') or
            stripped.startswith('|') or stripped.startswith('---') or
            stripped.startswith('**Quadro') or stripped.startswith('**Tabela')):
            if current:
                para = ' '.join(current).strip()
                if len(para.split()) >= 50:
                    paragraphs.append(para)
                current = []
            continue

        if stripped == '':
            if current:
                para = ' '.join(current).strip()
                if len(para.split()) >= 50:
                    paragraphs.append(para)
                current = []
        else:
            current.append(stripped)

    if current:
        para = ' '.join(current).strip()
        if len(para.split()) >= 50:
            paragraphs.append(para)

    return paragraphs


def find_concept_paragraphs(paragraphs, concept_terms):
    """Encontra parágrafos que mencionam um conceito (via seus termos-sinal)."""
    matches = []
    for i, para in enumerate(paragraphs):
        score = 0
        for term in concept_terms:
            if re.search(term, para, re.IGNORECASE):
                score += 1
        if score >= 1:  # Pelo menos 1 termo presente
            matches.append((i, para, score))
    return matches


def get_section_for_paragraph(text, paragraph_text):
    """Encontra a seção (heading) onde um parágrafo está localizado."""
    # Encontrar posição do parágrafo
    # Usar primeiras 100 chars como busca
    search_key = paragraph_text[:120].replace('(', r'\(').replace(')', r'\)')
    try:
        pos = re.search(re.escape(paragraph_text[:100]), text)
    except:
        pos = None

    if not pos:
        return "Seção não identificada"

    # Procurar heading anterior
    before_text = text[:pos.start()]
    headings = re.findall(r'^(#{2,4}\s+.+)$', before_text, re.MULTILINE)
    if headings:
        return headings[-1].strip().lstrip('#').strip()
    return "Início do capítulo"


def compute_similarity_matrix(paragraphs_list):
    """Calcula matriz de similaridade TF-IDF entre parágrafos."""
    if len(paragraphs_list) < 2:
        return np.array([])

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        stop_words=None,  # Português - não há stop words built-in
        min_df=1,
        max_df=0.95,
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(paragraphs_list)
        sim_matrix = cosine_similarity(tfidf_matrix)
        return sim_matrix
    except:
        return np.array([])


def analyze_cross_chapter(chapters, concept_key, concept_info):
    """Analisa repetições cross-chapter para um conceito específico."""
    sede = concept_info['sede']
    termos = concept_info['termos']

    # Coletar parágrafos relevantes de cada capítulo
    cap_paragraphs = {}  # cap_id -> [(idx, text, score)]
    for cap_id, text in chapters.items():
        paras = extract_paragraphs(text)
        matches = find_concept_paragraphs(paras, termos)
        if matches:
            cap_paragraphs[cap_id] = [(text_p, score, get_section_for_paragraph(text, text_p)) for _, text_p, score in matches]

    if len(cap_paragraphs) < 2:
        return None  # Conceito só aparece em 1 capítulo

    # Flatten para TF-IDF
    all_paras = []
    para_metadata = []  # (cap_id, section, score, original_text)
    for cap_id, matches in cap_paragraphs.items():
        for text_p, score, section in matches:
            all_paras.append(text_p)
            para_metadata.append((cap_id, section, score, text_p))

    # Calcular similaridade
    sim_matrix = compute_similarity_matrix(all_paras)
    if sim_matrix.size == 0:
        return None

    # Encontrar pares cross-chapter com alta similaridade
    findings = []
    n = len(all_paras)
    for i in range(n):
        for j in range(i + 1, n):
            cap_i = para_metadata[i][0]
            cap_j = para_metadata[j][0]
            if cap_i == cap_j:
                continue  # Pular intra-chapter (será fase 2)

            sim = sim_matrix[i][j]
            if sim >= 0.25:  # Threshold de similaridade
                findings.append({
                    'similarity': sim,
                    'cap_a': cap_i,
                    'section_a': para_metadata[i][1],
                    'text_a': para_metadata[i][3][:300],
                    'cap_b': cap_j,
                    'section_b': para_metadata[j][1],
                    'text_b': para_metadata[j][3][:300],
                    'sede': sede,
                })

    findings.sort(key=lambda x: x['similarity'], reverse=True)
    return findings[:20]  # Top 20 por conceito


def classify_severity(sim, cap_a, cap_b, sede):
    """Classifica severidade da repetição."""
    if sim >= 0.60:
        return 'CRITICO'    # Parágrafos quase idênticos
    elif sim >= 0.45:
        return 'RELEVANTE'  # Sobreposição significativa
    else:
        return 'SUGESTAO'   # Sobreposição parcial


def recommend_action(sim, cap_a, cap_b, sede):
    """Recomenda ação para a repetição."""
    # Se um dos capítulos é a sede, manter lá e reduzir no outro
    if cap_a == sede:
        target = cap_b
        source = cap_a
    elif cap_b == sede:
        target = cap_a
        source = cap_b
    else:
        # Nenhum é sede — reduzir no que tem menos relevância para o tema
        target = max(cap_a, cap_b)
        source = min(cap_a, cap_b)

    if sim >= 0.55:
        return f"ELIMINAR no Cap {target}: substituir por remissão ao Cap {source}"
    elif sim >= 0.40:
        return f"CONDENSAR no Cap {target}: reduzir a 1-2 frases + remissão ao Cap {source}"
    else:
        return f"AVALIAR: possível condensação no Cap {target} com remissão ao Cap {source}"


def count_concept_mentions(chapters, concept_info):
    """Conta quantos capítulos mencionam um conceito e quantas vezes."""
    termos = concept_info['termos']
    mentions = {}
    for cap_id, text in chapters.items():
        count = 0
        for term in termos:
            count += len(re.findall(term, text, re.IGNORECASE))
        if count > 0:
            mentions[cap_id] = count
    return mentions


def analyze_intra_chapter(chapters):
    """Detecta repetições dentro do mesmo capítulo (Fase 2 básica)."""
    findings = []

    for cap_id, text in chapters.items():
        paras = extract_paragraphs(text)
        if len(paras) < 3:
            continue

        sim_matrix = compute_similarity_matrix(paras)
        if sim_matrix.size == 0:
            continue

        n = len(paras)
        for i in range(n):
            for j in range(i + 2, n):  # Skip adjacent paragraphs
                sim = sim_matrix[i][j]
                if sim >= 0.45:
                    section_i = get_section_for_paragraph(text, paras[i])
                    section_j = get_section_for_paragraph(text, paras[j])
                    if section_i != section_j:  # Só se em seções diferentes
                        findings.append({
                            'cap': cap_id,
                            'similarity': sim,
                            'section_a': section_i,
                            'text_a': paras[i][:250],
                            'section_b': section_j,
                            'text_b': paras[j][:250],
                        })

    findings.sort(key=lambda x: x['similarity'], reverse=True)
    return findings[:50]  # Top 50


def main():
    project_dir = Path(__file__).parent.parent
    rascunhos_dir = project_dir / "output" / "rascunhos"
    output_dir = project_dir / "output"

    print("=" * 70)
    print("DETECÇÃO DE REPETIÇÕES — FASE 1 (Cross-Chapter) + FASE 2 (Intra)")
    print("=" * 70)

    # Carregar capítulos
    print("\nCarregando 23 capítulos...")
    chapters = load_chapters(rascunhos_dir)
    print(f"  {len(chapters)} capítulos carregados")
    total_words = sum(len(t.split()) for t in chapters.values())
    print(f"  {total_words:,} palavras totais")

    # ═══════════════════════════════════════════════════════
    # PARTE 1: Mapa de distribuição de conceitos
    # ═══════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("MAPA DE DISTRIBUIÇÃO DE CONCEITOS")
    print("=" * 70)

    concept_distribution = {}
    for key, info in CONCEITOS.items():
        mentions = count_concept_mentions(chapters, info)
        concept_distribution[key] = mentions
        n_caps = len(mentions)
        total_mentions = sum(mentions.values())
        sede = info['sede']
        other_caps = [c for c in mentions if c != sede]
        print(f"\n  {info['nome']} (sede: Cap {sede})")
        print(f"    Presente em {n_caps} capítulos, {total_mentions} menções totais")
        if other_caps:
            details = [f"Cap {c}({mentions[c]})" for c in sorted(other_caps)]
            print(f"    Fora da sede: {', '.join(details)}")

    # ═══════════════════════════════════════════════════════
    # PARTE 2: Análise cross-chapter por conceito
    # ═══════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("ANÁLISE CROSS-CHAPTER DE SIMILARIDADE")
    print("=" * 70)

    all_findings = []

    for key, info in CONCEITOS.items():
        print(f"\n  Analisando: {info['nome']}...", end=" ", flush=True)
        findings = analyze_cross_chapter(chapters, key, info)
        if findings:
            # Filtrar só os mais relevantes
            critical = [f for f in findings if f['similarity'] >= 0.45]
            relevant = [f for f in findings if 0.35 <= f['similarity'] < 0.45]
            suggestions = [f for f in findings if 0.25 <= f['similarity'] < 0.35]
            print(f"{len(critical)} críticos, {len(relevant)} relevantes, {len(suggestions)} sugestões")

            for f in findings:
                f['conceito'] = info['nome']
                f['conceito_key'] = key
            all_findings.extend(findings)
        else:
            print("OK (sem repetições significativas)")

    # ═══════════════════════════════════════════════════════
    # PARTE 3: Análise intra-chapter
    # ═══════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("ANÁLISE INTRA-CHAPTER DE SIMILARIDADE")
    print("=" * 70)

    print("\n  Analisando repetições dentro de cada capítulo...")
    intra_findings = analyze_intra_chapter(chapters)
    print(f"  {len(intra_findings)} repetições intra-chapter detectadas")

    # ═══════════════════════════════════════════════════════
    # GERAR RELATÓRIO
    # ═══════════════════════════════════════════════════════

    all_findings.sort(key=lambda x: x['similarity'], reverse=True)

    lines = []
    lines.append("RELATÓRIO DE REPETIÇÕES — FASE 1 + FASE 2")
    lines.append("=" * 70)
    lines.append(f"Data: 2026-05-15")
    lines.append(f"Capítulos analisados: {len(chapters)}")
    lines.append(f"Palavras totais: {total_words:,}")
    lines.append(f"Conceitos verificados: {len(CONCEITOS)}")
    lines.append("")

    # Sumário
    lines.append("SUMÁRIO EXECUTIVO")
    lines.append("-" * 50)
    criticos = [f for f in all_findings if f['similarity'] >= 0.45]
    relevantes = [f for f in all_findings if 0.35 <= f['similarity'] < 0.45]
    sugestoes = [f for f in all_findings if 0.25 <= f['similarity'] < 0.35]
    lines.append(f"  Repetições CRÍTICAS (sim >= 0.45): {len(criticos)}")
    lines.append(f"  Repetições RELEVANTES (0.35-0.45): {len(relevantes)}")
    lines.append(f"  Sugestões (0.25-0.35): {len(sugestoes)}")
    lines.append(f"  Repetições intra-chapter: {len(intra_findings)}")
    lines.append("")

    # Detalhamento cross-chapter
    lines.append("=" * 70)
    lines.append("DETALHAMENTO — REPETIÇÕES CROSS-CHAPTER")
    lines.append("=" * 70)

    # Agrupar por conceito
    by_concept = defaultdict(list)
    for f in all_findings:
        by_concept[f['conceito_key']].append(f)

    for key, concept_findings in sorted(by_concept.items(), key=lambda x: max(f['similarity'] for f in x[1]), reverse=True):
        info = CONCEITOS[key]
        lines.append(f"\n{'─' * 60}")
        lines.append(f"CONCEITO: {info['nome']}")
        lines.append(f"Capítulo-sede: {info['sede']}")
        lines.append(f"Pares com sobreposição: {len(concept_findings)}")
        lines.append("")

        for i, f in enumerate(concept_findings[:10], 1):
            sev = classify_severity(f['similarity'], f['cap_a'], f['cap_b'], f['sede'])
            action = recommend_action(f['similarity'], f['cap_a'], f['cap_b'], f['sede'])

            icon = {'CRITICO': '[!!!]', 'RELEVANTE': '[!!]', 'SUGESTAO': '[!]'}[sev]
            lines.append(f"  {icon} #{i} — Similaridade: {f['similarity']:.1%}")
            lines.append(f"    Cap {f['cap_a']}, {f['section_a'][:60]}")
            lines.append(f"    vs")
            lines.append(f"    Cap {f['cap_b']}, {f['section_b'][:60]}")
            lines.append(f"    Ação: {action}")
            lines.append(f"    Trecho A: \"{f['text_a'][:150]}...\"")
            lines.append(f"    Trecho B: \"{f['text_b'][:150]}...\"")
            lines.append("")

    # Detalhamento intra-chapter
    lines.append("\n" + "=" * 70)
    lines.append("DETALHAMENTO — REPETIÇÕES INTRA-CHAPTER")
    lines.append("=" * 70)

    by_cap = defaultdict(list)
    for f in intra_findings:
        by_cap[f['cap']].append(f)

    for cap_id in sorted(by_cap.keys()):
        cap_findings = by_cap[cap_id]
        lines.append(f"\n  Cap {cap_id} — {len(cap_findings)} repetições internas")
        for i, f in enumerate(cap_findings[:5], 1):
            lines.append(f"    [{f['similarity']:.1%}] {f['section_a'][:40]} ↔ {f['section_b'][:40]}")
            lines.append(f"      A: \"{f['text_a'][:120]}...\"")
            lines.append(f"      B: \"{f['text_b'][:120]}...\"")

    # Matriz capítulo × conceito
    lines.append("\n" + "=" * 70)
    lines.append("MATRIZ DE DISTRIBUIÇÃO: CAPÍTULO × CONCEITO")
    lines.append("=" * 70)
    lines.append("")

    # Header
    short_names = {
        'qualidade_segurado': 'QualSeg',
        'carencia': 'Carênc',
        'dependentes': 'Depend',
        'categorias_segurados': 'CategSeg',
        'regras_transicao': 'RTransição',
        'calculo_sb_rmi': 'Cálc/RMI',
        'fator_previdenciario': 'FatPrev',
        'reafirmacao_der': 'ReafDER',
        'decadencia_prescricao': 'DecPresc',
        'acumulacao': 'Acumul',
        'biopsicossocial': 'BioPsic',
        'cnis_prova': 'CNIS',
        'ec103_geral': 'EC103',
        'uniao_estavel': 'UniãoEst',
        'tutela_urgencia': 'TutelaUrg',
        'direito_adquirido': 'DirAdq',
    }

    header = f"  {'Cap':>4}"
    for key in CONCEITOS:
        header += f"  {short_names.get(key, key[:8]):>10}"
    lines.append(header)
    lines.append("  " + "-" * (4 + 12 * len(CONCEITOS)))

    for cap_id in range(1, 24):
        row = f"  {cap_id:>4}"
        for key in CONCEITOS:
            mentions = concept_distribution.get(key, {})
            count = mentions.get(cap_id, 0)
            sede = CONCEITOS[key]['sede']
            if cap_id == sede:
                cell = f"[{count}]" if count else "[-]"
            else:
                cell = str(count) if count else "."
            row += f"  {cell:>10}"
        lines.append(row)

    lines.append("")
    lines.append("  Legenda: [N] = capítulo-sede, N = menções, . = ausente")

    # Recomendações consolidadas
    lines.append("\n" + "=" * 70)
    lines.append("RECOMENDAÇÕES CONSOLIDADAS — AÇÕES PRIORITÁRIAS")
    lines.append("=" * 70)

    # Coletar recomendações únicas para os casos críticos
    actions_by_cap = defaultdict(list)
    for f in criticos:
        sev = classify_severity(f['similarity'], f['cap_a'], f['cap_b'], f['sede'])
        action = recommend_action(f['similarity'], f['cap_a'], f['cap_b'], f['sede'])
        # Identificar o capítulo-alvo (onde reduzir)
        if f['cap_a'] == f['sede']:
            target = f['cap_b']
        elif f['cap_b'] == f['sede']:
            target = f['cap_a']
        else:
            target = max(f['cap_a'], f['cap_b'])
        actions_by_cap[target].append({
            'conceito': f['conceito'],
            'similarity': f['similarity'],
            'action': action,
            'section': f['section_a'] if target == f['cap_a'] else f['section_b'],
        })

    for cap_id in sorted(actions_by_cap.keys()):
        actions = actions_by_cap[cap_id]
        lines.append(f"\n  Cap {cap_id}:")
        seen = set()
        for a in sorted(actions, key=lambda x: x['similarity'], reverse=True):
            key = (a['conceito'], a['action'])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"    [{a['similarity']:.0%}] {a['conceito']}: {a['action']}")

    report_text = '\n'.join(lines)

    # Salvar relatório
    report_path = output_dir / "relatorio_repeticoes.txt"
    report_path.write_text(report_text, encoding='utf-8')
    print(f"\n  Relatório salvo: {report_path}")

    # Imprimir sumário no terminal
    print("\n" + "=" * 70)
    print("SUMÁRIO")
    print("=" * 70)
    print(f"  CRÍTICAS: {len(criticos)}")
    print(f"  RELEVANTES: {len(relevantes)}")
    print(f"  SUGESTÕES: {len(sugestoes)}")
    print(f"  INTRA-CHAPTER: {len(intra_findings)}")
    print(f"\n  Relatório completo: {report_path}")

    return all_findings, intra_findings


if __name__ == '__main__':
    main()
