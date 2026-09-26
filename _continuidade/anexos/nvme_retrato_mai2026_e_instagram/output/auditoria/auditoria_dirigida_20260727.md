# Auditoria dirigida — 27/07/2026

**Origem:** conferência de precedentes feita para o calendário editorial do Instagram (marketing/calendario_editorial_90dias.md, seção 1-A) revelou padrões de erro no método "ementa + trecho de voto". Esta auditoria verifica se os mesmos padrões contaminaram os capítulos escritos.

**Método:** grep dirigido + leitura dos trechos relevantes. Não substitui a revisão de aprovação; aponta risco confirmado.

---

## cap_18 (BPC) — 3 achados, 2 exigem correção

### A18.1 — CORRIGIR · Presunção "absoluta" contradiz a TNU sem enfrentá-la
**Local:** §146 ("Entendemos que o critério legal de 1/4 do salário mínimo é parâmetro objetivo de presunção **absoluta** de miserabilidade").
**Problema:** o Tema 122 da TNU fixa presunção **relativa** ("pode ser afastada por outros elementos de prova"). A Reclamação 0000302-22 (item 11 do voto) registra expressamente a divergência com o STJ (Tema 185/REsp 1.112.557 — absoluta). O capítulo adota a linha do STJ como se fosse pacífica, sem citar o tema do órgão uniformizador dos JEFs — que é o público do livro.
**Correção sugerida:** manter a posição autoral, mas enfrentar a divergência: expor Tema 122 TNU × Tema 185 STJ e justificar a opção. Vira ponto forte do capítulo.

### A18.2 — CORRIGIR · Genro/nora "incluídos no grupo" = vias transversas
**Local:** §162 ("se genro ou nora contribuem efetivamente para o sustento do requerente e compartilham despesas domésticas de forma indissociável, sua **inclusão no grupo familiar** pode ser justificada").
**Problema:** é a conduta cassada na Reclamação 0000302-22 — reintroduzir no grupo, pela via da contribuição de fato, quem o rol taxativo exclui. A contribuição de fato pode pesar na **análise global da miserabilidade**, nunca na **composição do grupo/cálculo per capita**. São planos distintos, e o capítulo os funde.
**Correção sugerida:** reescrever o parágrafo separando os planos; citar [[TNU_Tema_73]] e [[TNU_Reclamacao_0000302-22]].

### A18.3 — ENRIQUECER · Tema 73 ausente; divergência interna não explorada
**Local:** §§152–154. O texto afirma a interpretação restritiva e diz que "a obrigação alimentar do CC não se confunde com a composição do grupo" — alinhado à linha textual — mas não cita o Tema 73, seu alcance temporal declarado ("redação original" / questão limitada ao pré-12.435/2011), nem a linha divergente do art. 1.695 CC (recusada em 0003636-52, reafirmada em 1001528-59 `⚠ conferir resultado`).
**Sugestão:** seção própria sobre (a) a questão intertemporal do Tema 73 e (b) as duas linhas de fundamentação. Material já verificado na ficha [[TNU_Tema_73]].

## Capítulos de tempo especial e rural — verificação pendente

Nenhum capítulo aprovado ou rascunho cita TNU Temas 174, 208, 213 ou 301 (grep em output/). Duas hipóteses: os capítulos correspondentes (tempo especial; rural) ainda não foram escritos, ou foram escritos sem esses precedentes — o que seria lacuna grave. **Verificar contra config/book_structure.yaml antes de redigi-los; usar as fichas novas como base.**

**Armadilha de homônimo detectada:** cap_14 cita corretamente "Tema 174/STF (RE 587.365)" — auxílio-reclusão. Não confundir com Tema 174/TNU (ruído). Padronizar sempre tribunal + número.

## Regra de método (extraída dos erros da conferência)

1. Tese se cita pelo **registro do tema**, não por ementa de julgado aplicador.
2. Conferir **qual voto prevaleceu** antes de expor a ratio (erro real: fundamento do voto vencido de 0003636-52 quase publicado como razão de decidir).
3. Ementa pode citar "Questão de Ordem" com número errado (caso "QO 20" × processo 0000020-09).
4. Temas homônimos entre tribunais: sempre qualificar.
