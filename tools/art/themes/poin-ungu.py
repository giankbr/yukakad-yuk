"""Poin Ungu — painted reward medal (gouache disc + gold-foil sparkle), painted violet cover/header backdrops.
Run: python3 -I /tmp/pen/art/themes/poin-ungu.py
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p8_lib import *  # noqa

OUT = outdir("poin-ungu")
rng = random.Random(33)
nxt = Seq(500)

# ---------------- medal: 92px css → render 240 ----------------
W = H = 240
cx = cy = 120
disc = circle_mask(W, H, cx, cy, 92)
disc_w = shape_mask(W, H, deform(ellipse_pts(cx, cy, 92, 92, 24), rng, 2, 0.02))
medal = blank(W, H)
medal = over(medal, shadow(disc, "#1a0b4d", (0, 8), 9, 0.35))
# gouache disc: green bottom-left → gold top-right, brushed
g = gouache_paint(disc_w, "#22b352", "#ffc01e", seed=nxt(), rough=2.5, streak=1.0, density=1.0)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
t = np.clip(((xx - cx) - (yy - cy)) / 260 + 0.5, 0, 1)
t = np.clip(t + (fbm(W, H, nxt(), 40, 4) - 0.5) * 0.9, 0, 1)[..., None]
ca, cb = np.array(hex_rgb("#1fa84c"), np.float32), np.array(hex_rgb("#ffc62a"), np.float32)
g[..., :3] = np.clip((ca * (1 - t) + cb * t) * (g[..., :3] / np.maximum(g[..., :3].mean(-1, keepdims=True), 1e-3)) ** 0.5, 0, 1)
# visible brush streaks + mottle so the disc reads as gouache, not a gradient
st = gaussian_filter(np.random.default_rng(nxt()).random((H, W)).astype(np.float32), (0.8, 9))
st = (st - st.mean()) / (st.std() + 1e-6)
mo = fbm(W, H, nxt(), 24, 3) - 0.5
g[..., :3] = np.clip(g[..., :3] * (1 + st[..., None] * 0.045 + mo[..., None] * 0.16), 0, 1)
medal = over(medal, g)
# a few loose comma strokes of yellow and green over the disc
for (a0, a1, r, col, wdt) in ((2.6, 3.9, 70, "#ffd24a", 16), (-0.9, 0.5, 66, "#8fd94a", 14), (1.3, 2.2, 58, "#f5b921", 12), (3.8, 4.8, 48, "#2fbd5c", 11)):
    sm = stroke_mask(W, H, arc_pts(cx, cy, r, a0, a1, 24), wdt) * disc
    medal = over(medal, gouache_paint(sm, col, seed=nxt(), rough=3, density=0.5, streak=1.0))
# darker rim wash + lighter top-left highlight (painted form)
rim = ring_mask(W, H, cx, cy, 86, 14)
medal = over(medal, gouache_paint(rim, "#157a36", "#c48d00", seed=nxt(), rough=4, density=0.35, streak=0.8))
hl = shape_mask(W, H, deform(ellipse_pts(cx - 30, cy - 36, 40, 22, 12, rot=-0.6), rng, 2, 0.1))
medal = over(medal, gouache_paint(hl, "#ffffff", seed=nxt(), rough=5, density=0.22))
# gold foil ring + inner ring
medal = over(medal, foil(ring_mask(W, H, cx, cy, 90, 7), "#e2b43a", seed=nxt(), emboss=0.9, sparkle=0.3))
medal = over(medal, foil(ring_mask(W, H, cx, cy, 72, 2.2), "#f3d27a", seed=nxt(), emboss=0.4, sparkle=0))
# four-point sparkle star (foil, pressed) + two small satellite stars
def star(p, x, y, r, k=0.26):
    p.moveTo(x, y - r); p.quadTo(x + r * k, y - r * k, x + r, y); p.quadTo(x + r * k, y + r * k, x, y + r)
    p.quadTo(x - r * k, y + r * k, x - r, y); p.quadTo(x - r * k, y - r * k, x, y - r); p.close()
big = path_mask(W, H, lambda p: star(p, cx - 6, cy + 6, 50))
big = displace(big, nxt(), 2.0, 30)
medal = over(medal, shadow(big, "#0e6b2e", (2, 4), 3, 0.35))
medal = over(medal, foil(big, "#fff1b8", seed=nxt(), emboss=1.1, sparkle=0.15))
for (x, y, r) in ((cx + 40, cy - 34, 16), (cx + 30, cy + 40, 10)):
    sm = displace(path_mask(W, H, lambda p: star(p, x, y, r)), nxt(), 1.2, 20)
    medal = over(medal, foil(sm, "#fff6d6", seed=nxt(), emboss=0.8, sparkle=0.4))
# ink-dot accents, hand-placed
def dots(cv):
    for (x, y, r) in ((cx - 52, cy + 48, 3), (cx - 58, cy - 10, 2.4), (cx + 58, cy + 8, 2.6)):
        cv.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
medal = over(medal, gouache_paint(mask_from(W, H, dots), "#fff4c2", seed=nxt(), rough=1, density=0.85))
print("medal", save_asset(medal, f"{OUT}/medal.webp", max_w=200, quality=84), round(kb(f"{OUT}/medal.webp")), "KB")

# ---------------- painted violet cover backdrop (full cover, 390×844 css; render 780×1400) ----------------
BW, BH = 780, 1400
bg = backdrop(BW, BH, [(0, "#3f1eb0"), (0.5, "#33179a"), (1.0, "#2a137c")],
              [(300, 130, 520, "#6a45e0", 0.55), (760, 700, 460, "#5a33d6", 0.35), (60, 1250, 480, "#1f0d6a", 0.5)], seed=12, streak=0.3, grain=0.45)
print("cover-bg", save_opaque(bg, f"{OUT}/cover-bg.webp", 74), round(kb(f"{OUT}/cover-bg.webp")), "KB")

# ---------------- header backdrop (390×110 css; render 780×240) ----------------
hb = backdrop(780, 240, [(0, "#4f2bd1"), (1, "#2e158f")], [(640, 40, 420, "#7050e8", 0.5), (100, 230, 360, "#24107a", 0.5)], seed=14, streak=0.3, grain=0.4)
print("header-bg", save_opaque(hb, f"{OUT}/header-bg.webp", 74), round(kb(f"{OUT}/header-bg.webp")), "KB")

sheet = Image.new("RGB", (780, 700), "#2b1480")
sheet.paste(Image.fromarray((bg[:700, ..., :3] * 255).astype(np.uint8)), (0, 0))
m = to_image(medal).resize((240, 240))
sheet.paste(m, (270, 60), m)
sheet.paste(Image.fromarray((hb[..., :3] * 255).astype(np.uint8)).resize((390, 120)), (20, 540))
sheet.save(f"{PREV}/pu-sheet.png")
print("total KB", round(sum(kb(f"{OUT}/{f}") for f in os.listdir(OUT))))
