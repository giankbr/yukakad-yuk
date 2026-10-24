"""Pasar Terapung — dawn floating market on the Martapura in wet watercolour: apricot sun in river mist, stilt houses
and trees dissolving on the far bank, small jukung with sellers in wide tanggui hats, one big foreground jukung
heaped with oranges, bananas, rambutan and greens (separate asset so it can bob), a tanggui emblem, a fruit bakul and
a river-ripple divider. Palette: apricot, river jade, mist lilac, wood umber + fruit accents.
Run: python3 -I pasar-terapung.py [part ...]   parts: sungai jukung tanggui bakul riak"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s1_lib import *
from scipy.ndimage import map_coordinates

OUT = outdir("pasar-terapung")
PARTS = sys.argv[1:] or ["sungai", "jukung", "tanggui", "bakul", "riak"]
PAPER = "#f7ead9"
WOOD, WOOD_D, WOOD_L = "#5b3a24", "#3b2416", "#9a6a43"
JADE, JADE_D = "#6d9188", "#3f6560"
MIST = "#d9cdd3"
STRAW, STRAW_D = "#e2bf78", "#a77e3e"
SHIRTS = ["#3f4f86", "#8a2f3a", "#4f7a54", "#6b3f6e", "#b4602d", "#2f5d6e"]
SKIN = "#9a6440"


def reflect(layer, axis_y, squash=0.8, strength=0.45, seed=1, tintc="#a9bdb6"):
    h, w = layer.shape[:2]
    out = blank(w, h)
    yy, xx = yx(w, h)
    d = yy - axis_y
    src_y = axis_y - d / squash
    rip = (fbm(w, h, seed, 9, 2) - 0.5) * 9 * np.clip(d / 50, 0, 1) + np.sin(yy * 0.85) * 1.4
    for c in range(4):
        out[..., c] = map_coordinates(layer[..., c], [src_y, xx + rip], order=1, mode="constant")
    fade = np.clip(1 - d / (h - axis_y + 1), 0, 1) ** 0.8 * (d > 0)
    out[..., 3] *= fade * strength
    out[..., :3] = out[..., :3] * 0.8 + np.array(hex_rgb(tintc), np.float32) * 0.2
    return out


def hull_pts(x0, x1, y, depth, rise=0.35):
    """Jukung: long, low dugout; both ends taper and lift a little."""
    L = x1 - x0
    top = [(x0 - L * 0.03, y - depth * rise * 1.4), (x0 + L * 0.08, y - depth * 0.05), (x0 + L * 0.5, y + depth * 0.06),
           (x1 - L * 0.08, y - depth * 0.05), (x1 + L * 0.03, y - depth * rise * 1.6)]
    bot = [(x1 - L * 0.06, y + depth * 0.7), (x0 + L * 0.5, y + depth * 1.05), (x0 + L * 0.06, y + depth * 0.7)]
    return top + bot


def tanggui_masks(W, H, cx, cy, r):
    """Wide shallow conical hat seen from the side-front: brim ellipse + low cone + small knob. Returns (hat, weave)."""
    brim = ell(W, H, cx, cy, r, r * 0.2)
    cone = poly(W, H, [(cx - r * 0.82, cy - r * 0.02), (cx - r * 0.1, cy - r * 0.36), (cx + r * 0.1, cy - r * 0.36), (cx + r * 0.82, cy - r * 0.02)], smooth=True)
    knob = ell(W, H, cx, cy - r * 0.37, r * 0.09, r * 0.05)
    hat = np.maximum(np.maximum(brim, cone), knob)
    rays = []
    for k in range(13):
        t = -0.8 + 1.6 * k / 12
        rays.append(([(cx + t * r * 0.08, cy - r * 0.33), (cx + t * r * 0.98, cy + r * 0.04)], max(0.6, r * 0.022), None))
    rings = [(arc_pts(cx, cy - r * 0.02, r * f, math.pi * 1.04, math.pi * 1.96, 22, 0.32), max(0.6, r * 0.02), None) for f in (0.45, 0.7, 0.92)]
    weave = strokes(W, H, rays + rings) * hat
    return hat, weave


def seller(art, W, H, x, base, s, rng, nx, shirt, paddle=0, fade=1.0):
    """Seated seller: body + shoulders, arm, small head under a tanggui hat. base = seat line (gunwale)."""
    bw, bh = 15 * s, 20 * s
    body = poly(W, H, [(x - bw, base), (x - bw * 0.9, base - bh * 0.6), (x - bw * 0.55, base - bh), (x + bw * 0.55, base - bh),
                       (x + bw * 0.9, base - bh * 0.6), (x + bw, base)], smooth=True)
    head = ell(W, H, x + s * 1.5, base - bh - 5.5 * s, 5.2 * s, 6 * s)
    art = G(art, head * fade, SKIN, "#7e4e30", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1.0, feather=0.6)
    art = G(art, body * fade, shirt, mix(shirt, "#000000", 0.25), seed=nx(), density=0.9, edge=0.5, bloom=0.25, rough=1.6, feather=0.7)
    if paddle:
        d = paddle
        pad = line(W, H, [(x + d * 4 * s, base - bh * 0.9), (x + d * 26 * s, base + 30 * s)], 2.2 * s, None)
        blade_m = ell(W, H, x + d * 27 * s, base + 30 * s, 3.2 * s, 9 * s, -d * 30)
        art = G(art, np.maximum(pad, blade_m) * fade, WOOD_D, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.8, feather=0.5)
        arm = line(W, H, [(x + d * 6 * s, base - bh * 0.8), (x + d * 12 * s, base - bh * 0.35), (x + d * 9 * s, base - bh * 0.05)], 4.2 * s, (0.1, 0.2))
        art = G(art, arm * fade, mix(shirt, "#000000", 0.15), seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1, feather=0.5)
    hat, weave = tanggui_masks(W, H, x + s * 1.5, base - bh - 9 * s, 19 * s)
    art = G(art, hat * fade, STRAW, "#d4a95c", seed=nx(), density=0.92, edge=0.55, bloom=0.2, rough=1.4, feather=0.6)
    art = G(art, weave * fade, STRAW_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.4)
    # shade under the brim
    sh = ell(W, H, x + s * 1.5, base - bh - 6.5 * s, 13 * s, 3 * s) * head
    art = G(art, sh * fade, "#5a3520", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=1)
    return art


def fruits(art, W, H, items, col, col_d, nx, fade=1.0, hi="#fff3d6"):
    """Round fruit painted opaque-ish with a shadow crescent (lower left) and a small highlight (upper right)."""
    if not items:
        return art
    base = circles(W, H, items)
    art = OV(art, base * fade, lambda m: pigment(m, col, mix(col, col_d, 0.3), seed=nx(), density=0.97, edge=0.5, bloom=0.1, gran=0.15, rough=0.7, feather=0.5))
    shade = np.clip(base - circles(W, H, [(x + r * 0.3, y - r * 0.3, r * 0.92) for x, y, r in items]), 0, 1)
    art = G(art, shade * fade, col_d, seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.5, feather=0.8)
    hl = circles(W, H, [(x + r * 0.35, y - r * 0.38, r * 0.22) for x, y, r in items])
    art = over(art, rgba(hi, gaussian_filter(hl, 0.8) * 0.75 * fade))
    return art


def heap(x0, x1, yb, r, rows, rng):
    """Stacked rows of fruit (top rows first so lower/front rows overlap them)."""
    out = []
    for i in range(rows - 1, -1, -1):
        span = (x1 - x0) * (1 - i * 0.22)
        cx = (x0 + x1) / 2 + rng.uniform(-r * .3, r * .3)
        n = max(1, int(span / (r * 1.85)))
        row = []
        for k in range(n):
            x = cx - span / 2 + r + k * (span - 2 * r) / max(1, n - 1) + rng.uniform(-r * .12, r * .12)
            row.append((x, yb - r * 0.95 - i * r * 1.45 + rng.uniform(-r * .1, r * .1), r * rng.uniform(.9, 1.08)))
        out.append(row)
    return out


def bananas(art, W, H, x, yb, s, rng, nx, fade=1.0, n=6):
    """A hand of bananas: separate curved fingers fanning up from a dark crown, each with its own wet edge."""
    for k in range(n):
        t = (k - (n - 1) / 2) / max(1, (n - 1) / 2)
        cx = x + t * s * 0.32
        bend = 0.12 + 0.05 * abs(t)
        pts = curve([(x + t * s * 0.06, yb), (cx - s * bend * 0.6, yb - s * 0.5), (cx + t * s * 0.12 + s * 0.08, yb - s * 0.98)], 16)
        m = strokes(W, H, [(pts, s * 0.15, (0.12, 0.38))])
        art = OV(art, m * fade, lambda mm: pigment(mm, "#f2d35a", "#e0ae2e", seed=nx(), density=0.97, edge=0.9, bloom=0.1, gran=0.15, rough=0.6, feather=0.5))
        tip = circles(W, H, [(pts[-1][0], pts[-1][1], s * 0.035)])
        art = G(art, tip * fade, "#5b4a22", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.3, feather=0.4)
    crown = ell(W, H, x, yb - s * 0.02, s * 0.12, s * 0.07)
    art = G(art, crown * fade, "#6b6a2a", "#4d4a1e", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5, feather=0.5)
    return art


def greens(art, W, H, x0, x1, yb, hgt, rng, nx, fade=1.0):
    """Bundles of sawi / kangkung: narrow upright leaves in two greens with pale stems."""
    for shade, (ca, cb) in enumerate([("#5d8a35", "#3f6a28"), ("#86ad4a", "#6b9a3c")]):
        leaves, stems = [], []
        n = int((x1 - x0) / (hgt * 0.13)) + 2
        for k in range(n):
            x = x0 + (x1 - x0) * (k + 0.5 * shade) / max(1, n - 1) + rng.uniform(-3, 3)
            a = -math.pi / 2 + rng.uniform(-0.5, 0.5)
            L = hgt * rng.uniform(0.7, 1.0) * (1 - 0.2 * shade)
            leaves.append(petal_pts(x + math.cos(a) * L * 0.3, yb + math.sin(a) * L * 0.3, L * 0.75, L * 0.2, a, n=12))
            stems.append(([(x, yb), (x + math.cos(a) * L * 0.55, yb + math.sin(a) * L * 0.55)], hgt * 0.035, (0.0, 0.5)))
        lm = shapes(W, H, leaves)
        art = OV(art, lm * fade, lambda m: pigment(m, ca, cb, seed=nx(), density=0.95, edge=0.7, bloom=0.3, rough=1.0, feather=0.6))
        art = G(art, strokes(W, H, stems) * fade, "#d8e6a8", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5, feather=0.4)
    return art


def fruit_pile(art, W, H, x0, x1, y, hgt, rng, nx, fade=1.0, rich=1.0):
    """Cargo along a gunwale line y: a random mix of greens, oranges, limes, bananas and rambutan per boat."""
    kinds = ["greens", "oranges", "bananas", "rambutan", "limes"]
    rng.shuffle(kinds)
    segs = kinds[:rng.choice([2, 3, 3, 4])]
    if "oranges" not in segs and rng.random() < 0.6:
        segs[0] = "oranges"
    wts = [{"greens": 0.8, "oranges": 1.3, "bananas": 0.7, "rambutan": 0.8, "limes": 0.9}[k] * rng.uniform(.85, 1.15) for k in segs]
    tot = sum(wts); L = x1 - x0; x = x0; r = hgt * 0.16
    for k, wt in zip(segs, wts):
        sx1 = x + L * wt / tot
        if k == "greens":
            art = greens(art, W, H, x + 2, sx1 - 2, y + 2, hgt * 0.95, rng, nx, fade)
        elif k == "oranges":
            for row in heap(x, sx1, y + 2, r, 3 if sx1 - x > r * 6 else 2, rng):
                art = fruits(art, W, H, row, "#f08a22", "#b4501a", nx, fade)
        elif k == "limes":
            for row in heap(x, sx1, y + 2, r * 0.8, 2, rng):
                art = fruits(art, W, H, row, "#9cb33e", "#58702a", nx, fade, hi="#f4ffd0")
        elif k == "rambutan":
            for row in heap(x, sx1, y + 2, r * 0.72, 2, rng):
                art = fruits(art, W, H, row, "#cf3b2c", "#7d1d1a", nx, fade, hi="#ffd9c9")
        else:
            art = bananas(art, W, H, (x + sx1) / 2, y + 2, hgt * 1.0, rng, nx, fade, n=max(4, min(7, int((sx1 - x) / (hgt * 0.12)))))
        x = sx1
    return art


def jukung(art, W, H, x0, x1, y, depth, rng, nx, sellers=(), cargo=True, fade=1.0, rich=1.0):
    hull = poly(W, H, hull_pts(x0, x1, y, depth), smooth=True)
    L = x1 - x0
    if cargo:
        art = fruit_pile(art, W, H, x0 + L * 0.26, x1 - L * 0.1, y + depth * 0.1, depth * 3.2, rng, nx, fade, rich)
    for (fx, s, shirt, pd) in sellers:
        art = seller(art, W, H, x0 + L * fx, y + depth * 0.2, s, rng, nx, shirt, pd, fade)
    art = G(art, hull * fade, WOOD, WOOD_D, seed=nx(), density=0.95, edge=0.6, bloom=0.15, rough=1.2, feather=0.6)
    rim = line(W, H, [(p[0], p[1] + depth * 0.12) for p in hull_pts(x0, x1, y, depth)[:5]], max(1.2, depth * 0.16), (0.05, 0.05))
    art = G(art, rim * hull * fade, WOOD_L, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    return art


if "sungai" in PARTS:
    W, H = 800, 860
    HORIZON = 430
    rng = random.Random(161); nx = Seq(161000)
    yy, xx = yx(W, H)
    art = blank(W, H)
    # dawn sky wash: transparent at the very top, apricot near the horizon
    sky = np.clip((yy - 40) / 360, 0, 1) * (yy < HORIZON + 4)
    art = G(art, sky, "#f6c9a0", "#efb48a", seed=nx(), density=0.55, edge=0.05, bloom=0.5, rough=12, feather=10)
    art = G(art, sky * np.clip((yy - 250) / 160, 0, 1), "#f2a87e", seed=nx(), density=0.35, edge=0.05, bloom=0.5, rough=10, feather=8)
    # sun
    sun = circles(W, H, [(560, 352, 40)])
    art = over(art, glow(sun, "#ffe9c8", radius=40, strength=0.5))
    art = G(art, sun, "#f9c890", "#f6ad78", seed=nx(), density=0.6, edge=0.3, bloom=0.3, rough=2, feather=1.5)
    # far bank: tree masses, then a row of varied stilt houses, all lilac-grey in the mist
    trees = []
    for k in range(26):
        x = rng.uniform(-30, W + 30); r = rng.uniform(22, 46)
        trees.append((x, HORIZON - 30 - rng.uniform(0, 26), r))
    art = G(art, circles(W, H, trees) * (yy < HORIZON - 6), "#b7a9b2", "#aa9fae", seed=nx(), density=0.45, edge=0.3, bloom=0.5, rough=4, feather=2.5)
    crowns = []
    for x, y0, r in [(60, 120, 50), (110, 96, 40), (300, 70, 34), (470, 128, 56), (520, 100, 38), (690, 110, 48), (740, 84, 36)]:
        for _ in range(5):
            crowns.append((x + rng.uniform(-r * .6, r * .6), HORIZON - y0 + rng.uniform(-r * .3, r * .5), r * rng.uniform(.45, .7)))
    cm = circles(W, H, crowns)
    trunks = strokes(W, H, [([(x, HORIZON - 12), (x + rng.uniform(-4, 4), HORIZON - y0 + 20)], 4, (0.0, 0.5)) for x, y0, r in
                            [(60, 120, 0), (470, 128, 0), (690, 110, 0)]])
    art = G(art, np.maximum(cm, trunks) * (yy < HORIZON - 6), "#a99aa8", "#9c91a3", seed=nx(), density=0.5, edge=0.45, bloom=0.5, rough=4, feather=2)
    walls, roofs, wins, posts = [], [], [], []
    x = -30
    while x < W + 10:
        w = rng.uniform(56, 118); h = rng.uniform(24, 38); base = HORIZON - 10 - rng.uniform(0, 8); rh = h * rng.uniform(0.6, 0.85)
        walls.append([(x, base), (x, base - h), (x + w, base - h), (x + w, base)])
        roofs.append([(x - 7, base - h + 2), (x + w * .5, base - h - rh), (x + w + 7, base - h + 2)])
        for j in range(int(w // 26)):
            wx = x + 9 + j * 26
            wins.append([(wx, base - h * .7), (wx + 9, base - h * .7), (wx + 9, base - h * .3), (wx, base - h * .3)])
        posts += [([(px, base), (px, HORIZON + 6)], 2.4, None) for px in np.arange(x + 4, x + w, 14)]
        x += w + rng.uniform(4, 30)
    art = G(art, shapes(W, H, walls, smooth=False), "#b4a3a6", "#a89aa3", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=1.5, feather=0.8)
    art = G(art, shapes(W, H, roofs, smooth=False), "#8f7d8a", "#857688", seed=nx(), density=0.65, edge=0.45, bloom=0.3, rough=1.5, feather=0.8)
    art = G(art, shapes(W, H, wins, smooth=False), "#7d6f7e", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    art = G(art, strokes(W, H, posts), "#857888", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    # bank line
    art = G(art, band(W, H, HORIZON - 14, HORIZON + 2, 4), "#8a7f8a", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=3)
    # mist across the bank foot
    for (y, hh, amt) in [(HORIZON - 8, 26, 0.7), (HORIZON - 40, 22, 0.45)]:
        b = np.clip(1 - np.abs(yy - y) / hh, 0, 1) ** 1.4 * (0.5 + 0.5 * fbm(W, H, int(y) + 3, 80, 3))
        art[..., 3] *= 1 - b * amt
    land = art.copy()
    # river
    water = (yy > HORIZON).astype(np.float32)
    riv = G(blank(W, H), water, "#c3cfc2", "#aebfb4", seed=nx(), density=0.55, edge=0.05, bloom=0.2, rough=8, feather=4)
    riv = G(riv, water * np.clip((yy - HORIZON - 60) / 300, 0, 1), JADE, "#7c9b8f", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=8, feather=5)
    riv = glaze(riv, reflect(land, HORIZON, squash=0.9, strength=0.4, seed=nx()))
    # sun path on the water
    path = np.clip(1 - np.abs(xx - 560 - (yy - HORIZON) * 0.08) / (30 + np.abs(yy - HORIZON) * 0.25), 0, 1) * water * np.clip(1 - (yy - HORIZON) / 330, 0, 1)
    sp = []
    for _ in range(70):
        y = rng.uniform(HORIZON + 6, HORIZON + 320); x = 560 + (y - HORIZON) * 0.08 + rng.gauss(0, 18 + (y - HORIZON) * 0.15); L = rng.uniform(14, 50)
        sp.append(([(x - L / 2, y), (x + L / 2, y + rng.uniform(-.5, .5))], rng.uniform(1.5, 3.2), (0.3, 0.3)))
    riv = G(riv, strokes(W, H, sp) * np.clip(path * 2.5, 0, 1), "#f7c38e", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.6, feather=0.5)
    streaks = []
    for _ in range(60):
        y = rng.uniform(HORIZON + 20, H - 20); x0 = rng.uniform(-40, W); L = rng.uniform(40, 200)
        streaks.append(([(x0, y), (x0 + L, y + rng.uniform(-1, 1))], rng.uniform(1.0, 2.4), (0.3, 0.3)))
    sm = strokes(W, H, streaks) * water
    riv[..., 3] *= 1 - sm * 0.5
    art = over(riv, land)
    # boats: far (small, misty) -> mid
    far = [(60, 170, HORIZON + 24, 5, [(0.25, 0.42, SHIRTS[0], 1)], 0.5), (250, 350, HORIZON + 18, 4, [(0.7, 0.36, SHIRTS[1], -1)], 0.45),
           (640, 780, HORIZON + 30, 5, [(0.2, 0.46, SHIRTS[2], 1), (0.75, 0.42, SHIRTS[4], 0)], 0.5),
           (430, 540, HORIZON + 44, 6, [(0.8, 0.55, SHIRTS[3], -1)], 0.62), (150, 290, HORIZON + 58, 7, [(0.15, 0.62, SHIRTS[5], 1)], 0.7)]
    for x0, x1, y, d, sel, f in far:
        art = jukung(art, W, H, x0, x1, y, d, rng, nx, sellers=sel, cargo=True, fade=f, rich=0.7)
    # the crowded middle of the market: overlapping boats, back to front
    mid = [(330, 560, HORIZON + 92, 9, [(0.86, 0.8, SHIRTS[4], -1)]), (560, 790, HORIZON + 104, 9, [(0.14, 0.8, SHIRTS[0], 1)]),
           (-40, 210, HORIZON + 120, 10, [(0.2, 0.9, SHIRTS[3], 1)]), (180, 470, HORIZON + 150, 12, [(0.12, 1.0, SHIRTS[2], 1), (0.86, 0.95, SHIRTS[1], 0)]),
           (500, 820, HORIZON + 186, 13, [(0.82, 1.1, SHIRTS[5], -1)])]
    for x0, x1, y, d, sel in mid:
        refl = ell(W, H, (x0 + x1) / 2, y + d * 2.2, (x1 - x0) * 0.45, d * 1.1)
        art = G(art, refl, "#4e6a62", seed=nx(), density=0.3, edge=0.1, bloom=0.3, rough=3, feather=2)
        art = jukung(art, W, H, x0, x1, y, d, rng, nx, sellers=sel, cargo=True)
    # mist veil over the far boats
    b = np.clip(1 - np.abs(yy - (HORIZON + 26)) / 30, 0, 1) ** 1.6 * (0.45 + 0.55 * fbm(W, H, 77, 70, 3))
    art = over(art, rgba("#f3e6e3", b * 0.35))
    # top fade into the page sky; bottom dissolves softly
    art[..., 3] *= np.clip((yy - 30) / 140, 0, 1)
    art[..., 3] *= np.clip((H - 6 - yy) / 90, 0, 1)
    art = art[110:]
    preview(art, "pt-sungai", tone=PAPER)
    save_full(art, f"{OUT}/sungai.webp", size=(680, 637), quality=60)
    clear()

if "jukung" in PARTS:
    W, H = 860, 300
    rng = random.Random(162); nx = Seq(162000)
    art = blank(W, H)
    refl = ell(W, H, 430, 262, 380, 20)
    art = G(art, refl, "#4b6b62", "#5b7b72", seed=nx(), density=0.5, edge=0.2, bloom=0.4, rough=4, feather=2.5)
    art = jukung(art, W, H, 60, 800, 214, 34, rng, nx, sellers=[(0.12, 2.6, "#2f4f86", 1)], cargo=True, rich=1.5)
    rip = strokes(W, H, [(arc_pts(430, 236, rr, math.pi * 0.05, math.pi * 0.95, 30, 0.08), 2.2, (0.2, 0.2)) for rr in (400, 440)])
    art = G(art, rip, "#5d7f76", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=0.6)
    preview(art, "pt-jukung", tone="#cfd8cc")
    save(art, f"{OUT}/jukung.webp", max_w=640, quality=80)
    clear()

if "tanggui" in PARTS:
    W, H = 360, 200
    rng = random.Random(163); nx = Seq(163000)
    art = blank(W, H)
    hat, weave = tanggui_masks(W, H, 180, 120, 160)
    art = G(art, hat, STRAW, "#d6a75a", seed=nx(), density=0.92, edge=0.6, bloom=0.25, rough=2, feather=0.8)
    art = G(art, weave, STRAW_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8, feather=0.5)
    rimm = np.clip(ell(W, H, 180, 120, 160, 32) - ell(W, H, 180, 117, 152, 26), 0, 1)
    art = G(art, rimm, "#8f6430", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1, feather=0.5)
    preview(art, "pt-tanggui", tone=PAPER)
    save(art, f"{OUT}/tanggui.webp", max_w=240, quality=82)
    clear()

if "bakul" in PARTS:
    W, H = 420, 330
    rng = random.Random(164); nx = Seq(164000)
    art = blank(W, H)
    art = greens(art, W, H, 250, 350, 204, 150, rng, nx)
    art = bananas(art, W, H, 130, 204, 170, rng, nx, n=7)
    for row in heap(110, 300, 206, 26, 3, rng):
        art = fruits(art, W, H, row, "#f08a22", "#b4501a", nx)
    for row in heap(270, 360, 206, 17, 2, rng):
        art = fruits(art, W, H, row, "#cf3b2c", "#7d1d1a", nx, hi="#ffd9c9")
    basket = poly(W, H, [(52, 196), (368, 196), (330, 300), (90, 300)], smooth=False)
    art = G(art, basket, "#c99a55", "#a77a3c", seed=nx(), density=0.92, edge=0.6, bloom=0.2, rough=1.5, feather=0.7)
    weave = strokes(W, H, [([(52 + k * 14, 196), (90 + k * 11.6, 300)], 2.0, None) for k in range(24)] +
                    [([(52 + t * 0, 214 + j * 20), (368, 214 + j * 20)], 2.2, None) for j in range(5) for t in [0]]) * basket
    art = G(art, weave, "#7a5428", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8, feather=0.5)
    rimm = line(W, H, [(46, 196), (210, 192), (374, 196)], 9, (0.05, 0.05))
    art = G(art, rimm, "#8a5f2c", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=1, feather=0.5)
    preview(art, "pt-bakul", tone=PAPER)
    save(art, f"{OUT}/bakul.webp", max_w=280, quality=82)
    clear()

if "riak" in PARTS:
    W, H = 520, 70
    rng = random.Random(165); nx = Seq(165000)
    art = blank(W, H)
    wav = []
    for j, (y, a, wd) in enumerate([(30, 7, 3.0), (44, 5, 2.2)]):
        pts = [(x, y + math.sin(x / 26 + j) * a * (1 - abs(x - 260) / 300)) for x in range(20, 501, 6)]
        wav.append((pts, wd, (0.3, 0.3)))
    art = G(art, strokes(W, H, wav), JADE, JADE_D, seed=nx(), density=0.8, edge=0.4, bloom=0.2, rough=1.2, feather=0.6)
    fr = circles(W, H, [(260, 30, 10)])
    art = G(art, fr, "#ec8a2a", "#d4661c", seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=0.8, feather=0.5)
    lf = shape_mask(W, H, petal_pts(270, 22, 18, 7, -0.6, n=10))
    art = G(art, lf, "#5e7f39", seed=nx(), density=0.9, edge=0.4, bloom=0.1, rough=0.6, feather=0.5)
    preview(art, "pt-riak", tone=PAPER)
    save(art, f"{OUT}/riak.webp", max_w=360, quality=84)
    clear()
