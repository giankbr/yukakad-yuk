"""Ultah Sepuh — an elder's 70th birthday in ivory, sepia watercolour and gold leaf: a painted family tree whose
branches end where framed portraits hang, an ornate gold oval frame, a corner bouquet of peonies and golden
chrysanthemums, a single chrysanthemum emblem and a gold-leaf flourish divider.
Run: python3 -I ultah-sepuh.py [part ...]   Assets -> public/themes/art/ultah-sepuh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c6_lib import *
import _j2_lib
import _p1_lib as _p1
_p1.PREV = PREV

OUT = outdir("ultah-sepuh")
PARTS = sys.argv[1:] or ["tree", "frame", "bouquet", "mum", "divider", "paper"]
IVORY = "#f8f2e4"
UMBER, UMBER_D, UMBER_L = "#8a6a4a", "#5a4130", "#b89a76"
SAGE, SAGE_D = "#9aa686", "#6b7a5c"
GOLD = "#c9a24e"
MUM, MUM_M, MUM_D = "#f1cf7a", "#dca94a", "#b07a2a"
PEONY_L, PEONY_M, PEONY_D = "#f4d9cc", "#e3a792", "#b7705c"

# frame anchor points on the tree canvas (also used by the page CSS as % positions)
TREE_W, TREE_H = 760, 820
ANCHORS = [(380, 168), (170, 336), (590, 336), (262, 540), (498, 540)]


def mum(art, W, H, cx, cy, r, nx, rng, tilt=1.0, rot=0.0):
    """Watercolour chrysanthemum: many rings of slim, slightly cupped petals, denser and darker toward the heart."""
    rings = [(1.0, 44, MUM, MUM_M, 0.34), (0.84, 38, MUM, MUM_M, 0.38), (0.66, 32, MUM_M, MUM, 0.42), (0.48, 24, MUM_M, MUM_D, 0.48), (0.3, 16, MUM_D, MUM_M, 0.55)]
    for i, (rf, n, ca, cb, dens) in enumerate(rings):
        polys = []
        for k in range(n):
            a = k / n * math.tau + rng.uniform(-.09, .09) + i * 0.29 + rot
            L = r * rf * rng.uniform(0.74, 1.06)
            bend = rng.uniform(-0.18, 0.18)
            line = [(cx + math.cos(a + bend * t * t) * L * (0.12 + 0.88 * t), cy + math.sin(a + bend * t * t) * L * (0.12 + 0.88 * t) * tilt) for t in [j / 9 for j in range(10)]]
            polys.append((line, L * rng.uniform(0.12, 0.17), (0.55, 0.0)))
        art = G(art, strokes(W, H, polys), ca, cb, seed=nx(), density=dens, edge=0.8, bloom=0.2, rough=1.0, feather=0.7)
    dots = [(cx + rng.gauss(0, r * 0.06), cy + rng.gauss(0, r * 0.06) * tilt, rng.uniform(1.5, 3)) for _ in range(18)]
    art = G(art, circles(W, H, dots), "#8a5a1c", seed=nx(), density=0.6, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    return art


if "paper" in PARTS:
    t = wrap_paper(512, 512, IVORY, seed=21, fibre=0.8, mottle=0.8)
    save_full(t, f"{OUT}/paper.webp", quality=72)

if "tree" in PARTS:
    W, H = TREE_W, TREE_H
    nx = Seq(51000); rng = random.Random(14); art = blank(W, H)
    # trunk + branches (each branch ends at a frame anchor, plus a few twigs)
    base = (380, 800)
    branches = [
        ([(380, 812), (368, 700), (390, 570), (374, 430), (382, 250)], 64, 14),
        ([(372, 790), (330, 806), (296, 816)], 26, 4),
        ([(388, 790), (430, 804), (470, 816)], 26, 4),
        ([(378, 520), (320, 470), (230, 420), (172, 360)], 20, 6),
        ([(382, 500), (450, 455), (530, 410), (588, 360)], 20, 6),
        ([(372, 690), (330, 640), (290, 600), (262, 566)], 18, 6),
        ([(384, 660), (430, 625), (470, 590), (498, 566)], 18, 6),
        ([(380, 330), (330, 280), (270, 240), (220, 222)], 10, 3),
        ([(380, 320), (440, 270), (500, 236), (560, 226)], 10, 3),
        ([(230, 420), (180, 440), (120, 452)], 8, 2.5),
        ([(530, 410), (590, 430), (646, 440)], 8, 2.5),
        ([(380, 800), (330, 806), (280, 812)], 14, 4),
        ([(380, 800), (432, 808), (486, 812)], 14, 4),
    ]
    items = []
    for pts, w0, w1 in branches:
        c = curve(pts, 40)
        n = len(c)
        for i in range(n - 1):
            t = i / (n - 1)
            items.append(([c[i], c[i + 1]], w0 + (w1 - w0) * t, None))
    bm = strokes(W, H, items)
    art = G(art, bm, UMBER, UMBER_L, seed=nx(), density=0.72, edge=0.6, bloom=0.3, rough=3, gran=0.35)
    art = G(art, side_light(bm, 8, 0, 4), UMBER_D, seed=nx(), density=0.5, edge=0.3, bloom=0.1, rough=2)
    bark = []
    for k in range(26):
        y = rng.uniform(440, 790); x = 380 + rng.uniform(-14, 14)
        bark.append(([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(16, 34))], 1.6, (0.2, 0.3)))
    art = G(art, strokes(W, H, bark) * bm, UMBER_D, seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    # leaves: sage watercolour wreaths around each frame anchor + sprays along the branches
    leaves = [[], [], []]; gold = []
    radii = [96, 76, 76, 66, 66]
    for (ax, ay), R in zip(ANCHORS, radii):
        for k in range(64):
            a = rng.uniform(0, math.tau)
            rr = R * rng.uniform(0.92, 1.32)
            x, y = ax + math.cos(a) * rr * 0.86, ay + math.sin(a) * rr
            L = rng.uniform(16, 30)
            la = a + math.pi / 2 * rng.choice((-1, 1)) + rng.uniform(-.7, .7)
            if rng.random() < 0.16:
                gold.append(petal_pts(x, y, L, L * 0.2, la, n=14))
            else:
                leaves[rng.randrange(3)].append(petal_pts(x, y, L * 1.25, L * 0.24, la, n=14))
    for pts, w0, w1 in branches[3:11]:
        c = curve(pts, 30)
        for j in range(4, len(c), 3):
            x, y = c[j]
            a, b = c[j - 1], c[min(len(c) - 1, j + 1)]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                if rng.random() < 0.6:
                    L = rng.uniform(14, 24)
                    la = ang + side * rng.uniform(0.6, 1.1)
                    leaves[rng.randrange(3)].append(petal_pts(x, y, L * 1.25, L * 0.24, la, n=14))
    for grp, (ca, cb, dn) in zip(leaves, [("#b3bd9d", SAGE, 0.55), (SAGE, SAGE_D, 0.6), (SAGE_D, "#56664a", 0.55)]):
        art = G(art, shapes(W, H, grp), ca, cb, seed=nx(), density=dn, edge=0.7, bloom=0.3, rough=1.4, feather=0.9, gran=0.2)
    lm = np.zeros((H, W), np.float32)
    art = gold_leaf(art, shapes(W, H, gold), GOLD, seed=nx())
    # grass line + a few gold-leaf petals falling
    turf = strokes(W, H, [([(x, 812), (x + rng.uniform(-6, 6), 812 - rng.uniform(8, 20))], 2.2, (0.0, 0.6)) for x in range(250, 520, 7)])
    art = G(art, turf, SAGE, SAGE_D, seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1.2, feather=0.6)
    keep_pixel(art, 0, 0); keep_pixel(art, W - 1, H - 1)
    art[0, 0, 3] = art[H - 1, W - 1, 3] = 0.03   # keep the full canvas so the CSS anchors stay true
    bbox_save(art, "sp-tree", f"{OUT}/tree.webp", 600, tone=IVORY)
    clear()

if "frame" in PARTS:
    W, H = 320, 380
    nx = Seq(52000); art = blank(W, H)
    cx, cy, rx, ry = 160, 196, 118, 150
    def ring(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=18)
        cv.c.drawOval(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry), p)
        p2 = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=3.5)
        cv.c.drawOval(skia.Rect(cx - rx + 17, cy - ry + 17, cx + rx - 17, cy + ry - 17), p2)
    m = mask_from(W, H, ring)
    beads = [(cx + math.cos(k / 64 * math.tau) * (rx + 14), cy + math.sin(k / 64 * math.tau) * (ry + 14), 4.2) for k in range(64)]
    m = np.clip(m + circles(W, H, beads), 0, 1)
    # crest: two leaves and a bow at the top, a small leaf pair at the bottom
    crest = [petal_pts(cx, cy - ry - 10, 52, 14, math.pi + 0.35, n=14), petal_pts(cx, cy - ry - 10, 52, 14, -0.35, n=14),
             petal_pts(cx, cy + ry + 12, 34, 10, math.pi - 0.3, n=12), petal_pts(cx, cy + ry + 12, 34, 10, 0.3, n=12)]
    cm = np.clip(shapes(W, H, crest) + circles(W, H, [(cx, cy - ry - 12, 12), (cx, cy + ry + 12, 8)]), 0, 1)
    full = np.clip(m + cm, 0, 1)
    art = OV(art, full, lambda mm: soft_shadow(mm, "#5a4130", 3, 0.35, 2, 3), pad=12)
    art = gold_leaf(art, full, GOLD, seed=nx(), crack=0.15)
    bbox_save(art, "sp-frame", f"{OUT}/frame.webp", 240, tone=IVORY)
    clear()

if "bouquet" in PARTS:
    W, H = 640, 480
    nx = Seq(53000); rng = random.Random(16); art = blank(W, H)
    # leaves first
    for (x, y, L, a) in [(170, 300, 150, 2.6), (210, 330, 130, 2.0), (420, 300, 150, 0.4), (470, 250, 130, -0.3), (330, 360, 120, 1.6),
                         (120, 230, 110, -2.8), (540, 330, 110, 0.9), (300, 180, 100, -1.9)]:
        lay, _ = _j2_lib.leaf(W, H, x, y, L, a, SAGE, SAGE_D, nx, rng, width=0.32)
        art = glaze(art, lay)
    for x, y, r in [(470, 200, 54), (180, 190, 48), (560, 290, 40)]:
        art = mum(art, W, H, x, y, r, nx, rng, tilt=0.9, rot=rng.uniform(0, 1))
    lay, _ = _j2_lib.peony(W, H, 320, 240, 108, PEONY_L, PEONY_M, PEONY_D, nx, rng)
    art = glaze(art, lay)
    lay, _ = _j2_lib.peony(W, H, 110, 300, 64, PEONY_L, PEONY_M, PEONY_D, nx, rng)
    art = glaze(art, lay)
    lay, _ = _j2_lib.bud(W, H, 410, 340, 22, 0.8, PEONY_M, PEONY_D, SAGE_D, nx, rng)
    art = glaze(art, lay)
    # gold-leaf accents: a few leaves and berries
    gl = shapes(W, H, [petal_pts(250, 110, 46, 13, -1.9, n=12), petal_pts(560, 170, 40, 12, -0.6, n=12), petal_pts(60, 220, 38, 11, -2.6, n=12)])
    art = gold_leaf(art, np.clip(gl + circles(W, H, [(590, 230, 6), (604, 246, 5), (40, 280, 5), (280, 380, 6)]), 0, 1), GOLD, seed=nx())
    bbox_save(art, "sp-bouquet", f"{OUT}/bouquet.webp", 440, tone=IVORY)
    clear()

if "mum" in PARTS:
    W, H = 240, 240
    nx = Seq(54000); rng = random.Random(18); art = blank(W, H)
    art = mum(art, W, H, 120, 120, 104, nx, rng)
    bbox_save(art, "sp-mum", f"{OUT}/mum.webp", 160, tone=IVORY)
    clear()

if "divider" in PARTS:
    W, H = 480, 80
    nx = Seq(55000); art = blank(W, H)
    def flourish(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, StrokeCap=skia.Paint.kRound_Cap)
        for sgn in (-1, 1):
            path = skia.Path(); path.moveTo(240 + sgn * 34, 40)
            path.cubicTo(240 + sgn * 90, 40, 240 + sgn * 120, 18, 240 + sgn * 160, 34)
            path.cubicTo(240 + sgn * 190, 46, 240 + sgn * 205, 36, 240 + sgn * 220, 40)
            cv.c.drawPath(path, p)
            loop = skia.Path(); loop.moveTo(240 + sgn * 150, 30)
            loop.cubicTo(240 + sgn * 140, 12, 240 + sgn * 118, 20, 240 + sgn * 126, 32)
            cv.c.drawPath(loop, p)
        dia = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.drawPath(poly_path([(240, 26), (254, 40), (240, 54), (226, 40)]), dia)
        for sgn in (-1, 1):
            cv.c.drawCircle(240 + sgn * 228, 40, 3.5, dia)
    m = mask_from(W, H, flourish)
    m = np.clip(m + shapes(W, H, [petal_pts(240 + s_ * 26, 40, 22, 6, (0 if s_ > 0 else math.pi), n=10) for s_ in (-1, 1)]), 0, 1)
    art = gold_leaf(art, m, GOLD, seed=nx(), crack=0.1)
    bbox_save(art, "sp-divider", f"{OUT}/divider.webp", 320, tone=IVORY)
    clear()
