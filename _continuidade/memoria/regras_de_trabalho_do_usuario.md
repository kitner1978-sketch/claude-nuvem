# Regras de trabalho do usuário (trecho do mapa de projetos do Mac)

Copiado de `~/.claude/PROJETOS.md` do Mac original em 24/09/2026. São regras que o autor fixou para **todos** os projetos, aprendidas com erro real. Valem aqui.

## 1. Quem é o usuário

**Luiz Bispo da Silva Neto** — Juiz Federal. Titular da 25ª Vara Federal de Goiana/PE,
atuou como **Desembargador Federal Auxiliar convocado na 7ª Turma do TRF5** e está se
removendo para a **1ª Relatoria da 3ª Turma Recursal da JFPE**. Também foi titular da
7ª Vara Federal de Petrolina. É professor da Escola da REJUFE e autor de livro de
Direito Previdenciário.

Isso explica a forma do acervo: quase tudo gira em torno de **julgar, automatizar a
vara, pesquisar jurisprudência e ensinar previdenciário**.

O trabalho é dividido em três frentes que reaparecem em vários projetos:

| Frente | Do que se trata |
|---|---|
| Gabinete / julgamento | Minutas, votos, ementas, correção de mutirão, sentenças |
| Automação / dados | Coleta do PJe, painéis, triagem de acervo, RAG de jurisprudência |
| Ensino / produção | Curso REJUFE, livro, artigos acadêmicos, jurimetria |

> ⚠️ **Inconsistência a resolver:** as memórias `user_perfil` dos projetos `n8n` e
> `tr3pe` descrevem o usuário como *"Servidor da Justiça Federal, Diretor de Secretaria
> na 25ª Vara"*. Todo o restante do acervo (e o uso real) indica **Juiz Federal**.
> Trate a descrição de "Diretor de Secretaria" como provavelmente incorreta e confirme
> antes de se apoiar nela.

---

### Servidores e nós (apelidos que aparecem nas memórias)

| Nome | O que é |
|---|---|
| **Onça** | Nó GPU (RTX 3090) de embeddings do RAG. Só via Tailscale. Guarda cópia completa da RAG (283 GB) em `/root/RAG` |
| **Formiga** | LXC 105 — roda a coleta do TRF5 2º grau (migrada do Mac em 22/06/2026) |
| **Hermes** | LXC 104 — roda os vigias externos (saúde da coleta, conclusos, remoção SEI) fora da VM do PJe |
| **VM 192.168.31.66** | Hospeda o dashboard `relatorio25vf` (porta 8080). Pode perder a rota default e parar a coleta em silêncio |
| **joaldo** | LXC 1003/1004 — serving de jurisprudência que recebe o delta |

### Servidores MCP (configuração global)

`jurisprudencia`, `jur-rag`, `jurisprudencia_7turma`, `informativos`, `legislacao`,
`jurisprudencia_sentencas`, `jurisprudencia_stf`, `jurisprudencia_tnu`, `pje`, `pje-gw`.

**Regra de roteamento das RAGs** (memória `rag-roteamento`): a base unificada quase não
tem STF. Use sempre a base dedicada certa antes de concluir que "não existe".

### 7.5 Projeto Livro — `/Volumes/Macintosh NVMe/Projeto Livro`

Livro de Direito Previdenciário. Registrado sob **dois slugs** por causa da renomeação
do volume (`Untitled` → `Macintosh NVMe`).

- **Atualização obrigatória:** o STF derrubou a idade mínima da aposentadoria especial na **ADI 6.309** — atualizar conservando o histórico.
- **Estilo:** escrita anti-IA, evitando travessões e ponto-e-vírgula.
- **Ferramenta:** `add_blockquote` no `md_to_docx` renderiza callouts do Obsidian e tabelas internas.
- Uma sessão discute plataforma para crescer o Instagram (~500 seguidores) e vender livros e cursos.

### 7.6 aposentadoria especial — `/Volumes/Macintosh NVMe/aposentadoria_especial`

Mesmas três memórias do Projeto Livro (ADI 6.309, escrita anti-IA, gerador DOCX) —
é o recorte temático do livro. Sem sessões.

## 10. Regras transversais de trabalho

Valem em qualquer projeto — foram aprendidas com erro real.

### Máquina e recursos
- **16 GB de RAM.** Paralelismo pesado (vários subagentes, varreduras simultâneas na base de 151 GB) **já travou o computador**. Trabalhar de forma sequencial.
- Agentes em paralelo que extraem PDF para um nome genérico no scratchpad **sobrescrevem uns aos outros** — um QA chegou a ler as razões de apelação de outro processo. Usar nome único por caso.

### Verificação antes de afirmar
- **Esgotar a busca antes de perguntar:** em 4 de 5 retificações de uma noite, a resposta já estava no arquivo em mãos. Buscar sempre o **contrário** do que se vai afirmar.
- **Precedente sem ficha completa conferida na fonte primária é descartado.** Não existe citação parcial, e **quem confere nunca é quem escreveu**.
- Zero ocorrência de um termo nos autos do recurso **não prova** que a minuta inventou — prova que a peça de origem não foi juntada.
- Unanimidade nos autos (sentença, apelação e recurso repetindo a mesma citação) **não prova** que a minuta divergente esteja errada.
- Nunca aceitar "é falso positivo do validador" sem rodar a checagem na frase exata.
- Nunca afirmar **por que** outro juízo decidiu a partir de extrato de tela (SEEU, BNMP, PJe) — de tela se descreve o que consta.
- Antes de redigir sobre matéria afetada, conferir se o repetitivo **já foi julgado** e se houve modulação.
- O campo "Tese firmada" do registro de tema do STF/STJ às vezes **repete o título** do tema e erra nos dois sentidos.

### Escrita
- **Anti-IA:** evitar travessões e ponto-e-vírgula; nada no texto final pode revelar produção por IA.
- Existem as skills globais `humanizar` e `avoid-ai-writing` para essa revisão.
- A data que o índice do PJe mostra ao lado do Id é a da **juntada**, não a do ato.

### Permissões
- **Leitura é proativa** (conferir peça no PJe, checar precedente na RAG).
- **Escrita exige autorização caso a caso** (gravar no PJe, publicar no OneDrive).

---

