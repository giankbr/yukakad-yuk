"""Majapahit Bata — red-brick candi bentar (split gate) in the Trowulan manner, Surya Majapahit roundel (rays + star,
architecture only, no figures), lotus pond, padma moulding frieze, brick wall tile. Gouache throughout.
Run: python3 -I majapahit-bata.py [part ...]   parts: gapura surya kolam teratai frieze bata"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o3_lib import *

OUT = outdir("majapahit-bata")
PARTS = sys.argv[1:] or ["gapura", "surya", "kolam", "teratai", "frieze", "bata"]
BRICK = ["#b5543a", "#a2452f", "#c0643f", "#8f3b28", "#b04a33", "#c97a52", "#9a4a34"]
MORT = "#7a4532"
SKY = "#f1e2c8"
LOTUS, LOTUS_D, LOTUS_L = "#e0929a", "#b9566a", "#f6d3d2"
LEAF, LEAF_D, LEAF_L = "#5f7f56", "#2f4a34", "#8fa772"
WATER, WATER_D, WATER_L = "#3f6f68", "#22433f", "#7fa39a"


def half_gate(W, H, xi, flip=False):
    """Left half of a candi bentar (inner cut face at x = xi). Returns (mask, ledges[(x0,x1,y)], antefix polys, panel polys)."""
    tiers = [  # (y_top, y_bottom, x_outer)
        (628, 700, 14), (612, 628, 30), (380, 612, 48), (360, 380, 34), (300, 360, 80), (284, 300, 66),
        (232, 284, 116), (218, 232, 104), (176, 218, 152), (164, 176, 142), (128, 164, 188), (118, 128, 180),
    ]
    polys, ledges = [], []
    for (y0, y1, xo) in tiers:
        polys.append([(xo, y0), (xi, y0), (xi, y1), (xo, y1)])
        ledges.append((xo, xi, y1))
    # crowning roof: tapering stepped spire to a point near the cut face
    for (y0, y1, xo) in [(92, 118, 214), (84, 92, 206), (62, 84, 238), (56, 62, 232), (38, 56, 262), (22, 38, 286), (8, 22, 306)]:
        polys.append([(xo, y0), (xi, y0), (xi, y1), (xo, y1)]); ledges.append((xo, xi, y1))
    ante = []
    for (y0, y1, xo) in tiers:
        if y1 - y0 < 20 and 100 < y0 < 620:  # cornice: small upright antefix at the outer corner
            ante.append([(xo + 2, y0 + 2), (xo + 4, y0 - 14), (xo + 10, y0 - 26), (xo + 16, y0 - 14), (xo + 20, y0 + 2)])
    panels = [[(86, 420), (xi - 36, 420), (xi - 36, 580), (86, 580)], [(118, 306), (xi - 40, 306), (xi - 40, 350), (118, 350)]]
    pts_all = polys
    if flip:
        f = lambda P: [(W - x, y) for (x, y) in P]
        pts_all = [f(p) for p in polys]; ante = [f(p) for p in ante]; panels = [f(p) for p in panels]
        ledges = [(W - x1, W - x0, y) for (x0, x1, y) in ledges]
    m = shapes(W, H, pts_all, smooth=False)
    return m, ledges, ante, panels


if "gapura" in PARTS:
    W, H = 780, 760
    nx = Seq(30100)
    art = blank(W, H)
    XI = 322
    for side in (0, 1):
        flip = side == 1
        m, ledges, ante, panels = half_gate(W, H, XI, flip)
        am = shapes(W, H, ante)
        m = np.maximum(m, am)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        # light from upper left: left half brighter, right half a touch in shade
        light = (1.04 - 0.1 * (yy / H)) if not flip else (0.9 - 0.08 * (yy / H))
        light = light * np.ones((H, W), np.float32)
        layer = brick_paint(m, W, H, BRICK, seed=nx(), bw=30, bh=11, mort_col=MORT, light=light)
        # ledge shadows under each cornice + lit top lip
        sh = np.zeros((H, W), np.float32); lip = np.zeros((H, W), np.float32)
        for (x0, x1, y) in ledges:
            band = np.zeros((H, W), np.float32)
            band[int(y):int(y) + 16, int(x0):int(x1)] = np.linspace(1, 0, 16)[:, None][: max(0, min(16, H - int(y)))]
            sh = np.maximum(sh, band)
            lip[max(0, int(y) - 3):int(y), int(x0):int(x1)] = 1
        sh = gaussian_filter(sh, 1.5) * m
        layer = shade(layer, sh, "#2a0d06", 0.55)
        layer = lighten(layer, gaussian_filter(lip, 0.8) * m, "#f0b48a", 0.25)
        # recessed panels: dark inner rim + slightly darker field
        pm = shapes(W, H, panels, smooth=False)
        rim = np.clip(pm - np.roll(np.roll(pm, 5, 0), 5 if not flip else -5, 1), 0, 1)
        layer = shade(layer, pm * 0.6, "#3a140a", 0.25)
        layer = shade(layer, gaussian_filter(rim, 1.2), "#2a0d06", 0.6)
        # weathering: dark rain streaks + moss near the base
        streak = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (40, 1.2))
        streak = np.clip((streak - streak.mean()) / (streak.std() + 1e-6) * 0.5, 0, 1)
        layer = shade(layer, streak * m * (yy / H), "#3b1a10", 0.18)
        moss = np.clip((fbm(W, H, nx(), 26, 3) - 0.45) * 3, 0, 1) * np.clip((yy - 520) / 180, 0, 1) * m
        layer = shade(layer, moss, "#58623c", 0.55)
        # the split face: a thin sliver of the cut inner side, darker
        cut = np.zeros((H, W), np.float32)
        if flip:
            cut[:, W - XI:W - XI + 9] = 1
            cut *= np.maximum(m, np.roll(m, -9, 1))
            layer = shade(layer, cut, "#2a0d06", 0.45)
        art = over(art, layer)
        clear()
    # steps between the halves, set back
    steps = []
    for k, (y0, w0) in enumerate([(640, 90), (662, 104), (684, 118)]):
        steps.append([(W / 2 - w0, y0), (W / 2 + w0, y0), (W / 2 + w0, y0 + 22), (W / 2 - w0, y0 + 22)])
    stm = shapes(W, H, steps, smooth=False)
    layer = brick_paint(stm, W, H, BRICK[2:], seed=nx(), bw=26, bh=11, mort_col=MORT)
    edge = np.zeros((H, W), np.float32)
    for (y0, _) in [(640, 0), (662, 0), (684, 0)]:
        edge[y0:y0 + 5] = 1
    layer = lighten(layer, edge * stm, "#f2c39c", 0.3)
    art = over(layer, art) if False else over(art, layer)
    # grass tufts at the foot
    tufts = []
    rng = random.Random(7)
    for i in range(70):
        x = rng.uniform(0, W); y = rng.uniform(696, 712)
        for j in range(3):
            a = -math.pi / 2 + rng.uniform(-0.6, 0.6)
            L = rng.uniform(10, 26)
            tufts.append(([(x, y), (x + math.cos(a) * L * .5, y + math.sin(a) * L * .5 + 1), (x + math.cos(a) * L, y + math.sin(a) * L)], 2.6, (0.0, 0.8)))
    tm = strokes(W, H, tufts)
    art = GP(art, tm, LEAF, LEAF_D, seed=nx(), rough=0.8, streak=0.6)
    preview(art, "mb-gapura", tone=SKY)
    save(art, f"{OUT}/gapura.webp", max_w=720, quality=80)
    clear()

if "surya" in PARTS:
    W = H = 520
    c = W / 2
    nx = Seq(30200)
    def wedge(a, r0, r1, wd):
        return [(c + math.cos(a - wd) * r0, c + math.sin(a - wd) * r0), (c + math.cos(a - wd * .35) * (r0 + (r1 - r0) * .7), c + math.sin(a - wd * .35) * (r0 + (r1 - r0) * .7)),
                (c + math.cos(a) * r1, c + math.sin(a) * r1), (c + math.cos(a + wd * .35) * (r0 + (r1 - r0) * .7), c + math.sin(a + wd * .35) * (r0 + (r1 - r0) * .7)),
                (c + math.cos(a + wd) * r0, c + math.sin(a + wd) * r0)]
    big = [wedge(k * math.tau / 8 - math.pi / 2, 130, 252, 0.2) for k in range(8)]
    mid = [wedge(k * math.tau / 8 - math.pi / 2 + math.pi / 8, 130, 214, 0.16) for k in range(8)]
    sm = [wedge(k * math.tau / 16 - math.pi / 2 + math.pi / 16, 130, 176, 0.08) for k in range(16)]
    rb, rm, rs = shapes(W, H, big, smooth=False), shapes(W, H, mid, smooth=False), shapes(W, H, sm, smooth=False)
    ridge = strokes(W, H, [([(c + math.cos(k * math.tau / 8 - math.pi / 2) * 134, c + math.sin(k * math.tau / 8 - math.pi / 2) * 134),
                             (c + math.cos(k * math.tau / 8 - math.pi / 2) * 236, c + math.sin(k * math.tau / 8 - math.pi / 2) * 236)], 3.2, (0.0, 0.6)) for k in range(8)])
    disc = circles(W, H, [(c, c, 136)])
    ring1 = np.clip(circles(W, H, [(c, c, 136)]) - circles(W, H, [(c, c, 124)]), 0, 1)
    ring2 = np.clip(circles(W, H, [(c, c, 106)]) - circles(W, H, [(c, c, 100)]), 0, 1)
    beads = circles(W, H, [(c + math.cos(k * math.tau / 32) * 114, c + math.sin(k * math.tau / 32) * 114, 4.0) for k in range(32)])
    sq1 = [(c + math.cos(a) * 86, c + math.sin(a) * 86) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
    sq2 = [(c + math.cos(a) * 86, c + math.sin(a) * 86) for a in [k * math.pi / 2 for k in range(4)]]
    star = shapes(W, H, [sq1, sq2], smooth=False)
    petals = shapes(W, H, [petal_pts(c, c, 50, 16, k * math.tau / 8 + math.pi / 8, n=12) for k in range(8)])
    boss = circles(W, H, [(c, c, 15)])
    rays = np.maximum.reduce([rb, rm, rs])
    height = (gaussian_filter(rb, 5) * 0.9 + gaussian_filter(rm, 4) * 0.7 + gaussian_filter(rs, 3) * 0.5 + ridge * 0.3)
    height = np.maximum(height * rays, disc * 0.45)
    height = np.maximum.reduce([height, ring1 * 0.85, ring2 * 0.7, beads * 0.8, gaussian_filter(star, 2.5) * 0.75, gaussian_filter(petals, 2) * 0.95, boss])
    full = np.clip(np.maximum(rays, disc), 0, 1)
    base = gouache_paint(full, "#b9773d", "#a45f30", seed=nx(), rough=1.4, streak=0.8)
    L = emboss(height, 1.4)
    rgb = base[..., :3] * (0.55 + 0.9 * L[..., None])
    rgb = rgb * (1 - 0.3 * np.clip(0.55 - height, 0, 1)[..., None])
    art = rgba(rgb, base[..., 3])
    art = shade(art, np.clip((fbm(W, H, nx(), 20, 3) - 0.5) * 2, 0, 1) * full, "#6a2e18", 0.25)
    art = lighten(art, np.clip((fbm(W, H, nx(), 9, 2) - 0.7) * 3, 0, 1) * full, "#f1d2a6", 0.25)
    preview(art, "mb-surya", tone=SKY)
    save(art, f"{OUT}/surya.webp", max_w=420, quality=82)
    clear()


def lotus_flower(art, W, H, x, y, s, rng, nx, open_=1.0):
    """Side-view lotus: back petals, front petals, pointed tips, pink gouache with deeper tips."""
    back, front = [], []
    for k, a in enumerate(np.linspace(-2.5, -0.64, 5)):
        back.append(petal_pts(x, y, s * 1.05, s * 0.32, a, n=14))
    for k, a in enumerate(np.linspace(-2.2, -0.94, 4)):
        front.append(petal_pts(x, y + s * 0.08, s * 0.95, s * 0.34, a, n=14))
    bm = shapes(W, H, back); fm = shapes(W, H, front)
    art = GP(art, bm, LOTUS_D, LOTUS, seed=nx(), rough=1.0, streak=0.6)
    lay = gouache_paint(fm, LOTUS_L, LOTUS, seed=nx(), rough=1.0, streak=0.8)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    tip = np.clip((y - s * 0.3 - yy) / (s * 0.6), 0, 1)
    lay = shade(lay, tip * fm, "#a8355a", 0.45)
    rim = np.clip(fm - gaussian_filter(fm, 1.5), 0, 1) * 3
    lay = shade(lay, rim, "#8a2e48", 0.5)
    art = over(art, lay)
    return art


def lotus_leaf(art, W, H, x, y, rx, ry, rng, nx):
    pts = deform(ellipse_pts(x, y, rx, ry, 18), rng, 2, 0.04)
    m = shape_mask(W, H, pts)
    notch = shape_mask(W, H, [(x, y), (x + rx * 1.1, y - ry * 0.18), (x + rx * 1.1, y + ry * 0.12)], smooth=False)
    m = np.clip(m - notch, 0, 1)
    lay = gouache_paint(m, LEAF, LEAF_D, seed=nx(), rough=1.4, streak=0.9)
    vein = strokes(W, H, [([(x, y), (x + math.cos(a) * rx * .9, y + math.sin(a) * ry * .9)], 1.6, (0.0, 0.6)) for a in np.linspace(0.3, math.tau - 0.3, 11)])
    lay = lighten(lay, vein * m, LEAF_L, 0.5)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    lay = lighten(lay, np.clip((y - yy) / ry, 0, 1) * m, LEAF_L, 0.3)
    art = over(art, soft_shadow(m, "#0d201d", blur=3, strength=0.45, dx=2, dy=4))
    return over(art, lay)


if "kolam" in PARTS:
    W, H = 800, 300
    nx = Seq(30300)
    rng = random.Random(33)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # brick pond rim on top, water below
    rim = np.zeros((H, W), np.float32); rim[40:66] = 1
    art = brick_paint(rim, W, H, BRICK, seed=nx(), bw=34, bh=12, mort_col=MORT)
    art = shade(art, np.clip((yy - 54) / 12, 0, 1) * rim, "#2a0d06", 0.4)
    water = np.zeros((H, W), np.float32); water[64:] = 1
    wl = gouache_paint(water, WATER, WATER_D, seed=nx(), rough=0.5, streak=1.0)
    wl = shade(wl, np.clip((yy - 64) / 220, 0, 1), "#16302d", 0.5)
    ripples = []
    for i in range(46):
        y = rng.uniform(80, 292); x = rng.uniform(-40, W); L = rng.uniform(40, 140)
        ripples.append(([(x, y), (x + L * .5, y + rng.uniform(-1.5, 1.5)), (x + L, y)], rng.uniform(1.4, 3.2), (0.3, 0.3)))
    wl = lighten(wl, strokes(W, H, ripples) * water, WATER_L, 0.45)
    # reflection of the brick rim
    refl = np.zeros((H, W), np.float32); refl[66:90] = np.linspace(0.5, 0, 24)[:, None]
    wl = shade(wl, refl * (0.6 + 0.4 * fbm(W, H, nx(), 8, 2)), "#7a2a18", 0.6)
    art = over(art, wl)
    clear()
    for (x, y, rx, ry) in [(80, 210, 70, 22), (230, 262, 84, 24), (420, 214, 60, 18), (560, 252, 92, 26), (720, 206, 66, 20), (330, 150, 44, 13), (650, 140, 40, 12), (40, 150, 40, 11)]:
        art = lotus_leaf(art, W, H, x, y, rx, ry, rng, nx)
        clear()
    stems = strokes(W, H, [(curve([(150, 236), (152, 180), (160, 140)], 16), 4, None), (curve([(480, 236), (476, 170), (470, 124)], 16), 4, None),
                           (curve([(640, 230), (648, 190), (660, 168)], 14), 3.5, None), (curve([(296, 250), (300, 210), (306, 188)], 14), 3, None)])
    art = GP(art, stems, LEAF_D, seed=nx(), rough=0.6)
    art = lotus_flower(art, W, H, 160, 140, 50, rng, nx)
    art = lotus_flower(art, W, H, 470, 124, 60, rng, nx)
    clear()
    # buds
    for (x, y, s_, a) in [(660, 168, 22, -1.7), (306, 188, 18, -1.45)]:
        m = shapes(W, H, [petal_pts(x, y, s_ * 1.8, s_ * 0.55, a, n=14)])
        lay = gouache_paint(m, LOTUS, LOTUS_D, seed=nx(), rough=0.8)
        art = over(art, lay)
    preview(art, "mb-kolam", tone=SKY)
    save(art, f"{OUT}/kolam.webp", max_w=800, quality=78)
    clear()

if "teratai" in PARTS:
    W, H = 300, 220
    nx = Seq(30400); rng = random.Random(44)
    art = blank(W, H)
    art = lotus_leaf(art, W, H, 150, 182, 120, 24, rng, nx)
    art = lotus_flower(art, W, H, 150, 168, 92, rng, nx)
    preview(art, "mb-teratai", tone=SKY)
    save(art, f"{OUT}/teratai.webp", max_w=160, quality=84)
    clear()

if "frieze" in PARTS:
    # padma moulding: a brick band with a row of carved lotus-petal (padma) relief
    W, H = 760, 84
    nx = Seq(30500)
    band = np.zeros((H, W), np.float32); band[8:76, 6:W - 6] = 1
    art = brick_paint(band, W, H, BRICK, seed=nx(), bw=28, bh=11, mort_col=MORT, mortar=1.0)
    pet = shapes(W, H, [deform(ellipse_pts(x, 50, 14, 22, 16), random.Random(x), 1, 0.02) for x in range(24, W - 10, 32)])
    pet = np.maximum(pet, shapes(W, H, [petal_pts(x, 26, 14, 6, -math.pi / 2, n=10) for x in range(24, W - 10, 32)])) * band
    L = emboss(gaussian_filter(pet, 3.5) * 1.4, 1.2)
    lay = art.copy()
    lay[..., :3] = art[..., :3] * (0.55 + 0.9 * L[..., None])
    art = rgba(art[..., :3] * (1 - pet[..., None]) + lay[..., :3] * pet[..., None], art[..., 3])
    rims = np.zeros((H, W), np.float32); rims[8:16] = 1; rims[70:76] = 1
    art = lighten(art, rims * band * 0.5, "#f0b48a", 0.4)
    art = shade(art, np.clip(np.roll(rims, 6, 0) - rims, 0, 1) * band, "#2a0d06", 0.4)
    preview(art, "mb-frieze", tone=SKY)
    save(art, f"{OUT}/frieze.webp", max_w=380, quality=84)
    clear()

if "bata" in PARTS:
    n = 256
    hid, mort, bev, row = brick_field(n, n, 64, 16, seed=5, wob=0, mortar=1.4, wrap=True)
    pal = np.stack([hexarr(c) for c in ["#5e2116", "#6b2a1b", "#55201a", "#743324", "#4e1b12"]])
    k = np.clip(hid * 4, 0, 3.999); i0 = np.floor(k).astype(int); t = (k - i0)[..., None]
    rgb = pal[i0] * (1 - t) + pal[np.minimum(i0 + 1, 4)] * t
    rgb *= (0.88 + 0.22 * wrap_noise(n, n, 7, 2.2))[..., None]
    rgb *= (0.93 + 0.12 * wrap_noise(n, n, 8, 18))[..., None]
    rgb = rgb * (1 - mort[..., None] * 0.6) + hexarr("#2e100a") * mort[..., None] * 0.6
    rgb *= (1 + 0.05 * (bev[..., None] - .5))
    save_full(rgba(rgb, np.ones((n, n), np.float32)), f"{OUT}/bata.webp", quality=72)
