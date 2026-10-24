"""Kolintang — watercolour + gouache: the Tomohon highlands at dusk (Lokon and Empung volcanoes with a thin steam
plume, mist, forest ridges, terraced krisan flower gardens, a Woloan wooden stilt house) and a painted kolintang
melody instrument (graded wooden bars on a carved box, two wrapped mallets). Extra pieces: krisan sprig, a three-bar
divider, a wood texture strip.
Run: python3 -I kolintang.py [part ...]   parts: scene kolintang krisan bilah kayu
Assets -> public/themes/art/kolintang/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t4_lib import *  # noqa

OUT = outdir("kolintang")
PARTS = sys.argv[1:] or ["scene", "kolintang", "krisan", "bilah", "kayu"]
WOOD, WOOD_L, WOOD_D = "#b9783a", "#dca364", "#6a3a17"
BOX, BOX_D = "#7a4320", "#3e1f0c"
GREEN, GREEN_D = "#2f5a3c", "#173828"
CORAL, MARI, MAGENTA, CREAM = "#e5636f", "#eba23a", "#c2457a", "#f6ead2"


def ridge(W, base, amps, rng, step=8):
    ph = [rng.uniform(0, 6) for _ in amps]
    pts = []
    x = -20
    while x <= W + 20:
        y = base
        for k, (a, f) in enumerate(amps):
            y -= a * math.sin(x / W * math.tau * f + ph[k])
        pts.append((x, y))
        x += step
    return pts


def volcano(cx, by, half, h, top, rng, crater=0.0):
    """Cone outline with concave flanks and a flat/notched summit."""
    L, R = [], []
    for i in range(21):
        t = i / 20
        y = by - h * (1 - t) ** 0.0 * 0 - h * t
        w = top + (half - top) * (1 - t) ** 1.8
        L.append((cx - w + rng.gauss(0, 1.2), by - h * t))
        R.append((cx + w + rng.gauss(0, 1.2), by - h * t))
    summit = [(cx - top, by - h), (cx - top * 0.3, by - h + crater), (cx + top * 0.4, by - h + crater * 0.6), (cx + top, by - h - 2)]
    return L + summit + R[::-1]


def part_scene():
    W, H = 780, 1180
    rng = random.Random(7); nx = Seq(100)
    sky = painted_sky(W, H, [(0, "#16372f"), (0.22, "#2c5a50"), (0.42, "#8aa79a"), (0.52, "#e9c08e"), (0.6, "#f0cf9f"), (1, "#f0cf9f")], seed=3, streak=0.8)
    art = sky
    # soft cloud washes in the dusk sky
    cl = []
    for _ in range(7):
        x, y = rng.uniform(-60, W), rng.uniform(250, 520)
        for j in range(4):
            cl.append((x + j * rng.uniform(26, 40), y + rng.uniform(-6, 6), rng.uniform(40, 70), rng.uniform(7, 12), rng.uniform(-3, 3)))
    art = G(art, displace(ellipses(W, H, cl), nx(), 6, 16), "#f3d9b3", "#d9b9a0", seed=nx(), density=0.35, edge=0.2, bloom=0.4, rough=6, feather=4)
    clear()
    # Lokon (broad, flat-topped) and Empung (crater) with steam
    lok = volcano(250, 760, 330, 250, 46, rng, crater=8)
    emp = volcano(560, 760, 300, 205, 30, rng, crater=14)
    m_l = displace(poly(W, H, lok, smooth=True), nx(), 2, 18)
    m_e = displace(poly(W, H, emp, smooth=True), nx(), 2, 18)
    art = G(art, m_e, "#7d8f98", "#8c9aa0", seed=nx(), density=0.85, edge=0.55, bloom=0.3, rough=2, feather=1)
    art = G(art, m_l, "#66808a", "#728b90", seed=nx(), density=0.88, edge=0.6, bloom=0.35, rough=2, feather=1)
    # short irregular gullies near the summits, fading downwards
    gl = []
    for cx, top, h, half, by in ((250, 46, 250, 330, 760), (560, 30, 205, 300, 760)):
        for k in range(11):
            u = rng.uniform(-0.9, 0.9)
            x0 = cx + u * top; y0 = by - h + rng.uniform(6, 20)
            L = rng.uniform(40, 120)
            x1 = x0 + u * L * 0.9 + rng.gauss(0, 6); y1 = y0 + L
            gl.append((curve([(x0, y0), ((x0 + x1) / 2 + rng.gauss(0, 5), (y0 + y1) / 2), (x1, y1)], 12), rng.uniform(2, 4.5), (0.05, 0.8)))
    gm = strokes(W, H, gl) * np.maximum(m_l, m_e) * (1 - ygrad(W, H, 560, 700))
    art = G(art, gm, "#55707a", seed=nx(), density=0.35, edge=0.35, rough=2, feather=1.2)
    # forested lower flanks
    fl = np.maximum(m_l, m_e) * ygrad(W, H, 640, 740)
    art = G(art, fl, "#5d7f74", "#4f7466", seed=nx(), density=0.55, edge=0.1, bloom=0.5, rough=6, feather=4)
    # sunlit right flanks
    lit = np.maximum(m_l * xgrad(W, H, 230, 420), m_e * xgrad(W, H, 560, 760)) * (1 - ygrad(W, H, 560, 760))
    art = G(art, lit, "#e9b98a", seed=nx(), density=0.28, edge=0.05, bloom=0.4, rough=4, feather=3)
    steam = []
    for k in range(9):
        steam.append((562 + k * 7 + k * k * 0.9 + rng.gauss(0, 2), 546 - k * 20, 10 + k * 4.5, 7 + k * 2.2, -35))
    steam += [(562, 545, 16, 9, 0), (570, 528, 20, 11, -30), (582, 508, 22, 12, -35)]
    art = G(art, displace(ellipses(W, H, steam), nx(), 6, 12) * (1 - ygrad(W, H, 520, 330) * 0.0), "#f4e8d6", "#e2d2c0", seed=nx(), density=0.6, edge=0.3, bloom=0.5, rough=5, feather=3)
    clear()
    # mist band at the volcano feet
    wisps = []
    for _ in range(26):
        x, y = rng.uniform(-80, W + 40), rng.uniform(715, 790)
        wisps.append((x, y, rng.uniform(60, 130), rng.uniform(8, 16), rng.uniform(-2, 2)))
    mist = displace(ellipses(W, H, wisps), nx(), 10, 30)
    art = over(art, flat(gaussian_filter(mist, 6), "#e8e4d8", 0.8))
    # forest ridges
    r1 = ridge(W, 790, [(18, 1.3), (7, 4.1)], rng)
    m1 = displace(poly(W, H, [(-20, H)] + r1 + [(W + 20, H)], smooth=True), nx(), 2, 14)
    art = GP(art, m1, "#4a7458", "#3c6a4e", seed=nx(), rough=2, streak=0.8, density=0.95)
    art = G(art, m1, "#3f6a50", "#4a765a", seed=nx(), density=0.4, edge=0.5, bloom=0.3, rough=2, feather=1)
    dabs = []
    for _ in range(900):
        x = rng.uniform(-10, W + 10); y = rng.uniform(770, 900)
        dabs.append((x, y, rng.uniform(2.5, 6.5), rng.uniform(1.5, 3.5), rng.uniform(-30, 30)))
    art = G(art, ellipses(W, H, dabs) * m1, "#3b6448", "#2b5238", seed=nx(), density=0.55, edge=0.45, bloom=0.2, rough=1.5, feather=0.6, gran=0.3)
    # tall cempaka / tree-fern silhouettes along the ridge
    tr = []
    for _ in range(16):
        x = rng.uniform(0, W); yb = 800 + rng.uniform(0, 40)
        hgt = rng.uniform(30, 60)
        tr.append(deform(ellipse_pts(x, yb - hgt * 0.6, hgt * 0.22, hgt * 0.5, 9), rng, 2, 0.12))
    art = G(art, shapes(W, H, tr), "#2e5a40", "#3b6a4a", seed=nx(), density=0.75, edge=0.55, bloom=0.2, rough=1.5, feather=0.6)
    clear()
    # flower-garden hill with terraced krisan beds
    r2 = ridge(W, 880, [(26, 0.7), (8, 2.6)], rng)
    m2 = displace(poly(W, H, [(-20, H)] + r2 + [(W + 20, H)], smooth=True), nx(), 2, 14)
    art = G(art, m2, "#6f9a5a", "#4f7d47", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=2, feather=1)
    cols = [CORAL, MARI, "#f2e2c4", MAGENTA, "#f08a3e", "#e9d25c"]
    rows = []
    for i in range(9):
        y0 = 905 + i * 30 + i * i * 1.6
        rows.append((y0, cols[(i * 2 + 1) % len(cols)], cols[(i * 2 + 2) % len(cols)]))
    for i, (y0, ca, cb) in enumerate(rows):
        bed = []
        amp = 10 + i * 1.5
        ph = rng.uniform(0, 3)
        pts = [(x, y0 + amp * math.sin(x / 210 + ph) - (r2[0][1] - 880) * 0) for x in range(-20, W + 21, 10)]
        thick = 10 + i * 3.0
        for x, y in pts:
            for _ in range(4 + i // 2):
                bed.append((x + rng.uniform(-7, 7), y + rng.uniform(-thick * 0.5, thick * 0.5), rng.uniform(2.2 + i * 0.3, 3.8 + i * 0.7)))
        bm = circles(W, H, bed) * m2
        art = GP(art, bm, ca, cb, seed=nx(), rough=1.0, streak=0.8, density=0.9)
        # dark green row line below the bed
        line = strokes(W, H, [([(x, y + thick * 0.7) for x, y in pts], 2 + i * 0.4, None)]) * m2
        art = G(art, line, "#35603c", seed=nx(), density=0.6, edge=0.2, rough=1, feather=0.6)
        if i % 3 == 2:
            clear()
    # a Woloan wooden stilt house on the right
    hx, hy = 612, 896
    roof = poly(W, H, [(hx - 62, hy - 40), (hx, hy - 82), (hx + 62, hy - 40)])
    body = rect(W, H, hx - 48, hy - 40, hx + 48, hy)
    stil = strokes(W, H, [([(hx + dx, hy), (hx + dx, hy + 22)], 3.2, None) for dx in (-42, -14, 14, 42)])
    art = GP(art, body, "#9a5a2c", "#7a4320", seed=nx(), rough=1.2)
    art = GP(art, stil, "#5a3216", seed=nx(), rough=0.6)
    art = GP(art, roof, "#8d2f2a", "#6c2420", seed=nx(), rough=1.2)
    win = shapes(W, H, [[(hx + dx - 7, hy - 30), (hx + dx + 7, hy - 30), (hx + dx + 7, hy - 14), (hx + dx - 7, hy - 14)] for dx in (-24, 0, 24)], smooth=False)
    art = GP(art, win, "#f2cf86", seed=nx(), rough=0.5)
    rail = strokes(W, H, [([(hx - 50, hy - 4), (hx + 50, hy - 4)], 2, None)])
    art = GP(art, rail, "#f1e2c4", seed=nx(), rough=0.4)
    clear()
    # bottom fades into the deep cover green (the kolintang stands on it)
    base = ygrad(W, H, 1000, 1170)
    art = over(art, flat(base, GREEN_D))
    art = add_grain(art, 5, 0.03)
    prev(art, "kolintang-scene")
    save_rgb(art, f"{OUT}/scene.webp", quality=74)


def bars_geom(x0, x1, ytop, ybot, n, rng):
    """Bars across the box top, long at the left (bass) to short at the right."""
    out = []
    span = x1 - x0
    bw = span / n * 0.8
    for i in range(n):
        t = i / (n - 1)
        cx = x0 + span * (i + 0.5) / n
        L = (ybot - ytop) * (1.0 - 0.42 * t)
        mid = (ytop + ybot) / 2 + (ybot - ytop) * 0.05 * t
        out.append((cx, mid - L / 2, mid + L / 2, bw * (1 - 0.15 * t)))
    return out


def part_kolintang():
    W, H = 780, 400
    rng = random.Random(11); nx = Seq(300)
    art = blank(W, H)
    # box: top face (trapezoid in slight perspective) + front face + legs
    top = [(60, 128), (720, 176), (720, 240), (60, 238)]
    endb = [(40, 140), (60, 128), (60, 330), (42, 316)]
    front = [(60, 236), (720, 238), (712, 300), (66, 318)]
    legs = strokes(W, H, [([(96, 312), (92, 380)], 16, None), ([(682, 298), (684, 372)], 14, None), ([(390, 308), (388, 364)], 12, None)])
    sh = soft_shadow(poly(W, H, [(60, 340), (720, 330), (740, 392), (40, 396)], smooth=True), "#0b1c12", blur=12, strength=0.55, dx=0, dy=0)
    art = over(art, sh)
    art = W_(art, legs, "#5a3216", BOX_D, seed=nx(), angle=1.57)
    m_front = poly(W, H, front)
    art = W_(art, m_front, BOX, BOX_D, seed=nx(), angle=0)
    # carved band on the front: simple lozenge + scroll border (Minahasa-style wood carving, inspired)
    band = poly(W, H, [(78, 252), (704, 254), (700, 288), (82, 302)])
    art = G(art, band, "#4a2410", seed=nx(), density=0.5, edge=0.4, rough=1, feather=0.6)
    loz = []
    for i in range(13):
        cx = 104 + i * 48.5; cy = 276 - i * 0.8
        loz.append([(cx - 14, cy), (cx, cy - 11), (cx + 14, cy), (cx, cy + 11)])
    art = FO(art, shapes(W, H, loz, smooth=False) - shapes(W, H, [[(x - 7 if k % 2 == 0 else x, y) for k, (x, y) in enumerate([(p[0][0] + 7, p[0][1]), (p[1][0], p[1][1] + 5.5), (p[2][0] - 7, p[2][1]), (p[3][0], p[3][1] - 5.5)])] for p in loz], smooth=False), "#c9963f", seed=nx(), emboss=0.5, sparkle=0.08)
    art = W_(art, poly(W, H, endb), "#5a2e12", BOX_D, seed=nx(), angle=1.57)
    m_top = poly(W, H, top)
    art = W_(art, m_top, "#5e3215", BOX_D, seed=nx(), angle=0)
    # two felt/string rails the bars rest on
    rails = strokes(W, H, [([(70, 156), (712, 194)], 6, None), ([(70, 226), (712, 230)], 6, None)])
    art = GP(art, rails, "#a8323a", "#7c2229", seed=nx(), rough=0.6)
    clear()
    # bars
    bars = bars_geom(82, 708, 120, 252, 14, rng)
    for i, (cx, y0, y1, bw) in enumerate(bars):
        sk = (cx - 60) / 660 * 0.06
        pts = [(cx - bw / 2, y0 + 4), (cx - bw / 2 + 2, y0), (cx + bw / 2 - 2, y0 + sk * 30), (cx + bw / 2, y0 + 4 + sk * 30),
               (cx + bw / 2, y1 - 3), (cx + bw / 2 - 2, y1), (cx - bw / 2 + 2, y1), (cx - bw / 2, y1 - 3)]
        m = poly(W, H, pts)
        shade = soft_shadow(m, "#1a0d05", blur=3, strength=0.65, dx=4, dy=6)
        art = over(art, shade)
        thick = np.clip(np.roll(m, 5, 0) - m, 0, 1)
        art = GP(art, thick, "#5a3012", "#3e1f0c", seed=nx(), rough=0.4)
        light = mix(WOOD_L, WOOD, rng.uniform(0, 0.5))
        art = W_(art, m, light, WOOD_D, seed=nx(), angle=1.57, streak=1.0)
        # carved-out underside arc reads as a darker middle; bright top edge
        arc = m * ygrad(W, H, y0 + (y1 - y0) * 0.35, y0 + (y1 - y0) * 0.5) * (1 - ygrad(W, H, y0 + (y1 - y0) * 0.55, y0 + (y1 - y0) * 0.72))
        art = G(art, arc, WOOD_D, seed=nx(), density=0.22, edge=0.1, rough=1, feather=1.5)
        hi = m * (1 - xgrad(W, H, cx - bw / 2, cx - bw / 2 + 4))
        art = tint(art, hi, "#fff0d0", 0.55)
        # string holes / nails
        art = over(art, flat(circles(W, H, [(cx, y0 + 12, 2.6), (cx, y1 - 12, 2.6)]), "#3a1c0a", 0.9))
        if i % 4 == 3:
            clear()
    # mallets: wooden sticks with wrapped rubber heads
    for (x0, y0, x1, y1, s) in ((430, 330, 650, 196, 1), (470, 352, 712, 232, 2)):
        stick = strokes(W, H, [([(x0, y0), (x1, y1)], 9, None)])
        sh2 = soft_shadow(stick, "#0b1c12", blur=4, strength=0.5, dx=5, dy=8)
        art = over(art, sh2)
        art = GP(art, stick, "#d6a46a", "#a8743e", seed=nx(), rough=0.4)
        art = tint(art, strokes(W, H, [([(x0, y0 - 2), (x1, y1 - 2)], 2.5, None)]), "#fff0d0", 0.45)
        head = ellipses(W, H, [(x1, y1, 19, 15, math.degrees(math.atan2(y1 - y0, x1 - x0)))])
        art = GP(art, head, "#2c2420", "#4a3a30", seed=nx(), rough=0.8)
        wrap = strokes(W, H, [([(x1 - 14, y1 - 6), (x1 + 12, y1 + 8)], 2.4, None), ([(x1 - 12, y1 + 6), (x1 + 14, y1 - 8)], 2.4, None), ([(x1 - 17, y1), (x1 + 17, y1)], 2.4, None)])
        art = GP(art, wrap * head, "#c9963f", seed=nx(), rough=0.3)
        art = tint(art, circles(W, H, [(x1 - 5, y1 - 5, 4)]), "#ffffff", 0.25)
    art = add_grain(art, 9, 0.03)
    prev(art, "kolintang-kolintang", bg=GREEN_D)
    save(art, f"{OUT}/kolintang.webp", max_w=760, quality=82)


def mum(art, W, H, cx, cy, r, ca, cb, rng, nx):
    """Chrysanthemum (krisan): many narrow ray petals in two rings + tight centre."""
    items = []
    for ring, k in ((1.0, 34), (0.82, 28), (0.62, 22), (0.42, 16)):
        for i in range(k):
            a = i / k * math.tau + rng.uniform(-0.08, 0.08) + ring
            L = r * ring * rng.uniform(0.85, 1.05)
            items.append((curve([(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.1), (cx + math.cos(a + 0.05) * L * 0.6, cy + math.sin(a + 0.05) * L * 0.55), (cx + math.cos(a) * L, cy + math.sin(a) * L * 0.86)], 8), r * 0.13 * ring + 1.2, (0.1, 0.5)))
    m = strokes(W, H, items)
    art = G(art, m, ca, cb, seed=nx(), density=0.78, edge=0.65, bloom=0.2, rough=1.4, feather=0.7)
    inner = strokes(W, H, items[-14:])
    art = G(art, inner, cb, seed=nx(), density=0.4, edge=0.5, rough=1, feather=0.6)
    art = G(art, circles(W, H, [(cx, cy, r * 0.16)]), "#9a5a1a", "#e0a640", seed=nx(), density=0.85, edge=0.5, rough=1, feather=0.6)
    return art


def part_krisan():
    W, H = 420, 340
    rng = random.Random(21); nx = Seq(500)
    art = blank(W, H)
    lv = []
    for (x, y, L, a) in ((205, 290, 95, 3.5), (212, 300, 100, 5.9), (196, 250, 80, 3.9), (232, 240, 82, 5.6), (214, 200, 60, 3.6), (214, 215, 64, 5.8)):
        base = petal_pts(x, y, L, L * 0.36, a, n=22)
        lob = [(px + math.cos(a + 1.57) * 5 * math.sin(k * 1.9), py + math.sin(a + 1.57) * 5 * math.sin(k * 1.9)) for k, (px, py) in enumerate(base)]
        lv.append(deform(lob, rng, 1, 0.05))
    leaves = shapes(W, H, lv)
    stems = strokes(W, H, [(curve([(210, 330), (200, 260), (150, 170)], 12), 4, None), (curve([(212, 330), (230, 250), (280, 160)], 12), 4, None), (curve([(214, 330), (214, 260), (212, 120)], 12), 4, None)])
    art = G(art, stems, "#4f7d47", seed=nx(), density=0.85, edge=0.4, rough=1, feather=0.6)
    art = G(art, leaves, "#5d8a4c", "#2f5a3c", seed=nx(), density=0.85, edge=0.65, bloom=0.35, rough=2.5)
    veins = [(curve([petal[0], petal[len(petal) // 2]], 6), 1.2, (0.1, 0.4)) for petal in lv]
    art = G(art, strokes(W, H, veins), "#2f5a3c", seed=nx(), density=0.5, edge=0.2, rough=0.6, feather=0.5)
    art = mum(art, W, H, 150, 168, 64, CORAL, "#c43d55", rng, nx)
    art = mum(art, W, H, 282, 160, 58, MARI, "#d0731f", rng, nx)
    clear()
    art = mum(art, W, H, 214, 104, 52, "#f4dfc2", "#d9a98c", rng, nx)
    art = mum(art, W, H, 340, 238, 34, MAGENTA, "#8e2a5a", rng, nx)
    art = mum(art, W, H, 82, 250, 30, MARI, "#c66a1e", rng, nx)
    prev(art, "kolintang-krisan")
    save(art, f"{OUT}/krisan.webp", max_w=360, quality=82)


def part_bilah():
    W, H = 460, 110
    rng = random.Random(31); nx = Seq(700)
    art = blank(W, H)
    rail = strokes(W, H, [([(40, 38), (420, 38)], 3, None), ([(40, 74), (420, 74)], 3, None)])
    art = GP(art, rail, "#a8323a", seed=nx(), rough=0.4)
    xs = [(70, 90), (130, 84), (190, 78), (250, 70), (310, 62), (370, 56)]
    for i, (cx, L) in enumerate(xs):
        m = poly(W, H, [(cx - 18, 56 - L / 2), (cx + 18, 56 - L / 2 + 1), (cx + 18, 56 + L / 2), (cx - 18, 56 + L / 2 - 1)])
        art = over(art, soft_shadow(m, "#2a1608", blur=2, strength=0.4, dx=2, dy=3))
        art = W_(art, m, mix(WOOD_L, WOOD, i / 8), WOOD_D, seed=nx(), angle=1.57)
        art = over(art, flat(circles(W, H, [(cx, 56 - L / 2 + 9, 2), (cx, 56 + L / 2 - 9, 2)]), "#3a1c0a"))
    art = mum(art, W, H, 432, 56, 22, CORAL, "#c43d55", rng, nx)
    art = mum(art, W, H, 26, 58, 17, MARI, "#d0731f", rng, nx)
    prev(art, "kolintang-bilah")
    save(art, f"{OUT}/bilah.webp", max_w=360, quality=82)


def part_kayu():
    W, H = 480, 160
    m = np.ones((H, W), np.float32)
    art = wood(m, "#c88b4c", WOOD_D, seed=41, angle=0, streak=1.0)
    art[..., 3] = 1
    prev(art, "kolintang-kayu")
    save_rgb(art, f"{OUT}/kayu.webp", quality=70)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
kb(OUT)
