# Projeto de Geração de Livro Acadêmico — Template de Referência

> **Baseado em:** *Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais*
> **Autores:** Claudio Kitner & Luiz Bispo da Silva Neto
> **Pipeline:** Markdown → DOCX (python-docx) → PDF (Word COM)
> **Lições acumuladas:** 4 etapas de correção textual + debugging de geração PDF

---

## 1. Estrutura de Diretórios

```
ProjetoLivro/
├── config/
│   ├── book_structure.yaml      # Estrutura do livro (partes, capítulos, status)
│   ├── models.yaml              # Configuração de modelos de IA (rotas, temperaturas)
│   └── prompts.yaml             # Prompts dos agentes (pesquisador, redator, auditor...)
│
├── scripts/
│   ├── gerar_livro_pdf.py       # Orquestrador principal: MD → DOCX unificado → PDF
│   ├── md_to_docx.py            # Conversor MD → DOCX com design editorial
│   ├── gerar_indice_referencias.py  # Extrai índice remissivo e referências
│   └── [utilitários auxiliares]
│
├── output/
│   ├── rascunhos/               # Arquivos fonte: cap_XX_rascunho.md
│   ├── capitulos/               # Versões finais: cap_XX.md
│   ├── docx/                    # DOCX individuais por capítulo
│   ├── auditoria/               # Relatórios de auditoria
│   ├── livro_completo.docx      # DOCX unificado
│   └── livro_completo.pdf       # PDF final
│
├── state/
│   ├── pipeline_state.json      # Estado do pipeline de processamento
│   └── glossario.json           # Glossário de termos técnicos
│
└── PROJETO_LIVRO_TEMPLATE.md    # Este documento
```

### Convenções de Nomenclatura

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Rascunho MD | `cap_XX_rascunho.md` | `cap_07_rascunho.md` |
| Capítulo final | `cap_XX.md` | `cap_07.md` |
| DOCX individual | `{basename}.docx` | `cap_07_rascunho.docx` |
| Pesquisa | `pesquisa_cap_XX.md` | `pesquisa_cap_07.md` |
| Estratégia | `estrategia_cap_XX.md` | `estrategia_cap_07.md` |
| Multi-parte | `cap_XX_parte_[a\|b].md` | `cap_07_parte_a.md` |

---

## 2. Estrutura do Livro

### 2.1 Definição de Partes e Capítulos

```yaml
# config/book_structure.yaml
title: "Título do Livro"
authors:
  - "Autor 1"
  - "Autor 2"

parts:
  - num: "I"
    title: "Nome da Parte I"
    chapters: ["01", "02", "03"]     # IDs com zero-padding de 2 dígitos
  - num: "II"
    title: "Nome da Parte II"
    chapters: ["04", "05"]
  # ...até Parte VI
```

### 2.2 Formato do Markdown de Entrada

Cada capítulo segue esta estrutura obrigatória:

```markdown
## Capítulo X — Título do Capítulo

### X.1 Primeira Seção

Parágrafo de abertura (receberá capitular automática).

Parágrafos seguintes com recuo de primeira linha.

#### X.1.1 Subseção

Texto da subseção.

::: box-atencao
**Título do box de atenção.**
Conteúdo explicativo.
:::

::: box-jurisprudencia
**Ementa ou título da jurisprudência.**
Texto descritivo.
:::

::: box-pratica
**Exemplo — Título descritivo:**
Texto prático.
:::

| Coluna 1 | Coluna 2 | Coluna 3 |
|----------|----------|----------|
| Dado A   | Dado B   | Dado C   |

*Fonte: Elaboração dos autores.*

> Citação em bloco com recuo e estilo diferenciado.

- Item de lista não ordenada
- Segundo item

1. Item de lista ordenada
2. Segundo item

## Referências

SOBRENOME, Nome. *Título da Obra*. Editora, Ano.
```

### 2.3 Regras Críticas do Markdown

1. **Heading do capítulo**: sempre `## Capítulo X — Título` (em-dash, não vírgula)
2. **Seções**: `### X.Y Título` (com número de capítulo prefixado)
3. **Subseções**: `#### X.Y.Z Título`
4. **Boxes**: delimitados por `::: box-TIPO ... :::` (4 tipos: atencao, jurisprudencia, pratica, quadro)
5. **Tabelas**: formato pipe Markdown padrão com linha de cabeçalho
6. **Referências**: seção `## Referências` ao final — preservada integralmente
7. **Negrito/Itálico**: `**negrito**`, `*itálico*`, `***negrito-itálico***`
8. **Sem HTML**: nenhuma tag HTML no Markdown

---

## 3. Design Editorial — Parâmetros Completos

### 3.1 Formato de Página

| Parâmetro | Valor |
|-----------|-------|
| Tamanho | A5 (14.8 cm × 21.0 cm) |
| Orientação | Retrato |
| Margens espelhadas | Sim (w:mirrorMargins) |
| Margem superior | 1.65 cm |
| Margem inferior | 1.70 cm |
| Margem interna (lombada) | 2.05 cm |
| Margem externa | 1.55 cm |
| Distância do cabeçalho | 0.80 cm |
| Distância do rodapé | 0.75 cm |

### 3.2 Tipografia

| Elemento | Fonte | Tamanho | Cor | Estilo |
|----------|-------|---------|-----|--------|
| Corpo do texto | EB Garamond | 10.7 pt | #201B16 | Normal |
| Seção (###) | EB Garamond | 15.5 pt | #3A3128 | Negrito + borda inferior |
| Subseção (####) | EB Garamond | 12.5 pt | #3A3128 | Negrito |
| Título do capítulo | EB Garamond | 20 pt | #2F2923 | Negrito, all-caps |
| Título de parte | EB Garamond | 18 pt | #2F2923 | Negrito, all-caps |
| Etiqueta "CAPÍTULO X" | Noto Sans | 9.5 pt | #8A6A2A | Negrito, all-caps |
| Etiqueta "PARTE X" | Noto Sans | 10 pt | #8A6A2A | Negrito, all-caps |
| Cabeçalho par/ímpar | EB Garamond | 8.6 pt | #6B6256 | Small-caps |
| Rodapé (nº página) | EB Garamond | 9 pt | #6B6256 | — |
| Nota de tabela | EB Garamond | 8.5 pt | #6B6256 | Itálico |
| Referência bibliográfica | EB Garamond | 9.4 pt | #201B16 | Recuo francês |
| Capitular inline | EB Garamond | 24 pt | #B78B37 | Negrito |
| Título capa | EB Garamond | 22 pt | #2F2923 | Negrito |
| Autores capa | EB Garamond | 14 pt | #3A3128 | Small-caps |

### 3.3 Espaçamento

| Elemento | Antes | Depois | Entrelinhas | Recuo 1ª linha |
|----------|-------|--------|-------------|----------------|
| Parágrafo corpo | 0 | 3.5 pt | 1.08 | 0.42 cm |
| Seção (###) | 18 pt | 7 pt | 1.0 | — |
| Subseção (####) | 13 pt | 4 pt | 1.0 | — |
| Drop cap | 0 | 3.5 pt | 1.08 | — |
| Item de lista | 0 | 2 pt | 1.08 | -0.35 cm (francês) |
| Blockquote | 0 | 3.5 pt | 1.08 | — |
| Referência | 0 | 2.4 pt | 1.0 | -0.48 cm (francês) |

### 3.4 Paleta de Cores

```
TEXTOS
  #201B16  Corpo do texto (quase-preto quente)
  #2F2923  Títulos (marrom escuro)
  #3A3128  Headings (marrom médio)
  #6B6256  Texto secundário (cinza-marrom)

ACENTOS
  #B78B37  Dourado principal (ornamentos, capitulares, borda atencao)
  #8A6A2A  Dourado escuro (etiquetas CAPÍTULO/PARTE)
  #B89B5E  Dourado seção (borda inferior de seções)
  #D7CDBB  Bege claro (borda cabeçalho, linhas decorativas)
  #D2C9B8  Bege genérico (bordas de boxes)

FUNDOS DE BOXES
  #F7F1E6  box-atencao   (bege quente)      borda: #B78B37
  #EEF3F7  box-jurisprudencia (azul claro)   borda: #4D6F8A
  #F0F4ED  box-pratica   (verde claro)       borda: #6E8563
  #F5F3EF  box-quadro    (bege neutro)       borda: #6B6256

TABELAS
  #F0EDE6  Cabeçalho de tabela (bege)
  #D2C9B8  Borda de tabela
```

### 3.5 Ornamentos

| Contexto | Símbolo | Fonte | Tamanho | Cor |
|----------|---------|-------|---------|-----|
| Capa (superior) | ◆  ◆  ◆ | EB Garamond | 11 pt | #B78B37 |
| Capa (inferior) | ◆ | EB Garamond | 9 pt | #B78B37 |
| Partes | ◆  ◆  ◆ | EB Garamond | 9 pt | #B78B37 |
| Capítulos | ◆ | EB Garamond | 9 pt | #B78B37 |
| Sumário | ◆ | EB Garamond | 9 pt | #B78B37 |

---

## 4. Estrutura de Seções do DOCX

### 4.1 Mapa de Seções

```
Seção 0  — CAPA
           Tipo: default (nextPage)
           pgNumType: lowerRoman, start=1
           Cabeçalho/rodapé: VAZIO (suprimido)

Seção 1  — SUMÁRIO
           Tipo: nextPage
           pgNumType: lowerRoman (continua da capa)
           Cabeçalho: "Sumário"
           Campo TOC: TOC \o "1-2" \h \z \u

Seção 2  — PARTE I (primeira parte)
           Tipo: oddPage
           pgNumType: decimal, start=1  ← REINÍCIO ARÁBICO
           Cabeçalho: "Parte I"

Seção 3  — CAPÍTULO 1
           Tipo: nextPage
           pgNumType: NENHUM (continua)
           Cabeçalho: "Capítulo 1 | Título"

Seção 4+ — CAPÍTULOS SUBSEQUENTES
           Tipo: nextPage
           pgNumType: NENHUM (continua)

Seções de PARTES II–VI
           Tipo: oddPage
           pgNumType: NENHUM (continua)

Última seção — ÍNDICE REMISSIVO
           Tipo: oddPage
           pgNumType: NENHUM (continua)
```

### 4.2 Heading Styles para TOC

| Estilo | Uso | Nível TOC |
|--------|-----|-----------|
| Heading 1 | Títulos de PARTES | Nível 1 (TOC 1, negrito, 11pt) |
| Heading 2 | Títulos de CAPÍTULOS | Nível 2 (TOC 2, normal, 10pt, indent 0.5cm) |

**IMPORTANTE**: Usar `all_caps=True` no run (não `.upper()` no texto) para que o TOC exiba texto legível em mixed-case.

### 4.3 Cabeçalhos e Rodapés

```
┌─────────────────────────────────────────┐
│ Página ÍMPAR (direita)                  │
│ Cabeçalho: "Capítulo X | Título"        │  ← alinhado à direita, small-caps
│                              borda ───   │  ← borda inferior #D7CDBB
│                                         │
│ [conteúdo]                              │
│                                         │
│              [nº página]                │  ← centralizado, 9pt
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Página PAR (esquerda)                   │
│ "Direito Previdenciário"                │  ← alinhado à esquerda, small-caps
│ ─── borda                               │
│                                         │
│ [conteúdo]                              │
│                                         │
│              [nº página]                │
└─────────────────────────────────────────┘

PRIMEIRA PÁGINA de cada seção:
  Cabeçalho: VAZIO
  Rodapé: [nº página] (centralizado)
```

---

## 5. Pipeline de Geração

### 5.1 Fluxo Completo

```
1. LEITURA DOS MDs
   ├─ Lê cap_XX_rascunho.md de output/rascunhos/
   ├─ strip_citations() remove ~200 citações doutrinárias
   └─ parse_markdown() converte em lista de blocos tipados

2. GERAÇÃO DO DOCX UNIFICADO (python-docx)
   ├─ Configura estilos: Normal, Heading 1, Heading 2, TOC 1, TOC 2
   ├─ Habilita margens espelhadas + cabeçalhos par/ímpar
   ├─ Insere capa (section 0, Roman)
   ├─ Insere sumário com campo TOC via XML (section 1, Roman)
   ├─ Para cada Parte:
   │   ├─ Nova seção ODD_PAGE
   │   ├─ Página divisória (Heading 1)
   │   └─ Para cada capítulo:
   │       ├─ Nova seção NEW_PAGE
   │       ├─ Configura header com título do capítulo
   │       └─ Insere blocos: chapter_title, section, paragraph, box, table, list...
   ├─ Insere índice remissivo (ODD_PAGE)
   └─ Salva .docx

3. CONVERSÃO PARA PDF (Word COM via win32com)
   ├─ Abre DOCX no Word (Visible=True)
   ├─ Força Print View (wdPrintView = 3)
   ├─ Navega ao final/início para forçar paginação
   ├─ doc.Repaginate()
   ├─ Atualiza todos os Fields (PAGE, TOC)
   ├─ TablesOfContents.Update()
   ├─ ExportAsFixedFormat (wdExportFormatPDF = 17)
   └─ Fecha e encerra Word

4. FALLBACK: LibreOffice headless (TOC não atualizado)
```

### 5.2 Conversão Word COM — Detalhes

```python
# Constantes Word COM
wdPrintView = 3
wdStory = 6
wdStatisticPages = 2
wdExportFormatPDF = 17
wdExportOptimizeForPrint = 0
wdExportAllPages = 0
wdExportDocumentContent = 0
wdExportCreateHeadingBookmarks = 1
wdAlertsNone = 0

# Tempos de espera (testados com documentos de 1300+ páginas)
# - Após abrir documento: 5s
# - Após navegar ao final: 8s
# - Após voltar ao início: 3s
# - Após Repaginate: 5s
# - Após atualizar campos: 3s
# - Após atualizar TOC: 3s
# - Antes de fechar: 3s
```

---

## 6. Bugs Conhecidos e Soluções

### 6.1 TOC com todas as páginas mostrando "1"

**Causa raiz**: `python-docx` ao chamar `doc.add_section()` copia o `w:pgNumType` inteiro da seção anterior. Se a primeira seção tem `start="1"`, **todas as seções subsequentes herdam `start="1"`**, reiniciando a paginação em cada seção.

**Solução**: Após cada `add_section()`, remover o `pgNumType` herdado:

```python
def add_new_section(doc, start_type='NEW_PAGE'):
    new_section = doc.add_section(st)
    setup_section(new_section)
    # CRÍTICO: remover pgNumType herdado
    sectPr = new_section._sectPr
    for old_pgNum in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(old_pgNum)
    return new_section
```

### 6.2 Drop Cap disforme com framePr

**Causa raiz**: `w:framePr dropCap="drop"` cria um frame flutuante separado do texto. Em formato A5 com margens espelhadas, o posicionamento do frame fica irregular, gerando letras desalinhadas.

**Solução**: Substituir por capitular inline (letra grande no mesmo parágrafo):

```python
def add_drop_cap(doc, text, cap_color="B78B37"):
    p = doc.add_paragraph()
    # Letra capitular inline — 24pt, dourada, negrito
    add_run_with_style(p, first_letter, size=Pt(24), bold=True, color=cap_color)
    # Restante do texto no mesmo parágrafo
    segments = _parse_inline_formatting(rest_text)
    for seg_text, is_bold, is_italic in segments:
        add_run_with_style(p, seg_text, size=Pt(10.7), bold=is_bold, italic=is_italic)
```

### 6.3 SaveAs2 falha em documentos grandes

**Causa raiz**: O método `doc.SaveAs2()` do Word COM falha com "O comando falhou" para documentos com 1000+ páginas.

**Solução**: Usar `doc.ExportAsFixedFormat()` que é mais robusto:

```python
doc.ExportAsFixedFormat(
    OutputFileName=pdf_abs,
    ExportFormat=17,           # wdExportFormatPDF
    OpenAfterExport=False,
    OptimizeFor=0,             # wdExportOptimizeForPrint
    CreateBookmarks=1          # wdExportCreateHeadingBookmarks
)
```

### 6.4 Bloqueio de arquivo por Word/Acrobat

**Causa raiz**: Processos Word ou Acrobat anteriores mantêm lock no .docx ou .pdf.

**Solução**: Matar processos antes de gerar:

```python
import subprocess
subprocess.run(['taskkill', '/f', '/im', 'WINWORD.EXE'], capture_output=True)
subprocess.run(['taskkill', '/f', '/im', 'Acrobat.exe'], capture_output=True)
```

### 6.5 all_caps no heading: TOC ilegível

**Causa raiz**: Usar `text.upper()` armazena o texto em MAIÚSCULAS no XML. O TOC mostra tudo em caixa alta sem espaçamento.

**Solução**: Armazenar mixed-case e usar `all_caps=True` no run:

```python
# ERRADO: p.add_run(title.upper())
# CERTO:
add_run_with_style(p, title, all_caps=True)  # Exibe CAPS, armazena mixed-case
```

### 6.6 Variável fora do escopo em except

**Causa raiz**: `except Exception as e:` — a variável `e` não existe fora do bloco except em Python 3.

**Solução**: Salvar em variável separada:

```python
word_error = None
try:
    _convert_via_word(...)
except Exception as e:
    word_error = str(e)  # salvar antes de sair do except
```

### 6.7 Campo TOC via placeholder vs. XML direto

**Causa raiz**: Inserir `<<TOC_PLACEHOLDER>>` e substituir via COM é frágil (Find/Replace pode falhar, o TOC fica sem formatação).

**Solução**: Inserir campo TOC diretamente no XML do DOCX:

```python
# Inserir campo TOC via XML (python-docx)
p_toc = doc.add_paragraph()
for tag in ['begin', 'instrText', 'separate', 'text', 'end']:
    r = parse_xml(f'<w:r {nsdecls("w")}>...</w:r>')
    p_toc._element.append(r)
# instrText: ' TOC \\o "1-2" \\h \\z \\u '
# Word COM só precisa chamar Fields.Update()
```

---

## 7. Strip Citations — Padrões de Remoção

A função `strip_citations()` remove citações doutrinárias do corpo do texto para o PDF, preservando a seção "## Referências". Essencial para livros que mantêm citações no MD fonte mas não no produto final.

### 7.1 Padrões Removidos

| # | Tipo | Exemplo | Resultado |
|---|------|---------|-----------|
| 1 | Parentética multi-autor | `(CASTRO; LAZZARI, 2025)` | *(removido)* |
| 2 | Parentética single | `(Castro, 2025)` | *(removido)* |
| 3 | Parentética com conectores | `(Castro e Lazzari, 2025; Kertzman, 2024)` | *(removido)* |
| 4 | Narrativa introdutória | `Como ensina Castro (2025),` | *(removido)* |
| 5 | Narrativa sujeito | `Castro (2025) ensina que` | `ensina que` |
| 6 | Conforme inline | `, conforme Castro (2025)` | *(removido)* |
| 7 | Como destaca trailing | `, como destaca Castro (2025)` | *(removido)* |

### 7.2 Verbos Introdutórios Reconhecidos

`ensina, leciona, aponta, destaca, observa, explica, ressalta, afirma, sustenta, defende, argumenta, esclarece, sintetiza, pondera, adverte, registra, assevera, preleciona, anota, pontua, consigna`

### 7.3 Limpeza Pós-Remoção

1. Espaços duplos → espaço simples
2. Espaço antes de pontuação → remove espaço
3. Capitalização após ponto final
4. Vírgulas duplicadas → vírgula única
5. Vírgula antes de ponto → ponto

---

## 8. Índice Remissivo — Extração Automática

### 8.1 Legislação

Padrões detectados automaticamente:
- `Lei [n.] X.XXX/AAAA`
- `Lei Complementar [n.] XXX/AAAA`
- `Decreto [n.] X.XXX/AAAA`
- `Decreto-Lei [n.] X.XXX/AAAA`
- `Instrução Normativa [INSS/PRES] [n.] XXX/AAAA`
- `Emenda Constitucional [n.] XXX[/AAAA]`
- `Medida Provisória [n.] XXX/AAAA`
- `Portaria [Conjunta] [n.] XXX/AAAA`

### 8.2 Súmulas e Temas

- `Súmula [Vinculante] [n.] XXX [do STF/STJ/TNU/TRF]`
- `Tema [n.] XXX [do STF/STJ/TNU]`

### 8.3 Institutos Jurídicos

49 termos hardcoded (configuráveis), incluindo: aposentadoria por idade, auxílio-doença, salário de benefício, carência, fator previdenciário, etc.

---

## 9. Agentes de IA — Configuração

### 9.1 Papéis dos Agentes

| Agente | Função | Temperatura |
|--------|--------|-------------|
| Pesquisador | Levantamento bibliográfico, fontes, jurisprudência | default |
| Redator | Redação do capítulo com estilo acadêmico | default |
| Advogado do Diabo | Crítica rigorosa, verificação de afirmações | 0.1 |
| Auditor | Verificação de citações, zero-tolerance | 0.0 |
| Consistência | Terminologia, contradições, redundâncias | default |
| Formatador | Conversão para formato Markdown correto | default |

### 9.2 Filtros Anti-IA na Redação

O redator aplica 8 filtros para evitar linguagem artificial:

1. **Conectivos pomposos**: "Nesse sentido", "Cumpre ressaltar", "Importante salientar"
2. **Redundâncias**: "é importante destacar que", "vale mencionar que"
3. **Adjetivos vazios**: "fundamental", "imprescindível", "inegável"
4. **Estruturas mecânicas**: "Em primeiro lugar... Em segundo lugar..."
5. **Meta-referências**: "conforme mencionado acima", "como veremos adiante"
6. **Generalizações**: "toda a doutrina concorda", "é unânime"
7. **Clichês jurídicos**: "via de regra", "a rigor", "em última análise"
8. **Repetição de padrão**: três parágrafos consecutivos com mesma estrutura

---

## 10. Checklist de Validação Pré-Publicação

### 10.1 Markdown

- [ ] Todos os capítulos têm heading `## Capítulo X — Título`
- [ ] Seções seguem `### X.Y Título` (com número do capítulo)
- [ ] Boxes usam delimitadores `::: box-TIPO ... :::`
- [ ] Tabelas têm linha separadora `|---|---|`
- [ ] Seção `## Referências` presente em cada capítulo
- [ ] Sem HTML embutido
- [ ] Sem headings espúrios (vírgulas em vez de em-dash no título)

### 10.2 DOCX/PDF

- [ ] Sumário (TOC) com páginas corretas e crescentes
- [ ] Todas as 6 Partes e 23 Capítulos listados no sumário
- [ ] Numeração romana na capa/sumário, arábica a partir de Parte I
- [ ] Cabeçalhos par (título do livro) e ímpar (título do capítulo)
- [ ] Rodapé com número de página em todas as páginas
- [ ] Capitulares sem distorção visual
- [ ] Boxes com fundo colorido e borda lateral
- [ ] Tabelas com cabeçalho diferenciado
- [ ] Partes sempre em página ímpar (ODD_PAGE)
- [ ] Drop caps apenas no primeiro parágrafo após heading
- [ ] Sem páginas em branco indesejadas (exceto verso de ODD_PAGE)

### 10.3 Conteúdo

- [ ] strip_citations removeu todas as citações parentéticas
- [ ] Referências intactas ao final de cada capítulo
- [ ] Índice remissivo com legislação, súmulas e institutos
- [ ] Sem termos repetidos no índice
- [ ] Metadados do documento (título, autor, assunto) preenchidos

---

## 11. Dependências e Ambiente

### 11.1 Python

```
Python 3.12+ (testado com 3.13)
python-docx >= 1.1.0
pywin32 (win32com.client para COM automation)
PyYAML (para config files)
```

### 11.2 Sistema

```
Microsoft Word (para COM automation e exportação PDF)
  - Fontes instaladas: EB Garamond, Noto Sans
  - Ativado: margens espelhadas, cabeçalhos par/ímpar

Fallback: LibreOffice (sem atualização de TOC)
```

### 11.3 Fontes Necessárias

| Fonte | Uso | Download |
|-------|-----|----------|
| EB Garamond | Corpo, títulos, cabeçalhos | Google Fonts |
| Noto Sans | Etiquetas de parte/capítulo | Google Fonts |

---

## 12. Lições Aprendidas — Referência Rápida

| # | Lição | Impacto |
|---|-------|---------|
| 1 | `add_section()` copia pgNumType — sempre limpar | TOC com páginas erradas |
| 2 | Usar `all_caps=True` no run, nunca `.upper()` | TOC ilegível |
| 3 | `ExportAsFixedFormat` > `SaveAs2` para PDFs grandes | Falha silenciosa |
| 4 | Matar Word/Acrobat antes de gerar | Lock de arquivo |
| 5 | Drop cap inline > framePr em A5 | Distorção visual |
| 6 | Campo TOC via XML direto > placeholder COM | Confiabilidade |
| 7 | Variável do except não sobrevive ao bloco | UnboundLocalError |
| 8 | Word COM precisa Print View + Repaginate + espera | TOC desatualizado |
| 9 | Heading em-dash (—), nunca vírgula | Parsing quebrado |
| 10 | Processar caps sequencialmente, nunca em paralelo | Consistência |
