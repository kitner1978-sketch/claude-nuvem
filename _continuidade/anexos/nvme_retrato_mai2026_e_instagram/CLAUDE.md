# Projeto: Livro de Direito Previdenciário — Pipeline de Agentes + Obsidian Vault

## Identidade da Obra

- **Título:** "Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais"
- **Autores:** Claudio Kitner e Luiz Bispo da Silva Neto
- **Público-alvo:** Advogados previdenciaristas e magistrados de Juizados Especiais Federais

## Estrutura do Vault Obsidian

Este projeto é um **vault Obsidian** que funciona como base de pesquisa e produção do livro. A pesquisa é salva como fichas individuais em Markdown com YAML frontmatter, wiki-links e callouts — permitindo navegação, busca por tags e cruzamento de fontes diretamente no Obsidian.

```
D:\Projeto Livro\
├── pesquisa\
│   ├── legislacao\         ← uma ficha por dispositivo/diploma
│   ├── jurisprudencia\     ← uma ficha por julgado/súmula/tema
│   ├── doutrina\           ← uma ficha por autor+obra
│   ├── templates\          ← templates Obsidian (não editar)
│   └── MOC_cap_XX.md       ← mapa de conteúdo por capítulo
├── config\
│   ├── prompts.yaml
│   ├── models.yaml
│   └── book_structure.yaml
├── scripts\
│   └── formatador.py
├── state\
│   ├── pipeline_state.json
│   └── glossario.json
├── output\
│   ├── capitulos\          ← texto final aprovado
│   ├── rascunhos\          ← rascunhos intermediários
│   └── auditoria\          ← relatórios de auditoria
└── .obsidian\
```

## Arquitetura

Este projeto usa um **pipeline de agentes** para gerar capítulos de um livro doutrinário. Cada agente tem um papel específico, um modelo designado e regras invioláveis.

### Roteamento de Modelos

| Agente | Modelo | Justificativa |
|---|---|---|
| Coordenador | Sonnet | Decisões de roteamento, gerência do fluxo |
| Pesquisador | Sonnet | Formulação de queries, interpretação de resultados |
| Redator | **Opus 4.6** | Prosa doutrinária, estilo, raciocínio longo |
| Advogado do Diabo | Sonnet | Raciocínio adversarial sobre texto delimitado |
| Auditor | Haiku | Verificação binária de citações (mecânica) |
| Formatador | Python puro | Zero tokens — script determinístico |
| Consistência | **Opus 4.6** | Contexto longo, múltiplos capítulos |

### Grafo de Execução

```
ENTRADA HUMANA (tema + diretrizes)
       │
       ▼
PESQUISADOR (Sonnet) ◄─── loop máx 2x ◄── AUDITOR reprova
  │ Gera fichas MD individuais no vault:
  │   pesquisa/legislacao/*.md
  │   pesquisa/jurisprudencia/*.md
  │   pesquisa/doutrina/*.md
  │   pesquisa/MOC_cap_XX.md
       │
       ▼
REDATOR (Opus 4.6) ◄──── loop máx 2x ◄── ADVOGADO DO DIABO (objeções CRÍTICAS)
       │
       ▼
ADVOGADO DO DIABO (Sonnet)
       │
       ├─ sem objeções críticas → AUDITOR
       └─ com objeções críticas → volta ao REDATOR
       │
       ▼
AUDITOR (Haiku)
       │
       ├─ aprovado (score ≥ 0.95) → FORMATADOR
       ├─ aprovado (score < 0.95) → FORMATADOR + flags
       └─ reprovado → volta ao PESQUISADOR
       │
       ▼
FORMATADOR (Python)
       │
       ▼
CONSISTÊNCIA (Opus 4.6) — caps 1-2 individual, depois a cada 3
       │
       ▼
APROVAÇÃO HUMANA
```

## Fontes de Pesquisa

### Legislação e Jurisprudência — SEMPRE via web search
- planalto.gov.br (legislação federal)
- portal.stf.jus.br (jurisprudência STF, súmulas vinculantes)
- www.stj.jus.br (jurisprudência STJ, temas repetitivos)
- www.cjf.jus.br/cjf/tnu (TNU)
- datajud.cnj.jus.br (CNJ)
- TRFs (TRF1 a TRF6)

⚠ **NUNCA usar PDFs do Drive para legislação ou jurisprudência.**

### Doutrina — Google Drive + web search
- PDFs de doutrina no Google Drive dos autores
- Autores de referência obrigatória:
  - João Batista Lazzari e Carlos Alberto Pereira de Castro
  - Ivan Kertzman
  - José Antonio Savaris
  - Marisa Santos
  - Fábio Zambitte Ibrahim
  - Miguel Horvath Júnior
- Priorizar edições mais recentes

## Regras Gerais do Pipeline

1. **Máximo de 3 iterações** por capítulo (loops combinados).
2. **Caps 1 e 2:** aprovação individual obrigatória antes do seguinte.
3. **Caps 3+:** execução em lotes de até 3, aprovação do lote.
4. **Consistência:** roda nos caps 1-2 e depois a cada 3 capítulos.
5. **Comunicação com o autor:** só texto final + flags. Etapas intermediárias só se houver problema.
6. Estado persistido em `state/pipeline_state.json`.
7. Capítulos aprovados versionados via Git.

## Convenções Obsidian

### Frontmatter YAML
Toda ficha de pesquisa começa com frontmatter YAML delimitado por `---`. Campos obrigatórios variam por tipo (ver templates em `pesquisa/templates/`).

### Wiki-links
Usar `[[nome_do_arquivo]]` para conectar fichas entre si. Exemplos:
- `[[CF88_art194_a_204]]` — link para ficha de legislação
- `[[STJ_Tema_995]]` — link para ficha de jurisprudência
- `[[Ibrahim_2023_Curso]]` — link para ficha de doutrina

### Callouts
- `> [!quote]` — citações literais (lei seca, teses, doutrina)
- `> [!warning]` — conflitos, alertas, mudanças legislativas
- `> [!tip]` — observações práticas para JEFs
- `> [!info]` — informações complementares

### Tags
Usar no frontmatter e no corpo. Tags padrão:
- `#legislação`, `#jurisprudência`, `#doutrina`
- `#pesquisa`, `#cap_XX`
- `#vigente`, `#revogado`, `#transição`
- Tags temáticas: `#aposentadoria`, `#pensão`, `#BPC`, etc.

### Nomenclatura de Arquivos
- Legislação: `{diploma}_{artigos}.md` → `CF88_art194_a_204.md`, `Lei8213_art57.md`
- Jurisprudência: `{tribunal}_{referencia}.md` → `STJ_Tema_995.md`, `STF_SV_33.md`
- Doutrina: `{Sobrenome}_{ano}_{obra_abreviada}.md` → `Ibrahim_2023_Curso.md`

---

# PROMPTS DOS AGENTES

Todos os prompts estão em `config/prompts.yaml`. Os agentes devem ser executados seguindo estritamente os prompts definidos lá.

## Como Executar um Capítulo

Quando o autor pedir para gerar um capítulo:

### Passo 1 — Pesquisador (Sonnet)
Ler o prompt do Pesquisador em `config/prompts.yaml`. Executar pesquisa conforme o protocolo (legislação via web, jurisprudência via web, doutrina via Drive + web).

**DIFERENÇA PRINCIPAL:** O Pesquisador agora gera **fichas individuais em Markdown** no vault Obsidian:
- Uma ficha por dispositivo/diploma em `pesquisa/legislacao/`
- Uma ficha por julgado/súmula/tema em `pesquisa/jurisprudencia/`
- Uma ficha por autor+obra em `pesquisa/doutrina/`
- Um MOC (Map of Content) em `pesquisa/MOC_cap_XX.md`

Seguir os templates em `pesquisa/templates/`. Avaliar confiança.

Se confiança < 0.6: alertar o autor antes de prosseguir.

### Passo 2 — Redator (Opus 4.6)
Ler o prompt do Redator em `config/prompts.yaml`. Receber as fichas de pesquisa do vault (ler os arquivos MD gerados) + diretrizes. Gerar capítulo completo em Markdown.

### Passo 3 — Advogado do Diabo (Sonnet)
Ler o prompt do Advogado do Diabo em `config/prompts.yaml`. Analisar o rascunho contra as fichas de pesquisa. Classificar objeções (CRÍTICA/RELEVANTE/SUGESTÃO).

- CRÍTICAS → voltar ao Redator (máx 2x)
- RELEVANTE/SUGESTÃO → viram flags, segue para Auditor

### Passo 4 — Auditor (Haiku)
Ler o prompt do Auditor em `config/prompts.yaml`. Verificar cada citação contra as fichas de pesquisa do vault.

- Aprovado (≥0.95) → Formatador
- Reprovado → voltar ao Pesquisador (máx 2x)

### Passo 5 — Formatador
Executar `scripts/formatador.py` sobre o texto. Padronizar referências, boxes, bibliografia.

### Passo 6 — Consistência (Opus 4.6, quando aplicável)
Ler o prompt de Consistência em `config/prompts.yaml`. Verificar contra glossário e capítulos anteriores.

### Passo 7 — Apresentação ao Autor
Formato:
```
## Capítulo [N] — [Título]
**Status:** Pronto para revisão
**Palavras:** X.XXX | **Score auditoria:** XX% | **Iterações:** N
**Fichas de pesquisa geradas:** X legislação, X jurisprudência, X doutrina
**Flags de revisão humana:** [lista, se houver]

[texto completo do capítulo]

[bibliografia ABNT]
```
