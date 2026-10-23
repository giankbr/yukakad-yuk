"""Haul & Tahlil — calm memorial art in deep green and cream: a loop of 33 green prayer beads (tasbih) with cream
separators, an imam bead and a silk tassel (gouache), laid with a sprig of jasmine (melati) in watercolour; a jasmine
sprig for corners, a single bloom and a melati-string divider. No figures, no calligraphy.
Run: python3 -I haul-tahlil.py [part ...]   parts: tasbih sprig bloom divider
Assets -> public/themes/art/haul-tahlil/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i1_lib import *

OUT = outdir("haul-tahlil")
PARTS = sys.argv[1:] or ["tasbih", "sprig", "bloom", "divider"]
GREEN, GREEN_D, GREEN_L = "#2f5a46", "#173326", "#5b8a70"
CREAM = "#f4eddc"
GOLD = "#b9975a"
jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = "#7d9a6d", "#4b6b4f", "#2f4a36"


def jasmine(art, W, H, x, y, r, rng, nx, rot=None, petals=6):
    """Melati (Jasminum sambac-like): separate oval petals with pointed tips, cool grey-green shadow, a green eye."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    ps = [deform(petal_pts(x, y, r, r * 0.3, rot + k * math.tau / petals + rng.uniform(-0.08, 0.08), n=12, cup=0.1), rng, 1, 0.04) for k in range(petals)]
    m = shapes(W, H, ps)
    art = G(art, np.roll(np.roll(m, 3, 0), 2, 1) * 0.9, "#8f9a8a", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1.5, feather=2.0, pad=10)
    art = GP(art, m, "#fffdf7", "#f2ede2", seed=nx(), rough=0.9, streak=0.4, pad=8)
    rim = np.clip(m - gaussian_filter(m, 1.3), 0, 1) * 2.4
    art = G(art, np.clip(rim, 0, 1), "#a6ad9c", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5, pad=6)
    veins = strokes(W, H, [([(x, y), (x + math.cos(rot + k * math.tau / petals) * r * 0.7, y + math.sin(rot + k * math.tau / petals) * r * 0.7)], 1.0, (0.1, 0.6)) for k in range(petals)])
    art = G(art, veins * m, "#c8cbbd", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4, feather=0.4, pad=6)
    art = G(art, circles(W, H, [(x, y, r * 0.17)]), "#c9c27a", "#8f9a52", seed=nx(), density=0.85, edge=0.4, rough=0.6, pad=6)
    return art


def sprig(art, W, H, pts, rng, nx, n_flowers=5, n_buds=4, leaf_len=70):
    """Jasmine twig along pts: paired glossy leaves, terminal cyme of white flowers and pink-tipped buds."""
    art = G(art, strokes(W, H, [(pts, 3.2, (0.0, 0.6))]), "#6f7d55", "#4a5a3a", seed=nx(), density=0.85, edge=0.4, rough=1, feather=0.6)
    n = len(pts)
    for k in range(4):
        i = int((k + 0.5) / 4.6 * (n - 1))
        x, y = pts[i]; x2, y2 = pts[min(n - 1, i + 1)]
        a = math.atan2(y2 - y, x2 - x)
        for sgn in (-1, 1):
            art = jw.leaf(art, W, H, x, y, leaf_len * rng.uniform(0.75, 1.0), a + sgn * rng.uniform(0.6, 0.9), rng, nx)
    ex, ey = pts[-1]
    for k in range(n_flowers):
        ang = rng.uniform(-math.pi, math.pi)
        d = rng.uniform(6, 34)
        art = jasmine(art, W, H, ex + math.cos(ang) * d * 1.6, ey + math.sin(ang) * d * 1.6, rng.uniform(19, 26), rng, nx)
    for k in range(n_buds):
        ang = rng.uniform(-math.pi, math.pi)
        d = rng.uniform(40, 70)
        bx, by = ex + math.cos(ang) * d, ey + math.sin(ang) * d
        m = shape_mask(W, H, petal_pts(bx, by, 22, 8, ang, n=10))
        art = G(art, m, "#fbf6ee", "#e8c9c4", seed=nx(), density=0.85, edge=0.5, bloom=0, rough=1, pad=6)
        art = G(art, strokes(W, H, [([(ex + math.cos(ang) * (d - 12), ey + math.sin(ang) * (d - 12)), (bx, by)], 1.8, None)]), "#7d8a5a", seed=nx(), density=0.7, edge=0.2, rough=0.5, feather=0.4, pad=6)
    return art


def bead(W, H, x, y, r, col, col2, rng, nx, art):
    m = circles(W, H, [(x, y, r)])
    art = over(art, soft_shadow(m, "#0c1a12", blur=2.2, strength=0.45, dx=2, dy=3))
    art = GP(art, m, col, col2, seed=nx(), rough=0.5, streak=0.35, pad=6)
    shade = circles(W, H, [(x + r * 0.35, y + r * 0.4, r * 0.85)]) * m
    art = G(art, np.clip(m - circles(W, H, [(x - r * 0.25, y - r * 0.3, r * 0.95)]), 0, 1), "#0b1a12", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.8, pad=6)
    hi = gaussian_filter(circles(W, H, [(x - r * 0.38, y - r * 0.42, r * 0.26)]), 1.0)
    art = OV(art, hi, lambda mm: tint(mm, "#f3f7ec", 0.8), pad=6)
    return art


if "tasbih" in PARTS:
    W, H = 600, 720
    nx = Seq(50100); rng = random.Random(51)
    art = blank(W, H)
    # teardrop loop, pinched towards the imam bead at the bottom
    cx, cy = 300, 280
    loop = []
    N = 33
    ctrl = [(300, 66), (430, 92), (500, 210), (478, 340), (400, 440), (322, 500), (300, 512), (278, 500), (200, 440), (122, 340), (100, 210), (170, 92)]
    path = curve(ctrl + ctrl[:3], 600)
    # keep one full revolution: from first ctrl to its repeat
    pts = path[: int(len(path) * 12 / 14)]
    # resample by arc length
    seg = [0.0]
    for i in range(1, len(pts)):
        seg.append(seg[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    total = seg[-1]
    # thread under the beads
    art = G(art, strokes(W, H, [(pts, 1.6, None)]), "#8a7a52", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.4)
    beads = []
    j = 0
    gap_lo, gap_hi = total * 0.47, total * 0.53  # leave room at the bottom for the imam bead
    usable = [d for d in np.linspace(0, total, 400)]
    for k in range(N + 2):
        d = (k + 0.5) / (N + 2) * total
        while j < len(seg) - 1 and seg[j] < d:
            j += 1
        beads.append((pts[j], k))
    # paint back to front (top first so lower beads overlap)
    for (p, k) in sorted(beads, key=lambda b: b[0][1]):
        x, y = p
        if abs(x - 300) < 40 and y > 470:
            continue
        if k in (11, 23):
            art = bead(W, H, x, y, 10, "#efe4c8", "#d4c29a", rng, nx, art)
        else:
            art = bead(W, H, x, y, 15, GREEN, GREEN_D, rng, nx, art)
    clear()
    # imam bead (elongated), cap, and the silk tassel
    imam = shape_mask(W, H, ellipse_pts(300, 528, 15, 26, 16))
    art = over(art, soft_shadow(imam, "#0c1a12", blur=2.5, strength=0.45, dx=2, dy=3))
    art = GP(art, imam, GREEN, GREEN_D, seed=nx(), rough=0.5, streak=0.4)
    art = OV(art, gaussian_filter(shape_mask(W, H, ellipse_pts(294, 516, 4, 9, 10)), 1), lambda m: tint(m, "#f3f7ec", 0.75))
    cap = shapes(W, H, [[(288, 552), (312, 552), (316, 566), (284, 566)]])
    art = GP(art, cap, GOLD, "#8a6d3a", seed=nx(), rough=0.4)
    threads = []
    for k in range(30):
        x0 = 300 + rng.uniform(-10, 10)
        sway = rng.uniform(-6, 6)
        L = rng.uniform(110, 140)
        threads.append((curve([(x0, 566), (x0 + sway * 0.5 + (x0 - 300) * 0.6, 566 + L * 0.5), (x0 + sway + (x0 - 300) * 1.6, 566 + L)], 20), rng.uniform(1.4, 2.4), (0.0, 0.25)))
    tm = strokes(W, H, threads)
    art = G(art, tm, "#e9dcb8", "#b9975a", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.6, feather=0.5)
    art = G(art, strokes(W, H, threads[::4]), "#8a6d3a", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    knot = polys(W, H, [rect(290, 578, 310, 586)])
    art = GP(art, knot, GOLD, "#8a6d3a", seed=nx(), rough=0.4)
    clear()
    # jasmine sprig laid across the lower left of the loop
    art = sprig(art, W, H, curve([(40, 640), (110, 560), (170, 470), (230, 420)], 40), rng, nx, n_flowers=6, n_buds=5, leaf_len=66)
    show(art, "ht-tasbih")
    save(art, f"{OUT}/tasbih.webp", max_w=420, quality=84)
    clear()

if "sprig" in PARTS:
    W, H = 480, 520
    nx = Seq(50200); rng = random.Random(52)
    art = blank(W, H)
    art = sprig(art, W, H, curve([(30, 500), (120, 400), (220, 300), (330, 190), (400, 120)], 50), rng, nx, n_flowers=7, n_buds=5, leaf_len=80)
    art = sprig(art, W, H, curve([(120, 400), (230, 430), (330, 430)], 30), rng, nx, n_flowers=4, n_buds=3, leaf_len=56)
    show(art, "ht-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=320, quality=82)
    clear()

if "bloom" in PARTS:
    W, H = 160, 160
    nx = Seq(50300); rng = random.Random(53)
    art = blank(W, H)
    for ang in (-2.4, -0.7):
        art = jw.leaf(art, W, H, 80, 80, 58, ang, rng, nx)
    art = jasmine(art, W, H, 80, 84, 44, rng, nx, rot=-1.57)
    show(art, "ht-bloom")
    save(art, f"{OUT}/bloom.webp", max_w=110, quality=84)

if "divider" in PARTS:
    # a slender jasmine twig: hairline stem, small paired leaves, one open bloom and two buds
    W, H = 520, 90
    nx = Seq(50400); rng = random.Random(54)
    art = blank(W, H)
    stem = curve([(20, 52), (140, 44), (260, 48), (380, 42), (500, 46)], 80)
    art = G(art, strokes(W, H, [(stem, 2.2, (0.1, 0.3))]), "#5f7a5c", "#3f5a42", seed=nx(), density=0.85, edge=0.3, rough=0.8, feather=0.5)
    for t, sgn in [(0.12, -1), (0.22, 1), (0.34, -1), (0.66, 1), (0.78, -1), (0.88, 1)]:
        x, y = stem[int(t * 79)]
        art = jw.leaf(art, W, H, x, y, 34, (-0.5 if t < 0.5 else -2.6) * 1.0 + sgn * 0.6, rng, nx)
    art = jasmine(art, W, H, W / 2, 46, 22, rng, nx)
    for bx, ang in [(W / 2 - 46, -2.6), (W / 2 + 46, -0.5)]:
        m = shape_mask(W, H, petal_pts(bx, 44, 16, 6, ang, n=10))
        art = G(art, m, "#fbf6ee", "#dcc6be", seed=nx(), density=0.9, edge=0.6, bloom=0, rough=1, pad=6)
    show(art, "ht-divider", bg="#f4eddc")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
