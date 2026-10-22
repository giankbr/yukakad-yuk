"""Simalungun Bolon — an original rumah bolon Simalungun (log-crib foundation, board walls, steep ijuk roof whose front
rises into a small hipped crown with a horn finial, gable face painted in red/white/black) on a ridge above the eastern
shore of Lake Toba in misty watercolour; a hiou cloth end with twisted fringe woven at thread level; a painted spiral
band; a gable emblem.  Run: python3 -I simalungun-bolon.py [part ...]   parts: bolon hiou gorga atap"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f1_lib import *
import _jw_lib

OUT = outdir("simalungun-bolon")
PARTS = sys.argv[1:] or ["bolon", "hiou", "gorga", "atap"]
RED, RED_D = "#a3282a", "#6e1818"
BONE, BLACK = "#efe6d2", "#221a18"
WOOD, WOOD_D, WOOD_L = "#5e3e28", "#33221a", "#86603e"
IJUK, IJUK_L = "#2a2724", "#4a443c"
LAKE, LAKE_D = "#7d98a6", "#4f6e7e"


def gable_paint(art, W, H, nx, rng, tri_pts, cx, top, base, hw):
    """Red/white/black painted gable: stacked bands of triangles and a central diamond."""
    tri = shapes(W, H, [tri_pts], smooth=False)
    art = GP(art, tri, RED, RED_D, seed=nx(), rough=0.6, streak=0.6)
    yy, xx = ygrid(W, H)
    hgt = base - top
    rows = 5
    polys_w, polys_b = [], []
    for r in range(rows):
        y0 = top + hgt * (0.25 + 0.15 * r)
        y1 = y0 + hgt * 0.07
        w_at = hw * (y1 - top) / hgt
        n = max(3, int(w_at * 2 / (hgt * 0.09)))
        step = w_at * 2 / n
        for k in range(n):
            x0 = cx - w_at + k * step
            (polys_w if (k + r) % 2 == 0 else polys_b).append([(x0, y1), (x0 + step / 2, y0), (x0 + step, y1)])
    bw = shapes(W, H, polys_w, smooth=False) * tri
    bb = shapes(W, H, polys_b, smooth=False) * tri
    art = GP(art, bw, BONE, "#ddd0b6", seed=nx(), rough=0.4)
    art = GP(art, bb, BLACK, seed=nx(), rough=0.4)
    lines = lin(W, H, [(cx - hw, top + hgt * (0.24 + 0.15 * r), cx + hw, top + hgt * (0.24 + 0.15 * r)) for r in range(rows + 1)], max(1.2, hgt * 0.012)) * tri
    art = GP(art, lines, BONE, seed=nx(), rough=0.3)
    dia = shapes(W, H, [[(cx, top + hgt * 0.04), (cx + hgt * 0.07, top + hgt * 0.13), (cx, top + hgt * 0.22), (cx - hgt * 0.07, top + hgt * 0.13)]], smooth=False)
    art = GP(art, dia, BONE, seed=nx(), rough=0.3)
    art = GP(art, shapes(W, H, [ellipse_pts(cx, top + hgt * 0.13, hgt * 0.025, hgt * 0.025, 10)]), BLACK, seed=nx(), rough=0.3)
    return art, tri


def horns(W, H, cx, y, s):
    """Stylised buffalo-horn finial: two upswept curved horns on a short post."""
    items = [([(cx, y + 22 * s), (cx, y)], 4 * s, None)]
    for d in (-1, 1):
        items.append((curve([(cx, y + 2 * s), (cx + d * 18 * s, y - 2 * s), (cx + d * 30 * s, y - 14 * s), (cx + d * 28 * s, y - 28 * s)], 20), 5 * s, (0.0, 0.8)))
    return strokes(W, H, items)


def rumah_bolon(art, W, H, nx, rng, cx, by, s):
    """Front-left three-quarter: gable end facing us at cx, long body receding to the right."""
    yy, xx = ygrid(W, H)
    fw = 120 * s           # half width of the front face
    L = 300 * s            # visible length of the side
    dy = -34 * s           # perspective rise of the far end
    # log-crib foundation: stacked horizontal logs with crossing ends (front + side)
    logs_f, logs_s, ends = [], [], []
    for k in range(6):
        y = by - 12 * s - k * 13 * s
        logs_f.append(rect(cx - fw - 10 * s, y - 6 * s, cx + fw + 10 * s, y + 6 * s))
        logs_s.append([(cx + fw, y - 6 * s), (cx + fw + L, y - 6 * s + dy * 0.5), (cx + fw + L, y + 6 * s + dy * 0.5), (cx + fw, y + 6 * s)])
        for ex in (cx - fw - 10 * s, cx + fw + 10 * s):
            ends.append(ellipse_pts(ex, y, 7 * s, 6.5 * s, 10))
    fs = shapes(W, H, logs_s, smooth=False)
    art = GP(art, fs, WOOD_D, WOOD, seed=nx(), rough=0.8, streak=1.0)
    ff = shapes(W, H, logs_f, smooth=False)
    art = GP(art, ff, WOOD, WOOD_L, seed=nx(), rough=0.8, streak=1.0)
    gaps = lin(W, H, [(cx - fw - 10 * s, by - 18 * s - k * 13 * s, cx + fw + 10 * s, by - 18 * s - k * 13 * s) for k in range(6)], 1.6 * s)
    art = G(art, gaps * ff, WOOD_D, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.5)
    art = GP(art, shapes(W, H, ends), "#9a7450", WOOD, seed=nx(), rough=0.5)
    floor_y = by - 12 * s - 6 * 13 * s
    # walls: front face boards + side wall
    wall_h = 70 * s
    side = shapes(W, H, [[(cx + fw, floor_y), (cx + fw + L, floor_y + dy * 0.5), (cx + fw + L, floor_y + dy * 0.5 - wall_h + 6 * s), (cx + fw, floor_y - wall_h)]], smooth=False)
    art = GP(art, side, "#4a3020", WOOD_D, seed=nx(), rough=0.6, streak=0.8)
    for k in range(5):
        x = cx + fw + L * (k + 0.5) / 5
        t = (x - cx - fw) / L
        y0 = floor_y + dy * 0.5 * t
        art = GP(art, shapes(W, H, [rect(x - 9 * s, y0 - wall_h * 0.75, x + 9 * s, y0 - wall_h * 0.35)], smooth=False), "#1c1410", seed=nx(), rough=0.3)
    front = shapes(W, H, [rect(cx - fw, floor_y - wall_h, cx + fw, floor_y)], smooth=False)
    art = GP(art, front, WOOD_L, WOOD, seed=nx(), rough=0.6, streak=0.9)
    art = G(art, lin(W, H, [(x, floor_y - wall_h, x, floor_y) for x in np.arange(cx - fw, cx + fw, 9 * s)], 1.2 * s) * front, WOOD_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.5)
    door = shapes(W, H, [rect(cx - 16 * s, floor_y - wall_h * 0.85, cx + 16 * s, floor_y)], smooth=False)
    art = GP(art, door, "#1c1410", seed=nx(), rough=0.3)
    # red-white band painted across the front wall (lintel)
    lint = shapes(W, H, [rect(cx - fw, floor_y - wall_h - 4 * s, cx + fw, floor_y - wall_h + 10 * s)], smooth=False)
    art = GP(art, lint, RED, RED_D, seed=nx(), rough=0.4)
    art = GP(art, lin(W, H, [(x, floor_y - wall_h + 7 * s, x + 7 * s, floor_y - wall_h - 1 * s) for x in np.arange(cx - fw, cx + fw, 10 * s)], 2 * s) * lint, BONE, seed=nx(), rough=0.3)
    # ladder
    lad = lin(W, H, [(cx - 14 * s, floor_y, cx - 22 * s, by + 4 * s), (cx + 14 * s, floor_y, cx + 22 * s, by + 4 * s)] + [(cx - 15 * s - k * 1.1 * s, floor_y + k * 11 * s, cx + 15 * s + k * 1.1 * s, floor_y + k * 11 * s) for k in range(1, 8)], 3 * s)
    art = GP(art, lad, "#7a5a3a", WOOD_D, seed=nx(), rough=0.4)
    # roof: side slope receding (ijuk), front gable triangle, eaves overhang
    eave_y = floor_y - wall_h - 6 * s
    top_y = eave_y - 190 * s
    side_roof = shapes(W, H, [[(cx - 4 * s, top_y + 10 * s), (cx + fw + L + 20 * s, top_y + 70 * s + dy * 0.4), (cx + fw + L + 40 * s, eave_y + 18 * s + dy * 0.5), (cx + fw + 30 * s, eave_y + 22 * s)]], smooth=False)
    art = GP(art, side_roof, IJUK, IJUK_L, seed=nx(), rough=1.4, streak=1.2)
    th = []
    for _ in range(int(1600 * s)):
        t = rng.random(); u = rng.random()
        x0 = cx + (fw + 30 * s) * u + (L + 20 * s) * t * (1 - 0.3 * u)
        y0 = (top_y + 10 * s) * (1 - u) + (eave_y + 20 * s) * u + (dy * 0.45) * t + 60 * s * t * (1 - u)
        Lh = rng.uniform(8, 18) * s
        th.append(([(x0, y0), (x0 + Lh * 0.35, y0 + Lh)], rng.uniform(1.0, 2.0) * s, (0.1, 0.5)))
    art = G(art, strokes(W, H, th) * side_roof, "#8a7e68", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = tint(art, side_roof * np.clip((yy - top_y) / (eave_y - top_y + 60 * s), 0, 1) ** 2, "#120e0c", 0.55)
    art = tint(art, side_roof * np.clip(1 - (yy - top_y) / (90 * s), 0, 1), "#b8b0a0", 0.25)
    # front eaves (ijuk overhang framing the gable)
    ov = shapes(W, H, [[(cx - fw - 40 * s, eave_y + 22 * s), (cx, top_y - 8 * s), (cx + fw + 40 * s, eave_y + 22 * s), (cx + fw + 24 * s, eave_y + 30 * s), (cx, top_y + 18 * s), (cx - fw - 24 * s, eave_y + 30 * s)]], smooth=False)
    art = GP(art, ov, IJUK, IJUK_L, seed=nx(), rough=1.2, streak=1.0)
    tri_pts = [(cx - fw - 6 * s, eave_y + 16 * s), (cx, top_y + 26 * s), (cx + fw + 6 * s, eave_y + 16 * s)]
    art, tri = gable_paint(art, W, H, nx, rng, tri_pts, cx, top_y + 26 * s, eave_y + 16 * s, fw + 6 * s)
    # small hipped crown at the ridge front + horn finial
    crown = shapes(W, H, [[(cx - 34 * s, top_y + 4 * s), (cx + 34 * s, top_y + 4 * s), (cx + 10 * s, top_y - 46 * s), (cx - 10 * s, top_y - 46 * s)]], smooth=False)
    art = GP(art, crown, IJUK, IJUK_L, seed=nx(), rough=1.0)
    cface = shapes(W, H, [[(cx - 20 * s, top_y + 2 * s), (cx, top_y - 30 * s), (cx + 20 * s, top_y + 2 * s)]], smooth=False)
    art = GP(art, cface, RED, RED_D, seed=nx(), rough=0.4)
    art = GP(art, lin(W, H, [(cx - 12 * s, top_y - 6 * s, cx + 12 * s, top_y - 6 * s)], 2.4 * s) * cface, BONE, seed=nx(), rough=0.3)
    hm = horns(W, H, cx, top_y - 64 * s, s)
    art = GP(art, hm, "#2a201a", "#4a3a2a", seed=nx(), rough=0.4)
    sil = np.maximum.reduce([fs, ff, side, front, side_roof, ov, tri, crown, hm])
    return art, sil


if "bolon" in PARTS:
    W, H = 780, 900
    nx = Seq(6100); rng = random.Random(61)
    yy, xx = ygrid(W, H)
    art = painted_sky(W, H, [(0, "#d9e2e2"), (0.3, "#e8ecea"), (0.45, "#f1efe6"), (0.5, "#c9d4d6"), (1, "#7d98a6")], seed=nx(), streak=0.4, grain=0.3)
    # far hills across the lake (west, misty)
    cl = strokes(W, H, [([(x, y), (x + L * 0.5, y - 4), (x + L, y)], rng.uniform(8, 18), (0.3, 0.4)) for x, y, L in
                        [(rng.uniform(-60, W), rng.uniform(60, 300), rng.uniform(140, 320)) for _ in range(14)]])
    art = G(art, cl, "#ffffff", "#e4eae8", seed=nx(), density=0.6, edge=0.3, bloom=0.5, rough=6)
    LK = 470
    for (y, amp, seed_, col, dens) in [(380, 50, 3, "#a9b9c0", 0.6), (430, 34, 4, "#8ea4ae", 0.75)]:
        hm = hills(W, H, y, amp, seed_, 0.7)
        art = G(art, hm * (yy < LK), col, mix(col, "#6f8893", 0.4), seed=nx(), density=dens, edge=0.4, bloom=0.5, rough=6)
    clear()
    lake = (yy >= LK).astype(np.float32)
    art = G(art, lake, "#9fb4bd", LAKE, seed=nx(), density=0.75, edge=0.0, bloom=0.4, rough=2)
    art = G(art, lake * np.clip((yy - LK) / 300, 0, 1), LAKE_D, seed=nx(), density=0.5, edge=0, bloom=0.3, rough=2)
    rip = sea_strokes(W, H, LK + 2, H, rng, n=200, length=(20, 120), width=(0.6, 1.8))
    art = G(art, rip * lake, "#e8eeee", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=0.6)
    for (bx, bw) in [(330, 30), (560, 18)]:
        bm = shapes(W, H, [[(bx - bw, LK + 60), (bx + bw, LK + 58), (bx + bw * 0.8, LK + 65), (bx - bw * 0.8, LK + 66)]], smooth=False)
        art = G(art, bm, "#3a3430", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5)
    # mist band over the water line
    art = tint(art, np.exp(-((yy - LK) / 26) ** 2).astype(np.float32), "#f2f2ee", 0.65)
    # steep near hills dropping into the lake on the left (eastern shore cliffs)
    cliff = shapes(W, H, [[(-20, 300), (50, 320), (110, 380), (160, 470), (190, 560), (230, 680), (-20, 720)]])
    art = G(art, cliff, "#4f6d5e", "#3a5648", seed=nx(), density=0.9, edge=0.5, bloom=0.4, rough=5, gran=0.3)
    art = G(art, cliff * np.clip((xx - 120) / 200, 0, 1), "#2c4238", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=3)
    clear()
    # pines on the cliff
    def pine(art, x, by_, h):
        tiers = []
        for k in range(6):
            t = k / 6
            yb = by_ - h * t * 0.85
            hw = h * 0.22 * (1 - t) + 3
            tiers.append([(x - hw, yb), (x, yb - h * 0.28), (x + hw, yb)])
        m = shapes(W, H, tiers, smooth=False)
        return G(art, m, "#2f4a3a", "#3e5c48", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1.5)
    for (x, by_, h) in [(30, 350, 90), (70, 366, 70), (112, 410, 74), (14, 410, 100), (150, 466, 56)]:
        art = pine(art, x, by_, h)
    clear()
    # foreground ridge (green, with a path) on which the house stands
    ridge = shapes(W, H, [[(-20, 790), (200, 760), (380, 730), (560, 712), (800, 690), (800, 920), (-20, 920)]])
    art = G(art, ridge, "#6f8a52", "#58744a", seed=nx(), density=0.95, edge=0.5, bloom=0.4, rough=4, gran=0.3)
    art = G(art, ridge * np.clip((yy - 720) / 200, 0, 1), "#34482c", seed=nx(), density=0.6, edge=0.1, bloom=0.3, rough=3)
    clear()
    house = blank(W, H)
    house, sil = rumah_bolon(house, W, H, nx, rng, 430, 748, 0.72)
    edge = np.clip(sil - gaussian_filter(sil, 1.2) * 1.05, 0, 1) * 2
    house = G(house, np.clip(edge, 0, 1), "#1a1412", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8, feather=0.5)
    sh = shapes(W, H, [deform(ellipse_pts(550, 752, 260, 14, 16), rng, 1, 0.04)])
    art = G(art, sh, "#2c3a22", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=3)
    art = over(art, house)
    clear()
    # banana + bamboo clump at the right
    for k in range(5):
        x = 30 + k * 18
        art = G(art, strokes(W, H, [(curve([(x, 880), (x + 6, 700), (x + 30 - k * 4, 540)], 20), 5, (0.0, 0.5))]), "#5f7a3e", "#7a8e46", seed=nx(), density=0.9, edge=0.4, bloom=0.1, rough=1)
    lv = []
    for k in range(40):
        x0 = rng.uniform(0, 170); y0 = rng.uniform(540, 780)
        a = rng.uniform(-0.3, 0.6) + (math.pi if rng.random() < 0.3 else 0)
        lv.append(petal_pts(x0, y0, rng.uniform(28, 46), rng.uniform(5, 8), a + math.pi * 0.0, n=8))
    art = G(art, shapes(W, H, lv), "#4f6a38", "#7a9248", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=1.5)
    # foreground grass strokes
    gs = [([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(14, 34))], rng.uniform(1, 2.2), (0, 0.7)) for x, y in [(rng.uniform(-10, W), rng.uniform(760, H)) for _ in range(500)]]
    art = G(art, strokes(W, H, gs), "#3e5a30", "#8aa060", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    clear()
    vm = vignette_mask(W, H, seed=nx(), inset=6, rough=24, fade=24)
    art[..., 3] *= np.clip(vm * 1.4, 0, 1)
    preview(art, "bolon", tone="#f3efe6")
    save(art, f"{OUT}/bolon.webp", max_w=760, quality=78)
    clear()

if "hiou" in PARTS:
    # warp-faced hiou: maroon ground, black + white pinstripe groups, a central field of white supplementary diamonds
    Tx, Ty = 96, 300
    pal = ["#7a1a22", "#1e1414", "#efe6d2", "#b8862e", "#a3282a"]
    col = np.zeros(Tx, np.int32)
    for (a, b, k) in [(0, 4, 1), (4, 5, 2), (5, 7, 1), (7, 8, 2), (8, 10, 1), (10, 14, 4), (14, 15, 3), (36, 37, 2), (38, 39, 2), (58, 59, 2), (60, 61, 2), (81, 82, 3), (82, 86, 4), (86, 88, 1), (88, 89, 2), (89, 91, 1), (91, 92, 2), (92, 96, 1)]:
        col[a:b] = k
    D = np.tile(col[None, :], (Ty, 1))
    # weft bands near the end (tumpal-like stripes)
    for (a, b, k) in [(240, 244, 1), (246, 248, 2), (250, 256, 4), (258, 260, 3), (262, 266, 1), (268, 300, 0)]:
        D[a:b, 14:82] = k
    cloth = ikat(D, pal, p=3, mode="warp", ground="#2a1414", amp=0.2, coh=2, along=10, face=0.8, seed=63, bleed=0.2, slub=0.25, fibre=0.08, tile=False)
    # supplementary white diamonds (pinar) in the central field
    S = np.zeros((Ty, Tx), np.float32)
    for r in range(20, 230, 18):
        for c0 in (24, 48, 72):
            cc = c0 + (9 if (r // 18) % 2 else 0) - 4
            for dy_ in range(-6, 7):
                w_ = 6 - abs(dy_)
                if 16 <= cc - w_ and cc + w_ < 80:
                    S[r + dy_, cc - w_:cc + w_ + 1] = 1
                    if w_ > 2:
                        S[r + dy_, cc - w_ + 2:cc + w_ - 1] = 0
    cloth = songket(cloth, S, p=3, base="#f2ead6", deep="#9a8a70", seed=64, float_len=3, tile=False)
    h, w = cloth.shape[:2]
    FR = 130
    W, H = w + 20, h + FR
    canvas = np.zeros((H, W, 3), np.float32)
    canvas[:h, 10:10 + w] = cloth
    # gentle hang: darker folds down the length
    yy, xx = ygrid(W, H)
    fold = 0.9 + 0.1 * np.sin((xx - 10) / w * math.pi * 3 + 0.5)
    canvas *= fold[..., None]
    m = np.zeros((H, W), np.float32); m[:h, 10:10 + w] = 1
    m = fray(m, seed=7, amount=1.0, scale=4, p=3)
    art = cutout(canvas, m, shadow=0.0)
    # twisted fringe (rambu): cords grouped, each with a small knot
    rng = random.Random(65); nx = Seq(6500)
    cords = []
    for k in range(24):
        x = 10 + (k + 0.5) * w / 24
        pts = [(x, h - 4)] + [(x + math.sin(j * 0.9 + k) * 1.6, h - 4 + j * (FR - 14) / 10) for j in range(1, 11)]
        cords.append((pts, 5.0, (0.0, 0.25)))
    cm = strokes(W, H, cords)
    fr = blank(W, H)
    fr = GP(fr, cm, "#7a1a22", "#5a1218", seed=nx(), rough=0.4)
    tw = lin(W, H, [(10 + (k + 0.5) * w / 24 - 2.5, y, 10 + (k + 0.5) * w / 24 + 2.5, y + 3) for k in range(24) for y in range(h + 4, h + FR - 18, 5)], 1.0) * cm
    fr = G(fr, tw, "#2a0c10", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, feather=0.4)
    kn = circles(W, H, [(10 + (k + 0.5) * w / 24, h + 6, 4.2) for k in range(24)])
    fr = GP(fr, kn, "#b8862e", seed=nx(), rough=0.3)
    art = over(fr, art)
    art = over(art, fr * np.concatenate([np.ones((H, W, 3)), (yy > h + 2)[..., None]], -1).astype(np.float32))
    preview(art, "hiou", tone="#f3efe6")
    save(art, f"{OUT}/hiou.webp", max_w=150, quality=82)
    clear()

if "gorga" in PARTS:
    W, H = 1000, 110
    nx = Seq(6700); rng = random.Random(67)
    band = shapes(W, H, [rect(0, 10, W, 100)], smooth=False)
    art = GP(blank(W, H), band, RED, RED_D, seed=nx(), rough=0.8, streak=0.8)
    # black border lines
    bl = lin(W, H, [(0, 16, W, 16), (0, 94, W, 94)], 3)
    art = GP(art, bl, BLACK, seed=nx(), rough=0.3)
    # chain of linked double spirals (white) with black fill triangles between
    items = []
    step = 100
    for k, x in enumerate(range(-50, W + 100, step)):
        d = 1 if k % 2 == 0 else -1
        a = spiral_pts(x, 55, 26, 4, math.pi if d > 0 else 0, 1.3, 40, d)
        b = spiral_pts(x + step / 2, 55, 26, 4, 0 if d > 0 else math.pi, 1.3, 40, d)
        items += [(a, 5, (0.0, 0.5)), (b, 5, (0.0, 0.5)), (curve([a[0], (x + step / 4, 55 - 26 * d), b[0]], 12), 5, None)]
    art = GP(art, strokes(W, H, items) * band, BONE, "#ddd0b6", seed=nx(), rough=0.4)
    tris = []
    for x in range(0, W + 20, 20):
        tris.append([(x, 22), (x + 10, 30), (x + 20, 22)])
        tris.append([(x, 88), (x + 10, 80), (x + 20, 88)])
    art = GP(art, shapes(W, H, tris, smooth=False), BLACK, seed=nx(), rough=0.3)
    art = GP(art, shapes(W, H, [rect(0, 2, W, 10), rect(0, 100, W, 108)], smooth=False), BONE, seed=nx(), rough=0.4)
    art = add_grain(art, 3, 0.03)
    preview(art, "gorga", tone="#f3efe6")
    save(art, f"{OUT}/gorga.webp", max_w=780, quality=80)
    clear()

if "atap" in PARTS:
    W, H = 300, 300
    nx = Seq(6900); rng = random.Random(69)
    art = blank(W, H)
    cx = 150
    ov = shapes(W, H, [[(10, 262), (cx, 70), (290, 262), (270, 272), (cx, 100), (30, 272)]], smooth=False)
    art = GP(art, ov, IJUK, IJUK_L, seed=nx(), rough=1.0)
    art, tri = gable_paint(art, W, H, nx, rng, [(36, 258), (cx, 104), (264, 258)], cx, 104, 258, 114)
    crown = shapes(W, H, [[(cx - 30, 80), (cx + 30, 80), (cx + 9, 40), (cx - 9, 40)]], smooth=False)
    art = GP(art, crown, IJUK, IJUK_L, seed=nx(), rough=0.8)
    art = GP(art, shapes(W, H, [[(cx - 16, 78), (cx, 52), (cx + 16, 78)]], smooth=False), RED, RED_D, seed=nx(), rough=0.4)
    art = GP(art, horns(W, H, cx, 36, 0.8), "#2a201a", "#4a3a2a", seed=nx(), rough=0.4)
    preview(art, "atap", tone="#f3efe6")
    save(art, f"{OUT}/atap.webp", max_w=140, quality=84)
    clear()
