"""Pesta Piyama — kids' sleepover in cosy picture-book gouache with soft plum pencil outlines: a blanket fort (patchwork
quilt draped over two chairs, a glowing doorway with pillows inside, a string of fairy lights along the canopy, a
pink rug) plus its separate bulb-glow layer for twinkling; Momo the plush bear (an original toy) hugging a pillow;
a striped popcorn bucket; a sleepy crescent moon in a nightcap; a short fairy-light divider; and a night-sky tile.
Run: python3 -I pesta-piyama.py [part ...]  parts: fort bear popcorn moon bulbs sky"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k6_lib import *

OUT = outdir("pesta-piyama")
PARTS = sys.argv[1:] or ["fort", "bear", "popcorn", "moon", "bulbs", "sky"]
INK = "#4a3658"
NIGHT, NIGHT_D = "#22385a", "#172741"
CREAM, BUTTER, BUTTER_D = "#fbeed3", "#ffd36e", "#e8ae3a"
CORAL, CORAL_D, PINK, PINK_D = "#f08a74", "#d9664f", "#f6b2c0", "#e38aa0"
MINT, MINT_D, LILAC, SKY = "#8fd3c1", "#5fb3a0", "#b9a7e0", "#8cc2ec"
WOOD, WOOD_D = "#b98257", "#8a5a36"
nx = Seq(2100)
BULBS = [BUTTER, CORAL, MINT, PINK, SKY]


def ink(art, mask, col, col2=None, lw=3.0):
    return inked(art, mask, col, col2, seed=nx(), ink=INK, lw=lw, alpha=0.85)


def fairy(art, W, H, pts, every=9, r=9, glow_only=False):
    """Wire + bulbs along a polyline; returns (art, glow_mask, bulb_cols)."""
    if not glow_only:
        wire = polyline_mask(W, H, [pts], 2.2)
        art = over(art, flat(wire, "#3d3550", 0.85))
    gl = []
    for k, i in enumerate(range(every // 2, len(pts) - 1, every)):
        (x, y), (x2, y2) = pts[i], pts[i + 1]
        col = BULBS[k % len(BULBS)]
        bm = ell(W, H, x, y + r * 0.9, r * 0.62, r, 0)
        cap = rrect(W, H, x - 3.5, y - 2, x + 3.5, y + 4, 1.5)
        gl.append((x, y + r * 0.9, col))
        if not glow_only:
            art = over(art, flat(cap, "#6a6070", 1.0))
            art = GP(art, bm, col, mix(col, "#ffffff", 0.4), seed=nx(), rough=0.4, pad=4)
            art = over(art, flat(ell(W, H, x - r * 0.18, y + r * 0.55, r * 0.18, r * 0.3, 0), "#ffffff", 0.75))
    return art, gl


def glow_layer(W, H, gl, r=9):
    lay = blank(W, H)
    for x, y, col in gl:
        m = circles(W, H, [(x, y, r * 1.3)])
        lay = over(lay, glow(m, col, r * 1.6, 0.55))
        lay = over(lay, glow(m, "#fff6d8", r * 0.6, 0.5))
    return lay


def fort():
    W, H = 840, 660
    art = blank(W, H)
    # rug
    rug = ell(W, H, 420, 590, 400, 62)
    art = ink(art, rug, PINK, "#f3a3b5")
    art = over(art, flat(np.clip(ell(W, H, 420, 590, 360, 48) - ell(W, H, 420, 590, 352, 42), 0, 1), "#ffffff", 0.6))
    # chair backs + legs
    for x0 in (52, 668):
        legs = polyline_mask(W, H, [[(x0 + 12, 430), (x0 + 6, 600)], [(x0 + 108, 430), (x0 + 114, 600)]], 12)
        art = ink(art, legs, WOOD, WOOD_D, 2.6)
        back = rrect(W, H, x0, 90, x0 + 120, 200, 18)
        art = ink(art, back, WOOD, WOOD_D)
        art = over(art, flat(rrect(W, H, x0 + 22, 112, x0 + 98, 150, 10), "#9a6a42", 0.5))
    # quilt canopy (outline, sagging top, flared hem)
    top = curve([(70, 156), (250, 196), (420, 176), (590, 196), (770, 156)], 60)
    hem = curve([(806, 566), (720, 548), (640, 560), (560, 546), (420, 556), (280, 546), (200, 560), (120, 548), (34, 566)], 80)
    quilt = shapes(W, H, [top + [(784, 300), (800, 460)] + hem + [(40, 460), (56, 300)]])
    door = shapes(W, H, [[(262, 560), (290, 390), (360, 280), (420, 262), (480, 280), (550, 390), (578, 560)]])
    inside = np.clip(door, 0, 1)
    quilt_m = np.clip(quilt - door, 0, 1)
    # patchwork: squares of colour
    rng = random.Random(nx())
    cols = [CORAL, MINT, BUTTER, LILAC, PINK, SKY, CREAM]
    patches = []
    cell = 66
    for j in range(0, 8):
        for i in range(0, 14):
            x, y = 40 + i * cell + (j % 2) * 18, 130 + j * cell
            patches.append((x, y, cols[(i * 3 + j * 2 + rng.randint(0, 1)) % len(cols)]))
    pw = blank(W, H)
    by_col = {}
    for x, y, c in patches:
        by_col.setdefault(c, []).append([(x, y), (x + cell, y + 4), (x + cell - 3, y + cell), (x - 2, y + cell - 3)])
    for c, polys in by_col.items():
        m = shapes(W, H, polys, smooth=False)
        pw = GP(pw, m, c, mix(c, "#ffffff", 0.18), seed=nx(), rough=1.2, streak=0.9, pad=6)
    # gingham / dots on a few patches
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dots = (((xx % 16) - 8) ** 2 + ((yy % 16) - 8) ** 2 < 9).astype(np.float32)
    pw = over(pw, flat(dots * shapes(W, H, by_col[LILAC], smooth=False), "#ffffff", 0.7))
    stripes = ((xx + yy) % 18 < 7).astype(np.float32)
    pw = over(pw, flat(stripes * shapes(W, H, by_col[SKY], smooth=False), "#ffffff", 0.55))
    # seams: dashed stitches along the grid
    seams = []
    for j in range(0, 9):
        seams.append([(30, 130 + j * cell), (820, 130 + j * cell)])
    for i in range(0, 15):
        seams.append([(40 + i * cell + 9, 120), (40 + i * cell + 9, 600)])
    sm = np.zeros((H, W), np.float32)
    for p in seams:
        sm = np.maximum(sm, dashed(W, H, p, 2.0, 7, 6))
    pw = over(pw, flat(sm, "#fffaf0", 0.75))
    # drape the flat patchwork: sag between the chairs, bulge at the sides
    yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx2 - 420) / 420
    dy = -26 * (1 - u ** 2) * np.clip((yy2 - 150) / 120, 0, 1) * np.clip((560 - yy2) / 200, 0, 1) + 8 * np.sin(xx2 / 55)
    dx = 30 * u * np.clip((yy2 - 200) / 360, 0, 1) + 5 * np.sin(yy2 / 40)
    pw = np.stack([map_coordinates(pw[..., c], [yy2 + dy, xx2 - dx], order=1, mode="nearest") for c in range(4)], -1)
    pw[..., 3] *= quilt_m
    art = over(art, pw)
    # drape folds (soft vertical shading), sides darker
    folds = strokes(W, H, [(curve([(x, 210), (x + 8, 380), (x - 6, 540)], 20), 20, (0.3, 0.3)) for x in (110, 190, 640, 720)])
    art = over(art, flat(gaussian_filter(folds, 8) * quilt_m, "#3a2a4a", 0.18))
    art = shade_side(art, quilt_m, "#3a2a4a", (1, 1), 0.2, 30, nx())
    # doorway: warm glowing interior with pillows
    art = GP(art, inside, "#5a3f5e", "#4a3552", seed=nx(), rough=1.0, pad=4)
    art = over(art, glow(ell(W, H, 420, 470, 120, 80) * inside, "#ffcf7a", 30, 0.5))
    art = over(art, flat(gaussian_filter(ell(W, H, 420, 480, 130, 90), 30) * inside, "#ffd88f", 0.55))
    p1 = rrect(W, H, 300, 470, 440, 548, 34, rot=-6)
    p2 = rrect(W, H, 410, 462, 548, 548, 34, rot=7)
    art = ink(art, p2 * inside, MINT, "#a5dccd", 2.6)
    art = ink(art, p1 * inside, PINK, "#f8c4cf", 2.6)
    # tie-backs
    for x, y in ((300, 400), (540, 400)):
        bow = np.maximum(ell(W, H, x - 14, y, 16, 10, -20), ell(W, H, x + 14, y, 16, 10, 20))
        art = ink(art, bow, CORAL, CORAL_D, 2.4)
    art = ink_edge(art, quilt, INK, 3.2, nx(), 0.85)
    art = ink_edge(art, inside, INK, 2.6, nx(), 0.8)
    # fairy lights along the canopy, sagging between three points
    lp = curve([(60, 150), (160, 208), (260, 200), (340, 228), (420, 206), (500, 228), (580, 200), (680, 208), (780, 150)], 120)
    art, gl = fairy(art, W, H, lp, every=8, r=10)
    art = add_grain(art, nx(), 0.025)
    prev(art, "pp-fort", bg=NIGHT)
    save_full(art, f"{OUT}/fort.webp", (600, 471), quality=80)
    g = glow_layer(W, H, gl, 10)
    prev(over(art, g), "pp-fort-glow", bg=NIGHT)
    save_full(g, f"{OUT}/fortglow.webp", (600, 471), quality=70)


def bear():
    W, H = 420, 460
    art = blank(W, H)
    body = ell(W, H, 210, 320, 120, 115)
    legs = np.maximum(ell(W, H, 130, 410, 58, 40, -10), ell(W, H, 290, 410, 58, 40, 10))
    art = ink(art, legs, "#d9a066", "#c98f55")
    for x in (118, 302):
        art = ink(art, ell(W, H, x, 418, 28, 22), "#f3d7b0")
    art = ink(art, body, "#d9a066", "#c98f55")
    # pillow hugged
    pil = rrect(W, H, 112, 270, 308, 382, 40, rot=-4)
    art = ink(art, pil, LILAC, "#cbbdf0")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    st = (((xx - 200) % 22) < 9).astype(np.float32)
    art = over(art, flat(st * pil, "#ffffff", 0.35))
    art = over(art, flat(dashed(W, H, [(126, 286), (296, 278), (298, 368), (126, 376), (126, 286)], 2, 6, 6), "#ffffff", 0.7))
    arms = np.maximum(ell(W, H, 120, 300, 34, 54, 40), ell(W, H, 300, 300, 34, 54, -40))
    art = ink(art, arms, "#d9a066", "#c98f55")
    # head
    ears = circles(W, H, [(118, 78, 40), (302, 78, 40)])
    art = ink(art, ears, "#d9a066", "#c98f55")
    art = GP(art, circles(W, H, [(120, 80, 22), (300, 80, 22)]), "#f3c2b2", seed=nx(), rough=0.6, pad=4)
    head = ell(W, H, 210, 150, 118, 104)
    art = ink(art, head, "#e2ab70", "#d39858")
    art = highlight(art, head, "#ffffff", 0.25, 18)
    muz = ell(W, H, 210, 186, 52, 38)
    art = ink(art, muz, "#f7e2c4", None, 2.4)
    art = over(art, flat(ell(W, H, 210, 170, 15, 11), INK, 0.95))
    smile = polyline_mask(W, H, [arc_pts(198, 188, 12, 0.2, 2.6, 10), arc_pts(222, 188, 12, 0.5, 2.9, 10)], 3)
    art = over(art, flat(smile, INK, 0.9))
    eyes = polyline_mask(W, H, [arc_pts(160, 132, 13, 0.4, 2.7, 10), arc_pts(260, 132, 13, 0.4, 2.7, 10)], 4)  # sleepy closed eyes
    art = over(art, flat(eyes, INK, 0.95))
    art = over(art, flat(gaussian_filter(ell(W, H, 142, 176, 18, 11) + ell(W, H, 278, 176, 18, 11), 2), "#f28a8a", 0.5))
    # nightcap
    cap = shapes(W, H, [[(104, 96), (150, 40), (230, 22), (300, 30), (360, 2), (378, 40), (320, 80), (316, 96)]])
    art = ink(art, cap, MINT, "#a5dccd")
    art = over(art, flat((((xx + yy * 0.4) % 28) < 11).astype(np.float32) * cap, "#ffffff", 0.55))
    band = rrect(W, H, 96, 80, 324, 108, 14, rot=-2)
    art = ink(art, band, CREAM)
    art = ink(art, circles(W, H, [(380, 30, 22)]), CREAM)
    art = add_grain(art, nx(), 0.025)
    prev(art, "pp-bear", bg=NIGHT)
    save(art, f"{OUT}/bear.webp", max_w=220, quality=82)


def popcorn():
    W, H = 340, 400
    art = blank(W, H)
    rng = random.Random(nx())
    puffs = []
    for k in range(34):
        x = rng.uniform(60, 280); y = rng.uniform(60, 170) + abs(x - 170) * 0.35
        puffs.append((x, y, rng.uniform(17, 26)))
    pm = circles(W, H, puffs)
    art = ink(art, pm, "#fff7e4", "#fbe7b8", 2.4)
    art = over(art, flat(circles(W, H, [(x + 5, y + 6, r * 0.45) for x, y, r in puffs[::2]]) * pm, "#f3c868", 0.6))
    bucket = shapes(W, H, [[(52, 168), (288, 168), (258, 392), (82, 392)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = (xx - 170) / (118 - (yy - 168) * 0.13)
    st = ((np.floor(t * 4 + 8) % 2) == 0).astype(np.float32)
    art = ink(art, bucket, "#fffaf2")
    art = GP(art, st * bucket, CORAL, seed=nx(), rough=0.8, pad=4)
    art = shade_side(art, bucket, "#5a2a2a", (1, 1), 0.25, 20, nx())
    art = ink_edge(art, bucket, INK, 3, nx())
    rim = rrect(W, H, 44, 160, 296, 186, 10)
    art = ink(art, rim, "#fffaf2")
    art = add_grain(art, nx(), 0.025)
    prev(art, "pp-popcorn", bg=NIGHT)
    save(art, f"{OUT}/popcorn.webp", max_w=170, quality=82)


def moon():
    W, H = 420, 440
    art = blank(W, H)
    body = np.clip(circles(W, H, [(200, 250, 150)]) - circles(W, H, [(275, 205, 128)]), 0, 1)
    art = over(art, glow(body, "#ffe7a8", 26, 0.35))
    art = ink(art, body, BUTTER, "#ffe08e")
    art = highlight(art, body, "#fffbe8", 0.35, 16)
    art = G(art, circles(W, H, [(110, 300, 14), (150, 360, 9), (90, 230, 8)]) * body, "#e9b84a", seed=nx(), density=0.5, edge=0.5, rough=1, pad=4)
    eye = polyline_mask(W, H, [arc_pts(128, 262, 15, 0.4, 2.7, 10)], 4)
    art = over(art, flat(eye, INK, 0.95))
    art = over(art, flat(gaussian_filter(ell(W, H, 120, 300, 16, 10), 2), "#f28a8a", 0.55))
    smile = polyline_mask(W, H, [arc_pts(150, 322, 12, 0.3, 2.3, 10)], 3.2)
    art = over(art, flat(smile, INK, 0.9))
    # nightcap draped over the top horn
    cap = shapes(W, H, [[(120, 118), (200, 96), (262, 120), (330, 120), (392, 190), (366, 206), (304, 160), (250, 150), (170, 160)]])
    art = ink(art, cap, CORAL, "#f4a08c")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = over(art, flat((((xx - yy * 0.6) % 30) < 11).astype(np.float32) * cap, "#ffffff", 0.5))
    band = shapes(W, H, [[(112, 128), (196, 102), (210, 140), (126, 168)]])
    art = ink(art, band, CREAM)
    art = ink(art, circles(W, H, [(384, 210, 24)]), CREAM)
    # z z z
    for k, (x, y, s) in enumerate(((300, 330, 22), (338, 290, 16), (366, 258, 12))):
        z = polyline_mask(W, H, [[(x - s, y - s), (x + s, y - s), (x - s, y + s), (x + s, y + s)]], 4 * s / 22 + 1.5)
        art = over(art, flat(z, "#fbeed3", 0.9))
    prev(art, "pp-moon", bg=NIGHT)
    save(art, f"{OUT}/moon.webp", max_w=220, quality=82)


def bulbs():
    W, H = 800, 120
    art = blank(W, H)
    lp = curve([(10, 20), (200, 52), (400, 30), (600, 52), (790, 20)], 160)
    art, gl = fairy(art, W, H, lp, every=20, r=11)
    art = over(glow_layer(W, H, gl, 9), art)
    prev(art, "pp-bulbs", bg=NIGHT)
    save(art, f"{OUT}/bulbs.webp", max_w=400, quality=82)


def sky():
    W = H = 512
    art = painted_sky(W, H, [(0, NIGHT), (1, NIGHT)], seed=nx(), streak=0.8, grain=0.6)
    art[..., :3] *= (0.93 + 0.1 * fbm(W, H, nx(), 120, 3))[..., None]
    rng = np.random.default_rng(nx())
    pts = [(float(rng.uniform(8, W - 8)), float(rng.uniform(8, H - 8)), float(rng.choice([0.9, 1.3, 1.8], p=[.55, .3, .15]))) for _ in range(70)]
    art = over(art, flat(circles(W, H, pts), "#fff4d8", 0.75))
    sp = np.zeros((H, W), np.float32)
    for _ in range(7):
        x, y = float(rng.uniform(30, W - 30)), float(rng.uniform(30, H - 30))
        sp = np.maximum(sp, fourpoint(W, H, x, y, float(rng.uniform(6, 10)), 0.3))
    art = over(art, flat(gaussian_filter(sp, 0.7), "#ffe7a8", 0.85))
    save_rgb(tileable(art), f"{OUT}/sky.webp", quality=76)


for part in PARTS:
    {"fort": fort, "bear": bear, "popcorn": popcorn, "moon": moon, "bulbs": bulbs, "sky": sky}[part]()
    clear()
