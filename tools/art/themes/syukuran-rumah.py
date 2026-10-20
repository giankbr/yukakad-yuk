"""Syukuran Rumah — gouache folk-painted house (layered for motion), tumpeng scene, roof divider, paper tile.
Run: python3 -I /tmp/pen/art/themes/syukuran-rumah.py
House layers share one 480x340 canvas (no trim) so they stack exactly: house, lights, tree, plant."""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _h_common import *

D = outdir("syukuran-rumah")
W, H = 480, 340
INK = "#4a3a2c"
TERRA, TERRA_D, TERRA_L = "#b85c38", "#8e3f25", "#d77f55"
SAGE, SAGE_D, SAGE_L = "#7d9471", "#4f6648", "#a8bb93"
CREAM, CREAM_D = "#f3e7cf", "#d8c6a5"
GOLD = "#e8b75c"
sd = Seeds(500)
rng = random.Random(12)


def save_full(arr, path, quality=82):
    im = to_image(arr)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def outline(art, pts, width=2.0, breaks=0.06, alpha=0.75, closed=True):
    return ink(art, outline_mask(W, H, pts, width, rng, closed=closed, wob=0.003, breaks=breaks), INK, seed=sd(), wear=0.3, alpha=alpha)


def house():
    art = blank(W, H)
    # ground: grass strip + path
    g_pts = deform([(20, 318), (460, 314), (468, 334), (12, 336)], rng, 3, 0.01)
    grass = poly_mask(W, H, g_pts)
    art = over(art, gouache_paint(grass, SAGE, SAGE_D, seed=sd(), rough=3, streak=0.6))
    for i in range(46):  # grass tufts
        x = rng.uniform(24, 456)
        h = rng.uniform(5, 11)
        m = stroke_mask(W, H, [(x, 320), (x + rng.uniform(-3, 3), 320 - h)], 2.4, (0.05, 0.6))
        art = over(art, gouache_paint(m, rng.choice([SAGE_D, SAGE_L, SAGE]), seed=sd(), rough=0.5))
    # chimney (behind roof)
    ch = deform(rect_pts(318, 82, 28, 70, 3), rng, 1, 0.006)
    art = gouache_form(art, shape_mask(W, H, ch, smooth=False), TERRA_L, TERRA_D, seed=sd(), sdx=-.25, sdy=0)
    cap = deform(rect_pts(312, 76, 40, 10, 3), rng, 1, 0.006)
    art = over(art, gouache_paint(shape_mask(W, H, cap, smooth=False), "#7a3a24", seed=sd(), rough=1.5))
    art = outline(art, ch); art = outline(art, cap, 1.6)
    # walls
    wall = deform(rect_pts(100, 176, 280, 144, 6), rng, 1, 0.004)
    wm = shape_mask(W, H, wall, smooth=False)
    art = gouache_form(art, wm, CREAM, CREAM_D, seed=sd(), sdx=-.12, sdy=0, streak=0.5)
    # soft roof shadow under the eaves
    eave_sh = poly_mask(W, H, [(100, 176), (380, 176), (380, 196), (100, 190)])
    es = gouache_paint(eave_sh * wm, "#b9a27e", seed=sd(), rough=2)
    es[..., 3] *= 0.55
    art = over(art, es)
    # plinth
    pl = deform(rect_pts(96, 306, 288, 14, 6), rng, 1, 0.004)
    art = over(art, gouache_paint(shape_mask(W, H, pl, smooth=False), "#a99883", "#8f7f6c", seed=sd(), rough=1.5))
    art = outline(art, wall, 2.2)
    # windows: dark interior + frame + sills (lit overlay is a separate asset)
    for x0 in (132, 292):
        win = deform(rect_pts(x0, 206, 56, 50, 3), rng, 1, 0.004)
        art = over(art, gouache_paint(shape_mask(W, H, win, smooth=False), "#3f4b3c", "#56624f", seed=sd(), rough=1.2))
        sill = deform(rect_pts(x0 - 6, 256, 68, 8, 3), rng, 1, 0.004)
        art = over(art, gouache_paint(shape_mask(W, H, sill, smooth=False), SAGE_D, seed=sd(), rough=1))
        bars = union(stroke_mask(W, H, [(x0 + 28, 207), (x0 + 28.5, 255)], 4, (0.02, 0.02)),
                     stroke_mask(W, H, [(x0 + 1, 231), (x0 + 55, 230.5)], 4, (0.02, 0.02)))
        art = over(art, gouache_paint(bars, "#efe3c8", seed=sd(), rough=0.6))
        art = outline(art, win, 2.0)
        # flower box under the left window, little shutters feel
        for k in range(5):
            fx = x0 + 6 + k * 11
            fm = dab(W, H, fx, 252, 4.5, 4, 0, rng)
            art = over(art, gouache_paint(fm, [TERRA_L, "#e9c7b2", GOLD][k % 3], seed=sd(), rough=1))
    # door: arched terracotta door + stone step
    dpts = [(214, 320), (214, 262)] + arc_pts(240, 262, 26, math.pi, math.tau, 14)[1:-1] + [(266, 262), (266, 320)]
    dpts = deform(dpts, rng, 1, 0.004)
    dm = shape_mask(W, H, dpts, smooth=False)
    art = gouache_form(art, dm, TERRA, TERRA_D, seed=sd(), sdx=-.2, sdy=0)
    for x in (227, 253):  # plank lines
        art = ink(art, stroke_mask(W, H, [(x, 252), (x + .5, 316)], 1.6, (.05, .05)) * dm, "#7a3a24", seed=sd(), alpha=.6)
    art = over(art, gouache_paint(dab(W, H, 258, 290, 3.2, 3.2, 0, rng), GOLD, seed=sd(), rough=.5))
    art = outline(art, dpts, 2.2)
    step = deform(rect_pts(204, 318, 72, 9, 4), rng, 1, 0.005)
    art = over(art, gouache_paint(shape_mask(W, H, step, smooth=False), "#c8b9a2", "#a99883", seed=sd(), rough=1.5))
    # roof
    roof = deform([(70, 186), (240, 70), (410, 186), (396, 194), (240, 90), (84, 194)], rng, 1, 0.003)
    gable = deform([(104, 180), (240, 88), (376, 180)], rng, 1, 0.003)
    gm = poly_mask(W, H, gable)
    art = gouache_form(art, gm, "#e6d6b8", CREAM_D, seed=sd(), sdx=-.1, sdy=0)
    # attic round window (dark; lit by overlay)
    aw = ellipse_pts(240, 142, 15, 15, 18)
    art = over(art, gouache_paint(shape_mask(W, H, aw), "#3f4b3c", seed=sd(), rough=1))
    art = over(art, gouache_paint(union(stroke_mask(W, H, [(240, 128), (240, 156)], 3, (.02, .02)), stroke_mask(W, H, [(226, 142), (254, 142)], 3, (.02, .02))) * shape_mask(W, H, aw), "#efe3c8", seed=sd(), rough=.5))
    art = outline(art, aw, 1.8)
    # roof tiles: a terracotta band with tile rows
    rm = poly_mask(W, H, roof)
    art = gouache_form(art, rm, TERRA, TERRA_D, seed=sd(), sdx=-.06, sdy=-.2)
    for k in range(1, 14):
        t = k / 14
        a = (70 + (240 - 70) * t, 186 + (70 - 186) * t); b = (84 + (240 - 84) * t, 194 + (90 - 194) * t)
        art = ink(art, stroke_mask(W, H, [a, b], 1.8, (.1, .1)) * rm, "#7a3a24", seed=sd(), alpha=.55)
        a = (410 + (240 - 410) * t, 186 + (70 - 186) * t); b = (396 + (240 - 396) * t, 194 + (90 - 194) * t)
        art = ink(art, stroke_mask(W, H, [a, b], 1.8, (.1, .1)) * rm, "#7a3a24", seed=sd(), alpha=.55)
    art = outline(art, roof, 2.4)
    art = outline(art, gable, 1.6, closed=False, alpha=.5)
    # ridge ornament (small finial)
    fin = deform([(234, 74), (246, 74), (240, 58)], rng, 1, 0.01)
    art = over(art, gouache_paint(poly_mask(W, H, fin), "#7a3a24", seed=sd(), rough=1))
    return art


def lights():
    """Warm lit panes + soft glow, to fade in over the dark windows."""
    art = blank(W, H)
    panes = blank(W, H)
    for x0 in (132, 292):
        for (px, py) in [(x0 + 2, 208), (x0 + 30, 208), (x0 + 2, 233), (x0 + 30, 233)]:
            m = shape_mask(W, H, deform(rect_pts(px + 1, py + 1, 22, 19, 2), rng, 1, 0.01), smooth=False)
            panes = over(panes, gouache_paint(m, "#f6cf7a", "#f2b65a", seed=sd(), rough=0.8))
        win = shape_mask(W, H, rect_pts(x0, 206, 56, 50, 2), smooth=False)
        art = over(art, glow(win, "#f7cd78", radius=14, strength=0.32))
    aw = shape_mask(W, H, ellipse_pts(240, 142, 12, 12, 16))
    art = over(art, glow(aw, "#f7cd78", radius=10, strength=0.35))
    for q in [(228, 130, 11, 11), (241, 130, 11, 11), (228, 143, 11, 11), (241, 143, 11, 11)]:
        m = shape_mask(W, H, rect_pts(*q, 2), smooth=False) * aw
        panes = over(panes, gouache_paint(m, "#f6cf7a", seed=sd(), rough=.4))
    # warm light under the door gap
    art = over(art, panes)
    return art


def tree():
    art = blank(W, H)
    trunk = deform([(420, 320), (432, 320), (431, 270), (442, 244), (436, 242), (426, 262), (416, 240), (410, 244), (421, 272)], rng, 1, 0.01)
    art = gouache_form(art, poly_mask(W, H, trunk), "#8a6a4a", "#5e4630", seed=sd(), sdx=-.3, sdy=0, rough=1.5)
    blobs = [(426, 206, 40, 36), (398, 228, 26, 22), (452, 230, 26, 24), (414, 180, 26, 24), (446, 190, 24, 22), (428, 236, 28, 18)]
    canopy = blank(W, H)
    for i, (x, y, rx, ry) in enumerate(blobs):
        m = dab(W, H, x, y, rx, ry, rng.uniform(0, 3), rng, n=12, wob=0.1)
        canopy = over(canopy, gouache_form(blank(W, H), m, [SAGE, SAGE_L, SAGE][i % 3], SAGE_D, seed=sd(), sdx=-.2, sdy=-.15, rough=3))
    # leaf strokes for texture
    for i in range(40):
        x, y = rng.gauss(426, 26), rng.gauss(208, 22)
        a = rng.uniform(0, math.pi)
        m = dab(W, H, x, y, 6, 2.6, a, rng, n=8, wob=.05)
        canopy = over(canopy, gouache_paint(m, rng.choice([SAGE_D, SAGE_L, "#8fa77f"]), seed=sd(), rough=.6))
    art = over(art, canopy)
    for (x, y) in [(410, 222), (440, 214), (432, 238)]:  # mangoes
        m = dab(W, H, x, y, 5.5, 7, .3, rng)
        art = over(art, gouache_paint(m, "#e3b84a", "#c7a03a", seed=sd(), rough=.8))
    return art


def plant():
    art = blank(W, H)
    pot = deform([(42, 294), (84, 294), (78, 320), (48, 320)], rng, 1, 0.01)
    art = gouache_form(art, poly_mask(W, H, pot), TERRA, TERRA_D, seed=sd(), sdx=-.25, sdy=0, rough=1.2)
    rim = deform(rect_pts(38, 288, 50, 9, 3), rng, 1, 0.01)
    art = over(art, gouache_paint(shape_mask(W, H, rim, smooth=False), TERRA_L, seed=sd(), rough=1))
    art = outline(art, pot, 1.8); art = outline(art, rim, 1.6)
    for k, (dx, ang, L) in enumerate([(-8, -2.0, 62), (0, -1.62, 78), (8, -1.25, 66), (-14, -2.35, 46), (14, -0.9, 48)]):
        base = (63 + dx * .4, 290)
        m = shape_mask(W, H, petal_pts(base[0], base[1], L, 7.5, ang, n=12))
        art = over(art, gouache_paint(m, [SAGE, SAGE_D, SAGE_L][k % 3], mix(SAGE_D, SAGE, .5), seed=sd(), rough=1.2))
        tip = (base[0] + math.cos(ang) * L * .1, base[1] + math.sin(ang) * L * .1)
        vein = [tip, (base[0] + math.cos(ang) * L * .8, base[1] + math.sin(ang) * L * .8)]
        art = ink(art, stroke_mask(W, H, vein, 1.2, (.1, .3)) * m, "#e9f0d8", seed=sd(), alpha=.35)
    return art


def tumpeng():
    TW, TH = 600, 400
    r = random.Random(33)
    art = blank(TW, TH)
    # tampah (woven bamboo tray)
    tray = ellipse_pts(300, 300, 270, 76, 30)
    tm = shape_mask(TW, TH, deform(tray, r, 1, 0.006))
    art = gouache_form(art, tm, "#d9b77c", "#a9844c", seed=sd(), sdx=0, sdy=.2)
    weave = blank(TW, TH)
    for k in range(-30, 31):
        x = 300 + k * 10
        m = stroke_mask(TW, TH, [(x - 40, 220), (x + 40, 380)], 2.2, (.02, .02)) * tm
        weave = over(weave, gouache_paint(m, "#a9844c", seed=sd(), rough=.3))
    weave[..., 3] *= 0.35
    art = over(art, weave)
    rim = outline_mask(TW, TH, ellipse_pts(300, 300, 270, 76, 30), 7, r, wob=0.002)
    art = over(art, gouache_paint(rim, "#b08c52", "#8e6b39", seed=sd(), rough=1))
    # banana leaf lining: one big leaf ellipse, then radiating leaf ribs + darker leaf seams
    lining = shape_mask(TW, TH, deform(ellipse_pts(300, 294, 248, 64, 30), r, 2, 0.01))
    art = over(art, gouache_paint(lining, "#5f8a4a", "#3f6a34", seed=sd(), rough=2, streak=1.0))
    for k, a in enumerate(np.linspace(0.05, math.pi - 0.05, 11)):
        p0 = (300, 290)
        p1 = (300 + math.cos(a) * 250, 290 + math.sin(a) * 66 * (1 if k % 2 else .9))
        p1b = (300 - math.cos(a) * 250, 290 - math.sin(a) * 60)
        for q in (p1, p1b):
            art = ink(art, stroke_mask(TW, TH, [p0, q], 2.2, (.05, .4)) * lining, "#86ad69" if k % 2 else "#3b6332", seed=sd(), alpha=.5)
    # side dishes
    def egg(x, y, s=1.0):
        nonlocal art
        w_ = shape_mask(TW, TH, deform(ellipse_pts(x, y, 24 * s, 15 * s, 12, .2), r, 1, .05))
        art = over(art, gouache_paint(w_, "#fbf4e6", seed=sd(), rough=1))
        art = over(art, gouache_paint(dab(TW, TH, x + 2, y - 1, 11 * s, 8 * s, 0, r), "#f2b437", "#e39a2a", seed=sd(), rough=.8))
    def chicken(x, y, a=0.3):
        nonlocal art
        m = shape_mask(TW, TH, deform(petal_pts(x, y, 70, 30, a + math.pi, n=16), r, 2, .04))
        bone = shape_mask(TW, TH, petal_pts(x - 4, y, 26, 6, a, n=10))
        art = over(art, gouache_paint(bone, "#efe0c4", seed=sd(), rough=.6))
        art = gouache_form(art, m, "#c07f3e", "#7d4a22", seed=sd(), sdx=-.18, sdy=-.18, rough=2.5)
        for _ in range(16):
            art = over(art, gouache_paint(dab(TW, TH, x - r.uniform(15, 60) * math.cos(a), y - r.uniform(10, 40) * math.sin(a) + r.uniform(-10, 10), 3.4, 2.2, r.uniform(0, 3), r) * m, "#e0ae66", seed=sd(), rough=.4))
    def beans(x, y, n=8):
        nonlocal art
        for i in range(n):
            a = r.uniform(-.35, .35) + .2
            p0 = (x + i * 7 + r.uniform(-2, 2), y + r.uniform(-5, 5))
            m = shape_mask(TW, TH, petal_pts(p0[0], p0[1], 44, 4.4, a, n=10))
            art = over(art, gouache_paint(m, "#5e9a3e", "#4c8432", seed=sd(), rough=.5))
    def chili(x, y, a):
        nonlocal art
        m = shape_mask(TW, TH, petal_pts(x, y, 52, 8, a, n=12, cup=.6))
        art = over(art, gouache_paint(m, "#d0392b", "#a52a20", seed=sd(), rough=.6))
        art = over(art, gouache_paint(stroke_mask(TW, TH, [(x + 2, y), (x - math.cos(a) * 10, y - math.sin(a) * 10 - 4)], 3.4, (.05, .3)), "#4c7a35", seed=sd(), rough=.3))
    def cucumber(x, y):
        nonlocal art
        art = over(art, gouache_paint(dab(TW, TH, x, y, 17, 11, 0, r), "#3f7a3a", seed=sd(), rough=.6))
        art = over(art, gouache_paint(dab(TW, TH, x, y, 13.5, 8.5, 0, r), "#d6e8b4", "#c2dc98", seed=sd(), rough=.4))
        for k in range(3):
            art = over(art, gouache_paint(dab(TW, TH, x - 5 + k * 5, y + (k % 2) * 2 - 1, 1.6, 1.2, 0, r), "#9fbf74", seed=sd(), rough=.2))
    def peanuts(x, y):
        nonlocal art
        for i in range(14):
            art = over(art, gouache_paint(dab(TW, TH, x + r.gauss(0, 16), y + r.gauss(0, 7), 6, 4.2, r.uniform(0, 3), r), "#c58a4a", "#9e6a35", seed=sd(), rough=.4))
    beans(110, 268); peanuts(460, 266); egg(178, 260, 1.0); egg(424, 262, .95)
    # the rice cone: squat, slightly lopsided, rounded shoulders
    pts = []
    for i in range(13):
        t = i / 12
        pts.append((186 + (300 - 186) * t ** 0.9 + r.uniform(-2, 2), 306 - (306 - 96) * t ** 1.08))
    for i in range(1, 13):
        t = i / 12
        pts.append((300 + (418 - 300) * t ** 1.1 + r.uniform(-2, 2), 96 + (306 - 96) * t ** 0.93))
    pts += [(380, 316), (300, 322), (222, 316)]
    cm = shape_mask(TW, TH, pts)
    art = gouache_form(art, cm, "#f3cd4a", "#d39a2a", seed=sd(), sdx=-.18, sdy=0, rough=2.0, streak=0.2)
    tex = blank(TW, TH)
    for _ in range(520):
        x, y = r.uniform(180, 420), r.uniform(96, 318)
        m = dab(TW, TH, x, y, 2.8, 1.4, r.uniform(0, 3), r, n=6, wob=0)
        tex = over(tex, gouache_paint(m * cm, r.choice(["#fbe58c", "#e9b53a", "#f7d665"]), seed=sd(), rough=.2))
    tex[..., 3] *= 0.6
    art = over(art, tex)
    capm = poly_mask(TW, TH, deform([(280, 120), (320, 120), (301, 70)], r, 1, 0.02))
    art = over(art, gouache_paint(capm, "#5f8a4a", "#3f6a34", seed=sd(), rough=1))
    art = ink(art, stroke_mask(TW, TH, [(301, 76), (300, 118)], 1.6, (.1, .2)), "#86ad69", seed=sd(), alpha=.6)
    # front dishes
    chicken(232, 334, 0.35); cucumber(352, 338); cucumber(384, 326); chili(414, 318, -0.45); chili(426, 336, -0.15)
    egg(300, 344, 1.05); beans(88, 302, 7); peanuts(500, 304)
    return art


def roof_divider():
    RW, RH = 120, 48
    r = random.Random(4)
    art = blank(RW, RH)
    m = stroke_mask(RW, RH, [(8, 40), (60, 10), (112, 40)], 6.5, (0.1, 0.1))
    art = over(art, gouache_paint(m, TERRA, TERRA_D, seed=sd(), rough=1.4))
    art = over(art, gouache_paint(dab(RW, RH, 60, 29, 5, 5, 0, r), "#c39a52", seed=sd(), rough=.6))
    return art


if __name__ == "__main__":
    layers = {"house": house(), "lights": lights(), "tree": tree(), "plant": plant()}
    for k, v in layers.items():
        print(k, save_full(v, f"{D}/{k}.webp", quality=82))
    comp = blank(W, H)
    for k in ("tree", "house", "plant", "lights"):
        comp = over(comp, layers[k])
    preview(comp, "sr-house.png", "#f7f1e6")
    bg = np.ones((H, W, 4), np.float32); bg[..., :3] = np.array(hex_rgb("#43553f"))
    to_image(over(bg, comp)).save(f"{PREV_ROOT}/sr-house-dark.png")
    t = tumpeng(); print("tumpeng", save_asset(t, f"{D}/tumpeng.webp", max_w=560, quality=80)); preview(t, "sr-tumpeng.png", "#efe5d3")
    print("roof", save_asset(roof_divider(), f"{D}/roof.webp", quality=84))
    print("paper", paper_tile(f"{D}/paper.webp", "#fdfbf7", seed=21, fiber=1.0, mottle=0.35))
    report(D)
