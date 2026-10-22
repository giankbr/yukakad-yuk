"""Musim Gugur — autumn maple & oak leaves in transparent watercolour: gold centres turning rust at the tips, pale
back-lit veins with fine darker ribs, a few tar spots; a maple twig for the corner, a drift of fallen leaves, acorns.
Run: python3 -I musim-gugur.py [part ...]
parts: leaves twig pile divider paper. Assets -> public/themes/art/musim-gugur/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d4_lib import *

OUT = outdir("musim-gugur")
PARTS = sys.argv[1:] or ["leaves", "twig", "pile", "divider", "paper"]
PAPER = "#f6eddc"
GOLD, AMBER, RUST, RED, BROWN, OLIVE = "#e2b33c", "#d9832b", "#b4462a", "#9a2f22", "#7a4a2a", "#8c8a3e"
PALS = {
    "red": (AMBER, RUST, RED),
    "amber": (GOLD, AMBER, RUST),
    "gold": ("#ecc94e", GOLD, AMBER),
    "brown": ("#c99a4a", "#a8682e", BROWN),
    "olive": ("#c9b44a", OLIVE, AMBER),
}


def paint_leaf(art, W, H, poly, vein_items, tips, pal, nx, rng):
    light, mid, deep = pal
    m = shapes(W, H, [poly])
    art = OV(art, displace(m, nx(), 1.5, 16), lambda mm: layer(np.clip(gaussian_filter(mm, 0.7) * 1.05, 0, 1), mix(light, "#fff6dc", 0.55), 0.82))
    art = G(art, m, light, mid, seed=nx(), density=0.78, edge=0.7, bloom=0.5, gran=0.25, rough=2.0, feather=0.8)
    # colour turns from the tips/edges inward
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    tip = np.zeros((H, W), np.float32)
    for (tx, ty, r) in tips:
        tip = np.maximum(tip, np.clip(1 - np.hypot(xx - tx, yy - ty) / r, 0, 1))
    edge = np.clip(m - gaussian_filter(m, 7), 0, 1) * 2.2
    turn = np.clip(tip * 1.3 + edge * 0.5, 0, 1) * m
    art = G(art, turn, mid, deep, seed=nx(), density=0.82, edge=0.4, bloom=0.5, gran=0.3, rough=3, feather=2.2)
    # back-lit veins: pale knock-out lines with fine darker ribs inside
    vm = strokes(W, H, vein_items) * m
    art = OV(art, gaussian_filter(vm, 1.2), lambda mm: layer(mm, "#fff1c8", 0.5))
    fine = strokes(W, H, [(p, max(0.6, w * 0.35), t) for p, w, t in vein_items]) * m
    art = G(art, fine, deep, mix(deep, "#4a2416", 0.4), seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    # a few tar spots
    spots = []
    for _ in range(0):
        px, py = poly[rng.randrange(len(poly))]
        cx_ = sum(p[0] for p in poly) / len(poly); cy_ = sum(p[1] for p in poly) / len(poly)
        t = rng.uniform(0.3, 0.6)
        spots.append((cx_ + (px - cx_) * t, cy_ + (py - cy_) * t, rng.uniform(2, 5)))
    if spots:
        art = G(art, circles(W, H, spots) * m, "#5a2a18", seed=nx(), density=0.6, edge=0.6, bloom=0.3, rough=1.2, feather=0.7, pad=8)
    return art


def maple(art, W, H, x, y, s, ang, pal, nx, rng, stem=True):
    """Stem base at (x, y); leaf grows along ang (radians, 0 = right)."""
    a = ang + math.pi / 2  # maple_poly measures from 'up'
    poly = maple_poly(x, y, s, a, rng)
    vs = veins(x, y, s, a, "maple")
    tips = [(px, py, s * 0.5) for (px, py) in [poly[i] for i in range(len(poly)) if i % 12 == 7]]
    if stem:
        sx, sy = x - math.cos(ang) * s * 0.42, y - math.sin(ang) * s * 0.42
        art = G(art, strokes(W, H, [([(x, y), ((x + sx) / 2 + 3, (y + sy) / 2), (sx, sy)], max(1.6, s * 0.035), (0.0, 0.3))]), BROWN, seed=nx(), density=0.8, edge=0.3, rough=0.8, feather=0.5)
    return paint_leaf(art, W, H, poly, vs, tips, pal, nx, rng)


def oak(art, W, H, x, y, s, ang, pal, nx, rng, stem=True):
    poly = oak_poly(x, y, s, ang, rng)
    vs = veins(x, y, s, ang, "oak")
    tips = [(x + math.cos(ang) * s, y + math.sin(ang) * s, s * 0.6)]
    if stem:
        sx, sy = x - math.cos(ang) * s * 0.22, y - math.sin(ang) * s * 0.22
        art = G(art, strokes(W, H, [([(x, y), (sx, sy)], max(1.6, s * 0.03), (0.0, 0.3))]), BROWN, seed=nx(), density=0.8, edge=0.3, rough=0.8, feather=0.5)
    return paint_leaf(art, W, H, poly, vs, tips, pal, nx, rng)


def acorn(art, W, H, x, y, s, ang, nx, rng):
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    nut = shapes(W, H, [[T(s * 0.25 + math.cos(t) * s * 0.55, math.sin(t) * s * 0.36) for t in np.linspace(0, math.tau, 18, endpoint=False)]])
    art = G(art, nut, "#c98a3a", "#a5652a", seed=nx(), density=0.85, edge=0.7, bloom=0.3, rough=1.2, feather=0.7)
    cap = shapes(W, H, [[T(-s * 0.05 + math.cos(t) * s * 0.3, math.sin(t) * s * 0.42) for t in np.linspace(0, math.tau, 18, endpoint=False)]])
    art = G(art, cap, "#7a5232", "#5a3a22", seed=nx(), density=0.9, edge=0.5, bloom=0.2, gran=0.6, rough=1.5, feather=0.6)
    return G(art, strokes(W, H, [([T(-s * 0.32, 0), T(-s * 0.5, -s * 0.06)], s * 0.08, None)]), "#5a3a22", seed=nx(), density=0.9, rough=0.5, feather=0.4)


if "leaves" in PARTS:
    specs = [("maple-red", "maple", "red", 1), ("maple-amber", "maple", "amber", 2), ("maple-gold", "maple", "gold", 3), ("oak-brown", "oak", "brown", 4), ("oak-olive", "oak", "olive", 5)]
    for name, kind, pal, seed in specs:
        W, H = 300, 320
        rng = random.Random(seed * 13); nx = Seq(70000 + seed * 900)
        art = blank(W, H)
        if kind == "maple":
            art = maple(art, W, H, 150, 230, 125, -math.pi / 2 + rng.uniform(-.15, .15), PALS[pal], nx, rng)
        else:
            art = oak(art, W, H, 150, 300, 260, -math.pi / 2 + rng.uniform(-.12, .12), PALS[pal], nx, rng)
        preview(art, f"mg-{name}", tone=PAPER)
        save(art, f"{OUT}/{name}.webp", max_w=110, quality=82)
        clear()

if "twig" in PARTS:
    W, H = 700, 640
    rng = random.Random(31); nx = Seq(31000)
    art = blank(W, H)
    main = curve([(700, 30), (560, 90), (420, 150), (300, 240), (200, 300), (110, 330)], 60)
    sub1 = curve([(470, 128), (430, 240), (400, 330)], 24)
    sub2 = curve([(320, 226), (260, 140), (230, 80)], 24)
    twig = strokes(W, H, [(main, 9, (0.0, 0.7)), (sub1, 5, (0.0, 0.6)), (sub2, 4.5, (0.0, 0.6))])
    art = G(art, twig, "#7a4a2a", "#5a3420", seed=nx(), density=0.88, edge=0.5, bloom=0.2, gran=0.4, rough=1.5, feather=0.7)
    for (x, y, s, a, pal) in [(400, 330, 130, 1.6, "red"), (230, 80, 110, -2.0, "amber"), (110, 330, 120, 2.6, "gold"), (560, 92, 112, 1.2, "amber"), (300, 242, 100, 1.9, "red")]:
        art = maple(art, W, H, x, y, s, a, PALS[pal], nx, rng, stem=False)
    art = oak(art, W, H, 640, 52, 170, 1.9, PALS["brown"], nx, rng, stem=False)
    art = acorn(art, W, H, 500, 190, 40, 1.4, nx, rng)
    art = acorn(art, W, H, 530, 186, 34, 1.0, nx, rng)
    preview(art, "mg-twig", tone=PAPER)
    save(art, f"{OUT}/twig.webp", max_w=340, quality=80)
    clear()

if "pile" in PARTS:
    W, H = 1000, 300
    rng = random.Random(41); nx = Seq(41000)
    art = blank(W, H)
    pals = list(PALS)
    items = []
    for k in range(22):
        x = rng.uniform(20, W - 20); y = rng.uniform(150, 290) if k > 4 else rng.uniform(190, 290)
        items.append((y, x))
    for y, x in sorted(items):
        a = rng.uniform(-math.pi, math.pi)
        if rng.random() < 0.65:
            art = maple(art, W, H, x, y, rng.uniform(70, 105), a, PALS[rng.choice(pals)], nx, rng)
        else:
            art = oak(art, W, H, x, y, rng.uniform(120, 170), a, PALS[rng.choice(pals)], nx, rng)
    art = acorn(art, W, H, 330, 270, 36, 0.3, nx, rng)
    art = acorn(art, W, H, 720, 262, 32, -0.4, nx, rng)
    preview(art, "mg-pile", tone=PAPER)
    save(art, f"{OUT}/pile.webp", max_w=560, quality=78)
    clear()

if "divider" in PARTS:
    W, H = 600, 150
    rng = random.Random(51); nx = Seq(51000)
    art = blank(W, H)
    stem = curve([(80, 100), (220, 80), (380, 82), (520, 70)], 30)
    art = G(art, strokes(W, H, [(stem, 4, (0.1, 0.4))]), "#7a4a2a", seed=nx(), density=0.85, edge=0.4, rough=1, feather=0.6)
    art = maple(art, W, H, 230, 80, 64, -2.0, PALS["red"], nx, rng, stem=False)
    art = oak(art, W, H, 360, 82, 96, -1.0, PALS["amber"], nx, rng, stem=False)
    art = acorn(art, W, H, 470, 88, 26, 1.2, nx, rng)
    preview(art, "mg-divider", tone=PAPER)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=82)
    clear()

if "paper" in PARTS:
    n = 360
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb(PAPER), np.float32)
    base *= (1 + (wrap_noise(n, n, 61, 26) - 0.5)[..., None] * 0.05 + (wrap_noise(n, n, 62, 0.8) - 0.5)[..., None] * 0.05)
    fib = gaussian_filter(np.random.default_rng(63).random((n, n)).astype(np.float32), (0.5, 5), mode="wrap")
    base *= (1 + (norm(fib) - 0.5)[..., None] * 0.04)
    save_rgb(np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1), f"{OUT}/paper.webp", quality=70)
    clear()
