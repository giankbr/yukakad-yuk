"""Tedak Siten — warm Javanese pastel, gouache + watercolour: tangga tebu (sugarcane ladder, seven rungs) tied with janur,
jadah tujuh warna stepping up on a banana leaf, bamboo kurungan decked with roses and melati, kembang setaman cluster,
single melati. Run: python3 -I tedak-siten.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b6_lib import *

OUT = outdir("tedak-siten")
PARTS = sys.argv[1:] or ["tangga", "jadah", "kurungan", "kembang", "melati", "petal"]
CANE, CANE_D, CANE_L = "#7d3c55", "#4e2236", "#b07489"
JANUR, JANUR_D = "#e8d98a", "#b9a453"
ROSE, ROSE_D, ROSE_L = "#d97a82", "#8e3446", "#f3c1bd"


def cane(art, W, H, p0, p1, width, nx, rng, node_every=74):
    """A sugarcane stalk from p0 to p1: gouache body, light side band, pale nodes with tiny buds."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    n = max(8, int(L / 12))
    pts = [(p0[0] + (p1[0] - p0[0]) * i / n + rng.gauss(0, 0.6), p0[1] + (p1[1] - p0[1]) * i / n) for i in range(n + 1)]
    body = strokes(W, H, [(pts, width, None)])
    art = GP(art, body, CANE, CANE_D, seed=nx(), rough=1.0, streak=1.2, pad=10)
    nxn, nyn = -math.sin(ang), math.cos(ang)
    hi = strokes(W, H, [([(x - nxn * width * 0.22, y - nyn * width * 0.22) for x, y in pts], width * 0.24, (0.05, 0.05))])
    art = G(art, hi * body, CANE_L, seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=1)
    sh = strokes(W, H, [([(x + nxn * width * 0.3, y + nyn * width * 0.3) for x, y in pts], width * 0.2, None)])
    art = G(art, sh * body, CANE_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1)
    nodes, buds = [], []
    k = rng.uniform(20, node_every)
    while k < L - 10:
        cx, cy = p0[0] + math.cos(ang) * k, p0[1] + math.sin(ang) * k
        nodes.append(([(cx - nxn * width * 0.55, cy - nyn * width * 0.55), (cx + nxn * width * 0.55, cy + nyn * width * 0.55)], 3.2, None))
        side = rng.choice((-1, 1))
        buds.append(petal_pts(cx + nxn * width * 0.25 * side, cy + nyn * width * 0.25 * side, width * 0.42, width * 0.2, ang + math.pi, n=8))
        k += node_every * rng.uniform(0.85, 1.1)
    art = GP(art, strokes(W, H, nodes) * body, "#d9b9a4", "#b98f80", seed=nx(), rough=0.5, pad=6)
    return G(art, shapes(W, H, buds) * body, "#e0c79b", seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.6)


def cane_leaves(art, W, H, x, y, rng, nx, n=4, spread=1.0, L=170):
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * 0.42 * spread + rng.uniform(-.1, .1)
        LL = L * rng.uniform(0.7, 1.05)
        p = curve([(x, y), (x + math.cos(a) * LL * 0.5, y + math.sin(a) * LL * 0.5), (x + math.cos(a + 0.5 * (1 if a > -math.pi / 2 else -1)) * LL, y + math.sin(a) * LL * 0.7 + LL * 0.3)], 24)
        m = shapes(W, H, [jw.blade(W, H, p, 9)])
        art = G(art, m, "#9ab27a", "#5e7f4c", seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=2)
    return art


def tie(art, W, H, x, y, nx, rng, ang=0.0):
    """Janur strip binding: a few pale wraps and two short tails."""
    wraps = []
    for k in range(3):
        dx = (k - 1) * 5
        wraps.append(([(x + dx - 9 * math.cos(ang + 1.2), y - 14), (x + dx + 9 * math.cos(ang + 1.2), y + 14)], 4.2, None))
    tails = [(curve([(x + 4, y + 8), (x + 16, y + 26), (x + 12 + rng.uniform(4, 10), y + 44)], 10), 4.5, (0.0, 0.5)),
             (curve([(x - 2, y + 8), (x - 12, y + 24), (x - 8 - rng.uniform(4, 10), y + 40)], 10), 4.0, (0.0, 0.5))]
    m = strokes(W, H, wraps + tails)
    art = GP(art, m, JANUR, JANUR_D, seed=nx(), rough=0.6, streak=0.6, pad=6)
    return G(art, np.clip(m - gaussian_filter(m, 1.2), 0, 1) * 2, JANUR_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)


if "tangga" in PARTS:
    W, H = 440, 700
    nx = Seq(30100); rng = random.Random(5)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(220, 676, 170, 14, 16), rng, 1, 0.03)])
    art = G(art, sh, "#6d4b3d", seed=nx(), density=0.28, edge=0.1, bloom=0, rough=3, feather=6)
    L0, L1 = (96, 676), (150, 120)
    R0, R1 = (318, 676), (300, 120)
    art = cane_leaves(art, W, H, 150, 130, rng, nx, 4, 1.0, 150)
    art = cane_leaves(art, W, H, 300, 130, rng, nx, 4, 1.1, 150)
    rungs = []
    for i in range(7):
        t = 0.1 + i * 0.125
        ya = L0[1] + (L1[1] - L0[1]) * t
        xa = L0[0] + (L1[0] - L0[0]) * t
        xb = R0[0] + (R1[0] - R0[0]) * t
        rungs.append((xa, xb, ya))
    for xa, xb, y in rungs:
        art = cane(art, W, H, (xa - 14, y + 2), (xb + 14, y - 2), 15, nx, rng, node_every=90)
    art = cane(art, W, H, L0, L1, 26, nx, rng)
    art = cane(art, W, H, R0, R1, 26, nx, rng)
    for xa, xb, y in rungs:
        art = tie(art, W, H, xa, y, nx, rng)
        art = tie(art, W, H, xb, y, nx, rng)
    # a small melati string draped from the top rung
    pts = curve([(rungs[-1][0], rungs[-1][2] + 6), (225, rungs[-1][2] + 46), (rungs[-1][1], rungs[-1][2] + 4)], 60)
    art = jw.melati_string(art, W, H, pts, rng, nx, size=6.5)
    preview(art, "ts-tangga")
    save(art, f"{OUT}/tangga.webp", max_w=300, quality=82)
    clear()

if "jadah" in PARTS:
    W, H = 640, 330
    nx = Seq(30300); rng = random.Random(7)
    art = blank(W, H)
    # banana leaf base
    leafp = curve([(18, 286), (200, 262), (420, 262), (624, 284)], 40)
    lm = shapes(W, H, [jw.blade(W, H, leafp, 40)])
    art = G(art, lm, "#9cbf84", "#5b8a4e", seed=nx(), density=0.75, edge=0.55, bloom=0.35, rough=3)
    veins = strokes(W, H, [(leafp[1:-1], 2.2, (0.1, 0.3))] + [([(x, 270 + (x - 320) ** 2 / 9000), (x + 26, 250 + (x - 320) ** 2 / 9000)], 1.0, None) for x in range(50, 600, 22)])
    art = G(art, veins * lm, "#4a7340", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, feather=0.5)
    cols = [("#d6635f", "#a8403f"), ("#f5efe4", "#ddd1bf"), ("#4a3d42", "#2a2226"), ("#f0c65a", "#c99a2e"), ("#86afd0", "#557ea3"), ("#f2a9b6", "#cf7f8f"), ("#a184bd", "#73579a")]
    w_, h_, dp = 74, 46, 18
    slots = [(0, 0), (1, 0), (2, 0), (3, 0), (0.5, 1), (2.5, 1), (1.5, 2)]
    order = [2, 0, 4, 1, 5, 3, 6]
    for i in sorted(range(7), key=lambda k: (slots[k][1], -slots[k][0])):
        c, cd = cols[order.index(i)] if False else cols[i]
        col_, row = slots[i]
        x = 132 + col_ * (w_ + 18) + row * 7; y1 = 270 - row * (h_ + 4); y0 = y1 - h_
        front = shapes(W, H, [deform(rect(x, y0, x + w_, y1), rng, 1, 0.012)])
        top = shapes(W, H, [[(x, y0), (x + dp, y0 - dp * 0.7), (x + w_ + dp, y0 - dp * 0.7), (x + w_, y0)]], smooth=False)
        side = shapes(W, H, [[(x + w_, y0), (x + w_ + dp, y0 - dp * 0.7), (x + w_ + dp, y1 - dp * 0.7), (x + w_, y1)]], smooth=False)
        art = GP(art, side, cd, mix(cd, "#000000", .15), seed=nx(), rough=1.0, pad=6)
        art = GP(art, front, c, mix(c, cd, .35), seed=nx(), rough=1.2, streak=0.6, pad=6)
        art = GP(art, top, mix(c, "#ffffff", .35), c, seed=nx(), rough=0.8, pad=6)
        speck = circles(W, H, [(x + rng.uniform(4, w_ - 4), rng.uniform(y0 + 4, y1 - 4), rng.uniform(0.8, 1.8)) for _ in range(30)])
        art = G(art, speck * front, mix(c, "#ffffff", .5) if i != 1 else "#c9bda8", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, feather=0.3)
        art = G(art, shade_side(front, -6, 0, 3), cd, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    preview(art, "ts-jadah")
    save(art, f"{OUT}/jadah.webp", max_w=440, quality=82)
    clear()

if "kurungan" in PARTS:
    W, H = 480, 640
    nx = Seq(30500); rng = random.Random(9)
    art = blank(W, H)
    cx = 240
    sh = shapes(W, H, [deform(ellipse_pts(cx, 600, 200, 18, 16), rng, 1, 0.03)])
    art = G(art, sh, "#6d4b3d", seed=nx(), density=0.26, edge=0.1, bloom=0, rough=3, feather=6)
    # bell outline: y=120 top to 590 bottom
    def half(t):  # width profile of the bell at height t (0 top .. 1 bottom)
        return 48 + 168 * (math.sin(t * math.pi * 0.5) ** 0.55)
    inside = shapes(W, H, [[(cx - half(i / 30), 150 + i / 30 * 420) for i in range(31)] + [(cx + half(1 - i / 30), 150 + (1 - i / 30) * 420) for i in range(31)]])
    art = G(art, inside, "#f3dccb", "#e9cbb6", seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=3)
    slats = []
    for k in range(-7, 8):
        f = k / 7
        pts = [(cx + f * half(i / 24), 150 + i / 24 * 420) for i in range(25)]
        slats.append((pts, 5.2 - abs(f) * 1.6, None))
    hoops = []
    for t in (0.0, 0.36, 0.68, 1.0):
        y = 150 + t * 420; hw = half(t)
        hoops.append((arc_pts(cx, y, hw, math.pi * 0.02, math.pi * 0.98, 30, 0.09), 7, None))
    bam = strokes(W, H, slats + hoops)
    art = GP(art, bam, "#d2a86e", "#a77a44", seed=nx(), rough=0.8, streak=0.9, pad=8)
    art = G(art, shade_side(bam, -3, -2, 2), "#7a5428", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5)
    # top knob + janur bow
    knob = np.maximum(circles(W, H, [(cx, 136, 18)]), shapes(W, H, [rect(cx - 8, 96, cx + 8, 140)], smooth=False))
    art = GP(art, knob, "#c99a5e", "#8f6532", seed=nx(), rough=0.6, pad=6)
    bow = shapes(W, H, [petal_pts(cx, 100, 70, 20, -2.6, n=12), petal_pts(cx, 100, 70, 20, -0.54, n=12), petal_pts(cx, 100, 60, 14, 1.9, n=10), petal_pts(cx, 100, 60, 14, 1.25, n=10)])
    art = GP(art, bow, JANUR, JANUR_D, seed=nx(), rough=0.8, streak=0.8, pad=8)
    art = G(art, strokes(W, H, [([(cx, 100), (cx + math.cos(a) * 58, 100 + math.sin(a) * 58)], 1.2, None) for a in (-2.6, -0.54)]), JANUR_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    # flower garlands: around the middle hoop and the bottom rim
    area = np.zeros((H, W), np.float32)
    flowers = blank(W, H)
    for t, nr, r in ((0.36, 5, 25), (1.0, 7, 30)):
        y = 150 + t * 420; hw = half(t)
        for j in range(nr):
            f = -0.88 + 1.76 * j / (nr - 1)
            fx = cx + f * hw; fy = y + 4 + (1 - f * f) * hw * 0.09
            if j % 2 == 0:
                flowers = jw.rose(flowers, W, H, fx, fy, r * rng.uniform(.85, 1.05), rng, nx, ROSE_L, ROSE, ROSE_D, area)
            else:
                flowers = jw.white_flower(flowers, W, H, fx, fy, r * 0.72, rng, nx)
                np.maximum(area, circles(W, H, [(fx, fy, r * 0.7)]), out=area)
    leaves = blank(W, H)
    for t, nr in ((0.36, 6), (1.0, 8)):
        y = 150 + t * 420; hw = half(t)
        for j in range(nr):
            f = -0.95 + 1.9 * j / (nr - 1)
            leaves = jw.leaf(leaves, W, H, cx + f * hw, y + 6, rng.uniform(34, 46), rng.choice((-2.6, -0.5, 2.8, 0.3)) + rng.uniform(-.3, .3), rng, nx, c=("#a8bf8e", "#6b8a5a"))
    leaves = knockout(leaves, area, amount=0.95, grow=3)
    art = glaze(art, leaves)
    art = over(art, flowers)
    for k in (-1, 1):
        x0 = cx + k * half(0.36) * 0.7; y0 = 150 + 0.36 * 420 + 10
        pts = curve([(x0, y0), (x0 + k * 6, y0 + 70), (x0 + k * 2, y0 + 130)], 40)
        art = jw.melati_string(art, W, H, pts, rng, nx, size=6)
    preview(art, "ts-kurungan")
    save(art, f"{OUT}/kurungan.webp", max_w=320, quality=82)
    clear()

if "kembang" in PARTS:
    W, H = 600, 240
    nx = Seq(30700); rng = random.Random(11)
    art = blank(W, H)
    area = np.zeros((H, W), np.float32)
    fl = blank(W, H)
    # kenanga: yellow-green drooping twisted petals
    def kenanga(a, x, y, s):
        polys = [deform(petal_pts(x, y, s * rng.uniform(2.3, 2.8), s * 0.2, math.pi / 2 + (k - 2.5) * 0.34 + rng.uniform(-.12, .12), n=12, cup=0.25), rng, 1, 0.08) for k in range(6)]
        m = shapes(W, H, polys)
        a = G(a, m, "#e8d66e", "#bdb04a", seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=1.5)
        return a, m
    # kantil: long cream petals in a loose tulip
    def kantil(a, x, y, s):
        polys = [petal_pts(x, y, s * 2.0, s * 0.42, -math.pi / 2 + (k - 2) * 0.34, n=12) for k in range(5)]
        m = shapes(W, H, polys)
        a = GP(a, m, "#fbf3dd", "#eadbb5", seed=nx(), rough=1.0, pad=8)
        a = G(a, np.clip(m - gaussian_filter(m, 1.4), 0, 1) * 2.5, "#b9a27a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
        return a, m
    fl = jw.rose(fl, W, H, 300, 128, 46, rng, nx, ROSE_L, ROSE, ROSE_D, area)
    fl = jw.rose(fl, W, H, 196, 150, 32, rng, nx, "#f6d0c8", "#e28b8f", ROSE_D, area)
    fl, m = kenanga(fl, 400, 112, 26); np.maximum(area, m, out=area)
    fl, m = kantil(fl, 112, 162, 24); np.maximum(area, m, out=area)
    fl, m = kenanga(fl, 488, 150, 20); np.maximum(area, m, out=area)
    for x, y, r in [(246, 92, 16), (356, 172, 15), (150, 108, 13), (444, 178, 13), (530, 112, 12), (66, 128, 12)]:
        fl = jw.white_flower(fl, W, H, x, y, r, rng, nx)
        np.maximum(area, circles(W, H, [(x, y, r)]), out=area)
    lv = blank(W, H)
    for x, y, L, a in [(250, 160, 70, 2.6), (350, 150, 66, 0.4), (150, 180, 56, 2.9), (430, 160, 60, 0.2), (300, 90, 50, -1.9), (520, 170, 46, 0.5)]:
        lv = jw.leaf(lv, W, H, x, y, L, a, rng, nx, c=("#a8bf8e", "#6b8a5a"))
    lv = knockout(lv, area, amount=0.95, grow=3)
    art = glaze(art, lv)
    art = over(art, fl)
    petals = shapes(W, H, [deform(petal_pts(x, y, rng.uniform(10, 16), rng.uniform(6, 9), rng.uniform(0, 6.28), n=10), rng, 1, 0.1) for x, y in
                          [(30, 190), (560, 200), (86, 214), (520, 70), (600 - 40, 140), (20, 120)]])
    art = G(art, petals, "#e8959a", "#c9606f", seed=nx(), density=0.75, edge=0.55, rough=1)
    preview(art, "ts-kembang")
    save(art, f"{OUT}/kembang.webp", max_w=420, quality=82)
    clear()

if "melati" in PARTS:
    W = H = 120
    nx = Seq(30900); rng = random.Random(13)
    art = jw.white_flower(blank(W, H), W, H, 60, 60, 40, rng, nx, petals=6)
    preview(art, "ts-melati", tone="#f5d9cc")
    save(art, f"{OUT}/melati.webp", max_w=72, quality=84)

if "petal" in PARTS:
    W = H = 90
    nx = Seq(31000); rng = random.Random(15)
    m = shapes(W, H, [deform(petal_pts(18, 50, 60, 22, -0.3, n=14, cup=0.4), rng, 1, 0.05)])
    art = G(blank(W, H), m, "#f2b3b5", "#d9707e", seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=1.5)
    preview(art, "ts-petal")
    save(art, f"{OUT}/petal.webp", max_w=44, quality=84)

kb(OUT)
