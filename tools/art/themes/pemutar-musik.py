"""Pemutar Musik — painted wishlist products (turntable, studio headphones, keyboard) in gouache + ink,
and a blush watercolour wash for the cover backdrop (replaces the CSS radial gradients; CSS keeps the drift).
Run: python3 -I /tmp/pen/art/themes/pemutar-musik.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p5_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/pemutar-musik"
PRE = "/tmp/pen/nt3-P5/pemutar-musik"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(44)
INK, RED, RED2, WOOD, WOOD2, CREAM, CREAM2, DARK, DARK2 = "#2a2426", "#fa2d48", "#c21a33", "#c99467", "#a9744a", "#fbf5ef", "#ebe2d6", "#3a3638", "#232022"

def turntable(W, H):
    cx, cy = W / 2, H / 2 + 6
    art = blank(W, H)
    plinth = rr(cx - 84, cy - 56, 168, 112, 14)
    art = over(art, shadow(W, H, plinth, "#000000", (5, 8), 9, 0.3))
    art = over(art, paint(fill_mask(W, H, plinth), WOOD, WOOD2))
    art = shade(art, W, H, rr(cx - 84, cy + 10, 168, 46, 12), "#6a3f1e", 0.3, 10)
    # platter + record
    art = over(art, paint(fill_mask(W, H, circ(cx - 14, cy, 48)), "#8f8a8c", "#5f5c58"))
    art = over(art, paint(fill_mask(W, H, circ(cx - 14, cy, 43)), "#1f1d1f", "#2e2a2d"))
    for r in (36, 29, 22):
        art = over(art, ink(W, H, circ(cx - 14, cy, r), 1.2, "#4a4548", 0.35))
    art = over(art, paint(fill_mask(W, H, circ(cx - 14, cy, 13)), RED, RED2))
    art = over(art, paint(fill_mask(W, H, circ(cx - 14, cy, 2.5)), CREAM))
    # tonearm
    arm = poly([(cx + 60, cy - 40), (cx + 8, cy - 6)], False)
    art = over(art, paint(fill_mask(W, H, circ(cx + 60, cy - 40, 9)), "#8f8a8c", "#5f5c58"))
    art = over(art, ink(W, H, arm, 5.0, "#b9b4b6", 0.0, 1.2))
    art = over(art, ink(W, H, arm, 1.6, INK, 0.1, 1.2))
    art = over(art, paint(fill_mask(W, H, rr(cx, cy - 12, 16, 10, 3)), DARK, DARK2))
    art = over(art, paint(fill_mask(W, H, circ(cx + 62, cy + 30, 7)), CREAM, CREAM2))   # knob
    art = over(art, ink(W, H, circ(cx + 62, cy + 30, 7), 1.6, INK, 0.2))
    art = over(art, ink(W, H, plinth, 2.6, INK, 0.2))
    art = over(art, ink(W, H, circ(cx - 14, cy, 48), 2.0, INK, 0.2))
    art = over(art, highlight(W, H, poly([(cx - 70, cy - 46), (cx + 50, cy - 48)], False), 0.5))
    return grain(art, nxt(), 0.04)

def headphones(W, H):
    cx, cy = W / 2, H / 2 + 14
    art = blank(W, H)
    band = skia.Path(); band.addArc(skia.Rect.MakeLTRB(cx - 62, cy - 96, cx + 62, cy + 30), 180, 180)
    bm = stroke_m(W, H, band, 14)
    art = over(art, shadow(W, H, band, "#000000", (4, 8), 9, 0.0))   # (no fill shadow; band is a stroke)
    art = over(art, paint(bm, DARK, DARK2, rough=1.6))
    pad = stroke_m(W, H, skia.Path().addArc(skia.Rect.MakeLTRB(cx - 50, cy - 86, cx + 50, cy + 20), 200, 140), 7)
    art = over(art, paint(pad, "#6b6366", "#4b4446", rough=1.2, density=0.9))
    for sx in (-1, 1):
        x = cx + sx * 60
        cup = rr(x - 22, cy - 30, 44, 68, 20)
        art = over(art, shadow(W, H, cup, "#000000", (5, 8), 8, 0.3))
        art = over(art, paint(fill_mask(W, H, cup), DARK, DARK2))
        art = shade(art, W, H, rr(x - 22, cy + 4, 44, 34, 16), "#000000", 0.35, 8)
        art = over(art, paint(fill_mask(W, H, rr(x - 14, cy - 22, 28, 52, 12)), "#5a5356", "#3d3739"))     # cushion
        art = over(art, paint(fill_mask(W, H, circ(x, cy + 4, 6)), RED, RED2))
        art = over(art, ink(W, H, cup, 2.6, INK, 0.2))
        art = over(art, highlight(W, H, poly([(x - 14, cy - 22), (x - 14, cy + 20)], False), 0.5))
    art = over(art, ink(W, H, band, 2.2, INK, 0.2))   # band outline (inner/outer merge into one wobbly stroke)
    # cable curl
    pts = [(cx - 60, cy + 40), (cx - 64, cy + 62), (cx - 48, cy + 70), (cx - 40, cy + 58), (cx - 30, cy + 74)]
    art = over(art, ink(W, H, poly(curve(pts, 40), False), 2.6, INK, 0.1))
    return grain(art, nxt(), 0.04)

def keyboard(W, H):
    cx, cy = W / 2, H / 2 + 10
    art = blank(W, H)
    body = rr(cx - 100, cy - 44, 200, 88, 10)
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.3))
    art = over(art, paint(fill_mask(W, H, body), DARK, DARK2))
    keys = rr(cx - 92, cy - 6, 184, 44, 4)
    art = over(art, paint(fill_mask(W, H, keys), CREAM, CREAM2))
    # white key separators
    n = 13
    for i in range(1, n):
        x = cx - 92 + i * 184 / n
        art = over(art, ink(W, H, poly([(x, cy - 6), (x, cy + 38)], False), 1.4, "#8a8386", 0.25, 1.0))
    # black keys (skip after 3rd and 7th of each octave)
    for i in range(n - 1):
        if i % 7 in (2, 6):
            continue
        x = cx - 92 + (i + 1) * 184 / n
        art = over(art, paint(fill_mask(W, H, rr(x - 5, cy - 7, 10, 26, 2)), "#1f1d1f", "#2e2a2d", rough=1.0))
    # controls
    for i in range(5):
        art = over(art, paint(fill_mask(W, H, circ(cx - 70 + i * 18, cy - 26, 5)), "#8f8a8c", "#5f5c58"))
    art = over(art, paint(fill_mask(W, H, rr(cx + 30, cy - 34, 56, 16, 3)), "#4fc3f7", "#1e88e5"))   # little display
    art = over(art, paint(fill_mask(W, H, circ(cx + 92 - 10, cy - 26, 6)), RED, RED2))
    art = over(art, ink(W, H, keys, 2.0, INK, 0.2))
    art = over(art, ink(W, H, body, 2.6, INK, 0.2))
    art = over(art, highlight(W, H, poly([(cx - 90, cy - 38), (cx + 20, cy - 40)], False), 0.45))
    return grain(art, nxt(), 0.04)

def backdrop(W, H):
    """Blush watercolour clouds; transparent so the CSS base colour and drift remain."""
    art = blank(W, H)
    blobs = [(W * 0.28, H * 0.18, 230, 170, "#f6b7c3", "#f3a3b2", 0.5), (W * 0.78, H * 0.52, 250, 210, "#f7cdd5", "#f0b4c0", 0.42),
             (W * 0.2, H * 0.78, 200, 150, "#f4c3cd", "#efb0bd", 0.4), (W * 0.65, H * 0.9, 220, 130, "#f8d5db", "#f2bcc6", 0.35),
             (W * 0.55, H * 0.3, 140, 110, "#fbe3e7", "#f7cdd5", 0.3)]
    for x, y, rx, ry, a, b, d in blobs:
        m = shape_mask(W, H, deform(ellipse_pts(x, y, rx, ry, 10), rng, 3, 0.16))
        art = glaze(art, pigment(m, a, b, seed=nxt(), density=d, edge=0.35, bloom=0.5, gran=0.3, rough=16, feather=4, mottle=0.7))
    return art

def save(arr, name, max_w, tone="#f2f2f7", q=82):
    size = save_asset(arr, f"{OUT}/{name}.webp", max_w=max_w, quality=q)
    preview(arr, f"{PRE}/{name}.png", tone)
    print(name, size, "%.1f KB" % kb(f"{OUT}/{name}.webp"))

save(turntable(220, 170), "gift-turntable", 160)
save(headphones(200, 200), "gift-headphones", 150)
save(keyboard(240, 140), "gift-keyboard", 180)
save(backdrop(560, 900), "backdrop", 400, "#f6dfe3", 68)
