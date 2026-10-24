"""Ultah Donat — kids' donut party in gouache with coloured-pencil lines: a tower of glazed donuts stacked as a
birthday cake on a scalloped stand with a striped candle, a pegboard donut wall, single donuts (strawberry, chocolate,
vanilla), a three-donut divider and a seamless sprinkle-confetti tile.
Run: python3 -I ultah-donat.py [part ...]   parts: menara dinding donat taburan pita
Assets -> public/themes/art/ultah-donat/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t1_lib import *

OUT = outdir("ultah-donat")
PARTS = sys.argv[1:] or ["menara", "dinding", "donat", "taburan", "pita"]
DOUGH, DOUGH_D = "#e7ad6a", "#c98543"
LINE = "#6a3c2a"
GLAZES = {
    "stroberi": ("#f58fb3", "#e9739c"),
    "cokelat": ("#6e3b2a", "#57291c"),
    "vanila": ("#fff1c9", "#f6deaa"),
    "mint": ("#9fe3c9", "#7fd2b4"),
    "lilac": ("#c8adf2", "#b493e6"),
    "biru": ("#93d3f5", "#75bfe8"),
}
SPRINKLES = ["#ff5d8f", "#ffd23f", "#3fb8f0", "#7bcf4a", "#ffffff", "#a77bea", "#ff8c42"]


def sprinkle_items(rng, mask, n, L=7.0, wd=3.0):
    h, w = mask.shape
    ys, xs = np.where(mask > 0.8)
    out = {}
    if len(xs) == 0:
        return out
    for _ in range(n):
        i = rng.randrange(len(xs))
        x, y = xs[i], ys[i]
        a = rng.uniform(0, math.pi)
        c = rng.choice(SPRINKLES)
        out.setdefault(c, []).append(([(x - math.cos(a) * L / 2, y - math.sin(a) * L / 2), (x + math.cos(a) * L / 2, y + math.sin(a) * L / 2)], wd, None))
    return out


def add_sprinkles(art, mask, rng, n, L=7.0, wd=3.0):
    H, W = mask.shape
    for c, items in sprinkle_items(rng, mask, n, L, wd).items():
        m = strokes(W, H, items)
        art = GP(art, m, c, mix(c, "#000000", 0.08), seed=rs(), rough=0.4, streak=0.3, pad=4)
        art = tint(art, np.clip(m - np.roll(m, -1, 0), 0, 1), "#ffffff", 0.35, pad=2)
    return art


def wavy_ellipse(cx, cy, rx, ry, rng, amp=0.05, lobes=9, n=60):
    ph = rng.uniform(0, 6)
    return [(cx + math.cos(t) * rx * (1 + amp * math.sin(lobes * t + ph)), cy + math.sin(t) * ry * (1 + amp * math.sin(lobes * t + ph))) for t in np.linspace(0, 2 * math.pi, n)[:-1]]


def side_donut(art, W, H, cx, cy, rx, glaze, rng, hole=True, sprinkles=True, th=None):
    """3/4-view donut: dough torus + glaze with drips over the front edge. cy = centre of the top ellipse."""
    ry = rx * 0.42
    th = th or rx * 0.36
    dough = np.maximum(ellipses(W, H, [(cx, cy, rx, ry, 0), (cx, cy + th, rx * 0.98, ry, 0)]),
                       shapes(W, H, [[(cx - rx, cy), (cx + rx, cy), (cx + rx * 0.98, cy + th), (cx - rx * 0.98, cy + th)]], smooth=False))
    art = paint(art, dough, DOUGH, DOUGH_D, lc=LINE, px=1.3, dens=0.75)
    art = shade(art, dough * (np.mgrid[0:H, 0:W][0] > cy + th * 0.4), "#a8642c", 0.4, rough=2)
    g1, g2 = GLAZES[glaze]
    gp = wavy_ellipse(cx, cy - ry * 0.05, rx * 0.97, ry * 0.95, rng, 0.03, 7)
    gm = shapes(W, H, [gp])
    drips = []
    for k in range(rng.randint(4, 6)):
        t = rng.uniform(0.15, 0.85) * math.pi
        x = cx + math.cos(t) * rx * 0.9
        y = cy + math.sin(t) * ry * 0.9
        L = rng.uniform(0.25, 0.75) * th
        wd = rng.uniform(5, 9) * rx / 90
        drips.append([(x - wd, y - 4), (x + wd, y - 4), (x + wd * 0.8, y + L), (x, y + L + wd * 0.9), (x - wd * 0.8, y + L)])
    gm = np.maximum(gm, shapes(W, H, drips))
    art = paint(art, gm, g1, g2, lc=mix(g2, LINE, 0.5), px=1.1, dens=0.6)
    hm = None
    if hole:
        hm = ellipses(W, H, [(cx, cy, rx * 0.26, ry * 0.3, 0)])
        art = paint(art, hm, DOUGH_D, "#a8642c", lc=LINE, px=1.0, dens=0.7)
        art = tint(art, ellipses(W, H, [(cx, cy - ry * 0.1, rx * 0.2, ry * 0.18, 0)]), "#7a4426", 0.75, pad=4)
    # glossy glaze highlight
    art = tint(art, gaussian_filter(strokes(W, H, [(curve([(cx - rx * 0.62, cy - ry * 0.2), (cx - rx * 0.4, cy - ry * 0.62), (cx - rx * 0.1, cy - ry * 0.72)], 12), rx * 0.07, (0.3, 0.3))]), 1.2), "#ffffff", 0.55 if glaze != "vanila" else 0.8, pad=4)
    if sprinkles:
        area = gm.copy()
        if hm is not None:
            area = np.clip(area - gaussian_filter(hm, 3) * 3, 0, 1)
        area *= (np.mgrid[0:H, 0:W][0] < cy + ry * 0.75)
        art = add_sprinkles(art, area, rng, int(rx * 0.55), L=rx * 0.09, wd=rx * 0.038)
    clear()
    return art


def top_donut(art, W, H, cx, cy, r, glaze, rng, sprinkles=True, cut=True):
    dough = circles(W, H, [(cx, cy, r)])
    hole = circles(W, H, [(cx, cy, r * 0.3)])
    art = OV(art, np.clip(dough - hole, 0, 1), lambda m: soft_shadow(m, "#5a3020", 5, 0.3, 3, 5), pad=20)
    ring = np.clip(dough - hole, 0, 1)
    art = paint(art, ring, DOUGH, DOUGH_D, lc=LINE, px=1.2, dens=0.75)
    g1, g2 = GLAZES[glaze]
    gm = np.clip(shapes(W, H, [wavy_ellipse(cx, cy, r * 0.86, r * 0.86, rng, 0.06, 8)]) - circles(W, H, [(cx, cy, r * 0.38)]), 0, 1)
    art = paint(art, gm, g1, g2, lc=mix(g2, LINE, 0.5), px=1.0, dens=0.55)
    art = tint(art, gaussian_filter(strokes(W, H, [(arc_pts(cx, cy, r * 0.62, math.pi * 1.05, math.pi * 1.45, 10), r * 0.07, (0.3, 0.3))]), 1.0), "#ffffff", 0.55, pad=4)
    if cut:
        art[..., 3] *= 1 - np.clip(hole * 1.2, 0, 1)
    else:
        art = tint(art, hole, "#fbe3ea", 1.0, pad=4)
        art = tint(art, np.clip(hole - np.roll(gaussian_filter(hole, 2), 3, 0), 0, 1), "#c98fa0", 0.5, pad=4)
    if sprinkles:
        art = add_sprinkles(art, gm, rng, int(r * 0.7), L=r * 0.12, wd=r * 0.05)
    clear()
    return art


random.seed(61)

if "menara" in PARTS:
    W, H = 440, 800
    rng = random.Random(7)
    art = blank(W, H)
    cx = 220
    # cake stand: scalloped plate + pedestal
    ped = shapes(W, H, [[(cx - 34, 690), (cx + 34, 690), (cx + 22, 742), (cx + 70, 770), (cx + 72, 784), (cx - 72, 784), (cx - 70, 770), (cx - 22, 742)]])
    art = OV(art, ellipses(W, H, [(cx, 786, 110, 12, 0)]), lambda m: soft_shadow(m, "#5a3020", 6, 0.35, 0, 0), pad=30)
    art = paint(art, ped, "#c8adf2", "#ad8fe0", lc=LINE)
    plate = shapes(W, H, [[(cx - 196 + k * 28 + 14 + 14 * math.cos(a), 680 + 12 * math.sin(a)) for k in range(14) for a in np.linspace(math.pi, 0, 6)] + [(cx + 190, 690), (cx - 190, 690)]])
    plate = np.maximum(plate, ellipses(W, H, [(cx, 676, 196, 26, 0)]))
    art = paint(art, plate, "#ffffff", "#efe6fb", lc=LINE)
    art = shade(art, plate * (np.mgrid[0:H, 0:W][0] > 682), "#b493e6", 0.35)
    # stack (bottom to top, slightly smaller each level, a little wobble)
    levels = [(160, "cokelat"), (148, "stroberi"), (136, "vanila"), (124, "mint"), (110, "lilac")]
    y = 588
    for i, (rx, gl) in enumerate(levels):
        th = rx * 0.36
        art = side_donut(art, W, H, cx + rng.uniform(-6, 6), y, rx, gl, rng, hole=(i == len(levels) - 1))
        y -= th + rx * 0.22
    # candle in the top hole: striped, with a flame
    top_y = y + levels[-1][0] * 0.36 + levels[-1][0] * 0.22
    cm = shapes(W, H, [[(cx - 9, top_y - 4), (cx + 9, top_y - 4), (cx + 9, top_y - 110), (cx - 9, top_y - 110)]], smooth=False)
    art = paint(art, cm, "#ffffff", "#f3eef8", lc=LINE, px=1.0)
    stripes = shapes(W, H, [[(cx - 9, top_y - 20 - k * 22), (cx + 9, top_y - 30 - k * 22), (cx + 9, top_y - 38 - k * 22), (cx - 9, top_y - 28 - k * 22)] for k in range(4)], smooth=False) * cm
    art = GP(art, stripes, "#ff5d8f", "#f2477d", seed=rs(), rough=0.5)
    art = tint(art, strokes(W, H, [([(cx, top_y - 110), (cx + 1, top_y - 122)], 2.0, None)]), "#3a2418", 1, pad=2)
    fl = shapes(W, H, [[(cx, top_y - 168), (cx + 12, top_y - 140), (cx + 9, top_y - 126), (cx, top_y - 120), (cx - 9, top_y - 126), (cx - 12, top_y - 140)]])
    art = OV(art, fl, lambda m: glow(m, "#ffcf5a", 16, 0.7), pad=110)
    art = paint(art, fl, "#ffb72e", "#ff8c2e", lc="#c25a10", px=0.9, dens=0.5)
    art = GP(art, shapes(W, H, [[(cx, top_y - 152), (cx + 5, top_y - 136), (cx, top_y - 128), (cx - 5, top_y - 136)]]), "#fff3b0", seed=rs(), rough=0.4)
    save(art, f"{OUT}/menara.webp", max_w=400, quality=82)
    prev(art, "ud_menara", bg="#c9efe0")

if "dinding" in PARTS:
    W, H = 780, 500
    rng = random.Random(11)
    art = blank(W, H)
    board = shapes(W, H, [[(30, 40), (750, 40), (750, 470), (30, 470)]], smooth=False)
    board = np.clip(gaussian_filter(displace(board, 3, 1.5, 20), 0.6), 0, 1)
    art = OV(art, board, lambda m: soft_shadow(m, "#3a5a50", 10, 0.35, 0, 10), pad=30)
    art = paint(art, board, "#fff4f7", "#fde7ee", lc=LINE, px=1.4)
    # pastel candy stripes at the top header
    hdr = shapes(W, H, [[(30, 40), (750, 40), (750, 96), (30, 96)]], smooth=False) * board
    for k in range(0, 26):
        sm = shapes(W, H, [[(30 + k * 30, 40), (50 + k * 30, 40), (30 + k * 30, 96), (10 + k * 30, 96)]], smooth=False) * hdr
        art = GP(art, sm, ["#f58fb3", "#ffe7a3", "#9fe3c9", "#c8adf2"][k % 4], seed=rs(), rough=0.6, streak=0.4, pad=4)
    art = line(art, hdr, 1.2, 0.7, LINE)
    # scalloped awning edge under the header
    scal = shapes(W, H, [[(30 + k * 36, 94)] + [(30 + k * 36 + 18 - 18 * math.cos(a), 94 + 16 * math.sin(a)) for a in np.linspace(0, math.pi, 9)] + [(30 + k * 36 + 36, 94)] for k in range(20)]) * (np.mgrid[0:H, 0:W][1] < 750)
    art = paint(art, scal, "#ffffff", "#f4f0f8", lc=LINE, px=1.1)
    # pegboard holes
    holes = circles(W, H, [(x, y, 3) for x in range(60, 740, 34) for y in range(140, 460, 34)])
    art = tint(art, holes, "#d9b9c4", 0.8, pad=2)
    clear()
    # rows of donuts hanging on pegs
    glz = ["stroberi", "cokelat", "vanila", "mint", "lilac", "biru"]
    k = 0
    for row, y in enumerate([196, 316, 424]):
        xs = [118, 272, 426, 580, 700] if row != 1 else [190, 345, 500, 650]
        for x in xs:
            r = 52 if row != 2 else 44
            art = top_donut(art, W, H, x + rng.uniform(-4, 4), y + rng.uniform(-3, 3), r, glz[k % len(glz)], rng, cut=False)
            peg = shapes(W, H, [[(x - 5, y - r * 0.32), (x + 5, y - r * 0.32), (x + 5, y - r * 0.32 + 12), (x - 5, y - r * 0.32 + 12)]], smooth=False)
            art = paint(art, peg, "#d9a36a", "#b97f48", lc=LINE, px=0.8)
            k += 1
    save(art, f"{OUT}/dinding.webp", max_w=780, quality=78)
    prev(art, "ud_dinding", bg="#c9efe0")

if "donat" in PARTS:
    for name, gl, seed in (("donat", "stroberi", 3), ("donat2", "cokelat", 5), ("donat3", "vanila", 9)):
        W, H = 220, 220
        art = top_donut(blank(W, H), W, H, 110, 106, 92, gl, random.Random(seed))
        save(art, f"{OUT}/{name}.webp", max_w=180, quality=84)
        prev(art, f"ud_{name}", bg="#c9efe0")

if "pita" in PARTS:
    # divider: three mini donuts on a dotted sprinkle line
    W, H = 420, 110
    rng = random.Random(4)
    art = blank(W, H)
    dots = []
    for x in range(10, 410, 14):
        if abs(x - 210) < 150 and (abs(x - 110) < 46 or abs(x - 210) < 46 or abs(x - 310) < 46):
            continue
        c = SPRINKLES[(x // 14) % len(SPRINKLES[:-1])]
        dots.append((c, ([(x - 4, 56 + 3 * math.sin(x)), (x + 4, 54 - 3 * math.sin(x))], 4.0, None)))
    for c in set(c for c, _ in dots):
        art = GP(art, strokes(W, H, [it for cc, it in dots if cc == c]), c, seed=rs(), rough=0.4, pad=4)
    for x, gl in ((110, "mint"), (210, "stroberi"), (310, "lilac")):
        art = top_donut(art, W, H, x, 55, 40 if x == 210 else 34, gl, rng)
    save(art, f"{OUT}/pita.webp", quality=84)
    prev(art, "ud_pita", bg="#fff7e8")

if "taburan" in PARTS:
    # seamless sprinkle confetti tile (sparse) for section backgrounds
    T = 320
    rng = random.Random(8)
    art = blank(T, T)
    items = {}
    for _ in range(30):
        x, y = rng.uniform(0, T), rng.uniform(0, T)
        a = rng.uniform(0, math.pi); L = rng.uniform(9, 13); c = rng.choice(SPRINKLES[:-1] + ["#ff5d8f"])
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                items.setdefault(c, []).append(([(x + dx - math.cos(a) * L / 2, y + dy - math.sin(a) * L / 2), (x + dx + math.cos(a) * L / 2, y + dy + math.sin(a) * L / 2)], 4.2, None))
    for c, it in items.items():
        art = GP(art, strokes(T, T, it), c, mix(c, "#000000", .08), seed=rs(), rough=0.3, streak=0.3, pad=2)
    art[..., 3] *= 0.55
    save_full(art, f"{OUT}/taburan.webp", quality=82)
    prev(art, "ud_taburan", bg="#fff7e8")

kb(OUT)
