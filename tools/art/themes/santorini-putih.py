"""Santorini Putih — gouache on hot-press: whitewashed cubic houses stacked on a caldera cliff, cobalt domes and doors,
magenta bougainvillea spilling over a white terrace wall, and a sparkling Aegean sea (original design, no crosses or
landmarks). Run: python3 -I santorini-putih.py [part ...]  parts: village bougain sprig bloom domes sea"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c4_lib import *

OUT = outdir("santorini-putih")
PARTS = sys.argv[1:] or ["village", "bougain", "sprig", "bloom", "domes", "sea"]
WHITE, WHITE_S, WHITE_D = "#fbfaf5", "#dfe5ee", "#c3cede"
COB, COB_D, COB_L = "#1f4fa8", "#163a80", "#3f72c9"
MAG, MAG_D, MAG_L = "#c21f74", "#8f1456", "#e85a9e"
LEAF, LEAF_D = "#4f7d3a", "#2f5426"
SEA, SEA_D, SEA_L = "#1d5fa6", "#123f7a", "#3f8fd0"


def bract(cx, cy, r, ang, rng):
    """Papery heart-shaped bougainvillea bract."""
    pts = []
    for i in range(20):
        t = i / 19 * math.tau
        x = math.sin(t) ** 3
        y = -(0.8 * math.cos(t) - 0.3 * math.cos(2 * t) - 0.12 * math.cos(3 * t))
        pts.append((x * r * 0.95, y * r))
    ca, sa = math.cos(ang), math.sin(ang)
    return deform([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], rng, 1, r * 0.015)


def bougain_cluster(W, H, cx, cy, s, rng, items):
    """Collect bract polys, florets and leaves for a cluster at (cx, cy)."""
    n = rng.randint(2, 4)
    for k in range(n):
        a = rng.uniform(0, math.tau)
        d = rng.uniform(0, 1) * s * 0.75
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.8
        base_a = rng.uniform(0, math.tau)
        for j in range(3):
            aa = base_a + j * math.tau / 3
            r = s * rng.uniform(0.55, 0.7)
            items["bracts"].append((bract(x + math.cos(aa) * r * 0.55, y + math.sin(aa) * r * 0.55, r, aa + math.pi / 2, rng), rng.random()))
            for dv in (-0.35, 0.0, 0.35):
                items.setdefault("veins", []).append(([(x, y), (x + math.cos(aa + dv) * r * 0.8, y + math.sin(aa + dv) * r * 0.8), (x + math.cos(aa + dv * 1.5) * r * 1.3, y + math.sin(aa + dv * 1.5) * r * 1.3)], max(0.8, r * 0.035)))
        items["florets"].append((x, y, s * 0.07))
    for k in range(rng.randint(2, 4)):
        a = rng.uniform(0, math.tau)
        L = s * rng.uniform(0.9, 1.3)
        x, y = cx + math.cos(a) * s * 0.9, cy + math.sin(a) * s * 0.8
        items["leaves"].append(petal_pts(x, y, L, L * 0.36, a, n=14))


def paint_bougain(art, W, H, items, nx, rng):
    if items["leaves"]:
        lm = shapes(W, H, items["leaves"])
        art = GP(art, lm, LEAF, LEAF_D, seed=nx(), rough=1.2, streak=1.0)
        art = over(art, flat(lm * light_mask(H, W, W * 0.7, H * 0.1, max(W, H)), "#86b05a", 0.35))
    groups = [[], [], []]
    for p, t in items["bracts"]:
        groups[0 if t < 0.4 else (1 if t < 0.8 else 2)].append(p)
    for g, (ca, cb) in zip(groups, [(MAG, MAG_L), (MAG_D, MAG), ("#e0679f", "#f191bd")]):
        if g:
            m = shapes(W, H, g)
            art = GP(art, m, ca, cb, seed=nx(), rough=1.0, streak=1.4)
            # papery light on the upper side of each bract
            art = over(art, flat(np.clip(m - np.roll(m, -3, 0), 0, 1) * m, "#f7a9cc", 0.35))
    if items.get("veins"):
        allb = shapes(W, H, [p for p, t in items["bracts"]])
        art = over(art, flat(strokes(W, H, items["veins"]) * allb, "#7a0f47", 0.28))
    if items["florets"]:
        fm = circles(W, H, items["florets"])
        art = GP(art, fm, "#f6f1d8", "#fff8e2", seed=nx(), rough=0.4, pad=6)
        art = over(art, flat(circles(W, H, [(x, y, r * 0.4) for x, y, r in items["florets"]]), "#e7c24a", 0.9))
    return art


def house(W, H, x0, y0, w, h, rng, roof="flat"):
    """Cubic house: front face, shaded side (cool blue-grey), parapet lip; returns masks."""
    front = rect(W, H, x0, y0, x0 + w, y0 + h)
    sd = w * rng.uniform(0.12, 0.22)
    side = poly(W, H, [(x0 + w, y0), (x0 + w + sd, y0 - sd * 0.25), (x0 + w + sd, y0 + h - sd * 0.25), (x0 + w, y0 + h)])
    top = None
    if roof == "vault":
        top = shapes(W, H, [[(x0, y0 + 1)] + [(x0 + w / 2 + math.cos(math.pi + t * math.pi) * w / 2, y0 - math.sin(t * math.pi) * w * 0.22) for t in np.linspace(0, 1, 20)] + [(x0 + w, y0 + 1)]], smooth=False)
    return front, side, top


if "village" in PARTS:
    W, H = 820, 980
    nx = Seq(82000); rng = random.Random(14)
    art = painted_sky(W, H, [(0.0, "#2c66c2"), (0.22, "#5b95da"), (0.38, "#a9cdee"), (1.0, "#cfe3f2")], seed=nx(), streak=0.8)
    # far island across the caldera
    hz = 330
    isl = shapes(W, H, [[(-20, hz + 4), (60, hz - 22), (180, hz - 34), (280, hz - 18), (360, hz - 6), (420, hz + 4)]])
    art = GP(art, isl, "#8da2bf", "#9fb3cc", seed=nx(), rough=2, streak=1)
    # sea: deep blue, lighter near horizon, sparkles on the right (sun up and to the right)
    sea = rect(W, H, -10, hz, W + 10, H + 10)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = GP(art, sea, SEA, SEA_D, seed=nx(), rough=1.0, streak=2.0)
    art = over(art, flat(sea * np.clip(1 - (yy - hz) / 140, 0, 1), "#4f95d2", 0.6))
    # horizontal brush ripples
    rip = []
    for _ in range(260):
        y = rng.uniform(hz + 6, H)
        x = rng.uniform(-40, W)
        L = rng.uniform(14, 50) * (0.4 + (y - hz) / (H - hz))
        rip.append(([(x, y), (x + L * 0.5, y - 1), (x + L, y)], rng.uniform(1.2, 2.6) * (0.5 + (y - hz) / (H - hz))))
    art = over(art, flat(strokes(W, H, rip) * sea, "#6aa9dd", 0.55))
    rip2 = [([(x, y), (x + L, y)], w) for (pts, w) in rip[:120] for x, y, L in [(pts[0][0] + 7, pts[0][1] + 4, (pts[2][0] - pts[0][0]) * 0.6)]]
    art = over(art, flat(strokes(W, H, rip2) * sea, SEA_D, 0.45))
    sp = []
    for _ in range(170):
        y = rng.uniform(hz + 6, H * 0.75)
        x = rng.gauss(W * 0.66, W * 0.18)
        sp.append(([(x - 3, y), (x + rng.uniform(3, 10), y)], rng.uniform(1.0, 2.4)))
    spm = strokes(W, H, sp) * sea
    art = over(art, glow(spm, "#ffffff", radius=2, strength=0.6))
    art = over(art, flat(spm, "#ffffff", 0.95))
    # caldera: the rock slope falls diagonally from the upper left to the sea; the village clings to its top
    def ytop(x):
        return 250 + x * 0.52
    def ybot(x):
        return 430 + x * 0.7
    cliff = shapes(W, H, [[(-20, 236), (300, ytop(300) - 4), (560, ytop(560) + 20), (640, 760), (660, H + 20), (-20, H + 20)]])
    art = GP(art, cliff, "#6a3b33", "#8d5139", seed=nx(), rough=2.5, streak=0.3)
    art = over(art, flat(cliff * np.clip((fbm(W, H, nx(), 60, 3) - 0.45) * 2.2, 0, 1), "#9c6a52", 0.5))
    strata = strokes(W, H, [(curve([(-20 + rng.uniform(-40, 40), y), (250, y + 40), (620, y + 230)], 30), rng.uniform(5, 14), (0.3, 0.3)) for y in range(420, 960, 52)]) * cliff
    art = over(art, flat(strata * np.clip((fbm(W, H, nx(), 30, 3) - 0.35) * 2.5, 0, 1), "#b56c48", 0.5))
    art = over(art, flat(strata * np.clip((fbm(W, H, nx(), 40, 3) - 0.5) * 3, 0, 1), "#8c7b86", 0.45))
    art = over(art, flat(cliff * np.clip((fbm(W, H, nx(), 14, 3) - 0.58) * 4, 0, 1), "#4f2519", 0.4))
    # village: back rows first so lower houses overlap the ones above
    rng2 = random.Random(31)
    tints = [WHITE] * 7 + ["#f6e3cf", "#f4d7cc", "#f1e7c9"]
    hs = []
    for r in range(11):
        t = r / 10
        x = -30 + rng2.uniform(-10, 20)
        while x < 560:
            yb = ytop(x) + (ybot(x) - ytop(x)) * t + rng2.uniform(-6, 6)
            if yb > ybot(x) + 4:
                break
            w = rng2.uniform(44, 86) * (1 - 0.15 * t)
            h = rng2.uniform(32, 56)
            hs.append((x, yb - h, w, h, rng2.random(), rng2.choice(tints)))
            x += w * rng2.uniform(0.7, 1.05)
    doors, wins = [], []
    for (x, y, w, h, r, tint) in hs:
        f = rect(W, H, x, y, x + w, y + h)
        sdw = w * 0.16
        side = poly(W, H, [(x, y), (x - sdw, y + sdw * 0.3), (x - sdw, y + h + sdw * 0.3), (x, y + h)])
        art = GP(art, side, WHITE_S, WHITE_D, seed=nx(), rough=0.5, streak=0.5, pad=4)
        art = GP(art, f, tint, "#f3f1ea" if tint == WHITE else tint, seed=nx(), rough=0.5, streak=0.6, pad=4)
        if r < 0.2:
            v = shapes(W, H, [[(x, y + 1)] + [(x + w / 2 + math.cos(math.pi + q * math.pi) * w / 2, y - math.sin(q * math.pi) * w * 0.2) for q in np.linspace(0, 1, 18)] + [(x + w, y + 1)]], smooth=False)
            art = GP(art, v, "#f4f2ec", WHITE_S, seed=nx(), rough=0.4, pad=4)
        art = over(art, flat(rect(W, H, x, y + h - 3, x + w, y + h + 1), "#c9d4e3", 0.6))
        if rng2.random() < 0.75:
            dx = x + rng2.uniform(0.15, 0.6) * w; dw = min(16, w * 0.2)
            doors.append([(dx, y + h), (dx, y + h * 0.42), (dx + dw / 2, y + h * 0.34), (dx + dw, y + h * 0.42), (dx + dw, y + h)])
        if rng2.random() < 0.55:
            wx = x + rng2.uniform(0.1, 0.7) * w
            wins.append([(wx, y + h * 0.2), (wx + 9, y + h * 0.2), (wx + 9, y + h * 0.36), (wx, y + h * 0.36)])
        # paint doors as we go so later houses cover them
        if doors:
            art = GP(art, shapes(W, H, doors, smooth=False), COB, COB_L, seed=nx(), rough=0.3, pad=4); doors = []
        if wins:
            art = GP(art, shapes(W, H, wins, smooth=False), "#2a5fb7", COB, seed=nx(), rough=0.3, pad=4); wins = []
        # domes sit on some houses
        if r > 0.93 and w > 60:
            dx, dy, rr = x + w / 2, y - 2, w * 0.36
            drum = rect(W, H, dx - rr * 1.05, dy - rr * 0.35, dx + rr * 1.05, dy + 2)
            art = GP(art, drum, WHITE, "#f3f1ea", seed=nx(), rough=0.4, pad=4)
            dmm = shapes(W, H, [[(dx - rr * 1.05, dy - rr * 0.34)] + [(dx + math.cos(math.pi + q * math.pi) * rr * 1.05, dy - rr * 0.35 - math.sin(q * math.pi) * rr) for q in np.linspace(0, 1, 24)] + [(dx + rr * 1.05, dy - rr * 0.34)]], smooth=False)
            art = GP(art, dmm, COB, COB_D, seed=nx(), rough=0.5, streak=1, pad=4)
            art = over(art, flat(gaussian_filter(circles(W, H, [(dx + rr * 0.35, dy - rr * 0.95, rr * 0.3)]) * dmm, 2.5), COB_L, 0.8))
            art = GP(art, np.clip(strokes(W, H, [([(dx, dy - rr * 1.35), (dx, dy - rr * 1.7)], 2.4)]) + circles(W, H, [(dx, dy - rr * 1.74, 3)]), 0, 1), "#f2f0e8", seed=nx(), rough=0.2, pad=4)
    # winding steps down the rock below the village
    stp = []
    for k in range(9):
        x0 = 240 + (k % 2) * 40 + k * 18; y0 = ybot(x0) + 30 + k * 26
        stp.append([(x0, y0), (x0 + 46, y0 + 8)])
    art = over(art, flat(strokes(W, H, [(p_, 3.0) for p_ in stp], cap=False) * cliff, "#efe6da", 0.75))
    # foreground: whitewashed terrace wall with a rounded hand-plastered top
    wy = 716
    wall = shapes(W, H, [[(-20, H + 20), (-20, wy + 8)] + [(x, wy + 3 * math.sin(x / 47) + rng.uniform(-1, 1)) for x in range(0, W + 1, 20)] + [(W + 20, wy + 8), (W + 20, H + 20)]])
    art = GP(art, wall, WHITE, "#f6f4ee", seed=nx(), rough=0.7, streak=0.8)
    cap = np.clip(wall - np.roll(wall, 14, 0), 0, 1)
    art = over(art, flat(gaussian_filter(np.roll(cap, 14, 0), 3) * wall, "#cfdae8", 0.55))
    # a planter (blue) on the wall left
    pot = shapes(W, H, [[(60, wy + 2), (66, wy - 34), (114, wy - 34), (120, wy + 2)]], smooth=False)
    art = GP(art, pot, COB, COB_D, seed=nx(), rough=0.5)
    # bougainvillea: big mass from the top right, and spilling down the wall at the right
    items = {"bracts": [], "florets": [], "leaves": []}
    for _ in range(26):
        t = rng.random()
        x = W - 40 - rng.random() ** 1.4 * 240
        y = 20 + rng.random() ** 1.2 * 220 if t < 0.55 else wy - 90 + rng.random() * 260
        if t >= 0.55:
            x = W - 20 - rng.random() ** 1.3 * 270
        bougain_cluster(W, H, x, y, rng.uniform(24, 40), rng, items)
    for _ in range(4):
        bougain_cluster(W, H, rng.uniform(70, 110), wy - 46 - rng.uniform(0, 20), rng.uniform(14, 20), rng, items)
    stems = [curve([(W + 10, -10), (W - 80, 60), (W - 140, 140), (W - 180, 230)], 30), curve([(W + 10, wy - 40), (W - 120, wy - 30), (W - 220, wy + 40), (W - 260, wy + 160)], 30)]
    art = GP(art, strokes(W, H, [(st, 5) for st in stems]), "#6b4a2e", seed=nx(), rough=0.6)
    art = paint_bougain(art, W, H, items, nx, rng)
    art = add_grain(art, nx(), 0.03)
    fade = np.clip((H - 20 - np.arange(H, dtype=np.float32)) / 150, 0, 1)[:, None]
    art[..., 3] *= fade
    preview(art, "sp-village")
    save(art, f"{OUT}/village.webp", max_w=780, quality=80)
    clear()

if "bougain" in PARTS:
    W, H = 620, 520
    nx = Seq(82200); rng = random.Random(7)
    art = blank(W, H)
    items = {"bracts": [], "florets": [], "leaves": []}
    for _ in range(20):
        x = W - 30 - rng.random() ** 1.2 * 420
        y = 30 + rng.random() ** 1.6 * 380 * (1 - (W - x) / 700)
        bougain_cluster(W, H, x, y, rng.uniform(22, 36), rng, items)
    art = GP(art, strokes(W, H, [(curve([(W + 10, 0), (W - 150, 60), (W - 300, 110), (W - 440, 120)], 30), 5), (curve([(W + 10, 30), (W - 80, 160), (W - 120, 300), (W - 110, 420)], 30), 4)]), "#6b4a2e", seed=nx(), rough=0.6)
    art = paint_bougain(art, W, H, items, nx, rng)
    preview(art, "sp-bougain")
    save(art, f"{OUT}/bougain.webp", max_w=440, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 520, 120
    nx = Seq(82300); rng = random.Random(3)
    art = blank(W, H)
    st = curve([(20, 70), (180, 52), (340, 66), (500, 50)], 50)
    art = GP(art, strokes(W, H, [(st, 2.6)]), "#6b4a2e", seed=nx(), rough=0.4)
    items = {"bracts": [], "florets": [], "leaves": []}
    for x, y, _a in resample(st, 64)[1:-1]:
        bougain_cluster(W, H, x, y + rng.uniform(-6, 6), rng.uniform(12, 16), rng, items)
    art = paint_bougain(art, W, H, items, nx, rng)
    preview(art, "sp-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=340, quality=84)
    clear()

if "bloom" in PARTS:
    W, H = 160, 160
    nx = Seq(82400); rng = random.Random(5)
    art = blank(W, H)
    items = {"bracts": [], "florets": [(80, 80, 6)], "leaves": [petal_pts(80, 80, 70, 26, 0.7, n=14)]}
    for j in range(3):
        aa = -math.pi / 2 + j * math.tau / 3
        items["bracts"].append((bract(80 + math.cos(aa) * 22, 80 + math.sin(aa) * 22, 40, aa + math.pi / 2, rng), j / 3))
    art = paint_bougain(art, W, H, items, nx, rng)
    preview(art, "sp-bloom")
    save(art, f"{OUT}/bloom.webp", max_w=80, quality=86)
    clear()

if "domes" in PARTS:
    # emblem: two blue domes above a little white house with a blue door, bougainvillea at its side
    W, H = 420, 380
    nx = Seq(82500); rng = random.Random(9)
    art = blank(W, H)
    f1, s1, _ = house(W, H, 100, 190, 170, 150, rng)
    f2, s2, _ = house(W, H, 230, 236, 110, 104, rng)
    drum = rect(W, H, 120, 150, 230, 192)
    art = GP(art, np.maximum(f1, drum), WHITE, "#f2f0e9", seed=nx(), rough=0.6)
    art = GP(art, s1, "#c5d1e2", "#aebdd3", seed=nx(), rough=0.6)
    art = GP(art, f2, WHITE, "#f2f0e9", seed=nx(), rough=0.6)
    art = GP(art, s2, "#c5d1e2", "#aebdd3", seed=nx(), rough=0.6)
    edge = outline(np.maximum.reduce([f1, f2, drum]), 3) * (1 - np.maximum(s1, s2))
    art = over(art, flat(gaussian_filter(edge, 0.6), "#9db0cb", 0.55))
    art = over(art, flat(rect(W, H, 100, 190, 270, 200) * f1, "#d3dcea", 0.7))
    dm = [[(118, 152)] + [(175 + math.cos(math.pi + t * math.pi) * 60, 152 - math.sin(t * math.pi) * 66) for t in np.linspace(0, 1, 30)] + [(235, 152)]]
    dmm = shapes(W, H, dm, smooth=False)
    art = GP(art, dmm, COB, COB_D, seed=nx(), rough=0.6, streak=1)
    art = over(art, flat(gaussian_filter(circles(W, H, [(196, 110, 18)]) * dmm, 4), COB_L, 0.8))
    art = GP(art, np.clip(strokes(W, H, [([(175, 86), (175, 64)], 4)]) + circles(W, H, [(175, 60, 6)]), 0, 1), "#f2f0e8", seed=nx(), rough=0.3)
    art = GP(art, shapes(W, H, [[(160, 340), (160, 262), (180, 248), (200, 262), (200, 340)]]), COB, COB_L, seed=nx(), rough=0.4)
    art = GP(art, rect(W, H, 262, 270, 296, 300), COB, seed=nx(), rough=0.3)
    art = GP(art, rect(W, H, 118, 214, 146, 244), COB, seed=nx(), rough=0.3)
    gr = rect(W, H, 70, 340, 360, 352)
    art = GP(art, gr, "#e9e3d6", WHITE_S, seed=nx(), rough=0.6)
    items = {"bracts": [], "florets": [], "leaves": []}
    for _ in range(6):
        bougain_cluster(W, H, rng.uniform(40, 110), rng.uniform(170, 330), rng.uniform(18, 26), rng, items)
    for _ in range(3):
        bougain_cluster(W, H, rng.uniform(320, 380), rng.uniform(220, 320), rng.uniform(16, 22), rng, items)
    art = paint_bougain(art, W, H, items, nx, rng)
    preview(art, "sp-domes")
    save(art, f"{OUT}/domes.webp", max_w=280, quality=84)
    clear()

if "sea" in PARTS:
    # band texture: deep Aegean with brush ripples and sun sparkles (opaque, tiles horizontally well enough)
    W, H = 860, 520
    nx = Seq(82600); rng = random.Random(11)
    art = painted_sky(W, H, [(0, "#1b5aa0"), (0.5, "#164d8d"), (1, "#0f3a70")], seed=nx(), streak=1.4)
    rip = []
    for _ in range(420):
        y = rng.uniform(0, H); x = rng.uniform(-40, W); L = rng.uniform(20, 70)
        rip.append(([(x, y), (x + L * 0.5, y - 1.5), (x + L, y)], rng.uniform(1.5, 3.5)))
    full = np.ones((H, W), np.float32)
    art = over(art, flat(strokes(W, H, rip[:260]), "#3a7fc4", 0.45))
    art = over(art, flat(strokes(W, H, rip[260:]), "#0d335f", 0.4))
    sp = [([(x - 3, y), (x + rng.uniform(3, 9), y)], rng.uniform(1, 2.2)) for x, y in [(rng.uniform(0, W), rng.uniform(0, H)) for _ in range(140)]]
    spm = strokes(W, H, sp)
    art = over(art, flat(spm, "#ffffff", 0.75 * 1.0))
    art = over(art, glow(spm, "#cfe6ff", radius=2.5, strength=0.5))
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/sea.webp", quality=74)
    clear()

kb_total(OUT)
