"""Kantong Oranye — gouache piggy-bank mascot with ink line, gold-foil coin, painted warm cover backdrop.
Run: python3 -I /tmp/pen/art/themes/kantong-oranye.py
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p8_lib import *  # noqa

OUT = outdir("kantong-oranye")
rng = random.Random(21)
nxt = Seq(300)

# ---------------- piggy bank (display ~44px in a 64px app tile; render at 4x) ----------------
W, H = 240, 200
ORANGE, DEEP, LIGHT, INK = "#f8a91b", "#d98a08", "#ffd36a", "#2a1d08"

def ell(cx, cy, rx, ry, n=12, wob=0.05):
    return deform(ellipse_pts(cx, cy, rx, ry, n), rng, 2, wob)

body = shape_mask(W, H, ell(112, 102, 74, 54))
snout = shape_mask(W, H, ell(186, 112, 24, 19, 10, 0.06))
ear = shape_mask(W, H, petal_pts(82, 64, 34, 12, -2.05, 12))
ear2 = shape_mask(W, H, petal_pts(110, 54, 30, 11, -1.8, 12))
legs = np.zeros((H, W), np.float32)
for lx in (64, 100, 136, 166):
    legs = np.maximum(legs, shape_mask(W, H, deform([(lx, 138), (lx + 26, 138), (lx + 23, 164), (lx + 3, 164)], rng, 3, 0.04), smooth=False))
silhouette = np.maximum.reduce([body, snout, ear, ear2, legs])

pig = blank(W, H)
pig = over(pig, shadow(silhouette, "#5a3a00", (4, 8), 7, 0.22))
pig = over(pig, gouache_paint(legs, DEEP, ORANGE, seed=nxt(), rough=2.5, streak=0.6))
pig = over(pig, gouache_paint(body, ORANGE, "#f3a01a", seed=nxt(), rough=3, streak=0.8))
pig = over(pig, gouache_paint(snout, "#f6b43a", ORANGE, seed=nxt(), rough=2.5))
EARS = np.maximum(ear, ear2)
# form: a lighter brushed patch top-left, darker belly
hi = shape_mask(W, H, ell(86, 76, 34, 20, 10, 0.1))
pig = over(pig, gouache_paint(hi, LIGHT, "#ffe08a", seed=nxt(), rough=4, density=0.55, streak=0.9))
belly = shape_mask(W, H, ell(120, 138, 60, 18, 10, 0.1)) * body
pig = over(pig, gouache_paint(belly, DEEP, "#c97d05", seed=nxt(), rough=4, density=0.45))
# coin slot (dark), eye, nostrils, cheek
slot = shape_mask(W, H, deform([(122, 44), (160, 40), (161, 47), (123, 51)], rng, 2, 0.05), smooth=False)
pig = over(pig, ink(slot, INK, seed=nxt(), wear=0.1))
eye = circle_mask(W, H, 150, 86, 5.5)
pig = over(pig, ink(eye, INK, seed=nxt(), wear=0.05))
pig = over(pig, gouache_paint(circle_mask(W, H, 152, 84, 1.8), "#ffffff", seed=nxt(), rough=0.5))
for nx in (179, 192):
    pig = over(pig, ink(circle_mask(W, H, nx, 112, 3.2), INK, seed=nxt(), wear=0.05))
cheek = shape_mask(W, H, ell(146, 108, 10, 6, 8, 0.1))
pig = over(pig, gouache_paint(cheek, "#f27a4a", seed=nxt(), rough=2, density=0.35))
# ink line: body + snout outline, tail curl, leg bottoms
outline = np.zeros((H, W), np.float32)
for pts, wdt in ((ell(112, 102, 75, 55, 28, 0.015), 3.4), (ell(186, 112, 24, 19, 18, 0.02), 2.8)):
    outline = np.maximum(outline, ink_mask(W, H, pts + pts[:1], wdt, rng, 0.45, (0.02, 0.02)))
tail = curve([(38, 94), (26, 84), (18, 96), (28, 108), (40, 102)], 40)
outline = np.maximum(outline, ink_mask(W, H, tail, 3.6, rng, 0.5))
for lx in (64, 100, 136, 166):
    outline = np.maximum(outline, ink_mask(W, H, [(lx + 2, 164), (lx + 24, 164)], 2.8, rng, 0.4))
pig = over(pig, ink(outline, INK, seed=nxt(), wear=0.22))
pig = over(pig, gouache_paint(EARS, DEEP, ORANGE, seed=nxt(), rough=2.5))
eo = np.zeros((H, W), np.float32)
for ep in (petal_pts(82, 64, 34, 12, -2.05, 18), petal_pts(110, 54, 30, 11, -1.8, 18)):
    eo = np.maximum(eo, ink_mask(W, H, ep[2:16], 2.8, rng, 0.4, (0.1, 0.1)))
pig = over(pig, ink(eo, INK, seed=nxt(), wear=0.2))
print("piggy", save_asset(pig, f"{OUT}/piggy.webp", max_w=180, quality=84), round(kb(f"{OUT}/piggy.webp")), "KB")
on_paper(pig, "#fbf8f1").save(f"{PREV}/ko-piggy.png")

# ---------------- gold coin (display 14px, render 64) ----------------
CW = 72
coin = blank(CW, CW)
disc = circle_mask(CW, CW, 36, 36, 30)
coin = over(coin, shadow(disc, "#7a4e00", (2, 3), 3, 0.3))
coin = over(coin, foil(disc, "#f1b42a", seed=nxt(), emboss=0.9, sparkle=0.4))
coin = over(coin, foil(ring_mask(CW, CW, 36, 36, 23, 3), "#c98a05", seed=nxt(), emboss=0.5, sparkle=0))
heart = path_mask(CW, CW, lambda p: (p.moveTo(36, 46), p.cubicTo(20, 34, 26, 20, 36, 28), p.cubicTo(46, 20, 52, 34, 36, 46), p.close()))
coin = over(coin, linocut(heart, "#b87400", seed=nxt(), wear=0.2, rough=1))
print("coin", save_asset(coin, f"{OUT}/coin.webp", max_w=64, quality=84), round(kb(f"{OUT}/coin.webp")), "KB")

# ---------------- painted warm cover backdrop (coverHead ~390x190 css; render 780x420) ----------------
BW, BH = 780, 420
bg = backdrop(BW, BH, [(0, "#f6d57a"), (0.55, "#fbe9b8"), (1.0, "#fbf8f1")],
              [(620, 40, 460, "#f4b322", 0.5), (80, 330, 420, "#ffffff", 0.7), (360, 150, 300, "#fff1c4", 0.45)], seed=7, streak=0.3, grain=0.45)
print("cover-bg", save_opaque(bg, f"{OUT}/cover-bg.webp", 76), round(kb(f"{OUT}/cover-bg.webp")), "KB")

# ---------------- summary card wash (main page, 390x~170 css; render 780x340) ----------------
sw = backdrop(780, 340, [(0, "#fdf0d2"), (1, "#ffffff")], [(700, 60, 360, "#fbe0a0", 0.5), (60, 300, 300, "#ffffff", 0.6)], seed=9, streak=0.25, grain=0.4)
print("summary-bg", save_opaque(sw, f"{OUT}/summary-bg.webp", 74), round(kb(f"{OUT}/summary-bg.webp")), "KB")

# preview sheet
sheet = Image.new("RGB", (780, 420 + 220), "#fbf8f1")
sheet.paste(Image.fromarray((bg[..., :3] * 255).astype(np.uint8)), (0, 0))
sheet.paste(on_paper(pig, "#ffffff").resize((240, 200)), (40, 430))
sheet.paste(on_paper(coin, "#ffffff").resize((144, 144)), (320, 450))
sheet.save(f"{PREV}/ko-sheet.png")
tot = sum(kb(f"{OUT}/{f}") for f in os.listdir(OUT))
print("total KB", round(tot))
