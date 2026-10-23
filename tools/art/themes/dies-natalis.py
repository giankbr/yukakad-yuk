"""Dies Natalis — academic anniversary: an original crest (teal enamel shield with open book, torch and waves, gold-foil
rim, laurel and vermilion scroll), a copperplate-engraved campus building with a clock tower, a gold satin ribbon
banner, a foil laurel divider, and a gold foil texture for the big anniversary number.
Run: python3 -I dies-natalis.py [part ...]   parts: crest campus ribbon laurel foil"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l4_lib import *

OUT = outdir("dies-natalis")
PARTS = sys.argv[1:] or ["crest", "campus", "ribbon", "laurel", "foil"]
TEAL, TEAL_D, TEAL_L = "#1d4a52", "#123238", "#2f6a72"
GOLD = "#c9a24c"
VERM, VERM_D = "#b03a2e", "#7e2219"
IVORY = "#f4ecd8"
INK = "#173b41"


def laurel_masks(W, H, cx, cy, r, a0, a1, side, leaf_l, leaf_w, n):
    """One laurel branch along an arc from a0 (bottom) to a1 (top); side=-1 left, +1 right. Returns (stem, leaves)."""
    pts = [(cx + side * math.cos(a) * r, cy + math.sin(a) * r) for a in np.linspace(a0, a1, 40)]
    stem = strokes(W, H, [(pts, max(2.5, leaf_w * .3), (.05, .3))])
    leaves = []
    for i in range(n):
        t = .06 + .9 * i / (n - 1)
        a = a0 + (a1 - a0) * t
        x, y = cx + side * math.cos(a) * r, cy + math.sin(a) * r
        travel = math.atan2(-math.cos(a), side * math.sin(a))
        ln = leaf_l * (1 - .35 * t)
        for k in (-1, 1):
            leaves.append(petal_pts(x, y, ln, leaf_w * (1 - .3 * t), travel + k * .6, n=12))
    return stem, shapes(W, H, leaves)


# ---------------------------------------------------------------- crest (500x600 -> 220)
if "crest" in PARTS:
    W, H = 500, 600
    nx = Seq(901000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = blank(W, H)
    cx = 250
    def shield(inset):
        top, bot = 120 + inset, 450 - inset * 1.4
        l, r = 140 + inset, 360 - inset
        pts = [(l, top), (cx, top - 14 + inset * .3), (r, top)] + [(r, top + (bot - top) * .45)] + \
              [(cx + (r - cx) * math.cos(t), top + (bot - top) * .45 + (bot - top) * .55 * math.sin(t)) for t in np.linspace(0, math.pi / 2, 10)] + \
              [(cx - (cx - l) * math.cos(t), top + (bot - top) * .45 + (bot - top) * .55 * math.sin(t)) for t in np.linspace(math.pi / 2, 0, 10)] + [(l, top + (bot - top) * .45)]
        return shapes(W, H, [pts], smooth=False)
    outer, inner = shield(0), shield(12)
    # laurel around the shield
    for side in (-1, 1):
        st, lv = laurel_masks(W, H, cx, 300, 180, math.pi * .62, math.pi * -.2, side, 56, 11, 10)
        a = FO(a, np.maximum(st, lv), "#c29b48", seed=nx(), emboss=.8, sparkle=.15)
        a = G(a, lv * (yy > 300), "#7a5a22", seed=nx(), density=.22, edge=.15, rough=1.5)
    a = FO(a, outer, "#cfa851", seed=nx(), emboss=.9, sparkle=.2)
    a = OV(a, inner, lambda m: gouache_paint(m, TEAL, TEAL_L, seed=nx(), rough=1, streak=1.2))
    a = G(a, inner * np.clip((xx - 250) / 110, 0, 1), TEAL_D, seed=nx(), density=.45, edge=.1, rough=2)
    # waves (maritime) in the lower field
    wv = strokes(W, H, [([(x, y0 + 7 * math.sin((x - 150) / 18)) for x in range(150, 352, 4)], 5, None) for y0 in (372, 394)]) * inner
    a = FO(a, wv, "#d8b55e", seed=nx(), emboss=.5)
    # open book
    book = shapes(W, H, [[(166, 300), (200, 288), (246, 296), (250, 302), (254, 296), (300, 288), (334, 300), (334, 348), (300, 338), (254, 346), (250, 352), (246, 346), (200, 338), (166, 348)]])
    a = OV(a, book, lambda m: gouache_paint(m, IVORY, "#e8dcc0", seed=nx(), rough=.8))
    lines = strokes(W, H, [([(178 + (i % 4) * 0, 306 + i * 9), (238, 312 + i * 9)], 1.6, None) for i in range(4)] + [([(262, 312 + i * 9), (322, 306 + i * 9)], 1.6, None) for i in range(4)])
    a = OV(a, lines, lambda m: gouache_paint(m, "#8d8270", seed=nx(), rough=.3, density=.8))
    spine = strokes(W, H, [([(250, 300), (250, 352)], 2.2, None)])
    a = OV(a, spine, lambda m: gouache_paint(m, "#6f6656", seed=nx(), rough=.3))
    # torch above the book
    handle = shapes(W, H, [[(242, 284), (258, 284), (254, 228), (246, 228)]], smooth=False)
    a = FO(a, handle, "#cfa851", seed=nx(), emboss=.8)
    cup = shapes(W, H, [[(232, 222), (268, 222), (260, 236), (240, 236)]], smooth=False)
    a = FO(a, cup, "#d8b55e", seed=nx(), emboss=.8)
    flame = shapes(W, H, [[(250, 150), (266, 182), (270, 206), (260, 222), (240, 222), (230, 204), (236, 186), (244, 194)]])
    a = OV(a, flame, lambda m: gouache_paint(m, VERM, "#d4612f", seed=nx(), rough=1))
    fin = shapes(W, H, [[(250, 176), (258, 196), (256, 216), (244, 216), (242, 198)]])
    a = OV(a, fin, lambda m: gouache_paint(m, "#f0b44a", "#f6cf73", seed=nx(), rough=.6))
    # star above the shield
    star = [(cx + math.cos(-math.pi / 2 + k * math.pi / 5) * (26 if k % 2 == 0 else 11), 66 + math.sin(-math.pi / 2 + k * math.pi / 5) * (26 if k % 2 == 0 else 11)) for k in range(10)]
    a = FO(a, shapes(W, H, [star], smooth=False), "#d8b55e", seed=nx(), emboss=.9, sparkle=.3)
    # vermilion scroll below
    scroll = shapes(W, H, [[(110, 470), (390, 470), (402, 500), (390, 530), (110, 530), (98, 500)]], smooth=False)
    tails = shapes(W, H, [[(110, 482), (62, 486), (80, 512), (62, 540), (122, 536)], [(390, 482), (438, 486), (420, 512), (438, 540), (378, 536)]], smooth=False)
    a = OV(a, tails, lambda m: gouache_paint(m, VERM_D, "#6a1c14", seed=nx(), rough=.8))
    a = OV(a, scroll, lambda m: gouache_paint(m, VERM, "#a33328", seed=nx(), rough=.8, streak=1.3))
    edge = strokes(W, H, [([(112, 476), (388, 476)], 2, None), ([(112, 524), (388, 524)], 2, None)])
    a = FO(a, edge, "#d8b55e", seed=nx(), emboss=.4)
    dots = circles(W, H, [(150 + i * 25, 500, 3.2) for i in range(9)])
    a = FO(a, dots, "#e3c46f", seed=nx(), emboss=.4)
    save(a, f"{OUT}/crest.webp", max_w=240)
    prev(a, "dn-crest", bg="#f4ecd8")
    clear()

# ---------------------------------------------------------------- campus (engraving, 1000x500 -> 760)
if "campus" in PARTS:
    W, H = 1000, 500
    nx = Seq(911000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    GL = 430
    rects = lambda items: shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)] for x0, y0, x1, y1 in items], smooth=False)
    wings = rects([(150, 270, 850, GL)])
    tower = rects([(450, 110, 550, GL)])
    towercap = shapes(W, H, [[(440, 112), (500, 40), (560, 112)]], smooth=False)
    pediment = shapes(W, H, [[(360, 270), (500, 196), (640, 270)]], smooth=False)
    portico = rects([(370, 270, 630, GL)])
    roof = shapes(W, H, [[(136, 272), (170, 244), (830, 244), (864, 272)]], smooth=False)
    steps = rects([(350, GL - 6, 650, GL + 8), (330, GL + 8, 670, GL + 20)])
    building = np.maximum.reduce([wings, tower, towercap, pediment, portico, roof, steps])
    # tone map (0 light .. 1 dark), light from the upper left
    tone = np.zeros((H, W), np.float32)
    tone += wings * .3
    tone = np.maximum(tone, roof * .62)
    tone = np.where(tower > .5, .26, tone)
    tone = np.where(towercap > .5, .55 + .3 * (xx > 500), tone)
    tone = np.where(pediment > .5, .3, tone)
    tone = np.where(portico > .5, .5, tone)
    cols = rects([(380 + i * 34, 282, 394 + i * 34, GL - 6) for i in range(8)])
    tone = np.where(cols > .5, .12 + .25 * ((xx - 380) % 34 > 9), tone)
    wins = rects([(170 + i * 42, 300, 194 + i * 42, 346) for i in range(5)] + [(170 + i * 42, 366, 194 + i * 42, 412) for i in range(5)] +
                 [(642 + i * 42, 300, 666 + i * 42, 346) for i in range(5)] + [(642 + i * 42, 366, 666 + i * 42, 412) for i in range(5)])
    tone = np.where(wins > .5, .82, tone)
    clock = circles(W, H, [(500, 150, 24)])
    tone = np.where(clock > .5, .04, tone)
    tw = rects([(478, 190, 522, 250)])
    tone = np.where(tw > .5, .85, tone)
    tone = np.where(steps > .5, .1 + .2 * ((yy - GL) % 14 > 7), tone)
    tone *= building
    sh = (xx > 820) * wings  # right edge in shade
    tone = np.maximum(tone, sh * .45)
    ink = engrave(building, tone, angle=1.57, spacing=4.2, seed=nx(), cross=.55)
    ink2 = engrave(roof, tone * roof, angle=.35, spacing=3.6, seed=nx(), cross=None)
    ink = np.maximum(ink * (1 - roof * .7), ink2)
    # outlines
    def outline(m):
        return np.clip(m - gaussian_filter(m, 1.0) * 1.0, 0, 1) * 3
    line = np.clip(sum(outline(m) for m in [wings, tower, towercap, pediment, portico, roof, wins, cols, clock, steps]), 0, 1)
    hands = strokes(W, H, [([(500, 150), (500, 134)], 2.4, None), ([(500, 150), (512, 156)], 2.4, None)])
    # trees either side (engraved crowns) + lawn hatching
    trees = circles(W, H, [(70, 330, 70), (120, 370, 56), (930, 330, 72), (880, 372, 54), (30, 390, 46), (970, 392, 44)])
    trunks = rects([(66, 380, 78, GL), (926, 380, 938, GL)])
    ttone = trees * (.35 + .5 * np.clip((xx - 60) / 140, 0, 1) * (xx < 300) + .5 * np.clip((xx - 860) / 140, 0, 1) * (xx > 700)) * (0.7 + .6 * fbm(W, H, nx(), 14, 3))
    tink = engrave(trees, np.clip(ttone, 0, 1), angle=.8, spacing=3.6, seed=nx(), cross=.6)
    lawn = ((yy > GL) & (yy < GL + 50)).astype(np.float32) * np.clip(1 - np.abs(xx - 500) / 520, 0, 1)
    link = hatch(W, H, 0.02, 5.0, .22, nx()) * lawn * np.clip((yy - GL) / 50, .2, 1) * (fbm(W, H, nx(), 20, 2) > .35)
    ground = strokes(W, H, [([(120, GL + 21), (880, GL + 21)], 2, None), ([(40, GL + 30), (960, GL + 30)], 1.2, None)])
    total = np.clip(np.maximum.reduce([ink, line, hands, tink, trunks, ground]) * (1 - np.maximum(trees, 0) * building * 0) , 0, 1)
    total = np.maximum(total * (1 - trees * (building > .5)), tink)
    a = LC(blank(W, H), total, INK, seed=nx(), wear=.2, rough=.4)
    flag = shapes(W, H, [[(500, 40), (500, 8), (532, 16), (500, 24)]], smooth=False)
    pole = strokes(W, H, [([(500, 44), (500, 6)], 2, None)])
    a = OV(a, pole, lambda m: linocut(m, INK, seed=nx(), wear=.1))
    a = OV(a, flag, lambda m: gouache_paint(m, VERM, seed=nx(), rough=.5))
    save(a, f"{OUT}/campus.webp", max_w=760, quality=82)
    prev(a, "dn-campus", bg="#f4ecd8")
    clear()

# ---------------------------------------------------------------- ribbon (gold satin banner, 820x170 -> 600)
if "ribbon" in PARTS:
    W, H = 820, 170
    nx = Seq(921000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = blank(W, H)
    band = [(130, 40)] + [(130 + 560 * t, 40 + 18 * math.sin(math.pi * t) * -1 + 18) for t in np.linspace(0, 1, 20)] + [(690, 40), (690, 112)] + [(130 + 560 * t, 112 + 18 - 18 * math.sin(math.pi * t) * 1) for t in np.linspace(1, 0, 20)][:-1] + [(130, 112)]
    band = [(130 + 560 * t, 58 - 18 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 24)] + [(130 + 560 * t, 128 - 18 * math.sin(math.pi * t)) for t in np.linspace(1, 0, 24)]
    tails = [[(130, 70), (20, 76), (58, 108), (20, 142), (150, 140)], [(690, 70), (800, 76), (762, 108), (800, 142), (670, 140)]]
    folds = [[(130, 58), (150, 140), (130, 128)], [(690, 58), (670, 140), (690, 128)]]
    tm = shapes(W, H, tails, smooth=False)
    a = FO(a, tm, "#a98336", seed=nx(), emboss=.5, sparkle=.1)
    a = G(a, tm, "#6e5220", seed=nx(), density=.4, edge=.2, rough=1.5)
    fm = shapes(W, H, folds, smooth=False)
    a = OV(a, fm, lambda m: gouache_paint(m, "#5e4519", seed=nx(), rough=.4))
    bm = shapes(W, H, [band])
    a = FO(a, bm, "#d2ac55", seed=nx(), emboss=.5, sparkle=.15)
    sat = bm * (.5 + .5 * np.sin((xx / 70) + 1.2)) * .35
    a = G(a, sat, "#8f6a26", seed=nx(), density=.5, edge=0, bloom=0, rough=3, gran=0)
    edges = strokes(W, H, [([(130 + 560 * t, 66 - 18 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 30)], 2, None), ([(130 + 560 * t, 120 - 18 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 30)], 2, None)])
    a = OV(a, edges, lambda m: gouache_paint(m, "#7a5a22", seed=nx(), rough=.3, density=.7))
    save(a, f"{OUT}/ribbon.webp", max_w=600)
    prev(a, "dn-ribbon", bg="#f4ecd8")
    clear()

# ---------------------------------------------------------------- laurel divider (foil, 420x130 -> 220)
if "laurel" in PARTS:
    W, H = 420, 130
    nx = Seq(931000)
    a = blank(W, H)
    for side in (-1, 1):
        # a horizontal branch from the centre outward
        pts = [(210 + side * (18 + i * 9), 70 - 10 * math.sin(i / 20 * math.pi)) for i in range(21)]
        st = strokes(W, H, [(pts, 3.4, (.05, .5))])
        leaves = []
        for i in range(2, 20, 2):
            x, y = pts[i]
            ln = 30 * (1 - i / 34)
            leaves.append(petal_pts(x, y, ln, 8 * (1 - i / 40), (0 if side > 0 else math.pi) - .9, n=12))
            leaves.append(petal_pts(x, y, ln, 8 * (1 - i / 40), (0 if side > 0 else math.pi) + .9, n=12))
        lm = shapes(W, H, leaves)
        a = FO(a, np.maximum(st, lm), "#c29b48", seed=nx(), emboss=.8, sparkle=.15)
    dot = circles(W, H, [(210, 70, 7)])
    a = OV(a, dot, lambda m: gouache_paint(m, VERM, seed=nx(), rough=.4))
    save(a, f"{OUT}/laurel.webp", max_w=220)
    prev(a, "dn-laurel", bg="#f4ecd8")
    clear()

# ---------------------------------------------------------------- foil texture (for the big number, 400x400)
if "foil" in PARTS:
    W = H = 400
    nx = Seq(941000)
    m = np.ones((H, W), np.float32)
    a = foil(m, "#c9a24c", seed=nx(), emboss=0, sparkle=.35)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    band = .5 + .5 * np.sin((xx * .6 + yy) / 38)
    a[..., :3] = np.clip(a[..., :3] * (.82 + .3 * band[..., None]), 0, 1)
    a = add_grain(a, nx(), .05)
    save_rgb(a, f"{OUT}/foil.webp", quality=74)
    clear()
