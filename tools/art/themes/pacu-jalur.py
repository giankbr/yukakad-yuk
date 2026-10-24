"""Pacu Jalur — the long carved jalur boats of Kuantan Singingi racing on the Kuantan river, in festive Melayu gouache:
a long jalur with painted prow and stern, a row of stylised rowers with paddles biting the water, a dancer at the prow;
the river with the far bank (trees, rumah panggung, crowd); a tall umbul-umbul banner on a bamboo pole; a bunting of
pennants; a mini jalur divider; the carved prow head. Palette: river jade-olive, Melayu yellow, red, green, teak.
Run: python3 -I pacu-jalur.py [part ...]   parts: jalur river umbul bunting mini prow
Assets -> public/themes/art/pacu-jalur/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q1_lib import *  # noqa

OUT = outdir("pacu-jalur")
PARTS = sys.argv[1:] or ["jalur", "river", "umbul", "bunting", "mini", "prow"]
TEAK, TEAK_D, TEAK_L = "#5a3420", "#2e1a10", "#8a5632"
YEL, YEL_L = "#e9b52c", "#f6d36a"
RED, RED_D = "#c0352a", "#8a2219"
GRN, GRN_D = "#2f7a4c", "#1d4f33"
INK = "#2a1a12"
CREAM = "#f6ead0"
WATER, WATER_D, WATER_L = "#5f8770", "#33584a", "#a9c4a6"


def hull_pts(x0, x1, wl, top_mid, h, rise_s, rise_p, n=40):
    """Long slim hull: gunwale curve on top, keel curve below, both sweeping up at the ends."""
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        up = rise_s * (1 - t) ** 6 + rise_p * t ** 7
        top.append((x, top_mid - up))
        bot.append((x, top_mid + h * (math.sin(math.pi * t) ** 0.35) - up * 0.9))
    return top, bot


def prow_head(W, H, x, y, s, d=1):
    """Carved prow ornament: a tall neck curling forward into a spiral head with a crest (stylised, not a real animal)."""
    neck = curve([(x - 30 * s * d, y + 40 * s), (x - 6 * s * d, y + 10 * s), (x + 6 * s * d, y - 30 * s), (x + 2 * s * d, y - 70 * s), (x + 22 * s * d, y - 96 * s)], 40)
    curl = spiral_scroll(x + 30 * s * d, y - 86 * s, 16 * s, math.pi * (1.25 if d > 0 else -0.25), 1.1, d=d, n=30)
    crest = [(x - 2 * s * d, y - 64 * s), (x - 26 * s * d, y - 84 * s), (x - 14 * s * d, y - 60 * s), (x - 30 * s * d, y - 58 * s), (x - 6 * s * d, y - 44 * s)]
    m_neck = strokes(W, H, [(neck, 16 * s, (0.0, 0.1)), (curl, 11 * s, (0.0, 0.6))])
    m_crest = poly(W, H, crest, smooth=True)
    return m_neck, m_crest, neck, curl


def rower(x, y, s, lean=0.5):
    """Stylised seated rower facing the prow (right): torso leaning forward, head, arms to the paddle."""
    hx, hy = x + 8 * s * lean, y - 26 * s
    torso = [(x - 6 * s, y), (x - 3 * s, y - 16 * s), (hx - 1 * s, hy + 6 * s), (hx + 6 * s, hy + 8 * s), (x + 7 * s, y - 10 * s), (x + 6 * s, y)]
    return torso, (hx, hy, 5.2 * s)


def part_jalur():
    W, H = 900, 270
    nx = Seq(100); rng = random.Random(11)
    art = blank(W, H)
    x0, x1, mid = 50, 820, 176
    top, bot = hull_pts(x0, x1, 196, mid, 34, 38, 60)
    hull = poly(W, H, top + bot[::-1], smooth=True)
    # paddles behind the hull (far side) — thin, darker
    paddles, blades, splashes = [], [], []
    xs = np.linspace(150, 735, 22)
    rowers = []
    for k, x in enumerate(xs):
        yy = mid - 2 - (38 * (1 - (x - x0) / (x1 - x0)) ** 6)
        ph = (k * 0.9) % 1.0
        ang = math.radians(118 + 14 * math.sin(k * 1.7))
        hand = (x + 4, yy - 16)
        tip = (hand[0] + math.cos(ang) * -62 * -1, hand[1] + 62)
        tip = (hand[0] - 26 - 6 * math.sin(k), hand[1] + 60)
        paddles.append(([hand, tip], 3.2, (0, 0.1)))
        blades.append((tip[0] - 2, tip[1] - 2, 4.5, 10, 25))
        for j in range(3):
            splashes.append(([(tip[0] - 8 + j * 6, tip[1] + 2), (tip[0] - 14 + j * 9, tip[1] - 6 - j * 2)], 2.2, (0.2, 0.5)))
        rowers.append(rower(x, yy, 1.0, 0.6 + 0.3 * math.sin(k * 0.8)))
    art = body(art, strokes(W, H, paddles), TEAK_L, seed=nx(), shade=0.2, rough=0.8)
    art = body(art, ellipses(W, H, blades), "#b9783f", seed=nx(), shade=0.2, rough=0.8)
    dip = np.maximum(strokes(W, H, paddles), ellipses(W, H, blades)) * ygrad(W, H, 204, 214)
    art = OV(art, dip, lambda mm: tint(mm, WATER, 0.7))
    # rowers (silhouettes) with yellow head cloths
    tor = shapes(W, H, [t for t, _ in rowers], smooth=True)
    heads = circles(W, H, [h for _, h in rowers])
    art = body(art, tor, "#3a2419", "#4a2e20", seed=nx(), shade=0.25, dark="#120a06", rough=1.2)
    art = body(art, heads, "#3a2419", seed=nx(), shade=0.2, rough=0.8)
    cloth = shapes(W, H, [[(hx - r, hy - r * 0.1), (hx - r * 0.8, hy - r * 0.9), (hx + r * 0.6, hy - r * 1.05), (hx + r * 1.1, hy - r * 0.2), (hx - r * 2.2, hy + r * 0.3)] for _, (hx, hy, r) in rowers], smooth=True)
    art = body(art, cloth, YEL, YEL_L, seed=nx(), shade=0.15, rough=0.8)
    clear()
    # hull: teak with painted bands
    art = body(art, hull, TEAK, TEAK_L, seed=nx(), shade=0.45, dark=TEAK_D, rough=1.4)
    t2, b2 = hull_pts(x0 + 30, x1 - 26, 196, mid + 6, 9, 36, 56)
    band_y = poly(W, H, t2 + b2[::-1], smooth=True) * hull
    art = body(art, band_y, YEL, YEL_L, seed=nx(), shade=0.15, rough=0.8)
    t3, b3 = hull_pts(x0 + 40, x1 - 40, 196, mid + 15, 8, 34, 52)
    band_r = poly(W, H, t3 + b3[::-1], smooth=True) * hull
    art = body(art, band_r, RED, seed=nx(), shade=0.2, rough=0.8)
    # dotted motif (pucuk rebung-like small triangles) on the yellow band
    tris = []
    for x in range(110, 770, 16):
        t = (x - x0 - 30) / (x1 - x0 - 56)
        yb = mid + 6 - (36 * (1 - t) ** 6 + 56 * t ** 7)
        tris.append([(x - 4, yb + 9), (x + 4, yb + 9), (x, yb + 2)])
    art = GP(art, shapes(W, H, tris, smooth=False) * band_y, GRN, seed=nx(), rough=0.6)
    dots = circles(W, H, [(x + 8, mid + 18.5 - (34 * (1 - (x + 8 - x0 - 40) / (x1 - x0 - 80)) ** 6 + 52 * ((x + 8 - x0 - 40) / (x1 - x0 - 80)) ** 7), 1.8) for x in range(110, 760, 16)])
    art = GP(art, dots * band_r, CREAM, seed=nx(), rough=0.4)
    art = line(art, [(top, 2.6, (0.02, 0.02))], nx(), col=TEAK_D)
    clear()
    # prow (right) and stern curl (left)
    pm_neck, pm_crest, neck, curl = prow_head(W, H, 828, 112, 1.05, 1)
    art = body(art, pm_crest, RED, seed=nx(), shade=0.25)
    art = body(art, pm_neck, YEL, "#d89c22", seed=nx(), shade=0.35, dark=RED_D, rough=1.0)
    art = line(art, [(neck[8:], 2.2, (0.1, 0.2)), (curl, 2.0, (0.0, 0.4))], nx(), col=RED_D)
    art = GP(art, circles(W, H, [(neck[24][0] + 3, neck[24][1], 3.2)]), GRN, seed=nx(), rough=0.4)
    stern = strokes(W, H, [(curve([(64, 150), (44, 132), (36, 108), (46, 92), (58, 100)], 30), 10, (0.0, 0.5))])
    art = body(art, stern, YEL, seed=nx(), shade=0.3, dark=RED_D)
    # stern flag pole with a small umbul
    art = line(art, [([(70, 150), (66, 40)], 3, (0, 0))], nx(), col=TEAK_D)
    fl = poly(W, H, [(67, 42), (112, 52), (100, 60), (114, 70), (67, 66)])
    art = body(art, fl, RED, seed=nx(), shade=0.2)
    art = GP(art, poly(W, H, [(67, 52), (106, 58), (67, 60)]) * fl, YEL, seed=nx(), rough=0.5)
    # dancer at the prow (tukang tari) and steersman at the stern — silhouettes
    dx, dy = 790, 128
    dancer = shapes(W, H, [[(dx - 5, dy + 30), (dx - 4, dy + 8), (dx - 6, dy - 6), (dx + 5, dy - 6), (dx + 4, dy + 8), (dx + 6, dy + 30)]], smooth=True)
    arms = strokes(W, H, [([(dx - 4, dy - 2), (dx - 18, dy - 12), (dx - 24, dy - 22)], 3.4, (0, 0.2)), ([(dx + 4, dy - 2), (dx + 16, dy - 8), (dx + 26, dy - 4)], 3.4, (0, 0.2))])
    art = body(art, np.maximum(dancer, arms), "#3a2419", seed=nx(), shade=0.2)
    art = body(art, circles(W, H, [(dx, dy - 13, 5.6)]), "#3a2419", seed=nx(), shade=0.1)
    art = body(art, poly(W, H, [(dx - 6, dy + 6), (dx + 6, dy + 6), (dx + 9, dy + 22), (dx - 9, dy + 22)]), RED, seed=nx(), shade=0.15)
    art = GP(art, poly(W, H, [(dx - 6, dy - 16), (dx + 6, dy - 18), (dx + 3, dy - 24), (dx - 4, dy - 23)]), YEL, seed=nx(), rough=0.4)
    sx, sy = 100, 136
    steer = shapes(W, H, [[(sx - 5, sy + 24), (sx - 4, sy), (sx + 4, sy), (sx + 6, sy + 24)]], smooth=True)
    art = body(art, np.maximum(steer, circles(W, H, [(sx, sy - 7, 5.2)])), "#3a2419", seed=nx(), shade=0.2)
    art = GP(art, poly(W, H, [(sx - 6, sy - 10), (sx + 6, sy - 12), (sx + 3, sy - 17), (sx - 4, sy - 16)]), YEL, seed=nx(), rough=0.4)
    clear()
    # waterline wake + paddle splashes (white gouache, dry)
    wake = strokes(W, H, [(curve([(x0 + 40, 206), (300, 212), (560, 210), (x1 - 10, 200), (x1 + 40, 194)], 50), 3.4, (0.1, 0.3)),
                          (curve([(x0 - 30, 214), (x0 + 60, 218), (220, 222)], 30), 2.6, (0.2, 0.5)),
                          (curve([(x1 - 40, 206), (x1 + 20, 210), (x1 + 66, 206)], 20), 2.4, (0.2, 0.5))] + splashes)
    art = GP(art, wake, "#f4f1e6", seed=nx(), rough=1.2, density=0.9)
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "pj-jalur", tone=CREAM)
    save(art, f"{OUT}/jalur.webp", max_w=780, quality=82)
    clear()


def part_river():
    W, H = 780, 430
    nx = Seq(400); rng = random.Random(21)
    art = blank(W, H)
    bank_y = 150
    # far bank trees: overlapping watercolour crowns
    crowns = []
    for k in range(26):
        x = k * 31 + rng.uniform(-8, 8)
        r = rng.uniform(22, 44)
        crowns.append((x, bank_y - r * 0.5 + rng.uniform(-10, 6), r))
    tm = np.maximum(circles(W, H, crowns), rect(W, H, -10, bank_y - 20, W + 10, bank_y + 16))
    art = G(art, tm, "#6f8b55", "#4f6e44", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=6)
    art = G(art, tm * ygrad(W, H, bank_y - 60, bank_y + 10), "#2f4a33", seed=nx(), density=0.55, edge=0.2, rough=4)
    # a few tall coconut palms
    for px, ph in ((90, 120), (640, 140), (700, 110)):
        trunk = strokes(W, H, [(curve([(px, bank_y), (px + 6, bank_y - ph * 0.5), (px + 14, bank_y - ph)], 20), 4, (0.0, 0.2))])
        art = G(art, trunk, "#5b4632", seed=nx(), density=0.8, edge=0.3, rough=1.5)
        fr = strokes(W, H, [(curve([(px + 14, bank_y - ph), (px + 14 + math.cos(a) * 26, bank_y - ph + math.sin(a) * 10 - 6), (px + 14 + math.cos(a) * 44, bank_y - ph + 14 + math.sin(a) * 12)], 16), 6, (0.1, 0.6)) for a in np.linspace(math.pi * 0.9, math.pi * 2.1, 6)])
        art = G(art, fr, "#3f6a3a", seed=nx(), density=0.85, edge=0.4, rough=2)
    clear()
    # rumah panggung (stilted houses) + crowd on the tepian
    for hx, hw in ((210, 70), (300, 56), (520, 80)):
        roof = poly(W, H, [(hx - 8, bank_y - 22), (hx + hw / 2, bank_y - 52), (hx + hw + 8, bank_y - 22)])
        wall = rect(W, H, hx, bank_y - 22, hx + hw, bank_y - 2)
        legs = strokes(W, H, [([(hx + 4 + i * (hw - 8) / 3, bank_y - 2), (hx + 4 + i * (hw - 8) / 3, bank_y + 10)], 2.4, (0, 0)) for i in range(4)])
        art = body(art, np.maximum(wall, legs), "#9a6a40", seed=nx(), shade=0.3, dark=TEAK_D, rough=1)
        art = body(art, roof, "#7a3a26", seed=nx(), shade=0.3, dark=TEAK_D, rough=1)
        art = GP(art, rect(W, H, hx + hw * 0.4, bank_y - 18, hx + hw * 0.6, bank_y - 6), TEAK_D, seed=nx(), rough=0.5)
    crowd = []
    cols = [RED, YEL, "#f2efe6", GRN, "#3d6fb0", "#d8774a"]
    for k in range(80):
        x = rng.uniform(0, W)
        y = bank_y + 12 + rng.uniform(-3, 4)
        crowd.append((x, y, rng.choice(cols)))
    for col in cols:
        pts = [(x, y, 3.4) for x, y, c in crowd if c == col]
        if pts:
            art = GP(art, circles(W, H, pts), col, seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, [(x, y - 5, 2.2) for x, y, c in crowd]), "#3a2419", seed=nx(), rough=0.4)
    clear()
    # river: opaque painted water from below the bank to the bottom
    wy = bank_y + 18
    sky = painted_sky(W, H - wy, [(0, "#8aa98a"), (0.25, WATER), (1, WATER_D)], seed=nx(), streak=1.0, grain=0.6)
    water = np.zeros((H, W, 4), np.float32)
    water[wy:] = sky
    edge = ygrad(W, H, wy - 2, wy + 3)
    water[..., 3] *= edge
    art = over(art, water)
    # bank reflection (dark green smear) and ripple strokes
    refl = rect(W, H, -10, wy, W + 10, wy + 40) * (1 - ygrad(W, H, wy, wy + 44))
    art = G(art, refl, "#3a5a3c", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=3, feather=3)
    rip = []
    for k in range(110):
        y = rng.uniform(wy + 30, H - 6)
        x = rng.uniform(-40, W)
        L = rng.uniform(30, 120) * (0.5 + (y - wy) / H)
        rip.append((curve([(x, y), (x + L * 0.5, y - 1.5), (x + L, y)], 16), rng.uniform(3, 6), (0.3, 0.3)))
    art = GP(art, strokes(W, H, rip), "#cfe0c6", seed=nx(), rough=1.0, density=0.55)
    dark = []
    for k in range(40):
        y = rng.uniform(wy + 40, H - 6)
        x = rng.uniform(-40, W)
        L = rng.uniform(40, 140)
        dark.append((curve([(x, y), (x + L * 0.5, y + 1.5), (x + L, y)], 16), rng.uniform(3.5, 6), (0.3, 0.3)))
    art = GP(art, strokes(W, H, dark), "#244a3e", seed=nx(), rough=1.0, density=0.6)
    art = add_grain(art, seed=7, amount=0.03)
    preview(art, "pj-river", tone=CREAM)
    save_full(art, f"{OUT}/river.webp", quality=78)
    clear()


def part_umbul():
    W, H = 200, 620
    nx = Seq(700)
    art = blank(W, H)
    # bamboo pole bending at the top
    pole = curve([(60, 610), (58, 400), (64, 160), (90, 50), (150, 14)], 60)
    art = body(art, strokes(W, H, [(pole, 7, (0.0, 0.25))]), "#b8925a", "#d2b27a", seed=nx(), shade=0.3, dark=TEAK_D, rough=0.8)
    nodes = [pole[i] for i in range(8, 50, 9)]
    art = line(art, [([(x - 5, y), (x + 5, y + 1)], 2, (0, 0)) for x, y in nodes], nx(), col="#7a5a32")
    # long banner hanging from the bent top: stripes, scalloped/forked tail
    left = curve([(92, 52), (96, 200), (88, 360), (98, 500)], 50)
    right = curve([(136, 30), (140, 190), (132, 350), (142, 520)], 50)
    tail = [(142, 520), (128, 560), (120, 524), (108, 572), (98, 500)]
    ban = poly(W, H, left + tail[1:] [::-1][::-1] + right[::-1], smooth=False)
    ban = poly(W, H, left + [(108, 572), (120, 524), (128, 560)] + right[::-1], smooth=False)
    stripes = [(RED, 0, 0.22), (YEL, 0.22, 0.4), (GRN, 0.4, 0.55), ("#f3ecdc", 0.55, 0.66), (RED, 0.66, 0.84), (YEL, 0.84, 1.1)]
    for col, a, b in stripes:
        y0, y1 = 30 + a * 540, 30 + b * 540
        m = ban * rect(W, H, 0, y0, W, y1)
        art = body(art, m, col, seed=nx(), shade=0.3, dark=TEAK_D, rough=1.0, light=(0.1, 0.5))
    # fold shading (wind ripples)
    folds = strokes(W, H, [(curve([(100 + k * 12, 60 + k * 30), (104 + k * 12, 300), (100 + k * 12, 540)], 30), 6, (0.1, 0.1)) for k in range(3)]) * ban
    art = G(art, folds, "#2a1a12", seed=nx(), density=0.22, edge=0.1, bloom=0.1, rough=2, feather=3)
    # small diamond motif on the white stripe, tassels at the tail tips
    y = 30 + 0.605 * 540
    art = GP(art, shapes(W, H, [[(x, y - 8), (x + 6, y), (x, y + 8), (x - 6, y)] for x in (106, 122)], smooth=False) * ban, RED, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(108, 576, 4), (128, 564, 4)]), YEL, seed=nx(), rough=0.5)
    art = line(art, [([(90, 52), (150, 18)], 2.4, (0, 0))], nx(), col=TEAK_D)
    art = add_grain(art, seed=8, amount=0.03)
    preview(art, "pj-umbul", tone=CREAM)
    save(art, f"{OUT}/umbul.webp", max_w=110, quality=84)
    clear()


def part_bunting():
    W, H = 820, 130
    nx = Seq(900); rng = random.Random(4)
    art = blank(W, H)
    cord = [(x, 12 + 26 * abs(math.sin(math.pi * x / W)) ** 1.2) for x in np.linspace(-6, W + 6, 60)]
    flags = {RED: [], YEL: [], GRN: [], "#f3ecdc": []}
    order = [RED, YEL, GRN, "#f3ecdc"]
    for k, x in enumerate(np.arange(18, W - 10, 44)):
        y = 12 + 26 * abs(math.sin(math.pi * x / W)) ** 1.2
        L = 54 + rng.uniform(-4, 6)
        flags[order[k % 4]].append([(x - 17, y), (x + 17, y + 0.5), (x + rng.uniform(-3, 3), y + L)])
    for col, fs in flags.items():
        if fs:
            art = body(art, shapes(W, H, fs, smooth=False), col, seed=nx(), shade=0.25, dark=TEAK_D, rough=1.4)
    art = line(art, [(cord, 2.4, (0, 0))], nx(), col="#6b4a2c")
    art = add_grain(art, seed=9, amount=0.03)
    preview(art, "pj-bunting", tone=CREAM)
    save(art, f"{OUT}/bunting.webp", max_w=780, quality=82)
    clear()


def part_mini():
    """Small jalur silhouette with rowers on a ripple: the section divider."""
    W, H = 420, 90
    nx = Seq(1100)
    art = blank(W, H)
    x0, x1, mid = 40, 360, 52
    top, bot = hull_pts(x0, x1, 0, mid, 11, 14, 22)
    hull = poly(W, H, top + bot[::-1], smooth=True)
    ro = []
    for x in np.linspace(90, 320, 10):
        y = mid - 1
        ro.append(([(x - 3, y), (x + 1, y - 10)], 5, (0, 0.3)))
        ro.append(([(x + 2, y - 8), (x - 10, y + 20)], 1.8, (0, 0)))
    heads = circles(W, H, [(x + 3, mid - 14, 3) for x in np.linspace(90, 320, 10)])
    art = body(art, np.maximum(strokes(W, H, ro), heads), "#3a2419", seed=nx(), shade=0.1, rough=0.6)
    art = body(art, hull, TEAK, seed=nx(), shade=0.3, dark=TEAK_D, rough=0.8)
    t2, b2 = hull_pts(x0 + 16, x1 - 16, 0, mid + 3, 4, 13, 20)
    art = GP(art, poly(W, H, t2 + b2[::-1], smooth=True) * hull, YEL, seed=nx(), rough=0.5)
    neck = curve([(x1 - 6, mid + 4), (x1 + 6, mid - 10), (x1 + 4, mid - 26), (x1 + 14, mid - 36)], 20)
    art = body(art, strokes(W, H, [(neck, 6, (0, 0.2)), (spiral_scroll(x1 + 18, mid - 34, 6, math.pi * 1.2, 1.0, n=16), 4, (0, 0.5))]), RED, seed=nx(), shade=0.2)
    st = curve([(x0 + 6, mid - 2), (x0 - 6, mid - 10), (x0 - 4, mid - 20)], 12)
    art = body(art, strokes(W, H, [(st, 5, (0, 0.4))]), RED, seed=nx(), shade=0.2)
    rip = strokes(W, H, [(curve([(10, 70), (110, 74), (210, 71), (310, 75), (410, 70)], 40), 2.4, (0.1, 0.1)),
                         (curve([(70, 80), (170, 83), (270, 80), (350, 83)], 30), 1.8, (0.2, 0.2))])
    art = G(art, rip, WATER, seed=nx(), density=0.85, edge=0.3, rough=1.2, feather=0.8)
    preview(art, "pj-mini", tone=CREAM)
    save(art, f"{OUT}/mini.webp", max_w=320, quality=84)
    clear()


def part_prow():
    W, H = 200, 240
    nx = Seq(1300)
    art = blank(W, H)
    m_neck, m_crest, neck, curl = prow_head(W, H, 80, 150, 1.5, 1)
    base = poly(W, H, [(20, 190), (130, 176), (110, 210), (30, 214)], smooth=True)
    art = body(art, base, TEAK, seed=nx(), shade=0.4, dark=TEAK_D)
    art = GP(art, poly(W, H, [(30, 196), (122, 184), (116, 194), (34, 204)], smooth=True), YEL, seed=nx(), rough=0.6)
    art = body(art, m_crest, RED, seed=nx(), shade=0.25)
    art = body(art, m_neck, YEL, "#d89c22", seed=nx(), shade=0.35, dark=RED_D, rough=1.0)
    art = line(art, [(neck[8:], 3, (0.1, 0.2)), (curl, 2.6, (0.0, 0.4))], nx(), col=RED_D)
    art = GP(art, circles(W, H, [(neck[24][0] + 4, neck[24][1], 4.5)]), GRN, seed=nx(), rough=0.4)
    preview(art, "pj-prow", tone=CREAM)
    save(art, f"{OUT}/prow.webp", max_w=120, quality=84)
    clear()


for p in PARTS:
    globals()[f"part_{p}"]()
kb_report(OUT)
