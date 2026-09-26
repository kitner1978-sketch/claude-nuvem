# Calibração + memória persistente (melhoria #10)

Torna o rigor **medível**. Sem ledger, "pertinente" é opinião; com ledger, há taxa de
acerto e limiares defensáveis — o mesmo padrão dos estudos jurimétricos auditáveis do
projeto.

## 1. Ledger de decisões — `ledger/decisoes.jsonl`

Uma linha JSON por execução da skill (append-only). Grave no estágio [9].

```json
{
  "ts": "AAAA-MM-DDTHH:MM:SS",
  "caso": {"tese": "…", "fatos_materiais": ["…"], "pedido": "…",
           "orgao_alvo": "3ª TR-JFPE", "perspectiva": "parte-autora", "rigor": "padrão"},
  "busca": {"variantes": ["…", "…"], "n_candidatos": 34, "n_lidos": 12},
  "decisoes": [
    {"processo": "…", "veredito": "PERTINENTE",
     "eixo_critico": "E2", "adversarial": {"votos_refutaram": 0, "de": 3},
     "destino": "citado", "cluster_tamanho": 7},
    {"processo": "…", "veredito": "DESCARTADO",
     "eixo_critico": "E6", "motivo": "superado por Tema X", "destino": "descartado"}
  ],
  "desfecho": null
}
```

`ts` não pode vir de `Date.now()` dentro de Workflow (indisponível) — carimbe a data no
momento da escrita via Bash/ambiente, ou peça ao usuário se for retroativo.

## 2. Feedback loop

Quando o usuário reportar o resultado real (o juiz distinguiu? a parte adversa refutou?
o precedente segurou na sentença/acórdão?), **atualize `desfecho`** na linha
correspondente:

```json
"desfecho": {"citado": "0000000-…", "resultado": "segurou|distinguido|refutado",
             "por": "juiz|adversario", "observacao": "…"}
```

## 3. Padrões confirmados → memória do projeto

Quando um padrão se repetir e se confirmar no ledger (ex.: *"acórdão que só reproduz a
ementa do STJ sem enfrentar o fato concreto X é distinguido em ~toda vez"*), promova a
**memória** do projeto:

- diretório: `~/.claude/projects/-Volumes-Macintosh-NVMe-jurisprudencia/memory/`
- formato do projeto: **um fato por arquivo** com frontmatter (`type: feedback` ou
  `reference`), corpo com **Why:** e **How to apply:**, links `[[…]]`;
- adicione o ponteiro de uma linha em `MEMORY.md`.

Esses fatos realimentam a rubrica (`references/rubrica.md`) — ex.: virar um sub-teste
explícito no eixo E3 ou E6.

## 4. Auditoria de amostra (recalibração)

Periodicamente (ou quando o usuário pedir "audita a pertinência"):

1. amostre N decisões passadas do ledger que tenham `desfecho`;
2. compare veredito da skill × resultado real → **precisão** (dos citados, quantos
   seguraram) e sinal de **recall** (algum descartado deveria ter sido citado?);
3. se um eixo erra sistematicamente, ajuste seu limiar de veto/rebaixamento e registre
   a mudança como memória `feedback`.

Meça e relate honestamente — inclusive quando a skill errou.
