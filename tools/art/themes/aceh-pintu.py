"""Aceh Pintu — black, red, green and yellow with gold: carved pintu Aceh doorway (lintel with tulak angin gable +
repeatable jamb), kerawang Gayo satin-stitch band tile on black cloth, rumah Krong Bade stilt house (gouache +
watercolour), 8-point bungong medallion (foil + silk) and a divider. No figures; geometry, flora, architecture only.
Run: python3 -I aceh-pintu.py [part ...]  parts: lintel jamb kerawang krong medallion divider."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a1_lib import *

OUT = outdir("aceh-pintu")
PARTS = sys.argv[1:] or ["lintel", "jamb", "kerawang", "krong", "medallion", "divider"]
BLK = "#121010"
WOOD, WOOD_D, WOOD_L = "#4a2c1a", "#24140b", "#6e4527"
RED, GRN, YEL, WHT = "#b8262a", "#2f7a3c", "#e2b337", "#efe6d2"
GOLD = "#cda14a"


def star8(cx, cy, r, inner=0.62, rot=0.0):
    pts = []
    for k in range(16):
        a = rot + k * math.pi / 8
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def bungong(W, H, cx, cy, r, n=8):
    """carved flower: n petals + round heart."""
    pet = [petal_pts(cx, cy, r, r * 0.3, k * math.tau / n, n=12) for k in range(n)]
    return shapes(W, H, pet), circles(W, H, [(cx, cy, r * 0.24)])


def relief(art, m, nx, base=WOOD_L, dark=WOOD_D):
    """raised carving on wood: light top-left edge, dark bottom-right."""
    art = GP(art, m, base, WOOD, seed=nx(), rough=0.8, streak=0.7, pad=8)
    hi = np.clip(m - np.roll(np.roll(m, 2, 0), 2, 1), 0, 1)
    lo = np.clip(m - np.roll(np.roll(m, -2, 0), -2, 1), 0, 1)
    art = over(art, flat(lo, dark, 0.7))
    art = over(art, flat(hi, "#b98a5a", 0.5))
    return art


if "lintel" in PARTS:
    W, H = 800, 330
    nx = Seq(50100); cx = W / 2
    beam = shapes(W, H, [[(0, 214), (W, 214), (W, 330), (0, 330)]], smooth=False)
    gable = shapes(W, H, [[(cx - 300, 222), (cx, 14), (cx + 300, 222)]], smooth=False)
    wood = np.maximum(beam, gable)
    art = GP(blank(W, H), wood, WOOD, WOOD_D, seed=nx(), rough=1.0, streak=1.0, pad=10)
    grain = wood * hatch(W, H, 0.0, 5, 0.1, nx(), 3.0)
    art = over(art, flat(grain, WOOD_D, 0.35))
    # gable: concentric painted triangles (red/green/yellow) + lattice of small diamonds (tulak angin)
    for k, (col, inset) in enumerate([(RED, 18), (YEL, 30), (GRN, 40), (BLK, 52)]):
        t = shapes(W, H, [[(cx - 300 + inset * 1.9, 222 - inset * 0.35), (cx, 14 + inset * 1.25), (cx + 300 - inset * 1.9, 222 - inset * 0.35)]], smooth=False)
        art = GP(art, t, col, seed=nx(), rough=0.7, pad=8)
    lat = []
    for row in range(7):
        y = 92 + row * 18
        half = (y - 14 - 66) / (208 - 66) * 230
        for x in np.arange(cx - half + 12, cx + half - 6, 22):
            lat.append([(x - 7, y), (x, y - 8), (x + 7, y), (x, y + 8)])
    latm = shapes(W, H, lat, smooth=False)
    art = GP(art, latm, YEL, "#f0cf6a", seed=nx(), rough=0.4, pad=6)
    art = over(art, flat(circles(W, H, [((p[0][0] + p[2][0]) / 2, p[0][1], 2.2) for p in lat]), RED, 0.95))
    # gable edge boards
    edge = polyline_mask(W, H, [[(cx - 304, 224), (cx, 10), (cx + 304, 224)]], 12, cap=False)
    art = relief(art, edge, nx)
    art = FO(art, polyline_mask(W, H, [[(cx - 300, 214), (cx, 22), (cx + 300, 214)]], 2.5, cap=False), GOLD, seed=nx(), emboss=0.5)
    # beam: carved bungong row between painted bands
    bands = shapes(W, H, [[(0, 222), (W, 222), (W, 232), (0, 232)], [(0, 312), (W, 312), (W, 322), (0, 322)]], smooth=False)
    art = GP(art, bands, RED, seed=nx(), rough=0.5, pad=6)
    art = GP(art, shapes(W, H, [[(0, 234), (W, 234), (W, 238), (0, 238)], [(0, 306), (W, 306), (W, 310), (0, 310)]], smooth=False), YEL, seed=nx(), rough=0.4, pad=6)
    flw, hearts, vines = np.zeros((H, W), np.float32), [], []
    for k, x in enumerate(range(40, W, 80)):
        p, h = bungong(W, H, x, 272, 26)
        flw = np.maximum(flw, p)
        hearts.append((x, 272))
        vines.append(curve([(x + 26, 272), (x + 40, 256 if k % 2 else 288), (x + 54, 272)], 14))
    vm = polyline_mask(W, H, vines, 4)
    art = relief(art, np.maximum(flw, vm), nx)
    art = GP(art, circles(W, H, [(x, y, 7) for x, y in hearts]), GRN, seed=nx(), rough=0.4, pad=6)
    art = FO(art, circles(W, H, [(x, y, 3) for x, y in hearts]), GOLD, seed=nx())
    # hanging fringe (gantung) under the beam: small carved drops
    drops = shapes(W, H, [petal_pts(x, 322, 18, 6, math.pi / 2, n=10) for x in range(20, W, 26)])
    art = relief(art, np.clip(drops - beam * 0, 0, 1), nx)
    preview(art, "ap-lintel", bg=BLK)
    save(art, f"{OUT}/lintel.webp", max_w=640, quality=80)
    clear()

if "jamb" in PARTS:
    W, H = 100, 360  # repeat-y
    nx = Seq(50200)
    post = np.ones((H, W), np.float32)
    art = GP(blank(W, H), post, WOOD, WOOD_D, seed=nx(), rough=0.0, streak=1.2, pad=0)
    art[..., 3] = 1
    art = over(art, flat(hatch(W, H, 1.5708, 6, 0.1, nx(), 3.0), WOOD_D, 0.3))
    # side painted bands
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for (x0, x1, col) in [(6, 12, RED), (12, 15, YEL), (85, 88, YEL), (88, 94, RED)]:
        m = ((xx >= x0) & (xx < x1)).astype(np.float32)
        art = over(art, flat(m, col, 0.95))
    # carved vertical sulur (vine) with bungong, period 180 -> seamless
    vine = [(50 + 18 * math.sin(y / 180 * math.tau), y) for y in range(-10, H + 11, 6)]
    vm = polyline_mask(W, H, [vine], 5)
    fl = np.zeros((H, W), np.float32); hearts = []
    for y in (45, 135, 225, 315):
        x = 50 + 18 * math.sin(y / 180 * math.tau)
        p, h = bungong(W, H, x, y, 17, 6)
        fl = np.maximum(fl, p); hearts.append((x, y))
    leaves = shapes(W, H, [petal_pts(50 + 18 * math.sin(y / 180 * math.tau), y, 20, 6, a, n=10) for y, a in [(0, 0.5), (90, 2.6), (180, 0.5), (270, 2.6), (360, 0.5)]])
    art = relief(art, np.maximum.reduce([vm, fl, leaves]), nx)
    art = GP(art, circles(W, H, [(x, y, 5) for x, y in hearts]), GRN, seed=nx(), rough=0.3, pad=4)
    art = FO(art, circles(W, H, [(x, y, 2.2) for x, y in hearts]), GOLD, seed=nx())
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/jamb.webp", quality=78)
    clear()

if "kerawang" in PARTS:
    # kerawang Gayo band (repeat-x): pucuk rebung triangles top/bottom, emun beriring cloud-scroll chain in the
    # middle, puter tali twisted rows, satin-stitched red/yellow/green/white on black cotton
    W, H = 288, 120
    nx = Seq(50300); cy = H / 2
    art = cloth_base(W, H, BLK, seed=nx(), cell=2.0, var=0.12)
    tri_t = [[(x, 0 + 6), (x + 24, 6), (x + 12, 26)] for x in range(-24, W + 24, 24)]
    tri_b = [[(x, H - 6), (x + 24, H - 6), (x + 12, H - 26)] for x in range(-24, W + 24, 24)]
    art = over(art, satin(shapes(W, H, tri_t, smooth=False), RED, seed=nx(), angle=1.2))
    art = over(art, satin(shapes(W, H, tri_b, smooth=False), RED, seed=nx(), angle=-1.2))
    inner_t = [[(x + 7, 8), (x + 17, 8), (x + 12, 18)] for x in range(-24, W + 24, 24)]
    inner_b = [[(x + 7, H - 8), (x + 17, H - 8), (x + 12, H - 18)] for x in range(-24, W + 24, 24)]
    art = over(art, satin(shapes(W, H, inner_t + inner_b, smooth=False), YEL, seed=nx(), angle=0.0))
    # puter tali: twisted rope rows (alternating short diagonals, green/white)
    ra, rb = [], []
    for x in range(-12, W + 12, 8):
        ra.append([(x, 34), (x + 6, 28)]); rb.append([(x, H - 34), (x + 6, H - 28)])
    art = over(art, satin(polyline_mask(W, H, ra + rb, 3.2, cap=False), GRN, seed=nx(), angle=0.9))
    # emun beriring: chain of S-scroll clouds, period 72
    sc_r, sc_y = [], []
    for k in range(-1, W // 72 + 2):
        x0 = k * 72
        sc_r.append(spiral_pts(x0 + 18, cy - 3, 14, 3, math.pi, 1.0, 30, 1))
        sc_r.append(spiral_pts(x0 + 54, cy + 3, 14, 3, 0, 1.0, 30, 1))
        sc_y.append(curve([(x0 + 4, cy - 3), (x0 + 36, cy + 10), (x0 + 68, cy + 3)], 20))
    art = over(art, satin(polyline_mask(W, H, sc_r, 5.0), YEL, seed=nx(), angle=0.3))
    art = over(art, satin(polyline_mask(W, H, sc_y, 3.0), WHT, seed=nx(), angle=1.2))
    dots = circles(W, H, [(k * 72 + 36, cy - 14, 3.2) for k in range(-1, W // 72 + 2)] + [(k * 72, cy + 14, 3.2) for k in range(-1, W // 72 + 2)])
    art = over(art, satin(dots, RED, seed=nx(), angle=0.0))
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/kerawang.webp", quality=82)
    clear()

if "krong" in PARTS:
    # rumah Krong Bade: long stilt house, steep rumbia roof, decorated gable, front stair; dusk wash + palms
    W, H = 900, 440
    nx = Seq(50400); rng = random.Random(3)
    art = blank(W, H)
    haze = shapes(W, H, [[(-20, 300), (W + 20, 296), (W + 20, 420), (-20, 420)]], smooth=False)
    art = G(art, haze, "#7c6b4a", "#4b5a3a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=10, feather=8)
    hx0, hx1, floor_y, wall_top = 230, 690, 300, 222
    roof = shapes(W, H, [[(hx0 - 56, wall_top + 14), (hx0 + 40, 60), (hx1 - 40, 60), (hx1 + 56, wall_top + 14)]], smooth=False)
    gable = shapes(W, H, [[(hx1 - 40, 60), (hx1 - 4, 60), (hx1 + 56, wall_top + 14), (hx1 + 14, wall_top + 14)]], smooth=False)
    wall = shapes(W, H, [[(hx0, wall_top), (hx1, wall_top), (hx1, floor_y), (hx0, floor_y)]], smooth=False)
    posts = polyline_mask(W, H, [[(x, floor_y), (x, 392)] for x in range(hx0 + 8, hx1, 46)], 9, cap=False)
    beams = polyline_mask(W, H, [[(hx0 - 6, floor_y + 4), (hx1 + 6, floor_y + 4)], [(hx0, 362), (hx1, 362)]], 6, cap=False)
    stair = polyline_mask(W, H, [[(hx0 + 120, floor_y + 6), (hx0 + 70, 394)], [(hx0 + 150, floor_y + 6), (hx0 + 100, 394)]] + [[(hx0 + 120 - t * 50, floor_y + 6 + t * 88), (hx0 + 150 - t * 50, floor_y + 6 + t * 88)] for t in (0.2, 0.4, 0.6, 0.8)], 4)
    shadow = shapes(W, H, [deform(ellipse_pts(470, 398, 330, 16, 18), rng, 1, 0.03)])
    art = G(art, shadow, "#1e140c", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=4, feather=5)
    art = GP(art, np.maximum.reduce([posts, beams, stair]), WOOD_D, WOOD, seed=nx(), rough=1.0, pad=8)
    art = GP(art, wall, WOOD, WOOD_D, seed=nx(), rough=1.0, streak=1.0)
    planks = wall * hatch(W, H, 1.5708, 9, 0.08, nx(), 0.6)
    art = over(art, flat(planks, WOOD_D, 0.5))
    # painted bands + windows on the wall
    for (y0, y1, col) in [(wall_top + 2, wall_top + 12, RED), (wall_top + 12, wall_top + 17, YEL), (floor_y - 16, floor_y - 10, GRN), (floor_y - 10, floor_y - 3, RED)]:
        art = GP(art, shapes(W, H, [[(hx0, y0), (hx1, y0), (hx1, y1), (hx0, y1)]], smooth=False), col, seed=nx(), rough=0.5, pad=6)
    wins = shapes(W, H, [[(x, 238), (x + 28, 238), (x + 28, 276), (x, 276)] for x in range(hx0 + 190, hx1 - 30, 64)], smooth=False)
    art = GP(art, wins, "#1a0f08", seed=nx(), rough=0.6, pad=6)
    art = GP(art, outline(wins, 3), YEL, seed=nx(), rough=0.4, pad=6)
    lat = polyline_mask(W, H, [[(x + 2, 238 + d), (x + 26, 238 + d)] for x in range(hx0 + 190, hx1 - 30, 64) for d in (12, 24)], 2)
    art = over(art, flat(lat * wins, YEL, 0.8))
    # roof: rumbia thatch, watercolour + dry strokes
    art = GP(art, roof, "#6b4f2c", "#4a341b", seed=nx(), rough=1.4, streak=1.2)
    art = G(art, roof * (0.4 + 0.6 * fbm(W, H, nx(), 40, 3)), "#8a6a3e", "#5e4526", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=4)
    th = roof * np.maximum(hatch(W, H, 1.35, 5, 0.2, nx(), 2.0), hatch(W, H, 1.5708, 22, 0.08, nx(), 1.0))
    art = over(art, flat(th * (0.5 + 0.5 * fbm(W, H, nx(), 12, 2)), "#2e1e0e", 0.7))
    hi_th = roof * hatch(W, H, 1.35, 7, 0.1, nx(), 2.5)
    art = over(art, flat(hi_th * fbm(W, H, nx(), 30, 2), "#b08a52", 0.45))
    fringe = polyline_mask(W, H, [[(x, wall_top + 12), (x - 3, wall_top + 24 + (x * 7) % 9)] for x in range(hx0 - 50, hx1 + 52, 5)], 2.4)
    art = over(art, flat(fringe, "#5e4526", 0.9))
    art = G(art, np.clip(roof - np.roll(gaussian_filter(roof, 4), -10, 0), 0, 1) * roof, "#2a1a0c", seed=nx(), density=0.6, edge=0, rough=1)
    # tulak angin gable: painted triangle with lattice
    art = GP(art, gable, WOOD, seed=nx(), rough=0.6, pad=6)
    for k, (col, s_) in enumerate([(RED, 0.82), (YEL, 0.66), (GRN, 0.48)]):
        gx, gy = hx1 + 14, wall_top - 30
        tri = [(gx + (hx1 - 40 - gx) * s_, gy + (60 - gy) * s_), (gx + (hx1 - 4 - gx) * s_, gy + (60 - gy) * s_), (gx + (hx1 + 56 - gx) * s_, gy + (wall_top + 14 - gy) * s_), (gx + (hx1 + 14 - gx) * s_, gy + (wall_top + 14 - gy) * s_)]
        art = GP(art, shapes(W, H, [tri], smooth=False), col, seed=nx(), rough=0.4, pad=6)
    ridge = polyline_mask(W, H, [[(hx0 + 34, 58), (hx1 - 34, 58)]], 7)
    art = GP(art, ridge, WOOD_D, seed=nx(), rough=0.5, pad=6)
    # palms and banana clumps (watercolour, behind/side)
    import _jw_lib as jw
    def coco(x, h, lean, seed):
        rr = random.Random(seed)
        top = (x + lean * h, 392 - h)
        items = [(curve([(x, 392), (x + lean * h * 0.3, 392 - h * 0.5), top], 24), 10, (0.0, 0.25))]
        for k in range(9):
            a = -math.pi + 0.2 + k * (math.pi - 0.4) / 8 + rr.gauss(0, 0.08)
            L = rr.uniform(90, 120)
            mid = (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.45 - 6)
            end = (top[0] + math.cos(a) * L * 1.1, top[1] + math.sin(a) * L * 0.25 + 62)
            fr = curve([top, mid, end], 24)
            items.append((fr, 4, (0.0, 0.6)))
            for j in range(3, len(fr) - 1, 2):
                (x0, y0), (x1, y1) = fr[j - 1], fr[j]
                ang = math.atan2(y1 - y0, x1 - x0)
                ll = 26 * (1 - j / len(fr)) + 8
                for sg in (-1, 1):
                    b = ang + sg * 1.0
                    items.append(([(x1, y1), (x1 + math.cos(b) * ll * 0.6, y1 + math.sin(b) * ll * 0.6 + ll * 0.25), (x1 + math.cos(b) * ll, y1 + math.sin(b) * ll + ll * 0.7)], 3.2, (0.0, 0.7)))
        return strokes(W, H, items)
    pm = np.maximum(coco(120, 300, 0.12, 4), coco(820, 260, -0.12, 8))
    art = G(art, pm, "#3f5a34", "#26391f", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=3)
    shrubs = shapes(W, H, [deform(ellipse_pts(x, 386, rx, 24, 12), rng, 2, 0.12) for x, rx in [(160, 70), (760, 80), (60, 50), (870, 50)]])
    art = G(art, shrubs, "#4e6b38", "#2c4423", seed=nx(), density=0.8, edge=0.45, bloom=0.35, rough=6)
    preview(art, "ap-krong", "#f3ead6")
    save(art, f"{OUT}/krong.webp", max_w=720, quality=80)
    clear()

if "medallion" in PARTS:
    W, H = 300, 300
    nx = Seq(50500); c = 150
    outer = shapes(W, H, [star8(c, c, 138, 0.74, math.pi / 8)], smooth=False)
    art = FO(blank(W, H), outer, GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    art = over(art, satin(shapes(W, H, [star8(c, c, 116, 0.74, math.pi / 8)], smooth=False), BLK, seed=nx(), angle=0.0, sheen=0.1))
    sq = shapes(W, H, [[(c - 70, c - 70), (c + 70, c - 70), (c + 70, c + 70), (c - 70, c + 70)], [(c, c - 99), (c + 99, c), (c, c + 99), (c - 99, c)]], smooth=False)
    art = over(art, satin(np.clip(sq - shapes(W, H, [star8(c, c, 74, 0.7)], smooth=False), 0, 1), RED, seed=nx(), angle=0.8))
    art = FO(art, outline(sq, 2.5), GOLD, seed=nx(), emboss=0.5)
    p, h = bungong(W, H, c, c, 62, 8)
    art = over(art, satin(p, GRN, seed=nx(), angle=1.3))
    art = FO(art, outline(p, 2.0), GOLD, seed=nx(), emboss=0.4)
    art = over(art, satin(circles(W, H, [(c, c, 18)]), YEL, seed=nx(), angle=0.0))
    art = FO(art, circles(W, H, [(c + math.cos(k * math.pi / 4 + math.pi / 8) * 128, c + math.sin(k * math.pi / 4 + math.pi / 8) * 128, 4) for k in range(8)]), "#f2d995", seed=nx())
    preview(art, "ap-medallion", bg=BLK)
    save(art, f"{OUT}/medallion.webp", max_w=180, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 600, 80
    nx = Seq(50600); cy = 40
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 4, 0, 1)[None, :]
    tl = [[(x, cy - 2), (x + 20, cy - 2), (x + 10, cy - 16)] for x in range(40, 250, 20)] + [[(x, cy - 2), (x + 20, cy - 2), (x + 10, cy - 16)] for x in range(350, 560, 20)]
    tb = [[(x + 10, cy + 2), (x + 30, cy + 2), (x + 20, cy + 16)] for x in range(30, 240, 20)] + [[(x + 10, cy + 2), (x + 30, cy + 2), (x + 20, cy + 16)] for x in range(340, 550, 20)]
    art = over(blank(W, H), satin(shapes(W, H, tl, smooth=False) * fade, RED, seed=nx(), angle=1.1))
    art = over(art, satin(shapes(W, H, tb, smooth=False) * fade, GRN, seed=nx(), angle=-1.1))
    st = shapes(W, H, [star8(300, cy, 30, 0.66, math.pi / 8)], smooth=False)
    art = FO(art, st, GOLD, seed=nx(), emboss=0.8)
    art = over(art, satin(shapes(W, H, [star8(300, cy, 18, 0.66, math.pi / 8)], smooth=False), RED, seed=nx(), angle=0.4))
    art = over(art, satin(circles(W, H, [(300, cy, 6)]), YEL, seed=nx()))
    preview(art, "ap-divider", bg=BLK)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
