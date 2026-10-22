"""Siraman Adat — Javanese pre-wedding bathing rite in pastel green & ivory, gouache + watercolour: a terracotta kendi
pouring a ribbon of water, a top-down clay jambangan of kembang setaman (rose, melati, kenanga, kanthil petals on
water), plaited janur band, a pair of cengkir gading, a coconut-shell gayung, pandan-and-melati sprig, falling petal.
Run: python3 -I siraman-adat.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f6_lib import *

OUT = outdir("siraman-adat")
PARTS = sys.argv[1:] or ["kendi", "setaman", "janur", "cengkir", "gayung", "sprig", "petal"]
CLAY, CLAY_D, CLAY_L = "#bf6a43", "#7f3b22", "#e9a67f"
WATER, WATER_D = "#a9d3cb", "#5f9e98"
JANUR, JANUR_D, JANUR_L = "#e7dc8e", "#a99b4c", "#f6f0c4"
ROSE, ROSE_D, ROSE_L = "#d0606a", "#8a2a3a", "#f1b9b4"
SAGE, SAGE_D = "#9fbf8e", "#55794c"


def petal_scatter(art, W, H, items, rng, nx):
    """items: (x, y, kind, size, ang). kinds: rose, melati, kenanga, kanthil."""
    for x, y, kind, s, a in items:
        if kind == "rose":
            shell = deform([(x + math.cos(t) * s * 0.78 * (1 - 0.18 * max(0, math.cos(t - a)) ** 6) * (1 + 0.1 * math.cos(2 * (t - a))), y + math.sin(t) * s * 0.66) for t in [i / 16 * math.tau for i in range(16)]], rng, 2, 0.07)
            m = shapes(W, H, [xf([(px - x, py - y) for px, py in shell], x, y, 1, a)])
            art = G(art, np.roll(np.roll(m, 3, 0), 2, 1), "#6f8f88", seed=nx(), density=0.2, edge=0.1, bloom=0, rough=2, feather=2.5, pad=10)
            c = rng.choice([ROSE, ROSE, "#e07f86", "#c24a5a", "#e9a2a4"])
            art = G(art, m, mix(c, ROSE_L, rng.uniform(0, .3)), c, seed=nx(), density=0.78, edge=0.7, bloom=0.35, rough=2, pad=8)
            bx, by = x - math.cos(a) * s * 0.6, y - math.sin(a) * s * 0.6
            art = G(art, spot(m, bx, by, s * 0.9), ROSE_D, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=1, pad=6)
        elif kind == "melati":
            art = jw.white_flower(art, W, H, x, y, s, rng, nx, rot=a)
        elif kind == "kenanga":
            polys = [deform(petal_pts(x, y, s * rng.uniform(1.9, 2.3), s * 0.22, a + k * 1.05 + rng.uniform(-.15, .15), n=12, cup=0.3), rng, 1, 0.08) for k in range(6)]
            m = shapes(W, H, polys)
            art = G(art, m, "#e6d36a", "#b5aa45", seed=nx(), density=0.78, edge=0.55, bloom=0.3, rough=1.5, pad=8)
        elif kind == "kanthil":
            polys = [petal_pts(x, y, s * 1.8, s * 0.42, a + (k - 2) * 0.32, n=12) for k in range(5)]
            m = shapes(W, H, polys)
            art = G(art, np.roll(np.roll(m, 3, 0), 2, 1), "#87a39c", seed=nx(), density=0.25, edge=0.1, bloom=0, rough=2, feather=2.5, pad=8)
            art = GP(art, m, "#fbf4de", "#e8d9b0", seed=nx(), rough=1.0, pad=8)
            art = G(art, edge_of(m), "#b3a07a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    return art


def kendi_local():
    """Kendi outline pieces in local units (body radius 1, origin at the belly centre, spout to the upper LEFT)."""
    body = ellipse_pts(0, 0, 1.0, 0.9, 40)
    neck = [(-0.17, -0.7), (-0.15, -1.25), (-0.27, -1.42), (-0.29, -1.5), (0.29, -1.5), (0.27, -1.42), (0.15, -1.25), (0.17, -0.7)]
    foot = [(-0.42, 0.8), (0.42, 0.8), (0.46, 0.98), (0.4, 1.02), (-0.4, 1.02), (-0.46, 0.98)]
    # spout: shoulder → bulb ("susu") → narrow tip
    sp = []
    for t in [i / 16 for i in range(17)]:
        x = -0.55 - 0.85 * t; y = -0.5 - 0.72 * t
        r = 0.2 * (1 - t) + 0.05 + 0.13 * math.exp(-((t - 0.45) / 0.18) ** 2)
        sp.append((x, y, r))
    top = [(x - r * 0.65, y + r * 0.76) for x, y, r in sp]
    bot = [(x + r * 0.65, y - r * 0.76) for x, y, r in sp]
    spout = top + bot[::-1]
    tip = sp[-1][:2]
    return body, neck, foot, spout, tip


if "kendi" in PARTS:
    W, H = 600, 760
    nx = Seq(61100); rng = random.Random(3)
    art = blank(W, H)
    R, ox, oy, ang = 118, 430, 230, -0.8
    body, neck, foot, spout, tip = kendi_local()
    P = lambda pts: xf(pts, ox, oy, R, ang)
    mb = shapes(W, H, [P(body)]); mn = shapes(W, H, [P(neck)], smooth=False); mf = shapes(W, H, [P(foot)], smooth=False)
    ms = shapes(W, H, [P(spout)])
    allm = np.maximum.reduce([mb, mn, mf, ms])
    tx, ty = P([tip])[0]
    # water ribbon: falls from the tip, bends down-left, ends in a splash
    path = curve([(tx, ty), (tx - 46, ty + 14), (tx - 92, ty + 70), (tx - 118, ty + 200), (tx - 126, H - 40)], 90)
    stream = strokes(W, H, [(path, 22, (0.0, 0.04))])
    art = G(art, stream, "#a7d4cc", "#8cc0b8", seed=nx(), density=0.5, edge=0.7, bloom=0.35, rough=2.5, feather=1.2)
    for k, off in enumerate((-6, 1, 7)):
        strand = [(x + off * (1 - i / len(path) * 0.5) + 2.5 * math.sin(i * 0.23 + k * 2), y) for i, (x, y) in enumerate(path)]
        art = G(art, strokes(W, H, [(strand, 4.5, (0.05, 0.15))]), "#6fb0a8", WATER_D, seed=nx(), density=0.38, edge=0.3, bloom=0, rough=1.5)
    art = G(art, strokes(W, H, [([(x + 6, y) for x, y in path[3:-4]], 6, (0.1, 0.2))]), WATER_D, seed=nx(), density=0.35, edge=0.3, bloom=0, rough=1.5)
    hl = strokes(W, H, [([(x - 5, y) for x, y in path[4:-6]], 3.5, (0.2, 0.3))])
    art = OV(art, hl, lambda m: tint(gaussian_filter(m, 0.8), "#f4fbf8", 0.8))
    drops = [(x + rng.choice((-1, 1)) * rng.uniform(16, 30), y + rng.gauss(0, 10), rng.uniform(2.5, 4.5)) for x, y in path[34::9]]
    sx, sy = path[-1]
    drops += [(sx + math.cos(a) * rng.uniform(20, 46), sy - abs(math.sin(a)) * rng.uniform(10, 34), rng.uniform(2.5, 5)) for a in [rng.uniform(math.pi, math.tau) for _ in range(9)]]
    art = G(art, circles(W, H, drops), WATER, WATER_D, seed=nx(), density=0.65, edge=0.7, bloom=0, rough=1, feather=0.6)
    pool = shapes(W, H, [deform(ellipse_pts(sx, sy + 6, 92, 16, 16), rng, 2, 0.04)])
    art = G(art, pool, WATER, "#cfe6df", seed=nx(), density=0.45, edge=0.6, bloom=0.5, rough=3)
    art = G(art, strokes(W, H, [(arc_pts(sx, sy + 6, rr, math.pi * 1.05, math.pi * 1.95, 20, 0.2), 2, None) for rr in (40, 66)]), WATER_D, seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1)
    # petals riding the stream
    art = petal_scatter(art, W, H, [(path[44][0] - 6, path[44][1], "rose", 9, 1.9), (path[62][0] + 4, path[62][1], "melati", 8, 0.4), (sx + 40, sy - 2, "rose", 10, -0.3), (sx - 50, sy + 4, "kenanga", 7, 0.9)], rng, nx)
    # clay body
    art = GP(art, allm, CLAY, mix(CLAY, CLAY_D, .3), seed=nx(), rough=1.4, streak=1.2)
    lx, ly = ox - R * 0.4, oy - R * 0.45
    dark = np.clip((radial(allm, lx, ly, R * 2.1) - 0.35) / 0.65, 0, 1) ** 0.9 * allm
    art = mul(art, gaussian_filter(dark, 3), "#5a2a1c", 1.0, seed=nx())
    art = mul(art, gaussian_filter(dark, 2) ** 2, "#3a1a10", 0.6, seed=nx())
    art = G(art, np.clip(gaussian_filter(mb, 4) * 1.4 - 0.4, 0, 1) * (1 - gaussian_filter(mb, 4)) * 4 * mb, "#e6996d", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    light = spot(mb, lx, ly, R * 0.75) ** 1.1
    art = lift(art, light, "#f4c09c", 0.75, seed=nx())
    art = G(art, spot(ms, *P([(-1.0, -0.98)])[0], R * 0.25), CLAY_L, seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=2)
    art = G(art, shade_side(mn, 6, 0, 3), CLAY_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # mouth (dark opening) + incised cream bands on the shoulder
    mouth = shapes(W, H, [P(ellipse_pts(0, -1.5, 0.26, 0.07, 14))])
    art = G(art, mouth, "#3c1c10", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.8)
    bands = []
    for yy, rx in ((-0.42, 0.9), (-0.3, 0.95)):
        bands.append((P(arc_pts(0, yy, rx, math.pi * 0.12, math.pi * 0.88, 30, 0.18)), 2.6, (0.05, 0.05)))
    zig = []
    for i in range(15):
        t0 = math.pi * (0.16 + 0.68 * i / 14)
        zig.append((P(arc_pts(math.cos(t0) * 0.93, -0.36 + math.sin(t0) * 0.17 + 0.06, 0.035, 0, math.tau, 8)), 4.0, None))
    bands.append((P(arc_pts(0, -0.04, 0.99, math.pi * 0.08, math.pi * 0.92, 30, 0.2)), 2.4, (0.05, 0.05)))
    bm = strokes(W, H, bands + zig) * mb
    art = GP(art, bm, "#f4e3cf", "#e6c9a8", seed=nx(), rough=0.5, streak=0.3, pad=6)
    art = G(art, edge_of(allm, 1.5), "#5b2915", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=0.5)
    # a few melati tied around the neck
    neck_pts = P(arc_pts(0, -1.05, 0.2, math.pi * -0.1, math.pi * 1.1, 14, 0.5))
    art = jw.melati_string(art, W, H, neck_pts + [(neck_pts[-1][0] - 8, neck_pts[-1][1] + 36)], rng, nx, size=6.5)
    preview(art, "sa-kendi", tone="#f6f4ea")
    save(art, f"{OUT}/kendi.webp", max_w=360, quality=82)
    clear()

if "setaman" in PARTS:
    W, H = 620, 620
    nx = Seq(61300); rng = random.Random(5)
    art = blank(W, H)
    cx, cy, R = 310, 310, 286
    rim = circles(W, H, [(cx, cy, R)])
    water = circles(W, H, [(cx, cy, R - 30)])
    art = GP(art, rim, CLAY, CLAY_D, seed=nx(), rough=1.5, streak=1.0)
    art = G(art, rim * radial(rim, cx - 120, cy - 140, R * 1.9) ** 1.4, CLAY_D, seed=nx(), density=0.5, edge=0, bloom=0.2, rough=2)
    art = G(art, ring(W, H, cx, cy, R - 6, 6), CLAY_L, seed=nx(), density=0.45, edge=0.3, bloom=0.2, rough=1.5)
    art = G(art, ring(W, H, cx, cy, R - 24, 10), "#6a3019", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1.5)
    art = OV(art, water, lambda m: tint(m, "#eef5ee"))
    art = G(art, water, WATER, "#c8e3da", seed=nx(), density=0.75, edge=0.55, bloom=0.5, rough=4, mottle=0.8)
    art = G(art, water * radial(water, cx + 60, cy + 70, R) ** 2, WATER_D, seed=nx(), density=0.35, edge=0, bloom=0.4, rough=3)
    rip = [(arc_pts(cx + rng.uniform(-90, 90), cy + rng.uniform(-90, 90), rr, a0, a0 + rng.uniform(1.0, 2.2), 24), 2.0, (0.2, 0.3))
           for rr, a0 in [(rng.uniform(40, 200), rng.uniform(0, 6.2)) for _ in range(12)]]
    art = lift(art, gaussian_filter(strokes(W, H, rip) * water, 0.8), "#f8fcfa", 0.85, seed=nx())
    items = []
    kinds = ["rose"] * 34 + ["melati"] * 12 + ["kenanga"] * 6 + ["kanthil"] * 5
    rng.shuffle(kinds)
    placed = []
    for k in kinds:
        for _ in range(60):
            a = rng.uniform(0, math.tau); d = (rng.random() ** 0.6) * (R - 64)
            x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
            if all(math.hypot(x - px, y - py) > 40 for px, py in placed):
                break
        placed.append((x, y))
        s = {"rose": rng.uniform(26, 34), "melati": rng.uniform(20, 25), "kenanga": rng.uniform(14, 17), "kanthil": rng.uniform(18, 21)}[k]
        items.append((x, y, k, s, rng.uniform(0, math.tau)))
    art = petal_scatter(art, W, H, items, rng, nx)
    preview(art, "sa-setaman", tone="#f6f4ea")
    save(art, f"{OUT}/setaman.webp", max_w=420, quality=80)
    clear()

if "janur" in PARTS:
    W, H = 900, 110
    nx = Seq(61500); rng = random.Random(7)
    art = blank(W, H)
    y0, y1, x0, x1 = 34, 76, 150, 750
    # plaited band: diagonal strips crossing
    a_strips, b_strips = [], []
    step = 26
    for i in range(-4, int((x1 - x0) / step) + 4):
        xa = x0 + i * step
        a_strips.append([(xa, y0), (xa + 11, y0), (xa + 11 + 34, y1), (xa + 34, y1)])
        b_strips.append([(xa + 34, y0), (xa + 45, y0), (xa + 11, y1), (xa, y1)])
    band = shapes(W, H, [deform(rect(x0, y0, x1, y1), rng, 1, 0.004)], smooth=False)
    ma = shapes(W, H, a_strips, smooth=False) * band; mb = shapes(W, H, b_strips, smooth=False) * band
    art = GP(art, band, JANUR_D, "#8d8040", seed=nx(), rough=0.8)
    art = GP(art, mb, mix(JANUR, JANUR_D, .25), JANUR_D, seed=nx(), rough=0.6, streak=1.0)
    art = GP(art, ma, JANUR, JANUR_L, seed=nx(), rough=0.6, streak=1.0)
    art = G(art, edge_of(ma, 1.0), "#8a7c3a", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4, feather=0.4)
    # curled tails at both ends + small hanging tassel strips
    tails = []
    for sgn, xe in ((-1, x0), (1, x1)):
        for k, (dy, L) in enumerate(((-8, 120), (6, 100), (16, 140))):
            p = curve([(xe, (y0 + y1) / 2 + dy), (xe + sgn * L * 0.5, (y0 + y1) / 2 + dy - 18 + k * 10), (xe + sgn * L, (y0 + y1) / 2 + dy + 8 + k * 6),
                       (xe + sgn * (L - 16), (y0 + y1) / 2 + dy + 24 + k * 4)], 40)
            tails.append((p, 7.5 - k, (0.0, 0.45)))
    tm = strokes(W, H, tails)
    art = GP(art, tm, JANUR, JANUR_D, seed=nx(), rough=0.6, streak=0.8)
    art = G(art, edge_of(tm, 1.0), "#8a7c3a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4, feather=0.4)
    preview(art, "sa-janur", tone="#f6f4ea")
    save(art, f"{OUT}/janur.webp", max_w=440, quality=82)
    clear()

if "cengkir" in PARTS:
    W, H = 520, 420
    nx = Seq(61700); rng = random.Random(9)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(260, 384, 220, 18, 16), rng, 1, 0.03)])
    art = G(art, sh, "#4e5d4a", seed=nx(), density=0.25, edge=0.1, bloom=0, rough=3, feather=6)
    for (cx, cy, r, tilt) in ((180, 250, 118, -0.12), (338, 262, 110, 0.14)):
        body = shapes(W, H, [deform(xf([(math.cos(t) * (0.96 + 0.06 * math.sin(t)), math.sin(t) * 1.08 * (1 + 0.12 * (math.sin(t) < 0) * -math.sin(t) * 0.0)) for t in [i / 30 * math.tau for i in range(30)]], cx, cy, r, tilt), rng, 1, 0.01)])
        # ivory-yellow young coconut (cengkir gading), faint ribs, greenish cap
        art = GP(art, body, "#ecd57c", "#d3b552", seed=nx(), rough=1.2, streak=1.2)
        art = mul(art, gaussian_filter(np.clip((radial(body, cx - r * .45, cy - r * .5, r * 2.0) - .3) / .7, 0, 1) * body, 3), "#8a6a1e", 0.9, seed=nx())
        art = lift(art, spot(body, cx - r * .38, cy - r * .4, r * .6) ** 1.2, "#fff5cc", 0.7, seed=nx())
        ribs = [(xf(arc_pts(0, 0.1, rr, -math.pi * 0.42, math.pi * 0.42, 20, 1.1), cx, cy, r, tilt - math.pi / 2), 2.0, (0.2, 0.2)) for rr in (0.4, 0.75)]
        art = mul(art, gaussian_filter(strokes(W, H, ribs) * body, 1.2), "#9c7d2a", 0.5, seed=nx())
        tx, ty = xf([(0, -1.04)], cx, cy, r, tilt)[0]
        cap = shapes(W, H, [deform(ellipse_pts(tx, ty + 6, r * 0.34, r * 0.16, 12, tilt), rng, 1, 0.05)])
        art = G(art, cap, SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.5)
        for k in range(4):
            a = tilt - math.pi / 2 + (k - 1.5) * 0.5
            art = G(art, shapes(W, H, [petal_pts(tx, ty + 4, r * 0.28, r * 0.08, a, n=10)]), "#7d9f6c", SAGE_D, seed=nx(), density=0.7, edge=0.4, rough=1)
        art = G(art, edge_of(body, 1.6), "#8a6f22", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5)
    art = petal_scatter(art, W, H, [(60, 370, "rose", 11, 0.4), (470, 372, "melati", 10, 0), (430, 392, "rose", 9, 2.2)], rng, nx)
    preview(art, "sa-cengkir", tone="#f6f4ea")
    save(art, f"{OUT}/cengkir.webp", max_w=300, quality=82)
    clear()

if "gayung" in PARTS:
    W, H = 460, 300
    nx = Seq(61900); rng = random.Random(11)
    art = blank(W, H)
    # coconut-shell bowl seen from the side-front, wooden handle to the right
    cx, cy, r = 150, 160, 104
    bowl = shapes(W, H, [[(cx - r + 4, cy)] + [(cx + math.cos(t) * r, cy + math.sin(t) * r * 0.82) for t in [i / 20 * math.pi for i in range(1, 20)]] + [(cx + r - 4, cy)]])
    lip = shapes(W, H, [deform(ellipse_pts(cx, cy, r, r * 0.26, 24), rng, 1, 0.01)])
    inner = shapes(W, H, [ellipse_pts(cx, cy + 3, r - 10, r * 0.2, 24)])
    handle = strokes(W, H, [(curve([(cx + r - 26, cy - 6), (cx + r + 80, cy - 34), (cx + r + 200, cy - 64)], 20), 17, (0.0, 0.1))])
    art = GP(art, handle, "#9a6a3c", "#6b4322", seed=nx(), rough=1.0, streak=1.6)
    art = G(art, shade_side(handle, 0, -4, 3), "#4a2d16", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = GP(art, bowl, "#6e4426", "#4a2a15", seed=nx(), rough=1.3, streak=1.4)
    fib = [(curve([(cx + rng.uniform(-r, r) * .9, cy + rng.uniform(4, 30)), (cx + rng.uniform(-r, r) * .8, cy + rng.uniform(30, 70))], 8), 1.2, (0.2, 0.2)) for _ in range(40)]
    art = G(art, strokes(W, H, fib) * bowl, "#9c7048", seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    art = G(art, spot(bowl, cx - 40, cy + 30, r * 0.6), "#a77a50", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=2)
    art = GP(art, lip, "#7b4d2b", "#5b3519", seed=nx(), rough=0.8)
    art = G(art, inner, WATER, "#d7ece5", seed=nx(), density=0.8, edge=0.6, bloom=0.4, rough=1.5)
    art = petal_scatter(art, W, H, [(cx - 30, cy + 2, "rose", 9, 0.2), (cx + 28, cy + 1, "melati", 8, 1.0)], rng, nx)
    art = G(art, edge_of(np.maximum(bowl, handle)), "#3a2010", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    preview(art, "sa-gayung", tone="#f6f4ea")
    save(art, f"{OUT}/gayung.webp", max_w=220, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 640, 640
    nx = Seq(62100); rng = random.Random(13)
    art = blank(W, H)
    ox, oy = 20, 20
    pandan = []
    for a in [0.05, 0.38, 0.7, 1.02, 1.32]:
        L = rng.uniform(430, 560)
        pandan.append(jw.blade(W, H, curve([(ox, oy), (ox + math.cos(a) * L * .5, oy + math.sin(a) * L * .5), (ox + math.cos(a + .28) * L, oy + math.sin(a + .28) * L)], 26), 16))
    pm = shapes(W, H, pandan)
    art = G(art, pm, "#8fb37d", "#4f7a48", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=3)
    art = G(art, pm * shade_side(pm, 0, 5, 4), "#3f6338", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=2)
    art = G(art, strokes(W, H, [(curve([(ox, oy), (ox + math.cos(a) * 260, oy + math.sin(a) * 260)], 12), 1.6, (0.1, 0.5)) for a in [0.05, 0.38, 0.7, 1.02, 1.32]]) * pm, "#3f6338", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=0.5)
    area = np.zeros((H, W), np.float32)
    fl = blank(W, H)
    fl = jw.rose(fl, W, H, 92, 92, 52, rng, nx, ROSE_L, ROSE, ROSE_D, area)
    fl = jw.rose(fl, W, H, 170, 58, 34, rng, nx, "#f6d4cc", "#e39a9c", "#b0505e", area)
    fl = jw.rose(fl, W, H, 58, 170, 32, rng, nx, "#f6d4cc", "#e39a9c", "#b0505e", area)
    art = glaze(knockout(art, area, amount=0.97, grow=3), fl)
    for (p0, p1, p2) in [((60, 60), (260, 170), (470, 130)), ((60, 70), (180, 300), (160, 480)), ((70, 70), (200, 230), (330, 330))]:
        art = jw.melati_string(art, W, H, curve([p0, p1, p2], 90), rng, nx, size=9.5)
    for x, y in [(150, 130), (215, 105), (120, 210), (60, 240)]:
        art = jw.white_flower(art, W, H, x, y, 16, rng, nx)
    art = petal_scatter(art, W, H, [(250, 150, "kanthil", 14, 0.6), (140, 260, "kenanga", 11, 1.4)], rng, nx)
    preview(art, "sa-sprig", tone="#f6f4ea")
    save(art, f"{OUT}/sprig.webp", max_w=320, quality=80)
    clear()

if "petal" in PARTS:
    W, H = 120, 100
    nx = Seq(62300); rng = random.Random(15)
    art = petal_scatter(blank(W, H), W, H, [(30, 50, "rose", 22, 0.15)], rng, nx)
    save(art, f"{OUT}/petal.webp", max_w=48, quality=84)
    clear()
