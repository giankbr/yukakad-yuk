"""Ultah Safari — kids birthday on a golden savanna in gouache + crayon (original characters): a tall friendly giraffe,
a little elephant with a curled trunk, a sitting lion cub, a flat-topped acacia, an open safari jeep with a spare tyre,
and a golden grass strip. Run: python3 -I ultah-safari.py [part ...]
parts: giraffe elephant lion acacia jeep grass   Assets -> public/themes/art/ultah-safari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e5_lib import *  # noqa

OUT = outdir("ultah-safari")
PARTS = sys.argv[1:] or ["giraffe", "elephant", "lion", "acacia", "jeep", "grass"]
INK = "#3a2618"
GIR, GIR2, GIRD, GIRL, SPOT = "#f2b44e", "#f6c46a", "#c47f2a", "#ffe0a0", "#b9622c"
ELE, ELE2, ELED, ELEL = "#93a3b4", "#a2b1c0", "#617286", "#cbd6e0"
LIO, LIO2, LIOD, LIOL, MANE, MANED = "#e9a744", "#efb65c", "#b57425", "#ffd896", "#c0662c", "#8f4520"
OLV, OLV2, OLVD, OLVL = "#7d8a3c", "#8f9b48", "#525c24", "#b9c27a"
KHA, KHA2, KHAD, KHAL = "#cdb46c", "#d8c07c", "#94803f", "#efe0a8"
GRASS, GRASS2, GRASSD = "#d9a845", "#e6bb5a", "#a87a2a"
CREAM = "#fff3dc"
BG = "#fbefd9"


def outline(art, m, nx, col, amt=0.7):
    return crayon(art, inner_edge(m, 2.4), mix(col, INK, .45), seed=nx(), amt=amt, tooth=0.3)


def part(art, m, c, c2, d, l, nx, ldir=(12, 12), blur=10, line=True):
    art = body_paint(art, m, c, c2, d, l, nx, ldir=ldir, blur=blur, light_amt=0.4, dark_amt=0.55)
    return outline(art, m, nx, d) if line else art


def spots(W, H, region, rng, n, rmin, rmax, avoid=None):
    polys = []
    ys, xs = np.where(region > 0.5)
    if len(xs) == 0:
        return np.zeros((H, W), np.float32)
    for _ in range(n):
        i = rng.randrange(len(xs))
        x, y = xs[i], ys[i]
        if avoid is not None and avoid[y, x] > 0.2:
            continue
        r = rng.uniform(rmin, rmax)
        polys.append(deform(ellipse_pts(x, y, r, r * rng.uniform(0.7, 1.0), 6, rng.uniform(0, 3)), rng, 1, 0.06))
    return shapes(W, H, polys) * region


if "giraffe" in PARTS:
    W, H = 460, 760
    nx = Seq(10100); rng = random.Random(1010)
    art = blank(W, H)
    art = soft_ground(art, W, H, 210, 728, 160, 14, "#6a4a30", nx, 0.35)
    # far legs (darker)
    far = strokes(W, H, [([(150, 520), (146, 712)], 24, (0.0, 0.0)), ([(268, 520), (276, 712)], 24, (0.0, 0.0))])
    art = part(art, far, GIRD, GIR, "#9a5f1e", GIR, nx, blur=6)
    tail = strokes(W, H, [(curve([(88, 470), (70, 520), (66, 580)], 20), 5, (0.0, 0.2))])
    art = GP(art, tail, GIRD, seed=nx(), rough=0.4, pad=6)
    art = GP(art, petal_pts(66, 576, 26, 9, math.pi / 2, 12) and shapes(W, H, [petal_pts(66, 572, 28, 9, math.pi / 2, 12)]), INK, seed=nx(), rough=0.4, pad=6)
    # body + neck + near legs
    body = ellipses(W, H, [(190, 480, 118, 70, -6)])
    neck = shapes(W, H, [[(236, 470), (262, 300), (290, 170), (330, 160), (322, 300), (300, 480)]])
    legs = strokes(W, H, [([(120, 520), (112, 716)], 26, (0.0, 0.0)), ([(246, 524), (240, 716)], 26, (0.0, 0.0))])
    torso = np.clip(body + neck + legs, 0, 1)
    art = part(art, torso, GIR, GIR2, GIRD, GIRL, nx, ldir=(14, 12), blur=16)
    sp = spots(W, H, np.clip(body + neck, 0, 1), rng, 70, 11, 19)
    art = GP(art, sp, SPOT, "#c87438", seed=nx(), rough=0.8, pad=6)
    art = GP(art, spots(W, H, legs * (np.arange(H)[:, None] < 620), rng, 14, 7, 10), SPOT, seed=nx(), rough=0.6, pad=6)
    art = tint(art, side_light(torso, 14, 12, 16), GIRD, 0.35, seed=nx())
    hooves = shapes(W, H, [[(x - 15, 700), (x + 15, 700), (x + 16, 722), (x - 16, 722)] for x in (112, 240)], smooth=False)
    art = GP(art, hooves, INK, "#4a3424", seed=nx(), rough=0.4, pad=6)
    # mane along the back of the neck
    def _nb(y):
        # back edge of the neck: (236,470)->(262,300)->(290,170)
        return 236 + (470 - y) / 170 * 26 if y > 300 else 262 + (300 - y) / 130 * 28
    mane = strokes(W, H, [([(_nb(y) + 6, y), (_nb(y) - 9, y - 6)], 9, (0.2, 0.2)) for y in range(450, 176, -17)])
    art = GP(art, mane * (1 - neck * 0.0), MANED, MANE, seed=nx(), rough=0.6, pad=6)
    # head
    head = shapes(W, H, [deform(ellipse_pts(330, 132, 56, 36, 16, 0.32), rng, 1, 0.006)])
    art = part(art, head, GIR, GIR2, GIRD, GIRL, nx, ldir=(8, 10), blur=10)
    muzzle = ellipses(W, H, [(368, 152, 30, 22, 20)]) * head
    art = GP(art, muzzle, "#f8d9a0", "#f2cf92", seed=nx(), rough=0.6, pad=6)
    art = GP(art, ellipses(W, H, [(380, 150, 4, 3, 20), (368, 156, 4, 3, 20)]), INK, seed=nx(), rough=0.3, pad=6)
    # ossicones + ear
    oss = strokes(W, H, [([(306, 104), (300, 66)], 8, None), ([(326, 100), (326, 62)], 8, None)])
    art = part(art, oss, GIR, GIR2, GIRD, GIRL, nx, blur=3)
    art = part(art, circles(W, H, [(300, 62, 9), (326, 58, 9)]), MANED, MANE, INK, MANE, nx, blur=3)
    ear = shapes(W, H, [petal_pts(296, 116, 42, 13, math.pi + 0.5, 12)])
    art = part(art, ear, GIR, GIR2, GIRD, GIRL, nx, blur=4)
    art = GP(art, shapes(W, H, [petal_pts(290, 112, 28, 6, math.pi + 0.5, 12)]), "#f19a86", seed=nx(), rough=0.4, pad=6)
    art = eye(art, W, H, 336, 120, 7.5, nx)
    art = crayon(art, strokes(W, H, [(arc_pts(336, 120, 11, -2.6, -1.0, 8), 2.2, None)]), INK, seed=nx(), amt=0.8)
    art = cheek(art, W, H, 344, 146, 9, nx)
    art = smile(art, W, H, 370, 158, 11, nx, a0=0.6, a1=2.3, w=2.6)
    preview(art, "sf-giraffe", tone=BG)
    save(art, f"{OUT}/giraffe.webp", max_w=230, quality=82)
    clear()

if "elephant" in PARTS:
    W, H = 600, 480
    nx = Seq(10200); rng = random.Random(1020)
    art = blank(W, H)
    art = soft_ground(art, W, H, 310, 448, 220, 16, "#6a4a30", nx, 0.35)
    farlegs = shapes(W, H, [[(x - 28, 300), (x + 28, 300), (x + 30, 432), (x - 30, 432)] for x in (250, 430)])
    art = part(art, farlegs, ELED, ELE, "#4a586a", ELE, nx, blur=8)
    tail = strokes(W, H, [(curve([(488, 260), (520, 300), (524, 340)], 20), 6, (0.0, 0.2))])
    art = GP(art, tail, ELED, seed=nx(), rough=0.4, pad=6)
    body = ellipses(W, H, [(350, 270, 160, 112, 0)])
    legs = shapes(W, H, [[(x - 32, 310), (x + 32, 310), (x + 34, 440), (x - 34, 440)] for x in (210, 390)])
    head = circles(W, H, [(170, 196, 96)])
    trunk = strokes(W, H, [(curve([(110, 220), (82, 290), (70, 350), (52, 392), (30, 380), (34, 352)], 60), 44, (0.0, 0.6))])
    whole = np.clip(body + legs + head + trunk, 0, 1)
    art = part(art, whole, ELE, ELE2, ELED, ELEL, nx, ldir=(14, 14), blur=18)
    # trunk wrinkles + toenails
    wr = strokes(W, H, [(arc_pts(x, y, 16, -0.6, 0.9, 8), 2.4, None) for x, y in ((92, 270), (80, 300), (72, 330), (62, 360))])
    art = crayon(art, wr * trunk, ELED, seed=nx(), amt=0.7)
    nails = circles(W, H, [(x + dx, 434, 9) for x in (210, 390) for dx in (-18, 0, 18)])
    art = GP(art, nails, CREAM, "#f6e6c6", seed=nx(), rough=0.3, pad=6)
    # ear
    ear = shapes(W, H, [deform([(210, 112), (290, 104), (330, 170), (318, 260), (262, 296), (222, 260), (206, 190)], rng, 1, 0.01)])
    art = part(art, ear, ELE2, ELE, ELED, ELEL, nx, ldir=(10, 10), blur=12)
    inner = shapes(W, H, [deform([(230, 136), (284, 132), (308, 182), (298, 246), (258, 268), (234, 236), (226, 180)], rng, 1, 0.01)]) * ear
    art = GP(art, inner, "#e9b3b0", "#f0c2bd", seed=nx(), rough=0.8, pad=6)
    art = eye(art, W, H, 150, 176, 9, nx)
    art = cheek(art, W, H, 130, 214, 13, nx)
    art = smile(art, W, H, 160, 232, 16, nx, a0=0.3, a1=1.8, w=3)
    # little party hat (it's a birthday!)
    hat = shapes(W, H, [[(130, 112), (190, 100), (150, 30)]], smooth=False)
    art = part(art, hat, "#e25b4b", "#ec7060", "#a83a2e", "#f8a090", nx, blur=5)
    art = GP(art, stripes(W, H, 0.4, 7, 12, seed=nx()) * hat, "#fde3a0", seed=nx(), rough=0.4)
    art = part(art, circles(W, H, [(150, 30, 11)]), "#f6c44a", "#ffd86a", "#c2901e", "#fff0b0", nx, blur=3)
    preview(art, "sf-elephant", tone=BG)
    save(art, f"{OUT}/elephant.webp", max_w=300, quality=82)
    clear()

if "lion" in PARTS:
    W, H = 420, 440
    nx = Seq(10300); rng = random.Random(1030)
    art = blank(W, H)
    art = soft_ground(art, W, H, 210, 414, 140, 12, "#6a4a30", nx, 0.35)
    tail = strokes(W, H, [(curve([(270, 380), (340, 390), (370, 340), (352, 300)], 40), 9, (0.0, 0.1))])
    art = GP(art, tail, LIO, LIO2, seed=nx(), rough=0.5, pad=6)
    art = part(art, shapes(W, H, [petal_pts(352, 304, 30, 13, -math.pi / 2 - 0.3, 12)]), MANE, MANED, MANED, MANE, nx, blur=3)
    body = shapes(W, H, [[(120, 400), (130, 300), (170, 236), (250, 236), (290, 300), (300, 400)]])
    art = part(art, body, LIO, LIO2, LIOD, LIOL, nx, ldir=(12, 10), blur=16)
    belly = ellipses(W, H, [(210, 330, 46, 60, 0)]) * body
    art = GP(art, belly, "#f6d396", "#f2c884", seed=nx(), rough=0.8, pad=6)
    paws = ellipses(W, H, [(176, 398, 30, 18, 0), (246, 398, 30, 18, 0)])
    art = part(art, paws, LIO2, LIO, LIOD, LIOL, nx, blur=5)
    art = crayon(art, strokes(W, H, [([(x, 392), (x, 410)], 2, None) for x in (168, 184, 238, 254)]), LIOD, seed=nx(), amt=0.7)
    # mane: lobed blob
    lobes = [(200 + math.cos(a) * 92, 166 + math.sin(a) * 86, 34) for a in np.linspace(0, math.tau, 14, endpoint=False)]
    mane = np.clip(circles(W, H, lobes) + circles(W, H, [(200, 166, 96)]), 0, 1)
    art = part(art, mane, MANE, "#c9743a", MANED, "#e09a5a", nx, ldir=(10, 10), blur=14)
    tufts = strokes(W, H, [([(200 + math.cos(a) * 70, 166 + math.sin(a) * 66), (200 + math.cos(a) * 104, 166 + math.sin(a) * 98)], 5, (0.2, 0.6)) for a in np.linspace(0, math.tau, 22, endpoint=False)])
    art = crayon(art, tufts * mane, MANED, seed=nx(), amt=0.55)
    ears = circles(W, H, [(140, 104, 22), (262, 104, 22)])
    art = part(art, ears, LIO, LIO2, LIOD, LIOL, nx, blur=4)
    art = GP(art, circles(W, H, [(140, 106, 11), (262, 106, 11)]), "#f2a48c", seed=nx(), rough=0.4, pad=6)
    head = shapes(W, H, [deform(ellipse_pts(201, 172, 72, 66, 18), rng, 1, 0.006)])
    art = part(art, head, LIO, LIO2, LIOD, LIOL, nx, ldir=(10, 10), blur=12)
    muzzle = ellipses(W, H, [(186, 204, 24, 18, 0), (216, 204, 24, 18, 0)])
    art = GP(art, muzzle, "#fbe6bf", "#f6dcae", seed=nx(), rough=0.5, pad=6)
    nose = shapes(W, H, [[(188, 184), (214, 184), (201, 200)]])
    art = part(art, nose, "#8a4a3a", "#9c5a48", "#5a2a20", "#c08070", nx, blur=3)
    art = eye(art, W, H, 174, 162, 8.5, nx)
    art = eye(art, W, H, 228, 162, 8.5, nx)
    art = cheek(art, W, H, 160, 196, 11, nx)
    art = cheek(art, W, H, 242, 196, 11, nx)
    art = smile(art, W, H, 192, 206, 9, nx, a0=0.3, a1=2.0, w=2.4)
    art = smile(art, W, H, 210, 206, 9, nx, a0=1.1, a1=2.8, w=2.4)
    whisk = strokes(W, H, [([(166, 208), (138, 204)], 1.6, None), ([(166, 214), (140, 218)], 1.6, None), ([(236, 208), (264, 204)], 1.6, None), ([(236, 214), (262, 218)], 1.6, None)])
    art = crayon(art, whisk, LIOD, seed=nx(), amt=0.6)
    preview(art, "sf-lion", tone=BG)
    save(art, f"{OUT}/lion.webp", max_w=210, quality=82)
    clear()

if "acacia" in PARTS:
    W, H = 640, 460
    nx = Seq(10400); rng = random.Random(1040)
    art = blank(W, H)
    br = [(curve([(320, 452), (318, 360), (300, 280), (240, 170)], 30), 22, (0.0, 0.7)),
          (curve([(318, 360), (346, 280), (410, 170)], 30), 16, (0.0, 0.7)),
          (curve([(304, 300), (250, 240), (150, 190)], 30), 10, (0.0, 0.8)),
          (curve([(350, 280), (430, 230), (510, 186)], 30), 10, (0.0, 0.8)),
          (curve([(300, 260), (320, 200), (330, 150)], 20), 8, (0.0, 0.8))]
    trunk = strokes(W, H, br)
    art = part(art, trunk, "#7a5232", "#8a6040", "#4e3220", "#a88060", nx, ldir=(8, 0), blur=6)
    can = []
    for cx, cy, rx, ry in ((210, 160, 140, 36), (420, 156, 160, 38), (320, 120, 190, 40), (150, 186, 70, 20), (520, 182, 80, 20)):
        can.append(deform(ellipse_pts(cx, cy, rx, ry, 18), rng, 2, 0.05))
    cm = shapes(W, H, can)
    art = part(art, cm, OLV, OLV2, OLVD, OLVL, nx, ldir=(0, 14), blur=14)
    dab = []
    for _ in range(120):
        ys, xs = np.where(cm > 0.6)
        i = rng.randrange(len(xs))
        dab.append(deform(ellipse_pts(xs[i], ys[i] - 4, rng.uniform(8, 16), rng.uniform(3, 6), 8), rng, 1, 0.08))
    art = GP(art, shapes(W, H, dab) * cm, OLVL, OLV2, seed=nx(), rough=0.8, pad=6)
    art = tint(art, side_light(cm, 0, 12, 10), OLVD, 0.45, seed=nx())
    preview(art, "sf-acacia", tone=BG)
    save(art, f"{OUT}/acacia.webp", max_w=320, quality=80)
    clear()

if "jeep" in PARTS:
    W, H = 640, 380
    nx = Seq(10500); rng = random.Random(1050)
    art = blank(W, H)
    art = soft_ground(art, W, H, 330, 344, 260, 16, "#6a4a30", nx, 0.35)
    # spare tyre (rear)
    art = wheel(art, W, H, 92, 200, 46, nx, hub=KHA, hub2=KHAD, bolt="#5a4a28")
    body = np.clip(gaussian_filter(shapes(W, H, [[(110, 170), (420, 170), (440, 198), (556, 206), (582, 226), (590, 300), (106, 300)]], smooth=False), 2.0) * 1.4, 0, 1)
    art = part(art, body, KHA, KHA2, KHAD, KHAL, nx, ldir=(10, 12), blur=14)
    stripe = shapes(W, H, [[(108, 236), (588, 244), (588, 262), (108, 254)]], smooth=False) * body
    art = GP(art, stripe, OLV, OLV2, seed=nx(), rough=0.5)
    art = GP(art, stripes(W, H, 1.2, 9, 14, seed=nx()) * stripe, "#fbefd9", seed=nx(), rough=0.4)
    # windscreen frame + roll bar
    frame = strokes(W, H, [([(424, 172), (396, 70)], 9, None), ([(396, 70), (440, 70)], 7, None), ([(440, 70), (446, 196)], 7, None)])
    art = part(art, frame, OLVD, OLV, "#3a4218", OLV, nx, blur=3)
    art = OV(art, shapes(W, H, [[(404, 82), (434, 82), (440, 168), (426, 168)]], smooth=False), lambda m: col_arr(m, "#cfe9f5", m * 0.55), pad=4)
    roll = strokes(W, H, [(curve([(170, 172), (190, 90), (300, 80), (330, 172)], 40), 8, None)])
    art = part(art, roll, OLVD, OLV, "#3a4218", OLV, nx, blur=3)
    # seats
    art = part(art, shapes(W, H, [[(230, 120), (262, 120), (270, 172), (226, 172)], [(340, 124), (370, 124), (378, 172), (334, 172)]]), "#8a5a34", "#9a6a40", "#5a3a20", "#c08a5a", nx, blur=4)
    # door line, handle, headlight, bumper, grille
    art = crayon(art, strokes(W, H, [([(300, 178), (300, 296)], 2.4, None), ([(300, 178), (420, 178)], 2.4, None)]), KHAD, seed=nx(), amt=0.7)
    art = GP(art, strokes(W, H, [([(380, 210), (404, 210)], 6, None)]), "#5a4a28", seed=nx(), rough=0.3, pad=6)
    art = OV(art, circles(W, H, [(566, 222, 11)]), lambda m: glow(m, "#fff1b0", 10, 0.5), pad=30)
    art = part(art, circles(W, H, [(566, 222, 10)]), "#fff6cf", "#ffffff", "#e3c76a", "#ffffff", nx, blur=3)
    art = part(art, shapes(W, H, [[(560, 288), (604, 288), (604, 306), (560, 306)]], smooth=False), OLVD, OLV, "#3a4218", OLV, nx, blur=3)
    # mudguard arches
    for x in (190, 480):
        art = part(art, shapes(W, H, [arc_pts(x, 300, 66, math.pi, 2 * math.pi, 20) + arc_pts(x, 300, 52, 2 * math.pi, math.pi, 20)]), OLVD, OLV, "#3a4218", OLV, nx, blur=3)
        art = wheel(art, W, H, x, 304, 50, nx, hub=KHA, hub2=KHAD, bolt="#5a4a28")
    # a little pennant on the roll bar
    art = part(art, strokes(W, H, [([(186, 104), (176, 30)], 4, None)]), "#5a4a28", "#6a5a38", INK, "#8a7a58", nx, blur=2)
    art = part(art, shapes(W, H, [[(178, 32), (236, 46), (180, 62)]], smooth=False), "#e25b4b", "#ec7060", "#a83a2e", "#f8a090", nx, blur=3)
    preview(art, "sf-jeep", tone=BG)
    save(art, f"{OUT}/jeep.webp", max_w=320, quality=82)
    clear()

if "grass" in PARTS:
    W, H = 900, 220
    nx = Seq(10600); rng = random.Random(1060)
    art = blank(W, H)
    top = lambda x: 90 + 8 * math.sin(x * 0.01) + 4 * math.sin(x * 0.05)
    g = shapes(W, H, [contour(top, -10, 910) + [(910, 230), (-10, 230)]])
    art = GP(art, g, GRASS, GRASS2, seed=nx(), rough=2.5, streak=0.6)
    art = tint(art, gaussian_filter(g, 18) * (np.arange(H)[:, None] / H), "#b07a30", 0.35, seed=nx())
    for col, n, L in ((GRASSD, 260, (18, 40)), ("#c49638", 260, (16, 36)), ("#f0cc72", 200, (12, 30))):
        items = []
        for _ in range(n):
            x = rng.uniform(-10, 910)
            y = rng.uniform(top(x) + 4, H)
            a = -math.pi / 2 + rng.uniform(-0.5, 0.5)
            l_ = rng.uniform(*L) * (0.6 + 0.4 * (1 - (y - 90) / 130))
            items.append((curve([(x, y), (x + math.cos(a) * l_ * .5 + rng.uniform(-3, 3), y + math.sin(a) * l_ * .5), (x + math.cos(a) * l_, y + math.sin(a) * l_)], 8), 3.0, (0.0, 0.9)))
        art = GP(art, strokes(W, H, items), col, seed=nx(), rough=0.6, pad=6)
        clear()
    rocks = [deform(ellipse_pts(x, top(x) + 40, rng.uniform(14, 24), rng.uniform(8, 12), 10), rng, 1, 0.05) for x in (150, 610, 790)]
    art = body_paint(art, shapes(W, H, rocks), "#b8a48a", "#c8b49a", "#7a6a55", "#e0d2bc", nx, ldir=(6, 6), blur=6)
    preview(art, "sf-grass", tone=BG)
    save(art, f"{OUT}/grass.webp", max_w=640, quality=78)
    clear()
