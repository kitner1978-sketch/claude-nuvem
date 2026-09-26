const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
        PageBreak } = require('docx');
const fs = require('fs');

// Page setup: A4
const PAGE_WIDTH = 11906;
const MARGIN_LEFT = 1440;
const MARGIN_RIGHT = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT; // 9026

// Colors
const BLUE_DARK = "1B4F72";
const BLUE_MED = "2E86C1";
const BLUE_LIGHT = "D6EAF8";
const GREEN = "27AE60";
const ORANGE = "E67E22";
const GRAY = "7F8C8D";
const GRAY_LIGHT = "F2F3F4";

function createPartHeading(text) {
  return new Paragraph({
    spacing: { before: 400, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE_DARK, space: 4 } },
    children: [
      new TextRun({ text: text, bold: true, font: "Arial", size: 26, color: BLUE_DARK }),
    ],
  });
}

function createChapterRow(cap, titulo, status) {
  const isReady = status === "done";
  const statusText = isReady ? "Escrito" : "A escrever";
  const statusColor = isReady ? GREEN : ORANGE;
  const rowBg = isReady ? "F0FFF0" : "FFFAF0";

  const border = { style: BorderStyle.SINGLE, size: 1, color: "D5D8DC" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const margins = { top: 60, bottom: 60, left: 100, right: 100 };

  return new TableRow({
    children: [
      new TableCell({
        borders, margins,
        width: { size: 800, type: WidthType.DXA },
        shading: { fill: rowBg, type: ShadingType.CLEAR },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: String(cap), bold: true, font: "Arial", size: 20, color: BLUE_MED }),
        ]})],
      }),
      new TableCell({
        borders, margins,
        width: { size: 6826, type: WidthType.DXA },
        shading: { fill: rowBg, type: ShadingType.CLEAR },
        children: [new Paragraph({ children: [
          new TextRun({ text: titulo, font: "Arial", size: 20 }),
        ]})],
      }),
      new TableCell({
        borders, margins,
        width: { size: 1400, type: WidthType.DXA },
        shading: { fill: rowBg, type: ShadingType.CLEAR },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: statusText, bold: true, font: "Arial", size: 18, color: statusColor }),
        ]})],
      }),
    ],
  });
}

function createTable(chapters) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "ABB2B9" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const margins = { top: 60, bottom: 60, left: 100, right: 100 };

  const headerRow = new TableRow({
    children: [
      new TableCell({
        borders, margins,
        width: { size: 800, type: WidthType.DXA },
        shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: "Cap.", bold: true, font: "Arial", size: 18, color: "FFFFFF" }),
        ]})],
      }),
      new TableCell({
        borders, margins,
        width: { size: 6826, type: WidthType.DXA },
        shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
        children: [new Paragraph({ children: [
          new TextRun({ text: "Titulo", bold: true, font: "Arial", size: 18, color: "FFFFFF" }),
        ]})],
      }),
      new TableCell({
        borders, margins,
        width: { size: 1400, type: WidthType.DXA },
        shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: "Status", bold: true, font: "Arial", size: 18, color: "FFFFFF" }),
        ]})],
      }),
    ],
  });

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [800, 6826, 1400],
    rows: [headerRow, ...chapters.map(ch => createChapterRow(ch.cap, ch.titulo, ch.status))],
  });
}

// Build document
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "DIREITO PREVIDENCIARIO:", bold: true, font: "Arial", size: 28, color: BLUE_DARK }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "Teoria e Pratica nos Juizados Especiais Federais", font: "Arial", size: 24, color: BLUE_MED, italics: true }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: BLUE_MED, space: 8 } },
        children: [
          new TextRun({ text: "SUMARIO COMPLETO — Nova Estrutura (23 capitulos)", bold: true, font: "Arial", size: 24 }),
        ],
      }),

      // PARTE I
      createPartHeading("PARTE I — Fundamentos do Regime Geral de Previdencia Social"),
      createTable([
        { cap: 1, titulo: "Evolucao Historica e Principios Constitucionais", status: "done" },
        { cap: 2, titulo: "Segurados e Dependentes", status: "done" },
        { cap: 3, titulo: "Periodo de Carencia e Manutencao da Qualidade de Segurado", status: "done" },
        { cap: 4, titulo: "Contribuicoes Previdenciarias e Custeio do RGPS", status: "new" },
        { cap: 5, titulo: "Reconhecimento, Computo e Averbacao de Tempo de Contribuicao", status: "new" },
      ]),

      new Paragraph({ spacing: { before: 200 }, children: [] }),

      // PARTE II
      createPartHeading("PARTE II — Beneficios por Incapacidade"),
      createTable([
        { cap: 6, titulo: "Aposentadoria por Incapacidade Permanente", status: "done" },
        { cap: 7, titulo: "Auxilio por Incapacidade Temporaria", status: "done" },
      ]),

      new Paragraph({ spacing: { before: 200 }, children: [] }),

      // PARTE III
      createPartHeading("PARTE III — Aposentadorias Programadas"),
      createTable([
        { cap: 8, titulo: "Aposentadoria Especial", status: "done" },
        { cap: 9, titulo: "Aposentadoria do Segurado Rural", status: "done" },
        { cap: 10, titulo: "Aposentadoria Programada e Aposentadoria por Idade Urbana", status: "new" },
        { cap: 11, titulo: "Aposentadoria por Tempo de Contribuicao e Regras de Transicao", status: "new" },
        { cap: 12, titulo: "Aposentadoria da Pessoa com Deficiencia (LC 142/2013)", status: "new" },
      ]),

      new Paragraph({ spacing: { before: 200 }, children: [] }),

      // PARTE IV
      createPartHeading("PARTE IV — Pensoes, Auxilios e Beneficio Assistencial"),
      createTable([
        { cap: 13, titulo: "Salario-Maternidade", status: "new" },
        { cap: 14, titulo: "Auxilio-Reclusao", status: "new" },
        { cap: 15, titulo: "Auxilio-Acidente e Salario-Familia", status: "new" },
        { cap: 16, titulo: "Calculo do Beneficio — Salario de Beneficio e RMI", status: "new" },
        { cap: 17, titulo: "Revisao de Beneficios Previdenciarios", status: "new" },
        { cap: 18, titulo: "Beneficio de Prestacao Continuada (LOAS/BPC)", status: "done" },
        { cap: 19, titulo: "Pensao por Morte", status: "done" },
      ]),

      new Paragraph({ spacing: { before: 200 }, children: [] }),

      // PARTE V
      createPartHeading("PARTE V — Temas Transversais"),
      createTable([
        { cap: 20, titulo: "Acumulacao de Beneficios", status: "new" },
        { cap: 21, titulo: "Decadencia, Prescricao e Coisa Julgada Previdenciaria", status: "new" },
      ]),

      new Paragraph({ spacing: { before: 200 }, children: [] }),

      // PARTE VI
      createPartHeading("PARTE VI — Processo Previdenciario nos JEFs"),
      createTable([
        { cap: 22, titulo: "Processo Administrativo Previdenciario", status: "new" },
        { cap: 23, titulo: "Competencia e Procedimento no JEF", status: "done" },
      ]),

      // Summary section
      new Paragraph({ spacing: { before: 500 }, children: [] }),
      new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: BLUE_MED, space: 8 } },
        spacing: { before: 300, after: 200 },
        children: [
          new TextRun({ text: "RESUMO", bold: true, font: "Arial", size: 24, color: BLUE_DARK }),
        ],
      }),

      // Summary table
      new Table({
        width: { size: 5000, type: WidthType.DXA },
        columnWidths: [3500, 1500],
        rows: [
          createSummaryRow("Capitulos escritos", "10", GREEN),
          createSummaryRow("Capitulos a escrever", "13", ORANGE),
          createSummaryRow("Total de capitulos", "23", BLUE_DARK),
          createSummaryRow("Palavras estimadas (final)", "~300.000-350.000", GRAY),
        ],
      }),
    ],
  }],
});

function createSummaryRow(label, value, color) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "D5D8DC" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const margins = { top: 60, bottom: 60, left: 100, right: 100 };

  return new TableRow({
    children: [
      new TableCell({
        borders, margins,
        width: { size: 3500, type: WidthType.DXA },
        children: [new Paragraph({ children: [
          new TextRun({ text: label, font: "Arial", size: 20 }),
        ]})],
      }),
      new TableCell({
        borders, margins,
        width: { size: 1500, type: WidthType.DXA },
        shading: { fill: GRAY_LIGHT, type: ShadingType.CLEAR },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: value, bold: true, font: "Arial", size: 20, color: color }),
        ]})],
      }),
    ],
  });
}

// Generate
const outputPath = "D:\\Projeto Livro\\output\\docx\\sumario_livro.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("DOCX created: " + outputPath);
}).catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
