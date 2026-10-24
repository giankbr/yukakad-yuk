"""Toska Syari — fresh tosca watercolour with fine gold foil: a big wet tosca disc with a pressed-foil eight-fold rosette
(khatam star, interlaced squares, ring of arcs), sprays of round eucalyptus leaves in tosca/teal washes on gold-foil
stems, a small foil star and a hairline foil divider. Geometry and flora only (no figures).
Run: python3 -I toska-syari.py [part ...]   parts: cakra ranting daun bintang garis"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s1_lib import *

OUT = outdir("toska-syari")
PARTS = sys.argv[1:] or ["cakra", "ranting", "daun", "bintang", "garis"]
T_L, T, T_D, T_DD = "#9fe0d6", "#3fbfae", "#1f9488", "#0f6a62"
GOLD = "#c9a04e"
PAPER = "#fbfdfc"


def star_pts(cx, cy, r, n=8, inner=0.0, rot=0.0):
    """Two interlaced squares (n=8) as one polygon outline of a star when inner given, else regular polygon."""
    pts = []
    for k in range(n * (2 if inner else 1)):
        a = rot + k * math.pi / (n if inner else n / 2) / (1 if inner else 1)
        rr = r if (not inner or k % 2 == 0) else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def square(cx, cy, r, rot):
    return [(cx + math.cos(rot + k * math.pi / 2) * r, cy + math.sin(rot + k * math.pi / 2) * r) for k in range(4)]


def outline(W, H, polys, width):
    items = []
    for p in polys:
        items.append((p + [p[0]], width, None))
    return strokes(W, H, items)


def rosette(W, H, cx, cy, R, w):
    """Line mask of an eight-fold rosette: khatam (two squares), inner octagram, circles, petal arcs, rays."""
    polys = [square(cx, cy, R * 0.62, 0), square(cx, cy, R * 0.62, math.pi / 4),
             square(cx, cy, R * 0.36, math.pi / 8), square(cx, cy, R * 0.36, math.pi / 8 + math.pi / 4)]
    m = outline(W, H, polys, w)
    rings = [(arc_pts(cx, cy, R * f, 0, 2 * math.pi, 120), w * k, None) for f, k in [(0.98, 1.1), (0.9, 0.6), (0.2, 0.8)]]
    arcs = []
    for k in range(16):
        a = k * math.pi / 8
        px, py = cx + math.cos(a) * R * 0.78, cy + math.sin(a) * R * 0.78
        arcs.append((arc_pts(px, py, R * 0.12, a - math.pi * 0.75, a + math.pi * 0.75, 18), w * 0.8, None))
    rays = []
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        rays.append(([(cx + math.cos(a) * R * 0.36, cy + math.sin(a) * R * 0.36), (cx + math.cos(a) * R * 0.88, cy + math.sin(a) * R * 0.88)], w * 0.6, None))
    dots = circles(W, H, [(cx + math.cos(k * math.pi / 4) * R * 0.62 * 1.0, cy + math.sin(k * math.pi / 4) * R * 0.62, w * 1.6) for k in range(8)])
    return np.clip(m + strokes(W, H, rings + arcs + rays) + dots, 0, 1)


def euca_spray(art, W, H, pts, rng, nx, leaf_r=(16, 30), pairs=8, gold=True, fade=1.0):
    """A eucalyptus spray: a curved foil stem with paired round leaves, smaller towards the tip."""
    stem = curve(pts, 60)
    n = len(stem)
    leaves, pets = [], []
    k = 4
    while k < n - 2:
        t = k / n
        x, y = stem[k]
        dx, dy = stem[min(n - 1, k + 1)][0] - stem[k - 1][0], stem[min(n - 1, k + 1)][1] - stem[k - 1][1]
        L = math.hypot(dx, dy) or 1
        nxv, nyv = -dy / L, dx / L
        r = (leaf_r[1] - (leaf_r[1] - leaf_r[0]) * t) * rng.uniform(0.85, 1.1)
        for side in (-1, 1):
            off = r * 1.08
            lx, ly = x + nxv * off * side + dx / L * r * 0.25, y + nyv * off * side + dy / L * r * 0.25
            leaves.append((lx, ly, r, rng.random()))
            pets.append(([(x, y), (x + (lx - x) * 0.3, y + (ly - y) * 0.3)], 1.6, (0.0, 0.3)))
        k += max(3, int(n / pairs * (1 - 0.35 * t)))
    art = G(art, strokes(W, H, pets) * fade, T_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    # paint leaves back-to-front in two tone groups so they overlap like glazes
    for grp, (ca, cb, dens) in enumerate([(T_L, T, 0.62), (T, T_D, 0.7)]):
        sel = [(x, y, r) for x, y, r, q in leaves if (q < 0.5) == (grp == 0)]
        if not sel:
            continue
        m = ellipses(W, H, [(x, y, r, r * 0.86, rng.uniform(0, 180)) for x, y, r in sel])
        art = G(art, m * fade, ca, cb, seed=nx(), density=dens, edge=0.65, bloom=0.45, gran=0.3, rough=2.2, feather=0.9)
    # a few darker veins (midribs)
    mids = [([(x - r * 0.5, y + r * 0.3), (x + r * 0.5, y - r * 0.3)], 1.2, (0.2, 0.4)) for x, y, r, q in leaves if q > 0.55]
    if mids:
        art = G(art, strokes(W, H, mids) * fade, T_DD, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.4)
    sm = strokes(W, H, [(stem, 3.0, (0.0, 0.6))])
    art = FO(art, sm * fade, GOLD, seed=nx(), emboss=0.4, sparkle=0.15) if gold else G(art, sm, T_DD, seed=nx(), density=0.7)
    return art


if "cakra" in PARTS:
    W = H = 640
    rng = random.Random(171); nx = Seq(171000)
    art = blank(W, H)
    disc = circles(W, H, [(320, 320, 280)])
    art = G(art, disc, T_L, T, seed=nx(), density=0.62, edge=0.7, bloom=0.55, gran=0.35, rough=6, feather=2.0, mottle=0.7)
    inner = circles(W, H, [(338, 300, 190)])
    art = G(art, inner * disc, T, T_D, seed=nx(), density=0.28, edge=0.3, bloom=0.6, gran=0.35, rough=9, feather=6)
    ros = rosette(W, H, 320, 320, 236, 3.4)
    art = FO(art, ros, GOLD, seed=nx(), emboss=0.5, sparkle=0.2)
    preview(art, "ts-cakra", tone=PAPER)
    save(art, f"{OUT}/cakra.webp", max_w=560, quality=80)
    clear()

if "ranting" in PARTS:
    W, H = 560, 720
    rng = random.Random(172); nx = Seq(172000)
    art = blank(W, H)
    art = euca_spray(art, W, H, [(470, 700), (420, 520), (330, 360), (220, 230), (120, 120), (50, 40)], rng, nx, leaf_r=(14, 34), pairs=11)
    art = euca_spray(art, W, H, [(420, 520), (500, 400), (530, 300), (520, 210)], rng, nx, leaf_r=(12, 24))
    art = euca_spray(art, W, H, [(330, 360), (250, 380), (160, 420), (90, 480)], rng, nx, leaf_r=(10, 22))
    preview(art, "ts-ranting", tone=PAPER)
    save(art, f"{OUT}/ranting.webp", max_w=360, quality=80)
    clear()

if "daun" in PARTS:
    # small spray for nodes / amp / sent
    W, H = 300, 220
    rng = random.Random(173); nx = Seq(173000)
    art = blank(W, H)
    art = euca_spray(art, W, H, [(20, 200), (110, 140), (200, 90), (280, 30)], rng, nx, leaf_r=(10, 22))
    preview(art, "ts-daun", tone=PAPER)
    save(art, f"{OUT}/daun.webp", max_w=160, quality=82)
    clear()

if "bintang" in PARTS:
    W = H = 200
    rng = random.Random(174); nx = Seq(174000)
    art = blank(W, H)
    st = shapes(W, H, [square(100, 100, 70, 0), square(100, 100, 70, math.pi / 4)], smooth=False)
    hole = shapes(W, H, [square(100, 100, 44, math.pi / 8), square(100, 100, 44, math.pi / 8 + math.pi / 4)], smooth=False)
    wash = circles(W, H, [(100, 100, 40)])
    art = G(art, wash, T_L, T, seed=nx(), density=0.65, edge=0.6, bloom=0.3, rough=2, feather=1)
    art = FO(art, np.clip(st - hole, 0, 1) + circles(W, H, [(100, 100, 7)]), GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    preview(art, "ts-bintang", tone=PAPER)
    save(art, f"{OUT}/bintang.webp", max_w=100, quality=84)
    clear()

if "garis" in PARTS:
    W, H = 640, 80
    rng = random.Random(175); nx = Seq(175000)
    art = blank(W, H)
    ln = strokes(W, H, [([(30, 40), (270, 40)], 2.2, (0.6, 0.0)), ([(370, 40), (610, 40)], 2.2, (0.0, 0.6))])
    st = shapes(W, H, [square(320, 40, 24, 0), square(320, 40, 24, math.pi / 4)], smooth=False)
    hole = shapes(W, H, [square(320, 40, 14, math.pi / 8), square(320, 40, 14, math.pi / 8 + math.pi / 4)], smooth=False)
    dots = circles(W, H, [(290, 40, 3), (350, 40, 3), (278, 40, 2), (362, 40, 2)])
    wash = ell(W, H, 320, 40, 60, 18)
    art = G(art, wash, T_L, seed=nx(), density=0.5, edge=0.5, bloom=0.4, rough=3, feather=1.5)
    art = FO(art, np.clip(ln + np.clip(st - hole, 0, 1) + dots, 0, 1), GOLD, seed=nx(), emboss=0.5, sparkle=0.15)
    preview(art, "ts-garis", tone=PAPER)
    save(art, f"{OUT}/garis.webp", max_w=320, quality=84)
    clear()
