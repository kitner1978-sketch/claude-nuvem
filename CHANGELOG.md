# CHANGELOG — Direito Previdenciario: Teoria e Pratica nos JEFs

## [tooling] — 2026-05-30 — Modularizacao do Design Code

Refatoracao dos scripts de geracao, sem alteracao do PDF (validado: 1.270 paginas, identico ao baseline v12).

### Novo modulo `scripts/design_code.py`
Fonte unica de verdade para a identidade visual: cores (`COLORS`), fontes (`FONT_SERIF`/`FONT_SANS`), escala tipografica (`SIZE_BODY`/`SIZE_SECTION`/`SIZE_SUBSECTION`), geometria A5 (`MARGINS_A5`) e helpers compartilhados (`apply_a5_margins`, `add_page_field`, `hex_to_rgb`).

### Centralizacao
- Fonte "EB Garamond" (~100 ocorrencias) e "Noto Sans" (~70) hardcoded -> `FONT_SERIF`/`FONT_SANS`. Trocar a tipografia agora e 1 edicao.
- Margens A5, antes duplicadas literalmente em `set_page_a5_mirrored` e `setup_section`, unificadas em `apply_a5_margins`.
- Tamanhos de corpo/secao/subsecao (duplicados entre os dois scripts) -> tokens unicos.

### Deduplicacao
- Campo PAGE (`_add_page_field` / `add_page_number_field`, 22 linhas identicas) -> `add_page_field` unico.
- Estilo Normal (9 linhas identicas) -> `apply_normal_style`.

Funcoes-monstro (`create_unified_docx`, `generate_docx`, `add_box`) deliberadamente **nao** alteradas (alto risco de mudar o layout, baixo ganho). Ver `reviews/analise_modularizacao_scripts.md`.

---

## [v12] — 2026-05-29

### Revisao qualitativa completa (23 capitulos)

Revisao sistematica em tres dimensoes: (1) precisao normativa, (2) exatidao jurisprudencial, (3) coerencia doutrinaria transversal. Todos os 23 relatorios salvos em `output/revisao_capXX.md`.

#### Metricas globais

| Metrica | Total |
|---------|-------|
| Achados criticos | 74 |
| Achados medios | 158 |
| Achados leves | 191 |
| Posicoes doutrinarias catalogadas | 255 |
| Itens de jurisprudencia verificados | ~170 |
| Contradicoes entre capitulos | 0 |

#### Correcoes aplicadas por faixa

| Faixa | Edicoes | PDF |
|-------|---------|-----|
| Caps 1-5 | ~30 | v10 (1.266pp) |
| Caps 6-15 | ~59 | v11 (1.268pp) |
| Caps 16-23 | ~37 | v12 (1.270pp) |
| **Total** | **~126** | |

---

### Detalhamento por capitulo

#### Parte I — Fundamentos (Caps. 1-5)
- Correcoes de terminologia pos-Lei 13.846/2019
- Atualizacao de valores monetarios para 2026 (SM R$ 1.621,00, Teto R$ 8.475,55)
- Correcao de metadata YAML
- Subdivisao de secoes de Referencias (Legislacao/Jurisprudencia/Doutrina)

#### Parte II — Incapacidade (Caps. 6-7)
- **Cap 6**: Terminologia "auxilio-doenca" corrigida em prosa corrente; nota sobre art. 151 revogado (Lei 13.135/2015); refs subdivididas; nota sobre Tema 1.246/STJ; nota sobre burnout CID-10 vs CID-11
- **Cap 7**: Terminologia corrigida; refs subdivididas; nota sobre burnout CID-11 QD85 vs CID-10 Z73.0

#### Parte III — Aposentadorias (Caps. 8-12)
- **Cap 8**: Frase duplicada removida (secao 8.3.2); Tema 1.070/STJ adicionado; refs subdivididas; metadata `parte` adicionada
- **Cap 9**: Refs subdivididas; metadata adicionada
- **Cap 10**: Metadata corrigida (II→III); vida toda "pendente"→"revertida pelo STF em novembro de 2025"; exemplo Helena corrigido (sem direito adquirido); secoes 10.14.2/10.14.3 reordenadas
- **Cap 11**: Metadata corrigida; Tema 334 STJ→STF (RE 630.501/RS) em 2 ocorrencias; paradigma Tema 422 nas refs corrigido (REsp 1.310.034/PR→1.151.363/MG)
- **Cap 12**: Metadata corrigida; pontuacao 2026 103/93→102/92; "portador de visao monocular"→"pessoa com visao monocular" (3 ocorrencias)

#### Parte IV — Pensoes, Auxilios e BPC (Caps. 13-18)
- **Cap 13**: "Relator para o acordao"→"O Relator" (Min. Barroso); "unissonas"→"unisonas"; art. 102→167 Decreto 3.048/99 (2 ocorrencias); frame-phrase "Importa distinguir" removida
- **Cap 14**: TODOS os valores 2025→2026 (SM R$1.518→R$1.621 em 13 ocorrencias; teto R$8.157→R$8.475; JEF R$91.080→R$97.260; MEI 5% e 11% recalculados); carencia "0 ou 12"→"0"; nota sobre regime intermediario 18/01-12/11/2019; limite baixa renda com nota de verificacao
- **Cap 15**: Cota SF R$62,04→R$67,54 (4x); teto SF R$1.819,26→R$1.980,38 (4x); calculos derivados corrigidos; Portaria 6→13 de 2026 (5x); anos citacoes Kertzman/Santos corrigidos; refs subdivididas
- **Cap 16**: YAML parte V→IV; "12 ultimos, se mais favoravel" removido do Quadro 16.6; art. 19 EC 103 adicionado ao Quadro 16.5; frame-phrase corrigida; refs subdivididas
- **Cap 17**: YAML frontmatter inserido; competencia JEFs art. 3o §3o→caput; "tres alteracoes"→"quatro marcos"; Memorando-Circular padronizado (3 ocorrencias)
- **Cap 18**: YAML parte adicionada; ref cruzada Cap 7→Cap 6 (biopsicossocial); ref cruzada Cap 8→Cap 6 (pericia); "portador de deficiencia"→"pessoa com deficiencia"

#### Parte V — Transversais (Caps. 19-21)
- **Cap 19**: YAML parte adicionada; secao de Referencias reestruturada com Legislacao/Jurisprudencia/Doutrina (12 julgados incluidos)
- **Cap 20**: YAML parte adicionada; Quadro 20.3 celulas corrompidas (",") corrigidas (4 celulas); legenda de abreviaturas adicionada
- **Cap 21**: YAML parte adicionada (2 arquivos); mapa de secoes corrigido "21.1 a 21.8"→"21.2 a 21.8" (2 arquivos)

#### Parte VI — Processo (Caps. 22-23)
- **Cap 22**: YAML frontmatter inserido; 3 referencias a "Parte B" eliminadas; introducao atualizada (3→4 blocos); nome Rel. Min. Barroso padronizado (8 ocorrencias em 3 arquivos)
- **Cap 23**: YAML parte adicionada; Sumula 235→501/STF (competencia acidentaria); nota sobre embargos suspensao vs interrupcao; refs subdivididas

---

### Achados criticos por capitulo (para referencia do autor)

| Cap | Criticos | Principais achados |
|-----|----------|--------------------|
| 1 | 3 | Metadata, valores desatualizados, terminologia |
| 2 | 4 | Temas fabricados, valores, metadata |
| 3 | 2 | Referencia cruzada, normativa |
| 4 | 4 | Valores, metadata, terminologia |
| 5 | 3 | Valores, terminologia, metadata |
| 6 | 6 | Art. 151 revogado, Tema 1.246 nao confirmado, terminologia |
| 7 | 4 | Burnout CID, pericias, terminologia |
| 8 | 5 | Frase duplicada, Tema 1.070 ausente, metadata |
| 9 | 3 | Metadata, normativa, refs |
| 10 | 3 | Vida toda contradicao, exemplo Helena errado, metadata |
| 11 | 4 | Tema 334 STJ→STF, paradigma Tema 422, edicoes doutrinarias |
| 12 | 5 | Metadata, terminologia, pontuacao, art. LC 142 |
| 13 | 3 | Tema 739 INCORRETO, Tema 914 nao confirmado, relator Barroso |
| 14 | 5 | Valores 2025, periodizacao dual→triplice, box contradiz regime |
| 15 | 3 | Valores SF incorretos, Portaria errada, Tema 862 data |
| 16 | 4 | YAML, "12 ultimos" no Quadro 16.6, simulacao temporal, PcD |
| 17 | 3 | YAML ausente, competencia JEFs art. errado, citacoes baixas |
| 18 | 0 | Nenhum critico (apenas medios: refs cruzadas erradas) |
| 19 | 4 | YAML, STF Tema 1.057 ausente, refs sem subdivisao, citacoes |
| 20 | 1 | Quadro 20.3 celulas corrompidas |
| 21 | 0 | Nenhum critico (capitulo de alta qualidade) |
| 22 | 3 | YAML ausente, "Parte B" inexistente, introducao desatualizada |
| 23 | 2 | Sumula 235→501, embargos suspensao vs interrupcao |

---

### Posicoes doutrinarias acumuladas

255 posicoes catalogadas ao longo dos 23 capitulos, cobrindo:
- Terminologia e natureza juridica dos beneficios
- Direito intertemporal (tempus regit actum)
- Jurisprudencia vinculante (STF, STJ, TNU)
- Calculos e formulas de beneficio
- Procedimento administrativo e judicial
- Acumulacao e interacao entre beneficios

### Coerencia transversal

- **Zero contradicoes** entre capitulos identificadas
- Mapa de capitulo-sede respeitado em toda a obra
- Terminologia pos-Lei 13.846/2019 consistente
- Principio tempus regit actum aplicado uniformemente
- Temas repetitivos (350, 995, 1.102) tratados de forma coerente

---

## [v11] — 2026-05-29

Correcoes aplicadas nos Caps 6-15 (59 edicoes). PDF com 1.268 paginas.

## [v10] — 2026-05-15

Correcoes aplicadas nos Caps 1-5 (~30 edicoes). PDF com 1.266 paginas.
Primeira revisao qualitativa sistematica (Caps 1-5).
