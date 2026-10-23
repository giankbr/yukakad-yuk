"""Dahlia Syari — warm watercolour dahlias in terracotta, blush and cream with olive serrated leaves, dried grass and
wax-flower buds. Floral only (syar'i, no figures). Run: python3 -I dahlia-syari.py [part ...]
parts: bouquet spray bloom wreath divider    Assets -> public/themes/art/dahlia-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k2_lib import *

OUT = outdir("dahlia-syari")
PARTS = sys.argv[1:] or ["bouquet", "spray", "bloom", "wreath", "divider"]
TERRA = ("#e9a27f", "#c8643f", "#8e3a22", "#5e2416")
BLUSH = ("#f6d5c8", "#e8a99a", "#b8705f", "#7b3b30")
CREAM = ("#fbf1e1", "#efd8b9", "#c9a47a", "#8a6a44")
RUST = ("#f0b98e", "#d98457", "#a14e2c", "#6b2c18")


def D(art, W, H, cx, cy, R, pal, rng, nx, **k):
    return dahlia(art, W, H, cx, cy, R, rng, nx, pal[0], pal[1], pal[2], centre=pal[3], **k)


def grass(art, W, H, base, n, L, spread, rng, nx, col=("#c9a06a", "#9a7046")):
    it = []
    for _ in range(n):
        a = rng.uniform(*spread)
        ll = L * rng.uniform(0.6, 1.1)
        bx, by = base[0] + rng.uniform(-8, 8), base[1] + rng.uniform(-8, 8)
        mid = (bx + math.cos(a) * ll * 0.5 + rng.uniform(-10, 10), by + math.sin(a) * ll * 0.5)
        tip = (bx + math.cos(a) * ll, by + math.sin(a) * ll + ll * 0.08)
        it.append((curve([(bx, by), mid, tip], 16), rng.uniform(2.2, 3.0), (0.0, 0.7)))
        # seed head: tiny oat-like strokes near the tip
        for j in range(5):
            t = 0.72 + j * 0.05
            px_, py_ = bx + (tip[0] - bx) * t, by + (tip[1] - by) * t
            for sg in (-1, 1):
                it.append(([(px_, py_), (px_ + math.cos(a + sg * 0.6) * 9, py_ + math.sin(a + sg * 0.6) * 9)], 2.6, (0.1, 0.6)))
    return G(art, strokes(W, H, it), col[0], col[1], seed=nx(), density=0.75, edge=0.4, bloom=0.1, rough=0.8, feather=0.6)


def buds(art, W, H, pts, r, pal, rng, nx):
    m = circles(W, H, [(x, y, r * rng.uniform(0.8, 1.2)) for x, y in pts])
    art = G(art, m, pal[0], pal[1], seed=nx(), density=0.85, edge=0.7, bloom=0.2, rough=1)
    return G(art, circles(W, H, [(x + r * 0.3, y + r * 0.3, r * 0.5) for x, y in pts]), pal[2], seed=nx(), density=0.4, edge=0.2, bloom=0, rough=0.8)


def stems(art, W, H, items, rng, nx):
    return G(art, strokes(W, H, items), "#7d8a58", "#4e5c36", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=0.8, feather=0.6)


if "bouquet" in PARTS:
    # cover cascade from the top-right corner
    W, H = 820, 700
    nx = Seq(61100); rng = random.Random(61)
    art = blank(W, H)
    for x, y, L, a in [(470, 260, 190, 2.6), (520, 380, 190, 2.0), (700, 430, 200, 1.5), (380, 170, 170, 3.1), (650, 120, 170, -2.2), (600, 470, 170, 2.2), (760, 300, 150, 0.4), (300, 330, 160, 2.6)]:
        art = dahlia_leaf(art, W, H, x, y, L, a, rng, nx)
    clear()
    art = stems(art, W, H, [(curve([(380, 470), (330, 520), (300, 610)], 10), 5, (0.0, 0.6)), (curve([(250, 300), (200, 340), (160, 420)], 10), 4, (0.0, 0.6))], rng, nx)
    art = buds(art, W, H, [(300, 612), (160, 424), (230, 380)], 15, TERRA, rng, nx)
    art = D(art, W, H, 600, 250, 175, TERRA, rng, nx, tilt=0.86, rot=0.2)
    clear()
    art = D(art, W, H, 380, 400, 125, BLUSH, rng, nx, tilt=0.8, rot=-0.3)
    clear()
    art = D(art, W, H, 690, 470, 110, CREAM, rng, nx, tilt=0.78, rot=0.5)
    clear()
    art = D(art, W, H, 300, 210, 80, RUST, rng, nx, tilt=0.82, rot=-0.6, rings=5)
    clear()
    art = grass(art, W, H, (330, 450), 7, 240, (1.9, 2.6), rng, nx)
    art = grass(art, W, H, (520, 130), 6, 200, (-2.4, -1.6), rng, nx)
    # wax-flower dots
    wf = [(rng.uniform(220, 780), rng.uniform(80, 560)) for _ in range(60)]
    wf = [(x, y) for x, y in wf if (x - 600) ** 2 + (y - 250) ** 2 > 180 ** 2 and (x - 380) ** 2 + (y - 400) ** 2 > 130 ** 2 and (x - 690) ** 2 + (y - 470) ** 2 > 115 ** 2]
    art = G(art, circles(W, H, [(x, y, rng.uniform(3, 5)) for x, y in wf[:34]]), "#f7e3d6", "#e9b9a6", seed=nx(), density=0.8, edge=0.6, bloom=0.1, rough=0.6)
    show(art, "dh-bouquet")
    save(art, f"{OUT}/bouquet.webp", max_w=560, quality=82)
    clear()

if "spray" in PARTS:
    W, H = 640, 460
    nx = Seq(61200); rng = random.Random(62)
    art = blank(W, H)
    art = grass(art, W, H, (240, 300), 8, 260, (-0.4, 0.3), rng, nx)
    for x, y, L, a in [(300, 260, 160, -0.3), (220, 330, 150, 0.4), (360, 340, 140, 0.1), (160, 200, 130, -1.0)]:
        art = dahlia_leaf(art, W, H, x, y, L, a, rng, nx)
    art = stems(art, W, H, [(curve([(330, 230), (420, 190), (500, 170)], 10), 4, (0.0, 0.6))], rng, nx)
    art = buds(art, W, H, [(502, 168), (460, 210)], 13, BLUSH, rng, nx)
    clear()
    art = D(art, W, H, 210, 260, 120, TERRA, rng, nx, tilt=0.84, rot=0.3)
    clear()
    art = D(art, W, H, 350, 300, 82, CREAM, rng, nx, tilt=0.8, rot=-0.4, rings=5)
    show(art, "dh-spray")
    save(art, f"{OUT}/spray.webp", max_w=400, quality=82)
    clear()

if "bloom" in PARTS:
    W, H = 380, 380
    nx = Seq(61300); rng = random.Random(63)
    art = blank(W, H)
    for a in (0.6, 2.4, 4.2):
        art = dahlia_leaf(art, W, H, 190 + math.cos(a) * 60, 190 + math.sin(a) * 60, 120, a, rng, nx)
    art = D(art, W, H, 190, 190, 150, TERRA, rng, nx, tilt=1.0, rings=7)
    show(art, "dh-bloom")
    save(art, f"{OUT}/bloom.webp", max_w=220, quality=84)
    clear()

if "wreath" in PARTS:
    # open crescent wreath for the monogram medallions
    W, H = 520, 520
    nx = Seq(61400); rng = random.Random(64)
    art = blank(W, H)
    cx, cy, R = 260, 260, 210
    ring_pts = [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in [math.pi * (0.55 + 0.95 * i / 60) for i in range(61)]]
    art = G(art, strokes(W, H, [(ring_pts, 4, (0.05, 0.3))]), "#7d8a58", "#4e5c36", seed=nx(), density=0.8, edge=0.4, rough=0.8)
    for i, (x, y) in enumerate(ring_pts[4::7]):
        a = math.atan2(y - cy, x - cx) + math.pi / 2
        art = dahlia_leaf(art, W, H, x, y, 64, a + (0.5 if i % 2 else -0.5) - 0.3, rng, nx)
    clear()
    art = grass(art, W, H, ring_pts[50], 5, 130, (-1.2, -0.4), rng, nx)
    art = buds(art, W, H, [ring_pts[8], ring_pts[18], ring_pts[44]], 11, BLUSH, rng, nx)
    art = D(art, W, H, *ring_pts[30], 78, TERRA, rng, nx, tilt=0.85, rot=0.3, rings=5)
    art = D(art, W, H, *ring_pts[56], 54, CREAM, rng, nx, tilt=0.8, rot=-0.3, rings=5)
    art = D(art, W, H, *ring_pts[2], 46, BLUSH, rng, nx, tilt=0.82, rot=0.6, rings=4)
    show(art, "dh-wreath")
    save_full(art, f"{OUT}/wreath.webp", size=(300, 300), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 600, 120
    nx = Seq(61500); rng = random.Random(65)
    art = blank(W, H)
    for sgn in (-1, 1):
        pts = curve([(W / 2 + sgn * 40, 64), (W / 2 + sgn * 130, 56), (W / 2 + sgn * 220, 66), (W / 2 + sgn * 280, 60)], 40)
        art = G(art, strokes(W, H, [(pts, 2.6, (0.05, 0.8))]), "#7d8a58", "#4e5c36", seed=nx(), density=0.85, edge=0.4, rough=0.6, feather=0.5)
        for t, a in ((0.35, -0.6), (0.7, 0.5)):
            x, y = pts[int(t * 39)]
            art = dahlia_leaf(art, W, H, x, y, 34, (a if sgn > 0 else math.pi - a), rng, nx)
        x, y = pts[-1]
        art = buds(art, W, H, [(x, y)], 6, BLUSH, rng, nx)
    art = D(art, W, H, W / 2, 60, 44, TERRA, rng, nx, tilt=0.85, rings=5)
    show(art, "dh-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()
