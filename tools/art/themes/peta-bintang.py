"""Peta Bintang — a hand-engraved star chart of the wedding night: a planisphere disc of painted indigo night with a
milky-way wash, gold-leaf declination rings, constellation figures and magnitude stars; a separate graduated degree
ring (rotates slowly); a lunar-phase strip; a compass-rose emblem; a constellation divider; a starry sky tile and an
atlas-parchment tile. Run: python3 -I peta-bintang.py [part ...]  parts: chart ring moons rose divider sky parch"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k6_lib import *

OUT = outdir("peta-bintang")
PARTS = sys.argv[1:] or ["chart", "ring", "moons", "rose", "divider", "sky", "parch"]
NAVY, NAVY2, NAVY_D = "#13224a", "#1d3264", "#0a1430"
GOLD, GOLD_L = "#c9a45a", "#ecd79c"
STAR = "#fff4d8"
nx = Seq(400)

CONST = {
    # name: (centre, scale, rotation, stars [(x, y, mag)], lines [(i, j)])
    "orion": ((-0.36, -0.2), 1.55, 0.25, [(-0.08, -0.13, 3), (0.07, -0.11, 2), (-0.03, 0.0, 2), (0.0, 0.012, 2), (0.032, 0.024, 2), (-0.065, 0.13, 2), (0.075, 0.125, 3), (0.0, -0.2, 1)],
              [(0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6), (0, 7), (1, 7)]),
    "crux": ((0.34, 0.44), 1.7, -0.3, [(0, -0.085, 3), (0, 0.085, 3), (-0.06, 0.005, 2), (0.055, -0.012, 2), (0.024, 0.03, 1)], [(0, 1), (2, 3)]),
    "centaur": ((0.55, 0.22), 1.6, 0.0, [(0, 0, 3), (-0.05, -0.04, 3)], [(0, 1)]),
    "scorpius": ((0.4, -0.18), 1.7, 0.4, [(-0.14, -0.12, 2), (-0.1, -0.07, 2), (-0.06, -0.03, 3), (-0.02, 0.02, 1), (0.0, 0.07, 2), (0.03, 0.11, 1), (0.08, 0.13, 2), (0.12, 0.1, 2), (0.13, 0.05, 2), (-0.16, -0.06, 1), (-0.12, -0.16, 1)],
                 [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (1, 9), (1, 10)]),
    "cassiopeia": ((-0.38, 0.5), 1.7, -0.15, [(-0.1, 0.0, 2), (-0.05, 0.05, 2), (0.0, 0.0, 3), (0.05, 0.05, 2), (0.1, -0.01, 2)], [(0, 1), (1, 2), (2, 3), (3, 4)]),
    "lyra": ((-0.68, 0.3), 1.6, 0.2, [(0, -0.05, 3), (-0.02, 0.0, 1), (0.02, 0.0, 1), (-0.03, 0.05, 1), (0.01, 0.05, 1)], [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]),
    "leo": ((-0.06, -0.7), 1.6, 0.0, [(-0.12, 0.03, 3), (-0.08, -0.02, 2), (-0.07, -0.07, 1), (-0.03, -0.09, 2), (0.06, -0.01, 2), (0.12, 0.02, 2), (0.05, 0.04, 1)],
            [(0, 1), (1, 2), (2, 3), (1, 6), (6, 4), (4, 5), (0, 6)]),
    "aquila": ((-0.08, 0.32), 1.5, 0.3, [(0, 0, 3), (-0.03, -0.02, 1), (0.03, 0.02, 1), (-0.06, 0.07, 1), (0.07, -0.06, 1)], [(1, 0), (0, 2), (0, 3), (0, 4)]),
}


def project(c, sc, rot, x, y, R, C):
    ca, sa = math.cos(rot), math.sin(rot)
    u, v = x * ca - y * sa, x * sa + y * ca
    return (C + (c[0] + u * sc) * R, C + (c[1] + v * sc) * R)


def chart():
    W = H = 1120; C = W / 2; R = 500
    disc = circles(W, H, [(C, C, R)])
    art = blank(W, H)
    art = GP(art, disc, NAVY, NAVY2, seed=nx(), rough=1.0, streak=1.2)
    # deeper vignette toward the rim
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - C, yy - C) / R
    art = over(art, flat(disc * np.clip((d - 0.35) * 1.2, 0, 1) ** 1.4, NAVY_D, 0.75))
    # milky way: a soft cloudy band crossing the disc
    band = np.exp(-(((xx - C) * 0.5 + (yy - C) * 0.86 - 40) / 120) ** 2).astype(np.float32)
    cl = fbm(W, H, nx(), 70, 4)
    mw = gaussian_filter(band * np.clip((cl - 0.25) * 1.5, 0, 1), 5) * disc
    art = G(art, mw * 0.8, "#6f86b8", "#9aa7c9", seed=nx(), density=0.42, edge=0.08, bloom=0.0, gran=0.3, rough=4, feather=4, pad=0)
    art = over(art, flat(gaussian_filter(mw, 6) * (fbm(W, H, nx(), 18, 3) > 0.62), "#dfe6ff", 0.22))
    # grid: declination circles + RA spokes + ecliptic (thin gold leaf)
    grid = np.zeros((H, W), np.float32)
    for r in (125, 250, 375):
        grid = np.maximum(grid, circle_line(W, H, C, C, r, 1.6, dash=(7, 6)))
    for k in range(12):
        a = k * math.tau / 12
        grid = np.maximum(grid, polyline_mask(W, H, [[(C + math.cos(a) * 40, C + math.sin(a) * 40), (C + math.cos(a) * (R - 4), C + math.sin(a) * (R - 4))]], 1.1))
    ecl = arc_pts(C + 60, C - 90, 430, 0, math.tau, 160)
    ecl = [(x, y) for x, y in ecl]
    grid = np.maximum(grid, dashed(W, H, ecl + [ecl[0]], 1.8, 3, 7) * disc)
    grid *= disc
    art = FO(art, grid, GOLD, seed=nx(), emboss=0.2, sparkle=0.05)
    art = over(art, flat(grid, NAVY_D, 0.35))  # sink the grid back into the sky
    # faint background stars
    rng = np.random.default_rng(nx())
    pts = []
    for _ in range(900):
        a = rng.uniform(0, math.tau); rr = R * math.sqrt(rng.uniform(0, 0.985))
        pts.append((C + math.cos(a) * rr, C + math.sin(a) * rr, float(rng.choice([0.7, 0.9, 1.1, 1.4], p=[.45, .3, .17, .08]))))
    sm = star_dots(W, H, pts)
    art = over(art, flat(sm, STAR, 0.75))
    # constellations
    lines = np.zeros((H, W), np.float32); big = []; mid = []
    for name, (c, sc, rot, st, ln) in CONST.items():
        P = [project(c, sc, rot, x, y, R, C) for x, y, _ in st]
        for i, j in ln:
            (x0, y0), (x1, y1) = P[i], P[j]
            L = math.hypot(x1 - x0, y1 - y0)
            k0 = 9 / L; k1 = 1 - 9 / L
            lines = np.maximum(lines, polyline_mask(W, H, [[(x0 + (x1 - x0) * k0, y0 + (y1 - y0) * k0), (x0 + (x1 - x0) * k1, y0 + (y1 - y0) * k1)]], 2.0))
        for (x, y), (_, _, m) in zip(P, st):
            (big if m == 3 else mid).append((x, y, {1: 2.4, 2: 3.6, 3: 5.2}[m]))
    art = FO(art, lines, GOLD_L, seed=nx(), emboss=0.15, sparkle=0.1)
    allst = star_dots(W, H, big + mid)
    art = over(art, glow(allst, "#ffe9b8", 7, 0.5))
    art = over(art, flat(allst, STAR, 1.0))
    sp = np.zeros((H, W), np.float32)
    for x, y, r in big:
        sp = np.maximum(sp, fourpoint(W, H, x, y, r * 3.4, 0.14, 0.12))
    art = over(art, flat(gaussian_filter(sp, 0.6), STAR, 0.8))
    # a small painted crescent moon near the rim
    mx, my, mr = C + 300, C + 250, 30
    moon = np.clip(circles(W, H, [(mx, my, mr)]) - circles(W, H, [(mx + 13, my - 9, mr * 0.9)]), 0, 1)
    art = over(art, glow(moon, "#fff0c8", 12, 0.35))
    art = G(art, moon, "#f6e7bf", "#e2cc93", seed=nx(), density=0.95, edge=0.4, rough=1.2, feather=0.8, pad=8)
    # rim: double gold-leaf edge
    rim = np.maximum(ring(W, H, C, C, R + 3, 5), ring(W, H, C, C, R - 10, 1.6))
    art = FO(art, rim, GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    art = add_grain(art, nx(), 0.03)
    prev(art, "pb-chart", bg="#0d1733")
    save_full(art, f"{OUT}/chart.webp", (720, 720), quality=80)


def ring_part():
    W = H = 1120; C = W / 2
    m = np.zeros((H, W), np.float32)
    m = np.maximum(m, circle_line(W, H, C, C, 516, 2.2))
    m = np.maximum(m, circle_line(W, H, C, C, 556, 1.6))
    ticks = []
    for k in range(180):
        a = k * math.tau / 180
        L = 20 if k % 15 == 0 else (12 if k % 5 == 0 else 7)
        ticks.append([(C + math.cos(a) * 518, C + math.sin(a) * 518), (C + math.cos(a) * (518 + L), C + math.sin(a) * (518 + L))])
    m = np.maximum(m, polyline_mask(W, H, ticks, 1.6, cap=False))
    dia = []
    for k in range(12):
        a = k * math.tau / 12 + math.tau / 24
        cx, cy = C + math.cos(a) * 545, C + math.sin(a) * 545
        dia.append([(cx + math.cos(a) * 7, cy + math.sin(a) * 7), (cx + math.cos(a + 1.57) * 3.2, cy + math.sin(a + 1.57) * 3.2),
                    (cx - math.cos(a) * 7, cy - math.sin(a) * 7), (cx - math.cos(a + 1.57) * 3.2, cy - math.sin(a + 1.57) * 3.2)])
    m = np.maximum(m, shapes(W, H, dia, smooth=False))
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.5, sparkle=0.2)
    prev(art, "pb-ring", bg="#0d1733")
    save_full(art, f"{OUT}/ring.webp", (760, 760), quality=80)


def moons():
    W, H = 1100, 190; cy = 95; r = 58
    art = blank(W, H)
    phases = [(1, 0.55, True), (1, 0.35, False), (0, 0, False), (-1, 0.35, False), (-1, 0.55, True)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for k, (side, kk, cres) in enumerate(phases):
        cx = 110 + k * 220
        d = circles(W, H, [(cx, cy, r)])
        art = over(art, flat(d, "#2a3d70", 0.55))  # earthshine
        if side == 0:
            lit = d
        else:
            half = d * ((xx - cx) * side > 0)
            e = ell(W, H, cx, cy, r * kk, r)
            lit = np.clip(half - e, 0, 1) if cres else np.clip(np.maximum(half, e * d), 0, 1)
        art = over(art, glow(lit, "#fff0c8", 10, 0.25))
        art = G(art, lit, "#f4e6c2", "#dccb9a", seed=nx(), density=0.95, edge=0.35, rough=1.0, feather=0.7, pad=6)
        rng = random.Random(nx())
        cr = [(cx + rng.uniform(-r * .6, r * .6), cy + rng.uniform(-r * .6, r * .6), rng.uniform(4, 11)) for _ in range(6)]
        art = G(art, circles(W, H, cr) * lit, "#b8a77d", seed=nx(), density=0.35, edge=0.5, rough=1.5, pad=4)
    prev(art, "pb-moons", bg="#0d1733")
    save(art, f"{OUT}/moons.webp", max_w=640, quality=82)


def rose():
    W = H = 560; C = 280
    art = blank(W, H)
    def pt(a, r):
        return (C + math.cos(a) * r, C + math.sin(a) * r)
    for k in range(16):
        a = -math.pi / 2 + k * math.tau / 16
        L = 250 if k % 4 == 0 else (170 if k % 2 == 0 else 110)
        wd = 0.16 if k % 4 == 0 else 0.2
        tip = pt(a, L); l = pt(a - wd, L * 0.16 + 24); rr = pt(a + wd, L * 0.16 + 24); c = (C, C)
        m1 = shapes(W, H, [[c, l, tip]], smooth=False); m2 = shapes(W, H, [[c, rr, tip]], smooth=False)
        art = FO(art, m1, GOLD_L if k % 4 == 0 else GOLD, seed=nx(), emboss=0.4)
        art = FO(art, m2, "#9c7a3a" if k % 4 == 0 else "#a8864a", seed=nx(), emboss=0.4)
    m = np.maximum(circle_line(W, H, C, C, 150, 2.0), circle_line(W, H, C, C, 140, 1.2, dash=(4, 5)))
    m = np.maximum(m, circles(W, H, [(C, C, 9)]))
    art = FO(art, m, GOLD, seed=nx(), emboss=0.5)
    prev(art, "pb-rose", bg="#0d1733")
    save(art, f"{OUT}/rose.webp", max_w=300, quality=82)


def divider():
    W, H = 760, 130; cy = 65
    st = [(30, 80, 2.2), (120, 52, 3.2), (220, 78, 2.6), (300, 58, 3.0), (380, 65, 0), (460, 72, 3.0), (540, 52, 2.6), (640, 78, 3.2), (730, 50, 2.2)]
    lines = []
    for (x0, y0, _), (x1, y1, _) in zip(st, st[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        k0 = (10 if _ != 0 else 22) / L
        lines.append([(x0 + (x1 - x0) * 8 / L, y0 + (y1 - y0) * 8 / L), (x1 - (x1 - x0) * 8 / L, y1 - (y1 - y0) * 8 / L)])
    lm = polyline_mask(W, H, [l for i, l in enumerate(lines) if i not in (3, 4)], 1.8)
    lm = np.maximum(lm, polyline_mask(W, H, [[(300 + 8, 59), (352, 63)], [(408, 66), (460 - 8, 71)]], 1.8))
    dots = star_dots(W, H, [(x, y, r) for x, y, r in st if r])
    centre = np.maximum(fourpoint(W, H, 380, 65, 30, 0.2), fourpoint(W, H, 380, 65, 16, 0.25, math.pi / 4))
    art = FO(blank(W, H), np.maximum(np.maximum(lm, dots), centre), GOLD, seed=nx(), emboss=0.5, sparkle=0.15)
    prev(art, "pb-divider", bg="#0d1733"); prev(art, "pb-divider-l", tone="#efe5cf")
    save(art, f"{OUT}/divider.webp", max_w=380, quality=84)


def sky():
    W = H = 512
    art = painted_sky(W, H, [(0, "#13224a"), (1, "#13224a")], seed=nx(), streak=0.8, grain=0.6)
    art[..., :3] *= (0.92 + 0.12 * fbm(W, H, nx(), 120, 3))[..., None]
    rng = np.random.default_rng(nx())
    pts = [(float(rng.uniform(6, W - 6)), float(rng.uniform(6, H - 6)), float(rng.choice([0.6, 0.8, 1.1, 1.5], p=[.45, .3, .17, .08]))) for _ in range(140)]
    art = over(art, flat(star_dots(W, H, pts), STAR, 0.7))
    art = tileable(art)
    save_rgb(art, f"{OUT}/sky.webp", quality=74)


def parch():
    W = H = 512
    p = np.asarray(paper(W, H, "#efe5cf", nx(), fiber=0.7, mottle=0.8), np.float32) / 255
    p = p * (0.95 + 0.07 * fbm(W, H, nx(), 140, 3))[..., None]
    arr = np.concatenate([p, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(tileable(arr), f"{OUT}/parch.webp", quality=72)


for part in PARTS:
    {"chart": chart, "ring": ring_part, "moons": moons, "rose": rose, "divider": divider, "sky": sky, "parch": parch}[part]()
    clear()
