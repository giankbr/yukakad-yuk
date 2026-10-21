"""Walimatus Safar — syukuran before hajj/umrah, green & gold: gouache arched landscape (morning sky, sage hills,
winding sand path with date palms), a small plane with its contrail (separate piece, animated), gold-foil pierced
lantern, foil khatam star, foil geometric band, deep-green lattice tile. No Kaaba, no figures.
Run: python3 -I walimatus-safar.py [part ...]  parts: path plane lamp star band velvet"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a4_lib import *

OUT = outdir("walimatus-safar")
PARTS = sys.argv[1:] or ["path", "plane", "lamp", "star", "band", "velvet"]
GOLD = "#c9a24e"
GREEN, GREEN_D = "#0f3b2e", "#082519"


def arch_poly(W, H, inset=0, n=40):
    """Round-topped arch (semicircle on a rectangle)."""
    r = W / 2 - inset
    top = [(W / 2 + math.cos(math.pi + math.pi * t) * r, r + inset + math.sin(math.pi + math.pi * t) * r) for t in [i / (n - 1) for i in range(n)]]
    return [(inset, H - inset)] + top + [(W - inset, H - inset)]


def date_palm(W, H, x, by, h, rng, lean=0.0):
    """Date palm masks: (trunk, crown, dates)."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.4, by - h * 0.5), top], 30)
    tr = strokes(W, H, [(trunk, h * 0.055, (0.0, 0.05))])
    items = []
    n = 14
    for k in range(n):
        a = -math.pi + 0.15 + (math.pi - 0.3) * k / (n - 1) + rng.uniform(-0.08, 0.08)
        L = h * rng.uniform(0.36, 0.48) * (0.75 if abs(a + math.pi / 2) < 0.4 else 1.0)
        droop = L * (0.35 + 0.5 * abs(math.cos(a)))
        pts = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - L * 0.12),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + droop)], 26)
        items.append((pts, h * 0.016, (0.05, 0.5)))
        for j in range(2, 25, 2):
            px, py = pts[j]; qx, qy = pts[j + 1]
            ang = math.atan2(qy - py, qx - px)
            ll = h * 0.095 * (1 - j / 32)
            for sd in (-1, 1):
                aa = ang + sd * 0.7 + 0.25
                items.append(([(px, py), (px + math.cos(aa) * ll, py + math.sin(aa) * ll + ll * 0.35)], h * 0.02, (0.1, 0.6)))
    crown = strokes(W, H, items)
    dates = circles(W, H, [(top[0] + rng.uniform(-h * 0.05, h * 0.05), top[1] + h * 0.04 + rng.uniform(0, h * 0.05), h * 0.011) for _ in range(18)])
    rings = strokes(W, H, [([(trunk[i][0] - h * 0.028, trunk[i][1] + 2), (trunk[i][0] + h * 0.028, trunk[i][1] - 3)], 1.4, None) for i in range(1, 29, 2)]) * tr
    return tr, crown, dates, rings


def star8(cx, cy, r, inner=0.72, rot=0.0):
    pts = []
    for k in range(16):
        a = rot + k * math.pi / 8
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


if "path" in PARTS:
    W, H = 600, 820
    nx = Seq(40100); rng = random.Random(4)
    HZ = 430
    art = painted_sky(W, H, [(0, "#bcd6c6"), (0.28, "#dbe6cf"), (0.5, "#f4e7c2"), (0.56, "#f7dcaa"), (1, "#f7dcaa")], seed=nx(), streak=0.6)
    # gouache clouds
    for (x, y, rx, ry) in [(140, 150, 90, 20), (210, 138, 60, 18), (450, 230, 110, 18), (520, 216, 50, 14), (90, 300, 70, 12)]:
        art = GP(art, shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 12), rng, 2, 0.1)]), "#fbf6ea", "#eef0e2", seed=nx(), rough=3, streak=0.8, density=0.85)
    # sun low on the horizon
    art = over(art, glow(circles(W, H, [(420, HZ - 20, 34)]), "#fff1c8", radius=40, strength=0.5))
    art = GP(art, circles(W, H, [(420, HZ - 20, 30)]), "#fff4d6", "#ffe6a8", seed=nx(), rough=1.2)
    # far mountains (rocky, sage-grey), near hills
    for (y, amp, wl, c1, c2, sd) in [(HZ - 10, 70, 0.6, "#a9b7a4", "#93a491", 5), (HZ + 6, 44, 0.45, "#8c9f86", "#74896f", 9)]:
        art = GP(art, hills(W, H, y, amp, sd, wl), c1, c2, seed=nx(), rough=2.5, streak=1.0)
    # sand plain
    plain = shapes(W, H, [[(-20, HZ + 20)] + [(x, HZ + 14 + 6 * math.sin(x / 60)) for x in range(-20, W + 21, 20)] + [(W + 20, H + 20), (-20, H + 20)]], smooth=False)
    art = GP(art, plain, "#e9cf9c", "#d9b57d", seed=nx(), rough=2, streak=1.2)
    # shading bands on the plain
    for k, (y, th) in enumerate([(HZ + 70, 10), (HZ + 150, 16), (HZ + 260, 22)]):
        pts = [(x, y + 8 * math.sin(x / 90 + k)) for x in range(-20, W + 20, 10)]
        art = G(art, strokes(W, H, [(pts, th, (0.2, 0.2))]), "#c99c62", seed=nx(), density=0.3, edge=0.3, bloom=0.2, rough=5, feather=3)
    # winding path towards the horizon (perspective: wide at the bottom)
    cpath = curve([(300, H + 30), (380, 700), (230, 590), (330, 500), (290, HZ + 20)], 120)
    L, R = [], []
    for i, (x, y) in enumerate(cpath):
        t = i / (len(cpath) - 1)
        wd = 120 * (1 - t) ** 1.6 + 4
        a, b = cpath[max(0, i - 1)], cpath[min(len(cpath) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        L.append((x - dy / d * wd, y + dx / d * wd)); R.append((x + dy / d * wd, y - dx / d * wd))
    path = shapes(W, H, [L + R[::-1]])
    art = GP(art, path, "#f8e8c4", "#f1d9a8", seed=nx(), rough=2.2, streak=0.9)
    edge = np.clip(gaussian_filter(path, 3) - path, 0, 1) * 3
    art = G(art, np.clip(edge, 0, 1), "#b88a55", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=2)
    # footprint-like pebbles along the path edges
    peb = []  # [(x + rng.uniform(-6, 6), y + rng.uniform(-3, 3), rng.uniform(1.5, 3.5) * (0.4 + (y - HZ) / 400)) for (x, y) in L[::6] + R[::6] if y > HZ + 40]
    # date palms beside the path
    for (x, by, h, lean) in [(110, 640, 230, 0.08), (70, 610, 180, -0.05), (500, 560, 160, -0.1), (470, 520, 110, 0.06), (190, 495, 70, 0.05)]:
        tr, crown, dates, rings = date_palm(W, H, x, by, h, rng, lean)
        art = GP(art, tr, "#7a5a3a", "#4f3a26", seed=nx(), rough=1.0, streak=0.8)
        art = G(art, rings, "#3a2a1a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4)
        art = GP(art, dates, "#b0602a", "#7a3a1a", seed=nx(), rough=0.6, pad=6)
        art = GP(art, crown, "#3a6a4c", "#1f4634", seed=nx(), rough=1.0, streak=0.8)
        art = G(art, ellipses(W, H, [(x, by + 2, h * 0.18, h * 0.03, 0)]), "#9c7448", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=2, feather=2)
    # foreground grass tufts
    tufts = []
    for x in list(range(10, 200, 26)) + list(range(420, 600, 24)):
        by = H - rng.uniform(10, 60)
        for k in range(5):
            a = -math.pi / 2 + rng.uniform(-0.6, 0.6)
            tufts.append(([(x, by), (x + math.cos(a) * 30, by + math.sin(a) * 36)], 3, (0.0, 0.8)))
    art = GP(art, strokes(W, H, tufts), "#6f8a55", "#4c6a40", seed=nx(), rough=0.8)
    art = add_grain(art, seed=3, amount=0.03)
    # cut to the arch and frame it with gold foil
    am = shape_mask(W, H, arch_poly(W, H, 10), smooth=False)
    art[..., 3] *= am
    frame = np.clip(shape_mask(W, H, arch_poly(W, H, 0), smooth=False) - shape_mask(W, H, arch_poly(W, H, 9), smooth=False), 0, 1)
    art = FO(art, frame, GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    inner = np.clip(shape_mask(W, H, arch_poly(W, H, 16), smooth=False) - shape_mask(W, H, arch_poly(W, H, 19), smooth=False), 0, 1)
    art = FO(art, inner, "#e6cf8f", seed=nx(), emboss=0.4, sparkle=0.05)
    preview(art, "ws-path", bg=GREEN)
    save(art, f"{OUT}/path.webp", max_w=560, quality=80)
    clear()

if "plane" in PARTS:
    W, H = 560, 260
    nx = Seq(40200)
    art = blank(W, H)
    trail = curve([(560, 250), (420, 190), (280, 120), (150, 78)], 60)
    art = G(art, strokes(W, H, [([(x, y + 4) for x, y in trail], 10, (0.85, 0.02))]), "#9fb6ad", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=4, feather=3)
    art = G(art, strokes(W, H, [(trail, 9, (0.85, 0.02))]), "#ffffff", "#f6f3ea", seed=nx(), density=0.95, edge=0.25, bloom=0.5, rough=4, feather=2.2)
    art = G(art, strokes(W, H, [([(x, y + 7) for x, y in trail], 5, (0.85, 0.05))]), "#ffffff", seed=nx(), density=0.5, edge=0.2, bloom=0.5, rough=4, feather=2)
    # small plane heading up-left
    px, py, ang = 128, 70, math.atan2(78 - 120, 150 - 280)
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (px + u * ca - v * sa, py + u * sa + v * ca)
    fus = [P(18, 0), P(12, -3), P(-20, -3), P(-24, 0), P(-20, 3), P(12, 3)]
    wings = [P(2, -2), P(-8, -22), P(-13, -22), P(-8, -2), P(-8, 2), P(-13, 22), P(-8, 22), P(2, 2)]
    tail = [P(-18, -2), P(-24, -9), P(-27, -9), P(-24, 0), P(-27, 9), P(-24, 9), P(-18, 2)]
    pm = shapes(W, H, [fus, wings, tail], smooth=False)
    art = GP(art, pm, "#f8f7f2", "#e3e6e2", seed=nx(), rough=0.5, streak=0.3, pad=6)
    art = G(art, np.clip(pm - np.roll(pm, -2, 0), 0, 1), "#7d8b85", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4, pad=6)
    preview(art, "ws-plane", bg="#cfe0d0")
    save(art, f"{OUT}/plane.webp", max_w=280, quality=84)

if "lamp" in PARTS:
    W, H = 320, 620
    nx = Seq(40300); cx = 160
    art = blank(W, H)
    art = over(art, glow(circles(W, H, [(cx, 390, 46)]), "#ffd27a", radius=28, strength=0.5))
    cord = strokes(W, H, [([(cx, 0), (cx, 170)], 3, None)])
    art = FO(art, cord, GOLD, seed=nx())
    body = shapes(W, H, [[(cx - 52, 300), (cx - 52, 470), (cx + 52, 470), (cx + 52, 300)]], smooth=False)
    art = GP(art, body, "#ffe3a0", "#f2b85a", seed=nx(), rough=0.8, pad=8)
    art = over(art, rgba("#fff6dc", gaussian_filter(circles(W, H, [(cx, 390, 22)]), 14) * 1.5 * body))
    # pierced gold shell: body with star cut-outs
    shell = body.copy()
    holes = shapes(W, H, [star8(cx + dx, 330 + dy, 9, 0.6) for dx in (-30, 0, 30) for dy in (0, 38, 76, 114)], smooth=False)
    holes = np.maximum(holes, shapes(W, H, [star8(cx + dx, 349 + dy, 5, 0.6) for dx in (-15, 15) for dy in (0, 38, 76)], smooth=False))
    shell = np.clip(shell - holes, 0, 1)
    art = FO(art, shell * 0.94, GOLD, seed=nx(), emboss=0.7, sparkle=0.12)
    dome = shapes(W, H, [[(cx - 60, 302), (cx - 54, 262), (cx - 30, 222), (cx, 186), (cx + 30, 222), (cx + 54, 262), (cx + 60, 302)]])
    dome_holes = shapes(W, H, [star8(cx + dx, 262, 6, 0.6) for dx in (-26, 0, 26)], smooth=False)
    art = GP(art, dome_holes, "#ffe6a8", seed=nx(), rough=0.4, pad=6)
    art = FO(art, np.clip(dome - dome_holes, 0, 1), GOLD, seed=nx(), emboss=0.8, sparkle=0.12)
    fin = np.maximum.reduce([shapes(W, H, [petal_pts(cx, 186, 30, 6, -math.pi / 2, n=10)]), circles(W, H, [(cx, 170, 7)])])
    base = shapes(W, H, [[(cx - 60, 468), (cx + 60, 468), (cx + 44, 492), (cx + 14, 512), (cx, 540), (cx - 14, 512), (cx - 44, 492)]])
    bands = shapes(W, H, [[(cx - 58, 296), (cx + 58, 296), (cx + 58, 306), (cx - 58, 306)], [(cx - 58, 464), (cx + 58, 464), (cx + 58, 474), (cx - 58, 474)]], smooth=False)
    tassel = strokes(W, H, [([(cx + d, 540), (cx + d * 1.6, 600)], 2.4, (0.0, 0.5)) for d in (-6, -3, 0, 3, 6)])
    art = FO(art, np.maximum.reduce([fin, base, bands]), GOLD, seed=nx(), emboss=0.8, sparkle=0.1)
    art = FO(art, np.maximum(tassel, circles(W, H, [(cx, 542, 7)])), "#d8b465", seed=nx(), emboss=0.4)
    preview(art, "ws-lamp", bg=GREEN)
    save(art, f"{OUT}/lamp.webp", max_w=200, quality=84)
    clear()

if "star" in PARTS:
    W = H = 200
    nx = Seq(40400)
    a = shapes(W, H, [star8(100, 100, 92, 0.76, math.pi / 8)], smooth=False)
    b = shapes(W, H, [star8(100, 100, 78, 0.76, math.pi / 8)], smooth=False)
    c = shapes(W, H, [star8(100, 100, 46, 0.62, 0)], smooth=False)
    d = circles(W, H, [(100, 100, 16)])
    m = np.clip(a - b, 0, 1) + np.clip(c - circles(W, H, [(100, 100, 30)]), 0, 1) + d
    lines = strokes(W, H, [([(100 + math.cos(k * math.pi / 4) * 30, 100 + math.sin(k * math.pi / 4) * 30), (100 + math.cos(k * math.pi / 4) * 76, 100 + math.sin(k * math.pi / 4) * 76)], 3, None) for k in range(8)])
    art = FO(blank(W, H), np.clip(m + lines, 0, 1), GOLD, seed=nx(), emboss=0.75, sparkle=0.14)
    preview(art, "ws-star", bg=GREEN)
    save(art, f"{OUT}/star.webp", max_w=120, quality=86)

if "band" in PARTS:
    # seamless foil geometric band: alternating 8-point stars and crosses between two rules
    W, H = 480, 56
    nx = Seq(40500)
    rules = shapes(W, H, [[(0, 2), (W, 2), (W, 5), (0, 5)], [(0, H - 5), (W, H - 5), (W, H - 2), (0, H - 2)]], smooth=False)
    stars = []
    for k in range(6):
        x = 40 + k * 80
        stars.append(star8(x, H / 2, 17, 0.7, math.pi / 8))
    sm = np.clip(shapes(W, H, stars, smooth=False) - circles(W, H, [(40 + k * 80, H / 2, 8) for k in range(6)]), 0, 1)
    dia = shapes(W, H, [[(x, H / 2 - 9), (x + 9, H / 2), (x, H / 2 + 9), (x - 9, H / 2)] for x in [80 * k for k in range(7)]], smooth=False)
    links = strokes(W, H, [([(x + 12, H / 2), (x + 26, H / 2)], 1.6, None) for x in [80 * k - 2 for k in range(7)]] + [([(x - 12, H / 2), (x - 26, H / 2)], 1.6, None) for x in [80 * k + 2 for k in range(7)]])
    art = FO(blank(W, H), np.clip(rules + sm + dia + links, 0, 1), GOLD, seed=nx(), emboss=0.6, sparkle=0.1)
    preview(art, "ws-band", bg=GREEN)
    save_full(art, f"{OUT}/band.webp", quality=84)

if "velvet" in PARTS:
    n = 256
    v = wrap_noise(n, n, 3, 2.0) * 0.5 + wrap_noise(n, n, 4, 24) * 0.5
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#0f3b2e"), np.float32) * (0.82 + 0.36 * v)[..., None]
    # faint embossed lattice (square-in-square), seamless
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    u = np.abs(((xx + yy) / n * 4) % 1 - 0.5); w = np.abs(((xx - yy) / n * 4) % 1 - 0.5)
    lat = np.clip(1 - np.minimum(u, w) * 40, 0, 1)
    base = base * (1 + lat[..., None] * 0.08)
    save_rgb(np.concatenate([base, np.ones((n, n, 1), np.float32)], -1), f"{OUT}/velvet.webp", quality=72)

kb(OUT)
