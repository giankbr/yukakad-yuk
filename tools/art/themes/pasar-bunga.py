"""Pasar Bunga — a flower-market stall: a big bouquet wrapped in kraft paper with a twine bow, a row of zinc buckets of
fresh flowers with blank chalkboard price tags, a striped scalloped awning tile, a small posy, a flowering sprig, and a
kraft paper tile. Watercolour flowers, gouache paper/zinc. Original art, no text.
Run: python3 -I pasar-bunga.py [part ...]   parts: bouquet buckets awning posy sprig kraft"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s6_lib import *
import _jw_lib as jw

OUT = outdir("pasar-bunga")
PARTS = sys.argv[1:] or ["bouquet", "buckets", "awning", "posy", "sprig", "kraft"]
KRAFT, KRAFT_D, KRAFT_L = "#c9a06c", "#9c7444", "#dcbb8c"
PINK, PINK_D, CORAL, CORAL_D = "#ef9fb2", "#c4566f", "#f2895e", "#c45a2f"
YEL, YEL_D, LILAC, LILAC_D = "#f5cf5a", "#d39a1c", "#b49ad8", "#7a5aa8"
SAGE, SAGE_D, EUC, EUC_D = "#86a77a", "#4f7448", "#9fb7a6", "#5f7f70"
ZINC, ZINC_D, ZINC_L = "#aab3b8", "#6f7a80", "#dfe4e6"
SLATE = "#2f3733"


def tulip(art, W, H, x, y, s, ang, rng, nx, col, deep):
    """Closed tulip cup: three overlapping petals pointing along ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    for k, off in enumerate([-0.32, 0.32, 0.0]):
        a = ang + off
        cx, cy = x + math.cos(a) * s * 0.1, y + math.sin(a) * s * 0.1
        m = shape_mask(W, H, deform(petal_pts(x - ca * s * .2, y - sa * s * .2, s * 1.25, s * 0.48, a, n=12), rng, 1, 0.05))
        art = G(art, m, col if k < 2 else mix(col, "#ffffff", .2), deep, seed=nx(), density=0.72, edge=0.6, bloom=0.35, rough=2.5, gran=0.2)
    return art


def daisy(art, W, H, x, y, r, rng, nx, col="#fffdf6", eye=YEL, eye_d=YEL_D, n=14, shadow="#c9c0b4"):
    polys = [petal_pts(x, y, r, r * 0.22, k * math.tau / n + rng.uniform(-.08, .08), n=8) for k in range(n)]
    m = shapes(W, H, polys)
    art = G(art, np.roll(np.roll(m, 2, 0), 1, 1), shadow, seed=nx(), density=0.35, edge=0.3, bloom=0, rough=1.5, feather=1.2, pad=8)
    art = GP(art, m, col, mix(col, "#e8e0d2", .5), seed=nx(), rough=0.9, streak=0.4, pad=8)
    art = G(art, np.clip((m - gaussian_filter(m, 1.1)) * 3, 0, 1), "#a99a8a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, feather=0.4, pad=6)
    art = GP(art, circles(W, H, [(x, y, r * 0.28)]), eye, eye_d, seed=nx(), rough=0.8, pad=6)
    art = G(art, circles(W, H, [(x + r * .06, y + r * .08, r * 0.2)]), eye_d, seed=nx(), density=0.4, edge=0.4, rough=0.8, pad=6)
    return art


def pompom(art, W, H, x, y, r, rng, nx, col, deep):
    """Chrysanthemum / ball dahlia: soft wash + many short petal strokes radiating."""
    art = G(art, circles(W, H, [(x, y, r)]), mix(col, "#ffffff", .25), col, seed=nx(), density=0.65, edge=0.4, bloom=0.4, rough=3)
    items = []
    for _ in range(int(r * 1.6)):
        a = rng.uniform(0, math.tau); d = r * math.sqrt(rng.random()) * 0.92
        px, py = x + math.cos(a) * d, y + math.sin(a) * d
        L = r * rng.uniform(0.16, 0.26)
        items.append(([(px - math.cos(a) * L * .3, py - math.sin(a) * L * .3), (px + math.cos(a) * L, py + math.sin(a) * L)], r * 0.09, (0.2, 0.6)))
    art = G(art, strokes(W, H, items), deep, seed=nx(), density=0.45, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)
    return art


def babys_breath(art, W, H, x, y, spread, rng, nx, n=40):
    stems = []
    tips = []
    for _ in range(9):
        a = rng.uniform(-math.pi, 0); L = spread * rng.uniform(.4, 1)
        tx, ty = x + math.cos(a) * L, y + math.sin(a) * L
        stems.append(([(x, y), (tx, ty)], 1.3, None))
        for _ in range(n // 9):
            tips.append((tx + rng.gauss(0, spread * .12), ty + rng.gauss(0, spread * .1), rng.uniform(2.2, 3.6)))
    art = G(art, strokes(W, H, stems), "#8aa078", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.4)
    m = circles(W, H, tips)
    art = GP(art, m, "#fffef8", "#f0ebe0", seed=nx(), rough=0.6, pad=6)
    art = G(art, np.clip((m - gaussian_filter(m, 1)) * 3, 0, 1), "#b8ae9f", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4, feather=0.3, pad=4)
    return art


def lavender_spike(art, W, H, x, y, L, ang, rng, nx, col=LILAC, deep=LILAC_D):
    pts = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [i / 12 for i in range(13)]]
    art = G(art, strokes(W, H, [(pts, 2.0, None)]), SAGE_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.4)
    buds = []
    for i, (px, py) in enumerate(pts[4:]):
        for side in (-1, 1):
            buds.append((px + side * 4 + rng.uniform(-1, 1), py + rng.uniform(-2, 2), 4.6 - i * 0.25, 3.4, math.degrees(ang) + side * 30))
    m = ellipses(W, H, buds)
    return G(art, m, col, deep, seed=nx(), density=0.75, edge=0.6, bloom=0.2, rough=1.4)


def euc_stem(art, W, H, pts, rng, nx, r=13):
    art = G(art, strokes(W, H, [(pts, 2.4, (0.05, 0.3))]), "#7d6a5a", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    discs = []
    for i in range(2, len(pts), 4):
        px, py = pts[i]
        for side in (-1, 1):
            discs.append((px + side * r * 0.75, py + rng.uniform(-3, 3), r * rng.uniform(.75, 1.05)))
    m = circles(W, H, discs)
    return G(art, m, EUC, EUC_D, seed=nx(), density=0.65, edge=0.55, bloom=0.4, rough=2.4, gran=0.3)


def bouquet():
    W, H = 640, 880
    rng = random.Random(7); nx = Seq(100)
    art = blank(W, H)
    cx = 318
    # greenery and stems poking out behind
    for (a, L) in [(-2.3, 300), (-1.9, 330), (-1.25, 320), (-0.85, 290), (-1.6, 350)]:
        p = curve([(cx, 470), (cx + math.cos(a) * L * .5, 470 + math.sin(a) * L * .5), (cx + math.cos(a + .15) * L, 470 + math.sin(a + .15) * L)], 30)
        art = euc_stem(art, W, H, p, rng, nx)
    for (a, L) in [(-2.05, 300), (-1.05, 320), (-1.45, 330)]:
        art = lavender_spike(art, W, H, cx + math.cos(a) * 140, 460 + math.sin(a) * 140, L * 0.55, a, rng, nx)
    for (x, y, L, a) in [(150, 330, 120, -2.6), (500, 320, 120, -0.4), (120, 420, 110, 2.9), (530, 420, 110, 0.2)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx, c=(SAGE, SAGE_D))
    clear()
    # flower heads
    flowers = blank(W, H)
    area = np.zeros((H, W), np.float32)
    jw.LEAF_A, jw.LEAF_B = SAGE, SAGE_D
    for (x, y, r, mid, deep) in [(232, 320, 90, "#e98aa0", "#a63b57"), (414, 300, 82, "#f4a58a", "#c55a3a"), (322, 432, 76, "#f2b6c2", "#b4506a")]:
        flowers = jw.rose(flowers, W, H, x, y, r, rng, nx, mix(mid, "#fff2ea", .35), mid, deep, area)
    clear()
    flowers = pompom(flowers, W, H, 128, 430, 62, rng, nx, YEL, YEL_D)
    flowers = pompom(flowers, W, H, 520, 418, 58, rng, nx, "#c9b2e6", LILAC_D)
    for (x, y, s, a) in [(322, 176, 36, -1.6), (220, 196, 32, -2.0), (432, 182, 34, -1.15), (122, 290, 32, -2.4), (536, 262, 32, -0.6), (276, 160, 28, -1.8), (378, 168, 28, -1.35), (80, 360, 28, -2.7), (575, 340, 28, -0.35)]:
        flowers = G(flowers, strokes(W, H, [([(x, y), (x - math.cos(a) * 60, y - math.sin(a) * 60)], 3.0, None)]), SAGE_D, seed=nx(), density=0.6, edge=0.1, rough=0.6, feather=0.4)
        flowers = tulip(flowers, W, H, x, y, s, a, rng, nx, CORAL if x % 2 else PINK, CORAL_D if x % 2 else PINK_D)
    clear()
    for (x, y, r) in [(160, 240, 30), (500, 214, 28), (424, 418, 30), (218, 440, 28), (330, 258, 26), (590, 470, 24), (60, 470, 24)]:
        flowers = daisy(flowers, W, H, x, y, r, rng, nx)
    art = glaze(knockout(art, area, 0.9, 4), flowers)
    art = babys_breath(art, W, H, 300, 230, 120, rng, nx, n=60)
    clear()
    # kraft cone: two overlapping sheets, folds, a crisp top edge
    back = [(110, 470), (cx - 6, 540), (530, 456), (cx + 34, 862), (cx - 22, 862)]
    front = [(96, 548), (226, 506), (cx + 8, 586), (420, 516), (546, 552), (cx + 26, 864), (cx - 26, 864)]
    bm = shape_mask(W, H, back, smooth=False)
    fm = shape_mask(W, H, deform(front, rng, 1, 0.01), smooth=False)
    art = OV(art, bm * (1 - fm), lambda m: gouache_paint(m, KRAFT_D, "#8a6538", seed=nx(), rough=1.5, streak=0.5), pad=12)
    art = OV(art, fm, lambda m: gouache_paint(m, KRAFT, KRAFT_L, seed=nx(), rough=1.5, streak=0.5), pad=12)
    folds = strokes(W, H, [([(226, 508), (cx + 4, 850)], 3.0, (0.1, 0.5)), ([(420, 518), (cx + 20, 850)], 3.0, (0.1, 0.5)), ([(150, 532), (cx - 16, 840)], 2.0, (0.2, 0.6))])
    art = G(art, folds * fm, KRAFT_D, seed=nx(), density=0.45, edge=0.3, bloom=0, rough=1.2, feather=1.2)
    # shade on the left of the cone, light on the right
    xx = np.arange(W, dtype=np.float32)[None, :]
    art = G(art, fm * np.clip((cx - 60 - xx) / 200, 0, 1), "#8a6538", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=4, feather=3)
    # paper fibre specks
    sp = (np.random.default_rng(3).random((H, W)) > 0.993).astype(np.float32) * fm
    art = G(art, gaussian_filter(sp, 0.6) * 3, "#7a5a32", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4, feather=0.3)
    # twine wraps + bow
    tw = []
    for k in range(3):
        y = 742 + k * 7
        tw.append(([(cx - 50 + k * 3, y), (cx, y + 5), (cx + 54 - k * 3, y - 2)], 2.6, None))
    tw += [(curve([(cx, 748), (cx - 50, 720), (cx - 64, 742), (cx, 752)], 20), 2.6, None),
           (curve([(cx, 748), (cx + 52, 722), (cx + 66, 744), (cx, 752)], 20), 2.6, None),
           (curve([(cx, 752), (cx - 20, 790), (cx - 34, 820)], 14), 2.4, (0, 0.5)),
           (curve([(cx, 752), (cx + 16, 794), (cx + 30, 826)], 14), 2.4, (0, 0.5))]
    art = OV(art, strokes(W, H, tw), lambda m: gouache_paint(m, "#d0485e", "#b23a50", seed=nx(), rough=0.6), pad=8)
    art = G(art, strokes(W, H, tw), "#7a2236", seed=nx(), density=0.25, edge=0.5, bloom=0, rough=0.5, feather=0.4)
    show(art, "pb-bouquet")
    save(art, f"{OUT}/bouquet.webp", max_w=560, quality=80)


def bucket(art, W, H, x, by, w, h, rng, nx):
    """Zinc bucket: tapered body, rolled rim, two ridges, cool sheen."""
    body = [(x - w / 2, by - h), (x + w / 2, by - h), (x + w * .42, by), (x - w * .42, by)]
    bm = shape_mask(W, H, body, smooth=False)
    bm = np.maximum(bm, ellipses(W, H, [(x, by, w * .42, 8, 0)]))
    art = OV(art, bm, lambda m: gouache_paint(m, ZINC, ZINC_L, seed=nx(), rough=1.2, streak=0.5), pad=10)
    xx = np.arange(W, dtype=np.float32)[None, :]
    rel = (xx - (x - w / 2)) / w
    art = G(art, bm * np.clip(1 - np.abs(rel - 0.3) * 6, 0, 1), "#ffffff", seed=nx(), density=0.0, edge=0, rough=1)
    art = OV(art, bm * np.clip(1 - np.abs(rel - 0.32) * 7, 0, 1) * 0.7, lambda m: gouache_paint(m, "#f4f7f8", seed=nx(), rough=1, streak=2), pad=6)
    art = G(art, bm * np.clip((rel - 0.62) * 2.6, 0, 1), ZINC_D, seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=2, feather=2)
    ridges = strokes(W, H, [([(x - w * .48, by - h * .62), (x + w * .48, by - h * .62)], 3.2, None), ([(x - w * .45, by - h * .3), (x + w * .45, by - h * .3)], 3.2, None)]) * bm
    art = G(art, ridges, ZINC_D, seed=nx(), density=0.55, edge=0.3, bloom=0, rough=1, feather=0.6)
    rim = ellipses(W, H, [(x, by - h, w / 2 + 4, 9, 0)])
    art = OV(art, rim, lambda m: gouache_paint(m, "#c4cbcf", "#e3e7e9", seed=nx(), rough=0.8), pad=8)
    art = G(art, np.clip(rim - ellipses(W, H, [(x, by - h + 2, w / 2 - 2, 6, 0)]), 0, 1), ZINC_D, seed=nx(), density=0.5, edge=0.3, rough=0.8, feather=0.5)
    # handle ears
    art = G(art, circles(W, H, [(x - w * .47, by - h * .82, 5), (x + w * .47, by - h * .82, 5)]), ZINC_D, seed=nx(), density=0.8, edge=0.4, rough=0.6)
    return art


def tag(art, W, H, x, y, rng, nx, rot=0.0):
    """Blank chalkboard tag on a stick with chalk scribble (no legible text)."""
    stick = strokes(W, H, [([(x, y + 20), (x - 6, y + 110)], 3.2, None)])
    art = OV(art, stick, lambda m: gouache_paint(m, "#b08a5c", "#8c6a42", seed=nx(), rough=0.6), pad=6)
    pts = [(-30, -20), (30, -20), (30, 20), (-30, 20)]
    ca, sa = math.cos(rot), math.sin(rot)
    poly = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    fr = shape_mask(W, H, poly, smooth=False)
    art = OV(art, fr, lambda m: gouache_paint(m, "#a07a4c", seed=nx(), rough=0.8), pad=6)
    inner = shape_mask(W, H, [(x + px * .82 * ca - py * .74 * sa, y + px * .82 * sa + py * .74 * ca) for px, py in pts], smooth=False)
    art = OV(art, inner, lambda m: gouache_paint(m, SLATE, "#3a433e", seed=nx(), rough=0.5, streak=0.8), pad=6)
    fx, fy = x - 12, y - 1
    sc = [([(fx, fy), (fx + math.cos(t) * 7, fy + math.sin(t) * 7)], 2.0, None) for t in [k * math.tau / 5 + .3 for k in range(5)]]
    sc += [(curve([(x + 2, y - 5), (x + 10, y - 7), (x + 19, y - 5)], 8), 2.0, None), (curve([(x + 2, y + 4), (x + 12, y + 3), (x + 18, y + 5)], 8), 2.0, None)]
    art = OV(art, strokes(W, H, sc) * inner, lambda m: gouache_paint(m, "#efece4", seed=nx(), rough=0.6, dry=0.5, density=0.8), pad=4)
    return art


def buckets():
    W, H = 820, 360
    rng = random.Random(12); nx = Seq(400)
    art = blank(W, H)
    specs = [(110, 340, 150, 120, "tulip_pink"), (300, 344, 160, 128, "sun"), (500, 340, 150, 120, "mix"), (700, 344, 160, 126, "lav")]
    flowers = blank(W, H)
    for (x, by, w, h, kind) in specs:
        top = by - h
        if kind == "tulip_pink":
            for k in range(14):
                fx = x + rng.uniform(-w * .45, w * .45); fy = top - rng.uniform(26, 120)
                flowers = G(flowers, strokes(W, H, [([(fx, fy), (x + (fx - x) * .3, top + 10)], 3.0, None)]), SAGE_D, seed=nx(), density=0.6, edge=0.1, rough=0.6, feather=0.4)
                flowers = tulip(flowers, W, H, fx, fy, rng.uniform(20, 26), -math.pi / 2 + (fx - x) / w * .8, rng, nx, PINK if k % 3 else CORAL, PINK_D if k % 3 else CORAL_D)
        elif kind == "sun":
            for k in range(8):
                fx = x + rng.uniform(-w * .4, w * .4); fy = top - rng.uniform(26, 120)
                flowers = jw.leaf(flowers, W, H, fx, fy + 30, 46, rng.choice([-2.6, -0.5]), rng, nx, c=(SAGE, SAGE_D))
                flowers = daisy(flowers, W, H, fx, fy, rng.uniform(22, 28), rng, nx, col=YEL, eye="#6b4a2a", eye_d="#3d2a18", n=16, shadow="#c7a24a")
        elif kind == "mix":
            for k in range(6):
                fx = x + rng.uniform(-w * .38, w * .38); fy = top - rng.uniform(24, 100)
                flowers = pompom(flowers, W, H, fx, fy, rng.uniform(30, 38), rng, nx, *rng.choice([("#f2b6c2", PINK_D), ("#fff3e6", "#d9b8a0"), ("#f6c38a", CORAL_D)]))
            flowers = babys_breath(flowers, W, H, x, top - 10, 90, rng, nx, n=36)
        else:
            for k in range(16):
                a = -math.pi / 2 + rng.uniform(-.45, .45)
                flowers = lavender_spike(flowers, W, H, x + rng.uniform(-w * .3, w * .3), top + 10, rng.uniform(110, 160), a, rng, nx)
            for k in range(5):
                flowers = euc_stem(flowers, W, H, curve([(x, top + 10), (x + rng.uniform(-60, 60), top - rng.uniform(60, 120))], 16), rng, nx, r=10)
        clear()
    art = glaze(art, flowers)
    for (x, by, w, h, kind) in specs:
        art = bucket(art, W, H, x, by, w, h, rng, nx)
        clear()
    art = tag(art, W, H, 196, 196, rng, nx, rot=-0.12)
    art = tag(art, W, H, 600, 206, rng, nx, rot=0.1)
    # soft ground shadow
    sh = ellipses(W, H, [(x, by + 4, w * .5, 8, 0) for (x, by, w, h, k) in specs])
    art = glaze(soft_sh(sh), art)
    show(art, "pb-buckets")
    save(art, f"{OUT}/buckets.webp", max_w=780, quality=80)


def soft_sh(m):
    return flat(gaussian_filter(m, 5), "#5b4a3a", 0.35)


def awning():
    W, H = 240, 84
    nx = Seq(600)
    art = blank(W, H)
    stripes = []
    cream = []
    for k in range(4):
        x0 = k * 60
        poly = [(x0, 0), (x0 + 30, 0), (x0 + 30, 52)] + [(x0 + 30 - 15 + 15 * math.cos(t / 10 * math.pi), 52 + 18 * math.sin(t / 10 * math.pi)) for t in range(11)][::-1][:0] + [(x0, 52)]
        stripes.append(rr(x0, 0, x0 + 30, 54))
        cream.append(rr(x0 + 30, 0, x0 + 60, 54))
    sc = circles(W, H, [(k * 30 + 15, 54, 15) for k in range(8)])
    g = shapes(W, H, stripes, smooth=False)
    c = shapes(W, H, cream, smooth=False)
    gm = np.clip(g + sc * np.repeat(np.repeat((np.arange(8) % 2 == 0).astype(np.float32), 30)[None, :W], H, 0), 0, 1)
    cm = np.clip(c + sc * np.repeat(np.repeat((np.arange(8) % 2 == 1).astype(np.float32), 30)[None, :W], H, 0), 0, 1)
    art = OV(art, gm, lambda m: gouache_paint(m, SAGE, "#7b9c70", seed=nx(), rough=0.6, streak=0.6), pad=0)
    art = OV(art, cm, lambda m: gouache_paint(m, "#f6eedd", "#ece2cc", seed=nx(), rough=0.6, streak=0.6), pad=0)
    # top fold shadow + scallop edge shading
    yy = np.arange(H, dtype=np.float32)[:, None]
    art[..., :3] *= (1 - 0.18 * np.clip((14 - yy) / 14, 0, 1))[..., None]
    edge = np.clip(np.maximum(gm, cm) - gaussian_filter(np.maximum(gm, cm), 2) * 1.0, 0, 1) * (yy > 46)
    art = G(art, edge * 2, "#5b6b52", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.6, pad=0)
    show(art, "pb-awning")
    save_full(art, f"{OUT}/awning.webp", quality=84)


def posy():
    W, H = 340, 300
    rng = random.Random(31); nx = Seq(800)
    art = blank(W, H)
    for (a, L) in [(-2.4, 130), (-0.7, 130)]:
        art = euc_stem(art, W, H, curve([(170, 190), (170 + math.cos(a) * L, 190 + math.sin(a) * L)], 14), rng, nx, r=10)
    for (x, y, L, a) in [(120, 200, 80, 2.6), (220, 200, 80, 0.5)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx, c=(SAGE, SAGE_D))
    fl = blank(W, H); area = np.zeros((H, W), np.float32)
    fl = jw.rose(fl, W, H, 150, 150, 50, rng, nx, "#fbd3d8", "#e98aa0", "#a63b57", area)
    art = glaze(knockout(art, area, 0.9, 4), fl)
    art = daisy(art, W, H, 222, 150, 26, rng, nx)
    art = tulip(art, W, H, 205, 96, 24, -1.3, rng, nx, CORAL, CORAL_D)
    art = babys_breath(art, W, H, 120, 120, 60, rng, nx, n=24)
    show(art, "pb-posy")
    save(art, f"{OUT}/posy.webp", max_w=220, quality=82)


def sprig():
    W, H = 560, 120
    rng = random.Random(41); nx = Seq(900)
    art = blank(W, H)
    st = curve([(20, 80), (200, 66), (360, 70), (540, 56)], 40)
    art = G(art, strokes(W, H, [(st, 2.6, (0.05, 0.2))]), SAGE_D, seed=nx(), density=0.65, edge=0.1, rough=0.6, feather=0.4)
    for i in range(4, 38, 5):
        x, y = st[i]
        art = jw.leaf(art, W, H, x, y, 38, -2.2 if i % 2 else 0.9, rng, nx, c=(SAGE, SAGE_D))
    art = daisy(art, W, H, 150, 62, 18, rng, nx)
    art = tulip(art, W, H, 290, 58, 16, -1.2, rng, nx, PINK, PINK_D)
    art = daisy(art, W, H, 420, 60, 16, rng, nx, col=YEL, eye="#6b4a2a", eye_d="#3d2a18", shadow="#c7a24a")
    art = tulip(art, W, H, 520, 46, 14, -0.5, rng, nx, CORAL, CORAL_D)
    show(art, "pb-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=82)


def kraft():
    W = H = 320
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#efe3cd"), np.float32)
    big = wrap_noise(W, H, 5, 28); fine = wrap_noise(W, H, 6, 0.7)
    fib = gaussian_filter(np.random.default_rng(7).random((H, W)).astype(np.float32), (0.5, 6), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    v = 1 + (big - .5) * 0.05 + (fine - .5) * 0.04 + fib * 0.008
    sp = gaussian_filter((np.random.default_rng(8).random((H, W)) > 0.995).astype(np.float32), 0.5, mode="wrap") * 2
    a = base * v[..., None] * (1 - sp[..., None] * 0.07)
    save_rgb(np.concatenate([np.clip(a, 0, 1), np.ones((H, W, 1), np.float32)], -1), f"{OUT}/kraft.webp", quality=70)


for p in PARTS:
    globals()[p]()
    clear()
