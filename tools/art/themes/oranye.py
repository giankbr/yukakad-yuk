"""Oranye — painted (gouache + ink) product thumbnails for the flash-sale seat cards.
Run: python3 -I /tmp/pen/art/themes/oranye.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p5_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/oranye"
PRE = "/tmp/pen/nt3-P5/oranye"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
W, H = 320, 190
rng = random.Random(7)
ORANGE, ORANGE2, WOOD, WOOD2, CREAM, CREAM2, INK, GOLD = "#ee5a3a", "#d8411f", "#c99467", "#a9744a", "#fbf2e6", "#efdcc8", "#3a2a24", "#e7bd55"

def chair(cx, base, scale=1.0, col=ORANGE, col2=ORANGE2, bow=False):
    """Upholstered armchair / banquet chair, 3/4 front, painted in gouache with an ink line."""
    s = scale
    art = blank(W, H)
    legs = [rr(cx - 42 * s, base - 30 * s, 9 * s, 34 * s, 3), rr(cx + 33 * s, base - 30 * s, 9 * s, 34 * s, 3),
            rr(cx - 30 * s, base - 36 * s, 7 * s, 28 * s, 3), rr(cx + 23 * s, base - 36 * s, 7 * s, 28 * s, 3)]
    for p in legs:
        art = over(art, paint(fill_mask(W, H, p), WOOD, WOOD2))
    seat = poly(wobbly([(cx - 52 * s, base - 40 * s), (cx + 52 * s, base - 40 * s), (cx + 46 * s, base - 16 * s), (cx - 46 * s, base - 16 * s)], rng, 0.015))
    back = rr(cx - 36 * s, base - 118 * s, 72 * s, 84 * s, 16 * s)
    armL = rr(cx - 56 * s, base - 72 * s, 20 * s, 36 * s, 8 * s)
    armR = rr(cx + 36 * s, base - 72 * s, 20 * s, 36 * s, 8 * s)
    art = over(art, shadow(W, H, seat, "#7a2e18", (4, 8), 8, 0.35))
    art = over(art, paint(fill_mask(W, H, back), col, col2))
    art = shade(art, W, H, rr(cx - 36 * s, base - 118 * s, 72 * s, 84 * s, 16 * s), "#7a3020", 0.18, 10)
    art = over(art, paint(fill_mask(W, H, seat), mix(col, "#ffffff", .12), col))
    for p in (armL, armR):
        art = over(art, paint(fill_mask(W, H, p), mix(col, "#ffffff", .08), col2))
    # tufting: three soft darker dots on the backrest
    for i in range(3):
        art = over(art, shadow(W, H, circ(cx + (i - 1) * 20 * s, base - 80 * s, 4 * s), "#8a3a22", (0, 0), 2.2, 0.55))
    if bow:   # banquet sash with a bow
        sash = poly(wobbly([(cx - 34 * s, base - 62 * s), (cx + 34 * s, base - 58 * s), (cx + 34 * s, base - 46 * s), (cx - 34 * s, base - 50 * s)], rng, 0.02))
        art = over(art, paint(fill_mask(W, H, sash), ORANGE, ORANGE2))
        loopL = oval(cx - 12 * s, base - 55 * s, 11 * s, 7 * s); loopR = oval(cx + 12 * s, base - 55 * s, 11 * s, 7 * s)
        tailL = poly([(cx - 2 * s, base - 52 * s), (cx - 12 * s, base - 30 * s), (cx - 4 * s, base - 32 * s)])
        tailR = poly([(cx + 2 * s, base - 52 * s), (cx + 12 * s, base - 30 * s), (cx + 4 * s, base - 32 * s)])
        for p in (tailL, tailR, loopL, loopR):
            art = over(art, paint(fill_mask(W, H, p), ORANGE, ORANGE2))
        art = over(art, paint(fill_mask(W, H, circ(cx, base - 55 * s, 4 * s)), ORANGE2))
        for p in (loopL, loopR):
            art = over(art, ink(W, H, p, 1.8, INK, 0.25))
    outline = skia.Path()
    for p in (back, armL, armR, seat) + tuple(legs):
        outline.addPath(p)
    art = over(art, ink(W, H, outline, 2.4, INK, 0.2))
    art = over(art, highlight(W, H, poly([(cx - 26 * s, base - 108 * s), (cx + 20 * s, base - 110 * s)], False), 0.5))
    return grain(art, nxt(), 0.04)

def vip(cx, base):
    """Gold-foil crown resting on a round VIP cushion."""
    art = blank(W, H)
    cushion = oval(cx, base - 26, 70, 22)
    art = over(art, shadow(W, H, cushion, "#7a2e18", (4, 10), 10, 0.4))
    art = over(art, paint(fill_mask(W, H, cushion), ORANGE, ORANGE2))
    art = shade(art, W, H, oval(cx, base - 14, 70, 14), "#7a3020", 0.3, 8)
    band = oval(cx, base - 32, 70, 20)
    art = over(art, paint(fill_mask(W, H, band), mix(ORANGE, "#ffffff", .14), ORANGE))
    art = over(art, ink(W, H, cushion, 2.2, INK, 0.22))
    # crown
    pts = [(cx - 44, base - 48), (cx - 44, base - 96), (cx - 22, base - 72), (cx, base - 108), (cx + 22, base - 72), (cx + 44, base - 96), (cx + 44, base - 48)]
    crown = poly(wobbly(pts, rng, 0.012))
    cm = fill_mask(W, H, crown)
    art = over(art, shadow(W, H, crown, "#5a2a10", (3, 5), 4, 0.4))
    art = over(art, foil(cm, GOLD, seed=nxt(), emboss=0.5, sparkle=0.12))
    base_band = rr(cx - 46, base - 60, 92, 14, 5)
    art = over(art, foil(fill_mask(W, H, base_band), "#c9983a", seed=nxt(), emboss=0.6, sparkle=0.1))
    for x, y in [(cx - 44, base - 98), (cx, base - 110), (cx + 44, base - 98)]:
        art = over(art, paint(fill_mask(W, H, circ(x, y, 5)), "#f3d27a", GOLD))
    for i in range(3):
        art = over(art, paint(fill_mask(W, H, circ(cx + (i - 1) * 26, base - 53, 4)), "#e8533a", "#b22a16"))
    art = over(art, ink(W, H, crown, 2.0, "#5a3a1a", 0.25))
    art = over(art, ink(W, H, base_band, 1.6, "#5a3a1a", 0.3))
    return grain(art, nxt(), 0.04)

def save(arr, name):
    size = save_asset(arr, f"{OUT}/{name}.webp", max_w=240, quality=82)
    preview(arr, f"{PRE}/{name}.png", "#ffeee8")
    print(name, size, "%.1f KB" % kb(f"{OUT}/{name}.webp"))

# 1. Kursi akad — one proper armchair
save(chair(160, 176, 1.05), "seat-akad")
# 2. Kursi resepsi — two banquet chairs with sashes
a = chair(118, 176, 0.86, CREAM, CREAM2, bow=True)
b = chair(206, 178, 0.86, CREAM, CREAM2, bow=True)
save(over(a, b), "seat-resepsi")
# 3. Meja VIP — crown on cushion
save(vip(160, 176), "seat-vip")
