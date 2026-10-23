"""Pesta Teh — afternoon-tea birthday in watercolour: blue-and-white porcelain teapot and cup with gold rims, a
three-tier cake stand with macarons, scones and petit fours, blush garden roses, a paper lace doily and lace edge.
Run: python3 -I pesta-teh.py [part ...]  parts: teapot cup stand roses doily lace macaron sprig
Assets -> public/themes/art/pesta-teh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l5_lib import *
import _j2_lib as j2
import _p1_lib
_p1_lib.PREV = PREV

OUT = outdir("pesta-teh")
PARTS = sys.argv[1:] or ["teapot", "cup", "stand", "roses", "doily", "lace", "macaron", "sprig"]
COBALT, COBALT_D = "#2f569b", "#1d3a70"
SHADE = "#a9b7cc"
GOLD = "#c4a15a"
ROSE_L, ROSE_M, ROSE_D = "#f6d3d3", "#e29aa3", "#b85f70"
LEAF_A, LEAF_B = "#9db28f", "#5f7a5a"


def porcelain(art, W, H, m, rng, nx, light_dir=(-1, -1)):
    """white glazed porcelain: pale wash + cool shadow on the far side + a bright highlight left."""
    art = G(art, m, "#f3f5f8", "#e7ecf3", seed=nx(), density=0.35, edge=0.45, bloom=0.3, rough=2)
    b = bbox(m, 0)
    y0, y1, x0, x1 = b
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - x0) / max(1, x1 - x0); v = (yy - y0) / max(1, y1 - y0)
    sh = np.clip((u - 0.45) * 1.6 + (v - 0.5) * 0.8, 0, 1) * m
    art = G(art, sh, SHADE, "#8ea0bb", seed=nx(), density=0.55, edge=0.2, bloom=0.4, rough=3)
    return art


def ink_flowers(art, W, H, m, rng, nx, n=6, r=(9, 16), col=COBALT):
    """loose cobalt brush flowers and leaves painted on porcelain (inside mask m)."""
    ys, xs = np.nonzero(m > 0.8)
    if len(xs) == 0:
        return art
    petals, leaves, dots = [], [], []
    for _ in range(n):
        j = rng.randrange(len(xs)); x, y = float(xs[j]), float(ys[j])
        rr = rng.uniform(*r)
        for k in range(5):
            a = k / 5 * math.tau + rng.uniform(-.2, .2)
            petals.append(petal_pts(x, y, rr, rr * 0.55, a, n=10))
        dots.append((x, y, rr * 0.22))
        for k in range(rng.randint(2, 3)):
            a = rng.uniform(0, math.tau)
            leaves.append((curve([(x + math.cos(a) * rr, y + math.sin(a) * rr), (x + math.cos(a + .3) * rr * 1.9, y + math.sin(a + .3) * rr * 1.9), (x + math.cos(a + .1) * rr * 2.5, y + math.sin(a + .1) * rr * 2.5)], 10), rr * 0.32, (0.1, 0.6)))
    pm = shapes(W, H, petals) * m
    art = G(art, pm, col, mix(col, "#6c8fcc", .4), seed=nx(), density=0.75, edge=0.7, bloom=0.3, rough=1.4, feather=0.8)
    art = G(art, strokes(W, H, leaves) * m, col, seed=nx(), density=0.7, edge=0.5, bloom=0.2, rough=1, feather=0.7)
    art = G(art, circles(W, H, dots) * m, COBALT_D, seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.6)
    return art


def gold_line(art, W, H, pts, width, nx):
    return FO(art, strokes(W, H, [(pts, width, None)]), GOLD, seed=nx(), emboss=0.4, sparkle=0.25)


def outline(m, px=2.0):
    return np.clip((gaussian_filter(m, px) > 0.05).astype(np.float32) - (gaussian_filter(m, px) > 0.95).astype(np.float32), 0, 1)


if "teapot" in PARTS:
    W, H = 640, 520
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    cx, cy = 300, 320
    body = shapes(W, H, [[(cx - 160, cy - 20), (cx - 140, cy - 110), (cx - 60, cy - 150), (cx + 60, cy - 150), (cx + 140, cy - 110), (cx + 160, cy - 20), (cx + 130, cy + 90), (cx + 60, cy + 130), (cx - 60, cy + 130), (cx - 130, cy + 90)]])
    foot = shapes(W, H, [[(cx - 70, cy + 120), (cx + 70, cy + 120), (cx + 86, cy + 150), (cx - 86, cy + 150)]], smooth=False)
    spout = shapes(W, H, [ribbon(curve([(cx - 130, cy + 30), (cx - 200, cy - 10), (cx - 230, cy - 80), (cx - 262, cy - 120)], 30), 36, 13)])
    handle = strokes(W, H, [(curve([(cx + 140, cy - 90), (cx + 230, cy - 110), (cx + 250, cy - 20), (cx + 200, cy + 60), (cx + 130, cy + 60)], 40), 22, None)])
    lid = shapes(W, H, [[(cx - 96, cy - 145), (cx - 70, cy - 196), (cx, cy - 214), (cx + 70, cy - 196), (cx + 96, cy - 145)]])
    knob = shapes(W, H, [deform(ellipse_pts(cx, cy - 226, 22, 18, 12), rng, 1, 0.05)])
    whole = np.clip(body + foot + spout + handle + lid + knob, 0, 1)
    # cast shadow on the table
    art = G(art, shapes(W, H, [deform(ellipse_pts(cx + 30, cy + 152, 210, 18, 16), rng, 1, 0.05)]), "#8d8a9a", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=5)
    for part in (handle, spout, foot, body, lid, knob):
        art = porcelain(art, W, H, part, rng, nx)
        clear()
    # contour in pale blue-grey (wet edge already gives most of it)
    art = G(art, outline(whole, 1.3) * 0.8, "#7d8fae", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    # cobalt band + flowers
    band = shapes(W, H, [deform([(cx - 156, cy - 54), (cx, cy - 50), (cx + 156, cy - 54), (cx + 158, cy - 30), (cx, cy - 26), (cx - 158, cy - 30)], rng, 2, 0.015)]) * body
    art = G(art, band, COBALT, seed=nx(), density=0.7, edge=0.6, bloom=0.2, rough=1.4)
    scal = circles(W, H, [(x, cy - 28, 7) for x in range(cx - 150, cx + 151, 16)]) * body
    art = G(art, scal, COBALT, seed=nx(), density=0.55, edge=0.5, bloom=0.1, rough=1)
    lower = body * (np.mgrid[0:H, 0:W][0] > cy - 10)
    art = ink_flowers(art, W, H, lower, rng, nx, n=9, r=(13, 20))
    art = ink_flowers(art, W, H, lid * 1.0, rng, nx, n=2, r=(9, 12))
    art = ink_flowers(art, W, H, spout * 1.0, rng, nx, n=1, r=(7, 9))
    # gold rims
    art = gold_line(art, W, H, curve([(cx - 96, cy - 146), (cx, cy - 140), (cx + 96, cy - 146)], 20), 4, nx)
    art = gold_line(art, W, H, curve([(cx - 84, cy + 148), (cx, cy + 152), (cx + 84, cy + 148)], 20), 3.5, nx)
    art = FO(art, knob * 0.95, GOLD, seed=nx(), emboss=0.7, sparkle=0.3)
    art = gold_line(art, W, H, curve([(cx - 252, cy - 118), (cx - 268, cy - 124)], 6), 4, nx)
    # highlight
    hi = strokes(W, H, [(curve([(cx - 118, cy - 80), (cx - 128, cy - 20), (cx - 110, cy + 40)], 20), 10, (0.3, 0.4))])
    art = OV(art, gaussian_filter(hi, 2) * 0.8, lambda mm: solid_layer(mm, "#ffffff"))
    clear()
    preview(art, "teh-teapot", tone="#faf5ec")
    save(art, f"{OUT}/teapot.webp", max_w=420)

if "cup" in PARTS:
    W, H = 460, 300
    rng = random.Random(21); nx = Seq(2100)
    art = blank(W, H)
    cx, cy = 220, 160
    saucer = shapes(W, H, [deform(ellipse_pts(cx, cy + 90, 200, 40, 20), rng, 1, 0.01)])
    cup = shapes(W, H, [[(cx - 120, cy - 60), (cx + 120, cy - 60), (cx + 104, cy + 30), (cx + 50, cy + 84), (cx - 50, cy + 84), (cx - 104, cy + 30)]])
    handle = strokes(W, H, [(curve([(cx + 108, cy - 30), (cx + 170, cy - 30), (cx + 172, cy + 20), (cx + 96, cy + 30)], 30), 16, None)])
    tea = shapes(W, H, [ellipse_pts(cx, cy - 58, 112, 18, 20)])
    art = G(art, shapes(W, H, [ellipse_pts(cx + 20, cy + 112, 190, 16, 16)]), "#8d8a9a", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=3, feather=5)
    art = porcelain(art, W, H, saucer, rng, nx)
    art = gold_line(art, W, H, arc_pts(cx, cy + 90, 196, math.pi * 0.05, math.pi * 0.95, 40, 0.2), 3, nx)
    art = porcelain(art, W, H, handle, rng, nx)
    art = porcelain(art, W, H, cup, rng, nx)
    art = G(art, outline(np.clip(cup + saucer + handle, 0, 1), 1.2) * 0.7, "#7d8fae", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    art = ink_flowers(art, W, H, cup * (np.mgrid[0:H, 0:W][0] > cy - 30), rng, nx, n=3, r=(12, 16))
    art = G(art, tea, "#b06a3a", "#7d4320", seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=1.5)
    art = gold_line(art, W, H, arc_pts(cx, cy - 58, 118, 0, math.pi, 40, 0.17), 3.5, nx)
    art = gold_line(art, W, H, arc_pts(cx, cy - 58, 118, math.pi, math.tau, 40, 0.17), 3.5, nx)
    preview(art, "teh-cup", tone="#faf5ec")
    save(art, f"{OUT}/cup.webp", max_w=280)

if "stand" in PARTS:
    W, H = 520, 760
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    cx = 260
    tiers = [(190, 150), (400, 196), (610, 238)]  # (plate y, half width)
    rod = strokes(W, H, [([(cx, 110), (cx, 640)], 9, None)])
    art = FO(art, rod, GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    top = shapes(W, H, [deform(ellipse_pts(cx, 100, 18, 15, 10), rng, 0, 0), [(cx - 10, 96), (cx, 66), (cx + 10, 96)]])
    art = FO(art, top, GOLD, seed=nx(), emboss=0.7, sparkle=0.3)
    mac_cols = [("#f4b9c4", "#e08c9e"), ("#bfe0cf", "#8cc3a8"), ("#d7c9ec", "#ac99d4"), ("#f6e0a1", "#e4bf62")]
    for ti, (py, hw) in enumerate(tiers):
        plate = shapes(W, H, [ellipse_pts(cx, py, hw, hw * 0.16, 28)])
        art = G(art, shapes(W, H, [ellipse_pts(cx + 8, py + hw * 0.16 + 6, hw * 0.9, 8, 16)]), "#8d8a9a", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=2, feather=4)
        art = porcelain(art, W, H, plate, rng, nx)
        art = gold_line(art, W, H, arc_pts(cx, py, hw - 2, 0.05, math.pi - 0.05, 40, 0.16), 3, nx)
        # treats on the plate
        n = [2, 3, 4][ti]
        xs = np.linspace(cx - hw * 0.62, cx + hw * 0.62, n)
        for k, x in enumerate(xs):
            x += rng.uniform(-6, 6)
            y = py - 6
            kind = ["mac", "scone", "cake"][(k + ti) % 3] if ti > 0 else "mac"
            if kind == "mac":
                ca, cb = mac_cols[(k + ti) % 4]
                r = 38 if ti == 2 else 34
                lo = shapes(W, H, [ellipse_pts(x, y - r * 0.35, r, r * 0.42, 16)])
                up = shapes(W, H, [ellipse_pts(x, y - r * 1.05, r, r * 0.48, 16)])
                fill = shapes(W, H, [ellipse_pts(x, y - r * 0.7, r * 0.92, r * 0.18, 16)])
                art = G(art, lo, ca, cb, seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=1.6)
                art = G(art, fill, "#fff6ee", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=1)
                art = G(art, up, ca, cb, seed=nx(), density=0.8, edge=0.6, bloom=0.3, rough=1.6)
                art = G(art, shapes(W, H, [ellipse_pts(x - r * 0.3, y - r * 1.2, r * 0.35, r * 0.12, 10)]), "#ffffff", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
            elif kind == "scone":
                r = 40
                sc = shapes(W, H, [deform(ellipse_pts(x, y - r * 0.6, r, r * 0.7, 12), rng, 2, 0.1)])
                art = G(art, sc, "#e3b878", "#c48a48", seed=nx(), density=0.8, edge=0.7, bloom=0.4, rough=3)
                art = G(art, sc * np.clip((np.mgrid[0:H, 0:W][0] - (y - r * 1.2)) / (r * 1.3), 0, 1), "#a8692e", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=2)
                cream = shapes(W, H, [deform(ellipse_pts(x, y - r * 1.25, r * 0.7, r * 0.3, 10), rng, 2, 0.14)])
                art = G(art, cream, "#fffaf0", "#f3e6cc", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=2)
                art = G(art, circles(W, H, [(x + 3, y - r * 1.45, r * 0.24)]), "#c23a4a", "#8e1f30", seed=nx(), density=0.9, edge=0.6, bloom=0.1, rough=1.2)
            else:
                r = 34
                ck = shapes(W, H, [[(x - r, y - 4), (x + r, y - 4), (x + r, y - r * 1.5), (x - r, y - r * 1.5)]], smooth=False)
                art = G(art, ck, "#f7dfe0", "#eec1c6", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.5)
                art = G(art, shapes(W, H, [[(x - r, y - r * 0.8), (x + r, y - r * 0.8), (x + r, y - r * 0.6), (x - r, y - r * 0.6)]], smooth=False), "#fff3e4", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
                icing = shapes(W, H, [[(x - r - 2, y - r * 1.5)] + [(x - r + i * r / 3, y - r * 1.5 + (8 if i % 2 else 2)) for i in range(7)] + [(x + r + 2, y - r * 1.5), (x + r, y - r * 1.75), (x - r, y - r * 1.75)]])
                art = G(art, icing, "#e597a6", "#c96f84", seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.2)
                art = G(art, circles(W, H, [(x, y - r * 1.9, 7)]), "#c23a4a", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=1)
            clear()
    # base foot
    foot = shapes(W, H, [[(cx - 60, 660), (cx + 60, 660), (cx + 30, 640), (cx - 30, 640)]], smooth=False)
    art = FO(art, foot, GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    preview(art, "teh-stand", tone="#faf5ec")
    save(art, f"{OUT}/stand.webp", max_w=320)

if "roses" in PARTS:
    W, H = 620, 460
    rng = random.Random(41)
    sdv = Seq(4100)
    art = blank(W, H)
    # leaves behind
    for x, y, L, a in [(170, 230, 120, 2.7), (330, 170, 110, -0.8), (470, 260, 120, 0.25), (150, 170, 100, -2.5), (300, 280, 110, 1.6), (470, 220, 100, -0.45), (230, 160, 96, -1.7), (100, 210, 80, 3.0)]:
        lay, _ = j2.leaf(W, H, x, y, L, a, LEAF_A, LEAF_B, sdv, rng)
        art = glaze(art, lay)
        clear()
    for x, y, r in [(260, 220, 96), (420, 250, 74), (150, 180, 62)]:
        lay, base = j2.rose(W, H, x, y, r, ROSE_L, ROSE_M, ROSE_D, sdv, rng)
        art = knockout(art, base, 0.85, 4)
        art = glaze(art, lay)
        clear()
    for x, y, s_, a in [(530, 200, 18, -0.4), (80, 240, 16, 2.8), (330, 120, 15, -1.3)]:
        lay, _ = j2.bud(W, H, x, y, s_, a, ROSE_M, ROSE_D, LEAF_B, sdv, rng)
        art = glaze(art, lay)
    preview(art, "teh-roses", tone="#faf5ec")
    save(art, f"{OUT}/roses.webp", max_w=420)

if "doily" in PARTS:
    # paper lace doily: scalloped edge, rings of pierced holes and petal cut-outs
    W = H = 760
    c = W / 2
    rng = random.Random(51); nx = Seq(5100)
    R = 360
    outer = [(c + math.cos(t) * (R - 14 + 14 * math.cos(t * 36)), c + math.sin(t) * (R - 14 + 14 * math.cos(t * 36))) for t in np.linspace(0, math.tau, 720, endpoint=False)]
    m = shapes(W, H, [outer], smooth=False)
    holes = []
    for ri, (rr, n, hs) in enumerate([(R - 34, 72, 5.5), (R - 58, 48, 9), (R - 88, 36, 6)]):
        for k in range(n):
            a = k / n * math.tau + (0.5 / n * math.tau if ri % 2 else 0)
            holes.append((c + math.cos(a) * rr, c + math.sin(a) * rr, hs))
    hm = circles(W, H, holes)
    petals = []
    for k in range(24):
        a = k / 24 * math.tau
        petals.append(petal_pts(c + math.cos(a) * (R - 150), c + math.sin(a) * (R - 150), 46, 14, a, n=12))
    pm = shapes(W, H, petals)
    ringline = np.clip(ring(W, H, c, c, R - 112, 2.2) + ring(W, H, c, c, R - 196, 2.2), 0, 1)
    paperm = np.clip(m - hm - pm * 0.9, 0, 1)
    pap = paper_tile(W, "#fffdf9", seed=7, fiber=0.8)
    pap[..., 3] = paperm
    emb = np.clip(gaussian_filter(paperm, 1.2) - gaussian_filter(np.roll(paperm, 2, 0), 1.2), -1, 1)
    pap[..., :3] = np.clip(pap[..., :3] - np.clip(-emb, 0, 1)[..., None] * 0.18, 0, 1)
    pap = G(pap, ringline * paperm, "#e6d9c6", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5)
    sh = np.roll(np.roll(gaussian_filter(paperm, 3), 4, 0), 2, 1) * 0.28
    shadow = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#9a8a7c"), np.float32), sh[..., None]], -1)
    art = over(shadow, pap)
    preview(art, "teh-doily", tone="#efe3d2")
    save(art, f"{OUT}/doily.webp", max_w=560, quality=80)

if "lace" in PARTS:
    # lace tablecloth edge (horizontally tileable strip): scallops with eyelet holes
    W, H = 400, 70
    xs = np.arange(W, dtype=np.float32)
    top = 8
    sc = 40.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = 46 + 12 * np.abs(np.sin(xx / sc * math.pi))
    body = (yy < edge).astype(np.float32)
    holes = np.zeros((H, W), np.float32)
    for x in np.arange(sc / 2, W, sc):
        holes = np.maximum(holes, (((xx - x) ** 2 + (yy - 44) ** 2) < 36).astype(np.float32))
        for dx in (-12, 12):
            holes = np.maximum(holes, (((xx - x - dx) ** 2 + (yy - 30) ** 2) < 9).astype(np.float32))
    stripe = ((yy > 14) & (yy < 18)).astype(np.float32)
    m = np.clip(body - holes - stripe * 0.6, 0, 1)
    m = gaussian_filter(m, 0.6)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fffdf8"), np.float32)
    rgb *= (1 - 0.06 * gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), 0.8, mode="wrap"))[..., None]
    sh = np.roll(gaussian_filter(m, 1.6), 2, 0) * 0.25
    out = over(np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#9a8a7c"), np.float32), sh[..., None]], -1), np.concatenate([rgb, m[..., None]], -1))
    to_image(out).save(f"{OUT}/lace.webp", "WEBP", quality=82, method=6)
    print("lace", os.path.getsize(f"{OUT}/lace.webp") // 1024, "KB")

if "macaron" in PARTS:
    W, H = 180, 160
    rng = random.Random(61); nx = Seq(6100)
    art = blank(W, H)
    x, y, r = 90, 100, 66
    lo = shapes(W, H, [ellipse_pts(x, y - r * 0.15, r, r * 0.42, 16)])
    up = shapes(W, H, [ellipse_pts(x, y - r * 0.85, r, r * 0.48, 16)])
    fill = shapes(W, H, [ellipse_pts(x, y - r * 0.5, r * 0.92, r * 0.18, 16)])
    art = G(art, lo, "#f4b9c4", "#e08c9e", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=2)
    art = G(art, fill, "#fff6ee", seed=nx(), density=0.95, edge=0.3, bloom=0, rough=1.2)
    art = G(art, up, "#f4b9c4", "#e08c9e", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=2)
    art = G(art, shapes(W, H, [ellipse_pts(x - r * 0.3, y - r * 1.0, r * 0.35, r * 0.12, 10)]), "#ffffff", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1)
    preview(art, "teh-macaron", tone="#faf5ec")
    save(art, f"{OUT}/macaron.webp", max_w=72)

if "sprig" in PARTS:
    # divider: small rose with two leaves on a hairline stem
    W, H = 520, 120
    rng = random.Random(71); sdv = Seq(7100)
    art = blank(W, H)
    st = strokes(W, H, [(curve([(30, 66), (180, 58), (260, 62), (340, 58), (490, 66)], 40), 2.2, (0.1, 0.1))])
    art = G(art, st, LEAF_B, seed=sdv(), density=0.8, edge=0.3, bloom=0, rough=0.6)
    for x, y, L, a in [(214, 58, 46, 3.4), (306, 58, 46, -0.25), (150, 62, 34, 3.0), (370, 60, 34, 0.1)]:
        lay, _ = j2.leaf(W, H, x, y, L, a, LEAF_A, LEAF_B, sdv, rng, vein=False)
        art = glaze(art, lay)
    lay, base = j2.rose(W, H, 260, 58, 30, ROSE_L, ROSE_M, ROSE_D, sdv, rng)
    art = glaze(knockout(art, base, 0.9, 3), lay)
    preview(art, "teh-sprig", tone="#faf5ec")
    save(art, f"{OUT}/sprig.webp", max_w=300)

kb_total(OUT)
