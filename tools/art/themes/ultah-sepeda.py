"""Ultah Sepeda — kids' bike party in poster gouache with a pencil line: a little bike with a helmet hanging on the
handlebar and streamers on the grips, a balloon bunch (separate so it can bob), the park track with cones, flags and two
small riders, a flag bunting, a mini pennant divider and a helmet.
Run: python3 -I ultah-sepeda.py [part ...]  parts: sepeda balon taman bendera panji helm
Assets -> public/themes/art/ultah-sepeda/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s2_lib import *

OUT = outdir("ultah-sepeda")
PARTS = sys.argv[1:] or ["sepeda", "balon", "taman", "bendera", "panji", "helm"]
LINE = "#2a2f45"
CORAL, CORAL_D = "#ff6b4a", "#d9472c"
SUN, SUN_D = "#ffc93c", "#e0a316"
TEAL, TEAL_D = "#1fa4a0", "#14807d"
SKY, SKY_D = "#5fb8e8", "#3b93c6"
GRAPE = "#8f6bd6"
LIME, LIME_D = "#8fd15a", "#5fa63a"
NAVY = "#233554"
WHITE = "#fffaf0"
GREY, GREY_D = "#9aa3b3", "#6c7488"


def P(art, mask, col, col2=None, px=1.3, dens=0.75, **k):
    return paint(art, mask, col, col2, px=px, dens=dens, lc=LINE, **k)


def hi(art, mask, dx=3, dy=3, col="#ffffff", d=0.45):
    return GP(art, light_side(mask, dx, dy, 2) * d, col, seed=rs(), rough=0.6, pad=6)


def wheel(art, W, H, cx, cy, r, rng, bead_cols):
    tyre = np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - r * 0.16)]), 0, 1)
    art = P(art, tyre, "#3a3d4a", "#2a2c36", px=1.0)
    rim = np.clip(circles(W, H, [(cx, cy, r - r * 0.16)]) - circles(W, H, [(cx, cy, r - r * 0.22)]), 0, 1)
    art = GP(art, rim, "#e6e9ef", "#c9ced8", seed=rs(), rough=0.5, pad=6)
    angs = np.linspace(0, math.tau, 13)[:-1]
    sp = strokes(W, H, [([(cx, cy), (cx + math.cos(a) * (r * .8), cy + math.sin(a) * (r * .8))], 1.6, None) for a in angs])
    art = G(art, sp, "#a3a9b6", seed=rs(), density=0.85, edge=0, bloom=0, rough=0.3, pad=6)
    # spoke beads, the kids' favourite
    for k, a in enumerate(angs[::2]):
        bx, by = cx + math.cos(a + 0.1) * r * 0.55, cy + math.sin(a + 0.1) * r * 0.55
        art = P(art, circles(W, H, [(bx, by, r * 0.07)]), bead_cols[k % len(bead_cols)], px=0.6, dens=0.4)
    art = P(art, circles(W, H, [(cx, cy, r * 0.13)]), "#d7dbe3", px=0.8)
    return art


def kid(art, W, H, x, y, s, shirt, helmet, bike, rng, flip=1):
    """Tiny stylised rider (side view) on a small bike: round head, dot eye, smile, helmet."""
    f = flip
    X = lambda u: x + u * s * f
    Y = lambda v: y + v * s
    art = wheel(art, W, H, X(-16), Y(14), 9 * s, rng, [SUN, CORAL])
    art = wheel(art, W, H, X(16), Y(14), 9 * s, rng, [TEAL, SUN])
    fr = strokes(W, H, [([(X(-16), Y(14)), (X(-2), Y(14))], 2.6 * s, None), ([(X(-2), Y(14)), (X(-6), Y(2))], 2.6 * s, None),
                        ([(X(-6), Y(2)), (X(10), Y(2))], 2.6 * s, None), ([(X(10), Y(2)), (X(16), Y(14))], 2.6 * s, None),
                        ([(X(10), Y(2)), (X(12), Y(-6))], 2.2 * s, None), ([(X(-2), Y(14)), (X(10), Y(2))], 2.6 * s, None)])
    art = P(art, fr, bike, px=0.8, dens=0.6)
    leg = strokes(W, H, [(curve([(X(-5), Y(-2)), (X(2), Y(6)), (X(-1), Y(13))], 8), 3.4 * s, None)])
    art = P(art, leg, NAVY, px=0.7, dens=0.5)
    body = shapes(W, H, [deform([(X(-8), Y(-1)), (X(-2), Y(-16)), (X(6), Y(-14)), (X(2), Y(0))], rng, 1, .04)])
    art = P(art, body, shirt, px=0.8, dens=0.55)
    arm = strokes(W, H, [(curve([(X(2), Y(-12)), (X(8), Y(-8)), (X(12), Y(-6))], 8), 2.6 * s, None)])
    art = P(art, arm, shirt, px=0.7, dens=0.5)
    head = circles(W, H, [(X(1), Y(-22), 6.2 * s)])
    art = P(art, head, "#c98a62", "#b5774f", px=0.8, dens=0.5)
    hel = shapes(W, H, [[(X(-6.5), Y(-22)), (X(-5), Y(-28)), (X(1), Y(-30.5)), (X(7), Y(-28)), (X(8.5), Y(-23)), (X(9.5), Y(-22))]])
    art = P(art, hel, helmet, px=0.8, dens=0.55)
    art = GP(art, circles(W, H, [(X(4.2), Y(-21), 0.95 * s)]), "#2a2018", seed=rs(), rough=0.3, pad=4)
    sm = strokes(W, H, [(arc_pts(X(4.2), Y(-19.5), 2.2 * s, 0.3, 2.4, 8), 0.8 * s, None)])
    art = G(art, sm, "#5a2a1a", seed=rs(), density=0.8, edge=0, bloom=0, rough=0.3, pad=4)
    return art


random.seed(19)

if "sepeda" in PARTS:
    W, H = 640, 420
    rng = random.Random(7)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(320, 396, 250, 13, 20)]), "#3b5a2a", seed=rs(), density=0.3, edge=0, bloom=0, rough=3, feather=3)
    Rh, Fh, r = (170, 312), (476, 312), 84
    art = wheel(art, W, H, *Rh, r, rng, [SUN, CORAL, TEAL, GRAPE])
    art = wheel(art, W, H, *Fh, r, rng, [TEAL, SUN, CORAL, LIME])
    BB, S, Hd = (300, 312), (258, 188), (430, 172)
    # chain guard + chain
    guard = shapes(W, H, [[(166, 298), (300, 296), (318, 312), (300, 330), (170, 326)]])
    art = P(art, guard, SUN, SUN_D)
    art = P(art, circles(W, H, [(BB[0], BB[1], 20)]), GREY, GREY_D, px=1.0)
    art = P(art, strokes(W, H, [([BB, (BB[0] + 24, BB[1] + 30)], 6, None)]), GREY_D, px=0.8)
    art = P(art, shapes(W, H, [ellipse_pts(BB[0] + 28, BB[1] + 34, 16, 6, 10)]), NAVY, px=0.8)
    # frame (step-through kid's frame)
    tubes = [(Rh, BB), (Rh, S), (S, BB), (BB, (420, 200)), ((420, 200), Hd), ((420, 200), Fh)]
    frame = strokes(W, H, [([a, b], 18, None) for a, b in tubes])
    art = P(art, frame, CORAL, CORAL_D, px=1.3, dens=0.8)
    art = hi(art, frame, 0, 4, "#ffd1c2", 0.6)
    # mudguards
    for (cx, cy) in (Rh, Fh):
        mg = strokes(W, H, [(arc_pts(cx, cy, r + 10, math.pi * 1.12, math.pi * 1.88, 24), 9, None)])
        art = P(art, mg, WHITE, "#e8e2d4", px=1.0)
    # saddle + post
    art = P(art, strokes(W, H, [([S, (S[0] - 6, S[1] - 26)], 9, None)]), GREY, px=0.9)
    seat = shapes(W, H, [deform([(S[0] - 52, S[1] - 34), (S[0] + 30, S[1] - 40), (S[0] + 34, S[1] - 26), (S[0] - 48, S[1] - 20)], rng, 1, .03)])
    art = P(art, seat, TEAL, TEAL_D)
    art = hi(art, seat, 0, 3, "#9fe3e0", 0.6)
    # handlebar: stem up, bar curving back, grips with streamers, a bell
    bar = strokes(W, H, [([Hd, (Hd[0] - 4, Hd[1] - 46)], 9, None), (curve([(Hd[0] - 4, Hd[1] - 46), (Hd[0] - 30, Hd[1] - 54), (Hd[0] - 62, Hd[1] - 50)], 16), 8, None)])
    art = P(art, bar, GREY, GREY_D, px=1.0)
    grip = strokes(W, H, [([(Hd[0] - 50, Hd[1] - 51), (Hd[0] - 76, Hd[1] - 48)], 14, None)])
    art = P(art, grip, NAVY, px=1.0)
    stream = [(curve([(Hd[0] - 78, Hd[1] - 48), (Hd[0] - 100 - k * 4, Hd[1] - 40 + k * 8), (Hd[0] - 124 - k * 6, Hd[1] - 30 + k * 16)], 14), 4, (0, .5)) for k in range(4)]
    for k, it in enumerate(stream):
        art = P(art, strokes(W, H, [it]), [CORAL, SUN, TEAL, GRAPE][k], px=0.6, dens=0.4)
    art = P(art, circles(W, H, [(Hd[0] - 30, Hd[1] - 64, 11)]), SUN, SUN_D, px=1.0)
    art = hi(art, circles(W, H, [(Hd[0] - 30, Hd[1] - 64, 11)]), 2, 3, "#fff2b8", 0.7)
    # front basket
    bk = shapes(W, H, [[(Hd[0] + 6, Hd[1] - 30), (Hd[0] + 88, Hd[1] - 30), (Hd[0] + 80, Hd[1] + 24), (Hd[0] + 12, Hd[1] + 24)]], smooth=False)
    art = P(art, bk, WHITE, "#e6dccb")
    weave = strokes(W, H, [([(Hd[0] + 8, Hd[1] - 18 + 10 * k), (Hd[0] + 86, Hd[1] - 18 + 10 * k)], 2, None) for k in range(4)] + [([(Hd[0] + 18 + 14 * k, Hd[1] - 30), (Hd[0] + 20 + 12 * k, Hd[1] + 24)], 2, None) for k in range(6)]) * bk
    art = shade(art, weave, SKY_D, 0.5)
    # helmet hanging from the handlebar by its strap
    strap = strokes(W, H, [(curve([(Hd[0] - 18, Hd[1] - 50), (Hd[0] - 30, Hd[1] - 10), (Hd[0] - 20, Hd[1] + 20)], 16), 3, None)])
    art = P(art, strap, NAVY, px=0.6, dens=0.4)
    hc = (Hd[0] - 30, Hd[1] + 46)
    helm = shapes(W, H, [[(hc[0] - 42, hc[1] + 8), (hc[0] - 38, hc[1] - 16), (hc[0] - 14, hc[1] - 34), (hc[0] + 18, hc[1] - 34), (hc[0] + 40, hc[1] - 14), (hc[0] + 46, hc[1] + 8)]])
    art = P(art, helm, SKY, SKY_D)
    vents = strokes(W, H, [([(hc[0] - 18 + 14 * k, hc[1] - 26), (hc[0] - 22 + 15 * k, hc[1] - 4)], 5, None) for k in range(4)]) * helm
    art = P(art, vents, NAVY, ln=False)
    art = hi(art, helm, 3, 4, "#cfeeff", 0.6)
    art = P(art, strokes(W, H, [([(hc[0] - 44, hc[1] + 8), (hc[0] + 48, hc[1] + 8)], 7, None)]), SUN, SUN_D, px=0.8)
    art = add_grain(art, 3, 0.025)
    save(art, f"{OUT}/sepeda.webp", max_w=560, quality=82)
    prev(art, "us_sepeda", bg="#bfe6f2")

if "balon" in PARTS:
    # balloon bunch, strings meeting at the bottom tie point (= the handlebar grip)
    W, H = 360, 520
    rng = random.Random(11)
    art = blank(W, H)
    tie = (190, 508)
    balls = [(110, 150, 62, CORAL, CORAL_D), (230, 110, 70, SUN, SUN_D), (290, 230, 56, TEAL, TEAL_D), (160, 270, 54, GRAPE, "#6f4cb8"), (60, 300, 44, LIME, LIME_D)]
    st = []
    for (x, y, rr, c, d) in balls:
        st.append((curve([(x, y + rr * 1.12), (x + (tie[0] - x) * 0.4 + rng.uniform(-14, 14), (y + tie[1]) / 2 + 30), tie], 30), 1.8, None))
    art = G(art, strokes(W, H, st), "#4a4f66", seed=rs(), density=0.85, edge=0, bloom=0, rough=0.4, feather=0.4)
    for (x, y, rr, c, d) in sorted(balls, key=lambda b: b[1]):
        b = shapes(W, H, [deform([(x + math.cos(t) * rr * (0.92 + 0.08 * math.sin(t)), y + math.sin(t) * rr * 1.1 - (rr * 0.12 if math.sin(t) < 0 else 0)) for t in np.linspace(0, math.tau, 26)[:-1]], rng, 1, .03)])
        art = P(art, b, c, d, px=1.2, dens=0.7)
        knot = shapes(W, H, [[(x - 8, y + rr * 1.16), (x + 8, y + rr * 1.16), (x, y + rr * 1.02)]], smooth=False)
        art = P(art, knot, d, px=0.7, dens=0.5)
        art = G(art, light_side(b, -8, -10, 7), mix(d, "#000000", .2), seed=rs(), density=0.35, edge=0.1, bloom=0.3, rough=2)
        art = GP(art, shapes(W, H, [petal_pts(x - rr * .42, y - rr * .5, rr * .42, rr * .16, -0.9, n=10)]), "#ffffff", seed=rs(), rough=0.6, density=0.6, pad=6)
    art = add_grain(art, 4, 0.02)
    save_full(art, f"{OUT}/balon.webp", size=(270, 390), quality=82)
    prev(art, "us_balon", bg="#bfe6f2")

if "taman" in PARTS:
    # park band: hedges and round trees, the bike track looping with a dashed centre line, cones, chequered flags, riders
    W, H = 780, 560
    rng = random.Random(23)
    art = blank(W, H)
    # back hedges/trees (top edge transparent: sits on the CSS sky)
    for (x, y, r, c, d) in [(70, 120, 70, "#5fa63a", "#4b8a2c"), (190, 96, 56, "#74ba45", "#5fa63a"), (600, 110, 78, "#5fa63a", "#4b8a2c"), (720, 130, 60, "#74ba45", "#5fa63a"), (420, 124, 46, "#74ba45", "#5fa63a")]:
        art = P(art, strokes(W, H, [([(x, y + r * .6), (x, y + r * 1.4)], r * .2, None)]), "#8a5a3a", "#6e4630", px=1.0)
        cr = blob(W, H, x, y, r, r * .95, rng, 14)
        art = P(art, cr, c, d, px=1.2, dens=0.55)
        art = hi(art, cr, 6, 8, "#bfe68a", 0.55)
    grass = shapes(W, H, [[(-20, 170)] + [(x, 170 + 10 * math.sin(x / 90)) for x in range(0, W + 1, 30)] + [(W + 20, 170), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    art = P(art, grass, LIME, "#7cc04c", px=1.4, dens=0.5, streak=0.9)
    tufts = []
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(190, H)
        for k in (-1, 0, 1):
            tufts.append(([(x + k * 3, y), (x + k * 5, y - 7 - abs(k) * -2)], 2, (0, .6)))
    art = shade(art, strokes(W, H, tufts), LIME_D, 0.6)
    clear()
    # track: a wide S loop
    cen = curve([(-40, 300), (180, 240), (420, 280), (560, 370), (700, 330), (840, 260)], 160)
    trk = strokes(W, H, [(cen, 96, None)])
    art = P(art, trk, "#8d97ac", "#7a849a", px=1.4, dens=0.6)
    edge = np.clip(strokes(W, H, [(cen, 104, None)]) - trk, 0, 1)
    art = P(art, edge, WHITE, "#e8e2d4", ln=False)
    dash = []
    for i, (x, y, a) in enumerate(along(cen, 28)):
        if i % 2 == 0:
            dash.append(([(x - math.cos(a) * 8, y - math.sin(a) * 8), (x + math.cos(a) * 8, y + math.sin(a) * 8)], 5, None))
    art = GP(art, strokes(W, H, dash), WHITE, seed=rs(), rough=0.6, pad=6)
    clear()
    # chequered start line across the track near the left
    sx, sy, sa = along(cen, 150)[0]
    cells = []
    for i in range(-4, 4):
        for j in range(2):
            if (i + j) % 2 == 0:
                px_ = sx + (-math.sin(sa)) * (i * 12 + 6) + math.cos(sa) * (j * 12)
                py_ = sy + math.cos(sa) * (i * 12 + 6) + math.sin(sa) * (j * 12)
                cells.append([(px_ - 6, py_ - 6), (px_ + 6, py_ - 6), (px_ + 6, py_ + 6), (px_ - 6, py_ + 6)])
    art = GP(art, shapes(W, H, cells, smooth=False), "#20232e", seed=rs(), rough=0.5, pad=6)
    # cones along the track edges
    for (x, y, s_) in [(250, 196, 1.0), (360, 214, 0.9), (520, 300, 1.0), (640, 420, 1.15), (120, 360, 1.1), (300, 352, 1.1), (740, 390, 1.0)]:
        cone = shapes(W, H, [[(x - 12 * s_, y), (x - 3 * s_, y - 30 * s_), (x + 3 * s_, y - 30 * s_), (x + 12 * s_, y)]], smooth=False)
        base = shapes(W, H, [[(x - 17 * s_, y), (x + 17 * s_, y), (x + 17 * s_, y + 5 * s_), (x - 17 * s_, y + 5 * s_)]], smooth=False)
        art = P(art, base, CORAL_D, px=0.8, dens=0.55)
        art = P(art, cone, "#ff8a3d", "#e8692a", px=0.9, dens=0.6)
        art = GP(art, cone * shapes(W, H, [[(x - 20, y - 18 * s_), (x + 20, y - 18 * s_), (x + 20, y - 11 * s_), (x - 20, y - 11 * s_)]], smooth=False), WHITE, seed=rs(), rough=0.4, pad=4)
    # flags on poles
    for (x, y, c) in [(40, 250, CORAL), (210, 190, SUN), (470, 222, TEAL), (690, 280, GRAPE)]:
        art = P(art, strokes(W, H, [([(x, y), (x, y - 70)], 4, None)]), "#f4efe4", px=0.8, dens=0.6)
        fl = shapes(W, H, [[(x + 2, y - 70), (x + 40, y - 60), (x + 2, y - 48)]], smooth=False)
        art = P(art, fl, c, mix(c, "#000000", .15), px=0.8, dens=0.6)
    clear()
    # two riders on the track
    art = kid(art, W, H, 430, 262, 2.2, SUN, CORAL, TEAL, rng, 1)
    art = kid(art, W, H, 600, 352, 2.4, TEAL, SUN, CORAL, rng, 1)
    art = kid(art, W, H, 150, 268, 2.0, CORAL, TEAL, GRAPE, rng, -1)
    # flowers in the grass
    fl = [(rng.uniform(0, W), rng.uniform(430, H - 10), rng.uniform(5, 8)) for _ in range(26)]
    for k, col in enumerate([WHITE, SUN, CORAL]):
        items = []
        for (x, y, r) in fl[k::3]:
            items += [(x + math.cos(j * 1.256) * r * .55, y + math.sin(j * 1.256) * r * .5, r * .5) for j in range(5)]
        art = P(art, circles(W, H, items), col, px=0.7, dens=0.4)
    art = add_grain(art, 6, 0.025)
    save(art, f"{OUT}/taman.webp", max_w=780, quality=76)
    prev(art, "us_taman", bg="#bfe6f2")

if "bendera" in PARTS:
    W, H = 800, 130
    rng = random.Random(31)
    art = blank(W, H)
    rope = [(x, 18 + 34 * math.sin(math.pi * x / W)) for x in range(0, W + 1, 8)]
    art = P(art, strokes(W, H, [(rope, 3, None)]), "#f4efe4", px=0.7, dens=0.6)
    cols = [CORAL, SUN, TEAL, GRAPE, LIME, SKY]
    for k, (x, y, a) in enumerate(along(rope, 50)):
        tri = [(x - 20, y + 2), (x + 20, y + 3), (x + rng.uniform(-3, 3), y + 54)]
        m = shapes(W, H, [tri], smooth=False)
        c = cols[k % len(cols)]
        art = P(art, m, c, mix(c, "#000000", .12), px=0.9, dens=0.6)
        if k % 3 == 1:
            art = GP(art, circles(W, H, [(x + dx, y + 16 + dy, 3) for dx, dy in [(-7, 0), (7, 0), (0, 12)]]), WHITE, seed=rs(), rough=0.4, pad=4)
    save_full(art, f"{OUT}/bendera.webp", size=(800, 130), quality=82)
    prev(art, "us_bendera", bg="#bfe6f2")

if "panji" in PARTS:
    W, H = 420, 70
    rng = random.Random(41)
    art = blank(W, H)
    rope = [(x, 12 + 14 * math.sin(math.pi * x / W)) for x in range(10, W - 9, 6)]
    art = P(art, strokes(W, H, [(rope, 2.2, None)]), NAVY, px=0.5, dens=0.4)
    cols = [CORAL, SUN, TEAL, GRAPE, LIME, SKY, CORAL]
    for k, (x, y, a) in enumerate(along(rope, 56)):
        m = shapes(W, H, [[(x - 15, y + 1), (x + 15, y + 2), (x, y + 38)]], smooth=False)
        art = P(art, m, cols[k % len(cols)], px=0.8, dens=0.6)
    save(art, f"{OUT}/panji.webp", max_w=320, quality=84)
    prev(art, "us_panji")

if "helm" in PARTS:
    W, H = 200, 150
    rng = random.Random(51)
    art = blank(W, H)
    hc = (100, 104)
    helm = shapes(W, H, [[(hc[0] - 80, hc[1] + 14), (hc[0] - 72, hc[1] - 30), (hc[0] - 28, hc[1] - 66), (hc[0] + 32, hc[1] - 66), (hc[0] + 74, hc[1] - 28), (hc[0] + 86, hc[1] + 14)]])
    art = P(art, helm, CORAL, CORAL_D, px=1.3)
    vents = strokes(W, H, [([(hc[0] - 36 + 24 * k, hc[1] - 52), (hc[0] - 42 + 26 * k, hc[1] - 10)], 9, None) for k in range(4)]) * helm
    art = P(art, vents, NAVY, ln=False)
    art = GP(art, strokes(W, H, [(curve([(hc[0] - 60, hc[1] - 24), (hc[0] - 10, hc[1] - 56), (hc[0] + 40, hc[1] - 50)], 20), 6, None)]) * helm, "#ffffff", seed=rs(), rough=0.5, density=0.55, pad=6)
    art = P(art, strokes(W, H, [([(hc[0] - 82, hc[1] + 14), (hc[0] + 88, hc[1] + 14)], 12, None)]), SUN, SUN_D, px=1.0)
    art = P(art, shapes(W, H, [[(hc[0] + 60, hc[1] - 4), (hc[0] + 98, hc[1] + 2), (hc[0] + 90, hc[1] + 12), (hc[0] + 58, hc[1] + 8)]]), NAVY, px=0.9)
    save(art, f"{OUT}/helm.webp", max_w=120, quality=84)
    prev(art, "us_helm")

kb(OUT)
