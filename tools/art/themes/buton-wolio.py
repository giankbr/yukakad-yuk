"""Buton Wolio — gouache: the Benteng Keraton Buton on its hill (coursed limestone walls with crenellations and
bastions following the ridge), the Kamali / Malige palace (tall timber house whose storeys step outward, tiered
roofs), the Buton strait with Muna island beyond; a tenun Buton tile (bright red / yellow / green / black stripes
crossing into a check, woven thread by thread), a stone-wall divider and a palace emblem.
Run: python3 -I buton-wolio.py [part ...]   parts: keraton tenun wall malige
Assets -> public/themes/art/buton-wolio/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c1_lib import *

OUT = outdir("buton-wolio")
PARTS = sys.argv[1:] or ["keraton", "tenun", "wall", "malige"]
STONE, STONE_D, STONE_L = "#b9ab8e", "#7d705c", "#ddd2b8"
WOOD, WOOD_D, WOOD_L = "#5a3420", "#2e1a10", "#8a5434"
ROOF, ROOF_D = "#3a2c28", "#1f1716"
RED, YEL, GRN, BLK, WHT = "#c8202a", "#f2c21b", "#178a4a", "#191412", "#f4ecd8"
SEA, SEA_D = "#2e7fb0", "#1c5a86"
HILL, HILL_D, HILL_L = "#5f8a45", "#3e6532", "#9ab865"


def malige(art, W, H, cx, by, s, rng, nx):
    """Kamali/Malige: four storeys on a low stone base, each storey wider than the one below, roof skirts between,
    a steep top gable; painted timber with white-trimmed windows."""
    def P(u, v):
        return (cx + u * s, by + v * s)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = shapes(W, H, [[P(-0.62, 0), P(0.62, 0), P(0.6, -0.12), P(-0.6, -0.12)]], smooth=False)
    art = GP(art, base, STONE, STONE_L, seed=nx(), rough=1.0)
    stl = strokes(W, H, [([P(u, -0.12), P(u, -0.3)], s * 0.035, None) for u in np.linspace(-0.5, 0.5, 6)])
    art = GP(art, stl, WOOD_D, seed=nx(), rough=0.5)
    y = -0.3
    widths = [0.52, 0.6, 0.68, 0.74]
    heights = [0.34, 0.3, 0.28, 0.24]
    for i, (w, h) in enumerate(zip(widths, heights)):
        body = shapes(W, H, [[P(-w, y), P(w, y), P(w, y - h), P(-w, y - h)]], smooth=False)
        art = GP(art, body, WOOD, "#6a3e26", seed=nx(), rough=0.8, streak=1.0)
        seams = np.clip((np.abs(((xx - cx) / (s * 0.05)) % 1.0 - 0.5) * 2 - 0.86) * 7, 0, 1) * body
        art = wash(art, seams, WOOD_D, 0.5, seed=nx())
        art = wash(art, body * grad(W, H, cx - s * w, 0, cx + s * w, 0), "#1c0f08", 0.45, seed=nx())
        art = wash(art, body * (1 - grad(W, H, cx - s * w, 0, cx, 0)), WOOD_L, 0.3, seed=nx())
        nwin = 3 + i
        wins = [[P(u - 0.05, y - h * 0.25), P(u + 0.05, y - h * 0.25), P(u + 0.05, y - h * 0.78), P(u - 0.05, y - h * 0.78)] for u in np.linspace(-w * 0.7, w * 0.7, nwin)]
        wm = shapes(W, H, wins, smooth=False)
        trim = np.clip(gaussian_filter(wm, 1.2) * 3, 0, 1) - wm
        art = wash(art, np.clip(trim, 0, 1), WHT, 0.85, seed=nx())
        art = GP(art, wm, "#24140c", seed=nx(), rough=0.4)
        # roof skirt over this storey (the next storey sits on it)
        skirt = shapes(W, H, [[P(-w - 0.12, y - h + 0.02), P(w + 0.12, y - h + 0.02), P(w * 0.9, y - h - 0.1), P(-w * 0.9, y - h - 0.1)]], smooth=False)
        art = GP(art, skirt, ROOF, "#4a3a34", seed=nx(), rough=0.8, streak=1.0)
        art = wash(art, skirt * grad(W, H, 0, by + (y - h - 0.1) * s, 0, by + (y - h) * s), ROOF_D, 0.4, seed=nx())
        y = y - h - 0.06
    # top gable roof
    top = shapes(W, H, [[P(-0.92, y + 0.02), P(0, y - 0.7), P(0.92, y + 0.02)]], smooth=False)
    art = GP(art, top, ROOF, "#4a3a34", seed=nx(), rough=1.0, streak=1.2)
    rows = np.clip((np.abs(((yy - by) / (s * 0.05)) % 1.0 - 0.5) * 2 - 0.8) * 5, 0, 1) * top
    art = wash(art, rows, ROOF_D, 0.45, seed=nx())
    art = wash(art, top * grad(W, H, cx - s * 0.9, 0, cx + s * 0.9, 0), ROOF_D, 0.35, seed=nx())
    gable = shapes(W, H, [[P(-0.34, y + 0.02), P(0, y - 0.32), P(0.34, y + 0.02)]], smooth=False)
    art = GP(art, gable, WOOD, seed=nx(), rough=0.6)
    sun = shapes(W, H, [[P(-0.12, y - 0.02), P(0, y - 0.18), P(0.12, y - 0.02)]], smooth=False)
    art = GP(art, sun, YEL, "#e0a818", seed=nx(), rough=0.4)
    crest = strokes(W, H, [([P(-0.03, y - 0.7), P(0, y - 0.84)], s * 0.03, None)])
    art = GP(art, crest, ROOF_D, seed=nx(), rough=0.4)
    return art


def wall_run(art, W, H, pts, h, rng, nx, crenel=True, light_side=-1):
    """Fort wall along a polyline (ground points), height h px: coursed stone with crenellations on top."""
    top = [(x, y - h) for x, y in pts]
    poly = pts + top[::-1]
    m = shapes(W, H, [poly], smooth=False)
    if crenel:
        cr = []
        for (x0, y0), (x1, y1) in zip(top[:-1], top[1:]):
            L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / (h * 0.55)))
            for k in range(n):
                t0 = (k + 0.15) / n; t1 = (k + 0.6) / n
                ax, ay = x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0
                bx, by_ = x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1
                cr.append([(ax, ay + 1), (bx, by_ + 1), (bx, by_ - h * 0.28), (ax, ay - h * 0.28)])
        m = np.clip(m + shapes(W, H, cr, smooth=False), 0, 1)
    art = GP(art, m, STONE, "#c4b698", seed=nx(), rough=1.0, streak=0.6)
    mort, tone = stone_courses(W, H, m, course=max(4, h * 0.16), brick=max(9, h * 0.4), seed=nx())
    art = wash(art, tone * (tone > 0.6) * m, STONE_L, 0.35, seed=nx())
    art = wash(art, tone * (tone < 0.3) * m, STONE_D, 0.3, seed=nx())
    art = wash(art, mort, "#6a5e4c", 0.55, seed=nx())
    art = wash(art, m * np.clip((fbm(W, H, nx(), 20, 3) - 0.55) * 3, 0, 1), "#7a8a5a", 0.3, seed=nx())  # moss
    art = wash(art, m * grad(W, H, 0, min(y for _, y in top), 0, max(y for _, y in pts)), STONE_D, 0.3, seed=nx())
    return art


if "keraton" in PARTS:
    W, H = 860, 660
    nx = Seq(100)
    rng = random.Random(41)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    HZ = 250
    art[:HZ + 4] = painted_sky(W, HZ + 4, [(0, "#8ec3e0"), (0.7, "#d3e7ee"), (1.0, "#f5ecd6")], seed=nx())
    for cy_, x0, x1 in [(70, 80, 380), (120, 520, 840)]:
        cl = shapes(W, H, [deform(ellipse_pts((x0 + x1) / 2, cy_, (x1 - x0) / 2, 22, 18), rng, 2, 0.08)])
        art = wash(art, gaussian_filter(cl, 4), "#ffffff", 0.75, seed=nx())
    # Muna across the strait
    muna = shapes(W, H, [deform([(-20, HZ + 2), (90, HZ - 24), (230, HZ - 36), (380, HZ - 18), (460, HZ + 2)], rng, 2, 0.02)])
    art = GP(art, muna, "#7d9fb0", "#6d90a4", seed=nx(), rough=2.0)
    sea = ((yy >= HZ) & (yy < 420)).astype(np.float32)
    art = wash(art, sea, SEA, 1.0, seed=nx(), col2="#3a8bbb")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, 420), SEA_D, 0.4, seed=nx())
    gl = strokes(W, H, [([(x, y), (x + rng.uniform(10, 30), y)], 1.5, (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(HZ + 4, 400)) for _ in range(80)]]) * sea
    art = wash(art, gl, "#e8f3fa", 0.75, seed=nx())
    # small boats in the strait
    for bx, by_, bs in [(140, 300, 20), (600, 285, 14)]:
        hull = shapes(W, H, [[(bx - bs, by_), (bx + bs, by_), (bx + bs * 0.7, by_ + bs * 0.25), (bx - bs * 0.7, by_ + bs * 0.25)]])
        sail = shapes(W, H, [[(bx - 2, by_ - 1), (bx - 2, by_ - bs * 1.3), (bx + bs * 0.7, by_ - 1)]], smooth=False)
        art = GP(art, hull, "#5a3a24", seed=nx(), rough=0.4)
        art = GP(art, sail, "#f4ecd8", seed=nx(), rough=0.4)
    # the hill of Wolio
    hill_pts = [(-20, H + 20), (-20, 420), (120, 380), (260, 340), (420, 318), (560, 326), (700, 350), (880, 392), (880, H + 20)]
    hill = shapes(W, H, [hill_pts])
    art = GP(art, hill, HILL, "#6f9a4e", seed=nx(), rough=2.5, streak=1.0)
    art = wash(art, hill * np.clip((fbm(W, H, nx(), 30, 3) - 0.5) * 2.5, 0, 1), HILL_D, 0.4, seed=nx())
    art = wash(art, hill * np.clip((fbm(W, H, nx(), 18, 3) - 0.55) * 3, 0, 1), HILL_L, 0.35, seed=nx())
    # trees dotting the slope
    trees = []
    for _ in range(70):
        tx = rng.uniform(-10, W + 10); ty = rng.uniform(380, 640)
        if 300 < tx < 600 and ty < 470:
            continue
        r = rng.uniform(8, 18) * (0.6 + (ty - 380) / 400)
        trees.append(deform(ellipse_pts(tx, ty, r * 1.2, r, 10), rng, 1, 0.1))
    tm = shapes(W, H, trees) * hill
    art = GP(art, tm, "#3a6430", "#4a7a3a", seed=nx(), rough=1.6)
    art = relief(art, tm, 4, 0.5, light="#a8c46a", dark="#1f3a1c", seed=nx())
    # back wall along the ridge (far), then the palace, then the long front wall with a bastion
    art = wall_run(art, W, H, [(150, 382), (300, 352), (430, 342), (600, 352), (740, 372)], 22, rng, nx)
    art = malige(art, W, H, 455, 470, 120, rng, nx)
    art = wall_run(art, W, H, [(-20, 540), (140, 500), (300, 488), (380, 492)], 44, rng, nx)
    art = wall_run(art, W, H, [(520, 492), (640, 498), (780, 520), (880, 548)], 44, rng, nx)
    # gate (lawa) between the front walls
    gate = shapes(W, H, [[(380, 494), (520, 494), (520, 438), (500, 420), (400, 420), (380, 438)]], smooth=False)
    art = GP(art, gate, STONE, STONE_L, seed=nx(), rough=1.0)
    mort, tone = stone_courses(W, H, gate, course=8, brick=18, seed=nx())
    art = wash(art, mort, "#6a5e4c", 0.5, seed=nx())
    door = shapes(W, H, [[(430, 494), (470, 494), (470, 456), (450, 444), (430, 456)]], smooth=False)
    art = GP(art, door, "#3a2618", seed=nx(), rough=0.5)
    # bastion (baluara) on the left: rounded tower
    bas = shapes(W, H, [ellipse_pts(150, 520, 52, 16, 24)]) + shapes(W, H, [[(98, 520), (202, 520), (198, 452), (102, 452)]], smooth=False)
    bas = np.clip(bas, 0, 1)
    art = GP(art, bas, STONE, "#c4b698", seed=nx(), rough=1.0)
    mort, tone = stone_courses(W, H, bas, course=8, brick=18, seed=nx())
    art = wash(art, mort, "#6a5e4c", 0.55, seed=nx())
    art = wash(art, bas * grad(W, H, 98, 0, 202, 0), STONE_D, 0.45, seed=nx())
    cren = shapes(W, H, [[(x, 454), (x + 12, 454), (x + 12, 440), (x, 440)] for x in range(100, 200, 22)], smooth=False)
    art = GP(art, cren, STONE, seed=nx(), rough=0.6)
    cannon = strokes(W, H, [([(186, 470), (226, 462)], 7, (0.0, 0.0))])
    art = GP(art, cannon, "#2a2624", seed=nx(), rough=0.4)
    # foreground grass and flowers of the hill
    fg = grass_tufts(W, H, 560, 660, 360, rng, 10, 30, 0.2, 2.0)
    art = GP(art, fg, "#4a7a3a", "#5f8a45", seed=nx(), rough=0.8)
    art = wash(art, grass_tufts(W, H, 580, 660, 200, rng, 10, 26, 0.3, 1.6), HILL_L, 0.5, seed=nx())
    art = fade_edges(art, top=60)
    save(art, f"{OUT}/keraton.webp", max_w=720, quality=76)
    show(art, "bw-keraton")
    clear()

if "tenun" in PARTS:
    # stripe sequence (thread groups): red ground with yellow, green, black bands and white pinstripes
    seq = [(0, 10), (4, 1), (0, 2), (4, 1), (0, 10), (3, 3), (1, 5), (3, 3), (0, 6), (2, 6), (4, 1), (2, 6), (0, 6)]
    pal = [RED, YEL, GRN, BLK, WHT]
    idx = []
    for c, k in seq:
        idx += [c] * k
    n = len(idx)  # threads per repeat
    idx = np.array(idx)
    # pattern: weft stripes dominate (weft-faced), warp crosses in thin checks every other pick
    rows = n * 2; cols = n * 2
    yy, xx = np.mgrid[0:rows, 0:cols]
    weft = idx[(yy // 2) % n]; warp = idx[(xx // 2) % n]
    p = np.where(((yy + xx) % 2 == 0) & (warp != 0), warp, weft)
    tile = weave_cells(p.astype(np.int32), pal, cell=3, seed=11, float_len=2, fibre=0.08)
    save_rgb(tile, f"{OUT}/tenun.webp", quality=82)
    show(tile, "bw-tenun")
    big = np.concatenate([np.concatenate([tile, tile], 1)] * 2, 0)
    show(big, "bw-tenun-2x2")
    clear()

if "wall" in PARTS:
    W, H = 480, 76
    nx = Seq(600)
    rng = random.Random(5)
    art = blank(W, H)
    art = wall_run(art, W, H, [(4, 66), (476, 66)], 34, rng, nx)
    save(art, f"{OUT}/wall.webp", max_w=400, quality=82)
    show(art, "bw-wall")
    clear()

if "malige" in PARTS:
    W, H = 300, 380
    nx = Seq(800)
    rng = random.Random(8)
    art = blank(W, H)
    ground = shapes(W, H, [ellipse_pts(150, 352, 120, 14, 24)])
    art = GP(art, ground, HILL, HILL_D, seed=nx(), rough=1.5)
    art = malige(art, W, H, 150, 350, 120, rng, nx)
    save(art, f"{OUT}/malige.webp", max_w=200, quality=84)
    show(art, "bw-malige")
    clear()
