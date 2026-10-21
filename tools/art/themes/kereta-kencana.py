"""Kereta Kencana — keraton grandeur, deep green & gold: gouache-and-foil royal carriage, payung agung, paes-inspired
gold ornament, foil corner, dark velvet tile. Run: python3 -I kereta-kencana.py [part ...]
parts: kereta payung paes corner velvet. Assets -> public/themes/art/kereta-kencana/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *
import _jw_lib as jw

OUT = outdir("kereta-kencana")
PARTS = sys.argv[1:] or ["kereta", "payung", "paes", "corner", "velvet"]
DARK = "#0f2a22"
GREEN, GREEN_D, GREEN_L = "#1d4a3a", "#0d2219", "#2f6b54"
GOLD = "#cfa652"
MAROON = "#6e1a22"


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


if "kereta" in PARTS:
    W, H = 780, 540
    nx = Seq(10100)
    art = blank(W, H)
    shadow = shapes(W, H, [deform(ellipse_pts(400, 505, 330, 18, 20), random.Random(1), 1, 0.03)])
    art = G(art, shadow, "#000000", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=4, feather=6)
    # drawbar + springs (behind)
    bar = strokes(W, H, [(curve([(232, 420), (140, 402), (40, 392)], 20), 7, (0.0, 0.2)),
                         (curve([(232, 420), (250, 380), (290, 360)], 14), 6, None), (curve([(545, 400), (540, 372), (520, 356)], 14), 6, None)])
    art = GP(art, bar, "#3a2a14", seed=nx(), rough=0.8, pad=8)
    art = FO(art, bar * 0.9, GOLD, seed=nx(), emboss=0.6)
    # body (boat-like) + roof dome + finial
    body = shapes(W, H, [[(232, 248), (252, 186), (302, 166), (540, 166), (592, 186), (612, 248), (602, 332), (562, 362), (262, 362), (232, 322)]])
    roof = shapes(W, H, [[(258, 170), (290, 122), (360, 100), (420, 94), (480, 100), (550, 122), (582, 170)]])
    finial = shapes(W, H, [petal_pts(420, 96, 52, 16, -math.pi / 2, n=12), deform(ellipse_pts(420, 96, 16, 9, 12), random.Random(2), 0, 0)])
    art = GP(art, np.maximum(body, roof), GREEN, GREEN_D, seed=nx(), rough=1.4, streak=0.9, pad=12)
    sh = np.clip(gaussian_filter(body, 10) - np.roll(gaussian_filter(body, 10), -14, 0), 0, 1) * body
    art = G(art, sh * 2, GREEN_D, seed=nx(), density=0.55, edge=0.1, bloom=0.2, rough=2)
    hi = np.clip(np.roll(gaussian_filter(roof, 6), 8, 0) - gaussian_filter(roof, 6), 0, 1) * roof * 3
    art = G(art, hi, GREEN_L, seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    # gold work: frames, window, door emblem, roof ribs, garlands, finial
    frame = np.maximum(outline(body, 7), outline(roof, 6))
    win = shapes(W, H, [[(322, 300), (322, 230), (340, 200), (372, 190), (404, 200), (420, 230), (420, 300)], [(444, 300), (444, 230), (462, 200), (494, 190), (526, 200), (544, 230), (544, 300)]])
    win_frame = outline(win, 5)
    art = GP(art, win, "#2d1b10", "#120b06", seed=nx(), rough=0.8, pad=8)
    art = G(art, win * jw.hatch(W, H, 1.2, 6, 0.12, 3), "#8a6a3a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    ribs = strokes(W, H, [(curve([(420, 96), (x, 120), (x + (x - 420) * 0.15, 168)], 16), 3, None) for x in (300, 360, 480, 540)])
    gar = strokes(W, H, [(curve([(270, 178), (330, 196), (420, 182), (510, 196), (570, 178)], 40), 4, None)])
    gar_dots = circles(W, H, [(x, 170 + 12 * math.sin((x - 270) / 300 * math.pi * 2), 4.4) for x in range(276, 570, 22)])
    belt = shapes(W, H, [[(240, 318), (604, 318), (598, 336), (246, 336)]], smooth=False)
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along([(262, 346), (586, 346)], 40)):
        it, lv = jw.lung(x, y, 14, a, 1 if k % 2 else -1); items += it; leaves += lv
    lungs = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    # front & rear sweeping scrolls (lung)
    fscroll = strokes(W, H, [(curve([(240, 250), (190, 232), (150, 200), (150, 168)], 24), 14, (0.0, 0.3)), (spiral_pts(168, 160, 26, 4, math.pi, 1.2, 40, 1), 9, (0.0, 0.5)),
                             (curve([(236, 300), (180, 300), (150, 278)], 18), 8, (0.0, 0.4))])
    rscroll = strokes(W, H, [(curve([(606, 250), (650, 226), (680, 196), (676, 164)], 24), 13, (0.0, 0.3)), (spiral_pts(660, 158, 24, 4, 0, 1.2, 40, -1), 9, (0.0, 0.5))])
    seat = shapes(W, H, [[(150, 214), (210, 206), (226, 236), (160, 240)]])
    gold = np.maximum.reduce([frame, win_frame, ribs, gar, gar_dots, belt, lungs * 0.95, fscroll, rscroll, finial, seat * 0.9])
    emb = circles(W, H, [(420, 262, 20)])
    art = FO(art, gold, GOLD, seed=nx(), emboss=0.75, sparkle=0.16)
    art = FO(art, ring(W, H, 420, 262, 22, 5), GOLD, seed=nx(), emboss=0.8)
    art = GP(art, circles(W, H, [(420, 262, 15)]), MAROON, "#3e0d12", seed=nx(), rough=0.6, pad=6)
    # wheels
    for (cx, cy, r) in [(545, 404), (232, 424)] and [(545, 404, 96), (232, 424, 76)]:
        sp = strokes(W, H, [([(cx, cy), (cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9)], 4.5, None) for a in [k * math.tau / 14 for k in range(14)]])
        art = GP(art, sp, MAROON, "#40101a", seed=nx(), rough=0.6, pad=8)
        art = FO(art, np.maximum.reduce([ring(W, H, cx, cy, r, 13), ring(W, H, cx, cy, r * 0.78, 3), circles(W, H, [(cx, cy, r * 0.2)])]), GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
        art = GP(art, circles(W, H, [(cx, cy, r * 0.08)]), GREEN_D, seed=nx(), rough=0.4, pad=6)
    preview(art, "kk-kereta", bg=DARK)
    save(art, f"{OUT}/kereta.webp", max_w=640, quality=82)

if "payung" in PARTS:
    # payung agung: tiered canopy (gold with green band and fringe), finial, long pole
    W, H = 300, 700
    nx = Seq(10200); cx = 150
    pole = strokes(W, H, [([(cx, 110), (cx, 690)], 7, None)])
    tiers = []
    for (y0, w0, w1, h) in [(170, 140, 96, 44), (128, 104, 60, 40), (92, 66, 26, 34)]:
        tiers.append([(cx - w0, y0), (cx - w1, y0 - h), (cx + w1, y0 - h), (cx + w0, y0), (cx + w0 * 0.98, y0 + 8), (cx - w0 * 0.98, y0 + 8)])
    canopy = shapes(W, H, tiers)
    band = shapes(W, H, [[(cx - 136, 160), (cx + 136, 160), (cx + 140, 176), (cx - 140, 176)]], smooth=False)
    fringe = []
    for k in range(-13, 14):
        x = cx + k * 10.5
        fringe.append(([(x, 176), (x, 196 + 6 * (k % 2))], 3, (0.0, 0.5)))
    fr = strokes(W, H, fringe)
    tassel = circles(W, H, [(cx + k * 10.5, 200 + 6 * (k % 2), 3.2) for k in range(-13, 14)])
    fin = shapes(W, H, [petal_pts(cx, 60, 44, 12, -math.pi / 2, n=12)]) + circles(W, H, [(cx, 60, 9)])
    art = blank(W, H)
    art = GP(art, pole, "#5a3c1e", "#2e1d0e", seed=nx(), rough=0.6, pad=8)
    art = FO(art, strokes(W, H, [([(cx, 112), (cx, 690)], 2, None)]), GOLD, seed=nx())
    art = FO(art, canopy, GOLD, seed=nx(), emboss=0.75, sparkle=0.14)
    art = G(art, canopy * jw.hatch(W, H, 1.57, 8, 0.08, 5), "#8a6526", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5)
    art = GP(art, band, GREEN, GREEN_D, seed=nx(), rough=0.6, pad=6)
    art = FO(art, np.clip(fin, 0, 1), GOLD, seed=nx(), emboss=0.8)
    art = FO(art, np.maximum(fr, tassel), "#e2c27a", seed=nx(), emboss=0.4)
    preview(art, "kk-payung", bg=DARK)
    save(art, f"{OUT}/payung.webp", max_w=200, quality=82)

if "paes" in PARTS:
    # paes-inspired crest: central gajahan point flanked by pengapit & penitis scallops, gold outline on deep green, small cundhuk
    W, H = 560, 200
    nx = Seq(10300); cx = W / 2
    shapes_ = []
    for (x, w, h) in [(cx, 74, 150), (cx - 96, 42, 96), (cx + 96, 42, 96), (cx - 168, 30, 66), (cx + 168, 30, 66), (cx - 226, 20, 40), (cx + 226, 20, 40)]:
        shapes_.append([(x - w, 190), (x - w * 0.9, 190 - h * 0.45), (x - w * 0.5, 190 - h * 0.85), (x, 190 - h), (x + w * 0.5, 190 - h * 0.85), (x + w * 0.9, 190 - h * 0.45), (x + w, 190)])
    m = shapes(W, H, shapes_)
    art = blank(W, H)
    art = GP(art, m, GREEN_D, "#06140f", seed=nx(), rough=1.0, pad=10)
    art = FO(art, outline(m, 5), GOLD, seed=nx(), emboss=0.6, sparkle=0.1)
    dots_ = []
    for p in shapes_:
        for t in range(1, 6):
            q = p[t]
            dots_.append((q[0], q[1] + 12, 2.2))
    art = FO(art, circles(W, H, dots_), "#e7cd8a", seed=nx())
    preview(art, "kk-paes", bg=DARK)
    save(art, f"{OUT}/paes.webp", max_w=360, quality=84)

if "corner" in PARTS:
    W, H = 300, 300
    nx = Seq(10400)
    items, leaves = [], []
    path = [(14, 290), (14, 60), (30, 30), (60, 14), (290, 14)]
    for k, (x, y, a) in enumerate(jw.along(curve(path, 60), 34)):
        it, lv = jw.lung(x, y, 18, a, 1 if k % 2 else -1); items += it; leaves += lv
    it, lv = jw.lung(54, 54, 34, -math.pi / 4, 1); items += it; leaves += lv
    m = np.maximum(strokes(W, H, items + [(curve(path, 60), 2.4, None)]), shapes(W, H, leaves))
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    preview(art, "kk-corner", bg=DARK)
    save(art, f"{OUT}/corner.webp", max_w=160, quality=84)

if "velvet" in PARTS:
    n = 256
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#12302a"), np.float32)
    v = wrap_noise(n, n, 3, 2.0) * 0.5 + wrap_noise(n, n, 4, 18) * 0.5
    base *= (0.8 + 0.4 * v)[..., None]
    art = np.concatenate([base, np.ones((n, n, 1), np.float32)], -1)
    save_full(art, f"{OUT}/velvet.webp", quality=70)
