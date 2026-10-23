"""Lasem Tiga Negeri — batik tiga negeri Lasem: cream mori dyed in three baths (bang-bangan mengkudu red, indigo,
sogan brown) with canting wax contours, cecek dots and remukan crackle. Seruni flowers + latohan sprigs, a stylised
batik burung hong (phoenix), and an old Chinese-Javanese Lasem house gate (watercolour) with swallowtail ridge.
Run: python3 -I lasem-tiga-negeri.py [part ...]  parts: kain gate hong sprig seruni pinggir"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i3_lib import *

OUT = outdir("lasem-tiga-negeri")
PARTS = sys.argv[1:] or ["kain", "gate", "hong", "sprig", "seruni", "pinggir"]
CREAM, RED, RED_D, INDIGO, INDIGO_D, SOGAN, SOGAN_D = "#efe3c8", "#a3242a", "#7c171d", "#22355f", "#162544", "#8a5527", "#5e3818"


def seruni(cx, cy, r, rot=0.0, n=9):
    """Batik seruni (chrysanthemum-peony): heart + two petal rings. Returns (red_fill, inner_fill, lines, dots)."""
    outer = [petal_pts(cx, cy, r, r * 0.42, rot + k * math.tau / n, n=14, cup=0.15) for k in range(n)]
    inner = [petal_pts(cx, cy, r * 0.62, r * 0.32, rot + (k + 0.5) * math.tau / n, n=12) for k in range(n)]
    heart = ellipse_pts(cx, cy, r * 0.24, r * 0.24, 14)
    lines = []
    for k in range(n):
        a = rot + k * math.tau / n
        lines.append([(cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62), (cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9)])
    dots = [(cx + math.cos(rot + (k + 0.5) * math.tau / n) * r * 0.42, cy + math.sin(rot + (k + 0.5) * math.tau / n) * r * 0.42) for k in range(n)]
    dots += [(cx + math.cos(rot + k * math.tau / 6) * r * 0.12, cy + math.sin(rot + k * math.tau / 6) * r * 0.12) for k in range(6)]
    return outer, inner, heart, lines, dots


def leaf_batik(x, y, L, wd, ang):
    """Pointed leaf + central vein + side vein strokes."""
    poly = petal_pts(x, y, L, wd, ang, n=16, cup=0.1)
    ca, sa = math.cos(ang), math.sin(ang)
    vein = [(x + ca * L * t, y + sa * L * t) for t in np.linspace(0.05, 0.92, 10)]
    sides = []
    for t in np.linspace(0.2, 0.8, 5):
        px, py = x + ca * L * t, y + sa * L * t
        for sgn in (-1, 1):
            nx_, ny_ = -sa * sgn, ca * sgn
            sides.append([(px, py), (px + (ca * 0.5 + nx_) * wd * 0.55, py + (sa * 0.5 + ny_) * wd * 0.55)])
    return poly, [vein] + sides


def latohan(x0, y0, L, ang, rng, beads=True):
    """Latoh seaweed sprig: wavy stem, alternate short side branches each ending in a bead."""
    ca, sa = math.cos(ang), math.sin(ang)
    stem = []
    for t in np.linspace(0, 1, 26):
        off = math.sin(t * math.pi * 2.2) * L * 0.05
        stem.append((x0 + ca * L * t - sa * off, y0 + sa * L * t + ca * off))
    branches, bead = [], []
    for i, t in enumerate(np.linspace(0.12, 0.92, 7)):
        px, py = stem[int(t * 25)]
        sgn = 1 if i % 2 else -1
        bl = L * rng.uniform(0.14, 0.22) * (1.1 - t * 0.5)
        ba = ang + sgn * rng.uniform(0.7, 1.0)
        mid = (px + math.cos(ba) * bl * 0.5 - sa * sgn * 2, py + math.sin(ba) * bl * 0.5 + ca * sgn * 2)
        end = (px + math.cos(ba + sgn * 0.3) * bl, py + math.sin(ba + sgn * 0.3) * bl)
        branches.append(curve([(px, py), mid, end], 10))
        bead.append((end[0], end[1], max(2.6, L * 0.028)))
    bead.append((stem[-1][0], stem[-1][1], max(3.0, L * 0.032)))
    return [stem] + branches, bead


if "kain" in PARTS:
    # seamless 420 tile: red seruni, indigo leaves + latohan, sogan ground with cream isen
    W = H = 420
    rng = random.Random(11)
    nx = Seq(61100)
    red_f, red_in, hearts, ind_f, lines, dots, beads, latl = [], [], [], [], [], [], [], []
    motifs = [(110, 120, 64, 0.2), (320, 300, 56, 0.9), (330, 70, 30, 0.4), (90, 340, 34, 1.3)]
    for cx, cy, r, rot in motifs:
        o, i, h, l, d = seruni(cx, cy, r, rot, 9 if r > 40 else 7)
        red_f += o; red_in += i; hearts.append(h); lines += l; dots += d
    leaves = [(150, 170, 70, 26, 0.75), (60, 70, 62, 22, -2.4), (270, 260, 62, 24, -2.3), (380, 360, 58, 22, 0.8),
              (200, 70, 58, 20, -0.4), (250, 380, 54, 20, 2.6), (20, 200, 60, 22, 0.1), (360, 170, 56, 20, 1.9)]
    for x, y, L, wd, a in leaves:
        p, vl = leaf_batik(x, y, L, wd, a)
        ind_f.append(p); lines += vl
    for x, y, L, a in [(175, 250, 110, -0.5), (240, 140, 90, 2.4), (20, 390, 80, -0.9), (300, 20, 80, 0.35)]:
        st, bd = latohan(x, y, L, a, rng)
        latl += st; beads += bd

    def wrap(fn):
        acc = np.zeros((H, W), np.float32)
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):
                acc = np.maximum(acc, fn(dx, dy))
        return acc
    sh = lambda pts, dx, dy: [(x + dx, y + dy) for x, y in pts]
    m_red = wrap(lambda dx, dy: shapes(W, H, [sh(p, dx, dy) for p in red_f]))
    m_redin = wrap(lambda dx, dy: shapes(W, H, [sh(p, dx, dy) for p in red_in]))
    m_heart = wrap(lambda dx, dy: shapes(W, H, [sh(p, dx, dy) for p in hearts]))
    m_ind = wrap(lambda dx, dy: shapes(W, H, [sh(p, dx, dy) for p in ind_f]))
    m_lat = wrap(lambda dx, dy: polyline_mask(W, H, [sh(p, dx, dy) for p in latl], 4.2))
    m_bead = wrap(lambda dx, dy: circles(W, H, [(x + dx, y + dy, r) for x, y, r in beads]))
    m_lines = wrap(lambda dx, dy: polyline_mask(W, H, [sh(p, dx, dy) for p in lines], 2.0))
    m_dots = wrap(lambda dx, dy: circles(W, H, [(x + dx, y + dy, 1.9) for x, y in dots]))
    # contour lines around every motif (wax outline)
    motif = np.clip(np.maximum.reduce([m_red, m_ind, m_lat, m_bead]), 0, 1)
    halo = np.clip(gaussian_filter(motif, 1.6) * 3, 0, 1)
    contour = np.clip(halo - motif, 0, 1)
    # sogan ground everywhere else with cream isen-isen (cecek + small ukel crosses on a grid)
    isen = []
    for gy in range(0, H, 14):
        for gx in range(0, W, 14):
            isen.append((gx + (7 if (gy // 14) % 2 else 0), gy, 1.5))
    m_isen = circles(W, H, isen)
    ground = np.clip(1 - halo, 0, 1)
    cloth = batik_cloth(W, H, CREAM, nx())
    # bath 1: indigo (leaves + latoh)
    blue = np.clip(np.maximum(m_ind, np.maximum(m_lat, m_bead)) - m_lines - m_dots, 0, 1)
    cloth = dye_bath(cloth, blue, INDIGO, nx(), depth=0.92, crack=0.5)
    # bath 2: mengkudu red (flowers)
    redm = np.clip(np.maximum(m_red - m_redin * 0.0, 0) - m_lines - m_dots, 0, 1)
    cloth = dye_bath(cloth, np.clip(redm - m_redin, 0, 1), RED, nx(), depth=0.92, crack=0.4)
    cloth = dye_bath(cloth, np.clip(m_redin - m_heart - m_dots, 0, 1), "#c4473a", nx(), depth=0.7, crack=0.3)
    cloth = dye_bath(cloth, np.clip(m_heart - m_dots, 0, 1), SOGAN, nx(), depth=0.9, crack=0.2)
    # bath 3: sogan brown ground (last, over everything not waxed)
    cloth = dye_bath(cloth, np.clip(ground - m_isen, 0, 1), "#6a3f1d", nx(), depth=0.93, crack=0.35, mott=0.3)
    cloth = add_grain(cloth, nx(), 0.03)
    tile = tileable(cloth)
    tile[..., 3] = 1
    save_rgb(tile, f"{OUT}/kain.webp", quality=80)
    prev(tile, "lasem-kain")
    clear()


if "gate" in PARTS:
    # old Lasem house gate (regol) in high white wall, tiled saddle roof with upswept swallowtail ridge ends,
    # double timber doors, house roof behind; watercolour + ink, aged lime wash
    W, H = 820, 600
    nx = Seq(61200); cx = W / 2
    rng = random.Random(5)
    art = blank(W, H)
    # sky wash behind (pale, fades out)
    sky = shapes(W, H, [[(40, 40), (W - 40, 30), (W - 20, 380), (20, 390)]])
    sky = sky * np.clip(1 - np.abs(np.mgrid[0:H, 0:W][1] - cx) / (W * 0.55), 0, 1)
    art = G(art, gaussian_filter(sky, 30), "#d9cbb0", "#cbb79a", seed=nx(), density=0.35, edge=0.1, bloom=0.5)
    # house roof behind wall (long saddle roof, ridge with curled ends), lighter = further away
    hr = [(50, 176), (140, 84), (W - 140, 84), (W - 50, 176)]
    art = G(art, shapes(W, H, [hr], smooth=False), "#8a8480", "#77716d", seed=nx(), density=0.75, edge=0.5)
    art = G(art, polyline_mask(W, H, [[(x, 88), (x + (x - cx) * 0.16, 172)] for x in range(146, W - 140, 14)], 1.8), "#4d4846", seed=nx(), density=0.45, edge=0.2, rough=2)
    ridge = curve([(104, 52), (140, 80), (cx, 78), (W - 140, 80), (W - 104, 52)], 40)
    art = G(art, polyline_mask(W, H, [ridge], 11), "#55504d", seed=nx(), density=0.9, edge=0.5, rough=2)
    art = G(art, polyline_mask(W, H, [[(46, 178), (W - 46, 178)]], 7), "#5a5450", seed=nx(), density=0.85, rough=2)
    # house front wall with two shuttered windows (krepyak)
    art = G(art, shapes(W, H, [[(96, 180), (W - 96, 180), (W - 96, 300), (96, 300)]], smooth=False), "#e4dacb", "#d3c4ab", seed=nx(), density=0.7)
    for x0 in (140, W - 220):
        win = shapes(W, H, [[(x0, 200), (x0 + 80, 200), (x0 + 80, 286), (x0, 286)]], smooth=False)
        art = G(art, win, "#5f7a6c", "#4b6457", seed=nx(), density=0.9, edge=0.5)
        sl = polyline_mask(W, H, [[(x0 + 4, y), (x0 + 76, y)] for y in range(206, 284, 7)] + [[(x0 + 40, 200), (x0 + 40, 286)]], 1.6)
        art = G(art, sl, "#2f4238", seed=nx(), density=0.6, edge=0.1, rough=1.5)
        art = G(art, polyline_mask(W, H, [[(x0 - 6, 196), (x0 + 86, 196)]], 5), "#cfc2a8", seed=nx(), density=0.9, rough=1.5)
    # compound wall (tembok tinggi) with coping
    wall = shapes(W, H, [[(0, 300), (W, 300), (W, 560), (0, 560)]], smooth=False)
    art = G(art, wall, "#efe7d6", "#dccdb2", seed=nx(), density=0.85, edge=0.35, bloom=0.5)
    # lime-wash stains & damp at the foot
    damp = wall * np.clip((np.mgrid[0:H, 0:W][0] - 470) / 90, 0, 1)
    art = G(art, damp, "#bfae8c", "#a99773", seed=nx(), density=0.45, bloom=0.7, edge=0.25)
    for _ in range(4):
        x = rng.uniform(40, W - 40); y = rng.uniform(320, 420)
        art = G(art, shapes(W, H, [ellipse_pts(x, y, rng.uniform(20, 50), rng.uniform(10, 26), 12)]) * wall, "#cfc0a2", seed=nx(), density=0.3, bloom=0.8)
    yy0, xx0 = np.mgrid[0:H, 0:W].astype(np.float32)
    brickf = (((yy0 % 12) > 1.6) & (((xx0 + ((yy0 // 12) % 2) * 13) % 26) > 2)).astype(np.float32)
    for (bx, by, rx, ry) in [(70, 420, 46, 30), (W - 90, 480, 52, 26), (cx - 250, 520, 30, 20)]:
        patch = shapes(W, H, [deform(ellipse_pts(bx, by, rx, ry, 9), rng, 3, 0.16)])
        art = G(art, patch, "#c9a587", seed=nx(), density=0.6, edge=0.7, bloom=0.3)
        art = G(art, patch * brickf * 0.9, "#a5523a", "#8a4430", seed=nx(), density=0.75, edge=0.2, rough=1.5)
    coping = shapes(W, H, [[(0, 290), (W, 290), (W, 306), (0, 306)]], smooth=False)
    art = G(art, coping, "#8b847c", "#6f6862", seed=nx(), density=0.85)
    # gate block (regol) centered: pillars + roof
    gw = 300
    pil = shapes(W, H, [[(cx - gw / 2 - 24, 250), (cx - gw / 2 + 24, 250), (cx - gw / 2 + 24, 560), (cx - gw / 2 - 24, 560)],
                         [(cx + gw / 2 - 24, 250), (cx + gw / 2 + 24, 250), (cx + gw / 2 + 24, 560), (cx + gw / 2 - 24, 560)]], smooth=False)
    art = G(art, pil, "#f4eee2", "#e2d6c0", seed=nx(), density=0.95, edge=0.45)
    art = G(art, pil * (np.mgrid[0:H, 0:W][1] > cx - gw / 2 + 4) * (np.mgrid[0:H, 0:W][1] < cx - gw / 2 + 24), "#b9a88a", seed=nx(), density=0.45)
    art = G(art, pil * (np.mgrid[0:H, 0:W][1] > cx + gw / 2 + 4), "#b9a88a", seed=nx(), density=0.45)
    # plaster panel frames on pillars (red framed calligraphy-free tablets)
    tabs = shapes(W, H, [[(cx - gw / 2 - 14, 330), (cx - gw / 2 + 14, 330), (cx - gw / 2 + 14, 470), (cx - gw / 2 - 14, 470)],
                          [(cx + gw / 2 - 14, 330), (cx + gw / 2 + 14, 330), (cx + gw / 2 + 14, 470), (cx + gw / 2 - 14, 470)]], smooth=False)
    art = G(art, tabs, RED, RED_D, seed=nx(), density=0.85, edge=0.6)
    art = G(art, shapes(W, H, [[(cx - gw / 2 - 8, 338), (cx - gw / 2 + 8, 338), (cx - gw / 2 + 8, 462), (cx - gw / 2 - 8, 462)],
                               [(cx + gw / 2 - 8, 338), (cx + gw / 2 + 8, 338), (cx + gw / 2 + 8, 462), (cx + gw / 2 - 8, 462)]], smooth=False), "#e6c46a", seed=nx(), density=0.55)
    # doorway: dark recess + two timber leaves (slightly ajar)
    door = shapes(W, H, [[(cx - gw / 2 + 26, 300), (cx + gw / 2 - 26, 300), (cx + gw / 2 - 26, 560), (cx - gw / 2 + 26, 560)]], smooth=False)
    art = G(art, door, "#3b2a22", "#2a1d18", seed=nx(), density=0.95, edge=0.3)
    lw = (gw - 52) / 2
    leafL = shapes(W, H, [[(cx - gw / 2 + 30, 306), (cx - 6, 306), (cx - 6, 556), (cx - gw / 2 + 30, 556)]], smooth=False)
    leafR = shapes(W, H, [[(cx + 10, 306), (cx + gw / 2 - 30, 306), (cx + gw / 2 - 30, 556), (cx + 10, 556)]], smooth=False)
    art = G(art, leafL, "#7d2a22", "#5e1d18", seed=nx(), density=0.95, edge=0.55)
    art = G(art, leafR, "#7a2820", "#5a1b16", seed=nx(), density=0.95, edge=0.55)
    planks = []
    for x0, x1 in [(cx - gw / 2 + 30, cx - 6), (cx + 10, cx + gw / 2 - 30)]:
        for x in np.linspace(x0 + 20, x1 - 20, 5):
            planks.append([(x, 310), (x + rng.uniform(-1, 1), 552)])
    art = G(art, polyline_mask(W, H, planks, 1.4), "#3a120e", seed=nx(), density=0.6, edge=0.1, rough=2)
    # carved panels on leaves
    pan = []
    for x0, x1 in [(cx - gw / 2 + 42, cx - 18), (cx + 22, cx + gw / 2 - 42)]:
        pan.append([(x0, 330), (x1, 330), (x1, 410), (x0, 410)])
        pan.append([(x0, 430), (x1, 430), (x1, 530), (x0, 530)])
    panm = polyline_mask(W, H, [p + [p[0]] for p in pan], 2.4, cap=False)
    art = G(art, panm, "#d6a54a", seed=nx(), density=0.75, edge=0.3, rough=2)
    rings = np.maximum(ring(W, H, cx - 22, 440, 9, 2.6), ring(W, H, cx + 26, 440, 9, 2.6))
    art = FO(art, rings, "#c9a14a", seed=nx())
    # gate roof: little saddle roof with swallowtail ridge
    rf = [(cx - gw / 2 - 70, 262), (cx - gw / 2 - 30, 196), (cx + gw / 2 + 30, 196), (cx + gw / 2 + 70, 262)]
    art = G(art, shapes(W, H, [rf], smooth=False), "#565150", "#3c3736", seed=nx(), density=0.95, edge=0.6)
    art = G(art, polyline_mask(W, H, [[(x, 200), (x + (x - cx) * 0.3, 260)] for x in range(int(cx - gw / 2 - 26), int(cx + gw / 2 + 30), 12)], 2.2), "#2a2524", seed=nx(), density=0.7, rough=2)
    eave = shapes(W, H, [[(cx - gw / 2 - 74, 258), (cx + gw / 2 + 74, 258), (cx + gw / 2 + 70, 270), (cx - gw / 2 - 70, 270)]], smooth=False)
    art = G(art, eave, "#2e2a29", seed=nx(), density=0.95)
    gr = curve([(cx - gw / 2 - 80, 150), (cx - gw / 2 - 52, 178), (cx - gw / 2 - 20, 194), (cx, 192), (cx + gw / 2 + 20, 194), (cx + gw / 2 + 52, 178), (cx + gw / 2 + 80, 150)], 60)
    art = G(art, polyline_mask(W, H, [gr], 14), "#3a3433", seed=nx(), density=1.0, edge=0.5, rough=2)
    tips = circles(W, H, [(cx - gw / 2 - 80, 150, 8), (cx + gw / 2 + 80, 150, 8)])
    art = G(art, tips, "#3a3433", seed=nx(), density=1)
    # ridge plaster ornament (simple white relief medallion — no figures)
    art = G(art, shapes(W, H, [ellipse_pts(cx, 214, 34, 14, 16)]), "#f2ebdd", seed=nx(), density=0.95)
    art = G(art, shapes(W, H, [ellipse_pts(cx, 214, 10, 8, 12)]), RED, seed=nx(), density=0.85)
    # lanterns hanging under eave (red paper lanterns)
    for lx in (cx - gw / 2 + 50, cx + gw / 2 - 50):
        art = G(art, polyline_mask(W, H, [[(lx, 270), (lx, 286)]], 1.5), "#2a2524", seed=nx(), density=0.8, rough=1)
        lm = shapes(W, H, [ellipse_pts(lx, 304, 17, 20, 16)])
        art = G(art, lm, "#c8322b", "#a3242a", seed=nx(), density=0.95, edge=0.6)
        art = G(art, shapes(W, H, [[(lx - 9, 282), (lx + 9, 282), (lx + 9, 287), (lx - 9, 287)], [(lx - 9, 322), (lx + 9, 322), (lx + 9, 327), (lx - 9, 327)]], smooth=False), "#e0b04a", seed=nx(), density=0.9)
        art = G(art, polyline_mask(W, H, [[(lx + d, 328), (lx + d, 346)] for d in (-3, 0, 3)], 1.2), "#c8322b", seed=nx(), density=0.8, rough=1)
    # step + ground shadow
    art = G(art, shapes(W, H, [[(cx - gw / 2 - 40, 556), (cx + gw / 2 + 40, 556), (cx + gw / 2 + 54, 578), (cx - gw / 2 - 54, 578)]], smooth=False), "#b6aa95", "#9e917b", seed=nx(), density=0.8)
    art = G(art, gaussian_filter(shapes(W, H, [[(0, 566), (W, 560), (W, 600), (0, 600)]], smooth=False), 6), "#c8b998", seed=nx(), density=0.5, bloom=0.6)
    # frangipani (kamboja) branch spilling over the wall, right
    br = curve([(W - 30, 236), (W - 80, 262), (W - 150, 292), (W - 190, 330)], 30)
    br2 = curve([(W - 80, 262), (W - 110, 220), (W - 130, 196)], 16)
    art = G(art, polyline_mask(W, H, [br, br2], 9), "#8f7b62", "#6f5d48", seed=nx(), density=0.9, rough=2)
    lvs = []
    for (x, y, a) in [(W - 120, 205, -2.2), (W - 145, 196, -1.4), (W - 115, 186, -0.8), (W - 190, 330, 2.2), (W - 200, 318, 3.0), (W - 176, 342, 1.5), (W - 60, 250, -1.9), (W - 40, 244, -1.0)]:
        lvs.append(petal_pts(x, y, rng.uniform(50, 66), rng.uniform(14, 18), a, n=14))
    art = G(art, shapes(W, H, lvs), "#5d7a4a", "#3f5c37", seed=nx(), density=0.8, edge=0.6)
    fl = []
    for (x, y) in [(W - 126, 196), (W - 196, 322), (W - 56, 244), (W - 98, 240)]:
        for k in range(5):
            fl.append(petal_pts(x, y, 22, 11, k * math.tau / 5 + rng.uniform(0, 1), n=10, cup=0.3))
    flm = shapes(W, H, fl)
    art = G(art, flm, "#fdf8ee", "#efd2b8", seed=nx(), density=0.95, edge=0.9)
    art = ink_edge(art, flm, "#b49a7a", 1.2, nx(), 0.6)
    art = G(art, circles(W, H, [(W - 126, 196, 4), (W - 196, 322, 4), (W - 56, 244, 4), (W - 98, 240, 4)]), "#e7b84a", seed=nx(), density=0.85)
    # ink accents (loose)
    ink = polyline_mask(W, H, [[(cx - gw / 2 - 24, 252), (cx - gw / 2 - 24, 556)], [(cx + gw / 2 + 24, 252), (cx + gw / 2 + 24, 556)], [(0, 306), (cx - gw / 2 - 24, 306)], [(cx + gw / 2 + 24, 306), (W, 306)]], 1.3)
    ink *= np.clip((fbm(W, H, nx(), 9, 2) - 0.25) * 4, 0, 1)
    art = over(art, flat(ink, "#3d2f28", 0.55))
    # fade the wall edges into paper (vignette alpha)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(np.minimum(xx, W - xx) / 46, 0, 1)
    # bake onto cream mori so the lime wash reads opaque; only the sky edge fades into the page
    bg = np.asarray(paper(W, H, "#f3ead6", 9), np.float32) / 255
    a = art[..., 3:4]
    rgb = bg * (1 - a) + (bg * art[..., :3]) ** 0.85 * a
    alpha = np.clip(yy / 130, 0, 1) * np.clip(np.minimum(xx, W - xx) / 30, 0, 1)
    alpha = np.maximum(alpha, np.clip(a[..., 0] * 1.4, 0, 1) * np.clip(yy / 40, 0, 1))
    art = np.concatenate([rgb, alpha[..., None]], -1)
    prev(art, "lasem-gate")
    save(art, f"{OUT}/gate.webp", max_w=680, quality=80)
    clear()


if "hong" in PARTS:
    # stylised batik phoenix flying left->right: S body, crest, layered wing, 3 long curled tail plumes
    W, H = 760, 530
    nx = Seq(61300); rng = random.Random(7)
    hx, hy = 560, 150
    body = curve([(hx, hy), (hx - 40, hy + 40), (hx - 110, hy + 80), (hx - 190, hy + 96)], 40)
    bodym = strokes(W, H, [(body, 46, (0.0, 0.55))])
    head = circles(W, H, [(hx + 4, hy - 4, 24)])
    beak = shapes(W, H, [[(hx + 22, hy - 14), (hx + 56, hy - 2), (hx + 24, hy + 6)]], smooth=False)
    crest = [curve([(hx - 6, hy - 22), (hx - 10 - 10 * k, hy - 56 - 8 * k), (hx - 34 - 14 * k, hy - 70 - 4 * k)], 14) for k in range(3)]
    crestm = strokes(W, H, [(c, 9, (0.1, 0.6)) for c in crest])
    crest_b = circles(W, H, [(c[-1][0], c[-1][1], 7) for c in crest])
    wattle = shapes(W, H, [petal_pts(hx + 6, hy + 14, 30, 10, 1.9, n=10)])
    # wing: fan of long feathers up-back
    wing = []
    wlines = []
    for k in range(6):
        a = -2.0 - k * 0.2
        L = 150 - k * 12
        base = (hx - 90 + k * 6, hy + 60)
        wing.append(petal_pts(base[0], base[1], L, 26, a, n=16, cup=0.1))
        wlines.append([(base[0] + math.cos(a) * 14, base[1] + math.sin(a) * 14), (base[0] + math.cos(a) * L * 0.85, base[1] + math.sin(a) * L * 0.85)])
    wing_cov = [petal_pts(hx - 80 + k * 14, hy + 64, 56, 22, -2.3 + k * 0.12, n=12) for k in range(4)]
    # tail: 3 long plumes sweeping down-left ending in curls (ukel)
    tails, tail_lines, ukel = [], [], []
    for k, (dx, dy, cw) in enumerate([(-250, 60, 1), (-300, 150, 1), (-220, 210, -1)]):
        p0 = (hx - 190, hy + 96)
        c = curve([p0, (p0[0] - 60, p0[1] + 10 + k * 20), (p0[0] + dx * 0.6, p0[1] + dy * 0.5), (p0[0] + dx, p0[1] + dy)], 50)
        tails.append((c, 30 - k * 4, (0.05, 0.6)))
        ex, ey = c[-1]
        sp = spiral_pts(ex + 12 * cw, ey + 4, 22, 4, math.pi * (0.0 if cw > 0 else 1.0), 1.2, 30, cw)
        ukel.append(sp)
        tail_lines.append(c[2:-4])
    tailm = strokes(W, H, tails)
    ukelm = polyline_mask(W, H, ukel, 7)
    # eye
    eye = circles(W, H, [(hx + 8, hy - 8, 5)])
    # wax lines: body scales (arcs), wing veins, tail spine lines, cecek
    scales = []
    for t in np.linspace(0.15, 0.85, 7):
        px, py = body[int(t * 39)]
        scales.append(arc_pts(px, py, 12, 0.3, 2.8, 10))
    lines = polyline_mask(W, H, scales + wlines + tail_lines, 2.2)
    dots_ = []
    for c, wd, _ in tails:
        for i in range(4, len(c) - 6, 4):
            x, y = c[i]; x2, y2 = c[i + 1]
            a = math.atan2(y2 - y, x2 - x) + math.pi / 2
            for sgn in (-1, 1):
                dots_.append((x + math.cos(a) * wd * 0.28 * sgn, y + math.sin(a) * wd * 0.28 * sgn, 1.8))
    dotm = circles(W, H, dots_)
    wingm = shapes(W, H, wing); wcov = shapes(W, H, wing_cov)
    contour_src = [bodym, head, beak, crestm, crest_b, wattle, wingm, wcov, tailm, ukelm]
    layers = [
        (wingm, INDIGO), (np.clip(wcov, 0, 1), "#36508a"), (tailm, SOGAN), (ukelm, RED), (crestm, INDIGO), (crest_b, RED),
        (bodym, RED), (head, RED), (wattle, SOGAN), (beak, "#c8923a"),
    ]
    # outline wax around each shape: inner rim of each mask
    rims = np.zeros((H, W), np.float32)
    for m in [wingm, wcov, bodym, head, tailm, wattle]:
        mb = (m > 0.5).astype(np.float32)
        d = distance_transform_edt(mb)
        rims = np.maximum(rims, ((d > 0) & (d < 2.4)).astype(np.float32))
    allw = np.maximum.reduce([lines, dotm, eye, rims])
    art = batik_motif(W, H, layers, allw, seed=nx(), crack=0.5)
    prev(art, "lasem-hong")
    save(art, f"{OUT}/hong.webp", max_w=560, quality=82)
    clear()


if "sprig" in PARTS:
    # divider: small seruni in the middle, latohan sprigs either side
    W, H = 640, 120
    nx = Seq(61400); rng = random.Random(3)
    cx, cy = W / 2, H / 2
    o, i, h, l, d = seruni(cx, cy, 34, 0.3, 8)
    st, bd = [], []
    for sgn in (-1, 1):
        s1, b1 = latohan(cx + sgn * 40, cy, 250, 0 if sgn > 0 else math.pi, rng)
        st += s1; bd += b1
    lf = []; lvl = []
    for sgn in (-1, 1):
        for (off, ang, L) in [(52, -0.5, 40), (60, 0.5, 34)]:
            p, vl = leaf_batik(cx + sgn * off, cy + (-6 if ang < 0 else 6), L, 14, (ang if sgn > 0 else math.pi - ang))
            lf.append(p); lvl += vl
    m_o = shapes(W, H, o); m_i = shapes(W, H, i); m_h = shapes(W, H, [h])
    m_st = polyline_mask(W, H, st, 4.4); m_bd = circles(W, H, [(x, y, r * 1.1) for x, y, r in bd]); m_lf = shapes(W, H, lf)
    lines = polyline_mask(W, H, l + lvl, 1.8)
    dots_ = circles(W, H, [(x, y, 1.7) for x, y in d])
    rims = np.zeros((H, W), np.float32)
    for m in [m_o, m_i, m_h, m_lf]:
        dd = distance_transform_edt((m > 0.5).astype(np.float32)); rims = np.maximum(rims, ((dd > 0) & (dd < 2.0)).astype(np.float32))
    art = batik_motif(W, H, [(m_st, INDIGO), (m_bd, RED), (m_lf, INDIGO), (m_o, RED), (m_i, "#c4473a"), (m_h, SOGAN)], np.maximum.reduce([lines, dots_, rims]), seed=nx())
    prev(art, "lasem-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=360, quality=84)
    clear()


if "seruni" in PARTS:
    W = H = 260
    nx = Seq(61500)
    o, i, h, l, d = seruni(130, 130, 110, 0.0, 10)
    lf = []; lvl = []
    for k in range(5):
        a = k * math.tau / 5 + 0.3
        p, vl = leaf_batik(130 + math.cos(a) * 60, 130 + math.sin(a) * 60, 64, 22, a)
        lf.append(p); lvl += vl
    m_o = shapes(W, H, o); m_i = shapes(W, H, i); m_h = shapes(W, H, [h]); m_lf = np.clip(shapes(W, H, lf) - gaussian_filter(m_o, 1) , 0, 1)
    rims = np.zeros((H, W), np.float32)
    for m in [m_o, m_i, m_h]:
        dd = distance_transform_edt((m > 0.5).astype(np.float32)); rims = np.maximum(rims, ((dd > 0) & (dd < 2.6)).astype(np.float32))
    lines = polyline_mask(W, H, l + lvl, 2.4)
    dots_ = circles(W, H, [(x, y, 2.6) for x, y in d])
    art = batik_motif(W, H, [(m_lf, INDIGO), (m_o, RED), (m_i, "#c4473a"), (m_h, SOGAN)], np.maximum.reduce([lines, dots_, rims]), seed=nx())
    prev(art, "lasem-seruni")
    save(art, f"{OUT}/seruni.webp", max_w=200, quality=84)
    clear()


if "pinggir" in PARTS:
    # border band repeat-x (period 60): indigo rail, red untu walang (sawtooth), sogan rail, cream cecek
    W, H = 240, 56
    nx = Seq(61600)
    cloth = batik_cloth(W, H, CREAM, nx())
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rail1 = ((yy > 3) & (yy < 11)).astype(np.float32)
    rail2 = ((yy > H - 11) & (yy < H - 3)).astype(np.float32)
    teeth = shapes(W, H, [[(x, 15), (x + 20, 15), (x + 10, 40)] for x in range(-20, W + 20, 20)], smooth=False)
    teeth2 = shapes(W, H, [[(x + 10, 42), (x + 20, 42), (x + 15, 30)] for x in range(-20, W + 20, 20)], smooth=False) * 0
    dots_ = circles(W, H, [(x + 10, 46, 1.8) for x in range(-20, W + 20, 20)] + [(x, 7, 1.5) for x in range(0, W, 8)])
    cloth = dye_bath(cloth, np.clip(rail1 - dots_, 0, 1), INDIGO, nx(), depth=0.92, crack=0.4, bleed=0.5)
    cloth = dye_bath(cloth, teeth, RED, nx(), depth=0.9, crack=0.3, bleed=0.5)
    cloth = dye_bath(cloth, rail2, SOGAN, nx(), depth=0.9, crack=0.5, bleed=0.5)
    cloth[..., 3] = 1
    save_rgb(cloth, f"{OUT}/pinggir.webp", quality=82)
    prev(cloth, "lasem-pinggir")
    clear()
