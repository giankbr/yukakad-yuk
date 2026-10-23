"""Mint Syari — fresh mint sprigs in loose watercolour (serrated, veined leaves in opposite pairs on square stems, a
few tiny lilac flower whorls), pale mint washes for an arch window and monogram discs. Flora only.
Run: python3 -I mint-syari.py [part ...]  parts: sprig sprig2 leaf wash disc
Assets -> public/themes/art/mint-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n1_lib import *

OUT = outdir("mint-syari")
PARTS = sys.argv[1:] or ["sprig", "sprig2", "leaf", "wash", "disc", "cluster"]
M_L, M, M_D, M_DD = "#9ee0bd", "#45b383", "#23875f", "#145a40"
LILAC = "#b9a6d6"


def serrate(pts, teeth=14, amt=2.6):
    """Saw-tooth the outline of a closed leaf polygon (teeth only along the blade, not the tip/stalk)."""
    n = len(pts)
    out = []
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    dense = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        for t in np.linspace(0, 1, 6, endpoint=False):
            dense.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    m = len(dense)
    for i, (x, y) in enumerate(dense):
        dx, dy = x - cx, y - cy; d = math.hypot(dx, dy) or 1
        phase = (i * teeth * 2 / m) % 1.0
        k = amt * (phase if phase < 0.8 else (1 - phase) * 4) * (0.6 + 0.4 * math.sin(i / m * math.pi))
        out.append((x + dx / d * k, y + dy / d * k))
    return out


def mint_leaf(art, W, H, x, y, L, ang, rng, nx, tone=0.5):
    """One mint leaf: ovate, serrated, rugose (glazed between lighter veins)."""
    ca0, sa0 = math.cos(ang), math.sin(ang)
    bend = rng.uniform(-0.12, 0.12)
    left, right = [], []
    for t in np.linspace(0, 1, 26):
        wdt = L * 0.3 * (math.sin(math.pi * t ** 0.62) ** 0.9) * (1.05 - 0.25 * t)
        u = L * t; off = bend * L * t * t
        bx, by = x + ca0 * u - sa0 * off, y + sa0 * u + ca0 * off
        left.append((bx - sa0 * wdt, by + ca0 * wdt)); right.append((bx + sa0 * wdt, by - ca0 * wdt))
    pts = left + right[::-1]
    pts = serrate(deform(pts, rng, 1, 0.02), teeth=int(8 + L / 14), amt=max(1.0, L * 0.03))
    m = shape_mask(W, H, pts, smooth=False)
    ca = mix(M_L, M, tone); cb = mix(M, M_D, tone)
    art = G(art, m, ca, cb, seed=nx(), density=0.62, edge=0.55, bloom=0.45, rough=2.2, holes=0.03, feather=1.0)
    # darker glaze on the shaded half
    half = shape_mask(W, H, petal_pts(x, y, L * 0.94, L * 0.2, ang + 0.1, n=12)) * m
    art = G(art, half, cb, seed=nx(), density=0.3, edge=0.3, bloom=0.2, rough=2)
    # veins: midrib + lateral pairs, a little darker; lighter halo beside them reads as rugose texture
    ca_, sa_ = math.cos(ang), math.sin(ang)
    vein = [([(x + ca_ * L * 0.04, y + sa_ * L * 0.04), (x + ca_ * L * 0.9, y + sa_ * L * 0.9)], max(1.0, L * 0.018), (0.05, 0.5))]
    for t in (0.2, 0.36, 0.52, 0.68):
        px, py = x + ca_ * L * t, y + sa_ * L * t
        for side in (-1, 1):
            va = ang + side * 0.85
            vl = L * 0.3 * (1 - t * 0.6)
            vein.append(([(px, py), (px + math.cos(va) * vl * 0.5 + ca_ * vl * 0.2, py + math.sin(va) * vl * 0.5 + sa_ * vl * 0.2),
                          (px + math.cos(va) * vl + ca_ * vl * 0.5, py + math.sin(va) * vl + sa_ * vl * 0.5)], max(0.8, L * 0.011), (0.05, 0.6)))
    vm = strokes(W, H, vein) * m
    art = OV(art, np.clip(dilate(vm, 1.2) - vm, 0, 1) * m, lambda q: flat(q, "#e9f7ee", 0.35))
    art = G(art, vm, M_DD, seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    return art, m


def whorl(art, W, H, x, y, r, rng, nx):
    """Tiny lilac mint-flower whorl (a fuzzy cluster of dots)."""
    items = [(x + rng.gauss(0, r * 0.5), y + rng.gauss(0, r * 0.35), rng.uniform(1.4, 2.6)) for _ in range(int(r * 2.2))]
    m = circles(W, H, items)
    art = G(art, gaussian_filter(m, 0.6), LILAC, "#9c86c4", seed=nx(), density=0.7, edge=0.4, bloom=0.2, rough=1.0, feather=0.6)
    return art


def sprig_paint(W, H, base, top, nx, rng, scale=1.0, pairs=6, flowers=True, lean=0.0):
    art = blank(W, H)
    (x0, y0), (x1, y1) = base, top
    stem = curve([(x0, y0), (x0 + (x1 - x0) * 0.3 + lean * 30, y0 + (y1 - y0) * 0.35), (x0 + (x1 - x0) * 0.75 - lean * 20, y0 + (y1 - y0) * 0.72), (x1, y1)], 60)
    art = G(art, strokes(W, H, [(stem, 4.2 * scale, (0.02, 0.4))]), "#6f9a5c", "#4a7a4a", seed=nx(), density=0.75, edge=0.4, bloom=0, rough=1, feather=0.6)
    nodes = [stem[int(len(stem) * t)] for t in np.linspace(0.22, 0.93, pairs)]
    for k, (px, py) in enumerate(nodes):
        i = stem.index((px, py))
        a = math.atan2(stem[min(i + 1, len(stem) - 1)][1] - stem[max(i - 1, 0)][1], stem[min(i + 1, len(stem) - 1)][0] - stem[max(i - 1, 0)][0])
        L = (90 - k * 8.5) * scale * rng.uniform(0.9, 1.08)
        for side in (-1, 1):
            la = a + side * rng.uniform(0.85, 1.15) + 0.35 * side
            art, _ = mint_leaf(art, W, H, px, py, L, la, rng, nx, tone=0.25 + 0.5 * rng.random())
        if flowers and k >= pairs - 2:
            art = whorl(art, W, H, px, py, 9 * scale, rng, nx)
    # top bud: two tiny young leaves
    tx, ty = stem[-1]
    a = math.atan2(stem[-1][1] - stem[-4][1], stem[-1][0] - stem[-4][0])
    for side in (-1, 1):
        art, _ = mint_leaf(art, W, H, tx, ty, 22 * scale, a + side * 0.5, rng, nx, tone=0.1)
    if flowers:
        art = whorl(art, W, H, tx + math.cos(a) * 8, ty + math.sin(a) * 8, 10 * scale, rng, nx)
    return art


def sprig():
    """Tall sprig rising from the bottom, for the cover arch and closing."""
    W, H = 380, 720
    rng = random.Random(7); nx = Seq(100)
    art = sprig_paint(W, H, (W * 0.42, H - 6), (W * 0.56, 40), nx, rng, scale=1.25, pairs=7, flowers=True, lean=0.5)
    preview(art, "ms-sprig", tone="#ffffff")
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=82)


def sprig2():
    """Horizontal sprig (divider / heading ornament)."""
    W, H = 520, 200
    rng = random.Random(11); nx = Seq(300)
    art = sprig_paint(W, H, (20, H * 0.62), (W - 30, H * 0.42), nx, rng, scale=0.8, pairs=5, flowers=False, lean=-0.3)
    preview(art, "ms-sprig2", tone="#ffffff")
    save(art, f"{OUT}/sprig2.webp", max_w=300, quality=82)


def leaf():
    W, H = 180, 180
    rng = random.Random(4); nx = Seq(500)
    art, _ = mint_leaf(blank(W, H), W, H, 30, 150, 140, -0.78, rng, nx, tone=0.45)
    art = G(art, strokes(W, H, [([(14, 164), (28, 150)], 3, (0.0, 0.3))]), "#6f9a5c", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.6)
    preview(art, "ms-leaf", tone="#ffffff")
    save(art, f"{OUT}/leaf.webp", max_w=110, quality=84)


def wash():
    """Pale mint watercolour wash in an arch shape (round top), wet edge and blooms, for the cover window."""
    W, H = 560, 760
    rng = random.Random(3); nx = Seq(700)
    cx, r = W / 2, W / 2 - 30
    pts = arc_pts(cx, 30 + r, r, math.pi, math.tau, 40) + [(cx + r, H - 30), (cx - r, H - 30)]
    m = shape_mask(W, H, deform(pts, rng, 2, 0.02))
    art = G(blank(W, H), m, "#d6f0e3", "#bfe6d2", seed=nx(), density=0.7, edge=0.55, bloom=0.25, rough=10, feather=2.2)
    art = G(art, m * np.clip(np.arange(H)[:, None] / H, 0, 1) ** 1.6, "#a6dcc0", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=8)
    preview(art, "ms-wash", tone="#ffffff")
    save(art, f"{OUT}/wash.webp", max_w=360, quality=70)


def disc():
    """Soft round mint wash for monograms."""
    W = H = 340
    rng = random.Random(5); nx = Seq(900)
    m = shape_mask(W, H, deform(ellipse_pts(W / 2, H / 2, 150, 148, 18), rng, 3, 0.05))
    art = G(blank(W, H), m, "#cfeedd", "#a6dcc0", seed=nx(), density=0.7, edge=0.6, bloom=0.25, rough=9, feather=2)
    preview(art, "ms-disc", tone="#ffffff")
    save(art, f"{OUT}/disc.webp", max_w=260, quality=80)


def cluster():
    """Three sprigs fanning out of one point, bottom-anchored, for the cover and closing."""
    W, H = 640, 560
    rng = random.Random(21); nx = Seq(1100)
    art = blank(W, H)
    for (bx, top, sc, pr, fl, ln) in [(0.47, (W * 0.12, 150), 0.85, 5, False, -2.2), (0.53, (W * 0.86, 110), 0.95, 5, True, 2.0), (0.5, (W * 0.44, 12), 1.05, 6, True, 1.2)]:
        lay = sprig_paint(W, H, (W * bx, H - 4), top, nx, rng, scale=sc, pairs=pr, flowers=fl, lean=ln)
        art = glaze(art, lay) if art[..., 3].max() > 0 else lay
        clear()
    preview(art, "ms-cluster", tone="#ffffff")
    save(art, f"{OUT}/cluster.webp", max_w=480, quality=80)


for p in PARTS:
    globals()[p]()
    clear()
