"""
Validacao pos-renumeracao: verifica integridade dos capitulos renumerados.
"""
import re
import os
import json

BASE = r'D:\Projeto Livro'
RASCUNHOS = os.path.join(BASE, 'output', 'rascunhos')
CAPITULOS = os.path.join(BASE, 'output', 'capitulos')
STATE = os.path.join(BASE, 'state')

CAPS_ESPERADOS = {
    1: "Evolucao Historica",
    2: "Segurados e Dependentes",
    3: "Periodo de Carencia",
    6: "Aposentadoria por Incapacidade Permanente",
    7: "Auxilio por Incapacidade Temporaria",
    8: "Aposentadoria Especial",
    9: "Aposentadoria do Segurado Rural",
    18: "Beneficio de Prestacao Continuada",
    19: "Pensao por Morte",
    23: "Competencia e Procedimento no JEF",
}

erros = []
ok = []

print("=" * 60)
print("VALIDACAO POS-RENUMERACAO")
print("=" * 60)

# 1. Verificar existencia dos arquivos
print("\n--- 1. Existencia dos arquivos ---")
for cap_num in CAPS_ESPERADOS:
    rascunho = os.path.join(RASCUNHOS, f'cap_{cap_num:02d}_rascunho.md')
    # caps 1-3 may not have rascunho files (cap 1 doesn't)
    if cap_num >= 6:
        if os.path.exists(rascunho):
            ok.append(f"Rascunho cap_{cap_num:02d}: existe")
        else:
            erros.append(f"ERRO: Rascunho cap_{cap_num:02d} NAO encontrado")

    final = os.path.join(CAPITULOS, f'cap_{cap_num:02d}.md')
    if os.path.exists(final):
        ok.append(f"Final cap_{cap_num:02d}: existe")
    else:
        if cap_num >= 6:
            erros.append(f"ERRO: Final cap_{cap_num:02d} NAO encontrado")

# 2. Verificar que arquivos antigos NAO existem
print("\n--- 2. Arquivos antigos removidos ---")
for old_num in [4, 5, 10]:  # 6,7,8,9 could conflict with new numbers
    for pattern in [f'cap_{old_num:02d}_rascunho.md', f'cap_{old_num:02d}.md']:
        old_path = os.path.join(RASCUNHOS if 'rascunho' in pattern else CAPITULOS, pattern)
        if os.path.exists(old_path):
            erros.append(f"ERRO: Arquivo antigo ainda existe: {pattern}")
        else:
            ok.append(f"Antigo {pattern}: removido OK")

# 3. Verificar conteudo dos rascunhos
print("\n--- 3. Conteudo dos rascunhos ---")
for cap_num in [6, 7, 8, 9, 18, 19, 23]:
    path = os.path.join(RASCUNHOS, f'cap_{cap_num:02d}_rascunho.md')
    if not os.path.exists(path):
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAML capitulo
    yaml_match = re.search(r'^capitulo:\s*(\d+)', content, re.MULTILINE)
    if yaml_match:
        yaml_num = int(yaml_match.group(1))
        if yaml_num == cap_num:
            ok.append(f"Cap {cap_num:02d} YAML capitulo: {yaml_num} OK")
        else:
            erros.append(f"ERRO Cap {cap_num:02d} YAML capitulo: esperado {cap_num}, encontrado {yaml_num}")

    # Heading
    heading_match = re.search(rf'^## Capitulo {cap_num}\b|^## Cap.tulo {cap_num}\b', content, re.MULTILINE)
    if heading_match:
        ok.append(f"Cap {cap_num:02d} heading: ## Capitulo {cap_num} OK")
    else:
        erros.append(f"ERRO Cap {cap_num:02d} heading: ## Capitulo {cap_num} NAO encontrado")

    # Section headings
    sections = re.findall(r'^### (\d+)\.\d+', content, re.MULTILINE)
    wrong_sections = [s for s in sections if int(s) != cap_num]
    if wrong_sections:
        erros.append(f"ERRO Cap {cap_num:02d} secoes com numero errado: {set(wrong_sections)}")
    else:
        ok.append(f"Cap {cap_num:02d} secoes: {len(sections)} secoes, todas com prefixo {cap_num} OK")

    # Sub-sections
    subsections = re.findall(r'^#### (\d+)\.\d+', content, re.MULTILINE)
    wrong_sub = [s for s in subsections if int(s) != cap_num]
    if wrong_sub:
        erros.append(f"ERRO Cap {cap_num:02d} subsecoes com numero errado: {set(wrong_sub)}")
    elif subsections:
        ok.append(f"Cap {cap_num:02d} subsecoes: {len(subsections)}, todas com prefixo {cap_num} OK")

    # Tags
    tag_expected = f'cap_{cap_num:02d}'
    if tag_expected in content:
        ok.append(f"Cap {cap_num:02d} tag: {tag_expected} OK")

    # Check for OLD tags
    for old_num in [4, 5, 6, 7, 8, 9, 10]:
        old_tag = f'cap_{old_num:02d}'
        if old_tag in content and cap_num != old_num:
            # Only flag if old_tag appears in YAML tags area (not in text)
            yaml_end = content.find('---', 3)
            yaml_section = content[:yaml_end] if yaml_end > 0 else ''
            if old_tag in yaml_section:
                erros.append(f"ERRO Cap {cap_num:02d}: tag antiga {old_tag} encontrada no YAML")

# 4. Verificar glossario
print("\n--- 4. Glossario ---")
with open(os.path.join(STATE, 'glossario.json'), 'r', encoding='utf-8') as f:
    glossario = json.load(f)

for termo in glossario.get('termos', []):
    cap_orig = termo.get('capitulo_origem', '')
    # Check no old IDs remain
    for old_num in [4, 5, 10]:
        if cap_orig == f'cap_{old_num:02d}':
            erros.append(f"ERRO Glossario: termo '{termo['termo']}' ainda tem capitulo_origem={cap_orig}")

old_ids_in_processados = [c for c in glossario.get('capitulos_processados', [])
                          if c in ['cap_04', 'cap_05', 'cap_10']]
if old_ids_in_processados:
    erros.append(f"ERRO Glossario capitulos_processados: IDs antigos: {old_ids_in_processados}")
else:
    ok.append("Glossario capitulos_processados: sem IDs antigos OK")

# 5. Verificar pipeline_state
print("\n--- 5. Pipeline state ---")
with open(os.path.join(STATE, 'pipeline_state.json'), 'r', encoding='utf-8') as f:
    pipeline = json.load(f)

caps_pipeline = list(pipeline.get('capitulos', {}).keys())
for old_id in ['cap_04', 'cap_05', 'cap_10']:
    if old_id in caps_pipeline:
        erros.append(f"ERRO Pipeline: chave antiga {old_id} encontrada")

for new_id in ['cap_06', 'cap_07', 'cap_08', 'cap_09', 'cap_18', 'cap_19', 'cap_23']:
    if new_id in caps_pipeline:
        ok.append(f"Pipeline: {new_id} presente OK")
    else:
        erros.append(f"ERRO Pipeline: {new_id} NAO encontrado")

prox = pipeline.get('livro', {}).get('proximo_capitulo', '')
if prox == 'cap_04':
    ok.append(f"Pipeline proximo_capitulo: {prox} OK")
else:
    erros.append(f"ERRO Pipeline proximo_capitulo: esperado cap_04, encontrado {prox}")

# 6. Cross-references
print("\n--- 6. Cross-references ---")
for cap_num in [6, 7, 8, 9, 18, 19, 23]:
    path = os.path.join(RASCUNHOS, f'cap_{cap_num:02d}_rascunho.md')
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find cross-refs like "Capitulo X" where X is NOT this chapter
    refs = re.findall(r'Cap.tulo\s+(\d+)', content)
    for ref in refs:
        ref_num = int(ref)
        if ref_num == cap_num:
            continue  # self-reference is fine
        if ref_num in [1, 2, 3]:
            continue  # references to unchanging chapters are fine
        if ref_num in [4, 5, 10]:
            erros.append(f"ERRO Cap {cap_num:02d}: referencia cruzada para Capitulo {ref_num} (antigo, deveria estar renumerado)")

# REPORT
print("\n" + "=" * 60)
print(f"RESULTADO: {len(ok)} OK, {len(erros)} ERROS")
print("=" * 60)

if erros:
    print("\nERROS:")
    for e in erros:
        print(f"  {e}")
else:
    print("\nNENHUM ERRO ENCONTRADO!")

print(f"\nVerificacoes OK: {len(ok)}")
for o in ok[:10]:
    print(f"  {o}")
if len(ok) > 10:
    print(f"  ... e mais {len(ok) - 10}")
