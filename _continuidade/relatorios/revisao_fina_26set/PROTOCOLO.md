# Protocolo da revisão fina (26/09/2026)

Você é revisor de texto e de direito de um livro jurídico brasileiro em fase de pré-publicação: "Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais" (Claudio Kitner e Luiz Bispo da Silva Neto, Editora Thoth). Sua tarefa é fazer a REVISÃO FINA de UM capítulo e gravar um relatório. Você NÃO edita o capítulo.

Arquivo do capítulo (somente leitura): `C:\projeto_livro\output\rascunhos\cap_NN_rascunho.md`
Relatório a gravar (único arquivo que você pode escrever): `C:\projeto_livro\_continuidade\relatorios\revisao_fina_26set\cap_NN.md`

## Como ler
Leia o arquivo INTEIRO com a ferramenta Read, em blocos (offset/limit) até o fim. Anote o total de linhas e confirme no relatório que leu todas. Não use web nem bases de jurisprudência. Não use nenhuma ferramenta além de Read, Grep e Write (Write só no caminho do relatório).

## Formato do capítulo
Markdown com frontmatter YAML (nem todos têm), linha `## Capítulo N — Título` (o travessão dessa linha é obrigatório: não toque), seções `### N.M` e `#### N.M.K`, boxes `::: box-atencao | box-jurisprudencia | box-pratica | box-quadro ... :::`, callouts `> [!warning]`/`> [!tip]`, tabelas Markdown, e fecho `### Referências` com `#### Legislação`, `#### Jurisprudência`, `#### Doutrina` (alguns capítulos só têm `#### Doutrina`: registre como observação na lista E, sem patch).

## O que procurar
1. ORTOGRAFIA E ACENTUAÇÃO: erros de digitação, acentos faltando/sobrando, letras trocadas, palavras dobradas ("de de"), palavras faltando.
2. GRAMÁTICA: concordância verbal e nominal, regência, crase, colocação pronominal, pontuação errada (vírgula entre sujeito e verbo, aposto aberto e não fechado, parêntese ou aspas sem fechar, frase sem ponto final, ponto duplo), maiúsculas/minúsculas inconsistentes.
3. FRASES DEFEITUOSAS: período inacabado, oração sem verbo, repetição de palavra na mesma frase, ambiguidade, anacoluto.
4. CONSISTÊNCIA INTERNA: numeração de seções e de "Quadro N.M" (o texto cita um quadro que não existe? quadros fora de ordem?), datas/percentuais/valores contraditórios dentro do capítulo, terminologia inconsistente (ex.: "auxílio-doença" × "auxílio por incapacidade temporária" quando fala do regime atual; "aposentadoria por invalidez" × "por incapacidade permanente"), sigla usada antes de definida, nome de autor grafado de dois modos.
5. REMISSÕES: "v. seção X.Y", "Capítulo N" ou "Quadro N.M" apontando para algo que não existe ou cujo tema não bate (as remissões entre capítulos já foram conferidas automaticamente; foque em coerência de tema).
6. FRASES DE BASTIDOR: qualquer resto de nota de produção ("verificar antes da publicação", "conforme pesquisa", "[a confirmar]", "consultar posição atualizada", instruções ao redator, placeholders). Isso é grave: vai para a lista A.
7. DIREITO (com cautela): afirmação jurídica que você tem ALTA confiança de estar errada (artigo/inciso trocado de forma evidente pelo próprio contexto, prazo ou percentual incompatível com a lei que você conhece com segurança, tribunal errado, cronologia impossível, tese atribuída ao tribunal errado). Dê a razão e a fonte que você conhece. Marque confiança (alta/média). O livro é de 2026 e cita fatos posteriores ao seu conhecimento (EC 136/2025, ADI 6.309 julgada em 2026, Lei 14.973/2024 etc.): NÃO marque como erro o que você simplesmente desconhece; nesses casos, se quiser, registre como "conferir" com confiança baixa, separado.
8. ESTILO (só o mais saliente, até ~15 itens): frases-moldura ("cumpre ressaltar que", "é importante destacar que", "vale registrar"), adjetivação tripla, "não apenas... mas também" em excesso, escadas enumerativas em prosa ("em primeiro lugar... em segundo lugar... em terceiro lugar"), conectivos repetidos ("nesse sentido", "dessa forma") no mesmo trecho, parágrafos muito longos (acima de ~200 palavras), pergunta retórica seguida de resposta óbvia, fecho de parágrafo com moral da história. Tudo isso denuncia produção por IA e os autores querem eliminar.

## O que NÃO apontar
- Travessões (—) e ponto-e-vírgula isolados: são tratados globalmente. Aponte apenas quando a estrutura estiver quebrada (aposto aberto com travessão e não fechado, por exemplo).
- Citações autor-data entre parênteses, ex. "(Castro; Lazzari, 2025)": o gerador as remove do Word.
- Grafia "salário-mínimo" com hífen: decisão já tomada.
- Introdução e Conclusão sem número: exigência da editora.
- Pendências já conhecidas: ADI 6.309, Tema 1.157/STJ sem aspas, Tema 1.271/STF, modulação da "vida toda", ADI 7.873, Súmula 577/STJ truncada no cap. 9, Súmula 149/STJ duplicada no cap. 13.
- Não proponha reescrever parágrafos inteiros por gosto. Revisão fina é cirúrgica.

## Formato do relatório (grave exatamente nesta estrutura, em português)

    # Revisão fina: Capítulo N

    Linhas lidas: N de N. Palavras: ~X.

    ## A. Correções mecânicas (aplicáveis sem decisão do autor)
    Tabela: | # | linha | tipo | trecho atual (exato) | proposta | motivo |
    (tipos: ortografia, acento, concordância, regência, crase, pontuação, palavra dobrada/faltante, bastidor, numeração)

    ## B. Consistência interna e remissões
    Lista com linha, problema, proposta.

    ## C. Direito
    Lista: linha, afirmação do livro, o que está errado, fonte, confiança (alta/média). Depois, sublista "Conferir (confiança baixa)".

    ## D. Estilo e legibilidade
    Lista curta com linha e sugestão pontual.

    ## E. Referências (seção final do capítulo)
    Entradas com erro de forma, autor citado no corpo sem entrada, entrada duplicada, ano inconsistente entre corpo e referência.

    ## F. Síntese
    3 a 5 linhas: estado geral do capítulo e os 3 problemas mais importantes.

    ## G. Patches (JSON)
    ```json
    [
      {"linha": 12, "old": "trecho exato e único do arquivo, com contexto suficiente", "new": "trecho corrigido"}
    ]
    ```

Regras dos patches (lista G): só os itens da lista A. "old" deve ser copiado LITERALMENTE do arquivo (mesmos acentos, aspas, espaços), longo o bastante para ocorrer UMA única vez no arquivo (inclua 5 a 10 palavras de contexto). "new" muda só o necessário. Não use travessão nem ponto-e-vírgula no "new". Nunca inclua num patch a linha `## Capítulo N — ...`. Se não houver certeza de que a correção é puramente mecânica, deixe fora do JSON e registre só na lista A ou B com a nota "decisão do autor".

Seja exaustivo nas listas A e B (leia frase por frase), criterioso na C e sóbrio na D. Ao terminar, responda com um resumo de 5 linhas do que encontrou (quantos itens por lista) e confirme o caminho do relatório gravado.
