# Handoff de sessão — Projeto Livro + Instagram

**Documento de restauração.** Escrito para que outra conta/sessão retome o trabalho sem
depender do histórico da conversa original.

- **Vault:** `/Volumes/Macintosh NVMe/Projeto Livro` (git, branch `main`)
- **Período coberto:** 27 a 29 de julho de 2026
- **Commits da sessão:** de `e291d8d` a `abf6a74` (12 commits)
- **Autor/usuário:** Luiz Bispo da Silva Neto — **Juiz Federal**, professor da Escola da REJUFE,
  coautor (com Claudio Kitner) de *Direito Previdenciário: Teoria e Prática nos Juizados
  Especiais Federais*

---

## 1. Ponto de partida e o que a sessão virou

O pedido inicial foi de **consultoria de Instagram**: o perfil tinha ~500 seguidores e o
objetivo declarado era "decuplicar" para vender livro e cursos. Durante a conversa a sessão
se desdobrou em três frentes que hoje estão entrelaçadas:

1. **Frente Instagram** — estratégia, verificação jurídica, identidade visual, fábrica de
   produção de posts, publicação assistida.
2. **Frente livro** — auditoria do vault, git, fila de aprovação, fichas novas de
   jurisprudência (a conferência feita para o Instagram achou erros que afetam capítulos).
3. **Frente método** — a descoberta, no meio do caminho, de que o método de citação usado
   até então (ler ementa e trecho de voto, em vez do registro do tema) produz erro
   sistemático. Isso vale para o livro tanto quanto para os posts.

> [!warning] Fato central para quem retomar
> O usuário é **magistrado**, não advogado. Toda decisão editorial passa pela
> **Resolução CNJ nº 305/2019**, não pelo Provimento da OAB. Ver seção 2.

---

## 2. Moldura normativa — Resolução CNJ nº 305/2019

Verificada em fonte oficial (`atos.cnj.jus.br/atos/detalhar/3124`) durante a sessão.
**Artigos conferidos literalmente:** art. 3º, parágrafo único; art. 4º, incisos I, IV, V, VI
e § 2º. **Não conferidos:** incisos II e III do art. 4º — pendência aberta.

| Dispositivo | Conteúdo | Efeito no projeto |
|---|---|---|
| art. 3º, § único | "É estimulado o uso educativo e instrutivo das redes sociais por magistrados, para fins de divulgar publicações científicas, conteúdos de artigos de doutrina, conhecimentos teóricos, estudos técnicos..." | **Verde.** Conteúdo doutrinário é incentivado, não apenas tolerado. É a base de toda a linha editorial. |
| art. 4º, I | Vedado opinar sobre processo pendente ou emitir juízo depreciativo sobre decisões — **ressalvados obra técnica e magistério** | Regra prática: **falar do precedente, nunca do processo.** |
| art. 4º, IV | Vedado "patrocinar postagens com finalidade de autopromoção ou intuito comercial" | **Zero tráfego pago.** Restrição estrutural: todo crescimento é orgânico. |
| art. 4º, V e VI | Vedado patrocínio e associação de imagem a marca | Sem publi, sem parceria comercial. |
| art. 4º, § 2º | Divulgação de obra técnica própria e de cursos em que atua como professor **não** é vedada, "desde que não caracterizada a exploração direta de atividade econômica lucrativa" | Abrigo para livro e cursos — **desde que a venda corra pela editora/Escola**, não por ele. A estrutura atual (inscrição por `escolarejufe2026@gmail.com`) já satisfaz isso. |

Complementos: CF art. 95, § único, I (magistério é a exceção permitida); LOMAN art. 36, I
(vedado exercer comércio).

**Decisão editorial derivada:** posts doutrinários levam só `@luiz.bispo.12` no rodapé;
identificação institucional fica reservada a posts de divulgação de curso, que são os que
dependem do § 2º.

---

## 3. Linha editorial — decisões e por quê

Três viradas aconteceram na sessão, todas por pedido do usuário. Quem retomar deve
respeitá-las:

**(a) De tático para doutrinário.** A primeira versão ensinava advocacia ("o erro que
derruba seu pedido", "o que o INSS não cita"). O usuário pediu registro doutrinário. Além
de melhor, é mais seguro: ensinar tática a um lado, vindo de juiz, se aproxima da borda do
art. 4º, I; exposição dogmática está no centro do art. 3º, § único. Ganho lateral: cada post
vira parágrafo de capítulo.

**(b) De vídeo falado para carrossel/Reel de cards.** O usuário não quer aparecer em câmera.
Solução: cards tipográficos, que servem ao carrossel **e** viram Reel animado pelo mesmo
gerador.

**(c) Linguagem.** Duas rodadas de correção do usuário. Ele rejeitou:
- inflação acadêmica ("O fundamento, contudo, não é literalista", "sob pena de", "por via oblíqua");
- metáforas esticadas — a metáfora da "porta" foi criada e usada em três cards até quebrar em
  "Por onde a porta não se atravessa", que ele apontou como ruim.

**Regra que ficou:** cada título **descreve o que está no card**, não comenta o card.
"Tirar do grupo e contar mesmo assim" em vez de "Por onde a porta não se atravessa".
A skill `avoid-ai-writing` foi usada uma vez e é o critério de referência.

**Formato do post doutrinário (spec de 8–9 cards):**
capa (pergunta) → o problema → hipótese concreta → base normativa → tese, item I →
desdobramento → tese, item II → limites → fecho (síntese + precedentes + hashtags).

Regras fixas: sem isca de engajamento ("comenta aí"); sem instrução tática; fecho é questão
em aberto ou síntese; **máximo 4 hashtags**; terceira pessoa.

---

## 4. Identidade visual

Consolidada depois de o usuário rejeitar a primeira versão ("code design com cara de IA" —
era azul-marinho + dourado + sans centralizado, o preset genérico).

| Elemento | Valor |
|---|---|
| Papel | `#EDE6D8` |
| Tinta | `#17150F` |
| Vermelhão (acento) | `#6B2318` |
| Painel de destaque | `#E2D8C3` |
| Claro (sobre fundo escuro) | `#C79A80` |
| Serifa | EB Garamond (fallback Georgia) |
| Sans | Inter (fallback Helvetica) |
| Formato card | 1080×1350 (4:5) |
| Formato Reel | 1080×1920, card a 92% erguido (zona segura do player) |

Dispositivos que definem a assinatura: faixa vermelha no topo com o assunto; **numeral
fantasma** do card em corpo 420 a 7% de opacidade; rodapé fixo com filete + `@LUIZ.BISPO.12`
+ paginação; card de fecho invertido (fundo escuro). Cinco arquétipos de card em vez de
clones: capa, lista, citação (aspa em corpo 200), painel, fecho.

> [!info] Decisão pendente
> O `#6B2318` foi adotado como cor do projeto na falta de definição da capa do livro. Se a
> obra tiver cor própria, trocar — e a troca é de uma constante no gerador.

---

## 5. A fábrica — como produzir um post

Dois scripts. **Nada é feito à mão.**

### `scripts/gerar_cards.py`
```bash
python3 scripts/gerar_cards.py marketing/posts/post_NN_tema/spec.json --png [--camadas]
```
- Lê um `spec.json` e emite os cards.
- `--png` renderiza via **Chrome headless** (`--window-size=1080,1350 --screenshot`).
  ImageMagick **não** serve: não resolve as fontes do SVG.
- `--camadas` emite `card_N_bg` (papel, faixa, numeral, rodapé) e `card_N_fg` (texto,
  fundo transparente) — necessários para o Reel.
- Saída: PNGs finais em `publicar/{slug}_card_NN.png`; SVGs e camadas em `producao/`.

### `scripts/gerar_reel.py`
```bash
python3 scripts/gerar_reel.py marketing/posts/post_NN_tema [nome_saida.mp4]
```
- Requer que os cards tenham sido gerados com `--camadas`.
- Movimento: **pan lateral alternado** no fundo (rostrum camera) + zoom fixo 1,055; o texto
  **assenta** por cima (desliza 14 px e desvanece em 0,9 s) — exceto no card 1, que abre
  completo no primeiro frame (decisão: ganhar o primeiro segundo).
- **Duração automática:** `2,6 s + caracteres/17`, limitada a 5–11 s. `"dur"` no spec
  sobrescreve. Foi assim que se resolveu a queixa "não consigo ler".
- **`reel_cards` no spec** seleciona um subconjunto (1-indexado). O Reel leva a espinha do
  argumento; o carrossel leva o desenvolvimento completo. Sem isso o vídeo passaria de 80 s.
- Sem áudio de propósito — trilha entra na publicação, pela biblioteca licenciada do
  Instagram.
- Encoder: libx264, crf 22, preset fast (crf 18 gerava 136 MB; hoje ~10–13 MB).

### Estrutura por post (obrigatória)
```
marketing/posts/post_NN_tema/
├── spec.json          ← fonte de tudo; campo "slug" nomeia os arquivos
├── legenda.txt        ← legenda pronta (≤2200 caracteres)
├── publicar/          ← SÓ o que sobe: postNN_tema_card_01.png … + _reel.mp4
└── producao/          ← interno: SVGs e camadas _bg/_fg (fora do git)
```
Essa estrutura nasceu de um erro real: três pastas com `card_1.png` idênticos causaram
confusão no upload. **Na hora de publicar, abrir apenas `publicar/`.**

### Dependências do ambiente
- `ffmpeg` (instalado via `brew install ffmpeg` durante a sessão)
- Google Chrome em `/Applications/Google Chrome.app` (usado headless)
- ImageMagick (`magick`) — só para folhas de contato
- Python 3 (stdlib apenas)

---

## 6. Método de verificação jurídica — a lição mais importante

O usuário exigiu conferência de todos os precedentes antes de publicar. A conferência achou
**erros reais**, inclusive num roteiro que quase foi publicado com a assinatura dele.

### Erros encontrados e a causa comum

| Erro | O que era | Causa |
|---|---|---|
| Fundamento do "dever de alimentos" apresentado como *ratio* do Tema 73 | Estava no **voto vencido** de 0003636-52; o relator p/ acórdão registrou que a matéria era alheia à controvérsia | leitura de voto sem checar qual prevaleceu |
| "Reclamação 0000302-22" citada como PEDILEF | É **Reclamação**, classe diversa | metadado não conferido |
| "Questão de Ordem nº 20" atribuída à tese do rol taxativo | A QO 20 **existe**, mas é processual (retorno para adequação). A tese é do **Tema 73** | ementa citando QO junto da tese |
| Tema 208 e Tema 174 tratados como equivalentes | A TNU diz expressamente que o 208 "não se debruça sobre a técnica de aferição"; omissão de responsável técnico **se supre**, omissão de técnica de medição **não** | extrapolação de raciocínio |
| Reel 09 baseado em "ruptura definitiva" | **Tema 301** (2024) é alteração de interpretação e superou isso | não checar tema posterior |
| Tema 122/TNU dito "alinhado" ao STF | Diverge do **Tema 185/STJ** (relativa × absoluta) | leitura de segunda mão |

**Regra de método consolidada:**
1. Tese se cita pelo **registro do tema**, nunca por ementa de julgado aplicador.
2. Conferir **qual voto prevaleceu** antes de expor a razão de decidir.
3. Conferir a **classe processual** (PEDILEF ≠ PUIL ≠ Reclamação).
4. Temas homônimos entre tribunais: sempre qualificar (ex.: Tema 174 da TNU é ruído;
   Tema 174 do STF é auxílio-reclusão — o cap_14 cita o do STF corretamente).
5. Checar se há tema posterior que alterou a interpretação.

Onde o índice devolveu o **registro estruturado** do tema (Tema 73, Tema 327), não houve erro.

### Ferramentas usadas
MCPs `jur-rag` (`juris_rag_search`), `jurisprudencia_tnu` (`buscar_tnu`),
`jurisprudencia_stf`, `legislacao`. Para PDF de acórdão que veio binário via WebFetch:
extrair com `pypdf`/`PyPDF2` a partir do arquivo salvo em `tool-results/`.

---

## 7. Fichas de jurisprudência criadas

Em `pesquisa/jurisprudencia/`, no padrão do vault (frontmatter, callouts, wiki-links):

| Ficha | Conteúdo verificado |
|---|---|
| `TNU_Tema_73.md` | Piloto PEDILEF 2006.63.01.052381-5/SP. **Alcance temporal declarado**: questão submetida limitada ao período anterior à Lei 12.435/2011; tese fala do art. 20 "em sua redação original". Duas linhas internas (textual × solidariedade alimentar). Registro oficial grafa "12.453/2011" — erro material |
| `TNU_Reclamacao_0000302-22.md` | Rel. Ivanir Cesar Ireno Junior, 2021. "Vias transversas". **Parágrafo 19**: o que se veda não é o argumento da capacidade alimentar, é pular o argumento |
| `TNU_Tema_174.md` | Firmado em ED no PEDILEF 0505614-83.2017.4.01.8300, Rel. Sérgio de Abreu Brito, 21/03/2019. Marco 19/11/2003. Omissão da técnica **não** é suprível. Distinção do Tema 1.083/STJ (NEN) |
| `TNU_Tema_208.md` | Tese literal (2 itens). Marco: Decreto 2.172/1997 (05/03/1997). Omissão de responsável técnico **é** suprível |
| `TNU_Tema_213.md` | Piloto **PUIL 0004439-44.2010.4.03.6318/SP**, Rel. Fabio de Souza Silva — acórdão íntegro (42 p.) baixado do CJF e salvo em `pdf/TNU_Tema213_PUIL_0004439-44.pdf`. Itens I e II literais. Distinção do Tema 188 (contribuinte individual) |
| `TNU_Tema_301.md` | PEDILEF 5001265-87.2022.4.04.7127/RS, Rel. Paulo Roberto Parca de Pinho, 2024. **Alteração de interpretação** sobre descontinuidade rural |

**STF ARE 664.335 = Tema 555**, Rel. Min. Luiz Fux, Plenário, j. 04/12/2014 — duas teses
confirmadas literalmente. **Súmula 9 da TNU** — texto literal confirmado em três julgados.

---

## 8. Estado do Instagram

**Perfil `@luiz.bispo.12`** (dados de 29/07, ~17h30):
- **549 seguidores** (era 550 no início) · 1.168 seguindo · 11 posts
- Bio **aplicada** nesta sessão: `Juiz Federal | Professor da Escola da REJUFE` /
  `Precedentes previdenciários da TNU, STJ e STF`
- Campo **Nome ainda "Luiz B Neto"** — não aplicado (ver pendências)
- Conta **ainda pessoal** — sem Insights

### Publicados
| # | Data | Formato | Tema | URL |
|---|---|---|---|---|
| 01 | 27/07 (dom) | Carrossel 8 cards | BPC — grupo familiar, Tema 73 | `instagram.com/p/DbT58_EGTRU` |
| 02a | 29/07 (madrugada) | **Reel** 57 s, com trilha | Tempo especial — EPI, Tema 213 | `instagram.com/p/DbY_NFmTAeI` |

**Dois defeitos no Reel publicado, ambos editáveis pelo app:**
1. **A capa é o card 2** ("Um formulário sem contraditório"), não a capa com a pergunta.
   A miniatura é o que faz alguém parar — corrigir em Editar → capa.
2. **A legenda foi truncada** em `#direitoprevidenciário #te`. Faltam
   `#tempoespecial #TNU #EscolaREJUFE`. Colar de novo a partir de `legenda.txt`.

Observação: entrou um cartaz de curso (Módulo 5) entre 27 e 29/07, o que devolve o grid ao
padrão antigo e dilui a linha editorial nova.

### Prontos, não publicados
- **Carrossel do Tema 213** — 9 cards em `posts/post_02_epi_tema213/publicar/`, mesma legenda.
- **Carrossel do ruído (Súmula 9)** — 8 cards em `posts/post_03_ruido_sumula9/publicar/` +
  `legenda.txt`. Era para sexta, 31/07.

### Série em curso
`TEMPO ESPECIAL · SÉRIE 1 DE 3` → EPI (Tema 213) · `2 DE 3` → ruído (Súmula 9) ·
`3 DE 3` → metodologia (Tema 174, **a produzir**; ficha já conferida). Cada fecho anuncia o
próximo.

---

## 9. Diagnóstico estratégico (última análise da sessão)

O usuário observou que dois posts não renderam nenhum seguidor. A avaliação honesta:

**Dois posts em dois dias não rendem seguidores — isso é o esperado.** Mas há uma razão de
fundo que precisa orientar o próximo passo:

> Com 549 seguidores, **o algoritmo não é o motor, é o amplificador**. O Instagram entrega
> primeiro a uma fração da audiência existente e decide distribuir com base na reação dela.
> Dos 549, poucas dezenas são previdenciaristas. Conteúdo sobre Tema 213 entregue a essa base
> gera reação morna, e o algoritmo conclui corretamente que não vale distribuir.
> **Os primeiros mil seguidores de um perfil profissional quase nunca vêm do algoritmo; vêm
> de importar audiência que já se tem.**

**Ativo de distribuição não utilizado** (nada foi feito nesta direção):
- Alunos dos módulos da Escola da REJUFE — pessoas que pagaram R$ 1.500 para ouvi-lo sobre
  exatamente estes temas. A audiência mais qualificada possível.
- A lista de `escolarejufe2026@gmail.com` — todos que já escreveram perguntando de curso.
- Claudio Kitner (coautor) e a rede dele; publicação como **Colaboração**.
- Conta institucional da Escola da REJUFE.
- Colegas de JEF, AJUFE, REJUFE.

**Autocrítica registrada:** a sessão construiu fábrica de produção (geradores, specs, Reel
cinematográfico) e quase nada de distribuição. O gargalo nunca foi produzir.

**Próximo passo proposto e não executado:** escrever três textos de semeadura — recado aos
alunos dos módulos, pedido de compartilhamento à Escola, mensagem ao Kitner para publicar
como Colaboração.

---

## 10. Pendências

### Do usuário (celular, minutos)
- [ ] Campo **Nome** → `Luiz Bispo | Previdenciário` — único campo indexado pela busca do
      Instagram. Tentado em 26/07 pela web e **bloqueado por verificação de segurança**.
- [ ] Converter para **conta Profissional**, categoria Educação — destrava Insights. Sem
      isso não há como saber se um post alcançou 40 ou 4.000 pessoas, e nenhuma decisão de
      formato é possível.
- [ ] Corrigir **capa e legenda** do Reel publicado.
- [ ] Fixar o post 01 no topo do grid; decidir sobre arquivar fotos pessoais.
- [ ] Link na bio.

### De verificação jurídica (travam roteiros)
- [ ] **PEDILEF 1001528-59.2023.4.06.3810** — resultado proclamado. Tenho o voto do relator
      p/ acórdão propondo reafirmação, não o desfecho. **Está na legenda publicada do post 01.**
      Redação segura alternativa: "e voltou a ser proposta em 1001528-59".
- [ ] **Tema 369** (Reel 02 do calendário antigo) — não retornou do índice; há voto por
      interpretação restritiva em 0001882-94.2021.4.05.8500 contra o relator.
- [ ] **Tema 173, Tema 378, Súmulas 48 e 80** (Reel 10) — não retornaram do índice.
- [ ] **Tema 27 × Tema 627 do STF** — o mesmo enunciado aparece com os dois números em
      julgados diferentes. Resolver antes de citar.
- [ ] **Incisos II e III do art. 4º** da Resolução 305 — não lidos; o checklist de compliance
      declara isso.

### De produto
- [ ] **`marketing/calendario_editorial_90dias.md` está desatualizado** — foi escrito para
      Reels falados (22 menções a "Reel", 1 a "carrossel") e descreve blocos cronometrados de
      fala. Os roteiros 02 a 12 estão em formato inutilizável (registro tático antigo +
      formato de fala). Precisa ser reescrito para o formato de spec/carrossel.
- [ ] Semáforo dos roteiros antigos (seção 1-A do calendário): 04, 07, 12 verdes; 06, 08, 11
      parciais; 02, 03, 05, 09, 10 com erro ou não confirmados.
- [ ] **Hipótese 1 de melhoria do vídeo, não implementada:** revelar o texto **por blocos**
      dentro do card (título, depois corpo, depois citação), em vez do card inteiro de uma
      vez. Reservada para o post do Tema 174. Exige quebrar o `fg` em sub-camadas.
- [ ] Texto alternativo dos cards (acessibilidade — hoje são imagens de texto puro,
      ilegíveis para leitor de tela).
- [ ] Criar `spec.json` do post 01 (foi feito à mão, antes da fábrica existir).

---

## 11. Frente livro — estado

- **17 capítulos** em `aguardando_aprovacao`; **0 aprovados**; **108 flags** acumuladas.
  A regra do projeto (caps 1-2 com aprovação individual antes do seguinte) foi ignorada e o
  pipeline seguiu até o cap_23.
- `state/pipeline_state.json`: `proximo_capitulo` corrigido de `cap_06` (já escrito) para
  `cap_15`.
- **`output/auditoria/fila_aprovacao.md`** — fila ordenada dos 17 capítulos, com as flags de
  prazo de validade destacadas (valores de portaria 2026, teses "recentíssimas" de 2024-25).
  Fluxo proposto: usuário pede "resumo de aprovação do cap_XX" e recebe uma página para decidir.
- **`output/auditoria/auditoria_dirigida_20260727.md`** — 3 achados no **cap_18 (BPC)**:
  1. §146 afirma presunção **absoluta** do critério de ¼, contradizendo o Tema 122 da TNU
     (relativa) sem enfrentar a divergência com o Tema 185 do STJ. **Corrigir.**
  2. §162 sugere **incluir genro/nora no grupo familiar** quando contribuem de fato — é
     exatamente a conduta cassada na Reclamação 0000302-22 ("vias transversas"). **Corrigir.**
  3. §§152-154 não citam o Tema 73 nem seu alcance temporal nem a divergência interna.
     **Enriquecer.**
- Capítulos de tempo especial e rural **ainda não existem** — as fichas novas (174, 208, 213,
  301) chegaram antes do erro.
- **cap_06** é o único sem `score_auditoria` (None) — reexecutar o Auditor antes de aprovar.
- Git iniciado nesta sessão (não existia). `node_modules` (9 MB) e `__pycache__` removidos;
  scripts temporários movidos para a pasta de backup.
- **Decisão pendente:** as pastas `backup_renumeracao_*` de maio continuam intocadas. Com git
  funcionando são redundantes, mas contêm versões pré-renumeração fora do repositório.

---

## 12. Notas operacionais (armadilhas conhecidas)

**Instagram bloqueou a conta uma vez** (26/07) por atividade automatizada: logar num
navegador novo e, na sequência, tentar alterar o campo Nome tem a assinatura de sequestro de
conta. **Usar sempre o Chrome do usuário** (MCP `claude-in-chrome`), onde a sessão é
reconhecida — nunca o painel de preview interno.

**Upload de arquivos é impossível pelo assistente.** `file_upload` do Chrome MCP só aceita
arquivos que o usuário anexou à conversa; caminho do projeto, pasta da sessão e até
`request_directory` são recusados. Controle de desktop também não resolve: navegadores só
recebem permissão de **leitura**, e a janela de seleção pertence ao Chrome. **O usuário
precisa arrastar o arquivo.** O que ajuda: `open -R "<caminho>"` revela o arquivo no Finder.

**Reel: a trilha não é editável depois de publicado.** Legenda, capa, marcações e texto
alternativo são editáveis; o vídeo e o áudio, não. A versão web **não** oferece o seletor de
música — para ter trilha, publicar pelo app.

**Rascunhos do Instagram** só existem no aparelho: Perfil → primeiro quadradinho da grade
("Rascunhos"), ou ➕ Criar → Reel → aba Rascunhos.

**Espelhamento do iPhone** foi tentado e falhou (iCloud fora de sincronia).

**Legenda:** limite de 2.200 **caracteres** — contar com `len()` em Python, não `wc -c`
(acentuação infla os bytes).

---

## 13. Como retomar

1. Ler este arquivo e `marketing/estado_publicacoes.md` (painel operacional).
2. `git log` para o histórico; tudo está commitado.
3. Se o objetivo for **crescer o perfil**: começar pela seção 9 (semeadura) e pelas duas
   primeiras pendências do usuário na seção 10. Produzir mais posts sem isso não muda o número.
4. Se o objetivo for **produzir um post**: copiar um `spec.json` existente como modelo,
   verificar os precedentes pelo método da seção 6, rodar os dois scripts da seção 5.
5. Se o objetivo for **o livro**: `output/auditoria/fila_aprovacao.md` e
   `output/auditoria/auditoria_dirigida_20260727.md`.

**MCPs necessários:** `claude-in-chrome` (publicação assistida), `jur-rag`,
`jurisprudencia_tnu`, `jurisprudencia_stf`, `legislacao`.
**Skills relevantes:** `avoid-ai-writing` (critério de linguagem), `jur-rag`, `pertinencia`.
