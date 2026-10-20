"""Tujuh Bulanan — transparent watercolour: janur band + hanging strips, bokor kembang setaman (bowl / floating
flowers / ripple layers on one canvas), seven-petal bloom, drifting petal sprites, siraman still life, paper tile.
Run: python3 -I /tmp/pen/art/themes/tujuh-bulanan.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _h_common import *

D = outdir("tujuh-bulanan")
ROSE, ROSE_D, ROSE_L = "#d27f88", "#a24e5c", "#f2c4c4"
JANUR, JANUR_D, JANUR_L = "#c3cc72", "#7f8c38", "#e3e6a6"
OCHRE, OCHRE_D, UMBER = "#dcae52", "#b07d2c", "#7d5222"
AQUA, AQUA_D = "#cfe6e2", "#94c4bf"
sd = Seeds(900)


def save_full(arr, path, quality=82):
    to_image(arr).save(path, "WEBP", quality=quality, method=6)
    return to_image(arr).size


def wash(dst, mask, a, b=None, **kw):
    kw.setdefault("seed", sd())
    return glaze(dst, pigment(mask, a, b, **kw))


# ---------------- janur ----------------
def janur_band():
    W, H = 780, 52
    rng = random.Random(2)
    art = blank(W, H)
    band = poly_mask(W, H, [(0, 0), (W, 0), (W, 32), (0, 32)])
    art = wash(art, band, JANUR, JANUR_L, density=0.7, edge=0.25, bloom=0.3, rough=2, feather=1.0)
    teeth = []
    for i in range(66):
        x = i * 12
        teeth += [(x, 31), (x + 6, 44 + rng.uniform(-1.5, 1.5))]
    teeth += [(W, 31), (W, 30), (0, 30)]
    art = wash(art, poly_mask(W, H, teeth), JANUR, JANUR_D, density=0.62, edge=0.5, bloom=0.2, rough=1.4, feather=0.8)
    # woven diagonals: alternating darker and lighter strokes
    for i in range(-4, 70):
        x = i * 12
        m = stroke_mask(W, H, [(x, 0), (x + 24, 32)], 3.2, (.02, .02))
        art = wash(art, m * band, JANUR_D, density=0.3, edge=0.2, bloom=0, rough=1, feather=0.6)
        m2 = stroke_mask(W, H, [(x + 24, 0), (x, 32)], 2.0, (.02, .02))
        art = wash(art, m2 * band, "#a9b55a", density=0.18, edge=0.1, bloom=0, rough=1, feather=0.6)
    return art


def janur_strip(length, k):
    W, H = 34, int(length + 14)
    rng = random.Random(10 + k)
    art = blank(W, H)
    x = W / 2
    pts = []
    for i in range(14):
        t = i / 13
        pts.append((x - 9 * math.sin(math.pi * min(1, t * 1.15)) ** 0.7 + rng.uniform(-.4, .4), 4 + t * length))
    for i in range(13, -1, -1):
        t = i / 13
        pts.append((x + 9 * math.sin(math.pi * min(1, t * 1.15)) ** 0.7 + rng.uniform(-.4, .4), 4 + t * length))
    m = shape_mask(W, H, pts)
    art = wash(art, m, [JANUR, "#cfd58a"][k % 2], JANUR_L, density=0.72, edge=0.55, bloom=0.3, rough=1.2, feather=0.8)
    rib = stroke_mask(W, H, [(x, 6), (x + .5, length * .92)], 1.4, (.05, .3))
    art = wash(art, rib, JANUR_D, density=0.45, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    return art


# ---------------- bokor ----------------
BW, BH = 420, 290


def bowl():
    rng = random.Random(4)
    art = blank(BW, BH)
    foot = poly_mask(BW, BH, deform([(162, 222), (258, 222), (280, 262), (140, 262)], rng, 1, 0.006))
    art = wash(art, foot, OCHRE, OCHRE_D, density=0.8, edge=0.5, bloom=0.2, rough=2)
    art = wash(art, foot * shape_mask(BW, BH, rect_pts(222, 220, 70, 46, 2), smooth=False), UMBER, density=0.4, edge=0.3, bloom=0.1, rough=2)
    body_pts = [(40, 112)] + curve([(40, 112), (70, 200), (210, 230), (350, 200), (380, 112)], 50) + [(380, 112)]
    body = shape_mask(BW, BH, body_pts)
    art = wash(art, body, "#e3bb65", OCHRE, density=0.72, edge=0.45, bloom=0.35, rough=3, holes=0.04)
    # form: umber shadow wash lower right, second deeper glaze at the bottom curve
    sh = body * np.clip(shift(gaussian_filter(body, 18), -40, -26) < 0.6, 0, 1).astype(np.float32)
    art = wash(art, gaussian_filter(sh, 3) * body, OCHRE_D, UMBER, density=0.55, edge=0.4, bloom=0.3, rough=4)
    art = wash(art, body * poly_mask(BW, BH, [(60, 196), (380, 150), (380, 240), (60, 240)]), UMBER, density=0.28, edge=0.3, bloom=0.2, rough=4)
    # engraved bands (thin darker washes) + lifted highlight (knock out a stroke so the paper shows)
    for (y0, amp, col, dens) in [(140, 26, UMBER, .35), (166, 22, OCHRE_D, .3)]:
        band = [(56 + i * 6.2, y0 + amp * math.sin(math.pi * i / 49)) for i in range(50)]
        art = wash(art, stroke_mask(BW, BH, band, 2.4, (.05, .05)) * body, col, density=dens, edge=.2, bloom=0, rough=1, feather=.7)
    hi = stroke_mask(BW, BH, curve([(78, 134), (96, 176), (140, 204)], 30), 12, (.3, .4))
    art = knockout(art, hi * body, amount=0.75, grow=2.5)
    # rim ring + water
    rim = shape_mask(BW, BH, ellipse_pts(210, 112, 172, 38, 40))
    art = wash(art, rim, "#e8c06a", OCHRE_D, density=0.8, edge=0.6, bloom=0.2, rough=2)
    water = shape_mask(BW, BH, ellipse_pts(210, 112, 160, 30, 40))
    art = knockout(art, water, amount=1.0, grow=0.6)
    art = wash(art, water, AQUA, AQUA_D, density=0.62, edge=0.5, bloom=0.45, rough=3)
    # shadowed far inner wall of the bowl (top of the water ellipse)
    far = water * poly_mask(BW, BH, [(40, 70), (380, 70), (380, 104), (40, 104)])
    art = wash(art, gaussian_filter(far, 2), "#9fb7a8", density=0.35, edge=0.2, bloom=0.2, rough=3)
    return art


def flowers():
    rng = random.Random(6)
    art = blank(BW, BH)
    def rose(cx, cy, r):
        nonlocal art
        base = shape_mask(BW, BH, deform(ellipse_pts(cx, cy, r, r * .78, 10), rng, 2, .1))
        art = wash(art, base, ROSE_L, ROSE, density=0.55, edge=0.45, bloom=0.4, rough=3)
        for k in range(6):
            rr = r * (0.9 - k * 0.13)
            a0 = rng.uniform(0, math.tau)
            pts = arc_pts(cx, cy, rr, a0, a0 + rng.uniform(1.6, 2.6), 18, 0.78)
            art = wash(art, stroke_mask(BW, BH, pts, r * .2), mix(ROSE, ROSE_D, k / 6), density=0.45 + k * .05, edge=.6, bloom=.1, rough=1.5, feather=.8)
        art = wash(art, shape_mask(BW, BH, ellipse_pts(cx, cy, r * .18, r * .14, 8)), ROSE_D, density=.7, edge=.6, bloom=0, rough=1)
    def melati(cx, cy, r, n=5):
        nonlocal art
        for i in range(n):
            a = -math.pi / 2 + i * math.tau / n + rng.uniform(-.1, .1)
            m = shape_mask(BW, BH, petal_pts(cx, cy, r, r * .42, a, n=12))
            art = wash(art, m, "#fbfaf5", "#e4e6e0", density=0.75, edge=0.8, bloom=0.1, rough=1.2, feather=.8)
        art = wash(art, shape_mask(BW, BH, ellipse_pts(cx, cy, r * .2, r * .2, 8)), "#e6cf62", density=.8, edge=.5, bloom=0, rough=1)
    def kenanga(cx, cy):
        nonlocal art
        for i in range(6):
            a = i * math.tau / 6 + .2
            m = shape_mask(BW, BH, petal_pts(cx, cy, 30, 4.6, a, n=12, cup=.4))
            art = wash(art, m, "#dcd165", "#b9b346", density=.7, edge=.55, bloom=.2, rough=1)
    def kantil(cx, cy):
        nonlocal art
        for a in (-.4, .35, 1.2):
            m = shape_mask(BW, BH, petal_pts(cx, cy, 34, 8, a + math.pi, n=12))
            art = wash(art, m, "#fbf5df", "#ece1bd", density=.8, edge=.75, bloom=.15, rough=1.2)
    kenanga(206, 106)
    rose(140, 100, 26)
    melati(262, 98, 15); melati(88, 112, 11); melati(178, 124, 9)
    kantil(314, 118)
    for i in range(10):  # loose petals on the water
        x, y = rng.uniform(80, 340), rng.uniform(96, 130)
        m = dab(BW, BH, x, y, 5, 3, rng.uniform(0, 3), rng)
        art = wash(art, m, rng.choice([ROSE, "#f6f3ea", "#dcd165"]), density=.6, edge=.5, bloom=0, rough=1)
    return art


def ripple():
    rng = random.Random(7)
    art = blank(BW, BH)
    m = outline_mask(BW, BH, ellipse_pts(210, 114, 90, 17, 32), 2.4, rng, wob=0.004, breaks=0.12)
    art = wash(art, m, "#ffffff", "#e9f5f2", density=.9, edge=.1, bloom=0, rough=1, feather=.6)
    return art


# ---------------- small motifs ----------------
def bloom():
    S = 96
    rng = random.Random(8)
    art = blank(S, S)
    for i in range(7):
        a = -math.pi / 2 + i * math.tau / 7
        m = shape_mask(S, S, deform(petal_pts(48, 48, 40, 14, a, n=12), rng, 1, .02))
        art = wash(art, m, [ROSE, "#dc929a"][i % 2], ROSE_L, density=0.62, edge=0.6, bloom=0.25, rough=1.6, feather=.9)
    art = wash(art, shape_mask(S, S, ellipse_pts(48, 48, 8, 8, 10)), "#d3a547", OCHRE_D, density=.85, edge=.6, bloom=0, rough=1)
    return art


def petal(kind, k):
    S = 40
    rng = random.Random(30 + k)
    art = blank(S, S)
    m = shape_mask(S, S, deform(petal_pts(6, 20, 28, 11, 0.0, n=12, cup=.5), rng, 1, .03))
    cols = {"rose": (ROSE, ROSE_L, .65, .6), "white": ("#fbfaf5", "#e2e3dc", .8, .85), "yellow": ("#dcd165", "#efe7a4", .7, .5)}[kind]
    art = wash(art, m, cols[0], cols[1], density=cols[2], edge=cols[3], bloom=.2, rough=1.2, feather=.8)
    return art


# ---------------- siraman still life ----------------
def siraman():
    W, H = 660, 400
    rng = random.Random(15)
    art = blank(W, H)
    # ground shadow
    art = wash(art, shape_mask(W, H, ellipse_pts(330, 362, 300, 22, 24)), "#d9c3bb", density=.35, edge=.1, bloom=.4, rough=8)
    # folded batik stack (left): three cloths, each a soft rectangle with a fold line and pattern
    cloths = [((62, 296, 230, 58), "#7a4f37", "#9a6a48", "parang"),
              ((76, 246, 206, 52), "#55607f", "#6f7a98", "kawung"),
              ((90, 200, 182, 48), ROSE, ROSE_L, "dots")]
    for (x, y, w, h), c1, c2, pat in cloths:
        pts = deform(rect_pts(x, y, w, h, 7), rng, 2, 0.011)
        m = shape_mask(W, H, pts)
        art = wash(art, m, c2, c1, density=.62, edge=.5, bloom=.3, rough=2.5)
        if pat == "parang":
            for i in range(-6, 26):
                xx = x + i * 11
                s_ = stroke_mask(W, H, curve([(xx, y + h), (xx + 14, y + h * .5), (xx + 30, y)], 16), 3.4, (.1, .1)) * m
                art = wash(art, s_, "#4a2e20", density=.45, edge=.3, bloom=0, rough=1, feather=.7)
        elif pat == "kawung":
            for i in range(8):
                for j in range(2):
                    cx, cy = x + 18 + i * 26 + (j % 2) * 13, y + 14 + j * 24
                    for a in range(4):
                        ang = a * math.pi / 2 + math.pi / 4
                        ex, ey = cx + math.cos(ang) * 6.5, cy + math.sin(ang) * 6.5
                        s_ = shape_mask(W, H, ellipse_pts(ex, ey, 7, 3.6, 10, ang)) * m
                        art = wash(art, s_, "#e9e3d6", density=.55, edge=.45, bloom=0, rough=.8, feather=.7)
                    art = wash(art, dab(W, H, cx, cy, 1.8, 1.8, 0, rng) * m, "#2f3955", density=.6, edge=.2, bloom=0, rough=.3, feather=.5)
        else:
            for i in range(30):
                s_ = dab(W, H, rng.uniform(x + 8, x + w - 8), rng.uniform(y + 8, y + h - 8), 3.2, 3.2, 0, rng) * m
                art = wash(art, s_, "#fbefe8", density=.7, edge=.3, bloom=0, rough=.6, feather=.6)
        # folded front edge: darker band at the bottom of each cloth
        fold = m * poly_mask(W, H, [(x - 4, y + h - 10), (x + w + 4, y + h - 10), (x + w + 4, y + h + 6), (x - 4, y + h + 6)])
        art = wash(art, fold, c1, density=.4, edge=.4, bloom=0, rough=1.5)
    # kendi (clay water jug)
    body = shape_mask(W, H, deform(ellipse_pts(402, 272, 78, 74, 16), rng, 1, .01))
    neck = shape_mask(W, H, deform([(380, 210), (424, 210), (430, 150), (374, 150)], rng, 1, .01), smooth=False)
    lip = shape_mask(W, H, ellipse_pts(402, 150, 34, 9, 18))
    spout = shape_mask(W, H, deform([(460, 236), (476, 230), (512, 186), (520, 192), (486, 250)], rng, 1, .01), smooth=False)
    clay = union(body, neck, spout)
    art = wash(art, clay, "#d48e66", "#bf7350", density=.7, edge=.5, bloom=.35, rough=3)
    sh = clay * (shift(gaussian_filter(body, 16), -34, -22) < 0.55).astype(np.float32)
    art = wash(art, gaussian_filter(sh, 3) * clay, "#9c5235", density=.5, edge=.4, bloom=.3, rough=4)
    art = wash(art, lip, "#c97d58", "#a35c3c", density=.75, edge=.6, bloom=.1, rough=1.5)
    art = wash(art, shape_mask(W, H, ellipse_pts(402, 150, 24, 5, 14)), "#6f3a26", density=.7, edge=.4, bloom=0, rough=1)
    for y0 in (232, 300):
        band = [(330 + i * 6, y0 + 6 * math.sin(math.pi * i / 24)) for i in range(25)]
        art = wash(art, stroke_mask(W, H, band, 2.4, (.05, .05)) * body, "#8e4a2f", density=.35, edge=.2, bloom=0, rough=1, feather=.7)
    hi = stroke_mask(W, H, curve([(352, 238), (346, 270), (360, 306)], 20), 11, (.3, .4))
    art = knockout(art, hi * body, amount=.7, grow=2.5)
    # two cengkir gading (young ivory coconuts) in front
    for (cx, cy, rx, ry, rot) in [(520, 322, 46, 40, .2), (590, 330, 42, 37, -.3)]:
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, ry, 14, rot), rng, 1, .02))
        art = wash(art, m, "#ecca58", "#d9a83a", density=.72, edge=.5, bloom=.35, rough=3)
        sh = m * (shift(gaussian_filter(m, 10), -16, -14) < .55).astype(np.float32)
        art = wash(art, gaussian_filter(sh, 2) * m, "#b98a2a", density=.45, edge=.3, bloom=.2, rough=3)
        cap = shape_mask(W, H, ellipse_pts(cx - rx * .15, cy - ry * .9, 10, 6, 10, rot))
        art = wash(art, cap, "#9aa04a", "#7c8a3a", density=.7, edge=.5, bloom=0, rough=1)
        art = knockout(art, stroke_mask(W, H, arc_pts(cx - 6, cy, rx * .7, math.pi * 1.05, math.pi * 1.45, 12), 7) * m, amount=.6, grow=2)
    # a few kembang setaman petals in the foreground
    for i in range(14):
        x, y = rng.uniform(40, 640), rng.uniform(352, 384)
        m = dab(W, H, x, y, 6, 3.4, rng.uniform(0, 3), rng)
        art = wash(art, m, rng.choice([ROSE, "#f4f1e6", "#dcd165", ROSE_L]), density=.65, edge=.55, bloom=0, rough=1)
    return art


if __name__ == "__main__":
    print("janur", save_asset(janur_band(), f"{D}/janur.webp", max_w=780, quality=80))
    for k, L in enumerate((116, 140, 192)):
        print("strip", k, save_asset(janur_strip(L, k), f"{D}/strip-{k}.webp", quality=84))
    b, f, r = bowl(), flowers(), ripple()
    for n, a in (("bokor", b), ("bokor-flowers", f), ("bokor-ripple", r)):
        print(n, save_full(a, f"{D}/{n}.webp"))
    preview(glaze(glaze(b, r), f), "tb-bokor.png", "#fbf6ee")
    print("bloom", save_asset(bloom(), f"{D}/bloom.webp", quality=84))
    for k, kind in enumerate(("rose", "white", "yellow")):
        print("petal", kind, save_asset(petal(kind, k), f"{D}/petal-{kind}.webp", quality=84))
    s_ = siraman(); print("siraman", save_asset(s_, f"{D}/siraman.webp", max_w=620, quality=80)); preview(s_, "tb-siraman.png", "#fbf6ee")
    print("paper", paper_tile(f"{D}/paper.webp", "#fdfbf8", seed=41, fiber=0.7, mottle=0.3))
    report(D)
