---
name: pertinencia
description: >
  Triagem de PERTINÊNCIA de julgados para minutas — decide, com rigor jurídico e
  trilha auditável, se os precedentes achados na RAG realmente servem ao caso do
  usuário (similaridade semântica ≠ pertinência). Roda um funil: expande a consulta,
  busca, gradua lendo o INTEIRO TEOR contra uma rubrica de vetos, verifica de forma
  adversarial (superação/distinguishing), agrupa por tese e entrega um dossiê de
  citáveis pronto para a minuta. Use SEMPRE que a tarefa for: "esses julgados
  servem?", "triar/filtrar precedentes", "verificar pertinência", "quais desses cito
  na minuta", "achar precedentes fortes para a tese X", "esse acórdão é aplicável ao
  meu caso", "montar dossiê de jurisprudência". Sobe em cima da skill [[jur-rag]].
---

# pertinencia — triagem de precedentes para minutas

Camada de **julgamento** entre o retrieval (skill `jur-rag`) e a minuta. A busca dá
*recall* (traz o que é parecido); esta skill dá *precision jurídica* (decide o que é
**citável com segurança**). Regra fundadora:

> **Similaridade semântica NÃO é pertinência jurídica.** Uma ementa textualmente
> parecida pode ser imprestável: *ratio* diferente, tese superada, órgão sem
> aderência, fato distintivo material. A skill existe para pegar exatamente isso.

## Parâmetros do uso (defaults)

A skill é **genérica** e **parametrizada**. No começo de cada uso, fixe (pergunte só o
que faltar):

- **órgão-alvo** — onde a minuta vai tramitar (ex.: `3ª TR-JFPE`, `7ª Turma TRF5`,
  `STJ`). Governa a *aderência do órgão* (eixo E7 da rubrica). Se o usuário não disser,
  trate como genérico e sinalize.
- **perspectiva** — `parte-autora` | `parte-ré` | `gabinete`. Governa a **polaridade
  padrão** e o bloco "contrários". Default: `parte-autora`. Gabinete → tom neutro, os
  dois lados pesam igual.
- **rigor** — `padrão` (funil completo) | `expresso` (pula travessia de citações e
  reduz o adversarial a 1 voto). Default: `padrão`.

## Entradas obrigatórias (sem isto, pertinência é chute)

Antes de rodar o funil, extraia/peça **três coisas** do caso do usuário. Se faltar,
peça objetivamente:

1. **Fatos materiais** — os fatos que sustentam (ou derrubam) a tese, não o relatório
   inteiro. Ex.: "laudo parcial, autor 58 anos, trabalho braçal, 3ª série".
2. **Tese a sustentar** — a proposição jurídica que a minuta vai defender, em uma
   frase afirmativa. Ex.: "condições pessoais suprem a incapacidade parcial do laudo".
3. **Pedido/dispositivo pretendido** — o que se quer que o julgador faça (concessão,
   reforma da dosimetria, extinção etc.). Define a *direção do dispositivo* buscada.

Reformule as três em suas palavras e confirme antes de gastar busca.

---

## O funil (estágios)

Rode em ordem. Cada estágio estreita o conjunto; o rigor cresce (e o custo também —
ver **Tiering** no fim).

```
Caso {fatos, tese, pedido, órgão-alvo, perspectiva}
  [0] Estruturar o caso
  [1] Expandir consulta (multi-query)      ← ataca o recall (~29% keyword) na origem
  [2] Buscar + fundir + dedup              ← jur_rag_search em cada variante
  [3] Triagem barata (metadados+ementa)    ← corta óbvios; modelo barato
  [4] Grading rigoroso (INTEIRO TEOR)      ← rubrica de vetos; 1 subagente por candidato
  [5] Travessia de citações                ← leading case + detecção de superação
  [6] Verificação adversarial              ← tenta REFUTAR cada sobrevivente
  [7] Clusterizar + escolher representante ← peso ≠ repetição; mata falso-amigo
  [8] Cross-grounding legislação/súmula     ← tese ainda bate com o texto legal vigente?
  [9] Dossiê + ledger                       ← saída p/ minuta + registro auditável
```

### [0] Estruturar o caso
Normalize as três entradas em um objeto de trabalho. Identifique: institutos/termos de
arte, artigos de lei, Temas/Súmulas prováveis, marco temporal (lei aplicável) e a
**polaridade desejada** do dispositivo. Isso alimenta a expansão.

### [1] Expandir consulta (multi-query) — melhoria #7
O recall por keyword é baixo (você mediu ~29%). **Não busque uma vez só.** Gere de 4 a
8 variantes da consulta e una os resultados:
- **sinônimos jurídicos / termos de arte** ("miserabilidade" ↔ "hipossuficiência" ↔
  "renda per capita ¼ do salário mínimo");
- a tese em forma **afirmativa E negativa** (você PRECISA achar quem a rejeita — é
  insumo do bloco "contrários" e do adversarial);
- **âncoras duras**: nº de artigo, nº de Tema/Súmula, nome do instituto;
- variação de **granularidade** (uma consulta ampla + consultas estreitas por
  sub-questão, se a tese tiver partes).
Registre as variantes usadas (entram no ledger).

### [2] Buscar + fundir + dedup
Rode `mcp__jur-rag__juris_rag_search` para cada variante, com filtros do órgão-alvo
(`tribunal`, `grau`, `tipo_doc`, `ano_min/ano_max`) — mas **sem estrangular**: filtro
apertado demais volta a matar recall. Fontes especializadas quando couber:
`mcp__jurisprudencia_stf__*` (STF inteiro teor), `mcp__jurisprudencia_sentencas__*`
(G1), `mcp__jurisprudencia_7turma__*`. Funda todos os hits, **dedup por `processo` /
`parent_id`**, guarde `parent_id` de cada um. Alvo: 20–40 candidatos.

### [3] Triagem barata
Antes de ler inteiro teor (caro), corte os óbvios só com metadados + trecho do search:
tema claramente errado, polaridade oposta irrecuperável, órgão sem qualquer aderência,
fora da janela temporal da lei aplicável. **Regra:** na dúvida, NÃO corte aqui —
descartes definitivos são no grading. Registre o motivo de cada corte.

### [4] Grading rigoroso — o coração (rubrica em `references/rubrica.md`)
Para cada sobrevivente, **leia o inteiro teor** com
`mcp__jur-rag__juris_rag_inteiro_teor(parent_id=...)` — **nunca** julgue pela ementa (a
ementa mente sobre a *ratio*). Aplique a **rubrica de vetos** (`references/rubrica.md`):
sete eixos, cada um pode **vetar** ou **rebaixar**. Saída por candidato:
`PERTINENTE` / `PERTINENTE-COM-RESSALVA` / `DESCARTADO`, com uma linha de justificativa
por eixo, o **trecho-âncora** (a *ratio*, verbatim, com pinpoint) e o **fator
distintivo** explícito (o que o adversário usaria para distinguir).

> **Paralelize:** 1 subagente por candidato (Agent tool), cada um lê um inteiro teor e
> devolve a rubrica preenchida no schema de `references/rubrica.md`. Escala com a frota
> e isola contexto.

### [5] Travessia de citações — melhoria #8
Do inteiro teor de cada `PERTINENTE`, extraia os julgados **que ele cita** e faça dois
movimentos:
- **Subir ao leading case** — se um acórdão de turma só repete tese do STJ/STF, busque
  o precedente-fonte (mais força). Cite a origem, use a turma como reforço.
- **Superação por quem cita depois** — busque julgados **posteriores** que citam o
  candidato; se o citam para **afastar/distinguir/superar**, é tese em erosão →
  rebaixa ou veta (eixo E6). "Muito citado" pode ser citado *contra*.
No modo `expresso`, pule este estágio.

### [6] Verificação adversarial — o que garante o rigor
Para cada sobrevivente, um passe **independente que tenta DERRUBAR** a citação (default:
refutar-se). Instrução ao verificador: *"assuma que este precedente NÃO serve; ache o
distinguishing material, a superação, o obiter, o órgão divergente. Só mantenha se não
conseguir refutar."* Rigor `padrão` = 3 votos (mantém se ≥2 sobrevivem); `expresso` = 1
voto. Use lentes distintas entre os votos (fática / vigência / ratio-vs-obiter) — não 3
refutadores idênticos. Rode como subagentes em paralelo.

### [7] Clusterizar + representante — melhoria #11
Muitos candidatos são a **mesma tese repetida** (boilerplate quase igual). Agrupe por
*ratio*; por cluster:
- escolha **um representante** (mais recente + mais forte + melhor fundamentado) p/ citar;
- reporte o **tamanho do cluster** como *peso* da tese ("jurisprudência copiosa"), sem
  encher a minuta de 12 ementas iguais;
- **mate o falso-amigo semântico**: se o cluster se formou por texto de enchimento
  (relatório, lei transcrita) e não pela controvérsia, dissolva-o — só vale cluster que
  compartilha a *ratio*.

### [8] Cross-grounding legislação/súmula — bônus
Confirme que a tese do precedente **ainda bate com o texto legal vigente**. Use
`mcp__jur-rag__legislacao_rag_search` / `mcp__legislacao__buscar_legislacao` e os
informativos (`mcp__jur-rag__informativos_rag_search`) para pegar precedente anterior a
reforma ou Tema afetado/pendente. Sinalize risco de vigência.

### [9] Dossiê + ledger
Monte a saída no formato de `references/saida.md` e **grave a decisão no ledger**
(seção Calibração). O dossiê é o entregável; o ledger é o que torna o rigor medível.

---

## Anti-alucinação (inegociável) — melhoria #4

- **Nunca inventar citação.** Todo citável carrega `processo`/`parent_id` REAL da RAG +
  trecho **literal** (copiado do inteiro teor, não parafraseado).
- **Pinpoint obrigatório** — o trecho exato que é a *ratio*, não "o acórdão diz que…".
- **Vigência ativa** — cruze com informativos/legislação e Temas antes de afirmar que
  vale.
- **Declare o vazio** — se a tese não tem respaldo forte no acervo, **diga isso**; não
  force 5 ementas fracas de enchimento. "Não achei precedente forte" é uma resposta
  válida e honesta.
- A fonte autoritativa é sempre o **inteiro teor**, nunca o trecho do `search`.

## Calibração + memória persistente — melhoria #10

A skill mede a própria precisão e aprende:

- **Ledger** (`ledger/decisoes.jsonl`, uma linha JSON por decisão): caso, variantes de
  busca, cada candidato com veredito da rubrica + veredito adversarial + destino
  (citado / descartado). Ver `references/calibracao.md` para o schema.
- **Feedback loop** — quando o usuário reportar o desfecho (o juiz distinguiu? a parte
  adversa refutou? o precedente segurou?), anexe ao ledger. Padrões que se confirmam
  (ex.: "acórdão que só repete ementa sem enfrentar o fato X sempre cai") viram
  **memória** em `~/.claude/projects/-Volumes-Macintosh-NVMe-jurisprudencia/memory/`
  (formato do projeto: um fato por arquivo + ponteiro no `MEMORY.md`), realimentando a
  rubrica.
- **Auditoria de amostra** — periodicamente, reavalie decisões passadas do ledger para
  checar se os vetos acertaram e recalibrar limiares. Sem isto, "rigor" é opinião; com
  isto, há taxa de acerto defensável (padrão dos seus estudos auditáveis).

## Tiering de custo — bônus

Gaste rigor onde importa:

- **barato/rápido**: estágios [1] expansão, [3] triagem;
- **caro/forte**: [4] grading (lê inteiro teor), [6] adversarial — subagentes em
  paralelo, um por item.

Nunca economize lendo ementa no lugar de inteiro teor no [4]/[6]: é ali que o
precedente falso passa.

## Ver também

- `references/rubrica.md` — os 7 eixos de veto + schema de saída por candidato.
- `references/saida.md` — formato do dossiê pronto p/ colar na minuta.
- `references/calibracao.md` — schema do ledger e protocolo de feedback.
- Skill [[jur-rag]] — camada de busca/inteiro teor por baixo desta.
