# Revisão fina de 26/09/2026: patches aplicados (capítulos 1 a 9)

Sessão na nuvem (Claude Code, repositório `claude-nuvem`), 26/09/2026, à tarde. Módulo 1 do que faltava: aplicar as listas G dos relatórios `cap_01.md` a `cap_09.md`.

## Método

1. Extração do JSON da seção G de cada relatório.
2. Ensaio a seco: cada "old" precisa ocorrer exatamente uma vez no capítulo. Os 122 passaram.
3. Leitura dos 122 pares, um a um, antes de gravar.
4. Aplicação com `_continuidade/ferramentas/patchlib.py` (UTF-8, LF).
5. Conferência posterior: número de linhas igual ao retrato `snapshots/rascunhos_pre_revisao_fina_26set/` nos 23 capítulos; linha `## Capítulo N — ...` intacta em todos; travessões e ponto-e-vírgulas não aumentaram (cap. 7: 52 para 51 travessões; cap. 9: 58 para 56); nenhum CRLF.
6. `verificar_refs_cruzadas`: 194 remissões, 0 erros.
7. DOCX regerado: `output/livro_completo - 26 de set 26.docx` (1.286.331 bytes; o de 22/09 tinha 1.286.327).

## Resultado

| Cap. | Patches no relatório | Aplicados | Observação |
|---|---|---|---|
| 1 | 24 | 24 | |
| 2 | 4 | 4 | |
| 3 | 11 | 11 | Os 5 patches "Autor (ano) verbo que" foram testados contra `strip_citations`: o gerador remove a oração e capitaliza a seguinte. Antes, o DOCX saía com "Santos e Calejon (2025) A EC 103/2019..." |
| 4 | 18 | 18 | Inclui a tabela do teto: "Até 11/1994" corrigido para "Até 11/1998" (linha seguinte é 12/1998, EC 20) |
| 5 | 5 | 5 | |
| 6 | 10 | 10 | "rel." para "Rel." segue a forma dominante do livro (107 contra 39) |
| 7 | 8 | 8 | Súmula 53/TNU restaurada ao enunciado oficial na l. 400, com a nomenclatura atual fora das aspas |
| 8 | 26 | 26 | |
| 9 | 16 | 13 | Ver abaixo |

**Cap. 9, não aplicados (3):** os patches 9 e 10 inseriam "Lei n. 8.213/91" e "Lei n. 10.256/2001", contra a forma dominante do livro (431 "Lei 8.213/91" contra 213 com "n."). O patch 16 trocava "(Cap. 16)" por "(Capítulo 16)", contra 33 ocorrências de "(Cap. N)" contra 8. Ambos dependem da padronização global (achados globais, item 5), que é decisão do autor.

**Cap. 9, reduzido (1):** o patch 8 passou a acrescentar só o "da" que faltava: "(art. 48, § 3º, da Lei 8.213/91, acrescentado pela Lei n. 11.718/2008)".

## O que este módulo NÃO cobre

- Listas A com nota "decisão do autor", listas B, C, D e E dos relatórios dos caps. 1 a 9.
- Os achados globais (`00_ACHADOS_GLOBAIS.md`): referências de doutrina, súmulas divergentes nos caps. 2, 3, 6, 15, 18, 19, 20 e 23, Tema 1.102 no cap. 16, Lei 15.363/2026, padronização de citações, textos dentro do gerador.
- Relatórios dos caps. 10 a 23 (não existem).

## Ambiente

`check_teses.py` e `conferir_aspas_reverso.py` não rodam nesta cópia: dependem de `jurisprudencia/` (13 GB, fora do git). PDF de conferência gerado com LibreOffice 24.2 (Writer instalado na sessão): `output/livro_completo - 26 de set 26.pdf`. A paginação do LibreOffice difere um pouco da do Word; serve para conferir texto, não para fechar o número de páginas.
