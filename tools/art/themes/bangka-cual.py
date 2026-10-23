"""Bangka Cual — tenun cual Bangka (soft red silk ground, ikat-blurred rose bands, gold and rose supplementary-weft
florals woven as thread floats), a pucuk-rebung tumpal border, a woven kembang emblem, and a secondary gouache
scene: granite boulders, turquoise shallows and a Malay stilt house among coconut palms.
Run: python3 -I bangka-cual.py [part ...]   parts: cual tumpal kembang pantai"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l4_lib import *
from _jw_lib import palm
from _p1_lib import wrap_noise

OUT = outdir("bangka-cual")
PARTS = sys.argv[1:] or ["cual", "tumpal", "kembang", "pantai"]
RED, RED_D, ROSE, ROSE_L = "#a22f38", "#7d1f2a", "#d77a7c", "#efb9ae"
GOLD, GOLD_L, GOLD_D = "#d8b25c", "#f0d898", "#9c7630"
MAROON = "#5e1822"


def C(h):
    return np.array(hex_rgb(h), np.float32)


def lay(rgb, mask, col, tone=None, amt=.35):
    c = C(col)
    if tone is not None:
        c = c[None, None, :] * (1 - amt / 2 + amt * tone[..., None])
    a = np.clip(mask, 0, 1)[..., None]
    return rgb * (1 - a) + c * a


def flower_draw(cv, x, y, it, part):
    """Original cual-inspired flower: 8 pointed petals, inner star, leaves on the diagonals."""
    _, _, r, kind = it
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    if kind == "big":
        if part == "petal":
            for k in range(8):
                a = k * math.tau / 8 + math.pi / 8
                cv.c.drawPath(smooth_path(petal_pts(x, y, r, r * .17, a, n=16)), p)
        elif part == "vein":
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(max(1.6, r * .03))
            for k in range(8):
                a = k * math.tau / 8 + math.pi / 8
                cv.c.drawLine(x + math.cos(a) * r * .45, y + math.sin(a) * r * .45, x + math.cos(a) * r * .86, y + math.sin(a) * r * .86, p)
        elif part == "rim":
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(max(2.0, r * .04))
            for k in range(8):
                a = k * math.tau / 8 + math.pi / 8
                cv.c.drawPath(smooth_path(petal_pts(x, y, r, r * .17, a, n=16)), p)
            p.setStyle(skia.Paint.kFill_Style)
            for k in range(4):  # diagonal leaves / tendrils
                a = k * math.tau / 4
                cv.c.drawPath(smooth_path(petal_pts(x + math.cos(a) * r * .95, y + math.sin(a) * r * .95, r * .5, r * .16, a, n=12)), p)
                for sgn in (-1, 1):
                    b = a + sgn * .55
                    cv.c.drawCircle(x + math.cos(b) * r * 1.18, y + math.sin(b) * r * 1.18, r * .05, p)
            cv.c.drawCircle(x, y, r * .13, p)
        elif part == "inner":
            for k in range(8):
                a = k * math.tau / 8
                cv.c.drawPath(smooth_path(petal_pts(x, y, r * .46, r * .12, a, n=12)), p)
    else:  # small tabur flower
        if part == "petal":
            cv.c.drawCircle(x, y, r * .26, p)
        elif part == "rim":
            for k in range(4):
                a = k * math.tau / 4 + math.pi / 4
                cv.c.drawPath(smooth_path(petal_pts(x, y, r, r * .3, a, n=14)), p)
            for k in range(4):
                a = k * math.tau / 4
                cv.c.drawCircle(x + math.cos(a) * r * .85, y + math.sin(a) * r * .85, r * .09, p)
        elif part == "inner":
            cv.c.drawCircle(x, y, r * .1, p)


# ---------------------------------------------------------------- cual (seamless 480 tile, shown at 240)
if "cual" in PARTS:
    W = H = 480
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n0 = wrap_noise(W, H, 301, 40)
    rgb = C(RED)[None, None] * (1 - n0[..., None] * .5) + C(RED_D)[None, None] * (n0[..., None] * .5)
    # ikat bands: soft rose lozenge lattice whose edges bleed along the warp (vertical)
    def lozenge(cv, x, y, it):
        s = it[2]
        cv.c.drawPath(poly_path([(x, y - s), (x + s * .62, y), (x, y + s), (x - s * .62, y)]), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    loz = wrapped(W, H, lozenge, [(0, 0, 150), (240, 240, 150), (240, 0, 150), (0, 240, 150)])
    hole = wrapped(W, H, lozenge, [(0, 0, 112), (240, 240, 112), (240, 0, 112), (0, 240, 112)])
    band = np.clip(loz - hole, 0, 1)
    bleed = gaussian_filter(band, (9, 1.5), mode="wrap")
    streak = wrap_noise(W, H, 302, (12, 0.8))
    bleed = np.clip(bleed * (0.45 + 1.1 * streak) * 1.3, 0, 1) * (0.6 + 0.4 * wrap_noise(W, H, 306, 20))
    rgb = lay(rgb, bleed * .55, ROSE)
    # warp + weft texture
    weft, wt = floats(W, H, 3.0, .6, seed=303)
    warp, _ = floats(W, H, 4.0, .5, seed=304, vertical=True)
    rgb = rgb * (0.9 + 0.1 * weft[..., None]) * (0.95 + 0.05 * warp[..., None]) * (0.96 + 0.08 * wt[..., None])
    # supplementary-weft motifs (thread floats)
    items = [(120, 120, 66, "big"), (360, 360, 66, "big"), (360, 120, 30, "small"), (120, 360, 30, "small")]
    fl, ft = floats(W, H, 2.4, .78, seed=305)
    m_pet = wrapped(W, H, lambda cv, x, y, it: flower_draw(cv, x, y, it, "petal"), items)
    m_rim = wrapped(W, H, lambda cv, x, y, it: flower_draw(cv, x, y, it, "rim"), items)
    m_in = wrapped(W, H, lambda cv, x, y, it: flower_draw(cv, x, y, it, "inner"), items)
    rgb = lay(rgb, m_pet * fl * .95, ROSE_L, ft, .3)
    m_vein = wrapped(W, H, lambda cv, x, y, it: flower_draw(cv, x, y, it, "vein"), items)
    pass
    rgb = lay(rgb, m_rim * fl, GOLD, ft, .5)
    rgb = lay(rgb, m_in * fl, GOLD_L, ft, .4)
    # tiny gold dots between (bunga tabur)
    def dot(cv, x, y, it):
        cv.c.drawCircle(x, y, 3.2, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    pts = [(x, y, 0) for x in (0, 240) for y in (0, 240)] + [(60 + 120 * i + 0, 60 + 120 * j) for i in range(4) for j in range(4) if (i + j) % 2 == 0 and (i, j) not in ((0, 0),)]
    pts = [(x, y, 0) for (x, y, *_) in [(p[0], p[1]) for p in pts]]
    rgb = lay(rgb, wrapped(W, H, dot, [(x, y, 0) for x in (0, 240) for y in (0, 240)]), GOLD, ft, .5)
    # subtle shadow under gold floats (relief)
    relief = np.roll(np.roll(np.clip(m_rim * fl, 0, 1), 1, 0), 1, 1)
    rgb *= (1 - 0.12 * gaussian_filter(relief, .8, mode="wrap")[..., None] * (1 - m_rim[..., None]))
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/cual.webp", quality=80)
    tiled = np.tile(arr, (2, 2, 1))
    prev(tiled, "bc-cual", bg="#000000")
    clear()

# ---------------------------------------------------------------- tumpal (horizontal repeat strip 480x104 -> 240x52)
if "tumpal" in PARTS:
    W, H = 480, 104
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rgb = np.ones((H, W, 3), np.float32) * C(MAROON)
    weft, wt = floats(W, H, 3.0, .6, seed=311)
    fl, ft = floats(W, H, 2.4, .8, seed=312)
    P = 80
    def tri(cv, x, y, it):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if it[2] == "out":
            cv.c.drawPath(poly_path([(x - 34, 86), (x, 18), (x + 34, 86), (x + 27, 86), (x, 32), (x - 27, 86)]), p)
        elif it[2] == "in":
            cv.c.drawPath(smooth_path(petal_pts(x, 80, 40, 11, -math.pi / 2, n=14)), p)
            for sgn in (-1, 1):
                cv.c.drawPath(smooth_path(petal_pts(x, 82, 22, 7, -math.pi / 2 + sgn * .7, n=12)), p)
        elif it[2] == "dot":
            cv.c.drawCircle(x, 62, 3.4, p)
            cv.c.drawCircle(x + 40, 74, 4.2, p)
    xs = [P / 2 + P * i for i in range(W // P)]
    m_out = wrapped(W, H, tri, [(x, 0, "out") for x in xs])
    m_in = wrapped(W, H, tri, [(x, 0, "in") for x in xs])
    m_dot = wrapped(W, H, tri, [(x, 0, "dot") for x in xs])
    bands = ((np.abs(yy - 92) < 4) | (np.abs(yy - 9) < 2.5)).astype(np.float32)
    def dia(cv, x, y, it):
        cv.c.drawPath(poly_path([(x, 92 - 7), (x + 6, 92), (x, 92 + 7), (x - 6, 92)]), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    m_dia = wrapped(W, H, dia, [(20 * i, 0) for i in range(W // 20)])
    rgb = rgb * (0.88 + 0.12 * weft[..., None])
    rgb = lay(rgb, m_in * fl, ROSE_L, ft, .3)
    rgb = lay(rgb, np.maximum(m_out, bands) * fl, GOLD, ft, .5)
    rgb = lay(rgb, np.maximum(m_dot, m_dia) * fl, GOLD_L, ft, .4)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/tumpal.webp", quality=82)
    prev(np.tile(arr, (1, 2, 1)), "bc-tumpal", bg="#000000")
    clear()

# ---------------------------------------------------------------- kembang (woven emblem, transparent, 300)
if "kembang" in PARTS:
    W = H = 300
    items = [(150, 150, 118, "big")]
    one = lambda part: wrapped(W * 3, H * 3, lambda cv, x, y, it: flower_draw(cv, x, y, it, part), [(450, 450, 96, "big")])[300:600, 300:600]
    m_pet, m_rim, m_in, m_vein = one("petal"), one("rim"), one("inner"), one("vein")
    fl, ft = floats(W, H, 2.6, .8, seed=321)
    sil = np.clip(np.maximum.reduce([m_pet, m_rim, m_in]), 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * C(RED)
    rgb = lay(rgb, m_pet * (0.55 + .45 * fl), ROSE_L, ft, .3)
    pass
    rgb = lay(rgb, m_rim * (0.35 + .65 * fl), GOLD, ft, .5)
    rgb = lay(rgb, m_in * (0.35 + .65 * fl), GOLD_L, ft, .4)
    a = np.clip(gaussian_filter(sil, .6), 0, 1)
    arr = np.concatenate([rgb, a[..., None]], -1)
    save(arr, f"{OUT}/kembang.webp", max_w=300)
    prev(arr, "bc-kembang", bg="#f4ead8")
    prev(arr, "bc-kembang-d", bg="#7d1f2a")
    clear()

# ---------------------------------------------------------------- pantai (gouache scene 840x560 -> 820)
if "pantai" in PARTS:
    W, H = 840, 560
    rng = random.Random(331); nx = Seq(331000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    HZ = 250
    art = painted_sky(W, H, [(0, "#f6e6d2"), (.3, "#f1dccb"), (.45, "#cfe6df"), (1, "#cfe6df")], seed=nx(), streak=.8)
    # far island + clouds
    cl = ellipses(W, H, [(160, 80, 120, 16, -2), (250, 66, 70, 12, 3), (640, 110, 150, 14, 1), (720, 96, 70, 12, 0)])
    art = GP(art, cl, "#fbf3ea", "#f3e6dc", seed=nx(), rough=6, streak=.9, density=.75)
    isl = shapes(W, H, [[(470, HZ + 2), (540, HZ - 26), (600, HZ - 34), (660, HZ - 20), (720, HZ + 2)]])
    art = GP(art, isl, "#9fb8ad", "#8eaa9f", seed=nx(), rough=3, density=.9)
    # sea: turquoise bands toward the shore
    sea = (yy >= HZ).astype(np.float32)
    art = GP(art, sea, "#3c9fa4", "#2f8b93", seed=nx(), rough=1.5, streak=1.2)
    for y0, col, col2, d in [(HZ + 40, "#47b6b0", "#3eaaa6", .95), (HZ + 95, "#68cdbf", "#5cc4b8", .95), (HZ + 150, "#9fe0cf", "#8dd7c8", .9)]:
        wv = (yy >= y0 + 8 * np.sin(xx / 70 + y0)).astype(np.float32)
        art = GP(art, wv, col, col2, seed=nx(), rough=5, streak=1.2, density=d)
    # sand
    sand = (yy >= 430 + 14 * np.sin(xx / 120 + 1) + 6 * np.sin(xx / 37)).astype(np.float32)
    art = GP(art, sand, "#efe0c4", "#e7d3b2", seed=nx(), rough=4, streak=.8)
    foam = stroke_mask(W, H, [(x, 430 + 14 * math.sin(x / 120 + 1) + 6 * math.sin(x / 37) - 2) for x in range(-10, W + 10, 8)], 5)
    art = GP(art, foam, "#ffffff", seed=nx(), rough=5, density=.8, dry=.4)
    # ripple highlights
    rip = strokes(W, H, [([(x, y), (x + rng.uniform(18, 50), y + rng.uniform(-1, 1))], rng.uniform(1.4, 2.4)) for x, y in [(rng.uniform(0, W), rng.uniform(HZ + 10, 420)) for _ in range(70)]])
    art = GP(art, rip, "#e9fbf6", seed=nx(), rough=1, density=.7)
    # small granite rocks in the shallows (mid-ground)
    def boulder(cx, cy, rx, ry, rot, seed):
        r2 = random.Random(seed)
        pts = deform(ellipse_pts(cx, cy, rx, ry, 14, rot), r2, 2, .05)
        return shapes(W, H, [pts])
    def granite(art, bm, cx, cy, rx, ry, far=False):
        art = GP(art, bm, "#c3b6aa", "#b2a497", seed=nx(), rough=2.5, streak=.8)
        sh = bm * np.clip(((xx - cx) * .55 + (yy - cy) * .85) / (ry * 1.0) + .25, 0, 1) ** 1.1
        art = G(art, sh, "#5a4f56", "#6a5c60", seed=nx(), density=.95 if not far else .6, edge=.4, bloom=.3, rough=4, feather=3)
        core = bm * np.clip(((xx - cx) * .55 + (yy - cy) * .85) / (ry * 1.0) - .25, 0, 1)
        art = G(art, core, "#4a3f48", seed=nx(), density=.6, edge=.3, bloom=.2, rough=4, feather=4)
        hi = bm * np.clip(-((xx - cx) * .45 + (yy - cy)) / (ry * 1.1) - .15, 0, 1) ** .8
        art = OV(art, hi, lambda m: gouache_paint(m, "#efe6d9", "#e6dccd", seed=nx(), rough=6, density=.85, dry=.35))
        speck = (fbm(W, H, nx(), 1.6, 1) > .9).astype(np.float32) * bm * (sh < .5)
        art = GP(art, speck, "#7b6f6f", seed=nx(), rough=.3, density=.35)
        return art
    for k, (cx, cy, rx, ry) in enumerate([(470, 402, 40, 22), (430, 412, 22, 14), (250, 380, 34, 18), (690, 398, 30, 16)]):
        bm = boulder(cx, cy, rx, ry, 0, 360 + k) * (yy < cy + ry * .55)
        art = granite(art, bm, cx, cy, rx, ry, True)
        wl = stroke_mask(W, H, [(cx - rx * 1.1, cy + ry * .55), (cx + rx * 1.1, cy + ry * .55)], 3)
        art = GP(art, wl, "#e9fbf6", seed=nx(), rough=2, density=.7, dry=.3)
    # palms behind the house (own: thick trunk, broad drooping fronds)
    def coco(art, x, by, h, lean, seed):
        r2 = random.Random(seed)
        top = (x + lean * h, by - h)
        trunk = curve([(x, by), (x + lean * h * .25, by - h * .55), top], 30)
        tm = strokes(W, H, [(trunk, h * .05, (0.02, .5))])
        art = GP(art, tm, "#7d6450", "#5f4a3a", seed=nx(), rough=1.2, streak=1.4)
        rings = strokes(W, H, [([(px - h * .02, py), (px + h * .02, py + 1)], 1.2, None) for px, py in trunk[2:-2:2]]) * tm
        art = GP(art, rings, "#4a382c", seed=nx(), rough=.5, density=.6)
        items = []
        for k in range(11):
            a = -math.pi / 2 + (k - 5) * .36 + r2.uniform(-.1, .1)
            Lf = h * r2.uniform(.36, .48)
            droop = Lf * (.25 + .5 * abs(k - 5) / 5)
            pts = curve([top, (top[0] + math.cos(a) * Lf * .55, top[1] + math.sin(a) * Lf * .55 - h * .03),
                         (top[0] + math.cos(a) * Lf, top[1] + math.sin(a) * Lf + droop)], 26)
            items.append((pts, h * .016, (.05, .6)))
            for j in range(3, 24, 2):
                px, py = pts[j]; qx, qy = pts[j + 1]
                ta = math.atan2(qy - py, qx - px)
                ll = Lf * .2 * (1 - j / 26) + Lf * .05
                for sg in (-1, 1):
                    qa = ta + sg * 1.0 + .45
                    items.append(([(px, py), (px + math.cos(qa) * ll * 1.15, py + math.sin(qa) * ll * 1.15)], h * .014, (.05, .7)))
        fm = strokes(W, H, items)
        art = GP(art, fm, "#3d6b44", "#2c5233", seed=nx(), rough=1.6, streak=1)
        art = G(art, fm * np.clip((yy - top[1]) / (h * .3), 0, 1), "#1f3d27", seed=nx(), density=.4, edge=.2, rough=2)
        return art
    for x, h, ln, sd in [(740, 300, -.13, 1), (800, 236, -.22, 2), (372, 250, .16, 3)]:
        art = coco(art, x, 432, h, ln, sd)
        clear()
    # stilt house (rumah panggung Melayu, 3/4 view: front gable + side roof) standing over the shallows
    hx, hb = 560, 372
    fx0, fx1, sx1 = hx - 104, hx - 4, hx + 96   # front facade, side wall right edge
    wt, wb = hb - 150, hb - 62
    apex = ((fx0 + fx1) / 2, hb - 262)
    posts = strokes(W, H, [([(hx + dx, wb), (hx + dx + rng.uniform(-1.5, 1.5), hb + 26)], 5.5, None) for dx in (-100, -70, -36, -6, 30, 62, 92)])
    art = GP(art, posts, "#4e3324", seed=nx(), rough=1.2)
    refl = strokes(W, H, [([(hx + dx, hb + 28), (hx + dx + 3, hb + 64)], 4, None) for dx in (-100, -70, -36, -6, 30, 62, 92)])
    art = G(art, refl, "#2a6a6f", seed=nx(), density=.35, edge=.1, rough=2)
    front = shapes(W, H, [[(fx0, wt), (fx1, wt), (fx1, wb), (fx0, wb)]], smooth=False)
    side = shapes(W, H, [[(fx1, wt + 4), (sx1, wt + 10), (sx1, wb), (fx1, wb)]], smooth=False)
    art = GP(art, front, "#d2a36b", "#c4945c", seed=nx(), rough=1.4, streak=1.4)
    art = GP(art, side, "#a97a4c", "#9a6c42", seed=nx(), rough=1.4, streak=1.4)
    planks = strokes(W, H, [([(fx0 + i * 8, wt), (fx0 + i * 8, wb)], 1.1, None) for i in range(1, 26)])
    art = GP(art, planks * np.maximum(front, side), "#8a5d36", seed=nx(), rough=.5, density=.45)
    door = shapes(W, H, [[(hx - 66, wt + 18), (hx - 42, wt + 18), (hx - 42, wb), (hx - 66, wb)]], smooth=False)
    art = GP(art, door, "#3d2618", seed=nx(), rough=1)
    win = shapes(W, H, [[(x0, wt + 26 + (x0 - fx1) * .06), (x0 + 24, wt + 26 + (x0 + 24 - fx1) * .06), (x0 + 24, wt + 66), (x0, wt + 66)] for x0 in (fx1 + 14, fx1 + 54)] +
                 [[(fx0 + 10, wt + 26), (fx0 + 28, wt + 26), (fx0 + 28, wt + 62), (fx0 + 10, wt + 62)], [(fx1 - 28, wt + 26), (fx1 - 10, wt + 26), (fx1 - 10, wt + 62), (fx1 - 28, wt + 62)]], smooth=False)
    art = GP(art, win, "#3d2618", seed=nx(), rough=1)
    shut = shapes(W, H, [[(x0, wt + 24), (x0 + 6, wt + 24), (x0 + 6, wt + 66), (x0, wt + 66)] for x0 in (fx1 + 8, fx1 + 38, fx1 + 48, fx1 + 78)], smooth=False)
    art = GP(art, shut, "#2f6f6a", seed=nx(), rough=1)
    gable = shapes(W, H, [[(fx0 - 10, wt + 2), apex, (fx1 + 10, wt + 2)]], smooth=False)
    art = GP(art, gable, "#e7d3ae", "#dcc59c", seed=nx(), rough=1.2, streak=1)
    rays = strokes(W, H, [([(apex[0], wt - 6), (apex[0] + math.cos(a) * 80, wt - 6 + math.sin(a) * 80)], 1.6, None) for a in [-math.pi + .25 * i for i in range(1, 13)]]) * gable
    art = GP(art, rays, "#9c6a3c", seed=nx(), rough=.4, density=.7)
    roofs = shapes(W, H, [[apex, (sx1 + 34, apex[1] + 16), (sx1 + 62, wt + 18), (fx1 + 16, wt + 4)]], smooth=False)
    art = GP(art, roofs, "#7a2a25", "#66211e", seed=nx(), rough=1.8, streak=1.6)
    rib = strokes(W, H, [([(apex[0] + t * (sx1 + 34 - apex[0]), apex[1] + t * 16), (fx1 + 16 + t * (sx1 + 62 - fx1 - 16), wt + 4 + t * 14)], 1.0, None) for t in [i / 22 for i in range(1, 22)]]) * roofs
    art = GP(art, rib, "#9a4038", seed=nx(), rough=.4, density=.5)
    trim = strokes(W, H, [([(fx0 - 14, wt + 4), apex], 5, None), ([apex, (fx1 + 16, wt + 4)], 5, None),
                          ([(apex[0] - 16, apex[1] - 20), (apex[0] + 8, apex[1] + 8)], 4, None), ([(apex[0] + 16, apex[1] - 20), (apex[0] - 8, apex[1] + 8)], 4, None),
                          ([(fx1 + 16, wt + 5), (sx1 + 62, wt + 19)], 4, None)])
    art = GP(art, trim, "#f2e6cc", seed=nx(), rough=.7)
    fringe = strokes(W, H, [([(x, wt + 6 + (x - fx1) * .096 if x > fx1 else wt + 6), (x, wt + 14 + (x - fx1) * .096 if x > fx1 else wt + 14)], 2.4, None) for x in range(int(fx0) - 8, int(sx1) + 56, 7)])
    art = GP(art, fringe, "#f2e6cc", seed=nx(), rough=.4, density=.85)
    deck = shapes(W, H, [[(fx0 - 14, wb - 2), (sx1 + 12, wb - 2), (sx1 + 12, wb + 9), (fx0 - 14, wb + 9)]], smooth=False)
    art = GP(art, deck, "#5e3e28", seed=nx(), rough=1.2)
    ladder = strokes(W, H, [([(fx0 - 4, wb + 6), (fx0 - 30, hb + 26)], 3, None), ([(fx0 + 12, wb + 6), (fx0 - 14, hb + 26)], 3, None)] + [([(fx0 - 6 - k * 5.2, wb + 20 + k * 16), (fx0 + 10 - k * 5.2, wb + 20 + k * 16)], 2.4, None) for k in range(5)])
    art = GP(art, ladder, "#4e3324", seed=nx(), rough=.8)
    art = G(art, np.maximum(side, roofs * (xx > apex[0] + 40)) * .7, "#5a3a3a", seed=nx(), density=.22, edge=.1, bloom=.3, rough=3)
    clear()
    # granite boulders: big rounded tors in the foreground, left + right (light from the top-left)
    rocks = [(70, 470, 150, 120, -.2), (230, 520, 120, 80, .1), (-20, 360, 110, 120, 0), (150, 390, 72, 60, .3),
             (800, 500, 130, 96, .2), (690, 540, 100, 56, 0), (900, 400, 120, 110, 0)]
    for k, (cx, cy, rx, ry, rot) in enumerate(rocks):
        bm = boulder(cx, cy, rx, ry, rot, 340 + k)
        art = granite(art, bm, cx, cy, rx, ry)
        crack = stroke_mask(W, H, [(cx - rx * .3, cy - ry * .7), (cx - rx * .12, cy - ry * .1), (cx + rx * .02, cy + ry * .6)], 2.0) * bm
        art = G(art, crack, "#4f4448", seed=nx(), density=.6, edge=.2, rough=1)
        clear()
    art = add_grain(art, 333, .03)
    save_rgb(art, f"{OUT}/pantai.webp", size=(820, 547), quality=78)
    prev(art, "bc-pantai", bg="#ffffff")
    clear()
