"""Rumah Gadang — gouache rumah gadang silhouette with gonjong roofs + gold foil, songket weave texture.
Run: python3 -I /tmp/pen/art/themes/rumah-gadang.py
Assets → /root/w/frontend/public/themes/art/rumah-gadang/
  cover.webp    painted cover: maroon night sky, rumah gadang with glowing windows   css 390x470 → 780x940 (opaque)
  songket.webp  songket weave tile (gold thread on maroon, thread-level)              css 128px → 256px (repeat, opaque)
  band.webp     pucuk rebung border band (gouache gold)                               css 240x28 → 480x56 (repeat-x)
  divider.webp  itiak pulang patang / kaluak paku foil divider                        css 170x28 → 340x56
  kaluak.webp   kaluak paku fern-curl corner, gold foil (mirror in CSS)               css 130px → 260px
  house.webp    small gouache rumah gadang silhouette (section motif)                 css 220px → 440px
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _r1_lib import *

OUT = outdir("rumah-gadang")
rng = random.Random(21)
nx = Seq(900)
GOLD, GOLD_L, GOLD_D = "#e3b341", "#f6d77a", "#a9801f"
MAROON, MAROON_D, MAROON_L = "#3b0810", "#1f0407", "#6a1222"
INK = "#160306"

# ---------------- rumah gadang silhouette (mask builder) ----------------
def house_masks(W, H, x0, x1, ridge_y, eave_y, floor_y, peaks=5, seed=1):
    """Returns (roof, body, windows, ridge_line, carving, stilts) masks for a rumah gadang spanning x0..x1."""
    r = random.Random(seed)
    span = x1 - x0
    px = [x0 + span * (0.03 + 0.94 * i / (peaks - 1)) for i in range(peaks)]
    depth = eave_y - ridge_y
    ph = [ridge_y + (0 if i in (0, peaks - 1) else depth * 0.16) + r.uniform(-3, 3) for i in range(peaks)]
    top = []
    for i in range(peaks - 1):
        xa, ya, xb, yb = px[i], ph[i], px[i + 1], ph[i + 1]
        n = 28
        for k in range(n):
            t = k / n
            sag = depth * 0.5 * math.sin(math.pi * t) ** 0.65
            top.append((xa + (xb - xa) * t, ya + (yb - ya) * t + sag))
    top.append((px[-1], ph[-1]))
    # outer gonjong: horn-like sweep outward and up
    tipL = curve([(px[0], ph[0] + 4), (x0 - span * 0.035, ph[0] - 14), (x0 - span * 0.06, ph[0] - depth * 0.3)], 14)
    tipR = curve([(px[-1], ph[-1] + 4), (x1 + span * 0.035, ph[-1] - 14), (x1 + span * 0.06, ph[-1] - depth * 0.3)], 14)
    # eave: slightly lifted at both ends, gentle sags under each section
    eave = []
    n = 40
    for k in range(n + 1):
        t = k / n
        x = x0 + span * t
        lift = 18 * (abs(t - 0.5) * 2) ** 2.2
        eave.append((x, eave_y - lift - 6 * math.sin(math.pi * t * (peaks - 1)) ** 2))
    roof_pts = tipL[::-1] + top + tipR + eave[::-1]
    roof = shape_mask(W, H, roof_pts, smooth=False)
    body = poly_mask(W, H, [(x0 + span * 0.05, eave_y - 10), (x1 - span * 0.05, eave_y - 10), (x1 - span * 0.07, floor_y), (x0 + span * 0.07, floor_y)])
    stilts = np.zeros((H, W), np.float32)
    for i in range(8):
        sx = x0 + span * (0.1 + 0.8 * i / 7)
        stilts = np.maximum(stilts, poly_mask(W, H, [(sx - 4, floor_y - 2), (sx + 4, floor_y - 2), (sx + 4, floor_y + 20), (sx - 4, floor_y + 20)]))
    body = np.maximum(body, stilts)
    windows = np.zeros((H, W), np.float32)
    nwin = 7
    for i in range(nwin):
        wx = x0 + span * (0.13 + 0.74 * i / (nwin - 1))
        hh = (floor_y - eave_y) * (0.48 if i != nwin // 2 else 0.68)
        wy = eave_y + (floor_y - eave_y) * 0.16
        windows = np.maximum(windows, poly_mask(W, H, [(wx - 9, wy), (wx + 9, wy), (wx + 9, wy + hh), (wx - 9, wy + hh)]))
    ridge = stroke_mask(W, H, tipL[::-1] + top + tipR, 2.4, taper=(0.02, 0.02))
    for i in range(peaks):
        ridge = np.maximum(ridge, stroke_mask(W, H, [(px[i], ph[i] + 6), (px[i] + (-1 if i < peaks / 2 else 1) * 2, eave_y - 14)], 1.1, taper=(0.1, 0.5)))
    carving = np.zeros((H, W), np.float32)
    cy = eave_y - 1
    xx = x0 + span * 0.08
    while xx < x1 - span * 0.08:
        carving = np.maximum(carving, poly_mask(W, H, [(xx, cy - 4), (xx + 5, cy), (xx, cy + 4), (xx - 5, cy)]))
        xx += 12
    carving = np.maximum(carving, stroke_mask(W, H, [(x0 + span * 0.07, cy + 8), (x1 - span * 0.07, cy + 8)], 1.4, taper=(0.02, 0.02)))
    return roof, body, windows, ridge, carving, stilts

def carving_field(W, H, cell, seed):
    """Ukiran wall carving: lattice of small diamonds with a seed dot, plus pucuak rabuang teeth (mask)."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.0, cell * 0.09))
        f = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for j in range(int(H / cell) + 2):
            for i in range(int(W / cell) + 2):
                cx = i * cell + (j % 2) * cell / 2; cy = j * cell * 0.8
                d = cell * 0.36
                cv.c.drawPath(poly_path([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)]), p)
                cv.c.drawCircle(cx, cy, cell * 0.08, f)
    return mask_from(W, H, draw)


def paint_house(W, H, x0, x1, ridge_y, eave_y, floor_y, peaks=5, seed=1, glow_win=True, scale=1.0):
    roof, body, windows, ridge, carving, stilts = house_masks(W, H, x0, x1, ridge_y, eave_y, floor_y, peaks, seed)
    yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    wall = np.clip(body - stilts, 0, 1)
    # carved wooden wall: deep red gouache with a gold-picked ukiran lattice (traditional red/black/gold palette)
    art = over(art, gouache_paint(wall, "#6a1420", "#7d1c26", seed=nx(), rough=1.4, streak=0.8))
    cf = carving_field(W, H, 15 * scale ** 0.5, seed) * np.clip(wall - gaussian_filter(windows, 2) * 2, 0, 1)
    pick = foil(np.clip(cf, 0, 1), GOLD_D, seed=nx(), emboss=0.4, sparkle=0.05)
    pick[..., 3] *= 0.55 * (0.7 + 0.3 * fbm(W, H, nx(), 20, 2))
    art = over(art, pick)
    # black lintel bands at top and bottom of the wall
    top_b = wall * (yy_ < eave_y + (floor_y - eave_y) * 0.12)
    bot_b = wall * (yy_ > floor_y - (floor_y - eave_y) * 0.1)
    art = over(art, gouache_paint(np.clip(top_b + bot_b, 0, 1), "#24060a", "#2e0a0e", seed=nx(), rough=0.8))
    art = over(art, gouache_paint(stilts, "#2b0d0a", "#3b1710", seed=nx(), rough=1.0))
    # ijuk (sugar-palm fibre) thatch: dark warm brown, streaks follow the slope, moonlit along the ridge
    roofp = gouache_paint(roof, "#2c120d", "#3d1a12", seed=nx(), rough=2.0, streak=1.0)
    st = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (7, 0.7))
    st = (st - st.mean()) / (st.std() + 1e-6)
    roofp[..., :3] = np.clip(roofp[..., :3] * (1 + st[..., None] * 0.22), 0, 1)
    rim = np.clip(roof - np.roll(gaussian_filter(roof, 3 * scale), int(5 * scale), 0), 0, 1)
    roofp[..., :3] = roofp[..., :3] * (1 - rim[..., None] * 0.6) + np.array(hex_rgb("#a0563a"), np.float32) * rim[..., None] * 0.6
    art = over(art, roofp)
    # shadow of the eave on the wall
    art = over(art, soft_shadow(roof * (yy_ > eave_y - 30), "#120203", blur=5 * scale, strength=0.6, dx=0, dy=int(6 * scale)) * np.concatenate([np.ones((H, W, 3)), wall[..., None]], -1))
    if glow_win:
        art = over(art, glow(windows, "#f2b24a", radius=8 * scale, strength=0.35))
        art = over(art, gouache_paint(windows, "#d99436", "#f0c063", seed=nx(), rough=0.8, streak=0.6))
        # window lattice (dark bars) + shutters
        bars = np.clip(windows - gaussian_filter(windows, 1.2) * 1.05, 0, 1)
        mull = windows * (np.abs(((xx_ + 0.5) % (9 * scale)) - 4.5 * scale) < 0.8 * scale)
        art = over(art, gouache_paint(np.clip(bars * 3 + mull, 0, 1), "#4a1f0a", seed=nx(), rough=0.3, density=0.8))
    else:
        art = over(art, gouache_paint(windows, "#2a070b", "#36090f", seed=nx(), rough=0.6))
        art = over(art, foil(np.clip(windows - gaussian_filter(windows, 1.0) * 1.05, 0, 1) * 3, GOLD, seed=nx(), emboss=0.4))
    art = over(art, foil(ridge, GOLD, seed=nx(), emboss=0.6, sparkle=0.1))
    art = over(art, foil(carving, GOLD, seed=nx(), emboss=0.6, sparkle=0.08))
    return art, np.maximum(roof, body)


# ---------------- cover ----------------
W, H = 780, 940
sky = painted_sky(W, H, [(0, "#1a0306"), (0.22, "#3a0a12"), (0.4, "#7e2434"), (0.5, "#8e343c"), (0.64, "#5a1020"), (1.0, "#3b0810")], seed=nx(), streak=0.8, grain=0.6)
# faint stars / dust high in the sky
dust = np.zeros((H, W), np.float32)
for _ in range(90):
    x, y = rng.uniform(0, W), rng.uniform(0, H * 0.45)
    dust = np.maximum(dust, circle_mask(W, H, x, y, rng.uniform(0.8, 1.8)))
cover = over(sky, glow(dust, "#f6d77a", radius=1.2, strength=0.25))
# moon: thin crescent glow upper left
moon = np.clip(circle_mask(W, H, 400, 120, 40) - circle_mask(W, H, 416, 109, 36), 0, 1)
cover = over(cover, glow(moon, "#f6d77a", radius=22, strength=0.3))
cover = over(cover, pigment(moon, "#f3d98a", "#e7b94c", seed=nx(), density=0.9, edge=0.3, bloom=0.2, rough=2))
# distant hills (Bukit Barisan) as dark washes
hills = blank(W, H)
for k, (yy0, col) in enumerate([(455, "#4a1420"), (490, "#36101a"), (520, "#2a0a10")]):
    pts = [(x, yy0 + 26 * math.sin(x / (120 + k * 40) + k) + 10 * math.sin(x / 37 + k * 2)) for x in range(-20, W + 40, 20)] + [(W + 40, H), (-20, H)]
    hills = glaze(hills, pigment(shape_mask(W, H, pts, smooth=True), col, seed=nx(), density=0.85, edge=0.25, bloom=0.15, rough=6))
cover = over(cover, hills)
# songket field at the bottom (fades in), painted as a soft weave behind the house
# main house
house, hmask = paint_house(W, H, 90, 690, 250, 490, 600, peaks=5, seed=3, scale=2.0)
# a smaller second house further back to the right (rangkiang / neighbour)
small, smask = paint_house(W, H, 600, 800, 420, 520, 580, peaks=3, seed=5, glow_win=True, scale=1.2)
small[..., 3] *= 0.8
cover = over(cover, small)
# ground glow under the house (lamps)
cover = over(cover, glow(np.clip(gaussian_filter(hmask, 2), 0, 1) * (np.mgrid[0:H, 0:W][0] > 560), "#c97a2a", radius=28, strength=0.25))
cover = over(cover, house)
# ground: dark soil with a faint path
ground = poly_mask(W, H, [(0, 615), (W, 605), (W, H), (0, H)])
cover = over(cover, gouache_paint(ground, "#1c0406", "#2a070b", seed=nx(), rough=3, streak=0.8))
# coconut palms silhouettes at the sides: bold drooping fronds
palms = np.zeros((H, W), np.float32)
for (bx, by, hgt, lean) in [(30, 660, 300, 0.16), (752, 665, 250, -0.14)]:
    trunk = curve([(bx, by), (bx + lean * 90, by - hgt * 0.5), (bx + lean * 170, by - hgt)], 40)
    palms = np.maximum(palms, stroke_mask(W, H, trunk, 10, taper=(0.02, 0.35)))
    tx, ty = trunk[-1]
    for q in range(7):
        a = -math.pi / 2 + (q - 3) * 0.5 + lean * 2
        fr = curve([(tx, ty), (tx + math.cos(a) * 70, ty + math.sin(a) * 70 + 8), (tx + math.cos(a) * 130, ty + math.sin(a) * 130 + 60)], 24)
        palms = np.maximum(palms, stroke_mask(W, H, fr, 7, taper=(0.05, 0.4)))
        for j in range(2, len(fr) - 1, 2):
            x, y = fr[j]
            d = (fr[j + 1][0] - fr[j - 1][0], fr[j + 1][1] - fr[j - 1][1]); da = math.atan2(d[1], d[0])
            L = 44 * (1 - j / len(fr)) + 10
            palms = np.maximum(palms, leaf_mask(W, H, x, y, L, 5, da + 0.9, n=8))
            palms = np.maximum(palms, leaf_mask(W, H, x, y, L, 5, da - 0.9, n=8))
cover = over(cover, gouache_paint(palms, INK, "#1d0508", seed=nx(), rough=1.4, streak=0.3))
cover = add_grain(vignette(cover, 0.35, 1.8), nx(), 0.035)
save_rgb(cover, f"{OUT}/cover.webp", quality=80)
Image.fromarray((np.clip(cover[..., :3], 0, 1) * 255).astype(np.uint8)).resize((390, 470)).save(f"{PREV}/rg-cover.png")

# ---------------- songket weave tile ----------------
T = 256
# ground threads: fine warp/weft lines
yy, xx = np.mgrid[0:T, 0:T].astype(np.float32)
warp = 0.5 + 0.5 * np.sin(xx * math.pi / 2)   # 4px period
weft = 0.5 + 0.5 * np.sin(yy * math.pi / 2)
ground = np.array(hex_rgb(MAROON), np.float32)[None, None, :] * (0.86 + 0.1 * warp + 0.08 * weft)[..., None]
tile = np.concatenate([ground, np.ones((T, T, 1), np.float32)], -1)
# supplementary gold weft motif: diamond lattice with pucuk rebung + small flowers (bungo)
motif = np.zeros((T, T), np.float32)
cell = 64
for i in range(0, T // cell + 1):
    for j in range(0, T // cell + 1):
        cx, cy = i * cell, j * cell
        # diamond outline (step pattern, like woven threads: horizontal dashes)
        for k in range(-7, 8):
            dy = k * 4
            half = max(0, 28 - abs(k) * 4)
            if half <= 0:
                continue
            for sx in (-1, 1):
                motif = np.maximum(motif, poly_mask(T, T, [(cx + sx * half - 3, cy + dy - 1.2), (cx + sx * half + 3, cy + dy - 1.2), (cx + sx * half + 3, cy + dy + 1.2), (cx + sx * half - 3, cy + dy + 1.2)]))
        # centre flower: a cross of dashes
        for k in range(-2, 3):
            motif = np.maximum(motif, poly_mask(T, T, [(cx - 8 + abs(k) * 3, cy + k * 4 - 1.2), (cx + 8 - abs(k) * 3, cy + k * 4 - 1.2), (cx + 8 - abs(k) * 3, cy + k * 4 + 1.2), (cx - 8 + abs(k) * 3, cy + k * 4 + 1.2)]))
        # pucuk rebung in the mid cell
        mx, my = cx + cell / 2, cy + cell / 2
        for k in range(0, 6):
            half = 2 + k * 2.6
            motif = np.maximum(motif, poly_mask(T, T, [(mx - half, my - 10 + k * 4 - 1.2), (mx + half, my - 10 + k * 4 - 1.2), (mx + half, my - 10 + k * 4 + 1.2), (mx - half, my - 10 + k * 4 + 1.2)]))
motif = np.maximum(motif, 0)
motif = np.roll(motif, 0)  # already periodic (cell divides T)
# thread texture: gold weft is made of horizontal thread segments
thread = 0.75 + 0.25 * (0.5 + 0.5 * np.sin(yy * math.pi / 2))
gold_t = foil(motif, GOLD, seed=nx(), emboss=0.4, sparkle=0.2)
gold_t[..., :3] *= thread[..., None]
gold_t[..., 3] *= 0.92
# loose threads / wear
gold_t[..., 3] *= 1 - 0.35 * np.clip((wrap_noise(T, T, nx(), 2) - 0.6) * 4, 0, 1)
tile = over(tile, gold_t)
save_rgb(tile, f"{OUT}/songket.webp", quality=80)
Image.fromarray((np.clip(tile[..., :3], 0, 1) * 255).astype(np.uint8)).resize((512, 512), Image.NEAREST).save(f"{PREV}/rg-songket.png")

# ---------------- pucuk rebung band ----------------
BW, BH = 480, 56
bm = np.zeros((BH, BW), np.float32)
for i in range(0, BW // 48 + 1):
    bx = i * 48
    tri = poly_mask(BW, BH, [(bx, 46), (bx + 24, 6), (bx + 48, 46)])
    tri_in = poly_mask(BW, BH, [(bx + 9, 42), (bx + 24, 18), (bx + 39, 42)])
    bm = np.maximum(bm, np.clip(tri - tri_in, 0, 1))
    bm = np.maximum(bm, poly_mask(BW, BH, [(bx + 24, 26), (bx + 30, 34), (bx + 24, 42), (bx + 18, 34)]))
    bm = np.maximum(bm, circle_mask(BW, BH, bx + 24, 51, 2.4))
bm = np.maximum(bm, stroke_mask(BW, BH, [(0, 2.5), (BW, 2.5)], 2.2, taper=(0.01, 0.01)))
band = gouache_paint(bm, GOLD, GOLD_D, seed=nx(), rough=1.0, streak=0.7, density=0.92)
band[..., 3] *= 1 - 0.3 * np.clip((wrap_noise(BW, BH, nx(), 1.5) - 0.62) * 5, 0, 1)
save_full(band, f"{OUT}/band.webp", quality=82)
preview(band, "rg-band", bg=MAROON)

# ---------------- divider (itiak pulang patang: ducks going home in a row) ----------------
DW, DH = 340, 56
dm = np.zeros((DH, DW), np.float32)
cy = DH / 2
for side in (-1, 1):
    line = curve([(DW / 2 + side * 30, cy), (DW / 2 + side * 90, cy - 1), (DW / 2 + side * 150, cy + 1), (DW / 2 + side * 166, cy)], 40)
    dm = np.maximum(dm, stroke_mask(DW, DH, line, 2.2, taper=(0.02, 0.6)))
    # three little duck shapes (comma strokes) marching toward the centre
    for q in range(3):
        x = DW / 2 + side * (52 + q * 34)
        body = shape_mask(DW, DH, ellipse_pts(x, cy - 7, 9, 5, 12, 0))
        neck = stroke_mask(DW, DH, curve([(x - side * 7, cy - 9), (x - side * 11, cy - 15), (x - side * 9, cy - 20)], 12), 3.2, taper=(0.1, 0.3))
        head = circle_mask(DW, DH, x - side * 9, cy - 20, 3.2)
        dm = np.maximum.reduce([dm, body, neck, head])
# kaluak paku curl at the centre
for side in (-1, 1):
    sp = [(DW / 2 + side * (4 + 10 * t) + side * math.cos(t * 6) * 6 * (1 - t), cy - 12 + math.sin(t * 6) * 6 * (1 - t) + t * 6) for t in [k / 24 for k in range(25)]]
    dm = np.maximum(dm, stroke_mask(DW, DH, sp, 2.6, taper=(0.05, 0.5)))
dm = np.maximum(dm, poly_mask(DW, DH, [(DW / 2, cy - 6), (DW / 2 + 6, cy + 2), (DW / 2, cy + 10), (DW / 2 - 6, cy + 2)]))
divider = over(blank(DW, DH), soft_shadow(dm, "#000000", blur=1.5, strength=0.4, dx=0, dy=1))
divider = over(divider, foil(dm, GOLD, seed=nx(), emboss=0.8, sparkle=0.15))
save_full(divider, f"{OUT}/divider.webp", quality=84)
preview(divider, "rg-divider", bg=MAROON)

# ---------------- kaluak paku corner (fern curls) ----------------
KW = KH = 260
km = np.zeros((KH, KW), np.float32)
def fern(cx, cy, r, a0, turns, ccw, width, n=50):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + ccw * t * turns * math.tau
        rr = r * (1 - t) + 2
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return stroke_mask(KW, KH, pts, width, taper=(0.02, 0.5))
stem = curve([(6, 254), (30, 200), (70, 150), (120, 110), (180, 80), (254, 60)], 60)
km = np.maximum(km, stroke_mask(KW, KH, stem, 6, taper=(0.02, 0.3)))
stem2 = curve([(8, 250), (26, 180), (50, 110), (74, 50), (84, 6)], 50)
km = np.maximum(km, stroke_mask(KW, KH, stem2, 6, taper=(0.02, 0.3)))
for (cx, cy, r, a0, turns, ccw, wd) in [(236, 66, 26, math.pi * 0.9, 0.9, 1, 4.5), (86, 24, 22, math.pi * 1.4, 0.9, -1, 4.5), (120, 118, 20, 2.4, 0.85, -1, 4), (60, 160, 18, 0.5, 0.85, 1, 4), (160, 96, 14, 3.4, 0.8, 1, 3.4), (46, 110, 14, -0.8, 0.8, -1, 3.4), (34, 214, 14, 2.2, 0.8, 1, 3.2)]:
    km = np.maximum(km, fern(cx, cy, r, a0, turns, ccw, wd))
# fiddlehead tips (little dots) + small leaflets along the stems
dots = np.zeros((KH, KW), np.float32)
for (cx, cy) in [(236, 66), (86, 24), (120, 118), (60, 160), (160, 96), (46, 110), (34, 214)]:
    dots = np.maximum(dots, circle_mask(KW, KH, cx, cy, 3.4))
lv = np.zeros((KH, KW), np.float32)
for j in range(6, len(stem) - 6, 8):
    x, y = stem[j]
    lv = np.maximum(lv, leaf_mask(KW, KH, x, y, 18, 4.5, -math.pi / 2 - 0.4, n=8, cup=0.3))
for j in range(6, len(stem2) - 6, 8):
    x, y = stem2[j]
    lv = np.maximum(lv, leaf_mask(KW, KH, x, y, 18, 4.5, 0.2, n=8, cup=0.3))
kal = over(blank(KW, KH), soft_shadow(np.maximum.reduce([km, dots, lv]), "#000000", blur=3, strength=0.5, dx=1, dy=2))
kal = over(kal, foil(km, GOLD, seed=nx(), emboss=0.7, sparkle=0.12))
kal = over(kal, foil(lv, GOLD_L, seed=nx(), emboss=0.9, sparkle=0.1))
kal = over(kal, foil(dots, GOLD_D, seed=nx(), emboss=0.9, sparkle=0.1))
save(kal, f"{OUT}/kaluak.webp", max_w=260)
preview(kal, "rg-kaluak", bg=MAROON)

# ---------------- small house motif (section ornament) ----------------
HW, HH = 440, 250
hs, _ = paint_house(HW, HH, 40, 400, 52, 156, 212, peaks=5, seed=9, glow_win=False, scale=1.0)
save(hs, f"{OUT}/house.webp", max_w=440)
preview(hs, "rg-house", bg="#4a0c16")
print("total KB:", sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1024)
