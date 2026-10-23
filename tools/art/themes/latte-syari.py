"""Latte Syari — coffee-with-milk still life, no figures: a latte seen from above (saucer, glazed cup, crema with an
abstract poured-foam swirl), a plain foam cup for monograms, caramel drizzle divider, poured milk-and-coffee wave
bands, three roasted beans, a faint coffee-ring stain. Watercolour washes for coffee, gouache for foam and ceramic.
Run: python3 -I latte-syari.py [part ...]   parts: cup mini swirl waves beans stain
Assets -> public/themes/art/latte-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i4_lib import *  # noqa

OUT = outdir("latte-syari")
PARTS = sys.argv[1:] or ["cup", "mini", "swirl", "waves", "beans", "stain"]
ESP, MOCHA, CARA, LATTE, CREAM, FOAM, MILK = "#3b2419", "#6b4430", "#b97a45", "#cfa57d", "#efe0cb", "#fbf4e8", "#fffaf2"
CERAMIC, CER_D = "#f6f0e6", "#d9cbb6"


def cup_top(W, H, cx, cy, R, nx, art_fn=None, saucer=True, handle=True):
    """Top view: saucer, cup wall and rim, coffee surface; art_fn paints the foam on the coffee."""
    art = blank(W, H)
    if saucer:
        sm = disc(W, H, cx + 6, cy + 10, R * 1.62)
        art = OV(art, sm, lambda m: col_arr(m, "#5a3a24", gaussian_filter(m, 14) * 0.22), pad=40)
        sm = disc(W, H, cx, cy, R * 1.58)
        art = GP(art, sm, CERAMIC, "#efe5d6", seed=nx(), rough=1.6, streak=0.15)
        well = ring_mask(W, H, cx, cy, R * 1.05, R * 1.28)
        art = G(art, gaussian_filter(well, 6), CER_D, "#cdbba2", seed=nx(), density=0.35, edge=0.1, bloom=0.1, rough=2, feather=2)
        rimg = ring_mask(W, H, cx, cy, R * 1.5, R * 1.56)
        art = G(art, rimg, "#c9b597", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1.2, feather=0.8)
    if handle:
        hm = shapes(W, H, [[(cx + R * 0.95, cy - R * 0.2), (cx + R * 1.5, cy - R * 0.17), (cx + R * 1.58, cy), (cx + R * 1.5, cy + R * 0.17), (cx + R * 0.95, cy + R * 0.2)]])
        art = OV(art, hm, lambda m: col_arr(m, "#5a3a24", np.roll(gaussian_filter(m, 6), 8, 0) * 0.25), pad=30)
        art = GP(art, hm, CERAMIC, "#e9dfcf", seed=nx(), rough=1.2, streak=0.12)
        hole = shapes(W, H, [[(cx + R * 1.1, cy - R * 0.08), (cx + R * 1.38, cy - R * 0.07), (cx + R * 1.38, cy + R * 0.07), (cx + R * 1.1, cy + R * 0.08)]])
        art = G(art, hole, CER_D, seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1, feather=1)
    cm = disc(W, H, cx, cy, R)
    art = OV(art, cm, lambda m: col_arr(m, "#4a2e1c", np.roll(gaussian_filter(m, 10), 10, 0) * 0.3), pad=40)
    art = GP(art, cm, MILK, CERAMIC, seed=nx(), rough=1.2, streak=0.12)
    inner = disc(W, H, cx, cy, R * 0.86)
    # inner wall shading: darker on the lit side's opposite
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wall = ring_mask(W, H, cx, cy, R * 0.86, R * 0.94)
    art = G(art, gaussian_filter(wall * np.clip(((xx - cx) + (yy - cy)) / R + 0.6, 0, 1), 3), CER_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1, feather=1)
    # coffee: watercolour crema, darker at the rim, lighter tan centre
    art = GP(art, inner, "#c08650", "#a8693a", seed=nx(), rough=1.0, streak=0.15)
    art = G(art, inner, CARA, LATTE, seed=nx(), density=0.35, edge=0.6, bloom=0.5, gran=0.5, rough=1.5, feather=1.0)
    rr = np.hypot(xx - cx, yy - cy) / (R * 0.86)
    art = G(art, inner * np.clip((rr - 0.55) * 2.2, 0, 1), MOCHA, CARA, seed=nx(), density=0.75, edge=0.2, bloom=0.3, rough=1, feather=2)
    if art_fn:
        art = art_fn(art, inner)
    # rim highlight
    hl = ring_mask(W, H, cx, cy, R * 0.955, R * 0.985) * np.clip(-((xx - cx) + (yy - cy)) / R, 0, 1)
    art = OV(art, hl, lambda m: col_arr(m, "#ffffff", m * 0.8), pad=10)
    return art


def foam_swirl(cx, cy, R, nx):
    """Abstract poured foam: a stack of nested crescents (each pour pushes into the last), dragged through by a line."""
    def paint(art, inner):
        H, W = inner.shape
        tilt = -0.32
        ca, sa = math.cos(tilt), math.sin(tilt)
        P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
        def soft(m, seed, amt=3.0):
            return np.clip(gaussian_filter(displace(m, seed, amt, 18), 1.6) * 1.15, 0, 1)
        for k in range(5):
            ex, ey = P(-R * 0.42 + k * R * 0.17, R * 0.02 * math.sin(k))
            rx, ry = R * (0.34 - k * 0.045), R * (0.5 - k * 0.07)
            fm = soft(ellipses(W, H, [(ex, ey, rx, ry, math.degrees(tilt))]), 30 + k)
            art = OV(art, fm * inner, lambda m: col_arr(m, MILK, m), pad=10)
            art = G(art, np.clip(fm - gaussian_filter(fm, 4), 0, 1) * inner * 2, CREAM, LATTE, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1, feather=1)
            cx2, cy2 = P(-R * 0.42 + k * R * 0.17 + rx * 0.22, R * 0.02 * math.sin(k))
            cm = soft(ellipses(W, H, [(cx2, cy2, rx * 0.8, ry * 0.86, math.degrees(tilt))]), 50 + k, 2.0)
            art = OV(art, cm * inner, lambda m: col_arr(m, "#bf8550", m * 0.97), pad=10)
            art = G(art, cm * inner, CARA, LATTE, seed=nx(), density=0.3, edge=0.5, bloom=0.4, gran=0.4, rough=1.2, feather=1)
        ex, ey = P(-R * 0.42 + 5 * R * 0.17, 0)
        fm = soft(ellipses(W, H, [(ex, ey, R * 0.1, R * 0.13, math.degrees(tilt))]), 70)
        art = OV(art, fm * inner, lambda m: col_arr(m, MILK, m), pad=10)
        line = curve([P(-R * 0.86, 1), P(-R * 0.2, -2), P(R * 0.35, 2), P(R * 0.62, 0)], 40)
        m = gaussian_filter(strokes(W, H, [(line, R * 0.028, (0.05, 0.7))]), 0.8)
        art = OV(art, m * inner, lambda mm: col_arr(mm, "#b77a45", mm * 0.95), pad=10)
        return art
    return paint


if "cup" in PARTS:
    W, H = 640, 640
    nx = Seq(500)
    art = cup_top(W, H, 300, 320, 176, nx, foam_swirl(300, 320, 176 * 0.86, nx))
    save(art, f"{OUT}/cup.webp", quality=82)
    prev(art, "ls-cup", "#efe0cb")
    clear()

if "mini" in PARTS:
    W, H = 360, 360
    nx = Seq(600)
    def plain(art, inner):
        fm = disc(W, H, 180, 180, 104)
        art = GP(art, fm * inner, FOAM, MILK, seed=nx(), rough=2.2, streak=0.15)
        ring = ring_mask(W, H, 180, 180, 96, 110)
        return G(art, gaussian_filter(ring, 4) * inner, CARA, seed=nx(), density=0.35, edge=0.2, bloom=0.1, rough=1, feather=2)
    art = cup_top(W, H, 180, 180, 150, nx, plain, saucer=False, handle=False)
    save(art, f"{OUT}/mini.webp", quality=82)
    prev(art, "ls-mini", "#efe0cb")
    clear()

if "swirl" in PARTS:
    W, H = 400, 80
    nx = Seq(700)
    pts = curve([(20, 46), (90, 30), (140, 52), (172, 36), (186, 20), (204, 26), (206, 46), (190, 54), (180, 40), (210, 34), (260, 52), (310, 30), (380, 42)], 120)
    m = strokes(W, H, [(pts, 4.2, (0.2, 0.3))])
    art = G(blank(W, H), m, CARA, MOCHA, seed=nx(), density=0.9, edge=0.6, bloom=0.1, gran=0.3, rough=1.2, feather=0.8)
    for x, y, r in [(110, 58, 3.2), (290, 22, 2.6), (60, 30, 2.2)]:
        art = G(art, disc(W, H, x, y, r), CARA, seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.8, feather=0.6)
    save(art, f"{OUT}/swirl.webp", quality=84)
    prev(art, "ls-swirl", "#fbf4e8")
    clear()

if "waves" in PARTS:
    W, H = 780, 380
    nx = Seq(800)
    rng = random.Random(81)
    art = blank(W, H)
    bands = [(0.0, FOAM, MILK), (0.2, CREAM, "#ead8bf"), (0.38, LATTE, "#c99f76"), (0.56, CARA, "#ad6f3d"), (0.74, MOCHA, "#5d3b29"), (0.88, ESP, "#2f1c13")]
    tops = []
    for i, (t, c1, c2) in enumerate(bands):
        y0 = 40 + t * (H - 40)
        ph = rng.uniform(0, 6); amp = 13 - i; wl = 260 + i * 50
        top = [(x, y0 + amp * math.sin(x / wl * math.tau + ph) + 5 * math.sin(x / 70 + ph * 2)) for x in range(-10, W + 11, 6)]
        tops.append(top)
        m = shape_mask(W, H, top + [(W + 10, H + 10), (-10, H + 10)], smooth=False)
        art = GP(art, m, c1, c2, seed=nx(), rough=2.0, streak=0.25)
        if i == 0:
            continue
        prevc = bands[i - 1][1]
        # milk folding into the darker layer: curls rolling off the boundary
        sheen = np.clip(gaussian_filter(m, 7) - m * 0.6, 0, 1) * (1 - m * 0.4)
        art = OV(art, sheen, lambda mm: col_arr(mm, prevc, mm * 0.5), pad=20)
        for k in range(0):
            j = rng.randint(8, len(top) - 20)
            bx, by = top[j]
            r0 = rng.uniform(9, 15)
            sp = spiral_pts(bx + r0, by + r0 * 0.9, r0, 1.5, math.pi * 1.05, 1.25, 50, 1)
            sp = [(x, y) for x, y in sp]
            tail = [(x, y + 1.5) for x, y in top[j - 14:j + 1]]
            sm = strokes(W, H, [(tail + sp, rng.uniform(3.0, 4.6), (0.05, 0.6))]) * m
            art = OV(art, sm, lambda mm: col_arr(mm, prevc, gaussian_filter(mm, 0.6) * 0.95), pad=8)
        st = [(x, y + 9 + 3 * math.sin(x / 33)) for x, y in top]
        sm = strokes(W, H, [(st, 1.4, (0.3, 0.3))]) * m
        art = OV(art, sm, lambda mm: col_arr(mm, prevc, mm * 0.35), pad=8)
    art = edge_fade(art, 3, "lr")
    save(art, f"{OUT}/waves.webp", quality=80)
    prev(art, "ls-waves", "#fbf4e8")
    clear()

if "beans" in PARTS:
    W, H = 220, 110
    nx = Seq(900)
    art = blank(W, H)
    for (x, y, a, s) in [(56, 58, 0.5, 1.0), (118, 46, -0.4, 0.92), (172, 64, 1.2, 0.85)]:
        pts = ellipse_pts(x, y, 30 * s, 20 * s, 20, a)
        m = shape_mask(W, H, pts)
        art = OV(art, m, lambda mm: col_arr(mm, "#2a160c", np.roll(gaussian_filter(mm, 4), 4, 0) * 0.3), pad=14)
        art = GP(art, m, "#5a3622", "#3e2416", seed=nx(), rough=1.2, streak=0.6)
        hl = shape_mask(W, H, ellipse_pts(x - math.cos(a) * 8 * s - 4, y - 7 * s, 14 * s, 6 * s, 14, a))
        art = OV(art, hl * m, lambda mm: col_arr(mm, "#a2714c", gaussian_filter(mm, 2.5) * 0.5), pad=8)
        ca, sa = math.cos(a), math.sin(a)
        crease = curve([(x - ca * 24 * s, y - sa * 24 * s), (x - ca * 8 * s - sa * 4, y - sa * 8 * s + ca * 4), (x + ca * 8 * s + sa * 4, y + sa * 8 * s - ca * 4), (x + ca * 24 * s, y + sa * 24 * s)], 30)
        cm = strokes(W, H, [(crease, 3.2 * s, (0.3, 0.3))])
        art = G(art, cm, "#24130a", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    save(art, f"{OUT}/beans.webp", quality=84)
    prev(art, "ls-beans", "#fbf4e8")
    clear()

if "stain" in PARTS:
    W, H = 420, 420
    nx = Seq(1000)
    rng = random.Random(3)
    ring = ring_mask(W, H, 210, 214, 150, 162)
    ring = displace(ring, 4, 5, 30)
    art = G(blank(W, H), ring, CARA, LATTE, seed=nx(), density=0.45, edge=0.9, bloom=0.4, gran=0.4, rough=4, feather=1.4)
    inner = disc(W, H, 210, 214, 150)
    art = G(art, inner, LATTE, seed=nx(), density=0.08, edge=0.4, bloom=0.5, rough=6, feather=3)
    for k in range(4):
        x, y = 210 + rng.uniform(-190, 190), 214 + rng.uniform(-190, 190)
        if math.hypot(x - 210, y - 214) < 175:
            continue
        art = G(art, disc(W, H, x, y, rng.uniform(4, 10)), CARA, seed=nx(), density=0.4, edge=0.7, bloom=0.2, rough=2, feather=1)
    save(art, f"{OUT}/stain.webp", quality=80)
    prev(art, "ls-stain", "#fbf4e8")
