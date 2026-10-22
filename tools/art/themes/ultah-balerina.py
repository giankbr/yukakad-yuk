"""Ultah Balerina — kids ballet birthday in gouache + coloured pencil: a pink velvet stage curtain with a gold
tieback and tassel, a scalloped valance with fringe, satin pointe shoes with crossed ribbons, a layered tulle tutu,
an open music box with a turning dancer figurine (separate sprite), and a satin bow.
Run: python3 -I ultah-balerina.py [part ...]   parts: curtain valance shoes tutu musicbox dancer bow
Assets -> public/themes/art/ultah-balerina/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f5_lib import *  # noqa

OUT = outdir("ultah-balerina")
PARTS = sys.argv[1:] or ["curtain", "valance", "shoes", "tutu", "skirt", "musicbox", "dancer", "bow"]
BG = "#fdf0f2"
INK = "#5a2a3c"
V1, V2, VD, VL = "#d9617f", "#e3738f", "#8e2a4c", "#ffb3c6"
GOLD, GOLD2, GOLDD, GOLDL = "#e2b04f", "#efc468", "#9a6a22", "#fff0b8"
SAT, SAT2, SATD, SATL = "#f6bccb", "#f9cbd6", "#d9879d", "#fff3f6"


def gold(art, m, nx, ldir=(4, 5)):
    art = body_paint(art, m, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=ldir, blur=4, light_amt=0.55, dark_amt=0.6)
    return art


def tassel(art, W, H, x, y, s, nx):
    knot = circles(W, H, [(x, y, 11 * s)])
    head = shapes(W, H, [[(x - 9 * s, y + 6 * s), (x + 9 * s, y + 6 * s), (x + 12 * s, y + 26 * s), (x - 12 * s, y + 26 * s)]])
    fr = strokes(W, H, [([(x + dx * s, y + 24 * s), (x + dx * 1.15 * s, y + 70 * s)], 3.2 * s, (0.0, 0.3)) for dx in np.linspace(-13, 13, 9)])
    art = gold(art, fr, nx, (2, 4))
    art = gold(art, np.clip(knot + head, 0, 1), nx)
    art = crayon(art, strokes(W, H, [([(x - 11 * s, y + 24 * s), (x + 11 * s, y + 24 * s)], 2.4 * s, None)]), GOLDD, seed=nx(), amt=0.8)
    return art


if "curtain" in PARTS:
    W, H = 380, 1040
    nx = Seq(50100); rng = random.Random(501)
    art = blank(W, H)
    tie_y = 600

    def xr(y):
        if y <= tie_y:
            t = max(0.0, y) / tie_y
            return 300 - 225 * t ** 1.6
        t = (y - tie_y) / (H - tie_y)
        return 75 + 110 * t ** 0.8

    pts = [(-10, -10)] + [(xr(y), y) for y in np.linspace(-10, H + 10, 80)] + [(-10, H + 10)]
    m = shapes(W, H, [pts], smooth=False)
    m = np.clip(gaussian_filter(m, 0.8) * 1.3, 0, 1)
    art = GP(art, m, V1, V2, seed=nx(), rough=1.0, streak=0.5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xrv = np.vectorize(xr)(np.arange(H, dtype=np.float32))[:, None]
    phase = xx / np.maximum(xrv, 1) * 4.6 * math.tau + (fbm(W, H, nx(), 120, 2) - 0.5) * 1.6
    f = 0.5 + 0.5 * np.sin(phase)
    art = tint(art, np.clip((0.45 - f) * 2.2, 0, 1) * m, VD, 0.8, seed=nx())
    art = tint(art, np.clip((f - 0.72) * 3.0, 0, 1) * m, VL, 0.55, seed=nx())
    # deep shadow along the inner edge + velvet sheen near the gather
    edge = np.clip(xx / np.maximum(xrv, 1), 0, 1)
    art = tint(art, np.clip((edge - 0.8) * 5, 0, 1) * m, VD, 0.55, seed=nx())
    art = crayon(art, inner_edge(m, 2.2), mix(VD, INK, 0.3), seed=nx(), amt=0.75)
    # gold braid hem along the inner edge
    hem = strokes(W, H, [([(xr(y) - 6, y) for y in np.linspace(0, H, 90)], 9, None)]) * m
    art = gold(art, hem, nx, (2, 2))
    art = crayon(art, stripes(W, H, 0.9, 2, 7, seed=nx()) * hem, GOLDD, seed=nx(), amt=0.5)
    # tieback rope + tassel
    rope = strokes(W, H, [(curve([(-6, tie_y - 18), (40, tie_y + 6), (82, tie_y - 4)], 30), 15, None)])
    art = gold(art, rope, nx, (3, 5))
    art = crayon(art, stripes(W, H, 2.1, 2.2, 6, seed=nx()) * rope, GOLDD, seed=nx(), amt=0.6)
    art = tassel(art, W, H, 84, tie_y + 2, 1.2, nx)
    preview(art, "bl-curtain", tone=BG)
    save(art, f"{OUT}/curtain.webp", max_w=190, quality=82)
    clear()

if "valance" in PARTS:
    W, H = 820, 230
    nx = Seq(50200); rng = random.Random(502)
    art = blank(W, H)
    n = 4
    sw = W / n
    polys = [[(-10, -10), (W + 10, -10), (W + 10, 70)] + [p for k in range(n - 1, -1, -1) for p in arc_pts(sw * k + sw / 2, 60, sw / 2 + 2, 0, math.pi, 20, 1.0)] + [(-10, 70)]]
    m = shapes(W, H, polys, smooth=False)
    art = GP(art, m, V1, V2, seed=nx(), rough=1.0, streak=0.5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for k in range(n):
        cx = sw * k + sw / 2
        d = np.sqrt((xx - cx) ** 2 + ((yy + 30) * 1.0) ** 2)
        f = 0.5 + 0.5 * np.sin(d / 13.0)
        sel = (np.abs(xx - cx) < sw / 2) * m
        art = tint(art, np.clip((0.4 - f) * 2.2, 0, 1) * sel, VD, 0.6, seed=nx())
        art = tint(art, np.clip((f - 0.78) * 3, 0, 1) * sel, VL, 0.4, seed=nx())
    art = crayon(art, inner_edge(m, 2.2), mix(VD, INK, 0.3), seed=nx(), amt=0.75)
    fringe_line = [p for k in range(n) for p in arc_pts(sw * k + sw / 2, 60, sw / 2 - 4, math.pi, 0, 20, 1.0)]
    band = strokes(W, H, [(fringe_line, 10, None)])
    fr = strokes(W, H, [([(x, y + 4), (x, y + 22)], 3.0, (0, 0.3)) for x, y in fringe_line[::1]])
    art = gold(art, fr, nx, (1, 3))
    art = gold(art, band, nx, (2, 3))
    for k in range(n + 1):
        art = tassel(art, W, H, sw * k if 0 < k < n else (14 if k == 0 else W - 14), 60, 0.9, nx)
    preview(art, "bl-valance", tone=BG)
    save(art, f"{OUT}/valance.webp", max_w=780, quality=80)
    clear()

if "shoes" in PARTS:
    W, H = 460, 460
    nx = Seq(50300); rng = random.Random(503)
    art = blank(W, H)

    def shoe(art, ox, oy, ang, flip):
        """Side view, hanging toe-down: blunt toe box at the bottom, heel + drawstring opening at the top."""
        ca, sa = math.cos(ang), math.sin(ang)
        P = lambda x, y: (ox + (x * flip) * ca - y * sa, oy + (x * flip) * sa + y * ca)
        outline = [P(*q) for q in [(-26, -120), (10, -128), (34, -112), (38, -40), (34, 40), (30, 110), (16, 140), (-8, 144), (-26, 128), (-34, 60), (-38, -20), (-36, -90)]]
        m = shapes(W, H, [outline])
        art = body_paint(art, m, SAT, SAT2, SATD, SATL, nx, ldir=(9 * flip, 4), blur=12, light_amt=0.6, dark_amt=0.55)
        art = sheen(art, m, lambda xx, yy: (xx - ox) * ca * flip + (yy - oy) * sa * 0.3, col_hi="#ffffff", amt=0.5, seed=nx(), freq=0.1)
        opening = shapes(W, H, [[P(*q) for q in [(-30, -112), (6, -122), (30, -106), (22, -64), (-2, -40), (-24, -70)]]])
        art = GP(art, opening * m, "#e98ea6", "#e07f99", seed=nx(), rough=0.5)
        art = tint(art, side_light(opening, 0, 10, 8) * m, "#a84e6a", 0.6, seed=nx())
        art = crayon(art, strokes(W, H, [([P(-30, -110), P(6, -120), P(30, -104)], 3, None)]), "#c86f88", seed=nx(), amt=0.8)
        # toe platform + pleats at the toe
        plat = ellipses(W, H, [(P(4, 136)[0], P(4, 136)[1], 15, 6, math.degrees(ang))]) * m
        art = tint(art, plat, SATD, 0.55, seed=nx())
        pl = strokes(W, H, [([P(x, 104), P(x * 0.6, 132)], 1.6, (0.2, 0.2)) for x in (-18, -8, 2, 12, 22)]) * m
        art = crayon(art, pl, "#d98aa0", seed=nx(), amt=0.6)
        art = crayon(art, inner_edge(m, 2.2), mix(SATD, INK, 0.3), seed=nx(), amt=0.8)
        return art, P(-30, -100), P(30, -96)

    art, l1, r1 = shoe(art, 160, 290, 0.16, 1)
    art, l2, r2 = shoe(art, 300, 300, -0.12, -1)
    knot = (230, 46)
    rib_paths = [
        [r1, (190, 150), (214, 80), knot], [l1, (120, 150), (150, 80), knot],
        [l2, (264, 170), (246, 90), knot], [r2, (350, 170), (300, 80), knot],
        [knot, (196, 70), (176, 110), (182, 140)], [knot, (262, 72), (290, 104), (286, 128)],
    ]
    for k, pth in enumerate(rib_paths):
        rm = strokes(W, H, [(curve(pth, 70), 10 if k < 4 else 12, (0.0, 0.0) if k < 4 else (0.0, 0.15))])
        art = body_paint(art, rm, "#f3a9bd", "#f6b8c8", "#cf7a93", "#ffeef3", nx, ldir=(3, 3), blur=3, light_amt=0.5, dark_amt=0.45)
        art = crayon(art, inner_edge(rm, 1.6), "#c06784", seed=nx(), amt=0.65)
    loops = shapes(W, H, [[knot, (190, 20), (176, 44), (200, 60)], [knot, (270, 20), (284, 44), (260, 60)]])
    art = body_paint(art, loops, "#f3a9bd", "#f6b8c8", "#cf7a93", "#ffeef3", nx, ldir=(3, 3), blur=4)
    art = crayon(art, inner_edge(loops, 1.8), "#c06784", seed=nx(), amt=0.7)
    art = body_paint(art, circles(W, H, [(knot[0], knot[1], 10)]), "#f08fab", "#f3a0b8", "#c06784", "#ffeef3", nx, ldir=(2, 2), blur=3)
    preview(art, "bl-shoes", tone=BG)
    save(art, f"{OUT}/shoes.webp", max_w=230, quality=82)
    clear()

if "tutu" in PARTS:
    W, H = 460, 340
    nx = Seq(50400); rng = random.Random(504)
    art = blank(W, H)
    # tulle layers: back (deeper), middle, front with scalloped hem
    for k, (ry, col, col2, a) in enumerate(((92, "#f08aa8", "#f3a0b8", 0.75), (78, "#f6a9bf", "#f8bccc", 0.7), (62, "#fbc6d3", "#fdd6e0", 0.75))):
        pts = []
        for i in range(48):
            t = i / 48 * math.tau
            r = 1 + 0.07 * math.sin(t * 14 + k)
            pts.append((230 + math.cos(t) * (210 - k * 18) * r, 210 + math.sin(t) * ry * r))
        m = shapes(W, H, [pts])
        m = m * (np.arange(H)[:, None] > 150 - k * 6)
        art = tulle(art, m, col, col2, nx, alpha=a)
        pleats = strokes(W, H, [([(230 + math.cos(t) * 40, 210 + math.sin(t) * 14), (230 + math.cos(t) * (200 - k * 18), 210 + math.sin(t) * ry)], 1.6, (0.1, 0.3)) for t in np.linspace(0, math.pi, 22)]) * m
        art = OV(art, pleats, lambda mm: col_arr(mm, "#ffffff", mm * 0.35), pad=4)
    # bodice
    bod = shapes(W, H, [[(186, 66), (208, 50), (230, 62), (252, 50), (274, 66), (266, 130), (256, 204), (204, 204), (194, 130)]])
    art = body_paint(art, bod, "#f39ab4", "#f6aec2", "#c45f80", "#ffe0e9", nx, ldir=(8, 6), blur=10)
    art = sheen(art, bod, lambda xx, yy: xx * 0.8 + yy * 0.2, amt=0.4, seed=nx(), freq=0.12)
    art = crayon(art, inner_edge(bod, 2.2), "#b35576", seed=nx(), amt=0.75)
    art = crayon(art, strokes(W, H, [([(230, 62), (230, 200)], 2, None)]), "#c86f88", seed=nx(), amt=0.4)
    # straps + sequins
    art = GP(art, strokes(W, H, [([(196, 54), (190, 12)], 7, None), ([(264, 54), (270, 12)], 7, None)]), "#f39ab4", seed=nx(), rough=0.4)
    for i in range(30):
        x = rng.uniform(186, 274); y = rng.uniform(70, 196)
        art = spark(art, x, y, rng.uniform(3, 6), col="#fff4f8", amt=0.85)
    for i in range(16):
        t = rng.uniform(0, math.pi); r = rng.uniform(0.4, 0.95)
        art = spark(art, 230 + math.cos(t) * 190 * r, 210 + math.sin(t) * 80 * r, rng.uniform(3, 6), col="#ffffff", amt=0.8)
    preview(art, "bl-tutu", tone=BG)
    save(art, f"{OUT}/tutu.webp", max_w=230, quality=82)
    clear()

if "skirt" in PARTS:
    W, H = 460, 340
    nx = Seq(50450); rng = random.Random(545)
    art = blank(W, H)
    # tulle layers: back (deeper), middle, front with scalloped hem
    for k, (ry, col, col2, a) in enumerate(((92, "#f08aa8", "#f3a0b8", 0.75), (78, "#f6a9bf", "#f8bccc", 0.7), (62, "#fbc6d3", "#fdd6e0", 0.75))):
        pts = []
        for i in range(48):
            t = i / 48 * math.tau
            r = 1 + 0.07 * math.sin(t * 14 + k)
            pts.append((230 + math.cos(t) * (210 - k * 18) * r, 210 + math.sin(t) * ry * r))
        m = shapes(W, H, [pts])
        m = m * (np.arange(H)[:, None] > 150 - k * 6)
        art = tulle(art, m, col, col2, nx, alpha=a)
        pleats = strokes(W, H, [([(230 + math.cos(t) * 40, 210 + math.sin(t) * 14), (230 + math.cos(t) * (200 - k * 18), 210 + math.sin(t) * ry)], 1.6, (0.1, 0.3)) for t in np.linspace(0, math.pi, 22)]) * m
        art = OV(art, pleats, lambda mm: col_arr(mm, "#ffffff", mm * 0.35), pad=4)
    for i in range(14):
        t = rng.uniform(0, math.pi); r = rng.uniform(0.4, 0.95)
        art = spark(art, 230 + math.cos(t) * 190 * r, 210 + math.sin(t) * 80 * r, rng.uniform(3, 6), col="#ffffff", amt=0.8)
    preview(art, "bl-skirt", tone=BG)
    save(art, f"{OUT}/skirt.webp", max_w=230, quality=82)
    clear()

if "musicbox" in PARTS:
    W, H = 520, 520
    nx = Seq(50500); rng = random.Random(505)
    art = blank(W, H)
    art = soft_ground(art, W, H, 260, 482, 220, 22, "#b06a80", nx, 0.3)
    # open lid with a mirror (behind)
    lid = shapes(W, H, [[(70, 290), (450, 290), (420, 70), (100, 70)]], smooth=False)
    art = body_paint(art, lid, "#f4a7bd", "#f7b7c9", "#c6607f", "#ffe3ec", nx, ldir=(6, 8), blur=10)
    mirror = shapes(W, H, [deform(ellipse_pts(260, 176, 120, 82, 30), rng, 1, 0.003)])
    art = gold(art, np.clip(gaussian_filter(mirror, 4) * 2 - mirror * 0.0, 0, 1) - mirror * 0.0, nx)
    inner = shapes(W, H, [ellipse_pts(260, 176, 108, 72, 30)])
    art = GP(art, inner, "#e8eef4", "#d6e0ea", seed=nx(), rough=0.4)
    art = tint(art, side_light(inner, -10, 10, 18), "#ffffff", 0.7, seed=nx())
    art = OV(art, strokes(W, H, [([(190, 150), (226, 116)], 6, (0.2, 0.2)), ([(206, 170), (250, 128)], 4, (0.2, 0.2))]), lambda mm: col_arr(mm, "#ffffff", mm * 0.8), pad=4)
    # box body
    box = shapes(W, H, [[(60, 290), (460, 290), (460, 470), (60, 470)]], smooth=False)
    art = body_paint(art, box, "#f6b3c5", "#f8c2d0", "#c96884", "#fff0f4", nx, ldir=(10, 10), blur=14)
    front = shapes(W, H, [[(60, 330), (460, 330), (460, 470), (60, 470)]], smooth=False)
    art = tint(art, front, "#e690a8", 0.35, seed=nx())
    trim = strokes(W, H, [([(60, 330), (460, 330)], 9, None), ([(60, 292), (460, 292)], 7, None), ([(60, 466), (460, 466)], 8, None)])
    art = gold(art, trim, nx, (1, 3))
    # gold scroll + heart plaque on the front
    plaque = shapes(W, H, [deform(ellipse_pts(260, 400, 54, 34, 20), rng, 1, 0.003)])
    art = gold(art, plaque, nx)
    art = GP(art, shapes(W, H, [ellipse_pts(260, 400, 44, 25, 20)]), "#fde7ee", seed=nx(), rough=0.4)
    heart = shapes(W, H, [[(260, 418), (240, 398), (244, 386), (254, 386), (260, 394), (266, 386), (276, 386), (280, 398)]])
    art = GP(art, heart, "#d9617f", seed=nx(), rough=0.5)
    for x in (100, 420):
        art = crayon(art, strokes(W, H, [(spiral_pts(x, 400, 26, 2.2, 40) if False else arc_pts(x, 400, 22, -2.8, 2.2, 20), 4, (0.1, 0.4))]), GOLDD, seed=nx(), amt=0.8)
    # feet + winding key
    feet = circles(W, H, [(86, 476, 14), (434, 476, 14)])
    art = gold(art, feet, nx)
    key = np.clip(strokes(W, H, [([(460, 380), (490, 380)], 7, None)]) + circles(W, H, [(500, 366, 13), (500, 394, 13)]), 0, 1)
    art = gold(art, key, nx)
    art = crayon(art, inner_edge(np.clip(box + lid, 0, 1), 2.2), "#a34d6c", seed=nx(), amt=0.7)
    # little turntable disc for the dancer
    disc = ellipses(W, H, [(260, 292, 60, 12, 0)])
    art = gold(art, disc, nx, (0, 3))
    preview(art, "bl-musicbox", tone=BG)
    save_full(art, f"{OUT}/musicbox.webp", size=(260, 260), quality=82)
    clear()

if "dancer" in PARTS:
    # stylised figurine (simple, faceless porcelain doll), turned by CSS
    W, H = 240, 400
    nx = Seq(50600); rng = random.Random(506)
    art = blank(W, H)
    SK, SK2, SKD, SKL = "#f2d2bd", "#f6dccb", "#c99a82", "#fff2e8"
    legs = strokes(W, H, [([(116, 206), (114, 380)], 14, (0.0, 0.45)), (curve([(128, 206), (162, 270), (176, 300), (150, 318)], 30), 13, (0.0, 0.3))])
    art = body_paint(art, legs, "#f8c9d6", "#fbd6e0", "#d58aa1", "#ffffff", nx, ldir=(4, 2), blur=4)
    arms = strokes(W, H, [(curve([(104, 130), (80, 90), (96, 44), (120, 34)], 30), 9, (0.05, 0.2)), (curve([(140, 130), (164, 90), (148, 44), (124, 34)], 30), 9, (0.05, 0.2))])
    art = body_paint(art, arms, SK, SK2, SKD, SKL, nx, ldir=(3, 2), blur=3)
    torso = shapes(W, H, [[(104, 120), (122, 110), (140, 120), (138, 200), (106, 200)]])
    art = body_paint(art, torso, "#f39ab4", "#f6aec2", "#c45f80", "#ffe0e9", nx, ldir=(5, 4), blur=6)
    neck = strokes(W, H, [([(122, 112), (122, 98)], 9, None)])
    head = circles(W, H, [(122, 82, 20)])
    bun = circles(W, H, [(122, 56, 11)])
    art = body_paint(art, np.clip(neck + head, 0, 1), SK, SK2, SKD, SKL, nx, ldir=(5, 4), blur=6)
    hair = np.clip(circles(W, H, [(122, 76, 21)]) * (np.arange(H)[:, None] < 78) + bun, 0, 1)
    art = body_paint(art, hair, "#7a4a36", "#8a5a42", "#4a2a1e", "#b07a5a", nx, ldir=(4, 4), blur=4)
    art = cheek(art, W, H, 116, 90, 5, nx, amt=0.4)
    # tutu disc
    tm = shapes(W, H, [[(122 + math.cos(t) * 74 * (1 + 0.06 * math.sin(t * 12)), 206 + math.sin(t) * 26 * (1 + 0.06 * math.sin(t * 12))) for t in np.linspace(0, math.tau, 60)]])
    art = tulle(art, tm, "#f6a9bf", "#fbc6d3", nx, alpha=0.85)
    art = tulle(art, shapes(W, H, [ellipse_pts(122, 200, 60, 16, 30)]), "#fde0e8", "#ffffff", nx, alpha=0.6, mesh=False)
    art = crayon(art, inner_edge(np.clip(torso + head + arms + legs + tm, 0, 1), 1.6), "#a34d6c", seed=nx(), amt=0.5)
    preview(art, "bl-dancer", tone=BG)
    save(art, f"{OUT}/dancer.webp", max_w=120, quality=84)
    clear()

if "bow" in PARTS:
    W, H = 260, 180
    nx = Seq(50700); rng = random.Random(507)
    art = blank(W, H)
    tails = shapes(W, H, [[(122, 86), (96, 150), (84, 170), (104, 162), (118, 172), (130, 96)], [(138, 86), (160, 150), (176, 170), (156, 162), (142, 172), (130, 96)]])
    loops = shapes(W, H, [[(130, 84), (90, 40), (40, 46), (34, 96), (70, 120), (128, 96)], [(130, 84), (170, 40), (220, 46), (226, 96), (190, 120), (132, 96)]])
    knot = shapes(W, H, [deform(ellipse_pts(130, 88, 20, 18, 14), rng, 1, 0.01)])
    for m in (tails, loops, knot):
        art = body_paint(art, m, V1, V2, VD, VL, nx, ldir=(5, 6), blur=7, light_amt=0.6)
        art = crayon(art, inner_edge(m, 2), mix(VD, INK, 0.3), seed=nx(), amt=0.75)
    art = crayon(art, strokes(W, H, [(curve([(60, 60), (80, 80), (118, 90)], 12), 2, None), (curve([(200, 60), (180, 80), (142, 90)], 12), 2, None)]), VD, seed=nx(), amt=0.6)
    preview(art, "bl-bow", tone=BG)
    save(art, f"{OUT}/bow.webp", max_w=130, quality=84)
    clear()
