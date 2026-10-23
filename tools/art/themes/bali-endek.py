"""Bali Endek — gouache and thread-level textile: Ubud terraced rice fields (sawah berundak) curving down a valley
with coconut palms and jungle ridges; a penjor (tall bamboo pole arching over, janur fringes, sampian at the tip,
small bamboo sanggah, rice-stalk and cloth hangings); a canang sari (janur tray with flowers in four colours and
shredded pandan); a jepun (frangipani) flower; a janur cut-leaf divider; and an endek weft-ikat tile (jade ground,
magenta lattice, saffron flowers, feathered along the weft).
Run: python3 -I bali-endek.py [part ...]  parts: sawah penjor canang jepun divider endek
Assets -> public/themes/art/bali-endek/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i2_lib import *  # noqa

OUT = outdir("bali-endek")
PARTS = sys.argv[1:] or ["sawah", "penjor", "canang", "jepun", "divider", "endek"]
JANUR, JANUR_L, JANUR_D = "#d9c86a", "#efe3a0", "#a39339"
BAMBOO, BAMBOO_D = "#c9a35c", "#7f5f2e"
RICE = ["#8fc24a", "#a6cf55", "#7cb243", "#b7d866", "#6fa43f"]
JADE, MAGENTA, SAFFRON, IVORY, INK = "#1d6b66", "#b2306a", "#e3a52e", "#f1e8d2", "#1b2224"


def sawah():
    W, H = 780, 620
    rng = random.Random(21); nx = Seq(2100)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # far jungle ridge with palm crowns on the skyline
    ridge = ridge_pts(W, 205, 70, rng, step=12, freq=(1.1, 2.7))
    rm = shapes(W, H, [ridge])
    art = GP(art, rm, "#5e8a6a", "#6f9a72", seed=nx(), rough=2.0)
    art = twash(art, rm * lin(W, H, 0, 110, 0, 230), "#d9ebe0", 0.35, seed=nx())
    # terraces: curved contour bands across the valley, spacing growing toward the viewer
    N = 13
    cx = W * 0.56
    def cy(i, x):
        t = i / N
        Y = 214 + 410 * t ** 1.32
        bow = (40 + 120 * t) * (((x - cx) / (W * 0.6)) ** 2)
        wob = 6 * math.sin(x / (60 + 20 * t) + i * 1.7) * (0.5 + t)
        return Y - bow + wob
    for i in range(N):
        xs = np.linspace(-20, W + 20, 60)
        top = [(x, cy(i, x)) for x in xs]
        bot = [(x, cy(i + 1, x)) for x in xs[::-1]]
        band = shapes(W, H, [top + bot])
        t = i / N
        col = RICE[i % len(RICE)]
        flooded = i in (3, 7)
        if flooded:
            art = GP(art, band, "#b8d6d8", "#d5e8e2", seed=nx(), rough=1.4)
            art = twash(art, band * lin(W, H, 0, cy(i, cx), 0, cy(i + 1, cx)), "#7fb3b8", 0.4, seed=nx())
            # young seedlings in rows on the water
            rows = [([(x, y), (x + 1, y - 4 - 6 * t)], 1.2 + t, (0.0, 0.6)) for x in np.arange(-10, W, 9 + 6 * t) for y in [cy(i, x) + (cy(i + 1, x) - cy(i, x)) * f for f in (0.35, 0.7)]]
            art = GP(art, strokes(W, H, rows) * band, "#7cb243", seed=nx(), rough=0.5)
        else:
            art = GP(art, band, col, mix(col, "#e8f0a0", 0.25), seed=nx(), rough=1.4, streak=1.4)
            # rice texture: short upright strokes, denser and larger near the bottom
            art = brushwork(art, band, [mix(col, "#3f6a2a", 0.25), mix(col, "#f2f6a8", 0.3)], rng, nx, n=int(120 + 260 * t), L=(4 + 8 * t, 9 + 16 * t), wd=(1 + 1.2 * t, 2 + 2 * t), ang=-math.pi / 2, ang_var=0.25)
            art = twash(art, band * lin(W, H, 0, cy(i, cx), 0, cy(i + 1, cx)), "#4f7f32", 0.25, seed=nx())
        # riser (earth wall) just under the upper edge and the bund line
        riser = strokes(W, H, [(top, 3 + 7 * t, None)])
        art = twash(art, riser * band, "#5d6e33", 0.6, seed=nx())
        lip = strokes(W, H, [([(x, y - 1.5 - 2 * t) for x, y in top], 1.2 + 1.5 * t, None)])
        art = twash(art, lip, "#e8f2b0", 0.55, seed=nx())
        trim_cache()
    last = [(x, cy(N, x)) for x in np.linspace(-20, W + 20, 60)] + [(W + 20, H + 20), (-20, H + 20)]
    lm = shapes(W, H, [last])
    art = GP(art, lm, RICE[1], mix(RICE[1], "#e8f0a0", 0.25), seed=nx(), rough=1.4, streak=1.4)
    art = brushwork(art, lm, [mix(RICE[1], "#3f6a2a", 0.25), mix(RICE[1], "#f2f6a8", 0.3)], rng, nx, n=300, L=(12, 26), wd=(2.2, 4), ang=-math.pi / 2, ang_var=0.25)
    art = twash(art, strokes(W, H, [([(x, cy(N, x)) for x in np.linspace(-20, W + 20, 60)], 10, None)]) * lm, "#5d6e33", 0.6, seed=nx())
    # coconut palms along the terraces
    def palm(px, py, ph, lean, s):
        nonlocal art
        trunk = curve([(px, py), (px + lean * ph * 0.3, py - ph * 0.55), (px + lean * ph, py - ph)], 24)
        art = GP(art, strokes(W, H, [(trunk, 5 * s, (0, 0.3))]), "#7d6a4e", "#9a8462", seed=nx(), rough=0.8)
        tx, ty = trunk[-1]
        items = []
        for a in np.linspace(-math.pi * 1.0, 0.0, 8):
            L = rng.uniform(26, 38) * s
            pts = curve([(tx, ty), (tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.4 - 4 * s), (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.25 + 12 * s)], 10)
            items.append((pts, 5 * s, (0.0, 0.8)))
        art = GP(art, strokes(W, H, items), "#3e6e3a", "#58894a", seed=nx(), rough=1.0)
    for px, py, ph, ln, s in [(90, 300, 110, 0.15, 1.0), (140, 330, 90, -0.1, 0.8), (650, 280, 120, -0.18, 1.0), (700, 300, 90, 0.1, 0.8), (420, 250, 70, 0.08, 0.6), (300, 262, 60, -0.1, 0.55), (560, 255, 70, 0.1, 0.6)]:
        palm(px, py, ph, ln, s)
    # little bamboo hut (kubu) on the right terraces
    hut = shapes(W, H, [[(600, 360), (640, 360), (640, 384), (600, 384)]], smooth=False)
    art = GP(art, hut, "#b48a55", seed=nx(), rough=0.6)
    roof = shapes(W, H, [[(590, 362), (620, 336), (650, 362)]], smooth=False)
    art = GP(art, roof, "#6e5636", "#8a6e46", seed=nx(), rough=1.0)
    art = twash(art, strokes(W, H, [([(x, 362), (x + 4, 340)], 1.0, None) for x in range(594, 648, 5)]) * roof, "#4a3a24", 0.4, seed=nx())
    # mist between ridge and terraces; fade the top edge into the sky
    haze = np.exp(-((yy - 225) / 18) ** 2) * (0.5 + 0.5 * fbm(W, H, nx(), 60, 3))
    art = twash(art, haze * (art[..., 3] > 0.1), "#eef5ec", 0.55, seed=nx())
    preview(art, "sawah", bg="#e9f0dc")
    print("sawah", save(art, f"{OUT}/sawah.webp", max_w=780, quality=78))
    clear()


def penjor():
    W, H = 420, 1100
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    # pole: straight then arching right, tip drooping
    pole = curve([(70, 1090), (72, 700), (80, 420), (120, 230), (210, 120), (310, 110), (380, 190)], 120)
    n = len(pole)
    items = []
    for i in range(n - 1):
        t = i / (n - 1)
        items.append(([pole[i], pole[i + 1]], 18 * (1 - t) + 4, None))
    pm = strokes(W, H, items)
    art = GP(art, pm, BAMBOO, mix(BAMBOO, "#ffffff", 0.2), seed=nx(), rough=0.8, streak=1.2)
    art = twash(art, pm * lin(W, H, 60, 0, 86, 0), BAMBOO_D, 0.35, seed=nx())
    nodes = strokes(W, H, [([(pole[i][0] - 10, pole[i][1]), (pole[i][0] + 10, pole[i][1] + 1)], 2.0, None) for i in range(6, int(n * 0.55), 9)]) * pm
    art = twash(art, nodes, BAMBOO_D, 0.7, seed=nx())
    # janur wrapping bands on the lower pole
    for y in (560, 640, 720, 900):
        b = rect(W, H, 50, y, 96, y + 14) * gaussian_filter(pm, 1)
        art = GP(art, np.clip(b * 1.4, 0, 1), JANUR, JANUR_L, seed=nx(), rough=0.8)
        art = twash(art, strokes(W, H, [([(x, y), (x + 6, y + 14)], 1.2, None) for x in range(50, 100, 7)]) * b, JANUR_D, 0.6, seed=nx())
    # fringe of janur strips hanging all along the arch
    fr = []
    for i in range(int(n * 0.28), n - 3):
        x, y = pole[i]
        for _ in range(2):
            L = rng.uniform(40, 84) * (0.6 + 0.4 * (i / n))
            sway = rng.uniform(-10, 10)
            fr.append(([(x + rng.uniform(-3, 3), y + 3), (x + sway * 0.4, y + L * 0.5), (x + sway, y + L)], rng.uniform(5, 8), (0.0, 0.75)))
    fm = strokes(W, H, fr)
    art = GP(art, fm, JANUR, JANUR_L, seed=nx(), rough=0.8, streak=1.0)
    art = twash(art, fm * rad(W, H, 220, 140, 220), "#fff6c4", 0.25, seed=nx())
    art = twash(art, np.clip(fm - np.roll(fm, -2, 1), 0, 1), JANUR_D, 0.4, seed=nx())
    # small curled ornaments (tamas) at intervals along the arch
    for i in range(int(n * 0.36), n - 8, 12):
        x, y = pole[i]
        cm = strokes(W, H, [(spiral_pts(x + 6, y + 70, 2, 12, 0, 1.6), 3.0, (0.0, 0.2)), ([(x, y + 6), (x + 2, y + 58)], 3.2, None)])
        art = GP(art, cm, JANUR_L, seed=nx(), rough=0.5)
    # sampian at the tip: a long woven janur ornament with curls and a tassel
    tx, ty = pole[-1]
    samp = shapes(W, H, [[(tx - 12, ty + 4), (tx + 12, ty + 4), (tx + 8, ty + 90), (tx, ty + 130), (tx - 8, ty + 90)]])
    art = GP(art, samp, JANUR, JANUR_L, seed=nx(), rough=0.8)
    art = twash(art, strokes(W, H, [([(tx - 10, y), (tx + 10, y + 4)], 1.4, None) for y in range(int(ty) + 14, int(ty) + 100, 8)]) * samp, JANUR_D, 0.55, seed=nx())
    curls = strokes(W, H, [(spiral_pts(tx - 20, ty + 40, 3, 16, 0.5, 1.5, d=-1), 3.4, (0, 0.2)), (spiral_pts(tx + 20, ty + 40, 3, 16, 2.6, 1.5), 3.4, (0, 0.2))])
    art = GP(art, curls, JANUR_L, seed=nx(), rough=0.5)
    tass = strokes(W, H, [([(tx, ty + 128), (tx + dx * 0.4, ty + 150), (tx + dx, ty + 176)], 2.2, (0, 0.7)) for dx in (-10, -4, 2, 8)])
    art = GP(art, tass, JANUR, seed=nx(), rough=0.5)
    # hangings on the lower pole: a bundle of rice stalks (padi) and white/yellow cloth (kain)
    rice = strokes(W, H, [([(96, 470), (120 + k * 3, 520), (126 + k * 4, 580)], 2.0, (0, 0.6)) for k in range(-3, 4)])
    art = GP(art, rice, "#d4a83c", "#e8c35a", seed=nx(), rough=0.6)
    grains = circles(W, H, [(126 + k * 4 + rng.uniform(-3, 3), 560 + rng.uniform(0, 26), 2.8) for k in range(-3, 4) for _ in range(4)])
    art = GP(art, grains, "#c99a2e", seed=nx(), rough=0.4)
    cloth = shapes(W, H, [[(94, 610), (150, 618), (146, 700), (132, 690), (118, 706), (96, 694)]])
    art = GP(art, cloth, "#f3ecd8", "#ffffff", seed=nx(), rough=1.0)
    art = twash(art, cloth * lin(W, H, 96, 610, 150, 700), "#c6b98f", 0.3, seed=nx())
    yel = shapes(W, H, [[(94, 612), (150, 620), (148, 636), (94, 628)]])
    art = GP(art, yel, "#e9c341", seed=nx(), rough=0.8)
    # sanggah penjor: a small bamboo offering shelf with a roof of janur
    sh = rect(W, H, 30, 790, 130, 800)
    art = GP(art, sh, "#9b7a42", seed=nx(), rough=0.5)
    legs = strokes(W, H, [([(36, 800), (36, 860)], 4, None), ([(124, 800), (124, 860)], 4, None)])
    art = GP(art, legs, "#8a6a36", seed=nx(), rough=0.5)
    rf = shapes(W, H, [[(24, 760), (80, 738), (136, 760), (128, 770), (32, 770)]], smooth=False)
    art = GP(art, rf, JANUR, JANUR_L, seed=nx(), rough=0.8)
    art = twash(art, strokes(W, H, [([(x, 760), (x + 3, 770)], 1.2, None) for x in range(28, 134, 6)]) * rf, JANUR_D, 0.5, seed=nx())
    offer = ellipses(W, H, [(62, 784, 10, 6, 0), (92, 784, 10, 6, 0)])
    art = GP(art, offer, "#e2557a", seed=nx(), rough=0.5)
    preview(art, "penjor", bg="#eaf1dc")
    print("penjor", save(art, f"{OUT}/penjor.webp", max_w=210, quality=82))
    clear()


def flower(art, W, H, x, y, r, col, col2, rng, nx, petals=5, centre="#f0c33c"):
    for k in range(petals):
        a = k / petals * math.tau + rng.uniform(-0.2, 0.2)
        pm = shapes(W, H, [deform(petal_pts(x, y, r, r * 0.5, a), rng, 1, 0.03)])
        art = GP(art, pm, col, col2, seed=nx(), rough=0.6)
        art = twash(art, pm * rad(W, H, x, y, r * 0.8), mix(col, "#000000", 0.25), 0.25, seed=nx())
    art = GP(art, circles(W, H, [(x, y, r * 0.22)]), centre, seed=nx(), rough=0.4)
    return art


def canang():
    W, H = 460, 340
    rng = random.Random(41); nx = Seq(4100)
    art = blank(W, H)
    cx, cy = W / 2, 190
    # tray seen in 3/4: a squashed square (diamond) with a raised woven rim
    def sq(s, dy=0):
        return [(cx, cy - 70 * s + dy), (cx + 170 * s, cy + dy), (cx, cy + 70 * s + dy), (cx - 170 * s, cy + dy)]
    side = shapes(W, H, [[(cx - 170, cy), (cx, cy + 70), (cx + 170, cy), (cx + 170, cy + 26), (cx, cy + 96), (cx - 170, cy + 26)]], smooth=False)
    art = GP(art, side, JANUR, JANUR_L, seed=nx(), rough=1.0)
    art = twash(art, strokes(W, H, [([(x, cy - 10), (x, cy + 110)], 1.4, None) for x in range(int(cx - 170), int(cx + 170), 9)]) * side, JANUR_D, 0.45, seed=nx())
    art = twash(art, side * lin(W, H, cx, 0, cx + 170, 0), "#7d7130", 0.35, seed=nx())
    top = shapes(W, H, [sq(1.0)], smooth=False)
    art = GP(art, top, "#cdbb5a", JANUR, seed=nx(), rough=1.0)
    # shredded pandan (green strands) filling the tray
    sp = [([(cx + rng.uniform(-130, 130), cy + rng.uniform(-40, 40)), (cx + rng.uniform(-130, 130), cy + rng.uniform(-40, 40))], rng.uniform(1.2, 2.2), (0.2, 0.2)) for _ in range(90)]
    art = GP(art, strokes(W, H, sp) * top, "#4d8a3a", "#6aa848", seed=nx(), rough=0.4)
    # flowers by direction: white (east), red (south), yellow (west), blue-violet (north) + jepun in the centre
    groups = [((cx + 80, cy - 6), "#f7f4ec", "#e8e2d2"), ((cx, cy + 34), "#d0303a", "#e0484e"), ((cx - 80, cy - 6), "#f0c030", "#f6d65a"), ((cx, cy - 40), "#6a4ea8", "#8a6cc0")]
    for (gx, gy), c1, c2 in groups:
        for _ in range(7):
            art = flower(art, W, H, gx + rng.uniform(-34, 34), gy + rng.uniform(-14, 14), rng.uniform(15, 21), c1, c2, rng, nx, petals=rng.choice([5, 6]), centre="#f6d25a" if c1 != "#f0c030" else "#d08a20")
        trim_cache()
    art = flower(art, W, H, cx + 6, cy - 4, 26, "#fbf7ec", "#ffffff", rng, nx, petals=5, centre="#f2c43a")
    # porosan & sampian: a small janur cone standing up at the back
    cone = shapes(W, H, [[(cx - 20, cy - 52), (cx, cy - 140), (cx + 20, cy - 52)]], smooth=False)
    art = GP(art, cone, JANUR_L, JANUR, seed=nx(), rough=0.6)
    art = twash(art, cone * lin(W, H, cx - 20, 0, cx + 20, 0), JANUR_D, 0.35, seed=nx())
    sh = np.roll(gaussian_filter(np.clip(side + top, 0, 1), 8), 10, 0) * (1 - np.clip(side + top, 0, 1))
    art = over(np.concatenate([np.ones((H, W, 3), np.float32) * carr("#5a5030"), (sh * 0.3)[..., None]], -1), art)
    preview(art, "canang", bg="#f2ecdc")
    print("canang", save(art, f"{OUT}/canang.webp", max_w=230, quality=84))
    clear()


def jepun():
    """Jepun (frangipani): five obovate petals overlapping in a pinwheel, white with a saffron throat."""
    W = H = 300
    rng = random.Random(51); nx = Seq(5100)
    art = blank(W, H)
    cx = cy = W / 2
    for k in range(5):
        a = k / 5 * math.tau - math.pi / 2
        # obovate petal from the centre: narrow claw, broad rounded tip, skewed so they overlap like a pinwheel
        pts = []
        for i in range(30):
            t = i / 29
            wdt = 46 * math.sin(math.pi * min(1, t * 1.15)) ** 0.7 * (0.25 + 0.75 * t ** 0.6)
            pts.append((t * 118, wdt + 16 * t))
        for i in range(29, -1, -1):
            t = i / 29
            wdt = 46 * math.sin(math.pi * min(1, t * 1.15)) ** 0.7 * (0.25 + 0.75 * t ** 0.6)
            pts.append((t * 118, -wdt * 0.55 + 16 * t))
        ca, sa = math.cos(a), math.sin(a)
        P = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
        pm = shapes(W, H, [deform(P, rng, 1, 0.01)])
        art = GP(art, pm, "#fdf9ef", "#ffffff", seed=nx(), rough=0.7)
        art = twash(art, pm * rad(W, H, cx, cy, 70) ** 0.8, "#f2bd34", 0.85, seed=nx(), col2="#f7d566")
        edge = np.clip(pm - gaussian_filter(pm, 1.6), 0, 1) * 3
        art = twash(art, np.clip(edge, 0, 1), "#b9a37a", 0.55, seed=nx())
        art = twash(art, pm * lin(W, H, cx + ca * 20, cy + sa * 20, cx + ca * 110 - sa * 40, cy + sa * 110 + ca * 40), "#d9ccb0", 0.22, seed=nx())
    art = GP(art, circles(W, H, [(cx, cy, 7)]), "#d9961f", seed=nx(), rough=0.4)
    preview(art, "jepun", bg="#f2ecdc")
    print("jepun", save(art, f"{OUT}/jepun.webp", max_w=110, quality=84))
    clear()


def divider():
    """Janur cut-leaf band: a folded young-palm-leaf strip with triangular notches and a curl at each end."""
    W, H = 560, 80
    rng = random.Random(61); nx = Seq(6100)
    art = blank(W, H)
    y = 40
    band = rect(W, H, 60, y - 9, W - 60, y + 9)
    teeth = []
    for x in range(60, W - 60, 16):
        teeth.append([(x, y + 9), (x + 8, y + 22), (x + 16, y + 9)])
        teeth.append([(x + 8, y - 9), (x + 16, y - 22), (x + 24, y - 9)] if x + 24 < W - 60 else [(x, y - 9), (x, y - 9), (x, y - 9)])
    m = np.clip(band + shapes(W, H, teeth, smooth=False), 0, 1)
    m = displace(m, nx(), 1.2, 10)
    art = GP(art, m, JANUR, JANUR_L, seed=nx(), rough=0.8, streak=1.2)
    art = twash(art, strokes(W, H, [([(60, y), (W - 60, y)], 1.4, None)]), JANUR_D, 0.6, seed=nx())
    cuts = strokes(W, H, [([(x, y - 9), (x, y + 9)], 1.2, None) for x in range(68, W - 60, 16)]) * band
    art = twash(art, cuts, JANUR_D, 0.45, seed=nx())
    curl = strokes(W, H, [(spiral_pts(44, y, 3, 18, 0.0, 1.4, d=-1), 4, (0, 0.2)), (spiral_pts(W - 44, y, 3, 18, math.pi, 1.4, d=-1), 4, (0, 0.2))])
    art = GP(art, curl, JANUR, seed=nx(), rough=0.5)
    art = flower(art, W, H, W / 2, y, 16, "#fbf6ea", "#ffffff", rng, nx, petals=5, centre="#f2c43a")
    preview(art, "divider", bg="#f2ecdc")
    print("divider", save(art, f"{OUT}/divider.webp", max_w=280, quality=84))
    clear()


def endek():
    """Endek weft ikat: jade ground, magenta lattice of stepped diamonds edged in ink, saffron four-petal flowers in
    every diamond, ivory dots on the crossings. 480 x 480 tile (shown at 240)."""
    S = 480
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    P = 120.0  # diamond period
    u = (xx + yy) / P; v = (xx - yy) / P
    fu = np.abs((u % 1.0) - 0.5); fv = np.abs((v % 1.0) - 0.5)
    lat = np.minimum(fu, fv)  # 0.5 at lattice line ... wait: distance to line = 0.5 - max
    dline = 0.5 - np.maximum(fu, fv)
    motif = np.zeros((S, S), np.int32)  # 0 jade
    # stepped (pixelated) look of tied bundles: quantise to 6 px
    q = 6
    Q = lambda a: a[(np.arange(S) // q * q)[:, None], (np.arange(S) // q * q)[None, :]]
    dl = Q(dline)
    motif[dl < 0.075] = 4  # ink edge
    motif[dl < 0.045] = 1  # magenta line
    # flower in each diamond centre
    cu = (u % 1.0) - 0.5; cv = (v % 1.0) - 0.5
    r = np.hypot(cu, cv)
    ang = np.arctan2(cv, cu)
    petal = r < (0.17 + 0.09 * np.cos(4 * ang)) * 1.0
    petal = Q(petal.astype(np.float32)) > 0.5
    motif[petal & (dl > 0.1)] = 2
    core = Q((r < 0.06).astype(np.float32)) > 0.5
    motif[core] = 3
    # ivory dots at lattice crossings
    cr = np.hypot(((u + 0.5) % 1.0) - 0.5, ((v + 0.5) % 1.0) - 0.5)
    # crossings of the lattice are where u and v are both integers: distance to nearest integer point
    du = np.abs(((u + 0.5) % 1.0) - 0.5); dv = np.abs(((v + 0.5) % 1.0) - 0.5)
    dots = Q(((du < 0.07) & (dv < 0.07)).astype(np.float32)) > 0.5
    motif[dots] = 3
    # small ink ticks halfway along each diamond (secondary motif)
    pal = [JADE, MAGENTA, SAFFRON, IVORY, INK]
    rgb = weft_ikat(motif, pal, seed=7, pick=3, bleed=12.0)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/endek.png")
    print("endek", save_rgb(rgb, f"{OUT}/endek.webp", quality=80))
    clear()


for p in PARTS:
    globals()[p]()
kb_report(OUT)
