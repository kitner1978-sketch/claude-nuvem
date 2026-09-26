---
name: ruido-crlf-git
description: "No seagate, git status mostra ~51 arquivos \"modificados\" que são só fim de linha CRLF; conferir com --ignore-cr-at-eol antes de concluir que há trabalho não commitado"
metadata: 
  node_type: memory
  type: project
  originSessionId: ae3de0e0-4c37-4476-94b7-0b2c8cf90231
  modified: 2026-09-21T22:14:26.549Z
---

Na cópia do seagate (projeto nascido no Windows, `D:\Projeto Livro`; disco exFAT), `git status` lista ~51 arquivos `M` (rascunhos, `state/*.json`, relatórios). Em 2026-09-21 o diff tinha inserções = deleções (28.154/28.154) e ficava **vazio** com `git diff --ignore-cr-at-eol`. `core.autocrlf` não está configurado.

**Why:** parece haver meses de trabalho não commitado, mas não há. O conteúdo real fora do git eram só 6 itens não rastreados (PDFs datados, `output/observacoes_09jun/`, `observacoes_coautor_09jun.md`, `sobreposicao_cap22_cap23.md`).

**How to apply:** nunca fazer `git add -A`/commit desses arquivos sem checar — viraria um commit de 28 mil linhas de ruído. Para ver mudança real: `git diff --ignore-cr-at-eol --stat`. Normalizar (`.gitattributes` com `* text=auto` + renormalize) é decisão do autor. Ver [[duas-copias-divergentes]].
