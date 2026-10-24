"""Upacara Teh — a Japanese tea ceremony in sumi line + light watercolour: iron kettle, a hand-thrown chawan of frothy
matcha, bamboo whisk and scoop, black lacquer caddy; one camellia in a slender vase; a tatami tile, washi tile,
steam wisps and a matcha brush stroke.
Run: python3 -I upacara-teh.py [part ...]  parts: tea flower steam tatami washi stroke bowl whisk
Assets -> public/themes/art/upacara-teh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q6_lib import *

OUT = outdir("upacara-teh")
PARTS = sys.argv[1:] or ["tea", "flower", "steam", "tatami", "washi", "stroke", "bowl", "whisk"]
SUMI = "#2b2a26"
MATCHA, MATCHA_D, MATCHA_L = "#7d9640", "#55692a", "#b3c477"
IRON, IRON_D = "#3b3936", "#1f1e1c"
BAMBOO, BAMBOO_D = "#d9c48e", "#b49a5c"


def ink(art, W, H, pts, w, a=0.75, taper=(0.1, 0.25), seed=1):
    m = strokes(W, H, [(pts, w, taper)])
    m = displace(m, seed, 1.2, 8)
    return OV(art, m, lambda q: flat(q, SUMI, a))


def kettle(art, W, H, cx, by, s, rng, nx):
    """Iron kama: squat round body, a flat lid with knob, two lugs, a rough cast surface."""
    body = shapes(W, H, [deform(arc_pts(cx, by - s * 0.42, s * 0.6, 0.0, math.pi, 30, 0.72) + arc_pts(cx, by - s * 0.42, s * 0.6, math.pi, math.tau, 30, 0.46), rng, 1, 0.015)])
    art = G(art, body, IRON, IRON_D, seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=2, feather=0.9, gran=0.7)
    # cast texture: dots of rust/dark
    tex = circles(W, H, [(cx + rng.uniform(-0.55, 0.55) * s, by - s * rng.uniform(0.15, 0.7), rng.uniform(0.5, 1.4)) for _ in range(90)]) * body
    art = OV(art, tex, lambda q: flat(q, "#1c1a18", 0.6))
    rust = displace(circles(W, H, [(cx + s * 0.3, by - s * 0.3, s * 0.15), (cx - s * 0.35, by - s * 0.5, s * 0.08)]), nx(), 6, 14) * body
    art = G(art, rust, "#7a4a2e", seed=nx(), density=0.3, edge=0.2, rough=4, feather=3)
    hl = strokes(W, H, [(arc_pts(cx, by - s * 0.42, s * 0.5, 3.6, 4.3, 12, 0.6), s * 0.05, (0.3, 0.3))]) * body
    art = OV(art, gaussian_filter(hl, 2), lambda q: flat(q, "#b8b2a6", 0.5))
    # shoulder ridge (hane) and lid
    art = ink(art, W, H, arc_pts(cx, by - s * 0.42, s * 0.6, math.pi * 1.02, math.tau * 0.99, 30, 0.2), 2.4, 0.7, seed=nx())
    lid = shapes(W, H, [ellipse_pts(cx, by - s * 0.66, s * 0.3, s * 0.07, 16)])
    art = G(art, lid, "#5a5650", IRON_D, seed=nx(), density=0.9, edge=0.5, rough=1, feather=0.7, gran=0.6)
    knob = shapes(W, H, [ellipse_pts(cx, by - s * 0.72, s * 0.06, s * 0.04, 10)])
    art = G(art, knob, "#3a3632", seed=nx(), density=0.95, edge=0.4, rough=0.6, feather=0.6)
    for side in (-1, 1):
        lug = shapes(W, H, [ellipse_pts(cx + side * s * 0.5, by - s * 0.6, s * 0.07, s * 0.05, 10)])
        art = G(art, lug, IRON_D, seed=nx(), density=0.95, rough=0.8, feather=0.6)
    art = ink(art, W, H, arc_pts(cx, by - s * 0.42, s * 0.6, 0.05, math.pi - 0.05, 30, 0.72), 2.0, 0.6, seed=nx())
    return art, body


def chawan(art, W, H, cx, by, s, rng, nx, glaze_a="#cdb38f", glaze_b="#b88f6a"):
    """Hand-thrown tea bowl (3/4 view): uneven rim, glaze drip to a bare foot, frothy matcha inside."""
    rim_y = by - s * 0.62
    outer = deform([(cx - s * 0.62, rim_y), (cx - s * 0.6, rim_y + s * 0.26), (cx - s * 0.46, by - s * 0.14), (cx - s * 0.22, by - s * 0.03), (cx + s * 0.22, by - s * 0.03), (cx + s * 0.47, by - s * 0.15), (cx + s * 0.61, rim_y + s * 0.25), (cx + s * 0.63, rim_y)] +
                   arc_pts(cx, rim_y, s * 0.625, 0.0, math.pi, 20, 0.2), rng, 1, 0.01)
    body = shapes(W, H, [outer])
    art = G(art, body, glaze_a, glaze_b, seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=2.5, feather=0.9, gran=0.5)
    # glaze pools darker at the lower body, bare clay foot
    low = body * ramp_y(H, W, rim_y + s * 0.2, by)
    art = G(art, low, "#8f6a4c", seed=nx(), density=0.45, edge=0.3, rough=3, feather=2)
    drips = strokes(W, H, [([(cx + u * s, rim_y + s * 0.05), (cx + u * s * 0.98, rim_y + s * rng.uniform(0.3, 0.5))], s * 0.05, (0.0, 0.6)) for u in (-0.45, -0.2, 0.1, 0.38)]) * body
    art = G(art, drips, "#e8dcc4", seed=nx(), density=0.4, edge=0.4, rough=2, feather=1.2)
    foot = shapes(W, H, [[(cx - s * 0.26, by - s * 0.06), (cx + s * 0.26, by - s * 0.06), (cx + s * 0.24, by), (cx - s * 0.24, by)]])
    art = G(art, foot, "#c99a72", "#b07e58", seed=nx(), density=0.8, edge=0.4, rough=1.5, feather=0.8, gran=0.6)
    # interior + matcha
    inner = shapes(W, H, [deform(ellipse_pts(cx, rim_y, s * 0.6, s * 0.12, 24), rng, 1, 0.02)])
    art = G(art, inner, "#6e5440", seed=nx(), density=0.75, edge=0.4, rough=1.5, feather=0.8)
    tea = shapes(W, H, [ellipse_pts(cx + s * 0.02, rim_y + s * 0.015, s * 0.5, s * 0.085, 24)])
    art = G(art, tea, MATCHA_L, MATCHA, seed=nx(), density=0.95, edge=0.45, bloom=0.5, rough=1.2, feather=0.8, gran=0.3)
    foam = shapes(W, H, [deform(ellipse_pts(cx - s * 0.05, rim_y + s * 0.01, s * 0.3, s * 0.045, 16), rng, 2, 0.15)])
    art = G(art, foam, "#d4e0a0", seed=nx(), density=0.5, edge=0.3, bloom=0.5, rough=3, feather=2)
    froth = circles(W, H, [(cx + rng.uniform(-0.42, 0.42) * s, rim_y + rng.uniform(-0.05, 0.07) * s, rng.uniform(0.4, 1.1)) for _ in range(60)]) * tea
    art = OV(art, froth, lambda q: flat(q, "#eef3d2", 0.45))
    art = ink(art, W, H, arc_pts(cx, rim_y, s * 0.62, math.pi * 0.02, math.pi * 0.98, 30, 0.2), 2.0, 0.7, seed=nx())
    art = ink(art, W, H, [(cx - s * 0.6, rim_y + s * 0.02), (cx - s * 0.58, rim_y + s * 0.3), (cx - s * 0.44, by - s * 0.14), (cx - s * 0.2, by - s * 0.04)], 1.8, 0.55, seed=nx())
    return art, body


def chasen(art, W, H, cx, by, s, rng, nx):
    """Bamboo whisk standing on its handle: tines flare in a bulb, bound by thread, handle below."""
    bulb_top, bulb_bot = by - s * 1.0, by - s * 0.42
    tines = []
    for k in range(30):
        u = (k / 29 - 0.5)
        x0 = cx + u * s * 0.18
        xm = cx + u * s * 0.42
        tines.append((curve([(x0, bulb_bot), (xm, bulb_top + s * 0.25), (cx + u * s * 0.24, bulb_top + s * 0.02 * abs(u) * 4)], 10), 1.4, (0.0, 0.2)))
    tm = strokes(W, H, tines)
    art = G(art, tm, BAMBOO, BAMBOO_D, seed=nx(), density=0.85, edge=0.5, rough=0.5, feather=0.4, gran=0.2)
    art = OV(art, strokes(W, H, tines[::3]), lambda q: flat(q, "#9a7e44", 0.45))
    core = shapes(W, H, [ellipse_pts(cx, bulb_top + s * 0.28, s * 0.07, s * 0.2, 12)])
    art = G(art, core, "#c4ab6e", seed=nx(), density=0.5, rough=1, feather=1)
    thread = strokes(W, H, [([(cx - s * 0.13, bulb_bot - s * 0.04), (cx + s * 0.13, bulb_bot - s * 0.04)], s * 0.035, None)])
    art = OV(art, thread, lambda q: flat(q, "#3a2e26", 0.85))
    handle = shapes(W, H, [[(cx - s * 0.11, bulb_bot), (cx + s * 0.11, bulb_bot), (cx + s * 0.1, by), (cx - s * 0.1, by)]], smooth=False)
    art = G(art, handle, "#dcc99a", BAMBOO_D, seed=nx(), density=0.85, edge=0.5, rough=1, feather=0.7)
    art = ink(art, W, H, [(cx - s * 0.11, bulb_bot + s * 0.25), (cx + s * 0.11, bulb_bot + s * 0.25)], 1.6, 0.5, seed=nx())
    art = ink(art, W, H, [(cx - s * 0.1, bulb_bot + 2), (cx - s * 0.1, by)], 1.4, 0.5, seed=nx())
    return art


def scoop(art, W, H, x0, y0, x1, y1, rng, nx):
    pts = bez((x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 6), (x1, y1), 20)
    m = strokes(W, H, [(pts, 6, (0.05, 0.05))])
    art = G(art, m, BAMBOO, BAMBOO_D, seed=nx(), density=0.85, edge=0.5, rough=0.6, feather=0.6)
    node = strokes(W, H, [([(x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.55 - 5), (x0 + (x1 - x0) * 0.55 + 2, y0 + (y1 - y0) * 0.55 + 4)], 2, None)])
    art = OV(art, node, lambda q: flat(q, "#8a6a3a", 0.8))
    art = ink(art, W, H, pts, 1.2, 0.5, (0.1, 0.1), seed=nx())
    return art


def natsume(art, W, H, cx, by, s, rng, nx):
    body = shapes(W, H, [[(cx - s * 0.5, by - s * 0.55), (cx + s * 0.5, by - s * 0.55), (cx + s * 0.48, by - s * 0.1), (cx + s * 0.36, by), (cx - s * 0.36, by), (cx - s * 0.48, by - s * 0.1)]])
    art = G(art, body, "#2a2422", "#141110", seed=nx(), density=0.95, edge=0.4, rough=1, feather=0.6)
    top = shapes(W, H, [ellipse_pts(cx, by - s * 0.56, s * 0.5, s * 0.14, 20)])
    art = G(art, top, "#3a3230", "#1a1614", seed=nx(), density=0.95, rough=0.8, feather=0.6)
    art = OV(art, gaussian_filter(strokes(W, H, [([(cx - s * 0.36, by - s * 0.45), (cx - s * 0.34, by - s * 0.12)], s * 0.06, (0.3, 0.3))]), 1.5), lambda q: flat(q, "#a8a29a", 0.5))
    art = OV(art, strokes(W, H, [([(cx - s * 0.5, by - s * 0.42), (cx + s * 0.5, by - s * 0.42)], 1.2, None)]) * body, lambda q: flat(q, "#6a6260", 0.6))
    # a gold-leaf maple leaf hint (makie)
    return art


def tea():
    W, H = 820, 440
    rng = random.Random(3); nx = Seq(100)
    art = blank(W, H)
    by = 400
    # shadows on the tatami (soft, cool)
    sh = ellipses(W, H, [(190, by + 4, 150, 22, 0), (440, by + 4, 120, 16, 0), (620, by + 4, 50, 8, 0), (720, by + 4, 60, 10, 0)])
    art = over(art, flat(gaussian_filter(sh, 9), "#3a3a20", 0.28))
    art, _ = kettle(art, W, H, 190, by, 230, rng, nx)
    # trivet / furo rim under the kettle
    art = G(art, shapes(W, H, [[(60, by - 8), (320, by - 8), (330, by + 4), (50, by + 4)]], smooth=False), "#6a5440", "#4a3a2c", seed=nx(), density=0.85, rough=1, feather=0.7)
    art, _ = chawan(art, W, H, 440, by, 190, rng, nx)
    art = chasen(art, W, H, 620, by, 150, rng, nx)
    art = natsume(art, W, H, 735, by, 110, rng, nx)
    art = scoop(art, W, H, 670, by - 66, 800, by - 52, rng, nx)
    preview(art, "teh-tea", "#e6dcae")
    save(art, f"{OUT}/tea.webp", max_w=760, quality=80)


def flower():
    """Chabana: one camellia with two leaves and a bud in a slender celadon vase."""
    W, H = 300, 620
    rng = random.Random(9); nx = Seq(300)
    art = blank(W, H)
    vx, by = 150, 600
    vase = shapes(W, H, [[(vx - 22, by - 300), (vx + 22, by - 300), (vx + 26, by - 260), (vx + 50, by - 120), (vx + 52, by - 40), (vx + 40, by), (vx - 40, by), (vx - 52, by - 40), (vx - 50, by - 120), (vx - 26, by - 260)]])
    art = G(art, vase, "#b9c7b2", "#93a691", seed=nx(), density=0.8, edge=0.6, bloom=0.4, rough=2, feather=0.9, gran=0.4)
    art = OV(art, gaussian_filter(strokes(W, H, [([(vx - 30, by - 230), (vx - 40, by - 60)], 6, (0.3, 0.3))]), 2), lambda q: flat(q, "#eef2e8", 0.6))
    art = ink(art, W, H, [(vx - 22, by - 300), (vx - 26, by - 260), (vx - 50, by - 120), (vx - 52, by - 40), (vx - 40, by)], 1.6, 0.5, seed=nx())
    # stem
    stem = curve([(vx + 2, by - 290), (vx - 6, by - 380), (vx + 20, by - 470), (vx + 40, by - 520)], 30)
    art = ink(art, W, H, stem, 5, 0.85, (0.0, 0.3), seed=nx())
    art = ink(art, W, H, curve([(vx - 4, by - 400), (vx - 40, by - 450), (vx - 60, by - 470)], 14), 3, 0.8, (0.0, 0.4), seed=nx())
    # leaves (deep glossy green, sumi-ish)
    for x, y, L, a in [(vx - 6, by - 380, 90, 3.6), (vx + 16, by - 455, 80, -0.5), (vx - 40, by - 450, 60, 3.9)]:
        m = shapes(W, H, [deform(petal_pts(x, y, L, L * 0.42, a, n=14), rng, 1, 0.03)])
        art = G(art, m, "#3f5a34", "#24361f", seed=nx(), density=0.85, edge=0.6, bloom=0.35, rough=2, feather=0.8)
        art = OV(art, strokes(W, H, [([(x, y), (x + math.cos(a) * L * 0.9, y + math.sin(a) * L * 0.9)], 1.2, (0.0, 0.4))]) * m, lambda q: flat(q, "#a9b98a", 0.5))
    # camellia bloom (red, cupped, golden stamens)
    cx, cy, r = vx + 44, by - 530, 58
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.55 + rng.gauss(0, 0.05)
        pts = petal_pts(cx, cy + 6, r * rng.uniform(0.95, 1.1), r * 0.85, a, n=14, cup=0.2)
        m = shapes(W, H, [deform(pts, rng, 1, 0.05)])
        art = G(art, m, "#c43d36", "#a32a27", seed=nx(), density=0.6, edge=0.65, bloom=0.4, rough=2.2, feather=0.9)
    front = shapes(W, H, [deform(arc_pts(cx, cy + 10, r * 0.75, 0.15, math.pi - 0.15, 16, 0.6) + [(cx, cy + 4)], rng, 1, 0.04)])
    art = G(art, front, "#b0302c", "#8e2220", seed=nx(), density=0.75, edge=0.6, bloom=0.2, rough=2, feather=0.8)
    stam = shapes(W, H, [deform(ellipse_pts(cx, cy - 4, r * 0.28, r * 0.2, 12), rng, 1, 0.08)])
    art = G(art, stam, "#f0cf5a", "#d9a92e", seed=nx(), density=0.9, edge=0.4, rough=1.5, feather=0.7)
    art = OV(art, circles(W, H, [(cx + rng.uniform(-1, 1) * r * 0.22, cy - 4 + rng.uniform(-1, 1) * r * 0.14, 1.6) for _ in range(30)]), lambda q: flat(q, "#a8741a", 0.8))
    bud = shapes(W, H, [deform(ellipse_pts(vx - 62, by - 478, 13, 17, 10, -0.5), rng, 1, 0.06)])
    art = G(art, bud, "#5a7040", "#3a5030", seed=nx(), density=0.85, rough=1, feather=0.7)
    art = G(art, shapes(W, H, [petal_pts(vx - 64, by - 482, 14, 10, -2.0, n=8)]), "#c43d36", seed=nx(), density=0.7, rough=1, feather=0.7)
    preview(art, "teh-flower", "#f3eee2")
    save(art, f"{OUT}/flower.webp", max_w=170, quality=82)


def steam():
    W, H = 160, 420
    rng = random.Random(4); nx = Seq(500)
    art = blank(W, H)
    for k, x in enumerate((60, 95)):
        pts = [(x + math.sin(t * 5 + k) * 18 * t, H - 10 - t * (H - 40)) for t in [i / 40 for i in range(41)]]
        m = gaussian_filter(strokes(W, H, [(pts, 16 - k * 4, (0.2, 0.6))]), 5)
        art = over(art, flat(m, "#ffffff", 0.55))
    save(art, f"{OUT}/steam.webp", max_w=80, quality=70)


def tatami():
    """Seamless tatami tile: tight rush weave running horizontally, warm straw-green, a dark heri border is CSS."""
    W, H = 256, 256
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rows = (np.sin(yy * math.pi / 2.0) * 0.5 + 0.5)
    stitch = (np.sin(xx * math.tau / 64 + (yy // 4) % 2 * math.pi) * 0.5 + 0.5) ** 6
    n = wrap_noise(W, H, 3, (0.6, 30))
    t = np.clip(0.55 * rows + 0.3 * n + 0.15 * stitch, 0, 1)
    c0, c1 = col3("#d6cc98"), col3("#b4a96e")
    rgb = c0 * (1 - t[..., None]) + c1 * t[..., None]
    save_rgb(np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/tatami.webp", quality=72)


def washi():
    W, H = 384, 384
    base = col3("#f4efe3")
    n = wrap_noise(W, H, 5, 6)
    rng = np.random.default_rng(3)
    fib = np.zeros((H, W), np.float32)
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a = rng.uniform(0, math.pi)
        L = rng.uniform(8, 30)
        for t in np.linspace(0, 1, 30):
            px, py = int((x + math.cos(a) * L * t) % W), int((y + math.sin(a) * L * t) % H)
            fib[py, px] = 1
    fib = gaussian_filter(fib, 0.5)
    fib = fib / (fib.max() + 1e-6)
    rgb = base * (0.975 + 0.035 * n[..., None]) - fib[..., None] * 0.05
    save_rgb(np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1), f"{OUT}/washi.webp", quality=70)


def stroke():
    """Matcha brush stroke (divider): dry hake stroke with streaks and a wet start."""
    W, H = 760, 90
    rng = random.Random(8); nx = Seq(700)
    art = blank(W, H)
    pts = [(60 + t * 640, 46 + math.sin(t * 3) * 6 - t * 6) for t in [i / 40 for i in range(41)]]
    m = strokes(W, H, [(pts, 30, (0.03, 0.35))])
    dry = gaussian_filter(np.random.default_rng(2).random((H, W)).astype(np.float32), (0.7, 26))
    dry = (dry - dry.min()) / (dry.max() - dry.min())
    tail = ramp_x(H, W, 360, 700)
    m = m * (1 - np.clip((tail * 0.75 - dry) * 8, 0, 1))
    art = G(art, m, MATCHA, MATCHA_D, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.5, feather=0.6, gran=0.3)
    preview(art, "teh-stroke", "#f3eee2")
    save(art, f"{OUT}/stroke.webp", max_w=360, quality=80)


def bowl():
    W, H = 260, 200
    rng = random.Random(14); nx = Seq(900)
    art = blank(W, H)
    art, _ = chawan(art, W, H, 130, 180, 180, rng, nx, glaze_a="#3a3634", glaze_b="#24201e")
    preview(art, "teh-bowl", "#f3eee2")
    save(art, f"{OUT}/bowl.webp", max_w=120, quality=82)


def whisk():
    W, H = 160, 260
    rng = random.Random(15); nx = Seq(1000)
    art = blank(W, H)
    art = chasen(art, W, H, 80, 250, 220, rng, nx)
    preview(art, "teh-whisk", "#f3eee2")
    save(art, f"{OUT}/whisk.webp", max_w=70, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
