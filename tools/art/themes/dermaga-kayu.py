"""Dermaga Kayu — a long weathered wooden pier running out into a calm sea at sunrise, soft pastel watercolour:
lilac-to-peach sky, a half-risen sun, a small rowboat tied to the pier, far island, gulls.
Assets: dermaga (full cover scene, opaque), camar (gulls, drifting), tali (rope-knot divider), kerang (shell node),
ombak (watercolour wave band).
Run: python3 -I dermaga-kayu.py [part ...]
Assets -> public/themes/art/dermaga-kayu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s5_lib import *

OUT = outdir("dermaga-kayu")
PARTS = sys.argv[1:] or ["dermaga", "camar", "tali", "kerang", "ombak"]
NAVY = "#2f4256"
WOOD, WOOD_D, WOOD_L = "#9a7a60", "#5f4636", "#c7a98a"
SEA, SEA_D, SEA_L = "#8fb3c4", "#5f8aa3", "#cfe0e6"
PEACH, LILAC, GOLD = "#f4c3a4", "#c7b6d8", "#f7d79a"


def dermaga():
    W, H = 760, 1360
    clear()
    hz = 830                     # horizon
    vx = 430                     # vanishing point x
    art = painted_sky(W, H, [(0, "#bfb3d6"), (0.2, "#d9c4dc"), (0.4, "#f1cdc4"), (0.56, "#f8d9b4"), (0.61, "#fbe4bd"), (1, "#fbe4bd")], seed=3, streak=0.5, grain=0.6)
    # wet-in-wet cloud washes
    for i, (x, y, rx, ry, c) in enumerate([(160, 330, 260, 34, "#e9c3cf"), (600, 250, 240, 26, "#e4c7dc"), (420, 520, 300, 22, "#f6d1b8"), (110, 610, 200, 16, "#f9d7bd"), (650, 650, 180, 14, "#fbdcc0")]):
        art = G(art, ellipses(W, H, [(x, y, rx, ry, 0)]), c, "#f7e0d4", seed=10 + i, density=0.55, edge=0.25, bloom=0.5, rough=14, feather=8, pad=40)
    # sun, half above the horizon, with glow
    art = over(art, glow(circles(W, H, [(vx + 70, hz, 70)]), "#fff1cf", radius=60, strength=0.55))
    art = G(art, circles(W, H, [(vx + 70, hz, 64)]) * (np.arange(H)[:, None] < hz), "#fde3a6", "#fbd38c", seed=20, density=0.85, edge=0.3, bloom=0.1, rough=1.5, feather=1.0)
    # far island
    isl = [(x, hz - 4 - 34 * math.exp(-((x - 120) / 90) ** 2) - 18 * math.exp(-((x - 230) / 60) ** 2)) for x in range(-10, 360, 8)]
    art = G(art, shape_mask(W, H, isl + [(360, hz + 2), (-10, hz + 2)], smooth=False), "#b9a8c9", "#a99cc0", seed=21, density=0.75, edge=0.5, bloom=0.2, rough=2, feather=1)
    clear()
    rng0 = 0
    # sea washes, deeper toward the bottom
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seam = (yy > hz).astype(np.float32)
    depth = np.clip((yy - hz) / (H - hz), 0, 1)
    seasky = painted_sky(W, H, [(0, "#d6e3e6"), (hz / H, "#d6e3e6"), (hz / H + 0.03, "#c4d8df"), (1, "#a9c6d3")], seed=8, streak=1.0, grain=0.5)
    art = over(art, np.concatenate([seasky[..., :3], seam[..., None]], -1))
    art = G(art, seam * (0.15 + 0.85 * depth), SEA, SEA_D, seed=22, density=0.5, edge=0.0, bloom=0.5, rough=0, feather=1, pad=0)
    for i, y in enumerate((900, 980, 1090, 1220)):
        art = G(art, ellipses(W, H, [(rng0 * 0 + 120 + i * 160, y, 300, 10 + i * 6, 0)]) * seam, "#7fa3b8", seed=60 + i, density=0.3, edge=0.1, bloom=0.5, rough=10, feather=5, pad=30)
    # sun path glitter: short horizontal strokes, widening toward the viewer
    rng = random.Random(5)
    gl = []
    for y in np.arange(hz + 4, H - 20, 7):
        t = (y - hz) / (H - hz)
        for _ in range(2):
            cx = vx + 70 + rng.gauss(0, 18 + t * 150)
            L = rng.uniform(8, 20 + t * 60)
            gl.append([(cx - L / 2, y), (cx + L / 2, y + rng.uniform(-1, 1))])
    art = OV(art, lines(W, H, gl, 2.0) * seam, lambda q: flat(gaussian_filter(q, 0.6), "#fff0cf", 0.75))
    # darker ripple strokes
    rp = []
    for y in np.arange(hz + 14, H, 13):
        t = (y - hz) / (H - hz)
        for _ in range(3):
            x0 = rng.uniform(-20, W)
            L = rng.uniform(20, 50 + t * 120)
            rp.append((curve([(x0, y), (x0 + L / 2, y - 1.5 - t * 3), (x0 + L, y)], 10), 1.4 + t * 2.5, (0.3, 0.3)))
    art = G(art, strokes(W, H, rp) * seam, SEA_D, "#6f8fb0", seed=23, density=0.4, edge=0.2, bloom=0, rough=0.6, feather=0.8)
    clear()
    # ── pier: deck trapezoid in perspective ──
    by = H + 40
    bl, br = 120, 640              # deck edges at the bottom
    tl, tr = vx - 14, vx + 14      # deck edges near the horizon end
    ty = hz + 18
    def edge(xb, xt, t):           # t 0 (bottom) .. 1 (far)
        return xb + (xt - xb) * t
    def ydepth(t):                 # perspective: far planks compressed
        return by - (by - ty) * (1 - (1 - t) ** 2.3)
    deck = [(bl, by), (br, by), (tr, ty), (tl, ty)]
    md = shape_mask(W, H, deck, smooth=False)
    # posts under the deck edges, both sides
    posts = []
    for k in range(16):
        t = k / 15
        y = ydepth(t)
        for side, xb, xt in ((-1, bl, tl), (1, br, tr)):
            x = edge(xb, xt, 1 - (1 - t) ** 2.3)
            sc = (1 - t) ** 1.6 * 0.95 + 0.05
            pw = 18 * sc
            posts.append(rect(x - pw / 2, y - 10 * sc, x + pw / 2, y + 120 * sc))
    mp = shapes(W, H, posts, smooth=False)
    art = G(art, mp, WOOD_D, "#4a3a32", seed=30, density=0.92, edge=0.6, bloom=0.2, rough=1.0, feather=0.6)
    # post reflections
    pref = np.roll(mp, 30, 0) * seam
    art = G(art, gaussian_filter(pref, (6, 1.5)) * 0.8, "#5c6f84", seed=31, density=0.5, edge=0.1, bloom=0.2, rough=4, feather=2)
    art = G(art, md, WOOD, WOOD_L, seed=32, density=0.9, edge=0.6, bloom=0.4, rough=1.2, feather=0.6)
    # plank seams across the deck
    seams = []
    k = 0
    t = 0.0
    while t < 1:
        u = 1 - (1 - t) ** 2.3
        y = ydepth(t)
        seams.append([(edge(bl, tl, u) - 2, y), (edge(br, tr, u) + 2, y)])
        k += 1
        t += 0.028
    art = G(art, lines(W, H, seams, 1.6) * md, WOOD_D, seed=33, density=0.55, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    # long grain strokes converging to the vanishing point
    gr = []
    for _ in range(46):
        u0 = rng.uniform(0.02, 0.98)
        xb = bl + (br - bl) * u0
        xt = tl + (tr - tl) * u0
        t0, t1 = sorted([rng.uniform(0, 0.8), rng.uniform(0, 0.8)])
        gr.append(([(xb + (xt - xb) * t0, by - (by - ty) * t0), (xb + (xt - xb) * t1, by - (by - ty) * t1)], 1.4, (0.3, 0.3)))
    art = G(art, strokes(W, H, gr) * md, "#7d604c", seed=34, density=0.35, edge=0.1, bloom=0, rough=0.5, feather=0.6)
    # morning light on the far deck, shadow near the viewer
    art = G(art, md * np.clip((yy - 1050) / 400, 0, 1), "#6d5246", seed=35, density=0.45, edge=0.0, bloom=0.3, rough=0, feather=4)
    art = OV(art, md * np.clip(1 - (yy - hz) / 260, 0, 1) * 0.35, lambda q: flat(q, "#ffe4c0", 1.0))
    clear()
    # bollards + rope posts along the deck edges
    bol = []
    for t in (0.12, 0.38, 0.62):
        u = 1 - (1 - t) ** 2.3
        y = ydepth(t)
        sc = (1 - t) ** 1.6 * 0.95 + 0.05
        for xb, xt, d in ((bl, tl, 1), (br, tr, -1)):
            x = edge(xb, xt, u) + d * 10 * sc
            bol.append(rect(x - 9 * sc, y - 70 * sc, x + 9 * sc, y))
    mb = shapes(W, H, bol, smooth=False)
    art = G(art, mb, WOOD_D, "#4a3a32", seed=36, density=0.95, edge=0.6, rough=0.8, feather=0.5)
    # rope rail sagging between the left posts
    rope = []
    tops = []
    for t in (0.12, 0.38, 0.62):
        u = 1 - (1 - t) ** 2.3
        y = ydepth(t)
        sc = (1 - t) ** 1.6 * 0.95 + 0.05
        tops.append((edge(bl, tl, u) + 10 * sc, y - 62 * sc, sc))
    for (x0, y0, s0), (x1, y1, s1) in zip(tops, tops[1:]):
        rope.append((curve([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 22 * s0), (x1, y1)], 20), 3.2 * s0 + 1, (0.0, 0.0)))
    art = G(art, strokes(W, H, rope), "#b49a72", "#8f7550", seed=37, density=0.85, edge=0.4, rough=0.4, feather=0.5)
    clear()
    # ── rowboat tied off the left side, mid-distance ──
    bx, byb, s = 150, 1010, 92
    hull = curve([(bx - s, byb - s * 0.12), (bx - s * 0.7, byb + s * 0.2), (bx + s * 0.5, byb + s * 0.22), (bx + s * 1.05, byb - s * 0.2)], 30) + [(bx + s * 0.9, byb - s * 0.12), (bx - s * 0.85, byb - s * 0.06)]
    mh = shape_mask(W, H, hull)
    art = G(art, mh, "#f4ece0", "#e9ddcb", seed=40, density=0.95, edge=0.5, bloom=0.2, rough=1.0, feather=0.6)
    band = strokes(W, H, [(curve([(bx - s * 0.92, byb - s * 0.02), (bx, byb + s * 0.1), (bx + s * 0.98, byb - s * 0.1)], 20), s * 0.07, (0.05, 0.05))]) * mh
    art = G(art, band, "#6f9fb2", seed=41, density=0.85, edge=0.3, rough=0.4, feather=0.5)
    inner = shape_mask(W, H, curve([(bx - s * 0.85, byb - s * 0.07), (bx, byb - s * 0.02), (bx + s * 0.9, byb - s * 0.13)], 20) + [(bx + s * 0.8, byb - s * 0.2), (bx - s * 0.75, byb - s * 0.14)])
    art = G(art, inner, "#8a6a52", seed=42, density=0.8, edge=0.4, rough=0.6, feather=0.5)
    art = G(art, gaussian_filter(np.roll(mh[::1], 0, 0), 1) * 0 + gaussian_filter(np.roll(np.flipud(mh), 2 * byb - H + 4, 0), (3, 1)) * seam * 0.6, "#7fa0b8", seed=43, density=0.45, rough=3, feather=2)
    art = G(art, strokes(W, H, [(curve([(bx + s * 0.95, byb - s * 0.17), (bx + s * 1.6, byb - s * 0.05), (edge(bl, tl, 1 - (1 - 0.38) ** 2.3) + 4, ydepth(0.38) - 30)], 20), 2.0, (0.0, 0.0))]), "#8f7550", seed=44, density=0.8, rough=0.3, feather=0.4)
    ripples = [(curve([(bx - s * 1.2 + d, byb + s * 0.24 + k * 7), (bx + d * 0.2, byb + s * 0.28 + k * 7), (bx + s * 1.2 - d, byb + s * 0.22 + k * 7)], 14), 1.6, (0.3, 0.3)) for k, d in enumerate((0, 20, 45))]
    art = G(art, strokes(W, H, ripples), SEA_D, seed=45, density=0.5, rough=0.5, feather=0.6)
    art = add_grain(art, 9, 0.03)
    preview(art, "dermaga")
    save_rgb(art, f"{OUT}/dermaga.webp", (760, 1360), quality=74)


def gull(W, H, x, y, s, flap):
    l = curve([(x, y), (x - s * 0.45, y - s * (0.3 + flap)), (x - s, y - s * 0.05 * (1 - flap))], 12)
    r = curve([(x, y), (x + s * 0.45, y - s * (0.3 + flap)), (x + s, y - s * 0.05 * (1 - flap))], 12)
    return [(l, s * 0.11, (0.1, 0.6)), (r, s * 0.11, (0.1, 0.6))]


def camar():
    W, H = 260, 120
    clear()
    art = blank(W, H)
    st = gull(W, H, 70, 70, 50, 0.15) + gull(W, H, 170, 40, 36, -0.05) + gull(W, H, 220, 85, 24, 0.2)
    art = G(art, strokes(W, H, st), "#5a5f78", "#7a7090", seed=3, density=0.8, edge=0.5, bloom=0.1, rough=0.6, feather=0.6)
    preview(art, "camar", tone="#f3dccd")
    save(art, f"{OUT}/camar.webp", max_w=200)


def tali():
    """Divider: a short length of rope with a knot in the middle."""
    W, H = 520, 70
    clear()
    art = blank(W, H)
    cy = H / 2
    segs = []
    for d in (-1, 1):
        p = curve([(W / 2 + d * 20, cy), (W / 2 + d * 120, cy + 5), (W / 2 + d * 230, cy - 2)], 40)
        segs.append((p, 5, (0.0, 0.25)))
    m = strokes(W, H, segs, cap=True)
    art = G(art, m, "#c7aa80", "#a8895e", seed=3, density=0.9, edge=0.5, rough=0.5, feather=0.5)
    tw = []
    for d in (-1, 1):
        for x in np.arange(24, 220, 9):
            px = W / 2 + d * x
            py = cy + 5 * math.sin(math.pi * (x - 20) / 210) * (1 if True else 0)
            tw.append(([(px - 2.5, py - 2.5), (px + 2.5, py + 2.5)], 1.3, (0.1, 0.1)))
    art = G(art, strokes(W, H, tw) * m, "#7d6040", seed=4, density=0.6, rough=0.3, feather=0.4)
    knot = ellipses(W, H, [(W / 2 - 7, cy - 2, 13, 9, -25), (W / 2 + 7, cy + 2, 13, 9, 25), (W / 2, cy, 9, 12, 0)])
    art = G(art, knot, "#c7aa80", "#9a7c52", seed=5, density=0.92, edge=0.7, rough=0.6, feather=0.5)
    art = G(art, strokes(W, H, [(curve([(W / 2 + 4, cy + 8), (W / 2 + 12, cy + 22), (W / 2 + 8, cy + 30)], 10), 4, (0.0, 0.5)), (curve([(W / 2 - 4, cy + 8), (W / 2 - 14, cy + 20), (W / 2 - 20, cy + 26)], 10), 4, (0.0, 0.5))]), "#b49a72", seed=6, density=0.85, edge=0.4, rough=0.4, feather=0.5)
    preview(art, "tali")
    save(art, f"{OUT}/tali.webp", max_w=440)


def kerang():
    """Scallop shell, watercolour."""
    W, H = 160, 160
    clear()
    art = blank(W, H)
    cx, cy = 80, 120
    fan = [(cx, cy)] + [(cx + math.cos(a) * 64 * (1 + 0.04 * math.sin(a * 22)), cy - 12 + math.sin(a) * 70) for a in np.linspace(math.pi * 1.08, math.pi * 1.92, 30)]
    m = shape_mask(W, H, fan)
    art = G(art, m, "#f6d2bf", "#f1b8a4", seed=3, density=0.85, edge=0.7, bloom=0.3, rough=1.2, feather=0.6)
    ribs = [([(cx, cy - 4), (cx + math.cos(a) * 62, cy - 12 + math.sin(a) * 66)], 2.2, (0.3, 0.2)) for a in np.linspace(math.pi * 1.12, math.pi * 1.88, 11)]
    art = G(art, strokes(W, H, ribs) * m, "#d98c78", seed=4, density=0.55, edge=0.2, rough=0.4, feather=0.6)
    ears = shapes(W, H, [[(cx - 4, cy - 12), (cx - 24, cy - 6), (cx - 22, cy + 4), (cx - 2, cy + 4)], [(cx + 4, cy - 12), (cx + 24, cy - 6), (cx + 22, cy + 4), (cx + 2, cy + 4)]], smooth=False)
    art = G(art, ears, "#f1c2ae", "#e5a28c", seed=5, density=0.85, edge=0.6, rough=0.6, feather=0.5)
    preview(art, "kerang")
    save(art, f"{OUT}/kerang.webp", max_w=90)


def ombak():
    """Wide band of calm watercolour sea with a soft upper edge (closing / countdown decor)."""
    W, H = 780, 200
    clear()
    art = blank(W, H)
    top = [(x, 40 + 6 * math.sin(x / 70) + 3 * math.sin(x / 23)) for x in range(-10, W + 20, 10)]
    m = shape_mask(W, H, top + [(W + 10, H + 10), (-10, H + 10)], smooth=False)
    art = G(art, m, SEA_L, SEA, seed=3, density=0.75, edge=0.55, bloom=0.4, rough=4, feather=1.5)
    yy = np.arange(H)[:, None] * np.ones((1, W))
    art = G(art, m * np.clip((yy - 70) / 130, 0, 1), SEA, SEA_D, seed=4, density=0.6, edge=0.0, bloom=0.3, rough=0, feather=2)
    rng = random.Random(4)
    rp = [(curve([(x0, y), (x0 + L / 2, y - 2), (x0 + L, y)], 10), 1.8, (0.3, 0.3)) for y in np.arange(62, H, 14) for x0, L in [(rng.uniform(-20, W), rng.uniform(40, 140)), (rng.uniform(-20, W), rng.uniform(40, 120))]]
    art = OV(art, strokes(W, H, rp) * m, lambda q: flat(q, "#eef6f6", 0.7))
    preview(art, "ombak", tone="#fbeee4")
    save(art, f"{OUT}/ombak.webp", max_w=780, quality=78)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
