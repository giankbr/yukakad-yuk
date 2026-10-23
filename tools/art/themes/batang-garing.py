"""Batang Garing — the Dayak Ngaju tree of life as a folk-painted ornament (inspired-by, decorative): spear-trunk on a
balanga jar above the waters, tiered branches that curl at the tips, leaves in red / ochre with black outlines, a
small stylised bird on top. Plus the Kahayan river at dawn (watercolour), a carved-curl border band, a curl corner,
a small bird and a bark-cloth (nyamu) paper tile.
Run: python3 -I batang-garing.py [part ...]  parts: tree river band curl bird bark
Assets -> public/themes/art/batang-garing/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n3_lib import *

OUT = outdir("batang-garing")
PARTS = sys.argv[1:] or ["tree", "river", "band", "curl", "bird", "bark"]
RED, RED_D = "#a3302a", "#7c211d"
OCH, OCH_L = "#d99a2b", "#ecbd55"
BLK = "#1c1612"
WHT = "#f1e6cd"
CREAM = "#efe3c8"


def leaf_poly(x, y, L, wd, ang):
    return petal_pts(x, y, L, wd, ang, n=14)


def paint_leaves(art, W, H, polys, cols, nx, vein=True):
    for col in set(cols):
        ps = [p for p, c in zip(polys, cols) if c == col]
        if not ps:
            continue
        m = shapes(W, H, ps)
        art = GP(art, m, col, mix(col, "#000000", 0.12), seed=nx(), rough=1.4, streak=0.8)
        art = ink(art, outline_out(m, 1.6), BLK, seed=nx(), wear=0.15, rough=0.8)
    if vein:
        items = []
        for p in polys:
            n = len(p)
            a, b = p[0], p[n // 2]
            items.append(([a, ((a[0] * 0.35 + b[0] * 0.65), (a[1] * 0.35 + b[1] * 0.65))], 1.6, (0.05, 0.5)))
        art = ink(art, strokes(W, H, items), BLK, seed=nx(), wear=0.1, rough=0.6)
    return art


def branch_path(x0, y0, side, L, rise, r):
    pts = curve([(x0, y0), (x0 + side * L * 0.42, y0 - rise * 0.22), (x0 + side * L * 0.86, y0 - rise * 0.7), (x0 + side * L, y0 - rise)], 40)
    ex, ey = pts[-1]
    if side > 0:
        cur = spiral_pts(ex - r, ey, r, r * 0.22, 0.0, 1.15, 40, -1)
    else:
        cur = spiral_pts(ex + r, ey, r, r * 0.22, math.pi, 1.15, 40, 1)
    return pts, cur


def tree():
    W, H = 640, 900
    rng = random.Random(11); nx = Seq(200)
    cx = 320
    art = blank(W, H)
    # ---- waters below the jar (three wavy bands)
    waves = []
    for k in range(3):
        y = 862 + k * 13
        pts = [(cx - 230 + k * 26 + i * 6, y + math.sin(i * 0.42 + k) * 4.5) for i in range(int((460 - k * 52) / 6))]
        waves.append((pts, 5.0 - k * 0.8, (0.08, 0.08)))
    art = GP(art, strokes(W, H, waves[1:2]), RED, seed=nx(), rough=1.0)
    art = ink(art, strokes(W, H, [waves[0], waves[2]]), BLK, seed=nx(), wear=0.15)
    # ---- trunk (spear shaft) from the jar to the spearhead
    top = 168
    trunk = [(cx - 13, 790), (cx - 11, 520), (cx - 8, 300), (cx - 6, top + 40), (cx + 6, top + 40), (cx + 8, 300), (cx + 11, 520), (cx + 13, 790)]
    tm = poly_mask(W, H, trunk)
    # ---- branches: 4 tiers, slightly staggered, tips curl inward
    tiers = [(648, 236, 120, 34), (536, 200, 112, 30), (420, 162, 100, 26), (306, 118, 84, 21)]
    items, leaves, lcols, beads, paths = [], [], [], [], []
    for ti, (y, L, rise, r) in enumerate(tiers):
        for side in (-1, 1):
            yy = y + (10 if side < 0 else 0) + rng.uniform(-3, 3)
            pts, cur = branch_path(cx, yy, side, L * rng.uniform(0.96, 1.03), rise, r)
            paths.append((pts, cur))
            wd = 15 - ti * 2.2
            items.append((pts, wd, (0.0, 0.0)))
            items.append((cur, wd * 0.8, (0.0, 0.7)))
            # upright leaves along the branch
            for j, t in enumerate((0.3, 0.52, 0.74)):
                i = int(t * (len(pts) - 1))
                px, py = pts[i]
                ang = -math.pi / 2 + side * (0.25 + 0.1 * j) + rng.uniform(-0.05, 0.05)
                Ll = (62 - ti * 9) * rng.uniform(0.92, 1.06)
                leaves.append(leaf_poly(px, py - 4, Ll, Ll * 0.3, ang))
                lcols.append(RED if (j + ti) % 2 == 0 else OCH)
            # hanging fruit beads under the branch
            for t in (0.42, 0.66):
                i = int(t * (len(pts) - 1))
                px, py = pts[i]
                beads.append((px, py + 16 + ti * -1.5, 6.5 - ti * 0.6))
                items.append(([(px, py + 4), (px, py + 11)], 2.0, None))
    bm = strokes(W, H, items)
    # back leaves first, then the dark wood on top
    art = paint_leaves(art, W, H, leaves, lcols, nx)
    wood = np.maximum(bm, tm)
    art = GP(art, wood, BLK, "#2c221a", seed=nx(), rough=1.2, streak=0.9)
    # red inner line along branches (folk double line) + ochre bands on the shaft
    inner = []
    for pts, cur in paths:
        inner.append((pts[3:], 3.2, (0.1, 0.1)))
        inner.append((cur[:26], 2.6, (0.0, 0.6)))
    dots_w = []
    for pts, cur in paths:
        for i in range(6, len(pts) - 4, 7):
            dots_w.append((pts[i][0], pts[i][1], 1.6))
    art = GP(art, strokes(W, H, inner) * wood, RED, seed=nx(), rough=0.6, streak=0.3)
    art = GP(art, circles(W, H, dots_w), WHT, seed=nx(), rough=0.3)
    bands = []
    for yb in range(250, 780, 46):
        w_ = 13 - (780 - yb) / 120
        bands.append(([(cx - w_, yb), (cx + w_, yb + 3)], 5, None))
    art = GP(art, strokes(W, H, bands) * tm, OCH, seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, beads), OCH_L, OCH, seed=nx(), rough=0.8)
    art = ink(art, outline_out(circles(W, H, beads), 1.4), BLK, seed=nx(), wear=0.1)
    # ---- spearhead + small stylised bird at the top
    head = [(cx, top - 70), (cx + 22, top - 18), (cx + 12, top + 8), (cx + 6, top + 44), (cx - 6, top + 44), (cx - 12, top + 8), (cx - 22, top - 18)]
    hm = shapes(W, H, [head])
    art = GP(art, hm, OCH, OCH_L, seed=nx(), rough=1.0)
    art = ink(art, outline_out(hm, 1.8), BLK, seed=nx(), wear=0.1)
    art = ink(art, strokes(W, H, [([(cx, top - 54), (cx, top + 30)], 3.0, (0.2, 0.2))]), RED_D, seed=nx(), wear=0.1)
    # guard (cross piece) under the head
    gm = shapes(W, H, [[(cx - 44, top + 46), (cx + 44, top + 46), (cx + 30, top + 60), (cx - 30, top + 60)]])
    art = GP(art, gm, RED, seed=nx(), rough=0.8)
    art = ink(art, outline_out(gm, 1.4), BLK, seed=nx(), wear=0.1)
    art = bird_on(art, W, H, cx + 30, top - 30, 0.42, nx, rng)
    # ---- balanga jar
    jar = []
    for i in range(41):
        t = i / 40
        yv = 772 + t * 92
        half = 34 + 74 * math.sin(math.pi * min(1, t * 1.05)) ** 0.8
        if t < 0.08:
            half = 40 - t * 70
        jar.append((cx + half, yv))
    body = jar + [(cx - x + cx, y) for x, y in jar[::-1]]
    jm = shapes(W, H, [body])
    art = GP(art, jm, RED, "#b8402f", seed=nx(), rough=1.2, streak=0.9)
    art = G(art, jm * right_of(W, cx + 10, 70), RED_D, seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=2)
    lip = shapes(W, H, [[(cx - 50, 762), (cx + 50, 762), (cx + 44, 778), (cx - 44, 778)]])
    art = GP(art, lip, BLK, seed=nx(), rough=0.8)
    # shoulder band with ochre teeth (tumpal-like) and white dots
    band = jm * (below(H, 800, 2) - below(H, 826, 2))
    art = GP(art, band, BLK, seed=nx(), rough=0.6)
    teeth = [[(cx - 88 + k * 22, 824), (cx - 77 + k * 22, 803), (cx - 66 + k * 22, 824)] for k in range(8)]
    art = GP(art, shapes(W, H, teeth, smooth=False) * band, OCH, seed=nx(), rough=0.6)
    dots_ = [(cx - 70 + k * 28, 846, 3.4) for k in range(6)]
    art = GP(art, circles(W, H, dots_), WHT, seed=nx(), rough=0.4)
    art = ink(art, outline_out(jm, 1.8), BLK, seed=nx(), wear=0.12)
    art = add_grain(art, 3, 0.05)
    save(art, f"{OUT}/tree.webp", max_w=600, quality=82)
    preview(art, "bg-tree", CREAM)


def bird_on(art, W, H, x, y, s, nx, rng, face=1):
    """Small stylised bird (simple folk silhouette: round body, short beak, curled tail)."""
    S = lambda u, v: (x + u * s * face, y + v * s)
    body = shapes(W, H, [[S(-70, 10), S(-40, -30), S(10, -42), S(48, -30), S(62, -6), S(40, 24), S(-10, 36), S(-50, 30)]])
    headm = circles(W, H, [(*S(54, -40), 26 * s)])
    beak = shapes(W, H, [[S(74, -50), S(104, -40), S(74, -30)]], smooth=False)
    tail = strokes(W, H, [(curve([S(-56, 4), S(-96, -10), S(-118, -40)], 16), 13 * s, (0.05, 0.5)),
                          (curve([S(-56, 8), S(-104, 2), S(-130, -14)], 16), 12 * s, (0.05, 0.5)),
                          (curve([S(-56, 12), S(-100, 18), S(-126, 12)], 16), 11 * s, (0.05, 0.5))])
    legs = strokes(W, H, [([S(-4, 32), S(-8, 62)], 5 * s, None), ([S(16, 30), S(18, 62)], 5 * s, None)])
    sil = np.maximum.reduce([body, headm, tail])
    art = ink(art, legs, BLK, seed=nx(), wear=0.05)
    art = GP(art, sil, BLK, "#2c221a", seed=nx(), rough=0.8)
    art = GP(art, beak, OCH, seed=nx(), rough=0.5)
    wing = shapes(W, H, [[S(-36, -2), S(-4, -26), S(30, -16), S(14, 8), S(-24, 12)]])
    art = GP(art, wing, RED, seed=nx(), rough=0.6)
    wl = strokes(W, H, [([S(-20, 2), S(14, -12)], 3 * s, (0.2, 0.4)), ([S(-16, 8), S(18, -4)], 3 * s, (0.2, 0.4))])
    art = GP(art, wl * wing, OCH_L, seed=nx(), rough=0.4)
    eye = circles(W, H, [(*S(60, -44), 6 * s)])
    art = GP(art, eye, WHT, seed=nx(), rough=0.3)
    art = GP(art, circles(W, H, [(*S(61, -44), 2.6 * s)]), BLK, seed=nx(), rough=0.2)
    return art


def bird():
    W, H = 280, 180
    nx = Seq(400); rng = random.Random(4)
    art = bird_on(blank(W, H), W, H, 150, 100, 1.0, nx, rng)
    art = add_grain(art, 5, 0.05)
    save(art, f"{OUT}/bird.webp", max_w=200, quality=84)
    preview(art, "bg-bird", CREAM)


def river():
    """Kahayan at dawn: pale sky glow, forest banks, broad tea-brown river with light streaks and a long boat."""
    W, H = 900, 460
    nx = Seq(600); rng = random.Random(21)
    art = blank(W, H)
    # dawn glow behind (transparent at top so the cover's bark ground shows through)
    sky = shapes(W, H, [[(-20, 120), (W + 20, 120), (W + 20, 330), (-20, 330)]], smooth=False) * below(H, 110, 120)
    art = G(art, sky, "#f2c27a", "#e9a35c", seed=nx(), density=0.55, edge=0.05, bloom=0.3, rough=8, feather=10)
    sun = circles(W, H, [(650, 262, 46)])
    art = G(art, sun, "#f5b453", "#e78d3c", seed=nx(), density=0.75, edge=0.4, bloom=0.2, rough=3)
    # far hills
    art = G(art, hills(W, H, 250, 26, 3, 0.7) * above(H, 300, 2), "#8a9a9a", "#6f8388", seed=nx(), density=0.55, edge=0.4, bloom=0.4, rough=6)
    # forest bank (far): tree crowns as bumpy silhouette + a few tall emergent trees
    pts = [(-20, H)]
    for x in range(-20, W + 30, 14):
        pts.append((x, 292 - 14 * abs(math.sin(x * 0.045 + 1)) - 9 * abs(math.sin(x * 0.11)) - rng.uniform(0, 5)))
    pts.append((W + 20, H))
    bank = shapes(W, H, [pts], smooth=True) * above(H, 318, 2)
    art = G(art, bank, "#3f5a44", "#2c4334", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=4)
    trunks, crowns = [], []
    for x0 in (90, 250, 470, 800):
        hgt = rng.uniform(56, 80)
        trunks.append(([(x0, 300), (x0 + rng.uniform(-6, 6), 300 - hgt)], 3.2, (0.0, 0.3)))
        for k in range(5):
            crowns.append(ellipse_pts(x0 + rng.uniform(-26, 26), 300 - hgt - rng.uniform(-4, 14), rng.uniform(18, 30), rng.uniform(10, 16), 12))
    art = G(art, strokes(W, H, trunks), "#2c4334", seed=nx(), density=0.8, edge=0.3, bloom=0.1, rough=2)
    art = G(art, shapes(W, H, [deform(c, rng, 2, 0.12) for c in crowns]), "#3c5a43", "#2c4334", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=4)
    # river body
    river_m = shapes(W, H, [[(-20, 314), (W + 20, 310), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    art = G(art, river_m, "#8c7a5a", "#5f6b64", seed=nx(), density=0.85, edge=0.15, bloom=0.25, rough=4)
    art = G(art, river_m * below(H, 360, 90), "#3f4d4a", seed=nx(), density=0.5, edge=0.05, bloom=0.2, rough=6)
    # reflections: sun column + bank reflection
    refl = []
    for k in range(26):
        y = 320 + k * 5.2
        w_ = 70 - k * 1.8 + rng.uniform(-10, 10)
        refl.append(([(650 - w_ / 2 + rng.uniform(-8, 8), y), (650 + w_ / 2 + rng.uniform(-8, 8), y)], 2.6, (0.3, 0.3)))
    art = G(art, strokes(W, H, refl), "#f6c46e", seed=nx(), density=0.8, edge=0.1, bloom=0, rough=1.2, feather=0.6)
    streaks = [([(rng.uniform(0, W), y), (rng.uniform(0, W), y)], rng.uniform(1.2, 2.2), (0.4, 0.4)) for y in np.linspace(340, 450, 18)]
    streaks = [([(x0, y), (x0 + rng.uniform(60, 180), y)], w_, t) for (([(x0, y), _], w_, t)) in streaks]
    art = G(art, strokes(W, H, streaks), "#e9d7b0", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=0.6)
    fr = []
    for (bx, by, d) in ((-10, 470, 1), (W + 10, 470, -1)):
        for k in range(7):
            a = -math.pi / 2 + d * (0.25 + k * 0.17)
            L = rng.uniform(120, 190)
            pts = curve([(bx, by), (bx + math.cos(a) * L * 0.5, by + math.sin(a) * L * 0.5), (bx + math.cos(a) * L + d * 20, by + math.sin(a) * L + L * 0.25)], 20)
            fr.append((pts, 7, (0.05, 0.6)))
            for j in range(3, 19, 2):
                px, py = pts[j]
                fr.append(([(px, py), (px + d * 22, py + 16)], 2.4, (0.1, 0.7)))
                fr.append(([(px, py), (px - d * 6, py + 26)], 2.4, (0.1, 0.7)))
    art = G(art, strokes(W, H, fr), "#2a3a2c", "#1f2b22", seed=nx(), density=0.9, edge=0.3, bloom=0.1, rough=2)
    # long boat (jukung) with a small rower silhouette, ink
    hull = shapes(W, H, [[(250, 372), (410, 372), (432, 362), (420, 378), (396, 386), (266, 386), (238, 378), (228, 364)]])
    rower = np.maximum.reduce([circles(W, H, [(330, 340, 6.5)]), shapes(W, H, [[(322, 348), (338, 348), (342, 372), (318, 372)]]),
                               strokes(W, H, [([(345, 330), (318, 398)], 2.6, None)])])
    art = ink(art, np.maximum(hull, rower), "#231c16", seed=nx(), wear=0.1)
    art = G(art, strokes(W, H, [([(250, 392), (420, 392)], 2.2, (0.3, 0.3)), ([(270, 399), (400, 399)], 1.6, (0.3, 0.3))]), "#2c2a24", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = add_grain(art, 7, 0.05)
    save(art, f"{OUT}/river.webp", max_w=860, quality=78)
    preview(art, "bg-river", CREAM)


def band():
    """Border band: black interlocking curls on an ochre ground with red diamonds, thin black rules."""
    W, H = 760, 84
    nx = Seq(800)
    art = blank(W, H)
    ground = shapes(W, H, [[(0, 10), (W, 10), (W, 74), (0, 74)]], smooth=False)
    art = GP(art, ground, OCH, OCH_L, seed=nx(), rough=1.2, streak=1.0)
    rules = strokes(W, H, [([(0, 12), (W, 12)], 4, None), ([(0, 72), (W, 72)], 4, None)])
    art = ink(art, rules, BLK, seed=nx(), wear=0.15)
    items = []
    step = 76
    for k in range(-1, W // step + 2):
        x = k * step + 38
        items.append((spiral_pts(x - 16, 42, 20, 3, math.pi, 1.0, 34, 1), 5.2, (0.0, 0.6)))
        items.append((spiral_pts(x + 16, 42, 20, 3, 0.0, 1.0, 34, 1), 5.2, (0.0, 0.6)))
        items.append(([(x - 16, 62), (x + 16, 22)], 5.2, None))
    curls = strokes(W, H, items) * ground
    art = ink(art, curls, BLK, seed=nx(), wear=0.18)
    dia = [[(k * step + 76, 30), (k * step + 84, 42), (k * step + 76, 54), (k * step + 68, 42)] for k in range(-1, W // step + 2)]
    art = GP(art, shapes(W, H, dia, smooth=False), RED, seed=nx(), rough=0.6)
    art = add_grain(art, 9, 0.05)
    save_full(art, f"{OUT}/band.webp", size=(570, 63), quality=82)
    preview(art, "bg-band", CREAM)


def curl():
    """Corner ornament: a single curled branch with three leaves and a bead."""
    W, H = 320, 300
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    pts, cur = branch_path(30, 270, 1, 230, 170, 46)
    leaves = []; cols = []
    for j, t in enumerate((0.25, 0.48, 0.7)):
        i = int(t * (len(pts) - 1)); px, py = pts[i]
        leaves.append(leaf_poly(px, py - 4, 74 - j * 6, 22, -math.pi / 2 + 0.35 + j * 0.12)); cols.append(RED if j % 2 == 0 else OCH)
    art = paint_leaves(art, W, H, leaves, cols, nx)
    wood = strokes(W, H, [(pts, 15, (0.0, 0.0)), (cur, 12, (0.0, 0.7))])
    art = GP(art, wood, BLK, "#2c221a", seed=nx(), rough=1.0)
    art = GP(art, strokes(W, H, [(pts[4:], 3.2, (0.1, 0.1)), (cur[:28], 2.6, (0.0, 0.6))]) * wood, RED, seed=nx(), rough=0.5)
    b = circles(W, H, [(pts[22][0], pts[22][1] + 18, 7)])
    art = GP(art, b, OCH_L, OCH, seed=nx(), rough=0.6)
    art = ink(art, outline_out(b, 1.4), BLK, seed=nx())
    art = add_grain(art, 11, 0.05)
    save(art, f"{OUT}/curl.webp", max_w=240, quality=84)
    preview(art, "bg-curl", CREAM)


def bark():
    """Seamless nyamu bark-cloth tile: beaten fibres running horizontally, faint mottling."""
    S = 512
    base = col3(CREAM)[None, None] * np.ones((S, S, 3), np.float32)
    f1 = wrap_noise(S, S, 31, (0.6, 14)) - 0.5
    f2 = wrap_noise(S, S, 32, (1.4, 40)) - 0.5
    big = wrap_noise(S, S, 33, 50) - 0.5
    fine = wrap_noise(S, S, 34, 0.7) - 0.5
    v = 1 + f1 * 0.07 + f2 * 0.045 + big * 0.06 + fine * 0.045
    rgb = base * v[..., None]
    rgb = rgb * (1 - (wrap_noise(S, S, 35, (0.5, 3)) > 0.82)[..., None] * 0.05)
    save_rgb(rgba(rgb, np.ones((S, S), np.float32)), f"{OUT}/bark.webp", quality=70)


for p in PARTS:
    globals()[p]()
    clear()
