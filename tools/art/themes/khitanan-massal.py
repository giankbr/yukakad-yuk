"""Khitanan Massal — cheerful community mass-circumcision invitation in gouache: a green-and-white striped canopy tent
with a scalloped valance, three stylised friendly boys in sarung, baju koko and peci (waving, one holding a gift),
wrapped gift parcels, a balloon cluster, a single gift box and a small bunting strip. No medical imagery, no animals.
Run: python3 -I khitanan-massal.py [part ...]   parts: tent kids balloons gift bunting"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s6_lib import *

OUT = outdir("khitanan-massal")
PARTS = sys.argv[1:] or ["tent", "kids", "balloons", "gift", "bunting"]
GREEN, GREEN_D, GREEN_L = "#2f9e6b", "#1f6e4d", "#5cbf8d"
YEL, YEL_D, CORAL, CORAL_D = "#f7c948", "#d9a21f", "#ef6f5e", "#c94f40"
CREAM, INK, SKY = "#fffaf0", "#23302a", "#bfe6f2"
SKINS = ["#a86d47", "#c98a5e", "#8d5a3b"]


def tent():
    W, H = 800, 330
    rng = random.Random(4); nx = Seq(100)
    art = blank(W, H)
    # roof: three gentle peaks, stripes radiating from each peak
    peaks = [(140, 30), (400, 8), (660, 30)]
    eave = 150
    roof_poly = [(-10, eave), (-10, 90), (140, 30), (270, 70), (400, 8), (530, 70), (660, 30), (810, 90), (810, eave)]
    rm = shape_mask(W, H, roof_poly, smooth=False)
    art = paint(art, rm, "#f7f4ea", "#ece6d6", seed=nx(), rough=1.2)
    stripes = []
    for (px, py) in peaks:
        for k in range(-5, 6):
            if k % 2:
                continue
            x0, x1 = px + k * 26, px + (k + 1) * 26
            stripes.append([(px, py), (px + (x0 - px) * 1.0 + (x0 - px) * 0.0, eave + 2), (x1, eave + 2)])
    sm = shapes(W, H, [[(px, py), (px + k * 26 * 1.0, eave + 2), (px + (k + 1) * 26, eave + 2)] for (px, py) in peaks for k in range(-6, 6, 2)], smooth=False) * rm
    art = paint(art, sm, GREEN, GREEN_D, seed=nx(), rough=1.0)
    # roof shading (right side of each peak darker)
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    sh = np.zeros((H, W), np.float32)
    for (px, py) in peaks:
        sh = np.maximum(sh, np.clip((xx - px) / 120, 0, 1) * (np.abs(xx - px) < 130))
    art = shade(art, rm * sh * 0.6, "#2b4a3a", seed=nx(), density=0.28)
    # valance with scallops: alternating green / white segments
    val_top, val_h, sc = eave, 34, 40
    seg_g, seg_w = [], []
    for i in range(-1, W // sc + 2):
        x0 = i * sc
        poly = [(x0, val_top), (x0 + sc, val_top), (x0 + sc, val_top + val_h)] + [(x0 + sc / 2 + sc / 2 * math.cos(t / 12 * math.pi), val_top + val_h + 12 * math.sin(t / 12 * math.pi)) for t in range(13)] + [(x0, val_top + val_h)]
        (seg_g if i % 2 == 0 else seg_w).append(poly)
    art = paint(art, shapes(W, H, seg_w, smooth=False), "#fbf8ef", "#eee8d8", seed=nx(), rough=0.8)
    art = paint(art, shapes(W, H, seg_g, smooth=False), GREEN, "#279060", seed=nx(), rough=0.8)
    trim = strokes(W, H, [([(-10, val_top + 1), (W + 10, val_top + 1)], 6, None)])
    art = paint(art, trim, YEL, YEL_D, seed=nx(), rough=0.6)
    # tassels
    tass = []
    for i in range(0, W // sc + 1):
        x = i * sc + sc / 2
        tass.append(([(x, val_top + val_h + 12), (x, val_top + val_h + 26)], 3, None))
    art = paint(art, strokes(W, H, tass), YEL, YEL_D, seed=nx(), rough=0.4)
    art = paint(art, circles(W, H, [(i * sc + sc / 2, val_top + val_h + 28, 4.5) for i in range(W // sc + 1)]), CORAL, CORAL_D, seed=nx(), rough=0.4)
    # poles at both ends
    poles = strokes(W, H, [([(26, eave + 40), (26, H)], 12, None), ([(W - 26, eave + 40), (W - 26, H)], 12, None)])
    art = paint(art, poles, "#d9d6cf", "#a9a59c", seed=nx(), rough=0.6)
    show(art, "km-tent", tone="#fff6dc")
    save(art, f"{OUT}/tent.webp", max_w=780, quality=82)


def plaid(W, H, mask, x0, y0, c1, c2, step=12, seed=1):
    """Sarung check: two crossing stripe sets inside mask."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = ((((xx - x0) // step) % 3) == 0).astype(np.float32)
    hz = ((((yy - y0) // step) % 3) == 0).astype(np.float32)
    thin_v = (np.abs(((xx - x0) % (step * 3)) - step * 1.8) < 1.2).astype(np.float32)
    return np.clip(v * 0.55 + hz * 0.55, 0, 1) * mask, thin_v * mask


def boy(art, W, H, x, by, h, nx, rng, skin, koko, sarung, sar2, wave=0, carry=False):
    s = h / 100.0
    X = lambda dx: x + dx * s
    Y = lambda dy: by - dy * s
    # feet / sandals
    art = paint(art, ellipses(W, H, [(X(-7), Y(1.5), 7 * s, 3 * s, 0), (X(7), Y(1.5), 7 * s, 3 * s, 0)]), "#6b4a32", seed=nx(), rough=0.5)
    art = paint(art, ellipses(W, H, [(X(-7), Y(3.5), 4.5 * s, 2.4 * s, 0), (X(7), Y(3.5), 4.5 * s, 2.4 * s, 0)]), skin, seed=nx(), rough=0.4)
    # sarung: slightly flared tube with a fold at the waist
    sm = shape_mask(W, H, [(X(-15), Y(48)), (X(15), Y(48)), (X(17), Y(4)), (X(-17), Y(4))], smooth=False)
    art = paint(art, sm, sarung, mix(sarung, "#000000", .1), seed=nx(), rough=0.8)
    a, b = plaid(W, H, sm, X(0), Y(48), sarung, sar2, step=max(4, int(4 * s)), seed=nx())
    art = over(art, flat(a, sar2, 0.55))
    art = over(art, flat(b, CREAM, 0.5))
    fold = strokes(W, H, [([(X(-15), Y(44)), (X(15), Y(44))], 3.4 * s, None), ([(X(4), Y(44)), (X(8), Y(30))], 2.0 * s, None)])
    art = shade(art, fold * sm, "#1f1a18", seed=nx(), density=0.35)
    art = shade(art, sm * np.clip((np.arange(W)[None, :] - X(4)) / (12 * s), 0, 1), "#1f1a18", seed=nx(), density=0.25)
    # baju koko: torso
    tm = rrect(W, H, [(X(-16), Y(80), X(16), Y(42), 9 * s)])
    art = paint(art, tm, koko, mix(koko, "#000000", .06), seed=nx(), rough=0.8)
    # arms
    la = [(X(-14), Y(76)), (X(-21), Y(60)), (X(-19), Y(47))]
    if wave:
        ra = [(X(14), Y(76)), (X(24), Y(88)), (X(26), Y(104))]
    else:
        ra = [(X(14), Y(76)), (X(21), Y(60)), (X(19), Y(47))]
    if carry:
        la = [(X(-14), Y(76)), (X(-16), Y(60)), (X(-4), Y(56))]
        ra = [(X(14), Y(76)), (X(16), Y(60)), (X(4), Y(56))]
    cl, cr = curve(la, 12), curve(ra, 12)
    art = paint(art, strokes(W, H, [(cl, 8.5 * s, None), (cr, 8.5 * s, None)]), koko, mix(koko, "#000000", .08), seed=nx(), rough=0.6)
    art = paint(art, circles(W, H, [(la[-1][0], la[-1][1], 4.2 * s), (ra[-1][0], ra[-1][1], 4.2 * s)]), skin, seed=nx(), rough=0.4)
    # collar band + buttons
    art = paint(art, strokes(W, H, [([(X(-6), Y(80)), (X(6), Y(80))], 3.2 * s, None), ([(X(0), Y(80)), (X(0), Y(62))], 2.4 * s, None)]), mix(koko, "#000000", .14), seed=nx(), rough=0.4)
    art = paint(art, circles(W, H, [(X(1.8), Y(75 - 5 * k), 1.1 * s) for k in range(3)]), YEL_D, seed=nx(), rough=0.2)
    art = shade(art, tm * np.clip((np.arange(W)[None, :] - X(6)) / (12 * s), 0, 1), "#3a4a5a", seed=nx(), density=0.25)
    # neck, head, ears
    art = paint(art, rrect(W, H, [(X(-3.5), Y(85), X(3.5), Y(78), 2 * s)]), skin, seed=nx(), rough=0.3)
    art = paint(art, circles(W, H, [(X(-11.5), Y(92), 3 * s), (X(11.5), Y(92), 3 * s)]), skin, seed=nx(), rough=0.3)
    head = ellipses(W, H, [(X(0), Y(93), 11.5 * s, 12 * s, 0)])
    art = paint(art, head, skin, mix(skin, "#000000", .05), seed=nx(), rough=0.4)
    art = shade(art, head * np.clip((np.arange(W)[None, :] - X(3)) / (10 * s), 0, 1), "#5a3420", seed=nx(), density=0.18)
    # peci: tapered velvet cap
    peci = shape_mask(W, H, [(X(-11.8), Y(99)), (X(11.8), Y(99)), (X(10.5), Y(110)), (X(-10.5), Y(110))], smooth=False)
    peci = np.maximum(peci, ellipses(W, H, [(X(0), Y(110), 10.5 * s, 2.2 * s, 0)]))
    art = paint(art, peci, "#1e1e22", "#2c2c33", seed=nx(), rough=0.4)
    art = over(art, flat(gaussian_filter(strokes(W, H, [([(X(-7), Y(107)), (X(4), Y(107.5))], 1.6 * s, None)]), 1) * peci, "#6d6d78", 0.6))
    # face: dot eyes, smile, cheeks (simple, friendly)
    art = paint(art, circles(W, H, [(X(-4.2), Y(93), 1.5 * s), (X(4.2), Y(93), 1.5 * s)]), INK, seed=nx(), rough=0.15)
    smile = strokes(W, H, [(arc_pts(X(0), Y(89.5), 4.2 * s, 0.35, math.pi - 0.35, 12), 1.3 * s, None)])
    art = paint(art, smile, "#5a2a1e", seed=nx(), rough=0.15)
    art = over(art, flat(gaussian_filter(circles(W, H, [(X(-7), Y(89), 2.4 * s), (X(7), Y(89), 2.4 * s)]), 1.4 * s), "#e0705a", 0.4))
    return art


def parcel(art, W, H, x, by, w, h, nx, wrap, ribbon, lid=None):
    box = rrect(W, H, [(x - w / 2, by - h, x + w / 2, by, 3)])
    art = paint(art, box, wrap, mix(wrap, "#000000", .08), seed=nx(), rough=0.8)
    lid_m = rrect(W, H, [(x - w / 2 - 4, by - h - 2, x + w / 2 + 4, by - h + h * 0.22, 3)])
    art = paint(art, lid_m, lid or mix(wrap, "#ffffff", .15), seed=nx(), rough=0.6)
    art = paint(art, shapes(W, H, [rr(x - w * .08, by - h - 2, x + w * .08, by)], smooth=False), ribbon, mix(ribbon, "#000000", .1), seed=nx(), rough=0.4)
    bow = shapes(W, H, [[(x, by - h - 2), (x - w * .3, by - h - h * .3), (x - w * .28, by - h + 2)], [(x, by - h - 2), (x + w * .3, by - h - h * .3), (x + w * .28, by - h + 2)]])
    art = paint(art, bow, ribbon, mix(ribbon, "#000000", .12), seed=nx(), rough=0.4)
    art = shade(art, box * np.clip((np.arange(W)[None, :] - x) / (w * .5), 0, 1), "#2b2b2b", seed=nx(), density=0.2)
    return art


def kids():
    W, H = 800, 440
    rng = random.Random(9); nx = Seq(300)
    art = blank(W, H)
    # ground shadow
    sh = ellipses(W, H, [(400, 424, 340, 14, 0)])
    art = over(art, flat(gaussian_filter(sh, 6), "#2f5a44", 0.25))
    # parcels back
    art = parcel(art, W, H, 92, 424, 90, 70, nx, CORAL, YEL)
    art = parcel(art, W, H, 150, 426, 64, 46, nx, YEL, GREEN)
    art = parcel(art, W, H, 690, 424, 96, 78, nx, "#6fb8d6", CORAL)
    art = parcel(art, W, H, 630, 428, 58, 40, nx, GREEN_L, YEL)
    clear()
    art = boy(art, W, H, 260, 420, 270, nx, rng, SKINS[1], "#f7f4ea", "#7a2f3a", "#d9b25a", wave=1)
    clear()
    art = boy(art, W, H, 400, 426, 300, nx, rng, SKINS[0], "#dff1ea", "#245a8a", "#e9e2d0", carry=True)
    clear()
    art = parcel(art, W, H, 400, 426 - 300 * .5, 54, 36, nx, YEL, CORAL)
    art = boy(art, W, H, 540, 420, 265, nx, rng, SKINS[2], "#fff3d6", "#2f6b4c", "#e2c45a", wave=1)
    art = art[:, ::-1].copy() if False else art
    show(art, "km-kids", tone="#fff6dc")
    save(art, f"{OUT}/kids.webp", max_w=760, quality=82)


def balloons():
    W, H = 300, 440
    rng = random.Random(14); nx = Seq(600)
    art = blank(W, H)
    knot = (150, 400)
    specs = [(98, 120, 54, CORAL), (196, 96, 58, YEL), (150, 196, 52, GREEN_L)]
    strs = [(curve([(bx, by + r * 1.15), (bx + (knot[0] - bx) * .5 + 8, (by + knot[1]) / 2), knot], 20), 1.6, None) for bx, by, r, c in specs]
    art = paint(art, strokes(W, H, strs), "#7c7c7c", seed=nx(), rough=0.3)
    for bx, by, r, c in specs:
        m = shape_mask(W, H, [(bx + math.cos(t) * r * (1 - 0.12 * max(0, math.sin(t))), by + math.sin(t) * r * 1.15 + (8 if math.sin(t) > 0.9 else 0)) for t in [k / 24 * math.tau for k in range(24)]])
        art = paint(art, m, c, mix(c, "#000000", .12), seed=nx(), rough=0.8)
        art = shade(art, m * np.clip(((np.arange(W)[None, :] - bx) / r + (np.arange(H)[:, None] - by) / r) * 0.6, 0, 1), "#3a2a2a", seed=nx(), density=0.3)
        hl = ellipses(W, H, [(bx - r * .35, by - r * .45, r * .16, r * .28, -30)])
        art = over(art, flat(gaussian_filter(hl, 2), "#ffffff", 0.7))
        art = paint(art, shapes(W, H, [[(bx - 6, by + r * 1.2), (bx + 6, by + r * 1.2), (bx, by + r * 1.1)]], smooth=False), mix(c, "#000000", .15), seed=nx(), rough=0.3)
    show(art, "km-balloons", tone="#fff6dc")
    save(art, f"{OUT}/balloons.webp", max_w=200, quality=82)


def gift():
    W, H = 220, 220
    nx = Seq(800)
    art = parcel(blank(W, H), W, H, 110, 196, 130, 110, nx, CORAL, YEL)
    show(art, "km-gift", tone="#fff6dc")
    save(art, f"{OUT}/gift.webp", max_w=120, quality=84)


def bunting():
    W, H = 600, 80
    nx = Seq(900)
    art = blank(W, H)
    line = curve([(0, 10), (150, 22), (300, 26), (450, 22), (600, 10)], 60)
    art = paint(art, strokes(W, H, [(line, 2.4, None)]), "#6b5a4a", seed=nx(), rough=0.3)
    cols = [GREEN, YEL, CORAL, "#6fb8d6", GREEN_L]
    for i in range(12):
        t = (i + 0.5) / 12
        x = t * W
        y = 10 + 16 * math.sin(math.pi * t)
        tri = shape_mask(W, H, [(x - 20, y), (x + 20, y), (x + 1, y + 44)], smooth=False)
        art = paint(art, tri, cols[i % len(cols)], mix(cols[i % len(cols)], "#000000", .1), seed=nx(), rough=0.8)
    show(art, "km-bunting", tone="#fff6dc")
    save(art, f"{OUT}/bunting.webp", max_w=400, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
