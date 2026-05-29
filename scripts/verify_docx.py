"""Verify all typographic XML attributes in the generated DOCX."""
import zipfile
import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'D:\Projeto Livro\output\livro_completo.docx'
ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'
MC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'

checks = {}

with zipfile.ZipFile(docx_path) as z:
    # ── 1. Document settings ──
    settings_xml = z.read('word/settings.xml')
    root = ET.fromstring(settings_xml)

    ah = root.find('.//w:autoHyphenation', ns)
    checks['autoHyphenation'] = 'OK' if ah is not None else 'MISSING'

    hz = root.find('.//w:hyphenationZone', ns)
    if hz is not None:
        checks['hyphenationZone'] = 'OK (val=' + hz.get(W + 'val', '?') + ')'
    else:
        checks['hyphenationZone'] = 'MISSING'

    chl = root.find('.//w:consecutiveHyphenLimit', ns)
    if chl is not None:
        checks['consecutiveHyphenLimit'] = 'OK (val=' + chl.get(W + 'val', '?') + ')'
    else:
        checks['consecutiveHyphenLimit'] = 'MISSING'

    csc = root.find('.//w:characterSpacingControl', ns)
    if csc is not None:
        checks['characterSpacingControl'] = 'OK (val=' + csc.get(W + 'val', '?') + ')'
    else:
        checks['characterSpacingControl'] = 'MISSING'

    tfl = root.find('.//w:themeFontLang', ns)
    if tfl is not None:
        checks['themeFontLang'] = 'OK (val=' + tfl.get(W + 'val', '?') + ')'
    else:
        checks['themeFontLang'] = 'MISSING'

    # ── 2. Compat settings ──
    compat = root.find('.//w:compat', ns)
    if compat is not None:
        compat_settings = compat.findall('.//w:compatSetting', ns)
        found_compat = {}
        for cs in compat_settings:
            name = cs.get(W + 'name', '')
            val = cs.get(W + 'val', '')
            found_compat[name] = val

        for key in ['autoSpaceLikeWord95', 'adjustLineHeightInTable', 'compatibilityMode']:
            if key in found_compat:
                checks['compat:' + key] = 'OK (val=' + found_compat[key] + ')'
            else:
                checks['compat:' + key] = 'MISSING'
    else:
        checks['compat'] = 'MISSING (no compat element)'

    # ── 3. Normal style w:lang ──
    styles_xml = z.read('word/styles.xml')
    sroot = ET.fromstring(styles_xml)
    normal = None
    for s in sroot.findall('.//w:style', ns):
        sid = s.get(W + 'styleId', '')
        if sid == 'Normal':
            normal = s
            break
    if normal is not None:
        rpr = normal.find('.//w:rPr', ns)
        if rpr is not None:
            lang = rpr.find('.//w:lang', ns)
            if lang is not None:
                checks['Normal style w:lang'] = 'OK (val=' + lang.get(W + 'val', '?') + ')'
            else:
                checks['Normal style w:lang'] = 'MISSING'
        else:
            checks['Normal style w:lang'] = 'MISSING (no rPr)'
    else:
        checks['Normal style'] = 'MISSING'

    # ── 4. Document XML analysis ──
    doc_xml = z.read('word/document.xml')
    droot = ET.fromstring(doc_xml)

    # mc:Ignorable includes w14
    mc_ign = droot.get(MC + 'Ignorable', '')
    if 'w14' in mc_ign.split():
        checks['mc:Ignorable w14'] = 'OK (' + mc_ign + ')'
    else:
        checks['mc:Ignorable w14'] = 'MISSING (got: ' + mc_ign + ')'

    # ── 5. Drop caps (w:framePr with dropCap) ──
    all_framePr = droot.findall('.//w:framePr', ns)
    drop_caps = [f for f in all_framePr if f.get(W + 'dropCap') == 'drop']
    checks['w:framePr dropCap'] = 'OK (' + str(len(drop_caps)) + ' capitulares)'

    # ── 6. Run-level: kern, lang, ligatures ──
    all_runs = droot.findall('.//w:r', ns)
    total = len(all_runs)
    t_kern = 0
    t_lang = 0
    t_lig = 0
    for r in all_runs:
        rpr = r.find('w:rPr', ns)
        if rpr is not None:
            if rpr.find('w:kern', ns) is not None:
                t_kern += 1
            if rpr.find('w:lang', ns) is not None:
                t_lang += 1
            # w14:ligatures — need to search with full namespace
            lig_elems = [child for child in rpr if child.tag == W14 + 'ligatures']
            if lig_elems:
                t_lig += 1

    pct_kern = 100 * t_kern / total if total else 0
    pct_lang = 100 * t_lang / total if total else 0
    pct_lig = 100 * t_lig / total if total else 0
    checks['w:kern total'] = str(t_kern) + '/' + str(total) + ' (' + format(pct_kern, '.1f') + '%)'
    checks['w:lang total'] = str(t_lang) + '/' + str(total) + ' (' + format(pct_lang, '.1f') + '%)'
    checks['w14:ligatures total'] = str(t_lig) + '/' + str(total) + ' (' + format(pct_lig, '.1f') + '%)'

    # Ligature value sample
    if t_lig > 0:
        for r in all_runs[:50]:
            rpr = r.find('w:rPr', ns)
            if rpr is not None:
                for child in rpr:
                    if child.tag == W14 + 'ligatures':
                        val = child.get(W14 + 'val', '?')
                        checks['w14:ligatures val'] = 'OK (' + val + ')'
                        break
                if 'w14:ligatures val' in checks:
                    break

print('=== VERIFICACAO DOCX COMPLETA ===')
print('=== Hifenizacao + Anti-Rio + Capitulares + Ligaduras ===')
print()
for k, v in checks.items():
    status = '[OK]' if 'OK' in v or '%' in v else '[!!]'
    print('  ' + status + ' ' + k + ': ' + v)
print()
print('=== Verificacao concluida ===')
