"""Ultah Es Krim — gouache ice-cream party for a kids' birthday: a towering four-scoop cone with drips, sprinkles and a
cherry, an ice-cream cart with a striped parasol, a scalloped striped awning, a strawberry-sauce drip band, a single
cone, a popsicle and a sprinkle scatter tile.
Run: python3 -I ultah-es-krim.py [part ...]  parts: tower cart awning drip cone popsicle sprinkles
Assets -> public/themes/art/ultah-es-krim/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m3_lib import *

OUT = outdir("ultah-es-krim")
PARTS = sys.argv[1:] or ["tower", "cart", "awning", "drip", "cone", "popsicle", "sprinkles"]
PINK, PINK_D, PINK_L = "#f29bb4", "#d96f8f", "#fbc9d6"
MINT, MINT_D, MINT_L = "#9fdcc6", "#6cbfa3", "#cdf0e2"
VAN, VAN_D = "#fbefc8", "#ead39a"
CHOC, CHOC_D, CHOC_L = "#7a4a33", "#55301f", "#9c6446"
CONE, CONE_D, CONE_L = "#e9b56a", "#c48a42", "#f6d39a"
CHERRY, CHERRY_D = "#e23a4a", "#a81f30"
BERRY = "#b48ce0"
SPRINK = ["#f25c78", "#ffd25a", "#6fc6f0", "#8ed36b", "#b48ce0", "#ffffff", "#ff9f4a"]


def scoop_pts(cx, cy, r, rng, lip=10, n_scal=7, squash=0.88):
    """Scoop: domed top (upper ellipse) and a ruffled bottom lip of round scallops."""
    pts = []
    for i in range(25):
        a = math.pi + math.pi * i / 24
        pts.append((cx + math.cos(a) * r * (1 + rng.uniform(-0.02, 0.02)), cy + math.sin(a) * r * squash))
    # bottom ruffle from right to left
    for k in range(n_scal):
        x0 = cx + r - 2 * r * k / n_scal
        x1 = cx + r - 2 * r * (k + 1) / n_scal
        xm = (x0 + x1) / 2
        dy = lip * (1 + rng.uniform(-0.25, 0.25))
        pts += [(x0, cy + 2), (xm + (x1 - x0) * 0.2, cy + dy), (xm, cy + dy * 1.15), (xm - (x1 - x0) * 0.2, cy + dy)]
    return pts


def scoop(art, W, H, cx, cy, r, col, col2, shade, light, nx, rng, lip=12):
    m = shapes(W, H, [scoop_pts(cx, cy, r, rng, lip)])
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.6, pad=8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx + r * 0.35) / r) ** 2 + ((yy - cy + r * 0.45) / r) ** 2)
    art = OV(art, m * np.clip((d - 0.8) / 0.7, 0, 1), lambda mm: gouache_paint(mm, shade, seed=nx(), rough=1.0, density=0.55))
    hl = shapes(W, H, [petal_pts(cx - r * 0.45, cy - r * 0.42, r * 0.5, r * 0.16, -0.6, n=10)])
    art = GP(art, hl, light, seed=nx(), rough=0.8, density=0.85, pad=4)
    # texture: little scraped flecks
    fl = strokes(W, H, [([(x, y), (x + rng.uniform(3, 8), y + rng.uniform(-2, 2))], 1.6, None) for x, y in [(cx + rng.uniform(-r * 0.7, r * 0.7), cy + rng.uniform(-r * 0.7, -2)) for _ in range(14)]])
    art = OV(art, fl * m, lambda mm: gouache_paint(mm, shade, seed=nx(), rough=0.4, density=0.5))
    return art, m


def sprinkles(W, H, rng, region, n, length=(6, 11), width=3.2, cols=SPRINK):
    out = []
    ys, xs = np.where(region > 0.6)
    if not len(xs):
        return out
    for _ in range(n):
        i = rng.randrange(len(xs))
        x, y = xs[i], ys[i]
        a = rng.uniform(0, math.pi)
        L = rng.uniform(*length) / 2
        out.append((rng.choice(cols), ([(x - math.cos(a) * L, y - math.sin(a) * L), (x + math.cos(a) * L, y + math.sin(a) * L)], width, None)))
    return out


def paint_sprinkles(art, W, H, items, nx):
    by = {}
    for c, it in items:
        by.setdefault(c, []).append(it)
    for c, its in by.items():
        art = GP(art, strokes(W, H, its), c, seed=nx(), rough=0.3, density=1.0, pad=4)
    return art


def waffle_cone(art, W, H, cx, top, bot, w, nx):
    cm = shapes(W, H, [[(cx - w / 2, top), (cx + w / 2, top), (cx + 4, bot), (cx - 4, bot)]], smooth=False)
    art = GP(art, cm, CONE, CONE_L, seed=nx(), rough=1.2, streak=0.8, pad=6)
    lines = []
    for k in range(-8, 9):
        x0 = cx + k * w * 0.14
        lines.append(([(x0 - w * 0.5, top - 10), (x0 + w * 0.5, bot + 30)], 3.2, None))
        lines.append(([(x0 + w * 0.5, top - 10), (x0 - w * 0.5, bot + 30)], 3.2, None))
    lm = strokes(W, H, lines) * cm
    art = OV(art, lm, lambda mm: gouache_paint(mm, CONE_D, seed=nx(), rough=0.5, density=0.9))
    art = OV(art, side_shade(cm, cx, cx + w * 0.6), lambda mm: gouache_paint(mm, CONE_D, seed=nx(), rough=0.5, density=0.35))
    return art


if "tower" in PARTS:
    W, H = 440, 940
    nx = Seq(61000)
    rng = random.Random(14)
    art = blank(W, H)
    cx = 220
    art = waffle_cone(art, W, H, cx, 640, 920, 210, nx)
    # scoops bottom -> top, each a little offset (wobbly tower)
    specs = [(cx - 4, 640, 118, PINK, PINK_L, PINK_D, "#ffe1ea"), (cx + 10, 520, 108, MINT, MINT_L, MINT_D, "#eafff6"),
             (cx - 8, 408, 100, VAN, "#fff6dc", VAN_D, "#ffffff"), (cx + 6, 300, 92, CHOC, CHOC_L, CHOC_D, "#c08a6a")]
    masks = []
    for x, y, r, c, c2, sh, li in specs:
        art, m = scoop(art, W, H, x, y, r, c, c2, sh, li, nx, rng, lip=14)
        masks.append(m)
    # drips: strawberry from the pink scoop onto the cone, chocolate sauce over the top
    drips = []
    for dx, L in [(-90, 46), (-52, 70), (-10, 38), (30, 84), (72, 52), (100, 34)]:
        x = cx - 4 + dx
        drips.append([(x - 9, 646), (x + 9, 646), (x + 8, 646 + L - 10), (x, 646 + L), (x - 8, 646 + L - 10)])
    art = GP(art, shapes(W, H, drips), PINK, PINK_D, seed=nx(), rough=0.8, pad=6)
    top_sauce = [(cx + 6 - 92, 300 - 16)] + arc_pts(cx + 6, 300 - 12, 92, math.pi * 1.06, math.pi * 1.94, 20) + [(cx + 6 + 92, 300 - 16)]
    sauce = []
    for dx, L in [(-80, 30), (-46, 56), (-8, 26), (26, 64), (64, 36)]:
        x = cx + 6 + dx
        sauce.append([(x - 10, 280), (x + 10, 280), (x + 9, 290 + L - 10), (x, 290 + L), (x - 9, 290 + L - 10)])
    sm = np.maximum(shapes(W, H, [top_sauce]) * masks[3], shapes(W, H, sauce) * (1 - 0) * (np.arange(H)[:, None] < 400))
    sm = np.maximum(shapes(W, H, [[(cx + 6 - 86, 270), (cx + 6 - 60, 228), (cx + 6, 210), (cx + 66, 226), (cx + 92, 268), (cx + 92, 286), (cx + 6 - 92, 286)]]) * masks[3], shapes(W, H, sauce))
    art = GP(art, sm, "#4a2516", "#6a3622", seed=nx(), rough=0.8, pad=6)
    art = GP(art, shapes(W, H, [petal_pts(cx - 30, 238, 46, 10, -0.35, n=10)]), "#9a5f43", seed=nx(), rough=0.5, density=0.8, pad=4)
    # vanilla drip onto the mint
    vd = [[(x - 8, 414), (x + 8, 414), (x + 7, 414 + L - 8), (x, 414 + L), (x - 7, 414 + L - 8)] for x, L in [(cx - 70, 40), (cx + 40, 56), (cx + 80, 30)]]
    art = GP(art, shapes(W, H, vd), VAN, VAN_D, seed=nx(), rough=0.8, pad=6)
    # sprinkles on vanilla & chocolate & pink
    items = sprinkles(W, H, rng, masks[2] * (np.arange(H)[:, None] < 400), 30) + sprinkles(W, H, rng, sm, 22) + sprinkles(W, H, rng, masks[0] * (np.arange(H)[:, None] < 630), 18)
    art = paint_sprinkles(art, W, H, items, nx)
    # cherry with stem
    stem = strokes(W, H, [(curve([(cx + 14, 196), (cx + 26, 150), (cx + 52, 126)], 14), 5, (0.0, 0.3))])
    art = GP(art, stem, "#5e7a2e", seed=nx(), rough=0.4, pad=4)
    ch = circles(W, H, [(cx + 8, 200, 32)])
    art = GP(art, ch, CHERRY, "#ef5464", seed=nx(), rough=1.0, pad=6)
    art = OV(art, side_shade(ch, cx, cx + 44), lambda mm: gouache_paint(mm, CHERRY_D, seed=nx(), rough=0.6, density=0.6))
    art = GP(art, ellipses(W, H, [(cx - 4, 188, 9, 6, -30)]), "#ffd6da", seed=nx(), rough=0.3, pad=4)
    preview(art, "ek-tower", tone="#fff3f6")
    save(art, f"{OUT}/tower.webp", max_w=230, quality=84)
    clear()

if "cart" in PARTS:
    W, H = 560, 600
    nx = Seq(62000)
    rng = random.Random(6)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # parasol
    pole = rects(W, H, [(272, 150, 280, 380)])
    art = GP(art, pole, "#c9c3bd", "#a9a29b", seed=nx(), rough=0.3, pad=4)
    can = shapes(W, H, [[(70, 176)] + arc_pts(276, 196, 208, math.pi * 1.06, math.pi * 1.94, 30) + [(482, 176)] + [(482 - k * 41.2 - (20.6 if j else 0), 176 + (16 if j else 0)) for k in range(10) for j in (0, 1)] + [(70, 176)]])
    can = shapes(W, H, [arc_pts(276, 196, 210, math.pi * 1.04, math.pi * 1.96, 40) + sum([[(482 - k * 41.6, 182), (482 - k * 41.6 - 20.8, 206), (482 - (k + 1) * 41.6, 182)] for k in range(10)], [])])
    art = GP(art, can, "#fff5ea", "#f7e7d8", seed=nx(), rough=1.0, pad=6)
    # pink panels: wedges from the top point
    tip = (276, -8)
    wedges = []
    for k in range(0, 10, 2):
        x0 = 482 - k * 41.6
        x1 = 482 - (k + 1) * 41.6
        wedges.append([tip, (x0 + 10, 160), (x0, 182), (x0 - 20.8, 206), (x1, 182), (x1 + 8, 160)])
    art = GP(art, shapes(W, H, wedges, smooth=False) * can, PINK, PINK_L, seed=nx(), rough=0.6, pad=4)
    art = OV(art, v_ramp(can, 40, 200) * 0.6, lambda mm: gouache_paint(mm, "#e5b9c0", seed=nx(), rough=0.6, density=0.35))
    art = GP(art, circles(W, H, [(276, -2, 10)]), PINK_D, seed=nx(), rough=0.3, pad=4)
    # cart box
    box = shapes(W, H, [[(110, 330), (450, 330), (440, 500), (120, 500)]], smooth=False)
    art = GP(art, box, MINT, MINT_L, seed=nx(), rough=1.0, streak=0.6, pad=6)
    stripes = rects(W, H, [(110, 372, 450, 388), (110, 404, 450, 410)])
    art = GP(art, stripes * box, PINK, seed=nx(), rough=0.5, pad=4)
    art = OV(art, side_shade(box, 330, 470), lambda mm: gouache_paint(mm, MINT_D, seed=nx(), rough=0.5, density=0.5))
    lid = shapes(W, H, [[(96, 312), (464, 312), (470, 336), (90, 336)]], smooth=False)
    art = GP(art, lid, "#fff5ea", "#efe2d2", seed=nx(), rough=0.6, pad=4)
    # three tubs with scoops peeking out of the lid
    for x, c, c2 in [(170, PINK, PINK_L), (276, VAN, "#fff6dc"), (382, CHOC, CHOC_L)]:
        art, _ = scoop(art, W, H, x, 314, 40, c, c2, {PINK: PINK_D, VAN: VAN_D, CHOC: CHOC_D}[c], "#ffffff", nx, rng, lip=8)
    items = sprinkles(W, H, rng, circles(W, H, [(276, 290, 30)]), 10, (5, 8), 2.6)
    art = paint_sprinkles(art, W, H, items, nx)
    # a big cone emblem on the side
    em = circles(W, H, [(280, 450, 34)])
    art = GP(art, em, "#fff5ea", seed=nx(), rough=0.6, pad=4)
    art = waffle_cone(art, W, H, 280, 452, 478, 30, nx)
    art, _ = scoop(art, W, H, 280, 450, 18, PINK, PINK_L, PINK_D, "#ffffff", nx, rng, lip=5)
    # handle + wheels
    handle = strokes(W, H, [(curve([(450, 360), (500, 340), (512, 300)], 12), 9, None)])
    art = GP(art, handle, "#c9c3bd", "#a9a29b", seed=nx(), rough=0.3, pad=4)
    for wx in (170, 390):
        wh = circles(W, H, [(wx, 516, 46)])
        art = GP(art, wh, "#5a5f73", "#474b5c", seed=nx(), rough=0.6, pad=4)
        art = GP(art, circles(W, H, [(wx, 516, 30)]), "#f7d46a", seed=nx(), rough=0.4, pad=4)
        sp = strokes(W, H, [([(wx + math.cos(a) * 6, 516 + math.sin(a) * 6), (wx + math.cos(a) * 28, 516 + math.sin(a) * 28)], 3, None) for a in np.linspace(0, math.tau, 8, endpoint=False)])
        art = GP(art, sp, "#d9a93c", seed=nx(), rough=0.3, pad=4)
        art = GP(art, circles(W, H, [(wx, 516, 7)]), "#5a5f73", seed=nx(), rough=0.3, pad=4)
    preview(art, "ek-cart", tone="#fff3f6")
    save(art, f"{OUT}/cart.webp", max_w=260, quality=84)
    clear()

if "awning" in PARTS:
    W, H = 640, 120
    nx = Seq(63000)
    P = 80
    body = rects(W, H, [(0, 0, W, 70)])
    scal = circles(W, H, [(x + P / 2, 70, P / 2) for x in range(-P, W + P, P)])
    m = np.maximum(body, scal * (np.arange(H)[:, None] >= 60))
    m = np.maximum(body, scal)
    art = GP(blank(W, H), m, "#fff5ea", "#f7ead9", seed=nx(), rough=0.8, pad=4)
    xx = np.arange(W)[None, :] * np.ones((H, 1))
    pink = (((xx // P) % 2) == 0).astype(np.float32) * m
    art = OV(art, pink, lambda mm: gouache_paint(mm, PINK, PINK_L, seed=nx(), rough=0.6, density=1.0))
    # fold shading inside each scallop and a top hem
    yy = np.arange(H)[:, None] * np.ones((1, W))
    sh = m * np.clip((yy - 50) / 60, 0, 1) * 0.6
    art = OV(art, sh, lambda mm: gouache_paint(mm, "#c96f8b", seed=nx(), rough=0.6, density=0.4))
    hem = rects(W, H, [(0, 0, W, 12)])
    art = GP(art, hem, MINT, MINT_D, seed=nx(), rough=0.4, pad=4)
    preview(art, "ek-awning", tone="#fff3f6")
    save_full(art, f"{OUT}/awning.webp", size=(320, 60), quality=86)
    clear()

if "drip" in PARTS:
    W, H = 640, 100
    nx = Seq(64000)
    rng = random.Random(2)
    band = rects(W, H, [(-5, 0, W + 5, 26)])
    drips = []
    x = 6
    while x < W - 40:
        w = rng.uniform(16, 26)
        L = rng.uniform(16, 64)
        drips.append([(x, 20), (x + w, 20), (x + w - 1, 20 + L - w * 0.4), (x + w / 2, 20 + L), (x + 1, 20 + L - w * 0.4)])
        x += w + rng.uniform(14, 40)
    m = np.maximum(band, shapes(W, H, drips))
    art = GP(blank(W, H), m, PINK, PINK_L, seed=nx(), rough=1.0, pad=6)
    hl = strokes(W, H, [([(d[0][0] + 5, 28), (d[0][0] + 5, 24 + (d[3][1] - 30) * 0.6)], 3, (0.2, 0.4)) for d in drips if d[3][1] > 50])
    art = GP(art, hl, "#ffe1ea", seed=nx(), rough=0.3, pad=4)
    art = paint_sprinkles(art, W, H, sprinkles(W, H, rng, band * (np.arange(H)[:, None] < 20), 40, (5, 9), 2.8), nx)
    preview(art, "ek-drip", tone="#fff3f6")
    save_full(art, f"{OUT}/drip.webp", size=(320, 50), quality=86)
    clear()

if "cone" in PARTS:
    W, H = 200, 300
    nx = Seq(65000)
    rng = random.Random(3)
    art = waffle_cone(blank(W, H), W, H, 100, 150, 290, 110, nx)
    art, m = scoop(art, W, H, 100, 150, 64, MINT, MINT_L, MINT_D, "#eafff6", nx, rng, lip=10)
    art = paint_sprinkles(art, W, H, sprinkles(W, H, rng, m * (np.arange(H)[:, None] < 140), 14, (8, 13), 4.2), nx)
    preview(art, "ek-cone", tone="#fff3f6")
    save(art, f"{OUT}/cone.webp", max_w=70, quality=88)
    clear()

if "popsicle" in PARTS:
    W, H = 200, 360
    nx = Seq(66000)
    rng = random.Random(4)
    art = blank(W, H)
    stick = shapes(W, H, [[(86, 250), (114, 250), (114, 340), (100, 350), (86, 340)]])
    art = GP(art, stick, "#e8c48c", "#d6ad70", seed=nx(), rough=0.5, pad=4)
    body = shapes(W, H, [[(40, 260), (40, 90)] + arc_pts(100, 90, 60, math.pi, math.tau, 20)[1:-1] + [(160, 90), (160, 260)]])
    art = GP(art, body, BERRY, "#c7a3ec", seed=nx(), rough=1.0, pad=6)
    dip = body * (np.arange(H)[:, None] < 120)
    art = GP(art, np.maximum(dip, shapes(W, H, [[(x - 8, 118), (x + 8, 118), (x, 118 + L)] for x, L in [(60, 30), (96, 46), (134, 26)]]) * body), PINK, PINK_L, seed=nx(), rough=0.8, pad=4)
    art = OV(art, side_shade(body, 110, 170), lambda mm: gouache_paint(mm, "#8b63bb", seed=nx(), rough=0.5, density=0.45))
    art = GP(art, shapes(W, H, [petal_pts(66, 150, 70, 10, -math.pi / 2, n=10)]), "#e7d6fa", seed=nx(), rough=0.5, density=0.8, pad=4)
    art = paint_sprinkles(art, W, H, sprinkles(W, H, rng, dip, 14, (8, 12), 4), nx)
    preview(art, "ek-popsicle", tone="#fff3f6")
    save(art, f"{OUT}/popsicle.webp", max_w=80, quality=88)
    clear()

if "sprinkles" in PARTS:
    S = 240
    nx = Seq(67000)
    rng = random.Random(9)
    region = np.ones((S, S), np.float32)
    region[:8] = 0; region[-8:] = 0; region[:, :8] = 0; region[:, -8:] = 0
    art = paint_sprinkles(blank(S, S), S, S, sprinkles(S, S, rng, region, 26, (10, 16), 4.6, [c for c in SPRINK if c != "#ffffff"]), nx)
    art[..., 3] *= 0.85
    preview(art, "ek-sprinkles", tone="#fff3f6")
    save_full(art, f"{OUT}/sprinkles.webp", size=(160, 160), quality=82)
    clear()
