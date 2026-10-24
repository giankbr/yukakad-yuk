"""Gamelan — a bronze gamelan set in a Javanese pendopo at night: gong ageng hanging in a carved red-lacquer gayor with
gold leaf, bonang kettles on their rancakan, a saron, a kendang. Gouache + foil + painted bronze.
Run: python3 -I gamelan.py [part ...]  parts: gong bonang saron kendang pencu divider pendopo"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q4_lib import *

OUT = outdir("gamelan")
PARTS = sys.argv[1:] or ["gong", "bonang", "saron", "kendang", "pencu", "divider", "pendopo"]
NIGHT = "#1a110d"
LAC, LAC_D, LAC_L = "#8f2417", "#4e100a", "#b8442a"
GOLD = "#d2a453"
BR, BR_L, BR_D = "#a06c2e", "#f0cc84", "#3b2210"
PAT = "#5f8f78"


def bronze_kettle(art, W, H, cx, cy, rx, ry, nx, boss=0.34, depth=1.0):
    """A bonang/kenong kettle in 3/4 view: deep side wall, flat top with a shoulder ring and a raised boss (pencu)."""
    dh = ry * 2.1 * depth
    side = shapes(W, H, [[(cx - rx, cy), (cx - rx * 0.97, cy + dh * 0.6), (cx - rx * 0.86, cy + dh), (cx, cy + dh + ry * 0.55),
                          (cx + rx * 0.86, cy + dh), (cx + rx * 0.97, cy + dh * 0.6), (cx + rx, cy)]])
    art = shadow(art, side, "#0e0603", blur=4, strength=0.5, dx=4, dy=6)
    art = SH(art, side, "#74441a", "#e3a85a", "#1e0f06", cx - rx * 0.35, cy + dh * 0.4, rx * 1.25, dh * 1.6, nx(),
             light=(-0.75, -0.1), spec=0.5, hammer=0.06, rough=0.6)
    top = ellipses(W, H, [(cx, cy, rx, ry, 0)])
    art = SH(art, top, "#94602a", "#efc47c", "#4a2a10", cx + rx * 0.2, cy + ry * 0.4, rx * 1.6, ry * 2.2, nx(),
             light=(-0.5, -0.7), spec=0.0, hammer=0.05, rough=0.5)
    rim = np.clip(top - ellipses(W, H, [(cx, cy - ry * 0.06, rx * 0.95, ry * 0.86, 0)]), 0, 1)
    art = T(art, rim * (np.mgrid[0:H, 0:W][0] > cy).astype(np.float32), "#fff0c4", 0.45, 0.6)
    sh = np.clip(ellipses(W, H, [(cx, cy, rx * 0.66, ry * 0.66, 0)]) - ellipses(W, H, [(cx, cy - ry * 0.05, rx * 0.6, ry * 0.58, 0)]), 0, 1)
    art = T(art, sh, "#3a2210", 0.55, 0.6)
    bx, by, br_ = cx, cy - ry * 0.2, rx * boss
    bm = ellipses(W, H, [(bx, by, br_, br_ * 0.86, 0)])
    art = shadow(art, bm, "#1a0c04", blur=3, strength=0.55, dx=3, dy=4)
    art = SH(art, bm, "#b07a36", "#fff2c8", "#2a1608", bx + 2, by + 2, br_, br_ * 0.86, nx(), light=(-0.5, -0.65), spec=0.85, rough=0.4)
    return art


if "gong" in PARTS:
    W, H = 720, 820
    nx = Seq(20100)
    rng = random.Random(4)
    art = blank(W, H)
    # ---- gayor (frame): posts, crossbar, crest, feet
    postL = rect(W, H, 64, 150, 112, 770, 6); postR = rect(W, H, 608, 150, 656, 770, 6)
    feet = np.maximum(rect(W, H, 30, 742, 150, 792, 10), rect(W, H, 570, 742, 690, 792, 10))
    bar = rect(W, H, 26, 118, 694, 176, 8)
    crest = shapes(W, H, [[(170, 122), (230, 92), (290, 66), (330, 30), (360, 10), (390, 30), (430, 66), (490, 92), (550, 122)]])
    frame = np.maximum.reduce([postL, postR, feet, bar, crest])
    art = shadow(art, frame, "#000000", blur=10, strength=0.35, dx=6, dy=8)
    # carved lung-lungan on the crossbar + crest, simple fluting on posts
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along([(40, 148), (680, 148)], 36)):
        it, lv = jw.lung(x, y, 21, a, 1 if k % 2 else -1); items += it; leaves += lv
    for side in (-1, 1):
        for k in range(4):
            x = 360 + side * (36 + k * 44)
            it, lv = jw.lung(x, 100 - (3 - k) * 12 + k * 3, 26 - k * 3, -side * 0.35, side); items += it; leaves += lv
    items.append((jw.spiral_pts(360, 46, 22, 3, -math.pi / 2, 1.2, 40, 1), 8, (0.0, 0.5)))
    for x in (88, 632):
        for k, (px, py, a) in enumerate(jw.along([(x, 206), (x, 724)], 40)):
            it, lv = jw.lung(px, py, 17, math.pi / 2, 1 if k % 2 else -1); items += it; leaves += lv
    art = over(art, carve(W, H, frame, items, leaves, nx, base=LAC, light=LAC_L, dark=LAC_D, gold=GOLD, gold_amt=0.72, seed=41))
    # gold trims (foil) on bar edges and post capitals
    trims = np.maximum.reduce([rect(W, H, 26, 170, 694, 177, 3), rect(W, H, 26, 117, 694, 124, 3),
                               rect(W, H, 56, 178, 120, 196, 4), rect(W, H, 600, 178, 664, 196, 4),
                               rect(W, H, 56, 726, 120, 742, 4), rect(W, H, 600, 726, 664, 742, 4)])
    fin = shapes(W, H, [petal_pts(360, 40, 46, 16, -math.pi / 2, n=12)])
    art = FO(art, np.maximum(trims, fin), GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    clear()
    # ---- cords (red, twisted) from the bar to the gong's ears
    cords = strokes(W, H, [(curve([(290, 176), (300, 228), (318, 268)], 16), 7, None), (curve([(430, 176), (420, 228), (402, 268)], 16), 7, None)])
    art = GP(art, cords, "#a8321f", "#5c140c", seed=nx(), rough=0.6, streak=1.2, pad=6)
    tw = strokes(W, H, [([(296 + t * 0.26, 184 + t * 1.0), (302 + t * 0.26, 190 + t * 1.0)], 2, None) for t in range(0, 80, 9)] +
                 [([(424 - t * 0.26, 184 + t * 1.0), (418 - t * 0.26, 190 + t * 1.0)], 2, None) for t in range(0, 80, 9)])
    art = T(art, tw, "#3a0b06", 0.6)
    # ---- the gong ageng
    cx, cy, R = 360, 490, 226
    disc = circles(W, H, [(cx, cy, R)])
    art = shadow(art, disc, "#000000", blur=16, strength=0.55, dx=10, dy=14)
    art = SH(art, disc, BR, BR_L, BR_D, cx - 20, cy - 20, R * 1.05, R * 1.05, nx(), light=(-0.55, -0.62), spec=0.35, hammer=0.18)
    face = circles(W, H, [(cx, cy, R * 0.84)])
    art = SH(art, face, "#8f5d27", "#e2b76a", "#2e1808", cx + 30, cy + 30, R * 1.5, R * 1.5, nx(), light=(-0.5, -0.66), spec=0.0, hammer=0.1)
    # lathe texture: fine concentric streaks across the whole disc
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr_ = np.hypot(xx - cx, yy - cy)
    lathe = np.sin(rr_ * 1.7 + (fbm(W, H, 91, 40, 2) - 0.5) * 6) * 0.5 + np.sin(rr_ * 0.31) * 0.5
    art[..., :3] *= (1 + 0.045 * lathe * disc)[..., None]
    # shadow side (lower right) glazed darker, warm bounce on the lower-left rim
    dk = disc * np.clip(((xx - cx) * 0.6 + (yy - cy) * 0.8) / R, 0, 1) ** 1.4
    art = over(art, tint(gaussian_filter(dk, 6), "#24110a", 0.62))
    warm = disc * np.clip(((cx - xx) * 0.3 + (cy - yy) * 0.9) / R, 0, 1) ** 2
    art = over(art, tint(gaussian_filter(warm, 10), "#ffd890", 0.22))
    # lathe rings (hand-painted concentric strokes)
    for k, rr in enumerate([R * 0.84, R * 0.62, R * 0.45, R * 0.3]):
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx, cy, rr, a0, a0 + math.tau * rng.uniform(0.7, 0.95), 90)
        art = G(art, stroke_mask(W, H, pts, 2.2 if k == 0 else 1.5), BR_D, seed=nx(), density=0.55 if k == 0 else 0.35, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    hi = stroke_mask(W, H, arc_pts(cx, cy, R * 0.93, math.pi * 1.05, math.pi * 1.55, 40), 9)
    art = OV(art, hi, lambda m: tint(gaussian_filter(m, 2.5), "#fff0c8", 0.6))
    hi2 = stroke_mask(W, H, arc_pts(cx, cy, R * 0.86, math.pi * 0.1, math.pi * 0.35, 20), 4)
    art = OV(art, hi2, lambda m: tint(gaussian_filter(m, 2), "#f6d996", 0.35))
    # verdigris patina near the lower rim
    pat = ring(W, H, cx, cy, R * 0.98, 30) * np.clip((fbm(W, H, 77, 26, 3) - 0.55) * 4, 0, 1)
    art = G(art, pat, PAT, "#3f6b5a", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=2)
    # boss (pencu)
    bm = circles(W, H, [(cx, cy, 52)])
    art = shadow(art, bm, "#1a0c04", blur=6, strength=0.6, dx=6, dy=8)
    art = SH(art, bm, "#b37a32", "#fff1c8", "#2a1608", cx + 4, cy + 4, 54, 54, nx(), light=(-0.5, -0.66), spec=0.9)
    clear()
    preview(art, "gm-gong", bg=NIGHT)
    save(art, f"{OUT}/gong.webp", max_w=560, quality=80)

if "bonang" in PARTS:
    W, H = 980, 380
    nx = Seq(20500)
    art = blank(W, H)
    # rancakan: long low red-lacquer box with gold carving, two string rows hold the kettles
    box = shapes(W, H, [[(30, 214), (950, 214), (968, 236), (962, 320), (18, 320), (12, 236)]], smooth=False)
    legs = np.maximum.reduce([rect(W, H, 40, 316, 92, 362, 6), rect(W, H, 888, 316, 940, 362, 6), rect(W, H, 466, 316, 514, 352, 6)])
    art = shadow(art, np.maximum(box, legs), "#000000", blur=10, strength=0.45, dx=4, dy=10)
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along([(30, 268), (950, 268)], 30)):
        it, lv = jw.lung(x, y, 19, a, 1 if k % 2 else -1); items += it; leaves += lv
    art = over(art, carve(W, H, np.maximum(box, legs), items, leaves, nx, base=LAC, light=LAC_L, dark=LAC_D, gold=GOLD, gold_amt=0.7, seed=43))
    art = FO(art, np.maximum(rect(W, H, 14, 212, 966, 222, 3), rect(W, H, 14, 312, 966, 320, 3)), GOLD, seed=nx(), emboss=0.7)
    clear()
    # back row (smaller, higher), front row (bigger, lower)
    for row, (y, rx, n, x0, x1) in enumerate([(120, 50, 7, 120, 860), (176, 58, 7, 84, 896)]):
        for i in range(n):
            x = x0 + (x1 - x0) * i / (n - 1) + random.Random(i + row * 10).gauss(0, 3)
            art = bronze_kettle(art, W, H, x, y, rx, rx * 0.36, nx)
        clear()
    preview(art, "gm-bonang", bg=NIGHT)
    save(art, f"{OUT}/bonang.webp", max_w=760, quality=78)

if "saron" in PARTS:
    W, H = 800, 300
    nx = Seq(20900)
    art = blank(W, H)
    base = shapes(W, H, [[(40, 150), (760, 150), (790, 196), (770, 262), (30, 262), (10, 196)]], smooth=False)
    art = shadow(art, base, "#000000", blur=10, strength=0.45, dx=4, dy=10)
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along([(40, 210), (760, 210)], 32)):
        it, lv = jw.lung(x, y, 20, a, 1 if k % 2 else -1); items += it; leaves += lv
    art = over(art, carve(W, H, base, items, leaves, nx, base=LAC, light=LAC_L, dark=LAC_D, gold=GOLD, gold_amt=0.7, seed=47))
    art = FO(art, rect(W, H, 12, 148, 788, 158, 3), GOLD, seed=nx(), emboss=0.7)
    # seven bronze bars (wilahan) resting over the trough, slightly decreasing
    for i in range(7):
        x = 92 + i * 102; w2 = 40 - i * 1.4; top = 76 + i * 3; bot = 162
        bar = rect(W, H, x - w2, top, x + w2, bot, 10)
        art = shadow(art, bar, "#140804", blur=4, strength=0.6, dx=3, dy=5)
        art = SH(art, bar, "#8a5a24", "#eebf74", "#26140a", x - 6, (top + bot) / 2 - 6, w2 * 1.5, (bot - top) * 1.1, nx(), light=(-0.6, -0.5), spec=0.45, hammer=0.04, rough=0.5)
        art = T(art, rect(W, H, x - w2 + 4, top + 3, x + w2 - 4, top + 7, 2), "#fff0c4", 0.4, 1)
        pins = circles(W, H, [(x, top + 12, 3.2), (x, bot - 12, 3.2)])
        art = T(art, pins, "#2a160a", 0.8)
    clear()
    # tabuh (mallet) lying across
    mal = strokes(W, H, [(curve([(520, 60), (640, 40), (760, 26)], 10), 7, None)])
    head = ellipses(W, H, [(520, 60, 26, 18, -10)])
    art = shadow(art, np.maximum(mal, head), "#000000", blur=4, strength=0.4, dx=3, dy=5)
    art = GP(art, mal, "#7a4a28", "#4a2a14", seed=nx(), rough=0.6, streak=1.2)
    art = SH(art, head, "#b78a52", "#e8c896", "#5a3a1a", 514, 54, 26, 18, nx(), light=(-0.5, -0.7), spec=0.2)
    preview(art, "gm-saron", bg=NIGHT)
    save(art, f"{OUT}/saron.webp", max_w=620, quality=78)

if "kendang" in PARTS:
    W, H = 460, 360
    nx = Seq(21300)
    art = blank(W, H)
    # stand (plangkan): two red-lacquer cradles
    stand = np.maximum.reduce([shapes(W, H, [[(80, 250), (140, 210), (200, 250), (192, 320), (88, 320)]]),
                               shapes(W, H, [[(270, 250), (330, 214), (390, 250), (382, 320), (278, 320)]]), rect(W, H, 70, 300, 400, 330, 6)])
    art = shadow(art, stand, "#000000", blur=8, strength=0.45, dx=4, dy=8)
    art = GP(art, stand, LAC, LAC_D, seed=nx(), rough=1.2, streak=1)
    art = FO(art, rect(W, H, 70, 298, 400, 306, 3), GOLD, seed=nx(), emboss=0.6)
    # body: barrel, slightly asymmetric (big head left)
    body = shapes(W, H, [[(60, 130), (120, 108), (240, 98), (340, 110), (400, 128), (404, 214), (340, 236), (240, 246), (120, 236), (60, 216)]])
    art = shadow(art, body, "#000000", blur=10, strength=0.5, dx=6, dy=10)
    art = SH(art, body, "#7b3f1c", "#c98a50", "#2f150a", 220, 140, 230, 110, nx(), light=(-0.3, -0.8), spec=0.3)
    # heads (leather)
    hl = ellipses(W, H, [(64, 173, 24, 58, 0)]); hr = ellipses(W, H, [(400, 171, 18, 46, 0)])
    art = SH(art, np.maximum(hl, hr), "#d8bf8f", "#f4e4c0", "#8a6a40", 60, 160, 30, 70, nx(), light=(-0.7, -0.5), spec=0.0)
    # rawhide lacing (Y lines) + rings
    lace = []
    for k in range(9):
        y = 128 + k * 11
        lace.append(([(70, y), (232, 172 + (k - 4) * 3)], 2.2, None)); lace.append(([(232, 172 + (k - 4) * 3), (396, 132 + k * 9)], 2.0, None))
    art = T(art, strokes(W, H, lace), "#e9d2a2", 0.85)
    rings = circles(W, H, [(232, 172 + (k - 4) * 3, 4) for k in range(9)])
    art = T(art, rings, "#3a1e0e", 0.8)
    art = FO(art, np.maximum(rect(W, H, 226, 100, 238, 244, 4), np.zeros((H, W), np.float32)), GOLD, seed=nx(), emboss=0.6)
    preview(art, "gm-kendang", bg=NIGHT)
    save(art, f"{OUT}/kendang.webp", max_w=360, quality=80)

if "pencu" in PARTS:
    W, H = 200, 160
    nx = Seq(21700)
    art = bronze_kettle(blank(W, H), W, H, 100, 50, 80, 30, nx, boss=0.36)
    preview(art, "gm-pencu", bg=NIGHT)
    save(art, f"{OUT}/pencu.webp", max_w=130, quality=84)

if "divider" in PARTS:
    W, H = 640, 70
    nx = Seq(21900)
    art = blank(W, H)
    rod = np.maximum(strokes(W, H, [(curve([(20, 36), (200, 34), (290, 35)], 20), 3, (0.4, 0.0))]),
                     strokes(W, H, [(curve([(350, 35), (440, 34), (620, 36)], 20), 3, (0.0, 0.4))]))
    art = FO(art, rod, GOLD, seed=nx(), emboss=0.6)
    for x, r in [(250, 7), (390, 7), (226, 4.5), (414, 4.5)]:
        art = SH(art, circles(W, H, [(x, 35, r)]), BR, BR_L, BR_D, x, 35, r, r, nx(), spec=0.6)
    bm = circles(W, H, [(320, 35, 22)])
    art = SH(art, bm, BR, BR_L, BR_D, 320, 35, 22, 22, nx(), spec=0.3, hammer=0.2)
    art = SH(art, circles(W, H, [(320, 35, 9)]), BR, "#fff1c8", BR_D, 320, 35, 9, 9, nx(), spec=0.9)
    preview(art, "gm-divider", bg="#f3e6cf")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)

if "pendopo" in PARTS:
    # night pendopo interior: dark painted backdrop, warm lamp light, tumpang sari ceiling beams, saka pillars
    W, H = 780, 1100
    nx = Seq(22300)
    art = painted_sky(W, H, [(0, "#24150f"), (0.35, "#3a2216"), (0.62, "#2a1810"), (1, "#140b08")], seed=5, streak=0.9, grain=0.15)
    glowm = ellipses(W, H, [(390, 470, 300, 240, 0)])
    art = over(art, glow(glowm, "#b8702e", radius=70, strength=0.2))
    # tumpang sari: stepped ceiling beams (perspective trapezoids)
    for k in range(5):
        y = 40 + k * 46; inset = 40 + k * 70
        beam = shapes(W, H, [[(inset, y), (W - inset, y), (W - inset - 22, y + 24), (inset + 22, y + 24)]], smooth=False)
        art = GP(art, beam, mix("#5a3420", "#2a160c", k / 6), "#20110a", seed=nx(), rough=1.4, streak=1.2)
        art = G(art, rect(W, H, inset + 20, y + 20, W - inset - 20, y + 25, 2), "#c9963f", seed=nx(), density=0.45, edge=0.3, bloom=0.1, rough=1)
    # saka guru pillars (left and right, close to camera), with umpak bases
    for x0, x1 in [(-10, 66), (714, 790), (150, 186), (594, 630)]:
        near = x1 - x0 > 50
        col = rect(W, H, x0, 230 if not near else 0, x1, 1040 if near else 900, 2)
        art = GP(art, col, "#3c2214" if near else "#4a2b19", "#1c0f08", seed=nx(), rough=1.0, streak=1.4)
        lit = rect(W, H, x0 + (x1 - x0) * 0.62, 230 if not near else 0, x0 + (x1 - x0) * 0.8, 1040 if near else 900, 2)
        art = G(art, lit, "#b46a32", seed=nx(), density=0.28, edge=0.1, bloom=0.2, rough=1, feather=3)
        umpak = shapes(W, H, [[(x0 - 14, (1040 if near else 900)), (x1 + 14, (1040 if near else 900)), (x1 + 4, (1080 if near else 930)), (x0 - 4, (1080 if near else 930))]], smooth=False)
        art = GP(art, umpak, "#4a3a30", "#231a14", seed=nx(), rough=1.2)
    # floor: polished tiles catching light
    floor = rect(W, H, 0, 900, W, H)
    art = G(art, floor, "#5a3420", "#2a160c", seed=nx(), density=0.5, edge=0.05, bloom=0.2, rough=2, feather=4)
    refl = ellipses(W, H, [(390, 960, 260, 50, 0)])
    art = over(art, glow(refl, "#e0a050", radius=30, strength=0.18))
    # hanging lamps (blencong-like oil lamps) as warm points
    for x, y in [(250, 300), (530, 300)]:
        art = over(art, glow(circles(W, H, [(x, y, 10)]), "#ffc070", radius=26, strength=0.6))
        art = T(art, circles(W, H, [(x, y, 5)]), "#fff0c0", 0.95, 1)
        art = T(art, lines(W, H, [((x, 260), (x, y - 6))], 1.4), "#120a06", 0.8)
    art = vignette(add_grain(art, 3, 0.018), 0.4)
    clear()
    on = to_image(art).convert("RGB"); on.save(f"{PREV}/gm-pendopo.png")
    save_opaque(art, f"{OUT}/pendopo.webp", size=(520, 733), quality=66)
