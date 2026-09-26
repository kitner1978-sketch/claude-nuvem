# Projeto Livro: leia primeiro

**Cópia de transporte feita em 24/09/2026** a partir do Mac do autor, para continuar o trabalho em outro computador. Este arquivo é carregado automaticamente pelo `CLAUDE.md` da raiz. Tudo o que o Claude Code do Mac sabia sobre o projeto está aqui ou nos arquivos para os quais ele aponta.

---

## 1. O que é

**"Direito Previdenciário: Teoria e Prática nos Juizados Especiais Federais"**, de Claudio Kitner e Luiz Bispo da Silva Neto. Público: advogados previdenciaristas e magistrados de JEF.

- **Luiz Bispo da Silva Neto** é o usuário do Claude Code: juiz federal, professor da Escola da REJUFE. Veja `memoria/regras_de_trabalho_do_usuario.md`.
- **Claudio Kitner** é o coautor. Suas observações de 09/06/2026 estão em `output/observacoes_coautor_09jun.md`.
- **Ingrid Moura** é a revisora. Em 18/09/2026 devolveu o livro revisado em Word, com 21 comentários (`anexos/revisora_ingrid/`).
- **Editora Thoth.** O Parecer 2829, de 16/07/2026, aprovou o projeto com ajustes. As normas, as dúvidas e a carta de 19/07/2026 estão em `output/auditoria/conformidade_normas_thoth.md`, `output/auditoria/duvidas_editora_thoth.md` e `output/carta_editora_thoth.docx`. **Não há registro no projeto de resposta da editora a essa carta.**

**Estrutura:** 6 partes e 23 capítulos, com cerca de 383 mil palavras. Em Word/PDF A5 são ~1.360 a 1.370 páginas.

| Parte | Capítulos |
|---|---|
| I. Fundamentos do RGPS | 1 Evolução histórica e princípios · 2 Segurados e dependentes · 3 Carência e qualidade de segurado · 4 Custeio · 5 Tempo de contribuição |
| II. Benefícios por incapacidade | 6 Aposentadoria por incapacidade permanente · 7 Auxílio por incapacidade temporária |
| III. Aposentadorias programadas | 8 Especial · 9 Rural · 10 Programada e por idade urbana · 11 Por tempo de contribuição e transição · 12 Pessoa com deficiência |
| IV. Pensões, auxílios e BPC | 13 Salário-maternidade · 14 Auxílio-reclusão · 15 Auxílio-acidente e salário-família · 16 Cálculo (SB e RMI) · 17 Revisões · 18 BPC/LOAS · 19 Pensão por morte |
| V. Temas transversais | 20 Acumulação · 21 Decadência, prescrição e coisa julgada |
| VI. Processo nos JEFs | 22 Processo administrativo · 23 Competência e procedimento no JEF (+ Epílogo da obra) |

**Fase atual:** pré-publicação, na **revisão final antes do envio do Word à editora**. O trabalho foi **pausado em 22/09/2026** no meio de uma conferência de legislação, por decisão do autor, para poupar cota.

---

## 2. Como o projeto funciona hoje

- **Fonte única do texto:** `output/rascunhos/cap_XX_rascunho.md`, os 23 arquivos terminados em `_rascunho.md`. **Não** edite `output/capitulos/`, que é export antigo, nem `*.formatado.md` ou `*_parte_a/b.md`, que são restos do pipeline.
- **Formato dos capítulos:** Markdown com frontmatter YAML e a linha `## Capítulo N — Título`. O travessão dessa linha é exigido pelo gerador. Há também boxes `::: box-atencao | box-jurisprudencia | box-pratica | box-quadro … :::`, callouts do Obsidian `> [!warning]`, `> [!tip]`, e o fecho `### Referências`, com `#### Legislação`, `#### Jurisprudência` e `#### Doutrina`.
- **Gerador do livro:** `scripts/gerar_livro_pdf.py`, função `create_unified_docx`. Ele monta capa, página de rosto, ficha catalográfica, Apresentação, abreviaturas, sumário, as 6 partes, os 23 capítulos, o **Epílogo**, as **Referências consolidadas**, o **Índice remissivo** e o **Sobre os Autores**. Usa as funções de `scripts/md_to_docx.py`: `parse_markdown`, `strip_citations`, boxes, tabelas e listas. A identidade visual está em `scripts/design_code.py` (EB Garamond, A5, dourado #B78B37).
- **Texto que não está em Markdown:** Apresentação, Sobre os Autores e ficha catalográfica estão escritos **dentro de `gerar_livro_pdf.py`**, como listas de strings Python. O ISBN está como "[a definir]", porque cabe à editora.
- **Referências:** o gerador retira o bloco `### Referências` de cada capítulo e junta tudo numa lista única no fim do livro, a pedido da Thoth. Se um capítulo perder esse título, as referências saem impressas no meio do texto. Isso já aconteceu no cap. 22 e foi corrigido em 22/09.
- **Citações no corpo:** `strip_citations` **remove do DOCX as citações autor-data** entre parênteses e as orações do tipo "como ensinam Castro e Lazzari (2025),". Esse comportamento já existia antes de setembro. Desde 21/09 ele preserva a atribuição de citações literais entre aspas (60 casos). ⚠️ A carta à editora diz que "a obra está integralmente em autor-data"; **convém o autor confirmar** se o Word enviado deve mesmo sair sem as citações no corpo.
- **Pipeline de agentes:** descrito no `CLAUDE.md` da raiz. Serviu para **redigir** os capítulos em maio de 2026 e hoje é histórico. `state/pipeline_state.json` também está defasado: a fonte de verdade sobre o andamento é este arquivo, o `CHANGELOG.md` e o `git log`.
- **Bases oficiais de jurisprudência** em `jurisprudencia/` (13 GB), baixadas por `scripts/baixar_stj.py` e `baixar_tnu.py`. Detalhes em `ambiente/MCP_E_FERRAMENTAS.md`.

### Como gerar o livro

Na raiz desta cópia:

```bash
export PYTHONDONTWRITEBYTECODE=1
cd scripts
python3 -c "import sys; sys.path.insert(0,'.'); from gerar_livro_pdf import create_unified_docx; create_unified_docx('../output/livro_completo - DD de mmm AA.docx')"
```

A geração leva uns 7 segundos. `python3 gerar_livro_pdf.py` gera `output/livro_completo.docx` e tenta o PDF (Word no Windows ou LibreOffice). Dependências em `ambiente/requirements.txt`. No exFAT, `PYTHONDONTWRITEBYTECODE=1` evita espalhar `__pycache__`.

### Como conferir

```bash
# remissões internas ("v. seção 3.8"): o script tem caminho D:\ fixo; rode assim
python3 -c "import sys; sys.path.insert(0,'scripts'); from pathlib import Path; import verificar_refs_cruzadas as m; m.RASCUNHOS_DIR=Path('output/rascunhos'); m.main()"
# o mesmo padrão serve para verificar_valores e verificar_citacoes_refs
python3 _continuidade/ferramentas/check_teses.py            # tese entre aspas × tese oficial do mesmo Tema
python3 _continuidade/ferramentas/conferir_aspas_reverso.py # todo trecho entre aspas × todas as teses oficiais
```

Em 22/09 havia 194 remissões internas, todas válidas.

**Avisos que os conferidores ainda dão em 24/09, e o que são.** Se aparecerem só estes, não há novidade:

- `check_teses.py` dá 3 avisos, todos **falsos positivos**. As aspas próximas ao número do Tema são de outro texto:
  - cap. 14, linha 346 (Tema 896): texto do art. 80, § 7º, da Lei 8.213;
  - cap. 5, linha 262 (Tema 327): Súmula 6/TNU;
  - cap. 15, linha 277 (Tema 269): expressão entre aspas.
- `conferir_aspas_reverso.py` dá 5 avisos:
  - cap. 18, linha 145: art. 20, § 3º, da LOAS;
  - cap. 23, linha 167: pedido de petição;
  - cap. 9, linha 368: Súmula 14/TNU;
  - cap. 10, linha 578: texto do art. 49;
  - cap. 9, linha 354: Súmula 577/STJ **truncada**. Este é o único real; ver o Módulo 4.

---

## 3. Mapa de caminhos

Relatórios e memórias citam caminhos do Mac. Correspondência:

| No Mac original | O que é | Nesta cópia |
|---|---|---|
| `/Volumes/2tb/Projeto Livro/` | **cópia mais recente** (fonte desta) | a raiz `projeto_livro/` |
| `/Volumes/seagate/Projeto Livro/` | retrato de 10/06/2026, defasado | não copiado. Os relatórios de set/2026 que estavam lá foram para `_continuidade/relatorios/` |
| `/Volumes/Macintosh NVMe/Projeto Livro/` | retrato de 10/05 (17 caps) + frente de Instagram, com histórico git **sem relação** | `_continuidade/anexos/nvme_retrato_mai2026_e_instagram/` (sem `.git`) + `nvme_projeto_livro_historico_git.bundle` (histórico completo: `git clone <bundle> pasta`) |
| `~/Downloads/livro_completo - 18 de set 26.docx` | DOCX da revisora | `_continuidade/anexos/revisora_ingrid/` |
| `~/.claude/projects/-Volumes-seagate-Projeto-Livro/memory/` | memória do Claude Code | `_continuidade/memoria/projeto_livro/` |
| `/private/tmp/.../scratchpad/` | ferramentas e retratos das sessões de 21–22/09 | `_continuidade/ferramentas/` e `_continuidade/snapshots/` |

---

## 4. Estado em 24/09/2026

### Git

- Branch `master`. Último commit: `0cb45ea` (20/07/2026, conformidade Thoth).
- **Nada de setembro foi commitado.** `git diff` mostra o trabalho de 21 e 22/09 nos 23 capítulos e em `scripts/md_to_docx.py` e `scripts/gerar_livro_pdf.py`.
- Os outros arquivos marcados `M` (`state/*.json`, `reviews/fase0_scripts/*.txt`, `output/verif*.md`) são **só fim de linha** (CRLF). `git diff --ignore-cr-at-eol` confirma: não há mudança de conteúdo.
- Não rastreados: os DOCX e PDF datados, a carta e a proposta para a editora, as observações do coautor e `_continuidade/`. O `CLAUDE.md` da raiz também recebeu, nesta cópia, um bloco de retomada no topo.
- `core.filemode=false`. O exFAT não guarda permissões, então o git não acusa mudança de modo.

### Último entregável

**`output/livro_completo - 22 de set 26.docx`**. Abre sem erro, tem 23 capítulos, ~383 mil palavras e o Epílogo como seção própria. Não foi gerado PDF.

### Linha do tempo resumida

| Data | O que aconteceu |
|---|---|
| mai/2026 | Redação dos 23 caps. pelo pipeline de agentes; revisões v10–v12 (~126 correções); v13 conferiu Temas contra bases oficiais (55 correções) |
| 31/05–10/06 | Polimento anti-IA e ABNT; blindagem jurídica; correção de tabelas em boxes; ajustes pedidos pelo coautor |
| 16–20/07 | Parecer da Thoth; conformidade com as normas (títulos em caixa de frase, ABNT 2023, referências consolidadas, Introdução e Conclusão sem número); revisão semântica; Apresentação e Sobre os Autores. DOCX de 19/07 |
| 25/08–11/09 | Revisão da Ingrid no DOCX de 19/07 (390 edições, 21 comentários) |
| **21/09** | Revisão dirigida: erros de direito corrigidos, entre eles a cronologia do art. 27-A invertida, uma "Súmula 74 da TNU" que não existe, CEBAS pela lei revogada e 11 teses parafraseadas entre aspas. Edições da Ingrid transportadas para o Markdown. Gerador corrigido. Detalhe em `relatorios/revisao_set2026_aplicada.md` |
| **22/09** | Conferência de legislação por 8 agentes, interrompida por cota. **Módulo 1** aplicado: 11 divergências graves (caps. 4, 12, 13, 15, 18, 20), entre elas dois parágrafos **inexistentes** do art. 24 da EC 103/2019 citados no cap. 20. Detalhe na seção 8 de `relatorios/revisao_set2026_aplicada.md` |

---

## 5. O que falta, por módulo

O autor pediu para **trabalhar por módulos curtos**, um por rodada, **sem vários agentes em paralelo**. Em 21/09, 8 agentes simultâneos estouraram o limite semanal da conta. A cota de 5 horas também é apertada.

### Módulo 2: aplicar as divergências MÉDIA e BAIXA já apuradas

- Estão em `relatorios/legislacao_22set/achados_g1.md` a `achados_g8.md`: **62 MÉDIA e 42 BAIXA**.
- Cobrem só os caps. **1, 2, 4, 6, 7, 9, 12, 13, 15, 16, 18, 20 e 21**. Os agentes foram parados no meio.
- As 11 ALTA já estão aplicadas: estão marcadas como "gravidade ALTA" nos relatórios e **não devem ser reaplicadas**.
- Método: para cada item, **reconferir o texto literal na fonte** (os agentes erram) e só depois aplicar com `ferramentas/patchlib.py`.
- ⚠️ **Os números de linha dos relatórios são de 22/09, antes do Módulo 1.** Nos caps. 4, 12, 13, 15, 18 e 20 localize o trecho pelo texto, não pela linha.

### Módulo 3: conferir a legislação dos 10 capítulos restantes

- Capítulos **3, 5, 8, 10, 11, 14, 17, 19, 22 e 23**, justamente os de maior densidade normativa.
- As frases candidatas já foram extraídas em `relatorios/legislacao_22set/cap_XX.txt` (807 no total). O protocolo de conferência está em `relatorios/legislacao_22set/INSTRUCOES.md`.
- Faça no máximo 2 capítulos por rodada.
- Exija que o relatório seja gravado **a cada capítulo concluído**.
- Os caminhos nas INSTRUCOES apontam para o Mac. Ajuste para esta cópia.

### Módulo 4: fechar e gerar o arquivo da editora

- Gerar o DOCX final e, se houver Word ou LibreOffice, o PDF de conferência.
- Pendências conhecidas a resolver antes do envio:
  - **ADI 6.309:** conferir se o acórdão foi publicado e se houve modulação. O livro diz que "até o fechamento desta edição" não havia acórdão. Os dados do livro (j. 03/06/2026, 6×5, Barroso relator originário) **estão corretos**.
  - **Tema 1.157/STJ:** a tese está descrita sem aspas, porque o acórdão ainda não havia sido publicado. Transcrever a tese oficial quando sair.
  - **Tema 1.271/STF** (menor sob guarda), **modulação da "vida toda"** e **ADI 7.873** (EC 136/2025): o livro os dá como pendentes. Confirmar.
  - **Comentário 18 da revisora:** Súmula 149/STJ duplicada no quadro do cap. 13.
  - **Súmulas entre aspas:** 36 foram inventariadas em `ferramentas/dados/sumulas_citadas.json`, mas só seis tiveram o texto conferido no enunciado oficial (TNU 24, 32, 47, 74 e 75; STJ 272). A base `jur-rag` traz o enunciado de cada uma: buscar "Súmula STJ 577 …" ou "Súmula TNU 47 …".
  - **Achado de 24/09, não corrigido:** a **Súmula 577/STJ** aparece entre aspas **sem o final "colhida sob o contraditório"** no cap. 9 (linhas 176, 179 e 354). O texto oficial é: "É possível reconhecer o tempo de serviço rural anterior ao documento mais antigo apresentado, desde que amparado em convincente prova testemunhal colhida sob o contraditório." No cap. 5 (linha 256) a citação está correta.
  - **Citações literais de doutrina e de lei entre aspas:** ainda **não foram conferidas** contra as obras.
  - **6 fichas de pesquisa da TNU** existem só no retrato do NVMe: Temas 73, 174, 208, 213, 301 e a Reclamação 0000302-22. Estão em `anexos/nvme_retrato_mai2026_e_instagram/pesquisa/jurisprudencia/`. Integrar ao `pesquisa/` se o autor quiser.

### Módulo 5: commit

Nada foi commitado. Commit **só com autorização do autor**. Sugestão de divisão:

1. correções de 21/09;
2. correções de 22/09;
3. gerador;
4. `_continuidade/`.

### Decisões que são do autor, não do Claude

1. **Grafia "salário-mínimo" com hífen.** Foi adotada em todo o livro seguindo a revisora, com a grafia original preservada dentro de citações literais. A lei escreve sem hífen. A reversão é global e simples.
2. **Numeração de Introdução e Conclusão.** A revisora renumerou ("1.1", "3.9"), mas a Thoth pediu sem número. Hoje está sem número.
3. **Citações autor-data no corpo do DOCX.** Ver seção 2: o gerador as remove.
4. **Declaração de uso de IA** exigida pela Thoth (item 6.1 do parecer). A carta de 19/07 traz uma redação. Confirmar se foi enviada e em que formato.

---

## 6. Regras de trabalho (fixadas pelo autor, valem sempre)

1. **Toda afirmação jurídica é conferida na fonte primária** antes de entrar no texto: lei no texto consolidado, Tema no registro oficial, súmula no enunciado oficial. **Quem confere nunca é quem escreveu.** Precedente sem ficha conferida é descartado.
2. **O que está entre aspas precisa ser literal.** Paráfrase vai sem aspas. Tese se cita pelo **registro do Tema**, nunca pela ementa de um julgado que a aplica.
3. Antes de escrever sobre matéria afetada, **conferir se o repetitivo já foi julgado e se houve modulação**. O campo "Tese firmada" das bases às vezes repete o título do tema.
4. **Escrita anti-IA:** travessões e ponto-e-vírgula no mínimo; nada no texto final pode revelar produção por IA. Exceções e detalhes em `memoria/projeto_livro/escrita-anti-ia.md`. Skills `avoid-ai-writing` e `humanizar` em `ambiente/skills/`.
5. **Corrigir no Markdown, nunca no Word.** O Word é regerado; correção feita nele se perde.
6. **Trabalho sequencial e por módulos.** Sem rajada de agentes paralelos.
7. **Leitura é livre; escrita externa exige autorização** (commit, envio à editora, publicação).

---

## 7. Armadilhas já conhecidas

Todas elas já causaram erro real neste projeto.

- **Três cópias do projeto** existiam no Mac. A do seagate parecia "a boa" e estava 10 commits atrás. Esta cópia vem da certa, a do 2tb.
- **Recorte de RAG que começa no meio de frase** pertence a outro item. Em 21/09 o final de um item do Informativo STF 1220 foi lido como relator e data da ADI 6.309, e gerou um "erro" que não existia. O engano foi retirado. A memória do livro irmão (`memoria/projeto_irmao_aposentadoria_especial/adi-6309-idade-minima.md`) tinha o mesmo engano e recebeu nota de correção.
- **Edição em lote sem retrato:** a ferramenta de transporte das edições da revisora truncou 3 capítulos. O dano foi recuperado porque havia cópia feita minutos antes. Sempre copie antes e compare linhas e bytes depois.
- **Relatório de agente "completo"** pode cobrir só metade dos capítulos. Confira as seções por capítulo.
- **"Verificado em fonte oficial"** no `pipeline_state.json` pode ser anterior à fonte. A ADI 6.309 foi marcada como verificada em 07/06, mas o Informativo é de 16/06.
- **Base oficial de Temas:** teses recém-julgadas aparecem como "*Aguardando a publicação do acórdão*" e às vezes o título está no lugar da tese.
- **planalto.gov.br** recusa conexões automatizadas com frequência. A Câmara (`www2.camara.leg.br/legin/...`) tem a publicação original.
- **Arquivos `._*` no exFAT:** o macOS os cria ao copiar para este disco. Dentro de `.git` eles atrapalham. Limpar com `dot_clean -m .` (Mac) ou apagando os `._*` de 4 KB.
- **Fim de linha:** o projeto nasceu no Windows. Grave os capítulos em **UTF-8 com LF** (`patchlib.py` já faz isso).

---

## 8. Índice desta pasta `_continuidade/`

| Pasta/arquivo | Conteúdo |
|---|---|
| `LEIA_PRIMEIRO.md` | este arquivo |
| `relatorios/revisao_set2026_varredura.md` | revisão dirigida de 21/09: achados, métodos, o que foi retirado |
| `relatorios/revisao_set2026_aplicada.md` | **tudo o que foi aplicado em 21 e 22/09**, com tabelas por capítulo (seção 8 = Módulo 1) |
| `relatorios/legislacao_22set/` | protocolo (`INSTRUCOES.md`), frases candidatas por capítulo e os 8 relatórios de divergências |
| `relatorios/validadores_22set/` | saída dos validadores do projeto em 21–22/09 |
| `memoria/` | memória do Claude Code do Mac + regras do usuário (ver o README) |
| `ferramentas/` | `patchlib.py`, conferidores de teses, varredor, dados das comparações (ver o README) |
| `snapshots/rascunhos_fim_21set/` | texto do DOCX de 21/09, para comparar com o de 22/09 |
| `anexos/revisora_ingrid/` | DOCX de 18/09 da revisora + `comentarios_ingrid.md` (os 21 comentários, o trecho e a situação de cada um) |
| `anexos/nvme_retrato_mai2026_e_instagram/` | retrato de maio + a frente de Instagram (`HANDOFF_SESSAO.md` descreve tudo: posts, geradores de cards e Reels, normas do CNJ para magistrado em rede social, método de verificação) |
| `anexos/nvme_projeto_livro_historico_git.bundle` | histórico git completo daquele retrato |
| `ambiente/MCP_E_FERRAMENTAS.md` | servidores de pesquisa usados, como substituí-los, skills e dependências |
| `ambiente/skills/` | skills `avoid-ai-writing`, `humanizar`, `jur-rag`, `pertinencia` (copiar para `~/.claude/skills/`) |
