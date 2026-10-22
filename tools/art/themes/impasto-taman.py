"""Impasto Taman — impressionist oil garden in thick impasto: lily pond, rose banks, dappled light.
Run: python3 -I impasto-taman.py [part ...]   parts: scene roses lily stroke frame canvas
Assets -> public/themes/art/impasto-taman/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *

OUT = outdir("impasto-taman")
PARTS = sys.argv[1:] or ["scene", "roses", "lily", "stroke", "frame", "canvas"]

ROSE = ["#e88aa0", "#f2b6c0", "#d45f78", "#fbe3dc", "#f08e74"]


def foliage_guide(W, H, seed, cols, scale=40):
    """Mottled foliage colour field from several greens + violet shadows + warm light."""
    g = np.zeros((H, W, 3), np.float32)
    n1 = fbm(W, H, seed, scale, 4); n2 = fbm(W, H, seed + 5, scale * 0.5, 3)
    base = np.array([hex_rgb(c) for c in cols], np.float32)
    idx = np.clip((n1 * 0.7 + n2 * 0.3) * (len(cols) - 0.001), 0, len(cols) - 1.001)
    i0 = idx.astype(int); t = (idx - i0)[..., None]
    g = base[i0] * (1 - t) + base[np.minimum(i0 + 1, len(cols) - 1)] * t
    return g


def paint_rose(P, x, y, r, c, rng, light=-2.3):
    """Impasto cabbage rose: crescent petal strokes in rings, lit from the top-left, deep heart."""
    cc = np.array(hex_rgb(c), np.float32)
    dk = cc * np.array([0.62, 0.5, 0.58]); hi = np.minimum(1, cc * 1.04 + 0.2)
    P.dab(x, y, 0.3, r * 1.5, r * 1.45, list(cc * 0.8), hv=0.5, bristle=False)
    for ring in range(5):
        rr = r * (1.0 - ring * 0.19)
        n = 8 - ring
        a0 = rng.uniform(0, math.tau)
        for j in range(n):
            a = a0 + j * math.tau / n + rng.gauss(0, 0.2)
            lit = 0.5 + 0.5 * math.cos(a - light)
            col = cc * (0.78 + 0.3 * lit) + (hi - cc) * lit * 0.5 * (1 - ring / 5)
            if ring >= 3:
                col = col * 0.75 + dk * 0.25
            P.dab(x + math.cos(a) * rr * 0.62, y + math.sin(a) * rr * 0.56, a + math.pi / 2 + rng.gauss(0, 0.15), rr * 0.95, rr * 0.3,
                  list(np.clip(col, 0, 1)), hv=0.62 + ring * 0.07, curl=0.32)
    for k in range(3):
        a = rng.uniform(0, math.tau)
        P.dab(x + math.cos(a) * r * 0.08, y + math.sin(a) * r * 0.08, a, r * 0.4, r * 0.16, list(dk), hv=0.95, curl=0.4)
    P.dab(x - r * 0.42, y - r * 0.46, -0.6, r * 0.55, r * 0.14, list(np.minimum(1, hi + 0.08)), hv=1.0, bristle=False)


if "scene" in PARTS:
    W, H = 720, 960
    rng = random.Random(4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    guide = vgrad(H, W, [(0, "#cfe0e6"), (0.12, "#f3e6c8"), (0.25, "#eadbb2"), (1, "#eadbb2")])
    # distant tree masses with an irregular crown line
    crown = 120 + 70 * fbm(W, 1, 11, 60, 3)[0] + 40 * np.sin(xx[0] / 90)
    trees = (yy > crown[None, :]).astype(np.float32) * (yy < 470)
    tg = foliage_guide(W, H, 21, ["#3f5a52", "#5b7a5c", "#7f8f5a", "#6a6f8f", "#4c6a5e", "#9aa46a"], 50)
    fill(guide, soft(trees, 3), "#000000")
    guide = guide + tg * soft(trees, 3)[..., None]
    # sky holes through the leaves
    holes = (fbm(W, H, 31, 26, 3) > 0.74).astype(np.float32) * trees * (yy < 330)
    fill(guide, soft(holes, 2), "#f4ead0", "#d9e6e4", seed=33)
    # weeping willow on the right: hanging strands of yellow-green
    willow = np.zeros((H, W), np.float32)
    strands = []
    for k in range(46):
        x0 = rng.uniform(420, 760); y0 = rng.uniform(60, 160)
        L = rng.uniform(220, 380)
        strands.append((curve([(x0, y0), (x0 + rng.uniform(-30, 10), y0 + L * 0.5), (x0 + rng.uniform(-40, 0), y0 + L)], 20), rng.uniform(8, 18), (0.1, 0.5)))
    willow = strokes(W, H, strands)
    fill(guide, soft(willow, 2) * 0.85, "#9fae5c", "#5f7b4a", seed=41, scale=40)
    # pond: band with reflections (mirrored trees, darker + cooler) and sky streaks
    pond_top = 455 + 10 * np.sin(xx[0] / 120)
    pond = ((yy > pond_top[None, :]) & (yy < 800 + 30 * np.sin(xx / 150))).astype(np.float32)
    refl = guide[np.clip((2 * 455 - yy).astype(int), 0, H - 1), xx.astype(int)] * 0.6 + np.array(hex_rgb("#7d9fb4"), np.float32) * 0.4
    streak = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), (2, 40))
    streak = np.clip((streak - 0.5) * 9, 0, 1)
    refl = refl * (1 - streak[..., None] * 0.6) + np.array(hex_rgb("#e6eeea"), np.float32) * streak[..., None] * 0.6
    ps = soft(pond, 2)[..., None]
    guide = guide * (1 - ps) + refl * ps
    # lily pads
    pads, lilies = [], []
    for k in range(30):
        y = rng.uniform(500, 790); s = 0.5 + (y - 480) / 320
        x = rng.uniform(-20, W + 20)
        if 420 < x < 760 and y < 520:
            continue
        pads.append((x, y, rng.uniform(30, 52) * s, rng.uniform(10, 17) * s, rng.uniform(-8, 8)))
        if rng.random() < 0.45:
            lilies.append((x + rng.uniform(-8, 8) * s, y - 5 * s, 12 * s))
    padm = ellipses(W, H, pads)
    fill(guide, padm, "#5f8a4c", "#a7b35a", seed=51, scale=24)
    padlight = padm * (fbm(W, H, 53, 18, 2) > 0.55)
    fill(guide, padlight * 0.7, "#c8c66c")
    lilym = circles(W, H, lilies)
    fill(guide, lilym, "#f4b9c6", "#fff1ea", seed=55, scale=8)
    # foreground banks: grass centre, rose bushes left & right
    bank = (yy > 790 + 30 * np.sin(xx / 150) - 12 * fbm(W, H, 61, 30, 2)).astype(np.float32)
    fill(guide, soft(bank, 3), "#6f8a48", "#3d5a3a", seed=63, scale=50)
    bushL = shape_mask(W, H, deform([(-40, 560), (120, 590), (240, 700), (300, 860), (240, 980), (-40, 980)], rng, 3, 0.12))
    bushR = shape_mask(W, H, deform([(W + 40, 610), (600, 640), (500, 760), (470, 900), (520, 980), (W + 40, 980)], rng, 3, 0.12))
    bush = np.maximum(bushL, bushR)
    bg_ = foliage_guide(W, H, 71, ["#2f4a36", "#456b44", "#5d7f45", "#384d5a", "#76904c"], 30)
    bs = soft(bush, 2)[..., None]
    guide = guide * (1 - bs) + bg_ * bs
    roses = []
    for k in range(70):
        side = rng.random() < 0.5
        m = bushL if side else bushR
        for _ in range(20):
            x = rng.uniform(-20, 330) if side else rng.uniform(450, W + 20); y = rng.uniform(570, 960)
            if m[int(min(H - 1, y)), int(min(W - 1, max(0, x)))] > 0.5:
                roses.append((x, y, rng.uniform(9, 22) * (0.6 + (y - 560) / 500), rng.choice(ROSE)))
                break
    for x, y, r, c in roses:
        mm = circles(W, H, [(x, y, r)])
        fill(guide, mm, c, mix(c, "#fff4ec", 0.45), seed=int(x * 7 + y), scale=10)
        fill(guide, circles(W, H, [(x + r * 0.2, y + r * 0.25, r * 0.45)]) * 0.6, mix(c, "#6b2236", 0.35))
    # dappled light: warm patches on bank/bushes/trees
    dap = np.clip((fbm(W, H, 81, 34, 3) - 0.6) * 5, 0, 1) * np.maximum(np.maximum(bank, bush * 0.7), trees * 0.6) * (1 - pond)
    guide = guide * (1 - dap[..., None] * 0.55) + np.array(hex_rgb("#f6e3a0"), np.float32) * dap[..., None] * 0.55
    guide = np.clip(guide, 0, 1)
    preview(np.concatenate([guide, np.ones((H, W, 1), np.float32)], -1), "it-guide", bg="#ffffff")

    # direction field
    base = np.full((H, W), -0.35, np.float32)              # sky: diagonal
    nd = (fbm(W, H, 91, 40, 2) - 0.5) * 2.6
    base = np.where(trees > 0.5, 1.25 + nd, base)            # foliage: varied, mostly steep
    base = np.where(willow > 0.4, math.pi / 2 + 0.12, base)
    base = np.where(pond > 0.5, 0.0 + (fbm(W, H, 93, 60, 2) - 0.5) * 0.25, base)
    base = np.where(bank > 0.5, math.pi / 2 + nd * 0.4, base)
    base = np.where(bush > 0.5, 0.9 + nd, base)
    ang = dir_from(guide, 5, base, 0.45)
    ang = np.where(pond * (1 - padm) > 0.5, (fbm(W, H, 95, 60, 2) - 0.5) * 0.2, ang)

    P = Impasto(W, H, 7)
    P.layer(guide, ang, 15, 46, 20, jitter=0.6, colvar=0.05, seed=1, hv=0.45, angvar=0.3)
    clear()
    P.layer(guide, ang, 10, 30, 12, jitter=0.9, colvar=0.06, seed=2, angvar=0.25)
    detail = np.clip(soft(np.maximum.reduce([padm, lilym, bush, willow * 0.8, holes, dap]), 4) * 3, 0, 1)
    P.layer(guide, ang, 6, 17, 7, where=detail, jitter=0.9, colvar=0.06, seed=3, angvar=0.3, hv=0.75)
    # flowers: short fat dabs, radial strokes around each rose / lily
    for x, y, r, c in roses:
        cc = hex_rgb(c)
        for j in range(int(5 + r / 2)):
            a = rng.uniform(0, math.tau); d = rng.uniform(0, r * 0.7)
            col = [min(1, v * rng.uniform(0.85, 1.12) + rng.uniform(-0.03, 0.12)) for v in cc]
            P.dab(x + math.cos(a) * d, y + math.sin(a) * d * 0.8, a + math.pi / 2 + rng.gauss(0, 0.4), r * rng.uniform(0.5, 0.9), r * rng.uniform(0.3, 0.45), col, hv=rng.uniform(0.8, 1.0), curl=0.2)
        P.dab(x + r * 0.15, y + r * 0.1, rng.uniform(0, 3), r * 0.35, r * 0.28, [v * 0.62 for v in cc], hv=0.7)
        P.dab(x - r * 0.3, y - r * 0.35, rng.uniform(-0.6, 0.2), r * 0.45, r * 0.22, [min(1, v * 1.05 + 0.18) for v in cc], hv=1.0)
    for x, y, r in lilies:
        for j in range(7):
            a = -math.pi / 2 + (j - 3) * 0.42
            col = hex_rgb(rng.choice(["#f7c4cf", "#fbe6e8", "#f2a8b8", "#fff6f0"]))
            P.dab(x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.55, a, r * 0.9, r * 0.38, col, hv=0.95, bristle=False)
        P.dab(x, y + 1, 0, r * 0.4, r * 0.3, hex_rgb("#f2c84b"), hv=1.0, bristle=False)
    # dappled light accents: thick pale-yellow touches
    P.layer(guide, ang, 9, 12, 7, where=dap, thresh=0.35, jitter=1, colvar=0.04, seed=4, lum=0.08, warm=0.05, hv=1.0, prob=0.55)
    # sparkle on water: horizontal light flicks
    flick = np.clip(streak * pond * (1 - padm), 0, 1)
    P.layer(guide, 0.0, 9, 16, 4, where=flick, thresh=0.5, jitter=1, colvar=0.03, seed=5, lum=0.12, hv=0.95, angvar=0.08, prob=0.6)
    clear()
    art = P.finish(relief=3.2, gloss=0.28)
    preview(art, "it-scene", bg="#ffffff")
    save_rgb(art, f"{OUT}/scene.webp", size=(600, 800), quality=74)
    del P; clear()

if "roses" in PARTS:
    # a rose spray (transparent, ragged impasto edge) for corners / closing
    W, H = 640, 460
    rng = random.Random(12)
    guide = foliage_guide(W, H, 101, ["#2f4a36", "#4f7244", "#6e8d4a", "#3b4f63", "#86a052"], 28)
    blob = shape_mask(W, H, deform(ellipse_pts(320, 270, 250, 130, 12, -0.12), rng, 3, 0.1))
    leaves = []
    for k in range(18):
        a = k / 18 * math.tau + rng.uniform(-0.15, 0.15); u = rng.uniform(0.8, 0.95); x = 320 + math.cos(a) * 250 * u; y = 270 + math.sin(a) * 130 * u
        leaves.append(petal_pts(x, y, rng.uniform(50, 75), rng.uniform(16, 22), math.atan2(math.sin(a) * 130, math.cos(a) * 250) + rng.uniform(-0.4, 0.4), n=10))
    lm = shapes(W, H, leaves)
    area = ragged(np.maximum(blob, lm), 103, 10, 26)
    ang = dir_from(guide, 4, (fbm(W, H, 105, 40, 2) - 0.5) * 4, 0.3)
    roses = [(190, 260, 62, ROSE[0]), (330, 210, 74, ROSE[3]), (460, 270, 60, ROSE[4]), (300, 340, 44, ROSE[2]), (110, 340, 34, ROSE[1]), (540, 200, 30, ROSE[1]), (410, 150, 26, ROSE[2])]
    P = Impasto(W, H, 11)
    P.layer(guide, ang, 11, 30, 13, where=area, jitter=0.8, seed=11, hv=0.5)
    for pts in leaves:
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        a = math.atan2(pts[len(pts) // 2][1] - pts[0][1], pts[len(pts) // 2][0] - pts[0][0])
        col = hex_rgb(rng.choice(["#4f7244", "#6e8d4a", "#3a5a3c", "#8aa456"]))
        P.dab(cx, cy, a, 64, 24, col, hv=0.7, curl=0.15, tip=0.7)
        P.dab(cx + math.cos(a + 1.6) * 5, cy + math.sin(a + 1.6) * 5, a, 50, 9, [min(1, v * 1.25 + 0.06) for v in col], hv=0.9, tip=0.7)
    for x, y, r, c in roses:
        paint_rose(P, x, y, r, c, rng)
    art = P.finish(relief=3.4, gloss=0.3, canvas_tex=0)
    a = art[..., 3]
    art[..., 3] = a * np.clip(displace(soft((a > 0.5).astype(np.float32), 1.5), 107, 3, 10) * 1.4, 0, 1)
    preview(art, "it-roses")
    save(art, f"{OUT}/roses.webp", max_w=520, quality=80)
    del P; clear()

if "lily" in PARTS:
    # single water lily on its pad (node / small ornament)
    W, H = 240, 170
    rng = random.Random(21)
    P = Impasto(W, H, 21)
    pad = ellipses(W, H, [(120, 112, 104, 46, -3)])
    pad = np.clip(pad - shapes(W, H, [[(120, 112), (232, 80), (232, 120)]], smooth=False), 0, 1)
    guide = foliage_guide(W, H, 121, ["#4d7a46", "#7f9e4e", "#a9b45c", "#5b8a5a"], 20)
    P.layer(guide, 0.08, 7, 24, 9, where=pad, jitter=0.8, seed=21, hv=0.55, angvar=0.35)
    for j in range(9):
        a = -math.pi / 2 + (j - 4) * 0.34
        col = hex_rgb(["#f7c4cf", "#fbe6e8", "#f2a8b8", "#fff6f0", "#ee97ab"][j % 5])
        P.dab(120 + math.cos(a) * 26, 88 + math.sin(a) * 30, a, 50, 20, col, hv=0.9, curl=0.1)
    for j in range(6):
        a = -math.pi / 2 + (j - 2.5) * 0.45
        P.dab(120 + math.cos(a) * 14, 92 + math.sin(a) * 16, a, 30, 14, hex_rgb(["#fff4f2", "#fbd9de"][j % 2]), hv=1.0)
    P.dab(120, 96, 0, 18, 14, hex_rgb("#f0c04a"), hv=1.0)
    art = P.finish(relief=3.0, gloss=0.3, canvas_tex=0)
    preview(art, "it-lily")
    save(art, f"{OUT}/lily.webp", max_w=180, quality=84)
    del P; clear()

if "stroke" in PARTS:
    # palette-knife smear divider: a long loaded stroke that drags colours (rose -> cream -> leaf green)
    W, H = 520, 110
    P = Impasto(W, H, 31)
    rng = random.Random(31)
    cols = ["#d45f78", "#e88aa0", "#f6e3c4", "#a7b35a", "#5f8a4c"]
    for i in range(160):
        t = i / 159
        x = 30 + t * 460
        y = 55 + 8 * math.sin(t * 5) + rng.gauss(0, 1.2)
        k = t * (len(cols) - 1); i0 = int(min(len(cols) - 2, k))
        c = [a * (1 - (k - i0)) + b * (k - i0) for a, b in zip(hex_rgb(cols[i0]), hex_rgb(cols[i0 + 1]))]
        wd = 36 * (math.sin(math.pi * min(1, t * 1.15)) ** 0.5 if t < 0.87 else max(0.2, (1 - t) * 6))
        P.dab(x, y, 0.05 + rng.gauss(0, 0.05), 18, max(4, wd), c, hv=0.55 + 0.35 * rng.random())
    art = P.finish(relief=3.6, gloss=0.4, canvas_tex=0)
    preview(art, "it-stroke")
    save(art, f"{OUT}/stroke.webp", max_w=360, quality=84)
    del P; clear()

if "frame" in PARTS:
    # painterly gilt frame for border-image (9-slice): 300x300, border 46px, transparent centre
    S, B = 300, 46
    P = Impasto(S, S, 41)
    rng = random.Random(41)
    ring_ = rect_m(S, S, 0, 0, S, S) - rect_m(S, S, B, B, S - B, S - B)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.minimum.reduce([xx, yy, S - 1 - xx, S - 1 - yy])   # distance from outer edge
    prof = np.clip(d / B, 0, 1)
    guide = np.zeros((S, S, 3), np.float32)
    gold = np.array(hex_rgb("#c49a4e"), np.float32); deep = np.array(hex_rgb("#7a5326"), np.float32); light = np.array(hex_rgb("#efd79a"), np.float32)
    bandv = 0.5 + 0.5 * np.cos(prof * math.pi * 3.0)
    guide = deep * (1 - bandv[..., None]) + gold * bandv[..., None]
    guide = np.where((np.abs(prof - 0.55) < 0.08)[..., None], light, guide)
    guide = np.where((prof > 0.86)[..., None], np.array(hex_rgb("#5a3a1c"), np.float32), guide)
    # strokes run along each side
    ang = np.where(np.minimum(yy, S - 1 - yy) < np.minimum(xx, S - 1 - xx), 0.0, math.pi / 2).astype(np.float32)
    P.layer(guide, ang, 6, 20, 7, where=ring_, jitter=0.5, colvar=0.06, seed=41, angvar=0.08, hv=0.6)
    P.layer(guide, ang, 9, 10, 5, where=ring_ * (np.abs(prof - 0.3) < 0.15), jitter=0.8, colvar=0.05, seed=42, lum=0.1, hv=0.95, prob=0.6, angvar=0.1)
    art = P.finish(relief=3.6, gloss=0.55, canvas_tex=0)
    art[..., 3] *= ring_
    preview(art, "it-frame", bg="#efe6d2")
    save_full(art, f"{OUT}/frame.webp", quality=84)
    del P; clear()

if "canvas" in PARTS:
    # primed linen canvas tile (seamless) for the page background
    S = 384
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    k = 2 * math.pi / S * 96
    warp = np.sin(xx * k) * 0.5 + 0.5; weft = np.sin(yy * k) * 0.5 + 0.5
    n = wrap_noise(S, S, 3, 1.2); n2 = wrap_noise(S, S, 4, 24)
    weave = np.where(((xx * 96 / S).astype(int) + (yy * 96 / S).astype(int)) % 2 == 0, warp, weft)
    v = 0.965 + 0.025 * weave + 0.02 * (n - 0.5) + 0.03 * (n2 - 0.5)
    base = np.array(hex_rgb("#f4ecdc"), np.float32)
    rgb = np.clip(base * v[..., None], 0, 1)
    arr = np.concatenate([rgb, np.ones((S, S, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/canvas.webp", quality=72)

kb(OUT)
