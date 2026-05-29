# Estratégia de Revisão para Geração do PDF Final

## Diagnóstico Completo

### Problema 1 — Headings H1 e H2 espúrios nos MDs (CRÍTICO)
**Impacto**: Aparecem como texto no PDF, corrompem cabeçalhos e sumário.

| Capítulo | Linha | Problema | Correção |
|----------|-------|----------|----------|
| Cap 01 | L3 | `# PARTE I — EVOLUÇÃO HISTÓRICA...` | Remover linha (é divisor interno, não heading) |
| Cap 01 | L114 | `# PARTE II — PRINCÍPIOS CONSTITUCIONAIS...` | Remover linha |
| Cap 01 | L216 | `## Capítulo 1 — PARTE III — PRINCÍPIOS...` | Remover linha (H2 duplicado com nome de parte) |
| Cap 01 | L287 | `## Capítulo 1 — PARTE IV — REFORMAS...` | Remover linha |
| Cap 17 | L1 | `# Capítulo 17 —` (H1 em vez de H2) | Trocar `#` por `##` |

**Total**: 5 correções pontuais nos MDs.

### Problema 2 — `box-quadro` sem estilo no script (CRÍTICO)
**Impacto**: 31 box-quadro em 7 capítulos renderizam com estilo de `box-atencao` (cor errada, label errado).

| Capítulo | Quantidade |
|----------|-----------|
| Cap 01 | 3 |
| Cap 15 | 6 |
| Cap 16 | 8 |
| Cap 17 | 6 |
| Cap 20 | 3 |
| Cap 21 | 2 |
| Cap 22 | 3 |

**Correção**: Adicionar `box-quadro` ao dict `config` em `add_box()` do md_to_docx.py com estilo próprio (fundo cinza claro, borda cinza, label "QUADRO").

### Problema 3 — Tabelas Markdown não renderizadas (CRÍTICO)
**Impacto**: 1.142 linhas de tabela em 16 capítulos aparecem como texto corrido.

**Correção**: Adicionar parser de tabela ao `parse_markdown()` e renderizador de tabela ao `generate_docx()`. Tabelas markdown têm formato previsível: `| col1 | col2 |` com separador `|---|---|`.

### Problema 4 — Listas não renderizadas (MODERADO)
**Impacto**: 1.254 itens de lista (- item) e 341 itens numerados em 14 capítulos aparecem como parágrafo contínuo.

**Correção**: Adicionar parser de listas ao `parse_markdown()`. Listas `- item` devem renderizar com bullet point e recuo; listas `1. item` com número e recuo.

### Problema 5 — Itálico não processado (MODERADO)
**Impacto**: 98 trechos em *itálico* em 14 capítulos aparecem com asteriscos literais.

**Correção**: Estender `add_paragraph_with_bold()` para processar também `*itálico*` além de `**negrito**`.

### Problema 6 — Cabeçalhos do PDF incorretos (CRÍTICO)
**Impacto**: O cabeçalho de cada capítulo pode mostrar a parte errada porque o script `gerar_livro_pdf.py` configura o header DEPOIS de adicionar o conteúdo — as seções do Word associam headers por posição.

**Correção**: Configurar header ANTES de inserir conteúdo do capítulo. Também garantir que cada capítulo tenha sua própria seção Word com `section break`.

### Problema 7 — Sumário (TOC) precisa de estilos corretos
**Impacto**: O TOC usa Heading 1 (partes) e Heading 2 (capítulos), mas os estilos atribuídos no script podem ser sobrescritos pela formatação manual.

**Correção**: Garantir que os estilos Heading 1 e Heading 2 estejam corretamente vinculados aos elementos da parte e do capítulo. Usar `paragraph.style` ANTES de adicionar runs formatados.

## Plano de Execução (5 fases)

### Fase 1 — Correção dos MDs (5 correções pontuais)
- Remover 4 headings espúrios do cap_01
- Corrigir H1→H2 no cap_17
- Tempo estimado: 2 minutos

### Fase 2 — Upgrade do md_to_docx.py (parser + renderizador)
Adicionar ao script:
- Parser de tabelas markdown → bloco tipo `table`
- Parser de listas (- item e N. item) → bloco tipo `list_item`
- Suporte a `*itálico*` no processador inline
- Estilo para `box-quadro` (fundo #F5F3EF, borda #A09882, accent #6B6256, label "QUADRO")
- Tempo estimado: 15 minutos

### Fase 3 — Correção do gerar_livro_pdf.py
- Configurar header/footer de cada seção ANTES do conteúdo
- Garantir que estilos Heading 1/2 persistam após formatação manual
- Adicionar sumário com formatação refinada
- Tempo estimado: 10 minutos

### Fase 4 — Regenerar todos os 23 DOCX individuais
- Rodar md_to_docx.py atualizado em todos os capítulos
- Verificar que não há regressões
- Tempo estimado: 5 minutos

### Fase 5 — Gerar PDF final e validação visual
- Rodar gerar_livro_pdf.py com script corrigido
- Validação: verificar cabeçalhos, sumário, tabelas, boxes, listas em pelo menos 5 capítulos amostrais
- Tempo estimado: 10 minutos
