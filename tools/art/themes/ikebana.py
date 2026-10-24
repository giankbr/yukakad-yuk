"""Ikebana — a moribana arrangement: a sumi-brushed flowering-quince branch (shin), a leaning leafy branch (soe), two
irises with sword leaves (hikae) on a kenzan in a shallow indigo-glazed suiban; washi paper. Watercolour + sumi ink.
Run: python3 -I ikebana.py [part ...]  parts: arrangement iris sprig washi"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q4_lib import *

OUT = outdir("ikebana")
PARTS = sys.argv[1:] or ["arrangement", "iris", "sprig", "washi"]
SUMI = "#2b2622"
VIO, VIO_D, VIO_L = "#5a4a96", "#2f2463", "#9d8fd0"
GREEN, GREEN_D = "#6f8f5a", "#344f34"
BLOS, BLOS_D = "#f4cfc4", "#d0766e"
WASHI = "#f1ebde"


def branch(art, pts, width, seed, col=SUMI):
    return sumi(art, curve(pts, 60), width, col, seed=seed, dry=0.45)


def blossom(art, W, H, x, y, r, rng, nx, open_=1.0):
    """Five-petal quince/plum blossom: pale wash petals, darker rim, ink-dot stamens."""
    for k in range(5):
        a = rng.uniform(0, 1) + k * math.tau / 5
        pm = shape_mask(W, H, deform(ellipse_pts(x + math.cos(a) * r * 0.55 * open_, y + math.sin(a) * r * 0.55 * open_, r * 0.52, r * 0.44, 9, a), rng, 1, 0.1))
        art = G(art, pm, BLOS, BLOS_D, seed=nx(), density=0.55, edge=0.7, bloom=0.25, rough=2, feather=0.9)
    c = circles(W, H, [(x, y, r * 0.22)])
    art = G(art, c, "#c9a24a", "#8a5a2a", seed=nx(), density=0.75, edge=0.4, bloom=0, rough=1)
    dots = circles(W, H, [(x + math.cos(a) * r * 0.33, y + math.sin(a) * r * 0.33, 1.4) for a in [k * math.tau / 9 + rng.random() for k in range(9)]])
    return T(art, dots, "#4a2a1a", 0.85)


def bud(art, W, H, x, y, r, ang, rng, nx):
    m = shape_mask(W, H, deform(petal_pts(x, y, r * 1.5, r * 0.8, ang, n=10), rng, 1, 0.08))
    return G(art, m, "#e3a9a0", "#b86a68", seed=nx(), density=0.7, edge=0.6, bloom=0.1, rough=1.5)


def sword_leaf(art, W, H, base, tip, width, rng, nx, bend=0.0):
    (x0, y0), (x1, y1) = base, tip
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    pts = curve([(x0, y0), (mx, my), (x1, y1)], 30)
    poly = jw.blade(W, H, pts, width)
    m = shape_mask(W, H, poly)
    art = G(art, m, GREEN, GREEN_D, seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=2.5)
    mid = stroke_mask(W, H, pts[2:-4], 1.2)
    return G(art, mid, GREEN_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.6, feather=0.5)


def iris(art, W, H, x, y, s, rng, nx, tilt=0.0):
    """Japanese iris (hanashobu-like) seen from the side: 3 drooping falls with a yellow signal, 3 upright standards."""
    # standards (behind, upright)
    for a in (-1.9, -1.57, -1.2):
        m = shape_mask(W, H, deform(petal_pts(x, y - s * 0.1, s * 0.95, s * 0.34, a + tilt, n=12, cup=0.1), rng, 1, 0.08))
        art = G(art, m, VIO_L, VIO, seed=nx(), density=0.6, edge=0.7, bloom=0.3, rough=2)
    # falls (front, drooping outward)
    for a, L in ((2.75, 1.25), (0.42, 1.2), (1.57, 0.9)):
        m = shape_mask(W, H, deform(petal_pts(x, y, s * L, s * 0.52, a + tilt * 0.5, n=14, cup=-0.1), rng, 1, 0.08))
        art = G(art, m, VIO, VIO_D, seed=nx(), density=0.78, edge=0.75, bloom=0.35, rough=2.5)
        sx, sy = x + math.cos(a + tilt * 0.5) * s * 0.35, y + math.sin(a + tilt * 0.5) * s * 0.35
        sig = shape_mask(W, H, petal_pts(x + math.cos(a) * s * 0.1, y + math.sin(a) * s * 0.1, s * 0.42, s * 0.09, a + tilt * 0.5, n=8))
        art = G(art, sig, "#e8c24a", "#c0902a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
        veins = strokes(W, H, [([(sx, sy), (sx + math.cos(a + d) * s * 0.5, sy + math.sin(a + d) * s * 0.5)], 0.9, None) for d in (-0.25, 0, 0.25)])
        art = G(art, veins, VIO_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4)
    return art


if "arrangement" in PARTS:
    W, H = 760, 1000
    nx = Seq(40100)
    rng = random.Random(7)
    art = blank(W, H)
    kx, ky = 336, 842  # kenzan centre
    # ---- shin: tall quince branch rising up-left with a crooked elbow
    shin = [(kx, ky - 6), (318, 700), (262, 560), (276, 430), (220, 300), (176, 168), (190, 70)]
    art = branch(art, shin, 15, 11)
    art = branch(art, [(262, 560), (200, 520), (150, 470)], 7, 12)
    art = branch(art, [(276, 430), (330, 360), (356, 300)], 6, 13)
    art = branch(art, [(220, 300), (160, 268)], 5, 14)
    for x, y, r in [(150, 466, 30), (186, 158, 26), (356, 296, 28), (240, 352, 22), (204, 236, 18)]:
        art = blossom(art, W, H, x, y, r, rng, nx)
    for x, y, a in [(190, 70, -1.4), (160, 266, 3.2), (130, 452, 3.6), (370, 280, -0.9), (282, 470, 0.2)]:
        art = bud(art, W, H, x, y, 9, a, rng, nx)
    clear()
    # ---- soe: a branch leaning right with a few leaves
    soe = [(kx + 8, ky - 6), (400, 760), (500, 690), (590, 620), (660, 590)]
    art = branch(art, soe, 9, 21, col="#3a3128")
    for (x, y, a, L) in [(470, 708, -1.1, 48), (540, 660, -0.7, 52), (610, 612, -1.4, 44), (590, 628, 0.5, 40), (660, 590, -0.3, 38), (430, 740, 0.7, 36)]:
        m = shape_mask(W, H, petal_pts(x, y, L * 1.25, L * 0.26, a, n=16))
        art = G(art, m, "#7f9a5a", "#4a6a3a", seed=nx(), density=0.72, edge=0.6, bloom=0.3, rough=2)
        rib = stroke_mask(W, H, [(x, y), (x + math.cos(a) * L * 1.0, y + math.sin(a) * L * 1.0)], 1.1)
        art = G(art, rib, "#3a5a32", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4)
    clear()
    # ---- hikae: irises and sword leaves, low and forward
    for base, tip, wd, bend in [((340, 846), (300, 560), 14, -20), ((346, 846), (380, 600), 12, 16), ((352, 846), (420, 700), 11, 20),
                                ((330, 846), (262, 690), 11, -16), ((344, 846), (350, 520), 10, 4)]:
        art = sword_leaf(art, W, H, base, tip, wd, rng, nx, bend)
    stems = strokes(W, H, [(curve([(338, 846), (330, 720), (312, 640)], 20), 5, None), (curve([(346, 846), (372, 760), (408, 720)], 20), 4.5, None)])
    art = G(art, stems, GREEN, GREEN_D, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1)
    art = iris(art, W, H, 312, 626, 62, rng, nx, tilt=-0.15)
    art = iris(art, W, H, 410, 708, 48, rng, nx, tilt=0.2)
    clear()
    # ---- suiban: shallow dish, glazed indigo with a celadon run at the rim; water and the kenzan
    dish = shapes(W, H, [[(150, 850), (610, 850), (596, 900), (560, 920), (200, 920), (164, 900)]])
    art = shadow(art, dish, "#3a3020", blur=12, strength=0.22, dx=0, dy=16)
    art = G(art, dish, "#34505e", "#1f3440", seed=nx(), density=0.92, edge=0.55, bloom=0.4, rough=2, feather=1.2)
    rim = ellipses(W, H, [(380, 850, 232, 22, 0)])
    water = ellipses(W, H, [(380, 852, 214, 16, 0)])
    art = G(art, np.clip(rim - water, 0, 1), "#8fb0aa", "#5f8a8a", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1)
    art = G(art, water, "#9fb6b2", "#6f8f90", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=1.5)
    drips = strokes(W, H, [([(x, 862), (x + rng.uniform(-2, 2), 862 + rng.uniform(10, 30))], rng.uniform(3, 6), (0.0, 0.8)) for x in range(176, 596, 26)])
    art = G(art, drips * dish, "#7fa3a0", seed=nx(), density=0.6, edge=0.3, bloom=0.1, rough=1)
    ken = ellipses(W, H, [(kx + 4, 850, 34, 7, 0)])
    art = G(art, ken, "#2a2622", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.8)
    pins = lines(W, H, [((kx - 26 + k * 6, 847), (kx - 26 + k * 6, 841)) for k in range(10)], 1.1)
    art = T(art, pins, "#4a4440", 0.8)
    # re-draw the stem bases over the kenzan so they sit in it
    art = branch(art, [(kx, ky + 4), (kx - 2, ky - 18)], 13, 31)
    art = branch(art, [(kx + 8, ky + 4), (kx + 14, ky - 14)], 8, 32, col="#3a3128")
    clear()
    preview(art, "ik-arrangement", tone=WASHI)
    save(art, f"{OUT}/arrangement.webp", max_w=520, quality=80)

if "iris" in PARTS:
    W, H = 300, 620
    nx = Seq(40500); rng = random.Random(9)
    art = blank(W, H)
    for base, tip, wd, bend in [((150, 610), (110, 300), 11, -14), ((156, 610), (210, 360), 10, 14), ((150, 610), (180, 420), 8, 8)]:
        art = sword_leaf(art, W, H, base, tip, wd, rng, nx, bend)
    art = G(art, strokes(W, H, [(curve([(152, 610), (146, 400), (140, 180)], 20), 5, None)]), GREEN, GREEN_D, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1)
    art = iris(art, W, H, 140, 160, 64, rng, nx)
    art = bud(art, W, H, 196, 300, 12, -1.2, rng, nx) if False else art
    preview(art, "ik-iris", tone=WASHI)
    save(art, f"{OUT}/iris.webp", max_w=180, quality=82)

if "sprig" in PARTS:
    W, H = 720, 140
    nx = Seq(40700); rng = random.Random(3)
    art = blank(W, H)
    art = branch(art, [(30, 96), (200, 84), (380, 70), (560, 62), (690, 38)], 7, 41)
    art = branch(art, [(380, 70), (430, 104), (470, 112)], 4, 42)
    for x, y, r in [(470, 108, 17), (300, 70, 15)]:
        art = blossom(art, W, H, x, y, r, rng, nx)
    for x, y, a in [(690, 36, -0.4), (560, 52, -1.6), (190, 74, -1.2)]:
        art = bud(art, W, H, x, y, 7, a, rng, nx)
    preview(art, "ik-sprig", tone=WASHI)
    save(art, f"{OUT}/sprig.webp", max_w=360, quality=84)

if "washi" in PARTS:
    # washi tile: soft cream with long kozo fibres and a few pressed flecks (seamless)
    S = 512
    base = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(WASHI), np.float32)
    mot = wrap_noise(S, S, 5, 40)
    base *= (0.975 + 0.05 * mot)[..., None]
    cv = Canvas(S, S)
    rr = random.Random(11)
    for _ in range(160):
        x, y = rr.uniform(0, S), rr.uniform(0, S); L = rr.uniform(20, 90); a = rr.uniform(0, math.pi)
        pts = [(x + math.cos(a) * t + math.sin(t * 0.08) * 4, y + math.sin(a) * t) for t in np.linspace(0, L, 12)]
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=rr.uniform(0.5, 1.2), Style=skia.Paint.kStroke_Style)
        path = skia.Path(); path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        for dx in (-S, 0, S):
            for dy in (-S, 0, S):
                cv.c.save(); cv.c.translate(dx, dy); cv.c.drawPath(path, p); cv.c.restore()
    fib = cv.array()[..., 3]
    base = base * (1 - fib[..., None] * 0.05) + fib[..., None] * 0.03
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8), "RGB")
    img.save(f"{OUT}/washi.webp", "WEBP", quality=70, method=6)
    print("washi", os.path.getsize(f"{OUT}/washi.webp") // 1024, "KB")
