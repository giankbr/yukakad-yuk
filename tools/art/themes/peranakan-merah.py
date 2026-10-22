"""Peranakan Merah — Chinese-Indonesian (Peranakan) wedding: silk-embroidered burung hong (phoenix) with couched gold,
kasut-manik beaded peony, nyonya majolica tile, kebaya-encim lace edge, red lacquer silk.
Run: python3 -I peranakan-merah.py [part ...]   parts: hong peony tile lace divider silk"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c2_lib import *

OUT = outdir("peranakan-merah")
PARTS = sys.argv[1:] or ["hong", "peony", "tile", "lace", "divider", "silk"]
RED, RED_D, RED_L = "#a8161f", "#5c0910", "#d23a35"
GOLD, GOLD_L, GOLD_D = "#d5a948", "#f1d58c", "#8f6422"
JADE, JADE_D, JADE_L = "#2f8a6c", "#185743", "#7cc7a4"
TEAL = "#2b7f95"
PINK, PINK_D, PINK_L = "#e47d8f", "#b8455e", "#f7c3c8"
CREAM = "#f8ecd6"


def half_ribbons(path, wf):
    """Left and right halves of a feather (rachis = path)."""
    n = len(path); L, R, M = [], [], []
    for i in range(n):
        a = tangent(path, i); t = i / (n - 1); ww = wf(t) / 2
        nx_, ny_ = -math.sin(a), math.cos(a)
        L.append((path[i][0] + nx_ * ww, path[i][1] + ny_ * ww)); R.append((path[i][0] - nx_ * ww, path[i][1] - ny_ * ww)); M.append(path[i])
    return L, R, M


def feather(art, W, H, path, wf, ca, cb, nx, seg=6, slant=0.65, spacing=2.6, outline=True, rachis=GOLD_L):
    L, R, M = half_ribbons(path, wf)
    n = len(path)
    for side, P, sg in ((0, L, 1), (1, R, -1)):
        for s0 in range(0, n - 1, seg):
            s1 = min(n - 1, s0 + seg + 1)
            polyg = M[s0:s1 + 1] + P[s0:s1 + 1][::-1]
            m = shapes(W, H, [polyg], smooth=False)
            a = tangent(path, (s0 + s1) // 2)
            t = s0 / (n - 1)
            art = SAT(art, m, mix(ca, cb, t), mix(ca, cb, min(1, t + .2)), angle=a + sg * slant, spacing=spacing, seed=nx(), stitch=12, sheen=0.6)
    if outline:
        art = OV(art, np.ones((1, 1), np.float32) * 0, lambda m: m) if False else art
        oc = couch(W, H, [(L, 2.2), (R, 2.2)], GOLD, seed=nx(), width=2.2)
        art = over(art, oc)
    art = over(art, couch(W, H, [(M, 1.8)], rachis, seed=nx(), width=1.8))
    return art


if "hong" in PARTS:
    W, H = 920, 720
    nx = Seq(30100)
    rnd = random.Random(5)
    art = blank(W, H)
    # ---- tail plumes (behind): long S-curves from the rump, ending in curls with eye spots
    rump = (470, 372)
    tails = [
        ([rump, (560, 420), (660, 430), (760, 380), (820, 300), (800, 240), (760, 250)], JADE_D, JADE_L, 46),
        ([rump, (560, 450), (650, 500), (760, 520), (850, 480), (870, 420), (835, 410)], TEAL, "#9fd6dc", 40),
        ([rump, (540, 470), (590, 560), (680, 620), (780, 640), (830, 600), (805, 580)], RED, PINK_L, 44),
        ([rump, (600, 400), (700, 350), (760, 270), (740, 180), (690, 170), (690, 200)], GOLD_D, GOLD_L, 34),
    ]
    for pts, ca, cb, wd in tails:
        base = curve(pts[:-2], 70)
        # curl the tip inward
        a_end = tangent(base, len(base) - 1)
        ex0, ey0 = base[-1]
        turn = 1 if (pts[-1][0] - pts[-3][0]) * math.sin(a_end) - (pts[-1][1] - pts[-3][1]) * math.cos(a_end) < 0 else -1
        cx_, cy_ = ex0 + math.cos(a_end + turn * math.pi / 2) * 26, ey0 + math.sin(a_end + turn * math.pi / 2) * 26
        a0 = math.atan2(ey0 - cy_, ex0 - cx_)
        sp = [(cx_ + math.cos(a0 + turn * k * 0.21) * 26 * (1 - k * 0.035), cy_ + math.sin(a0 + turn * k * 0.21) * 26 * (1 - k * 0.035)) for k in range(1, 24)]
        path = base + sp
        wf = lambda t, wd=wd: wd * (0.3 + 0.7 * math.sin(min(1, t * 1.6) * math.pi * 0.5) ** 0.6) * (1 - 0.88 * max(0, t - 0.55) / 0.45) * (1 + 0.14 * math.sin(t * 52))
        art = feather(art, W, H, path, wf, ca, cb, nx, seg=5, slant=0.7)
        # eye spot near the end
        ex, ey = path[int(len(base) * 0.86)]
        eye = circles(W, H, [(ex, ey, wd * 0.36)])
        art = SAT(art, eye, PINK if ca != RED else GOLD_L, None, radial=(ex, ey), spacing=2.2, seed=nx(), stitch=6)
        art = SAT(art, circles(W, H, [(ex, ey, wd * 0.17)]), RED_D if ca != RED else JADE_D, None, radial=(ex, ey), spacing=2, seed=nx(), stitch=4)
        art = over(art, couch(W, H, [(arc_pts(ex, ey, wd * 0.37, 0, math.tau, 40), 2.0)], GOLD, seed=nx()))
    # ---- far wing (behind body)
    def wing(art, sx, sy, a0, a1, n, Lmin, Lmax, ca, cb):
        for k in range(n):
            t = k / (n - 1)
            a = a0 + (a1 - a0) * t
            L = Lmin + (Lmax - Lmin) * math.sin(t * math.pi * 0.85 + 0.15)
            bend = 0.25
            p = [(sx, sy), (sx + math.cos(a) * L * 0.5 + math.cos(a + 1.57) * L * bend * 0.2, sy + math.sin(a) * L * 0.5 + math.sin(a + 1.57) * L * bend * 0.2), (sx + math.cos(a) * L, sy + math.sin(a) * L)]
            path = curve(p, 30)
            art = feather(art, W, H, path, lambda u, L=L: L * 0.2 * math.sin(min(1, u * 1.1) * math.pi) ** 0.5 + 2, ca, cb, nx, seg=6, slant=0.6, spacing=2.3)
        return art
    art = wing(art, 400, 280, -1.35, -0.35, 7, 150, 230, JADE, "#c9e6c9")
    # ---- body + neck (red/orange satin with gold scale couching)
    neck = curve([(258, 196), (282, 236), (318, 280), (370, 312)], 40)
    neck_poly = ribbon(neck, 34, 70)
    body = deform(ellipse_pts(410, 330, 88, 52, 16, 0.32), rnd, 1, 0.02)
    bm = shapes(W, H, [neck_poly, body])
    art = SAT(art, bm, "#f08a3c", "#c9402c", angle=0.85, spacing=2.6, seed=nx(), stitch=10, sheen=0.55)
    # breast scales (couched gold arcs)
    sc = []
    for r_ in range(5):
        for c_ in range(6 - r_):
            x = 300 + c_ * 26 + r_ * 22; y = 250 + r_ * 22 + c_ * 10
            if bm[int(y), int(x)] > 0.5:
                sc.append((arc_pts(x, y, 11, 0.2, math.pi - 0.2, 10), 1.6))
    art = over(art, couch(W, H, sc, GOLD_L, seed=nx(), width=1.6))
    art = over(art, couch(W, H, [(neck_poly + [neck_poly[0]], 2.0), (body + [body[0]], 2.2)], GOLD, seed=nx()))
    # ---- head: crest, beak, eye, wattle
    hm = circles(W, H, [(252, 186, 27)])
    art = SAT(art, hm, "#f29a46", "#d4572f", radial=(252, 186), spacing=2.2, seed=nx(), stitch=8)
    beak = poly(W, H, [(228, 176), (186, 196), (228, 200)], smooth=False)
    art = SAT(art, beak, GOLD_L, GOLD, angle=3.0, spacing=1.8, seed=nx(), stitch=8)
    wat = poly(W, H, petal_pts(236, 206, 34, 12, 1.9, n=10))
    art = SAT(art, wat, PINK, PINK_D, angle=1.9, spacing=2, seed=nx(), stitch=8)
    for k, (dx, dy, L) in enumerate([(14, -22, 66), (2, -26, 56), (24, -14, 58)]):
        a = -1.1 + k * 0.32
        p = curve([(252 + dx * .4, 186 + dy * .4), (252 + dx + math.cos(a) * L * .5, 186 + dy + math.sin(a) * L * .5), (252 + dx + math.cos(a + .5) * L, 186 + dy + math.sin(a + .5) * L)], 24)
        art = feather(art, W, H, p, lambda u: 12 * math.sin(min(1, u * 1.1) * math.pi) ** .7 + 1.5, JADE_D, JADE_L, nx, seg=5, spacing=2)
        ex, ey = p[-1]
        art = SAT(art, circles(W, H, [(ex, ey, 6)]), GOLD_L, None, radial=(ex, ey), spacing=1.6, seed=nx(), stitch=4)
    art = over(art, couch(W, H, [(arc_pts(252, 186, 27, 0, math.tau, 40), 2.0)], GOLD, seed=nx()))
    art = SAT(art, circles(W, H, [(244, 182, 7)]), "#f8f0dc", None, radial=(244, 182), spacing=1.6, seed=nx(), stitch=4)
    art = SAT(art, circles(W, H, [(243, 182, 3.6)]), "#1a0c0a", None, radial=(243, 182), spacing=1.4, seed=nx(), stitch=3)
    # ---- near wing (over body): coverts as scale rows + long primaries
    art = wing(art, 410, 300, -1.05, 0.05, 6, 120, 200, "#e9b44c", "#fbe7b0")
    cov = []
    for r_ in range(3):
        for c_ in range(5):
            x = 380 + c_ * 22 + r_ * 8; y = 290 - r_ * 16 + c_ * 4
            cov.append(deform(petal_pts(x, y, 30, 13, -0.5 - r_ * 0.12, n=10), rnd, 0, 0))
    for k, pp in enumerate(cov):
        m = poly(W, H, pp)
        art = SAT(art, m, [JADE, TEAL, "#e9b44c"][k % 3], "#f2ead0", angle=-0.5, spacing=2, seed=nx(), stitch=7)
        art = over(art, couch(W, H, [(pp + [pp[0]], 1.4)], GOLD, seed=nx(), width=1.4))
    # french knots scattered (tiny gold beads) along the tail tips
    kn = []
    for _ in range(40):
        kn.append((rnd.uniform(560, 880), rnd.uniform(160, 660), rnd.uniform(1.8, 3)))
    kn = [k for k in kn if art[int(k[1]), int(k[0]), 3] < 0.1]
    art = over(art, couch(W, H, [([(x - .1, y), (x + .1, y)], r * 2) for x, y, r in kn[:22]], GOLD_L, seed=nx()))
    art = drop_shadow(art, blur=3, dy=2, strength=0.35)
    preview(art, "pm-hong", bg=RED)
    save(art, f"{OUT}/hong.webp", max_w=640, quality=84)
    clear()

if "peony" in PARTS:
    # kasut-manik beaded roundel: cream bead ground, pink peony with buds and leaves, red + gold bead borders
    W = H = 520
    nx = Seq(30200); rnd = random.Random(8)
    cx, cy = W / 2, H / 2
    d = blank(W, H)
    def put(d, m, col):
        return over(d, flat(np.clip(m, 0, 1), col))
    d = put(d, circles(W, H, [(cx, cy, 250)]), "#b3121c")
    d = put(d, circles(W, H, [(cx, cy, 238)]), GOLD)
    d = put(d, circles(W, H, [(cx, cy, 226)]), "#f4ecd9")
    # scalloped inner border: little pink/green alternating dots
    for k in range(36):
        a = k / 36 * math.tau
        d = put(d, circles(W, H, [(cx + math.cos(a) * 214, cy + math.sin(a) * 214, 6)]), JADE if k % 2 else PINK_D)
    # leaves (outlined like bead rows)
    inn = blank(W, H)
    for (x, y, L, a) in [(186, 340, 118, 2.4), (344, 346, 112, 0.75), (312, 160, 104, -1.05), (164, 200, 96, -2.5), (392, 240, 92, -0.25)]:
        pts = petal_pts(x, y, L, L * 0.4, a, n=14)
        inn = put(inn, poly(W, H, pts), "#123f31")
        inn = put(inn, poly(W, H, petal_pts(x + math.cos(a) * 8, y + math.sin(a) * 8, L * 0.86, L * 0.3, a, n=14)), JADE)
        inn = put(inn, strokes(W, H, [([(x, y), (x + math.cos(a) * L * 0.85, y + math.sin(a) * L * 0.85)], 6, None)]), JADE_L)
    # peony: outlined scalloped petals in three rings, deep heart, gold stamens
    pc = (cx - 4, cy + 4)
    for ring, (rf, n, col) in enumerate([(1.0, 9, "#f3a5b2"), (0.72, 8, PINK), (0.46, 7, "#c94a66")]):
        for k in range(n):
            a = k / n * math.tau + ring * 0.35
            px, py = pc[0] + math.cos(a) * 70 * rf, pc[1] + math.sin(a) * 64 * rf
            pts = ellipse_pts(px, py, 58 * rf, 44 * rf, 16, a + math.pi / 2)
            pts = [(x + math.cos(i * 2.3) * 5, y + math.sin(i * 1.9) * 5) for i, (x, y) in enumerate(pts)]
            inn = put(inn, poly(W, H, [(pc[0] + (x - pc[0]) * 1.06, pc[1] + (y - pc[1]) * 1.06) for x, y in pts]), "#7d1530")
            inn = put(inn, poly(W, H, pts), col)
            inn = put(inn, poly(W, H, ellipse_pts(px - math.cos(a) * 18 * rf, py - math.sin(a) * 14 * rf, 32 * rf, 22 * rf, 12, a + math.pi / 2)), mix(col, "#7d1530", 0.35))
    inn = put(inn, circles(W, H, [(pc[0], pc[1], 34)]), "#7d1530")
    for k in range(16):
        a = k / 16 * math.tau
        inn = put(inn, circles(W, H, [(pc[0] + math.cos(a) * 24, pc[1] + math.sin(a) * 24, 6)]), GOLD_L)
    inn = put(inn, circles(W, H, [(pc[0], pc[1], 11)]), GOLD)
    # buds
    for (x, y, a) in [(160, 156, -2.3), (372, 384, 0.8)]:
        inn = put(inn, poly(W, H, petal_pts(x, y, 58, 30, a, n=10)), "#7d1530")
        inn = put(inn, poly(W, H, petal_pts(x, y, 50, 24, a, n=10)), PINK)
        inn = put(inn, poly(W, H, petal_pts(x, y, 30, 26, a + math.pi, n=10)), JADE)
    inn[..., 3] *= circles(W, H, [(cx, cy, 206)])
    d = over(d, inn)
    # tiny gold sparkles
    for _ in range(10):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(150, 195)
        d = put(d, circles(W, H, [(cx + math.cos(a) * r, cy + math.sin(a) * r, 4)]), GOLD)
    art = beadwork(d, pitch=7.0, seed=nx(), fabric="#e9dcc0")
    art = drop_shadow(art, blur=4, dy=3, strength=0.35)
    preview(art, "pm-peony", bg=RED_D)
    save(art, f"{OUT}/peony.webp", max_w=380, quality=86)
    clear()

if "tile" in PARTS:
    # nyonya majolica tile: tube-lined relief, glossy glaze; corner quarter-fans join into roundels when repeated
    S = 300
    nx = Seq(30300); rnd = random.Random(11)
    c = S / 2
    art = GP(blank(S, S), np.ones((S, S), np.float32), "#f3ead6", "#e9dcc0", seed=nx(), rough=0.0, streak=0.6, pad=0)
    lines = []
    fills = []
    # corner quarter fans (yellow + green) -> roundels across tiles
    for (qx, qy) in [(0, 0), (S, 0), (0, S), (S, S)]:
        fills.append((circles(S, S, [(qx, qy, 74)]), "#e8b94a"))
        fills.append((circles(S, S, [(qx, qy, 52)]), "#3f8f6e"))
        fills.append((circles(S, S, [(qx, qy, 24)]), "#d9607a"))
        lines += [(arc_pts(qx, qy, r, 0, math.tau, 60), 2.4) for r in (74, 52, 24)]
        for k in range(8):
            a = k / 8 * math.tau
            lines.append(([(qx + math.cos(a) * 26, qy + math.sin(a) * 26), (qx + math.cos(a) * 50, qy + math.sin(a) * 50)], 2.2))
    # diagonal leaves
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        pts = petal_pts(c + math.cos(a) * 34, c + math.sin(a) * 34, 62, 22, a, n=12)
        fills.append((poly(S, S, pts), "#4f9a72"))
        lines.append((pts + [pts[0]], 2.2))
        lines.append(([(c + math.cos(a) * 62, c + math.sin(a) * 62), (c + math.cos(a) * 90, c + math.sin(a) * 90)], 1.6))
    # central peony (top view), four lobed petals + inner ring
    for k in range(8):
        a = k * math.pi / 4
        rr = 50 if k % 2 == 0 else 40
        pts = ellipse_pts(c + math.cos(a) * rr * 0.55, c + math.sin(a) * rr * 0.55, rr * 0.55, rr * 0.42, 14, a)
        fills.append((poly(S, S, pts), "#e98aa0" if k % 2 == 0 else "#f3b9c4"))
        lines.append((pts + [pts[0]], 2.2))
    fills.append((circles(S, S, [(c, c, 20)]), "#c23e5e"))
    fills.append((circles(S, S, [(c, c, 9)]), "#e8b94a"))
    lines += [(arc_pts(c, c, 20, 0, math.tau, 40), 2.2)]
    # cobalt border
    bd = np.clip(1 - shapes(S, S, [[(8, 8), (S - 8, 8), (S - 8, S - 8), (8, S - 8)]], smooth=False), 0, 1)
    for m, col in fills:
        art = GP(art, m, col, mix(col, "#ffffff", 0.18), seed=nx(), rough=1.2, streak=0.4, pad=6)
    art = GP(art, bd, "#2c4f9a", "#3a64b5", seed=nx(), rough=0.6, pad=0)
    tube = strokes(S, S, [(p, w_, None) for p, w_ in lines])
    art = GP(art, tube, "#2a3a6a", "#3a4b80", seed=nx(), rough=0.5, pad=4)
    # relief + glaze: emboss from tube lines, glossy highlight, fine crazing
    rel = gaussian_filter(np.maximum(tube, bd), 1.4)
    gy, gx = np.gradient(rel)
    shade = np.clip(-(gx + gy) * 9, -1, 1)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    gloss = np.exp(-(((xx - S * 0.32) / (S * 0.5)) ** 2 + ((yy - S * 0.26) / (S * 0.32)) ** 2)) * 0.16
    cr = crackle(S, S, nx(), 70, 0.7) * 0.12
    rgb = art[..., :3] * (1 + shade[..., None] * 0.22) * (1 - cr[..., None]) + gloss[..., None]
    art = rgba(rgb, np.ones((S, S), np.float32))
    art = add_grain(art, seed=3, amount=0.03)
    preview(art, "pm-tile")
    save_full(art, f"{OUT}/tile.webp", size=(160, 160), quality=84)
    clear()

if "lace" in PARTS:
    # kebaya-encim lace edge: cream embroidered net with scalloped hem, cut-work flowers (repeat-x)
    W, H = 480, 120
    nx = Seq(30400)
    def draw(cv):
        p = paint_white()
        for k in range(4):
            x = k * 120 + 60
            cv.c.drawCircle(x, 70, 52, p)
        cv.c.drawRect(skia.Rect(-10, 0, W + 10, 62), p)
    body = tile_mask(W, H, draw)
    body[H - 2:] = 0
    # net: fine diagonal grid
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    net = np.maximum(np.abs(np.sin((xx + yy) * math.pi / 6)) < 0.18, np.abs(np.sin((xx - yy) * math.pi / 6)) < 0.18).astype(np.float32)
    # motifs: small flowers in each scallop + leafy vine along the top
    items = []; leaves = []; flowers = []
    for k in range(4):
        x = k * 120 + 60
        for j in range(6):
            a = j / 6 * math.tau
            flowers.append(petal_pts(x, 72, 22, 9, a, n=10))
        items.append((arc_pts(x, 70, 46, 0.05, math.pi - 0.05, 30), 3.0))
        items.append((arc_pts(x, 70, 40, 0.2, math.pi - 0.2, 30), 1.6))
    vine = [(x, 30 + 8 * math.sin(x / W * 4 * math.tau)) for x in range(-8, W + 9, 4)]
    items.append((vine, 2.6))
    for k in range(16):
        x = k * 30 + 15; y = 30 + 8 * math.sin(x / W * 4 * math.tau)
        leaves.append(petal_pts(x, y, 16, 6, -1.2 if k % 2 else 1.2, n=8))
    solid_m = np.maximum(strokes(W, H, items), shapes(W, H, flowers + leaves))
    holes = circles(W, H, [(k * 120 + 60, 72, 5) for k in range(4)])
    m = np.clip(np.maximum(net * 0.75, solid_m) * body - holes, 0, 1)
    edge = np.clip(gaussian_filter(body, 1.2) - gaussian_filter(body, 3.5), 0, 1) * 2.5 * body
    m = np.clip(np.maximum(m, edge), 0, 1)
    art = rgba(np.ones((H, W, 3), np.float32) * C("#fbf3e3") * (0.9 + 0.1 * solid_m)[..., None], m)
    sh = gaussian_filter(solid_m, 0.8) - solid_m
    art[..., :3] *= (1 - np.clip(sh, 0, 1) * 0.3)[..., None]
    preview(art, "pm-lace", bg=RED)
    save_full(art, f"{OUT}/lace.webp", size=(240, 60), quality=86)
    clear()

if "divider" in PARTS:
    # couched-gold divider: double cloud scroll (awan) + three beads
    W, H = 520, 90
    nx = Seq(30500)
    cx, cy = W / 2, 46
    items = []
    for sgn in (-1, 1):
        items.append((curve([(cx + sgn * 40, cy), (cx + sgn * 120, cy - 10), (cx + sgn * 200, cy + 6), (cx + sgn * 240, cy)], 50), 3.0))
        items.append((spiral_pts(cx + sgn * 62, cy - 4, 16, 3, math.pi / 2, 1.3, 40, sgn), 2.6))
        items.append((spiral_pts(cx + sgn * 150, cy + 2, 11, 2, -math.pi / 2, 1.2, 30, -sgn), 2.2))
    art = couch(W, H, items, GOLD, seed=nx(), width=3)
    d = blank(W, H)
    for k, (x, r, col) in enumerate([(cx - 20, 7, JADE), (cx, 11, RED), (cx + 20, 7, JADE)]):
        d = over(d, flat(circles(W, H, [(x, cy, r)]), col))
    art = over(art, SAT(blank(W, H), circles(W, H, [(cx, cy, 12)]), PINK, RED, radial=(cx, cy), spacing=1.8, seed=nx(), stitch=5))
    for x in (cx - 22, cx + 22):
        art = SAT(art, circles(W, H, [(x, cy, 7)]), JADE, JADE_L, radial=(x, cy), spacing=1.6, seed=nx(), stitch=4)
    preview(art, "pm-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)

if "silk" in PARTS:
    S = 256
    art = silk(S, S, "#a3141d", "#8c0f18", seed=4, pitch=2.0, drape=0.5, bands=1)
    # faint woven damask: tiny cloud lattice (self-coloured)
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2)
        for (x, y) in [(64, 64), (192, 192)]:
            for r in (18, 30):
                cv.c.drawCircle(x, y, r, p)
    dm = tile_mask(S, S, draw)
    art[..., :3] *= (1 + dm * 0.07)[..., None]
    save_full(art, f"{OUT}/silk.webp", quality=72)
