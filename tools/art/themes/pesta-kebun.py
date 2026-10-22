"""Pesta Kebun — an adult birthday garden party at dusk in watercolour + gouache: a painted dusk sky with a far tree
line, a long linen-dressed table receding under the trees with wildflower jars and hurricane candles, string lights
with warm bulbs, a tree hung with glowing paper lanterns, a wildflower jar bouquet and a small sprig.
Run: python3 -I pesta-kebun.py [part ...]   parts: sky lights tree table bouquet sprig
Assets -> public/themes/art/pesta-kebun/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f5_lib import *  # noqa

OUT = outdir("pesta-kebun")
PARTS = sys.argv[1:] or ["sky", "lights", "tree", "table", "bouquet", "sprig"]
DUSK = "#3d3a5e"
FOL, FOL2, FOLD = "#2f4a46", "#3f5c50", "#1c2c2c"
LINEN, LINEN2, LINEND = "#f6efe4", "#efe4d2", "#b9a48c"
FLOWERS = [("#e8735a", "#f08a6c"), ("#f4c95d", "#f7d77e"), ("#9b8ac4", "#b2a3d6"), ("#fbf6ee", "#f3ece0"), ("#f2a7a0", "#f6bdb4")]


def flower_head(art, W, H, x, y, r, cols, nx, rng, kind="daisy"):
    c, c2 = cols
    if kind == "daisy":
        polys = [petal_pts(x, y, r, r * 0.32, a + rng.uniform(-.1, .1), 10) for a in np.linspace(0, math.tau, rng.randint(8, 11), endpoint=False)]
        m = shapes(W, H, polys)
        art = G(art, m, c, c2, seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=0.8, feather=0.5)
        ctr = circles(W, H, [(x, y, r * 0.3)])
        art = GP(art, ctr, "#e0a43a" if c != "#f4c95d" else "#a8642a", seed=nx(), rough=0.4)
    elif kind == "cosmos":
        polys = [deform(petal_pts(x, y, r, r * 0.55, a, 12), rng, 1, 0.02) for a in np.linspace(0, math.tau, 8, endpoint=False)]
        m = shapes(W, H, polys)
        art = G(art, m, c, c2, seed=nx(), density=0.85, edge=0.7, bloom=0.3, rough=1.0, feather=0.6)
        art = GP(art, circles(W, H, [(x, y, r * 0.22)]), "#e2b23e", seed=nx(), rough=0.4)
    elif kind == "spike":
        items = [(x + rng.uniform(-2, 2), y + k * r * 0.35, r * 0.28) for k in range(7)]
        m = circles(W, H, items)
        art = G(art, m, c, c2, seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=0.8, feather=0.5)
    else:  # button
        m = circles(W, H, [(x, y, r * 0.5)])
        art = GP(art, m, c, c2, seed=nx(), rough=0.6)
        art = tint(art, side_light(m, 2, 2, 2), mix(c, "#6a3a1a", 0.4), 0.5, seed=nx())
    return art


def bunch(art, W, H, cx, base_y, spread, height, nx, rng, n=14, scale=1.0, stems=True):
    """Loose wildflower bunch rising from (cx, base_y)."""
    heads = []
    for i in range(n):
        a = rng.uniform(-spread, spread)
        L = height * rng.uniform(0.6, 1.0)
        tx = cx + math.sin(a) * L
        ty = base_y - math.cos(a) * L
        heads.append((tx, ty, a))
    if stems:
        st = strokes(W, H, [(curve([(cx + rng.uniform(-4, 4), base_y), ((cx + tx) / 2 + rng.uniform(-6, 6), (base_y + ty) / 2), (tx, ty)], 16), 2.2 * scale, (0.0, 0.2)) for tx, ty, a in heads])
        art = G(art, st, "#5f7a4a", "#7a8f52", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.5, feather=0.4)
        lv = shapes(W, H, [petal_pts(cx + rng.uniform(-spread, spread) * height * 0.5, base_y - rng.uniform(0.2, 0.6) * height, 18 * scale, 4 * scale, rng.uniform(-2.6, -0.5), 10) for _ in range(n // 2)])
        art = G(art, lv, "#6d8a54", "#88a066", seed=nx(), density=0.8, edge=0.5, bloom=0.1, rough=0.6, feather=0.4)
        grass = strokes(W, H, [(curve([(cx, base_y), (cx + math.sin(a) * height * 0.6, base_y - height * 0.7), (cx + math.sin(a) * height * 1.0 + rng.uniform(-10, 10), base_y - height * rng.uniform(0.9, 1.15))], 16), 1.4 * scale, (0.0, 0.6)) for a in (rng.uniform(-spread, spread) for _ in range(5))])
        art = G(art, grass, "#a3a25a", "#c2b86e", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.4, feather=0.3)
    kinds = ["daisy", "cosmos", "spike", "button", "cosmos", "daisy"]
    for i, (tx, ty, a) in enumerate(heads):
        kind = kinds[i % len(kinds)]
        cols = FLOWERS[rng.randrange(len(FLOWERS))] if kind != "spike" else FLOWERS[2]
        if kind == "daisy" and cols[0] == "#9b8ac4":
            cols = FLOWERS[3]
        art = flower_head(art, W, H, tx, ty, rng.uniform(9, 14) * scale, cols, nx, rng, kind)
    return art


def lantern(art, W, H, x, y, r, col, nx, glow_amt=1.0):
    """Round paper lantern hanging at (x, y top): warm glow, ribbed paper, dark cap."""
    art = OV(art, circles(W, H, [(x, y + r, r * 1.2)]), lambda mm: col_arr(mm, "#ffcf7a", np.clip(gaussian_filter(mm, r * 0.9), 0, 1) * 0.55 * glow_amt), pad=int(r * 3))
    body = ellipses(W, H, [(x, y + r, r, r * 0.92, 0)])
    art = GP(art, body, col, mix(col, "#fff2c8", 0.4), seed=nx(), rough=0.6, streak=0.3)
    art = tint(art, side_light(body, r * 0.25, r * 0.15, r * 0.4), mix(col, "#8a3a1a", 0.5), 0.5, seed=nx())
    art = tint(art, gaussian_filter(circles(W, H, [(x - r * 0.15, y + r * 0.9, r * 0.45)]), r * 0.3) * body, "#fff6d8", 0.7, seed=nx())
    rib_items = [([(x + r * 0.98 * math.sin(a) * math.cos(t), y + r - r * 0.9 * math.cos(t)) for t in np.linspace(-1.35, 1.35, 14)], 1.1, None) for a in (-1.0, -0.5, 0.0, 0.5, 1.0)]
    art = crayon(art, strokes(W, H, rib_items) * body, mix(col, "#7a3a1a", 0.35), seed=nx(), amt=0.35)
    caps = shapes(W, H, [[(x - r * 0.35, y + 2), (x + r * 0.35, y + 2), (x + r * 0.3, y + r * 0.16), (x - r * 0.3, y + r * 0.16)], [(x - r * 0.3, y + r * 1.84), (x + r * 0.3, y + r * 1.84), (x + r * 0.35, y + r * 1.98), (x - r * 0.35, y + r * 1.98)]], smooth=False)
    art = GP(art, caps, "#2a2226", seed=nx(), rough=0.3)
    return art


if "sky" in PARTS:
    W, H = 780, 1180
    nx = Seq(60100); rng = random.Random(601)
    art = painted_sky(W, H, [(0, "#3b3a64"), (0.32, "#6f5f8e"), (0.55, "#c48aa0"), (0.72, "#f2b08a"), (0.86, "#f8d29a"), (1, "#f2c48c")], seed=nx(), streak=0.9)
    # soft wash clouds
    for i in range(7):
        x = rng.uniform(0, W); y = rng.uniform(H * 0.25, H * 0.65)
        m = ellipses(W, H, [(x, y, rng.uniform(120, 240), rng.uniform(16, 30), rng.uniform(-4, 4))])
        art = G(art, m, "#f4b6a0", "#d993a6", seed=nx(), density=0.35, edge=0.3, bloom=0.3, rough=6, feather=6)
        clear()
    # first stars
    for i in range(10):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, H * 0.28)
        art = OV(art, circles(W, H, [(x, y, rng.uniform(1.2, 2.2))]), lambda mm: col_arr(mm, "#fff6dc", np.clip(gaussian_filter(mm, 0.8) * 1.5, 0, 1) * 0.8), pad=6)
    # far tree line: rounded canopies (mauve-blue), nearer darker row
    for row, (base, rr, c, c2, dens) in enumerate(((H - 150, (40, 80), "#5d5577", "#6e6284", 0.85), (H - 70, (34, 64), "#3f4a5a", "#47506a", 0.95))):
        items = [(x, base - rng.uniform(0, 50), rng.uniform(*rr)) for x in np.arange(-30, W + 40, rng.uniform(40, 60))]
        tl = np.clip(circles(W, H, items) + shapes(W, H, [[(-10, base), (W + 10, base), (W + 10, H + 10), (-10, H + 10)]], smooth=False), 0, 1)
        art = G(art, tl, c, c2, seed=nx(), density=dens, edge=0.5, bloom=0.3, rough=6, feather=2)
        clear()
    art = add_grain(art, nx(), 0.025)
    preview(art, "pk-sky", tone="#f6efe4")
    save_rgb(art, f"{OUT}/sky.webp", size=(520, 787), quality=74)
    clear()

if "lights" in PARTS:
    W, H = 840, 200
    nx = Seq(60200); rng = random.Random(602)
    art = blank(W, H)
    swags = [catenary(-10, 20, 420, 26, 90), catenary(420, 26, 850, 18, 96)]
    wire = strokes(W, H, [(sw, 2.4, None) for sw in swags])
    art = G(art, wire, "#2a2426", seed=nx(), density=0.95, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    bulbs = []
    for sw in swags:
        for i in range(2, len(sw) - 1, 5):
            bulbs.append(sw[i])
    for (x, y) in bulbs:
        y2 = y + 6
        hm = circles(W, H, [(x, y2 + 16, 10)])
        art = OV(art, hm, lambda mm: col_arr(mm, "#ffc86a", np.clip(gaussian_filter(mm, 16), 0, 1) * 0.75), pad=50)
        art = GP(art, shapes(W, H, [[(x - 4, y), (x + 4, y), (x + 4, y2 + 3), (x - 4, y2 + 3)]], smooth=False), "#3a3236", seed=nx(), rough=0.2)
        bm = ellipses(W, H, [(x, y2 + 15, 8, 12, 0)])
        art = OV(art, bm, lambda mm: col_arr(mm, "#ffe3a0", np.clip(gaussian_filter(mm, 0.8), 0, 1) * 0.95), pad=6)
        art = OV(art, circles(W, H, [(x, y2 + 15, 4)]), lambda mm: col_arr(mm, "#fffaf0", np.clip(gaussian_filter(mm, 1.5), 0, 1)), pad=6)
    art = edge_fade(art, 2)
    preview(art, "pk-lights", bg=DUSK)
    save_full(art, f"{OUT}/lights.webp", size=(420, 100), quality=82)
    clear()

if "tree" in PARTS:
    W, H = 560, 860
    nx = Seq(60300); rng = random.Random(603)
    art = blank(W, H)
    # trunk + limbs reaching right
    trunk = strokes(W, H, [(curve([(90, H + 10), (100, 640), (88, 480), (110, 330)], 40), 46, (0.0, 0.3)),
                           (curve([(100, 520), (200, 470), (330, 450), (470, 470)], 40), 20, (0.0, 0.5)),
                           (curve([(104, 400), (180, 320), (290, 290)], 30), 16, (0.0, 0.5)),
                           (curve([(96, 620), (40, 560), (0, 540)], 20), 18, (0.0, 0.5))])
    art = G(art, trunk, "#2c2a30", "#3b3540", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
    # canopy: clustered watercolour blobs, darker inside, lighter rim catching the dusk
    blobs = []
    for i in range(34):
        x = rng.uniform(-40, 520); y = rng.uniform(40, 420) + (x / 520) * 60
        blobs.append(deform(ellipse_pts(x, y, rng.uniform(50, 100), rng.uniform(40, 70), 10, rng.uniform(0, 3)), rng, 2, 0.06))
    can = shapes(W, H, blobs)
    art = G(art, can, FOL, FOL2, seed=nx(), density=0.95, edge=0.6, bloom=0.4, rough=5, feather=1.2, gran=0.35)
    art = G(art, can * side_light(can, -20, 30, 24), FOLD, seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=3, feather=3)
    art = G(art, can * side_light(can, 16, 20, 14), "#8a7a8a", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=3, feather=3)
    leaves = []
    for i in range(140):
        x = rng.uniform(-30, 540); y = rng.uniform(20, 470)
        if can[int(np.clip(y, 0, H - 1)), int(np.clip(x, 0, W - 1))] < 0.5 and rng.random() < 0.7:
            continue
        leaves.append(petal_pts(x, y, rng.uniform(10, 18), rng.uniform(4, 6), rng.uniform(0, math.tau), 8))
    art = G(art, shapes(W, H, leaves), "#45625a", "#58705e", seed=nx(), density=0.8, edge=0.6, bloom=0.1, rough=1, feather=0.5)
    clear()
    # hanging lanterns
    for x, y, r, col, L in ((180, 430, 26, "#f6c35e", 60), (320, 452, 22, "#f09a6a", 46), (440, 470, 28, "#f8d27a", 70), (250, 300, 18, "#f6b0a0", 40), (60, 420, 20, "#f8d27a", 50)):
        art = G(art, strokes(W, H, [([(x, y - 40), (x, y + L - 30)], 1.6, None)]), "#2a2426", seed=nx(), density=0.9, edge=0.1, bloom=0, rough=0.3, feather=0.3)
        art = lantern(art, W, H, x, y + L - 30, r, col, nx)
        clear()
    preview(art, "pk-tree", bg=DUSK)
    save(art, f"{OUT}/tree.webp", max_w=280, quality=80)
    clear()

if "table" in PARTS:
    W, H = 840, 380
    nx = Seq(60400); rng = random.Random(604)
    art = blank(W, H)
    top_y, hem_y = 220, 360
    # chair backs peeking behind the table (cross-back wooden bistro chairs)
    chairs = []
    for x in np.arange(40, W, 120):
        x += rng.uniform(-8, 8)
        chairs += [([(x - 28, top_y + 4), (x - 30, top_y - 92)], 7, None), ([(x + 28, top_y + 4), (x + 30, top_y - 92)], 7, None),
                   (curve([(x - 30, top_y - 92), (x, top_y - 100), (x + 30, top_y - 92)], 10), 8, None),
                   ([(x - 26, top_y - 70), (x + 26, top_y - 16)], 4, None), ([(x + 26, top_y - 70), (x - 26, top_y - 16)], 4, None)]
    cm = strokes(W, H, chairs)
    art = G(art, cm, "#6b4a3a", "#7d5a44", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.6, feather=0.4)
    art = G(art, cm * side_light(cm, 2, 0, 2), "#3a2620", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, feather=0.4)
    # cloth: slight scalloped hem, soft vertical folds, warm light from the candles on top
    hem = [(x, hem_y + 8 * math.sin(x / 70 * math.pi) ** 2 + rng.uniform(-2, 2)) for x in np.linspace(-10, W + 10, 60)]
    cloth = [(-10, top_y), (W + 10, top_y)] + hem[::-1]
    clm = shapes(W, H, [cloth], smooth=False)
    art = G(art, clm, LINEN, LINEN2, seed=nx(), density=0.96, edge=0.3, bloom=0.15, rough=1.2, feather=0.6, mottle=0.25)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    folds = 0.5 + 0.5 * np.sin(xx / 70 * math.pi * 2 + (fbm(W, H, nx(), 60, 2) - 0.5) * 2)
    art = tint(art, clm * np.clip((0.35 - folds) * 2, 0, 1) * np.clip((yy - top_y) / 60, 0, 1), "#b9a0a8", 0.5, seed=nx())
    art = tint(art, clm * np.clip((yy - top_y - 40) / 120, 0, 1), "#9a86a0", 0.45, seed=nx())
    art = tint(art, clm * np.exp(-((yy - top_y) / 14) ** 2), "#fff6e2", 0.6, seed=nx())
    # greenery runner draping over the front edge
    lv = []
    for i in range(160):
        x = rng.uniform(0, W); y = top_y + rng.uniform(-8, 6) + (14 * math.sin(x / 50) ** 2 if rng.random() < 0.3 else 0)
        lv.append(petal_pts(x, y, rng.uniform(10, 17), rng.uniform(3.5, 5.5), rng.uniform(-math.pi, 0.4), 8))
    art = G(art, shapes(W, H, lv), "#5d7a52", "#7f9668", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=0.6, feather=0.4)
    clear()
    # objects on the table, left to right
    def jar_bunch(art, x, s):
        art = bunch(art, W, H, x, top_y - 30 * s, 0.7, 120 * s, nx, rng, n=int(16 * s) + 4, scale=s)
        jar = shapes(W, H, [[(x - 20 * s, top_y - 44 * s), (x + 20 * s, top_y - 44 * s), (x + 22 * s, top_y - 6), (x - 22 * s, top_y - 6)]])
        art = G(art, jar, "#cfe0d8", seed=nx(), density=0.22, edge=0.5, bloom=0, rough=0.5, feather=0.4)
        return glass_glints(art, jar, nx, col="#ffffff", amt=1.3)

    def hurricane(art, x, s):
        art = candle_flame(art, W, H, x, top_y - 50 * s, 26 * s, 6 * s, nx, halo=1.0)
        pil = shapes(W, H, [[(x - 10 * s, top_y - 48 * s), (x + 10 * s, top_y - 48 * s), (x + 10 * s, top_y - 4), (x - 10 * s, top_y - 4)]], smooth=False)
        art = GP(art, pil, "#fbf1dc", "#f2e2c4", seed=nx(), rough=0.3)
        art = tint(art, side_light(pil, 4, 0, 3), "#b08a6a", 0.5, seed=nx())
        hur = shapes(W, H, [[(x - 22 * s, top_y - 96 * s), (x + 22 * s, top_y - 96 * s), (x + 28 * s, top_y - 40 * s), (x + 20 * s, top_y - 4), (x - 20 * s, top_y - 4), (x - 28 * s, top_y - 40 * s)]])
        return glass_glints(art, hur, nx, col="#fff1d0", amt=1.2)

    def wine(art, x, s):
        bowl = shapes(W, H, [[(x - 11 * s, top_y - 70 * s), (x + 11 * s, top_y - 70 * s), (x + 12 * s, top_y - 52 * s), (x, top_y - 40 * s), (x - 12 * s, top_y - 52 * s)]])
        art = G(art, bowl * (yy > top_y - 58 * s), "#8e2236", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.3, feather=0.3)
        st = np.clip(strokes(W, H, [([(x, top_y - 40 * s), (x, top_y - 4)], 2.2, None)]) + ellipses(W, H, [(x, top_y - 4, 10 * s, 2.5, 0)]), 0, 1)
        return glass_glints(art, np.clip(bowl + st, 0, 1), nx, amt=1.3)

    def cake(art, x):
        stand = np.clip(ellipses(W, H, [(x, top_y - 40, 70, 7, 0)]) + shapes(W, H, [[(x - 8, top_y - 40), (x + 8, top_y - 40), (x + 14, top_y - 4), (x - 14, top_y - 4)]], smooth=False), 0, 1)
        art = G(art, stand, "#f4efe8", "#e6ddd2", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.4, feather=0.4)
        art = G(art, stand * side_light(stand, 3, 2, 3), "#9a8a94", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.4)
        for (w2, y0, y1) in ((56, top_y - 98, top_y - 44), (40, top_y - 140, top_y - 98)):
            tier = shapes(W, H, [[(x - w2, y1), (x + w2, y1), (x + w2, y0), (x - w2, y0)]], smooth=False)
            art = GP(art, tier, "#e9d2b4", "#e2c39c", seed=nx(), rough=0.6, streak=0.6)
            # semi-naked cake: cream scraped over sponge
            cream = tier * np.clip(fbm(W, H, nx(), 14, 3) * 1.6 - 0.25, 0, 1)
            art = tint(art, cream, "#fbf5ea", 0.85, seed=nx())
            art = tint(art, side_light(tier, 6, 0, 8), "#a88a72", 0.45, seed=nx())
            art = tint(art, np.exp(-((yy - y0) / 4) ** 2) * tier, "#fffaf0", 0.8, seed=nx())
        # flowers on the cake + slim candles with flames
        art = bunch(art, W, H, x + 26, top_y - 138, 0.9, 26, nx, rng, n=5, scale=0.7, stems=False)
        art = bunch(art, W, H, x - 46, top_y - 96, 0.9, 20, nx, rng, n=4, scale=0.6, stems=False)
        for cx in (x - 18, x - 4, x + 10):
            cm2 = shapes(W, H, [[(cx - 2.5, top_y - 166), (cx + 2.5, top_y - 166), (cx + 2.5, top_y - 140), (cx - 2.5, top_y - 140)]], smooth=False)
            art = GP(art, cm2, "#f6dfa0", seed=nx(), rough=0.2)
            art = candle_flame(art, W, H, cx, top_y - 166, 14, 3.4, nx, halo=0.7)
        return art

    plan = [(40, "jar", 0.9), (108, "hur", 0.9), (160, "wine", 1.0), (236, "jar", 1.0), (318, "hur", 1.0), (420, "cake", 1), (520, "hur", 1.0), (586, "wine", 1.0), (650, "jar", 1.05), (734, "hur", 0.9), (800, "jar", 0.85)]
    for x, kind, s_ in plan:
        art = {"jar": jar_bunch, "hur": hurricane, "wine": wine}[kind](art, x, s_) if kind != "cake" else cake(art, x)
        clear()
    preview(art, "pk-table", bg="#4a4466")
    save(art, f"{OUT}/table.webp", max_w=420, quality=80)
    clear()

if "bouquet" in PARTS:
    W, H = 360, 460
    nx = Seq(60500); rng = random.Random(605)
    art = blank(W, H)
    art = bunch(art, W, H, 180, 320, 0.62, 190, nx, rng, n=34, scale=1.0)
    jar = shapes(W, H, [[(128, 300), (232, 300), (240, 330), (236, 430), (124, 430), (120, 330)]])
    art = G(art, jar, "#d6e4dc", "#c8d8d0", seed=nx(), density=0.25, edge=0.6, bloom=0, rough=0.6, feather=0.5)
    water = jar * (np.arange(H)[:, None] > 352)
    art = G(art, water, "#a9c4b8", seed=nx(), density=0.3, edge=0.4, bloom=0, rough=0.6, feather=0.5)
    art = glass_glints(art, jar, nx, col="#ffffff", amt=1.3)
    art = OV(art, strokes(W, H, [([(140, 318), (136, 410)], 5, (0.2, 0.3))]), lambda mm: col_arr(mm, "#ffffff", mm * 0.7), pad=4)
    twine = strokes(W, H, [([(124, 322), (180, 330), (238, 322)], 4, None), (curve([(176, 330), (166, 352), (158, 364)], 10), 3, (0, 0.3))])
    art = GP(art, twine, "#c19a6b", "#a8825a", seed=nx(), rough=0.3)
    preview(art, "pk-bouquet", tone="#f6efe4")
    save(art, f"{OUT}/bouquet.webp", max_w=180, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 340, 110
    nx = Seq(60600); rng = random.Random(606)
    art = blank(W, H)
    st = strokes(W, H, [(curve([(20, 80), (120, 64), (240, 58), (320, 40)], 30), 2.4, (0.05, 0.4))])
    art = G(art, st, "#5f7a4a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.4, feather=0.3)
    for x, y, r, kind, cols in ((90, 58, 12, "cosmos", FLOWERS[4]), (170, 52, 10, "daisy", FLOWERS[3]), (250, 44, 11, "cosmos", FLOWERS[0]), (310, 34, 7, "button", FLOWERS[1])):
        art = G(art, strokes(W, H, [([(x, y + 14), (x, y)], 1.6, None)]), "#5f7a4a", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.3, feather=0.3)
        art = flower_head(art, W, H, x, y, r, cols, nx, rng, kind)
    lv = shapes(W, H, [petal_pts(60, 76, 20, 5, -2.6, 10), petal_pts(140, 66, 18, 5, -0.5, 10), petal_pts(210, 62, 18, 5, -2.4, 10)])
    art = G(art, lv, "#6d8a54", "#88a066", seed=nx(), density=0.8, edge=0.5, bloom=0.1, rough=0.6, feather=0.4)
    preview(art, "pk-sprig", tone="#f6efe4")
    save(art, f"{OUT}/sprig.webp", max_w=200, quality=84)
    clear()
