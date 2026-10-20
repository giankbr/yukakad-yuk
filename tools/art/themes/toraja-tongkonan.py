"""Toraja Tongkonan — linocut relief print + matte gouache (red / black / yellow / white of the pa'ssura carvings).
Run: python3 -I /tmp/pen/art/themes/toraja-tongkonan.py
Assets → /root/w/frontend/public/themes/art/toraja-tongkonan/
  house.webp      tongkonan front view (cover / closing hero)   css 250px → 504px
  rays.webp       pa' barre allo sun rays (rotating)            css 260px → 520px
  sun.webp        barre allo disc with four-way cross            css  74–260px → 300px
  plate.webp      barre allo disc without cross (monogram)       css 86px → 300px
  roof-red.webp   upswept roof crown for event cards             css 100% x 44 → 600px
  roof-black.webp upswept roof crown for the couple cards        css 132 x 30 → 600px
  band.webp       pa'ssura border tile (8 repeats)               css 256x18 → 512x36
  tedong-red.webp / tedong-black.webp  buffalo-head markers      css 28–48px → 96px
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g_util import *

OUT = outdir("toraja-tongkonan")
rng = random.Random(23)
nx = Seq(700)
BLACK, BLACK2, RED, RED_D, YEL, YEL_L, WHITE = "#16110f", "#2a201b", "#a3201b", "#7a1612", "#e5a823", "#f2c75b", "#f0e7d8"

# ---------------- house ----------------
S = 2.1; W, H = 504, 420
def M(d, stroke=None, wob=0.7):
    return svg_mask(W, H, d, scale=S, stroke=stroke * S if stroke else None, wob=wob, seed=nx())

house = blank(W, H)
# ground wash
ground = M("M20 186 C 70 180 170 180 222 186 L 226 196 C 160 192 80 192 16 196 Z", wob=1.2)
house = glaze(house, pigment(ground, "#4a3426", "#2a1d16", seed=nx(), density=0.75, edge=0.4, bloom=0.2, rough=5))
# stilts, beam, pillar (linocut black)
struct = M("M80 146 H160 V152 H80 Z")
for x in [90, 104, 136, 150]:
    struct = np.maximum(struct, M(f"M{x-2.8} 151 H{x+2.8} L{x+2.4} 187 H{x-2.4} Z"))
struct = np.maximum(struct, M("M116.6 96 H123.4 L123 188 H117 Z"))
house = over(house, linocut(struct, BLACK, seed=nx(), wear=0.25))
# facade (red gouache), flaring upwards
fac = M("M73 95 H167 L154 147 H86 Z", wob=0.9)
house = over(house, gouache_paint(fac, RED, RED_D, seed=nx(), rough=1.4, streak=1.1))
# carving bands on facade: black lines, yellow zigzag, white dots/circles
carve = np.maximum(M("M80 110 H160", stroke=1.6), M("M84 128 H156", stroke=1.6))
carve = np.maximum(carve, M("M74 96 H166", stroke=1.8))
house = over(house, linocut(carve, BLACK, seed=nx(), wear=0.3))
zig = "M82 110 " + " ".join(f"L{82 + i * 4.75 + 4.75:.2f} {102 if i % 2 == 0 else 110}" for i in range(16))
house = over(house, linocut(M(zig, stroke=1.6), YEL, seed=nx(), wear=0.35))
dots = np.zeros((H, W), np.float32)
for i in range(8):
    dots = np.maximum(dots, circle_mask(W, H, (92.5 + i * 9) * S + rng.uniform(-1, 1), 137 * S + rng.uniform(-1, 1), 2.1 * S))
house = over(house, gouache_paint(dots, WHITE, seed=nx(), rough=0.6))
rings = np.maximum(ring_mask(W, H, 89 * S, 119 * S, 4 * S, 1.5 * S), ring_mask(W, H, 151 * S, 119 * S, 4 * S, 1.5 * S))
house = over(house, gouache_paint(rings, WHITE, seed=nx(), rough=0.5))
# kabongo' buffalo head carving
horns = M("M108 115 Q 102 108 97 112 Q 104 116 110 121 M132 115 Q 138 108 143 112 Q 136 116 130 121", stroke=2.2)
house = over(house, gouache_paint(horns, WHITE, seed=nx(), rough=0.6))
house = over(house, linocut(M("M112 115 H128 L124 128 H116 Z"), BLACK, seed=nx(), wear=0.2))
# stacked buffalo horns on the pillar (white gouache with black outline)
for y in [156, 164, 172, 180]:
    hm = M(f"M105 {y - 4} Q 120 {y + 4} 135 {y - 4} Q 120 {y + 8} 105 {y - 4} Z", wob=0.5)
    house = over(house, gouache_paint(hm, WHITE, "#d9cdb8", seed=nx(), rough=0.8))
    house = over(house, linocut(M(f"M105 {y - 4} Q 120 {y + 8} 135 {y - 4}", stroke=0.9), BLACK, seed=nx(), wear=0.3))
# saddle roof: black linocut with bamboo layer cuts and yellow edge
roof = M("M2 6 Q 60 70 120 70 Q 180 70 238 6 L 229 42 Q 180 98 120 98 Q 60 98 11 42 Z", wob=1.0)
house = over(house, gouache_paint(roof, "#2e231d", "#1c1512", seed=nx(), rough=1.4, streak=1.4))
cuts = np.zeros((H, W), np.float32)
for k, off in enumerate([3, 7, 11, 15, 19, 23]):
    cuts = np.maximum(cuts, M(f"M{5 + k * 1.1} {10 + off * 1.3} Q 60 {72 + off * 1.05} 120 {72 + off * 1.05} Q 180 {72 + off * 1.05} {235 - k * 1.1} {10 + off * 1.3}", stroke=0.7, wob=0.9))
house = over(house, linocut(cuts, "#8a6a50", seed=nx(), wear=0.5))
edge = np.maximum(M("M2 6 Q 60 70 120 70 Q 180 70 238 6", stroke=1.7, wob=0.6), M("M11 42 Q 60 98 120 98 Q 180 98 229 42", stroke=1.4, wob=0.6))
house = over(house, linocut(edge, YEL, seed=nx(), wear=0.35))
# rooster at the gable tip
house = over(house, gouache_paint(M("M116 67 q 3 -9 9 -7 q -1 4 -4 5 l 3 4 z"), YEL, seed=nx(), rough=0.6))
house = over(house, linocut(M("M38 189 H202", stroke=1.6, wob=1.0), YEL, seed=nx(), wear=0.4))
save(house, f"{OUT}/house.webp", max_w=504)
preview(house, "tj-house", bg="#2a1512")

# ---------------- sun: rays + discs ----------------
W = H = 520; C = W / 2; S2 = W / 120
rays = blank(W, H)
ry_y = np.zeros((H, W), np.float32); ry_w = np.zeros((H, W), np.float32)
for i in range(16):
    a = math.radians(i * 22.5 + rng.uniform(-1, 1))
    ro, ri, hw = 57 * S2, 43 * S2, math.radians(5.6)
    pts = [(C + math.sin(a - hw) * ro, C - math.cos(a - hw) * ro), (C + math.sin(a) * ri, C - math.cos(a) * ri), (C + math.sin(a + hw) * ro, C - math.cos(a + hw) * ro)]
    m = poly_mask(W, H, wobble(pts, rng, 2))
    if i % 2: ry_w = np.maximum(ry_w, m)
    else: ry_y = np.maximum(ry_y, m)
rays = over(rays, gouache_paint(ry_y, YEL, "#c98d18", seed=nx(), rough=2, streak=1.2))
rays = over(rays, gouache_paint(ry_w, WHITE, "#d8ccb6", seed=nx(), rough=2, streak=1.2))
save_full(rays, f"{OUT}/rays.webp")

W = H = 300; C = W / 2; S3 = W / 86
def disc(cross):
    d = blank(W, H)
    d = over(d, linocut(circle_mask(W, H, C, C, 42 * S3), BLACK, seed=nx(), wear=0.15))
    d = over(d, linocut(ring_mask(W, H, C, C, 41.5 * S3, 1.8 * S3), YEL, seed=nx(), wear=0.35))
    d = over(d, gouache_paint(circle_mask(W, H, C, C, 35 * S3), RED, RED_D, seed=nx(), rough=1.8, streak=1.1))
    if cross:
        pet = np.zeros((H, W), np.float32)
        for deg in [0, 90, 180, 270]:
            pet = np.maximum(pet, svg_mask(W, H, "M60 60 C 52 50 52 36 60 28 C 68 36 68 50 60 60 Z", scale=S3, tx=C - 60 * S3, ty=C - 60 * S3, rot=deg + rng.uniform(-2, 2), cx=60, cy=60, wob=0.8, seed=nx()))
        d = over(d, gouache_paint(pet, YEL, "#c98d18", seed=nx(), rough=1.2))
        dd = np.zeros((H, W), np.float32)
        for deg in [45, 135, 225, 315]:
            a = math.radians(deg)
            dd = np.maximum(dd, circle_mask(W, H, C + math.sin(a) * 26 * S3, C - math.cos(a) * 26 * S3, 3 * S3))
        d = over(d, gouache_paint(dd, WHITE, seed=nx(), rough=0.6))
        d = over(d, linocut(circle_mask(W, H, C, C, 7.5 * S3), WHITE, seed=nx(), wear=0.1))
        d = over(d, linocut(circle_mask(W, H, C, C, 5.4 * S3), BLACK, seed=nx(), wear=0.1))
    else:
        dash = np.zeros((H, W), np.float32)
        for k in range(36):
            a = k / 36 * math.tau
            dash = np.maximum(dash, circle_mask(W, H, C + math.cos(a) * 28 * S3, C + math.sin(a) * 28 * S3, 0.75 * S3))
        d = over(d, gouache_paint(dash, WHITE, seed=nx(), rough=0.4, density=0.8))
    return d
sun = disc(True); save_full(sun, f"{OUT}/sun.webp")
plate = disc(False); save_full(plate, f"{OUT}/plate.webp")
preview(rays, "tj-rays", bg=BLACK); preview(sun, "tj-sun", bg=BLACK)

# ---------------- roof crowns ----------------
W, H = 600, 128; S4 = 3.0
def roof_img(col, col2, line):
    r = blank(W, H)
    m = svg_mask(W, H, "M2 2 Q 50 30 100 30 Q 150 30 198 2 L 192 16 Q 150 40 100 40 Q 50 40 8 16 Z", scale=S4, ty=2, wob=1.0, seed=nx())
    r = over(r, gouache_paint(m, col, col2, seed=nx(), rough=1.6, streak=1.2))
    cuts = np.zeros((H, W), np.float32)
    for k, off in enumerate([4, 8]):
        cuts = np.maximum(cuts, svg_mask(W, H, f"M{5 + k} {5 + off} Q 50 {32 + off * .3} 100 {32 + off * .3} Q 150 {32 + off * .3} {195 - k} {5 + off}", scale=S4, ty=2, stroke=1.4, wob=0.8, seed=nx()))
    r = over(r, linocut(cuts, line, seed=nx(), wear=0.45))
    return r
save_full(roof_img(RED, RED_D, YEL), f"{OUT}/roof-red.webp")
save_full(roof_img(BLACK, BLACK2, YEL), f"{OUT}/roof-black.webp")
preview(roof_img(RED, RED_D, YEL), "tj-roof", tone="#f7f1e6")

# ---------------- pa'ssura band tile ----------------
TW, TH, n = 512, 36, 8
cw = TW / n; sc = cw / 32
band = np.zeros((TH, TW, 4), np.float32)
band[..., :3] = np.array(hex_rgb(BLACK), np.float32); band[..., 3] = 1
band = over(band, gouache_paint(np.ones((TH, TW), np.float32), BLACK, BLACK2, seed=nx(), rough=0, streak=1.5))
reds = np.zeros((TH, TW), np.float32); zz = np.zeros((TH, TW), np.float32); wd = np.zeros((TH, TW), np.float32)
for k in range(n):
    x0 = k * cw
    reds = np.maximum(reds, poly_mask(TW, TH, wobble([(x0 + 1 * sc, 36), (x0 + 8 * sc, 10), (x0 + 15 * sc, 36)], rng, .6)))
    reds = np.maximum(reds, poly_mask(TW, TH, wobble([(x0 + 17 * sc, 0), (x0 + 24 * sc, 26), (x0 + 31 * sc, 0)], rng, .6)))
    wd = np.maximum(wd, circle_mask(TW, TH, x0 + 8 * sc, 26, 3.0)); wd = np.maximum(wd, circle_mask(TW, TH, x0 + 24 * sc, 10, 3.0))
zpts = []
for k in range(n * 2 + 1):
    zpts.append((k * cw / 2, 20 if k % 2 == 0 else (6 if (k // 1) % 4 == 1 else 32)))
def zdraw(cv):
    p = skia.Path(); p.moveTo(-4, 20)
    for x, y in zpts: p.lineTo(x + rng.gauss(0, .4), y + rng.gauss(0, .4))
    p.lineTo(TW + 4, 20)
    cv.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, StrokeJoin=skia.Paint.kRound_Join))
zz = mask_from(TW, TH, zdraw)
band = over(band, gouache_paint(reds, RED, RED_D, seed=nx(), rough=0.8))
band = over(band, linocut(zz, YEL, seed=nx(), wear=0.3, rough=0.6))
band = over(band, gouache_paint(wd, WHITE, seed=nx(), rough=0.4))
band[..., 3] = 1
save_full(band, f"{OUT}/band.webp", quality=80)
preview(np.concatenate([band, band], 1), "tj-band", bg=BLACK)

# ---------------- tedong markers ----------------
W, H = 120, 96; S5 = 3.0
for name, col, col2, eye in [("red", RED, RED_D, BLACK), ("black", BLACK, BLACK2, "#f7f1e6"), ("yellow", YEL, "#c98d18", BLACK)]:
    t = blank(W, H)
    hm = svg_mask(W, H, "M14 12 C 6 12 1 7 2 1 C 6 6 10 8 16 8 Z M26 12 C 34 12 39 7 38 1 C 34 6 30 8 24 8 Z", scale=S5, wob=0.5, seed=nx())
    hd = svg_mask(W, H, "M13 9 H27 L24 27 Q 20 31 16 27 Z", scale=S5, wob=0.5, seed=nx())
    t = over(t, linocut(np.maximum(hm, hd), col, seed=nx(), wear=0.3, rough=1.0))
    eyes = np.maximum(circle_mask(W, H, 17 * S5, 15 * S5, 1.7 * S5), circle_mask(W, H, 23 * S5, 15 * S5, 1.7 * S5))
    t = over(t, gouache_paint(eyes, eye, seed=nx(), rough=0.4))
    save(t, f"{OUT}/tedong-{name}.webp", max_w=96)
