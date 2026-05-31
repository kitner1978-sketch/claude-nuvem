# Verificação de Jurisprudência — Capítulo 16 (Cálculo do Benefício: SB e RMI)

**Arquivo verificado:** `D:\Projeto Livro\output\rascunhos\cap_16_rascunho.md`
**Bases oficiais:** STJ (temas.csv / processos.csv), STF (temas_repercussao_geral_stf.xlsx), TNU (temas_representativos_tnu.csv)
**Data da verificação:** 2026-05-30

---

## Tabela de citações

| Citação | Tipo | Veredito | Dado oficial | Correção |
|---------|------|----------|--------------|----------|
| Tema 76/STF — RE 564.354, Rel. Cármen Lúcia, j. 08/09/2010 (readequação ao teto ECs 20/98 e 41/03) | Tema STF | ✅ | Tema 76; RE 564354; Rel. MIN. CÁRMEN LÚCIA; j. 08/09/2010; "Não ofende o ato jurídico perfeito a aplicação imediata do art. 14 da EC 20/1998 e do art. 5º da EC 41/2003 aos benefícios... de modo a que passem a observar o novo teto constitucional." | — |
| Tema 1300/STF — RE 1.469.150, Rel. Luís Roberto Barroso, j. 18/12/2025 (constitucionalidade do coef. 60%+2% na incap. permanente não acidentária) | Tema STF | 🚩 (dispositivo) | Tema 1300; RE 1469150; Rel. MIN. LUÍS ROBERTO BARROSO; j. 18/12/2025; tese: "É constitucional o pagamento do benefício de aposentadoria por incapacidade permanente nos termos fixados pelo **art. 26, § 2º, III, da EC 103/2019** para os casos em que a incapacidade... seja constatada posteriormente à Reforma." | Processo, relator e data ✅. Erro: o capítulo cita o fundamento como **"art. 26, §§ 2º e 3º, inciso I"** (3x); a tese oficial diz **"art. 26, § 2º, III"**. Ajustar a remissão do dispositivo. |
| Tema 1102/STF — RE 1.276.977, Rel. p/ acórdão Alexandre de Moraes (orig.) / Nunes Marques (embargos) | Tema STF | ✅ (com ressalva externa) | Tema 1102; RE 1276977; Rel. MIN. ALEXANDRE DE MORAES; j. 01/12/2022 (mérito); tese de cogência do art. 3º da Lei 9.876/99 + modulação (irrepetibilidade até 05/04/2024; inexigibilidade de sucumbência p/ ações pendentes até essa data) | Processo, relator do mérito e modulação ✅ na base (mérito 2022 + modulação 2024). A REVERSÃO de 26/11/2025 (embargos infringentes, tese revertida, Rel. p/ acórdão Nunes Marques) **NÃO consta da base** — conferir externamente (não tratado como erro). |
| Tema 905/STJ — REsp 1.495.146/MG, Rel. Mauro Campbell, j. 22/02/2018 (correção monetária) | Tema STJ | ✅ | Tema 905; REsp 1495146 (leadingCase=S); Rel. MAURO CAMPBELL MARQUES; j. 22/02/2018; pub. 02/03/2018; S1 | — |
| Tema 995/STJ — Rel. Mauro Campbell, j. 22/10/2019 (reafirmação da DER) | Tema STJ | ✅ | Tema 995; Rel. MAURO CAMPBELL MARQUES; j. 22/10/2019; pub. 02/12/2019; S1; leadingCase REsp 1.727.063; tese de reafirmação da DER (arts. 493 e 933 CPC) | — |
| Tema 1070/STJ — REsp 1.870.793/RS e 1.870.815/RS, **Rel. Gurgel de Faria**, 1ª Seção, j. 11/05/2022, trânsito 13/02/2023 (soma de concomitantes) | Tema STJ | ⚠️ (relator) | Tema 1070; processos REsp 1.870.793 (leading=S) e 1.870.815 (leading=N) ✅; j. 11/05/2022 ✅; pub. 24/05/2022; tese de soma das contribuições concomitantes ✅. **Campo ministroRelator na base = SÉRGIO KUKINA** (relator sorteado/de afetação), não Gurgel de Faria. | Processos, data e tese conferem. Divergência apenas no relator: a base registra o relator de afetação (Kukina); o capítulo indica Gurgel de Faria (provável relator p/ acórdão). Conferir manualmente qual constou no acórdão final. |
| ADI 2.110/DF e 2.111/DF — Rel. Nunes Marques, j. 21/03/2024 (constitucionalidade/cogência do art. 3º da Lei 9.876/99) | ADI STF | ⚠️ fora da base | Não há base de ADIs. Consistente com a modulação referida na tese oficial do Tema 1102 (data 05/04/2024 = publicação da ata do mérito das ADIs 2.110/2.111). | Conferir manualmente (relator e data 21/03/2024). |
| ADI 2.111 (constitucionalidade do fator previdenciário, j. 21/03/2024) — seção 16.4.3 | ADI STF | ⚠️ fora da base | Não há base de ADIs. | Conferir manualmente. |
| Súmula 85/STJ (prescrição quinquenal de parcelas) | Súmula | ⚠️ fora da base | — | Conferir manualmente. |
| TNU — PEDILEF 0513964-82.2017.4.05.8300 (rejeição de índice mais favorável ao INPC) | TNU | ❓ | **Não localizado** na base de temas representativos da TNU (396 temas). PEDILEF individual pode não constar do rol de temas representativos. | Conferir manualmente (a base só cataloga temas representativos, não todos os PEDILEFs). |
| RE 199.994, Rel. Marco Aurélio (irredutibilidade vs. paridade com SM) — seção 16.8 | Julgado STF | ⚠️ fora da base | Não é tema de repercussão geral catalogado na planilha. | Conferir manualmente. |

---

## Lista de correções "X" → "Y" (com linha)

1. **Linha 226** (box-jurisprudencia Tema 1300) — fundamento do dispositivo:
   - "X": *"o coeficiente de cálculo previsto no **art. 26, §§ 2º e 3º, inciso I**, da EC 103/2019"*
   - "Y": conferir contra a tese oficial, que se reporta ao **"art. 26, § 2º, III, da EC 103/2019"**.
   - Observação: a tese oficial do STF (Tema 1300) fixa o fundamento como "art. 26, § 2º, **III**", e não "§§ 2º e 3º, I". Recomenda-se alinhar a remissão (ou explicitar que a doutrina/coeficiente está nos §§ 2º e 3º, I, mas a TESE FIRMADA refere o § 2º, III).

2. **Linhas 211, 271, 594** (texto e Quadros 16.2 e 16.6) — referências ao fundamento da aposentadoria por incapacidade permanente não acidentária como "art. 26, §§ 2º e 3º, I":
   - Coerentes entre si, mas divergem do dispositivo citado na tese oficial do Tema 1300 ("art. 26, § 2º, III"). Avaliar uniformização. (Não é erro de tese, é de remissão ao inciso/parágrafo.)

3. **Linhas 423, 430, 688** (Tema 1070/STJ) — relator:
   - "X": *"Rel. Min. **Gurgel de Faria**"*
   - "Y": a base oficial do STJ registra **Sérgio Kukina** como ministroRelator (relator sorteado/de afetação) dos REsp 1.870.793 e 1.870.815. Confirmar manualmente o relator p/ acórdão do julgamento de 11/05/2022 antes de alterar — pode haver redistribuição (afetação Kukina → acórdão Gurgel de Faria). ⚠️ Não corrigir cegamente.

---

## Verificações pontuais solicitadas (calibração do capítulo de Cálculo)

- **Tema 76/STF** (readequação ao teto, RE 564.354, Rel. Cármen Lúcia): ✅ tudo confere (processo, relator, data 08/09/2010, tese).
- **Tema 1300/STF** (60%+2%, RE 1.469.150, Rel. Barroso — não Fux; j. 18/12/2025): ✅ processo, relator (Barroso, confirmado — NÃO Fux), data 18/12/2025. 🚩 única ressalva: dispositivo citado ("§§ 2º e 3º, I") difere da tese oficial ("§ 2º, III").
- **Tema 1070/STJ** (concomitantes, Lei 9.876/99): ✅ tese, processos e data; ⚠️ relator divergente na base (Kukina vs. Gurgel de Faria).
- **Tema 905/STJ** (correção monetária, REsp 1.495.146, Rel. Mauro Campbell): ✅ tudo confere.
- **Tema 1102/STF** (vida toda): base traz mérito 01/12/2022 + modulação 05/04/2024. A reversão de nov/2025 narrada no capítulo **NÃO consta da base** — sinalizado para conferência externa, sem tratar como erro (conforme instrução).

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de citações verificadas | 11 |
| ✅ Corretas (base confirma) | 5 (Temas 76, 905, 995, 1070-tese/processos/data, 1102-mérito) |
| 🚩 Erro/discrepância que a base contradiz | 1 (Tema 1300 — dispositivo "§§ 2º e 3º, I" vs. tese oficial "§ 2º, III") |
| ⚠️ Atenção / fora da base / divergência menor | 4 (Tema 1070 relator; ADIs 2.110/2.111; Súmula 85/STJ; RE 199.994) |
| ❓ Não localizado na base | 1 (PEDILEF TNU 0513964-82.2017.4.05.8300) |

**Erros críticos:**
1. 🚩 **Tema 1300/STF** — o fundamento citado no box e quadros ("art. 26, §§ 2º e 3º, inciso I") não coincide com o dispositivo da tese oficial ("art. 26, § 2º, III"). Processo (RE 1.469.150), relator (Barroso) e data (18/12/2025) estão corretos.
2. ⚠️ **Tema 1070/STJ** — relator: base registra Sérgio Kukina (afetação); capítulo cita Gurgel de Faria. Confirmar relator p/ acórdão antes de corrigir.
