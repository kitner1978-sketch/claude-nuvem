---
name: revisao-dirigida-set2026
description: "Revisão fina de 21/09/2026 aplicada ao Markdown do 2tb e DOCX regenerado; o que foi corrigido, o que eu errei no caminho e o que o pipeline não cobre"
metadata: 
  node_type: memory
  type: project
  originSessionId: ae3de0e0-4c37-4476-94b7-0b2c8cf90231
  modified: 2026-09-21T23:12:07.164Z
---

Em 2026-09-21 revisei os 23 capítulos (Markdown do **2tb**), apliquei correções, incorporei 360 edições da revisora Ingrid Moura, corrigi o gerador e gerei `output/livro_completo - 21 de set 26.docx` (cópia na raiz do seagate). **Nada foi commitado** no 2tb. Relatórios: `/Volumes/seagate/Projeto Livro/output/revisao_set2026_varredura.md` e `revisao_set2026_aplicada.md`.

Erros de direito encontrados e corrigidos (todos conferidos em fonte):
- Cap. 3: cronologia do art. 27-A invertida (correto: Lei 13.457/2017 = metade; MP 871/2019 = integral; Lei 13.846/2019 = metade). Art. 24 p.ú. revogado desde 06/01/2017. Tema 176/TNU acrescentado.
- Cap. 4: CEBAS é LC 187/2021 (revogou a Lei 12.101); tese do Tema 32/STF na redação dos embargos; art. 15, I (não II).
- Caps. 4 e 5: **"Súmula 74 da TNU" inventada** sobre rural sem recolhimento (a 74 real é prescrição) → Súmula 24/TNU + Súmula 272/STJ.
- Cap. 18: Tema 185/STJ diz presunção **absoluta** abaixo de ¼; o Tema 122/TNU é que diz **relativa**. O erro do livro era o título/citação da seção 18.13, não as linhas que diziam "absoluta".
- Cap. 21: Tema 629/STJ é extinção sem mérito por falta de prova (caso rural); a aplicação a incapacidade é extensão doutrinária.
- 11 teses e 2 súmulas estavam parafraseadas entre aspas; restauradas ao literal.

**Dois erros meus nesta sessão, para não repetir:**
1. Afirmei que o Informativo STF 1220 dava "rel. Zanin, 29/05/2026" para a ADI 6.309. Era o **final do item anterior** colado no mesmo recorte da base (começava com vírgula). Os dados do livro (j. 03/06/2026, 6×5, Barroso relator originário) estão certos. A memória `adi-6309-idade-minima` do projeto `aposentadoria_especial` (caminho `-Volumes-Untitled-Projeto-Livro`) tem o mesmo engano.
2. Minha ferramenta de transporte de edições truncou 3 capítulos; recuperei de backup feito antes.

**Why:** a verificação v13 (mai/2026) conferiu número/relator/data de Temas, mas não o **teor entre aspas**, não cobriu **súmulas** e nada conferiu a **narrativa legislativa** (quem incluiu/revogou, qual redação vigorou quando).

**How to apply:** ao ler recorte de RAG de informativo, conferir se o trecho começa no meio de outro item antes de atribuir relator/data. Antes de editar em lote, copiar os arquivos e conferir tamanho/linhas depois de cada etapa. Pendente antes da publicação: conferir citações literais de **lei e doutrina** (não cobertas), acórdão da ADI 6.309, tese publicada do Tema 1.157/STJ, estado do Tema 1.271/STF. Decisões do autor em aberto: grafia "salário-mínimo" (adotei a da revisora, exceto em citação literal) e numeração de Introdução/Conclusão. Ver [[revisao-ingrid-set2026]], [[duas-copias-divergentes]].
