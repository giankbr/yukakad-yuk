"""Herbarium Klasik — pressed dried specimens on herbarium sheets: flattened cosmos, fern frond, lavender sprig and a
small leafy twig in faded, slightly translucent washes with browned rims; paper masking tape; kraft and cotton
mounting-sheet tiles. Run: python3 -I herbarium-klasik.py [part ...]
parts: kraft sheet cosmos fern sprig twig tape. Assets -> public/themes/art/herbarium-klasik/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a5_lib import *

OUT = outdir("herbarium-klasik")
PARTS = sys.argv[1:] or ["kraft", "sheet", "cosmos", "fern", "sprig", "twig", "tape"]
SHEET = "#f1e9d6"
KRAFT = "#b68e60"
BROWN = "#7a5532"
STEM, STEM_D = "#8d8456", "#5f5934"
LEAF, LEAF_D = "#98955f", "#6d6a3e"


def pressed(art, mask, c1, c2, seed, rim="#8a5f3a", density=0.55, pad=14):
    """Flattened, translucent plant tissue: faded wash, browned rim where it dried first, faint shadow of its thickness."""
    sh = np.roll(np.roll(gaussian_filter(mask, 1.6), 2, 0), 2, 1) * 0.22
    art = OV(art, sh, lambda m: layer(m, "#4a3a28", 1.0), pad=pad)
    art = G(art, mask, c1, c2, seed=seed, density=density, edge=0.7, bloom=0.45, gran=0.3, rough=1.6, feather=0.7, pad=pad)
    ring = np.clip(mask - gaussian_filter(mask, 2.2) * 1.05, 0, 1) * 2.2
    return G(art, np.clip(ring, 0, 1), rim, seed=seed + 5, density=0.42, edge=0.2, bloom=0.1, rough=1, feather=0.6, pad=pad)


def stem_items(pts, w0, w1):
    n = len(pts)
    return [([pts[i], pts[i + 1]], w0 + (w1 - w0) * (i / (n - 1)), None) for i in range(n - 1)]


def cosmos_petal(cx, cy, L, Wd, ang, rng):
    loc = [(0, 0), (0.3, -0.32), (0.7, -0.5), (0.95, -0.42), (1.0, -0.22), (0.94, -0.12), (1.0, 0.0), (0.94, 0.12), (1.0, 0.22), (0.95, 0.42), (0.7, 0.5), (0.3, 0.32)]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + (u * L * rng.uniform(.97, 1.03)) * ca - (v * Wd * 2) * sa, cy + (u * L * rng.uniform(.97, 1.03)) * sa + (v * Wd * 2) * ca) for u, v in loc]


def flower(art, W, H, x, y, r, rng, nx, rot=0.0):
    polys = [cosmos_petal(x, y, r, r * 0.215, rot + k * math.tau / 8 + rng.uniform(-0.08, 0.08), rng) for k in range(8)]
    m = shapes(W, H, polys)
    art = pressed(art, m, "#c88aa4", "#b47a95", nx(), rim="#86506a", density=0.5)
    veins = []
    for k in range(8):
        a = rot + k * math.tau / 8
        for dv in (-0.12, 0, 0.12):
            veins.append(([(x + math.cos(a + dv) * r * 0.2, y + math.sin(a + dv) * r * 0.2), (x + math.cos(a + dv * 0.6) * r * 0.85, y + math.sin(a + dv * 0.6) * r * 0.85)], 1.0, (0.1, 0.4)))
    art = G(art, strokes(W, H, veins) * m, "#8e5470", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.4, pad=8)
    disc = circles(W, H, [(x, y, r * 0.2)])
    art = pressed(art, disc, "#c59a3e", "#9c7428", nx(), rim="#6b4a1e", density=0.85)
    dots_ = circles(W, H, [(x + math.cos(a) * rr, y + math.sin(a) * rr, 1.6) for a, rr in [(rng.uniform(0, 6.3), rng.uniform(0, r * 0.18)) for _ in range(24)]])
    return G(art, dots_, "#5a3e1a", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.5, feather=0.4, pad=6)


def leaflet(W, H, x, y, L, Wd, ang, rng, lobes=0):
    pts = petal_pts(x, y, L, Wd, ang, n=16)
    if lobes:
        pts = deform(pts, rng, 1, 0.06)
    return pts


if "kraft" in PARTS:
    n = 420
    base = rgb_arr(n, n, KRAFT)
    base *= (1 + (wrap_noise(n, n, 3, 24) - 0.5) * 0.08 + (wrap_noise(n, n, 4, 0.7) - 0.5) * 0.09)[..., None]
    fib = wrap_noise(n, n, 5, 0.6)
    fibx = gaussian_filter(np.random.default_rng(6).random((n, n)).astype(np.float32), (0.5, 5), mode="wrap")
    fibx = (fibx - fibx.min()) / (fibx.max() - fibx.min())
    base *= (1 + (fibx - 0.5) * 0.1)[..., None]
    spk = (np.random.default_rng(7).random((n, n)) > 0.9965).astype(np.float32)
    spk = gaussian_filter(spk, 0.7, mode="wrap") * 3
    base = base * (1 - np.clip(spk, 0, 1)[..., None] * 0.35)
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/kraft.webp", quality=72)
    clear()

if "sheet" in PARTS:
    n = 480
    rng = random.Random(51)
    base = rgb_arr(n, n, SHEET)
    base *= (1 + (wrap_noise(n, n, 8, 30) - 0.5) * 0.05 + (wrap_noise(n, n, 9, 0.8) - 0.5) * 0.04)[..., None]
    # foxing: small rusty age spots
    fox = wrap_circles(n, n, [(rng.uniform(0, n), rng.uniform(0, n), r, r * rng.uniform(.7, 1), 0) for r in [rng.uniform(1.2, 4.5) for _ in range(26)]])
    fox = gaussian_filter(fox, 1.4, mode="wrap")
    tint = rgb_arr(n, n, "#b98a58")
    base = base * (1 - fox[..., None] * 0.28) + tint * fox[..., None] * 0.28
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/sheet.webp", quality=74)
    clear()

if "cosmos" in PARTS:
    W, H = 560, 940
    rng = random.Random(52); nx = Seq(50100)
    art = blank(W, H)
    s1 = curve([(270, 930), (262, 700), (250, 480), (232, 300), (200, 170)], 60)
    s2 = curve([(258, 640), (330, 520), (380, 400), (400, 330)], 40)
    s3 = curve([(248, 520), (190, 470), (150, 420)], 24)
    stem = strokes(W, H, stem_items(s1, 6, 3) + stem_items(s2, 4, 2.4) + stem_items(s3, 3, 1.6))
    # feathery thread leaves
    fl = []
    for (bx, by, side, L) in [(264, 820, -1, 150), (266, 760, 1, 140), (256, 600, -1, 130), (252, 560, 1, 110), (244, 420, -1, 100)]:
        main = curve([(bx, by), (bx + side * L * 0.5, by - L * 0.25), (bx + side * L, by - L * 0.15)], 20)
        fl += stem_items(main, 2.4, 1)
        for (x, y, a) in along(main, 20):
            for sg in (-1, 1):
                aa = a + sg * 0.9
                fl.append(([(x, y), (x + math.cos(aa) * 26, y + math.sin(aa) * 26 - 4)], 1.6, (0.0, 0.6)))
    leaves = strokes(W, H, fl)
    art = pressed(art, leaves, LEAF, LEAF_D, nx(), rim="#6a5a30", density=0.7)
    art = pressed(art, stem, STEM, STEM_D, nx(), rim="#5d4a2a", density=0.8)
    art = flower(art, W, H, 196, 150, 112, rng, nx, rot=0.2)
    art = flower(art, W, H, 404, 318, 84, rng, nx, rot=0.6)
    bud_m = shapes(W, H, [petal_pts(150, 420, 40, 16, -2.2, n=12)])
    art = pressed(art, bud_m, "#8d7a4a", "#6d5a30", nx(), rim="#4d3a1e", density=0.75)
    art = pressed(art, shapes(W, H, [petal_pts(142, 410, 26, 9, -2.3, n=10)]), "#b6829a", "#9a6a82", nx(), density=0.55)
    preview(art, "hk-cosmos", tone=SHEET)
    save(art, f"{OUT}/cosmos.webp", max_w=300, quality=80)
    clear()

if "fern" in PARTS:
    W, H = 520, 960
    rng = random.Random(53); nx = Seq(50200)
    art = blank(W, H)
    rach = curve([(250, 950), (254, 760), (268, 520), (300, 290), (350, 70)], 80)
    polys = []
    pts = along(rach, 30)
    N = len(pts)
    for i, (x, y, a) in enumerate(pts[1:], 1):
        t = i / N
        L = (36 + 118 * math.sin(math.pi * min(1, t * 1.15 + 0.05)) ** 0.8) * (1 - t * 0.45)
        for sg in (-1, 1):
            aa = a + sg * (1.25 - t * 0.3)
            off = sg * 8
            polys.append(leaflet(W, H, x, y + off * 0.2, L, L * 0.12, aa + rng.uniform(-.05, .05), rng, lobes=1))
    m = shapes(W, H, polys)
    art = pressed(art, m, LEAF, "#86834e", nx(), rim="#7a5a2e", density=0.62)
    # pinnule cuts: lighter notches across each pinna (serration) + midribs
    ribs = []
    for i, (x, y, a) in enumerate(pts[1:], 1):
        t = i / N
        L = (36 + 118 * math.sin(math.pi * min(1, t * 1.15 + 0.05)) ** 0.8) * (1 - t * 0.45)
        for sg in (-1, 1):
            aa = a + sg * (1.25 - t * 0.3)
            ribs.append(([(x, y), (x + math.cos(aa) * L * 0.92, y + math.sin(aa) * L * 0.92)], 1.3, (0.0, 0.5)))
    art = G(art, strokes(W, H, ribs) * m, LEAF_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = pressed(art, strokes(W, H, stem_items(rach, 5, 1.6)), "#7e6b40", "#5c4a28", nx(), rim="#4a3820", density=0.85)
    # a few browned, dried tips
    tips = shapes(W, H, polys[-10:]) * m
    art = G(art, tips, "#a37a46", seed=nx(), density=0.35, edge=0.3, bloom=0.3, rough=1)
    preview(art, "hk-fern", tone=SHEET)
    save(art, f"{OUT}/fern.webp", max_w=280, quality=80)
    clear()

if "sprig" in PARTS:
    W, H = 380, 760
    rng = random.Random(54); nx = Seq(50300)
    art = blank(W, H)
    stems = [curve([(190, 750), (184, 500), (160, 260), (130, 90)], 40), curve([(194, 750), (200, 480), (226, 250), (262, 110)], 40),
             curve([(192, 750), (192, 520), (190, 320), (194, 160)], 40)]
    sm = strokes(W, H, sum([stem_items(p, 4, 2) for p in stems], []))
    lv = shapes(W, H, [petal_pts(188, 640, 90, 9, -2.0), petal_pts(196, 600, 84, 8, -1.1), petal_pts(190, 560, 70, 7, -2.3)])
    art = pressed(art, lv, "#9aa07a", "#7a8058", nx(), rim="#6a6038", density=0.6)
    art = pressed(art, sm, STEM, STEM_D, nx(), density=0.8)
    florets = []
    for p in stems:
        top = p[-int(len(p) * 0.45):]
        for (x, y, a) in along(top, 11):
            for sg in (-1, 1):
                florets.append((x + sg * rng.uniform(4, 8), y + rng.uniform(-3, 3), rng.uniform(5.5, 7.5), rng.uniform(3.4, 4.6), math.degrees(a) + sg * 30))
    fm = ellipses(W, H, florets)
    art = pressed(art, fm, "#9b88b5", "#7d6b98", nx(), rim="#5a4870", density=0.66)
    preview(art, "hk-sprig", tone=SHEET)
    save(art, f"{OUT}/sprig.webp", max_w=200, quality=80)
    clear()

if "twig" in PARTS:
    W, H = 640, 220
    rng = random.Random(55); nx = Seq(50400)
    art = blank(W, H)
    st = curve([(20, 150), (180, 120), (360, 104), (520, 80), (620, 60)], 50)
    leaves = []
    for k, (x, y, a) in enumerate(along(st, 56)):
        if x > 600:
            continue
        sg = 1 if k % 2 else -1
        L = 64 - k * 3
        leaves.append(petal_pts(x, y, L, L * 0.26, a + sg * 0.85, n=14))
    lm = shapes(W, H, leaves)
    art = pressed(art, lm, LEAF, LEAF_D, nx(), rim="#7a5a2e", density=0.6)
    veins = [([(x, y), (x + math.cos(a + (0.85 if k % 2 else -0.85)) * 50, y + math.sin(a + (0.85 if k % 2 else -0.85)) * 50)], 1.1, (0.1, 0.5)) for k, (x, y, a) in enumerate(along(st, 56))]
    art = G(art, strokes(W, H, veins) * lm, LEAF_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = pressed(art, strokes(W, H, stem_items(st, 4, 1.6)), "#7e6b40", "#5c4a28", nx(), density=0.85)
    tiny = circles(W, H, [(x + rng.gauss(0, 6), y - 14 + rng.gauss(0, 6), rng.uniform(4, 6)) for (x, y, a) in along(st[30:], 40)])
    art = pressed(art, tiny, "#efe4cc", "#ddd0b2", nx(), rim="#a98a5e", density=0.8)
    preview(art, "hk-twig", tone=SHEET)
    save(art, f"{OUT}/twig.webp", max_w=300, quality=82)

if "tape" in PARTS:
    art = tape(260, 74, 56, col="#dcc596", alpha=0.74)
    preview(art, "hk-tape", tone=SHEET)
    save(art, f"{OUT}/tape.webp", max_w=130, quality=84)
