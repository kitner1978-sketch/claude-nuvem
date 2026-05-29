import re
import sys

path = r'D:\Projeto Livro\output\rascunhos\cap_06_rascunho.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Word count
text_only = re.sub(r'[#|:\-{}\[\]>*_~`]', ' ', content)
text_only = re.sub(r'\s+', ' ', text_only).strip()
words = len(text_only.split())
print(f'Word count: {words}')

# Count sections
h3 = re.findall(r'^### \d+\.\d+', content, re.MULTILINE)
h4 = re.findall(r'^#### \d+\.\d+\.\d+', content, re.MULTILINE)
print(f'H3 sections: {len(h3)}')
print(f'H4 subsections: {len(h4)}')

# Count boxes
pratica = len(re.findall(r'^::: pratica', content, re.MULTILINE))
atencao = len(re.findall(r'^::: atencao', content, re.MULTILINE))
jurisprudencia = len(re.findall(r'^::: jurisprudencia', content, re.MULTILINE))
total_boxes = pratica + atencao + jurisprudencia
print(f'Boxes: {total_boxes} ({pratica} pratica + {atencao} atencao + {jurisprudencia} jurisprudencia)')

# Check box closure
open_boxes = len(re.findall(r'^:::\s+(pratica|atencao|jurisprudencia)', content, re.MULTILINE))
close_boxes = len(re.findall(r'^:::\s*$', content, re.MULTILINE))
print(f'Box open/close: {open_boxes} open, {close_boxes} close')
if open_boxes != close_boxes:
    print('WARNING: box open/close MISMATCH!')
else:
    print('Box open/close: OK')

# Count references
ref_section = content.split('## REFER')
if len(ref_section) > 1:
    refs = re.findall(r'^[A-Z]', ref_section[1], re.MULTILINE)
    print(f'References: {len(refs)}')

# Check Lei n. consistency
lei_n_dot = len(re.findall(r'Lei n\.', content))
lei_no = len(re.findall(r'Lei no\.', content))
lei_num = len(re.findall(r'Lei n\xba', content))
print(f'"Lei n." (correct): {lei_n_dot}')
if lei_no > 0:
    print(f'WARNING: "Lei no." found: {lei_no}')
if lei_num > 0:
    print(f'WARNING: "Lei n\xba" found: {lei_num}')

# Section numbering sequence
section_strs = re.findall(r'^### (\d+)\.(\d+)', content, re.MULTILINE)
prev_sub = 0
gaps = []
for ch, sub in section_strs:
    curr = int(sub)
    if curr != prev_sub + 1:
        gaps.append(f'{ch}.{prev_sub} -> {ch}.{curr}')
    prev_sub = curr

if gaps:
    print(f'Section gaps: {gaps}')
else:
    print('Section numbering: sequential OK')

print('\nFormatador check complete')
