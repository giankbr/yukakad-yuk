"""Ukiran Botani — copperplate-engraved botanical plates: an open peony with a bud, lanceolate leaves and a fern frond,
cut in parallel lines, cross-hatching and stipple, printed in warm black ink on aged paper.
Run: python3 -I ukiran-botani.py [part ...]  parts: plate fern sprig specimen paper
Assets -> public/themes/art/ukiran-botani/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q2_lib import *

OUT = outdir("ukiran-botani")
PARTS = sys.argv[1:] or ["plate", "fern", "sprig", "specimen", "paper"]
INK = "#1e1a16"
PAPER = "#efe5cf"


def round_petal(cx, cy, L, Wd, ang, rng, n=26, ruffle=0.06, skew=0.0):
    """Broad petal: narrow claw at the base, widest at ~70%, rounded wavy tip."""
    right, left = [], []
    ph = rng.random() * 6
    n = 40
    for i in range(n + 1):
        t = i / n
        hw = Wd * (t ** 0.6) * max(0.0, 1 - t ** 3.2) ** 0.55
        wob = 1 + ruffle * (math.sin(t * 23 + ph) * 0.6 + math.sin(t * 41 + ph * 2) * 0.4) * t ** 2
        right.append((t * L, hw * wob * (1 + skew)))
        left.append((t * L, -hw * (2 - wob) * (1 - skew)))
    pts = right + left[::-1]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def leaf_pts(x, y, L, Wd, ang, bend=0.15, n=24):
    """Lanceolate leaf along a slightly curved midrib; returns outline, midrib."""
    mid = []
    for i in range(n + 1):
        t = i / n
        a = ang + bend * t
        if i == 0:
            px, py = x, y
        else:
            px += math.cos(a) * L / n; py += math.sin(a) * L / n
        mid.append((px, py, a))
    r, l = [], []
    for i, (px, py, a) in enumerate(mid):
        t = i / n
        hw = Wd * math.sin(math.pi * t ** 0.8) ** 0.9
        nx_, ny_ = -math.sin(a), math.cos(a)
        r.append((px + nx_ * hw, py + ny_ * hw)); l.append((px - nx_ * hw, py - ny_ * hw))
    return r + l[::-1], [(p[0], p[1]) for p in mid]


def eng_leaf(ink, W, H, x, y, L, Wd, ang, bend, seed, light=(-0.6, -0.8)):
    outline, mid = leaf_pts(x, y, L, Wd, ang, bend)
    # two halves: shaded half darker, lines run as oblique veins
    n = len(mid)
    half_r = outline[: n] + mid[::-1]
    half_l = mid + outline[n:]
    mr = shape_mask(W, H, half_r, smooth=False)
    ml = shape_mask(W, H, half_l, smooth=False)
    ink = engrave_shape(ink, ml, ang + 0.75 + bend * 0.5, spacing=3.3, base=0.12, edge=0.35, grad=0.25, seed=seed, cross=None, bend=0.4, outline=1.6, light=light)
    ink = engrave_shape(ink, mr, ang - 0.75 + bend * 0.5, spacing=3.3, base=0.42, edge=0.45, grad=0.25, seed=seed + 1, cross=0.68, bend=0.4, outline=1.6, knock=False, light=light)
    ink = engrave_line(ink, [mid], width=2.0, taper=(0.02, 0.5))
    return ink


def eng_fern(ink, W, H, x, y, L, ang, curl, seed, scale=1.0, flip=1):
    rach = frond_pts(x, y, L, ang, curl * flip)
    rng = random.Random(seed)
    n = len(rach)
    pinnae = []
    for i in range(2, n - 1, 1):
        px, py = rach[i]
        qx, qy = rach[i + 1]
        a = math.atan2(qy - py, qx - px)
        t = i / (n - 1)
        pl = (1 - t) ** 0.7 * 118 * scale * (0.6 + 0.4 * math.sin(math.pi * min(1, t * 1.6)))
        if pl < 5:
            continue
        for side in (-1, 1):
            pa = a + side * (1.05 - 0.25 * t)
            pinnae.append((px, py, pl * (0.92 + 0.16 * rng.random()), pa, side))
    # pinnae as lobed slivers, engraved with short cross lines
    for k, (px, py, pl, pa, side) in enumerate(pinnae):
        pts = petal_pts(px, py, pl, pl * 0.19, pa, n=16, cup=0.12 * side)
        m = shape_mask(W, H, pts)
        dark = 0.2 + 0.35 * (side > 0)
        ink = engrave_shape(ink, m, pa + 1.3, spacing=2.9, base=dark, edge=0.3, grad=0.2, seed=seed + k, cross=None, outline=1.25, knock=True)
        # lobes: small notches as ticks along the pinna
        ticks = []
        L_ = int(pl // 7)
        for j in range(1, L_):
            t = j / L_
            cx_ = px + math.cos(pa) * pl * t; cy_ = py + math.sin(pa) * pl * t
            w_ = pl * 0.19 * math.sin(math.pi * t) ** 0.8
            for sd in (-1, 1):
                ex = cx_ - math.sin(pa) * w_ * sd; ey = cy_ + math.cos(pa) * w_ * sd
                ticks.append([(ex, ey), (ex * 0.55 + cx_ * 0.45, ey * 0.55 + cy_ * 0.45)])
        ink = engrave_line(ink, ticks, width=0.9, taper=(0.0, 0.6))
    ink = engrave_line(ink, [rach], width=2.6 * scale, taper=(0.02, 0.6))
    return ink


def peony(ink, W, H, cx, cy, R, seed, tilt=0.0):
    rng = random.Random(seed)
    lit = lambda X, Y: 0.32 * ((X - cx) / R * 0.55 + (Y - cy) / R * 0.7) - 0.05
    deep = lambda X, Y: lit(X, Y) + 0.28 * np.clip(1 - np.hypot(X - cx, (Y - cy - R * 0.05) * 1.6) / (R * 0.55), 0, 1)
    # back petals (fan behind, opening up and outward)
    k = 0
    for a in [-2.6, -2.15, -1.75, -1.35, -0.95, -0.5]:
        a2 = a + tilt + rng.uniform(-0.06, 0.06)
        pts = round_petal(cx, cy + R * 0.1, R * rng.uniform(0.92, 1.05), R * 0.42, a2, rng, ruffle=0.3)
        ink = engrave_shape(ink, shape_mask(W, H, pts), a2, spacing=3.2, base=0.38, edge=0.42, grad=0.7, seed=seed + k, cross=0.6, bend=0.35, outline=1.9, tone_add=lit)
        k += 1
    # side petals, lower and spreading
    for a in [math.pi - 0.15, 0.15, math.pi + 0.35, -0.35]:
        a2 = a + tilt
        pts = round_petal(cx, cy + R * 0.18, R * 0.9, R * 0.4, a2, rng, ruffle=0.32)
        ink = engrave_shape(ink, shape_mask(W, H, pts), a2, spacing=3.2, base=0.3, edge=0.45, grad=0.7, seed=seed + 40 + k, cross=0.62, bend=0.3, outline=1.9, tone_add=lit)
        k += 1
    # inner cupped petals (rising)
    for a in [-2.2, -1.6, -1.0]:
        a2 = a + tilt + rng.uniform(-0.05, 0.05)
        pts = round_petal(cx, cy + R * 0.2, R * 0.62, R * 0.32, a2, rng, ruffle=0.32)
        ink = engrave_shape(ink, shape_mask(W, H, pts), a2, spacing=3.0, base=0.2, edge=0.5, grad=0.65, seed=seed + 80 + k, cross=0.66, bend=0.5, outline=1.7, tone_add=deep)
        k += 1
    # stamens: stippled dome with little anther dots
    dome = shape_mask(W, H, ellipse_pts(cx, cy + R * 0.02, R * 0.26, R * 0.16, 18))
    ink = engrave_shape(ink, dome, 0.3, spacing=2.6, base=0.25, edge=0.4, grad=0.7, seed=seed + 120, cross=None, outline=1.0, stipple=6.0)
    anth = []
    for i in range(26):
        t = rng.uniform(-1, 1); r_ = rng.uniform(0.1, 1)
        anth.append((cx + t * R * 0.28, cy - R * 0.02 - r_ * R * 0.12 * (1 - abs(t) * 0.5), rng.uniform(1.4, 2.3)))
    ink = np.maximum(ink, circles(W, H, anth))
    # front petals: wide, curling down over the cup
    for a, ln in [(1.95, 0.7), (1.2, 0.72), (1.57, 0.78)]:
        a2 = a + tilt
        pts = round_petal(cx, cy + R * 0.08, R * ln, R * 0.42, a2, rng, ruffle=0.3)
        ink = engrave_shape(ink, shape_mask(W, H, pts), a2 + 1.4, spacing=3.1, base=0.16, edge=0.5, grad=0.7, seed=seed + 160 + k, cross=0.64, bend=0.6, outline=1.9, tone_add=lit)
        k += 1
    return ink


def bud(ink, W, H, x, y, s, ang, seed):
    rng = random.Random(seed)
    pts = round_petal(x, y, s, s * 0.45, ang, rng, ruffle=0.03)
    ink = engrave_shape(ink, shape_mask(W, H, pts), ang, spacing=3.0, base=0.3, edge=0.5, grad=0.7, seed=seed, cross=0.6, bend=0.6, outline=1.8)
    for d in (-0.5, 0.45):
        sp = petal_pts(x, y, s * 0.7, s * 0.16, ang + d, n=14)
        ink = engrave_shape(ink, shape_mask(W, H, sp), ang + d + 1.2, spacing=2.8, base=0.35, edge=0.4, grad=0.3, seed=seed + 7, cross=0.7, outline=1.5)
    return ink


def plate():
    W, H = 640, 920
    ink = np.zeros((H, W), np.float32)
    # two fern fronds behind: one sweeping up-left, one leaning right
    ink = eng_fern(ink, W, H, 300, 905, 620, -2.0, 0.26, 11, scale=0.95, flip=1)
    ink = eng_fern(ink, W, H, 340, 905, 520, -1.15, -0.2, 13, scale=0.8, flip=1)
    clear()
    # main stem
    stem = [(318 + 14 * math.sin(t * 2.4) - t * 10, 900 - t * 590) for t in np.linspace(0, 1, 40)]
    side = [(stem[18][0] + 0, stem[18][1])] + [(stem[18][0] + t * 170 - 40 * t * t, stem[18][1] - t * 190) for t in np.linspace(0.05, 1, 20)]
    ink = engrave_line(ink, [stem], width=4.2, taper=(0.0, 0.1))
    ink = engrave_line(ink, [side], width=2.8, taper=(0.0, 0.3))
    ink = engrave_line(ink, [[(x + 3.2, y) for x, y in stem[2:-4]]], width=1.0, taper=(0.1, 0.1))
    ink = eng_leaf(ink, W, H, 322, 760, 210, 40, -0.35, -0.25, 31)
    ink = eng_leaf(ink, W, H, 316, 690, 190, 36, math.pi + 0.55, 0.22, 33)
    ink = eng_leaf(ink, W, H, 314, 560, 150, 30, -0.7, -0.2, 35)
    ink = eng_leaf(ink, W, H, 420, 470, 120, 24, -0.6, -0.2, 37)
    clear()
    ink = bud(ink, W, H, side[-1][0] - 2, side[-1][1] + 6, 92, -1.2, 51)
    ink = peony(ink, W, H, 330, 268, 175, 61, tilt=0.05)
    clear()
    arr = ink_to_rgba(ink, INK, seed=3)
    preview(arr, "ub-plate", tone=PAPER)
    save(arr, f"{OUT}/plate.webp", quality=80)


def fern():
    W, H = 300, 720
    ink = np.zeros((H, W), np.float32)
    ink = eng_fern(ink, W, H, 150, 712, 700, -1.62, 0.12, 71, scale=0.82)
    arr = ink_to_rgba(ink, INK, seed=4)
    preview(arr, "ub-fern", tone=PAPER)
    save(arr, f"{OUT}/fern.webp", quality=80)


def sprig():
    """Horizontal divider: a little leafy sprig either side of a tiny flower."""
    W, H = 540, 100
    ink = np.zeros((H, W), np.float32)
    for flip in (1, -1):
        cx = W / 2
        st = [(cx + flip * (16 + t * 220), 50 + 5 * math.sin(t * 3.0)) for t in np.linspace(0, 1, 30)]
        ink = engrave_line(ink, [st], width=1.8, taper=(0.0, 0.5))
        for j, t in enumerate([0.18, 0.36, 0.54, 0.72, 0.88]):
            px, py = st[int(t * 29)]
            up = -1 if j % 2 == 0 else 1
            a = -0.62 * up if flip > 0 else math.pi + 0.62 * up
            ink = eng_leaf(ink, W, H, px, py, 44 - 18 * t, 10 - 3 * t, a, 0.12 * up * flip, 90 + j + (10 if flip < 0 else 0))
    rng = random.Random(5)
    for k, a in enumerate(np.linspace(0, math.tau, 6)[:-1]):
        pts = round_petal(W / 2, 50, 17, 9, a - 1.57, rng, ruffle=0.05)
        ink = engrave_shape(ink, shape_mask(W, H, pts), a, spacing=2.6, base=0.18, edge=0.5, grad=0.3, seed=120 + k, cross=None, outline=1.3)
    ink = np.maximum(ink, circles(W, H, [(W / 2, 50, 4.0)]))
    arr = ink_to_rgba(ink, INK, seed=6)
    preview(arr, "ub-sprig", tone=PAPER)
    save(arr, f"{OUT}/sprig.webp", quality=82)


def specimen():
    """Small single bloom on a short stem (timeline node, sent-art, closing emblem)."""
    W, H = 300, 380
    ink = np.zeros((H, W), np.float32)
    stem = [(150 + 8 * math.sin(t * 2), 372 - t * 210) for t in np.linspace(0, 1, 20)]
    ink = engrave_line(ink, [stem], width=3.0, taper=(0.0, 0.1))
    ink = eng_leaf(ink, W, H, 152, 300, 92, 18, -0.5, -0.2, 140)
    ink = eng_leaf(ink, W, H, 150, 262, 80, 16, math.pi + 0.6, 0.2, 142)
    ink = peony(ink, W, H, 150, 120, 92, 150)
    arr = ink_to_rgba(ink, INK, seed=8)
    preview(arr, "ub-specimen", tone=PAPER)
    save(arr, f"{OUT}/specimen.webp", quality=82)


def paper_tile():
    """Aged laid paper: warm cream, faint chain lines, foxing spots; seamless 512."""
    S = 512
    rng = np.random.default_rng(9)
    base = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(PAPER), np.float32)
    big = wrap_noise(S, S, 11, 40) - 0.5
    fine = wrap_noise(S, S, 12, 0.7) - 0.5
    fib = gaussian_filter(rng.random((S, S)).astype(np.float32), (0.5, 7), mode="wrap"); fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    xx = np.arange(S, dtype=np.float32)[None, :]
    chain = np.clip(1 - np.abs(((xx / 64) % 1) - 0.5) * 2 / 0.03, 0, 1) * 0.012
    laid = (np.sin(np.arange(S, dtype=np.float32)[:, None] * math.tau / 4) * 0.004)
    v = 1 + big * 0.06 + fine * 0.035 + fib * 0.006 - chain + laid
    # foxing: a few warm brown spots
    fox = np.zeros((S, S), np.float32)
    for _ in range(14):
        x, y = rng.integers(0, S, 2); r = rng.uniform(1.5, 6)
        yy, xx2 = np.mgrid[0:S, 0:S]
        dx = np.minimum(np.abs(xx2 - x), S - np.abs(xx2 - x)); dy = np.minimum(np.abs(yy - y), S - np.abs(yy - y))
        fox = np.maximum(fox, np.exp(-(dx ** 2 + dy ** 2) / (2 * r * r)) * rng.uniform(0.25, 0.6))
    rgb = base * v[..., None]
    rgb = rgb * (1 - fox[..., None] * np.array([0.12, 0.2, 0.32], np.float32))
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(f"{OUT}/paper.webp", "WEBP", quality=84, method=6)
    print("paper.webp", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")


for p in PARTS:
    {"plate": plate, "fern": fern, "sprig": sprig, "specimen": specimen, "paper": paper_tile}[p]()
    clear()
