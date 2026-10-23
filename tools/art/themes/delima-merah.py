"""Delima Merah — pomegranates in the manner of Islamic-world textile / ceramic ornament (botanical only, no figures, no
calligraphy): an ogee arch of pomegranate branches with fruits, split fruit showing its seeds, crinkled scarlet
blossoms and slender leaves, gouache on cream with a fine gold contour. Plus a sprig divider, a single blossom, a split
fruit emblem and a gold ogee-lattice tile.
Run: python3 -I delima-merah.py [part ...]  parts: arch sprig blossom split lattice
Assets -> public/themes/art/delima-merah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n3_lib import *

OUT = outdir("delima-merah")
PARTS = sys.argv[1:] or ["arch", "sprig", "blossom", "split", "lattice"]
RED, RED_L, RED_D, RED_DD = "#8e1b24", "#c0393a", "#62101a", "#3f0a11"
SCAR, SCAR_L = "#d3412f", "#ea6a45"
LEAF, LEAF_L, LEAF_D = "#4d6b3a", "#73905a", "#2e4528"
STEM = "#5b4a2e"
GOLD = "#c69a45"
CREAM = "#f6eddb"
PITH, PITH_D = "#f3d9c0", "#d9a98c"


def contour(art, m, col=RED_DD, w=1.4, seed=1):
    return ink(art, outline_out(m, w), col, seed=seed, wear=0.08, rough=0.7)


def gold_line(art, m, seed=1):
    return FO(art, m, GOLD, seed=seed, emboss=0.3, sparkle=0.12)


def leaf_one(art, W, H, x, y, L, ang, nx, rng, curl=0.0):
    poly = petal_pts(x, y, L, L * 0.2, ang, n=16, cup=curl)
    m = shapes(W, H, [poly])
    art = GP(art, m, LEAF, LEAF_L, seed=nx(), rough=1.0, streak=0.7)
    half = shapes(W, H, [petal_pts(x, y, L * 0.96, L * 0.09, ang + 0.05, n=14, cup=curl)])
    art = G(art, half * m, LEAF_D, seed=nx(), density=0.45, edge=0.2, bloom=0.1, rough=1.2, feather=0.8, pad=8)
    vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in (0.05, 0.3, 0.6, 0.85)]
    art = ink(art, strokes(W, H, [(vein, 1.3, (0.05, 0.5))]), LEAF_D, seed=nx(), wear=0.1)
    return contour(art, m, LEAF_D, 1.1, nx())


def fruit(art, W, H, x, y, r, nx, rng, tilt=0.0):
    """Whole pomegranate: rounded, slightly faceted body, highlight upper-left, crown of sepals."""
    pts = deform(ellipse_pts(x, y, r, r * 0.94, 12, tilt), rng, 1, 0.04)
    m = shapes(W, H, [pts])
    art = GP(art, m, RED, RED_L, seed=nx(), rough=1.0, streak=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(((xx - (x + r * 0.5)) ** 2 + (yy - (y + r * 0.45)) ** 2) ** 0.5 / (r * 1.25), 0, 1)
    art = G(art, m * (1 - d), RED_D, seed=nx(), density=0.55, edge=0.1, bloom=0.15, rough=2, feather=4)
    hl = shapes(W, H, [ellipse_pts(x - r * 0.38, y - r * 0.32, r * 0.3, r * 0.17, 12, -0.7)])
    art = tint(art, hl * m, "#e8725d", 0.55, blur=3)
    # crown
    cx_, cy_ = x + math.sin(tilt) * r * 0.9, y - math.cos(tilt) * r * 0.9
    crown = [[(cx_ - r * 0.24, cy_ + r * 0.12), (cx_ - r * 0.2, cy_ - r * 0.18), (cx_ + r * 0.2, cy_ - r * 0.18), (cx_ + r * 0.24, cy_ + r * 0.12)]]
    for k in range(5):
        a = -math.pi / 2 + tilt + (k - 2) * 0.42
        bx, by = cx_ + math.cos(a) * r * 0.16, cy_ - r * 0.12 + math.sin(a) * r * 0.06
        crown.append([(bx - r * 0.06, by), (bx + math.cos(a) * r * 0.3, by + math.sin(a) * r * 0.3), (bx + r * 0.06, by)])
    cm = shapes(W, H, crown, smooth=False)
    art = GP(art, cm, RED_D, RED, seed=nx(), rough=0.8)
    art = contour(art, np.maximum(m, cm), RED_DD, 1.4, nx())
    return art


def blossom(art, W, H, x, y, s, ang, nx, rng):
    """Pomegranate flower: fleshy bell calyx with pointed lobes, crinkled scarlet petals fanning out, gold stamens."""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    # petals (behind the calyx), opening along +u
    pets = []
    for k in range(5):
        a = (k - 2) * 0.42
        base = P(0.55, 0)
        tip = (base[0] + math.cos(ang + a) * s * 0.85, base[1] + math.sin(ang + a) * s * 0.85)
        mid = (base[0] + math.cos(ang + a) * s * 0.45, base[1] + math.sin(ang + a) * s * 0.45)
        w = s * 0.34
        nrm = (-math.sin(ang + a), math.cos(ang + a))
        poly = [base, (mid[0] + nrm[0] * w, mid[1] + nrm[1] * w), (tip[0] + nrm[0] * w * 0.6, tip[1] + nrm[1] * w * 0.6), tip,
                (tip[0] - nrm[0] * w * 0.6, tip[1] - nrm[1] * w * 0.6), (mid[0] - nrm[0] * w, mid[1] - nrm[1] * w)]
        pets.append(deform(poly, rng, 2, 0.05))
    pm = shapes(W, H, pets)
    art = GP(art, pm, SCAR, SCAR_L, seed=nx(), rough=1.4, streak=1.0)
    crinkle = []
    for p in pets:
        b, t = p[0], p[3]
        for j in (-1, 0, 1):
            crinkle.append(([(b[0] * 0.75 + t[0] * 0.25 + j * 3, b[1] * 0.75 + t[1] * 0.25 + j * 3), (b[0] * 0.2 + t[0] * 0.8 + j * 5, b[1] * 0.2 + t[1] * 0.8 + j * 5)], 1.2, (0.2, 0.5)))
    art = G(art, strokes(W, H, crinkle) * pm, "#a52a22", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1, feather=0.5, pad=8)
    art = contour(art, pm, "#7a1a16", 1.1, nx())
    # stamens
    st = []
    for k in range(7):
        a = ang + (k - 3) * 0.16
        b = P(0.6, 0)
        st.append(([b, (b[0] + math.cos(a) * s * 0.42, b[1] + math.sin(a) * s * 0.42)], 1.2, None))
    art = ink(art, strokes(W, H, st) * 0.6, "#d9a640", seed=nx(), wear=0.05)
    art = GP(art, circles(W, H, [(P(0.6, 0)[0] + math.cos(ang + (k - 3) * 0.16) * s * 0.44, P(0.6, 0)[1] + math.sin(ang + (k - 3) * 0.16) * s * 0.44, s * 0.05) for k in range(7)]), "#f2cf62", seed=nx(), rough=0.3)
    # calyx (bell / urn) with lobed rim
    cal = [P(-0.55, 0), P(-0.4, -0.16), P(0.1, -0.24), P(0.42, -0.36), P(0.66, -0.42), P(0.54, -0.2), P(0.62, -0.08),
           P(0.5, 0), P(0.62, 0.08), P(0.54, 0.2), P(0.66, 0.42), P(0.42, 0.36), P(0.1, 0.24), P(-0.4, 0.16)]
    cm = shapes(W, H, [cal])
    art = GP(art, cm, RED, "#a32a2c", seed=nx(), rough=0.8, streak=0.6)
    art = G(art, cm * shapes(W, H, [[P(-0.5, 0.02), P(0.6, 0.02), P(0.6, 0.44), P(-0.5, 0.2)]], smooth=False), RED_D, seed=nx(), density=0.5, edge=0.2, bloom=0.1, rough=1, feather=1.2, pad=8)
    art = tint(art, shapes(W, H, [[P(-0.3, -0.1), P(0.4, -0.2), P(0.4, -0.12), P(-0.3, -0.04)]]), "#d9605a", 0.5, blur=1.5)
    return contour(art, cm, RED_DD, 1.3, nx())


def stem(art, W, H, items, nx):
    m = strokes(W, H, items)
    art = GP(art, m, STEM, "#6e5a36", seed=nx(), rough=0.8, streak=0.6)
    return contour(art, m, "#3a2e1c", 1.0, nx())


def split_fruit(art, W, H, x, y, r, nx, rng):
    """Pomegranate broken open: red rind rim, cream pith walls, clusters of glossy arils."""
    outer = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 0.92, 14), rng, 1, 0.03)])
    art = GP(art, outer, RED, RED_L, seed=nx(), rough=1.0)
    art = contour(art, outer, RED_DD, 1.6, nx())
    inner_pts = deform(ellipse_pts(x, y + r * 0.04, r * 0.82, r * 0.74, 14), rng, 1, 0.05)
    im = shapes(W, H, [inner_pts])
    art = GP(art, im, PITH, "#f7e4cf", seed=nx(), rough=0.8)
    art = G(art, im, PITH_D, seed=nx(), density=0.3, edge=0.5, bloom=0.2, rough=2, feather=1.5)
    # chambers: pith walls radiate; arils fill the chambers
    walls = []
    for k in range(6):
        a = k * math.tau / 6 + 0.3
        walls.append(([(x, y + r * 0.04), (x + math.cos(a) * r * 0.82, y + r * 0.04 + math.sin(a) * r * 0.74)], r * 0.06, (0.2, 0.2)))
    wm = strokes(W, H, walls) * im
    ar = []
    tries = 0
    while len(ar) < 140 and tries < 4000:
        tries += 1
        rr = math.sqrt(rng.random()) * r * 0.72
        a = rng.uniform(0, math.tau)
        px, py = x + math.cos(a) * rr, y + r * 0.04 + math.sin(a) * rr * 0.9
        rad = r * rng.uniform(0.085, 0.11)
        if all((px - qx) ** 2 + (py - qy) ** 2 > (rad + qr) ** 2 * 0.62 for qx, qy, qr in ar):
            ar.append((px, py, rad))
    polys = [deform(ellipse_pts(px, py, rad, rad * 0.86, 7, rng.uniform(0, 3)), rng, 1, 0.06) for px, py, rad in ar]
    arm = shapes(W, H, polys) * im * (1 - np.clip(gaussian_filter(wm, 1.5) * 2.5, 0, 1))
    arm = np.clip(arm, 0, 1)
    art = tint(art, np.clip(gaussian_filter(arm, 2.5) * 1.6, 0, 1) * im, "#9a5a4a", 0.45)
    art = GP(art, arm, "#b01e2e", "#cf3343", seed=nx(), rough=0.4, streak=0.3)
    art = G(art, arm * np.clip(gaussian_filter(arm, 3) * -1 + 1.2, 0, 1), "#7a0f1e", seed=nx(), density=0.5, edge=0.6, bloom=0, rough=0.6, feather=0.6)
    art = tint(art, outline_out(shapes(W, H, polys), 0.7) * im, "#6a0c18", 0.8)
    glints = circles(W, H, [(px - rad * 0.32, py - rad * 0.34, rad * 0.24) for px, py, rad in ar])
    art = tint(art, glints * arm, "#fff1ec", 0.85, blur=0.5)
    return art


def arch():
    W, H = 640, 900
    rng = random.Random(5); nx = Seq(100)
    cx = W / 2
    half = blank(W, H)
    # pointed arch as a double gold band with dots between (left half; mirrored below)
    def arch_line(off):
        return curve([(cx - 206 - off, 900), (cx - 206 - off, 560), (cx - 204 - off, 380), (cx - 170 - off * 0.8, 250), (cx - 96 - off * 0.5, 160), (cx - 30, 108 - off), (cx + 2, 94 - off)], 90)
    outer, inner = arch_line(9), arch_line(-9)
    half = gold_line(half, strokes(W, H, [(outer, 3.4, None), (inner, 2.4, None)]), nx())
    mids = arch_line(0)
    dots_ = [(x, y, 2.6) for (x, y, _a) in along(mids, 22)]
    half = GP(half, circles(W, H, dots_), RED, seed=nx(), rough=0.3)
    # sinuous vine meandering across the arch band, rising from the bottom corner
    vine = []
    for i in range(0, len(mids) - 6):
        x, y = mids[i]
        (ax, ay), (bx, by) = mids[max(0, i - 1)], mids[i + 1]
        a = math.atan2(by - ay, bx - ax)
        w = math.sin(i * 0.36) * 22
        vine.append((x - math.sin(a) * w, y + math.cos(a) * w))
    leaves, fruits, flowers, buds = [], [], [], []
    for i in range(2, len(vine) - 2, 3):
        (ax, ay), (bx, by) = vine[i - 1], vine[i + 1]
        a = math.atan2(by - ay, bx - ax)
        for sgn in (-1, 1):
            if rng.random() < 0.9:
                leaves.append((vine[i][0], vine[i][1], rng.uniform(34, 46), a + sgn * rng.uniform(0.55, 0.85), sgn * 0.3))
    # ornaments at the meander crests (alternating fruit / blossom), away from the very top
    crest = [i for i in range(4, len(vine) - 10) if abs(math.sin(i * 0.36)) > 0.985]
    shoots = []
    for k, i in enumerate(crest):
        x, y = vine[i]
        out = 1 if math.sin(i * 0.36) > 0 else -1  # which side of the band the crest sits
        (ax, ay), (bx, by) = vine[i - 1], vine[i + 1]
        a = math.atan2(by - ay, bx - ax) + out * math.pi / 2
        inward = out > 0
        tip = (x + math.cos(a) * (16 if inward else 30), y + math.sin(a) * (16 if inward else 30))
        shoots.append(([(x, y), tip], 3.4, (0.05, 0.4)))
        if not inward:
            fruits.append((tip[0] + math.cos(a) * 16, tip[1] + math.sin(a) * 16, 27 if k % 4 < 2 else 23, a + math.pi / 2))
        else:
            flowers.append((tip[0], tip[1], 24, a))
    for (x, y, L, a, c) in leaves:
        half = leaf_one(half, W, H, x, y, L, a, nx, rng, curl=c)
    half = stem(half, W, H, [(vine, 6, (0.02, 0.3))] + shoots, nx)
    for (x, y, r, t) in fruits:
        half = fruit(half, W, H, x, y, r, nx, rng, tilt=t)
    for (x, y, sz, a) in flowers:
        half = blossom(half, W, H, x, y, sz, a, nx, rng)
    clear()
    art = over(half, np.ascontiguousarray(half[:, ::-1]))
    # crowning split fruit at the apex, leaves behind it
    art = leaf_one(art, W, H, cx - 34, 84, 60, math.pi * 0.92, nx, rng, 0.3)
    art = leaf_one(art, W, H, cx + 34, 84, 60, 0.08, nx, rng, -0.3)
    art = split_fruit(art, W, H, cx, 62, 54, nx, rng)
    art = add_grain(art, 3, 0.04)
    save(art, f"{OUT}/arch.webp", max_w=620, quality=82)
    preview(art, "dm-arch", CREAM)


def sprig():
    W, H = 640, 140
    rng = random.Random(8); nx = Seq(300)
    art = blank(W, H)
    for side in (-1, 1):
        path = curve([(320 + side * 30, 76), (320 + side * 140, 62), (320 + side * 240, 78), (320 + side * 300, 66)], 40)
        for i in range(4, len(path) - 1, 5):
            (ax, ay), (bx, by) = path[i - 1], path[min(len(path) - 1, i + 1)]
            a = math.atan2(by - ay, bx - ax)
            for sgn in (-1, 1):
                art = leaf_one(art, W, H, path[i][0], path[i][1], rng.uniform(32, 42), a + sgn * 0.7, nx, rng, sgn * 0.3)
        art = stem(art, W, H, [(path, 4.5, (0.05, 0.6))], nx)
        art = blossom(art, W, H, path[-1][0] - side * 4, path[-1][1], 30, 0 if side > 0 else math.pi, nx, rng)
    art = fruit(art, W, H, 320, 78, 30, nx, rng)
    art = add_grain(art, 4, 0.04)
    save(art, f"{OUT}/sprig.webp", max_w=440, quality=84)
    preview(art, "dm-sprig", CREAM)


def blossom_one():
    W, H = 220, 220
    rng = random.Random(9); nx = Seq(500)
    art = blank(W, H)
    art = leaf_one(art, W, H, 110, 160, 60, math.pi * 0.8, nx, rng, 0.3)
    art = leaf_one(art, W, H, 110, 160, 56, math.pi * 0.25, nx, rng, -0.3)
    art = blossom(art, W, H, 110, 150, 70, -math.pi / 2, nx, rng)
    art = add_grain(art, 6, 0.04)
    save(art, f"{OUT}/blossom.webp", max_w=160, quality=84)
    preview(art, "dm-blossom", CREAM)


def split():
    W, H = 320, 300
    rng = random.Random(10); nx = Seq(700)
    art = blank(W, H)
    art = leaf_one(art, W, H, 160, 70, 92, math.pi * 1.1, nx, rng, 0.3)
    art = leaf_one(art, W, H, 160, 70, 86, -0.15, nx, rng, -0.3)
    art = split_fruit(art, W, H, 160, 170, 110, nx, rng)
    art = add_grain(art, 7, 0.04)
    save(art, f"{OUT}/split.webp", max_w=260, quality=84)
    preview(art, "dm-split", CREAM)


def lattice():
    """Seamless gold ogee lattice with a small pomegranate silhouette at every node (for the deep red bands)."""
    S = 240
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                for sgn in (-1, 1):
                    path = skia.Path()
                    pts = [(ox + S / 2 + sgn * (S / 2) * math.sin(t / 40 * math.pi), oy + t / 40 * S) for t in range(41)]
                    path.moveTo(*pts[0])
                    for q in pts[1:]:
                        path.lineTo(*q)
                    cv.c.drawPath(path, p)
        f = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for (fx, fy) in ((S / 2, S / 2), (0, 0), (S, 0), (0, S), (S, S)):
            cv.c.drawCircle(fx, fy + 4, 13, f)
            path = skia.Path(); path.moveTo(fx - 7, fy - 6); path.lineTo(fx - 5, fy - 16); path.lineTo(fx, fy - 10); path.lineTo(fx + 5, fy - 16); path.lineTo(fx + 7, fy - 6); path.close()
            cv.c.drawPath(path, f)
    m = mask_from(S, S, draw)
    art = foil(m, GOLD, seed=3, emboss=0.3, sparkle=0.1)
    art[..., 3] *= 0.9
    save_full(art, f"{OUT}/lattice.webp", quality=80)


for p in PARTS:
    {"blossom": blossom_one}.get(p, globals().get(p))()
    clear()
