"""Danau Maninjau — watercolour on cold-press paper: Lake Maninjau seen from the Kelok 44 hairpins. Pale morning sky,
the far crater rim in layered blue-green washes with mist at its foot, the deep ultramarine lake with keramba rafts,
a lakeshore of sawah terraces, coconut palms and a rumah gadang with gonjong roofs by the water; in the foreground the
steep green slope with the switchback road. Extra pieces: a rumah gadang vignette, padi sprig, hairpin-road divider,
mist band (drifts).
Run: python3 -I danau-maninjau.py [part ...]   parts: scene house padi road mist
Assets -> public/themes/art/danau-maninjau/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s4_lib import *  # noqa

OUT = outdir("danau-maninjau")
PARTS = sys.argv[1:] or ["scene", "house", "padi", "road", "mist"]
PAPER = "#f6f1e6"
LAKE, LAKE_D, LAKE_L = "#2a5f8f", "#173f6a", "#6f9dbf"
RIM, RIM_D = "#7f9ea0", "#5b7f80"
GREEN, GREEN_D, GREEN_L = "#4f8a4a", "#2f5f36", "#a6c46a"
ROOF, ROOF_D = "#3b3430", "#221c1a"
WALL, WALL_D = "#9a5232", "#6e3520"


def on_paper_rgb(art, tone=PAPER, seed=3):
    h, w = art.shape[:2]
    bg = np.asarray(paper(w, h, tone, seed, fiber=0.6, mottle=0.4), np.float32) / 255
    a = art[..., 3:4]
    return bg * (1 - a) + (bg * art[..., :3]) ** 0.9 * a


def ridge(W, base, amps, rng, step=10):
    ph = [rng.uniform(0, 6) for _ in amps]
    pts = []
    x = -20
    while x <= W + 20:
        y = base
        for k, (a, f) in enumerate(amps):
            y -= a * math.sin(x / W * math.tau * f + ph[k])
        pts.append((x, y + rng.uniform(-1.2, 1.2)))
        x += step
    return pts


def gonjong_house(W, H, x0, x1, ridge_y, eave_y, floor_y, peaks=4, seed=1):
    """Rumah gadang masks: roof (ijuk roof whose ridge sweeps up into slim gonjong spires, ship-like eave lifted at both
    ends), body (walls flaring outward to the top, bottom edge lifted at the ends), windows, stilts, ridge edge,
    carved wall bands, finials."""
    r = random.Random(seed)
    span = x1 - x0
    d = eave_y - ridge_y
    lift = d * 0.42
    px = [x0 - span * 0.05 + (span * 1.1) * i / (peaks - 1) for i in range(peaks)]
    py = [ridge_y + (0 if i in (0, peaks - 1) else d * 0.1) + r.uniform(-1.5, 1.5) for i in range(peaks)]
    top = []
    for i in range(peaks - 1):
        xa, ya, xb, yb = px[i], py[i], px[i + 1], py[i + 1]
        sag = d * 0.58
        for k in range(1, 30):
            t = k / 30
            top.append((xa + (xb - xa) * t, ya + (yb - ya) * t + sag * (1 - (2 * t - 1) ** 2) ** 0.38))
    eave = []
    for k in range(41):
        t = k / 40
        eave.append((x0 - span * 0.05 + span * 1.1 * t, eave_y - lift * abs(2 * t - 1) ** 2.4))
    outerL = [(eave[0][0] - span * 0.015, eave[0][1] - 2), (px[0] - span * 0.01, (py[0] + eave[0][1]) / 2)]
    outerR = [((px[-1] + span * 0.01), (py[-1] + eave[-1][1]) / 2), (eave[-1][0] + span * 0.015, eave[-1][1] - 2)]
    roof = poly(W, H, outerL + [(px[0], py[0])] + top + [(px[-1], py[-1])] + outerR + eave[::-1])
    horns = []
    for i, (x, y) in enumerate(zip(px, py)):
        lean = (-1 if i == 0 else 1 if i == peaks - 1 else 0) * span * 0.03
        horns.append((curve([(x - lean * 0.3, y + d * 0.42), (x, y + d * 0.12), (x + lean, y - d * 0.2)], 12), span * 0.04, (0.0, 0.95)))
    roof = np.maximum(roof, strokes(W, H, horns))
    py = [y - d * 0.2 for y in py]
    px = [x + (-1 if i == 0 else 1 if i == peaks - 1 else 0) * span * 0.03 for i, x in enumerate(px)]
    flo = []
    for k in range(41):
        t = k / 40
        flo.append((x0 + span * 0.04 + span * 0.92 * t, floor_y - lift * 0.45 * abs(2 * t - 1) ** 2.4))
    wall_top = [(x, y - 1) for x, y in eave if x0 - 2 <= x <= x1 + 2]
    body = poly(W, H, wall_top + flo[::-1])
    wins = []
    for i in range(7):
        wx = x0 + span * (0.12 + 0.76 * i / 6)
        t = (wx - x0) / span
        wy = eave_y - lift * abs(2 * t - 1) ** 2.4 + (floor_y - eave_y) * 0.2
        ww = span * 0.022; wh = (floor_y - eave_y) * 0.42
        wins.append([(wx - ww, wy), (wx + ww, wy), (wx + ww, wy + wh), (wx - ww, wy + wh)])
    windows = shapes(W, H, wins, smooth=False)
    st = []
    for i in range(10):
        t = 0.06 + 0.88 * i / 9
        sx = x0 + span * 0.04 + span * 0.92 * t
        sy = floor_y - lift * 0.45 * abs(2 * t - 1) ** 2.4
        st.append(([(sx, sy - 2), (sx, floor_y + (floor_y - eave_y) * 0.26)], max(1.4, span * 0.011), None))
    stilts = strokes(W, H, st)
    edge = strokes(W, H, [(top, max(1.0, span * 0.006), (0.02, 0.02))])
    bands = strokes(W, H, [([(x, y + (floor_y - eave_y) * f) for x, y in flo], max(1.0, span * 0.012), None) for f in (-0.08,)] +
                    [([(x, y + 3) for x, y in wall_top], max(1.0, span * 0.014), None)]) * body
    fin = strokes(W, H, [([(x, y), (x + (-1 if i == 0 else 1 if i == peaks - 1 else 0) * span * 0.008, y - d * 0.12)], max(1.0, span * 0.007), (0.0, 0.8)) for i, (x, y) in enumerate(zip(px, py))])
    return roof, body, windows, stilts, edge, bands, fin


def palm(art, W, H, x, by, h, rng, nx, lean=0.1, col="#3d6a3a", trunk="#6b5a44"):
    top = (x + h * lean, by - h)
    tr = strokes(W, H, [(curve([(x, by), (x + h * lean * 0.3, by - h * 0.5), top], 16), max(2, h * 0.04), (0.0, 0.3))])
    art = G(art, tr, trunk, seed=nx(), density=0.9, edge=0.5, rough=0.6, feather=0.5, pad=8)
    fr = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.12, 0.12)
        L = h * rng.uniform(0.38, 0.5)
        droop = abs(math.cos(a)) * L * 0.55
        end = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.6 + droop)
        mid = (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.5)
        fr.append((curve([top, mid, end], 12), max(2.5, h * 0.06), (0.05, 0.6)))
    art = G(art, strokes(W, H, fr), col, mix_hex(col, "#1e3b26", 0.4), seed=nx(), density=0.95, edge=0.6, rough=0.8, feather=0.6, pad=10)
    return art


def part_scene():
    W, H = 760, 1560
    rng = random.Random(44); nx = Seq(400)
    art = blank(W, H)
    # sky: cerulean at the top fading to warm paper above the rim
    sky = rect(W, H, 0, 0, W, 420) * (1 - ygrad(W, H, 30, 380))
    art = G(art, sky, "#9fc2dc", "#b7d0e2", seed=nx(), density=0.7, edge=0.08, bloom=0.5, rough=10, feather=6, mottle=0.7)
    warm = rect(W, H, 0, 220, W, 420) * ygrad(W, H, 220, 330) * (1 - ygrad(W, H, 330, 420))
    art = G(art, warm, "#f1cfa8", "#efd9b6", seed=nx(), density=0.4, edge=0.02, bloom=0.4, rough=12, feather=10)
    cl = []
    for _ in range(4):
        x, y = rng.uniform(-40, W), rng.uniform(140, 260)
        for j in range(5):
            cl.append((x + j * rng.uniform(16, 26), y + rng.uniform(-6, 4), rng.uniform(22, 40), rng.uniform(6, 10), 0))
    art = knockout(art, displace(ellipses(W, H, cl), nx(), 6, 14), amount=0.7, grow=3)
    clear()
    # far crater rim: a tall steep wall across the whole width, three layered washes
    far = ridge(W, 360, [(22, 1.2), (9, 3.4)], rng)
    m_far = displace(poly(W, H, [(-20, 700)] + far + [(W + 20, 700)], smooth=True), nx(), 2, 18)
    art = G(art, m_far, "#a7b8c2", "#9cb1ba", seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=2, feather=1.2)
    mid = ridge(W, 430, [(34, 0.9), (12, 2.7)], rng)
    m_mid = displace(poly(W, H, [(-20, 700)] + mid + [(W + 20, 700)], smooth=True), nx(), 2, 18)
    art = G(art, m_mid, "#7c9c98", "#6a8f8a", seed=nx(), density=0.8, edge=0.6, bloom=0.35, rough=2, feather=1)
    near = ridge(W, 520, [(40, 0.7), (14, 2.2)], rng)
    m_near = displace(poly(W, H, [(-20, 700)] + near + [(W + 20, 700)], smooth=True), nx(), 2, 18)
    art = G(art, m_near, "#5f8a6a", "#4f7c5c", seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=2.5, feather=1)
    # ravines (dark down-strokes) and forest canopy dabs on the walls
    gl = []
    for _ in range(22):
        x = rng.uniform(-10, W + 10); y = rng.uniform(440, 600)
        gl.append((curve([(x, y), (x + rng.uniform(-6, 6), y + 26), (x + rng.uniform(-10, 10), y + rng.uniform(50, 100))], 10), rng.uniform(1.6, 4), (0.1, 0.6)))
    art = G(art, strokes(W, H, gl) * m_mid, "#3f6658", "#355a4c", seed=nx(), density=0.45, edge=0.3, rough=1, feather=0.8)
    dabs = []
    for _ in range(900):
        x = rng.uniform(-10, W + 10); y = rng.uniform(440, 690)
        r = 3 + (y - 440) * 0.025
        dabs.append((x, y, r * rng.uniform(0.9, 1.4), r * rng.uniform(0.6, 0.9), 0))
    dm = ellipses(W, H, dabs) * m_near
    art = G(art, dm * (fbm(W, H, nx(), 40, 3) > 0.45), "#86ae74", "#9cbf7c", seed=nx(), density=0.45, edge=0.5, bloom=0.2, rough=1.2, feather=0.6)
    art = G(art, dm * (fbm(W, H, nx(), 40, 3) > 0.6), "#2f5a44", seed=nx(), density=0.35, edge=0.4, rough=1.2, feather=0.6)
    clear()
    # far shoreline villages: a ribbon of tiny roofs and a white mosque dome, then mist at the foot of the wall
    shore_y = 700
    vil = []
    for _ in range(60):
        x = rng.uniform(10, W - 10); y = shore_y - rng.uniform(2, 12)
        vil.append([(x - 4, y), (x + 4, y), (x + 3, y - 4), (x - 3, y - 4)])
    art = G(art, shapes(W, H, vil, smooth=False), "#b4644a", "#8a4a3a", seed=nx(), density=0.75, edge=0.4, rough=0.4, feather=0.4, pad=6)
    art = G(art, circles(W, H, [(470, shore_y - 12, 5)]) + rect(W, H, 465, shore_y - 12, 475, shore_y - 2), "#f4efe6", seed=nx(), density=0.9, edge=0.3, rough=0.3, feather=0.3, pad=6)
    m = mist(W, H, [(shore_y - 22, 12, -40, W + 40, 0.5), (shore_y - 60, 8, 120, 620, 0.3)], nx, rng, col="#ffffff", col2="#eef2f4")
    art = over(art, m)
    clear()
    # the lake: full width, deep ultramarine, darkest under the wall
    lake = displace(rect(W, H, -20, shore_y, W + 20, 1100), nx(), 1.5, 30)
    art = G(art, lake, LAKE, "#2f6a98", seed=nx(), density=0.9, edge=0.3, bloom=0.25, rough=2, feather=1, mottle=0.4)
    art = G(art, lake * (1 - ygrad(W, H, shore_y, shore_y + 130)), LAKE_D, "#1d4a72", seed=nx(), density=0.55, edge=0.05, bloom=0.2, rough=4, feather=6)
    idx = np.clip((shore_y - (np.arange(H) - shore_y) * 1.6).astype(int), 0, H - 1)
    refl = m_near[idx] * lake * (np.arange(H)[:, None] > shore_y + 4) * (1 - ygrad(W, H, shore_y, shore_y + 160))
    art = G(art, refl * 0.7, "#2f5a5a", seed=nx(), density=0.5, edge=0.1, rough=2, feather=2)
    streaks = []
    for _ in range(140):
        y = rng.uniform(shore_y + 30, 1060); x = rng.uniform(-20, W)
        streaks.append(([(x, y), (x + rng.uniform(30, 120) * (0.6 + (y - shore_y) / 400), y + rng.uniform(-0.5, 0.5))], rng.uniform(1, 2.6), (0.3, 0.3)))
    art = knockout(art, strokes(W, H, streaks) * lake, amount=0.5, grow=0.6)
    rafts = []
    for cx, cy, s in [(150, 820, 1.0), (200, 832, 1.0), (300, 790, 1.1), (350, 802, 1.1), (330, 960, 1.5), (390, 976, 1.5)]:
        for i in range(3):
            for j in range(2):
                x = cx + i * 9 * s; y = cy + j * 4 * s
                rafts.append([(x, y), (x + 7 * s, y), (x + 8 * s, y + 3 * s), (x + s, y + 3 * s)])
    art = G(art, shapes(W, H, rafts, smooth=False), "#7a6a52", seed=nx(), density=0.85, edge=0.4, rough=0.6, feather=0.4, pad=6)
    # a jukung with a fisherman's wake
    art = G(art, poly(W, H, [(250, 900), (300, 900), (292, 906), (258, 906)], smooth=True), "#5a3a2a", seed=nx(), density=0.9, edge=0.4, rough=0.4, feather=0.4, pad=6)
    art = knockout(art, strokes(W, H, [([(300, 904), (360, 910)], 1.6, (0.0, 0.8)), ([(300, 906), (350, 916)], 1.2, (0.0, 0.8))]), amount=0.6, grow=0.6)
    clear()
    # near shore across the width: sawah terraces as contour bands, palms, the rumah gadang by the water (right)
    shore = [(-20, 1000), (200, 985), (420, 978), (600, 972), (W + 20, 968), (W + 20, 1200), (-20, 1200)]
    land = displace(poly(W, H, shore, smooth=True), nx(), 2, 16)
    art = knockout(art, land, amount=1.0, grow=0.5)
    art = G(art, land, "#b9c66a", "#9fbb5c", seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=2, feather=1)
    bands = []
    for r in range(10):
        y0 = 990 + r * (8 + r * 1.2)
        pts = [(x, y0 + 6 * math.sin(x / 60 + r * 0.8)) for x in range(-20, W + 30, 12)]
        bands.append((pts, 1.2 + r * 0.12, None))
    art = G(art, strokes(W, H, bands) * land * (1 - ygrad(W, H, 1050, 1075)), "#6f8a3a", seed=nx(), density=0.6, edge=0.2, rough=0.5, feather=0.5)
    pat = fbm(W, H, nx(), 50, 2)
    art = G(art, land * (pat > 0.56), "#e3cf68", seed=nx(), density=0.5, edge=0.4, rough=2, feather=1)
    art = G(art, land * (pat < 0.36), "#5e9e50", seed=nx(), density=0.45, edge=0.4, rough=2, feather=1)
    # reflections of sawah light in flooded plots
    fl = []
    for _ in range(40):
        x = rng.uniform(0, W); y = rng.uniform(995, 1080)
        fl.append(([(x, y), (x + rng.uniform(14, 34), y)], 2.2, (0.2, 0.2)))
    art = G(art, strokes(W, H, fl) * land, "#a9c7d6", seed=nx(), density=0.6, edge=0.3, rough=0.5, feather=0.5)
    clear()
    roof, body, wins, stilts, edge, bands_h, fin = gonjong_house(W, H, 495, 675, 884, 946, 984, peaks=4, seed=3)
    art = G(art, stilts, "#4a3326", seed=nx(), density=0.95, edge=0.5, rough=0.5, feather=0.4, pad=8)
    art = G(art, body, WALL, "#a85e38", seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=0.8, feather=0.5, pad=8)
    art = G(art, bands_h, "#d2a548", seed=nx(), density=0.85, edge=0.4, rough=0.4, feather=0.4, pad=6)
    art = G(art, wins, "#3a2016", seed=nx(), density=0.85, edge=0.4, rough=0.4, feather=0.4, pad=6)
    art = G(art, roof, ROOF, "#4a403a", seed=nx(), density=0.95, edge=0.7, bloom=0.15, rough=0.8, feather=0.5, pad=8)
    art = G(art, roof * (1 - ygrad(W, H, 870, 930)), "#9a9ca4", seed=nx(), density=0.3, edge=0.3, rough=0.6, feather=0.6, pad=8)
    ijs = []
    for _ in range(160):
        x = rng.uniform(470, 700); y = rng.uniform(900, 946)
        ijs.append(([(x, y), (x + rng.uniform(-1.5, 1.5), y + rng.uniform(5, 10))], 0.9, (0.1, 0.6)))
    art = G(art, strokes(W, H, ijs) * roof, "#7c7a80", seed=nx(), density=0.45, edge=0.2, rough=0.3, feather=0.3, pad=6)
    art = G(art, edge + fin, "#c9a24e", seed=nx(), density=0.7, edge=0.2, rough=0.4, feather=0.4, pad=6)
    hm = np.maximum(np.maximum(roof, body), stilts)
    idx = np.clip((1960 - np.arange(H) - 0).astype(int), 0, H - 1)
    for x, by, h, ln in [(452, 996, 100, -0.12), (426, 994, 70, 0.1), (722, 990, 116, -0.08), (744, 998, 80, 0.14), (60, 1004, 90, 0.08), (300, 990, 60, -0.06)]:
        art = palm(art, W, H, x, by, h, rng, nx, lean=ln)
    clear()
    # foreground: forested slope we stand on, Kelok 44 switchbacks winding down (perspective: wider when nearer)
    fg_top = [(-20, 1060), (160, 1070), (360, 1086), (560, 1080), (W + 20, 1090)]
    fg = displace(poly(W, H, fg_top + [(W + 20, H + 20), (-20, H + 20)], smooth=True), nx(), 3, 20)
    art = G(art, fg, "#3f7444", "#35663c", seed=nx(), density=0.92, edge=0.6, bloom=0.35, rough=3, feather=1.2)
    art = G(art, fg * ygrad(W, H, 1150, 1560), GREEN_D, "#24452c", seed=nx(), density=0.6, edge=0.1, bloom=0.3, rough=4, feather=6)
    turns = [(520, 1078), (250, 1104), (560, 1140), (150, 1190), (640, 1256), (70, 1340), (700, 1440), (-40, 1560)]
    pts = []
    for i in range(len(turns) - 1):
        (x0, y0), (x1, y1) = turns[i], turns[i + 1]
        pts += [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + (5 if i % 2 else -5))]
    pts.append(turns[-1])
    road = curve(pts, 360)
    rw = [(road[i:i + 2], 3 + max(0, road[i][1] - 1070) * 0.05, None) for i in range(len(road) - 1)]
    rm = strokes(W, H, rw)
    # canopy between the bends: crowns grow with nearness, three glazes (shadow, body, sunlit top-left)
    crowns = []
    for _ in range(1300):
        x = rng.uniform(-20, W + 20); y = rng.uniform(1080, H + 20)
        r = (4 + (y - 1070) * 0.045) * rng.uniform(0.55, 1.35)
        crowns.append((x, y, r * rng.uniform(1.0, 1.5), r * rng.uniform(0.7, 1.0), rng.uniform(-20, 20)))
    free = 1 - np.clip(gaussian_filter(rm, 2.5) * 2.5, 0, 1)
    cm = ellipses(W, H, crowns) * fg * free
    art = G(art, cm, "#5c9150", "#4f8448", seed=nx(), density=0.75, edge=0.7, bloom=0.3, rough=2.4, feather=0.7)
    lit = ellipses(W, H, [(x - rx * rng.uniform(0.1, 0.4), y - ry * rng.uniform(0.2, 0.45), rx * rng.uniform(0.4, 0.75), ry * rng.uniform(0.35, 0.6), a + rng.uniform(-25, 25)) for x, y, rx, ry, a in crowns if rng.random() < 0.7]) * fg * free
    art = G(art, lit, "#a5cc6e", "#b9d77c", seed=nx(), density=0.55, edge=0.5, bloom=0.3, rough=1.8, feather=0.6)
    hi = ellipses(W, H, [(x - rx * rng.uniform(0.3, 0.55), y - ry * rng.uniform(0.35, 0.6), rx * rng.uniform(0.15, 0.3), ry * rng.uniform(0.12, 0.22), a) for x, y, rx, ry, a in crowns if rng.random() < 0.3]) * fg * free
    art = G(art, hi, "#b8d47e", seed=nx(), density=0.5, edge=0.4, rough=1.2, feather=0.5)
    clear()
    art = knockout(art, rm, amount=0.92, grow=0.6)
    art = G(art, rm, "#c9c0a8", "#b2a993", seed=nx(), density=0.8, edge=0.7, bloom=0.2, rough=0.8, feather=0.5)
    # shadowed inner edge + painted centre dashes
    inner = np.clip(rm - np.roll(rm, -3, 0), 0, 1)
    art = G(art, inner, "#6a6252", seed=nx(), density=0.5, edge=0.2, rough=0.4, feather=0.4)
    dash = [(road[i:i + 3], 0.8 + max(0, road[i][1] - 1070) * 0.006, None) for i in range(0, len(road) - 3, 8)]
    art = G(art, strokes(W, H, dash), "#f6efd8", seed=nx(), density=0.8, edge=0.2, rough=0.3, feather=0.3)
    # numbered hairpin posts (white with a red cap) at each bend
    posts = []
    for tx, ty in turns[1:-1]:
        s = 0.5 + (ty - 1070) * 0.006
        px = tx + (-14 if tx < 380 else 14) * s
        posts.append((px, ty - 10 * s, s))
    art = G(art, strokes(W, H, [([(x, y), (x, y - 12 * s)], 3.5 * s, None) for x, y, s in posts]), "#fbf7ee", seed=nx(), density=0.95, edge=0.3, rough=0.3, feather=0.3, pad=6)
    art = G(art, strokes(W, H, [([(x, y - 9 * s), (x, y - 12 * s)], 3.5 * s, None) for x, y, s in posts]), "#c0392b", seed=nx(), density=0.95, edge=0.3, rough=0.3, feather=0.3, pad=6)
    clear()
    rgb = on_paper_rgb(art)
    prev_rgb(rgb, "dm-scene")
    save_rgb(rgb, f"{OUT}/scene.webp", quality=74)
    clear()


def part_house():
    """Rumah gadang vignette (closing / people): watercolour on transparent, reflection fading in the lake."""
    W, H = 680, 420
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    water = rect(W, H, 20, 268, 660, 380) * (1 - np.abs(xgrad(W, H, 20, 660) - 0.5) * 1.7).clip(0, 1) * (1 - ygrad(W, H, 330, 410))
    art = G(art, displace(water, nx(), 4, 16), LAKE_L, LAKE, seed=nx(), density=0.65, edge=0.4, bloom=0.4, rough=4, feather=2)
    roof, body, wins, stilts, edge, bands, fin = gonjong_house(W, H, 200, 480, 40, 160, 236, peaks=4, seed=5)
    hm = np.maximum(np.maximum(roof, body), stilts)
    idx = np.clip((2 * 262 - np.arange(H)).astype(int), 0, H - 1)
    hr = hm[idx] * (np.arange(H)[:, None] > 268) * water
    art = G(art, gaussian_filter(hr, 1.5) * 0.7, "#2c3c52", seed=nx(), density=0.6, edge=0.1, rough=3, feather=1.5)
    art = G(art, stilts, "#4a3326", seed=nx(), density=0.95, edge=0.5, rough=0.6, feather=0.5)
    art = G(art, body, WALL, "#a85e38", seed=nx(), density=0.95, edge=0.7, bloom=0.3, rough=1, feather=0.6)
    # carved wall: diamond lattice (painted ukiran) between the gold bands
    lat = hatch(W, H, 0.7, 9, 0.22, seed=3) + hatch(W, H, -0.7, 9, 0.22, seed=4)
    art = G(art, np.clip(lat, 0, 1) * body * (1 - wins), "#3a1a10", seed=nx(), density=0.35, edge=0.1, rough=0.5, feather=0.5)
    art = G(art, bands, "#d8a845", seed=nx(), density=0.9, edge=0.4, rough=0.5, feather=0.4)
    art = G(art, wins, "#2a160e", seed=nx(), density=0.9, edge=0.5, rough=0.5, feather=0.4)
    art = G(art, roof, ROOF, "#4a403a", seed=nx(), density=0.95, edge=0.8, bloom=0.2, rough=1, feather=0.6)
    ij = []
    for _ in range(260):
        x = rng.uniform(170, 520); y = rng.uniform(50, 155)
        ij.append(([(x, y), (x + rng.uniform(-2, 2), y + rng.uniform(8, 18))], 1.1, (0.1, 0.6)))
    art = G(art, strokes(W, H, ij) * roof, "#8a8890", seed=nx(), density=0.4, edge=0.2, rough=0.4, feather=0.4)
    art = G(art, edge + fin, "#c9a24e", seed=nx(), density=0.8, edge=0.3, rough=0.5, feather=0.4)
    grass = rect(W, H, 90, 250, 600, 270)
    art = G(art, displace(grass, nx(), 4, 10), "#7fae62", "#5e9a50", seed=nx(), density=0.8, edge=0.5, rough=4, feather=1)
    for x, by, h, ln in [(120, 262, 170, -0.1), (560, 264, 150, 0.12), (596, 266, 104, -0.05)]:
        art = palm(art, W, H, x, by, h, rng, nx, lean=ln)
    prev_rgba(art, "dm-house", bg=PAPER)
    save_a(art, f"{OUT}/house.webp", max_w=560)
    clear()


def part_padi():
    """Padi sprig: arching rice stalk heavy with golden grains (nodes, amp, sent)."""
    W, H = 240, 300
    rng = random.Random(3); nx = Seq(1200)
    art = blank(W, H)
    stem = curve([(120, 292), (118, 200), (128, 120), (160, 70), (196, 60)], 50)
    leaves = [(curve([(119, 250), (90, 190), (40, 150)], 16), 9, (0.05, 0.7)), (curve([(120, 220), (150, 170), (190, 150)], 16), 8, (0.05, 0.7)),
              (curve([(119, 280), (80, 250), (50, 236)], 12), 7, (0.05, 0.7))]
    art = G(art, strokes(W, H, [(stem, 4, (0.0, 0.3))] + leaves), "#7ea64a", "#5f8a3a", seed=nx(), density=0.9, edge=0.6, rough=0.8, feather=0.5)
    grains = []
    for i, (x, y, a) in enumerate(resample(stem[18:], 10)):
        for side in (-1, 1):
            gx = x + math.cos(a + side * 1.2) * 9; gy = y + math.sin(a + side * 1.2) * 9 + 8
            grains.append((gx, gy, 6.5, 3.6, math.degrees(a) + side * 30 + 90))
    for x, y, a in resample(stem[18:], 10)[::2]:
        grains.append((x + 3, y + 14, 6, 3.4, math.degrees(a) + 90))
    gm = ellipses(W, H, grains)
    art = G(art, gm, "#e3b84a", "#c99a34", seed=nx(), density=0.95, edge=0.8, bloom=0.2, rough=0.6, feather=0.5)
    art = G(art, gm * (fbm(W, H, nx(), 8, 2) > 0.55), "#a8762a", seed=nx(), density=0.5, edge=0.3, rough=0.4, feather=0.4)
    prev_rgba(art, "dm-padi")
    save_a(art, f"{OUT}/padi.webp", max_w=160)
    clear()


def part_road():
    """Hairpin road divider: a ribbon of grey road switching back twice, yellow edge line, tiny posts."""
    W, H = 700, 140
    rng = random.Random(5); nx = Seq(1500)
    art = blank(W, H)
    def seg(p, q, n=30):
        return [(p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n) for k in range(n)]
    R = 19
    pts = seg((10, 112), (520, 104)) + arc_pts(520, 104 - R, R, math.pi / 2, -math.pi / 2, 24)[0:24]
    pts = pts + seg((520, 104 - 2 * R), (180, 64)) + arc_pts(180, 64 - R, R, math.pi / 2, 3 * math.pi / 2, 24)
    pts = pts + seg((180, 64 - 2 * R), (690, 20))
    pts = curve(pts[::3] + [pts[-1]], 400)
    road = strokes(W, H, [(pts, 14, (0.05, 0.05))])
    art = G(art, road, "#9a9384", "#8a8476", seed=nx(), density=0.85, edge=0.7, bloom=0.2, rough=1, feather=0.6)
    dash = [(pts[i:i + 4], 2, None) for i in range(0, len(pts) - 4, 12)]
    art = G(art, strokes(W, H, dash), "#f2e9d0", seed=nx(), density=0.9, edge=0.2, rough=0.4, feather=0.3)
    grass = []
    for x, y, a in resample(pts, 9):
        for side in (-1, 1):
            gx = x + math.cos(a + side * math.pi / 2) * 12; gy = y + math.sin(a + side * math.pi / 2) * 12
            grass.append(([(gx, gy), (gx + rng.uniform(-2, 2), gy - rng.uniform(5, 10))], 1.8, (0.0, 0.7)))
    art = G(art, strokes(W, H, grass), "#6fa04e", "#4f8a40", seed=nx(), density=0.7, edge=0.3, rough=0.5, feather=0.4)
    prev_rgba(art, "dm-road")
    save_a(art, f"{OUT}/road.webp", max_w=420)
    clear()


def part_mist():
    """Mist band (transparent white wash), drifts across the lake on the cover."""
    W, H = 900, 160
    rng = random.Random(12); nx = Seq(1700)
    art = mist(W, H, [(80, 22, -40, W + 40, 0.55), (100, 14, 80, W - 120, 0.4)], nx, rng, col="#ffffff", col2="#eef2f4")
    prev_rgba(art, "dm-mist", bg="#2a5f8f")
    save_a(art, f"{OUT}/mist.webp", max_w=900, quality=70)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
