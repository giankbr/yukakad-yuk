"""Ultah Kucing — kids birthday with original cartoon cats (gouache + crayon line): Oyen the orange tabby in a cardboard
box, Mochi the grey-white cat hugging a yarn ball, Kiko the black kitten peeking, a fish-shaped birthday cake, yarn
balls and paw prints.
Run: python3 -I ultah-kucing.py [part ...]  parts: boxcat yarncat peek cake yarn paw
Assets -> public/themes/art/ultah-kucing/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g2_lib import *

OUT = outdir("ultah-kucing")
PARTS = sys.argv[1:] or ["boxcat", "yarncat", "peek", "cake", "yarn", "paw"]
INK = "#3a2a24"
OR, OR_D, OR_L = "#f3a04a", "#d4762c", "#fbc98a"
GR, GR_D, GR_L = "#a9adb8", "#7d818e", "#d3d6de"
WH, WH_D = "#fbf6ee", "#ddd3c4"
BK, BK_D, BK_L = "#3b3640", "#26222a", "#5b5562"
PINK, PINK_D = "#f59ab0", "#d9607d"
TEAL, TEAL_D, TEAL_L = "#3aa6a0", "#2a7f7a", "#7fd0c8"
MUST, MUST_D = "#f2b84b", "#c98a22"
BOX, BOX_D, BOX_L = "#c98f55", "#9c6a3a", "#e0b07a"


def body_paint(art, m, col, col2, dark, light, nx, light_dir=(-12, -14), outline=True):
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.45)
    art = tint(art, side_light(m, *light_dir, 9), dark, 0.7, seed=nx())
    art = tint(art, side_light(m, -light_dir[0] * .7, -light_dir[1] * .7, 7), light, 0.5, seed=nx())
    if outline:
        art = crayon(art, inner_edge(m, 2.2), mix(dark, INK, 0.5), seed=nx(), amt=0.8, tooth=0.25)
    return art


def ink(art, W, H, items, nx, col=INK, amt=0.9):
    return crayon(art, strokes(W, H, items), col, seed=nx(), amt=amt, tooth=0.2)


def face(art, W, H, cx, cy, s, nx, happy=False, nose=PINK):
    """Cat face features centred on (cx, cy): eyes, pink nose, w-mouth, blush, whiskers."""
    if happy:
        art = ink(art, W, H, [(arc_pts(cx - 20 * s, cy + 2 * s, 9 * s, math.pi * 1.1, math.pi * 1.9, 12), 3.2 * s, (0.2, 0.2)),
                              (arc_pts(cx + 20 * s, cy + 2 * s, 9 * s, math.pi * 1.1, math.pi * 1.9, 12), 3.2 * s, (0.2, 0.2))], nx)
    else:
        for ex in (-20, 20):
            art = GP(art, ellipses(W, H, [(cx + ex * s, cy, 7.5 * s, 9 * s, 0)]), "#2a1f1c", seed=nx(), rough=0.4, pad=6)
            art = OV(art, circles(W, H, [(cx + ex * s - 2.4 * s, cy - 3.2 * s, 2.8 * s)]), lambda m: col_arr(m, "#ffffff", m), pad=4)
    art = GP(art, shapes(W, H, [[(cx - 5 * s, cy + 12 * s), (cx + 5 * s, cy + 12 * s), (cx, cy + 18 * s)]]), nose, seed=nx(), rough=0.3, pad=6)
    art = ink(art, W, H, [(arc_pts(cx - 5 * s, cy + 19 * s, 5 * s, 0.1, math.pi * 0.9, 10), 2.4 * s, None),
                          (arc_pts(cx + 5 * s, cy + 19 * s, 5 * s, 0.1, math.pi * 0.9, 10), 2.4 * s, None)], nx)
    art = G(art, circles(W, H, [(cx - 32 * s, cy + 14 * s, 8 * s), (cx + 32 * s, cy + 14 * s, 8 * s)]), "#f59aa0", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=2, feather=2.5)
    wh = []
    for side in (-1, 1):
        for k, dy in enumerate((-3, 4)):
            wh.append(([(cx + side * 28 * s, cy + (14 + dy) * s), (cx + side * 56 * s, cy + (10 + dy * 2.2) * s)], 1.6 * s, (0.1, 0.5)))
    return ink(art, W, H, wh, nx, col=mix(INK, "#ffffff", 0.25), amt=0.7)


def head_masks(W, H, cx, cy, s, rng, ear_tilt=0.0):
    head = shapes(W, H, [deform(ellipse_pts(cx, cy, 62 * s, 52 * s, 18), rng, 1, 0.015)])
    ears, inner = [], []
    for side in (-1, 1):
        bx = cx + side * 38 * s
        tip = (cx + side * (52 + ear_tilt) * s, cy - 76 * s)
        ears.append([(bx - 22 * s, cy - 28 * s), tip, (bx + 22 * s, cy - 38 * s)] if side < 0 else [(bx - 22 * s, cy - 38 * s), tip, (bx + 22 * s, cy - 28 * s)])
        inner.append([(bx - 11 * s, cy - 36 * s), (cx + side * (49 + ear_tilt) * s, cy - 64 * s), (bx + 11 * s, cy - 40 * s)])
    return head, shapes(W, H, ears), shapes(W, H, inner)


if "boxcat" in PARTS:
    W, H = 520, 560
    nx = Seq(60100); rng = random.Random(3)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(260, 528, 220, 18, 20)]), "#6b4a30", seed=nx(), density=0.28, edge=0.05, bloom=0, rough=3, feather=6)
    # box back flaps + inner back wall
    back = shapes(W, H, [[(96, 300), (424, 300), (410, 330), (110, 330)]], smooth=False)
    art = body_paint(art, back, BOX_D, "#8a5c30", "#6e4622", BOX, nx, outline=False)
    flapL = shapes(W, H, [[(96, 300), (40, 236), (60, 226), (150, 300)]], smooth=False)
    flapR = shapes(W, H, [[(370, 300), (470, 222), (488, 236), (424, 300)]], smooth=False)
    art = body_paint(art, np.clip(flapL + flapR, 0, 1), BOX_L, BOX, BOX_D, "#f0c894", nx)
    # cat body + head (sitting inside the box)
    body = shapes(W, H, [deform(ellipse_pts(260, 310, 92, 80, 18), rng, 1, 0.02)])
    art = body_paint(art, body, OR, "#f5ac5c", OR_D, OR_L, nx)
    chest = shapes(W, H, [deform(ellipse_pts(260, 300, 46, 46, 14), rng, 1, 0.03)]) * body
    art = body_paint(art, chest, WH, "#fff9f0", WH_D, "#ffffff", nx, outline=False)
    hx, hy = 260, 186
    head, ears, inner = head_masks(W, H, hx, hy, 1.15, rng)
    art = body_paint(art, ears, OR, OR, OR_D, OR_L, nx)
    art = GP(art, inner, PINK, "#f7b0c0", seed=nx(), rough=0.6, pad=6)
    art = body_paint(art, head, OR, "#f5ac5c", OR_D, OR_L, nx)
    muzzle = shapes(W, H, [deform(ellipse_pts(hx, hy + 22, 34, 22, 14), rng, 1, 0.03)])
    art = GP(art, muzzle, WH, "#fff9f0", seed=nx(), rough=0.8)
    # tabby stripes
    st = [([(hx - 10 + k * 10, hy - 56), (hx - 8 + k * 9, hy - 34)], 7, (0.0, 0.7)) for k in range(3)]
    st += [([(hx - 62, hy + 2 + k * 12), (hx - 44, hy + 4 + k * 12)], 6, (0.0, 0.7)) for k in range(2)]
    st += [([(hx + 62, hy + 2 + k * 12), (hx + 44, hy + 4 + k * 12)], 6, (0.0, 0.7)) for k in range(2)]
    st += [([(196, 280 + k * 22), (216, 286 + k * 22)], 8, (0.0, 0.7)) for k in range(3)] + [([(324, 280 + k * 22), (304, 286 + k * 22)], 8, (0.0, 0.7)) for k in range(3)]
    art = GP(art, strokes(W, H, st) * np.clip(head + body, 0, 1), OR_D, "#c96a26", seed=nx(), rough=0.6, pad=6)
    art = face(art, W, H, hx, hy + 2, 1.15, nx)
    # party hat
    hat = shapes(W, H, [[(hx - 30, hy - 48), (hx + 26, hy - 56), (hx - 8, hy - 132)]], smooth=False)
    art = body_paint(art, hat, TEAL, "#45b3ac", TEAL_D, TEAL_L, nx)
    dots_ = circles(W, H, [(hx - 10, hy - 70, 5), (hx + 4, hy - 88, 4), (hx - 12, hy - 104, 3.5), (hx + 10, hy - 64, 4)]) * hat
    art = GP(art, dots_, MUST, seed=nx(), rough=0.3, pad=6)
    art = body_paint(art, circles(W, H, [(hx - 8, hy - 134, 10)]), PINK, "#f7b0c0", PINK_D, "#ffd0dc", nx)
    # box front + side
    front = shapes(W, H, [deform([(90, 330), (430, 330), (420, 520), (100, 520)], rng, 1, 0.004)], smooth=False)
    side = shapes(W, H, [[(430, 330), (470, 300), (460, 490), (420, 520)]], smooth=False)
    art = body_paint(art, side, BOX_D, "#8a5c30", "#6e4622", BOX, nx)
    art = body_paint(art, front, BOX, "#cf9a62", BOX_D, BOX_L, nx, light_dir=(10, -10))
    corr = strokes(W, H, [([(100 + k * 10, 336), (104 + k * 10, 514)], 1.2, None) for k in range(32)]) * front
    art = OV(art, corr, lambda m: col_arr(m, "#8a5c30", m * 0.18), pad=4)
    tape = shapes(W, H, [[(230, 330), (290, 330), (292, 420), (228, 420)]], smooth=False)
    art = GP(art, tape, "#e9cf9a", "#efd9ad", seed=nx(), rough=0.6, pad=6, density=0.8)
    art = ink(art, W, H, [([(150, 440), (176, 440)], 4, None), ([(150, 456), (200, 456)], 4, None), ([(350, 470), (368, 486), (386, 470)], 3.5, None)], nx, col="#7a4e28", amt=0.6)
    # paws hooked over the box rim
    paws = ellipses(W, H, [(208, 334, 26, 16, -8), (312, 334, 26, 16, 8)])
    art = body_paint(art, paws, OR, "#f5ac5c", OR_D, OR_L, nx)
    art = ink(art, W, H, [([(x + d, 340), (x + d, 348)], 2.4, None) for x in (208, 312) for d in (-8, 0, 8)], nx, amt=0.7)
    # tail curling out over the side
    tail = strokes(W, H, [(curve([(410, 320), (470, 300), (492, 250), (470, 214)], 30), 22, (0.0, 0.25))])
    art = body_paint(art, tail * (1 - front), OR, "#f5ac5c", OR_D, OR_L, nx)
    art = GP(art, strokes(W, H, [([(486, 254), (466, 256)], 7, None), ([(484, 228), (466, 236)], 7, None)]) * tail, OR_D, seed=nx(), rough=0.4, pad=6)
    preview(art, "boxcat")
    save(art, f"{OUT}/boxcat.webp", max_w=440, quality=82)
    clear()

if "yarncat" in PARTS:
    W, H = 560, 380
    nx = Seq(60200); rng = random.Random(5)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(280, 352, 240, 14, 20)]), "#6b4a30", seed=nx(), density=0.25, edge=0.05, bloom=0, rough=3, feather=6)
    # Mochi lying on her belly, front paws around a yarn ball, tail up
    body = shapes(W, H, [deform(ellipse_pts(300, 300, 140, 54, 20, 0.0), rng, 1, 0.015)])
    tail = strokes(W, H, [(curve([(420, 296), (476, 276), (504, 220), (492, 170)], 30), 26, (0.0, 0.3))])
    art = body_paint(art, tail, GR, GR, GR_D, GR_L, nx)
    art = GP(art, strokes(W, H, [(curve([(498, 206), (504, 186), (492, 170)], 10), 26, (0.0, 0.3))]) * tail, WH, seed=nx(), rough=0.5, pad=6)
    art = body_paint(art, body, GR, "#b3b7c1", GR_D, GR_L, nx)
    patch = shapes(W, H, [deform(ellipse_pts(280, 330, 90, 26, 14), rng, 1, 0.04)]) * body
    art = GP(art, patch, WH, "#fff9f0", seed=nx(), rough=0.8)
    hx, hy = 196, 240
    head, ears, inner = head_masks(W, H, hx, hy, 1.0, rng, ear_tilt=-4)
    art = body_paint(art, ears, GR, GR, GR_D, GR_L, nx)
    art = GP(art, inner, PINK, "#f7b0c0", seed=nx(), rough=0.6, pad=6)
    art = body_paint(art, head, GR, "#b3b7c1", GR_D, GR_L, nx)
    blaze = shapes(W, H, [[(hx - 10, hy - 50), (hx + 10, hy - 50), (hx + 30, hy + 40), (hx - 30, hy + 40)]]) * head
    art = GP(art, blaze, WH, "#fff9f0", seed=nx(), rough=0.8)
    art = face(art, W, H, hx, hy + 2, 1.0, nx, happy=True)
    # yarn ball
    yx, yy_, yr = 96, 306, 48
    ball = circles(W, H, [(yx, yy_, yr)])
    art = body_paint(art, ball, PINK, "#f7a8bc", PINK_D, "#ffd0dc", nx)
    wr = []
    for k in range(7):
        a = k * 0.45 + 0.3
        wr.append((arc_pts(yx, yy_, yr * 0.95, a, a + 2.6, 24, squash=0.45 + 0.08 * k), 2.6, None))
    yl = np.clip(strokes(W, H, wr) * ball, 0, 1)
    yyg, xxg = np.mgrid[0:H, 0:W].astype(np.float32)
    rot = np.clip(yl, 0, 1)
    art = OV(art, rot, lambda m: col_arr(m, PINK_D, m * 0.55), pad=4)
    # loose strand trailing right
    strand = curve([(yx + 30, yy_ + 40), (200, 360), (330, 362), (420, 356), (548, 330)], 60)
    art = ink(art, W, H, [(strand, 3.4, (0.0, 0.1))], nx, col=PINK_D, amt=0.85)
    # paws hugging the ball
    paws = ellipses(W, H, [(132, 284, 22, 14, -30), (136, 334, 22, 14, 20)])
    art = body_paint(art, paws, WH, "#fff9f0", WH_D, "#ffffff", nx)
    preview(art, "yarncat")
    save(art, f"{OUT}/yarncat.webp", max_w=460, quality=82)
    clear()

if "peek" in PARTS:
    # Kiko, a black kitten with white muzzle, peeking over an edge (head + two paws)
    W, H = 300, 220
    nx = Seq(60300); rng = random.Random(7)
    art = blank(W, H)
    hx, hy = 150, 132
    head, ears, inner = head_masks(W, H, hx, hy, 1.0, rng)
    art = body_paint(art, ears, BK, BK, BK_D, BK_L, nx)
    art = GP(art, inner, PINK, "#f7b0c0", seed=nx(), rough=0.6, pad=6)
    art = body_paint(art, head, BK, "#45404a", BK_D, BK_L, nx)
    muzzle = shapes(W, H, [deform(ellipse_pts(hx, hy + 22, 30, 20, 14), rng, 1, 0.03)])
    art = GP(art, muzzle, WH, "#fff9f0", seed=nx(), rough=0.8)
    for ex in (-20, 20):
        art = GP(art, ellipses(W, H, [(hx + ex, hy, 11, 12, 0)]), "#f4d35c", seed=nx(), rough=0.4, pad=6)
        art = GP(art, ellipses(W, H, [(hx + ex, hy, 4.5, 10, 0)]), "#1a1418", seed=nx(), rough=0.3, pad=6)
        art = OV(art, circles(W, H, [(hx + ex - 3, hy - 4, 2.6)]), lambda m: col_arr(m, "#ffffff", m), pad=4)
    art = GP(art, shapes(W, H, [[(hx - 5, hy + 13), (hx + 5, hy + 13), (hx, hy + 19)]]), PINK, seed=nx(), rough=0.3, pad=6)
    art = ink(art, W, H, [(arc_pts(hx - 5, hy + 20, 5, 0.1, math.pi * 0.9, 10), 2.4, None), (arc_pts(hx + 5, hy + 20, 5, 0.1, math.pi * 0.9, 10), 2.4, None)], nx)
    wh = [([(hx + sd * 26, hy + 16 + dy), (hx + sd * 58, hy + 12 + dy * 2.2)], 1.6, (0.1, 0.5)) for sd in (-1, 1) for dy in (-3, 4)]
    art = ink(art, W, H, wh, nx, col="#e9e2d8", amt=0.8)
    paws = ellipses(W, H, [(96, 196, 26, 16, -6), (204, 196, 26, 16, 6)])
    art = body_paint(art, paws, WH, "#fff9f0", WH_D, "#ffffff", nx)
    art = ink(art, W, H, [([(x + d, 202), (x + d, 210)], 2.2, None) for x in (96, 204) for d in (-8, 0, 8)], nx, amt=0.6)
    art[205:] = 0
    preview(art, "peek")
    save(art, f"{OUT}/peek.webp", max_w=220, quality=82)
    clear()

if "cake" in PARTS:
    W, H = 480, 340
    nx = Seq(60400); rng = random.Random(9)
    art = blank(W, H)
    plate = shapes(W, H, [ellipse_pts(240, 300, 220, 26, 24)])
    art = body_paint(art, plate, "#bfe3df", "#a9d6d0", "#78b2ad", "#e2f4f1", nx, outline=False)
    # fish body (teal sponge with cream frosting scales), tail fin right, mouth left
    body = shapes(W, H, [[(60, 220), (110, 160), (200, 136), (300, 150), (360, 196), (360, 240), (300, 280), (200, 292), (110, 276)]])
    tail = shapes(W, H, [[(346, 214), (440, 150), (452, 170), (420, 222), (452, 276), (440, 294)]])
    art = body_paint(art, tail, MUST, "#f5c565", MUST_D, "#fbe0a0", nx)
    art = GP(art, strokes(W, H, [([(360, 218), (432, 168)], 3, None), ([(360, 222), (440, 222)], 3, None), ([(360, 228), (432, 280)], 3, None)]) * tail, MUST_D, seed=nx(), rough=0.4, pad=6, density=0.7)
    art = body_paint(art, body, TEAL, "#45b3ac", TEAL_D, TEAL_L, nx)
    # side layer showing sponge
    layer = shapes(W, H, [[(70, 236), (360, 236), (350, 250), (300, 280), (200, 292), (110, 276)]]) * body
    art = GP(art, layer, "#f6e2c4", "#efd3aa", seed=nx(), rough=0.8)
    art = GP(art, strokes(W, H, [([(80, 252), (340, 252)], 4, None)]) * layer, PINK, seed=nx(), rough=0.4, pad=6)
    # piped scales
    sc = []
    for row, y in enumerate((170, 196, 222)):
        for k in range(6):
            x = 170 + k * 30 + (15 if row % 2 else 0)
            if x < 345:
                sc.append((arc_pts(x, y, 14, 0.15, math.pi - 0.15, 12), 4, None))
    art = GP(art, strokes(W, H, sc) * body, "#fff6e6", seed=nx(), rough=0.4, pad=6)
    # face: big round eye, smile
    art = GP(art, circles(W, H, [(116, 200, 18)]), "#fff6e6", seed=nx(), rough=0.4, pad=6)
    art = GP(art, circles(W, H, [(120, 202, 9)]), "#2a1f1c", seed=nx(), rough=0.3, pad=6)
    art = OV(art, circles(W, H, [(117, 198, 3)]), lambda m: col_arr(m, "#ffffff", m), pad=4)
    art = ink(art, W, H, [(arc_pts(84, 222, 12, 0.2, 1.6, 10), 3, None)], nx)
    art = G(art, circles(W, H, [(140, 230, 9)]), "#f59aa0", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=2, feather=2.5)
    # candles
    for k, (x, c) in enumerate(((190, PINK), (232, MUST), (274, "#b9a3e3"), (316, TEAL_L))):
        top = 84 + (k % 2) * 8
        base_y = 150 + abs(x - 250) * 0.15
        cm = shapes(W, H, [[(x - 6, base_y), (x - 6, top), (x + 6, top), (x + 6, base_y)]], smooth=False)
        art = GP(art, cm, c, seed=nx(), rough=0.5, pad=6)
        art = GP(art, strokes(W, H, [([(x - 6, top + j), (x + 6, top + j - 6)], 2.4, None) for j in range(10, int(base_y - top), 14)]) * cm, "#ffffff", seed=nx(), rough=0.3, pad=6, density=0.8)
        fl = shapes(W, H, [petal_pts(x, top - 4, 24, 8, -math.pi / 2 + rng.uniform(-.15, .15), n=12)])
        art = OV(art, fl, lambda m: col_arr(m, "#ffd45c", np.clip(gaussian_filter(m, 7) * 1.4, 0, 1) * 0.35), pad=20)
        art = GP(art, fl, "#ffb43c", "#ff8a3c", seed=nx(), rough=0.5, pad=6)
        art = GP(art, shapes(W, H, [petal_pts(x, top - 6, 12, 4, -math.pi / 2, n=10)]), "#fff2b8", seed=nx(), rough=0.3, pad=6)
    preview(art, "cake")
    save(art, f"{OUT}/cake.webp", max_w=360, quality=82)
    clear()

if "yarn" in PARTS:
    for name, (c, cd, cl) in (("yarn", (TEAL, TEAL_D, TEAL_L)), ("yarn2", (MUST, MUST_D, "#fbe0a0"))):
        W, H = 220, 200
        nx = Seq(60500 + len(name)); rng = random.Random(len(name))
        art = blank(W, H)
        yx, yy_, yr = 100, 104, 70
        ball = circles(W, H, [(yx, yy_, yr)])
        art = body_paint(art, ball, c, c, cd, cl, nx)
        wr = []
        for k in range(9):
            a = k * 0.5 + rng.uniform(0, .3)
            wr.append((arc_pts(yx, yy_, yr * 0.96, a, a + 2.4, 28, squash=0.3 + 0.08 * k), 3.2, None))
        wr.append((arc_pts(yx, yy_, yr * 0.9, -1.2, 1.4, 24, squash=1.0), 3.2, None))
        art = OV(art, strokes(W, H, wr) * ball, lambda m: col_arr(m, cd, m * 0.6), pad=4)
        art = OV(art, np.roll(strokes(W, H, wr) * ball, -2, 0), lambda m: col_arr(m, cl, m * 0.4), pad=4)
        strand = curve([(yx + 50, yy_ + 50), (190, 190), (214, 150), (200, 120)], 30)
        art = ink(art, W, H, [(strand, 3.4, (0.0, 0.2))], nx, col=cd, amt=0.85)
        preview(art, name)
        save(art, f"{OUT}/{name}.webp", max_w=140, quality=82)
        clear()

if "paw" in PARTS:
    W, H = 120, 120
    nx = Seq(60600); rng = random.Random(1)
    m = np.clip(ellipses(W, H, [(60, 74, 26, 21, 0)]) + circles(W, H, [(30, 44, 11), (50, 30, 11), (72, 30, 11), (92, 44, 11)]), 0, 1)
    art = GP(blank(W, H), m, PINK, "#f7a8bc", seed=nx(), rough=1.2, streak=0.6)
    art = tint(art, side_light(m, 3, 4, 3), PINK_D, 0.5, seed=nx())
    preview(art, "paw")
    save(art, f"{OUT}/paw.webp", max_w=60, quality=82)
