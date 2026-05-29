# Estratégia de Revisão de Ajustes Finos — Todos os Capítulos

**Data:** 14/05/2026
**Escopo:** Capítulos 02 a 23 (22 capítulos redigidos; Cap. 01 pendente de redação)
**Total:** ~335.000 palavras

---

## 1. Diagnóstico Geral

A auditoria automatizada de todos os 22 capítulos identificou **7 eixos de revisão** organizados em 3 fases, da mais mecânica (automatizável) à mais intelectual (exige leitura humana). Os números abaixo refletem a varredura completa.

### 1.1 Mapa de Status

| Cap | Título | Palavras | Status YAML | Boxes | Prefixo `box-` | Referências |
|-----|--------|----------|-------------|-------|-----------------|-------------|
| 01 | Evolução Histórica e Princípios Constitucionais | — | pipelinado | — | — | — |
| 02 | Segurados e Dependentes | 9.988 | pipelinado | 9 | ✅ | ✅ |
| 03 | Período de Carência | 9.985 | pipelinado | 11 | ✅ | ✅ |
| 04 | Contribuições Previdenciárias | 20.043 | aguard_aprov | 56 | ❌ | ✅ |
| 05 | Reconhecimento de TC | 17.043 | aguard_aprov | — | ❌ | ❌ |
| 06 | Aposent. Incapac. Permanente | 12.060 | pipelinado | 12 | ✅ | ✅ |
| 07 | Auxílio Incapac. Temporária | 12.974 | pipelinado | — | ❌ | ❌ |
| 08 | Aposentadoria Especial | 13.176 | pipelinado | — | ❌ | ❌ |
| 09 | Aposentadoria Rural | 16.325 | pipelinado | — | ❌ | ✅ |
| 10 | Aposent. Programada/Idade | 18.267 | aguard_aprov | 33 | ❌ (misto) | ❌ |
| 11 | Aposent. por TC / Transição | 18.015 | aguard_aprov | — | ❌ | ❌ |
| 12 | Aposent. PcD (LC 142) | 18.003 | aguard_aprov | — | ❌ | ❌ |
| 13 | Salário-Maternidade | 16.961 | aguard_aprov | 11 | ❌ | ❌ |
| 14 | Auxílio-Reclusão | 15.947 | aguard_aprov | 29 | ❌ | ❌ |
| 15 | Auxílio-Acidente e Sal.-Família | 8.452 | aprovado | 15 | ✅ | ✅ |
| 16 | Cálculo — SB e RMI | 15.423 | aprovado | 18 | ✅ | ✅ |
| 17 | Revisão de Benefícios | 20.770 | aprovado | 28 | ✅ | ✅ |
| 18 | BPC/LOAS | 18.904 | aprovado | 28 | ✅ | ✅ |
| 19 | Pensão por Morte | 19.540 | pipelinado | 33 | ❌ | ✅ |
| 20 | Acumulação de Benefícios | 16.927 | aprovado | — | ✅ | ✅ |
| 21 | Decadência/Prescrição/CJ | 18.193 | aprovado | 11 | ✅ | ✅ |
| 22 | Proc. Administrativo | 17.904 | aprovado | 17 | ✅ | ✅ |
| 23 | Competência e Proc. no JEF | 17.135 | pipelinado | — | ❌ | ✅ |

**Legenda:** ✅ = conforme | ❌ = precisa correção | — = não verificado/ausente

### 1.2 Achados Consolidados

| Eixo | Qtd. Total | Capítulos Mais Afetados |
|------|-----------|------------------------|
| "auxílio-doença" (termo proibido) | **72 ocorrências** | Cap. 07 (29), Cap. 06 (17), Cap. 03 (6), Cap. 15 (6) |
| "aposentadoria por invalidez" (termo proibido) | **37 ocorrências** | Cap. 06 (20), Cap. 03 (4), Cap. 07 (4) |
| Boxes sem prefixo `box-` | **~11 capítulos** | Caps. 04, 05, 07, 08, 09, 10, 11, 12, 13, 14, 19, 23 |
| Frame-phrases (anti-IA) | **42 ocorrências** | Cap. 14 (7), Cap. 07 (6), Cap. 02 (3), Cap. 03 (3), Cap. 05 (3) |
| "portanto" excessivo | **41 ocorrências** | Cap. 10 (8), Cap. 12 (6), Cap. 13 (4), Cap. 19 (4) |
| Em-dashes por capítulo (> 100) | **4 capítulos** | Cap. 04 (166), Cap. 17 (128), Cap. 11 (123), Cap. 12 (107) |
| Seção Referências ausente | **~10 capítulos** | Caps. 05, 07, 08, 10, 11, 12, 13, 14, 18(?), 22(?) |
| Título `## Capítulo N —` ausente | **2 capítulos** | Caps. 02, 03 |
| Numeração de seções (`### N.X`) ausente | **3 capítulos** | Caps. 02, 03, 06 |
| Cap. 17 — numeração dupla em headings | **1 capítulo** | Cap. 17 (17.1–17.53 com labels 17.X.Y embutidos) |
| Referência cruzada errada | **2 confirmados** | Cap. 16 (auxílio-reclusão → Cap. 19, deveria ser 14); Cap. 19 (ref "(9.15)" → deveria ser "(19.15)") |
| Valores monetários desatualizados em tabelas | **3 pontos** | Cap. 04 (teto), Cap. 16 (teto 2023/2024) |
| Título divergente entre arquivo e YAML | **2 capítulos** | Cap. 15 (falta "e Salário-Família"), Cap. 22 (título expandido) |

---

## 2. Fases da Revisão

### FASE 1 — Correções Mecânicas (automatizáveis por script/regex)

**Prioridade: MÁXIMA — rodar antes de qualquer revisão humana**
**Estimativa: 1 sessão**

#### 1A. Padronização de boxes (prefixo `box-`)

- **Regex:** `^::: (pratica|atencao|jurisprudencia|quadro)` → `::: box-$1`
- **Capítulos afetados:** 04, 05, 07, 08, 09, 10, 11, 12, 13, 14, 19, 23
- **Impacto:** ~200+ ocorrências. Sem risco de falso positivo (o padrão é unívoco).
- **Verificação:** Após aplicar, contar `^::: ` sem `box-` — deve ser zero.

#### 1B. Substituição terminológica — termos proibidos

Regra: substituir apenas em **texto corrido** (body text). **Preservar** o termo antigo quando:
- Estiver dentro de citação direta de lei/súmula/acórdão (entre aspas ou em bloco de jurisprudência)
- For referência histórica explícita ("antigo auxílio-doença", "então denominada aposentadoria por invalidez")

**Protocolo por capítulo:**

| Capítulo | `auxílio-doença` → `auxílio por incapacidade temporária` | `apos. por invalidez` → `apos. por incapacidade permanente` |
|----------|:---:|:---:|
| 03 | 6 (verificar quais são citações) | 4 |
| 04 | 1 | 1 |
| 05 | 2 | 2 |
| 06 | 17 (muitas em corpo, ~5 em citações) | 20 (idem, ~5 em citações) |
| 07 | 29 (capítulo-chave: ~15 são citações históricas) | 4 |
| 10 | 3 | 2 |
| 11 | 1 | 0 |
| 12 | 0 | 1 |
| 13 | 2 | 0 |
| 14 | 3 | 2 |
| 15 | 6 | 0 |
| 19 | 1 | 1 |
| 23 | 1 | 0 |

**Método seguro:** Para cada ocorrência, ler a frase circundante (contexto de 3 linhas). Se for citação direta → manter e adicionar nota "(atual [termo correto])" na primeira ocorrência da citação. Se for texto corrido → substituir.

#### 1C. Padronização do título H2

- **Caps. 02 e 03:** Acrescentar `## Capítulo N — ` antes do título existente.
- **Cap. 02:** `## Segurados e Dependentes` → `## Capítulo 2 — Segurados e Dependentes`
- **Cap. 03:** idem → `## Capítulo 3 — Período de Carência e Manutenção da Qualidade de Segurado`

#### 1D. Numeração de seções

- **Caps. 02, 03, 06:** Não possuem `### N.X` — usam headings descritivos.
- **Decisão necessária:** Padronizar TODOS os capítulos com numeração `### N.X` e `#### N.X.Y`, ou aceitar os 3 primeiros como exceção?
- **Recomendação:** Padronizar. Capítulos mais recentes (15–23) todos usam numeração. Será necessário numerar manualmente as seções de 02, 03 e 06.

#### 1E. Correção do Cap. 17 — numeração dupla

- **Problema:** Headings como `### 17.1 17.2.1 Art. 103...` contêm dois sistemas de numeração sobrepostos.
- **Ação:** Remover o primeiro número sequencial (17.1, 17.2...) e manter apenas o hierárquico (17.2.1, 17.2.2...), ou vice-versa. Exige leitura do capítulo para decidir qual é o sistema "real".
- **Risco:** Referências cruzadas dentro e fora do capítulo podem quebrar.

---

### FASE 2 — Revisão Estrutural (semi-automatizável, requer verificação)

**Prioridade: ALTA**
**Estimativa: 2–3 sessões**

#### 2A. Referências cruzadas entre capítulos

Erros confirmados:
1. **Cap. 16, linha 283:** Tabela atribui auxílio-reclusão ao "Cap. 19" — corrigir para "Cap. 14".
2. **Cap. 19, linha 114:** Referência "(9.15)" → corrigir para "(19.15)".
3. **Cap. 22, linha 209:** "seção 21.5.2 do Capítulo 21" — verificar se 21.5.2 existe como heading no cap. 21 (pode ser 21.5 sem sub-numeração).

Protocolo para todas as referências:
- Buscar `[Cc]ap(ítulo|\.)?\s*\d+` e `seção\s*\d+\.\d+` em todos os capítulos.
- Para cada referência, validar que o capítulo e a seção existem.
- Atenção especial ao Cap. 17 (numeração instável).

#### 2B. Seção de Referências Bibliográficas

**10 capítulos sem seção de Referências:** 05, 07, 08, 10, 11, 12, 13, 14, (18?), (22?)

Protocolo:
- Caps. que possuem `referencias:` no YAML frontmatter (ex.: Cap. 10): extrair de lá e formatar como `## Referências` ou `### N.X Referências` ao final.
- Caps. sem fonte alguma: gerar seção com legislação citada + doutrina referenciada no corpo.
- **Padrão adotado nos caps. mais recentes (21, 22):** Referências como última seção numerada (`### N.X Referências`), subdividida em `#### Legislação`, `#### Jurisprudência`, `#### Doutrina`.

#### 2C. Consistência de títulos entre arquivos e YAML

| Capítulo | Problema | Ação |
|----------|----------|------|
| 15 | YAML do arquivo: "Auxílio-Acidente" / YAML livro: "Auxílio-Acidente e Salário-Família" | Alinhar — o capítulo trata ambos |
| 22 | H2: "O Processo Administrativo Previdenciário e a Interface com os JEFs" / YAML: "Processo Administrativo Previdenciário" | Encurtar H2 ou expandir YAML |
| 16 | H2 usa dois-pontos; YAML usa travessão | Padronizar (travessão) |

#### 2D. YAML frontmatter

Alguns capítulos (02, 03, 22) não possuem YAML frontmatter; outros (04–21, 23) possuem com campos variáveis. 

**Decisão:** O frontmatter é necessário para o pipeline? Se sim, padronizar campos em todos. Se não, remover de todos para simplicidade.

#### 2E. Valores monetários em tabelas históricas

| Local | Valor | Ação |
|-------|-------|------|
| Cap. 04, tabela (linha ~808) | Teto R$ 7.786,02 (2024) | Acrescentar linha 2025/2026 com R$ 8.475,55 |
| Cap. 16, tabelas (linhas 637-638) | Teto R$ 7.507,49 (2023) e R$ 7.786,02 (2024) | Acrescentar linha 2025/2026 com R$ 8.475,55 |
| Cap. 19, tabela (linha ~629) | Possível R$ 1.320 | Verificar se é cálculo (OK) ou valor defasado |

**Nota:** Os valores correntes (SM = R$ 1.621,00 e Teto = R$ 8.475,55) já estão bem distribuídos: 84 e 37 ocorrências respectivamente. A SELIC 14,50% está correta no Cap. 17.

---

### FASE 3 — Revisão de Redação e Estilo (exige leitura humana assistida por IA)

**Prioridade: MÉDIA-ALTA**
**Estimativa: 1 sessão por capítulo (22 sessões) ou blocos de 3-4 capítulos**

#### 3A. Frame-phrases (anti-IA) — 42 ocorrências

Expressões a eliminar ou reescrever:
- "é importante destacar (que)" 
- "vale ressaltar (que)"
- "cumpre observar (que)"
- "nesse contexto"
- "nessa perspectiva"
- "é fundamental (que)"
- "merece destaque"
- "convém mencionar"
- "importa notar"

**Método:** Para cada ocorrência, substituir por construção mais direta. Exemplos:
- "É importante destacar que o INSS..." → "O INSS..."
- "Vale ressaltar que a jurisprudência..." → "A jurisprudência..."
- "Nesse contexto, o segurado..." → "O segurado..."

**Capítulos prioritários:** 14 (7), 07 (6), 02 (3), 03 (3), 05 (3).

#### 3B. Densidade de "portanto" — 41 ocorrências

Limite: máximo 1 por seção (### ou ####).

**Capítulos prioritários:** 10 (8 ocorrências), 12 (6), 13 (4), 19 (4).

Substituições possíveis: "dessa forma", "assim", "logo", "por conseguinte" — ou simplesmente eliminar (a conclusão muitas vezes é autoevidente).

#### 3C. Densidade de travessões (em-dashes)

Recomendação: máximo 2–3 por seção. Capítulos com mais de 100 travessões:

| Capítulo | Total | Seções | Média |
|----------|-------|--------|-------|
| 04 | 166 | ~20 | 8,3 |
| 17 | 128 | ~53 | 2,4 |
| 11 | 123 | ~20 | 6,2 |
| 12 | 107 | ~20 | 5,4 |
| 10 | 103 | ~17 | 6,1 |

**Ação:** Nos caps. 04, 11, 12 e 10, substituir travessões excessivos por vírgulas, parênteses ou reestruturação da frase. Cap. 17 está aceitável (média 2,4).

#### 3D. Parágrafos "sanduíche" e redundâncias

Padrão a eliminar: parágrafo que (1) enuncia um conceito, (2) dá exemplo, (3) repete o conceito com palavras diferentes. Detecção manual — usar IA para flaggar parágrafos com alta similaridade semântica entre primeira e última frases.

#### 3E. Fluidez das transições entre seções

Verificar se cada seção termina com uma frase de transição natural para a próxima, sem ser formulaica ("Passemos agora a analisar...").

#### 3F. Uniformidade da profundidade de `####`

- **Caps. 19, 22:** Estrutura plana (sem `####`). 
- **Caps. 21, 15, 16, 17:** Usam `####` extensivamente.
- **Decisão:** Aceitar variação (capítulos curtos = planos, longos = hierárquicos) ou padronizar?
- **Recomendação:** Aceitar variação desde que o sumário do livro seja consistente. Não forçar sub-subseções onde o conteúdo não as exige.

---

## 3. Ordem de Execução Recomendada

```
FASE 1 (Mecânica) — 1 sessão
  ├── 1A. Regex: boxes sem prefixo → box-   [12 capítulos]
  ├── 1B. Terminologia proibida              [13 capítulos, ~109 ocorrências]
  ├── 1C. Títulos H2 dos caps. 02, 03       [2 capítulos]
  ├── 1D. Numeração de seções caps. 02, 03, 06 [decisão + 3 capítulos]
  └── 1E. Cap. 17 — resolver numeração dupla [1 capítulo, complexo]

FASE 2 (Estrutural) — 2-3 sessões
  ├── 2A. Validar referências cruzadas       [22 capítulos]
  ├── 2B. Gerar/padronizar Referências       [10 capítulos]
  ├── 2C. Alinhar títulos arquivo ↔ YAML     [3 capítulos]
  ├── 2D. Padronizar ou remover frontmatter  [decisão global]
  └── 2E. Atualizar tabelas de valores       [3 pontos em 2 capítulos]

FASE 3 (Redação) — em blocos temáticos
  ├── Bloco A: Caps. 02–05 (Parte I — Fundamentos)
  ├── Bloco B: Caps. 06–07 (Parte II — Incapacidade)  ← maior carga terminológica
  ├── Bloco C: Caps. 08–12 (Parte III — Aposentadorias)
  ├── Bloco D: Caps. 13–18 (Parte IV — Pensões/Auxílios/BPC)
  ├── Bloco E: Caps. 19–21 (Parte V — Transversais)
  └── Bloco F: Caps. 22–23 (Parte VI — Processo)
```

---

## 4. Protocolo de Execução por Capítulo (Fase 3)

Para cada capítulo na Fase 3, o agente revisor deve:

1. **Ler** o capítulo inteiro
2. **Aplicar checklist automático:**
   - [ ] Zero ocorrências de "auxílio-doença" em texto corrido
   - [ ] Zero ocorrências de "aposentadoria por invalidez" em texto corrido
   - [ ] Todos os boxes com prefixo `box-`
   - [ ] Título no formato `## Capítulo N — Título`
   - [ ] Seções numeradas (`### N.X`, `#### N.X.Y`)
   - [ ] Seção `### N.X Referências` presente e subdivida
   - [ ] SM = R$ 1.621,00, Teto = R$ 8.475,55, SELIC = 14,50% a.a.
   - [ ] Máximo 1 "portanto" por seção
   - [ ] Máximo 2-3 travessões por seção
   - [ ] Zero frame-phrases
3. **Revisar redação:**
   - [ ] 1ª pessoa do plural consistente
   - [ ] Parágrafos-sanduíche eliminados
   - [ ] Transições fluidas entre seções
   - [ ] Citações inline (nunca notas de rodapé)
   - [ ] Referências cruzadas validadas
4. **Gerar relatório** de alterações com linha/antes/depois
5. **Rodar formatador** + gerar novo DOCX

---

## 5. Pendência: Capítulo 01

O Capítulo 01 ("Evolução Histórica e Princípios Constitucionais") consta no YAML como "pipelinado" mas **não existe arquivo de rascunho** na pasta `output/rascunhos/`. 

**Opções:**
- A) Redigir o Cap. 01 dentro do pipeline normal (pesquisa → estratégia → redação → revisão)
- B) Deixar para o final, após a revisão dos demais, para que o capítulo inaugural já nasça no padrão consolidado

**Recomendação:** Opção B — redigir por último, incorporando todas as decisões de estilo tomadas durante a revisão.

---

## 6. Decisões Pendentes (requerem input dos autores)

| # | Decisão | Opções | Recomendação |
|---|---------|--------|--------------|
| D1 | Numeração de seções nos caps. 02, 03, 06 | (a) Numerar todas / (b) Manter descritivo | (a) Numerar |
| D2 | YAML frontmatter | (a) Padronizar em todos / (b) Remover de todos | Depende do pipeline |
| D3 | Profundidade `####` | (a) Obrigatória quando > 3 parágrafos / (b) Livre por capítulo | (b) Livre |
| D4 | Cap. 17 — qual numeração manter | (a) Sequencial (17.1–17.53) / (b) Hierárquica (17.X.Y) | (b) Hierárquica |
| D5 | Termos antigos em citações diretas | (a) Manter + nota "(atual...)" / (b) Modernizar mesmo em citações | (a) Manter + nota |
| D6 | Cap. 01 — redigir agora ou ao final | (a) Agora / (b) Ao final da revisão | (b) Ao final |
