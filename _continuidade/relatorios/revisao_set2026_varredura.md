# Revisão dirigida — setembro/2026

**Data:** 21/09/2026
**Texto examinado:** os 23 `cap_XX_rascunho.md` de `/Volumes/2tb/Projeto Livro/output/rascunhos/` (HEAD `0cb45ea`, 20/07/2026), que é o Markdown mais recente. **Os números de linha abaixo são desse repositório**, não da cópia do seagate.
**Ponto de partida:** os 21 comentários da revisora Ingrid Moura no DOCX de 18/09/2026, que só fez checagem jurídica até o cap. 5.
**Método:** duas varreduras por expressão regular nos 23 capítulos (A = regra superada; B = frase de bastidor), leitura de cada ocorrência em contexto e conferência dos pontos jurídicos em fonte (MCP `legislacao` — texto consolidado Planalto/normas.leg.br; MCP `informativos` e `jur-rag` — Informativos do STF).
**Atualização (21/09/2026, noite):** as propostas abaixo foram aplicadas ao Markdown do 2tb e o DOCX foi regenerado. O que foi feito, o que mudou em relação a este relatório e os achados novos estão em `revisao_set2026_aplicada.md`.

Legenda de verificação: ✅ conferido em fonte nesta sessão · ⚠️ não foi possível conferir (dizer por quê).

---

## Parte 1 — Achados críticos (erro de direito, conferidos em fonte)

### 1.1 Cronologia do art. 27-A está invertida — cap. 3, seções 3.8.3 e 3.8.4 ✅

É o achado mais grave. O livro afirma que a Lei 13.457/2017 manteve a carência **integral** e que a MP 871/2019 **introduziu a regra da metade**. O texto literal das normas diz o contrário:

| Norma | Texto conferido | O que o livro diz |
|---|---|---|
| MP 739, de 07/07/2016 | alterou o **parágrafo único do art. 27** (não criou o art. 27-A): "com os períodos previstos nos incisos I e III" (integral) | "introduziu pela primeira vez o art. 27-A"; vigência "18/07/2016 a 04/01/2017" |
| MP 767, de 06/01/2017 | **criou o art. 27-A** (integral) e **revogou o art. 24, parágrafo único** | correto quanto à carência integral; omite a revogação |
| Lei 13.457, de 26/06/2017 | art. 27-A: "com **metade** dos períodos previstos nos incisos I e III" | "manteve a exigência de carência integral" ❌ |
| MP 871, de 18/01/2019 | art. 27-A: "com os **períodos integrais** de carência previstos nos incisos I, III e IV" | "substituiu a carência integral pela regra da metade" ❌ |
| Lei 13.846, de 18/06/2019 | art. 27-A: "com **metade** dos períodos previstos nos incisos I, III e IV" | correto |

Consequência prática do erro: para DII entre 18/01/2019 e 17/06/2019 o livro manda aplicar 6 contribuições, quando a MP 871 exigia 12; para DII entre 27/06/2017 e 17/01/2019 manda aplicar 12, quando a Lei 13.457 exigia 6. Afeta diretamente a orientação "verificar qual regime estava vigente na DII".

Trechos a reescrever (cap. 3): linhas 276 (3.8.3, "A MP 871/2019… inseriu o art. 27-A na redação vigente"; "representou agravamento em relação à regra anterior"), 278 (atribuição a Porto, 2024, de que "a regra da metade foi introduzida pela MP 871/2019" — conferir na obra se o autor diz isso mesmo), 285 (box: lista das cinco alterações), 291–301 (itens *a* a *f*) e 303 (exemplos).

**Cronologia proposta para os itens (a)–(f):**

> (a) Até 07/07/2016: art. 24, parágrafo único — um terço da carência (4 contribuições nos benefícios por incapacidade).
> (b) MP 739/2016 (publicada em 08/07/2016; perdeu eficácia em 04/11/2016 sem conversão): deu nova redação ao parágrafo único do art. 27, exigindo carência integral.
> (c) De 05/11/2016 a 05/01/2017: com a perda de eficácia da MP 739, voltou a incidir o art. 24, parágrafo único (um terço).
> (d) MP 767/2017 (a partir de 06/01/2017): criou o art. 27-A com carência integral e revogou o art. 24, parágrafo único.
> (e) Lei 13.457/2017 (a partir de 27/06/2017): converteu a MP 767 com alteração — regra da **metade** (incisos I e III).
> (f) MP 871/2019 (18/01/2019 a 17/06/2019): voltou à carência **integral** e incluiu o auxílio-reclusão (inciso IV).
> (g) Lei 13.846/2019 (a partir de 18/06/2019): restabeleceu a **metade**, agora para os incisos I, III e IV. É a redação vigente.

⚠️ A data de perda de eficácia da MP 739 (04/11/2016, Ato Declaratório do Congresso) e a data de publicação (08/07/2016) não estão no acervo consultado; conferir no Planalto. O dia "18/07/2016" usado no livro não corresponde à MP (que é de 07/07/2016 ✅).

O exemplo de "fevereiro de 2017" (comentário #2 da Ingrid) se resolve junto: o intervalo em que voltou o um terço é **novembro/2016 a 05/01/2017**; o exemplo deve usar dezembro de 2016. E o exemplo seguinte da mesma linha ("dezembro de 2016, sob o regime da MP 739/2016") também cai, porque em dezembro a MP já não vigia.

Reflexos em outros capítulos:
- **cap. 7, linha 70** (7.3.3): "art. 27-A (introduzido pela Lei n. 13.846/2019)" → "acrescido pela MP 767/2017, convertida na Lei 13.457/2017, com redação da Lei 13.846/2019".
- **cap. 14, linha 292**: mesmo erro ("incluído pela Lei 13.846/2019") e chama a regra da metade de "regra de transição", o que ela não é; a frase "quando o segurado que não atingiu as 24 contribuições se filiar ao RGPS após a vigência…" descreve primeira filiação, hipótese em que a linha 298 do mesmo capítulo diz (corretamente) que a metade **não** se aplica. Contradição interna.
- **cap. 3, linha 318**: a "posição dos autores" invoca a "conjugação dos arts. 15, 24 (parágrafo único), 27-A e 102" — retirar o art. 24, p.ú., ou qualificá-lo como revogado.

### 1.2 Art. 24, parágrafo único, tratado como vigente — caps. 3 e 4 ✅

Texto consolidado da Lei 8.213: "Parágrafo único. (Revogado pela Medida Provisória nº 767, de 6/1/2017, convertida na Lei nº 13.457, de 26/6/2017)".

- **cap. 3, linhas 268–272** — a seção 3.8.2 inteira ("A regra geral do art. 24, parágrafo único") o apresenta no presente ("estabelece regra geral", "campo de aplicação residual… relativamente restrito"). Não há campo residual: o dispositivo não existe desde 06/01/2017. Proposta: renomear para "3.8.2 O regime anterior: o art. 24, parágrafo único (revogado)", pôr os verbos no passado e dizer que hoje a matéria é regida só pelo art. 27-A, restrito aos quatro benefícios que ele enumera.
- **cap. 4, linha 1137** (comentário #7 da Ingrid): "(art. 24, parágrafo único, Lei 8.213/91)" → "(art. 27-A da Lei 8.213/91; v. Cap. 3, seção 3.8)".

### 1.3 ~~Metadados da ADI 6.309~~ — ACHADO RETIRADO (erro meu de leitura)

Na primeira versão deste relatório afirmei que o Informativo STF 1220 registrava "relator Ministro Cristiano Zanin, julgamento virtual finalizado em 29.05.2026" para a ADI 6.309, em conflito com o livro. **Estava errado.** O trecho recuperado da base começa com vírgula: é o final do item *anterior* do Informativo, colado ao sumário em que a ADI 6.309 aparece. STF Notícias e IBDP (03/06/2026) confirmam o que o livro diz: conclusão em 03/06/2026, placar de 6×5, Min. Barroso como relator originário vencido quanto à idade mínima. **Nenhuma das 24 linhas foi alterada.** A memória do projeto *aposentadoria_especial* (19/07/2026) traz o mesmo engano e deve ser revista.

Alterou-se apenas a frase "a eventual modulação de efeitos será definida na publicação do acórdão" (5 ocorrências), reescrita como ressalva datada ("Até o fechamento desta edição, o acórdão não havia sido publicado…").

### 1.4 CEBAS: a seção 4.19 trata a Lei 12.101/2009 como vigente — cap. 4 ✅

A Ingrid marcou um ponto (#8); são cinco (linhas 35, 1256, 1284, 1286, 1297), e o problema é de fundo:

- O Decreto 11.791/2023, art. 1º ✅, "regulamenta a **Lei Complementar nº 187, de 16 de dezembro de 2021**, que dispõe sobre a certificação das entidades beneficentes e regula os procedimentos referentes à imunidade de contribuições à seguridade social de que trata o § 7º do art. 195". A certificação hoje é regida pela LC 187/2021, não pela Lei 12.101/2009.
- **Linha 1284** afirma que "o STF admitiu que a Lei 12.101/2009 (lei ordinária) é constitucional na medida em que regulamenta requisitos já previstos no art. 14 do CTN". A tese do **Tema 32** (RE 566.622, ED julgados em 18–19/12/2019, Informativo 964 ✅) é outra: "A lei complementar é forma exigível para a definição do modo beneficente de atuação das entidades de assistência social contempladas pelo art. 195, § 7º, da CF, especialmente no que se refere à instituição de contrapartidas a serem por elas observadas" — com a ressalva de que aspectos **procedimentais** (certificação, fiscalização, controle) cabem em lei ordinária. Foi justamente isso que levou à edição da LC 187/2021.
- **Linha 1286** conclui que "os requisitos do art. 14 do CTN e da Lei 12.101/2009 são os parâmetros vigentes" — desatualizado.
- Os percentuais da linha 1260 (20% de bolsas; 60% ao SUS) eram os da Lei 12.101. ⚠️ Não conferi os da LC 187; precisam ser relidos na lei antes de reescrever.

Proposta: reescrever 4.19.1, 4.19.2 e 4.19.4 tendo a LC 187/2021 como lei de regência, a Lei 12.101 como antecedente histórico e o Tema 32 com a tese literal. É reescrita de seção, não ajuste pontual.

---

## Parte 2 — Resíduos de regra superada em menções laterais

Os capítulos-sede estão atualizados; o resíduo está onde o tema aparece de passagem.

| Cap.:linha | Trecho | Problema | Proposta |
|---|---|---|---|
| 05:744 | "insuficiente para aposentadoria especial (exige 25 anos + idade)" | contradiz as linhas 725 e 732 do mesmo capítulo (ADI 6.309) — comentário #15 | "(exige 25 anos de efetiva exposição)" |
| 11:717 | "auxílio por incapacidade temporária… ou aposentadoria por incapacidade **temporária**" | lapso — comentário #17 | "aposentadoria por incapacidade **permanente**" |
| 04:1101(a) | "o art. 15, **II**… mantém a qualidade de segurado de quem está em gozo de benefício" | é o inciso **I** ✅ ("sem limite de prazo, quem está em gozo de benefício, exceto do auxílio-acidente") — comentário #5 | trocar para "art. 15, I"; acrescentar a ressalva do auxílio-acidente, que o trecho omite |
| 04:1625 | box "Cooperativa de fachada": "contratam cooperativa (15% sobre NF)" | descreve como prática atual uma contribuição que o próprio capítulo (l. 165, 1608, 1613) diz inconstitucional (Tema 166, RE 595.838) — comentário #10 | reescrever o incentivo da fraude sem a alíquota: "para afastar a contribuição patronal de 20% + RAT e os encargos trabalhistas" |
| 03:272 e 3.8.3 | art. 27-A "para benefícios por incapacidade, **salário-maternidade** e auxílio-reclusão" | a carência do salário-maternidade caiu nas ADIs 2.110/2.111 (o art. 25, III, consolidado já traz "Vide ADIs" ✅) — comentário #1 | adotar a redação sugerida pela Ingrid, remetendo à seção 3.3.5 |
| 08:37 | "As alterações abrangeram: (a) a introdução de requisito de idade mínima (55, 58 ou 60…)" | é narrativa histórica, mas está a 18 linhas do aviso da linha 19 e sem ressalva própria | acrescentar "(requisito depois declarado inconstitucional, v. 8.4.1)" |

Sem problema (conferidos e corretos): cap. 3, linhas 29, 49, 120 e cap. 13, linha 126 (carência do salário-maternidade, todos já no passado); cap. 4, linhas 165, 1608–1615 (cooperativas); cap. 5, linhas 725, 732; cap. 8, linhas 19, 92, 532; cap. 12, linha 1050; cap. 9 (Tema 642 — "idade mínima" ali é a da aposentadoria rural); cap. 11, linha 118 (EC 20/98).

---

## Parte 3 — Frases de bastidor no corpo do texto

Flags do pipeline ou recados de pesquisa que vazaram para o leitor. Remover ou converter.

| Cap.:linha | Trecho | Ação |
|---|---|---|
| 01:31 | "(nota: a EC 136/2025 foi promulgada durante a elaboração desta obra; recomenda-se a verificação da redação final…)" | remover (a Ingrid já removeu no DOCX) |
| 01:367 | "(cuja redação final deve ser conferida no Diário Oficial da União, dado que a emenda foi promulgada durante a elaboração desta obra)" | remover — **conferir o texto da EC 136 e fechar** |
| 01:372 | título de box: "*(nota: verificar redação final no DOU)*" | remover (persiste no DOCX de 18/09) |
| 01:463 | referência: "(Verificar redação final publicada no DOU.)" | substituir pela referência ABNT completa da EC 136/2025 |
| 04:284 | "Verificar vigência atualizada antes da publicação." | remover — conferir o cronograma da Lei 14.973/2024 (#4) |
| 04:1101 | "(tema sobre o qual se deve consultar a posição atualizada antes do ajuizamento)" | substituir pelo precedente: a frase fala em "entendimento consolidado" sem citar nenhum (#6) |
| 05:711 · 08:88 · 08:92 · 08:665 · 11:813 | "A eventual modulação de efeitos será definida na publicação do acórdão" (e, em 08:88, "o acórdão ainda será redigido…") | cinco ocorrências da mesma frase; resolver de uma vez após conferir o acórdão (#14) — ver 1.3 |
| 17:579 | "[verificar a taxa vigente na data de leitura]" entre colchetes | remover os colchetes; se quiser manter o aviso, integrá-lo à frase |
| 18:153 | "[Nota: valor projetado para 2026 com base na política de valorização… Verificar o salá…" | o salário mínimo de 2026 já é dado certo; remover a nota |
| 06:5 · 07:5 | frontmatter `status: rascunho` | inofensivo se o gerador ignora o YAML; uniformizar com os demais |

Avisos ao leitor que **podem ficar** (são conselho legítimo, não bastidor): 14:72 (BEPS como ordem de grandeza), 18:432 (conferir redação atualizada da LOAS), 23:326 (superpreferência), 12:513 e 12:1299 (projetos de lei sobre a LC 142), e todos os "o advogado deve verificar…" de checklists (caps. 1, 4, 5, 10, 11, 17, 19, 21, 23).

---

## Parte 4 — Pendências que dependem de conferência externa

| Cap.:linha | Afirmação no livro | Situação |
|---|---|---|
| 02:181 · 19:173 · 19:176 | Tema 1.271/STF (menor sob guarda, RE 1.442.021) "permanece pendente de julgamento" | ⚠️ o tema não retornou no acervo de informativos; conferir no portal do STF |
| 17:147 | modulação da "vida toda" "pendente de julgamento em plenário físico" | ⚠️ não conferido |
| 17:797 | ADI 7.873 (EC 136/2025) "Pendente de julgamento (junho/2026)" | ⚠️ não conferido; se mantiver, a data de corte do livro já cobre a ressalva |
| 04:1256 ss. | percentuais de gratuidade do CEBAS | ⚠️ reler na LC 187/2021 |
| 03:278 | atribuição a Porto (2024) sobre a origem da regra da metade | ⚠️ conferir na obra; se o autor disser isso, registrar a divergência em vez de repetir o erro |

---

## Parte 5 — Comentários da Ingrid: situação de cada um

| # | Cap. | Procede? | Onde está tratado |
|---|---|---|---|
| 1 | 3 | sim ✅ | Parte 2 |
| 2 | 3 | sim ✅ (e o problema é maior) | 1.1 |
| 3 | 3 | sim — pensão por morte não tem carência; adotar a redação dela | — |
| 4 | 4 | sim | Parte 3 |
| 5 | 4 | sim ✅ | Parte 2 |
| 6 | 4 | sim | Parte 3 |
| 7 | 4 | sim ✅ (dispositivo revogado) | 1.2 |
| 8 | 4 | sim ✅ (e o problema é maior) | 1.4 |
| 9 | 4 | sim — o art. 150, VI, *c*, é imunidade de impostos; o parágrafo chama de "isenção" e mistura os regimes. O STF (Informativo 964 ✅) registra que o "são isentas" do art. 195, § 7º, tem natureza de imunidade | reescrever junto com 1.4 |
| 10 | 4 | sim | Parte 2 |
| 11 | 5 | ⚠️ não analisado a fundo — exige ler 5.x sobre rural pré e pós-1991 | — |
| 12 | 5 | provável — o Tema 216/TNU, como o próprio 5.6.2 o descreve, não exige vínculo empregatício | harmonizar com 5.6.2 |
| 13 | 5 | sim — a frase não diz qual circunstância; ou especifica, ou fica só "Justiça Estadual" | — |
| 14 | 5 | sim | Parte 3 / 1.3 |
| 15 | 5 | sim | Parte 2 |
| 16 | 6 | sim — frase entre aspas sem fonte: ou cita, ou tira as aspas | — |
| 17 | 11 | sim | Parte 2 |
| 18 | 13 | sim — duplicidade no quadro | — |
| 19–21 | 15 | defeito do gerador: `[!warning]`/`[!tip]` saindo como texto (4 ocorrências, todas no cap. 15) | corrigir em `md_to_docx.py`, não no Word |

---

## Resumo por capítulo

| Cap. | Crítico | Resíduo | Bastidor | Observação |
|---|---|---|---|---|
| 1 | ADI 6.309 (3) | — | 4 | EC 136/2025 nunca foi "fechada" |
| 3 | **27-A invertido; art. 24 p.ú.** | 1 | — | reescrever 3.8.2 a 3.8.4 |
| 4 | **CEBAS/LC 187**; art. 24 p.ú. | 3 | 2 | capítulo com mais pontos |
| 5 | ADI 6.309 (6) | 1 | 1 | |
| 7 | — | origem do 27-A | — | |
| 8 | ADI 6.309 (9) | 1 | 3 | capítulo-sede; concentra a narrativa do julgamento |
| 11 | ADI 6.309 (4) | 1 | 1 | |
| 12 | ADI 6.309 (1) | — | — | |
| 14 | — | 27-A (origem + contradição interna) | — | |
| 17 | — | — | 1 | 2 pendências a conferir |
| 18 | — | — | 1 | seção 18.13 (ver `revisao_set2026_aplicada.md`: o erro era o título e a citação do Tema 185, não a palavra "absoluta") e genro/nora |
| 2, 19 | — | — | — | Tema 1.271 "pendente" (02:181, 19:173, 19:176) a conferir |
| 23 | ADI 6.309 (1) | — | — | |
| 6, 9, 10, 13, 15, 16, 20, 21, 22 | nada nestas duas varreduras | | | |

**Limite desta revisão:** as varreduras procuram famílias de erro conhecidas. O achado 1.1 (cronologia invertida) **não** foi encontrado pela varredura — apareceu porque conferi um comentário da Ingrid contra o texto da lei. Isso indica que a checagem de jurisprudência de maio (v13) não teve equivalente para **legislação**: nenhuma etapa do pipeline comparou a narrativa legislativa do livro com o texto consolidado das normas. É a lacuna que recomendo fechar antes da publicação.
