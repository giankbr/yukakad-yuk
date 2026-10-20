"""Melayu Songket — gouache folk paint + pressed gold foil.
Run: python3 -I /tmp/pen/art/themes/melayu-songket.py
Assets → /root/w/frontend/public/themes/art/melayu-songket/
  ring.webp    rotating pucuk-rebung ring (foil)            css 200px → 440px
  core.webp    bunga cengkih flower on painted green disc    css 148px → 330px
  plate.webp   empty painted disc (for initials)             css 148px → 330px
  awan.webp    awan larat scroll divider (gouache gold)      css 132px → 280px
  band.webp    pucuk rebung border tile (gouache)            css 224x36 → 448x72 (repeat-x)
  songket.webp songket weave tile (gouache dots + threads)   css 160px → 320px (repeat)
  rebung.webp  tumpal marker (gouache)                       css 26px → 60px
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g_util import *

OUT = outdir("melayu-songket")
rng = random.Random(11)
nx = Seq(300)
GOLD, GOLD_L, GOLD_D = "#e3ad2a", "#f3cf6a", "#b8861a"
GREEN, GREEN_D, GREEN_M = "#0d4a35", "#083424", "#1d6045"
RED = "#a8322a"

# ---------------- ring ----------------
S = 2.2; W = H = 440; C = W / 2
ring = blank(W, H)
m = ring_mask(W, H, C, C, 96 * S, 2.2)
ring = over(ring, foil(m, GOLD, seed=nx(), emboss=0.4))
tri = np.zeros((H, W), np.float32)
for k in range(24):
    a = math.radians(k * 15 + rng.uniform(-1.2, 1.2))
    r_out, r_in, half = 94 * S + rng.uniform(-2, 2), 75 * S + rng.uniform(-3, 2), math.radians(4.1 + rng.uniform(-.3, .3))
    pts = [(C + math.sin(a - half) * r_out, C - math.cos(a - half) * r_out),
           (C + math.sin(a) * r_in, C - math.cos(a) * r_in),
           (C + math.sin(a + half) * r_out, C - math.cos(a + half) * r_out)]
    tri = np.maximum(tri, poly_mask(W, H, wobble(pts, rng, 1.2)))
ring = over(ring, gouache_paint(tri, GOLD, GOLD_D, seed=nx(), rough=1.6, streak=0.9))
ring = over(ring, foil(tri * 0.3, GOLD_L, seed=nx(), emboss=0.5, sparkle=0.1))
dots = np.zeros((H, W), np.float32)
for k in range(24):
    a = math.radians(k * 15 + 7.5)
    dots = np.maximum(dots, circle_mask(W, H, C + math.sin(a) * 90 * S, C - math.cos(a) * 90 * S, 1.9 * S + rng.uniform(-.4, .4)))
ring = over(ring, gouache_paint(dots, GOLD_L, seed=nx(), rough=1.0))
save(ring, f"{OUT}/ring.webp", max_w=440)
preview(ring, "ml-ring", bg=GREEN)

# ---------------- disc (plate) + flower (core) ----------------
W = H = 340; C = W / 2; S2 = 2.2
def disc():
    d = blank(W, H)
    base = circle_mask(W, H, C, C, 74 * S2)
    d = over(d, gouache_paint(base, GREEN_D, GREEN_M, seed=nx(), rough=1.4, streak=0.35))
    # soft darker shading towards the lower right (light from upper left)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = np.clip(((xx - C * .7) + (yy - C * .7)) / (W * 1.1), 0, 1) * base
    d = over(d, gouache_paint(shade * 0.55, "#04201a", seed=nx(), rough=0.5, density=0.6))
    rim = ring_mask(W, H, C, C, 73.5 * S2, 3.2)
    d = over(d, foil(rim, GOLD, seed=nx(), emboss=0.5, sparkle=0.15))
    dash = np.zeros((H, W), np.float32)
    for k in range(52):
        a = k / 52 * math.tau + rng.uniform(-.02, .02)
        dash = np.maximum(dash, circle_mask(W, H, C + math.cos(a) * 67 * S2, C + math.sin(a) * 67 * S2, rng.uniform(1.3, 1.9)))
    d = over(d, gouache_paint(dash, GOLD, seed=nx(), rough=0.6, density=0.85))
    return d

plate = disc()
save(plate, f"{OUT}/plate.webp", max_w=330)

core = disc()
petals = np.zeros((H, W), np.float32); holes = np.zeros((H, W), np.float32)
for k in range(8):
    rot = k * 45 + rng.uniform(-3, 3)
    sc = S2 * rng.uniform(.97, 1.03)
    petals = np.maximum(petals, svg_mask(W, H, "M100 100 C 88 82 90 60 100 46 C 110 60 112 82 100 100 Z", scale=sc,
                                         tx=C - 100 * sc, ty=C - 100 * sc, rot=rot, cx=100, cy=100, wob=0.8, seed=nx()))
    holes = np.maximum(holes, svg_mask(W, H, "M100 92 C 95 80 96 66 100 58 C 104 66 105 80 100 92 Z", scale=sc,
                                       tx=C - 100 * sc, ty=C - 100 * sc, rot=rot, cx=100, cy=100, wob=0.6, seed=nx()))
core = over(core, gouache_paint(petals, GOLD, GOLD_D, seed=nx(), rough=1.0, streak=0.6))
core = over(core, foil(petals * 0.45, GOLD_L, seed=nx(), emboss=0.9, sparkle=0.12))
core = over(core, gouache_paint(holes, GREEN_D, GREEN_M, seed=nx(), rough=0.8))
# thin gold vein in each petal hole
veins = np.zeros((H, W), np.float32)
for k in range(8):
    a = math.radians(k * 45)
    p0 = (C + math.sin(a) * 18, C - math.cos(a) * 18); p1 = (C + math.sin(a) * 66, C - math.cos(a) * 66)
    veins = np.maximum(veins, stroke_mask(W, H, [p0, ((p0[0] + p1[0]) / 2 + 1, (p0[1] + p1[1]) / 2), p1], 1.6))
core = over(core, gouache_paint(veins, GOLD_D, seed=nx(), rough=0.4, density=0.7))
heart = circle_mask(W, H, C, C, 10 * S2)
core = over(core, gouache_paint(np.clip(heart * 1.0, 0, 1), GREEN_D, seed=nx(), rough=1.0))
core = over(core, foil(circle_mask(W, H, C, C, 8.4 * S2), GOLD_L, seed=nx(), emboss=0.8))
core = over(core, gouache_paint(circle_mask(W, H, C + 0.6, C - 0.4, 3.2 * S2), RED, "#8d2620", seed=nx(), rough=0.8))
save(core, f"{OUT}/core.webp", max_w=330)
cover = over(ring.copy(), np.pad(core, ((50, 50), (50, 50), (0, 0))))
preview(cover, "ml-medal", bg=GREEN)

# ---------------- awan larat divider ----------------
W, H = 560, 110; S3 = 4.0
half = "M6 12 C 18 12 22 3 32 3 C 42 3 45 13 38 16 C 33 18 30 12 34 10 M32 3 C 44 -1 54 6 60 12"
bud_leaf = "M20 11 C 22 16 28 18 30 22 C 24 22 20 18 20 11 Z"
aw = blank(W, H)
strokes = np.zeros((H, W), np.float32); fills = np.zeros((H, W), np.float32)
for sx in (1, -1):
    tx = W / 2
    strokes = np.maximum(strokes, svg_mask(W, H, half, scale=S3, sx=sx, tx=tx, ty=8, stroke=5.2, wob=0.9, seed=nx()))
    fills = np.maximum(fills, svg_mask(W, H, bud_leaf, scale=S3, sx=sx, tx=tx, ty=8, wob=0.8, seed=nx()))
fills = np.maximum(fills, svg_mask(W, H, "M66 4 L71 12 L66 20 L61 12 Z", scale=S3, tx=W / 2 - 66 * S3, ty=8, wob=0.6, seed=nx()))
aw = over(aw, gouache_paint(np.maximum(strokes, fills), GOLD, GOLD_D, seed=nx(), rough=1.4, streak=1.0, dry=0.12))
aw = over(aw, gouache_paint(circle_mask(W, H, W / 2, 8 + 12 * S3, 6), RED, seed=nx(), rough=0.6))
save(aw, f"{OUT}/awan.webp", max_w=280)
preview(aw, "ml-awan", tone="#fbf6e4")

# ---------------- pucuk rebung band tile (8 triangles, seamless: gaps at tile edges) ----------------
TW, TH, n = 448, 72, 8
cw = TW / n
band = blank(TW, TH)
outer = np.zeros((TH, TW), np.float32); inner = np.zeros((TH, TW), np.float32); tip = np.zeros((TH, TW), np.float32); dot = np.zeros((TH, TW), np.float32)
for k in range(n):
    x0 = k * cw
    j = lambda a=1.0: rng.uniform(-a, a)
    outer = np.maximum(outer, poly_mask(TW, TH, [(x0 + cw / 2 + j(), 3 + j()), (x0 + cw - 2.5 + j(.6), TH), (x0 + 2.5 + j(.6), TH)]))
    inner = np.maximum(inner, poly_mask(TW, TH, [(x0 + cw / 2 + j(), 26 + j()), (x0 + cw * .8 + j(.6), TH), (x0 + cw * .2 + j(.6), TH)]))
    tip = np.maximum(tip, poly_mask(TW, TH, [(x0 + cw / 2 + j(.6), 44 + j()), (x0 + cw * .66, TH), (x0 + cw * .34, TH)]))
    dot = np.maximum(dot, circle_mask(TW, TH, x0 + cw / 2 + j(.5), 16 + j(.5), 3.0))
band = over(band, gouache_paint(outer, GOLD, GOLD_D, seed=nx(), rough=1.2, streak=1.2))
band = over(band, gouache_paint(inner, GREEN, GREEN_D, seed=nx(), rough=1.0))
band = over(band, gouache_paint(tip, GOLD_L, GOLD, seed=nx(), rough=0.8))
band = over(band, gouache_paint(dot, RED, seed=nx(), rough=0.5))
save_full(band, f"{OUT}/band.webp")
preview(np.concatenate([band, band], 1), "ml-band", bg=GREEN)

# ---------------- songket weave tile ----------------
TS = 320; cell = TS / 4
yy, xx = np.mgrid[0:TS, 0:TS].astype(np.float32)
thread = wrap_noise(TS, TS, nx(), (0.4, 30))          # horizontal weft threads
weft = 0.5 + 0.5 * np.sin(yy / TS * math.tau * 80)     # periodic thread rows
motif = np.zeros((TS, TS), np.float32); dotm = np.zeros((TS, TS), np.float32); redm = np.zeros((TS, TS), np.float32)
for i in range(4):
    for k in range(4):
        cx, cy = k * cell + cell / 2, i * cell + cell / 2
        s_ = cell * 0.1
        sq = [(cx - s_, cy - s_), (cx + s_, cy - s_), (cx + s_, cy + s_), (cx - s_, cy + s_)]
        motif = np.maximum(motif, poly_mask(TS, TS, wobble(sq, rng, .5)))
        motif = np.maximum(motif, poly_mask(TS, TS, wobble(rot_pts(sq, cx, cy, math.pi / 4), rng, .5)))
        for dx, dy in [(0, -.36), (0, .36), (-.36, 0), (.36, 0)]:
            dotm = np.maximum(dotm, circle_mask(TS, TS, cx + dx * cell, cy + dy * cell, 2.0))
        redm = np.maximum(redm, circle_mask(TS, TS, cx, cy, 3.2))
tile = np.zeros((TS, TS, 4), np.float32)
gold = np.array(hex_rgb(GOLD), np.float32)
tile[..., :3] = gold
tile[..., 3] = np.clip((weft * 0.18 + thread * 0.12) * 0.35, 0, 1)   # faint thread sheen
tile = over(tile, gouache_paint(np.maximum(motif, dotm), GOLD, GOLD_L, seed=nx(), rough=0.6, density=0.95))
tile = over(tile, gouache_paint(redm, RED, seed=nx(), rough=0.4))
save_full(tile, f"{OUT}/songket.webp", quality=78)
preview(np.tile(tile, (2, 2, 1)), "ml-songket", bg=GREEN)

# ---------------- rebung marker ----------------
W, H = 72, 90
mk = blank(W, H)
mk = over(mk, gouache_paint(poly_mask(W, H, [(36, 3), (69, 87), (3, 87)]), GOLD, GOLD_D, seed=nx(), rough=1.0))
mk = over(mk, gouache_paint(poly_mask(W, H, [(36, 30), (54, 82), (18, 82)]), GREEN, seed=nx(), rough=0.8))
mk = over(mk, gouache_paint(poly_mask(W, H, [(36, 54), (45, 80), (27, 80)]), GOLD_L, seed=nx(), rough=0.6))
save(mk, f"{OUT}/rebung.webp", max_w=60)
