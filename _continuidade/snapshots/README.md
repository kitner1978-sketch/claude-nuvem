# Retratos do texto-fonte

Três estados do livro existem nesta cópia:

| Estado | Onde |
|---|---|
| 20/07/2026 (último commit, `0cb45ea`) | no git: `git show HEAD:output/rascunhos/cap_03_rascunho.md` |
| **21/09/2026, 20h** — é o texto do `output/livro_completo - 21 de set 26.docx` (revisão dirigida + edições da revisora + gerador corrigido) | `rascunhos_fim_21set/` (23 capítulos + os dois scripts do gerador) |
| **22/09/2026, 6h** — é o texto do `output/livro_completo - 22 de set 26.docx`. Acrescenta ao anterior: Epílogo do cap. 23 corrigido e montado como seção própria, título "Referências" restaurado no cap. 22, exemplo do cap. 15 ajustado ao salário-mínimo de 2026, Tema 251/TNU literal, 4 precedentes inexistentes substituídos (caps. 4 e 14), Apresentação corrigida e o **Módulo 1** (11 divergências graves de legislação) | a própria árvore de trabalho (`output/rascunhos/`, `scripts/`) |

Para ver o que mudou entre os dois DOCX num capítulo:

```bash
diff _continuidade/snapshots/rascunhos_fim_21set/cap_20_rascunho.md output/rascunhos/cap_20_rascunho.md
```
