#!/usr/bin/env python3
"""Gera um Reel cinematográfico (1080x1920, mp4) a partir das camadas dos cards.

Movimento: o fundo desliza lateralmente (câmera de rostrum, direção alternada,
zoom fixo suave); o texto entra assentando (desliza 14px e desvanece) sobre o
fundo já em movimento. Ritmo variável por card (capa e fecho mais longos, ou
"dur" no spec.json). Abre e fecha em papel. Grão de filme sutil. Sem áudio —
a trilha entra na publicação, pela biblioteca do Instagram.

Pré-requisito: python3 scripts/gerar_cards.py <spec> --png --camadas
Uso: python3 scripts/gerar_reel.py marketing/capas/carrossel_02 reel_02.mp4
"""
import json
import os
import subprocess
import sys

FPS = 30
FADE = 0.8
PAPEL = "0xEDE6D8"
ZOOM = 1.055
CPS = 17.0        # caracteres por segundo — ritmo de leitura em tela pequena
BASE = 2.6        # respiro: entrada do texto + pausa antes da transição
MIN, MAX = 5.0, 11.0


def texto_do_card(c):
    """Concatena o texto legível do card, para dimensionar a duração."""
    p = []
    t = c.get("titulo")
    p += t if isinstance(t, list) else ([t] if t else [])
    p += [c.get("kicker", ""), c.get("badge", "")] + c.get("sub", [])
    for tipo, dado in c.get("blocos", []):
        if tipo == "painel":
            p += [dado.get("kicker", "")] + dado["linhas"]
        elif tipo == "prec":
            p += [d[:40] for d in dado]      # referências são varridas, não lidas
        elif tipo == "lista":
            p += [d.lstrip("~") for d in dado]
        else:
            p += dado
    return " ".join(x for x in p if x)


def duracao(c):
    if "dur" in c:
        return float(c["dur"])
    return round(min(MAX, max(MIN, BASE + len(texto_do_card(c)) / CPS)), 1)


def main():
    pasta = sys.argv[1].rstrip("/")
    png = os.path.join(pasta, "producao")
    with open(os.path.join(pasta, "spec.json")) as f:
        spec = json.load(f)
    cards = spec["cards"]
    slug = spec.get("slug") or os.path.basename(pasta)
    pub = os.path.join(pasta, "publicar")
    os.makedirs(pub, exist_ok=True)
    saida = os.path.join(pub, sys.argv[2] if len(sys.argv) > 2 else f"{slug}_reel.mp4")
    # subconjunto opcional para o Reel: "reel_cards": [1,4,6,7,8] (1-indexado)
    idx = [i - 1 for i in spec.get("reel_cards", range(1, len(cards) + 1))]
    durs = [duracao(cards[i]) for i in idx]
    n = len(idx)
    for k, i in enumerate(idx):
        print(f"  card_{i+1}: {durs[k]}s")

    cmd = ["ffmpeg", "-y"]
    for k, i in enumerate(idx):
        cmd += ["-i", os.path.join(png, f"card_{i+1}_bg.png")]
        cmd += ["-loop", "1", "-t", str(durs[k]), "-i", os.path.join(png, f"card_{i+1}_fg.png")]

    fc = []
    for i in range(n):
        d = int(durs[i] * FPS)
        pan = f"(iw-iw/zoom)*on/{d}" if i % 2 == 0 else f"(iw-iw/zoom)*(1-on/{d})"
        fc.append(
            f"[{2*i}:v]scale=2160:2700,zoompan=z='{ZOOM}':d={d}"
            f":x='{pan}':y='(ih-ih/zoom)/2':s=1080x1350:fps={FPS}[bg{i}]"
        )
        if i == 0:
            # hipótese 2: o vídeo abre já na capa completa — sem fade, sem assentamento
            fc.append(f"[{2*i+1}:v]fps={FPS},format=rgba[fg{i}]")
            ov = "overlay=x=0:y=0:shortest=1"
        else:
            fc.append(f"[{2*i+1}:v]fps={FPS},format=rgba,fade=t=in:st=0:d=0.9:alpha=1[fg{i}]")
            ov = "overlay=x=0:y='14*max(0,1-t/0.9)':shortest=1"
        # hipótese 3: card a 92%, erguido — paginação e referências fora da UI do player
        fc.append(
            f"[bg{i}][fg{i}]{ov},scale=994:1242,"
            f"pad=1080:1920:43:200:color={PAPEL},setsar=1[v{i}]"
        )
    prev, total = "v0", durs[0]
    for i in range(1, n):
        off = total - FADE
        fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[x{i}]")
        prev, total = f"x{i}", off + durs[i]
    fc.append(
        f"[{prev}]fade=t=out:st={total - 0.8:.2f}:d=0.8:color={PAPEL},"
        f"noise=alls=5:allf=t,format=yuv420p[vout]"
    )

    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]",
            "-c:v", "libx264", "-crf", "22", "-preset", "fast",
            "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-1200:])
    print(f"ok: {saida} ({total:.1f}s, {n} cards)")


if __name__ == "__main__":
    main()
