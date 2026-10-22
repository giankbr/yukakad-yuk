"""Istana Maimun — Malay-Deli royal wedding: gouache palace facade (original, inspired by Deli palace arches and domes),
gilt carved arch frame with pucuk rebung band and lebah bergantung pendants, carved fringe beam, songket Deli tile.
Run: python3 -I istana-maimun.py [part ...]   parts: istana arch lebah songket divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c2_lib import *

OUT = outdir("istana-maimun")
PARTS = sys.argv[1:] or ["istana", "arch", "lebah", "songket", "divider"]
YEL, YEL_D, YEL_L = "#e6b62a", "#c08a17", "#f6dc7c"
CREAM = "#fbf1d2"
GOLD, GOLD_L = "#c99a3c", "#f0d48a"
GREEN, GREEN_D = "#2d5a46", "#173528"
BROWN = "#4a2a12"
WHITE = "#fbf6e8"


def ogee(cx, base, w, h, n=40, kind="ogee"):
    """Arch outline points (left jamb up, arch, right jamb down) as an open polygon for filling (closed at base)."""
    pts = [(cx - w / 2, base)]
    spring = base - h * 0.55
    pts.append((cx - w / 2, spring))
    for i in range(1, n):
        t = i / n
        if kind == "ogee":
            # rises, swells, and flips into a point at the top (keel arch)
            x = cx - w / 2 + w / 2 * t
            y = spring - h * 0.45 * (math.sin(t * math.pi / 2) ** 0.8 * 0.85 + 0.15 * max(0, (t - 0.7) / 0.3) ** 2)
            x += -math.sin(t * math.pi) * w * 0.05
        else:  # horseshoe-ish pointed
            a = math.pi + t * math.pi / 2
            x = cx + math.cos(a) * w / 2 * (1 + 0.08 * math.sin(t * math.pi))
            y = spring + math.sin(a) * h * 0.45
        pts.append((x, y))
    pts.append((cx, spring - h * 0.45))
    right = [(2 * cx - x, y) for x, y in pts[::-1]]
    return pts + right[1:]


def pucuk(x0, x1, y, h, n):
    """Row of pucuk rebung (bamboo-shoot triangles) as polygons + inner line items."""
    polys, lines = [], []
    w = (x1 - x0) / n
    for k in range(n):
        a = x0 + k * w
        polys.append([(a, y), (a + w / 2, y - h), (a + w, y)])
        lines.append(([(a + w * 0.25, y - 2), (a + w / 2, y - h * 0.55), (a + w * 0.75, y - 2)], max(1.2, w * 0.06)))
    return polys, lines


def lebah(x0, x1, y, L, n):
    """lebah bergantung: hanging drop pendants under a beam."""
    out = []
    w = (x1 - x0) / n
    for k in range(n):
        cx = x0 + w * (k + 0.5)
        out.append([(cx - w * 0.32, y), (cx + w * 0.32, y), (cx + w * 0.2, y + L * 0.45), (cx, y + L), (cx - w * 0.2, y + L * 0.45)])
    return out


if "istana" in PARTS:
    W, H = 960, 520
    nx = Seq(50100); rnd = random.Random(4)
    art = blank(W, H)
    cx = W / 2
    base = 470
    gp = lambda art, m, c1, c2=None, **k: GP(art, m, c1, c2, seed=nx(), rough=1.2, streak=0.8, **k)
    # ground shadow
    art = G(art, poly(W, H, deform(ellipse_pts(cx, base + 18, 470, 20, 18), rnd, 1, 0.02)), "#7a5a2a", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=4, feather=6)
    # wings (long arcades)
    for sg in (-1, 1):
        x0 = cx + sg * 120; x1 = cx + sg * 450
        wing = poly(W, H, [(min(x0, x1), base), (min(x0, x1), base - 150), (max(x0, x1), base - 150), (max(x0, x1), base)], smooth=False)
        art = gp(art, wing, YEL, YEL_D)
        # parapet with small finials
        par = poly(W, H, [(min(x0, x1) - 6, base - 150), (max(x0, x1) + 6, base - 150), (max(x0, x1) + 6, base - 166), (min(x0, x1) - 6, base - 166)], smooth=False)
        art = gp(art, par, WHITE, CREAM)
        art = FO(art, np.clip(np.clip(gaussian_filter(par, 1.0) * 2.6, 0, 1) - par, 0, 1), GOLD, seed=nx(), emboss=0.3)
        art = G(art, np.clip(par - np.roll(par, -3, 0), 0, 1), "#a88a5a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
        fin = shapes(W, H, [petal_pts(x, base - 160, 24, 6, -math.pi / 2, n=8) for x in range(int(min(x0, x1)) + 10, int(max(x0, x1)), 36)])
        art = FO(art, fin, GOLD, seed=nx(), emboss=0.6)
        # two storeys of arches
        for row, (yb, ah, aw) in enumerate([(base, 92, 40), (base - 98, 44, 30)]):
            n = 6
            xs = [min(x0, x1) + (abs(x1 - x0)) * (k + 0.5) / n for k in range(n)]
            arches = [ogee(x, yb - 4, aw, ah, kind="ogee" if row == 0 else "horse") for x in xs]
            am = shapes(W, H, arches, smooth=False)
            art = gp(art, am, "#2a1c10", "#3c2814")
            art = G(art, am * (np.mgrid[0:H, 0:W][0] > yb - ah * 0.35), "#7a4e22", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
            art = FO(art, np.clip(np.clip(gaussian_filter(am, 1.8) * 2.6, 0, 1) - am, 0, 1), GOLD, seed=nx(), emboss=0.5)
            if row == 0:
                # columns
                cols = shapes(W, H, [[(x - aw / 2 - 9, yb), (x - aw / 2 - 9, yb - ah * 0.6), (x - aw / 2 - 3, yb - ah * 0.6), (x - aw / 2 - 3, yb)] for x in xs], smooth=False)
                art = gp(art, cols, WHITE, CREAM)
        # string course band (green)
        band = poly(W, H, [(min(x0, x1), base - 100), (max(x0, x1), base - 100), (max(x0, x1), base - 106), (min(x0, x1), base - 106)], smooth=False)
        art = gp(art, band, GREEN, GREEN_D)
        # end tower with small dome
        tx = x1 - sg * 18
        tower = poly(W, H, [(tx - 26, base), (tx - 26, base - 200), (tx + 26, base - 200), (tx + 26, base)], smooth=False)
        art = gp(art, tower, YEL_L, YEL)
        art = gp(art, shapes(W, H, [ogee(tx, base - 120, 22, 60, kind="horse")], smooth=False), "#2a1c10")
        dome = shapes(W, H, [[(tx - 28, base - 200)] + [(tx + math.cos(a) * 28, base - 200 - math.sin(a) * 34 * (1 + 0.25 * math.sin(a * 2))) for a in np.linspace(math.pi, 0, 24)] + [(tx + 28, base - 200)]])
        art = gp(art, dome, GREEN, GREEN_D)
        art = G(art, dome * (np.mgrid[0:H, 0:W][1] < tx - 6), "#4f8a6c", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=1)
        art = FO(art, shapes(W, H, [petal_pts(tx, base - 236, 26, 6, -math.pi / 2, n=8)]) + circles(W, H, [(tx, base - 238, 5)]), GOLD, seed=nx())
    # central pavilion: taller, projecting, big keel arch, grand dome
    pav = poly(W, H, [(cx - 130, base), (cx - 130, base - 230), (cx + 130, base - 230), (cx + 130, base)], smooth=False)
    art = gp(art, pav, YEL_L, YEL)
    sh = poly(W, H, [(cx + 60, base), (cx + 60, base - 230), (cx + 130, base - 230), (cx + 130, base)], smooth=False)
    art = G(art, sh, YEL_D, seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=4)
    big = ogee(cx, base - 2, 120, 190, kind="ogee")
    bm_ = shapes(W, H, [big], smooth=False)
    art = gp(art, bm_, "#2a1c10", "#46301a")
    frame = np.clip(np.clip(gaussian_filter(bm_, 5) * 2.6, 0, 1) - bm_, 0, 1)
    art = FO(art, frame, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    # carved double doors inside the keel arch, gilt panels
    inner = shapes(W, H, [ogee(cx, base - 2, 92, 150, kind="ogee")], smooth=False)
    art = gp(art, inner, "#6a3c18", "#4a2a12")
    art = FO(art, np.clip(np.clip(gaussian_filter(inner, 1.6) * 2.6, 0, 1) - inner, 0, 1), GOLD_L, seed=nx(), emboss=0.5)
    art = G(art, strokes(W, H, [([(cx, base - 2), (cx, base - 128)], 2.0, None)]), "#2a1508", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
    pan = []
    for sg in (-1, 1):
        for (y0, y1) in [(base - 120, base - 76), (base - 66, base - 14)]:
            pan.append([(cx + sg * 8, y0), (cx + sg * 38, y0), (cx + sg * 38, y1), (cx + sg * 8, y1)])
    pm_ = shapes(W, H, pan, smooth=False)
    art = FO(art, np.clip(np.clip(gaussian_filter(pm_, 1.2) * 2.6, 0, 1) - np.clip((gaussian_filter(pm_, 1.2) - 0.6) * 4, 0, 1), 0, 1), GOLD, seed=nx(), emboss=0.5)
    pp2, pl2 = pucuk(cx - 36, cx + 36, base - 14, 30, 4)
    art = FO(art, np.maximum(shapes(W, H, [[(x, y) for x, y in p] for p in pp2], smooth=False) * 0.0 + strokes(W, H, [(p + [p[0]], 1.6, None) for p in pp2]), strokes(W, H, pl2)), GOLD, seed=nx(), emboss=0.5)
    # pucuk rebung band across the pavilion + lebah bergantung under the cornice
    pp, pl = pucuk(cx - 128, cx + 128, base - 206, 20, 12)
    art = gp(art, shapes(W, H, pp, smooth=False), GREEN, GREEN_D)
    art = FO(art, strokes(W, H, pl), GOLD_L, seed=nx())
    corn = poly(W, H, [(cx - 140, base - 230), (cx + 140, base - 230), (cx + 140, base - 244), (cx - 140, base - 244)], smooth=False)
    art = gp(art, corn, WHITE, CREAM)
    art = FO(art, shapes(W, H, lebah(cx - 138, cx + 138, base - 230, 14, 20)), GOLD, seed=nx(), emboss=0.6)
    # side windows on pavilion
    for sg in (-1, 1):
        w_ = shapes(W, H, [ogee(cx + sg * 96, base - 70, 30, 80, kind="horse"), ogee(cx + sg * 96, base - 150, 26, 50, kind="horse")], smooth=False)
        art = gp(art, w_, "#2a1c10")
        art = FO(art, np.clip(np.clip(gaussian_filter(w_, 1.8) * 2.6, 0, 1) - w_, 0, 1), GOLD, seed=nx(), emboss=0.5)
    # grand dome on a drum
    drum = poly(W, H, [(cx - 70, base - 244), (cx - 70, base - 280), (cx + 70, base - 280), (cx + 70, base - 244)], smooth=False)
    art = gp(art, drum, YEL, YEL_D)
    art = gp(art, shapes(W, H, [ogee(cx + k * 30, base - 248, 12, 28, kind="horse") for k in (-1.5, -0.5, 0.5, 1.5)], smooth=False), "#2a1c10")
    dome = shapes(W, H, [[(cx - 78, base - 280)] + [(cx + math.cos(a) * 78 * (1 + 0.12 * math.sin(a)), base - 280 - math.sin(a) * 96 - max(0, math.sin(a) - 0.9) * 180) for a in np.linspace(math.pi, 0, 40)] + [(cx + 78, base - 280)]])
    art = gp(art, dome, GREEN, GREEN_D)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, dome * (xx < cx - 20) * np.clip((cx - 20 - xx) / 40, 0, 1), "#5e9a7a", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    ribs = strokes(W, H, [(curve([(cx + k * 22, base - 282), (cx + k * 18, base - 330), (cx, base - 378)], 20), 2.0, None) for k in (-3, -2, -1, 0, 1, 2, 3)]) * dome
    art = FO(art, ribs, GOLD, seed=nx(), emboss=0.4)
    art = FO(art, np.maximum(shapes(W, H, [petal_pts(cx, base - 378, 48, 9, -math.pi / 2, n=10)]), circles(W, H, [(cx, base - 392, 8), (cx, base - 410, 4.5)])), GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    # steps
    for k in range(4):
        st = poly(W, H, [(cx - 90 - k * 14, base + k * 6), (cx + 90 + k * 14, base + k * 6), (cx + 90 + k * 14, base + k * 6 + 6), (cx - 90 - k * 14, base + k * 6 + 6)], smooth=False)
        art = gp(art, st, WHITE if k % 2 == 0 else CREAM, "#e7dcc0")
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "im-istana", tone=CREAM)
    save(art, f"{OUT}/istana.webp", max_w=720, quality=82)
    clear()

import _jw_lib as jw


def ring_between(W, H, outer, inner):
    return np.clip(shapes(W, H, [outer], smooth=False) - shapes(W, H, [inner], smooth=False), 0, 1)


if "arch" in PARTS:
    # gilt carved keel-arch frame (transparent opening) for the cover photo
    W, H = 620, 820
    nx = Seq(50200)
    cx = W / 2; base = 800
    outer = ogee(cx, base, 560, 700, n=60)
    inner = ogee(cx, base, 448, 600, n=60)
    mid = ogee(cx, base, 504, 650, n=60)
    band = ring_between(W, H, outer, inner)
    art = GP(blank(W, H), band, "#d39a1a", "#b67c10", seed=nx(), rough=0.8, streak=0.9, pad=10)
    items, leaves = [], []
    path = curve(mid, 240)
    for k, (x, y, a) in enumerate(jw.along(path, 50)):
        it, lv = jw.lung(x, y, 27, a, 1 if k % 2 else -1); items += it; leaves += lv
    relief0 = np.maximum(strokes(W, H, items), shapes(W, H, leaves)) * band
    art = G(art, np.clip(gaussian_filter(relief0, 2.2) * 1.4 - relief0, 0, 1) * band, "#7a4a0a", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1, feather=0.8)
    relief = np.maximum(strokes(W, H, items), shapes(W, H, leaves)) * band
    art = FO(art, relief, GOLD, seed=nx(), emboss=0.8, sparkle=0.14)
    # mouldings: outer & inner gilt beads
    mo = strokes(W, H, [(outer[1:-1], 6, None), (inner[1:-1], 5, None)])
    art = FO(art, mo, GOLD_L, seed=nx(), emboss=0.7)
    art = GP(art, strokes(W, H, [(ogee(cx, base, 460, 612, n=60)[1:-1], 3, None)]), GREEN, GREEN_D, seed=nx(), rough=0.3, pad=4)
    beads = circles(W, H, [(x + math.cos(a + math.pi / 2) * 0, y, 3.2) for (x, y, a) in jw.along(curve(ogee(cx, base, 430, 584, n=60)[1:-1], 200), 12)])
    art = FO(art, beads, GOLD_L, seed=nx(), emboss=0.8)
    # crown: pucuk rebung crest + finial above the keel point
    top_y = min(p[1] for p in outer)
    crest = []
    for k, (dx, h_) in enumerate([(0, 90), (-46, 56), (46, 56), (-84, 34), (84, 34)]):
        crest.append([(cx + dx - h_ * 0.42, top_y + 26), (cx + dx, top_y + 26 - h_), (cx + dx + h_ * 0.42, top_y + 26)])
    cm = shapes(W, H, crest, smooth=False)
    art = GP(art, cm, "#d39a1a", "#b67c10", seed=nx(), rough=0.6, pad=8)
    art = FO(art, np.clip(np.clip(gaussian_filter(cm, 1.4) * 2.6, 0, 1) - np.clip((gaussian_filter(cm, 1.4) - 0.7) * 5, 0, 1), 0, 1), GOLD_L, seed=nx(), emboss=0.6)
    art = FO(art, strokes(W, H, [([(cx + dx - h_ * 0.2, top_y + 22), (cx + dx, top_y + 26 - h_ * 0.6), (cx + dx + h_ * 0.2, top_y + 22)], 2.0, None) for dx, h_ in [(0, 90), (-46, 56), (46, 56), (-84, 34), (84, 34)]]), GOLD, seed=nx())
    # lebah bergantung hanging inside the springing line
    spring_y = base - 600 * 0.55
    for sg in (-1, 1):
        x0 = cx + sg * 224
        drops = lebah(x0 - 0.0001 if sg < 0 else x0 - 40, x0 + 40 if sg < 0 else x0, spring_y, 26, 3)
        art = FO(art, shapes(W, H, drops), GOLD, seed=nx(), emboss=0.7)
    art = drop_shadow(art, blur=5, dy=4, strength=0.4)
    preview(art, "im-arch", tone=CREAM)
    save(art, f"{OUT}/arch.webp", max_w=360, quality=84)
    clear()

if "lebah" in PARTS:
    # carved fringe beam: gilt pucuk rebung beam with lebah bergantung pendants (repeat-x)
    W, H = 480, 110
    nx = Seq(50300)
    beam = poly(W, H, [(0, 0), (W, 0), (W, 46), (0, 46)], smooth=False)
    art = GP(blank(W, H), beam, YEL_D, "#a87412", seed=nx(), rough=0.0, streak=0.8, pad=0)
    pp, pl = pucuk(0, W, 42, 30, 12)
    art = FO(art, np.clip(strokes(W, H, [(p + [p[0]], 2.2, None) for p in pp]) + strokes(W, H, pl), 0, 1), GOLD_L, seed=nx(), emboss=0.7)
    art = FO(art, strokes(W, H, [([(0, 4), (W, 4)], 3, None), ([(0, 44), (W, 44)], 4, None)]), GOLD_L, seed=nx(), emboss=0.6)
    drops = shapes(W, H, lebah(0, W, 46, 52, 12))
    art = GP(art, drops, YEL, YEL_D, seed=nx(), rough=0.6, pad=6)
    art = FO(art, np.clip(np.clip(gaussian_filter(drops, 1.2) * 2.6, 0, 1) - np.clip((gaussian_filter(drops, 1.2) - 0.7) * 5, 0, 1), 0, 1), GOLD, seed=nx(), emboss=0.6)
    art = FO(art, circles(W, H, [(20 + k * 40, 92, 4) for k in range(12)]), GOLD_L, seed=nx(), emboss=0.8)
    preview(art, "im-lebah", tone=CREAM)
    save_full(art, f"{OUT}/lebah.webp", size=(240, 55), quality=84)
    clear()

if "songket" in PARTS:
    # songket Deli: royal-yellow silk ground with gold weft floats forming pucuk rebung rows + bunga tabur (tileable)
    S = 240
    nx = Seq(50400)
    art = silk(S, S, "#c98e12", "#b07a0c", seed=nx(), pitch=2.0, drape=0.4, bands=1)
    def draw(cv):
        p = paint_white()
        # pucuk rebung band at top and bottom of the tile
        for y0, up in ((0, -1), (S, 1)):
            for k in range(6):
                x = k * 40
                path = skia.Path(); path.moveTo(x, y0); path.lineTo(x + 20, y0 - up * 52); path.lineTo(x + 40, y0); path.close()
                cv.c.drawPath(path, p)
        # bunga tabur: small 8-point stars in the field
        for (x, y) in [(60, 120), (180, 120), (0, 120), (120, 120)]:
            r = 16 if (x // 60) % 2 == 0 else 9
            path = skia.Path()
            for j in range(16):
                a = j / 16 * math.tau; rr = r if j % 2 == 0 else r * 0.45
                (path.moveTo if j == 0 else path.lineTo)(x + math.cos(a) * rr, y + math.sin(a) * rr)
            path.close(); cv.c.drawPath(path, p)
    gm = tile_mask(S, S, draw)
    # cut a lozenge inside each pucuk so the ground shows (two-tone weave)
    def draw2(cv):
        p = paint_white()
        for y0, up in ((0, -1), (S, 1)):
            for k in range(6):
                x = k * 40
                path = skia.Path(); path.moveTo(x + 13, y0 - up * 6); path.lineTo(x + 20, y0 - up * 34); path.lineTo(x + 27, y0 - up * 6); path.close()
                cv.c.drawPath(path, p)
    gm = np.clip(gm - tile_mask(S, S, draw2), 0, 1)
    art = over(art, lame(gm, "#f2d27a", seed=nx(), pitch=2.4, bind=7, deep="#9a6a1c"))
    save_full(art, f"{OUT}/songket.webp", quality=78)
    preview(art, "im-songket", tone=CREAM)
    clear()

if "divider" in PARTS:
    W, H = 560, 90
    nx = Seq(50500)
    cx = W / 2
    pp, pl = pucuk(cx - 30, cx + 30, 66, 50, 1)
    items = [(curve([(cx - 40, 58), (cx - 140, 50), (cx - 250, 60)], 30), 3.0), (curve([(cx + 40, 58), (cx + 140, 50), (cx + 250, 60)], 30), 3.0)]
    lv = []
    for sg in (-1, 1):
        for k, (x, y, a) in enumerate(jw.along(curve([(cx + sg * 50, 58), (cx + sg * 140, 50), (cx + sg * 240, 60)], 30), 46)):
            it, l_ = jw.lung(x, y, 22, a if sg > 0 else a + math.pi, 1 if k % 2 else -1); items += it; lv += l_
    m = np.maximum.reduce([strokes(W, H, items), shapes(W, H, lv), shapes(W, H, pp, smooth=False)])
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.7, sparkle=0.14)
    art = GP(art, shapes(W, H, [[(cx - 10, 62), (cx, 36), (cx + 10, 62)]], smooth=False), GREEN, GREEN_D, seed=nx(), rough=0.4, pad=4)
    preview(art, "im-divider", tone=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)
