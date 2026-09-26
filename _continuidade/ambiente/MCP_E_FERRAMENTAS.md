# Ambiente: servidores MCP, skills e dependências

O trabalho de revisão depende de **conferir cada afirmação jurídica em fonte**. No Mac original, isso era feito por servidores MCP de pesquisa. Nenhum deles vai junto nesta cópia: rodam a partir de bases de centenas de GB no disco `2tb` ou num servidor da rede Tailscale. Este arquivo diz o que cada um fazia e como substituí-lo em outro computador.

## Servidores MCP usados no livro

| Nome no Claude Code | O que consulta | Como rodava no Mac original | Em outro computador |
|---|---|---|---|
| `legislacao` | Legislação federal consolidada (Planalto/normas.leg.br): texto vigente, com as anotações "(Incluído pela…)", "(Redação dada pela…)", "(Revogado pela…)". **Foi a fonte de todas as correções de legislação.** | stdio: `/Volumes/2tb/jurisprudencia/.ragenv/bin/python /Volumes/2tb/Planalto/legis_mcp.py` | Não portátil. Substituto: WebFetch no planalto.gov.br (o texto compilado de cada lei traz as mesmas anotações). O site às vezes recusa conexão (ECONNRESET); a Câmara (`www2.camara.leg.br/legin/...publicacaooriginal...`) serve como alternativa para a redação original |
| `informativos` | Informativos do STF e STJ + teses de Repercussão Geral e Repetitivos | stdio: `.../informativos/info_mcp.py` | Não portátil. Usar `jur-rag` (abaixo), que tem o mesmo corpus de informativos |
| `jur-rag` | Dois corpora: jurisprudência (TRF5, TRs, STJ, STF, TNU; 20 milhões de trechos) e informativos STF/STJ; inclui os **enunciados oficiais de súmulas** como documentos próprios (buscar "Súmula TNU 47 …" traz o texto e a situação: vigente/cancelada) | HTTP: `http://100.65.53.53:8765/mcp` (nó `ia-rag`, só pela Tailscale) | **Portátil se o outro computador estiver na mesma rede Tailscale.** Configuração abaixo |
| `jurisprudencia_tnu` | Inteiro teor de julgados da TNU | stdio: `.../rag_pack/scripts/tnu_mcp.py` | Não portátil. Usar `jur-rag` com `tribunal="TNU"` |
| `jurisprudencia_stf` | Inteiro teor de acórdãos do STF (2016–2025) | stdio: `.../rag_pack/scripts/stf_mcp.py` | Não portátil. Usar `jur-rag` e o portal do STF |
| `jurisprudencia` | Base unificada de jurisprudência | stdio: `/Volumes/2tb/RAG/rag_mcp.py` | Não portátil. Usar `jur-rag` |

Os servidores `pje`, `pje-gw`, `pje-tr`, `jurisprudencia_7turma`, `jurisprudencia_sentencas` e `jurisprudencia_trpe` existem no Mac, mas **não têm relação com o livro**.

### Configurar o `jur-rag` no outro computador

Com o computador na mesma rede Tailscale do Mac, em um terminal:

```bash
claude mcp add --transport http jur-rag http://100.65.53.53:8765/mcp
```

Instruções de uso do servidor: `skills/jur-rag/SKILL.md` (a regra principal é: buscar ≠ ler o inteiro teor).

### Sem nenhum MCP: o que ainda funciona offline

O repositório traz as **bases oficiais baixadas** em `jurisprudencia/` (13 GB):

- `jurisprudencia/stj/precedentes/temas.csv` — 1.441 Temas repetitivos do STJ, com tese firmada, datas e situação.
- `jurisprudencia/stf/temas_repercussao_geral_stf.xlsx` — 1.464 Temas de Repercussão Geral do STF, com tese, relator e data.
- `jurisprudencia/tnu/temas_representativos_tnu.json` — ~396 Temas representativos da TNU.
- `jurisprudencia/stj/espelhos.sqlite` — espelhos de acórdãos do STJ (usado por `scripts/verificar_resp.py`).
- `jurisprudencia/stj/integras-de-decisoes-terminativas-e-acordaos-do-diario-da-justica/` — 12 GB de íntegras; nenhum script de conferência usa, só o de download (`scripts/baixar_stj.py`).

Os conferidores `../ferramentas/check_teses.py` e `../ferramentas/conferir_aspas_reverso.py` usam apenas as três primeiras e rodam sem internet.

**Limite dessas bases:** a coluna de tese às vezes repete o título do tema, e teses julgadas há pouco aparecem como "*Aguardando a publicação do acórdão*" (caso do Tema 1.157/STJ). Nesses casos, conferir no portal do tribunal.

## Skills copiadas (`skills/`)

| Skill | Para quê | Como instalar |
|---|---|---|
| `avoid-ai-writing` | Auditoria e reescrita de "marcas de IA" em português (critério adotado pelo autor) | copiar a pasta para `~/.claude/skills/` |
| `humanizar` | Outra passada de naturalização de texto | idem |
| `jur-rag` | Manual de uso do servidor `jur-rag` | idem |
| `pertinencia` | Usada na frente de Instagram (checagem de pertinência de conteúdo) | idem |

## Dependências para gerar o livro

```bash
pip install -r requirements.txt
```

- Python 3.12 (testado com 3.12.3), `python-docx` 1.2.0, `lxml`, `PyYAML`, `openpyxl` 3.1.5.
- **DOCX:** puro Python, roda em qualquer sistema (ver `../LEIA_PRIMEIRO.md`, seção "Como gerar o livro").
- **PDF:** `scripts/gerar_livro_pdf.py` converte o DOCX por automação do Microsoft Word **só no Windows** (`win32com`, pacote `pywin32`, ou via PowerShell) ou, em qualquer sistema, pelo LibreOffice (`soffice --headless`), se estiver instalado. A editora pediu o arquivo em **Word**; PDF é só para conferência.
- Fontes usadas na diagramação: **EB Garamond** e **Noto Sans** (Google Fonts). Sem elas instaladas, o Word substitui e a paginação muda.
