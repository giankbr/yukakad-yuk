"""Bunga Rampai — a brass bokor heaped with sliced pandan, rose petals, jasmine and cempaka, in transparent watercolour.
Assets: bokor (cover/hero), kelopak (single rose petal, falling), melati (single jasmine bloom, falling), cempaka (node),
untai (pandan + petal divider), tabur (scattered petals corner for sections).
Run: python3 -I bunga-rampai.py [part ...]
Assets -> public/themes/art/bunga-rampai/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s5_lib import *

OUT = outdir("bunga-rampai")
PARTS = sys.argv[1:] or ["bokor", "kelopak", "melati", "cempaka", "untai", "tabur"]
PAND, PAND_D, PAND_L = "#5f8a3a", "#3f6426", "#9cbf5e"
ROSE, ROSE_D, ROSE_L = "#d0606e", "#9e3445", "#efa2a8"
ROSE2 = "#b8404f"
BRASS, BRASS_D, BRASS_L = "#c99a48", "#8a5f22", "#f1d58e"
JAS, JAS_S = "#fffdf6", "#c9c6b0"
CEM, CEM_D = "#f4e2a8", "#d9b45e"


def rose_petal(art, W, H, x, y, s, ang, seed, col=ROSE, deep=ROSE_D):
    """Rounded fan-shaped rose petal: narrow base at (x, y), broad notched top along ang."""
    rng = random.Random(seed)
    wid = rng.uniform(0.36, 0.44)
    loc = [(0.0, 0.0)]
    for a in np.linspace(-2.25, 2.25, 18):
        r = 0.5 * (0.84 if abs(a) < 0.3 else 1.0)
        loc.append((s * 0.52 + math.cos(a) * s * r, math.sin(a) * s * wid * 1.05))
    c, sn = math.cos(ang), math.sin(ang)
    pts = [(x + px * c - py * sn, y + px * sn + py * c) for px, py in loc]
    m = shape_mask(W, H, pts)
    art = G(art, m, col, ROSE_L if col != ROSE_L else "#f6c6c6", seed=seed, density=0.8, edge=0.9, bloom=0.35, rough=0.9, feather=0.6, pad=10)
    hl = strokes(W, H, [([(x + c * s * 0.35, y + sn * s * 0.35), (x + c * s * 0.8 - sn * s * 0.08, y + sn * s * 0.8 + c * s * 0.08)], s * 0.16, (0.3, 0.4))]) * m
    art = OV(art, gaussian_filter(hl, 1.5), lambda q: flat(q, "#fbe1e0", 0.45), pad=6)
    base = circles(W, H, [(x + c * s * 0.18, y + sn * s * 0.18, s * 0.22)]) * m
    art = G(art, base, deep, seed=seed + 1, density=0.55, edge=0.1, bloom=0, rough=1.0, feather=2.0, pad=8)
    return art


def jasmine(art, W, H, x, y, r, seed, rot=None):
    rng = random.Random(seed)
    rot = rng.uniform(0, math.tau) if rot is None else rot
    n = rng.choice([5, 6])
    pet = [petal_pts(x + math.cos(rot + i * math.tau / n) * r * 0.08, y + math.sin(rot + i * math.tau / n) * r * 0.08, r, r * 0.34, rot + i * math.tau / n, n=14, cup=0.2) for i in range(n)]
    m = shapes(W, H, pet)
    shadow = np.roll(np.roll(m, 2, 0), 1, 1)
    art = G(art, shadow, "#8d8a6e", seed=seed + 3, density=0.45, edge=0.2, bloom=0, rough=0.8, feather=1.2, pad=8)
    art = OV(art, m, lambda q: pigment(q, JAS, "#f3f0de", seed=seed, density=0.97, edge=0.1, bloom=0.0, gran=0.1, rough=0.8, feather=0.5), pad=8)
    rim = np.clip(m - gaussian_filter(m, 1.6) * 1.1, 0, 1)
    vein = strokes(W, H, [([(x, y), (x + math.cos(rot + i * math.tau / n) * r * 0.7, y + math.sin(rot + i * math.tau / n) * r * 0.7)], 1.2, (0.1, 0.5)) for i in range(n)])
    art = G(art, np.clip(rim * 2.5 + vein * 0.6, 0, 1) * m, "#a8a58a", seed=seed + 1, density=0.55, edge=0.1, bloom=0, rough=0.3, feather=0.4, pad=8)
    art = G(art, circles(W, H, [(x, y, r * 0.17)]), "#d9cf7a", "#a9a650", seed=seed + 2, density=0.85, edge=0.3, rough=0.4, feather=0.5, pad=6)
    return art


def cempaka(art, W, H, x, y, L, ang, seed):
    """Cempaka: a loose cluster of long, narrow golden petals from one point (cempaka kuning)."""
    rng = random.Random(seed)
    for k, d in enumerate((-0.6, -0.28, 0.02, 0.32, 0.62)):
        a = ang + d + rng.uniform(-0.08, 0.08)
        LL = L * rng.uniform(0.8, 1.05)
        loc = [(0, 0)] + [(LL * t, LL * 0.11 * math.sin(math.pi * t ** 0.8) * sd + LL * 0.06 * t * t) for t in np.linspace(0.05, 1, 10) for sd in (1,)] + \
              [(LL * t, -LL * 0.11 * math.sin(math.pi * t ** 0.8) + LL * 0.06 * t * t) for t in np.linspace(1, 0.05, 10)]
        c, sn = math.cos(a), math.sin(a)
        pts = [(x + px * c - py * sn, y + px * sn + py * c) for px, py in loc]
        m = shape_mask(W, H, pts)
        art = G(art, m, "#f2c66e", "#f6dc9a", seed=seed + k, density=0.85, edge=0.75, bloom=0.2, rough=1.0, feather=0.6, pad=8)
        art = G(art, strokes(W, H, [([(x, y), (x + c * LL * 0.7, y + sn * LL * 0.7)], 1.4, (0.1, 0.5))]) * m, "#c98a2e", seed=seed + 9 + k, density=0.45, edge=0.1, bloom=0, rough=0.4, feather=0.5, pad=6)
    art = G(art, circles(W, H, [(x, y, L * 0.07)]), "#7d9440", seed=seed + 20, density=0.85, edge=0.3, rough=0.4, feather=0.5, pad=6)
    return art


def pandan_strips(W, H, items):
    """items: (x, y, L, ang, width) short sliced ribbons, slightly curved."""
    out = []
    for x, y, L, a, w_, bend in items:
        p = curve([(x, y), (x + math.cos(a) * L * 0.5 + math.cos(a + 1.57) * bend, y + math.sin(a) * L * 0.5 + math.sin(a + 1.57) * bend), (x + math.cos(a) * L, y + math.sin(a) * L)], 12)
        out.append((p, w_, (0.04, 0.04)))
    return strokes(W, H, out, cap=False)


def bokor():
    W, H = 700, 600
    clear()
    art = blank(W, H)
    rng = random.Random(7)
    cx, rim_y = 350, 300
    # shadow on the cloth
    art = G(art, ellipses(W, H, [(cx + 14, 548, 210, 26, 0)]), "#c9b4a2", seed=2, density=0.4, edge=0.2, bloom=0.2, rough=4, feather=6)
    # ── brass bokor ──
    bowl = curve([(cx - 252, rim_y), (cx - 236, rim_y + 62), (cx - 170, rim_y + 118), (cx - 70, rim_y + 140)], 20) + \
           curve([(cx + 70, rim_y + 140), (cx + 170, rim_y + 118), (cx + 236, rim_y + 62), (cx + 252, rim_y)], 20) + [(cx, rim_y + 30)]
    mb = shape_mask(W, H, bowl, smooth=False)
    foot = curve([(cx - 52, rim_y + 136), (cx - 40, rim_y + 160), (cx - 60, rim_y + 188), (cx - 130, rim_y + 214), (cx - 140, rim_y + 232)], 16) + \
           curve([(cx + 140, rim_y + 232), (cx + 130, rim_y + 214), (cx + 60, rim_y + 188), (cx + 40, rim_y + 160), (cx + 52, rim_y + 136)], 16)
    mf = shape_mask(W, H, foot, smooth=False)
    mfb = ellipses(W, H, [(cx, rim_y + 232, 140, 14, 0)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for mm, sd in ((np.maximum(mf, mfb), 11), (mb, 12)):
        art = G(art, mm, "#c38e3a", "#dcae58", seed=sd, density=0.95, edge=0.7, bloom=0.3, rough=1.6, feather=0.8)
    # form shading: dark core right of centre, reflected light at the far right edge
    core = np.exp(-((xx - (cx + 120)) / 95) ** 2) * 0.9 + np.clip((yy - rim_y - 60) / 90, 0, 1) * 0.5
    art = G(art, mb * np.clip(core, 0, 1), "#7a4e1a", "#94622a", seed=13, density=0.75, edge=0.15, bloom=0.3, rough=1, feather=3)
    fcore = np.exp(-((xx - (cx + 45)) / 45) ** 2) * 0.8 + np.clip((yy - rim_y - 205) / 30, 0, 1) * 0.4
    art = G(art, np.maximum(mf, mfb) * np.clip(fcore, 0, 1), "#7a4e1a", seed=14, density=0.7, edge=0.15, rough=1, feather=3)
    hl = strokes(W, H, [(curve([(cx - 200, rim_y + 40), (cx - 175, rim_y + 82), (cx - 120, rim_y + 116)], 12), 20, (0.3, 0.4)),
                        (curve([(cx - 100, rim_y + 48), (cx - 88, rim_y + 92), (cx - 62, rim_y + 128)], 12), 8, (0.3, 0.4)),
                        ([(cx - 30, rim_y + 166), (cx - 26, rim_y + 186)], 6, (0.3, 0.3)), ([(cx - 95, rim_y + 210), (cx - 40, rim_y + 197)], 6, (0.3, 0.3))])
    art = OV(art, hl * np.maximum(mb, np.maximum(mf, mfb)), lambda q: flat(gaussian_filter(q, 2.5), "#f6e2a6", 0.8))
    # engraved band: little repeating arches + buds round the belly
    band = []
    for t in np.linspace(-0.9, 0.9, 17):
        bx = cx + t * 222
        by = rim_y + 66 - (t * t) * 22
        band.append((arc_pts(bx, by, 11, math.pi, math.tau, 12), 2.2, (0.15, 0.15)))
        band.append(([(bx, by + 6), (bx, by + 14)], 1.8, (0.2, 0.2)))
    art = G(art, strokes(W, H, band) * mb, "#5e3a12", seed=15, density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    bl = [curve([(cx - 245, rim_y + 38), (cx, rim_y + 74), (cx + 245, rim_y + 38)], 40), curve([(cx - 230, rim_y + 92), (cx, rim_y + 124), (cx + 230, rim_y + 92)], 40)]
    art = G(art, strokes(W, H, [(p, 2.2, (0.05, 0.05)) for p in bl]) * mb, "#5e3a12", seed=16, density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    # scalloped rim lip
    scal = [(cx + math.cos(a) * 252, rim_y + math.sin(a) * 30 + 2, 9) for a in np.linspace(0.08, math.pi - 0.08, 26)]
    rim = np.maximum(ellipses(W, H, [(cx, rim_y, 256, 30, 0)]), circles(W, H, scal))
    art = G(art, rim, "#e4c070", "#c99a48", seed=17, density=0.95, edge=0.8, bloom=0.2, rough=1.2, feather=0.6)
    art = G(art, np.clip(rim - np.roll(rim, -4, 0), 0, 1), "#8a5f22", seed=18, density=0.6, edge=0.1, rough=0.5, feather=0.6)
    clear()
    # ── heap ──
    heap = [(cx - 238, rim_y + 6)] + curve([(cx - 238, rim_y + 6), (cx - 200, rim_y - 70), (cx - 90, rim_y - 120), (cx + 20, rim_y - 135), (cx + 130, rim_y - 108), (cx + 215, rim_y - 60), (cx + 240, rim_y + 6)], 40) + [(cx, rim_y + 26)]
    mh = shape_mask(W, H, heap)
    art = G(art, mh, PAND_D, PAND, seed=21, density=0.7, edge=0.15, bloom=0.3, rough=8, feather=3)
    # pandan slices in layers
    for layer, (ca, cb, wd, n) in enumerate([(PAND_D, PAND, 10, 120), (PAND, PAND_L, 9, 120), (PAND_L, "#b9d27c", 7, 70)]):
        items = []
        for _ in range(n):
            u = rng.uniform(-1, 1)
            top = rim_y - 150 * (1 - u * u) ** 0.8
            y = rng.uniform(top + 6, rim_y + 6)
            x = cx + u * 232
            items.append((x, y, rng.uniform(36, 66), rng.uniform(0, math.pi), wd * rng.uniform(0.8, 1.15), rng.uniform(-6, 6)))
        art = G(art, pandan_strips(W, H, items) * gaussian_filter(mh, 1.5), ca, cb, seed=30 + layer, density=0.9, edge=0.55, bloom=0.1, rough=0.8, feather=0.6)
    clear()
    # rose petals over the heap
    for i in range(34):
        u = rng.uniform(-0.95, 0.95)
        top = rim_y - 150 * (1 - u * u) ** 0.8
        x = cx + u * 225
        y = rng.uniform(top + 10, rim_y + 4)
        col = rng.choice([ROSE, ROSE, ROSE2, ROSE_L])
        art = rose_petal(art, W, H, x, y, rng.uniform(24, 32), rng.uniform(0, math.tau), 100 + i, col, ROSE_D)
    clear()
    for i, (u, v) in enumerate([(-0.6, 0.55), (-0.3, 0.85), (0.05, 0.92), (0.35, 0.8), (0.65, 0.5), (-0.1, 0.55), (0.2, 0.45), (-0.45, 0.3), (0.5, 0.25), (-0.78, 0.2), (0.82, 0.15), (0.0, 0.25)]):
        x = cx + u * 220
        top = rim_y - 150 * (1 - u * u) ** 0.8
        y = rim_y - (rim_y - top) * v + 8
        art = jasmine(art, W, H, x, y, rng.uniform(16, 20), 300 + i)
    for i, (u, v, a) in enumerate([(-0.4, 0.62, -2.3), (0.28, 0.66, -0.7), (0.62, 0.3, -0.3), (-0.72, 0.28, -2.7)]):
        x = cx + u * 220
        top = rim_y - 150 * (1 - u * u) ** 0.8
        y = rim_y - (rim_y - top) * v + 8
        art = cempaka(art, W, H, x, y, 46, a, 400 + i)
    clear()
    # spilled petals on the cloth
    for i, (x, y, s_, a) in enumerate([(80, 520, 26, 0.4), (130, 552, 22, 2.0), (590, 528, 25, -0.6), (630, 500, 20, 1.2), (560, 565, 21, 2.6)]):
        art = rose_petal(art, W, H, x, y, s_, a, 500 + i, ROSE if i % 2 else ROSE2)
    art = jasmine(art, W, H, 175, 520, 17, 520)
    art = jasmine(art, W, H, 520, 552, 15, 521)
    art = pandan_strips_paint(art, W, H, [(40, 566, 46, 0.3, 9, 3), (630, 552, 40, 2.6, 9, -3), (470, 578, 38, 0.1, 8, 3)], 530)
    preview(art, "bokor")
    save(art, f"{OUT}/bokor.webp", max_w=640, quality=82)


def pandan_strips_paint(art, W, H, items, seed):
    return G(art, pandan_strips(W, H, items), PAND, PAND_L, seed=seed, density=0.9, edge=0.5, bloom=0.1, rough=0.8, feather=0.6)


def kelopak():
    W, H = 90, 90
    art = rose_petal(blank(W, H), W, H, 14, 45, 64, 0.05, 61, ROSE, ROSE_D)
    preview(art, "kelopak")
    save(art, f"{OUT}/kelopak.webp", max_w=60)


def melati():
    W, H = 80, 80
    art = jasmine(blank(W, H), W, H, 40, 40, 30, 71, rot=0.3)
    preview(art, "melati", tone="#e9d9d0")
    save(art, f"{OUT}/melati.webp", max_w=56)


def cempaka_():
    W, H = 160, 160
    art = cempaka(blank(W, H), W, H, 40, 120, 110, -0.75, 81)
    art = G(art, strokes(W, H, [([(40, 120), (22, 146)], 4, (0.1, 0.3))]), PAND_D, seed=82, density=0.8, edge=0.3, rough=0.6, feather=0.6)
    preview(art, "cempaka")
    save(art, f"{OUT}/cempaka.webp", max_w=100)


globals()["cempaka_part"] = cempaka_


def untai():
    """Divider: a long pandan ribbon tied in the middle with a jasmine, petals along it."""
    W, H = 560, 90
    clear()
    art = blank(W, H)
    cy = H / 2
    rib = []
    for d in (-1, 1):
        rib.append((curve([(W / 2 + d * 16, cy), (W / 2 + d * 90, cy - 9), (W / 2 + d * 170, cy + 5), (W / 2 + d * 250, cy - 3)], 40), 7, (0.02, 0.5)))
    art = G(art, strokes(W, H, rib, cap=False), PAND, PAND_D, seed=3, density=0.88, edge=0.6, bloom=0.1, rough=0.8, feather=0.6)
    art = G(art, strokes(W, H, [(p, 2, (0.02, 0.5)) for p, _, _ in rib]), PAND_L, seed=4, density=0.6, edge=0.1, bloom=0, rough=0.4, feather=0.5)
    for i, (x, y, s_, a) in enumerate([(W / 2 - 70, cy + 6, 18, 0.6), (W / 2 + 95, cy - 8, 17, -2.4), (W / 2 - 160, cy - 6, 15, 2.2), (W / 2 + 175, cy + 6, 15, 1.0)]):
        art = rose_petal(art, W, H, x, y, s_, a, 20 + i, ROSE if i % 2 else ROSE2)
    art = jasmine(art, W, H, W / 2, cy, 18, 31)
    art = jasmine(art, W, H, W / 2 - 32, cy + 8, 11, 32)
    art = jasmine(art, W, H, W / 2 + 32, cy - 6, 11, 33)
    preview(art, "untai")
    save(art, f"{OUT}/untai.webp", max_w=480)


def tabur():
    """A loose scatter of petals, jasmine and pandan slices — corner ornament."""
    W, H = 360, 300
    clear()
    art = blank(W, H)
    rng = random.Random(9)
    items = [(rng.uniform(20, 330), rng.uniform(20, 280), rng.uniform(30, 50), rng.uniform(0, math.pi), 8, rng.uniform(-4, 4)) for _ in range(12)]
    items = [it for it in items if it[0] + it[1] < 420]
    art = pandan_strips_paint(art, W, H, items, 5)
    for i in range(16):
        x, y = rng.uniform(16, 320), rng.uniform(16, 270)
        if x + y > 400:
            continue
        art = rose_petal(art, W, H, x, y, rng.uniform(20, 28), rng.uniform(0, math.tau), 40 + i, rng.choice([ROSE, ROSE2, ROSE_L]))
    for i, (x, y) in enumerate([(60, 70), (150, 40), (40, 170), (210, 110), (110, 140)]):
        art = jasmine(art, W, H, x, y, rng.uniform(14, 18), 70 + i)
    art = cempaka(art, W, H, 30, 30, 46, 0.6, 90)
    preview(art, "tabur")
    save(art, f"{OUT}/tabur.webp", max_w=300)


for p in PARTS:
    (cempaka_ if p == "cempaka" else globals()[p])()
    clear()
kb(OUT)
