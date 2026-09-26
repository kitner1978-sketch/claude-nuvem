#!/usr/bin/env python3
"""Gera os cards de carrossel do Instagram (1080x1350) a partir de um spec JSON.

Uso: python3 scripts/gerar_cards.py marketing/capas/carrossel_NN/spec.json [--png] [--camadas]
--png      renderiza PNGs via Chrome headless
--camadas  emite também card_N_bg / card_N_fg (fundo e texto separados, para o Reel)
Identidade: papel #EDE6D8, tinta #17150F, vermelhão #6B2318, painel #E2D8C3.
"""
import json, os, subprocess, sys, html

PAPEL, TINTA, VERM, PAINEL, CLARO = "#EDE6D8", "#17150F", "#6B2318", "#E2D8C3", "#C79A80"
SERIF = "EB Garamond, Georgia, serif"
SANS = "Inter, Helvetica, Arial, sans-serif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
e = html.escape


def txt(x, y, s, fam, size, fill, ls=None, w=None, anchor=None):
    a = f' letter-spacing="{ls}"' if ls else ''
    wt = f' font-weight="{w}"' if w else ''
    an = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}"{wt}{a}{an} fill="{fill}">{e(s)}</text>'


def linhas(x, y0, lh, ls_, fam, size, fill):
    out, y = [], y0
    for ln in ls_:
        out.append(txt(x, y, ln, fam, size, fill))
        y += lh
    return out, y


def card_parts(c, dark=False):
    """Retorna (fundo, frente): fundo = papel/faixa/numeral/rodapé; frente = conteúdo."""
    bg_fill = TINTA if dark else PAPEL
    fg = PAPEL if dark else TINTA
    ac = CLARO if dark else VERM
    bg = [f'<rect width="1080" height="1350" fill="{bg_fill}"/>',
          f'<rect width="1080" height="104" fill="{VERM}"/>',
          txt(88, 66, c["header"], SANS, 26, PAPEL, ls=6, w=500)]
    if c.get("num"):
        op = 0.05 if dark else 0.07
        bg.append(f'<text x="640" y="1180" font-family="{SERIF}" font-size="420" fill="{VERM if not dark else PAPEL}" opacity="{op}">{c["num"]}</text>')
    fr = []

    if c["tipo"] == "capa":
        fr.append(txt(88, 290, c["kicker"], SANS, 27, VERM, ls=5, w=500))
        fr.append(f'<rect x="88" y="332" width="120" height="5" fill="{VERM}"/>')
        y = 470
        for ln in c["titulo"]:
            fr.append(txt(88, y, ln, SERIF, 92, TINTA)); y += 112
        by = y + 42
        bw = 68 + len(c["badge"]) * 24
        fr.append(f'<rect x="88" y="{by}" width="{bw}" height="86" fill="{VERM}"/>')
        fr.append(txt(122, by + 56, c["badge"], SANS, 30, PAPEL, ls=5, w=500))
        sy = by + 190
        for ln in c.get("sub", []):
            fr.append(txt(88, sy, ln, SERIF, 46, TINTA + '" opacity="0.75')); sy += 56
        pag = "ARRASTE →"
    else:
        if c.get("titulo"):
            fr.append(txt(88, 252, c["titulo"], SERIF, c.get("tsize", 62), fg))
            fr.append(f'<rect x="88" y="292" width="904" height="1" fill="{fg}" opacity="0.28"/>')
        y = c.get("y0", 386)
        for tipo, dado in c.get("blocos", []):
            if tipo == "sans":
                ls_, y = linhas(88, y, 58, dado, SANS, 40, fg); fr += ls_; y += 44
            elif tipo == "serif":
                ls_, y = linhas(88, y, 70, dado, SERIF, 58, fg); fr += ls_; y += 44
            elif tipo == "barra":
                h = 70 * len(dado) + 20
                fr.append(f'<rect x="88" y="{y - 52}" width="6" height="{h}" fill="{ac}"/>')
                ls_, y = linhas(136, y, 70, dado, SERIF, 58, fg); fr += ls_; y += 44
            elif tipo == "painel":
                kick = dado.get("kicker")
                lns = dado["linhas"]
                h = 62 * len(lns) + (66 if kick else 0) + 76
                fr.append(f'<rect x="88" y="{y - 46}" width="904" height="{h}" fill="{PAINEL}"/>')
                yy = y + 20
                if kick:
                    fr.append(txt(128, yy, kick, SANS, 26, VERM, ls=4, w=500)); yy += 66
                ls_, yy = linhas(128, yy, 62, lns, SERIF, 50, TINTA); fr += ls_
                y = yy + 74
            elif tipo == "lista":
                for item in dado:
                    cont = item.startswith("~")
                    t = item[1:] if cont else item
                    if not cont:
                        fr.append(f'<rect x="88" y="{y - 14}" width="22" height="4" fill="{ac}"/>')
                    fr.append(txt(140, y, t, SANS, 38, fg)); y += 62
                y += 30
            elif tipo == "prec":
                fr.append(txt(88, y, "PRECEDENTES", SANS, 25, ac, ls=3)); y += 52
                for ln in dado:
                    fr.append(txt(88, y, ln, SANS, 27, fg + '" opacity="0.85')); y += 44
                y += 20
        if c.get("ref"):
            fr.append(txt(88, 1160, c["ref"], SANS, 25, ac, ls=2))
        pag = c.get("pag", "")
    fy = 1176 if c["tipo"] == "fecho" else 1216
    bg.append(f'<rect x="88" y="{fy}" width="904" height="1" fill="{fg}" opacity="0.28"/>')
    if c.get("hashtags"):
        bg.append(txt(88, fy + 58, c["hashtags"], SANS, 26, ac))
        bg.append(txt(88, fy + 116, "@LUIZ.BISPO.12", SANS, 24, fg + '" opacity="0.72', ls=3))
        bg.append(txt(992, fy + 116, pag, SANS, 24, ac, ls=3, anchor="end"))
    else:
        bg.append(txt(88, fy + 56, "@LUIZ.BISPO.12", SANS, 24, fg + '" opacity="0.72', ls=3))
        bg.append(txt(992, fy + 56, pag, SANS, 24, ac, ls=3, anchor="end"))
    return bg, fr


def svg(parts):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">'
            + '\n'.join(parts) + '</svg>')


def render(svg_path, png_path, transparente=False):
    extra = ["--default-background-color=00000000"] if transparente else []
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1350",
                    *extra, f"--screenshot={png_path}", f"file://{svg_path}"],
                   capture_output=True)


def main():
    """Estrutura por post:
    posts/post_NN_tema/           spec.json + legenda.txt
      publicar/                   SOMENTE o que sobe: {slug}_card_01.png ...
      producao/                   SVGs e camadas bg/fg (uso interno)
    """
    spec_path = sys.argv[1]
    render_png = "--png" in sys.argv
    camadas = "--camadas" in sys.argv
    raiz = os.path.dirname(os.path.abspath(spec_path))
    with open(spec_path) as f:
        spec = json.load(f)
    slug = spec.get("slug") or os.path.basename(raiz)
    pub = os.path.join(raiz, "publicar")
    prod = os.path.join(raiz, "producao")
    n = len(spec["cards"])
    for i, c in enumerate(spec["cards"], 1):
        c.setdefault("num", f"{i:02d}")
        if c["tipo"] != "capa":
            c.setdefault("pag", f"{i} / {n}")
        bg, fr = card_parts(c, dark=(c["tipo"] == "fecho"))
        alvos = {f"card_{i}": bg + fr}
        if camadas:
            alvos[f"card_{i}_bg"] = bg
            alvos[f"card_{i}_fg"] = fr
        for nome, parts in alvos.items():
            os.makedirs(prod, exist_ok=True)
            p = os.path.join(prod, f"{nome}.svg")
            with open(p, "w") as f:
                f.write(svg(parts))
            if render_png and os.path.exists(CHROME):
                if nome.endswith(("_bg", "_fg")):
                    dest = os.path.join(prod, f"{nome}.png")
                else:
                    os.makedirs(pub, exist_ok=True)
                    dest = os.path.join(pub, f"{slug}_card_{i:02d}.png")
                render(p, dest, transparente=nome.endswith("_fg"))
        print(f"card_{i}: ok" + (" (+bg/fg)" if camadas else ""))


if __name__ == "__main__":
    main()
