"""Linocut Bunga — two-colour relief print (cukil lino) of wildflowers: a red block (poppies, cosmos, a carved sun)
printed first, a black key block (stems, leaves with gouged veins, grass, umbels, outlines, chatter marks) printed
over it slightly out of register. Paper tooth, uneven roller ink and V-gouge cuts everywhere; deep red + warm black
on cream. Run: python3 -I linocut-bunga.py [part ...]  parts: print sprig bloom stalks frieze paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i6_lib import *  # noqa

OUT = outdir("linocut-bunga")
PARTS = sys.argv[1:] or ["print", "sprig", "bloom", "stalks", "frieze", "paper"]
RED, BLK, CREAM = "#b3271f", "#1d1a17", "#f2e8d5"
REG = (4, 3)   # red block offset (registration drift)


def shift(m, dx, dy):
    return np.roll(np.roll(m, dy, 0), dx, 1)


def U(*ms):
    out = ms[0].copy()
    for m in ms[1:]:
        out = np.maximum(out, m)
    return out


def poppy(W, H, cx, cy, r, ang, rng, petals=4):
    """Return (red, black, cuts_red) masks for a front-facing poppy."""
    polys = []
    for k in range(petals):
        a = ang + k * 2 * math.pi / petals + rng.uniform(-0.18, 0.18)
        pts = petal_pts(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12, r * rng.uniform(0.92, 1.05), r * 0.78, a, n=22, cup=0.2)
        polys.append(deform(pts, rng, 1, 0.018))
    red = shapes(W, H, polys)
    # each petal's edge carved where it overlaps the others (flat print, petals read by their cut outlines)
    pm = [shapes(W, H, [q]) for q in polys]
    pcut = np.zeros((H, W), np.float32)
    for i, m in enumerate(pm[1:], 1):
        under = U(*pm[:i])
        pcut = U(pcut, rim(m, 1.3) * under)
    cut = radial_cuts(W, H, cx, cy, r * 0.34, r * 0.9, 26, max(1.6, r * 0.045), rng, a0=ang)
    # separation cuts between petals
    sep = []
    for k in range(petals):
        a = ang + (k + 0.5) * 2 * math.pi / petals + rng.uniform(-0.1, 0.1)
        sep.append(([(cx + math.cos(a) * r * .2, cy + math.sin(a) * r * .2), (cx + math.cos(a) * r * .75, cy + math.sin(a) * r * .75)], max(2.2, r * .06), (0.1, 0.7)))
    cut = U(cut, strokes(W, H, sep) * 0, pcut)
    centre = circles(W, H, [(cx, cy, r * 0.27)])
    star = radial_cuts(W, H, cx, cy, r * 0.05, r * 0.22, 8, max(1.3, r * 0.035), rng, a0=rng.uniform(0, 1), jitter=0.05)
    dots = []
    for k in range(18):
        a = k / 18 * 2 * math.pi + rng.uniform(-.1, .1)
        rr = r * rng.uniform(0.33, 0.42)
        dots.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr, r * rng.uniform(0.03, 0.05)))
    black = np.clip(centre - star, 0, 1)
    black = U(black, circles(W, H, dots))
    outline = rim(red, 1.6) * 0.95
    return red, U(black, outline), cut


def cosmos(W, H, cx, cy, r, rng, petals=8):
    polys = []
    a0 = rng.uniform(0, 1)
    for k in range(petals):
        a = a0 + k * 2 * math.pi / petals + rng.uniform(-.08, .08)
        pts = petal_pts(cx + math.cos(a) * r * .18, cy + math.sin(a) * r * .18, r * rng.uniform(.8, 1.0), r * .42, a, n=10, cup=-.1)
        polys.append(deform(pts, rng, 1, 0.02))
    red = shapes(W, H, polys)
    cut = []
    for k in range(petals):
        a = a0 + k * 2 * math.pi / petals
        cut.append(([(cx + math.cos(a) * r * .32, cy + math.sin(a) * r * .32), (cx + math.cos(a) * r * .78, cy + math.sin(a) * r * .78)], max(1.4, r * .05), (0.1, 0.6)))
    black = circles(W, H, [(cx, cy, r * .2)])
    black = np.clip(black - circles(W, H, [(cx + rng.uniform(-1, 1), cy - r * .05, r * .07)]), 0, 1)
    return red, black, strokes(W, H, cut)


def leaf(W, H, x, y, L, wd, ang, rng):
    """Black leaf with a carved midrib + herringbone vein gouges. Returns (black, cut)."""
    wd = wd * 0.6
    pts = deform(petal_pts(x, y, L, wd, ang, n=18, cup=0.1), rng, 1, 0.02)
    m = shapes(W, H, [pts])
    items = [([P(x, y, ang, L * t, 0) for t in np.linspace(0.1, 0.88, 6)], max(1.8, wd * 0.12), (0.1, 0.5))]
    for t in np.linspace(0.2, 0.74, 5):
        for sgn in (-1, 1):
            items.append((curve([P(x, y, ang, L * t, sgn * wd * .06), P(x, y, ang, L * (t + .1), sgn * wd * .42), P(x, y, ang, L * (t + .15), sgn * wd * .66)], 10), max(2.2, wd * 0.14), (0.05, 0.75)))
    return m, strokes(W, H, items)


def stem(pts, wd):
    return (curve(pts, 40), wd, (0.02, 0.1))


def umbel(W, H, cx, cy, r, rng):
    """Wild carrot umbel: rays from a point + dotted florets."""
    rays, dots = [], []
    for k in range(11):
        a = -math.pi / 2 + (k - 5) * 0.2 + rng.uniform(-.05, .05)
        L = r * rng.uniform(.8, 1.0)
        ex, ey = cx + math.cos(a) * L, cy + math.sin(a) * L
        rays.append(([(cx, cy), ((cx + ex) / 2, (cy + ey) / 2 + 2), (ex, ey)], 2.0, None))
        for j in range(7):
            b = rng.uniform(0, 2 * math.pi); d = rng.uniform(0, r * .16)
            dots.append((ex + math.cos(b) * d, ey + math.sin(b) * d * .6 - r * .04, rng.uniform(1.6, 3.0)))
    return U(strokes(W, H, rays), circles(W, H, dots))


def bell(W, H, x, y, s, ang, rng):
    """Small hanging bell flower (red) on a black pedicel."""
    pts = [P(x, y, ang, 0, -s * .18), P(x, y, ang, s * .6, -s * .42), P(x, y, ang, s * 1.0, -s * .5), P(x, y, ang, s * .92, -s * .1),
           P(x, y, ang, s * 1.05, 0), P(x, y, ang, s * .92, s * .1), P(x, y, ang, s * 1.0, s * .5), P(x, y, ang, s * .6, s * .42), P(x, y, ang, 0, s * .18)]
    red = shapes(W, H, [deform(pts, rng, 1, 0.05)])
    cut = strokes(W, H, [([P(x, y, ang, s * .2, 0), P(x, y, ang, s * .85, 0)], max(1.2, s * .07), (0.1, 0.5))])
    return red, cut


def grass(W, H, rng, x0, x1, base, hmin, hmax, n, lean=0.0):
    items = []
    for i in range(n):
        x = rng.uniform(x0, x1); hgt = rng.uniform(hmin, hmax); b = lean + rng.uniform(-0.35, 0.35)
        items.append(([(x, base), (x + b * hgt * .3, base - hgt * .5), (x + b * hgt, base - hgt)], rng.uniform(3, 6), (0.0, 0.85)))
    return strokes(W, H, items)


def render(W, H, red, black, seed):
    art = blank(W, H)
    art = print_ink(art, shift(red, *REG), RED, seed=seed, wear=0.18, roller=0.26, tooth=0.22)
    art = print_ink(art, black, BLK, seed=seed + 7, wear=0.26, roller=0.18, tooth=0.3)
    return art


# ------------------------------------------------------------------ cover print
def part_print():
    W, H = 680, 860
    rng = random.Random(11)
    red = np.zeros((H, W), np.float32); black = red.copy(); rcut = red.copy(); bcut = red.copy()
    # block edge (key block frame with chipped, uneven border)
    frame_out = shape_mask(W, H, deform([(14, 16), (W - 12, 12), (W - 16, H - 14), (12, H - 12)], rng, 4, 0.004), smooth=False)
    frame_in = shape_mask(W, H, deform([(30, 32), (W - 30, 30), (W - 32, H - 30), (30, H - 32)], rng, 4, 0.004), smooth=False)
    border = np.clip(frame_out - frame_in, 0, 1)
    border = np.clip(border - gouges(W, H, rng, border, 70, (5, 12), (1.6, 3.0), 0.0, 3.2), 0, 1)
    black = U(black, border)
    # carved sun (red) top-right with concentric gouged rings
    sx, sy, sr = 470, 196, 118
    sun = circles(W, H, [(sx, sy, sr)])
    rings = []
    for k, rr in enumerate(np.arange(24, sr - 8, 15)):
        rings.append((arc_pts(sx, sy, rr, rng.uniform(0, 1), rng.uniform(0, 1) + 2 * math.pi * rng.uniform(.6, .95), 40), 2.6, (0.1, 0.2)))
    red = U(red, sun); rcut = U(rcut, strokes(W, H, rings))
    # ground: black hill with grass cuts
    gpts = [(30, 700)] + [(x, 690 + 16 * math.sin(x / 70) + rng.uniform(-4, 4)) for x in range(60, W - 20, 40)] + [(W - 30, 700), (W - 30, H - 30), (30, H - 30)]
    ground = shape_mask(W, H, gpts, smooth=False) * frame_in
    gc = gouges(W, H, rng, ground, 150, (12, 26), (2.0, 3.6), -math.pi / 2, 0.45, curve=0.35)
    black = U(black, ground); bcut = U(bcut, gc)
    # stems + leaves
    st = []
    flowers = [(212, 300, 108, 0.3, 470), (420, 470, 84, 1.1, 420), (156, 560, 64, -0.4, 300)]
    for (cx, cy, r, a, ln) in flowers:
        st.append(stem([(cx + rng.uniform(-30, 30), 760), (cx - 18, cy + (760 - cy) * .55), (cx, cy + r * 0.3)], 6.5))
    st += [stem([(560, 760), (585, 560), (568, 400)], 4.5), stem([(330, 760), (318, 600), (346, 520)], 4.0), stem([(96, 760), (80, 600), (104, 430)], 4.0),
           stem([(610, 760), (630, 640), (612, 590)], 3.5)]
    black = U(black, strokes(W, H, st))
    for (x, y, L, wd, a) in [(226, 640, 150, 44, -2.4), (214, 600, 130, 40, -0.6), (420, 650, 130, 38, -0.55), (428, 600, 112, 34, -2.55),
                             (160, 680, 100, 30, -2.7), (575, 600, 96, 28, -0.9), (96, 640, 90, 26, -0.5)]:
        m, c = leaf(W, H, x, y, L, wd, a, rng)
        black = U(black, m); bcut = U(bcut, c)
    # umbel + bells + buds
    black = U(black, umbel(W, H, 568, 400, 70, rng))
    black = U(black, strokes(W, H, [stem([(104, 430), (128, 360), (166, 330)], 3.0), stem([(104, 430), (80, 370), (60, 352)], 3.0)]))
    for (x, y, s, a) in [(166, 330, 34, 1.3), (60, 352, 30, 1.9), (104, 410, 30, 1.5)]:
        rm, rc = bell(W, H, x, y, s, a, rng); red = U(red, rm); rcut = U(rcut, rc)
    for (cx, cy, r, a, _) in flowers:
        rm, bm, cm = poppy(W, H, cx, cy, r, a, rng)
        red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    rm, bm, cm = cosmos(W, H, 346, 516, 44, rng)
    red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    rm, bm, cm = cosmos(W, H, 612, 586, 34, rng)
    red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    for (dx, dy, dr, sx0) in [(64, 500, 30, 70), (520, 650, 24, 520)]:
        black = U(black, strokes(W, H, [stem([(sx0, 760), (dx + 6, (dy + 760) / 2), (dx, dy)], 3.0)]))
        pp = []; cc = []
        for k in range(11):
            a = k / 11 * 2 * math.pi + rng.uniform(-.06, .06)
            pp.append(deform(petal_pts(dx + math.cos(a) * dr * .2, dy + math.sin(a) * dr * .2, dr, dr * .22, a, n=10), rng, 1, 0.02))
            cc.append(([(dx + math.cos(a) * dr * .38, dy + math.sin(a) * dr * .38), (dx + math.cos(a) * dr * .85, dy + math.sin(a) * dr * .85)], 1.6, (0.1, 0.5)))
        black = U(black, shapes(W, H, pp)); bcut = U(bcut, strokes(W, H, cc))
        red = U(red, circles(W, H, [(dx, dy, dr * .26)]))
        bcut = U(bcut, circles(W, H, [(dx, dy, dr * .3)]))
    # bud on a curved stem
    black = U(black, strokes(W, H, [stem([(330, 760), (300, 660), (290, 610)], 3.5)]))
    red = U(red, shapes(W, H, [deform(petal_pts(290, 612, 36, 22, -1.7, n=10, cup=.2), rng, 1, 0.05)]))
    # chatter: leftover ridges in the cleared background
    occupied = np.clip(gaussian_filter(U(red, black, sun), 6) * 4, 0, 1)
    region = frame_in * (1 - occupied)
    chatter = gouges(W, H, rng, region, 120, (8, 22), (1.6, 3.0), 0.05, 0.25, thr=0.9, curve=0.15)
    black = U(black, chatter * 0.95)
    # carve
    red = np.clip(red - rcut, 0, 1) * frame_out
    black = np.clip(black - bcut, 0, 1)
    art = render(W, H, red, black, 21)
    preview(art, "lino-print", tone=CREAM)
    save(art, f"{OUT}/print.webp", max_w=520, quality=66)


def part_sprig():
    W, H = 460, 90
    rng = random.Random(5)
    black = strokes(W, H, [stem([(18, 50), (120, 44), (230, 48), (340, 42), (442, 46)], 3.2)])
    bcut = np.zeros((H, W), np.float32); red = bcut.copy(); rcut = bcut.copy()
    for x, side in [(70, -1), (130, 1), (170, -1), (300, 1), (330, -1), (390, 1)]:
        m, c = leaf(W, H, x, 46, 40, 14, -math.pi / 2 * side - 0.6 * (1 if x < 230 else -1) * side, rng)
        black = U(black, m); bcut = U(bcut, c)
    rm, bm, cm = poppy(W, H, 230, 45, 30, 0.4, rng)
    red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    for x in (30, 432):
        red = U(red, circles(W, H, [(x, 48, 7)]))
    art = render(W, H, np.clip(red - rcut, 0, 1), np.clip(black - bcut, 0, 1), 31)
    preview(art, "lino-sprig", tone=CREAM)
    save(art, f"{OUT}/sprig.webp", max_w=440, quality=82)


def part_bloom():
    W, H = 260, 260
    rng = random.Random(8)
    rm, bm, cm = poppy(W, H, 130, 130, 100, 0.2, rng, petals=5)
    art = render(W, H, np.clip(rm - cm, 0, 1), bm, 41)
    preview(art, "lino-bloom", tone=CREAM)
    save(art, f"{OUT}/bloom.webp", max_w=220, quality=82)


def part_stalks():
    W, H = 300, 720
    rng = random.Random(14)
    red = np.zeros((H, W), np.float32); black = red.copy(); rcut = red.copy(); bcut = red.copy()
    black = U(black, grass(W, H, rng, 10, 290, 712, 120, 330, 26, lean=0.15))
    black = U(black, strokes(W, H, [stem([(120, 712), (110, 420), (140, 160)], 5), stem([(200, 712), (220, 520), (196, 330)], 4), stem([(60, 712), (48, 540), (74, 440)], 3.5)]))
    for (x, y, L, wd, a) in [(114, 520, 110, 34, -2.5), (118, 470, 96, 30, -0.55), (214, 600, 90, 28, -0.6), (54, 600, 80, 24, -2.6)]:
        m, c = leaf(W, H, x, y, L, wd, a, rng)
        black = U(black, m); bcut = U(bcut, c)
    rm, bm, cm = poppy(W, H, 140, 150, 74, 0.5, rng)
    red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    rm, bm, cm = cosmos(W, H, 196, 326, 40, rng)
    red = U(red, rm); rcut = U(rcut, cm); black = U(black, bm)
    black = U(black, umbel(W, H, 74, 440, 52, rng))
    art = render(W, H, np.clip(red - rcut, 0, 1), np.clip(black - bcut, 0, 1), 51)
    preview(art, "lino-stalks", tone=CREAM)
    save(art, f"{OUT}/stalks.webp", max_w=260, quality=80)


def part_frieze():
    """Black block strip with reversed (carved-out) leaves and red poppies printed into the cut windows."""
    W, H = 820, 200
    rng = random.Random(23)
    block = shape_mask(W, H, deform([(4, 6), (W - 4, 4), (W - 6, H - 6), (6, H - 4)], rng, 4, 0.004), smooth=False)
    cutout = np.zeros((H, W), np.float32); red = cutout.copy(); rcut = cutout.copy()
    # vine
    vine = curve([(0, 120)] + [(x, 100 + 34 * math.sin(x / 62)) for x in range(60, W, 60)] + [(W, 110)], 120)
    cutout = U(cutout, strokes(W, H, [(vine, 5, None)]))
    for i, x in enumerate(range(50, W, 105)):
        y = 100 + 34 * math.sin(x / 62)
        if i % 2 == 0:
            rm, bm, cm = poppy(W, H, x, y - 6, 40, rng.uniform(0, 1), rng)
            win = np.clip(gaussian_filter(rm, 1.5) * 3, 0, 1)
            cutout = U(cutout, win * 0)  # red sits on the black block's carved window
            cutout = U(cutout, np.clip(gaussian_filter(rm, 3) * 3, 0, 1))
            red = U(red, rm); rcut = U(rcut, cm)
            # centre stays black: subtract from cutout
            cutout = np.clip(cutout - circles(W, H, [(x, y - 6, 11)]), 0, 1)
        else:
            for s in (-1, 1):
                a = -math.pi / 2 + s * 1.0 + rng.uniform(-.15, .15)
                pts = deform(petal_pts(x, y, 54, 11, a, n=16), rng, 1, 0.02)
                cutout = U(cutout, shapes(W, H, [pts]))
                rib = strokes(W, H, [([P(x, y, a, 8, 0), P(x, y, a, 44, 0)], 2.0, (0.1, 0.6))])
                cutout = np.clip(cutout - rib, 0, 1)
    cutout = U(cutout, gouges(W, H, rng, block, 90, (6, 14), (1.6, 2.8), 0.0, 3.2, curve=.3))
    black = np.clip(block - cutout, 0, 1)
    art = blank(W, H)
    art = print_ink(art, shift(np.clip(red - rcut, 0, 1), *REG), RED, seed=61, wear=.28, roller=.25)
    art = print_ink(art, black, BLK, seed=62, wear=.22, roller=.2, tooth=.3)
    preview(art, "lino-frieze", tone=CREAM)
    save(art, f"{OUT}/frieze.webp", max_w=780, quality=78)


def part_paper():
    S = 512
    base = np.asarray(paper(S, S, CREAM, 9, fiber=0.8, mottle=0.6), np.float32) / 255
    # stray ink specks (offset from the press)
    rng = np.random.default_rng(4)
    sp = (rng.random((S, S)) > 0.9993).astype(np.float32)
    sp = gaussian_filter(sp, 0.8) * 4
    rgb = base[..., :3] * (1 - np.clip(sp, 0, .25)[..., None])
    n = wrap_noise(S, S, 7, 40)
    rgb *= (0.985 + 0.03 * n)[..., None]
    img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    # make seamless by half-offset blending
    a = np.asarray(img, np.float32)
    b = np.roll(np.roll(a, S // 2, 0), S // 2, 1)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    k = np.clip(np.minimum(np.minimum(xx, S - 1 - xx), np.minimum(yy, S - 1 - yy)) / (S / 4), 0, 1)[..., None]
    out = Image.fromarray((a * k + b * (1 - k)).astype(np.uint8))
    out.save(f"{OUT}/paper.webp", "WEBP", quality=72, method=6)
    print("paper.webp", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
