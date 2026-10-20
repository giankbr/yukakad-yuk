"""Streaming — painted profile avatars (gouache faces with ink) for the "Siapa yang menonton?" picker,
the nav profile chip and the review avatars. Transparent; the coloured tile stays CSS.
Run: python3 -I /tmp/pen/art/themes/streaming.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p5_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/streaming"
PRE = "/tmp/pen/nt3-P5/streaming"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
W = H = 280
rng = random.Random(21)
CREAM, CREAM2, INK, CHEEK = "#fff7ee", "#f4e3cf", "#2a2224", "#f08a7c"

def face(kind):
    cx, cy, r = 140, 142, 92
    art = blank(W, H)
    head = smooth_path(deform(ellipse_pts(cx, cy, r, r * 0.96, 10), rng, 2, 0.05))
    art = over(art, shadow(W, H, head, "#000000", (0, 6), 10, 0.28))
    art = over(art, paint(fill_mask(W, H, head), CREAM, CREAM2, rough=3.0, streak=0.9))
    art = shade(art, W, H, oval(cx + 10, cy + 40, r, r * 0.7), "#c9a98a", 0.22, 14)
    # cheeks — soft watercolour blush
    for x in (cx - 48, cx + 48):
        art = over(art, pigment(fill_mask(W, H, oval(x, cy + 22, 17, 11)), CHEEK, "#e86f6a", seed=nxt(), density=0.42, edge=0.2, bloom=0.4, rough=4, feather=2.5))
    # eyes
    if kind == "wink":
        art = over(art, paint(fill_mask(W, H, oval(cx - 30, cy - 12, 8, 10)), INK))
        art = over(art, ink(W, H, poly([(cx + 18, cy - 10), (cx + 30, cy - 16), (cx + 42, cy - 10)], False), 4.5, INK, 0.1))
    elif kind == "happy":   # closed smiling eyes
        for x in (cx - 30, cx + 30):
            art = over(art, ink(W, H, poly([(x - 12, cy - 6), (x, cy - 18), (x + 12, cy - 6)], False), 4.5, INK, 0.1))
    else:
        for x in (cx - 30, cx + 30):
            art = over(art, paint(fill_mask(W, H, oval(x, cy - 12, 8, 10)), INK))
            art = over(art, paint(fill_mask(W, H, circ(x + 3, cy - 16, 2.5)), "#ffffff"))
    # mouth
    if kind == "grin":
        m = poly([(cx - 34, cy + 22), (cx + 34, cy + 22), (cx + 20, cy + 50), (cx - 20, cy + 50)])
        art = over(art, paint(fill_mask(W, H, m), "#3b2426", "#5a2d33"))
        art = over(art, paint(fill_mask(W, H, rr(cx - 28, cy + 23, 56, 9, 3)), "#ffffff"))
        art = over(art, ink(W, H, m, 3.2, INK, 0.1))
    else:
        pts = [(cx + math.cos(a) * 36, cy + 8 + math.sin(a) * 30) for a in [0.35 + (math.pi - 0.7) * i / 14 for i in range(15)]]
        art = over(art, ink(W, H, poly(pts, False), 5.0, INK, 0.08))
    # a few hair strokes on top so it isn't a plain ball
    for i, (x, a) in enumerate([(cx - 26, -1.9), (cx, -1.65), (cx + 26, -1.4)]):
        p = poly([(x, cy - r + 6), (x + math.cos(a) * 26, cy - r + 6 + math.sin(a) * 26)], False)
        art = over(art, ink(W, H, p, 4.0, INK, 0.1))
    art = over(art, ink(W, H, head, 3.0, INK, 0.22))
    art = over(art, highlight(W, H, poly([(cx - 50, cy - 60), (cx - 20, cy - 78)], False), 0.5))
    return grain(art, nxt(), 0.04)

for name, kind in [("guest", "smile"), ("keluarga", "happy"), ("sahabat", "grin"), ("rekan", "wink")]:
    art = face(kind)
    size = save_asset(art, f"{OUT}/avatar-{name}.webp", max_w=220 if name == "guest" else 110, quality=82)
    preview(art, f"{PRE}/avatar-{name}.png", "#9a1a1a" if name == "guest" else "#2b5fa8")
    print(name, size, "%.1f KB" % kb(f"{OUT}/avatar-{name}.webp"))
