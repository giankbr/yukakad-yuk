"""Kampung Naga — Sundanese adat village in a valley near Tasikmalaya: rows of identical stilt houses with thick black
ijuk roofs and whitewashed woven-bamboo walls, terraced paddies, the Ciwulan river, stone stairs down the slope, misty
forested hills. Transparent watercolour with gouache whitewash.
Run: python3 -I kampung-naga.py [part ...]  parts: lembah imah sawah divider batu
Assets -> public/themes/art/kampung-naga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o1_lib import *

OUT = outdir("kampung-naga")
PARTS = sys.argv[1:] or ["lembah", "imah", "sawah", "divider", "batu"]
IJUK, IJUK_D, IJUK_L = "#2e2622", "#1b1613", "#5a4a3e"
KAPUR, KAPUR_D = "#f3efe4", "#d9d2bf"
WOOD, WOOD_D = "#7a5434", "#4c321e"
STONE, STONE_D = "#8f8a7e", "#5f5b52"
LEAF, LEAF_D, LEAF_L = "#5f7f3a", "#3c5a2a", "#9cb25a"
PADDY, PADDY_L = "#8fae48", "#c3d27a"
WATER, WATER_D = "#8fb5b0", "#5f8f8a"
MIST = "#e7ebe2"


def house(art, W, H, cx, by, w, nx, rng, detail=1.0, face=1):
    """One Kampung Naga house (long side): stone footings, short stilts, whitewashed anyaman walls, a door, a heavy
    black ijuk gable roof with fibre strokes and small crossed ridge-horns (capit gunting)."""
    s = w / 100.0
    hb = 40 * s          # wall height
    st = 9 * s           # stilt height
    fy = by - st         # floor line
    wy = fy - hb         # wall top
    x0, x1 = cx - w / 2, cx + w / 2
    # footing stones + stilts
    stones = [ellipse_pts(x, by - 1.5 * s, 5 * s, 3 * s, 10) for x in np.linspace(x0 + 5 * s, x1 - 5 * s, 5)]
    art = G(art, shapes(W, H, stones), STONE, STONE_D, seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1.2, feather=0.8)
    posts = strokes(W, H, [([(x, fy), (x, by - 3 * s)], 3.2 * s, None) for x in np.linspace(x0 + 5 * s, x1 - 5 * s, 5)])
    art = G(art, posts, WOOD_D, seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    # under-floor shadow
    art = G(art, shapes(W, H, [rect(x0 + 2 * s, fy, x1 - 2 * s, fy + st * 0.5)], smooth=False), "#3a3a32", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
    # walls
    wall = shapes(W, H, [rect(x0 + 3 * s, wy, x1 - 3 * s, fy)], smooth=False)
    art = GP(art, wall, KAPUR, mix(KAPUR, KAPUR_D, 0.4), seed=nx(), rough=0.8 * max(1, s), streak=0.4)
    if detail > 0.5:
        # anyaman sasag weave: fine diagonal cross-hatch, faint
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        p = max(2.5, 3.4 * s)
        weave = ((np.abs(((xx + yy) / p) % 2 - 1) < 0.22) | (np.abs(((xx - yy) / p) % 2 - 1) < 0.22)).astype(np.float32) * wall
        art = G(art, weave, KAPUR_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.4)
    # floor beam + corner posts
    beam = strokes(W, H, [([(x0 + 1 * s, fy), (x1 - 1 * s, fy)], 3.2 * s, None), ([(x0 + 3.5 * s, wy), (x0 + 3.5 * s, fy)], 2.4 * s, None), ([(x1 - 3.5 * s, wy), (x1 - 3.5 * s, fy)], 2.4 * s, None)])
    art = G(art, beam, WOOD, WOOD_D, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6, feather=0.6)
    # door + window (dark openings with a wooden frame)
    dx = cx + face * 18 * s
    door = shapes(W, H, [rect(dx - 7 * s, wy + 10 * s, dx + 7 * s, fy - 1 * s)], smooth=False)
    art = G(art, door, "#5e4330", "#3e2a1c", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6)
    win = shapes(W, H, [rect(cx - face * 22 * s - 6 * s, wy + 12 * s, cx - face * 22 * s + 6 * s, wy + 22 * s)], smooth=False)
    art = G(art, win, "#3a2c22", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6)
    if detail > 0.5:
        bars = strokes(W, H, [([(cx - face * 22 * s + k * 3 * s, wy + 12 * s), (cx - face * 22 * s + k * 3 * s, wy + 22 * s)], 0.9 * s, None) for k in (-1, 0, 1)])
        art = OV(art, bars, lambda q: flat(q, "#b89a74", 0.9))
        # small bamboo step to the door
        step = shapes(W, H, [rect(dx - 8 * s, by - 6 * s, dx + 8 * s, by - 3.5 * s)], smooth=False)
        art = G(art, step, WOOD, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5)
    # roof: thick ijuk, long side view = trapezoid with a curved heavy eave
    ry = wy - 40 * s
    roof = [(x0 - 11 * s, wy + 6 * s), (x0 + 6 * s, ry + 2 * s), (x1 - 6 * s, ry), (x1 + 11 * s, wy + 6 * s),
            (x1 + 8 * s, wy + 10 * s), (cx, wy + 11 * s), (x0 - 8 * s, wy + 10 * s)]
    rm = shapes(W, H, [roof], smooth=False)
    rm = displace(rm, nx(), 1.0 * max(1, s * 0.6), 10)
    art = knockout(art, rm, 1.0, 0.5)
    art = G(art, rm, IJUK, IJUK_D, seed=nx(), density=0.97, edge=0.35, bloom=0.08, gran=0.35, rough=1.0, feather=0.6, mottle=0.3)
    # fibre strokes running down the slope, lighter at the top where light hits
    fib = []
    for k in range(int(70 * detail * s) + 12):
        t = rng.random()
        xt = x0 + 6 * s + (x1 - x0 - 12 * s) * t
        xb = x0 - 11 * s + (x1 - x0 + 22 * s) * t
        y0 = ry + rng.uniform(0, 8) * s
        fib.append(([(xt, y0), (xt + (xb - xt) * 0.6, y0 + (wy + 6 * s - y0) * 0.6), (xb + rng.uniform(-2, 2) * s, wy + 8 * s + rng.uniform(-1, 2) * s)], rng.uniform(0.5, 1.1) * s, (0.1, 0.4)))
    art = OV(art, strokes(W, H, fib) * rm, lambda q: flat(q, IJUK_L, 0.55))
    top = strokes(W, H, [([(x0 + 6 * s, ry + 2 * s), (x1 - 6 * s, ry)], 3.2 * s, None)])
    art = G(art, top, IJUK_D, seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5)
    eave = strokes(W, H, [([(x0 - 9 * s, wy + 8 * s), (cx, wy + 9.5 * s), (x1 + 9 * s, wy + 8 * s)], 2.6 * s, (0.05, 0.05))]) * dilate(rm, 0.5)
    art = G(art, eave, "#6b5a40", "#54462f", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6)
    sheen = shapes(W, H, [[(x0 + 6 * s, ry + 3 * s), (x1 - 6 * s, ry + 1 * s), (x1 - 4 * s, ry + 10 * s), (x0 + 4 * s, ry + 12 * s)]]) * rm
    art = OV(art, sheen, lambda q: flat(q, "#8a7a6a", 0.22))
    # crossed ridge horns
    horns = []
    for ex, d in [(x0 + 6 * s, -1), (x1 - 6 * s, 1)]:
        horns.append(([(ex - d * 2 * s, ry + 3 * s), (ex + d * 4 * s, ry - 5 * s)], 1.5 * s, (0.0, 0.4)))
        horns.append(([(ex + d * 1 * s, ry + 3 * s), (ex - d * 2 * s, ry - 5 * s)], 1.5 * s, (0.0, 0.4)))
    art = G(art, strokes(W, H, horns), IJUK_D, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.4)
    # eave shadow on the wall
    sh = shapes(W, H, [rect(x0 + 3 * s, wy + 6 * s, x1 - 3 * s, wy + 14 * s)], smooth=False)
    art = G(art, sh, "#6a6a5e", seed=nx(), density=0.35, edge=0, bloom=0.1, rough=1)
    return art


def tree_clump(art, W, H, cx, by, r, nx, rng, col=LEAF, col2=LEAF_D, n=9):
    blobs = [deform(ellipse_pts(cx + rng.gauss(0, r * 0.5), by - r * 0.8 + rng.gauss(0, r * 0.35), r * rng.uniform(0.4, 0.65), r * rng.uniform(0.35, 0.55), 12), rng, 2, 0.15) for _ in range(n)]
    m = shapes(W, H, blobs)
    art = G(art, m, col, col2, seed=nx(), density=0.8, edge=0.5, bloom=0.35, rough=4, gran=0.3)
    dark = shapes(W, H, [deform(ellipse_pts(cx + rng.gauss(r * 0.2, r * 0.3), by - r * 0.5, r * 0.45, r * 0.3, 10), rng, 2, 0.15) for _ in range(3)]) * m
    art = G(art, dark, col2, seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=3)
    return art


def bamboo_clump(art, W, H, bx, by, h, nx, rng, side=1):
    items = []
    for k in range(7):
        x = bx + rng.uniform(-14, 14)
        lean = side * rng.uniform(0.05, 0.35)
        items.append((curve([(x, by), (x + lean * h * 0.4, by - h * 0.6), (x + lean * h, by - h)], 16), rng.uniform(2.5, 4), (0.0, 0.7)))
    art = G(art, strokes(W, H, items), "#6f8a3c", "#4f6a2c", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    lv = []
    for (pts, _, _) in items:
        for j in range(5, 16, 2):
            x, y = pts[j]
            for d in (-1, 1):
                a = math.pi / 2 + d * rng.uniform(0.6, 1.3) + side * 0.2
                lv.append(blade(W, H, curve([(x, y), (x + math.cos(a) * 12, y + math.sin(a) * 6 + 4), (x + math.cos(a) * 22, y + math.sin(a) * 14 + 8)], 8), 3.2))
    art = G(art, shapes(W, H, lv), LEAF, LEAF_D, seed=nx(), density=0.75, edge=0.4, bloom=0.2, rough=1.5)
    return art


def palm_tree(art, W, H, x, by, h, nx, rng, lean=0.1):
    art = G(art, palm(W, H, x, by, h, rng, lean), "#56703a", "#3e552c", seed=nx(), density=0.8, edge=0.3, bloom=0.1, rough=1.2, feather=0.7)
    return art


def lembah():
    """Cover valley (portrait). Top ~40% is pale misty sky for the names."""
    W, H = 720, 1260
    rng = random.Random(11); nx = Seq(100)
    art = painted_sky(W, H, [(0, "#f4f3ec"), (0.3, "#eef0e8"), (0.42, "#e3e9e0"), (0.6, "#d6e0d6"), (1, "#c9d6c8")], seed=3, streak=0.5)
    # far ridges (misty blue-green), layered
    for (y, amp, col, col2, dens, sd) in [(580, 80, "#bccbc4", "#aabdb6", 0.55, 1), (650, 60, "#a3b8a9", "#8ea898", 0.65, 2)]:
        m = hills(W, H, y, amp, sd, 0.6)
        art = G(art, m, col, col2, seed=nx(), density=dens, edge=0.35, bloom=0.4, rough=6, gran=0.25)
        mist = np.clip(1 - np.abs(np.arange(H)[:, None] - (y + 40)) / 50, 0, 1) * np.ones((1, W)) * (0.6 + 0.4 * fbm(W, H, sd + 9, 90, 2))
        art = OV(art, mist.astype(np.float32), lambda q: flat(q, MIST, 0.55))
        clear()
    # right slope with terraced paddies stepping down toward the village
    slopeR = shapes(W, H, [[(250, 900), (360, 780), (500, 720), (640, 690), (740, 680), (740, 940), (250, 940)]])
    art = G(art, slopeR, "#8aa25a", "#73904a", seed=nx(), density=0.85, edge=0.3, bloom=0.3, rough=4)
    for k in range(8):
        y0 = 708 + k * 26
        xs = np.linspace(300 + max(0, 6 - k) * 26, W + 30, 18)
        top = [(x, y0 + (W - x) * 0.18 + 6 * math.sin(x / 70 + k)) for x in xs]
        bot = [(x, y + 22) for x, y in top[::-1]]
        m = shapes(W, H, [top + bot]) * slopeR
        if k % 3 == 1:
            art = G(art, m, "#d3e2dc", "#b4ccc5", seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=2)
            art = OV(art, strokes(W, H, [([(x, y + 10) for x, y in top], 1.2, (0.3, 0.3))]) * m, lambda q: flat(q, "#f4f7f2", 0.6))
        else:
            art = G(art, m, PADDY if k % 2 else "#a3bd52", "#7f9e3e", seed=nx(), density=0.88, edge=0.45, bloom=0.3, rough=2, gran=0.35)
            rows = strokes(W, H, [([(x, y + 5 + j * 5) for x, y in top], 0.8, None) for j in range(3)]) * m
            art = G(art, rows, "#6a8a34", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
        art = G(art, strokes(W, H, [(top, 2.4, None)]) * dilate(slopeR, 1), "#7d6c4a", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8)
    clear()
    # left slope: forest, and the stone stairs zig-zagging down
    slope = shapes(W, H, [[(-20, 700), (110, 690), (230, 740), (330, 860), (380, 960), (-20, 960)]])
    art = G(art, slope, "#6c8a48", "#557540", seed=nx(), density=0.88, edge=0.3, bloom=0.3, rough=5, gran=0.3)
    for (x, y, r) in [(20, 740, 58), (100, 728, 44), (300, 860, 40), (24, 860, 56)]:
        art = tree_clump(art, W, H, x, y, r, nx, rng, "#5d7c3c", "#3e5a2c")
    steps = []
    for k in range(20):
        t = k / 19
        x = 120 + t * 160 + 34 * math.sin(t * 9)
        y = 720 + t * 180
        wd = 18 + t * 12
        steps.append(rect(x - wd / 2, y, x + wd / 2, y + 4 + t * 2))
    sm = shapes(W, H, steps, smooth=False)
    art = G(art, sm, "#d6d0bf", "#b3ac99", seed=nx(), density=0.95, edge=0.45, bloom=0, rough=0.8, feather=0.5)
    art = G(art, np.clip(np.roll(sm, 3, 0) - sm, 0, 1), STONE_D, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.5)
    clear()
    # the village terrace
    ground = shapes(W, H, [[(60, 920), (330, 890), (600, 900), (740, 920), (740, 1060), (-20, 1060), (-20, 960)]])
    art = G(art, ground, "#b9ae8a", "#a69a76", seed=nx(), density=0.85, edge=0.35, bloom=0.3, rough=3)
    art = G(art, ground * np.clip((np.arange(H)[:, None] - 990) / 60, 0, 1), "#7f9a4a", "#6a8a40", seed=nx(), density=0.8, edge=0.2, bloom=0.2, rough=3)
    for (x, y, r) in [(80, 930, 34), (640, 925, 40), (700, 950, 30)]:
        art = tree_clump(art, W, H, x, y, r, nx, rng, "#6a8a44", "#4a6a34", 7)
    # rows of identical houses, staggered, back row first; a breath of mist between rows
    rows_ = [(930, 58, [190, 290, 390, 490, 585], 0.6), (978, 72, [130, 250, 370, 490, 610], 0.8), (1040, 92, [205, 360, 515], 1.0)]
    for i, (by, w, xs, det) in enumerate(rows_):
        for x in xs:
            art = house(art, W, H, x + rng.uniform(-6, 6), by + rng.uniform(-3, 3), w, nx, rng, det)
        if i < 2:
            band = np.clip(1 - np.abs(np.arange(H)[:, None] - (by + 4)) / 14, 0, 1) * np.ones((1, W)) * (0.5 + 0.5 * fbm(W, H, 40 + i, 60, 2))
            art = OV(art, band.astype(np.float32), lambda q: flat(q, MIST, 0.4))
        clear()
    art = bamboo_clump(art, W, H, 40, 1080, 230, nx, rng, side=1)
    art = bamboo_clump(art, W, H, 690, 1075, 190, nx, rng, side=-1)
    clear()
    # Ciwulan river across the bottom with pale boulders
    river = shapes(W, H, [[(-20, 1080), (200, 1072), (420, 1090), (740, 1076), (740, H + 20), (-20, H + 20)]])
    art = G(art, river, WATER, WATER_D, seed=nx(), density=0.82, edge=0.5, bloom=0.45, rough=3, gran=0.3)
    refl = shapes(W, H, [rect(x - 40, 1092, x + 40, 1150) for x in (205, 360, 515)], smooth=False) * river
    art = G(art, refl, "#6f8f86", seed=nx(), density=0.35, edge=0.1, bloom=0.4, rough=6)
    ripple = strokes(W, H, [([(x, y), (x + rng.uniform(30, 70), y + rng.uniform(-1, 1))], 1.6, (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(1100, H)) for _ in range(54)]])
    art = OV(art, ripple * river, lambda q: flat(q, "#eef4ef", 0.7))
    bank = strokes(W, H, [([(-20, 1080), (200, 1072), (420, 1090), (740, 1076)], 9, None)])
    art = G(art, bank, "#6f7a4a", "#55603a", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=3)
    boulders = [deform(ellipse_pts(x, y, rx, rx * 0.5, 12), rng, 2, 0.1) for (x, y, rx) in [(80, 1150, 36), (148, 1180, 20), (520, 1160, 42), (604, 1208, 24), (330, 1222, 30), (690, 1134, 20)]]
    bm = shapes(W, H, boulders)
    art = G(art, bm, "#c4beae", "#9a9484", seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=1.5)
    yy = np.arange(H)[:, None].astype(np.float32)
    art = OV(art, bm * np.clip(1 - (np.roll(bm, -10, 0) > 0.5) * 1.0, 0, 1), lambda q: flat(q, "#f2efe6", 0.55))
    art = G(art, np.clip(bm - np.roll(bm, -6, 0), 0, 1), "#6a665c", seed=nx(), density=0.6, edge=0, bloom=0, rough=1)
    art = add_grain(art, 7, 0.035)
    preview(art, "kn-lembah")
    save_rgb(art, f"{OUT}/lembah.webp", size=(600, 1050), quality=74)


def imah():
    W, H = 420, 350
    rng = random.Random(3); nx = Seq(500)
    art = blank(W, H)
    ground = shapes(W, H, [deform(ellipse_pts(W / 2, H - 22, 190, 16, 16), rng, 2, 0.08)])
    art = G(art, ground, "#a3b56a", "#7f9a4a", seed=nx(), density=0.6, edge=0.5, bloom=0.3, rough=4)
    art = house(art, W, H, W / 2, H - 22, 300, nx, rng, 1.0)
    preview(art, "kn-imah")
    save(art, f"{OUT}/imah.webp", max_w=360, quality=84)


def sawah():
    """Terraced paddy band with a few houses and a palm, transparent top (for closing / countdown bottom)."""
    W, H = 760, 300
    rng = random.Random(5); nx = Seq(700)
    art = blank(W, H)
    hill = hills(W, H, 120, 22, 8, 0.8)
    art = G(art, hill, "#9fb6a6", "#8aa696", seed=nx(), density=0.6, edge=0.4, bloom=0.4, rough=5)
    for k in range(6):
        y = 140 + k * 28
        top = [(x, y + 14 * math.sin(x / 140 + k * 0.6)) for x in np.linspace(-30, W + 30, 30)]
        bot = [(x, y + 30 + 14 * math.sin(x / 140 + k * 0.6)) for x in np.linspace(W + 30, -30, 30)]
        m = shapes(W, H, [top + bot])
        if k % 2:
            art = G(art, m, "#cfe0da", "#b1cbc4", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=2)
        else:
            art = G(art, m, PADDY, "#7f9e3e", seed=nx(), density=0.88, edge=0.45, bloom=0.3, rough=2, gran=0.35)
        art = G(art, strokes(W, H, [(top, 2.2, None)]), "#7a6a48", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8)
    for x, w in [(150, 70), (240, 70), (560, 64)]:
        art = house(art, W, H, x, 150, w, nx, rng, 0.7)
    for (x, y, r) in [(650, 150, 46), (700, 160, 38), (40, 160, 34)]:
        art = tree_clump(art, W, H, x, y, r, nx, rng, "#6a8a44", "#4a6a34", 8)
    preview(art, "kn-sawah")
    save(art, f"{OUT}/sawah.webp", max_w=720, quality=80)


def divider():
    """Three flat river stones on a hairline, like the stepping stones by the Ciwulan."""
    W, H = 440, 70
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    line = strokes(W, H, [([(20, 36), (420, 36)], 2.2, (0.3, 0.3))])
    art = G(art, line, "#5a6646", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.6)
    st = [deform(ellipse_pts(x, 36, rx, rx * 0.5, 12), rng, 2, 0.1) for x, rx in [(180, 20), (220, 26), (262, 18)]]
    m = shapes(W, H, st)
    art = G(art, m, "#a8a291", "#77715f", seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=1.2)
    art = OV(art, m * np.clip(1 - (np.arange(H)[:, None] - 24) / 10, 0, 1), lambda q: flat(q, "#e8e4d8", 0.45))
    for x in (120, 320):
        art = G(art, circles(W, H, [(x, 36, 3)]), "#5f7f3a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5)
    preview(art, "kn-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


def batu():
    W = H = 120
    rng = random.Random(4); nx = Seq(1100)
    m = shapes(W, H, [deform(ellipse_pts(60, 62, 48, 34, 14), rng, 2, 0.1)])
    art = G(blank(W, H), m, "#a8a291", "#77715f", seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=1.6)
    art = OV(art, m * np.clip(1 - (np.arange(H)[:, None] - 34) / 22, 0, 1), lambda q: flat(q, "#e8e4d8", 0.45))
    moss = shapes(W, H, [deform(ellipse_pts(40, 86, 26, 8, 10), rng, 2, 0.2)]) * m
    art = G(art, moss, LEAF, seed=nx(), density=0.7, edge=0.4, bloom=0.3, rough=2)
    preview(art, "kn-batu")
    save(art, f"{OUT}/batu.webp", max_w=72, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
