"""Provence Lavender — summer gouache landscape: warm painted sky, a dry-grass hill with an ochre stone farmhouse (mas),
terracotta roof and grey-blue shutters between flame cypresses and round olives, lavender rows in perspective leading
up to it; a tied lavender bunch and a small crossed-sprig divider.
Run: python3 -I provence-lavender.py [part ...]  parts: sky farm rows bunch sprig
Assets -> public/themes/art/provence-lavender/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m6_lib import *

OUT = outdir("provence-lavender")
PARTS = sys.argv[1:] or ["sky", "farm", "rows", "bunch", "sprig"]

LAV_L, LAV, LAV_D, LAV_DD = "#b3a2d8", "#8a73bf", "#62509a", "#46386f"
SAGE, SAGE_D, SAGE_L = "#8f9b63", "#5f6b3f", "#b7b97a"
STRAW, STRAW_D, STRAW_L = "#d8b878", "#b38f52", "#ead19a"
STONE, STONE_D, STONE_L = "#dcc196", "#b0916a", "#f0dcb6"
TILE, TILE_D = "#c7704a", "#9a4c31"
SHUT, SHUT_D = "#8aa3ad", "#5e7a86"
CYP, CYP_D = "#3f5232", "#263522"
SOIL, SOIL_D = "#b88c62", "#8d6744"


def cypress(art, W, H, x, by, h, rng, nx):
    w = h * 0.13
    pts = [(x, by - h)]
    n = 9
    for k in range(1, n + 1):
        t = k / n
        pts.append((x + w * math.sin(t * math.pi * 0.92) * (1 + rng.uniform(-.12, .12)), by - h + h * t))
    for k in range(n, 0, -1):
        t = k / n
        pts.append((x - w * math.sin(t * math.pi * 0.92) * (1 + rng.uniform(-.12, .12)), by - h + h * t))
    m = shape_mask(W, H, pts)
    art = GP(art, m, CYP, CYP_D, seed=nx(), rough=2.2, streak=1.2)
    # lit flank (sun from the left) + dabs
    lit = m * np.clip((x - np.arange(W)[None, :]) / (w * 0.9), 0, 1)
    art = GP(art, lit * 0.6, "#65794a", SAGE_D, seed=nx(), rough=1.5, streak=1.0)
    dabs = []
    for k in range(int(h / 6)):
        yy = by - h * rng.uniform(0.05, 0.95)
        dabs.append(([(x + rng.uniform(-w * .8, w * .2), yy), (x + rng.uniform(-w * .3, w * .5), yy - rng.uniform(4, 9))], rng.uniform(2, 3.5)))
    art = GP(art, strokes(W, H, dabs) * m * 0.7, CYP_D, seed=nx(), rough=1)
    return art


def olive(art, W, H, x, by, r, rng, nx):
    trunk = strokes(W, H, [(curve([(x, by), (x - 3, by - r * 0.5), (x + 2, by - r * 0.9)], 8), r * 0.16, (0, .3))])
    art = GP(art, trunk, "#6b5a45", seed=nx(), rough=1)
    blobs = [deform(ellipse_pts(x + rng.uniform(-r * .5, r * .5), by - r * 1.2 + rng.uniform(-r * .3, r * .3), r * rng.uniform(.5, .75), r * rng.uniform(.4, .55), 10), rng, 1, 0.12) for _ in range(5)]
    m = shapes(W, H, blobs)
    art = GP(art, m, "#7f8a5a", "#5d6942", seed=nx(), rough=2.4, streak=0.8)
    hi = shapes(W, H, [deform(ellipse_pts(x - r * .35, by - r * 1.45, r * .4, r * .25, 8), rng, 1, .15)]) * m
    art = GP(art, hi * 0.7, "#a3a873", seed=nx(), rough=1.5)
    return art


if "sky" in PARTS:
    W, H = 420, 820
    nx = Seq(100)
    sky = painted_sky(W, H, [(0, "#c9d8e4"), (0.35, "#e7e6dc"), (0.7, "#f6e6c8"), (1, "#f4dcb2")], seed=6, streak=0.5, grain=0.6)
    rng = random.Random(4)
    cl = []
    for cx, cy, s in [(70, 210, 0.9), (330, 140, 0.7), (300, 330, 0.5)]:
        for k in range(5):
            cl.append(deform(ellipse_pts(cx + (k - 2) * 24 * s, cy + rng.uniform(-6, 4) * s - (10 if k in (1, 2) else 0) * s, 32 * s, 12 * s, 10), rng, 1, 0.1))
    cm = gaussian_filter(shapes(W, H, cl), 3)
    sky = GP(sky, cm * 0.7, "#fbf6ec", "#f1ead9", seed=nx(), rough=3, streak=0.3, density=0.7)
    save_rgb(sky, f"{OUT}/sky.webp", quality=68)

if "farm" in PARTS:
    W, H = 840, 480
    rng = random.Random(21); nx = Seq(2100)
    art = blank(W, H)
    # far blue ridge + hill
    ridge = [(-10, H), (-10, 210)] + [(x, 205 - 30 * math.sin(x / 140) - 12 * math.sin(x / 47 + 1)) for x in range(0, W + 20, 20)] + [(W + 10, H)]
    art = GP(art, shape_mask(W, H, ridge), "#b7b8cf", "#a3a6c4", seed=nx(), rough=2, streak=0.6, density=0.9)
    hill = [(-10, H), (-10, 330)] + [(x, 300 - 120 * math.exp(-((x - 470) / 260) ** 2) + 8 * math.sin(x / 33)) for x in range(0, W + 20, 20)] + [(W + 10, H)]
    hm = shape_mask(W, H, hill)
    art = GP(art, hm, STRAW, SAGE_L, seed=nx(), rough=2.2, streak=1.2)
    shade = hm * np.clip((np.arange(W)[None, :] - 520) / 300, 0, 1) * np.clip((np.arange(H)[:, None] - 200) / 200, 0, 1)
    art = GP(art, shade * 0.55, STRAW_D, SAGE, seed=nx(), rough=2)
    # dry-grass strokes
    gs = []
    for k in range(260):
        x = rng.uniform(0, W); y = rng.uniform(260, H)
        if hm[min(H - 1, int(y)), min(W - 1, int(x))] < 0.5:
            continue
        L = 3 + (y - 200) / 40
        gs.append(([(x, y), (x + rng.uniform(-L, L) * 0.6, y - L)], 1.4))
    art = GP(art, strokes(W, H, gs) * 0.55, STRAW_L, seed=nx(), rough=0.8)
    # olives on the hill
    for x, by, r in [(150, 312, 26), (215, 300, 20), (700, 300, 24), (760, 318, 28)]:
        art = olive(art, W, H, x, by, r, rng, nx)
    clear()
    # farmhouse (mas): main block + lower wing, terracotta roofs, light from the left
    bx, by = 430, 272
    main = shapes(W, H, [[(bx - 70, by), (bx + 70, by), (bx + 70, by - 92), (bx - 70, by - 92)]], smooth=False)
    wing = shapes(W, H, [[(bx + 70, by), (bx + 150, by), (bx + 150, by - 52), (bx + 70, by - 52)]], smooth=False)
    art = GP(art, main, STONE_L, STONE, seed=nx(), rough=1.0, streak=1.1)
    art = GP(art, wing, STONE, STONE_D, seed=nx(), rough=1.0, streak=1.1)
    # stone texture
    st = []
    for k in range(70):
        x = rng.uniform(bx - 66, bx + 146); y = rng.uniform(by - 88, by - 4)
        if x > bx + 70 and y < by - 50:
            continue
        st.append(([(x, y), (x + rng.uniform(5, 10), y + rng.uniform(-1, 1))], rng.uniform(2.2, 3.5)))
    art = GP(art, strokes(W, H, st) * 0.45, STONE_D, seed=nx(), rough=0.8)
    roof = shapes(W, H, [[(bx - 80, by - 90), (bx + 78, by - 90), (bx + 50, by - 122), (bx - 54, by - 122)]], smooth=False)
    roof2 = shapes(W, H, [[(bx + 66, by - 50), (bx + 158, by - 50), (bx + 140, by - 70), (bx + 66, by - 72)]], smooth=False)
    art = GP(art, roof, TILE, TILE_D, seed=nx(), rough=1.0, streak=1.3)
    art = GP(art, roof2, TILE_D, TILE, seed=nx(), rough=1.0, streak=1.3)
    tiles = strokes(W, H, [([(bx - 76 + k * 9, by - 91), (bx - 52 + k * 7.4, by - 121)], 1.2, None) for k in range(15)])
    art = GP(art, tiles * roof * 0.5, "#8a3e27", seed=nx(), rough=0.5)
    eave = strokes(W, H, [([(bx - 80, by - 89), (bx + 78, by - 89)], 3, None)])
    art = GP(art, eave, "#7c4a33", seed=nx(), rough=0.5)
    # windows with shutters, door
    for wx, wy in [(bx - 44, by - 74), (bx - 8, by - 74), (bx + 28, by - 74), (bx - 44, by - 36), (bx + 28, by - 36), (bx + 100, by - 38)]:
        g = shapes(W, H, [rect(wx, wy, wx + 12, wy + 18)], smooth=False)
        art = GP(art, g, "#3d3b44", seed=nx(), rough=0.5)
        for sx in (wx - 7, wx + 12):
            sh = shapes(W, H, [rect(sx, wy - 1, sx + 7, wy + 19)], smooth=False)
            art = GP(art, sh, SHUT, SHUT_D, seed=nx(), rough=0.5, streak=0.8)
    door = shapes(W, H, [[(bx - 10, by), (bx + 8, by), (bx + 8, by - 26), (bx - 1, by - 32), (bx - 10, by - 26)]], smooth=False)
    art = GP(art, door, SHUT_D, seed=nx(), rough=0.5)
    sideshade = shapes(W, H, [rect(bx + 40, by - 90, bx + 70, by)], smooth=False) * main
    art = G(art, sideshade, "#b49a8a", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
    # chimney
    ch = shapes(W, H, [rect(bx + 26, by - 136, bx + 38, by - 112)], smooth=False)
    art = GP(art, ch, STONE_D, seed=nx(), rough=0.6)
    # climbing rose/vine by the door + shrub
    vb = []
    for k in range(24):
        vb.append(ellipse_pts(bx - 26 + rng.uniform(-6, 6), by - rng.uniform(0, 40), rng.uniform(3, 6), rng.uniform(2, 4), 7))
    art = GP(art, shapes(W, H, vb), "#6f7d48", "#56633a", seed=nx(), rough=1)
    art = GP(art, circles(W, H, [(bx - 26 + rng.uniform(-6, 6), by - rng.uniform(4, 38), 2.2) for _ in range(10)]), "#d98aa0", seed=nx(), rough=0.4)
    clear()
    # cypresses flanking
    for x, h_ in [(320, 190), (342, 150), (606, 176), (628, 128), (660, 102)]:
        art = cypress(art, W, H, x, 282 + (x - 470) * 0.05, h_, rng, nx)
    # path from the house down the hill
    path = shapes(W, H, [[(bx - 4, by + 2), (bx + 12, by + 2), (bx + 60, H + 4), (bx - 40, H + 4)]], smooth=False)
    art = GP(art, path * 0.85, "#e7cfa0", STONE, seed=nx(), rough=2, streak=0.8)
    yy_ = np.arange(H, dtype=np.float32)[:, None]
    art[..., 3] *= np.clip((H - yy_) / 110, 0, 1) ** 0.8
    pv(art, "pl-farm", "#efe3cc")
    save(art, f"{OUT}/farm.webp", max_w=780, quality=78)
    clear()

if "rows" in PARTS:
    W, H = 780, 720
    rng = random.Random(31); nx = Seq(3100)
    vx, vy = 400, -46
    pitch = 170
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rb = vx + (xx - vx) * (H - vy) / (yy - vy)          # bottom-x of the ray through each pixel
    u = ((rb - (vx - pitch / 2)) % pitch) / pitch        # 0..1 across one row pitch
    idx = np.floor((rb - (vx - pitch / 2)) / pitch)
    band = np.clip((0.5 - np.abs(u - 0.5)) / 0.06 - 0.6, 0, 1) * (idx != 0)   # lavender mounds; centre gap = path
    band = gaussian_filter(band, 0.8)
    art = blank(W, H)
    ground = np.ones((H, W), np.float32)
    art = GP(art, ground, SAGE, SOIL, seed=nx(), rough=2, streak=1.0)
    art = GP(art, band, LAV_D, LAV, seed=nx(), rough=3, streak=1)
    # mound shading: lit left flank, shadowed right flank (sun from the left)
    lit = band * np.clip((0.42 - u) / 0.25, 0, 1)
    shd = band * np.clip((u - 0.55) / 0.25, 0, 1)
    art = G(art, lit * 0.8, LAV_L, seed=nx(), density=0.6, edge=0, bloom=0.2, rough=1.5)
    art = G(art, shd * 0.8, LAV_DD, seed=nx(), density=0.55, edge=0, bloom=0.2, rough=1.5)
    # aerial haze toward the horizon
    fade = np.clip(1 - yy / (H * 0.55), 0, 1) ** 1.6
    art = G(art, fade * 0.9, "#d2c6df", "#e3d6c4", seed=nx(), density=0.6, edge=0, bloom=0, rough=1, mottle=0.3)
    # lavender spikes on the near rows, size grows with depth
    def sample(n, umin=0.18, umax=0.82):
        out = []
        while len(out) < n:
            y = H * (rng.random() ** 0.55)
            if y < 60:
                continue
            k = rng.randint(-3, 3)
            if k == 0:
                continue
            uu = rng.uniform(umin, umax)
            xb = vx - pitch / 2 + (k + uu) * pitch
            x = vx + (xb - vx) * (y - vy) / (H - vy)
            if -10 < x < W + 10:
                out.append((x, y, y / H))
        return out
    for colset, cnt, ur in [((LAV_DD, LAV_D), 1300, (0.5, 0.86)), ((LAV, LAV_D), 1300, (0.15, 0.85)), ((LAV_L, LAV), 1000, (0.14, 0.5))]:
        items = []
        for x, y, t in sample(cnt, *ur):
            L = 2 + 34 * t ** 1.5
            items.append(([(x, y), (x + rng.uniform(-.25, .25) * L, y - L)], 0.8 + 3.6 * t, (0.0, 0.5)))
        art = GP(art, strokes(W, H, items), *colset, seed=nx(), rough=0.9, streak=0.6)
        clear()
    tips = []
    for x, y, t in sample(800, 0.14, 0.45):
        L = 2 + 16 * t ** 1.5
        tips.append(([(x, y - L * 1.2), (x, y - L * 2.1)], 0.7 + 2.6 * t, (0.0, 0.6)))
    art = GP(art, strokes(W, H, tips) * 0.85, "#d8ccf0", seed=nx(), rough=0.6)
    # gravel path in the centre gap
    pa = np.clip((0.5 - np.abs(u - 0.5)) / 0.04 - 0.2, 0, 1)
    pa = (1 - pa) * (idx == 0) * np.clip((yy - 20) / 40, 0, 1)
    pa = np.clip(gaussian_filter((idx == 0).astype(np.float32) * (np.abs(u - 0.5) < 0.36), 1.2), 0, 1)
    art = GP(art, pa, "#e6d1a8", "#cfb185", seed=nx(), rough=2.6, streak=0.8)
    peb = [(rng.uniform(0, W), H * rng.random() ** 0.5) for _ in range(600)]
    art = GP(art, circles(W, H, [(x, y, 0.4 + 2.6 * y / H) for x, y in peb]) * pa * 0.6, "#b39470", seed=nx(), rough=0.4)
    art[..., 3] *= np.clip(yy / 40, 0, 1)
    pv(art, "pl-rows")
    save(art, f"{OUT}/rows.webp", max_w=780, quality=72)
    clear()

if "bunch" in PARTS:
    W, H = 320, 560
    rng = random.Random(41); nx = Seq(4100)
    art = blank(W, H)
    stems, heads = [], []
    for k in range(13):
        a = -math.pi / 2 + (k - 6) * 0.07 + rng.uniform(-.03, .03)
        L = rng.uniform(380, 470)
        x0, y0 = 160 + (k - 6) * 1.6, 520
        x1, y1 = x0 + math.cos(a) * L, y0 + math.sin(a) * L
        stems.append(([(x0, y0), ((x0 + x1) / 2 + rng.uniform(-4, 4), (y0 + y1) / 2), (x1, y1)], 3.0, (0, 0.2)))
        heads.append((x1, y1, a, L))
    art = G(art, strokes(W, H, [(curve(p, 12), w_, t_) for p, w_, t_ in stems]), SAGE, SAGE_D, seed=nx(), density=0.75, edge=0.5, bloom=0.1, rough=1.2, feather=0.8)
    for colset, kk in [((LAV, LAV_D), 0), ((LAV_L, LAV), 1)]:
        dots = []
        for (x1, y1, a, L) in heads:
            for j in range(22):
                t = j / 22
                d = t * 150
                px = x1 - math.cos(a) * d + rng.uniform(-5, 5) * (1 - t * .5)
                py = y1 - math.sin(a) * d
                r = (6.2 - t * 2.4) * rng.uniform(.8, 1.1)
                if (j + kk) % 2 == 0:
                    dots.append((px, py, r))
        art = G(art, ellipses(W, H, [(x, y, r * 0.75, r, rng.uniform(-20, 20)) for x, y, r in dots]), *colset, seed=nx(), density=0.75, edge=0.8, bloom=0.25, rough=1.2, feather=0.8, gran=0.35)
        clear()
    # linen ribbon bow
    rb = [[(140, 398), (180, 398), (184, 420), (136, 420)]]
    art = GP(art, shapes(W, H, rb, smooth=False), "#9fb2c4", "#7f97ad", seed=nx(), rough=1)
    loops = [deform(petal_pts(160, 408, 56, 24, a, n=14), rng, 1, 0.06) for a in (math.pi * 0.95, 0.05)]
    tails = [deform(petal_pts(160, 412, 82, 14, a, n=12), rng, 1, 0.06) for a in (math.pi * 0.62, math.pi * 0.4)]
    art = GP(art, shapes(W, H, loops + tails), "#a8bacb", "#7f97ad", seed=nx(), rough=1.2, streak=0.8)
    art = G(art, shapes(W, H, [deform(petal_pts(160, 408, 40, 10, a, n=12), rng, 1, .05) for a in (math.pi * 0.95, 0.05)]), "#5f7891", seed=nx(), density=0.4, edge=0.5, bloom=0, rough=1)
    art = GP(art, circles(W, H, [(160, 409, 10)]), "#6f879d", seed=nx(), rough=0.8)
    pv(art, "pl-bunch")
    save(art, f"{OUT}/bunch.webp", max_w=240, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 520, 150
    rng = random.Random(51); nx = Seq(5100)
    art = blank(W, H)
    st, dots = [], []
    for side in (-1, 1):
        for k in range(3):
            a = math.radians(8 + k * 9)
            x0, y0 = 260, 120
            L = 230 - k * 34
            x1, y1 = x0 + side * math.cos(a) * L, y0 - math.sin(a) * L
            st.append(([(x0, y0), (x1, y1)], 2.2, (0, 0.2)))
            for j in range(24):
                t = j / 24
                px = x1 + (x0 - x1) * t * 0.5; py = y1 + (y0 - y1) * t * 0.5
                if j % 2 == 0:
                    dots.append((px + rng.uniform(-2, 2), py - 3, 6.0 - t * 2.4))
                else:
                    dots.append((px + rng.uniform(-2, 2), py + 3, 6.0 - t * 2.4))
    art = G(art, strokes(W, H, st), SAGE, SAGE_D, seed=nx(), density=0.75, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    art = G(art, ellipses(W, H, [(x, y, r * 1.0, r * 0.7, rng.uniform(-15, 15)) for x, y, r in dots]), LAV, LAV_D, seed=nx(), density=0.75, edge=0.8, bloom=0.2, rough=1, feather=0.7, gran=0.3)
    art = G(art, circles(W, H, [(260, 120, 8)]), "#7f97ad", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.6)
    pv(art, "pl-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=320, quality=82)

kb(OUT)
