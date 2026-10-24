"""Batik Semarangan — Semarang pesisir batik: asem arang (tamarind) branches with pinnate leaves and pods, kuntul
(egret) birds, cecek-pitu dot rosettes, ombak (sea wave) border, tumpal teeth. Warm soga reds and indigo on cream,
rendered as wax-resist batik: soaked dye, cream klowong outline, remukan crackle, canting dots.
Run: python3 -I batik-semarangan.py [part ...]   parts: kain tumpal ranting kuntul kembang
Assets -> public/themes/art/batik-semarangan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t1_lib import *

OUT = outdir("batik-semarangan")
PARTS = sys.argv[1:] or ["kain", "tumpal", "ranting", "kuntul", "kembang"]
INDIGO, INDIGO_L = "#1d2a52", "#2a3b6e"
RED, RED_D = "#b03a2b", "#7e2219"
SOGA = "#8a4a26"
CREAM, CREAM_D = "#f1e5c8", "#e2cfa4"
OCHRE = "#d29a3e"
DOT = "#8ea0cc"


def klowong(art, mask, col, px=2.0, alpha=0.95):
    return tint(art, outline(mask, px), col, alpha, pad=6)


def leaf_group(rng, x, y, ang, L, n, lw, lh):
    """Pinnate tamarind leaf: rachis + paired leaflets. Returns (rachis pts, leaflet ellipses)."""
    pts = []; ells = []
    bend = rng.uniform(-0.35, 0.35)
    for i in range(n + 1):
        t = i / n
        a = ang + bend * t
        pts.append((x + math.cos(ang) * L * t + math.cos(a + 1.57) * bend * 18 * t * t, y + math.sin(ang) * L * t + math.sin(a + 1.57) * bend * 18 * t * t))
    for i in range(1, n):
        px_, py_ = pts[i]
        a = ang + bend * i / n
        k = 1 - 0.35 * (i / n)
        for side in (-1, 1):
            la = a + side * 1.05
            cx = px_ + math.cos(la) * lw * k * 0.95; cy = py_ + math.sin(la) * lw * k * 0.95
            ells.append((cx, cy, lw * k, lh * k, math.degrees(la)))
    ells.append((pts[-1][0] + math.cos(ang) * lw * 0.6, pts[-1][1] + math.sin(ang) * lw * 0.6, lw * 0.8, lh * 0.8, math.degrees(ang)))
    return pts, ells


def pod(x, y, L, ang, curl):
    """Tamarind pod outline (curved, beaded)."""
    top = []; bot = []
    n = 14
    for i in range(n + 1):
        t = i / n
        a = ang + curl * t
        cx = x + sum(math.cos(ang + curl * j / n) * L / n for j in range(i))
        cy = y + sum(math.sin(ang + curl * j / n) * L / n for j in range(i))
        wdt = (7 + 2.2 * math.sin(t * math.pi * 5) ** 2) * (0.5 + 0.5 * math.sin(min(1, t * 1.15) * math.pi) ** 0.4)
        top.append((cx + math.cos(a - 1.57) * wdt, cy + math.sin(a - 1.57) * wdt))
        bot.append((cx + math.cos(a + 1.57) * wdt, cy + math.sin(a + 1.57) * wdt))
    return top + bot[::-1]


def egret_stand(ox, oy, s=1.0, flip=False):
    f = -1 if flip else 1
    P = lambda pts: [(ox + f * x * s, oy + y * s) for x, y in pts]
    body = P([(-42, -8), (-14, -28), (26, -26), (60, -8), (96, 14), (60, 14), (14, 24), (-28, 16)])
    neck = P([(-36, -10), (-58, -42), (-40, -74), (-52, -100)])
    head = P([(-66, -106), (-56, -114), (-44, -110), (-42, -98), (-54, -94)])
    beak = P([(-62, -106), (-110, -98), (-60, -98)])
    legs = [P([(-2, 20), (2, 52), (0, 86)]), P([(16, 20), (24, 50), (26, 84)])]
    toes = [P([(0, 86), (-14, 92)]), P([(0, 86), (10, 92)]), P([(26, 84), (40, 90)]), P([(26, 84), (16, 91)])]
    plumes = [P([(30, -20), (70, -30), (104, -6)]), P([(26, -14), (66, -18), (100, 6)])]
    wingfeathers = [P([(4 + k * 13, -12 + k * 2), (14 + k * 13, 4 + k * 2), (24 + k * 13, -6 + k * 2)]) for k in range(4)]
    return body, neck, head, beak, legs + toes, plumes, wingfeathers


def egret_fly(ox, oy, s=1.0, flip=False, up=1.0):
    f = -1 if flip else 1
    P = lambda pts: [(ox + f * x * s, oy + y * s) for x, y in pts]
    body = P([(-52, -2), (-30, -14), (10, -14), (46, -6), (64, 2), (36, 10), (-10, 12), (-40, 8)])
    head = P([(-70, -14), (-58, -22), (-46, -16), (-48, -4), (-60, -4)])
    neck = P([(-46, -8), (-56, -12)])
    beak = P([(-68, -16), (-104, -10), (-66, -8)])
    wing = [P(petal_pts(-4 + k * 5, -6, (62 + k * 9) * up, 15, math.radians(-118 + k * 13), n=10)) for k in range(6)]
    wing.append(P(ellipse_pts(8, -16, 30, 16, 12, -0.5)))
    wing2 = P([(4, 4), (-6, 30), (20, 52), (36, 34), (30, 8)])
    legs = [P([(56, 2), (110, 8)]), P([(56, 6), (108, 14)])]
    feathers = [P([(-4 + k * 5 + math.cos(math.radians(-118 + k * 13)) * 20, -6 + math.sin(math.radians(-118 + k * 13)) * 20), (-4 + k * 5 + math.cos(math.radians(-118 + k * 13)) * (50 + k * 8) * up, -6 + math.sin(math.radians(-118 + k * 13)) * (50 + k * 8) * up)]) for k in range(6)]
    return body, head, neck, beak, wing, wing2, legs, feathers


def paint_egret_stand(art, W, H, ox, oy, s, flip, rng):
    body, neck, head, beak, legs, plumes, wf = egret_stand(ox, oy, s, flip)
    m = np.maximum(shapes(W, H, [body, head]), strokes(W, H, [(curve(neck, 30), 13 * s, (0, 0))]))
    art = D(art, m, CREAM, "#f7eedb", seed=rs())
    art = klowong(art, m, SOGA, 1.6)
    bm = shapes(W, H, [beak], smooth=False)
    art = D(art, bm, OCHRE, "#e0b053", seed=rs())
    lm = strokes(W, H, [(curve(l, 10), 3.2 * s, (0, 0.2)) for l in legs])
    art = D(art, lm, RED_D, seed=rs())
    pm = strokes(W, H, [(curve(p, 24), 2.2 * s, (0.1, 0.6)) for p in plumes] + [(curve(p, 10), 2.4 * s, (0.2, 0.2)) for p in wf])
    art = tint(art, pm, RED, 0.9, pad=4)
    e = head[2]
    art = tint(art, circles(W, H, [(e[0] - (6 if not flip else -6) * s, e[1] + 1 * s, 2.4 * s)]), INDIGO, 1.0, pad=4)
    # canting dots along the back
    pts = [body[1], body[2], body[3]]
    dots = [(pts[0][0] + (pts[2][0] - pts[0][0]) * t, pts[0][1] + (pts[2][1] - pts[0][1]) * t + 8 * s) for t in np.linspace(0.1, 0.9, 7)]
    art = tint(art, cecek(W, H, dots, 1.6 * s), RED, 0.9, pad=3)
    return art


def paint_egret_fly(art, W, H, ox, oy, s, flip, up, rng):
    body, head, neck, beak, wing, wing2, legs, feathers = egret_fly(ox, oy, s, flip, up)
    m = shapes(W, H, [body, head, wing2] + wing)
    art = D(art, m, CREAM, "#f7eedb", seed=rs())
    art = klowong(art, m, SOGA, 1.5)
    art = D(art, shapes(W, H, [beak], smooth=False), OCHRE, seed=rs())
    art = D(art, strokes(W, H, [(l, 2.6 * s, (0, 0.3)) for l in legs]), RED_D, seed=rs())
    art = klowong(art, shapes(W, H, wing[:-1]), SOGA, 1.1, 0.7)
    art = tint(art, strokes(W, H, [(f_, 1.8 * s, (0.2, 0.5)) for f_ in feathers]), RED, 0.8, pad=3)
    art = tint(art, circles(W, H, [(head[2][0] + (-4 if not flip else 4) * s, head[2][1] - 2 * s, 2.2 * s)]), INDIGO, 1.0, pad=3)
    return art


def cecek_pitu(cx, cy, r=2.2, d=6.0):
    return [(cx, cy)] + [(cx + math.cos(a) * d, cy + math.sin(a) * d) for a in np.linspace(0, 2 * math.pi, 7)[:-1]]


def kembang(art, W, H, cx, cy, R, rng, cols=(RED, CREAM, OCHRE)):
    """Small batik rosette: 8 petals with a cecek heart."""
    petals = [petal_pts(cx, cy, R, R * 0.5, a, n=10) for a in np.linspace(0, 2 * math.pi, 9)[:-1] + rng.uniform(0, 0.4)]
    m = shapes(W, H, petals)
    art = D(art, m, cols[0], RED_D, seed=rs())
    art = klowong(art, m, cols[1], 1.5)
    art = tint(art, circles(W, H, [(cx, cy, R * 0.26)]), cols[2], 1, pad=4)
    art = tint(art, cecek(W, H, cecek_pitu(cx, cy, d=R * 0.55), R * 0.07 + 0.8), cols[1], 0.95, pad=3)
    return art


random.seed(31)

if "kain" in PARTS:
    W, H = 780, 880
    rng = random.Random(5)
    full = np.ones((H, W), np.float32)
    art = dye(full, INDIGO, INDIGO_L, seed=3, mottle=0.1)
    art[..., 3] = 1
    # background isen: cecek-pitu clusters + scattered dots
    pts = []
    for y in range(30, H - 120, 46):
        for x in range(20 + (y // 46 % 2) * 23, W, 46):
            if rng.random() < 0.55:
                pts += cecek_pitu(x + rng.uniform(-4, 4), y + rng.uniform(-4, 4), d=4.6)
            else:
                pts.append((x + rng.uniform(-6, 6), y + rng.uniform(-6, 6)))
    art = tint(art, cecek(W, H, pts, 1.45), DOT, 0.75, pad=2)
    clear()
    # trunk + branches (asem arang: gnarled, dark soga)
    br = [
        (curve([(70, 900), (110, 760), (96, 640), (150, 520), (230, 420), (330, 340)], 80), 64, (0, 0.5)),
        (curve([(150, 520), (90, 430), (40, 360), (-10, 330)], 50), 30, (0, 0.6)),
        (curve([(300, 360), (420, 290), (540, 270), (660, 210), (800, 190)], 70), 30, (0, 0.85)),
        (curve([(420, 292), (470, 200), (520, 120), (600, 60)], 50), 16, (0, 0.85)),
        (curve([(230, 420), (250, 300), (220, 200), (250, 110)], 50), 18, (0, 0.85)),
        (curve([(560, 268), (640, 330), (720, 350), (800, 340)], 50), 14, (0, 0.85)),
        (curve([(96, 640), (40, 600), (-10, 600)], 30), 20, (0, 0.6)),
    ]
    tm = strokes(W, H, br)
    tm = np.clip(gaussian_filter(tm, 0.6), 0, 1)
    art = D(art, tm, SOGA, RED_D, seed=rs())
    art = remukan(art, tm, RED_D, seed=rs(), strength=0.5, scale=14)
    # bark isen: rows of cream dots along the trunk
    bark = []
    for c, w_, _ in br[:3]:
        for i in range(2, len(c) - 3, 2):
            bark.append(c[i])
    art = tint(art, cecek(W, H, [(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3)) for x, y in bark], 1.8), CREAM_D, 0.8, pad=2)
    art = klowong(art, tm, CREAM, 2.2)
    clear()
    # leaves: three colour groups of pinnate leaves along branches
    anchors = []
    for c, w_, _ in br[1:]:
        for i in range(6, len(c) - 1, 7):
            anchors.append(c[i])
    groups = {CREAM: [], OCHRE: [], RED: []}
    rachis = []
    for k, (x, y) in enumerate(anchors):
        for j in range(rng.choice([2, 3])):
            ang = rng.uniform(-math.pi, math.pi)
            if y < 120:
                ang = rng.uniform(0.2, 2.9)
            pts_, ells = leaf_group(rng, x, y, ang, rng.uniform(70, 120), rng.choice([6, 7, 8]), 11, 5.2)
            col = [CREAM, CREAM, OCHRE, RED][(k + j) % 4]
            groups[col] += ells
            rachis.append((pts_, 1.2, (0, 0.3)))
    for col, ells in groups.items():
        lm = ellipses(W, H, ells)
        art = D(art, lm, col, mix(col, "#ffffff", .15), seed=rs())
        art = klowong(art, lm, CREAM if col == RED else SOGA, 1.0, 0.8)
        clear()
    art = tint(art, strokes(W, H, rachis), RED_D, 0.55, pad=3)
    # pods
    pods = [pod(x + rng.uniform(-5, 5), y, rng.uniform(46, 70), rng.uniform(1.2, 1.9), rng.uniform(-0.7, 0.7)) for x, y in anchors[1::3]]
    pm = shapes(W, H, pods)
    art = D(art, pm, "#a3602c", "#8a4a26", seed=rs())
    art = klowong(art, pm, CREAM, 1.4)
    clear()
    # egrets: one perched on the long branch, two flying
    art = paint_egret_stand(art, W, H, 560, 182, 0.95, False, rng)
    art = paint_egret_fly(art, W, H, 620, 470, 0.95, True, 1.0, rng)
    art = paint_egret_fly(art, W, H, 420, 560, 0.72, True, 0.8, rng)
    clear()
    # rosettes scattered
    for (x, y, R) in [(330, 470, 18), (700, 620, 15), (220, 660, 14), (520, 690, 12), (740, 80, 13)]:
        art = kembang(art, W, H, x, y, R, rng)
    clear()
    # ombak: three rows of pesisir wave scallops at the bottom
    base = H - 118
    rows = [(base, RED, CREAM), (base + 38, CREAM_D, RED), (base + 76, RED_D, CREAM)]
    for r_i, (y0, col, lc) in enumerate(rows):
        polys = []
        off = (r_i % 2) * 30
        for x in range(-60 + off, W + 60, 60):
            pts_ = [(x, y0 + 40)] + [(x + 30 + math.cos(a) * 30, y0 + 22 + math.sin(a) * 22) for a in np.linspace(math.pi, 2 * math.pi, 12)] + [(x + 60, y0 + 40)]
            curl = [(x + 30 + math.cos(a) * 12, y0 + 18 + math.sin(a) * 12) for a in np.linspace(math.pi * 0.9, 2.6 * math.pi, 16)]
            polys.append(pts_)
        wm = np.maximum(shapes(W, H, polys, smooth=False), shapes(W, H, [[(-10, y0 + 38), (W + 10, y0 + 38), (W + 10, H + 10), (-10, H + 10)]], smooth=False))
        art = D(art, wm, col, mix(col, "#000000", .08), seed=rs())
        crest = strokes(W, H, [([(x + 30 + math.cos(a) * 17, y0 + 24 + math.sin(a) * 13) for a in np.linspace(math.pi * 1.1, 1.9 * math.pi, 9)], 2.2, (0.2, 0.2)) for x in range(-60 + off, W + 60, 60)])
        art = tint(art, crest, lc, 0.9, pad=2)
        art = klowong(art, wm, lc if col != CREAM_D else SOGA, 1.6)
        clear()
    # global crackle over the cloth (wax remukan) and a slight warm age
    allm = np.ones((H, W), np.float32)
    art = remukan(art, allm, "#121a36", seed=77, strength=0.2, scale=40)
    art = add_grain(art, 3, 0.03)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/kain.webp", quality=74)
    prev(art, "bs_kain")

if "tumpal" in PARTS:
    # seamless band: row of tumpal teeth (red, cream klowong, indigo inner vein) standing on an indigo hem
    W, H = 192, 64
    rng = random.Random(8)
    art = blank(W, H)
    hem = shapes(W, H, [[(-4, 46), (W + 4, 46), (W + 4, H), (-4, H)]], smooth=False)
    art = D(art, hem, INDIGO, INDIGO_L, seed=4)
    teeth = [[(x, 48), (x + 24, 4), (x + 48, 48)] for x in range(-48, W + 48, 48)]
    tm = shapes(W, H, teeth, smooth=False)
    art = D(art, tm, RED, "#c04a34", seed=5)
    inner = shapes(W, H, [[(x + 12, 46), (x + 24, 20), (x + 36, 46)] for x in range(-48, W + 48, 48)], smooth=False)
    art = D(art, inner, INDIGO, seed=6)
    art = klowong(art, np.maximum(tm, hem), CREAM, 1.4)
    art = tint(art, cecek(W, H, [(x + 24, 12 + k * 7) for x in range(-48, W + 48, 48) for k in range(0, 1)] + [(x, 55) for x in range(6, W, 12)], 1.5), CREAM, 0.95, pad=2)
    art = remukan(art, np.maximum(tm, hem), "#4a1610", seed=9, strength=0.25, scale=10)
    save_full(art, f"{OUT}/tumpal.webp", quality=84)
    prev(art, "bs_tumpal", bg="#f1e5c8")

if "ranting" in PARTS:
    # divider: a horizontal asem sprig with a pod and a cecek-pitu either side
    W, H = 460, 96
    rng = random.Random(12)
    art = blank(W, H)
    stem = curve([(30, 54), (140, 46), (240, 50), (340, 44), (430, 50)], 60)
    sm = strokes(W, H, [(stem, 3.2, (0.1, 0.1))])
    ells_l = []; ells_r = []; rach = []
    for i, (x, y) in enumerate(stem[6:-4:9]):
        for side in (-1, 1):
            ang = side * rng.uniform(0.7, 1.1) - 0.15 + (0 if x < 230 else math.pi * 0)
            ang = (-0.5 if side < 0 else 0.5) + (math.pi if x < 230 else 0) * 0
            pts_, ells = leaf_group(rng, x, y, (-0.55 if side < 0 else 0.55) + (0.25 if x > 230 else -0.25), rng.uniform(34, 44), 5, 6.5, 3.0)
            (ells_l if i % 2 else ells_r).extend(ells)
            rach.append((pts_, 1.0, (0, 0.3)))
    art = D(art, sm, SOGA, seed=3)
    for col, ells in ((RED, ells_l), (SOGA, ells_r)):
        lm = ellipses(W, H, ells)
        art = D(art, lm, col, mix(col, "#ffffff", .12), seed=rs())
    art = tint(art, strokes(W, H, rach), RED_D, 0.8, pad=2)
    art = D(art, shapes(W, H, [pod(214, 50, 48, 1.45, 0.5)]), "#a3602c", seed=8)
    art = tint(art, cecek(W, H, cecek_pitu(14, 50, d=5) + cecek_pitu(446, 48, d=5), 1.7), RED, 1, pad=2)
    save(art, f"{OUT}/ranting.webp", quality=86)
    prev(art, "bs_ranting")

if "kuntul" in PARTS:
    W, H = 330, 250
    rng = random.Random(14)
    art = blank(W, H)
    # backing: a red rosette-dotted disc so the cream egret reads on cream paper
    disc = shapes(W, H, [deform(ellipse_pts(165, 128, 118, 108, 22), random.Random(2), 2, 0.05)])
    art = D(art, disc, INDIGO, INDIGO_L, seed=2)
    art = tint(art, cecek(W, H, fill_dots(np.clip(disc - outline(disc, 3), 0, 1), 15, rng, margin=0.9), 1.4), DOT, 0.7, pad=2)
    art = klowong(art, disc, RED, 3.0)
    art = paint_egret_fly(art, W, H, 175, 150, 0.95, True, 0.9, rng)
    art = remukan(art, disc, "#121a36", seed=3, strength=0.22, scale=20)
    save(art, f"{OUT}/kuntul.webp", quality=84)
    prev(art, "bs_kuntul")

if "kembang" in PARTS:
    W, H = 96, 96
    rng = random.Random(3)
    art = kembang(blank(W, H), W, H, 48, 48, 40, rng)
    save(art, f"{OUT}/kembang.webp", quality=86)
    prev(art, "bs_kembang")

kb(OUT)
