"""Balkon Paris — matte gouache (Parisian travel-sketch poster feel): cream limestone facade, French window with slate-blue
shutters, wrought-iron Juliet balcony with flower pots, wisteria/lilac cascades; striped café awning.
Run: python3 -I balkon-paris.py [part ...]   parts: window wisteria railing sprig awning stone
Assets -> public/themes/art/balkon-paris/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f4_lib import *

OUT = outdir("balkon-paris")
PARTS = sys.argv[1:] or ["window", "wisteria", "railing", "sprig", "garland", "awning", "stone"]

STONE, STONE_L, STONE_D = "#eadcc2", "#f4ead7", "#cdb995"
SLATE, SLATE_D, SLATE_L = "#7f93a6", "#5d7084", "#a3b4c3"
IRON, IRON_L = "#2a2830", "#5d5a66"
LILAC = ["#efe2f3", "#dcc4ea", "#c4a3dc", "#a986c9", "#8a68b3", "#6e4f9c"]
LEAF = ["#a9bf7a", "#86a35e", "#64844a"]


def raceme(W, H, x, y, L, ang, rng, buckets, leafm=None, scale=1.0, curl=0.15):
    """Wisteria raceme hanging from (x, y): florets along a drooping curve, open/pale at the top, buds/dark at the tip.
    Adds floret ellipses into `buckets` (list of lists per tone index)."""
    pts = [(x + math.sin(ang) * L * t + math.sin(t * 3 + rng.uniform(0, 1)) * L * curl * t, y + math.cos(ang) * L * t) for t in np.linspace(0, 1, 30)]
    n = int(64 * L / 160 * scale + 16)
    for i in range(n):
        t = (i / n) ** 0.85
        px, py = pts[int(t * 29)]
        wdt = (1 - t) ** 0.9 * L * 0.13 + 2.0 * scale
        for j in range(3 if t < 0.5 else (2 if t < 0.85 else 1)):
            ox = rng.uniform(-wdt, wdt)
            r = (1 - t * 0.55) * 5.6 * scale * rng.uniform(0.8, 1.2)
            tone = int(t * 4.4 + rng.uniform(-0.7, 0.7) + (0.9 if ox > wdt * 0.25 else 0))
            tone = min(5, max(0, tone))
            buckets[tone].append((px + ox, py + rng.uniform(-2, 2), r * 1.1, r * 0.8, rng.uniform(-40, 40)))
    return pts


def paint_wisteria(art, W, H, items, nx, rng, leaves=True, vine=None):
    buckets = [[] for _ in range(6)]
    for (x, y, L, ang, sc) in items:
        raceme(W, H, x, y, L, ang, rng, buckets, scale=sc)
    if vine:
        art = OV(art, strokes(W, H, [(v, 4.5, (0.05, 0.3)) for v in vine]), lambda m: gouache_paint(m, "#6d5a48", "#4f4234", seed=nx(), rough=1.2))
    if leaves:
        lv = [[], [], []]
        for (x, y, L, ang, sc) in items:
            for k in range(rng.randint(3, 5)):
                a = rng.uniform(-math.pi, 0) + rng.uniform(-.4, .4)
                lx, ly = x + rng.uniform(-14, 14) * sc, y + rng.uniform(-8, 10) * sc
                for j in range(5):
                    q = lx + math.cos(a) * j * 11 * sc, ly + math.sin(a) * j * 11 * sc
                    for side in (-1, 1):
                        lv[rng.randint(0, 2)].append(petal_pts(q[0], q[1], 17 * sc, 5.5 * sc, a + side * 1.0, n=10))
        for k in range(3):
            if lv[k]:
                art = OV(art, shapes(W, H, lv[k]), lambda m, k=k: gouache_paint(m, LEAF[k], LEAF[min(2, k + 1)], seed=nx(), rough=1.6, streak=0.8))
    # florets back-to-front: darker/tip tones first so pale open florets sit on top
    for tone in [5, 4, 3, 2, 1, 0]:
        if not buckets[tone]:
            continue
        m = ellipses(W, H, buckets[tone])
        art = OV(art, m, lambda m, t=tone: gouache_paint(m, LILAC[t], LILAC[max(0, t - 1)], seed=nx(), rough=1.3, streak=0.9))
    # tiny pale highlights on the open florets
    hl = ellipses(W, H, [(e[0] - e[2] * 0.3, e[1] - e[3] * 0.3, e[2] * 0.4, e[3] * 0.3, e[4]) for e in buckets[1][::2] + buckets[0][::2]])
    art = OV(art, hl, lambda m: gouache_paint(m, "#fbf6fb", seed=nx(), rough=0.8, density=0.8))
    return art


def railing_mask(W, H, x0, x1, ytop, ybot, s=1.0):
    """Wrought-iron balcony: rails, posts, paired C-scrolls in each panel, central oval medallion."""
    s = s * 1.35
    items = [([(x0, ytop), (x1, ytop)], 7 * s, None), ([(x0, ytop + 9 * s), (x1, ytop + 9 * s)], 2.6 * s, None),
             ([(x0, ybot), (x1, ybot)], 6 * s, None), ([(x0, ybot - 10 * s), (x1, ybot - 10 * s)], 2.6 * s, None)]
    hgt = ybot - ytop
    npan = max(3, int((x1 - x0) / (hgt * 0.62)))
    pw = (x1 - x0) / npan
    for i in range(npan + 1):
        x = x0 + i * pw
        items.append(([(x, ytop), (x, ybot)], 4.2 * s, None))
    for i in range(npan):
        cx = x0 + (i + 0.5) * pw
        cy = (ytop + ybot) / 2 + 2 * s
        r = min(pw, hgt) * 0.24
        if i == npan // 2:
            items.append((arc_pts(cx, cy, r * 1.25, 0, math.tau, 40, 1.3), 3.2 * s, None))
            items.append((arc_pts(cx, cy, r * 0.55, 0, math.tau, 24, 1.3), 2.4 * s, None))
            continue
        for sgn in (-1, 1):
            # C-scrolls back to back
            sp = spiral_pts(cx + sgn * r * 0.15, cy - r * 0.9, r * 0.9, r * 0.12, math.pi / 2 + (0 if sgn > 0 else math.pi), 1.1, 40, sgn)
            items.append((sp, 2.8 * s, (0.0, 0.4)))
            sp = spiral_pts(cx + sgn * r * 0.15, cy + r * 0.9, r * 0.9, r * 0.12, -math.pi / 2 + (0 if sgn > 0 else math.pi), 1.1, 40, -sgn)
            items.append((sp, 2.8 * s, (0.0, 0.4)))
        items.append(([(cx, ytop + 9 * s), (cx, ytop + 18 * s)], 2.4 * s, None))
        for bx in (cx - pw * 0.36, cx + pw * 0.36):
            items.append(([(bx, ytop + 9 * s), (bx, ybot - 10 * s)], 2.2 * s, None))
        items.append(([(cx, ybot - 10 * s), (cx, ybot - 18 * s)], 2.4 * s, None))
    # finials on posts
    m = strokes(W, H, items)
    balls = circles(W, H, [(x0 + i * pw, ytop - 6 * s, 5 * s) for i in range(npan + 1)])
    return np.maximum(m, balls)


def paint_iron(art, m, nx, light=(-2, -2)):
    art = OV(art, m, lambda mm: gouache_paint(mm, IRON, "#36333d", seed=nx(), rough=0.7, streak=0.6), pad=8)
    hi = np.clip(m - np.roll(np.roll(m, 2, 0), 2, 1), 0, 1) * 0.8
    return OV(art, hi, lambda mm: gouache_paint(mm, IRON_L, seed=nx(), rough=0.5, density=0.7), pad=6)


if "window" in PARTS:
    W, H = 680, 900
    nx = Seq(30100)
    rng = random.Random(3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    # stone wall patch with a brushy vignette edge
    wall = np.clip((displace(gaussian_filter(rect_m(W, H, 40, 40, W - 40, H - 30), 18), 31, 26, 60) - 0.3) * 2.2, 0, 1)
    art = OV(art, wall, lambda m: gouache_paint(m, STONE, STONE_L, seed=nx(), rough=2, streak=1.0))
    # ashlar joints
    joints = []
    for r_, y in enumerate(range(80, H - 40, 62)):
        joints.append((0, y, W, y))
        off = 0 if r_ % 2 else 70
        for x in range(off, W, 140):
            joints.append((x, y, x, y + 62))
    jm = lines(W, H, joints, 2.2) * wall
    art = OV(art, jm, lambda m: gouache_paint(m, STONE_D, seed=nx(), rough=1.2, density=0.55))
    art = OV(art, wall * np.clip((fbm(W, H, 41, 40, 3) - .5) * 2.5, 0, 1), lambda m: gouache_paint(m, "#d9c7a5", seed=nx(), rough=2, density=0.35))
    # window surround (moulded frame), recess, keystone
    X0, X1, Y0, Y1 = 196, 484, 140, 720
    surround = np.clip(rect_m(W, H, X0 - 30, Y0 - 30, X1 + 30, Y1) - rect_m(W, H, X0, Y0, X1, Y1), 0, 1)
    art = OV(art, surround, lambda m: gouache_paint(m, STONE_L, "#fbf4e6", seed=nx(), rough=1, streak=0.7))
    art = OV(art, np.clip(rect_m(W, H, X0 - 30, Y0 - 30, X1 + 30, Y0 - 22) + rect_m(W, H, X1 + 22, Y0 - 30, X1 + 30, Y1), 0, 1), lambda m: gouache_paint(m, STONE_D, seed=nx(), rough=0.8, density=0.6))
    key = shapes(W, H, [[(X0 + 120, Y0 - 34), (X1 - 120, Y0 - 34), (X1 - 128, Y0 + 14), (X0 + 128, Y0 + 14)]], smooth=False)
    art = OV(art, key, lambda m: gouache_paint(m, "#f7eedd", STONE, seed=nx(), rough=0.8))
    art = OV(art, lines(W, H, [(X0 + 130, Y0 - 20, X1 - 130, Y0 - 20)], 2) , lambda m: gouache_paint(m, STONE_D, seed=nx(), rough=0.5))
    # French window: two leaves, glass panes reflecting a lilac-blue sky, sheer curtain inside
    glass = rect_m(W, H, X0 + 8, Y0 + 8, X1 - 8, Y1 - 6)
    art = OV(art, glass, lambda m: np.concatenate([vgrad(m.shape[0], m.shape[1], [(0, "#9fb3c6"), (0.5, "#c8c2dc"), (1, "#8e8aa8")]) , m[..., None] * 0.97], -1), pad=0)
    art = OV(art, glass * np.clip((fbm(W, H, 51, 50, 2) - 0.4) * 2, 0, 1) * 0.5, lambda m: gouache_paint(m, "#e6e9f2", seed=nx(), rough=1, density=0.6))
    curtain = shapes(W, H, [[(X0 + 10, Y0 + 10), (X0 + 96, Y0 + 10), (X0 + 60, Y1 - 120), (X0 + 10, Y1 - 10)], [(X1 - 10, Y0 + 10), (X1 - 90, Y0 + 10), (X1 - 50, Y1 - 160), (X1 - 10, Y1 - 10)]])
    art = OV(art, curtain * glass, lambda m: gouache_paint(m, "#f3eef3", "#e2dceb", seed=nx(), rough=1, streak=1.2, density=0.85))
    # reflection diagonal
    refl = shapes(W, H, [[(X0 + 30, Y0 + 200), (X0 + 90, Y0 + 140), (X0 + 130, Y0 + 140), (X0 + 70, Y0 + 200)], [(X1 - 110, Y0 + 330), (X1 - 50, Y0 + 270), (X1 - 30, Y0 + 270), (X1 - 90, Y0 + 330)]], smooth=False)
    art = OV(art, refl * glass * 0.55, lambda m: gouache_paint(m, "#ffffff", seed=nx(), rough=0.6))
    # mullions + frames (cream painted wood)
    mx = (X0 + X1) / 2
    bars = [(X0 + 4, Y0 + 4, X1 - 4, Y0 + 4), (X0 + 4, Y1 - 4, X1 - 4, Y1 - 4), (X0 + 4, Y0, X0 + 4, Y1), (X1 - 4, Y0, X1 - 4, Y1), (mx, Y0, mx, Y1)]
    for k in range(1, 5):
        y = Y0 + (Y1 - Y0) * k / 5
        bars.append((X0, y, X1, y))
    for x in ((X0 + mx) / 2, (mx + X1) / 2):
        bars.append((x, Y0, x, Y1))
    fm = lines(W, H, [b for b in bars], 9, cap=False)
    art = OV(art, fm, lambda m: gouache_paint(m, "#f6f0e4", "#e8ddc9", seed=nx(), rough=0.6))
    art = OV(art, lines(W, H, [(b[0] + 3, b[1] + 4, b[2] + 3, b[3] + 4) for b in bars], 2.5, cap=False) * (1 - fm), lambda m: gouache_paint(m, "#6f6d86", seed=nx(), rough=0.5, density=0.5))
    # open shutters (louvred) left and right
    for sx0, sx1 in [(X0 - 150, X0 - 34), (X1 + 34, X1 + 150)]:
        sh = rect_m(W, H, sx0, Y0 - 6, sx1, Y1 - 4)
        art = OV(art, soft(sh, 8) * 0.5 * (xx > sx1 if sx0 < X0 else xx < sx0), lambda m: gouache_paint(m, "#bba989", seed=nx(), rough=2, density=0.6))
        art = OV(art, sh, lambda m: gouache_paint(m, SLATE, SLATE_L, seed=nx(), rough=1, streak=1.0))
        lou = lines(W, H, [(sx0 + 12, y, sx1 - 12, y + 3) for y in range(Y0 + 16, Y1 - 10, 14)], 3, cap=False)
        art = OV(art, lou, lambda m: gouache_paint(m, SLATE_D, seed=nx(), rough=0.5, density=0.8))
        art = OV(art, lines(W, H, [(sx0 + 12, y + 3, sx1 - 12, y + 6) for y in range(Y0 + 16, Y1 - 10, 14)], 1.6, cap=False), lambda m: gouache_paint(m, "#c3d0dc", seed=nx(), rough=0.4, density=0.8))
        art = OV(art, np.clip(sh - rect_m(W, H, sx0 + 8, Y0 + 2, sx1 - 8, Y1 - 12), 0, 1), lambda m: gouache_paint(m, SLATE_D, seed=nx(), rough=0.5))
    # balcony floor slab + shadow on the wall
    slab = rect_m(W, H, X0 - 70, Y1 - 6, X1 + 70, Y1 + 18)
    art = OV(art, slab, lambda m: gouache_paint(m, STONE_L, STONE_D, seed=nx(), rough=0.8))
    art = OV(art, rect_m(W, H, X0 - 64, Y1 + 18, X1 + 64, Y1 + 30), lambda m: gouache_paint(m, "#b8a27c", seed=nx(), rough=1, density=0.7))
    rail = railing_mask(W, H, X0 - 64, X1 + 64, Y1 - 150, Y1 - 6, 1.0)
    shadow = np.roll(np.roll(rail, 16, 0), 18, 1) * glass
    art = OV(art, soft(shadow, 1.5) * 0.35, lambda m: gouache_paint(m, "#4f4a6a", seed=nx(), rough=0.5, density=0.6))
    # flower pots on the slab (terracotta) with lilac + white blooms, behind the railing
    pots = []
    for px in (X0 - 30, X1 - 10):
        pots.append([(px, Y1 - 50), (px + 64, Y1 - 50), (px + 56, Y1 - 6), (px + 8, Y1 - 6)])
    art = OV(art, shapes(W, H, pots, smooth=False), lambda m: gouache_paint(m, "#c87a55", "#a85c3e", seed=nx(), rough=0.8))
    blooms = []
    for px in (X0 - 30, X1 - 10):
        for k in range(16):
            blooms.append((px + 32 + rng.gauss(0, 26), Y1 - 64 + rng.gauss(0, 14), rng.uniform(7, 12)))
    art = OV(art, circles(W, H, [(x, y + 6, r * 1.6) for x, y, r in blooms]), lambda m: gouache_paint(m, "#6f8c50", "#86a35e", seed=nx(), rough=2))
    art = OV(art, circles(W, H, blooms[::2]), lambda m: gouache_paint(m, "#c4a3dc", "#a986c9", seed=nx(), rough=1.5))
    art = OV(art, circles(W, H, blooms[1::2]), lambda m: gouache_paint(m, "#f6eef0", "#ead9e6", seed=nx(), rough=1.5))
    art = paint_iron(art, rail, nx)
    # wisteria: vine along the top of the surround with racemes cascading over the left shutter and top right
    vine = [curve([(20, 110), (140, 96), (260, 118), (380, 98), (520, 112), (660, 92)], 40), curve([(120, 100), (100, 220), (70, 330)], 20)]
    items = []
    for x in list(np.linspace(40, 640, 14)):
        y = 100 + 10 * math.sin(x / 40)
        if 250 < x < 430 and rng.random() < 0.6:
            continue
        items.append((x + rng.uniform(-10, 10), y, rng.uniform(110, 200) * (1.15 if x < 200 or x > 520 else 0.75), rng.uniform(-0.15, 0.15), rng.uniform(0.9, 1.15)))
    for y in (220, 300):
        items.append((86 + rng.uniform(-8, 8), y, rng.uniform(110, 160), rng.uniform(-0.1, 0.1), 0.9))
    art = paint_wisteria(art, W, H, items, nx, rng, vine=vine)
    # a few fallen petals on the slab
    art = OV(art, ellipses(W, H, [(rng.uniform(X0 - 50, X1 + 50), Y1 + 6 + rng.uniform(-4, 6), 4, 2.4, rng.uniform(0, 180)) for _ in range(12)]), lambda m: gouache_paint(m, LILAC[2], seed=nx(), rough=0.5))
    preview(art, "bp-window", tone="#f7f1e6")
    save(art, f"{OUT}/window.webp", max_w=560, quality=80)
    clear()

if "wisteria" in PARTS:
    W, H = 360, 520
    nx = Seq(31100)
    rng = random.Random(5)
    art = blank(W, H)
    vine = [curve([(-10, 30), (90, 22), (200, 40), (330, 26), (370, 30)], 30)]
    items = [(40, 30, 340, 0.05, 1.15), (110, 32, 420, -0.03, 1.2), (190, 38, 300, 0.06, 1.05), (260, 32, 380, -0.05, 1.15), (320, 28, 240, 0.08, 0.95), (150, 36, 200, 0.1, 0.9)]
    art = paint_wisteria(art, W, H, items, nx, rng, vine=vine)
    preview(art, "bp-wisteria", tone="#f7f1e6")
    save(art, f"{OUT}/wisteria.webp", max_w=260, quality=82)
    clear()

if "railing" in PARTS:
    W, H = 800, 200
    nx = Seq(32100)
    rng = random.Random(7)
    art = blank(W, H)
    rail = railing_mask(W, H, 20, 780, 50, 180, 0.9)
    art = paint_iron(art, rail, nx)
    items = [(x, 52, rng.uniform(70, 130), rng.uniform(-0.1, 0.1), 0.75) for x in (60, 120, 640, 700, 750)]
    vine = [curve([(10, 54), (100, 48), (200, 56)], 14), curve([(600, 54), (700, 46), (790, 54)], 14)]
    art = paint_wisteria(art, W, H, items, nx, rng, vine=vine)
    preview(art, "bp-railing", tone="#f7f1e6")
    save(art, f"{OUT}/railing.webp", max_w=640, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 260, 200
    nx = Seq(33100)
    rng = random.Random(9)
    art = blank(W, H)
    art = paint_wisteria(art, W, H, [(110, 24, 160, -0.35, 0.85), (150, 22, 120, 0.25, 0.75)], nx, rng, vine=[curve([(40, 30), (130, 18), (220, 28)], 12)])
    preview(art, "bp-sprig", tone="#f7f1e6")
    save(art, f"{OUT}/sprig.webp", max_w=150, quality=84)
    clear()

if "garland" in PARTS:
    # horizontal divider: a twig with leaves and three short hanging racemes
    W, H = 420, 130
    nx = Seq(35100)
    rng = random.Random(15)
    art = blank(W, H)
    art = paint_wisteria(art, W, H, [(150, 30, 80, 0.05, 0.62), (215, 32, 100, -0.02, 0.7), (280, 30, 74, 0.08, 0.6)], nx, rng,
                         vine=[curve([(30, 34), (120, 24), (220, 34), (310, 24), (390, 32)], 30)])
    preview(art, "bp-garland", tone="#f7f1e6")
    save(art, f"{OUT}/garland.webp", max_w=260, quality=84)
    clear()

if "awning" in PARTS:
    # scalloped café awning edge (repeat-x tile, 400 wide = 8 stripes)
    W, H = 400, 110
    nx = Seq(34100)
    art = blank(W, H)
    body = rect_m(W, H, -4, 0, W + 4, 70)
    scal = circles(W, H, [(25 + i * 50, 70, 25) for i in range(-1, 9)])
    m = np.maximum(body, scal * (np.mgrid[0:H, 0:W][0] > 60))
    stripes = np.zeros((H, W), np.float32)
    for i in range(8):
        if i % 2 == 0:
            stripes[:, i * 50:(i + 1) * 50] = 1
    art = OV(art, m * (1 - stripes), lambda mm: gouache_paint(mm, "#fbf5ea", "#f1e8da", seed=nx(), rough=0.8, streak=1.2), pad=0)
    art = OV(art, m * stripes, lambda mm: gouache_paint(mm, "#a986c9", "#9b78bd", seed=nx(), rough=0.8, streak=1.2), pad=0)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    shade = m * np.clip((yy - 40) / 40, 0, 1) * 0.25
    art = OV(art, shade, lambda mm: gouache_paint(mm, "#4f3f6a", seed=nx(), rough=0.5, density=0.5), pad=0)
    edge = np.clip(m - np.roll(m, -3, 0), 0, 1) * (yy > 50)
    art = OV(art, edge, lambda mm: gouache_paint(mm, "#cdbda6", seed=nx(), rough=0.3, density=0.9), pad=0)
    art = OV(art, rect_m(W, H, -4, 0, W + 4, 6), lambda mm: gouache_paint(mm, "#3a3442", seed=nx(), rough=0.3), pad=0)
    preview(art, "bp-awning", tone="#f7f1e6")
    save_full(art, f"{OUT}/awning.webp", size=(240, 66), quality=84)
    clear()

if "stone" in PARTS:
    S = 384
    n1 = wrap_noise(S, S, 3, 30); n2 = wrap_noise(S, S, 4, 0.9); n3 = wrap_noise(S, S, 5, 6)
    v = 0.97 + 0.04 * (n1 - .5) + 0.025 * (n2 - .5) + 0.02 * (n3 - .5)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    j = np.zeros((S, S), np.float32)
    for k in range(4):
        y = k * 96
        j = np.maximum(j, np.exp(-((yy - y) / 1.0) ** 2))
        off = 0 if k % 2 else 96
        for x in range(off, S + 192, 192):
            j = np.maximum(j, np.exp(-((xx - (x % S)) / 1.0) ** 2) * ((yy >= y) & (yy < y + 96)))
    v = v - 0.05 * j * (0.6 + 0.4 * n3)
    rgbv = np.clip(np.array(hex_rgb("#f2e8d6"), np.float32) * v[..., None], 0, 1)
    save_rgb(np.concatenate([rgbv, np.ones((S, S, 1), np.float32)], -1), f"{OUT}/stone.webp", quality=72)

kb(OUT)
