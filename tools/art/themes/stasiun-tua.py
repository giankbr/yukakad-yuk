"""Stasiun Tua — an old railway station painted in sepia gouache with teal ironwork: a canopy edge with dagger-board
valance and wrought-iron corner spandrels, a big hanging station clock (dial only; the hands are CSS so they can tick),
a steam locomotive side-on with red drivers and brass bands, soft steam puffs, a stack of leather luggage trunks and a
wrought-iron scroll divider. Palette: sepia paper, teal iron, brass, rust red, coal.
Run: python3 -I stasiun-tua.py [part ...]   parts: kanopi jam lokomotif uap koper ulir"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t5_lib import *

OUT = outdir("stasiun-tua")
PARTS = sys.argv[1:] or ["kanopi", "jam", "lokomotif", "uap", "koper", "ulir"]
TEAL, TEAL_D, TEAL_L = "#2f6563", "#1d4142", "#5f8f88"
BRASS, BRASS_D, BRASS_L = "#c49445", "#8a6326", "#ecc87e"
RUST, RUST_D = "#9a4630", "#5f2618"
COAL, COAL_L = "#22302f", "#46605c"
CREAM, CREAM_D = "#f1e4c6", "#cdb98e"
WOOD, WOOD_D, WOOD_L = "#8a5a33", "#4e2f17", "#b98552"


def scroll(cx, cy, r, turns=1.4, a0=0.0, sgn=1, n=40):
    """Spiral C-scroll points (wrought-iron curl)."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + sgn * t * turns * math.tau
        rr = r * (1 - 0.78 * t)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def iron(art, W, H, items, nx, col=TEAL, col2=TEAL_D):
    m = strokes(W, H, items)
    art = GP(art, m, col, col2, seed=nx(), rough=0.8, streak=0.6)
    hl = strokes(W, H, [([(x - 0.8, y - 0.8) for x, y in it[0]], it[1] * 0.3, it[2] if len(it) > 2 else None) for it in items]) * m
    return OV(art, hl, lambda mm: rgba(TEAL_L, mm * 0.6))


def kanopi():
    W, H = 860, 250
    nx = Seq(5)
    rng = random.Random(3)
    art = blank(W, H)
    # roof underside: sepia boards
    roof = rect(W, H, 0, 0, W, 58)
    art = GP(art, roof, "#a8794a", "#7c5532", seed=nx(), rough=0.6, streak=1.2)
    boards = strokes(W, H, [([(x, 0), (x + 1, 58)], 1.6, None) for x in range(14, W, 30)])
    art = OV(art, boards, lambda mm: rgba(WOOD_D, mm * 0.45))
    art = OV(art, rect(W, H, 0, 40, W, 58) * vgrad(W, H, 40, 58), lambda mm: rgba("#2a170a", mm * 0.4))
    # iron fascia beam with rivets
    beam = rect(W, H, 0, 56, W, 82)
    art = GP(art, beam, TEAL, TEAL_D, seed=nx(), rough=0.6, streak=0.8)
    art = OV(art, rect(W, H, 0, 57, W, 61), lambda mm: rgba(TEAL_L, mm * 0.6))
    riv = circles(W, H, [(x, 70, 2.6) for x in range(10, W, 22)])
    art = GP(art, riv, BRASS_L, BRASS, seed=nx(), rough=0.3)
    # dagger-board valance (cream boards with pointed ends)
    polys = []
    x = -4
    while x < W:
        wd = 22
        L = 46 + rng.uniform(-1.5, 1.5)
        polys.append([(x + 1, 80), (x + wd - 1, 80), (x + wd - 1, 80 + L - 12), (x + wd / 2, 80 + L), (x + 1, 80 + L - 12)])
        x += wd
    val = shapes(W, H, polys, smooth=False)
    art = GP(art, val, "#f4e7c8", "#e6d3a6", seed=nx(), rough=1.0, streak=1.0)
    gaps = strokes(W, H, [([(x, 82), (x, 120)], 1.6, None) for x in range(-4, W, 22)]) * val
    art = OV(art, gaps, lambda mm: rgba(WOOD_D, mm * 0.65))
    half = shapes(W, H, [[(p[0][0] + 11, 80), p[1], p[2], p[3]] for p in polys], smooth=False) * val
    art = OV(art, half, lambda mm: rgba("#9d8455", mm * 0.4))
    edge = np.clip(val - gaussian_filter(val, 1.2) * 1.05, 0, 1)
    art = OV(art, edge, lambda mm: rgba(WOOD_D, mm * 0.6))
    art = OV(art, rect(W, H, 0, 80, W, 90) * val, lambda mm: rgba("#3a2410", mm * 0.3))
    art = OV(art, val * (fbm(W, H, nx(), 18, 2) > 0.62), lambda mm: rgba("#b59d6c", mm * 0.35))
    # wrought-iron corner spandrels framing the platform
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        sg = -side
        items = [
            ([(x0 + sg * 14, 82), (x0 + sg * 14, H)], 12, None),  # column
            (curve([(x0 + sg * 14, 230), (x0 + sg * 60, 150), (x0 + sg * 150, 98), (x0 + sg * 210, 86)], 50), 6, (0.0, 0.2)),
            (scroll(x0 + sg * 66, 128, 26, 1.3, math.pi if side < 0 else 0, sgn=-side), 4, (0.0, 0.3)),
            (scroll(x0 + sg * 42, 182, 20, 1.2, math.pi * 1.5, sgn=side), 4, (0.0, 0.3)),
            (scroll(x0 + sg * 118, 108, 14, 1.1, math.pi, sgn=-side), 3.4, (0.0, 0.3)),
        ]
        art = iron(art, W, H, items, nx)
        cap = rect(W, H, x0 + sg * 14 - 13, 80, x0 + sg * 14 + 13, 92, 2)
        art = GP(art, cap, TEAL_D, seed=nx(), rough=0.4)
    save_prev(art, "kanopi", "#efe2c8")
    save_full(art, f"{OUT}/kanopi.webp", size=(860, 250), quality=80)


def jam():
    W, H = 460, 540
    cx, cy, R = 230, 320, 196
    nx = Seq(21)
    art = blank(W, H)
    # hanging bracket: rod + scrolls
    items = [([(230, 0), (230, cy - R - 6)], 12, None),
             (scroll(196, 70, 30, 1.25, 0, sgn=1), 6, (0.0, 0.3)), (scroll(264, 70, 30, 1.25, math.pi, sgn=-1), 6, (0.0, 0.3)),
             (curve([(150, 112), (190, 100), (230, 96), (270, 100), (310, 112)], 30), 7, (0.1, 0.1))]
    art = iron(art, W, H, items, nx)
    knob = circles(W, H, [(230, 112, 13)])
    art = GP(art, knob, BRASS, BRASS_D, seed=nx(), rough=0.4)
    # case
    case = circles(W, H, [(cx, cy, R)])
    art = GP(art, case, TEAL, TEAL_D, seed=nx(), rough=1.0, streak=0.6)
    sh = side_shade(case, (cx, cy - R), (cx, cy + R), R * 2)
    art = OV(art, case * np.clip(sh - 0.5, 0, 1), lambda mm: rgba("#0f2526", mm * 0.7))
    bez = ring(W, H, cx, cy, R - 14, 16)
    art = FO(art, bez, BRASS, seed=nx(), emboss=0.8, sparkle=0.15)
    dial = circles(W, H, [(cx, cy, R - 30)])
    art = GP(art, dial, "#f7eed7", "#eadcb8", seed=nx(), rough=0.5, streak=0.3)
    yy, xx = yx(W, H)
    d = np.hypot(xx - cx, yy - cy) / (R - 30)
    art = OV(art, dial * np.clip((d - 0.55) * 1.6, 0, 1), lambda mm: rgba("#c7b080", mm * 0.45))
    # ticks
    minor, major = [], []
    for k in range(60):
        a = k / 60 * math.tau
        r0 = R - 44 if k % 5 else R - 64
        (major if k % 5 == 0 else minor).append(([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * (R - 38), cy + math.sin(a) * (R - 38))], 7 if k % 5 == 0 else 2.4, None))
    art = LC(art, strokes(W, H, minor), "#3a2a1c", seed=nx(), wear=0.2, rough=0.5)
    art = LC(art, strokes(W, H, major), "#2a1d12", seed=nx(), wear=0.2, rough=0.5)
    # roman numerals, printed then worn
    def numerals(cv):
        tf = skia.Typeface("DejaVu Serif") or skia.Typeface()
        font = skia.Font(tf, 27)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        labels = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        for k, lab in enumerate(labels):
            a = k / 12 * math.tau - math.pi / 2
            r = R - 98
            wdt = font.measureText(lab)
            cv.c.save()
            cv.c.translate(cx + math.cos(a) * r, cy + math.sin(a) * r)
            cv.c.drawString(lab, -wdt / 2, 11, font, p)
            cv.c.restore()
    nm = mask_from(W, H, numerals)
    art = LC(art, nm, "#2a1d12", seed=nx(), wear=0.25, rough=0.4)
    # small makers' ring
    art = OV(art, ring(W, H, cx, cy, 52, 1.6), lambda mm: rgba("#9c8457", mm * 0.6))
    save_prev(art, "jam", "#efe2c8")
    save_full(art, f"{OUT}/jam.webp", size=(460, 540), quality=82)


def lokomotif():
    W, H = 860, 430
    nx = Seq(41)
    art = blank(W, H)
    # sleepers + rails
    sl = shapes(W, H, [[(x, 396), (x + 34, 396), (x + 40, 416), (x - 6, 416)] for x in range(0, W, 52)], smooth=False)
    art = GP(art, sl, WOOD, WOOD_D, seed=nx(), rough=1.0, streak=1.2)
    rail = rect(W, H, 0, 388, W, 398)
    art = GP(art, rail, "#6b6f6a", "#3c3f3b", seed=nx(), rough=0.4)
    art = OV(art, rect(W, H, 0, 388, W, 391), lambda mm: rgba("#c9c5b6", mm * 0.8))
    # cab + boiler + smokebox
    body = []
    cab = rect(W, H, 604, 112, 800, 286, 4)
    art = GP(art, cab, "#2c4746", COAL, seed=nx(), rough=0.8, streak=0.8)
    roof = poly(W, H, [(588, 112), (596, 98), (812, 98), (820, 112)], smooth=False)
    art = GP(art, roof, COAL, "#121a1a", seed=nx(), rough=0.6)
    win = rect(W, H, 640, 140, 706, 196, 6)
    art = GP(art, win, "#f2cf7e", "#d9a24f", seed=nx(), rough=0.4)
    art = OV(art, ring(W, H, 0, 0, 1, 1) * 0 + rect(W, H, 671, 140, 675, 196), lambda mm: rgba(COAL, mm))
    art = OV(art, rect(W, H, 740, 136, 780, 286, 3), lambda mm: rgba("#162222", mm * 0.5))
    boiler = rect(W, H, 140, 158, 610, 270, 50)
    art = GP(art, boiler, "#2f4c4a", COAL, seed=nx(), rough=0.8, streak=0.9)
    sh = side_shade(boiler, (140, 158), (610, 158), 112)
    art = OV(art, boiler * np.clip((vgrad(W, H, 158, 270) - 0.55) * 1.8, 0, 1), lambda mm: rgba("#0e1717", mm * 0.6))
    art = OV(art, boiler * np.clip(1 - abs(vgrad(W, H, 158, 270) - 0.25) * 8, 0, 1), lambda mm: rgba("#7aa39a", mm * 0.45))
    smoke = rect(W, H, 128, 156, 244, 272, 46)
    art = GP(art, smoke, "#1e2a2a", "#141c1c", seed=nx(), rough=0.6)
    door = ell(W, H, 134, 214, 18, 50)
    art = GP(art, door, "#2a3838", "#141c1c", seed=nx(), rough=0.4)
    art = OV(art, ring(W, H, 134, 214, 10, 3) * door, lambda mm: rgba(BRASS, mm))
    # brass bands
    bands = rect(W, H, 262, 158, 270, 270) + rect(W, H, 404, 158, 412, 270) + rect(W, H, 532, 158, 540, 270)
    art = FO(art, np.clip(bands * boiler, 0, 1), BRASS, seed=nx(), emboss=0.5, sparkle=0.1)
    # stack, domes, lamp, whistle
    stack = poly(W, H, [(170, 158), (172, 108), (160, 92), (160, 80), (216, 80), (216, 92), (204, 108), (206, 158)], smooth=False)
    art = GP(art, stack, "#26393a", COAL, seed=nx(), rough=0.5)
    art = OV(art, rect(W, H, 158, 78, 218, 86), lambda mm: rgba(BRASS, mm * 0.9))
    dome = poly(W, H, [(326, 160), (330, 134), (358, 120), (386, 134), (390, 160)], smooth=True)
    art = FO(art, dome, BRASS, seed=nx(), emboss=0.8, sparkle=0.2)
    sand = poly(W, H, [(452, 160), (456, 140), (476, 132), (496, 140), (500, 160)], smooth=True)
    art = GP(art, sand, "#2f4c4a", COAL, seed=nx(), rough=0.5)
    whistle = rect(W, H, 588, 128, 596, 160)
    art = FO(art, whistle, BRASS, seed=nx(), emboss=0.4)
    lamp = rect(W, H, 106, 130, 136, 156, 4)
    art = GP(art, lamp, COAL, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(114, 143, 9)]), "#fbe3a2", "#f2c066", seed=nx(), rough=0.3)
    # running board (rust stripe) + buffer beam + cowcatcher
    board = rect(W, H, 108, 270, 812, 284)
    art = GP(art, board, RUST, RUST_D, seed=nx(), rough=0.5)
    beam = rect(W, H, 84, 266, 134, 306, 3)
    art = GP(art, beam, RUST, RUST_D, seed=nx(), rough=0.5)
    buf = rect(W, H, 64, 278, 88, 292, 3)
    art = GP(art, buf, "#4b4f4b", seed=nx(), rough=0.3)
    cow = poly(W, H, [(80, 306), (134, 306), (134, 390), (48, 390)], smooth=False)
    art = GP(art, cow, RUST, RUST_D, seed=nx(), rough=0.6)
    bars = strokes(W, H, [([(84 + k * 10, 310), (58 + k * 13, 388)], 3, None) for k in range(6)]) * cow
    art = OV(art, bars, lambda mm: rgba(RUST_D, mm * 0.8))
    cyl = rect(W, H, 150, 286, 262, 332, 10)
    art = GP(art, cyl, "#2f4c4a", COAL, seed=nx(), rough=0.5)
    art = OV(art, rect(W, H, 150, 286, 262, 292, 4), lambda mm: rgba(BRASS, mm * 0.8))
    # wheels
    def wheel(cx, cy, r, spokes):
        nonlocal art
        tire = circles(W, H, [(cx, cy, r)])
        art = GP(art, tire, "#3a3f3c", "#1f2321", seed=nx(), rough=0.5)
        rim = circles(W, H, [(cx, cy, r * 0.88)])
        art = GP(art, rim, RUST, RUST_D, seed=nx(), rough=0.5)
        inner = circles(W, H, [(cx, cy, r * 0.74)])
        art = OV(art, inner, lambda mm: rgba("#1d2423", mm * 0.85))
        sp = strokes(W, H, [([(cx, cy), (cx + math.cos(k / spokes * math.tau) * r * 0.76, cy + math.sin(k / spokes * math.tau) * r * 0.76)], max(2.5, r * 0.08), None) for k in range(spokes)])
        art = GP(art, sp, RUST, RUST_D, seed=nx(), rough=0.3)
        hub = circles(W, H, [(cx, cy, r * 0.2)])
        art = GP(art, hub, RUST, RUST_D, seed=nx(), rough=0.3)
        art = OV(art, ring(W, H, cx, cy, r - 1, 2.5), lambda mm: rgba("#9aa09a", mm * 0.6))
    wheel(198, 360, 30, 8)
    for x in (340, 466, 592):
        wheel(x, 334, 56, 14)
    wheel(724, 356, 34, 10)
    rods = strokes(W, H, [([(340, 356), (592, 356)], 9, None), ([(262, 310), (340, 356)], 8, None)])
    art = GP(art, rods, "#9ea39c", "#5b605a", seed=nx(), rough=0.3)
    pins = circles(W, H, [(340, 356, 7), (466, 356, 7), (592, 356, 7)])
    art = FO(art, pins, BRASS, seed=nx(), emboss=0.5)
    # name plate on the cab side (no text)
    art = FO(art, rect(W, H, 618, 222, 728, 252, 6), BRASS, seed=nx(), emboss=0.7, sparkle=0.1)
    # overall sepia glaze + grime at the bottom
    art = OV(art, art[..., 3] * vgrad(W, H, 260, 400) * 0.35, lambda mm: rgba("#1a1209", mm))
    save_prev(art, "lokomotif", "#efe2c8")
    save(art, f"{OUT}/lokomotif.webp", max_w=860, quality=80)


def uap():
    W, H = 520, 300
    nx = Seq(61)
    rng = random.Random(7)
    art = blank(W, H)
    blobs = []
    x, y, r = 80, 230, 46
    for k in range(13):
        blobs.append((x + rng.uniform(-14, 14), y + rng.uniform(-10, 10), r * rng.uniform(0.8, 1.2), r * rng.uniform(0.7, 0.95), rng.uniform(-30, 30)))
        x += rng.uniform(24, 36)
        y -= rng.uniform(8, 16)
        r *= 1.05
    m = ellipses(W, H, blobs)
    art = G(art, m, "#f8f4ea", "#e2ddd0", seed=nx(), density=0.92, edge=0.25, bloom=0.5, rough=8, feather=4)
    sh = ellipses(W, H, [(bx + 8, by + 12, rx * 0.7, ry * 0.5, a) for bx, by, rx, ry, a in blobs[::2]]) * m
    art = G(art, sh, "#cfc8b8", "#b8b1a2", seed=nx(), density=0.45, edge=0.1, bloom=0.4, rough=6, feather=5)
    save_prev(art, "uap", bg="#7d8b84")
    save(art, f"{OUT}/uap.webp", max_w=400, quality=78)


def koper():
    W, H = 420, 360
    nx = Seq(81)
    art = blank(W, H)

    def trunk(x0, y0, x1, y1, col, col2, r=10, straps=True):
        nonlocal art
        m = rect(W, H, x0, y0, x1, y1, r)
        art = GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.9)
        art = OV(art, m * np.clip((vgrad(W, H, y0, y1) - 0.6) * 2, 0, 1), lambda mm: rgba("#24130a", mm * 0.45))
        art = OV(art, rect(W, H, x0 + 4, y0 + 3, x1 - 4, y0 + 7, 2), lambda mm: rgba("#f3d7a8", mm * 0.35))
        seam = rect(W, H, x0, (y0 + y1) / 2 - 2, x1, (y0 + y1) / 2 + 2)
        art = OV(art, seam, lambda mm: rgba("#2a160a", mm * 0.5))
        if straps:
            for sx in (x0 + (x1 - x0) * 0.25, x0 + (x1 - x0) * 0.75):
                st = rect(W, H, sx - 8, y0 - 1, sx + 8, y1 + 1, 2)
                art = GP(art, st, "#5c3a1e", "#3d2512", seed=nx(), rough=0.5)
                art = FO(art, rect(W, H, sx - 10, (y0 + y1) / 2 - 7, sx + 10, (y0 + y1) / 2 + 7, 2), BRASS, seed=nx(), emboss=0.6)
        corners = []
        for cx_, cy_ in ((x0 + 9, y0 + 9), (x1 - 9, y0 + 9), (x0 + 9, y1 - 9), (x1 - 9, y1 - 9)):
            corners.append((cx_, cy_, 9))
        art = FO(art, circles(W, H, corners), BRASS, seed=nx(), emboss=0.7, sparkle=0.1)

    trunk(30, 236, 390, 340, "#7a4a28", "#5a331a")
    trunk(70, 150, 350, 236, TEAL, TEAL_D)
    trunk(120, 82, 300, 150, "#a8693a", "#7c4a24", r=8, straps=False)
    handle = strokes(W, H, [(curve([(180, 82), (186, 62), (210, 56), (234, 62), (240, 82)], 20), 7, None)])
    art = GP(art, handle, "#4a2c14", seed=nx(), rough=0.4)
    tag = poly(W, H, [(304, 120), (338, 128), (332, 162), (298, 154)], smooth=False)
    art = GP(art, tag, CREAM, CREAM_D, seed=nx(), rough=0.5)
    art = OV(art, strokes(W, H, [([(300, 118), (292, 100), (276, 96)], 1.6, None)]), lambda mm: rgba("#5b4a35", mm))
    art = OV(art, ell(W, H, 210, 346, 190, 10), lambda mm: rgba("#2a1a0c", mm * 0.18))
    save_prev(art, "koper", "#efe2c8")
    save(art, f"{OUT}/koper.webp", max_w=320, quality=82)


def ulir():
    W, H = 460, 80
    nx = Seq(91)
    art = blank(W, H)
    items = [([(40 + 156 * t / 20, 40) for t in range(21)], 3.2, (0.3, 0.02)), ([(264 + 156 * t / 20, 40) for t in range(21)], 3.2, (0.02, 0.3)),
             (scroll(212, 32, 18, 1.2, math.pi * 0.5, sgn=1), 3.6, (0.0, 0.3)), (scroll(248, 48, 18, 1.2, -math.pi * 0.5, sgn=1), 3.6, (0.0, 0.3)),
             (scroll(178, 28, 11, 1.0, math.pi * 0.5, sgn=-1), 2.6, (0.0, 0.3)), (scroll(282, 52, 11, 1.0, -math.pi * 0.5, sgn=-1), 2.6, (0.0, 0.3))]
    art = iron(art, W, H, items, nx)
    art = FO(art, circles(W, H, [(230, 40, 6), (40, 40, 4), (420, 40, 4)]), BRASS, seed=nx(), emboss=0.6)
    save_prev(art, "ulir", "#efe2c8")
    save(art, f"{OUT}/ulir.webp", max_w=400, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
