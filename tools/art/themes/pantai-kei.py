"""Pantai Kei — Kei Islands (Maluku Tenggara): flour-white sand of Ngurbloat, layered turquoise sea, a low hazy island
on the horizon, a wooden Kei boat with a carved prow, a leaning coconut palm, a woven tenun Kei band (diamonds and
hooks in red-brown, black and ochre), shells. Watercolour on paper with gouache accents. Original art.
Run: python3 -I pantai-kei.py [part ...]   parts: scene palm boat tenun shell sand"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s6_lib import *

OUT = outdir("pantai-kei")
PARTS = sys.argv[1:] or ["scene", "palm", "boat", "tenun", "shell", "sand"]
SAND, SAND_D = "#fbf8f1", "#e9dfcc"
TEAL_D, TEAL, TURQ, AQUA = "#0d5c6b", "#168f97", "#3cc2bd", "#9fe3d6"
INK = "#12343c"
RED, RED_D, OCHRE, BLACK = "#b1442e", "#7c2a1c", "#d39a3a", "#2b211d"


def scene():
    W, H = 780, 800
    rng = random.Random(3); nx = Seq(300)
    HZ = 250
    art = painted_sky(W, H, [(0, "#a9d8e3"), (0.22, "#d5eef0"), (0.31, "#f3faf7"), (1, "#f3faf7")], seed=4, streak=0.5, grain=0.4)
    # soft cumulus near the horizon, white over the blue
    for (cx, cy, w, h) in [(150, 200, 300, 70), (600, 186, 260, 60), (380, 92, 180, 34), (700, 70, 140, 26)]:
        m = cloud_mask(W, H, cx, cy, w, h, rng, lobes=7)
        art = OV(art, m, lambda mm: pigment(mm, "#ffffff", "#fbfdfd", seed=nx(), density=0.9, edge=0.0, bloom=0.25, rough=7, feather=2.5, gran=0.1), pad=30)
        under = m * np.clip((np.arange(H)[:, None] - (cy + h * 0.1)) / (h * 0.4), 0, 1)
        art = G(art, under, "#c4dbe2", seed=nx(), density=0.35, edge=0.15, bloom=0.3, rough=6, feather=3)
    # far island (Kei Besar ridge), hazy
    ridge = [(330, HZ + 2)] + [(x, HZ - 34 * math.sin(math.pi * (x - 330) / 470) ** 0.6 - 6 * math.sin(x / 29) - rng.uniform(0, 3)) for x in range(340, 801, 16)] + [(800, HZ + 2)]
    art = G(art, shape_mask(W, H, ridge), "#86aea6", "#6b988f", seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=3)
    art = G(art, shape_mask(W, H, [(-10, HZ + 2), (-10, HZ - 6), (60, HZ - 12), (130, HZ - 8), (180, HZ + 2)]), "#a3c3bb", seed=nx(), density=0.55, edge=0.45, rough=2)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    xx = np.ones((H, 1), np.float32) * np.arange(W, dtype=np.float32)[None, :]
    shore_y = lambda x: 690 - 0.11 * x + 10 * math.sin(x / 90 + 1) + 4 * math.sin(x / 27)
    # sea: graded base wash, then glazed bands with wet edges
    sea_m = np.clip((yy - HZ) / 1.2, 0, 1)
    t = np.clip((yy - HZ) / (640 - HZ), 0, 1)
    t = np.clip(t + (fbm(W, H, 77, 120, 3) - .5) * 0.1 * (t > 0.04), 0, 1)
    stops = [(0, "#0f6474"), (0.2, "#1a8f98"), (0.48, "#38bdb8"), (0.78, "#8edfd2"), (1, "#d2f3ea")]
    rgb = np.zeros((H, W, 3), np.float32)
    for i in range(len(stops) - 1):
        a0, c0 = stops[i]; a1, c1 = stops[i + 1]
        k = np.clip((t - a0) / (a1 - a0), 0, 1)[..., None]
        sel = ((t >= a0) & (t <= a1))[..., None]
        rgb = np.where(sel, np.array(hex_rgb(c0)) * (1 - k) + np.array(hex_rgb(c1)) * k, rgb)
    streak = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), (1.5, 30))
    streak = (streak - streak.mean()) / (streak.std() + 1e-6)
    rgb = rgb * (1 + streak[..., None] * 0.018)
    art = over(art, rgba(rgb.astype(np.float32), sea_m))
    for (y0, y1, c, d) in [(HZ, HZ + 70, "#0c5a6a", 0.35), (HZ + 60, HZ + 150, "#1b8c95", 0.22), (HZ + 170, HZ + 260, "#2aa9a8", 0.18)]:
        band = shape_mask(W, H, [(-20, y0)] + [(x, y1 + 12 * math.sin(x / 70 + y0)) for x in range(-20, W + 40, 40)] + [(W + 20, y0)])
        art = G(art, band * sea_m, c, seed=nx(), density=d, edge=0.45, bloom=0.5, rough=12, feather=3, gran=0.3)
    # reef shadows under the turquoise
    for (cx, cy, rx, ry) in [(120, 470, 130, 20), (540, 420, 160, 16), (650, 505, 100, 14), (300, 530, 90, 12)]:
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, ry, 10), rng, 2, 0.16))
        art = G(art, m, "#2a8f8c", "#3a9e96", seed=nx(), density=0.3, edge=0.35, bloom=0.5, rough=10, feather=4)
    # light glints: broken horizontal strokes, opaque white
    rip = []
    for _ in range(80):
        y = rng.uniform(HZ + 10, 610)
        k = (y - HZ) / (610 - HZ)
        x = rng.uniform(-20, W)
        L = rng.uniform(10, 46) * (0.5 + k)
        rip.append(([(x, y), (x + L * .5, y + rng.uniform(-.8, .8)), (x + L, y)], 0.9 + 2.0 * k, (0.35, 0.35)))
    art = OV(art, strokes(W, H, rip), lambda mm: pigment(mm, "#f4fffb", seed=nx(), density=0.75, edge=0.0, bloom=0, rough=1.0, feather=0.4, gran=0.3), pad=8)
    # shoreline: sand, wet band, two foam laces
    top = [(x, shore_y(x)) for x in range(-20, W + 21, 12)]
    sand_m = shape_mask(W, H, top + [(W + 20, H + 10), (-20, H + 10)])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * np.array(hex_rgb(SAND), np.float32), sand_m))
    wet = shape_mask(W, H, top + [(x, y + 16 + 6 * math.sin(x / 50)) for x, y in top[::-1]])
    art = G(art, wet, "#ddd3bd", "#c8e4da", seed=nx(), density=0.5, edge=0.5, bloom=0.4, rough=4)
    swash = shape_mask(W, H, [(x, y - 26 - 8 * math.sin(x / 61)) for x, y in top] + [(x, y + 2) for x, y in top[::-1]])
    art = OV(art, swash, lambda mm: pigment(mm, "#e9fbf6", "#f7fffd", seed=nx(), density=0.55, edge=0.1, bloom=0.4, rough=6, feather=2), pad=20)
    foam = strokes(W, H, [([(x, y - 1) for x, y in top], 6.0, None), ([(x, y - 26 - 8 * math.sin(x / 61)) for x, y in top], 3.0, None)])
    art = OV(art, foam, lambda mm: gouache_paint(mm, "#ffffff", "#f3fbf9", seed=nx(), rough=3.0, dry=0.35), pad=12)
    # sand speckle + soft dune shading
    sp = (np.random.default_rng(9).random((H, W)) > 0.995).astype(np.float32)
    art = G(art, gaussian_filter(sp, 0.5) * 3 * sand_m, "#b8a88c", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.3)
    dune = sand_m * np.clip((yy - 700) / 60, 0, 1) * (fbm(W, H, 31, 90, 2) > 0.55)
    art = G(art, dune, SAND_D, seed=nx(), density=0.25, edge=0.3, bloom=0.4, rough=8, feather=6)
    fade = np.clip((H - 4 - yy) / 110, 0, 1)
    art[..., 3] *= fade
    show(art, "kei-scene", bg=SAND)
    save(art, f"{OUT}/scene.webp", max_w=780, quality=80)


def palm():
    W, H = 520, 760
    rng = random.Random(8); nx = Seq(500)
    art = blank(W, H)
    art = palm_tree(art, W, H, 500, 750, (250, 190), rng, nx, lean=-0.6, nfr=11, flen=190)
    show(art, "kei-palm", tone=SAND)
    save(art, f"{OUT}/palm.webp", max_w=380, quality=78)


def boat():
    W, H = 520, 260
    rng = random.Random(11); nx = Seq(700)
    art = blank(W, H)
    # hull: long low wooden boat, upswept carved prow (right) and stern (left)
    hull = [(40, 120), (90, 150), (200, 168), (330, 168), (430, 150), (488, 92), (500, 70), (492, 74), (470, 112), (420, 126), (300, 132), (160, 130), (70, 112), (48, 92), (40, 96)]
    hm = shape_mask(W, H, hull)
    art = paint(art, hm, "#f2ede2", "#ddd5c4", seed=nx(), rough=1.2)
    # coloured strakes
    st1 = hm * np.clip(shape_mask(W, H, [(30, 128), (520, 118), (520, 136), (30, 144)]), 0, 1)
    art = paint(art, st1, "#1f6f86", "#195a6e", seed=nx(), rough=0.8)
    st2 = hm * shape_mask(W, H, [(30, 146), (520, 136), (520, 146), (30, 156)])
    art = paint(art, st2, RED, RED_D, seed=nx(), rough=0.8)
    belly = hm * shape_mask(W, H, [(30, 156), (520, 146), (520, 200), (30, 200)])
    art = paint(art, belly, "#6b4a32", "#4c3322", seed=nx(), rough=0.8)
    # hull shading underside
    art = shade(art, hm * np.clip((np.arange(H)[:, None] - 140) / 30, 0, 1), "#3b3a3a", seed=nx(), density=0.3)
    # carved prow scroll
    scroll = strokes(W, H, [(spiral_pts(494, 66, 3, 14, 0.5, 1.4, 30), 3.0, None)])
    art = paint(art, scroll, RED_D, seed=nx(), rough=0.5)
    # gunwale line and ribs
    gw = strokes(W, H, [(curve([(48, 96), (70, 112), (160, 130), (300, 132), (420, 126), (470, 112), (492, 76)], 40), 3.0, None)])
    art = paint(art, gw, "#5b3d28", seed=nx(), rough=0.5)
    # small mast with a furled sail and a flag
    mast = strokes(W, H, [([(250, 128), (252, 18)], 4.5, None)])
    art = paint(art, mast, "#6b4a32", "#4c3322", seed=nx(), rough=0.6)
    sail = shape_mask(W, H, [(256, 26), (330, 100), (258, 112)])
    art = paint(art, sail, "#f7efe0", "#e4d6bd", seed=nx(), rough=1.5)
    art = G(art, strokes(W, H, [([(262, 70), (300, 86)], 2.0, None), ([(260, 92), (316, 100)], 2.0, None)]) * sail, "#c9b590", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    flag = shape_mask(W, H, [(252, 18), (282, 24), (252, 32)], smooth=False)
    art = paint(art, flag, RED, seed=nx(), rough=0.6)
    # water line reflection (soft)
    refl = shape_mask(W, H, deform(ellipse_pts(270, 176, 230, 9, 14), rng, 2, 0.1))
    art = G(art, refl, "#0e6a74", "#178e93", seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=5, feather=2)
    show(art, "kei-boat", bg="#3cc2bd")
    save(art, f"{OUT}/boat.webp", max_w=300, quality=82)


def tenun_tile(W, H, rng, nx):
    """One horizontal repeat of a Kei-inspired woven band: borders, stepped diamonds with hooks, small crosses."""
    art = blank(W, H)
    base = rrect(W, H, [(0, 0, W, H, 0)])
    art = paint(art, base, "#7c2a1c", "#6c2418", seed=nx(), rough=0.01, streak=1.6)
    # cream borders
    bands = shapes(W, H, [rr(0, 4, W, 9), rr(0, H - 9, W, H - 4)], smooth=False)
    art = paint(art, bands, "#efe2c6", seed=nx(), rough=0.01)
    blk = shapes(W, H, [rr(0, 11, W, 15), rr(0, H - 15, W, H - 11)], smooth=False)
    art = paint(art, blk, BLACK, seed=nx(), rough=0.01)
    cy = H / 2; n = 2; step = W / n
    polys, inner, hooks, dots_ = [], [], [], []
    for i in range(n):
        cx = step * (i + 0.5)
        r = H * 0.3
        # stepped diamond (stairs)
        pts = []
        s = 5
        for k in range(s + 1):
            pts.append((cx - r + k * r / s, cy - k * r / s * 1.0))
            pts.append((cx - r + (k + 1) * r / s, cy - k * r / s))
        dia = [(cx - r, cy), (cx, cy - r), (cx + r, cy), (cx, cy + r)]
        polys.append(dia)
        inner.append([(cx - r * .5, cy), (cx, cy - r * .5), (cx + r * .5, cy), (cx, cy + r * .5)])
        dots_.append((cx, cy, 2.6))
        for sx in (-1, 1):
            hx = cx + sx * step * 0.5
            hooks.append(([(hx, cy - r * .8), (hx, cy + r * .8)], 3.0, None))
            hooks.append(([(hx - 7, cy - r * .55), (hx, cy - r * .8), (hx + 7, cy - r * .55)], 2.4, None))
            hooks.append(([(hx - 7, cy + r * .55), (hx, cy + r * .8), (hx + 7, cy + r * .55)], 2.4, None))
    art = paint(art, shapes(W, H, polys, smooth=False), OCHRE, "#c48a2c", seed=nx(), rough=0.6)
    art = paint(art, shapes(W, H, inner, smooth=False), BLACK, seed=nx(), rough=0.5)
    art = paint(art, circles(W, H, dots_), "#efe2c6", seed=nx(), rough=0.3)
    art = paint(art, strokes(W, H, hooks), "#efe2c6", seed=nx(), rough=0.3)
    teeth = []
    for k in range(int(W / 12)):
        x0 = k * 12
        teeth.append([(x0, 15), (x0 + 6, 21), (x0 + 12, 15)])
        teeth.append([(x0, H - 15), (x0 + 6, H - 21), (x0 + 12, H - 15)])
    art = paint(art, shapes(W, H, teeth, smooth=False), OCHRE, seed=nx(), rough=0.3)
    # weave texture: fine vertical warp + horizontal weft
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = 0.5 + 0.25 * np.sin(xx * math.pi / 1.6) + 0.25 * np.sin(yy * math.pi / 2.2)
    art[..., :3] *= (0.9 + 0.12 * weave)[..., None]
    return art


def tenun():
    W, H = 240, 60
    rng = random.Random(5); nx = Seq(900)
    art = tenun_tile(W, H, rng, nx)
    art = np.concatenate([art, art, art], 1)
    show(art, "kei-tenun")
    save_full(art[:, :W], f"{OUT}/tenun.webp", quality=84)


def shell():
    W, H = 260, 200
    rng = random.Random(14); nx = Seq(1100)
    art = blank(W, H)
    # scallop shell
    cx, cy = 120, 120
    fan = [(cx, cy + 50)] + [(cx + math.cos(a) * 70, cy + math.sin(a) * 62) for a in [math.pi + 0.2 + k * (math.pi - 0.4) / 14 for k in range(15)]]
    fm = shape_mask(W, H, deform(fan, rng, 1, 0.02))
    art = G(art, fm, "#f3d8c4", "#e7b49a", seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=2)
    ribs = [([(cx, cy + 46), (cx + math.cos(a) * 66, cy + math.sin(a) * 58)], 2.2, (0.4, 0.1)) for a in [math.pi + 0.3 + k * (math.pi - 0.6) / 8 for k in range(9)]]
    art = G(art, strokes(W, H, ribs) * fm, "#c97f62", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=1)
    ear = shapes(W, H, [[(cx - 16, cy + 44), (cx + 16, cy + 44), (cx + 10, cy + 58), (cx - 10, cy + 58)]])
    art = G(art, ear, "#e7b49a", seed=nx(), density=0.8, edge=0.5, rough=1)
    # cowrie
    cw = shape_mask(W, H, deform(ellipse_pts(200, 150, 32, 22, 12, -0.4), rng, 1, 0.04))
    art = G(art, cw, "#f6efe2", "#d9c7a8", seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.5)
    sl = strokes(W, H, [(curve([(176, 162), (198, 152), (222, 138)], 12), 3.0, (0.2, 0.2))])
    art = G(art, sl, "#8a6a4a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.8)
    spots = [(rng.uniform(180, 220), rng.uniform(132, 160), rng.uniform(1.4, 2.6)) for _ in range(12)]
    art = G(art, circles(W, H, spots) * cw, "#b9905c", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.5)
    # small turquoise sea glass
    sg = shape_mask(W, H, deform(ellipse_pts(54, 168, 16, 11, 8, 0.4), rng, 1, 0.08))
    art = G(art, sg, "#8fdcd2", "#4fb8b0", seed=nx(), density=0.75, edge=0.7, rough=1.5)
    show(art, "kei-shell", tone=SAND)
    save(art, f"{OUT}/shell.webp", max_w=160, quality=84)


def sand():
    W, H = 360, 360
    rng = np.random.default_rng(21)
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(SAND), np.float32)
    g = wrap_noise(W, H, 2, 0.6); big = wrap_noise(W, H, 3, 30)
    v = 1 + (g - .5) * 0.035 + (big - .5) * 0.03
    sp = (rng.random((H, W)) > 0.993).astype(np.float32)
    sp = gaussian_filter(sp, 0.5, mode="wrap") * 2.2
    out = base * v[..., None]
    out = out * (1 - sp[..., None] * 0.18) + np.array(hex_rgb("#c9a978")) * sp[..., None] * 0.18
    arr = np.concatenate([np.clip(out, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/sand.webp", quality=70)


for p in PARTS:
    globals()[p]()
    clear()
