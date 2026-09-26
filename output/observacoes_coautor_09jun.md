# Catálogo de Observações do Co-autor — 09/06/2026

**Origem:** 11 screenshots (WhatsApp, 19:21–19:23) do co-autor lendo o PDF no celular, em scroll contínuo (cada print mostra a nota anterior no topo e uma nova embaixo).
**Importante:** o PDF lido é uma **versão antiga**, anterior ao fix de diagramação de 08/06 (commit `64ce287`). Os pontos de "tabela/traços e barras" já mudaram no PDF atual.

São **8 observações distintas** (algumas aparecem em mais de um print). Duas delas — Quadro 1.1 e a pontuação — vinham nos prints iniciais (bateria 17→16), recebidos depois.

| # | Categoria | Observação (palavras do co-autor) | Local | Análise / Status | Ação |
|---|-----------|-----------------------------------|-------|------------------|------|
| 1 | Diagramação (quadros) | "Quadro talvez precise ser melhorado para deixar mais claro." / "Esse estilo de quadro que tem esses traços e barras… talvez tenha um formato mais convidativo e claro." | Quadro 1.1 (Cap. 1, p. 6) e box "Retenção art. 31" (Cap. 4) | **JÁ RESOLVIDO.** Era o bug das tabelas markdown dentro de boxes (texto cru `\| … \| ---`). Corrigido hoje (`64ce287`); no PDF atual renderizam como tabela. | Reenviar o PDF de hoje ao co-autor para conferir. |
| 2 | Pontuação | "A pontuação não está com problema na frase 'A tripartição…'?" | Cap. 1, seç. 1.8 (Constituição de 1988), linha 114 | **PROCEDE.** Travessão abre o aposto e não fecha; vírgula antes de "constitui" separa sujeito do verbo. | Fechar o aposto com travessão: "…(arts. 203–204) **—** constitui os três pilares…". Correção objetiva, posso aplicar já. |
| 3 | Estilo | "Alguns parágrafos lidos ficaram compridos, com muitas frases. Talvez fique confuso e cansativo ler." | Cap. 1 (universalidade ~p. 22-23; tripartição) | **Procede.** A fusão anti-IA de listas em prosa deixou parágrafos densos. | Quebrar parágrafos > ~8 linhas; passe de legibilidade nos caps mais densos (1, 4, 11). |
| 4 | Substância / citação | "Algumas referências a entendimento de tribunais talvez devessem vir acompanhadas de algum julgado." | Cap. 1 ("jurisprudência consolidada", "o STF reconhece") | **Procede.** Remissões genéricas sem nº de julgado. | Onde a tese for vinculante, citar julgado (Tema/Súmula/REsp); levantar ocorrências de "jurisprudência consolidada/pacífica" sem citação. |
| 5 | Elogio | "Esses quadros são excelentes. Muito atraentes." | Boxes em geral | Feedback positivo. | Manter o padrão visual. |
| 6 | Jurisprudência + estrutura | "Deixou-me preocupado com a atualização da jurisprudência. Aqui parece que o STF julgou recentemente." + "Esse quadro talvez tenha ficado perdido na temática do capítulo… só antecipando, de forma superficial, o que será visto em capítulos posteriores." | Cap. 1, box "Vedação do retrocesso social e a redução de benefícios pela EC 103/2019" (p. 40) | **PROCEDE (duplo).** (a) Box só diz "ADIs foram ajuizadas", sem desfecho — mas o julgamento existe: **Tema 1.300/STF** (RE 1.469.150), já tratado no **Cap. 6, seç. 6.7.3**. (b) O box antecipa tema de incapacidade (Cap. 6) num capítulo histórico/principiológico. | Enxugar o box ao plano principiológico (vedação do retrocesso) + remissão ao Cap. 6 com o desfecho do Tema 1.300; ou realocar. |
| 7 | Diagramação (layout) | "Problema na formatação da página." + "Problema de espaço na página novamente." | Cap. 1 ("1.25 Referências"); Cap. 4, p. 148 (vão grande no rodapé) | A reavaliar no PDF novo (o co-autor viu o antigo). Provável `cantSplit`/`keep_with_next` empurrando conteúdo e deixando vão; fluxo mudou com as tabelas agora mais altas. | Auditar páginas com >40% de vão no rodapé no PDF atual; afrouxar quebras pontualmente; revisar espaçamento do heading de Referências. |
| 8 | Conteúdo / escopo | "Lembrar ainda de tratar de regimes previdenciários, ainda que superficial." + "Separar o processo administrativo previdenciário do capítulo do processo nos JEFs." | Cap. 4 (regimes); Caps. 22/23 | (a) Possível lacuna: panorama RGPS × RPPS × RPC. (b) Caps. 22 (adm) e 23 (JEF) já estão separados — confirmar se é reforço ou se viu sobreposição. | Decisão do autor: incluir panorama curto dos regimes; confirmar separação 22/23 e checar sobreposição. |

## Síntese

- ✅ **Já resolvido:** #1 (tabelas em box → fix de hoje). Reenviar PDF atualizado.
- ✍️ **Correção objetiva (posso aplicar já):** #2 (pontuação "A tripartição").
- ✍️ **Procede, requer edição:** #3 (parágrafos longos), #4 (citar julgados), #6 (atualizar box com Tema 1.300).
- ⚠️ **Reavaliar no PDF novo:** #7 (formatação/espaço — viu o PDF antigo).
- 🤔 **Decisão do autor:** #6-b (enxugar/realocar box), #8 (regimes; separação 22/23).
- 👍 **Elogio:** #5 (manter padrão dos quadros).
