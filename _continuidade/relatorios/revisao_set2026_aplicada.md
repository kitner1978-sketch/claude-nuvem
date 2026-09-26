# Revisão fina de 21/09/2026 — o que foi aplicado

**Onde:** Markdown de `/Volumes/2tb/Projeto Livro/output/rascunhos/` (23 capítulos) e scripts `md_to_docx.py` e `gerar_livro_pdf.py`. **Nada foi commitado**: as alterações estão na árvore de trabalho do 2tb (`git diff` mostra tudo; `git checkout -- output/rascunhos scripts` desfaz).
**Resultado:** `output/livro_completo - 21 de set 26.docx` (2tb), com cópia na raiz de `/Volumes/seagate/Projeto Livro/`. 23 capítulos, ~383 mil palavras, abre sem erro. PDF não foi gerado.
**Fontes de conferência:** legislação consolidada (MCP `legislacao`), Informativos STF/STJ, base `jur-rag` (enunciados oficiais de súmulas), bases oficiais baixadas pelo projeto em `jurisprudencia/` (Temas STJ, STF e TNU), publicação oficial da Câmara (LC 187/2021) e Ato Declaratório do Congresso (MP 739).

---

## 1. Correções de direito (todas conferidas em fonte)

### Legislação
| Cap. | O que estava errado | Correção |
|---|---|---|
| 3 (3.8.2–3.8.4), 7, 14 | Cronologia do art. 27-A **invertida**: dizia que a Lei 13.457/2017 manteve carência integral e que a MP 871/2019 criou a regra da metade | Reescrita: MP 739 (art. 27, p.ú., integral, eficácia até 04/11/2016) → intervalo com o art. 24 p.ú. → MP 767 (cria o 27-A, integral) → **Lei 13.457 = metade** → **MP 871 = integral** → Lei 13.846 = metade. Exemplos refeitos. Incluído o **Tema 176/TNU**, que o livro não citava |
| 3, 4 | Art. 24, parágrafo único, tratado como "regra geral" vigente | Revogado desde 06/01/2017; seção 3.8.2 passou a tratá-lo como regime anterior |
| 4 (4.19) | CEBAS regido pela Lei 12.101/2009 | **LC 187/2021** (revogou a Lei 12.101, art. 47, II): validade de 3 anos (art. 36), 1 bolsa integral para cada 5 pagantes (art. 20), 60% ao SUS (art. 9º, II), retroação do cancelamento (art. 38, § 6º). Box do **Tema 32/STF** com a tese na redação dos embargos |
| 4 | art. 15, **II** (gozo de benefício) | art. 15, **I**, com a ressalva do auxílio-acidente |
| 4 | "isenção" do art. 150, VI, *c* | imunidade de impostos (art. 150, VI, *b* e *c*) × imunidade de contribuições (art. 195, § 7º) × isenção legal |
| 4 | box de cooperativas citava "15% sobre NF" como prática | retirada a alíquota (inconstitucional, Tema 166/STF) |
| 1, 17 | EC 136/2025 com quatro notas "verificar no DOU" | EC 136, de 09/09/2025, conferida (art. 3º: IPCA + juros simples de 2% a.a., limitado à Selic); notas removidas |

### Súmulas
| Cap. | O que estava errado | Correção |
|---|---|---|
| **4 e 5 (7 pontos)** | **"Súmula 74 da TNU" inventada** — transcrita entre aspas com dois textos diferentes sobre atividade rural sem recolhimento. A Súmula 74 verdadeira trata de **prescrição** | Substituída pela **Súmula 24/TNU** (rural *anterior* à Lei 8.213, sem recolhimento, exceto carência) e pela **Súmula 272/STJ** (pós-1991: só com contribuição facultativa). O texto anterior afirmava o contrário do direito vigente |
| 5, 2 | Súmula 75/TNU entre aspas com texto que não é o literal; descrita no cap. 2 como prova de "salários de contribuição" | Texto literal restaurado |
| 8 | Súmula 32/TNU cancelada "em abril de 2014" | 09/10/2013 |

### Temas (teses entre aspas que não eram a tese)
| Cap. | Tema | Problema |
|---|---|---|
| 18 (18.13) | **185/STJ** | Título dizia "presunção relativa" e a "citação literal" terminava em "presunção objetiva e relativa". A tese oficial diz **"presume-se absolutamente"**. Corrigido, e incluído o **Tema 122/TNU** (presunção *relativa*), com a divergência explicada — é ela que interessa nos JEFs. **Retifico o que eu disse antes:** as linhas do capítulo que falavam em "absoluta" estavam certas |
| 18 | 217/TNU, 27/STF | paráfrases entre aspas → texto literal |
| 18 | genro/nora | o texto admitia incluí-los no grupo familiar; reescrito com o rol do art. 20, § 1º, e o Tema 73/TNU |
| 21 (21.16) | **629/STJ** | atribuía ao STJ uma tese sobre nova ação em benefício por incapacidade e uma definição de "prova nova" entre aspas. A tese é sobre extinção sem mérito por falta de prova (caso rural). Reescrito como **extensão doutrinária** do precedente, que é o que de fato é |
| 21 | 966/STJ | "prazo decadencial de dez anos estabelecido no art. 103" → literal |
| 9 | 532/STJ (2×), 642/STJ | tese inexistente entre aspas ("atividade urbana intercalada") → literal |
| 4 | 350/STF | paráfrase como "Tese" → item I literal + remissão |
| 5, 6 | 1.007/STJ, 982/STJ | paráfrases → literal |
| 22 | 1.157/STJ | "tese" entre aspas, mas o acórdão não estava publicado (base oficial de maio/2026) → descrita sem aspas, com a ressalva |

### Coerência interna
- cap. 5: "25 anos + idade" → "25 anos de efetiva exposição"; aluno-aprendiz sem "vínculo empregatício" (harmonizado com 5.6.2); competência na recusa de CTC por RPPS especificada.
- cap. 11: "aposentadoria por incapacidade temporária" → permanente.
- cap. 3: pensão por morte "com cômputo integral da carência" → redação da revisora.
- cap. 8: idade mínima 55/58/60 com ressalva da ADI 6.309.

## 2. O que NÃO mudou (e por quê)
- **ADI 6.309** — os dados do livro estão corretos; o erro era meu (ver `revisao_set2026_varredura.md`, item 1.3).
- Tema 1.271/STF (menor sob guarda), modulação da "vida toda" e ADI 7.873: continuam como "pendentes". Não consegui confirmar o estado atual.
- Comentários da revisora nº 16 (citação sem fonte) e 19–21 (`[!warning]`): eram defeito do gerador, resolvidos na seção 4. Nº 18 (duplicidade no quadro do cap. 13): não mexido.

## 3. Edições da revisora Ingrid Moura incorporadas ao Markdown
- **360 edições de texto** transportadas do DOCX de 18/09 para o fonte.
- **"salário-mínimo" com hífen** adotado em todo o livro (353 ocorrências), porque ela o aplicou em 87% dos casos; **preservada a grafia original dentro de citações literais**. Reversível com uma substituição global, se o autor preferir a grafia da lei.
- **Acentuação do cap. 10** restaurada por completo (72 palavras + 5 casos de "é/está" conferidos à mão). Varredura no livro inteiro: zero remanescentes.
- 124 edições não transportadas: quase todas eram consertos manuais de defeitos do gerador, agora resolvidos na origem. Exceção que fica para decisão: ela **renumerou** Introdução e Conclusão ("1.1", "3.9"…), o que contraria a desnumeração feita em julho a pedido da Thoth. Mantive sem número.

## 4. Correções no gerador
| Defeito no DOCX | Causa | Correção |
|---|---|---|
| Listas saindo "1. 1. 1." (26 casos) | itens separados por linha em branco viravam blocos de um item | o número agora vem do Markdown (nos dois scripts, que tinham o laço duplicado) |
| "Observam que…", ", e Castro e Lazzari (2025)," | `strip_citations` removia o autor e deixava o verbo, e não entendia listas de autores | ou remove a oração inteira, ou não remove nada |
| **Citações literais sem fonte** | o mesmo script apagava a atribuição de trechos entre aspas | atribuição é preservada sempre que houver aspas no período (60 casos) |
| `[!warning]` como texto (cap. 15) | callout Obsidian sem tratamento | marcador vira título em negrito |
| "---" como texto | linha horizontal do Markdown | ignorada |
| "tema", "lei", "súmula" minúsculos em 61 títulos | regra de título da Thoth aplicada a nomes próprios | 25 títulos corrigidos no fonte (os demais vieram com as edições da revisora) |

## 5. Conferência do DOCX novo
| Verificação | jul/19 | 18/09 (revisora) | **21/09** |
|---|---|---|---|
| marcador `[!tipo]` literal | 4 | 4 | **0** |
| verbo órfão | 14 | 8 | **0** |
| nota de bastidor | 7 | 6 | **0** |
| palavra sem acento | 101 | 3 | **0** |
| "Súmula 74" (inexistente) | 7 | 7 | **0** |
| presunção "relativa" atribuída ao STJ | 3 | 5 | **0** |
| título com tema/lei em minúscula | 61 | 30 | **0** |
| lista "1." repetida | 26 | 0 | **0** |

## 6. Um incidente, para registro
Minha ferramenta de transporte das edições tinha um erro que **truncou os caps. 2, 6 e 7**. Percebi pelo `git diff` (1.961 linhas removidas), restaurei de um backup que havia feito minutos antes, corrigi a ferramenta e passei a verificar o tamanho de cada arquivo após cada etapa. O estado final foi conferido capítulo a capítulo contra o HEAD: só os caps. 3 e 18 mudaram de tamanho, pelas linhas que acrescentei.

## 7. O que esta revisão indica sobre o resto
Dois padrões de erro que **nenhuma etapa do pipeline cobria**:
1. **Narrativa legislativa** (quem incluiu, quem revogou, qual redação vigorou quando) — achei no art. 27-A e no CEBAS só porque conferi contra o texto da lei.
2. **Texto entre aspas que não é literal** — 1 súmula inventada, 2 súmulas e 11 teses parafraseadas. A verificação de maio (v13) conferiu número, relator e data dos Temas, mas não o teor entre aspas, e não cobriu súmulas.

O conferidor automático que usei só alcança aspas na mesma linha do número do tema: conferiu 69 citações de tese. **Correção (24/09):** das súmulas, 36 com texto entre aspas foram apenas *inventariadas* (`sumulas_citadas.json`); o texto de só seis foi conferido contra o enunciado oficial (TNU 24, 32, 47, 74 e 75; STJ 272). Em 24/09 a Súmula 577/STJ apareceu truncada no cap. 9. **Citações literais de lei e de doutrina não foram conferidas.** Recomendo esse passe antes da publicação, junto com a conferência do acórdão da ADI 6.309 e do Tema 1.157/STJ.

---

## 8. Sessão de 22/09/2026 — conferência de legislação (PAUSADA por módulos)

**Método:** 807 frases com afirmações sobre legislação foram extraídas dos 23 capítulos (`revisao_set2026_legislacao/cap_XX.txt`) e conferidas por 8 agentes contra o texto consolidado (Planalto), com a regra de só apontar divergência demonstrada por texto literal (`INSTRUCOES.md`). Os agentes foram interrompidos para poupar cota: **13 capítulos conferidos** (1, 2, 4, 6, 7, 9, 12, 13, 15, 16, 18, 20, 21); **10 não conferidos** (3, 5, 8, 10, 11, 14, 17, 19, 22, 23). Relatórios em `revisao_set2026_legislacao/achados_g1..g8.md`: 115 divergências (11 ALTA, 62 MÉDIA, 42 BAIXA).

### Módulo 1 — CONCLUÍDO: as 11 divergências ALTA (todas reconferidas na fonte e aplicadas)
| Cap. | Erro | Correção |
|---|---|---|
| 4 | Cronograma da reoneração (Lei 14.973/2024) deslocado um ano e com proporções erradas | Tabela e box refeitos pelo art. 9º-A da Lei 12.546/2011: 2025 80%/25%, 2026 60%/50%, 2027 40%/75%, 2028 extinção |
| 4 | Arts. 45 e 46 da Lei 8.212 citados como vigentes (prazos de 5 anos) | Revogados pela LC 128/2008 após a SV 8; prazos são os dos arts. 173 e 174 do CTN (títulos 4.18.2/4.18.3 e 3 parágrafos) |
| 12 | "Lacuna" do art. 40, § 4º-A, para servidor com deficiência | Art. 22 da EC 103/2019 manda aplicar a LC 142 ao servidor federal (10 anos de serviço + 5 no cargo) |
| 13 | Pai biológico "só tem licença de 5/20 dias" | Lei 15.371/2026 instituiu o salário-paternidade (10/15/20 dias, de 2027 a 2029); projeto de "salário-parentalidade" descrito como se pendente |
| 13 | Demora administrativa no salário-maternidade | Lei 15.415/2026: prazo de 30 dias, concessão provisória automática, irrepetibilidade salvo má-fé |
| 15 | Auxílio-acidente + pensão por morte "sujeita às faixas do art. 24" | O § 1º do art. 24 é taxativo (pensão/pensão, pensão/aposentadoria, pensão militar/aposentadoria); acumulação integral (3 pontos + quadro 15.3) |
| 18 | LOAS art. 20, § 3º citado como "inferior a 1/4" | Redação vigente (Lei 14.176/2021): "igual ou inferior" |
| 18 | Art. 20, § 14, com "incisos I a VI" | O § 14 tem comando único; o rol está no Decreto 6.214/2007, art. 4º, § 2º. Corrigida contradição interna sobre Bolsa Família (Decreto 12.534/2025) |
| 18 | Auxílio-inclusão: "renda per capita até 2 SM (art. 26, II)" | É a remuneração do próprio beneficiário (art. 26-A, I, "a"); renda per capita segue o critério do BPC (art. 26-A, IV e § 4º) |
| 20 | "§ 3º do art. 24" excepciona pensão acidentária do redutor | **Inexistente.** O § 3º trata de revisão a pedido. Seção 20.6.1 reescrita |
| 20 | "§ 6º do art. 24" protege policiais mortos em serviço | **Inexistente** (o art. 24 vai até o § 5º). A proteção é o art. 40, § 7º, CF, dirigido à lei do ente. Seção 20.6.2 reescrita; 20.6.3 renumerada para 20.6.2 |

Também nesta sessão: Tema 251/TNU restaurado ao literal (cap. 3); 4 precedentes avulsos inexistentes substituídos por fontes verificadas (caps. 4 e 14); Epílogo do cap. 23 corrigido e promovido a seção própria; cap. 22 recuperou o título "Referências"; exemplo do cap. 15 ajustado ao SM de 2026; validadores: 194 remissões internas válidas.

**Entregável:** `livro_completo - 22 de set 26.docx` (2tb e raiz do seagate). 23 capítulos, ~383 mil palavras, abre sem erro. Sem PDF.

### Módulos PENDENTES (para retomar)
2. As 62 MÉDIA e 42 BAIXA dos 13 capítulos conferidos (ler `achados_g*.md`; muitas são datas/números de dispositivo).
3. Conferência dos 10 capítulos restantes (3, 5, 8, 10, 11, 14, 17, 19, 22, 23) — sugestão: 2 agentes por vez, com gravação incremental.
4. DOCX final + PDF + relatório para a editora.
5. **Commit no 2tb** — nada foi commitado; `git diff` mostra tudo.
