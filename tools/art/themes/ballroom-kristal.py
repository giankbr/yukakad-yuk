"""Ballroom Kristal — a grand ballroom in champagne light: painted crystal chandelier (gilt arms, candle glow, swags of
crystal drops), the hall scene (arched windows, silk drapes, round tables with candles, glossy marble floor with
reflections), a single banquet table vignette, a silk swag corner and a seamless marble tile.
Run: python3 -I ballroom-kristal.py [part ...]. parts: chandelier hall table swag marble.
Assets -> public/themes/art/ballroom-kristal/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s3_lib import *

OUT = outdir("ballroom-kristal")
PARTS = sys.argv[1:] or ["chandelier", "hall", "table", "marble", "divider"]
GOLD = "#c9a35a"
CREAM, CHAMP, TAUPE, ESP = "#f7efe2", "#e8d6b5", "#9a8266", "#3a2c22"
SILK, SILK_D = "#ead7bd", "#b99b78"


def _unused_crystal_layer(W, H, items, seed):
    """items: list of polygons (crystal drops). Painted as pale glass: grey-lilac body, white highlight, warm reflex."""
    body = shapes(W, H, items, smooth=False)
    art = blank(W, H)
    art = GP(art, body, "#d9d6d8", "#b9b3b8", seed=seed, rough=0.6, streak=0.6, density=0.88, pad=6)
    # facet: left half lighter, right half darker
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hl = []
    sh = []
    for p in items:
        xs = [q[0] for q in p]; ys = [q[1] for q in p]
        cx = sum(xs) / len(xs); top = min(ys); bot = max(ys); w = max(xs) - min(xs)
        hl.append([(cx - w * 0.3, top + (bot - top) * 0.3), (cx - w * 0.05, top + (bot - top) * 0.15), (cx - w * 0.05, top + (bot - top) * 0.8), (cx - w * 0.28, top + (bot - top) * 0.62)])
        sh.append([(cx + w * 0.05, top + (bot - top) * 0.25), (cx + w * 0.34, top + (bot - top) * 0.55), (cx + w * 0.05, bot - (bot - top) * 0.05)])
    art = OV(art, shapes(W, H, hl, smooth=False) * body, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fffdf8"), np.float32), (m * 0.85)[..., None]], -1), pad=4)
    art = OV(art, shapes(W, H, sh, smooth=False) * body, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#8e8590"), np.float32), (m * 0.55)[..., None]], -1), pad=4)
    return art, body


def glass(W, H, beads, drops, seed, dim=1.0):
    """Paint crystal beads (x, y, r) and drops (polygons) as cut glass: grey-lilac rim, pale body, white glint."""
    art = blank(W, H)
    body = np.maximum(circles(W, H, beads), shapes(W, H, drops, smooth=False) if drops else 0)
    rim = np.clip(gaussian_filter(body, 0.9) - gaussian_filter(body, 0.9) * 0 - np.clip((gaussian_filter(body, 1.2) - 0.75) * 4, 0, 1), 0, 1) * (body > 0.05)
    a = body * 0.92 * dim
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    tint = 0.5 + 0.5 * np.sin(xx * 0.07 + yy * 0.05 + fbm(W, H, seed, 40, 2) * 5)
    base = ramp(tint, [(0, "#d7d2da"), (0.5, "#f2efea"), (1, "#e9dcc4")])
    rgb = base * (1 - rim[..., None] * 0.55) + np.array(hex_rgb("#6f6670"), np.float32) * rim[..., None] * 0.55
    art = np.concatenate([rgb, a[..., None]], -1)
    gl = circles(W, H, [(x - r * 0.35, y - r * 0.35, max(0.8, r * 0.38)) for x, y, r in beads[::2]])
    art = over(art, np.concatenate([np.ones((H, W, 3), np.float32), (gl * 0.95 * dim)[..., None]], -1))
    if drops:
        hl = []
        for p in drops:
            xs = [q[0] for q in p]; ys = [q[1] for q in p]
            cx = sum(xs) / len(xs); top = min(ys); bot = max(ys); w = max(xs) - min(xs)
            hl.append([(cx - w * 0.28, top + (bot - top) * 0.32), (cx - w * 0.04, top + (bot - top) * 0.12), (cx - w * 0.04, top + (bot - top) * 0.82)])
        hm = shapes(W, H, hl, smooth=False)
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32), (hm * 0.85 * dim)[..., None]], -1))
    return art


def chandelier(W, H, cx, top, s, seed, glow_amt=1.0):
    """Tiered crystal chandelier ("wedding cake" with a crystal basket), width ~ 2*s. Returns RGBA."""
    rng = random.Random(seed)
    nx = Seq(seed)
    tiers = [(top + s * 0.30, s * 0.34, 14, 0.16), (top + s * 0.62, s * 0.62, 20, 0.2), (top + s * 0.96, s * 0.86, 26, 0.24)]
    back_b, front_b, back_d, front_d, candles_f, candles_b = [], [], [], [], [], []
    gold_items = [([(cx, 0), (cx, top + s * 0.1)], s * 0.022, None)]
    for k, (ty, rx, n, L) in enumerate(tiers):
        ry = rx * 0.2
        gold_items.append(([(cx + math.cos(t) * rx, ty + math.sin(t) * ry) for t in np.linspace(0, math.tau, 64)], s * 0.019, None))
        # arms from stem to ring
        for t in np.linspace(0, math.tau, 7)[:-1] + 0.3:
            gold_items.append((curve([(cx, ty - s * 0.08), (cx + math.cos(t) * rx * 0.5, ty - s * 0.1 + math.sin(t) * ry * 0.5), (cx + math.cos(t) * rx, ty + math.sin(t) * ry)], 12), s * 0.014, None))
        for i in range(n):
            t = math.tau * i / n + (0.5 if k % 2 else 0) * math.tau / n
            x0 = cx + math.cos(t) * rx; y0 = ty + math.sin(t) * ry
            front = math.sin(t) > -0.05
            ln = L * s * (0.85 + 0.3 * rng.random())
            bb = back_b if not front else front_b
            dd = back_d if not front else front_d
            nb = max(3, int(ln / (s * 0.03)))
            for j in range(1, nb):
                bb.append((x0, y0 + j * ln / nb, s * 0.0105))
            dd.append(crystal_drop(W, H, x0, y0 + ln, s * 0.05, rng, "pear" if i % 2 else "prism"))
            if i % 3 == 0:
                (candles_f if front else candles_b).append((x0, y0 - s * 0.012))
        # front swag of beads between strands
        for i in range(n):
            t1 = math.tau * i / n; t2 = math.tau * (i + 1) / n
            if math.sin((t1 + t2) / 2) < 0.1:
                continue
            for j in range(1, 6):
                u = j / 6
                t = t1 + (t2 - t1) * u
                front_b.append((cx + math.cos(t) * rx, ty + math.sin(t) * ry + math.sin(u * math.pi) * s * 0.06, s * 0.009))
    # crystal basket under the bottom tier converging to a finial
    ty, rx, n, L = tiers[-1]
    bot = top + s * 1.62
    for i in range(18):
        t = math.tau * i / 18
        x0 = cx + math.cos(t) * rx * 0.55; y0 = ty + s * 0.05 + math.sin(t) * rx * 0.1
        front = math.sin(t) > -0.05
        for j in range(1, 14):
            u = j / 14
            x = x0 + (cx - x0) * u ** 1.4; y = y0 + (bot - y0) * u + math.sin(u * math.pi) * s * 0.06
            (front_b if front else back_b).append((x, y, s * (0.011 - 0.004 * u)))
    front_d.append(crystal_drop(W, H, cx, bot, s * 0.11, rng, "pear"))
    stem = shapes(W, H, [[(cx - s * 0.025, top + s * 0.08), (cx + s * 0.025, top + s * 0.08), (cx + s * 0.035, top + s * 1.06), (cx - s * 0.035, top + s * 1.06)]], smooth=False)
    knobs = ellipses(W, H, [(cx, top + s * yy, s * r, s * r * 0.7, 0) for yy, r in ((0.12, 0.06), (0.26, 0.05), (0.56, 0.08), (0.9, 0.09), (1.06, 0.1))])
    art = blank(W, H)
    # warm glow behind
    art = over(art, glow(circles(W, H, [(cx, top + s * 0.75, s * 0.55)]), "#fff0c8", radius=s * 0.3, strength=0.2 * glow_amt))
    art = over(art, glass(W, H, back_b, back_d, nx(), dim=0.55))
    cm = circles(W, H, [(x, y - s * 0.06, s * 0.03) for x, y in candles_b + candles_f])
    art = over(art, glow(cm, "#ffd98a", radius=s * 0.07, strength=0.6 * glow_amt))
    gold = np.maximum.reduce([strokes(W, H, gold_items), stem, knobs])
    art = FO(art, gold, GOLD, seed=nx(), emboss=0.7, sparkle=0.08)
    for cl in (candles_b, candles_f):
        if not cl:
            continue
        wax = shapes(W, H, [[(x - s * 0.01, y), (x + s * 0.01, y), (x + s * 0.009, y - s * 0.07), (x - s * 0.009, y - s * 0.07)] for x, y in cl], smooth=False)
        art = GP(art, wax, "#fbf6ea", "#e2d4ba", seed=nx(), rough=0.3, pad=4)
        cups = ellipses(W, H, [(x, y, s * 0.022, s * 0.01, 0) for x, y in cl])
        art = FO(art, cups, "#d8b46a", seed=nx(), emboss=0.5)
        fl = shapes(W, H, [petal_pts(x, y - s * 0.072, s * 0.04, s * 0.012, -math.pi / 2, n=10) for x, y in cl])
        art = over(art, glow(fl, "#ffcf6a", radius=s * 0.018, strength=0.7))
        art = GP(art, fl, "#fff3c4", "#ffbb50", seed=nx(), rough=0.3, pad=4)
    art = over(art, glass(W, H, front_b, front_d, nx(), dim=1.0))
    return art


if "chandelier" in PARTS:
    W, H = 520, 680
    art = chandelier(W, H, 260, 40, 240, 7001)
    preview(art, "bk-chandelier", bg="#efe2c8")
    preview(art, "bk-chandelier-d", bg="#3a2c22")
    save(art, f"{OUT}/chandelier.webp", max_w=400, quality=82)


def marble_rgb(W, H, seed, base="#f3ebe0", vein="#a8998a", wrap=True, sc=1.0):
    """Turbulence marble: a few long wavy veins with varying width + faint secondary veins + cloudy body."""
    nz = (lambda s_, sg: wrap_noise(W, H, s_, sg)) if wrap else (lambda s_, sg: fbm(W, H, s_, sg * 4, 4))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n1 = nz(seed, 26 * sc); n2 = nz(seed + 1, 6 * sc); n3 = nz(seed + 2, 50 * sc); n4 = nz(seed + 3, 14 * sc)
    turb = (n1 - 0.5) * 1.3 + (n4 - 0.5) * 0.5 + (n2 - 0.5) * 0.15
    f = np.sin((xx / W * 1 + yy / H * 2) * np.pi * 2 + turb * 2.4)
    width = 0.05 + 0.08 * n3
    v1 = np.clip(1 - np.abs(f) / width, 0, 1) ** 1.3
    f2 = np.sin((xx / W * 3 - yy / H * 1) * np.pi * 2 + turb * 2.6 + 1.3)
    v2 = np.clip(1 - np.abs(f2) / 0.03, 0, 1) * 0.45 * (n3 > 0.45)
    cloud = (n3 - 0.5) * 0.07 + (n2 - 0.5) * 0.03
    b = np.array(hex_rgb(base), np.float32); v = np.array(hex_rgb(vein), np.float32)
    t = np.clip(v1 * 0.6 + v2 * 0.5, 0, 1)[..., None]
    halo = np.clip(1 - np.abs(f) / (width * 4), 0, 1)[..., None] * 0.12
    rgb = b * (1 + cloud[..., None]) * (1 - t) * (1 - halo * 0.4) + v * t
    return np.clip(rgb, 0, 1)


if "marble" in PARTS:
    W = H = 480
    rgb = marble_rgb(W, H, 5101)
    art = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    preview(art, "bk-marble")
    save_full(art, f"{OUT}/marble.webp", quality=70)


def table_art(art, W, H, cx, cy, s, nx, rng, floor_reflect=True, chairs_on=True):
    """Round banquet table at (cx, cy) = centre of the top ellipse; s = radius. Ivory cloth, gilt chairs, candles."""
    rx, ry = s, s * 0.26
    drop = s * 0.5
    # chairs behind (gilt chiavari backs)
    chairs = []
    for k in range(7):
        t = math.pi + math.pi * (k + 0.5) / 7
        x = cx + math.cos(t) * rx * 1.08; y = cy + math.sin(t) * ry * 1.08
        cw, ch = s * 0.07, s * 0.26
        chairs.append(([(x - cw, y), (x - cw, y - ch), (x + cw, y - ch), (x + cw, y)], s * 0.016, None))
        for u in (-0.33, 0.33):
            chairs.append(([(x + cw * u, y - ch), (x + cw * u, y - ch * 0.45)], s * 0.01, None))
        chairs.append(([(x - cw, y - ch * 0.45), (x + cw, y - ch * 0.45)], s * 0.012, None))
    if chairs_on:
        art = FO(art, strokes(W, H, chairs), "#bf9a55", seed=nx(), emboss=0.4, sparkle=0.05)
    # shadow/reflection on floor
    if floor_reflect:
        refl = shapes(W, H, [deform(ellipse_pts(cx, cy + drop + ry * 0.4, rx * 1.05, ry * 0.5), rng, 1, 0.04)])
        art = G(art, refl, "#6f5a46", seed=nx(), density=0.28, edge=0.1, bloom=0.2, rough=3, feather=s * 0.05)
    # skirt with folds
    skirt_pts = [(cx - rx, cy)] + [(cx - rx * 1.04 + rx * 2.08 * u, cy + drop + math.sin(u * 22) * s * 0.025 + math.sin(u * math.pi) * ry * 0.9) for u in np.linspace(0, 1, 30)] + [(cx + rx, cy)]
    skirt = shapes(W, H, [skirt_pts], smooth=False)
    art = GP(art, skirt, "#f6f1e8", "#e4dacb", seed=nx(), rough=1.0, streak=0.6, pad=8)
    folds = strokes(W, H, [([(cx - rx + rx * 2 * u, cy + ry * 0.6), (cx - rx * 1.03 + rx * 2.06 * u, cy + drop + math.sin(u * math.pi) * ry * 0.8)], s * 0.035, (0.3, 0.1)) for u in np.linspace(0.06, 0.94, 11)])
    art = G(art, folds * skirt, "#b9a993", seed=nx(), density=0.35, edge=0.2, bloom=0.1, rough=1.5, feather=s * 0.02)
    sidesh = np.clip(skirt * (np.abs(np.mgrid[0:H, 0:W][1] - cx) / rx) ** 3, 0, 1)
    art = G(art, sidesh, "#a8957c", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=s * 0.04)
    top = ellipses(W, H, [(cx, cy, rx, ry, 0)])
    art = GP(art, top, "#fffaf2", "#efe6d6", seed=nx(), rough=0.8, pad=8)
    # place settings: gold chargers
    plates = ellipses(W, H, [(cx + math.cos(t) * rx * 0.72, cy + math.sin(t) * ry * 0.72, s * 0.09, s * 0.03, 0) for t in np.linspace(0, math.tau, 9)[:-1]])
    art = FO(art, plates, "#d1b06e", seed=nx(), emboss=0.4, sparkle=0.05)
    # centrepiece: low blush flowers + three candles in glass
    flow = ellipses(W, H, [(cx + dx * s, cy - s * 0.03 + dy * s, s * r, s * r * 0.8, 0) for dx, dy, r in ((-0.12, 0, .07), (0.0, -0.04, .08), (0.12, 0, .07), (-0.05, 0.03, .06), (0.07, 0.03, .06))])
    art = G(art, flow, "#e8b9ad", "#c98a86", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=2)
    leaves = ellipses(W, H, [(cx + dx * s, cy + s * 0.05, s * 0.05, s * 0.018, a) for dx, a in ((-0.2, -20), (0.2, 20), (-0.02, 5))])
    art = G(art, leaves, "#8d9a7a", "#5e6d52", seed=nx(), density=0.8, edge=0.4, rough=1)
    # tall gilt candelabra in the centre
    cdl = strokes(W, H, [([(cx, cy - s * 0.05), (cx, cy - s * 0.62)], s * 0.025, None), (curve([(cx - s * 0.18, cy - s * 0.5), (cx - s * 0.12, cy - s * 0.4), (cx, cy - s * 0.42), (cx + s * 0.12, cy - s * 0.4), (cx + s * 0.18, cy - s * 0.5)], 20), s * 0.02, None)])
    cdl = np.maximum(cdl, ellipses(W, H, [(cx, cy - s * 0.04, s * 0.07, s * 0.022, 0)]))
    art = FO(art, cdl, "#c9a35a", seed=nx(), emboss=0.6, sparkle=0.05)
    cand = [(cx - s * 0.18, cy - s * 0.5, 0.14), (cx, cy - s * 0.62, 0.14), (cx + s * 0.18, cy - s * 0.5, 0.14), (cx - s * 0.3, cy + s * 0.02, 0.1), (cx + s * 0.3, cy + s * 0.02, 0.1)]
    fl = shapes(W, H, [petal_pts(x, y - s * h - s * 0.01, s * 0.08, s * 0.024, -math.pi / 2, n=10) for x, y, h in cand])
    art = over(art, glow(fl, "#ffd27a", radius=s * 0.1, strength=0.5))
    wax = shapes(W, H, [[(x - s * .018, y), (x + s * .018, y), (x + s * .016, y - s * h), (x - s * .016, y - s * h)] for x, y, h in cand], smooth=False)
    art = GP(art, wax, "#fffbf1", "#eadfc8", seed=nx(), rough=0.3, pad=4)
    art = GP(art, fl, "#fff4c8", "#ffbf55", seed=nx(), rough=0.3, pad=4)
    return art


if "table" in PARTS:
    W, H = 560, 420
    nx = Seq(5300); rng = random.Random(3)
    art = blank(W, H)
    art = table_art(art, W, H, 280, 220, 220, nx, rng, chairs_on=False)
    preview(art, "bk-table", tone="#f3ebe0")
    save(art, f"{OUT}/table.webp", max_w=420, quality=80)


if "swag" in PARTS:
    # silk drape corner: a swag from the top-left with a tie-back tassel; champagne silk with deep folds
    W, H = 420, 620
    nx = Seq(5500); rng = random.Random(8)
    art = blank(W, H)
    panel = [(0, 0), (150, 0), (170, 120), (150, 300), (118, 380), (128, 470), (170, 620), (0, 620)]
    pm = shapes(W, H, [panel])
    art = GP(art, pm, SILK, SILK_D, seed=nx(), rough=1.2, streak=0.3, pad=10)
    folds = []
    for k in range(7):
        x0 = 10 + k * 20
        folds.append((curve([(x0, 0), (x0 + 30 + k * 6, 160), (118 - (6 - k) * 6, 380), (x0 + 20 + k * 4, 620)], 30), 9 - k * 0.6, (0.05, 0.05)))
    fm = strokes(W, H, folds) * pm
    art = G(art, fm, "#8e7154", seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=2, feather=3)
    hi = strokes(W, H, [(curve([(x0 + 10, 0), (x0 + 40 + k * 6, 160), (122 - (6 - k) * 6, 380), (x0 + 30 + k * 4, 620)], 30), 3, (0.1, 0.1)) for k, x0 in enumerate(range(16, 160, 22))]) * pm
    art = G(art, hi, "#fff6e6", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=2)
    swag = [(0, 0), (420, 0), (420, 30), (330, 70), (220, 110), (120, 100), (40, 70), (0, 60)]
    sm = shapes(W, H, [swag])
    art = GP(art, sm, "#efdec4", SILK_D, seed=nx(), rough=1.2, streak=0.3, pad=10)
    sw = strokes(W, H, [(curve([(10, 20 + k * 12), (130, 60 + k * 13), (260, 50 + k * 10), (410, 10 + k * 6)], 30), 4, (0.1, 0.1)) for k in range(5)]) * sm
    art = G(art, sw, "#9a7b5c", seed=nx(), density=0.5, edge=0.3, rough=1.5, feather=2)
    tie = strokes(W, H, [(curve([(110, 372), (140, 384), (170, 380)], 10), 10, None)])
    art = FO(art, tie, GOLD, seed=nx(), emboss=0.7)
    tassel = shapes(W, H, [[(166, 380), (178, 380), (190, 450), (154, 450)]], smooth=False)
    art = FO(art, tassel, "#c79c4d", seed=nx(), emboss=0.5)
    tl = strokes(W, H, [([(158 + k * 3.2, 412), (156 + k * 3.4, 452)], 1.2, None) for k in range(11)])
    art = G(art, tl, "#7a5a26", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    preview(art, "bk-swag", tone="#f3ebe0")
    save(art, f"{OUT}/swag.webp", max_w=260, quality=80)


if "hall" in PARTS:
    W, H = 720, 980
    VX, VY, FY = 360, 330, 520  # vanishing point, floor line (base of the back wall)
    nx = Seq(5700); rng = random.Random(21)
    sky = painted_sky(W, H, [(0, "#e9d8b8"), (0.45, "#e6cfa6"), (1, "#d2b48a")], seed=nx(), streak=0.8)
    art = sky.copy()
    # side walls in perspective (slightly darker), back wall rectangle
    BX0, BX1, BY0 = 150, 570, 120
    lw = shapes(W, H, [[(0, 0), (BX0, BY0), (BX0, FY), (0, H * 0.72)]], smooth=False)
    rw = shapes(W, H, [[(W, 0), (BX1, BY0), (BX1, FY), (W, H * 0.72)]], smooth=False)
    art = G(art, np.maximum(lw, rw), "#c7ad85", seed=nx(), density=0.35, edge=0.15, bloom=0.2, rough=3)
    # cornice
    corn = shapes(W, H, [[(BX0 - 4, BY0 - 4), (BX1 + 4, BY0 - 4), (BX1 + 4, BY0 + 12), (BX0 - 4, BY0 + 12)]], smooth=False)
    art = FO(art, corn, GOLD, seed=nx(), emboss=0.6, sparkle=0.05)
    cl = strokes(W, H, [([(0, 0), (BX0, BY0)], 6, None), ([(W, 0), (BX1, BY0)], 6, None), ([(0, 40), (BX0, BY0 + 30)], 3, None), ([(W, 40), (BX1, BY0 + 30)], 3, None)])
    art = FO(art, cl, "#b8914a", seed=nx(), emboss=0.5)
    # arched windows on back wall, glowing
    wins = []
    for wx in (225, 360, 495):
        ww = 74
        pts = [(wx - ww / 2, FY - 18), (wx - ww / 2, 220)] + arc_pts(wx, 220, ww / 2, math.pi, math.tau, 16) + [(wx + ww / 2, FY - 18)]
        wins.append(pts)
    wm = shapes(W, H, wins, smooth=False)
    art = over(art, glow(wm, "#fff6dc", radius=26, strength=0.45))
    win_col = painted_sky(W, H, [(0, "#fffaf0"), (0.4, "#fbeed0"), (0.6, "#f1dcb0"), (1, "#e9cf9d")], seed=nx(), streak=0.4)
    win_col[..., 3] = gaussian_filter(wm, 0.8)
    art = over(art, win_col)
    mull = []
    for wx in (225, 360, 495):
        mull.append(([(wx, 186), (wx, FY - 18)], 2.0, None))
        for yy in range(250, FY - 18, 44):
            mull.append(([(wx - 37, yy), (wx + 37, yy)], 1.6, None))
    art = G(art, strokes(W, H, mull) * gaussian_filter(wm, 1), "#a88b62", seed=nx(), density=0.65, edge=0.1, bloom=0, rough=0.6, feather=0.6)
    # pilasters between windows
    pil = shapes(W, H, [[(x - 11, 160), (x + 11, 160), (x + 11, FY), (x - 11, FY)] for x in (BX0 + 14, 292, 428, BX1 - 14)], smooth=False)
    art = GP(art, pil, "#f4ead8", "#e3d2b3", seed=nx(), rough=0.8, streak=0.8)
    caps = shapes(W, H, [[(x - 15, 152), (x + 15, 152), (x + 13, 166), (x - 13, 166)] for x in (BX0 + 14, 292, 428, BX1 - 14)], smooth=False)
    art = FO(art, caps, GOLD, seed=nx(), emboss=0.6)
    # dado line
    art = FO(art, strokes(W, H, [([(BX0, FY - 30), (BX1, FY - 30)], 2.5, None)]), "#b8914a", seed=nx(), emboss=0.4)
    # marble floor in perspective with reflections
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    below = yy > FY
    z = 9000.0 / np.maximum(yy - VY, 1)
    X = (xx - VX) * z / 400.0
    Z = z
    chk = ((np.floor(X / 3.2) + np.floor(Z / 3.2)) % 2).astype(np.float32)
    mar = marble_rgb(W, H, 5801, base="#f1e7d7", vein="#b3a28c", wrap=False, sc=1.5)
    mar2 = marble_rgb(W, H, 5803, base="#dcc7a6", vein="#9a8468", wrap=False, sc=1.5)
    floor = mar * (1 - chk[..., None]) + mar2 * chk[..., None]
    # reflection of the wall + windows (mirror about the floor line), blurred and faded with depth
    ref = np.zeros_like(floor)
    src_rows = np.clip(2 * FY - yy.astype(int), 0, H - 1)
    ref = art[src_rows, xx.astype(int), :3]
    ref = gaussian_filter(ref, (6, 1.5, 0))
    fade = np.clip(1 - (yy - FY) / (H - FY) * 1.1, 0, 1)[..., None] * 0.55
    floor = floor * (1 - fade) + ref * fade
    # depth darkening near the wall + vignette to the sides
    floor *= (0.88 + 0.12 * np.clip((yy - FY) / 200, 0, 1))[..., None]
    fl = np.concatenate([floor, below[..., None].astype(np.float32)], -1)
    art = over(art, fl)
    joint = np.clip(1 - np.minimum(np.abs((X % 1.0) - 0.5), np.abs((Z % 1.0) - 0.5)) * 0, 0, 1)
    # tables receding (far to near)
    # two distant chandeliers hanging in front of the back wall
    for cxx in (250, 470):
        ch = chandelier(W, H, cxx, 140, 58, 7100 + cxx, glow_amt=1.0)
        art = over(art, ch)
        trim_cache()
    art = over(art, glow(circles(W, H, [(360, 300, 40)]), "#fff4d8", radius=60, strength=0.12))
    rows = [(FY + 34, [196, 300, 420, 524], 34), (FY + 110, [150, 360, 570], 64), (FY + 290, [120, 600], 150)]
    for ty, xs, sz in rows:
        for x in xs:
            art = table_art(art, W, H, x + rng.uniform(-5, 5), ty, sz, nx, rng, chairs_on=False)
        trim_cache()
    # warm haze in the middle distance
    haze = shapes(W, H, [[(BX0, FY - 80), (BX1, FY - 80), (BX1 + 40, FY + 60), (BX0 - 40, FY + 60)]], smooth=False)
    art = over(art, glow(haze, "#fff3da", radius=30, strength=0.18))
    # silk drapes framing both sides, valance swag across the top
    for side in (-1, 1):
        def X_(x):
            return x if side < 0 else W - x
        panel = [(X_(0), 0), (X_(120), 0), (X_(136), 200), (X_(118), 520), (X_(92), 600), (X_(112), 760), (X_(160), H), (X_(0), H)]
        pm = shapes(W, H, [panel])
        art = GP(art, pm, SILK, SILK_D, seed=nx(), rough=1.4, streak=1.3, pad=10)
        folds, his = [], []
        for k in range(7):
            x0 = 6 + k * 17
            path = [(X_(x0), 0), (X_(x0 + 26 + k * 5), 240), (X_(96 - (6 - k) * 5), 600), (X_(x0 + 30 + k * 6), H)]
            folds.append((curve(path, 40), 9 - k * 0.5, (0.04, 0.04)))
            his.append((curve([(px + (4 if side < 0 else -4), py) for px, py in path], 40), 3.2, (0.1, 0.1)))
        art = G(art, strokes(W, H, folds) * pm, "#86694c", seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=2, feather=3)
        art = G(art, strokes(W, H, his) * pm, "#fff7e8", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=1, feather=2)
        tie = strokes(W, H, [(curve([(X_(88), 594), (X_(108), 604), (X_(126), 600)], 10), 7, None)])
        art = FO(art, tie, GOLD, seed=nx(), emboss=0.7)
        trim_cache()
    val = [(0, 0), (W, 0), (W, 46)] + [(W - u * W, 46 + 34 * abs(math.sin(u * math.pi * 3))) for u in np.linspace(0, 1, 60)] + [(0, 46)]
    vm = shapes(W, H, [val], smooth=False)
    art = GP(art, vm, "#efdec4", SILK_D, seed=nx(), rough=1.2, streak=1.2, pad=10)
    vs = strokes(W, H, [([(W - u * W, 8 + k * 9 + 28 * abs(math.sin(u * math.pi * 3)) * (k / 4)) for u in np.linspace(0, 1, 90)], 3, (0.02, 0.02)) for k in range(5)]) * vm
    art = G(art, vs, "#9a7b5c", seed=nx(), density=0.45, edge=0.3, rough=1.5, feather=2)
    # light pools from the windows on the floor
    pools = shapes(W, H, [[(wx - 30, FY + 4), (wx + 30, FY + 4), (wx + 90, H), (wx - 90, H)] for wx in (225, 360, 495)], smooth=False)
    art = over(art, glow(pools, "#fff2d2", radius=24, strength=0.12))
    # soft vignette and grain
    art = vignette(art, strength=0.32)
    art = add_grain(art, seed=5, amount=0.03)
    art[..., 3] = 1
    # fade the top edge so it melts into the cover's champagne gradient
    tfade = np.clip(yy / 60, 0, 1)
    art[..., 3] = tfade
    preview(art, "bk-hall")
    save_full(art, f"{OUT}/hall.webp", size=(560, 762), quality=74)


if "divider" in PARTS:
    # gilt rod with three swags of crystal beads and a drop at each low point
    W, H = 440, 90
    nx = Seq(5900); rng = random.Random(2)
    rod = strokes(W, H, [([(20, 20), (420, 20)], 3.2, (0.05, 0.05))])
    knobs = circles(W, H, [(20, 20, 6), (420, 20, 6), (153, 20, 5), (287, 20, 5)])
    art = FO(blank(W, H), np.maximum(rod, knobs), GOLD, seed=nx(), emboss=0.6)
    beads, drops = [], []
    for a, b, d in ((20, 153, 26), (153, 287, 34), (287, 420, 26)):
        for j in range(1, 22):
            u = j / 22
            beads.append((a + (b - a) * u, 22 + math.sin(u * math.pi) * d, 2.6))
        drops.append(crystal_drop(W, H, (a + b) / 2, 22 + d + 3, 14, rng, "pear"))
    art = over(art, glass(W, H, beads, drops, nx()))
    preview(art, "bk-divider", tone="#f3ebe0")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
