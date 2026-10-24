"""Lomba Masak — a neighbourhood cooking contest in fresh, chunky gouache: a cooking station (wooden counter with a
blue gingham cloth, enamel pot on a gas ring, wok and spatula, cutting board with sliced veg, a heap of tomatoes,
chilies, eggplant, carrots, cabbage and scallions), rising steam wisps (separate, animated), the judges' table with three
covered plates, score paddles and a bell, a hanging red apron, a vegetable divider and a crossed spoon & whisk.
Palette: cobalt enamel, saffron, tomato red, leaf green, cream, wood.
Run: python3 -I lomba-masak.py [part ...]   parts: dapur asap juri celemek sayur sendok"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t5_lib import *

OUT = outdir("lomba-masak")
PARTS = sys.argv[1:] or ["dapur", "asap", "juri", "celemek", "sayur", "sendok"]
COBALT, COBALT_D, COBALT_L = "#2c4fa3", "#1b3274", "#5b7fd0"
SAFFRON, SAFFRON_D = "#f3b93a", "#c9861b"
TOMATO, TOMATO_D, TOMATO_L = "#e04a32", "#9f2617", "#ff8a6a"
LEAF, LEAF_D, LEAF_L = "#4f9a45", "#2c6430", "#9ccc6a"
CREAM, CREAM_D = "#fff6e3", "#ead9b5"
WOOD, WOOD_D, WOOD_L = "#b07a45", "#6e4422", "#d9a66b"
INK = "#2a1f1a"


def hl(art, W, H, m, col="#ffffff", amt=0.5, dx=-0.3, dy=-0.35, r=0.35):
    """Gouache highlight dab inside mask m, towards the upper-left."""
    ys, xs = np.where(m > 0.5)
    if len(xs) == 0:
        return art
    cx, cy = xs.mean(), ys.mean()
    rx, ry = (xs.max() - xs.min()) / 2, (ys.max() - ys.min()) / 2
    dab = ell(W, H, cx + dx * rx, cy + dy * ry, rx * r, ry * r * 0.7, -30) * m
    return OV(art, gaussian_filter(dab, 1.2), lambda mm: rgba(col, mm * amt))


def shade(art, W, H, m, col, amt=0.35, side=1):
    ys, xs = np.where(m > 0.5)
    if len(xs) == 0:
        return art
    cx, cy = xs.mean(), ys.mean()
    rx, ry = (xs.max() - xs.min()) / 2 + 1, (ys.max() - ys.min()) / 2 + 1
    yy, xx = yx(W, H)
    t = np.clip(((xx - cx) / rx * 0.6 * side + (yy - cy) / ry * 0.8), 0, 1)
    return OV(art, m * t, lambda mm: rgba(col, mm * amt))


def tomato(art, W, H, cx, cy, r, nx):
    m = ell(W, H, cx, cy, r, r * 0.86)
    art = GP(art, m, TOMATO, "#ea5a3b", seed=nx(), rough=1.0, streak=0.6)
    art = shade(art, W, H, m, TOMATO_D, 0.45)
    art = hl(art, W, H, m, "#ffd2c0", 0.7)
    cal = []
    for k in range(5):
        a = k / 5 * math.tau - math.pi / 2
        cal.append(petal_pts(cx, cy - r * 0.78, r * 0.42, r * 0.16, a, n=10))
    art = GP(art, shapes(W, H, cal), LEAF, LEAF_D, seed=nx(), rough=0.5)
    return art


def chili(art, W, H, pts, wd, nx, col=TOMATO, col2=TOMATO_D):
    c = curve(pts, 30)
    m = line(W, H, c, wd, (0.0, 0.85))
    art = GP(art, m, col, col2, seed=nx(), rough=0.6, streak=0.5)
    art = OV(art, line(W, H, [(x - 1, y - wd * 0.22) for x, y in c[2:-8]], wd * 0.22, (0.1, 0.6)) * m, lambda mm: rgba("#ffd0c0", mm * 0.6))
    cap = ell(W, H, c[0][0], c[0][1], wd * 0.7, wd * 0.5)
    art = GP(art, cap, LEAF, LEAF_D, seed=nx(), rough=0.4)
    a = math.atan2(c[0][1] - c[3][1], c[0][0] - c[3][0])
    st = line(W, H, [c[0], (c[0][0] + math.cos(a) * wd * 1.2, c[0][1] + math.sin(a) * wd * 1.2 - wd * 0.4)], wd * 0.35, None)
    return GP(art, st, LEAF_D, seed=nx(), rough=0.3)


def carrot(art, W, H, x, y, L, ang, nx):
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    w = L * 0.16
    body = [(x + px * w, y + py * w), (x + ca * L * 0.5 + px * w * 0.7, y + sa * L * 0.5 + py * w * 0.7), (x + ca * L, y + sa * L),
            (x + ca * L * 0.5 - px * w * 0.7, y + sa * L * 0.5 - py * w * 0.7), (x - px * w, y - py * w)]
    m = poly(W, H, body, smooth=True)
    art = GP(art, m, "#f28a2e", "#e06d1c", seed=nx(), rough=0.8, streak=0.6)
    art = shade(art, W, H, m, "#a8460f", 0.3)
    rid = strokes(W, H, [([(x + ca * L * t + px * w * 0.6 * (1 - t), y + sa * L * t + py * w * 0.6 * (1 - t)), (x + ca * L * t + px * w * 0.1, y + sa * L * t + py * w * 0.1)], 1.6, None) for t in (0.2, 0.36, 0.52, 0.68)]) * m
    art = OV(art, rid, lambda mm: rgba("#a8460f", mm * 0.6))
    fr = []
    for k in range(5):
        aa = ang + math.pi + (k - 2) * 0.28
        fr.append((curve([(x, y), (x + math.cos(aa) * L * 0.25, y + math.sin(aa) * L * 0.25 - 4), (x + math.cos(aa) * L * 0.45, y + math.sin(aa) * L * 0.45)], 10), L * 0.04, (0.05, 0.6)))
    return GP(art, strokes(W, H, fr), LEAF, LEAF_D, seed=nx(), rough=0.4)


def eggplant(art, W, H, x, y, L, ang, nx):
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    prof = [(0.0, 0.1), (0.25, 0.16), (0.5, 0.22), (0.72, 0.27), (0.9, 0.24), (1.0, 0.12), (1.04, 0.0)]
    pts = [(x + ca * L * u + px * L * w, y + sa * L * u + py * L * w) for u, w in prof]
    pts += [(x + ca * L * u - px * L * w * 0.9, y + sa * L * u - py * L * w * 0.9) for u, w in prof[::-1][1:]]
    m = shape_mask(W, H, pts)
    art = GP(art, m, "#6b3d8a", "#4b2766", seed=nx(), rough=0.8, streak=0.6)
    art = shade(art, W, H, m, "#2a1238", 0.4)
    art = hl(art, W, H, m, "#c8a4e0", 0.6, r=0.25)
    cap = [petal_pts(x, y, L * 0.3, L * 0.12, ang + d, n=10) for d in (-0.5, 0, 0.5)]
    art = GP(art, shapes(W, H, cap), LEAF, LEAF_D, seed=nx(), rough=0.4)
    st = line(W, H, [(x, y), (x - math.cos(ang) * L * 0.14, y - math.sin(ang) * L * 0.14)], L * 0.06, None)
    return GP(art, st, LEAF_D, seed=nx(), rough=0.3)


def cabbage(art, W, H, cx, cy, r, nx):
    m = ell(W, H, cx, cy, r, r * 0.9)
    art = GP(art, m, "#b9da7a", "#94c25a", seed=nx(), rough=1.2, streak=0.5)
    for k, (dx, rr) in enumerate([(-0.35, 0.75), (0.38, 0.72), (0.0, 0.55)]):
        lm = ell(W, H, cx + dx * r, cy + 0.1 * r, rr * r * 0.7, rr * r * 0.8) * m
        art = GP(art, lm, "#d4ea9d" if k == 2 else "#a8d06a", "#86b84e", seed=nx(), rough=0.8, streak=0.4)
        art = OV(art, np.clip(lm - gaussian_filter(lm, 1.4) * 1.05, 0, 1), lambda mm: rgba(LEAF_D, mm * 0.5))
    veins = strokes(W, H, [(curve([(cx, cy + r * 0.8), (cx + d * r * 0.3, cy), (cx + d * r * 0.6, cy - r * 0.6)], 12), 1.8, (0.1, 0.5)) for d in (-1, -0.3, 0.4, 1)]) * m
    return OV(art, veins, lambda mm: rgba("#eaf6cc", mm * 0.7))


def scallions(art, W, H, x, y, L, ang, nx, n=4):
    items, whites = [], []
    for k in range(n):
        a = ang + (k - n / 2) * 0.05
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        items.append(([(x + math.cos(a) * L * 0.3, y + math.sin(a) * L * 0.3), ((x + ex) / 2, (y + ey) / 2 - 3), (ex, ey)], 6, (0.02, 0.4)))
        whites.append(([(x, y), (x + math.cos(a) * L * 0.32, y + math.sin(a) * L * 0.32)], 7, (0.2, 0.0)))
    art = GP(art, strokes(W, H, items), LEAF, LEAF_D, seed=nx(), rough=0.4)
    return GP(art, strokes(W, H, whites), "#f6f3e4", "#dfe7c8", seed=nx(), rough=0.4)


def enamel_pot(art, W, H, x0, y0, x1, y1, nx, col=COBALT, col2=COBALT_D):
    cx = (x0 + x1) / 2
    rx = (x1 - x0) / 2
    body = rect(W, H, x0, y0, x1, y1, 18)
    body = np.maximum(body, ell(W, H, cx, y1 - 6, rx, 16))
    art = GP(art, body, col, col2, seed=nx(), rough=0.8, streak=0.7)
    art = shade(art, W, H, body, "#0d1a45", 0.45)
    art = OV(art, rect(W, H, x0 + rx * 0.25, y0 + 14, x0 + rx * 0.38, y1 - 14, 6), lambda mm: rgba("#9bb4ee", mm * 0.45))
    rim = ell(W, H, cx, y0, rx + 6, 14)
    art = GP(art, rim, "#f7f4ee", "#dfe4ec", seed=nx(), rough=0.5)
    # enamel chips + speckles
    spk = circles(W, H, [(x0 + random.Random(k).uniform(6, 2 * rx - 6), y0 + random.Random(k + 50).uniform(20, y1 - y0 - 10), random.Random(k + 9).uniform(1.2, 2.6)) for k in range(26)]) * body
    art = OV(art, spk, lambda mm: rgba("#f2f0ea", mm * 0.8))
    for side in (-1, 1):
        hx = cx + side * (rx + 12)
        h = rect(W, H, hx - 12, y0 + 18, hx + 12, y0 + 30, 6)
        art = GP(art, h, "#2a2a30", seed=nx(), rough=0.4)
    lid = ell(W, H, cx + 10, y0 - 8, rx - 2, 12)
    art = GP(art, lid, col, col2, seed=nx(), rough=0.5)
    art = OV(art, ell(W, H, cx + 10, y0 - 12, rx - 12, 5) * lid, lambda mm: rgba("#9bb4ee", mm * 0.4))
    knob = ell(W, H, cx + 12, y0 - 20, 12, 8)
    return GP(art, knob, "#2a2a30", seed=nx(), rough=0.3)


def dapur():
    W, H = 860, 560
    nx = Seq(3)
    art = blank(W, H)
    # counter: wood top + gingham cloth
    top = rect(W, H, 10, 372, 850, 404, 8)
    art = GP(art, top, WOOD_L, WOOD, seed=nx(), rough=1.0, streak=1.3)
    grain = strokes(W, H, [(curve([(20, y), (300, y + 2), (600, y - 1), (840, y + 1)], 20), 1.4, None) for y in (382, 392)]) * top
    art = OV(art, grain, lambda mm: rgba(WOOD_D, mm * 0.35))
    cloth = poly(W, H, [(18, 400), (842, 400), (848, 546), (796, 556), (740, 546), (680, 556), (620, 546), (560, 556), (500, 546), (440, 556), (380, 546), (320, 556), (260, 546), (200, 556), (140, 546), (80, 556), (12, 546)], smooth=False)
    art = GP(art, cloth, "#f8f3ea", "#efe6d6", seed=nx(), rough=1.4, streak=0.6)
    yy, xx = yx(W, H)
    gx = ((xx // 22) % 2 == 0).astype(np.float32)
    gy = (((yy - 400) // 22) % 2 == 0).astype(np.float32)
    art = OV(art, cloth * gx * 0.55, lambda mm: rgba(COBALT_L, mm))
    art = OV(art, cloth * gy * 0.55, lambda mm: rgba(COBALT_L, mm))
    art = OV(art, cloth * gx * gy * 0.5, lambda mm: rgba(COBALT, mm))
    art = OV(art, cloth * np.clip(1 - (yy - 400) / 22, 0, 1), lambda mm: rgba("#3b2414", mm * 0.3))
    clear()
    # gas ring + pot (left)
    stove = rect(W, H, 70, 336, 300, 376, 8)
    art = GP(art, stove, "#4a4f57", "#2f333a", seed=nx(), rough=0.6, streak=0.6)
    art = OV(art, rect(W, H, 76, 338, 294, 344, 3), lambda mm: rgba("#8a919c", mm * 0.6))
    knobs = circles(W, H, [(110, 360, 8), (260, 360, 8)])
    art = GP(art, knobs, "#e8e2d6", seed=nx(), rough=0.3)
    flame = shapes(W, H, [petal_pts(140 + k * 16, 338, 14, 6, -math.pi / 2, n=8) for k in range(6)])
    art = GP(art, flame, "#5aa0ff", "#f5c04a", seed=nx(), rough=0.4)
    art = enamel_pot(art, W, H, 98, 196, 272, 334, nx)
    clear()
    # wok with spatula (middle) on a second ring
    ring2 = rect(W, H, 352, 344, 560, 376, 8)
    art = GP(art, ring2, "#4a4f57", "#2f333a", seed=nx(), rough=0.6)
    wok = poly(W, H, [(340, 300), (572, 300), (550, 330), (500, 348), (412, 348), (362, 330)], smooth=True)
    art = GP(art, wok, "#2d2d33", "#18181c", seed=nx(), rough=0.6, streak=0.5)
    art = OV(art, ell(W, H, 456, 302, 116, 10), lambda mm: rgba("#55555e", mm * 0.9))
    # nasi goreng-ish contents: rice, egg, greens
    food = ell(W, H, 456, 300, 98, 8)
    art = GP(art, food, "#e9b960", "#c98b3a", seed=nx(), rough=1.2)
    bits = circles(W, H, [(380 + k * 13 + (k % 3) * 2, 298 + (k % 2) * 3, 3.6) for k in range(12)])
    art = GP(art, bits, LEAF_L, LEAF, seed=nx(), rough=0.3)
    handle = line(W, H, [(572, 304), (640, 296), (676, 292)], 12, None)
    art = GP(art, handle, WOOD, WOOD_D, seed=nx(), rough=0.5)
    spat = poly(W, H, [(470, 262), (520, 268), (514, 296), (466, 290)], smooth=False)
    art = GP(art, spat, "#c9cdd4", "#8d939c", seed=nx(), rough=0.4)
    art = GP(art, line(W, H, [(512, 268), (560, 176), (568, 160)], 9, None), WOOD, WOOD_D, seed=nx(), rough=0.4)
    clear()
    # cutting board with cucumber + carrot coins and a knife (right)
    board = rect(W, H, 600, 344, 820, 378, 14)
    art = GP(art, board, "#e6bd84", "#c99a5c", seed=nx(), rough=0.8, streak=1.2)
    art = GP(art, ell(W, H, 816, 361, 16, 9), "#e6bd84", seed=nx(), rough=0.5)
    cuc = [(630 + k * 20, 352, 11) for k in range(4)]
    art = GP(art, circles(W, H, cuc), "#4f8a3c", seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(x, y, r - 3) for x, y, r in cuc]), "#d9edb0", "#bfe08c", seed=nx(), rough=0.3)
    coins = [(700 + k * 16, 366, 8) for k in range(4)]
    art = GP(art, circles(W, H, coins), "#f28a2e", "#e06d1c", seed=nx(), rough=0.3)
    knife = poly(W, H, [(706, 346), (800, 338), (806, 344), (708, 352)], smooth=False)
    art = GP(art, knife, "#d4d8de", "#9aa1aa", seed=nx(), rough=0.3)
    art = GP(art, rect(W, H, 770, 334, 812, 346, 4), INK, seed=nx(), rough=0.3)
    clear()
    # vegetable heap at the front of the counter
    art = cabbage(art, W, H, 336, 352, 44, nx)
    art = eggplant(art, W, H, 280, 386, 90, 0.25, nx)
    art = carrot(art, W, H, 560, 352, 110, 0.35, nx)
    art = carrot(art, W, H, 600, 372, 96, 0.1, nx)
    art = scallions(art, W, H, 40, 380, 150, -0.35, nx)
    clear()
    for cx, cy, r in ((424, 380, 26), (472, 386, 22), (448, 362, 20), (196, 388, 24)):
        art = tomato(art, W, H, cx, cy, r, nx)
    art = chili(art, W, H, [(500, 380), (530, 392), (566, 390), (590, 378)], 11, nx)
    art = chili(art, W, H, [(508, 396), (540, 402), (572, 400)], 9, nx, LEAF, LEAF_D)
    art = chili(art, W, H, [(230, 360), (250, 376), (262, 398)], 9, nx)
    save_prev(art, "dapur", "#fff6e3")
    save(art, f"{OUT}/dapur.webp", max_w=860, quality=80)


def asap():
    W, H = 220, 300
    nx = Seq(31)
    rng = random.Random(5)
    items = []
    for k in range(3):
        x = 60 + k * 50
        pts = [(x + math.sin(t * 2.6 + k) * 22, 290 - t * 270) for t in np.linspace(0, 1, 30)]
        items.append((pts, rng.uniform(9, 13), (0.15, 0.55)))
    m = strokes(W, H, items)
    art = G(blank(W, H), m, "#ffffff", "#eef1f6", seed=nx(), density=0.85, edge=0.25, bloom=0.4, rough=4, feather=2.5)
    save_prev(art, "asap", bg="#2c4fa3")
    save(art, f"{OUT}/asap.webp", max_w=160, quality=80)


def juri():
    W, H = 860, 360
    nx = Seq(51)
    art = blank(W, H)
    # tablecloth with a red skirt
    top = poly(W, H, [(30, 200), (830, 200), (846, 236), (14, 236)], smooth=False)
    art = GP(art, top, "#fffaf0", "#efe6d4", seed=nx(), rough=1.0, streak=0.6)
    skirt = poly(W, H, [(14, 234), (846, 234), (840, 352), (20, 352)], smooth=False)
    art = GP(art, skirt, TOMATO, "#c63c26", seed=nx(), rough=1.2, streak=0.8)
    pleats = strokes(W, H, [([(x, 238), (x + 2, 350)], 3, None) for x in range(50, 840, 46)]) * skirt
    art = OV(art, pleats, lambda mm: rgba(TOMATO_D, mm * 0.5))
    art = OV(art, rect(W, H, 14, 234, 846, 248), lambda mm: rgba(SAFFRON, mm * 0.9))
    clear()
    # three plates with dishes and cutlery
    dishes = [(190, "#d9772b", "#a24f17"), (430, "#f0d27a", "#c99a3a"), (670, "#7a3b22", "#4b2112")]
    for k, (cx, c1, c2) in enumerate(dishes):
        plate = ell(W, H, cx, 206, 92, 22)
        art = GP(art, plate, "#ffffff", "#e9edf2", seed=nx(), rough=0.5)
        art = OV(art, ring(W, H, 0, 0, 1, 1) * 0 + np.clip(plate - ell(W, H, cx, 206, 70, 16), 0, 1), lambda mm: rgba("#c9d2de", mm * 0.6))
        art = OV(art, np.clip(ell(W, H, cx, 206, 80, 19) - ell(W, H, cx, 206, 76, 17.5), 0, 1), lambda mm: rgba(COBALT_L, mm * 0.8))
        food = ell(W, H, cx, 194, 46, 20)
        art = GP(art, food, c1, c2, seed=nx(), rough=1.4, streak=0.6)
        art = hl(art, W, H, food, "#fff2c6", 0.5)
        gar = shapes(W, H, [petal_pts(cx + d * 14, 180, 14, 6, -math.pi / 2 + d * 0.6, n=8) for d in (-1, 0, 1)])
        art = GP(art, gar, LEAF, LEAF_D, seed=nx(), rough=0.3)
        if k == 1:
            art = tomato(art, W, H, cx + 28, 186, 9, nx)
        fork = line(W, H, [(cx - 112, 230), (cx - 104, 186)], 5, None)
        spoon = np.maximum(line(W, H, [(cx + 110, 230), (cx + 104, 194)], 5, None), ell(W, H, cx + 103, 188, 7, 10))
        art = GP(art, np.maximum(fork, spoon), "#c9cdd4", "#8d939c", seed=nx(), rough=0.3)
        # score paddle behind the plate
        clear()
    for k, (cx, val) in enumerate([(300, "9"), (550, "10"), (780, "8")]):
        stick = rect(W, H, cx - 5, 96, cx + 5, 196, 3)
        art = GP(art, stick, WOOD, WOOD_D, seed=nx(), rough=0.4)
        pad = circles(W, H, [(cx, 70, 46)])
        art = GP(art, pad, SAFFRON if k != 1 else "#ffffff", SAFFRON_D if k != 1 else "#eee6d6", seed=nx(), rough=0.8, streak=0.6)
        art = OV(art, ring(W, H, cx, 70, 46, 5), lambda mm: rgba(COBALT, mm))

        def num(cv, cx=cx, val=val):
            tf = skia.Typeface("DejaVu Sans", skia.FontStyle.Bold()) or skia.Typeface()
            font = skia.Font(tf, 46)
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
            wd = font.measureText(val)
            cv.c.drawString(val, cx - wd / 2, 86, font, p)
        art = GP(art, mask_from(W, H, num), COBALT, COBALT_D, seed=nx(), rough=0.8)
    bell = poly(W, H, [(70, 202), (76, 178), (90, 166), (104, 178), (110, 202)], smooth=True)
    art = FO(art, np.maximum(bell, ell(W, H, 90, 160, 5, 5)), "#d4a440", seed=nx(), emboss=0.7)
    art = OV(art, ell(W, H, 90, 203, 26, 5), lambda mm: rgba("#3a2a1a", mm * 0.4))
    save_prev(art, "juri", "#fff6e3")
    save(art, f"{OUT}/juri.webp", max_w=860, quality=80)


def celemek():
    W, H = 320, 440
    nx = Seq(71)
    art = blank(W, H)
    hook = line(W, H, [(160, 8), (160, 30)], 6, None)
    art = GP(art, hook, "#5a5f68", seed=nx(), rough=0.3)
    neck = strokes(W, H, [(curve([(108, 120), (128, 60), (160, 34), (192, 60), (212, 120)], 30), 10, None)])
    art = GP(art, neck, "#fffaf0", CREAM_D, seed=nx(), rough=0.5)
    body = poly(W, H, [(104, 112), (216, 112), (220, 170), (262, 196), (270, 410), (50, 410), (58, 196), (100, 170)], smooth=True)
    art = GP(art, body, TOMATO, "#c63c26", seed=nx(), rough=1.4, streak=1.0)
    art = shade(art, W, H, body, TOMATO_D, 0.35)
    folds = strokes(W, H, [(curve([(x, 210), (x + 4, 300), (x - 2, 400)], 20), 4, (0.2, 0.2)) for x in (110, 170, 222)]) * body
    art = OV(art, gaussian_filter(folds, 2), lambda mm: rgba(TOMATO_D, mm * 0.45))
    ties = strokes(W, H, [(curve([(60, 200), (30, 222), (20, 260), (34, 290)], 20), 9, (0.05, 0.3)), (curve([(260, 200), (290, 224), (300, 262), (288, 292)], 20), 9, (0.05, 0.3))])
    art = GP(art, ties, "#fffaf0", CREAM_D, seed=nx(), rough=0.5)
    pocket = rect(W, H, 104, 250, 216, 330, 12)
    art = GP(art, pocket, "#fffaf0", CREAM_D, seed=nx(), rough=0.8)
    yy, xx = yx(W, H)
    art = OV(art, pocket * ((xx // 12) % 2 == 0) * 0.5, lambda mm: rgba(COBALT_L, mm))
    art = OV(art, pocket * (((yy - 250) // 12) % 2 == 0) * 0.5, lambda mm: rgba(COBALT_L, mm))
    stitch = strokes(W, H, [([(x, 256), (x + 6, 256)], 2, None) for x in range(110, 210, 12)])
    art = OV(art, stitch, lambda mm: rgba(COBALT_D, mm * 0.8))
    art = GP(art, line(W, H, [(186, 252), (194, 196), (198, 178)], 7, None), WOOD, WOOD_D, seed=nx(), rough=0.4)
    art = GP(art, ell(W, H, 199, 172, 9, 12), WOOD, WOOD_D, seed=nx(), rough=0.4)
    save_prev(art, "celemek", "#fff6e3")
    save(art, f"{OUT}/celemek.webp", max_w=220, quality=84)


def sayur():
    W, H = 500, 120
    nx = Seq(91)
    art = blank(W, H)
    art = scallions(art, W, H, 30, 70, 120, -0.06, nx, n=3)
    art = carrot(art, W, H, 150, 56, 96, 0.12, nx)
    art = tomato(art, W, H, 266, 64, 26, nx)
    art = chili(art, W, H, [(300, 70), (330, 82), (370, 80), (392, 68)], 11, nx)
    art = eggplant(art, W, H, 400, 52, 84, 0.2, nx)
    save_prev(art, "sayur", "#fff6e3")
    save(art, f"{OUT}/sayur.webp", max_w=400, quality=84)


def sendok():
    W, H = 220, 220
    nx = Seq(101)
    art = blank(W, H)
    handle = line(W, H, [(40, 190), (122, 104)], 12, None)
    bowl = ell(W, H, 146, 78, 24, 36, 45)
    spoon = np.maximum(handle, bowl)
    art = GP(art, spoon, WOOD_L, WOOD, seed=nx(), rough=0.6, streak=1.0)
    art = OV(art, ell(W, H, 150, 74, 13, 22, 45) * bowl, lambda mm: rgba(WOOD_D, mm * 0.3))
    cv_items = []
    for k, sc in enumerate((1.0, 0.7, 0.4)):
        cv_items.append((ellipse_pts(78, 72, 22 * sc + 4, 50, n=36, rot=math.radians(-45)) + [ellipse_pts(78, 72, 22 * sc + 4, 50, n=36, rot=math.radians(-45))[0]], 3.0, None))
    loops = strokes(W, H, cv_items)
    art = GP(art, loops, "#c9cdd4", "#8d939c", seed=nx(), rough=0.3)
    wh_h = line(W, H, [(186, 190), (112, 116)], 13, None)
    art = GP(art, wh_h, COBALT, COBALT_D, seed=nx(), rough=0.4)
    save_prev(art, "sendok", "#fff6e3")
    save(art, f"{OUT}/sendok.webp", max_w=140, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
