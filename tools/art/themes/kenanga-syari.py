"""Kenanga Syari — watercolour cananga (kenanga): long drooping, twisted yellow-green petals hanging in clusters under
glossy leaves, on quiet cream. Run: python3 -I kenanga-syari.py [part ...]
parts: branch blossom sprig. Assets -> public/themes/art/kenanga-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m4_lib import *

OUT = outdir("kenanga-syari")
PARTS = sys.argv[1:] or ["branch", "blossom", "sprig", "wash"]
CREAM = "#f6f1e3"
PET_A, PET_B, PET_D = "#d9d36a", "#ecd862", "#a7a440"
LEAF_A, LEAF_B, LEAF_D = "#7d9858", "#58784a", "#3a5634"
TWIG = "#6d5a40"


def petal_poly(x, y, ang, L, wd, rng, wave=0.12, n=26):
    """Long narrow cananga petal from (x, y) along ang (radians, 0 = right, pi/2 = down), wavy and twisted."""
    ph = rng.uniform(0, math.tau)
    left, right = [], []
    droop = rng.uniform(0.3, 0.55)
    for i in range(n + 1):
        t = i / n
        a = ang + droop * t * t * (1 if math.cos(ang) >= 0 else -1) * 0.6
        lat = math.sin(t * 7.5 + ph) * L * wave * 0.45 * t
        cx = x + math.cos(ang) * L * t - math.sin(ang) * lat
        cy = y + math.sin(ang) * L * t + math.cos(ang) * lat + L * droop * t * t * 0.35
        w = wd * (math.sin(math.pi * min(1, t * 1.06)) ** 0.5) * (0.35 + 0.65 * abs(math.cos(t * 5.0 + ph)))
        nxv, nyv = -math.sin(a), math.cos(a)
        left.append((cx + nxv * w, cy + nyv * w))
        right.append((cx - nxv * w, cy - nyv * w))
    return left + right[::-1]


def flower(art, W, H, x, y, s, rng, nx, ripe=0.5, alpha=1.0):
    """One hanging cananga flower: 3 outer + 3 inner petals spread downward from the calyx at (x, y)."""
    angs = [math.radians(a + rng.uniform(-8, 8)) for a in (40, 66, 90, 112, 138, 80)]
    order = list(range(6))
    rng.shuffle(order)
    for k in order:
        L = s * rng.uniform(0.85, 1.12) * (0.92 if k == 5 else 1)
        pm = shapes(W, H, [petal_poly(x, y, angs[k], L, s * 0.1, rng)])
        col_a = mix(PET_A, PET_B, rng.random())
        art = G(art, pm, col_a, mix(col_a, "#c8d070", 0.4), seed=nx(), density=0.86 * alpha, edge=0.65, bloom=0.35, rough=2.2, feather=0.9, gran=0.3)
        # greener near the base, a brown-maroon spot on ripe flowers
        base = pm * circles(W, H, [(x, y, s * 0.32)])
        art = G(art, gaussian_filter(base, 2), "#9aa648", seed=nx(), density=0.55 * alpha, edge=0.2, bloom=0.2, rough=1.5)
        if rng.random() < ripe:
            spot = pm * circles(W, H, [(x + math.cos(angs[k]) * s * 0.12, y + math.sin(angs[k]) * s * 0.12, s * 0.07)])
            art = G(art, spot, "#8a5a2a", seed=nx(), density=0.5 * alpha, edge=0.3, bloom=0, rough=1)
        # a faint vein down the petal
        vein = strokes(W, H, [(curve([(x, y)] + [(x + math.cos(angs[k]) * L * t, y + math.sin(angs[k]) * L * t) for t in (0.4, 0.75)], 10), 0.9, (0.1, 0.6))])
        art = G(art, vein * pm, PET_D, seed=nx(), density=0.35 * alpha, edge=0, bloom=0, rough=0.8)
    cal = circles(W, H, [(x, y, s * 0.05)])
    art = G(art, cal, "#6f8a3a", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=1)
    return art


def leaf(art, W, H, x, y, L, ang, rng, nx, tone=0.5):
    pts = petal_pts(x, y, L, L * 0.2, ang, n=18, cup=rng.uniform(-0.1, 0.1))
    m = shapes(W, H, [deform(pts, rng, 1, 0.025)])
    ca = mix(LEAF_A, LEAF_B, tone)
    art = G(art, m, ca, mix(ca, "#9aae6a", 0.3), seed=nx(), density=0.8, edge=0.55, bloom=0.4, rough=3, feather=1.1, gran=0.25)
    # half-leaf shading and midrib
    tip = (x + math.cos(ang) * L, y + math.sin(ang) * L)
    rib = [(x + (tip[0] - x) * t + math.sin(t * math.pi) * L * 0.03, y + (tip[1] - y) * t) for t in np.linspace(0, 0.95, 12)]
    nrm = (-math.sin(ang), math.cos(ang))
    half = m * shapes(W, H, [rib + [(p[0] + nrm[0] * L * 0.4, p[1] + nrm[1] * L * 0.4) for p in rib[::-1]]], smooth=False)
    art = G(art, half, LEAF_D, seed=nx(), density=0.4, edge=0.3, bloom=0.3, rough=2)
    art = soft(art, strokes(W, H, [(rib, 1.3, (0.05, 0.4))]) * m, "#c9d49a", alpha=0.6, pad=4)
    veins = []
    for t in np.linspace(0.18, 0.8, 6):
        p = rib[int(t * 11)]
        for sgn in (-1, 1):
            veins.append(([p, (p[0] + math.cos(ang + sgn * 0.7) * L * 0.16, p[1] + math.sin(ang + sgn * 0.7) * L * 0.16)], 0.8, (0.05, 0.6)))
    art = G(art, strokes(W, H, veins) * m, LEAF_D, seed=nx(), density=0.3, edge=0, bloom=0, rough=0.6)
    return art


def cluster(art, W, H, x, y, s, rng, nx, n=3, stalk=40):
    """A short pedicel bunch hanging from the twig at (x, y): n flowers at staggered depths."""
    tips = []
    for k in range(n):
        dx = (k - (n - 1) / 2) * s * 0.45 + rng.uniform(-6, 6)
        dy = stalk + rng.uniform(0, s * 0.35) + (k % 2) * s * 0.2
        tips.append((x + dx, y + dy))
    st = strokes(W, H, [(curve([(x, y), (x + (tx - x) * 0.4, y + (ty - y) * 0.5), (tx, ty)], 10), 2.2, (0.0, 0.3)) for tx, ty in tips])
    art = G(art, st, "#6e7e3a", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=1)
    for k, (tx, ty) in enumerate(sorted(tips, key=lambda p: p[1])):
        art = flower(art, W, H, tx, ty, s * rng.uniform(0.85, 1.05), rng, nx, ripe=0.45)
        clear()
    return art


if "branch" in PARTS:
    # one branch enters from the top-right corner and arcs down-left; leaves alternate, three clusters hang at
    # different heights, the left of the page stays open for the names
    W, H = 640, 880
    nx = Seq(50000)
    rng = random.Random(5)
    art = blank(W, H)
    twig = curve([(660, -10), (560, 90), (470, 200), (380, 330), (300, 470), (250, 560)], 90)
    art = G(art, strokes(W, H, [(twig, 8, (0.0, 0.7))]), TWIG, "#8a7450", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=1.5)
    leaves = [(8, -10, 170), (16, 150, 150), (24, 20, 175), (33, 175, 150), (41, 40, 165), (50, 195, 140), (58, 60, 150), (66, 210, 120), (74, 70, 120), (82, 230, 90), (87, 100, 80)]
    for i, a, L in leaves:
        px, py = twig[i]
        art = leaf(art, W, H, px, py, L * rng.uniform(0.9, 1.08), math.radians(a + rng.uniform(-10, 10)), rng, nx, tone=rng.random())
        clear()
    for (i, s_, n, st) in ((20, 170, 3, 40), (46, 160, 2, 54), (78, 140, 2, 34)):
        art = cluster(art, W, H, twig[i][0], twig[i][1] + 4, s_, rng, nx, n=n, stalk=st)
    for (fx, fy, fa) in ((160, 760, 0.5), (420, 820, 2.5)):
        art = G(art, shapes(W, H, [petal_poly(fx, fy, fa, 80, 9, rng)]), PET_A, PET_B, seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=2)
    prev(art, "kg-branch", CREAM)
    save_rgba_full(art, f"{OUT}/branch.webp", size=(520, 715), quality=82)

if "blossom" in PARTS:
    W, H = 360, 420
    nx = Seq(51000)
    rng = random.Random(12)
    art = blank(W, H)
    # tiny bit of twig with one leaf, two flowers hanging
    tw = curve([(70, 40), (190, 30), (310, 44)], 20)
    art = G(art, strokes(W, H, [(tw, 5, (0.1, 0.4))]), TWIG, seed=nx(), density=0.9, edge=0.4, bloom=0, rough=1)
    art = leaf(art, W, H, 210, 36, 120, math.radians(-12), rng, nx, tone=0.3)
    art = cluster(art, W, H, 175, 36, 170, rng, nx, n=2, stalk=36)
    prev(art, "kg-blossom", CREAM)
    save(art, f"{OUT}/blossom.webp", max_w=180, quality=84)

if "sprig" in PARTS:
    W, H = 640, 380
    nx = Seq(52000)
    rng = random.Random(33)
    art = blank(W, H)
    tw = curve([(30, 120), (200, 96), (400, 100), (610, 130)], 40)
    art = G(art, strokes(W, H, [(tw, 5, (0.0, 0.5))]), TWIG, seed=nx(), density=0.9, edge=0.4, bloom=0, rough=1)
    for (i, a, L) in ((8, -150, 120), (16, -60, 130), (24, -120, 110), (32, -40, 120), (36, 30, 100)):
        art = leaf(art, W, H, tw[i][0], tw[i][1], L, math.radians(a), rng, nx, tone=rng.random())
        clear()
    art = cluster(art, W, H, tw[12][0], tw[12][1], 140, rng, nx, n=2, stalk=24)
    art = cluster(art, W, H, tw[28][0], tw[28][1], 120, rng, nx, n=1, stalk=20)
    prev(art, "kg-sprig", CREAM)
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=84)

if "wash" in PARTS:
    # loose pale wash behind the monograms: two glazes, a hard wet rim, a bloom
    W, H = 440, 440
    nx = Seq(53000)
    rng = random.Random(8)
    art = blank(W, H)
    m = shapes(W, H, [deform(ellipse_pts(220, 220, 170, 176, 14), rng, 3, 0.07)])
    art = G(art, m, "#e8e6b4", "#dfe2b0", seed=nx(), density=0.55, edge=0.75, bloom=0.55, rough=8, feather=2)
    m2 = shapes(W, H, [deform(ellipse_pts(236, 206, 120, 110, 12), rng, 3, 0.1)])
    art = G(art, m2, "#d9dc98", seed=nx(), density=0.3, edge=0.6, bloom=0.5, rough=7, feather=2)
    prev(art, "kg-wash", CREAM)
    save(art, f"{OUT}/wash.webp", max_w=300, quality=74)
