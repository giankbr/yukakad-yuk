"""Ultah Gemerlap — painted night-party scene: indigo washes with watercolour bokeh, foil fireworks, foil confetti,
gouache two-tier cake with separate flames, foil photo ring.
Run: python3 -I /tmp/pen/art/themes/ultah-gemerlap.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentc import *  # noqa

OUT = "/root/w/frontend/public/themes/art/ultah-gemerlap"
PRE = "/tmp/pen/nt2-C/ug"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(55)
seed = [1300]
def nxt():
    seed[0] += 23
    return seed[0]

GOLD, GOLD_L, BLUSH = "#d9b45a", "#f3dc9b", "#e8b4a0"
INDIGO, NIGHT = "#2a2350", "#07060f"

# ---------- cover / section night backdrop (opaque) ----------
W, H = 780, 1688
bg = painted_sky(W, H, [(0, "#2a2350"), (.3, "#1a1638"), (.62, "#100d24"), (1, NIGHT)], seed=nxt(), streak=.35)
# soft top light pool (painted, wet-edged) where the spotlight falls
pool = shape_mask(W, H, deform(ellipse_pts(W / 2, 120, 420, 380, 12), rng, 3, .1))
bg = over(bg, scale_alpha(pigment(pool, "#3a3168", "#463a72", seed=nxt(), density=.5, edge=.25, bloom=.6, rough=30, feather=10, mottle=.8), .7))
# plum/indigo cloud washes
for i in range(7):
    cx, cy = rng.uniform(0, W), rng.uniform(300, 1500)
    m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rng.uniform(160, 300), rng.uniform(70, 140), 10, rng.uniform(-.3, .3)), rng, 3, .14))
    bg = glaze(bg, pigment(m, rng.choice(["#3b2c5e", "#2e2654", "#45305f"]), "#2a2350", seed=nxt(), density=.22, edge=.4, bloom=.5, rough=18, feather=5, gran=.2))
# watercolour bokeh: overlapping wet discs, kept to the margins so the centre column stays calm
bok = blank(W, H)
spots = []
for _ in range(22):
    side = rng.choice([-1, 1])
    x = W / 2 + side * rng.uniform(190, 430)
    y = rng.choice([rng.uniform(0, 420), rng.uniform(0, 420), rng.uniform(420, 1300)])
    spots.append((x, y, rng.uniform(10, 42)))
for x, y, r in spots:
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r, 14), rng, 1, .03))
    col = rng.choice([("#e8c167", "#d9a74a"), ("#f0a98c", "#e48f78"), ("#f3d48a", "#e8b95c")])
    bok = over(bok, scale_alpha(glow(m, col[0], radius=r * .5, strength=.18), .8))
    bok = over(bok, scale_alpha(pigment(m, *col, seed=nxt(), density=.55, edge=1.0, bloom=.5, rough=2.5, feather=1.4, gran=.15), rng.uniform(.3, .55)))
bg = over(bg, bok)
bg[..., 3] = 1
print("night", save_opaque(bg, f"{OUT}/night.webp", quality=74), round(kb(f"{OUT}/night.webp")))
on_bg(bg, bg).save(f"{PRE}/night.png")


# ---------- foil firework bursts ----------
def burst(name, base, tip, S=220, rays=14):
    cx = cy = S / 2
    strokes, dots = [], []
    for i in range(rays):
        a = i / rays * math.tau + rng.uniform(-.08, .08)
        r1 = S * rng.uniform(.1, .16); r2 = S * rng.uniform(.33, .47)
        sag = rng.uniform(2, 7)  # gravity: rays droop a touch
        p = [(cx + math.cos(a) * (r1 + (r2 - r1) * t), cy + math.sin(a) * (r1 + (r2 - r1) * t) + sag * t * t) for t in [k / 6 for k in range(7)]]
        strokes.append((p, rng.uniform(3, 5.5) if i % 2 == 0 else rng.uniform(2, 3.2)))
        ex, ey = p[-1]
        dots.append((ex + math.cos(a) * 7, ey + math.sin(a) * 7 + 2, rng.uniform(2, 3.6)))
        if rng.random() < .6:
            dots.append((ex + math.cos(a) * 15, ey + math.sin(a) * 15 + 5, rng.uniform(1.2, 2.2)))
    m = strokes_mask(S, S, strokes)
    lay = foil(m, base, seed=nxt(), emboss=.5, sparkle=.2)
    lay = over(glow(np.maximum(m, dots_mask(S, S, dots)), tip, radius=6, strength=.25), lay)
    lay = over(lay, pigment(dots_mask(S, S, dots), tip, seed=nxt(), density=.95, edge=.2, bloom=0, rough=.8, feather=.5))
    lay = over(lay, foil(circle_mask(S, S, cx, cy, 5), base, seed=nxt(), emboss=.6, sparkle=0))
    print(name, save_asset(lay, f"{OUT}/{name}.webp", quality=84), round(kb(f"{OUT}/{name}.webp")))
    return lay

bg_gold = burst("burst-gold", "#c9a14a", GOLD_L)
bg_blush = burst("burst-blush", "#d39a86", "#f6d2c4", S=180, rays=12)
on_color(over(bg_gold, blank(*bg_gold.shape[1::-1])), INDIGO).save(f"{PRE}/burst.png")


# ---------- foil confetti flakes (falling glitter) ----------
def flake(name, kind):
    S = 40
    if kind == "strip":
        m = shape_mask(S, S, deform([(8, 14), (32, 10), (33, 18), (9, 23)], rng, 1, .03), smooth=False)
        lay = foil(m, "#c9a14a", seed=nxt(), emboss=.7, sparkle=.3)
    elif kind == "sequin":
        m = circle_mask(S, S, 20, 20, 12)
        lay = foil(m, "#d4ad5c", seed=nxt(), emboss=.9, sparkle=.3)
        lay[..., 3] *= 1 - circle_mask(S, S, 20, 20, 3)
    else:
        m = shape_mask(S, S, deform(ellipse_pts(20, 20, 13, 9, 9, .6), rng, 1, .08))
        lay = gouache_paint(m, BLUSH, "#f1c9b8", seed=nxt(), rough=1.2, streak=.6)
    save_asset(lay, f"{OUT}/{name}.webp", quality=84)
    print(name, round(kb(f"{OUT}/{name}.webp"), 1))

flake("flake-strip", "strip"); flake("flake-sequin", "sequin"); flake("flake-blush", "blush")


# ---------- gouache cake (body) + flames + smoke ----------
K = 2.5
CW, CH = int(160 * K), int(150 * K)
def V(x, y):
    return (x * K, y * K)
def rect_pts(x, y, w, h, r=7):
    pts = []
    for (cx, cy, a0) in [(x + w - r, y + r, -math.pi / 2), (x + w - r, y + h - r, 0), (x + r, y + h - r, math.pi / 2), (x + r, y + r, math.pi)]:
        for j in range(5):
            a = a0 + j / 4 * math.pi / 2
            pts.append(V(cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts
cake = blank(CW, CH)
shadow = shape_mask(CW, CH, ellipse_pts(*V(80, 140), 72 * K, 7 * K, 16))
cake = over(cake, pigment(shadow, "#05040a", seed=nxt(), density=.5, edge=0, bloom=0, rough=3, feather=4))
lower = shape_mask(CW, CH, rect_pts(22, 92, 116, 46))
upper = shape_mask(CW, CH, rect_pts(38, 60, 84, 34))
cake = over(cake, gouache_paint(lower, "#2b2452", "#352c63", seed=nxt(), rough=1.6, streak=.45))
cake = over(cake, gouache_paint(upper, "#3b3170", "#463a7c", seed=nxt(), rough=1.6, streak=.45))
# side shading (light from upper-left)
for m_, x0, x1 in [(lower, 22, 138), (upper, 38, 122)]:
    xx = np.linspace(0, 1, CW, dtype=np.float32)[None, :] * np.ones((CH, 1), np.float32)
    k = np.clip((xx * CW / K - (x0 + (x1 - x0) * .62)) / ((x1 - x0) * .38), 0, 1)
    cake = over(cake, np.concatenate([np.zeros((CH, CW, 3), np.float32) + np.array(hex_rgb("#120e28"), np.float32), (m_ * k * .4)[..., None]], -1))
# gold drips under each top edge
def drips(x0, x1, y, depth):
    pts = [V(x0 + 1, y - 1)]
    x = x0 + 1
    while x < x1 - 1:
        w = rng.uniform(8, 15); d = rng.uniform(.25, 1) * depth
        pts += [V(x + w * .15, y + 2.5), V(x + w * .3, y + d * .85), V(x + w * .42, y + d), V(x + w * .58, y + d), V(x + w * .7, y + d * .85), V(x + w * .85, y + 2.5)]
        x += w + rng.choice([0, 0, rng.uniform(3, 9)])
    pts += [V(x1 - 1, y - 1)]
    return pts
for (x0, x1, y, d) in [(22, 138, 93, 13), (38, 122, 61, 10)]:
    dm = shape_mask(CW, CH, drips(x0, x1, y, d), smooth=False)
    cake = over(cake, foil(dm, "#c9a14a", seed=nxt(), emboss=.8, sparkle=.15))
# piped pearls along the bases
pearls = [(V(x, 137)[0], V(x, 137)[1], 2.2 * K) for x in np.arange(26, 136, 6.2)] + [(V(x, 93)[0], V(x, 93)[1], 1.8 * K) for x in np.arange(42, 120, 6)]
cake = over(cake, foil(dots_mask(CW, CH, pearls), "#e2c27a", seed=nxt(), emboss=1.0, sparkle=.1))
# blush sugar dots
cake = over(cake, gouache_paint(dots_mask(CW, CH, [(*V(46, 122), 2.6 * K), (*V(80, 118), 2.6 * K), (*V(114, 122), 2.6 * K), (*V(62, 80), 2.2 * K), (*V(98, 80), 2.2 * K)]), BLUSH, "#f3cdbd", seed=nxt(), rough=.8))
# candles (striped), wick
for i, x in enumerate([58, 80, 102]):
    cm = shape_mask(CW, CH, rect_pts(x - 3.2, 37, 6.4, 24, 2), smooth=True)
    cake = over(cake, gouache_paint(cm, GOLD_L if i == 1 else BLUSH, "#fff0d6", seed=nxt(), rough=.8, streak=.6))
    stripes = lines_mask(CW, CH, [[V(x - 3.2, 42 + j * 6), V(x + 3.2, 39 + j * 6)] for j in range(4)], 1.6 * K)
    cake = over(cake, scale_alpha(gouache_paint(stripes * cm, "#b98a3a" if i == 1 else "#c97f6c", seed=nxt(), rough=.5), .55))
    cake = over(cake, pigment(lines_mask(CW, CH, [[V(x, 37), V(x + .4, 33.5)]], 1.1 * K), "#1a1424", seed=nxt(), density=.9, edge=0, bloom=0, rough=.3, feather=.4))
print("cake", save_full(cake, f"{OUT}/cake.webp", quality=84), round(kb(f"{OUT}/cake.webp")))

FW, FH = 48, 72  # flame canvas (css 16x24 at 3x)
fl_m = shape_mask(FW, FH, [(24, 6), (33, 30), (34, 48), (24, 62), (14, 48), (15, 30)])
flame = glow(fl_m, "#ffcf6b", radius=7, strength=.35)
flame = over(flame, pigment(fl_m, "#ffb347", "#ffcf6b", seed=nxt(), density=1, edge=.4, bloom=.2, rough=1.4, feather=.8))
core = shape_mask(FW, FH, [(24, 30), (29, 46), (24, 58), (19, 46)])
flame = over(flame, pigment(core, "#fff6dc", "#ffe7a6", seed=nxt(), density=1, edge=.2, bloom=0, rough=.8, feather=.8))
print("flame", save_full(flame, f"{OUT}/flame.webp", quality=86), round(kb(f"{OUT}/flame.webp"), 1))
SMW, SMH = 36, 72
smoke_m = strokes_mask(SMW, SMH, [(curve([(18, 70), (10, 56), (22, 42), (12, 26), (20, 8)], 30), 4)])
smoke = pigment(smoke_m, "#e8dcc0", "#cfc4b2", seed=nxt(), density=.55, edge=.4, bloom=.3, rough=2, feather=1.6)
print("smoke", save_full(smoke, f"{OUT}/smoke.webp", quality=84), round(kb(f"{OUT}/smoke.webp"), 1))
prev = on_color(cake, INDIGO)
prev.save(f"{PRE}/cake.png")

# ---------- foil photo ring (replaces the conic gradient frame) ----------
R = 504
ring_m = np.clip(circle_mask(R, R, R / 2, R / 2, R / 2 - 4) - circle_mask(R, R, R / 2, R / 2, R / 2 - 16), 0, 1)
ring = foil(ring_m, "#c9a14a", seed=nxt(), emboss=1.0, sparkle=.25)
# hand-set rhinestones around the band
stones = [(R / 2 + math.cos(a) * (R / 2 - 10), R / 2 + math.sin(a) * (R / 2 - 10), 4.2) for a in [k / 36 * math.tau + rng.uniform(-.02, .02) for k in range(36)]]
ring = over(ring, foil(dots_mask(R, R, stones), "#efd9a2", seed=nxt(), emboss=1.2, sparkle=.4))
print("ring", save_full(ring, f"{OUT}/ring.webp", quality=84), round(kb(f"{OUT}/ring.webp")))
on_color(ring, INDIGO).save(f"{PRE}/ring.png")
