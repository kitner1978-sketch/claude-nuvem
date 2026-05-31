# Verificação de Jurisprudência — Capítulo 15 (Auxílio-Acidente e Salário-Família)

Arquivo verificado: `D:\Projeto Livro\output\rascunhos\cap_15_rascunho.md`
Data da verificação: 2026-05-30
Bases consultadas: STJ (temas.csv / processos.csv), STF (temas_repercussao_geral_stf.xlsx), TNU (temas_representativos_tnu.csv)

Legenda do veredito: ✅ confere | 🚩 contradiz a base (erro) | ⚠️ impreciso / fora da base / atenção | ❓ não verificável na base

---

## Tabela de citações

| Citação (linha) | Tipo | Veredito | Dado oficial | Correção sugerida |
|---|---|---|---|---|
| Tema 862/STJ — data julgamento 22/06/2021 (l. 174 e l. 690) | Tema STJ | 🚩 | `dataJulgamento = 2021-06-09` (09/06/2021). Leading case REsp 1.729.555/SP, Rel. Min. Assusete Magalhães, S1 (1ª Seção). dataPublicacaoAcordao = 2021-07-01 | Trocar **22/06/2021 → 09/06/2021** (data de publicação usada/embaralhada como data de julgamento) |
| Tema 862/STJ — DJe 29/11/2021 (l. 690) | Tema STJ | ⚠️ | Acórdão publicado em 01/07/2021. 29/11/2021 é a data de publicação dos **embargos de declaração** (campo `dataPublicacaoEmbargosDeDeclaração`) | Conferir: o DJe do acórdão é 01/07/2021; 29/11/2021 refere-se aos EDcl. Ajustar para "DJe 01/07/2021" (ou esclarecer que 29/11 são os EDcl) |
| Tema 862/STJ — tese entre aspas (l. 174) | Tese STJ | 🚩 | Tese oficial: *"O termo inicial do auxílio-acidente deve recair no dia seguinte ao da cessação do auxílio-doença que lhe deu origem, conforme determina o art. 86, § 2º, da Lei 8.213/91, observando-se a prescrição quinquenal da Súmula 85/STJ."* | A citação entre aspas do livro diverge do texto oficial: "**O marco inicial**" → oficial "O termo inicial"; suprimiu "conforme determina o art. 86, § 2º, da Lei 8.213/91"; "**observada, em todo caso**" → oficial "observando-se". Corrigir para o texto literal |
| Tema 862/STJ — leading case REsp 1.729.555/SP (l. 20, 174, 690) | Processo STJ | ✅ | processos.csv: REsp 1729555, `leadingCase = S`, Rel. ASSUSETE MAGALHÃES, vinculado ao Tema 862, j. 2021-06-09 | OK |
| Tema 862/STJ — Rel. Min. Assusete Magalhães (l. 174, 690) | Relator | ✅ | ministroRelator = ASSUSETE MAGALHÃES | OK |
| Tema 862/STJ — Primeira Seção / 1ª Seção (l. 174, 452, 690) | Órgão | ✅ | orgaoJulgador = S1 (Primeira Seção) | OK |
| Tema 269/TNU (l. 86, 700) — PEDILEF 0031628-86.2017.4.02.5054/ES, j. 05/05/2022 | Tema TNU | ✅ | TNU 269: PEDILEF 0031628-86.2017.4.02.5054/ES; para acórdão Juiz Federal Ivanir César Ireno Júnior; julgado 05/05/2022 | OK (relator e data conferem) |
| Tema 269/TNU — tese entre aspas (l. 86) | Tese TNU | ⚠️ | Oficial: *"...para os fins do art. 86 da Lei 8.213/91 (auxílio-acidente), consiste em evento súbito e de origem traumática..."* | Substância idêntica. O livro grafou "art. 86 da Lei **n.** 8.213/**1991**" (inseriu "n." e ano por extenso dentro das aspas) e omitiu o parêntese "(auxílio-acidente)". Padronizar a transcrição literal |
| Tema 315/TNU (l. 176, 702) — PEDILEF 5063339-35.2020.4.04.7100/RS, j. 18/10/2023, Rel. Lilian Oliveira da Costa Tourinho | Tema TNU | ✅ | TNU 315: mesmo PEDILEF; para acórdão Juíza Federal Lilian Oliveira da Costa Tourinho; julgado 18/10/2023 | OK |
| Tema 322/TNU (l. 109, 208, 247, 704) — PEDILEF 5014634-54.2021.4.04.7202/SC, j. 22/11/2023, Rel. Luciana Ortiz Tavares Costa Zanoni | Tema TNU | ✅ | TNU 322: mesmo PEDILEF; Juíza Federal Luciana Ortiz Tavares Costa Zanoni; julgado 22/11/2023. Tese ressalva Súmula 507/STJ — coerente com l. 247 | OK |
| Tema 1246/STJ (l. 334) — "aferição da incapacidade é fático-probatória, insuscetível de reexame em REsp" | Tema STJ | ✅ | STJ Tema 1246, S1, j. 2024-11-13: tese declara inadmissível REsp para rediscutir preenchimento do requisito da incapacidade (existência/extensão/duração) em benefício por incapacidade, incluído auxílio-acidente. Leading case REsp 2.082.395, Rel. Paulo Sérgio Domingues | OK (livro não cita nº de processo; a paráfrase é fiel à tese) |
| Tema 350/STF — RE 631.240 (l. 328, 626) — prévio requerimento administrativo | Tema STF | ✅ | STF Tema 350: paradigma RE 631240, Rel. Min. Luís Roberto Barroso, j. 03/09/2014, mérito julgado. Tese trata de exigência de prévio requerimento | OK (atenção: **STJ** Tema 350 é matéria diversa — crédito educativo; o livro corretamente atribui o nº ao **STF**) |
| Súmula 44/STJ (l. 52, 66, 148, 273, 454, 692) | Súmula STJ | ⚠️ | Fora da base de temas/precedentes | Conferir manualmente. Texto e contexto (grau mínimo de disacusia) coerentes; aprovação em 1992 (l. 692) é informação histórica não verificável aqui |
| Súmula 507/STJ (l. 64, 221, 247, 416, 453, 694) | Súmula STJ | ⚠️ | Fora da base | Conferir manualmente. Aprovação informada como 26/03/2014 (l. 694). Conteúdo coerente com o regime de transição 11.11.1997 |
| Súmula 85/STJ (l. 174, 342, 444, 607, 622) | Súmula STJ | ⚠️ | Fora da base | Conferir manualmente (prescrição quinquenal) — consistente com as teses dos Temas 862/STJ e 315/TNU |
| Súmulas 15/STJ e 501/STF (l. 127, 264) | Súmula | ⚠️ | Fora da base | Conferir manualmente (competência da Justiça Estadual em acidentária) |
| Jur. em Teses STJ, ed. 198 (l. 52, 62, 225, 376, 458, 696) | Jur. Teses | ⚠️ | Fora da base de temas | Conferir manualmente. Publicação informada 08/09/2022 (l. 696) |
| Jur. em Teses STJ, ed. 199 (l. 52, 182, 187, 334, 444, 459, 698) | Jur. Teses | ⚠️ | Fora da base | Conferir manualmente. Publicação informada 16/09/2022 (l. 698) |
| RE 661.256 (não citado) / Tema 503 | — | — | (Não citado no capítulo — verificado só por precaução do erro recorrente; sem impacto) |

---

## Lista de correções concretas

1. **Linha 174** — `j. 22/06/2021` → **`j. 09/06/2021`**.
   Contexto: "...Tema 862 (REsp 1.729.555/SP, Primeira Seção, Rel. Min. Assusete Magalhães, j. 22/06/2021)". A base STJ traz `dataJulgamento = 2021-06-09`. (Erro recorrente confirmado: data de publicação/embargos usada como julgamento.)

2. **Linha 174** — corrigir a transcrição entre aspas da tese do Tema 862. De:
   `"O marco inicial do auxílio-acidente deve recair no dia seguinte ao da cessação do auxílio-doença que lhe deu origem, observada, em todo caso, a prescrição quinquenal prevista na Súmula 85/STJ."`
   Para (texto oficial):
   `"O termo inicial do auxílio-acidente deve recair no dia seguinte ao da cessação do auxílio-doença que lhe deu origem, conforme determina o art. 86, § 2º, da Lei 8.213/91, observando-se a prescrição quinquenal da Súmula 85/STJ."`

3. **Linha 690** — referência bibliográfica: `Julgado em 22/06/2021. DJe 29/11/2021` → **`Julgado em 09/06/2021. DJe 01/07/2021`** (a publicação de 29/11/2021 corresponde aos embargos de declaração, não ao acórdão; confirmar o DJe a adotar).

4. **(Opcional) Linha 86** — padronizar a transcrição literal da tese do Tema 269/TNU: o oficial diz "para os fins do art. 86 da Lei 8.213/91 (auxílio-acidente)"; o livro inseriu "n." e "1991" por extenso dentro das aspas e suprimiu "(auxílio-acidente)". Sem erro de conteúdo, apenas fidelidade da citação.

---

## Resumo

- **Total de citações analisadas:** 18 linhas/itens distintos
- ✅ Conferem: **8** (Temas 269, 315, 322/TNU; 1246, 350/STF e os atributos corretos do 862 — leading case, relator, órgão)
- 🚩 Erros (contradição com a base): **2** (data do Tema 862 = 09/06/2021, não 22/06; tese do Tema 862 transcrita com alterações dentro das aspas)
- ⚠️ Atenção / fora da base: **8** (DJe do Tema 862; transcrição do Tema 269; Súmulas 15/44/85/501/507; Jur. Teses 198/199 — conferir manualmente)
- ❓ Não verificável: **0**

### Erros críticos
1. **Tema 862/STJ julgado em 09/06/2021** (não 22/06/2021) — aparece em 2 locais (l. 174 e l. 690). Erro recorrente já mapeado.
2. **Tese do Tema 862 entre aspas diverge do texto oficial** (l. 174): "marco inicial" → "termo inicial"; supressão de "conforme determina o art. 86, § 2º, da Lei 8.213/91". Caso típico de "modernização" de termos dentro de aspas de tese oficial.

Nenhum Tema homônimo trocado entre tribunais; o livro corretamente atribuiu o Tema 350 ao STF (RE 631.240) — atenção que o Tema 350 do STJ trata de matéria diversa (crédito educativo). Temas 269/315/322 da TNU, 1246/350 conferem integralmente.
