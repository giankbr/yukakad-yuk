"""Shared painted building blocks for the six adat-Jawa themes (joglo-marun, kawung-biru, gebyok-sogan, busana-jawi,
wayang-mega, kereta-kencana): flora (roses, melati strings, orchids, banana/pandan, buds), joglo, kawung, parang,
gebyok carving, mega mendung, wayang, kereta, payung. Colours are module globals so a theme can retint (jw.LEAF_A = ...)."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *

CREAM = "#f6ecdc"
MAROON, OXBLOOD, RED = "#6b1e24", "#4a1016", "#b3313a"
GOLD, GOLD_L, GOLD_D = "#c29a4a", "#e2c27a", "#8a6526"
TEAK, TEAK_D, TEAK_L = "#6e4022", "#3f2312", "#8f5a32"
LEAF_A, LEAF_B, LEAF_D = "#7f9a63", "#4c6b42", "#2f4a2e"


# ---------------------------------------------------------------- flora
def rose(art, W, H, cx, cy, r, rng, nx, light, mid, deep, area=None, open_=1.0):
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * 0.88, 10, rng.uniform(0, 3)), rng, 2, 0.12))
    if area is not None:
        np.maximum(area, base, out=area)
    art = G(art, base, light, mid, seed=nx(), density=0.72, edge=0.45, bloom=0.45, rough=8, holes=0.06)
    for k in range(11):
        rr = r * (0.97 - k * 0.08) * open_
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .04), cy + rng.gauss(0, r * .04), rr, a0, a0 + rng.uniform(1.3, 2.6), 26, 0.86)
        sm = stroke_mask(W, H, pts, r * rng.uniform(0.09, 0.16))
        col = mix(mid, deep, min(1, k / 8))
        art = G(art, sm, col, mix(col, light, .25), seed=nx(), density=0.45 + k * 0.04, edge=0.65, bloom=0.15, rough=3.5, feather=1.0)
    heart = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * .16, r * .13, 8), rng, 1, 0.1))
    art = G(art, heart, deep, seed=nx(), density=0.85, edge=0.7, bloom=0, rough=2.5)
    return art


def bud(art, W, H, x, y, s, ang, rng, nx, col, deep):
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 1.6, s * 0.7, ang, n=12), rng, 2, 0.08))
    art = G(art, m, col, deep, seed=nx(), density=0.7, edge=0.6, rough=3)
    sep = strokes(W, H, [(curve([(x, y), (x + math.cos(ang + .5) * s * .9, y + math.sin(ang + .5) * s * .9)], 8), s * .22),
                         (curve([(x, y), (x + math.cos(ang - .5) * s * .9, y + math.sin(ang - .5) * s * .9)], 8), s * .22)])
    return G(art, sep, LEAF_B, LEAF_D, seed=nx(), density=0.75, edge=0.4, rough=1.5, feather=0.8, bloom=0)


def blade(W, H, pts, width):
    """Long leaf (pandan/banana) as a polygon around a centre curve."""
    n = len(pts); L = []; R = []
    for i in range(n):
        t = i / (n - 1)
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nxn, nyn = -dy / d, dx / d
        wd = width * (math.sin(math.pi * min(1, t * 1.05)) ** 0.7 if t > 0.02 else 0.05) * (0.4 + 0.6 * (1 - t) ** 0.3)
        L.append((pts[i][0] + nxn * wd, pts[i][1] + nyn * wd)); R.append((pts[i][0] - nxn * wd, pts[i][1] - nyn * wd))
    return L + R[::-1]


def banana(art, W, H, pts, width, rng, nx, area=None, tear=True):
    poly = blade(W, H, pts, width)
    m = shape_mask(W, H, poly)
    if tear:  # banana leaves split along the side veins
        cuts = []
        for j in range(3, len(pts) - 3, rng.randint(3, 5)):
            a, b = pts[j - 1], pts[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                if rng.random() < 0.45:
                    aa = ang + side * 1.05
                    cuts.append(([(pts[j][0] + math.cos(aa) * width * .45, pts[j][1] + math.sin(aa) * width * .45),
                                  (pts[j][0] + math.cos(aa) * width * 1.3, pts[j][1] + math.sin(aa) * width * 1.3)], 2.6, None))
        if cuts:
            m = np.clip(m - strokes(W, H, cuts), 0, 1)
    if area is not None:
        np.maximum(area, m, out=area)
    art = G(art, m, LEAF_A, LEAF_B, seed=nx(), density=0.62, edge=0.5, bloom=0.4, rough=4, holes=0.04)
    half = shape_mask(W, H, [p for p in blade(W, H, pts, width)[:len(pts)]] + pts[::-1])
    art = G(art, half * m, LEAF_B, LEAF_D, seed=nx(), density=0.38, edge=0.3, bloom=0.2, rough=2)
    veins = [(pts[2:-2], 3.0, (0.05, 0.4))]
    for j in range(3, len(pts) - 3, 2):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for side in (-1, 1):
            aa = ang + side * 1.0
            veins.append(([pts[j], (pts[j][0] + math.cos(aa) * width * .8, pts[j][1] + math.sin(aa) * width * .8)], 1.1, (0.1, 0.6)))
    return G(art, strokes(W, H, veins) * m, LEAF_D, seed=nx(), density=0.32, edge=0.1, bloom=0, rough=1, feather=0.5)


def leaf(art, W, H, x, y, L, ang, rng, nx, area=None, c=(LEAF_A, LEAF_B)):
    m = shape_mask(W, H, petal_pts(x, y, L, L * 0.34, ang, n=10))
    if area is not None:
        np.maximum(area, m, out=area)
    art = G(art, m, c[0], c[1], seed=nx(), density=0.66, edge=0.5, bloom=0.35, rough=4, holes=0.05)
    half = shape_mask(W, H, petal_pts(x, y, L * 0.95, L * 0.15, ang + 0.07, n=10))
    art = G(art, half, c[1], seed=nx(), density=0.3, edge=0.3, bloom=0.2, rough=2.5)
    vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [j / 10 for j in range(1, 9)]]
    return G(art, stroke_mask(W, H, vein, 2.2), LEAF_D, seed=nx(), density=0.3, edge=0.1, bloom=0, rough=1, feather=0.5)


def white_flower(art, W, H, x, y, r, rng, nx, petals=5, shade="#b9a79c", rot=None):
    """Melati: opaque white gouache star with soft grey-violet shadow and a green-yellow eye."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    polys = [petal_pts(x, y, r, r * 0.42, rot + k * math.tau / petals, n=10) for k in range(petals)]
    m = shapes(W, H, polys)
    art = G(art, np.roll(np.roll(m, 2, 0), 2, 1) * 0.8, shade, seed=nx(), density=0.35, edge=0.3, bloom=0, rough=1.5, feather=1.4, pad=8)
    art = GP(art, m, "#fffdf6", "#f1ebe0", seed=nx(), rough=1.0, streak=0.4, pad=8)
    art = G(art, np.clip((m - gaussian_filter(m, 1.2)) * 3, 0, 1), "#9c8778", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=0.4, pad=6)
    art = G(art, circles(W, H, [(x, y, r * 0.16)]), "#c9b86a", "#9aa45a", seed=nx(), density=0.8, edge=0.3, rough=0.8, pad=6)
    return art


def melati_string(art, W, H, pts, rng, nx, size=7.0):
    """Roncean melati: chain of white buds along a drooping curve, every few a small open flower."""
    thread = strokes(W, H, [(pts, 1.2, None)])
    art = G(art, thread, "#8f8a6a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, feather=0.4)
    buds, opens = [], []
    step = size * 1.55
    acc = 0.0
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        acc += d
        if acc >= step:
            acc = 0
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            if rng.random() < 0.18:
                opens.append(b)
            else:
                buds.append((b[0], b[1], size * rng.uniform(0.85, 1.05), size * 0.55, math.degrees(ang)))
    m = ellipses(W, H, buds)
    art = G(art, np.roll(np.roll(m, 2, 0), 1, 1), "#b5a89c", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1, feather=1.2, pad=8)
    art = GP(art, m, "#fffcf3", "#eee6d6", seed=nx(), rough=0.8, streak=0.4, pad=8)
    art = G(art, np.clip((m - gaussian_filter(m, 1.1)) * 3, 0, 1), "#9c8778", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    for (x, y) in opens:
        art = white_flower(art, W, H, x, y, size * 1.3, rng, nx)
    return art


def orchid(art, W, H, x, y, r, rng, nx, rot=0.0):
    """White moth orchid: 3 narrow sepals, 2 broad petals, a maroon-pink lip."""
    polys = []
    for k, a in enumerate([-math.pi / 2, math.pi / 2 + 0.75, math.pi / 2 - 0.75]):
        polys.append(petal_pts(x, y, r * 1.0, r * 0.3, a + rot, n=12))
    broad = [shapes(W, H, [deform(ellipse_pts(x + math.cos(a + rot) * r * .5, y + math.sin(a + rot) * r * .5, r * .55, r * .48, 12, a + rot), rng, 1, .05)])
             for a in (math.pi - 0.15, 0.15)]
    sep = shapes(W, H, polys)
    allm = np.maximum.reduce([sep] + broad)
    art = G(art, np.roll(np.roll(allm, 3, 0), 2, 1), "#b8a5ad", seed=nx(), density=0.35, edge=0.3, bloom=0, rough=2, feather=1.8, pad=10)
    art = GP(art, sep, "#fbf7f2", "#ece2de", seed=nx(), rough=1.2, pad=8)
    art = G(art, np.clip((sep - gaussian_filter(sep, 1.3)) * 3, 0, 1), "#a08a90", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4, pad=6)
    for b in broad:
        art = GP(art, b, "#fffdf8", "#f1e6e2", seed=nx(), rough=1.4, pad=8)
        art = G(art, np.clip((b - gaussian_filter(b, 1.3)) * 3, 0, 1), "#a08a90", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4, pad=6)
        art = G(art, b * np.clip(1 - gaussian_filter(b, 6) * 1.25, 0, 1) * 2, "#d9c4c9", seed=nx(), density=0.3, edge=0.2, bloom=0, rough=1, pad=8)
    lip = shapes(W, H, [deform(petal_pts(x, y + r * .05, r * .55, r * .22, math.pi / 2 + rot, n=10), rng, 1, .06)])
    art = G(art, lip, "#a8384c", MAROON, seed=nx(), density=0.85, edge=0.6, rough=1.4, pad=8)
    art = G(art, circles(W, H, [(x, y - r * 0.02, r * 0.12)]), "#e0b64e", seed=nx(), density=0.8, edge=0.4, rough=0.6, pad=6)
    return art


def dots(art, W, H, rng, nx, cx, cy, sx, sy, n, col):
    items = [(cx + rng.gauss(0, sx), cy + rng.gauss(0, sy), rng.uniform(1.4, 4.2)) for _ in range(n)]
    items = [(x, y, r) for x, y, r in items if 4 < x < W - 4 and 4 < y < H - 4]
    return G(art, circles(W, H, items), col, seed=nx(), density=0.5, edge=0.25, bloom=0, rough=1, feather=0.5)


def bouquet(W, H, seed, scale=1.0, flip_orchid=False, origin=None):
    """Corner bouquet anchored at bottom-left (origin); spills up and to the right."""
    rng = random.Random(seed); nx = Seq(seed * 100)
    ox, oy = origin or (20, H - 10)
    S = scale
    back = blank(W, H)
    rose_area = np.zeros((H, W), np.float32)
    flowers = blank(W, H)
    # roses (hero), painted first so leaves can tuck behind
    specs = [(0.36, 0.66, 98, RED, OXBLOOD), (0.60, 0.80, 80, "#8e2430", OXBLOOD), (0.20, 0.44, 74, "#c2464a", MAROON),
             (0.52, 0.56, 58, "#d0606a", "#7c1f2b")]
    for fx, fy, r, mid, deep in specs:
        flowers = rose(flowers, W, H, W * fx, H * fy, r * S, rng, nx, mix(mid, "#f1c9bd", 0.3), mid, deep, rose_area)
    # leaves behind
    for (a, L, wd) in [(-1.25, 0.95, 46), (-0.85, 1.0, 52), (-0.45, 0.92, 44), (-0.15, 0.8, 40)]:
        L *= H * 0.72 * S
        p = curve([(ox, oy), (ox + math.cos(a) * L * .35, oy + math.sin(a) * L * .35 - 10), (ox + math.cos(a + .12) * L * .7, oy + math.sin(a + .12) * L * .7),
                   (ox + math.cos(a + .3) * L, oy + math.sin(a + .3) * L + 20)], 30)
        back = banana(back, W, H, p, wd * S, rng, nx)
    pandan = []
    for a in [-1.45, -1.05, -0.62, -0.28, 0.02]:
        L = H * rng.uniform(0.62, 0.86) * S
        pandan.append(blade(W, H, curve([(ox + 30, oy - 20), (ox + 30 + math.cos(a) * L * .55, oy - 20 + math.sin(a) * L * .55),
                                         (ox + 30 + math.cos(a + .25) * L, oy - 20 + math.sin(a + .25) * L + 30)], 24), 11 * S))
    pm = shapes(W, H, pandan)
    back = G(back, pm, "#6f925a", "#3d5f3a", seed=nx(), density=0.62, edge=0.55, bloom=0.3, rough=3)
    back = G(back, strokes(W, H, [(curve([(ox + 30, oy - 20), (ox + 30 + math.cos(a) * H * .4 * S, oy - 20 + math.sin(a) * H * .4 * S)], 12), 1.4, (0.1, 0.5)) for a in [-1.45, -1.05, -0.62, -0.28]]) * pm,
             LEAF_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=0.5)
    for (fx, fy, L, a) in [(0.48, 0.42, 150, -1.0), (0.70, 0.62, 140, -0.3), (0.12, 0.62, 130, -2.0), (0.80, 0.86, 120, 0.15), (0.30, 0.28, 120, -1.6),
                           (0.42, 0.90, 110, 0.5), (0.86, 0.72, 100, -0.5)]:
        back = leaf(back, W, H, W * fx, H * fy, L * S, a, rng, nx, c=random.Random(int(fx * 100)).choice([(LEAF_A, LEAF_B), ("#93a675", "#5d7a4c"), ("#728d5c", "#3f5d3b")]))
    back = knockout(back, rose_area, amount=0.94, grow=4)
    art = glaze(back, flowers)
    # orchid spray arching out to the right
    stem = curve([(W * .52, H * .58), (W * .70, H * .47), (W * .85, H * .45), (W * .97, H * .52)], 40)
    art = G(art, strokes(W, H, [(stem, 3.2 * S, (0.02, 0.4))]), "#6d7f4e", "#4a5a33", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1, feather=0.6)
    for k, t in enumerate([0.30, 0.55, 0.80]):
        px, py = stem[int(t * (len(stem) - 1))]
        art = orchid(art, W, H, px, py + 6 * S, (34 - k * 4) * S, rng, nx, rot=rng.uniform(-.25, .25))
    ex, ey = stem[-1]
    art = G(art, ellipses(W, H, [(ex, ey, 9 * S, 6 * S, 30)]), "#dfe2c6", "#a8b07a", seed=nx(), density=0.7, edge=0.5, rough=1)
    # melati strings draping from the heart of the bouquet
    for (p0, p1, p2) in [((0.42, 0.70), (0.62, 0.95), (0.95, 0.93)), ((0.30, 0.74), (0.50, 0.99), (0.80, 1.0)), ((0.24, 0.50), (0.10, 0.20), (0.18, 0.04))]:
        pts = curve([(W * p0[0], H * p0[1]), (W * p1[0], H * p1[1]), (W * p2[0], H * p2[1])], 90)
        pts = [(x, min(H - 8, y)) for x, y in pts]
        art = melati_string(art, W, H, pts, rng, nx, size=7.5 * S)
    # loose melati blossoms tucked between the roses
    for fx, fy in [(0.47, 0.70), (0.28, 0.58), (0.70, 0.71), (0.12, 0.52), (0.40, 0.48)]:
        art = white_flower(art, W, H, W * fx, H * fy, 13 * S, rng, nx)
    for (fx, fy, s_, a) in [(0.08, 0.30, 16, -1.9), (0.78, 0.36, 15, -0.7), (0.92, 0.66, 13, 0.1)]:
        art = bud(art, W, H, W * fx, H * fy, s_ * S, a, rng, nx, "#c4474f", OXBLOOD)
    art = dots(art, W, H, rng, nx, W * .5, H * .55, W * .3, H * .25, 26, "#b6454c")
    return art




# ---------------------------------------------------------------- architecture
def _trap(cx, y0, y1, w0, w1, sag=0.0, n=10):
    """Roof tier: bottom edge at y0 (width w0), top edge at y1 (width w1); sides curve concave by `sag`."""
    L = []; R = []
    for i in range(n + 1):
        t = i / n
        y = y0 + (y1 - y0) * t
        hw = (w0 + (w1 - w0) * t) / 2 - sag * math.sin(math.pi * t) * (w0 - w1) * 0.5
        L.append((cx - hw, y)); R.append((cx + hw, y))
    return L + R[::-1]


def joglo_masks(W, H, cx, by, w):
    """Masks for a joglo pendopo (side view): dict of roof tiers, under-eave shadows, posts, platform, ridge, tiles."""
    m = {}
    t_em, t_pn, t_br, t_top = by - 0.30 * w, by - 0.43 * w, by - 0.56 * w, by - 0.86 * w
    emper = _trap(cx, t_em, t_pn, 1.12 * w, 0.70 * w, 0.16)
    pen = _trap(cx, t_pn + 0.012 * w, t_br, 0.74 * w, 0.46 * w, 0.12)
    bru = _trap(cx, t_br + 0.012 * w, t_top, 0.48 * w, 0.15 * w, 0.22)
    m["emper"] = shapes(W, H, [emper], smooth=False)
    m["pen"] = shapes(W, H, [pen], smooth=False)
    m["bru"] = shapes(W, H, [bru], smooth=False)
    # eave shadow bands beneath each tier
    m["shadow"] = shapes(W, H, [[(cx - 0.52 * w, t_em), (cx + 0.52 * w, t_em), (cx + 0.47 * w, t_em + 0.035 * w), (cx - 0.47 * w, t_em + 0.035 * w)],
                                [(cx - 0.35 * w, t_pn + 0.01 * w), (cx + 0.35 * w, t_pn + 0.01 * w), (cx + 0.33 * w, t_pn + 0.03 * w), (cx - 0.33 * w, t_pn + 0.03 * w)],
                                [(cx - 0.23 * w, t_br + 0.01 * w), (cx + 0.23 * w, t_br + 0.01 * w), (cx + 0.22 * w, t_br + 0.028 * w), (cx - 0.22 * w, t_br + 0.028 * w)]], smooth=False)
    # posts (saka) + umpak bases + lintel
    posts = []
    xs = [-0.44, -0.30, -0.12, 0.12, 0.30, 0.44]
    for f in xs:
        x = cx + f * w; pw = 0.022 * w if abs(f) > 0.2 else 0.028 * w
        posts.append([(x - pw / 2, t_em + 0.03 * w), (x + pw / 2, t_em + 0.03 * w), (x + pw / 2, by - 0.045 * w), (x - pw / 2, by - 0.045 * w)])
    m["posts"] = shapes(W, H, posts, smooth=False)
    m["umpak"] = shapes(W, H, [[(cx + f * w - 0.026 * w, by - 0.02 * w), (cx + f * w + 0.026 * w, by - 0.02 * w), (cx + f * w + 0.018 * w, by - 0.05 * w), (cx + f * w - 0.018 * w, by - 0.05 * w)] for f in xs], smooth=False)
    m["lintel"] = shapes(W, H, [[(cx - 0.47 * w, t_em + 0.03 * w), (cx + 0.47 * w, t_em + 0.03 * w), (cx + 0.47 * w, t_em + 0.05 * w), (cx - 0.47 * w, t_em + 0.05 * w)]], smooth=False)
    # carved gebyok panel behind the central posts
    m["gebyok"] = shapes(W, H, [[(cx - 0.12 * w, t_em + 0.05 * w), (cx + 0.12 * w, t_em + 0.05 * w), (cx + 0.12 * w, by - 0.045 * w), (cx - 0.12 * w, by - 0.045 * w)]], smooth=False)
    m["platform"] = shapes(W, H, [[(cx - 0.56 * w, by - 0.02 * w), (cx + 0.56 * w, by - 0.02 * w), (cx + 0.6 * w, by + 0.03 * w), (cx - 0.6 * w, by + 0.03 * w)],
                                  [(cx - 0.18 * w, by + 0.03 * w), (cx + 0.18 * w, by + 0.03 * w), (cx + 0.21 * w, by + 0.07 * w), (cx - 0.21 * w, by + 0.07 * w)]], smooth=False)
    # ridge + curled wuwung ornaments at both ends and the centre
    ridge = [(curve([(cx - 0.075 * w, t_top), (cx + 0.075 * w, t_top)], 6), 0.012 * w, None)]
    for sgn in (-1, 1):
        ex = cx + sgn * 0.075 * w
        ridge.append((curve([(ex, t_top), (ex + sgn * 0.01 * w, t_top - 0.03 * w), (ex - sgn * 0.004 * w, t_top - 0.05 * w), (ex - sgn * 0.016 * w, t_top - 0.04 * w)], 14), 0.008 * w, (0.0, 0.5)))
    ridge.append((curve([(cx, t_top), (cx, t_top - 0.035 * w)], 6), 0.007 * w, (0.0, 0.6)))
    m["ridge"] = strokes(W, H, ridge)
    # roof tile courses (horizontal lines, clipped later by roof masks)
    lines = []
    for (y0, y1, w0, w1, k) in [(t_em, t_pn, 1.12 * w, 0.70 * w, 7), (t_pn, t_br, 0.74 * w, 0.46 * w, 6), (t_br, t_top, 0.48 * w, 0.15 * w, 11)]:
        for j in range(1, k):
            t = j / k; y = y0 + (y1 - y0) * t; hw = (w0 + (w1 - w0) * t) / 2
            lines.append(([(cx - hw, y), (cx + hw, y)], max(1.0, 0.0035 * w), None))
    m["tiles"] = strokes(W, H, lines)
    m["all"] = np.maximum.reduce([m[k] for k in ("emper", "pen", "bru", "posts", "umpak", "lintel", "gebyok", "platform", "ridge")])
    return m


def joglo_wash(W, H, cx, by, w, light, mid, dark, nx, density=1.0):
    """Faded watercolour joglo: tiers glazed light→dark, posts, eave shadows and tile courses as dry strokes."""
    m = joglo_masks(W, H, cx, by, w)
    a = blank(W, H)
    d = density
    a = G(a, m["platform"], light, mid, seed=nx(), density=0.42 * d, edge=0.4, bloom=0.4, rough=4)
    a = G(a, np.maximum(m["posts"], m["umpak"]), mid, dark, seed=nx(), density=0.55 * d, edge=0.5, bloom=0.2, rough=2)
    a = G(a, m["gebyok"], light, mid, seed=nx(), density=0.3 * d, edge=0.5, bloom=0.5, rough=3)
    a = G(a, m["lintel"], mid, dark, seed=nx(), density=0.6 * d, edge=0.4, rough=1.5)
    for k, key in enumerate(("emper", "pen", "bru")):
        a = G(a, m[key], mix(light, mid, 0.2 + k * 0.25), mid, seed=nx(), density=(0.5 + 0.1 * k) * d, edge=0.55, bloom=0.4, rough=4, holes=0.03)
    roof = np.maximum.reduce([m["emper"], m["pen"], m["bru"]])
    a = G(a, m["tiles"] * roof, dark, seed=nx(), density=0.34 * d, edge=0.1, bloom=0, rough=1.2, feather=0.6)
    a = G(a, m["shadow"], dark, seed=nx(), density=0.6 * d, edge=0.3, bloom=0, rough=1.5)
    a = G(a, m["ridge"], dark, seed=nx(), density=0.75 * d, edge=0.3, bloom=0, rough=1, feather=0.6)
    # carved lattice hint in the gebyok
    gx0, gx1 = cx - 0.11 * w, cx + 0.11 * w
    gy0, gy1 = by - 0.30 * w + 0.06 * w, by - 0.05 * w
    lat = []
    for j in range(5):
        x = gx0 + (gx1 - gx0) * (j + 0.5) / 5
        lat.append(([(x, gy0), (x, gy1)], max(1, 0.004 * w), None))
    lat.append(([(gx0, (gy0 + gy1) / 2), (gx1, (gy0 + gy1) / 2)], max(1, 0.004 * w), None))
    a = G(a, strokes(W, H, lat), dark, seed=nx(), density=0.35 * d, edge=0.1, bloom=0, rough=1, feather=0.6)
    return a, m


def palm(W, H, x, by, h, rng, lean=0.1):
    """Coconut palm mask: curved trunk + drooping fronds."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.3, by - h * 0.5), top], 30)
    items = [(trunk, h * 0.025, (0.02, 0.6))]
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.1, 0.1)
        L = h * rng.uniform(0.32, 0.45)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5 - h * 0.02),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.45)], 24)
        items.append((pts, h * 0.022, (0.1, 0.5)))
        for j in range(3, 22, 2):  # leaflets
            px, py = pts[j]; qa = a + (1.2 if j % 4 == 1 else -1.2)
            items.append(([(px, py), (px + math.cos(qa + 0.6) * L * 0.18, py + math.sin(qa + 0.6) * L * 0.18 + L * 0.06)], h * 0.006, (0.1, 0.7)))
    return strokes(W, H, items)


def hills(W, H, y, amp, seed, wl=0.5):
    rng = random.Random(seed)
    pts = [(-20, H + 20)]
    ph = rng.uniform(0, 6)
    for i in range(0, W + 41, 20):
        pts.append((i - 20, y - amp * (0.6 * math.sin(i / (W * wl) * math.pi * 2 + ph) + 0.4 * math.sin(i / (W * wl * 0.37) + ph * 2)) ** 1))
    pts.append((W + 20, H + 20))
    return shapes(W, H, [pts], smooth=False)


# ---------------------------------------------------------------- carving (ukiran lung-lungan)
def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in [i / (n - 1) for i in range(n)]]


def lung(x, y, s, ang, flip=1):
    """One lung-lungan motif (S-scroll with a curled tendril and two leaves) as (stroke items, leaf polys)."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        v *= flip
        return (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    stem = curve([P(-0.9, 0.15), P(-0.4, -0.25), P(0.1, -0.05), P(0.5, 0.25), P(0.85, 0.05)], 30)
    # curl at the head
    hx, hy = P(0.85, 0.05)
    cur = spiral_pts(hx, hy - 0.001, s * 0.26, s * 0.04, ang - math.pi / 2 * flip, 0.9, 30, -flip)
    cur = [(px + (hx - cur[0][0]), py + (hy - cur[0][1])) for px, py in cur]
    tend = curve([P(-0.2, -0.2), P(-0.05, -0.55), P(0.2, -0.6), P(0.28, -0.42)], 20)
    items = [(stem, s * 0.13, (0.15, 0.1)), (cur, s * 0.1, (0.0, 0.55)), (tend, s * 0.05, (0.1, 0.5))]
    leaves = [petal_pts(*P(-0.5, -0.2), s * 0.7, s * 0.24, ang + flip * 2.4, n=10),
              petal_pts(*P(0.25, 0.15), s * 0.6, s * 0.2, ang + flip * 0.9, n=10)]
    return items, leaves


def carve(W, H, band, items, leaves, nx, base=None, light=None, dark=None, gold=None, gold_amt=0.55, seed=7):
    """Paint a carved-teak band: gouache wood, recessed ground, raised relief with light/shadow and worn gold leaf."""
    base = base or TEAK; light = light or TEAK_L; dark = dark or TEAK_D; gold = gold or GOLD
    relief = np.maximum(strokes(W, H, items), shapes(W, H, leaves)) * band
    art = GP(blank(W, H), band, base, dark, seed=nx(), rough=2.0, streak=0.9, pad=12)
    ground = np.clip(band - gaussian_filter(relief, 2.5) * 1.6, 0, 1) * band
    art = G(art, ground, dark, seed=nx(), density=0.55, edge=0.35, bloom=0.2, rough=1.5, feather=0.8)
    art = GP(art, relief, light, base, seed=nx(), rough=1.2, streak=0.7, pad=10)
    hi = np.clip(relief - np.roll(np.roll(relief, 2, 0), 2, 1), 0, 1)
    lo = np.clip(relief - np.roll(np.roll(relief, -2, 0), -2, 1), 0, 1)
    art = G(art, lo, dark, seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    art = OV(art, hi, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(mix(light, "#fff1d6", 0.5)), np.float32), (m * 0.55)[..., None]], -1))
    if gold_amt:
        wear = fbm(W, H, seed, 14, 3)
        gm = relief * np.clip((wear - (1 - gold_amt)) * 4, 0, 1)
        art = FO(art, gm, gold, seed=nx(), emboss=0.5, sparkle=0.1)
    # band edge mouldings
    edge = np.clip(band - gaussian_filter(band, 1.5) * 1.15, 0, 1) * 3
    art = G(art, np.clip(edge, 0, 1), dark, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5)
    return art


def along(pts, step):
    """Resample a polyline at roughly fixed arc length; yields (x, y, angle)."""
    out = []; acc = step / 2
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out


# ---------------------------------------------------------------- wayang kulit (original, stylised)
def _offset_poly(pts, d):
    """Shrink a closed polygon by d along vertex normals (approximate; good for gentle shapes)."""
    n = len(pts); out = []
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        tx, ty = c[0] - a[0], c[1] - a[1]; L = math.hypot(tx, ty) or 1
        nx_, ny_ = -ty / L, tx / L
        if (b[0] - cx) * nx_ + (b[1] - cy) * ny_ > 0:
            nx_, ny_ = -nx_, -ny_
        out.append((b[0] + nx_ * d, b[1] + ny_ * d))
    return out


def wayang_masks(W, H, ox, oy, s, kind="putra", face=1):
    """Stylised wayang-kulit figure in a 100x260 unit box facing right (face=-1 mirrors). Original design.
    Masks: body (leather), holes (openwork), face, crown, kain (painted cloth), trim (gilt), sticks (cempurit)."""
    def P(x, y):
        if face < 0:
            x = 100 - x
        return (ox + x * s, oy + y * s)
    def poly(pts):
        return [P(*p) for p in pts]
    if kind == "putra":
        crown = [(41, 42), (36, 26), (40, 15), (45, 20), (48, 5), (53, 17), (59, 21), (62, 30), (61, 37)]
        headbody = [(61, 37), (70, 40), (81, 45), (68, 47), (64, 53), (57, 57), (57, 63), (64, 73), (62, 103), (45, 103), (40, 75), (44, 62), (42, 52), (41, 42)]
        kain = [(43, 99), (62, 99), (70, 140), (87, 190), (71, 184), (63, 196), (60, 238), (46, 238), (42, 196), (34, 186), (19, 192), (34, 140)]
        arms = [([(61, 66), (72, 98), (83, 128)], 4.0), ([(45, 66), (37, 98), (27, 126)], 4.0)]
        legs = [([(57, 192), (66, 236), (84, 242)], 5.0), ([(48, 192), (40, 236), (23, 241)], 5.0)]
        curl = (37, 36, 8.5)
        facem = [(61, 37), (70, 40), (81, 45), (68, 47), (64, 53), (57, 57), (55, 46)]
    else:
        crown = [(43, 38), (38, 27), (41, 17), (49, 13), (57, 17), (59, 26), (57, 34)]
        headbody = [(57, 34), (65, 41), (71, 47), (62, 48), (60, 54), (55, 57), (56, 63), (61, 72), (59, 100), (46, 100), (42, 74), (46, 62), (44, 50), (43, 38)]
        kain = [(45, 96), (60, 96), (66, 150), (74, 212), (63, 220), (59, 244), (47, 244), (44, 220), (33, 212), (39, 150)]
        arms = [([(58, 66), (66, 96), (70, 124)], 3.5), ([(46, 66), (41, 96), (36, 122)], 3.5)]
        legs = [([(55, 240), (64, 248)], 4.0), ([(50, 240), (41, 248)], 4.0)]
        curl = (39, 26, 6.5)
        facem = [(57, 34), (65, 41), (71, 47), (62, 48), (60, 54), (55, 57), (53, 44)]
    crown_m = shapes(W, H, [poly(crown)], smooth=False)
    body_m = shapes(W, H, [poly(headbody)], smooth=True)
    kain_m = shapes(W, H, [poly(kain)], smooth=False)
    limbs = strokes(W, H, [(curve([P(*q) for q in a], 16), w * s, (0.05, 0.3)) for a, w in arms + legs] +
                    [(spiral_pts(*P(curl[0], curl[1]), curl[2] * s, 1.5 * s, 0, 1.15, 36, -face), 2.4 * s, (0.0, 0.4))])
    body = gaussian_filter(np.maximum.reduce([crown_m, body_m, kain_m, limbs]), 0.5)
    # openwork: a dotted line just inside the kain and torso contours, slits in diagonal rows (parang-like), crown lace
    items = []
    for shape, d, step in [(kain, 3.2, 4.6), (headbody[6:12], 3.0, 4.6)]:
        inner = _offset_poly(shape, d) if shape is kain else [(x - 3 * (1 if x > 52 else -1), y) for x, y in shape]
        for (x, y, _a) in along([P(*q) for q in inner] + ([P(*inner[0])] if shape is kain else []), step * s):
            items.append((x, y, 0.95 * s))
    holes = circles(W, H, items)
    slits = []
    for k in range(-6, 12):
        x0 = 30 + k * 7
        slits.append(([P(x0, 120), P(x0 + 30, 200)], 1.2 * s, (0.2, 0.2)))
    slit_m = strokes(W, H, slits) * np.clip(gaussian_filter(kain_m, 5 * s) * 2.4 - 1.25, 0, 1)
    torso_slits = strokes(W, H, [(curve([P(47, 76), P(52, 84), P(57, 76)], 12), 1.1 * s, (0.2, 0.2)), (curve([P(47, 88), P(52, 96), P(57, 88)], 12), 1.1 * s, (0.2, 0.2))])
    crown_lace = circles(W, H, [(*P(x, y), 0.9 * s) for x, y in ([(44, 28), (47, 22), (50, 12), (53, 22), (56, 28), (48, 34), (55, 34)] if kind == "putra" else [(46, 22), (50, 19), (54, 22), (49, 29)])])
    holes = np.clip(holes + slit_m * 0.9 + torso_slits + crown_lace, 0, 1) * np.clip(gaussian_filter(body, 1.2) * 1.6 - 0.5, 0, 1)
    face_m = shapes(W, H, [poly(facem)], smooth=True) * body_m
    trim = strokes(W, H, [(curve([P(45, 63), P(51, 70), P(57, 63)], 12), 1.7 * s, None), (curve([P(43, 100), P(62, 100)], 6), 2.6 * s, None),
                          (curve([P(*q) for q in crown[:5]], 14), 1.3 * s, None), (curve([P(38, 118), P(52, 128), P(66, 118)], 12), 1.3 * s, None)])
    hand_f = P(*arms[0][0][-1]); hand_b = P(*arms[1][0][-1])
    sticks = strokes(W, H, [([hand_f, (hand_f[0] + 3 * s * face, oy + 262 * s)], 1.2 * s, None), ([hand_b, (hand_b[0] - 3 * s * face, oy + 260 * s)], 1.2 * s, None),
                            ([P(52, 64), P(52, 266)], 1.5 * s, None)])
    return {"body": body, "holes": holes, "face": face_m, "crown": crown_m, "kain": kain_m, "trim": trim, "sticks": sticks}


def kawung_tile(n, cell, width=0.0, fat=0.33):
    """Seamless kawung mask (n x n px, n multiple of cell): four diagonal petals around every lattice point,
    so neighbouring flowers share their tips (the classic kawung lattice)."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style if width else skia.Paint.kFill_Style, StrokeWidth=width or 1)
        c = cell; L = c * 0.6; R = c * fat
        for gx in range(-1, n // c + 2):
            for gy in range(-1, n // c + 2):
                cx, cy = gx * c, gy * c
                for k in range(4):
                    a = 45 + k * 90
                    cv.c.save(); cv.c.translate(cx + math.cos(math.radians(a)) * c * 0.25, cy + math.sin(math.radians(a)) * c * 0.25); cv.c.rotate(a)
                    cv.c.drawOval(skia.Rect(-L * 0.5, -R * 0.5, L * 0.5, R * 0.5), p)
                    cv.c.restore()
    return mask_from(n, n, draw)
