"""Kenduri Panen — village harvest thanksgiving in transparent watercolour on warm paper: a morning panorama (low sun,
misty blue hills, palms and village roofs, golden sawah terraces with dikes, a wooden lumbung on stilts, rice sheaves
standing in the field), a tied rice sheaf (ikat padi), a tumpeng on a woven tampah with banana leaf and side dishes
(a shared meal, not an offering), a lumbung alone, a border of ripe rice stalks and a single-stalk divider.
Run: python3 -I kenduri-panen.py [part ...]   parts: panorama sheaf tumpeng lumbung stalks divider
Assets -> public/themes/art/kenduri-panen/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k5_lib import *  # noqa

OUT = outdir("kenduri-panen")
PARTS = sys.argv[1:] or ["panorama", "sheaf", "tumpeng", "lumbung", "stalks", "divider"]
GOLD, OCHRE, STRAW, STRAW_L = "#d9a441", "#b9812a", "#e8c872", "#f3dc9c"
SAGE, LEAF, LEAF_D = "#9aae66", "#6f8a3c", "#4f6a2e"
TEAK, TEAK_D, THATCH, THATCH_D = "#8a5a32", "#5a381e", "#b08a52", "#6e5234"
HILL, HILL_D, PEACH, CREAM = "#a9b3bd", "#7f8d9c", "#f0c08e", "#f7ecd2"
nx = Seq(900)


def bezier(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]


def grains(path, size, rng, every=1):
    """Grain ellipses alternating along a drooping panicle path."""
    items = []
    for i in range(1, len(path), every):
        (x0, y0), (x1, y1) = path[i - 1], path[i]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        t = i / len(path)
        s = size * (0.6 + 0.5 * math.sin(math.pi * min(1, t * 1.2)))
        for side in (-1, 1):
            off = side * s * 0.9
            nxv, nyv = -(y1 - y0), (x1 - x0)
            L = math.hypot(nxv, nyv) + 1e-6
            items.append((x1 + nxv / L * off, y1 + nyv / L * off, s * 1.25, s * 0.55, ang + side * 28 + rng.uniform(-10, 10)))
    return items


def stalk(rng, base, height, lean, droop, size=3.0, n=26):
    """One rice stalk: stem path and panicle path."""
    bx, by = base
    top = (bx + lean * height * 0.35, by - height)
    stem = bezier(base, (bx + lean * height * 0.05, by - height * 0.6), top, 18)
    tip = (top[0] + droop * height * 0.38, top[1] + height * 0.22)
    pan = bezier(top, (top[0] + droop * height * 0.28, top[1] - height * 0.06), tip, n)
    return stem, pan


def paint_stalks(art, W, H, stalks, rng, gold=(GOLD, STRAW), stem_col=(SAGE, STRAW), size=3.0, sw=1.6):
    stems, ells, pans = [], [], []
    for stem, pan in stalks:
        stems.append((stem, sw, (0.0, 0.3)))
        pans.append((pan, sw * 0.7, (0.0, 0.5)))
        ells += grains(pan, size, rng)
    art = G(art, strokes(W, H, stems), stem_col[0], stem_col[1], seed=nx(), density=0.75, edge=0.3, bloom=0.1, rough=0.8, feather=0.4)
    art = G(art, strokes(W, H, pans), OCHRE, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.3)
    art = G(art, ellipses(W, H, ells), gold[0], gold[1], seed=nx(), density=0.88, edge=0.55, bloom=0.2, gran=0.4, rough=0.8, feather=0.4)
    return art


def blades(W, H, rng, base_pts, height, n, width=4.0):
    items = []
    for _ in range(n):
        bx, by = base_pts[rng.integers(len(base_pts))]
        h = height * rng.uniform(0.6, 1.1)
        lean = rng.uniform(-0.7, 0.7)
        pts = bezier((bx, by), (bx + lean * h * 0.2, by - h * 0.7), (bx + lean * h * 0.6, by - h * (0.75 + rng.uniform(-0.1, 0.15))), 14)
        items.append((pts, width * rng.uniform(0.7, 1.2), (0.0, 0.85)))
    return strokes(W, H, items)


def lumbung_paint(art, W, H, cx, by, s):
    """Lumbung padi: four teak stilts, anti-rat discs, a small woven body, a tall bell-shaped thatched roof."""
    posts = []
    for dx in (-30, -10, 10, 30):
        posts.append(([(cx + dx * s, by), (cx + dx * s * 0.96, by - 70 * s)], 5.5 * s, None))
    art = G(art, strokes(W, H, posts), TEAK, TEAK_D, seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=0.8, feather=0.5)
    discs = ellipses(W, H, [(cx, by - 72 * s, 42 * s, 6 * s, 0)])
    art = G(art, discs, TEAK_D, TEAK, seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.7, feather=0.5)
    body = polys(W, H, [[(cx - 36 * s, by - 76 * s), (cx + 36 * s, by - 76 * s), (cx + 38 * s, by - 128 * s), (cx - 38 * s, by - 128 * s)]], smooth=False)
    art = G(art, body, "#c9a46a", "#b58f55", seed=nx(), density=0.85, edge=0.5, bloom=0.2, gran=0.4, rough=1, feather=0.6)
    weave = hatch(W, H, 0.75, 4.0 * s, 0.28, nx()) * body
    art = G(art, weave, TEAK, seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.6, feather=0.3)
    art = G(art, rects(W, H, [(cx - 7 * s, by - 120 * s, 14 * s, 38 * s)], 2), TEAK_D, seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.6, feather=0.4)
    roof = [(cx - 66 * s, by - 116 * s), (cx - 54 * s, by - 150 * s), (cx - 36 * s, by - 200 * s), (cx - 16 * s, by - 236 * s), (cx, by - 246 * s),
            (cx + 16 * s, by - 236 * s), (cx + 36 * s, by - 200 * s), (cx + 54 * s, by - 150 * s), (cx + 66 * s, by - 116 * s), (cx, by - 124 * s)]
    rm = polys(W, H, [roof])
    art = G(art, rm, THATCH, "#c39b5d", seed=nx(), density=0.9, edge=0.6, bloom=0.3, gran=0.5, rough=1.6, feather=0.8)
    # thatch strands + shadow side
    strands = []
    rng = np.random.default_rng(int(cx))
    for _ in range(int(90 * s)):
        x = rng.uniform(cx - 62 * s, cx + 62 * s)
        y0 = rng.uniform(by - 240 * s, by - 140 * s)
        strands.append(([(x, y0), (x + (x - cx) * 0.25, y0 + rng.uniform(30, 70) * s)], 1.2 * s, (0.1, 0.4)))
    art = G(art, strokes(W, H, strands) * rm, THATCH_D, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.6, feather=0.3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, rm * np.clip((xx - cx) / (60 * s), 0, 1), "#6b4e30", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=1.2, feather=1.5)
    art = G(art, strokes(W, H, [([(cx - 66 * s, by - 116 * s), (cx, by - 126 * s), (cx + 66 * s, by - 116 * s)], 3 * s, None)]), THATCH_D, seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.6, feather=0.4)
    art = G(art, strokes(W, H, [([(cx, by - 246 * s), (cx, by - 262 * s)], 3 * s, None)]), TEAK_D, seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.4, feather=0.3)
    return art


def sheaf_stalks(cx, waist, s, rng, n=34):
    """Stalks of a tied sheaf: stems fan from the waist; upper heads droop both ways."""
    out = []
    for i in range(n):
        t = (i / (n - 1)) * 2 - 1
        base = (cx + t * 14 * s, waist + 120 * s)
        lean = t * 0.8 + rng.uniform(-0.15, 0.15)
        h = (200 + rng.uniform(-20, 30)) * s
        droop = (1 if t > 0 else -1) * rng.uniform(0.5, 1.0)
        stem, pan = stalk(rng, base, h, lean, droop, n=22)
        # pinch the stems through the tie
        stem = [(x + (cx - x) * max(0, 1 - abs(y - waist) / (60 * s)) * 0.7, y) for x, y in stem]
        out.append((stem, pan))
    return out


def sheaf_paint(art, W, H, cx, waist, s, rng):
    st = sheaf_stalks(cx, waist, s, rng)
    art = paint_stalks(art, W, H, st, rng, size=3.2 * s, sw=1.7 * s)
    # cut ends at the bottom
    ends = ellipses(W, H, [(cx + t * 16 * s, waist + 120 * s, 2.2 * s, 1.2 * s, 0) for t in np.linspace(-1, 1, 14)])
    art = G(art, ends, OCHRE, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.4, feather=0.3)
    tie = strokes(W, H, [([(cx - 13 * s, waist - 2 * s), (cx, waist + 3 * s), (cx + 13 * s, waist - 2 * s)], 5 * s, None),
                         ([(cx - 12 * s, waist + 8 * s), (cx, waist + 12 * s), (cx + 12 * s, waist + 8 * s)], 4 * s, None)])
    art = G(art, tie, "#8a6a3a", TEAK, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.3)
    return art


def panorama():
    W, H = 780, 980
    rng = np.random.default_rng(5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    bg = np.asarray(paper(W, H, "#f8efd9", 4), np.float32) / 255
    art = np.concatenate([bg, np.ones((H, W, 1), np.float32)], -1)
    # sky: warm wash, peach near the horizon
    sky = rects(W, H, [(-20, -20, W + 40, 640)])
    art = G(art, sky * np.clip((yy - 140) / 480, 0, 1), PEACH, "#f3d3a4", seed=nx(), density=0.5, edge=0.0, bloom=0.5, gran=0.25, rough=4, feather=8, pad=0)
    art = G(art, sky * np.clip(1 - yy / 360, 0, 1), "#cfdbe0", "#e3e6dc", seed=nx(), density=0.35, edge=0.0, bloom=0.5, gran=0.2, rough=4, feather=8, pad=0)
    # sun: a soft disc with a halo, lifted out of the wash
    sun = disc(W, H, 540, 452, 70)
    art = over(art, glow(sun, "#fff3d2", 70, 0.7))
    art = G(art, sun, "#f7cf72", "#f4bd5c", seed=nx(), density=0.75, edge=0.5, bloom=0.3, gran=0.2, rough=2.5, feather=1.6)
    # hills: far (blue-grey) and near (grey-green), with mist between
    def ridge(y, amp, seed, wl):
        n = fbm(W, 1, seed, 140 * wl, 3)[0]
        return y - amp * n
    far = ridge(560, 120, nx(), 1.4)
    mfar = (yy > far[None, :]).astype(np.float32) * (yy < 700)
    art = G(art, mfar, HILL, "#b8c0c4", seed=nx(), density=0.6, edge=0.45, bloom=0.4, gran=0.3, rough=3, feather=1.5, pad=0)
    mist = np.exp(-((yy - 585) / 30) ** 2) * (0.6 + 0.4 * fbm(W, H, nx(), 120, 2))
    art = over(art, col_arr(mist, "#fbf1dc", mist * 0.75))
    near = ridge(640, 70, nx(), 0.9)
    mnear = (yy > near[None, :]).astype(np.float32) * (yy < 720)
    art = G(art, mnear, "#93a487", "#a7b38f", seed=nx(), density=0.6, edge=0.45, bloom=0.4, gran=0.3, rough=3, feather=1.5, pad=0)
    # palms + village roofs on the tree line
    palms = []
    tree_line = 650
    for x in (60, 92, 170, 610, 650, 720, 748):
        h = rng.uniform(70, 120)
        top = (x + rng.uniform(-10, 10), tree_line - h)
        palms.append(([(x, tree_line + 10), (x + (top[0] - x) * 0.5, tree_line - h * 0.5), top], 3.0, (0.0, 0.2)))
        for a in np.linspace(-2.7, -0.4, 6):
            L = rng.uniform(26, 40)
            end = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.4 + 14)
            palms.append(([top, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5), end], 3.2, (0.0, 0.7)))
    art = G(art, strokes(W, H, palms), "#6d7f5a", "#7d8c66", seed=nx(), density=0.75, edge=0.4, bloom=0.2, rough=1.2, feather=0.6)
    bush = ellipses(W, H, [(x, tree_line + 12, rng.uniform(30, 60), rng.uniform(10, 18), 0) for x in np.linspace(-20, W + 20, 18)])
    art = G(art, bush, "#7e8f62", "#93a173", seed=nx(), density=0.7, edge=0.4, bloom=0.3, gran=0.3, rough=2, feather=1)
    walls, roofs = [], []
    for x, w in ((236, 40), (300, 34), (380, 46)):
        walls.append((x - w / 2 + 4, tree_line - 4, w - 8, 18))
        roofs.append([(x - w / 2 - 4, tree_line - 2), (x - w / 2 + 8, tree_line - 18), (x + w / 2 - 8, tree_line - 18), (x + w / 2 + 4, tree_line - 2)])
    art = GP(art, rects(W, H, walls), "#efe2c4", "#e0cfa8", seed=nx(), rough=0.8, streak=0.3)
    art = G(art, rects(W, H, [(x - 3, tree_line + 2, 6, 10) for x, w in ((236, 40), (300, 34), (380, 46))]), TEAK_D, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.4, feather=0.3)
    art = G(art, polys(W, H, roofs, smooth=False), "#a8674a", "#b97a55", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1, feather=0.6)
    # a mosque-like dome far off is avoided; a slim village tree instead
    # golden sawah: undulating bands with dikes, texture strokes growing toward the viewer
    y = 670
    bands = []
    k = 0
    while y < H + 40:
        hgt = 14 + (y - 660) * 0.16
        top = [(x, y + 6 * math.sin(x / 120 + k) ) for x in np.linspace(-10, W + 10, 30)]
        bot = [(x, y + hgt + 6 * math.sin(x / 120 + k + 0.6)) for x in np.linspace(W + 10, -10, 30)]
        bands.append((top + bot, k, y, hgt))
        y += hgt - 1
        k += 1
    for pts, k, y0, hgt in bands:
        m = polys(W, H, [pts], smooth=False)
        c1, c2 = [(GOLD, STRAW), (STRAW, "#e2b45a"), ("#cf9a3c", GOLD), ("#c3b35c", STRAW)][k % 4]
        art = G(art, m, c1, c2, seed=nx(), density=0.7, edge=0.45, bloom=0.3, gran=0.4, rough=2, feather=1, pad=4)
        # rice texture: short upright strokes, density by depth
        n = int(W / max(3, 16 - hgt * 0.18))
        tex = []
        for _ in range(n):
            x = rng.uniform(0, W)
            yb = y0 + hgt * rng.uniform(0.5, 1.0)
            L = hgt * rng.uniform(0.35, 0.7)
            tex.append(([(x, yb), (x + rng.uniform(-2, 2), yb - L)], max(0.8, hgt * 0.05), (0.0, 0.6)))
        art = G(art, strokes(W, H, tex) * m, OCHRE, "#a87a2c", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.5, feather=0.3, pad=2)
    dikes = []
    for pts, k, y0, hgt in bands:
        dikes.append(([(p[0], p[1] + 1) for p in pts[:30]], 1.4 + hgt * 0.03, None))
    art = G(art, strokes(W, H, dikes), "#8a9a55", "#a1ab68", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=0.6, feather=0.4)
    # a winding pematang path toward the lumbung
    path = curve([(150, H + 10), (300, 900), (250, 840), (420, 800), (560, 772)], 40)
    art = G(art, strokes(W, H, [(path, 18, (0.0, 0.9))]), "#d8c79b", "#c9b48a", seed=nx(), density=0.75, edge=0.4, bloom=0.2, gran=0.4, rough=1.5, feather=0.8)
    # lumbung on the right
    art = lumbung_paint(art, W, H, 600, 772, 0.85)
    # rice sheaves standing in the field (foreground left) + ripe stalks along the bottom edge
    art = sheaf_paint(art, W, H, 104, 818, 0.62, rng)
    art = sheaf_paint(art, W, H, 186, 842, 0.5, rng)
    st = []
    for x in np.linspace(-10, W + 10, 70):
        st.append(stalk(rng, (x + rng.uniform(-6, 6), H + 6), rng.uniform(70, 120), rng.uniform(-0.3, 0.3), rng.choice([-1, 1]) * rng.uniform(0.6, 1), n=18))
    art = paint_stalks(art, W, H, st, rng, size=2.8, sw=1.5)
    art = add_grain(art, nx(), 0.03)
    save_full(art, f"{OUT}/panorama.webp", quality=76, rgb=True)
    prev(art, "kp-panorama")


def sheaf():
    W, H = 300, 420
    rng = np.random.default_rng(11)
    art = blank(W, H)
    art = sheaf_paint(art, W, H, 150, 250, 1.0, rng)
    save(art, f"{OUT}/sheaf.webp", max_w=260)
    prev(art, "kp-sheaf")


def tumpeng():
    W, H = 460, 360
    rng = np.random.default_rng(13)
    art = blank(W, H)
    cx, cy = 230, 270
    # tampah: woven bamboo tray
    tray = ellipses(W, H, [(cx, cy, 200, 62, 0)])
    art = G(art, tray, "#d3b27a", "#c49d5d", seed=nx(), density=0.85, edge=0.55, bloom=0.2, gran=0.5, rough=1.2, feather=0.8)
    weave = np.maximum(hatch(W, H, 0.78, 6.0, 0.25, nx()), hatch(W, H, -0.78, 6.0, 0.25, nx()) * 0.7) * tray
    art = G(art, weave, "#a07a42", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=0.5, feather=0.3)
    rim = np.clip(gaussian_filter(tray, 2) - gaussian_filter(ellipses(W, H, [(cx, cy - 2, 190, 56, 0)]), 2), 0, 1) * 2
    art = G(art, np.clip(rim, 0, 1), "#8a6534", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.6, feather=0.4)
    # banana leaf lining, scalloped
    leaf_pts = []
    for t in np.linspace(0, 2 * math.pi, 48, endpoint=False):
        r = 1 + 0.06 * math.sin(t * 8)
        leaf_pts.append((cx + math.cos(t) * 176 * r, cy - 6 + math.sin(t) * 50 * r))
    lm = polys(W, H, [leaf_pts])
    art = G(art, lm, "#7f9e45", "#5f8236", seed=nx(), density=0.85, edge=0.6, bloom=0.3, gran=0.3, rough=1.6, feather=0.8)
    veins = [[(cx, cy - 6), (cx + math.cos(t) * 170, cy - 6 + math.sin(t) * 48)] for t in np.linspace(0, 2 * math.pi, 22, endpoint=False)]
    art = G(art, lines_mask(W, H, veins, 1.0) * lm, "#4f6a2e", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=0.4, feather=0.3)
    # side dishes around the cone: urap greens, egg halves, tempe, chili, fried chicken pieces
    dishes = []
    for i, a in enumerate(np.linspace(0, 2 * math.pi, 12, endpoint=False)):
        x, y = cx + math.cos(a) * 128, cy - 8 + math.sin(a) * 34
        dishes.append((i % 4, x, y))
    for kind, x, y in sorted(dishes, key=lambda d: d[2]):
        if kind == 0:   # urap
            m = ellipses(W, H, [(x + rng.uniform(-6, 6), y + rng.uniform(-3, 3), 9, 5, rng.uniform(0, 180)) for _ in range(7)])
            art = G(art, m, "#6f9a3a", "#a9b85a", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=0.8, feather=0.4, pad=8)
            art = G(art, circles(W, H, [(x + rng.uniform(-8, 8), y + rng.uniform(-4, 4), 1.6) for _ in range(10)]), "#f4ecd8", seed=nx(), density=0.9, edge=0.1, bloom=0, rough=0.3, feather=0.2, pad=6)
        elif kind == 1:  # egg half
            art = GP(art, ellipses(W, H, [(x, y, 15, 9, 0)]), "#fbf6ea", "#efe6d0", seed=nx(), rough=0.6, streak=0.2)
            art = G(art, ellipses(W, H, [(x, y - 1, 7, 4.5, 0)]), "#f2b632", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.4, feather=0.3, pad=6)
        elif kind == 2:  # tempe
            art = G(art, rects(W, H, [(x - 13, y - 6, 26, 12, rng.uniform(-15, 15))], 3), "#b9853e", "#9a6a2c", seed=nx(), density=0.9, edge=0.5, bloom=0.1, gran=0.6, rough=0.8, feather=0.4, pad=8)
        else:            # chicken piece
            art = G(art, polys(W, H, [ellipse_pts(x, y, 16, 9, n=10, rot=rng.uniform(-0.4, 0.4))]), "#b7652d", "#8e4a20", seed=nx(), density=0.9, edge=0.5, bloom=0.2, gran=0.4, rough=1.2, feather=0.5, pad=8)
    # the cone of yellow rice
    cone = [(cx - 104, cy - 2), (cx - 80, cy - 52), (cx - 44, cy - 120), (cx - 12, cy - 170), (cx, cy - 180), (cx + 12, cy - 170),
            (cx + 44, cy - 120), (cx + 80, cy - 52), (cx + 104, cy - 2), (cx, cy + 16)]
    cm = polys(W, H, [cone])
    art = GP(art, cm, "#f4d067", "#edc24f", seed=nx(), rough=1.2, streak=0.4)
    art = G(art, cm, "#f2c94c", "#e9b43a", seed=nx(), density=0.88, edge=0.55, bloom=0.4, gran=0.6, rough=1.6, feather=0.8)
    art = G(art, cm * np.clip((np.mgrid[0:H, 0:W][1] - cx) / 80, 0, 1), "#d39a2a", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=1, feather=1.5)
    rice = circles(W, H, [(cx + rng.uniform(-100, 100), cy - rng.uniform(0, 180), 1.4) for _ in range(650)]) * cm
    art = G(art, rice, "#fff1c2", seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.3, feather=0.2)
    # garnish at the tip: a small red chili flower, and a cucumber band at the base
    tipm = polys(W, H, [petal_pts(cx, cy - 180, 18, 6, -math.pi / 2 + d, n=10) for d in (-0.6, 0, 0.6)])
    art = G(art, tipm, "#d0412c", "#b6301f", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.6, feather=0.4, pad=8)
    cuc = ellipses(W, H, [(cx + math.cos(a) * 100, cy + math.sin(a) * 16, 9, 5, 0) for a in np.linspace(0.2, math.pi - 0.2, 7)])
    art = G(art, cuc, "#9cc169", "#cfe0a0", seed=nx(), density=0.9, edge=0.5, bloom=0, rough=0.6, feather=0.4)
    save(art, f"{OUT}/tumpeng.webp", max_w=420)
    prev(art, "kp-tumpeng")


def lumbung():
    W, H = 300, 340
    rng = np.random.default_rng(17)
    art = blank(W, H)
    ground = ellipses(W, H, [(150, 318, 120, 14, 0)])
    art = G(art, ground, "#c9b48a", "#d7c49a", seed=nx(), density=0.55, edge=0.3, bloom=0.4, rough=2, feather=1.5)
    art = lumbung_paint(art, W, H, 150, 318, 1.1)
    base = [(x, 318) for x in np.linspace(40, 260, 20)]
    art = G(art, blades(W, H, rng, base, 46, 40, 3.2), SAGE, LEAF, seed=nx(), density=0.75, edge=0.3, bloom=0.1, rough=0.8, feather=0.4)
    save(art, f"{OUT}/lumbung.webp", max_w=280)
    prev(art, "kp-lumbung")


def stalks():
    W, H = 780, 200
    rng = np.random.default_rng(19)
    art = blank(W, H)
    base = [(x, H + 4) for x in np.linspace(-10, W + 10, 60)]
    art = G(art, blades(W, H, rng, base, 120, 70, 3.6), SAGE, "#b2b874", seed=nx(), density=0.65, edge=0.3, bloom=0.1, rough=0.8, feather=0.4)
    st = [stalk(rng, (x + rng.uniform(-5, 5), H + 4), rng.uniform(110, 170), rng.uniform(-0.3, 0.3), rng.choice([-1, 1]) * rng.uniform(0.6, 1.0), n=20)
          for x in np.linspace(0, W, 46)]
    art = paint_stalks(art, W, H, st, rng, size=3.0, sw=1.6)
    save(art, f"{OUT}/stalks.webp", max_w=780, quality=80)
    prev(art, "kp-stalks")


def divider():
    W, H = 380, 60
    rng = np.random.default_rng(23)
    art = blank(W, H)
    stem = bezier((20, 40), (190, 28), (300, 34), 30)
    pan = bezier((300, 34), (340, 30), (362, 46), 20)
    art = G(art, strokes(W, H, [(stem, 1.8, (0.1, 0.0)), (pan, 1.2, (0.0, 0.4))]), SAGE, STRAW, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.5, feather=0.3, pad=6)
    leafs = strokes(W, H, [(bezier((120, 34), (170, 14), (230, 12), 14), 4.0, (0.0, 0.9)), (bezier((80, 38), (60, 50), (30, 54), 12), 3.4, (0.0, 0.9))])
    art = G(art, leafs, LEAF, SAGE, seed=nx(), density=0.75, edge=0.4, bloom=0.1, rough=0.6, feather=0.4, pad=6)
    art = G(art, ellipses(W, H, grains(pan, 3.2, rng) + grains(bezier((300, 34), (318, 20), (330, 22), 8), 2.6, rng)), GOLD, STRAW, seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=0.5, feather=0.3, pad=6)
    save(art, f"{OUT}/divider.webp", max_w=380)
    prev(art, "kp-divider")


for part in PARTS:
    globals()[part]()
    clear()
