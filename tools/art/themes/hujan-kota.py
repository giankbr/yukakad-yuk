"""Hujan Kota — a rainy city night painted in gouache + watercolour glazes: a row of old shop-houses with warm lit
windows, glowing blank shop signs (no lettering, no brands), a street lamp, a couple seen from behind under two
umbrellas, and the wet street mirroring every light. Plus: raindrops-on-glass overlay tile, the umbrella pair alone,
a rooftop strip with reflections, a puddle-ripple divider and a lit-window node.
Run: python3 -I hujan-kota.py [part ...]   parts: street drops pair roofs ripple node
Assets -> public/themes/art/hujan-kota/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k5_lib import *  # noqa

OUT = outdir("hujan-kota")
PARTS = sys.argv[1:] or ["street", "drops", "rain", "pair", "roofs", "ripple", "node"]
NIGHT, NIGHT2, HAZE = "#141b27", "#202c3c", "#4c4550"
WALL = ["#2c3a46", "#3a3340", "#2e4142", "#3b3a3a", "#31384a"]
AMBER, AMBER_L, AMBER_D = "#f0b765", "#ffd9a0", "#c97f3c"
SIGN = ["#e26a4f", "#5fb2a8", "#e9a64a", "#c95a6d"]
TERRA, MUSTARD, COAT = "#b9533c", "#c99a3e", "#1c2029"
nx = Seq(500)


def lit(art, mask, col, radius=14, strength=0.6):
    return over(art, glow(mask, col, radius, strength))


def building_row(W, H, base_y, rng, x0=-20, x1=None, scale=1.0, lit_p=0.55, signs=True):
    """Shop-house façades along base_y. Returns dict of masks."""
    x1 = x1 if x1 is not None else W + 20
    walls, winL, winD, awn, shop, sgn, sgn_col, trims = [], [], [], [], [], [], [], []
    x = x0
    k = 0
    while x < x1:
        bw = rng.uniform(130, 210) * scale
        top = base_y - rng.uniform(250, 420) * scale
        walls.append((k % len(WALL), [(x, base_y), (x, top + 10), (x + 6, top), (x + bw - 6, top), (x + bw, top + 10), (x + bw, base_y)]))
        trims.append((x - 4, top - 8 * scale, bw + 8, 10 * scale))
        # upper floors: window grid
        rows = int((base_y - 120 * scale - top) // (72 * scale))
        cols = max(2, int(bw // (52 * scale)))
        ww = bw / cols * 0.52
        for r in range(rows):
            for c in range(cols):
                wx = x + bw / cols * (c + 0.24)
                wy = top + 30 * scale + r * 72 * scale
                (winL if rng.random() < lit_p else winD).append((wx, wy, ww, 44 * scale))
        # ground floor: awning + lit shop
        ay = base_y - 104 * scale
        awn.append([(x + 4, ay), (x + bw - 4, ay), (x + bw + 8, ay + 26 * scale), (x - 8, ay + 26 * scale)])
        shop.append((x + 12, ay + 30 * scale, bw - 24, base_y - ay - 36 * scale))
        if signs and rng.random() < 0.8:
            if rng.random() < 0.5:   # blade sign
                sx = x + (bw - 18 if rng.random() < 0.5 else 4)
                sgn.append((sx, top + 60 * scale, 20 * scale, rng.uniform(90, 150) * scale))
            else:                     # board over the awning
                sgn.append((x + bw * 0.18, ay - 34 * scale, bw * 0.64, 24 * scale))
            sgn_col.append(SIGN[k % len(SIGN)])
        x += bw + rng.uniform(-2, 6)
        k += 1
    return dict(walls=walls, winL=winL, winD=winD, awn=awn, shop=shop, sgn=sgn, sgn_col=sgn_col, trims=trims)


def paint_row(art, W, H, row, haze=0.0):
    for ci, pts in row["walls"]:
        m = polys(W, H, [pts], smooth=False)
        art = GP(art, m, WALL[ci], mix(WALL[ci], "#000000", 0.25), seed=nx(), rough=1.6, streak=0.7)
    art = GP(art, rects(W, H, row["trims"]), "#46505c", "#2c333d", seed=nx(), rough=1.2, streak=0.4)
    md = rects(W, H, row["winD"], 3)
    art = GP(art, md, "#1d2430", "#283140", seed=nx(), rough=1.0, streak=0.3)
    ml = rects(W, H, row["winL"], 3)
    art = lit(art, ml, AMBER, 16, 0.35)
    art = GP(art, ml, AMBER, AMBER_D, seed=nx(), rough=1.0, streak=0.5)
    art = G(art, ml * fbm(W, H, nx(), 30, 2), AMBER_L, seed=nx(), density=0.6, edge=0.1, bloom=0.2, rough=1, feather=1)
    # window mullions
    mull = []
    for x, y, w, h in row["winL"] + row["winD"]:
        mull += [[(x + w / 2, y), (x + w / 2, y + h)], [(x, y + h * 0.42), (x + w, y + h * 0.42)]]
    art = over(art, tint(lines_mask(W, H, mull, 1.6), "#1a1e26", 0.85))
    ms = rects(W, H, row["shop"], 2)
    art = lit(art, ms, AMBER, 26, 0.5)
    art = GP(art, ms, "#f6c77e", "#e39a4c", seed=nx(), rough=1.2, streak=0.6)
    art = G(art, ms * fbm(W, H, nx(), 18, 3), "#8a5a35", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=1.5, feather=1.2)
    # shop interiors: shelves, a door, hanging lamps, window frames
    det, doors, lamps = [], [], []
    for x, y, w, h in row["shop"]:
        n = max(2, int(w // 46))
        for i in range(1, n):
            det.append([(x + w * i / n, y), (x + w * i / n, y + h)])
        det.append([(x, y + h * 0.18), (x + w, y + h * 0.18)])
        for j in (0.55, 0.78):
            det.append([(x + 4, y + h * j), (x + w * 0.45, y + h * j)])
        doors.append((x + w * 0.62, y + h * 0.3, w * 0.22, h * 0.7))
        lamps += [(x + w * 0.25, y + h * 0.3, 3.2), (x + w * 0.75, y + h * 0.3, 3.2)]
    art = G(art, rects(W, H, doors), "#6b3f2a", "#4a2c22", seed=nx(), density=0.75, edge=0.3, bloom=0.2, rough=1, feather=0.8)
    art = over(art, tint(lines_mask(W, H, det, 2.0), "#5b3a26", 0.65))
    ml2 = circles(W, H, lamps)
    art = lit(art, ml2, "#fff1d2", 8, 0.8)
    art = over(art, tint(ml2, "#fffaf0", 1))
    for i, pts in enumerate(row["awn"]):
        c = ["#7d3a2f", "#2f5a56", "#7a5a2a", "#5a3550", "#33475e"][i % 5]
        m = polys(W, H, [pts], smooth=False)
        art = GP(art, m, c, mix(c, "#1a1a1a", 0.3), seed=nx(), rough=1.4, streak=0.8)
        x0, y0 = pts[0]; x1 = pts[1][0]
        stripes = [[(x0 + k, y0), (x0 + k - 6, y0 + 26)] for k in np.arange(8, x1 - x0, 16)]
        art = over(art, tint(lines_mask(W, H, stripes, 6) * m, mix(c, "#f3e2c4", 0.45), 0.55))
        hem = rects(W, H, [(pts[3][0], pts[3][1] - 4, pts[2][0] - pts[3][0], 5)])
        art = over(art, tint(hem, "#ffd59a", 0.55))
    for r, c in zip(row["sgn"], row["sgn_col"]):
        m = rects(W, H, [r], 4)
        art = lit(art, m, c, 22, 0.55)
        art = GP(art, m, mix(c, "#ffffff", 0.35), c, seed=nx(), rough=1.0, streak=0.4)
        # faint ruled marks instead of lettering
        x, y, w, h = r
        if w > h:
            marks = [[(x + w * (0.15 + 0.14 * i), y + h * 0.5), (x + w * (0.22 + 0.14 * i), y + h * 0.5)] for i in range(5)]
        else:
            marks = [[(x + w * 0.5, y + h * (0.12 + 0.16 * i)), (x + w * 0.5, y + h * (0.2 + 0.16 * i))] for i in range(5)]
        art = over(art, tint(lines_mask(W, H, marks, 2.4), mix(c, "#3a1d1d", 0.5), 0.45))
    if haze:
        hz = np.ones((H, W), np.float32) * haze
        art = over(art, col_arr(hz, HAZE, hz * (art[..., 3] > 0)))
    return art


def figure_pair(W, H, cx, foot, s, rng):
    """Two people from behind under umbrellas. Returns (body_mask, umbrella list)."""
    parts = []
    umbs = []
    for i, (dx, hgt, col) in enumerate(((-30, 1.0, TERRA), (30, 0.94, MUSTARD))):
        x = cx + dx * s
        top = foot - 160 * s * hgt
        sh = top + 26 * s
        # long coat: shoulders, a slight waist, flared hem
        coat = [(x - 15 * s, sh - 4 * s), (x + 15 * s, sh - 4 * s), (x + 21 * s, sh + 8 * s), (x + 19 * s, sh + 50 * s),
                (x + 23 * s, foot - 46 * s), (x - 23 * s, foot - 46 * s), (x - 19 * s, sh + 50 * s), (x - 21 * s, sh + 8 * s)]
        parts.append(("coat", coat))
        parts.append(("head", ellipse_pts(x, top + 12 * s, 10 * s, 12 * s, n=16)))
        parts.append(("neck", [(x - 5 * s, top + 18 * s), (x + 5 * s, top + 18 * s), (x + 6 * s, sh), (x - 6 * s, sh)]))
        for lx in (-8, 8):
            parts.append(("leg", [(x + (lx - 6) * s, foot - 50 * s), (x + (lx + 6) * s, foot - 50 * s), (x + (lx + 5) * s, foot - 6 * s), (x + (lx - 4) * s, foot - 6 * s)]))
            parts.append(("shoe", ellipse_pts(x + (lx + 2) * s, foot - 3 * s, 7 * s, 3.6 * s, n=12)))
        # the arm raised to the handle, on the inside
        side = 1 if i == 0 else -1
        parts.append(("arm", [(x + side * 12 * s, sh + 2 * s), (x + side * 19 * s, sh + 4 * s), (x + side * 20 * s, sh + 34 * s), (x + side * 13 * s, sh + 34 * s)]))
        tilt = 0.16 * side
        ux, uy, R = x + side * 16 * s, top - 14 * s, 74 * s
        f = rot_frame(tilt, ux, uy)
        pts = []
        for t in np.linspace(math.pi, 2 * math.pi, 26):
            pts.append(f(math.cos(t) * R, math.sin(t) * R * 0.6))
        for j in range(8, -1, -1):
            u = -R + 2 * R * j / 8
            pts.append(f(u, (5 * s if j % 2 else 0)))
        umbs.append((pts, col, f, R))
    mb = polys(W, H, [p for _, p in parts if _ not in ("shoe",)])
    mb = np.maximum(mb, polys(W, H, [p for _, p in parts if _ == "shoe"]))
    return mb, umbs


def street():
    W, H = 780, 1180
    hy = 720
    rng = np.random.default_rng(7)
    art = painted_sky(W, H, [(0, "#10161f"), (0.25, "#18212e"), (0.5, "#2a3140"), (0.6, "#4a4049"), (1, "#1a1f28")], seed=nx(), streak=0.9)
    # far towers in haze
    far = []
    x = -10
    while x < W:
        bw = rng.uniform(50, 110)
        far.append([(x, hy - 200), (x, hy - rng.uniform(330, 520)), (x + bw, hy - rng.uniform(330, 520)), (x + bw, hy - 200)])
        x += bw + rng.uniform(4, 30)
    mf = polys(W, H, far, smooth=False)
    yy0 = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = GP(art, mf, "#262e3d", "#303747", seed=nx(), rough=1.8, streak=0.6)
    art = G(art, mf * fbm(W, H, nx(), 50, 3), "#3e4556", "#2a3142", seed=nx(), density=0.55, edge=0.15, bloom=0.5, gran=0.5, rough=2, feather=2)
    fw = [(rng.uniform(0, W), rng.uniform(hy - 500, hy - 230), 7, 9) for _ in range(90)]
    fwm = rects(W, H, fw) * mf
    art = lit(art, fwm, AMBER, 6, 0.25)
    art = over(art, tint(fwm, "#d8a868", 0.7))
    art = over(art, col_arr(mf, "#5a5260", mf * np.clip((yy0 - (hy - 520)) / 420, 0, 1) * 0.42))
    # haze band
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    band = np.exp(-((yy - (hy - 230)) / 120) ** 2) * (0.4 + 0.3 * fbm(W, H, nx(), 140, 3))
    art = over(art, col_arr(band, "#6b5a5a", band * 0.45))
    # shop-house row
    row = building_row(W, H, hy, rng, scale=1.0)
    art = paint_row(art, W, H, row)
    # sidewalk + curb
    art = GP(art, rects(W, H, [(-10, hy - 4, W + 20, 22)]), "#3b3f48", "#2c3038", seed=nx(), rough=1.2, streak=0.6)
    art = over(art, tint(rects(W, H, [(-10, hy + 16, W + 20, 5)]), "#8a8f98", 0.5))
    # street lamp (left)
    lx = 96
    pole = lines_mask(W, H, [[(lx, hy + 120), (lx, 420), (lx + 4, 396), (lx + 40, 384)]], 7)
    head = shapes(W, H, [[(lx + 26, 380), (lx + 62, 380), (lx + 56, 396), (lx + 32, 396)]], smooth=False)
    bulb = disc(W, H, lx + 44, 402, 9)
    art = lit(art, bulb, "#ffd79a", 60, 0.55)
    art = lit(art, bulb, "#ffe7bf", 18, 0.9)
    art = GP(art, np.maximum(pole, head), "#1b1f27", "#2a2f38", seed=nx(), rough=1.0, streak=0.3)
    art = over(art, tint(bulb, "#fff2d8", 1.0))
    # light cone from the lamp (warm, soft, with rain visible inside)
    cone = shapes(W, H, [[(lx + 34, 400), (lx + 54, 400), (lx + 170, hy + 140), (lx - 90, hy + 140)]], smooth=False)
    cone = gaussian_filter(cone, 16) * np.clip(1 - (yy - 400) / 520, 0, 1)
    art = over(art, col_arr(cone, "#ffd08a", cone * 0.22))
    # wet street
    road = rects(W, H, [(-10, hy + 21, W + 20, H - hy)])
    art = over(art, col_arr(road, "#151a22", road))
    art = G(art, road * fbm(W, H, nx(), 60, 3), "#2b3240", "#1d232d", seed=nx(), density=0.6, edge=0.1, bloom=0.4, gran=0.5, rough=2, feather=2)
    art = reflect_smear(art, hy + 22, strength=0.78, stretch=0.9, wob=7, seed=nx(), fade=0.55)
    # vertical light streaks under the brightest sources (the wet-asphalt "drip" of light)
    streaks = []
    for x, y, w, h in row["shop"]:
        for _ in range(3):
            sx = x + rng.uniform(0.1, 0.9) * w
            streaks.append([(sx, hy + 30), (sx + rng.uniform(-6, 6), hy + rng.uniform(160, 320))])
    for r, c in zip(row["sgn"], row["sgn_col"]):
        sx = r[0] + r[2] / 2
        sm = gaussian_filter(lines_mask(W, H, [[(sx, hy + 40), (sx, hy + rng.uniform(200, 380))]], 10), (14, 3))
        art = over(art, col_arr(sm, c, np.clip(sm * 1.6, 0, 0.7)))
    sm = gaussian_filter(lines_mask(W, H, streaks, 7), (16, 2.5))
    art = over(art, col_arr(sm, AMBER_L, np.clip(sm * 1.4, 0, 0.55)))
    sm = gaussian_filter(lines_mask(W, H, [[(lx + 44, hy + 30), (lx + 44, hy + 420)]], 14), (20, 4))
    art = over(art, col_arr(sm, "#ffdca8", np.clip(sm * 1.5, 0, 0.6)))
    # couple under umbrellas
    cx, foot, s = 480, 905, 1.05
    mb, umbs = figure_pair(W, H, cx, foot, s, rng)
    figs = blank(W, H)
    figs = GP(figs, mb, COAT, "#272c38", seed=nx(), rough=1.2, streak=0.5)
    rim = np.clip(mb - np.roll(mb, -3, 1), 0, 1) * (yy < foot - 40)
    figs = over(figs, col_arr(rim, AMBER, rim * 0.55))
    for pts, col, f, R in umbs:
        m = polys(W, H, [pts], smooth=False)
        figs = GP(figs, m, col, mix(col, "#000000", 0.35), seed=nx(), rough=1.4, streak=0.6)
        # ribs and top highlight (lit from the shops behind/above)
        ribs = [[f(0, -R * 0.6), f(u, 2 * s)] for u in np.linspace(-R * 0.9, R * 0.9, 7)]
        figs = over(figs, tint(lines_mask(W, H, ribs, 1.6) * m, mix(col, "#000000", 0.5), 0.5))
        top = m * np.clip(1 - (yy - (f(0, -R * 0.62)[1])) / (R * 0.5), 0, 1)
        figs = G(figs, top, mix(col, "#ffe2b0", 0.55), seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=1.5, feather=2)
        tip = disc(W, H, *f(0, -R * 0.64), 3.2 * s)
        figs = over(figs, tint(tip, "#2a2a2a", 1))
        handle = lines_mask(W, H, [[f(0, -R * 0.6), f(0, 30 * s)]], 2.2 * s)
        figs = over(figs, tint(handle * (1 - m), "#1a1a1a", 0.9))
    # their reflection in the wet road
    refl = figs[::-1].copy()
    off = 2 * foot - H
    rf = np.zeros_like(figs)
    if off >= 0:
        rf[off:] = refl[:H - off]
    else:
        rf[:H + off] = refl[-off:]
    rf = gaussian_filter(rf, (5, 1.2, 0))
    rf[..., 3] *= 0.45 * np.clip(1 - (yy - foot) / 260, 0, 1) * (yy > foot)
    art = over(art, rf)
    art = over(art, figs)
    # puddle ripples
    rip = []
    for _ in range(26):
        px, py = rng.uniform(0, W), rng.uniform(hy + 60, H - 20)
        r = rng.uniform(6, 22) * (0.5 + (py - hy) / (H - hy))
        rip.append(([(px + math.cos(t) * r, py + math.sin(t) * r * 0.28) for t in np.linspace(0, 2 * math.pi, 28)], 1.3))
    rm = lines_mask(W, H, [p for p, _ in rip], 1.3)
    art = over(art, tint(rm, "#c8cfd8", 0.28))
    # falling rain in the air (painted, faint) + brighter inside the lamp light
    rain = rain_streaks(W, H, 520, nx(), (16, 34), 1.0, 0.1)
    art = over(art, col_arr(rain, "#c9d4e0", rain * 0.16))
    art = over(art, col_arr(rain * cone, "#ffe2b5", rain * cone * 2.2))
    art = add_grain(art, nx(), 0.05)
    art = vignette(art, 0.35)
    save_full(art, f"{OUT}/street.webp", quality=74, rgb=True)
    prev(art, "hk-street")


def drops():
    """Raindrops on a window pane, seamless 360 x 360, transparent: lensed beads (bright rim top-left, dark bottom),
    a few elongated drips with trails."""
    N = 360
    rng = np.random.default_rng(3)
    O = 0
    art = blank(N, N)
    items = []
    for _ in range(130):
        items.append((rng.uniform(0, N), rng.uniform(0, N), rng.uniform(1.4, 4.5)))
    for _ in range(14):
        items.append((rng.uniform(0, N), rng.uniform(0, N), rng.uniform(5, 8.5)))
    body, hi, lo = [], [], []
    for x, y, r in items:
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                body.append((x + ox, y + oy, r))
                hi.append((x + ox - r * 0.32, y + oy - r * 0.36, r * 0.34))
                lo.append((x + ox, y + oy + r * 0.45, r * 0.72))
    mb = circles(N, N, body)
    art = over(art, col_arr(mb, "#9fb0c2", mb * 0.22))
    ml = circles(N, N, lo) * mb
    art = over(art, col_arr(ml, "#0d121a", ml * 0.35))
    rim = np.clip(mb - gaussian_filter(mb, 1.2), 0, 1) * 2
    art = over(art, col_arr(rim, "#e6eef7", np.clip(rim, 0, 1) * 0.5))
    mh = circles(N, N, hi)
    art = over(art, col_arr(mh, "#ffffff", mh * 0.85))
    # trails: thin cleared streaks above a few big drops
    tr = []
    for x, y, r in items[-14:]:
        if rng.random() < 0.6:
            for ox in (-N, 0, N):
                for oy in (-N, 0, N):
                    tr.append([(x + ox, y + oy - r), (x + ox + rng.uniform(-3, 3), y + oy - r - rng.uniform(30, 90))])
    tm = lines_mask(N, N, tr, 2.0)
    art = over(art, col_arr(tm, "#c7d3df", tm * 0.18))
    save_full(art, f"{OUT}/drops.webp", quality=82)
    prev(np.concatenate([art, art], 1), "hk-drops", bg="#2a3140")


def rain():
    """Seamless falling-rain tile 200 x 300 (transparent): thin pale streaks, slight slant, varied length/alpha."""
    W, H = 200, 300
    rng = np.random.default_rng(12)
    art = blank(W, H)
    for alpha, n, lw in ((0.22, 26, 1.0), (0.4, 12, 1.3)):
        segs = []
        for _ in range(n):
            x, y, L = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(18, 46)
            for ox in (-W, 0, W):
                for oy in (-H, 0, H):
                    segs.append([(x + ox, y + oy), (x + ox - L * 0.08, y + oy + L)])
        m = gaussian_filter(lines_mask(W, H, segs, lw), 0.4)
        art = over(art, col_arr(m, "#dfe8f2", m * alpha))
    save_full(art, f"{OUT}/rain.webp", quality=82)
    prev(np.concatenate([art, art], 0), "hk-rain", bg="#1a2230")


def pair():
    W, H = 420, 430
    rng = np.random.default_rng(9)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    mb, umbs = figure_pair(W, H, 210, 400, 1.55, rng)
    art = blank(W, H)
    art = GP(art, mb, "#2a3140", "#353d4e", seed=nx(), rough=1.2, streak=0.5)
    rim = np.clip(mb - np.roll(mb, -4, 1), 0, 1) * (yy < 360)
    art = over(art, col_arr(rim, AMBER, rim * 0.7))
    rim = np.clip(mb - np.roll(mb, 3, 1), 0, 1) * (yy < 360)
    art = over(art, col_arr(rim, "#8fb1c9", rim * 0.45))
    for pts, col, f, R in umbs:
        m = polys(W, H, [pts], smooth=False)
        art = GP(art, m, col, mix(col, "#000000", 0.3), seed=nx(), rough=1.6, streak=0.6)
        ribs = [[f(0, -R * 0.6), f(u, 3)] for u in np.linspace(-R * 0.9, R * 0.9, 7)]
        art = over(art, tint(lines_mask(W, H, ribs, 2.0) * m, mix(col, "#000000", 0.5), 0.45))
        top = m * np.clip(1 - (yy - (f(0, -R * 0.62)[1])) / (R * 0.5), 0, 1)
        art = G(art, top, mix(col, "#ffe2b0", 0.5), seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=1.5, feather=2)
        art = over(art, tint(disc(W, H, *f(0, -R * 0.64), 5), "#2a2a2a", 1))
        handle = lines_mask(W, H, [[f(0, -R * 0.6), f(0, 46)]], 3)
        art = over(art, tint(handle * (1 - m), "#1a1a1a", 0.9))
    rain = rain_streaks(W, H, 70, nx(), (14, 26), 1.2, 0.1) * (1 - mb)
    art = over(art, col_arr(rain, "#9fb3c8", rain * 0.5))
    save(art, f"{OUT}/pair.webp", max_w=420)
    prev(art, "hk-pair", bg="#1f2734")


def roofs():
    """Rooftop strip with lit windows standing on a wet reflective street, transparent sky (for bands)."""
    W, H = 780, 330
    hy = 210
    rng = np.random.default_rng(21)
    art = blank(W, H)
    row = building_row(W, H, hy, rng, scale=0.55, lit_p=0.6)
    art = paint_row(art, W, H, row)
    art = GP(art, rects(W, H, [(-10, hy - 2, W + 20, 10)]), "#3b3f48", seed=nx(), rough=1.0, streak=0.4)
    road = rects(W, H, [(-10, hy + 8, W + 20, H)])
    art = over(art, col_arr(road, "#151a22", road))
    art = reflect_smear(art, hy + 8, strength=0.7, stretch=0.8, wob=5, seed=nx(), fade=0.6)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art[..., 3] *= np.clip((H - yy) / 70, 0, 1)
    art = add_grain(art, nx(), 0.04)
    save(art, f"{OUT}/roofs.webp", max_w=780, quality=78)
    prev(art, "hk-roofs", bg="#1a2230")


def ripple():
    W, H = 380, 50
    art = blank(W, H)
    rings = []
    for r, a in ((14, 1.0), (30, 0.7), (50, 0.45), (74, 0.3)):
        rings.append(([(W / 2 + math.cos(t) * r * 2.2, H / 2 + math.sin(t) * r * 0.26) for t in np.linspace(0, 2 * math.pi, 64)], a))
    for pts, a in rings:
        m = lines_mask(W, H, [pts], 1.8)
        art = G(art, m, "#d48f4a", "#7d98ad", seed=nx(), density=0.75 * a + 0.2, edge=0.2, bloom=0, rough=0.6, feather=0.4, pad=4)
    art = G(art, disc(W, H, W / 2, H / 2 - 2, 3), "#e5a25a", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.4, feather=0.3, pad=4)
    save(art, f"{OUT}/ripple.webp", max_w=380)
    prev(art, "hk-ripple", bg="#f1ede6")


def node():
    W = H = 96
    art = blank(W, H)
    m = rects(W, H, [(26, 22, 44, 54)], 4)
    art = lit(art, m, AMBER, 12, 0.5)
    art = GP(art, m, AMBER, AMBER_D, seed=nx(), rough=0.8, streak=0.5)
    art = over(art, tint(lines_mask(W, H, [[(48, 22), (48, 76)], [(26, 44), (70, 44)]], 2.4), "#2a2f38", 0.9))
    art = over(art, tint(rects(W, H, [(22, 74, 52, 6)]), "#2a2f38", 0.9))
    save(art, f"{OUT}/node.webp", max_w=96)
    prev(art, "hk-node", bg="#f1ede6")


for part in PARTS:
    globals()[part]()
    clear()
