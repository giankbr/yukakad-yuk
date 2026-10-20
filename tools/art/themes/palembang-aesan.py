"""Palembang Aesan — pressed gold foil (karsuhun-inspired fan crown, kembang goyang pins, lotus corners, limar
jewels) with small gouache ruby accents.
Run: python3 -I /tmp/pen/art/themes/palembang-aesan.py
Assets → /root/w/frontend/public/themes/art/palembang-aesan/
  crown.webp     fan crown without the pins (576x384 canvas = viewBox 240x160 x2.4, untrimmed)   css 120–230px
  goyang.webp    one kembang goyang pin at 0deg, cropped to viewBox x108-132 / y6-56 (rotated ×5 in CSS)
  corner.webp    lotus-bud corner                                  css 46px → 120px
  limar-gold.webp / limar-red.webp   songket-limar diamond jewel     css 16–34px → 72px
  limar.webp     limar dot field tile (4x4 motifs)                  css 144px → 288px
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g_util import *

OUT = outdir("palembang-aesan")
rng = random.Random(41)
nx = Seq(1300)
GOLD, GOLD_L, GOLD_D, RUBY, PEARL = "#d3a247", "#f2d58b", "#8f621d", "#9b1520", "#f7eedb"

S = 2.4; W, H = 576, 384
def M(d, stroke=None, wob=0.5, **kw):
    return svg_mask(W, H, d, scale=S, stroke=stroke * S if stroke else None, wob=wob, seed=nx(), **kw)

def gem(arr, x, y, r, col=RUBY):
    arr = over(arr, gouache_paint(circle_mask(W, H, x, y, r), col, mix(col, "#000000", .3), seed=nx(), rough=0.3))
    return over(arr, gouache_paint(circle_mask(W, H, x - r * .35, y - r * .4, r * .32), "#ffffff", seed=nx(), rough=0.1, density=0.6))

# ---------------- crown (no pins) ----------------
crown = blank(W, H)
fan = np.zeros((H, W), np.float32); veins = np.zeros((H, W), np.float32)
PETALS = [-72, -54, -36, -18, 0, 18, 36, 54, 72]
gems = []
for deg in PETALS:
    k = (72 - abs(deg))
    d = f"M120 132 C 111 110 112 {82 - k / 4} 120 {62 - k / 3} C 128 {82 - k / 4} 129 110 120 132 Z"
    r = deg + rng.uniform(-1.2, 1.2)
    fan = np.maximum(fan, M(d, rot=r, cx=120, cy=132))
    veins = np.maximum(veins, M(f"M120 122 L120 {74 - k / 3.4}", stroke=0.9, rot=r, cx=120, cy=132))
    a = math.radians(r); rr = 40 + k / 5
    gems.append(((120 + math.sin(a) * rr) * S, (132 - math.cos(a) * rr) * S, 2.1 * S))
crown = over(crown, foil(fan, GOLD, seed=nx(), emboss=0.9, sparkle=0.12))
crown = over(crown, linocut(veins, GOLD_D, seed=nx(), wear=0.4, rough=0.6))
inner = np.zeros((H, W), np.float32)
for deg in [-60, -40, -20, 0, 20, 40, 60]:
    inner = np.maximum(inner, M("M120 132 C 114 120 115 106 120 98 C 125 106 126 120 120 132 Z", rot=deg + rng.uniform(-1.5, 1.5), cx=120, cy=132))
crown = over(crown, foil(inner, GOLD_L, seed=nx(), emboss=1.0, sparkle=0.2))
band = M("M44 130 Q120 110 196 130 L192 148 Q120 128 48 148 Z", wob=0.6)
crown = over(crown, foil(band, GOLD, seed=nx(), emboss=1.0, sparkle=0.15))
crown = over(crown, linocut(np.maximum(M("M46 133 Q120 113 194 133", stroke=0.7), M("M48 145 Q120 125 192 145", stroke=0.7)), GOLD_D, seed=nx(), wear=0.4))
for (x, y, r) in gems:
    crown = gem(crown, x, y, r)
for i, x in enumerate([60, 80, 100, 120, 140, 160, 180]):
    y = 129 + abs(120 - x) / 9 - 6
    if i == 3:
        crown = gem(crown, x * S, y * S, 4.2 * S)
    else:
        crown = gem(crown, x * S, y * S, 2.4 * S, PEARL)
tas = np.zeros((H, W), np.float32)
for x in [52, 70, 88, 106, 134, 152, 170, 188]:
    y0 = 146 - abs(120 - x) / 10
    tas = np.maximum(tas, M(f"M{x} {y0} L{x + rng.uniform(-.4, .4)} {y0 + 9}", stroke=1.5))
    tas = np.maximum(tas, circle_mask(W, H, x * S, (y0 + 10) * S, 1.6 * S))
crown = over(crown, foil(tas, GOLD, seed=nx(), emboss=0.6))
save_full(crown, f"{OUT}/crown.webp", quality=84)

# ---------------- goyang pin (vertical, pivot at (120,132)) ----------------
pin = blank(W, H)
stem = M("M120 54 C 123 44 117 36 120 26", stroke=1.3, wob=0.3)
pin = over(pin, foil(stem, GOLD, seed=nx(), emboss=0.4))
bl = np.zeros((H, W), np.float32)
for r in [0, 72, 144, 216, 288]:
    bl = np.maximum(bl, svg_mask(W, H, "M120 21 C 117 18 117 13 120 10 C 123 13 123 18 120 21 Z", scale=S, rot=r + rng.uniform(-4, 4), cx=120, cy=24, wob=0.3, seed=nx()))
pin = over(pin, foil(bl, GOLD_L, seed=nx(), emboss=1.0, sparkle=0.2))
pin = gem(pin, 120 * S, 24 * S, 2.3 * S)
# crop to the pin's own box (viewBox x 108-132, y 6-56) so the animated <img> stays small
x0, x1, y0, y1 = int(108 * S), int(132 * S), int(6 * S), int(56 * S)
save_full(pin[y0:y1, x0:x1], f"{OUT}/goyang.webp", quality=84)

full = crown.copy()
from scipy.ndimage import rotate as ndrot
for deg in [-60, -30, 0, 30, 60]:
    # preview only: rotate the pin around the pivot
    py, px = int(132 * S), int(120 * S)
    big = np.pad(pin, ((0, max(0, 2 * py - H)), (0, 0), (0, 0)))
    rot = ndrot(big, -deg, axes=(1, 0), reshape=False, order=1)[:H]
    full = over(full, rot.astype(np.float32))
preview(full, "pl-crown", bg="#6d0d16")

# ---------------- corner ----------------
W2 = H2 = 120; s2 = 2.5
cr = blank(W2, H2)
lines = np.maximum(svg_mask(W2, H2, "M2 46 V20 M2 46 H28", scale=s2, stroke=1.5 * s2, wob=0.3, seed=nx()), np.zeros((H2, W2), np.float32))
cr = over(cr, foil(lines, GOLD, seed=nx(), emboss=0.4))
l1 = svg_mask(W2, H2, "M8 40 C 8 26 16 16 26 12 C 22 20 20 30 8 40 Z", scale=s2, wob=0.4, seed=nx())
l2 = svg_mask(W2, H2, "M8 40 C 18 38 28 32 34 22 C 26 24 16 30 8 40 Z", scale=s2, wob=0.4, seed=nx())
cr = over(cr, foil(l2, GOLD_D, seed=nx(), emboss=0.9))
cr = over(cr, foil(l1, GOLD, seed=nx(), emboss=0.9, sparkle=0.2))
cr = over(cr, foil(np.maximum(circle_mask(W2, H2, 30 * s2, 10 * s2, 2.2 * s2), circle_mask(W2, H2, 38 * s2, 18 * s2, 1.5 * s2)), GOLD_L, seed=nx(), emboss=0.8))
keep_pixel(cr, 0, 0); keep_pixel(cr, W2 - 1, H2 - 1)
save_full(cr, f"{OUT}/corner.webp", quality=84)

# ---------------- limar jewels ----------------
W3, H3 = 72, 66; s3 = 3.0
def limar(base, red=False):
    a = blank(W3, H3)
    dm = np.zeros((H3, W3), np.float32)
    for x, y in [[12, 1.6], [17, 6], [22, 11], [17, 16], [12, 20.4], [7, 16], [2, 11], [7, 6]]:
        dm = np.maximum(dm, circle_mask(W3, H3, x * s3, y * s3, 1.5 * s3))
    core = svg_mask(W3, H3, "M12 6.6 L16.4 11 L12 15.4 L7.6 11 Z", scale=s3, wob=0.2, seed=nx())
    if red:
        a = over(a, gouache_paint(np.maximum(dm, core), RUBY, "#7a0f18", seed=nx(), rough=0.4))
        a = over(a, foil(svg_mask(W3, H3, "M12 9 L14 11 L12 13 L10 11 Z", scale=s3, seed=nx()), GOLD_L, seed=nx(), emboss=0.6))
    else:
        a = over(a, foil(np.maximum(dm, core), base, seed=nx(), emboss=0.9, sparkle=0.2))
    return a
save(limar(GOLD), f"{OUT}/limar-gold.webp")
save(limar(GOLD, red=True), f"{OUT}/limar-red.webp")

# ---------------- limar field tile ----------------
TS = 288; cell = TS / 4; k = cell / 36
dots = np.zeros((TS, TS), np.float32); cores = np.zeros((TS, TS), np.float32)
for i in range(4):
    for j in range(4):
        ox, oy = j * cell, i * cell
        for x, y in [(18, 5), (24.5, 11.5), (31, 18), (24.5, 24.5), (18, 31), (11.5, 24.5), (5, 18), (11.5, 11.5)]:
            dots = np.maximum(dots, circle_mask(TS, TS, ox + x * k + rng.uniform(-.5, .5), oy + y * k + rng.uniform(-.5, .5), 1.4 * k))
        cores = np.maximum(cores, poly_mask(TS, TS, wobble([(ox + 18 * k, oy + 14 * k), (ox + 22 * k, oy + 18 * k), (ox + 18 * k, oy + 22 * k), (ox + 14 * k, oy + 18 * k)], rng, .5)))
        # corner dots placed at cell centre-offsets so nothing crosses the tile edge
        dots = np.maximum(dots, circle_mask(TS, TS, ox + 1.8 * k, oy + 1.8 * k, 1.2 * k))
tile = blank(TS, TS)
tile = over(tile, foil(np.maximum(dots, cores), GOLD, seed=nx(), emboss=0.5, sparkle=0.15))
save_full(tile, f"{OUT}/limar.webp", quality=80)
preview(np.tile(tile, (2, 2, 1)), "pl-tile", bg="#6d0d16")
