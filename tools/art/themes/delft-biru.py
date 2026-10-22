"""Delft Biru — hand-painted Delft blue-and-white tiles with an Indies-heritage touch: tin-glaze crackle, cobalt
'trek' outlines + pooled washes, quarter-fleuron corners that join across tiles; scenes of a kincir (windmill), a
sailing ship (kapal layar), a tulip vase; a 9-slice tile frame, a brush-scroll divider, a glazed vase and a wall tile.
Run: python3 -I delft-biru.py [part ...]  parts: mill ship flower frame border vase wall
Assets -> public/themes/art/delft-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b5_lib import *

OUT = outdir("delft-biru")
PARTS = sys.argv[1:] or ["mill", "ship", "flower", "frame", "border", "vase", "wall"]
S = 560


def corners(art, W, H, nx, size=0.16, inset=0.0):
    """Quarter-fleuron at every corner (they join into a full ornament when tiles meet)."""
    k = size * W
    for cx, cy, sx, sy in ((inset, inset, 1, 1), (W - inset, inset, -1, 1), (inset, H - inset, 1, -1), (W - inset, H - inset, -1, -1)):
        P = lambda u, v: (cx + sx * u * k, cy + sy * v * k)
        art = dab(art, W, H, [[P(0, 0), P(.42, 0), P(.38, .16), P(.16, .38), P(0, .42)]], nx())
        # three leaves: along both edges + the diagonal, ending in curls
        leaf = lambda pts, wd: (pts, wd, (0.05, 0.7))
        items = [
            leaf(curve([P(.4, .06), P(.7, .1), P(.95, .04), P(1.12, .14)], 18), 7),
            leaf(curve([P(.06, .4), P(.1, .7), P(.04, .95), P(.14, 1.12)], 18), 7),
            leaf(curve([P(.3, .3), P(.55, .5), P(.78, .62), P(.92, .55)], 18), 8),
            leaf(curve([P(.3, .3), P(.5, .55), P(.62, .78), P(.55, .92)], 18), 8),
        ]
        art = trek(art, W, H, items, nx(), col=COB)
        art = dab(art, W, H, [ellipse_pts(*P(.96, .5), k * .05, k * .05, 8), ellipse_pts(*P(.5, .96), k * .05, k * .05, 8)], nx())
    return art


def roundel(art, W, H, nx, r=0.37):
    c = W / 2
    pts = arc_pts(c, c, r * W, 0, math.tau * 1.02, 60)
    art = trek(art, W, H, [(pts, 3.2, None)], nx(), col=COB)
    return art


def tile_base(seed):
    art, m = glaze_tile(S, seed)
    return art, m


def finish(art, m):
    """Keep paint on the tile, faint glaze gloss over everything."""
    art[..., 3] = np.maximum(art[..., 3] * 0 + m, 0) * 1.0
    return art


def paint_on(tile, m, paint):
    """Composite the painted layer onto the glazed tile (paint soaks into the glaze a little)."""
    out = over(tile, paint)
    out[..., 3] = m
    return out


def sky_streaks(p, nx, rng, y0, y1, clip):
    """Horizontal loaded-brush strokes of thin cobalt for the sky (fading upward)."""
    c = S / 2
    items = []
    for y in np.arange(y1, y0, -14):
        k = (y - y0) / (y1 - y0)
        x0 = c - 200 + rng.uniform(0, 40); x1 = c + 200 - rng.uniform(0, 40)
        items.append(([(x0, y + rng.uniform(-3, 3)), ((x0 + x1) / 2, y + rng.uniform(-4, 4)), (x1, y + rng.uniform(-3, 3))], 9 + 6 * k, (.2, .3)))
    m = strokes(S, S, items) * clip
    return cobalt_wash(p, m * .55, nx(), density=.32, rough=3, bloom=.3)


def birds(art, W, H, nx, spots):
    items = []
    for x, y, s in spots:
        items.append(([(x - s, y - s * .3), (x - s * .4, y - s * .45), (x, y)], 2.2, (0.0, 0.3)))
        items.append(([(x, y), (x + s * .45, y - s * .5), (x + s, y - s * .35)], 2.2, (0.3, 0.0)))
    return trek(art, W, H, items, nx(), col=COB)


if "mill" in PARTS:
    nx = Seq(30100); rng = random.Random(3)
    tile, m = tile_base(11)
    p = blank(S, S)
    p = corners(p, S, S, nx)
    p = roundel(p, S, S, nx)
    c = S / 2
    clip = circles(S, S, [(c, c, S * .35)])
    # sky wash + cloud
    p = sky_streaks(p, nx, rng, 150, 250, clip)
    cloud = shapes(S, S, [deform(ellipse_pts(c + 92, 196, 46, 14, 12), rng, 2, .05), deform(ellipse_pts(c + 64, 186, 30, 12, 10), rng, 2, .05)])
    p = knockout(p, cloud, .95, 2)
    # land + water
    land = shapes(S, S, [[(c - 200, 352), (c - 120, 340), (c - 20, 336), (c + 80, 342), (c + 200, 350), (c + 200, 372), (c - 200, 372)]]) * clip
    p = cobalt_wash(p, land, nx(), density=.62)
    water = [([(c - 150 + rng.uniform(-8, 8), y), (c + 150 + rng.uniform(-8, 8), y)], 2.0, (.2, .2)) for y in range(384, 440, 11)]
    p = trek(p, S, S, [(it[0], it[1] * rng.uniform(.8, 1.2), it[2]) for it in water], nx(), col=COB_W, density=.7)
    # trees left
    for tx, ty, tr in ((c - 118, 322, 22), (c - 92, 314, 26), (c - 140, 330, 15)):
        p = dab(p, S, S, [deform(ellipse_pts(tx, ty, tr, tr * 1.1, 12), rng, 2, .06)], nx(), col=COB_W, density=.75)
        p = trek(p, S, S, [([(tx, ty + tr), (tx, ty + tr + 16)], 3, None)], nx())
    # little Indies house right (pointed roof)
    p = cobalt_wash(p, poly(S, S, [(c + 84, 340), (c + 84, 312), (c + 128, 312), (c + 128, 340)]), nx(), density=.3)
    p = dab(p, S, S, [[(c + 76, 314), (c + 106, 290), (c + 136, 314)]], nx(), col=COB)
    p = trek(p, S, S, [([(c + 84, 340), (c + 84, 312), (c + 128, 312), (c + 128, 340)], 2.4, None), ([(c + 102, 340), (c + 102, 324), (c + 110, 324), (c + 110, 340)], 2, None)], nx())
    # windmill tower + cap
    tower = poly(S, S, [(c - 34, 344), (c - 20, 214), (c + 20, 214), (c + 34, 344)])
    p = cobalt_wash(p, tower, nx(), density=.5)
    p = tint(p, side_light(tower, 10, 0, 6) * 1.5, COB[0], .55, seed=nx())
    p = trek(p, S, S, [([(c - 34, 344), (c - 20, 214)], 3.4, None), ([(c + 34, 344), (c + 20, 214)], 3.4, None),
                       ([(c - 9, 344), (c - 9, 316), (c + 9, 316), (c + 9, 344)], 2.6, None),
                       ([(c - 4, 262), (c + 6, 262)], 4, None), ([(c - 36, 300), (c + 36, 300)], 2.6, None)], nx())
    p = dab(p, S, S, [[(c - 26, 216), (c - 18, 196), (c, 186), (c + 18, 196), (c + 26, 216)]], nx())
    # four sails (lattice), turned a little
    hub = (c, 202)
    items, sails = [], []
    for k in range(4):
        a = math.radians(28 + k * 90)
        dx, dy = math.cos(a), math.sin(a)
        nxv, nyv = -dy, dx
        L = 128
        items.append(([hub, (hub[0] + dx * L, hub[1] + dy * L)], 3.6, (0.0, 0.1)))
        q = [(hub[0] + dx * 22, hub[1] + dy * 22), (hub[0] + dx * L, hub[1] + dy * L),
             (hub[0] + dx * L + nxv * 26, hub[1] + dy * L + nyv * 26), (hub[0] + dx * 22 + nxv * 26, hub[1] + dy * 22 + nyv * 26)]
        sails.append(q)
        items.append(([q[1], q[2], q[3]], 2.2, None))
        for t in np.linspace(.15, .9, 6):
            a1 = (hub[0] + dx * (22 + (L - 22) * t), hub[1] + dy * (22 + (L - 22) * t))
            items.append(([a1, (a1[0] + nxv * 26, a1[1] + nyv * 26)], 1.5, None))
        items.append(([(hub[0] + dx * 22 + nxv * 13, hub[1] + dy * 22 + nyv * 13), (hub[0] + dx * L + nxv * 13, hub[1] + dy * L + nyv * 13)], 1.4, None))
    p = cobalt_wash(p, shapes(S, S, sails, smooth=False), nx(), density=.22, rough=1.5, bloom=.1)
    p = trek(p, S, S, items, nx())
    p = dab(p, S, S, [ellipse_pts(*hub, 7, 7, 10)], nx(), col=COB_D)
    p = birds(p, S, S, nx, [(c - 70, 176, 10), (c - 48, 160, 7), (c + 140, 232, 6)])
    art = paint_on(tile, m, p)
    preview(art, "delft-mill")
    save(art, f"{OUT}/mill.webp", max_w=320, quality=80)
    clear()

if "ship" in PARTS:
    nx = Seq(30200); rng = random.Random(5)
    tile, m = tile_base(23)
    p = blank(S, S)
    p = corners(p, S, S, nx)
    p = roundel(p, S, S, nx)
    c = S / 2
    clip = circles(S, S, [(c, c, S * .35)])
    p = sky_streaks(p, nx, rng, 140, 232, clip)
    # sea
    sea = shapes(S, S, [[(c - 200, 352), (c + 200, 352), (c + 200, 470), (c - 200, 470)]]) * clip
    p = cobalt_wash(p, sea * .55, nx(), density=.38, rough=4, bloom=.3)
    waves = []
    for row, y in enumerate(range(360, 452, 15)):
        x0 = c - 160 + (row % 2) * 14
        for x in range(int(x0), int(c + 160), 34):
            if (x - c) ** 2 + (y - c) ** 2 < (S * .33) ** 2:
                waves.append((arc_pts(x + 10, y + 4, 11, math.pi * 1.1, math.pi * 1.9, 8), 2.2, (.1, .3)))
    p = trek(p, S, S, waves, nx(), col=COB)
    # hull
    hull = shapes(S, S, [[(c - 112, 318), (c + 104, 312), (c + 126, 300), (c + 98, 352), (c - 86, 356), (c - 118, 334)]])
    p = cobalt_wash(p, hull, nx(), density=.75, col=COB)
    p = tint(p, side_light(hull, 0, 8, 6) * 1.4, COB_D[0], .6, seed=nx())
    p = trek(p, S, S, [(curve([(c - 108, 330), (c, 330), (c + 112, 318)], 16), 2.2, None)], nx(), col=("#e9eef7", "#e9eef7"), density=.5)
    # masts + square sails
    items = []
    sails = []
    for mx, top, scale in ((c - 56, 176, .8), (c + 6, 142, 1.0), (c + 66, 186, .75)):
        items.append(([(mx, 316), (mx, top)], 3.0, None))
        y = top + 16
        for k, (w_, h_) in enumerate(((34, 30), (44, 38), (52, 44))):
            w2, h2 = w_ * scale, h_ * scale
            q = [(mx - w2, y), (mx + w2, y), (mx + w2 * 1.08, y + h2), (mx - w2 * 1.08, y + h2)]
            q = [(qx, qy + 6 * math.sin((qx - mx) / w2 * 1.4)) for qx, qy in q]
            sails.append(deform(q, rng, 1, .02))
            items.append((curve([(mx - w2 * 1.08, y + h2), (mx, y + h2 + 7), (mx + w2 * 1.08, y + h2)], 10), 2.2, None))
            items.append(([(mx - w2, y), (mx + w2, y)], 2.6, None))
            y += h2 + 6
        items.append(([(mx, top), (mx + 22, top + 6), (mx, top + 10)], 2.0, None))
    p = cobalt_wash(p, shapes(S, S, sails), nx(), density=.3, rough=1.6)
    for q in sails:
        p = tint(p, side_light(shapes(S, S, [q]), 8, 0, 5) * 1.3, COB_W[0], .55, seed=nx())
    p = trek(p, S, S, items, nx())
    # rigging
    rig = [([(c - 120, 306), (c - 56, 176)], 1.1, None), ([(c - 56, 176), (c + 6, 142)], 1.1, None),
           ([(c + 6, 142), (c + 66, 186)], 1.1, None), ([(c + 66, 186), (c + 124, 300)], 1.1, None)]
    p = trek(p, S, S, rig, nx(), col=COB, density=.7)
    # far island with palms (Indies coast)
    isl = shapes(S, S, [deform(ellipse_pts(c - 136, 352, 40, 9, 12), rng, 1, .05)]) * clip
    p = cobalt_wash(p, isl, nx(), density=.5)
    for px_, ph in ((c - 150, 40), (c - 128, 32)):
        p = trek(p, S, S, [(curve([(px_, 350), (px_ + 3, 330), (px_ + 6, 350 - ph)], 10), 2.6, None)] +
                 [(curve([(px_ + 6, 350 - ph), (px_ + 6 + math.cos(a) * 12, 350 - ph + math.sin(a) * 8 - 3), (px_ + 6 + math.cos(a) * 20, 350 - ph + math.sin(a) * 12 + 5)], 8), 2.6, (0, .7)) for a in (-2.8, -2.2, -.9, -.3)], nx())
    p = birds(p, S, S, nx, [(c + 126, 190, 9), (c + 108, 208, 6)])
    art = paint_on(tile, m, p)
    preview(art, "delft-ship")
    save(art, f"{OUT}/ship.webp", max_w=320, quality=80)
    clear()

if "flower" in PARTS:
    nx = Seq(30300); rng = random.Random(7)
    tile, m = tile_base(37)
    p = blank(S, S)
    p = corners(p, S, S, nx)
    c = S / 2
    # vase (baluster)
    vase = shapes(S, S, [[(c - 26, 300), (c - 40, 330), (c - 52, 372), (c - 44, 408), (c - 22, 424), (c + 22, 424), (c + 44, 408), (c + 52, 372), (c + 40, 330), (c + 26, 300)]])
    p = cobalt_wash(p, vase, nx(), density=.45)
    p = tint(p, side_light(vase, 12, 0, 8) * 1.4, COB[0], .6, seed=nx())
    p = trek(p, S, S, [(curve([(c - 26, 300), (c - 40, 330), (c - 52, 372), (c - 44, 408), (c - 22, 424), (c + 22, 424), (c + 44, 408), (c + 52, 372), (c + 40, 330), (c + 26, 300)], 40), 3, None),
                       ([(c - 30, 300), (c + 30, 300)], 4, None), (curve([(c - 50, 366), (c, 374), (c + 50, 366)], 12), 2, None)], nx())
    # stems
    stems = [((c - 8, 300), (c - 70, 220), (c - 96, 176)), ((c, 300), (c + 2, 210), (c - 4, 150)), ((c + 8, 300), (c + 66, 226), (c + 100, 184)),
             ((c - 4, 300), (c - 40, 250), (c - 46, 232)), ((c + 4, 300), (c + 40, 252), (c + 52, 236))]
    p = trek(p, S, S, [(curve(list(st), 14), 2.6, (0, .1)) for st in stems], nx())
    # tulips on the long stems, small rosettes on the short ones
    for (x, y), ang, sz in (((c - 96, 176), -.5, 1.0), ((c - 4, 150), 0.0, 1.1), ((c + 100, 184), .5, 1.0)):
        cu = []
        for k, off in enumerate((-.42, 0, .42)):
            cu.append(petal_pts(x, y + 6, 46 * sz, 15 * sz, -math.pi / 2 + ang + off, n=14))
        p = dab(p, S, S, cu[:1] + cu[2:], nx(), col=COB_W, density=.7)
        p = dab(p, S, S, cu[1:2], nx(), col=COB, density=.85)
        p = trek(p, S, S, [(petal_pts(x, y + 6, 46 * sz, 15 * sz, -math.pi / 2 + ang + o, n=14) + [petal_pts(x, y + 6, 46 * sz, 15 * sz, -math.pi / 2 + ang + o, n=14)[0]], 1.6, None) for o in (-.42, .42)], nx(), col=COB_D, density=.75)
    for (x, y) in ((c - 46, 232), (c + 52, 236)):
        p = dab(p, S, S, [petal_pts(x, y, 16, 7, a, n=10) for a in np.linspace(0, math.tau, 6)[:-1]], nx(), col=COB_W, density=.7)
        p = dab(p, S, S, [ellipse_pts(x, y, 5, 5, 8)], nx(), col=COB_D)
    # leaves
    lv = []
    for (x, y, L, a) in ((c - 40, 262, 46, -2.5), (c + 36, 268, 44, -.7), (c - 6, 236, 36, -1.9), (c + 12, 196, 34, -1.1), (c - 76, 214, 30, -2.9)):
        lv.append(petal_pts(x, y, L, 10, a, n=12, cup=.4))
    p = dab(p, S, S, lv, nx(), col=COB, density=.8)
    # small dot border ring
    p = dab(p, S, S, [ellipse_pts(c + math.cos(a) * 200, c + math.sin(a) * 200, 3.4, 3.4, 8) for a in np.linspace(0, math.tau, 40)[:-1]], nx(), col=COB, density=.7)
    art = paint_on(tile, m, p)
    preview(art, "delft-flower")
    save(art, f"{OUT}/flower.webp", max_w=320, quality=80)
    clear()

if "frame" in PARTS:
    # 9-slice frame: transparent centre, cobalt double rule + joined corner fleurons. Slice = 150 of 600.
    F = 600
    nx = Seq(30400); rng = random.Random(9)
    p = blank(F, F)
    band = shapes(F, F, [[(0, 0), (F, 0), (F, F), (0, F)]], smooth=False) - shapes(F, F, [[(34, 34), (F - 34, 34), (F - 34, F - 34), (34, F - 34)]], smooth=False)
    p = cobalt_wash(p, np.clip(band, 0, 1), nx(), density=.9, col=COB, rough=1.4, bloom=.05, edge=.4)
    inner = [([(48, y), (F - 48, y)], 2.4, None) for y in (48, F - 48)] + [([(x, 48), (x, F - 48)], 2.4, None) for x in (48, F - 48)]
    p = trek(p, F, F, inner, nx(), col=COB)
    # white glaze dots on the band
    dots = [(t, 17) for t in range(60, F - 50, 30)]
    pts = []
    for t, d in dots:
        pts += [ellipse_pts(t, d, 3.2, 3.2, 8), ellipse_pts(t, F - d, 3.2, 3.2, 8), ellipse_pts(d, t, 3.2, 3.2, 8), ellipse_pts(F - d, t, 3.2, 3.2, 8)]
    p = knockout(p, shapes(F, F, pts), .8, .6)
    # corner fleurons inside
    for cx, cy, sx, sy in ((34, 34, 1, 1), (F - 34, 34, -1, 1), (34, F - 34, 1, -1), (F - 34, F - 34, -1, -1)):
        P = lambda u, v: (cx + sx * u, cy + sy * v)
        p = dab(p, F, F, [[P(0, 0), P(44, 0), P(40, 18), P(18, 40), P(0, 44)]], nx())
        p = trek(p, F, F, [(curve([P(26, 26), P(54, 48), P(84, 58), P(100, 48)], 16), 6, (0.05, .7)),
                           (curve([P(26, 26), P(48, 54), P(58, 84), P(48, 100)], 16), 6, (0.05, .7))], nx(), col=COB)
        p = dab(p, F, F, [ellipse_pts(*P(104, 42), 4.5, 4.5, 8), ellipse_pts(*P(42, 104), 4.5, 4.5, 8)], nx())
    preview(p, "delft-frame")
    save_full(p, f"{OUT}/frame.webp", size=(400, 400), quality=82)
    clear()

if "border" in PARTS:
    W, H = 640, 96
    nx = Seq(30500); rng = random.Random(11)
    p = blank(W, H)
    c = W / 2; y = H / 2
    p = dab(p, W, H, [petal_pts(c, y, 26, 9, a, n=12) for a in (0, math.pi / 2, math.pi, -math.pi / 2)], nx())
    p = dab(p, W, H, [ellipse_pts(c, y, 6, 6, 10)], nx(), col=COB_D)
    items = []
    for sx in (1, -1):
        items.append((curve([(c + sx * 30, y), (c + sx * 90, y - 16), (c + sx * 160, y + 10), (c + sx * 230, y - 8), (c + sx * 300, y + 2)], 40), 5, (0.05, .9)))
        for k, (u, d) in enumerate(((90, -1), (160, 1), (230, -1))):
            items.append((curve([(c + sx * u, y - 16 * (d < 0) + 10 * (d > 0) * .8), (c + sx * (u + 14), y + d * 22), (c + sx * (u + 30), y + d * 18)], 10), 3.6, (0.05, .6)))
    p = trek(p, W, H, items, nx(), col=COB)
    lv = []
    for sx in (1, -1):
        for u, d in ((60, 1), (126, -1), (196, 1), (262, -1)):
            lv.append(petal_pts(c + sx * u, y + d * 4, 22, 6, (math.pi if sx < 0 else 0) + d * sx * .9 + (0 if sx > 0 else 0), n=10))
    p = dab(p, W, H, lv, nx(), col=COB_W, density=.75)
    p = dab(p, W, H, [ellipse_pts(c + sx * 304, y + 2, 3.5, 3.5, 8) for sx in (1, -1)], nx())
    preview(p, "delft-border")
    save(p, f"{OUT}/border.webp", max_w=400, quality=82)
    clear()

if "vase" in PARTS:
    # Glazed white vase painted with cobalt bands and a flower — standalone object
    W, H = 420, 560
    nx = Seq(30600); rng = random.Random(13)
    c = W / 2
    outline_pts = [(c - 34, 60), (c - 40, 70), (c - 36, 110), (c - 70, 170), (c - 128, 280), (c - 138, 360), (c - 118, 440), (c - 70, 496), (c - 60, 520),
                   (c + 60, 520), (c + 70, 496), (c + 118, 440), (c + 138, 360), (c + 128, 280), (c + 70, 170), (c + 36, 110), (c + 40, 70), (c + 34, 60)]
    body = shapes(W, H, [outline_pts])
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(c + 14, 524, 150, 14, 20)])
    art = G(art, shadow, "#2b3550", seed=nx(), density=.28, edge=.05, bloom=0, rough=3, feather=6)
    g, _ = glaze_tile(W, 51, bevel=False, radius=0)
    g = g[:H] if g.shape[0] >= H else np.pad(g, ((0, H - g.shape[0]), (0, 0), (0, 0)), mode="reflect")
    gl = g.copy(); gl[..., 3] = body
    art = over(art, gl)
    art = tint(art, side_light(body, 22, 0, 18) * 1.3, "#aeb9cf", .7, seed=nx())
    art = tint(art, side_light(body, -14, -6, 10) * 1.1, "#ffffff", .7, seed=nx())
    # painted decoration
    p = blank(W, H)
    rings = [(curve([(c - 38, 104), (c, 110), (c + 38, 104)], 10), 6, None), (curve([(c - 66, 176), (c, 186), (c + 66, 176)], 14), 4, None),
             (curve([(c - 118, 448), (c, 462), (c + 118, 448)], 20), 5, None), (curve([(c - 64, 504), (c, 512), (c + 64, 504)], 12), 6, None)]
    p = trek(p, W, H, rings, nx(), col=COB)
    p = cobalt_wash(p, shapes(W, H, [[(c - 34, 62), (c + 34, 62), (c + 38, 100), (c - 38, 100)]]), nx(), density=.6)
    # bouquet painted on the belly
    for (x, y), a, s_ in (((c - 46, 266), -.5, .8), ((c + 4, 238), 0, .95), ((c + 52, 272), .5, .8)):
        p = trek(p, W, H, [(curve([(c, 420), (x + (c - x) * .4, 340), (x, y + 18)], 12), 2.2, None)], nx())
        cu = [petal_pts(x, y + 6, 40 * s_, 13 * s_, -math.pi / 2 + a + o, n=14) for o in (-.42, 0, .42)]
        p = dab(p, W, H, [cu[0], cu[2]], nx(), col=COB_W, density=.7)
        p = dab(p, W, H, [cu[1]], nx(), col=COB, density=.85)
    p = dab(p, W, H, [petal_pts(x, y, 30, 8, a, n=12, cup=.3) for x, y, a in ((c - 20, 360, -2.6), (c + 20, 352, -.5), (c - 8, 318, -2.0), (c + 14, 300, -1.0))], nx(), col=COB, density=.8)
    # little dot rows
    p = dab(p, W, H, [ellipse_pts(c + t, 196 + abs(t) * .12, 3, 3, 8) for t in range(-60, 61, 15)], nx(), col=COB, density=.8)
    p[..., 3] *= body
    art = over(art, p)
    # glaze gloss highlight
    hl = strokes(W, H, [(curve([(c - 96, 300), (c - 104, 360), (c - 92, 420)], 12), 10, (.3, .3))]) * body
    art = tint(art, gaussian_filter(hl, 4), "#ffffff", .65, seed=nx())
    preview(art, "delft-vase")
    save(art, f"{OUT}/vase.webp", max_w=300, quality=82)
    clear()

if "wall" in PARTS:
    # Seamless tiled wall: 2x2 plain glazed tiles, grout lines, faint corner fleurons joining at the grout crossings.
    T = 256
    W = 2 * T
    nx = Seq(30700)
    wall = np.zeros((W, W, 4), np.float32)
    grout = np.ones((W, W, 4), np.float32); grout[..., :3] = np.array(hex_rgb("#dfe3ea"), np.float32)
    wall = grout
    for i in range(2):
        for j in range(2):
            t, mm = glaze_tile(T - 4, 61 + i * 2 + j, crack=.1, radius=4)
            sub = wall[i * T + 2:i * T + T - 2, j * T + 2:j * T + T - 2]
            wall[i * T + 2:i * T + T - 2, j * T + 2:j * T + T - 2] = over(sub, t)
    p = blank(W, W)
    # fleurons at the four tile crossings (centred on the grout cross; wrap via offset)
    for (cx, cy) in ((0, 0), (T, 0), (0, T), (T, T), (W, 0), (0, W), (W, W), (W, T), (T, W)):
        if 0 <= cx <= W and 0 <= cy <= W:
            pts = [petal_pts(cx, cy, 30, 9, a + math.pi / 4, n=12) for a in np.linspace(0, math.tau, 5)[:-1]]
            p = dab(p, W, W, pts, nx(), col=COB_W, density=.45)
            p = dab(p, W, W, [ellipse_pts(cx + math.cos(a) * 40, cy + math.sin(a) * 40, 4, 4, 8) for a in np.linspace(0, math.tau, 5)[:-1]], nx(), col=COB_W, density=.45)
    p[..., 3] *= .65
    wall = over(wall, p)
    wall[..., 3] = 1
    preview(wall, "delft-wall")
    save_rgb(wall, f"{OUT}/wall.webp", size=(320, 320), quality=74)
    clear()
