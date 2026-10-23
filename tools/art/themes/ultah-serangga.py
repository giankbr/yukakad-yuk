"""Ultah Serangga — kids' birthday in a sunny garden: original cute bugs (ladybug, bee, butterfly, snail), a big
magnifying glass, grass and flowers, a sun. Opaque gouache, picture-book style.
Run: python3 -I ultah-serangga.py [part ...]  parts: garden lens ladybug bee butterfly snail sun sprig
Assets -> public/themes/art/ultah-serangga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m1_lib import *

OUT = outdir("ultah-serangga")
PARTS = sys.argv[1:] or ["garden", "lens", "ladybug", "bee", "butterfly", "snail", "sun", "sprig"]
INK = "#2b2a22"
RED, RED_D = "#e2412f", "#b52a1d"
YEL, YEL_D = "#ffc93c", "#e8a019"
GRN, GRN_L, GRN_D = "#5fae4a", "#8cc95f", "#3b7f35"
PINK = "#f4a4a0"
WHITE = "#fffbef"


def paint(art, m, c1, c2=None, nx=None, rough=1.6, streak=0.8):
    return GP(art, m, c1, c2 or c1, seed=nx(), rough=rough, streak=streak)


def below(H, y, soft=40):
    return np.clip((np.arange(H, dtype=np.float32)[:, None] - y) / soft, 0, 1)


def right_of(W, x, soft=30):
    return np.clip((np.arange(W, dtype=np.float32)[None, :] - x) / soft, 0, 1)


def shade(art, m, col, nx, k=0.35):
    return G(art, m, col, seed=nx(), density=k, edge=0.25, bloom=0.2, rough=2, feather=2)


def face(art, W, H, nx, x, y, s, look=(0.0, 0.0), smile=True, blush=True, eye_gap=1.0):
    """Cute face: two big eyes with pupils and glints, a smile and pink cheeks."""
    ex = 0.36 * s * eye_gap
    whites = circles(W, H, [(x - ex, y, 0.2 * s), (x + ex, y, 0.2 * s)])
    art = paint(art, whites, WHITE, nx=nx, rough=0.5, streak=0.2)
    pup = circles(W, H, [(x - ex + look[0] * s * 0.06, y + look[1] * s * 0.06 + s * 0.02, 0.13 * s), (x + ex + look[0] * s * 0.06, y + look[1] * s * 0.06 + s * 0.02, 0.13 * s)])
    art = paint(art, pup, INK, nx=nx, rough=0.4, streak=0.2)
    gl = circles(W, H, [(x - ex - s * 0.04, y - s * 0.04, 0.045 * s), (x + ex - s * 0.04, y - s * 0.04, 0.045 * s)])
    art = OV(art, gl, lambda m: rgba(np.ones(m.shape + (3,), np.float32), m))
    if blush:
        ch = circles(W, H, [(x - ex * 1.55, y + s * 0.26, 0.11 * s), (x + ex * 1.55, y + s * 0.26, 0.11 * s)])
        art = G(art, ch, PINK, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=2)
    if smile:
        sm = strokes(W, H, [(arc_pts(x, y + s * 0.16, s * 0.18, 0.35, math.pi - 0.35, 16), max(2, s * 0.05), (0.2, 0.2))])
        art = paint(art, sm, INK, nx=nx, rough=0.4, streak=0.1)
    return art


def ladybug_art(W, H, cx, cy, s, nx, rot=0.0):
    art = blank(W, H)
    legs = []
    for k in range(3):
        for side in (-1, 1):
            a = rot + side * (0.5 + k * 0.55)
            legs.append(([(cx + math.cos(a) * s * 0.5, cy + math.sin(a) * s * 0.3 + s * 0.05), (cx + math.cos(a) * s * 0.78, cy + math.sin(a) * s * 0.45 + s * 0.12)], s * 0.06, (0.0, 0.3)))
    art = paint(art, strokes(W, H, legs), INK, nx=nx, rough=0.8)
    body = shapes(W, H, [ellipse_pts(cx, cy + s * 0.08, s * 0.62, s * 0.52, 24)])
    art = paint(art, body, RED, "#ee5a3d", nx=nx)
    art = shade(art, body * below(H, cy + s * 0.25), RED_D, nx, 0.45)
    split = strokes(W, H, [([(cx, cy - s * 0.3), (cx, cy + s * 0.58)], s * 0.05, (0.05, 0.1))]) * body
    art = paint(art, split, INK, nx=nx, rough=0.6)
    spots = circles(W, H, [(cx - s * 0.3, cy + s * 0.02, s * 0.11), (cx + s * 0.32, cy + s * 0.06, s * 0.12), (cx - s * 0.22, cy + s * 0.34, s * 0.1),
                           (cx + s * 0.24, cy + s * 0.36, s * 0.09), (cx - s * 0.46, cy + s * 0.22, s * 0.06), (cx + s * 0.48, cy + s * 0.26, s * 0.06)]) * body
    art = paint(art, spots, INK, nx=nx, rough=0.6)
    hl = shapes(W, H, [ellipse_pts(cx - s * 0.28, cy - s * 0.18, s * 0.16, s * 0.06, 12, -0.5)])
    art = OV(art, hl, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#ffd8c8"), gaussian_filter(m, 1.5) * 0.7))
    head = shapes(W, H, [ellipse_pts(cx, cy - s * 0.42, s * 0.36, s * 0.27, 20)])
    art = paint(art, head, "#34322a", INK, nx=nx)
    ant = strokes(W, H, [(curve([(cx - s * 0.12, cy - s * 0.64), (cx - s * 0.26, cy - s * 0.86), (cx - s * 0.36, cy - s * 0.9)], 12), s * 0.04, (0.0, 0.2)),
                         (curve([(cx + s * 0.12, cy - s * 0.64), (cx + s * 0.26, cy - s * 0.86), (cx + s * 0.36, cy - s * 0.9)], 12), s * 0.04, (0.0, 0.2))])
    art = paint(art, ant, INK, nx=nx, rough=0.5)
    art = paint(art, circles(W, H, [(cx - s * 0.36, cy - s * 0.9, s * 0.06), (cx + s * 0.36, cy - s * 0.9, s * 0.06)]), INK, nx=nx, rough=0.4)
    art = face(art, W, H, nx, cx, cy - s * 0.46, s * 0.5, smile=True)
    return art


def ladybug():
    W = H = 300
    nx = Seq(100)
    art = ladybug_art(W, H, 150, 160, 200, nx)
    preview(art, "us-ladybug", bg="#cfe9b8")
    save(art, f"{OUT}/ladybug.webp", max_w=200, quality=84)


def bee():
    W, H = 340, 300
    nx = Seq(200)
    art = blank(W, H)
    cx, cy, s = 170, 170, 180
    wings = shapes(W, H, [petal_pts(cx - s * 0.05, cy - s * 0.3, s * 0.55, s * 0.24, -math.pi * 0.62, n=16), petal_pts(cx + s * 0.1, cy - s * 0.3, s * 0.5, s * 0.22, -math.pi * 0.36, n=16)])
    art = G(art, wings, "#d8eef6", "#bcdcec", seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=2)
    art = G(art, np.clip(wings - gaussian_filter(wings, 3) * 1.2, 0, 1) * 3, "#7aa6bf", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8, feather=0.6)
    body = shapes(W, H, [ellipse_pts(cx + s * 0.1, cy + s * 0.08, s * 0.5, s * 0.36, 24)])
    sting = shapes(W, H, [[(cx + s * 0.56, cy + s * 0.04), (cx + s * 0.74, cy + s * 0.1), (cx + s * 0.56, cy + s * 0.16)]], smooth=False)
    art = paint(art, sting, INK, nx=nx, rough=0.5)
    art = paint(art, body, YEL, "#ffd864", nx=nx)
    stripes = shapes(W, H, [[(cx + s * (0.06 + k * 0.2), cy - s * 0.4), (cx + s * (0.16 + k * 0.2), cy - s * 0.4), (cx + s * (0.12 + k * 0.2), cy + s * 0.5), (cx + s * (0.02 + k * 0.2), cy + s * 0.5)] for k in range(3)], smooth=False) * body
    art = paint(art, stripes, INK, "#3b382d", nx=nx, rough=1.0)
    art = shade(art, body * below(H, cy + s * 0.22), YEL_D, nx, 0.45)
    head = circles(W, H, [(cx - s * 0.36, cy + s * 0.02, s * 0.3)])
    art = paint(art, head, YEL, "#ffd864", nx=nx)
    ant = strokes(W, H, [(curve([(cx - s * 0.44, cy - s * 0.24), (cx - s * 0.56, cy - s * 0.46), (cx - s * 0.66, cy - s * 0.5)], 12), s * 0.035, (0.0, 0.2)),
                         (curve([(cx - s * 0.3, cy - s * 0.26), (cx - s * 0.32, cy - s * 0.5), (cx - s * 0.4, cy - s * 0.58)], 12), s * 0.035, (0.0, 0.2))])
    art = paint(art, ant, INK, nx=nx, rough=0.5)
    art = paint(art, circles(W, H, [(cx - s * 0.66, cy - s * 0.5, s * 0.05), (cx - s * 0.4, cy - s * 0.58, s * 0.05)]), INK, nx=nx, rough=0.4)
    art = face(art, W, H, nx, cx - s * 0.38, cy + s * 0.0, s * 0.42, look=(-0.4, 0))
    preview(art, "us-bee", bg="#cfe9b8")
    save(art, f"{OUT}/bee.webp", max_w=220, quality=84)


def butterfly():
    W, H = 360, 300
    nx = Seq(300)
    art = blank(W, H)
    cx, cy = 180, 150
    up = [deform(ellipse_pts(cx + side * 70, cy - 46, 74, 62, 16, side * -0.5), random.Random(3 + side), 1, 0.05) for side in (-1, 1)]
    lo = [deform(ellipse_pts(cx + side * 52, cy + 52, 50, 46, 16, side * 0.6), random.Random(5 + side), 1, 0.05) for side in (-1, 1)]
    wu = shapes(W, H, up); wl = shapes(W, H, lo)
    art = paint(art, wl, "#a979d6", "#c79be8", nx=nx)
    art = paint(art, wu, "#ff9a3d", "#ffb65c", nx=nx)
    art = shade(art, np.maximum(wu, wl) * np.clip(1 - np.abs(np.arange(W)[None, :] - cx) / 60, 0, 1), "#c4562a", nx, 0.4)
    edge = np.clip(np.maximum(wu, wl) - gaussian_filter((np.maximum(wu, wl) > 0.5).astype(np.float32), 5) * 1.3, 0, 1) * 2
    art = paint(art, np.clip(edge, 0, 1), "#5b3a7a", nx=nx, rough=0.8)
    dots = circles(W, H, [(cx + side * dx, cy + dy, r) for side in (-1, 1) for dx, dy, r in [(96, -60, 12), (64, -30, 8), (110, -24, 6), (62, 64, 10), (36, 80, 6)]])
    art = paint(art, dots, WHITE, nx=nx, rough=0.5)
    dots2 = circles(W, H, [(cx + side * 96, cy - 60, 6) for side in (-1, 1)])
    art = paint(art, dots2, "#e2412f", nx=nx, rough=0.4)
    body = shapes(W, H, [ellipse_pts(cx, cy + 10, 13, 70, 16)])
    art = paint(art, body, "#4a3b5c", "#33283f", nx=nx, rough=0.8)
    head = circles(W, H, [(cx, cy - 66, 26)])
    art = paint(art, head, "#4a3b5c", "#33283f", nx=nx, rough=0.8)
    ant = strokes(W, H, [(spiral_pts(cx - 30, cy - 120, 10, 2, 0, 0.9, 20, -1)[::-1] + [(cx - 8, cy - 88)], 3.5, (0.0, 0.1)),
                         (spiral_pts(cx + 30, cy - 120, 10, 2, math.pi, 0.9, 20, 1)[::-1] + [(cx + 8, cy - 88)], 3.5, (0.0, 0.1))])
    art = paint(art, ant, "#33283f", nx=nx, rough=0.5)
    art = face(art, W, H, nx, cx, cy - 68, 54, blush=True)
    preview(art, "us-butterfly", bg="#cfe9b8")
    save(art, f"{OUT}/butterfly.webp", max_w=220, quality=84)


def snail():
    W, H = 380, 300
    nx = Seq(400)
    art = blank(W, H)
    foot = shapes(W, H, [curve([(40, 262), (90, 236), (220, 234), (300, 232), (336, 170), (356, 150), (372, 176), (350, 250), (300, 270), (60, 274), (40, 262)], 60)])
    art = paint(art, foot, "#b8d98a", "#cfe6a6", nx=nx)
    art = shade(art, foot * below(H, 254), GRN_D, nx, 0.35)
    stalks = strokes(W, H, [([(346, 170), (340, 118)], 9, (0.0, 0.0)), ([(362, 172), (372, 122)], 9, (0.0, 0.0))])
    art = paint(art, stalks, "#b8d98a", nx=nx)
    shell = circles(W, H, [(176, 160, 100)])
    art = paint(art, shell, "#f29a4a", "#f7b768", nx=nx)
    art = shade(art, shell * below(H, 200), "#c4652a", nx, 0.5)
    sp = spiral_pts(186, 166, 84, 6, math.pi * 1.1, 2.4, 140, 1)
    art = paint(art, strokes(W, H, [(sp, 10, (0.02, 0.4))]) * shell, "#a84a20", "#c45a28", nx=nx, rough=0.8)
    hl = shapes(W, H, [ellipse_pts(130, 100, 30, 12, 12, -0.7)])
    art = OV(art, hl, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#ffe0b8"), gaussian_filter(m, 2) * 0.7))
    # eyes on stalks
    for ex, ey in [(338, 112), (374, 116)]:
        art = paint(art, circles(W, H, [(ex, ey, 16)]), WHITE, nx=nx, rough=0.4)
        art = paint(art, circles(W, H, [(ex + 3, ey + 2, 9)]), INK, nx=nx, rough=0.3)
        art = OV(art, circles(W, H, [(ex, ey - 3, 3.5)]), lambda m: rgba(np.ones(m.shape + (3,), np.float32), m))
    sm = strokes(W, H, [(arc_pts(354, 200, 14, 0.3, math.pi - 0.3, 12), 4, (0.2, 0.2))])
    art = paint(art, sm, INK, nx=nx, rough=0.3)
    art = G(art, circles(W, H, [(334, 212, 9)]), PINK, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1, feather=2)
    preview(art, "us-snail", bg="#cfe9b8")
    save(art, f"{OUT}/snail.webp", max_w=240, quality=84)


def lens():
    """Big magnifying glass: thick red-orange rim with a glass glare, wooden handle angled down-right."""
    W, H = 560, 640
    nx = Seq(500)
    art = blank(W, H)
    cx, cy, R = 262, 262, 236
    handle = strokes(W, H, [([(cx + R * 0.72, cy + R * 0.72), (cx + R * 1.12, cy + R * 1.4)], 56, (0.0, 0.0))])
    art = paint(art, handle, "#9a5a2e", "#b8733e", nx=nx, streak=1.4)
    art = shade(art, handle * right_of(W, cx + R * 0.9), "#5a3214", nx, 0.5)
    collar = strokes(W, H, [([(cx + R * 0.7, cy + R * 0.7), (cx + R * 0.86, cy + R * 0.94)], 64, None)])
    art = paint(art, collar, "#2f6fb5", "#3f86cc", nx=nx)
    ring = np.clip(circles(W, H, [(cx, cy, R)]) - circles(W, H, [(cx, cy, R - 34)]), 0, 1)
    art = paint(art, ring, RED, "#f26a3c", nx=nx)
    art = shade(art, ring * below(H, cy + R * 0.3), RED_D, nx, 0.5)
    hi = np.clip(circles(W, H, [(cx, cy, R - 6)]) - circles(W, H, [(cx, cy, R - 14)]), 0, 1) * (np.arange(H)[:, None] < cy - R * 0.2)
    art = OV(art, hi, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#ffd0b8"), gaussian_filter(m, 1) * 0.8))
    # glass glare (translucent) inside
    glass = circles(W, H, [(cx, cy, R - 33)])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3("#dff3ff"), glass * 0.10))
    gl = strokes(W, H, [(arc_pts(cx, cy, R - 62, math.pi * 1.08, math.pi * 1.42, 24), 16, (0.2, 0.3)),
                        (arc_pts(cx, cy, R - 62, math.pi * 1.5, math.pi * 1.56, 8), 16, (0.2, 0.2))])
    art = OV(art, gl, lambda m: rgba(np.ones(m.shape + (3,), np.float32), gaussian_filter(m, 1.2) * 0.75))
    preview(art, "us-lens", bg="#9fd27a")
    save_full(art, f"{OUT}/lens.webp", size=(420, 480), quality=82)


def flower(art, W, H, x, y, r, col, eye, nx, petals=6, rng=None):
    rng = rng or random.Random(int(x * 7 + y))
    rot = rng.uniform(0, 1)
    pm = shapes(W, H, [petal_pts(x, y, r, r * 0.5, rot + k * math.tau / petals, n=12) for k in range(petals)])
    art = paint(art, pm, col, mix(col, "#ffffff", 0.25), nx=nx)
    art = paint(art, circles(W, H, [(x, y, r * 0.32)]), eye, nx=nx, rough=0.6)
    return art


def garden():
    """Front garden band: big leaves, grass tufts, daisies, tulips and a red mushroom, transparent sky."""
    W, H = 800, 380
    rng = random.Random(6); nx = Seq(600)
    art = blank(W, H)
    hillm = shapes(W, H, [[(-20, H + 10)] + [(x, H * 0.5 + 26 * math.sin(x / 120) + 10 * math.sin(x / 41)) for x in range(-20, W + 40, 20)] + [(W + 20, H + 10)]], smooth=False)
    art = paint(art, hillm, "#7cc35a", "#8fd067", nx=nx, streak=1.2)
    art = shade(art, hillm * below(H, H * 0.75), GRN_D, nx, 0.4)
    # back big leaves
    for (x, L, a) in [(40, 220, -1.9), (90, 200, -1.25), (740, 230, -1.25), (690, 190, -1.95), (400, 150, -1.6)]:
        m = shapes(W, H, [petal_pts(x, H - 10, L, L * 0.32, a, n=14)])
        art = paint(art, m, GRN, GRN_L, nx=nx)
        half = shapes(W, H, [petal_pts(x, H - 10, L * 0.96, L * 0.15, a + 0.08, n=12)])
        art = shade(art, half, GRN_D, nx, 0.35)
        art = paint(art, strokes(W, H, [([(x, H - 10), (x + math.cos(a) * L * 0.85, H - 10 + math.sin(a) * L * 0.85)], 3, (0.05, 0.4))]), "#3b7f35", nx=nx, rough=0.5)
    # stems + flowers
    specs = [(170, 0.56, 26, "#ffffff", YEL), (250, 0.48, 22, "#ff8fb0", "#ffd45c"), (330, 0.6, 18, "#ffffff", YEL), (520, 0.52, 24, "#ffd45c", "#e27a2c"),
             (600, 0.44, 22, "#ffffff", YEL), (470, 0.66, 16, "#b98ae0", "#ffd45c"), (120, 0.7, 16, "#ff8fb0", YEL), (660, 0.64, 18, "#ff8fb0", YEL)]
    st = strokes(W, H, [(curve([(x, H), (x + rng.uniform(-10, 10), H * (t + 1) / 2), (x, H * t)], 12), 4, (0.0, 0.0)) for x, t, r, c, e in specs])
    art = paint(art, st, GRN_D, "#4b9140", nx=nx, rough=0.6)
    for x, t, r, c, e in specs:
        art = flower(art, W, H, x, H * t, r, c, e, nx)
    # tulips
    for x, t, c in [(380, 0.5, "#e2412f"), (420, 0.58, "#ff8fb0")]:
        art = paint(art, strokes(W, H, [([(x, H), (x, H * t)], 4, None)]), GRN_D, nx=nx, rough=0.5)
        tm = shapes(W, H, [[(x - 18, H * t - 2), (x - 20, H * t - 34), (x - 8, H * t - 24), (x, H * t - 40), (x + 8, H * t - 24), (x + 20, H * t - 34), (x + 18, H * t - 2), (x, H * t + 10)]])
        art = paint(art, tm, c, mix(c, "#ffffff", 0.2), nx=nx)
    # mushroom
    mx, my = 300, H - 40
    art = paint(art, shapes(W, H, [[(mx - 16, my + 34), (mx - 12, my - 6), (mx + 12, my - 6), (mx + 16, my + 34)]]), WHITE, "#efe6cf", nx=nx)
    cap = shapes(W, H, [curve([(mx - 52, my), (mx - 40, my - 40), (mx, my - 56), (mx + 40, my - 40), (mx + 52, my), (mx, my - 8), (mx - 52, my)], 40)])
    art = paint(art, cap, RED, "#ee5a3d", nx=nx)
    art = paint(art, circles(W, H, [(mx - 22, my - 28, 8), (mx + 14, my - 38, 9), (mx + 32, my - 16, 6), (mx - 6, my - 14, 5)]) * cap, WHITE, nx=nx, rough=0.4)
    # grass tufts in front
    blades = []
    for _ in range(170):
        x = rng.uniform(-10, W + 10); L = rng.uniform(26, 64); a = -math.pi / 2 + rng.uniform(-0.5, 0.5)
        blades.append(([(x, H + 4), (x + math.cos(a) * L * 0.5, H - L * 0.5), (x + math.cos(a) * L, H + math.sin(a) * L)], rng.uniform(5, 9), (0.0, 0.8)))
    art = paint(art, strokes(W, H, blades), "#4f9e3d", "#6bb84c", nx=nx, rough=0.8)
    preview(art, "us-garden", bg="#bfe6f5")
    save(art, f"{OUT}/garden.webp", max_w=720, quality=80)


def sun():
    W = H = 300
    nx = Seq(700)
    art = blank(W, H)
    rays = strokes(W, H, [([(150 + math.cos(a) * 92, 150 + math.sin(a) * 92), (150 + math.cos(a) * 138, 150 + math.sin(a) * 138)], 16, (0.1, 0.6)) for a in np.linspace(0, math.tau, 13)[:-1]])
    art = paint(art, rays, "#ffd45c", YEL, nx=nx)
    disc = circles(W, H, [(150, 150, 82)])
    art = paint(art, disc, YEL, "#ffd864", nx=nx)
    art = shade(art, disc * below(H, 180), YEL_D, nx, 0.35)
    art = face(art, W, H, nx, 150, 146, 90)
    save(art, f"{OUT}/sun.webp", max_w=200, quality=84)


def sprig():
    """Divider: a curling vine with small leaves and a tiny ladybug at the middle."""
    W, H = 380, 80
    nx = Seq(800)
    art = blank(W, H)
    vine = curve([(14, 46), (100, 34), (190, 48), (280, 34), (366, 46)], 60)
    art = paint(art, strokes(W, H, [(vine, 4, (0.05, 0.05))]), GRN_D, nx=nx, rough=0.5)
    leaves = []
    for k, (px, py, a) in enumerate(along(vine, 26)):
        if abs(px - W / 2) < 30:
            continue
        side = 1 if k % 2 else -1
        leaves.append(petal_pts(px, py, 28, 13, a + side * 1.0 - (0 if side > 0 else 0), n=10))
    art = paint(art, shapes(W, H, leaves), GRN, GRN_L, nx=nx, rough=0.8)
    lb = ladybug_art(W, H, W / 2, 36, 40, nx)
    art = over(art, lb)
    save(art, f"{OUT}/sprig.webp", max_w=340, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
