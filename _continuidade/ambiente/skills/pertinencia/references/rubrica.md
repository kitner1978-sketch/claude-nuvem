# Rubrica de pertinência — 7 eixos de veto

Aplicada no estágio [4] (grading) a cada candidato, **lendo o inteiro teor** (nunca a
ementa). Cada eixo pode **VETAR** (descarta o candidato) ou **REBAIXAR** (mantém como
`PERTINENTE-COM-RESSALVA`). Não é média ponderada frouxa — é gate: um veto sozinho
derruba.

| # | Eixo | Pergunta central | Efeito se falha |
|---|------|------------------|-----------------|
| **E1** | **Identidade da tese** | A *questão jurídica decidida* é a mesma? (não o tema geral — a controvérsia específica) | **VETO** se não |
| **E2** | **Identidade fática material** | Os fatos que sustentam a *ratio* coincidem? Quais fatos do caso do usuário faltam/divergem no precedente? | **VETO** se o fato distintivo for material à *ratio* |
| **E3** | **Ratio vs. obiter** | O trecho que interessa é *fundamento determinante* ou dito de passagem? | **REBAIXA** se obiter (persuasão fraca) |
| **E4** | **Direção do dispositivo** | O resultado é favorável à tese/pedido que a minuta vai sustentar? | Marca **polaridade**; se oposta → vai p/ bloco "contrários" |
| **E5** | **Força/hierarquia** | Vinculante (repetitivo/RG/súmula/IRDR) > STJ-STF persuasivo > turma > monocrática | **ORDENA** prioridade (não veta) |
| **E6** | **Vigência** | Superado, distinguido por julgados posteriores, lei mudou, Tema afetado/pendente? | **VETO** se superado; **REBAIXA** se em erosão/risco |
| **E7** | **Aderência do órgão** | O órgão prolator tem competência/aderência ao órgão-alvo do caso? | **REBAIXA** se órgão divergente; nota se turma de linha oposta |

## Como decidir o veredito final

- **DESCARTADO** — qualquer VETO em E1, E2 ou E6.
- **PERTINENTE-COM-RESSALVA** — nenhum veto, mas ≥1 rebaixamento (E3 obiter, E6 erosão,
  E7 órgão divergente). A ressalva **tem que aparecer no dossiê**.
- **PERTINENTE** — passa limpo em todos os eixos; E5 define a posição no ranking.

## Regras de disciplina

- **Fato distintivo material vs. imaterial (E2):** só é material o fato que, se mudado,
  mudaria a *ratio*. Diferença de nome/valor/data que não move o fundamento é imaterial.
  Sempre explicite QUAL fato distingue e POR QUE é (ou não é) material — é o que o
  adversário vai usar.
- **Ratio (E3):** a *ratio* é o fundamento **necessário** ao dispositivo. Teste: se
  removê-lo, o resultado muda? Se não muda, é obiter.
- **Nunca infira vigência só pela data (E6):** confirme com a travessia de citações
  [estágio 5] e com informativos/legislação [estágio 8].

## Schema de saída por candidato (para os subagentes de grading)

Cada subagente que lê um inteiro teor devolve **exatamente** este objeto:

```json
{
  "processo": "0000000-00.0000.0.00.0000",
  "parent_id": "…",
  "orgao": "3ª TR-JFPE",
  "data": "AAAA-MM-DD",
  "tipo_doc": "acórdão|sentença|monocrática",
  "veredito": "PERTINENTE | PERTINENTE-COM-RESSALVA | DESCARTADO",
  "eixos": {
    "E1_tese":      {"ok": true,  "nota": "mesma controvérsia: superação de laudo parcial por condições pessoais"},
    "E2_fatos":     {"ok": true,  "nota": "idade+braçal+baixa escolaridade presentes", "fato_distintivo": "precedente tem 62a vs 58a do caso — imaterial"},
    "E3_ratio":     {"ok": true,  "nota": "é fundamento determinante do provimento", "obiter": false},
    "E4_direcao":   {"polaridade": "favoravel"},
    "E5_forca":     {"nivel": "turma", "vinculante": false},
    "E6_vigencia":  {"ok": true,  "nota": "sem superação; Tema 1300 não incorporado", "risco": "baixo"},
    "E7_aderencia": {"ok": true,  "nota": "mesmo órgão-alvo"}
  },
  "trecho_ancora": "«transcrição literal da ratio, verbatim do inteiro teor»",
  "pinpoint": "fls. X / item Y do voto",
  "fator_distintivo": "o que o adversário usaria para distinguir; vazio se nenhum relevante",
  "cluster_hint": "assinatura curta da tese p/ agrupamento no estágio [7]"
}
```

`trecho_ancora` é **copiado**, não parafraseado — é o que vai literal na minuta.
