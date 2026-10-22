"""Khataman Quran — calm green & gold: gouache walnut rehal holding a closed mushaf (plain green cover, foil border and
geometric medallion, no calligraphy), green-glass hanging lantern, foil 8-point star, foil divider, watercolour jasmine
sprig, pale geometric paper tile. Run: python3 -I khataman-quran.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b6_lib import *

OUT = outdir("khataman-quran")
PARTS = sys.argv[1:] or ["rehal", "lantern", "star", "divider", "sprig", "tile"]
GREEN, GREEN_D, GREEN_L = "#24574a", "#123a30", "#3f7a68"
GOLD = "#c9a45a"
WOOD, WOOD_D, WOOD_L = "#875733", "#4d2c17", "#b07b4c"
CREAM = "#f5efe1"

if "rehal" in PARTS:
    W, H = 640, 660
    nx = Seq(20100); rng = random.Random(4)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(322, 618, 250, 22, 20), rng, 1, 0.03)])
    art = G(art, sh, "#3b2a1c", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=4, feather=7)
    # back legs splaying behind (shadowed)
    legs = shapes(W, H, [[(146, 430), (176, 430), (150, 612), (118, 612)], [(464, 430), (494, 430), (522, 612), (490, 612)]], smooth=False)
    art = wood(art, legs, nx, mix(WOOD, WOOD_D, .45), WOOD_D, WOOD, angle=1.45, spacing=7, seed=5)
    # back board with a gently pointed crest
    crest = curve([(150, 168), (200, 150), (262, 120), (300, 92), (320, 70), (340, 92), (378, 120), (440, 150), (490, 168)], 40)
    back = shapes(W, H, [crest + [(500, 300), (510, 440), (130, 440), (140, 300)]], smooth=False)
    art = wood(art, back, nx, WOOD, WOOD_D, WOOD_L, angle=1.5, spacing=10, seed=7)
    # pierced star window in the crest + pale-gold inlay along the crest
    win = shapes(W, H, [star8(320, 126, 24, 15, math.pi / 8)], smooth=False)
    art = GP(art, win, "#2a170b", "#1b0f07", seed=nx(), rough=0.6, pad=6)
    art = FO(art, outline(win, 4), GOLD, seed=nx(), emboss=0.7, sparkle=0.1)
    inlay = strokes(W, H, [(curve([(p[0], p[1] + 16) for p in crest[3:-3]], 40), 3, (0.08, 0.08))])
    art = FO(art, inlay, GOLD, seed=nx(), emboss=0.6, sparkle=0.08)
    # the closed mushaf, leaning on the back board
    page = shapes(W, H, [[(214, 196), (446, 196), (462, 210), (466, 458), (218, 466)]], smooth=False)
    art = GP(art, page, "#efe5cc", "#d8c9a4", seed=nx(), rough=0.8, streak=0.6, pad=8)
    leaves = strokes(W, H, [([(450 + k * 3.2, 208 + k * 2), (454 + k * 3.2, 458)], 0.9, None) for k in range(4)] +
                     [([(222, 458 + k * 2.4), (462, 452 + k * 2.4)], 0.9, None) for k in range(3)])
    art = G(art, leaves * page, "#a8936a", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4, feather=0.3)
    cover = shapes(W, H, [[(200, 186), (444, 186), (450, 448), (204, 456)]], smooth=False)
    art = GP(art, cover, GREEN, GREEN_D, seed=nx(), rough=1.0, streak=0.9, pad=10)
    art = G(art, shade_side(cover, -14, -10, 10), GREEN_D, seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1)
    spine = shapes(W, H, [[(200, 186), (222, 186), (226, 455), (204, 456)]], smooth=False)
    art = G(art, spine, GREEN_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8)
    # foil frame: double border, corner fillers, central geometric medallion (no calligraphy)
    fr = np.maximum(inner_line(cover, 18, 4), inner_line(cover, 30, 2))
    cx, cy = 330, 318
    med = np.maximum.reduce([
        np.clip(shapes(W, H, [star8(cx, cy, 64, 46, math.pi / 8)], smooth=False) - shapes(W, H, [star8(cx, cy, 58, 41, math.pi / 8)], smooth=False), 0, 1),
        ring(W, H, cx, cy, 36, 3), ring(W, H, cx, cy, 24, 2), circles(W, H, [(cx, cy, 8)]),
        shapes(W, H, [star8(cx, cy, 18, 11, 0)], smooth=False) * 0.0,
    ])
    corners = []
    for (x, y, sx, sy) in [(238, 224, 1, 1), (414, 224, -1, 1), (240, 416, 1, -1), (414, 414, -1, -1)]:
        corners.append([(x, y), (x + sx * 34, y), (x, y + sy * 34)])
    cfill = shapes(W, H, corners, smooth=False)
    dots_ = circles(W, H, [(cx + math.cos(a) * 84, cy + math.sin(a) * 84, 2.6) for a in [k * math.pi / 4 for k in range(8)]])
    art = FO(art, np.maximum.reduce([fr, med, cfill * 0.92, dots_]), GOLD, seed=nx(), emboss=0.8, sparkle=0.14)
    # ribbon bookmark tails over the ledge
    rib = shapes(W, H, [[(306, 448), (318, 448), (314, 520), (306, 508), (298, 518)], [(322, 448), (334, 448), (338, 512), (330, 503), (322, 514)]], smooth=False)
    # front ledge + front legs with a pointed-arch opening
    ledge = shapes(W, H, [[(150, 442), (492, 442), (500, 474), (142, 474)]], smooth=False)
    arch = curve([(236, 608), (236, 560), (262, 528), (320, 506), (378, 528), (404, 560), (404, 608)], 30)
    front = np.clip(shapes(W, H, [[(166, 474), (476, 474), (488, 610), (154, 610)]], smooth=False) - shapes(W, H, [arch + [(404, 620), (236, 620)]]), 0, 1)
    art = wood(art, front, nx, mix(WOOD, WOOD_L, .2), WOOD_D, WOOD_L, angle=0.05, spacing=9, seed=9)
    art = wood(art, ledge, nx, WOOD_L, WOOD_D, "#c9935e", angle=0.02, spacing=6, seed=11, grain=0.35)
    art = G(art, shade_side(ledge, 0, -6, 3), WOOD_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
    art = GP(art, rib, "#2f6a57", GREEN_D, seed=nx(), rough=0.6, pad=6)
    art = FO(art, outline(rib, 2) * 0.8, GOLD, seed=nx(), emboss=0.5)
    fwin = shapes(W, H, [star8(320, 488, 0.1, 0.1)], smooth=False)
    art = FO(art, inner_line(front, 10, 2.5), GOLD, seed=nx(), emboss=0.6, sparkle=0.06)
    preview(art, "kq-rehal")
    save(art, f"{OUT}/rehal.webp", max_w=520, quality=82)
    clear()

if "lantern" in PARTS:
    W, H = 260, 560
    nx = Seq(20300); rng = random.Random(8)
    cx = 130
    art = blank(W, H)
    glass = shapes(W, H, [[(cx - 60, 150), (cx - 72, 190), (cx - 72, 318), (cx - 56, 350), (cx + 56, 350), (cx + 72, 318), (cx + 72, 190), (cx + 60, 150)]], smooth=False)
    art = over(art, glow(circles(W, H, [(cx, 260, 70)]), "#ffd98a", radius=40, strength=0.42))
    art = G(art, glass, "#5f9a7e", "#2f6d5a", seed=nx(), density=0.75, edge=0.6, bloom=0.4, rough=2)
    inner = ellipses(W, H, [(cx, 262, 44, 74, 0)])
    art = OV(art, gaussian_filter(inner, 14), lambda m: tint(m, "#ffe3a0", 0.85))
    art = flame(W, H, cx, 290, 46, rng, nx, art)
    # brass frame
    bars = strokes(W, H, [([(x0, 152), (x1, 190), (x1, 318), (x2, 350)], 5, None) for x0, x1, x2 in [(cx - 60, cx - 72, cx - 56), (cx + 60, cx + 72, cx + 56)]] +
                   [([(cx - 26, 152), (cx - 30, 190), (cx - 30, 318), (cx - 24, 350)], 3.4, None), ([(cx + 26, 152), (cx + 30, 190), (cx + 30, 318), (cx + 24, 350)], 3.4, None),
                    ([(cx - 72, 190), (cx + 72, 190)], 3, None), ([(cx - 72, 318), (cx + 72, 318)], 3, None)])
    cap = shapes(W, H, [arc_pts(cx, 152, 70, math.pi, math.tau, 28, 0.9) + [(cx + 70, 152)]])
    band = shapes(W, H, [rect(cx - 74, 140, cx + 74, 156)], smooth=False)
    stem = shapes(W, H, [rect(cx - 7, 44, cx + 7, 92)], smooth=False)
    knob = circles(W, H, [(cx, 86, 13)])
    hook = ring(W, H, cx, 30, 15, 5)
    base = shapes(W, H, [[(cx - 66, 348), (cx + 66, 348), (cx + 52, 372), (cx - 52, 372)]], smooth=False)
    cone = shapes(W, H, [[(cx - 46, 370), (cx + 46, 370), (cx + 6, 438), (cx - 6, 438)]])
    drop = shapes(W, H, [petal_pts(cx, 470, 34, 11, -math.pi / 2, n=12)])
    metal = np.maximum.reduce([bars, cap, band, stem, knob, hook, base, cone, drop])
    art = FO(art, metal, "#b8914c", seed=nx(), emboss=0.8, sparkle=0.12)
    pierce = circles(W, H, [(cx + math.cos(a) * 46, 128 - abs(math.sin(a)) * 18, 3.2) for a in [math.pi + k * math.pi / 8 for k in range(1, 8)]] +
                     [(cx + dx, 360, 2.6) for dx in range(-44, 50, 14)])
    art = GP(art, pierce, "#5a3c12", "#3a250a", seed=nx(), rough=0.4, pad=6)
    art = G(art, shade_side(np.maximum(cap, cone), -10, 0, 6), "#5a3c12", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.8)
    preview(art, "kq-lantern", bg="#f5efe1")
    save(art, f"{OUT}/lantern.webp", max_w=200, quality=82)
    clear()

if "star" in PARTS:
    W = H = 160
    nx = Seq(20500)
    m = shapes(W, H, [star8(80, 80, 66, 48, math.pi / 8)], smooth=False)
    hole = shapes(W, H, [star8(80, 80, 54, 39, math.pi / 8)], smooth=False)
    art = FO(blank(W, H), np.clip(m - hole, 0, 1), GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    art = GP(art, circles(W, H, [(80, 80, 24)]), GREEN, GREEN_D, seed=nx(), rough=0.6, pad=6)
    art = FO(art, np.maximum(ring(W, H, 80, 80, 26, 4), shapes(W, H, [star8(80, 80, 14, 8, 0)], smooth=False)), GOLD, seed=nx(), emboss=0.8)
    preview(art, "kq-star", bg=CREAM)
    save(art, f"{OUT}/star.webp", max_w=96, quality=84)

if "divider" in PARTS:
    W, H = 520, 60
    nx = Seq(20600)
    line = strokes(W, H, [([(14, 30), (206, 30)], 3, (0.9, 0.0)), ([(314, 30), (506, 30)], 3, (0.0, 0.9))])
    st = np.clip(shapes(W, H, [star8(260, 30, 22, 15, math.pi / 8)], smooth=False) - shapes(W, H, [star8(260, 30, 16, 11, math.pi / 8)], smooth=False), 0, 1)
    dd = circles(W, H, [(260, 30, 5), (222, 30, 4), (298, 30, 4), (196, 30, 2.4), (324, 30, 2.4)])
    lz = shapes(W, H, [[(232, 30), (240, 24), (248, 30), (240, 36)], [(272, 30), (280, 24), (288, 30), (280, 36)]], smooth=False)
    art = FO(blank(W, H), np.maximum.reduce([line, st, dd, lz]), GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    preview(art, "kq-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)

if "sprig" in PARTS:
    W, H = 520, 420
    nx = Seq(20700); rng = random.Random(12)
    jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = "#8aa58a", "#4f7564", "#2c4a3e"
    art = blank(W, H)
    stem = curve([(30, 400), (120, 330), (240, 250), (360, 200), (490, 186)], 60)
    art = G(art, strokes(W, H, [(stem, 5, (0.02, 0.5))]), "#6b7d5a", "#43553a", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1)
    for i, t in enumerate([0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82, 0.9]):
        x, y = stem[int(t * (len(stem) - 1))]
        side = 1 if i % 2 else -1
        a = math.atan2(stem[min(59, int(t * 59) + 1)][1] - y, stem[min(59, int(t * 59) + 1)][0] - x) + side * 0.9
        art = jw.leaf(art, W, H, x, y, rng.uniform(70, 104) * (1.1 - t * 0.4), a, rng, nx,
                      c=rng.choice([("#8aa58a", "#4f7564"), ("#9bb293", "#5d7c66"), ("#7c9a83", "#46695a")]))
    for t, r in [(0.18, 20), (0.3, 22), (0.47, 19), (0.6, 21), (0.78, 18), (0.97, 16)]:
        x, y = stem[int(t * (len(stem) - 1))]
        art = jw.white_flower(art, W, H, x + rng.uniform(-10, 10), y - rng.uniform(12, 24), r, rng, nx)
    for t in [0.44, 0.68, 0.88]:
        x, y = stem[int(t * (len(stem) - 1))]
        bm = ellipses(W, H, [(x + 6, y + 18, 6, 10, 20)])
        art = GP(art, bm, "#fffaf0", "#ece3d2", seed=nx(), rough=0.6, pad=6)
    preview(art, "kq-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=400, quality=80)
    clear()

if "tile" in PARTS:
    # pale 8-fold lattice, painted in thin gold-green watercolour on cream paper (seamless 360px)
    N = 360
    nx = Seq(20800)
    pp = paper(N, N, CREAM, seed=5)
    base = np.concatenate([np.asarray(pp, np.float32) / 255, np.ones((N, N, 1), np.float32)], -1)
    items = []
    for (cx, cy) in [(0, 0), (N, 0), (0, N), (N, N), (N / 2, N / 2)]:
        st = star8(cx, cy, 92, 66, math.pi / 8)
        items.append((st + [st[0]], 2.2, None))
        items.append((arc_pts(cx, cy, 40, 0, math.tau, 40), 1.6, None))
    for (cx, cy) in [(N / 2, 0), (0, N / 2), (N, N / 2), (N / 2, N)]:
        sq = [(cx, cy - 46), (cx + 46, cy), (cx, cy + 46), (cx - 46, cy), (cx, cy - 46)]
        items.append((sq, 1.8, None))
    m = strokes(N, N, items)
    art = G(base, m, "#b7a46a", "#8ea48a", seed=nx(), density=0.32, edge=0.3, bloom=0, rough=1.2, feather=0.6, pad=0)
    im = to_image(art).convert("RGB")
    im.save(f"{OUT}/tile.webp", "WEBP", quality=72, method=6)
    print("tile.webp", im.size, os.path.getsize(f"{OUT}/tile.webp") // 1024, "KB")

kb(OUT)
