"""Seminar Ilmiah — editorial gouache for an academic seminar: a ball-and-stick molecule (matte painted spheres with
soft modelling, painted bonds), a lecture hall (screen with a painted chart, lectern with mic, curved rows of seats,
a few listeners as simple shapes from behind), a hand-painted data-line divider and a small atom node.
Palette: deep indigo, teal, signal orange, warm paper, lilac grey; light from the upper left.
Run: python3 -I seminar-ilmiah.py [part ...]  parts: molecule hall chart atom"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i6_lib import *  # noqa

OUT = outdir("seminar-ilmiah")
PARTS = sys.argv[1:] or ["molecule", "hall", "chart", "atom"]
IND, IND_D, IND_L, TEAL, TEAL_D, TEAL_L, ORA, ORA_D, PAP, LIL = "#14213d", "#0b1428", "#2e4372", "#0f7b74", "#0a524d", "#4fb3a8", "#f26b38", "#b8461d", "#f4f1ea", "#cdd3e2"


def sphere(art, W, H, x, y, r, col, seed, dark=None, hi="#ffffff"):
    m = circle_mask(W, H, x, y, r)
    art = GP(art, m, col, mix(col, "#ffffff", .12), seed=seed, rough=1.0, streak=.7)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - x + r * .35) ** 2 + (yy - y + r * .35) ** 2) / (r * 1.6)
    shade = np.clip(d - .25, 0, 1) ** 1.3 * m
    art = tint(art, shade, dark or mix(col, "#0b1428", .6), .75, seed=seed + 1)
    rimlight = np.clip(side_light(m, 3, 3, 1.5), 0, 1) * m
    art = tint(art, rimlight, mix(col, "#9fb0d8", .5), .35, seed=seed + 2)
    hl = circle_mask(W, H, x - r * .38, y - r * .42, r * .22)
    art = tint(art, gaussian_filter(hl, r * .08), hi, .55, seed=seed + 3)
    return art


def bond(art, W, H, a, b, wd, seed, col="#c9ccd6"):
    m = strokes(W, H, [([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b], wd, None)])
    art = GP(art, m, col, "#e4e6ec", seed=seed, rough=.6, streak=.6)
    # cylinder shading: dark along the lower side
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    if ny < 0:
        nx, ny = -nx, -ny
    art = tint(art, side_light(m, int(-nx * wd * .4), int(-ny * wd * .4), 1.0) * m, "#6b7390", .6, seed=seed + 1)
    return art


def part_molecule():
    W, H = 560, 500
    rng = random.Random(5)
    art = blank(W, H)
    atoms = [(270, 250, 58, TEAL), (150, 170, 40, ORA), (400, 150, 44, IND_L), (420, 330, 36, PAP), (150, 360, 46, IND_L),
             (60, 260, 26, PAP), (290, 80, 28, PAP), (510, 230, 26, ORA), (250, 440, 28, TEAL_L)]
    bonds = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 6), (2, 7), (4, 8), (3, 7), (4, 5)]
    # back-to-front: draw bonds first (behind spheres)
    for k, (i, j) in enumerate(bonds):
        a, b = atoms[i], atoms[j]
        art = bond(art, W, H, (a[0], a[1]), (b[0], b[1]), 13, 100 + k)
    for k, (x, y, r, c) in sorted(enumerate(atoms), key=lambda t: t[1][2])[::1]:
        pass
    for k, (x, y, r, c) in enumerate(sorted(atoms, key=lambda t: t[2])):
        art = sphere(art, W, H, x, y, r, c, 10 + k * 7, dark="#7d7a72" if c == PAP else None)
    # soft cast shadow
    sh = np.zeros((H, W), np.float32)
    for (x, y, r, c) in atoms:
        sh = np.maximum(sh, circle_mask(W, H, x + 14, y + 18, r))
    art = over(col_arr(sh, IND, gaussian_filter(sh, 10) * .12), art)
    preview(art, "sem-molecule", tone=PAP)
    save(art, f"{OUT}/molecule.webp", max_w=420, quality=82)


def part_hall():
    W, H = 780, 470
    rng = random.Random(3)
    art = painted_sky(W, H, [(0, "#e6e2d8"), (0.55, "#ddd8cc"), (0.56, "#c9c1b0"), (1, "#a99f8c")], seed=4, streak=.5, grain=.4)
    # wall panels
    pan = []
    for x in range(0, W, 78):
        pan.append(([(x, 0), (x, 250)], 3, None))
    art = OV(art, strokes(W, H, pan), lambda m: col_arr(m, "#c9c2b3", m * .7), pad=3)
    # screen with a painted chart
    scr = shape_mask(W, H, [(250, 40), (610, 34), (612, 232), (252, 236)], smooth=False)
    art = over(soft_shadow(scr, "#3a3326", 8, .35, 6, 8), art)
    art = GP(art, scr, "#fbfaf6", "#f1efe8", seed=5, rough=.8, streak=.5)
    frame = np.clip(scr - shape_mask(W, H, [(258, 47), (603, 41), (605, 226), (260, 229)], smooth=False), 0, 1)
    art = GP(art, frame, IND, seed=6, rough=.5)
    bars = []
    for i, hgt in enumerate([40, 64, 52, 96, 124]):
        x = 300 + i * 36
        bars.append(shape_mask(W, H, [(x, 205), (x + 22, 205), (x + 22, 205 - hgt), (x, 205 - hgt)], smooth=False))
    for i, b in enumerate(bars):
        art = GP(art, b, TEAL if i < 4 else ORA, seed=20 + i, rough=.8, streak=.7)
    line = [(480 + k * 20, 180 - 60 * (1 - math.exp(-k / 2.5)) + rng.uniform(-4, 4)) for k in range(6)]
    art = GP(art, strokes(W, H, [(curve(line, 30), 4, None)]), IND_L, seed=30, rough=.6)
    art = GP(art, circles(W, H, [(x, y, 5.5) for x, y in line]), ORA, seed=31, rough=.5)
    axis = strokes(W, H, [([(290, 70), (290, 206), (585, 206)], 2.4, None)])
    art = OV(art, axis, lambda m: col_arr(m, IND, m * .8), pad=3)
    txt = strokes(W, H, [([(300, 62), (400, 62)], 6, (0.05, 0.05)), ([(300, 76), (360, 76)], 4, (0.05, 0.05))])
    art = OV(art, txt, lambda m: col_arr(m, IND, m * .75), pad=3)
    # stage + lectern + mic + plant
    stage = shape_mask(W, H, [(0, 258), (W, 258), (W, 290), (0, 296)], smooth=False)
    art = GP(art, stage, "#8a6b49", "#9c7b56", seed=40, rough=1.0)
    art = tint(art, side_light(stage, 0, -5, 2) * stage, "#4d3a26", .5, seed=41)
    lec = shape_mask(W, H, [(110, 160), (196, 160), (186, 270), (120, 270)], smooth=False)
    art = GP(art, lec, IND, IND_L, seed=42, rough=.8)
    art = tint(art, side_light(lec, -6, 0, 3) * lec, IND_D, .6, seed=43)
    art = GP(art, shape_mask(W, H, [(104, 150), (202, 150), (198, 164), (108, 164)], smooth=False), TEAL, seed=44, rough=.5)
    mic = strokes(W, H, [([(170, 150), (182, 126), (196, 116)], 3, None)])
    art = OV(art, mic, lambda m: col_arr(m, "#2a2a2a", m), pad=3)
    art = GP(art, circles(W, H, [(198, 114, 6)]), "#2a2a2a", seed=45, rough=.3)
    art = GP(art, shape_mask(W, H, [(140, 196), (166, 196), (166, 222), (140, 222)], smooth=False), ORA, seed=46, rough=.5)
    pot = shape_mask(W, H, [(670, 220), (712, 220), (704, 262), (678, 262)], smooth=False)
    art = GP(art, pot, ORA_D, ORA, seed=47, rough=.6)
    lv = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * .28
        L = rng.uniform(60, 100)
        lv.append(([(691, 222), (691 + math.cos(a) * L * .5, 222 + math.sin(a) * L * .55), (691 + math.cos(a) * L, 222 + math.sin(a) * L)], 13, (0.2, 0.7)))
    art = impasto(art, strokes(W, H, lv), "#3f7a52", "#5b9a6a", seed=48, rough=1.0)
    # audience rows: curved seat backs + heads seen from behind
    for ri, (y0, sc, col) in enumerate([(330, .78, "#33508a"), (382, .9, "#2a4378"), (440, 1.05, "#1f3463")]):
        n = int(W / (54 * sc)) + 2
        seats, heads, shoulders = [], [], []
        for i in range(n):
            x = i * 54 * sc + (ri % 2) * 27 * sc - 10
            yc = y0 - 14 * sc * math.cos((x - W / 2) / W * math.pi)
            seats.append(shape_mask(W, H, [(x - 22 * sc, yc), (x + 22 * sc, yc), (x + 20 * sc, yc + 44 * sc), (x - 20 * sc, yc + 44 * sc)], smooth=True))
            if rng.random() < .55:
                heads.append((x + rng.uniform(-3, 3), yc - 20 * sc, 11 * sc * rng.uniform(.9, 1.1)))
                shoulders.append((x, yc - 2 * sc, 20 * sc, 12 * sc, 0))
        sm = np.clip(sum(seats), 0, 1)
        if shoulders:
            hm = np.clip(circles(W, H, heads) + ellipses(W, H, shoulders), 0, 1)
            art = GP(art, hm, rng.choice(["#4a3a2e", "#2c2522"]), "#5a463a", seed=60 + ri, rough=.8, streak=.4)
        art = GP(art, sm, col, mix(col, "#ffffff", .1), seed=70 + ri, rough=.8, streak=.7)
        art = tint(art, side_light(sm, 0, -4, 2) * sm, IND_D, .45, seed=80 + ri)
        art = tint(art, side_light(sm, 0, 4, 2) * sm, "#6f88c0", .35, seed=90 + ri)
    art = add_grain(art, 2, .025)
    preview(art, "sem-hall")
    save_rgb(art, f"{OUT}/hall.webp", size=(700, 422), quality=76)


def part_chart():
    W, H = 440, 80
    rng = random.Random(7)
    art = blank(W, H)
    pts = [(14 + k * 24, 46 - 18 * math.sin(k * .7) - k * .9 + rng.uniform(-2, 2)) for k in range(18)]
    art = GP(art, strokes(W, H, [(curve(pts, 80), 3.2, (0.05, 0.05))]), IND, seed=1, rough=.6)
    for i, (x, y) in enumerate(pts[::3]):
        art = sphere(art, W, H, x, y, 6.5, ORA if i == 3 else TEAL, 10 + i)
    preview(art, "sem-chart", tone=PAP)
    save(art, f"{OUT}/chart.webp", max_w=420, quality=84)


def part_atom():
    W = H = 180
    art = blank(W, H)
    ring1 = shape_mask(W, H, ellipse_pts(90, 90, 80, 26, 40, .5), smooth=True) - shape_mask(W, H, ellipse_pts(90, 90, 75, 22, 40, .5), smooth=True)
    ring2 = shape_mask(W, H, ellipse_pts(90, 90, 80, 26, 40, -.6), smooth=True) - shape_mask(W, H, ellipse_pts(90, 90, 75, 22, 40, -.6), smooth=True)
    art = GP(art, np.clip(ring1, 0, 1), IND_L, seed=2, rough=.4)
    art = GP(art, np.clip(ring2, 0, 1), TEAL, seed=3, rough=.4)
    art = sphere(art, W, H, 90, 90, 24, ORA, 4)
    art = sphere(art, W, H, 90 + 80 * math.cos(.5) * .98, 90 + 80 * math.sin(.5) * .98, 8, TEAL_L, 5)
    art = sphere(art, W, H, 90 - 80 * math.cos(.6) * .98, 90 + 80 * math.sin(.6) * .98, 8, IND_L, 6)
    preview(art, "sem-atom", tone=PAP)
    save(art, f"{OUT}/atom.webp", max_w=120, quality=84)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
