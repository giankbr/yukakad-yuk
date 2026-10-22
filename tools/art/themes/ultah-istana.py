"""Ultah Istana — storybook pen-and-watercolour fairy-tale castle (original design: crooked pastel towers with bent
witch-hat roofs, a heart window, a round wooden door, climbing roses), flower-garden border, pennant, cloud,
butterfly, tiara and a little birthday cake.
Run: python3 -I ultah-istana.py [part ...]  parts: castle garden pennant cloud butterfly tiara cake
Assets -> public/themes/art/ultah-istana/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *

OUT = outdir("ultah-istana")
PARTS = sys.argv[1:] or ["castle", "garden", "pennant", "cloud", "butterfly", "tiara", "cake"]
INK = "#6a4f74"
PINK, MINT, BUTTER, LILAC, PEACH, SKY = "#f4b6c9", "#bfe4d2", "#fbe39a", "#d7c3f0", "#f8c4a4", "#bcd9f4"
LEAF_A_, LEAF_B_ = "#8cc48e", "#4f9a68"


def wash(art, m, col, col2=None, nx=None, dens=0.7, shade=None, k=10, base=True):
    if base:  # opaque white ground so the wash covers what is behind (paper reserved inside the shape)
        art = GP(art, m, "#fffdfb", "#fbf6f2", seed=nx(), rough=1.2, streak=0.2)
    art = G(art, m, col, col2 or mix(col, "#ffffff", 0.3), seed=nx(), density=dens, edge=0.55, bloom=0.4, rough=3, holes=0.03)
    if shade is not None:
        sh = inner_shade(m, int(shade[0] * k), int(shade[1] * k), blur=k)
        art = G(art, sh, mix(col, "#5a3f7a", 0.45), seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=2)
    return art


def ink(art, m, nx, w=2.6, dens=0.8):
    edge = np.clip(soft(m, 0.8) * (1 - soft(m, 0.8)) * 4, 0, 1)
    edge = np.clip(gaussian_filter((edge > 0.35).astype(np.float32), w * 0.35) * 2, 0, 1)
    edge = np.roll(np.roll(edge, 1, 0), 1, 1)  # pen slightly off the wash, like a real sketch
    brk = np.clip((fbm(m.shape[1], m.shape[0], 91, 30, 2) - 0.1) * 5, 0, 1)
    return G(art, edge * brk, INK, seed=nx(), density=dens, edge=0, bloom=0, rough=0.5, feather=0.3)


def cone(tip, base_l, base_r, bend=0.0):
    (tx, ty), (lx, ly), (rx, ry) = tip, base_l, base_r
    mx = (lx + rx) / 2
    L = curve([(lx, ly), (lx + (tx - lx) * 0.45 + bend, ly + (ty - ly) * 0.55), (tx, ty)], 20)
    R = curve([(tx, ty), (rx + (tx - rx) * 0.45 + bend, ry + (ty - ry) * 0.55), (rx, ry)], 20)
    bot = [(rx - 4, ry + 8), (mx, ry + 16), (lx + 4, ly + 8)]
    return L + R[1:] + bot


def arch_win(cx, by, w, h):
    pts = [(cx - w / 2, by), (cx - w / 2, by - h + w / 2)]
    pts += arc_pts(cx, by - h + w / 2, w / 2, math.pi, math.tau, 12)[1:]
    pts += [(cx + w / 2, by)]
    return pts


def heart(cx, cy, s):
    pts = []
    for t in np.linspace(0, math.tau, 40, endpoint=False):
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    return pts


def flower(art, W, H, x, y, r, col, rng, nx, petals=5, eye="#f3c74a"):
    polys = [petal_pts(x, y, r, r * 0.55, k * math.tau / petals + rng.uniform(-.2, .2), n=10) for k in range(petals)]
    m = shapes(W, H, polys)
    art = G(art, m, col, mix(col, "#ffffff", 0.4), seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=1.5, pad=8)
    return G(art, circles(W, H, [(x, y, r * 0.28)]), eye, seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.8, pad=6)


def tulip(art, W, H, x, y, s, col, rng, nx):
    st = strokes(W, H, [(curve([(x, y + s * 3.2), (x + rng.uniform(-6, 6), y + s * 1.6), (x, y)], 12), 3, None)])
    art = G(art, st, LEAF_B_, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1, pad=6)
    lf = shapes(W, H, [petal_pts(x, y + s * 3, s * 2.2, s * 0.45, -math.pi / 2 - 0.4 * rng.choice([-1, 1]), n=10)])
    art = G(art, lf, LEAF_A_, LEAF_B_, seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=1.5, pad=6)
    cup = shapes(W, H, [[(x - s * 0.7, y - s * 0.2), (x - s * 0.75, y - s * 1.2), (x - s * 0.35, y - s * 0.7), (x, y - s * 1.35), (x + s * 0.35, y - s * 0.7), (x + s * 0.75, y - s * 1.2), (x + s * 0.7, y - s * 0.2), (x, y + s * 0.35)]])
    art = G(art, cup, col, mix(col, "#ffffff", 0.35), seed=nx(), density=0.8, edge=0.65, bloom=0.3, rough=1.5, pad=6)
    return art


if "castle" in PARTS:
    W, H = 760, 760
    rng = random.Random(6); nx = Seq(600)
    art = blank(W, H)
    hill = shapes(W, H, [deform([(-40, 760), (-40, 690), (160, 640), (380, 630), (600, 640), (800, 690), (800, 760)], rng, 2, 0.04)])
    art = wash(art, hill, "#b9dfa8", "#d8efc4", nx, dens=0.75)
    # back: left slim tower, right tower
    lt = shapes(W, H, [[(150, 650), (152, 300), (232, 300), (234, 650)]], smooth=False)
    art = wash(art, lt, MINT, nx=nx, shade=(-1, 0), k=12); art = ink(art, lt, nx)
    rt = shapes(W, H, [[(498, 650), (500, 330), (592, 330), (594, 650)]], smooth=False)
    art = wash(art, rt, BUTTER, nx=nx, shade=(-1, 0), k=12); art = ink(art, rt, nx)
    # keep (round tower)
    kp = shapes(W, H, [[(282, 650), (282, 262), (470, 262), (470, 650)]], smooth=False)
    art = wash(art, kp, PINK, nx=nx, shade=(-1, 0), k=18); art = ink(art, kp, nx)
    curv = strokes(W, H, [(curve([(282, 330), (376, 344), (470, 330)], 20), 2, None), (curve([(282, 420), (376, 434), (470, 420)], 20), 2, None)])
    art = G(art, curv, mix(PINK, INK, 0.4), seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    # small bay turret on the keep
    bay = shapes(W, H, [[(452, 470), (452, 392), (512, 392), (512, 470), (482, 492)]], smooth=False)
    art = wash(art, bay, LILAC, nx=nx, shade=(-1, 0), k=8); art = ink(art, bay, nx)
    # roofs (bent witch-hat cones)
    roofs = [(cone((168, 136), (138, 304), (246, 304), bend=-38), PEACH), (cone((566, 186), (488, 334), (604, 334), bend=40), PINK),
             (cone((372, 52), (262, 266), (490, 266), bend=-30), LILAC), (cone((494, 330), (444, 396), (520, 396), bend=14), SKY)]
    roof_masks = []
    for pts, col in roofs:
        m = shapes(W, H, [pts]); roof_masks.append(m)
        art = wash(art, m, col, nx=nx, shade=(-1, 0), k=10)
        art = ink(art, m, nx)
    # stripes on the big lilac roof
    big = roof_masks[2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(xx - 372, yy - 52 + 1e-3)
    stripes = (np.sin(ang * 26) > 0.25).astype(np.float32) * big
    art = G(art, soft(stripes, 0.8), "#a98ad8", seed=nx(), density=0.5, edge=0.3, bloom=0.2, rough=1.5)
    # roof finials: little poles (pennants are separate, animated assets)
    for tx, ty in ((168, 136), (566, 186), (372, 52), (494, 330)):
        pole = strokes(W, H, [([(tx, ty + 4), (tx, ty - 34)], 3, None)])
        art = G(art, pole, INK, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.6, feather=0.5)
        art = G(art, circles(W, H, [(tx, ty - 36, 5)]), "#f0c24a", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.5)
    # front gatehouse with scalloped battlements
    gate = shapes(W, H, [[(222, 656), (222, 486), (530, 486), (530, 656)]], smooth=False)
    bumps = circles(W, H, [(x, 486, 17) for x in np.arange(238, 530, 34)])
    gm = np.maximum(gate, bumps * (np.arange(H)[:, None] < 490))
    art = wash(art, gm, "#f3ebf8", "#e7dcf3", nx=nx, shade=(-1, 0), k=14); art = ink(art, gm, nx)
    # door, heart window, windows
    door = shapes(W, H, [arch_win(376, 656, 86, 120)])
    art = wash(art, door, "#d39a6a", "#b77a4c", nx=nx, dens=0.85, shade=(-1, 0), k=6); art = ink(art, door, nx)
    planks = strokes(W, H, [([(376 + dx, 650), (376 + dx, 560)], 1.6, None) for dx in (-22, 0, 22)]) * door
    art = G(art, planks, "#7a4a2c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8)
    art = G(art, circles(W, H, [(398, 612, 5)]), "#f0c24a", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.5)
    hw = shapes(W, H, [heart(376, 520, 26)])
    art = G(art, hw, "#ffd56b", "#ffb3c7", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1); art = ink(art, hw, nx)
    wins = [arch_win(192, 400, 30, 56), arch_win(192, 520, 30, 56), arch_win(546, 440, 32, 56), arch_win(330, 380, 34, 64), arch_win(422, 380, 34, 64), arch_win(482, 456, 24, 40),
            arch_win(270, 600, 30, 48), arch_win(482, 600, 30, 48)]
    for w_ in wins:
        wm = shapes(W, H, [w_])
        art = G(art, wm, "#8c76b8", "#ffd56b", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=1, pad=6)
        art = ink(art, wm, nx, dens=0.55)
    # climbing roses on the left tower + flower boxes
    vine = strokes(W, H, [(curve([(160, 650), (176, 580), (150, 520), (178, 450), (160, 380)], 50), 3, (0.0, 0.3)), (curve([(230, 650), (214, 600), (236, 560)], 20), 2.5, None)])
    art = G(art, vine, LEAF_B_, seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1)
    for k in range(18):
        t = rng.random(); y = 650 - t * 270; x = 166 + 12 * math.sin(t * 9) + rng.uniform(-10, 10)
        art = G(art, shapes(W, H, [petal_pts(x, y, 13, 5, rng.uniform(0, math.tau), n=8)]), LEAF_A_, LEAF_B_, seed=nx(), density=0.75, edge=0.5, bloom=0.2, rough=1, pad=6)
        if k % 2 == 0:
            art = flower(art, W, H, x + rng.uniform(-5, 5), y + rng.uniform(-5, 5), 8, rng.choice(["#f07fa6", "#f6a6c0", "#fff1f5"]), rng, nx)
    for bx, by in ((270, 606), (482, 606)):
        box = shapes(W, H, [[(bx - 24, by + 4), (bx + 24, by + 4), (bx + 20, by + 18), (bx - 20, by + 18)]], smooth=False)
        art = G(art, box, "#c98f62", seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.8, pad=6)
        for j in range(4):
            art = flower(art, W, H, bx - 16 + j * 11, by + rng.uniform(-2, 3), 6, rng.choice(["#f07fa6", "#ffd56b", "#b694e6"]), rng, nx)
        clear()
    # path + bushes
    path = shapes(W, H, [[(342, 654), (410, 654), (500, 770), (252, 770)]], smooth=False)
    art = wash(art, path, "#f2e2c4", nx=nx, dens=0.7)
    stones = ellipses(W, H, [(376 + (rng.random() - 0.5) * (40 + (y - 660) * 1.6), y, 9 + (y - 660) * 0.08, 4 + (y - 660) * 0.04, 0) for y in np.arange(668, 760, 9) for _ in range(2)])
    art = G(art, stones * path, "#d8c09a", seed=nx(), density=0.5, edge=0.6, bloom=0, rough=1)
    for bx in (110, 250, 520, 650):
        bm = shapes(W, H, [deform(ellipse_pts(bx, 668, 70, 36, 14), rng, 2, 0.08)])
        art = wash(art, bm, "#9fd29a", LEAF_B_, nx=nx, dens=0.8, shade=(-1, -1), k=10)
        for j in range(6):
            art = flower(art, W, H, bx + rng.uniform(-50, 50), 664 + rng.uniform(-22, 12), rng.uniform(6, 9), rng.choice(["#f07fa6", "#ffd56b", "#ffffff", "#b694e6"]), rng, nx)
        clear()
    fade = np.clip(np.minimum(np.arange(W), W - 1 - np.arange(W)) / 90.0, 0, 1)[None, :] ** 0.8
    art[..., 3] *= fade
    preview(art, "ui-castle", tone="#fff7fb")
    save_full(art, f"{OUT}/castle.webp", size=(560, 560), quality=80)
    clear()

if "garden" in PARTS:
    W, H = 780, 220
    rng = random.Random(16); nx = Seq(1600)
    art = blank(W, H)
    grass = shapes(W, H, [deform([(-20, 220), (-20, 170), (200, 150), (420, 160), (620, 146), (800, 168), (800, 220)], rng, 2, 0.05)])
    art = wash(art, grass, "#b9dfa8", "#8cc48e", nx=nx, dens=0.8)
    blades = strokes(W, H, [([(x, 180 + rng.uniform(-6, 10)), (x + rng.uniform(-6, 6), 150 + rng.uniform(-20, 0))], 2.2, (0, 0.6)) for x in np.arange(0, W, 9)])
    art = G(art, blades, LEAF_B_, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    for k in range(18):
        x = 20 + k * 43 + rng.uniform(-12, 12)
        if k % 3 == 0:
            art = tulip(art, W, H, x, rng.uniform(70, 100), rng.uniform(13, 16), rng.choice([PINK, "#f07fa6", PEACH, "#b694e6"]), rng, nx)
        else:
            st = strokes(W, H, [(curve([(x, 180), (x + rng.uniform(-8, 8), 140), (x, rng.uniform(100, 130))], 12), 2.4, None)])
            art = G(art, st, LEAF_B_, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1, pad=6)
            art = flower(art, W, H, x, rng.uniform(100, 130), rng.uniform(11, 15), rng.choice(["#ffffff", "#ffd56b", "#f6a6c0", SKY, "#b694e6"]), rng, nx, petals=rng.choice([5, 6, 8]))
        if k % 4 == 3:
            clear()
    preview(art, "ui-garden", tone="#fff7fb")
    save(art, f"{OUT}/garden.webp", max_w=780, quality=80)
    clear()

if "pennant" in PARTS:
    W, H = 160, 90
    nx = Seq(2000); rng = random.Random(20)
    art = blank(W, H)
    m = shapes(W, H, [[(6, 10), (60, 18), (150, 28), (118, 44), (150, 64), (60, 70), (6, 78)]])
    art = wash(art, m, "#f07fa6", "#f6a6c0", nx=nx, dens=0.85, shade=(0, -1), k=6)
    art = G(art, strokes(W, H, [(curve([(16, 44), (70, 40), (120, 46)], 16), 5, None)]) * m, "#fff1f5", seed=nx(), density=0.7, edge=0.3, bloom=0, rough=1)
    art = ink(art, m, nx, dens=0.55)
    preview(art, "ui-pennant", tone="#fff7fb")
    save_full(art, f"{OUT}/pennant.webp", size=(80, 45), quality=84)

if "cloud" in PARTS:
    W, H = 420, 220
    nx = Seq(2200); rng = random.Random(22)
    art = blank(W, H)
    m = np.maximum(circles(W, H, [(90, 140, 50), (160, 105, 62), (240, 95, 58), (310, 125, 52), (360, 150, 34)]), shapes(W, H, [[(50, 175), (380, 175), (380, 150), (50, 150)]], smooth=False))
    m = np.clip(displace(m, 23, 3, 20), 0, 1)
    art = G(art, m, "#ffffff", "#f3eefb", seed=nx(), density=0.95, edge=0.25, bloom=0.2, rough=4)
    art = G(art, inner_shade(m, 0, -12, 12), "#c9bfe6", seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=3)
    art = ink(art, m, nx, dens=0.35)
    preview(art, "ui-cloud", tone="#e6f1fb")
    save(art, f"{OUT}/cloud.webp", max_w=220, quality=82)

if "butterfly" in PARTS:
    W, H = 160, 130
    nx = Seq(2400); rng = random.Random(24)
    art = blank(W, H)
    for side in (-1, 1):
        up = shapes(W, H, [deform(ellipse_pts(80 + side * 34, 50, 34, 30, 14, side * 0.5), rng, 1, 0.04)])
        lo = shapes(W, H, [deform(ellipse_pts(80 + side * 24, 88, 22, 24, 12, -side * 0.4), rng, 1, 0.04)])
        art = wash(art, up, "#b694e6", "#f6a6c0", nx=nx, dens=0.8)
        art = wash(art, lo, "#f6a6c0", "#ffd56b", nx=nx, dens=0.8)
        art = ink(art, np.maximum(up, lo), nx, dens=0.5)
        art = G(art, circles(W, H, [(80 + side * 40, 46, 7)]), "#ffffff", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.6)
    body = shapes(W, H, [ellipse_pts(80, 70, 5, 30, 10)])
    art = G(art, body, INK, seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5)
    art = G(art, strokes(W, H, [(curve([(80, 42), (72, 22), (64, 16)], 8), 1.6, None), (curve([(80, 42), (88, 22), (96, 16)], 8), 1.6, None)]), INK, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    preview(art, "ui-butterfly", tone="#fff7fb")
    save_full(art, f"{OUT}/butterfly.webp", size=(80, 65), quality=84)

if "tiara" in PARTS:
    W, H = 300, 140
    nx = Seq(2600); rng = random.Random(26)
    art = blank(W, H)
    band = strokes(W, H, [(curve([(20, 110), (150, 126), (280, 110)], 30), 12, None)])
    pts = [(30, 112), (70, 66), (100, 100), (125, 48), (150, 22), (175, 48), (200, 100), (230, 66), (270, 112), (150, 124)]
    body = shapes(W, H, [pts])
    holes = circles(W, H, [(150, 60, 18), (70, 88, 12), (230, 88, 12), (110, 104, 8), (190, 104, 8)])
    frame = np.maximum(band, np.clip(body - holes * 0.0, 0, 1))
    art = FO(art, frame, "#e2b552", seed=nx(), emboss=0.8, sparkle=0.1)
    for x, y, r, c in [(150, 60, 14, "#f07fa6"), (70, 84, 9, "#b694e6"), (230, 84, 9, "#b694e6"), (110, 102, 6, SKY), (190, 102, 6, SKY)]:
        gm = circles(W, H, [(x, y, r)])
        art = G(art, gm, c, mix(c, "#ffffff", 0.4), seed=nx(), density=0.9, edge=0.6, bloom=0, rough=0.6, pad=6)
        art = G(art, circles(W, H, [(x - r * 0.35, y - r * 0.35, r * 0.28)]), "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.3, pad=4)
    art = FO(art, circles(W, H, [(150, 26, 6), (70, 66, 4.5), (230, 66, 4.5)]), "#e2b552", seed=nx())
    preview(art, "ui-tiara", tone="#fff7fb")
    save(art, f"{OUT}/tiara.webp", max_w=160, quality=84)

if "cake" in PARTS:
    W, H = 300, 320
    nx = Seq(2800); rng = random.Random(28)
    art = blank(W, H)
    plate = shapes(W, H, [ellipse_pts(150, 296, 120, 16, 18)])
    art = wash(art, plate, "#e7e2f3", nx=nx, dens=0.8); art = ink(art, plate, nx, dens=0.4)
    t1 = shapes(W, H, [[(50, 296), (50, 210), (250, 210), (250, 296)]], smooth=False)
    t2 = shapes(W, H, [[(84, 212), (84, 146), (216, 146), (216, 212)]], smooth=False)
    art = wash(art, t1, PINK, nx=nx, dens=0.8, shade=(-1, 0), k=12); art = ink(art, t1, nx, dens=0.5)
    art = wash(art, t2, LILAC, nx=nx, dens=0.8, shade=(-1, 0), k=10); art = ink(art, t2, nx, dens=0.5)
    drip1 = shapes(W, H, [[(50, 210), (250, 210), (250, 226)] + [(250 - k * 20, 226 + (14 if k % 2 else 0)) for k in range(11)]], smooth=True)
    drip2 = shapes(W, H, [[(84, 146), (216, 146), (216, 160)] + [(216 - k * 13, 160 + (11 if k % 2 else 0)) for k in range(11)]], smooth=True)
    for d in (drip1, drip2):
        art = wash(art, d, "#ffffff", "#fff3f7", nx=nx, dens=0.95); art = ink(art, d, nx, dens=0.45)
    dots = circles(W, H, [(x, y, 4) for x, y in [(80, 260), (120, 272), (165, 258), (210, 270), (110, 186), (150, 194), (190, 184)]])
    art = G(art, dots, "#ffd56b", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5)
    for k, x in enumerate(np.linspace(100, 200, 6)):
        c = shapes(W, H, [[(x - 4, 146), (x - 4, 100), (x + 4, 100), (x + 4, 146)]], smooth=False)
        art = G(art, c, [SKY, PINK, BUTTER, MINT, LILAC, PEACH][k], seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5)
        fl = shapes(W, H, [petal_pts(x, 98, 18, 6, -math.pi / 2, n=10)])
        art = G(art, glow(fl, "#ffe39a", 6, 0.5)[..., 3], "#ffe39a", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
        art = G(art, fl, "#ffb23a", "#ffe066", seed=nx(), density=0.95, edge=0.5, bloom=0, rough=0.5)
    preview(art, "ui-cake", tone="#fff7fb")
    save(art, f"{OUT}/cake.webp", max_w=180, quality=84)

kb(OUT)
