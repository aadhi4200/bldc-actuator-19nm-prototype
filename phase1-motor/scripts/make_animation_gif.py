"""Render the rotor flux animation to an animated GIF for the README.

Same model as animation/bldc_v1_rotor_flux_animation.html: each tooth's polarity = coil sign x phase current,
currents timed for maximum torque. One electrical cycle (360/14 deg of rotor turn) repeats exactly, so the GIF
loops seamlessly.

Usage: python phase1-motor/scripts/make_animation_gif.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import params as P

PATTERN = "AabBCcaABbcC" * 2
PP = P.POLES // 2
R = dict(bore=P.R_BORE, yoke=P.R_YOKE, shoe=P.R_SHOE, od=P.R_OD,
         mi=P.R_MAG_IN, mo=P.R_MAG_IN + P.ARC_MAG_T, ro=P.ROTOR_RING_OD / 2)
SS = 2                      # supersampling for smooth edges
W, H = 520, 640
CX, CY, SC = 260, 250, 4.6
RED, BLUE, GREY = (226, 75, 74), (55, 138, 221), (180, 179, 172)
PH_COL = [(226, 75, 74), (29, 158, 117), (127, 119, 221)]
OUT = Path(__file__).resolve().parent.parent / "animation" / "bldc_v1_rotor_flux_animation.gif"

ph = lambda t: "ABC".index(t.upper())
sg = lambda t: 1 if t.isupper() else -1
phi = lambda k: k * 2 * math.pi / P.SLOTS


def best_timing():
    best = (-1e9, None, None)
    for seq in ([0, -1, 1], [0, 1, -1]):
        for i in range(72):
            d = math.radians(i * 5)
            T = 0.0
            for n in range(60):
                tm = n / 60 * 2 * math.pi / PP * 2
                te = PP * tm
                for k in range(P.SLOTS):
                    p = PATTERN[k]
                    T += math.cos(te + d + seq[ph(p)] * 2 * math.pi / 3) * sg(p) * math.sin(PP * (phi(k) - tm))
            if T > best[0]:
                best = (T, d, seq)
    return best[1], best[2]


DELTA, SEQ = best_timing()
cur = lambda p, te: math.cos(te + DELTA + SEQ[p] * 2 * math.pi / 3)


def pt(r, a):
    return ((CX + r * SC * math.cos(a)) * SS, (CY - r * SC * math.sin(a)) * SS)


def ring_poly(r1, r2, a1, a2, n=16):
    return [pt(r2, a1 + (a2 - a1) * i / n) for i in range(n + 1)] + \
           [pt(r1, a1 + (a2 - a1) * i / n) for i in range(n, -1, -1)]


def blend(c, a):
    return tuple(int(255 + (ci - 255) * a) for ci in c)


def frame(tm, font, small):
    img = Image.new("RGB", (W * SS, H * SS), "white")
    d = ImageDraw.Draw(img)
    te = PP * tm
    d.polygon(ring_poly(R["mo"], R["ro"], 0, 2 * math.pi, 120), fill=blend(GREY, 0.6))
    hp = math.pi / P.POLES * P.ARC_POLE_ARC
    for j in range(P.POLES):
        a = tm + j * 2 * math.pi / P.POLES
        d.polygon(ring_poly(R["mi"], R["mo"], a - hp, a + hp, 6), fill=BLUE if j % 2 else RED)
    d.polygon(ring_poly(R["bore"], R["yoke"], 0, 2 * math.pi, 120), fill=blend(GREY, 0.7))
    hw, op = P.TOOTH_WIDTH / 2, math.asin(P.SLOT_OPENING / 2 / R["od"])
    sh = math.pi / P.SLOTS - op
    for k in range(P.SLOTS):
        a, p = phi(k), PATTERN[k]
        v = sg(p) * cur(ph(p), te)
        ca, sa = math.cos(a), math.sin(a)
        q = lambda r, o: ((CX + (r * ca - o * sa) * SC) * SS, (CY - (r * sa + o * ca) * SC) * SS)
        poly = [q(R["yoke"] - 0.3, -hw), q(R["shoe"], -hw), pt(R["shoe"], a - sh)]
        poly += [pt(R["od"], a - sh + 2 * sh * i / 8) for i in range(9)]
        poly += [pt(R["shoe"], a + sh), q(R["shoe"], hw), q(R["yoke"] - 0.3, hw)]
        d.polygon(poly, fill=blend(RED if v >= 0 else BLUE, 0.15 + 0.85 * min(1, abs(v))),
                  outline=(150, 150, 150))
        lx, ly = pt(33, a)
        d.text((lx, ly), p, fill=(40, 40, 40), font=small, anchor="mm")
    d.text((CX * SS, (CY - 8) * SS), "stator (fixed)", fill=(110, 110, 105), font=small, anchor="mm")
    d.text((CX * SS, (CY + 10) * SS), "rotor turns", fill=(110, 110, 105), font=small, anchor="mm")
    # phase currents
    y0, amp, x0, x1 = 545, 38, 50, 500
    d.line([(x0 * SS, y0 * SS), (x1 * SS, y0 * SS)], fill=(200, 200, 195), width=SS)
    for p in range(3):
        pts = []
        for i in range(301):
            e = te - 2 * math.pi + i / 300 * 4 * math.pi
            pts.append(((x0 + (x1 - x0) * i / 300) * SS, (y0 - amp * cur(p, e)) * SS))
        d.line(pts, fill=PH_COL[p], width=2 * SS)
        d.text((18 * SS, (y0 - 30 + p * 22) * SS), "ABC"[p], fill=PH_COL[p], font=font, anchor="lm")
    xm = (x0 + x1) / 2
    d.line([(xm * SS, (y0 - amp - 6) * SS), (xm * SS, (y0 + amp + 6) * SS)], fill=(60, 60, 60), width=SS)
    d.text(((xm + 4) * SS, (y0 + amp + 4) * SS), "now", fill=(90, 90, 90), font=small, anchor="lt")
    d.text((W / 2 * SS, 20 * SS), "24N28P: teeth become electromagnets that pull the magnets around",
           fill=(40, 40, 40), font=small, anchor="mm")
    d.text((W / 2 * SS, 485 * SS), "red = N, blue = S   |   phase currents A, B, C (14 cycles per rotor turn)",
           fill=(90, 90, 90), font=small, anchor="mm")
    return img.resize((W, H), Image.LANCZOS)


def main():
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15 * SS)
        small = ImageFont.truetype("DejaVuSans.ttf", 12 * SS)
    except OSError:
        font = small = ImageFont.load_default()
    n = 48
    period = 2 * math.pi / PP          # one electrical cycle of rotor turn: frame n == frame 0
    frames = [frame(i / n * period, font, small) for i in range(n)]
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=60, loop=0, optimize=True)
    print(OUT.name, f"{OUT.stat().st_size / 1024:.0f} KB, {n} frames")


if __name__ == "__main__":
    main()
