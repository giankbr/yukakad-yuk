"""Ultah Bajak Laut — storybook treasure map: watercolour on a reserved paper ground with a sepia dip-pen contour
(original designs). A chunky friendly wooden pirate ship (striped sails, crow's nest, portholes, a black flag with a
smiling eye-patch face), a palm island with a painted red X, a red-green parrot on a perch, a brass telescope, an open
treasure chest with coins, a compass rose, a dotted-trail divider and a tileable parchment texture.
Run: python3 -I ultah-bajak-laut.py [part ...]  parts: ship island parrot telescope chest compass divider parchment
Assets -> public/themes/art/ultah-bajak-laut/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i2_lib import *  # noqa
import _e6_lib as e6

OUT = outdir("ultah-bajak-laut")
PARTS = sys.argv[1:] or ["ship", "island", "parrot", "telescope", "chest", "compass", "divider", "parchment"]
SEPIA = "#4a2e1c"
WOOD, WOOD2, WOOD_D = "#9a5f34", "#b87a46", "#5e3820"
CREAM, CREAM2 = "#f6ead2", "#fff7e6"
RED, RED2 = "#d4473a", "#e8685a"
TEAL, TEAL2 = "#2f9aa6", "#6cc6c4"
GOLD, GOLD2 = "#e8b33c", "#f6d168"
NAVY = "#263247"
LEAF, LEAF2 = "#4f9a4a", "#7cc35e"
SAND, SAND2 = "#f0d494", "#f7e4b4"


def ink(art, m, col, col2=None, nx=None, shade=(1, 1), k=12, dens=0.8, line=SEPIA, lw=2.4, base=True, sh_col="#5a3a3a"):
    """Watercolour wash on a reserved white ground, a glazed shadow on one side, then a dip-pen contour."""
    art = e6.wash(art, m, col, col2, nx=nx, dens=dens, shade=shade, k=k, base=base, sh_col=sh_col)
    if line:
        art = e6.pen(art, m, nx, col=line, w=lw, dens=0.85)
    return art


def pen_lines(art, W, H, items, nx, col=SEPIA, dens=0.8):
    return G(art, strokes(W, H, items), col, seed=nx(), density=dens, edge=0, bloom=0, rough=0.5, feather=0.35, pad=6)


def wave_band(art, W, H, y, x0, x1, nx, rng, amp=10, period=46, col=TEAL, col2=TEAL2):
    pts = [(x0, y + 60)]
    x = x0
    while x <= x1:
        pts += [(x + period * t, y - amp * math.sin(math.pi * t) ** 0.8) for t in np.linspace(0, 1, 8)]
        x += period
    pts += [(x1, y + 60)]
    m = shapes(W, H, [pts], smooth=False)
    art = ink(art, m, col, col2, nx, shade=(0, 1), k=10, dens=0.75, lw=2.0)
    foam = []
    x = x0
    while x <= x1:
        foam.append((arc_pts(x + period * 0.5, y + 2, period * 0.32, math.pi * 1.1, math.pi * 1.9, 8), 2.2, (0.2, 0.2)))
        x += period
    art = G(art, strokes(W, H, foam), "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.4, pad=6)
    return art


def ship():
    W, H = 720, 700
    rng = random.Random(1); nx = Seq(100)
    art = blank(W, H)
    # masts first (behind sails)
    masts = strokes(W, H, [([(300, 450), (300, 80)], 13, None), ([(470, 450), (470, 150)], 11, None)])
    art = ink(art, masts, WOOD, WOOD2, nx, shade=(1, 0), k=5, lw=2.0)
    # rigging lines from mast tops to hull ends
    art = pen_lines(art, W, H, [([(300, 90), (120, 352)], 1.6, None), ([(300, 90), (610, 380)], 1.4, None), ([(470, 160), (640, 360)], 1.4, None), ([(470, 160), (300, 120)], 1.2, None)], nx, dens=0.6)
    # main sails: billowing, cream with red stripes
    def sail(x0, x1, y0, y1, bulge):
        top = [(x, y0 + 6 * math.sin(math.pi * (x - x0) / (x1 - x0))) for x in np.linspace(x0, x1, 12)]
        right = [(x1 + bulge * math.sin(math.pi * t), y0 + (y1 - y0) * t) for t in np.linspace(0, 1, 12)]
        bot = [(x, y1 + bulge * 0.35 * math.sin(math.pi * (x - x0) / (x1 - x0))) for x in np.linspace(x1, x0, 12)]
        left = [(x0 + bulge * math.sin(math.pi * t), y1 - (y1 - y0) * t) for t in np.linspace(0, 1, 12)]
        return top + right + bot + left
    for (x0, x1, y0, y1, b) in [(200, 400, 130, 300, 22), (222, 378, 318, 410, 14), (395, 545, 190, 330, 18), (410, 530, 345, 420, 12)]:
        pts = sail(x0, x1, y0, y1, b)
        m = shapes(W, H, [deform(pts, rng, 1, 0.004)])
        art = ink(art, m, CREAM, CREAM2, nx, shade=(1, 1), k=16, dens=0.55, sh_col="#a9876a")
        # stripes
        for f0, f1 in ((0.28, 0.42), (0.62, 0.76)):
            st = m * rect(W, H, 0, y0 + (y1 - y0) * f0, W, y0 + (y1 - y0) * f1)
            art = G(art, displace(st, nx(), 2, 12), RED, RED2, seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=2)
        # billow seams
        art = pen_lines(art, W, H, [(curve([(x0 + b * 0.6, y0 + 20), ((x0 + x1) / 2 + b * 0.7, (y0 + y1) / 2), (x0 + b * 0.6, y1 - 12)], 14), 1.2, (0.2, 0.3))], nx, dens=0.4)
        # yard (spar) across the top
        yard = strokes(W, H, [([(x0 - 14, y0 - 2), (x1 + 14, y0 - 2)], 8, None)])
        art = ink(art, yard, WOOD_D, WOOD, nx, shade=None, lw=1.8)
    # crow's nest
    nest = shapes(W, H, [[(272, 96), (328, 96), (322, 124), (278, 124)]], smooth=False)
    art = ink(art, nest, WOOD, WOOD2, nx, shade=(1, 0), k=6, lw=2.0)
    art = pen_lines(art, W, H, [([(276, 104), (324, 104)], 1.2, None), ([(277, 114), (323, 114)], 1.2, None)], nx, dens=0.5)
    # flag: black, waving, with a friendly smiling eye-patch face
    fl = [(304, 22), (330, 14), (360, 26), (392, 18), (392, 70), (360, 78), (330, 66), (304, 74)]
    fm = shapes(W, H, [fl])
    art = ink(art, fm, "#2b2b33", "#3d3d48", nx, shade=(1, 1), k=8, dens=0.95, sh_col="#000000")
    pole = strokes(W, H, [([(302, 84), (302, 10)], 5, None)])
    art = ink(art, pole, WOOD_D, None, nx, shade=None, lw=1.4)
    face = circles(W, H, [(348, 46, 17)])
    art = ink(art, face, "#fbf3e2", "#ffffff", nx, shade=None, line=None)
    eye = circles(W, H, [(342, 42, 2.8)])
    art = G(art, eye, "#2b2b33", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2, pad=4)
    patch = shapes(W, H, [ellipse_pts(355, 42, 5.5, 4.5, 10)])
    art = G(art, patch + strokes(W, H, [([(333, 36), (366, 47)], 1.6, None)]), "#2b2b33", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2, pad=4)
    smile = strokes(W, H, [(arc_pts(348, 49, 8, 0.35, math.pi - 0.35, 10), 2.0, (0.2, 0.2))])
    art = G(art, smile, "#2b2b33", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2, pad=4)
    # hull
    hull = [(96, 330), (236, 336), (246, 398), (560, 400), (636, 356), (648, 372), (618, 452), (560, 520), (190, 526), (130, 470)]
    hm = shapes(W, H, [deform(hull, rng, 1, 0.003)])
    art = ink(art, hm, WOOD, WOOD2, nx, shade=(1, 1), k=24, dens=0.85, lw=2.8, sh_col="#3a2010")
    # planks following the hull curve
    planks = []
    for f in np.linspace(0.18, 0.92, 6):
        y_l = 398 + (526 - 398) * f
        planks.append((curve([(130 + 40 * f, y_l - 4), (380, y_l + 6 * f), (600 - 40 * f, y_l - 10 - 10 * (1 - f))], 20), 1.4, (0.05, 0.05)))
    art = pen_lines(art, W, H, planks, nx, dens=0.55)
    trim = strokes(W, H, [(curve([(110, 420), (380, 432), (628, 410)], 20), 12, None)]) * hm
    art = ink(art, trim, GOLD, GOLD2, nx, shade=None, line=None, dens=0.9)
    # aft castle panel & windows
    win = shapes(W, H, [[(130, 350), (226, 352), (228, 392), (138, 392)]], smooth=False)
    art = ink(art, win, WOOD2, "#c98e58", nx, shade=(1, 1), k=8, lw=1.8)
    for x in (150, 178, 206):
        wm = shapes(W, H, [[(x - 9, 360), (x + 9, 360), (x + 9, 384), (x - 9, 384)]], smooth=False)
        art = ink(art, wm, "#f4c86a", "#ffe09a", nx, shade=None, lw=1.6, dens=0.9)
    # portholes
    for x in (300, 380, 460):
        ring = circles(W, H, [(x, 468, 18)])
        art = ink(art, ring, GOLD, GOLD2, nx, shade=None, lw=1.8, dens=0.9)
        gl = circles(W, H, [(x, 468, 11)])
        art = ink(art, gl, NAVY, "#3b4c66", nx, shade=None, line=None, dens=0.9)
        art = G(art, strokes(W, H, [(arc_pts(x, 468, 6, math.pi * 1.1, math.pi * 1.5, 6), 2.2, None)]), "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.2, pad=4)
    # rail with balusters
    rail = strokes(W, H, [([(244, 382), (560, 384), (630, 346)], 5, None)])
    art = ink(art, rail, WOOD_D, None, nx, shade=None, lw=1.4)
    art = pen_lines(art, W, H, [([(x, 384), (x, 398)], 2.0, None) for x in range(256, 556, 22)], nx, dens=0.7)
    # bowsprit
    bs = strokes(W, H, [([(620, 372), (700, 320)], 8, None)])
    art = ink(art, bs, WOOD, None, nx, shade=None, lw=1.6)
    art = pen_lines(art, W, H, [([(700, 322), (545, 190)], 1.3, None)], nx, dens=0.6)
    # sea
    art = wave_band(art, W, H, 520, -20, W + 20, nx, rng, amp=14, period=58)
    art = wave_band(art, W, H, 566, -50, W + 20, nx, rng, amp=12, period=64, col="#2a8796", col2="#53b3b6")
    preview(art, "ship", bg="#ecd9b0")
    print("ship", save(art, f"{OUT}/ship.webp", max_w=360, quality=82))
    clear()


def palm(art, W, H, px, py, ph, lean, rng, nx, s=1.0):
    trunk = curve([(px, py), (px + lean * ph * 0.3, py - ph * 0.55), (px + lean * ph, py - ph)], 24)
    tm = strokes(W, H, [(trunk, 14 * s, (0.0, 0.3))])
    art = ink(art, tm, "#a2774a", "#c09464", nx, shade=(1, 0), k=6, lw=2.0)
    art = pen_lines(art, W, H, [([(x - 6 * s, y), (x + 6 * s, y + 2)], 1.3, None) for x, y in trunk[3::3]], nx, dens=0.6)
    tx, ty = trunk[-1]
    for a in np.linspace(-math.pi * 0.98, -0.02, 6):
        L = rng.uniform(70, 95) * s
        pts = [(tx, ty), (tx + math.cos(a) * L * 0.55, ty + math.sin(a) * L * 0.5 - 14 * s), (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.25 + 26 * s)]
        c = curve(pts, 16)
        left = []; right = []
        for i, (x, y) in enumerate(c):
            t = i / (len(c) - 1)
            wd = 16 * s * math.sin(math.pi * min(1, t * 1.1)) ** 0.7
            j = min(len(c) - 1, i + 1); k_ = max(0, i - 1)
            dx, dy = c[j][0] - c[k_][0], c[j][1] - c[k_][1]
            d = math.hypot(dx, dy) or 1
            left.append((x - dy / d * wd, y + dx / d * wd)); right.append((x + dy / d * wd * 0.6, y - dx / d * wd * 0.6))
        m = shapes(W, H, [left + right[::-1]])
        art = ink(art, m, LEAF, LEAF2, nx, shade=(0, 1), k=6, dens=0.85, lw=1.8)
        art = pen_lines(art, W, H, [(c, 1.3, (0.0, 0.5))], nx, dens=0.6)
    nuts = circles(W, H, [(tx - 6 * s, ty + 6 * s, 7 * s), (tx + 7 * s, ty + 8 * s, 7 * s)])
    art = ink(art, nuts, "#7a5a2a", "#9a7a3a", nx, shade=None, lw=1.4)
    return art


def island():
    W, H = 640, 440
    rng = random.Random(2); nx = Seq(200)
    art = blank(W, H)
    # shallow water ring
    ring = shapes(W, H, [deform(ellipse_pts(320, 330, 300, 92, 16), rng, 2, 0.03)])
    art = G(art, displace(ring, nx(), 6, 20), TEAL2, "#a8e0d6", seed=nx(), density=0.55, edge=0.7, bloom=0.4, rough=4)
    sand = shapes(W, H, [deform(ellipse_pts(320, 318, 240, 64, 16), rng, 2, 0.04)])
    art = ink(art, sand, SAND, SAND2, nx, shade=(0, 1), k=14, dens=0.8, sh_col="#a87a4a")
    hill = shapes(W, H, [[(150, 300), (220, 250), (300, 238), (380, 252), (450, 300), (300, 316)]])
    art = ink(art, hill, LEAF, LEAF2, nx, shade=(1, 1), k=14, dens=0.75)
    rocks = shapes(W, H, [deform(ellipse_pts(500, 318, 30, 18, 9), rng, 1, 0.08), deform(ellipse_pts(530, 326, 18, 11, 9), rng, 1, 0.08)])
    art = ink(art, rocks, "#9a948a", "#b8b2a6", nx, shade=(1, 1), k=6, dens=0.8, lw=1.8)
    art = palm(art, W, H, 250, 286, 190, -0.18, rng, nx, 1.0)
    art = palm(art, W, H, 330, 290, 150, 0.22, rng, nx, 0.82)
    # red X with brush strokes
    xm = strokes(W, H, [([(402, 290), (458, 342)], 17, (0.12, 0.12)), ([(460, 288), (400, 344)], 17, (0.12, 0.12))])
    art = G(art, xm, RED, "#b83226", seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=1.4, pad=8)
    # dotted trail arriving at the X
    trail = curve([(40, 380), (140, 370), (250, 345), (340, 332), (400, 322)], 40)
    art = G(art, dotted(W, H, trail, 15, 3.2), SEPIA, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.3, pad=4)
    # grass tufts
    gt = grass_tufts(W, H, 296, 320, 26, rng, hmin=8, hmax=16, lean=0.2, width=2.0)
    art = G(art, gt * sand, "#3f8a3e", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3, pad=4)
    preview(art, "island", bg="#ecd9b0")
    print("island", save(art, f"{OUT}/island.webp", max_w=320, quality=82))
    clear()


def parrot():
    W, H = 360, 460
    rng = random.Random(3); nx = Seq(300)
    art = blank(W, H)
    # tail feathers (behind)
    for dx, col, c2 in ((-14, "#2f6fb8", "#5a94d4"), (0, RED, RED2), (14, GOLD, GOLD2)):
        t = shapes(W, H, [[(170 + dx * 0.4, 300), (186 + dx * 0.4, 300), (196 + dx, 440), (178 + dx, 446)]])
        art = ink(art, t, col, c2, nx, shade=(1, 0), k=6, lw=1.8)
    # perch
    perch = strokes(W, H, [([(30, 318), (330, 306)], 16, None)])
    art = ink(art, perch, WOOD, WOOD2, nx, shade=(0, 1), k=6, lw=2.0)
    # body
    body = shapes(W, H, [deform(ellipse_pts(184, 230, 66, 92, 18, 0.18), rng, 1, 0.01)])
    art = ink(art, body, RED, RED2, nx, shade=(1, 1), k=22, dens=0.85, sh_col="#6a1a1a")
    belly = shapes(W, H, [ellipse_pts(170, 250, 34, 56, 14, 0.18)])
    art = ink(art, belly, "#f08a5a", "#f6a878", nx, shade=None, line=None, dens=0.7)
    # wing: green with yellow and blue bars
    wing = shapes(W, H, [[(204, 170), (252, 210), (262, 280), (240, 326), (210, 300), (196, 230)]])
    art = ink(art, wing, LEAF, LEAF2, nx, shade=(1, 1), k=10, lw=2.0)
    for f, c in ((0.55, GOLD), (0.78, "#2f6fb8")):
        bar = wing * rect(W, H, 0, 170 + 160 * f - 14, W, 170 + 160 * f + 6)
        art = G(art, bar, c, seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1.2, pad=6)
    art = pen_lines(art, W, H, [([(214, 240 + k * 18), (252, 252 + k * 18)], 1.2, None) for k in range(4)], nx, dens=0.5)
    # head
    head = circles(W, H, [(170, 132, 54)])
    art = ink(art, head, RED, RED2, nx, shade=(1, 1), k=16, dens=0.85, sh_col="#6a1a1a")
    face = shapes(W, H, [ellipse_pts(150, 128, 26, 22, 14, -0.2)])
    art = ink(art, face, "#fbf3e2", "#ffffff", nx, shade=None, line=None, dens=0.95)
    art = pen_lines(art, W, H, [(arc_pts(150, 128, 20, -0.5, 2.2, 8), 1.0, (0.2, 0.2))], nx, dens=0.35)
    eye = circles(W, H, [(150, 124, 9)])
    art = G(art, eye, "#1f1a1a", seed=nx(), density=0.96, edge=0, bloom=0, rough=0.2, pad=4)
    art = G(art, circles(W, H, [(147, 120, 3.2)]), "#ffffff", seed=nx(), density=1, edge=0, bloom=0, rough=0.1, pad=4)
    # beak: curved, yellow-horn, upper hook over lower
    up = shapes(W, H, [[(122, 128), (100, 132), (84, 150), (90, 170), (100, 160), (116, 152), (128, 146)]])
    art = ink(art, up, "#f2c45a", "#f8dc8a", nx, shade=(1, 1), k=6, lw=2.0)
    lo = shapes(W, H, [[(124, 148), (104, 160), (110, 172), (128, 160)]])
    art = ink(art, lo, "#5a4a3a", "#7a6a52", nx, shade=None, lw=1.6)
    # crest feathers & cheek blush
    crest = shapes(W, H, [[(182, 82), (196, 54), (204, 86)], [(196, 90), (220, 70), (216, 98)]])
    art = ink(art, crest, RED, RED2, nx, shade=None, lw=1.6)
    # feet on the perch
    feet = strokes(W, H, [([(170, 312), (162, 324)], 6, None), ([(176, 312), (178, 326)], 6, None), ([(196, 310), (192, 324)], 6, None), ([(202, 310), (208, 322)], 6, None)])
    art = ink(art, feet, "#7a7a86", None, nx, shade=None, lw=1.2)
    preview(art, "parrot", bg="#ecd9b0")
    print("parrot", save(art, f"{OUT}/parrot.webp", max_w=170, quality=84))
    clear()


def telescope():
    W, H = 520, 200
    rng = random.Random(4); nx = Seq(400)
    art = blank(W, H)
    ang = -0.22
    ca, sa = math.cos(ang), math.sin(ang)
    def seg(u0, u1, r0, r1):
        P = lambda u, v: (60 + u * ca - v * sa, 120 + u * sa + v * ca)
        return [P(u0, -r0), P(u1, -r1), P(u1, r1), P(u0, r0)]
    parts = [(0, 150, 22, 24, "#b67a3a", "#d39a56"), (150, 290, 28, 30, GOLD, GOLD2), (290, 400, 34, 36, "#b67a3a", "#d39a56")]
    for u0, u1, r0, r1, c1, c2 in parts:
        m = shapes(W, H, [seg(u0, u1, r0, r1)], smooth=False)
        art = ink(art, m, c1, c2, nx, shade=(0, 1), k=10, dens=0.85, lw=2.0)
        rim = shapes(W, H, [seg(u1 - 10, u1 + 2, r1 + 3, r1 + 3)], smooth=False)
        art = ink(art, rim, "#c99032", "#f0c460", nx, shade=None, lw=1.6, dens=0.9)
    lens = shapes(W, H, [ellipse_pts(60 + 404 * ca, 120 + 404 * sa, 8, 37, 14, ang)])
    art = ink(art, lens, TEAL, TEAL2, nx, shade=None, lw=1.8, dens=0.9)
    hi = strokes(W, H, [([(80 + u * ca - 14 * (-sa) * 0, 120 + u * sa - 14) for u in (20, 380)], 3, (0.3, 0.3))])
    art = G(art, strokes(W, H, [([(60 + u * ca + 12 * sa, 120 + u * sa - 12 * ca) for u in (20, 380)], 3.2, (0.2, 0.2))]), "#fff6d8", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, pad=4)
    preview(art, "telescope", bg="#ecd9b0")
    print("telescope", save(art, f"{OUT}/telescope.webp", max_w=220, quality=84))
    clear()


def chest():
    W, H = 460, 400
    rng = random.Random(5); nx = Seq(500)
    art = blank(W, H)
    # lid (open, tilted back)
    lid = shapes(W, H, [[(90, 150), (370, 150), (380, 70), (340, 30), (120, 30), (80, 70)]])
    art = ink(art, lid, WOOD, WOOD2, nx, shade=(1, 1), k=14, lw=2.6, sh_col="#3a2010")
    lidin = shapes(W, H, [[(104, 146), (356, 146), (364, 82), (332, 50), (128, 50), (96, 82)]])
    art = ink(art, lidin, "#6a3a22", "#7e4a2a", nx, shade=None, line=None, dens=0.85)
    # coins heaped above the rim
    coins = [(rng.uniform(110, 350), rng.uniform(150, 200), rng.uniform(13, 18)) for _ in range(26)]
    coins.sort(key=lambda c: c[1])
    heap = shapes(W, H, [[(96, 214), (130, 168), (200, 140), (270, 142), (330, 168), (364, 214)]])
    art = ink(art, heap, GOLD, GOLD2, nx, shade=(1, 1), k=14, dens=0.9, sh_col="#a06a1a")
    for x, y, r in coins:
        c = shapes(W, H, [ellipse_pts(x, y, r, r * 0.62, 12, rng.uniform(-0.3, 0.3))])
        art = ink(art, c, GOLD, GOLD2, nx, shade=None, lw=1.4, dens=0.92)
        art = pen_lines(art, W, H, [(arc_pts(x, y, r * 0.55, math.pi * 1.1, math.pi * 1.9, 6, squash=0.62), 1.0, None)], nx, dens=0.4)
    gem = shapes(W, H, [[(214, 152), (230, 138), (246, 152), (230, 170)]], smooth=False)
    art = ink(art, gem, RED, RED2, nx, shade=None, lw=1.4, dens=0.95)
    gem2 = shapes(W, H, [[(298, 170), (310, 158), (322, 170), (310, 184)]], smooth=False)
    art = ink(art, gem2, TEAL, TEAL2, nx, shade=None, lw=1.4, dens=0.95)
    # box
    box = shapes(W, H, [[(80, 206), (380, 206), (372, 360), (88, 360)]], smooth=False)
    art = ink(art, box, WOOD, WOOD2, nx, shade=(1, 1), k=22, lw=2.8, sh_col="#3a2010")
    art = pen_lines(art, W, H, [([(86, y), (376, y)], 1.3, None) for y in (250, 296)], nx, dens=0.5)
    for x0 in (112, 330):
        band = shapes(W, H, [[(x0, 206), (x0 + 24, 206), (x0 + 22, 360), (x0 + 2, 360)]], smooth=False)
        art = ink(art, band, "#c99032", "#e8b84a", nx, shade=None, lw=1.6, dens=0.92)
    lock = shapes(W, H, [[(210, 220), (250, 220), (250, 268), (230, 280), (210, 268)]], smooth=False)
    art = ink(art, lock, "#c99032", "#e8b84a", nx, shade=None, lw=1.8, dens=0.92)
    art = G(art, circles(W, H, [(230, 244, 5)]) + strokes(W, H, [([(230, 246), (230, 260)], 3, None)]), "#3a2010", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.2, pad=4)
    # sparkle glints (painted, small)
    for x, y in ((150, 140), (330, 132)):
        art = G(art, strokes(W, H, [([(x - 9, y), (x + 9, y)], 2.4, (0.4, 0.4)), ([(x, y - 9), (x, y + 9)], 2.4, (0.4, 0.4))]), "#fffbe8", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2, pad=4)
    preview(art, "chest", bg="#ecd9b0")
    print("chest", save(art, f"{OUT}/chest.webp", max_w=220, quality=84))
    clear()


def compass():
    W = H = 360
    rng = random.Random(6); nx = Seq(600)
    art = blank(W, H)
    c = W / 2
    ring = np.clip(circles(W, H, [(c, c, 150)]) - circles(W, H, [(c, c, 128)]), 0, 1)
    disc = circles(W, H, [(c, c, 150)])
    art = ink(art, disc, CREAM, CREAM2, nx, shade=(1, 1), k=16, dens=0.5, sh_col="#a9876a")
    art = ink(art, ring, "#d9b06a", "#e8c88a", nx, shade=None, lw=2.0, dens=0.8)
    ticks = [([(c + math.cos(a) * 130, c + math.sin(a) * 130), (c + math.cos(a) * (140 if k % 4 else 148), c + math.sin(a) * (140 if k % 4 else 148))], 1.6, None) for k, a in enumerate(np.linspace(0, math.tau, 32, endpoint=False))]
    art = pen_lines(art, W, H, ticks, nx, dens=0.7)
    def point(a, L, w):
        return [(c, c), (c + math.cos(a - math.pi / 2) * w, c + math.sin(a - math.pi / 2) * w), (c + math.cos(a) * L, c + math.sin(a) * L), (c + math.cos(a + math.pi / 2) * w, c + math.sin(a + math.pi / 2) * w)]
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4 + math.pi / 4 * 0
        if k % 2:
            m = shapes(W, H, [point(a, 86, 14)], smooth=False)
            art = ink(art, m, TEAL, TEAL2, nx, shade=None, lw=1.6, dens=0.85)
    for k in range(4):
        a = -math.pi / 2 + k * math.pi / 2
        m = shapes(W, H, [point(a, 124, 22)], smooth=False)
        col = RED if k == 0 else NAVY
        art = ink(art, m, col, mix(col, "#ffffff", 0.2), nx, shade=None, lw=1.8, dens=0.9)
        half = shapes(W, H, [[(c, c), (c + math.cos(a - math.pi / 2) * 22, c + math.sin(a - math.pi / 2) * 22), (c + math.cos(a) * 124, c + math.sin(a) * 124)]], smooth=False)
        art = G(art, half, "#ffffff", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.3, pad=4)
    art = ink(art, circles(W, H, [(c, c, 14)]), GOLD, GOLD2, nx, shade=None, lw=1.6, dens=0.95)
    preview(art, "compass", bg="#ecd9b0")
    print("compass", save(art, f"{OUT}/compass.webp", max_w=150, quality=84))
    clear()


def divider():
    W, H = 560, 90
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    trail = curve([(14, 54), (120, 34), (240, 58), (330, 40)], 50)
    art = G(art, dotted(W, H, trail, 16, 3.6), SEPIA, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.3, pad=4)
    xm = strokes(W, H, [([(350, 26), (384, 60)], 9, (0.15, 0.15)), ([(384, 24), (350, 62)], 9, (0.15, 0.15))])
    art = G(art, xm, RED, "#b83226", seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=1.2, pad=8)
    trail2 = curve([(404, 46), (470, 60), (546, 40)], 30)
    art = G(art, dotted(W, H, trail2, 16, 3.6), SEPIA, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.3, pad=4)
    preview(art, "divider", bg="#ecd9b0")
    print("divider", save(art, f"{OUT}/divider.webp", max_w=280, quality=84))
    clear()


def parchment():
    """Tileable parchment: warm paper, tea stains, fibre; 512 x 512 opaque."""
    S = 512
    base = np.asarray(paper(S, S, "#efdcb4", 9, fiber=1.0, mottle=1.2), np.float32) / 255
    st = fbm(S, S, 91, 140, 4)
    st2 = fbm(S, S, 93, 50, 3)
    stain = np.clip((st - 0.5) * 2.2, 0, 1) * 0.12 + np.clip((st2 - 0.66) * 3, 0, 1) * 0.07
    speck = (np.random.default_rng(5).random((S, S)) > 0.9975).astype(np.float32)
    stain = stain + gaussian_filter(speck, 0.7) * 1.6
    rgb = base * (1 - stain[..., None]) + carr("#b98a4a") * stain[..., None]
    # make it tile: crossfade with a half-shifted copy
    sh = np.roll(np.roll(rgb, S // 2, 0), S // 2, 1)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    w = (np.minimum(xx, S - 1 - xx) / (S / 2)) * (np.minimum(yy, S - 1 - yy) / (S / 2))
    w = np.clip(w * 3, 0, 1)[..., None]
    rgb = rgb * w + sh * (1 - w)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/parchment.png")
    print("parchment", save_rgb(rgb, f"{OUT}/parchment.webp", quality=72))
    clear()


for p in PARTS:
    globals()[p]()
kb_report(OUT)
