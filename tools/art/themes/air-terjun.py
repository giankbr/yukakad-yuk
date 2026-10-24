"""Air Terjun — a tropical rainforest waterfall in watercolour: misty canopy, layered jungle ridges, basalt cliffs
with moss and hanging greens, a white column of falling water, a turquoise plunge pool with foam, mossy boulders,
ferns in the foreground and soft light shafts. The water column is a separate seamless tile so CSS can animate it.
Run: python3 -I air-terjun.py [part ...]  parts: scene falls fern frond stone
Assets -> public/themes/art/air-terjun/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t2_lib import *

OUT = outdir("air-terjun")
PARTS = sys.argv[1:] or ["scene", "falls", "fern", "frond", "stone"]
MIST = "#eaf2ea"
JG1, JG2, JG3 = "#8fb5a2", "#5f8f78", "#2f5f4a"
LEAF, LEAF_D, LEAF_L = "#4f8a3c", "#24502c", "#8fbf5a"
MOSS, MOSS_L = "#6f9a3c", "#a6c45e"
ROCK, ROCK_D, ROCK_L = "#4c5a54", "#2c3833", "#7d8a82"
POOL, POOL_D, POOL_L = "#2fb3a8", "#13716f", "#8fe0d4"


def frond_items(x, y, L, ang, curl=0.35, n=22, side_w=0.2, rng=None):
    """Fern frond: rachis curve + alternate pinnae as leaf polygons (returns stroke items, leaf polys)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = ang + curl * t * t
        if i == 0:
            px, py = x, y
        else:
            px, py = pts[-1][0] + math.cos(a) * L / n, pts[-1][1] + math.sin(a) * L / n
        pts.append((px, py))
    items = [(pts, max(1.5, L * 0.012), (0.0, 0.6))]
    leaves = []
    for i in range(2, n):
        t = i / n
        px, py = pts[i]
        a = math.atan2(pts[i + 1][1] - pts[i - 1][1], pts[i + 1][0] - pts[i - 1][0])
        size = L * side_w * math.sin(math.pi * (t * 0.86 + 0.1)) ** 0.8 * (1 - t * 0.45)
        for side in (-1, 1):
            pa = a + side * (0.95 - 0.25 * t) + (rng.uniform(-0.08, 0.08) if rng else 0)
            leaves.append(petal_pts(px, py, size, size * 0.24, pa, n=10))
    return items, leaves


def fern_cluster(art, W, H, bx, by, s, nx, rng, fronds, cols=(LEAF, LEAF_D, LEAF_L)):
    allm = np.zeros((H, W), np.float32)
    for k, (ang, L, curl) in enumerate(fronds):
        it, lv = frond_items(bx, by, L * s, ang, curl, rng=rng)
        m = np.clip(strokes(W, H, it) + shapes(W, H, lv), 0, 1)
        c0 = mix(cols[0], cols[2], rng.uniform(0, 0.4)) if k % 2 else cols[0]
        art = GP(art, m, c0, mix(c0, cols[2], 0.3), seed=nx(), rough=0.8, streak=0.5)
        art = tint(art, side_light(m, 2, 3, 2), cols[1], 0.6, seed=nx())
        np.maximum(allm, m, out=allm)
    return art, allm


def crown(art, W, H, cents, nx, rng, cols, dab=(6, 12), n=1.0, ldir=(-10, -10)):
    """Gouache tree crown: scalloped silhouette, shadow side, then light brush dabs on the lit side."""
    sub = []
    for x, y, r in cents:
        for _ in range(7):
            a_ = rng.uniform(0, math.tau); d_ = rng.uniform(0.25, 0.6) * r
            sub.append(deform(ellipse_pts(x + math.cos(a_) * d_, y + math.sin(a_) * d_ * 0.85, r * rng.uniform(0.38, 0.55), r * rng.uniform(0.34, 0.5), 12), rng, 1, 0.06))
    sil = shapes(W, H, sub)
    art = body(art, sil, cols[0], cols[1], cols[2], cols[3], nx, ldir=(-ldir[0], -ldir[1]), blur=12, rough=2.4)
    for tone, frac, k in ((mix(cols[0], cols[3], 0.45), 0.9, 1.0), (cols[3], 0.6, 0.6)):
        d = []
        for x, y, r in cents:
            for _ in range(int(r * k * n)):
                ang = rng.uniform(math.pi * 0.85, math.pi * 1.95); dd = rng.uniform(0.1, frac) * r
                d.append((x + math.cos(ang) * dd + ldir[0] * 0.3, y + math.sin(ang) * dd, rng.uniform(*dab) * 0.7, rng.uniform(*dab) * 0.3, rng.uniform(-70, 10)))
        dm = ellipses(W, H, d) * np.clip(gaussian_filter(sil, 1) * 1.2, 0, 1)
        art = GP(art, dm, tone, mix(tone, cols[0], 0.3), seed=nx(), rough=0.9, streak=0.6)
    return art, sil


def blade_leaf(art, W, H, pts, wd, nx, cols=("#4f8f3e", "#2f6a36", "#1b4424", "#8fc060")):
    import _jw_lib as jw
    m = shapes(W, H, [jw.blade(W, H, pts, wd)])
    art = body(art, m, cols[0], cols[1], cols[2], cols[3], nx, ldir=(0, 8), blur=6, rough=1.2)
    half = shapes(W, H, [jw.blade(W, H, pts, wd)[:len(pts)] + pts[::-1]]) * m
    art = tint(art, half, cols[2], 0.35, seed=nx())
    veins = [(pts[1:-2], 2.6, (0.05, 0.4))]
    for j in range(2, len(pts) - 2, 2):
        a_, b_ = pts[j - 1], pts[j + 1]
        ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0])
        for side in (-1, 1):
            aa = ang + side * 0.9
            veins.append(([pts[j], (pts[j][0] + math.cos(aa) * wd * .9, pts[j][1] + math.sin(aa) * wd * .9)], 1.2, (0.1, 0.6)))
    art = tint(art, strokes(W, H, veins) * m, cols[3], 0.5, seed=nx(), streak=0.2)
    return art


if "scene" in PARTS:
    W, H = 600, 1080
    nx = Seq(91000); rng = random.Random(11)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#f6f3df"), (0.14, "#e3eedc"), (0.3, "#bcd8c6"), (0.55, "#7fa892"), (1, "#2c5240")], seed=nx(), streak=0.7, grain=0.2)
    sun = gaussian_filter(circles(W, H, [(140, 60, 60)]), 36)
    art = over(art, col_arr(sun, "#fffbe6", np.clip(sun * 1.5, 0, 0.85)))
    # far ridges: scalloped jungle silhouettes, lighter with distance
    for y, amp, cols in ((200, 26, ("#b7d1c0", "#c6dccb", "#9fbfac", "#d6e6da")), (262, 32, ("#8fb5a0", "#9ec0ab", "#77a08a", "#b4d0be")), (330, 30, ("#66937b", "#72a087", "#4f7c66", "#8fbaa0"))):
        hm = hills(W, H, y, amp, nx(), 0.55)
        tops = circles(W, H, [(x, y - amp * 0.3 + rng.uniform(-12, 8), rng.uniform(14, 26)) for x in range(-10, W + 20, 22)])
        sil = np.clip(hm + tops, 0, 1)
        art = body(art, sil, cols[0], cols[1], cols[2], cols[3], nx, ldir=(8, 10), blur=10, rough=1.6)
        band = gaussian_filter(shapes(W, H, [[(-20, y + 34), (W + 20, y + 24), (W + 20, y + 70), (-20, y + 80)]]), 14)
        art = over(art, col_arr(band, MIST, band * 0.5))
        clear()
    # basalt massif with a crest notch
    lip = 360
    crest = [(80, 860), (86, 560), (110, 440), (146, 388), (196, 356), (240, 350), (264, lip), (338, lip), (362, 346), (410, 352), (456, 380), (494, 440), (516, 560), (520, 860)]
    mass = shapes(W, H, [deform(crest, rng, 2, 0.006)], smooth=True)
    art = body(art, mass, ROCK, "#55635b", ROCK_D, ROCK_L, nx, ldir=(14, 6), blur=26, rough=2.2)
    blocks = []
    for k in range(22):
        y0 = 380 + k * 22 + rng.uniform(-6, 6)
        x0 = rng.uniform(96, 220) if k % 2 else rng.uniform(370, 480)
        blocks.append((curve([(x0, y0), (x0 + rng.uniform(30, 60), y0 + rng.uniform(-4, 4)), (x0 + rng.uniform(70, 110), y0 + rng.uniform(-3, 6))], 12), rng.uniform(1.6, 3), (0.3, 0.3)))
        blocks.append((curve([(x0 + 30, y0), (x0 + 32 + rng.uniform(-5, 5), y0 + rng.uniform(16, 30))], 6), 1.8, (0.2, 0.4)))
    art = tint(art, strokes(W, H, blocks) * mass, ROCK_D, 0.7, seed=nx(), streak=0.3)
    hl = [(curve([(x0 := rng.uniform(100, 500), y0 := rng.uniform(380, 800)), (x0 + rng.uniform(20, 50), y0 - rng.uniform(0, 4))], 6), 2.2, (0.3, 0.3)) for _ in range(30)]
    art = tint(art, strokes(W, H, hl) * mass, ROCK_L, 0.45, seed=nx(), streak=0.3)
    stain = mass * np.clip(fbm(W, H, nx(), 50, 3) * 1.8 - 0.7, 0, 1)
    art = tint(art, stain, "#5f7a58", 0.45, seed=nx())
    drips = [(curve([(x0 := rng.uniform(100, 500), y0 := rng.uniform(370, 600)), (x0 + rng.uniform(-4, 4), y0 + rng.uniform(80, 200))], 8), rng.uniform(3, 8), (0.1, 0.6)) for _ in range(22)]
    art = tint(art, gaussian_filter(strokes(W, H, drips), 2) * mass, ROCK_D, 0.4, seed=nx())
    moss = []
    for _ in range(40):
        x0 = rng.uniform(96, 504); y0 = rng.uniform(370, 800)
        if 236 < x0 < 366:
            continue
        L = rng.uniform(20, 60)
        moss.append((curve([(x0, y0), (x0 + L * 0.5, y0 + rng.uniform(-4, 4)), (x0 + L, y0 + rng.uniform(-3, 5))], 10), rng.uniform(4, 9), (0.4, 0.4)))
    mm = strokes(W, H, moss) * mass
    art = GP(art, mm, MOSS, "#7fa848", seed=nx(), rough=2.2, streak=0.5)
    art = tint(art, side_light(mm, 0, -3, 2), MOSS_L, 0.6, seed=nx())
    clear()
    # water column (static base; CSS layers a moving shimmer tile on top)
    fall = shapes(W, H, [[(264, lip - 4), (338, lip - 4), (344, 560), (358, 806), (242, 806), (256, 560)]], smooth=False)
    art = body(art, np.clip(gaussian_filter(fall, 5) * 1.5, 0, 1) * mass, "#2a3632", "#323f3a", "#1c2622", "#3c4a44", nx, blur=4)
    art = GP(art, fall, "#d6ecea", "#c2e3de", seed=nx(), rough=1.2, streak=0.4, density=0.95)
    streak = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), (40, 1.3))
    streak = (streak - streak.min()) / (streak.max() - streak.min())
    art = over(art, col_arr(fall, "#ffffff", fall * np.clip((streak - 0.45) * 3.2, 0, 1)))
    art = over(art, col_arr(fall, "#86b6b0", fall * np.clip((0.42 - streak) * 2.2, 0, 1) * 0.6))
    # crest vegetation + hanging vines
    art, _ = crown(art, W, H, [(130, 400, 30), (168, 370, 26), (210, 356, 22), (392, 352, 22), (432, 362, 26), (476, 396, 30), (100, 480, 24), (500, 486, 24)], nx, rng, ("#3e7a3c", "#4a8844", "#24502c", "#8fc062"))
    vines = []
    for _ in range(14):
        x0 = rng.choice([rng.uniform(120, 236), rng.uniform(366, 486)]); y0 = rng.uniform(356, 400); L = rng.uniform(70, 210)
        vines.append((curve([(x0, y0), (x0 + rng.uniform(-6, 6), y0 + L * 0.5), (x0 + rng.uniform(-10, 10), y0 + L)], 16), rng.uniform(2, 3.2), (0.05, 0.6)))
    art = GP(art, strokes(W, H, vines), "#2f6a36", "#3f7a3c", seed=nx(), rough=0.8)
    clear()
    # jungle walls framing both sides
    for side in (-1, 1):
        cx_ = 0 if side < 0 else W
        edge_pts = [(cx_ - side * (120 + 40 * math.sin(k * 1.3) + rng.uniform(-10, 10)), 300 + k * 50) for k in range(14)]
        under = shapes(W, H, [[(cx_ + side * 30, 280)] + edge_pts + [(cx_ + side * 30, 1000)]])
        art = body(art, under, "#1f4a2c", "#24502c", "#11301b", "#2f6036", nx, ldir=(side * 10, 0), blur=16)
        cents = [(cx_ - side * rng.uniform(0, 110), 270 + k * 52 + rng.uniform(-14, 14), rng.uniform(48, 74)) for k in range(12)]
        art, _ = crown(art, W, H, cents, nx, rng, ("#2f6a36", "#3b7840", "#163a22", "#79b05a"), dab=(8, 16), ldir=(-10 * side, -10))
        clear()
    for pts_, wd in (([(-10, 640), (40, 606), (100, 594), (160, 612)], 30), ([(610, 580), (560, 556), (500, 560), (446, 586)], 30), ([(-10, 770), (60, 716), (120, 700)], 26), ([(610, 720), (550, 690), (494, 692)], 24)):
        art = blade_leaf(art, W, H, curve(pts_, 20), wd, nx)
    clear()
    # plunge pool
    pool = shapes(W, H, [deform(ellipse_pts(300, 866, 280, 74, 24), rng, 2, 0.02)])
    art = body(art, pool, POOL, "#38bcae", POOL_D, POOL_L, nx, ldir=(0, -12), blur=18, rough=1.6)
    deep = gaussian_filter(shapes(W, H, [ellipse_pts(300, 892, 180, 30, 20)]), 10) * pool
    art = tint(art, deep, POOL_D, 0.5, seed=nx())
    rip = []
    for k in range(18):
        rx = rng.uniform(30, 150)
        cx_ = 300 + rng.uniform(-110, 110); cy_ = 828 + k * 5.5
        a0 = rng.uniform(0.2, 1.5)
        rip.append((arc_pts(cx_, cy_ - rx * 0.18, rx, a0, a0 + rng.uniform(0.5, 1.1), 14, 0.2), rng.uniform(1.6, 2.6), (0.3, 0.3)))
    art = GP(art, strokes(W, H, rip) * pool, "#c6f0e8", seed=nx(), rough=0.6, density=0.85)
    spray = ellipses(W, H, [(300 + rng.gauss(0, 44), 806 + rng.gauss(0, 8) - abs(rng.gauss(0, 16)), rng.uniform(5, 14), rng.uniform(3, 8), rng.uniform(-30, 30)) for _ in range(70)])
    art = GP(art, spray, "#ffffff", "#e6f6f2", seed=nx(), rough=1.2, density=0.9)
    mistm = shapes(W, H, [ellipse_pts(300, 790, 220, 70, 20)])
    art = over(art, col_arr(gaussian_filter(mistm, 26), MIST, gaussian_filter(mistm, 26) * 0.6))
    clear()
    # mossy boulders
    for x, y, rx, ry in [(70, 840, 86, 46), (182, 940, 68, 28), (524, 832, 88, 46), (432, 950, 74, 28), (306, 962, 44, 16)]:
        bm = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 16), rng, 3, 0.05)])
        art = body(art, bm, ROCK, "#5a675f", ROCK_D, ROCK_L, nx, ldir=(10, 8), blur=10, rough=1.6)
        topm = bm * np.clip((y - yy) / (ry * 0.9), 0, 1) * np.clip(0.4 + 0.9 * fbm(W, H, nx(), 16, 2), 0, 1)
        art = GP(art, np.clip(topm * 1.4, 0, 1), MOSS, "#86ad4c", seed=nx(), rough=2.0, streak=0.5)
        art = tint(art, side_light(np.clip(topm * 1.4, 0, 1), -4, -4, 4), MOSS_L, 0.5, seed=nx())
    # foreground bank + big ferns
    bank = shapes(W, H, [[(-20, 990), (120, 966), (300, 992), (480, 968), (620, 980), (620, 1100), (-20, 1100)]])
    art = body(art, bank, "#24502c", "#2b5a32", "#122e1a", "#3b7040", nx, ldir=(0, 10), blur=10)
    clear()
    fc = ("#6fa84a", "#2f6a36", "#a9d070")
    art, _ = fern_cluster(art, W, H, 30, 1090, 1.15, nx, rng, [(-1.25, 300, 0.5), (-0.95, 290, 0.6), (-0.6, 250, 0.7), (-1.65, 250, -0.2), (-0.25, 210, 0.6)], cols=fc)
    clear()
    art, _ = fern_cluster(art, W, H, 580, 1090, 1.15, nx, rng, [(-1.9, 300, -0.5), (-2.2, 280, -0.6), (-2.55, 240, -0.6), (-1.5, 250, 0.2), (-2.9, 200, -0.5)], cols=fc)
    clear()
    rays = shapes(W, H, [[(40 + k * 80, -10), (80 + k * 80, -10), (300 + k * 100, 900), (240 + k * 100, 900)] for k in range(3)], smooth=False)
    rays = gaussian_filter(rays, 16) * np.clip(1 - yy / 950, 0, 1)
    art = over(art, col_arr(rays, "#fffbe0", rays * 0.18))
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/at-scene.png")
    save_rgb(art, f"{OUT}/scene.webp", quality=76)
    clear()

if "falls" in PARTS:
    # seamless vertical shimmer tile for the water column (alpha streaks, wraps in y)
    W, H = 96, 320
    nx = Seq(92000)
    n = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (34, 1.2), mode="wrap")
    n = (n - n.min()) / (n.max() - n.min())
    n2 = gaussian_filter(np.random.default_rng(4).random((H, W)).astype(np.float32), (10, 0.8), mode="wrap")
    n2 = (n2 - n2.min()) / (n2.max() - n2.min())
    a = np.clip((n - 0.5) * 2.6, 0, 1) * 0.75 + np.clip((n2 - 0.62) * 3, 0, 1) * 0.5
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    edge = np.clip(np.minimum(xx, W - 1 - xx) / 12, 0, 1)
    a = np.clip(a * edge, 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#ffffff"), np.float32)
    rgb = rgb * (1 - 0.15 * (1 - n2[..., None]))
    arr = np.concatenate([rgb, a[..., None]], -1)
    save_full(arr, f"{OUT}/falls.webp", quality=78)
    preview(arr, "at-falls", bg="#3a5a50")

if "fern" in PARTS:
    W, H = 420, 380
    nx = Seq(93000); rng = random.Random(21)
    art = blank(W, H)
    art, _ = fern_cluster(art, W, H, 60, 372, 1.0, nx, rng, [(-1.35, 330, 0.55), (-1.0, 300, 0.6), (-0.6, 270, 0.65), (-0.25, 230, 0.6), (-1.75, 250, -0.25), (0.05, 170, 0.5)])
    preview(art, "at-fern", tone="#f2f6ee")
    save(art, f"{OUT}/fern.webp", max_w=300, quality=82)
    clear()

if "frond" in PARTS:
    W, H = 440, 90
    nx = Seq(94000); rng = random.Random(4)
    art = blank(W, H)
    it, lv = frond_items(20, 48, 400, -0.04, 0.1, n=26, side_w=0.09, rng=rng)
    m = np.clip(strokes(W, H, it) + shapes(W, H, lv), 0, 1)
    art = G(art, m, LEAF, LEAF_D, seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=2, feather=0.7)
    drop = shapes(W, H, [[(410, 40), (418, 56), (412, 62), (404, 56)]])
    art = G(art, circles(W, H, [(412, 60, 6)]) + drop, POOL, POOL_D, seed=nx(), density=0.8, edge=0.5, bloom=0, rough=1)
    preview(art, "at-frond", tone="#f2f6ee")
    save(art, f"{OUT}/frond.webp", max_w=320, quality=84)
    clear()

if "stone" in PARTS:
    W, H = 110, 90
    nx = Seq(95000); rng = random.Random(7)
    art = blank(W, H)
    b = shapes(W, H, [deform(ellipse_pts(55, 52, 44, 30, 14), rng, 2, 0.04)])
    art = G(art, b, ROCK, ROCK_D, seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=3, gran=0.4)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = G(art, b * np.clip((50 - yy) / 26, 0, 1), MOSS, MOSS_L, seed=nx(), density=0.9, edge=0.4, bloom=0.3, rough=3)
    preview(art, "at-stone", tone="#f2f6ee")
    save(art, f"{OUT}/stone.webp", max_w=72, quality=84)
    clear()
