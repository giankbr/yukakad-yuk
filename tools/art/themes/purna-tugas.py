"""Purna Tugas — warm navy & cream retirement thanksgiving: open memory book with navy cloth cover, pressed flowers held
by washi tape, illegible handwriting, ochre ribbon bookmark; navy-and-gold fountain pen; pressed cosmos sprig; small
pressed daisy. Run: python3 -I purna-tugas.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b6_lib import *

OUT = outdir("purna-tugas")
PARTS = sys.argv[1:] or ["journal", "pen", "pressed", "bloom"]
NAVY, NAVY_D, NAVY_L = "#22345a", "#121d36", "#3b5384"
CREAM, CREAM_D = "#f6eedd", "#e2d3b5"
OCHRE = "#c4923f"
ROSE, ROSE_D = "#d49c97", "#a8615f"
SAGE, SAGE_D = "#98a98d", "#5f7560"


def daisy(art, W, H, x, y, r, rng, nx, col="#f7f0e2", eye="#d8a94a", n=12, flat=0.0):
    polys = [deform(petal_pts(x, y, r, r * 0.22, k * math.tau / n + rng.uniform(-.08, .08), n=10), rng, 1, 0.06) for k in range(n)]
    m = shapes(W, H, polys)
    art = G(art, m, mix(col, "#b9a98a", 0.25), seed=nx(), density=0.35, edge=0.6, bloom=0.2, rough=1)
    art = GP(art, m, col, mix(col, "#e8dcc4", .6), seed=nx(), rough=0.8, pad=6, density=0.8)
    return G(art, circles(W, H, [(x, y, r * 0.26)]), eye, mix(eye, "#8a5a20", .4), seed=nx(), density=0.85, edge=0.5, rough=0.8)


def cosmos(art, W, H, x, y, r, rng, nx):
    polys = [deform(ellipse_pts(x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55, r * 0.5, r * 0.24, 12, a), rng, 1, 0.05) for a in [k * math.tau / 8 + rng.uniform(-.1, .1) for k in range(8)]]
    m = shapes(W, H, polys)
    art = G(art, m, ROSE, ROSE_D, seed=nx(), density=0.6, edge=0.6, bloom=0.4, rough=2)
    art = G(art, m * fbm(W, H, nx(), 20, 2), ROSE_D, seed=nx(), density=0.25, edge=0.2, bloom=0, rough=1)
    return G(art, circles(W, H, [(x, y, r * 0.2)]), "#c7a04c", "#8a6a2a", seed=nx(), density=0.85, edge=0.5, rough=0.8)


def fern(art, W, H, pts, size, rng, nx, col=SAGE, col2=SAGE_D):
    items = [(pts, 2.2, (0.02, 0.4))]
    polys = []
    for i in range(2, len(pts) - 1, 2):
        a, b = pts[i - 1], pts[i + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        t = i / len(pts)
        for side in (-1, 1):
            polys.append(petal_pts(pts[i][0], pts[i][1], size * (1.1 - t * 0.8), size * 0.24, ang + side * 1.05, n=8))
    art = G(art, shapes(W, H, polys), col, col2, seed=nx(), density=0.55, edge=0.5, bloom=0.3, rough=1.5)
    return G(art, strokes(W, H, items), col2, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6)


def scribble(W, H, x0, x1, y, rng, size=7):
    """One line of illegible running handwriting as a polyline."""
    pts = []; x = x0
    while x < x1:
        k = rng.uniform(0.6, 1.3)
        pts.append((x, y + rng.uniform(-size, size * 0.4) * k))
        x += rng.uniform(2.2, 4.2)
        if rng.random() < 0.035:
            x += rng.uniform(8, 14)
            pts.append(None)
    lines, cur = [], []
    for p in pts:
        if p is None:
            if len(cur) > 2:
                lines.append(curve(cur, len(cur) * 3))
            cur = []
        else:
            cur.append(p)
    if len(cur) > 2:
        lines.append(curve(cur, len(cur) * 3))
    return lines


if "journal" in PARTS:
    W, H = 780, 560
    nx = Seq(50100); rng = random.Random(3)
    art = blank(W, H)
    sh = shapes(W, H, [rect(40, 50, 750, 530)], smooth=False)
    art = over(art, soft_shadow(sh, "#0b1222", blur=14, strength=0.45, dx=8, dy=12))
    cover = shapes(W, H, [deform([(30, 40), (390, 54), (750, 40), (754, 520), (390, 532), (26, 520)], rng, 1, 0.004)], smooth=False)
    art = GP(art, cover, NAVY, NAVY_D, seed=nx(), rough=1.0, streak=1.2, pad=10)
    cloth = jw.hatch(W, H, 0.0, 3.0, 0.35, 5, wob=0.6) * cover
    art = G(art, cloth, NAVY_L, seed=nx(), density=0.18, edge=0, bloom=0, rough=0.5, feather=0.4)
    # pages (left and right), slightly curved toward the gutter
    lp = shapes(W, H, [[(50, 58), (200, 60), (330, 64), (390, 74), (390, 520), (330, 514), (50, 510)]], smooth=False)
    rp = lp[:, ::-1].copy()
    pages = np.maximum(lp, rp)
    art = GP(art, pages, CREAM, CREAM_D, seed=nx(), rough=0.8, streak=0.12, pad=8)
    art = G(art, pages * fbm(W, H, nx(), 90, 3), "#d9c49c", seed=nx(), density=0.22, edge=0.1, bloom=0.5, rough=2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gut = np.exp(-((xx - 390) / 26) ** 2) * pages
    art = G(art, gut, "#a99067", seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    stack = strokes(W, H, [([(52, 512 + k * 3), (388, 518 + k * 3)], 0.9, None) for k in range(3)] + [([(392, 518 + k * 3), (728, 512 + k * 3)], 0.9, None) for k in range(3)])
    art = G(art, stack, "#b8a27a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    # left page: pressed cosmos + fern + daisy held with washi tape
    art = fern(art, W, H, curve([(120, 440), (150, 350), (200, 260), (230, 170)], 26), 30, rng, nx)
    stem = strokes(W, H, [(curve([(250, 450), (240, 350), (270, 250), (262, 170)], 30), 2.6, (0.02, 0.3)), (curve([(244, 330), (300, 290), (322, 260)], 14), 2, (0.0, 0.4))])
    art = G(art, stem, SAGE_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6)
    art = cosmos(art, W, H, 262, 162, 42, rng, nx)
    art = cosmos(art, W, H, 324, 256, 30, rng, nx)
    art = daisy(art, W, H, 132, 214, 26, rng, nx)
    for (x, y, L, a) in [(240, 380, 40, 2.6), (258, 300, 34, -0.4), (120, 300, 30, -2.4)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx, c=(SAGE, SAGE_D))
    for (x, y, a, c) in [(250, 430, -0.25, "#d9a6a0"), (140, 160, 0.4, "#bccbb4"), (330, 300, 0.7, "#e7cf98")]:
        tp = shapes(W, H, [petal_pts(x - 40 * math.cos(a), y - 40 * math.sin(a), 80, 14, a, n=4)], smooth=False)
        tp = shapes(W, H, [[(x - 40 * math.cos(a) - 12 * math.sin(a), y - 40 * math.sin(a) + 12 * math.cos(a)), (x + 40 * math.cos(a) - 12 * math.sin(a), y + 40 * math.sin(a) + 12 * math.cos(a)),
                            (x + 40 * math.cos(a) + 12 * math.sin(a), y + 40 * math.sin(a) - 12 * math.cos(a)), (x - 40 * math.cos(a) + 12 * math.sin(a), y - 40 * math.sin(a) - 12 * math.cos(a))]], smooth=False)
        art = OV(art, tp, lambda m, c=c: tint(m, c, 0.72))
    # right page: handwriting lines, a small pasted photo card, a pressed leaf
    lines = []
    for i, y in enumerate(range(104, 480, 24)):
        x1 = 704 if i not in (3, 9, 14) else rng.uniform(520, 620)
        x0 = 438 if not (5 <= i <= 9) else 604
        lines += [(ln, 1.5, None) for ln in scribble(W, H, x0, x1, y, rng, 4)]
    ink = strokes(W, H, lines)
    art = G(art, ink, "#2b3a63", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.4, feather=0.4)
    card = shapes(W, H, [[(436, 222), (586, 214), (592, 334), (442, 342)]], smooth=False)
    art = over(art, soft_shadow(card, "#3a2a14", blur=4, strength=0.3, dx=2, dy=3))
    art = GP(art, card, "#fbf7ee", "#efe6d2", seed=nx(), rough=0.6, pad=6)
    pic = shapes(W, H, [[(448, 230), (580, 223), (584, 306), (452, 313)]], smooth=False)
    sky = pigment(pic, "#b9c9d8", "#e7d2b4", seed=nx(), density=0.85, edge=0.3, bloom=0.4, rough=1)
    art = over(art, sky)
    hillm = shapes(W, H, [[(448, 290), (490, 268), (530, 280), (584, 262), (584, 306), (452, 313)]]) * pic
    art = G(art, hillm, "#8ea283", "#5f7a63", seed=nx(), density=0.75, edge=0.4, rough=1.5)
    bld = shapes(W, H, [rect(500, 252, 540, 290)], smooth=False) * pic
    art = G(art, bld, "#e9e1d0", "#c8b89a", seed=nx(), density=0.8, edge=0.5, rough=0.8)
    art = G(art, shapes(W, H, [[(496, 254), (520, 240), (544, 254)]], smooth=False) * pic, "#a05a42", seed=nx(), density=0.8, edge=0.5, rough=0.6)
    tp = shapes(W, H, [[(492, 206), (540, 202), (542, 226), (494, 230)]], smooth=False)
    art = OV(art, tp, lambda m: tint(m, "#e7cf98", 0.7))
    art = jw.leaf(art, W, H, 640, 380, 70, -2.2, rng, nx, c=("#c9a66a", "#9b7a3e"))
    # ribbon bookmark lying across the right page and hanging out the bottom
    rib = shapes(W, H, [[(400, 52), (414, 52), (470, 380), (500, 548), (488, 556), (476, 540), (466, 552), (456, 384)]], smooth=False)
    art = GP(art, rib, OCHRE, "#9a6c26", seed=nx(), rough=0.6, streak=1.2, pad=6)
    art = G(art, shade_side(rib, -3, 0, 2), "#7a5218", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4)
    preview(art, "pt-journal", bg="#22345a")
    save(art, f"{OUT}/journal.webp", max_w=560, quality=82)
    clear()

if "pen" in PARTS:
    W, H = 560, 110
    nx = Seq(50300); rng = random.Random(5)
    art = blank(W, H)
    sh = shapes(W, H, [rect(30, 66, 520, 80)], smooth=False)
    art = over(art, soft_shadow(sh, "#0b1222", blur=6, strength=0.35, dx=0, dy=8))
    barrel = shapes(W, H, [[(110, 40), (470, 38), (500, 46), (506, 55), (500, 64), (470, 72), (110, 70)]])
    grip = shapes(W, H, [[(70, 46), (112, 41), (112, 69), (70, 64)]], smooth=False)
    nib = shapes(W, H, [[(16, 55), (40, 48), (72, 45), (72, 65), (40, 62)]], smooth=False)
    art = FO(art, nib, "#d2ad5e", seed=nx(), emboss=0.8, sparkle=0.15)
    art = GP(art, strokes(W, H, [([(20, 55), (58, 55)], 1.2, None)]) * nib, "#5a4318", seed=nx(), rough=0.2, pad=4)
    art = GP(art, circles(W, H, [(58, 55, 2.6)]), "#5a4318", seed=nx(), rough=0.2, pad=4)
    art = GP(art, grip, "#14203a", "#0d152a", seed=nx(), rough=0.5, pad=6)
    art = GP(art, barrel, NAVY, NAVY_D, seed=nx(), rough=0.6, streak=1.0, pad=8)
    hi = strokes(W, H, [([(120, 46), (470, 45)], 3.5, (0.1, 0.2))])
    art = G(art, hi, "#8aa2cf", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4)
    bands = np.maximum.reduce([shapes(W, H, [rect(108, 39, 116, 71)], smooth=False), shapes(W, H, [rect(300, 38, 312, 72)], smooth=False)])
    clip = shapes(W, H, [[(316, 30), (452, 30), (460, 35), (452, 40), (330, 40)]])
    art = FO(art, np.maximum(bands, clip), "#c9a45a", seed=nx(), emboss=0.8, sparkle=0.14)
    art = FO(art, circles(W, H, [(320, 35, 7)]), "#c9a45a", seed=nx(), emboss=0.8)
    preview(art, "pt-pen", bg="#f6eedd")
    save(art, f"{OUT}/pen.webp", max_w=300, quality=84)
    clear()

if "pressed" in PARTS:
    W, H = 320, 420
    nx = Seq(50500); rng = random.Random(9)
    art = blank(W, H)
    st = curve([(160, 410), (150, 300), (170, 200), (156, 90)], 30)
    art = G(art, strokes(W, H, [(st, 3, (0.02, 0.3)), (curve([(152, 280), (210, 230), (236, 180)], 14), 2.2, (0, 0.4)), (curve([(160, 230), (104, 196), (90, 150)], 14), 2, (0, 0.4))]), SAGE_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6)
    for (x, y, L, a) in [(152, 340, 66, -2.5), (156, 320, 60, -0.6), (164, 260, 52, -2.8), (166, 250, 46, -0.3)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx, c=(SAGE, SAGE_D))
    art = cosmos(art, W, H, 156, 86, 54, rng, nx)
    art = cosmos(art, W, H, 238, 172, 34, rng, nx)
    art = daisy(art, W, H, 90, 146, 26, rng, nx)
    preview(art, "pt-pressed")
    save(art, f"{OUT}/pressed.webp", max_w=220, quality=82)
    clear()

if "bloom" in PARTS:
    W = H = 120
    nx = Seq(50700); rng = random.Random(11)
    art = daisy(blank(W, H), W, H, 60, 60, 46, rng, nx, n=14)
    preview(art, "pt-bloom", bg="#22345a")
    save(art, f"{OUT}/bloom.webp", max_w=72, quality=84)

kb(OUT)
