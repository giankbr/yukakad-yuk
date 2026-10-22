"""Natal Keluarga — a warm family Christmas in gouache: a fir tree with cream garlands, red/gold ornaments and glowing
warm bulbs; a gold-leaf star (separate, it twinkles); three candles in brass holders with separate flames (flicker);
a pine & poinsettia corner sprig; a single poinsettia; a string of warm lights; a painted deep-green backdrop.
No snow (Indonesian Christmas), no Santa. Run: python3 -I natal-keluarga.py [part ...]
Assets -> public/themes/art/natal-keluarga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c6_lib import *
import _j1_lib as _j1


def strokes(W, H, items, cap=True):
    """Densify two-point strokes so their taper is applied along the stroke (not collapsed to the thin end)."""
    return _j1.strokes(W, H, [((lerp_pts(it[0][0], it[0][-1], 8) if len(it[0]) == 2 else it[0]),) + tuple(it[1:]) for it in items], cap)

OUT = outdir("natal-keluarga")
PARTS = sys.argv[1:] or ["tree", "star", "candles", "flame", "sprig", "poinsettia", "lights", "night"]
PINE_D, PINE, PINE_L, PINE_H = "#173d2b", "#24573c", "#3d7a52", "#6a9e6a"
RED, RED_D, RED_L = "#b8322c", "#86211f", "#d8584a"
CREAM, CREAM_D = "#f1e4c4", "#d9c597"
GOLD = "#c9a24e"
WARM = "#ffd27a"
WOOD, WOOD_D = "#7a4e2e", "#4e3020"
DARK_BG = "#14301f"


def needles(art, W, H, polys_tiers, rng, nx):
    """Short gouache needle strokes radiating down/out from the tier spine, dark → light toward upper left."""
    for tier, (cx, top, bot, half) in enumerate(polys_tiers):
        for col, frac, wd in ((PINE, 1.0, 4.2), (PINE_L, 0.6, 3.4), (PINE_H, 0.22, 2.6)):
            items = []
            for _ in range(int(220 * frac * (0.6 + tier * 0.18))):
                t = rng.uniform(0.1, 1.0)
                y = top + (bot - top) * t
                span = half * (t ** 0.9)
                x = cx + rng.uniform(-span, span)
                side = 1 if x > cx else -1
                if col == PINE_H and side > 0 and rng.random() < 0.7:
                    continue
                L = rng.uniform(10, 22)
                a = math.pi / 2 - side * rng.uniform(0.4, 0.9)
                items.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L * 0.8)], wd, (0.1, 0.5)))
            m = strokes(W, H, items)
            art = GP(art, m, col, mix(col, "#0f2a1d", 0.2), seed=nx(), rough=0.8, streak=0.7, pad=8)
    return art


if "night" in PARTS:
    W, H = 400, 860
    sky = painted_sky(W, H, [(0, "#0f2a1d"), (0.45, "#173d2b"), (0.8, "#1c4632"), (1, "#14301f")], seed=7, streak=1.0, grain=0.8)
    save_rgb(sky, f"{OUT}/night.webp", quality=66)

if "tree" in PARTS:
    W, H = 560, 800
    nx = Seq(61000); rng = random.Random(21); art = blank(W, H)
    cx = 280
    tiers = [(cx, 70, 210, 86), (cx, 150, 330, 140), (cx, 250, 460, 190), (cx, 360, 590, 236), (cx, 470, 690, 262)]
    # trunk + pot
    trunk = shapes(W, H, [[(cx - 22, 660), (cx + 22, 660), (cx + 26, 720), (cx - 26, 720)]], smooth=False)
    art = GP(art, trunk, WOOD, WOOD_D, seed=nx(), rough=1.0)
    pot = shapes(W, H, [[(cx - 70, 700), (cx + 70, 700), (cx + 56, 790), (cx - 56, 790)]], smooth=False)
    art = GP(art, pot, RED, RED_D, seed=nx(), rough=1.2, streak=0.8)
    art = tint(art, side_light(pot, -8, 0, 5), RED_D, 0.6, seed=nx())
    band = shapes(W, H, [[(cx - 70, 700), (cx + 70, 700), (cx + 67, 716), (cx - 67, 716)]], smooth=False)
    art = gold_leaf(art, band, GOLD, seed=nx())
    # tiers: silhouette with scalloped hem
    polys = []
    for (x, top, bot, half) in tiers:
        hem = []
        n = 9
        for k in range(n + 1):
            px = x + half - 2 * half * k / n
            hem.append((px, bot + (10 if k % 2 else -4) + rng.uniform(-3, 3)))
        polys.append(deform([(x, top)] + [(x + half * 0.5, (top + bot) / 2 + 8)] + hem + [(x - half * 0.5, (top + bot) / 2 + 8)], rng, 1, 0.01))
    for i in reversed(range(len(polys))):
        m = shapes(W, H, [polys[i]])
        art = GP(art, m, PINE_D, "#1d4a34", seed=nx(), rough=1.6, streak=0.6)
        art = needles(art, W, H, [tiers[i]], rng, nx)
        art = tint(art, side_light(m, 0, -14, 8), "#0f2a1d", 0.55, seed=nx())
    full = shapes(W, H, polys)
    # garlands: cream ribbon drapes
    drapes = []
    for (y0, y1, hw, sag) in [(170, 190, 70, 18), (290, 320, 120, 24), (410, 448, 168, 30), (530, 572, 214, 34)]:
        pts = [(cx - hw + 2 * hw * t, y0 + (y1 - y0) * t + math.sin(t * math.pi) * sag) for t in [j / 24 for j in range(25)]]
        drapes.append(pts)
    gm = strokes(W, H, [(d, 7, (0.08, 0.08)) for d in drapes]) * np.clip(gaussian_filter(full, 3) * 1.4, 0, 1)
    art = GP(art, gm, CREAM, CREAM_D, seed=nx(), rough=0.8, streak=0.9)
    art = tint(art, side_light(gm, 0, -3, 1.5), "#a89060", 0.5, seed=nx())
    # ornaments
    orns = []
    for (x, top, bot, half) in tiers[1:]:
        for _ in range(4):
            t = rng.uniform(0.45, 0.95)
            y = top + (bot - top) * t
            ox = x + rng.uniform(-half * t * 0.8, half * t * 0.8)
            orns.append((ox, y, rng.uniform(9, 13), rng.choice(["red", "red", "gold", "cream"])))
    for ox, oy, r, kind in orns:
        m = circles(W, H, [(ox, oy, r)])
        if kind == "gold":
            art = gold_leaf(art, m, GOLD, seed=nx())
        else:
            art = GP(art, m, RED if kind == "red" else CREAM, RED_D if kind == "red" else CREAM_D, seed=nx(), rough=0.6, pad=6)
            art = tint(art, side_light(m, -4, -4, 2.5), RED_D if kind == "red" else "#b09a6a", 0.6, seed=nx())
        art = GP(art, circles(W, H, [(ox - r * 0.35, oy - r * 0.4, r * 0.25)]), "#fff4dc", seed=nx(), rough=0.3, pad=4, density=0.85)
        art = gold_leaf(art, shapes(W, H, [[(ox - 3, oy - r - 4), (ox + 3, oy - r - 4), (ox + 3, oy - r + 1), (ox - 3, oy - r + 1)]], smooth=False), GOLD, seed=nx())
    # warm bulbs along the garlands
    for d in drapes:
        for j in range(1, len(d) - 1, 3):
            x, y = d[j]
            art = bulb(art, x + rng.uniform(-2, 2), y + 9, 4.2, WARM, "#fff6dc", halo=0.9)
    # two simple wrapped gifts at the foot
    for (gx, gw, gh, col, rib) in ((cx - 150, 76, 58, CREAM, RED), (cx + 96, 64, 70, RED, CREAM)):
        box = shapes(W, H, [[(gx, 790 - gh), (gx + gw, 790 - gh), (gx + gw, 790), (gx, 790)]], smooth=False)
        art = GP(art, box, col, mix(col, "#000000", 0.12), seed=nx(), rough=1.0)
        art = tint(art, side_light(box, -6, 0, 4), mix(col, "#000000", 0.35), 0.5, seed=nx())
        rb = shapes(W, H, [[(gx + gw / 2 - 5, 790 - gh), (gx + gw / 2 + 5, 790 - gh), (gx + gw / 2 + 5, 790), (gx + gw / 2 - 5, 790)]], smooth=False)
        art = GP(art, rb, rib, seed=nx(), rough=0.5, pad=6)
        bow = shapes(W, H, [[(gx + gw / 2, 790 - gh), (gx + gw / 2 - 20, 790 - gh - 14), (gx + gw / 2 - 18, 790 - gh + 4)], [(gx + gw / 2, 790 - gh), (gx + gw / 2 + 20, 790 - gh - 14), (gx + gw / 2 + 18, 790 - gh + 4)]])
        art = GP(art, bow, rib, seed=nx(), rough=0.5, pad=6)
    bbox_save(art, "nt-tree", f"{OUT}/tree.webp", 420, tone=CREAM, bg=DARK_BG)
    clear()

if "star" in PARTS:
    W, H = 220, 220
    nx = Seq(62000); art = blank(W, H)
    pts = [(110 + math.cos(-math.pi / 2 + k * math.pi / 5) * (70 if k % 2 == 0 else 30), 112 + math.sin(-math.pi / 2 + k * math.pi / 5) * (70 if k % 2 == 0 else 30)) for k in range(10)]
    m = shapes(W, H, [pts], smooth=False)
    art = OV(art, m, lambda mm: glow(mm, "#ffdf9a", radius=16, strength=0.55), pad=60)
    art = gold_leaf(art, m, "#d9b257", seed=nx(), crack=0.1)
    bbox_save(art, "nt-star", f"{OUT}/star.webp", 150, bg=DARK_BG)
    clear()

if "flame" in PARTS:
    W, H = 80, 130
    nx = Seq(63000); art = blank(W, H)
    outer = shapes(W, H, [petal_pts(40, 104, 70, 15, -math.pi / 2, n=16)])
    art = OV(art, outer, lambda mm: glow(mm, "#ffc66a", radius=10, strength=0.6), pad=40)
    art = GP(art, outer, "#ffb347", "#ffd27a", seed=nx(), rough=0.4, pad=6)
    inner = shapes(W, H, [petal_pts(40, 102, 40, 8, -math.pi / 2, n=14)])
    art = GP(art, inner, "#fff2c4", seed=nx(), rough=0.3, pad=6)
    keep_pixel(art, 0, 0); keep_pixel(art, W - 1, H - 1); art[0, 0, 3] = art[H - 1, W - 1, 3] = 0.03
    bbox_save(art, "nt-flame", f"{OUT}/flame.webp", 60, bg=DARK_BG)
    clear()

if "candles" in PARTS:
    W, H = 520, 380
    nx = Seq(64000); rng = random.Random(23); art = blank(W, H)
    for (x, top, wd) in ((150, 120, 46), (260, 60, 52), (370, 140, 44)):
        body = shapes(W, H, [[(x - wd / 2, top), (x + wd / 2, top), (x + wd / 2, 300), (x - wd / 2, 300)]], smooth=False)
        art = GP(art, body, CREAM, "#f8eed6", seed=nx(), rough=0.9, streak=0.9)
        art = tint(art, side_light(body, -8, 0, 5), CREAM_D, 0.7, seed=nx())
        drip = shapes(W, H, [[(x - wd / 2, top), (x - wd / 2 + 10, top), (x - wd / 2 + 9, top + 34), (x - wd / 2 + 4, top + 38), (x - wd / 2, top + 30)]])
        art = GP(art, drip, "#fbf4e2", seed=nx(), rough=0.4, pad=6)
        wick = strokes(W, H, [([(x, top), (x + 1, top - 12)], 3, None)])
        art = GP(art, wick, "#2a1d14", seed=nx(), rough=0.2, pad=4)
        holder = shapes(W, H, [[(x - wd / 2 - 18, 300), (x + wd / 2 + 18, 300), (x + wd / 2 + 8, 318), (x + 10, 324), (x + 14, 344), (x - 14, 344), (x - 10, 324), (x - wd / 2 - 8, 318)]])
        art = gold_leaf(art, holder, "#b8913f", seed=nx())
    # pine sprigs + berries at the base
    base_items = []
    for k in range(90):
        x0 = rng.uniform(60, 460); y0 = rng.uniform(338, 362)
        a = rng.uniform(-math.pi, 0) if rng.random() < 0.5 else rng.uniform(-0.6, 0.6) + (0 if x0 > 260 else math.pi)
        L = rng.uniform(14, 30)
        base_items.append(([(x0, y0), (x0 + math.cos(a) * L, y0 + math.sin(a) * L * 0.5)], rng.uniform(2.6, 3.6), (0.1, 0.5)))
    art = GP(art, strokes(W, H, base_items), PINE, PINE_D, seed=nx(), rough=0.6, streak=0.6)
    art = GP(art, strokes(W, H, base_items[::3]), PINE_L, seed=nx(), rough=0.6, streak=0.6)
    for bx, by in ((110, 352), (122, 344), (402, 350), (414, 358), (300, 362), (210, 356)):
        art = GP(art, circles(W, H, [(bx, by, 7)]), RED, RED_D, seed=nx(), rough=0.4, pad=6)
        art = GP(art, circles(W, H, [(bx - 2, by - 2.5, 2)]), "#ffe2d0", seed=nx(), rough=0.2, pad=4)
    bbox_save(art, "nt-candles", f"{OUT}/candles.webp", 360, bg=DARK_BG)
    clear()


def poinsettia(art, W, H, cx, cy, r, rng, nx, rot=0.0):
    for ring, (rf, n, col, col2) in enumerate([(1.0, 6, RED_D, RED), (0.78, 6, RED, RED_L)]):
        polys = []
        for k in range(n):
            a = rot + k / n * math.tau + ring * math.pi / n + rng.uniform(-.1, .1)
            polys.append(deform(petal_pts(cx, cy, r * rf * rng.uniform(0.9, 1.05), r * 0.22, a, n=14), rng, 1, 0.02))
        m = shapes(W, H, polys)
        art = GP(art, m, col, col2, seed=nx(), rough=0.9, streak=0.8)
        veins = []
        for p in polys:
            mid = p[len(p) // 4]
            veins.append(([(cx, cy), mid], 1.4, (0.1, 0.4)))
        art = tint(art, strokes(W, H, veins) * m, RED_D, 0.55, seed=nx())
    dots = [(cx + rng.gauss(0, r * 0.07), cy + rng.gauss(0, r * 0.07), r * 0.05) for _ in range(7)]
    art = GP(art, circles(W, H, dots), "#d9b257", "#6a8a3a", seed=nx(), rough=0.3, pad=6)
    return art


if "poinsettia" in PARTS:
    W, H = 240, 240
    nx = Seq(65000); rng = random.Random(25); art = blank(W, H)
    art = poinsettia(art, W, H, 120, 120, 104, rng, nx)
    bbox_save(art, "nt-poin", f"{OUT}/poinsettia.webp", 150, bg="#f4ead3")
    clear()

if "sprig" in PARTS:
    W, H = 600, 420
    nx = Seq(66000); rng = random.Random(27); art = blank(W, H)
    branches = [curve([(20, 40), (160, 90), (320, 140), (520, 170)], 40), curve([(40, 200), (180, 170), (300, 150)], 30), curve([(60, 20), (200, 30), (360, 70)], 30)]
    art = GP(art, strokes(W, H, [(b, 6, (0.0, 0.6)) for b in branches]), WOOD, WOOD_D, seed=nx(), rough=0.6)
    for col, frac in ((PINE_D, 1.0), (PINE, 0.8), (PINE_L, 0.4)):
        items = []
        for b in branches:
            for j in range(1, len(b) - 1):
                if rng.random() > frac:
                    continue
                x, y = b[j]; a0 = math.atan2(b[j + 1][1] - b[j - 1][1], b[j + 1][0] - b[j - 1][0])
                for side in (-1, 1):
                    a = a0 + side * rng.uniform(0.5, 1.0)
                    L = rng.uniform(22, 38) * (1 - j / len(b) * 0.4)
                    items.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(2.4, 3.4), (0.05, 0.6)))
        art = GP(art, strokes(W, H, items), col, mix(col, "#0f2a1d", 0.2), seed=nx(), rough=0.6, streak=0.7)
    art = poinsettia(art, W, H, 250, 160, 92, rng, nx, rot=0.3)
    art = poinsettia(art, W, H, 450, 210, 62, rng, nx, rot=1.0)
    for bx, by in ((120, 120), (132, 110), (110, 104), (370, 120), (382, 130), (540, 160), (552, 172)):
        art = GP(art, circles(W, H, [(bx, by, 9)]), RED, RED_D, seed=nx(), rough=0.4, pad=6)
        art = GP(art, circles(W, H, [(bx - 3, by - 3, 2.5)]), "#ffe2d0", seed=nx(), rough=0.2, pad=4)
    # small pine cone
    cone = shapes(W, H, [ellipse_pts(330, 240, 22, 34, 14, 0.3)])
    art = GP(art, cone, WOOD, WOOD_D, seed=nx(), rough=0.8)
    scales = [(arc_pts(330 + math.sin(0.3) * k * 6, 222 + k * 10, 16, 0.3, 2.8, 10), 2.2, (0.1, 0.1)) for k in range(5)]
    art = tint(art, strokes(W, H, scales) * cone, WOOD_D, 0.8, seed=nx())
    bbox_save(art, "nt-sprig", f"{OUT}/sprig.webp", 400, bg="#f4ead3")
    clear()

if "lights" in PARTS:
    W, H = 760, 110
    nx = Seq(67000); rng = random.Random(29); art = blank(W, H)
    wire = [(x, 24 + math.sin(x / 760 * math.pi * 3) * 10 + 14 * math.sin(x / 760 * math.pi)) for x in range(0, 761, 8)]
    art = GP(art, strokes(W, H, [(wire, 2.4, None)]), "#2a3a2a", seed=nx(), rough=0.2, pad=6)
    cols = [WARM, "#ffb070", "#fff0c0", WARM, "#ffc58a"]
    for i, j in enumerate(range(3, len(wire) - 2, 7)):
        x, y = wire[j]
        cap = shapes(W, H, [[(x - 4, y), (x + 4, y), (x + 4, y + 8), (x - 4, y + 8)]], smooth=False)
        art = GP(art, cap, "#3a4a3a", seed=nx(), rough=0.2, pad=4)
        art = bulb(art, x, y + 18, 7.5, cols[i % len(cols)], "#fffaf0", halo=1.0)
    bbox_save(art, "nt-lights", f"{OUT}/lights.webp", 520, bg=DARK_BG)
    clear()
