"""Oasis Kurma — bright midday oasis in fresh gouache: pale blue sky, apricot dunes, a clear turquoise pool mirroring a
grove of date palms on the far bank, foreground date palms heavy with amber date clusters.
Run: python3 -I oasis-kurma.py [part ...]   parts: scene palm dates sprig dune sand
Assets -> public/themes/art/oasis-kurma/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b3_lib import *

OUT = outdir("oasis-kurma")
PARTS = sys.argv[1:] or ["scene", "palm", "dates", "sprig", "dune", "sand"]
SKY_T, SKY_B = "#8fc3e6", "#e9f3f4"
SAND_L, SAND_M, SAND_D = "#f3e2c2", "#e7c99a", "#c99a68"
G_DARK, G_MID, G_LIGHT, G_SUN = "#2f5a36", "#4f8241", "#7fae4e", "#b5cf6e"
TRUNK, TRUNK_D = "#9a7550", "#5e4430"
DATE_A, DATE_B, DATE_C = "#e0a03a", "#b8602a", "#7a3a1e"


def frond_strokes(x0, y0, ang, L, droop, rng, lw=3.4, density=1.0, fold=0.55, hang=0.35):
    """One pinnate date-palm frond: rachis launched at ang and bent by gravity (droop = strength), many narrow
    leaflets angled toward the tip, hanging slightly. Returns (rachis_stroke, leaflet_strokes)."""
    pts = [(x0, y0)]
    dx, dy = math.cos(ang), math.sin(ang)
    step = L / 35
    for i in range(1, 36):
        t = i / 35
        dy += abs(droop) * 0.09 * t
        n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
        pts.append((pts[-1][0] + dx * step, pts[-1][1] + dy * step))
    leaf = []
    n = int(34 * density)
    for k in range(3, n):
        t = k / n
        i = min(34, int(t * 35))
        x, y = pts[i]
        ddx, ddy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        da = math.atan2(ddy, ddx)
        ll = L * (0.26 * math.sin(math.pi * (0.12 + 0.8 * t)) + 0.04) * rng.uniform(0.85, 1.15)
        for side in (-1, 1):
            a = da + side * (fold + rng.uniform(-0.1, 0.1))
            ex, ey = x + math.cos(a) * ll, y + math.sin(a) * ll + ll * hang
            mx, my = x + math.cos(a) * ll * 0.5, y + math.sin(a) * ll * 0.5 + ll * 0.08
            leaf.append(([(x, y), (mx, my), (ex, ey)], lw * rng.uniform(0.85, 1.1), (0.04, 0.75)))
    return (pts, lw * 1.1, (0.02, 0.5)), leaf


def trunk_masks(W, H, base, top, w0, w1, bend=0.0):
    """Tapered curved trunk polygon + leaf-base (diamond) texture lines."""
    (bx, by), (tx, ty) = base, top
    n = 30
    left, right, mid = [], [], []
    for i in range(n + 1):
        t = i / n
        x = bx + (tx - bx) * t + math.sin(t * math.pi) * bend
        y = by + (ty - by) * t
        wd = w0 + (w1 - w0) * t
        left.append((x - wd / 2, y)); right.append((x + wd / 2, y)); mid.append((x, y, wd))
    body = shape_mask(W, H, left + right[::-1], smooth=False)
    lines = []
    for i in range(1, n * 2):
        t = i / (n * 2)
        j = int(t * n)
        x, y, wd = mid[j]
        lines.append(([(x - wd / 2, y + wd * 0.18), (x, y - wd * 0.05), (x + wd / 2, y + wd * 0.18)], 1.6, None))
    tex = strokes(W, H, lines) * body
    # shade side (right) mask
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade_m = np.zeros((H, W), np.float32)
    for x, y, wd in mid:
        pass
    return body, tex, mid


def paint_palm(art, W, H, base, height, seed, lean=0.0, scale=1.0, clusters=3, light_side=-1, far=False):
    """A full date palm onto art (gouache, opaque)."""
    rng = random.Random(seed)
    bx, by = base
    top = (bx + lean * height, by - height)
    w0, w1 = 30 * scale, 19 * scale
    body, tex, mid = trunk_masks(W, H, base, top, w0, w1, bend=lean * height * 0.15)
    tcol, tcol2 = (TRUNK, "#b08a62") if not far else ("#b49a7c", "#c9b39a")
    art = GP(art, body, tcol, tcol2, seed=seed)
    # shade half of the trunk away from the sun
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cxline = np.interp(yy[:, 0], [m[1] for m in mid[::-1]], [m[0] for m in mid[::-1]])[:, None]
    shadow = body * (((xx - cxline) * (-light_side)) > -2 * scale)
    art = OV(art, shadow, lambda m: gouache_paint(m, TRUNK_D if not far else "#9c8268", seed=seed + 1, density=0.55))
    art = OV(art, tex, lambda m: gouache_paint(m, "#4a3522" if not far else "#8c7258", seed=seed + 2, density=0.7, rough=1.5))
    tx, ty = mid[-1][0], mid[-1][1]
    # fronds: back (dark) -> middle -> front (light)
    angs = []
    for k in range(17):
        a = -math.pi / 2 + (k - 8) * 0.36 + rng.uniform(-0.08, 0.08)
        angs.append(a)
    layers = [([], G_DARK, "#3c6a3c"), ([], G_MID, "#669a48"), ([], G_LIGHT, G_SUN)]
    for k, a in enumerate(angs):
        side = math.cos(a)
        L = (150 + rng.uniform(-15, 25)) * scale * (1.0 - 0.25 * abs(math.sin(a + math.pi / 2)) * 0)
        droop = 0.35 + 0.75 * abs(side)
        rach, leaf = frond_strokes(tx, ty, a, L, droop, rng, lw=5.4 * scale, density=1.0)
        lay = 0 if k % 3 == 0 else (1 if k % 3 == 1 else 2)
        if (light_side < 0 and side < -0.2) or (light_side > 0 and side > 0.2):
            lay = min(2, lay + 1)
        layers[lay][0].extend([rach] + leaf)
    # a few drooping old fronds below
    for k in range(4):
        a = math.pi / 2 + (k - 1.5) * 0.7
        rach, leaf = frond_strokes(tx, ty + 4, a + (0.5 if k < 2 else -0.5), 120 * scale, 1.2, rng, lw=4.6 * scale, density=0.8)
        layers[0][0].extend([rach] + leaf)
    for items, c1, c2 in layers:
        m = strokes(W, H, items)
        if far:
            c1, c2 = mix(c1, "#c9dccd", 0.5), mix(c2, "#dde8cf", 0.5)
        art = GP(art, m, c1, c2, seed=rng.randint(1, 999), rough=1.4, streak=0.6)
        trim_cache()
    # dates hang beneath the crown
    if clusters:
        for k in range(clusters):
            a = math.pi / 2 + (k - (clusters - 1) / 2) * 0.55 + rng.uniform(-0.1, 0.1)
            art = date_cluster(art, W, H, tx + math.cos(a) * 10 * scale, ty + 14 * scale, 52 * scale, a, seed + 10 + k, scale)
    return art


def date_cluster(art, W, H, x, y, L, ang, seed, scale=1.0):
    """Hanging bunch: orange stalks (strands) fanning down with dates threaded along them."""
    rng = random.Random(seed)
    strands = []
    dates = []
    for k in range(9):
        a = ang + (k - 4) * 0.08 + rng.uniform(-0.05, 0.05)
        ln = L * rng.uniform(0.8, 1.2)
        p0 = (x, y)
        p1 = (x + math.cos(ang) * ln * 0.4, y + math.sin(ang) * ln * 0.4)
        p3 = (x + math.cos(a) * ln + (k - 4) * 2.2 * scale, y + math.sin(a) * ln + ln * 0.25)
        pts = bez(p0, p1, ((p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2), p3, 16)
        strands.append((pts, 1.6 * scale, (0.0, 0.3)))
        for j in range(4, 16, 2):
            px, py = pts[j]
            dates.append((px + rng.uniform(-3, 3) * scale, py + rng.uniform(-1, 3) * scale, 3.6 * scale * rng.uniform(0.9, 1.1), 5.2 * scale * rng.uniform(0.9, 1.1), rng.uniform(-15, 15) + math.degrees(a - math.pi / 2)))
    art = GP(art, strokes(W, H, strands), "#d8a24a", "#c48a34", seed=seed, rough=1.0)
    rng.shuffle(dates)
    n = len(dates)
    groups = [dates[: n // 3], dates[n // 3: 2 * n // 3], dates[2 * n // 3:]]
    for g, (c1, c2) in zip(groups, ((DATE_C, DATE_B), (DATE_B, DATE_A), (DATE_A, "#efc05a"))):
        m = ellipses(W, H, g)
        art = GP(art, m, c1, c2, seed=seed + 3, rough=1.0, streak=0.3)
        # glossy highlight on each date
        hl = ellipses(W, H, [(dx - dw * 0.35, dy - dh * 0.35, dw * 0.28, dh * 0.3, r) for dx, dy, dw, dh, r in g])
        art = OV(art, hl * m, lambda mm: gouache_paint(mm, "#fbe2a6", seed=seed + 5, density=0.55, rough=0.6))
    return art


if "scene" in PARTS:
    W, H = 640, 1390
    hz = int(H * 0.46)            # horizon of the far dunes
    pool_top, pool_bot = int(H * 0.535), int(H * 0.63)
    sky = painted_sky(W, H, [(0, "#7fb6df"), (0.25, "#a9d0ea"), (0.44, "#e6f1f1"), (1, "#f8f0e2")], seed=3, streak=0.35, grain=0.3)
    art = sky
    # soft gouache clouds
    rng = random.Random(9)
    cl = []
    for cx_, cy_, s_ in ((120, 210, 1.0), (500, 150, 0.8), (430, 380, 0.6), (60, 470, 0.5)):
        for k in range(6):
            cl.append((cx_ + rng.uniform(-60, 60) * s_, cy_ + rng.uniform(-10, 12) * s_, rng.uniform(30, 56) * s_, rng.uniform(14, 22) * s_, 0))
    art = GP(art, ellipses(W, H, cl), "#fbfdfc", "#eef5f6", seed=11, rough=4, density=0.75)
    # far dunes: three ridges, pale apricot with lilac-shaded lee sides
    for k, (yb, amp, c1, c2, sh) in enumerate(((hz - 40, 40, "#f1dcc0", "#ecd3b2", "#d9bfa8"), (hz - 4, 34, "#efd4ae", "#e6c597", "#cfa982"), (hz + 50, 26, "#f2dcb8", "#e9cb9c", "#d2a979"))):
        xs = np.linspace(-20, W + 20, 40)
        prof = [(x, yb - amp * (0.5 + 0.5 * math.sin(x / (120 + 40 * k) + k * 2.1)) - 10 * math.sin(x / 47 + k)) for x in xs]
        poly = prof + [(W + 20, H), (-20, H)]
        m = shape_mask(W, H, poly)
        art = GP(art, m, c1, c2, seed=20 + k, rough=2.5)
        # lee-side shadows: a soft band under each crest on the right flank
        shp = [(x, y + 2) for x, y in prof] + [(x + 40, y + 26 + 8 * math.sin(x / 30)) for x, y in prof[::-1]]
        art = OV(art, shape_mask(W, H, shp) * m, lambda mm, c=sh, s_=k: gouache_paint(mm, c, seed=30 + s_, density=0.45, rough=3))
    # far grove of palms on the other bank (small, hazy)
    far_items = [(70, pool_top + 8, 230, -0.04, 0.55), (150, pool_top + 4, 270, 0.05, 0.62), (230, pool_top + 10, 200, -0.08, 0.5),
                 (430, pool_top + 6, 250, 0.06, 0.58), (520, pool_top + 10, 210, -0.05, 0.5), (590, pool_top + 4, 280, 0.03, 0.62)]
    for i, (x, y, hgt, ln, sc) in enumerate(far_items):
        art = paint_palm(art, W, H, (x, y), hgt, 100 + i, lean=ln, scale=sc, clusters=2 if sc > 0.55 else 0, far=True)
        clear()
    # bank grasses / reeds behind the pool
    reeds = []
    for k in range(120):
        x = rng.uniform(-10, W + 10); y = pool_top + rng.uniform(-4, 6)
        hgt = rng.uniform(10, 34)
        reeds.append(([(x, y), (x + rng.uniform(-6, 6), y - hgt)], rng.uniform(1.6, 2.8), (0.0, 0.7)))
    art = GP(art, strokes(W, H, reeds), "#6f9a4a", "#9bbb5c", seed=41, rough=1)
    # pool: reflection of everything above the bank, flipped, rippled, tinted turquoise
    region = art[pool_top - (pool_bot - pool_top) * 2: pool_top][::-1]
    rh = pool_bot - pool_top
    refl = region[: rh * 2: 2] if region.shape[0] >= rh * 2 else region[:rh]
    refl = refl[:rh]
    yy, xx = np.mgrid[0:rh, 0:W].astype(np.float32)
    rip = np.sin(yy * 0.9 + fbm(W, rh, 7, 20, 2) * 6) * (1.2 + yy / rh * 3)
    refl = np.stack([map_coordinates(refl[..., c], [yy, np.clip(xx + rip, 0, W - 1)], order=1) for c in range(4)], -1)
    water = np.ones((rh, W, 3), np.float32) * C("#6cc3c6")
    deep = np.ones((rh, W, 3), np.float32) * C("#3f9fb0")
    t = (yy / rh)[..., None]
    wcol = water * (1 - t) + deep * t
    rgb = refl[..., :3] * 0.45 + wcol * 0.55
    # sky glints: horizontal light dashes
    dash = (gaussian_filter(np.random.default_rng(5).random((rh, W)).astype(np.float32), (0.6, 9)) > 0.53).astype(np.float32)
    rgb = rgb * (1 - dash[..., None] * 0.5) + dash[..., None] * 0.5 * C("#f4fbfb")
    pool = np.zeros((H, W), np.float32)
    pool_shape = [(x, pool_top + 3 * math.sin(x / 40)) for x in np.linspace(-20, W + 20, 30)] + [(x, pool_bot + 6 * math.sin(x / 55 + 1)) for x in np.linspace(W + 20, -20, 30)]
    pm = shape_mask(W, H, pool_shape)
    full = np.zeros((H, W, 4), np.float32)
    full[pool_top:pool_bot, :, :3] = rgb
    full[pool_top:pool_bot, :, 3] = 1
    full[pool_bot:pool_bot + 12, :, :3] = rgb[-1:]
    full[pool_bot:pool_bot + 12, :, 3] = 1
    full[..., 3] *= np.clip(displace(pm, 13, 2.0, 20), 0, 1)
    art = over(art, full)
    # near bank: pale sand with a wet darker lip, then foreground sand
    near = [(x, pool_bot + 4 + 5 * math.sin(x / 55 + 1) + 3 * math.sin(x / 13)) for x in np.linspace(-20, W + 20, 50)] + [(W + 20, H), (-20, H)]
    nm = shape_mask(W, H, near)
    art = GP(art, nm, "#f8eed9", "#f2e2c4", seed=51, rough=2.5, streak=0.25)
    lip = shape_mask(W, H, near[:50] + [(x, y + 10) for x, y in near[:50][::-1]])
    art = OV(art, lip, lambda mm: gouache_paint(mm, "#d9bd90", seed=52, density=0.6, rough=2))
    # foreground tufts and pebbles
    tufts = []
    for cx_ in (40, 600, 110):
        for k in range(16):
            a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
            l = rng.uniform(16, 40)
            tufts.append(([(cx_, pool_bot + 30), (cx_ + math.cos(a) * l * 0.6, pool_bot + 30 + math.sin(a) * l * 0.6), (cx_ + math.cos(a) * l, pool_bot + 30 + math.sin(a) * l)], 2.4, (0, 0.7)))
    art = GP(art, strokes(W, H, tufts), "#7ea24c", "#a8c25e", seed=61, rough=1)
    # ripple marks on the foreground sand
    rip = []
    for k in range(14):
        y = pool_bot + 80 + k * 36 + rng.uniform(-6, 6)
        x0 = rng.uniform(-40, 200); ln = rng.uniform(160, 420)
        rip.append(([(x0 + t * ln, y + 6 * math.sin(t * 6 + k)) for t in np.linspace(0, 1, 20)], 3.2, (0.3, 0.4)))
    art = OV(art, strokes(W, H, rip), lambda mm: gouache_paint(mm, "#e4cb9f", seed=71, density=0.55, rough=1.5, streak=0.2))
    art = add_grain(art, 3, 0.02)
    rgb_save(art, f"{OUT}/scene.webp", quality=78, size=(560, 1216))
    to_image(art).convert("RGB").save(f"{PREV}/ok-scene.png")
    clear()

if "palm" in PARTS:
    W, H = 520, 1100
    art = blank(W, H)
    art = paint_palm(art, W, H, (300, 1090), 820, 7, lean=-0.1, scale=1.25, clusters=4, light_side=-1)
    preview(art, "ok-palm", bg="#a9d0ea")
    save(art, f"{OUT}/palm.webp", max_w=300, quality=82)
    clear()

if "dates" in PARTS:
    S = 260
    art = blank(S, S)
    # short frond stub on top + one rich bunch
    rng = random.Random(4)
    rach, leaf = frond_strokes(130, 40, -0.5, 120, 0.8, rng, lw=5.0)
    rach2, leaf2 = frond_strokes(130, 40, math.pi + 0.5, 120, 0.8, rng, lw=5.0)
    art = GP(art, strokes(S, S, [rach] + leaf + [rach2] + leaf2), G_MID, G_LIGHT, seed=5, rough=1.2)
    art = date_cluster(art, S, S, 130, 44, 120, math.pi / 2, 8, 1.6)
    preview(art, "ok-dates", bg="#f6efe0")
    save(art, f"{OUT}/dates.webp", max_w=180, quality=84)
    clear()

if "sprig" in PARTS:
    W, H = 620, 120
    art = blank(W, H)
    rng = random.Random(12)
    items = []
    for side in (-1, 1):
        rach, leaf = frond_strokes(W / 2 + side * 16, 58, (0 if side > 0 else math.pi) + side * -0.06, 270, 0.12, rng, lw=4.4, density=1.2, fold=0.75, hang=0.08)
        items += [rach] + leaf
    art = GP(art, strokes(W, H, items), G_MID, G_LIGHT, seed=13, rough=1.0)
    art = date_cluster(art, W, H, W / 2, 50, 48, math.pi / 2, 14, 0.9)
    preview(art, "ok-sprig", bg="#f6efe0")
    save(art, f"{OUT}/sprig.webp", max_w=440, quality=84)
    clear()

if "dune" in PARTS:
    W, H = 800, 220
    art = blank(W, H)
    for k, (yb, amp, c1, c2) in enumerate(((90, 50, "#efd4ae", "#e6c597"), (150, 36, "#f3e0c0", "#ead0a6"))):
        xs = np.linspace(-20, W + 20, 40)
        prof = [(x, yb - amp * (0.5 + 0.5 * math.sin(x / (150 + 30 * k) + k * 1.7)) - 8 * math.sin(x / 53 + k)) for x in xs]
        m = shape_mask(W, H, prof + [(W + 20, H + 60), (-20, H + 60)])
        art = GP(art, m, c1, c2, seed=80 + k, rough=2.5)
        shp = [(x, y + 2) for x, y in prof] + [(x + 50, y + 30) for x, y in prof[::-1]]
        art = OV(art, shape_mask(W, H, shp) * m, lambda mm, s_=k: gouache_paint(mm, "#d6b58c", seed=90 + s_, density=0.45, rough=3))
    preview(art, "ok-dune", bg="#8fc3e6")
    save_full(art, f"{OUT}/dune.webp", size=(640, 176), quality=80)
    clear()

if "sand" in PARTS:
    S = 512
    n1 = noise(S, S, 3, 50, wrap=True); n2 = noise(S, S, 4, 1.0, wrap=True)
    rgb = lerp3(C("#f9f1e2"), C("#f2e5cd"), np.clip(n1 * 1.2 - 0.1, 0, 1))
    rgb = rgb * (0.985 + 0.03 * n2[..., None])
    rgb_save(rgba(rgb, np.ones((S, S), np.float32)), f"{OUT}/sand.webp", quality=72)
    clear()

report(OUT)
