"""Mamasa Banua — misty pine valleys of Mamasa (Sulawesi Barat): layered watercolour ridges, pine-clad hills, rice
terraces, and a banua with its heavy, low boat-shaped shingle roof and painted carved gable (red / yellow / black /
white) in gouache. Also a painted carved band, a carved medallion, a pine cluster and a small divider.
Run: python3 -I mamasa-banua.py [part ...]   parts: valley band medallion pines divider
Assets -> public/themes/art/mamasa-banua/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i1_lib import *

OUT = outdir("mamasa-banua")
PARTS = sys.argv[1:] or ["valley", "band", "medallion", "pines", "divider"]
RED, RED_D = "#a8322a", "#6e1d18"
YEL, YEL_D = "#e0aa3a", "#b07a1e"
BLK = "#1f1a17"
WHT = "#f3ece0"
WOOD, WOOD_D = "#5a3a26", "#2e1d13"
PINE, PINE_D = "#3c5a45", "#1f3528"


def pine_mask(W, H, specs, rng):
    """Pines (Pinus merkusii-like): thin trunk + clumpy tufts of needles along drooping tiers. specs: (x, by, h)."""
    trunks, tufts = [], []
    for x, by, h in specs:
        trunks.append(([(x, by), (x + rng.uniform(-1.5, 1.5), by - h)], max(1.2, h * 0.03), (0.0, 0.6)))
        tiers = int(4 + h / 26)
        for k in range(tiers):
            t = k / tiers
            y = by - h * (0.2 + 0.8 * t)
            L = h * 0.3 * (1 - t) ** 0.85 + h * 0.035
            for sgn in (-1, 1):
                n = max(2, int(L / max(3, h * 0.03)))
                for j in range(n):
                    u = (j + 0.5) / n
                    px_ = x + sgn * L * u
                    py_ = y + L * 0.28 * u * u + rng.uniform(-1, 1) * h * 0.01
                    tufts.append((px_, py_, h * rng.uniform(0.035, 0.055), h * rng.uniform(0.018, 0.028), rng.uniform(-25, 25) + sgn * 15))
        tufts.append((x, by - h, h * 0.03, h * 0.05, 0))
    return np.maximum(strokes(W, H, trunks), ellipses(W, H, tufts))


def pine_items(x, by, h, rng):
    return [(x, by, h)]


def banua(W, H, x0, by, w, nx, rng, art, scale=1.0):
    """Side view banua: stilts, plank body, carved painted gable at the left end, heavy saddle roof of shingles."""
    s_ = scale
    bh = 0.26 * w           # body height
    sh = 0.18 * w           # stilt height
    top = by - sh - bh
    # stilts + cross beams
    st = [([(x0 + w * f, by), (x0 + w * f, by - sh)], 0.022 * w, None) for f in (0.08, 0.26, 0.44, 0.62, 0.80, 0.94)]
    st += [([(x0 + w * 0.06, by - sh * 0.45), (x0 + w * 0.96, by - sh * 0.45)], 0.012 * w, None)]
    art = GP(art, strokes(W, H, st), WOOD, WOOD_D, seed=nx(), rough=0.8, streak=0.6, pad=8)
    # ladder at the front
    lad = [([(x0 - 0.05 * w, by), (x0 + 0.06 * w, by - sh)], 0.01 * w, None), ([(x0 - 0.0 * w, by), (x0 + 0.11 * w, by - sh)], 0.01 * w, None)]
    lad += [([(x0 - 0.05 * w + 0.11 * w * t, by - sh * t), (x0 + 0.11 * w * t, by - sh * t)], 0.007 * w, None) for t in (0.25, 0.5, 0.75)]
    art = GP(art, strokes(W, H, lad), "#6d4a30", WOOD_D, seed=nx(), rough=0.6, pad=8)
    # body: planks
    body = polys(W, H, [rect(x0, top, x0 + w, by - sh)])
    art = GP(art, body, "#6e4a30", "#4a2f1e", seed=nx(), rough=1.2, streak=1.0)
    planks = strokes(W, H, [([(x0, y), (x0 + w, y)], 1.2, None) for y in np.arange(top + 6, by - sh, 7)])
    art = G(art, planks * body, WOOD_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.4)
    # painted carved panels along the body (repeating squares)
    pw = bh * 0.7
    k = 0
    for px_ in np.arange(x0 + w * 0.2, x0 + w * 0.92, pw * 1.15):
        cx, cy = px_ + pw / 2, top + bh / 2
        sq = polys(W, H, [rect(px_, cy - pw / 2, px_ + pw, cy + pw / 2)])
        art = GP(art, sq, BLK, seed=nx(), rough=0.5, pad=6)
        dia = polys(W, H, [[(cx, cy - pw * 0.42), (cx + pw * 0.42, cy), (cx, cy + pw * 0.42), (cx - pw * 0.42, cy)]])
        art = GP(art, dia, RED if k % 2 == 0 else YEL, seed=nx(), rough=0.5, pad=6)
        art = GP(art, circles(W, H, [(cx, cy, pw * 0.13)]), WHT, seed=nx(), rough=0.3, pad=4)
        k += 1
    # front gable (left end): tall painted triangle panel under the projecting roof
    gx = x0 - 0.03 * w
    gab = polys(W, H, [[(gx, by - sh), (gx, top - 0.06 * w), (gx + 0.17 * w, top - 0.20 * w), (gx + 0.2 * w, by - sh)]])
    art = GP(art, gab, BLK, seed=nx(), rough=0.7, pad=8)
    # gable motifs: stacked bands of red/yellow triangles and white lines
    bands = []
    for j, y in enumerate(np.arange(by - sh - 4, top - 0.16 * w, -0.045 * w)):
        tri = []
        for i in range(7):
            tx = gx + 0.01 * w + i * 0.028 * w
            tri.append([(tx, y), (tx + 0.014 * w, y - 0.03 * w), (tx + 0.028 * w, y)])
        m = polys(W, H, tri) * gab
        art = GP(art, m, (RED, YEL, WHT)[j % 3], seed=nx(), rough=0.4, pad=4)
        bands.append(([(gx, y + 1), (gx + 0.2 * w, y + 1)], 1.4, None))
    art = GP(art, strokes(W, H, bands) * gab, WHT, seed=nx(), rough=0.3, pad=4)
    # heavy saddle roof: low ridge with a gentle sag, ends lifting only modestly, thick eaves
    rx0, rx1 = x0 - 0.26 * w, x0 + w + 0.22 * w
    ridge = curve([(rx0, top - 0.33 * w), (x0 + w * 0.15, top - 0.25 * w), (x0 + w * 0.55, top - 0.235 * w), (x0 + w * 0.95, top - 0.25 * w), (rx1, top - 0.31 * w)], 50)
    eave = curve([(rx1 - 0.01 * w, top - 0.20 * w), (x0 + w * 1.02, top + 0.06 * w), (x0 + w * 0.5, top + 0.10 * w), (x0 - 0.04 * w, top + 0.06 * w), (rx0 + 0.02 * w, top - 0.22 * w)], 50)
    roof = shapes(W, H, [ridge + eave])
    art = over(art, soft_shadow(roof, "#1a1410", blur=5, strength=0.5, dx=0, dy=8))
    art = GP(art, roof, "#3a2e26", "#221a15", seed=nx(), rough=1.6, streak=1.1)
    # shingle courses following the roof
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rows = strokes(W, H, [([(p[0], p[1] + d) for p in ridge], 1.3, None) for d in np.arange(8, 0.36 * w, 6)])
    art = G(art, rows * roof, "#0f0b09", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8, feather=0.4)
    lit = roof * np.clip(1 - (yy - (top - 0.3 * w)) / (0.18 * w), 0, 1)
    art = G(art, lit, "#7a6a58", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
    rim = strokes(W, H, [(eave, 0.02 * w, (0.05, 0.05))])
    art = GP(art, rim, "#2a201a", seed=nx(), rough=0.6, pad=6)
    # painted ridge-end boards
    for (ex, ey) in (ridge[0], ridge[-1]):
        art = GP(art, polys(W, H, [[(ex - 3, ey - 2), (ex + 3, ey - 2), (ex + 3, ey + 0.1 * w), (ex - 3, ey + 0.1 * w)]]), RED, seed=nx(), rough=0.3, pad=4)
    return art, roof


if "valley" in PARTS:
    W, H = 780, 760
    nx = Seq(40100); rng = random.Random(41)
    sky = painted_sky(W, H, [(0, "#eef0e8"), (0.35, "#e8ebe2"), (0.6, "#dfe4da"), (1, "#dfe4da")], seed=4, streak=0.6)
    art = fade_alpha(sky, 0, H * 0.22)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # far ridges, cooler and paler with distance, mist between
    for i, (y, amp, col, col2, wl) in enumerate([(H * 0.30, 50, "#b9c4c6", "#a5b3b8", 0.9), (H * 0.38, 46, "#99aab0", "#869aa0", 0.62),
                                               (H * 0.47, 40, "#7c938f", "#647d78", 0.5)]):
        r = hills(W, H, y, amp, 60 + i, wl)
        art = G(art, r, col, col2, seed=nx(), density=0.8, edge=0.5, bloom=0.4, rough=5)
        mist = r * np.clip(((y + 40) - yy) / -60 + 1.4, 0, 1) * np.clip((yy - y) / 60, 0, 1)
        art = OV(art, gaussian_filter(mist, 6) * 0.55, lambda m: tint(m, "#eef0e8", 1.0))
    clear()
    # pine-clad mid hill with ridge-line pines
    mid = hills(W, H, H * 0.56, 34, 71, 0.7)
    art = G(art, mid, "#57735a", "#3d5a46", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=4)
    items = []
    for x in np.arange(-10, W + 10, 9):
        # ridge height at x
        col = mid[:, int(min(W - 1, max(0, x)))]
        ys = np.where(col > 0.5)[0]
        if len(ys) == 0:
            continue
        y0 = ys.min()
        for _ in range(2):
            items += pine_items(x + rng.uniform(-4, 4), y0 + rng.uniform(4, 40), rng.uniform(26, 52), rng)
    pm = pine_mask(W, H, items, rng)
    art = G(art, pm, PINE, PINE_D, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.2, feather=0.6)
    haze = mid * np.clip((yy - H * 0.6) / 50, 0, 1)
    art = OV(art, gaussian_filter(haze, 4) * 0.35, lambda m: tint(m, "#dfe6dc", 1.0))
    clear()
    # rice terraces: contour bands stepping down, alternating fresh and ripening greens with dark bunds
    TY = H * 0.62
    prev = None
    cols = [("#9cb35f", "#7f9a48"), ("#b7c36a", "#93a352"), ("#8faa55", "#6f8c40"), ("#c4c46e", "#a5a656"), ("#94ae58", "#738f44"), ("#aebd64", "#8d9f4d"), ("#88a452", "#69873f")]
    for i in range(7):
        y = TY + i * (H - TY) / 6.2
        amp = 10 + i * 3
        ph = rng.uniform(0, 3)
        top = [(x, y + amp * math.sin(x / W * 3.2 + ph) + 8 * math.sin(x / 70 + i) + 5 * math.sin(x / 31 + ph * 2)) for x in range(-20, W + 21, 10)]
        band = polys(W, H, [top + [(W + 20, H + 20), (-20, H + 20)]])
        art = GP(art, band, *cols[i], seed=nx(), rough=2.0, streak=0.8)
        lip = strokes(W, H, [(top, 3.0 + i * 0.4, None)])
        art = GP(art, lip, "#5e6b34", "#4a5528", seed=nx(), rough=0.8, pad=6)
        wet = strokes(W, H, [([(p[0], p[1] + 5 + i) for p in top], 4 + i, None)]) * band
        art = G(art, wet, "#c9d6b0", seed=nx(), density=0.3, edge=0.1, bloom=0.2, rough=1.5)
        if i in (1, 4):
            nxt = [(x, y + (H - TY) / 6.2 + 4) for x, _ in top]
            pond = band * np.clip(fbm(W, H, 90 + i, 120, 2) * 5 - 3.0, 0, 1)
            art = OV(art, gaussian_filter(pond, 1), lambda m: gouache_paint(m, "#d3dddc", "#aebfc2", seed=nx(), rough=2, streak=1.0, density=0.9))
        # rice rows
        rows = strokes(W, H, [([(x, y + 10 + j * 7), (x + 4, y + 6 + j * 7)], 1.2, None) for x in range(0, W, 9) for j in range(3)])
        art = G(art, rows * band, "#5f7a36", seed=nx(), density=0.28, edge=0, bloom=0, rough=0.5, feather=0.4)
    clear()
    # the banua on a terrace (mid-right) and a smaller one far left
    art, _ = banua(W, H, W * 0.47, H * 0.70, 300, nx, rng, art)
    art, _ = banua(W, H, W * 0.06, H * 0.615, 110, nx, rng, art)
    # foreground pines framing left and right
    fp = []
    fp += pine_items(W * 0.03, H * 0.98, 250, rng)
    fp += pine_items(W * 0.14, H * 1.0, 180, rng)
    fp += pine_items(W * 0.97, H * 0.99, 230, rng)
    art = G(art, pine_mask(W, H, fp, rng), "#2f4a39", "#16271d", seed=nx(), density=0.92, edge=0.55, bloom=0.2, rough=1.4, feather=0.6)
    art = add_grain(art, 7, 0.03)
    show(art, "mm-valley")
    save_full(art, f"{OUT}/valley.webp", size=(780, 760), quality=78)
    clear()


def motif_band(W, H, nx, rng, h0, h1):
    """Painted carved band: black ground, red/yellow triangles + white-lined spiral pairs (ukiran Mamasa-inspired)."""
    band = polys(W, H, [rect(0, h0, W, h1)])
    art = GP(blank(W, H), band, BLK, "#2a221d", seed=nx(), rough=0.6, streak=0.6)
    hh = h1 - h0
    step = hh * 1.6
    tri_r, tri_y, spir, lines = [], [], [], []
    for i, x in enumerate(np.arange(-step, W + step, step)):
        tri_r.append([(x, h0 + hh * 0.12), (x + step / 2, h0 + hh * 0.12), (x + step / 4, h0 + hh * 0.42)])
        tri_y.append([(x + step / 2, h1 - hh * 0.12), (x + step, h1 - hh * 0.12), (x + step * 0.75, h1 - hh * 0.42)])
        cx, cy = x + step * 0.75, h0 + hh * 0.36
        spir.append((spiral_pts(x + step * 0.25, h1 - hh * 0.32, hh * 0.18, hh * 0.03, 0, 1.4, 30, 1), hh * 0.06, (0.0, 0.5)))
        spir.append((spiral_pts(cx, cy, hh * 0.15, hh * 0.03, math.pi, 1.4, 30, -1), hh * 0.06, (0.0, 0.5)))
    art = GP(art, polys(W, H, tri_r), RED, RED_D, seed=nx(), rough=0.6, pad=6)
    art = GP(art, polys(W, H, tri_y), YEL, YEL_D, seed=nx(), rough=0.6, pad=6)
    art = GP(art, strokes(W, H, spir), WHT, "#e2d8c6", seed=nx(), rough=0.4, pad=6)
    edges = strokes(W, H, [([(0, h0 + hh * 0.06), (W, h0 + hh * 0.06)], hh * 0.05, None), ([(0, h1 - hh * 0.06), (W, h1 - hh * 0.06)], hh * 0.05, None)])
    art = GP(art, edges, WHT, seed=nx(), rough=0.4, pad=4)
    # carved relief shading: dark under each shape, wear
    relief = np.maximum.reduce([polys(W, H, tri_r), polys(W, H, tri_y), strokes(W, H, spir)])
    lo = np.clip(np.roll(relief, 2, 0) - relief, 0, 1)
    art = G(art, lo, "#000000", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.5)
    return art


if "band" in PARTS:
    W, H = 780, 72
    nx = Seq(40200); rng = random.Random(42)
    art = motif_band(W, H, nx, rng, 4, 68)
    show(art, "mm-band", bg="#efe6d6")
    save_full(art, f"{OUT}/band.webp", size=(780, 72), quality=82)

if "divider" in PARTS:
    W, H = 520, 64
    nx = Seq(40300); rng = random.Random(43)
    art = motif_band(W, H, nx, rng, 8, 56)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    k = np.clip(1 - np.abs(xx - W / 2) / (W / 2), 0, 1) ** 0.25
    art[..., 3] *= np.clip(k * 1.6, 0, 1)
    show(art, "mm-divider", bg="#efe6d6")
    save(art, f"{OUT}/divider.webp", max_w=260, quality=84)

if "medallion" in PARTS:
    W, H = 300, 300
    nx = Seq(40400); rng = random.Random(44)
    cx, cy = 150, 150
    sq = polys(W, H, [[(cx, 8), (W - 8, cy), (cx, H - 8), (8, cy)]])
    art = GP(blank(W, H), sq, BLK, "#2a221d", seed=nx(), rough=0.8, streak=0.6)
    art = GP(art, strokes(W, H, [([(cx, 18), (W - 18, cy), (cx, H - 18), (18, cy), (cx, 18)], 5, None)]), WHT, seed=nx(), rough=0.4)
    # rosette: 8 red petals, 8 yellow between, white spirals at the quarters, a white/red eye
    pet = [petal_pts(cx, cy, 92, 30, k * math.tau / 8, n=12) for k in range(8)]
    art = GP(art, shapes(W, H, pet), RED, RED_D, seed=nx(), rough=0.6)
    pet2 = [petal_pts(cx, cy, 64, 18, k * math.tau / 8 + math.tau / 16, n=10) for k in range(8)]
    art = GP(art, shapes(W, H, pet2), YEL, YEL_D, seed=nx(), rough=0.5)
    sp = [(spiral_pts(cx + math.cos(a) * 108, cy + math.sin(a) * 108, 14, 2, a, 1.3, 26, 1), 4, (0.0, 0.5)) for a in [k * math.tau / 4 for k in range(4)]]
    art = GP(art, strokes(W, H, sp), WHT, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(cx, cy, 22)]), WHT, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(cx, cy, 11)]), RED, seed=nx(), rough=0.3)
    relief = np.maximum(shapes(W, H, pet), shapes(W, H, pet2))
    art = G(art, np.clip(np.roll(relief, 3, 0) - relief, 0, 1), "#000000", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.5)
    show(art, "mm-medallion", bg="#efe6d6")
    save(art, f"{OUT}/medallion.webp", max_w=180, quality=84)

if "pines" in PARTS:
    W, H = 360, 460
    nx = Seq(40500); rng = random.Random(45)
    it = pine_items(120, 452, 400, rng) + pine_items(250, 456, 300, rng) + pine_items(320, 458, 180, rng)
    art = G(blank(W, H), pine_mask(W, H, it, rng), "#3c5a45", "#1f3528", seed=nx(), density=0.9, edge=0.6, bloom=0.25, rough=1.4, feather=0.6)
    show(art, "mm-pines")
    save(art, f"{OUT}/pines.webp", max_w=220, quality=82)
