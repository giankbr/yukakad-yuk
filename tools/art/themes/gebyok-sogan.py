"""Gebyok Sogan — ivory & sogan brown: carved gebyok gate crown (ukiran lung-lungan, bronze leaf), gold-foil kembar mayang,
misty mountains/palms/joglo roof, garden-rose & peony bouquet, parang strip. Run: python3 -I gebyok-sogan.py [part ...]
parts: gate emblem mist bouquet parang. Assets -> public/themes/art/gebyok-sogan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *
import _jw_lib as jw
import _j2_lib as j2

OUT = outdir("gebyok-sogan")
PARTS = sys.argv[1:] or ["gate", "emblem", "mist", "bouquet", "parang"]
IVORY = "#f5eee2"
SOGAN, SOGAN_D, SOGAN_L = "#7a5230", "#4a2f19", "#a5774a"
BRONZE = "#b88a4a"

if "gate" in PARTS:
    W, H = 800, 470
    nx = Seq(8100)
    cx = W / 2
    lintel = shapes(W, H, [[(0, 170), (W, 170), (W, 246), (0, 246)]], smooth=False)
    crown_pts = [(cx - 250, 176), (cx - 190, 120), (cx - 120, 96), (cx - 70, 60), (cx - 30, 44), (cx, 4), (cx + 30, 44), (cx + 70, 60), (cx + 120, 96), (cx + 190, 120), (cx + 250, 176)]
    crown = shapes(W, H, [crown_pts])
    posts = shapes(W, H, [[(0, 240), (66, 240), (66, H), (0, H)], [(W - 66, 240), (W, 240), (W, H), (W - 66, H)]], smooth=False)
    # hanging tlacapan (triangular fringe) under the lintel
    fr = []
    for x in range(86, W - 80, 36):
        fr.append([(x - 14, 244), (x + 14, 244), (x, 282)])
    fringe = shapes(W, H, fr, smooth=False)
    band = np.clip(np.maximum.reduce([lintel, crown, posts, fringe]), 0, 1)
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along([(70, 208), (W - 70, 208)], 50)):
        if abs(x - cx) < 70:
            continue
        it, lv = jw.lung(x, y, 26, a, 1 if k % 2 else -1); items += it; leaves += lv
    for sgn in (-1, 1):
        for (u, v, s_, a) in [(20, 70, 46, -1.25), (78, 104, 40, -0.6), (140, 128, 34, -0.3), (200, 152, 26, -0.1)]:
            it, lv = jw.lung(cx + sgn * u, v, s_, a if sgn > 0 else math.pi - a, sgn); items += it; leaves += lv
        for (y) in range(270, H, 50):
            it, lv = jw.lung(33 if sgn < 0 else W - 33, y, 22, math.pi / 2, 1 if (y // 50) % 2 else -1); items += it; leaves += lv
    leaves.append(petal_pts(cx, 120, 118, 26, -math.pi / 2, n=12))
    leaves += [petal_pts(x, 246, 30, 9, math.pi / 2, n=8) for x in range(86, W - 80, 36)]
    art = jw.carve(W, H, band, items, leaves, nx, base=SOGAN, light=SOGAN_L, dark=SOGAN_D, gold=BRONZE, gold_amt=0.3, seed=9)
    mould = np.clip(shapes(W, H, [[(0, 166), (W, 166), (W, 176), (0, 176)], [(0, 240), (W, 240), (W, 248), (0, 248)]], smooth=False) - crown * 0.0, 0, 1)
    art = GP(art, mould, SOGAN_L, SOGAN, seed=nx(), rough=1, pad=8)
    art = FO(art, mould * np.clip((fbm(W, H, 5, 10, 3) - 0.45) * 3, 0, 1), BRONZE, seed=nx(), sparkle=0.05)
    preview(art, "gs-gate", IVORY)
    save(art, f"{OUT}/gate.webp", max_w=720, quality=80)

if "emblem" in PARTS:
    # kembar mayang (inspired): central stem, tiered janur blades, two birds, keris-spears, crowning bud — gold foil on ivory
    W, H = 360, 520
    nx = Seq(8200); cx = W / 2
    items = [([(cx, 470), (cx, 120)], 6, (0.05, 0.1))]
    polys = []
    for i, (y, L) in enumerate([(430, 120), (380, 132), (330, 128), (280, 118), (232, 100), (190, 80)]):
        for sgn in (-1, 1):
            a = -math.pi / 2 + sgn * (1.05 - i * 0.1)
            polys.append(petal_pts(cx, y, L, 13 - i, a, n=14, cup=0.18 * sgn))
            items.append((curve([(cx, y), (cx + sgn * L * 0.45, y - L * 0.35), (cx + sgn * L * 0.62, y - L * 0.72)], 14), 1.6, (0.1, 0.3)))
    # birds (manuk-manukan) perched mid-height
    for sgn in (-1, 1):
        bx, by = cx + sgn * 58, 300
        polys.append([(bx - sgn * 24, by + 6), (bx - sgn * 6, by - 12), (bx + sgn * 16, by - 16), (bx + sgn * 26, by - 10), (bx + sgn * 12, by - 4), (bx + sgn * 20, by + 10), (bx - sgn * 4, by + 10)])
    # keris spears and crowning bud
    for sgn in (-1, 1):
        items.append((curve([(cx + sgn * 10, 210), (cx + sgn * 22, 150), (cx + sgn * 18, 96), (cx + sgn * 26, 60)], 20), 3, (0.0, 0.7)))
    polys.append(petal_pts(cx, 128, 92, 22, -math.pi / 2, n=14))
    polys.append(deform(ellipse_pts(cx, 474, 46, 16, 14), random.Random(2), 1, 0.05))
    m = np.maximum(strokes(W, H, items), shapes(W, H, polys))
    art = blank(W, H)
    art = G(art, gaussian_filter(m, 6), "#a07a3a", seed=nx(), density=0.25, edge=0.1, bloom=0, rough=2)
    art = FO(art, m, "#c9a25a", seed=nx(), emboss=0.7, sparkle=0.12)
    wear = np.clip((fbm(W, H, 8, 8, 3) - 0.72) * 4, 0, 1) * m
    art = G(art, wear, SOGAN, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6)
    preview(art, "gs-emblem", IVORY)
    save(art, f"{OUT}/emblem.webp", max_w=260, quality=84)

if "mist" in PARTS:
    W, H = 800, 560
    nx = Seq(8300); rng = random.Random(83)
    art = blank(W, H)
    art = G(art, jw.hills(W, H, 210, 90, 11, 0.7), "#ddd0bd", "#cfbea6", seed=nx(), density=0.42, edge=0.4, bloom=0.5, rough=10)
    art = G(art, jw.hills(W, H, 300, 50, 12, 0.5), "#cdb99c", "#b9a082", seed=nx(), density=0.45, edge=0.4, bloom=0.5, rough=8)
    for (x, h, ln) in [(90, 300, -0.1), (150, 240, 0.1), (660, 280, 0.12), (720, 220, -0.08), (600, 190, 0.05)]:
        art = G(art, jw.palm(W, H, x, 470, h, rng, ln), "#a88b6b", "#8a6d4f", seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=2.5, feather=0.8)
    j, _ = jw.joglo_wash(W, H, 400, 500, 460, "#e1d2bd", "#a98a68", "#5f452c", nx, density=0.8)
    art = glaze(art, j)
    mist = np.clip(np.linspace(0, 1, H)[:, None] * 1.6 - 0.65, 0, 1) * np.ones((1, W))
    art[..., 3] *= (1 - 0.7 * mist).astype(np.float32)
    preview(art, "gs-mist", IVORY)
    save(art, f"{OUT}/mist.webp", max_w=680, quality=76)

if "bouquet" in PARTS:
    # low wide spray: peonies + garden roses (ivory, apricot, dusty rose, sogan), eucalyptus-ish leaves, melati drops
    W, H = 840, 420
    nx = Seq(8400); rng = random.Random(84)
    sd = lambda: nx()
    back = blank(W, H)
    area = np.zeros((H, W), np.float32)
    for (x, y, L, a) in [(150, 250, 200, -2.7), (250, 200, 210, -2.0), (400, 170, 220, -1.6), (560, 200, 210, -1.1), (680, 250, 200, -0.45),
                         (90, 300, 160, 3.0), (740, 300, 160, 0.1), (330, 240, 150, -2.4), (480, 240, 150, -0.8)]:
        lay, _m = j2.leaf(W, H, x, y, L * 0.72, a, "#a3ad8a", "#5f7052", sd, rng, width=0.3)
        back = glaze(back, lay)
    flowers = blank(W, H)
    for (x, y, r, kind, cols) in [(400, 250, 92, "peony", ("#fbf3e8", "#ead3bd", "#b88a62")), (250, 280, 74, "rose", ("#f2d6c4", "#d29a80", "#8f5640")),
                                  (560, 285, 78, "rose", ("#efdcc8", "#c7a07c", "#7a5230")), (130, 320, 56, "peony", ("#f6e7dc", "#e2bfae", "#a7705c")),
                                  (680, 320, 60, "rose", ("#f4e3d4", "#dcb49a", "#9a6648")), (320, 180, 44, "rose", ("#f7ece0", "#e3c5ad", "#a57a5a")),
                                  (490, 180, 40, "rose", ("#f2d9c9", "#d6a790", "#8f5a44"))]:
        fn = j2.peony if kind == "peony" else j2.rose
        lay, m = fn(W, H, x, y + 10, r * 1.3, *cols, sd, rng)
        flowers = glaze(flowers, lay); np.maximum(area, m, out=area)
    back = knockout(back, area, amount=0.94, grow=4)
    art = glaze(back, flowers)
    for (x, y, a) in [(200, 150, -2.2), (610, 150, -0.9), (60, 250, -2.9), (770, 240, -0.2)]:
        lay, _m = j2.bud(W, H, x, y, 14, a, "#e9c9b2", "#a7705c", "#6f7f5a", sd, rng)
        art = glaze(art, lay)
    for x0 in (300, 470):
        pts = curve([(x0, 300), (x0 + 30, 350), (x0 + 80, 372)], 60)
        art = jw.melati_string(art, W, H, pts, rng, nx, size=6.5)
    art = jw.dots(art, W, H, rng, nx, 410, 230, 260, 70, 22, "#c09070")
    preview(art, "gs-bouquet", IVORY)
    save(art, f"{OUT}/bouquet.webp", max_w=700, quality=80)

if "parang" in PARTS:
    # seamless horizontal strip: parang rusak — chained S-curls along diagonals, mlinjon dots between, sogan on ivory
    W, H = 240, 60
    nx = Seq(8500)
    curls, lens, dots_ = [], [], []
    period = 40
    for k in range(-3, 9):
        x0 = k * period
        # chain of lens-shaped "blades" climbing the diagonal
        for j in range(4):
            t = j / 4
            cx_, cy_ = x0 + 8 + t * 46, H - 6 - t * (H - 12)
            lens.append(deform(petal_pts(cx_ - 7, cy_ + 7, 18, 6.5, -math.pi / 4, n=12), random.Random(j), 0, 0))
            curls.append((spiral_pts(cx_ + 2, cy_ - 1, 4.2, 0.8, math.pi * 0.25, 0.9, 16, 1), 1.6, (0.0, 0.5)))
        dots_ += [(x0 + 30 + t * 30, H - 10 - t * (H - 20), 1.8) for t in (0.15, 0.5, 0.85)]
    lm = shapes(W, H, lens)
    cm = strokes(W, H, curls)
    art = blank(W, H)
    art = OV(art, np.clip(lm - cm * 0.9, 0, 1), lambda q: linocut(q, SOGAN, seed=5, wear=0.22, rough=0.7))
    art = OV(art, circles(W, H, dots_), lambda q: linocut(q, SOGAN_D, seed=6, wear=0.1, rough=0.4))
    edge = shapes(W, H, [[(0, 0), (W, 0), (W, 2.5), (0, 2.5)], [(0, H - 2.5), (W, H - 2.5), (W, H), (0, H)]], smooth=False)
    art = OV(art, edge, lambda q: linocut(q, SOGAN_D, seed=7, wear=0.1, rough=0.4))
    save_full(art, f"{OUT}/parang.webp", quality=82)
    preview(art, "gs-parang", IVORY)
