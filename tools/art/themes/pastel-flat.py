"""Pastel Flat — gouache "flat" illustration with brush texture: a hill-and-sun scene under a floral arch,
flower clusters, a bunting garland, painted confetti, paper grain.
Run: python3 -I /tmp/pen/art/themes/pastel-flat.py [asset…]
"""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _p2_lib import *  # noqa
import _p3_common as p3
from _p3_common import rrect_mask, dots_mask
PREV = "/tmp/pen/nt3-R2"

D = f"{OUT}/pastel-flat"
os.makedirs(D, exist_ok=True)
TONE = "#fff6f4"
PINK, CORAL, BLUE, YELLOW, CREAM = "#f29ab0", "#f08a6c", "#8fbde6", "#f6cf6a", "#fff3e6"
MINT = ["#cfe9d6", "#a8d5b5", "#79b78f", "#5b9b73"]
DEEP = {PINK: "#d9748f", CORAL: "#cf6a4e", BLUE: "#6a9ccf", YELLOW: "#d9ad45"}


def g(mask, col, seed, col2=None, rough=3.0, streak=0.6, density=0.97):
    return gou(mask, col, col2 or mix(col, "#ffffff", .08), seed=seed, rough=rough, streak=streak, density=density)


def daisy(W, H, cx, cy, r, col, sd, rng, petals=6, centre=YELLOW):
    lay = blank(W, H)
    for i in range(petals):
        a = i / petals * math.tau + rng.uniform(-.15, .15)
        pm = shape_mask(W, H, deform(petal_pts(cx + math.cos(a) * r * .22, cy + math.sin(a) * r * .22, r * .8, r * .34, a, n=12), rng, 1, .05))
        lay = over(lay, g(pm, col, sd(), col2=mix(col, DEEP.get(col, col), rng.uniform(0, .5))))
    cm = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * .26, r * .26, 10), rng, 1, .08))
    lay = over(lay, g(cm, centre, sd(), col2=mix(centre, "#ffffff", .2)))
    return lay


def pompom(W, H, cx, cy, r, col, sd, rng):
    lay = blank(W, H)
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * .95, 12), rng, 2, .1))
    lay = over(lay, g(base, col, sd()))
    dm = dots(W, H, cx - r * .25, cy - r * .25, r * .35, r * .35, 7, r * .09, r * .16, rng)
    lay = over(lay, g(dm * base, mix(col, "#ffffff", .45), sd(), rough=1.5))
    return lay


def leaf_g(W, H, x, y, L, a, col, sd, rng, width=0.36):
    m = shape_mask(W, H, deform(petal_pts(x, y, L, L * width, a, n=12), rng, 1, .04))
    lay = g(m, col, sd(), col2=mix(col, "#2f6b4c", .12))
    vein = stroke_mask(W, H, [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in (0.12, 0.5, 0.85)], max(1.5, L * .035))
    return over(lay, g(vein * m, mix(col, "#ffffff", .4), sd(), rough=1.2))


def arch_scene(W, H, rng, sd, cx=390, top=330, R=210, ground=740):
    """Sky, sun, clouds, hills and a flower-covered garden arch (shared by the cover and the opening)."""
    art = painted_sky(W, H, [(0, "#fde3e8"), (0.3, "#fdeeee"), (0.55, "#fff5f0"), (1, "#fff6f4")], seed=3, streak=0.35, grain=0.7)
    art = over(art, glow(shape_mask(W, H, ellipse_pts(cx, top + 10, 120, 120, 16)), "#fff1c9", radius=40, strength=0.5))
    art = over(art, g(shape_mask(W, H, deform(ellipse_pts(cx, top + 10, 118, 118, 18), rng, 2, .015)), "#fde7b3", sd(), col2="#fbd889", rough=2, streak=0.3))
    for (ccx, ccy, s, o) in [(110, 150, 1.0, .95), (650, 110, .85, .92), (700, 380, .6, .85), (70, 420, .55, .8)]:
        cm = np.zeros((H, W), np.float32)
        for (dx, dy, r) in [(0, 0, 44), (46, -16, 40), (90, 2, 34), (-40, 10, 30), (30, 16, 38)]:
            cm = np.maximum(cm, shape_mask(W, H, ellipse_pts(ccx + dx * s, ccy + dy * s, r * s, r * s * .9, 14)))
        cm = np.maximum(cm, shape_mask(W, H, [(ccx - 66 * s, ccy + 28 * s), (ccx + 118 * s, ccy + 28 * s), (ccx + 118 * s, ccy + 8 * s), (ccx - 66 * s, ccy + 8 * s)], smooth=False))
        art = over(art, g(cm, "#ffffff", sd(), col2="#fff3f1", rough=2.0, streak=0.3, density=o))
    hills = [("#f8d3cb", 560, 0.4, 50), ("#cfe9d6", 640, 1.9, 60), ("#b2dcc0", 720, 3.6, 46), ("#97cca8", 820, 5.2, 40)]
    for i, (col, base, ph, amp) in enumerate(hills):
        pts = [(x, base - amp * math.sin(x / W * math.pi * 1.3 + ph) - 18 * math.cos(x / W * 5.3 + ph)) for x in np.linspace(-40, W + 40, 20)]
        hm = shape_mask(W, H, pts + [(W + 40, H + 40), (-40, H + 40)])
        art = over(art, g(hm, col, sd(), col2=mix(col, "#ffffff", .12), rough=3, streak=0.5))
        if i in (1, 2):
            for (tx, k) in ([(70, 1.0), (250, .7), (600, .8), (720, 1.1)] if i == 1 else [(150, 1.1), (660, 1.2)]):
                ty = base - amp * math.sin(tx / W * math.pi * 1.3 + ph) - 18 * math.cos(tx / W * 5.3 + ph)
                tr = 24 * k * (0.9 + i * 0.25)
                art = over(art, g(stroke_mask(W, H, [(tx, ty + 6), (tx, ty - tr * .9)], 6 * k, taper=(0, 0)), "#c69a78", sd(), rough=1.0))
                can = shape_mask(W, H, deform(ellipse_pts(tx, ty - tr * 1.35, tr, tr * 1.15, 14), rng, 2, .05))
                art = over(art, g(can, "#7fbf95" if i == 1 else "#66ab80", sd(), col2="#8fcaa2", rough=2.5))
                hl = shape_mask(W, H, deform(ellipse_pts(tx - tr * .3, ty - tr * 1.65, tr * .42, tr * .3, 10), rng, 1, .1))
                art = over(art, g(hl * can, "#b6e0c3", sd(), rough=1.2, density=.8))
    # garden arch: cream posts + semicircle, then foliage and flowers all along it
    frame = stroke_mask(W, H, [(cx - R, ground)] + arc_pts(cx, top, R, math.pi, math.tau, 40) + [(cx + R, ground)], 18, taper=(0, 0))
    art = over(art, g(frame, "#fff4e6", sd(), col2="#f5e3cc", rough=1.6, streak=0.4))
    arch = blank(W, H)
    path = [(cx - R, ground - 30 - t * (ground - top - 30)) for t in np.linspace(0, 1, 7)] + arc_pts(cx, top, R, math.pi, math.tau, 15)[1:-1] + [(cx + R, top + t * (ground - top - 30)) for t in np.linspace(0, 1, 7)]
    for i, (x, y) in enumerate(path):
        nrm = math.atan2(y - top, x - cx) if y < top + 1 else (math.pi if x < cx else 0)
        for k in range(2):
            a = nrm + rng.uniform(-1.4, 1.4)
            arch = over(arch, leaf_g(W, H, x + rng.gauss(0, 6), y + rng.gauss(0, 6), rng.uniform(34, 52), a, MINT[rng.choice([2, 3])], sd, rng))
    flowers = [PINK, CORAL, BLUE, YELLOW]
    for i, (x, y) in enumerate(path[::1]):
        if i % 2 and y > top + 40:
            continue
        col = flowers[(i * 3) % 4]
        r = rng.uniform(22, 30) * (1.3 if i in (9, 13, 17) else 1)
        if i % 3 == 1:
            arch = over(arch, pompom(W, H, x + rng.gauss(0, 4), y + rng.gauss(0, 4), r * .75, col, sd, rng))
        else:
            arch = over(arch, daisy(W, H, x + rng.gauss(0, 4), y + rng.gauss(0, 4), r, col, sd, rng, petals=rng.choice([5, 6]), centre=YELLOW if col != YELLOW else CORAL))
    return art, arch


def person_shade(layer, mask, k=0.22):
    return p3.shade(layer, mask, light=(-0.7, -0.6), k=k, blur=10, hi="#ffffff", lo="#6b4f6a")


def couple(W, H, rng, sd, cx=390, ground=740):
    """Stylised, friendly couple (flat gouache, simple closed-eye faces). Groom left, bride right."""
    out = blank(W, H)
    SKIN, SKIN2, HAIR = "#f3c9a8", "#e9b48f", "#7a4e36"
    gx, bx = cx - 62, cx + 66
    # bride's veil (behind everything), translucent
    veil = shape_mask(W, H, deform([(bx + 6, 392), (bx + 64, 470), (bx + 96, 640), (bx + 104, ground - 10), (bx + 20, ground - 30), (bx + 18, 470)], rng, 2, .02))
    out = over(out, pig(veil, "#ffffff", "#fdf3f6", seed=sd(), density=0.55, edge=0.35, bloom=0.3, rough=4, feather=1.5, gran=0.1))
    # --- groom ---
    legs = shape_mask(W, H, [(gx - 34, 560), (gx + 32, 560), (gx + 30, ground - 12), (gx + 6, ground - 12), (gx, 600), (gx - 6, ground - 12), (gx - 30, ground - 12)], smooth=False)
    out = over(out, person_shade(g(legs, "#6f98c9", sd(), col2="#7aa3d2", rough=1.6), legs))
    for sx in (-18, 18):
        shoe = shape_mask(W, H, deform(ellipse_pts(gx + sx + (4 if sx > 0 else -4), ground - 8, 17, 8, 12), rng, 1, .04))
        out = over(out, g(shoe, "#8a5a3c", sd(), rough=1.0))
    jacket = shape_mask(W, H, deform([(gx - 46, 448), (gx + 44, 448), (gx + 40, 584), (gx + 6, 596), (gx - 6, 596), (gx - 40, 584)], rng, 2, .012), smooth=False)
    out = over(out, person_shade(g(jacket, "#86afe0", sd(), col2="#93b9e6", rough=1.6), jacket, 0.28))
    shirt = shape_mask(W, H, [(gx - 14, 448), (gx + 14, 448), (gx, 520)], smooth=False)
    out = over(out, g(shirt, "#fffaf3", sd(), rough=0.8))
    tie = shape_mask(W, H, [(gx - 6, 452), (gx + 6, 452), (gx + 4, 470), (gx, 478), (gx - 4, 470)], smooth=False)
    out = over(out, g(tie, "#e98aa4", sd(), rough=0.6))
    for sx in (-1, 1):
        lap = shape_mask(W, H, [(gx + sx * 16, 450), (gx + sx * 30, 452), (gx + sx * 6, 530), (gx, 528)], smooth=False)
        out = over(out, g(lap, "#7199cc", sd(), rough=0.8))
    out = over(out, daisy(W, H, gx - 26, 474, 9, PINK, sd, rng, petals=5))
    # arms: left hangs, right reaches to the bride's hand
    arm_l = stroke_mask(W, H, curve([(gx - 40, 458), (gx - 52, 520), (gx - 48, 580)], 20), 22, taper=(0, 0.05))
    out = over(out, person_shade(g(arm_l, "#7ea8db", sd(), rough=1.4), arm_l, 0.25))
    out = over(out, g(shape_mask(W, H, ellipse_pts(gx - 47, 590, 11, 12, 12)), SKIN, sd(), col2=SKIN2, rough=1))
    hand_y = 556
    arm_r = stroke_mask(W, H, curve([(gx + 38, 458), (gx + 52, 520), (cx - 2, hand_y)], 20), 22, taper=(0, 0.1))
    out = over(out, person_shade(g(arm_r, "#7ea8db", sd(), rough=1.4), arm_r, 0.25))
    # neck + head
    out = over(out, g(rrect_mask(W, H, gx - 9, 424, 18, 28, 4), SKIN2, sd(), rough=0.8))
    head = shape_mask(W, H, deform(ellipse_pts(gx + 2, 392, 36, 40, 18), rng, 1, .01))
    out = over(out, person_shade(g(head, SKIN, sd(), col2=SKIN2, rough=1.0), head, 0.15))
    for ex in (-36, 38):
        out = over(out, g(shape_mask(W, H, ellipse_pts(gx + 2 + ex, 396, 7, 10, 10)), SKIN2, sd(), rough=0.6))
    hair = shape_mask(W, H, deform([(gx - 38, 392), (gx - 36, 362), (gx - 14, 346), (gx + 16, 346), (gx + 38, 362), (gx + 40, 388), (gx + 30, 372), (gx + 10, 368), (gx - 6, 362), (gx - 24, 374)], rng, 1, .02))
    out = over(out, g(hair, HAIR, sd(), col2="#8a5d42", rough=1.2))
    # --- bride ---
    gown = shape_mask(W, H, deform([(bx - 26, 500), (bx + 26, 500), (bx + 46, 560), (bx + 92, ground - 4), (bx + 30, ground + 4), (bx - 30, ground + 4), (bx - 92, ground - 4), (bx - 46, 560)], rng, 2, .012))
    out = over(out, person_shade(g(gown, "#fffaf4", sd(), col2="#fbefe6", rough=1.6, streak=0.4), gown, 0.3))
    for k in (-50, -14, 22, 58):
        fold = stroke_mask(W, H, curve([(bx + k * 0.3, 540), (bx + k * 0.8, 640), (bx + k * 1.15, ground - 8)], 20), 3, taper=(0.4, 0.2)) * gown
        out = over(out, g(fold, "#efdfd3", sd(), rough=0.6, density=0.7))
    bod = shape_mask(W, H, deform([(bx - 28, 448), (bx + 28, 448), (bx + 26, 506), (bx - 26, 506)], rng, 1, .02), smooth=False)
    out = over(out, person_shade(g(bod, "#fffaf4", sd(), col2="#f8ece2", rough=1.2), bod, 0.25))
    out = over(out, g(stroke_mask(W, H, [(bx - 27, 503), (bx + 27, 503)], 7, taper=(0, 0)), "#f4b6c4", sd(), rough=0.6))
    out = over(out, g(rrect_mask(W, H, bx - 8, 420, 16, 32, 4), SKIN2, sd(), rough=0.8))
    for sx in (-1, 1):
        sh = shape_mask(W, H, ellipse_pts(bx + sx * 26, 452, 11, 9, 10))
        out = over(out, g(sh, SKIN, sd(), rough=0.8))
    # arms: left arm to the joined hands, right holds the bouquet
    arm = stroke_mask(W, H, curve([(bx - 30, 456), (bx - 40, 510), (cx + 6, hand_y)], 20), 16, taper=(0, 0.1))
    out = over(out, person_shade(g(arm, SKIN, sd(), col2=SKIN2, rough=1.0), arm, 0.2))
    arm2 = stroke_mask(W, H, curve([(bx + 30, 456), (bx + 40, 512), (bx + 12, 540)], 20), 16, taper=(0, 0.1))
    out = over(out, person_shade(g(arm2, SKIN, sd(), col2=SKIN2, rough=1.0), arm2, 0.2))
    # joined hands
    out = over(out, g(shape_mask(W, H, deform(ellipse_pts(cx + 2, hand_y, 15, 12, 12), rng, 1, .04)), SKIN, sd(), col2=SKIN2, rough=1))
    # bouquet
    bq = blank(W, H)
    for (dx, dy, L, a) in [(-14, 4, 30, 2.4), (16, 6, 30, 0.7), (0, 14, 26, 1.6), (-24, -4, 22, 3.0), (26, -2, 22, 0.1)]:
        bq = over(bq, leaf_g(W, H, bx + 6 + dx, 548 + dy, L, a, MINT[2], sd, rng))
    for (dx, dy, col, r) in [(-12, 540, PINK, 15), (12, 536, CORAL, 14), (2, 552, BLUE, 12), (-20, 556, YELLOW, 10), (22, 554, PINK, 11)]:
        bq = over(bq, daisy(W, H, bx + 6 + dx, dy, r, col, sd, rng, petals=5) if col != BLUE else pompom(W, H, bx + 6 + dx, dy, r, col, sd, rng))
    bq = over(bq, g(stroke_mask(W, H, [(bx + 4, 560), (bx + 8, 598)], 9, taper=(0, 0.2)), "#79b78f", sd(), rough=0.8))
    out = over(out, bq)
    # head, hair (bun) and flower crown; slight tilt toward the groom
    bh = shape_mask(W, H, deform(ellipse_pts(bx - 2, 392, 33, 37, 18, rot=-0.12), rng, 1, .01))
    hair_back = shape_mask(W, H, deform([(bx - 36, 384), (bx - 30, 352), (bx - 4, 340), (bx + 26, 348), (bx + 40, 374), (bx + 44, 430), (bx + 30, 448), (bx + 30, 410), (bx - 30, 414)], rng, 1, .02))
    out = over(out, g(hair_back, "#8a5b3f", sd(), col2="#9a6a4a", rough=1.2))
    out = over(out, person_shade(g(bh, SKIN, sd(), col2=SKIN2, rough=1.0), bh, 0.15))
    fringe = shape_mask(W, H, deform([(bx - 34, 388), (bx - 30, 358), (bx - 2, 348), (bx + 28, 356), (bx + 36, 380), (bx + 16, 368), (bx - 8, 366), (bx - 22, 376)], rng, 1, .02))
    out = over(out, g(fringe, "#8a5b3f", sd(), col2="#9a6a4a", rough=1.2))
    out = over(out, g(shape_mask(W, H, deform(ellipse_pts(bx + 26, 346, 18, 16, 12), rng, 1, .04)), "#8a5b3f", sd(), rough=1.2))
    for i, a in enumerate(np.linspace(math.pi * 1.08, math.pi * 1.92, 7)):
        fx, fy = bx - 2 + math.cos(a) * 34, 384 + math.sin(a) * 36
        out = over(out, daisy(W, H, fx, fy, 7.5, [PINK, BLUE, YELLOW, CORAL][i % 4], sd, rng, petals=5))
    # faces: happy closed eyes, small smiles, rosy cheeks (ink-thin, hand drawn)
    def face(fx, fy, tilt):
        f = np.zeros((H, W), np.float32)
        for ex in (-13, 13):
            f = np.maximum(f, stroke_mask(W, H, arc_pts(fx + ex, fy - 2 + ex * tilt, 6, math.pi * 1.1, math.pi * 1.9, 8), 2.4, taper=(0.2, 0.2)))
        f = np.maximum(f, stroke_mask(W, H, arc_pts(fx, fy + 12, 7, math.pi * 0.15, math.pi * 0.85, 10), 2.4, taper=(0.2, 0.2)))
        layer = g(f, "#5b3a33", sd(), rough=0.3, streak=0)
        ch = dots_mask(W, H, [(fx - 21, fy + 10, 7), (fx + 21, fy + 10, 7)])
        return over(pig(ch, "#f39aac", seed=sd(), density=0.5, edge=0.2, bloom=0, rough=1.5, feather=2), layer)
    out = over(out, face(gx + 4, 400, 0.0))
    out = over(out, face(bx - 4, 400, -0.04))
    return out


def hero():
    """Cover: the couple under a flower arch on a meadow (top 60% carries the scene, the bottom fades into the card)."""
    W, H = 780, 1240
    rng = random.Random(7); sd = Seeds(100)
    art, arch = arch_scene(W, H, rng, sd)
    art = over(art, g(shape_mask(W, H, deform(ellipse_pts(390, 742, 190, 22, 16), rng, 1, .03)), "#86c29b", sd(), rough=2, density=.6))
    art = over(art, couple(W, H, rng, sd))
    art = over(art, arch)
    # foreground meadow flowers (left/right), partly under the fade
    for (x, y, col, r) in [(60, 820, PINK, 30), (130, 870, YELLOW, 24), (40, 930, CORAL, 26), (700, 830, BLUE, 26), (740, 900, PINK, 30), (640, 900, CORAL, 22), (210, 800, BLUE, 18), (560, 806, YELLOW, 18)]:
        for k in range(3):
            art = over(art, leaf_g(W, H, x + rng.gauss(0, 10), y + 30, rng.uniform(36, 50), -math.pi / 2 + rng.uniform(-1.0, 1.0), MINT[rng.choice([2, 3])], sd, rng))
        art = over(art, daisy(W, H, x, y, r, col, sd, rng, petals=rng.choice([5, 6])) if col != BLUE else pompom(W, H, x, y, r * .8, col, sd, rng))
    for (x, y, col, r) in [(80, 70, PINK, 8), (700, 60, BLUE, 7), (220, 300, YELLOW, 7), (590, 290, CORAL, 6), (730, 250, PINK, 6)]:
        art = over(art, g(shape_mask(W, H, deform(ellipse_pts(x, y, r, r, 8), rng, 1, .1)), col, sd(), rough=1.2))
    print("hero", save_asset(art, f"{D}/hero.webp", max_w=780, quality=80), kb(f"{D}/hero.webp"))
    im = to_image(art).convert("RGB"); im.save(f"{PREV}/pf-hero.png")
    im.crop((180, 280, 600, 780)).save(f"{PREV}/pf-hero-zoom.png")


def cluster():
    """A small horizontal flower spray: the centre ornament of section-heading dividers."""
    W, H = 320, 140
    rng = random.Random(4); sd = Seeds(700)
    art = blank(W, H)
    for (x, y, L, a, c) in [(160, 74, 70, math.pi + 0.15, 2), (160, 74, 70, -0.15, 3), (150, 78, 50, math.pi - 0.45, 3), (170, 78, 50, 0.45, 2),
                            (130, 70, 40, math.pi * 1.25, 1), (190, 70, 40, -math.pi * 0.25, 1)]:
        art = over(art, leaf_g(W, H, x, y, L, a, MINT[c], sd, rng, width=0.32))
    art = over(art, pompom(W, H, 112, 76, 17, BLUE, sd, rng))
    art = over(art, daisy(W, H, 208, 76, 20, CORAL, sd, rng, petals=6))
    art = over(art, daisy(W, H, 160, 68, 27, PINK, sd, rng, petals=5))
    for (x, y, col) in [(84, 66, YELLOW), (238, 64, PINK)]:
        art = over(art, g(shape_mask(W, H, deform(ellipse_pts(x, y, 6, 6, 8), rng, 1, .1)), col, sd(), rough=1.0))
    print("cluster", save_asset(art, f"{D}/cluster.webp", max_w=160, quality=82), kb(f"{D}/cluster.webp"))
    preview(art, f"{PREV}/pf-cluster.png", TONE)


def bunting():
    """Gouache flag garland (tiles horizontally: the string ends at the same height on both sides)."""
    W, H = 800, 130
    rng = random.Random(9); sd = Seeds(900)
    art = blank(W, H)
    n = 8
    string = [(x, 18 + 14 * math.sin(math.pi * ((x % 100) / 100))) for x in np.linspace(0, W, 80)]
    art = over(art, g(stroke_mask(W, H, string, 3, taper=(0, 0)), "#b98c6a", sd(), rough=1.0))
    cols = [PINK, BLUE, YELLOW, CORAL, MINT[2], PINK, BLUE, CORAL]
    for i in range(n):
        x0 = i * 100 + 12; x1 = x0 + 76
        y0 = 18 + 14 * math.sin(math.pi * 0.12); y1 = 18 + 14 * math.sin(math.pi * 0.88)
        tri = [(x0, y0 + 2), (x1, y1 + 2), ((x0 + x1) / 2 + rng.uniform(-4, 4), 108 + rng.uniform(-8, 6))]
        m = shape_mask(W, H, deform(tri, rng, 2, .03), smooth=False)
        art = over(art, g(m, cols[i], sd(), col2=mix(cols[i], DEEP.get(cols[i], cols[i]), .3), rough=2.5))
        if i % 2:
            dm = dots(W, H, (x0 + x1) / 2, 55, 18, 16, 5, 3, 5, rng) * m
            art = over(art, g(dm, "#ffffff", sd(), rough=1.0, density=.85))
    print("bunting", save_asset(art, f"{D}/bunting.webp", max_w=400, quality=82), kb(f"{D}/bunting.webp"))
    preview(art, f"{PREV}/pf-bunting.png", TONE)


def confetti():
    """Sprite of 4 painted confetti pieces (square, circle, pill, triangle) at 48px each → 192×48."""
    W, H = 192, 48
    rng = random.Random(2); sd = Seeds(50)
    art = blank(W, H)
    art = over(art, g(shape_mask(W, H, deform([(14, 12), (34, 10), (36, 36), (12, 38)], rng, 2, .05), smooth=False), PINK, sd(), rough=1.5))
    art = over(art, g(shape_mask(W, H, deform(ellipse_pts(72, 24, 13, 13, 10), rng, 1, .08)), BLUE, sd(), rough=1.5))
    art = over(art, g(stroke_mask(W, H, [(104, 24), (136, 24)], 14, taper=(0, 0)), YELLOW, sd(), rough=1.5))
    art = over(art, g(shape_mask(W, H, deform([(154, 36), (182, 36), (168, 10)], rng, 2, .05), smooth=False), CORAL, sd(), rough=1.5))
    save_rgba(art, f"{D}/confetti.webp", quality=84)
    print("confetti", kb(f"{D}/confetti.webp"))


def texture():
    save_texture(paper_tile(512, "#fffaf9", seed=51, mottle=0.4, fine=1.0, fiber=0.8, strength=0.75), f"{D}/paper.webp", quality=68)
    print("paper", kb(f"{D}/paper.webp"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["hero", "cluster", "bunting", "confetti", "texture"]
    for w in which:
        globals()[w]()
