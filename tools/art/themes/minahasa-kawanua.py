"""Minahasa Kawanua — red/black/gold: kain bentenan woven at thread level (stepped lozenges, sinoi stripes, zigzag
bands, gold supplementary weft), rumah panggung kayu Woloan (gouache: plank walls, carved cream gable, twin front
stairs, rust zinc roof) before a watercolour Gunung Lokon, a small gold-foil manguni emblem and a woven divider.
Run: python3 -I minahasa-kawanua.py [part ...]   parts: bentenan rumah manguni divider
Assets -> public/themes/art/minahasa-kawanua/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b1_lib import *

OUT = outdir("minahasa-kawanua")
PARTS = sys.argv[1:] or ["bentenan", "rumah", "manguni", "divider"]
RED, RED_D, BLACK, GOLD, CREAM = "#a8231f", "#6a1412", "#17100d", "#bf8f3a", "#efe2c6"
PAL = [RED, BLACK, GOLD, CREAM, RED_D]


def bentenan_pattern(cols=60):
    rows = 64
    P = np.zeros((rows, cols), np.int32)
    yy, xx = np.mgrid[0:rows, 0:cols]

    def stripes(r0, seq):
        for k, v in enumerate(seq):
            P[r0 + k] = v
    stripes(0, [1, 2, 1, 3])
    # zigzag band (rows 4-8): red tooth on black
    for r in range(4, 9):
        k = r - 4
        P[r] = np.where(((xx[r] + k) % 10 < 5) ^ ((xx[r] - k) % 10 < 5), 0, 1)
    stripes(9, [1, 2])
    # main band 1 (rows 11-31): red ground, nested stepped lozenges
    r0, r1, cyc = 11, 32, 21
    band = P[r0:r1]; band[:] = 0
    for cx in range(-10, cols + 20, 20):
        for (a, b, v) in [(9, 10, 1), (7, 8, 2), (5, 6, 1), (3, 4, 3), (0, 2, 2)]:
            m = manhattan_ring(r1 - r0, cols, cyc - r0, cx, a, b)
            band[m] = v
        # hooks: little cream steps at the lozenge tips
        for dx in (-12, 12):
            m = manhattan_ring(r1 - r0, cols, cyc - r0, cx + dx, 0, 1)
            band[m & (band == 0)] = 3
    # half lozenges in the gaps (black)
    for cx in range(0, cols + 20, 20):
        for top in (0, r1 - r0 - 1):
            m = manhattan_ring(r1 - r0, cols, top, cx, 0, 3)
            band[m & (band == 0)] = 1
    stripes(32, [1, 3, 1, 2, 2, 1, 3, 1])
    # band 2 (rows 40-55): black ground, red hourglass/X with gold rim, offset half a repeat
    r0, r1 = 40, 56
    b2 = P[r0:r1]; b2[:] = 1
    hh = r1 - r0
    for cx in range(0, cols + 20, 20):
        y, x = np.mgrid[0:hh, 0:cols]
        d = np.abs(x - cx)
        dy = np.abs(y - hh / 2 + 0.5)
        hour = (d <= dy + 1) & (d <= 8)
        rim = (d == dy + 2) & (d <= 9)
        b2[hour] = 0; b2[rim] = 2
        b2[(d <= 1) & (dy <= 1.5)] = 3
    for cx in range(10, cols + 20, 20):
        m = manhattan_ring(hh, cols, hh // 2, cx, 0, 2)
        b2[m] = 2
        m = manhattan_ring(hh, cols, hh // 2, cx, 0, 0)
        b2[m] = 4
    stripes(56, [1, 2, 1])
    for r in range(59, 64):
        k = r - 59
        P[r] = np.where((xx[r] + k * 2) % 6 < 3, 4, 0)
    return P


if "bentenan" in PARTS:
    P = bentenan_pattern()
    tile = weave_cells(P, PAL, cell=6, seed=7, metallic=(2,), float_len=3)
    save_rgb(tile, f"{OUT}/bentenan.webp", quality=80)
    show(tile, "mk-bentenan")
    big = np.concatenate([np.concatenate([tile, tile], 1)] * 2, 0)
    show(big, "mk-bentenan-2x2")
    clear()

if "divider" in PARTS:
    cols, rows = 46, 7
    P = np.full((rows, cols), 0, np.int32)
    P[0] = 1; P[-1] = 1; P[1] = 2; P[-2] = 2
    for cx in range(3, cols, 8):
        m = manhattan_ring(rows, cols, 3, cx, 0, 2)
        P[m & (np.arange(rows)[:, None] >= 2) & (np.arange(rows)[:, None] <= 4)] = 1
        P[3, cx] = 3
    t = weave_cells(P, PAL, cell=6, seed=3, metallic=(2,), float_len=3)
    H, W = t.shape[:2]
    # fringe: loose warp threads hanging off both ends
    fr = 26
    out = np.zeros((H, W + fr * 2, 4), np.float32)
    out[:, fr:fr + W] = t
    rng = random.Random(4)
    items = []
    for y in range(2, H - 1, 3):
        for side in (0, 1):
            x0 = fr if side == 0 else fr + W
            L = rng.uniform(14, 24)
            dx = -L if side == 0 else L
            items.append(([(x0, y), (x0 + dx * 0.5, y + rng.uniform(-1, 1)), (x0 + dx, y + rng.uniform(-2, 2))], 1.6, (0.0, 0.6)))
    fm = strokes(W + fr * 2, H, items)
    out = GP(out, fm, RED, RED_D, seed=5, rough=0.4, streak=0.6, pad=4)
    save(out, f"{OUT}/divider.webp", max_w=400)
    show(out, "mk-divider", bg="#f3ead9")
    clear()

if "manguni" in PARTS:
    W, H = 240, 260
    nx = Seq(500)
    rng = random.Random(9)
    cx = 120
    body = shapes(W, H, [deform([(cx - 62, 120), (cx - 70, 60), (cx - 52, 28), (cx - 30, 46), (cx, 38), (cx + 30, 46), (cx + 52, 28), (cx + 70, 60), (cx + 62, 120),
                                 (cx + 54, 186), (cx + 26, 230), (cx, 238), (cx - 26, 230), (cx - 54, 186)], rng, 1, 0.01)])
    art = GP(blank(W, H), body, BLACK, "#2a1a14", seed=nx(), rough=1.2, streak=0.8)
    # gold rim + facial disc
    rim = outline(body, 6)
    art = FO(art, rim, GOLD, seed=nx(), emboss=0.6, sparkle=0.15)
    disc = shapes(W, H, [[(cx - 54, 70), (cx - 30, 56), (cx, 74), (cx + 30, 56), (cx + 54, 70), (cx + 58, 104), (cx + 30, 126), (cx, 120), (cx - 30, 126), (cx - 58, 104)]])
    art = GP(art, disc, RED, RED_D, seed=nx(), rough=1.0)
    eyes = ring(W, H, cx - 28, 92, 20, 6) + ring(W, H, cx + 28, 92, 20, 6)
    art = FO(art, np.clip(eyes, 0, 1), GOLD, seed=nx(), emboss=0.7)
    pup = circles(W, H, [(cx - 28, 92, 9), (cx + 28, 92, 9)])
    art = GP(art, pup, CREAM, seed=nx(), rough=0.5)
    pup2 = circles(W, H, [(cx - 27, 93, 4.5), (cx + 29, 93, 4.5)])
    art = GP(art, pup2, BLACK, seed=nx(), rough=0.3)
    beak = shapes(W, H, [[(cx - 8, 112), (cx + 8, 112), (cx, 136)]], smooth=False)
    art = FO(art, beak, GOLD, seed=nx(), emboss=0.8)
    # breast feathers: chevron stitches, stepped like the cloth
    items = []
    for row, y in enumerate(range(148, 222, 16)):
        half = 44 - row * 7
        for x in range(cx - half, cx + half + 1, 16):
            items.append(([(x - 6, y - 4), (x, y + 3), (x + 6, y - 4)], 3.2, None))
    feath = strokes(W, H, items) * body
    art = FO(art, feath, GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    # perch
    perch = strokes(W, H, [([(cx - 74, 244), (cx + 74, 244)], 6, (0.1, 0.1))])
    art = FO(art, perch, GOLD, seed=nx(), emboss=0.5)
    claws = strokes(W, H, [([(x, 232), (x + d, 244)], 3, None) for x in (cx - 22, cx - 14, cx + 14, cx + 22) for d in (-3, 3)])
    art = FO(art, claws, GOLD, seed=nx())
    save(art, f"{OUT}/manguni.webp", max_w=200)
    show(art, "mk-manguni", bg=BLACK)
    clear()

if "rumah" in PARTS:
    W, H = 900, 640
    nx = Seq(2000)
    rng = random.Random(11)
    art = blank(W, H)
    # Gunung Lokon: watercolour, cool grey-blue, crater notch
    mt = shapes(W, H, [[(-20, 430), (150, 330), (300, 210), (380, 150), (420, 160), (450, 148), (520, 200), (660, 300), (820, 360), (930, 400), (930, 470), (-20, 470)]])
    art = G(art, mt, "#8796a6", "#6c7d92", seed=nx(), density=0.55, edge=0.6, bloom=0.4, rough=8, feather=2)
    mt2 = shapes(W, H, [[(-20, 450), (120, 400), (260, 380), (420, 390), (600, 360), (760, 390), (930, 380), (930, 480), (-20, 480)]])
    art = G(art, mt2, "#5f7e6a", "#4a6a5a", seed=nx(), density=0.5, edge=0.5, bloom=0.3, rough=8)
    smoke = shapes(W, H, [deform(ellipse_pts(440, 120, 40, 18, 14), rng, 2, 0.1), deform(ellipse_pts(480, 86, 56, 20, 14), rng, 2, 0.1)])
    art = G(art, smoke, "#c9ccd0", seed=nx(), density=0.28, edge=0.3, bloom=0.5, rough=10, feather=4)
    field = shapes(W, H, [deform([(-20, 452), (200, 440), (450, 446), (700, 438), (930, 448), (930, 600), (-20, 600)], rng, 2, 0.02)])
    art = G(art, field, "#a9b77a", "#8fa468", seed=nx(), density=0.5, edge=0.45, bloom=0.5, rough=8)
    # ground strip
    gr = shapes(W, H, [deform([(40, 590), (200, 572), (450, 576), (700, 570), (860, 590), (860, 620), (40, 620)], rng, 1, 0.02)])
    art = G(art, gr, "#5c6b3a", "#7a7f42", seed=nx(), density=0.75, edge=0.5, bloom=0.3, rough=5)
    gr2 = shapes(W, H, [deform([(0, 560), (250, 548), (650, 552), (900, 556), (900, 606), (0, 606)], rng, 2, 0.03)])
    art = G(art, gr2, "#8a9a58", seed=nx(), density=0.35, edge=0.5, bloom=0.5, rough=8)

    cx = 450
    # ---- stilts (tiang) behind
    stilt_xs = [212, 268, 330, 392, 508, 570, 632, 688]
    st = strokes(W, H, [([(x, 418), (x + rng.uniform(-1, 1), 586)], 14, None) for x in stilt_xs])
    art = knockout(art, st, 1.0, 1)
    art = GP(art, st, "#5a3218", "#3a1f0e", seed=nx(), rough=1.0, streak=1.0)
    stl = strokes(W, H, [([(x - 4, 420), (x - 4, 584)], 3, None) for x in stilt_xs])
    art = G(art, stl, "#a06a3c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    braces = strokes(W, H, [([(stilt_xs[i], 440), (stilt_xs[i + 1], 470)], 5, None) for i in range(0, len(stilt_xs) - 1) if i != 3])
    art = GP(art, braces, "#4a2a14", seed=nx(), rough=0.8)
    # ---- floor beam + body walls
    body = rect(W, H, 182, 282, 718, 410)
    beam = rect(W, H, 168, 404, 732, 426)
    art = knockout(art, np.maximum(body, beam), 1.0, 1)
    art = GP(art, body, "#9a5a2c", "#7c4422", seed=nx(), rough=2.4, streak=1.6)
    # vertical plank lines
    pl = strokes(W, H, [([(x + rng.uniform(-.6, .6), 284), (x, 408)], 1.6, None) for x in range(190, 716, 13)]) * body
    art = G(art, pl, "#4a2611", seed=nx(), density=0.65, edge=0, bloom=0, rough=0.4, feather=0.5)
    for k, x in enumerate(range(184, 716, 13)):
        tone = rng.choice(["#b06a34", "#7a4020", "#8c4c26", "#a35e2e"])
        art = G(art, rect(W, H, x, 284, x + 12, 408), tone, seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=1.2, feather=0.6, pad=4)
    grain = fbm(W, H, nx(), 6, 2) * body
    art = G(art, np.clip((grain - 0.6) * 3, 0, 1) * body, "#5b2f14", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.3)
    art = GP(art, beam, "#4a2612", "#2e170a", seed=nx(), rough=0.8)
    # windows with shutters + central door
    wins = []
    for x in (214, 300, 556, 642):
        wins.append((x, 306, x + 46, 386))
    for (x0, y0, x1, y1) in wins:
        frame = rect(W, H, x0 - 6, y0 - 6, x1 + 6, y1 + 6)
        art = GP(art, frame, CREAM, "#d9c9a6", seed=nx(), rough=0.8)
        pane = rect(W, H, x0, y0, x1, y1)
        art = GP(art, pane, "#2a1810", "#1a0e08", seed=nx(), rough=0.6)
        mull = rect(W, H, (x0 + x1) / 2 - 1.5, y0, (x0 + x1) / 2 + 1.5, y1) + rect(W, H, x0, (y0 + y1) / 2 - 1.5, x1, (y0 + y1) / 2 + 1.5)
        art = GP(art, np.clip(mull, 0, 1), CREAM, seed=nx(), rough=0.4)
        # open shutters (red)
        for sx in (x0 - 24, x1 + 6):
            sh = rect(W, H, sx, y0 - 2, sx + 18, y1 + 2)
            art = GP(art, sh, RED, RED_D, seed=nx(), rough=0.8)
            lv = strokes(W, H, [([(sx + 2, yy), (sx + 16, yy)], 1.4, None) for yy in range(y0 + 4, y1, 6)]) * sh
            art = G(art, lv, RED_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3, feather=0.4)
    door = rect(W, H, 412, 300, 488, 408)
    art = GP(art, rect(W, H, 404, 292, 496, 408), CREAM, "#d8c7a2", seed=nx(), rough=0.8)
    art = GP(art, door, RED_D, "#4a0e0c", seed=nx(), rough=0.8)
    dp = strokes(W, H, [([(450, 302), (450, 406)], 2.2, None)]) + strokes(W, H, [([(416, 352), (484, 352)], 2, None)])
    art = G(art, np.clip(dp, 0, 1), "#2a0806", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    # ---- veranda deck with railing in front of the door
    deck = rect(W, H, 360, 404, 540, 418)
    art = GP(art, deck, "#5e3418", seed=nx(), rough=0.6)
    rail = strokes(W, H, [([(360, 372), (400, 372)], 4, None), ([(500, 372), (540, 372)], 4, None)] +
                   [([(x, 372), (x, 404)], 3, None) for x in list(range(362, 402, 9)) + list(range(502, 542, 9))])
    art = GP(art, rail, CREAM, "#cdb994", seed=nx(), rough=0.5)
    # ---- twin stairs: left one descends left, right one descends right (Minahasa signature)
    for side in (-1, 1):
        top = (450 + side * 90, 418)
        bot = (450 + side * 210, 588)
        stringer = strokes(W, H, [([top, bot], 8, None), ([(top[0], top[1] - 34), (bot[0], bot[1] - 34)], 4, None)])
        art = GP(art, stringer, CREAM, "#cbb68f", seed=nx(), rough=0.6)
        posts = strokes(W, H, [([(top[0] + (bot[0] - top[0]) * t, top[1] + (bot[1] - top[1]) * t), (top[0] + (bot[0] - top[0]) * t, top[1] + (bot[1] - top[1]) * t - 34)], 3, None) for t in np.linspace(0, 1, 7)])
        art = GP(art, posts, CREAM, seed=nx(), rough=0.4)
        treads = strokes(W, H, [([(top[0] + (bot[0] - top[0]) * t - 10, top[1] + (bot[1] - top[1]) * t + 4), (top[0] + (bot[0] - top[0]) * t + 10, top[1] + (bot[1] - top[1]) * t + 4)], 4, None) for t in np.linspace(0.06, 0.96, 10)])
        art = GP(art, treads, "#6a3a1a", seed=nx(), rough=0.5)
    # ---- roof: main body + front gable (rust zinc with ribs)
    roof = quad(W, H, [(128, 290), (772, 290), (660, 168), (240, 168)])
    art = knockout(art, roof, 1.0, 1)
    art = GP(art, roof, "#8e2c1e", "#6e2015", seed=nx(), rough=2.6, streak=1.8)
    ribs = strokes(W, H, [([(x, 170), (x + (x - 450) * 0.22, 288)], 1.8, None) for x in range(246, 660, 11)]) * roof
    art = G(art, ribs, "#4a120c", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.5)
    rust = np.clip((fbm(W, H, nx(), 30, 3) - 0.55) * 3, 0, 1) * roof
    art = G(art, rust, "#b0552c", seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=2)
    gable = quad(W, H, [(310, 292), (590, 292), (450, 92)])
    art = knockout(art, gable, 1.0, 1)
    art = GP(art, gable, "#a2602e", "#87502a", seed=nx(), rough=2.2, streak=1.6)
    # carved cream lattice in the gable: concentric triangles + sunburst slats + scalloped fascia
    tri_items = []
    for k, s_ in enumerate((0.78, 0.56)):
        ax, ay = 450, 92 + (292 - 92) * (1 - s_) + 6
        bx = 450 - 140 * s_; by = 284
        tri_items.append(([(bx, by), (ax, ay), (900 - bx, by), (bx, by)], 3.2, None))
    for t in np.linspace(-0.8, 0.8, 9):
        tri_items.append(([(450, 182), (450 + t * 110, 284)], 2.6, None))
    lat = strokes(W, H, tri_items) * gable
    art = GP(art, lat, CREAM, "#d9c7a0", seed=nx(), rough=0.4)
    vent = shapes(W, H, [deform(ellipse_pts(450, 214, 16, 16, 12), rng, 0, 0)])
    art = GP(art, vent, "#2a160c", seed=nx(), rough=0.5)
    fascia = strokes(W, H, [([(300, 298), (450, 84), (600, 298)], 9, None)])
    art = GP(art, fascia, CREAM, "#d6c39a", seed=nx(), rough=0.6)
    scal = circles(W, H, [(300 + (450 - 300) * t + 8 * math.cos(-0.96), 298 + (84 - 298) * t + 8, 4.2) for t in np.linspace(0.04, 0.95, 16)] +
                   [(600 + (450 - 600) * t, 298 + (84 - 298) * t + 8, 4.2) for t in np.linspace(0.04, 0.95, 16)])
    art = GP(art, scal, CREAM, seed=nx(), rough=0.3)
    eave = strokes(W, H, [([(124, 292), (776, 292)], 6, None)])
    art = GP(art, eave, CREAM, "#cdb994", seed=nx(), rough=0.6)
    # finial (horn-like crossed ends)
    fin = strokes(W, H, [([(450, 92), (432, 58), (424, 44)], 4.5, (0.0, 0.5)), ([(450, 92), (468, 58), (476, 44)], 4.5, (0.0, 0.5))])
    art = GP(art, fin, CREAM, seed=nx(), rough=0.4)
    # eave shadow on the wall
    shd = rect(W, H, 182, 290, 718, 304)
    art = G(art, shd, "#2a1208", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=2, feather=3)
    # light from the left, shade on the right, dark under the floor
    yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    house = np.clip(body + roof + gable + beam, 0, 1)
    shade_r = house * np.clip((xx_ - 470) / 300, 0, 1) * 0.8
    art = G(art, shade_r, "#3a1a10", seed=nx(), density=0.75, edge=0.05, bloom=0.3, rough=3, feather=6)
    lit = house * np.clip((380 - xx_) / 300, 0, 1) * 0.7
    art = G(art, lit, "#f6cf8a", seed=nx(), density=0.45, edge=0.05, bloom=0.4, rough=3, feather=6)
    under = rect(W, H, 180, 426, 720, 470)
    art = G(art, under * np.clip(1 - (yy_ - 426) / 50, 0, 1), "#2a1a12", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=4, feather=6)
    gsh = shapes(W, H, [deform(ellipse_pts(450, 590, 330, 16, 18), rng, 1, 0.03)])
    art = G(art, gsh, "#2c3420", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=4, feather=4)
    # ---- Tomohon flowers & shrubs at the base
    shrubs = []
    for (x, y, r) in [(120, 574, 50), (180, 590, 36), (760, 570, 54), (822, 588, 38), (330, 596, 26), (580, 598, 28)]:
        shrubs.append(deform(ellipse_pts(x, y, r, r * 0.62, 14), rng, 2, 0.06))
    sm = shapes(W, H, shrubs)
    art = G(art, sm, "#3f6a38", "#2b4a2a", seed=nx(), density=0.85, edge=0.6, bloom=0.35, rough=4)
    fl = []
    for _ in range(46):
        bx = rng.choice([120, 180, 760, 822, 330, 580]) + rng.uniform(-40, 40)
        by = 560 + rng.uniform(-18, 30)
        fl.append((bx, by, rng.uniform(3.5, 6.5)))
    fm1 = circles(W, H, fl[::2]); fm2 = circles(W, H, fl[1::2])
    art = G(art, fm1 * sm, "#d8402c", seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=1.5, feather=0.8)
    art = G(art, fm2 * sm, "#f0b630", seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=1.5, feather=0.8)
    art = add_grain(art, 3, 0.03)
    save(art, f"{OUT}/rumah.webp", max_w=860, quality=80)
    show(art, "mk-rumah", tone="#f4ead8")
    clear()
