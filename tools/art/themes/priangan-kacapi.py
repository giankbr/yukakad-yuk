"""Priangan Kacapi — adat Sunda Priangan: woven bamboo bilik wall (tileable twill), a kacapi parahu zither with its
row of bridges, a bamboo suling, golden rice sprigs, and a gouache view of Priangan rice terraces with a saung.
Run: python3 -I priangan-kacapi.py [part ...]  parts: bilik kacapi suling padi sawah
Assets -> public/themes/art/priangan-kacapi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g2_lib import *

OUT = outdir("priangan-kacapi")
PARTS = sys.argv[1:] or ["bilik", "kacapi", "suling", "padi", "sawah"]
INK = "#3a2416"
BAMBOO, BAMBOO_D, BAMBOO_L = "#d6b26e", "#a9803f", "#ecd49a"
WOOD, WOOD_D, WOOD_L = "#8a4f2a", "#552d17", "#b2723f"
RICE, RICE_D, RICE_L = "#8fa53e", "#5d7429", "#b9c766"
GOLDEN, GOLDEN_D = "#d9a944", "#a87a26"

if "bilik" in PARTS:
    # anyaman bilik: flat bamboo strips woven 2-over-2 on the diagonal. Tileable 384 px.
    P, d = 384, 24
    yy, xx = np.mgrid[0:P, 0:P].astype(np.float32)
    u, v = xx + yy, xx - yy
    i, j = np.floor(u / d).astype(int), np.floor(v / d).astype(int)
    fu, fv = (u / d) % 1.0, (v / d) % 1.0
    over_u = ((i - j) % 4) < 2           # strip running along v-direction (index i) is on top
    rng = np.random.default_rng(31)
    N = P // d
    tones_i = rng.uniform(-1, 1, N)
    tones_j = rng.uniform(-1, 1, N)
    ti = tones_i[i % N]; tj = tones_j[j % N]
    # strip coordinates across (for edge shading) and along (for fibres)
    across = np.where(over_u, fu, fv)
    tone = np.where(over_u, ti, tj)
    # fibres: streak noise along the strip direction; build two wrap fields along the two diagonals
    def diag_fibres(seed, sgn):
        base = lin_field(P, P, seed, (1, 0), 22, 0.5)
        # rotate by shearing indices (wrap-safe for 45 degrees)
        out = np.zeros_like(base)
        for y in range(P):
            out[y] = np.roll(base[y], sgn * y)
        return out
    fib_u = diag_fibres(41, 1)
    fib_v = diag_fibres(43, -1)
    fib = np.where(over_u, fib_v, fib_u)
    base = rgb_of(BAMBOO) * (1 + tone[..., None] * 0.07)
    skin = np.where((tone > 0.7)[..., None], base * 0.5 + rgb_of(BAMBOO_L) * 0.5, base)   # some strips show the glossy outer skin
    rgb = skin * (1 + fib[..., None] * 0.03)
    # rounded strip: darker at both long edges, plus the strip dives under its neighbour at the end of each float
    edge = np.clip(1 - np.sin(across * math.pi) * 1.25, 0, 1) ** 1.6
    rgb = rgb * (1 - edge[..., None] * 0.32)
    along = np.where(over_u, fv, fu)
    # position along a 2-cell float: shade near the end where it goes under
    cellpos = np.where(over_u, ((i - j) % 4 + 0) , 0)
    fl = np.where(over_u, (((i - j) % 2) + fv) / 2.0, ((((j - i) % 4) - 2) % 2 + fu) / 2.0)
    dive = np.clip((np.abs(fl - 0.5) * 2 - 0.72) * 3.2, 0, 1)
    rgb = rgb * (1 - dive[..., None] * 0.28)
    # gaps between strips show the dark wall behind
    gapl = np.clip((np.abs(across - 0.5) * 2 - 0.9) * 10, 0, 1)
    rgb = rgb * (1 - gapl[..., None] * 0.55)
    # big soft mottling (age, smoke)
    mot = wrapn(P, P, 51, 40)
    rgb = rgb * (0.93 + 0.1 * mot[..., None])
    img = opaque(rgb)
    to_image(img).convert("RGB").save(f"{PREV}/bilik-tile.png")
    big = np.tile(img, (2, 2, 1))
    to_image(big).convert("RGB").save(f"{PREV}/bilik-2x2.png")
    save_rgb(img, f"{OUT}/bilik.webp", quality=72)
    clear()

if "kacapi" in PARTS:
    # kacapi parahu seen from above at a slight angle, lying horizontally; scroll ends curl up.
    W, H = 900, 300
    nx = Seq(30100); rng = random.Random(7)
    x0, x1, cy = 70, 830, 150
    top = []; bot = []
    for k in range(41):
        t = k / 40
        x = x0 + (x1 - x0) * t
        bulge = math.sin(math.pi * t) ** 0.55
        top.append((x, cy - 62 * bulge - 8))
        bot.append((x, cy + 58 * bulge + 4))
    hull = shapes(W, H, [top + bot[::-1]])
    side = shapes(W, H, [[(x, y + 30 * math.sin(math.pi * (x - x0) / (x1 - x0)) ** 0.5 + 6) for x, y in bot] + bot[::-1]])
    side = np.clip(side + gaussian_filter(hull, 2) * 0, 0, 1)
    # soundboard inset
    board = shapes(W, H, [[(x, y + 14) for x, y in top[3:-3]] + [(x, y - 12) for x, y in bot[3:-3]][::-1]])
    # curled ends (gelung) at both tips
    curlL = strokes(W, H, [(spiral_pts(x0 + 6, cy - 22, 4, 30, math.pi * 0.2, 1.1, 30, -1), 16, (0.0, 0.5))])
    curlR = strokes(W, H, [(spiral_pts(x1 - 6, cy - 22, 4, 30, math.pi * 0.8, 1.1, 30, 1), 16, (0.0, 0.5))])
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(450, 232, 380, 26, 24)])
    art = G(art, shadow, "#4a3020", seed=nx(), density=0.28, edge=0.05, bloom=0, rough=3, feather=6)
    art = GP(art, side, WOOD_D, "#4a2614", seed=nx(), rough=1.2, streak=0.8)
    art = wood(art, side, WOOD_D, WOOD_D, "#2e170b", seed=nx(), along=0.0, amt=0.4)
    art = GP(art, hull, WOOD, "#7a4524", seed=nx(), rough=2.6, streak=1.6)
    art = wood(art, hull, WOOD, WOOD, WOOD_D, seed=nx(), along=0.02, amt=0.5)
    art = GP(art, board, "#c08a52", "#a96f3c", seed=nx(), rough=2.0, streak=1.6)
    art = G(art, board * (fbm(W, H, 77, 90, 3) > 0.5), "#8a5a30", seed=nx(), density=0.18, edge=0.2, bloom=0.3, rough=6, feather=4)
    art = wood(art, board, "#c08a52", "#c08a52", "#8a5a30", seed=nx(), along=0.0, amt=0.45)
    art = tint(art, side_light(board, 0, -10, 6), "#7a4a28", 0.5, seed=nx())
    art = tint(art, side_light(hull, 6, 8, 6), WOOD_L, 0.45, seed=nx())
    # sound hole (rosette) on the board
    art = GP(art, ellipses(W, H, [(560, cy - 2, 18, 12, 0)]), "#3a1f10", seed=nx(), rough=0.6, pad=8)
    art = GP(art, curlL, WOOD, WOOD_D, seed=nx(), rough=0.8)
    art = GP(art, curlR, WOOD, WOOD_D, seed=nx(), rough=0.8)
    art = crayon(art, inner_edge(np.clip(hull + side, 0, 1), 2.4), "#3a1f10", seed=nx(), amt=0.75, tooth=0.35)
    rimhi = strokes(W, H, [([(x, y + 4) for x, y in top[4:-4]], 3.2, (0.2, 0.3))])
    art = crayon(art, rimhi, "#e2b27a", seed=nx(), amt=0.6, tooth=0.5)
    # 18 strings across the board, slightly converging
    sl = []
    xs0, xs1 = 140, 760
    for k in range(18):
        t = k / 17
        yl = cy - 34 + 68 * t; yr = cy - 40 + 80 * t
        sl.append(([(xs0, yl), (xs1, yr)], 1.3, None))
    sm = strokes(W, H, sl) * np.clip(hull + 0.0, 0, 1)
    art = OV(art, np.roll(sm, 2, 0), lambda m: col_arr(m, "#4a2a14", m * 0.45), pad=4)
    art = OV(art, sm, lambda m: col_arr(m, "#f4ead2", m * 0.92), pad=4)
    # bridges (inang): little dark triangles on a diagonal, one per string
    br = []
    for k in range(18):
        t = k / 17
        bx = 300 + 300 * t + rng.uniform(-6, 6)
        by = (cy - 34 + 68 * t) + ((cy - 40 + 80 * t) - (cy - 34 + 68 * t)) * (bx - xs0) / (xs1 - xs0)
        br.append([(bx - 7, by + 4), (bx + 7, by + 4), (bx, by - 6)])
    bm = shapes(W, H, br, smooth=False)
    art = GP(art, bm, "#2b160a", "#3d2010", seed=nx(), rough=0.4, pad=6)
    art = OV(art, shapes(W, H, [[(x - 3, y) for x, y in b[:2]] + [b[2]] for b in br], smooth=False), lambda m: col_arr(m, "#d8a86a", m * 0.35), pad=4)
    # tuning pegs along the right end
    pegs = []
    for k in range(18):
        t = k / 17
        px = 770 + 14 * math.sin(t * math.pi)
        py = cy - 44 + 88 * t
        pegs.append((px + 8, py, 5.2, 3.6, 0))
    art = GP(art, ellipses(W, H, pegs), "#e9d3a4", "#d6b77e", seed=nx(), rough=0.4, pad=6)
    art = OV(art, ellipses(W, H, [(x + 9, y + 1.5, 2.5, 1.6, 0) for x, y, *_ in pegs]), lambda m: col_arr(m, "#7a5a30", m * 0.6), pad=4)
    # string ends on the left: small brass pins
    art = GP(art, circles(W, H, [(xs0 - 4, cy - 34 + 68 * k / 17, 2.6) for k in range(18)]), "#d9b566", seed=nx(), rough=0.3, pad=6)
    preview(art, "kacapi")
    save(art, f"{OUT}/kacapi.webp", max_w=760, quality=82)
    clear()

if "suling" in PARTS:
    W, H = 720, 90
    nx = Seq(30200); rng = random.Random(9)
    x0, x1, cy, r = 30, 690, 44, 15
    tube = np.maximum(shapes(W, H, [[(x0, cy - r), (x1, cy - r + 1.5), (x1, cy + r - 1.5), (x0, cy + r)]], smooth=False), ellipses(W, H, [(x0, cy, 3, r, 0), (x1, cy, 3, r - 1.5, 0)]))
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(360, cy + 26, 330, 7, 20)]), "#4a3020", seed=nx(), density=0.22, edge=0.05, bloom=0, rough=3, feather=4)
    art = GP(art, tube, BAMBOO, "#c99f58", seed=nx(), rough=1.2, streak=1.6)
    art = tint(art, side_light(tube, 0, 9, 4), BAMBOO_D, 0.75, seed=nx())
    art = tint(art, side_light(tube, 0, -8, 3), "#f4e2b0", 0.55, seed=nx())
    art = crayon(art, strokes(W, H, [([(x0 + 10, cy - 7), (x1 - 10, cy - 7)], 2.2, (0.1, 0.1))]), "#fbf0cf", seed=nx(), amt=0.5, tooth=0.5)
    # nodes (ruas)
    for nxp in (210, 520):
        nm = strokes(W, H, [([(nxp, cy - r + 1), (nxp + 1, cy + r - 1)], 4.2, None)])
        art = GP(art, nm, "#9c7338", seed=nx(), rough=0.6, pad=6)
        art = crayon(art, strokes(W, H, [([(nxp + 3, cy - r + 2), (nxp + 4, cy + r - 2)], 1.4, None)]), "#efd9a0", seed=nx(), amt=0.6)
    # rattan wrap (sumber) near the mouth end + two thin bands
    wrap = shapes(W, H, [[(x0 + 18, cy - r - 1.5), (x0 + 46, cy - r - 1.5), (x0 + 46, cy + r + 1.5), (x0 + 18, cy + r + 1.5)]], smooth=False)
    art = GP(art, wrap, "#8a3d22", "#6e2c18", seed=nx(), rough=0.6, pad=6)
    art = crayon(art, strokes(W, H, [([(x0 + 18 + k * 3.5, cy - r), (x0 + 22 + k * 3.5, cy + r)], 1.0, None) for k in range(8)]) * wrap, "#c46a3e", seed=nx(), amt=0.6)
    for bx in (x0 + 58, x1 - 30):
        art = GP(art, strokes(W, H, [([(bx, cy - r - 1), (bx, cy + r + 1)], 3.2, None)]), "#6e2c18", seed=nx(), rough=0.4, pad=6)
    # finger holes (6 on top in two groups of 3... suling sunda has 4 or 6)
    holes = [(x, cy - 1, 4.6, 3.6, 0) for x in (380, 412, 444, 494, 526, 558)]
    art = GP(art, ellipses(W, H, holes), "#3a2412", seed=nx(), rough=0.4, pad=6)
    art = OV(art, ellipses(W, H, [(x, y + 2, a * 0.7, b * 0.5, 0) for x, y, a, b, _ in holes]), lambda m: col_arr(m, "#7a5428", m * 0.5), pad=4)
    art = GP(art, ellipses(W, H, [(x0 + 70, cy - 2, 5, 3, 0)]), "#3a2412", seed=nx(), rough=0.4, pad=6)
    art = crayon(art, inner_edge(tube, 1.8), "#6e4f24", seed=nx(), amt=0.65, tooth=0.35)
    preview(art, "suling")
    save(art, f"{OUT}/suling.webp", max_w=400, quality=82)
    clear()

if "padi" in PARTS:
    # a bowed sheaf of ripe rice: three stalks with drooping panicles, two long leaves
    W, H = 360, 420
    nx = Seq(30300); rng = random.Random(13)
    art = blank(W, H)
    leaves = [curve([(150, 410), (130, 300), (70, 190), (30, 150)], 40), curve([(160, 410), (190, 290), (270, 210), (330, 200)], 40)]
    lm = strokes(W, H, [(pt, 13, (0.05, 0.8)) for pt in leaves])
    art = GP(art, lm, "#9aa548", "#7c8a33", seed=nx(), rough=1.4, streak=1.4)
    art = tint(art, side_light(lm, 2, 4, 3), "#5d6a26", 0.5, seed=nx())
    stalks = []
    for k, (tip, sag) in enumerate([((90, 70), 0.0), ((185, 40), 0.1), ((250, 110), 0.2)]):
        st = curve([(152 + k * 4, 410), (150 + (tip[0] - 150) * 0.3, 250), (tip[0] + 20, tip[1] + 30), tip], 50)
        stalks.append(st)
    art = GP(art, strokes(W, H, [(st, 4.2, (0.0, 0.3)) for st in stalks]), "#b49a45", "#8f7a33", seed=nx(), rough=0.6)
    grains = []
    spines = []
    for k, st in enumerate(stalks):
        tip = st[-1]
        dirx = -1 if tip[0] < 150 else 1
        # the heavy panicle bows over: an arc from the stalk top, outward then down
        sp = curve([tip, (tip[0] + dirx * 26, tip[1] - 6), (tip[0] + dirx * 44, tip[1] + 40), (tip[0] + dirx * 40, tip[1] + 110)], 30)
        spines.append((sp, 2.0, (0.0, 0.4)))
        for j in range(3, 30):
            x, y = sp[j]; a0, b0 = sp[j - 1], sp[min(29, j + 1)]
            ang = math.atan2(b0[1] - a0[1], b0[0] - a0[0])
            for side in (-1, 1):
                if rng.random() < 0.8:
                    ga = ang + side * 0.55 + rng.uniform(-.15, .15)
                    grains.append(petal_pts(x + math.cos(ga) * 3, y + math.sin(ga) * 3, rng.uniform(11, 15), 4.6, ga, n=10))
    art = GP(art, strokes(W, H, spines), "#a8892f", seed=nx(), rough=0.4, pad=6)
    gm = shapes(W, H, grains)
    art = GP(art, gm, GOLDEN, "#e8bd58", seed=nx(), rough=1.0, streak=0.8)
    art = tint(art, side_light(gm, -3, -3, 2), "#f6dc8c", 0.6, seed=nx())
    art = tint(art, side_light(gm, 3, 3, 2), GOLDEN_D, 0.6, seed=nx())
    # tie (tali) around the sheaf
    art = GP(art, strokes(W, H, [([(136, 340), (170, 334)], 7, None)]), "#7a3d1f", seed=nx(), rough=0.5, pad=6)
    preview(art, "padi")
    save(art, f"{OUT}/padi.webp", max_w=240, quality=82)
    clear()

if "sawah" in PARTS:
    W, H = 840, 640
    nx = Seq(30400); rng = random.Random(21)
    art = blank(W, H)
    # far volcano (flat top like Tangkuban Parahu) in blue haze
    far = [(-20, 300)]
    for x in range(-20, W + 21, 12):
        t = x / W
        y = 250 - 120 * math.exp(-((t - 0.36) / 0.22) ** 2) - 30 * math.exp(-((t - 0.82) / 0.12) ** 2) + 6 * math.sin(x / 23)
        y = max(y, 140)  # truncated crater rim
        far.append((x, y))
    far += [(W + 20, 300), (W + 20, 360), (-20, 360)]
    fm = shapes(W, H, [far], smooth=False)
    art = G(art, fm, "#9fb2b8", "#b7c4c2", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=6, feather=3)
    art = G(art, fm * (np.mgrid[0:H, 0:W][0] > 210), "#8aa0a0", seed=nx(), density=0.25, edge=0.1, bloom=0.3, rough=8, feather=8)
    # mid hills with tree clumps
    mid = hills(W, H, 300, 26, 5, 0.7)
    art = G(art, mid, "#6f8f62", "#86a06a", seed=nx(), density=0.7, edge=0.4, bloom=0.35, rough=6, feather=2)
    clumps = []
    for k in range(26):
        x = rng.uniform(0, W); y = 290 + rng.uniform(-10, 30)
        clumps.append(deform(ellipse_pts(x, y, rng.uniform(14, 30), rng.uniform(10, 18), 12), rng, 1, 0.1))
    art = G(art, shapes(W, H, clumps) * (1 - np.clip(fm - mid, 0, 1) * 0), "#4d6e45", seed=nx(), density=0.55, edge=0.5, bloom=0.2, rough=4, feather=2)
    # palms + bamboo clump on the ridge
    for x, h_, ln in ((70, 150, -0.12), (104, 118, 0.1), (770, 140, 0.06)):
        pm = palm(W, H, x, 330, h_, rng, ln)
        pm = np.clip(gaussian_filter(pm, 1.0) * 1.8, 0, 1)
        art = GP(art, pm, "#3f5a35", "#4f6c3e", seed=nx(), rough=1.0, streak=1.0)
    culms = []
    for k in range(14):
        a0 = -math.pi / 2 + (k - 6.5) * 0.11
        L = rng.uniform(110, 160)
        bx = 690 + rng.uniform(-8, 8)
        culms.append(curve([(bx, 332), (bx + math.cos(a0) * L * 0.5, 332 + math.sin(a0) * L * 0.5), (bx + math.cos(a0 * 1.0 + (k - 6.5) * 0.06) * L * 1.1, 332 + math.sin(a0) * L * 0.85 + abs(k - 6.5) * 6)], 20))
    art = GP(art, strokes(W, H, [(c, 2.2, (0.0, 0.5)) for c in culms]), "#56703a", seed=nx(), rough=0.4, pad=6)
    foli = []
    for c in culms:
        for j in range(5, 20, 1):
            x, y = c[j]
            foli.append(deform(ellipse_pts(x + rng.uniform(-10, 10), y + rng.uniform(-4, 10), rng.uniform(10, 20), rng.uniform(5, 9), 10, rng.uniform(-.6, .6)), rng, 1, 0.12))
    fm2 = shapes(W, H, foli)
    art = G(art, fm2, "#4f6c3e", "#6a8a4a", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=3, feather=1.2)
    art = G(art, fm2 * (fbm(W, H, 991, 20, 2) > 0.55), "#3c5631", seed=nx(), density=0.5, edge=0.4, bloom=0.1, rough=2, feather=1)
    # terraces: nested contour curves (a spur on the left, a gully on the right), widening toward the viewer
    def ycurve(k, x):
        b = 322 + k * 22 + k * k * 1.55
        sc = 1 - k * 0.045
        return (b - 34 * sc * math.exp(-((x - 250) / 190) ** 2) + 30 * sc * math.exp(-((x - 640) / 140) ** 2)
                + 5 * math.sin(x / 57 + k * 1.3) + 0.03 * (x - 420))
    xs = list(range(-20, W + 21, 8))
    states = ["young", "young", "golden", "water", "young", "golden", "young", "water", "young", "golden", "young", "young"]
    cols = {"young": (RICE, "#9cae46"), "golden": ("#cfae4a", GOLDEN), "water": ("#a9bcbc", "#c4d0c6")}
    nb = len(states)
    for k in range(nb):
        top_ = [(x, ycurve(k, x)) for x in xs]
        bot_ = [(x, ycurve(k + 1, x)) for x in xs]
        band = shapes(W, H, [top_ + bot_[::-1]], smooth=False)
        st = states[k]
        ca, cb = cols[st]
        if k % 3 == 1:
            ca = mix(ca, "#7f9a38", 0.3)
        art = GP(art, band, ca, cb, seed=nx(), rough=2.2, streak=1.2)
        art = G(art, band * (fbm(W, H, nx(), 80, 3) > 0.55), mix(ca, "#5d7429", 0.4), seed=nx(), density=0.22, edge=0.2, bloom=0.3, rough=6, feather=4)
        if st == "water":
            art = tint(art, band * (fbm(W, H, nx(), 50, 3) > 0.52), "#e9eee6", 0.55, seed=nx())
            dots_ = []
            for row in range(4):
                for x in range(0, W, 9):
                    t = (row + 0.6) / 4.4
                    y = ycurve(k, x) + (ycurve(k + 1, x) - ycurve(k, x)) * t
                    dots_.append(([(x + rng.uniform(-2, 2), y + 1.5), (x + rng.uniform(-1, 1), y - 2 - k * 0.15)], 1.2 + k * 0.06, None))
            art = GP(art, strokes(W, H, dots_) * band, "#7c9a3a", seed=nx(), rough=0.3, pad=4, density=0.8)
        else:
            ticks = []
            sz = 2.2 + k * 0.55
            for _ in range(int(120 + k * 34)):
                x = rng.uniform(-10, W + 10)
                t = rng.uniform(0.3, 1.0)
                y = ycurve(k, x) + (ycurve(k + 1, x) - ycurve(k, x)) * t
                a = -math.pi / 2 + rng.uniform(-0.45, 0.45)
                ticks.append(([(x, y), (x + math.cos(a) * sz, y + math.sin(a) * sz)], 1.0 + k * 0.1, (0.0, 0.7)))
            tm = strokes(W, H, ticks) * band
            dark = RICE_D if st == "young" else GOLDEN_D
            light = RICE_L if st == "young" else "#f0d27a"
            art = GP(art, tm * (fbm(W, H, nx(), 18, 2) > 0.5), dark, seed=nx(), rough=0.3, pad=4, density=0.55)
            art = GP(art, np.roll(tm, -2, 0) * (fbm(W, H, nx(), 18, 2) > 0.6), light, seed=nx(), rough=0.3, pad=4, density=0.55)
        # terrace riser: a darker grassy wall just below the dike, then the dike highlight
        wall_h = 2.5 + k * 0.9
        riser = shapes(W, H, [[(x, y - wall_h) for x, y in bot_] + [(x, y + 1) for x, y in bot_[::-1]]], smooth=False)
        art = GP(art, riser, "#56682c", "#4a5c26", seed=nx(), rough=0.8, pad=6)
        art = crayon(art, strokes(W, H, [([(x, y - wall_h) for x, y in bot_], 1.0 + k * 0.12, None)]), "#c9d37f", seed=nx(), amt=0.5, tooth=0.5)
        clear()
    # aerial haze over the far terraces
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    hz = np.clip((440 - yy) / 120, 0, 1) ** 1.2 * 0.38 * art[..., 3]
    art = over(art, col_arr(hz, "#eef0e4", hz))
    # saung on stilts on the 3rd terrace, right side
    sx, sy = 548, ycurve(4, 548) + 4
    legs = strokes(W, H, [([(sx + dx, sy), (sx + dx, sy - 19)], 3.0, None) for dx in (-22, -7, 9, 22)])
    art = GP(art, legs, "#6e5028", seed=nx(), rough=0.4, pad=6)
    floor_ = shapes(W, H, [[(sx - 27, sy - 20), (sx + 27, sy - 20), (sx + 27, sy - 16), (sx - 27, sy - 16)]], smooth=False)
    art = GP(art, floor_, "#8a6634", seed=nx(), rough=0.4, pad=6)
    wall = shapes(W, H, [[(sx - 23, sy - 20), (sx + 23, sy - 20), (sx + 23, sy - 32), (sx - 23, sy - 32)]], smooth=False)
    art = GP(art, wall, "#d4b072", "#c7a062", seed=nx(), rough=0.5, pad=6)
    art = crayon(art, strokes(W, H, [([(sx - 23 + k * 4.3, sy - 32), (sx - 19 + k * 4.3, sy - 20)], 0.9, None) for k in range(11)]) * wall, "#9a7a40", seed=nx(), amt=0.5)
    roof = shapes(W, H, [[(sx - 42, sy - 29), (sx - 22, sy - 40), (sx - 3, sy - 62), (sx + 3, sy - 62), (sx + 22, sy - 40), (sx + 42, sy - 29), (sx + 29, sy - 33), (sx - 29, sy - 33)]], smooth=False)
    art = GP(art, roof, "#3b2a1c", "#2c1f15", seed=nx(), rough=1.0, streak=1.4)
    art = crayon(art, strokes(W, H, [([(sx - 1 + k * 5, sy - 60), (sx - 36 + k * 9, sy - 32)], 0.8, None) for k in range(12)]) * roof, "#6a4e34", seed=nx(), amt=0.45)
    # ridge horns (cagak gunting) crossing at the roof peak
    art = GP(art, strokes(W, H, [([(sx - 9, sy - 58), (sx + 6, sy - 71)], 2.6, None), ([(sx + 9, sy - 58), (sx - 6, sy - 71)], 2.6, None)]), "#2c1f15", seed=nx(), rough=0.3, pad=6)
    preview(art, "sawah")
    save(art, f"{OUT}/sawah.webp", max_w=780, quality=78)
    clear()
