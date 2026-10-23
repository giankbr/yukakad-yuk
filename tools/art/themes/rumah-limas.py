"""Rumah Limas — the tiered rumah limas of Palembang on stilts above the Musi at dusk, red-and-gold lacquered (lakuer)
carved panels, songket limar. Original, inspired-by drawings (no real bridge, no copied carving).
Run: python3 -I rumah-limas.py [part ...]  parts: limas lakuer panel songket divider simbar
Assets -> public/themes/art/rumah-limas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n1_lib import *

OUT = outdir("rumah-limas")
PARTS = sys.argv[1:] or ["limas", "lakuer", "panel", "songket", "divider", "simbar"]
RED, RED_D, RED_L = "#8e1c1c", "#561010", "#b23a2a"
BLACK = "#1c0f0c"
GOLD, GOLD_L, GOLD_D = "#d4a343", "#f0d488", "#8f6420"
TEAK, TEAK_D, TEAK_L = "#5a3220", "#2e170e", "#7f4a2c"
TILE = "#7a3b26"


def flower(cx, cy, r, n=8, rot0=0.0):
    """Bunga tanjung style rosette: n rounded petals + heart, as polys."""
    polys = [petal_pts(cx, cy, r, r * 0.46, rot0 + k * math.tau / n, n=10) for k in range(n)]
    return polys


def scroll_motif(W, H, x0, x1, cy, s, seed):
    """Carved band motif: rosettes joined by lung-lungan S-scrolls (stroke items, leaf polys, flower polys)."""
    items, leaves, fl = [], [], []
    step = s * 2.4
    k = 0
    x = x0
    while x < x1 + step:
        fl += flower(x, cy, s * 0.42, 8, k * 0.2)
        for flip in (1, -1):
            it, lv = lung(x + step * 0.5, cy + flip * s * 0.05, s * 0.62, 0.0 if flip > 0 else math.pi, flip)
            items += it; leaves += lv
        x += step; k += 1
    return items, leaves, fl


def gold_carving(art, W, H, items, leaves, fl, nx, ground_mask=None, seed=5, shadow=BLACK):
    relief_m = np.clip(np.maximum.reduce([strokes(W, H, items), shapes(W, H, leaves), shapes(W, H, fl)]), 0, 1)
    if ground_mask is not None:
        relief_m = relief_m * ground_mask
    sh = np.clip(np.roll(np.roll(dilate(relief_m, 0.8), 3, 0), 2, 1) - relief_m * 0.6, 0, 1)
    art = G(art, sh, shadow, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.8, feather=0.9)
    art = FO(art, relief_m, GOLD, seed=nx(), emboss=0.9, sparkle=0.2)
    # dark engraved line in the middle of petals / leaves (carving cut)
    return art, relief_m


def lacquer_ground(W, H, mask, nx, col=RED, col2=RED_D):
    art = GP(blank(W, H), mask, col, col2, seed=nx(), rough=1.2, streak=1.2, pad=8)
    # lacquer sheen: soft lighter streaks
    sheen = mask * np.clip(fbm(W, H, nx(), 60, 2) - 0.45, 0, 1) * 1.4
    art = OV(art, sheen, lambda q: flat(q, RED_L, 0.35))
    return art


# ---------------------------------------------------------------- scene
def house(art, W, H, cx, by, w, nx, rng):
    """Rumah limas, front elevation: stilts, a lower front terrace with railings and twin stairs (kekijing), the raised
    main hall with a wall of red-lacquered carved doors, a frieze of gilded carving, and the great hipped limas roof
    with simbar horns on its short ridge. Returns (art, silhouette mask)."""
    hw = w / 2
    fl_ter = by - w * 0.17
    fl_main = fl_ter - w * 0.045
    wall_top = fl_main - w * 0.27
    sil = np.zeros((H, W), np.float32)
    # stilts (tiang) under both floors
    posts = []
    for i in range(15):
        x = cx - hw * 0.96 + i * (w * 0.96 / 14)
        posts.append(([(x, fl_ter), (x + rng.uniform(-1, 1), by + 2)], w * 0.016, None))
    pm = strokes(W, H, posts)
    art = GP(art, pm, "#3a2116", BLACK, seed=nx(), rough=1, streak=0.8)
    art = G(art, pm * np.clip((np.arange(W)[None, :] - cx) / hw + 0.3, 0, 1), BLACK, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    under = shapes(W, H, [rect(cx - hw * 0.96, fl_ter, cx + hw * 0.96, fl_ter + w * 0.03)], smooth=False)
    art = G(art, under, BLACK, seed=nx(), density=0.55, edge=0.2, bloom=0.1, rough=1)
    sil = np.maximum(sil, pm)
    # main hall wall
    body = shapes(W, H, [rect(cx - hw * 0.82, wall_top, cx + hw * 0.82, fl_main)], smooth=False)
    art = GP(art, body, TEAK, TEAK_D, seed=nx(), rough=1.0, streak=1.4)
    planks = strokes(W, H, [([(cx - hw * 0.82 + i * w * 0.82 / 26, wall_top), (cx - hw * 0.82 + i * w * 0.82 / 26, fl_main)], 1.0, None) for i in range(1, 26)]) * body
    art = G(art, planks, TEAK_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.4)
    sil = np.maximum(sil, body)
    # carved lacquered doors
    nd = 7
    doors = []
    dw = w * 0.82 * 2 / 2 / nd
    for i in range(nd):
        x0 = cx - hw * 0.82 + w * 0.82 * 0.04 + i * (w * 0.82 * 0.92 / nd)
        doors.append(rect(x0 + w * 0.008, wall_top + w * 0.085, x0 + w * 0.82 * 0.92 / nd - w * 0.008, fl_main - w * 0.006))
    dm = shapes(W, H, doors, smooth=False)
    art = GP(art, dm, RED, RED_D, seed=nx(), rough=0.8, streak=1.0)
    parts = []
    frames = []
    for d in doors:
        (x0, y0), (x1, _), (_, y1), _ = d
        mx = (x1 + x0) / 2
        frames += [([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 1.6, None), ([(mx, y0 + 2), (mx, y1 - 2)], 1.0, None)]
        parts.append(dict(stem=[], leaves=[], curls=[], flowers=[(mx, y0 + (y1 - y0) * 0.26, (x1 - x0) * 0.3)]))
        pth = [(mx, y0 + (y1 - y0) * 0.5), (mx, y1 - 4)]
        parts.append(dict(stem=[], curls=[], flowers=[], leaves=[(petal_pts(mx, y0 + (y1 - y0) * (0.5 + 0.13 * j), (x1 - x0) * 0.32, (x1 - x0) * 0.1, math.pi if j % 2 else 0, n=8), [(mx, y0)]) for j in range(4)]))
    art = FO(art, strokes(W, H, frames), GOLD, seed=nx(), emboss=0.6, sparkle=0.25)
    art, _ = gild(art, W, H, merge(*parts), nx, scale=0.6)
    # warm lamplight through the doors' upper fanlights
    lamp = shapes(W, H, [rect(d[0][0] + 3, d[0][1] - w * 0.03, d[1][0] - 3, d[0][1] - w * 0.008) for d in doors], smooth=False)
    art = GP(art, lamp, "#f6c46a", "#e8a24a", seed=nx(), rough=0.5)
    art = over(art, glow(lamp, "#ffcf7a", 6, 0.35))
    # frieze under the eave: lacquer with gilded vine
    fr = shapes(W, H, [rect(cx - hw * 0.82, wall_top, cx + hw * 0.82, wall_top + w * 0.05)], smooth=False)
    art = GP(art, fr, RED_D, BLACK, seed=nx(), rough=0.6)
    fy = wall_top + w * 0.025
    pv = vine([(x, fy + 3 * math.sin(x / 12)) for x in np.arange(cx - hw * 0.8, cx + hw * 0.8, 3)], w * 0.03, rng, every=1.0, curl=False)
    art, _ = gild(art, W, H, pv, nx, ground=fr, scale=0.5)
    # eave shadow across the top of the wall
    esh = shapes(W, H, [rect(cx - hw * 0.82, wall_top, cx + hw * 0.82, wall_top + w * 0.11)], smooth=False) * np.clip(1 - (np.arange(H)[:, None] - wall_top) / (w * 0.11), 0, 1)
    art = G(art, esh, BLACK, seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1)
    # floors
    for (y0, y1, x0, x1) in [(fl_main - 2, fl_main + w * 0.014, cx - hw * 0.86, cx + hw * 0.86), (fl_ter - w * 0.012, fl_ter + w * 0.016, cx - hw * 0.98, cx + hw * 0.98)]:
        f = shapes(W, H, [rect(x0, y0, x1, y1)], smooth=False)
        art = GP(art, f, "#4a2a1a", BLACK, seed=nx(), rough=0.8)
        art = G(art, strokes(W, H, [([(x0, y0 + 1), (x1, y0 + 1)], 1.2, None)]), "#d08a52", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
        sil = np.maximum(sil, f)
    # terrace railings with gilded top rail, gap in the middle for the stairs
    rail = []
    rt = fl_ter - w * 0.06
    for (a, b) in [(cx - hw * 0.98, cx - hw * 0.16), (cx + hw * 0.16, cx + hw * 0.98)]:
        rail.append(([(a, rt), (b, rt)], 2.6, None))
        for x in np.arange(a, b + 0.1, w * 0.012):
            rail.append(([(x, rt), (x, fl_ter)], 1.3, None))
    rm = strokes(W, H, rail)
    art = GP(art, rm, "#6a3c24", TEAK_D, seed=nx(), rough=0.5)
    art = FO(art, strokes(W, H, [r for r in rail if r[1] > 2]), GOLD_D, seed=nx(), emboss=0.4, sparkle=0.1)
    sil = np.maximum(sil, rm)
    # twin stairs coming down left and right from the middle gap
    for d in (-1, 1):
        x_top = cx + d * hw * 0.16
        x_bot = cx + d * hw * 0.42
        st = shapes(W, H, [[(x_top, fl_ter), (x_top - d * w * 0.045, fl_ter), (x_bot - d * w * 0.045, by + 2), (x_bot, by + 2)]], smooth=False)
        art = GP(art, st, "#6a3c24", TEAK, seed=nx(), rough=0.8)
        steps = [([(x_top + (x_bot - x_top) * t, fl_ter + (by - fl_ter) * t), (x_top + (x_bot - x_top) * t - d * w * 0.045, fl_ter + (by - fl_ter) * t)], 1.4, None) for t in np.linspace(0.12, 0.95, 7)]
        art = G(art, strokes(W, H, steps), BLACK, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.4)
        sil = np.maximum(sil, st)
    # roof: lower overhang over the terrace, then the steep limas pyramid
    eave_y = wall_top + w * 0.012
    low = shapes(W, H, [[(cx - hw * 1.06, eave_y + w * 0.03), (cx + hw * 1.06, eave_y + w * 0.03), (cx + hw * 0.92, eave_y - w * 0.035), (cx - hw * 0.92, eave_y - w * 0.035)]], smooth=False)
    art = GP(art, low, "#5a2a1a", "#3a1a10", seed=nx(), rough=1.0, streak=1.4)
    art = G(art, strokes(W, H, [([(cx - hw * 1.06, eave_y + w * 0.03), (cx + hw * 1.06, eave_y + w * 0.03)], 2.4, None)]), "#c47a48", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    ridge_y = eave_y - w * 0.39
    base_y = eave_y - w * 0.035
    main = shapes(W, H, [[(cx - hw * 0.9, base_y), (cx + hw * 0.9, base_y), (cx + hw * 0.27, ridge_y), (cx - hw * 0.27, ridge_y)]], smooth=False)
    art = GP(art, main, TILE, "#4a2316", seed=nx(), rough=1.2, streak=1.6)
    rows = []
    for t in np.linspace(0.03, 0.98, 26):
        y = base_y + (ridge_y - base_y) * t
        half = hw * 0.9 + (hw * 0.27 - hw * 0.9) * t
        rows.append(([(cx - half, y), (cx + half, y)], 1.2, None))
    art = G(art, strokes(W, H, rows) * main, "#3a180e", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8, feather=0.5)
    # sunset light on the left slope, shade on the right
    xs = np.arange(W)[None, :].astype(np.float32)
    art = G(art, main * np.clip((cx - xs) / (hw * 0.8), 0, 1), "#e0955a", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=2)
    art = G(art, main * np.clip((xs - cx) / (hw * 0.8), 0, 1), "#2a120c", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
    hips = strokes(W, H, [([(cx - hw * 0.9, base_y), (cx - hw * 0.27, ridge_y)], 3, None), ([(cx + hw * 0.9, base_y), (cx + hw * 0.27, ridge_y)], 3, None)])
    art = G(art, hips, "#f0b070", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    sil = np.maximum.reduce([sil, main, low])
    # ridge with simbar: upturned horns at both ends and a row of small spikes between
    sim = [([(cx - hw * 0.29, ridge_y), (cx + hw * 0.29, ridge_y)], w * 0.014, None)]
    for d in (-1, 1):
        x = cx + d * hw * 0.29
        sim.append((curve([(x, ridge_y), (x + d * w * 0.02, ridge_y - w * 0.035), (x + d * w * 0.05, ridge_y - w * 0.07), (x + d * w * 0.075, ridge_y - w * 0.072)], 16), w * 0.013, (0.0, 0.7)))
    for i in range(7):
        x = cx - hw * 0.21 + i * hw * 0.07
        sim.append(([(x, ridge_y), (x, ridge_y - w * (0.03 if i % 2 else 0.045))], w * 0.006, (0.0, 0.6)))
    simm = strokes(W, H, sim)
    art = G(art, np.roll(simm, 2, 1), BLACK, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    art = FO(art, simm, GOLD, seed=nx(), emboss=0.7, sparkle=0.35)
    sil = np.maximum(sil, simm)
    return art, sil


def limas():
    W, H = 760, 700
    rng = random.Random(11); nx = Seq(1100)
    art = painted_sky(W, H, [(0, "#3b1f2c"), (0.16, "#6e3434"), (0.32, "#c86e3e"), (0.46, "#f0b466"), (0.535, "#f6d08c"),
                             (0.545, "#b47442"), (0.72, "#6a3b25"), (1, "#3a2016")], seed=9, streak=1.4)
    sun = circles(W, H, [(W * 0.2, H * 0.5, 26)])
    art = over(art, glow(sun, "#ffd890", 70, 0.7))
    art = OV(art, sun, lambda m: flat(np.clip(gaussian_filter(m, 1.2), 0, 1), "#ffe6b0", 0.95))
    for (cx, cy, rx) in [(W * 0.18, H * 0.12, 170), (W * 0.62, H * 0.08, 140), (W * 0.92, H * 0.26, 100), (W * 0.36, H * 0.33, 120), (W * 0.12, H * 0.4, 90)]:
        cl = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, rx * 0.08, 12), rng, 3, 0.15)])
        art = G(art, cl, "#eba26a", "#b45f45", seed=nx(), density=0.5, edge=0.35, bloom=0.4, rough=8)
    sky_y = H * 0.54
    # far bank across the Musi: low houses, a tiered tajug mosque roof, palms
    far = []
    x = -10
    while x < W * 0.5:
        bw = rng.uniform(16, 40); bh = rng.uniform(6, 18)
        far.append([(x, sky_y), (x, sky_y - bh), (x + bw * 0.5, sky_y - bh - rng.uniform(4, 10)), (x + bw, sky_y - bh), (x + bw, sky_y)])
        x += bw + rng.uniform(0, 8)
    tx = W * 0.36
    for wd, y0 in [(56, 0), (36, 13), (18, 24)]:
        far.append([(tx - wd / 2, sky_y - y0 - 12), (tx + wd / 2, sky_y - y0 - 12), (tx + wd * 0.18, sky_y - y0 - 26), (tx - wd * 0.18, sky_y - y0 - 26)])
    far.append(rect(tx - 24, sky_y - 14, tx + 24, sky_y))
    art = G(art, shapes(W, H, far, smooth=False), "#80504a", "#6a3c3a", seed=nx(), density=0.7, edge=0.3, bloom=0.2, rough=2)
    for px in [W * 0.04, W * 0.11, W * 0.27, W * 0.45]:
        art = G(art, palm(W, H, px, sky_y, rng.uniform(34, 52), rng, rng.uniform(-0.15, 0.15)), "#6e4040", seed=nx(), density=0.7, edge=0.3, bloom=0, rough=1.5)
    # the river: broad golden-brown water with banded reflections and the sun's glitter path
    for k, y in enumerate(np.linspace(H * 0.55, H * 0.99, 18)):
        band = strokes(W, H, [([(x, y + math.sin(x / 60 + k) * 2) for x in np.arange(-20, W + 20, 20)], rng.uniform(2, 6), (0.1, 0.1))])
        art = G(art, band * fbm(W, H, 60 + k, 40, 2) * 1.6, "#3e2318" if k % 2 else "#c88c50", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=4)
    gl = strokes(W, H, [([(W * 0.2 + rng.gauss(0, 14 + (y - H * 0.54) * 0.25), y), (W * 0.2 + rng.gauss(0, 14) + rng.uniform(12, 44), y)], 2.2, (0.3, 0.3)) for y in np.linspace(H * 0.55, H * 0.97, 34)])
    art = OV(art, gl, lambda m: flat(m, "#ffd99a", 0.7))
    # near bank (right), the house on stilts, trees beside it
    hx, hby, hw_ = W * 0.62, H * 0.71, W * 0.56
    bank_top = [(W * 0.22, hby + 16)] + [(x, hby + 2 + rng.uniform(-2, 2) - 4 * math.sin((x - W * 0.22) / (W * 0.8) * math.pi)) for x in np.arange(W * 0.26, W + 30, 24)]
    bank = shapes(W, H, [bank_top + [(W + 30, hby + 44), (W * 0.3, hby + 40)]])
    hl = blank(W, H)
    # a banana clump and a mango tree behind the house (dark silhouettes against the dusk)
    for (px, ph, ln) in [(W * 0.95, 200, -0.12), (W * 0.99, 160, 0.1), (W * 0.27, 120, -0.2)]:
        pm_ = palm(W, H, px, hby + 8, ph, rng, ln)
        hl = G(hl, pm_, "#3a2018", "#24140e", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=1.5)
    hl, sil = house(hl, W, H, hx, hby, hw_, nx, rng)
    hl = GP(hl, bank, "#3b2418", "#24150e", seed=nx(), rough=3, streak=1)
    grass = strokes(W, H, [([(x, hby + 6 + rng.uniform(-2, 4)), (x + rng.uniform(-4, 4), hby - rng.uniform(4, 12))], 1.6, (0.1, 0.7)) for x in np.arange(W * 0.25, W, 5)])
    hl = G(hl, grass, "#5a4a2a", "#3a2e1a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5)
    # reflection of everything on the near bank, broken by ripples
    from scipy.ndimage import map_coordinates
    ry = hby + 30
    yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
    src_y = 2 * ry - yy2
    wob = (fbm(W, H, 77, 10, 2) - 0.5) * 10
    refl = np.stack([map_coordinates(hl[..., c], [src_y, xx2 + wob], order=1, mode="constant") for c in range(4)], -1)
    refl[yy2 < ry] = 0
    refl[..., 3] *= np.clip(1 - (yy2 - ry) / (H * 0.32), 0, 1) * 0.5
    refl[..., :3] = refl[..., :3] * 0.55 + col3("#4a2a1a") * 0.45
    art = over(art, refl)
    art = over(art, hl)
    # a covered perahu kajang moored on the left, sitting on the water
    bx, by_, L = W * 0.2, H * 0.88, 250
    hull = shapes(W, H, [curve([(bx - L / 2, by_ - L * 0.07), (bx - L * 0.3, by_ + L * 0.03), (bx + L * 0.3, by_ + L * 0.03), (bx + L / 2, by_ - L * 0.09),
                               (bx + L * 0.44, by_ - L * 0.04), (bx - L * 0.44, by_ - L * 0.03)], 50)])
    kaj = shapes(W, H, [arc_pts(bx - L * 0.04, by_ - L * 0.03, L * 0.22, math.pi, math.tau, 24, 0.55) + [(bx + L * 0.18, by_ - L * 0.03), (bx - L * 0.26, by_ - L * 0.03)]])
    art = GP(art, kaj, "#7a5530", "#4e3420", seed=nx(), rough=1.2, streak=1.4)
    art = G(art, strokes(W, H, [([(bx - L * 0.26 + i * L * 0.04, by_ - L * 0.03), (bx - L * 0.24 + i * L * 0.04, by_ - L * 0.13 - 6 * math.sin(i / 11 * math.pi))], 1.2, None) for i in range(12)]) * kaj, "#3a2414", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    art = GP(art, hull, "#2a1810", "#140b07", seed=nx(), rough=1)
    art = G(art, strokes(W, H, [([(bx - L * 0.46, by_ - L * 0.05), (bx + L * 0.45, by_ - L * 0.065)], 2.2, None)]) * dilate(hull, 1), RED_L, seed=nx(), density=0.85, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    art = G(art, strokes(W, H, [([(bx - L * 0.4, by_ - L * 0.02), (bx + L * 0.4, by_ - L * 0.03)], 1.4, None)]) * dilate(hull, 1), GOLD, seed=nx(), density=0.8, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    rip = strokes(W, H, [([(bx - L * 0.6 + k * 14 + rng.uniform(-3, 3), by_ + 8 + (k % 3) * 4), (bx - L * 0.6 + k * 14 + 10, by_ + 8 + (k % 3) * 4)], 1.6, (0.3, 0.3)) for k in range(int(L * 1.2 / 14))])
    art = OV(art, rip, lambda m: flat(m, "#e8ac68", 0.6))
    art = add_grain(art, 7, 0.03)
    preview(art, "rl-limas")
    save_rgb(art, f"{OUT}/limas.webp", size=(720, int(720 * H / W)), quality=78)


# ---------------------------------------------------------------- lacquer pieces
def shift_parts(p, dx, dy=0):
    sh = lambda pts: [(x + dx, y + dy) for x, y in pts]
    return dict(stem=[(sh(a),) + tuple(b) for a, *b in p["stem"]], curls=[(sh(a),) + tuple(b) for a, *b in p["curls"]],
                leaves=[(sh(a), sh(v)) for a, v in p["leaves"]], flowers=[(x + dx, y + dy, r) for x, y, r in p["flowers"]])


def lakuer():
    """Seamless (repeat-x) carved lacquer band: red lacquer ground, black borders with gold fillets, a dense gilded
    leafy vine waving between lotus rosettes."""
    W, H = 400, 104
    nx = Seq(2100); rng = random.Random(8)
    band = np.ones((H, W), np.float32)
    art = lacquer_ground(W, H, band, nx)
    edges = shapes(W, H, [rect(-5, 0, W + 5, 12), rect(-5, H - 12, W + 5, H)], smooth=False)
    art = GP(art, edges, BLACK, "#2a1410", seed=nx(), rough=0.4)
    gl = strokes(W, H, [([(-5, 14), (W + 5, 14)], 2.4, None), ([(-5, H - 14), (W + 5, H - 14)], 2.4, None)])
    art = FO(art, gl, GOLD, seed=nx(), emboss=0.4, sparkle=0.2)
    # dentil row in the black borders
    den = shapes(W, H, [rect(x, 3, x + 6, 9) for x in range(0, W, 12)] + [rect(x + 6, H - 9, x + 12, H - 3) for x in range(0, W, 12)], smooth=False)
    art = FO(art, den, GOLD_D, seed=nx(), emboss=0.3, sparkle=0.05)
    cy = H / 2
    P = W / 2
    path = [(x, cy + 14 * math.sin((x - 50) / P * math.tau)) for x in np.arange(0, W + 1, 4)]
    p = vine(path, 26, rng, every=1.0, curl=True)
    p["flowers"] = [(50 + k * P, cy, 21) for k in range(2)]
    # drop leaves that collide with the rosettes
    p["leaves"] = [(a, v) for a, v in p["leaves"] if min(abs(v[0][0] - 50 - k * P) for k in range(-1, 3)) > 18]
    allp = merge(p, shift_parts(p, -W), shift_parts(p, W))
    inner = shapes(W, H, [rect(-5, 17, W + 5, H - 17)], smooth=False)
    art, _ = gild(art, W, H, allp, nx, ground=inner, glaze_col=RED_D)
    art = add_grain(art, 3, 0.03)
    preview(art, "rl-lakuer")
    save_rgb(art, f"{OUT}/lakuer.webp", quality=82)


def panel():
    """A square lacquered carved panel: red field, black-and-gold frame, a gilded lotus in the middle and dense leafy
    scrolls springing from it into the corners."""
    W = H = 320
    nx = Seq(3100); rng = random.Random(4)
    full = shapes(W, H, [rect(6, 6, W - 6, H - 6)], smooth=False)
    art = GP(blank(W, H), full, BLACK, "#2a1410", seed=nx(), rough=0.8)
    field = shapes(W, H, [rect(26, 26, W - 26, H - 26)], smooth=False)
    art = over(art, lacquer_ground(W, H, field, nx))
    fr = strokes(W, H, [(rect(16, 16, W - 16, H - 16) + [(16, 16)], 3.0, None), (rect(30, 30, W - 30, H - 30) + [(30, 30)], 1.8, None)])
    art = FO(art, fr, GOLD, seed=nx(), emboss=0.5, sparkle=0.2)
    cx = cy = W / 2
    parts = []
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        for flip in (1, -1):
            aa = a + flip * 0.32
            pth = curve([(cx + math.cos(a) * 40, cy + math.sin(a) * 40), (cx + math.cos(aa) * 80, cy + math.sin(aa) * 80),
                         (cx + math.cos(a + flip * 0.05) * 112, cy + math.sin(a + flip * 0.05) * 112)], 30)
            parts.append(vine(pth, 22, rng, every=1.1, curl=True))
        parts.append(dict(stem=[], leaves=[], curls=[], flowers=[(cx + math.cos(a) * 118, cy + math.sin(a) * 118, 13)]))
    for k in range(4):
        a = k * math.pi / 2
        parts.append(dict(stem=[], curls=[], flowers=[], leaves=[(petal_pts(cx + math.cos(a) * 48, cy + math.sin(a) * 48, 62, 18, a, n=12), [(cx + math.cos(a) * (52 + t * 50), cy + math.sin(a) * (52 + t * 50)) for t in (0.1, 0.5, 0.9)])]))
    parts.append(dict(stem=[], leaves=[], curls=[], flowers=[(cx, cy, 50)]))
    art, rm = gild(art, W, H, merge(*parts), nx, ground=erode(field, 3), glaze_col=RED_D, scale=1.2)
    o, i = lotus_polys(cx, cy, 30, 8, 0.4)
    art = FO(art, shapes(W, H, i), GOLD_L, seed=nx(), emboss=0.9)
    art = G(art, edge_ring(shapes(W, H, i), 1.0), "#2a120c", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = GP(art, circles(W, H, [(cx, cy, 10)]), RED_D, seed=nx(), rough=0.3)
    art = FO(art, circles(W, H, [(cx + math.cos(k) * 5, cy + math.sin(k) * 5, 1.6) for k in range(6)]), GOLD_L, seed=nx())
    art = add_grain(art, 5, 0.03)
    preview(art, "rl-panel", bg="#2a1410")
    save(art, f"{OUT}/panel.webp", max_w=280, quality=82)


def songket():
    """Seamless songket limar tile: deep red silk with limar (weft-ikat) blush streaks and a gold supplementary-weft
    lattice of eight-point stars (bintang) inside diamond trellises."""
    W = H = 240
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    limar = wrap_noise(W, H, 3, (12, 2.5))
    k = np.clip(limar - 0.55, 0, 1)[..., None] * 2.4
    base = col3("#7c1717") * (1 - k) + col3("#b0402e") * k
    weft = 0.94 + 0.06 * np.sin(yy * math.pi / 1.5)
    base = base * weft[..., None] * (0.92 + 0.12 * wrap_noise(W, H, 5, 20)[..., None])
    P = 80
    polys, items = [], []
    for i in range(-1, W // P + 2):
        for j in range(-1, 2 * H // P + 2):
            cx, cy = i * P + (P / 2 if j % 2 else 0), j * P / 2
            star = []
            for q in range(16):
                r = 12 if q % 2 == 0 else 5
                a = q * math.tau / 16
                star.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
            polys.append(star)
            d = 26
            items.append(([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy), (cx, cy - d)], 1.8, None))
            items.append(([(cx - 2, cy - d - 8), (cx + 2, cy - d - 8)], 3, None))
    motif = np.maximum(shapes(W, H, polys, smooth=False), strokes(W, H, items) * 0.95)
    floats = (np.sin(yy * math.pi / 1.6) > -0.3).astype(np.float32)
    g = foil(motif * floats, GOLD, seed=7, emboss=0.4, sparkle=0.3)
    rgb = base * (1 - g[..., 3:4]) + g[..., :3] * g[..., 3:4]
    art = rgba(rgb, np.ones((H, W), np.float32))
    preview(art, "rl-songket")
    save_rgb(art, f"{OUT}/songket.webp", quality=78)


def divider():
    W, H = 420, 70
    nx = Seq(5100); rng = random.Random(2)
    art = blank(W, H)
    cx, cy = W / 2, H / 2
    parts = []
    for d in (-1, 1):
        pth = [(cx + d * x, cy + 7 * math.sin(x / 34) * d) for x in np.arange(26, 196, 3)]
        parts.append(vine(pth, 18, rng, every=1.15, curl=True))
        parts.append(dict(stem=[], leaves=[], curls=[], flowers=[(cx + d * 198, cy, 7)]))
    parts.append(dict(stem=[], leaves=[], curls=[], flowers=[(cx, cy, 22)]))
    art, rm = gild(art, W, H, merge(*parts), nx, shadow="#2a100a")
    preview(art, "rl-divider", bg=RED)
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)


def simbar():
    """Simbar roof crest: gilded upturned horns and a spike around a lotus (used for nodes / ampersand)."""
    W = H = 180
    nx = Seq(6100); rng = random.Random(6)
    art = blank(W, H)
    cx, cy = W / 2, H * 0.64
    parts = []
    for d in (-1, 1):
        parts.append(dict(stem=[(curve([(cx + d * 12, cy), (cx + d * 34, cy - 20), (cx + d * 50, cy - 56), (cx + d * 72, cy - 66)], 24), 10, (0.0, 0.75))],
                          leaves=[(petal_pts(cx + d * 14, cy + 6, 50, 16, math.pi / 2 - d * 1.35, n=12, cup=0.2 * d), [(cx + d * (16 + t * 44), cy + 6 + t * 10) for t in (0.1, 0.5, 0.9)])],
                          curls=[(spiral_pts(cx + d * 70, cy - 58, 8, 1.5, math.pi, 0.9, 16, d), 5, (0.0, 0.6))], flowers=[]))
    parts.append(dict(stem=[(curve([(cx, cy - 6), (cx + 2, cy - 44), (cx, cy - 78)], 12), 9, (0.0, 0.85))], leaves=[], curls=[], flowers=[(cx, cy, 24)]))
    art, _ = gild(art, W, H, merge(*parts), nx, shadow="#2a100a", scale=1.1)
    preview(art, "rl-simbar", bg=RED)
    save(art, f"{OUT}/simbar.webp", max_w=130, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
