"""Lomba Layangan — bright gouache poster of a beach kite festival (made-up community event): a clear sky with soft
clouds and small far-off kites, a turquoise sea, a sand beach with umbul-umbul flag poles and a panitia tent; separate
kites each with its own string (they sway from the anchor): wajik diamond with bow tail, ikan fish with streamers,
modern rainbow delta, box kite; a pennant bunting, a string spool (tin can) and a mini diamond kite for timeline nodes.
Run: python3 -I lomba-layangan.py [part ...]   parts: scene wajik ikan delta kotak bunting spool
Assets -> public/themes/art/lomba-layangan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s4_lib import *  # noqa

OUT = outdir("lomba-layangan")
PARTS = sys.argv[1:] or ["scene", "wajik", "ikan", "delta", "kotak", "bunting", "mini"]
RED, YEL, BLUE, GRN, PINK, ORA, WHT, NAVY = "#e2452f", "#f6b73c", "#2c7bd1", "#34a368", "#d94e8f", "#f08a2c", "#fbf6ec", "#1d2b4f"
SPAR = "#8a5a2e"


def gp(art, mask, c1, c2=None, seed=1, rough=2.0, streak=0.7):
    return GP(art, mask, c1, c2, seed=seed, rough=rough, streak=streak)


def string(W, H, p0, p1, sag=0.08, width=2.0):
    """Kite line from the bridle p0 down to the anchor p1, bowing with the wind."""
    pts = []
    for k in range(60):
        t = k / 59
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        x += math.sin(math.pi * t) * (p1[1] - p0[1]) * sag
        pts.append((x, y))
    return strokes(W, H, [(pts, width, (0.0, 0.0))])


def ribbon(W, H, p0, length, amp, waves, width, ang=math.pi / 2, phase=0.0):
    pts = []
    for k in range(80):
        t = k / 79
        d = t * length
        off = math.sin(t * waves * math.tau + phase) * amp * (0.3 + 0.7 * t)
        x = p0[0] + math.cos(ang) * d - math.sin(ang) * off
        y = p0[1] + math.sin(ang) * d + math.cos(ang) * off
        pts.append((x, y))
    return pts, strokes(W, H, [(pts, width, (0.05, 0.4))])


def outline(art, W, H, mask, col=NAVY, w=2.2, nx=None):
    edge = np.clip(gaussian_filter(mask, 0.8) - gaussian_filter(np.clip(mask - np.clip(mask - np.roll(mask, 2, 0), 0, 1) - np.clip(mask - np.roll(mask, 2, 1), 0, 1) - np.clip(mask - np.roll(mask, -2, 0), 0, 1) - np.clip(mask - np.roll(mask, -2, 1), 0, 1), 0, 1), 0.8), 0, 1)
    return GP(art, np.clip(edge * 1.6, 0, 1), col, seed=nx() if nx else 3, rough=0.8, streak=0.3)


def finish(art, name, max_w):
    prev_rgba(art, f"ll-{name}", bg="#9fd3f0")
    return save_a(art, f"{OUT}/{name}.webp", max_w=max_w, quality=84)


def part_wajik():
    W, H = 420, 1200
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    c = (210, 190)
    top, bot, lft, rgt = (210, 40), (210, 360), (95, 160), (325, 160)
    q = [[top, rgt, c], [rgt, bot, c], [bot, lft, c], [lft, top, c]]
    cols = [RED, YEL, RED, YEL]
    for k, (pts, col) in enumerate(zip(q, cols)):
        art = gp(art, poly(W, H, pts), col, mix_hex(col, "#000000", 0.08), seed=nx())
    # white centre diamond + stripes
    cd = [(210, 120), (262, 165), (210, 245), (158, 165)]
    art = gp(art, poly(W, H, cd), WHT, seed=nx(), rough=1.2)
    art = gp(art, poly(W, H, [(210, 145), (236, 168), (210, 210), (184, 168)]), BLUE, seed=nx(), rough=1.0)
    body = poly(W, H, [top, rgt, bot, lft])
    art = outline(art, W, H, body, nx=nx)
    art = gp(art, strokes(W, H, [([top, bot], 4, None), (curve([lft, (210, 146), rgt], 20), 4, None)]), SPAR, seed=nx(), rough=0.6, streak=0.3)
    # bow tail
    pts, rm = ribbon(W, H, bot, 420, 26, 2.2, 3.0)
    art = gp(art, rm, NAVY, seed=nx(), rough=0.6, streak=0.3)
    bows = []
    for t in (0.18, 0.36, 0.54, 0.72, 0.9):
        x, y = pts[int(t * 79)]
        bows += [[(x, y), (x - 22, y - 12), (x - 22, y + 12)], [(x, y), (x + 22, y - 12), (x + 22, y + 12)]]
    art = gp(art, shapes(W, H, bows[::2]), BLUE, seed=nx(), rough=1)
    art = gp(art, shapes(W, H, bows[1::2]), GRN, seed=nx(), rough=1)
    art = over(solid_layer(string(W, H, (210, 190), (210, H - 2), sag=-0.05, width=2), "#ffffff", 0.9), art)
    return finish(art, "wajik", 210)


def part_ikan():
    W, H = 560, 1200
    nx = Seq(300); rng = random.Random(2)
    art = blank(W, H)
    cx, cy = 200, 200
    bodyp = [(cx - 150, cy), (cx - 100, cy - 70), (cx + 10, cy - 88), (cx + 110, cy - 50), (cx + 150, cy), (cx + 110, cy + 50), (cx + 10, cy + 88), (cx - 100, cy + 70)]
    body = poly(W, H, bodyp, smooth=True)
    tail = poly(W, H, [(cx + 135, cy), (cx + 230, cy - 90), (cx + 205, cy), (cx + 230, cy + 90)], smooth=True)
    finT = poly(W, H, [(cx - 40, cy - 80), (cx + 10, cy - 140), (cx + 70, cy - 70)], smooth=True)
    finB = poly(W, H, [(cx - 20, cy + 80), (cx + 20, cy + 128), (cx + 60, cy + 70)], smooth=True)
    for m, col in ((finT, PINK), (finB, PINK), (tail, ORA)):
        art = gp(art, m, col, mix_hex(col, "#ffffff", 0.15), seed=nx())
    art = gp(art, body, ORA, YEL, seed=nx())
    # scales: rows of arcs, belly lighter, bands of pink
    sc = []
    for row in range(-3, 4):
        for col in range(-3, 4):
            x = cx - 40 + col * 30 + (row % 2) * 15; y = cy + row * 22
            sc.append((arc_pts(x, y, 15, 0.3, math.pi - 0.3, 10), 2.2, None))
    art = gp(art, strokes(W, H, sc) * gaussian_filter(body, 1) * (xgrad(W, H, cx - 100, cx - 60)), RED, seed=nx(), rough=0.6, streak=0.3)
    art = gp(art, body * (ygrad(W, H, cy + 30, cy + 70)), WHT, YEL, seed=nx(), rough=1)
    head = body * (1 - xgrad(W, H, cx - 92, cx - 88))
    art = gp(art, head, RED, seed=nx(), rough=1)
    art = gp(art, circles(W, H, [(cx - 105, cy - 18, 17)]), WHT, seed=nx(), rough=0.6)
    art = gp(art, circles(W, H, [(cx - 102, cy - 18, 8)]), NAVY, seed=nx(), rough=0.5)
    art = outline(art, W, H, np.clip(body + tail + finT + finB, 0, 1), nx=nx)
    for k, col in enumerate((BLUE, GRN, PINK)):
        pts, rm = ribbon(W, H, (cx + 215, cy + (k - 1) * 40), 230, 16, 1.4, 7, ang=0.75 - k * 0.1, phase=k)
        art = gp(art, rm, col, seed=nx(), rough=0.6, streak=0.3)
    art = over(solid_layer(string(W, H, (cx - 20, cy + 40), (W // 2, H - 2), sag=0.06, width=2), "#ffffff", 0.9), art)
    return finish(art, "ikan", 260)


def part_delta():
    W, H = 480, 1200
    nx = Seq(500)
    art = blank(W, H)
    apex = (240, 40); L, R = (30, 260), (450, 260)
    tri = poly(W, H, [apex, R, (240, 230), L])
    cols = [RED, ORA, YEL, GRN, BLUE, PINK]
    for k, col in enumerate(cols):
        x0 = 30 + 420 * k / 6; x1 = 30 + 420 * (k + 1) / 6
        art = gp(art, tri * rect(W, H, x0, 0, x1 + 1, H), col, mix_hex(col, "#000000", 0.07), seed=nx(), rough=0.6)
    keel = poly(W, H, [(240, 140), (275, 300), (205, 300)])
    art = gp(art, keel, WHT, seed=nx(), rough=0.8)
    art = outline(art, W, H, np.clip(tri + keel, 0, 1), nx=nx)
    art = gp(art, strokes(W, H, [([apex, (240, 230)], 4, None), ([(90, 220), (390, 220)], 3, None)]), SPAR, seed=nx(), rough=0.5, streak=0.3)
    for k, (x, col) in enumerate(((150, BLUE), (330, RED))):
        pts, rm = ribbon(W, H, (x, 236), 360, 18, 2.0, 6, phase=k * 2)
        art = gp(art, rm, col, seed=nx(), rough=0.5, streak=0.3)
    art = over(solid_layer(string(W, H, (240, 300), (W // 2, H - 2), sag=-0.07, width=2), "#ffffff", 0.9), art)
    return finish(art, "delta", 240)


def part_kotak():
    W, H = 360, 1200
    nx = Seq(700)
    art = blank(W, H)
    # two cells of a box kite in 3/4 view: front faces + side faces, spars at the corners
    def cell(y0, y1, cf, cs):
        front = poly(W, H, [(90, y0), (220, y0 - 14), (220, y1 - 14), (90, y1)])
        side = poly(W, H, [(220, y0 - 14), (290, y0 + 6), (290, y1 + 6), (220, y1 - 14)])
        return front, side
    f1, s1 = cell(50, 150, BLUE, "#1f5ea6")
    f2, s2 = cell(250, 350, BLUE, "#1f5ea6")
    art = gp(art, f1, YEL, seed=nx()); art = gp(art, s1, ORA, seed=nx())
    art = gp(art, f2, RED, seed=nx()); art = gp(art, s2, "#b8341f", seed=nx())
    stripes = np.clip(f1 * (np.sin(np.arange(W)[None, :] / 8.0) > 0.6) + f2 * (np.sin(np.arange(W)[None, :] / 8.0) > 0.6), 0, 1)
    art = gp(art, stripes, WHT, seed=nx(), rough=0.6)
    art = outline(art, W, H, np.clip(f1 + s1 + f2 + s2, 0, 1), nx=nx)
    sp = strokes(W, H, [([(90, 40), (90, 360)], 4, None), ([(220, 26), (220, 346)], 4, None), ([(290, 46), (290, 366)], 4, None), ([(90, 200), (290, 210)], 3, None)])
    art = gp(art, sp, SPAR, seed=nx(), rough=0.5, streak=0.3)
    art = over(solid_layer(string(W, H, (150, 200), (W // 2, H - 2), sag=0.05, width=2), "#ffffff", 0.9), art)
    return finish(art, "kotak", 180)


def part_bunting():
    """Pennant bunting (divider): a sagging cord with triangular cloth flags."""
    W, H = 760, 150
    nx = Seq(900)
    art = blank(W, H)
    cord = [(x, 20 + 34 * math.sin(math.pi * x / W)) for x in range(0, W + 1, 8)]
    art = gp(art, strokes(W, H, [(cord, 3, None)]), NAVY, seed=nx(), rough=0.5, streak=0.3)
    cols = [RED, YEL, BLUE, GRN, ORA, PINK]
    flags = [[] for _ in cols]
    n = 13
    for k in range(n):
        x = 20 + (W - 40) * k / (n - 1)
        y = 20 + 34 * math.sin(math.pi * x / W)
        flags[k % len(cols)].append([(x - 22, y), (x + 22, y + 1), (x + 2, y + 62)])
    for fl, col in zip(flags, cols):
        if fl:
            art = gp(art, shapes(W, H, fl, smooth=False), col, mix_hex(col, "#ffffff", 0.1), seed=nx(), rough=1.4)
    prev_rgba(art, "ll-bunting", bg="#fdf4e1")
    save_a(art, f"{OUT}/bunting.webp", max_w=380)


def part_spool():
    """Tin-can spool wound with plain string, a stick through it."""
    W, H = 220, 220
    nx = Seq(1100)
    art = blank(W, H)
    can = poly(W, H, [(60, 60), (160, 60), (160, 170), (60, 170)])
    art = gp(art, can, "#c9ccd2", "#9aa0aa", seed=nx(), rough=0.8)
    wound = poly(W, H, [(58, 80), (162, 80), (162, 150), (58, 150)])
    art = gp(art, wound, WHT, "#efe6d0", seed=nx(), rough=0.8)
    lines = [([(58, y), (162, y + 3)], 1.4, None) for y in range(84, 150, 5)]
    art = gp(art, strokes(W, H, lines), "#d9caa6", seed=nx(), rough=0.3, streak=0.2)
    art = gp(art, ellipses(W, H, [(110, 60, 50, 10, 0)]), "#e5e7ea", seed=nx(), rough=0.5)
    art = gp(art, strokes(W, H, [([(30, 190), (190, 34)], 7, None)]), SPAR, seed=nx(), rough=0.5, streak=0.3)
    art = gp(art, strokes(W, H, [(curve([(162, 100), (190, 90), (214, 50)], 12), 1.6, None)]), RED, seed=nx(), rough=0.3)
    art = outline(art, W, H, np.clip(can + wound, 0, 1), nx=nx)
    prev_rgba(art, "ll-spool", bg="#fdf4e1")
    save_a(art, f"{OUT}/spool.webp", max_w=110)


def part_scene():
    W, H = 760, 1560
    rng = random.Random(17); nx = Seq(1300)
    art = painted_sky(W, H, [(0, "#3d9be0"), (0.35, "#7cc2ee"), (0.66, "#c8e8f6"), (0.72, "#e6f4f8"), (1, "#f2e2bd")], seed=nx(), streak=1.0, grain=0.4)
    # clouds: lumpy gouache with flat bottoms
    for cxc, cyc, sc in [(130, 300, 1.0), (560, 200, 1.2), (620, 640, 0.8), (90, 820, 0.7), (420, 930, 0.9)]:
        cl = [(cxc + dx * sc, cyc + dy * sc, rx * sc, ry * sc, 0) for dx, dy, rx, ry in [(-60, 0, 50, 26), (-10, -20, 56, 38), (50, -6, 48, 30), (95, 6, 36, 20), (-100, 10, 30, 16)]]
        m = ellipses(W, H, cl) * (1 - ygrad(W, H, cyc + 12 * sc, cyc + 14 * sc))
        art = gp(art, m, "#ffffff", "#f2f7fb", seed=nx(), rough=3, streak=1.0)
        art = gp(art, m * ygrad(W, H, cyc - 5 * sc, cyc + 14 * sc), "#d9e9f3", seed=nx(), rough=2, streak=0.8)
    clear()
    # small far-off kites high in the sky
    far = []
    for _ in range(9):
        x, y, s = rng.uniform(40, 720), rng.uniform(380, 900), rng.uniform(7, 13)
        far.append(([(x, y - s), (x + s * 0.7, y), (x, y + s * 1.2), (x - s * 0.7, y)], (x, y + s * 1.2), rng.choice([RED, YEL, PINK, ORA, GRN, NAVY])))
    for pts, tail, col in far:
        art = gp(art, poly(W, H, pts), col, seed=nx(), rough=0.6, streak=0.3)
        art = gp(art, strokes(W, H, [(curve([tail, (tail[0] + 6, tail[1] + 14), (tail[0] - 4, tail[1] + 28)], 10), 1.2, (0, 0.5))]), NAVY, seed=nx(), rough=0.3, streak=0.2)
    clear()
    # sea: turquoise band with white crest strokes, a far island
    hz = 1110
    isl = poly(W, H, [(520, hz + 2), (580, hz - 22), (640, hz - 30), (700, hz - 12), (760, hz + 2)], smooth=True)
    art = gp(art, isl, "#6fa7a8", "#5f9a9b", seed=nx(), rough=1)
    sea = rect(W, H, -10, hz, W + 10, 1250)
    art = gp(art, sea, "#2bb3c0", "#1e8fb0", seed=nx(), rough=1, streak=1.4)
    art = gp(art, sea * ygrad(W, H, hz, 1250), "#4fd0cf", seed=nx(), rough=1, streak=1.2)
    crests = []
    for _ in range(70):
        y = rng.uniform(hz + 10, 1240); x = rng.uniform(-10, W)
        crests.append(([(x, y), (x + rng.uniform(16, 50), y + rng.uniform(-1, 1))], rng.uniform(1.6, 3.4), (0.3, 0.3)))
    art = gp(art, strokes(W, H, crests), "#ffffff", seed=nx(), rough=0.6, streak=0.4)
    foam = []
    x = -10
    while x < W + 10:
        foam.append((x, 1252 + rng.uniform(-3, 3), rng.uniform(20, 40), rng.uniform(4, 8), 0))
        x += rng.uniform(18, 30)
    art = gp(art, ellipses(W, H, foam), "#ffffff", "#e6f6f6", seed=nx(), rough=2)
    clear()
    # sand
    sand = rect(W, H, -10, 1255, W + 10, H + 10)
    art = gp(art, displace(sand, nx(), 3, 20), "#f1d39a", "#e8c283", seed=nx(), rough=2, streak=1.2)
    wet = sand * (1 - ygrad(W, H, 1255, 1300))
    art = gp(art, wet, "#d9b67a", seed=nx(), rough=1.5, streak=1.0)
    dots = []
    for _ in range(700):
        dots.append((rng.uniform(0, W), rng.uniform(1270, H), rng.uniform(0.8, 2.0), rng.uniform(0.6, 1.4), 0))
    art = gp(art, ellipses(W, H, dots), "#c99e5f", seed=nx(), rough=0.3, streak=0.2)
    # footprints trail
    fp = []
    for k in range(14):
        x = 120 + k * 32 + (k % 2) * 8; y = 1560 - k * 18 - (k % 2) * 10
        fp.append((x, y, 6, 3.5, -30))
    art = gp(art, ellipses(W, H, fp), "#d2a868", seed=nx(), rough=0.4, streak=0.2)
    # umbul-umbul flag poles (left & right) bending in the wind
    for px, h, cols in [(40, 420, (RED, YEL)), (88, 360, (BLUE, WHT)), (690, 440, (GRN, YEL)), (730, 380, (PINK, ORA))]:
        base = 1330 + (px % 3) * 6
        pole = strokes(W, H, [(curve([(px, base), (px + 4, base - h * 0.5), (px + 18, base - h)], 20), 4, (0.0, 0.3))])
        art = gp(art, pole, "#8a5a2e", seed=nx(), rough=0.5, streak=0.3)
        top = (px + 18, base - h)
        flag = [top]
        L = h * 0.62
        for k in range(1, 22):
            t = k / 21
            flag.append((top[0] + 8 + 30 * t + 6 * math.sin(t * 6), top[1] + L * t))
        for k in range(21, -1, -1):
            t = k / 21
            flag.append((top[0] + 2 + 6 * t + 6 * math.sin(t * 6), top[1] + L * t))
        fm = poly(W, H, flag, smooth=True)
        art = gp(art, fm, cols[0], seed=nx(), rough=0.8)
        art = gp(art, fm * (np.sin(np.arange(H)[:, None] / 10.0) > 0.2), cols[1], seed=nx(), rough=0.8)
    # panitia tent with striped roof (centre-left), a table
    tent_roof = poly(W, H, [(240, 1290), (300, 1240), (360, 1290)])
    art = gp(art, tent_roof, RED, seed=nx(), rough=1)
    art = gp(art, tent_roof * (np.sin(np.arange(W)[None, :] / 6.0) > 0.4), WHT, seed=nx(), rough=0.8)
    art = gp(art, rect(W, H, 248, 1290, 352, 1300), "#c33b28", seed=nx(), rough=0.6)
    art = gp(art, strokes(W, H, [([(250, 1298), (250, 1340)], 3, None), ([(350, 1298), (350, 1340)], 3, None)]), "#7a5a3a", seed=nx(), rough=0.4)
    art = gp(art, rect(W, H, 270, 1316, 330, 1324), "#7a5a3a", seed=nx(), rough=0.4)
    rgb = art[..., :3]
    prev_rgb(rgb, "ll-scene")
    save_rgb(rgb, f"{OUT}/scene.webp", quality=76)
    clear()


def part_mini():
    """Small wajik kite without string (timeline nodes, sent)."""
    W, H = 200, 240
    nx = Seq(1500)
    art = blank(W, H)
    c = (100, 95)
    top, bot, lft, rgt = (100, 10), (100, 200), (30, 80), (170, 80)
    for pts, col in zip([[top, rgt, c], [rgt, bot, c], [bot, lft, c], [lft, top, c]], [BLUE, GRN, BLUE, GRN]):
        art = gp(art, poly(W, H, pts), col, mix_hex(col, "#000000", 0.08), seed=nx(), rough=1.2)
    art = gp(art, poly(W, H, [(100, 60), (124, 84), (100, 124), (76, 84)]), YEL, seed=nx(), rough=0.8)
    art = outline(art, W, H, poly(W, H, [top, rgt, bot, lft]), nx=nx)
    art = gp(art, strokes(W, H, [([top, bot], 4, None), (curve([lft, (100, 70), rgt], 16), 4, None)]), SPAR, seed=nx(), rough=0.4, streak=0.3)
    pts, rm = ribbon(W, H, bot, 36, 6, 1.0, 3, ang=math.pi / 2)
    art = gp(art, rm, RED, seed=nx(), rough=0.4, streak=0.3)
    prev_rgba(art, "ll-mini", bg="#fdf4e1")
    save_a(art, f"{OUT}/mini.webp", max_w=84)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
