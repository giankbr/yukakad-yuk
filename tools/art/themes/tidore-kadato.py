"""Tidore Kadato — dawn over Tidore: watercolour cone of Kie Matubu rising from a teal sea, the white Kadato Kie
(sultan's palace) with its stepped roofs and grand stair in gouache, clove branches with crimson buds, a split nutmeg
with scarlet mace. Run: python3 -I tidore-kadato.py [part ...]   parts: scene clove nutmeg divider
Assets -> public/themes/art/tidore-kadato/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i1_lib import *

OUT = outdir("tidore-kadato")
PARTS = sys.argv[1:] or ["scene", "clove", "nutmeg", "divider"]
CREAM = "#f6ead8"
CLOVE, CLOVE_D = "#7a2f26", "#4a1a14"
MACE = "#c8362b"
SEA, SEA_D = "#3d8487", "#24585c"
LEAF, LEAF_D, LEAF_L = "#4f6b3a", "#2e4426", "#7d9156"


def clove_cluster(art, W, H, x, y, s, a0, spread, n, rng, nx):
    """A cyme of clove buds: pink-red stalks radiating from a twig tip, each ending in a 4-sepal cup + round bud."""
    stalks, cups, balls = [], [], []
    for k in range(n):
        a = a0 + (k / max(1, n - 1) - 0.5) * spread + rng.uniform(-0.12, 0.12)
        L = s * rng.uniform(0.75, 1.1)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        mid = (x + math.cos(a) * L * 0.5 + rng.uniform(-2, 2), y + math.sin(a) * L * 0.5)
        stalks.append((curve([(x, y), mid, (ex, ey)], 10), s * 0.17, (0.35, 0.0)))
        cx_, cy_ = ex + math.cos(a) * s * 0.12, ey + math.sin(a) * s * 0.12
        for j in (-1, 1):
            cups.append(petal_pts(ex, ey, s * 0.32, s * 0.14, a + j * 0.5, n=8))
        balls.append((cx_ + math.cos(a) * s * 0.06, cy_ + math.sin(a) * s * 0.06, s * 0.15))
    sm = strokes(W, H, stalks)
    art = G(art, sm, "#c4554a", "#8f2f2a", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1.2, feather=0.6, pad=8)
    cm = shapes(W, H, cups)
    art = G(art, cm, MACE, CLOVE, seed=nx(), density=0.9, edge=0.6, bloom=0, rough=1.0, feather=0.5, pad=8)
    bm = circles(W, H, balls)
    art = GP(art, bm, "#e0a07a", "#c46a4c", seed=nx(), rough=0.6, streak=0.3, pad=6)
    hi = circles(W, H, [(bx - r * 0.3, by - r * 0.3, r * 0.35) for bx, by, r in balls])
    art = OV(art, hi * 0.5, lambda m: tint(m, "#f7dcc6", 0.7), pad=4)
    return art


def clove_leaf(art, W, H, x, y, L, ang, rng, nx, young=False):
    pts = deform(petal_pts(x, y, L, L * 0.2, ang, n=14, cup=0.05), rng, 1, 0.05)
    m = shape_mask(W, H, pts)
    if young:
        art = G(art, m, "#b8613f", "#8a3a28", seed=nx(), density=0.7, edge=0.55, bloom=0.3, rough=2, pad=10)
    else:
        art = G(art, m, LEAF_L, LEAF, seed=nx(), density=0.85, edge=0.7, bloom=0.3, rough=2.5, pad=10)
        # glossy half: darker on one side of the midrib
        half = shape_mask(W, H, [(x, y)] + [p for p in pts[: len(pts) // 2]])
        art = G(art, half * m, LEAF_D, seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=1.5, pad=10)
    vein = strokes(W, H, [(curve([(x, y), (x + math.cos(ang) * L * 0.95, y + math.sin(ang) * L * 0.95)], 10), 1.4, (0.0, 0.6))])
    art = G(art, vein, "#d9d3a0" if not young else "#e8b48e", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    return art


def palm2(art, W, H, x, by, h, lean, rng, nx):
    """Coconut palm: ringed, tapered trunk and ten drooping fronds of dense leaflets (watercolour + dry strokes)."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.25, by - h * 0.5), top], 40)
    tm = strokes(W, H, [(trunk, h * 0.045, (0.0, 0.0))])
    art = G(art, tm, "#8a7656", "#5e4c34", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1, feather=0.6)
    rings = strokes(W, H, [([(px_ - h * 0.025, py_), (px_ + h * 0.025, py_ + 1)], 1.2, None) for px_, py_ in trunk[2::3]]) * tm
    art = G(art, rings, "#3e3122", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.4)
    leaflets, spines = [], []
    for k in range(10):
        a = -math.pi / 2 + (k - 4.5) * 0.36 + rng.uniform(-0.08, 0.08)
        L = h * rng.uniform(0.34, 0.46)
        droop = L * (0.25 + 0.5 * abs(math.cos(a)))
        pts = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - h * 0.03), (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + droop)], 30)
        spines.append((pts, h * 0.008, (0.0, 0.6)))
        for j in range(2, 29):
            px_, py_ = pts[j]; qx, qy = pts[j + 1]
            ang = math.atan2(qy - py_, qx - px_)
            ll = L * 0.2 * (1 - j / 34)
            for sgn in (-1, 1):
                qa = ang + sgn * 0.9 + 0.35
                leaflets.append(([(px_, py_), (px_ + math.cos(qa) * ll, py_ + math.sin(qa) * ll + ll * 0.35)], h * 0.011, (0.05, 0.7)))
    lm = strokes(W, H, leaflets + spines)
    art = G(art, lm, "#5d7a3c", "#2f4524", seed=nx(), density=0.9, edge=0.55, bloom=0.2, rough=1.0, feather=0.5)
    art = G(art, circles(W, H, [(top[0] + dx, top[1] + 6 + dy, h * 0.022) for dx, dy in [(-5, 0), (4, 2), (0, 6)]]), "#7b6a2e", "#4f4420", seed=nx(), density=0.9, edge=0.4, rough=0.6)
    return art


if "scene" in PARTS:
    W, H = 780, 720
    nx = Seq(30100); rng = random.Random(31)
    HZ = int(H * 0.60)  # horizon (sea level)
    sky = painted_sky(W, H, [(0, "#f6ead8"), (0.30, "#f6e1c6"), (0.50, "#f2c79f"), (0.60, "#eeb48d"), (1, "#eeb48d")], seed=3, streak=0.8)
    art = fade_alpha(sky, 0, H * 0.26)
    # low sun right of the cone + warm glow
    sun = circles(W, H, [(W * 0.84, H * 0.25, 26)])
    art = over(art, glow(sun, "#fff0d2", radius=40, strength=0.9))
    art = GP(art, sun, "#fff7e8", "#fde6c2", seed=nx(), rough=1.0, streak=0.2)
    art = G(art, edge_of(sun, 3), "#e9a77c", seed=nx(), density=0.4, edge=0.3, bloom=0, rough=1)
    # soft cloud streaks
    clouds = strokes(W, H, [(curve([(x0, y0), (x0 + L * 0.5, y0 - 4), (x0 + L, y0 + 2)], 20), w, (0.3, 0.3)) for x0, y0, L, w in
                            [(30, 170, 260, 14), (470, 140, 240, 10), (540, 230, 220, 12), (90, 250, 160, 8)]])
    art = G(art, clouds, "#fbf2e4", "#f4dcc2", seed=nx(), density=0.6, edge=0.2, bloom=0.4, rough=6, feather=3)
    clear()
    # Kie Matubu: a near-perfect cone with slightly concave flanks, its foot at the horizon
    px, py = W * 0.40, H * 0.10
    L, R = [], []
    for i in range(41):
        t = i / 40
        hw = (W * 0.62) * (t ** 1.35) + 10 * t
        yy = py + (HZ + 6 - py) * t
        L.append((px - hw * 0.98 + rng.uniform(-1.5, 1.5), yy)); R.append((px + hw * 1.02 + rng.uniform(-1.5, 1.5), yy))
    cone_pts = [(px - 7, py - 2), (px + 6, py - 1)] + R[1:] + L[::-1][:-1]
    cone = polys(W, H, [cone_pts])
    art = G(art, cone, "#8aa0a4", "#6f8a93", seed=nx(), density=0.78, edge=0.5, bloom=0.4, rough=4)
    # forested lower slopes (deeper, greener) + shadowed right flank
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    lower = cone * np.clip((yy - H * 0.30) / (H * 0.2), 0, 1)
    art = G(art, lower, "#5d7d6c", "#3e5f55", seed=nx(), density=0.6, edge=0.25, bloom=0.5, rough=6)
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    shade = cone * np.clip((xx - px - (yy - py) * 0.15) / 120, 0, 1)
    art = G(art, shade, "#4d6472", seed=nx(), density=0.38, edge=0.15, bloom=0.3, rough=4)
    # ravines radiating from the summit: dark creases with a lit ridge beside each, fading downhill
    rav, ridge = [], []
    for k in range(11):
        f = (k / 10 - 0.5) * 1.7 + rng.uniform(-0.05, 0.05)
        x1 = px + f * W * 0.5 + rng.uniform(-14, 14)
        y1 = HZ - rng.uniform(60, 170)
        mx_, my_ = (px + x1) / 2 + rng.uniform(-10, 10), (py + y1) / 2 + rng.uniform(0, 24)
        pts = curve([(px + f * 8, py + 18 + rng.uniform(0, 16)), (mx_, my_), (x1, y1)], 30)
        rav.append((pts, rng.uniform(3.0, 5.5), (0.15, 0.6)))
        ridge.append(([(x + 5, y) for x, y in pts], rng.uniform(2.0, 3.5), (0.2, 0.6)))
    fade = np.clip(1.15 - (yy - py) / (HZ - py), 0, 1)
    art = G(art, strokes(W, H, rav) * cone * fade, "#3f5560", seed=nx(), density=0.38, edge=0.35, bloom=0.1, rough=2.5, feather=1.2)
    art = G(art, strokes(W, H, ridge) * cone * fade * (xx < px + 30), "#b7c0bb", seed=nx(), density=0.28, edge=0.2, bloom=0, rough=2, feather=1.2)
    # forest texture: small dabs on the lower slopes
    dab = []
    for _ in range(1100):
        y = rng.uniform(H * 0.34, HZ)
        t = (y - py) / (HZ - py)
        hw = (W * 0.62) * (t ** 1.35)
        x = rng.uniform(px - hw, px + hw)
        dab.append((x, y, 0, 0, 0)); dab[-1] = (x, y, rng.uniform(2.5, 5), rng.uniform(1.6, 3), rng.uniform(-20, 20))
    art = G(art, ellipses(W, H, dab) * cone, "#4d6e58", "#36543f", seed=nx(), density=0.22, edge=0.4, bloom=0, rough=1.5, feather=0.8)
    haze = cone * np.clip((yy - (HZ - 70)) / 70, 0, 1)
    art = OV(art, gaussian_filter(haze, 3) * 0.45, lambda m: tint(m, "#e9cdb4", 1.0))
    # summit rim highlight + cloud collar around the upper slopes
    rim = strokes(W, H, [(curve([(px - 14, py + 6), (px, py + 2), (px + 14, py + 6)], 8), 3, None)])
    art = G(art, rim, "#c7c9c0", seed=nx(), density=0.6, edge=0.2, rough=1)
    collar = strokes(W, H, [(curve([(px - 190, py + 150), (px - 60, py + 128), (px + 80, py + 140), (px + 240, py + 120)], 40), 26, (0.3, 0.35)),
                            (curve([(px - 120, py + 180), (px + 30, py + 170), (px + 160, py + 182)], 30), 14, (0.3, 0.35))])
    art = OV(art, gaussian_filter(collar, 4) * 0.85, lambda m: gouache_paint(m, "#fbf3e6", "#efe2d0", seed=nx(), rough=8, streak=0.6, density=0.82))
    clear()
    # distant islands (Halmahera hint) on the horizon right
    isl = polys(W, H, [[(W * 0.66, HZ + 2), (W * 0.72, HZ - 14), (W * 0.80, HZ - 18), (W * 0.9, HZ - 10), (W + 10, HZ - 16), (W + 10, HZ + 2)]])
    art = G(art, isl, "#8f9ca8", seed=nx(), density=0.45, edge=0.4, bloom=0.2, rough=3)
    # sea
    sea = polys(W, H, [rect(-10, HZ, W + 10, H + 10)])
    art = GP(art, sea, "#5a9b9a", SEA_D, seed=nx(), rough=1.2, streak=1.0)
    deep = sea * np.clip((yy - HZ) / (H * 0.22), 0, 1)
    art = G(art, deep, SEA_D, "#1f4b52", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=3)
    # sun glitter + swell lines
    glit = []
    for k in range(110):
        y = HZ + 4 + (k / 70) ** 1.6 * (H * 0.2)
        x = W * 0.84 + rng.gauss(0, 18 + (y - HZ) * 0.7)
        glit.append(([(x - rng.uniform(6, 22), y), (x + rng.uniform(6, 22), y)], rng.uniform(1.2, 2.6), (0.3, 0.3)))
    art = OV(art, strokes(W, H, glit), lambda m: gouache_paint(m, "#f7dcb6", "#fbeedb", seed=nx(), rough=0.8, streak=0.2, density=0.9))
    swell = [([(x, y), (x + rng.uniform(30, 80), y + rng.uniform(-1, 1))], 1.4, (0.3, 0.3)) for x, y in [(rng.uniform(-20, W), rng.uniform(HZ + 10, H * 0.82)) for _ in range(50)]]
    art = G(art, strokes(W, H, swell) * sea, "#9cc6bf", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    clear()
    # shoreline: wet sand strip, then the grassy terrace the palace stands on
    GY = int(H * 0.82)
    sand = polys(W, H, [[(-10, GY - 4), (W * 0.3, GY - 22), (W * 0.7, GY - 26), (W + 10, GY - 14), (W + 10, H + 10), (-10, H + 10)]])
    art = GP(art, sand, "#e6c9a0", "#d4ad7e", seed=nx(), rough=3, streak=0.8)
    foam = strokes(W, H, [(curve([(-10, GY - 6), (W * 0.3, GY - 24), (W * 0.7, GY - 28), (W + 10, GY - 16)], 50), 2.5, None)])
    art = OV(art, foam, lambda m: gouache_paint(m, "#f8f1e4", seed=nx(), rough=1.5, density=0.85))
    land = polys(W, H, [[(-10, GY + 20), (W * 0.18, GY - 2), (W * 0.5, GY - 10), (W * 0.82, GY), (W + 10, GY + 10), (W + 10, H + 10), (-10, H + 10)]])
    art = GP(art, land, "#7c8a4c", "#55663a", seed=nx(), rough=4, streak=0.9)
    art = G(art, land * np.clip((yy - GY) / 90, 0, 1), "#3e4c2a", seed=nx(), density=0.45, edge=0.1, bloom=0.4, rough=4)
    grass = strokes(W, H, [([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(5, 12))], 1.6, (0.0, 0.8)) for x, y in [(rng.uniform(0, W), rng.uniform(GY, H)) for _ in range(500)]])
    art = G(art, grass * land, "#3f522a", "#9aa461", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    # Kadato Kie — white palace, two storeys, stepped hipped roofs, grand frontal stair
    cx, by = W * 0.56, GY - 2
    bw = 300
    base = polys(W, H, [rect(cx - bw * 0.56, by - 22, cx + bw * 0.56, by + 4)])
    lower = polys(W, H, [rect(cx - bw * 0.5, by - 84, cx + bw * 0.5, by - 20)])
    upper = polys(W, H, [rect(cx - bw * 0.3, by - 136, cx + bw * 0.3, by - 92)])
    wings = polys(W, H, [rect(cx - bw * 0.72, by - 58, cx - bw * 0.5, by - 18), rect(cx + bw * 0.5, by - 58, cx + bw * 0.72, by - 18)])
    roof1 = polys(W, H, [[(cx - bw * 0.56, by - 82), (cx - bw * 0.36, by - 104), (cx + bw * 0.36, by - 104), (cx + bw * 0.56, by - 82)]])
    roof2 = polys(W, H, [[(cx - bw * 0.36, by - 134), (cx - bw * 0.16, by - 170), (cx + bw * 0.16, by - 170), (cx + bw * 0.36, by - 134)]])
    roof3 = polys(W, H, [[(cx - bw * 0.15, by - 168), (cx - bw * 0.04, by - 192), (cx + bw * 0.04, by - 192), (cx + bw * 0.15, by - 168)]])
    roofw = polys(W, H, [[(cx - bw * 0.77, by - 56), (cx - bw * 0.68, by - 72), (cx - bw * 0.52, by - 72), (cx - bw * 0.48, by - 56)],
                         [(cx + bw * 0.48, by - 56), (cx + bw * 0.52, by - 72), (cx + bw * 0.68, by - 72), (cx + bw * 0.77, by - 56)]])
    stair = polys(W, H, [[(cx - 34, by - 22), (cx + 34, by - 22), (cx + 70, by + 16), (cx - 70, by + 16)]])
    walls = np.maximum.reduce([base, lower, upper, wings])
    shadow = soft_shadow(np.maximum(walls, stair), "#2c3a20", blur=6, strength=0.45, dx=10, dy=4)
    art = over(art, shadow)
    art = GP(art, walls, "#fbf6ec", "#ece2d2", seed=nx(), rough=1.8, streak=0.6)
    # cool shade on right faces + under the eaves
    sh = np.maximum.reduce([polys(W, H, [rect(cx - bw * 0.5, by - 84, cx + bw * 0.5, by - 74), rect(cx - bw * 0.3, by - 136, cx + bw * 0.3, by - 128),
                                         rect(cx - bw * 0.72, by - 58, cx - bw * 0.5, by - 52), rect(cx + bw * 0.5, by - 58, cx + bw * 0.72, by - 52)])])
    art = G(art, sh, "#b9b2b0", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    art = G(art, walls * np.clip((xx - cx - bw * 0.2) / 160, 0, 1), "#c9bfb6", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=2)
    # windows / arched doors: rows of tall openings
    ops = []
    for k in range(-6, 7):
        if abs(k) <= 1:
            continue
        x = cx + k * bw * 0.072
        ops.append(rect(x - 6, by - 66, x + 6, by - 32))
    for k in range(-3, 4):
        x = cx + k * bw * 0.075
        ops.append(rect(x - 5, by - 124, x + 5, by - 100))
    for sgn in (-1, 1):
        for k in range(2):
            x = cx + sgn * bw * (0.56 + k * 0.1)
            ops.append(rect(x - 5, by - 46, x + 5, by - 26))
    art = GP(art, polys(W, H, ops), "#5a4434", "#3a2a20", seed=nx(), rough=0.5, streak=0.3, pad=8)
    door = polys(W, H, [rect(cx - 15, by - 72, cx + 15, by - 22)])
    art = GP(art, door, CLOVE, CLOVE_D, seed=nx(), rough=0.5, pad=8)
    # columns on the facade + cornice lines
    cols = strokes(W, H, [([(cx + k * bw * 0.072 + bw * 0.036, by - 80), (cx + k * bw * 0.072 + bw * 0.036, by - 22)], 2.2, None) for k in range(-7, 7)])
    art = G(art, cols * lower, "#c8beb0", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    cor = strokes(W, H, [([(cx - bw * 0.5, by - 22), (cx + bw * 0.5, by - 22)], 2.4, None), ([(cx - bw * 0.3, by - 92), (cx + bw * 0.3, by - 92)], 2.2, None)])
    art = G(art, cor, "#a99f94", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    # stair: pale stone with tread lines + balustrade
    art = GP(art, stair, "#efe6d6", "#d9cdb9", seed=nx(), rough=0.8, streak=0.3)
    tr = strokes(W, H, [([(cx - 34 - 36 * t, by - 22 + 38 * t), (cx + 34 + 36 * t, by - 22 + 38 * t)], 1.3, None) for t in [i / 9 for i in range(1, 9)]])
    art = G(art, tr * stair, "#a69a88", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.4)
    bal = strokes(W, H, [([(cx - 36, by - 24), (cx - 74, by + 14)], 4, None), ([(cx + 36, by - 24), (cx + 74, by + 14)], 4, None)])
    art = GP(art, bal, "#fbf6ec", "#e5dccd", seed=nx(), rough=0.5)
    # roofs: clove-red tiles, darker ridge, tile courses
    roofs = np.maximum.reduce([roof1, roof2, roof3, roofw])
    art = GP(art, roofs, "#8c3a2c", CLOVE_D, seed=nx(), rough=1.6, streak=0.9)
    courses = strokes(W, H, [([(0, y), (W, y)], 1.1, None) for y in range(int(by - 192), int(by - 56), 6)])
    art = G(art, courses * roofs, "#3d140f", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.4)
    eaves = polys(W, H, [rect(cx - bw * 0.57, by - 84, cx + bw * 0.57, by - 80), rect(cx - bw * 0.37, by - 136, cx + bw * 0.37, by - 132), rect(cx - bw * 0.16, by - 170, cx + bw * 0.16, by - 167)])
    art = GP(art, eaves, "#e9d9b8", "#cdb98e", seed=nx(), rough=0.4)
    fin = np.maximum(polys(W, H, [rect(cx - 1.6, by - 214, cx + 1.6, by - 190)]), circles(W, H, [(cx, by - 214, 4.5)]))
    art = FO(art, fin, "#c9a24f", seed=nx(), emboss=0.5)
    # coconut palms framing the palace + leafy shrubs along the terrace
    for x, h, lean in [(W * 0.07, 250, 0.10), (W * 0.19, 190, -0.10), (W * 0.94, 230, -0.12)]:
        art = palm2(art, W, H, x, GY + 16, h, lean, rng, nx)
    bush = []
    for x0 in list(np.linspace(10, W * 0.33, 7)) + list(np.linspace(W * 0.79, W - 6, 5)):
        for _ in range(9):
            bush.append((x0 + rng.gauss(0, 10), GY + 6 + rng.gauss(0, 5) - rng.uniform(0, 14), rng.uniform(5, 9), rng.uniform(3, 5), rng.uniform(-60, 60)))
    bm = ellipses(W, H, bush)
    art = G(art, bm, "#6f8a45", "#3a5228", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.5, feather=0.6)
    art = G(art, bm * np.clip((yy - GY + 6) / 14, 0, 1), "#2b3d1f", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1)
    art = add_grain(art, 5, 0.03)
    show(art, "td-scene")
    save_full(art, f"{OUT}/scene.webp", size=(780, 720), quality=80)
    clear()

if "clove" in PARTS:
    W, H = 560, 600
    nx = Seq(30200); rng = random.Random(32)
    art = blank(W, H)
    # woody twig sweeping up from bottom-left, with side twigs
    main = curve([(40, H - 20), (150, H - 160), (250, H - 300), (340, H - 430), (440, 90)], 60)
    sides = [curve([main[22], (300, 330), (430, 300), (500, 250)], 30), curve([main[34], (210, 220), (150, 140), (120, 70)], 30),
             curve([main[12], (230, 500), (330, 520)], 24)]
    tw = strokes(W, H, [(main, 9, (0.0, 0.7))] + [(sd, 5, (0.0, 0.7)) for sd in sides])
    art = G(art, tw, "#8a6a4c", "#5a3e2a", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)
    # leaves in pairs along the twigs (older leaves green, tip leaves rusty young)
    for pts, n0 in [(main, 4), (sides[0], 3), (sides[1], 3), (sides[2], 2)]:
        for k in range(n0):
            i = int((k + 0.6) / (n0 + 0.4) * (len(pts) - 1))
            x, y = pts[i]; x2, y2 = pts[min(len(pts) - 1, i + 1)]
            a = math.atan2(y2 - y, x2 - x)
            for j in (-1, 1):
                art = clove_leaf(art, W, H, x, y, rng.uniform(120, 160), a + j * rng.uniform(0.55, 0.85), rng, nx, young=(k == n0 - 1 and j == 1))
    clear()
    # bud clusters at tips
    for (x, y), a in [(main[-1], -0.9), (sides[0][-1], -0.3), (sides[1][-1], -1.9), (sides[2][-1], 0.3)]:
        art = clove_cluster(art, W, H, x, y, 46, a, 2.4, 9, rng, nx)
    show(art, "td-clove")
    save(art, f"{OUT}/clove.webp", max_w=400, quality=82)
    clear()

if "nutmeg" in PARTS:
    # whole nutmeg fruit split along its seam: apricot husk, white flesh lips, dark seed laced with scarlet mace
    W, H = 440, 440
    nx = Seq(30300); rng = random.Random(33)
    art = blank(W, H)
    cx, cy = 220, 250
    for ang, L, yng in [(-2.45, 180, False), (-0.6, 170, False), (-1.35, 120, True)]:
        art = clove_leaf(art, W, H, cx + math.cos(ang) * 40, cy - 96 + math.sin(ang) * 10, L, ang, rng, nx, young=yng)
    fruit = shape_mask(W, H, deform(ellipse_pts(cx, cy, 118, 112, 14, 0.2), rng, 1, 0.03))
    art = G(art, fruit, "#f1cf8c", "#e2a866", seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = fruit * np.clip(((xx - cx) * 0.6 + (yy - cy) * 0.8) / 130, 0, 1)
    art = G(art, shade, "#b9773e", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=2)
    hl = gaussian_filter(circles(W, H, [(cx - 52, cy - 50, 30)]), 10) * fruit
    art = OV(art, hl * 0.7, lambda m: tint(m, "#fbecc8", 0.9))
    # the open seam (lens) with a creamy flesh rim
    lens = [(cx + 18 + 70 * math.sin(t * math.pi) * (1 if side else -1) * 0.62, cy - 104 + 208 * t) for side in (1, 0) for t in ([i / 20 for i in range(21)] if side else [1 - i / 20 for i in range(21)])]
    lm = shape_mask(W, H, lens)
    art = GP(art, lm, "#fbf1dc", "#efdcb4", seed=nx(), rough=1.0)
    inner = shape_mask(W, H, [(cx + 18 + (x - cx - 18) * 0.78, cy + (y - cy) * 0.86) for x, y in lens])
    art = GP(art, inner, "#4a2414", "#2a130a", seed=nx(), rough=0.8, streak=0.4)
    lace = []
    for k in range(7):
        x0 = cx + 18 + (k - 3) * 10
        pts = [(x0 + math.sin(t * 7 + k * 1.3) * 9, cy - 86 + 172 * t) for t in [i / 40 for i in range(41)]]
        lace.append((pts, rng.uniform(5, 8), (0.25, 0.25)))
        for _ in range(3):
            t0 = rng.uniform(0.15, 0.85); i0 = int(t0 * 40)
            bx, by_ = pts[i0]
            lace.append(([(bx, by_), (bx + rng.uniform(-14, 14), by_ + rng.uniform(4, 14))], 3.5, (0.2, 0.6)))
    art = G(art, strokes(W, H, lace) * inner, "#de4a32", "#a8231a", seed=nx(), density=0.95, edge=0.65, bloom=0.1, rough=1.0, feather=0.5)
    art = OV(art, gaussian_filter(circles(W, H, [(cx + 8, cy - 40, 8)]), 3) * inner * 0.6, lambda m: tint(m, "#ffd2bf", 0.8))
    rim = edge_of(fruit, 2.5)
    art = G(art, rim, "#a5652f", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1, feather=0.8)
    stem = strokes(W, H, [(curve([(cx - 4, cy - 108), (cx - 2, cy - 132), (cx + 10, cy - 150)], 10), 7, (0.0, 0.5))])
    art = G(art, stem, "#6d5a3a", seed=nx(), density=0.9, edge=0.4, rough=0.8)
    show(art, "td-nutmeg")
    save(art, f"{OUT}/nutmeg.webp", max_w=240, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 520, 90
    nx = Seq(30400); rng = random.Random(34)
    art = blank(W, H)
    for sgn in (-1, 1):
        pts = curve([(W / 2 + sgn * 40, 46), (W / 2 + sgn * 120, 40), (W / 2 + sgn * 190, 50), (W / 2 + sgn * 250, 44)], 40)
        art = G(art, strokes(W, H, [(pts, 3.2, (0.05, 0.8))]), CLOVE, CLOVE_D, seed=nx(), density=0.85, edge=0.5, rough=1, feather=0.6)
        for t in (0.35, 0.7):
            x, y = pts[int(t * 39)]
            art = clove_leaf(art, W, H, x, y, 36, (-0.6 if sgn > 0 else -2.5), rng, nx)
    art = clove_cluster(art, W, H, W / 2, 56, 26, -math.pi / 2, 2.8, 7, rng, nx)
    show(art, "td-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
