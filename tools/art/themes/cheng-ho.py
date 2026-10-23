"""Cheng Ho — a Chinese-style Indonesian mosque (architecture only): three tiers of jade-green pagoda roofs with
upturned eaves and red ridges, vermilion walls and columns, lattice windows, a moon-arched door, stone platform,
side halls, a gold finial with a small crescent. Gouache with ink contours. Also: a round red lantern, a gold
auspicious-cloud divider, a red lattice corner. Run: python3 -I cheng-ho.py [part ...]
parts: masjid lantern cloud lattice"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k1_lib import *  # noqa

OUT = outdir("cheng-ho")
PARTS = sys.argv[1:] or ["masjid", "lantern", "cloud", "lattice"]
VERM, VERM_D, VERM_L = "#b8322a", "#7c1a16", "#d5503c"
JADE, JADE_D, JADE_L = "#2f6d57", "#1c4a3a", "#5e9a7c"
GOLD, GOLD_D = "#d6a64a", "#94701f"
STONE, STONE_D = "#c9bfac", "#8f8573"
INK = "#2a1f1a"
CREAM = "#f5ecd9"


def roof_pts(cx, ey, ew, tw, th, lift):
    """Pagoda roof: concave slopes, eave line that sweeps up at both tips (swallow-tail)."""
    L = curve([(cx - ew, ey - lift), (cx - ew * 0.86, ey - lift * 0.25), (cx - ew * 0.6, ey + 2), (cx, ey + 4)], 18)
    R = [(2 * cx - x, y) for x, y in L[::-1]]
    sl = curve([(cx - tw, ey - th), (cx - (tw + ew) * 0.5 - ew * 0.06, ey - th * 0.35), (cx - ew, ey - lift)], 14)
    sr = [(2 * cx - x, y) for x, y in sl[::-1]]
    return L + R[1:] + sr[1:] + sl[:-1]


def roof(art, W, H, cx, ey, ew, tw, th, lift, nx, rng):
    pts = roof_pts(cx, ey, ew, tw, th, lift)
    m = shapes(W, H, [pts], smooth=False)
    art = GP(art, m, JADE, JADE_D, seed=nx(), rough=1.2, streak=0.9)
    # glazed tile rows: lines running down the slope, converging to the ridge
    rows = []
    for k in range(-26, 27):
        t = k / 26
        x0 = cx + t * tw; x1 = cx + t * ew * 1.02
        rows.append(([(x0, ey - th), ((x0 + x1) / 2 + t * 6, ey - th * 0.35), (x1, ey + 2 - abs(t) ** 3 * lift)], 1.3, None))
    art = G(art, strokes(W, H, rows) * m, JADE_D, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    hi = np.clip(m - np.roll(m, 6, 0), 0, 1)
    rside = m * np.clip((np.mgrid[0:H, 0:W][1] - cx) / ew, 0, 1)
    art = G(art, rside, JADE_D, seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    art = G(art, gaussian_filter(m, 3) * np.clip(1 - np.abs(np.mgrid[0:H, 0:W][1] - cx) / (ew * 0.9), 0, 1) * m * 0.6, JADE_L, seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    # red ridge + eave fascia, gold tips
    eave = strokes(W, H, [(curve([(cx - ew, ey - lift), (cx - ew * 0.86, ey - lift * 0.25), (cx - ew * 0.6, ey + 2), (cx, ey + 4), (cx + ew * 0.6, ey + 2), (cx + ew * 0.86, ey - lift * 0.25), (cx + ew, ey - lift)], 50), 6, (0.03, 0.03))])
    ridge = strokes(W, H, [([(cx - tw - 4, ey - th), (cx + tw + 4, ey - th)], 7, None)] +
                    [(curve([(cx + s_ * tw, ey - th), (cx + s_ * ((tw + ew) * 0.5 + ew * 0.06), ey - th * 0.35), (cx + s_ * ew, ey - lift)], 20), 4, (0.05, 0.1)) for s_ in (-1, 1)])
    art = GP(art, np.maximum(eave, ridge), VERM, VERM_D, seed=nx(), rough=0.6, pad=8)
    tips = circles(W, H, [(cx - ew, ey - lift - 3, 5), (cx + ew, ey - lift - 3, 5)])
    art = FO(art, tips, GOLD, seed=nx(), emboss=0.7)
    art = ink(art, outline(np.maximum(m, eave), 1.6), INK, 0.75, seed=nx())
    return art, m


def wall(art, W, H, x0, x1, y0, y1, nx, cols=4, door=False, windows=True):
    m = shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)
    art = GP(art, m, VERM, VERM_L, seed=nx(), rough=0.8, streak=1.0)
    # shadow under the eave
    sh = m * np.clip(1 - (np.mgrid[0:H, 0:W][0] - y0) / 26.0, 0, 1)
    art = G(art, sh, VERM_D, "#4a0e0b", seed=nx(), density=0.6, edge=0, bloom=0.2, rough=1)
    side = m * np.clip((np.mgrid[0:H, 0:W][1] - (x0 + (x1 - x0) * 0.55)) / ((x1 - x0) * 0.45), 0, 1)
    art = G(art, side, VERM_D, seed=nx(), density=0.32, edge=0, bloom=0.35, rough=2)
    # columns (darker red with a gold capital), green lintel
    xs = np.linspace(x0 + 6, x1 - 6, cols)
    colm = strokes(W, H, [([(x, y0 + 4), (x, y1)], 9, None) for x in xs])
    art = GP(art, colm, VERM_D, "#5e130f", seed=nx(), rough=0.5, pad=8)
    caps = shapes(W, H, [[(x - 9, y0 + 8), (x + 9, y0 + 8), (x + 6, y0 + 16), (x - 6, y0 + 16)] for x in xs], smooth=False)
    art = FO(art, caps, GOLD, seed=nx(), emboss=0.6)
    lint = shapes(W, H, [[(x0, y0 + 2), (x1, y0 + 2), (x1, y0 + 9), (x0, y0 + 9)]], smooth=False)
    art = GP(art, lint, JADE_D, seed=nx(), rough=0.4, pad=6)
    # lattice windows between columns
    if windows:
        for i in range(len(xs) - 1):
            a, b = xs[i] + 12, xs[i + 1] - 12
            if door and i == (len(xs) - 1) // 2:
                continue
            if b - a < 14:
                continue
            wy0, wy1 = y0 + 26, min(y1 - 16, y0 + 26 + (b - a) * 1.25)
            wm = shapes(W, H, [[(a, wy0), (b, wy0), (b, wy1), (a, wy1)]], smooth=False)
            art = GP(art, wm, "#3a1410", "#24100c", seed=nx(), rough=0.4, pad=6)
            lat = []
            for xx in np.linspace(a + 3, b - 3, 4):
                lat.append(([(xx, wy0 + 2), (xx, wy1 - 2)], 1.6, None))
            for yy in np.linspace(wy0 + 3, wy1 - 3, max(3, int((wy1 - wy0) / 9))):
                lat.append(([(a + 2, yy), (b - 2, yy)], 1.6, None))
            art = GP(art, strokes(W, H, lat) * wm, GOLD_D, "#b38a3a", seed=nx(), rough=0.3, pad=6)
            art = GP(art, outline(wm, 2.4), JADE_D, seed=nx(), rough=0.3, pad=6)
    if door:
        i = (len(xs) - 1) // 2
        a, b = xs[i] + 10, xs[i + 1] - 10
        dcx = (a + b) / 2; r = (b - a) / 2
        dm = shapes(W, H, [[(a, y1)] + arc_pts(dcx, y0 + 30 + r, r, math.pi, math.tau, 20) + [(b, y1)]], smooth=False)
        art = GP(art, dm, "#2a0e0b", "#170807", seed=nx(), rough=0.4, pad=6)
        art = FO(art, outline(dm, 3.2), GOLD, seed=nx(), emboss=0.7)
        # warm light inside
        art = G(art, np.clip(1 - gaussian_filter(1 - dm, 10) * 2.2, 0, 1) * dm, "#d99a48", seed=nx(), density=0.55, edge=0, bloom=0.3, rough=1)
    art = ink(art, outline(m, 1.4), INK, 0.6, seed=nx())
    return art


if "masjid" in PARTS:
    W, H = 820, 700
    nx = Seq(40100); rng = random.Random(8)
    art = blank(W, H)
    cx = W / 2
    # ground shadow + stone platform with steps
    art = G(art, shapes(W, H, [deform(ellipse_pts(cx, 662, 380, 22, 20), rng, 1, 0.03)]), "#3a2a20", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=4, feather=6)
    plat = shapes(W, H, [[(50, 612), (770, 612), (784, 652), (36, 652)]], smooth=False)
    art = GP(art, plat, STONE, "#d8cfbd", seed=nx(), rough=1.0, streak=1.0)
    steps = strokes(W, H, [([(cx - 90 + k * 8, 620 + k * 9), (cx + 90 - k * 8, 620 + k * 9)], 2, None) for k in range(4)] + [([(60, 622), (760, 622)], 1.4, None)])
    art = G(art, steps, STONE_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    art = ink(art, outline(plat, 1.4), INK, 0.55, seed=nx())
    # side halls
    for sgn in (-1, 1):
        wx = cx + sgn * 250
        art = wall(art, W, H, wx - 92, wx + 92, 506, 612, nx, cols=4, windows=True)
        art, _ = roof(art, W, H, wx, 508, 128, 70, 44, 18, nx, rng)
    # main hall
    art = wall(art, W, H, cx - 150, cx + 150, 432, 612, nx, cols=5, door=True)
    art, r1 = roof(art, W, H, cx, 434, 214, 116, 62, 30, nx, rng)
    art = wall(art, W, H, cx - 96, cx + 96, 324, 376, nx, cols=4, windows=True)
    art, r2 = roof(art, W, H, cx, 326, 150, 64, 54, 26, nx, rng)
    art = wall(art, W, H, cx - 54, cx + 54, 236, 274, nx, cols=3, windows=True)
    # top roof: pyramidal (octagonal look) to a point
    art, r3 = roof(art, W, H, cx, 238, 106, 6, 82, 24, nx, rng)
    # gold finial + small crescent
    fin = np.maximum.reduce([
        strokes(W, H, [([(cx, 160), (cx, 108)], 5, (0.0, 0.3))]),
        circles(W, H, [(cx, 150, 9), (cx, 130, 7)]),
    ])
    cres = np.clip(circles(W, H, [(cx, 92, 13)]) - circles(W, H, [(cx + 6, 88, 11)]), 0, 1)
    art = FO(art, np.maximum(fin, cres), GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    art = ink(art, outline(np.maximum(fin, cres), 1.2), GOLD_D, 0.6, seed=nx())
    prev(art, "ch-masjid", bg=CREAM)
    save(art, f"{OUT}/masjid.webp", max_w=640, quality=82)
    clear()


if "lantern" in PARTS:
    W, H = 200, 380
    nx = Seq(40200); rng = random.Random(2)
    art = blank(W, H)
    cx = 100
    art = GP(art, strokes(W, H, [([(cx, 0), (cx, 92)], 2.4, None)]), INK, seed=nx(), rough=0.3, pad=6)
    body = shapes(W, H, [deform(ellipse_pts(cx, 190, 82, 92, 24), rng, 1, 0.02)])
    art = G(art, glow(body, "#ff9a4a", 22, 0.5)[..., 3] * 0.7, "#ff8a3a", seed=nx(), density=0.4, edge=0, bloom=0, rough=4, feather=8)
    art = GP(art, body, VERM, VERM_L, seed=nx(), rough=1.0, streak=0.8)
    # inner glow and ribs
    art = G(art, gaussian_filter(circles(W, H, [(cx - 12, 180, 46)]), 14) * body, "#f6a14a", seed=nx(), density=0.55, edge=0, bloom=0.3, rough=2)
    ribs = strokes(W, H, [(arc_pts(cx, 190, 82 * k, -math.pi / 2, math.pi / 2, 30, 92 / 82 / max(k, .01) * k) if False else
                           [(cx + 82 * k * math.sin(t), 190 - 92 * math.cos(t)) for t in np.linspace(0, math.pi, 30)], 1.6, None) for k in (-0.85, -0.5, -0.15, 0.2, 0.55, 0.88)])
    art = G(art, ribs * body, VERM_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    caps = shapes(W, H, [[(cx - 40, 98), (cx + 40, 98), (cx + 34, 114), (cx - 34, 114)], [(cx - 40, 282), (cx + 40, 282), (cx + 34, 266), (cx - 34, 266)]], smooth=False)
    art = FO(art, caps, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    tas = strokes(W, H, [([(cx + dx, 284), (cx + dx * 1.3, 360 + abs(dx) * -0.6)], 2.2, (0.0, 0.6)) for dx in range(-12, 13, 3)])
    art = GP(art, tas, VERM, VERM_D, seed=nx(), rough=0.4, pad=6)
    art = FO(art, circles(W, H, [(cx, 290, 8)]), GOLD, seed=nx(), emboss=0.8)
    art = ink(art, outline(body, 1.2), INK, 0.5, seed=nx())
    prev(art, "ch-lantern", bg=CREAM)
    save(art, f"{OUT}/lantern.webp", max_w=110, quality=84)
    clear()


if "cloud" in PARTS:
    W, H = 520, 130
    nx = Seq(40300)
    art = blank(W, H)
    cx, cy = W / 2, 70
    items = []
    for sgn in (-1, 1):
        # auspicious cloud scroll: a long tail with two curls, mirrored
        items.append((curve([(cx + sgn * 30, cy + 10), (cx + sgn * 120, cy + 14), (cx + sgn * 200, cy + 4), (cx + sgn * 236, cy - 10)], 30), 4.2, (0.0, 0.5)))
        items.append((spiral_pts(cx + sgn * 56, cy - 6, 30, 5, math.pi / 2, 1.1, 40, -sgn), 4.2, (0.0, 0.5)))
        items.append((spiral_pts(cx + sgn * 128, cy - 2, 20, 4, math.pi / 2, 1.0, 34, -sgn), 3.6, (0.0, 0.5)))
        items.append((spiral_pts(cx + sgn * 176, cy + 2, 13, 3, math.pi / 2, 0.9, 28, -sgn), 3.0, (0.0, 0.5)))
    m = strokes(W, H, items)
    dia = shapes(W, H, [[(cx, cy - 22), (cx + 14, cy - 6), (cx, cy + 10), (cx - 14, cy - 6)]], smooth=False)
    art = FO(art, m, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    art = GP(art, dia, VERM, VERM_D, seed=nx(), rough=0.4, pad=6)
    art = FO(art, outline(dia, 2.4), GOLD, seed=nx())
    prev(art, "ch-cloud", bg=CREAM)
    save(art, f"{OUT}/cloud.webp", max_w=300, quality=84)


if "lattice" in PARTS:
    # red lacquer corner of a Chinese window lattice (fret pattern), L-shaped
    W, H = 320, 320
    nx = Seq(40400)
    art = blank(W, H)
    g = 16
    items = []
    for i in range(0, 20):
        x = 8 + i * g
        items.append(([(x, 8), (x, 8 + g * 3)], 4, None)) if i % 2 == 0 else None
        items.append(([(8, x), (8 + g * 3, x)], 4, None)) if i % 2 == 0 else None
    # fret (huiwen) running border
    fret = []
    for k in range(9):
        x = 14 + k * 34
        fret += [(x, 14), (x + 28, 14), (x + 28, 40), (x + 8, 40), (x + 8, 24), (x + 18, 24)]
    vfret = [(y, x) for x, y in fret]
    m = strokes(W, H, [(fret, 4.5, None), (vfret, 4.5, None), ([(4, 52), (W - 4, 52)], 3, None), ([(52, 4), (52, H - 4)], 3, None), ([(4, 4), (W - 4, 4)], 6, None), ([(4, 4), (4, H - 4)], 6, None)])
    # fade the arms towards their ends
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    m *= np.clip(1.25 - np.maximum(xx, yy) / W, 0, 1)
    art = GP(art, m, VERM, VERM_D, seed=nx(), rough=0.5, pad=8)
    art = FO(art, circles(W, H, [(52, 52, 7)]), GOLD, seed=nx(), emboss=0.8)
    prev(art, "ch-lattice", bg=CREAM)
    save(art, f"{OUT}/lattice.webp", max_w=170, quality=84)
