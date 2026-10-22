"""Shan Shui — Chinese ink landscape (山水) on aged silk: tall layered peaks with hemp-fibre texture strokes, mist bands,
a waterfall between cliffs, gnarled pines with needle wheels, a small pavilion and a fishing boat, light indigo-green
and ochre washes. Assets: the tall scroll painting, a wide misty range, an overhanging pine, a mist puff, a scroll rod,
a vermilion seal block, a brush divider and a silk tile.
Run: python3 -I shan-shui.py [part ...]   parts: scroll range pine mist rod seal divider silk"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e4_lib import *

OUT = outdir("shan-shui")
PARTS = sys.argv[1:] or ["scroll", "range", "pine", "mist", "rod", "seal", "divider", "silk"]
SILK = "#ece3cc"
INK, INK2 = "#1d1c1a", "#3a3834"
GREY = "#7d8080"
BLUEGREEN, BLUEGREEN2 = "#6f9488", "#86a39a"
OCHRE = "#c4a06a"


def ridge_fade(mask, depth):
    """1 at the top edge of each column of the mask, fading downward (ink concentrated at the ridge)."""
    h, w = mask.shape
    m = mask > 0.5
    first = np.where(m.any(0), m.argmax(0), h).astype(np.float32)
    first = gaussian_filter(first, 3)
    yy = np.arange(h, dtype=np.float32)[:, None]
    d = np.clip(yy - first[None, :], 0, None)
    return np.exp(-d / depth) * mask


def peak(art, W, H, ridge, base_y, nx, rng, tone=INK, depth=60, density=0.7, cun=1.0, wash=None, wash_depth=None):
    """One ink mountain: ridge polyline closed down to base_y; dark ridge fading into mist + texture strokes."""
    poly = ridge + [(ridge[-1][0], base_y), (ridge[0][0], base_y)]
    m = shapes(W, H, [poly])
    if wash:
        art = G(art, ridge_fade(m, wash_depth or depth * 2.4), wash[0], wash[1], seed=nx(), density=0.55, edge=0.3, bloom=0.5, gran=0.3, rough=4, feather=2.5)
    fade = ridge_fade(m, depth)
    art = G(art, fade, mix(tone, "#ffffff", 0.35), tone, seed=nx(), density=density, edge=0.35, bloom=0.45, gran=0.45, rough=4, feather=1.8)
    # hemp-fibre / axe-cut texture strokes following the slope, denser near the ridge
    st = []
    xs = [p[0] for p in ridge]
    for _ in range(int(cun * (max(xs) - min(xs)) * 0.55)):
        x = rng.uniform(min(xs), max(xs))
        # ridge height at x
        ry = min((p[1] for p in ridge if abs(p[0] - x) < (max(xs) - min(xs)) / len(ridge)), default=base_y)
        y = ry + abs(rng.gauss(0, depth * 0.9)) + 4
        if y > base_y - 6:
            continue
        L = rng.uniform(8, 22)
        a = math.pi / 2 + rng.uniform(-0.5, 0.5)
        st.append(([(x, y), (x + math.cos(a) * L * 0.5 + rng.gauss(0, 1.5), y + math.sin(a) * L * 0.5), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(1.0, 2.2), (0.1, 0.6)))
    if st:
        sm = strokes(W, H, st) * m
        art = G(art, sm, tone, seed=nx(), density=0.55 * density / 0.7, edge=0.2, bloom=0, gran=0.5, rough=0.8, feather=0.5)
    # ridge contour: a broken dry line
    rl = strokes(W, H, [([(x, y + 1) for x, y in curve(ridge, 60)], 2.4, (0.05, 0.05))])
    rl *= (fbm(W, H, nx(), 30, 2) > 0.38)
    art = ink(art, rl, nx(), col=tone, col2=tone, density=0.8 * density / 0.7, bleed=0.12, dry=0.5, rough=1.2, pad=10)
    return art


def crag(art, W, H, cx, base_y, height, width, nx, rng, tone=INK, density=0.75, wash=None, lobes=3, fold=1.0, depth=None):
    """A craggy shan-shui mountain: main tall peak plus overlapping lower lobes in front, each with a dark ridge,
    long fold lines running down the face and clustered axe-cut texture strokes on the shadow side."""
    parts = [(cx, height, width)]
    for k in range(lobes):
        side = -1 if k % 2 == 0 else 1
        parts.append((cx + side * width * rng.uniform(0.18, 0.42), height * rng.uniform(0.45, 0.72), width * rng.uniform(0.45, 0.7)))
    parts.sort(key=lambda p: -p[1])
    for (px, ph, pw) in parts:
        ridge = mountain_profile(px - pw / 2, px + pw / 2, base_y, base_y - ph, rng, n=17, sharp=0.85, jag=0.22)
        # round "alum-head" bumps along the top
        ridge = [(x, y - (math.sin(i * 1.7 + rng.uniform(0, 3)) * 0.5 + 0.5) * ph * 0.05 * (0 < i < len(ridge) - 1)) for i, (x, y) in enumerate(ridge)]
        poly = ridge + [(ridge[-1][0], base_y), (ridge[0][0], base_y)]
        m = shapes(W, H, [poly])
        art = knockout(art, m, 0.55, 3)
        dp = depth or ph * 0.22
        if wash:
            art = G(art, ridge_fade(m, dp * 2.2), wash[0], wash[1], seed=nx(), density=0.5, edge=0.3, bloom=0.5, gran=0.3, rough=4, feather=2.5)
        art = G(art, ridge_fade(m, dp), mix(tone, "#ffffff", 0.4), tone, seed=nx(), density=density * 0.8, edge=0.4, bloom=0.5, gran=0.5, rough=4, feather=1.8)
        # fold lines from ridge high points downward
        folds, cun = [], []
        tops = [ridge[i] for i in range(1, len(ridge) - 1) if ridge[i][1] <= ridge[i - 1][1] and ridge[i][1] <= ridge[i + 1][1]] or [min(ridge, key=lambda p: p[1])]
        tops += [ridge[i] for i in range(2, len(ridge) - 2, 3)]
        for (tx, ty) in tops:
            Lf = ph * rng.uniform(0.25, 0.55) * fold
            dx = (tx - px) / max(1, pw / 2) * Lf * 0.35 + rng.uniform(-8, 8)
            f = curve([(tx, ty + 2), (tx + dx * 0.4 + rng.uniform(-6, 6), ty + Lf * 0.45), (tx + dx, ty + Lf)], 24)
            folds.append((f, rng.uniform(1.6, 2.8), (0.05, 0.7)))
            for (fx, fy, fa) in along(f, 7):
                if rng.random() < 0.75:
                    sd = -1 if tx < px else 1
                    L = rng.uniform(6, 16) * (1 - (fy - ty) / (Lf + 1)) + 4
                    a2 = fa + sd * rng.uniform(0.5, 1.0)
                    cun.append(([(fx, fy), (fx + math.cos(a2) * L, fy + math.sin(a2) * L)], rng.uniform(1.0, 1.8), (0.1, 0.5)))
        fm = strokes(W, H, folds) * m
        art = ink(art, fm * (fbm(W, H, nx(), 24, 2) > 0.3), nx(), col=tone, col2=tone, density=0.7 * density, bleed=0.1, dry=0.55, rough=1.2, pad=10)
        if cun:
            art = G(art, strokes(W, H, cun) * m, tone, seed=nx(), density=0.5 * density, edge=0.2, bloom=0, gran=0.5, rough=0.8, feather=0.5)
        rl = strokes(W, H, [([(x, y + 1) for x, y in curve(ridge, 80)], 2.8, (0.03, 0.03))]) * (fbm(W, H, nx(), 22, 2) > 0.42)
        art = ink(art, rl, nx(), col=tone, col2=tone, density=0.85 * density, bleed=0.12, dry=0.55, rough=1.4, pad=10)
        clear()
    return art


def mist(art, y0, y1, strength=1.0, seed=1):
    """Knock pigment back toward silk in a soft, uneven horizontal band."""
    h, w = art.shape[:2]
    yy = np.arange(h, dtype=np.float32)[:, None]
    c = (y0 + y1) / 2; half = (y1 - y0) / 2
    band = np.clip(1 - np.abs(yy - c) / half, 0, 1) ** 1.2 * np.ones((1, w), np.float32)
    n = fbm(w, h, seed, 90, 3)
    band = np.clip(band * (0.7 + 0.8 * n) * strength, 0, 1)
    out = art.copy()
    out[..., 3] *= 1 - band
    return out


def pine(art, W, H, x, y, h_, lean, nx, rng, scale=1.0, clusters=7):
    """Gnarled pine: bent trunk stroke, a few limbs, and needle 'wheels' (radiating short strokes) inked over a wash."""
    pts = [(x, y)]
    for i in range(1, 7):
        t = i / 6
        pts.append((x + lean * h_ * t + math.sin(t * 5 + rng.uniform(0, 1)) * h_ * 0.06, y - h_ * t))
    trunk = []
    for i in range(len(pts) - 1):
        w0 = (9 - i * 1.2) * scale
        trunk.append(([pts[i], pts[i + 1]], max(1.2, w0), None))
    limbs, heads = [], []
    for k in range(clusters):
        i = rng.randint(2, 6)
        bx, by = pts[i]
        side = -1 if k % 2 else 1
        L = h_ * rng.uniform(0.18, 0.4) * (1.2 - i / 8)
        ex, ey = bx + side * L, by - L * rng.uniform(0.05, 0.3)
        limbs.append(([(bx, by), ((bx + ex) / 2, (by + ey) / 2 + 4 * scale), (ex, ey)], 3.2 * scale, (0.0, 0.5)))
        heads.append((ex, ey))
    heads.append(pts[-1])
    art = ink(art, strokes(W, H, trunk + limbs), nx(), density=0.88, bleed=0.15, dry=0.5, rough=1.4, pad=12)
    # needle masses: a pale grey-green wash, then ink wheels
    pads, wheels = [], []
    for (hx, hy) in heads:
        rr = rng.uniform(13, 20) * scale
        pads.append((hx, hy - rr * 0.1, rr * 1.6, rr * 0.75, rng.uniform(-10, 10)))
        for j in range(rng.randint(2, 4)):
            cx, cy = hx + rng.uniform(-rr, rr), hy + rng.uniform(-rr * 0.4, rr * 0.25)
            for a in np.linspace(math.pi * 1.05, math.pi * 1.95, 9):
                L = rr * rng.uniform(0.55, 0.85)
                wheels.append(([(cx, cy), (cx + math.cos(a) * L, cy + math.sin(a) * L)], 1.3 * scale, (0.0, 0.5)))
    art = G(art, ellipses(W, H, pads), "#8a9e94", "#6f857a", seed=nx(), density=0.32, edge=0.4, bloom=0.4, gran=0.3, rough=3, feather=1.6)
    art = ink(art, strokes(W, H, wheels), nx(), density=0.85, bleed=0.1, dry=0.25, rough=0.8, pad=10)
    return art


def pavilion(art, W, H, x, y, s, nx):
    roof = [(x - s * 1.1, y - s * 0.55), (x - s * 0.5, y - s * 0.9), (x + s * 0.5, y - s * 0.9), (x + s * 1.1, y - s * 0.55), (x + s * 0.6, y - s * 0.62), (x - s * 0.6, y - s * 0.62)]
    art = ink(art, shapes(W, H, [roof], smooth=False), nx(), density=0.85, bleed=0.08, dry=0.2, rough=0.8, pad=8)
    posts = strokes(W, H, [([(x - s * 0.55, y - s * 0.6), (x - s * 0.55, y)], 1.6, None), ([(x + s * 0.55, y - s * 0.6), (x + s * 0.55, y)], 1.6, None), ([(x - s * 0.8, y), (x + s * 0.8, y)], 1.8, None)])
    return ink(art, posts, nx(), density=0.8, bleed=0, dry=0.1, rough=0.5, pad=8)


def boat(art, W, H, x, y, s, nx):
    hull = [(x - s, y), (x + s, y - s * 0.12), (x + s * 0.7, y + s * 0.18), (x - s * 0.7, y + s * 0.2)]
    art = ink(art, shapes(W, H, [hull]), nx(), density=0.8, bleed=0.08, dry=0.2, rough=0.6, pad=8)
    fig = strokes(W, H, [([(x + s * 0.15, y - s * 0.05), (x + s * 0.1, y - s * 0.45)], 2.4, None), ([(x + s * 0.12, y - s * 0.3), (x - s * 0.9, y - s * 1.1)], 1.0, None)])
    art = ink(art, fig, nx(), density=0.75, bleed=0, dry=0.1, rough=0.5, pad=8)
    ripples = strokes(W, H, [([(x - s * 1.6 + k * s * 0.9, y + s * 0.4 + (k % 2) * 4), (x - s * 1.0 + k * s * 0.9, y + s * 0.42 + (k % 2) * 4)], 1.0, (0.3, 0.3)) for k in range(4)])
    return G(art, ripples, GREY, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.4)


def silk_bg(W, H, seed=3):
    rgb = paper_tile(max(W, H), SILK, seed=seed, fiber=0.25, mottle=1.4)[:H, :W]
    stain = fbm(W, H, seed + 7, 160, 3)
    rgb = rgb * (1 - 0.06 * (stain[..., None] - 0.5))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.maximum(np.abs(xx - W / 2) / (W / 2), np.abs(yy - H / 2) / (H / 2))
    rgb = rgb * (1 - 0.07 * np.clip((d - 0.75) / 0.25, 0, 1) ** 2)[..., None]
    return np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)


if "scroll" in PARTS:
    W, H = 600, 1140
    rng = random.Random(3); nx = Seq(3000)
    art = blank(W, H)
    # far peaks (pale blue-grey)
    art = crag(art, W, H, 400, 560, 430, 300, nx, rng, tone="#7c8890", density=0.5, lobes=2, fold=0.7)
    art = crag(art, W, H, 150, 600, 330, 260, nx, rng, tone="#7c8890", density=0.45, lobes=2, fold=0.7)
    art = mist(art, 440, 640, 1.25, nx())
    # middle cliffs framing a waterfall
    art = crag(art, W, H, 130, 920, 600, 330, nx, rng, density=0.85, lobes=3, wash=(BLUEGREEN, BLUEGREEN2))
    art = crag(art, W, H, 500, 920, 470, 300, nx, rng, density=0.8, lobes=3, wash=(BLUEGREEN2, OCHRE))
    # waterfall: keep the gap clean, a few falling grey threads
    fall = shapes(W, H, [[(300, 520), (338, 520), (346, 880), (292, 880)]], smooth=False)
    art = knockout(art, fall, 1.0, 3)
    threads = strokes(W, H, [([(304 + k * 7 + rng.uniform(-2, 2), 525 + rng.uniform(0, 40)), (302 + k * 7.5, 700), (300 + k * 8 + rng.uniform(-3, 3), 860)], 1.0, (0.2, 0.3)) for k in range(6)])
    art = G(art, threads, "#7d8686", seed=nx(), density=0.7, edge=0.1, bloom=0.2, rough=0.6, feather=0.5)
    top_at = lambda x, y0: y0 + int(np.argmax(art[y0:, int(x), 3] > 0.6))
    art = pine(art, W, H, 118, top_at(118, 340) + 8, 80, 0.25, nx, rng, 0.85, 5)
    art = pine(art, W, H, 262, top_at(262, 520) + 8, 60, -0.2, nx, rng, 0.75, 4)
    art = pavilion(art, W, H, 520, top_at(520, 470) + 10, 22, nx)
    art = pine(art, W, H, 470, top_at(470, 600) + 8, 60, -0.3, nx, rng, 0.7, 4)
    art = mist(art, 760, 960, 1.3, nx())
    # foreground rocks and two big pines, water with a boat
    art = crag(art, W, H, 110, 1150, 230, 300, nx, rng, density=0.95, lobes=2, wash=(OCHRE, "#b48a58"), fold=0.8)
    art = pine(art, W, H, 150, top_at(150, 900) + 10, 210, 0.35, nx, rng, 1.4, 8)
    art = pine(art, W, H, 80, top_at(80, 900) + 10, 150, 0.55, nx, rng, 1.15, 6)
    art = boat(art, W, H, 440, 1060, 34, nx)
    bg = silk_bg(W, H)
    out = over(bg, art)
    clear()
    Image.fromarray((np.clip(out[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/ss-scroll.png")
    save_rgb(out, f"{OUT}/scroll.webp", size=(560, 1064), quality=78)

if "range" in PARTS:
    W, H = 1200, 360
    rng = random.Random(7); nx = Seq(7000)
    art = blank(W, H)
    for (x0, x1, top, base, tone, dens) in [(-40, 520, 60, 300, "#8a949a", 0.38), (420, 1040, 30, 300, "#8a949a", 0.38), (860, 1240, 110, 300, "#8a949a", 0.36),
                                             (-40, 380, 140, 360, INK, 0.62), (300, 760, 170, 360, "#3a3a38", 0.55), (700, 1240, 120, 360, INK, 0.66)]:
        r = mountain_profile(x0, x1, base, top, rng, n=13, sharp=1.0, jag=0.14)
        art = crag(art, W, H, (x0 + x1) / 2, base, base - top, x1 - x0, nx, rng, tone=tone, density=dens, lobes=2, fold=0.6, wash=(BLUEGREEN, BLUEGREEN2) if dens > 0.5 else None)
        if dens < 0.5:
            art = mist(art, 200, 330, 1.1, nx())
    art = mist(art, 270, 380, 1.4, nx())
    art = pine(art, W, H, 1010, 150, 60, 0.2, nx, rng, 0.7, 4)
    preview(art, "ss-range", tone=SILK)
    save_full(art, f"{OUT}/range.webp", size=(860, 258), quality=80)
    clear()

if "pine" in PARTS:
    W, H = 640, 520
    rng = random.Random(11); nx = Seq(11000)
    art = blank(W, H)
    trunk = curve([(660, 40), (540, 70), (420, 140), (330, 170), (220, 230), (120, 260), (40, 330)], 60)
    items = [([trunk[i], trunk[i + 1]], max(3, 22 - i * 0.3), None) for i in range(len(trunk) - 1)]
    heads = [(40, 330), (130, 250)]
    for (bi, side, L) in [(12, -1, 90), (22, 1, 70), (32, -1, 100), (42, 1, 80), (50, -1, 70)]:
        bx, by = trunk[bi]
        ex, ey = bx - L * 0.6, by + side * L * 0.6 + 40
        items.append(([(bx, by), ((bx + ex) / 2, (by + ey) / 2 - 10), (ex, ey)], 5, (0.0, 0.5)))
        heads.append((ex, ey))
    art = ink(art, strokes(W, H, items), nx(), density=0.9, bleed=0.18, dry=0.55, rough=1.5)
    pads, wheels = [], []
    for (hx, hy) in heads:
        rr = rng.uniform(26, 36)
        pads.append((hx, hy, rr * 1.7, rr * 0.8, rng.uniform(-12, 12)))
        for j in range(4):
            cx, cy = hx + rng.uniform(-rr * 1.1, rr * 1.1), hy + rng.uniform(-rr * 0.4, rr * 0.3)
            for a in np.linspace(math.pi * 1.0, math.pi * 2.0, 11):
                Ln = rr * rng.uniform(0.6, 0.9)
                wheels.append(([(cx, cy), (cx + math.cos(a) * Ln, cy + math.sin(a) * Ln)], 1.8, (0.0, 0.5)))
    art = G(art, ellipses(W, H, pads), "#8a9e94", "#6f857a", seed=nx(), density=0.34, edge=0.45, bloom=0.45, gran=0.3, rough=3, feather=1.8)
    art = ink(art, strokes(W, H, wheels), nx(), density=0.88, bleed=0.12, dry=0.25, rough=0.8)
    preview(art, "ss-pine", tone=SILK)
    save(art, f"{OUT}/pine.webp", max_w=300, quality=82)
    clear()

if "mist" in PARTS:
    W, H = 700, 220
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    e = np.exp(-(((xx - W / 2) / (W * 0.42)) ** 2 + ((yy - H / 2) / (H * 0.32)) ** 2) * 1.6)
    n = fbm(W, H, 13, 70, 4)
    a = np.clip(e * (0.5 + 0.9 * n) - 0.12, 0, 1) * 0.85
    arr = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f7f2e6"), np.float32), a[..., None]], -1)
    save_full(arr, f"{OUT}/mist.webp", size=(420, 132), quality=70)
    clear()

if "rod" in PARTS:
    W, H = 900, 70
    rng = random.Random(17); nx = Seq(17000)
    art = blank(W, H)
    body = shapes(W, H, [[(40, 22), (860, 22), (860, 48), (40, 48)]], smooth=False)
    art = GP(art, body, "#4a2f22", "#6a4430", seed=nx(), rough=1.0, streak=1.0)
    hl = shapes(W, H, [[(44, 26), (856, 26), (856, 31), (44, 31)]], smooth=False)
    art = OV(art, gaussian_filter(hl, 1.5), lambda m: layer(m, "#c39a72", 0.45))
    for cx in (22, 878):
        knob = ellipses(W, H, [(cx, 35, 22, 30, 0)])
        art = GP(art, knob, "#2b1d16", "#5b3a2a", seed=nx(), rough=1.0)
        art = OV(art, gaussian_filter(ellipses(W, H, [(cx - 6, 24, 7, 9, 0)]), 2), lambda m: layer(m, "#d8b48a", 0.4))
    preview(art, "ss-rod", tone=SILK)
    save(art, f"{OUT}/rod.webp", max_w=450, quality=84)
    clear()

if "seal" in PARTS:
    W = H = 240
    rng = random.Random(19); nx = Seq(19000)
    sq = shapes(W, H, [[(30 + rng.uniform(-3, 3), 28 + rng.uniform(-3, 3)), (212 + rng.uniform(-3, 3), 30 + rng.uniform(-3, 3)), (210 + rng.uniform(-3, 3), 214 + rng.uniform(-3, 3)), (28 + rng.uniform(-3, 3), 210 + rng.uniform(-3, 3))]], smooth=False)
    art = LC(blank(W, H), sq, "#b8322a", seed=nx(), wear=0.45, rough=2.5)
    preview(art, "ss-seal", tone=SILK)
    save(art, f"{OUT}/seal.webp", max_w=110, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 640, 120
    rng = random.Random(23); nx = Seq(23000)
    art = blank(W, H)
    line = curve([(40, 66), (180, 58), (330, 64), (480, 56), (600, 62)], 60)
    items = [([line[i], line[i + 1]], 7 * (0.35 + 0.65 * math.sin(math.pi * i / (len(line) - 1)) ** 0.5), None) for i in range(len(line) - 1)]
    art = ink(art, strokes(W, H, items), nx(), density=0.9, bleed=0.15, dry=0.65, rough=1.4)
    art = LC(art, shapes(W, H, [[(306, 44), (334, 45), (333, 72), (305, 71)]], smooth=False), "#b8322a", seed=nx(), wear=0.4)
    preview(art, "ss-divider", tone=SILK)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=84)
    clear()

if "silk" in PARTS:
    save_tile(paper_tile(360, SILK, seed=29, fiber=0.2, mottle=0.9), f"{OUT}/silk.webp", quality=80)
