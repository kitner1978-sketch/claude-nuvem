# Revisão fina de 26/09/2026: achados globais (transversais aos capítulos)

Fonte lida: `output/rascunhos/cap_01..23_rascunho.md` (384.096 palavras). Retrato prévio dos 23 arquivos em `_continuidade/snapshots/rascunhos_pre_revisao_fina_26set/`. Os achados por capítulo estão em `cap_NN.md` nesta pasta (listas A a G). Este arquivo reúne o que atravessa capítulos e o que foi conferido em fonte primária (jur-rag) pelo revisor-coordenador, e não pelos revisores de capítulo.

## 1. Referências de doutrina: a mesma obra com edições, cidades e anos diferentes

O gerador (`gerar_livro_pdf.py`, `add_consolidated_references`) só funde entradas idênticas (ignora asteriscos e espaços). Como os capítulos citam a mesma obra de formas diferentes, a lista consolidada da editora sairá com a mesma obra repetida 3 a 6 vezes. Levantamento (143 entradas brutas de doutrina viram 43 na lista final, para cerca de 25 obras distintas):

| Obra | Formas encontradas (capítulos) | Decisão necessária |
|---|---|---|
| IBRAHIM, Curso de Direito Previdenciário | 28. ed. Niterói 2025, com BRAGANÇA e FOLMANN (caps. 1-8); 27. ed. Rio de Janeiro 2024 (cap. 9); 27. ed. Niterói 2025 (caps. 10-15); 28. ed. Rio de Janeiro 2025 (caps. 16-20, 23); 28. ed. Niterói 2025 (caps. 21-22) | Uma única entrada. O corpo cita "Ibrahim (2025)" na maior parte e "Ibrahim; Bragança; Folmann (2025)" no cap. 1. Definir autoria e edição efetivamente consultadas |
| HORVATH JÚNIOR, Direito Previdenciário | 13. ed. Quartier Latin 2024 (caps. 2, 9); 13. ed. Rideel 2022 (cap. 7); 14. ed. Quartier Latin 2022 (cap. 15); 14. ed. Quartier Latin 2025 (caps. 1, 6, 18-20, 23); 14. ed. Rideel 2025 (caps. 3, 16); 15. ed. Rideel 2025 (cap. 8) | Uma única entrada (editora, edição e ano corretos) |
| SANTOS, Marisa; CALEJON | "CALEJON, Rodrigo", SaraivaJur, 15. ed. (caps. 2, 3, 6-8); "CALEJON, Celia", Saraiva, 15. ed. (caps. 4-5); "CALEJON, Celia/Célia", 16. ed. (caps. 20-21); só SANTOS, 15. ed. (caps. 9, 15, 18, 19, 23) | Conferir o nome do coautor (Celia × Rodrigo) e unificar edição |
| SAVARIS, Direito Processual Previdenciário | 11. ed. 2023 (maioria); 10. ed. 2023 (cap. 12); 9. ed. 2023 (cap. 21) | Unificar (11. ed.) |
| PORTO, Rafael, Manual de Direito Previdenciário | 2. ed. 2024 "Editora JusPodivm" (caps. 2-4, 6-7); 2. ed. 2024 "JusPodivm" (cap. 5); 3. ed. 2025 (cap. 8) | Unificar |
| CASTRO; LAZZARI, Manual | "Rio de Janeiro: Forense" (21 caps.) × "São Paulo: Forense" (caps. 19, 23); cap. 17 inverte a ordem dos autores ("LAZZARI; CASTRO") | Padronizar "Rio de Janeiro" e a ordem CASTRO; LAZZARI |
| KERTZMAN; AMADO; SAVARIS (Fundamentos); demais | Variam só em negrito/itálico e ponto dentro/fora do negrito | O gerador já funde |

Também: `verificar_citacoes_refs` acusa 32 citações sem entrada no próprio capítulo (Ibrahim 2025, Kertzman 2025, Savaris 2023, Santos 2025, Amado 2025 nos caps. 15, 19-23). Como a lista final é consolidada, o efeito é nulo desde que a obra apareça em algum capítulo; hoje aparece. Na jurisprudência, 3 pares quase idênticos escapam da fusão por pontuação (Tema 350/STF, Súmula 85/STJ, Tema 253/TNU: travessão × vírgula, com e sem ponto final).

Sugestão operacional: escolher a forma canônica de cada obra e aplicar nos 23 capítulos com `patchlib.py` (é substituição exata), ou ensinar o gerador a fundir por autor + título.

## 2. Súmulas citadas entre aspas: conferência contra o enunciado oficial (jur-rag)

61 citações de súmula entre aspas nos 23 capítulos; 28 enunciados distintos puxados de `precedente:STJ|TNU|STF:SUM:N` (arquivo `_sumulas_oficiais_jurrag.json`). Resultado: 37 batem; TNU 24, 47, 75 e STJ 272 já haviam sido conferidas em 21/09; TCU 96 (aluno-aprendiz, cap. 5 l. 377) não está na base.

Divergências reais:

| Cap./linha | Súmula | Problema | Correção |
|---|---|---|---|
| 19:185 | TNU 63 | Cita a redação ANTIGA como vigente. A TNU alterou o enunciado em 18/09/2025 | Enunciado atual: "Para os fatos geradores ocorridos até a entrada em vigor da MP nº 871/2019, a comprovação de união estável para efeito de concessão de pensão por morte prescinde de início de prova material." Mencionar a alteração de 18/09/2025. O restante do capítulo (l. 112, 192, 631, 655) e o cap. 2 (l. 168) já aplicam a súmula só aos óbitos anteriores à MP 871, o que é compatível |
| 6:38, 6:124, 7:400 | TNU 53 | Texto "modernizado" dentro das aspas ("auxílio por incapacidade temporária ... aposentadoria por incapacidade permanente") | Oficial: "Não há direito a auxílio-doença ou a aposentadoria por invalidez quando a incapacidade para o trabalho é preexistente ao reingresso do segurado no Regime Geral de Previdência Social." Nomenclatura atual fora das aspas |
| 3:110, 3:162 | TNU 53 e 73 | Parênteses "(atual ...)" inseridos dentro das aspas | Usar colchetes [atual ...] ou tirar das aspas |
| 15:221 | STJ 507 | O texto entre aspas não é o enunciado (é paráfrase com menção à MP 1.596-14/97) | Oficial: "A acumulação de auxílio-acidente com aposentadoria pressupõe que a lesão incapacitante e a aposentadoria sejam anteriores a 11/11/1997, observado o critério do art. 23 da Lei n. 8.213/1991 para definição do momento da lesão nos casos de doença profissional ou do trabalho." |
| 20:422 | STJ 507 | "e a concessão da aposentadoria" (oficial: "e a aposentadoria"); "Lei 8.213/1991" (oficial: "Lei n. 8.213/1991") | Ajustar às palavras oficiais |
| 9:176, 9:179, 9:354 | STJ 577 | Truncada, sem "colhida sob o contraditório" (já conhecida) | Completar |
| 18:102 | TNU 29 | "mas também a que impossibilita" (oficial: "mas também a impossibilita") | Ajustar |
| 2:206 | TNU 4 | "se deu após" (oficial: "deu-se após") | Ajustar |
| 23:301 | TNU 53 e 77 | Descrições entre parênteses erradas: 53 é incapacidade preexistente ao reingresso (não "condições pessoais"); 77 é dispensa da análise das condições pessoais quando não há incapacidade (não "incapacidade e deficiência") | Corrigir as descrições |

## 3. Revisão da vida toda (Tema 1.102/STF): box do cap. 16 diverge do Informativo STF 1200

Conferido no Informativo STF 1200 (03/12/2025), item "Impossibilidade de o segurado do INSS optar pela regra mais favorável ... RE 1.276.977/DF":

- Processo: RE 1.276.977/**DF** (o box do cap. 16, l. 486, diz "/RS"; o cap. 10, l. 608, diz "/DF").
- Relator Min. Marco Aurélio, redator do acórdão Min. Alexandre de Moraes; julgamento (dos embargos) finalizado em **25/11/2025**, sessão virtual. O box diz "Min. Nunes Marques (embargos)" e "26/11/2025" (o cap. 16, l. 481 e 500, e a referência da l. 730 repetem 26/11/2025). Conferir no acórdão; pelo Informativo, a data é 25/11/2025.
- A "tese vigente" entre aspas na l. 490 ("É indevida a aplicação da revisão da vida toda após a declaração de constitucionalidade...") **não é a tese oficial**. Teses fixadas: "1. A declaração de constitucionalidade do art. 3º da Lei n. 9.876/1999 impõe que o dispositivo legal seja observado de forma cogente pelos demais órgãos do Poder Judiciário e pela Administração Pública, em sua interpretação textual, que não permite exceção. O segurado do INSS que se enquadre no dispositivo não pode optar pela regra definitiva prevista no art. 29, I e II, da Lei n. 8.213/1991, independentemente de lhe ser mais favorável. 2. Ficam modulados os efeitos dessa decisão para determinar: a) a irrepetibilidade dos valores percebidos pelos segurados em virtude de decisões judiciais, definitivas ou provisórias, prolatadas até 5/4/24, data da publicação da ata de julgamento do mérito das ADI nºs 2.110/DF e 2.111/DF; b) excepcionalmente, no presente caso, a impossibilidade de se cobrarem valores a título de honorários sucumbenciais, custas e perícias contábeis dos autores que buscavam, por meio de ações judiciais pendentes de conclusão até a referida data, a revisão da vida toda. Ficam mantidas as eventuais repetições realizadas quanto aos valores a que se refere o item a) e os eventuais pagamentos quanto aos valores a que se refere o item b) efetuados."
- O cap. 1 (l. 196, 322, 393, 479) diz que o Tema 1.102 "foi superado em 2024" pelas ADIs; o cancelamento formal da tese ocorreu nos embargos de nov/2025. Harmonizar com os caps. 10 e 16. O cap. 1 também descreve o Tema 999/STJ como "matéria diversa" da vida toda, quando o Tema 999/STJ é a própria tese no STJ (apontado pelo revisor do cap. 1).
- O item "(c) 15/05/2026, novos embargos rejeitados" do box não pôde ser conferido na base.

## 4. Pendências jurisprudenciais do Módulo 4: o que a base diz em 26/09/2026

- ADI 6.309: a base só tem o Informativo 1220 (16/06/2026), já usado no livro. Sem registro de publicação do acórdão ou modulação.
- Tema 1.157/STJ: registro oficial ainda "Aguardando a publicação do acórdão" (j. 07/05/2026). Manter sem aspas.
- Tema 1.271/STF: o campo "tese firmada" da base repete o título do tema (armadilha conhecida). Não conferível aqui.
- ADI 7.873: nada na base.

## 4-bis. Atualização legislativa ausente: Lei 15.363, de 26/03/2026

A base de legislação traz a Lei 15.363/2026 (DOU 26/03/2026), que acrescentou o § 4º ao art. 45-A da Lei 8.212/91 e o § 2º ao art. 96 da Lei 8.213/91 (o parágrafo único do art. 96 virou § 1º): a multa de 10% da indenização não se aplica ao tempo rural (empregado rural ou segurado especial) anterior à obrigatoriedade de filiação, inclusive para contagem recíproca. O livro não a menciona (busca por "15.363" sem resultado). Afeta o cap. 4 (indenização do art. 45-A, l. 897-1078 e quadro da l. 1223), o cap. 5 (contagem recíproca e tempo rural pré-1991) e o cap. 9. Além disso, toda remissão ao "parágrafo único do art. 96" passou a ser "§ 1º". Conferir o texto no DOU antes de incorporar.

## 5. Padronização de citações (mecânica, global)

Contagens nos 23 capítulos:

| Forma | Ocorrências | Forma dominante |
|---|---|---|
| "Lei n. 8.213/91" × "Lei 8.213/91" × "Lei 8.213/1991" × "Lei n. 8.213/1991" | 213 × 431 × 19 × 3 | sem "n." e com "/91" (as 16 "Lei nº 8.213" estão dentro de teses literais) |
| "EC 103/2019" × "EC n. 103/2019" × "Emenda Constitucional n. 103" | 406 × 59 × 17 | "EC 103/2019" |
| "Decreto 3.048/99" × "Decreto n. 3.048/99" × "Decreto n. 3.048/1999" | 102 × 18 × 18 | "Decreto 3.048/99" |
| "§ 1º" × "§1º" | 759 × 123 | com espaço (o texto oficial das leis usa "§ 1º") |
| "Tema 1.102" × "Tema 1102" (e 1057, 1070, 1360) | 230 × 54 | com ponto de milhar; os 54 sem ponto concentram-se nos caps. 17, 19 e 21 |
| "CF/88" × "CF/1988" | 141 × 6 | "CF/88" |
| "Min." × "Ministro" (antes de nome) | 221 × 7 | "Min." |
| "j. " × "julgado em" | 172 × 15 | "j." |

Decisão do autor: adotar a forma dominante e aplicar por substituição em lote (fora de citações literais). "§1º" → "§ 1º" e "Tema NNNN" → "Tema N.NNN" são seguros.

## 6. Travessões e ponto-e-vírgula (escrita anti-IA)

Ainda há 1.652 travessões (cerca de 1.300 em prosa, fora de tabelas, títulos, citações e referências) e 1.665 ponto-e-vírgulas. Os capítulos mais carregados: 4 (108 em prosa), 10 (96), 12 (91), 6 (88), 17 (87), 11 (85). O script `scripts/fix_emdashes.py` existe (meta de 2 por seção) mas converte automaticamente, com risco de sentido. Recomendação: passe manual por capítulo, prioridade aos seis acima, convertendo apostos em parênteses ou vírgulas. Não foi aplicado nesta revisão por ser decisão de estilo dos autores.

## 7. Textos que vivem dentro do gerador (não estão em Markdown)

- **Apresentação** (`add_apresentacao_page`): diz que a obra reflete o estado do direito "até junho de 2026". O texto já incorpora fatos de setembro (Res. CNJ 673, revisão de 21-22/09). Atualizar a data de corte no fechamento. Três travessões e um "não apenas ... mas" no texto.
- **Sobre os Autores** (`add_sobre_autores_page`): a docstring registra "E-mail de contato pendente de confirmação dos autores". A biografia de Claudio Kitner não menciona o doutorado em andamento (Filosofia do Direito, PUC-SP) nem a atuação como relator na 3ª Turma Recursal de PE; ambos os autores aparecem como aprovados no "XIII Concurso" (3ª Região em 2007 e 1ª Região em 2011). Conferir os dados.
- **Ficha catalográfica**: ISBN "[a definir]" (cabe à editora).

## 8. Restos de bastidor e notas de acompanhamento

- cap. 1, l. 329: rótulo "Nota de atualização:" dentro do texto corrido (patch na lista G do cap. 1).
- cap. 23, l. 545: parágrafo "Registramos, ainda, em nota de acompanhamento, que o regime de precatórios ... Eventuais alterações supervenientes ao fechamento desta edição, cujo número, data de promulgação e dispositivos efetivamente modificados devem ser conferidos pelo operador..." lê-se como placeholder escrito antes da EC 136/2025, que o livro já cita em outros pontos. Reescrever nomeando a EC 136/2025 ou suprimir.
- cap. 18, l. 434: "Recomendamos ao leitor conferir, na data de leitura, a redação atualizada da LOAS ... no portal da legislação federal (planalto.gov.br)": tom de aviso editorial; decidir se fica.
- Nove ocorrências de "até o fechamento desta edição" (caps. 5, 8, 11, 16, 18, 22, 23): revisar todas na data de envio.

## 9. Estrutura

- Caps. 2 e 3 não têm frontmatter YAML (o gerador não depende dele) e só têm `#### Doutrina` nas Referências; o cap. 4 não tem `#### Legislação`. Os demais têm as três subseções.
- Introdução e Conclusão: o gerador desnumera os títulos que começam por "Introdução"/"Conclusão". Mas só 8 capítulos usam esses nomes; os outros fecham com "Consolidação das posições adotadas", "Síntese e quadros práticos" etc., que continuarão numerados. Se a editora exige Introdução/Conclusão sem número em todos, padronizar os títulos.
- cap. 2, l. 3: a citação de Castro e Lazzari perdeu as aspas de fechamento nas edições de setembro (o HEAD do git as tinha). Patch na lista G do cap. 2.
