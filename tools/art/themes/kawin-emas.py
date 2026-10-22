"""Kawin Emas — a golden wedding anniversary (50 years) syukuran: an old family photo album in brown leather with
gold-stamped tooling, watercolour chrysanthemums (krisan) in honey-gold, cream and rust with lobed leaves, a pressed
gold-foil wreath for the '50', and a stamped gold divider.
Run: python3 -I kawin-emas.py [part ...]   parts: bouquet krisan wreath leather divider
Assets -> public/themes/art/kawin-emas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g1_lib import *  # noqa

OUT = outdir("kawin-emas")
PARTS = sys.argv[1:] or ["bouquet", "krisan", "wreath", "leather", "divider"]
GOLDS = [("#f7d77a", "#e0a83a", "#a86a1a", "#7a4a12"), ("#fbf1d6", "#ecd6a2", "#c49a52", "#a0762e"), ("#f3b36a", "#d87a34", "#9a4a1e", "#6a2e12")]


def lobed_leaf(W, H, x, y, L, ang, rng):
    """Chrysanthemum leaf: deeply lobed outline (5 lobes) along a midrib."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (x + u * L * ca - v * L * sa, y + u * L * sa + v * L * ca)
    pts = [P(0, 0)]
    lobes = [(0.18, 0.16), (0.42, 0.26), (0.68, 0.22), (0.9, 0.12)]
    for i, (u, w) in enumerate(lobes):
        pts += [P(u - 0.08, w * 0.45), P(u, w + rng.uniform(-0.02, 0.02)), P(u + 0.07, w * 0.5)]
    pts.append(P(1.0, 0))
    for i, (u, w) in reversed(list(enumerate(lobes))):
        pts += [P(u + 0.07, -w * 0.5), P(u, -w + rng.uniform(-0.02, 0.02)), P(u - 0.08, -w * 0.45)]
    return pts, (P(0, 0), P(1.0, 0))


def leaf_paint(art, W, H, x, y, L, ang, nx, rng, c=("#7d8a4a", "#5a6a3a")):
    pts, (a, b) = lobed_leaf(W, H, x, y, L, ang, rng)
    m = shape_mask(W, H, pts)
    art = knockout(art, m, amount=0.6, grow=1.0)
    art = G(art, m, c[0], c[1], seed=nx(), density=0.85, edge=0.65, bloom=0.4, rough=1.2, feather=0.7, gran=0.3)
    art = G(art, strokes(W, H, [([a, b], max(1, L * 0.02), (0.0, 0.7))]) * m, "#3e4a26", seed=nx(), density=0.45, edge=0.1, rough=0.5, feather=0.5)
    return art


def part_bouquet():
    W, H = 900, 760
    rng = random.Random(50); nx = Seq(500)
    art = blank(W, H)
    # stems from bottom-left gathering point
    gx, gy = 200, 760
    heads = [(420, 300, 150, 0), (650, 230, 112, 1), (250, 380, 120, 2), (560, 470, 98, 0), (760, 420, 72, 1), (360, 560, 70, 2)]
    st = [(curve([(gx + rng.uniform(-10, 10), gy), ((gx + x) / 2 + rng.uniform(-30, 30), (gy + y) / 2 + 40), (x, y)], 30), 4.5, (0.0, 0.3)) for x, y, r, k in heads]
    art = G(art, strokes(W, H, st), "#6f7a42", "#566236", seed=nx(), density=0.85, edge=0.4, rough=1, feather=0.6)
    for (pts, _, _) in st:
        for t, side in ((0.55, 1), (0.75, -1)):
            i = int(len(pts) * t)
            x, y = pts[i]
            dx, dy = pts[i + 1][0] - x, pts[i + 1][1] - y
            a = math.atan2(dy, dx) + side * 0.9
            art = leaf_paint(art, W, H, x, y, rng.uniform(100, 140), a, nx, rng)
        clear()
    for x, y, r, k in sorted(heads, key=lambda h: h[2]):
        l, m_, d, c = GOLDS[k]
        art = chrysanthemum(art, W, H, x, y, r, nx, rng, l, m_, d, centre=c, rot=rng.uniform(0, 3), tilt=rng.uniform(0.8, 0.95), layers=5)
        clear()
    preview(art, "ke-bouquet", tone="#f7eedb")
    save(art, f"{OUT}/bouquet.webp", max_w=520, quality=82)
    clear()


def part_krisan():
    W = H = 280
    rng = random.Random(7); nx = Seq(900)
    art = blank(W, H)
    art = leaf_paint(art, W, H, 150, 160, 110, 0.5, nx, rng)
    art = leaf_paint(art, W, H, 130, 150, 100, 2.6, nx, rng)
    l, m_, d, c = GOLDS[0]
    art = chrysanthemum(art, W, H, 140, 130, 100, nx, rng, l, m_, d, centre=c, rot=0.3, tilt=0.92)
    preview(art, "ke-krisan", tone="#f7eedb")
    save(art, f"{OUT}/krisan.webp", max_w=150, quality=84)
    clear()


def part_wreath():
    """Gold-foil wreath of slender leaves on two curving branches, open at the top, a small bow at the bottom."""
    W = H = 560
    rng = random.Random(3); nx = Seq(1200)
    cx, cy, R = W / 2, H / 2 + 10, 210
    items, leaves = [], []
    for side in (-1, 1):
        branch = [(cx + math.sin(t) * R * side, cy + math.cos(t) * R) for t in np.linspace(0.15, 2.55, 50)]
        items.append((branch, 5, (0.0, 0.6)))
        for i, t in enumerate(np.linspace(0.3, 2.5, 15)):
            bx, by = cx + math.sin(t) * R * side, cy + math.cos(t) * R
            tang = math.atan2(-math.sin(t), math.cos(t) * side)
            L = 46 - t * 7
            for d in (-1, 1):
                leaves.append(petal_pts(bx, by, L * rng.uniform(0.85, 1.1), L * 0.22, tang + d * 0.6, n=10))
        # tiny chrysanthemum rosettes on the branch
        for t in (0.9, 1.9):
            bx, by = cx + math.sin(t) * R * side, cy + math.cos(t) * R
            for k in range(14):
                a = k / 14 * math.tau
                leaves.append(petal_pts(bx, by, 16, 3.5, a, n=8))
    m = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    bow = shapes(W, H, [[(cx, cy + R + 4), (cx - 40, cy + R - 18), (cx - 46, cy + R + 16)], [(cx, cy + R + 4), (cx + 40, cy + R - 18), (cx + 46, cy + R + 16)],
                        [(cx - 4, cy + R + 4), (cx - 26, cy + R + 50), (cx - 14, cy + R + 52)], [(cx + 4, cy + R + 4), (cx + 26, cy + R + 50), (cx + 14, cy + R + 52)]], smooth=False)
    m = np.maximum(m, bow)
    art = FO(blank(W, H), m, "#c9a04a", seed=nx(), emboss=0.7, sparkle=0.3)
    wear = np.clip((fbm(W, H, nx(), 8, 2) - 0.8) * 4, 0, 1) * m
    art[..., 3] *= 1 - wear * 0.5
    preview(art, "ke-wreath", bg="#4a2a18")
    save(art, f"{OUT}/wreath.webp", max_w=320, quality=84)
    clear()


def part_leather():
    W = H = 320
    rng = np.random.default_rng(9)
    def nz(sig):
        n = gaussian_filter(rng.random((H, W)).astype(np.float32), sig, mode="wrap")
        return (n - n.mean()) / (n.std() + 1e-6)
    pebble = nz(1.6); cell = np.clip(nz(3.5), -1.5, 1.5); big = nz(W / 8); fine = nz(0.6)
    v = 1 + pebble * 0.05 + cell * 0.05 + big * 0.06 + fine * 0.03
    rgb = np.ones((H, W, 3), np.float32) * col_arr("#4b2a19") * v[..., None]
    rgb = rgb + np.clip(big, 0, None)[..., None] * 0.02 * (col_arr("#7a4a2a") - col_arr("#4b2a19"))
    prev_rgb(np.clip(rgb, 0, 1), "ke-leather")
    rgb_save(np.clip(rgb, 0, 1), f"{OUT}/leather.webp", quality=72)


def part_divider():
    W, H = 600, 70
    rng = random.Random(2); nx = Seq(1500)
    cx, cy = W / 2, H / 2
    items = [([(40, cy), (cx - 50, cy)], 2.2, (0.4, 0.0)), ([(cx + 50, cy), (W - 40, cy)], 2.2, (0.0, 0.4)),
             ([(90, cy + 7), (cx - 60, cy + 7)], 1.0, (0.4, 0.0)), ([(cx + 60, cy + 7), (W - 90, cy + 7)], 1.0, (0.0, 0.4))]
    pets = [petal_pts(cx, cy, 24, 4.2, k / 16 * math.tau, n=8) for k in range(16)]
    pets += [petal_pts(cx + d * 52, cy, 12, 3.6, (0 if d > 0 else math.pi) + e * 0.6, n=8) for d in (-1, 1) for e in (-1, 1)]
    m = np.maximum(strokes(W, H, items), shapes(W, H, pets))
    m = np.maximum(m, circles(W, H, [(cx + d * 84, cy, 3.2) for d in (-1, 1)] + [(cx + d * 100, cy, 2.2) for d in (-1, 1)]))
    art = FO(blank(W, H), m, "#c9a04a", seed=nx(), emboss=0.6, sparkle=0.2)
    preview(art, "ke-divider", tone="#f7eedb")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
