"""Biru Syari — dusty-blue watercolour on white: seamless soft-stripe paper, climbing sprays of small blue five-petal
flowers with grey-green leaves, a horizontal spray divider and an eight-point geometric rosette (khatam) in blue wash.
Run: python3 -I biru-syari.py [part ...]  parts: stripes climb spray rosette
Assets -> public/themes/art/biru-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m6_lib import *

OUT = outdir("biru-syari")
PARTS = sys.argv[1:] or ["stripes", "climb", "spray", "rosette"]

BLUE_L, BLUE, BLUE_D, NAVY = "#a9c0d6", "#7896b6", "#4f6f93", "#33496a"
LEAF, LEAF_D = "#9aaba4", "#6d827d"
CREAM = "#f3eedf"


def flower(art, W, H, x, y, r, rng, nx, col=BLUE, col2=BLUE_L, rot=None):
    rot = rng.uniform(0, math.tau) if rot is None else rot
    pet = []
    for k in range(5):
        a = rot + k / 5 * math.tau + rng.uniform(-.12, .12)
        d = r * 0.55
        pet.append(deform(ellipse_pts(x + math.cos(a) * d, y + math.sin(a) * d, r * 0.52, r * 0.46, 10, a), rng, 1, 0.08))
    m = shapes(W, H, pet)
    art = G(art, m, col2, col, seed=nx(), density=0.62, edge=0.7, bloom=0.3, rough=1.6, feather=0.9, gran=0.3)
    c = circles(W, H, [(x, y, r * 0.24)])
    art = G(art, c, "#efe4b8", seed=nx(), density=0.8, edge=0.5, bloom=0, rough=0.8, feather=0.6)
    dot = circles(W, H, [(x, y, r * 0.09)])
    art = G(art, dot, BLUE_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.4, feather=0.5)
    return art


def bud(items, x, y, r):
    items.append((x, y, r))


def cluster(art, W, H, x, y, s, rng, nx, n=5):
    """scorpioid forget-me-not head: buds curling at the tip, open flowers below"""
    ang = rng.uniform(-2.4, -0.7)
    pts = []
    for k in range(n + 3):
        t = k / (n + 2)
        a = ang + t * 2.2
        rr = s * (1.9 - t * 1.0)
        pts.append((x + math.cos(a) * rr * t * 1.5, y + math.sin(a) * rr * t * 1.5))
    stem = strokes(W, H, [(curve([(x, y)] + pts[::2], 16), max(1.0, s * 0.07), (0, 0.4))])
    art = G(art, stem, LEAF_D, seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.8, feather=0.6)
    bd = []
    for k, (px, py) in enumerate(pts):
        if k < n:
            art = flower(art, W, H, px, py, s * rng.uniform(0.42, 0.52) * (1 - k * 0.07), rng, nx,
                         col=BLUE if rng.random() < 0.6 else BLUE_D, col2=BLUE_L)
        else:
            bd.append((px, py, s * 0.11))
    if bd:
        art = G(art, circles(W, H, bd), "#c9a7c4", BLUE_L, seed=nx(), density=0.7, edge=0.6, bloom=0, rough=0.8, feather=0.7)
    return art


def leafm(W, H, x, y, L, a, rng):
    return shape_mask(W, H, deform(petal_pts(x, y, L, L * 0.26, a, n=14, cup=0.1), rng, 1, 0.05))


def leafy(art, W, H, x, y, L, a, rng, nx):
    m = leafm(W, H, x, y, L, a, rng)
    art = G(art, m, LEAF, LEAF_D, seed=nx(), density=0.55, edge=0.75, bloom=0.35, rough=2.0, feather=1.0, gran=0.3)
    vein = strokes(W, H, [([(x, y), (x + math.cos(a) * L * 0.8, y + math.sin(a) * L * 0.8)], 1.0, (0, .6))])
    art = G(art, vein * 0.7, LEAF_D, seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    return art


def branch(art, W, H, pts, rng, nx, leaves=8, heads=4, s=34, width=2.6):
    c = curve(pts, 60)
    art = G(art, strokes(W, H, [(c, width, (0.02, 0.5))]), LEAF_D, "#7c8f96", seed=nx(), density=0.75, edge=0.35, bloom=0, rough=1, feather=0.7)
    for k in range(leaves):
        i = int(4 + (len(c) - 8) * (k + 0.5) / leaves)
        x, y = c[i]
        dx, dy = c[i + 1][0] - c[i - 1][0], c[i + 1][1] - c[i - 1][1]
        ta = math.atan2(dy, dx)
        side = 1 if k % 2 else -1
        art = leafy(art, W, H, x, y, s * rng.uniform(1.0, 1.5) * (1 - 0.4 * k / leaves), ta + side * rng.uniform(0.6, 1.0), rng, nx)
    for k in range(heads):
        i = int((len(c) - 3) * (0.3 + 0.7 * (k + 0.5) / heads))
        x, y = c[min(i, len(c) - 1)]
        side = 1 if k % 2 else -1
        ox, oy = x + side * s * 0.9, y - s * 0.4
        twig = strokes(W, H, [(curve([(x, y), ((x + ox) / 2, y - s * 0.2), (ox, oy)], 10), 1.4, (0, 0.5))])
        art = G(art, twig, LEAF_D, seed=nx(), density=0.65, edge=0.3, bloom=0, rough=0.6, feather=0.6)
        art = cluster(art, W, H, ox, oy, s * rng.uniform(0.9, 1.15), rng, nx, n=rng.choice([4, 5, 6]))
    x, y = c[-1]
    art = cluster(art, W, H, x, y, s * 1.05, rng, nx, n=5)
    return art


if "stripes" in PARTS:
    W, H = 256, 512
    nx = Seq(100)
    art = solid(W, H, "#fbfaf7")
    pap = np.asarray(paper(W, H, "#fbfaf7", 5), np.float32) / 255
    art[..., :3] = pap
    # wide pale band + two hairlines per 128 px column, centred so tile edges fall in the white gap
    for cx in (64, 192):
        band = shapes(W, H, [rect(cx - 22, -20, cx + 22, H + 20)], smooth=False)
        art = G(art, band, "#cfdbe7", "#bfcfe0", seed=nx(), density=0.42, edge=0.45, bloom=0.25, rough=2.2, feather=1.4, gran=0.35, mottle=0.6)
        for dx in (-31, 31):
            ln = strokes(W, H, [([(cx + dx, -10), (cx + dx + 0.6, H + 10)], 1.6, None)])
            art = G(art, ln, BLUE, seed=nx(), density=0.38, edge=0.2, bloom=0, rough=0.9, feather=0.5, gran=0.3)
    # vertical seam: crossfade with a half-height rolled copy near the top/bottom edge
    sh = np.roll(art, H // 2, 0)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    k = np.clip(np.minimum(yy, H - 1 - yy) / 60, 0, 1)
    art = art * k + sh * (1 - k)
    save_rgb(art, f"{OUT}/stripes.webp", quality=74)
    Image.fromarray((np.clip(np.tile(art[..., :3], (2, 3, 1)), 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/bs-stripes.png")

if "climb" in PARTS:
    W, H = 380, 900
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    art = branch(art, W, H, [(70, 890), (110, 700), (90, 520), (150, 330), (200, 130)], rng, nx, leaves=12, heads=6, s=42, width=3.2)
    clear()
    art = branch(art, W, H, [(40, 880), (30, 760), (60, 640), (40, 560)], rng, nx, leaves=4, heads=1, s=34, width=2.0)
    art = branch(art, W, H, [(110, 700), (190, 640), (260, 520), (300, 440)], rng, nx, leaves=5, heads=2, s=36, width=2.0)
    clear()
    pv(art, "bs-climb")
    save(art, f"{OUT}/climb.webp", max_w=380, quality=80)

if "spray" in PARTS:
    W, H = 560, 170
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    art = branch(art, W, H, [(260, 80), (190, 70), (110, 84), (30, 66)], rng, nx, leaves=5, heads=1, s=28, width=1.8)
    art = branch(art, W, H, [(262, 82), (330, 72), (410, 86), (490, 70)], rng, nx, leaves=5, heads=1, s=28, width=1.8)
    art = cluster(art, W, H, 262, 76, 32, rng, nx, n=5)
    pv(art, "bs-spray")
    save(art, f"{OUT}/spray.webp", max_w=360, quality=82)

if "rosette" in PARTS:
    W = H = 300
    rng = random.Random(3); nx = Seq(300)
    art = blank(W, H)
    cx = cy = 150

    def star(r, rot=0.0):
        pts = []
        for k in range(16):
            a = rot + k / 16 * math.tau
            rr = r if k % 2 == 0 else r * 0.72
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        return pts
    # two overlapping squares = eight-point star; wash, then white interlace lines and a blue outline
    sq1 = [(cx + math.cos(a) * 128, cy + math.sin(a) * 128) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
    sq2 = [(cx + math.cos(a) * 128, cy + math.sin(a) * 128) for a in [k * math.pi / 2 for k in range(4)]]
    body = shapes(W, H, [sq1, sq2], smooth=False)
    art = G(art, body, BLUE_L, BLUE, seed=nx(), density=0.55, edge=0.75, bloom=0.35, rough=1.6, feather=1.0, gran=0.35)
    inner = shapes(W, H, [star(86, math.pi / 8)], smooth=False)
    art = G(art, inner, BLUE, BLUE_D, seed=nx(), density=0.6, edge=0.7, bloom=0.25, rough=1.2, feather=0.9)
    core = circles(W, H, [(cx, cy, 34)])
    art = G(art, core, "#e9eef3", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.8)
    petals = shapes(W, H, petal_ring(cx, cy, 30, 8, 0.36, 0, 0, None))
    art = G(art, petals, BLUE_L, BLUE, seed=nx(), density=0.6, edge=0.6, bloom=0.2, rough=0.6, feather=0.6)
    lines = []
    for poly in (sq1, sq2, star(86, math.pi / 8)):
        lines.append((poly + [poly[0]], 3.2, None))
    lm = strokes(W, H, lines)
    def white(m):
        rgb = np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fbfaf7"), np.float32)
        return np.concatenate([rgb, np.clip(m * 0.92, 0, 1)[..., None]], -1)
    art = OV(art, lm, white)
    edge = strokes(W, H, [([(x * 1.0, y * 1.0) for x, y in sq1 + [sq1[0]]], 1.6, None), ([(x, y) for x, y in sq2 + [sq2[0]]], 1.6, None)])
    art = G(art, edge, NAVY, seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1.2, feather=0.6)
    pv(art, "bs-rosette")
    save(art, f"{OUT}/rosette.webp", max_w=240, quality=82)

kb(OUT)
