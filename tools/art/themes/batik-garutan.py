"""Batik Garutan — hand-drawn batik from Garut on a cream "gumading" ground: a seamless lereng (diagonal) tile in
soft soga, indigo and sage with cecek dots and little flowers; a canting-drawn flower spray with isen-isen; a small
bud for nodes; a tendril divider; and a watercolour Garut landscape (Cikuray cone, Papandayan, tea terraces).
Run: python3 -I batik-garutan.py [part ...]  parts: lereng kembang kuncup divider cikuray kain
Assets -> public/themes/art/batik-garutan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q2_lib import *

OUT = outdir("batik-garutan")
PARTS = sys.argv[1:] or ["lereng", "kembang", "kuncup", "divider", "cikuray", "kain"]
CREAM, CREAM_D = "#efe2c3", "#e2d1aa"
SOGA, SOGA_D, SOGA_L = "#94603a", "#6b3f22", "#b88a5e"
BIRU, BIRU_D, BIRU_L = "#41627d", "#2f4a62", "#7f9cb0"
HIJAU, HIJAU_D = "#7d9168", "#5d7150"
LINE = "#3f2a1c"


def cloth(W, H, seed=1, tone=CREAM):
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    low = fbm(W, H, seed, 120, 3) - 0.5
    rgb *= (1 + low * 0.05)[..., None]
    rgb *= weave(H, W, seed, 0.05)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def wrap_blend(arr):
    """Make a geometry-periodic render seamless: cross-fade with its half-offset roll near the edges."""
    h, w = arr.shape[:2]
    sh = np.roll(np.roll(arr, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = np.minimum(xx, w - 1 - xx) / (w / 2); wy = np.minimum(yy, h - 1 - yy) / (h / 2)
    k = np.clip(np.minimum(wx, wy) * 3.0, 0, 1)[..., None]
    return arr * k + sh * (1 - k)


def flower_pts(cx, cy, r, n, rot, ratio=0.55, rng=None):
    """Rounded n-petal flower outline."""
    pts = []
    for i in range(n * 10):
        t = i / (n * 10) * math.tau
        rr = r * (ratio + (1 - ratio) * abs(math.sin(n * (t + rot) / 2)) ** 0.7)
        pts.append((cx + math.cos(t) * rr, cy + math.sin(t) * rr))
    return pts


def lereng():
    S, P = 360, 180
    clear()
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    u = (xx + yy) % P

    def band(a, b):
        return ((u >= a) & (u < b)).astype(np.float32)

    def lattice(uc, dv, v0=0.0):
        pts = []
        for k in range(-3, 6):
            for m in range(-12, 24):
                uu = uc + k * P; vv = v0 + m * dv
                x, y = (uu + vv) / 2, (uu - vv) / 2
                if -40 < x < S + 40 and -40 < y < S + 40:
                    pts.append((x, y))
        return pts

    art = cloth(S, S, 2)
    # soga band
    art = D(art, band(0, 50), SOGA, SOGA_D, seed=11, rough=0.6, bleed=0.7)
    # blue band
    art = D(art, band(62, 114), BIRU, BIRU_D, seed=12, rough=0.6, bleed=0.7)
    # green narrow band
    art = D(art, band(126, 146), HIJAU, HIJAU_D, seed=13, rough=0.6, bleed=0.7)
    # crackle veins across the coloured bands (cracked wax)
    cr = crackle(S, S, 21, 0.012, 30) * np.clip(band(0, 50) + band(62, 114) + band(126, 146), 0, 1)
    art = OV(art, cr, lambda q: flat(q, "#2b1d14", 0.45))
    # canting lines along band edges
    edges = np.zeros((S, S), np.float32)
    for e in (0, 50, 62, 114, 126, 146):
        d = np.abs(((xx + yy - e + P / 2) % P) - P / 2) / math.sqrt(2)
        edges = np.maximum(edges, np.clip(1.4 - d, 0, 1))
    art = D(art, edges, LINE, seed=14, rough=0.5, bleed=0.5, density=0.85)
    # motifs: cream cecek rows + small cream flowers on soga
    dots = [(x, y, 2.3) for x, y in lattice(12, 18)] + [(x, y, 2.3) for x, y in lattice(38, 18, 9)]
    art = D(art, circles(S, S, dots), CREAM, seed=15, rough=0.3, bleed=0.5)
    fl = [flower_pts(x, y, 9, 4, 0.785) for x, y in lattice(25, 36)]
    art = D(art, shapes(S, S, fl), CREAM, seed=16, rough=0.3, bleed=0.5)
    art = D(art, circles(S, S, [(x, y, 2.4) for x, y in lattice(25, 36)]), SOGA_D, seed=17, rough=0.2, bleed=0.4)
    # blue band: cream 5-petal flowers with soga centres and little leaves
    centers = lattice(88, 72)
    fl = [flower_pts(x, y, 17, 5, 0.3) for x, y in centers]
    art = D(art, shapes(S, S, fl), CREAM, seed=18, rough=0.4, bleed=0.5)
    ring_l = np.zeros((S, S), np.float32)
    for x, y in centers:
        ring_l = np.maximum(ring_l, strokes(S, S, [(flower_pts(x, y, 13, 5, 0.3)[::3] + [flower_pts(x, y, 13, 5, 0.3)[0]], 1.2, None)]))
    art = D(art, ring_l, BIRU_L, seed=19, rough=0.3, bleed=0.4)
    art = D(art, circles(S, S, [(x, y, 5) for x, y in centers]), SOGA, seed=20, rough=0.2, bleed=0.4)
    lv = []
    for x, y in lattice(88, 72, 36):
        lv.append(petal_pts(x - 10, y + 10, 22, 6, -0.785, n=12))
    art = D(art, shapes(S, S, lv), CREAM_D, seed=22, rough=0.3, bleed=0.5)
    # green band: cream chevron leaves
    lv = [petal_pts(x - 4, y + 4, 12, 3.4, -0.785 + 0.5, n=10) for x, y in lattice(136, 20)]
    art = D(art, shapes(S, S, lv), CREAM, seed=23, rough=0.25, bleed=0.4)
    # cream band: small soga cecek
    dots = [(x, y, 1.6) for x, y in lattice(156, 12)] + [(x, y, 1.6) for x, y in lattice(170, 12, 6)]
    art = D(art, circles(S, S, dots), SOGA_L, seed=24, rough=0.2, bleed=0.4, density=0.8)
    art = wrap_blend(art)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{OUT}/lereng.webp", "WEBP", quality=80, method=6)
    print("lereng.webp", os.path.getsize(f"{OUT}/lereng.webp") // 1024, "KB")
    big = np.tile(art[..., :3], (2, 2, 1))
    Image.fromarray((np.clip(big, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/bg-lereng.png")


def inset(pts, d):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    out = []
    for x, y in pts:
        vx, vy = x - cx, y - cy
        L = math.hypot(vx, vy) + 1e-6
        k = max(0.0, (L - d) / L)
        out.append((cx + vx * k, cy + vy * k))
    return out


def canting(art, W, H, polys, width=2.4, seed=1, closed=True):
    items = []
    for pts in polys:
        q = list(pts) + ([pts[0]] if closed else [])
        items.append((q, width, None))
    m = strokes(W, H, items)
    return D(art, m, LINE, seed=seed, rough=0.6, bleed=0.45, density=0.92)


def cecek_along(pts, step, r=1.6):
    out = []
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        L = math.hypot(x1 - x0, y1 - y0)
        while acc < L:
            t = acc / max(L, 1e-6)
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r))
            acc += step
        acc -= L
    return out


def erase(art, mask, grow=1.2):
    m = np.clip(gaussian_filter(mask, grow) * 1.6, 0, 1)
    out = art.copy()
    out[..., 3] *= 1 - m
    return out


def soft_petal(cx, cy, L, Wd, ang, n=30):
    right, left = [], []
    for i in range(n + 1):
        t = i / n
        hw = Wd * (t ** 0.5) * max(0.0, 1 - t ** 2.6) ** 0.5
        right.append((t * L, hw)); left.append((t * L, -hw))
    pts = right + left[::-1]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def petal_one(art, W, H, pts, col, col2, seed, base, ang, L, isen="cecek"):
    m = shape_mask(W, H, pts)
    art = erase(art, m)
    art = D(art, m, col, col2, seed=seed, rough=0.7, bleed=0.6, density=1.0)
    bx, by = base
    if isen == "cecek":
        art = D(art, circles(W, H, cecek_along(inset(pts, 6)[3:-3], 7.5, 1.7)), CREAM, seed=seed + 2, rough=0.3, bleed=0.4)
    else:
        lines = []
        for d in np.linspace(-0.22, 0.22, 5):
            a = ang + d
            lines.append(([(bx + math.cos(a) * L * 0.22, by + math.sin(a) * L * 0.22), (bx + math.cos(a) * L * (0.72 - abs(d)), by + math.sin(a) * L * (0.72 - abs(d)))], 1.3, (0.1, 0.4)))
        art = D(art, strokes(W, H, lines), CREAM, seed=seed + 2, rough=0.3, bleed=0.35, density=0.9)
    return canting(art, W, H, [pts], 2.3, seed + 1)


def batik_flower(art, W, H, cx, cy, R, rot, seed, petal_col=SOGA, petal_col2=SOGA_D, inner_col=BIRU, n=8):
    """Layered canting flower: outer petals (cecek rim), inner ring petals (sawut lines), dotted centre."""
    order = list(range(n))
    for k, i in enumerate(order):
        a = rot + i * math.tau / n
        pts = soft_petal(cx, cy, R, R * 0.36, a)
        art = petal_one(art, W, H, pts, petal_col, petal_col2, seed + k * 3, (cx, cy), a, R, "cecek")
    inner2 = inner_col
    for k in range(n):
        a = rot + (k + 0.5) * math.tau / n
        pts = soft_petal(cx, cy, R * 0.6, R * 0.24, a)
        art = petal_one(art, W, H, pts, inner2, BIRU_D if inner2 == BIRU else SOGA, seed + 60 + k * 3, (cx, cy), a, R * 0.6, "sawut")
    core = circles(W, H, [(cx, cy, R * 0.2)])
    art = erase(art, core)
    art = D(art, core, CREAM, seed=seed + 6, rough=0.4, bleed=0.4, density=1.0)
    art = canting(art, W, H, [ellipse_pts(cx, cy, R * 0.2, R * 0.2, 24)], 2.0, seed + 7)
    cd = [(cx + math.cos(a) * r, cy + math.sin(a) * r, 1.8) for r in (R * 0.07, R * 0.13) for a in np.linspace(0, math.tau, 9 if r > R * 0.1 else 5)[:-1]]
    art = D(art, circles(W, H, cd + [(cx, cy, 2.2)]), SOGA_D, seed=seed + 8, rough=0.2, bleed=0.3)
    return art


def batik_leaf(art, W, H, x, y, L, Wd, ang, seed, col=HIJAU, col2=HIJAU_D, bend=0.2):
    pts = []
    mid = []
    n = 22
    for i in range(n + 1):
        t = i / n
        a = ang + bend * t
        if i == 0:
            px, py = x, y
        else:
            px += math.cos(a) * L / n; py += math.sin(a) * L / n
        mid.append((px, py, a))
    r, l = [], []
    for i, (px, py, a) in enumerate(mid):
        t = i / n
        hw = Wd * math.sin(math.pi * t ** 0.75) ** 0.85
        r.append((px - math.sin(a) * hw, py + math.cos(a) * hw)); l.append((px + math.sin(a) * hw, py - math.cos(a) * hw))
    outline = r + l[::-1]
    lm = shape_mask(W, H, outline)
    art = erase(art, lm)
    art = D(art, lm, col, col2, seed=seed, rough=0.8, bleed=0.6, density=1.0)
    art = canting(art, W, H, [outline], 2.2, seed + 1)
    veins = [([(p[0], p[1]) for p in mid[1:-2]], 1.8, None)]
    for i in range(3, n - 2, 3):
        px, py, a = mid[i]
        for sd in (-1, 1):
            hw = Wd * math.sin(math.pi * (i / n) ** 0.75) ** 0.85 * 0.75
            veins.append(([(px, py), (px + math.cos(a + sd * 0.9) * hw * 1.2, py + math.sin(a + sd * 0.9) * hw * 1.2)], 1.3, None))
    art = D(art, strokes(W, H, veins), CREAM, seed=seed + 2, rough=0.3, bleed=0.35, density=0.85)
    return art


def tendril(art, W, H, x, y, L, ang, curl, seed, dots=True):
    pts = spiral_like(x, y, L, ang, curl)
    art = canting(art, W, H, [pts], 2.0, seed, closed=False)
    if dots:
        ds = [(px, py, 1.9) for px, py in pts[4::5]]
        art = D(art, circles(W, H, ds), SOGA, seed=seed + 1, rough=0.2, bleed=0.3)
    return art


def spiral_like(x, y, L, ang, curl, n=46):
    pts = [(x, y)]
    a = ang
    step = L / n
    for i in range(n):
        t = i / n
        a += curl * (0.01 + 0.5 * t ** 3)
        x += math.cos(a) * step * (1 - 0.55 * t); y += math.sin(a) * step * (1 - 0.55 * t)
        pts.append((x, y))
    return pts


def textured(art, seed):
    h, w = art.shape[:2]
    out = multiply_rgb(art, weave(h, w, seed, 0.06))
    cr = crackle(h, w, seed + 5, 0.011, 28) * (art[..., 3] > 0.5)
    out[..., :3] = out[..., :3] * (1 - cr[..., None] * 0.35) + np.array(hex_rgb("#2b1d14"), np.float32) * cr[..., None] * 0.35
    return out


def cecek_telu(W, H, pts, r=2.0):
    out = []
    for x, y, a in pts:
        for k in range(3):
            b = a + k * math.tau / 3
            out.append((x + math.cos(b) * r * 2.2, y + math.sin(b) * r * 2.2, r))
    return circles(W, H, out)


def batik_spray_extras(art, W, H):
    art = D(art, cecek_telu(W, H, [(120, 250, 0.2), (420, 200, 0.5), (610, 420, 0.1), (470, 470, 0.9), (150, 470, 0.3), (640, 220, 0.6), (380, 120, 0.2)]), SOGA, seed=91, rough=0.2, bleed=0.3)
    return textured(art, 93)


def kembang():
    """Flower spray: a big soga bloom, an indigo bloom, buds and leaves on curling stems (transparent)."""
    W, H = 720, 560
    art = blank(W, H)
    stems = [([(360, 540), (352, 470), (330, 400), (300, 330), (270, 270)], 3.0, None),
             ([(352, 470), (400, 420), (460, 380), (520, 330)], 2.6, None),
             ([(330, 400), (280, 410), (220, 400), (170, 360)], 2.4, None)]
    art = D(art, strokes(W, H, stems), SOGA_D, seed=3, rough=0.5, bleed=0.4)
    art = batik_leaf(art, W, H, 352, 480, 150, 34, -2.6, 31, HIJAU, HIJAU_D, 0.35)
    art = batik_leaf(art, W, H, 360, 470, 150, 32, -0.35, 33, BIRU_L, BIRU, -0.3)
    art = batik_leaf(art, W, H, 300, 360, 120, 28, -2.9, 35, HIJAU, HIJAU_D, 0.3)
    art = batik_leaf(art, W, H, 430, 400, 110, 26, -1.2, 37, HIJAU, HIJAU_D, -0.4)
    art = batik_leaf(art, W, H, 220, 402, 100, 22, 2.5, 38, BIRU_L, BIRU, 0.3)
    art = batik_leaf(art, W, H, 470, 382, 96, 22, 0.55, 39, HIJAU, HIJAU_D, 0.3)
    clear()
    art = tendril(art, W, H, 200, 400, 150, 3.0, -1, 41)
    art = tendril(art, W, H, 470, 380, 160, 0.1, 1, 43)
    art = tendril(art, W, H, 280, 300, 130, -2.4, 1, 45)
    art = batik_flower(art, W, H, 270, 250, 128, 0.2, 51)
    clear()
    art = batik_flower(art, W, H, 525, 310, 82, 0.5, 61, petal_col=BIRU, petal_col2=BIRU_D, inner_col=SOGA_L, n=7)
    # bud on the left stem
    bud = petal_pts(170, 362, 70, 26, -2.5, n=18)
    art = D(art, shape_mask(W, H, bud), SOGA_L, SOGA, seed=71, rough=0.6, bleed=0.5)
    art = canting(art, W, H, [bud], 2.2, 72)
    art = D(art, circles(W, H, cecek_along(inset(bud, 6)[2:-2], 7, 1.6)), CREAM, seed=73, rough=0.2, bleed=0.3)
    sep = [petal_pts(170, 362, 34, 12, -2.5 + d, n=12) for d in (-0.5, 0.5)]
    art = D(art, shapes(W, H, sep), HIJAU, HIJAU_D, seed=74, rough=0.4, bleed=0.4)
    art = canting(art, W, H, sep, 1.8, 75)
    art = batik_spray_extras(art, W, H)
    preview(art, "bg-kembang", tone=CREAM)
    save(art, f"{OUT}/kembang.webp", max_w=620, quality=82)


def kuncup():
    W, H = 220, 220
    art = blank(W, H)
    art = batik_flower(art, W, H, 110, 110, 96, 0.3, 81, n=8)
    art = textured(art, 83)
    preview(art, "bg-kuncup", tone=CREAM)
    save(art, f"{OUT}/kuncup.webp", max_w=160, quality=84)


def divider():
    W, H = 560, 90
    art = blank(W, H)
    c = W / 2
    for sd in (-1, 1):
        pts = [(c + sd * (34 + t * 220), 45 + 7 * math.sin(t * 6.3)) for t in np.linspace(0, 1, 50)]
        art = canting(art, W, H, [pts], 2.0, 5 + sd, closed=False)
        art = D(art, circles(W, H, [(x, y + 7, 1.7) for x, y in pts[3::6]] + [(x, y - 7, 1.7) for x, y in pts[6::6]]), SOGA, seed=8 + sd, rough=0.2, bleed=0.3)
        art = batik_leaf(art, W, H, c + sd * 40, 45, 46, 10, (0 if sd > 0 else math.pi) - 0.35, 12 + sd, HIJAU, HIJAU_D, 0.2 * sd)
        art = batik_leaf(art, W, H, c + sd * 40, 45, 40, 9, (0 if sd > 0 else math.pi) + 0.45, 14 + sd, BIRU_L, BIRU, -0.2 * sd)
    art = batik_flower(art, W, H, c, 45, 36, 0.1, 21, n=6)
    preview(art, "bg-divider", tone=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=440, quality=84)


def cikuray():
    """Watercolour Garut landscape: Cikuray cone, Papandayan's broken crest, tea terraces, a few albasia trees."""
    W, H = 900, 520
    art = blank(W, H)
    rng = random.Random(4)
    # far: Cikuray, symmetric cone
    cone = [(80, 380), (300, 230), (420, 110), (452, 98), (490, 112), (610, 230), (840, 380), (840, 420), (80, 420)]
    art = G(art, shape_mask(W, H, cone), "#9fb0bd", "#7f95a8", seed=11, density=0.55, edge=0.45, bloom=0.35, rough=4, feather=2.4)
    ridges = [[(452 + d * 6, 110), (452 + d * 40, 200), (452 + d * 70, 300)] for d in (-2, -1, 1, 2, 3)]
    art = G(art, strokes(W, H, [(r, 6, (0.1, 0.5)) for r in ridges]), "#6f8598", seed=12, density=0.3, edge=0.2, bloom=0.1, rough=3)
    # Papandayan on the left: lower, broken crest
    pap = [(-10, 400), (60, 300), (120, 250), (150, 262), (175, 240), (210, 262), (300, 340), (380, 420), (-10, 430)]
    art = G(art, shape_mask(W, H, pap), "#8ea08e", "#7a8f86", seed=13, density=0.6, edge=0.45, bloom=0.3, rough=4, feather=2)
    # mist band
    clear()
    # mid hills (sage)
    hill1 = [(-10, 380)] + [(x, 360 - 30 * math.sin(x / 140) - 12 * math.sin(x / 47)) for x in range(0, 911, 30)] + [(910, 520), (-10, 520)]
    art = G(art, shape_mask(W, H, hill1), "#9db07d", "#7d9168", seed=14, density=0.7, edge=0.4, bloom=0.3, rough=4)
    # tea terraces: rows of rounded bushes following curves
    rows = []
    for k in range(9):
        y0 = 400 + k * 15
        rows.append([(x, y0 + 16 * math.sin(x / 160 + k * 0.4)) for x in range(-20, 930, 10)])
    hedge = [(r, 13 + k * 1.2, None) for k, r in enumerate(rows)]
    shade = [([(x, y + 6 + k * 0.4) for x, y in r], 5 + k * 0.5, None) for k, r in enumerate(rows)]
    art = G(art, strokes(W, H, hedge), "#7f9a58", "#5f7c44", seed=15, density=0.78, edge=0.55, bloom=0.3, rough=3.0, feather=1.2)
    art = G(art, strokes(W, H, shade), "#4e6a38", seed=17, density=0.55, edge=0.3, bloom=0.2, rough=2.5, feather=1.0)
    clear()
    for tx, th in [(110, 130), (168, 96), (770, 140), (835, 100)]:
        trunk = shapes(W, H, [[(tx - 4, 470), (tx + 5, 470), (tx + 6, 470 - th), (tx + 2, 470 - th)]], smooth=False)
        art = G(art, trunk, "#5a4632", seed=tx, density=0.85, edge=0.3, bloom=0, rough=1.2)
        br = [([(tx + 3, 470 - th * 0.75), (tx + 3 + d * th * 0.25, 470 - th * 0.98)], 2.2, (0.0, 0.4)) for d in (-1, 1)]
        art = G(art, strokes(W, H, br), "#5a4632", seed=tx + 2, density=0.8, edge=0.2, bloom=0, rough=1)
        tiers = []
        for k, (dy, sx) in enumerate([(0, 0.48), (-0.1, 0.34), (0.06, 0.3)]):
            ox = (k - 1) * th * 0.18
            tiers.append([(tx + 4 + ox + math.cos(a) * th * sx * (1 + 0.1 * math.sin(a * 7 + k)), 470 - th * (1 + dy) + math.sin(a) * th * 0.11 - (th * 0.04 if math.sin(a) < 0 else 0)) for a in np.linspace(0, math.tau, 30)[:-1]])
        art = G(art, shapes(W, H, tiers), "#6a8a50", "#4b6638", seed=tx + 1, density=0.75, edge=0.6, bloom=0.4, rough=5)
    # top fade (transparent sky)
    yy = np.arange(H, dtype=np.float32)[:, None]
    art[..., 3] *= np.clip((yy - 60) / 120, 0, 1)
    preview(art, "bg-cikuray", tone=CREAM)
    save(art, f"{OUT}/cikuray.webp", max_w=780, quality=78)


def kain():
    """Seamless cream gumading cloth tile with a faint crackle — the page ground."""
    S = 320
    art = cloth(S, S, 31)
    cr = crackle(S, S, 33, 0.008, 40)
    art = OV(art, cr, lambda q: flat(q, "#a8875a", 0.12))
    art = wrap_blend(art)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{OUT}/kain.webp", "WEBP", quality=74, method=6)
    print("kain.webp", os.path.getsize(f"{OUT}/kain.webp") // 1024, "KB")


for p in PARTS:
    {"lereng": lereng, "kembang": kembang, "kuncup": kuncup, "divider": divider, "cikuray": cikuray, "kain": kain}[p]()
    clear()
