# Direito Previdenciario - Teoria e Pratica nos Juizados Especiais Federais

Pipeline automatizado de geracao de livro juridico: 23 capitulos em Markdown convertidos em DOCX formatado e PDF final de 1.334 paginas.

## Estrutura

```
config/           # Configuracao (book_structure.yaml, models.yaml, prompts.yaml)
scripts/          # Pipeline Python (md_to_docx.py, gerar_livro_pdf.py, validadores)
output/capitulos/ # Capitulos-fonte em Markdown
pesquisa/         # MOCs e templates de pesquisa
state/            # Estado do pipeline (glossario, progresso)
```

## Pipeline

1. **Escrita**: Capitulos em Markdown com formatacao especial (boxes, citacoes, jurisprudencia)
2. **Conversao**: `md_to_docx.py` converte cada MD em DOCX individual formatado (A5, EB Garamond, capitulares)
3. **Unificacao**: `gerar_livro_pdf.py` unifica os 23 DOCXs em livro completo com sumario, partes, headers e rodapes
4. **Exportacao**: Conversao final DOCX -> PDF via Word COM automation

## Especificacoes de Design

| Parametro | Valor |
|-----------|-------|
| Formato | A5 (148mm x 210mm) |
| Fonte principal | EB Garamond 10.7pt |
| Margens | Espelhadas (interna 2.0cm, externa 1.5cm) |
| Cor accent | #B78B37 (dourado) |
| Capitulos | 23 em 4 partes |

## Dependencias

- Python 3.12+
- python-docx, lxml, PyYAML
- Microsoft Word (COM automation para PDF)

## Autor

Projeto de autoria privada. Repositorio privado.
