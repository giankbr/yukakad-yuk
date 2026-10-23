"""Abu Syari — dove grey and silver, no photos: a hairline 8-fold star rosette ring (silver foil lines), a seamless
hairline khatam lattice, silver-veined grey leaf sprigs in watercolour, a hairline star divider and a small star node.
Run: python3 -I abu-syari.py [part ...]  parts: rosette lattice sprig divider star
Assets -> public/themes/art/abu-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o1_lib import *

OUT = outdir("abu-syari")
PARTS = sys.argv[1:] or ["rosette", "lattice", "sprig", "divider", "star"]
SILVER, SILVER_D = "#b9bdc4", "#8d929b"
SAGE, SAGE_D, SAGE_L = "#a7aeab", "#7d8582", "#c9cecb"
DOVE = "#e7e8ea"


def star8(cx, cy, r, rot=0.0, inner=0.0):
    """8-point star outline (two overlapping squares) as point list for polyline strokes."""
    out = []
    for k in range(2):
        a0 = rot + k * math.pi / 4
        out.append([(cx + math.cos(a0 + j * math.pi / 2) * r, cy + math.sin(a0 + j * math.pi / 2) * r) for j in range(5)])
    return out


def seg_items(polys, w):
    return [(p, w, None) for p in polys]


def silver_lines(W, H, items, nx, base=SILVER):
    m = strokes(W, H, items)
    art = FO(blank(W, H), m, base, seed=nx(), emboss=0.4, sparkle=0.35)
    return art, m


def rosette():
    """Ring rosette: interlaced 8-point stars around a clear centre, concentric hairline circles, a petal crown."""
    W = H = 960
    cx = cy = W / 2
    nx = Seq(100)
    items = []
    for r in (300, 306, 420, 426, 440):
        items.append((arc_pts(cx, cy, r, 0, math.tau, 240), 2.0 if r in (300, 426) else 1.4, None))
    # 16 small 8-point stars around the ring
    for k in range(16):
        a = k * math.tau / 16
        x, y = cx + math.cos(a) * 363, cy + math.sin(a) * 363
        for j in range(8):
            items.append((petal_pts(x, y, 30, 9, a + j * math.pi / 4, n=12) + [petal_pts(x, y, 30, 9, a + j * math.pi / 4, n=12)[0]], 1.3, None))
        items.append((arc_pts(x, y, 7, 0, math.tau, 24), 1.3, None))
    # interlacing chords between neighbouring stars
    for k in range(16):
        a, b = k * math.tau / 16, (k + 1) * math.tau / 16
        items.append(([(cx + math.cos(a) * 306, cy + math.sin(a) * 306), (cx + math.cos(b) * 420, cy + math.sin(b) * 420)], 1.2, None))
        items.append(([(cx + math.cos(a) * 420, cy + math.sin(a) * 420), (cx + math.cos(b) * 306, cy + math.sin(b) * 306)], 1.2, None))
        c = (a + b) / 2
        items.append(([(cx + math.cos(c) * 306, cy + math.sin(c) * 306), (cx + math.cos(c) * 330, cy + math.sin(c) * 330)], 1.0, None))
        items.append(([(cx + math.cos(c) * 396, cy + math.sin(c) * 396), (cx + math.cos(c) * 420, cy + math.sin(c) * 420)], 1.0, None))
    # outer petal crown (pointed arches) + dots
    for k in range(32):
        a = k * math.tau / 32
        b = (k + 1) * math.tau / 32
        m_ = (a + b) / 2
        items.append(([(cx + math.cos(a) * 440, cy + math.sin(a) * 440), (cx + math.cos(m_) * 458, cy + math.sin(m_) * 458), (cx + math.cos(b) * 440, cy + math.sin(b) * 440)], 1.0, None))
    art, m = silver_lines(W, H, items, nx)
    dots = circles(W, H, [(cx + math.cos(k * math.tau / 32 + math.pi / 32) * 433, cy + math.sin(k * math.tau / 32 + math.pi / 32) * 433, 2.6) for k in range(32)])
    art = over(art, FO(blank(W, H), dots, SILVER_D, seed=nx(), emboss=0.6, sparkle=0.4))
    # soft grey wash behind the band so the hairlines sit on something
    band = np.clip(circles(W, H, [(cx, cy, 424)]) - circles(W, H, [(cx, cy, 302)]), 0, 1)
    wash = pigment(band, "#d3d6db", "#c6cad1", seed=nx(), density=0.55, edge=0.5, bloom=0.45, rough=4, gran=0.4)
    art = over(wash, art)
    preview(art, "as-rosette", bg=DOVE)
    save(art, f"{OUT}/rosette.webp", max_w=560, quality=76)


def lattice():
    """Seamless hairline khatam lattice tile (transparent): 8-point stars joined by crosses."""
    W = H = 240
    nx = Seq(300)
    items = []
    for (x, y) in [(0, 0), (240, 0), (0, 240), (240, 240), (120, 120)]:
        for p in star8(x, y, 52, 0.0):
            items.append((p, 1.1, None))
        items.append((star8(x, y, 30, math.pi / 8)[0], 0.9, None))
    for (x, y) in [(120, 0), (0, 120), (240, 120), (120, 240)]:
        items.append(([(x - 34, y), (x, y - 34), (x + 34, y), (x, y + 34), (x - 34, y)], 1.0, None))
    m = strokes(W, H, items)
    art = FO(blank(W, H), m, "#a9aeb6", seed=nx(), emboss=0.2, sparkle=0.2)
    preview(art, "as-lattice", bg=DOVE)
    save_full(art, f"{OUT}/lattice.webp", size=(160, 160), quality=82)


def leaf(art, W, H, x, y, L, a, nx, rng, col=SAGE, col2=SAGE_D):
    p = petal_pts(x, y, L, L * 0.3, a, n=14, cup=rng.uniform(-0.15, 0.15))
    m = shape_mask(W, H, p)
    art = G(art, m, col, col2, seed=nx(), density=0.6, edge=0.55, bloom=0.4, rough=2.5, gran=0.35)
    vein = strokes(W, H, [([(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0.05, 0.85, 8)], 1.4, (0.1, 0.5))]) * m
    art = over(art, FO(blank(W, H), vein, "#c8ccd2", seed=nx(), emboss=0.3, sparkle=0.6))
    return art, m


def sprig():
    """Diagonal olive-like sprig: a curved silver stem with paired grey-green leaves and two small silver berries."""
    W, H = 520, 760
    rng = random.Random(5); nx = Seq(500)
    art = blank(W, H)
    stem = curve([(60, 740), (150, 560), (250, 380), (380, 200), (470, 40)], 60)
    for i in range(6, len(stem) - 2, 5):
        x, y = stem[i]
        x2, y2 = stem[i + 1]
        a = math.atan2(y2 - y, x2 - x)
        t = i / len(stem)
        L = 120 * (1 - t * 0.55)
        for d in (-1, 1):
            art, _ = leaf(art, W, H, x, y, L * rng.uniform(0.85, 1.05), a + d * rng.uniform(0.6, 0.9), nx, rng,
                          SAGE if d > 0 else SAGE_L, SAGE_D)
        clear()
    art, _ = leaf(art, W, H, stem[-1][0], stem[-1][1], 70, -0.9, nx, rng)
    sm = strokes(W, H, [(stem, 4.5, (0.0, 0.6))])
    art = over(art, FO(blank(W, H), sm, SILVER, seed=nx(), emboss=0.5, sparkle=0.4))
    ber = circles(W, H, [(stem[20][0] + 26, stem[20][1] + 10, 9), (stem[34][0] - 22, stem[34][1] - 6, 7)])
    art = over(art, FO(blank(W, H), ber, "#c2c6cc", seed=nx(), emboss=0.9, sparkle=0.5))
    preview(art, "as-sprig", bg=DOVE)
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=82)


def divider():
    W, H = 520, 80
    nx = Seq(700)
    cx, cy = W / 2, H / 2
    items = [([(20, cy), (cx - 46, cy)], 1.4, (0.6, 0.0)), ([(cx + 46, cy), (W - 20, cy)], 1.4, (0.0, 0.6))]
    for p in star8(cx, cy, 26, math.pi / 8):
        items.append((p, 1.8, None))
    items.append((arc_pts(cx, cy, 9, 0, math.tau, 30), 1.4, None))
    for d in (-1, 1):
        x = cx + d * 70
        items.append(([(x - 8, cy), (x, cy - 8), (x + 8, cy), (x, cy + 8), (x - 8, cy)], 1.3, None))
    art, m = silver_lines(W, H, items, nx, "#9aa0a8")
    preview(art, "as-divider", bg=DOVE)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


def star():
    W = H = 140
    nx = Seq(900)
    items = []
    for p in star8(70, 70, 56, math.pi / 8):
        items.append((p, 3.0, None))
    items.append((arc_pts(70, 70, 22, 0, math.tau, 40), 2.4, None))
    art, m = silver_lines(W, H, items, nx, "#9aa0a8")
    fill = shapes(W, H, [star8(70, 70, 54, math.pi / 8)[0], star8(70, 70, 54, math.pi / 8)[1]], smooth=False)
    wash = pigment(fill, "#dfe1e5", "#d3d6db", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=1.5)
    art = over(wash, art)
    preview(art, "as-star", bg=DOVE)
    save(art, f"{OUT}/star.webp", max_w=72, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
