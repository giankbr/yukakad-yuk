"""Kutai Erau — an original wooden keraton of the Kutai Kartanegara sultanate on the bank of the Mahakam at golden hour
(three-tier sirap roof, yellow walls with green pilasters, umbul-umbul banners, a jetty), long river boats with
yellow-green bands, Kutai carved-wood ornament (green lacquer with gold relief), a carved corner and a carved rosette.
Run: python3 -I kutai-erau.py [part ...]   parts: keraton perahu ukir sudut kembang"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f1_lib import *
import _jw_lib

OUT = outdir("kutai-erau")
PARTS = sys.argv[1:] or ["keraton", "perahu", "ukir", "sudut", "kembang"]
YEL, YEL_L, YEL_D = "#e8bf3e", "#f4dc86", "#b38a22"
GRN, GRN_D, GRN_L = "#2f5e3c", "#1c3a27", "#5d8c4f"
GOLD = "#d2a743"
WOOD, WOOD_D = "#6a4428", "#3d2615"
ROOF, ROOF_D = "#3f4c3a", "#262f24"


def keraton(art, W, H, nx, rng, cx, by):
    """Raised wooden palace; by = floor level. Returns art and the full silhouette mask."""
    sil = []
    # stilts + floor beam
    pst = shapes(W, H, [rect(x - 3, by, x + 3, by + 64) for x in range(cx - 236, cx + 240, 24)], smooth=False)
    art = GP(art, pst, WOOD, WOOD_D, seed=nx(), rough=1.0)
    beam = shapes(W, H, [rect(cx - 250, by - 10, cx + 250, by + 4)], smooth=False)
    art = GP(art, beam, WOOD_D, WOOD, seed=nx(), rough=0.8)
    # side wings (lower pavilions)
    for s in (-1, 1):
        x0 = cx + s * 250; x1 = cx + s * 380
        lo, hi = min(x0, x1), max(x0, x1)
        wall = shapes(W, H, [rect(lo, by - 52, hi, by - 8)], smooth=False)
        art = GP(art, wall, YEL, YEL_L if s > 0 else YEL_D, seed=nx(), rough=0.8, streak=0.7)
        win = shapes(W, H, [rect(x - 7, by - 44, x + 7, by - 16) for x in range(lo + 16, hi - 8, 26)], smooth=False)
        art = GP(art, win, GRN, GRN_D, seed=nx(), rough=0.6)
        rf = shapes(W, H, [[(lo - 14, by - 50), (hi + 14, by - 50), (hi - 30, by - 92), (lo + 30, by - 92)]], smooth=False)
        art = GP(art, rf, ROOF, ROOF_D, seed=nx(), rough=1.0, streak=0.9)
        sil += [wall, rf]
        wp = shapes(W, H, [rect(x - 3, by, x + 3, by + 60) for x in range(lo + 6, hi, 24)], smooth=False)
        art = GP(art, wp, WOOD, WOOD_D, seed=nx(), rough=1.0)
    # main hall walls
    wall = shapes(W, H, [rect(cx - 210, by - 86, cx + 210, by - 8)], smooth=False)
    yy, xx = ygrid(W, H)
    art = GP(art, wall, YEL, YEL_L, seed=nx(), rough=0.8, streak=0.8)
    art = G(art, wall * np.clip((cx - xx) / 420 + 0.2, 0, 1), "#b98a2a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
    art = G(art, lin(W, H, [(x, by - 86, x + 1, by - 8) for x in range(cx - 208, cx + 210, 7)], 1.0) * wall, "#9a7420", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.5)
    pil = shapes(W, H, [rect(x - 4, by - 86, x + 4, by - 8) for x in range(cx - 206, cx + 210, 46)], smooth=False)
    art = GP(art, pil, GRN, GRN_D, seed=nx(), rough=0.6)
    wins = []
    for x in range(cx - 183, cx + 190, 46):
        if abs(x - cx) < 50:
            continue
        wins.append(rect(x - 9, by - 70, x + 9, by - 22))
    wm = shapes(W, H, wins, smooth=False)
    art = GP(art, wm, "#2a2618", "#3b3220", seed=nx(), rough=0.5)
    sh = shapes(W, H, [rect(x - 9, by - 70, x - 1, by - 22) for x in range(cx - 183, cx + 190, 46) if abs(x - cx) >= 50], smooth=False)
    art = GP(art, sh, GRN_L, GRN, seed=nx(), rough=0.5)
    fas = shapes(W, H, [rect(cx - 214, by - 92, cx + 214, by - 82)], smooth=False)
    art = GP(art, fas, "#f3ead0", "#e4d6b0", seed=nx(), rough=0.5)
    zig = lin(W, H, [(x, by - 87, x + 5, by - 84) for x in range(cx - 212, cx + 212, 6)], 1.2)
    art = G(art, zig * fas, GRN, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.5)
    sil += [wall]
    # three-tier hip roof (tumpang)
    t1 = shapes(W, H, [[(cx - 252, by - 88), (cx + 252, by - 88), (cx + 170, by - 150), (cx - 170, by - 150)]], smooth=False)
    band = shapes(W, H, [rect(cx - 150, by - 164, cx + 150, by - 148)], smooth=False)
    t2 = shapes(W, H, [[(cx - 178, by - 160), (cx + 178, by - 160), (cx + 96, by - 214), (cx - 96, by - 214)]], smooth=False)
    band2 = shapes(W, H, [rect(cx - 80, by - 226, cx + 80, by - 212)], smooth=False)
    t3 = shapes(W, H, [[(cx - 104, by - 222), (cx + 104, by - 222), (cx + 8, by - 296), (cx - 8, by - 296)]], smooth=False)
    for b_ in (band, band2):
        art = GP(art, b_, YEL, YEL_D, seed=nx(), rough=0.6)
        art = GP(art, lin(W, H, [(x, 0, x, H) for x in range(cx - 150, cx + 152, 12)], 3) * b_, GRN, seed=nx(), rough=0.4)
    for t, k in ((t1, 0), (t2, 1), (t3, 2)):
        art = GP(art, t, ROOF, mix(ROOF, "#56664a", 0.4 + 0.2 * k), seed=nx(), rough=1.0, streak=1.0)
        # sirap courses + light on the right slope
        ys = [y for y in range(0, H, 7)]
        art = G(art, lin(W, H, [(0, y, W, y + 1) for y in ys], 1.1) * t, ROOF_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5)
        art = tint(art, t * np.clip((xx - cx) / 200, 0, 1), "#c9c08a", 0.22)
    # eave shadow under first tier
    art = G(art, shapes(W, H, [rect(cx - 212, by - 86, cx + 212, by - 74)], smooth=False), "#5a4416", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1)
    # ridge finial (mustaka) in gold
    fin = np.maximum(shapes(W, H, [deform(ellipse_pts(cx, by - 304, 7, 10, 10), rng, 1, 0.03)]), lin(W, H, [(cx, by - 326, cx, by - 296)], 3))
    art = FO(art, fin, GOLD, seed=nx(), emboss=0.6)
    sil += [t1, t2, t3, band, band2]
    # central porch with carved gable
    pw = 64
    pr = shapes(W, H, [[(cx - pw - 16, by - 70), (cx, by - 128), (cx + pw + 16, by - 70)]], smooth=False)
    tri = shapes(W, H, [[(cx - pw + 4, by - 74), (cx, by - 118), (cx + pw - 4, by - 74)]], smooth=False)
    art = GP(art, pr, ROOF, "#56664a", seed=nx(), rough=0.8)
    art = GP(art, tri, GRN, GRN_D, seed=nx(), rough=0.6)
    sun = []
    for k in range(9):
        a = math.pi + k * math.pi / 8
        sun.append(([(cx, by - 76), (cx + math.cos(a) * 34, by - 76 + math.sin(a) * 34)], 2.2, (0.0, 0.3)))
    art = FO(art, strokes(W, H, sun) * tri, GOLD, seed=nx(), emboss=0.5)
    art = FO(art, shapes(W, H, [ellipse_pts(cx, by - 78, 10, 8, 12)]) * tri, YEL_L, seed=nx())
    pp = shapes(W, H, [rect(cx + s * pw - 4, by - 74, cx + s * pw + 4, by - 8) for s in (-1, 1)], smooth=False)
    art = GP(art, pp, "#f3ead0", "#d8c8a0", seed=nx(), rough=0.5)
    door = shapes(W, H, [rect(cx - 22, by - 66, cx + 22, by - 8)], smooth=False)
    art = GP(art, door, "#3a2a14", "#2a1e10", seed=nx(), rough=0.5)
    art = FO(art, lin(W, H, [(cx - 22, by - 66, cx + 22, by - 66), (cx, by - 66, cx, by - 8)], 2), GOLD, seed=nx())
    sil += [pr]
    # stair to the jetty
    st = shapes(W, H, [[(cx - 30, by), (cx + 30, by), (cx + 46, by + 60), (cx - 46, by + 60)]], smooth=False)
    art = GP(art, st, "#8a6236", WOOD, seed=nx(), rough=0.8)
    art = G(art, lin(W, H, [(cx - 50, y, cx + 50, y) for y in range(by + 6, by + 60, 7)], 1.4) * st, WOOD_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.4)
    rail = lin(W, H, [(cx - 30, by - 8, cx - 48, by + 62), (cx + 30, by - 8, cx + 48, by + 62)], 3)
    art = GP(art, rail, YEL, YEL_D, seed=nx(), rough=0.5)
    sil += [st, pst, beam]
    return art, np.maximum.reduce(sil)


def umbul(art, W, H, nx, rng, x, by, h, side, col, col2):
    """Tall bamboo pole with a long curved umbul-umbul banner."""
    pole = strokes(W, H, [(curve([(x, by), (x + side * 4, by - h * 0.5), (x + side * 10, by - h)], 20), 3.0, (0.0, 0.2))])
    art = GP(art, pole, "#c9a85a", "#8a6a2a", seed=nx(), rough=0.5)
    top = (x + side * 10, by - h)
    pts = []
    for i in range(20):
        t = i / 19
        pts.append((top[0] + side * (6 + t * 26) + math.sin(t * 5) * 4, top[1] + 4 + t * h * 0.5))
    ban = strokes(W, H, [(pts, 13, (0.0, 0.85))])
    art = GP(art, ban, col, col2, seed=nx(), rough=0.8)
    stripe = strokes(W, H, [([(p[0] - side * 2, p[1]) for p in pts], 3, (0.0, 0.85))]) * ban
    art = GP(art, stripe, "#2f5e3c", seed=nx(), rough=0.4)
    return art


def tree(W, H, rng, cx, by, r):
    centers = [(cx + rng.uniform(-r, r) * 0.7, by - r - rng.uniform(0, r * 0.8), 1.0) for _ in range(5)]
    crown = blobs(W, H, centers, rng, r=(r * 0.35, r * 0.6), n=6)
    trunk = strokes(W, H, [([(cx, by), (cx + 2, by - r * 0.9)], max(3, r * 0.1), (0, 0.4))])
    return crown, trunk


if "keraton" in PARTS:
    W, H = 800, 860
    nx = Seq(4100); rng = random.Random(41)
    WL = 520  # waterline
    sky = painted_sky(W, H, [(0, "#f3e6c2"), (0.3, "#f7dc9a"), (0.52, "#f6c47a"), (0.6, "#f0a860"), (0.62, "#b9a774"), (1.0, "#4e6656")], seed=nx(), streak=0.5, grain=0.3)
    yy, xx = ygrid(W, H)
    art = sky.copy()
    # sun haze on the right
    SX, SY = 640, 170
    disc = np.clip((34 - np.hypot(xx - SX, yy - SY)) / 3, 0, 1)
    art = tint(art, np.exp(-((np.hypot(xx - SX, yy - SY) / 190) ** 2)).astype(np.float32), "#fff7dc", 0.75)
    art = G(art, disc, "#fff2c0", "#ffe89a", seed=nx(), density=0.9, edge=0.2, bloom=0.1, rough=2)
    # thin clouds
    cl = strokes(W, H, [([(x, y), (x + L * 0.5, y - 2), (x + L, y)], rng.uniform(3, 7), (0.3, 0.4)) for x, y, L in
                        [(rng.uniform(-40, W), rng.uniform(60, 280), rng.uniform(80, 220)) for _ in range(22)]])
    art = G(art, cl, "#f8efd8", "#e9d6a8", seed=nx(), density=0.55, edge=0.3, bloom=0.4, rough=4)
    # far bank: distant forest line
    far = hills(W, H, WL - 22, 14, 7, 0.4)
    far = far * (yy < WL + 2)
    art = G(art, far, "#8f9a6e", "#7a8a62", seed=nx(), density=0.75, edge=0.4, bloom=0.4, rough=5)
    clear()
    # trees behind the palace
    for (tx, r, col) in [(80, 46, "#4f6a3e"), (150, 38, "#5a7444"), (690, 52, "#47623a"), (760, 40, "#58714a"), (250, 34, "#4f6a3e"), (560, 36, "#56704a")]:
        crown, trunk = tree(W, H, rng, tx, WL - 50, r)
        art = G(art, trunk, "#4a3a28", seed=nx(), density=0.8, edge=0.3, rough=1)
        art = G(art, crown, col, "#3a5232", seed=nx(), density=0.85, edge=0.5, bloom=0.35, rough=3, gran=0.2)
    clear()
    for (px, h, ln) in [(40, 250, 0.05), (122, 210, -0.08), (718, 260, -0.06), (640, 200, 0.07)]:
        pm = _jw_lib.palm(W, H, px, WL - 6, h, rng, ln)
        art = G(art, pm, "#3f5a32", "#5a7642", seed=nx(), density=0.95, edge=0.45, bloom=0.2, rough=2)
    clear()
    # bank under the palace
    bank = shapes(W, H, [[(-10, WL - 20), (W + 10, WL - 26), (W + 10, WL + 6), (-10, WL + 6)]], smooth=False)
    art = G(art, bank, "#7a6a42", "#5f5434", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=3)
    pal = blank(W, H)
    pal, sil = keraton(pal, W, H, nx, rng, 400, WL - 74)
    edge = np.clip(sil - gaussian_filter(sil, 1.2) * 1.05, 0, 1) * 2
    pal = G(pal, np.clip(edge, 0, 1), "#2a2414", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.8, feather=0.5)
    pal = umbul(pal, W, H, nx, rng, 300, WL - 4, 230, -1, YEL, YEL_L)
    pal = umbul(pal, W, H, nx, rng, 500, WL - 4, 230, 1, YEL, YEL_L)
    pal = umbul(pal, W, H, nx, rng, 228, WL - 4, 170, -1, "#c43a2a", "#d8573a")
    pal = umbul(pal, W, H, nx, rng, 572, WL - 4, 170, 1, GRN_L, GRN)
    art = over(art, pal)
    clear()
    # jetty
    jet = shapes(W, H, [rect(310, WL - 16, 490, WL - 8)], smooth=False)
    art = GP(art, jet, "#8a6236", WOOD_D, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [rect(x - 2, WL - 10, x + 2, WL + 10) for x in range(316, 490, 28)], smooth=False), WOOD_D, seed=nx(), rough=0.5)
    # river: the Mahakam, olive brown-green with sky light
    river = (yy > WL).astype(np.float32)
    art = G(art, river * np.clip((yy - WL) / 260, 0, 1), "#46645a", "#3c5648", seed=nx(), density=0.55, edge=0.0, bloom=0.3, rough=2)
    # reflection
    src = art[max(0, 2 * WL - H):WL][::-1]
    ref = np.zeros_like(art)
    ref[WL:WL + src.shape[0]] = src
    ref[..., :3] = gaussian_filter(ref[..., :3], (4, 2.5, 0))
    nzx = (fbm(W, H, nx(), 8, 2) - 0.5) * 22
    from scipy.ndimage import map_coordinates
    for c in range(3):
        ref[..., c] = map_coordinates(ref[..., c], [yy, xx + nzx * np.clip((yy - WL) / 60, 0, 1)], order=1, mode="nearest")
    ref[..., :3] = ref[..., :3] * 0.72 + C("#5a6440") * 0.16
    fade = np.clip(1 - (yy - WL) / 240, 0, 1) * river * 0.5
    ref[..., 3] = fade
    art = over(art, ref)
    rip = sea_strokes(W, H, WL + 4, H, rng, n=320, length=(18, 120), width=(0.8, 2.6))
    art = G(art, rip * river, "#f6e0a0", "#fff0c0", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1, feather=0.6)
    rip2 = sea_strokes(W, H, WL + 10, H, rng, n=200, length=(30, 140), width=(1, 3))
    art = G(art, rip2 * river, "#3f4a2e", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1, feather=0.6)
    # glint path under the sun
    gl = rip * river * np.exp(-((xx - 640) / 70) ** 2)
    art = tint(art, gl, "#fff4c8", 0.9)
    clear()
    # foreground nipa fronds rising from the water at both corners
    for (bx, by_, dirs) in [(-10, H - 40, [-1.25, -0.95, -0.7, -0.45, -1.5]), (W + 10, H - 70, [-1.9, -2.2, -2.45, -1.65])]:
        items = []
        for a in dirs:
            L = rng.uniform(240, 330)
            pts = curve([(bx, by_), (bx + math.cos(a) * L * 0.55, by_ + math.sin(a) * L * 0.55), (bx + math.cos(a) * L, by_ + math.sin(a) * L + L * 0.22)], 30)
            items.append((pts, 5, (0.05, 0.4)))
            for j in range(2, 29, 2):
                px, py = pts[j]
                for sgn in (-1, 1):
                    qa = a + sgn * 0.9 + 0.35
                    ll = L * 0.3 * (1 - j / 36)
                    items.append(([(px, py), (px + math.cos(qa) * ll * 0.5, py + math.sin(qa) * ll * 0.5 + ll * 0.15), (px + math.cos(qa) * ll, py + math.sin(qa) * ll + ll * 0.5)], 7, (0.15, 0.7)))
        fm = strokes(W, H, items)
        art = G(art, fm, "#3d5a32", "#55753e", seed=nx(), density=0.92, edge=0.5, bloom=0.25, rough=1.5, gran=0.2)
    clear()
    # ragged painted bottom + sides edge
    vm = vignette_mask(W, H, seed=nx(), inset=4, rough=20, fade=26)
    yfade = np.clip((H - 30 - yy + (fbm(W, H, nx(), 50, 3) - 0.5) * 60) / 50, 0, 1)
    art[..., 3] *= np.clip(np.minimum(vm * 4, 1) * yfade, 0, 1)
    art = add_grain(art, 3, 0.015)
    preview(art, "keraton", tone="#f6e7b4")
    save(art, f"{OUT}/keraton.webp", max_w=780, quality=78)
    clear()

if "perahu" in PARTS:
    W, H = 560, 200
    nx = Seq(4300); rng = random.Random(43)
    art = blank(W, H)
    # long boat: low hull with upswept prow and stern
    top = curve([(30, 70), (70, 112), (280, 120), (490, 110), (536, 60)], 60)
    bot = curve([(538, 62), (500, 138), (280, 150), (80, 140), (28, 72)], 60)
    hull = shapes(W, H, [top + bot], smooth=False)
    art = GP(art, hull, GRN, GRN_D, seed=nx(), rough=1.2, streak=0.9)
    yy, xx = ygrid(W, H)
    band = hull * (np.abs(yy - (126 + (xx - 280) ** 2 / 9000)) < 6)
    art = GP(art, band, YEL, YEL_L, seed=nx(), rough=0.6)
    dots = circles(W, H, [(x, 126 + (x - 280) ** 2 / 9000, 2.2) for x in range(90, 480, 14)]) * hull
    art = GP(art, dots, "#c43a2a", seed=nx(), rough=0.3)
    gun = strokes(W, H, [(curve([(34, 72), (72, 112), (280, 119), (490, 109), (532, 62)], 60), 4, (0.05, 0.05))])
    art = GP(art, gun, YEL_D, YEL, seed=nx(), rough=0.5)
    # small curled carved ends
    for (x, y, d) in [(30, 70, -1), (536, 60, 1)]:
        cur = spiral_pts(x + d * 6, y - 8, 10, 2, math.pi / 2, 0.9, 20, d)
        art = FO(art, strokes(W, H, [(cur, 3.2, (0, 0.5))]), GOLD, seed=nx())
    # canopy (atap) mid-boat
    can = shapes(W, H, [[(200, 112), (360, 112), (350, 76), (210, 76)]], smooth=False)
    art = GP(art, can, "#b5762e", "#8a5520", seed=nx(), rough=1.0)
    art = G(art, lin(W, H, [(x, 76, x - 4, 112) for x in range(214, 352, 8)], 1.4) * can, "#6a3e18", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.5)
    rf = shapes(W, H, [[(190, 80), (370, 80), (350, 64), (210, 64)]], smooth=False)
    art = GP(art, rf, YEL, YEL_D, seed=nx(), rough=0.6)
    # paddles resting
    pad_ = strokes(W, H, [([(120, 92), (150, 150)], 3, None), ([(420, 92), (390, 150)], 3, None)])
    art = GP(art, pad_, WOOD, WOOD_D, seed=nx(), rough=0.5)
    # flags
    for (x, c) in [(70, YEL), (500, "#c43a2a")]:
        art = GP(art, lin(W, H, [(x, 104, x, 20)], 2.4), WOOD_D, seed=nx(), rough=0.3)
        fl = shapes(W, H, [[(x, 22), (x + 34, 30), (x, 42)]], smooth=False)
        art = GP(art, fl, c, mix(c, "#000000", 0.15), seed=nx(), rough=0.6)
    # waterline ripple
    rip = strokes(W, H, [([(x, 150 + rng.uniform(-2, 2)), (x + L, 150 + rng.uniform(-2, 2))], 2.2, (0.3, 0.3)) for x, L in [(rng.uniform(0, 500), rng.uniform(40, 120)) for _ in range(14)]])
    art = G(art, rip, "#5d6a44", "#f6e0a0", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    preview(art, "perahu", tone="#d9c58a")
    save(art, f"{OUT}/perahu.webp", max_w=300, quality=82)
    clear()


def vine(path, step, size, rng, width=1.0, side0=1):
    """Kutai sulur: a sinuous main stem with alternating spiral curls, kangkung leaves and small buds."""
    items = [(path, size * 0.16 * width, (0.04, 0.04))]
    leaves = []
    side = side0
    for (x, y, a) in along(path, step):
        n_ = a + side * math.pi / 2
        bx, by_ = x + math.cos(n_) * size * 0.55 + math.cos(a) * size * 0.35, y + math.sin(n_) * size * 0.55 + math.sin(a) * size * 0.35
        br = curve([(x, y), (x + math.cos(n_) * size * 0.35 + math.cos(a) * size * 0.05, y + math.sin(n_) * size * 0.35 + math.sin(a) * size * 0.05), (bx, by_)], 14)
        sp = spiral_pts(bx, by_, size * 0.42, size * 0.1, n_ + math.pi * (0.5 if side > 0 else -0.5) + math.pi, 1.0, 30, side)
        sp = [(px + (bx - sp[0][0]), py + (by_ - sp[0][1])) for px, py in sp]
        items += [(br, size * 0.12 * width, (0.0, 0.0)), (sp, size * 0.075 * width, (0.0, 0.7))]
        # tendril
        tn = n_ - side * 0.9
        items.append((curve([(x, y), (x + math.cos(tn) * size * 0.5, y + math.sin(tn) * size * 0.5), (x + math.cos(tn + side * 0.8) * size * 0.75, y + math.sin(tn + side * 0.8) * size * 0.75)], 14), size * 0.05 * width, (0.1, 0.6)))
        leaves.append(deform(petal_pts(x, y, size * 1.15, size * 0.26, a + side * 0.6 + math.pi, n=14, cup=0.25), rng, 1, 0.03))
        leaves.append(deform(petal_pts(bx, by_, size * 0.6, size * 0.22, n_ + side * 1.2, n=10), rng, 1, 0.03))
        side = -side
    return items, leaves


def relief_items(W, H, cx, cy, s, n, rng):
    """A frieze of lung scrolls along a horizontal line, alternately flipped."""
    items, leaves = [], []
    step = s * 1.9
    x0 = cx - (n - 1) / 2 * step
    for i in range(n):
        it, lv = lung(x0 + i * step, cy, s, 0.0 if i % 2 == 0 else math.pi, 1 if i % 2 == 0 else -1)
        items += it; leaves += lv
    return items, leaves


if "ukir" in PARTS:
    W, H = 1000, 150
    nx = Seq(4500); rng = random.Random(45)
    band = shapes(W, H, [rect(0, 18, W, 132)], smooth=False)
    path = [(x, 75 + 20 * math.sin(x / 140 * math.pi)) for x in range(-60, W + 61, 6)]
    items, leaves = vine(path, 70, 50, rng, 1.0)
    flowers = []
    for x in range(70, W, 140):
        y = 75 + 20 * math.sin(x / 140 * math.pi)
        for a in range(5):
            flowers.append(petal_pts(x, y, 13, 6, a * math.tau / 5, n=8))
    art = carve(W, H, band, items, leaves + flowers, nx, base=GRN, light=GRN_L, dark=GRN_D, gold=GOLD, gold_amt=0.85, seed=nx())
    mo = shapes(W, H, [rect(0, 6, W, 20), rect(0, 130, W, 144)], smooth=False)
    art = GP(art, mo, YEL, YEL_D, seed=nx(), rough=0.6)
    beads = circles(W, H, [(x, 13, 3) for x in range(6, W, 12)] + [(x, 137, 3) for x in range(12, W, 12)])
    art = FO(art, beads, GOLD, seed=nx())
    preview(art, "ukir", tone="#f6e7b4")
    save(art, f"{OUT}/ukir.webp", max_w=780, quality=80)
    clear()


def free_relief(W, H, items, leaves, nx, leafcol=(GRN_L, GRN), gold=GOLD):
    """Carved ornament without a panel: drop shadow, green leaves, gold-leaf scrolls."""
    st = strokes(W, H, items); lv = shapes(W, H, leaves)
    allm = np.maximum(st, lv)
    art = blank(W, H)
    art = over(art, soft_shadow(allm, "#3a2a10", blur=3, strength=0.35, dx=2, dy=3))
    art = GP(art, lv, leafcol[0], leafcol[1], seed=nx(), rough=1.0)
    vein = np.clip(lv - gaussian_filter(lv, 2.5) * 1.3, 0, 1)
    art = G(art, vein, GRN_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    art = FO(art, st, gold, seed=nx(), emboss=0.7, sparkle=0.15)
    return art


if "sudut" in PARTS:
    W, H = 380, 380
    nx = Seq(4700); rng = random.Random(47)
    path = curve([(40, 372), (34, 160), (60, 64), (160, 34), (372, 40)], 80)
    items, leaves = vine(path, 62, 46, rng, 1.1, side0=1)
    # a carved flower at the corner
    for k in range(6):
        leaves.append(petal_pts(64, 64, 26, 11, k * math.tau / 6 + 0.3, n=8))
    art = free_relief(W, H, items, leaves, nx)
    art = FO(art, circles(W, H, [(64, 64, 9)]), YEL, seed=nx())
    preview(art, "sudut", tone="#f6e7b4")
    save(art, f"{OUT}/sudut.webp", max_w=190, quality=82)
    clear()

if "kembang" in PARTS:
    W, H = 260, 260
    nx = Seq(4900); rng = random.Random(49)
    c = 130
    items, leaves = [], []
    for k in range(8):
        a = k * math.pi / 4
        leaves.append(deform(petal_pts(c + math.cos(a) * 18, c + math.sin(a) * 18, 78, 30, a, n=12, cup=0.1), rng, 1, 0.02))
    small = [petal_pts(c + math.cos(a) * 10, c + math.sin(a) * 10, 52, 20, a, n=10) for a in [k * math.pi / 4 + math.pi / 8 for k in range(8)]]
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        items.append((spiral_pts(c + math.cos(a) * 92, c + math.sin(a) * 92, 14, 3, a + math.pi, 0.9, 20, 1), 4, (0, 0.5)))
    lv = shapes(W, H, leaves); sm = shapes(W, H, small)
    art = blank(W, H)
    art = over(art, soft_shadow(np.maximum(lv, sm), "#3a2a10", blur=3, strength=0.35, dx=2, dy=3))
    art = GP(art, lv, GRN_L, GRN, seed=nx(), rough=1.0)
    art = G(art, np.clip(lv - gaussian_filter(lv, 3) * 1.25, 0, 1), GRN_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5)
    art = FO(art, sm, GOLD, seed=nx(), emboss=0.7)
    art = FO(art, strokes(W, H, items), GOLD, seed=nx(), emboss=0.6)
    art = GP(art, circles(W, H, [(c, c, 20)]), YEL, YEL_D, seed=nx(), rough=0.6)
    art = FO(art, np.clip(circles(W, H, [(c, c, 24)]) - circles(W, H, [(c, c, 19)]), 0, 1), GOLD, seed=nx())
    art = GP(art, circles(W, H, [(c, c, 7)]), "#c43a2a", seed=nx(), rough=0.3)
    preview(art, "kembang", tone="#f6e7b4")
    save(art, f"{OUT}/kembang.webp", max_w=130, quality=84)
    clear()
