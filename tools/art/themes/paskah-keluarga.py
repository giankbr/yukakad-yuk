"""Paskah Keluarga — Easter morning in soft watercolour: the empty rock tomb at dawn with the stone rolled away, white
trumpet lilies, painted eggs in a moss nest, spring sprigs. Respectful: no figures.
Run: python3 -I paskah-keluarga.py [part ...]   parts: dawn lilies lily eggs egg sprig
Assets -> public/themes/art/paskah-keluarga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h5_lib import *

OUT = outdir("paskah-keluarga")
PARTS = sys.argv[1:] or ["dawn", "lilies", "lily", "eggs", "egg", "sprig"]
SEQ = Seq(1100)
LEAF, LEAF_D, LEAF_L = "#7f9a58", "#556f3a", "#a9bf7c"
LILAC, LILAC_D = "#b7a3cf", "#8a74ad"
GOLD, PEACH = "#f2cf86", "#f3b99a"
STONE, STONE_D = "#b9ad9c", "#7d7264"


def dawn():
    W, H = 640, 1120
    rng = random.Random(7)
    arr = painted_sky(W, H, [(0, "#c9c4e2"), (0.22, "#e9d3df"), (0.42, "#f8dcc0"), (0.55, "#fbe7bf"), (1, "#f6efd8")], seed=12, streak=0.7, grain=0.5)
    # sunrise glow behind the hill
    sun = circles(W, H, [(250, 640, 60)])
    arr = over(arr, glow(sun, "#fff3cf", radius=70, strength=0.6))
    arr = over(arr, glow(sun, "#fffaf0", radius=16, strength=0.9))
    # soft cloud washes
    for cy, cx, rx, col in [(180, 420, 220, "#e0c9de"), (300, 140, 180, "#f2d2c6"), (460, 520, 160, "#f7dcc7")]:
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, 36, 12), rng, 3, 0.25))
        arr = G(arr, m, col, "#fbeee2", seed=SEQ(), density=0.35, edge=0.4, bloom=0.5, gran=0.3, rough=10, feather=4)
    flush()
    # far hills (lilac haze) then the green tomb hill
    far = shape_mask(W, H, [(0, 690), (120, 640), (260, 668), (400, 620), (520, 650), (640, 630), (640, 800), (0, 800)])
    arr = G(arr, far, "#bdb3cf", "#cbbfd6", seed=SEQ(), density=0.5, edge=0.4, bloom=0.4, gran=0.3, rough=6, feather=1.5)
    hill = shape_mask(W, H, [(0, 760), (140, 700), (300, 690), (440, 640), (560, 610), (640, 600), (640, H), (0, H)])
    arr = G(arr, hill, "#9fb57a", "#c1cf92", seed=SEQ(), density=0.75, edge=0.5, bloom=0.4, gran=0.4, rough=6, feather=1.4)
    flush()
    # rock face of the tomb (right) with the dark opening
    rock = shape_mask(W, H, deform([(320, 790), (350, 650), (430, 560), (540, 512), (640, 500), (640, 830), (330, 830)], rng, 2, 0.05))
    arr = OV(arr, rock, lambda m: pigment(m, "#cfc4b1", "#ddd3c1", seed=SEQ(), density=1.0, edge=0.3, bloom=0.2, gran=0.5, rough=4, feather=1.0))
    arr = G(arr, rock, STONE, "#d3c8b5", seed=SEQ(), density=0.5, edge=0.65, bloom=0.45, gran=0.6, rough=4, feather=1.0)
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    arr = G(arr, rock * np.clip((xs - 0.8) * 5, 0, 1), STONE_D, seed=SEQ(), density=0.4, edge=0.3, bloom=0.3, gran=0.6, rough=3)
    # strata cracks, dry brush
    cracks = strokes(W, H, [(curve([(380, 640), (450, 600), (520, 590)], 10), 2.5, (0.2, 0.5)), (curve([(560, 540), (610, 560), (640, 556)], 8), 2.5, (0.2, 0.4)),
                             (curve([(360, 720), (400, 700)], 6), 2.2, (0.2, 0.5))])
    arr = G(arr, cracks * rock, STONE_D, seed=SEQ(), density=0.6, edge=0.2, rough=1, gran=0.6, holes=0.2)
    door = shape_mask(W, H, deform([(462, 800), (462, 690), (478, 650), (516, 632), (554, 650), (570, 690), (570, 800)], rng, 1, 0.02))
    arr = G(arr, door, "#4a3f35", "#352d25", seed=SEQ(), density=0.92, edge=0.6, bloom=0.15, gran=0.5, rough=2)
    inner = door * shape_mask(W, H, ellipse_pts(516, 790, 50, 40, 10))
    arr = over(arr, glow(inner, "#fff0c6", radius=14, strength=0.45))
    # the round stone rolled aside
    st = shape_mask(W, H, deform(ellipse_pts(386, 760, 58, 60, 14), rng, 1, 0.04))
    arr = OV(arr, st, lambda m: pigment(m, "#d6ccba", seed=SEQ(), density=1.0, edge=0.3, bloom=0.2, gran=0.4, rough=2.5))
    arr = G(arr, st, "#cbbfad", STONE, seed=SEQ(), density=0.5, edge=0.65, bloom=0.4, gran=0.6, rough=2.5)
    sts = st * shape_mask(W, H, ellipse_pts(408, 778, 52, 52, 10))
    arr = G(arr, sts, STONE_D, seed=SEQ(), density=0.35, edge=0.2, bloom=0.2, gran=0.5, rough=2)
    arr = G(arr, ring_mask(W, H, 386, 760, 40, 2.4) * st, STONE_D, seed=SEQ(), density=0.4, edge=0.2, rough=1)
    shadow = shape_mask(W, H, ellipse_pts(420, 822, 80, 12, 10))
    arr = G(arr, gaussian_filter(shadow, 4), "#5f6b45", seed=SEQ(), density=0.35, edge=0.1, rough=2)
    flush()
    # path of light grass + spring meadow flecks
    path = shape_mask(W, H, [(462, 810), (572, 810), (420, 1000), (220, H), (40, H), (330, 920)])
    arr = G(arr, path, "#ead9a8", "#f3e6bf", seed=SEQ(), density=0.5, edge=0.4, bloom=0.5, gran=0.4, rough=8, feather=2)
    dots = []
    for k in range(260):
        y = rng.uniform(720, H)
        dots.append((rng.uniform(0, W), y, rng.uniform(1.6, 3.6) * (0.6 + (y - 720) / 500)))
    cols = ["#fbf8ef", "#f4d68a", LILAC]
    for i, col in enumerate(cols):
        cm = circles(W, H, dots[i::3])
        arr = G(arr, cm, col, seed=SEQ(), density=0.8, edge=0.4, bloom=0, gran=0.2, rough=1.0, feather=0.6)
    flush()
    # olive tree silhouettes (soft) on the left of the hill
    for tx, ty, s_ in [(90, 720, 1.0), (170, 706, 0.7)]:
        tr = strokes(W, H, [(curve([(tx, ty + 10), (tx + 4, ty - 30 * s_), (tx - 4, ty - 60 * s_)], 10), 5 * s_, (0, .4))])
        arr = G(arr, tr, "#6d6152", seed=SEQ(), density=0.6, edge=0.3, rough=1)
        cm = circles(W, H, [(tx + rng.gauss(0, 22 * s_), ty - 70 * s_ + rng.gauss(0, 14 * s_), rng.uniform(12, 22) * s_) for _ in range(10)])
        arr = G(arr, cm, "#8d9a6a", "#a7b07e", seed=SEQ(), density=0.6, edge=0.5, bloom=0.4, gran=0.4, rough=4)
    arr[..., 3] = 1
    preview(arr, "pk-dawn")
    save_rgb(arr, f"{OUT}/dawn.webp", quality=72)


def lily_leaf(W, H, x, y, L, a, rng):
    pts = petal_pts(x, y, L, L * 0.2, a, n=14, cup=0.2)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.05))
    lay = pig(m, LEAF, LEAF_L, seed=SEQ(), density=0.7, edge=0.6, bloom=0.35, gran=0.3, rough=2.5)
    v = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0.05, 0.9, 8)]
    lay = glaze(lay, pig(stroke_mask(W, H, v, max(1.0, L * 0.012)), LEAF_D, seed=SEQ(), density=0.4, edge=0.1, bloom=0, rough=0.6, feather=0.5))
    return lay


def lilies():
    W, H = 760, 900
    rng = random.Random(13)
    art_ = blank(W, H)
    stems = [curve([(330, 900), (340, 640), (300, 420), (250, 300)], 40), curve([(360, 900), (400, 640), (470, 470), (540, 380)], 40),
             curve([(345, 900), (360, 700), (380, 560), (390, 470)], 30)]
    art_ = G(art_, strokes(W, H, [(p, 10, (0, .1)) for p in stems]), LEAF_D, LEAF, seed=SEQ(), density=0.8, edge=0.5, rough=1.2, feather=0.7)
    for p in stems:
        for t in (0.2, 0.35, 0.5, 0.65):
            i = int(len(p) * t); x, y = p[i]
            a = math.atan2(p[i + 1][1] - y, p[i + 1][0] - x) + rng.choice([-1, 1]) * rng.uniform(0.3, 0.7) + math.pi
            a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
            art_ = glaze(art_, lily_leaf(W, H, x, y, rng.uniform(110, 170), a, rng))
        flush()
    # buds
    for bx, by, a in [(250, 300, -2.2), (395, 470, -1.6)]:
        pts = petal_pts(bx, by, 120, 26, a, n=14)
        m = shape_mask(W, H, deform(pts, rng, 1, 0.04))
        art_ = glaze(art_, pig(m, "#f4f1df", "#d9dcb0", seed=SEQ(), density=0.7, edge=0.6, bloom=0.3, rough=2))
        art_ = glaze(art_, pig(m * shape_mask(W, H, petal_pts(bx, by, 50, 26, a, n=10)), LEAF_L, seed=SEQ(), density=0.5, edge=0.3, rough=1.5))
    flush()
    for (fx, fy, s_, a) in [(540, 380, 190, -0.5), (300, 500, 175, -2.6), (470, 610, 150, -0.1)]:
        lay = lily_bloom(W, H, fx, fy, s_, a, rng, SEQ)
        art_ = knockout(art_, np.clip(lay[..., 3] * 1.4, 0, 1), 0.9, 1.5)
        art_ = glaze(art_, lay)
        flush()
    preview(art_, "pk-lilies", "#fbf7ec")
    save(art_, f"{OUT}/lilies.webp", max_w=480, quality=80)


def lily():
    W, H = 300, 260
    rng = random.Random(19)
    lay = lily_bloom(W, H, 110, 150, 150, -0.25, rng, SEQ)
    preview(lay, "pk-lily", "#fbf7ec")
    save(lay, f"{OUT}/lily.webp", max_w=150, quality=84)


def painted_egg(W, H, cx, cy, r, ang, rng, base, bands, dots_col):
    pts = egg_pts(cx, cy, r, ang)
    m = shape_mask(W, H, pts)
    lay = pig(m, base, mix(base, "#ffffff", 0.35), seed=SEQ(), density=0.85, edge=0.5, bloom=0.3, gran=0.25, rough=1.2, feather=0.8)
    c, s_ = math.cos(ang), math.sin(ang)
    for k, (t, col, wd) in enumerate(bands):
        y0 = t * r
        pts_b = [(cx + (x * c - y0 * s_), cy + (x * s_ + y0 * c)) for x in np.linspace(-r, r, 24)]
        pts_b = [(x, y + math.sin(i * 1.1) * r * 0.03) for i, (x, y) in enumerate(pts_b)]
        bm = stroke_mask(W, H, pts_b, r * wd, taper=(0.0, 0.0)) * m
        lay = glaze(lay, pig(bm, col, seed=SEQ(), density=0.75, edge=0.4, bloom=0, gran=0.2, rough=0.8, feather=0.5))
    dd = []
    for k in range(9):
        x = rng.uniform(-0.55, 0.55) * r; y = rng.uniform(-0.75, 0.6) * r
        dd.append((cx + x * c - y * s_, cy + x * s_ + y * c, r * rng.uniform(0.05, 0.08)))
    lay = glaze(lay, pig(circles(W, H, dd) * m, dots_col, seed=SEQ(), density=0.8, edge=0.3, bloom=0, rough=0.6, feather=0.5))
    # shading on the lower right, highlight upper left
    sh = m * shape_mask(W, H, ellipse_pts(cx + r * 0.35, cy + r * 0.3, r * 0.8, r * 0.9, 12))
    lay = glaze(lay, pig(gaussian_filter(sh, r * 0.12), "#8a7a8a", seed=SEQ(), density=0.25, edge=0.1, bloom=0.1, rough=1))
    hl = gaussian_filter(shape_mask(W, H, ellipse_pts(cx - r * 0.3, cy - r * 0.45, r * 0.18, r * 0.3, 8, -0.4)), r * 0.08) * m
    lay[..., :3] = lay[..., :3] * (1 - hl[..., None] * 0.5) + hl[..., None] * 0.5
    return lay, m


def nest_ring(W, H, cx, cy, rx, ry, rng, t0, t1):
    """Woven twig ring (an ellipse band) between angles t0..t1 (radians, 0 = right, pi/2 = front)."""
    lay = blank(W, H)
    band = []
    for t in np.linspace(t0, t1, 40):
        band.append((cx + math.cos(t) * rx, cy + math.sin(t) * ry))
    lift = ry * (0.42 if t0 < 1 else 0.1)
    inner = [(cx + math.cos(t) * rx * 0.86, cy + math.sin(t) * ry * 0.4 - lift) for t in np.linspace(t1, t0, 40)]
    m = shape_mask(W, H, band + inner)
    lay = G(lay, m, "#9a8460", "#b39c74", seed=SEQ(), density=0.85, edge=0.5, bloom=0.3, gran=0.5, rough=3)
    items = []
    for k in range(110):
        a0 = rng.uniform(t0, t1); a1 = a0 + rng.uniform(0.25, 0.6) * (1 if t1 > t0 else -1)
        rr = rng.uniform(0.8, 1.02)
        items.append(([(cx + math.cos(t) * rx * rr, cy + math.sin(t) * ry * rr - (1 - rr) * ry * 0.6) for t in np.linspace(a0, a1, 8)], rng.uniform(1.4, 2.8), (0.2, 0.2)))
    lay = G(lay, strokes(W, H, items) * np.clip(gaussian_filter(m, 2) * 1.5, 0, 1), "#5f4c32", "#7a6342", seed=SEQ(), density=0.75, edge=0.3, rough=0.8, feather=0.5)
    return lay, m


def eggs():
    W, H = 640, 400
    rng = random.Random(23)
    cx, cy, rx, ry = 320, 262, 236, 76
    art_, _ = nest_ring(W, H, cx, cy, rx, ry, rng, math.pi * 1.0, math.pi * 2.0)
    moss = circles(W, H, [(cx + rng.uniform(-rx, rx) * 0.8, cy - rng.uniform(4, 30), rng.uniform(5, 10)) for _ in range(50)])
    art_ = G(art_, moss, LEAF, LEAF_L, seed=SEQ(), density=0.8, edge=0.5, bloom=0.3, gran=0.4, rough=3)
    flush()
    specs = [(220, 232, 74, -0.35, "#c9b8e0", [(-0.1, "#8a74ad", 0.12), (0.25, "#f6efd8", 0.07)], "#fbf8ef"),
             (420, 228, 70, 0.32, "#f3d79a", [(0.0, "#e7a86e", 0.14), (-0.42, "#9fb57a", 0.08)], "#fbf8ef"),
             (320, 214, 82, 0.05, "#f6efe2", [(-0.15, "#9fb57a", 0.1), (0.15, "#b7a3cf", 0.1), (0.42, "#f2b8a0", 0.07)], "#e7a86e")]
    for ex, ey, r, a, base, bands, dc in specs:
        lay, m = painted_egg(W, H, ex, ey, r, a, rng, base, bands, dc)
        art_ = knockout(art_, m, 1.0, 1.0)
        art_ = glaze(art_, lay)
        flush()
    front, fm = nest_ring(W, H, cx, cy, rx, ry, rng, 0.0, math.pi)
    art_ = knockout(art_, fm, 1.0, 0.8)
    art_ = over(art_, front)
    flowers = [(cx + rng.uniform(-190, 190), cy + 40 + rng.uniform(-10, 26), rng.uniform(5, 8)) for _ in range(10)]
    art_ = G(art_, circles(W, H, flowers), "#fbf8ef", seed=SEQ(), density=0.95, edge=0.4, rough=1)
    art_ = G(art_, circles(W, H, [(x, y, r * 0.35) for x, y, r in flowers]), "#f2cf86", seed=SEQ(), density=0.9, edge=0.2, rough=0.5)
    preview(art_, "pk-eggs", "#fbf7ec")
    save(art_, f"{OUT}/eggs.webp", max_w=360, quality=82)


def egg():
    W, H = 200, 240
    rng = random.Random(29)
    lay, m = painted_egg(W, H, 100, 126, 84, 0.15, rng, "#c9b8e0", [(-0.2, "#8a74ad", 0.12), (0.15, "#f6efd8", 0.08), (0.45, "#9fb57a", 0.07)], "#fbf8ef")
    preview(lay, "pk-egg", "#fbf7ec")
    save(lay, f"{OUT}/egg.webp", max_w=80, quality=84)


def sprig():
    W, H = 900, 160
    rng = random.Random(31)
    art_ = blank(W, H)
    main = curve([(60, 100), (300, 84), (600, 92), (840, 70)], 50)
    art_ = G(art_, strokes(W, H, [(main, 4, (0.05, 0.2))]), LEAF_D, seed=SEQ(), density=0.75, edge=0.4, rough=0.8, feather=0.6)
    for k in range(12):
        i = rng.randint(3, len(main) - 4); x, y = main[i]
        a = -math.pi / 2 + rng.uniform(-1.2, 1.2)
        art_ = glaze(art_, lily_leaf(W, H, x, y, rng.uniform(34, 56), a if rng.random() < 0.6 else -a, rng))
    flush()
    blossoms = []
    for k in range(34):
        i = rng.randint(len(main) // 2, len(main) - 1); x, y = main[i]
        blossoms.append((x + rng.gauss(0, 18), y + rng.gauss(-10, 12), rng.uniform(5, 8)))
    for k in range(16):
        i = rng.randint(0, len(main) // 3); x, y = main[i]
        blossoms.append((x + rng.gauss(0, 14), y + rng.gauss(-8, 10), rng.uniform(4.5, 7)))
    art_ = G(art_, circles(W, H, blossoms), LILAC, "#cdbfe0", seed=SEQ(), density=0.8, edge=0.6, bloom=0.3, rough=1.4, feather=0.7)
    art_ = G(art_, circles(W, H, [(x, y, r * 0.3) for x, y, r in blossoms]), "#f2cf86", seed=SEQ(), density=0.9, edge=0.2, rough=0.5, feather=0.4)
    preview(art_, "pk-sprig", "#fbf7ec")
    save(art_, f"{OUT}/sprig.webp", max_w=440, quality=82)


for part in PARTS:
    {"dawn": dawn, "lilies": lilies, "lily": lily, "eggs": eggs, "egg": egg, "sprig": sprig}[part]()
    flush()
kb(OUT)
