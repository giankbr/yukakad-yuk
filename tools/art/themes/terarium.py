"""Terarium — watercolour glass terrariums: an open globe with moss, echeveria, fern and pebbles; a brass-framed
geometric terrarium hanging on a chain; a little bell jar on a walnut base; a fern frond divider and a rosette sprig.
Glass is a faint tint, dark rim and painted reflections.
Run: python3 -I terarium.py [part ...]  parts: globe geo cloche fern sprig
Assets -> public/themes/art/terarium/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m3_lib import *

OUT = outdir("terarium")
PARTS = sys.argv[1:] or ["globe", "geo", "cloche", "fern", "sprig"]
MOSS, MOSS_L, MOSS_D = "#6f8f3e", "#a7bd64", "#3f5a2a"
FERN, FERN_D = "#5b8a4f", "#2f5a36"
SUCC, SUCC_L, SUCC_TIP = "#8fae9c", "#c4d6c4", "#d68c8c"
BRASS, BRASS_D = "#b48a44", "#7d5a24"
SOIL, SAND, CHAR = "#5a4334", "#e2cfa8", "#3b3633"
GLASS_EDGE = "#7f978c"


def erode(m, r):
    return np.clip((gaussian_filter(m, r) - 0.5) * 6 + 0.5, 0, 1) * m


def glass(art, W, H, M, nx, tint="#dbe9e2", shine=None, rim=2.4):
    """Paint the glass: faint tint, darker rim, and bright reflection strokes (list of point lists)."""
    art = G(art, M, tint, "#e9f1ea", seed=nx(), density=0.16, edge=0.4, bloom=0.2, rough=1.2, feather=0.8, gran=0.05)
    edge = np.clip(M - erode(M, rim), 0, 1)
    art = G(art, edge, GLASS_EDGE, "#5f7a70", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    if shine:
        sm = strokes(W, H, [(p, w, (0.25, 0.4)) for p, w in shine])
        art = over(art, glow(sm * M, "#ffffff", radius=1.0, strength=0.85))
    return art


def fern_frond(W, H, base, tip, bend, n=12, size=1.0, side_ang=0.95):
    """Fern frond: rachis curve + paired pinnae (petal polys). Returns (rachis items, pinna polys)."""
    (bx, by), (tx, ty) = base, tip
    mx, my = (bx + tx) / 2 + bend[0], (by + ty) / 2 + bend[1]
    pts = curve([(bx, by), (mx, my), (tx, ty)], 60)
    items = [(pts, 2.4 * size, (0.0, 0.5))]
    polys = []
    for i in range(2, n + 1):
        k = i / (n + 1)
        idx = int(k * (len(pts) - 2))
        x, y = pts[idx]
        x2, y2 = pts[idx + 1]
        a = math.atan2(y2 - y, x2 - x)
        L = (22 * size) * (1 - k * 0.75)
        for sgn in (-1, 1):
            polys.append(petal_pts(x, y, L, L * 0.32, a + sgn * side_ang, n=10))
    return items, polys


def rosette(art, W, H, cx, cy, r, nx, rng, tilt=0.55):
    """Echeveria rosette seen from slightly above: rings of pointed leaves, pink tips."""
    rings = [(1.0, 11), (0.74, 9), (0.5, 7), (0.28, 5)]
    for ri, (f, n) in enumerate(rings):
        polys = []
        off = rng.uniform(0, 1)
        for i in range(n):
            a = (i + off) / n * math.tau
            L = r * f
            ex = cx + math.cos(a) * L * 0.08
            ey = cy + math.sin(a) * L * 0.08 * tilt
            polys.append(rot_pts(petal_pts(ex, ey, L, L * 0.42, 0, n=12), ex, ey, 0) if False else
                         [(ex + (px - ex) * 1.0, ey + (py - ey) * tilt) for px, py in rot_pts(petal_pts(ex, ey, L, L * 0.42, 0, n=12), ex, ey, a)])
        m = shapes(W, H, polys)
        art = G(art, m, SUCC if ri < 2 else SUCC_L, "#9fbcb0", seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=1.4, feather=0.9)
        tips = shapes(W, H, [[(cx + (px - cx), cy + (py - cy)) for px, py in p[5:8]] for p in polys], smooth=False)
        art = G(art, m * np.clip(gaussian_filter(tips, 3) * 3, 0, 1), SUCC_TIP, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    art = G(art, circles(W, H, [(cx, cy, r * 0.12)]), "#e3eedf", seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.6)
    return art


def moss_mound(art, W, H, pts, nx, rng, clip=None):
    m = shapes(W, H, [pts])
    if clip is not None:
        m = m * clip
    art = G(art, m, MOSS, MOSS_D, seed=nx(), density=0.85, edge=0.4, bloom=0.4, rough=3, feather=1.2, gran=0.5)
    ys, xs = np.where(m > 0.5)
    if len(xs):
        sel = rng.sample(range(len(xs)), min(220, len(xs)))
        dots = circles(W, H, [(xs[i], ys[i], rng.uniform(1.4, 3.4)) for i in sel])
        art = G(art, dots * m, MOSS_L, "#c7d37a", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.6, feather=0.5)
        sel = rng.sample(range(len(xs)), min(140, len(xs)))
        dots2 = circles(W, H, [(xs[i], ys[i], rng.uniform(1.2, 2.6)) for i in sel])
        art = G(art, dots2 * m, MOSS_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    return art


def pebbles(art, W, H, items, nx, rng, clip=None):
    for cx, cy, rx, ry in items:
        m = ellipses(W, H, [(cx, cy, rx, ry, rng.uniform(-20, 20))])
        if clip is not None:
            m = m * clip
        col = rng.choice(["#cfc7bb", "#b8aea2", "#d9a37f", "#e9e1d3", "#8f8a86"])
        art = G(art, m, col, seed=nx(), density=0.85, edge=0.6, bloom=0.1, rough=1, feather=0.8)
        art = G(art, v_ramp(m, cy - ry * 0.2, cy + ry), "#6e6660", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    return art


if "globe" in PARTS:
    W, H = 600, 620
    nx = Seq(51000)
    rng = random.Random(8)
    art = blank(W, H)
    cx, cy, R = 300, 340, 250
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    globe_m = circles(W, H, [(cx, cy, R)]) * (yy > cy - R * 0.62)  # open top (cut)
    globe_m = np.clip(globe_m, 0, 1).astype(np.float32)
    inner = erode(globe_m, 4)
    # shadow on the table
    sh = ellipses(W, H, [(cx + 14, cy + R - 6, R * 0.62, 18, 0)])
    art = G(art, sh, "#9aa49c", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=3, feather=6)
    # back rim of the opening (seen through glass)
    oy = cy - R * 0.62
    ow = math.sqrt(R * R - (R * 0.62) ** 2)
    # layered substrate: pebbles, charcoal, soil (curved by the bowl)
    def layer(y0, y1):
        return inner * (yy > y0) * (yy <= y1)
    art = G(art, layer(cy + 150, cy + R), "#d8ccb7", "#c6b59a", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=2, feather=1)
    peb = [(rng.uniform(cx - 200, cx + 200), rng.uniform(cy + 160, cy + 235), rng.uniform(8, 16), rng.uniform(6, 11)) for _ in range(46)]
    art = pebbles(art, W, H, peb, nx, rng, clip=inner * (yy > cy + 150))
    art = G(art, layer(cy + 132, cy + 152), CHAR, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=2, gran=0.6)
    soil = layer(cy + 70, cy + 134)
    art = G(art, soil, SOIL, "#6e5240", seed=nx(), density=0.85, edge=0.3, bloom=0.2, rough=3, gran=0.6)
    # moss hills
    art = moss_mound(art, W, H, [(cx - 236, cy + 96), (cx - 200, cy + 40), (cx - 120, cy + 30), (cx - 40, cy + 66), (cx + 20, cy + 84), (cx + 120, cy + 52), (cx + 210, cy + 60), (cx + 240, cy + 100), (cx + 240, cy + 120), (cx - 240, cy + 120)], nx, rng, clip=inner)
    # fern clump behind on the left
    items, polys = [], []
    for base, tip, bend, sz in [((cx - 110, cy + 60), (cx - 190, cy - 120), (-30, 10), 1.3), ((cx - 100, cy + 60), (cx - 60, cy - 160), (-34, 0), 1.4), ((cx - 96, cy + 62), (cx + 10, cy - 70), (10, -20), 1.1), ((cx - 116, cy + 60), (cx - 236, cy - 20), (0, -40), 1.0)]:
        it, po = fern_frond(W, H, base, tip, bend, 14, sz)
        items += it; polys += po
    fm = np.maximum(strokes(W, H, items), shapes(W, H, polys)) * inner
    art = G(art, fm, FERN, "#77a15e", seed=nx(), density=0.85, edge=0.55, bloom=0.3, rough=1.6, feather=0.8)
    art = G(art, fm * np.clip((xx - (cx - 150)) / 120, 0, 1), FERN_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    # echeveria rosettes
    art = rosette(art, W, H, cx + 70, cy + 40, 74, nx, rng)
    art = rosette(art, W, H, cx + 170, cy + 66, 40, nx, rng)
    # a small haworthia (striped spikes)
    sp = [petal_pts(cx - 10, cy + 72, rng.uniform(36, 54), 9, -math.pi / 2 + rng.uniform(-0.8, 0.8), n=10) for _ in range(9)]
    spm = shapes(W, H, sp) * inner
    art = G(art, spm, "#4f7a5a", "#3e6449", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1, feather=0.7)
    stripes = strokes(W, H, [([(cx - 40 + k * 7, cy + 40 + (k % 3) * 6), (cx - 36 + k * 7, cy + 44 + (k % 3) * 6)], 1.6, None) for k in range(10)])
    art = G(art, stripes * spm, "#e7efe0", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    # a white stone
    art = pebbles(art, W, H, [(cx + 140, cy + 108, 22, 13), (cx - 170, cy + 104, 16, 10)], nx, rng, clip=inner)
    # the glass
    shine = [(arc_pts(cx, cy, R - 22, math.radians(150), math.radians(215), 24), 7), (arc_pts(cx, cy, R - 40, math.radians(160), math.radians(185), 12), 3),
             (arc_pts(cx, cy, R - 18, math.radians(-30), math.radians(18), 20), 4)]
    art = glass(art, W, H, globe_m, nx, shine=shine, rim=3)
    # rim of the opening: ellipse ring
    ring = np.clip(ellipses(W, H, [(cx, oy, ow, 18, 0)]) - ellipses(W, H, [(cx, oy + 1, ow - 7, 13, 0)]), 0, 1)
    art = G(art, ring, GLASS_EDGE, "#9fb5ab", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.8, feather=0.6)
    art = over(art, glow(ring * (xx < cx - 40) * (yy < oy), "#ffffff", radius=0.8, strength=0.8))
    preview(art, "ter-globe")
    save(art, f"{OUT}/globe.webp", max_w=320, quality=84)
    clear()

if "geo" in PARTS:
    # hanging geometric terrarium: hexagonal bipyramid-ish brass frame, chain from the top
    W, H = 420, 700
    nx = Seq(52000)
    rng = random.Random(3)
    art = blank(W, H)
    cx = 210
    top = (cx, 250)
    ring = [(cx - 160, 470), (cx - 80, 432), (cx + 80, 432), (cx + 160, 470), (cx + 80, 508), (cx - 80, 508)]
    bot = [(cx - 110, 640), (cx + 110, 640), (cx + 60, 664), (cx - 60, 664)]
    hull = [top, (cx + 160, 470), (cx + 110, 640), (cx + 60, 664), (cx - 60, 664), (cx - 110, 640), (cx - 160, 470)]
    M = shapes(W, H, [hull], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    inner = erode(M, 3)
    # inside: soil, moss, air-plant + small succulent; opening on the front-left facet
    base = inner * (yy > 590)
    art = G(art, base, SOIL, "#6e5240", seed=nx(), density=0.85, edge=0.3, bloom=0.1, rough=2, gran=0.5)
    art = pebbles(art, W, H, [(rng.uniform(cx - 90, cx + 90), rng.uniform(625, 655), rng.uniform(6, 11), rng.uniform(4, 7)) for _ in range(20)], nx, rng, clip=inner * (yy > 612))
    art = moss_mound(art, W, H, [(cx - 112, 600), (cx - 60, 566), (cx + 10, 580), (cx + 80, 560), (cx + 118, 600), (cx + 112, 612), (cx - 112, 612)], nx, rng, clip=inner)
    art = rosette(art, W, H, cx + 40, 566, 46, nx, rng)
    # tillandsia air plant: curling grey-green blades
    bl = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.28
        L = rng.uniform(70, 110)
        bl.append((curve([(cx - 50, 584), (cx - 50 + math.cos(a) * L * 0.5, 584 + math.sin(a) * L * 0.5), (cx - 50 + math.cos(a + 0.5 * (1 if k > 4 else -1)) * L, 584 + math.sin(a + 0.4 * (1 if k > 4 else -1)) * L)], 16), 5.5, (0.05, 0.8)))
    bm = strokes(W, H, bl) * inner
    art = G(art, bm, "#9fb6a6", "#7f9e8a", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1, feather=0.7)
    art = G(art, bm * (yy < 520), "#d98a9a", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    # glass panes
    art = glass(art, W, H, M, nx, shine=[([(cx - 120, 480), (cx - 70, 600)], 5), ([(cx - 40, 300), (cx - 110, 450)], 4), ([(cx + 120, 488), (cx + 92, 600)], 3)], rim=1.5)
    # brass frame (foil) over everything
    edges = [(top, p) for p in ring[:4]] + [(ring[i], ring[(i + 1) % 6]) for i in range(6)] + [(ring[0], bot[0]), (ring[3], bot[1]), (ring[5], bot[3]), (ring[4], bot[2]), (bot[0], bot[3]), (bot[3], bot[2]), (bot[2], bot[1]), (ring[5], bot[0]), (ring[4], bot[1])]
    fr = strokes(W, H, [([a, b], 5, None) for a, b in edges], cap=True)
    art = FO(art, fr, BRASS, seed=nx(), emboss=0.5, sparkle=0.2)
    art = G(art, fr, BRASS_D, seed=nx(), density=0.25, edge=0.2, bloom=0, rough=0.4, feather=0.4)
    knob = circles(W, H, [(cx, 246, 9)])
    art = FO(art, knob, BRASS, seed=nx(), emboss=0.6, sparkle=0.2)
    # chain
    links = []
    for i, y in enumerate(range(0, 238, 16)):
        if i % 2 == 0:
            links.append((cx, y + 8, 5, 9.5, 0))
        else:
            links.append((cx, y + 8, 2.2, 9.5, 0))
    lm = np.clip(ellipses(W, H, links) - ellipses(W, H, [(x, y, rx * 0.45, ry * 0.7, r) for x, y, rx, ry, r in links if rx > 3]), 0, 1)
    art = FO(art, lm, BRASS, seed=nx(), emboss=0.5, sparkle=0.1)
    preview(art, "ter-geo")
    save(art, f"{OUT}/geo.webp", max_w=200, quality=84)
    clear()

if "cloche" in PARTS:
    W, H = 340, 420
    nx = Seq(53000)
    rng = random.Random(5)
    art = blank(W, H)
    cx = 170
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = shapes(W, H, [[(cx - 140, 360), (cx + 140, 360), (cx + 132, 392), (cx - 132, 392)]])
    art = GP(art, base, "#7a5232", "#5e3d24", seed=nx(), rough=0.6, streak=1.2, pad=6)
    art = G(art, rects(W, H, [(cx - 140, 356, cx + 140, 366)]), "#a8784c", seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.4)
    bell = shapes(W, H, [[(cx - 112, 360), (cx - 112, 170)] + arc_pts(cx, 170, 112, math.pi, math.tau, 30)[1:-1] + [(cx + 112, 170), (cx + 112, 360)]])
    inner = erode(bell, 3)
    art = moss_mound(art, W, H, [(cx - 100, 356), (cx - 70, 318), (cx - 10, 306), (cx + 60, 316), (cx + 100, 350), (cx + 100, 358), (cx - 100, 358)], nx, rng, clip=inner)
    items, polys = [], []
    for base_, tip, bend, sz in [((cx - 6, 316), (cx - 70, 180), (-24, 0), 1.0), ((cx, 314), (cx + 50, 160), (20, 0), 1.1), ((cx + 4, 316), (cx + 92, 250), (0, -24), 0.8), ((cx - 8, 318), (cx - 96, 270), (0, -20), 0.75)]:
        it, po = fern_frond(W, H, base_, tip, bend, 13, sz)
        items += it; polys += po
    fm = np.maximum(strokes(W, H, items), shapes(W, H, polys)) * inner
    art = G(art, fm, FERN, "#7aa35f", seed=nx(), density=0.85, edge=0.55, bloom=0.3, rough=1.4, feather=0.8)
    art = glass(art, W, H, bell, nx, shine=[(curve([(cx - 84, 330), (cx - 92, 220), (cx - 60, 110)], 20), 6), (curve([(cx + 90, 300), (cx + 94, 220)], 10), 3)], rim=2)
    knob = np.maximum(circles(W, H, [(cx, 46, 15)]), rects(W, H, [(cx - 6, 52, cx + 6, 62)]))
    art = G(art, knob, "#c9d8d0", seed=nx(), density=0.4, edge=0.6, bloom=0, rough=0.6)
    art = over(art, glow(circles(W, H, [(cx - 5, 41, 4)]), "#ffffff", radius=1, strength=1))
    preview(art, "ter-cloche")
    save(art, f"{OUT}/cloche.webp", max_w=170, quality=84)
    clear()

if "fern" in PARTS:
    W, H = 600, 120
    nx = Seq(54000)
    items, polys = [], []
    it, po = fern_frond(W, H, (20, 70), (580, 52), (0, 26), 24, 1.5, 1.05)
    items += it; polys += po
    m = np.maximum(strokes(W, H, items), shapes(W, H, polys))
    art = G(blank(W, H), m, FERN, "#86ac66", seed=nx(), density=0.85, edge=0.55, bloom=0.3, rough=1.4, feather=0.8)
    art = G(art, m * np.clip((np.arange(W)[None, :] - 300) / 300, 0, 1), "#a7bd64", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    preview(art, "ter-fern")
    save(art, f"{OUT}/fern.webp", max_w=280, quality=86)
    clear()

if "sprig" in PARTS:
    W, H = 160, 140
    nx = Seq(55000)
    rng = random.Random(9)
    art = rosette(blank(W, H), W, H, 80, 74, 66, nx, rng, tilt=0.7)
    preview(art, "ter-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=72, quality=88)
    clear()
