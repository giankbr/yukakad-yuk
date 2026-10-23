"""Kebun Sayur — playful farm gouache: harvest basket (carrots, tomatoes, cabbage, eggplant, radishes), zinc watering
can, blank wooden plant stake, raised wooden bed with sprouting rows, wildflower posy, and small carrot/tomato/pea icons.
Run: python3 -I kebun-sayur.py [part ...]  parts: basket can stake bed wild icons
Assets -> public/themes/art/kebun-sayur/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m6_lib import *

OUT = outdir("kebun-sayur")
PARTS = sys.argv[1:] or ["basket", "can", "stake", "bed", "wild", "icons"]

LEAF, LEAF_D, LEAF_L = "#5f8f3a", "#3d6427", "#8fb85a"
TOM, TOM_D, TOM_L = "#d8452f", "#a32c1f", "#f07a5a"
CAR, CAR_D = "#ee8a2a", "#c2611a"
EGG, EGG_D, EGG_L = "#5b3a6b", "#3b2348", "#8a6a9c"
RAD, RAD_D = "#d9506b", "#a8324d"
CAB, CAB_D, CAB_L = "#9cc46a", "#6c9a45", "#cfe39a"
WICK, WICK_D, WICK_L = "#c99a5a", "#8f6533", "#e4bf80"
WOOD, WOOD_D, WOOD_L = "#c79a62", "#93683e", "#e2bf8a"
SOIL, SOIL_D = "#6b4630", "#47301f"
ZINC, ZINC_D, ZINC_L = "#9fb0b9", "#6c7e89", "#d3dde2"


def hilite(art, W, H, m, x, y, rx, ry, col, nx, amt=0.75):
    hm = ellipses(W, H, [(x, y, rx, ry, -30)]) * m
    return GP(art, gaussian_filter(hm, 1.2) * amt, col, seed=nx(), rough=0.8)


def tomato(art, W, H, x, y, r, rng, nx):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 0.88, 12), rng, 1, 0.05))
    art = GP(art, m, TOM, TOM_D, seed=nx(), rough=1.2, streak=0.8)
    sh = m * np.clip((np.arange(W)[None, :] - x) / r, 0, 1) * np.clip((np.arange(H)[:, None] - y + r * .2) / r, 0, 1)
    art = GP(art, sh * 0.6, TOM_D, seed=nx(), rough=1)
    art = hilite(art, W, H, m, x - r * .38, y - r * .38, r * .28, r * .16, TOM_L, nx)
    cal = shapes(W, H, [petal_pts(x, y - r * .78, r * .55, r * .2, a, n=10) for a in np.linspace(0, math.tau, 6)[:-1] + rng.uniform(0, 1)])
    art = GP(art, cal, LEAF, LEAF_D, seed=nx(), rough=0.8)
    return art


def carrot(art, W, H, x, y, L, ang, rng, nx):
    tip = (x + math.cos(ang) * L, y + math.sin(ang) * L)
    pa = ang + math.pi / 2
    w = L * 0.12
    body = [(x + math.cos(pa) * w, y + math.sin(pa) * w), ((x + tip[0]) / 2 + math.cos(pa) * w * 0.6, (y + tip[1]) / 2 + math.sin(pa) * w * 0.6), tip,
            ((x + tip[0]) / 2 - math.cos(pa) * w * 0.6, (y + tip[1]) / 2 - math.sin(pa) * w * 0.6), (x - math.cos(pa) * w, y - math.sin(pa) * w)]
    m = shape_mask(W, H, body)
    tops = []
    for k in range(5):
        a2 = ang + math.pi + (k - 2) * 0.32 + rng.uniform(-.1, .1)
        LL = L * rng.uniform(0.45, 0.7)
        tops.append((curve([(x, y), (x + math.cos(a2) * LL * .5, y + math.sin(a2) * LL * .5 - 3), (x + math.cos(a2) * LL, y + math.sin(a2) * LL)], 8), L * 0.045, (0.05, 0.4)))
    tm = strokes(W, H, tops)
    art = GP(art, tm, LEAF, LEAF_D, seed=nx(), rough=1)
    fr = []
    for k in range(int(L / 9)):
        t = rng.uniform(0.1, 0.9)
        r = w * (1 - t * .6)
        px, py = x + math.cos(ang) * L * t, y + math.sin(ang) * L * t
        fr.append(([(px - math.cos(pa) * r * .8, py - math.sin(pa) * r * .8), (px - math.cos(pa) * r * .2, py - math.sin(pa) * r * .2)], 1.3, None))
    art = GP(art, m, CAR, CAR_D, seed=nx(), rough=1.0, streak=1.0)
    art = GP(art, strokes(W, H, fr) * m * 0.6, CAR_D, seed=nx(), rough=0.5)
    return art


def eggplant(art, W, H, x, y, L, ang, rng, nx):
    pa = ang + math.pi / 2
    pts = []
    for k in range(14):
        t = k / 13
        wd = L * (0.16 + 0.18 * math.sin(t * math.pi) ** 0.8 * (0.6 + 0.6 * t))
        pts.append((x + math.cos(ang) * L * t + math.cos(pa) * wd, y + math.sin(ang) * L * t + math.sin(pa) * wd))
    for k in range(13, -1, -1):
        t = k / 13
        wd = L * (0.16 + 0.18 * math.sin(t * math.pi) ** 0.8 * (0.6 + 0.6 * t))
        pts.append((x + math.cos(ang) * L * t - math.cos(pa) * wd * 0.9, y + math.sin(ang) * L * t - math.sin(pa) * wd * 0.9))
    m = shape_mask(W, H, pts)
    art = GP(art, m, EGG, EGG_D, seed=nx(), rough=1.0, streak=0.6)
    hx, hy = x + math.cos(ang) * L * .6 - math.cos(pa) * L * .12, y + math.sin(ang) * L * .6 - math.sin(pa) * L * .12
    art = hilite(art, W, H, m, hx, hy, L * .2, L * .05, EGG_L, nx, 0.7)
    cap = shapes(W, H, [petal_pts(x + math.cos(ang) * L * .05, y + math.sin(ang) * L * .05, L * .3, L * .12, ang + d, n=10) for d in (-0.5, 0, 0.5)])
    art = GP(art, cap, LEAF, LEAF_D, seed=nx(), rough=0.8)
    stem = strokes(W, H, [([(x, y), (x - math.cos(ang) * L * .18, y - math.sin(ang) * L * .18)], L * .07, (0, .2))])
    art = GP(art, stem, LEAF_D, seed=nx(), rough=0.6)
    return art


def cabbage(art, W, H, x, y, r, rng, nx):
    base = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 0.85, 12), rng, 1, 0.06))
    art = GP(art, base, CAB, CAB_D, seed=nx(), rough=1.4, streak=0.8)
    for k in range(6):
        a0 = rng.uniform(0, math.tau)
        rr = r * (0.95 - k * 0.12)
        arc = arc_pts(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3), rr, a0, a0 + rng.uniform(1.6, 2.6), 20, 0.85)
        art = GP(art, strokes(W, H, [(arc, 3.0, (0.1, 0.3))]) * base, CAB_D, seed=nx(), rough=0.6)
    art = hilite(art, W, H, base, x - r * .3, y - r * .35, r * .4, r * .2, CAB_L, nx, 0.6)
    veins = [([(x, y + r * .3), (x + math.cos(a) * r * .9, y + r * .3 + math.sin(a) * r * .6)], 1.6, (0, .5)) for a in np.linspace(-2.6, -0.5, 5)]
    art = GP(art, strokes(W, H, veins) * base * 0.6, "#e8f2c6", seed=nx(), rough=0.5)
    return art


def radish(art, W, H, x, y, r, ang, rng, nx):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * 0.9, 12), rng, 1, 0.05))
    root = strokes(W, H, [([(x + math.cos(ang) * r * .7, y + math.sin(ang) * r * .7), (x + math.cos(ang) * r * 2.0, y + math.sin(ang) * r * 2.0)], r * .2, (0, 0.9))])
    art = GP(art, root, "#f2e4d8", seed=nx(), rough=0.5)
    art = GP(art, m, RAD, RAD_D, seed=nx(), rough=1)
    art = hilite(art, W, H, m, x - r * .3, y - r * .3, r * .3, r * .18, "#f39bb0", nx, 0.7)
    lv = [deform(petal_pts(x, y, r * 2.2, r * 0.7, ang + math.pi + d, n=12), rng, 1, 0.06) for d in (-0.4, 0.1, 0.5)]
    art = GP(art, shapes(W, H, lv), LEAF_L, LEAF, seed=nx(), rough=1)
    return art


def leaf_shape(x, y, L, a, w=0.35):
    return petal_pts(x, y, L, L * w, a, n=12, cup=0.1)


if "basket" in PARTS:
    W, H = 640, 520
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    # back handle
    handle = strokes(W, H, [(arc_pts(320, 300, 230, math.pi * 1.06, math.pi * 1.94, 40, 0.95), 16, None)])
    art = GP(art, handle, WICK, WICK_D, seed=nx(), rough=1.2, streak=1.2)
    tw = strokes(W, H, [([(p[0] - 5, p[1] - 5), (p[0] + 5, p[1] + 5)], 3, None) for p in arc_pts(320, 300, 230, math.pi * 1.07, math.pi * 1.93, 30, 0.95)])
    art = GP(art, tw * handle, WICK_D, seed=nx(), rough=0.5)
    # produce (back to front)
    art = cabbage(art, W, H, 240, 270, 88, rng, nx)
    # carrots stand up behind, tips down inside the basket
    for x, y, L, a in [(372, 190, 170, 1.2), (428, 172, 180, 1.45), (486, 196, 165, 1.75)]:
        art = carrot(art, W, H, x, y, L, a, rng, nx)
    clear()
    art = eggplant(art, W, H, 120, 250, 150, 0.35, rng, nx)
    art = radish(art, W, H, 520, 296, 32, -0.5, rng, nx)
    art = radish(art, W, H, 556, 316, 28, -0.2, rng, nx)
    for x, y, r in [(300, 292, 46), (372, 306, 42), (208, 300, 40)]:
        art = tomato(art, W, H, x, y, r, rng, nx)
    clear()
    # basket body: trapezoid, woven rows
    body = [(70, 330), (590, 330), (540, 500), (120, 500)]
    bm = shapes(W, H, [body], smooth=False)
    art = GP(art, bm, WICK, WICK_L, seed=nx(), rough=1.4, streak=1.2)
    weave = []
    for r_ in range(6):
        yy = 344 + r_ * 27
        for c in range(22):
            xx = 80 + c * 24 + (12 if r_ % 2 else 0)
            weave.append(([(xx - 9, yy - 8), (xx + 9, yy + 8)], 6.5, None))
    art = GP(art, strokes(W, H, weave) * bm, WICK_L, seed=nx(), rough=0.8, streak=1)
    gaps = strokes(W, H, [([(80, 344 + r_ * 27 + 13), (580, 344 + r_ * 27 + 13)], 2.4, None) for r_ in range(6)])
    art = GP(art, gaps * bm * 0.8, WICK_D, seed=nx(), rough=0.5)
    shade = bm * np.clip((np.arange(W)[None, :] - 400) / 200, 0, 1)
    art = G(art, shade * 0.7, WICK_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    rim = strokes(W, H, [([(62, 332), (598, 332)], 18, None)])
    art = GP(art, rim, WICK_D, WICK, seed=nx(), rough=1.2, streak=1.2)
    art = GP(art, strokes(W, H, [([(66 + k * 14, 326), (76 + k * 14, 338)], 3, None) for k in range(38)]) * rim, WICK_L, seed=nx(), rough=0.5)
    pv(art, "ks-basket")
    save(art, f"{OUT}/basket.webp", max_w=520, quality=80)
    clear()

if "can" in PARTS:
    W, H = 420, 300
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    body = [(110, 90), (250, 90), (262, 270), (98, 270)]
    bm = shapes(W, H, [body], smooth=False)
    spout = shapes(W, H, [[(240, 220), (372, 92), (384, 104), (258, 248)]], smooth=False)
    rose = shape_mask(W, H, ellipse_pts(386, 92, 20, 12, 12, -0.8))
    handle = strokes(W, H, [(arc_pts(180, 96, 72, math.pi * 1.05, math.pi * 1.95, 30, 0.7), 12, None)])
    sideh = strokes(W, H, [(curve([(104, 120), (60, 150), (64, 210), (100, 236)], 20), 11, None)])
    for m, c1, c2 in [(handle, ZINC, ZINC_D), (sideh, ZINC, ZINC_D), (spout, ZINC, ZINC_D), (bm, ZINC, ZINC_L), (rose, ZINC_D, ZINC)]:
        art = GP(art, m, c1, c2, seed=nx(), rough=1.0, streak=1.2)
    ribs = strokes(W, H, [([(104, y), (258, y)], 4, None) for y in (110, 250)])
    art = GP(art, ribs * bm, ZINC_D, seed=nx(), rough=0.5)
    sh = bm * np.clip((np.arange(W)[None, :] - 200) / 60, 0, 1)
    art = G(art, sh * 0.6, "#5d6e79", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = GP(art, strokes(W, H, [([(130, 126), (126, 240)], 9, (0.2, 0.2))]) * bm * 0.7, "#eef3f5", seed=nx(), rough=0.5)
    holes = circles(W, H, [(386 + dx, 92 + dy, 1.8) for dx, dy in [(-6, -4), (0, 0), (6, 4), (-4, 4), (4, -4), (8, -2), (-8, 2)]])
    art = GP(art, holes, "#4d5c66", seed=nx(), rough=0.2)
    # water drops
    drops = [shape_mask(W, H, [(x, y - 7), (x + 4, y + 2), (x, y + 6), (x - 4, y + 2)]) for x, y in [(398, 130), (408, 158), (392, 176), (414, 196)]]
    for d in drops:
        art = GP(art, d, "#7fb6d6", "#a9d2ea", seed=nx(), rough=0.6)
    pv(art, "ks-can")
    save(art, f"{OUT}/can.webp", max_w=300, quality=82)

if "stake" in PARTS:
    W, H = 400, 700
    rng = random.Random(13); nx = Seq(1300)
    art = blank(W, H)
    board = [(30, 40), (370, 30), (376, 300), (24, 310)]
    post = [(176, 290), (226, 290), (222, 620), (201, 690), (180, 620)]
    pm = shapes(W, H, [post], smooth=False)
    art = GP(art, pm, WOOD_D, WOOD, seed=nx(), rough=1.2, streak=1.5)
    bmask = shapes(W, H, [board], smooth=False)
    art = GP(art, bmask, WOOD_L, WOOD, seed=nx(), rough=1.4, streak=1.6)
    grain = []
    for k in range(16):
        y = rng.uniform(50, 295)
        grain.append((curve([(36, y), (140, y + rng.uniform(-4, 4)), (260, y + rng.uniform(-5, 5)), (366, y + rng.uniform(-3, 3))], 20), rng.uniform(1.0, 2.0), (0.1, 0.1)))
    art = GP(art, strokes(W, H, grain) * bmask * 0.5, WOOD, seed=nx(), rough=0.6)
    knot = ellipses(W, H, [(310, 250, 12, 6, -3)])
    art = GP(art, knot * 0.7, WOOD_D, seed=nx(), rough=0.6)
    edge = bmask - gaussian_filter(bmask, 4) * 0
    rim = np.clip(bmask - np.clip(gaussian_filter(bmask, 5) * 1.6 - 0.6, 0, 1), 0, 1)
    art = G(art, rim * 0.9, WOOD_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    nails = circles(W, H, [(200, 70, 7), (200, 278, 7)])
    art = GP(art, nails, "#6c6a66", "#9a9894", seed=nx(), rough=0.4)
    # twine wrapped on the post
    tw = strokes(W, H, [([(172, 340 + k * 9), (230, 334 + k * 9)], 4, None) for k in range(4)])
    art = GP(art, tw, "#d9c49a", "#bfa676", seed=nx(), rough=0.6)
    pv(art, "ks-stake")
    save(art, f"{OUT}/stake.webp", max_w=300, quality=82)

if "bed" in PARTS:
    W, H = 900, 300
    rng = random.Random(17); nx = Seq(1700)
    art = blank(W, H)
    soil = shapes(W, H, [[(0, 150)] + [(x, 140 + 8 * math.sin(x / 37) + rng.uniform(-3, 3)) for x in range(0, W + 1, 30)] + [(W, 150), (W, 200), (0, 200)]])
    art = GP(art, soil, SOIL, SOIL_D, seed=nx(), rough=2, streak=0.6)
    # plants: lettuces, carrot tops, onion blades, a tomato cane
    for k in range(18):
        x = 30 + k * 50 + rng.uniform(-10, 10)
        kind = k % 3
        if kind == 0:
            lv = [deform(leaf_shape(x, 150, rng.uniform(34, 46), -math.pi / 2 + d, 0.6), rng, 1, 0.08) for d in (-1.0, -0.5, 0, 0.5, 1.0)]
            art = GP(art, shapes(W, H, lv), CAB, LEAF, seed=nx(), rough=1.2, streak=0.8)
            art = GP(art, shapes(W, H, [deform(leaf_shape(x, 150, 24, -math.pi / 2 + d, 0.6), rng, 1, 0.08) for d in (-0.4, 0.4)]), CAB_L, seed=nx(), rough=1)
        elif kind == 1:
            tops = [(curve([(x, 150), (x + math.cos(a) * 20, 150 + math.sin(a) * 30), (x + math.cos(a) * 30, 150 + math.sin(a) * 52)], 8), 3.5, (0, .5)) for a in np.linspace(-2.3, -0.8, 5)]
            art = GP(art, strokes(W, H, tops), LEAF, LEAF_D, seed=nx(), rough=0.8)
            fr = []
            for a in np.linspace(-2.3, -0.8, 5):
                for t in (0.5, 0.75, 0.95):
                    px, py = x + math.cos(a) * 30 * t, 150 + math.sin(a) * 52 * t
                    fr.append(([(px - 5, py), (px + 5, py - 3)], 2.2, None))
            art = GP(art, strokes(W, H, fr), LEAF_L, seed=nx(), rough=0.6)
            art = GP(art, ellipses(W, H, [(x, 154, 8, 5, 0)]), CAR, seed=nx(), rough=0.5)
        else:
            bl = [(curve([(x + d * 4, 152), (x + d * 8, 120), (x + d * 14, 92 + abs(d) * 6)], 8), 4, (0, .6)) for d in (-1, 0, 1)]
            art = GP(art, strokes(W, H, bl), "#7aa64a", LEAF_D, seed=nx(), rough=0.7)
    clear()
    # wooden boards in front
    for row, (y0, y1) in enumerate([(176, 232), (232, 290)]):
        board = shapes(W, H, [[(-6, y0), (W + 6, y0 + 2), (W + 6, y1), (-6, y1 - 1)]], smooth=False)
        art = GP(art, board, WOOD if row == 0 else WOOD_D, WOOD_L if row == 0 else WOOD, seed=nx(), rough=1.4, streak=1.8)
        gr = [(curve([(0, y0 + rng.uniform(8, y1 - y0 - 8)), (W / 2, y0 + rng.uniform(8, y1 - y0 - 8)), (W, y0 + rng.uniform(8, y1 - y0 - 8))], 20), 1.4, (0.05, 0.05)) for _ in range(5)]
        art = GP(art, strokes(W, H, gr) * board * 0.5, WOOD_D, seed=nx(), rough=0.6)
        art = GP(art, strokes(W, H, [([(0, y1 - 1), (W, y1 - 1)], 3, None)]) * 0.6, "#5e3f22", seed=nx(), rough=0.6)
    posts = shapes(W, H, [rect(x, 170, x + 22, 292) for x in (10, 440, 868)], smooth=False)
    art = GP(art, posts, WOOD_D, "#6e4a2a", seed=nx(), rough=1, streak=1.2)
    art = GP(art, circles(W, H, [(x + 11, y, 3.5) for x in (10, 440, 868) for y in (192, 262)]), "#504a44", seed=nx(), rough=0.3)
    pv(art, "ks-bed")
    save(art, f"{OUT}/bed.webp", max_w=780, quality=78)
    clear()

if "wild" in PARTS:
    W, H = 380, 380
    rng = random.Random(23); nx = Seq(2300)
    art = blank(W, H)
    stems, flowers = [], []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.24 + rng.uniform(-.06, .06)
        L = rng.uniform(140, 210)
        x1, y1 = 190 + math.cos(a) * L, 360 + math.sin(a) * L
        stems.append((curve([(190, 360), (190 + math.cos(a) * L * .5 + rng.uniform(-10, 10), 360 + math.sin(a) * L * .5), (x1, y1)], 12), 2.4, (0, .1)))
        flowers.append((x1, y1, k % 3))
    art = GP(art, strokes(W, H, stems), LEAF, LEAF_D, seed=nx(), rough=0.8)
    lv = [deform(leaf_shape(190 + rng.uniform(-30, 30), 340 - rng.uniform(0, 100), rng.uniform(34, 52), -math.pi / 2 + rng.choice([-1, 1]) * rng.uniform(0.5, 1.1), 0.28), rng, 1, .05) for _ in range(12)]
    art = GP(art, shapes(W, H, lv), LEAF_L, LEAF, seed=nx(), rough=0.9)
    for x, y, kind in flowers:
        if kind == 0:  # daisy
            pet = shapes(W, H, petal_ring(x, y, 26, 12, 0.3, rng.uniform(0, 1), 0.05, rng))
            art = GP(art, pet, "#fbf7ee", "#d9ccae", seed=nx(), rough=0.8)
            art = GP(art, circles(W, H, [(x, y, 8)]), "#f1b62e", "#d9921e", seed=nx(), rough=0.5)
        elif kind == 1:  # poppy
            pet = shapes(W, H, [deform(ellipse_pts(x + math.cos(a) * 12, y + math.sin(a) * 12, 18, 14, 10, a), rng, 1, .1) for a in np.linspace(0, math.tau, 5)[:-1] + 0.3])
            art = GP(art, pet, TOM, TOM_D, seed=nx(), rough=1)
            art = GP(art, circles(W, H, [(x, y, 6)]), "#2c2320", seed=nx(), rough=0.4)
        else:  # cornflower
            pet = shapes(W, H, petal_ring(x, y, 22, 9, 0.38, rng.uniform(0, 1), 0.08, rng))
            art = GP(art, pet, "#4f7fd0", "#3a5fae", seed=nx(), rough=0.9)
            art = GP(art, circles(W, H, [(x, y, 4)]), "#2b3f7a", seed=nx(), rough=0.4)
    tie = strokes(W, H, [([(176, 330), (204, 326)], 7, None), (curve([(190, 328), (170, 350), (160, 372)], 8), 3, None), (curve([(192, 328), (214, 348), (226, 366)], 8), 3, None)])
    art = GP(art, tie, "#d9c49a", "#bfa676", seed=nx(), rough=0.5)
    pv(art, "ks-wild")
    save(art, f"{OUT}/wild.webp", max_w=260, quality=82)

if "icons" in PARTS:
    W, H = 200, 200
    rng = random.Random(29)
    nx = Seq(2900)
    a = carrot(blank(W, H), W, H, 70, 60, 140, 0.9, rng, nx)
    pv(a, "ks-carrot"); save(a, f"{OUT}/carrot.webp", max_w=96, quality=84)
    t = tomato(blank(W, H), W, H, 100, 110, 70, rng, nx)
    pv(t, "ks-tomato"); save(t, f"{OUT}/tomato.webp", max_w=96, quality=84)
    p = blank(W, H)
    pod = shape_mask(W, H, [(30, 140), (70, 80), (130, 50), (175, 40), (150, 80), (100, 130), (50, 160)])
    p = GP(p, pod, LEAF_L, LEAF, seed=nx(), rough=1)
    p = GP(p, circles(W, H, [(60 + k * 22, 128 - k * 19, 13) for k in range(5)]), "#a9d06a", LEAF, seed=nx(), rough=0.8)
    p = hilite(p, W, H, pod, 120, 60, 30, 6, "#d6eaa6", nx)
    pv(p, "ks-pea"); save(p, f"{OUT}/pea.webp", max_w=96, quality=84)

kb(OUT)
