"""Rumah Pohon — a storybook treehouse at golden hour in gouache with a soft brown-pencil contour (original designs):
the canopy with a plank treehouse (shingled roof, glowing round window, balcony railing, bunting and fairy lights),
a tall trunk with roots, ferns and mushrooms, a rope ladder, a pale-pine hanging sign board, a misty golden forest,
and a bunting divider.
Run: python3 -I rumah-pohon.py [part ...]  parts: canopy trunk ladder sign forest bunting
Assets -> public/themes/art/rumah-pohon/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t3_lib import *

OUT = outdir("rumah-pohon")
PARTS = sys.argv[1:] or ["canopy", "trunk", "ladder", "sign", "forest", "bunting"]
LINE = "#4a2e1c"
BARK, BARK2, BARK_D = "#7a4c2c", "#9a6638", "#4a2c18"
PLANK, PLANK2 = "#c98f52", "#e2ae6e"
ROOF, ROOF2 = "#b8492f", "#d6683f"
F_D, F_M, F_L, RIM = "#2e5434", "#4e7c3c", "#8eab48", "#f0c95e"
BULB = "#ffd57a"
FLAGS = [("#d9573b", "#e8774f"), ("#e8b43a", "#f3cb5a"), ("#3f8f8a", "#5aaba3"), ("#f4e6c8", "#fff6e0")]


def tn(art, m, col, col2, nx, k=10, line=LINE, line_a=0.55, shade=(-1, -1), sh=None):
    return toon(art, m, col, col2, nx, shade=shade, k=k, sh_col=sh, line=line, line_w=2.0, line_a=line_a)


def clump(rng, cx, cy, r):
    return deform(ellipse_pts(cx, cy, r, r * rng.uniform(0.7, 0.9), 12, rng.uniform(0, 3)), rng, 2, 0.16)


def foliage(art, W, H, rng, nx, centers, rim_side=1):
    """Leaf clumps painted dark->mid->light with a warm rim on the sun side and leafy dabs."""
    dark = shapes(W, H, [clump(rng, x, y, r) for x, y, r in centers])
    art = G(art, dark, F_D, "#3a6438", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=6)
    mid = shapes(W, H, [clump(rng, x - rim_side * r * 0.12, y - r * 0.16, r * 0.78) for x, y, r in centers])
    art = G(art, mid, F_M, "#5c8a40", seed=nx(), density=0.85, edge=0.55, bloom=0.4, rough=5)
    lite = shapes(W, H, [clump(rng, x + rim_side * r * 0.22, y - r * 0.3, r * 0.45) for x, y, r in centers])
    art = G(art, lite, F_L, "#a9bf55", seed=nx(), density=0.7, edge=0.5, bloom=0.4, rough=4)
    dabs = []
    for x, y, r in centers:
        for _ in range(int(r / 3)):
            a = rng.uniform(-math.pi, math.pi); d = rng.uniform(0.3, 1.0) * r
            px, py = x + math.cos(a) * d, y + math.sin(a) * d * 0.8
            dabs.append(petal_pts(px, py, rng.uniform(9, 15), rng.uniform(5, 7), rng.uniform(0, math.tau), n=8))
    dm = shapes(W, H, dabs) * np.clip(gaussian_filter(dark, 3) * 1.4, 0, 1)
    art = G(art, dm, "#86ab4c", "#5f8c40", seed=nx(), density=0.38, edge=0.5, bloom=0.2, rough=1.5)
    rim = np.clip(dark - np.roll(dark, -rim_side * 12, 1) - np.roll(dark, 10, 0) * 0.3, 0, 1)
    art = G(art, rim * dark, RIM, "#f6d978", seed=nx(), density=0.65, edge=0.4, bloom=0.3, rough=3)
    return art


def fairy(art, W, H, nx, pts, step=24, line=True):
    path = curve(pts, 60)
    if line:
        art = G(art, strokes(W, H, [(path, 1.6, None)]), "#3a2a1c", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4)
    for x, y, _ in along(path, step):
        art = bulb(art, W, H, x, y + 4, 4.2, nx, BULB, "#fff8e0", 3.0)
    return art


if "canopy" in PARTS:
    W, H = 780, 780
    nx = Seq(100); rng = random.Random(11)
    art = blank(W, H)
    # limbs behind the leaves
    limbs = [
        (curve([(250, 790), (240, 640), (180, 520), (90, 470), (10, 470)], 40), 40, (0.0, 0.8)),
        (curve([(270, 790), (300, 600), (420, 520), (620, 470), (775, 420)], 40), 44, (0.0, 0.8)),
        (curve([(260, 700), (250, 560), (300, 420), (360, 300)], 30), 30, (0.0, 0.7)),
    ]
    lm = np.clip(strokes(W, H, limbs) + shapes(W, H, [[(203, 800), (198, 640), (230, 560), (290, 560), (312, 640), (307, 800)]]), 0, 1)
    centers = [(90, 140, 110), (250, 70, 120), (440, 60, 125), (630, 110, 120), (740, 230, 95), (40, 300, 100),
               (170, 300, 110), (620, 330, 105), (330, 200, 110), (520, 210, 105), (730, 380, 70), (60, 430, 70)]
    art = foliage(art, W, H, rng, nx, centers)
    art = tn(art, lm, BARK, BARK2, nx, k=10, sh=BARK_D)
    # platform + balcony
    plat = shapes(W, H, [[(236, 470), (612, 470), (612, 492), (236, 492)]], smooth=False)
    art = tn(art, plat, PLANK, PLANK2, nx, k=6, sh="#8a5a30")
    seams = strokes(W, H, [([(x, 472), (x, 490)], 1.4, None) for x in range(256, 612, 30)])
    art = G(art, seams, "#7a4a28", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    braces = strokes(W, H, [([(300, 492), (270, 560)], 10, None), ([(560, 492), (300, 600)], 10, None)])
    art = tn(art, braces, BARK, BARK2, nx, k=4, sh=BARK_D)
    # house walls (vertical planks)
    wall = shapes(W, H, [[(360, 300), (580, 300), (586, 470), (354, 470)]], smooth=False)
    art = tn(art, wall, "#b97a42", "#d39558", nx, k=14, sh="#7a4a28")
    pl = strokes(W, H, [([(x, 304), (x + 1, 468)], 1.6, None) for x in range(384, 580, 26)]) * wall
    art = G(art, pl, "#7a4a28", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5)
    # shingled roof
    roof = shapes(W, H, [[(330, 316), (470, 190), (612, 316), (600, 328), (342, 328)]], smooth=False)
    art = tn(art, roof, ROOF, ROOF2, nx, k=12, sh="#7d2a1c")
    sh_rows = []
    for y in range(214, 326, 14):
        t = (y - 190) / 126
        x0, x1 = 470 - 140 * t, 470 + 142 * t
        sh_rows.append(([(x0 + 4, y), (x1 - 4, y)], 1.8, None))
        for x in np.arange(x0 + 10 + (y % 28) / 2, x1 - 6, 16):
            sh_rows.append(([(x, y - 12), (x, y)], 1.2, None))
    art = G(art, strokes(W, H, sh_rows) * roof, "#7d2a1c", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5)
    chim = shapes(W, H, [[(540, 220), (562, 220), (562, 262), (540, 248)]], smooth=False)
    art = tn(art, chim, "#a35a3a", "#c07050", nx, k=4)
    # round window glowing + door
    art = OV(art, circles(W, H, [(414, 370, 44)]), lambda m: glow(m, "#ffd890", 18, 0.45))
    win = circles(W, H, [(414, 370, 25)])
    art = GP(art, win, "#ffd27a", "#fff1c2", seed=nx(), rough=0.6, streak=0.3)
    art = G(art, strokes(W, H, [([(414, 346), (414, 394)], 2.6, None), ([(390, 370), (438, 370)], 2.6, None)]) * win, "#7a4a28", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    art = G(art, contour(win, 4, nx()), "#6a3e20", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.5)
    door = shapes(W, H, [[(490, 470), (490, 380)] + arc_pts(518, 380, 28, math.pi, 2 * math.pi, 14) + [(546, 380), (546, 470)]], smooth=False)
    art = tn(art, door, "#3f8f8a", "#5aaba3", nx, k=6)
    art = bulb(art, W, H, 538, 428, 3, nx, "#f0c95e", "#fff3c0", 1.6)
    # balcony railing on the left part of the platform
    rail = [([(240, 470), (240, 432)], 5, None), ([(236, 432), (352, 432)], 6, None)]
    rail += [([(x, 470), (x, 436)], 3.5, None) for x in range(262, 352, 20)]
    art = tn(art, strokes(W, H, rail), PLANK, PLANK2, nx, k=3, sh="#8a5a30")
    # flower box under the window
    box = shapes(W, H, [[(384, 402), (446, 402), (442, 416), (388, 416)]], smooth=False)
    art = tn(art, box, "#d9573b", "#e8774f", nx, k=3)
    fl = circles(W, H, [(390 + i * 9, 398 + (i % 2) * 3, 4.5) for i in range(7)])
    art = GP(art, fl, "#f4e6c8", "#ffffff", seed=nx(), rough=0.5)
    # bunting from roof eave to a branch
    path = curve([(334, 318), (240, 380), (120, 400), (20, 380)], 50)
    art = G(art, strokes(W, H, [(path, 1.6, None)]), "#3a2a1c", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4)
    for i, (x, y, a) in enumerate(along(path, 34)):
        c1, c2 = FLAGS[i % 4]
        tri = shapes(W, H, [[(x - 13, y), (x + 13, y), (x + 2, y + 30)]], smooth=False)
        art = tn(art, tri, c1, c2, nx, k=3, line_a=0.45)
    # fairy lights along the limbs and the eaves
    art = fairy(art, W, H, nx, [(612, 492), (680, 510), (775, 470)])
    art = fairy(art, W, H, nx, [(10, 520), (120, 540), (236, 494)])
    art = fairy(art, W, H, nx, [(470, 196), (540, 272), (612, 318)], step=20, line=False)
    # a few leaf clumps in front of the house edges
    front = [(640, 300, 52), (330, 470, 44), (700, 470, 60), (80, 520, 52)]
    art = foliage(art, W, H, rng, nx, front)
    preview(art, "rp-canopy", tone="#f6d79a")
    save_full(art, f"{OUT}/canopy.webp", quality=72)
    clear()

if "trunk" in PARTS:
    W, H = 780, 1200
    nx = Seq(400); rng = random.Random(4)
    art = blank(W, H)
    cx = 255
    L = [(cx - 52, -60), (cx - 58, 300), (cx - 66, 700), (cx - 90, 960), (cx - 150, 1080), (cx - 230, 1120)]
    R = [(cx + 230, 1120), (cx + 140, 1070), (cx + 92, 960), (cx + 70, 700), (cx + 62, 300), (cx + 56, -60)]
    trunk = shapes(W, H, [curve(L, 30) + curve(R, 30)])
    art = tn(art, trunk, BARK, BARK2, nx, k=26, sh=BARK_D)
    bark = []
    for i in range(26):
        x = cx + rng.uniform(-55, 55)
        y0 = rng.uniform(0, 900); ln = rng.uniform(80, 260)
        bark.append((curve([(x, y0), (x + rng.uniform(-8, 8), y0 + ln / 2), (x + rng.uniform(-12, 12), y0 + ln)], 12), rng.uniform(2, 4), (0.2, 0.3)))
    art = G(art, strokes(W, H, bark) * trunk, BARK_D, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=1)
    art = G(art, inner_shade(trunk, -30, 0, 14), RIM, seed=nx(), density=0.25, edge=0.2, bloom=0.2, rough=2)
    # knot hole
    hole = shapes(W, H, [ellipse_pts(cx + 14, 560, 16, 24, 12)])
    art = tn(art, hole, "#2a170c", "#3a2414", nx, k=4)
    # roots + moss
    roots = [(curve([(cx - 40, 980), (cx - 140, 1080), (cx - 290, 1130)], 20), 26, (0.0, 0.9)),
             (curve([(cx + 40, 980), (cx + 150, 1080), (cx + 300, 1120)], 20), 24, (0.0, 0.9))]
    art = tn(art, strokes(W, H, roots), BARK, BARK2, nx, k=8, sh=BARK_D)
    moss = trunk * np.clip(fbm(W, H, nx(), 24, 3) * 1.8 - 1.0, 0, 1) * np.clip(np.linspace(0, 1, H, dtype=np.float32)[:, None] * 2 - 0.9, 0, 1)
    art = G(art, moss, "#6f8a3a", "#8eab48", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=3)
    # ground: grassy mound, ferns, mushrooms, little flowers
    ground = hills(W, H, 1110, 18, nx(), 0.7)
    art = tn(art, ground, "#4e7c3c", "#6f9a44", nx, k=10, line_a=0.35)
    fr = []
    for fx, fy, s_, d in [(70, 1120, 1.0, 1), (470, 1110, 1.1, -1), (650, 1120, 0.9, 1), (740, 1110, 0.8, -1)]:
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.45 * d
            tip = (fx + math.cos(a) * 110 * s_, fy + math.sin(a) * 90 * s_)
            stem = curve([(fx, fy), ((fx + tip[0]) / 2 + 10 * d, (fy + tip[1]) / 2 - 10), tip], 16)
            fr.append((stem, 3, (0.05, 0.4)))
            for x, y, ang in along(stem, 9):
                for sg in (-1, 1):
                    fr.append(([(x, y), (x + math.cos(ang + sg * 1.2) * 16 * s_, y + math.sin(ang + sg * 1.2) * 16 * s_)], 4.5 * s_, (0.1, 0.6)))
    art = G(art, strokes(W, H, fr), "#3f6a36", "#6f9a44", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1.5)
    for mx, my, r_ in [(420, 1112, 20), (452, 1118, 13), (110, 1126, 15)]:
        stem = shapes(W, H, [[(mx - 5, my - 2), (mx + 5, my - 2), (mx + 6, my + 22), (mx - 6, my + 22)]], smooth=False)
        art = tn(art, stem, "#f4e6c8", "#ffffff", nx, k=3)
        cap = shapes(W, H, [arc_pts(mx, my, r_, math.pi, 2 * math.pi, 16, 0.75) + [(mx + r_, my + 2), (mx - r_, my + 2)]])
        art = tn(art, cap, "#d9573b", "#e8774f", nx, k=5)
        art = GP(art, circles(W, H, [(mx - r_ * 0.4, my - r_ * 0.35, r_ * 0.14), (mx + r_ * 0.3, my - r_ * 0.45, r_ * 0.12)]), "#fff6e0", seed=nx(), rough=0.3)
    preview(art, "rp-trunk", tone="#f6d79a")
    save_full(art, f"{OUT}/trunk.webp", quality=76)
    clear()

if "ladder" in PARTS:
    W, H = 150, 900
    nx = Seq(700)
    art = blank(W, H)
    l = curve([(30, 0), (34, 450), (40, 890)], 30)
    r = curve([(118, 0), (116, 450), (112, 890)], 30)
    ropes = strokes(W, H, [(l, 6, None), (r, 6, None)])
    art = tn(art, ropes, "#c9a46a", "#e2c48a", nx, k=3, line_a=0.4)
    tw = strokes(W, H, [([(x - 4, y), (x + 4, y + 6)], 1.4, None) for pts_ in (l, r) for (x, y) in pts_[::1]]) * ropes
    art = G(art, tw, "#8a6a3a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    rungs = []
    for y in range(60, 880, 78):
        rungs.append(shapes(W, H, [[(30, y), (118, y + 3), (118, y + 17), (30, y + 14)]], smooth=False))
    rm = np.clip(sum(rungs), 0, 1)
    art = tn(art, rm, PLANK, PLANK2, nx, k=4, sh="#8a5a30")
    preview(art, "rp-ladder", tone="#f6d79a")
    save(art, f"{OUT}/ladder.webp", max_w=150, quality=80)
    clear()

if "sign" in PARTS:
    W, H = 680, 600
    nx = Seq(800); rng = random.Random(8)
    art = blank(W, H)
    board = shapes(W, H, [deform([(14, 18), (666, 10), (672, 588), (8, 592)], rng, 1, 0.01)], smooth=False)
    art = GP(art, board, "#ecc995", "#f5dcae", seed=nx(), rough=1.2, streak=0.8)
    grain = []
    for i in range(46):
        y = rng.uniform(20, 580); x0 = rng.uniform(0, 400)
        grain.append((curve([(x0, y), (x0 + 120, y + rng.uniform(-4, 4)), (x0 + 300, y + rng.uniform(-6, 6))], 20), rng.uniform(0.8, 1.6), (0.2, 0.3)))
    art = G(art, strokes(W, H, grain) * board, "#c08a50", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    seams = strokes(W, H, [([(10, y), (670, y + 2)], 2.4, None) for y in (150, 300, 450)]) * board
    art = G(art, seams, "#8a5a30", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5)
    frame = np.clip(board - shapes(W, H, [[(34, 36), (646, 32), (650, 566), (30, 568)]], smooth=False), 0, 1)
    art = GP(art, frame, "#b07a44", "#c98f52", seed=nx(), rough=0.8, streak=0.8)
    art = G(art, inner_shade(board, 0, -10, 12), "#8a5a30", seed=nx(), density=0.3, edge=0.2, bloom=0, rough=1)
    art = G(art, contour(board, 2.6, nx()), LINE, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    nails = circles(W, H, [(x, y, 5) for x in (22, 658) for y in (22, 300, 578)])
    art = GP(art, nails, "#6a5a4a", "#9a8a7a", seed=nx(), rough=0.3)
    save_full(art, f"{OUT}/sign.webp", quality=72)
    clear()

if "forest" in PARTS:
    W, H = 780, 560
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    layers = [(250, "#d9b98a", "#e6c99a", 0.55, 26), (330, "#a9a070", "#bfb07a", 0.7, 30), (420, "#6f7f4f", "#86915a", 0.85, 36)]
    for base, c1, c2, dens, sz in layers:
        trees = []
        x = rng.uniform(-20, 20)
        while x < W + 40:
            h_ = rng.uniform(90, 180) * (base / 330)
            trees.append(deform([(x - sz, base + 60), (x - sz * 0.6, base - h_ * 0.4), (x, base - h_), (x + sz * 0.6, base - h_ * 0.4), (x + sz, base + 60)], rng, 2, 0.06))
            x += rng.uniform(sz * 1.1, sz * 1.9)
        m = np.clip(shapes(W, H, trees) + shapes(W, H, [[(0, base + 20), (W, base + 20), (W, H), (0, H)]], smooth=False), 0, 1)
        art = G(art, m, c1, c2, seed=nx(), density=dens, edge=0.45, bloom=0.4, rough=6)
    # sun rays
    rays = shapes(W, H, [[(700, 0), (740, 0), (420, H), (330, H)], [(620, 0), (650, 0), (180, H), (120, H)]], smooth=False)
    art = OV(art, gaussian_filter(rays, 14), lambda m: solid_rgba(m, "#fff1c4", 0.18))
    save_full(art, f"{OUT}/forest.webp", size=(520, 373), quality=70)
    preview(art, "rp-forest", tone="#f6d79a")
    clear()

if "bunting" in PARTS:
    W, H = 560, 120
    nx = Seq(990)
    art = blank(W, H)
    path = curve([(10, 20), (140, 44), (280, 52), (420, 44), (550, 20)], 50)
    art = G(art, strokes(W, H, [(path, 2.0, None)]), "#3a2a1c", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    for i, (x, y, a) in enumerate(along(path, 46)):
        c1, c2 = FLAGS[i % 4]
        tri = shapes(W, H, [[(x - 18, y - 1), (x + 18, y + 1), (x + 2, y + 50)]], smooth=False)
        art = tn(art, tri, c1, c2, nx, k=4, line_a=0.45)
        if i % 4 in (0, 2):
            dots = circles(W, H, [(x - 5, y + 12, 3), (x + 6, y + 13, 3), (x + 1, y + 26, 3)]) * tri
            art = GP(art, dots, "#fff6e0", seed=nx(), rough=0.3)
    preview(art, "rp-bunting", tone="#f6eedb")
    save(art, f"{OUT}/bunting.webp", max_w=420, quality=82)
    clear()
