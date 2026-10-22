"""Peresmian Usaha — grand opening of a small shop (gouache): a storefront at dusk with a blank wooden sign (the business
name is typeset over it in HTML), teal-and-cream scalloped awning, warm window with shelves and pendant lamps, glass
door, potted plants; a red satin ribbon with a big bow, golden scissors, two Indonesian papan bunga (flower boards with
a blank white panel for HTML text, on bamboo legs) and a confetti scatter.
Run: python3 -I peresmian-usaha.py [part ...]   parts: shop ribbon scissors board confetti
Assets -> public/themes/art/peresmian-usaha/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d6_lib import *

OUT = outdir("peresmian-usaha")
PARTS = sys.argv[1:] or ["shop", "ribbon", "scissors", "board", "confetti"]
INK = "#3a2620"
RED, RED2, REDD, REDL = "#c8282e", "#d93a3a", "#8a1820", "#f06a64"
GOLD, GOLD2, GOLDD, GOLDL = "#d4a640", "#e2b955", "#9a7424", "#fbe6a6"
TEAL, TEAL2, TEALD = "#2f6f68", "#3a7d75", "#1d4a45"
CREAM, CREAM2, CREAMD = "#fbf4e8", "#f3e8d4", "#d8c3a0"
PLASTER, PLASTER2, PLASTERD = "#efdcc0", "#e8d2b2", "#c2a27a"
BRICK, BRICKD = "#b5654a", "#8a4634"
WOODC, WOODC2, WOODCD = "#7a4f33", "#8a5c3c", "#4e3020"
LEAF, LEAF2, LEAFD = "#5f8a4a", "#6f9a56", "#3d6334"
WARM = "#f6c675"
BG = "#fbf4e8"


if "shop" in PARTS:
    W, H = 760, 760
    nx = Seq(91100); rng = random.Random(911)
    art = blank(W, H)
    art = soft_ground(art, W, H, 380, 722, 360, 20, "#6a4a36", nx, 0.35)
    # sidewalk
    walk = shapes(W, H, [[(10, 690), (750, 690), (760, 730), (0, 730)]], smooth=False)
    art = GP(art, walk, "#d8c8ae", "#cdbb9e", seed=nx(), rough=0.8)
    art = tint(art, strokes(W, H, [([(x, 692), (x - 8, 728)], 2, None) for x in range(60, 760, 90)]) * walk, "#a8957a", 0.5, seed=nx())
    # facade
    fac = shapes(W, H, [[(60, 250), (700, 250), (700, 692), (60, 692)]], smooth=False)
    art = body_paint(art, fac, PLASTER, PLASTER2, PLASTERD, "#fff1da", nx, ldir=(18, 0), blur=22, light_amt=0.3)
    cornice = shapes(W, H, [[(46, 236), (714, 236), (706, 256), (54, 256)]], smooth=False)
    art = body_paint(art, cornice, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(0, 6), blur=4)
    parapet = shapes(W, H, [[(70, 150), (690, 150), (690, 238), (70, 238)]], smooth=False)
    art = body_paint(art, parapet, PLASTER, PLASTER2, PLASTERD, "#fff1da", nx, ldir=(14, 6), blur=12, light_amt=0.3)
    # brick plinth
    plinth = shapes(W, H, [[(60, 632), (700, 632), (700, 692), (60, 692)]], smooth=False)
    art = GP(art, plinth, BRICK, "#bf6e52", seed=nx(), rough=0.8)
    bl = []
    for j, y in enumerate(range(632, 692, 15)):
        bl.append(([(60, y), (700, y)], 1.6, None))
        for x in range(60 + (j % 2) * 20, 700, 40):
            bl.append(([(x, y), (x, y + 15)], 1.6, None))
    art = tint(art, strokes(W, H, bl) * plinth, BRICKD, 0.6, seed=nx())
    # signboard (blank, HTML text goes on it): x 170..590, y 162..228
    sign = shapes(W, H, [[(170, 162), (590, 162), (590, 228), (170, 228)]], smooth=False)
    art = soft_ground(art, W, H, 384, 232, 210, 8, "#7a5a40", nx, 0.3)
    art = wood(art, sign, WOODC, WOODC2, WOODCD, nx, angle=0.0, ring=9, grain_amt=0.35)
    art = GP(art, np.clip(inner_edge(sign, 6) - inner_edge(sign, 3) * 0, 0, 1), GOLD, GOLD2, seed=nx(), rough=0.4, pad=6)
    art = tint(art, side_light(sign, 0, 8, 6), "#2a180f", 0.4, seed=nx())
    # small lamps over the sign
    for lx in (250, 510):
        art = GP(art, strokes(W, H, [([(lx, 150), (lx, 138), (lx + 14, 138)], 3, None)]), "#2c2420", seed=nx(), rough=0.2, pad=6)
        cone = shapes(W, H, [[(lx + 6, 136), (lx + 24, 136), (lx + 30, 150), (lx, 150)]], smooth=False)
        art = GP(art, cone, "#2c2420", "#3a302a", seed=nx(), rough=0.3, pad=6)
        art = OV(art, gaussian_filter(shapes(W, H, [[(lx + 2, 150), (lx + 28, 150), (lx + 60, 200), (lx - 30, 200)]], smooth=False), 6) * 0.7, lambda m: col_arr(m, "#ffe8b0", m * 0.35), pad=10)
    # window (left) with warm interior
    win = shapes(W, H, [[(96, 352), (380, 352), (380, 610), (96, 610)]], smooth=False)
    art = GP(art, win, "#f2c47a", "#e8a85a", seed=nx(), rough=0.4)
    art = OV(art, gaussian_filter(ellipses(W, H, [(238, 470, 130, 110, 0)]), 30) * win, lambda m: col_arr(m, "#fff0c8", np.clip(m * 1.2, 0, 0.85)), pad=4)
    shelves = strokes(W, H, [([(110, y), (366, y)], 5, None) for y in (452, 512)])
    art = GP(art, shelves * win, "#8a5c3c", "#7a4f33", seed=nx(), rough=0.3)
    jars = []
    for y in (452, 512):
        x = 118
        while x < 350:
            w_ = rng.uniform(14, 24); h_ = rng.uniform(20, 34)
            jars.append(([(x, y - 3), (x + w_, y - 3), (x + w_, y - 3 - h_), (x, y - 3 - h_)], rng.choice(["#b5654a", "#5f8a4a", "#d4a640", "#7a4f33", "#efdcc0", "#2f6f68"])))
            x += w_ + rng.uniform(6, 14)
    for col in set(c for _, c in jars):
        m = shapes(W, H, [p for p, c in jars if c == col]) * win
        art = GP(art, m, col, mix(col, "#ffffff", 0.15), seed=nx(), rough=0.4, pad=6)
    counter = shapes(W, H, [[(96, 560), (380, 560), (380, 610), (96, 610)]], smooth=False)
    art = GP(art, counter, "#6a4430", "#7a4f33", seed=nx(), rough=0.4)
    for lx in (170, 300):
        art = crayon(art, strokes(W, H, [([(lx, 352), (lx, 390)], 1.6, None)]), "#3a2620", seed=nx(), amt=0.7)
        sh = shapes(W, H, [[(lx - 16, 404), (lx + 16, 404), (lx + 6, 388), (lx - 6, 388)]], smooth=False)
        art = GP(art, sh, "#2f2a26", seed=nx(), rough=0.2, pad=6)
        art = OV(art, circles(W, H, [(lx, 408, 6)]), lambda m: glow(m, "#fff2c8", 14, 0.7), pad=40)
    # window frame + glazing bars + glass sheen
    wf = np.clip(strokes(W, H, [([(96, 352), (380, 352), (380, 610), (96, 610), (96, 352)], 10, None), ([(238, 352), (238, 560)], 6, None)]), 0, 1)
    art = GP(art, wf, TEAL, TEAL2, seed=nx(), rough=0.4)
    sheen_ = strokes(W, H, [([(120, 380), (190, 360)], 14, (0.3, 0.3)), ([(140, 420), (220, 392)], 6, (0.3, 0.3))]) * win
    art = OV(art, gaussian_filter(sheen_, 2), lambda m: col_arr(m, "#ffffff", m * 0.35), pad=4)
    sill = shapes(W, H, [[(86, 610), (390, 610), (384, 624), (92, 624)]], smooth=False)
    art = body_paint(art, sill, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(0, 4), blur=3)
    # door (right)
    door = shapes(W, H, [[(440, 352), (600, 352), (600, 692), (440, 692)]], smooth=False)
    art = GP(art, door, TEAL, TEAL2, seed=nx(), rough=0.4)
    glass = shapes(W, H, [[(458, 370), (582, 370), (582, 560), (458, 560)]], smooth=False)
    art = GP(art, glass, "#f2c47a", "#e8a85a", seed=nx(), rough=0.4)
    art = OV(art, gaussian_filter(ellipses(W, H, [(520, 470, 60, 90, 0)]), 20) * glass, lambda m: col_arr(m, "#fff0c8", np.clip(m * 1.2, 0, 0.8)), pad=4)
    art = OV(art, gaussian_filter(strokes(W, H, [([(470, 400), (520, 380)], 10, (0.3, 0.3))]) * glass, 2), lambda m: col_arr(m, "#ffffff", m * 0.35), pad=4)
    panel = shapes(W, H, [[(464, 584), (576, 584), (576, 672), (464, 672)]], smooth=False)
    art = tint(art, inner_edge(panel, 3), TEALD, 0.7, seed=nx())
    art = body_paint(art, circles(W, H, [(586, 560, 7)]), GOLD, GOLD2, GOLDD, GOLDL, nx, blur=2)
    # "BUKA" hanging tag left blank (small cream plate)
    tag = shapes(W, H, [[(486, 430), (554, 430), (554, 470), (486, 470)]], smooth=False)
    art = crayon(art, strokes(W, H, [([(492, 430), (520, 404), (548, 430)], 1.6, None)]), "#3a2620", seed=nx(), amt=0.7)
    art = body_paint(art, tag, CREAM, CREAM2, CREAMD, "#ffffff", nx, blur=3, line="#8a6a4a")
    art = GP(art, strokes(W, H, [([(498, 450), (542, 450)], 5, None)]), RED, seed=nx(), rough=0.3, pad=6)
    art = tint(art, side_light(door, 10, 0, 10), TEALD, 0.5, seed=nx())
    # awning across the top of window + door: teal/cream stripes, scalloped valance
    awn_poly = [(76, 268), (684, 268), (712, 340), (48, 340)]
    awn = shapes(W, H, [awn_poly], smooth=False)
    sc = circles(W, H, [(48 + (i + 0.5) * (664 / 14), 340, 664 / 28) for i in range(14)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    awn = np.clip(awn + sc * (yy >= 338), 0, 1)
    t = np.clip((yy - 268) / 72, 0, 1)
    xc = 380 + (xx - 380) / (1 + 0.088 * t)
    u = (xc - 76) / (608 / 14)
    band = np.clip(np.minimum(u % 1.0, 0.5 - (u % 1.0)) * 30 + 0.5, 0, 1) * ((u % 1.0) < 0.52)
    art = soft_ground(art, W, H, 380, 368, 330, 12, "#5a3a28", nx, 0.35)
    art = body_paint(art, awn, CREAM, CREAM2, CREAMD, "#ffffff", nx, ldir=(0, 10), blur=10, light_amt=0.3)
    art = GP(art, awn * band, TEAL, TEAL2, seed=nx(), rough=0.6, streak=0.7)
    art = tint(art, side_light(awn, 0, 14, 12), "#1a3a36", 0.4, seed=nx())
    art = crayon(art, inner_edge(awn, 2.0), "#2a4a44", seed=nx(), amt=0.55)
    # potted plants each side
    for px_, flip in ((70, 1), (690, -1)):
        pot = shapes(W, H, [[(px_ - 30, 640), (px_ + 30, 640), (px_ + 22, 700), (px_ - 22, 700)]], smooth=False)
        leaves = []
        for k in range(9):
            a = -math.pi / 2 + (k - 4) * 0.32 + rng.uniform(-.08, .08)
            L = rng.uniform(60, 100)
            leaves.append(petal_pts(px_ + math.cos(a) * 8, 640, L, L * 0.2, a, n=12))
        lm = shapes(W, H, leaves)
        art = body_paint(art, lm, LEAF, LEAF2, LEAFD, "#9cc07a", nx, ldir=(8 * flip, 0), blur=6, line=mix(LEAFD, INK, .3))
        art = body_paint(art, pot, "#c8744e", "#d2825a", "#8e4a30", "#e8a07a", nx, ldir=(6 * flip, 0), blur=5, line="#7a3c26")
    art = crayon(art, inner_edge(np.clip(fac + parapet, 0, 1), 2.0), "#a8865e", seed=nx(), amt=0.45)
    preview(art, "pu-shop", tone=BG)
    save_full(art, f"{OUT}/shop.webp", size=(520, 520), quality=80)
    clear()

if "ribbon" in PARTS:
    W, H = 960, 280
    nx = Seq(91200); rng = random.Random(912)
    art = blank(W, H)
    cx, cy = 480, 120
    bandL = shapes(W, H, [curve([(0, 108), (240, 112), (440, 116)], 20) + curve([(440, 140), (240, 138), (0, 136)], 20)], smooth=False)
    bandR = shapes(W, H, [curve([(520, 116), (720, 112), (W, 104)], 20) + curve([(W, 132), (720, 138), (520, 140)], 20)], smooth=False)
    tails = shapes(W, H, [[(470, 136), (420, 250), (440, 244), (452, 262), (492, 140)], [(490, 136), (548, 246), (530, 240), (520, 262), (470, 140)]])
    loopL = shapes(W, H, [curve([(476, 124), (420, 60), (360, 64), (350, 120), (380, 176), (476, 132)], 40)])
    loopR = shapes(W, H, [curve([(484, 124), (540, 60), (600, 64), (610, 120), (580, 176), (484, 132)], 40)])
    holeL = shapes(W, H, [curve([(460, 124), (412, 84), (380, 92), (378, 124), (400, 150), (460, 130)], 30)])
    holeR = shapes(W, H, [curve([(500, 124), (548, 84), (580, 92), (582, 124), (560, 150), (500, 130)], 30)])
    for m, ldir in ((bandL, (0, 8)), (bandR, (0, 8)), (tails, (4, 6))):
        art = body_paint(art, m, RED, RED2, REDD, REDL, nx, ldir=ldir, blur=6, light_amt=0.35)
    art = sheen(art, np.clip(bandL + bandR, 0, 1), lambda x, y: x / 60.0, col_hi="#ff9a8e", col_lo=REDD, amt=0.45, seed=nx())
    for m, hole in ((loopL, holeL), (loopR, holeR)):
        art = body_paint(art, m, RED, RED2, REDD, REDL, nx, ldir=(0, 10), blur=10, light_amt=0.4)
        art = tint(art, gaussian_filter(hole, 3) * m, "#6a1018", 0.55, seed=nx())
    art = sheen(art, np.clip(loopL + loopR, 0, 1), lambda x, y: np.hypot(x - cx, y - cy) / 14.0, col_hi="#ff9a8e", amt=0.4, seed=nx())
    knot = shapes(W, H, [deform(ellipse_pts(cx, 130, 26, 30, 12, 0), rng, 1, 0.03)])
    art = body_paint(art, knot, RED, RED2, REDD, REDL, nx, ldir=(4, 6), blur=6)
    art = tint(art, strokes(W, H, [([(cx - 12, 108), (cx - 8, 152)], 3, (0.2, 0.2)), ([(cx + 10, 110), (cx + 8, 150)], 3, (0.2, 0.2))]), REDD, 0.6, seed=nx())
    art = crayon(art, inner_edge(np.clip(bandL + bandR + loopL + loopR + tails + knot, 0, 1), 1.8), "#6a1018", seed=nx(), amt=0.45)
    preview(art, "pu-ribbon", tone=BG)
    save(art, f"{OUT}/ribbon.webp", max_w=640, quality=82)
    clear()

if "scissors" in PARTS:
    W, H = 340, 340
    nx = Seq(91300); rng = random.Random(913)
    art = blank(W, H)
    piv = (170, 178)

    def blade(a, L=150, w=20):
        ca, sa = math.cos(a), math.sin(a)
        px, py = -sa, ca
        return [(piv[0] - ca * 10 + px * w * 0.5, piv[1] - sa * 10 + py * w * 0.5), (piv[0] + ca * L * 0.6 + px * w * 0.55, piv[1] + sa * L * 0.6 + py * w * 0.55),
                (piv[0] + ca * L, piv[1] + sa * L), (piv[0] + ca * L * 0.6 - px * w * 0.25, piv[1] + sa * L * 0.6 - py * w * 0.25), (piv[0] - ca * 10 - px * w * 0.4, piv[1] - sa * 10 - py * w * 0.4)]

    def handle(a, r=34, d=70):
        hx, hy = piv[0] - math.cos(a) * d, piv[1] - math.sin(a) * d
        ring = np.clip(circles(W, H, [(hx, hy, r)]) - circles(W, H, [(hx, hy, r - 13)]), 0, 1)
        neck = strokes(W, H, [([(piv[0], piv[1]), (hx + math.cos(a) * (r - 6), hy + math.sin(a) * (r - 6))], 15, None)])
        return np.clip(ring + neck, 0, 1)
    a1, a2 = -0.95, -0.35
    b1 = shapes(W, H, [blade(a1)], smooth=False)
    b2 = shapes(W, H, [blade(a2)], smooth=False)
    art = soft_ground(art, W, H, 190, 300, 110, 10, "#6a4a36", nx, 0.25)
    for b in (b2, b1):
        art = body_paint(art, b, "#ecd59a", "#f6e6b8", GOLDD, "#fff8dc", nx, ldir=(4, 6), blur=4, light_amt=0.5)
        art = crayon(art, inner_edge(b, 1.4), "#8a6a24", seed=nx(), amt=0.6)
    h1, h2 = handle(a1 - 0.5, r=32, d=74), handle(a2 + 0.5, r=32, d=74)
    for h in (h2, h1):
        art = body_paint(art, h, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(5, 6), blur=5, line=mix(GOLDD, INK, .3))
        art = sheen(art, h, lambda x, y: (x + y) / 12.0, col_hi="#fff4c8", amt=0.45, seed=nx())
    art = body_paint(art, circles(W, H, [(piv[0], piv[1], 9)]), GOLDD, GOLD, "#6a4f1c", GOLDL, nx, blur=3)
    preview(art, "pu-scissors", tone=BG)
    save(art, f"{OUT}/scissors.webp", max_w=180, quality=84)
    clear()

if "board" in PARTS:
    for name, pal, sd in (("board-a", [("#d83a3a", "#a82028"), ("#f2c230", "#c8941c"), ("#ffffff", "#d8d0c8")], 0), ("board-b", [("#ef8fb0", "#c85a80"), ("#ffffff", "#d8d0c8"), ("#f6a640", "#c87a24")], 1)):
        W, H = 380, 560
        nx = Seq(91400 + sd * 300); rng = random.Random(914 + sd)
        art = blank(W, H)
        art = soft_ground(art, W, H, 190, 540, 150, 10, "#6a4a36", nx, 0.3)
        legs = strokes(W, H, [([(96, 380), (80, 548)], 11, None), ([(284, 380), (300, 548)], 11, None), ([(190, 400), (190, 548)], 9, None)])
        art = body_paint(art, legs, "#c9a46a", "#d6b47a", "#8f7040", "#efd9a6", nx, ldir=(3, 0), blur=3)
        art = tint(art, strokes(W, H, [([(70, y), (310, y)], 2, None) for y in (440, 500)]) * legs, "#7a5a30", 0.6, seed=nx())
        frame = shapes(W, H, [[(40, 56), (340, 56), (340, 420), (40, 420)]], smooth=False)
        art = GP(art, frame, "#3d6334", "#4a7040", seed=nx(), rough=0.8)
        # white panel (blank for HTML text): x 76..304, y 96..380
        panel = shapes(W, H, [[(76, 96), (304, 96), (304, 380), (76, 380)]], smooth=False)
        art = body_paint(art, panel, "#fffdf8", "#f8f4ec", "#d8d0c4", "#ffffff", nx, ldir=(0, 4), blur=6, light_amt=0.2)
        # flower border: blooms along the frame band + crest on top
        pts = []
        for x in np.linspace(48, 332, 13):
            pts += [(x, 76), (x, 400)]
        for y in np.linspace(96, 380, 11):
            pts += [(58, y), (322, y)]
        crest = [(190 + math.cos(a) * 90, 56 - math.sin(a) * 36) for a in np.linspace(0.15, math.pi - 0.15, 9)]
        pts += crest + [(190, 20)]
        rng.shuffle(pts)
        leafs = []
        for x, y in pts[::2]:
            a = rng.uniform(0, 6.28)
            leafs.append(petal_pts(x + math.cos(a) * 10, y + math.sin(a) * 10, 22, 8, a, n=10))
        art = body_paint(art, shapes(W, H, leafs), LEAF, LEAF2, LEAFD, "#9cc07a", nx, ldir=(3, 3), blur=3)
        for i, (x, y) in enumerate(pts):
            c, d = pal[i % len(pal)]
            r = rng.uniform(13, 18) if (x, y) not in crest else rng.uniform(17, 22)
            petals = [petal_pts(x, y, r, r * 0.55, a + rng.uniform(-.1, .1), n=10) for a in np.linspace(0, 6.28, 7)[:-1] + rng.uniform(0, 1)]
            m = shapes(W, H, petals)
            art = body_paint(art, m, c, mix(c, "#ffffff", 0.15), d, mix(c, "#ffffff", 0.5), nx, ldir=(2, 3), blur=3, light_amt=0.3, dark_amt=0.55)
            art = GP(art, circles(W, H, [(x, y, r * 0.28)]), "#f2c230" if c != "#f2c230" else "#c8541c", seed=nx(), rough=0.3, pad=5)
            if i % 10 == 9:
                clear()
        # sash ribbon across the bottom corner
        sash = shapes(W, H, [[(40, 330), (130, 420), (98, 420), (40, 362)]], smooth=False)
        art = body_paint(art, sash, RED if sd else GOLD, mix(RED if sd else GOLD, "#ffffff", .15), REDD if sd else GOLDD, REDL if sd else GOLDL, nx, blur=3)
        preview(art, f"pu-{name}", tone=BG)
        save_full(art, f"{OUT}/{name}.webp", size=(190, 280), quality=80)
        clear()

if "confetti" in PARTS:
    W, H = 640, 640
    nx = Seq(91500); rng = random.Random(915)
    art = blank(W, H)
    art = confetti(art, W, H, 240, [RED, GOLD, TEAL, "#ef8fb0", "#f6a640"], nx, rng, size=(12, 22))
    preview(art, "pu-confetti", tone="#3a2620")
    save_full(art, f"{OUT}/confetti.webp", size=(400, 400), quality=78)
    clear()
