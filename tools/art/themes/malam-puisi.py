"""Malam Puisi — a small café-theatre stage for a poetry night, painted in warm gouache: plank wall, velvet curtains,
a sagging string of bulbs, one warm spotlight on a vintage microphone, two wooden stools, open notebooks and
candles at the stage edge. Close-up mic, candle (glow split for flicker), notebook and an ink flourish divider.
Run: python3 -I malam-puisi.py [part ...]   parts: panggung mik lilin buku garis"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t6_lib import *

OUT = outdir("malam-puisi")
PARTS = sys.argv[1:] or ["panggung", "mik", "lilin", "buku", "garis"]
INK = "#2b1a14"


def mic(art, W, H, cx, top, s, nx, stand_to=None):
    """Vintage capsule microphone: chrome oval with horizontal grille ribs, yoke, and a thin stand."""
    if stand_to:
        st = strokes(W, H, [([(cx, top + s * 1.25), (cx, stand_to)], s * 0.07, None)])
        art = GP(art, st, "#3a302c", "#6b5d55", seed=nx(), rough=0.4, streak=0.3)
        art = OV(art, strokes(W, H, [([(cx - s * 0.015, top + s * 1.3), (cx - s * 0.015, stand_to)], s * 0.02, None)]), lambda m: rgba("#d8c3a2", m * 0.6))
        base = ell(W, H, cx, stand_to, s * 0.42, s * 0.08)
        art = GP(art, base, "#2a221e", "#4a3e38", seed=nx(), rough=0.6, streak=0.3)
        art = OV(art, np.clip(base - soft(base, 2) * 1.3, 0, 1) + 0 * base, lambda m: rgba("#c9a77a", m * 0.6))
    # yoke
    yk = strokes(W, H, [(arc_pts(cx, top + s * 0.62, s * 0.44, math.pi * 0.05, math.pi * 0.95, 20), s * 0.06, None),
                        ([(cx, top + s * 1.06), (cx, top + s * 1.3)], s * 0.09, None)])
    art = GP(art, yk, "#4a3e38", "#75665c", seed=nx(), rough=0.4, streak=0.3)
    body = ell(W, H, cx, top + s * 0.55, s * 0.34, s * 0.55)
    yy, xx = yx(W, H)
    art = GP(art, body, "#8f8378", "#cbbca8", seed=nx(), rough=0.5, streak=0.4)
    # chrome shading: dark core band, bright warm highlights from the spotlight above-left
    core = np.clip(1 - np.abs(xx - (cx + s * 0.08)) / (s * 0.12), 0, 1) * body
    art = OV(art, soft(core, s * 0.04), lambda m: rgba("#3c322d", m * 0.6))
    hi = np.clip(1 - np.abs(xx - (cx - s * 0.17)) / (s * 0.06), 0, 1) * body
    art = OV(art, soft(hi, s * 0.02), lambda m: rgba("#fff1d6", np.clip(m * 1.4, 0, 1) * 0.85))
    rim = np.clip(1 - np.abs(xx - (cx + s * 0.28)) / (s * 0.05), 0, 1) * body
    art = OV(art, soft(rim, s * 0.02), lambda m: rgba("#f3b25a", m * 0.6))
    ribs = []
    for k in range(-9, 10):
        y = top + s * 0.55 + k * s * 0.05
        hw = s * 0.34 * math.sqrt(max(0, 1 - (k * 0.05 / 0.55) ** 2))
        ribs.append(([(cx - hw * 0.94, y), (cx + hw * 0.94, y)], max(0.8, s * 0.012), None))
    art = OV(art, strokes(W, H, ribs) * body, lambda m: rgba("#2e2622", m * 0.55))
    band = np.clip(1 - np.abs(yy - (top + s * 0.55)) / (s * 0.05), 0, 1) * body
    art = GP(art, band, "#b8a58c", "#e6d4b5", seed=nx(), rough=0.3, streak=0.2)
    art = OV(art, np.clip(body - soft(body, 1.5) * 1.2, 0, 1), lambda m: rgba("#241c19", m * 0.7))
    return art


def stool(art, W, H, cx, seat_y, s, nx, light=1.0):
    legs = []
    for dx, foot in ((-0.42, -0.6), (0.42, 0.6), (-0.16, -0.22), (0.16, 0.24)):
        legs.append(([(cx + dx * s, seat_y + s * 0.06), (cx + foot * s, seat_y + s * 1.55)], s * (0.07 if abs(dx) > .3 else 0.055), None))
    lm = strokes(W, H, legs)
    art = GP(art, lm, "#6b4127", "#4a2b19", seed=nx(), rough=0.6, streak=0.8)
    rung = strokes(W, H, [([(cx - s * 0.5, seat_y + s * 0.95), (cx + s * 0.5, seat_y + s * 0.95)], s * 0.045, None)])
    art = GP(art, rung, "#7a4c2e", seed=nx(), rough=0.4, streak=0.6)
    seat = ell(W, H, cx, seat_y, s * 0.55, s * 0.16)
    art = GP(art, seat, "#a06a3d", "#7a4c2e", seed=nx(), rough=0.6, streak=0.8)
    edge = np.clip(ell(W, H, cx, seat_y + s * 0.07, s * 0.55, s * 0.13) - seat, 0, 1)
    art = GP(art, edge, "#5a3520", seed=nx(), rough=0.4, streak=0.5)
    art = OV(art, soft(ell(W, H, cx - s * 0.12, seat_y - s * 0.03, s * 0.3, s * 0.06), s * 0.04) * seat, lambda m: rgba("#f6c98a", m * 0.55 * light))
    return art


def notebook(art, W, H, cx, cy, s, ang, nx, rng):
    """Open notebook seen from above-front: two pages with ruled lines and handwriting squiggles."""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)
    cover = poly(W, H, [P(-1.04 * s, -0.66 * s), P(1.04 * s, -0.66 * s), P(1.04 * s, 0.7 * s), P(-1.04 * s, 0.7 * s)])
    art = GP(art, cover, "#6e2a24", "#55201c", seed=nx(), rough=0.8, streak=0.5)
    pages = []
    for side in (-1, 1):
        pts = [P(0, -0.58 * s), P(side * 0.98 * s, -0.62 * s), P(side * 0.98 * s, 0.62 * s), P(0, 0.6 * s)]
        m = shape_mask(W, H, [pts[0], P(side * 0.5 * s, -0.68 * s), pts[1], pts[2], P(side * 0.5 * s, 0.56 * s), pts[3]])
        pages.append(m)
        art = GP(art, m, "#f3e6c9", "#e6d2ad", seed=nx(), rough=0.5, streak=0.3)
        lines, hand = [], []
        for k in range(7):
            y = -0.42 * s + k * 0.14 * s
            lines.append(([P(side * 0.1 * s, y), P(side * 0.9 * s, y)], max(0.6, s * 0.008), None))
            if rng.random() < 0.85:
                x = side * 0.14 * s if side > 0 else -0.86 * s
                end = x + rng.uniform(0.35, 0.72) * s
                while x < end:
                    L = rng.uniform(0.07, 0.2) * s
                    fq = rng.uniform(55, 80) / (s / 60); amp = s * rng.uniform(0.012, 0.02); ph = rng.uniform(0, 6)
                    pts2 = [P(x + t * L + math.cos(t * fq + ph) * amp * 0.5, y - s * 0.03 + math.sin(t * fq + ph) * amp) for t in [j / 30 for j in range(31)]]
                    hand.append((pts2, max(0.6, s * 0.011), (0.05, 0.1)))
                    x += L + rng.uniform(0.03, 0.05) * s
        art = OV(art, strokes(W, H, lines) * m, lambda mm: rgba("#9fb2c4", mm * 0.5))
        art = OV(art, strokes(W, H, hand) * m, lambda mm: rgba("#2b2a44", mm * 0.75))
    gut = soft(strokes(W, H, [([P(0, -0.6 * s), P(0, 0.6 * s)], s * 0.05, None)]), s * 0.03) * np.maximum(*pages)
    art = OV(art, gut, lambda mm: rgba("#7a5a3a", mm * 0.5))
    return art


def candle(art, W, H, cx, base, h, wd, nx, glow_amt=1.0, flame=True):
    body = poly(W, H, [(cx - wd / 2, base), (cx - wd / 2, base - h), (cx - wd * 0.2, base - h - wd * 0.08), (cx + wd * 0.25, base - h + wd * 0.04), (cx + wd / 2, base - h), (cx + wd / 2, base)], smooth=False)
    art = GP(art, body, "#f1e2c4", "#d9c39b", seed=nx(), rough=0.6, streak=0.4)
    yy, xx = yx(W, H)
    shade = np.clip((xx - cx) / (wd / 2), 0, 1) * body
    art = OV(art, shade, lambda m: rgba("#a8865a", m * 0.45))
    lit = np.clip(1 - (base - h - yy) / -h * 0 - (yy - (base - h)) / (h * 0.6), 0, 1) * body
    art = OV(art, lit, lambda m: rgba("#ffd28a", m * 0.4 * glow_amt))
    drip = strokes(W, H, [([(cx - wd * 0.3, base - h), (cx - wd * 0.32, base - h + wd * 0.9)], wd * 0.16, (0.0, 0.6))])
    art = GP(art, drip, "#f7ecd6", seed=nx(), rough=0.3, streak=0.2)
    wick = strokes(W, H, [([(cx, base - h), (cx + 1, base - h - wd * 0.22)], max(1, wd * 0.06), None)])
    art = OV(art, wick, lambda m: rgba("#1c120e", m))
    if flame:
        fm = shape_mask(W, H, petal_pts(cx, base - h - wd * 0.1, wd * 0.8, wd * 0.34, -math.pi / 2, n=14))
        art = OV(art, soft(fm, 1.0), lambda m: rgba("#ffcf6a", m))
        core = shape_mask(W, H, petal_pts(cx, base - h - wd * 0.1, wd * 0.42, wd * 0.18, -math.pi / 2, n=12))
        art = OV(art, soft(core, 0.8), lambda m: rgba("#fff8e0", m))
    return art


def flames_glow(W, H, pts, col="#ffb347", radius=40, strength=0.9):
    m = circles(W, H, [(x, y, r) for x, y, r in pts])
    return glow(m, col, radius, strength)


if "panggung" in PARTS:
    W, H = 860, 1140
    rng = random.Random(31); nx = Seq(3100)
    yy, xx = yx(W, H)
    art = painted_sky(W, H, [(0, "#1d1110"), (0.5, "#2c1814"), (1, "#1a0f0d")], seed=4, streak=0.4)
    # plank wall
    pl = []
    for k in range(0, W + 60, 62):
        pl.append(([(k + rng.uniform(-2, 2), 0), (k + rng.uniform(-2, 2), 780)], 3, None))
    art = OV(art, strokes(W, H, pl), lambda m: rgba("#120a09", m * 0.6))
    grain = fbm(W, H, 7, 6, 2) * (yy < 780)
    art = OV(art, np.clip((grain - 0.55) * 3, 0, 1), lambda m: rgba("#3a2119", m * 0.35))
    # poem pages pinned on the wall (dim)
    for (x, y, a) in [(150, 300, -6), (232, 360, 4), (650, 290, 5), (720, 380, -4)]:
        pm = ellipses(W, H, [(x, y, 1, 1, 0)]) * 0
        pts = [(x - 34, y - 44), (x + 34, y - 44), (x + 34, y + 44), (x - 34, y + 44)]
        ar = math.radians(a)
        pts = [(x + (px - x) * math.cos(ar) - (py - y) * math.sin(ar), y + (px - x) * math.sin(ar) + (py - y) * math.cos(ar)) for px, py in pts]
        pm = poly(W, H, pts)
        art = GP(art, pm, "#8a7258", "#6e5a46", seed=nx(), rough=0.6, streak=0.3, density=0.8)
        ln = strokes(W, H, [([(x - 22, y - 30 + j * 11), (x + rng.uniform(4, 24), y - 30 + j * 11)], 1.6, None) for j in range(6)])
        art = OV(art, ln * pm, lambda m: rgba("#3a2a20", m * 0.6))
        art = OV(art, circles(W, H, [(pts[0][0] * .5 + pts[1][0] * .5, pts[0][1] * .5 + pts[1][1] * .5 + 5, 4)]), lambda m: rgba("#b8352c", m))
    # stage floor (perspective planks) and front edge
    floor = poly(W, H, [(0, 780), (W, 780), (W, 900), (0, 900)])
    art = GP(art, floor, "#7a4a2a", "#5a341d", seed=nx(), rough=0.8, streak=1.0, pad=2)
    fl = [([(W / 2 + (k - 7) * 30, 780), (W / 2 + (k - 7) * 78, 900)], 2.2, None) for k in range(15)]
    art = OV(art, strokes(W, H, fl) * floor, lambda m: rgba("#3a2112", m * 0.55))
    front = poly(W, H, [(0, 900), (W, 900), (W, H), (0, H)])
    art = GP(art, front, "#2a1610", "#1d0f0b", seed=nx(), rough=0.6, streak=0.6, pad=2)
    art = OV(art, strokes(W, H, [([(0, 902), (W, 902)], 5, None)]), lambda m: rgba("#a0703f", m * 0.8))
    # spotlight: cone + pool
    cone = poly(W, H, [(W / 2 - 40, -10), (W / 2 + 40, -10), (W / 2 + 250, 860), (W / 2 - 250, 860)])
    cone = soft(cone, 30) * np.clip(1 - yy / 1000, 0.25, 1)
    art = add_light(art, cone, "#ffcf8a", 0.32)
    pool = soft(ell(W, H, W / 2, 830, 280, 60), 26)
    art = add_light(art, pool, "#ffc070", 0.55)
    # curtains
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        pts = [(x0, -10), (x0 - side * -150, -10), (x0 - side * -120, 300), (x0 - side * -80, 560), (x0 - side * -100, 905), (x0, 905)]
        pts = [(x0 + side * -1 * (x0 - p[0]) if False else p[0], p[1]) for p in pts]
        cm = poly(W, H, [(x0, -10), (x0 + (-side) * 150, -10), (x0 + (-side) * 118, 300), (x0 + (-side) * 70, 560), (x0 + (-side) * 104, 905), (x0, 905)], smooth=True)
        art = GP(art, cm, "#6e1620", "#4a0d14", seed=nx(), rough=1.0, streak=1.2, pad=2)
        folds = [([(x0 + (-side) * f, -10), (x0 + (-side) * (f * 0.72), 560), (x0 + (-side) * (f * 0.86), 905)], 10, (0.0, 0.0)) for f in (30, 66, 102, 130)]
        art = OV(art, soft(strokes(W, H, folds), 6) * cm, lambda m: rgba("#2a0509", m * 0.55))
        hl = [([(x0 + (-side) * (f + 12), -10), (x0 + (-side) * ((f + 12) * 0.72), 560), (x0 + (-side) * ((f + 12) * 0.86), 905)], 5, (0.0, 0.0)) for f in (48, 86)]
        art = OV(art, soft(strokes(W, H, hl), 4) * cm, lambda m: rgba("#c0424a", m * 0.35))
    valance = poly(W, H, [(0, -10), (W, -10), (W, 70)] + [(W - k * W / 8 - W / 16, 70 + 26 * (1 if k % 2 == 0 else 0.0)) for k in range(8)] + [(0, 70)], smooth=True)
    art = GP(art, valance, "#7a1a24", "#560f17", seed=nx(), rough=1.0, streak=1.0, pad=2)
    art = OV(art, strokes(W, H, [([(0, 64 + 8 * math.sin(k / 3)) if False else (k * 20, 66) for k in range(0, 45)], 3, None)]), lambda m: rgba("#c99a45", m * 0.7))
    # string lights
    wire = [(x, 120 + 46 * math.sin(math.pi * ((x % 430) / 430))) for x in range(0, W + 1, 10)]
    art = OV(art, strokes(W, H, [(wire, 2, None)]), lambda m: rgba("#0e0807", m * 0.9))
    bulbs = [(wire[i][0], wire[i][1] + 10, 7) for i in range(3, len(wire) - 2, 6)]
    bm = circles(W, H, bulbs)
    art = add_light(art, gaussian_filter(bm, 14) * 2.2, "#ffb14a", 0.5)
    art = OV(art, bm, lambda m: rgba("#ffe2a0", m))
    # stools, notebook, mic
    art = stool(art, W, H, 238, 600, 110, nx, light=0.6)
    art = stool(art, W, H, 640, 620, 100, nx, light=0.6)
    art = notebook(art, W, H, 640, 606, 62, -0.12, nx, rng)
    art = mic(art, W, H, W / 2, 330, 120, nx, stand_to=820)
    # books stack + candles at the stage front
    for i, (w_, c) in enumerate([(130, "#3e5a4a"), (118, "#7a2a24"), (124, "#c99a45")]):
        bk = poly(W, H, [(70 + i * 4, 880 - i * 24), (70 + w_ + i * 4, 880 - i * 24), (70 + w_ + i * 4, 900 - i * 24), (70 + i * 4, 900 - i * 24)])
        art = GP(art, bk, c, mix(c, "#000000", .3), seed=nx(), rough=0.4, streak=0.6)
        art = OV(art, strokes(W, H, [([(72 + i * 4, 891 - i * 24), (66 + w_ + i * 4, 891 - i * 24)], 1.4, None)]), lambda m: rgba("#f3e6c9", m * 0.5))
    art = notebook(art, W, H, 500, 870, 52, 0.06, nx, rng)
    cs = [(150, 834, 46, 22), (186, 846, 30, 20), (708, 888, 64, 24), (744, 896, 40, 20), (676, 896, 28, 18)]
    gl = [(x, b - h - 12, 8) for x, b, h, w_ in cs]
    art = add_light(art, np.clip(gaussian_filter(circles(W, H, gl), 30) * 30, 0, 1), "#ffa94a", 0.75)
    art = add_light(art, np.clip(gaussian_filter(circles(W, H, gl), 10) * 10, 0, 1), "#ffd27a", 0.6)
    for x, b, h, w_ in cs:
        art = candle(art, W, H, x, b, h, w_, nx)
    art = vignette(art, 0.45, 1.4)
    fade = np.clip((yy - (H - 170)) / 170, 0, 1)[..., None]
    art[..., :3] = art[..., :3] * (1 - fade) + np.array(hex_rgb("#1d1210"), np.float32) * fade
    prev(art, "puisi-panggung", bg="#000000")
    save_rgb(art, f"{OUT}/panggung.webp", size=(860, 1140), quality=76)
    clear()

if "mik" in PARTS:
    W, H = 320, 520
    nx = Seq(4100)
    a = mic(blank(W, H), W, H, W / 2, 30, 200, nx)
    prev(a, "puisi-mik", bg="#2b1a14")
    save(a, f"{OUT}/mik.webp", max_w=150, quality=84)

if "lilin" in PARTS:
    W, H = 200, 300
    nx = Seq(4300)
    a = candle(blank(W, H), W, H, 100, 280, 150, 46, nx, flame=False)
    prev(a, "puisi-lilin", bg="#2b1a14")
    save_full(a, f"{OUT}/lilin.webp", size=(100, 150), quality=84)
    f = blank(W, H)
    f = over(f, glow(circles(W, H, [(100, 112, 14)]), "#ffb347", 26, 0.9))
    f = candle(f, W, H, 100, 280, 150, 46, nx, flame=True)
    fl = blank(W, H)
    fm = np.clip(f[..., 3] * (yx(W, H)[0] < 132), 0, 1)
    fl = f.copy(); fl[..., 3] = fm
    prev(fl, "puisi-api", bg="#2b1a14")
    save_full(fl, f"{OUT}/api.webp", size=(100, 150), quality=84)

if "buku" in PARTS:
    W, H = 560, 380
    rng = random.Random(5); nx = Seq(4500)
    a = notebook(blank(W, H), W, H, W / 2, H / 2, 240, -0.04, nx, rng)
    pen = strokes(W, H, [([(380, 300), (520, 120)], 12, (0.05, 0.1))])
    a = GP(a, pen, "#1f1a2e", "#3a3150", seed=nx(), rough=0.4, streak=0.3)
    a = OV(a, strokes(W, H, [([(376, 305), (390, 287)], 6, None)]), lambda m: rgba("#c99a45", m))
    prev(a, "puisi-buku", bg="#2b1a14")
    save(a, f"{OUT}/buku.webp", max_w=360, quality=82)

if "garis" in PARTS:
    W, H = 760, 120
    nx = Seq(4700)
    pts = [(40 + t * 680, 60 + math.sin(t * math.pi * 3) * 10 * (1 - abs(t - .5) * 2)) for t in [j / 80 for j in range(81)]]
    loop = [(380 + math.cos(a) * 26 - 0, 60 + math.sin(a) * 18) for a in [j / 40 * math.tau for j in range(41)]]
    m = strokes(W, H, [(pts[:38], 3.2, (0.6, 0.0)), (loop, 2.4, (0.1, 0.1)), (pts[43:], 3.2, (0.0, 0.6))])
    a = LC(blank(W, H), m, "#c99a45", seed=nx(), wear=0.2, rough=0.8)
    dot = circles(W, H, [(380, 60, 6)])
    a = LC(a, dot, "#c99a45", seed=nx(), wear=0.1)
    prev(a, "puisi-garis", bg="#2b1a14")
    save(a, f"{OUT}/garis.webp", max_w=380, quality=84)
