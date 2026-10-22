"""Maluku Tifa — gouache: two carved tifa drums (painted hardwood with relief spirals, a stretched hide head, braided
rattan ring and rattan lacing with wooden wedges), clove & nutmeg sprigs (glossy leaves, pink-red clove buds, a split
nutmeg with its red mace over the dark seed), a turquoise island sea (Ambon bay), and a tenun ikat Tanimbar tile woven
thread by thread (warp-faced, dye bleeding along the warp). Run: python3 -I maluku-tifa.py [part ...]
parts: tifa sprig sea ikat twig    Assets -> public/themes/art/maluku-tifa/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c1_lib import *

OUT = outdir("maluku-tifa")
PARTS = sys.argv[1:] or ["tifa", "sprig", "sea", "ikat", "twig"]
WOOD, WOOD_D, WOOD_L = "#6b3520", "#3a1a10", "#9a5631"
OCHRE, RUST, CREAM, BLACK = "#c99a45", "#a8442a", "#ead9b6", "#1e1a1c"
HIDE, HIDE_D = "#e3c99c", "#b8956a"
RATTAN, RATTAN_D = "#c79a58", "#8a6232"
TURQ, TURQ_D, TEAL = "#1aa3a3", "#0d6f7a", "#0b4a5a"
LEAF, LEAF_D, LEAF_L = "#3b6b3a", "#22452a", "#7aa260"


def tifa(art, W, H, cx, top, h, r, rng, nx, tilt=0.0):
    """One tifa: single-headed long drum; head at `top`, length h, head radius r (seen slightly from above)."""
    ca, sa = math.cos(tilt), math.sin(tilt)
    def P(u, v):  # u across (-1..1 * r), v down (0..1 * h)
        x, y = u * r, v * h
        return (cx + x * ca - y * sa, top + x * sa + y * ca)
    ell = 0.28  # head ellipse squash
    # body silhouette: slight flare at the head, waist, flared foot (carved open foot)
    prof = [(0.0, 1.0), (0.08, 0.98), (0.2, 0.86), (0.45, 0.72), (0.62, 0.74), (0.78, 0.86), (0.9, 0.98), (1.0, 1.04)]
    L = [P(-w, v) for v, w in prof]; R = [P(w, v) for v, w in prof[::-1]]
    body = shapes(W, H, [L + [P(0, 1.0 + ell * 0.25)] + R + [P(0, -ell * 0.2)]])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = knockout(art, body, 1.0, 1.0)
    art = GP(art, body, WOOD, "#7a3e24", seed=nx(), rough=1.4, streak=1.0)
    # cylinder shading: dark on the right, lit stripe left of centre
    u = ((xx - cx) * ca + (yy - top) * sa) / r
    art = wash(art, body * np.clip((u + 0.1) / 1.0, 0, 1) ** 1.3, WOOD_D, 0.7, seed=nx())
    art = wash(art, body * np.clip(1 - np.abs(u + 0.45) / 0.25, 0, 1), WOOD_L, 0.45, seed=nx())
    # carved relief bands: ochre/rust painted grooves (spirals & chevrons), following the cylinder curvature
    v = ((xx - cx) * -sa + (yy - top) * ca) / h
    curv = (1 - np.clip(u, -1, 1) ** 2) ** 0.5 * ell * r / h * 0.9
    vv = v - curv
    bands = []
    for v0, v1, kind in [(0.16, 0.24, "zig"), (0.3, 0.52, "spiral"), (0.56, 0.62, "dots"), (0.7, 0.8, "zig")]:
        band = body * ((vv > v0) & (vv < v1))
        if kind == "zig":
            ph = (u * 3.2) % 1.0
            zig = np.abs(((vv - v0) / (v1 - v0)) - np.abs(ph - 0.5) * 2) < 0.22
            m = band * zig
            art = wash(art, m, OCHRE, 0.9, seed=nx())
        elif kind == "spiral":
            # interlocking hooks: concentric squares per cell
            cu = (u + 1) * 2.2; cv = (vv - v0) / (v1 - v0) * 2
            fu, fv = cu % 1.0, cv % 1.0
            d = np.maximum(np.abs(fu - 0.5), np.abs(fv - 0.5))
            sq = ((d > 0.12) & (d < 0.2)) | ((d > 0.3) & (d < 0.38))
            gap = (np.abs(fu - 0.5) < 0.1) & (fv > 0.5)
            m = band * (sq & ~gap)
            art = wash(art, m, CREAM, 0.85, seed=nx())
            art = wash(art, band * (d < 0.1), RUST, 0.9, seed=nx())
        else:
            dd = ((u * 5) % 1.0 - 0.5) ** 2 + (((vv - v0) / (v1 - v0)) - 0.5) ** 2 * 0.6
            art = wash(art, band * (dd < 0.05), CREAM, 0.85, seed=nx())
        # carved edge lines
        edge = body * ((np.abs(vv - v0) < 0.005) | (np.abs(vv - v1) < 0.005))
        art = wash(art, edge.astype(np.float32), WOOD_D, 0.9, seed=nx())
    # re-shade the paint on the dark side
    art = wash(art, body * np.clip((u - 0.2) / 0.8, 0, 1) * (vv > 0.1), WOOD_D, 0.45, seed=nx())
    # side handle (carved loop) on the left
    hd = strokes(W, H, [(curve([P(-0.76, 0.36), P(-1.12, 0.44), P(-1.12, 0.56), P(-0.73, 0.62)], 20), r * 0.13, None)])
    art = knockout(art, hd, 1.0, 0.8)
    art = GP(art, hd, WOOD, seed=nx(), rough=0.8)
    art = wash(art, hd * np.clip((-u - 0.9) / 0.3, 0, 1), WOOD_L, 0.5, seed=nx())
    # rattan lacing: zigzag cords from the head ring down to a lower ring, with wedges
    v_lo = 0.15
    cords = []
    n = 9
    for i in range(n):
        a0 = -1 + 2 * i / n; a1 = -1 + 2 * (i + 0.5) / n
        p0 = P(a0 * 0.97, 0.02 + (1 - a0 ** 2) ** 0.5 * ell * r / h); p1 = P(a1 * 0.9, v_lo + (1 - a1 ** 2) ** 0.5 * ell * r / h * 0.9)
        a2 = -1 + 2 * (i + 1) / n
        p2 = P(a2 * 0.97, 0.02 + (1 - a2 ** 2) ** 0.5 * ell * r / h)
        cords += [([p0, p1], r * 0.045, None), ([p1, p2], r * 0.045, None)]
    cm = strokes(W, H, cords) * body
    art = wash(art, np.roll(cm, 2, 1) * body, WOOD_D, 0.6, seed=nx())
    art = GP(art, cm, RATTAN, RATTAN_D, seed=nx(), rough=0.5, streak=0.5)
    lo = [P(-0.9 + 1.8 * k / 30, v_lo + (1 - (-0.9 + 1.8 * k / 30) ** 2 / 0.81) ** 0.5 * ell * r / h * 0.9) for k in range(31)]
    lring = strokes(W, H, [(lo, r * 0.11, None)])
    art = GP(art, lring, RATTAN, RATTAN_D, seed=nx(), rough=0.6, streak=0.8)
    braid = lring * (np.sin((xx * ca + yy * sa) * 0.9 + (yy * ca) * 0.9) > 0.3)
    art = wash(art, braid.astype(np.float32), RATTAN_D, 0.55, seed=nx())
    wedges = shapes(W, H, [[P(a - 0.05, v_lo + 0.02), P(a + 0.05, v_lo + 0.02), P(a + 0.03, v_lo + 0.09), P(a - 0.03, v_lo + 0.09)] for a in np.linspace(-0.7, 0.7, 5)], smooth=False)
    art = GP(art, wedges, "#4a2416", seed=nx(), rough=0.5)
    art = wash(art, lring * np.clip(u, 0, 1), WOOD_D, 0.5, seed=nx())
    # head: ellipse of stretched hide + braided rattan rim
    head = shapes(W, H, [ellipse_pts(*P(0, 0), r * 1.0, r * ell, 40, tilt)])
    art = GP(art, head, HIDE, "#d8b986", seed=nx(), rough=0.8, streak=0.4)
    art = wash(art, head * np.clip((fbm(W, H, nx(), 10, 3) - 0.4) * 2, 0, 1), HIDE_D, 0.35, seed=nx())
    art = wash(art, head * radial(W, H, *P(-0.25, -0.05), r * 0.6), "#f6e6c4", 0.5, seed=nx())
    rim = np.clip(head - shapes(W, H, [ellipse_pts(*P(0, 0.004), r * 0.88, r * ell * 0.82, 40, tilt)]), 0, 1)
    art = GP(art, rim, RATTAN, RATTAN_D, seed=nx(), rough=0.5, streak=0.6)
    art = wash(art, rim * (np.sin(np.arctan2(yy - P(0, 0)[1], (xx - P(0, 0)[0]) * ell) * 46) > 0.2), RATTAN_D, 0.6, seed=nx())
    return art


if "tifa" in PARTS:
    W, H = 620, 760
    nx = Seq(100)
    rng = random.Random(7)
    art = blank(W, H)
    floor = shapes(W, H, [ellipse_pts(330, 712, 250, 30, 30)])
    art = wash(art, gaussian_filter(floor, 10), "#2a1a14", 0.35, seed=nx())
    art = tifa(art, W, H, 418, 120, 560, 92, rng, nx, tilt=0.12)
    art = tifa(art, W, H, 238, 60, 640, 108, rng, nx, tilt=-0.04)
    save(art, f"{OUT}/tifa.webp", max_w=440, quality=80)
    show(art, "mt-tifa")
    clear()


def clove_cluster(art, W, H, x, y, s, rng, nx, n=9, ang=-1.57):
    """Cluster of clove buds: thin pink-red stalks fanning out, each bud a tapering hypanthium with a round head."""
    items, heads = [], []
    for i in range(n):
        a = ang + (i - n / 2) / n * 1.5 + rng.uniform(-0.1, 0.1)
        L = s * rng.uniform(0.6, 1.0)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        mx, my = x + math.cos(a) * L * 0.25, y + math.sin(a) * L * 0.25
        items.append(([(x, y), (mx, my)], s * 0.05, None))
        items.append(([(mx + math.cos(a) * L * 0.75 * t, my + math.sin(a) * L * 0.75 * t) for t in np.linspace(0, 1, 8)], s * 0.1, (0.9, 0.0)))
        hx, hy = ex + math.cos(a) * s * 0.1, ey + math.sin(a) * s * 0.1
        heads.append((hx, hy, s * 0.08))
    stalk = strokes(W, H, items)
    art = GP(art, stalk, "#c4463a", "#a83a32", seed=nx(), rough=0.5)
    art = wash(art, stalk * grad(W, H, x, y, x + math.cos(ang) * s, y + math.sin(ang) * s), "#7a8a3a", 0.35, seed=nx())
    hm = circles(W, H, heads)
    art = GP(art, hm, "#e0796a", "#d45c50", seed=nx(), rough=0.4)
    art = wash(art, hm * np.roll(np.roll(1 - gaussian_filter(hm, 1.2), 1, 0), 1, 1), "#8a2a24", 0.4, seed=nx())
    # four little sepals around each head
    sep = strokes(W, H, [([(hx - r * 1.1 * math.cos(a), hy - r * 1.1 * math.sin(a)), (hx - r * 0.4 * math.cos(a), hy - r * 0.4 * math.sin(a))], r * 0.6, (0.0, 0.6))
                         for (hx, hy, r), a in [(hd, ang + (i - n / 2) / n * 1.5) for i, hd in enumerate(heads)]])
    art = GP(art, sep, "#9a2e28", seed=nx(), rough=0.4)
    return art


def nutmeg(art, W, H, x, y, r, rng, nx):
    """Split nutmeg fruit: pale yellow halves, the red lacy mace over a dark glossy seed."""
    fr = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 1.1, 24), rng, 1, 0.02)])
    art = GP(art, fr, "#e8d27a", "#d9b95a", seed=nx(), rough=1.0)
    art = relief(art, fr, r * 0.3, 0.45, light="#fff2b8", dark="#9a7a2a", seed=nx())
    gap = shapes(W, H, [[(x - r * 0.18, y - r * 1.0), (x + r * 0.28, y - r * 0.6), (x + r * 0.38, y + r * 0.2), (x + r * 0.1, y + r * 0.95), (x - r * 0.3, y + r * 0.5), (x - r * 0.4, y - r * 0.3)]])
    art = GP(art, gap * fr, "#3a1e14", seed=nx(), rough=0.6)
    seed_m = shapes(W, H, [ellipse_pts(x, y - r * 0.02, r * 0.32, r * 0.5, 20, 0.3)]) * gap
    art = GP(art, seed_m, "#4a2618", "#5a2e1c", seed=nx(), rough=0.5)
    art = wash(art, seed_m * radial(W, H, x - r * 0.12, y - r * 0.2, r * 0.25), "#a46a44", 0.6, seed=nx())
    mace = []
    for k in range(16):
        a = rng.uniform(0, math.pi); sx, sy = x + rng.uniform(-r * 0.3, r * 0.3), y + rng.uniform(-r * 0.45, r * 0.45)
        L = r * rng.uniform(0.25, 0.5)
        mace.append((curve([(sx - math.cos(a) * L, sy - math.sin(a) * L), (sx + rng.uniform(-r * 0.08, r * 0.08), sy), (sx + math.cos(a + 0.4) * L, sy + math.sin(a + 0.4) * L)], 14), r * 0.055, (0.2, 0.2)))
    mm = strokes(W, H, mace) * seed_m
    art = GP(art, mm, "#c8262a", "#e0402e", seed=nx(), rough=0.4)
    return art


def clove_leaf(art, W, H, x, y, L, ang, rng, nx):
    return jungle_leaf(art, W, H, x, y, L, L * 0.22, ang, rng, nx, cols=(LEAF, LEAF_D), vein=LEAF_D, light=LEAF_L, bend=rng.uniform(-0.1, 0.1))


if "sprig" in PARTS:
    W, H = 640, 520
    nx = Seq(400)
    rng = random.Random(9)
    art = blank(W, H)
    br = strokes(W, H, [(curve([(20, 480), (180, 380), (360, 300), (560, 230)], 40), 9, (0.0, 0.5)), (curve([(250, 345), (300, 250), (330, 170)], 20), 5, (0.0, 0.6))])
    art = GP(art, br, "#5a3a22", "#7a5030", seed=nx(), rough=0.8)
    for x, y, L, a in [(120, 420, 190, -2.2), (200, 370, 170, 0.5), (330, 310, 200, -1.0), (400, 280, 160, 0.6), (520, 245, 130, -0.6), (300, 220, 140, -2.4), (90, 440, 150, 0.9)]:
        art = clove_leaf(art, W, H, x, y, L, a, rng, nx)
    art = clove_cluster(art, W, H, 330, 172, 70, rng, nx, n=12, ang=-1.5)
    art = clove_cluster(art, W, H, 560, 232, 58, rng, nx, n=8, ang=-0.7)
    art = nutmeg(art, W, H, 200, 430, 52, rng, nx)
    art = nutmeg(art, W, H, 440, 330, 40, rng, nx)
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=80)
    show(art, "mt-sprig")
    clear()

if "twig" in PARTS:
    W, H = 460, 100
    nx = Seq(600)
    rng = random.Random(3)
    art = blank(W, H)
    br = strokes(W, H, [(curve([(16, 60), (120, 50), (230, 56), (340, 50), (444, 60)], 40), 3.0, (0.1, 0.1))])
    art = GP(art, br, "#5a3a22", seed=nx(), rough=0.5)
    for x, a in [(60, -0.5), (110, 2.6), (350, -0.6), (400, 2.7), (160, -2.5), (300, -0.8)]:
        art = clove_leaf(art, W, H, x, 54, 54, a, rng, nx)
    art = clove_cluster(art, W, H, 230, 58, 30, rng, nx, n=7, ang=-1.57)
    save(art, f"{OUT}/twig.webp", max_w=380, quality=82)
    show(art, "mt-twig")
    clear()

if "sea" in PARTS:
    W, H = 840, 520
    nx = Seq(800)
    rng = random.Random(21)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    HZ = 210
    art = blank(W, H)
    sky = painted_sky(W, HZ + 6, [(0, "#9fd6dd"), (0.7, "#d9eee6"), (1.0, "#f4efd9")], seed=nx())
    art[:HZ + 6] = sky
    for cy_, x0, x1 in [(70, 60, 380), (110, 470, 800), (150, 200, 420)]:
        cl = shapes(W, H, [deform(ellipse_pts((x0 + x1) / 2, cy_, (x1 - x0) / 2, 18, 18), rng, 2, 0.08)])
        art = wash(art, gaussian_filter(cl, 5), "#ffffff", 0.75, seed=nx())
    # far islands (Ambon's hills across the bay)
    for pts, col in [([(-20, HZ), (60, HZ - 40), (150, HZ - 62), (240, HZ - 30), (330, HZ)], "#6f9e8e"), ([(520, HZ), (600, HZ - 28), (700, HZ - 50), (800, HZ - 22), (860, HZ)], "#7fa99a")]:
        isl = shapes(W, H, [deform(pts, rng, 2, 0.02)])
        art = GP(art, isl, col, mix(col, "#4a7a6a", 0.4), seed=nx(), rough=2.0)
        art = wash(art, isl * grad(W, H, 0, HZ - 60, 0, HZ), "#a9cdbd", 0.35, seed=nx())
    sea = (yy >= HZ).astype(np.float32)
    art = wash(art, sea, "#6cc9c4", 1.0, seed=nx(), col2="#5cc0bf")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, H), TURQ, 0.8, seed=nx())
    art = wash(art, sea * grad(W, H, 0, HZ + 120, 0, H) * np.clip((fbm(W, H, nx(), 50, 3) - 0.3) * 1.8, 0, 1), TURQ_D, 0.6, seed=nx())
    # reef patches & sun sparkle
    reef = sea * np.clip((fbm(W, H, nx(), 40, 3) - 0.62) * 4, 0, 1) * grad(W, H, 0, HZ + 40, 0, HZ + 200)
    art = wash(art, reef, "#9fe0cf", 0.28, seed=nx())
    gl = strokes(W, H, [([(x, y), (x + rng.uniform(10, 36), y)], rng.uniform(1.2, 2.6), (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(HZ + 6, H - 20)) for _ in range(120)]]) * sea
    art = wash(art, gl, "#ffffff", 0.75, seed=nx())
    # near island with white beach and palms on the right
    isl = shapes(W, H, [[(520, 330), (600, 290), (700, 270), (800, 268), (860, 280), (860, 360), (520, 360)]])
    beach = shapes(W, H, [[(500, 338), (600, 318), (860, 322), (860, 372), (520, 366)]])
    art = GP(art, isl, "#3f7a4c", "#2f6340", seed=nx(), rough=2.0)
    art = wash(art, isl * np.clip((fbm(W, H, nx(), 14, 3) - 0.45) * 3, 0, 1), "#6aa265", 0.5, seed=nx())
    art = GP(art, beach, "#f4ead2", "#e8dcc0", seed=nx(), rough=1.6)
    shore = strokes(W, H, [(curve([(505, 352), (620, 336), (860, 340)], 20), 6, (0.2, 0.0))])
    art = wash(art, shore, "#bfeee6", 0.6, seed=nx())
    for px, ph, ln in [(640, 120, -0.3), (700, 150, 0.2), (770, 130, -0.1)]:
        trunk = strokes(W, H, [(curve([(px, 326), (px + ln * ph * 0.5, 326 - ph * 0.55), (px + ln * ph, 326 - ph)], 16), 5, (0.0, 0.6))])
        art = GP(art, trunk, "#6a5034", seed=nx(), rough=0.6)
        tx, ty = px + ln * ph, 326 - ph
        fr = strokes(W, H, [(curve([(tx, ty), (tx + math.cos(a) * 30, ty + math.sin(a) * 30 - 6), (tx + math.cos(a) * 58, ty + math.sin(a) * 58 + 10)], 14), 7, (0.1, 0.7)) for a in np.linspace(-2.9, -0.2, 7)])
        art = GP(art, fr, "#2f6a3a", "#3f7f45", seed=nx(), rough=0.8)
    # a small fishing outrigger on the water
    hull = shapes(W, H, [[(250, 360), (330, 360), (318, 372), (262, 372)]])
    art = GP(art, hull, "#c0442e", seed=nx(), rough=0.5)
    oars = strokes(W, H, [([(240, 378), (340, 378)], 2.5, None), ([(268, 362), (262, 378)], 2, None), ([(312, 362), (318, 378)], 2, None)])
    art = GP(art, oars, "#4a3020", seed=nx(), rough=0.4)
    art = fade_edges(art, top=50)
    save(art, f"{OUT}/sea.webp", max_w=720, quality=76)
    show(art, "mt-sea")
    clear()

if "ikat" in PARTS:
    TW, TH = 216, 288
    pal = ["#4a1c17", CREAM, RUST, BLACK, OCHRE]
    yy, xx = np.mgrid[0:TH, 0:TW]
    motif = np.zeros((TH, TW), np.int32)
    # warp stripes at the tile edge (they meet the neighbour tile into one band)
    for x0, x1, c in [(0, 9, 3), (9, 12, 4), (12, 15, 1), (15, 24, 3), (24, 27, 2), (189, 192, 2), (192, 201, 3), (201, 204, 1), (204, 207, 4), (207, 216, 3)]:
        motif[:, x0:x1] = c
    cx = 108
    for cy in (72, 216):
        dx, dy = np.abs(xx - cx), np.abs(yy - cy)
        d = dx / 70 + dy / 62
        motif[(d < 1) & (d > 0.84)] = 1
        motif[(d < 0.84) & (d > 0.66)] = 2
        motif[(d < 0.66) & (d > 0.54)] = 1
        motif[(d < 0.54)] = 3
        motif[(d < 0.3) & (d > 0.18)] = 4
        motif[d < 0.1] = 1
        # hooks (kait) off the diamond tips, left and right
        for sgn in (-1, 1):
            hx = cx + sgn * 72
            hook = (np.abs(yy - cy) < 5) & (np.abs(xx - hx) < 10)
            hook |= (np.abs(xx - (hx + sgn * 6)) < 4) & (yy - cy > -18) & (yy - cy < 0)
            motif[hook & (xx > 27) & (xx < 189)] = 1
    # chevron rows between the diamonds
    for cy in (0, 144, 288):
        ch = (np.abs((yy - cy) - (np.abs(xx - cx) * 0.28)) < 4) & (np.abs(xx - cx) < 70)
        motif[ch] = 4
        ch2 = (np.abs((yy - cy) + 10 - (np.abs(xx - cx) * 0.28)) < 2.5) & (np.abs(xx - cx) < 56)
        motif[ch2] = 1
    tile = ikat(TW, TH, motif, pal, seed=5, warp=3, bleed=6.0)
    save_rgb(tile, f"{OUT}/ikat.webp", quality=80)
    show(tile, "mt-ikat")
    big = np.concatenate([np.concatenate([tile, tile], 1)] * 2, 0)
    show(big, "mt-ikat-2x2")
    clear()
