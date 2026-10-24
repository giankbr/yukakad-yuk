"""Taman Sari — the Yogyakarta water castle, painted in lime-plaster gouache with soft watercolour weathering
(original, inspired-by designs; architecture only): a tall gateway frame with stepped crest, carved floral reliefs and
a lit archivolt (the cover looks *through* it), a turquoise bathing pool with stone coping, steps and two mushroom
fountains, a carved flower urn with bougainvillea, and a carved relief band divider.
Run: python3 -I taman-sari.py [part ...]  parts: gate pool urn relief
Assets -> public/themes/art/taman-sari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t3_lib import *

OUT = outdir("taman-sari")
PARTS = sys.argv[1:] or ["gate", "pool", "urn", "relief"]
CREAM, CREAM2 = "#efe4cb", "#e4d3b0"
SHADE = "#8e7a58"
DEEP = "#5f5038"
TEAL, TEAL2, TEAL_D = "#5fbfb8", "#8fd8cf", "#23787a"
BOUG, BOUG2 = "#c2367a", "#e0619c"
LEAF, LEAF2 = "#5f7f45", "#86a35a"


def arch(cx, cy, rx, ry, n=48):
    return arc_pts(cx, cy, rx, math.pi, 2 * math.pi, n, ry / rx)


def scroll_items(x, y, s, ang, flip):
    items, leaves = lung(x, y, s, ang, flip)
    return items, leaves


if "gate" in PARTS:
    W, H = 780, 1120
    nx = Seq(100); rng = random.Random(3)
    art = blank(W, H)
    # outer silhouette: two pillars + stepped crest
    crest = [(0, H), (0, 214), (18, 214), (18, 190), (58, 190), (58, 160), (124, 160), (124, 132), (196, 132), (196, 104),
             (262, 104), (280, 80), (318, 72), (338, 50), (362, 44), (372, 22), (390, 6)]
    crest = crest + [(W - x, y) for x, y in reversed(crest)]
    outer = shapes(W, H, [crest], smooth=False)
    ox0, ox1, oy = 132, 648, 360
    opening = shapes(W, H, [[(ox0, H + 10), (ox0, oy)] + arch(390, oy, (ox1 - ox0) / 2, 196) + [(ox1, oy), (ox1, H + 10)]], smooth=False)
    shifted = np.roll(opening, -20, 1)
    shifted[:, -20:] = 0
    shifted = np.roll(shifted, 8, 0)
    reveal = np.clip(opening - shifted, 0, 1)
    wall = np.clip(outer - opening, 0, 1)
    art = stucco(art, np.clip(wall + reveal, 0, 1), nx, wear=0.95)
    pat = np.clip(wall + reveal, 0, 1) * np.clip(fbm(W, H, nx(), 90, 3) * 1.8 - 1.0, 0, 1)
    art = G(art, pat, "#c9a46a", "#b8925a", seed=nx(), density=0.35, edge=0.5, bloom=0.5, rough=6)
    # reveal (wall thickness) in shade
    art = G(art, reveal, SHADE, "#a08a62", seed=nx(), density=0.55, edge=0.4, bloom=0.3, rough=1.5)
    art = G(art, gaussian_filter(reveal, 3) * reveal, DEEP, seed=nx(), density=0.25, edge=0, bloom=0, rough=1)
    # archivolt band (moulding) around the opening
    av_out = shapes(W, H, [[(ox0 - 26, H + 10), (ox0 - 26, oy)] + arch(390, oy, (ox1 - ox0) / 2 + 26, 222) + [(ox1 + 26, oy), (ox1 + 26, H + 10)]], smooth=False)
    band = np.clip(av_out - opening, 0, 1) * (np.mgrid[0:H, 0:W][0] < oy + 4)
    petals = []
    for k in range(23):
        a = math.pi + math.pi * (k + 0.5) / 23
        rx, ry = (ox1 - ox0) / 2 + 13, 209
        px, py = 390 + math.cos(a) * rx, oy + math.sin(a) * ry
        petals.append(ellipse_pts(px, py, 6.5, 9.5, 10, a + math.pi / 2))
    pm = shapes(W, H, petals) * band
    art = G(art, band, "#d8c49c", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=1)
    art = emboss(art, pm, nx, s=1.0, k=10)
    rim = np.clip(gaussian_filter(av_out, 1.0) - gaussian_filter(av_out, 3.0), 0, 1) * 2
    art = emboss(art, np.clip(rim, 0, 1) * (np.mgrid[0:H, 0:W][0] < oy + 4), nx, s=0.8, k=6, cast=2)
    # keystone rosette
    ks = []
    for k in range(8):
        a = k * math.tau / 8 + 0.2
        ks.append(petal_pts(390 + math.cos(a) * 4, 164 + math.sin(a) * 4, 26, 13, a, n=10))
    ksm = shapes(W, H, ks)
    art = GP(art, circles(W, H, [(390, 164, 34)]), CREAM, CREAM2, seed=nx(), rough=1, streak=0.4)
    art = emboss(art, ksm, nx, s=1.2, k=9)
    art = emboss(art, circles(W, H, [(390, 164, 8)]), nx, s=1.0, k=9)
    art = emboss(art, ring_mask(W, H, 390, 164, 36, 3), nx, s=0.8, k=7)
    # spandrel scrolls (left, mirrored right)
    items, leaves = [], []
    for (x, y, s_, a, f) in [(210, 186, 58, -0.35, 1), (292, 142, 44, -0.15, 1), (150, 236, 46, -1.05, -1)]:
        it, lv = lung(x, y, s_, a, f)
        items += it; leaves += lv
    sp = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    sp = np.maximum(sp, sp[:, ::-1]) * wall * (1 - gaussian_filter(av_out, 2) * 1.2).clip(0, 1)
    art = G(art, gaussian_filter(sp, 3), SHADE, seed=nx(), density=0.18, edge=0, bloom=0, rough=1)
    art = emboss(art, sp, nx, s=1.3, k=10)
    # tier mouldings along the crest steps
    tiers = []
    for y in (214, 190, 160, 132, 104):
        tiers.append(([(0, y + 3), (W, y + 3)], 5, None))
    tm = strokes(W, H, tiers) * outer
    art = emboss(art, tm, nx, s=0.9, k=7, cast=2)
    under = np.zeros((H, W), np.float32)
    for y in (214, 190, 160, 132, 104):
        under[y + 6:y + 20] = np.linspace(1, 0, 14, dtype=np.float32)[:, None]
    art = G(art, under * outer * (1 - opening), SHADE, seed=nx(), density=0.4, edge=0, bloom=0.2, rough=1.5)
    vol = []
    for x, y in ((18, 190), (58, 160), (124, 132), (196, 104)):
        vol.append((spiral_pts(x + 14, y - 12, 12, 3, math.pi, 1.2, 30, 1), 5, (0.0, 0.5)))
    vm_ = strokes(W, H, vol)
    vm_ = np.maximum(vm_, vm_[:, ::-1]) * outer
    art = emboss(art, vm_, nx, s=1.0, k=9)
    edge_ = np.clip(outer - gaussian_filter(outer, 1.2), 0, 1) * 2 + np.clip(gaussian_filter(opening, 1.2) - opening, 0, 1) * 0
    art = G(art, np.clip(edge_, 0, 1), DEEP, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    # crown finial
    crown = [ellipse_pts(390, 30, 16, 24, 14), ellipse_pts(390, 60, 34, 12, 14)]
    for d in (-1, 1):
        crown.append(petal_pts(390 + d * 30, 66, 38, 13, -math.pi / 2 + d * 0.9, n=10))
    art = emboss(art, shapes(W, H, crown) * outer, nx, s=1.2, k=9)
    # pillar capitals and recessed panels with climbing vines
    for x0, x1 in ((0, ox0 - 26), (ox1 + 26, W)):
        cap = shapes(W, H, [[(x0, 236), (x1, 236), (x1, 262), (x0, 262)]], smooth=False) * wall
        art = G(art, cap, "#d8c49c", seed=nx(), density=0.3, edge=0.3, bloom=0.1, rough=1)
        art = emboss(art, strokes(W, H, [([(x0, 240), (x1, 240)], 4, None), ([(x0, 258), (x1, 258)], 4, None)]) * wall, nx, s=0.8, k=7, cast=2)
        px0, px1 = x0 + 20, x1 - 20
        panel = shapes(W, H, [[(px0, 290), (px1, 290), (px1, H - 20), (px0, H - 20)]], smooth=False)
        inner = shapes(W, H, [[(px0 + 7, 297), (px1 - 7, 297), (px1 - 7, H - 27), (px0 + 7, H - 27)]], smooth=False)
        art = G(art, inner, "#cdb98f", seed=nx(), density=0.35, edge=0.35, bloom=0.3, rough=1.2)
        art = emboss(art, np.clip(panel - inner, 0, 1), nx, s=0.9, k=7, cast=2)
        cx = (px0 + px1) / 2
        its, lvs = [], []
        vine = [(cx + math.sin(y / 46) * (px1 - px0) * 0.18, y) for y in range(310, H - 40, 6)]
        its.append((vine, 5, None))
        for i, y in enumerate(range(330, H - 60, 64)):
            f = 1 if i % 2 else -1
            it, lv = lung(cx + f * 6, y, 22, -math.pi / 2 + f * 0.6, f)
            its += it; lvs += lv
            lvs.append(petal_pts(cx - f * 4, y + 30, 22, 9, math.pi / 2 - f * 1.1, n=10))
        vm = np.maximum(strokes(W, H, its), shapes(W, H, lvs)) * inner
        art = emboss(art, vm, nx, s=1.1, k=10)
    # weathered top edges catch the light; soft shadow under the crest tiers
    art = G(art, np.clip(gaussian_filter(outer, 6) - outer * 0.0, 0, 1) * (1 - outer) * 0, SHADE, seed=nx())
    preview(art, "ts-gate", tone="#cfe7e3")
    save(art, f"{OUT}/gate.webp", max_w=780, quality=80)
    clear()

if "pool" in PARTS:
    W, H = 780, 520
    nx = Seq(400); rng = random.Random(5)
    art = blank(W, H)
    # back coping wall
    back = shapes(W, H, [[(0, 0), (W, 0), (W, 70), (0, 70)]], smooth=False)
    art = stucco(art, back, nx, wear=0.4)
    art = G(art, shapes(W, H, [[(0, 34), (W, 34), (W, 70), (0, 70)]], smooth=False), SHADE, seed=nx(), density=0.32, edge=0.3, bloom=0.2, rough=1)
    art = emboss(art, strokes(W, H, [([(0, 32), (W, 32)], 4, None)]), nx, s=0.8, k=7)
    # central steps going down into the water
    for i, (y0, y1, inset) in enumerate([(70, 96, 0), (96, 120, 18), (120, 142, 36)]):
        st = shapes(W, H, [[(300 + inset, y0), (480 - inset, y0), (480 - inset, y1), (300 + inset, y1)]], smooth=False)
        art = stucco(art, st, nx, wear=0.3, moss=None)
        art = G(art, shapes(W, H, [[(300 + inset, y0 + 9), (480 - inset, y0 + 9), (480 - inset, y1), (300 + inset, y1)]], smooth=False), SHADE, seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1)
    # water
    water = shapes(W, H, [[(0, 70), (W, 70), (W, 486), (0, 486)]], smooth=False)
    steps_m = shapes(W, H, [[(300, 70), (480, 70), (480, 96), (462, 96), (462, 120), (444, 120), (444, 142), (336, 142), (336, 120), (318, 120), (318, 96), (300, 96)]], smooth=False)
    wat = np.clip(water - steps_m, 0, 1)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = OV(art, wat, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(TEAL), np.float32), m[..., None]], -1))
    art = G(art, wat * np.clip(1.2 - yy * 1.6, 0, 1), TEAL_D, "#2f8f8c", seed=nx(), density=0.55, edge=0.2, bloom=0.4, rough=4)
    art = G(art, wat * np.clip(yy * 1.6 - 0.5, 0, 1), TEAL2, "#a8e4d8", seed=nx(), density=0.55, edge=0.2, bloom=0.5, rough=4)
    cs = caustics(W, H, nx(), 24, 16) * wat * (0.4 + 0.6 * yy)
    art = OV(art, cs, lambda m: solid_rgba(m, "#e9fbf4", 0.32))
    art = G(art, wat * np.clip(1 - (yy - 0.13) * 9, 0, 1), "#1d5e60", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=2)
    # reflection of the back wall: pale wobbly band just under the coping
    refl = np.clip(shapes(W, H, [[(0, 70), (W, 70), (W, 120), (0, 120)]], smooth=False) * fbm(W, H, nx(), 12, 2) * 1.6 - 0.4, 0, 1) * wat
    art = OV(art, gaussian_filter(refl, (0.6, 3)), lambda m: solid_rgba(m, "#f1ead2", 0.45))
    art = OV(art, np.clip(gaussian_filter(steps_m, 4) * 2 - steps_m * 2, 0, 1) * wat, lambda m: solid_rgba(m, "#1f5f61", 0.4))
    # ripple lines
    rip = []
    for _ in range(26):
        y = rng.uniform(150, 470); x = rng.uniform(0, W); L = rng.uniform(30, 90)
        rip.append(([(x - L / 2, y), (x, y - 2), (x + L / 2, y)], rng.uniform(1.4, 2.6), (0.4, 0.4)))
    art = OV(art, strokes(W, H, rip) * wat, lambda m: solid_rgba(m, "#f3fffb", 0.55))
    # mushroom fountains
    for fx in (150, 630):
        fy = 230
        ring = []
        for r_, a_ in ((46, 0.5), (64, 0.3)):
            ring.append((arc_pts(fx, fy + 70, r_, 0, math.tau, 60, 0.28), 2.0, None))
        art = OV(art, strokes(W, H, ring) * wat, lambda m: solid_rgba(m, "#f6fffb", 0.6))
        stem = shapes(W, H, [[(fx - 13, fy), (fx + 13, fy), (fx + 17, fy + 72), (fx - 17, fy + 72)]], smooth=False)
        art = stucco(art, stem, nx, wear=0.4, moss="#6f8a5a")
        art = G(art, inner_shade(stem, -8, 0, 4), SHADE, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
        cap = shapes(W, H, [arc_pts(fx, fy + 4, 62, math.pi, 2 * math.pi, 30, 0.62) + [(fx + 64, fy + 6), (fx - 64, fy + 6)]])
        art = stucco(art, cap, nx, wear=0.45)
        art = G(art, inner_shade(cap, -10, -6, 6), SHADE, seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1)
        art = emboss(art, strokes(W, H, [(arc_pts(fx, fy + 4, 52, math.pi * 1.1, math.pi * 1.9, 20, 0.6), 3, None)]), nx, s=0.8, k=7)
        # water curtain falling from the rim
        drops = []
        for k in range(14):
            sx = fx - 60 + k * 120 / 13
            drops.append(([(sx, fy + 8), (sx + (sx - fx) * 0.12, fy + 40), (sx + (sx - fx) * 0.2, fy + 68)], 1.6, (0.05, 0.6)))
        art = OV(art, strokes(W, H, drops), lambda m: solid_rgba(m, "#f4fffd", 0.55))
    # front coping
    front = shapes(W, H, [[(0, 486), (W, 486), (W, H), (0, H)]], smooth=False)
    art = stucco(art, front, nx, wear=0.35, moss=None)
    art = emboss(art, strokes(W, H, [([(0, 490), (W, 490)], 4, None)]), nx, s=0.8, k=7)
    art = G(art, np.clip(gaussian_filter(front, 5) - front, 0, 1) * 2, "#1f5f61", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    preview(art, "ts-pool")
    save(art, f"{OUT}/pool.webp", max_w=780, quality=78)
    clear()

if "urn" in PARTS:
    W, H = 340, 500
    nx = Seq(700); rng = random.Random(7)
    art = blank(W, H)
    cx = 170
    # bougainvillea: a soft leaf mass, leaves along the rim and two trailing sprays, then papery bract clusters
    blobs = []
    for _ in range(9):
        bx = cx + rng.uniform(-95, 95); by = rng.uniform(110, 215)
        blobs.append(deform(ellipse_pts(bx, by, rng.uniform(40, 62), rng.uniform(32, 46), 12, rng.uniform(0, 3)), rng, 2, 0.18))
    mass = shapes(W, H, blobs)
    art = G(art, mass, "#3f5f30", "#5d7f42", seed=nx(), density=0.85, edge=0.55, bloom=0.4, rough=6)
    lv = []
    for _ in range(70):
        a = rng.uniform(-math.pi, 0); r_ = rng.uniform(60, 125)
        x = cx + math.cos(a) * r_ * 1.0; y = 205 + math.sin(a) * r_ * 0.85
        lv.append(petal_pts(x, y, rng.uniform(16, 24), rng.uniform(8, 11), a + rng.uniform(-0.6, 0.6), n=10))
    sprays = []
    for d in (-1, 1):
        stem = curve([(cx + d * 70, 225), (cx + d * 112, 236), (cx + d * 128, 280), (cx + d * 120, 330)], 30)
        sprays.append((stem, 3, (0.05, 0.4)))
        for x, y, ang in along(stem, 16):
            for sgn in (-1, 1):
                lv.append(petal_pts(x, y, rng.uniform(13, 18), rng.uniform(6, 8), ang + sgn * 1.0, n=8))
    art = G(art, strokes(W, H, sprays), "#5a4a2a", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.5)
    lm = shapes(W, H, lv)
    art = G(art, lm, LEAF, LEAF2, seed=nx(), density=0.8, edge=0.6, bloom=0.25, rough=2.5)
    art = G(art, shapes(W, H, lv[::4]), "#3a5530", seed=nx(), density=0.45, edge=0.5, bloom=0.2, rough=2)
    flowers = [(cx + rng.uniform(-100, 100), rng.uniform(100, 215)) for _ in range(16)]
    for d in (-1, 1):
        flowers += [(cx + d * 124, 300), (cx + d * 112, 248)]
    for x, y in flowers:
        cl = []
        for k in range(rng.randint(5, 8)):
            bx, by = x + rng.gauss(0, 10), y + rng.gauss(0, 8)
            for p_ in range(3):
                aa = p_ * math.tau / 3 + rng.uniform(0, 1)
                cl.append(petal_pts(bx, by, rng.uniform(8, 11), rng.uniform(6, 8), aa, n=8, cup=0.2))
        cm = shapes(W, H, cl)
        art = G(art, cm, BOUG, BOUG2, seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.8)
        art = G(art, inner_shade(cm, 3, 3, 3), "#7d1b4c", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    # urn body (classical jambangan)
    prof = [(0, 230), (78, 230), (72, 244), (60, 252), (92, 300), (100, 340), (86, 384), (52, 412), (34, 420), (34, 432), (56, 440), (60, 470), (0, 470)]
    body = [(cx + x, y) for x, y in prof] + [(cx - x, y) for x, y in reversed(prof)]
    um = shapes(W, H, [body])
    art = stucco(art, um, nx, wear=0.55)
    art = G(art, inner_shade(um, 18, 0, 14), SHADE, seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=2)
    art = G(art, inner_shade(um, 0, -10, 6), DEEP, seed=nx(), density=0.3, edge=0, bloom=0, rough=1)
    # relief band with small scrolls + rim moulding
    its, lvs = [], []
    for k, x in enumerate(range(cx - 70, cx + 80, 46)):
        it, l2 = lung(x, 324, 20, 0, 1 if k % 2 else -1)
        its += it; lvs += l2
    rel = np.maximum(strokes(W, H, its), shapes(W, H, lvs)) * um
    art = emboss(art, rel, nx, s=1.0, k=10)
    art = emboss(art, strokes(W, H, [([(cx - 76, 238), (cx + 76, 238)], 5, None), ([(cx - 96, 292), (cx + 96, 292)], 3, None), ([(cx - 92, 358), (cx + 92, 358)], 3, None), ([(cx - 50, 438), (cx + 50, 438)], 4, None)]) * um, nx, s=0.8, k=7)
    preview(art, "ts-urn")
    save(art, f"{OUT}/urn.webp", max_w=300, quality=80)
    clear()

if "relief" in PARTS:
    W, H = 720, 150
    nx = Seq(900)
    art = blank(W, H)
    plaque = shapes(W, H, [[(60, 30), (W - 60, 30), (W - 30, 75), (W - 60, 120), (60, 120), (30, 75)]], smooth=False)
    art = stucco(art, plaque, nx, wear=0.35, moss=None)
    inner = shapes(W, H, [[(74, 40), (W - 74, 40), (W - 44, 75), (W - 74, 110), (74, 110), (44, 75)]], smooth=False)
    art = G(art, inner, "#d3bf96", seed=nx(), density=0.35, edge=0.35, bloom=0.3, rough=1)
    art = emboss(art, np.clip(plaque - inner, 0, 1), nx, s=0.8, k=7, cast=2)
    its, lvs = [], []
    for (x, a, f) in [(300, math.pi, 1), (220, math.pi, -1), (140, math.pi, 1)]:
        it, lv = lung(x, 76, 34, a, f)
        its += it; lvs += lv
    ros = []
    for k in range(6):
        a = k * math.tau / 6
        ros.append(petal_pts(360 + math.cos(a) * 3, 75 + math.sin(a) * 3, 24, 12, a, n=10))
    rm = np.maximum(strokes(W, H, its), shapes(W, H, lvs))
    rm = np.maximum(rm, rm[:, ::-1])
    rm = np.maximum(rm, shapes(W, H, ros)) * inner
    art = emboss(art, rm, nx, s=1.1, k=10)
    art = emboss(art, circles(W, H, [(360, 75, 6)]), nx, s=0.9, k=9)
    preview(art, "ts-relief")
    save(art, f"{OUT}/relief.webp", max_w=420, quality=82)
    clear()
