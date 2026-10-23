"""Renda Putih — layered white lace over ivory satin, painted at thread level: hexagonal bobbinet ground, cloth-stitch
flowers and leaves, raised cordonnet outlines, picot edges and the soft shadow each layer casts on the satin.
Parts: veil (cover lace panel with an oval satin window), trim (repeat-x scalloped border), doily (round guipure
medallion), sprig (small spray), divider (lace insertion), satin (seamless ivory satin tile).
Run: python3 -I renda-putih.py [part ...]   Assets -> public/themes/art/renda-putih/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k4_lib import *

OUT = outdir("renda-putih")
PARTS = sys.argv[1:] or ["satin", "veil", "trim", "doily", "sprig", "divider"]
SATIN = "#efe7da"


def ell_ring(W, H, cx, cy, rx, ry, w):
    o = ellipses(W, H, [(cx, cy, rx + w / 2, ry + w / 2, 0)])
    i = ellipses(W, H, [(cx, cy, rx - w / 2, ry - w / 2, 0)])
    return np.clip(o - i, 0, 1)


def spray(W, H, x, y, r, ang, rng, cloth, cord, flip=1):
    """A flower with two leaves and a curling cord stem."""
    flower_lace(W, H, x, y, r, rng.choice([5, 6, 7]), rng, rot=rng.uniform(0, 1), cloth=cloth, cord=cord)
    for s_ in (-1, 1):
        a = ang + s_ * rng.uniform(0.7, 1.1)
        leaf_lace(W, H, x + math.cos(a) * r * 1.05, y + math.sin(a) * r * 1.05, r * rng.uniform(0.9, 1.25), a + s_ * 0.25, rng, cloth, cord)
    st = curve([(x + math.cos(ang + math.pi) * r * 0.9, y + math.sin(ang + math.pi) * r * 0.9),
                (x + math.cos(ang + math.pi + 0.5 * flip) * r * 1.8, y + math.sin(ang + math.pi + 0.5 * flip) * r * 1.8),
                (x + math.cos(ang + math.pi + 0.1 * flip) * r * 2.4, y + math.sin(ang + math.pi + 0.1 * flip) * r * 2.4)], 30)
    np.maximum(cord, strokes(W, H, [(st, 3.0, (0.05, 0.3))]), out=cord)
    # curl at the end of the stem
    ex, ey = st[-1]
    np.maximum(cord, strokes(W, H, [(spiral_pts(ex, ey, r * 0.35, r * 0.05, ang, 1.1, 30, flip), 2.4, (0.0, 0.5))]), out=cord)


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * turns * math.tau * i / (n - 1)) * (r0 + (r1 - r0) * i / (n - 1)),
             cy + math.sin(a0 + d * turns * math.tau * i / (n - 1)) * (r0 + (r1 - r0) * i / (n - 1))) for i in range(n)]


if "satin" in PARTS:
    W = H = 512
    fold = wrap_noise(W, H, 3, (90, 40))
    fold2 = wrap_noise(W, H, 4, (40, 20))
    weave = wrap_noise(W, H, 5, (0.4, 2.5))
    t = np.clip(0.55 + (fold - 0.5) * 0.6 + (fold2 - 0.5) * 0.25, 0, 1)
    rgb = ramp(t, [(0, "#e3d8c6"), (0.45, "#eee6d8"), (0.75, "#f6f0e6"), (1, "#fffcf6")])
    rgb = rgb * (1 + (weave[..., None] - 0.5) * 0.035)
    sat = rgba(rgb, np.ones((H, W), np.float32))
    show(np.tile(sat, (1, 2, 1)), "rp-satin")
    save_rgb(sat, f"{OUT}/satin.webp", quality=72)

def tulle_tile(spacing=9.0, periods=4, thread=0.17, seed=1):
    """Seamless hexagonal bobbinet tile: returns RGBA (white threads), tile size (w, h_exact)."""
    Px = 2 * spacing * periods / 2 * 1.0
    Px = 2 * spacing * (periods // 2)
    Py = 2 * spacing / math.sqrt(3) * periods
    w, h = int(round(Px)), int(round(Py))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xx = xx * Px / w; yy = yy * Py / h
    a = np.zeros((h, w), np.float32)
    for ang in (0.0, math.pi / 3, 2 * math.pi / 3):
        u = (xx * math.cos(ang) + yy * math.sin(ang)) / spacing
        f = np.abs((u % 1.0) - 0.5) * 2
        a = np.maximum(a, np.clip((thread - (1 - f)) / 0.12 + 0.5, 0, 1))
    # knots where threads twist
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb("#fffdf8"), np.float32)
    return rgba(rgb, a * 0.55), (Px, Py)


def veil_sheet(W, H, cx, cy, rx, ry, edge_y, period, depth, rng):
    sh = LaceSheet(W, H)
    # garland of sprays around the window
    n = 12
    for k in range(n):
        t = -math.pi / 2 + (k + 0.5) / n * math.tau
        x, y = cx + math.cos(t) * (rx + 66), cy + math.sin(t) * (ry + 60)
        if not (-30 < x < W + 30 and -30 < y < edge_y - 40):
            continue
        r = 30 if k % 2 else 23
        sh.flower(x, y, r, rng.choice([5, 6]), rng, rot=rng.uniform(0, 1), open_every=3)
        for s_ in (-1, 1):
            la = t + math.pi / 2 * s_ + rng.uniform(-0.2, 0.2)
            sh.leaf(x + math.cos(la) * r * 1.0, y + math.sin(la) * r * 1.0, r * 1.15, la, rng)
        t2 = t + math.pi / n
        x2, y2 = cx + math.cos(t2) * (rx + 58), cy + math.sin(t2) * (ry + 52)
        sh.stem([(x + math.cos(t + math.pi / 2) * r * 1.6, y + math.sin(t + math.pi / 2) * r * 1.6), (x2 + math.cos(t2) * 14, y2 + math.sin(t2) * 14), (x2, y2)], 2.4)
        sh.dots.append((x2, y2, 4.0))
    for (x, y, r, a0) in ((64, 74, 50, 0.8), (W - 64, 74, 50, math.pi - 0.8), (56, edge_y - 120, 38, -0.7), (W - 56, edge_y - 120, 38, math.pi + 0.7)):
        sh.flower(x, y, r, 7, rng, rot=rng.uniform(0, 1), open_every=2)
        for d in (-1.0, 1.0):
            la = a0 + d * 0.9
            sh.leaf(x + math.cos(la) * r, y + math.sin(la) * r, r * 1.2, la, rng)
        sh.flower(x + math.cos(a0) * r * 2.3, y + math.sin(a0) * r * 2.3, r * 0.42, 5, rng, rot=0.3)
    for i in range(-1, W // period + 2):
        xm = i * period + period / 2
        if -20 < xm < W + 20:
            sh.flower(xm, edge_y + depth * 0.42, 17, 5, rng, rot=rng.uniform(0, 1))
            for s_ in (-1, 1):
                sh.leaf(xm + s_ * 20, edge_y + depth * 0.28, 22, (0 if s_ > 0 else math.pi) - 0.5 * s_, rng)
    return sh


if "veil" in PARTS:
    W, H = 780, 1060
    rng = random.Random(11)
    cx, cy, rx, ry = 390, 470, 262, 330
    EY, PER, DEP = 940, 130, 64
    region, cord_e, pic_e = scallop_edge(W, H, EY, PER, DEP, x0=-1, x1=W + 1, picot_r=2.6)
    window = ellipses(W, H, [(cx, cy, rx, ry, 0)])
    net = np.clip(region - window, 0, 1)
    rim = np.maximum.reduce([cord_e, ell_ring(W, H, cx, cy, rx, ry, 5), ell_ring(W, H, cx, cy, rx + 17, ry + 17, 3)])
    sc = [(cx + math.cos(k / 60 * math.tau) * (rx - 4), cy + math.sin(k / 60 * math.tau) * (ry - 4), 3.0) for k in range(60)]
    pic = np.maximum(pic_e, np.clip(circles(W, H, sc) - circles(W, H, [(a, b, 1.3) for a, b, _ in sc]), 0, 1))
    beads = circles(W, H, [(cx + math.cos(k / 80 * math.tau) * (rx + 9), cy + math.sin(k / 80 * math.tau) * (ry + 9), 2.5) for k in range(80)])
    dots = [(rng.uniform(0, W), rng.uniform(0, EY), rng.uniform(1.8, 2.6)) for _ in range(260)]
    sheet = veil_sheet(W, H, cx, cy, rx, ry, EY, PER, DEP, rng)
    motif_area = gaussian_filter(shapes(W, H, sheet.cloth + sheet.half), 5) > 0.02
    dm = circles(W, H, dots) * net * (1 - motif_area)
    art = sheet.render(picot=pic, extra_cord=rim, extra_cloth=np.maximum(beads, dm), seed=13)
    art[..., 3] *= np.clip(gaussian_filter(region, 0.7) + gaussian_filter(window, 3) * 0, 0, 1) * (1 - window * 0) 
    # preview with the mesh composited (as on the page)
    tile, (Px, Py) = tulle_tile(9.0, 4)
    th, tw = tile.shape[:2]
    reps = np.tile(tile, (H // th + 1, W // tw + 1, 1))[:H, :W].copy()
    reps[..., 3] *= net
    satin = np.asarray(Image.open(f"{OUT}/satin.webp").convert("RGB"), np.float32) / 255
    bg = rgba(np.tile(satin, (3, 2, 1))[:H, :W], np.ones((H, W), np.float32))
    comp = over(bg, flat(gaussian_filter(np.roll(np.roll(np.maximum(net * 0.5, art[..., 3]), 3, 0), 2, 1), 2), "#6b5a48", 0.35))
    comp = over(over(comp, reps), art)
    show(comp, "rp-veil-comp", bg=SATIN)
    save_full(art, f"{OUT}/veil.webp", size=(624, 848), quality=80)
    mask = flat(np.clip(gaussian_filter(net, 0.8), 0, 1), "#ffffff")
    save_full(mask, f"{OUT}/veilmask.webp", size=(390, 530), quality=70)
    save_full(tile, f"{OUT}/tulle.webp", quality=90)
    print("tulle period", Px, Py)
    clear()

if "trim" in PARTS:
    # repeat-x scalloped border: mesh band + flowers in each scallop (tile 240 x 100 -> CSS 120 x 50)
    TW, H = 240, 100
    W = TW * 3
    rng = random.Random(23)
    region, cord_e, pic_e = scallop_edge(W, H, 62, 120, 30, x0=0, x1=W, picot_r=2.4)
    sh = LaceSheet(W, H)
    for rep in range(3):
        o = rep * TW
        rr = random.Random(5)
        for k in range(2):
            xm = o + k * 120 + 60
            sh.flower(xm, 52, 20, 6, rr, rot=0.2, open_every=3)
            for s_ in (-1, 1):
                sh.leaf(xm + s_ * 24, 40, 26, (0 if s_ > 0 else math.pi) - 0.45 * s_, rr)
            sh.dots += [(xm + 60, 22, 3.2), (xm + 48, 30, 2.2), (xm + 72, 30, 2.2)]
    top = strokes(W, H, [([(0, 8), (W, 8)], 3.2, None), ([(0, 15), (W, 15)], 1.6, None)])
    tile, _ = tulle_tile(9.0, 4)
    th, tw = tile.shape[:2]
    mesh = np.tile(tile[..., 3], (H // th + 1, W // tw + 1))[:H, :W]
    net = np.clip(region * (1 - (np.mgrid[0:H, 0:W][0] < 8)), 0, 1)
    art = sh.render(net=net, mesh=mesh, picot=pic_e, extra_cord=np.maximum(cord_e, top), seed=29, shadow=0.3)
    art = art[:, TW:2 * TW]
    show(np.concatenate([art] * 3, 1), "rp-trim", bg=SATIN)
    save_full(art, f"{OUT}/trim.webp", quality=84)

if "doily" in PARTS:
    W = H = 440
    cx = cy = W / 2
    rng = random.Random(31)
    sh = LaceSheet(W, H)
    sh.flower(cx, cy, 44, 8, rng, rot=0.0, open_every=2)
    for k in range(8):   # ring of leaves
        a = k * math.tau / 8 + math.pi / 8
        sh.leaf(cx + math.cos(a) * 58, cy + math.sin(a) * 58, 52, a, rng)
    loops, bars = [], []
    for k in range(16):  # ring of open loops joined by bars (guipure: no net)
        a = k * math.tau / 16
        lx, ly = cx + math.cos(a) * 140, cy + math.sin(a) * 140
        loops.append(ellipse_pts(lx, ly, 17, 17, 16))
        sh.dots.append((lx, ly, 5.0))
        bars.append(([(cx + math.cos(a) * 112, cy + math.sin(a) * 112), (cx + math.cos(a) * 123, cy + math.sin(a) * 123)], 2.6))
        a2 = a + math.pi / 16
        bars.append(([(cx + math.cos(a2) * 100, cy + math.sin(a2) * 100), (cx + math.cos(a2) * 176, cy + math.sin(a2) * 176)], 2.2))
    for pts in loops:
        sh.cords.append((pts, 3.4))
    for b in bars:
        sh.lines.append(b)
    ring1 = ell_ring(W, H, cx, cy, 106, 106, 4)
    ring2 = ell_ring(W, H, cx, cy, 174, 174, 3)
    # outer scallops with picots
    sc, pics = [], []
    for k in range(24):
        a = k * math.tau / 24
        sx, sy = cx + math.cos(a) * 186, cy + math.sin(a) * 186
        sc.append(arc_pts(sx, sy, 22, a - 1.6, a + 1.6, 18))
        for t in np.linspace(a - 1.3, a + 1.3, 4):
            pics.append((sx + math.cos(t) * 25, sy + math.sin(t) * 25, 2.6))
    scm = strokes(W, H, [(p, 4.2, None) for p in sc])
    pic = np.clip(circles(W, H, pics) - circles(W, H, [(a, b, 1.1) for a, b, _ in pics]), 0, 1)
    # scallop fill: cloth stitch crescent
    fill = np.clip(circles(W, H, [(cx + math.cos(k * math.tau / 24) * 186, cy + math.sin(k * math.tau / 24) * 186, 18) for k in range(24)]) - circles(W, H, [(cx, cy, 178)]), 0, 1)
    art = sh.render(picot=pic, extra_cord=np.maximum.reduce([ring1, ring2, scm]), extra_cloth=fill, seed=37, shadow=0.35)
    show(art, "rp-doily", bg=SATIN)
    save(art, f"{OUT}/doily.webp", max_w=300, quality=84)

if "sprig" in PARTS:
    W = H = 220
    rng = random.Random(41)
    sh = LaceSheet(W, H)
    sh.flower(110, 96, 40, 6, rng, rot=0.3, open_every=3)
    sh.leaf(80, 140, 56, 2.2, rng)
    sh.leaf(140, 140, 56, 0.94, rng)
    sh.stem([(110, 136), (104, 170), (112, 200)], 3.0)
    sh.flower(60, 58, 14, 5, rng, rot=0.1)
    sh.flower(164, 56, 12, 5, rng, rot=0.5)
    art = sh.render(seed=43, shadow=0.35)
    show(art, "rp-sprig", bg=SATIN)
    save(art, f"{OUT}/sprig.webp", max_w=110, quality=86)

if "divider" in PARTS:
    W, H = 720, 64
    rng = random.Random(51)
    sh = LaceSheet(W, H)
    for k, x in enumerate(range(70, 651, 58)):
        big = abs(x - 360) < 30
        sh.flower(x, 32, 19 if big else 11, 6 if big else 5, rng, rot=k * 0.4, open_every=2 if big else 0)
        if not big and x < 650:
            sh.dots.append((x + 29, 32, 3.0))
    lines = strokes(W, H, [([(60, 14), (W - 60, 14)], 2.4, (0.2, 0.2)), ([(60, 50), (W - 60, 50)], 2.4, (0.2, 0.2))])
    tile, _ = tulle_tile(9.0, 4)
    th, tw = tile.shape[:2]
    mesh = np.tile(tile[..., 3], (H // th + 1, W // tw + 1))[:H, :W]
    net = shapes(W, H, [[(60, 14), (W - 60, 14), (W - 60, 50), (60, 50)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    net *= np.clip(1 - np.abs(xx - W / 2) / (W / 2 - 60), 0, 1) ** 0.5
    art = sh.render(net=net, mesh=mesh, extra_cord=lines, seed=53, shadow=0.3)
    show(art, "rp-divider", bg=SATIN)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
