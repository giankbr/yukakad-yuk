"""Bima Mbojo — uma lengge rice barns (tall steep alang-alang roofs on four posts with round rat-guard discs) on a dry
savanna hill above the calm Teluk Bima at dusk, in gouache; tembe nggoli check cloth woven at thread level (seamless
tile + a folded cloth band); a single uma lengge emblem; a tied sheaf of rice.
Run: python3 -I bima-mbojo.py [part ...]   parts: lengge tembe pita lengge1 padi"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f1_lib import *
import _jw_lib

OUT = outdir("bima-mbojo")
PARTS = sys.argv[1:] or ["lengge", "tembe", "pita", "lengge1", "padi"]
MAG, MAG_D, AUB = "#a3243f", "#6e1530", "#2c1830"
SAF, SAF_L = "#e3a83a", "#f2cf7a"
TEAL, TEAL_D = "#2f6f78", "#1d4a54"
THATCH, THATCH_D, THATCH_L = "#b98d4e", "#7a5a2e", "#dcb878"
POST, POST_D = "#6a4a30", "#3e2a1a"
GRASS, GRASS_D = "#c99a52", "#9a7038"
WEAVE = ["#9c1f3a", "#2a1424", "#e2a52e", "#f1e6d0", "#1f6f6b", "#c8455a"]


def uma_lengge(art, W, H, nx, rng, cx, by, s, light=1.0):
    """One uma lengge (front view); by = ground, s = scale. Tall hipped thatch roof with a front face, side slivers and
    a hanging straw skirt; four posts with round rat-guard discs; a sitting deck between the posts. Light from the left."""
    yy, xx = ygrid(W, H)
    rw, rh = 60 * s, 210 * s
    post_h = 92 * s
    ry = by - post_h
    bp = shapes(W, H, [rect(cx + d * 22 * s - 3 * s, ry - 4 * s, cx + d * 22 * s + 3 * s, by - 8 * s) for d in (-1, 1)], smooth=False)
    art = GP(art, bp, mix(POST, "#c9b08a", 0.3), POST, seed=nx(), rough=0.6)
    deck = shapes(W, H, [rect(cx - 50 * s, by - 40 * s, cx + 50 * s, by - 33 * s)], smooth=False)
    art = GP(art, deck, "#9a7a50", POST_D, seed=nx(), rough=0.6)
    art = G(art, lin(W, H, [(x, by - 40 * s, x, by - 33 * s) for x in np.arange(cx - 48 * s, cx + 50 * s, 6 * s)], 1.0) * deck, POST_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
    fp = shapes(W, H, [rect(cx + d * 40 * s - 4 * s, ry - 4 * s, cx + d * 40 * s + 4 * s, by) for d in (-1, 1)], smooth=False)
    art = GP(art, fp, POST, POST_D, seed=nx(), rough=0.6)
    stones = shapes(W, H, [deform(ellipse_pts(cx + d * 40 * s, by + 1 * s, 9 * s, 5 * s, 10), rng, 1, 0.05) for d in (-1, 1)])
    art = GP(art, stones, "#8f8678", "#6a6258", seed=nx(), rough=0.5)
    discs = shapes(W, H, [ellipse_pts(cx + d * 40 * s, ry + 8 * s, 13 * s, 4.5 * s, 14) for d in (-1, 1)])
    art = GP(art, discs, "#7d5a36", POST_D, seed=nx(), rough=0.4)
    art = GP(art, shapes(W, H, [rect(cx - 52 * s, ry - 2 * s, cx + 52 * s, ry + 3 * s)], smooth=False), POST_D, seed=nx(), rough=0.4)

    def prof(t, w):  # half-width at height fraction t (0 = eave, 1 = apex): steep with a gentle belly
        return w * (1 - t) ** 0.85 * (1 + 0.1 * math.sin(math.pi * t))
    ap = (cx, ry - rh)
    outer = [(cx - prof(i / 24, rw), ry - rh * i / 24) for i in range(25)]
    outer = outer + [(2 * cx - x, y) for (x, y) in outer[::-1]]
    roof = shapes(W, H, [outer], smooth=False)
    front = [(cx - prof(i / 24, rw * 0.72), ry - rh * i / 24) for i in range(25)]
    front = front + [(2 * cx - x, y) for (x, y) in front[::-1]]
    fm = shapes(W, H, [front], smooth=False)
    art = GP(art, roof, THATCH_D, THATCH, seed=nx(), rough=1.0, streak=1.0)
    art = GP(art, fm, THATCH, THATCH_L, seed=nx(), rough=1.0, streak=1.0)
    left_side = roof * (1 - fm) * (xx < cx)
    art = tint(art, left_side, "#f0d090", 0.35 * light)
    art = tint(art, fm * np.clip((xx - cx) / (rw * 0.8), 0, 1), "#6a4a24", 0.3)
    # straw: near-vertical strokes following the roof
    items = []
    for _ in range(int(420 * s)):
        t0 = rng.random() ** 0.8
        u = rng.uniform(-1, 1)
        y0 = ry - rh * t0
        x0 = cx + u * prof(t0, rw)
        L = rng.uniform(10, 24) * s
        t1 = max(0.0, t0 - L / rh)
        x1 = cx + u * prof(t1, rw)
        items.append(([(x0, y0), (x1, ry - rh * t1)], rng.uniform(0.8, 1.6) * max(0.7, s), (0.1, 0.4)))
    art = G(art, strokes(W, H, items) * roof, "#5e4020", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    # hanging skirt fringe
    fr = [([(x, ry - 2 * s), (x + rng.uniform(-1.5, 1.5) * s, ry + rng.uniform(6, 12) * s)], 1.4 * s, (0.0, 0.5)) for x in np.arange(cx - rw, cx + rw, 2.4 * s)]
    art = G(art, strokes(W, H, fr), THATCH, THATCH_D, seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5)
    # bamboo tie bands
    for f in (0.3, 0.58):
        y = ry - rh * f
        art = G(art, lin(W, H, [(cx - prof(f, rw), y, cx + prof(f, rw), y + 1)], 2.4 * s), "#4a2e16", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.5)
    # gable door (small square hatch) and the little ventilation triangle
    gy = ry - rh * 0.44
    art = GP(art, shapes(W, H, [rect(cx - 9 * s, gy, cx + 9 * s, gy + 18 * s)], smooth=False), "#7a5432", POST_D, seed=nx(), rough=0.4)
    art = G(art, lin(W, H, [(cx - 9 * s, gy, cx + 9 * s, gy), (cx - 9 * s, gy + 18 * s, cx + 9 * s, gy + 18 * s), (cx, gy, cx, gy + 18 * s)], 1.5 * s), POST_D, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)
    vy = ry - rh * 0.74
    art = GP(art, shapes(W, H, [[(cx - 6 * s, vy + 10 * s), (cx, vy - 2 * s), (cx + 6 * s, vy + 10 * s)]], smooth=False), "#2e1e12", seed=nx(), rough=0.3)
    cap = strokes(W, H, [([(cx - 5 * s, ap[1] + 12 * s), (cx, ap[1] - 8 * s), (cx + 5 * s, ap[1] + 12 * s)], 3.6 * s, None)])
    art = GP(art, cap, "#4a2e16", POST_D, seed=nx(), rough=0.4)
    return art, np.maximum.reduce([roof, fp, bp, deck])


def lontar(art, W, H, nx, rng, x, by, h):
    trunk = strokes(W, H, [(curve([(x, by), (x + 2, by - h * 0.5), (x + 4, by - h)], 20), max(3, h * 0.03), (0.0, 0.3))])
    art = GP(art, trunk, "#5a4a3a", "#3a2e24", seed=nx(), rough=0.6)
    back, front = [], []
    for k in range(15):
        a = -math.pi / 2 + (k - 7) * 0.36 + rng.uniform(-0.1, 0.1)
        L = h * rng.uniform(0.15, 0.22)
        px, py = x + 4 + math.cos(a) * L * 0.5, by - h + math.sin(a) * L * 0.45 + L * 0.15
        ribs = []
        for j in range(11):
            b = a - 0.75 + j * 0.15
            ribs.append(([(px, py), (px + math.cos(b) * L * 0.55, py + math.sin(b) * L * 0.55), (px + math.cos(b) * L, py + math.sin(b) * L + L * 0.12)], max(1.6, h * 0.008), (0.05, 0.5)))
        (back if k % 2 else front).extend(ribs)
    art = G(art, strokes(W, H, back), "#3f5a32", "#55703e", seed=nx(), density=0.95, edge=0.4, bloom=0.2, rough=1.0)
    art = G(art, strokes(W, H, front), "#66803e", "#8a9a50", seed=nx(), density=0.95, edge=0.4, bloom=0.2, rough=1.0)
    return art


if "lengge" in PARTS:
    W, H = 780, 940
    nx = Seq(5100); rng = random.Random(51)
    yy, xx = ygrid(W, H)
    HZ = 430
    art = painted_sky(W, H, [(0, "#efd3c0"), (0.22, "#f4c7a0"), (0.4, "#f2b07c"), (0.47, "#e99a6c"), (0.5, "#8fa3a4"), (1, "#2c5c66")], seed=nx(), streak=0.7)
    # low sun over the bay
    SX, SY = 520, 372
    art = tint(art, np.exp(-((np.hypot(xx - SX, yy - SY) / 170) ** 2)).astype(np.float32) * (yy < HZ), "#fff1cc", 0.7)
    art = G(art, np.clip((30 - np.hypot(xx - SX, yy - SY)) / 3, 0, 1), "#fff4d8", "#ffe2a8", seed=nx(), density=0.95, edge=0.15, bloom=0, rough=1.5)
    # long cloud streaks
    cl = strokes(W, H, [([(x, y), (x + L * 0.5, y - 3), (x + L, y)], rng.uniform(4, 9), (0.3, 0.4)) for x, y, L in
                        [(rng.uniform(-60, W), rng.uniform(70, 330), rng.uniform(120, 300)) for _ in range(16)]])
    art = G(art, cl, "#f7d9c0", "#d99a88", seed=nx(), density=0.6, edge=0.3, bloom=0.3, rough=4)
    # far hills across the bay (two layers)
    h1 = hills(W, H, HZ - 46, 30, 11, 0.6) * (yy < HZ + 1)
    art = GP(art, h1, "#9a8aa6", "#8a7a9a", seed=nx(), rough=2.5)
    h2 = hills(W, H, HZ - 16, 16, 12, 0.35) * (yy < HZ + 1)
    art = GP(art, h2, "#6f6a8a", "#5e5a7a", seed=nx(), rough=2.5)
    clear()
    # bay water
    water = (yy >= HZ).astype(np.float32)
    art = GP(art, water, "#5e8c92", TEAL, seed=nx(), rough=0.5, streak=0.6)
    art = tint(art, water * np.clip((yy - HZ) / 260, 0, 1), TEAL_D, 0.55)
    rip = sea_strokes(W, H, HZ + 3, H, rng, n=260, length=(16, 110), width=(0.8, 2.4))
    art = G(art, rip * water, "#f6c9a0", "#ffe6c0", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1, feather=0.6)
    art = tint(art, rip * water * np.exp(-((xx - SX) / 60) ** 2), "#fff2d0", 0.95)
    # little fishing boats far out
    for (bx, bw) in [(170, 26), (640, 20)]:
        bm = shapes(W, H, [[(bx - bw, HZ + 22), (bx + bw, HZ + 22), (bx + bw * 0.7, HZ + 28), (bx - bw * 0.7, HZ + 28)]], smooth=False)
        art = GP(art, bm, "#3a2a2a", seed=nx(), rough=0.4)
        art = GP(art, lin(W, H, [(bx, HZ + 22, bx, HZ + 2)], 1.6), "#3a2a2a", seed=nx(), rough=0.3)
    clear()
    # foreground hill: dry savanna, ochre
    hill = shapes(W, H, [[(-20, 560), (120, 520), (300, 540), (480, 590), (640, 610), (800, 600), (800, 960), (-20, 960)]])
    art = GP(art, hill, GRASS, "#b8884a", seed=nx(), rough=3, streak=0.8)
    art = tint(art, hill * np.clip((yy - 560) / 380, 0, 1), "#7a4a2a", 0.4)
    grass = []
    for _ in range(700):
        x = rng.uniform(-10, W + 10); y = rng.uniform(530, H)
        L = rng.uniform(6, 16) * (0.6 + (y - 530) / 400)
        a = -math.pi / 2 + rng.uniform(-0.4, 0.4)
        grass.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(0.8, 1.8), (0.0, 0.6)))
    gm = strokes(W, H, grass) * hill
    art = G(art, gm, "#8a5f2e", "#e8c27a", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    clear()
    # lontar palms
    # a gnarled tamarind on the right
    trunk = strokes(W, H, [(curve([(700, 640), (690, 560), (712, 480), (700, 420)], 30), 16, (0.0, 0.4)),
                           (curve([(698, 520), (650, 470), (610, 440)], 20), 8, (0.0, 0.6)), (curve([(706, 480), (750, 440), (790, 420)], 20), 8, (0.0, 0.6))])
    art = GP(art, trunk, "#4a3626", "#2e2018", seed=nx(), rough=1.0)
    crown = blobs(W, H, [(660, 400, 1.2), (720, 370, 1.4), (600, 430, 1.0), (770, 400, 1.1), (690, 340, 1.0)], rng, r=(26, 44), n=7)
    art = GP(art, crown, "#5a6a36", "#76843e", seed=nx(), rough=3)
    lite = blobs(W, H, [(640, 380, 0.8), (700, 345, 0.9), (600, 418, 0.7)], rng, r=(18, 30), n=5) * crown
    art = GP(art, lite, "#8a9448", "#a2a858", seed=nx(), rough=2)
    art = G(art, crown * np.clip((xx - 680) / 120, 0, 1), "#2e3a1e", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=2)
    clear()
    # the barns, back to front
    for (cx, by, s_) in [(392, 566, 0.5), (470, 584, 0.58), (120, 610, 0.72), (560, 664, 0.86), (290, 740, 1.12)]:
        sh = shapes(W, H, [deform(ellipse_pts(cx + 18 * s_, by + 2, 70 * s_, 9 * s_, 14), rng, 1, 0.04)])
        art = G(art, sh, "#5a3418", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=2)
        art, _ = uma_lengge(art, W, H, nx, rng, cx, by, s_)
        clear()
    # foreground grass tufts
    tufts = []
    for _ in range(140):
        x = rng.uniform(-20, W + 20); y = rng.uniform(800, H)
        for k in range(12):
            a = -math.pi / 2 + rng.uniform(-0.5, 0.5); L = rng.uniform(26, 60)
            tufts.append(([(x, y), (x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5), (x + math.cos(a) * L + rng.uniform(-8, 8), y + math.sin(a) * L)], rng.uniform(1.0, 1.8), (0.0, 0.8)))
    art = GP(art, strokes(W, H, tufts), "#d8b06a", "#a87a3c", seed=nx(), rough=0.4)
    clear()
    # ragged painted edge
    vm = vignette_mask(W, H, seed=nx(), inset=6, rough=24, fade=24)
    art[..., 3] *= np.clip(vm * 1.4, 0, 1)
    art = add_grain(art, 5, 0.02)
    preview(art, "lengge", tone="#f6ead8")
    save(art, f"{OUT}/lengge.webp", max_w=760, quality=78)
    clear()

if "tembe" in PARTS:
    N = 160
    # tembe nggoli: bold red checks, black and gold bars, fine white lines
    bands = [(0, 26, 0), (26, 34, 1), (34, 36, 3), (36, 44, 2), (44, 46, 3), (46, 54, 1), (54, 80, 0),
             (80, 84, 5), (84, 106, 0), (106, 110, 4), (110, 112, 3), (112, 116, 4), (116, 140, 0), (140, 142, 2), (142, 160, 0)]
    D = check_design(N, bands, 0)
    cloth = ikat(D, WEAVE, p=3, mode="double", amp=0.25, coh=2.0, along=10, seed=53, bleed=0.25, slub=0.2, fibre=0.08, thread_var=0.05)
    # nggoli sheen: soft diagonal gloss
    h, w = cloth.shape[:2]
    yy, xx = ygrid(w, h)
    gl = 0.5 + 0.5 * np.sin((xx + yy) / w * 2 * math.pi)
    cloth = np.clip(cloth * (0.95 + 0.1 * gl[..., None]), 0, 1)
    prev_rgb(cloth, "tembe")
    save_rgb_arr(cloth, f"{OUT}/tembe.webp", quality=78)
    clear()

if "pita" in PARTS:
    # a folded tembe band: cloth strip with a soft wave, folds shading and a hemmed edge
    N = 160
    bands = [(0, 26, 0), (26, 34, 1), (34, 36, 3), (36, 44, 2), (44, 46, 3), (46, 54, 1), (54, 80, 0),
             (80, 84, 5), (84, 106, 0), (106, 110, 4), (110, 112, 3), (112, 116, 4), (116, 140, 0), (140, 142, 2), (142, 160, 0)]
    D = check_design(N, bands, 0)
    tile = ikat(D, WEAVE, p=2, mode="double", amp=0.25, coh=2.0, along=10, seed=55, bleed=0.25, slub=0.2, fibre=0.08)
    W, H = 1000, 130
    cloth = tile_to(tile, W, H)
    yy, xx = ygrid(W, H)
    folds = 0.82 + 0.18 * np.sin(xx / 120 * math.pi + 0.6) * np.sin(xx / 47 + 1.0) ** 2
    cloth = cloth * folds[..., None]
    top = 18 + 6 * np.sin(xx / 160 * math.pi)
    bot = 112 + 6 * np.sin(xx / 160 * math.pi + 0.8)
    m = np.clip(np.minimum(yy - top, bot - yy) / 1.5, 0, 1).astype(np.float32)
    m = fray(m, seed=5, amount=1.2, scale=4, p=2)
    hem = (np.abs(yy - top - 5) < 1.4) | (np.abs(bot - 5 - yy) < 1.4)
    cloth = np.where(hem[..., None], cloth * 0.55 + C(SAF) * 0.45, cloth)
    art = cutout(cloth, m, shadow=0.3)
    preview(art, "pita", tone="#f6ead8")
    save(art, f"{OUT}/pita.webp", max_w=780, quality=80)
    clear()

if "lengge1" in PARTS:
    W, H = 340, 620
    nx = Seq(5700); rng = random.Random(57)
    art = blank(W, H)
    gr = shapes(W, H, [deform(ellipse_pts(176, 590, 130, 16, 16), rng, 1, 0.05)])
    art = G(art, gr, GRASS, GRASS_D, seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=3)
    art, _ = uma_lengge(art, W, H, nx, rng, 170, 588, 1.6)
    preview(art, "lengge1", tone="#f6ead8")
    save(art, f"{OUT}/lengge1.webp", max_w=170, quality=82)
    clear()

if "padi" in PARTS:
    W, H = 480, 420
    nx = Seq(5900); rng = random.Random(59)
    art = blank(W, H)
    stalks, grains = [], []
    for k in range(26):
        a = -math.pi / 2 + (k - 12.5) * 0.016 + rng.uniform(-0.01, 0.01)
        L = rng.uniform(250, 290)
        bx = 150 + (k - 12.5) * 1.2
        top = (bx + math.cos(a) * L, 410 + math.sin(a) * L)
        bend = 10 + (k - 12.5) * 2.2
        pts = curve([(bx, 410), (bx + math.cos(a) * L * 0.55, 410 + math.sin(a) * L * 0.55), (top[0] + bend * 3.5 + 30, top[1] + 50 + rng.uniform(0, 30))], 24)
        stalks.append((pts, 2.0, (0.0, 0.3)))
        # drooping panicle of grains near the top
        for j in range(14, 24):
            px, py = pts[j]
            for sgn in (-1, 1):
                gx = px + sgn * rng.uniform(3, 6) + bend * 0.2
                gy = py + rng.uniform(-2, 4)
                grains.append(deform(ellipse_pts(gx, gy, 2.6, 4.6, 8, rng.uniform(-0.5, 0.5) + sgn * 0.4), rng, 1, 0.08))
    sm = strokes(W, H, stalks)
    art = G(art, sm, "#a88a3a", "#c9a24e", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=0.8)
    gm = shapes(W, H, grains)
    art = GP(art, gm, SAF, "#c98a2a", seed=nx(), rough=0.4)
    art = G(art, gm, "#8a5a1a", seed=nx(), density=0.25, edge=0.5, bloom=0, rough=0.4)
    # tie: a small band of tembe red around the bundle
    tie = shapes(W, H, [[(132, 318), (172, 314), (174, 334), (130, 337)]], smooth=True)
    art = GP(art, tie, MAG, MAG_D, seed=nx(), rough=0.6)
    art = GP(art, lin(W, H, [(132, 326, 172, 323)], 2) * tie, SAF, seed=nx(), rough=0.3)
    preview(art, "padi", tone="#f6ead8")
    save(art, f"{OUT}/padi.webp", max_w=160, quality=82)
    clear()
