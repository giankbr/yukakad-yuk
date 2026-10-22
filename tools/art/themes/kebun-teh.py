"""Kebun Teh — Puncak tea estate in fresh morning watercolour (original): contour rows of clipped tea bushes on terraced
slopes, a winding pickers' path, tall shade trees, a small wooden hut on stilts, pickers in caping hats, distant
double-peaked volcano and drifting mist. Also a tea-row band, a pucuk teh sprig (two leaves and a bud), a bamboo
picking basket and a mist wisp. Run: python3 -I kebun-teh.py [part ...]
parts: scene band sprig basket mist   Assets -> public/themes/art/kebun-teh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e5_lib import *  # noqa

OUT = outdir("kebun-teh")
PARTS = sys.argv[1:] or ["scene", "band", "sprig", "basket", "mist"]
BG = "#f7f3e8"
TEA, TEA2, TEAD, TEAL = "#6fa548", "#8cbc4f", "#2f6b3a", "#c4dc7a"
SAGE, MOUNT, MOUNT2 = "#8eb59a", "#93a9bd", "#b3c3cf"
EARTH, EARTHD, WOOD, ROOF = "#c9a46a", "#9a6e45", "#a8774c", "#8a4b33"


def wash(art, m, a, b=None, seed=1, **k):
    k.setdefault("density", 0.8)
    return G(art, m, a, b, seed=seed, **k)


def tea_rows(art, W, H, top, x0, x1, ybot, n, nx, rng, col=TEAD, col2=TEA, hi=TEAL, thick=None, bump=True, curve_pow=1.7, clip=None, fill=0.72):
    """Contour rows of clipped tea hedges between a top contour `top(x)` and ybot; spacing widens toward the viewer and
    each hedge fills `fill` of its spacing, with a lumpy clipped top."""
    rows = []
    xm = (x0 + x1) / 2
    span = max(10, ybot - top(xm))
    for k in range(n):
        d0, d1 = (k + 0.5) / n, (k + 1.5) / n
        dd = d0 ** curve_pow
        sp = (d1 ** curve_pow - dd) * span
        th = max(2.5, sp * fill)
        ph = rng.uniform(0, 6)
        pts = [(x, top(x) + dd * (ybot - top(x)) + math.sin(x * 0.011 + ph) * th * 0.12) for x in np.linspace(x0, x1, 60)]
        rows.append((pts, th))
    items = [([(x, y + th * 0.1) for x, y in p], th * 0.7, None) for p, th in rows]
    m = strokes(W, H, items)
    if bump:
        bumps = []
        for p, th in rows:
            xs = np.arange(x0, x1, max(2.0, th * 0.55))
            px_, py_ = np.array([q[0] for q in p]), np.array([q[1] for q in p])
            for x in xs:
                y = float(np.interp(x, px_, py_))
                bumps.append((x + rng.uniform(-1, 1) * th * .1, y - th * 0.08 + rng.uniform(-1, 1) * th * 0.05, th * rng.uniform(0.36, 0.46)))
        m = np.clip(m + circles(W, H, bumps), 0, 1)
    if clip is not None:
        m = m * clip
    art = wash(art, m, col2, col, seed=nx(), density=0.86, edge=0.45, bloom=0.2, gran=0.35, rough=2.2, feather=0.9)
    # sunlit tops
    tops = strokes(W, H, [([(x, y - th * 0.2) for x, y in p], th * 0.3, None) for p, th in rows])
    shad = strokes(W, H, [([(x, y + th * 0.32) for x, y in p], th * 0.22, None) for p, th in rows])
    if clip is not None:
        tops = tops * clip
    art = wash(art, tops * m, hi, TEA2, seed=nx(), density=0.55, edge=0.2, bloom=0.1, gran=0.3, rough=1.5, feather=0.8)
    if clip is not None:
        shad = shad * clip
    art = wash(art, shad * m, "#1f4f2e", None, seed=nx(), density=0.35, edge=0.1, bloom=0.0, gran=0.3, rough=1.2, feather=1.0)
    return art


def caping_picker(art, W, H, x, y, s, body, nx):
    """Tiny tea picker seen from behind/side: caping hat, body dab, basket on the back (no face)."""
    art = wash(art, ellipses(W, H, [(x, y + s * 0.55, s * 0.32, s * 0.5, 0)]), body, mix(body, "#000000", .15), seed=nx(), density=0.9, edge=0.3, rough=0.8, feather=0.5)
    art = wash(art, ellipses(W, H, [(x + s * 0.3, y + s * 0.5, s * 0.26, s * 0.32, 0)]), EARTH, EARTHD, seed=nx(), density=0.9, edge=0.4, rough=0.6, feather=0.4)
    hat = shapes(W, H, [[(x - s * 0.8, y + s * 0.12), (x - s * 0.1, y - s * 0.4), (x + s * 0.1, y - s * 0.4), (x + s * 0.8, y + s * 0.12), (x, y + s * 0.2)]], smooth=False)
    art = wash(art, hat, "#f1dca0", "#d9b86d", seed=nx(), density=1.0, edge=0.7, rough=0.4, feather=0.3)
    art = wash(art, side_light(hat, 0, -3, 2), "#a8844a", None, seed=nx(), density=0.6, edge=0.1, rough=0.3, feather=0.3)
    return art


def shade_tree(art, W, H, x, yb, h, nx, rng):
    trunk = strokes(W, H, [(curve([(x, yb), (x + rng.uniform(-6, 6), yb - h * 0.5), (x + rng.uniform(-10, 10), yb - h)], 20), max(2, h * 0.025), (0.0, 0.6))])
    br = []
    for _ in range(4):
        a = rng.uniform(-2.4, -0.7)
        sx, sy = x + rng.uniform(-6, 6), yb - h * rng.uniform(0.6, 0.95)
        br.append(([(sx, sy), (sx + math.cos(a) * h * 0.22, sy + math.sin(a) * h * 0.14)], max(1.2, h * 0.012), (0, 0.5)))
    art = wash(art, np.clip(trunk + strokes(W, H, br), 0, 1), "#6d6250", "#55493a", seed=nx(), density=0.8, edge=0.4, rough=0.8, feather=0.5)
    blobs = []
    for _ in range(5):
        cx, cy = x + rng.uniform(-h * 0.26, h * 0.26), yb - h * rng.uniform(0.9, 1.06)
        blobs.append(deform(ellipse_pts(cx, cy, h * rng.uniform(0.12, 0.2), h * rng.uniform(0.04, 0.07), 10, rng.uniform(-.1, .1)), rng, 2, 0.08))
    cm = shapes(W, H, blobs)
    art = wash(art, cm, "#5f8f52", "#3f6e42", seed=nx(), density=0.72, edge=0.55, bloom=0.3, gran=0.3, rough=3, feather=1.2)
    return art


if "scene" in PARTS:
    W, H = 900, 820
    nx = Seq(81100); rng = random.Random(811)
    art = blank(W, H)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    # sky: thin cool wash fading to nothing at the top, warm near the horizon
    sky = np.clip((yy - 0.02) * 3.2, 0, 1) * (yy < 0.55)
    art = wash(art, sky * 0.55, "#cfe2ea", "#f3e6c8", seed=nx(), density=0.5, edge=0.0, bloom=0.4, gran=0.15, rough=4, feather=6)
    # pale sun glow
    art = OV(art, circles(W, H, [(690, 150, 46)]), lambda m: glow(m, "#fff3cf", 30, 0.5), pad=80)
    # volcano (twin peaks), far
    vol = [(-20, 370), (120, 300), (250, 238), (330, 214), (372, 222), (420, 202), (470, 176), (520, 168), (560, 180), (640, 230), (760, 290), (920, 340), (920, 420), (-20, 420)]
    vm = shapes(W, H, [deform(vol, rng, 2, 0.006)])
    art = wash(art, vm, MOUNT2, MOUNT, seed=nx(), density=0.62, edge=0.5, bloom=0.25, gran=0.4, rough=3, feather=1.2)
    gul = []
    for i in range(9):
        x0 = 400 + i * 30 + rng.uniform(-6, 6)
        y0 = 176 + abs(x0 - 510) * 0.55
        gul.append((curve([(x0, y0 + 4), (x0 + (x0 - 510) * 0.25, y0 + 60), (x0 + (x0 - 510) * 0.5, y0 + 130)], 16), rng.uniform(3, 6), (0.3, 0.8)))
    art = wash(art, strokes(W, H, gul) * vm, "#7f93a8", None, seed=nx(), density=0.22, edge=0.2, rough=1.4, feather=0.8)
    art = mist(art, W, H, [(450, 340, 520, 40, 0.75), (180, 360, 300, 26, 0.6)], seed=nx())
    clear()
    # far ridge (sage)
    far = lambda x: 372 + 22 * math.sin(x * 0.009 + 0.6) + 12 * math.sin(x * 0.023)
    fm = shapes(W, H, [contour(far, -20, 920) + [(920, 720), (-20, 720)]])
    art = wash(art, fm, "#a9c6a0", SAGE, seed=nx(), density=0.68, edge=0.45, bloom=0.3, gran=0.35, rough=3, feather=1.2)
    art = tea_rows(art, W, H, far, -20, 920, 520, 9, nx, rng, col="#6f9a68", col2="#8fb586", hi="#c8dcb4", bump=False, clip=fm, fill=0.5)
    art = mist(art, W, H, [(620, 430, 380, 30, 0.7), (120, 446, 260, 22, 0.55)], seed=nx())
    clear()
    # mid hill (right) with hut and trees
    mid = lambda x: 470 - 86 * math.exp(-((x - 640) / 250) ** 2) + 6 * math.sin(x * 0.02)
    mm = shapes(W, H, [[(60, 560), (140, 500)] + contour(mid, 200, 920) + [(920, 700), (60, 700)]])
    art = wash(art, mm, "#cfe39a", "#b9d77e", seed=nx(), density=0.7, edge=0.35, bloom=0.3, gran=0.3, rough=3, feather=1.4)
    art = tea_rows(art, W, H, mid, 60, 920, 680, 11, nx, rng, clip=mm, fill=0.62)
    for tx, th in ((470, 120), (760, 150), (880, 110)):
        art = shade_tree(art, W, H, tx, mid(tx) + 6, th, nx, rng)
    clear()
    # hut on stilts near the crest
    hx, hy = 612, mid(612) - 4
    stilts = strokes(W, H, [([(hx - 26, hy - 18), (hx - 26, hy + 8)], 3, None), ([(hx + 22, hy - 18), (hx + 22, hy + 8)], 3, None)])
    art = wash(art, stilts, "#6b4a32", None, seed=nx(), density=0.9, edge=0.3, rough=0.6, feather=0.4)
    wall = shapes(W, H, [[(hx - 34, hy - 46), (hx + 30, hy - 46), (hx + 30, hy - 16), (hx - 34, hy - 16)]], smooth=False)
    art = wash(art, wall, "#c79868", WOOD, seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=0.8, feather=0.5)
    art = wash(art, strokes(W, H, [([(hx - 30 + i * 8, hy - 44), (hx - 30 + i * 8, hy - 18)], 1.2, None) for i in range(8)]) * wall, "#8a5f3a", None, seed=nx(), density=0.5, edge=0.1, rough=0.4, feather=0.3)
    art = wash(art, shapes(W, H, [[(hx + 2, hy - 40), (hx + 16, hy - 40), (hx + 16, hy - 24), (hx + 2, hy - 24)]], smooth=False), "#4a3428", None, seed=nx(), density=0.9, rough=0.4, feather=0.3)
    roof = shapes(W, H, [[(hx - 46, hy - 42), (hx - 2, hy - 74), (hx + 42, hy - 42), (hx + 36, hy - 38), (hx - 40, hy - 38)]], smooth=False)
    art = wash(art, roof, "#a65b3c", ROOF, seed=nx(), density=0.92, edge=0.6, bloom=0.2, rough=0.8, feather=0.5)
    clear()
    # left foreground slope
    fl = lambda x: 520 + 0.16 * (x - 0) + 40 * math.sin(x * 0.012 + 1.2) - 90 * math.exp(-((x - 60) / 160) ** 2)
    flm = shapes(W, H, [contour(fl, -20, 560) + [(560, 820), (-20, 820)]])
    art = knockout(art, flm, 0.95, 0.8)
    art = wash(art, flm, "#d6e8a2", "#bcd884", seed=nx(), density=0.74, edge=0.35, bloom=0.3, gran=0.3, rough=3, feather=1.4)
    art = tea_rows(art, W, H, fl, -20, 560, 860, 8, nx, rng, clip=flm)
    clear()
    # right foreground slope (closer) with the pickers' path between
    fr = lambda x: 600 - 0.14 * (x - 420) + 26 * math.sin(x * 0.016)
    frm = shapes(W, H, [[(300, 840), (340, 720)] + contour(fr, 390, 920) + [(920, 840)]])
    art = knockout(art, frm, 0.95, 0.8)
    art = wash(art, frm, "#d4e7a0", "#b5d47c", seed=nx(), density=0.74, edge=0.35, bloom=0.3, gran=0.3, rough=3, feather=1.4)
    art = tea_rows(art, W, H, fr, 300, 920, 870, 7, nx, rng, clip=frm)
    clear()
    # winding path from the bottom toward the hut
    pth = curve([(470, 830), (440, 760), (500, 690), (470, 630), (530, 572), (600, 520), (612, mid(612) + 10)], 80)
    pm = np.zeros((H, W), np.float32)
    items = []
    for i in range(len(pth) - 1):
        t = 1 - i / (len(pth) - 1)
        items.append(([pth[i], pth[i + 1]], 3 + 30 * t ** 1.6, None))
    pm = strokes(W, H, items)
    art = knockout(art, pm, 0.7, 1.5)
    art = wash(art, pm, "#e3c995", EARTH, seed=nx(), density=0.8, edge=0.5, bloom=0.25, gran=0.5, rough=2, feather=1.0)
    clear()
    # pickers
    for (px, py, s_, c) in ((548, 548, 26, "#c44a3a"), (690, 610, 32, "#3d6ea6"), (330, 650, 38, "#d98a3a"), (735, 474, 18, "#c44a3a")):
        art = caping_picker(art, W, H, px, py, s_, c, nx)
    art = mist(art, W, H, [(300, 500, 330, 28, 0.45), (760, 530, 240, 22, 0.4)], seed=nx())
    # fade the bottom edge into paper
    a = art[..., 3] * np.clip((H - 6 - np.arange(H)[:, None]) / 60, 0, 1)
    art[..., 3] = a
    preview(art, "kt-scene", tone=BG)
    save(art, f"{OUT}/scene.webp", max_w=660, quality=74)
    clear()

if "band" in PARTS:
    W, H = 900, 280
    nx = Seq(81200); rng = random.Random(812)
    art = blank(W, H)
    top = lambda x: 120 + 26 * math.sin(x * 0.008 + 0.4) + 10 * math.sin(x * 0.03)
    m = shapes(W, H, [contour(top, -10, 910) + [(910, 290), (-10, 290)]])
    art = wash(art, m, "#d6e8a2", "#bcd884", seed=nx(), density=0.72, edge=0.35, bloom=0.3, gran=0.3, rough=3, feather=1.4)
    art = tea_rows(art, W, H, top, -10, 910, 320, 6, nx, rng, clip=m)
    art = shade_tree(art, W, H, 160, top(160) + 4, 110, nx, rng)
    art = caping_picker(art, W, H, 640, top(640) + 30, 30, "#c44a3a", nx)
    art = caping_picker(art, W, H, 410, top(410) + 52, 34, "#3d6ea6", nx)
    preview(art, "kt-band", tone=BG)
    save(art, f"{OUT}/band.webp", max_w=640, quality=78)
    clear()

if "sprig" in PARTS:
    W, H = 300, 300
    nx = Seq(81300); rng = random.Random(813)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(150, 290), (146, 220), (152, 150), (160, 70)], 30), 5, (0.0, 0.5))])
    art = wash(art, stem, "#7a9a48", "#5d7f3a", seed=nx(), density=0.85, edge=0.4, rough=1, feather=0.6)
    leaves = [(149, 196, 128, 25, math.pi + 0.5, TEA, TEAD), (152, 158, 118, 23, -0.42, TEA2, TEA)]
    for x, y, L, w, a, c1, c2 in leaves:
        lm = shapes(W, H, [deform(leaf_cut(x, y, L, w, a, 22, .25), rng, 1, 0.01)])
        art = wash(art, lm, c1, c2, seed=nx(), density=0.85, edge=0.6, bloom=0.35, gran=0.35, rough=2, feather=1)
        ca, sa = math.cos(a), math.sin(a)
        art = wash(art, strokes(W, H, [([(x + ca * L * .08, y + sa * L * .08), (x + ca * L * .85, y + sa * L * .85)], 2.2, (0.1, 0.6))]), TEAD, None, seed=nx(), density=0.5, edge=0.2, rough=0.6, feather=0.5)
        # serrated edge hints
        serr = []
        for t in np.linspace(0.2, 0.85, 7):
            for sd in (1, -1):
                ex, ey = x + ca * L * t - sa * sd * w * math.sin(math.pi * t) ** .85 * .92, y + sa * L * t + ca * sd * w * math.sin(math.pi * t) ** .85 * .92
                serr.append(([(ex, ey), (ex + ca * 5, ey + sa * 5)], 1.4, None))
        art = wash(art, strokes(W, H, serr) * lm, TEAD, None, seed=nx(), density=0.45, edge=0.1, rough=0.4, feather=0.4)
    bud = shapes(W, H, [deform(petal_pts(160, 112, 66, 16, -math.pi / 2 + 0.05, 16), rng, 1, 0.01)])
    art = wash(art, bud, TEAL, TEA2, seed=nx(), density=0.88, edge=0.6, bloom=0.3, gran=0.3, rough=1.6, feather=0.8)
    preview(art, "kt-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=150, quality=82)
    clear()

if "basket" in PARTS:
    W, H = 360, 340
    nx = Seq(81400); rng = random.Random(814)
    art = blank(W, H)
    # heap of fresh shoots peeking out
    heap = []
    for _ in range(26):
        x, y = rng.uniform(90, 270), rng.uniform(70, 120)
        heap.append(deform(leaf_cut(x, y, rng.uniform(40, 64), rng.uniform(12, 18), rng.uniform(-2.8, -0.4), 14, .2), rng, 1, 0.01))
    art = wash(art, shapes(W, H, heap), TEA2, TEA, seed=nx(), density=0.85, edge=0.6, bloom=0.3, gran=0.3, rough=2, feather=1)
    art = wash(art, shapes(W, H, heap[::3]), TEAL, None, seed=nx(), density=0.6, edge=0.3, rough=1.5, feather=0.8)
    body = shapes(W, H, [[(70, 110), (290, 110), (282, 200), (262, 268), (220, 298), (140, 298), (98, 268), (78, 200)]], smooth=True)
    art = knockout(art, body, 1.0, 1)
    art = wash(art, body, "#e2c48a", "#c9a46a", seed=nx(), density=0.88, edge=0.55, bloom=0.3, gran=0.5, rough=1.6, feather=0.8)
    weave = []
    for i in range(19):
        y = 118 + i * 10
        weave.append(([(60, y + (i % 2) * 2), (300, y - (i % 2) * 2)], 3.4 if i % 2 else 2.0, None))
    for i in range(8):
        x = 96 + i * 24
        weave.append(([(x, 112), (x + (180 - x) * 0.12, 298)], 1.2, None))
    art = wash(art, strokes(W, H, weave) * body, EARTHD, None, seed=nx(), density=0.5, edge=0.2, rough=0.6, feather=0.5)
    art = wash(art, side_light(body, 24, 0, 18), "#8a6338", None, seed=nx(), density=0.45, edge=0.0, rough=2, feather=2)
    rimm = strokes(W, H, [([(64, 110), (296, 110)], 12, None)])
    art = wash(art, rimm, "#b48a52", EARTHD, seed=nx(), density=0.9, edge=0.5, rough=1, feather=0.6)
    strap = strokes(W, H, [(curve([(80, 112), (60, 40), (180, 6), (300, 40), (280, 112)], 40), 6, None)])
    art = wash(art, knockout(blank(W, H), np.zeros((H, W), np.float32)) if False else strap * (1 - body), "#8a5f3a", None, seed=nx(), density=0.7, edge=0.4, rough=0.8, feather=0.5)
    preview(art, "kt-basket", tone=BG)
    save(art, f"{OUT}/basket.webp", max_w=170, quality=82)
    clear()

if "mist" in PARTS:
    W, H = 900, 200
    nx = Seq(81500)
    art = blank(W, H)
    art = mist(art, W, H, [(300, 100, 320, 46, 0.85), (640, 112, 300, 38, 0.8), (460, 90, 200, 30, 0.6)], seed=nx())
    preview(art, "kt-mist", bg="#8fa6a0")
    save(art, f"{OUT}/mist.webp", max_w=560, quality=70)
    clear()
