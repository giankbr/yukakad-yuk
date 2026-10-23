"""Piknik Gingham — a top-down picnic flat-lay in matte gouache, light from the top-left with soft cast shadows on the
cloth: a rattan basket (woven body, braided rim, handles) holding a gingham napkin, a baguette and apples; a ceramic
plate of watermelon, strawberries and grapes; two glasses of lemonade with lemon wheels, ice and striped straws; a
wooden board of sandwiches; a tied bunch of wildflowers (daisies, cornflowers, poppies); a daisy-chain divider; and a
woven red gingham cloth tile. Run: python3 -I piknik-gingham.py [part ...]
parts: cloth basket fruit lemonade sandwich flowers chain"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k6_lib import *

OUT = outdir("piknik-gingham")
PARTS = sys.argv[1:] or ["cloth", "basket", "fruit", "lemonade", "sandwich", "flowers", "chain"]
RED, RED_D, RED_L = "#d8443a", "#a82e28", "#ef7a6a"
CREAM = "#fff8ea"
RATTAN, RATTAN_D, RATTAN_L = "#c98f55", "#8a5a2e", "#e9bf86"
LEAF, LEAF_D, LEAF_L = "#6f9a4a", "#4b7232", "#a6c97a"
LEMON, LEMON_D = "#f5cf3d", "#d9a91e"
SHADOW = "#5a2a22"
nx = Seq(900)


def drop(art, mask, blur=7, strength=0.32, dx=6, dy=8, col=SHADOW):
    return over(art, soft_shadow(mask, col, blur, strength, dx, dy))


def body(art, mask, col, col2=None, shade=None, hi=0.35, sh=0.3, blur=12, rough=1.4):
    art = GP(art, mask, col, col2, seed=nx(), rough=rough, streak=0.9, pad=10)
    art = shade_side(art, mask, shade or mix(col, "#2a1a10", 0.45), (1, 1), sh, blur, nx())
    if hi:
        art = highlight(art, mask, "#ffffff", hi, blur)
    return art


def weave_map(W, H, cell=26, ang=0.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ca, sa = math.cos(ang), math.sin(ang)
    u, v = xx * ca + yy * sa, -xx * sa + yy * ca
    i = np.floor(u / cell); j = np.floor(v / cell)
    par = ((i + j) % 2) == 0
    k = cell / 3.0
    prof_h = np.sin(np.pi * ((v % k) / k)) ** 0.6
    prof_v = np.sin(np.pi * ((u % k) / k)) ** 0.6
    edge_h = np.sin(np.pi * ((u % cell) / cell)) ** 0.25
    edge_v = np.sin(np.pi * ((v % cell) / cell)) ** 0.25
    return np.where(par, prof_h * edge_h, prof_v * edge_v).astype(np.float32)


def textured(mask, lum, dark, light, seed):
    h, w = mask.shape
    d, l = col_arr(dark), col_arr(light)
    n = fbm(w, h, seed, 40, 3)[..., None]
    L = np.clip(lum[..., None] * (0.85 + 0.3 * n), 0, 1)
    rgb = d * (1 - L) + l * L
    m = np.clip((gaussian_filter(displace(mask, seed, 1.2, 20), 0.7) - 0.35) * 2.2, 0, 1)
    return np.concatenate([rgb, m[..., None]], -1)


def cloth():
    W = H = 384
    g = gingham(W, H, 24, RED, CREAM, seed=nx(), alpha=0.5, warp_jit=0.7)
    g[..., :3] *= (0.96 + 0.06 * fbm(W, H, nx(), 90, 3))[..., None]
    save_rgb(tileable(g), f"{OUT}/cloth.webp", quality=78)


def basket():
    W, H = 760, 620
    art = blank(W, H)
    outer = rrect(W, H, 70, 90, 690, 540, 70, rot=-4)
    inner = rrect(W, H, 112, 132, 648, 498, 44, rot=-4)
    art = drop(art, outer, 12, 0.38, 14, 18)
    # handle folded flat over the far rim
    hl = polyline_mask(W, H, [curve([(180, 120), (240, 40), (520, 30), (590, 110)], 40)], 30)
    art = drop(art, hl, 6, 0.3, 8, 10)
    art = OV(art, hl, lambda m: textured(m, weave_map(m.shape[1], m.shape[0], 9, 0.8), RATTAN_D, RATTAN_L, nx()))
    rim = np.clip(outer - inner, 0, 1)
    art = OV(art, inner, lambda m: textured(m, weave_map(m.shape[1], m.shape[0], 30, math.radians(-4)), "#7a4a22", RATTAN, nx()))
    art = shade_side(art, inner, "#4a2a12", (-1, -1), 0.45, 26, nx())  # inner wall shadow
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    braid = (0.5 + 0.5 * np.sin((xx * 0.8 + yy) / 4.5)) ** 0.8 * (0.8 + 0.2 * fbm(W, H, nx(), 6, 2))
    art = over(art, textured(rim, braid, RATTAN_D, RATTAN_L, nx()))
    art = highlight(art, rim, "#fff3d6", 0.3, 10)
    # contents: gingham napkin, baguette, apples
    nap = shapes(W, H, [[(150, 300), (230, 170), (380, 190), (420, 300), (360, 460), (200, 470)]])
    art = drop(art, nap, 6, 0.3, 6, 8)
    g = gingham(W, H, 14, RED, CREAM, seed=nx(), alpha=0.55, warp_jit=2.5)
    g[..., 3] = np.clip((gaussian_filter(displace(nap, nx(), 2, 30), 0.8) - 0.35) * 2.2, 0, 1)
    art = over(art, g)
    for p in ([(210, 220), (290, 300), (330, 430)], [(180, 360), (260, 380), (300, 460)]):
        art = over(art, flat(gaussian_filter(polyline_mask(W, H, [curve(p, 20)], 8), 4), "#6a2018", 0.25))
    art = shade_side(art, nap, "#5a1a10", (1, 1), 0.25, 18, nx())
    bag = ell(W, H, 500, 320, 52, 190, -28)
    art = drop(art, bag, 7, 0.35, 8, 10)
    art = body(art, bag, "#d99a4c", "#c07a34", "#7a4416", 0.4, 0.4, 16)
    scores = polyline_mask(W, H, [[(470 + (k - 2) * 52 * math.sin(math.radians(28)) - 18, 320 + (k - 2) * 52 * math.cos(math.radians(28)) - 10), (470 + (k - 2) * 52 * math.sin(math.radians(28)) + 40, 320 + (k - 2) * 52 * math.cos(math.radians(28)) + 6)] for k in range(5)], 9)
    art = GP(art, scores * bag, "#f3d79a", seed=nx(), rough=1.0, pad=4)
    for cx, cy in ((590, 220), (575, 430), (430, 455)):
        ap = circles(W, H, [(cx, cy, 44)])
        art = drop(art, ap, 6, 0.35, 7, 9)
        art = body(art, ap, RED, "#b9322a", "#6e1610", 0.5, 0.45, 14)
        art = over(art, flat(gaussian_filter(ell(W, H, cx - 14, cy - 16, 12, 7, -35), 2), "#ffffff", 0.55))
        art = GP(art, strokes(W, H, [([(cx + 2, cy - 2), (cx + 8, cy - 14)], 4, None)]), "#5a3a1a", seed=nx(), rough=0.4, pad=4)
        art = GP(art, shapes(W, H, [petal_pts(cx + 8, cy - 12, 22, 9, math.radians(-30))]), LEAF, seed=nx(), rough=0.6, pad=4)
    art = add_grain(art, nx(), 0.03)
    prev(art, "pg-basket", tone="#f4e3d3")
    save(art, f"{OUT}/basket.webp", max_w=560, quality=80)


def strawberry(art, W, H, cx, cy, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    pts = [P(0, -22 * s), P(16 * s, -16 * s), P(18 * s, 0), P(8 * s, 20 * s), P(0, 26 * s), P(-8 * s, 20 * s), P(-18 * s, 0), P(-16 * s, -16 * s)]
    m = shapes(W, H, [pts])
    art = drop(art, m, 4, 0.3, 4, 5)
    art = body(art, m, "#e0372f", "#c22a25", "#7a1010", 0.45, 0.35, 8)
    rng = random.Random(nx())
    seeds = [P(rng.uniform(-11, 11) * s, rng.uniform(-10, 18) * s) for _ in range(12)]
    art = over(art, flat(ellipses(W, H, [(x, y, 1.8 * s, 1.2 * s, math.degrees(ang)) for x, y in seeds]) * m, "#f6e08a", 0.9))
    cal = shapes(W, H, [petal_pts(*P(0, -22 * s), 15 * s, 6 * s, ang - math.pi / 2 + d, n=10) for d in (-1.1, -0.4, 0.3, 1.0)])
    art = GP(art, cal, LEAF, LEAF_D, seed=nx(), rough=0.6, pad=4)
    return art


def fruit():
    W = H = 620; C = 310
    art = blank(W, H)
    plate = circles(W, H, [(C, C, 270)])
    art = drop(art, plate, 14, 0.35, 14, 18)
    art = body(art, plate, "#fbfaf5", "#eef0ec", "#9aa6b0", 0.0, 0.35, 30, rough=0.6)
    well = circles(W, H, [(C, C, 205)])
    art = shade_side(art, well, "#8f9ca8", (-1, -1), 0.3, 14, nx())
    art = over(art, flat(ring(W, H, C, C, 250, 6), "#5a7fa8", 0.55))
    # watermelon slices fanned
    for k, a in enumerate([-2.5, -1.95, -1.4]):
        cx, cy = C + math.cos(a) * 20, C + math.sin(a) * 20
        tri = [(cx, cy)] + arc_pts(cx, cy, 190, a - 0.26, a + 0.26, 12)
        m = shapes(W, H, [tri], smooth=False)
        art = drop(art, m, 5, 0.3, 5, 7)
        rind = np.clip(m - shapes(W, H, [[(cx, cy)] + arc_pts(cx, cy, 168, a - 0.25, a + 0.25, 12)], smooth=False), 0, 1)
        art = body(art, m, "#ee4b52", "#e23a48", "#a51f2a", 0.3, 0.2, 10)
        art = GP(art, rind, "#4f8a3a", "#6aa04a", seed=nx(), rough=0.8, pad=4)
        art = GP(art, np.clip(shapes(W, H, [[(cx, cy)] + arc_pts(cx, cy, 172, a - 0.25, a + 0.25, 12)], smooth=False) - shapes(W, H, [[(cx, cy)] + arc_pts(cx, cy, 160, a - 0.25, a + 0.25, 12)], smooth=False), 0, 1), "#eef3d8", seed=nx(), rough=0.6, pad=4)
        rng = random.Random(nx())
        sd = []
        for _ in range(7):
            rr = rng.uniform(60, 145); aa = a + rng.uniform(-0.16, 0.16)
            sd.append((cx + math.cos(aa) * rr, cy + math.sin(aa) * rr, 6, 3.5, math.degrees(aa)))
        art = over(art, flat(ellipses(W, H, sd), "#2a1a1a", 0.9))
    # grapes
    rng = random.Random(nx())
    for k in range(16):
        gx, gy = C + 120 + rng.uniform(-60, 60), C + 40 + rng.uniform(-50, 90)
        g = circles(W, H, [(gx, gy, 24)])
        art = drop(art, g, 3, 0.25, 3, 4)
        art = body(art, g, "#7a3d82", "#5e2a6a", "#2a0f30", 0.0, 0.4, 7)
        art = over(art, flat(gaussian_filter(ell(W, H, gx - 7, gy - 8, 6, 4, -30), 1.5), "#e9d8f0", 0.7))
    art = GP(art, polyline_mask(W, H, [curve([(C + 150, C - 50), (C + 128, C + 10), (C + 120, C + 80)], 20)], 5), "#6b5a2a", seed=nx(), rough=0.5, pad=4)
    # strawberries
    for cx, cy, ang in ((C - 60, C + 120, 0.4), (C - 140, C + 60, -0.6), (C + 10, C + 190, 1.2), (C - 120, C + 170, 2.2), (C + 30, C + 60, -1.8)):
        art = strawberry(art, W, H, cx, cy, 1.7, ang)
    art = add_grain(art, nx(), 0.03)
    prev(art, "pg-fruit", tone="#f4e3d3")
    save(art, f"{OUT}/fruit.webp", max_w=380, quality=80)


def lemon_wheel(art, W, H, cx, cy, r, seg=True):
    m = circles(W, H, [(cx, cy, r)])
    art = GP(art, m, LEMON_D, seed=nx(), rough=0.6, pad=4)
    pith = circles(W, H, [(cx, cy, r * 0.9)])
    art = GP(art, pith, "#fbf3c8", seed=nx(), rough=0.5, pad=4)
    if seg:
        segs = []
        for k in range(9):
            a0 = k * math.tau / 9
            segs.append([(cx + math.cos(a0 + 0.06) * r * 0.12, cy + math.sin(a0 + 0.06) * r * 0.12)] + arc_pts(cx, cy, r * 0.82, a0 + 0.08, a0 + math.tau / 9 - 0.08, 6))
        sm = shapes(W, H, segs)
        art = GP(art, sm, LEMON, "#f8dd6a", seed=nx(), rough=0.6, pad=4)
        art = highlight(art, sm, "#ffffff", 0.3, 4)
    return art


def lemonade():
    W, H = 640, 520
    art = blank(W, H)
    for cx, cy, r, sa in ((210, 230, 150, -0.7), (460, 330, 132, 0.5)):
        glass = circles(W, H, [(cx, cy, r)])
        art = drop(art, glass, 12, 0.22, 12, 16, "#7a5a3a")
        art = over(art, flat(glass, "#dfeef0", 0.55))
        liquid = circles(W, H, [(cx, cy, r * 0.86)])
        art = G(art, liquid, "#f7e27a", "#f2d24f", seed=nx(), density=0.8, edge=0.35, bloom=0.2, rough=1.5, feather=1.0)
        rng = random.Random(nx())
        for k in range(3):
            a = rng.uniform(0, math.tau); d = r * 0.45
            ice = rrect(W, H, cx + math.cos(a) * d - 26, cy + math.sin(a) * d - 26, cx + math.cos(a) * d + 26, cy + math.sin(a) * d + 26, 10, rot=rng.uniform(0, 80))
            art = over(art, flat(gaussian_filter(ice, 1.5), "#ffffff", 0.45))
            art = highlight(art, ice, "#ffffff", 0.5, 5)
        art = lemon_wheel(art, W, H, cx - r * 0.1, cy + r * 0.05, r * 0.42)
        rim = ring(W, H, cx, cy, r, 10)
        art = over(art, flat(rim, "#ffffff", 0.75))
        art = shade_side(art, rim, "#8aa9b0", (1, 1), 0.5, 6, nx())
        # striped straw from the centre out past the rim
        x0, y0 = cx + r * 0.15, cy - r * 0.1
        x1, y1 = cx + math.cos(sa - 1.3) * (r + 70), cy + math.sin(sa - 1.3) * (r + 70)
        st = polyline_mask(W, H, [[(x0, y0), (x1, y1)]], 16)
        art = drop(art, st, 3, 0.25, 4, 6)
        L = math.hypot(x1 - x0, y1 - y0)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        tpar = ((xx - x0) * (x1 - x0) + (yy - y0) * (y1 - y0)) / L
        stripes = ((tpar / 14) % 2 < 1).astype(np.float32)
        art = GP(art, st, "#ffffff", seed=nx(), rough=0.4, pad=4)
        art = GP(art, st * stripes, RED, seed=nx(), rough=0.4, pad=4)
        art = shade_side(art, st, "#7a2a20", (1, 1), 0.3, 4, nx())
    # a whole lemon + a half
    lm = ell(W, H, 520, 110, 62, 48, 20)
    art = drop(art, lm, 6, 0.32, 7, 9)
    art = body(art, lm, LEMON, LEMON_D, "#9a6a10", 0.5, 0.4, 14)
    art = over(art, flat(ell(W, H, 580, 130, 8, 6, 20), "#9aa040", 0.8))
    hl = circles(W, H, [(120, 440, 62)])
    art = drop(art, hl, 6, 0.32, 7, 9)
    art = lemon_wheel(art, W, H, 120, 440, 62)
    lf = shapes(W, H, [petal_pts(560, 60, 70, 26, math.radians(-40), n=14)])
    art = body(art, lf, LEAF, LEAF_D, LEAF_D, 0.3, 0.3, 8)
    art = over(art, flat(polyline_mask(W, H, [[(560, 60), (612, 16)]], 2.2), LEAF_D, 0.7))
    art = add_grain(art, nx(), 0.03)
    prev(art, "pg-lemonade", tone="#f4e3d3")
    save(art, f"{OUT}/lemonade.webp", max_w=380, quality=80)


def sandwich():
    W, H = 700, 560
    art = blank(W, H)
    board = rrect(W, H, 60, 90, 600, 470, 40, rot=6)
    hold = rrect(W, H, 560, 230, 690, 330, 46, rot=6)
    hole = circles(W, H, [(652, 288, 18)])
    bm = np.clip(np.maximum(board, hold) - hole, 0, 1)
    art = drop(art, bm, 12, 0.38, 14, 18)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    grain = (0.5 + 0.5 * np.sin((yy * 0.98 - xx * 0.1 + (fbm(W, H, nx(), 90, 3) - 0.5) * 22) / 3.4)) ** 2
    art = OV(art, bm, lambda m: textured(m, grain[:m.shape[0], :m.shape[1]] * 0.6 + 0.3, "#b07a46", "#e3b27c", nx()), pad=0)
    art = highlight(art, bm, "#fff4dc", 0.25, 18)
    art = shade_side(art, bm, "#6a3e18", (1, 1), 0.3, 14, nx())
    for cx, cy, ang in ((220, 250, 10), (390, 330, 190), (250, 390, 100)):
        a = math.radians(ang)
        def P(u, v):
            return (cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a))
        tri = [P(-110, -70), P(110, -70), P(-110, 90)]
        lettuce = shapes(W, H, [[P(-118, -78), P(118, -76), P(-116, 98)]], smooth=False)
        lettuce = displace(lettuce, nx(), 5, 6)
        art = drop(art, lettuce, 6, 0.3, 6, 8)
        art = GP(art, lettuce, "#7fb04f", "#5f9a3a", seed=nx(), rough=2.5, pad=8)
        tom = shapes(W, H, [[P(-60, -76), P(40, -78), P(-10, -66)]])
        art = GP(art, tom, "#e0473a", seed=nx(), rough=1.5, pad=6)
        bread = shapes(W, H, [tri], smooth=False)
        bread = gaussian_filter(bread, 3)
        bread = (bread > 0.5).astype(np.float32)
        art = body(art, bread, "#d99a4c", "#c98a3e", "#7a4416", 0.2, 0.3, 10, rough=1.2)
        crumb = shapes(W, H, [[P(-100, -61), P(92, -61), P(-100, 74)]], smooth=False)
        crumb = (gaussian_filter(crumb, 4) > 0.5).astype(np.float32)
        art = GP(art, crumb, "#f8e8c4", "#f0dcae", seed=nx(), rough=1.0, pad=6)
        pores = (fbm(W, H, nx(), 5, 2) > 0.7).astype(np.float32) * crumb
        art = over(art, flat(gaussian_filter(pores, 0.6), "#d8b880", 0.45))
    art = add_grain(art, nx(), 0.03)
    prev(art, "pg-sandwich", tone="#f4e3d3")
    save(art, f"{OUT}/sandwich.webp", max_w=380, quality=80)


def daisy(art, W, H, cx, cy, r, rng, col="#ffffff", centre=LEMON_D, n=14):
    pet = []
    for k in range(n):
        a = k * math.tau / n + rng.uniform(-0.08, 0.08)
        pet.append(petal_pts(cx + math.cos(a) * r * 0.15, cy + math.sin(a) * r * 0.15, r * rng.uniform(0.85, 1.0), r * 0.26, a, n=10))
    pm = shapes(W, H, pet)
    art = drop(art, pm, 3, 0.22, 3, 4)
    art = GP(art, pm, col, "#f1ede2", seed=nx(), rough=0.8, pad=4)
    art = shade_side(art, pm, "#b8b0a0", (1, 1), 0.35, 5, nx())
    c = circles(W, H, [(cx, cy, r * 0.28)])
    art = body(art, c, LEMON, centre, "#9a6a10", 0.3, 0.4, 5)
    return art


def cornflower(art, W, H, cx, cy, r, rng):
    pts = []
    for k in range(9):
        a = k * math.tau / 9 + rng.uniform(-0.1, 0.1)
        pts.append([(cx, cy)] + [(cx + math.cos(a + d) * r * rr, cy + math.sin(a + d) * r * rr) for d, rr in ((-0.25, 0.7), (-0.18, 1.0), (-0.06, 0.82), (0.06, 1.0), (0.18, 0.8), (0.25, 0.65))])
    m = shapes(W, H, pts, smooth=False)
    art = drop(art, m, 3, 0.22, 3, 4)
    art = GP(art, m, "#3f6fd0", "#5a86de", seed=nx(), rough=1.0, pad=4)
    art = shade_side(art, m, "#1f3a8a", (1, 1), 0.35, 5, nx())
    art = over(art, flat(circles(W, H, [(cx, cy, r * 0.22)]), "#2a3a7a", 0.9))
    return art


def poppy(art, W, H, cx, cy, r, rng):
    pet = [ell(W, H, cx + math.cos(a) * r * 0.42, cy + math.sin(a) * r * 0.42, r * 0.62, r * 0.55, math.degrees(a)) for a in [rng.uniform(0, 1) + k * math.tau / 4 for k in range(4)]]
    m = np.maximum.reduce(pet)
    m = displace(m, nx(), 3, 10)
    art = drop(art, m, 4, 0.25, 4, 5)
    art = body(art, m, "#e8392e", "#d42a24", "#8a1010", 0.3, 0.3, 8)
    for p in pet[:2]:
        art = shade_side(art, p, "#9a1a14", (1, 1), 0.18, 6, nx())
    art = over(art, flat(circles(W, H, [(cx, cy, r * 0.22)]), "#2a1a1a", 0.92))
    art = over(art, flat(polyline_mask(W, H, [[(cx + math.cos(a) * r * 0.22, cy + math.sin(a) * r * 0.22), (cx + math.cos(a) * r * 0.36, cy + math.sin(a) * r * 0.36)] for a in np.linspace(0, math.tau, 14)], 1.6), "#2a1a1a", 0.8))
    return art


def flowers():
    W, H = 760, 620
    art = blank(W, H)
    rng = random.Random(nx())
    tie = (300, 470)
    heads = [(170, 150, "d", 46), (280, 90, "c", 40), (400, 120, "p", 58), (520, 190, "d", 42), (230, 250, "p", 50), (360, 240, "d", 50), (480, 300, "c", 36), (130, 300, "c", 34), (600, 110, "d", 34), (300, 330, "b", 18), (440, 400, "b", 16), (560, 290, "b", 18), (200, 380, "b", 14)]
    stems = []
    for x, y, *_ in heads:
        stems.append((curve([(x, y), ((x + tie[0]) / 2 + rng.uniform(-20, 20), (y + tie[1]) / 2), tie, (tie[0] - (x - tie[0]) * 0.35, tie[1] + 120)], 30), 6, None))
    for k in range(9):
        a = rng.uniform(-2.6, -0.5); L = rng.uniform(160, 300)
        stems.append((curve([(tie[0] + math.cos(a) * L, tie[1] + math.sin(a) * L), (tie[0] + math.cos(a) * L * 0.5, tie[1] + math.sin(a) * L * 0.5), tie, (tie[0] - math.cos(a) * 110, tie[1] - math.sin(a) * 110)], 30), 4.5, (0.4, 0.05)))
    sm = strokes(W, H, stems)
    art = drop(art, sm, 4, 0.25, 4, 6)
    art = GP(art, sm, LEAF, LEAF_D, seed=nx(), rough=0.8, pad=6)
    lv = shapes(W, H, [petal_pts(tie[0] + math.cos(a) * 80, tie[1] + math.sin(a) * 80, 90, 24, a, n=12) for a in (-2.4, -1.0, -1.9)])
    art = body(art, lv, LEAF, LEAF_D, LEAF_D, 0.25, 0.3, 8)
    # twine bow
    tw = polyline_mask(W, H, [[(tie[0] - 34, tie[1] - 10), (tie[0] + 34, tie[1] + 10)], curve([(tie[0], tie[1]), (tie[0] - 50, tie[1] - 40), (tie[0] - 60, tie[1] + 10), (tie[0], tie[1])], 20), curve([(tie[0], tie[1]), (tie[0] + 50, tie[1] - 30), (tie[0] + 64, tie[1] + 16), (tie[0], tie[1])], 20), [(tie[0], tie[1]), (tie[0] - 30, tie[1] + 70)], [(tie[0], tie[1]), (tie[0] + 18, tie[1] + 78)]], 5)
    art = drop(art, tw, 3, 0.3, 3, 4)
    art = GP(art, tw, "#d8b98a", "#bf9a66", seed=nx(), rough=0.5, pad=4)
    for x, y, kind, r in heads:
        if kind == "d":
            art = daisy(art, W, H, x, y, r, rng)
        elif kind == "c":
            art = cornflower(art, W, H, x, y, r, rng)
        elif kind == "p":
            art = poppy(art, W, H, x, y, r, rng)
        else:
            m = circles(W, H, [(x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5, r * 0.55) for a in np.linspace(0, math.tau, 6)[:-1]])
            art = body(art, m, LEMON, LEMON_D, "#9a6a10", 0.35, 0.3, 4)
    art = add_grain(art, nx(), 0.03)
    prev(art, "pg-flowers", tone="#f4e3d3")
    save(art, f"{OUT}/flowers.webp", max_w=400, quality=80)


def chain():
    W, H = 780, 150
    art = blank(W, H)
    rng = random.Random(nx())
    stem = strokes(W, H, [(curve([(20, 86), (200, 66), (390, 90), (580, 64), (760, 84)], 60), 5, None)])
    art = GP(art, stem, LEAF, LEAF_D, seed=nx(), rough=0.6, pad=6)
    lv = shapes(W, H, [petal_pts(x, y, 40, 13, a, n=10) for x, y, a in ((110, 76, -0.6), (290, 78, 0.5), (480, 78, -0.5), (670, 72, 0.6), (200, 72, 2.6), (580, 66, 2.5))])
    art = body(art, lv, LEAF, LEAF_D, LEAF_D, 0.25, 0.3, 5)
    for x, y, r in ((60, 82, 26), (390, 84, 40), (720, 80, 26)):
        art = daisy(art, W, H, x, y, r, rng)
    art = cornflower(art, W, H, 230, 70, 22, rng)
    art = cornflower(art, W, H, 560, 68, 22, rng)
    prev(art, "pg-chain", tone="#f4e3d3")
    save(art, f"{OUT}/chain.webp", max_w=390, quality=82)


for part in PARTS:
    {"cloth": cloth, "basket": basket, "fruit": fruit, "lemonade": lemonade, "sandwich": sandwich, "flowers": flowers, "chain": chain}[part]()
    clear()
