"""Ultah Anjing — kids' birthday puppy party in gouache + crayon line: original generic puppies (a corgi-like pup in a
party hat, a tricolour floppy-eared pup peeking from a red-roofed doghouse, a white pup with black spots and a red
ball), bones, balls, paw prints and bunting on a sunny backyard.
Run: python3 -I ultah-anjing.py [part ...]  parts: house corgi spotty ball bone paw bunting cake
Assets -> public/themes/art/ultah-anjing/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t2_lib import *

OUT = outdir("ultah-anjing")
PARTS = sys.argv[1:] or ["house", "corgi", "spotty", "ball", "bone", "paw", "bunting", "cake"]
INK = "#3b2a20"
TAN, TAN_D, TAN_L = "#e8964a", "#c06f2c", "#f6bd7c"
BRN, BRN_D, BRN_L = "#8a5232", "#5e3420", "#b07650"
WH, WH_D = "#fffaf0", "#e2d6c2"
BK, BK_D, BK_L = "#3a3436", "#241f21", "#5c5557"
RED, RED_D, RED_L = "#e05a3a", "#b23e24", "#f08a6a"
YEL, YEL_D, YEL_L = "#ffc93c", "#e0a218", "#ffe08a"
BLU, BLU_D, BLU_L = "#4a9fe0", "#2f78b8", "#8cc6f2"
GRN, GRN_D, GRN_L = "#7cc35a", "#4f9a3a", "#a8dc84"
PINK, PINK_D = "#f59aaa", "#d9637a"
WOOD, WOOD_D, WOOD_L = "#f2c26b", "#c9933e", "#fbdb9a"


def ink(art, W, H, items, nx, col=INK, amt=0.9):
    return crayon(art, strokes(W, H, items), col, seed=nx(), amt=amt, tooth=0.2)


def paint(art, m, c, nx, ldir=(-10, -12), blur=9, line=True):
    art = body(art, m, c[0], c[1] if len(c) > 1 else c[0], c[2] if len(c) > 2 else c[0], c[3] if len(c) > 3 else c[0], nx, ldir=ldir, blur=blur)
    if line:
        art = crayon(art, inner_edge(m, 2.2), mix(c[2] if len(c) > 2 else c[0], INK, 0.75), seed=nx(), amt=0.95, tooth=0.05)
    return art


def face(art, W, H, cx, cy, s, nx, tongue=True, wink=False):
    for ex in (-22, 22):
        if wink and ex > 0:
            art = ink(art, W, H, [(arc_pts(cx + ex * s, cy + 2 * s, 8 * s, math.pi * 1.15, math.pi * 1.85, 12), 3.4 * s, (0.2, 0.2))], nx)
            continue
        art = GP(art, ellipses(W, H, [(cx + ex * s, cy, 7.5 * s, 9 * s, 0)]), "#231a16", seed=nx(), rough=0.4, pad=6)
        art = OV(art, circles(W, H, [(cx + ex * s - 2.6 * s, cy - 3.4 * s, 2.9 * s)]), lambda m: col_arr(m, "#ffffff", m), pad=4)
    nose = shapes(W, H, [[(cx - 10 * s, cy + 13 * s), (cx + 10 * s, cy + 13 * s), (cx + 6 * s, cy + 21 * s), (cx, cy + 23 * s), (cx - 6 * s, cy + 21 * s)]])
    art = GP(art, nose, "#2a1f1c", seed=nx(), rough=0.4, pad=6)
    art = OV(art, ellipses(W, H, [(cx - 3 * s, cy + 15.5 * s, 3.4 * s, 1.8 * s, 0)]), lambda m: col_arr(m, "#ffffff", m * 0.7), pad=4)
    if tongue:
        tm = shapes(W, H, [deform(ellipse_pts(cx, cy + 36 * s, 7 * s, 9 * s, 12), random.Random(1), 1, 0.02)])
        art = paint(art, tm, (PINK, "#f7b0bc", PINK_D, "#ffd0da"), nx, blur=2)
        art = ink(art, W, H, [([(cx, cy + 31 * s), (cx, cy + 39 * s)], 1.6 * s, None)], nx, col=PINK_D, amt=0.7)
    art = ink(art, W, H, [([(cx, cy + 23 * s), (cx, cy + 28 * s)], 2.4 * s, None),
                          (arc_pts(cx - 7 * s, cy + 27 * s, 7 * s, 0.1, math.pi * 0.9, 10), 2.6 * s, None),
                          (arc_pts(cx + 7 * s, cy + 27 * s, 7 * s, 0.1, math.pi * 0.9, 10), 2.6 * s, None)], nx)
    art = G(art, circles(W, H, [(cx - 34 * s, cy + 16 * s, 8 * s), (cx + 34 * s, cy + 16 * s, 8 * s)]), "#f59aa0", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=2, feather=2.5)
    return art


def head(art, W, H, cx, cy, s, nx, rng, base, muzzle=WH, ears="flop", ear_c=None, spots=(), blaze=None, tongue=True, wink=False):
    hm = shapes(W, H, [deform(ellipse_pts(cx, cy, 60 * s, 52 * s, 18), rng, 1, 0.012)])
    ear_c = ear_c or base
    if ears == "up":
        em = shapes(W, H, [[(cx - 56 * s, cy - 18 * s), (cx - 58 * s, cy - 62 * s), (cx - 52 * s, cy - 86 * s), (cx - 40 * s, cy - 76 * s), (cx - 14 * s, cy - 44 * s)],
                           [(cx + 56 * s, cy - 18 * s), (cx + 58 * s, cy - 62 * s), (cx + 52 * s, cy - 86 * s), (cx + 40 * s, cy - 76 * s), (cx + 14 * s, cy - 44 * s)]])
        art = paint(art, em, ear_c, nx)
        inner = shapes(W, H, [[(cx - 46 * s, cy - 34 * s), (cx - 48 * s, cy - 70 * s), (cx - 26 * s, cy - 48 * s)],
                              [(cx + 46 * s, cy - 34 * s), (cx + 48 * s, cy - 70 * s), (cx + 26 * s, cy - 48 * s)]])
        art = GP(art, inner, "#f7b8b0", "#f4a8a0", seed=nx(), rough=0.5, pad=6)
    art = paint(art, hm, base, nx)
    for sx, sy, sr in spots:
        sm = shapes(W, H, [deform(ellipse_pts(cx + sx * s, cy + sy * s, sr * s, sr * 0.85 * s, 10), rng, 1, 0.08)]) * hm
        art = GP(art, sm, BK, BK_L, seed=nx(), rough=0.6, pad=6)
    if blaze:
        bm = shapes(W, H, [[(cx - 8 * s, cy - 52 * s), (cx + 8 * s, cy - 52 * s), (cx + 14 * s, cy - 4 * s), (cx - 14 * s, cy - 4 * s)]]) * hm
        art = GP(art, bm, blaze, seed=nx(), rough=0.6, pad=6)
    mz = shapes(W, H, [deform(ellipse_pts(cx, cy + 22 * s, 36 * s, 24 * s, 14), rng, 1, 0.02)])
    art = paint(art, mz * hm, (muzzle, "#ffffff", WH_D, "#ffffff"), nx, blur=4, line=False)
    if ears == "flop":
        em = shapes(W, H, [deform(petal_pts(cx - 50 * s, cy - 30 * s, 84 * s, 26 * s, math.pi * 0.56, n=16), rng, 1, 0.01),
                           deform(petal_pts(cx + 50 * s, cy - 30 * s, 84 * s, 26 * s, math.pi * 0.44, n=16), rng, 1, 0.01)])
        art = paint(art, em, ear_c, nx, ldir=(0, -8), blur=6)
    art = face(art, W, H, cx, cy, s, nx, tongue=tongue, wink=wink)
    return art, hm


def sitting(art, W, H, cx, cy, s, nx, rng, base, chest=WH, tail_side=1, legs=1.0):
    """Sitting body under a head centred at (cx, cy): returns art (draw before the head)."""
    tail = strokes(W, H, [(curve([(cx + tail_side * 40 * s, cy + 120 * s), (cx + tail_side * 78 * s, cy + 104 * s), (cx + tail_side * 92 * s, cy + 70 * s)], 20), 16 * s, (0.0, 0.5))])
    art = paint(art, tail, base, nx, blur=4)
    bm = shapes(W, H, [deform(ellipse_pts(cx, cy + 92 * s, 54 * s, 56 * s, 16), rng, 1, 0.012)])
    art = paint(art, bm, base, nx)
    ch = shapes(W, H, [deform(ellipse_pts(cx, cy + 82 * s, 28 * s, 36 * s, 14), rng, 1, 0.03)]) * bm
    art = paint(art, ch, (chest, "#ffffff", WH_D, "#ffffff"), nx, blur=4, line=False)
    lg = shapes(W, H, [[(cx - 30 * s, cy + 92 * s), (cx - 10 * s, cy + 92 * s), (cx - 10 * s, cy + (92 + 52 * legs) * s), (cx - 30 * s, cy + (92 + 52 * legs) * s)],
                       [(cx + 10 * s, cy + 92 * s), (cx + 30 * s, cy + 92 * s), (cx + 30 * s, cy + (92 + 52 * legs) * s), (cx + 10 * s, cy + (92 + 52 * legs) * s)]])
    art = paint(art, lg, base, nx, blur=4)
    py = cy + (92 + 52 * legs) * s
    paws = ellipses(W, H, [(cx - 21 * s, py, 15 * s, 10 * s, 0), (cx + 21 * s, py, 15 * s, 10 * s, 0)])
    art = paint(art, paws, (chest, "#ffffff", WH_D, "#ffffff"), nx, blur=3)
    art = ink(art, W, H, [([(cx + x * s, py - 2 * s), (cx + x * s, py + 6 * s)], 2 * s, None) for x in (-25, -17, 17, 25)], nx, amt=0.6)
    return art


def party_hat(art, W, H, x, y, s, nx, ang=-0.25, col=BLU):
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    hat = shapes(W, H, [[P(-26, 0), P(26, 0), P(0, -70)]], smooth=False)
    art = paint(art, hat, (col, mix(col, "#ffffff", .15), mix(col, INK, .3), mix(col, "#ffffff", .4)), nx, blur=4)
    st = strokes(W, H, [([P(-18, -14), P(16, -24)], 5 * s, None), ([P(-10, -36), P(9, -42)], 4 * s, None)]) * hat
    art = GP(art, st, YEL, seed=nx(), rough=0.3, pad=6)
    art = paint(art, circles(W, H, [(*P(0, -72), 10 * s)]), (RED, RED_L, RED_D, "#ffb8a0"), nx, blur=2)
    return art


def ball(art, W, H, cx, cy, r, nx, col=(RED, RED_L, RED_D, "#ffb8a0"), stripe=YEL):
    m = circles(W, H, [(cx, cy, r)])
    art = paint(art, m, col, nx, ldir=(-r * 0.25, -r * 0.25), blur=r * 0.3)
    st = strokes(W, H, [(arc_pts(cx - r * 1.3, cy + r * 0.2, r * 1.5, -0.6, 0.6, 16), r * 0.24, None)]) * m
    art = GP(art, st, stripe, seed=nx(), rough=0.4, pad=4)
    art = OV(art, ellipses(W, H, [(cx - r * 0.35, cy - r * 0.42, r * 0.22, r * 0.12, -30)]), lambda mm: col_arr(mm, "#ffffff", mm * 0.75), pad=4)
    return art


def bone(art, W, H, cx, cy, L, nx, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
    r = L * 0.13
    m = np.clip(strokes(W, H, [([P(-L * 0.36, 0), P(L * 0.36, 0)], L * 0.17, None)]) +
                circles(W, H, [(*P(-L * 0.42, -r * 0.8), r), (*P(-L * 0.42, r * 0.8), r), (*P(L * 0.42, -r * 0.8), r), (*P(L * 0.42, r * 0.8), r)]), 0, 1)
    art = paint(art, m, (WH, "#fffdf6", "#d8c6a6", "#ffffff"), nx, blur=L * 0.05)
    return art


if "house" in PARTS:
    W, H = 460, 470
    nx = Seq(101000); rng = random.Random(3)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(230, 448, 210, 16, 20)]), "#4f7a3a", seed=nx(), density=0.35, edge=0.05, bloom=0, rough=3, feather=6)
    walls = shapes(W, H, [[(70, 190), (390, 190), (390, 446), (70, 446)]], smooth=False)
    art = paint(art, walls, (WOOD, WOOD_L, WOOD_D, "#fff0c4"), nx, ldir=(-12, 0), blur=12)
    planks = strokes(W, H, [([(70, 220 + k * 30), (390, 220 + k * 30)], 2.4, None) for k in range(8)]) * walls
    art = tint(art, planks, WOOD_D, 0.6, seed=nx(), streak=0.3)
    art = wood(art, walls, WOOD, WOOD_L, WOOD_D, seed=nx(), along=0.0, amt=0.25)
    door = shapes(W, H, [[(156, 446), (156, 300)] + arc_pts(230, 300, 74, math.pi, math.tau, 24) + [(304, 300), (304, 446)]], smooth=False)
    art = GP(art, door, "#3a2a24", "#2a1d18", seed=nx(), rough=0.6)
    art = ink(art, W, H, [(arc_pts(230, 300, 76, math.pi, math.tau, 24), 4, None)], nx, col=WOOD_D, amt=0.7)
    # puppy peeking out of the door (tricolour floppy-eared)
    art, hm = head(art, W, H, 230, 368, 1.05, nx, rng, (TAN, TAN_L, TAN_D, TAN_L), ears="flop", ear_c=(BRN, BRN_L, BRN_D, BRN_L), blaze=WH, tongue=True)
    paws = ellipses(W, H, [(196, 438, 22, 13, 0), (264, 438, 22, 13, 0)])
    art = paint(art, paws, (WH, "#ffffff", WH_D, "#ffffff"), nx, blur=3)
    art = ink(art, W, H, [([(x, 434), (x, 444)], 2.2, None) for x in (188, 198, 256, 266)], nx, amt=0.6)
    # roof
    roof = shapes(W, H, [[(36, 206), (230, 40), (424, 206), (400, 222), (230, 76), (60, 222)]], smooth=False)
    art = paint(art, roof, (RED, RED_L, RED_D, "#ffa88a"), nx, ldir=(0, 10), blur=6)
    shingles = strokes(W, H, [([(230 - k * 22, 72 + k * 18.8), (230 + k * 22, 72 + k * 18.8)], 2, None) for k in range(1, 8)]) * roof
    art = tint(art, shingles, RED_D, 0.4, seed=nx())
    gable = shapes(W, H, [[(80, 190), (230, 70), (380, 190)]], smooth=False)
    art = paint(art, gable * (1 - roof), (WOOD, WOOD_L, WOOD_D, "#fff0c4"), nx, blur=6)
    art = bone(art, W, H, 230, 150, 84, nx)
    art = paint(art, shapes(W, H, [[(56, 440), (404, 440), (404, 454), (56, 454)]], smooth=False), (GRN_D, GRN, "#3a7a2a", GRN_L), nx, blur=3)
    preview(art, "ua-house", tone="#dff1fb")
    save(art, f"{OUT}/house.webp", max_w=400, quality=84)
    clear()

if "corgi" in PARTS:
    W, H = 300, 380
    nx = Seq(102000); rng = random.Random(5)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(150, 362, 100, 12, 20)]), "#4f7a3a", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=6)
    cols = (TAN, "#ee9f56", TAN_D, TAN_L)
    art = sitting(art, W, H, 150, 160, 1.0, nx, rng, cols, tail_side=1, legs=0.7)
    art, hm = head(art, W, H, 150, 160, 1.05, nx, rng, cols, ears="up", tongue=True)
    art = party_hat(art, W, H, 168, 108, 1.0, nx, ang=0.25, col=BLU)
    preview(art, "ua-corgi", tone="#dff1fb")
    save(art, f"{OUT}/corgi.webp", max_w=220, quality=84)
    clear()

if "spotty" in PARTS:
    W, H = 340, 380
    nx = Seq(103000); rng = random.Random(9)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(160, 362, 120, 12, 20)]), "#4f7a3a", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=6)
    cols = (WH, "#ffffff", WH_D, "#ffffff")
    art = sitting(art, W, H, 140, 150, 1.0, nx, rng, cols, tail_side=-1, legs=0.8)
    spots = circles(W, H, [(110, 230, 9), (168, 250, 7), (128, 270, 6), (178, 214, 8), (100, 196, 5)])
    art = GP(art, spots, BK, BK_L, seed=nx(), rough=0.8, pad=6)
    art, hm = head(art, W, H, 140, 150, 1.0, nx, rng, cols, ears="flop", ear_c=(BK, BK_L, BK_D, BK_L), spots=[(26, -26, 10), (-30, 4, 7), (6, -40, 6)], tongue=False, wink=True)
    art = ball(art, W, H, 262, 322, 40, nx)
    preview(art, "ua-spotty", tone="#dff1fb")
    save(art, f"{OUT}/spotty.webp", max_w=240, quality=84)
    clear()

if "ball" in PARTS:
    W, H = 120, 120
    nx = Seq(104000)
    art = ball(blank(W, H), W, H, 60, 60, 50, nx, col=(YEL, YEL_L, YEL_D, "#fff2b0"), stripe=BLU)
    preview(art, "ua-ball", tone="#dff1fb")
    save(art, f"{OUT}/ball.webp", max_w=90, quality=84)
    clear()

if "bone" in PARTS:
    W, H = 200, 90
    nx = Seq(105000)
    art = bone(blank(W, H), W, H, 100, 45, 170, nx)
    preview(art, "ua-bone", tone="#dff1fb")
    save(art, f"{OUT}/bone.webp", max_w=120, quality=84)
    clear()

if "paw" in PARTS:
    W, H = 100, 100
    nx = Seq(106000)
    m = np.clip(ellipses(W, H, [(50, 62, 22, 18, 0)]) + circles(W, H, [(24, 36, 9), (40, 22, 9.5), (60, 22, 9.5), (76, 36, 9)]), 0, 1)
    art = GP(blank(W, H), m, BRN, BRN_L, seed=nx(), rough=1.2, streak=0.5)
    preview(art, "ua-paw", tone="#dff1fb")
    save(art, f"{OUT}/paw.webp", max_w=50, quality=84)
    clear()

if "bunting" in PARTS:
    W, H = 840, 120
    nx = Seq(107000)
    art = blank(W, H)
    rope = curve([(0, 14), (210, 40), (420, 20), (630, 42), (840, 16)], 80)
    art = ink(art, W, H, [(rope, 3, None)], nx, col="#8a6a4a", amt=0.9)
    cols = [RED, YEL, BLU, GRN, PINK]
    flags = []
    for k, (x, y, _a) in enumerate(along(rope, 56)):
        flags.append((k, [(x - 22, y - 2), (x + 22, y + 2), (x + math.sin(_a) * 0 + 2, y + 52)]))
    for k, f in flags:
        c = cols[k % len(cols)]
        art = paint(art, shapes(W, H, [f], smooth=False), (c, mix(c, "#ffffff", .15), mix(c, INK, .3), mix(c, "#ffffff", .4)), nx, blur=3)
        if k % 2 == 0:
            cx_ = sum(p[0] for p in f) / 3; cy_ = sum(p[1] for p in f) / 3 - 4
            pm = np.clip(ellipses(W, H, [(cx_, cy_ + 4, 6, 5, 0)]) + circles(W, H, [(cx_ - 7, cy_ - 4, 2.6), (cx_ - 2.5, cy_ - 8, 2.6), (cx_ + 2.5, cy_ - 8, 2.6), (cx_ + 7, cy_ - 4, 2.6)]), 0, 1)
            art = GP(art, pm, "#ffffff", seed=nx(), rough=0.3, pad=4)
    preview(art, "ua-bunting", tone="#dff1fb")
    save(art, f"{OUT}/bunting.webp", max_w=840, quality=82)
    clear()

if "cake" in PARTS:
    W, H = 340, 300
    nx = Seq(108000); rng = random.Random(2)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(170, 280, 140, 12, 20)]), "#6a5a4a", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=6)
    plate = shapes(W, H, [ellipse_pts(170, 270, 140, 18, 24)])
    art = paint(art, plate, (WH, "#ffffff", WH_D, "#ffffff"), nx, blur=4)
    tier = shapes(W, H, [[(70, 262), (70, 170)] + arc_pts(170, 170, 100, math.pi, math.tau, 20, 0.2) + [(270, 170), (270, 262)] + arc_pts(170, 262, 100, 0, math.pi, 20, 0.2)[::-1]], smooth=False)
    art = paint(art, tier, (BLU_L, "#a4d4f6", BLU, "#d0ecff"), nx, ldir=(-14, 0), blur=12)
    drip = shapes(W, H, [[(70, 170)] + arc_pts(170, 170, 100, math.pi, math.tau, 20, 0.2) + [(270, 170), (270, 196)] +
                         [(270 - k * 12.5, 196 + (14 if k % 2 else 0) + rng.uniform(-2, 4)) for k in range(1, 16)] + [(70, 196)]], smooth=True)
    art = paint(art, drip, (WH, "#ffffff", WH_D, "#ffffff"), nx, blur=4)
    for k, x in enumerate((112, 170, 228)):
        art = bone(art, W, H, x, 234, 48, nx, ang=0.25 if k % 2 else -0.25)
    for k, x in enumerate((140, 170, 200)):
        cm = shapes(W, H, [[(x - 6, 154), (x + 6, 154), (x + 6, 104), (x - 6, 104)]], smooth=False)
        c = [RED, YEL, GRN][k]
        art = paint(art, cm, (c, mix(c, "#ffffff", .2), mix(c, INK, .3), mix(c, "#ffffff", .4)), nx, blur=2)
        fl = shapes(W, H, [petal_pts(x, 102, 20, 8, -math.pi / 2, n=12)])
        art = over(art, glow(fl, "#ffd36a", radius=8, strength=0.5))
        art = paint(art, fl, (YEL, YEL_L, "#f08a2a", "#fff6c0"), nx, blur=2, line=False)
    preview(art, "ua-cake", tone="#dff1fb")
    save(art, f"{OUT}/cake.webp", max_w=240, quality=84)
    clear()
