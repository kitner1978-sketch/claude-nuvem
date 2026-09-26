# Ferramentas criadas nas sessões de 21 e 22/09/2026

Escritas durante a revisão fina. Todas usam caminhos relativos à raiz desta cópia (`_RAIZ = …parents[2]`), então rodam de onde a pasta `projeto_livro` estiver. Nenhuma altera o livro sozinha, exceto `patchlib.py` quando chamada, e `port_ingrid.py` com `--apply`.

| Arquivo | O que faz | Uso |
|---|---|---|
| `patchlib.py` | Aplica substituições **exatas** nos capítulos: cada trecho antigo precisa aparecer **uma única vez**, senão aborta sem gravar. Grava em UTF-8 com fim de linha LF. Foi a forma de editar todas as correções | `from patchlib import patch; patch(3, [("texto antigo exato", "texto novo")])` |
| `check_teses.py` | Para cada "Tema N" do STF/STJ/TNU seguido de trecho entre aspas, compara as aspas com a tese oficial daquele número (bases em `jurisprudencia/`). Lista semelhança < 0,82 | `python3 check_teses.py` |
| `conferir_aspas_reverso.py` | Caminho inverso: todo trecho entre aspas (90+ caracteres) contra **todas** as teses oficiais. Achou o Tema 251/TNU "modernizado" dentro das aspas | `python3 conferir_aspas_reverso.py` |
| `sweep.py` | Função `sweep(padroes)` para varrer os 23 capítulos por expressões regulares e devolver capítulo, linha, seção e contexto. Base das varreduras "regra superada" e "frase de bastidor" | importar e chamar |
| `port_ingrid.py` | **Histórico.** Transportou as edições da revisora (DOCX de 18/09) para o Markdown. Tinha um erro que truncou 3 capítulos na primeira execução; a versão aqui já tem a correção e uma salvaguarda de tamanho. Não rodar de novo sobre o texto atual: as edições já estão aplicadas | — |

## `dados/`

| Arquivo | Conteúdo |
|---|---|
| `diff_jul_set.json` | Parágrafos do DOCX de 19/07 (`A`), do DOCX da revisora de 18/09 (`B`) e os blocos alterados (`ch`) |
| `edits_ingrid.json` | As 390 edições da revisora, classificadas por capítulo e tipo |
| `ingrid_nao_transportadas.json` | As 124 edições dela que não foram levadas ao Markdown (quase todas consertos de defeitos do gerador, hoje resolvidos). Inclui a renumeração de Introdução/Conclusão, que depende de decisão do autor |
| `mapa_acentos.json` | Mapa "palavra sem acento → forma acentuada", extraído do próprio livro; usado para restaurar o cap. 10 |
| `sumulas_citadas.json`, `teses_suspeitas.json`, `sweepA.json`, `sweepB.json` | Saídas das varreduras de 21/09 (retratos daquele dia; os números de linha mudaram depois) |

## Regras aprendidas ao usar estas ferramentas

1. **Antes de qualquer edição em lote, copie os 23 capítulos** para uma pasta temporária e, depois, compare número de linhas e bytes de cada arquivo com a versão anterior (`git show HEAD:caminho | wc -l`). Foi assim que se descobriu a truncagem.
2. Relatório de agente que diz "completo" **não prova** que cobriu tudo: conferir quais capítulos têm seção própria no arquivo.
3. Recorte de base RAG que começa com vírgula ou no meio de frase é **pedaço de outro item**. Não atribuir relator/data a partir dele.
