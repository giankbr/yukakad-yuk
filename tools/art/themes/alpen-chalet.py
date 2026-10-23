"""Alpen Chalet — bright gouache Alpine scene: painted sky, snowy peaks, wooden chalet with geranium flower boxes on a
meadow hill, foreground wildflowers; green shutter, flower box, wildflower garland and gentian bloom ornaments.
Run: python3 -I alpen-chalet.py [part ...]  parts: sky peaks chalet flowers shutter box garland bloom
Assets -> public/themes/art/alpen-chalet/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l5_lib import *

OUT = outdir("alpen-chalet")
PARTS = sys.argv[1:] or ["sky", "peaks", "chalet", "flowers", "shutter", "box", "garland", "bloom"]

WOOD, WOOD_D, WOOD_L = "#8a5230", "#5a321c", "#b47546"
ROOF, ROOF_D = "#5b4638", "#3a2c24"
PLASTER, PLASTER_D = "#f4efe3", "#cfc6b4"
SHUTTER, SHUTTER_D = "#3f7a4f", "#27543a"
GERAN, GERAN_D, GERAN_L = "#d6362c", "#9e1f1d", "#f06a52"
MEADOW, MEADOW_D, MEADOW_L = "#76a94a", "#4b7a34", "#a9cc66"
PINE, PINE_D = "#2f5a3c", "#1d3c29"
ROCK, ROCK_D, ROCK_L = "#7f8fa6", "#56647c", "#aab8c9"
SNOW, SNOW_S = "#fbfcfd", "#cfdbe8"


def geranium_cluster(art, W, H, x, y, r, rng, nx, n=7):
    """ball of small red petals + a few leaves"""
    lv = []
    for k in range(3):
        a = rng.uniform(math.pi * 0.1, math.pi * 0.9)
        lv.append(deform(ellipse_pts(x + math.cos(a) * r * 1.1, y + r * 0.6 + math.sin(a) * r * 0.4, r * 0.7, r * 0.5, 10), rng, 1, 0.08))
    art = GP(art, shapes(W, H, lv), MEADOW_D, PINE, seed=nx(), rough=1.2, streak=0.8)
    dots = []
    for k in range(n):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, r * 0.7)
        dots.append((x + math.cos(a) * d, y + math.sin(a) * d * 0.8, r * rng.uniform(0.32, 0.45)))
    art = GP(art, circles(W, H, dots), GERAN, GERAN_D, seed=nx(), rough=1.4, streak=0.6)
    hi = circles(W, H, [(dx - rr * 0.3, dy - rr * 0.3, rr * 0.4) for dx, dy, rr in dots[: n // 2]])
    art = GP(art, hi * 0.8, GERAN_L, seed=nx(), rough=0.8)
    return art


def flower_box(art, W, H, x0, x1, y, rng, nx, h=26):
    """wooden box with geraniums and trailing leaves"""
    box = shapes(W, H, [[(x0, y), (x1, y), (x1 - 4, y + h), (x0 + 4, y + h)]], smooth=False)
    for k in range(int((x1 - x0) / 18)):
        geranium_cluster_x = x0 + 10 + k * 18 + rng.uniform(-4, 4)
        art = geranium_cluster(art, W, H, geranium_cluster_x, y - 8 + rng.uniform(-4, 3), rng.uniform(9, 12), rng, nx, n=6)
    trail = []
    for k in range(int((x1 - x0) / 30)):
        tx = x0 + 12 + k * 30 + rng.uniform(-6, 6)
        trail.append((curve([(tx, y + h * 0.4), (tx + rng.uniform(-6, 6), y + h + 10), (tx + rng.uniform(-8, 8), y + h + rng.uniform(16, 30))], 10), 4.5, (0.0, 0.5)))
    art = GP(art, strokes(W, H, trail), MEADOW_D, seed=nx(), rough=1.0)
    art = GP(art, box, WOOD, WOOD_D, seed=nx(), rough=0.9, streak=1.2)
    plank = strokes(W, H, [([(x0 + 3, y + h * 0.5), (x1 - 3, y + h * 0.5)], 1.4, None)])
    art = G(art, plank, WOOD_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5)
    return art


def window(art, W, H, x, y, w, h, rng, nx, shutters=True):
    glass = shapes(W, H, [[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], smooth=False)
    art = GP(art, glass, "#2c4057", "#40607e", seed=nx(), rough=0.7, streak=0.4)
    refl = strokes(W, H, [([(x + w * 0.2, y + h * 0.75), (x + w * 0.55, y + h * 0.2)], w * 0.12, None)])
    art = G(art, refl, "#9cc0dc", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.5)
    frame = strokes(W, H, [([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], 4, None),
                           ([(x + w / 2, y), (x + w / 2, y + h)], 3, None), ([(x, y + h * 0.45), (x + w, y + h * 0.45)], 3, None)])
    art = GP(art, frame, PLASTER, seed=nx(), rough=0.6)
    if shutters:
        sw = w * 0.52
        for sx in (x - sw - 3, x + w + 3):
            sh = shapes(W, H, [[(sx, y - 2), (sx + sw, y - 2), (sx + sw, y + h + 2), (sx, y + h + 2)]], smooth=False)
            art = GP(art, sh, SHUTTER, SHUTTER_D, seed=nx(), rough=0.8, streak=1.0)
            slats = strokes(W, H, [([(sx + 2, yy), (sx + sw - 2, yy)], 1.2, None) for yy in np.arange(y + 4, y + h, 5.5)])
            art = G(art, slats, SHUTTER_D, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.4)
    return art


def pine(art, W, H, x, by, h, rng, nx, col=PINE, col2=PINE_D):
    tiers = []
    n = 6
    for k in range(n):
        t = k / n
        yy = by - h * (0.12 + t * 0.85)
        ww = h * 0.34 * (1 - t * 0.85)
        tiers.append(deform([(x - ww, yy + h * 0.16), (x, yy - h * 0.1), (x + ww, yy + h * 0.16), (x, yy + h * 0.1)], rng, 1, 0.06))
    trunk = shapes(W, H, [[(x - h * 0.03, by), (x + h * 0.03, by), (x + h * 0.02, by - h * 0.2), (x - h * 0.02, by - h * 0.2)]], smooth=False)
    art = GP(art, trunk, WOOD_D, seed=nx(), rough=0.6)
    m = shapes(W, H, tiers)
    art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=1.0)
    lit = m * np.clip(gaussian_filter(np.roll(m, 5, 1), 3) - gaussian_filter(m, 3) + 0.0, 0, 1)
    sideL = shapes(W, H, [[(x - h * 0.36, by), (x, by - h * 1.0), (x - h * 0.02, by)]], smooth=False) * m
    art = G(art, sideL, MEADOW, seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2)
    return art


def daisy(W, H, x, y, r, rng, items_w, items_c):
    for k in range(9):
        a = k / 9 * math.tau + rng.uniform(-.1, .1)
        items_w.append(petal_pts(x, y, r, r * 0.34, a, n=10))
    items_c.append((x, y, r * 0.3))


if "sky" in PARTS:
    W, H = 420, 760
    nx = Seq(100)
    sky = painted_sky(W, H, [(0, "#79b2da"), (0.45, "#b9d9ee"), (0.8, "#e6f1f4"), (1, "#f3f6ee")], seed=4, streak=0.35, grain=0.6)
    rng = random.Random(5)
    cl = []
    for cx, cy, s in [(80, 170, 1.0), (330, 110, 0.8), (260, 300, 0.6)]:
        for k in range(6):
            cl.append(deform(ellipse_pts(cx + (k - 2.5) * 22 * s, cy + rng.uniform(-8, 4) * s - (12 if 1 < k < 4 else 0) * s, 30 * s, 16 * s, 10), rng, 1, 0.1))
    cm = gaussian_filter(shapes(W, H, cl), 2.5)
    sky = GP(sky, cm * 0.85, "#ffffff", "#e9f2f8", seed=nx(), rough=3.5, streak=0.3, density=0.75)
    save_rgb(sky, f"{OUT}/sky.webp", quality=70)

if "peaks" in PARTS:
    W, H = 840, 470
    rng = random.Random(21); nx = Seq(2100)
    art = blank(W, H)

    def ridge(x0, y0, x1, y1, n, amp):
        pts = [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
        return [(x + (rng.uniform(-amp, amp) if 0 < i < n else 0), y + (rng.uniform(-amp, amp) if 0 < i < n else 0)) for i, (x, y) in enumerate(pts)]

    # far range: soft blue, rolling
    far = [(0, 330)] + [(x, 320 - 70 * abs(math.sin(x / 150 + 0.4)) - rng.uniform(0, 26)) for x in range(0, 841, 30)] + [(840, 470), (0, 470)]
    art = GP(art, shapes(W, H, [far]), "#b9cbe0", "#cbd9e8", seed=nx(), rough=3.0, streak=0.6)
    peaks = [(230, 78, 290), (540, 34, 320), (790, 140, 200)]
    for px, py, bw in peaks:
        lft = ridge(px - bw, 470, px, py, 9, 14)
        rgt = ridge(px, py, px + bw, 470, 9, 14)
        L = lft + rgt[1:]
        m = shapes(W, H, [L], smooth=False)
        art = GP(art, m, ROCK_L, "#9cadc2", seed=nx(), rough=2.2, streak=0.25)
        # shadow side: right of a wandering crease from the apex
        crease = ridge(px, py, px + bw * 0.12, 470, 8, 12)
        sh = shapes(W, H, [crease + rgt[::-1][:-1]], smooth=False) * m
        art = GP(art, sh, ROCK, ROCK_D, seed=nx(), rough=2.0, streak=0.25, density=0.92)
        art = dabs(art, W, H, m, "#8d9db4", rng, nx, n=40, size=(16, 34), width=(3, 6), ang=1.2, density=0.35, medium="w")
        # snow cap above a wobbly snowline
        sy = py + (470 - py) * 0.34
        line = [(px - bw * 0.7, sy + 40)] + [(px - bw * 0.6 + k * bw * 0.12, sy + (rng.uniform(12, 46) if k % 2 else rng.uniform(-14, 4)) + abs(k - 5) * 4) for k in range(11)] + [(px + bw * 0.7, sy + 40)]
        cap = shapes(W, H, [line + [(px + bw * 0.7, py - 20), (px - bw * 0.7, py - 20)]]) * m
        cap = np.clip(cap - 0, 0, 1)
        art = GP(art, cap, SNOW, "#f3f6fa", seed=nx(), rough=2.6, streak=0.2)
        art = G(art, cap * sh, "#9fb2cf", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=2)
        # snow streaks down gullies + dark rock ribs
        st = []
        for _ in range(5):
            sx = px + rng.uniform(-bw * 0.4, bw * 0.4)
            y0 = sy + rng.uniform(5, 30)
            st.append((curve([(sx, y0), (sx + (sx - px) * 0.25, y0 + rng.uniform(30, 70))], 10), rng.uniform(7, 12), (0.0, 0.9)))
        art = GP(art, strokes(W, H, st) * m, SNOW, "#e2eaf3", seed=nx(), rough=1.4, density=0.85)
        clear()
    # soft valley mist (low, uneven)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    mist = np.clip((yy - 0.78) / 0.22, 0, 1) * (0.55 + 0.45 * fbm(W, H, 77, 90, 3)) * art[..., 3]
    art = OV(art, mist * 0.7, lambda mm: solid_layer(mm, "#dfeaf0"))
    preview(art, "alpen-peaks", tone="#cfe3f0")
    save(art, f"{OUT}/peaks.webp", max_w=780)
if "chalet" in PARTS:
    W, H = 840, 660
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    # distant forested slopes behind the meadow
    fz = [(0, 262)]
    for x in range(0, 841, 9):
        fz.append((x, 268 + 22 * math.sin(x / 120) + (-(rng.uniform(8, 20)) if (x // 9) % 2 else 0)))
    fz += [(840, 470), (0, 470)]
    fm = shapes(W, H, [fz], smooth=False)
    art = GP(art, fm, "#4f7a63", "#3f6a58", seed=nx(), rough=1.6, streak=0.3)
    art = G(art, fm * np.clip(1 - np.linspace(0, 1, H, dtype=np.float32)[:, None] * 2.2 + 0.4, 0, 1), "#a9c3cf", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=3)
    # meadow hill
    hill = [(0, 380)] + [(x, 420 - 70 * math.sin((x + 80) / 840 * math.pi) + rng.uniform(-4, 4)) for x in range(0, 841, 60)] + [(840, 400), (840, 660), (0, 660)]
    hm = shapes(W, H, [hill])
    art = GP(art, hm, MEADOW, MEADOW_D, seed=nx(), rough=2.5, streak=1.4)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = G(art, hm * np.clip((yy - 0.6) * 2, 0, 1), MEADOW_D, seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=4)
    sun = shapes(W, H, [[(0, 360), (360, 330), (300, 470), (0, 520)]]) * hm
    art = G(art, gaussian_filter(sun, 20), MEADOW_L, seed=nx(), density=0.6, edge=0.05, bloom=0.3, rough=3)
    art = dabs(art, W, H, hm, MEADOW_L, rng, nx, n=160, size=(10, 22), width=(3, 6), ang=-0.1, density=0.5)
    art = dabs(art, W, H, hm * (yy > 0.75), MEADOW_D, rng, nx, n=120, size=(10, 22), width=(3, 6), ang=0.1, density=0.5)
    # meadow strokes
    gs = []
    for _ in range(260):
        x = rng.uniform(0, W); y = rng.uniform(380, H)
        if hm[int(min(H - 1, y)), int(min(W - 1, x))] < 0.5: continue
        gs.append(([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(6, 14))], 1.6, (0.0, 0.6)))
    art = G(art, strokes(W, H, gs), MEADOW_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5)
    clear()
    # pines left and right
    for x, by, h in [(120, 400, 210), (190, 410, 170), (70, 420, 150), (760, 400, 190), (700, 418, 140)]:
        art = pine(art, W, H, x, by, h, rng, nx)
    clear()
    cx, gy = 440, 470
    # shadow on grass
    art = G(art, shapes(W, H, [deform(ellipse_pts(cx + 30, gy + 8, 230, 22, 14), rng, 1, 0.04)]), MEADOW_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=3, feather=4)
    # plaster base
    base = shapes(W, H, [[(cx - 180, gy), (cx + 180, gy), (cx + 180, gy - 90), (cx - 180, gy - 90)]], smooth=False)
    art = GP(art, base, PLASTER, PLASTER_D, seed=nx(), rough=1.0, streak=0.8)
    stones = circles(W, H, [(cx - 180 + rng.uniform(0, 360), gy - rng.uniform(4, 86), rng.uniform(3, 6)) for _ in range(34)])
    art = G(art, stones * base, "#b9ae9a", seed=nx(), density=0.4, edge=0.4, bloom=0, rough=1)
    # wooden upper storey
    up = shapes(W, H, [[(cx - 172, gy - 90), (cx + 172, gy - 90), (cx + 172, gy - 230), (cx, gy - 330), (cx - 172, gy - 230)]], smooth=False)
    art = GP(art, up, WOOD, WOOD_L, seed=nx(), rough=1.0, streak=1.6)
    logs = strokes(W, H, [([(cx - 172, y), (cx + 172, y)], 1.6, None) for y in range(gy - 220, gy - 92, 12)])
    art = G(art, logs * up, WOOD_D, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6)
    shade = shapes(W, H, [[(cx + 40, gy - 90), (cx + 172, gy - 90), (cx + 172, gy - 230), (cx + 40, gy - 300)]], smooth=False) * up
    art = G(art, shade, WOOD_D, seed=nx(), density=0.28, edge=0.1, bloom=0.2, rough=2)
    # gable vertical boards
    gable = strokes(W, H, [([(x, gy - 232), (x, gy - 330 + abs(x - cx) * 0.58 + 6)], 1.4, None) for x in range(cx - 150, cx + 151, 14)])
    art = G(art, gable * up, WOOD_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5)
    # roof with deep eaves
    roof = shapes(W, H, [[(cx - 235, gy - 205), (cx, gy - 352), (cx + 235, gy - 205), (cx + 222, gy - 190), (cx, gy - 328), (cx - 222, gy - 190)]], smooth=False)
    art = GP(art, roof, ROOF, ROOF_D, seed=nx(), rough=1.0, streak=1.2)
    art = dabs(art, W, H, roof, "#776052", rng, nx, n=90, size=(8, 16), width=(2, 3.5), ang=0.0, density=0.6)
    art = dabs(art, W, H, up, WOOD_L, rng, nx, n=70, size=(14, 30), width=(2, 4), ang=0.0, density=0.45)
    chim = shapes(W, H, [[(cx + 92, gy - 296), (cx + 118, gy - 296), (cx + 118, gy - 254), (cx + 92, gy - 240)]], smooth=False)
    art = GP(art, chim, PLASTER, PLASTER_D, seed=nx(), rough=0.8)
    art = GP(art, strokes(W, H, [([(cx + 88, gy - 298), (cx + 122, gy - 298)], 6, None)]), ROOF_D, seed=nx(), rough=0.5)
    ridge_hi = strokes(W, H, [([(cx - 228, gy - 200), (cx, gy - 346)], 3, None)])
    art = GP(art, ridge_hi * 0.8, "#8a7260", seed=nx(), rough=0.6)
    # eave shadow under roof
    es = shapes(W, H, [[(cx - 172, gy - 230), (cx, gy - 330), (cx + 172, gy - 230), (cx + 172, gy - 214), (cx, gy - 310), (cx - 172, gy - 214)]], smooth=False)
    art = G(art, es, ROOF_D, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=1.2)
    # gable window
    art = window(art, W, H, cx - 18, gy - 278, 36, 40, rng, nx, shutters=False)
    # balcony: railing with heart-cut boards
    by0, by1 = gy - 136, gy - 96
    rail = shapes(W, H, [[(cx - 196, by1), (cx + 196, by1), (cx + 196, by0), (cx - 196, by0)]], smooth=False)
    art = window(art, W, H, cx - 110, gy - 212, 50, 60, rng, nx)
    art = window(art, W, H, cx + 60, gy - 212, 50, 60, rng, nx)
    art = flower_box(art, W, H, cx - 122, cx - 48, gy - 150, rng, nx, h=10)
    art = flower_box(art, W, H, cx + 48, cx + 122, gy - 150, rng, nx, h=10)
    art = GP(art, rail, WOOD_L, WOOD, seed=nx(), rough=0.8, streak=1.2)
    boards = strokes(W, H, [([(x, by0 + 2), (x, by1 - 2)], 1.4, None) for x in range(cx - 190, cx + 191, 13)])
    art = G(art, boards, WOOD_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.4)
    hearts = []
    for x in range(cx - 184, cx + 185, 26):
        hy = (by0 + by1) / 2
        hearts.append([(x, hy + 5), (x - 5, hy - 1), (x - 3, hy - 5), (x, hy - 3), (x + 3, hy - 5), (x + 5, hy - 1)])
    art = GP(art, shapes(W, H, hearts), "#3b2414", seed=nx(), rough=0.4)
    art = GP(art, strokes(W, H, [([(cx - 200, by0), (cx + 200, by0)], 5, None), ([(cx - 200, by1), (cx + 200, by1)], 5, None)]), WOOD_D, seed=nx(), rough=0.6)
    art = flower_box(art, W, H, cx - 190, cx + 190, by0 - 4, rng, nx, h=10)
    clear()
    # ground floor windows + door
    art = window(art, W, H, cx - 130, gy - 74, 46, 44, rng, nx)
    art = window(art, W, H, cx + 84, gy - 74, 46, 44, rng, nx)
    art = flower_box(art, W, H, cx - 156, cx - 58, gy - 28, rng, nx, h=16)
    art = flower_box(art, W, H, cx + 58, cx + 156, gy - 28, rng, nx, h=16)
    door = shapes(W, H, [[(cx - 26, gy), (cx + 26, gy), (cx + 26, gy - 70), (cx, gy - 80), (cx - 26, gy - 70)]], smooth=False)
    art = GP(art, door, WOOD_D, "#6b3c20", seed=nx(), rough=0.7, streak=1.2)
    art = GP(art, strokes(W, H, [([(cx, gy - 76), (cx, gy - 2)], 1.4, None)]), "#2e1a0e", seed=nx(), rough=0.4)
    # path
    path = shapes(W, H, [[(cx - 24, gy + 2), (cx + 24, gy + 2), (cx + 70, H), (cx - 40, H)]])
    art = GP(art, path, "#d9c9a3", "#c6b48a", seed=nx(), rough=2.2, streak=0.8)
    clear()
    preview(art, "alpen-chalet", tone="#cfe3f0")
    save(art, f"{OUT}/chalet.webp", max_w=780)

if "flowers" in PARTS:
    W, H = 840, 300
    rng = random.Random(41); nx = Seq(4100)
    art = blank(W, H)
    ground = shapes(W, H, [[(0, 120)] + [(x, 110 + 30 * math.sin(x / 90) + rng.uniform(-6, 6)) for x in range(0, 841, 40)] + [(840, 300), (0, 300)]])
    art = GP(art, ground, MEADOW, MEADOW_D, seed=nx(), rough=2.0, streak=1.2)
    gr = []
    for _ in range(420):
        x = rng.uniform(0, W); y = rng.uniform(120, H)
        L = rng.uniform(18, 46)
        gr.append((curve([(x, y), (x + rng.uniform(-6, 6), y - L * 0.6), (x + rng.uniform(-12, 12), y - L)], 6), rng.uniform(2.0, 3.2), (0.0, 0.7)))
    g = strokes(W, H, gr)
    art = GP(art, g, MEADOW_D, PINE, seed=nx(), rough=0.6, streak=0.6)
    gl = strokes(W, H, gr[::3])
    art = GP(art, gl, MEADOW_L, MEADOW, seed=nx(), rough=0.6, streak=0.6)
    clear()
    stems = []
    blooms = []
    for _ in range(80):
        x = rng.uniform(10, W - 10); y = rng.uniform(80, 250)
        stems.append((curve([(x, y + 70), (x + rng.uniform(-6, 6), y + 30), (x, y)], 8), 2.0, (0.0, 0.3)))
        blooms.append((x, y, rng.choice(["daisy", "daisy", "gentian", "butter", "clover", "daisy"]), (8 + (y - 80) / 170 * 12) * rng.uniform(.85, 1.15)))
    art = GP(art, strokes(W, H, stems), MEADOW_D, seed=nx(), rough=0.5)
    dw, dc, gen, but, clo = [], [], [], [], []
    for x, y, kind, r in blooms:
        if kind == "daisy":
            daisy(W, H, x, y, r, rng, dw, dc)
        elif kind == "gentian":
            gen.append([(x - r * 0.7, y - r), (x, y - r * 0.6), (x + r * 0.7, y - r), (x + r * 0.45, y + r * 0.5), (x - r * 0.45, y + r * 0.5)])
        elif kind == "butter":
            for k in range(5):
                but.append(petal_pts(x, y, r * 0.8, r * 0.55, k / 5 * math.tau, n=10))
        else:
            clo.append(deform(ellipse_pts(x, y, r * 0.6, r * 0.85, 10), rng, 1, 0.1))
    art = GP(art, shapes(W, H, dw), "#ffffff", "#eef0f4", seed=nx(), rough=0.7)
    art = GP(art, circles(W, H, dc), "#f2b630", "#d88f1c", seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, gen, smooth=False), "#2f5fc4", "#1f3f94", seed=nx(), rough=0.9, streak=1.0)
    art = GP(art, shapes(W, H, but), "#f5cc2e", "#e8a91c", seed=nx(), rough=0.7)
    art = GP(art, shapes(W, H, clo), "#e07aa4", "#b84f7f", seed=nx(), rough=1.0)
    clear()
    preview(art, "alpen-flowers", tone="#cfe3f0")
    save(art, f"{OUT}/flowers.webp", max_w=780)

if "shutter" in PARTS:
    W, H = 160, 380
    rng = random.Random(51); nx = Seq(5100)
    art = blank(W, H)
    sh = shapes(W, H, [[(14, 12), (146, 12), (146, 368), (14, 368)]], smooth=False)
    art = GP(art, sh, SHUTTER, SHUTTER_D, seed=nx(), rough=1.0, streak=1.4)
    frame = strokes(W, H, [([(14, 12), (146, 12), (146, 368), (14, 368), (14, 12)], 12, None), ([(14, 190), (146, 190)], 12, None)])
    art = GP(art, frame, "#4b8a5b", SHUTTER, seed=nx(), rough=0.8, streak=1.2)
    slats = strokes(W, H, [([(24, y), (136, y)], 3.2, None) for y in list(range(30, 182, 10)) + list(range(206, 362, 10))])
    art = G(art, slats, "#1c3d29", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5)
    hx, hy = 80, 104
    heart = shapes(W, H, [[(hx, hy + 22), (hx - 22, hy - 2), (hx - 14, hy - 18), (hx, hy - 10), (hx + 14, hy - 18), (hx + 22, hy - 2)]])
    art = GP(art, heart, "#f6efe1", seed=nx(), rough=0.8)
    hinge = strokes(W, H, [([(6, 50), (40, 50)], 5, None), ([(6, 330), (40, 330)], 5, None)])
    art = GP(art, hinge, "#2a2a2a", seed=nx(), rough=0.5)
    preview(art, "alpen-shutter", tone="#f6efe1")
    save(art, f"{OUT}/shutter.webp", max_w=110)

if "box" in PARTS:
    W, H = 600, 170
    rng = random.Random(61); nx = Seq(6100)
    art = blank(W, H)
    art = flower_box(art, W, H, 20, 580, 74, rng, nx, h=46)
    # bigger cluster blooms on top
    for x in range(50, 560, 48):
        art = geranium_cluster(art, W, H, x + rng.uniform(-8, 8), 52 + rng.uniform(-10, 6), rng.uniform(18, 24), rng, nx, n=8)
    clear()
    preview(art, "alpen-box", tone="#f6efe1")
    save(art, f"{OUT}/box.webp", max_w=400)

if "garland" in PARTS:
    W, H = 600, 130
    rng = random.Random(71); nx = Seq(7100)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(20, 70), (160, 60), (300, 72), (440, 58), (580, 68)], 60), 3, (0.05, 0.05))])
    art = GP(art, stem, MEADOW_D, seed=nx(), rough=0.5)
    lv = []
    for k, (x, y) in enumerate(curve([(20, 70), (160, 60), (300, 72), (440, 58), (580, 68)], 26)):
        if k % 2 == 0 and 3 < k < 23:
            continue
        a = -math.pi / 2 + (0.8 if k % 2 else -0.8) + rng.uniform(-.3, .3)
        lv.append(petal_pts(x, y, rng.uniform(22, 32), 9, a, n=10))
    art = GP(art, shapes(W, H, lv), MEADOW, MEADOW_D, seed=nx(), rough=0.8)
    dw, dc = [], []
    for x in (90, 380, 520):
        daisy(W, H, x, 64 + rng.uniform(-6, 6), 25, rng, dw, dc)
    art = GP(art, shapes(W, H, dw), "#ffffff", "#e9edf2", seed=nx(), rough=0.7)
    art = GP(art, circles(W, H, dc), "#f2b630", "#d88f1c", seed=nx(), rough=0.6)
    gen = [[(x - 17, 42), (x, 52), (x + 17, 42), (x + 11, 82), (x - 11, 82)] for x in (200, 455)]
    art = GP(art, shapes(W, H, gen, smooth=False), "#2f5fc4", "#1f3f94", seed=nx(), rough=0.8)
    art = geranium_cluster(art, W, H, 300, 62, 26, rng, nx, n=10)
    preview(art, "alpen-garland", tone="#fbf7ee")
    save(art, f"{OUT}/garland.webp", max_w=320)

if "bloom" in PARTS:
    W, H = 160, 160
    rng = random.Random(81); nx = Seq(8100)
    art = blank(W, H)
    dw, dc = [], []
    for k in range(12):
        a = k / 12 * math.tau
        dw.append(petal_pts(80, 80, 62, 20, a, n=10))
    art = GP(art, shapes(W, H, dw), "#ffffff", "#e8ecf1", seed=nx(), rough=1.0, streak=0.8)
    art = G(art, shapes(W, H, [petal_pts(80, 80, 60, 10, k / 12 * math.tau + 0.1, n=8) for k in range(12)]), "#c9d3de", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1)
    art = GP(art, circles(W, H, [(80, 80, 18)]), "#f2b630", "#d88f1c", seed=nx(), rough=0.8)
    art = G(art, circles(W, H, [(86, 86, 10)]), "#b5701a", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1)
    preview(art, "alpen-bloom", tone="#fbf7ee")
    save(art, f"{OUT}/bloom.webp", max_w=80)

kb_total(OUT)
