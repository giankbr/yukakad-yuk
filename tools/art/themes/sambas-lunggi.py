"""Sambas Lunggi — kain lunggi Sambas: aubergine/plum silk with scattered couched-gold bunga tabur, a crimson pucuk
rebung border woven in gold, a gold-thread flower medallion and divider, and a gouache dawn scene of the yellow Keraton
Alwatzikhoebillah on the confluence of the Sambas rivers (tall flagpole, river gate, sampan, nipah palms). No figures.
Run: python3 -I sambas-lunggi.py [part ...]  parts: lunggi pucuk bunga divider keraton"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i3_lib import *
from _jw_lib import palm

OUT = outdir("sambas-lunggi")
PARTS = sys.argv[1:] or ["lunggi", "pucuk", "bunga", "divider", "keraton"]
PLUM, PLUM_D, CRIM, GOLD, GOLD_L = "#3d1533", "#2a0d23", "#8e1b3f", "#d2a64a", "#f0d58d"
YEL, YEL_D, ROOF, ROOF_D, WHITE = "#e8c24a", "#c99a2c", "#3d4a40", "#27312b", "#f4ecd9"


def tabur(cx, cy, r, n=8, rot=0.0):
    """small songket flower: n diamond petals around a square heart (geometric, woven look)."""
    pets = []
    for k in range(n):
        a = rot + k * math.tau / n
        ca, sa = math.cos(a), math.sin(a)
        px, py = cx + ca * r * 0.55, cy + sa * r * 0.55
        pets.append([(cx + ca * r * 0.18, cy + sa * r * 0.18), (px - sa * r * 0.2, py + ca * r * 0.2), (cx + ca * r, cy + sa * r), (px + sa * r * 0.2, py - ca * r * 0.2)])
    heart = [(cx, cy - r * 0.2), (cx + r * 0.2, cy), (cx, cy + r * 0.2), (cx - r * 0.2, cy)]
    return pets, heart


if "lunggi" in PARTS:
    W = H = 320
    nx = Seq(62100)
    cloth = cloth_base(W, H, PLUM, seed=nx(), cell=2.0, var=0.14)
    # faint shot-silk sheen bands
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = 0.5 + 0.5 * np.sin((xx + yy * 0.3) / W * math.tau * 2)
    cloth[..., :3] *= (0.92 + 0.12 * sheen)[..., None]
    cloth[..., :3] = np.clip(cloth[..., :3] * np.array([1.02, 0.98, 1.03]), 0, 1)
    # scattered tabur on a half-drop grid (period 80) + tiny gold specks between
    pets, hearts, specks = [], [], []
    for j in range(-1, 5):
        for i in range(-1, 5):
            cx = i * 80 + (40 if j % 2 else 0); cy = j * 80
            p, h = tabur(cx, cy, 17 if (i + j) % 2 else 13, 8, 0.0 if (i + j) % 2 else math.pi / 8)
            pets += p; hearts.append(h)
            specks += [(cx + 40, cy, 2.2), (cx, cy + 40, 2.2)] if j % 2 == 0 else []
    pm = shapes(W, H, pets, smooth=False); hm = shapes(W, H, hearts, smooth=False)
    sm = shapes(W, H, [[(x - r, y), (x, y - r * 1.6), (x + r, y), (x, y + r * 1.6)] for x, y, r in specks], smooth=False)
    gold = couched(np.clip(pm + sm, 0, 1), GOLD, seed=nx(), angle=0.0, pitch=1.6, stitch=6.0, stitch_col=PLUM_D, emboss=0.6)
    cloth = over(cloth, gold)
    cloth = over(cloth, couched(hm, "#e07a8f", seed=nx(), angle=0.0, pitch=1.4, stitch=5.0, stitch_col=PLUM_D))
    cloth[..., 3] = 1
    tile = tileable(cloth)
    tile[..., 3] = 1
    save_rgb(tile, f"{OUT}/lunggi.webp", quality=80)
    prev(tile, "sambas-lunggi")
    clear()


if "pucuk" in PARTS:
    # border band (repeat-x, period 60): crimson silk, gold pucuk rebung (tall triangles with inner motif),
    # a gold diamond chain under, thin gold rails
    W, H = 240, 96
    nx = Seq(62200)
    cloth = cloth_base(W, H, CRIM, seed=nx(), cell=2.0, var=0.12)
    tri, inner, dia, rails = [], [], [], []
    for x in range(-60, W + 60, 30):
        tri.append([(x, 64), (x + 30, 64), (x + 15, 12)])
        inner.append([(x + 9, 60), (x + 21, 60), (x + 15, 34)])
    for x in range(-30, W + 30, 15):
        dia.append([(x, 80), (x + 7.5, 74), (x + 15, 80), (x + 7.5, 86)])
    rails = [[(0, 4), (W, 4), (W, 8), (0, 8)], [(0, 66), (W, 66), (W, 69), (0, 69)], [(0, 90), (W, 90), (W, 93), (0, 93)]]
    tm = np.clip(shapes(W, H, tri, smooth=False) - shapes(W, H, inner, smooth=False), 0, 1)
    gm = np.clip(tm + shapes(W, H, dia, smooth=False) + shapes(W, H, rails, smooth=False), 0, 1)
    cloth = over(cloth, couched(gm, GOLD, seed=nx(), angle=0.0, pitch=1.5, stitch=6.0, stitch_col="#5a0f26"))
    cloth = over(cloth, couched(shapes(W, H, inner, smooth=False), "#e8b4c0", seed=nx(), angle=0.0, pitch=1.4, stitch=5.0, stitch_col="#5a0f26"))
    cloth[..., 3] = 1
    save_rgb(cloth, f"{OUT}/pucuk.webp", quality=82)
    prev(cloth, "sambas-pucuk")
    clear()


if "bunga" in PARTS:
    # gold-thread medallion: 8-point star of diamonds, ring of tabur petals, crimson heart (transparent)
    W = H = 240
    nx = Seq(62300); cx = cy = 120
    p1, h1 = tabur(cx, cy, 100, 8, 0.0)
    p2, _ = tabur(cx, cy, 70, 8, math.pi / 8)
    ringm = ring(W, H, cx, cy, 112, 4)
    dots = shapes(W, H, [[(cx + math.cos(a) * 108 - 5, cy + math.sin(a) * 108), (cx + math.cos(a) * 108, cy + math.sin(a) * 108 - 5), (cx + math.cos(a) * 108 + 5, cy + math.sin(a) * 108), (cx + math.cos(a) * 108, cy + math.sin(a) * 108 + 5)] for a in np.linspace(0, math.tau, 24, endpoint=False)], smooth=False)
    outer = shapes(W, H, p1, smooth=False); inner = shapes(W, H, p2, smooth=False)
    gold = np.clip(outer - gaussian_filter(inner, 1.5) * 1.5, 0, 1)
    art = blank(W, H)
    art = over(art, couched(np.clip(gold + ringm * 0 + dots, 0, 1), GOLD, seed=nx(), angle=0.0, pitch=1.7, stitch=7, stitch_col=PLUM_D))
    art = over(art, couched(inner, "#c23a5c", seed=nx(), angle=math.pi / 2, pitch=1.5, stitch=6, stitch_col="#4a0c20"))
    art = over(art, couched(shapes(W, H, [h1], smooth=False), GOLD_L, seed=nx(), angle=0.0, pitch=1.4, stitch=5, stitch_col=PLUM_D))
    prev(art, "sambas-bunga", bg=PLUM)
    save(art, f"{OUT}/bunga.webp", max_w=180, quality=84)
    clear()


if "divider" in PARTS:
    W, H = 560, 64
    nx = Seq(62400); cx, cy = W / 2, H / 2
    p, h = tabur(cx, cy, 26, 8, 0.0)
    lines = [[(cx - 40 - k * 4, cy - 1.5), (40 + k * 18, cy - 1.5), (40 + k * 18, cy + 1.5), (cx - 40 - k * 4, cy + 1.5)] for k in range(1)]
    lines += [[(cx + 40, cy - 1.5), (W - 40, cy - 1.5), (W - 40, cy + 1.5), (cx + 40, cy + 1.5)]]
    d = []
    for sgn in (-1, 1):
        for k in range(5):
            x = cx + sgn * (60 + k * 46)
            r = 9 - k * 1.2
            d.append([(x - r, cy), (x, cy - r), (x + r, cy), (x, cy + r)])
    m = np.clip(shapes(W, H, p + lines + d, smooth=False), 0, 1)
    art = over(blank(W, H), couched(m, GOLD, seed=nx(), angle=0.0, pitch=1.5, stitch=6, stitch_col=PLUM_D))
    art = over(art, couched(shapes(W, H, [h], smooth=False), "#c23a5c", seed=nx(), pitch=1.3, stitch=5, stitch_col="#4a0c20"))
    prev(art, "sambas-divider", bg="#f5ead2")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
    clear()


if "keraton" in PARTS:
    W, H = 820, 600
    nx = Seq(62500); rng = random.Random(21)
    horizon = 330
    art = painted_sky(W, H, [(0, "#efcfb3"), (0.25, "#f5dcc0"), (0.5, "#f6d6b0"), (0.55, "#d9c2a6"), (0.62, "#8fa39c"), (1.0, "#3d6064")], seed=nx(), streak=0.8)
    # low sun glow behind palace + soft clouds
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun = np.exp(-(((xx - 560) / 160) ** 2 + ((yy - 250) / 110) ** 2))
    art[..., :3] = np.clip(art[..., :3] + sun[..., None] * np.array([0.08, 0.05, 0.0]), 0, 1)
    for (cx, cy, rx, ry) in [(150, 90, 150, 22), (520, 60, 190, 18), (700, 150, 120, 16)]:
        art = G(art, shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 10), rng, 3, 0.12)]), "#f2c6b2", "#e8b8a8", seed=nx(), density=0.45, edge=0.4)
    # far bank treeline (confluence: two banks meeting at right)
    far = [(-20, horizon + 6)]
    for x in range(-20, W + 40, 22):
        far.append((x, horizon - 16 - 14 * abs(math.sin(x * 0.031)) - 8 * rng.random() - (18 if 640 < x < 760 else 0)))
    far.append((W + 20, horizon + 6))
    art = G(art, shapes(W, H, [far]), "#6f8a74", "#5c7864", seed=nx(), density=0.75, edge=0.5)
    # palace ground: low embankment
    bank = [(120, horizon + 6), (700, horizon + 2), (720, horizon + 24), (110, horizon + 28)]
    art = GP(art, shapes(W, H, [bank]), "#7d8a5a", "#68764a", seed=nx(), rough=2)
    # flagpole (tall mast with yardarm & rigging) left of palace
    fx = 190
    art = GP(art, polyline_mask(W, H, [[(fx, horizon + 10), (fx, 84)]], 5), WHITE, "#d8ceb8", seed=nx(), rough=1)
    art = GP(art, polyline_mask(W, H, [[(fx - 40, 150), (fx + 40, 150)], [(fx - 26, 112), (fx + 26, 112)]], 3), WHITE, seed=nx(), rough=1)
    rig = [[(fx - 40, 150), (fx - 70, horizon + 10)], [(fx + 40, 150), (fx + 72, horizon + 10)], [(fx, 86), (fx - 40, 150)], [(fx, 86), (fx + 40, 150)], [(fx - 26, 112), (fx - 40, 150)], [(fx + 26, 112), (fx + 40, 150)]]
    art = over(art, flat(polyline_mask(W, H, rig, 1.0), "#6b5a48", 0.6))
    art = GP(art, shapes(W, H, [[(fx + 2, 86), (fx + 24, 84), (fx + 44, 90), (fx + 44, 98), (fx + 24, 92), (fx + 2, 94)]]), "#c0392b", "#a8302a", seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(fx + 2, 94), (fx + 24, 92), (fx + 44, 98), (fx + 44, 106), (fx + 24, 100), (fx + 2, 102)]]), WHITE, seed=nx(), rough=0.6)
    # main palace: raised on short posts, yellow plank walls, white frames, two-tier hipped roof
    x0, x1, wb, wt = 270, 600, horizon + 4, 236
    posts = polyline_mask(W, H, [[(x, wb - 14), (x, wb + 6)] for x in range(x0 + 6, x1, 26)], 5, cap=False)
    art = GP(art, posts, "#5a4630", seed=nx(), rough=1)
    body = shapes(W, H, [[(x0, wt), (x1, wt), (x1, wb - 12), (x0, wb - 12)]], smooth=False)
    art = GP(art, body, YEL, "#f0cf62", seed=nx(), rough=1.2, streak=1.0)
    art = shade_side(art, body, YEL_D, (1, 0), 0.35, 30, nx())
    planks = polyline_mask(W, H, [[(x0, y), (x1, y)] for y in range(wt + 8, wb - 12, 7)], 1.0, cap=False)
    art = over(art, flat(planks * body, "#b98a28", 0.35))
    wins = []
    for x in range(x0 + 18, x1 - 30, 38):
        if 395 < x < 470:
            continue
        wins.append([(x, wt + 22), (x + 20, wt + 22), (x + 20, wb - 34), (x, wb - 34)])
    wm = shapes(W, H, wins, smooth=False)
    frame = np.clip(gaussian_filter(wm, 1.4) * 3, 0, 1)
    art = GP(art, frame, WHITE, seed=nx(), rough=0.8)
    art = GP(art, wm, "#4e5a52", "#3b463f", seed=nx(), rough=0.6)
    art = over(art, flat(polyline_mask(W, H, [[((w[0][0] + w[1][0]) / 2, w[0][1]), ((w[0][0] + w[1][0]) / 2, w[2][1])] for w in wins], 1.6, cap=False), WHITE, 0.9))
    # white balustrade / skirting
    art = GP(art, shapes(W, H, [[(x0 - 4, wb - 16), (x1 + 4, wb - 16), (x1 + 4, wb - 10), (x0 - 4, wb - 10)]], smooth=False), WHITE, seed=nx(), rough=0.6)
    # lower roof (wide hipped) then upper tier
    r1 = [(x0 - 34, wt + 4), (x0 + 40, 176), (x1 - 40, 176), (x1 + 34, wt + 4)]
    art = GP(art, shapes(W, H, [r1], smooth=False), ROOF, "#4a5a4c", seed=nx(), rough=1.2, streak=1.2)
    art = over(art, flat(polyline_mask(W, H, [[(x, 178), (x + (x - 435) * 0.25, wt + 2)] for x in range(x0 + 44, x1 - 40, 9)], 1.0) * shapes(W, H, [r1], smooth=False), ROOF_D, 0.5))
    art = GP(art, polyline_mask(W, H, [[(x0 - 36, wt + 4), (x1 + 36, wt + 4)]], 5, cap=False), WHITE, seed=nx(), rough=0.6)
    r2 = [(x0 + 50, 180), (x0 + 110, 132), (x1 - 110, 132), (x1 - 50, 180)]
    art = GP(art, shapes(W, H, [r2], smooth=False), "#44544a", ROOF, seed=nx(), rough=1.2, streak=1.2)
    art = GP(art, polyline_mask(W, H, [[(x0 + 108, 132), (x1 - 108, 132)]], 4, cap=False), WHITE, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(x0 + 60, 166), (x1 - 60, 166), (x1 - 62, 180), (x0 + 62, 180)]], smooth=False), YEL, seed=nx(), rough=0.8)
    # finials (mahkota atap) at the ridge ends
    for fxx in (x0 + 110, x1 - 110):
        art = GP(art, shapes(W, H, [[(fxx - 4, 132), (fxx + 4, 132), (fxx, 112)]], smooth=False), GOLD, seed=nx(), rough=0.5)
    # front porch with own gable roof and white columns, stair
    px0, px1 = 392, 478
    art = GP(art, shapes(W, H, [[(px0, 250), (px1, 250), (px1, wb - 10), (px0, wb - 10)]], smooth=False), "#f2d36c", seed=nx(), rough=0.8)
    art = GP(art, polyline_mask(W, H, [[(x, 256), (x, wb - 12)] for x in (px0 + 6, px0 + 30, px1 - 30, px1 - 6)], 5, cap=False), WHITE, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(px0 + 40, 270), (px1 - 40, 270), (px1 - 40, wb - 14), (px0 + 40, wb - 14)]], smooth=False), "#5a3a26", seed=nx(), rough=0.5)
    art = GP(art, shapes(W, H, [[(px0 - 18, 254), ((px0 + px1) / 2, 212), (px1 + 18, 254)]], smooth=False), ROOF, "#4a5a4c", seed=nx(), rough=1)
    art = GP(art, shapes(W, H, [[(px0 - 2, 250), ((px0 + px1) / 2, 222), (px1 + 2, 250)]], smooth=False), WHITE, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(px0 + 10, 248), ((px0 + px1) / 2, 228), (px1 - 10, 248)]], smooth=False), YEL, seed=nx(), rough=0.6)
    st = [[(px0 + 30 - k * 5, wb - 8 + k * 6), (px1 - 30 + k * 5, wb - 8 + k * 6), (px1 - 30 + k * 5, wb - 3 + k * 6), (px0 + 30 - k * 5, wb - 3 + k * 6)] for k in range(4)]
    art = GP(art, shapes(W, H, st, smooth=False), WHITE, "#d8ccb0", seed=nx(), rough=0.6)
    # river gate pavilion (gerbang tepi sungai) at right with jetty
    gx = 680
    art = GP(art, polyline_mask(W, H, [[(gx - 26, horizon + 2), (gx - 26, horizon - 44)], [(gx + 26, horizon + 2), (gx + 26, horizon - 44)]], 6, cap=False), WHITE, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(gx - 40, horizon - 42), (gx, horizon - 84), (gx + 40, horizon - 42)]], smooth=False), ROOF, seed=nx(), rough=1)
    art = GP(art, shapes(W, H, [[(gx - 30, horizon - 44), (gx + 30, horizon - 44), (gx + 30, horizon - 36), (gx - 30, horizon - 36)]], smooth=False), YEL, seed=nx(), rough=0.6)
    jetty = shapes(W, H, [[(gx - 30, horizon + 4), (gx + 30, horizon + 4), (gx + 70, horizon + 60), (gx - 10, horizon + 60)]], smooth=False)
    art = GP(art, jetty, "#8a6a48", "#6e5236", seed=nx(), rough=1.2)
    art = over(art, flat(polyline_mask(W, H, [[(gx - 26 + k * 5, horizon + 8 + k * 7), (gx + 34 + k * 5, horizon + 8 + k * 7)] for k in range(8)], 1.0, cap=False) * jetty, "#4a3624", 0.5))
    # palms both sides
    for (x, by, h, lean) in [(70, horizon + 24, 250, 0.12), (118, horizon + 26, 180, -0.08), (770, horizon + 18, 210, -0.1)]:
        pm = palm(W, H, x, by, h, rng, lean)
        pm = np.clip(gaussian_filter(pm, 1.1) * 3.0, 0, 1)
        art = GP(art, pm, "#4f6a3e", "#3b5530", seed=nx(), rough=1.2, streak=0.8)
    # nipah clumps at the water's edge
    nip = []
    for x0_, n in [(90, 9), (560, 6), (740, 8)]:
        for k in range(n):
            a = -math.pi / 2 + (k - n / 2) * 0.28
            base = (x0_ + rng.uniform(-8, 8), horizon + 26)
            L = rng.uniform(34, 60)
            nip.append((curve([base, (base[0] + math.cos(a) * L * 0.6, base[1] + math.sin(a) * L * 0.6), (base[0] + math.cos(a) * L + a * 6, base[1] + math.sin(a) * L + 14)], 10), 4, (0.05, 0.6)))
    art = G(art, strokes(W, H, nip), "#5d7a44", "#466234", seed=nx(), density=0.9, edge=0.5, rough=2)
    # reflections: mirror the band above horizon into the water, broken by ripples
    band = art[horizon - 220:horizon + 6].copy()
    refl = band[::-1]
    rh = refl.shape[0]
    ys = np.arange(rh, dtype=np.float32)
    ripple = (np.sin(ys[:, None] * 0.9 + np.arange(W)[None, :] * 0.02) * 3).astype(np.float32)
    rr = np.zeros_like(refl)
    for y in range(rh):
        rr[y] = np.roll(refl[y], int(ripple[y, 0] + 2 * math.sin(y * 0.37)), axis=0)
    water = art[horizon + 28:horizon + 28 + rh]
    k = (0.42 * np.exp(-ys / 150))[:, None, None] * (0.6 + 0.4 * (np.sin(ys * 1.7)[:, None, None] > -0.4))
    hh = min(rh, water.shape[0])
    water[:hh, :, :3] = water[:hh, :, :3] * (1 - k[:hh]) + rr[:hh, :, :3] * k[:hh]
    art[horizon + 28:horizon + 28 + hh] = water[:hh]
    # light streaks on water
    streaks = polyline_mask(W, H, [[(x, y), (x + rng.uniform(30, 90), y)] for x, y in [(rng.uniform(0, W), rng.uniform(horizon + 40, H - 20)) for _ in range(40)]], 1.6)
    art = over(art, flat(streaks, "#f6dcb8", 0.45))
    # sampan with pole (no figure), right foreground
    bx, byy = 600, 500
    hull = shapes(W, H, [[(bx - 120, byy - 14), (bx - 60, byy + 8), (bx + 70, byy + 8), (bx + 130, byy - 18), (bx + 70, byy - 2), (bx - 60, byy - 2)]])
    art = GP(art, hull, "#4a3020", "#3a2418", seed=nx(), rough=1)
    art = GP(art, polyline_mask(W, H, [[(bx - 110, byy - 12), (bx + 120, byy - 15)]], 2.4), "#c79a4a", seed=nx(), rough=0.5)
    art = GP(art, polyline_mask(W, H, [[(bx + 30, byy - 4), (bx + 90, byy - 150)]], 3), "#6b5236", seed=nx(), rough=0.5)
    art = over(art, flat(gaussian_filter(shapes(W, H, [ellipse_pts(bx + 4, byy + 14, 140, 7, 12)]), 3), "#1f3a3c", 0.5))
    art = add_grain(art, nx(), 0.03)
    art[..., 3] = 1
    prev(art, "sambas-keraton")
    save_rgb(art, f"{OUT}/keraton.webp", size=(720, 527), quality=80)
    clear()
