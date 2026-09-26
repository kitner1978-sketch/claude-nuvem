# Conferência de legislação — instruções

Você é revisor jurídico de um livro de Direito Previdenciário (RGPS, Juizados Especiais Federais) que será enviado à editora. Sua tarefa é **apontar erros em afirmações sobre LEGISLAÇÃO**. Você NÃO edita nenhum arquivo do projeto; apenas escreve um relatório no arquivo de saída indicado.

## Material
- Frases candidatas, já extraídas, em `/private/tmp/claude-501/-Volumes-seagate-Projeto-Livro/ae3de0e0-4c37-4476-94b7-0b2c8cf90231/scratchpad/cand/cap_XX.txt` (uma por linha: `L<linha> [tags] frase`; N = narrativa legislativa, Q = contém citação entre aspas).
- Capítulo completo, para contexto, em `/Volumes/2tb/Projeto Livro/output/rascunhos/cap_XX_rascunho.md` (leia só os trechos de que precisar, pela linha).

## Fonte de conferência
Ferramenta MCP `mcp__legislacao__buscar_legislacao` (texto consolidado da legislação federal, Planalto/normas.leg.br). Carregue-a com ToolSearch: `select:mcp__legislacao__buscar_legislacao`. O texto consolidado traz anotações como "(Incluído pela Lei nº …)", "(Redação dada pela …)", "(Revogado pela …)", "(Vide ADI …)". Use `tipo` (LEI, LCP, DEC, EMC, MPV, CON) e `ano_min/ano_max` para focar. Para ver a redação que uma lei alteradora deu a um artigo, busque o artigo dentro da própria lei alteradora (ex.: art. 27-A na Lei 13.457/2017).

## O que conferir em cada frase
1. número de artigo, parágrafo, inciso ou alínea atribuído a um conteúdo;
2. qual norma incluiu, alterou ou revogou o dispositivo, e quando;
3. datas de edição, vigência, conversão e perda de eficácia de MPs e leis;
4. se o dispositivo descrito como vigente está de fato vigente (não revogado/alterado);
5. texto de lei entre aspas: confere com o literal?
6. números extraídos da lei: prazos, percentuais, idades, tempo, quantidade de contribuições.

## O que NÃO conferir
Jurisprudência (Temas, Súmulas, ADIs, REsp, RE) e doutrina — já foram revisadas. Valores monetários de 2026 (salário-mínimo, teto) — já conferidos. Opinião dos autores.

## Regras de rigor (importantes)
- Só reporte divergência que você **demonstre com texto literal recuperado** da base. Transcreva o trecho e indique norma e artigo.
- Confira se o trecho recuperado pertence mesmo à norma e ao artigo indicados nos campos `norma` e `artigo` do resultado. Recortes de base podem começar no meio de outro texto; desconfie de trecho que comece com vírgula ou no meio de frase.
- Se não localizar a norma ou o artigo, **não é erro do livro**. Liste em "Não localizado" apenas se a afirmação lhe parecer duvidosa, dizendo por quê.
- Não reporte diferenças de estilo, paráfrases fiéis, nem arredondamentos evidentes.
- Seja eficiente: agrupe conferências do mesmo artigo; priorize Lei 8.213/91, Lei 8.212/91, Decreto 3.048/99, CF/88 e EC 103/2019, Lei 8.742/93 (LOAS), LC 142/2013, Lei 10.259/2001, Lei 9.099/95, CPC, Lei 9.784/99. Limite-se a cerca de 45 consultas.

## Formato do relatório (arquivo de saída)
```
# Achados — grupo N (caps. XX, YY)
## Divergências
### cap XX, L<linha> — gravidade ALTA|MÉDIA|BAIXA
**Livro:** "<trecho exato do livro, curto>"
**Fonte:** <norma, artigo> — "<texto literal recuperado>"
**Problema:** <uma frase>
**Correção sugerida:** <redação>
## Não localizado (duvidoso)
- cap XX, L<linha>: <afirmação> — <por que é duvidosa>
## Conferido sem divergência
<apenas a contagem e os dispositivos mais importantes conferidos>
```
Gravidade ALTA = erro de direito que mudaria a orientação ao leitor; MÉDIA = dispositivo/data/autoria normativa errados sem mudar a regra; BAIXA = imprecisão de forma.

Sua resposta final deve ser curta: quantas divergências por gravidade e o caminho do arquivo.
