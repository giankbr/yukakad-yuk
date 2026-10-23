"""Pondok Inggris — English stone cottage garden in loose storybook watercolour: thatched cottage, climbing roses,
hollyhocks, foxgloves, delphiniums, picket gate. Run: python3 -I pondok-inggris.py [part ...]
parts: cottage border vine foxglove rose. Assets -> public/themes/art/pondok-inggris/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h6_lib import *

OUT = outdir("pondok-inggris")
PARTS = sys.argv[1:] or ["cottage", "border", "vine", "foxglove", "rose"]
SAGE, SAGE_D, SAGE_L = "#7d9a6e", "#4b6644", "#a9bf93"
ROSE, ROSE_D, ROSE_L = "#d98a9a", "#a8506a", "#f1c3c8"
FOX, FOX_D = "#c07fb0", "#7c3f78"
DELPH, DELPH_D, DELPH_L = "#6f8fd0", "#3b4f9a", "#a9bde8"
HOLLY, HOLLY_D = "#e9a6b0", "#b85a74"
STONE, STONE_D = "#d9c7a4", "#9f8a6a"
THATCH, THATCH_D = "#c9a36a", "#8a6638"
jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = SAGE_L, SAGE, SAGE_D


def wash(art, m, a, b=None, seed=1, d=0.6, **k):
    k.setdefault("edge", 0.5); k.setdefault("bloom", 0.35); k.setdefault("rough", 5)
    return G(art, m, a, b, seed=seed, density=d, **k)


def foliage(art, W, H, nx, rng, cx, cy, rx, ry, n=26, cols=(SAGE_L, SAGE, SAGE_D)):
    """Loose leafy mass: overlapping deformed blobs in 3 tones (lightest first)."""
    for i, c in enumerate(cols):
        polys = []
        for _ in range(n // (i + 1)):
            x = cx + rng.gauss(0, rx * 0.5); y = cy + rng.gauss(0, ry * 0.5) + i * ry * 0.12
            r = rng.uniform(0.18, 0.32) * min(rx, ry) * (1 - i * 0.2)
            polys.append(deform(ellipse_pts(x, y, r, r * 0.8, 8, rng.uniform(0, 3)), rng, 2, 0.12))
        art = wash(art, shapes(W, H, polys), c, mix(c, "#5f7a4a", 0.3), seed=nx(), d=0.5 + i * 0.1, holes=0.08)
    return art


def small_roses(art, W, H, nx, rng, pts, r=9, cols=(ROSE_L, ROSE, ROSE_D)):
    heads = [deform(ellipse_pts(x, y, r * s, r * s * 0.85, 8, rng.uniform(0, 3)), rng, 1, 0.12) for x, y, s in pts]
    art = wash(art, shapes(W, H, heads), cols[0], cols[1], seed=nx(), d=0.75, edge=0.7, bloom=0.3, rough=2.5, pad=10)
    swirls = []
    for x, y, s in pts:
        a0 = rng.uniform(0, math.tau)
        swirls.append((arc_pts(x, y, r * s * 0.45, a0, a0 + 3.6, 12, 0.85), r * s * 0.22, (0.2, 0.3)))
    return G(art, strokes(W, H, swirls), cols[2], seed=nx(), density=0.7, edge=0.4, bloom=0, rough=1.2, feather=0.6, pad=8)


def spike(W, H, x, by, h, lean, rng):
    """Flower spike stem polyline from base to tip."""
    return curve([(x, by), (x + lean * h * 0.3, by - h * 0.5), (x + lean * h, by - h)], 30)


def foxglove(art, W, H, nx, rng, x, by, h, lean=0.05, col=FOX, deep=FOX_D, s=1.0):
    stem = spike(W, H, x, by, h, lean, rng)
    art = G(art, strokes(W, H, [(stem, 3.2 * s, (0.02, 0.3))]), SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1.2, pad=8)
    bells, spots = [], []
    for j in range(len(stem) - 2, len(stem) // 3, -1):
        t = 1 - j / len(stem)
        px, py = stem[j]
        side = 1 if j % 2 else -1
        L = (13 + 19 * min(1, t * 2.2)) * s
        a = math.pi / 2 + side * 0.9
        bells.append(deform(petal_pts(px, py, L, L * 0.42, a, n=10, cup=0.1), rng, 1, 0.06))
        bx, by_ = px + math.cos(a) * L * 0.75, py + math.sin(a) * L * 0.75
        spots += [(bx + rng.uniform(-2, 2) * s, by_ + rng.uniform(-2, 2) * s, 1.2 * s)]
    m = shapes(W, H, bells)
    art = G(art, m, mix(col, "#ffffff", 0.25), col, seed=nx(), density=0.75, edge=0.75, bloom=0.3, rough=2.2, pad=10)
    art = G(art, circles(W, H, spots), deep, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.5, pad=6)
    for j in range(0, len(stem) // 3, 4):  # basal leaves
        px, py = stem[j]
        art = jw.leaf(art, W, H, px, py, 34 * s, -math.pi / 2 + (1.0 if j % 8 else -1.0) * 1.1, rng, nx)
    return art


def delphinium(art, W, H, nx, rng, x, by, h, lean=0.0, s=1.0):
    stem = spike(W, H, x, by, h, lean, rng)
    art = G(art, strokes(W, H, [(stem, 3 * s, (0.02, 0.3))]), SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1.2, pad=8)
    flor = {0: [], 1: [], 2: []}
    for j in range(len(stem) - 1, len(stem) // 3, -1):
        t = 1 - j / len(stem)
        px, py = stem[j]
        wid = (6 + 14 * min(1, t * 1.8)) * s
        for _ in range(2):
            fx, fy = px + rng.uniform(-wid, wid), py + rng.uniform(-3, 3)
            r = rng.uniform(4.5, 7) * s
            k = rng.choice([0, 1, 1, 2])
            flor[k].append(deform(ellipse_pts(fx, fy, r, r * 0.9, 7, rng.uniform(0, 3)), rng, 1, 0.15))
    for k, (a, b) in enumerate([(DELPH_L, DELPH), (DELPH, "#5a74c0"), (DELPH_D, "#4a5fae")]):
        if flor[k]:
            art = G(art, shapes(W, H, flor[k]), a, b, seed=nx(), density=0.7 + k * 0.08, edge=0.6, bloom=0.3, rough=2, pad=10)
    for j in range(2, len(stem) // 3, 5):
        px, py = stem[j]
        art = jw.leaf(art, W, H, px, py, 26 * s, -math.pi / 2 + (1.2 if j % 2 else -1.2), rng, nx)
    return art


def hollyhock(art, W, H, nx, rng, x, by, h, lean=0.0, s=1.0, col=HOLLY, deep=HOLLY_D):
    stem = spike(W, H, x, by, h, lean, rng)
    art = G(art, strokes(W, H, [(stem, 3.6 * s, (0.02, 0.2))]), SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1.2, pad=8)
    heads, eyes, buds = [], [], []
    for j in range(len(stem) - 1, len(stem) // 4, -3):
        t = 1 - j / len(stem)
        px, py = stem[j]
        side = rng.choice([-1, 1])
        if t < 0.12:
            buds.append((px + side * 3, py, 4 * s)); continue
        r = (9 + 9 * min(1, t * 2)) * s
        cx, cy = px + side * r * 0.55, py
        heads.append(deform(ellipse_pts(cx, cy, r, r * 0.92, 9, rng.uniform(0, 3)), rng, 2, 0.1))
        eyes.append((cx, cy, r * 0.22))
    art = G(art, shapes(W, H, heads), mix(col, "#ffffff", 0.3), col, seed=nx(), density=0.72, edge=0.75, bloom=0.4, rough=2.5, pad=10)
    art = G(art, circles(W, H, eyes), deep, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1, pad=6)
    art = G(art, circles(W, H, buds), SAGE_L, SAGE, seed=nx(), density=0.8, edge=0.4, rough=1, pad=6)
    for j in range(1, len(stem) // 3, 4):
        px, py = stem[j]
        art = jw.leaf(art, W, H, px, py, 30 * s, -math.pi / 2 + (1.3 if j % 2 else -1.3), rng, nx)
    return art


def daisies(art, W, H, nx, rng, pts, r=6):
    for x, y in pts:
        art = jw.white_flower(art, W, H, x, y, r * rng.uniform(0.8, 1.2), rng, nx, petals=8, shade="#a7a1b5")
    return art


def vignette_alpha(arr, seed, cx, cy, rx, ry, soft=0.18):
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    n = (fbm(w, h, seed, 60, 3) - 0.5) * 0.35
    k = np.clip((1 - (d + n)) / soft, 0, 1)
    out = arr.copy(); out[..., 3] *= k
    return out


if "cottage" in PARTS:
    W, H = 820, 900
    nx = Seq(61000); rng = random.Random(61)
    art = blank(W, H)
    # soft sky + background trees
    art = wash(art, shapes(W, H, [deform([(40, 120), (780, 90), (800, 420), (20, 440)], rng, 3, 0.05)]), "#cfdcea", "#e8e2cf", seed=nx(), d=0.35, edge=0.25, bloom=0.5, rough=10)
    art = foliage(art, W, H, nx, rng, 150, 360, 210, 190, n=30, cols=("#b7c79c", "#8fa77c", "#61805a"))
    art = foliage(art, W, H, nx, rng, 700, 330, 190, 210, n=30, cols=("#bccba0", "#93ab80", "#5e7c58"))
    clear()
    # cottage walls (honey stone); trees are knocked out behind the cottage
    wall = shapes(W, H, [[(200, 440), (640, 440), (642, 690), (198, 690)]], smooth=False)
    house = np.maximum.reduce([wall, shapes(W, H, [[(178, 462), (250, 300), (612, 300), (682, 462)], [(536, 236), (594, 236), (594, 380), (536, 380)]], smooth=False)])
    art = knockout(art, house, amount=1.0, grow=2.0)
    art = wash(art, wall, STONE, "#e6d6b6", seed=nx(), d=0.75, edge=0.35, bloom=0.3, rough=2.5)
    stones = []
    for row, y in enumerate(range(452, 690, 17)):
        x = 202 + (row % 2) * 14
        while x < 640:
            w_ = rng.uniform(20, 36)
            stones.append(deform([(x, y), (x + w_ - 3, y + 1), (x + w_ - 4, y + 13), (x + 1, y + 14)], rng, 1, 0.08))
            x += w_
    sel = [p for p in stones if rng.random() < 0.4]
    art = G(art, shapes(W, H, sel), "#c4ad84", "#d8c19a", seed=nx(), density=0.32, edge=0.7, bloom=0.2, rough=1.5, pad=8)
    sel2 = [p for p in stones if rng.random() < 0.18]
    art = G(art, shapes(W, H, sel2), "#a99070", seed=nx(), density=0.35, edge=0.6, bloom=0.1, rough=1.2, pad=8)
    # shadow under eaves
    art = G(art, shapes(W, H, [[(198, 440), (642, 440), (642, 470), (198, 478)]], smooth=False), "#7d6a55", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=3)
    # chimney
    chim = shapes(W, H, [[(540, 250), (584, 250), (586, 380), (538, 380)]], smooth=False)
    art = wash(art, chim, "#c9a27c", "#a7795a", seed=nx(), d=0.8, edge=0.5, rough=1.5)
    art = wash(art, shapes(W, H, [[(532, 240), (592, 240), (592, 256), (532, 256)]], smooth=False), "#8b6448", seed=nx(), d=0.8, rough=1.2)
    art = G(art, strokes(W, H, [(curve([(560, 236), (548, 200), (572, 170), (556, 130), (580, 96)], 30), 14, (0.1, 0.6))]), "#c9cdd6", seed=nx(), density=0.25, edge=0.2, bloom=0.4, rough=6, feather=4)
    # thatched roof with eyebrow dormer
    roof = [(178, 462), (196, 420), (250, 316), (300, 290), (560, 290), (612, 316), (662, 420), (682, 462), (560, 470), (500, 452),
            (470, 410), (440, 398), (410, 410), (380, 452), (320, 470)]
    rm = shapes(W, H, [roof])
    art = wash(art, rm, "#dcbd84", THATCH, seed=nx(), d=0.8, edge=0.55, bloom=0.4, rough=3)
    # thatch strokes
    th = []
    for i in range(140):
        x = rng.uniform(200, 660); y = rng.uniform(300, 450)
        th.append(([(x, y), (x + rng.uniform(-3, 3), y + rng.uniform(14, 30))], rng.uniform(1.2, 2.2), (0.2, 0.4)))
    under = np.clip(rm - np.roll(gaussian_filter(rm, 14), -26, 0) * 1.4, 0, 1) * rm
    art = G(art, under, "#9a7444", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=3)
    art = G(art, strokes(W, H, th) * rm, THATCH_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    ridge = strokes(W, H, [(curve([(250, 318), (300, 298), (560, 298), (612, 318)], 30), 9, None)])
    art = G(art, ridge, "#a77f48", seed=nx(), density=0.6, edge=0.4, rough=1.5)
    eave = strokes(W, H, [(curve([(180, 460), (320, 468), (380, 450), (410, 412), (440, 400), (470, 412), (500, 450), (560, 468), (680, 460)], 60), 7, None)])
    art = G(art, eave, THATCH_D, "#6e4d2a", seed=nx(), density=0.65, edge=0.4, rough=1.5)
    clear()
    # windows: dormer + two lower; small leaded panes
    def window(art, x, y, w, h, arch=False):
        glass = shapes(W, H, [rect(x, y, w, h)], smooth=False)
        art = G(art, glass, "#4e5d6c", "#7f93a2", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=1.2)
        refl = shapes(W, H, [[(x + 4, y + h - 4), (x + w * 0.5, y + 4), (x + w * 0.7, y + 4), (x + w * 0.2, y + h - 4)]], smooth=False)
        art = OV(art, refl * glass, lambda m: rgba_solid(m, "#dfe7ee", 0.35))
        bars = [([(x + w * k / 3, y), (x + w * k / 3, y + h)], 2.2, None) for k in (1, 2)] + [([(x, y + h * k / 2), (x + w, y + h * k / 2)], 2.2, None) for k in (1,)]
        frame = strokes(W, H, bars + [(rect(x, y, w, h) + [(x, y)], 4, None)])
        art = GP(art, frame, "#f7f3ea", "#e8e1d2", seed=nx(), rough=0.6, streak=0.3, pad=6)
        sill = shapes(W, H, [rect(x - 6, y + h, w + 12, 7)], smooth=False)
        return GP(art, sill, "#efe8da", "#cfc5b2", seed=nx(), rough=0.7, pad=6)
    art = window(art, 418, 404, 44, 34)
    art = window(art, 236, 520, 74, 62)
    art = window(art, 486, 520, 84, 62)
    # door (arched, cornflower blue) with stone porch
    dm = shapes(W, H, [[(352, 690)] + arc_pts(380, 560, 28, math.pi, math.tau, 16) + [(408, 690)]], smooth=False)
    art = GP(art, dm, "#5d78a8", "#46608f", seed=nx(), rough=1.0, streak=0.9, pad=8)
    art = G(art, strokes(W, H, [([(380, 540), (380, 688)], 1.6, None), ([(356, 610), (404, 610)], 1.4, None)]), "#2f4268", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = G(art, circles(W, H, [(398, 626, 3)]), "#c9a24e", seed=nx(), density=0.9, edge=0.2, rough=0.4, pad=4)
    # climbing roses: foliage + rose heads up the wall and round the door
    path_l = curve([(338, 690), (334, 600), (346, 532), (380, 508), (414, 532), (424, 600), (420, 690)], 40)
    pts = []
    for i, (x, y) in enumerate(path_l):
        if i % 2 == 0:
            pts.append((x + rng.uniform(-14, 14), y + rng.uniform(-8, 8), rng.uniform(0.7, 1.15)))
    folpoly = [deform(ellipse_pts(x + rng.uniform(-10, 10), y + rng.uniform(-8, 8), rng.uniform(9, 15), rng.uniform(6, 10), 7, rng.uniform(0, 3)), rng, 1, 0.15) for x, y in path_l]
    art = G(art, shapes(W, H, folpoly), SAGE, SAGE_D, seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=2.5, pad=10)
    art = small_roses(art, W, H, nx, rng, pts, r=8)
    # rambler across left wall & under the dormer
    path2 = curve([(206, 690), (214, 600), (230, 500), (300, 488), (360, 480)], 30)
    fol2 = [deform(ellipse_pts(x + rng.uniform(-8, 8), y + rng.uniform(-6, 6), rng.uniform(8, 13), rng.uniform(5, 9), 7, rng.uniform(0, 3)), rng, 1, 0.15) for x, y in path2]
    art = G(art, shapes(W, H, fol2), SAGE_L, SAGE, seed=nx(), density=0.7, edge=0.55, bloom=0.3, rough=2.5, pad=10)
    art = small_roses(art, W, H, nx, rng, [(x + rng.uniform(-8, 8), y + rng.uniform(-6, 6), rng.uniform(0.6, 1)) for x, y in path2[::3]], r=8, cols=("#f6dcd8", "#e7a9b0", "#b56679"))
    clear()
    # hollyhocks against the right wall
    art = hollyhock(art, W, H, nx, rng, 604, 700, 300, -0.04)
    art = hollyhock(art, W, H, nx, rng, 630, 700, 250, 0.05, col="#f4d9a0", deep="#c08a3a")
    art = hollyhock(art, W, H, nx, rng, 216, 700, 230, -0.05, col="#e9b2c6", deep="#9c4a6e")
    clear()
    # garden ground + path to the gate
    ground = shapes(W, H, [deform([(40, 680), (780, 676), (800, 860), (20, 860)], rng, 2, 0.04)])
    art = wash(art, ground, "#a9bf8b", "#7f9c6a", seed=nx(), d=0.55, edge=0.3, bloom=0.5, rough=8)
    pathm = shapes(W, H, [[(360, 690), (400, 690), (468, 860), (300, 860)]])
    art = wash(art, pathm, "#e2d4b8", "#cdb995", seed=nx(), d=0.85, edge=0.5, bloom=0.3, rough=4)
    flag = [deform(ellipse_pts(rng.uniform(320, 450) - 0, y, rng.uniform(14, 22), 6 + (y - 690) / 30, 8), rng, 1, 0.1) for y in range(704, 860, 22)]
    art = G(art, shapes(W, H, flag) * pathm, "#b8a37f", seed=nx(), density=0.5, edge=0.7, bloom=0.2, rough=1.5)
    # border beds: foxgloves left, delphiniums right, daisies & lavender along the front
    art = foliage(art, W, H, nx, rng, 150, 760, 170, 80, n=26)
    art = foliage(art, W, H, nx, rng, 670, 760, 170, 80, n=26)
    for x, h, ln in [(70, 300, 0.06), (112, 360, 0.02), (160, 300, -0.03), (250, 240, -0.06)]:
        art = foxglove(art, W, H, nx, rng, x, 800, h, ln, s=1.05)
    clear()
    art = foxglove(art, W, H, nx, rng, 200, 820, 260, 0.04, col="#e8c8d8", deep="#a0628a")
    for x, h, ln in [(560, 230, 0.05), (640, 330, 0.01), (700, 380, -0.02), (760, 300, -0.06)]:
        art = delphinium(art, W, H, nx, rng, x, 800, h, ln, s=1.05)
    clear()
    lav = []
    for x in list(range(40, 300, 9)) + list(range(500, 790, 9)):
        y = 820 + rng.uniform(-10, 10)
        lav.append((curve([(x, y), (x + rng.uniform(-8, 8), y - rng.uniform(30, 52))], 8), 3.5, (0.4, 0.2)))
    art = G(art, strokes(W, H, lav), "#a593cc", "#7f6aae", seed=nx(), density=0.6, edge=0.5, bloom=0.2, rough=1.5, feather=0.7)
    art = daisies(art, W, H, nx, rng, [(rng.uniform(30, 300), rng.uniform(800, 850)) for _ in range(9)] + [(rng.uniform(510, 790), rng.uniform(800, 850)) for _ in range(9)])
    clear()
    # picket fence + gate (white gouache with lilac-grey shadow)
    pick = []
    for x in list(range(14, 296, 26)) + list(range(512, 806, 26)):
        pick.append([(x, 868), (x, 802), (x + 8, 790), (x + 16, 802), (x + 16, 868)])
    gate = []
    for k in range(6):
        x = 304 + k * 34
        top = 776 - 18 * math.sin(math.pi * (k + 0.5) / 6)
        gate.append([(x, 868), (x, top + 12), (x + 9, top), (x + 18, top + 12), (x + 18, 868)])
    rails = [rect(0, 812, 300, 9), rect(510, 812, 310, 9), rect(0, 846, 300, 9), rect(510, 846, 310, 9), rect(300, 806, 212, 10), rect(300, 846, 212, 10)]
    posts = [rect(292, 762, 16, 106), rect(504, 762, 16, 106)]
    fm = shapes(W, H, pick + gate + rails + posts, smooth=False)
    art = G(art, np.roll(np.roll(fm, 4, 1), 3, 0) * 0.9, "#8c86a6", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1.5, feather=1.5)
    art = GP(art, fm, "#fbf8f0", "#ebe5d8", seed=nx(), rough=1.0, streak=0.5, pad=8)
    sh = np.clip(fm - np.roll(fm, -3, 1), 0, 1)
    art = G(art, sh, "#a29ab5", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    art = small_roses(art, W, H, nx, rng, [(300, 764, 1.0), (318, 776, 0.8), (512, 760, 1.05), (494, 772, 0.8), (520, 780, 0.7)], r=10)
    art = vignette_alpha(art, 77, W / 2, H * 0.53, W * 0.6, H * 0.6, soft=0.22)
    preview6(art, "pi-cottage")
    save(art, f"{OUT}/cottage.webp", max_w=580, quality=70)
    clear()

if "border" in PARTS:
    # wide flower border strip (countdown top / closing)
    W, H = 1100, 380
    nx = Seq(62000); rng = random.Random(62)
    art = blank(W, H)
    art = foliage(art, W, H, nx, rng, 550, 320, 620, 110, n=90)
    xs = list(range(30, 1090, 44))
    for i, x in enumerate(xs):
        h = rng.uniform(180, 330); ln = rng.uniform(-0.06, 0.06)
        k = i % 4
        if k == 0:
            art = foxglove(art, W, H, nx, rng, x, 372, h, ln, s=0.9)
        elif k == 1:
            art = delphinium(art, W, H, nx, rng, x, 372, h, ln, s=0.9)
        elif k == 2:
            art = hollyhock(art, W, H, nx, rng, x, 372, h * 0.9, ln, s=0.8, col=rng.choice([HOLLY, "#f4d9a0", "#f0c6cf"]))
        else:
            art = foxglove(art, W, H, nx, rng, x, 372, h * 0.8, ln, s=0.85, col="#e8c8d8", deep="#a0628a")
        if i % 3 == 0:
            clear()
    art = daisies(art, W, H, nx, rng, [(rng.uniform(10, 1090), rng.uniform(330, 370)) for _ in range(16)], r=7)
    preview6(art, "pi-border")
    save(art, f"{OUT}/border.webp", max_w=820, quality=72)
    clear()

if "vine" in PARTS:
    # rose rambler garland (section divider)
    W, H = 620, 140
    nx = Seq(63000); rng = random.Random(63)
    art = blank(W, H)
    path = curve([(20, 80), (160, 54), (310, 84), (460, 56), (600, 78)], 60)
    art = G(art, strokes(W, H, [(path, 3, (0.05, 0.05))]), "#6b7d4f", SAGE_D, seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1)
    for i, (x, y) in enumerate(path[2:-2:4]):
        art = jw.leaf(art, W, H, x, y, rng.uniform(18, 26), (-1.2 if i % 2 else 1.6) + rng.uniform(-0.4, 0.4), rng, nx)
    for x, y, L, a in [(290, 70, 34, 3.4), (330, 72, 34, -0.3), (300, 92, 30, 2.2), (322, 92, 30, 1.0)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx)
    art = knockout(art, circles(W, H, [(310, 78, 26)]), amount=1.0, grow=1.5)
    art = jw.rose(art, W, H, 310, 78, 28, rng, nx, ROSE_L, ROSE, ROSE_D)
    art = small_roses(art, W, H, nx, rng, [(220, 64, 1.4), (400, 66, 1.5), (120, 62, 1.1), (500, 64, 1.1), (40, 80, 0.8), (580, 76, 0.8)], r=11)
    art = G(art, circles(W, H, [(270, 92, 4), (352, 92, 4), (172, 50, 3), (450, 50, 3)]), ROSE_L, ROSE, seed=nx(), density=0.8, rough=0.8, pad=6)
    preview6(art, "pi-vine")
    save(art, f"{OUT}/vine.webp", max_w=360, quality=82)
    clear()

if "foxglove" in PARTS:
    W, H = 220, 640
    nx = Seq(64000); rng = random.Random(64)
    art = blank(W, H)
    art = foxglove(art, W, H, nx, rng, 120, 630, 560, -0.04, s=1.3)
    art = delphinium(art, W, H, nx, rng, 70, 630, 420, 0.05, s=1.1)
    preview6(art, "pi-foxglove")
    save(art, f"{OUT}/foxglove.webp", max_w=170, quality=82)
    clear()

if "rose" in PARTS:
    W, H = 300, 280
    nx = Seq(65000); rng = random.Random(65)
    art = blank(W, H)
    for x, y, L, a in [(150, 140, 100, 2.5), (150, 140, 96, 0.45), (150, 140, 80, -0.75), (150, 140, 84, -2.3)]:
        art = jw.leaf(art, W, H, x, y, L + 10, a, rng, nx)
    art = knockout(art, circles(W, H, [(150, 140, 56)]), amount=1.0, grow=1.5)
    art = jw.rose(art, W, H, 150, 140, 58, rng, nx, ROSE_L, ROSE, ROSE_D)
    preview6(art, "pi-rose")
    save(art, f"{OUT}/rose.webp", max_w=180, quality=84)
    clear()
