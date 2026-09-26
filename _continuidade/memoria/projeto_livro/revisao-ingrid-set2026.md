---
name: revisao-ingrid-set2026
description: "O que a revisora Ingrid Moura mudou entre o DOCX de 19/07 e o de 18/09/2026 — 390 edições pequenas, nenhuma reescrita de fundo; revela defeitos do gerador e do cap_10"
metadata: 
  node_type: memory
  type: project
  originSessionId: ae3de0e0-4c37-4476-94b7-0b2c8cf90231
  modified: 2026-09-21T22:21:31.590Z
---

Comparação feita em 2026-09-21 entre `livro_completo - 19 de jul 26.docx` (gerado pelo pipeline; idêntico no 2tb e na raiz do seagate) e `~/Downloads/livro_completo - 18 de set 26.docx` (editado no Word por Ingrid Moura, sem tracked changes, 21 comentários).

- 13.257 parágrafos idênticos; **390 edições**, saldo de −319 palavras. As ~9,7 mil palavras "a mais" são só o sumário, que em julho era o placeholder "Atualize o sumário para ver as entradas".
- 307 são pontuação/caixa/hífen; 68 trocam até 3 palavras; 14 mexem em trecho curto; 1 reescrita (remoção de nota editorial interna sobre a EC 136/2025 no cap. 1).
- ~280 são **"salário mínimo" → "salário-mínimo"** (com hífen). Decisão da revisora; a CF e a Lei 8.213 grafam sem hífen. Autor ainda não se pronunciou.
- Defeitos **de origem** que ela consertou à mão e que voltam se o DOCX for regerado do Markdown:
  1. **cap_10 sem acentuação** no fonte (`unica especie`, `configuracao`, `calculo`…) — ~29 linhas em `cap_10_rascunho.md`.
  2. **Listas numeradas saindo "1. 1. 1."** no DOCX (caps. 5, 14 e outros) — defeito do `md_to_docx.py`.
  3. **Restos de `strip_citations`**: ", e Castro e Lazzari (2025)," solto e verbos órfãos ("Observam que", "Registra que", "Destaca que") após a remoção do autor-sujeito. Ela corrigiu 6 de 14; **8 permanecem** no DOCX de setembro.
  4. "tema"/"lei" em minúscula por efeito do sentence-case da Thoth aplicado além dos títulos.
- Ainda no DOCX de setembro: 1 nota interna "(nota: verificar redação final no DOU)" sobre a EC 136/2025.

**How to apply:** corrigir 1–4 no Markdown/gerador (2tb) em vez de no Word, senão a próxima geração desfaz o trabalho dela. Ver [[duas-copias-divergentes]].
