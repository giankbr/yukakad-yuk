"""Ultah Polisi — kids' birthday, little police officer party in storybook gouache: friendly patrol car, generic
star badge (no real insignia), traffic light, cone, whistle, city street with a zebra crossing.
Run: python3 -I ultah-polisi.py [street car badge light cone whistle divider]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q5_lib import *

OUT = outdir("ultah-polisi")
PARTS = sys.argv[1:] or ["street", "car", "badge", "light", "cone", "whistle", "divider"]
NAVY, BLUE, SKY, YEL, RED, WHITE, ASPH = "#1d3a6e", "#2f6fd0", "#bfe3f7", "#ffc93c", "#e5483b", "#f8f6ef", "#4a4f5c"
GOLD, GOLD_D = "#f2b632", "#b97c12"


def g(art, m, c1, c2=None, **k):
    k.setdefault("rough", 1.2); k.setdefault("streak", 1.1)
    return GP(art, m, c1, c2, seed=NX(), **k)


def rr(W, H, x0, y0, x1, y1, r):
    return rrect_mask(W, H, x0, y0, x1, y1, r)


def shade_bottom(art, m, col, amt=0.35, frac=0.45):
    ys = np.where(m.max(1) > 0.5)[0]
    if len(ys) == 0:
        return art
    y0, y1 = ys.min(), ys.max()
    yy = np.arange(m.shape[0], dtype=np.float32)[:, None]
    k = np.clip((yy - (y0 + (y1 - y0) * (1 - frac))) / ((y1 - y0) * frac + 1), 0, 1)
    return g(art, m * k, col, density=amt, rough=0.6)


NX = Seq(60000)

if "street" in PARTS:
    W, H = 700, 1400
    rng = random.Random(61)
    art = painted_sky(W, H, [(0, "#9fd3f2"), (0.45, "#cdeaf8"), (0.62, "#e6f4fa"), (1, "#e6f4fa")], seed=6, streak=0.4, grain=0.4)
    # clouds
    cl = []
    for (x, y, s) in [(110, 160, 1.0), (560, 110, 0.8), (420, 330, 0.7), (60, 520, 0.6), (640, 560, 0.75)]:
        for j in range(5):
            cl.append((x + (j - 2) * 34 * s + rng.uniform(-6, 6), y + rng.uniform(-10, 8) - (16 * s if j in (1, 2, 3) else 0), (30 + rng.uniform(0, 16)) * s))
    art = g(art, circles(W, H, cl), "#ffffff", "#f2f7fb", rough=2.2, density=0.95)
    # buildings
    x = -30; k = 0
    cols = ["#7cc7c0", "#f6b38b", "#ffd76a", "#b9a6e0", "#8fb8ee", "#f39aa0"]
    blds = []
    while x < W + 20:
        bw = rng.uniform(110, 170); bh = rng.uniform(220, 380)
        blds.append((x, bw, bh, cols[k % len(cols)])); x += bw - 6; k += 1
    for (bx, bw, bh, col) in blds:
        top = 1150 - bh
        m = rr(W, H, bx, top, bx + bw, 1160, 10)
        art = g(art, m, col, mix(col, "#000000", .12))
        art = g(art, shapes(W, H, [rect(bx - 6, top - 10, bx + bw + 6, top + 8)], smooth=False), mix(col, "#000000", .25), rough=0.8)
        wins = []
        for wy in np.arange(top + 30, 1080, 58):
            for wx in np.arange(bx + 18, bx + bw - 34, 40):
                wins.append(rr(W, H, wx, wy, wx + 24, wy + 32, 5))
        if wins:
            wm = np.maximum.reduce(wins)
            art = g(art, wm, "#fff6d8", "#d9ecf5", rough=0.6)
            art = g(art, np.clip(wm - np.roll(np.roll(wm, 5, 0), 5, 1), 0, 1), "#ffffff", rough=0.4, density=0.7)
        door = rr(W, H, bx + bw / 2 - 18, 1092, bx + bw / 2 + 18, 1160, 16)
        art = g(art, door, mix(col, "#2a2a40", .55), rough=0.6)
        clear()
    # awning stripes on one shop
    bx, bw, *_ = blds[2]
    aw = shapes(W, H, [[(bx + 8, 1060), (bx + bw - 8, 1060), (bx + bw, 1086), (bx, 1086)]], smooth=False)
    stripes = aw * (((np.arange(W)[None, :] - bx) // 16) % 2 == 0)
    art = g(art, aw, "#ffffff", rough=0.6)
    art = g(art, stripes.astype(np.float32), RED, rough=0.6)
    # round trees
    for tx in [60, 250, 470, 650]:
        art = g(art, shapes(W, H, [rect(tx - 6, 1100, tx + 6, 1170)], smooth=False), "#7a5432", rough=0.6)
        art = g(art, circles(W, H, [(tx, 1080, 44), (tx - 28, 1100, 30), (tx + 30, 1098, 32)]), "#5dbb63", "#3f9a4d", rough=2.0)
        art = g(art, circles(W, H, [(tx - 14, 1066, 14)]), "#86d389", rough=1.0, density=0.7)
    # sidewalk + curb
    art = g(art, shapes(W, H, [rect(-10, 1160, W + 10, 1215)], smooth=False), "#e4ddcf", "#d6cdbb", rough=0.8)
    tiles = strokes(W, H, [([(x, 1162), (x - 8, 1212)], 2, None) for x in range(20, W, 44)])
    art = g(art, tiles, "#c2b8a4", rough=0.4, density=0.6)
    art = g(art, shapes(W, H, [rect(-10, 1210, W + 10, 1226)], smooth=False), "#b8b1a4", rough=0.6)
    # road, zebra crossing, centre dashes
    art = g(art, shapes(W, H, [rect(-10, 1224, W + 10, H + 10)], smooth=False), ASPH, "#3d424e", rough=0.8, streak=1.6)
    zeb = shapes(W, H, [rect(x, 1236, x + 30, H - 6) for x in range(150, 560, 54)], smooth=False)
    art = g(art, zeb, "#f4f2ea", rough=0.8, dry=0.15)
    dash = shapes(W, H, [rect(x, 1306, x + 50, 1314) for x in list(range(-20, 120, 90)) + list(range(590, W, 90))], smooth=False)
    art = g(art, dash, YEL, rough=0.6)
    art = add_grain(art, 3, 0.03)
    preview(art, "up-street", bg="#000000")
    save_rgb(art, f"{OUT}/street.webp", size=(560, 1120), quality=76)
    clear()

if "car" in PARTS:
    W, H = 720, 360
    art = blank(W, H)
    art = over(art, tint(gaussian_filter(shapes(W, H, [ellipse_pts(360, 318, 300, 16, 20)]), 6), "#000000", 0.35))
    body = rr(W, H, 50, 160, 670, 292, 46)
    cab = shapes(W, H, [[(190, 168), (232, 96), (250, 86), (452, 86), (476, 96), (546, 168)]])
    art = g(art, np.maximum(body, cab), WHITE, "#e9e6dc")
    skirt = body * (np.arange(H)[:, None] > 248)
    art = g(art, skirt.astype(np.float32), NAVY, "#152c55")
    stripe = body * ((np.arange(H)[:, None] > 206) & (np.arange(H)[:, None] < 226))
    art = g(art, stripe.astype(np.float32), BLUE, rough=0.8)
    art = shade_bottom(art, np.maximum(body, cab), "#7d8aa3", amt=0.25)
    wins = [shapes(W, H, [[(236, 160), (262, 104), (346, 104), (346, 160)]]), shapes(W, H, [[(364, 160), (364, 104), (452, 104), (500, 160)]])]
    for wm in wins:
        art = g(art, wm, "#a9d7f2", "#7fb9e0", rough=0.6)
    glint = strokes(W, H, [([(290, 150), (318, 110)], 7, None), ([(400, 150), (428, 110)], 7, None)])
    art = g(art, glint, "#e7f5fd", rough=0.4, density=0.8)
    # door lines + handle
    doors = strokes(W, H, [([(354, 96), (354, 286)], 3, None), ([(232, 168), (232, 286)], 3, None), ([(490, 168), (490, 286)], 3, None)])
    art = g(art, doors, "#b9b6ab", rough=0.4)
    art = g(art, rr(W, H, 300, 178, 330, 186, 4), "#9a978c", rough=0.3)
    art = g(art, rr(W, H, 430, 178, 460, 186, 4), "#9a978c", rough=0.3)
    # gold star on the front door
    st = shapes(W, H, [star_pts(420, 232, 26, 11, 5)], smooth=False)
    art = g(art, st, GOLD, GOLD_D, rough=0.6)
    # light bar (dim; the page adds the flashing glow)
    art = g(art, rr(W, H, 300, 76, 436, 90, 6), "#3b3f4a", rough=0.4)
    art = g(art, rr(W, H, 306, 56, 368, 82, 10), "#e04a4a", "#b83232", rough=0.6)
    art = g(art, rr(W, H, 368, 56, 430, 82, 10), "#3d7de0", "#2c5fb5", rough=0.6)
    art = g(art, rr(W, H, 316, 60, 340, 66, 3), "#ffd0c8", rough=0.3, density=0.7)
    art = g(art, rr(W, H, 378, 60, 402, 66, 3), "#d4e4ff", rough=0.3, density=0.7)
    # lights, bumpers
    art = g(art, rr(W, H, 640, 196, 676, 222, 10), "#ffe27a", "#f6c443", rough=0.5)
    art = g(art, rr(W, H, 44, 196, 66, 222, 8), RED, rough=0.5)
    art = g(art, rr(W, H, 600, 270, 690, 292, 10), "#a9adb7", rough=0.5)
    art = g(art, rr(W, H, 30, 270, 120, 292, 10), "#a9adb7", rough=0.5)
    # wheels
    for cx in (170, 540):
        art = g(art, circles(W, H, [(cx, 292, 56)]), "#3a3b42", rough=0.6)
        art = g(art, circles(W, H, [(cx, 292, 52)]), "#24252b", "#33343c", rough=0.6)
        art = g(art, circles(W, H, [(cx, 292, 26)]), "#c9ccd4", "#a3a8b4", rough=0.4)
        art = g(art, circles(W, H, [(cx, 292, 9)]), "#6c707c", rough=0.3)
        art = g(art, strokes(W, H, [(arc_pts(cx, 292, 40, 3.6, 4.6, 12), 5, None)]), "#5a5c66", rough=0.3, density=0.8)
    # outline ink (storybook)
    sil = np.maximum(body, cab)
    art = g(art, outline(sil, 4), NAVY, rough=0.6, density=0.85)
    preview(art, "up-car", tone="#e6f4fa")
    save(art, f"{OUT}/car.webp", max_w=460, quality=84)
    clear()

if "badge" in PARTS:
    W = H = 320
    cx = cy = 160
    art = blank(W, H)
    st = shapes(W, H, [star_pts(cx, cy, 138, 78, 6)], smooth=False)
    balls = circles(W, H, [(cx + math.cos(-math.pi / 2 + k * math.pi / 3) * 132, cy + math.sin(-math.pi / 2 + k * math.pi / 3) * 132, 17) for k in range(6)])
    sil = np.maximum(st, balls)
    art = over(art, tint(gaussian_filter(np.roll(np.roll(sil, 8, 0), 5, 1), 6), "#000000", 0.3))
    art = g(art, sil, GOLD, "#f7cf5c", rough=1.0)
    # bevel: darker lower-right faces of each arm
    for k in range(6):
        a = -math.pi / 2 + k * math.pi / 3
        tip = (cx + math.cos(a) * 138, cy + math.sin(a) * 138)
        side = (cx + math.cos(a + math.pi / 6) * 78, cy + math.sin(a + math.pi / 6) * 78)
        art = g(art, shapes(W, H, [[(cx, cy), tip, side]], smooth=False), GOLD_D, "#d39a22", rough=0.5, density=0.55)
    art = g(art, circles(W, H, [(cx, cy, 70)]), "#e3a62a", rough=0.6)
    art = g(art, circles(W, H, [(cx, cy, 60)]), NAVY, "#24467f", rough=0.6)
    art = g(art, ring(W, H, cx, cy, 52, 3), "#f7cf5c", rough=0.3)
    hl = strokes(W, H, [(arc_pts(cx, cy, 116, 3.7, 4.3, 10), 6, None)])
    art = g(art, hl, "#fff1b8", rough=0.4, density=0.75)
    art = g(art, outline(sil, 3), "#8a5a0c", rough=0.5, density=0.8)
    preview(art, "up-badge", tone="#e6f4fa")
    save(art, f"{OUT}/badge.webp", max_w=220, quality=84)
    clear()

if "light" in PARTS:
    W, H = 200, 560
    art = blank(W, H)
    art = g(art, rr(W, H, 88, 300, 112, 560, 8), "#5b6170", "#454a56", rough=0.6)
    house = rr(W, H, 40, 20, 160, 320, 26)
    art = g(art, house, "#2b3140", "#1f2430", rough=0.8)
    for k, (c1, c2) in enumerate([("#8f2f2a", "#6f201c"), ("#9b7a22", "#7a5d14"), ("#2f7a45", "#215a32")]):
        y = 70 + k * 92
        hood = shapes(W, H, [[(56, y - 34), (144, y - 34), (150, y - 20), (50, y - 20)]], smooth=False)
        art = g(art, circles(W, H, [(100, y + 6, 36)]), "#141821", rough=0.5)
        art = g(art, circles(W, H, [(100, y + 6, 31)]), c1, c2, rough=0.5)
        art = g(art, hood, "#3a4152", rough=0.4)
        art = g(art, circles(W, H, [(90, y - 4, 8)]), "#ffffff", rough=0.3, density=0.35)
    art = g(art, outline(house, 3), "#141821", rough=0.4)
    preview(art, "up-light", tone="#e6f4fa")
    save_full(art, f"{OUT}/light.webp", size=(100, 280), quality=84)
    clear()

if "cone" in PARTS:
    W, H = 240, 300
    art = blank(W, H)
    base = rr(W, H, 22, 250, 218, 282, 10)
    art = g(art, base, "#f0642f", "#d64d1f", rough=0.6)
    cone = shapes(W, H, [[(100, 30), (140, 30), (196, 256), (44, 256)]], smooth=False)
    art = g(art, cone, "#ff7a3a", "#e85a24", rough=0.8)
    yy = np.arange(H)[:, None]
    bands = cone * (((yy > 100) & (yy < 128)) | ((yy > 172) & (yy < 202)))
    art = g(art, bands.astype(np.float32), "#ffffff", "#ecebe6", rough=0.5)
    sh = cone * np.clip((np.arange(W)[None, :] - 130) / 60, 0, 1)
    art = g(art, sh, "#b23a14", rough=0.5, density=0.45)
    art = g(art, strokes(W, H, [([(108, 50), (78, 236)], 6, None)]), "#ffb48a", rough=0.4, density=0.7)
    art = g(art, outline(np.maximum(cone, base), 3), "#8a2c0e", rough=0.4, density=0.8)
    preview(art, "up-cone", tone="#e6f4fa")
    save(art, f"{OUT}/cone.webp", max_w=110, quality=84)
    clear()

if "whistle" in PARTS:
    W, H = 320, 220
    art = blank(W, H)
    cord = strokes(W, H, [(curve([(70, 96), (40, 60), (60, 20), (120, 18), (150, 50)], 30), 6, None)])
    art = g(art, cord, RED, "#c23528", rough=0.4)
    ringm = ring(W, H, 78, 100, 16, 6)
    art = g(art, ringm, "#9aa0ab", rough=0.3)
    bodym = np.maximum(circles(W, H, [(150, 140, 58)]), rr(W, H, 150, 82, 296, 132, 12))
    art = g(art, bodym, "#c9ced8", "#9ea5b3", rough=0.8)
    art = shade_bottom(art, bodym, "#5e6676", amt=0.45, frac=0.5)
    art = g(art, rr(W, H, 268, 92, 290, 122, 6), "#2c3140", rough=0.3)
    art = g(art, rr(W, H, 186, 90, 214, 104, 4), "#3a4050", rough=0.3)
    art = g(art, strokes(W, H, [(arc_pts(150, 140, 42, 3.5, 4.6, 12), 8, None), ([(170, 92), (280, 92)], 5, None)]), "#f4f7fb", rough=0.3, density=0.85)
    art = g(art, outline(bodym, 3), "#3a4050", rough=0.4, density=0.8)
    preview(art, "up-whistle", tone="#e6f4fa")
    save(art, f"{OUT}/whistle.webp", max_w=150, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 760, 60
    art = blank(W, H)
    road = rr(W, H, 10, 14, 750, 46, 16)
    art = g(art, road, ASPH, "#3d424e", rough=0.8)
    dash = shapes(W, H, [rect(x, 27, x + 36, 33) for x in range(40, 720, 64)], smooth=False)
    art = g(art, dash, YEL, rough=0.4)
    edge = np.clip(road - inset(road, 4), 0, 1)
    art = g(art, edge, "#f4f2ea", rough=0.3, density=0.8)
    preview(art, "up-divider", tone="#fff8ea")
    save(art, f"{OUT}/divider.webp", max_w=380, quality=84)
    clear()

kb(OUT)
