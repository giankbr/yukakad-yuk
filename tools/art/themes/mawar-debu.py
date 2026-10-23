"""Mawar Debu — dried dusty-rose bundle tied with a mauve satin ribbon, single dried rose heads, a satin bow and a
long loose ribbon; soft watercolour on cotton paper. Run: python3 -I mawar-debu.py [part ...]
parts: paper bundle rose bow ribbon sprig  -> public/themes/art/mawar-debu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h5_lib import *

OUT = outdir("mawar-debu")
PARTS = sys.argv[1:] or ["paper", "bundle", "rose", "bow", "ribbon", "sprig"]
SEQ = Seq(900)
R_L, R_M, R_D = "#e2c2bf", "#b98a8f", "#6f4652"     # dried rose
R2_L, R2_M, R2_D = "#d9b7a6", "#a87a72", "#5e3d3a"  # tea-rose variant
LEAF_A, LEAF_B = "#8e8c69", "#5f5e46"
STEM = "#7a6a52"
SATIN, SATIN_D, SATIN_L = "#bf98a6", "#8a6378", "#f1dde2"


def ribbon(W, H, pts, w0, phase=0.0, freq=0.018, seed=1, col=SATIN, dark=SATIN_D, light=SATIN_L, dens=0.78):
    """Satin ribbon along a centreline: twists (width ~ |cos|), back side darker, sheen streak on the front.
    Each run of one side is a single continuous polygon so the edges stay clean."""
    pts = resample(pts, 2.5)
    n = len(pts)
    L = 0.0
    rows = []
    for i in range(n):
        x, y = pts[i]
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        dx, dy = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        d = math.hypot(dx, dy) or 1
        nx_, ny_ = -dy / d, dx / d
        if i:
            L += math.hypot(x - pts[i - 1][0], y - pts[i - 1][1])
        c = math.cos(phase + L * freq)
        wd = w0 * (0.1 + 0.9 * abs(c)) / 2
        rows.append((x, y, nx_, ny_, wd, c))
    runs = []
    cur = [rows[0]]
    for r in rows[1:]:
        if (r[5] >= 0) == (cur[-1][5] >= 0):
            cur.append(r)
        else:
            cur.append(r); runs.append(cur); cur = [r]
    runs.append(cur)
    front, back, sheen, shade = [], [], [], []
    for run in runs:
        if len(run) < 2:
            continue
        left = [(x + nx_ * w, y + ny_ * w) for x, y, nx_, ny_, w, c in run]
        right = [(x - nx_ * w, y - ny_ * w) for x, y, nx_, ny_, w, c in run]
        poly = left + right[::-1]
        if run[len(run) // 2][5] >= 0:
            front.append(poly)
            sl = [(x + nx_ * w * 0.15, y + ny_ * w * 0.15) for x, y, nx_, ny_, w, c in run if c > 0.5]
            if len(sl) > 3:
                sheen.append(sl)
            sh = [(x - nx_ * w * 0.7, y - ny_ * w * 0.7) for x, y, nx_, ny_, w, c in run]
            shade.append(sh)
        else:
            back.append(poly)
    lay = blank(W, H)
    if back:
        mb = shapes(W, H, back, smooth=False)
        lay = G(lay, mb, dark, mix(dark, col, .3), seed=SEQ(), density=dens + 0.12, edge=0.4, bloom=0.08, gran=0.1, rough=0.8, feather=0.7)
    if front:
        mf = shapes(W, H, front, smooth=False)
        lay = G(lay, mf, col, mix(col, light, .3), seed=SEQ(), density=dens, edge=0.45, bloom=0.12, gran=0.1, rough=0.8, feather=0.7)
        ms = strokes(W, H, [(p, w0 * 0.42, (0.3, 0.3)) for p in shade]) * mf
        lay = G(lay, gaussian_filter(ms, 2.0), dark, seed=SEQ(), density=0.22, edge=0.1, bloom=0, gran=0.05, rough=0.5, feather=1.5)
        if sheen:
            mh = gaussian_filter(strokes(W, H, [(p, w0 * 0.18, (0.35, 0.35)) for p in sheen]), 2.0) * mf
            lay = OV(lay, mh, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(light), np.float32), (np.clip(m, 0, 1) * 0.6)[..., None]], -1))
    return lay


def dried_leaf(W, H, x, y, L, a, rng, curl=0.25):
    pts = petal_pts(x, y, L, L * 0.3, a, n=14, cup=curl)
    m = shape_mask(W, H, deform(pts, rng, 2, 0.08))
    lay = pig(m, LEAF_A, LEAF_B, seed=SEQ(), density=0.62, edge=0.7, bloom=0.35, rough=3.5, holes=0.04)
    v = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0.05, 0.85, 8)]
    lay = glaze(lay, pig(stroke_mask(W, H, v, max(1.2, L * 0.03)), LEAF_B, seed=SEQ(), density=0.45, edge=0.2, bloom=0, rough=1, feather=.6))
    return lay


def dried_rose(W, H, cx, cy, r, rng, pal=0, tilt=0.86):
    L_, M_, D_ = (R_L, R_M, R_D) if pal == 0 else (R2_L, R2_M, R2_D)
    lay, base = rose(W, H, cx, cy, r, L_, M_, D_, SEQ, rng, petals=12, tilt=tilt)
    # dried look: darkened, crinkled petal tips
    rim = np.clip(base - gaussian_filter(base, r * 0.12), 0, 1) * 2.2
    lay = glaze(lay, pig(np.clip(rim, 0, 1), D_, seed=SEQ(), density=0.55, edge=0.8, bloom=0, rough=3.0, feather=0.8))
    return lay, base


def paper_tile():
    W = H = 512
    p = paper(W, H, "#f3e7e3", seed=41, fiber=0.7, mottle=0.45)
    arr = np.asarray(p, np.float32) / 255
    rgb = arr[..., :3]
    # faint rose-dust blooms, wrapped
    n = wrap_noise(W, H, 7, 38)
    rgb = rgb * (1 - 0.035 * (n[..., None] - 0.5)) - np.array([0, 0.012, 0.006]) * n[..., None]
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    im.save(f"{OUT}/paper.webp", "WEBP", quality=74, method=6)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")


def sepals(W, H, x, y, r, a, rng):
    """Dried, curling sepals under a rose head (a = direction of the stem from the head)."""
    items = []
    for k in range(5):
        aa = a + rng.uniform(-1.3, 1.3)
        L = r * rng.uniform(0.45, 0.7)
        p0 = (x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55)
        pts = curve([p0, (p0[0] + math.cos(aa) * L * .5, p0[1] + math.sin(aa) * L * .5), (p0[0] + math.cos(aa + 0.6) * L, p0[1] + math.sin(aa + 0.6) * L)], 12)
        items.append((pts, r * 0.09, (0.1, 0.6)))
    return pig(strokes(W, H, items), LEAF_B, "#56523d", seed=SEQ(), density=0.7, edge=0.5, bloom=0, rough=1.2, feather=0.6)


def gyp(W, H, x0, y0, x1, y1, rng, n=14):
    """Dried baby's breath: hairline branching stems ending in tiny cream florets."""
    items, dots = [], []
    main = curve([(x0, y0), ((x0 + x1) / 2 + rng.uniform(-20, 20), (y0 + y1) / 2), (x1, y1)], 20)
    items.append((main, 2.2, (0, .2)))
    for k in range(n):
        i = rng.randint(len(main) // 3, len(main) - 1)
        bx, by = main[i]
        a = math.atan2(y1 - y0, x1 - x0) + rng.uniform(-1.1, 1.1)
        L = rng.uniform(18, 46)
        ex, ey = bx + math.cos(a) * L, by + math.sin(a) * L
        items.append(([(bx, by), (ex, ey)], 1.3, (0, .3)))
        for j in range(rng.randint(2, 4)):
            dots.append((ex + rng.gauss(0, 5), ey + rng.gauss(0, 5), rng.uniform(3.2, 5.2)))
    lay = pig(strokes(W, H, items), "#8b7d62", seed=SEQ(), density=0.65, edge=0.3, bloom=0, rough=0.8, feather=0.5)
    cm = circles(W, H, dots)
    lay = over(lay, local(pigment, cm, "#fbf4ea", "#efe2d6", seed=SEQ(), density=0.95, edge=0.0, bloom=0, rough=1.0, feather=0.6))
    lay = glaze(lay, local(pigment, np.clip(cm - gaussian_filter(cm, 1.2), 0, 1) * 2, "#b49c96", seed=SEQ(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4))
    return lay


def bundle():
    W, H = 900, 1060
    rng = random.Random(11)
    art_ = blank(W, H)
    tie = (430, 650)
    # (x, y, r, palette, tilt, droop angle of head->stem)
    heads = [(560, 250, 96, 0, 0.84), (712, 372, 80, 1, 0.66), (402, 330, 84, 0, 0.78), (660, 168, 64, 1, 0.72),
             (282, 214, 62, 0, 0.62), (560, 446, 70, 1, 0.86), (205, 360, 54, 0, 0.6)]
    stems = []
    for hx, hy, r, _, _ in heads + [(800, 250, 0, 0, 0), (338, 112, 0, 0, 0), (470, 140, 0, 0, 0)]:
        foot = (tie[0] - (hx - tie[0]) * 0.5 + rng.uniform(-30, 30), H - 30 - rng.uniform(0, 80))
        mid = (tie[0] + rng.uniform(-10, 10), tie[1])
        pts = curve([foot, mid, ((mid[0] + hx) / 2 + rng.uniform(-18, 18), (mid[1] + hy) / 2 + rng.uniform(-10, 10)), (hx, hy + r * 0.45)], 48)
        stems.append(pts)
    items = [(p, rng.uniform(5.5, 8.5), (0.0, 0.08)) for p in stems]
    art_ = G(art_, strokes(W, H, items), STEM, "#5a4f3c", seed=SEQ(), density=0.8, edge=0.55, bloom=0.1, rough=1.4, feather=0.7)
    # thorns
    th = []
    for p in stems:
        for t in (0.55, 0.7, 0.86):
            i = int(len(p) * t); x, y = p[i]
            a = math.atan2(p[i + 1][1] - y, p[i + 1][0] - x)
            sgn = rng.choice([-1, 1])
            th.append([(x, y), (x + math.cos(a + sgn * 1.2) * 9, y + math.sin(a + sgn * 1.2) * 9)])
    art_ = G(art_, strokes(W, H, [(q, 3.4, (0, 0.9)) for q in th]), "#5a4f3c", seed=SEQ(), density=0.7, edge=0.3, rough=0.6, feather=.5)
    flush()
    # baby's breath behind
    for (a, b, c, d) in [(430, 600, 250, 120), (440, 600, 820, 150), (430, 610, 140, 290), (440, 600, 600, 70)]:
        art_ = glaze(art_, gyp(W, H, a, b, c, d, rng))
        flush()
    # dried leaves along stems
    for p in stems[:8]:
        for t in (0.5, 0.64, 0.8):
            i = int(len(p) * t)
            x, y = p[i]
            a = math.atan2(p[i + 1][1] - y, p[i + 1][0] - x) + rng.choice([-1, 1]) * rng.uniform(0.55, 1.15)
            art_ = glaze(art_, dried_leaf(W, H, x, y, rng.uniform(64, 104), a, rng, curl=rng.uniform(.15, .5)))
        flush()
    for bx, by, a in [(800, 250, -0.5), (338, 112, -1.9), (470, 140, -1.5)]:
        lay, _ = bud(W, H, bx, by, 23, a, R_M, R_D, LEAF_B, SEQ, rng)
        art_ = glaze(art_, lay)
    flush()
    for hx, hy, r, pal, tilt in sorted(heads, key=lambda t: t[1]):
        art_ = glaze(art_, sepals(W, H, hx, hy, r, math.pi / 2 + (hx - tie[0]) * -0.002, rng))
        lay, base = dried_rose(W, H, hx, hy, r, rng, pal, tilt=tilt)
        art_ = knockout(art_, base, 0.85, 3.0)
        art_ = glaze(art_, lay)
        flush()
    wrap = ribbon(W, H, [(tie[0] - 64, tie[1] - 22), (tie[0], tie[1] + 4), (tie[0] + 64, tie[1] - 12)], 34, phase=0.2, freq=0.004, seed=3)
    bl = over(wrap, bow_layer(W, H, tie[0] + 6, tie[1] - 6, 1.0, rng))
    art_ = knockout(art_, np.clip(bl[..., 3] * 1.6, 0, 1), 1.0, 0.8)
    art_ = over(art_, bl)
    flush()
    preview(art_, "md-bundle", "#f3e7e3")
    save(art_, f"{OUT}/bundle.webp", max_w=620, quality=80)


def bow_layer(W, H, cx, cy, s, rng, tails=True):
    lay = blank(W, H)
    # loops: left and right
    for side in (-1, 1):
        pts = [(cx, cy)] + [(cx + side * (60 + 90 * math.sin(t)) * s * (0.6 + 0.4 * math.sin(t)), cy - 70 * s * math.sin(2 * t) - 6 * s) for t in np.linspace(0.25, math.pi - 0.15, 18)] + [(cx, cy + 2)]
        lay = over(lay, ribbon(W, H, pts, 30 * s, phase=0.5 + side, freq=0.012 / s, seed=SEQ()))
    if tails:
        for side in (-1, 1):
            pts = curve([(cx, cy + 4), (cx + side * 40 * s, cy + 90 * s), (cx + side * 20 * s, cy + 180 * s), (cx + side * 70 * s, cy + 270 * s)], 30)
            lay = over(lay, ribbon(W, H, pts, 28 * s, phase=0.1 + side * 0.4, freq=0.011 / s, seed=SEQ()))
    knot = shape_mask(W, H, deform(ellipse_pts(cx, cy, 17 * s, 21 * s, 10), rng, 1, .08))
    lay = over(lay, local(pigment, knot, SATIN_D, SATIN, seed=SEQ(), density=0.95, edge=0.5, bloom=0, rough=1.2, feather=0.8))
    hl = shape_mask(W, H, ellipse_pts(cx - 4 * s, cy - 6 * s, 6 * s, 10 * s, 8, 0.3))
    lay = over(lay, local(pigment, gaussian_filter(hl, 2), SATIN_L, seed=SEQ(), density=0.5, edge=0, bloom=0, rough=1))
    return lay


def bow():
    W, H = 420, 420
    rng = random.Random(5)
    lay = bow_layer(W, H, 210, 130, 1.05, rng)
    preview(lay, "md-bow", "#f3e7e3")
    save(lay, f"{OUT}/bow.webp", max_w=260, quality=82)


def single_rose():
    W, H = 300, 300
    rng = random.Random(23)
    art_ = blank(W, H)
    for x, y, a in [(150, 190, 2.4), (150, 190, 0.7)]:
        art_ = glaze(art_, dried_leaf(W, H, x, y, 92, a, rng, 0.25))
    lay, base = dried_rose(W, H, 150, 145, 78, rng, 0)
    art_ = knockout(art_, base, 0.9, 3.0)
    art_ = glaze(art_, lay)
    preview(art_, "md-rose", "#f3e7e3")
    save(art_, f"{OUT}/rose.webp", max_w=180, quality=82)


def long_ribbon():
    W, H = 360, 1400
    pts = curve([(180, 0), (90, 220), (250, 480), (110, 760), (240, 1020), (150, 1260), (200, 1400)], 120)
    lay = ribbon(W, H, pts, 46, phase=0.4, freq=0.0085, seed=7)
    preview(lay, "md-ribbon", "#f3e7e3")
    save_full(lay, f"{OUT}/ribbon.webp", size=(180, 700), quality=78)


def sprig():
    """Horizontal divider: one dried rose stem laid flat with two leaves and a small ribbon tie."""
    W, H = 900, 200
    rng = random.Random(31)
    art_ = blank(W, H)
    pts = curve([(40, 120), (300, 104), (560, 110), (780, 96)], 50)
    art_ = G(art_, strokes(W, H, [(pts, 6, (0.05, 0.1))]), STEM, seed=SEQ(), density=0.8, edge=0.5, rough=1.2, feather=.7)
    for x, y, a, L in [(220, 108, -2.6, 74), (300, 104, 0.55, 66), (470, 108, -0.6, 70), (560, 110, 2.5, 60)]:
        art_ = glaze(art_, dried_leaf(W, H, x, y, L, a, rng, .2))
    flush()
    lb, _ = bud(W, H, 60, 118, 18, math.pi + 0.1, R_M, R_D, LEAF_B, SEQ, rng)
    art_ = glaze(art_, lb)
    lay, base = dried_rose(W, H, 800, 96, 58, rng, 0, tilt=0.8)
    art_ = knockout(art_, base, .85, 3)
    art_ = glaze(art_, lay)
    art_ = over(art_, ribbon(W, H, [(372, 82), (380, 106), (388, 134)], 24, phase=0.1, freq=0.01, seed=9))
    art_ = over(art_, ribbon(W, H, curve([(384, 108), (420, 140), (470, 150), (520, 176)], 20), 16, phase=0.7, freq=0.03, seed=10))
    preview(art_, "md-sprig", "#f3e7e3")
    save(art_, f"{OUT}/sprig.webp", max_w=440, quality=82)


for part in PARTS:
    {"paper": paper_tile, "bundle": bundle, "rose": single_rose, "bow": bow, "ribbon": long_ribbon, "sprig": sprig}[part]()
    flush()
kb(OUT)
