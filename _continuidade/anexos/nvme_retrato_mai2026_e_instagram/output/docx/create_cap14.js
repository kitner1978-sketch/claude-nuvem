const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
        PageBreak, Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

// Page setup: A4
const PAGE_WIDTH = 11906;
const MARGIN_LEFT = 1440;
const MARGIN_RIGHT = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT;

// Colors
const BLUE_DARK = "1B4F72";
const BLUE_MED = "2E86C1";
const GREEN = "27AE60";
const GREEN_LIGHT = "E8F8F5";
const ORANGE = "E67E22";
const ORANGE_LIGHT = "FEF9E7";
const BLUE_LIGHT = "EBF5FB";
const GRAY = "566573";
const GRAY_LIGHT = "F2F3F4";

// Read the markdown file
const mdContent = fs.readFileSync('D:\\Projeto Livro\\output\\rascunhos\\cap_14_rascunho.md', 'utf8');

// Parse sections from markdown
function parseMarkdown(content) {
  const yamlEnd = content.indexOf('---', 3);
  const body = content.substring(yamlEnd + 3).trim();
  return body;
}

// Create a box (pratica, atencao, jurisprudencia)
function createBox(title, content, type) {
  let bgColor, borderColor, titleColor;
  if (type === 'pratica') {
    bgColor = GREEN_LIGHT; borderColor = GREEN; titleColor = GREEN;
  } else if (type === 'atencao') {
    bgColor = ORANGE_LIGHT; borderColor = ORANGE; titleColor = ORANGE;
  } else {
    bgColor = BLUE_LIGHT; borderColor = BLUE_MED; titleColor = BLUE_MED;
  }

  const border = { style: BorderStyle.SINGLE, size: 6, color: borderColor };
  const lines = content.split('\n').filter(l => l.trim());

  const children = [
    new Paragraph({
      spacing: { before: 60, after: 60 },
      children: [new TextRun({ text: title, bold: true, font: "Arial", size: 20, color: titleColor })],
    }),
  ];

  for (const line of lines) {
    const cleanLine = line.replace(/\*\*/g, '').replace(/\|/g, ' | ');
    // Detect checkbox items
    if (cleanLine.match(/^-\s*\[[\sx]\]/)) {
      children.push(new Paragraph({
        spacing: { before: 30, after: 30 },
        indent: { left: 200 },
        children: [new TextRun({ text: cleanLine.replace(/^-\s*/, ''), font: "Arial", size: 19 })],
      }));
    } else {
      children.push(new Paragraph({
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: cleanLine, font: "Arial", size: 19 })],
      }));
    }
  }

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: border, right: border },
            shading: { fill: bgColor, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            children: children,
          }),
        ],
      }),
    ],
  });
}

// Parse the markdown into document elements
function buildDocElements(body) {
  const elements = [];
  const lines = body.split('\n');
  let i = 0;
  let inBox = false;
  let boxType = '';
  let boxContent = '';
  let boxTitle = '';

  while (i < lines.length) {
    const line = lines[i];

    // Box start
    if (line.startsWith('::: pratica') || line.startsWith('::: atencao') || line.startsWith('::: jurisprudencia')) {
      inBox = true;
      boxType = line.replace('::: ', '').trim();
      boxContent = '';
      boxTitle = '';
      i++;
      continue;
    }

    // Box end
    if (line.startsWith(':::') && inBox) {
      if (boxContent.trim()) {
        elements.push(new Paragraph({ spacing: { before: 200 }, children: [] }));
        elements.push(createBox(boxTitle || boxType.toUpperCase(), boxContent, boxType));
        elements.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
      }
      inBox = false;
      boxContent = '';
      boxTitle = '';
      i++;
      continue;
    }

    // Inside box
    if (inBox) {
      if (!boxTitle && line.startsWith('**') && line.includes('**')) {
        boxTitle = line.replace(/\*\*/g, '').trim();
      } else {
        boxContent += line + '\n';
      }
      i++;
      continue;
    }

    // Chapter title (## Capítulo)
    if (line.startsWith('## Capítulo') || (line.startsWith('## ') && line.includes('Auxílio-Reclusão'))) {
      elements.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 100 },
        children: [
          new TextRun({ text: "PARTE IV", bold: true, font: "Arial", size: 20, color: GRAY }),
        ],
      }));
      elements.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 100, after: 100 },
        children: [
          new TextRun({ text: "Pensões, Auxílios e Benefício Assistencial", italic: true, font: "Arial", size: 20, color: GRAY }),
        ],
      }));
      elements.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 400 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLUE_MED, space: 8 } },
        children: [
          new TextRun({ text: line.replace('## ', ''), bold: true, font: "Arial", size: 32, color: BLUE_DARK }),
        ],
      }));
      i++;
      continue;
    }

    // Section heading (### )
    if (line.startsWith('### ')) {
      elements.push(new Paragraph({ spacing: { before: 100 }, children: [] }));
      elements.push(new Paragraph({
        spacing: { before: 360, after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE_MED, space: 4 } },
        children: [
          new TextRun({ text: line.replace('### ', ''), bold: true, font: "Arial", size: 26, color: BLUE_DARK }),
        ],
      }));
      i++;
      continue;
    }

    // Subsection heading (#### )
    if (line.startsWith('#### ')) {
      elements.push(new Paragraph({
        spacing: { before: 280, after: 140 },
        children: [
          new TextRun({ text: line.replace('#### ', ''), bold: true, font: "Arial", size: 23, color: BLUE_MED }),
        ],
      }));
      i++;
      continue;
    }

    // Table (starts with |)
    if (line.startsWith('|') && line.includes('|')) {
      const tableLines = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        if (!lines[i].includes('---')) {
          tableLines.push(lines[i]);
        }
        i++;
      }

      if (tableLines.length > 0) {
        const rows = tableLines.map(tl =>
          tl.split('|').filter(c => c.trim()).map(c => c.trim())
        );

        if (rows.length > 0) {
          const numCols = rows[0].length;
          const colWidth = Math.floor(CONTENT_WIDTH / numCols);
          const border = { style: BorderStyle.SINGLE, size: 1, color: "ABB2B9" };
          const borders = { top: border, bottom: border, left: border, right: border };

          const tableRows = rows.map((row, rowIdx) => {
            const isHeader = rowIdx === 0;
            while (row.length < numCols) row.push('');
            return new TableRow({
              children: row.slice(0, numCols).map(cell =>
                new TableCell({
                  borders,
                  width: { size: colWidth, type: WidthType.DXA },
                  shading: { fill: isHeader ? BLUE_DARK : (rowIdx % 2 === 0 ? GRAY_LIGHT : "FFFFFF"), type: ShadingType.CLEAR },
                  margins: { top: 50, bottom: 50, left: 80, right: 80 },
                  children: [new Paragraph({
                    children: [new TextRun({
                      text: cell.replace(/\*\*/g, ''),
                      bold: isHeader,
                      font: "Arial",
                      size: 18,
                      color: isHeader ? "FFFFFF" : "000000",
                    })],
                  })],
                })
              ),
            });
          });

          elements.push(new Paragraph({ spacing: { before: 160 }, children: [] }));
          elements.push(new Table({
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            columnWidths: Array(numCols).fill(colWidth),
            rows: tableRows,
          }));
          elements.push(new Paragraph({ spacing: { after: 160 }, children: [] }));
        }
      }
      continue;
    }

    // Numbered list items (1. 2. 3. etc)
    if (/^\d+\.\s/.test(line)) {
      const text = line.replace(/^\d+\.\s+/, '');
      elements.push(new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 360 },
        children: [
          new TextRun({ text: line.match(/^\d+/)[0] + '. ', bold: true, font: "Arial", size: 21 }),
          new TextRun({ text: text.replace(/\*\*/g, ''), font: "Arial", size: 21 }),
        ],
      }));
      i++;
      continue;
    }

    // List items (- or  -)
    if (line.startsWith('- ') || line.startsWith('  - ')) {
      const indent = line.startsWith('  - ') ? 720 : 360;
      const text = line.replace(/^-\s+/, '').replace(/^\s+-\s+/, '');
      elements.push(new Paragraph({
        spacing: { before: 40, after: 40 },
        indent: { left: indent },
        children: [
          new TextRun({ text: "• ", font: "Arial", size: 21 }),
          new TextRun({ text: text.replace(/\*\*/g, ''), font: "Arial", size: 21 }),
        ],
      }));
      i++;
      continue;
    }

    // Lettered/labeled items (a) b) c) or **A**, **Primeira: etc)
    if (/^[a-e]\)\s/.test(line) || /^\*\*[A-Z]/.test(line) || /^\*\*[a-z]\)/.test(line)) {
      elements.push(new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 360 },
        children: [
          new TextRun({ text: line.replace(/\*\*/g, ''), font: "Arial", size: 21 }),
        ],
      }));
      i++;
      continue;
    }

    // Bold paragraph starters (Cap 14 specific)
    if (line.startsWith('**Passo ') || line.startsWith('**Opção ') || line.startsWith('**Cenário ')
        || line.startsWith('**Exemplo') || line.startsWith('**Importante:')
        || line.startsWith('**Recomendação') || line.startsWith('**Observação')
        || line.startsWith('**Primeira fase') || line.startsWith('**Segunda fase')
        || line.startsWith('**Terceira fase') || line.startsWith('**Quarta fase')
        || line.startsWith('**Regime antigo') || line.startsWith('**Regime novo')
        || line.startsWith('**Posição ') || line.startsWith('**Posição restritiva')
        || line.startsWith('**Posição ampliativa') || line.startsWith('**Posição intermediária')
        || line.startsWith('**Posição majoritária') || line.startsWith('**Posição minoritária')
        || line.startsWith('**Manutenção') || line.startsWith('**Extensão')
        || line.startsWith('**Facultatividade') || line.startsWith('**Qualidade')
        || line.startsWith('**Segurado') || line.startsWith('**Segurada')
        || line.startsWith('**Monitoração') || line.startsWith('**Prisão domiciliar')
        || line.startsWith('**Prisão provisória') || line.startsWith('**Soltura')
        || line.startsWith('**Conversão') || line.startsWith('**Classe ')
        || line.startsWith('**Duração') || line.startsWith('**Rateio')
        || line.startsWith('**Progressão') || line.startsWith('**Regressão')
        || line.startsWith('**Regime semiaberto') || line.startsWith('**Regime fechado')
        || line.startsWith('**No âmbito') || line.startsWith('**No regime')
        || line.startsWith('**Requerimento') || line.startsWith('**Para dependentes')
        || line.startsWith('**Peculiaridade') || line.startsWith('**Múltiplas')
        || line.startsWith('**O sujeito') || line.startsWith('**O momento')
        || line.startsWith('**O parâmetro') || line.startsWith('**O que diz')
        || line.startsWith('**Evolução temporal') || line.startsWith('**Argumentos')
        || line.startsWith('**Flexibilização') || line.startsWith('**Prescrição')
        || line.startsWith('**Execução') || line.startsWith('**Instrução')
        || line.startsWith('**Competência') || line.startsWith('**Prévio')
        || line.startsWith('**Tutela') || line.startsWith('**Valor')
        || line.startsWith('**Antes') || line.startsWith('**Após')
        || line.startsWith('**Questão') || line.startsWith('**Morte')
        || line.startsWith('**MEI') || line.startsWith('**Preso ')
        || line.startsWith('**Trabalho') || line.startsWith('**Indulto')
        || line.startsWith('**Detração') || line.startsWith('**Recambiamento')
        || line.startsWith('**Pandemia') || line.startsWith('**Cumprimento')
        || line.startsWith('**Auxílio') || line.startsWith('**AR ')
        || line.startsWith('**Acumulação') || line.startsWith('**Dependente')
        || line.startsWith('**Consequência') || line.startsWith('**Tendência')
        || line.startsWith('**Aplicação') || line.startsWith('**Fundamento')
        || line.startsWith('**Relevância') || line.startsWith('**Referência')
        || line.startsWith('**Perspectivas') || line.startsWith('**Orientação')
        || line.startsWith('**Dica') || line.startsWith('**Ponto')
        || line.startsWith('**Nota') || line.startsWith('**Atenção')) {
      elements.push(new Paragraph({
        spacing: { before: 80, after: 80 },
        indent: { left: 360 },
        children: [
          new TextRun({ text: line.replace(/\*\*/g, ''), font: "Arial", size: 21 }),
        ],
      }));
      i++;
      continue;
    }

    // Regular paragraph
    if (line.trim() && !line.startsWith('#')) {
      const cleanLine = line.replace(/\*\*/g, '');
      elements.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        spacing: { before: 100, after: 100 },
        children: [
          new TextRun({ text: cleanLine, font: "Arial", size: 21 }),
        ],
      }));
    }

    i++;
  }

  return elements;
}

// Build the document
const body = parseMarkdown(mdContent);
const docElements = buildDocElements(body);

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
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "Cap. 14 — Auxílio-Reclusão", font: "Arial", size: 16, color: GRAY, italics: true }),
          ],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "— ", font: "Arial", size: 18, color: GRAY }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: GRAY }),
            new TextRun({ text: " —", font: "Arial", size: 18, color: GRAY }),
          ],
        })],
      }),
    },
    children: docElements,
  }],
});

// Generate
const outputPath = "D:\\Projeto Livro\\output\\docx\\cap_14.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("DOCX created: " + outputPath);
  console.log("Elements: " + docElements.length);
  console.log("File size: " + (buffer.length / 1024).toFixed(1) + " KB");
}).catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
