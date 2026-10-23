"""Manggarai Lingko — painted pieces: the spider-web lingko rice field seen from above (gouache cells, planted rows,
earth bunds, tree clumps), a Wae Rebo-like mbaru niang village in mountain mist (watercolour + gouache thatch),
a woven songke band tile (black with red/yellow/green/white motifs), a black songke weave tile, a single cone-house
emblem and a small songke divider.
Run: python3 -I manggarai-lingko.py [part ...]  parts: lingko niang songke weave cone divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k3_lib import *

OUT = outdir("manggarai-lingko")
PARTS = sys.argv[1:] or ["lingko", "niang", "songke", "weave", "cone", "divider"]
BLACK = "#16120e"
SONG = {"r": "#c8432b", "o": "#e08a2c", "y": "#e8c547", "g": "#3f8a4a", "w": "#efe6d2", "b": "#3b6aa0"}


def thatch(W, H, roof, rng, n=900, col_len=(6, 14)):
    """Short downward thatch strokes clipped to the roof."""
    ys, xs = np.where(roof > 0.5)
    if len(xs) == 0:
        return np.zeros_like(roof)
    idx = np.random.default_rng(rng.randint(0, 9999)).choice(len(xs), min(n, len(xs)), replace=False)
    items = []
    for i in idx:
        x, y = float(xs[i]), float(ys[i])
        L = rng.uniform(*col_len)
        items.append(([(x, y), (x + rng.uniform(-1.2, 1.2), y + L)], rng.uniform(0.8, 1.6), (0.1, 0.6)))
    return strokes(W, H, items) * roof


if "lingko" in PARTS:
    W = H = 700
    cx, cy = 350, 350
    nx = Seq(51100); rng = random.Random(11)
    art = blank(W, H)
    R0 = 312
    # irregular outer boundary
    ang_n = 180
    bound = []
    for i in range(ang_n):
        a = 2 * math.pi * i / ang_n
        r = R0 * (1 + 0.035 * math.sin(3 * a + 0.4) + 0.025 * math.sin(7 * a + 1.3) + 0.012 * math.sin(13 * a))
        bound.append(r)

    def rb(a):
        a %= 2 * math.pi
        f = a / (2 * math.pi) * ang_n
        i = int(f); t = f - i
        return bound[i % ang_n] * (1 - t) + bound[(i + 1) % ang_n] * t

    disc = shapes(W, H, [[(cx + math.cos(2 * math.pi * i / ang_n) * bound[i], cy + math.sin(2 * math.pi * i / ang_n) * bound[i]) for i in range(ang_n)]])
    # earth / bund base
    art = GP(art, disc, "#6f6a35", "#57582c", seed=nx(), rough=2.5, streak=0.6)
    # spokes
    spokes = []
    a = rng.uniform(0, 0.2)
    while a < 2 * math.pi - 0.08:
        spokes.append(a)
        a += rng.uniform(0.13, 0.26)
    rings = [0.36, 0.55, 0.72, 0.87, 1.0]
    classes = {
        "young": ("#9cc25c", "#86b04c"), "deep": ("#5f9341", "#4f8238"), "ripe": ("#c2bf5c", "#adab4a"),
        "gold": ("#d6b456", "#c29c40"), "water": ("#b7cfc4", "#9dbbb2"), "fallow": ("#a88a55", "#8f7445"),
    }
    order = ["young", "deep", "ripe", "young", "deep", "gold", "young", "water", "deep", "young", "ripe", "young"]
    cells = {k: [] for k in classes}
    gap_a = 0.012
    for si in range(len(spokes)):
        a0 = spokes[si] + gap_a
        a1 = (spokes[(si + 1) % len(spokes)] if si + 1 < len(spokes) else spokes[0] + 2 * math.pi) - gap_a
        base = order[(si * 3 + rng.randint(0, 2)) % len(order)]
        jit = [rng.uniform(-0.03, 0.03) for _ in rings]
        bounds = [0] + [ri for ri in range(1, len(rings) - 1) if rng.random() < 0.45] + [len(rings) - 1]
        for bi in range(len(bounds) - 1):
            ri, ro = bounds[bi], bounds[bi + 1]
            r_in = rings[ri] + (jit[ri] if ri else 0); r_out = rings[ro] + (jit[ro] if ro < len(rings) - 1 else 0)
            k = base if rng.random() < 0.6 else rng.choice(order)
            n = max(4, int((a1 - a0) * 26))
            outer = [(cx + math.cos(a0 + (a1 - a0) * t / n) * (rb(a0 + (a1 - a0) * t / n) * r_out - 4), cy + math.sin(a0 + (a1 - a0) * t / n) * (rb(a0 + (a1 - a0) * t / n) * r_out - 4)) for t in range(n + 1)]
            inner = [(cx + math.cos(a1 - (a1 - a0) * t / n) * (rb(a1) * r_in + 4), cy + math.sin(a1 - (a1 - a0) * t / n) * (rb(a1) * r_in + 4)) for t in range(n + 1)]
            cells[k].append(outer + inner)
    allcells = np.zeros((H, W), np.float32)
    for k, polys in cells.items():
        if not polys:
            continue
        m = shapes(W, H, polys, smooth=False)
        allcells = np.maximum(allcells, m)
        art = GP(art, m, *classes[k], seed=nx(), rough=1.6, streak=0.9)
        clear()
    # planted rows: concentric lines inside the cells
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.hypot(xx - cx, yy - cy) + (fbm(W, H, 7, 50, 2) - 0.5) * 6
    rows = np.clip((np.cos(2 * math.pi * rr / 5.5) - 0.55) * 3, 0, 1) * allcells
    art = G(art, rows, "#3d6a2b", seed=nx(), density=0.32, edge=0.0, bloom=0.0, gran=0.3, rough=1.0, feather=0.4)
    # water cells catch the sky: pale streaks
    wm = shapes(W, H, cells["water"], smooth=False)
    art = G(art, wm * fbm(W, H, 9, 30, 3), "#e6efe9", seed=nx(), density=0.5, edge=0, bloom=0.4, rough=2)
    # sun from the upper-left: soft shade on the lower-right of the disc
    shade = disc * np.clip(((xx - cx) * 0.6 + (yy - cy) * 0.8) / R0, 0, 1) ** 1.4
    art = G(art, shade, "#3c4a2a", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=4, feather=8)
    clear()
    # lodok centre (the photo sits over it): dark earth ring
    lod = circles(W, H, [(cx, cy, R0 * 0.36 + 2)])
    art = GP(art, lod, "#4b4325", "#3a3520", seed=nx(), rough=2)
    art = G(art, ring_mask(W, H, cx, cy, R0 * 0.36 - 6, 3), "#d9c58a", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1.5)
    # tree clumps on part of the rim
    clumps = []
    for i in range(70):
        a = rng.uniform(0, 2 * math.pi)
        if 0.6 < a < 2.2:  # keep the lower side open
            continue
        r = rb(a) + rng.uniform(-6, 14)
        clumps.append((cx + math.cos(a) * r, cy + math.sin(a) * r, rng.uniform(7, 16)))
    cm = circles(W, H, clumps)
    art = GP(art, cm, "#2f5a2c", "#24452a", seed=nx(), rough=3.5, streak=0.4)
    art = G(art, circles(W, H, [(x - r * 0.3, y - r * 0.3, r * 0.5) for x, y, r in clumps]), "#6f9a4a", seed=nx(), density=0.5, edge=0.2, rough=2)
    art = add_grain(art, seed=5, amount=0.035)
    preview(art, "ml-lingko", bg=BLACK)
    save_full(art, f"{OUT}/lingko.webp", size=(640, 640), quality=80)
    clear()

if "niang" in PARTS:
    W, H = 760, 440
    nx = Seq(51200); rng = random.Random(21)
    art = blank(W, H)
    # sky wash (fades to transparent at the top so it melts into the paper)
    sky = np.clip(np.linspace(0, 1, H)[:, None] * 2.2 - 0.15, 0, 1) * np.ones((1, W))
    art = G(art, sky.astype(np.float32) * 0.6, "#cfdcd4", "#e7e2cf", seed=nx(), density=0.5, edge=0, bloom=0.5, rough=6, pad=0)
    # mountain layers, far to near, with mist between
    layers = [(170, 90, 0.35, "#9fb3b0", "#8aa2a2", 3), (215, 80, 0.5, "#6f8e84", "#5d7d72", 7), (262, 60, 0.7, "#4c7556", "#3d6447", 11)]
    for y, amp, wl, c1, c2, sd in layers:
        m = hills(W, H, y, amp, sd, wl)
        art = G(art, m, c1, c2, seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=6)
        mist = np.clip(1 - np.abs(np.linspace(0, H, H)[:, None] - (y + amp * 0.35)) / 26, 0, 1) * np.ones((1, W))
        art = G(art, (mist * fbm(W, H, sd + 40, 90, 3)).astype(np.float32), "#f4f1e6", seed=nx(), density=0.7, edge=0, bloom=0.3, rough=8, feather=6)
        clear()
    # forest texture on the near ridge: dabs
    dabs = [(rng.uniform(0, W), rng.uniform(250, 330), rng.uniform(5, 11)) for _ in range(260)]
    dm = circles(W, H, dabs) * hills(W, H, 262, 60, 11, 0.7)
    art = G(art, dm, "#2c5236", seed=nx(), density=0.55, edge=0.5, bloom=0.1, rough=2)
    # clearing (grass) — a soft oval meadow
    meadow = shapes(W, H, [[(-30, 350)] + [(x, 318 + 10 * math.sin(x / 120) - 30 * math.exp(-((x - 380) / 260) ** 2)) for x in range(-30, W + 31, 20)] + [(W + 30, H + 20), (-30, H + 20)]], smooth=False)
    art = GP(art, meadow, "#93ad62", "#7c9852", seed=nx(), rough=2.5, streak=1.1)
    art = G(art, meadow * np.clip((np.linspace(0, 1, H)[:, None] - 0.8) * 4, 0, 1), "#5d7f3c", seed=nx(), density=0.5, edge=0, rough=5, feather=5)
    clear()
    # seven cone houses arranged in a shallow arc (back ones smaller)
    houses = [(110, 330, 96, 70), (215, 316, 104, 76), (318, 308, 112, 82), (430, 312, 120, 88), (540, 320, 108, 80), (640, 334, 98, 72), (372, 372, 150, 110)]
    for (hx, by, h, w) in sorted(houses, key=lambda t: t[1]):
        roof, bands, door, posts, fin = cone_house(W, H, hx, by, h, w, rng)
        art = G(art, ellipses(W, H, [(hx + 8, by + 4, w * 0.62, h * 0.07, 0)]), "#3f5a2a", seed=nx(), density=0.5, edge=0, bloom=0, rough=2, feather=3)
        art = GP(art, posts, "#4a3624", seed=nx(), rough=0.6, pad=6)
        art = GP(art, roof, "#b98e55", "#8f6a3c", seed=nx(), rough=1.4, streak=1.2)
        art = G(art, thatch(W, H, roof, rng, n=int(h * 6)), "#5e4126", seed=nx(), density=0.45, edge=0, bloom=0, gran=0.2, rough=0.6, feather=0.4)
        # light from the left: shade the right half
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        art = G(art, roof * np.clip((xx - hx) / (w * 0.5), 0, 1), "#5a3e22", seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1.5, feather=2)
        art = G(art, roof * np.clip((hx - xx) / (w * 0.5) - 0.3, 0, 1), "#f0d9a6", seed=nx(), density=0.4, edge=0, bloom=0.2, rough=1.5, feather=2)
        art = G(art, bands, "#4a321c", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.5)
        art = GP(art, door, "#2b2117", seed=nx(), rough=0.5, pad=6)
        art = GP(art, fin, "#3a2a1c", seed=nx(), rough=0.4, pad=6)
        clear()
    # foreground grass tufts + a few wildflowers
    tufts = []
    for x in range(0, W, 14):
        by = H - rng.uniform(4, 36)
        for k in range(3):
            a = -math.pi / 2 + rng.uniform(-0.5, 0.5)
            tufts.append(([(x + rng.uniform(-4, 4), by), (x + math.cos(a) * 22, by + math.sin(a) * 26)], 2.2, (0.0, 0.8)))
    art = GP(art, strokes(W, H, tufts), "#5f8a3e", "#486f33", seed=nx(), rough=0.8)
    art = GP(art, circles(W, H, [(rng.uniform(0, W), H - rng.uniform(14, 40), rng.uniform(2, 3.5)) for _ in range(40)]), "#e8c547", "#e08a2c", seed=nx(), rough=0.5)
    art = add_grain(art, seed=7, amount=0.03)
    preview(art, "ml-niang")
    save(art, f"{OUT}/niang.webp", max_w=720, quality=80)
    clear()


def songke_motifs(W, H, rows):
    """rows: list of (y0, y1, kind, colour) — periodic geometric motif masks in a W x H tile."""
    out = []
    for (y0, y1, kind, col) in rows:
        cv = Canvas(W, H)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        hh = y1 - y0; mid = (y0 + y1) / 2
        if kind == "stripe":
            cv.c.drawRect(skia.Rect(0, y0, W, y1), p)
        elif kind == "diamond":
            step = hh * 1.6
            n = int(round(W / step)); step = W / n
            for i in range(-1, n + 1):
                x = i * step + step / 2
                cv.c.drawPath(poly_path([(x, y0), (x + step * 0.42, mid), (x, y1), (x - step * 0.42, mid)]), p)
        elif kind == "eye":  # mata manuk: diamond with hollow centre
            step = hh * 2.0
            n = int(round(W / step)); step = W / n
            for i in range(-1, n + 1):
                x = i * step + step / 2
                cv.c.drawPath(poly_path([(x, y0), (x + step * 0.46, mid), (x, y1), (x - step * 0.46, mid)]), p)
            q = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK, BlendMode=skia.BlendMode.kClear)
            for i in range(-1, n + 1):
                x = i * step + step / 2
                cv.c.drawPath(poly_path([(x, y0 + hh * 0.28), (x + step * 0.2, mid), (x, y1 - hh * 0.28), (x - step * 0.2, mid)]), q)
        elif kind == "zigzag":
            step = hh * 1.4
            n = int(round(W / step)); step = W / n
            pts = []
            for i in range(-1, n + 2):
                pts.append((i * step, y1 if i % 2 else y0))
            sp = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.6, hh * 0.32))
            path = skia.Path(); path.moveTo(*pts[0])
            for pt in pts[1:]:
                path.lineTo(*pt)
            cv.c.drawPath(path, sp)
        elif kind == "dots":
            step = hh * 1.8
            n = int(round(W / step)); step = W / n
            for i in range(n + 1):
                cv.c.drawRect(skia.Rect(i * step + step * 0.3, y0, i * step + step * 0.7, y1), p)
        elif kind == "spider":  # ranggong: an x-cross with a hollow box centre
            step = hh * 2.2
            n = int(round(W / step)); step = W / n
            sp = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, hh * 0.16))
            for i in range(-1, n + 1):
                x = i * step + step / 2
                cv.c.drawLine(x - step * 0.4, y0, x + step * 0.4, y1, sp); cv.c.drawLine(x - step * 0.4, y1, x + step * 0.4, y0, sp)
                cv.c.drawRect(skia.Rect(x - hh * 0.22, mid - hh * 0.22, x + hh * 0.22, mid + hh * 0.22), p)
        out.append((cv.array()[..., 3], col))
    return out


def weave_render(W, H, rows, ground=BLACK, seed=1, period=(3.0, 4.0)):
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(ground), np.float32)
    th = threads(W, H, period[0], period[1], seed, 0.18)
    rgb = base.copy()
    for k, (m, col) in enumerate(songke_motifs(W, H, rows)):
        m = np.clip(periodic_blur(m, 0.6) * 1.2, 0, 1)
        c = np.array(hex_rgb(col), np.float32)
        # stepped (woven) edges: quantise the mask to the thread grid
        tone = 0.9 + 0.2 * wrap_noise(W, H, seed + k * 7, 6)
        rgb = rgb * (1 - m[..., None]) + (c * tone[..., None]) * m[..., None]
    rgb *= th[..., None]
    # faint fuzz / sheen
    rgb = np.clip(rgb * (0.96 + 0.08 * wrap_noise(W, H, seed + 99, 0.7))[..., None], 0, 1)
    return np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)


if "songke" in PARTS:
    W, H = 384, 72
    S = SONG
    rows = [
        (2, 5, "stripe", S["y"]), (7, 9, "stripe", S["r"]),
        (12, 22, "zigzag", S["g"]),
        (25, 47, "eye", S["r"]), (31, 41, "diamond", S["y"]),
        (50, 60, "spider", S["w"]),
        (63, 65, "stripe", S["r"]), (67, 70, "stripe", S["y"]),
    ]
    art = weave_render(W, H, rows, seed=3)
    preview(art, "ml-songke")
    save_full(art, f"{OUT}/songke.webp", quality=84)

if "weave" in PARTS:
    W, H = 192, 192
    rows = [(0, 1, "stripe", "#211a14")]
    art = weave_render(W, H, rows, ground="#1a1510", seed=9, period=(3.0, 3.0))
    # very sparse woven specks (supplementary weft)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    speck = ((xx % 48 < 6) & (yy % 48 < 3) & (((xx // 48) + (yy // 48)) % 2 == 0)).astype(np.float32)
    art[..., :3] = art[..., :3] * (1 - speck[..., None] * 0.6) + np.array(hex_rgb("#7a3a26"), np.float32) * speck[..., None] * 0.6
    save_rgb(art, f"{OUT}/weave.webp", quality=72)

if "cone" in PARTS:
    W, H = 240, 260
    nx = Seq(51300); rng = random.Random(31)
    art = blank(W, H)
    roof, bands, door, posts, fin = cone_house(W, H, 120, 232, 200, 160, rng)
    art = G(art, ellipses(W, H, [(126, 236, 100, 10, 0)]), "#6d7a3a", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=2, feather=2)
    art = GP(art, posts, "#4a3624", seed=nx(), rough=0.6)
    art = GP(art, roof, "#c39a5e", "#93703f", seed=nx(), rough=1.4, streak=1.2)
    art = G(art, thatch(W, H, roof, rng, n=1100), "#5e4126", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, roof * np.clip((xx - 120) / 80, 0, 1), "#5a3e22", seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1.5, feather=2)
    art = G(art, roof * np.clip((120 - xx) / 80 - 0.3, 0, 1), "#f3dfae", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1.5, feather=2)
    art = G(art, bands, "#4a321c", seed=nx(), density=0.65, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = GP(art, door, "#2b2117", seed=nx(), rough=0.5)
    art = GP(art, fin, "#3a2a1c", seed=nx(), rough=0.4)
    preview(art, "ml-cone")
    save(art, f"{OUT}/cone.webp", max_w=120, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 384, 30
    S = SONG
    rows = [(3, 5, "stripe", S["y"]), (8, 22, "eye", S["r"]), (11, 19, "diamond", S["y"]), (25, 27, "stripe", S["y"])]
    band = weave_render(W, H, rows, seed=13)
    # taper into a sash: fade both ends with a cut chevron
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(xx, W - 1 - xx) - np.abs(yy - H / 2) * 0.9
    band[..., 3] = np.clip(d / 2, 0, 1)
    save(band, f"{OUT}/divider.webp", max_w=384, quality=84)

kb(OUT)
