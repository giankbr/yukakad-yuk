"""Reuni Sekolah — retro school notebook: ruled-paper and chalkboard tiles, ballpoint doodles (school building, paper
plane, margin doodles), chalk doodles (school bell, stars), a gouache angkatan rosette badge, masking tape, a pencil.
Run: python3 -I reuni-sekolah.py [part ...]  parts: paper board school plane doodles chalk badge tape pencil node
Assets -> public/themes/art/reuni-sekolah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *

OUT = outdir("reuni-sekolah")
PARTS = sys.argv[1:] or ["paper", "board", "school", "plane", "doodles", "chalk", "badge", "tape", "pencil", "node"]
PEN = "#23377e"
RED = "#c8423a"
MUSTARD = "#e3a83a"


def wob(pts, rng, a=0.9):
    return [(x + rng.gauss(0, a), y + rng.gauss(0, a)) for x, y in pts]


def line(a, b, n=12):
    return lerp_pts(a, b, n)


def rect(x0, y0, x1, y1):
    return  [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def poly(pts):
    out = []
    for a, b in zip(pts, pts[1:]):
        out += line(a, b, max(4, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 6)))[:-1]
    return out + [pts[-1]]


def sketch(rng, pts, w=2.0, twice=True, sharp=None):
    """A ballpoint stroke, sometimes retraced (doodler's double line). sharp: straight segments (default for 4+ pts)."""
    if sharp is None:
        sharp = False
    path = (lambda: poly(pts)) if sharp or len(pts) == 2 else (lambda: curve(pts, max(12, len(pts) * 8)))
    out = [(wob(path(), rng, 0.6), w)]
    if twice and rng.random() < 0.55:
        out.append((wob(path(), rng, 1.1), w * 0.8))
    return out


def star5(cx, cy, r, rot=-math.pi / 2):
    pts = [(cx + math.cos(rot + k * 4 * math.pi / 5) * r, cy + math.sin(rot + k * 4 * math.pi / 5) * r) for k in range(6)]
    return pts


if "paper" in PARTS:
    W = H = 512
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    big = wrap_noise(W, H, 3, 40); fine = wrap_noise(W, H, 4, 0.7); fib = wrap_noise(W, H, 5, 3)
    base = np.array(hex_rgb("#fbf7ea"), np.float32)
    v = 1 + (big - 0.5) * 0.03 + (fine - 0.5) * 0.035 + (fib - 0.5) * 0.02
    rgb = base * v[..., None]
    # printed rules every 32px, ink slightly uneven
    d = np.abs(((yy - 31) % 32) - 0) ; d = np.minimum(d, 32 - d)
    rule = np.clip(1.3 - d, 0, 1) * (0.72 + 0.28 * wrap_noise(W, H, 7, 6))
    ink = np.array(hex_rgb("#9fb8d8"), np.float32)
    rgb = rgb * (1 - rule[..., None] * 0.85) + ink * rule[..., None] * 0.85
    a = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_full(a, f"{OUT}/paper.webp", quality=74)

if "board" in PARTS:
    W = H = 512
    base = np.array(hex_rgb("#2c3d35"), np.float32)
    big = wrap_noise(W, H, 11, 36); mid = wrap_noise(W, H, 12, 9); fine = wrap_noise(W, H, 13, 0.6)
    rgb = base * (1 + (big - 0.5) * 0.18 + (mid - 0.5) * 0.08 + (fine - 0.5) * 0.06)[..., None]
    # old eraser swirls (wide, faint) — wrapped
    rng = random.Random(5)
    items = []
    for _ in range(7):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(70, 170)
        a0 = rng.uniform(0, 6)
        items.append((arc_pts(cx, cy, r, a0, a0 + rng.uniform(1.2, 2.6), 40, rng.uniform(0.4, 0.9)), rng.uniform(26, 50), (0.3, 0.3)))
    sw = strokes(W, H, items)
    sw = tile_wrap(gaussian_filter(sw, 6)) * (0.5 + 0.5 * wrap_noise(W, H, 15, 2.5))
    dust = np.array(hex_rgb("#c9d3cc"), np.float32)
    k = (sw * 0.06 + (wrap_noise(W, H, 16, 22) > 0.7) * 0.03)[..., None]
    rgb = rgb * (1 - k) + dust * k
    a = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_full(a, f"{OUT}/board.webp", quality=70)

if "school" in PARTS:
    W, H = 640, 420
    rng = random.Random(31)
    it = []
    gy = 360
    # main building + wings
    it += sketch(rng, rect(170, 190, 470, gy), sharp=True)
    it += sketch(rng, [(150, 196), (320, 108), (490, 196)], sharp=True)
    it += sketch(rng, rect(60, 236, 170, gy), sharp=True) + sketch(rng, rect(470, 236, 580, gy), sharp=True)
    it += sketch(rng, [(50, 240), (60, 230), (170, 230)], twice=False, sharp=True) + sketch(rng, [(470, 230), (580, 230), (590, 240)], twice=False, sharp=True)
    # clock in the gable
    it += [(wob(arc_pts(320, 160, 22, 0, math.tau, 40), rng, 0.5), 2.0), (line((320, 160), (320, 146), 5), 2.2), (line((320, 160), (331, 165), 5), 2.2)]
    # windows (4x2) with crossbars
    for r in range(2):
        for c in range(5):
            x = 192 + c * 56; y = 210 + r * 52
            if r == 1 and c == 2:
                continue
            it += sketch(rng, rect(x, y, x + 30, y + 32), 1.7, twice=False, sharp=True)
            it += [(wob(line((x + 15, y), (x + 15, y + 32), 6), rng, 0.4), 1.2), (wob(line((x, y + 16), (x + 30, y + 16), 6), rng, 0.4), 1.2)]
    for x in (78, 120, 488, 530):
        it += sketch(rng, rect(x, 258, x + 28, 290), 1.6, twice=False, sharp=True)
    # door + steps
    it += sketch(rng, [(296, gy), (296, 300), (320, 286), (344, 300), (344, gy)], sharp=True)
    it += sketch(rng, [(282, gy + 10), (358, gy + 10)], twice=False) + sketch(rng, [(272, gy + 20), (368, gy + 20)], twice=False)
    # flag pole + flag
    it += sketch(rng, [(612, gy + 18), (612, 120)], 2.0)
    it += sketch(rng, [(612, 124), (650 - 8, 130), (612, 146)], 1.8, twice=False, sharp=True)
    # tree (scribbled crown)
    it += sketch(rng, [(30, gy + 16), (34, 300)], 2.2)
    sc = []
    for k in range(70):
        t = k / 70 * math.tau * 5
        sc.append((34 + math.cos(t) * (26 + 6 * math.sin(t * 2.3)) + rng.gauss(0, 2), 270 + math.sin(t) * (30 + 5 * math.cos(t * 1.7)) + rng.gauss(0, 2)))
    it += [(sc, 1.3)]
    # ground line
    it += [(wob(curve([(0, gy + 26), (200, gy + 24), (420, gy + 28), (640, gy + 25)], 60), rng, 0.6), 1.8)]
    # hatch on roof (light shading)
    for k in range(14):
        x = 200 + k * 18
        y_top = 196 - (1 - abs(x - 320) / 170) * 88
        it += [(wob(line((x, 196), (x + 8, max(y_top + 6, 120)), 5), rng, 0.4), 1.0)]
    art = ballpoint(blank(W, H), it, PEN, seed=7)
    preview(art, "rs-school", tone="#fbf7ea")
    save(art, f"{OUT}/school.webp", max_w=420, quality=82)
    clear()

if "plane" in PARTS:
    W, H = 420, 260
    rng = random.Random(41)
    it = []
    body = [(250, 90), (390, 40), (300, 150), (250, 90)]
    it += sketch(rng, body, 2.0, sharp=True)
    it += sketch(rng, [(390, 40), (290, 110), (300, 150)], 1.8, twice=False, sharp=True)
    it += sketch(rng, [(290, 110), (275, 128)], 1.6, twice=False)
    # dashed loop trail
    trail = curve([(240, 100), (170, 140), (120, 110), (140, 70), (180, 92), (150, 170), (60, 210), (10, 200)], 160)
    for i in range(0, len(trail) - 6, 10):
        it.append((wob(trail[i:i + 6], rng, 0.4), 1.6))
    art = ballpoint(blank(W, H), it, PEN, seed=9)
    preview(art, "rs-plane", tone="#fbf7ea")
    save(art, f"{OUT}/plane.webp", max_w=240, quality=82)
    clear()

if "doodles" in PARTS:
    W, H = 220, 640
    rng = random.Random(51)
    it = []
    it += sketch(rng, star5(110, 60, 36), 2.0, sharp=True)
    sp = [(110 + math.cos(t) * t * 3.2, 170 + math.sin(t) * t * 3.2) for t in [i * 0.25 for i in range(60)]]
    it += [(wob(sp, rng, 0.4), 1.8)]
    hx, hy = 110, 300
    heart = [(hx, hy + 30), (hx - 34, hy), (hx - 30, hy - 24), (hx - 10, hy - 26), (hx, hy - 10), (hx + 10, hy - 26), (hx + 30, hy - 24), (hx + 34, hy), (hx, hy + 30)]
    it += sketch(rng, heart, 2.0)
    for k in range(6):
        it += [(wob(line((hx - 22 + k * 8, hy + 16 - abs(k - 2.5) * 3), (hx - 14 + k * 8, hy - 14), 5), rng, 0.3), 1.1)]
    it += sketch(rng, [(60, 420), (100, 400), (140, 430), (170, 410)], 2.0, twice=False)
    it += sketch(rng, [(150, 396), (172, 410), (154, 430)], 2.0, twice=False)
    # little smiley sun + rays
    it += [(wob(arc_pts(110, 530, 30, 0, math.tau, 40), rng, 0.5), 2.0)]
    for k in range(10):
        a = k * math.tau / 10
        it += [(line((110 + math.cos(a) * 40, 530 + math.sin(a) * 40), (110 + math.cos(a) * 54, 530 + math.sin(a) * 54), 4), 1.8)]
    it += [(line((100, 522), (100, 526), 3), 3.2), (line((120, 522), (120, 526), 3), 3.2), (wob(arc_pts(110, 532, 13, 0.4, 2.7, 14), rng, 0.3), 1.8)]
    art = ballpoint(blank(W, H), it, PEN, seed=11)
    preview(art, "rs-doodles", tone="#fbf7ea")
    save(art, f"{OUT}/doodles.webp", max_w=110, quality=82)
    clear()

if "chalk" in PARTS:
    # school bell ringing + stars, drawn in chalk (for the countdown chalkboard band)
    W, H = 300, 260
    rng = random.Random(61)
    it = []
    bell = [(110, 180), (120, 150), (122, 110), (136, 80), (150, 72), (164, 80), (178, 110), (180, 150), (190, 180)]
    it += [(wob(curve(bell, 60), rng, 0.8), 6)]
    it += [(wob(line((96, 184), (204, 184), 20), rng, 0.8), 6), (wob(arc_pts(150, 194, 10, 0, math.tau, 24), rng, 0.6), 5)]
    it += [(wob(line((150, 72), (150, 52), 6), rng, 0.5), 5), (wob(arc_pts(150, 46, 7, 0, math.tau, 18), rng, 0.4), 4)]
    for s_ in (-1, 1):
        for k in range(3):
            r = 70 + k * 16
            a0 = -math.pi / 2 + s_ * 0.6
            it += [(wob(arc_pts(150, 130, r, a0 + s_ * 0.5, a0 + s_ * 0.95, 12), rng, 0.6), 4)]
    for (x, y, r) in [(40, 60, 16), (262, 70, 12), (250, 216, 10)]:
        it += [(wob(star5(x, y, r), rng, 0.5), 3.5)]
    art = chalk(blank(W, H), it, seed=5)
    preview(art, "rs-chalk", bg="#2c3d35")
    save(art, f"{OUT}/chalk.webp", max_w=180, quality=80)
    clear()

if "badge" in PARTS:
    W, H = 360, 440
    nx = Seq(40100); rng = random.Random(71)
    cx, cy = 180, 170
    # ribbon tails
    tails = shapes(W, H, [[(cx - 70, 230), (cx - 18, 250), (cx - 46, 420), (cx - 70, 392), (cx - 100, 408)],
                          [(cx + 70, 230), (cx + 18, 250), (cx + 46, 420), (cx + 70, 392), (cx + 100, 408)]], smooth=False)
    art = GP(blank(W, H), tails, RED, "#a8322c", seed=nx(), rough=1.2, streak=0.8)
    art = tint(art, side_light(tails, 6, 0, 4), "#7e221e", 0.5, seed=nx())
    # scalloped rosette
    sc = []
    for k in range(40):
        a = k / 40 * math.tau
        r = 140 + (8 if k % 2 == 0 else -2)
        sc.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    ros = shapes(W, H, [sc])
    art = GP(art, ros, MUSTARD, "#d9962e", seed=nx(), rough=1.0, streak=0.8)
    pleats = strokes(W, H, [([(cx + math.cos(a) * 100, cy + math.sin(a) * 100), (cx + math.cos(a) * 142, cy + math.sin(a) * 142)], 2.2, None) for a in [k / 40 * math.tau for k in range(40)]]) * ros
    art = tint(art, pleats, "#b47720", 0.55, seed=nx())
    inner = circles(W, H, [(cx, cy, 104)])
    art = GP(art, inner, RED, "#b8382f", seed=nx(), rough=0.8, streak=0.6)
    core = circles(W, H, [(cx, cy, 86)])
    art = GP(art, core, "#f8efd8", "#efe2c0", seed=nx(), rough=0.8, streak=0.6)
    art = tint(art, side_light(core, -8, -8, 6), "#d8c49a", 0.6, seed=nx())
    stitch = strokes(W, H, [(arc_pts(cx, cy, 95, a, a + 0.09, 3), 2.2, None) for a in [k * 0.16 for k in range(40)]])
    art = GP(art, stitch, "#f8efd8", seed=nx(), rough=0.3, pad=6, density=0.9)
    preview(art, "rs-badge", tone="#fbf7ea")
    save(art, f"{OUT}/badge.webp", max_w=200, quality=82)
    clear()

if "tape" in PARTS:
    W, H = 300, 90
    nx = Seq(40200); rng = random.Random(81)
    top = [(14 + x * 2, 14 + rng.uniform(-2, 2)) for x in range(137)]
    right = [(286 + rng.uniform(-5, 5) * ((k % 2) * 2 - 1) * 0.6, 14 + k * 6) for k in range(11)]
    bottom = [(286 - x * 2, 76 + rng.uniform(-2, 2)) for x in range(137)]
    left = [(14 + rng.uniform(-5, 5) * ((k % 2) * 2 - 1) * 0.6, 76 - k * 6) for k in range(11)]
    m = shapes(W, H, [top + right + bottom + left], smooth=False)
    art = OV(blank(W, H), m, lambda mm: col_arr(mm, "#efe2bd", mm * (0.78 + 0.12 * (fbm(mm.shape[1], mm.shape[0], 3, 12, 2) - 0.5))))
    art = tint(art, inner_edge(m, 2), "#d8c79a", 0.5, seed=nx())
    preview(art, "rs-tape", tone="#fbf7ea")
    save(art, f"{OUT}/tape.webp", max_w=140, quality=80)

if "pencil" in PARTS:
    W, H = 520, 80
    nx = Seq(40300)
    body = shapes(W, H, [[(70, 22), (440, 22), (440, 58), (70, 58)]], smooth=False)
    tip = shapes(W, H, [[(70, 22), (14, 40), (70, 58)]], smooth=False)
    lead = shapes(W, H, [[(32, 34), (14, 40), (32, 46)]], smooth=False)
    ferrule = shapes(W, H, [[(440, 20), (474, 20), (474, 60), (440, 60)]], smooth=False)
    eraser = shapes(W, H, [[(474, 21), (496, 21), (504, 30), (504, 50), (496, 59), (474, 59)]])
    art = GP(blank(W, H), body, "#f2c13c", "#ebb22e", seed=nx(), rough=0.8, streak=1.0)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    facet = body * (np.abs(yy - 34) < 2.5) + body * (np.abs(yy - 46) < 2.5)
    art = tint(art, facet, "#c98f1e", 0.45, seed=nx())
    art = tint(art, body * (yy > 47), "#d99a22", 0.5, seed=nx())
    art = GP(art, tip, "#efd3a6", "#e2bf8a", seed=nx(), rough=0.8)
    art = GP(art, lead, "#3a3532", seed=nx(), rough=0.4, pad=6)
    art = GP(art, ferrule, "#b9b3a6", "#9a9488", seed=nx(), rough=0.5)
    art = tint(art, ferrule * ((np.arange(W)[None, :] % 8) < 2), "#7e786c", 0.6, seed=nx())
    art = GP(art, eraser, "#f19aa0", "#e88a92", seed=nx(), rough=0.6)
    preview(art, "rs-pencil", tone="#fbf7ea")
    save(art, f"{OUT}/pencil.webp", max_w=180, quality=82)
    clear()

if "node" in PARTS:
    W, H = 120, 120
    rng = random.Random(91)
    it = [(wob(arc_pts(60, 62, 40, -0.4, math.tau + 0.2, 50, 0.95), rng, 0.6), 2.2)]
    it += sketch(rng, star5(60, 62, 20), 2.2, twice=False, sharp=True)
    art = ballpoint(blank(W, H), it, RED, seed=13)
    preview(art, "rs-node", tone="#fbf7ea")
    save(art, f"{OUT}/node.webp", max_w=60, quality=82)
