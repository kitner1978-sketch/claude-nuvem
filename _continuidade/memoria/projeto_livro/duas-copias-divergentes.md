---
name: duas-copias-divergentes
description: O Projeto Livro tem TRÊS cópias em discos diferentes; a mais recente em Markdown é a do 2tb (20/07/2026) e há um DOCX revisado de 18/09/2026 fora de qualquer repositório
metadata: 
  node_type: memory
  type: project
  originSessionId: ae3de0e0-4c37-4476-94b7-0b2c8cf90231
  modified: 2026-09-21T22:17:16.735Z
---

Verificado em 2026-09-21. Antes de editar qualquer capítulo, confirmar em qual cópia se está.

| Cópia | Git | Estado |
|---|---|---|
| `/Volumes/2tb/Projeto Livro` | `master`, 26 commits, último `0cb45ea` de 2026-07-20 (+ alterações **não commitadas** de 2026-09-21) | **Fonte Markdown mais recente.** Continuação direta do seagate (contém `4c9fb53`) + 10 commits: conformidade com a editora **Thoth** (sentence-case, ABNT 2023), Apresentação e Sobre os Autores embutidos, corte normativo harmonizado para junho/2026, revisão semântica de 19/07, referências consolidadas. ~391 mil palavras. Tem `carta_editora_thoth.docx` e `Proposta_Divisao_Editorial` |
| `/Volumes/seagate/Projeto Livro` | `master`, 16 commits, último `4c9fb53` de 2026-06-10 | Retrato de 10/06 da mesma linhagem. **Defasado em 10 commits.** |
| `/Volumes/Macintosh NVMe/Projeto Livro` | `main`, 13 commits, histórico **sem relação** | Retrato de 10/05 (17 caps) + frente de Instagram (`marketing/`, `gerar_cards.py`, `gerar_reel.py`, `HANDOFF_SESSAO.md`) |

**Versão mais recente do texto, fora do git:** `~/Downloads/livro_completo - 18 de set 26.docx` — editado direto no Word por **Ingrid Moura** (revisora; revisão 43, ~395 mil palavras, 1.373 pp.), **sem controle de alterações** e com **21 comentários** datados de 25/08 a 11/09/2026 (checagens jurídicas nos caps. 3, 4, 5, 8 etc.). As mudanças dela não estão em nenhum Markdown.

**Why:** numa mesma sessão concluí errado que o seagate era "a cópia boa" por ter comparado só com o NVMe. O `PROJETOS.md` aponta para o NVMe, que é a pior das três. O `pipeline_state.json` do 2tb também está defasado (ainda lista como pendentes Apresentação e corte normativo, já resolvidos nos commits de 19/07).

**How to apply:** trabalhar no 2tb. Para reconciliar o DOCX da Ingrid com o Markdown é preciso diff de texto (não há tracked changes). Só no NVMe: 6 fichas TNU (Temas 73, 174, 208, 213, 301, Reclamação 0000302-22) e `output/auditoria/auditoria_dirigida_20260727.md`. Os achados dessa auditoria no cap_18 foram tratados em 2026-09-21 (ver [[revisao-dirigida-set2026]]): o Tema 185/STJ fala em presunção *absoluta* e o Tema 122/TNU em *relativa* — o erro do livro era a seção 18.13, não as linhas com "absoluta". Ver [[ruido-crlf-git]] e [[escrita-anti-ia]].
