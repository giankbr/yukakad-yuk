"""Sadu Tenun — Al Sadu Bedouin weaving, rendered as coarse warp-faced wool (original, inspired-by patterns; geometry
only, no figures): two broad bands (diamond "eyes" with combs; saw-tooth triangles), a narrow ticking band, a
diamond "eye" medallion, a cream wool field tile, a row of wrapped tassels and a goat-hair tent scene at dusk.
Run: python3 -I sadu-tenun.py [part ...]  parts: bandA bandB tick eye field tassels tent
Assets -> public/themes/art/sadu-tenun/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t3_lib import *

OUT = outdir("sadu-tenun")
PARTS = sys.argv[1:] or ["bandA", "bandB", "tick", "eye", "field", "tassels", "tent"]
BLACK, RED, IVORY, OCHRE, BROWN = "#1d1512", "#9a2622", "#ebe0c9", "#c4882c", "#5a3320"
PAL = [BLACK, RED, IVORY, OCHRE, BROWN]
K, R, I, O, B = 0, 1, 2, 3, 4
CELL = (6, 9)


def tick_rows(cols, a=K, b=I, n=2):
    return [[a if (c + r) % 2 == 0 else b for c in range(cols)] for r in range(n)]


def solid(cols, v, n=1):
    return [[v] * cols for _ in range(n)]


def diamond_zone(cols, rows, period=22, bg=R):
    g = [[bg] * cols for _ in range(rows)]
    cy = (rows - 1) / 2
    for c in range(cols):
        k = (c % period) - period / 2 + 0.5
        for r in range(rows):
            d = abs(k) / (period / 2 - 1) * cy + abs(r - cy)
            dd = abs(k) + abs(r - cy) * (period / 2 - 1) / cy
            if dd <= period / 2 - 1.5:
                ring = int(dd // 2.2)
                g[r][c] = [I, K, O, K, I, R][ring % 6]
            # combs: black teeth hanging from the top / rising from the bottom between the diamonds
            if abs(k) >= period / 2 - 2.5:
                pass
        # comb teeth at the diamond tips (between diamonds)
        kk = c % period
        if kk in (0, period - 1):
            for r in list(range(0, 3)) + list(range(rows - 3, rows)):
                g[r][c] = K
        if kk in (1, period - 2):
            for r in (0, rows - 1):
                g[r][c] = K
    # comb spines along top/bottom edges of the zone
    for c in range(cols):
        if c % period in (period // 2 - 3, period // 2 + 2):
            pass
    return g


def comb_row(cols, up=True, period=6, h=4, fg=K, bg=I):
    g = [[bg] * cols for _ in range(h)]
    for c in range(cols):
        for r in range(h):
            if r == (h - 1 if up else 0) or (c % period in (0, 2, 4) and True):
                g[r][c] = fg
    return g


def teeth(cols, h=8, period=12, a=R, b=K):
    g = [[a] * cols for _ in range(h)]
    for c in range(cols):
        k = c % period
        tri = k if k < period / 2 else period - 1 - k
        for r in range(h):
            if r >= h - 1 - int(tri * (h - 1) / (period / 2 - 1)):
                g[r][c] = b
    return g


def stack(*parts):
    out = []
    for p in parts:
        out += p
    return out


def render(grid, name, seed, max_w=780, q=80, prev_bg="#2a1f19"):
    art = weave(grid, PAL, CELL, seed=seed)
    preview(art, name, bg=prev_bg)
    return art


if "bandA" in PARTS:
    cols = 130
    g = stack(solid(cols, K), tick_rows(cols, K, I), solid(cols, O), solid(cols, R),
              diamond_zone(cols, 15), solid(cols, R), solid(cols, O), tick_rows(cols, K, I), solid(cols, K))
    art = render(g, "sd-bandA", 11)
    save_full(art, f"{OUT}/bandA.webp", quality=78)
    clear()

if "bandB" in PARTS:
    cols = 130
    up = teeth(cols, 7, 14, I, R)
    down = [row[:] for row in reversed(teeth(cols, 7, 14, K, R))]
    g = stack(solid(cols, B), tick_rows(cols, R, I), solid(cols, K), up, down, solid(cols, K), tick_rows(cols, R, I), solid(cols, B))
    art = render(g, "sd-bandB", 21)
    save_full(art, f"{OUT}/bandB.webp", quality=78)
    clear()

if "tick" in PARTS:
    cols = 130
    g = stack(solid(cols, R), tick_rows(cols, K, I, 2), solid(cols, O), tick_rows(cols, K, I, 2), solid(cols, R))
    art = render(g, "sd-tick", 31)
    save_full(art, f"{OUT}/tick.webp", quality=78)
    clear()

if "eye" in PARTS:
    n = 21
    g = [[R] * n for _ in range(n)]
    c0 = (n - 1) / 2
    for r in range(n):
        for c in range(n):
            d = abs(r - c0) + abs(c - c0)
            if d <= c0:
                g[r][c] = [K, I, O, I, K, R, K, I, R, I, K][int(d) % 11]
    # crop to the diamond by alpha
    art = weave(g, PAL, (6, 6), seed=41)
    h, w = art.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dm = (np.abs(xx - w / 2) / (w / 2) + np.abs(yy - h / 2) / (h / 2)) <= 1.0
    art[..., 3] = gaussian_filter(dm.astype(np.float32), 0.8)
    preview(art, "sd-eye", bg="#ebe0c9")
    save(art, f"{OUT}/eye.webp", max_w=126, quality=82)
    clear()

if "field" in PARTS:
    cols, rows = 40, 28
    rng = np.random.default_rng(5)
    g = [[I] * cols for _ in range(rows)]
    for c in range(cols):
        if c % 20 == 9:
            for r in range(rows):
                g[r][c] = O if (r // 2) % 2 == 0 else I
    art = weave(g, PAL, CELL, seed=51, fuzz=0.35, gap=0.22)
    art[..., :3] = art[..., :3] * 0.55 + np.array(hex_rgb("#f3eadb"), np.float32) * 0.45
    save_full(art, f"{OUT}/field.webp", quality=74)
    clear()

if "tassels" in PARTS:
    W, H = 780, 190
    nx = Seq(600); rng = random.Random(6)
    art = blank(W, H)
    cols_ = [RED, BLACK, OCHRE, RED, IVORY]
    n = 11
    for i in range(n):
        x = 30 + i * (W - 60) / (n - 1)
        col = cols_[i % len(cols_)]
        strands = []
        for k in range(16):
            dx = (k - 7.5) * 1.7
            sway = rng.uniform(-6, 6)
            pts = curve([(x + dx * 0.5, 24), (x + dx, 70), (x + dx * 1.6 + sway * 0.5, 120), (x + dx * 2.0 + sway, 176 + rng.uniform(-8, 6))], 16)
            strands.append((pts, rng.uniform(1.6, 2.6), (0.02, 0.15)))
        sm = strokes(W, H, strands)
        art = GP(art, sm, col, mix(col, "#ffffff", 0.18), seed=nx(), rough=0.6, streak=0.8)
        art = G(art, inner_shade(sm, 2, 0, 2), mix(col, "#000000", 0.45), seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5)
        # wrapped head + binding
        head = shapes(W, H, [ellipse_pts(x, 30, 9, 17, 12)])
        art = GP(art, head, col, mix(col, "#000000", 0.2), seed=nx(), rough=0.6, streak=0.8)
        wrap = strokes(W, H, [([(x - 10, y), (x + 10, y + 1.5)], 1.6, None) for y in range(18, 46, 4)]) * head
        art = G(art, wrap, mix(col, "#000000", 0.5), seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
        bind = strokes(W, H, [([(x - 9, 48), (x + 9, 48)], 5, None)])
        art = GP(art, bind, OCHRE if col != OCHRE else RED, seed=nx(), rough=0.5, streak=0.6)
        cord = strokes(W, H, [([(x, 0), (x, 16)], 3, None)])
        art = GP(art, cord, BLACK, seed=nx(), rough=0.4, streak=0.5)
    preview(art, "sd-tassels", bg="#2a1f19")
    save_full(art, f"{OUT}/tassels.webp", quality=80)
    clear()

if "tent" in PARTS:
    W, H = 780, 460
    nx = Seq(800); rng = random.Random(8)
    art = blank(W, H)
    # dunes
    d1 = hills(W, H, 360, 24, nx(), 0.9)
    art = GP(art, d1, "#d79a52", "#e7b36e", seed=nx(), rough=1.5, streak=0.7)
    d2 = hills(W, H, 392, 18, nx(), 0.6)
    art = GP(art, d2, "#c2803f", "#d4945a", seed=nx(), rough=1.5, streak=0.7)
    # tent body: long low black goat-hair tent with peaks over the poles
    ridge = [(110, 380), (130, 250)]
    peaks = [(220, 190), (390, 172), (560, 190)]
    sag = [(305, 222), (475, 222)]
    top = [(130, 250), peaks[0], sag[0], peaks[1], sag[1], peaks[2], (650, 250), (672, 380)]
    tent_pts = [(110, 380)] + curve(top, 80) + [(110, 380)]
    tm = shapes(W, H, [tent_pts], smooth=False)
    art = GP(art, tm, "#241a16", "#33261f", seed=nx(), rough=1.4, streak=1.0)
    # woven goat-hair strips (vertical panels)
    strips = []
    for x in range(140, 660, 34):
        strips.append(([(x, 170), (x + 2, 390)], 2.0, None))
    art = G(art, strokes(W, H, strips) * tm, "#4a3a30", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6)
    # open front: the sadu dividing curtain (qata) glimpsed inside
    door = shapes(W, H, [[(316, 382), (322, 270), (390, 246), (458, 270), (464, 382)]], smooth=False)
    g = stack(solid(30, K), tick_rows(30, K, I), solid(30, R), teeth(30, 6, 10, I, R), solid(30, O), tick_rows(30, R, I), solid(30, R), diamond_zone(30, 9, 10), solid(30, K))
    wv = weave(g, PAL, (6, 6), seed=81)
    hh, ww = wv.shape[:2]
    layer = blank(W, H)
    y0, x0 = 246, 300
    hh2, ww2 = min(hh, 136), min(ww, 180)
    layer[y0:y0 + hh2, x0:x0 + ww2] = wv[:hh2, :ww2]
    layer[..., 3] *= door
    art = over(art, layer)
    art = G(art, np.clip(gaussian_filter(door, 8) * door * 0 + inner_shade(door, 0, 14, 10), 0, 1), "#140d0a", seed=nx(), density=0.6, edge=0, bloom=0, rough=1)
    folds = []
    for x0_, x1_ in ((220, 250), (390, 360), (390, 420), (560, 530), (220, 190), (560, 590)):
        folds.append((curve([(x0_, 196), ((x0_ + x1_) / 2, 280), (x1_, 378)], 20), 7, (0.1, 0.3)))
    art = G(art, strokes(W, H, folds) * tm * (1 - door), "#5a4638", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=2)
    flap = strokes(W, H, [([(322, 270), (390, 246), (458, 270)], 6, None)])
    art = GP(art, flap, "#3a2b22", seed=nx(), rough=0.8, streak=0.6)
    # poles, guy ropes, pegs
    poles = [([(x, y), (x, 382)], 4, None) for x, y in (peaks[0], peaks[2])]
    art = GP(art, strokes(W, H, poles) * (1 - door), "#6a4a2e", seed=nx(), rough=0.6, streak=0.5)
    ropes = []
    for x, y in [(130, 250), peaks[0], peaks[2], (650, 250)]:
        tx = x - 110 if x < 390 else x + 110
        ropes.append((curve([(x, y), ((x + tx) / 2, (y + 400) / 2 + 6), (tx, 400)], 16), 1.4, None))
    art = G(art, strokes(W, H, ropes), "#3a2a20", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.4)
    preview(art, "sd-tent", bg="#e8b46a")
    save(art, f"{OUT}/tent.webp", max_w=780, quality=80)
    clear()
