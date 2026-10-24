"""Dallah Kopi — Arabian coffee hospitality in gouache with polished-brass shading: a tall brass dallah with a beak
spout and spire lid, porcelain finjan cups of golden qahwa, a round brass tray of dates, majlis cushions and the edge
of a red-indigo carpet. No figures, no calligraphy.
Run: python3 -I dallah-kopi.py [part ...]  parts: still dallah finjan date carpet ring divider
Assets -> public/themes/art/dallah-kopi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t2_lib import *

OUT = outdir("dallah-kopi")
PARTS = sys.argv[1:] or ["still", "dallah", "finjan", "date", "carpet", "ring", "divider"]
INK = "#2b1810"
BR, BR_L, BR_D, BR_H = "#c4943e", "#e2bd6a", "#6e4a1a", "#fff1c4"
SAF = "#e3a72f"
RED, RED_D, RED_L = "#9e2f24", "#6a1c16", "#c24a36"
IND, IND_D = "#26345e", "#161f3c"
CRM, CRM_D = "#f3e6cc", "#cdb894"
GRN = "#7d8a4a"
DATE, DATE_D, DATE_L = "#6b3015", "#3e1a0b", "#a2552a"
QAHWA, QAHWA_D = "#c8962e", "#8a5e18"


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def lathe(W, H, cx, top, prof, smooth=True):
    """Solid of revolution silhouette: prof = [(t, halfwidth)] down from `top` (t in px)."""
    L = [(cx - w, top + t) for t, w in prof]
    R = [(cx + w, top + t) for t, w in prof][::-1]
    return shapes(W, H, [L + R], smooth=smooth)


def dallah(art, W, H, cx, base, h, nx):
    """Brass dallah standing at (cx, base) with total height h."""
    k = h / 360.0
    top = base - h
    prof = [(0, 2), (14, 5), (22, 9), (30, 5), (40, 7), (52, 14), (64, 26), (72, 30), (80, 26), (92, 30),
            (104, 36), (122, 40), (150, 34), (172, 26), (186, 24), (200, 30), (226, 52), (256, 74), (290, 86),
            (318, 84), (336, 72), (344, 60), (350, 66), (360, 62)]
    prof = [(t * k, w * k) for t, w in prof]
    bodym = lathe(W, H, cx, top, prof)
    # spout: from the belly up to a beak
    sp = curve([(cx + 52 * k, top + 250 * k), (cx + 96 * k, top + 220 * k), (cx + 118 * k, top + 160 * k), (cx + 132 * k, top + 112 * k), (cx + 150 * k, top + 96 * k)], 40)
    spout = strokes(W, H, [(sp, 22 * k, (0.0, 0.35))])
    beak = poly(W, H, [(cx + 128 * k, top + 112 * k), (cx + 146 * k, top + 88 * k), (cx + 184 * k, top + 86 * k), (cx + 160 * k, top + 104 * k), (cx + 144 * k, top + 118 * k)], smooth=True)
    spout = np.clip(spout + beak, 0, 1)
    # handle: C-curve on the left with a thumb rest
    hd = curve([(cx - 28 * k, top + 104 * k), (cx - 78 * k, top + 112 * k), (cx - 104 * k, top + 170 * k), (cx - 96 * k, top + 232 * k), (cx - 66 * k, top + 266 * k)], 40)
    handle = strokes(W, H, [(hd, 12 * k, (0.05, 0.1))])
    thumb = strokes(W, H, [([(cx - 30 * k, top + 98 * k), (cx - 52 * k, top + 86 * k)], 9 * k, None)])
    back = np.clip(handle + thumb, 0, 1) * (1 - bodym)
    art = metal(art, back, BR, BR_H, BR_D, nx, amt=0.6)
    art = crayon(art, inner_edge(back, 1.4), BR_D, seed=nx(), amt=0.6)
    art = metal(art, spout, BR, BR_H, BR_D, nx, amt=0.55)
    art = crayon(art, inner_edge(spout, 1.4), BR_D, seed=nx(), amt=0.6)
    art = metal(art, bodym, BR, BR_H, BR_D, nx, amt=0.8)
    # engraved rings, bands, dotted chasing
    rings = []
    for t in (30, 52, 72, 92, 104, 172, 200, 226, 318, 344):
        tt = t * k
        w = np.interp(tt, [p[0] for p in prof], [p[1] for p in prof])
        rings.append((curve([(cx - w + 1, top + tt), (cx, top + tt + 3 * k), (cx + w - 1, top + tt)], 12), 2.0 * k, None))
    rm = strokes(W, H, rings) * bodym
    art = tint(art, rm, BR_D, 0.75, seed=nx(), streak=0.2)
    dots = []
    for t in range(232, 312, 9):
        tt = t * k
        w = np.interp(tt, [p[0] for p in prof], [p[1] for p in prof])
        for u in np.linspace(-0.75, 0.75, 9):
            if (t // 9) % 2 == 0 or abs(u) < 0.6:
                dots.append((cx + u * w, top + tt + (1 - u * u) * 4 * k, 1.5 * k))
    dm = circles(W, H, dots) * bodym
    art = tint(art, dm, BR_D, 0.6, seed=nx(), streak=0.2)
    # small turquoise inlay stone on the belly band
    art = body(art, circles(W, H, [(cx, top + 210 * k, 6 * k)]), "#3e9a8e", "#5ab8a8", "#1f5e56", "#9fe0d4", nx, blur=1.5)
    art = crayon(art, inner_edge(bodym, 1.6), BR_D, seed=nx(), amt=0.65)
    return art, np.clip(bodym + spout + back, 0, 1)


def finjan(art, W, H, cx, base, s, nx, steam=False):
    """Handleless porcelain cup with golden qahwa; s = cup height."""
    rt, rb = s * 0.62, s * 0.36
    cup = poly(W, H, [(cx - rt, base - s), (cx + rt, base - s), (cx + rb * 1.05, base - s * 0.12), (cx + rb * 0.7, base), (cx - rb * 0.7, base), (cx - rb * 1.05, base - s * 0.12)], smooth=False)
    cup = gaussian_filter(cup, 0.8)
    bot = shapes(W, H, [ellipse_pts(cx, base - s * 0.06, rb, s * 0.1, 16)])
    cup = np.clip(cup + bot, 0, 1)
    art = body(art, cup, "#fbf6ec", "#ffffff", "#c9bfae", "#ffffff", nx, ldir=(-s * 0.18, 0), blur=s * 0.14, rough=0.6)
    band = poly(W, H, [(cx - rt * 0.94, base - s * 0.78), (cx + rt * 0.94, base - s * 0.78), (cx + rt * 0.86, base - s * 0.62), (cx - rt * 0.86, base - s * 0.62)])
    art = GP(art, band * cup, GRN, "#6b7a3c", seed=nx(), rough=0.4, pad=4)
    gb = strokes(W, H, [([(cx - rt * 0.95, base - s * 0.8), (cx + rt * 0.95, base - s * 0.8)], max(1.2, s * 0.04), None),
                        ([(cx - rt * 0.85, base - s * 0.6), (cx + rt * 0.85, base - s * 0.6)], max(1.2, s * 0.04), None)]) * cup
    art = FO(art, gb, BR, seed=nx(), emboss=0.3, sparkle=0.05)
    lip = shapes(W, H, [ellipse_pts(cx, base - s, rt, s * 0.16, 24)])
    art = body(art, lip, "#fbf6ec", "#ffffff", "#c9bfae", "#ffffff", nx, blur=1.5, rough=0.4)
    q = shapes(W, H, [ellipse_pts(cx, base - s + s * 0.02, rt * 0.86, s * 0.11, 24)])
    art = GP(art, q, QAHWA, QAHWA_D, seed=nx(), rough=0.3, pad=4)
    art = tint(art, side_light(q, s * 0.1, s * 0.05, 2), "#f6d77e", 0.5, seed=nx())
    rimg = strokes(W, H, [(arc_pts(cx, base - s, rt, 0, math.tau, 40, s * 0.16 / rt), max(1.0, s * 0.03), None)])
    art = FO(art, rimg, BR, seed=nx(), emboss=0.2, sparkle=0.05)
    art = crayon(art, inner_edge(np.clip(cup + lip, 0, 1), 1.2), "#8c7a62", seed=nx(), amt=0.45)
    return art, np.clip(cup + lip, 0, 1)


def date_fruit(art, W, H, x, y, L, ang, nx, rng):
    m = shapes(W, H, [deform(ellipse_pts(x, y, L, L * 0.4, 16, ang), rng, 1, 0.015)])
    art = body(art, m, DATE, "#7c3a19", DATE_D, DATE_L, nx, ldir=(L * 0.25, L * 0.3), blur=L * 0.25, rough=0.5)
    wr = []
    for j in range(2):
        o = (j - 0.5) * L * 0.36
        ca, sa = math.cos(ang), math.sin(ang)
        p0 = (x - ca * L * 0.6 - sa * o, y - sa * L * 0.6 + ca * o)
        p1 = (x + ca * L * 0.5 - sa * o * 1.2, y + sa * L * 0.5 + ca * o * 1.2)
        wr.append((curve([p0, ((p0[0] + p1[0]) / 2 + rng.uniform(-2, 2), (p0[1] + p1[1]) / 2 + rng.uniform(-2, 2)), p1], 10), max(0.8, L * 0.05), None))
    art = tint(art, strokes(W, H, wr) * m, DATE_D, 0.55, seed=nx(), streak=0.2)
    hl = strokes(W, H, [(curve([(x - math.cos(ang) * L * 0.4 - math.sin(ang) * L * 0.18, y - math.sin(ang) * L * 0.4 - L * 0.18),
                                (x + math.cos(ang) * L * 0.2 - math.sin(ang) * L * 0.24, y + math.sin(ang) * L * 0.2 - L * 0.24)], 8), L * 0.12, None)]) * m
    art = tint(art, gaussian_filter(hl, 1), "#e9b58a", 0.5, seed=nx(), streak=0.2)
    return art, m


def tray(art, W, H, cx, cy, rx, ry, nx):
    plate = shapes(W, H, [ellipse_pts(cx, cy, rx, ry, 40)])
    art = metal(art, plate, BR, BR_H, BR_D, nx, amt=0.55)
    inner = shapes(W, H, [ellipse_pts(cx, cy - ry * 0.06, rx * 0.84, ry * 0.76, 40)])
    art = tint(art, inner, BR_D, 0.35, seed=nx())
    eng = strokes(W, H, [(arc_pts(cx, cy - ry * 0.06, rx * 0.84, 0, math.tau, 60, ry * 0.76 / (rx * 0.84)), 1.6, None),
                         (arc_pts(cx, cy - ry * 0.06, rx * 0.74, 0, math.tau, 60, ry * 0.66 / (rx * 0.74)), 1.2, None)])
    art = tint(art, eng, BR_D, 0.7, seed=nx(), streak=0.2)
    hi = strokes(W, H, [(arc_pts(cx, cy, rx * 0.97, math.pi * 1.1, math.pi * 1.5, 20, ry / rx), 3, None)])
    art = tint(art, hi, BR_H, 0.7, seed=nx(), streak=0.2)
    art = crayon(art, inner_edge(plate, 1.4), BR_D, seed=nx(), amt=0.6)
    return art, plate


if "still" in PARTS:
    W, H = 820, 600
    nx = Seq(81000); rng = random.Random(8)
    art = blank(W, H)
    # majlis cushions behind (left & right), red with indigo/cream stripes
    for x0, x1, y0 in ((-20, 300, 250), (560, 840, 270)):
        cm = shapes(W, H, [deform([(x0, y0 + 30), (x0 + 20, y0), (x1 - 20, y0 + 6), (x1, y0 + 34), (x1, 500), (x0, 500)], rng, 2, 0.01)])
        art = body(art, cm, RED, RED_L, RED_D, RED_L, nx, ldir=(0, -14), blur=14)
        stripes = []
        for j, (yy, col) in enumerate(((y0 + 46, IND), (y0 + 60, CRM), (y0 + 74, IND), (y0 + 150, SAF), (y0 + 164, IND))):
            stripes.append((yy, col))
        for yy, col in stripes:
            st = poly(W, H, [(x0, yy), (x1, yy + 2), (x1, yy + 10), (x0, yy + 8)]) * cm
            art = GP(art, st, col, seed=nx(), rough=0.5, pad=4)
        # small diamond row
        dia = shapes(W, H, [[(xx, y0 + 112), (xx + 9, y0 + 102), (xx + 18, y0 + 112), (xx + 9, y0 + 122)] for xx in range(x0 + 10, x1, 30)], smooth=False) * cm
        art = GP(art, dia, CRM, CRM_D, seed=nx(), rough=0.4, pad=4)
        art = tint(art, side_light(cm, 0, -18, 16), RED_D, 0.45, seed=nx())
    # carpet floor (front band with border pattern + fringe)
    floor = poly(W, H, [(0, 470), (W, 470), (W, 600), (0, 600)])
    art = body(art, floor, RED, RED_L, RED_D, RED_L, nx, ldir=(0, -10), blur=12)
    brd = poly(W, H, [(0, 540), (W, 540), (W, 572), (0, 572)])
    art = GP(art, brd, IND, IND_D, seed=nx(), rough=0.4)
    mot = shapes(W, H, [[(x, 556), (x + 14, 544), (x + 28, 556), (x + 14, 568)] for x in range(-10, W, 40)], smooth=False)
    art = GP(art, mot, CRM, CRM_D, seed=nx(), rough=0.4, pad=4)
    art = GP(art, circles(W, H, [(x + 14, 556, 3.4) for x in range(-10, W, 40)]), RED, seed=nx(), rough=0.2, pad=4)
    lines = strokes(W, H, [([(0, 486), (W, 486)], 3, None), ([(0, 532), (W, 532)], 3, None), ([(0, 578), (W, 578)], 3, None)])
    art = GP(art, lines, SAF, seed=nx(), rough=0.4, pad=4)
    small = shapes(W, H, [[(x, 509), (x + 8, 500), (x + 16, 509), (x + 8, 518)] for x in range(6, W, 24)], smooth=False)
    art = GP(art, small, SAF, "#c98a1e", seed=nx(), rough=0.3, pad=4)
    art = tint(art, poly(W, H, [(0, 470), (W, 470), (W, 500), (0, 500)]), RED_D, 0.35, seed=nx())
    # tray with dates (left-centre)
    art = G(art, shapes(W, H, [ellipse_pts(300, 512, 200, 26, 30)]), "#3a120c", seed=nx(), density=0.45, edge=0.05, bloom=0, rough=3, feather=7)
    art, plate = tray(art, W, H, 296, 492, 190, 46, nx)
    pile = []
    for row, (yy, n, sp) in enumerate(((488, 9, 30), (472, 7, 30), (458, 5, 30), (446, 3, 28))):
        for j in range(n):
            pile.append((296 - (n - 1) * sp / 2 + j * sp + rng.uniform(-4, 4), yy + rng.uniform(-3, 3), rng.uniform(15, 18), rng.uniform(-0.5, 0.5)))
    for x, y, L, a in pile:
        art, _ = date_fruit(art, W, H, x, y, L, a, nx, rng)
    # dallah (right)
    art = G(art, shapes(W, H, [ellipse_pts(574, 528, 80, 12, 24)]), "#3a120c", seed=nx(), density=0.5, edge=0.05, bloom=0, rough=3, feather=6)
    art, _ = dallah(art, W, H, 560, 526, 400, nx)
    clear()
    # finjan cups in front
    for x, y, s_ in ((132, 566, 62), (700, 574, 66), (446, 580, 56)):
        art = G(art, shapes(W, H, [ellipse_pts(x + 4, y + 2, s_ * 0.5, 6, 16)]), "#3a120c", seed=nx(), density=0.45, edge=0.05, bloom=0, rough=2, feather=4)
        art, _ = finjan(art, W, H, x, y, s_, nx)
    # cardamom pods scattered
    for x, y in ((236, 586), (520, 588), (560, 576), (770, 590), (90, 590)):
        pod = shapes(W, H, [ellipse_pts(x, y, 8, 4.5, 12, rng.uniform(0, 3))])
        art = body(art, pod, "#8a9a52", "#a3b366", "#5c6a34", "#c6d38a", nx, blur=1.5, rough=0.4)
    art = add_grain(art, nx(), 0.04)
    preview(art, "dk-still", bg="#2a1810")
    save(art, f"{OUT}/still.webp", max_w=820, quality=80)
    clear()

if "dallah" in PARTS:
    W, H = 340, 460
    nx = Seq(82000)
    art = blank(W, H)
    art, _ = dallah(art, W, H, 150, 440, 420, nx)
    art = add_grain(art, nx(), 0.03)
    preview(art, "dk-dallah", tone="#f5ead7")
    save(art, f"{OUT}/dallah.webp", max_w=260, quality=84)
    clear()

if "finjan" in PARTS:
    W, H = 160, 130
    nx = Seq(83000)
    art = blank(W, H)
    art, _ = finjan(art, W, H, 80, 118, 90, nx)
    preview(art, "dk-finjan", tone="#f5ead7")
    save(art, f"{OUT}/finjan.webp", max_w=120, quality=84)
    clear()

if "date" in PARTS:
    W, H = 90, 70
    nx = Seq(84000); rng = random.Random(2)
    art = blank(W, H)
    art, _ = date_fruit(art, W, H, 45, 35, 34, -0.35, nx, rng)
    preview(art, "dk-date", tone="#f5ead7")
    save(art, f"{OUT}/date.webp", max_w=60, quality=84)
    clear()

if "carpet" in PARTS:
    # Seamless horizontal carpet border (repeat-x): red ground, indigo band, cream lozenges, saffron lines, fringe.
    W, H = 480, 64
    nx = Seq(85000)
    art = blank(W, H)
    def rep(fn):
        out = []
        for ox in (-W, 0, W):
            out += fn(ox)
        return out
    ground = np.ones((H, W), np.float32)
    art = GP(art, ground, RED, "#a8382b", seed=nx(), rough=0.1, streak=0.8)
    band = np.zeros((H, W), np.float32); band[16:48] = 1
    art = GP(art, band, IND, IND_D, seed=nx(), rough=0.0)
    loz = shapes(W, H, rep(lambda ox: [[(ox + x, 32), (ox + x + 20, 18), (ox + x + 40, 32), (ox + x + 20, 46)] for x in range(0, W, 60)]), smooth=False)
    art = GP(art, loz, CRM, CRM_D, seed=nx(), rough=0.3)
    inn = shapes(W, H, rep(lambda ox: [[(ox + x + 10, 32), (ox + x + 20, 25), (ox + x + 30, 32), (ox + x + 20, 39)] for x in range(0, W, 60)]), smooth=False)
    art = GP(art, inn, RED, seed=nx(), rough=0.2)
    hooks = strokes(W, H, rep(lambda ox: [([(ox + x + 44, 24), (ox + x + 50, 32), (ox + x + 56, 24)], 2.4, None) for x in range(0, W, 60)] +
                              [([(ox + x + 44, 40), (ox + x + 50, 32), (ox + x + 56, 40)], 2.4, None) for x in range(0, W, 60)]))
    art = GP(art, hooks, SAF, seed=nx(), rough=0.2)
    ln = strokes(W, H, [([(-10, 10), (W + 10, 10)], 2.4, None), ([(-10, 54), (W + 10, 54)], 2.4, None)])
    art = GP(art, ln, SAF, seed=nx(), rough=0.2)
    tri = shapes(W, H, rep(lambda ox: [[(ox + x, 0), (ox + x + 6, 6), (ox + x + 12, 0)] for x in range(0, W, 12)] + [[(ox + x, 64), (ox + x + 6, 58), (ox + x + 12, 64)] for x in range(0, W, 12)]), smooth=False)
    art = GP(art, tri, CRM, seed=nx(), rough=0.2)
    art = add_grain(art, nx(), 0.05)
    save_rgb(art, f"{OUT}/carpet.webp", quality=78)
    Image.fromarray((np.clip(np.concatenate([art, art], 1)[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/dk-carpet.png")
    clear()

if "ring" in PARTS:
    # Brass tray rim that frames the round hero photo (transparent centre).
    W = H = 560
    nx = Seq(86000)
    art = blank(W, H)
    c = W / 2
    outer = circles(W, H, [(c, c, 272)])
    hole = circles(W, H, [(c, c, 214)])
    rim = np.clip(outer - hole, 0, 1)
    art = GP(art, rim, BR, mix(BR, BR_D, 0.2), seed=nx(), rough=0.6, streak=0.3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy - c, xx - c)
    sheen = (0.5 + 0.5 * np.cos(ang * 2 + 0.8)) * rim
    art = tint(art, sheen, BR_H, 0.6, seed=nx(), streak=0.3)
    art = tint(art, (0.5 + 0.5 * np.cos(ang * 2 + 0.8 + math.pi)) * rim, BR_D, 0.55, seed=nx(), streak=0.3)
    # engraved arabesque: 16 petals + dotted rings
    eng = [(arc_pts(c, c, r, 0, math.tau, 120), 1.6, None) for r in (220, 228, 262, 266)]
    for k in range(16):
        a = k / 16 * math.tau
        p = petal_pts(c + math.cos(a) * 232, c + math.sin(a) * 232, 30, 9, a, n=14)
        eng.append((p + [p[0]], 1.4, None))
        a2 = a + math.pi / 16
        eng.append(([(c + math.cos(a2) * 236, c + math.sin(a2) * 236), (c + math.cos(a2) * 256, c + math.sin(a2) * 256)], 1.4, None))
    em = strokes(W, H, eng) * rim
    art = tint(art, em, BR_D, 0.75, seed=nx(), streak=0.2)
    dots = circles(W, H, [(c + math.cos(k / 72 * math.tau) * 245, c + math.sin(k / 72 * math.tau) * 245, 1.6) for k in range(72)]) * rim
    art = tint(art, dots, BR_D, 0.5, seed=nx())
    art = crayon(art, inner_edge(outer, 1.6), BR_D, seed=nx(), amt=0.7)
    art = crayon(art, np.clip(gaussian_filter(hole, 1.2) - hole, 0, 1) * 3 * rim, BR_D, seed=nx(), amt=0.7)
    art = add_grain(art, nx(), 0.03)
    preview(art, "dk-ring", bg="#2a1810")
    save_full(art, f"{OUT}/ring.webp", size=(400, 400), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 420, 70
    nx = Seq(87000)
    art = blank(W, H)
    c = 210
    star = shapes(W, H, [[(c + math.cos(k / 16 * math.tau - math.pi / 2) * (20 if k % 2 == 0 else 9), 35 + math.sin(k / 16 * math.tau - math.pi / 2) * (20 if k % 2 == 0 else 9)) for k in range(16)]], smooth=False)
    lines = strokes(W, H, [(curve([(20, 35), (100, 35), (176, 35)], 12), 2.6, (0.7, 0.0)), (curve([(244, 35), (320, 35), (400, 35)], 12), 2.6, (0.0, 0.7))])
    dia = shapes(W, H, [[(x, 35), (x + 7, 28), (x + 14, 35), (x + 7, 42)] for x in (150, 256)], smooth=False)
    m = np.clip(star + lines + dia, 0, 1)
    art = metal(art, m, BR, BR_H, BR_D, nx, amt=0.4)
    art = FO(art, star, BR, seed=nx(), emboss=0.6, sparkle=0.05)
    art = GP(art, circles(W, H, [(c, 35, 5)]), RED, seed=nx(), rough=0.2, pad=4)
    preview(art, "dk-divider", tone="#f5ead7")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
    clear()
