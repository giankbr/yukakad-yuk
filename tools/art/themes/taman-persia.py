"""Taman Persia — Persian-miniature-style chahar bagh (no figures): gold-leaf sky with lapis cloud bands, tiled
pavilion, four-fold garden with water channels and octagonal pool, cypresses, pomegranate trees, flower beds;
illuminated shamsa, lapis-and-gold illumination band, pomegranate branch. Opaque gouache + gold, fine brush detail.
Run: python3 -I taman-persia.py [part ...]   parts: garden cypress pomegranate shamsa rule paper
Assets -> public/themes/art/taman-persia/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a3_lib import *

OUT = outdir("taman-persia")
PARTS = sys.argv[1:] or ["garden", "cypress", "pomegranate", "shamsa", "rule", "paper"]
LAPIS, LAPIS_D, LAPIS_L = "#1f3a8a", "#132560", "#4a6cc2"
GOLD = "#c9a24a"
CYP, CYP_D, CYP_L = "#1f4a35", "#12301f", "#3b7351"
PIST, PIST_D = "#9fb87a", "#7c9a5c"
POM, POM_D = "#b8302a", "#7c1a1c"
WATER, SILVER = "#8fb3c9", "#dfe8ee"
IVORY = "#f3ead6"


def fine(W, H, pts, w=1.2):
    return strokes(W, H, [(pts, w, (0.1, 0.2))])


def paint_cypress(art, W, H, x, by, h, w, rng, nx, lean=0.0):
    poly = cypress_poly(x, by, h, w, rng, lean)
    m = shape_mask(W, H, poly)
    art = GP(art, m, CYP, CYP_D, seed=nx(), rough=0.8, streak=0.7)
    # fine foliage strokes: chevrons of lighter green, each a single tiny brush stroke
    items = []
    for t in np.linspace(0.06, 0.92, int(h / 7)):
        yy = by - h * t
        wd = w * (math.sin(math.pi * min(1, t * 1.05)) ** 0.55) * (1 - t) ** 0.35 * 0.8
        cx = x + lean * h * t * t
        for u in np.linspace(-0.8, 0.8, max(2, int(wd / 4))):
            px = cx + u * wd
            items.append(([(px - 3, yy + 2), (px, yy - 1), (px + 3, yy + 2)], 1.3, None))
    art = GP(art, strokes(W, H, items) * m, CYP_L, seed=nx(), rough=0.3, density=0.8)
    edge = np.clip(np.roll(m, 3, 1) - m, 0, 1) * 0 + np.clip(m - np.roll(m, -4, 1), 0, 1)
    art = G(art, edge, CYP_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    trunk = strokes(W, H, [([(x, by), (x, by + 8)], 4, None)])
    return GP(art, trunk, "#5b3c22", seed=nx(), rough=0.3)


def paint_pomtree(art, W, H, x, by, r, rng, nx, fruits=6, blossom=False):
    trunk = strokes(W, H, [(curve([(x, by), (x - 2, by - r * 0.6), (x + 1, by - r * 1.0)], 12), 5, (0.0, 0.4)),
                           (curve([(x, by - r * 0.7), (x - r * 0.4, by - r * 1.1)], 8), 2.4, (0.0, 0.5)),
                           (curve([(x, by - r * 0.75), (x + r * 0.45, by - r * 1.15)], 8), 2.4, (0.0, 0.5))])
    art = GP(art, trunk, "#6b4526", "#3e2816", seed=nx(), rough=0.4)
    cy = by - r * 1.45
    crown = shape_mask(W, H, deform(ellipse_pts(x, cy, r, r * 0.86, 14), rng, 2, 0.06))
    art = GP(art, crown, "#4f7f3e", "#2f5a2c", seed=nx(), rough=1.2, streak=0.6)
    # leaf clusters as tiny almond strokes, light and dark
    lv = []
    for _ in range(int(r * 3.2)):
        a = rng.uniform(0, math.tau); d = math.sqrt(rng.random()) * r * 0.92
        px, py = x + math.cos(a) * d, cy + math.sin(a) * d * 0.86
        lv.append(petal_pts(px, py, rng.uniform(5, 8), 2.2, rng.uniform(0, math.tau), n=6))
    lm = shapes(W, H, lv) * crown
    art = GP(art, lm * (noise(W, H, nx(), 6) > 0.45), "#86ab5c", seed=nx(), rough=0.3, density=0.9)
    art = GP(art, lm * (noise(W, H, nx(), 6) > 0.6), "#24482a", seed=nx(), rough=0.3, density=0.8)
    for _ in range(fruits):
        a = rng.uniform(0, math.tau); d = math.sqrt(rng.random()) * r * 0.75
        fx, fy = x + math.cos(a) * d, cy + math.sin(a) * d * 0.8
        fr = rng.uniform(r * 0.09, r * 0.13)
        fm = circles(W, H, [(fx, fy, fr)])
        art = GP(art, fm, POM, POM_D, seed=nx(), rough=0.4)
        art = GP(art, shapes(W, H, [[(fx - fr * 0.35, fy - fr * 0.9), (fx, fy - fr * 1.5), (fx + fr * 0.35, fy - fr * 0.9)]], smooth=False), POM_D, seed=nx(), rough=0.2)
        art = OV(art, circles(W, H, [(fx - fr * 0.35, fy - fr * 0.35, fr * 0.28)]), lambda m: rgba(flat(*m.shape, "#f2b79a"), gaussian_filter(m, 0.8) * 0.7))
    if blossom:
        bl = circles(W, H, [(x + rng.gauss(0, r * 0.5), cy + rng.gauss(0, r * 0.4), 1.8) for _ in range(30)]) * crown
        art = GP(art, bl, "#f6e4e0", seed=nx(), rough=0.2)
    return art


def flowers(art, W, H, region, rng, nx, n, cols=("#f4efe3", "#c0392b", "#e6b84a", "#6d8fd0")):
    """Tiny gouache flowers dotted across a bed: centre dot + 4-5 petal dots."""
    ys, xs = np.where(region > 0.5)
    if len(xs) == 0:
        return art
    idx = np.random.default_rng(nx()).choice(len(xs), n)
    by_col = {c: [] for c in cols}
    for k in idx:
        x, y = xs[k], ys[k]
        c = cols[rng.randrange(len(cols))]
        r = rng.uniform(1.6, 2.6)
        for j in range(5):
            a = j * math.tau / 5 + rng.uniform(0, 1)
            by_col[c].append((x + math.cos(a) * r, y + math.sin(a) * r, r * 0.65))
    for c, items in by_col.items():
        if items:
            art = GP(art, circles(W, H, items) * region, c, seed=nx(), rough=0.2, density=0.95)
    return art


def water(art, W, H, m, nx, horizontal=True):
    art = GP(art, m, WATER, "#6f97b1", seed=nx(), rough=0.4, streak=0.8)
    ys, xs = np.where(m > 0.5)
    if len(xs) == 0:
        return art
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    items = []
    if horizontal:
        for y in np.arange(y0 + 4, y1 - 2, 6):
            for x in np.arange(x0, x1, 22):
                items.append(([(x + k, y + 1.6 * math.sin(k / 5.5 * math.pi)) for k in range(0, 22, 2)], 1.1, None))
    else:
        for x in np.arange(x0 + 4, x1 - 2, 6):
            for y in np.arange(y0, y1, 22):
                items.append(([(x + 1.6 * math.sin(k / 5.5 * math.pi), y + k) for k in range(0, 22, 2)], 1.1, None))
    art = GP(art, strokes(W, H, items) * m, SILVER, seed=nx(), rough=0.2, density=0.85)
    return art


if "garden" in PARTS:
    clear()
    W, H = 780, 960
    rng = random.Random(3); nx = Seq(30000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = rgba(flat(H, W, IVORY), np.ones((H, W), np.float32))
    M = 26  # margin for the ruled frame
    inner = shapes(W, H, [[(M, M), (W - M, M), (W - M, H - M), (M, H - M)]], smooth=False)
    horizon = 300
    # gold sky (foil) with a lapis band of cloud scrolls
    sky = inner * (yy < horizon + 10)
    skyc = painted_sky(W, H, [(0, LAPIS_D), (0.18, LAPIS), (0.32, "#3a5fb0")], seed=nx(), streak=0.8, grain=0.8)
    skyc[..., 3] = sky
    art = over(art, skyc)
    stars = circles(W, H, [(rng.uniform(M, W - M), rng.uniform(M, horizon - 60), rng.uniform(0.8, 1.6)) for _ in range(70)]) * sky
    art = FO(art, stars, "#e3c56e", seed=nx(), emboss=0.1, sparkle=0.3)
    cl = []
    for (cx, cy, s_) in [(170, 92, 1.0), (560, 76, 1.2), (330, 160, 0.75), (660, 190, 0.7), (110, 210, 0.7)]:
        pts = [(cx - 70 * s_, cy), (cx - 40 * s_, cy - 14 * s_), (cx - 10 * s_, cy - 2 * s_), (cx + 20 * s_, cy - 18 * s_), (cx + 60 * s_, cy - 4 * s_), (cx + 84 * s_, cy + 8 * s_)]
        cl.append((curve(pts, 30), 12 * s_, (0.25, 0.35)))
        cl.append((curve([(p[0], p[1] + 10 * s_) for p in pts[1:-1]], 20), 7 * s_, (0.3, 0.4)))
        cl.append((spiral_pts(cx - 70 * s_, cy + 6 * s_, 10 * s_, 1, -math.pi / 2, 0.85, 16, -1), 6 * s_, (0.0, 0.6)))
        cl.append((spiral_pts(cx + 84 * s_, cy, 9 * s_, 1, math.pi / 2, 0.85, 16, 1), 5 * s_, (0.0, 0.6)))
    clouds = strokes(W, H, cl) * sky
    art = FO(art, clouds, GOLD, seed=nx(), emboss=0.45, sparkle=0.12)
    art = GP(art, np.clip(outline_of(clouds, 1.0), 0, 1) * sky, "#7a5a1e", seed=nx(), rough=0.1, density=0.6)
    # distant rounded hills (lavender/pink rocks typical of miniatures), behind the wall
    hills = shape_mask(W, H, [(M, horizon + 20), (M, 262), (110, 236), (190, 256), (260, 226), (330, 250), (450, 232), (540, 254), (640, 228), (W - M, 250), (W - M, horizon + 20)])
    art = GP(art, hills * inner, "#c9a7b8", "#a98aa6", seed=nx(), rough=1.4, streak=0.6)
    art = GP(art, strokes(W, H, [(curve([(M, 270), (120, 248), (200, 266), (270, 240)], 20), 2, None), (curve([(470, 244), (560, 262), (650, 238), (W - M, 258)], 20), 2, None)]) * hills, "#f0dbe4", seed=nx(), rough=0.2, density=0.6)
    # garden ground (pistachio) with a slight radial lightening
    ground = inner * (yy >= horizon)
    art = GP(art, ground, PIST, PIST_D, seed=nx(), rough=0.3, streak=0.9)
    # garden wall with crenellations across the horizon
    wall = shapes(W, H, [[(M, horizon - 14), (W - M, horizon - 14), (W - M, horizon + 8), (M, horizon + 8)]], smooth=False)
    cren = shapes(W, H, [[(x, horizon - 14), (x + 8, horizon - 24), (x + 16, horizon - 14)] for x in np.arange(M, W - M - 10, 20)], smooth=False)
    wm = np.maximum(wall, cren) * inner
    art = GP(art, wm, "#d9b48a", "#c39a6e", seed=nx(), rough=0.4)
    art = GP(art, strokes(W, H, [([(M, horizon + 7), (W - M, horizon + 7)], 1.6, None)] + [([(x, horizon - 12), (x, horizon + 6)], 0.9, None) for x in np.arange(M + 10, W - M, 20)]) * inner, "#8d6a48", seed=nx(), rough=0.2, density=0.7)
    # pavilion (kiosk): iwan arch facade, tiled spandrels, small dome
    px = W / 2
    pav = shapes(W, H, [[(px - 92, horizon + 36), (px - 92, 214), (px + 92, 214), (px + 92, horizon + 36)]], smooth=False)
    dome = shape_mask(W, H, [(px - 54, 214), (px - 54, 186), (px - 40, 160), (px - 16, 144), (px, 128), (px + 16, 144), (px + 40, 160), (px + 54, 186), (px + 54, 214)])
    drum = shapes(W, H, [[(px - 60, 214), (px + 60, 214), (px + 60, 200), (px - 60, 200)]], smooth=False)
    art = GP(art, dome, "#3c8fa0", "#2a6f82", seed=nx(), rough=0.4)
    dome_p = strokes(W, H, [(curve([(px + u, 210), (px + u * 0.7, 170), (px, 130)], 12), 1.0, None) for u in (-40, -20, 0, 20, 40)]) * dome
    art = GP(art, dome_p, "#9fd0d6", seed=nx(), rough=0.2, density=0.7)
    art = FO(art, strokes(W, H, [([(px, 128), (px, 104)], 2.2, None)]) + circles(W, H, [(px, 112, 4)]), GOLD, seed=nx())
    art = GP(art, np.maximum(pav, drum), "#efe4cf", "#dcccad", seed=nx(), rough=0.4)
    iwan = shape_mask(W, H, [(px - 46, horizon + 36), (px - 46, 262), (px - 38, 240), (px - 20, 226), (px, 218), (px + 20, 226), (px + 38, 240), (px + 46, 262), (px + 46, horizon + 36)])
    art = GP(art, iwan, LAPIS, LAPIS_D, seed=nx(), rough=0.3)
    # iwan inner: gold lattice + hanging lamp shape (architecture only)
    lat = strokes(W, H, [([(px - 60 + k * 12, horizon + 40), (px + k * 12, 210)], 0.9, None) for k in range(-6, 12)] + [([(px + 60 - k * 12, horizon + 40), (px - k * 12, 210)], 0.9, None) for k in range(-6, 12)]) * iwan
    art = FO(art, lat * 0.8, GOLD, seed=nx(), emboss=0.1)
    tiles = shapes(W, H, [[(px - 88, 218), (px - 50, 218), (px - 50, horizon + 32), (px - 88, horizon + 32)], [(px + 50, 218), (px + 88, 218), (px + 88, horizon + 32), (px + 50, horizon + 32)]], smooth=False)
    tl = []
    for (x0_, x1_) in [(px - 88, px - 50), (px + 50, px + 88)]:
        for y in np.arange(222, horizon + 30, 10):
            for x in np.arange(x0_ + 4, x1_, 10):
                tl.append((x + (5 if int(y / 10) % 2 else 0), y, 2.4))
    art = GP(art, circles(W, H, tl) * tiles, "#2f7f91", seed=nx(), rough=0.2)
    art = FO(art, np.clip(outline_of(np.maximum(pav, iwan), 1.6), 0, 1) * inner, GOLD, seed=nx(), emboss=0.2)
    # four-fold garden: vertical + horizontal channels, octagonal pool at the crossing, stone kerbs
    cx, cy = W / 2, 640
    ch_w = 26
    vch = shapes(W, H, [[(cx - ch_w / 2, horizon + 40), (cx + ch_w / 2, horizon + 40), (cx + ch_w / 2, H - M), (cx - ch_w / 2, H - M)]], smooth=False)
    hch = shapes(W, H, [[(M, cy - ch_w / 2), (W - M, cy - ch_w / 2), (W - M, cy + ch_w / 2), (M, cy + ch_w / 2)]], smooth=False)
    octo = shapes(W, H, [[(cx + math.cos(a) * 82, cy + math.sin(a) * 66) for a in [math.pi / 8 + k * math.pi / 4 for k in range(8)]]], smooth=False)
    kerb = (gaussian_filter(np.maximum.reduce([vch, hch, octo]), 3.5) > 0.05).astype(np.float32) * inner
    art = GP(art, kerb, "#e9dcc2", "#cdbb98", seed=nx(), rough=0.3)
    art = water(art, W, H, vch * (1 - octo), nx, horizontal=False)
    art = water(art, W, H, hch * (1 - octo) * inner, nx, horizontal=True)
    art = water(art, W, H, octo, nx, horizontal=True)
    # fountain jet in the pool
    art = GP(art, circles(W, H, [(cx, cy, 10)]), "#f2ece0", seed=nx(), rough=0.2)
    art = GP(art, strokes(W, H, [(curve([(cx, cy - 4), (cx - 14, cy - 26), (cx - 26, cy - 8)], 10), 1.2, None), (curve([(cx, cy - 4), (cx + 14, cy - 26), (cx + 26, cy - 8)], 10), 1.2, None), ([(cx, cy - 2), (cx, cy - 34)], 1.6, None)]), SILVER, seed=nx(), rough=0.2)
    # flower beds: four parterres with ruled borders (dark green hedging) + dotted flowers
    beds = []
    for (x0_, x1_) in [(M + 14, cx - ch_w / 2 - 14), (cx + ch_w / 2 + 14, W - M - 14)]:
        for (y0_, y1_) in [(horizon + 52, cy - ch_w / 2 - 14), (cy + ch_w / 2 + 14, H - M - 14)]:
            beds.append([(x0_, y0_), (x1_, y0_), (x1_, y1_), (x0_, y1_)])
    bedm = shapes(W, H, beds, smooth=False) * (1 - (gaussian_filter(octo, 10) > 0.1))
    art = GP(art, np.clip(bedm - (gaussian_filter(bedm, 1.2) > 0.98) * 1.0, 0, 1) * 0 + bedm, "#6f9150", "#58783f", seed=nx(), rough=0.3, streak=0.8)
    hedge = np.clip((gaussian_filter(bedm, 1.4) > 0.05).astype(np.float32) - (gaussian_filter(bedm, 1.4) > 0.9), 0, 1)
    art = GP(art, hedge, CYP_D, seed=nx(), rough=0.2)
    art = FO(art, np.clip((gaussian_filter(bedm, 1) > 0.05).astype(np.float32) - (gaussian_filter(bedm, 1) > 0.6), 0, 1), GOLD, seed=nx(), emboss=0.1)
    inbed = bedm * (1 - (gaussian_filter(bedm, 3) < 0.9))
    tufts = []
    for _ in range(1400):
        x, y = rng.uniform(M, W - M), rng.uniform(horizon + 30, H - M)
        for dx in (-2.5, 0, 2.5):
            tufts.append(([(x, y), (x + dx, y - rng.uniform(4, 7))], 0.9, None))
    tm = strokes(W, H, tufts) * ground * (1 - kerb)
    art = GP(art, tm * (noise(W, H, nx(), 4) > 0.4), "#4f7438", seed=nx(), rough=0.1, density=0.75)
    art = GP(art, tm * (noise(W, H, nx(), 4) > 0.65), "#b7cc8a", seed=nx(), rough=0.1, density=0.6)
    art = flowers(art, W, H, inbed, rng, nx, 900)
    # trees: cypress rows flanking the main channel and pomegranate trees in each parterre (back to front)
    for (x, by, h_, w_) in [(cx - 64, 430, 150, 15), (cx + 64, 430, 150, 15), (cx - 64, 560, 170, 17), (cx + 64, 560, 170, 17)]:
        art = paint_cypress(art, W, H, x, by, h_, w_, rng, nx, lean=rng.uniform(-0.03, 0.03))
    for (x, by, r_) in [(150, 470, 52), (630, 470, 52), (260, 470, 40), (520, 470, 40)]:
        art = paint_pomtree(art, W, H, x, by, r_, rng, nx, fruits=7, blossom=r_ < 45)
    for (x, by, h_, w_) in [(cx - 70, 900, 210, 20), (cx + 70, 900, 210, 20)]:
        art = paint_cypress(art, W, H, x, by, h_, w_, rng, nx, lean=rng.uniform(-0.02, 0.02))
    for (x, by, r_) in [(140, 880, 70), (640, 880, 70)]:
        art = paint_pomtree(art, W, H, x, by, r_, rng, nx, fruits=9)
    # irises / tulips at the front edge
    st = []
    for x in np.arange(M + 20, W - M - 10, 34):
        if abs(x - cx) < 30:
            continue
        st.append(([(x, H - M - 4), (x + 2, H - M - 26)], 1.4, None))
    art = GP(art, strokes(W, H, st), "#3d6b39", seed=nx(), rough=0.2)
    art = GP(art, circles(W, H, [(x + 2, H - M - 30, 4.2) for x in np.arange(M + 20, W - M - 10, 34) if abs(x - cx) >= 30]), POM, seed=nx(), rough=0.2)
    # ruled frame: gold + lapis + red rulings around the painting (illuminated manuscript margins)
    rules = []
    for (d_, w_, col) in [(0, 3.4, GOLD), (5, 1.2, LAPIS), (9, 2.0, GOLD), (-6, 1.0, POM)]:
        rules.append((d_, w_, col))
    art[..., 3] = np.where(inner > 0.5, 1.0, art[..., 3])
    for d_, w_, col in rules:
        lm = poly_lines(W, H, [[(M - d_, M - d_), (W - M + d_, M - d_), (W - M + d_, H - M + d_), (M - d_, H - M + d_)]], w_)
        if col == GOLD:
            art = FO(art, lm, GOLD, seed=nx(), emboss=0.3)
        else:
            art = GP(art, lm, col, seed=nx(), rough=0.2)
    # outside the frame: transparent (page colour comes from CSS)
    outer = shapes(W, H, [[(M - 12, M - 12), (W - M + 12, M - 12), (W - M + 12, H - M + 12), (M - 12, H - M + 12)]], smooth=False)
    art[..., 3] *= np.clip(outer, 0, 1)
    art = add_grain(art, 5, 0.035)
    preview(art, "tp-garden")
    save(art, f"{OUT}/garden.webp", max_w=640, quality=80)

if "cypress" in PARTS:
    clear()
    W, H = 140, 520
    rng = random.Random(13); nx = Seq(31000)
    art = paint_cypress(blank(W, H), W, H, 70, 500, 470, 34, rng, nx, lean=0.02)
    preview(art, "tp-cypress")
    save(art, f"{OUT}/cypress.webp", max_w=90, quality=82)

if "pomegranate" in PARTS:
    clear()
    W, H = 560, 440
    rng = random.Random(23); nx = Seq(32000)
    art = blank(W, H)
    br = curve([(550, 30), (430, 90), (320, 170), (200, 260), (80, 360), (10, 420)], 50)
    tw = [curve([(320, 170), (300, 250), (300, 300)], 14), curve([(430, 90), (450, 170), (440, 210)], 14), curve([(200, 260), (170, 200), (130, 170)], 14)]
    art = GP(art, strokes(W, H, [(br, 8, (0.0, 0.6))] + [(t, 4, (0.0, 0.6)) for t in tw]), "#6b4526", "#3e2816", seed=nx(), rough=0.4, streak=0.6)
    for pts in [br] + tw:
        for k, (x, y, a) in enumerate(along(pts, 26)):
            side = 1 if k % 2 else -1
            L = rng.uniform(34, 48); aa = a + side * rng.uniform(0.7, 1.1)
            m = shape_mask(W, H, petal_pts(x, y, L, L * 0.26, aa, n=10))
            art = GP(art, m, "#4f7f3e", "#2f5a2c", seed=nx(), rough=0.6, streak=0.6)
            art = GP(art, fine(W, H, [(x + math.cos(aa) * L * t, y + math.sin(aa) * L * t) for t in (0.1, 0.5, 0.9)], 1.0) * m, "#9cc07a", seed=nx(), rough=0.1, density=0.8)
            art = FO(art, outline_of(m, 1.0) * 0.6, GOLD, seed=nx(), emboss=0.1)
    for (x, y, r, split) in [(300, 318, 46, True), (440, 228, 38, False), (128, 190, 34, False)]:
        fm = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 0.96, 14), rng, 1, 0.03))
        art = GP(art, fm, POM, POM_D, seed=nx(), rough=0.5, streak=0.5)
        art = G(art, shape_mask(W, H, ellipse_pts(x + r * 0.3, y + r * 0.3, r * 0.7, r * 0.6, 12)) * fm, POM_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
        crown = shapes(W, H, [[(x - r * 0.3, y - r * 0.86), (x - r * 0.36, y - r * 1.25), (x - r * 0.14, y - r * 1.08), (x, y - r * 1.32), (x + r * 0.14, y - r * 1.08), (x + r * 0.36, y - r * 1.25), (x + r * 0.3, y - r * 0.86)]], smooth=False)
        art = GP(art, crown, POM_D, seed=nx(), rough=0.3)
        art = OV(art, circles(W, H, [(x - r * 0.38, y - r * 0.3, r * 0.2)]) * fm, lambda m: rgba(flat(*m.shape, "#f6c2a8"), gaussian_filter(m, 2) * 0.75))
        if split:
            cut = shape_mask(W, H, [(x - r * 0.1, y - r * 0.2), (x + r * 0.55, y - r * 0.05), (x + r * 0.62, y + r * 0.45), (x + r * 0.15, y + r * 0.6), (x - r * 0.15, y + r * 0.25)])
            art = GP(art, cut, "#f3e2c4", "#e9cfa6", seed=nx(), rough=0.4)
            seeds = []
            for _ in range(60):
                sx, sy = x + r * rng.uniform(-0.1, 0.6), y + r * rng.uniform(-0.15, 0.55)
                seeds.append((sx, sy, rng.uniform(2.2, 3.4)))
            sm = circles(W, H, seeds) * cut
            art = GP(art, sm, "#d2333a", "#a01826", seed=nx(), rough=0.2)
            art = OV(art, circles(W, H, [(sx - 0.8, sy - 0.8, 0.8) for sx, sy, _ in seeds]) * cut, lambda m: rgba(flat(*m.shape, "#ffd9d3"), m * 0.9))
        art = FO(art, outline_of(fm, 1.2) * 0.8, GOLD, seed=nx(), emboss=0.15)
    for (x, y) in [(540, 36), (230, 236), (80, 356)]:
        fl = shapes(W, H, [petal_pts(x, y, 12, 6, k * math.tau / 5 - math.pi / 2, n=8) for k in range(5)])
        art = GP(art, fl, "#d8452f", "#a52a22", seed=nx(), rough=0.2)
        art = FO(art, circles(W, H, [(x, y, 3)]), GOLD, seed=nx())
    preview(art, "tp-pomegranate")
    save(art, f"{OUT}/pomegranate.webp", max_w=320, quality=82)

if "shamsa" in PARTS:
    clear()
    # illuminated shamsa (sun medallion): gold-ground roundel with lapis arabesque scrolls, scalloped edge,
    # radiating fine lapis "sun rays" — the closing emblem and monogram ground
    S = 460; c = S / 2
    rng = random.Random(33); nx = Seq(33000)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.hypot(xx - c, yy - c); aa = np.arctan2(yy - c, xx - c)
    rays = ((rr < 226) & (rr > 150) & (np.cos(aa * 48) > 0.55)).astype(np.float32) * np.clip((226 - rr) / 76, 0, 1)
    art = GP(blank(S, S), gaussian_filter(rays, 0.4), LAPIS_L, seed=nx(), rough=0.2, density=0.8)
    scal = circles(S, S, [(c + math.cos(a) * 140, c + math.sin(a) * 140, 18) for a in [k * math.tau / 24 for k in range(24)]] + [(c, c, 146)])
    art = FO(art, scal, GOLD, seed=nx(), emboss=0.45, sparkle=0.1)
    disc = circles(S, S, [(c, c, 124)])
    art = GP(art, disc, LAPIS, LAPIS_D, seed=nx(), rough=0.3)
    # gold arabesque scrolls on lapis: 4-fold split palmettes + spiral tendrils
    it = []
    for k in range(4):
        a0 = k * math.pi / 2
        sp = spiral_pts(c + math.cos(a0) * 60, c + math.sin(a0) * 60, 44, 6, a0 + math.pi, 1.1, 40, 1)
        it.append((sp, 3.0, (0.05, 0.4)))
        sp2 = spiral_pts(c + math.cos(a0 + math.pi / 4) * 78, c + math.sin(a0 + math.pi / 4) * 78, 26, 4, a0 + math.pi / 4 + math.pi, 0.9, 30, -1)
        it.append((sp2, 2.2, (0.05, 0.4)))
    pal = [petal_pts(c + math.cos(k * math.pi / 2) * 100, c + math.sin(k * math.pi / 2) * 100, 22, 9, k * math.pi / 2 + math.pi, n=10) for k in range(4)]
    pal += [petal_pts(c, c, 34, 10, k * math.pi / 4, n=10) for k in range(8)]
    orn = np.maximum(strokes(S, S, it), shapes(S, S, pal)) * disc
    art = FO(art, orn, GOLD, seed=nx(), emboss=0.4)
    art = GP(art, circles(S, S, [(c, c, 13)]), POM, seed=nx(), rough=0.2)
    art = FO(art, np.clip(np.abs(rr - 124) < 2.2, 0, 1).astype(np.float32), GOLD, seed=nx(), emboss=0.5)
    art = GP(art, circles(S, S, [(c + math.cos(a) * 140, c + math.sin(a) * 140, 4) for a in [k * math.tau / 24 for k in range(24)]]), POM, seed=nx(), rough=0.2)
    preview(art, "tp-shamsa", bg=IVORY)
    save(art, f"{OUT}/shamsa.webp", max_w=240, quality=84)

if "rule" in PARTS:
    clear()
    # illumination band: lapis cartouche (rounded-pointed ends) with gold scroll, flanked by gold ruled lines + finials
    W, H = 720, 110
    rng = random.Random(43); nx = Seq(34000)
    c = W / 2; cy = H / 2
    cart = shape_mask(W, H, [(c - 200, cy), (c - 170, cy - 30), (c + 170, cy - 30), (c + 200, cy), (c + 170, cy + 30), (c - 170, cy + 30)], smooth=False)
    art = FO(blank(W, H), (gaussian_filter(cart, 4) > 0.02).astype(np.float32), GOLD, seed=nx(), emboss=0.4)
    art = GP(art, cart, LAPIS, LAPIS_D, seed=nx(), rough=0.3)
    sc = []
    for k in range(-3, 4):
        x = c + k * 52
        sc.append((spiral_pts(x, cy, 18, 3, math.pi if k % 2 else 0, 1.0, 30, 1 if k % 2 else -1), 2.4, (0.05, 0.4)))
    leaves = [petal_pts(c + k * 52 + 18, cy + (8 if k % 2 else -8), 14, 5, (0.6 if k % 2 else -0.6), n=8) for k in range(-3, 3)]
    art = FO(art, np.maximum(strokes(W, H, sc), shapes(W, H, leaves)) * cart, GOLD, seed=nx(), emboss=0.35)
    lines = strokes(W, H, [([(20, cy - 6), (c - 212, cy - 6)], 2, None), ([(20, cy + 6), (c - 212, cy + 6)], 2, None), ([(c + 212, cy - 6), (W - 20, cy - 6)], 2, None), ([(c + 212, cy + 6), (W - 20, cy + 6)], 2, None)])
    art = FO(art, lines, GOLD, seed=nx(), emboss=0.3)
    fin = shapes(W, H, [petal_pts(18, cy, 16, 7, math.pi, n=10), petal_pts(W - 18, cy, 16, 7, 0, n=10)])
    art = GP(art, fin, POM, seed=nx(), rough=0.2)
    art = GP(art, circles(W, H, [(c - 200, cy, 4), (c + 200, cy, 4)]), POM, seed=nx(), rough=0.2)
    preview(art, "tp-rule", bg=IVORY)
    save(art, f"{OUT}/rule.webp", max_w=420, quality=84)

if "paper" in PARTS:
    # burnished (ahar-coated) manuscript paper tile, seamless
    n = 320
    rgb = flat(n, n, "#f2e7cf") * (0.96 + 0.06 * noise(n, n, 3, 22, True)[..., None] + 0.02 * noise(n, n, 4, 1.2, True)[..., None])
    fib = np.clip((noise(n, n, 5, 0.8, True) - 0.7) * 4, 0, 1) * 0.04
    rgb = rgb * (1 - fib[..., None])
    save_tex(rgba(rgb, np.ones((n, n), np.float32)), f"{OUT}/paper.webp", quality=74)

report(OUT)
