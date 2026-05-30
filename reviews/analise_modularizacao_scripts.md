# Análise de Modularização dos Scripts — Referência

> **STATUS: IMPLEMENTADO em 2026-05-30** — itens 1 (design code) e 2 (deduplicação) aplicados;
> criado `scripts/design_code.py`; PDF revalidado em 1.270 páginas (idêntico ao baseline v12).
> O item 3 (funções-monstro) foi deliberadamente **mantido como está** (alto risco, baixo ganho).
> O mapeamento abaixo permanece como referência da estrutura e de uma eventual refatoração futura.
> Data do mapeamento: 2026-05-29

## Resumo

Pipeline: ~9.128 linhas em 23 scripts. Apenas dois são candidatos a modularização:
- `scripts/md_to_docx.py` — 1.409 linhas
- `scripts/gerar_livro_pdf.py` — 1.303 linhas

Os outros 21 são utilitários de propósito único, no tamanho adequado. **Não modularizar.**

---

## Candidatos a refatoração (em ordem de valor/risco)

### 1. Design code disperso — ALTO VALOR, BAIXO RISCO

Hoje o "design code" está hardcoded e espalhado:
- `"EB Garamond"` aparece ~100 vezes; `"Noto Sans"` ~55 vezes
- Tamanhos de fonte (`Pt(10.7)`, `Pt(15.5)`, `Pt(12.5)`, `Pt(20)`, `Pt(9.5)`...) em ~90 locais
- Espaçamento de linha (1.08, 1.05, 1.03, 1.0) e de parágrafo (3.5pt, 4pt, 2pt) em ~25 locais
- Margens A5 escritas inline em duas funções (`set_page_a5_mirrored` e `setup_section`)
- Recuos de célula (150/220/180/100/240 dxa) inline
- **Apenas `COLORS` está centralizado** (md_to_docx.py L38-56, importado por gerar_livro_pdf)

**Proposta futura:** criar `scripts/design_code.py` com tokens:
```python
FONTS = {"body": "EB Garamond", "sans": "Noto Sans"}
SIZES = {"body": 10.7, "section": 15.5, "subsection": 12.5, "chapter_title": 20, "label": 9.5}
SPACING = {"line_body": 1.08, "para_after": 3.5, "first_indent_cm": 0.42}
MARGINS_A5 = {"top": 1.65, "bottom": 1.70, "left": 2.05, "right": 1.55,
              "header": 0.80, "footer": 0.75, "width": 14.8, "height": 21.0}
```
Substituir literais por tokens de **valor idêntico** → PDF deve sair igual (validar paginação = 1.270pp).

### 2. Duplicação de código — VALOR MÉDIO, BAIXO RISCO

| Duplicação | md_to_docx.py | gerar_livro_pdf.py | Observação |
|---|---|---|---|
| PAGE field | `_add_page_field()` L846-868 | `add_page_number_field()` L78-99 | **22 linhas idênticas**, nomes diferentes |
| Estilo Normal | `generate_docx()` L1256-1265 | `create_unified_docx()` L788-797 | **9 linhas idênticas** |
| Margens A5 | `set_page_a5_mirrored()` L566-599 | `setup_section()` L102-119 | Idênticas; `setup_section` não chama os `_enable_*` |

**Proposta futura:** mover funções compartilhadas para um módulo comum (ex.: `docx_helpers.py`) e importar nos dois lados.

### 3. Funções "monstro" — VALOR BAIXO, RISCO ALTO

Funções que misturam responsabilidades (config + OOXML + renderização):
- `create_unified_docx()` (gerar_livro_pdf.py L783-1031, **249 linhas**) — estilos + settings + I/O + orquestração de capa→TOC→capítulos→backmatter
- `generate_docx()` (md_to_docx.py L1248-1370, 122 linhas) — switch com 8 branches
- `add_box()` (md_to_docx.py L943-1089, 147 linhas) — seleção de config + tabela OOXML + render de 3 tipos de lista

**Recomendação:** NÃO refatorar a menos que a manutenção se torne dolorosa. O código funciona e a quebra pode alterar sutilmente o layout do PDF. Decomposição sugerida, se um dia for feita:
- `create_unified_docx` → `configure_styles()`, `configure_settings()`, `build_frontmatter()`, `build_chapters()`, `build_backmatter()`
- `add_box` → `_get_box_config()`, `_add_box_table()`, `_render_box_content()`

---

## Protocolo de validação (para quando refatorar)

1. Commitar/backup antes (já temos baseline no commit `a0a4946`)
2. Refatorar
3. Gerar PDF: `& "C:\Python313\python.exe" "D:\Projeto Livro\scripts\gerar_livro_pdf.py"`
4. Conferir paginação final = **1.270 páginas** (baseline v12)
5. Comparar amostras de layout (capa, capitular, boxes, TOC)
