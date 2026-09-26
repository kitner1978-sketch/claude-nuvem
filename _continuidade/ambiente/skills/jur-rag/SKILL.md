---
name: jur-rag
description: >
  Pesquisa jurídica via o servidor MCP jur-rag — DOIS corpora: (1) jurisprudência
  brasileira (TRF5, Turmas Recursais, STJ, STF, Pangea — 20,46M chunks/5,3M docs) e
  (2) informativos de jurisprudência do STF e STJ (78k trechos, edições completas).
  Use SEMPRE que a tarefa envolver achar acórdãos/sentenças/decisões, precedentes,
  teses, ementas, ler o INTEIRO TEOR de um julgado, OU consultar informativos do
  STF/STJ. Gatilhos: "jurisprudência", "acórdão", "sentença", "precedente", "tese",
  "informativo do STF/STJ", "informativo n.", "STJ/STF/TRF5", nº de processo CNJ,
  "o que decidiu o tribunal sobre...". Ferramentas: mcp__jur-rag__juris_rag_search,
  mcp__jur-rag__juris_rag_inteiro_teor, mcp__jur-rag__informativos_rag_search,
  mcp__jur-rag__informativos_rag_inteiro_teor.
---

# jur-rag — pesquisa jurídica (jurisprudência + informativos)

RAG jurídico servido por MCP (LXC `ia-rag`, via Tailscale `http://100.65.53.53:8765/mcp`).
**Dois corpora isolados** no mesmo servidor (bases/índices separados — resultados nunca se misturam):

| Corpus | Conteúdo | Tools |
|---|---|---|
| **juris** | acórdãos/sentenças: TRF5, Turmas Recursais, STJ (~1,05M), STF, Pangea | `juris_rag_search` · `juris_rag_inteiro_teor` |
| **informativos** | informativos de jurisprudência do STF (1–1221) e STJ (1–893) | `informativos_rag_search` · `informativos_rag_inteiro_teor` |

Embedding BGE-M3 + busca híbrida (densa + BM25). Recuperação ~85 ms.

## Qual corpus usar?

- Quer **a decisão em si** (precedente, inteiro teor de um acórdão/sentença, citar o que o
  tribunal decidiu num processo)? → **juris**.
- Quer a **tese/ementa destacada** num informativo, "o que saiu no informativo do STJ sobre X",
  ou uma **edição** específica? → **informativos**.
- Na dúvida ou para cobertura ampla, pode consultar os dois (são tools distintas).

## Regra de ouro: BUSCAR ≠ LER O INTEIRO TEOR

São dois mecanismos **diferentes** em cada corpus. Não confunda:

| Ferramenta | O que faz | Mecanismo |
|---|---|---|
| `*_rag_search` | **ACHA** trechos relevantes | busca semântica (embedding + FAISS + BM25) — aproximada |
| `*_rag_inteiro_teor` | **LÊ** o texto completo | **consulta direta ao banco** — exata, verbatim |

➡️ **Para o texto completo, SEMPRE use `*_rag_inteiro_teor`.** **NUNCA** remonte o inteiro teor
juntando resultados do `search` — os trechos são fragmentos (com overlap), podem misturar
documentos e ficam incompletos. O `inteiro_teor` é barato, exato e não alucina.

## Fluxo — jurisprudência (2 passos)

1. **Achar** — `juris_rag_search(pergunta, ...)`
   - Pergunta em linguagem natural (descreva o tema/tese).
   - Filtros: `tribunal` (`TRF5`, `TR-PE`, `STJ`, `STF`, `JFPE`…), `grau`, `tipo_doc`, `ano_min`, `ano_max`.
   - Retorna trechos rankeados + **`processo`** + **`parent_id`** (guarde-os).
2. **Ler/citar** — `juris_rag_inteiro_teor(parent_id="...")` (ou `processo`)
   - Texto completo e verbatim (tabela `parents`). **Use antes de citar/transcrever.**

## Fluxo — informativos (2 passos)

1. **Achar** — `informativos_rag_search(pergunta, ...)`
   - Filtros: `tribunal` (`STF`/`STJ`), `tipo_doc` (`informativo`, `tema_stf`, `tema_stj`), `ano_min`, `ano_max`.
   - Retorna trechos com **tribunal**, **nº da edição** e **data** + **`chunk_id`**.
2. **Ler** — `informativos_rag_inteiro_teor(edicao=N, tribunal="STJ")` p/ a **edição inteira**,
   ou `informativos_rag_inteiro_teor(chunk_id=...)` p/ um julgado específico.
   - ⚠️ A numeração de `informativo` colide com a de `tema_stf`/`tema_stj`; por isso o default é
     `tipo_doc="informativo"`. Para um tema pelo número, passe `tipo_doc="tema_stj"`.
   - 💡 O informativo é um **resumo/tese**; o **inteiro teor do acórdão citado** está no corpus
     **juris** — pegue o nº do processo no informativo e busque via `juris_rag_*`.

## Disciplina jurídica

- **Cite sempre pelo número do processo / edição** (vem em todo resultado).
- O **trecho do search é só relevância**; a fonte autoritativa é o **inteiro teor**.
- Você (Claude) lê os trechos e raciocina — **não há tool de "resposta pronta"**.
- Não invente processo, relator, edição ou tese — se não veio do RAG, diga que não achou.

## Dicas

- Sem bons resultados? Reformule (mais contexto/tese) ou solte filtros; peça `k` maior p/ abrangência.
- A RAG é **somente leitura**; atualização do corpus é processo à parte (no `ia-rag`).
