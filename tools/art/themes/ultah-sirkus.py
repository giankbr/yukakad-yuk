"""Ultah Sirkus — kids birthday under a striped big top (gouache + crayon, original characters): a red/cream circus tent with
teal scalloped valance and a pennant, a friendly seal balancing a beach ball on a star drum, a balloon trio, a striped
popcorn box, scallop-flag bunting and a painted gold star. Run: python3 -I ultah-sirkus.py [part ...]
parts: tent seal balloons popcorn bunting star   Assets -> public/themes/art/ultah-sirkus/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d6_lib import *

OUT = outdir("ultah-sirkus")
PARTS = sys.argv[1:] or ["tent", "seal", "balloons", "popcorn", "bunting", "star"]
INK = "#2b2140"
RED, RED2, REDD, REDL = "#d8402f", "#e05238", "#9e2a22", "#f07a5a"
CREAM, CREAM2, CREAMD = "#fbf1dc", "#f6e6c6", "#d9bf94"
TEAL, TEAL2, TEALD, TEALL = "#2f8a92", "#3a9aa0", "#1d5c66", "#6cc0c0"
GOLD, GOLD2, GOLDD, GOLDL = "#f2b134", "#f6c457", "#b97a1c", "#ffe7a8"
BG = "#fbf3e2"


def shade_line(art, m, nx, col=INK, amt=0.75):
    return crayon(art, inner_edge(m, 2.2), col, seed=nx(), amt=amt, tooth=0.28)


if "tent" in PARTS:
    W, H = 760, 660
    nx = Seq(61100); rng = random.Random(611)
    art = blank(W, H)
    px, py = 380, 92
    art = soft_ground(art, W, H, 380, 606, 330, 26, "#7a5a3a", nx, 0.32)
    # wall (cylinder) with vertical stripes in perspective
    wall_poly = [(118, 300), (642, 300), (646, 592)] + [(380 + 266 * math.cos(t), 592 + 22 * math.sin(t)) for t in np.linspace(0, math.pi, 30)] + [(114, 592)]
    wall = shapes(W, H, [deform(wall_poly, rng, 1, 0.003)], smooth=False)
    xx = np.arange(W, dtype=np.float32)
    u = np.arcsin(np.clip((xx - 380) / 300, -1, 1)) / math.pi * 15
    band = (np.clip(np.minimum(u % 1.0, 0.5 - (u % 1.0)) * 30 + 0.5, 0, 1) * ((u % 1.0) < 0.52))[None, :] * np.ones((H, 1), np.float32)
    art = body_paint(art, wall, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(26, -4), blur=22, light_amt=0.3)
    art = GP(art, wall * band, RED, RED2, seed=nx(), rough=1.2, streak=0.6)
    art = tint(art, side_light(wall, 30, 0, 26) * 1.0, REDD, 0.45, seed=nx())
    art = tint(art, gaussian_filter(strokes(W, H, [([(120, 312), (640, 312)], 30, None)]), 10) * wall, "#5a2a20", 0.35, seed=nx())
    # entrance: dark interior + tied-back flaps
    door = shapes(W, H, [[(380, 336), (446, 600), (314, 600)]], smooth=False)
    art = GP(art, door, "#2b2140", "#3a2850", seed=nx(), rough=1.0)
    gl = gaussian_filter(ellipses(W, H, [(380, 610, 70, 90, 0)]), 26) * door
    art = OV(art, gl, lambda m: col_arr(m, "#f6b24a", np.clip(m * 1.1, 0, 0.8)), pad=4)
    art = OV(art, ellipses(W, H, [(380, 588, 40, 7, 0)]) * door, lambda m: col_arr(m, "#ffe3a0", m * 0.6), pad=4)
    flapL = shapes(W, H, [[(380, 334), (314, 600), (290, 600), (312, 470), (350, 400)]])
    flapR = shapes(W, H, [[(380, 334), (446, 600), (470, 600), (448, 470), (410, 400)]])
    art = body_paint(art, flapL, RED, RED2, REDD, REDL, nx, ldir=(8, -6), blur=8)
    art = body_paint(art, flapR, RED, RED2, REDD, REDL, nx, ldir=(-8, -6), blur=8)
    ties = strokes(W, H, [([(300, 488), (326, 480)], 7, None), ([(460, 488), (434, 480)], 7, None)])
    art = GP(art, ties, GOLD, GOLD2, seed=nx(), rough=0.5, pad=6)
    art = shade_line(art, wall, nx, amt=0.6)
    # roof: concave cone with radial stripes from the peak
    left = curve([(px, py), (300, 170), (190, 248), (66, 318)], 40)
    right = curve([(700 - 6, 318), (570, 248), (460, 170), (px, py)], 40)
    bottom = [(66 + (694 - 66) * t, 318 + 26 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 40)]
    roof = shapes(W, H, [left + bottom + right], smooth=False)
    roof = np.clip(gaussian_filter(roof, 1.0) * 1.2, 0, 1)
    fan = radial_stripes(W, H, px, py, 30, 0.5, rot=0.05, wob=0.025, seed=nx())
    art = body_paint(art, roof, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(18, -10), blur=18, light_amt=0.3)
    art = GP(art, roof * fan, RED, RED2, seed=nx(), rough=1.0, streak=0.6)
    art = tint(art, side_light(roof, 24, -6, 22), REDD, 0.5, seed=nx())
    art = tint(art, side_light(roof, -18, 8, 16), "#fff4dc", 0.35, seed=nx())
    # sag shading along each seam bottom
    art = shade_line(art, roof, nx, amt=0.7)
    # scalloped valance (teal + gold dots)
    sc = []
    n = 15
    for i in range(n):
        t = (i + 0.5) / n
        x = 66 + (694 - 66) * t
        y = 318 + 26 * math.sin(t * math.pi)
        sc.append((x, y, (694 - 66) / n * 0.55))
    val = np.clip(circles(W, H, sc) - shapes(W, H, [[(0, 0), (W, 0), (W, 1)] + [(694 - (694 - 66) * t, 316 + 26 * math.sin((1 - t) * math.pi) - 2) for t in np.linspace(0, 1, 40)] + [(0, 1)]], smooth=False), 0, 1)
    band = strokes(W, H, [(bottom, 14, None)])
    val = np.clip(val + band, 0, 1)
    art = body_paint(art, val, TEAL, TEAL2, TEALD, TEALL, nx, ldir=(10, -8), blur=6, line=mix(TEALD, INK, .4))
    dots = circles(W, H, [(x, y + r * 0.45, 4.6) for x, y, r in sc])
    art = GP(art, dots, GOLD, GOLDL, seed=nx(), rough=0.4, pad=6)
    trim = strokes(W, H, [(bottom, 4, None)])
    art = crayon(art, trim, GOLD, seed=nx(), amt=0.9, tooth=0.2)
    # pole, finial and pennant
    art = GP(art, strokes(W, H, [([(px, py + 4), (px, 22)], 6, None)]), "#7a5a3a", seed=nx(), rough=0.4, pad=6)
    flag = shapes(W, H, [curve([(px + 2, 26), (px + 50, 30), (px + 98, 42), (px + 54, 50), (px + 2, 62)], 30)], smooth=False)
    art = body_paint(art, flag, TEAL, TEAL2, TEALD, TEALL, nx, ldir=(0, -6), blur=5, line=mix(TEALD, INK, .4))
    art = GP(art, shapes(W, H, [star_pts(px + 40, 44, 9, 4)], smooth=False), GOLD, GOLDL, seed=nx(), rough=0.3, pad=6)
    art = body_paint(art, circles(W, H, [(px, 20, 10)]), GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(-3, -3), blur=3)
    art = body_paint(art, ellipses(W, H, [(px, py + 2, 16, 8, 0)]), GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(-3, -3), blur=3)
    # string of bulbs along valance
    bulbs = []
    for i in range(22):
        t = (i + 0.5) / 22
        bulbs.append((70 + (690 - 70) * t, 352 + 30 * math.sin(t * math.pi)))
    wire = strokes(W, H, [(curve([(70, 344), (380, 384), (690, 344)], 60), 2.0, None)])
    art = crayon(art, wire, INK, seed=nx(), amt=0.6, tooth=0.2)
    bm = circles(W, H, [(x, y, 5.2) for x, y in bulbs])
    art = OV(art, bm, lambda m: glow(m, "#ffd77a", 6, 0.6), pad=20)
    art = GP(art, bm, "#fff1c2", "#ffe08a", seed=nx(), rough=0.3, pad=6)
    preview(art, "sk-tent", tone=BG)
    save(art, f"{OUT}/tent.webp", max_w=560, quality=80)
    clear()

if "seal" in PARTS:
    W, H = 440, 600
    nx = Seq(61200); rng = random.Random(612)
    art = blank(W, H)
    GREY, GREY2, GREYD, GREYL, BELLY = "#6d88a0", "#7a96ac", "#45607a", "#a7c0d2", "#a9c0cf"
    art = soft_ground(art, W, H, 220, 566, 140, 14, "#6a4a30", nx, 0.35)
    # drum pedestal
    drum = shapes(W, H, [[(112, 452), (328, 452), (322, 556)] + [(220 + 102 * math.cos(t), 556 + 18 * math.sin(t)) for t in np.linspace(0, math.pi, 24)] + [(118, 556)]], smooth=False)
    art = body_paint(art, drum, RED, RED2, REDD, REDL, nx, ldir=(18, -2), blur=16)
    zig = []
    for i in range(9):
        x0 = 118 + i * 23.5
        zig.append([(x0, 474), (x0 + 11.75, 534), (x0 + 23.5, 474)])
    art = GP(art, shapes(W, H, zig, smooth=False) * drum, CREAM, CREAM2, seed=nx(), rough=0.8)
    art = GP(art, strokes(W, H, [([(114, 470), (326, 470)], 8, None), ([(118, 540), (322, 540)], 8, None)]) * drum, GOLD, GOLD2, seed=nx(), rough=0.6)
    art = tint(art, side_light(drum, 22, 0, 16), REDD, 0.4, seed=nx())
    top = ellipses(W, H, [(220, 452, 108, 20, 0)])
    art = body_paint(art, top, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(8, -4), blur=6, line=mix(GOLDD, INK, .3))
    art = shade_line(art, drum, nx, amt=0.6)
    # seal body
    outline = [(146, 448), (134, 392), (146, 330), (178, 274), (204, 226), (222, 188), (250, 160), (284, 150), (316, 158), (334, 178),
               (326, 200), (302, 214), (290, 240), (294, 292), (312, 352), (318, 410), (306, 448)]
    sb = shapes(W, H, [deform(outline, rng, 1, 0.004)])
    tail = shapes(W, H, [[(296, 444), (344, 420), (372, 426), (352, 446), (376, 456), (340, 460), (300, 456)]])
    art = body_paint(art, tail, GREY, GREY2, GREYD, GREYL, nx, ldir=(6, -6), blur=6, line=mix(GREYD, INK, .4))
    art = body_paint(art, sb, GREY, GREY2, GREYD, GREYL, nx, ldir=(16, -8), blur=18, line=mix(GREYD, INK, .45))
    belly = shapes(W, H, [deform([(170, 440), (164, 384), (176, 326), (202, 278), (222, 250), (230, 284), (226, 340), (220, 400), (210, 442)], rng, 1, 0.01)]) * sb
    art = GP(art, belly, BELLY, "#b8ccd8", seed=nx(), rough=1.0, streak=0.7)
    art = tint(art, side_light(belly, 8, 0, 8), "#9fb4c2", 0.45, seed=nx())
    # front flipper
    fl = shapes(W, H, [petal_pts(262, 300, 86, 26, 1.0, n=14)])
    art = body_paint(art, fl, GREYD, GREY, "#33485e", GREY2, nx, ldir=(4, -6), blur=6, line=mix(GREYD, INK, .5))
    # spots
    sp = [deform(ellipse_pts(rng.uniform(250, 300), rng.uniform(330, 420), rng.uniform(5, 9), rng.uniform(4, 6), 10, rng.uniform(0, 3)), rng, 1, 0.05) for _ in range(6)]
    art = GP(art, shapes(W, H, sp) * sb * (1 - belly), "#58718a", seed=nx(), rough=0.6, pad=6)
    # face: muzzle, nose, eye, cheek, whiskers
    muzzle = ellipses(W, H, [(318, 176, 18, 14, -20)])
    art = GP(art, muzzle * sb, "#93abbd", "#9cb3c4", seed=nx(), rough=0.6, pad=6)
    art = body_paint(art, ellipses(W, H, [(334, 164, 10, 7.5, -25)]), "#2b2a35", "#3a3946", "#16151c", "#6a6a7a", nx, ldir=(2, 2), blur=3)
    art = eye(art, W, H, 282, 172, 9, nx)
    art = cheek(art, W, H, 296, 196, 9, nx)
    art = smile(art, W, H, 316, 182, 12, nx, a0=0.6, a1=2.2, w=2.6)
    wh = [([(322, 184), (348, 190)], 1.6, (0.0, 0.5)), ([(322, 180), (350, 180)], 1.6, (0.0, 0.5)), ([(306, 186), (282, 196)], 1.6, (0.0, 0.5))]
    art = crayon(art, strokes(W, H, wh), "#2b2a35", seed=nx(), amt=0.6, tooth=0.2)
    # beach ball on the nose
    bx, by, br = 342, 94, 60
    disc = circles(W, H, [(bx, by, br)])
    cols = [RED, CREAM, TEAL, CREAM, GOLD, CREAM]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy - (by - br * 0.75), (xx - (bx - br * 0.2)) * 1.0)
    seg = ((ang + math.pi) / (2 * math.pi) * 12).astype(int) % 6
    for i, c in enumerate(cols):
        if c == CREAM:
            continue
        m = disc * (seg == i).astype(np.float32)
        m = gaussian_filter(m, 0.8)
        art = GP(art, m, c, mix(c, "#ffffff", 0.12), seed=nx(), rough=0.8)
    art = GP(art, disc * (1 - np.isin(seg, [0, 2, 4]).astype(np.float32)), CREAM, CREAM2, seed=nx(), rough=0.8)
    art = tint(art, side_light(disc, 18, 16, 18), "#2b2140", 0.38, seed=nx())
    art = tint(art, side_light(disc, -14, -14, 14), "#ffffff", 0.4, seed=nx())
    art = body_paint(art, circles(W, H, [(bx - br * 0.2, by - br * 0.75, 9)]), CREAM, CREAM2, CREAMD, "#ffffff", nx, blur=3)
    art = shade_line(art, disc, nx, amt=0.7)
    # motion marks
    mm = strokes(W, H, [(arc_pts(bx, by, br + 16, 3.6, 4.3, 10), 3.4, (0.3, 0.3)), (arc_pts(bx, by, br + 16, 5.2, 5.8, 10), 3.4, (0.3, 0.3))])
    art = crayon(art, mm, GOLDD, seed=nx(), amt=0.7)
    preview(art, "sk-seal", tone=BG)
    save(art, f"{OUT}/seal.webp", max_w=300, quality=82)
    clear()

if "balloons" in PARTS:
    W, H = 380, 560
    nx = Seq(61300); rng = random.Random(613)
    art = blank(W, H)
    knot_pt = (196, 520)
    specs = [(118, 168, 66, 80, RED, RED2, REDD, REDL, -0.2), (266, 150, 62, 76, TEAL, TEAL2, TEALD, TEALL, 0.3), (190, 270, 64, 78, GOLD, GOLD2, GOLDD, GOLDL, 0.0)]
    items = []
    for x, y, rx, ry, *_ in specs:
        items.append((curve([(x, y + ry * 1.08), ((x + knot_pt[0]) / 2 + rng.uniform(-18, 18), (y + ry + knot_pt[1]) / 2), knot_pt], 40), 2.0, (0.0, 0.0)))
    art = crayon(art, strokes(W, H, items), "#7d6f68", seed=nx(), amt=0.7, tooth=0.2)
    bow = shapes(W, H, [petal_pts(196, 520, 22, 9, 2.6, n=12), petal_pts(196, 520, 22, 9, 0.5, n=12)])
    art = GP(art, bow, RED, RED2, seed=nx(), rough=0.6, pad=6)
    for x, y, rx, ry, c, c2, d, l, sw in specs:
        art = balloon(art, W, H, x, y, rx, ry, c, c2, d, l, nx, rng, string=False)
        art = shade_line(art, shapes(W, H, [ellipse_pts(x, y, rx, ry, 18)]), nx, col=mix(d, INK, .4), amt=0.45)
    # little star print on the gold balloon
    art = GP(art, shapes(W, H, [star_pts(194, 276, 20, 9)], smooth=False), CREAM, "#fff8e8", seed=nx(), rough=0.6, pad=6)
    preview(art, "sk-balloons", tone=BG)
    save(art, f"{OUT}/balloons.webp", max_w=240, quality=82)
    clear()

if "popcorn" in PARTS:
    W, H = 300, 380
    nx = Seq(61400); rng = random.Random(614)
    art = blank(W, H)
    art = soft_ground(art, W, H, 150, 352, 86, 10, "#6a4a30", nx, 0.3)
    box_poly = [(64, 150), (236, 150), (208, 348), (92, 348)]
    box = shapes(W, H, [deform(box_poly, rng, 1, 0.004)], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # stripes converge with the taper
    t = (yy - 150) / 198
    half = 86 - 28 * t
    u = (xx - 150) / np.maximum(half, 1) * 3.5
    band = np.clip(np.minimum(u % 1.0, 0.5 - (u % 1.0)) * 24 + 0.5, 0, 1) * ((u % 1.0) < 0.52)
    art = body_paint(art, box, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(12, 0), blur=10, light_amt=0.3)
    art = GP(art, box * band, RED, RED2, seed=nx(), rough=0.8)
    art = tint(art, side_light(box, 16, 0, 12), REDD, 0.4, seed=nx())
    # label
    lab = ellipses(W, H, [(150, 254, 44, 30, 0)])
    art = body_paint(art, lab, GOLD, GOLD2, GOLDD, GOLDL, nx, blur=5, line=mix(GOLDD, INK, .3))
    art = GP(art, shapes(W, H, [star_pts(150, 254, 20, 9)], smooth=False), RED, RED2, seed=nx(), rough=0.4, pad=6)
    art = shade_line(art, box, nx, amt=0.6)
    # popcorn heap: clusters of puffy kernels
    kern = []
    for _ in range(46):
        a = rng.uniform(0, math.pi)
        r = rng.uniform(0, 1) ** 0.6
        x = 150 + math.cos(a) * 92 * r * rng.choice([-1, 1])
        y = 150 - math.sin(a) * 70 * r * 0.95 - 4
        kern.append((x, y, rng.uniform(13, 20)))
    kern.sort(key=lambda k: -k[1])
    for i, (x, y, r) in enumerate(kern):
        puff = [deform(ellipse_pts(x + math.cos(q) * r * 0.45, y + math.sin(q) * r * 0.45, r * 0.62, r * 0.55, 10, q), rng, 1, 0.05) for q in np.linspace(0, 6.28, 4, endpoint=False) + rng.uniform(0, 1)]
        m = shapes(W, H, puff)
        art = body_paint(art, m, "#fff6e2", "#fbecc8", "#e3c27e", "#ffffff", nx, ldir=(5, 5), blur=5, light_amt=0.25, dark_amt=0.6)
        if i % 3 == 0:
            art = GP(art, circles(W, H, [(x + rng.uniform(-3, 3), y + r * 0.2, r * 0.22)]), "#f0b84a", "#e8a33a", seed=nx(), rough=0.4, pad=6)
        if i % 8 == 0:
            clear()
    preview(art, "sk-popcorn", tone=BG)
    save(art, f"{OUT}/popcorn.webp", max_w=190, quality=82)
    clear()

if "bunting" in PARTS:
    W, H = 860, 180
    nx = Seq(61500); rng = random.Random(615)
    art = blank(W, H)
    rope = curve([(0, 22), (W * .5, 70), (W, 22)], 90)
    cols = [(RED, REDD), (CREAM, CREAMD), (TEAL, TEALD), (GOLD, GOLDD)]
    n = 13
    for i in range(n):
        t = (i + 0.5) / n
        idx = int(t * (len(rope) - 1))
        x, y = rope[idx]
        c, d = cols[i % len(cols)]
        hw, L = 26, 62
        poly = [(x - hw, y)] + [(x + hw * math.cos(a), y + L * 0.5 + L * 0.5 * math.sin(a)) for a in np.linspace(0, math.pi, 16)][::-1][::-1]
        poly = [(x - hw, y), (x + hw, y)] + [(x + hw * math.cos(a), y + L * 0.48 + L * 0.52 * math.sin(a)) for a in np.linspace(0, math.pi, 18)]
        m = shapes(W, H, [deform(poly, rng, 1, 0.006)], smooth=False)
        m = np.clip(gaussian_filter(m, 1.0) * 1.3, 0, 1)
        art = body_paint(art, m, c, mix(c, "#ffffff", 0.1), d, mix(c, "#ffffff", 0.45), nx, ldir=(-4, -6), blur=6, line=mix(d, INK, .4))
        dc = CREAM if c != CREAM else RED
        dots = circles(W, H, [(x + dx, y + dy, 3.6) for dx, dy in ((-10, 22), (10, 22), (0, 40), (-14, 42), (14, 42))]) * m
        art = GP(art, dots, dc, seed=nx(), rough=0.3, pad=5)
    art = crayon(art, strokes(W, H, [(rope, 3.2, None)]), "#6a5444", seed=nx(), amt=0.9, tooth=0.2)
    preview(art, "sk-bunting", tone=BG)
    save(art, f"{OUT}/bunting.webp", max_w=640, quality=80)
    clear()

if "star" in PARTS:
    W, H = 180, 180
    nx = Seq(61600); rng = random.Random(616)
    art = blank(W, H)
    m = shapes(W, H, [deform(star_pts(90, 94, 74, 32), rng, 1, 0.01)])
    art = body_paint(art, m, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(8, 8), blur=8, line=mix(GOLDD, INK, .3))
    art = OV(art, gaussian_filter(strokes(W, H, [(curve([(68, 72), (80, 60), (92, 54)], 10), 6, (0.2, 0.4))]), 1.2) * m, lambda mm: col_arr(mm, "#ffffff", mm * 0.6), pad=6)
    preview(art, "sk-star", tone=BG)
    save(art, f"{OUT}/star.webp", max_w=96, quality=84)
    clear()
