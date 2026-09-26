---
name: avoid-ai-writing
description: Audita e reescreve textos para remover padrões de escrita de IA ("marcas de IA") em português brasileiro. Use esta skill quando pedirem para "remover marcas de IA", "limpar texto de IA", "tirar cara de IA", "revisar para padrões de IA", "deixar menos parecido com IA" ou "humanizar o texto". Suporta modo só-detecção, modo edição-no-arquivo, perfil de voz opcional (casual / profissional / técnico / acolhedor / direto) e iteração até convergir.
version: 3.10.0-ptbr
license: MIT
compatibility: Qualquer assistente de código que suporte o formato SKILL.md do agentskills.io (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) ou OpenClaw. Não requer ferramentas externas nem APIs.
metadata:
  author: Conor Bronsdon
  adaptation: português brasileiro
  tags: escrita edição voz qualidade portugues
  agentskills_spec: "1.0"
  openclaw:
    emoji: "✍️"
---

# Evitar Escrita de IA — Auditar e Reescrever (pt-BR)

Você está editando conteúdo para remover padrões de escrita de IA ("marcas de IA") que fazem o texto soar gerado por máquina, com foco em português brasileiro.

## O que esta skill é e o que não é

Isto é uma **ferramenta de qualidade de escrita**, não um veredito. Os padrões sinalizados aqui são estatisticamente mais comuns em texto de LLM, mas pessoas no piloto automático — sobretudo escrevendo com prazo apertado, em gêneros pouco familiares, ou num idioma que não é o materno — produzem as mesmas formas. Auditorias independentes de detectores comerciais de IA encontraram taxas de falso-positivo acima de 60% em quem escreve inglês como segunda língua (Liang et al., Stanford, *Patterns* 2023) e taxas gerais de classificação errada acima de 70% em detectores de código aberto (Jabarian & Imas, BFI Working Paper 2025-116, 2025). Paráfrase adversarial reduz a precisão de detecção em ~88% em todos os métodos testados (arXiv:2506.07001, 2025).

Os padrões servem como sinal — tanto para limpar a própria escrita quanto para avaliar se um texto soa gerado por IA. Só não os transforme na única base de uma decisão séria (integridade acadêmica, contratação, publicação, autoria). Várias regras aqui também disparam em quem escreve numa segunda língua, em humanos sob prazo e em gêneros técnicos que comprimem vocabulário por natureza. Combine o sinal com o contexto: quem escreveu, qual o gênero, como é a voz normal da pessoa, que outras evidências você tem.

Em resumo: sinais, não prova. Vale agir; não vale arruinar o dia de alguém.

## Modos

Esta skill opera em um de três modos:

**`reescrever`** (padrão) — Sinaliza as marcas de IA e reescreve o texto para corrigi-las.

**`detectar`** — Só sinaliza as marcas de IA. Sem reescrever. Use este modo quando:
- A pessoa quer ver o que foi sinalizado e decidir sozinha o que corrigir
- Os padrões sinalizados podem ser intencionais (padrões de IA nem sempre são ruins — funcionam em doses pequenas)
- Você está auditando um texto que não quer alterar (conteúdo publicado, texto de outra pessoa, material de referência)
- Você quer uma varredura rápida sem esperar uma reescrita completa

**`editar`** — Edita um arquivo no lugar em vez de devolver o texto reescrito. Use quando a pessoa apontar para um arquivo ("limpa o `rascunho.md`", "corrige as marcas de IA direto neste arquivo") e quiser o arquivo alterado, não uma cópia para colar de volta. Faça **edições mínimas e pontuais** com a ferramenta Edit — altere os trechos sinalizados, não o documento inteiro. **Preserve trechos que já estão humanos**: se um parágrafo não tem marcas, deixe-o intacto. **Não edite citações, blocos de código ou texto atribuído a outra pessoa** — sinalize-os em vez de reescrever. Para um arquivo grande, confirme qual seção limpar antes de mudar qualquer coisa. Depois de editar, releia o arquivo e confirme que os padrões sinalizados foram resolvidos.

Acione o modo detectar quando a pessoa disser "detectar", "só sinalizar", "só auditar", "apenas aponta", "varredura", "que padrões de IA tem aqui" ou similar. Acione o modo editar quando ela nomear um arquivo e pedir para corrigir ou limpar no lugar. Use reescrever como padrão se nada for especificado.

**Invocação.** Linguagem natural basta ("reescreve isso num tom direto pro LinkedIn", "edita o `post.md` no lugar", "varre isso, não reescreve"). Quem quiser pode passar opções explícitas, que mapeiam para as seções abaixo: `[--modo reescrever|detectar|editar]`, `[--voz casual|profissional|tecnico|acolhedor|direto]`, `[--contexto linkedin|blog|blog-tecnico|email-investidor|docs|casual]`, `[--arquivo CAMINHO]`, `[--iterar N]` (máx. 2).

**Iterar até convergir (opcional).** O modo reescrever já roda uma segunda passada corretiva (ver Formato de saída) — essa passada embutida *é* a passada 2, então `--iterar` não soma em cima dela. Quando a pessoa pedir para "iterar", "continuar até ficar limpo" ou passar `--iterar N`, repita o ciclo auditar→reescrever até não restar nenhum padrão ou atingir **N passadas**. Limite **N em 2**: uma reescrita mais uma passada corretiva já elimina os padrões sinalizados, e uma terceira passada custa uma geração inteira raramente encontrando mais. Informe quantas passadas levou ("convergiu em 2 passadas").

---

No modo **reescrever**, seu trabalho é:

1. **Auditar**: identificar toda marca de IA presente, citando o texto específico
2. **Reescrever**: devolver uma versão limpa, sem nenhuma marca de IA
3. **Mostrar um resumo do diff**: listar brevemente o que mudou e por quê

No modo **detectar**, seu trabalho é:

1. **Auditar**: identificar toda marca de IA presente, citando o texto específico
2. **Avaliar**: indicar quais sinalizações são problemas claros vs. padrões que podem ser intencionais ou eficazes no contexto

No modo **editar**, seu trabalho é:

1. **Ler** o arquivo que a pessoa nomeou
2. **Editar no lugar**: aplicar correções mínimas e pontuais aos trechos sinalizados com a ferramenta Edit, deixando intactos os trechos que já estão humanos
3. **Verificar**: reler o arquivo e confirmar que os padrões sinalizados foram resolvidos; relatar o que mudou

---

## O que remover ou corrigir

### Formatação
- **Travessões (— e --)**: Substitua por vírgulas, pontos, parênteses, ou reescreva como duas frases. Meta: zero. Máximo absoluto: um a cada 1.000 palavras. Vale também para títulos e subtítulos, não só para o corpo do texto. Pegue tanto o travessão Unicode (—) quanto o substituto de hífen duplo (--). Atenção: o travessão é abusado em pt-BR por LLM, muitas vezes onde uma vírgula ou dois pontos resolveriam.
- **Excesso de negrito**: Tire o negrito da maioria das expressões. No máximo uma expressão em negrito por seção principal, ou nenhuma. Se algo é importante o bastante para estar em negrito, reestruture a frase para começar por ele.
- **Emoji em títulos**: Remova por completo. Nada de `## 🚀 O que isso significa`. Exceção: posts de rede social podem usar um ou dois emoji com parcimônia — no fim da linha, nunca no meio da frase.
- **Excesso de listas com marcadores**: Converta seções cheias de bullets em parágrafos corridos. Bullets só para conteúdo genuinamente em lista (comparação de recursos, instruções passo a passo, parâmetros de API).
- **Aspas e apóstrofos curvos (" " ' ')**: Aspas e apóstrofos curvos (U+201C/U+201D, U+2018/U+2019) são um sinal *fraco* de "colado do chat" — relevante sobretudo em contextos de texto puro como comentários de código, mensagens de commit ou rascunhos em .txt, onde nada curva automaticamente. Trate como corroborante, nunca como conclusivo: Word, Google Docs, macOS e iOS curvam aspas por padrão, então a maioria da prosa humana também as contém. Não sinalize apóstrofo curvo (U+2019) sozinho. Substitua por aspas retas em texto puro/código; deixe-as em publicações finalizadas e na pontuação correta para o idioma (aspas «» em alguns contextos lusófonos formais).

### Estrutura da frase
- **"Não é X — é Y" / "Não se trata de X, e sim de Y"**: Reescreva como afirmação direta e positiva. No máximo uma por texto, e só se servir ao argumento.
- **Intensificadores vazios**: Corte `genuíno` / `genuinamente`, `verdadeiro` / `verdadeiramente`, `real` / `realmente`, `francamente`, `sendo honesto` / `para ser honesto`, `sejamos claros`, `vale ressaltar que`. Apenas afirme o fato.
- **Endosso vago ("vale a pena [verbo]")**: Corte ou substitua `vale a pena ler`, `vale a pena prestar atenção`, `vale conferir`, `vale dar uma olhada`, `vale o seu tempo`, `imperdível`. Trocam um joinha genérico por um motivo específico. Diga *por que* algo importa.
- **Atenuação (hedging)**: Corte `talvez`, `pode potencialmente`, `é importante notar que`, `só para deixar claro`, `de certa forma`. Vá direto ao ponto.
- **Frases-ponte ausentes**: Cada parágrafo deve se conectar ao anterior. Se dá para reordenar os parágrafos sem o leitor perceber, falta tecido conectivo.
- **Regra de três compulsiva**: Varie os agrupamentos. Use dois itens, quatro itens, ou uma frase inteira no lugar de tríades. No máximo um padrão "adjetivo, adjetivo e adjetivo" por texto.

### Palavras e expressões a substituir

As palavras estão organizadas em três níveis (tiers), conforme a confiabilidade com que indicam texto gerado por IA. Essa abordagem em níveis reduz falsos-positivos em palavras que são aceitáveis isoladas, mas suspeitas em aglomerado.

- **Nível 1 — Sempre sinalizar.** Aparecem muito mais em texto de IA do que humano. Substitua à primeira vista.
- **Nível 2 — Sinalizar em aglomerado.** Aceitáveis sozinhas, mas duas ou mais no mesmo parágrafo já são um forte sinal de IA. Sinalize quando aparecerem juntas.
- **Nível 3 — Sinalizar por densidade.** Palavras comuns que a IA simplesmente abusa. Só sinalize quando representam uma fração perceptível do texto (cerca de 3%+ do total de palavras).

**Pegue as formas flexionadas.** Cada entrada abaixo cobre a palavra listada *e suas variantes morfológicas* — advérbio (`-mente`), gerúndio/particípio, plural, comparativo/superlativo e conjugações verbais — a menos que a variante carregue um sentido legítimo distinto. Assim `robusto` também pega `robusta`/`robustos`/`robustez`; `alavancar` pega `alavancando`/`alavancagem`; `meticuloso` cobre `meticulosamente`. Quando a variante tem um sentido honesto separado, julgue pelo contexto em vez de casar cegamente.

#### Nível 1 — Sempre substituir

| Substituir | Por |
|---|---|
| mergulhar / mergulhar fundo (metáfora) | explorar, examinar, analisar, ver de perto |
| desvendar | explicar, mostrar, esclarecer |
| panorama / cenário (metáfora) | área, campo, setor, mercado, mundo |
| tapeçaria / mosaico (metáfora) | (descreva a complexidade real) |
| âmbito / esfera | área, campo, domínio |
| paradigma | modelo, abordagem, estrutura |
| embarcar (metáfora) | começar, iniciar |
| farol / norte (metáfora) | (reescreva por inteiro) |
| prova viva de / testemunho de | mostra, prova, demonstra |
| robusto | forte, confiável, sólido |
| abrangente | completo, detalhado, amplo |
| de ponta / na vanguarda | mais recente, mais novo, avançado |
| alavancar / lançar mão de | usar, aproveitar |
| crucial / pivotal / primordial | importante, central, decisivo |
| ressalta / sublinha / evidencia | destaca, mostra |
| meticuloso / meticulosamente | cuidadoso, detalhado, preciso |
| perfeito / sem emendas / sem atritos | suave, fácil, sem fricção |
| divisor de águas | (descreva o que mudou especificamente e por que importa) |
| utilizar | usar |
| ponto de inflexão / momento decisivo | virada, mudança (ou descreva o que mudou) |
| marcando um momento decisivo | (diga o que aconteceu) |
| o futuro é promissor | (corte — diga algo específico ou nada) |
| só o tempo dirá / somente o tempo dirá | (corte — diga algo específico ou nada) |
| aninhado / encravado | fica em, está localizado em, situa-se em |
| vibrante | (descreva o que o torna ativo, ou corte) |
| próspero / florescente | crescente, ativo (ou cite um número) |
| apesar dos desafios… continua a prosperar | (nomeie o desafio e a resposta, ou corte) |
| evidenciando / demonstrando (de enfeite) | mostrando (ou corte a oração) |
| mergulho profundo / aprofundar | examinar, analisar, ver de perto |
| destrinchar / dissecar (de enfeite) | explicar, detalhar, percorrer |
| intrincado / intricado / nuances complexas | complexo, detalhado (ou nomeie a complexidade) |
| complexidades | (nomeie as complexidades reais, ou use "problemas"/"detalhes") |
| em constante evolução / em constante mudança | em mudança (ou descreva como) |
| duradouro / perene | que dura, de longa data (ou diga há quanto tempo) |
| árduo / hercúleo / assustador | difícil, trabalhoso |
| holístico / abordagem holística | completo, integral (ou descreva o que inclui) |
| acionável | prático, útil, concreto |
| impactante | eficaz, significativo (ou descreva o impacto) |
| aprendizados | lições, conclusões, descobertas |
| líder de pensamento / referência no assunto | especialista, autoridade (ou descreva a contribuição real) |
| melhores práticas | o que funciona, métodos comprovados, abordagem padrão |
| em sua essência / em seu cerne | (corte — apenas afirme o que é) |
| sinergia / sinergias | (descreva o efeito combinado real) |
| interação / interrelação (de enfeite) | relação, conexão |
| a fim de / com o intuito de / com o objetivo de | para |
| devido ao fato de que / em virtude de | porque |
| serve como / configura-se como | é |
| conta com / dispõe de (de enfeite) | tem, inclui |
| ostenta / apresenta (inflado) | tem, é, mostra |
| iniciar-se / dar início a (inflado) | começar |
| averiguar / constatar (inflado) | descobrir, saber, ver |
| empreitada / esforço hercúleo | esforço, tentativa |
| ávido / sedento (como intensificador) | interessado, animado (ou corte) |
| genuíno / genuinamente (como intensificador) | (corte — apenas afirme o fato) |
| sinfonia / orquestrar (metáfora) | (descreva a coordenação real) |
| abraçar / abarcar (metáfora) | adotar, aceitar, usar, migrar para |
| de suma importância / de extrema relevância | importante (ou diga por que importa) |
| no atual cenário / nos dias de hoje / na era digital | (corte ou diga o contexto específico) |

#### Nível 2 — Sinalizar quando 2+ aparecem no mesmo parágrafo

Estas palavras são legítimas sozinhas. Quando duas ou mais aparecem juntas, o parágrafo provavelmente precisa de reescrita.

| Substituir | Por |
|---|---|
| aproveitar (de enfeite) | usar, tirar proveito |
| navegar (metáfora) | lidar com, conduzir, resolver |
| fomentar / fomento | incentivar, apoiar, construir |
| elevar / potencializar | melhorar, reforçar, fortalecer |
| desbloquear / destravar (metáfora) | liberar, permitir, habilitar |
| otimizar / agilizar | simplificar, acelerar |
| empoderar / capacitar (de enfeite) | permitir, possibilitar |
| reforçar / robustecer | apoiar, fortalecer |
| liderar / encabeçar (inflado) | conduzir, tocar, comandar |
| ressoar / dialogar com | conectar com, interessar a, importar a |
| revolucionar | mudar, transformar (ou descreva o que mudou) |
| facilitar / viabilizar | permitir, ajudar, possibilitar |
| sustentar / embasar | apoiar, dar base a |
| nuançado / cheio de nuances | específico, sutil (ou nomeie a nuance real) |
| crucial | importante, central, necessário |
| multifacetado | (descreva as facetas reais, ou corte) |
| ecossistema (metáfora) | sistema, comunidade, rede, mercado |
| miríade / vasta gama | muitos (ou dê um número) |
| infinidade / plêiade / leque de | muitos, vários (ou dê um número) |
| abarcar / abranger | incluir, cobrir, contemplar |
| catalisar / impulsionar (de enfeite) | iniciar, acelerar, disparar |
| reimaginar / repensar (de enfeite) | redesenhar, reformular |
| galvanizar / mobilizar | motivar, reunir, impulsionar |
| ampliar / incrementar (de enfeite) | aumentar, expandir, somar |
| cultivar (metáfora) | construir, desenvolver, criar |
| iluminar / lançar luz sobre | esclarecer, explicar, mostrar |
| elucidar | explicar, esclarecer, detalhar |
| justapor / contrapor | comparar, contrastar |
| mudança de paradigma | (descreva o que de fato mudou) |
| transformador / transformação | (descreva o que mudou e como) |
| pilar / alicerce / pedra angular | base, fundamento, parte central |
| primordial / soberano | mais importante, prioridade máxima |
| prestes a / a postos para | pronto para, perto de, começando a |
| emergente / em ascensão (de enfeite) | crescente, novo (ou cite um número) |
| nascente / incipiente | novo, em estágio inicial |
| quintessencial | típico, clássico, definidor |
| abrangente / norteador (de estrutura) | principal, central, amplo |
| subjacente / que embasa | base, fundamento, o que sustenta |

#### Nível 3 — Sinalizar só em alta densidade

São palavras normais. Só sinalize quando o texto está saturado delas — sinal de que a IA encheu espaço com elogio vago em vez de detalhe.

| Palavra | O que fazer |
|---|---|
| significativo / significativamente | Troque algumas por dados: números, comparações, exemplos |
| inovador / inovação | Descreva o que de fato é novo |
| eficaz / eficiente / eficazmente | Diga como ou cite uma métrica |
| dinâmico / dinâmica | Nomeie as forças ou mudanças reais |
| escalável / escalabilidade | Descreva o que escala e até onde |
| convincente / atraente | Diga por que convence |
| sem precedentes / inédito | Nomeie o precedente que quebra (ou corte) |
| excepcional / excepcionalmente | Cite o que o torna exceção |
| notável / notavelmente | Diga o que vale notar |
| sofisticado | Descreva a sofisticação |
| fundamental (de enfeite) | Diga o papel que cumpriu |
| de classe mundial / estado da arte / referência de mercado | Cite um benchmark ou comparação |

#### Expressões de Nível 3 — Sinalizar por densidade ou em aglomerado

Clichês de várias palavras, inofensivos isolados, mas que se empilham em conteúdo gerado por IA (cripto, web3, marketing de tecnologia e "reviews" de produto são os piores). Sinalize a partir de **2 usos da mesma expressão**, *e* aplique uma **regra de aglomerado**: três ou mais expressões *distintas* desta tabela num só texto já é forte sinal, mesmo que cada uma apareça uma vez — é a forma que LLMs tomam ao variar o próprio clichê para parecer menos repetitivo.

| Expressão | O que fazer |
|---|---|
| setor emergente / espaço emergente / nova categoria | Nomeie o setor real ou o que há de emergente nele |
| a integração de (X com Y) | Descreva o que se integra e o que muda para o usuário |
| a interseção de (X e Y) / na confluência de | Escolha a sobreposição específica que importa ou corte |
| impulsionado pela comunidade | Diga o que a comunidade faz. Sozinho é enchimento |
| sustentabilidade de longo prazo | Cite o horizonte de tempo e a restrição. "Longo prazo" é vago |
| engajamento do usuário | Nomeie a ação. "Engajamento" embrulha cliques/comentários/retenção |
| infraestrutura descentralizada / compute descentralizado | Especifique a arquitetura ou corte. Virou rótulo, não afirmação |
| solução completa / solução de ponta a ponta | Diga o que ela faz, especificamente |
| pensado para o longo prazo / projetado para [X] | Corte "pensado para" — ou ele faz, ou não. Aí afirme a propriedade |

### Frases de molde (evitar)

Estas construções de preencher-lacuna indicam que a frase foi gerada, não escrita. Se a frase tem um espaço onde caberia qualquer substantivo ou adjetivo e ainda soaria igual, é genérica demais.

- "um passo [adjetivo] rumo a [substantivo]" → descreva a capacidade, benchmark ou resultado específico
- "um grande avanço para [substantivo]" → mesma regra: diga o que de fato mudou
- "Seja você [X] ou [Y]" → falsa amplitude. Escolha o público que você realmente atende, ou corte. "Seja você um fundador de startup ou um arquiteto corporativo" não diz nada — é só "todo mundo".
- "Recentemente, tive o prazer de [verbo]" → padrão de review/rede social. Diga o que houve: "conversei com", "li", "participei de".

### Conectores a remover ou reescrever
- "Ademais" / "Outrossim" / "Adicionalmente" / "Além disso" (em excesso) → reestruture para a conexão ficar óbvia, ou use "e", "também"
- "No atual cenário de [X]" / "Numa era em que" → corte ou diga o contexto específico
- "Vale ressaltar que" / "Vale destacar que" / "Cabe salientar" / "Notadamente" → apenas afirme o fato
- "Eis o que é interessante" / "O que mais chama atenção" / "O que se destaca aqui" → molduras que conduzem o leitor. Deixe o conteúdo sinalizar a própria importância. Se precisar de uma deixa, torne-a específica: "O número de receita importa porque..." em vez de "Aqui está a parte interessante."
- "Em conclusão" / "Em suma" / "Em síntese" / "Concluindo" → sua conclusão deveria ser óbvia
- "Quando se trata de" / "No que diz respeito a" / "No que tange a" → fale do assunto diretamente
- "No fim das contas" / "No final do dia" → corte
- "Dito isso" / "Posto isso" → corte ou use "mas", "porém", "no entanto". Não abuse de nenhum deles.

### Problemas estruturais
- **Parágrafos de tamanho uniforme**: Varie de propósito. Inclua parágrafos de 1-2 frases e outros mais longos. Se todo parágrafo tem mais ou menos o mesmo tamanho, corrija.
- **Aberturas formulaicas**: Se o texto abre com contexto amplo antes de chegar ao ponto ("No mundo em rápida transformação de..."), reescreva para começar pela notícia ou pela ideia. O contexto pode vir depois.
- **Gramática suspeitosamente impecável**: Não lixe toda a personalidade. Fragmentos deliberados, frases começando com "E" ou "Mas": se a voz natural usa, mantenha.

### Inflação de importância
- Frases como "marcando um momento decisivo na evolução de..." ou "um divisor de águas para o setor" inflam eventos rotineiros em marcos históricos. Diga o que aconteceu e deixe o leitor julgar a importância.
- Se a frase continua funcionando depois de deletar a oração inflada, delete-a.

### Fechamentos de futuro-genéricos
- "Pode se tornar uma das narrativas mais importantes do próximo ciclo", "pode vir a ser a tendência definidora da próxima década", "está prestes a se tornar o próximo grande capítulo de [X]". A IA recorre a esse formato quando precisa fechar um pensamento sem se comprometer com uma afirmação verificável. É gramaticalmente uma previsão, mas sem conteúdo testável.
- Padrão: modal (pode / poderá / vai / está prestes a) + "se tornar" + uma das mais [adjetivo] + (narrativa / história / tendência / tema / capítulo / movimento / força).
- Correção: escolha a versão falsificável. "O compute descentralizado pode ficar mais barato que o spot da AWS para cargas paralelizáveis até 2027" é uma previsão. "A interseção de IA e DePIN pode se tornar uma das narrativas mais importantes do próximo ciclo" não é.

### Previsões com atenuação empilhada
- Empilhar um modal com um advérbio de atenuação: "poderia eventualmente criar", "pode acabar destravando", "talvez venha a transformar". Qualquer palavra sozinha é aceitável; o empilhamento é a marca. Cada atenuação cancela a próxima, deixando uma frase que não afirma nada enquanto soa cautelosa e ponderada.
- Correção: escolha uma. Se quer dizer "pode criar", diga isso. Se quer dizer "potencialmente cria", diga isso. As duas juntas é enchimento.

### Inflação com "real/verdadeiro"
- "Tokenomics real on-chain", "sustentabilidade de recompensa de verdade", "utilidade genuína", "verdadeiro encaixe produto-mercado". Usar `real` / `verdadeiro` / `genuíno` / `de fato` como intensificador vazio sobre um substantivo abstrato insinua que o resto do campo é falso ou superficial — sem nomear o que torna esta instância a verdadeira. Comum em conteúdo de cripto/IA/web3 onde quem escreve quer sinalizar sofisticação.
- Diferente da regra de "intensificadores vazios" (genuíno / verdadeiramente / francamente como atenuação de frase). Esta é a forma modificadora de substantivo, em que o intensificador gruda num substantivo abstrato para fabricar um contraste que fica subentendido.
- **Ressalva — contraste nomeado:** se a frase nomeia explicitamente qual é a versão falsa/superficial, deixe. "Liquidação real on-chain, não IOUs em ponte" ou "receita de verdade, de clientes pagantes, não de subsídios" é escrita contrastiva honesta. A marca de IA é o contraste não dito.
- Correção quando nenhum contraste é nomeado: tire o adjetivo e acrescente a afirmação específica. "Sustentabilidade de recompensa" → "recompensas pagas com R$ X/mês em taxas, não com emissão de tokens."

### Excesso de hashtags
- Blocos longos de hashtags no fim (6+ hashtags num post curto) são quase universais em conteúdo de rede social gerado por IA e raros em posts humanos pensados. O bloco costuma misturar uma tag específica do projeto com tags genéricas de categoria (#IA #Cripto #Web3 #Inovação #Tecnologia #Futuro) — as genéricas não ajudam na descoberta e soam como saída de bot.
- **Por que 6?** Piso empírico. O engajamento orgânico no LinkedIn e no X estabiliza ou cai depois de 3-5 tags; posts humanos que passam de 5 costumam ser posts de lançamento trocando alcance por engajamento, enquanto posts gerados por IA usam 10-15 por padrão. O detector trata 6+ como sinalização firme; a spec trata 5+ como marca leve, digna de um segundo olhar nos perfis `linkedin` e `email-investidor`.
- Correção: 2-3 tags específicas no máximo, ou nenhuma. Se uma hashtag não ajudaria o leitor a achar trabalho relacionado, é enchimento.

### Listas de sintagmas nominais soltos
- Uma lista de 5+ itens em que cada item é um sintagma curto (≤6 palavras) de adjetivo+substantivo, sem verbo. "Eficiência de mineração estável / Conectividade de pool confiável / Desempenho otimizado / Baixa taxa de falhas / Utilização eficiente de hardware / Estabilidade térmica consistente." Lê como folheto de marketing porque é a forma padrão da IA ao resumir recursos.
- A marca é a *simetria*: todo item com a mesma forma gramatical, todo item com tamanho paralelo, nenhum afirma nada verificável. Uma lista genuína de observações teria tamanhos variados, verbos ocasionais e ao menos um item que foge do padrão.
- Correção: converta em parágrafo corrido, ou reescreva os itens como afirmações completas ("As falhas ficaram abaixo de 1% num teste de 12 horas" supera "Baixa taxa de falhas"). Se a lista é mesmo a forma certa, varie os itens para cada um carregar uma informação de forma diferente.
- Esta regra *não* vale para conteúdo genuinamente em lista (entradas de changelog, listas de tarefas, docs de parâmetros, lista de ingredientes), onde sintagmas soltos são a forma correta.

### Fuga do verbo de ligação
- Texto de IA evita "é" e "tem" substituindo por verbos mais pomposos: "serve como", "configura-se como", "apresenta", "ostenta", "representa". Soa como release de assessoria de imprensa.
- Use "é" ou "tem" por padrão, a menos que um verbo mais específico realmente acrescente sentido.

### Ciclagem de sinônimos
- A IA gira sinônimos para não repetir uma palavra: "desenvolvedores… programadores… profissionais… construtores" no mesmo parágrafo. Quem escreve bem repete a palavra mais clara.
- Se o mesmo substantivo ou verbo aparece três vezes num parágrafo e é a palavra certa, mantenha as três. Variação forçada lê como abuso de dicionário de sinônimos.

### Atribuições vagas
- "Especialistas acreditam", "Estudos mostram", "Pesquisas sugerem", "Líderes do setor concordam" — sem nomear o especialista, o estudo ou o líder. Cite uma fonte específica ou tire a atribuição e afirme diretamente.

### Frases de enchimento
- Tire o recheio mecânico que soma palavras sem sentido:
  - "É importante notar que" → (apenas afirme)
  - "Em termos de" → (reescreva)
  - "A realidade é que" / "O fato é que" → (corte ou afirme direto)
- Obs.: "A fim de", "Devido ao fato de que" e "No fim das contas" estão na tabela de palavras/expressões e nas seções de conectores acima — não duplique regras.

### Conclusões genéricas
- "O futuro é promissor", "Só o tempo dirá", "Uma coisa é certa", "À medida que avançamos" — enchimento disfarçado de conclusão. Corte. Se o texto precisa de um fechamento, torne-o específico ao argumento.

### Resíduos de chatbot
- "Espero que ajude!", "Claro!", "Com certeza!", "Ótima pergunta!", "Fique à vontade para entrar em contato", "Me avise se precisar de mais alguma coisa" — tiques de conversa de interface de chat, não escrita. Remova por completo.
- Atenção também a: "Neste artigo, vamos explorar…" ou "Vamos nessa!" — metanarração gerada por IA. Corte ou reescreva com uma abertura direta.

### Construções com "vamos"
- "Vamos explorar", "Vamos dar uma olhada", "Vamos destrinchar isso", "Vamos analisar" — a IA usa "vamos" como abertura falso-colaborativa para entrar num tópico. É enchimento que atrasa o ponto. Comece pelo ponto. Sinalize qualquer "vamos + verbo" que funcione como transição em vez de um convite genuíno à ação.

### Citação por nome-dropping
- Texto de IA empilha citações de prestígio para fabricar credibilidade: "citado no Estadão, na Folha, na BBC e no Valor". Se uma fonte importa, use-a com contexto: "Numa entrevista de 2024 à Folha, ela argumentou...". Uma referência específica supera quatro menções de nome.

### Análises superficiais em gerúndio
- Cadeias de gerúndios usadas como pseudoanálise: "simbolizando o compromisso da região com o progresso, refletindo décadas de investimento e evidenciando uma nova era de colaboração". Não dizem nada. Substitua por fatos específicos ou corte.
- O mesmo movimento aparece sem gerúndio: "isto representa uma mudança mais ampla", "a decisão simboliza um compromisso com a excelência", "fala de uma tendência maior no setor". Se a importância é real, mostre com uma consequência específica; senão, corte.

### Linguagem promocional
- A IA recorre à prosa de folheto turístico: "aninhada entre as deslumbrantes colinas", "um polo vibrante de inovação", "um ecossistema próspero". Substitua por descrição simples: "é uma cidade na região serrana", "tem 12 startups". Se você não diria numa conversa, corte.

### Desafios formulaicos
- "Apesar dos desafios, [sujeito] continua a prosperar" ou "Mesmo enfrentando ventos contrários, a organização permanece resiliente". É um não-enunciado. Nomeie o desafio real e a resposta real, ou corte a frase.

### Falsas amplitudes
- A IA cria falsa abrangência juntando extremos não relacionados: "do Big Bang à matéria escura", "das civilizações antigas às startups modernas". Soa grandioso e não diz nada. Liste os temas reais ou escolha o que importa.

### Listas com cabeçalho embutido
- Listas em que cada item começa com um cabeçalho em negrito que se repete: "**Desempenho:** O desempenho melhorou em...". Tire o cabeçalho em negrito e escreva o ponto direto. Se os itens precisam de cabeçalho, provavelmente deveriam ser parágrafos.

### Ponto final em rótulo de lista
- Em listas com marcadores em que cada item abre com um rótulo curto, LLMs terminam o rótulo com ponto e rodam a explicação como frase separada. Quem escreve à mão quase sempre usa dois-pontos. Forma mais forte: rótulos em negrito (`**Indicações.**`, `**Distribuição.**` onde uma pessoa escreve `**Indicações:**`). Forma mais fraca, ainda assim marca: o mesmo sem negrito (`- Indicações. Anos de conferências e rede de contatos.`). Corrija o ponto para dois-pontos e minúscula no começo da glosa, ou tire o rótulo e escreva o ponto como frase. Ressalvas: quando o rótulo é uma frase completa por si só, o ponto está correto; e, na forma sem negrito, só sinalize quando o trecho inicial é claramente um rótulo (sintagma de 1-4 palavras, sem verbo).

### Maiúsculas em excesso nos títulos
- A IA às vezes capitaliza demais ou usa caixa alta de propaganda. Em português, use apenas a inicial maiúscula em títulos e subtítulos ("Negociações estratégicas e parcerias", não "Negociações Estratégicas e Parcerias"). Reserve a caixa alta total, se usar, para o título principal.

### Excesso de pares hifenizados / locuções emparelhadas
- A IA empilha modificadores: "uma solução de alta qualidade, bem arquitetada e à prova de futuro". Corte para o modificador que de fato importa. Atenção também à locução "X e Y" redundante em série ("rápido e eficiente, seguro e confiável, simples e intuitivo") — escolha o atributo que carrega peso.

### Avisos de corte de conhecimento
- "Embora os detalhes específicos sejam limitados com base nas informações disponíveis", "Até a minha última atualização", "Não tenho acesso a dados em tempo real". São limitações do modelo vazando para a prosa. Ou ache a informação ou tire a atenuação. Nunca publique uma frase que admite que quem escreveu não foi atrás.

### Preenchimento especulativo de lacuna
- Quando falta um fato, o modelo preenche a lacuna com especulação atenuada disfarçada de contexto: "mantém um perfil público relativamente discreto", "acredita-se que tenha", "provavelmente iniciou a carreira em", "ao que tudo indica estudou". São palpites formatados como afirmações. Diferente dos avisos de corte, que *admitem* a lacuna — este a esconde atrás de enchimento plausível, o que é pior, porque o leitor não distingue o que se sabe do que foi inventado. Corte a especulação, ou troque por um fato com fonte.

### Marcadores de molde não preenchidos
- Lacunas entre colchetes que deveriam ter sido substituídas antes de publicar: `[Seu Nome]`, `[INSERIR URL DA FONTE]`, `[Descreva a seção específica]`, `2025-XX-XX`, `<!-- Adicionar citação se houver -->`. São prova quase definitiva de que um boilerplate gerado por IA foi colado sem edição. Trate qualquer marcador visível como bug de publicação: preencha com conteúdo real ou apague a frase inteira.
- Pegue as formas óbvias: `\[(?:Seu|Inserir|Adicionar|Descreva|Especifique|Escolha)[^\]]+\]`, `\b\d{4}-XX-XX\b`, comentários HTML/Markdown com verbos de molde (`adicionar`, `preencher`, `todo`, `inserir`).

### Vazamento de marcação de citação de chatbot
- Tokens internos de citação que vazam ao copiar e colar de interfaces de chat: `citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`. Não são padrões — são impressões digitais. A presença deles é basicamente prova de que o texto foi gerado por uma ferramenta de chat específica e colado sem limpeza.
- A correção é mecânica: apague todo token de marcação. Se a citação importava, troque por uma referência real. Não tente humanizar a marcação — delete.

### Parâmetros de URL de ferramentas de IA
- Parâmetros de rastreamento que ferramentas de IA acrescentam às URLs que geram, sobrevivendo ao copia-e-cola para o conteúdo publicado: `utm_source=chatgpt.com`, `utm_source=copilot.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`. Mesma lógica do vazamento de citação — a presença do parâmetro é a assinatura, independentemente do texto ao redor.
- A correção: tire o parâmetro de toda URL. Mantenha a URL se o link importa; perca só o parâmetro.

### Inflação de novidade
- Texto de IA trata conceitos consagrados como se quem fala os tivesse inventado: "Ele cunhou um termo", "Ela criou a expressão", "um conceito que ninguém nomeia", "uma falha que ninguém comenta". Na prática, a maioria das ideias numa conversa é aplicação de conceitos existentes, não invenção.
- Dois problemas. Primeiro, é arriscado factualmente: se o conceito já tem verbete na Wikipédia, reivindicar novidade faz quem escreve parecer desinformado. Segundo, bajula o sujeito de um jeito promocional, não analítico.
- A correção: descreva o que a pessoa *fez com* o conceito, não que o descobriu. "A Marina mostrou como o envenenamento de contexto acontece na prática" em vez de "A Marina apresentou um termo que eu nunca tinha ouvido". Na dúvida, presuma que não é novidade.
- Padrões relacionados a sinalizar: "a falha que ninguém nomeia", "o problema de que ninguém fala", "o insight que todos ignoram", "o que ninguém te conta sobre". São iscas de engajamento que alegam escassez de conhecimento onde não há.

### Ganchos de engajamento de infomercial
- Fragmentos-gancho que armam uma revelação: "O detalhe?", "O pulo do gato?", "A questão é a seguinte.", "Mas tem um porém:", "A melhor parte?", "Reviravolta:", "O resultado?". A IA usa para fingir ritmo e fabricar suspense em torno de informação banal — o equivalente em prosa de um infomercial.
- Diferente das perguntas retóricas (que enrolam antes de um ponto) e dos resíduos de chatbot (que performam prestatividade): estes são teasers no meio do fluxo que enchem o ritmo. A correção é apagar o gancho e dizer a coisa. "O detalhe? Só funciona aos fins de semana." vira "Só funciona aos fins de semana."

### Fechamentos de endosso social
- A assinatura curatorial que LLMs acrescentam a posts de LinkedIn e X que compartilham ou recomendam algo — em geral dois-pontos armando um link: "Esse vale o seu tempo:", "Leitura obrigatória:", "Recomendo muito a leitura.", "Faça um favor a você e leia isto.", "Você não vai querer perder.", "Salve para depois.", "Não durma nessa.", "Confie em mim, vale ler.", "Depois me agradece."
- Por que é marca: performa uma recomendação sem dar ao leitor um motivo para clicar. O endosso é genérico e ancorado em demonstrativo ("ESSE vale o seu tempo") — caberia embaixo de qualquer link, e é por isso que o LLM recorre a ele para fechar um post de compartilhamento.
- A correção: diga *o que* é a coisa e *para quem*, depois tire o call-to-action. "Esse vale o seu tempo:" vira "A análise da Sara sobre por que janelas de contexto vazam — a explicação mais clara que achei para quem depura pipelines de RAG." Se você não consegue nomear um motivo específico, o compartilhamento não precisa de assinatura.

### Achatamento emocional
- A IA reivindica emoções como muleta estrutural sem transmiti-las pela escrita: "O que mais me surpreendeu", "Fiquei fascinado ao descobrir", "O que me chamou a atenção foi", "Fiquei animado ao saber", "A parte mais interessante", e a variante de subtítulo: "Parte interessante do projeto:" / "Coisa interessante aqui:". A forma de cabeçalho faz o mesmo serviço — pré-anuncia uma importância que a escrita ainda não conquistou.
- Dois problemas. Primeiro, é dizer-sem-mostrar: se a coisa é mesmo surpreendente, o leitor deveria sentir isso pelo conteúdo, não pelo anúncio. Segundo, são frases abusadas como introdução de lista e transição.
- Este padrão nem sempre é IA. Também é sinal de escrita humana preguiçosa no piloto automático. Sinalize de todo jeito.
- A correção não é "nunca diga surpreso". É: se você reivindica uma emoção, a escrita ao redor deve justificá-la. Senão, corte a reivindicação e apresente a coisa direto.

### Falsa concessão
- "Embora X seja impressionante, Y continua sendo um desafio" ou "Apesar dos avanços de X, Y segue em aberto". A IA usa isso para soar equilibrada sem de fato pesar nada. As duas metades são vagas. Ou torne a concessão específica (nomeie o impressionante, nomeie o desafio real) ou escolha um lado e defenda.

### Perguntas retóricas de abertura
- "Mas o que isso significa para os desenvolvedores?" / "Então, por que você deveria se importar?" / "E agora?" — a IA usa perguntas retóricas para enrolar antes do ponto. Se você sabe a resposta, diga. Perguntas retóricas se conquistam com uma boa preparação, não se jogam como transição de seção.

### Atenuação entre parênteses
- "(e, cada vez mais, Z)" / "(ou, mais precisamente, Y)" / "(e, talvez mais importante, W)" — a IA insere apartes entre parênteses para soar matizada sem se comprometer. Se o aparte importa, dê uma frase a ele. Se não, corte.

### Inflação de lista numerada
- "Três conclusões principais" / "Cinco coisas para saber" / "Os sete principais" — a IA recorre a listas numeradas porque são estruturalmente seguras. Só use lista numerada quando o conteúdo de fato tem aquela quantidade de itens discretos e paralelos. Se você está enchendo para bater um número, a lista não deveria existir.

### Resíduos de cadeia de raciocínio
- "Vamos pensar passo a passo", "Destrinchando isso", "Para abordar de forma sistemática", "Passo 1:", "Eis meu raciocínio", "Primeiro, vamos considerar", "Analisando de forma lógica" — são resíduos de cadeia de raciocínio vazando para a prosa publicada. O leitor não precisa ver o andaime. Diga a conclusão, depois a evidência.

### Tom bajulador
- "Ótima pergunta!", "Excelente ponto!", "Você está absolutíssimo!", "Que observação perspicaz" — são recompensas de conversa de interface de chat, não escrita. Remova por completo.
- Diferente dos resíduos de chatbot: a bajulação valida especificamente o leitor/perguntador em vez de só performar prestatividade.

### Laços de reconhecimento
- "Você está perguntando sobre", "A questão de se", "Para responder à sua pergunta", "Ótima pergunta. A..." — a IA reenuncia o prompt antes de responder. Em texto, é puro enchimento. O leitor sabe o que perguntou. Responda.
- Padrão relacionado: abrir uma seção resumindo o que a seção anterior disse. Se a estrutura é clara, o leitor não precisa da recapitulação.

### Frases de calibragem de confiança
- "Vale ressaltar que", "Curiosamente", "Surpreendentemente", "Importante", "Notavelmente", "Sem dúvida", "Inegavelmente" — a IA usa para sinalizar como o leitor deve se sentir sobre um fato em vez de deixar o fato falar.
- "Eis o que é interessante", "Aqui está a parte interessante" — deixa que pré-interpreta a importância. Funciona quando seguida de dado genuinamente surpreendente; falha quando introduz a repetição de algo óbvio (o padrão da IA).
- Um "notavelmente" num texto de 2.000 palavras é aceitável. Três em 500 é empilhamento de ênfase estilo IA. Sinalize por densidade.
- Relacionado — **clichês de autoridade persuasiva**: "a verdadeira questão é", "em sua essência", "fundamentalmente", "não se engane", "a verdade é que". Mesmo movimento das frases acima, mas afirmam profundidade ou peso em vez de sentimento: anunciam que o que vem é importante em vez de mostrar. Corte o clichê e vá à substância.

### Autorrotulagem de importância
- Depois de listar ou descrever vários itens, quem escreve aponta de volta para um e o rotula como contraintuitivo / esperto / surpreendente / chave: "Esse último movimento é o contraintuitivo", "Esta é a parte interessante", "Aquele terceiro item é a história de verdade", "É aqui que fica engenhoso".
- O rótulo faz o trabalho que o conteúdo deveria fazer. Se um movimento é mesmo contraintuitivo, o leitor reconhece pela descrição; se não é reconhecível sem o rótulo, o rótulo não foi conquistado.
- Correção: corte a frase de rotulagem e deixe a explicação seguinte fazer o trabalho. Ou reestruture para o item que você queria destacar vir primeiro ou com mais detalhe, tornando o rótulo redundante.

### Excesso de estrutura
- Títulos demais em texto curto: mais de 3 títulos em menos de 300 palavras quase sempre é IA tentando parecer organizada. Junte seções ou use transições em prosa.
- Itens de lista demais: 8+ marcadores em menos de 200 palavras significa que o conteúdo deveria ser parágrafo, não lista.
- Títulos de seção formulaicos: "Visão geral", "Pontos principais", "Resumo", "Conclusão", "Introdução" — andaime padrão de IA. Use títulos que digam algo específico sobre o que vem.

### Ritmo e uniformidade

Não são problemas de palavra ou frase isolada — são padrões de como o texto flui como um todo. Texto de IA é metronômico; texto humano tem ritmo variado.

**Estrutura é o sinal de detecção nº 1.** Ferramentas de detecção de IA pesam a regularidade estrutural acima do vocabulário. Construção de frase consistente, ritmo uniforme e fraseado simétrico são mais difíceis de mascarar do que trocar algumas palavras sinalizadas. Se você corrigir todas as palavras do Nível 1 mas deixar o ritmo intacto, o texto ainda lê como IA.

- **Uniformidade no tamanho das frases**: Se a maioria tem 15-25 palavras, soa robótico. Misture frases curtas e secas (3-8 palavras) com outras longas e fluidas (20+). Fragmentos funcionam. Perguntas quebram a monotonia.
- **Uniformidade no tamanho dos parágrafos**: Se todo parágrafo tem 3-5 frases e mais ou menos o mesmo tamanho, varie de propósito. Alguns parágrafos deveriam ter uma frase. Outros, ser mais longos.
- **Repetição de vocabulário vs. ciclagem de sinônimos**: A IA ou repete a mesma palavra mecanicamente ou cicla sinônimos de forma vistosa. Quem escreve bem repete quando a palavra é certa e varia quando é natural — sem fórmula.
- **Teste de leitura em voz alta**: Se o texto pudesse ser lido por uma voz sintetizada sem soar estranho, provavelmente está uniforme demais. Escrita humana tem ritmo que resiste à leitura robótica.
- **Ausência de primeira pessoa**: Onde cabe, quem escreve deveria ter opiniões, preferências e reações. A IA é implacavelmente neutra. Se o texto deveria ter voz, a ausência de "eu acho", "na minha experiência" ou de uma preferência declarada já é uma marca de IA.
- **Polimento excessivo**: Editar agressivamente toda irregularidade pode empurrar a escrita humana *na direção* do perfil estatístico da IA. Disfluência natural, escolhas idiossincráticas e ritmo irregular são o que mantêm o texto fora da classificação "gerado por IA". Não lixe toda a personalidade em nome da prosa limpa. Esta skill deve fazer o texto soar mais humano, não menos.

### Diversidade de vocabulário (estilométrica)

Em textos mais longos (200+ palavras), olhe quanto vocabulário o texto de fato usa. A razão tipo-token (TTR) — tipos de palavra distintos divididos pelo total de tokens — é um sinal estilométrico clássico, fácil de ler a olho. Prosa humana neste tamanho costuma ficar em torno de 0,50-0,65. Texto de IA tende a ser mais raso, às vezes caindo abaixo de 0,40 quando o modelo trava num vocabulário pequeno.

Uma TTR muito baixa não é, por si só, prova de autoria de IA — tópicos estreitos, material técnico de referência e escrita em segunda língua comprimem vocabulário de forma legítima. Mas em prosa geral onde se esperaria amplitude (ensaios, artigos, conteúdo de rede social acima de ~200 palavras), uma TTR abaixo de 0,40 merece um segundo olhar. A correção raramente é passar dicionário de sinônimos; é ampliar o *o quê* — nomear coisas específicas, citar casos específicos, trocar um substantivo abstrato reaproveitado pela instância concreta por trás dele.

### Imunidade ao embaralhamento de parágrafos (teste de estrutura)
- Um diagnóstico para quem escreve, não um regex: dá para trocar dois parágrafos do corpo sem quebrar o texto? Se a ordem não importa, você escreveu uma lista de pontos, não um argumento que se constrói. Prosa de IA costuma falhar nisso — cada parágrafo é um módulo autocontido sem conexão de carga com o vizinho.
- A correção é estrutural, não lexical: estabeleça um fio condutor em que cada parágrafo dependa do anterior. Se os parágrafos são mesmo independentes, decida se o texto deveria ser uma lista explícita, ou se está faltando uma tese.

### Efeito esteira / baixa densidade de informação (teste de conteúdo)
- Outro teste para quem escreve: leia cada parágrafo e pergunte "o que de fato é novo aqui?". Prosa de IA reenuncia a premissa com palavras novas em vez de avançá-la — muito movimento, pouca distância percorrida. A marca é que você poderia cortar 40-60% sem perder informação.
- A correção: para cada parágrafo, nomeie o único fato, afirmação ou virada que ele contribui. Se não houver, corte. Se houver, comece por ele e tire o pigarro.

### Quando reescrever do zero vs. remendar

Se o texto tem 5+ palavras sinalizadas em várias categorias, 3+ categorias de padrão distintas acionadas e tamanho uniforme de frase/parágrafo, remendar expressões individuais não resolve — a própria estrutura é gerada por IA. Recomende reescrita total: enuncie o ponto central numa frase, depois reconstrua a partir dela.

---

## Níveis de severidade

Nem toda marca de IA é igual. Numa passada rápida ou ao triar um documento grande, priorize por nível:

### P0 — Mata-credibilidade (corrigir já)
- Avisos de corte de conhecimento ("Até a minha última atualização")
- Resíduos de chatbot ("Espero que ajude!", "Ótima pergunta!")
- Atribuições vagas sem fonte ("Especialistas acreditam")
- Inflação de importância em eventos rotineiros
- Excesso de hashtags em posts de `linkedin` e `email-investidor`

### P1 — Cara de IA óbvia (corrigir antes de publicar)
- Violações da tabela de palavras (mergulhar, alavancar, robusto, abrangente, etc.)
- Frases de molde e construções de preencher-lacuna
- Aberturas com "Vamos"
- Ciclagem de sinônimos dentro de um parágrafo
- Aberturas formulaicas ("No mundo em rápida transformação de...")
- Excesso de negrito
- Frequência de travessões (acima de 1 a cada 1.000 palavras)
- Fechamentos de futuro-genéricos ("pode se tornar uma das narrativas mais importantes…")
- Fechamentos de endosso social ("esse vale o seu tempo:", "depois me agradece")
- Previsões com atenuação empilhada ("poderia eventualmente", "pode acabar")
- Inflação com "real/verdadeiro" ("tokenomics real on-chain")
- Listas de sintagmas nominais soltos (5+ itens curtos de adj+substantivo, sem verbo)
- Aglomerado de expressões de Nível 3 (≥3 clichês distintos num texto)

### P2 — Polimento estilístico (corrigir quando der)
- Conclusões genéricas ("O futuro é promissor")
- Regra de três compulsiva
- Tamanho uniforme de parágrafo
- Fuga do verbo de ligação (serve como, ostenta, apresenta)
- Conectores (Ademais, Outrossim, Adicionalmente)
- Excesso de hashtags (perfis `blog`/`blog-tecnico`)
- Repetição de expressão de Nível 3 (uma expressão ≥2×)

Use P0+P1 para passadas rápidas. A auditoria completa cobre os três níveis.

---

## Escotilha de autorreferência

Ao escrever *sobre* padrões de escrita de IA (posts de blog, tutoriais, documentação de skill como este arquivo), exemplos citados ficam isentos de sinalização. Texto entre aspas, em blocos de código, ou marcado explicitamente como ilustrativo ("por exemplo, a IA poderia escrever...") não deve ser reescrito. Só sinalize padrões na prosa do próprio autor, não em exemplos citados de escrita ruim.

---

## Perfis de contexto

Passe uma dica opcional de contexto para ajustar o rigor das regras. Se nada for especificado, detecte automaticamente por pistas do conteúdo (curto + hashtags = social, blocos de código = técnico, saudação = e-mail, padrão = blog).

### Definição dos perfis

**`linkedin`** — Rede social de formato curto. Fragmentos secos e formatação visual importam.
**`blog`** — Padrão. Prosa longa comum. Todas as regras em força máxima.
**`blog-tecnico`** — Texto longo com código, arquitetura, APIs. Termos técnicos têm passe.
**`email-investidor`** — Público de alta confiança. Aperte tudo; linguagem promocional é o maior risco.
**`docs`** — Documentação, READMEs, guias. Clareza acima de voz.
**`casual`** — Mensagens de Slack, notas internas, respostas rápidas. Só pegue os piores casos.

### Matriz de tolerância

Regras não listadas na tabela valem em força máxima em todos os perfis.

| Regra | linkedin | blog | blog-tecnico | email-investidor | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Travessões | relaxado (2/post OK) | rígido | rígido | rígido | relaxado | pular |
| Excesso de negrito | relaxado (negrito-gancho OK) | rígido | rígido | rígido | relaxado | pular |
| Emoji em títulos | relaxado (1-2 no fim de linha) | rígido | rígido | rígido | pular | pular |
| Excesso de bullets | pular (listas funcionam no LinkedIn) | rígido | relaxado (listas técnicas OK) | rígido | pular (listas são docs) | pular |
| Atenuação | rígido | rígido | relaxado ("pode" é preciso em técnico) | rígido | relaxado | pular |
| Tabela de palavras (lista completa) | rígido | rígido | **parcial** (ver abaixo) | rígido | relaxado | só P0 |
| Linguagem promocional | relaxado (alguma venda é esperada) | rígido | rígido | **extra rígido** | rígido | pular |
| Inflação de importância | rígido | rígido | rígido | **extra rígido** | relaxado | pular |
| Fuga do verbo de ligação | pular | rígido | relaxado | rígido | pular | pular |
| Parágrafo uniforme | pular (formato curto) | rígido | rígido | rígido | relaxado | pular |
| Inflação de lista numerada | relaxado | rígido | relaxado | rígido | pular | pular |
| Perguntas retóricas | relaxado (1 como gancho OK) | rígido | rígido | rígido | rígido | pular |
| Conectores | pular (formato curto) | rígido | rígido | rígido | relaxado | pular |
| Conclusões genéricas | pular | rígido | rígido | **extra rígido** | pular | pular |
| Excesso de hashtags | rígido | rígido | rígido | **extra rígido** | pular (não há hashtag em docs) | pular |
| Listas de sintagmas soltos | rígido | rígido | relaxado (listas de opções técnicas OK) | rígido | relaxado (listas de parâmetro OK) | pular |
| Aglomerado de expressões N3 | rígido | rígido | rígido | **extra rígido** | relaxado | pular |
| Fechamentos de futuro-genéricos | rígido | rígido | rígido | **extra rígido** | pular | pular |
| Fechamentos de endosso social | rígido (a marca do post de LinkedIn) | rígido | rígido | rígido | pular | relaxado (1 OK num DM) |
| Previsões com atenuação empilhada | rígido | rígido | relaxado ("pode" é precisão atenuada) | **extra rígido** | relaxado | pular |
| Inflação com real/verdadeiro | rígido | rígido | rígido | **extra rígido** | relaxado | pular |

**Exceções da tabela de palavras em blog-tecnico:** Estes termos têm sentido técnico legítimo e não devem ser sinalizados em contexto técnico: `robusto`, `abrangente`, `ecossistema`, `alavancar` (quando se fala de alavancagem real de plataforma/API), `facilitar`, `sustentar`, `otimizar`. Ainda sinalize: `mergulhar`, `tapeçaria`, `farol`, `embarcar`, `prova viva de`, `divisor de águas`, `desvendar`.

**"Extra rígido"** significa: sinalize até casos limítrofes. Num e-mail a investidor, um único "ecossistema próspero" pode minar a mensagem inteira.

**"Pular"** significa: não audite esta categoria neste perfil.

### Pistas de detecção automática

Quando nenhum contexto é especificado, infira por estes sinais:

| Sinal | Contexto inferido |
|--------|-----------------|
| Menos de 300 palavras + hashtags ou menções | `linkedin` |
| Blocos de código, referências de API ou arquitetura técnica | `blog-tecnico` |
| Saudação ("Olá [nome]", "Prezado") + linguagem de investimento/captação | `email-investidor` |
| Instruções passo a passo, docs de parâmetro, estrutura de README | `docs` |
| Nenhum sinal forte | `blog` (padrão mais seguro — todas as regras valem) |

Se a detecção automática parecer errada, diga qual perfil está usando e por quê. A pessoa pode sobrescrever.

---

## Perfis de voz

Os perfis de contexto (acima) definem *o quão rígido* ser para um público. Os perfis de voz definem *como a prosa deve soar* — a persona. São eixos independentes: dá para escrever direto num blog ou acolhedor numa doc. Voz é **opcional** — se a pessoa não nomear uma, infira pelo registro existente do texto e não imponha uma persona a um texto que já tem uma.

Cada perfil é um conjunto de metas concretas, não um clima:

**`casual`** — Contrações e coloquialismos naturais; a ausência soa dura. Frases curtas (mire ≤14 palavras em média); fragmentos permitidos. Ao menos um toque de primeira pessoa ou anedota concreta. Quase zero jargão. Mantenha atenuações calorosas ("sinceramente", "eu acho") mas corte as corporativas ("vale ressaltar"). *Posts de blog, social, comunidade.*

**`profissional`** — Voz ativa na maioria das frases. Varie o tamanho; evite três frases iguais em sequência. Uma afirmação concreta por parágrafo (um número, um nome, uma data), nunca "dizem os especialistas". Deixe o pedido explícito. Baixa tolerância a atenuação. *LinkedIn, e-mail a investidor, propostas.*

**`tecnico`** — Prefira o verbo de ligação simples ("X é Y") aos substitutos inflados ("serve como", "configura-se como"). Uma ideia por frase; modo imperativo para instruções. Jargão é aceitável, mas defina no primeiro uso. Tabelas e listas só onde o conteúdo é genuinamente em lista, não de enfeite. *Docs, blog técnico.*

**`acolhedor`** — Fale com o leitor diretamente ("você") e reconheça-o ao menos uma vez. Corte intensificadores ("muito", "verdadeiramente", "incrivelmente") em favor de verbos mais fortes. Sem aberturas de empatia performática ("eu entendo perfeitamente como você se sente"). Frases médias (15-20 palavras) para um ritmo sem pressa. *Mentoria, onboarding, agradecimentos.*

**`direto`** — Comece pela afirmação; corte os preâmbulos "é importante notar que". Travessões são raros aqui; use ponto final para dar ênfase. Sem enchimento para bater a regra de três. Quase zero atenuação; sinalize empilhamentos de "pode / poderia / potencialmente". Declarativas curtas, com uma frase longa ocasional para contraste. *Memos de decisão, posicionamento, feedback duro.*

**Calibrar por amostra (opcional).** Se a pessoa der uma amostra da própria escrita ("imita minha voz — toma esse post"), analise o padrão de tamanho de frase, a taxa de coloquialismo, as aberturas de parágrafo e as escolhas de palavra recorrentes, e imite isso em vez de um perfil nomeado. Não "melhore" o vocabulário: se a pessoa escreve "coisa" e "negócio", mantenha o registro.

**Como voz se combina com contexto.** A voz define a meta; o contexto define o rigor da imposição. Uma *meta* de voz sempre vale, mesmo onde um perfil de contexto pularia a categoria — voz `tecnico` ainda prefere verbo de ligação simples num contexto `casual` que ignoraria a fuga do verbo de ligação. Onde os dois eixos governam a mesma regra e concordam, reforçam-se. Onde discordam, resolva para o **mais rígido** dos dois. Pares-padrão sensatos: casual↔casual, profissional↔linkedin/email-investidor, tecnico↔docs/blog-tecnico.

---

## Formato de saída

### Modo reescrever (padrão)

Devolva sua resposta em quatro seções:

**1. Problemas encontrados**
Lista com marcadores de toda marca de IA identificada, com o texto problemático citado.

**2. Versão reescrita**
O conteúdo reescrito por completo. Preserve a estrutura, a intenção e todos os detalhes técnicos específicos do original. Mude só o que as diretrizes exigem.

**3. O que mudou**
Resumo breve das edições principais. Não palavra por palavra, só as mudanças relevantes.

**4. Auditoria de segunda passada**
Releia a versão reescrita da seção 2. Identifique marcas de IA que sobreviveram à primeira passada — transições recicladas, inflação remanescente, fuga do verbo de ligação, enchimento, ou qualquer coisa das categorias acima. Corrija, devolva o texto corrigido inline e anote o que mudou nesta passada. Se a reescrita estiver limpa, diga isso.

### Modo detectar

Devolva sua resposta em duas seções:

**1. Problemas encontrados**
Lista com marcadores de toda marca de IA identificada, com o texto problemático citado. Agrupe por severidade (P0, P1, P2).

**2. Avaliação**
Para cada sinalização, indique se é um problema claro ou um julgamento de valor. Alguns padrões associados à IA são técnicas eficazes de escrita — parágrafo uniforme é problema, mas um "no entanto" bem colocado não é. Aponte quais sinalizações a pessoa definitivamente deve corrigir vs. quais merecem um segundo olhar mas podem estar OK no contexto. Se o texto está limpo, diga isso.

### Modo editar

Depois de editar o arquivo no lugar, devolva um relatório curto — não o arquivo inteiro:

**1. Edições feitas**
Lista com marcadores das mudanças, cada uma com o local no arquivo e o antes → depois. Só os trechos que você tocou.

**2. Verificação**
Confirme que releu o arquivo e que os padrões sinalizados foram resolvidos. Anote o que deixou de propósito por já estar humano ou ser intencional.

---

## Calibragem de tom

A meta é escrita que soa como pessoa escreveu. Direta. Específica. A escrita deve demonstrar confiança, não afirmá-la.

Cinco princípios para reescritas que soam humanas:
1. **Varie o tamanho das frases** — misture curtas e longas. Fragmentos são aceitáveis.
2. **Seja concreto** — troque afirmações vagas por números, nomes, datas ou exemplos.
3. **Tenha voz** — onde cabe, use primeira pessoa, declare preferências, mostre reações.
4. **Corte a neutralidade** — pessoas têm opiniões. Se o texto deve tomar posição, tome.
5. **Conquiste a ênfase** — não diga ao leitor que algo é interessante. Torne interessante.

Se o texto original já é bom, diga isso e faça só os cortes necessários. Não edite demais por editar.

A tabela de substituições oferece padrões, não mandatos. Se uma palavra sinalizada é claramente a escolha certa no contexto, preserve-a.
