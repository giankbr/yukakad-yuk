"""Joglo Marun — cream & maroon adat Jawa: carved teak gebyok arch frame with worn gold leaf, faded watercolour joglo,
red/maroon rose + melati + orchid + banana/pandan bouquets, melati-rose sprig divider, paper.
Run: python3 -I /tmp/pen/art/themes/joglo-marun.py [part ...]   parts: bouquet cluster frame joglo sprig paper
Assets -> /root/w/frontend/public/themes/art/joglo-marun/
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *
import _jw_lib as jw

OUT = outdir("joglo-marun")
PARTS = sys.argv[1:] or ["bouquet", "cluster", "frame", "joglo", "sprig", "paper"]
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


# ---------------------------------------------------------------- parts
if "bouquet" in PARTS:
    W, H = 640, 720
    art = bouquet(W, H, 11)
    preview(art, "jm-bouquet", CREAM)
    save(art, f"{OUT}/bouquet.webp", max_w=600, quality=80)

if "cluster" in PARTS:
    W, H = 420, 360
    rng = random.Random(23); nx = Seq(2300)
    area = np.zeros((H, W), np.float32)
    fl = blank(W, H)
    fl = rose(fl, W, H, 150, 120, 62, rng, nx, "#ecc3bb", RED, OXBLOOD, area)
    fl = rose(fl, W, H, 255, 70, 42, rng, nx, "#efcdc4", "#9a2934", OXBLOOD, area)
    bk = blank(W, H)
    for (x, y, L, a) in [(140, 100, 200, 0.35), (160, 130, 170, 1.05), (120, 110, 150, 2.1), (240, 80, 150, -0.1), (190, 100, 130, 0.75)]:
        bk = leaf(bk, W, H, x, y, L, a, rng, nx)
    p = curve([(110, 100), (220, 150), (320, 170), (400, 150)], 30)
    bk = banana(bk, W, H, p, 30, rng, nx)
    bk = knockout(bk, area, amount=0.94, grow=4)
    art = glaze(bk, fl)
    pts = curve([(170, 160), (215, 255), (300, 300), (370, 270)], 70)
    art = melati_string(art, W, H, pts, rng, nx, size=6.5)
    art = white_flower(art, W, H, 210, 135, 12, rng, nx)
    art = white_flower(art, W, H, 90, 160, 11, rng, nx)
    art = bud(art, W, H, 330, 60, 13, -0.3, rng, nx, "#c4474f", OXBLOOD)
    art = dots(art, W, H, rng, nx, 230, 160, 90, 60, 14, "#b6454c")
    preview(art, "jm-cluster", CREAM)
    save(art, f"{OUT}/cluster.webp", max_w=400, quality=80)

if "sprig" in PARTS:
    W, H = 360, 90
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    stem = curve([(28, 52), (110, 44), (180, 47), (250, 44), (332, 52)], 60)
    art = G(art, strokes(W, H, [(stem, 2.0, (0.1, 0.1))]), "#6d7f4e", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.8, feather=0.5, pad=8)
    for (x, y, a, L) in [(120, 44, -2.6, 46), (240, 44, -0.5, 46), (90, 48, 2.7, 40), (270, 48, 0.4, 40), (60, 50, -2.9, 30), (300, 50, -0.2, 30)]:
        art = leaf(art, W, H, x, y, L, a, rng, nx)
    area = np.zeros((H, W), np.float32)
    art = rose(art, W, H, 180, 45, 24, rng, nx, "#ecc3bb", RED, OXBLOOD, area)
    for x in (146, 214):
        art = white_flower(art, W, H, x, 44 + rng.uniform(-3, 3), 9.5, rng, nx)
    for x, y in [(44, 52), (318, 52), (100, 41), (262, 41)]:
        art = white_flower(art, W, H, x, y, 6.5, rng, nx, petals=5)
    preview(art, "jm-sprig", CREAM)
    save(art, f"{OUT}/sprig.webp", quality=84)

if "paper" in PARTS:
    img = paper(400, 400, CREAM, seed=44, fiber=0.8, mottle=0.9)
    a = np.asarray(img, np.float32) / 255
    g = wrap_noise(400, 400, 9, 22)
    a = np.clip(a * (0.985 + 0.03 * g[..., None]), 0, 1)
    save_texture(Image.fromarray((a * 255).astype(np.uint8)), f"{OUT}/paper.webp", quality=74)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")

if "frame" in PARTS:
    # carved teak gebyok arch (ukiran lung-lungan, worn gold leaf) framing the cream cover panel; crown on the apex
    W, H = 640, 980
    nx = Seq(4100)
    cx, r, top, BW = 320, 286, 430, 58
    def arch(off):
        pts = arc_pts(cx, top, r - off, math.pi, 2 * math.pi, 80)
        return [(cx - r + off, H + 10)] + pts + [(cx + r - off, H + 10)]
    band = np.clip(shapes(W, H, [arch(0)], smooth=False) - shapes(W, H, [arch(BW)], smooth=False), 0, 1)
    ct = top - r
    crown = shapes(W, H, [[(cx - 130, ct + 26), (cx - 84, ct - 34), (cx - 36, ct - 62), (cx, ct - 132), (cx + 36, ct - 62), (cx + 84, ct - 34), (cx + 130, ct + 26)]])
    band = np.maximum(band, crown)
    mid = arc_pts(cx, top, r - BW / 2, math.pi, 2 * math.pi, 100)
    path = [(cx - r + BW / 2, H)] + [(cx - r + BW / 2, top)] + mid + [(cx + r - BW / 2, top), (cx + r - BW / 2, H)]
    items, leaves = [], []
    for k, (x, y, a) in enumerate(jw.along(path, 50)):
        if abs(x - cx) < 60 and y < ct + 60:
            continue
        it, lv = jw.lung(x, y, 28, a, 1 if k % 2 else -1)
        items += it; leaves += lv
    for sgn in (-1, 1):
        for (u, v, s_, a) in [(14, -66, 44, -1.3), (60, -32, 36, -0.55), (100, 2, 28, -0.15)]:
            it, lv = jw.lung(cx + sgn * u, ct + v, s_, a if sgn > 0 else math.pi - a, sgn)
            items += it; leaves += lv
    leaves.append(petal_pts(cx, ct - 12, 104, 20, -math.pi / 2, n=12))
    art = jw.carve(W, H, band, items, leaves, nx, gold_amt=0.34)
    mo = np.clip(shapes(W, H, [arch(-3)], smooth=False) - shapes(W, H, [arch(7)], smooth=False), 0, 1)
    mi = np.clip(shapes(W, H, [arch(BW - 7)], smooth=False) - shapes(W, H, [arch(BW + 3)], smooth=False), 0, 1)
    art = GP(art, np.maximum(mo, mi), TEAK_L, TEAK, seed=nx(), rough=1, pad=8)
    art = FO(art, mi * np.clip((fbm(W, H, 4, 10, 3) - 0.5) * 3, 0, 1), GOLD, seed=nx(), sparkle=0.05)
    preview(art, "jm-frame", CREAM)
    save(art, f"{OUT}/frame.webp", max_w=560, quality=80)

if "joglo" in PARTS:
    # faded maroon-rose watercolour joglo pendopo with palms and a soft hill line behind
    W, H = 760, 560
    nx = Seq(5200); rng = random.Random(52)
    art = blank(W, H)
    art = G(art, jw.hills(W, H, 330, 26, 3, 0.9), "#e9d6cf", "#d9bdb3", seed=nx(), density=0.38, edge=0.35, bloom=0.5, rough=8)
    for (x, h, ln) in [(110, 300, -0.12), (160, 250, 0.08), (640, 290, 0.14), (700, 230, -0.05)]:
        art = G(art, jw.palm(W, H, x, 470, h, rng, ln), "#cfa79d", "#b48379", seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=2.5, feather=0.8)
    j, _ = jw.joglo_wash(W, H, 380, 500, 520, "#ead2c8", "#b97b72", "#6d2d2e", nx, density=0.95)
    art = glaze(art, j)
    preview(art, "jm-joglo", CREAM)
    save(art, f"{OUT}/joglo.webp", max_w=640, quality=78)
