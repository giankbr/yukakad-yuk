"""Ultah Dino — kids birthday, friendly gouache dinosaurs (original characters): Moli the round green long-neck, Teri the
small orange triceratops, a volcano-shaped birthday cake, prehistoric ferns, footprints, a spotted egg, a grassy ground.
Run: python3 -I ultah-dino.py [part ...]  parts: longneck trike cake fern foot egg ground sun
Assets -> public/themes/art/ultah-dino/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *

OUT = outdir("ultah-dino")
PARTS = sys.argv[1:] or ["longneck", "trike", "cake", "fern", "foot", "egg", "ground", "sun"]
INK = "#3b2a1e"          # warm sepia line
GREEN, GREEN_D, GREEN_L, BELLY = "#7dbb5a", "#4f8a3c", "#a9d77e", "#e9e2a6"
ORANGE, ORANGE_D, FRILL, HORN = "#f0904a", "#c9622e", "#f7c35c", "#f6ecd2"
CHOC, CHOC_D, CREAM, PINK, PINK_D = "#7a4a2f", "#57321f", "#f7e8cf", "#f48aa0", "#d9607d"
CHEEK = "#f59aa0"


def eye(art, W, H, x, y, r, nx):
    art = GP(art, circles(W, H, [(x, y, r)]), "#2a1c14", seed=nx(), rough=0.4, pad=6)
    art = OV(art, circles(W, H, [(x - r * 0.35, y - r * 0.38, r * 0.34)]), lambda m: col_arr(m, "#ffffff", m))
    return art


def cheek(art, W, H, x, y, r, nx):
    return G(art, circles(W, H, [(x, y, r)]), CHEEK, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=2, feather=2.5)


def body_paint(art, m, col, col2, dark, light, nx, light_dir=(-14, -16), outline=True):
    art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=0.45)
    art = tint(art, side_light(m, *light_dir, 9), dark, 0.75, seed=nx())
    art = tint(art, side_light(m, -light_dir[0] * .7, -light_dir[1] * .7, 7), light, 0.5, seed=nx())
    if outline:
        art = crayon(art, inner_edge(m, 2.2), mix(dark, INK, 0.45), seed=nx(), amt=0.8, tooth=0.25)
    return art


if "longneck" in PARTS:
    W, H = 560, 560
    nx = Seq(20100); rng = random.Random(3)
    # body (round), neck curving up-left, small head, tail to the right, four stubby legs
    body = shapes(W, H, [deform(ellipse_pts(330, 390, 150, 112, 16, -0.08), rng, 1, 0.02)])
    neck_c = curve([(250, 360), (205, 300), (175, 220), (170, 150), (190, 108)], 40)
    neck = strokes(W, H, [(neck_c, 66, (0.0, 0.0))])
    neck = np.maximum(neck, strokes(W, H, [(neck_c[:22], 86, (0.0, 0.0))]))
    head = shapes(W, H, [deform(ellipse_pts(214, 104, 62, 44, 14, 0.12), rng, 1, 0.02)])
    tail = strokes(W, H, [(curve([(440, 400), (500, 410), (540, 380), (548, 344)], 30), 54, (0.0, 0.85))])
    legs = shapes(W, H, [[(x - 30, 430), (x + 30, 430), (x + 32, 500), (x + 26, 512), (x - 26, 512), (x - 32, 500)] for x in (238, 408)])
    legs_b = shapes(W, H, [[(x - 26, 440), (x + 26, 440), (x + 28, 496), (x + 22, 506), (x - 22, 506), (x - 28, 496)] for x in (296, 456)])
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(340, 514, 200, 16, 20)])
    art = G(art, shadow, "#5b4a2e", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=5)
    art = body_paint(art, legs_b, GREEN_D, "#457a33", "#2f5a26", GREEN, nx)
    art = body_paint(art, tail, GREEN, GREEN_D, GREEN_D, GREEN_L, nx)
    full = np.clip(body + neck + head, 0, 1)
    art = body_paint(art, full, GREEN, "#86c463", GREEN_D, GREEN_L, nx)
    art = body_paint(art, legs, GREEN, GREEN_D, GREEN_D, GREEN_L, nx)
    # toenails
    art = GP(art, ellipses(W, H, [(x + dx, 508, 7, 4, 0) for x in (238, 408) for dx in (-15, 0, 15)]), HORN, seed=nx(), rough=0.5, pad=6)
    # belly patch + neck underside
    belly = shapes(W, H, [deform(ellipse_pts(292, 448, 84, 40, 14, -0.12), rng, 1, 0.03)]) * body
    under = strokes(W, H, [([(x + 18, y + 6) for x, y in neck_c[6:30]], 22, (0.1, 0.3))]) * neck
    art = GP(art, np.clip(belly + under, 0, 1), BELLY, "#f1ecbd", seed=nx(), rough=1.2, streak=0.8)
    art = tint(art, side_light(belly, 0, -10, 6), "#cfc382", 0.5, seed=nx())
    # spots
    sp = []
    for _ in range(11):
        sx, sy = rng.uniform(250, 440), rng.uniform(300, 380)
        sp.append(deform(ellipse_pts(sx, sy, rng.uniform(9, 17), rng.uniform(7, 12), 10, rng.uniform(0, 3)), rng, 1, 0.05))
    for t in (0.35, 0.5, 0.65):
        px, py = neck_c[int(t * len(neck_c))]
        sp.append(deform(ellipse_pts(px - 10, py, 8, 6, 10, 0.5), rng, 1, 0.05))
    spots = shapes(W, H, sp) * np.clip(body + neck, 0, 1) * (1 - belly)
    art = GP(art, spots, "#5f9d45", "#538f3e", seed=nx(), rough=1.0, pad=8)
    # face
    art = eye(art, W, H, 226, 94, 8.5, nx)
    art = cheek(art, W, H, 230, 122, 9, nx)
    smile = strokes(W, H, [(arc_pts(254, 104, 13, 0.5, 1.9, 14), 3.2, (0.2, 0.2))])
    art = crayon(art, smile, INK, seed=nx(), amt=0.9)
    nost = circles(W, H, [(266, 92, 2.6)])
    art = OV(art, nost, lambda m: col_arr(m, INK, m * 0.7))
    # little party hat
    hat = shapes(W, H, [[(192, 66), (228, 70), (204, 14)]], smooth=False)
    art = GP(art, hat, "#f7c35c", "#f0a842", seed=nx(), rough=0.8, pad=8)
    stripes = strokes(W, H, [([(196, 50), (222, 54)], 5, None), ([(201, 34), (217, 37)], 4, None)]) * hat
    art = GP(art, stripes, PINK, seed=nx(), rough=0.4, pad=6)
    art = GP(art, circles(W, H, [(204, 14, 8)]), "#7fc6c0", seed=nx(), rough=0.6, pad=6)
    art = crayon(art, inner_edge(hat, 1.8), "#b9782a", seed=nx(), amt=0.7, tooth=0.25)
    preview(art, "dino-longneck")
    save(art, f"{OUT}/longneck.webp", max_w=480, quality=82)
    clear()

if "trike" in PARTS:
    W, H = 460, 360
    nx = Seq(20200); rng = random.Random(5)
    body = shapes(W, H, [deform(ellipse_pts(270, 220, 120, 82, 16, 0.02), rng, 1, 0.02)])
    tail = strokes(W, H, [(curve([(370, 230), (410, 240), (440, 226)], 20), 40, (0.0, 0.9))])
    frill = shapes(W, H, [deform(ellipse_pts(148, 150, 78, 90, 18, -0.35), rng, 1, 0.02)])
    head = shapes(W, H, [deform(ellipse_pts(122, 196, 66, 52, 16, 0.15), rng, 1, 0.02)])
    beak = shapes(W, H, [[(70, 196), (40, 216), (60, 240), (96, 236)]])
    legs = shapes(W, H, [[(x - 24, 260), (x + 24, 260), (x + 26, 322), (x + 20, 332), (x - 20, 332), (x - 26, 322)] for x in (200, 330)])
    legs_b = shapes(W, H, [[(x - 20, 266), (x + 20, 266), (x + 22, 318), (x + 16, 326), (x - 16, 326), (x - 22, 318)] for x in (246, 370)])
    horns = shapes(W, H, [petal_pts(112, 150, 56, 9, -2.2, n=12), petal_pts(152, 160, 52, 9, -1.55, n=12), petal_pts(70, 196, 26, 7, -2.0, n=10)])
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(260, 334, 170, 12, 20)])
    art = G(art, shadow, "#5b4a2e", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=5)
    art = body_paint(art, legs_b, ORANGE_D, "#b9572a", "#8d3f1d", ORANGE, nx)
    art = body_paint(art, tail, ORANGE, ORANGE_D, ORANGE_D, "#f7b07a", nx)
    art = body_paint(art, body, ORANGE, "#f39c58", ORANGE_D, "#f8b984", nx)
    art = body_paint(art, legs, ORANGE, ORANGE_D, ORANGE_D, "#f8b984", nx)
    art = body_paint(art, frill, FRILL, "#f4b04a", "#d9923a", "#fbe08f", nx)
    # frill scallop dots
    dots_ = []
    for k in range(9):
        a = -0.35 + -math.pi * 0.15 + k * 0.42
        dots_.append((148 + math.cos(a - 1.6) * 66, 150 + math.sin(a - 1.6) * 76, 6.5))
    art = GP(art, circles(W, H, dots_) * frill, "#f08a7a", seed=nx(), rough=0.6, pad=6)
    art = body_paint(art, head, ORANGE, "#f39c58", ORANGE_D, "#f8b984", nx)
    art = body_paint(art, beak, "#e7c39a", "#d8a978", "#b9875a", "#f3dcbc", nx)
    art = body_paint(art, horns, HORN, "#efe0bb", "#cdb98d", "#fffaf0", nx)
    belly = shapes(W, H, [deform(ellipse_pts(270, 262, 90, 34, 12, 0.0), rng, 1, 0.03)]) * body
    art = GP(art, belly, "#f8c99a", "#f6d3a8", seed=nx(), rough=1.0)
    sp = [deform(ellipse_pts(rng.uniform(220, 350), rng.uniform(170, 220), rng.uniform(8, 13), rng.uniform(6, 9), 10, rng.uniform(0, 3)), rng, 1, 0.05) for _ in range(8)]
    art = GP(art, shapes(W, H, sp) * body * (1 - belly), "#e47a3a", seed=nx(), rough=0.9, pad=8)
    art = GP(art, ellipses(W, H, [(x + dx, 328, 6, 3.5, 0) for x in (200, 330) for dx in (-12, 0, 12)]), HORN, seed=nx(), rough=0.5, pad=6)
    art = eye(art, W, H, 114, 186, 7.5, nx)
    art = cheek(art, W, H, 132, 214, 10, nx)
    art = crayon(art, strokes(W, H, [(arc_pts(96, 216, 14, 0.6, 1.9, 12), 3, (0.2, 0.2))]), INK, seed=nx(), amt=0.85)
    preview(art, "dino-trike")
    save(art, f"{OUT}/trike.webp", max_w=400, quality=82)
    clear()

if "cake" in PARTS:
    W, H = 420, 460
    nx = Seq(20300); rng = random.Random(7)
    cx = 210
    plate = shapes(W, H, [ellipse_pts(cx, 420, 186, 22, 24)])
    cone = shapes(W, H, [[(cx - 160, 410), (cx - 128, 330), (cx - 92, 230), (cx - 62, 160), (cx - 46, 150), (cx + 46, 150), (cx + 62, 160), (cx + 92, 230), (cx + 128, 330), (cx + 160, 410)]])
    art = blank(W, H)
    art = GP(art, plate, "#bfe3df", "#9fd0cb", seed=nx(), rough=0.8)
    art = tint(art, side_light(plate, 0, -6, 3), "#78b2ad", 0.6, seed=nx())
    art = body_paint(art, cone, CHOC, "#8a5536", CHOC_D, "#9a6444", nx, light_dir=(-16, 0))
    # cream layers (wavy bands)
    bands = []
    for y in (370, 290):
        pts = [(x, y + 5 * math.sin(x / 14)) for x in range(cx - 170, cx + 171, 6)]
        bands.append((pts, 14, None))
    layers = strokes(W, H, bands) * cone
    art = GP(art, layers, CREAM, "#f3dcb8", seed=nx(), rough=0.8)
    # pink lava frosting from the crater with drips
    lava_pts = [(cx - 70, 172), (cx - 56, 144), (cx - 30, 130), (cx + 30, 130), (cx + 56, 144), (cx + 70, 172)]
    lava = shapes(W, H, [lava_pts])
    drips = []
    for k, (dx, L) in enumerate([(-58, 60), (-34, 96), (-8, 40), (16, 120), (40, 70), (60, 50)]):
        x = cx + dx
        drips.append(([(x, 150), (x + rng.uniform(-6, 6) - dx * 0.25, 150 + L)], 16 - abs(dx) * 0.07, (0.0, 0.0)))
    lava = np.clip(lava + strokes(W, H, drips), 0, 1)
    art = body_paint(art, lava, PINK, "#f59ab0", PINK_D, "#f9bccb", nx, light_dir=(-8, -8))
    # sprinkles
    spr = []
    for _ in range(26):
        x = rng.uniform(cx - 130, cx + 130); y = rng.uniform(190, 400)
        a = rng.uniform(0, math.pi)
        spr.append(([(x, y), (x + math.cos(a) * 9, y + math.sin(a) * 9)], 4.2, None))
    sprm = strokes(W, H, spr) * cone * (1 - lava)
    for i, c in enumerate(("#f7c35c", "#7fc6c0", "#ffffff", "#a9d77e")):
        sel = strokes(W, H, spr[i::4]) * cone * (1 - lava)
        art = GP(art, sel, c, seed=nx(), rough=0.3, pad=6)
    # five candles erupting from the crater
    for k, (dx, h, c) in enumerate([(-44, 52, "#7fc6c0"), (-22, 70, "#f7c35c"), (0, 84, "#a9d77e"), (22, 70, "#b9a3e3"), (44, 52, "#f48aa0")]):
        x = cx + dx; top = 136 - h + abs(dx) * 0.4
        cm = shapes(W, H, [[(x - 6, 142), (x - 6, top), (x + 6, top), (x + 6, 142)]], smooth=False)
        art = GP(art, cm, c, seed=nx(), rough=0.5, pad=6)
        art = GP(art, strokes(W, H, [([(x - 6, top + j), (x + 6, top + j - 6)], 2.4, None) for j in range(10, int(142 - top), 14)]) * cm, "#ffffff", seed=nx(), rough=0.3, pad=6, density=0.8)
        fl = shapes(W, H, [petal_pts(x, top - 4, 24, 8, -math.pi / 2 + rng.uniform(-.15, .15), n=12)])
        art = OV(art, fl, lambda m: col_arr(m, "#ffd45c", np.clip(gaussian_filter(m, 7) * 1.4, 0, 1) * 0.35), pad=20)
        art = GP(art, fl, "#ffb43c", "#ff8a3c", seed=nx(), rough=0.5, pad=6)
        art = GP(art, shapes(W, H, [petal_pts(x, top - 6, 12, 4, -math.pi / 2, n=10)]), "#fff2b8", seed=nx(), rough=0.3, pad=6)
    preview(art, "dino-cake")
    save(art, f"{OUT}/cake.webp", max_w=320, quality=82)
    clear()

if "fern" in PARTS:
    W, H = 320, 520
    nx = Seq(20400); rng = random.Random(11)
    art = blank(W, H)
    for (base, tip, sc, cols) in [((150, 515), (60, 40), 1.0, (GREEN_D, "#3f7432")), ((170, 515), (290, 120), 0.82, (GREEN, GREEN_D)), ((160, 515), (175, 170), 0.7, ("#94c96a", GREEN))]:
        mid = ((base[0] + tip[0]) / 2 + (tip[1] - base[1]) * -0.12, (base[1] + tip[1]) / 2)
        stem = curve([base, mid, tip], 60)
        leaves = []
        n = len(stem)
        for i in range(4, n - 2, 2):
            t = i / n
            x, y = stem[i]; a, b = stem[i - 1], stem[i + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            L = (12 + 40 * math.sin(math.pi * min(1, (1 - t) * 1.1)) ** 0.8) * sc
            for side in (-1, 1):
                leaves.append(petal_pts(x, y, L, L * 0.26, ang + side * 1.05, n=10))
        m = np.maximum(shapes(W, H, leaves), strokes(W, H, [(stem, 4.5 * sc, (0.0, 0.6))]))
        art = GP(art, m, cols[0], cols[1], seed=nx(), rough=1.4, streak=1.1)
        art = tint(art, side_light(m, 4, -5, 3), "#c8e69a", 0.35, seed=nx())
    preview(art, "dino-fern")
    save(art, f"{OUT}/fern.webp", max_w=220, quality=82)
    clear()

if "foot" in PARTS:
    W, H = 160, 170
    nx = Seq(20500); rng = random.Random(13)
    pad_ = shapes(W, H, [deform(ellipse_pts(80, 112, 34, 38, 14), rng, 1, 0.04)])
    toes = shapes(W, H, [petal_pts(80, 92, 70, 15, -math.pi / 2, n=12), petal_pts(70, 96, 62, 14, -math.pi / 2 - 0.62, n=12), petal_pts(90, 96, 62, 14, -math.pi / 2 + 0.62, n=12)])
    m = np.clip(pad_ + toes, 0, 1)
    art = GP(blank(W, H), m, "#8b6a46", "#6f5236", seed=nx(), rough=2.2, streak=1.2, dry=0.25, density=0.9)
    art = tint(art, inner_edge(m, 3), "#5a412a", 0.4, seed=nx())
    preview(art, "dino-foot")
    save(art, f"{OUT}/foot.webp", max_w=72, quality=82)
    clear()

if "egg" in PARTS:
    W, H = 440, 540
    nx = Seq(20600); rng = random.Random(17)
    pts = []
    for i in range(40):
        t = i / 40 * math.tau
        r = 1 + 0.14 * math.sin(t)  # pointier top (t=-pi/2 -> smaller)
        pts.append((220 + math.cos(t) * 180 * (1 - 0.1 * (math.sin(t) < 0) * abs(math.sin(t))), 280 + math.sin(t) * 240 * (0.94 if math.sin(t) > 0 else 1.0)))
    m = shapes(W, H, [pts])
    art = GP(blank(W, H), m, "#f6efd8", "#efe4c2", seed=nx(), rough=1.4, streak=0.9)
    art = tint(art, side_light(m, -20, -20, 18), "#d9cba0", 0.7, seed=nx())
    art = tint(art, side_light(m, 16, 18, 14), "#fffbea", 0.5, seed=nx())
    sp = [deform(ellipse_pts(rng.uniform(80, 360), rng.uniform(80, 500), rng.uniform(12, 28), rng.uniform(10, 22), 10, rng.uniform(0, 3)), rng, 1, 0.06) for _ in range(16)]
    art = GP(art, shapes(W, H, sp) * m, "#a9d77e", "#8cc46a", seed=nx(), rough=1.0, density=0.85)
    art = crayon(art, inner_edge(m, 2.4), "#b7a57a", seed=nx(), amt=0.7, tooth=0.25)
    preview(art, "dino-egg")
    save(art, f"{OUT}/egg.webp", max_w=300, quality=80)
    clear()

if "ground" in PARTS:
    W, H = 900, 220
    nx = Seq(20700); rng = random.Random(19)
    back = hills(W, H, 92, 26, 3, 0.7)
    front = hills(W, H, 140, 18, 8, 0.45)
    art = GP(blank(W, H), back, "#a9d77e", "#9ccd70", seed=nx(), rough=2, streak=1.1)
    art = GP(art, front, "#86c463", "#7dbb5a", seed=nx(), rough=2, streak=1.2)
    art = tint(art, side_light(front, 0, 14, 8), "#b9e08f", 0.4, seed=nx())
    # grass tufts + pebbles
    tufts = []
    for _ in range(40):
        x = rng.uniform(10, W - 10); y = rng.uniform(150, 210)
        for a in (-0.5, 0, 0.5):
            tufts.append(([(x, y), (x + math.sin(a) * 14, y - 16 + abs(a) * 6)], 3.2, (0.0, 0.8)))
    art = GP(art, strokes(W, H, tufts) * front, "#5f9d45", seed=nx(), rough=0.5)
    peb = ellipses(W, H, [(rng.uniform(20, W - 20), rng.uniform(170, 212), rng.uniform(5, 10), rng.uniform(3, 6), rng.uniform(-20, 20)) for _ in range(16)]) * front
    art = GP(art, peb, "#e9e2c6", "#d3c9a8", seed=nx(), rough=0.6)
    save_full(art, f"{OUT}/ground.webp", size=(600, 147), quality=80)
    preview(art, "dino-ground")
    clear()

if "sun" in PARTS:
    W, H = 300, 300
    nx = Seq(20800)
    disc = circles(W, H, [(150, 150, 70)])
    rays = strokes(W, H, [([(150 + math.cos(a) * 92, 150 + math.sin(a) * 92), (150 + math.cos(a) * 132, 150 + math.sin(a) * 132)], 16, (0.2, 0.5)) for a in [k * math.tau / 12 + 0.1 for k in range(12)]])
    art = GP(blank(W, H), rays, "#f7c35c", "#f4b04a", seed=nx(), rough=1.6, streak=1.0, dry=0.2)
    art = GP(art, disc, "#ffd46a", "#f7c35c", seed=nx(), rough=1.6, streak=1.0)
    art = tint(art, side_light(disc, -12, -12, 10), "#f0a842", 0.5, seed=nx())
    preview(art, "dino-sun")
    save(art, f"{OUT}/sun.webp", max_w=160, quality=80)
    clear()
