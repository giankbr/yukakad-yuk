"""Kafe Kopi — cozy coffee shop: wood-framed chalkboard with chalk doodles, a counter with latte, croissant, beans and a
pothos; top-down latte with rosetta; bean-and-leaf divider; single bean; trailing pothos in a hanging pot.
Run: python3 -I kafe-kopi.py [part ...]  parts: board counter cup beans bean pothos"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n6_lib import *

OUT = outdir("kafe-kopi")
PARTS = sys.argv[1:] or ["board", "counter", "cup", "beans", "bean", "pothos"]
SLATE, SLATE_D = "#2c3430", "#1f2522"
WOOD, WOOD_D, WOOD_L = "#9a6a43", "#5e3c22", "#c08d5e"
ESP, ESP_D = "#5a3522", "#2e1a10"
CREMA, MILK = "#d9a877", "#f4e6cf"
CUP, CUP_D = "#f3ece2", "#c9bba8"
TERRA, TERRA_D = "#c4673f", "#8a4227"
LEAFC = ("#7fa060", "#4f7448", "#2f4c32")


def chalk(arr, mask, seed, col="#f1ede4", alpha=0.92):
    """chalk on slate: dry, broken, grainy stroke."""
    h, w = mask.shape
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.6)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    br = fbm(w, h, seed + 3, 9, 2)
    a = mask * (0.35 + 0.65 * g) * (1 - 0.6 * np.clip((br - 0.66) * 4, 0, 1)) * alpha
    return over(arr, tint(np.clip(a, 0, 1), col, 1.0))


def wood(art, mask, nx, horizontal=True, base=WOOD, dark=WOOD_D):
    """gouache wood with grain lines."""
    art = GP(art, mask, base, mix(base, dark, 0.35), seed=nx(), rough=1.0, streak=1.2, pad=10)
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = yy if horizontal else xx
    v = xx if horizontal else yy
    n = fbm(w, h, nx(), 60, 3)
    grain = np.abs(np.sin((u + n * 26 + np.sin(v / 90) * 6) / 3.2)) ** 14
    art = G(art, grain * mask * 0.9, dark, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    return art


def bean_poly(cx, cy, r, ang):
    return deform(ellipse_pts(cx, cy, r, r * 0.68, 14, ang), random.Random(int(cx * 7 + cy)), 1, 0.03)


def paint_bean(art, W, H, cx, cy, r, ang, nx):
    m = shapes(W, H, [bean_poly(cx, cy, r, ang)])
    art = G(art, m, "#7a4a2c", ESP_D, seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.2, feather=0.6, pad=6)
    ca, sa = math.cos(ang), math.sin(ang)
    crease = [(cx + ca * r * t - sa * r * 0.12 * math.sin(t * 3), cy + sa * r * t + ca * r * 0.12 * math.sin(t * 3)) for t in [k / 10 - 0.8 for k in range(17)]]
    art = G(art, stroke_mask(W, H, crease, r * 0.16), "#1c0f08", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.4, pad=4)
    hi = shapes(W, H, [ellipse_pts(cx - sa * r * 0.3 - ca * r * 0.2, cy + ca * r * 0.3 * -1 - sa * r * 0.2, r * 0.35, r * 0.14, 8, ang)])
    return lay(art, gaussian_filter(hi, 1.2) * 0.55, "#c89a72", 0.6)


def leafy(art, W, H, x, y, L, ang, nx, c=LEAFC):
    m = shape_mask(W, H, petal_pts(x, y, L, L * 0.3, ang, n=18))
    art = G(art, m, c[0], c[1], seed=nx(), density=0.75, edge=0.5, bloom=0.3, rough=2, feather=0.8, pad=8)
    vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [j / 10 for j in range(1, 9)]]
    return G(art, stroke_mask(W, H, vein, 1.6), c[2], seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.5, pad=6)


def pothos_leaf(art, W, H, x, y, L, ang, nx):
    """pothos leaf: broad ovate with a pointed tip and a slight heart notch at the stem, marbled."""
    pts = []
    for i in range(28):
        t = i / 28 * math.tau
        u = (1 - math.cos(t)) / 2                  # 0 at stem .. 1 at tip
        wv = math.sin(math.pi * u ** 0.8) ** 0.9 * (1 - 0.15 * u)
        px = u * L - (0.12 * L * math.exp(-u * 18))
        py = math.copysign(wv * L * 0.36, math.sin(t))
        pts.append((px, py))
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    m = shape_mask(W, H, pts)
    art = G(art, m, "#8fb35f", "#4f7d3e", seed=nx(), density=0.8, edge=0.55, bloom=0.4, rough=1.6, feather=0.7, pad=8)
    art = G(art, m * (fbm(W, H, nx(), 7, 2) > 0.64), "#e6e3a8", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6, feather=0.6, pad=6)
    vein = [(x + ca * L * t, y + sa * L * t) for t in [j / 10 for j in range(0, 9)]]
    return G(art, stroke_mask(W, H, vein, 1.4), "#2f5230", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.5, pad=6)


def heart_pts(cx, cy, s, squash=1.0, n=40):
    out = []
    for i in range(n):
        t = i / n * math.tau
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        out.append((cx + x * s / 16, cy - y * s / 16 * squash))
    return out


def latte_top(art, W, H, cx, cy, r, nx, squash=1.0):
    """coffee surface with a rosetta (milk) seen from above (optionally squashed for perspective)."""
    sur = shapes(W, H, [ellipse_pts(cx, cy, r, r * squash, 32)])
    art = G(art, sur, CREMA, "#b97d4e", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1, feather=0.8, pad=8)
    ring = np.clip(sur - shapes(W, H, [ellipse_pts(cx, cy, r * 0.86, r * 0.86 * squash, 32)]), 0, 1)
    art = G(art, ring, ESP, seed=nx(), density=0.55, edge=0.2, bloom=0.1, rough=0.8, feather=1.4, pad=8)
    # latte art: a layered heart with a pulled tail
    milk = shapes(W, H, [heart_pts(cx, cy - r * 0.06 * squash, r * 0.62, squash)])
    art = GP(art, milk * sur, MILK, "#efd8b7", seed=nx(), rough=0.8, streak=0.3, pad=8)
    rings = strokes(W, H, [(heart_pts(cx, cy - r * 0.02 * squash, r * k, squash) + [heart_pts(cx, cy - r * 0.02 * squash, r * k, squash)[0]], r * 0.035, None) for k in (0.42, 0.24)])
    art = G(art, rings * milk, CREMA, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.7, pad=6)
    tail = stroke_mask(W, H, [(cx, cy - r * 0.5 * squash), (cx, cy + r * 0.6 * squash)], r * 0.04)
    art = G(art, tail * sur, CREMA, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.5, feather=0.6, pad=6)
    return art


if "board" in PARTS:
    W, H = 720, 820
    rng = random.Random(81); nx = Seq(8100)
    art = blank(W, H)
    F = 34
    outer = shapes(W, H, [rect(10, 10, W - 10, H - 10)], smooth=False)
    inner = shapes(W, H, [rect(10 + F, 10 + F, W - 10 - F, H - 10 - F)], smooth=False)
    art = G(art, np.roll(np.roll(outer, 10, 0), 6, 1), "#3a2a1f", seed=nx(), density=0.35, edge=0, bloom=0, rough=2, feather=8)
    art = wood(art, np.clip(outer - inner, 0, 1), nx)
    # mitred joins + bevel
    mit = strokes(W, H, [([(10, 10), (10 + F, 10 + F)], 1.6, None), ([(W - 10, 10), (W - 10 - F, 10 + F)], 1.6, None),
                         ([(10, H - 10), (10 + F, H - 10 - F)], 1.6, None), ([(W - 10, H - 10), (W - 10 - F, H - 10 - F)], 1.6, None)])
    art = G(art, mit, WOOD_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = lay(art, edge_hi(outer, -3, -3) * 0.8, "#f0c999", 0.5)
    art = G(art, np.clip(gaussian_filter(inner, 2) - inner * 0.0, 0, 1) * (1 - inner) * np.clip(outer - inner, 0, 1) * 2.5, WOOD_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    # slate
    art = GP(art, inner, SLATE, SLATE_D, seed=nx(), rough=0.4, streak=0.6, pad=4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dust = fbm(W, H, nx(), 110, 4)
    wipes = np.abs(np.sin((xx * 0.35 + yy * 0.9) / 70 + dust * 4)) ** 6 * 0.5 + np.clip(dust - 0.45, 0, 1) * 0.6
    art = lay(art, inner * gaussian_filter(wipes, 6) * 0.1, "#c9cfc8", 1.0)
    edge_dust = inner * np.clip(1 - np.minimum.reduce([xx - 44, W - 44 - xx, yy - 44, H - 44 - yy]) / 60, 0, 1)
    art = lay(art, edge_dust * 0.16, "#dfe3dc", 1.0)
    # chalk doodles: cup with steam (top), flourishes, bean sprig (bottom)
    cx, cy = W / 2, 128
    cup = [(cx - 44, cy - 10), (cx - 38, cy + 34), (cx - 22, cy + 46), (cx + 22, cy + 46), (cx + 38, cy + 34), (cx + 44, cy - 10)]
    items = [(cup, 3.4, None), ([(cx - 46, cy - 10), (cx + 46, cy - 10)], 3.4, None),
             (arc_pts(cx + 52, cy + 10, 15, -math.pi / 2, math.pi / 2, 16), 3.2, None),
             (curve([(cx - 70, cy + 54), (cx, cy + 60), (cx + 70, cy + 54)], 20), 3.2, None)]
    for dx in (-16, 4, 22):
        items.append((curve([(cx + dx, cy - 18), (cx + dx - 8, cy - 34), (cx + dx + 6, cy - 50), (cx + dx - 4, cy - 66)], 20), 2.6, (0.2, 0.5)))
    for sgn in (-1, 1):
        x0 = cx + sgn * 92
        items.append((curve([(x0, cy + 20), (x0 + sgn * 70, cy + 12), (x0 + sgn * 130, cy + 28), (x0 + sgn * 160, cy + 12)], 30), 2.4, (0.1, 0.4)))
        items.append((spiral_pts(x0 + sgn * 166, cy + 4, 10, 2, math.pi / 2, 0.85, 20, sgn), 2.2, (0.0, 0.5)))
    # bottom: sprig of two leaves + beans in chalk
    by = H - 118
    items.append((curve([(cx - 120, by), (cx - 40, by - 10), (cx + 40, by - 10), (cx + 120, by)], 30), 2.4, None))
    for x in (cx - 100, cx - 60, cx + 60, cx + 100):
        d = -1 if x < cx else 1
        tip = (x + d * 14, by - 40)
        items.append((curve([(x, by - 6), (x - 12, by - 24), tip], 14), 2.2, None))
        items.append((curve([(x, by - 6), (x + 12, by - 18), tip], 14), 2.2, None))
    m = strokes(W, H, items)
    beans_m = np.zeros((H, W), np.float32)
    for x, a in ((cx - 18, 0.5), (cx + 16, -0.4)):
        p = bean_poly(x, by - 2, 13, a)
        beans_m = np.maximum(beans_m, strokes(W, H, [(p + [p[0]], 2.6, None), ([(x - math.cos(a) * 9, by - 2 - math.sin(a) * 9), (x + math.cos(a) * 9, by - 2 + math.sin(a) * 9)], 2, None)]))
    # corner dots
    dots = circles(W, H, [(78, 78, 3), (W - 78, 78, 3), (78, H - 78, 3), (W - 78, H - 78, 3)])
    art = chalk(art, np.maximum.reduce([m, beans_m, dots]), 33)
    # a stick of chalk resting on the ledge
    ledge = shapes(W, H, [rect(10, H - 22, W - 10, H - 4)], smooth=False)
    art = wood(art, ledge, nx, base=WOOD_L)
    art = GP(art, shapes(W, H, [rect(W - 190, H - 34, W - 140, H - 22)], smooth=False), "#f4efe6", "#d9d4ca", seed=nx(), rough=0.6, pad=6)
    prev(art, "kk-board", tone="#efe4d3")
    save(art, f"{OUT}/board.webp", max_w=620, quality=76)
    clear()

if "counter" in PARTS:
    W, H = 780, 380
    rng = random.Random(83); nx = Seq(8300)
    art = blank(W, H)
    top = shapes(W, H, [rect(0, 250, W, 300)], smooth=False)
    front = shapes(W, H, [rect(0, 300, W, H)], smooth=False)
    art = wood(art, top, nx, base=WOOD_L)
    art = wood(art, front, nx, horizontal=False, base=WOOD, dark=WOOD_D)
    pl = strokes(W, H, [([(x, 300), (x, H)], 2, None) for x in range(70, W, 110)])
    art = G(art, pl * front, WOOD_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.5)
    art = G(art, shapes(W, H, [rect(0, 300, W, 312)], smooth=False), WOOD_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=2)
    art = lay(art, edge_hi(top, 0, -3) * 0.9, "#f3cf9e", 0.6)
    # pothos pot (right)
    pot = shapes(W, H, [[(640, 262), (720, 262), (708, 180), (652, 180)]], smooth=False)
    art = G(art, shapes(W, H, [ellipse_pts(684, 266, 54, 7, 16)]), "#3a2414", seed=nx(), density=0.45, edge=0, bloom=0, rough=2, feather=3)
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.34 + rng.uniform(-0.1, 0.1)
        L = rng.uniform(40, 80)
        x, y = 680 + math.cos(a) * L * 0.6, 176 + math.sin(a) * L * 0.6
        art = G(art, stroke_mask(W, H, [(680, 182), (x, y)], 2), "#4f7448", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, pad=6)
        art = pothos_leaf(art, W, H, x, y, rng.uniform(24, 32), a + rng.uniform(-0.4, 0.4), nx)
    for k in range(3):   # trailing vine over the pot edge
        vx = 650 + k * 30
        vine = curve([(vx, 186), (vx - 20 + k * 10, 230), (vx - 10, 270), (vx - 26 + k * 8, 300)], 30)
        art = G(art, stroke_mask(W, H, vine, 2), "#4f7448", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, pad=6)
        for j in (10, 20, 29):
            art = pothos_leaf(art, W, H, vine[j][0], vine[j][1], 18, math.pi / 2 + rng.uniform(-0.9, 0.9), nx)
    art = GP(art, pot, TERRA, TERRA_D, seed=nx(), rough=0.8, streak=0.8)
    art = GP(art, shapes(W, H, [rect(648, 176, 712, 192)], smooth=False), mix(TERRA, "#ffffff", 0.1), TERRA, seed=nx(), rough=0.6)
    clear()
    # croissant on a small plate (left)
    art = G(art, shapes(W, H, [ellipse_pts(150, 262, 104, 18, 24)]), "#3a2414", seed=nx(), density=0.4, edge=0, bloom=0, rough=2, feather=3)
    plate = shapes(W, H, [ellipse_pts(150, 252, 100, 20, 30)])
    art = GP(art, plate, "#f6f1e8", "#ddd2c2", seed=nx(), rough=0.5)
    art = G(art, np.clip(plate - shapes(W, H, [ellipse_pts(150, 250, 76, 13, 30)]), 0, 1), "#c9bba8", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    cres = shapes(W, H, [curve([(78, 246), (100, 214), (150, 200), (200, 214), (222, 246), (196, 236), (150, 228), (104, 236), (78, 246)], 40)])
    art = G(art, cres, "#e3a85a", "#b9712f", seed=nx(), density=0.9, edge=0.6, bloom=0.3, rough=1.5, feather=0.8, pad=8)
    segs = [(-50, 14, 0.7), (-28, 22, 0.35), (0, 27, 0.0), (28, 22, -0.35), (50, 14, -0.7)]
    for dx, r, a in segs:
        m = shapes(W, H, [deform(ellipse_pts(150 + dx, 228 + (27 - r) * 0.6, r * 0.62, r, 14, a), rng, 1, 0.04)])
        art = G(art, m, "#e3a85a", "#b9712f", seed=nx(), density=0.9, edge=0.6, bloom=0.3, rough=1.5, feather=0.8, pad=8)
        art = lay(art, gaussian_filter(edge_hi(m, -4, -4), 1.5) * 0.9, "#f9dca0", 0.7)
    art = G(art, strokes(W, H, [([(150 + dx + 8, 214), (150 + dx + 4, 248)], 1.6, None) for dx, r, a in segs]), "#8a4f1c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    clear()
    # latte cup on saucer (centre)
    cx = 400
    art = G(art, shapes(W, H, [ellipse_pts(cx, 268, 118, 18, 24)]), "#3a2414", seed=nx(), density=0.45, edge=0, bloom=0, rough=2, feather=3)
    saucer = shapes(W, H, [ellipse_pts(cx, 256, 112, 24, 30)])
    art = GP(art, saucer, CUP, CUP_D, seed=nx(), rough=0.5)
    art = G(art, edge_lo(saucer, 0, 3) * 1.5, CUP_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    body = shapes(W, H, [[(cx - 78, 150), (cx + 78, 150), (cx + 70, 210), (cx + 50, 246), (cx - 50, 246), (cx - 70, 210)]])
    handle = strokes(W, H, [(arc_pts(cx + 84, 190, 26, -math.pi / 2 - 0.2, math.pi / 2 + 0.3, 20), 11, None)])
    art = GP(art, np.maximum(body, handle), CUP, CUP_D, seed=nx(), rough=0.6, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, body * np.clip((xx - cx) / 80, 0, 1), CUP_D, seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1)
    band = body * ((yy > 196) & (yy < 212)).astype(np.float32)
    art = GP(art, band, TERRA, TERRA_D, seed=nx(), rough=0.4)
    art = latte_top(art, W, H, cx, 150, 76, nx, squash=0.3)
    art = lay(art, np.clip((cx - 40 - xx) / 40, 0, 1) * body * 0.5, "#ffffff", 0.5)
    clear()
    # beans scattered
    for x, y, a in ((262, 266, 0.4), (286, 276, -0.6), (540, 270, 1.1), (566, 262, -0.2), (520, 282, 0.2), (596, 280, 0.7), (40, 276, -0.3)):
        art = paint_bean(art, W, H, x, y, 11, a, nx)
    prev(art, "kk-counter", tone="#efe4d3")
    save(art, f"{OUT}/counter.webp", max_w=720, quality=78)
    clear()

if "cup" in PARTS:
    W, H = 360, 360
    nx = Seq(8500)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(188, 190, 150, 150, 40)]), "#3a2414", seed=nx(), density=0.3, edge=0, bloom=0, rough=2, feather=8)
    sau = shapes(W, H, [ellipse_pts(180, 180, 150, 150, 40)])
    art = GP(art, sau, CUP, CUP_D, seed=nx(), rough=0.6)
    art = G(art, np.clip(sau - shapes(W, H, [ellipse_pts(180, 180, 128, 128, 40)]), 0, 1), CUP_D, seed=nx(), density=0.35, edge=0.2, bloom=0, rough=0.5)
    handle = strokes(W, H, [([(268, 120), (300, 88)], 22, None)])
    cupm = np.maximum(shapes(W, H, [ellipse_pts(180, 180, 100, 100, 40)]), handle)
    art = G(art, np.roll(np.roll(cupm, 6, 0), 6, 1), "#8a7a66", seed=nx(), density=0.4, edge=0, bloom=0, rough=1, feather=4)
    art = GP(art, cupm, "#fbf7f0", CUP, seed=nx(), rough=0.6)
    art = GP(art, np.clip(shapes(W, H, [ellipse_pts(180, 180, 100, 100, 40)]) - shapes(W, H, [ellipse_pts(180, 180, 90, 90, 40)]), 0, 1), TERRA, TERRA_D, seed=nx(), rough=0.4)
    art = latte_top(art, W, H, 180, 186, 84, nx, 1.0)
    spoon = strokes(W, H, [([(64, 284), (120, 226)], 7, (0.0, 0.0))])
    art = GP(art, np.maximum(spoon, shapes(W, H, [ellipse_pts(132, 214, 16, 10, 14, -0.8)])), "#c9c4bb", "#8c877e", seed=nx(), rough=0.4)
    prev(art, "kk-cup", tone="#efe4d3")
    save(art, f"{OUT}/cup.webp", max_w=240, quality=82)
    clear()

if "beans" in PARTS:
    W, H = 520, 110
    rng = random.Random(5); nx = Seq(8700)
    art = blank(W, H)
    stem = curve([(60, 62), (180, 50), (340, 50), (460, 62)], 40)
    art = G(art, stroke_mask(W, H, stem, 3), "#5a4a2a", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
    for x, a in ((120, -2.4), (190, -0.7), (330, -2.4), (400, -0.7)):
        art = leafy(art, W, H, x, 52, 54, a, nx)
    # coffee cherries and beans
    for x, y in ((248, 60), (266, 50), (284, 62)):
        m = circles(W, H, [(x, y, 11)])
        art = G(art, m, "#c2332e", "#7d1c1c", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1, feather=0.6, pad=6)
        art = lay(art, gaussian_filter(circles(W, H, [(x - 4, y - 4, 3)]), 1) , "#ffd9c9", 0.8)
    for x, a in ((40, 0.3), (482, -0.4)):
        art = paint_bean(art, W, H, x, 64, 13, a, nx)
    prev(art, "kk-beans", tone="#efe4d3")
    save(art, f"{OUT}/beans.webp", max_w=320, quality=84)

if "bean" in PARTS:
    W, H = 100, 100
    nx = Seq(8900)
    art = paint_bean(blank(W, H), W, H, 50, 50, 30, -0.6, nx)
    prev(art, "kk-bean", tone="#efe4d3")
    save(art, f"{OUT}/bean.webp", max_w=56, quality=84)

if "pothos" in PARTS:
    W, H = 300, 560
    rng = random.Random(15); nx = Seq(9100)
    art = blank(W, H)
    rope = strokes(W, H, [([(150, 0), (150, 70)], 2.4, None), ([(150, 70), (96, 130)], 2, None), ([(150, 70), (204, 130)], 2, None)])
    art = G(art, rope, "#a88a62", "#6e5636", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5)
    vines = []
    for k, (x0, dx, L) in enumerate(((110, -40, 380), (150, 10, 430), (190, 40, 340), (130, -10, 260), (175, 26, 300))):
        v = curve([(x0, 150), (x0 + dx * 0.4, 150 + L * 0.35), (x0 + dx, 150 + L * 0.7), (x0 + dx * 0.6, 150 + L)], 60)
        vines.append(v)
        art = G(art, stroke_mask(W, H, v, 2.2), "#4f7448", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, pad=6)
    pot = shapes(W, H, [[(92, 128), (208, 128), (196, 196), (104, 196)]], smooth=False)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.42
        art = pothos_leaf(art, W, H, 150 + math.cos(a) * 46, 120 + math.sin(a) * 34, 28, a, nx)
    art = GP(art, pot, TERRA, TERRA_D, seed=nx(), rough=0.8, streak=0.8)
    art = GP(art, shapes(W, H, [rect(88, 124, 212, 140)], smooth=False), mix(TERRA, "#ffffff", 0.12), TERRA, seed=nx(), rough=0.5)
    clear()
    for v in vines:
        for j in range(4, len(v), 7):
            side = 1 if (j // 7) % 2 else -1
            art = pothos_leaf(art, W, H, v[j][0] + side * 4, v[j][1], rng.uniform(19, 26), math.pi / 2 + side * rng.uniform(0.5, 1.2), nx)
        clear()
    prev(art, "kk-pothos", tone="#efe4d3")
    save(art, f"{OUT}/pothos.webp", max_w=200, quality=82)
