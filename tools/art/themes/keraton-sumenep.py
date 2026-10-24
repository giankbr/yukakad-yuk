"""Keraton Sumenep — the Labang Mesem gate of the Sumenep palace in gouache (white plaster, sweeping slate roof with a
red curled ridge, jade posts, chrome-yellow trims, red doors), hanging red lanterns, a brightly painted Madura carving
band (red ground, jade leaves, yellow leaf), a carved flower medallion and a Madura batik tile.
Run: python3 -I keraton-sumenep.py [part ...]  parts: gate lantern ukir kembang divider batik
Assets -> public/themes/art/keraton-sumenep/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t2_lib import *

OUT = outdir("keraton-sumenep")
PARTS = sys.argv[1:] or ["gate", "lantern", "ukir", "kembang", "divider", "batik"]
INK = "#3a2418"
WALL, WALL_D, WALL_L = "#f3ead8", "#cdbd9f", "#fffaf0"
RED, RED_D, RED_L = "#b5262b", "#7a1419", "#d9483f"
YEL, YEL_D, YEL_L = "#e8b42a", "#b07f12", "#f7d66a"
GRN, GRN_D, GRN_L = "#2f7a52", "#1b4c35", "#5aa477"
ROOF, ROOF_D, ROOF_L = "#3b4a46", "#232e2b", "#64746e"


def poly(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def relief(art, W, H, ground, items, leaves, nx, base=RED, base_d=RED_D, fg=GRN, fg_l=GRN_L, fg_d=GRN_D, gild=YEL, thick=1.0):
    """Brightly painted Madura carving: red ground, raised jade relief with cast shadow and a yellow gilt edge."""
    art = body(art, ground, base, mix(base, RED_L, 0.2), base_d, RED_L, nx, ldir=(0, -4), blur=6)
    rel = np.maximum(strokes(W, H, [(p, w * thick, t) for p, w, t in items]), shapes(W, H, leaves)) * ground
    sh = np.roll(np.roll(gaussian_filter(rel, 1.5), 3, 0), 2, 1) * ground
    art = G(art, sh, base_d, seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.6, feather=0.6)
    art = body(art, rel, fg, fg_l, fg_d, mix(fg_l, "#ffffff", 0.3), nx, ldir=(3, 3), blur=1.6, rough=0.6)
    art = crayon(art, inner_edge(rel, 1.3), gild, seed=nx(), amt=0.9, tooth=0.15)
    return art


if "gate" in PARTS:
    W, H = 800, 640
    nx = Seq(71000); rng = random.Random(5)
    art = blank(W, H)
    cx = 400
    # ground shadow + steps
    art = G(art, shapes(W, H, [ellipse_pts(cx, 612, 380, 20, 24)]), "#6b5a40", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=6)
    steps = poly(W, H, [(90, 586), (710, 586), (722, 612), (78, 612)])
    art = body(art, steps, "#d8ccb4", "#e6dcc6", "#9e8f75", "#fff8ea", nx, ldir=(0, -6), blur=4, outline=INK, line_amt=0.35)
    # side wings (low walls with small roofs)
    for sx in (-1, 1):
        x0, x1 = (52, 150) if sx < 0 else (650, 748)
        wing = poly(W, H, [(x0, 420), (x1, 420), (x1, 588), (x0, 588)])
        art = body(art, wing, WALL, WALL_L, WALL_D, "#ffffff", nx, ldir=(-8 * sx, -6), blur=7, outline=INK, line_amt=0.35)
        band = poly(W, H, [(x0, 452), (x1, 452), (x1, 464), (x0, 464)])
        art = GP(art, band, YEL, YEL_L, seed=nx(), rough=0.5, pad=6)
        base_ = poly(W, H, [(x0, 560), (x1, 560), (x1, 588), (x0, 588)])
        art = GP(art, base_, GRN, GRN_D, seed=nx(), rough=0.5, pad=6)
        cap = poly(W, H, [(x0 - 14, 424), (x1 + 14, 424), (x1 + 4, 404), ((x0 + x1) / 2, 392), (x0 - 4, 404)])
        art = body(art, cap, ROOF, ROOF_L, ROOF_D, ROOF_L, nx, ldir=(0, 6), blur=4, outline=INK, line_amt=0.4)
        # small window grille in the wing
        win = poly(W, H, [((x0 + x1) / 2 - 18, 486), ((x0 + x1) / 2 + 18, 486), ((x0 + x1) / 2 + 18, 534), ((x0 + x1) / 2 - 18, 534)])
        art = GP(art, win, GRN_D, GRN, seed=nx(), rough=0.4, pad=6)
        bars = strokes(W, H, [([((x0 + x1) / 2 + d, 488), ((x0 + x1) / 2 + d, 532)], 2.2, None) for d in (-9, 0, 9)])
        art = GP(art, bars * win, YEL, seed=nx(), rough=0.3, pad=4)
    # main gate block
    block = poly(W, H, [(150, 318), (650, 318), (650, 588), (150, 588)])
    art = body(art, block, WALL, WALL_L, WALL_D, "#ffffff", nx, ldir=(-10, -4), blur=10, outline=INK, line_amt=0.4)
    # pilasters (jade) and base course
    for px in (150, 236, 548, 634):
        pil = poly(W, H, [(px, 330), (px + 18, 330), (px + 18, 588), (px, 588)])
        art = body(art, pil, GRN, GRN_L, GRN_D, GRN_L, nx, ldir=(-4, 0), blur=3, outline=INK, line_amt=0.3)
        cap_ = poly(W, H, [(px - 5, 326), (px + 23, 326), (px + 23, 340), (px - 5, 340)])
        art = GP(art, cap_, YEL, YEL_L, seed=nx(), rough=0.4, pad=4)
    base2 = poly(W, H, [(150, 562), (650, 562), (650, 588), (150, 588)])
    art = body(art, base2, RED, RED_L, RED_D, RED_L, nx, ldir=(0, -4), blur=3)
    # arched opening
    ox0, ox1, otop, obot = 322, 478, 372, 588
    r = (ox1 - ox0) / 2
    arch_pts = [(ox0, obot), (ox0, otop + r)] + arc_pts(cx, otop + r, r, math.pi, math.tau, 30) + [(ox1, otop + r), (ox1, obot)]
    opening = poly(W, H, arch_pts)
    frame = np.clip(gaussian_filter(opening, 7) * 2.5, 0, 1)
    frame = np.clip(frame - opening * 0.0, 0, 1)
    frame_ring = np.clip(poly(W, H, [(ox0 - 14, obot), (ox0 - 14, otop + r)] + arc_pts(cx, otop + r, r + 14, math.pi, math.tau, 30) + [(ox1 + 14, otop + r), (ox1 + 14, obot)]) - opening, 0, 1)
    art = body(art, frame_ring, YEL, YEL_L, YEL_D, YEL_L, nx, ldir=(-4, -4), blur=3, outline=INK, line_amt=0.4)
    # inner: shadowed passage, glimpse of courtyard light at the far end, red door leaves open on both sides
    art = GP(art, opening, "#4a3a2c", "#3a2c22", seed=nx(), rough=0.4)
    far = poly(W, H, [(372, 588), (372, 470)] + arc_pts(cx, 470, 28, math.pi, math.tau, 16) + [(428, 470), (428, 588)])
    art = GP(art, far, "#f2dfae", "#e8cf8e", seed=nx(), rough=0.6)
    art = tint(art, gaussian_filter(far, 8) * opening, "#f4d995", 0.35, seed=nx(), clip=True)
    floor = poly(W, H, [(ox0, 588), (372, 548), (428, 548), (ox1, 588)]) * opening
    art = GP(art, floor, "#8a7558", "#6f5c44", seed=nx(), rough=0.4, pad=4)
    for sx in (-1, 1):
        dl = poly(W, H, [(cx + sx * 78, 588), (cx + sx * 78, 440), (cx + sx * 46, 452), (cx + sx * 46, 562)])
        art = body(art, dl * opening, RED, RED_L, RED_D, RED_L, nx, ldir=(sx * 4, 0), blur=4)
        studs = circles(W, H, [(cx + sx * (52 + k % 2 * 14), 470 + (k // 2) * 22, 2.4) for k in range(8)]) * dl
        art = GP(art, studs, YEL_L, seed=nx(), rough=0.2, pad=3)
    art = crayon(art, inner_edge(opening, 2.0), INK, seed=nx(), amt=0.6, tooth=0.25)
    # carved panels above the arch, either side (red ground with jade/yellow scrolls)
    for sx in (-1, 1):
        pcx = cx + sx * 142
        panel = poly(W, H, [(pcx - 56, 360), (pcx + 56, 360), (pcx + 56, 430), (pcx - 56, 430)])
        items, leaves = [], []
        for k, f in enumerate((1, -1)):
            it, lv = lung(pcx + (k - 0.5) * 52, 398, 30, 0.0 if k == 0 else math.pi, 1)
            items += it; leaves += lv
        leaves += [petal_pts(pcx, 394, 14, 7, j / 5 * math.tau, n=10) for j in range(5)]
        art = relief(art, W, H, panel, items, leaves, nx, thick=1.5)
        art = GP(art, circles(W, H, [(pcx, 394, 4)]), YEL_L, seed=nx(), rough=0.2, pad=4)
        art = crayon(art, inner_edge(panel, 2), INK, seed=nx(), amt=0.5)
        # tall slit windows below the panels
        win = poly(W, H, [(pcx - 20, 452), (pcx + 20, 452), (pcx + 20, 536), (pcx - 20, 536)])
        art = GP(art, win, GRN_D, GRN, seed=nx(), rough=0.4, pad=4)
        bars = strokes(W, H, [([(pcx + d, 454), (pcx + d, 534)], 2.4, None) for d in (-10, 0, 10)] + [([(pcx - 20, 494), (pcx + 20, 494)], 2.4, None)])
        art = GP(art, bars * win, YEL, seed=nx(), rough=0.3, pad=4)
        art = crayon(art, inner_edge(win, 1.6), INK, seed=nx(), amt=0.5)
    # yellow cornice + red frieze across the top of the block
    corn = poly(W, H, [(140, 304), (660, 304), (660, 320), (140, 320)])
    art = body(art, corn, YEL, YEL_L, YEL_D, YEL_L, nx, ldir=(0, -3), blur=2, outline=INK, line_amt=0.4)
    friez = poly(W, H, [(150, 320), (650, 320), (650, 334), (150, 334)])
    art = GP(art, friez, RED, RED_D, seed=nx(), rough=0.4)
    dent = shapes(W, H, [[(158 + k * 16, 322), (166 + k * 16, 322), (166 + k * 16, 332), (158 + k * 16, 332)] for k in range(31)], smooth=False)
    art = GP(art, dent * friez, YEL_L, seed=nx(), rough=0.3, pad=4)
    # lower canopy roof over the block front
    can = poly(W, H, [(118, 312), (682, 312), (660, 284), (140, 284)])
    art = body(art, can, ROOF, ROOF_L, ROOF_D, ROOF_L, nx, ldir=(0, 6), blur=4, outline=INK, line_amt=0.4)
    tiles = strokes(W, H, [([(130 + k * 14, 310), (146 + k * 12.4, 286)], 1.6, None) for k in range(40)]) * can
    art = G(art, tiles, ROOF_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    # upper pavilion (lookout): posts, railing, red panels
    pav = poly(W, H, [(232, 196), (568, 196), (568, 286), (232, 286)])
    art = body(art, pav, "#6a2a1e", "#7a3424", "#3c140e", "#8a4430", nx, ldir=(0, -6), blur=5)
    for k in range(6):
        px = 238 + k * 64
        post = poly(W, H, [(px, 198), (px + 12, 198), (px + 12, 286), (px, 286)])
        art = body(art, post, GRN, GRN_L, GRN_D, GRN_L, nx, ldir=(-3, 0), blur=2, outline=INK, line_amt=0.3)
        if k < 5:
            pnl = poly(W, H, [(px + 18, 250), (px + 58, 250), (px + 58, 282), (px + 18, 282)])
            art = body(art, pnl, RED, RED_L, RED_D, RED_L, nx, ldir=(0, -3), blur=2)
            dia = poly(W, H, [(px + 38, 254), (px + 52, 266), (px + 38, 278), (px + 24, 266)])
            art = GP(art, dia, YEL, YEL_L, seed=nx(), rough=0.3, pad=4)
            # hanging fretwork under the beam
            fret = strokes(W, H, [(arc_pts(px + 38, 206, 18, 0.15, math.pi - 0.15, 12), 3, None)])
            art = GP(art, fret, YEL, seed=nx(), rough=0.3, pad=4)
    rail = poly(W, H, [(230, 244), (570, 244), (570, 252), (230, 252)])
    art = GP(art, rail, YEL, YEL_L, seed=nx(), rough=0.4, pad=4)
    # main roof: sweeping eaves with upturned tips
    eave_l, eave_r = (150, 186), (650, 186)
    roof_pts = [eave_l] + curve([(150, 186), (210, 200), (300, 204), (400, 205), (500, 204), (590, 200), (650, 186)], 40) + \
               [(650, 186), (612, 172)] + curve([(612, 172), (560, 150), (520, 112)], 16) + [(280, 112)] + curve([(280, 112), (240, 150), (188, 172)], 16) + [(188, 172)]
    roof = shapes(W, H, [roof_pts], smooth=False)
    art = body(art, roof, ROOF, ROOF_L, ROOF_D, ROOF_L, nx, ldir=(-6, 8), blur=6, outline=INK, line_amt=0.45)
    ribs = strokes(W, H, [([(196 + k * 13.5, 202), (288 + k * 9, 112)], 1.8, None) for k in range(36)]) * roof
    art = G(art, ribs, ROOF_D, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    eave_trim = strokes(W, H, [(curve([(146, 184), (210, 199), (300, 203), (400, 204), (500, 203), (590, 199), (654, 184)], 40), 5, None)])
    art = GP(art, eave_trim, YEL, YEL_L, seed=nx(), rough=0.4, pad=4)
    # ridge with curled ends + centre ornament (red)
    ridge = strokes(W, H, [(curve([(262, 104), (330, 110), (400, 111), (470, 110), (538, 104)], 30), 12, None)])
    curls = strokes(W, H, [(spiral_pts(256, 92, 16, 3, math.pi * 0.3, 1.1, 30, 1), 7, (0.0, 0.6)),
                           (spiral_pts(544, 92, 16, 3, math.pi * 0.7, 1.1, 30, -1), 7, (0.0, 0.6))])
    tips = strokes(W, H, [(curve([(156, 186), (138, 178), (130, 160)], 12), 7, (0.0, 0.7)), (curve([(644, 186), (662, 178), (670, 160)], 12), 7, (0.0, 0.7))])
    art = body(art, np.clip(ridge + curls + tips, 0, 1), RED, RED_L, RED_D, RED_L, nx, ldir=(0, 3), blur=2, outline=INK, line_amt=0.4)
    orn = poly(W, H, [(400, 64), (418, 92), (410, 104), (390, 104), (382, 92)])
    art = body(art, orn, YEL, YEL_L, YEL_D, YEL_L, nx, ldir=(-3, 0), blur=2, outline=INK, line_amt=0.4)
    art = body(art, circles(W, H, [(400, 58, 9)]), RED, RED_L, RED_D, RED_L, nx, blur=2)
    # nameplate above the arch: blank yellow plaque with red border
    plq = poly(W, H, [(352, 340), (448, 340), (448, 358), (352, 358)])
    art = body(art, plq, RED, RED_L, RED_D, RED_L, nx, blur=2)
    walls = np.clip(block + poly(W, H, [(52, 420), (150, 420), (150, 588), (52, 588)]) + poly(W, H, [(650, 420), (748, 420), (748, 588), (650, 588)]), 0, 1)
    stain = walls * np.clip(fbm(W, H, nx(), 60, 3) * 1.6 - 0.6, 0, 1) * (1 - opening)
    art = G(art, stain, "#c9b48c", "#b9a17a", seed=nx(), density=0.22, edge=0.3, bloom=0.4, rough=6)
    art = add_grain(art, nx(), 0.05)
    preview(art, "ks-gate", tone="#fbf3e2")
    save(art, f"{OUT}/gate.webp", max_w=800, quality=82)
    clear()

if "lantern" in PARTS:
    W, H = 120, 240
    nx = Seq(72000)
    art = blank(W, H)
    cordm = strokes(W, H, [([(60, 0), (60, 40)], 2.2, None)])
    art = GP(art, cordm, INK, seed=nx(), rough=0.3, pad=4)
    capT = poly(W, H, [(40, 40), (80, 40), (84, 54), (36, 54)])
    capB = poly(W, H, [(36, 158), (84, 158), (80, 172), (40, 172)])
    lamp = shapes(W, H, [deform(ellipse_pts(60, 106, 50, 58, 24), random.Random(3), 1, 0.01)])
    art = body(art, lamp, RED, RED_L, RED_D, "#f06a52", nx, ldir=(-8, -4), blur=10, outline=INK, line_amt=0.5)
    ribs = strokes(W, H, [(curve([(60 + d * 0.4, 50), (60 + d, 106), (60 + d * 0.4, 162)], 20), 1.6, None) for d in (-36, -18, 0, 18, 36)]) * lamp
    art = G(art, ribs, RED_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.4, feather=0.3)
    glowm = shapes(W, H, [ellipse_pts(52, 100, 18, 28, 12)])
    art = tint(art, gaussian_filter(glowm, 6), "#ffb36a", 0.45, seed=nx())
    art = body(art, np.clip(capT + capB, 0, 1), YEL, YEL_L, YEL_D, YEL_L, nx, blur=2, outline=INK, line_amt=0.5)
    tas = strokes(W, H, [([(60 + d, 172), (60 + d * 1.6, 232)], 1.6, (0.0, 0.5)) for d in range(-7, 8, 2)])
    art = GP(art, tas, YEL, YEL_D, seed=nx(), rough=0.4, pad=4)
    knot = circles(W, H, [(60, 178, 6)])
    art = GP(art, knot, RED_D, seed=nx(), rough=0.3, pad=4)
    preview(art, "ks-lantern", tone="#fbf3e2")
    save(art, f"{OUT}/lantern.webp", max_w=120, quality=84)
    clear()

if "ukir" in PARTS:
    W, H = 840, 120
    nx = Seq(73000)
    art = blank(W, H)
    band = poly(W, H, [(0, 12), (W, 12), (W, 108), (0, 108)])
    items, leaves = [], []
    for k in range(6):
        it, lv = lung(70 + k * 140, 64, 50, 0.0, 1 if k % 2 == 0 else -1)
        items += it; leaves += lv
    for k in range(6):
        fx = 140 * k + 140
        leaves += [petal_pts(fx, 60, 20, 9, j / 6 * math.tau + 0.3, n=10) for j in range(6)]
    art = relief(art, W, H, band, items, leaves, nx, thick=1.5)
    art = GP(art, circles(W, H, [(140 * k + 140, 60, 6) for k in range(6)]), RED, seed=nx(), rough=0.3, pad=4)
    for y0 in (0, 106):
        m = poly(W, H, [(0, y0), (W, y0), (W, y0 + 14), (0, y0 + 14)])
        art = body(art, m, YEL, YEL_L, YEL_D, YEL_L, nx, ldir=(0, -2), blur=2)
    art = add_grain(art, nx(), 0.04)
    preview(art, "ks-ukir", tone="#fbf3e2")
    save(art, f"{OUT}/ukir.webp", max_w=840, quality=80)
    clear()

if "kembang" in PARTS:
    W, H = 300, 300
    nx = Seq(74000); rng = random.Random(9)
    art = blank(W, H)
    cx, cy = 150, 150
    disc = circles(W, H, [(cx, cy, 136)])
    art = body(art, disc, GRN, GRN_L, GRN_D, GRN_L, nx, ldir=(-8, -8), blur=8, outline=INK, line_amt=0.4)
    ring = np.clip(circles(W, H, [(cx, cy, 126)]) - circles(W, H, [(cx, cy, 116)]), 0, 1)
    art = GP(art, ring, YEL, YEL_L, seed=nx(), rough=0.4, pad=4)
    inner = circles(W, H, [(cx, cy, 112)])
    art = GP(art, inner, RED, RED_D, seed=nx(), rough=0.5)
    # eight scroll leaves around + big 8-petal flower
    items, leaves = [], []
    for k in range(8):
        a = k / 8 * math.tau
        it, lv = lung(cx + math.cos(a) * 78, cy + math.sin(a) * 78, 30, a + math.pi / 2, 1)
        items += it; leaves += lv
    art = relief(art, W, H, inner, items, leaves, nx, thick=1.6)
    pet = shapes(W, H, [petal_pts(cx, cy, 52, 20, k / 8 * math.tau + 0.2, n=12) for k in range(8)])
    art = body(art, pet, YEL, YEL_L, YEL_D, "#fff0b0", nx, ldir=(3, 3), blur=2.5, outline=RED_D, line_amt=0.6)
    pet2 = shapes(W, H, [petal_pts(cx, cy, 30, 12, k / 8 * math.tau + 0.6, n=12) for k in range(8)])
    art = body(art, pet2, "#f2f0e6", "#ffffff", WALL_D, "#ffffff", nx, blur=2)
    art = body(art, circles(W, H, [(cx, cy, 12)]), RED, RED_L, RED_D, RED_L, nx, blur=2, outline=INK, line_amt=0.5)
    art = add_grain(art, nx(), 0.03)
    preview(art, "ks-kembang", tone="#fbf3e2")
    save(art, f"{OUT}/kembang.webp", max_w=260, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 420, 80
    nx = Seq(75000)
    art = blank(W, H)
    items, leaves = [], []
    it, lv = lung(150, 40, 46, math.pi, 1); items += it; leaves += lv
    it, lv = lung(270, 40, 46, 0.0, -1); items += it; leaves += lv
    items += [(curve([(14, 40), (60, 40), (100, 40)], 12), 3.0, (0.6, 0.05)), (curve([(320, 40), (360, 40), (406, 40)], 12), 3.0, (0.05, 0.6))]
    art = GP(art, strokes(W, H, [(p, w * 1.3, t) for p, w, t in items]), RED, RED_D, seed=nx(), rough=0.5, pad=6)
    art = body(art, shapes(W, H, leaves), GRN, GRN_L, GRN_D, GRN_L, nx, blur=2)
    dia = poly(W, H, [(210, 18), (232, 40), (210, 62), (188, 40)])
    art = body(art, dia, YEL, YEL_L, YEL_D, YEL_L, nx, blur=2, outline=RED_D, line_amt=0.7)
    art = GP(art, circles(W, H, [(210, 40, 6)]), RED, seed=nx(), rough=0.2, pad=4)
    preview(art, "ks-divider", tone="#fbf3e2")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
    clear()

if "batik" in PARTS:
    # Madura batik tile: bold red & yellow flowers with jade leaves on a deep green ground, canting dots (isen).
    T = 320
    nx = Seq(76000); rng = random.Random(4)
    W = H = T * 3  # draw on a 3x3 field, keep centre tile → seamless
    def rep(fn):
        out = []
        for ox in (-T, 0, T):
            for oy in (-T, 0, T):
                out += fn(ox + T, oy + T)
        return out
    flowers = [(80, 90, 1.0), (240, 230, 0.85), (250, 60, 0.55), (60, 260, 0.5)]
    pet = rep(lambda ox, oy: [petal_pts(ox + x, oy + y, 48 * s, 20 * s, k / 6 * math.tau + s, n=16) for x, y, s in flowers for k in range(6)])
    leafp = rep(lambda ox, oy: [petal_pts(ox + x + math.cos(a) * 40 * s, oy + y + math.sin(a) * 40 * s, 56 * s, 16 * s, a + 0.4, n=12) for x, y, s in flowers for a in (0.6, 2.4, 4.3)])
    stems = rep(lambda ox, oy: [(curve([(ox + 80, oy + 90), (ox + 160, oy + 120), (ox + 200, oy + 200), (ox + 240, oy + 230)], 30), 5, None),
                                (curve([(ox + 240, oy + 230), (ox + 300, oy + 300), (ox + 380, oy + 330), (ox + 400, oy + 410)], 30), 5, None)])
    ground = np.ones((H, W), np.float32)
    art = GP(blank(W, H), ground, "#174334", "#1d4d3b", seed=nx(), rough=0.1, streak=0.8)
    lm = shapes(W, H, leafp)
    art = GP(art, lm, GRN_L, GRN, seed=nx(), rough=0.8)
    art = GP(art, strokes(W, H, stems), "#3e8a5e", seed=nx(), rough=0.6)
    pm = shapes(W, H, pet)
    art = GP(art, pm, RED, RED_L, seed=nx(), rough=0.8)
    hearts = circles(W, H, rep(lambda ox, oy: [(ox + x, oy + y, 14 * s) for x, y, s in flowers]))
    art = GP(art, hearts, YEL, YEL_L, seed=nx(), rough=0.5)
    # malam (wax) lines: thin light outlines
    pol = []
    for P in pet + leafp:
        pol.append((P + [P[0]], 2.2, None))
    outl = strokes(W, H, pol)
    art = OV(art, outl, lambda m: col_arr(m, "#f6ead0", m * 0.7))
    dots = circles(W, H, rep(lambda ox, oy: [(ox + rng.uniform(0, T), oy + rng.uniform(0, T), 1.8) for _ in range(140)])) * (1 - np.clip(gaussian_filter(pm + lm, 3) * 3, 0, 1))
    art = OV(art, dots, lambda m: col_arr(m, YEL_L, m * 0.55))
    tile = art[T:2 * T, T:2 * T]
    tile = add_grain(tile, nx(), 0.04)
    Image.fromarray((np.clip(tile, 0, 1) * 255).astype(np.uint8)).convert("RGB").save(f"{PREV}/ks-batik.png")
    save_rgb(tile, f"{OUT}/batik.webp", quality=72)
    clear()
