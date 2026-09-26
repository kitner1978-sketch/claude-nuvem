---
name: gerador-docx-callouts
description: add_blockquote no md_to_docx renderiza callouts Obsidian e tabelas internas
metadata: 
  node_type: memory
  type: project
  originSessionId: eab83ea0-3316-4038-a699-dc338636e973
---

O gerador de DOCX (`aposentadoria_especial/scripts/md_to_docx.py`, função `add_blockquote`, usada também por `gerar_livro_pdf.py`) tinha um defeito: renderizava callouts `> [!tipo] Título` despejando o marcador `[!quote]/[!info]/[!tip]/[!warning]` como texto literal e as tabelas markdown internas como pipes crus (`| a | b |` / `|---|`). Isso afetava 168 callouts e ~28 tabelas internas na prova.

Corrigido em 2026-07-19: `add_blockquote` agora extrai o marcador `[!tipo]`, estiliza o título (negrito), e converte tabelas markdown internas em tabelas reais via `add_table_block`. Callouts só de prosa mantêm a caixa com borda dourada à esquerda; callouts com tabela viram legenda + tabela real. Ver [[escrita-anti-ia]].
