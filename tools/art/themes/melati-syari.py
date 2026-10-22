"""Melati Syari — white jasmine (melati, Jasminum sambac) in clean gouache on pale green: roncean strands of tightly
strung buds draped in swags, open double flowers, fresh glossy leaves in opposite pairs, a round bud wreath for the
monogram medallion. Opaque matte white with soft grey-green shadows, no outlines. No figures.
Run: python3 -I melati-syari.py [part ...]  parts: curtain medallion sprig divider bloom paper
Assets -> public/themes/art/melati-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c3_lib import *

OUT = outdir("melati-syari")
PARTS = sys.argv[1:] or ["curtain", "medallion", "sprig", "divider", "bloom", "paper"]
WHITE, WHITE_S = "#fffefa", "#eef0e6"
SHADOW = "#8ea58c"
CREAM = "#f3e7b8"
LEAF_L, LEAF, LEAF_D = "#8fbf6a", "#5f9a4e", "#3d6e3c"
STEM = "#6f8f4a"
PAPER = "#eef4e8"


def leaf(art, W, H, x, y, L, ang, nx, wd=0.36, tone=0.0):
    """Gouache jasmine leaf: oval-pointed, a lighter and a darker half split by a pale midrib."""
    a_ = mix(LEAF_L, LEAF, 0.3 + tone * 0.5); b_ = mix(LEAF, LEAF_D, 0.2 + tone * 0.5)
    full = shapes(W, H, [petal_pts(x, y, L, L * wd, ang, n=14)])
    art = G(art, np.roll(np.roll(full, 3, 0), 2, 1), SHADOW, seed=nx(), density=0.28, edge=0.1, bloom=0, rough=2, feather=2.5, pad=10)
    art = GP(art, full, a_, b_, seed=nx(), rough=1.2, streak=0.9, pad=10)
    # darker lower half
    ca, sa = math.cos(ang), math.sin(ang)
    half = [(x, y)] + [(x + ca * L * t - sa * L * wd * 0.5 * math.sin(math.pi * t) * 0.95, y + sa * L * t + ca * L * wd * 0.5 * math.sin(math.pi * t) * 0.95) for t in np.linspace(0, 1, 16)]
    hm = shapes(W, H, [half]) * full
    art = GP(art, hm, b_, mix(b_, LEAF_D, 0.4), seed=nx(), rough=0.6, streak=0.8, density=0.8, pad=10)
    vein = [(x + ca * L * t, y + sa * L * t) for t in np.linspace(0.05, 0.85, 10)]
    art = GP(art, strokes(W, H, [(vein, max(1.2, L * 0.03), (0.1, 0.6))]), "#d7ebbb", seed=nx(), rough=0.3, density=0.7, pad=6)
    return art


def flower(art, W, H, x, y, r, nx, rng, double=True, rot=None):
    """Open double jasmine: rounded oblong petals painted one by one (each with its own soft shadow and edge),
    an inner whorl, grey-green shading toward the centre and a cream eye."""
    rot = rng.uniform(0, math.tau) if rot is None else rot

    def whorl(art, n, rr, pw, a0, shade):
        for k in range(n):
            a = a0 + k * math.tau / n + rng.uniform(-.1, .1)
            px, py = x + math.cos(a) * rr * 0.56, y + math.sin(a) * rr * 0.56
            m = ellipses(W, H, [(px, py, rr * 0.5, rr * pw, math.degrees(a))])
            art = G(art, np.roll(np.roll(gaussian_filter(m, 2.2), 2, 0), 2, 1), shade, seed=nx(), density=0.42, edge=0.05, bloom=0, rough=1, feather=1.5, pad=8)
            art = GP(art, m, WHITE, WHITE_S, seed=nx(), rough=0.8, streak=0.15, pad=8)
            base = m * light_mask(H, W, x, y, rr * 0.8)
            art = G(art, base, SHADOW, seed=nx(), density=0.4, edge=0.05, bloom=0.1, rough=0.8, feather=1.2, pad=6)
            art = G(art, np.clip(m - gaussian_filter(m, 1.1) * 1.03, 0, 1) * 2.2, "#86a083", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.4, pad=6)
        return art
    art = whorl(art, 7, r, 0.27, rot, "#7f957d")
    if double:
        art = whorl(art, 5, r * 0.6, 0.3, rot + 0.45, "#8ea58c")
    art = G(art, circles(W, H, [(x, y, r * 0.13)]), CREAM, "#c9c27a", seed=nx(), density=0.8, edge=0.3, rough=0.5, pad=6)
    return art


def bud(art, W, H, x, y, L, ang, nx, calyx=True):
    """Closed jasmine bud: plump pointed ellipse, faint pink-cream tip shading, small green calyx at the base."""
    m = shapes(W, H, [petal_pts(x, y, L, L * 0.46, ang, n=12)])
    art = G(art, np.roll(np.roll(m, 2, 0), 2, 1), SHADOW, seed=nx(), density=0.3, edge=0.1, bloom=0, rough=1, feather=1.8, pad=8)
    art = GP(art, m, WHITE, WHITE_S, seed=nx(), rough=0.7, streak=0.4, pad=8)
    art = G(art, np.clip(m - gaussian_filter(m, 1.2) * 1.04, 0, 1) * 2.5, "#7f957d", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.5, pad=6)
    side = shapes(W, H, [petal_pts(x + math.cos(ang + 1.57) * L * 0.08, y + math.sin(ang + 1.57) * L * 0.08, L * 0.9, L * 0.2, ang, n=10)]) * m
    art = G(art, side, SHADOW, seed=nx(), density=0.4, edge=0.1, bloom=0, rough=0.6, feather=1.2, pad=6)
    if calyx:
        cm = shapes(W, H, [petal_pts(x, y, L * 0.3, L * 0.2, ang + d, n=8) for d in (-0.5, 0.5, 0.0)])
        art = GP(art, cm, LEAF, LEAF_D, seed=nx(), rough=0.5, pad=6)
    return art


def strand(art, W, H, pts, nx, rng, size=11.0, every_flower=0.0, shade="#6f8a6c"):
    """Roncean melati: long buds strung tightly through their bases, leaning alternately to each side of the
    thread like a braided rope; painted in five interleaved passes so neighbouring buds keep their own edges."""
    path = resample(pts, size * 0.36)
    buds_ = []
    for i, (x, y, a) in enumerate(path):
        side = (1, -1)[i % 2]
        ang = a + side * rng.uniform(0.75, 1.5)
        L = size * rng.uniform(1.0, 1.25)
        buds_.append((x - math.cos(ang) * L * 0.18, y - math.sin(ang) * L * 0.18, L, ang))
    for k in range(5):
        sel = [b for j, b in enumerate(buds_) if j % 5 == k]
        if not sel:
            continue
        m = shapes(W, H, [petal_pts(bx, by, L, L * 0.23, ang, n=22) for (bx, by, L, ang) in sel])
        art = G(art, np.roll(np.roll(gaussian_filter(m, 1.5), 3, 0), 2, 1), shade, seed=nx(), density=0.35, edge=0.05, bloom=0, rough=1, feather=2.0, pad=10)
        art = GP(art, m, ("#eef2e8", "#f6f8f1", "#fbfcf7", "#ffffff", "#fdfdf8")[k], WHITE_S, seed=nx(), rough=0.7, streak=0.4, pad=10)
        sh = np.clip(m - np.roll(np.roll(m, -2, 0), -1, 1), 0, 1)
        art = G(art, gaussian_filter(sh, 1.0), "#9db39a", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.5, feather=0.6, pad=6)
        rim = np.clip(m - gaussian_filter(m, 1.0) * 1.08, 0, 1) * 3
        art = G(art, rim, "#7c977a", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.3, feather=0.3, pad=6)
    if every_flower:
        for j in range(int(1 / every_flower) // 2, len(path), int(1 / every_flower)):
            x, y, a = path[j]
            art = flower(art, W, H, x, y, size * 1.25, nx, rng)
    return art


def tassel(art, W, H, x, y, L, nx, rng, size=10.0, shade="#6f8a6c"):
    """A short hanging strand ending in an open flower and two buds."""
    pts = curve([(x, y), (x + rng.uniform(-6, 6), y + L * 0.5), (x + rng.uniform(-4, 4), y + L)], 30)
    art = strand(art, W, H, pts, nx, rng, size=size, shade=shade)
    ex, ey = pts[-1]
    art = bud(art, W, H, ex - 4, ey + 4, size * 1.6, math.pi / 2 + 0.4, nx)
    art = bud(art, W, H, ex + 4, ey + 4, size * 1.5, math.pi / 2 - 0.35, nx)
    art = flower(art, W, H, ex, ey, size * 1.5, nx, rng)
    return art


def knot(art, W, H, x, y, nx, rng, s=1.0, flip=1):
    """Tie point: a pair of leaves, buds and one open flower."""
    for (ang, L, t) in [(-0.4, 54, 0.0), (math.pi + 0.4, 50, 0.3), (0.9, 44, 0.6), (math.pi - 0.9, 42, 0.2)]:
        art = leaf(art, W, H, x, y, L * s, ang if flip > 0 else math.pi - ang, nx, tone=t)
    for (dx, dy, ang) in [(-16, -8, -2.3), (14, -10, -0.9), (2, -18, -1.6)]:
        art = bud(art, W, H, x + dx * s, y + dy * s, 20 * s, ang, nx)
    art = flower(art, W, H, x, y + 2, 21 * s, nx, rng)
    return art


if "curtain" in PARTS:
    # cover canopy: a leafy vine across the top with roncean strands hanging at falling-then-rising lengths,
    # leaving a V of open space for the bismillah; painted for a deep leaf-green ground.
    W, H = 780, 600
    nx = Seq(400); rng = random.Random(12)
    art = blank(W, H)
    DSH = "#10271a"
    xs = [26, 106, 186, 262, 338, 442, 518, 594, 674, 754]
    lens = [540, 440, 330, 228, 150, 150, 228, 330, 440, 540]
    for x, L in zip(xs, lens):
        art = tassel(art, W, H, x + rng.uniform(-3, 3), 34, L * 0.92, nx, rng, size=12.5, shade=DSH)
        clear()
    vine = curve([(-20, 30), (200, 44), (390, 24), (590, 44), (800, 30)], 120)
    art = GP(art, strokes(W, H, [(vine, 4.5, (0.6, 0.8))]), STEM, LEAF_D, seed=nx(), rough=0.5)
    for i, (x, y, a) in enumerate(resample(vine, 46)):
        t = (i % 3) / 3
        art = leaf(art, W, H, x, y, 46 + rng.uniform(-6, 8), a - 0.8 + rng.uniform(-.2, .2), nx, tone=t)
        art = leaf(art, W, H, x, y, 40 + rng.uniform(-6, 8), a + 0.9 + math.pi * (i % 2) * 0.0 + rng.uniform(-.2, .2), nx, tone=1 - t)
    clear()
    for x in xs:
        art = flower(art, W, H, x, 34, 17, nx, rng)
    for (x, y, L, a) in [(150, 22, 18, -1.9), (300, 16, 18, -1.2), (480, 18, 18, -2.0), (630, 22, 18, -1.1)]:
        art = bud(art, W, H, x, y, L, a, nx)
    preview(art, "curtain", bg="#2c5a3c")
    save(art, f"{OUT}/curtain.webp", max_w=780, quality=80)
    clear()

if "medallion" in PARTS:
    W = H = 460
    nx = Seq(700); rng = random.Random(4)
    art = blank(W, H)
    cx = cy = 230; R = 176
    ringp = [(cx + math.cos(t) * R, cy + math.sin(t) * R) for t in np.linspace(-math.pi / 2, math.pi * 1.5, 120)]
    # leaves around the ring (pairs), pointing along the circle
    for k in range(14):
        t = -math.pi / 2 + k * math.tau / 14 + 0.12
        x, y = cx + math.cos(t) * R, cy + math.sin(t) * R
        tang = t + math.pi / 2
        art = leaf(art, W, H, x, y, 46, tang + 0.55, nx, tone=(k % 3) / 3)
        art = leaf(art, W, H, x, y, 40, tang - 0.65 + math.pi, nx, tone=((k + 1) % 3) / 3)
    clear()
    art = strand(art, W, H, ringp, nx, rng, size=15)
    clear()
    for k in range(4):
        t = -math.pi / 2 + k * math.tau / 4
        art = flower(art, W, H, cx + math.cos(t) * R, cy + math.sin(t) * R, 24, nx, rng)
    for k in range(4):
        t = -math.pi / 4 + k * math.tau / 4
        art = flower(art, W, H, cx + math.cos(t) * R, cy + math.sin(t) * R, 17, nx, rng, double=False)
    preview(art, "medallion", bg=PAPER)
    save(art, f"{OUT}/medallion.webp", max_w=400, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 520, 420
    nx = Seq(1100); rng = random.Random(7)
    art = blank(W, H)
    stem = curve([(30, 380), (160, 300), (300, 220), (470, 70)], 60)
    art = GP(art, strokes(W, H, [(stem, 5, (0.0, 0.5))]), STEM, LEAF_D, seed=nx(), rough=0.5)
    for i, (x, y, a) in enumerate(resample(stem, 62)[1:]):
        L = 70 - i * 6
        art = leaf(art, W, H, x, y, L, a - 0.9, nx, tone=(i % 3) / 3)
        art = leaf(art, W, H, x, y, L * 0.92, a + 0.95, nx, tone=((i + 1) % 3) / 3)
    clear()
    side = curve([(250, 255), (240, 170), (270, 120)], 20)
    art = GP(art, strokes(W, H, [(side, 3, (0.0, 0.5))]), STEM, seed=nx(), rough=0.4)
    art = flower(art, W, H, 270, 116, 34, nx, rng)
    art = flower(art, W, H, 470, 70, 30, nx, rng)
    art = flower(art, W, H, 150, 300, 26, nx, rng, double=False)
    for (x, y, L, a) in [(300, 140, 26, -0.4), (232, 128, 24, -2.4), (452, 40, 24, -1.2), (500, 86, 22, 0.2), (130, 270, 20, -2.0)]:
        art = bud(art, W, H, x, y, L, a, nx)
    preview(art, "sprig", bg=PAPER)
    save(art, f"{OUT}/sprig.webp", max_w=340, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 760, 120
    nx = Seq(1500); rng = random.Random(2)
    art = blank(W, H)
    for sgn in (-1, 1):
        pts = curve([(380, 60), (380 + sgn * 160, 72), (380 + sgn * 330, 58)], 40)
        art = strand(art, W, H, pts, nx, rng, size=14)
    art = leaf(art, W, H, 380, 60, 52, -0.3, nx); art = leaf(art, W, H, 380, 60, 52, math.pi + 0.3, nx, tone=0.5)
    art = flower(art, W, H, 380, 58, 26, nx, rng)
    for sgn in (-1, 1):
        art = bud(art, W, H, 380 + sgn * 336, 58, 16, math.pi / 2 - sgn * 1.2 + (0 if sgn > 0 else math.pi), nx)
    preview(art, "divider", bg=PAPER)
    save(art, f"{OUT}/divider.webp", max_w=330, quality=82)
    clear()

if "bloom" in PARTS:
    W = H = 200
    nx = Seq(1900); rng = random.Random(9)
    art = blank(W, H)
    art = leaf(art, W, H, 100, 104, 78, 0.5, nx, tone=0.2)
    art = leaf(art, W, H, 100, 104, 70, math.pi - 0.3, nx, tone=0.6)
    art = flower(art, W, H, 100, 96, 46, nx, rng, rot=0.3)
    preview(art, "bloom", bg=PAPER)
    save(art, f"{OUT}/bloom.webp", max_w=120, quality=84)
    clear()

if "paper" in PARTS:
    W = H = 320
    n1 = wrap_noise(W, H, 8, 14); n2 = wrap_noise(W, H, 9, 1.6)
    base = col_arr(PAPER)[None, None] * (0.975 + 0.03 * n1[..., None] + 0.03 * (n2[..., None] - 0.5))
    img = np.concatenate([np.clip(base, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/paper.webp", quality=84)
