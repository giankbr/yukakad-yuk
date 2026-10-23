"""Mawar Putih — white garden roses with deep green foliage in watercolour + gouache on soft ivory (syar'i: flora only).
Run: python3 -I mawar-putih.py [part ...]   parts: wreath cluster sprig rose corner
Assets -> public/themes/art/mawar-putih/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o6_lib import *

OUT = outdir("mawar-putih")
PARTS = sys.argv[1:] or ["wreath", "cluster", "sprig", "rose", "corner"]
LEAF = [("#3f6b4c", "#1c3a29"), ("#4d7a58", "#22432f"), ("#355e44", "#173222"), ("#5b8462", "#2a4a34")]
SAGE = ("#8ea98a", "#55785c")


def leafset(art, W, H, items, rng, nx, area=None):
    for (x, y, L, a) in items:
        art = rose_leaf(art, W, H, x, y, L, a, rng, nx, c=rng.choice(LEAF), area=area)
    return art


def filler(art, W, H, pts, rng, nx, n=3):
    """Tiny white waxflower sprays (five-dot blossoms) to lighten the greens."""
    for (x, y) in pts:
        for _ in range(n):
            bx, by = x + rng.gauss(0, 10), y + rng.gauss(0, 10)
            r = rng.uniform(4, 6.5)
            pet = circles(W, H, [(bx + math.cos(k * 1.256 + .3) * r * .8, by + math.sin(k * 1.256 + .3) * r * .8, r * .62) for k in range(5)])
            art = GP(art, pet, "#fbf8ef", "#e6dfcc", seed=nx(), rough=0.6, streak=0.1, pad=6)
            art = G(art, np.clip((pet - gaussian_filter(pet, 1)) * 3, 0, 1), "#8c937c", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.4, pad=4)
            art = G(art, circles(W, H, [(bx, by, r * .28)]), "#b8a85c", seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.5, pad=4)
    return art


def bouquet(W, H, roses, leaves, sprays, buds, fill, seed, sage=(), halo=1.0, front=True):
    rng = random.Random(seed); nx = Seq(seed * 10)
    back = blank(W, H)
    area = np.zeros((H, W), np.float32)
    for (pts, L) in sprays:
        back = rose_spray(back, W, H, curve(pts, 40), rng, nx, L=L, c=rng.choice(LEAF))
    for (pts, L) in sage:
        back = rose_spray(back, W, H, curve(pts, 30), rng, nx, L=L, c=SAGE, stem="#4d6b52")
    # foliage collar around every rose (radiating leaves), then the free leaves
    auto = []
    for (x, y, r, tilt, warm) in roses:
        n = rng.randint(5, 7)
        a0 = rng.uniform(0, math.tau)
        for k in range(n):
            a = a0 + k / n * math.tau + rng.uniform(-.3, .3)
            d = r * rng.uniform(0.55, 0.8)
            auto.append((x + math.cos(a) * d, y + math.sin(a) * d * tilt, r * rng.uniform(0.85, 1.15) * halo, a + rng.uniform(-.35, .35)))
    back = leafset(back, W, H, auto + list(leaves), rng, nx)
    clear()
    fl = blank(W, H)
    for (x, y, r, tilt, warm) in sorted(roses, key=lambda q: q[2]):
        fl = white_rose(fl, W, H, x, y, r, rng, nx, tilt=tilt, warm=warm, area=area)
        clear()
    back = knockout(back, area, 0.97, 1.5)
    art = over(back, fl)
    if front:  # a few leaves tucked over the rose rims
        fr = []
        for (x, y, r, tilt, warm) in roses[:4]:
            a = rng.uniform(0.3, 2.6)
            fr.append((x + math.cos(a) * r * 0.85, y + math.sin(a) * r * 0.85 * tilt, r * 0.55, a + rng.uniform(-.3, .3)))
        art = leafset(art, W, H, fr, rng, nx)
    for (x, y, s_, a) in buds:
        art = white_bud(art, W, H, x, y, s_, a, rng, nx)
    art = filler(art, W, H, fill, rng, nx)
    return art


if "wreath" in PARTS:
    # crescent wreath open to the right: roses heaped at lower-left, foliage tapering to both tips
    W, H = 800, 760
    cx, cy, R = 430, 380, 300
    arcp = lambda a, rr=R: (cx + math.cos(a) * rr, cy + math.sin(a) * rr)
    sprays = []
    for a0, a1, L in [(2.0, 0.55, 62), (2.4, 0.95, 56), (3.6, 5.2, 62), (3.2, 4.85, 56), (2.9, 1.7, 60), (3.0, 4.2, 58)]:
        pts = [arcp(a0 + (a1 - a0) * t, R + 30 * math.sin(t * 3 + a0)) for t in (0, .33, .66, 1)]
        sprays.append((pts, L))
    leaves = []
    rng0 = random.Random(5)
    for k in range(26):
        a = rng0.uniform(1.4, 4.9)
        x, y = arcp(a, R + rng0.uniform(-40, 40))
        leaves.append((x, y, rng0.uniform(52, 78), a + math.pi / 2 * rng0.choice([-1, 1]) + rng0.uniform(-.5, .5)))
    roses = []
    for a, r, t, w, dr in [(2.7, 104, .8, .3, 0), (3.25, 84, .7, .6, 18), (2.15, 86, .86, .5, -6), (3.8, 64, .78, .4, 6), (1.62, 66, .7, .7, 10),
                           (2.45, 54, .9, .5, 76), (3.05, 50, .72, .4, -70), (4.3, 44, .8, .5, 0), (1.15, 42, .82, .6, 0)]:
        x, y = arcp(a, R + dr)
        roses.append((x, y, r, t, w))
    buds = [(*arcp(4.55, R + 6), 15, -0.3), (*arcp(1.12, R + 4), 14, 0.9), (*arcp(4.3, R - 30), 12, -1.0), (*arcp(1.4, R + 40), 12, 1.6)]
    fill = [arcp(a, R + rng0.uniform(-30, 30)) for a in (1.3, 1.9, 2.45, 3.05, 3.6, 4.15, 4.7)]
    sage = [([arcp(2.5, R + 20), arcp(2.4, R + 90), arcp(2.2, R + 130)], 34), ([arcp(3.6, R + 20), arcp(3.8, R + 90), arcp(4.0, R + 120)], 32)]
    art = bouquet(W, H, roses, leaves, sprays, buds, fill, 71, sage)
    save(art, f"{OUT}/wreath.webp", max_w=760, quality=80)
    prev(art, "mp_wreath")

if "cluster" in PARTS:
    W, H = 600, 440
    sprays = [([(300, 260), (180, 230), (70, 250), (20, 300)], 58), ([(300, 260), (420, 220), (530, 236), (585, 280)], 58),
              ([(300, 250), (240, 140), (200, 60)], 50), ([(310, 260), (400, 340), (470, 410)], 52), ([(290, 270), (200, 350), (120, 400)], 50)]
    leaves = [(220, 200, 70, -2.4), (380, 200, 70, -0.7), (300, 330, 70, 1.6), (160, 280, 64, 2.6), (450, 300, 64, 0.5), (330, 160, 60, -1.3)]
    roses = [(300, 245, 100, .86, .4), (178, 290, 72, .88, .6), (425, 285, 76, .84, .3)]
    buds = [(110, 210, 14, -2.5), (500, 200, 14, -0.6), (260, 120, 12, -1.9)]
    fill = [(240, 340), (370, 360), (330, 150), (90, 330), (520, 330)]
    art = bouquet(W, H, roses, leaves, sprays, buds, fill, 83)
    save(art, f"{OUT}/cluster.webp", max_w=520, quality=80)
    prev(art, "mp_cluster")

if "sprig" in PARTS:
    W, H = 560, 140
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    for side in (-1, 1):
        pts = curve([(280, 74), (280 + side * 110, 64), (280 + side * 200, 76), (280 + side * 262, 60)], 40)
        art = rose_spray(art, W, H, pts, rng, nx, L=40, c=LEAF[0 if side < 0 else 2])
    area = np.zeros((H, W), np.float32)
    fl = white_rose(blank(W, H), W, H, 280, 72, 34, rng, nx, tilt=0.8, area=area)
    art = over(knockout(art, area, 0.97, 1.2), fl)
    art = filler(art, W, H, [(226, 64), (336, 66)], rng, nx, n=2)
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=82)
    prev(art, "mp_sprig")

if "rose" in PARTS:
    W, H = 300, 280
    rng = random.Random(21); nx = Seq(2100)
    back = blank(W, H); area = np.zeros((H, W), np.float32)
    back = leafset(back, W, H, [(150, 150, 92, -0.35), (150, 150, 88, -2.7), (150, 160, 80, 1.95)], rng, nx)
    fl = white_rose(blank(W, H), W, H, 150, 138, 78, rng, nx, area=area)
    art = over(knockout(back, area, 0.97, 1.5), fl)
    save(art, f"{OUT}/rose.webp", max_w=220, quality=82)
    prev(art, "mp_rose")

if "corner" in PARTS:
    # foliage corner for the deep-green bands: lighter sage + green leaves so it reads on dark, one white rose + bud
    W, H = 460, 440
    sprays = [([(30, 420), (120, 300), (240, 230), (380, 210)], 56), ([(20, 430), (60, 300), (80, 170), (70, 40)], 54), ([(40, 420), (200, 380), (330, 400), (440, 420)], 50)]
    sage = [([(40, 410), (160, 250), (230, 120)], 40), ([(50, 420), (260, 330), (400, 300)], 38)]
    leaves = [(120, 340, 70, -0.9), (90, 260, 64, -1.8), (210, 320, 66, -0.2)]
    art = bouquet(W, H, [(110, 360, 70, .86, .5)], leaves, sprays, [(250, 240, 13, -0.6), (70, 160, 12, -1.7)], [(170, 280), (60, 300)], 97, sage)
    save(art, f"{OUT}/corner.webp", max_w=360, quality=80)
    prev(art, "mp_corner", bg="#17301f")

kb(OUT)
