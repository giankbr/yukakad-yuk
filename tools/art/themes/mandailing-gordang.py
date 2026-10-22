"""Mandailing Gordang — an original bagas godang (big house raised on many posts, broad black ijuk roof, a wide front
stair, a tall gable painted with red/white/black bindu triangles) with an open sopo beside it, among the layered green
hills and rice terraces of Tapanuli Selatan (watercolour + gouache); gordang sambilan, nine hand-carved drums of
decreasing size with hide heads, rattan lacing and wedges, standing on a rack; a single drum; a bindu triangle band.
Run: python3 -I mandailing-gordang.py [part ...]   parts: bagas gordang gendang bindu"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f1_lib import *
import _jw_lib

OUT = outdir("mandailing-gordang")
PARTS = sys.argv[1:] or ["bagas", "gordang", "gendang", "bindu"]
RED, RED_D = "#b02a26", "#7a1a18"
WHITE, BLACK = "#f2ead8", "#1e1a16"
GOLD = "#d4a440"
WOOD, WOOD_D, WOOD_L = "#7a4a2a", "#3e2416", "#a8703e"
IJUK, IJUK_L = "#24221e", "#46413a"
GREEN, GREEN_D, GREEN_L = "#3f7a46", "#24502e", "#8ab45a"
HIDE, HIDE_D = "#efe0bc", "#c9b07c"


def bindu_gable(art, W, H, nx, cx, top, base, hw):
    """Gable face: stacked rows of alternating red/black/white triangles with a central bindu star."""
    tri = shapes(W, H, [[(cx - hw, base), (cx, top), (cx + hw, base)]], smooth=False)
    art = GP(art, tri, WHITE, "#e4d8c0", seed=nx(), rough=0.5)
    hgt = base - top
    reds, blacks = [], []
    rows = 6
    for r in range(rows):
        y1 = top + hgt * (0.3 + 0.115 * (r + 1))
        y0 = y1 - hgt * 0.08
        w_at = hw * (y1 - top) / hgt
        n = max(3, int(w_at * 2 / (hgt * 0.085)))
        step = w_at * 2 / n
        for k in range(n):
            x0 = cx - w_at + k * step
            (reds if (k + r) % 2 == 0 else blacks).append([(x0, y1), (x0 + step / 2, y0), (x0 + step, y1)])
    art = GP(art, shapes(W, H, reds, smooth=False) * tri, RED, RED_D, seed=nx(), rough=0.4)
    art = GP(art, shapes(W, H, blacks, smooth=False) * tri, BLACK, seed=nx(), rough=0.4)
    # bindu: eight triangles around a centre (star) near the apex
    by_ = top + hgt * 0.2
    r0 = hgt * 0.09
    st = []
    for k in range(8):
        a = k * math.pi / 4
        st.append([(cx + math.cos(a - 0.3) * r0 * 0.45, by_ + math.sin(a - 0.3) * r0 * 0.45), (cx + math.cos(a) * r0, by_ + math.sin(a) * r0), (cx + math.cos(a + 0.3) * r0 * 0.45, by_ + math.sin(a + 0.3) * r0 * 0.45)])
    art = GP(art, shapes(W, H, st, smooth=False), RED, RED_D, seed=nx(), rough=0.3)
    art = FO(art, circles(W, H, [(cx, by_, r0 * 0.38)]), GOLD, seed=nx())
    return art, tri


def bagas_godang(art, W, H, nx, rng, cx, by, s):
    yy, xx = ygrid(W, H)
    hw = 150 * s
    floor = by - 74 * s
    # posts (many), cross beams
    xs = np.linspace(cx - hw + 8 * s, cx + hw - 8 * s, 9)
    pst = shapes(W, H, [rect(x - 4 * s, floor, x + 4 * s, by) for x in xs], smooth=False)
    art = GP(art, pst, WOOD, WOOD_D, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [deform(ellipse_pts(x, by + 2 * s, 8 * s, 4 * s, 10), rng, 1, 0.05) for x in xs]), "#8a8274", seed=nx(), rough=0.4)
    beam = lin(W, H, [(cx - hw, floor + 32 * s, cx + hw, floor + 32 * s)], 4 * s)
    art = GP(art, beam, WOOD_D, seed=nx(), rough=0.4)
    sill = shapes(W, H, [rect(cx - hw - 6 * s, floor - 8 * s, cx + hw + 6 * s, floor + 4 * s)], smooth=False)
    art = GP(art, sill, WOOD_D, WOOD, seed=nx(), rough=0.5)
    # walls
    wall_h = 78 * s
    wall = shapes(W, H, [rect(cx - hw, floor - 8 * s - wall_h, cx + hw, floor - 8 * s)], smooth=False)
    art = GP(art, wall, WOOD_L, WOOD, seed=nx(), rough=0.6, streak=0.9)
    art = G(art, lin(W, H, [(x, floor - wall_h, x, floor) for x in np.arange(cx - hw, cx + hw, 8 * s)], 1.1 * s) * wall, WOOD_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.5)
    art = G(art, wall * np.clip((xx - cx) / hw, 0, 1), "#3a2214", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=2)
    wins = []
    for x in np.linspace(cx - hw + 30 * s, cx + hw - 30 * s, 6):
        if abs(x - cx) < 30 * s:
            continue
        wins.append(rect(x - 11 * s, floor - 8 * s - wall_h * 0.78, x + 11 * s, floor - 8 * s - wall_h * 0.25))
    art = GP(art, shapes(W, H, wins, smooth=False), "#1e140e", seed=nx(), rough=0.3)
    # painted band under the eaves (red/black/white zigzag)
    band = shapes(W, H, [rect(cx - hw, floor - 8 * s - wall_h - 12 * s, cx + hw, floor - 8 * s - wall_h)], smooth=False)
    art = GP(art, band, RED, RED_D, seed=nx(), rough=0.4)
    zz = []
    y0 = floor - 8 * s - wall_h - 12 * s
    for x in np.arange(cx - hw, cx + hw, 12 * s):
        zz.append([(x, y0 + 12 * s), (x + 6 * s, y0 + 1 * s), (x + 12 * s, y0 + 12 * s)])
    art = GP(art, shapes(W, H, zz, smooth=False) * band, BLACK, seed=nx(), rough=0.3)
    # door + broad stair
    dw = 22 * s
    door = shapes(W, H, [rect(cx - dw, floor - 8 * s - wall_h * 0.88, cx + dw, floor - 8 * s)], smooth=False)
    art = GP(art, door, "#2a1a10", seed=nx(), rough=0.3)
    art = FO(art, lin(W, H, [(cx - dw, floor - 8 * s - wall_h * 0.88, cx + dw, floor - 8 * s - wall_h * 0.88)], 2.5 * s), GOLD, seed=nx())
    st = shapes(W, H, [[(cx - dw - 4 * s, floor), (cx + dw + 4 * s, floor), (cx + dw + 26 * s, by + 4 * s), (cx - dw - 26 * s, by + 4 * s)]], smooth=False)
    art = GP(art, st, "#9a6a3c", WOOD, seed=nx(), rough=0.5)
    art = G(art, lin(W, H, [(cx - 60 * s, y, cx + 60 * s, y) for y in np.arange(floor + 8 * s, by, 9 * s)], 1.8 * s) * st, WOOD_D, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.4, feather=0.4)
    # roof: broad black ijuk with long eaves, side slopes visible as wedges, tall front gable
    eave = floor - 8 * s - wall_h - 10 * s
    top = eave - 210 * s
    roof = shapes(W, H, [[(cx - hw - 78 * s, eave + 34 * s), (cx, top - 44 * s), (cx + hw + 78 * s, eave + 34 * s), (cx + hw + 50 * s, eave + 44 * s), (cx, top + 16 * s), (cx - hw - 50 * s, eave + 44 * s)]], smooth=False)
    art = GP(art, roof, IJUK, IJUK_L, seed=nx(), rough=1.2, streak=1.2)
    rs = []
    for _ in range(int(1400 * s)):
        t = rng.random(); side = rng.choice((-1, 1)); v = rng.random()
        x0 = cx + side * (hw + 78 * s) * t * (0.75 + 0.25 * v)
        y0 = (top - 44 * s) + (eave + 34 * s - top + 44 * s) * t + 30 * s * v
        L = rng.uniform(8, 18) * s
        rs.append(([(x0, y0), (x0 + side * L * 0.6, y0 + L)], rng.uniform(1.0, 1.8) * s, (0.1, 0.5)))
    art = G(art, strokes(W, H, rs) * roof, "#6a6252", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.5)

    art, tri = bindu_gable(art, W, H, nx, cx, top + 26 * s, eave + 16 * s, hw + 18 * s)
    # gable edge boards (red) + small crossed finials
    edge = strokes(W, H, [([(cx - hw - 22 * s, eave + 18 * s), (cx, top + 22 * s), (cx + hw + 22 * s, eave + 18 * s)], 6 * s, None)])
    art = GP(art, edge, RED, RED_D, seed=nx(), rough=0.4)
    fin = strokes(W, H, [([(cx - 4 * s, top + 26 * s), (cx + 18 * s, top - 26 * s)], 4 * s, (0, 0.5)), ([(cx + 4 * s, top + 26 * s), (cx - 18 * s, top - 26 * s)], 4 * s, (0, 0.5))])
    art = GP(art, fin, IJUK, seed=nx(), rough=0.3)
    sil = np.maximum.reduce([roof, wall, pst, st, tri])
    return art, sil


def sopo(art, W, H, nx, rng, cx, by, s):
    """Open hall: posts, low platform and a hipped ijuk roof; drums faintly inside."""
    hw = 70 * s
    plat = shapes(W, H, [rect(cx - hw, by - 30 * s, cx + hw, by - 22 * s)], smooth=False)
    pst = shapes(W, H, [rect(x - 3 * s, by - 100 * s, x + 3 * s, by) for x in np.linspace(cx - hw + 4 * s, cx + hw - 4 * s, 4)], smooth=False)
    art = GP(art, pst, WOOD, WOOD_D, seed=nx(), rough=0.5)
    drums = shapes(W, H, [rect(x - 5 * s, by - 30 * s - h * s, x + 5 * s, by - 30 * s) for x, h in zip(np.linspace(cx - hw + 16 * s, cx + hw - 16 * s, 9), np.linspace(52, 26, 9))], smooth=False)
    art = GP(art, drums, "#8a5a32", WOOD_D, seed=nx(), rough=0.4)
    art = GP(art, plat, WOOD_D, WOOD, seed=nx(), rough=0.4)
    roof = shapes(W, H, [[(cx - hw - 26 * s, by - 96 * s), (cx + hw + 26 * s, by - 96 * s), (cx + 22 * s, by - 170 * s), (cx - 22 * s, by - 170 * s)]], smooth=False)
    art = GP(art, roof, IJUK, IJUK_L, seed=nx(), rough=1.0, streak=1.0)
    return art


if "bagas" in PARTS:
    W, H = 780, 900
    nx = Seq(7100); rng = random.Random(71)
    yy, xx = ygrid(W, H)
    art = painted_sky(W, H, [(0, "#cfe0e2"), (0.3, "#e6eee6"), (0.42, "#f4f1e2"), (1, "#f4f1e2")], seed=nx(), streak=0.5, grain=0.3)
    cl = strokes(W, H, [([(x, y), (x + L * 0.5, y - 5), (x + L, y)], rng.uniform(10, 22), (0.3, 0.4)) for x, y, L in
                        [(rng.uniform(-60, W), rng.uniform(40, 260), rng.uniform(140, 300)) for _ in range(12)]])
    art = G(art, cl, "#ffffff", "#e9efea", seed=nx(), density=0.7, edge=0.3, bloom=0.5, rough=6)
    # layered hills: far blue -> near green
    layers = [(300, 60, 21, "#a8c0bc", "#93b0aa", 0.7), (360, 56, 22, "#7fa48a", "#6e9a7c", 0.8), (430, 48, 23, "#5f9460", "#4f8452", 0.9), (500, 36, 24, "#4f8a4c", "#3f7a42", 0.95)]
    for (y, amp, seed_, ca, cb, d) in layers:
        hm = hills(W, H, y, amp, seed_, 0.55)
        art = G(art, hm, ca, cb, seed=nx(), density=d, edge=0.45, bloom=0.4, rough=6, gran=0.25)
        art = tint(art, hm * np.exp(-((yy - y - 30) / 30) ** 2), "#f4f6ee", 0.35)
        clear()
    # tree clumps on the near hill
    for (tx, ty, r) in [(80, 520, 34), (150, 505, 26), (640, 500, 30), (720, 520, 38), (540, 515, 22)]:
        crown = blobs(W, H, [(tx, ty, 1.0)], rng, r=(r * 0.5, r * 0.8), n=6)
        art = G(art, crown, "#2f6a3a", "#3f7a42", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=2)
    clear()
    # coconut / areca palms
    for (px, h, ln) in [(60, 280, 0.06), (720, 300, -0.07), (760, 220, -0.03)]:
        art = G(art, _jw_lib.palm(W, H, px, 640, h, rng, ln), "#2f5a30", "#4a7a3a", seed=nx(), density=0.95, edge=0.45, bloom=0.2, rough=2)
    clear()
    # terraces in front: curved bands of bright green with darker bunds
    ter = shapes(W, H, [[(-20, 640), (200, 620), (400, 625), (600, 615), (800, 620), (800, 920), (-20, 920)]])
    art = G(art, ter, "#8ab45a", "#a6c463", seed=nx(), density=0.95, edge=0.4, bloom=0.4, rough=4, gran=0.2)
    bunds = []
    for k in range(7):
        y = 660 + k * 36 + k * k * 2
        pts = [(x, y + 10 * math.sin(x / 140 + k)) for x in range(-20, W + 30, 20)]
        bunds.append((pts, 2.5 + k * 0.5, None))
    bm = strokes(W, H, bunds) * ter
    art = G(art, bm, "#4f7a34", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1)
    art = G(art, ter * np.clip((yy - 700) / 220, 0, 1), "#4f8a3a", seed=nx(), density=0.45, edge=0, bloom=0.3, rough=3)
    # young rice tufts
    tufts = []
    for k in range(7):
        y = 660 + k * 36 + k * k * 2 + 14
        for x in np.arange(-10, W + 10, 14 + k * 2):
            for j in range(3):
                a = -math.pi / 2 + (j - 1) * 0.35
                L = 6 + k * 1.6
                tufts.append(([(x, y + 10 * math.sin(x / 140 + k)), (x + math.cos(a) * L, y + 10 * math.sin(x / 140 + k) + math.sin(a) * L)], 1.2 + k * 0.15, (0, 0.6)))
    art = G(art, strokes(W, H, tufts) * ter, "#5f9a3a", "#3f7a2a", seed=nx(), density=0.85, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    clear()
    # the house + sopo on a cleared yard
    yard = shapes(W, H, [deform(ellipse_pts(390, 640, 330, 22, 18), rng, 1, 0.03)])
    art = G(art, yard, "#c9b07a", "#b09a68", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=3)
    house = blank(W, H)
    house = sopo(house, W, H, nx, rng, 650, 640, 0.9)
    house, sil = bagas_godang(house, W, H, nx, rng, 340, 640, 1.0)
    edge = np.clip(sil - gaussian_filter(sil, 1.2) * 1.05, 0, 1) * 2
    house = G(house, np.clip(edge, 0, 1), "#140e0a", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8, feather=0.5)
    art = over(art, house)
    clear()
    vm = vignette_mask(W, H, seed=nx(), inset=6, rough=24, fade=24)
    art[..., 3] *= np.clip(vm * 1.4, 0, 1)
    art = add_grain(art, 7, 0.015)
    preview(art, "bagas", tone="#f4f1e2")
    save(art, f"{OUT}/bagas.webp", max_w=760, quality=78)
    clear()


def drum(art, W, H, nx, rng, x, by, h, r):
    """One gordang: a slightly tapered wooden body, hide head, rattan lacing to a wedge ring, carved foot."""
    yy, xx = ygrid(W, H)
    top = by - h
    body = shapes(W, H, [[(x - r, top + r * 0.18), (x + r, top + r * 0.18), (x + r * 0.86, by - r * 0.1), (x - r * 0.86, by - r * 0.1)]], smooth=False)
    art = GP(art, body, WOOD_L, WOOD, seed=nx(), rough=0.6, streak=1.0)
    # cylinder shading: light at left, dark at right
    u = np.clip((xx - (x - r)) / (2 * r), 0, 1)
    shade = body * (0.55 * np.clip((u - 0.42) * 1.7, 0, 1) - 0.18 * np.clip((0.35 - u) * 3, 0, 1))
    art = art.copy()
    art[..., :3] *= (1 - shade)[..., None]
    grain = strokes(W, H, [([(x + d * r * 0.9, top + r * 0.3), (x + d * r * 0.8 + rng.uniform(-1, 1), by - r * 0.2)], 1.0, (0.1, 0.1)) for d in np.linspace(-0.85, 0.85, 7)])
    art = G(art, grain * body, WOOD_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.5)
    # wedge ring at ~68% down
    ry_ = top + h * 0.66
    ring = shapes(W, H, [rect(x - r * 0.95, ry_ - 4, x + r * 0.95, ry_ + 4)], smooth=False) * body
    art = GP(art, ring, "#c99a5a", "#8a6234", seed=nx(), rough=0.3)
    wedges = shapes(W, H, [rect(xw - 2.4, ry_ - 3, xw + 2.4, ry_ + 13) for xw in np.linspace(x - r * 0.8, x + r * 0.8, 6)], smooth=False)
    art = GP(art, wedges, "#d8b070", "#a07a40", seed=nx(), rough=0.3)
    # rattan lacing zigzag from head rim to ring
    pts = []
    n = 7
    for k in range(n * 2 + 1):
        t = k / (n * 2)
        px = x - r * 0.92 + t * r * 1.84
        py = top + r * 0.22 if k % 2 == 0 else ry_ - 4
        pts.append((px, py))
    lace = strokes(W, H, [(pts, 1.8, None)]) * body
    art = GP(art, lace, "#e2c890", "#b8945a", seed=nx(), rough=0.3)
    # head: hide ellipse with rim
    head = shapes(W, H, [ellipse_pts(x, top + r * 0.18, r, r * 0.3, 18)])
    art = GP(art, head, HIDE, HIDE_D, seed=nx(), rough=0.4)
    art = tint(art, head * np.clip((xx - x) / r, 0, 1), "#8a6a3a", 0.3)
    rim = np.clip(head - shapes(W, H, [ellipse_pts(x, top + r * 0.2, r * 0.86, r * 0.24, 18)]), 0, 1)
    art = GP(art, rim, "#6a4a2a", seed=nx(), rough=0.3)
    # foot
    foot = shapes(W, H, [[(x - r * 0.86, by - r * 0.12), (x + r * 0.86, by - r * 0.12), (x + r * 0.7, by), (x - r * 0.7, by)]], smooth=False)
    art = GP(art, foot, WOOD_D, seed=nx(), rough=0.3)
    return art


if "gordang" in PARTS:
    W, H = 1000, 460
    nx = Seq(7300); rng = random.Random(73)
    art = blank(W, H)
    # rack: two posts and a cross pole behind the drums
    rack = lin(W, H, [(30, 160, 980, 230), (40, 150, 40, 440), (970, 220, 970, 440)], 8)
    art = GP(art, rack, WOOD_D, WOOD, seed=nx(), rough=0.5)
    ground = shapes(W, H, [deform(ellipse_pts(500, 440, 490, 16, 18), rng, 1, 0.03)])
    art = G(art, ground, "#3a2a1c", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=3)
    x = 70
    for k in range(9):
        h = 330 - k * 25
        r = 50 - k * 2.6
        art = drum(art, W, H, nx, rng, x, 438, h, r)
        x += 2 * r + 8
        clear()
    # two beaters resting
    sticks = lin(W, H, [(820, 438, 900, 410), (835, 440, 925, 420)], 4)
    art = GP(art, sticks, "#c9a06a", WOOD, seed=nx(), rough=0.3)
    preview(art, "gordang", tone="#f4f1e2")
    save(art, f"{OUT}/gordang.webp", max_w=640, quality=82)
    clear()

if "gendang" in PARTS:
    W, H = 160, 260
    nx = Seq(7500); rng = random.Random(75)
    art = blank(W, H)
    art = drum(art, W, H, nx, rng, 80, 250, 230, 56)
    preview(art, "gendang", tone="#f4f1e2")
    save(art, f"{OUT}/gendang.webp", max_w=70, quality=84)
    clear()

if "bindu" in PARTS:
    W, H = 1000, 70
    nx = Seq(7700); rng = random.Random(77)
    band = shapes(W, H, [rect(0, 8, W, 62)], smooth=False)
    art = GP(blank(W, H), band, BLACK, "#2a241e", seed=nx(), rough=0.6)
    up, dn = [], []
    step = 36
    for x in range(-step, W + step, step):
        up.append([(x, 56), (x + step / 2, 14), (x + step, 56)])
        dn.append([(x + step / 2 + 4, 16), (x + step - 0, 50), (x + step + step / 2 - 4, 16)])
    art = GP(art, shapes(W, H, up, smooth=False) * band, RED, RED_D, seed=nx(), rough=0.4)
    inner = []
    for x in range(-step, W + step, step):
        inner.append([(x + 9, 52), (x + step / 2, 28), (x + step - 9, 52)])
    art = GP(art, shapes(W, H, inner, smooth=False) * band, WHITE, seed=nx(), rough=0.3)
    art = FO(art, shapes(W, H, [rect(0, 2, W, 9), rect(0, 61, W, 68)], smooth=False), GOLD, seed=nx(), emboss=0.4)
    art = add_grain(art, 3, 0.03)
    preview(art, "bindu", tone="#f4f1e2")
    save(art, f"{OUT}/bindu.webp", max_w=780, quality=80)
    clear()
