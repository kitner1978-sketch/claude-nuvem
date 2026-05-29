"""
Script de Renumeração de Capítulos
===================================
Renumera os capítulos 4-10 conforme o mapa definido.
Atualiza: arquivos, conteúdo, YAML, seções, glossário, pipeline_state.

MAPA:
  4 → 6   (Apo. Incapacidade Permanente)
  5 → 7   (Aux. Incapacidade Temporária)
  6 → 8   (Aposentadoria Especial)
  7 → 9   (Aposentadoria Rural)
  8 → 18  (BPC/LOAS)
  9 → 19  (Pensão por Morte)
  10 → 23 (Competência e Procedimento no JEF)
"""

import os
import re
import json
import shutil
from datetime import datetime

BASE = r'D:\Projeto Livro'
RASCUNHOS = os.path.join(BASE, 'output', 'rascunhos')
CAPITULOS = os.path.join(BASE, 'output', 'capitulos')
DOCX_DIR = os.path.join(BASE, 'output', 'docx')
STATE_DIR = os.path.join(BASE, 'state')
BACKUP_DIR = os.path.join(BASE, 'backup_renumeracao')

MAPA = {4: 6, 5: 7, 6: 8, 7: 9, 8: 18, 9: 19, 10: 23}

# Títulos dos capítulos (para normalizar o heading ##)
TITULOS = {
    4: "Aposentadoria por Incapacidade Permanente",
    5: "Auxílio por Incapacidade Temporária",
    6: "Aposentadoria Especial",
    7: "Aposentadoria do Segurado Rural",
    8: "Benefício de Prestação Continuada (LOAS/BPC)",
    9: "Pensão por Morte",
    10: "Competência e Procedimento no JEF",
}

log_entries = []

def log(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))
    log_entries.append(msg)


def transform_content(content, old_num, new_num):
    """Transforma o conteúdo do capítulo: YAML, headings, seções, referências."""
    changes = []

    # 1. YAML frontmatter: capitulo: X
    new_content, n = re.subn(
        r'^(capitulo:\s*)\d+',
        rf'\g<1>{new_num}',
        content, flags=re.MULTILINE
    )
    if n > 0:
        changes.append(f"YAML capitulo: {old_num} → {new_num}")
    content = new_content

    # 2. YAML tags: cap_XX
    old_tag = f'cap_{old_num:02d}'
    new_tag = f'cap_{new_num:02d}'
    if old_tag in content:
        content = content.replace(old_tag, new_tag)
        changes.append(f"Tag: {old_tag} → {new_tag}")

    # 3. Heading: ## Capítulo X — Título
    new_content, n = re.subn(
        rf'^## Capítulo\s+{old_num}\s*[—–\-]\s*',
        f'## Capítulo {new_num} — ',
        content, flags=re.MULTILINE
    )
    if n > 0:
        changes.append(f"Heading: ## Capítulo {old_num} → {new_num}")
    content = new_content

    # 4. Heading SEM prefixo "Capítulo" (caso do cap 4)
    titulo = TITULOS.get(old_num, '')
    if titulo and old_num == 4:
        pattern = rf'^## {re.escape(titulo)}\s*$'
        replacement = f'## Capítulo {new_num} — {titulo}'
        new_content, n = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        if n > 0:
            changes.append(f"Heading normalizado: ## {titulo} → ## Capítulo {new_num} — {titulo}")
        content = new_content

    # 5. Seções ### X.Y
    new_content, n = re.subn(
        rf'^(###\s+){old_num}\.(\d+)',
        rf'\g<1>{new_num}.\2',
        content, flags=re.MULTILINE
    )
    if n > 0:
        changes.append(f"Seções ###: {n} ocorrências ({old_num}.Y → {new_num}.Y)")
    content = new_content

    # 6. Subseções #### X.Y.Z
    new_content, n = re.subn(
        rf'^(####\s+){old_num}\.(\d+)',
        rf'\g<1>{new_num}.\2',
        content, flags=re.MULTILINE
    )
    if n > 0:
        changes.append(f"Subseções ####: {n} ocorrências ({old_num}.Y.Z → {new_num}.Y.Z)")
    content = new_content

    # 7. Referências textuais: "seção X.Y" / "Seção X.Y"
    new_content, n = re.subn(
        rf'(seção\s+){old_num}\.(\d+)',
        rf'\g<1>{new_num}.\2',
        content, flags=re.IGNORECASE
    )
    if n > 0:
        changes.append(f"Ref. seção: {n} ocorrências (seção {old_num}.Y → seção {new_num}.Y)")
    content = new_content

    # 8. YAML parte: atualizar para nova organização
    parte_map = {
        4: "II — Benefícios por Incapacidade",
        5: "II — Benefícios por Incapacidade",
        6: "III — Aposentadorias Programadas",
        7: "III — Aposentadorias Programadas",
        8: "IV — Pensões, Auxílios e Benefício Assistencial",
        9: "IV — Pensões, Auxílios e Benefício Assistencial",
        10: "VI — Processo Previdenciário nos JEFs",
    }
    new_parte = parte_map.get(old_num)
    if new_parte:
        new_content, n = re.subn(
            r'^(parte:\s*")[^"]*(")',
            rf'\g<1>{new_parte}\2',
            content, flags=re.MULTILINE
        )
        if n > 0:
            changes.append(f"YAML parte: → {new_parte}")
        content = new_content

    return content, changes


def backup_files():
    """Cria backup completo antes da renumeração."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{BACKUP_DIR}_{timestamp}"
    os.makedirs(backup_path, exist_ok=True)

    dirs_to_backup = [
        ('rascunhos', RASCUNHOS),
        ('capitulos', CAPITULOS),
        ('docx', DOCX_DIR),
        ('state', STATE_DIR),
    ]

    for name, src_dir in dirs_to_backup:
        dst = os.path.join(backup_path, name)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst)
            log(f"  Backup: {src_dir} → {dst}")

    return backup_path


def main():
    log("=" * 70)
    log("RENUMERAÇÃO DE CAPÍTULOS")
    log("=" * 70)
    log(f"Mapa: {MAPA}")
    log("")

    # ===== BACKUP =====
    log("--- FASE 0: Backup ---")
    backup_path = backup_files()
    log(f"  Backup salvo em: {backup_path}")
    log("")

    # ===== FASE 1: Ler todos os arquivos =====
    log("--- FASE 1: Leitura de arquivos ---")
    files_data = {}  # key: (old_num, suffix, directory) → value: (old_path, content_or_None)

    file_patterns = {
        RASCUNHOS: ['_rascunho.md', '_rascunho.formatado.md', '_rascunho.formato_meta.json'],
        CAPITULOS: ['.md'],
    }

    for directory, suffixes in file_patterns.items():
        for old_num in MAPA:
            for suffix in suffixes:
                if directory == CAPITULOS:
                    filename = f'cap_{old_num:02d}{suffix}'
                else:
                    filename = f'cap_{old_num:02d}{suffix}'
                path = os.path.join(directory, filename)
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    files_data[(old_num, suffix, directory)] = (path, content)
                    log(f"  Lido: {os.path.relpath(path, BASE)}")

    # DOCX (binário — rastrear para exclusão)
    for old_num in MAPA:
        docx_path = os.path.join(DOCX_DIR, f'cap_{old_num:02d}.docx')
        if os.path.exists(docx_path):
            files_data[(old_num, '.docx', DOCX_DIR)] = (docx_path, None)
            log(f"  Lido (binário): {os.path.relpath(docx_path, BASE)}")

    log(f"  Total: {len(files_data)} arquivos")
    log("")

    # ===== FASE 2: Excluir arquivos antigos =====
    log("--- FASE 2: Exclusão dos arquivos originais ---")
    for key, (old_path, _) in files_data.items():
        os.remove(old_path)
        log(f"  Excluído: {os.path.relpath(old_path, BASE)}")
    log("")

    # ===== FASE 3: Escrever arquivos renumerados =====
    log("--- FASE 3: Escrita dos arquivos renumerados ---")
    for (old_num, suffix, directory), (old_path, content) in files_data.items():
        new_num = MAPA[old_num]

        if content is None:  # DOCX — será regenerado depois
            log(f"  Pulado (DOCX, regenerar depois): cap_{old_num:02d}.docx")
            continue

        # Transformar conteúdo
        if suffix.endswith('.md'):
            content, changes = transform_content(content, old_num, new_num)
            for c in changes:
                log(f"    {c}")
        elif suffix.endswith('.json'):
            content = content.replace(f'"cap_{old_num:02d}"', f'"cap_{new_num:02d}"')
            content = content.replace(f'cap_{old_num:02d}', f'cap_{new_num:02d}')
            log(f"    JSON: cap_{old_num:02d} → cap_{new_num:02d}")

        # Novo caminho
        new_filename = f'cap_{new_num:02d}{suffix}'
        new_path = os.path.join(directory, new_filename)

        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"  Escrito: {os.path.relpath(new_path, BASE)}")

    log("")

    # ===== FASE 4: Atualizar glossario.json =====
    log("--- FASE 4: Atualizar glossario.json ---")
    glossario_path = os.path.join(STATE_DIR, 'glossario.json')
    with open(glossario_path, 'r', encoding='utf-8') as f:
        glossario = json.load(f)

    termos_atualizados = 0
    for termo in glossario.get('termos', []):
        cap_orig = termo.get('capitulo_origem', '')
        for old_num, new_num in MAPA.items():
            if cap_orig == f'cap_{old_num:02d}':
                termo['capitulo_origem'] = f'cap_{new_num:02d}'
                termos_atualizados += 1
                break

    # Atualizar capitulos_processados
    if 'capitulos_processados' in glossario:
        old_list = glossario['capitulos_processados']
        new_list = []
        for cap_id in old_list:
            matched = False
            for old_num, new_num in MAPA.items():
                if cap_id == f'cap_{old_num:02d}':
                    new_list.append(f'cap_{new_num:02d}')
                    matched = True
                    break
            if not matched:
                new_list.append(cap_id)
        glossario['capitulos_processados'] = sorted(new_list)
        log(f"  capitulos_processados: {old_list} → {glossario['capitulos_processados']}")

    with open(glossario_path, 'w', encoding='utf-8') as f:
        json.dump(glossario, f, ensure_ascii=False, indent=2)
    log(f"  {termos_atualizados} termos atualizados no glossário")
    log("")

    # ===== FASE 5: Atualizar pipeline_state.json =====
    log("--- FASE 5: Atualizar pipeline_state.json ---")
    pipeline_path = os.path.join(STATE_DIR, 'pipeline_state.json')
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        pipeline = json.load(f)

    if 'capitulos' in pipeline:
        new_capitulos = {}
        for cap_id, data in pipeline['capitulos'].items():
            matched = False
            for old_num, new_num in MAPA.items():
                if cap_id == f'cap_{old_num:02d}':
                    new_key = f'cap_{new_num:02d}'
                    new_capitulos[new_key] = data
                    log(f"  Pipeline: {cap_id} → {new_key} ({data.get('titulo', '?')})")
                    matched = True
                    break
            if not matched:
                new_capitulos[cap_id] = data

        pipeline['capitulos'] = dict(sorted(new_capitulos.items()))

    # Atualizar proximo_capitulo
    old_prox = pipeline.get('livro', {}).get('proximo_capitulo', '')
    pipeline['livro']['proximo_capitulo'] = 'cap_04'
    log(f"  proximo_capitulo: {old_prox} → cap_04")

    with open(pipeline_path, 'w', encoding='utf-8') as f:
        json.dump(pipeline, f, ensure_ascii=False, indent=2)
    log("")

    # ===== RESUMO =====
    log("=" * 70)
    log("RENUMERAÇÃO CONCLUÍDA")
    log("=" * 70)
    log("")
    log("Mapeamento executado:")
    for old_num, new_num in sorted(MAPA.items()):
        titulo = TITULOS.get(old_num, '?')
        log(f"  Cap {old_num:2d} → Cap {new_num:2d}  ({titulo})")
    log("")
    log(f"Backup em: {backup_path}")
    log("AÇÃO PENDENTE: Atualizar book_structure.yaml")
    log("AÇÃO PENDENTE: Regenerar DOCX (7 capítulos)")
    log("")

    # Salvar log
    log_path = os.path.join(BASE, 'scripts', 'renumeracao_log.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_entries))
    print(f"Log salvo em: {log_path}")


if __name__ == '__main__':
    main()
