"""Khitan Pangeran — little-prince khitanan in gouache + gold foil: a domed palace, a jewelled crown, pennant bunting,
8-point stars, crescent moon, royal-blue star-lattice tile. No figures (Islamic theme).
Run: python3 -I khitan-pangeran.py [part ...]  parts: palace crown bunting star moon tile flag
Assets -> public/themes/art/khitan-pangeran/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *

OUT = outdir("khitan-pangeran")
PARTS = sys.argv[1:] or ["palace", "crown", "bunting", "star", "moon", "tile"]
BLUE, BLUE_D, BLUE_L = "#2f5cc4", "#163584", "#5f8ae2"
GOLD = "#d9a93f"
IVORY, IVORY_D = "#fbf1dc", "#e8d3ad"
RED = "#c8413a"


def onion(cx, by, w, h):
    prof = [(0, 0.42), (0.12, 0.52), (0.3, 0.55), (0.5, 0.44), (0.68, 0.26), (0.82, 0.1), (0.93, 0.03), (1.0, 0.0)]
    L = [(cx - w * p, by - h * t) for t, p in prof]
    R = [(cx + w * p, by - h * t) for t, p in prof[::-1]][1:]
    return L + R


def arch(cx, by, w, h, n=10):
    """Pointed (ogee-ish) arch opening as polygon."""
    pts = [(cx - w / 2, by), (cx - w / 2, by - h * 0.55)]
    pts += [(cx - w / 2 + w / 2 * (1 - math.cos(t * math.pi / 2)), by - h * 0.55 - h * 0.45 * math.sin(t * math.pi / 2) ** 0.8) for t in np.linspace(0.15, 1, n)]
    pts += [(2 * cx - x, y) for x, y in pts[::-1]][1:]
    return pts


def star8(cx, cy, r, rot=0.0, inner=0.72):
    pts = []
    for k in range(16):
        a = rot + k * math.pi / 8
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def form(art, W, H, m, col, col2, nx, light=(-1, -1), dark=None, k=10):
    """Gouache shape with a soft shadow side and a lit side."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.3)
    sh = inner_shade(m, -int(light[0] * k), -int(light[1] * k), blur=k * 0.8)
    art = G(art, sh, dark or mix(col, "#0a1440", 0.45), seed=nx(), density=0.45, edge=0.05, bloom=0.2, rough=0.6, feather=0.6)
    hi = inner_shade(m, int(light[0] * k * 0.7), int(light[1] * k * 0.7), blur=k * 0.6)
    art = G(art, hi * 0.7, "#ffffff", seed=nx(), density=0.22, edge=0, bloom=0.2, rough=0.6, feather=0.6)
    return art


if "palace" in PARTS:
    W, H = 780, 560
    rng = random.Random(5); nx = Seq(500)
    art = blank(W, H)
    GY = 536
    # ground shadow & lawn
    art = G(art, shapes(W, H, [deform(ellipse_pts(390, GY + 6, 380, 20, 18), rng, 1, 0.03)]), "#0c1a40", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=5)
    # towers (minarets)
    for tx in (78, 702):
        body = shapes(W, H, [[(tx - 22, GY), (tx - 22, 230), (tx + 22, 230), (tx + 22, GY)]], smooth=False)
        art = form(art, W, H, body, IVORY, IVORY_D, nx, k=8)
        bal = shapes(W, H, [[(tx - 32, 236), (tx + 32, 236), (tx + 26, 252), (tx - 26, 252)]], smooth=False)
        art = GP(art, bal, BLUE, BLUE_D, seed=nx(), rough=0.6)
        art = FO(art, strokes(W, H, [([(tx - 32, 236), (tx + 32, 236)], 4, None), ([(tx - 22, 380), (tx + 22, 380)], 3, None)]), GOLD, seed=nx(), emboss=0.6)
        dome = shapes(W, H, [onion(tx, 230, 46, 70)])
        art = form(art, W, H, dome, BLUE_L, BLUE, nx, k=6)
        art = FO(art, strokes(W, H, [([(tx, 160), (tx, 132)], 3, None)]) + circles(W, H, [(tx, 156, 5)]), GOLD, seed=nx())
        for wy in (300, 440):
            win = shapes(W, H, [arch(tx, wy + 36, 16, 36)], smooth=False)
            art = GP(art, win, "#ffd76a", "#f1a93a", seed=nx(), rough=0.4)
            art = G(art, glow(win, "#ffe39a", 6, 0.5)[..., 3], "#ffe39a", seed=nx(), density=0.25, edge=0, bloom=0, rough=1)
    # wings
    for x0, x1 in ((100, 250), (530, 680)):
        cx = (x0 + x1) / 2
        body = shapes(W, H, [[(x0, GY), (x0, 380), (x1, 380), (x1, GY)]], smooth=False)
        art = form(art, W, H, body, IVORY, IVORY_D, nx, k=9)
        dome = shapes(W, H, [onion(cx, 384, 92, 104)])
        art = form(art, W, H, dome, BLUE_L, BLUE, nx, k=8)
        art = FO(art, strokes(W, H, [(curve([(cx - 30, 380), (cx - 22, 330), (cx, 282)], 14), 2.5, None), (curve([(cx + 30, 380), (cx + 22, 330), (cx, 282)], 14), 2.5, None),
                                     ([(cx, 282), (cx, 250)], 3, None)]) + circles(W, H, [(cx, 268, 5.5)]), GOLD, seed=nx())
        for wx in (cx - 40, cx, cx + 40):
            win = shapes(W, H, [arch(wx, 470, 24, 52)], smooth=False)
            art = GP(art, win, "#ffd76a", "#f1a93a", seed=nx(), rough=0.4)
            art = FO(art, outline(win, 4), GOLD, seed=nx(), emboss=0.5)
        trim = circles(W, H, [(x, 380, 7) for x in np.arange(x0 + 7, x1, 14)]) * (np.arange(H)[:, None] < 381)
        art = FO(art, trim + strokes(W, H, [([(x0, 382), (x1, 382)], 4, None)]), GOLD, seed=nx(), emboss=0.6)
    # main hall + drum + great dome
    hall = shapes(W, H, [[(240, GY), (240, 300), (540, 300), (540, GY)]], smooth=False)
    art = form(art, W, H, hall, IVORY, IVORY_D, nx, k=12)
    drum = shapes(W, H, [[(300, 304), (300, 270), (480, 270), (480, 304)]], smooth=False)
    art = form(art, W, H, drum, IVORY, IVORY_D, nx, k=6)
    for wx in np.arange(318, 480, 24):
        art = GP(art, shapes(W, H, [arch(wx, 298, 9, 20)], smooth=False), BLUE_D, seed=nx(), rough=0.3)
    dome = shapes(W, H, [onion(390, 274, 210, 214)])
    art = form(art, W, H, dome, BLUE_L, BLUE, nx, k=16)
    ribs = strokes(W, H, [(curve([(390 + dx, 272), (390 + dx * 1.22, 205), (390 + dx * 0.55, 130), (390, 62)], 30), 3.5, None) for dx in (-70, -35, 0, 35, 70)])
    art = FO(art, ribs * dome, GOLD, seed=nx(), emboss=0.6)
    band = strokes(W, H, [([(282, 272), (498, 272)], 9, None)])
    art = FO(art, band, GOLD, seed=nx(), emboss=0.7)
    art = FO(art, strokes(W, H, [([(390, 64), (390, 18)], 4, None)]) + circles(W, H, [(390, 52, 8), (390, 30, 5)]), GOLD, seed=nx(), sparkle=0.3)
    dots = circles(W, H, [(390 + dx * 1.0, y, 3.2) for dx, y in [(-90, 236), (-52, 236), (52, 236), (90, 236), (-62, 180), (62, 180), (-20, 180), (20, 180)]]) * dome
    art = FO(art, dots, GOLD, seed=nx())
    # crenellation on the hall roof
    cren = circles(W, H, [(x, 300, 8) for x in np.arange(248, 540, 16)]) * (np.arange(H)[:, None] < 301)
    art = FO(art, cren + strokes(W, H, [([(240, 302), (540, 302)], 5, None)]), GOLD, seed=nx(), emboss=0.6)
    # great door + windows
    door = shapes(W, H, [arch(390, GY, 92, 160)], smooth=False)
    art = form(art, W, H, door, BLUE, BLUE_D, nx, k=8)
    art = FO(art, outline(door, 7), GOLD, seed=nx(), emboss=0.7)
    art = FO(art, strokes(W, H, [([(390, GY - 4), (390, GY - 120)], 2.5, None)]) + circles(W, H, [(376, GY - 64, 3.5), (404, GY - 64, 3.5)]), GOLD, seed=nx())
    for wx in (282, 498):
        win = shapes(W, H, [arch(wx, 440, 40, 90)], smooth=False)
        art = GP(art, win, "#ffd76a", "#f1a93a", seed=nx(), rough=0.4)
        art = G(art, win * hatch(W, H, 1.57, 10, 0.12, 3), "#c47d24", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
        art = FO(art, outline(win, 5), GOLD, seed=nx(), emboss=0.6)
    for wx in (282, 340, 440, 498):
        st = shapes(W, H, [star8(wx, 344, 12, 0.2)], smooth=False)
        art = FO(art, st, GOLD, seed=nx(), emboss=0.7)
    # steps
    for k, (w_, y) in enumerate([(150, GY - 4), (120, GY - 14)]):
        art = GP(art, shapes(W, H, [[(390 - w_ / 2, y + 10), (390 - w_ / 2, y), (390 + w_ / 2, y), (390 + w_ / 2, y + 10)]], smooth=False), "#e9dcc0", "#d8c39c", seed=nx(), rough=0.6)
    # pennants on tower tips
    for tx, d in ((78, 1), (702, -1)):
        pen = shapes(W, H, [[(tx, 132), (tx + d * 46, 140), (tx, 150)]], smooth=False)
        art = GP(art, pen, RED, "#a52f2a", seed=nx(), rough=0.8)
    # flowering bushes at the base
    for bx in (30, 200, 580, 750):
        bm = shapes(W, H, [deform(ellipse_pts(bx, GY - 8, 48, 26, 12), rng, 2, 0.08)])
        art = form(art, W, H, bm, "#3f8a55", "#2e6a43", nx, k=6)
        fl = circles(W, H, [(bx + rng.uniform(-36, 36), GY - 10 + rng.uniform(-16, 8), rng.uniform(3, 5)) for _ in range(9)])
        art = GP(art, fl, "#ffd76a", "#f6b2a0", seed=nx(), rough=0.3)
    clear()
    preview(art, "kp-palace", bg="#1d3a8f")
    save(art, f"{OUT}/palace.webp", max_w=780, quality=82)
    clear()

if "crown" in PARTS:
    W, H = 420, 320
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    cap = shapes(W, H, [deform(ellipse_pts(210, 170, 120, 90, 16), rng, 1, 0.02)])
    art = form(art, W, H, cap, "#c8413a", "#8e2420", nx, k=10)
    pts = [(70, 250), (60, 110), (120, 170), (160, 80), (210, 150), (260, 80), (300, 170), (360, 110), (350, 250)]
    body = shapes(W, H, [deform(pts, rng, 1, 0.01)], smooth=False)
    art = G(art, np.roll(np.roll(body, 8, 0), 6, 1), "#0c1a40", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=2, feather=5)
    art = FO(art, body, GOLD, seed=nx(), emboss=0.8, sparkle=0.1)
    sh = inner_shade(body, 10, 6, 7)
    art = G(art, sh, "#8a5a12", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1)
    band = shapes(W, H, [[(66, 256), (64, 214), (356, 214), (354, 256)]], smooth=False)
    art = FO(art, band, "#e7bf5a", seed=nx(), emboss=0.9, sparkle=0.1)
    art = G(art, inner_shade(band, 0, 8, 5), "#8a5a12", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    balls = circles(W, H, [(60, 104, 13), (160, 74, 14), (260, 74, 14), (360, 104, 13)])
    art = FO(art, balls, GOLD, seed=nx(), emboss=0.9, sparkle=0.12)
    top = circles(W, H, [(210, 140, 16)])
    art = FO(art, top, GOLD, seed=nx(), emboss=0.9, sparkle=0.12)
    for (x, y, r, c) in [(120, 236, 13, RED), (210, 236, 16, BLUE), (300, 236, 13, "#2f9a63"), (210, 182, 11, RED), (160, 236, 6, "#ffffff"), (255, 236, 6, "#ffffff")]:
        gm = circles(W, H, [(x, y, r)]) if c != RED or r != 11 else shapes(W, H, [[(x, y - r * 1.3), (x + r, y), (x, y + r * 1.3), (x - r, y)]], smooth=False)
        art = form(art, W, H, gm, mix(c, "#ffffff", 0.2), c, nx, k=4)
        art = GP(art, circles(W, H, [(x - r * 0.35, y - r * 0.35, max(1.5, r * 0.25))]), "#ffffff", seed=nx(), rough=0.2)
    preview(art, "kp-crown", bg="#1d3a8f")
    save(art, f"{OUT}/crown.webp", max_w=300, quality=84)
    clear()

if "bunting" in PARTS:
    W, H = 800, 150
    rng = random.Random(13); nx = Seq(1300)
    art = blank(W, H)
    line = curve([(0, 16), (200, 52), (400, 64), (600, 52), (800, 16)], 120)
    art = GP(art, strokes(W, H, [(line, 3, None)]), "#7a5a22", seed=nx(), rough=0.4)
    cols = [BLUE, GOLD, RED, IVORY]
    for k, (x, y, a) in enumerate(along(line, 50)):
        if x < 12 or x > W - 12:
            continue
        ca_, sa_ = math.cos(a), math.sin(a)
        p0 = (x - ca_ * 20, y - sa_ * 20); p1 = (x + ca_ * 20, y + sa_ * 20); tip = (x - sa_ * -58 * 0 + 0, y + 62)
        tri = shapes(W, H, [[p0, p1, (x + rng.uniform(-3, 3), y + 62)]], smooth=False)
        c = cols[k % 4]
        if c == GOLD:
            art = FO(art, tri, GOLD, seed=nx(), emboss=0.6)
        else:
            art = form(art, W, H, tri, c, mix(c, "#000000", 0.15), nx, k=5)
        dm = shapes(W, H, [star8(x, y + 22, 7, 0.0)], smooth=False)
        if c == GOLD:
            art = GP(art, dm, BLUE, seed=nx(), rough=0.3)
        else:
            art = FO(art, dm, GOLD, seed=nx(), emboss=0.5)
    preview(art, "kp-bunting", bg="#1d3a8f")
    save(art, f"{OUT}/bunting.webp", max_w=780, quality=82)
    clear()

if "star" in PARTS:
    W, H = 120, 120
    nx = Seq(1500)
    art = blank(W, H)
    st = shapes(W, H, [star8(60, 60, 50, 0.0, 0.74)], smooth=False)
    art = FO(art, st, GOLD, seed=nx(), emboss=0.9, sparkle=0.12)
    art = GP(art, shapes(W, H, [star8(60, 60, 22, math.pi / 8, 0.74)], smooth=False), BLUE, BLUE_D, seed=nx(), rough=0.3)
    art = FO(art, circles(W, H, [(60, 60, 7)]), GOLD, seed=nx())
    preview(art, "kp-star", bg="#1d3a8f")
    save(art, f"{OUT}/star.webp", max_w=72, quality=86)

if "moon" in PARTS:
    W, H = 220, 220
    nx = Seq(1700)
    art = blank(W, H)
    m = np.clip(circles(W, H, [(110, 110, 80)]) - circles(W, H, [(146, 88, 70)]), 0, 1)
    art = G(art, glow(m, "#ffe7a0", 16, 0.6)[..., 3], "#ffe7a0", seed=nx(), density=0.5, edge=0, bloom=0, rough=2)
    art = FO(art, m, "#e6bb55", seed=nx(), emboss=0.9, sparkle=0.1)
    preview(art, "kp-moon", bg="#1d3a8f")
    save(art, f"{OUT}/moon.webp", max_w=140, quality=84)

if "flag" in PARTS:
    # swallow-tail royal banner on a gold pole (divider centre / sent art)
    W, H = 220, 200
    rng = random.Random(19); nx = Seq(1900)
    art = blank(W, H)
    pole = strokes(W, H, [([(40, 196), (40, 20)], 6, None)])
    art = FO(art, pole + circles(W, H, [(40, 16, 9)]), GOLD, seed=nx(), emboss=0.7)
    flag = shapes(W, H, [[(43, 28), (120, 40), (200, 30), (176, 62), (204, 96), (120, 84), (43, 94)]])
    art = form(art, W, H, flag, BLUE_L, BLUE, nx, k=8)
    wave = strokes(W, H, [(curve([(60, 34), (120, 50), (180, 40)], 20), 3, None), (curve([(60, 88), (120, 76), (180, 86)], 20), 3, None)]) * flag
    art = FO(art, wave, GOLD, seed=nx(), emboss=0.5)
    art = FO(art, shapes(W, H, [star8(110, 62, 14, 0.1)], smooth=False), GOLD, seed=nx(), emboss=0.7)
    preview(art, "kp-flag", bg="#fbf1dc")
    save(art, f"{OUT}/flag.webp", max_w=140, quality=84)

if "tile" in PARTS:
    # seamless royal-blue tile: faint star lattice + tiny gold dots (gouache streaks)
    S = 240
    rng = random.Random(23); nx = Seq(2300)
    n = wrap_noise(S, S, 5, 18) * 0.6 + wrap_noise(S, S, 6, 1.0) * 0.4
    base = np.concatenate([np.array(hex_rgb("#1d3a90"), np.float32) * (0.94 + 0.12 * n)[..., None], np.ones((S, S, 1), np.float32)], -1)
    items = []
    for ox in (-S, 0, S):
        for oy in (-S, 0, S):
            items.append(star8(ox + S / 2, oy + S / 2, 40, 0, 0.7))
            items.append(star8(ox, oy, 40, 0, 0.7))
    stars = np.clip(shapes(S, S, items, smooth=False) - shapes(S, S, [p for p in [star8(ox + cx, oy + cy, 33, 0, 0.7) for ox in (-S, 0, S) for oy in (-S, 0, S) for cx, cy in ((S / 2, S / 2), (0, 0))]], smooth=False), 0, 1)
    art = over(base, np.concatenate([np.ones((S, S, 3), np.float32) * np.array(hex_rgb("#3a5cb8"), np.float32), (stars * 0.55)[..., None]], -1))
    d = circles(S, S, [(x, y, 2.2) for x, y in [(S / 2, 0), (0, S / 2), (S / 2, S), (S, S / 2)]])
    art = over(art, foil(d, GOLD, seed=5))
    save_rgb(art, f"{OUT}/tile.webp", quality=74)

kb(OUT)
