"""Pesta BBQ — a backyard barbecue at dusk: kettle grill with sate skewers and corn, string lights, a wooden picnic
table with cold drinks and a cooler, a bean-bag toss board on the lawn. Playful gouache.
Run: python3 -I pesta-bbq.py [part ...]  parts: scene lampu asap sate jagung divider es
Assets -> public/themes/art/pesta-bbq/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o4_lib import *

OUT = outdir("pesta-bbq")
PARTS = sys.argv[1:] or ["scene", "lampu", "asap", "sate", "jagung", "divider", "es"]
CHAR, CHAR_L = "#2b2a2e", "#4a4850"
RED, RED_D = "#d9452b", "#a93220"
MUSTARD, MUSTARD_D = "#f2b632", "#d08f1c"
WOOD, WOOD_D, WOOD_L = "#b9773f", "#8a5228", "#d79a5c"
GRASS, GRASS_D, GRASS_L = "#5f9a4a", "#3f7436", "#86b85e"
CREAM = "#fff4df"
MEAT, MEAT_D = "#9a4a26", "#6a2c14"


def g(art, m, c1, c2=None, nx=None, rough=1.0, streak=0.8, **k):
    return GP(art, m, c1, c2 or c1, seed=nx(), rough=rough, streak=streak, **k)


def skewer(art, W, H, x0, y0, x1, y1, nx, n=4, s=12, glaze=True):
    """Sate: bamboo stick with chunky meat pieces, glossy kecap glaze and charred edges."""
    art = g(art, strokes(W, H, [([(x0, y0), (x1, y1)], s * 0.22, None)]), "#e2c48a", "#c9a46a", nx)
    for i in range(n):
        t = 0.32 + i * (0.6 / n)
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, s * 0.62, s * 0.52, 10, 0.4 * i), random.Random(i + int(x0)), 1, 0.12)])
        art = g(art, m, MEAT, MEAT_D, nx, rough=1.2)
        art = OV(art, edge_ring(m, 1.8), lambda q: flat(q, "#3a160a", 0.6))
        if glaze:
            hl = shapes(W, H, [petal_pts(cx - s * 0.2, cy - s * 0.25, s * 0.42, s * 0.12, -0.6, n=8)])
            art = OV(art, hl * m, lambda q: flat(q, "#f0b089", 0.7))
    return art


def corn(art, W, H, cx, cy, L, ang, nx, husk=True):
    """Grilled corn: yellow cob with kernel rows and char marks, a husk tail."""
    c, sn = math.cos(ang), math.sin(ang)
    def T(u, v):
        return (cx + u * c - v * sn, cy + u * sn + v * c)
    cob = shapes(W, H, [[T(-L / 2, -L * 0.14), T(L * 0.4, -L * 0.15), T(L / 2, 0), T(L * 0.4, L * 0.15), T(-L / 2, L * 0.14)]])
    art = g(art, cob, MUSTARD, "#f7cd55", nx)
    rows = strokes(W, H, [([T(-L / 2, v), T(L * 0.45, v * 0.9)], 1.0, None) for v in np.linspace(-L * 0.1, L * 0.1, 4)] +
                   [([T(u, -L * 0.15), T(u, L * 0.15)], 1.0, None) for u in np.linspace(-L * 0.45, L * 0.4, 9)]) * cob
    art = OV(art, rows, lambda q: flat(q, "#c98a1a", 0.6))
    ch = strokes(W, H, [([T(u, -L * 0.15), T(u + L * 0.05, L * 0.15)], L * 0.035, None) for u in (-0.3 * L, -0.05 * L, 0.2 * L)]) * cob
    art = OV(art, ch, lambda q: flat(q, "#4a2a10", 0.7))
    if husk:
        hk = shapes(W, H, [[T(-L / 2, -L * 0.12), T(-L * 0.85, -L * 0.25), T(-L * 0.7, 0), T(-L * 0.9, L * 0.2), T(-L / 2, L * 0.12)]])
        art = g(art, hk, "#a9b86a", "#7f944a", nx)
    return art


def grill(art, W, H, cx, by, s, nx, rng):
    """Kettle grill on three legs, lid propped open behind, glowing coals, sate and corn on the grate."""
    bowl_y = by - s * 0.95
    legs = strokes(W, H, [([(cx - s * 0.32, bowl_y + s * 0.15), (cx - s * 0.5, by)], s * 0.05, None), ([(cx + s * 0.32, bowl_y + s * 0.15), (cx + s * 0.5, by)], s * 0.05, None), ([(cx, bowl_y + s * 0.3), (cx + s * 0.05, by + 4)], s * 0.05, None)])
    art = g(art, legs, CHAR, nx=nx)
    wheels = circles(W, H, [(cx - s * 0.5, by - s * 0.04, s * 0.07)])
    art = g(art, wheels, "#555555", nx=nx)
    lid = shapes(W, H, [[(cx - s * 0.62, bowl_y - s * 0.02), (cx - s * 0.7, bowl_y - s * 0.55), (cx - s * 0.48, bowl_y - s * 0.92), (cx - s * 0.32, bowl_y - s * 0.7), (cx - s * 0.36, bowl_y - s * 0.08)]])
    art = g(art, lid, RED_D, "#8a2818", nx)
    art = OV(art, strokes(W, H, [([(cx - s * 0.62, bowl_y - s * 0.5), (cx - s * 0.52, bowl_y - s * 0.82)], s * 0.03, None)]), lambda q: flat(q, "#ff9a78", 0.5))
    bowl = shapes(W, H, [arc_pts(cx, bowl_y, s * 0.6, 0, math.pi, 24, 0.75)])
    art = g(art, bowl, RED, RED_D, nx)
    hi = shapes(W, H, [arc_pts(cx - s * 0.12, bowl_y + s * 0.06, s * 0.36, 2.2, 2.9, 12, 0.9) + [(cx - s * 0.2, bowl_y + s * 0.12)]])
    art = OV(art, shapes(W, H, [petal_pts(cx - s * 0.34, bowl_y + s * 0.2, s * 0.22, s * 0.05, 0.9, n=8)]), lambda q: flat(q, "#ff9a78", 0.6))
    rim = strokes(W, H, [([(cx - s * 0.62, bowl_y), (cx + s * 0.62, bowl_y)], s * 0.05, None)])
    art = g(art, rim, CHAR_L, CHAR, nx)
    # coals glow under grate
    coal = shapes(W, H, [[(cx - s * 0.5, bowl_y - 2), (cx + s * 0.5, bowl_y - 2), (cx + s * 0.4, bowl_y - s * 0.06), (cx - s * 0.4, bowl_y - s * 0.06)]])
    art = over(art, glow(coal, "#ff8a2a", s * 0.12, 0.6))
    # food
    for i, x in enumerate(np.linspace(cx - s * 0.42, cx + s * 0.08, 4)):
        art = skewer(art, W, H, x - s * 0.08, bowl_y + s * 0.0, x + s * 0.16, bowl_y - s * 0.12, nx, n=4, s=s * 0.07)
    art = corn(art, W, H, cx + s * 0.34, bowl_y - s * 0.05, s * 0.34, -0.2, nx, husk=False)
    art = OV(art, strokes(W, H, [([(cx + s * 0.6, bowl_y + s * 0.05), (cx + s * 0.85, bowl_y - s * 0.08)], s * 0.035, None)]), lambda q: flat(q, CHAR, 1))
    return art


def table(art, W, H, x, y, w, nx, rng):
    """Wooden picnic table with benches; drinks on top."""
    top = shapes(W, H, [rect(x, y, x + w, y + w * 0.06)], smooth=False)
    art = g(art, top, WOOD_L, WOOD, nx, streak=1.4)
    art = OV(art, strokes(W, H, [([(x + w * t, y + 1), (x + w * t, y + w * 0.06)], 1.0, None) for t in (0.33, 0.66)]), lambda q: flat(q, WOOD_D, 0.6))
    art = OV(art, shapes(W, H, [rect(x, y + w * 0.05, x + w, y + w * 0.075)], smooth=False), lambda q: flat(q, WOOD_D, 0.9))
    legs = strokes(W, H, [([(x + w * 0.15, y + w * 0.07), (x + w * 0.05, y + w * 0.36)], w * 0.03, None), ([(x + w * 0.15, y + w * 0.07), (x + w * 0.26, y + w * 0.36)], w * 0.03, None),
                          ([(x + w * 0.85, y + w * 0.07), (x + w * 0.74, y + w * 0.36)], w * 0.03, None), ([(x + w * 0.85, y + w * 0.07), (x + w * 0.95, y + w * 0.36)], w * 0.03, None)])
    art = g(art, legs, WOOD, WOOD_D, nx)
    bench = shapes(W, H, [rect(x - w * 0.04, y + w * 0.2, x + w * 1.04, y + w * 0.24)], smooth=False)
    art = g(art, bench, WOOD_L, WOOD, nx, streak=1.4)
    art = OV(art, shapes(W, H, [rect(x - w * 0.04, y + w * 0.235, x + w * 1.04, y + w * 0.25)], smooth=False), lambda q: flat(q, WOOD_D, 0.8))
    # drinks: es jeruk glasses, a jug of es teh, bottles
    for i, (gx, col) in enumerate([(0.12, "#f39a2e"), (0.24, "#c8622a"), (0.62, "#f39a2e")]):
        gl = shapes(W, H, [[(x + w * gx, y - w * 0.1), (x + w * (gx + 0.06), y - w * 0.1), (x + w * (gx + 0.055), y), (x + w * (gx + 0.005), y)]], smooth=False)
        art = over(art, flat(gl, "#e9f4f2", 0.55))
        liq = shapes(W, H, [[(x + w * (gx + 0.004), y - w * 0.075), (x + w * (gx + 0.056), y - w * 0.075), (x + w * (gx + 0.052), y - 2), (x + w * (gx + 0.008), y - 2)]], smooth=False)
        art = g(art, liq, col, mix(col, "#ffffff", 0.2), nx, rough=0.5)
        art = OV(art, strokes(W, H, [([(x + w * (gx + 0.04), y - w * 0.14), (x + w * (gx + 0.03), y - w * 0.05)], 2.2, None)]), lambda q: flat(q, RED, 1))
        art = OV(art, strokes(W, H, [([(x + w * (gx + 0.012), y - w * 0.09), (x + w * (gx + 0.014), y - w * 0.02)], 1.6, None)]), lambda q: flat(q, "#ffffff", 0.7))
    jug = shapes(W, H, [[(x + w * 0.36, y - w * 0.2), (x + w * 0.48, y - w * 0.2), (x + w * 0.5, y), (x + w * 0.34, y)]])
    art = over(art, flat(jug, "#e9f4f2", 0.5))
    art = g(art, shapes(W, H, [[(x + w * 0.355, y - w * 0.14), (x + w * 0.485, y - w * 0.14), (x + w * 0.495, y - 2), (x + w * 0.345, y - 2)]]), "#9a5a2a", "#b5703a", nx, rough=0.5)
    art = OV(art, strokes(W, H, [(arc_pts(x + w * 0.5, y - w * 0.11, w * 0.045, -1.3, 1.3, 12), 3.0, None)]), lambda q: flat(q, "#cfe2df", 0.8))
    ice = circles(W, H, [(x + w * (0.38 + 0.03 * k), y - w * (0.12 + 0.01 * (k % 2)), w * 0.012) for k in range(3)])
    art = over(art, flat(ice, "#ffffff", 0.75))
    # plate of sate
    plate = ellipses(W, H, [(x + w * 0.82, y - 3, w * 0.12, w * 0.025, 0)])
    art = g(art, plate, CREAM, "#f1e3c6", nx)
    for k in range(3):
        art = skewer(art, W, H, x + w * 0.72, y - 4 - k * 4, x + w * 0.93, y - 10 - k * 4, nx, n=3, s=w * 0.03)
    return art


def cooler(art, W, H, x, by, w, nx):
    body = shapes(W, H, [rect(x, by - w * 0.6, x + w, by)], smooth=False)
    art = g(art, body, "#3d8fb8", "#2f78a0", nx)
    lid = shapes(W, H, [rect(x - w * 0.04, by - w * 0.72, x + w * 1.04, by - w * 0.58)], smooth=False)
    art = g(art, lid, CREAM, "#efe1c2", nx)
    art = OV(art, strokes(W, H, [([(x + w * 0.3, by - w * 0.72), (x + w * 0.35, by - w * 0.84), (x + w * 0.65, by - w * 0.84), (x + w * 0.7, by - w * 0.72)], w * 0.04, None)]), lambda q: flat(q, CHAR, 1))
    art = OV(art, shapes(W, H, [rect(x + w * 0.1, by - w * 0.45, x + w * 0.9, by - w * 0.32)], smooth=False), lambda q: flat(q, "#ffffff", 0.85))
    # bottles leaning on it
    for i, (bx, col) in enumerate([(x + w * 1.08, "#3f7a3a"), (x + w * 1.22, "#c8402a")]):
        b = shapes(W, H, [[(bx, by), (bx + w * 0.1, by), (bx + w * 0.1, by - w * 0.4), (bx + w * 0.065, by - w * 0.48), (bx + w * 0.065, by - w * 0.6), (bx + w * 0.035, by - w * 0.6), (bx + w * 0.035, by - w * 0.48), (bx, by - w * 0.4)]], smooth=False)
        art = g(art, b, col, mix(col, "#000000", 0.2), nx, rough=0.6)
        art = OV(art, shapes(W, H, [rect(bx, by - w * 0.3, bx + w * 0.1, by - w * 0.17)], smooth=False), lambda q: flat(q, CREAM, 0.95))
        art = OV(art, strokes(W, H, [([(bx + w * 0.025, by - w * 0.38), (bx + w * 0.025, by - w * 0.05)], 1.6, None)]), lambda q: flat(q, "#ffffff", 0.5))
    return art


def toss(art, W, H, x, by, w, nx):
    """Bean-bag toss board (lawn game) with a hole and two bean bags."""
    bd = shapes(W, H, [[(x, by), (x + w, by), (x + w * 0.82, by - w * 0.55), (x + w * 0.18, by - w * 0.55)]], smooth=False)
    art = g(art, bd, MUSTARD, MUSTARD_D, nx)
    art = OV(art, strokes(W, H, [([(x + w * 0.12, by - w * 0.36), (x + w * 0.88, by - w * 0.36)], w * 0.04, None)]) * bd, lambda q: flat(q, RED, 0.9))
    hole = ellipses(W, H, [(x + w * 0.5, by - w * 0.42, w * 0.1, w * 0.05, 0)])
    art = g(art, hole, CHAR, nx=nx)
    bags = shapes(W, H, [deform(ellipse_pts(x + w * 1.15, by - 4, w * 0.09, w * 0.05, 8, 0.2), random.Random(2), 1, 0.1), deform(ellipse_pts(x + w * 0.45, by - w * 0.2, w * 0.08, w * 0.045, 8, -0.3), random.Random(3), 1, 0.1)])
    art = g(art, bags, RED, RED_D, nx)
    return art


def scene():
    """Transparent foreground for the cover bottom: lawn, fence, a frangipani tree, grill, table, cooler, toss."""
    W, H = 760, 560
    rng = random.Random(8); nx = Seq(100)
    art = blank(W, H)
    # fence
    pick = []
    for x in range(-10, W + 20, 34):
        pick.append(rect(x, 170, x + 26, 360))
    fm = shapes(W, H, pick + [rect(-10, 210, W + 10, 226), rect(-10, 300, W + 10, 316)], smooth=False)
    art = g(art, fm, "#f3e6cc", "#e3d0aa", nx, streak=1.2)
    tips = shapes(W, H, [[(x, 170), (x + 13, 156), (x + 26, 170)] for x in range(-10, W + 20, 34)], smooth=False)
    art = g(art, tips, "#f3e6cc", "#e3d0aa", nx)
    art = OV(art, strokes(W, H, [([(x + 26, 170), (x + 26, 360)], 2.0, None) for x in range(-10, W + 20, 34)]), lambda q: flat(q, "#b9a27a", 0.6))
    # frangipani tree at the right behind fence
    trunk = strokes(W, H, [(curve([(690, 380), (660, 260), (610, 170)], 16), 16, (0.0, 0.5)), (curve([(668, 280), (720, 200), (760, 150)], 12), 11, (0.0, 0.5))])
    art = g(art, trunk, "#8f7a66", "#6e5a48", nx)
    leaves = []
    for (lx, ly) in [(600, 150), (640, 120), (700, 140), (750, 120), (580, 180), (730, 170)]:
        for k in range(5):
            a = k * math.tau / 5 + rng.uniform(-0.3, 0.3)
            leaves.append(petal_pts(lx, ly, rng.uniform(38, 52), 13, a, n=10))
    art = g(art, shapes(W, H, leaves), GRASS, GRASS_D, nx)
    fl = []
    for (lx, ly) in [(610, 140), (655, 112), (712, 132), (745, 110), (590, 175)]:
        for k in range(5):
            fl.append(petal_pts(lx, ly, 11, 6, k * math.tau / 5 + 0.4, n=8))
    fm2 = shapes(W, H, fl)
    art = g(art, fm2, "#ffffff", "#fff0d0", nx, rough=0.6)
    art = OV(art, circles(W, H, [(x, y, 3.5) for (x, y) in [(610, 140), (655, 112), (712, 132), (745, 110), (590, 175)]]), lambda q: flat(q, MUSTARD, 1))
    # lawn
    lawn = shapes(W, H, [[(-20, 340), (200, 322), (420, 332), (600, 318), (W + 20, 330), (W + 20, H + 10), (-20, H + 10)]])
    art = g(art, lawn, GRASS_L, GRASS, nx, rough=3, streak=1.0)
    blades = strokes(W, H, [([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(5, 11))], 1.4, (0.0, 0.8)) for x, y in [(rng.uniform(0, W), rng.uniform(345, H)) for _ in range(260)]])
    art = OV(art, blades, lambda q: flat(q, GRASS_D, 0.55))
    sh = ellipses(W, H, [(150, 520, 120, 16, 0), (470, 512, 170, 18, 0), (650, 520, 70, 10, 0)])
    art = OV(art, gaussian_filter(sh, 6), lambda q: flat(q, "#2e5a28", 0.45))
    clear()
    art = toss(art, W, H, 590, 500, 104, nx)
    art = table(art, W, H, 360, 392, 290, nx, rng)
    art = grill(art, W, H, 160, 520, 190, nx, rng)
    art = cooler(art, W, H, 290, 548, 78, nx)
    preview(art, "bbq-scene", bg="#2f3a5a")
    save(art, f"{OUT}/scene.webp", max_w=760, quality=80)


def lampu():
    """String lights: a drooping cable with round warm bulbs, each glowing; transparent."""
    W, H = 800, 170
    rng = random.Random(5); nx = Seq(600)
    art = blank(W, H)
    pts = []
    for x in np.linspace(-10, W + 10, 80):
        t = (x + 10) / (W + 20)
        y = 22 + 70 * math.sin(math.pi * ((t * 2) % 1)) ** 1.2 * (0.9 if t < 0.5 else 1.0)
        pts.append((x, y))
    art = g(art, strokes(W, H, [(pts, 2.6, None)]), CHAR, nx=nx)
    bulbs = []
    for i in range(1, 79, 5):
        x, y = pts[i]
        bulbs.append((x, y + 14))
    sock = strokes(W, H, [([(x, y - 12), (x, y - 4)], 6.5, None) for x, y in bulbs])
    art = g(art, sock, CHAR_L, CHAR, nx)
    bm = circles(W, H, [(x, y + 4, 9) for x, y in bulbs])
    art = over(art, glow(bm, "#ffd27a", 12, 0.55))
    cols = ["#ffe3a0", "#ffd27a", "#fff0c8"]
    art = g(art, bm, "#ffe3a0", "#ffc860", nx, rough=0.5)
    art = OV(art, circles(W, H, [(x - 3, y + 1, 3) for x, y in bulbs]), lambda q: flat(q, "#ffffff", 0.85))
    preview(art, "bbq-lampu", bg="#2f3a5a")
    save(art, f"{OUT}/lampu.webp", max_w=800, quality=82)


def asap():
    """A smoke wisp from the grill (animated rising)."""
    W, H = 200, 360
    nx = Seq(900)
    art = blank(W, H)
    path = [(100 + 26 * math.sin(t * 5.5) * t, 350 - t * 330) for t in np.linspace(0, 1, 40)]
    m = strokes(W, H, [(path, 26, (0.05, 0.6))])
    m = gaussian_filter(m, 6) * np.clip(fbm(W, H, 4, 30, 3) * 1.6 - 0.2, 0, 1)
    art = over(art, flat(np.clip(m * 1.3, 0, 1), "#f1ece4", 0.7))
    preview(art, "bbq-asap", bg="#2f3a5a")
    save(art, f"{OUT}/asap.webp", max_w=120, quality=80)


def sate():
    W, H = 260, 200
    nx = Seq(1200)
    art = blank(W, H)
    for k in range(3):
        art = skewer(art, W, H, 20 + k * 12, 170 - k * 18, 230 + k * 6, 60 - k * 22, nx, n=4, s=26)
    preview(art, "bbq-sate")
    save(art, f"{OUT}/sate.webp", max_w=150, quality=84)


def jagung():
    W, H = 240, 160
    nx = Seq(1500)
    art = blank(W, H)
    art = corn(art, W, H, 140, 80, 150, -0.35, nx)
    preview(art, "bbq-jagung")
    save(art, f"{OUT}/jagung.webp", max_w=130, quality=84)


def divider():
    """A long skewer with meat, corn rounds and peppers: the section divider."""
    W, H = 720, 80
    nx = Seq(1800)
    art = blank(W, H)
    art = g(art, strokes(W, H, [([(20, 40), (700, 40)], 4, None)]), "#e2c48a", "#c9a46a", nx)
    xs = np.linspace(150, 570, 9)
    for i, x in enumerate(xs):
        if i % 3 == 1:
            m = shapes(W, H, [rect(x - 9, 22, x + 9, 58)])
            art = g(art, m, MUSTARD, "#f7cd55", nx)
            art = OV(art, strokes(W, H, [([(x - 9, y), (x + 9, y)], 1.0, None) for y in (30, 38, 46, 54)]) * m, lambda q: flat(q, "#c98a1a", 0.6))
        elif i % 3 == 2:
            m = shapes(W, H, [deform(ellipse_pts(x, 40, 14, 16, 10), random.Random(i), 1, 0.15)])
            art = g(art, m, "#4f9a3a" if i % 2 else RED, None, nx)
        else:
            m = shapes(W, H, [deform(ellipse_pts(x, 40, 17, 15, 10, 0.3), random.Random(i + 9), 1, 0.12)])
            art = g(art, m, MEAT, MEAT_D, nx)
            art = OV(art, shapes(W, H, [petal_pts(x - 4, 33, 9, 3, -0.5, n=8)]) * m, lambda q: flat(q, "#f0b089", 0.7))
    preview(art, "bbq-divider")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)


def es():
    """Glass of es jeruk with straw and ice (sent / emblem)."""
    W, H = 200, 260
    nx = Seq(2100)
    art = blank(W, H)
    gl = shapes(W, H, [[(40, 40), (160, 40), (150, 240), (50, 240)]], smooth=False)
    art = over(art, flat(gl, "#e9f4f2", 0.6))
    liq = shapes(W, H, [[(44, 90), (156, 90), (148, 234), (52, 234)]], smooth=False)
    art = g(art, liq, "#f39a2e", "#f7b24a", nx, rough=0.6)
    ice = shapes(W, H, [rect(60, 100, 95, 132), rect(100, 108, 136, 140), rect(78, 140, 112, 172)], smooth=False)
    art = over(art, flat(ice, "#fff6e0", 0.55))
    sl = circles(W, H, [(150, 48, 34)])
    art = g(art, sl, "#f7c04a", "#f39a2e", nx, rough=0.6)
    art = OV(art, strokes(W, H, [([(150, 48), (150 + 30 * math.cos(a), 48 + 30 * math.sin(a))], 1.6, None) for a in np.linspace(0, math.tau, 9)]) * sl, lambda q: flat(q, "#fff2c8", 0.8))
    art = OV(art, strokes(W, H, [([(118, 10), (102, 200)], 9, None)]), lambda q: flat(q, RED, 1))
    art = OV(art, strokes(W, H, [([(58, 60), (64, 220)], 5, None)]), lambda q: flat(q, "#ffffff", 0.5))
    preview(art, "bbq-es")
    save(art, f"{OUT}/es.webp", max_w=120, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
