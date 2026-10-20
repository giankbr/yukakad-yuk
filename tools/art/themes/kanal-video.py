"""Kanal Video — painted Super Thanks wishlist products (gouache + ink) and the "Final — LIVE" episode thumbnail.
Run: python3 -I /tmp/pen/art/themes/kanal-video.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p5_lib import *  # noqa

OUT = "/root/w/frontend/public/themes/art/kanal-video"
PRE = "/tmp/pen/nt3-P5/kanal-video"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(33)
INK, WHITE, WHITE2, GREY, GREY2, RED, RED2, PINK = "#2a2426", "#fbfaf7", "#e9e6e0", "#8d8a86", "#5f5c58", "#ff2f4f", "#c8102e", "#ffb3bf"

def purifier(W, H):
    cx, base = W / 2, H - 14
    art = blank(W, H)
    body = rr(cx - 44, base - 150, 88, 150, 26)
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.3))
    art = over(art, paint(fill_mask(W, H, body), WHITE, WHITE2))
    art = shade(art, W, H, rr(cx + 6, base - 150, 40, 150, 20), "#9a9590", 0.22, 10)
    # grille slats
    for i in range(7):
        y = base - 118 + i * 13
        art = over(art, ink(W, H, poly([(cx - 26, y), (cx + 26, y)], False), 2.4, GREY2, 0.25))
    # top vent + glowing status light
    vent = rr(cx - 26, base - 144, 52, 10, 5)
    art = over(art, paint(fill_mask(W, H, vent), GREY2, GREY))
    art = over(art, glow(fill_mask(W, H, circ(cx, base - 28, 5)), "#4fc3f7", 6, 0.8))
    art = over(art, paint(fill_mask(W, H, circ(cx, base - 28, 4)), "#4fc3f7", "#1e88e5"))
    art = over(art, ink(W, H, body, 2.6, INK, 0.2))
    # clean-air swirls
    for k, (x, y) in enumerate([(cx + 56, base - 120), (cx - 62, base - 96)]):
        pts = arc_pts(x, y, 14 + k * 3, math.pi * 1.1, math.pi * 2.6, 20)
        art = over(art, ink(W, H, poly(pts, False), 2.2, "#6ab7e6", 0.15))
    art = over(art, highlight(W, H, poly([(cx - 30, base - 130), (cx - 30, base - 60)], False), 0.6))
    return grain(art, nxt(), 0.04)

def speaker(W, H):
    cx, base = W / 2, H - 16
    art = blank(W, H)
    body = rr(cx - 70, base - 76, 140, 76, 30)
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.3))
    art = over(art, paint(fill_mask(W, H, body), "#3a3638", "#232022"))
    art = shade(art, W, H, rr(cx - 70, base - 36, 140, 36, 20), "#000000", 0.35, 10)
    # fabric mesh dots
    def mesh(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for i in range(-5, 6):
            for j in range(-2, 3):
                cv.c.drawCircle(cx + i * 12 + (j % 2) * 6, base - 40 + j * 11, 1.6, p)
    art = over(art, paint(mask_from(W, H, mesh), "#6d6769", "#55504f", rough=0.8, density=0.9))
    # strap + small buttons
    strap = poly([(cx + 50, base - 70), (cx + 70, base - 96), (cx + 78, base - 88), (cx + 62, base - 66)])
    art = over(art, paint(fill_mask(W, H, strap), "#c9a26a", "#a67d44"))
    art = over(art, ink(W, H, strap, 1.8, INK, 0.2))
    for i in range(3):
        art = over(art, paint(fill_mask(W, H, circ(cx - 24 + i * 24, base - 72, 4)), "#8f8a8c", "#6d6769"))
    art = over(art, ink(W, H, body, 2.6, INK, 0.2))
    # sound waves
    for k in range(2):
        pts = arc_pts(cx - 92, base - 40, 14 + k * 10, math.pi * 0.72, math.pi * 1.28, 16)
        art = over(art, ink(W, H, poly(pts, False), 2.4, RED, 0.12))
    art = over(art, highlight(W, H, poly([(cx - 52, base - 66), (cx + 20, base - 68)], False), 0.45))
    return grain(art, nxt(), 0.04)

def camera(W, H):
    cx, base = W / 2, H - 18
    art = blank(W, H)
    body = rr(cx - 72, base - 92, 144, 92, 18)
    art = over(art, shadow(W, H, body, "#000000", (5, 8), 9, 0.3))
    art = over(art, paint(fill_mask(W, H, body), "#3b3537", "#232022"))
    grip = rr(cx - 72, base - 92, 44, 92, 18)
    art = over(art, paint(fill_mask(W, H, grip), "#5a4a40", "#3e3029"))
    art = over(art, paint(fill_mask(W, H, rr(cx - 40, base - 104, 48, 18, 6)), "#3b3537", "#232022"))   # prism hump
    art = over(art, paint(fill_mask(W, H, rr(cx + 30, base - 100, 22, 10, 4)), "#8f8a8c", "#5f5c58"))    # shutter
    # lens
    art = over(art, paint(fill_mask(W, H, circ(cx + 6, base - 46, 34)), "#8f8a8c", "#5f5c58"))
    art = over(art, paint(fill_mask(W, H, circ(cx + 6, base - 46, 27)), "#1b1a1c", "#2b2d33"))
    art = over(art, pigment(fill_mask(W, H, circ(cx + 6, base - 46, 20)), "#3f6fb0", "#1f2e5a", seed=nxt(), density=0.9, edge=0.5, bloom=0.3, rough=2))
    art = over(art, paint(fill_mask(W, H, oval(cx - 2, base - 56, 7, 4)), "#dfe9f7"))
    art = over(art, paint(fill_mask(W, H, circ(cx + 52, base - 76, 4)), RED, RED2))   # rec light
    art = over(art, ink(W, H, body, 2.6, INK, 0.2))
    art = over(art, ink(W, H, circ(cx + 6, base - 46, 34), 2.2, INK, 0.15))
    art = over(art, ink(W, H, circ(cx + 6, base - 46, 27), 1.6, INK, 0.3))
    art = over(art, highlight(W, H, poly([(cx - 20, base - 84), (cx + 56, base - 84)], False), 0.45))
    return grain(art, nxt(), 0.04)

def final_thumb(W, H):
    """Soft pink painted scene: two gold rings and gouache confetti — the 'Final: Menuju Selamanya' thumbnail."""
    art = painted_sky(W, H, [(0, "#ffe9ec"), (0.55, "#fff3f1"), (1, "#ffe3e6")], seed=nxt(), streak=0.8, grain=0.7)
    cx, cy = W * 0.5, H * 0.56
    glow_m = fill_mask(W, H, circ(cx, cy, 60))
    art = over(art, glow(glow_m, "#ffffff", 30, 0.5))
    for k, (x, y, rot) in enumerate([(cx - 22, cy, -0.3), (cx + 22, cy + 4, 0.25)]):
        ring = skia.Path(); ring.addCircle(x, y, 34)
        m = stroke_m(W, H, ring, 9)
        art = over(art, shadow(W, H, circ(x, y + 6, 36), "#c8102e", (0, 0), 7, 0.18))
        art = over(art, foil(m, "#e2b857", seed=nxt(), emboss=0.6, sparkle=0.2))
        art = over(art, ink(W, H, ring, 1.3, "#7a5a1e", 0.4))
    art = over(art, paint(fill_mask(W, H, oval(cx - 22, cy - 34, 6, 7)), "#fff3c8", "#f0d58a"))   # small stone
    def confetti(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for _ in range(26):
            x, y = rng.uniform(10, W - 10), rng.uniform(8, H - 8)
            if abs(x - cx) < 70 and abs(y - cy) < 46:
                continue
            cv.c.save(); cv.c.translate(x, y); cv.c.rotate(rng.uniform(0, 180))
            cv.c.drawRect(skia.Rect.MakeXYWH(-5, -2.5, 10, 5), p); cv.c.restore()
    cm = mask_from(W, H, confetti)
    art = over(art, paint(cm, RED, PINK, rough=1.2, density=0.85))
    def confetti2(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for _ in range(16):
            x, y = rng.uniform(10, W - 10), rng.uniform(8, H - 8)
            if abs(x - cx) < 70 and abs(y - cy) < 46:
                continue
            cv.c.drawCircle(x, y, rng.uniform(2, 4), p)
    art = over(art, paint(mask_from(W, H, confetti2), "#e2b857", "#f3d98a", rough=1.0, density=0.85))
    return grain(art, nxt(), 0.03)

def save(arr, name, max_w, tone="#f2f2f2"):
    size = save_asset(arr, f"{OUT}/{name}.webp", max_w=max_w, quality=82)
    preview(arr, f"{PRE}/{name}.png", tone)
    print(name, size, "%.1f KB" % kb(f"{OUT}/{name}.webp"))

save(purifier(220, 190), "gift-purifier", 170)
save(speaker(240, 160), "gift-speaker", 190)
save(camera(240, 160), "gift-camera", 190)
save(final_thumb(360, 204), "final-thumb", 300)
