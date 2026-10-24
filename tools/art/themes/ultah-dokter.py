"""Ultah Dokter — a little doctor's birthday in kid-friendly gouache with plum outlines: a teddy-bear patient with a head
bandage and plasters, a red toy stethoscope, a first-aid kit, a single plaster (divider / decor) and a small birthday
cake with a red-cross topper. Palette: cream, tomato red, sky blue, plaster tan, honey yellow; plum ink.
Run: python3 -I ultah-dokter.py [part ...]   parts: teddy steto kit plester kue
Assets -> public/themes/art/ultah-dokter/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q1_lib import *  # noqa

OUT = outdir("ultah-dokter")
PARTS = sys.argv[1:] or ["teddy", "steto", "kit", "plester", "kue"]
PLUM = "#3b2a4a"
RED, RED_D = "#e5483b", "#b8322a"
SKY, SKY_D = "#8fc9ea", "#3f8fc4"
TAN, TAN_D = "#f2c48d", "#d69a5e"
HONEY = "#ffcf4a"
WHITE = "#fffaf3"
BEAR, BEAR_L, BEAR_D = "#c98a52", "#e0a96e", "#8a5530"


def sm(pts, k=10):
    """Closed Catmull-Rom resample so fills and outlines share one smooth geometry."""
    n = len(pts); out = []
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for j in range(k):
            t = j / k; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out


def ol(art, pts_list, seed, w=4.0, closed=True):
    items = []
    for pts in pts_list:
        p = list(pts) + ([pts[0]] if closed else [])
        items.append((p, w, (0, 0)))
    return line(art, items, seed, col=PLUM, rough=0.8)


def circ(cx, cy, r, n=40):
    return [(cx + math.cos(t) * r, cy + math.sin(t) * r) for t in np.linspace(0, math.tau, n, endpoint=False)]


def ell(cx, cy, rx, ry, rot=0, n=40):
    c, s_ = math.cos(rot), math.sin(rot)
    return [(cx + math.cos(t) * rx * c - math.sin(t) * ry * s_, cy + math.cos(t) * rx * s_ + math.sin(t) * ry * c) for t in np.linspace(0, math.tau, n, endpoint=False)]


def B(art, pts, col, seed, col2=None, shade=0.3, light=(0.3, 0.2)):
    W, H = art.shape[1], art.shape[0]
    return body(art, poly(W, H, pts, smooth=False), col, col2, seed=seed, shade=shade, dark=PLUM, light=light, rough=1.6)


def part_teddy():
    W, H = 440, 480
    nx = Seq(100)
    art = blank(W, H)
    shadow = ellipses(W, H, [(220, 452, 170, 16, 0)])
    art = G(art, shadow, PLUM, seed=nx(), density=0.22, edge=0.1, bloom=0, rough=3, feather=6)
    # legs (sitting, feet forward), body, arms, head, ears
    legs = [ell(140, 400, 62, 46, -0.3), ell(300, 400, 62, 46, 0.3)]
    bodyp = ell(220, 320, 120, 112)
    arms = [ell(108, 300, 38, 78, 0.5), ell(332, 300, 38, 78, -0.5)]
    ears = [circ(122, 74, 40), circ(318, 74, 40)]
    head = ell(220, 160, 128, 112)
    for pts in ears:
        art = B(art, pts, BEAR, nx())
        art = ol(art, [pts], nx(), 4.2)
        cx_, cy_ = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        art = B(art, [(cx_ + (x - cx_) * 0.55, cy_ + 6 + (y - cy_) * 0.55) for x, y in pts], BEAR_L, nx(), shade=0.15)
    art = B(art, bodyp, BEAR, nx(), BEAR_L)
    art = ol(art, [bodyp], nx(), 4.2)
    art = B(art, ell(220, 336, 72, 70), BEAR_L, nx(), shade=0.15)
    for pts in arms + legs:
        art = B(art, pts, BEAR, nx())
        art = ol(art, [pts], nx(), 4.2)
    art = B(art, ell(118, 410, 34, 28, -0.3), BEAR_L, nx(), shade=0.1)
    art = B(art, ell(322, 410, 34, 28, 0.3), BEAR_L, nx(), shade=0.1)
    art = B(art, head, BEAR, nx(), BEAR_L)
    art = ol(art, [head], nx(), 4.2)
    art = B(art, ell(220, 204, 58, 44), BEAR_L, nx(), shade=0.12)
    art = ol(art, [ell(220, 204, 58, 44)], nx(), 3)
    # face: eyes, nose, smile, cheeks
    art = GP(art, circles(W, H, [(178, 160, 10), (262, 160, 10)]), PLUM, seed=nx(), rough=0.5)
    art = GP(art, circles(W, H, [(174, 156, 3.2), (258, 156, 3.2)]), WHITE, seed=nx(), rough=0.3)
    art = body(art, ellipses(W, H, [(220, 190, 18, 13, 0)]), PLUM, seed=nx(), shade=0.0, rough=0.6)
    art = line(art, [(curve([(202, 216), (220, 228), (238, 216)], 16), 3.6, (0.1, 0.1)), ([(220, 202), (220, 222)], 3, (0, 0))], nx(), col=PLUM)
    art = G(art, circles(W, H, [(148, 200, 18), (292, 200, 18)]), "#f08a7a", seed=nx(), density=0.45, edge=0.1, rough=1.5, feather=3)
    # head bandage band (white gauze) across the forehead with a little knot
    band = strokes(W, H, [(curve([(98, 118), (160, 96), (220, 92), (280, 96), (342, 118)], 30), 26, (0.0, 0.0))]) * poly(W, H, head, smooth=True)
    art = body(art, band, WHITE, "#f1ece4", seed=nx(), shade=0.2, dark="#8f8798", rough=0.8)
    art = line(art, [(curve([(108, 104), (160, 84), (220, 80), (280, 84), (332, 104)], 30), 2.4, (0, 0)), (curve([(104, 130), (160, 110), (220, 106), (280, 110), (336, 130)], 30), 2.4, (0, 0))], nx(), col="#b9b0c2")
    knot = [ell(350, 100, 18, 11, 0.6), ell(362, 128, 16, 10, -0.4)]
    for k in knot:
        art = B(art, k, WHITE, nx(), shade=0.2)
    art = ol(art, knot, nx(), 2.6)
    # red-cross plaster on the tummy and a plaster on the knee
    tp = [(186, 300), (254, 288), (262, 322), (194, 334)]
    art = B(art, tp, TAN, nx(), shade=0.15)
    art = GP(art, poly(W, H, [(208, 300), (240, 294), (244, 318), (212, 324)], smooth=True), "#f7dcb6", seed=nx(), rough=0.5)
    art = GP(art, circles(W, H, [(214 + i * 8, 304 + j * 8 - i * 1.5, 1.6) for i in range(4) for j in range(2)]), TAN_D, seed=nx(), rough=0.3)
    art = ol(art, [tp], nx(), 2.6)
    kp = [(278, 386), (334, 368), (342, 390), (286, 408)]
    art = B(art, kp, TAN, nx(), shade=0.15)
    art = ol(art, [kp], nx(), 2.6)
    # small red heart sticker on the arm
    hx, hy = 340, 270
    heart = [(hx, hy + 14), (hx - 16, hy), (hx - 14, hy - 10), (hx - 6, hy - 12), (hx, hy - 6), (hx + 6, hy - 12), (hx + 14, hy - 10), (hx + 16, hy)]
    art = B(art, sm(heart, 6), RED, nx(), shade=0.15)
    art = ol(art, [sm(heart, 6)], nx(), 2.4)
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "ud-teddy", tone="#eaf5fb")
    save(art, f"{OUT}/teddy.webp", max_w=300, quality=84)
    clear()


def part_steto():
    W, H = 460, 360
    nx = Seq(400)
    art = blank(W, H)
    # Y-shaped red tube: two ear branches joining, then a long loop to the chest piece
    left = curve([(120, 40), (104, 90), (130, 150), (180, 180)], 30)
    right = curve([(240, 40), (256, 90), (230, 150), (180, 180)], 30)
    tube = curve([(180, 180), (176, 240), (220, 300), (300, 300), (350, 250), (360, 210)], 50)
    art = body(art, strokes(W, H, [(left, 13, (0, 0)), (right, 13, (0, 0)), (tube, 15, (0, 0))]), RED, "#f0645a", seed=nx(), shade=0.3, dark=RED_D, rough=1.0)
    art = GP(art, strokes(W, H, [(left[3:-6], 3, (0.2, 0.3)), (right[3:-6], 3, (0.2, 0.3)), (tube[4:-10], 3.5, (0.2, 0.3))]) * 1.0, "#ff9a90", seed=nx(), rough=0.6)
    art = line(art, [(left, 2.4, (0, 0)), (right, 2.4, (0, 0)), (tube, 2.4, (0, 0))], nx(), col=PLUM)
    # ear tips (honey balls) and metal yoke
    art = body(art, circles(W, H, [(120, 36, 14), (240, 36, 14)]), HONEY, seed=nx(), shade=0.3, dark=PLUM)
    art = ol(art, [circ(120, 36, 14), circ(240, 36, 14)], nx(), 2.6)
    art = body(art, ellipses(W, H, [(180, 182, 18, 12, 0)]), "#c9d3de", seed=nx(), shade=0.35, dark=PLUM)
    # chest piece: a big round disc
    cx, cy = 372, 196
    art = body(art, circles(W, H, [(cx, cy, 52)]), "#c9d3de", "#e6edf3", seed=nx(), shade=0.4, dark=PLUM)
    art = body(art, circles(W, H, [(cx, cy, 36)]), SKY, "#b5def4", seed=nx(), shade=0.25, dark=PLUM)
    art = ol(art, [circ(cx, cy, 52), circ(cx, cy, 36)], nx(), 3.4)
    cross = poly(W, H, [(cx - 7, cy - 20), (cx + 7, cy - 20), (cx + 7, cy - 7), (cx + 20, cy - 7), (cx + 20, cy + 7), (cx + 7, cy + 7), (cx + 7, cy + 20), (cx - 7, cy + 20), (cx - 7, cy + 7), (cx - 20, cy + 7), (cx - 20, cy - 7), (cx - 7, cy - 7)])
    art = GP(art, cross, WHITE, seed=nx(), rough=0.6)
    art = GP(art, strokes(W, H, [(arc_pts(cx, cy, 44, 3.6, 4.6, 10), 4, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.5)
    art = add_grain(art, seed=6, amount=0.03)
    preview(art, "ud-steto", tone="#eaf5fb")
    save(art, f"{OUT}/steto.webp", max_w=280, quality=84)
    clear()


def red_cross(W, H, cx, cy, a, b):
    return poly(W, H, [(cx - a, cy - b), (cx + a, cy - b), (cx + a, cy - a), (cx + b, cy - a), (cx + b, cy + a), (cx + a, cy + a), (cx + a, cy + b), (cx - a, cy + b), (cx - a, cy + a), (cx - b, cy + a), (cx - b, cy - a), (cx - a, cy - a)])


def part_kit():
    W, H = 380, 320
    nx = Seq(700)
    art = blank(W, H)
    art = G(art, ellipses(W, H, [(190, 294, 160, 14, 0)]), PLUM, seed=nx(), density=0.22, edge=0.1, bloom=0, rough=3, feather=6)
    # handle
    hd = curve([(140, 92), (146, 40), (234, 40), (240, 92)], 30)
    art = body(art, strokes(W, H, [(hd, 16, (0, 0))]), RED_D, seed=nx(), shade=0.2, dark=PLUM)
    art = line(art, [(hd, 2.4, (0, 0))], nx(), col=PLUM)
    # box: front + lid band
    box = [(40, 96), (340, 92), (346, 280), (34, 284)]
    art = B(art, box, WHITE, nx(), "#f2ece4", shade=0.3)
    lid = [(40, 96), (340, 92), (342, 128), (38, 132)]
    art = B(art, lid, RED, nx(), "#ef6a5e", shade=0.2)
    art = ol(art, [box], nx(), 4.2)
    art = line(art, [([(38, 132), (342, 128)], 3, (0, 0))], nx(), col=PLUM)
    art = body(art, rect(W, H, 176, 124, 204, 144), HONEY, seed=nx(), shade=0.2, dark=PLUM)
    art = ol(art, [[(176, 124), (204, 124), (204, 144), (176, 144)]], nx(), 2.4)
    cm = red_cross(W, H, 190, 208, 20, 54)
    art = body(art, cm, RED, "#ef6a5e", seed=nx(), shade=0.2, dark=PLUM)
    art = ol(art, [[(170, 154), (210, 154), (210, 188), (244, 188), (244, 228), (210, 228), (210, 262), (170, 262), (170, 228), (136, 228), (136, 188), (170, 188)]], nx(), 3)
    art = GP(art, strokes(W, H, [([(56, 150), (58, 260)], 6, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.6)
    # a plaster and a pill peeking out
    art = add_grain(art, seed=7, amount=0.03)
    preview(art, "ud-kit", tone="#eaf5fb")
    save(art, f"{OUT}/kit.webp", max_w=240, quality=84)
    clear()


def part_plester():
    W, H = 300, 110
    nx = Seq(900)
    art = blank(W, H)
    pts = sm([(30, 30), (270, 22), (282, 50), (272, 80), (32, 88), (20, 60)], 8)
    m = poly(W, H, pts, smooth=True)
    art = body(art, m, TAN, "#f7d2a3", seed=nx(), shade=0.2, dark=PLUM)
    pad = poly(W, H, [(110, 34), (190, 30), (192, 76), (112, 80)], smooth=False)
    art = body(art, pad, "#fbe6c8", seed=nx(), shade=0.1, dark=PLUM)
    holes = [(x, y, 2.2) for x in (50, 64, 78, 222, 236, 250) for y in (46, 64)]
    art = GP(art, circles(W, H, holes), TAN_D, seed=nx(), rough=0.3)
    art = GP(art, circles(W, H, [(122 + i * 13, 40 + j * 12, 1.8) for i in range(6) for j in range(4)]), "#e7bf8a", seed=nx(), rough=0.3)
    art = ol(art, [pts], nx(), 3.4)
    art = add_grain(art, seed=8, amount=0.03)
    preview(art, "ud-plester", tone="#eaf5fb")
    save(art, f"{OUT}/plester.webp", max_w=220, quality=84)
    clear()


def part_kue():
    W, H = 360, 380
    nx = Seq(1100)
    art = blank(W, H)
    art = G(art, ellipses(W, H, [(180, 352, 150, 14, 0)]), PLUM, seed=nx(), density=0.2, edge=0.1, bloom=0, rough=3, feather=6)
    plate = ell(180, 336, 150, 18)
    art = B(art, plate, "#e6edf3", nx(), shade=0.2)
    tier = [(60, 220), (300, 220), (300, 330), (60, 330)]
    art = B(art, tier, SKY, nx(), "#a8d6ef", shade=0.3)
    # white frosting drip on top
    drip = [(56, 214), (304, 214), (304, 244)] + [(304 - k * 31, 244 + (16 if k % 2 else 4)) for k in range(1, 8)] + [(56, 248)]
    art = B(art, drip, WHITE, nx(), shade=0.15)
    top = ell(180, 216, 124, 20)
    art = B(art, top, WHITE, nx(), shade=0.1)
    # sprinkles + a red-cross badge on the side
    import random as _r
    rr = _r.Random(3)
    spr = [([(x, y), (x + 6 * math.cos(a), y + 6 * math.sin(a))], 3, (0, 0)) for x, y, a in [(rr.uniform(80, 280), rr.uniform(270, 320), rr.uniform(0, 3)) for _ in range(22)]]
    cols = [RED, HONEY, WHITE]
    for i, c in enumerate(cols):
        art = GP(art, strokes(W, H, spr[i::3]), c, seed=nx(), rough=0.4)
    art = body(art, circles(W, H, [(180, 288, 26)]), WHITE, seed=nx(), shade=0.15, dark=PLUM)
    art = body(art, red_cross(W, H, 180, 288, 6, 17), RED, seed=nx(), shade=0.1, dark=PLUM)
    art = ol(art, [tier, top, circ(180, 288, 26), plate], nx(), 3.6)
    # candles with flames
    for i, x in enumerate((130, 180, 230)):
        c = [(x - 7, 214), (x + 7, 214), (x + 7, 150), (x - 7, 150)]
        art = B(art, c, [RED, HONEY, SKY_D][i], nx(), shade=0.2)
        art = GP(art, strokes(W, H, [([(x - 7, 196 - k * 18), (x + 7, 186 - k * 18)], 3, (0, 0)) for k in range(3)]) * poly(W, H, c), WHITE, seed=nx(), rough=0.4)
        art = ol(art, [c], nx(), 2.6)
        fl = [(x, 112), (x + 9, 132), (x + 6, 144), (x - 6, 144), (x - 9, 132)]
        art = B(art, sm(fl, 6), HONEY, nx(), "#ffe28a", shade=0.1)
        art = GP(art, poly(W, H, [(x, 126), (x + 4, 136), (x, 142), (x - 4, 136)], smooth=True), "#ff8f3a", seed=nx(), rough=0.3)
    art = add_grain(art, seed=9, amount=0.03)
    preview(art, "ud-kue", tone="#eaf5fb")
    save(art, f"{OUT}/kue.webp", max_w=260, quality=84)
    clear()


for p in PARTS:
    globals()[f"part_{p}"]()
kb_report(OUT)
