"""Gorga Toba — Batak Toba gorga carving (red/white/black relief, linocut-printed) and Lake Toba seen from Samosir
(watercolour). Run: python3 -I gorga-toba.py [part ...]; parts: toba lintel desa ipon.
Assets -> public/themes/art/gorga-toba/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l1_lib import *

OUT = outdir("gorga-toba")
PARTS = sys.argv[1:] or ["toba", "lintel", "desa", "ipon"]
BLACK, BLACK_L = "#1d1916", "#2c2622"
RED, RED_D = "#ad2a1f", "#7e1c14"
WHITE, WHITE_D = "#f1ebdf", "#d8cfbf"


def rim(mask, px):
    """Thin band hugging a relief shape (the white outline gorga carvers paint around the red)."""
    grown = np.clip(gaussian_filter(mask, px * 0.55) * 3.2, 0, 1)
    return np.clip(grown - mask, 0, 1)


def scroll_items(x0, x1, cy, amp, period, s, phase=0):
    """Running gorga vine: a wave stem with a spiral curling out of every crest/trough (alternating)."""
    stem = [(x, cy + amp * math.sin((x - x0) / period * math.pi + phase)) for x in np.linspace(x0, x1, 200)]
    items = [(stem, s * 0.16, None)]
    k = 0
    x = x0 + period * 0.5
    while x < x1 - period * 0.2:
        up = k % 2 == 0
        yc = cy + amp * math.sin((x - x0) / period * math.pi + phase)
        d = -1 if up else 1
        # spiral sits beside the crest, curling inward
        cx_, cy_ = x + period * 0.32, yc + d * s * 0.62
        sp = spiral_pts(cx_, cy_, s * 0.58, s * 0.08, math.pi if d < 0 else math.pi, 1.6, 50, -d)
        items.append(([(x, yc)] + sp, s * 0.13, (0.0, 0.55)))
        # small tendril on the other side
        t = curve([(x - period * 0.05, yc), (x - period * 0.22, yc + d * s * 0.5), (x - period * 0.18, yc + d * s * 0.85)], 16)
        items.append((t, s * 0.08, (0.0, 0.6)))
        x += period
        k += 1
    return items


def s_motif(cx, cy, w, r, flip=1):
    """Gorga double spiral: a spiral unwinding on the left, an S bridge, and a spiral winding in on the right."""
    lx, rx = cx - w * 0.5, cx + w * 0.5
    ly, ry = cy - r * 0.35 * flip, cy + r * 0.35 * flip
    # left: from centre outward (angle increases), ending at the bottom (flip=1) heading right
    a_end = math.pi / 2 * flip
    turns = 1.6
    left = [(lx + math.cos(a_end - flip * (1 - t) * turns * math.tau) * r * (0.12 + 0.88 * t), ly + math.sin(a_end - flip * (1 - t) * turns * math.tau) * r * (0.12 + 0.88 * t)) for t in [i / 59 for i in range(60)]]
    b_start = -math.pi / 2 * flip
    right = [(rx + math.cos(b_start - flip * t * turns * math.tau) * r * (1 - 0.88 * t), ry + math.sin(b_start - flip * t * turns * math.tau) * r * (1 - 0.88 * t)) for t in [i / 59 for i in range(60)]]
    bridge = curve([left[-1], (cx - w * 0.1, left[-1][1]), (cx + w * 0.1, right[0][1]), right[0]], 30)
    return left + bridge[1:-1] + right


if "toba" in PARTS:
    # Lake Toba from the Samosir shore at morning: caldera wall in layered blue, mist, still water, pines, a solu.
    W, H = 900, 620
    nx = Seq(40100)
    art = painted_sky(W, H, [(0, "#c9d7dd"), (0.32, "#eae3d3"), (0.46, "#f2eadb"), (1, "#f2eadb")], seed=nx(), streak=0.8)
    # far caldera wall (three layers, lighter = farther)
    for y, amp, col, col2, seed in [(236, 60, "#a3b6c1", "#b8c6cc", 3), (268, 52, "#7891a2", "#8ea5b1", 8), (298, 30, "#4f6e80", "#5f7f8f", 13)]:
        m = hills(W, H, y, amp, seed, wl=0.7)
        m *= (np.mgrid[0:H, 0:W][0] < 330).astype(np.float32)
        art = G(art, m, col, col2, seed=nx(), density=0.75, edge=0.45, bloom=0.4, rough=6, feather=1.4)
    # mist band
    mist = shapes(W, H, [[(-20, 300), (W + 20, 292), (W + 20, 334), (-20, 342)]])
    art = OV(art, gaussian_filter(mist, 14) * 0.85, lambda m: tint(m, "#eef0ea"))
    # water
    water = shapes(W, H, [[(-10, 326), (W + 10, 326), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = G(art, water * np.clip((yy - 326) / 260, 0.15, 1), "#4f7e98", "#6f99ad", seed=nx(), density=0.8, edge=0.1, bloom=0.25, rough=2, feather=1)
    # reflections: horizontal dry-brush streaks
    rng = random.Random(4)
    streaks = [([(x, y), (x + rng.uniform(40, 160), y + rng.uniform(-1, 1))], rng.uniform(1.2, 3.2), (0.3, 0.3)) for x, y in [(rng.uniform(-40, W), rng.uniform(334, H)) for _ in range(90)]]
    art = OV(art, strokes(W, H, streaks) * 0.5, lambda m: tint(m, "#e8eee9"))
    dark = [([(x, y), (x + rng.uniform(60, 200), y)], rng.uniform(1.5, 3), (0.3, 0.3)) for x, y in [(rng.uniform(-40, W), rng.uniform(380, H)) for _ in range(50)]]
    art = G(art, strokes(W, H, dark), "#3f6a82", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1.5, feather=0.8)
    # reflection of the caldera wall
    refl = np.flipud(hills(W, H, H - 300 + 300 - 26, 18, 13, wl=0.7))
    refl = np.roll(refl, 0, 0) * ((yy > 326) & (yy < 372)).astype(np.float32)
    art = G(art, refl * 0.6, "#4f7387", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=4, feather=3)
    clear()
    # Samosir foreground: grassy slope on the left with stones and pines
    slope = shapes(W, H, [[(-20, 420), (90, 404), (220, 430), (330, 470), (430, 520), (520, H + 20), (-20, H + 20)]])
    art = G(art, slope, "#6f8a4e", "#8f9f5a", seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=5)
    art = G(art, slope * hatch(W, H, 1.3, 9, 0.12, 6, wob=4), "#4b6236", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    stones = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 9, 0), random.Random(int(x)), 2, 0.12) for x, y, rx, ry in [(400, 548, 40, 15), (330, 596, 52, 18), (480, 604, 34, 12), (200, 612, 60, 16)]])
    art = G(art, stones, "#8d8a80", "#b0aa9c", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=3)
    art = G(art, stones * np.clip((yy - 540) / 80, 0, 1), "#57524a", seed=nx(), density=0.45, edge=0.2, rough=2)
    clear()
    # tusam pines (Pinus merkusii) on the slope
    rngp = random.Random(9)
    pines = []
    for (x, by, h) in [(70, 430, 230), (150, 438, 180), (34, 446, 150), (250, 452, 120)]:
        trunk = ([(x, by), (x + 2, by - h)], 4.5, None)
        pines.append(("t", trunk))
        tiers = []
        for j in range(7):
            t = j / 6
            yy0 = by - h * (0.25 + 0.75 * t)
            ww = h * 0.32 * (1 - t * 0.75) * rngp.uniform(0.85, 1.15)
            tiers.append(deform([(x - ww, yy0 + 10), (x + rngp.uniform(-4, 4), yy0 - h * 0.12), (x + ww, yy0 + 8), (x, yy0 + 2)], rngp, 1, 0.06))
        pines.append(("c", tiers))
    tr = strokes(W, H, [p[1] for p in pines if p[0] == "t"])
    art = G(art, tr, "#3d2f24", seed=nx(), density=0.8, edge=0.3, rough=1)
    crowns = shapes(W, H, [t for p in pines if p[0] == "c" for t in p[1]])
    art = G(art, crowns, "#2f4a35", "#3f5f3e", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=3)
    art = G(art, crowns * np.clip(fbm(W, H, 77, 10, 2) - 0.45, 0, 1) * 2, "#1f3326", seed=nx(), density=0.6, edge=0.2, rough=1)
    # solu (dugout boat) on the water
    boat = shapes(W, H, [[(610, 452), (700, 452), (716, 444), (712, 458), (700, 462), (618, 462), (604, 446)]])
    art = G(art, boat, "#3a2a20", seed=nx(), density=0.9, edge=0.4, rough=1.2)
    art = G(art, strokes(W, H, [([(640, 444), (690, 420)], 2.2, None)]), "#3a2a20", seed=nx(), density=0.8, edge=0.2, rough=0.6)
    art = OV(art, strokes(W, H, [([(590, 468), (740, 468)], 2, (0.4, 0.4)), ([(620, 476), (710, 476)], 1.5, (0.4, 0.4))]) * 0.7, lambda m: tint(m, "#e8eee9"))
    # birds
    birds = [curve([(x - 7, y - 2), (x, y + 2), (x + 7, y - 3)], 8) for x, y in [(560, 150), (585, 140), (610, 162)]]
    art = G(art, strokes(W, H, [(b, 1.6, (0.2, 0.2)) for b in birds]), "#3e4a52", seed=nx(), density=0.7, edge=0.1, rough=0.5)
    art = add_grain(art, 5, 0.03)
    save_rgb(art, f"{OUT}/toba.webp", size=(720, 496), quality=76)
    preview(art, "gt-toba")
    clear()

if "lintel" in PARTS:
    # carved board: ipon-ipon tooth borders top & bottom, running red-white scroll, desa na ualu medallion in the centre
    W, H = 1100, 300
    nx = Seq(41100)
    board = rrect_mask(W, H, 4, 6, W - 4, H - 6, 6)
    art = GP(blank(W, H), board, BLACK, BLACK_L, seed=nx(), rough=1.0, streak=1.2, pad=8)
    art = G(art, board * hatch(W, H, 0.02, 9, 0.1, 7, wob=4), "#3b322b", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    # ipon-ipon (teeth) bands
    teeth_top, teeth_bot = [], []
    step = 26
    for i in range(int(W / step) + 1):
        x = 8 + i * step
        teeth_top.append([(x, 18), (x + step, 18), (x + step / 2, 44)])
        teeth_bot.append([(x, H - 18), (x + step, H - 18), (x + step / 2, H - 44)])
    tm = shapes(W, H, teeth_top + teeth_bot, smooth=False) * board
    bands = shapes(W, H, [rect(8, 14, W - 8, 19), rect(8, H - 19, W - 8, H - 14)], smooth=False)
    art = LC(art, np.maximum(tm, bands), WHITE, seed=nx(), wear=0.35)
    inner = shapes(W, H, [[(x[0][0] + 7, 22), (x[1][0] - 7, 22), (x[2][0], 36)] for x in teeth_top] + [[(x[0][0] + 7, H - 22), (x[1][0] - 7, H - 22), (x[2][0], H - 36)] for x in teeth_bot], smooth=False) * board
    art = LC(art, inner, RED, seed=nx(), wear=0.3)
    # running scrolls left and right of the medallion
    cx, cy = W / 2, H / 2
    items = []
    n = 4
    span = (cx - 120 - 30) / n
    for i in range(n):
        mx = 30 + span * (i + 0.5)
        f = 1 if i % 2 == 0 else -1
        items.append((s_motif(mx, cy, span * 0.66, 46, f), 9, (0.04, 0.12)))
        # leaf tendrils in the free corners
        ty = cy - 66 * f
        items.append((curve([(mx - span * 0.05, ty + 18 * f), (mx + span * 0.12, ty), (mx + span * 0.3, ty + 10 * f)], 16), 6, (0.0, 0.6)))
    half = strokes(W, H, items)
    half[:, int(cx):] = 0
    mir = half[:, ::-1]
    red_raw = np.maximum(half, mir)
    red = red_raw * board
    white = rim(red, 6) * board
    art = LC(art, white, WHITE, seed=nx(), wear=0.4)
    art = LC(art, red, RED, seed=nx(), wear=0.35)
    # carved shading on the red relief (lower-right edge darker)
    lo = np.clip(red - lift(red, -2, -3), 0, 1)
    art = G(art, lo, RED_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.6)
    hi = np.clip(red - lift(red, 2, 3), 0, 1)
    art = OV(art, hi * 0.35, lambda m: tint(m, "#e86a50"))
    clear()
    # medallion: desa na ualu (eight directions)
    R = 104
    disc = circles(W, H, [(cx, cy, R)])
    art = GP(art, disc, BLACK, seed=nx(), rough=0.6, pad=6)
    art = LC(art, ring(W, H, cx, cy, R, 7), WHITE, seed=nx(), wear=0.3)
    pts_big, pts_small = [], []
    for k in range(8):
        a = k * math.tau / 8 - math.pi / 2
        r = R * 0.86 if k % 2 == 0 else R * 0.62
        w = 0.2 if k % 2 == 0 else 0.26
        poly = [(cx + math.cos(a - w) * R * 0.22, cy + math.sin(a - w) * R * 0.22), (cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + w) * R * 0.22, cy + math.sin(a + w) * R * 0.22)]
        (pts_big if k % 2 == 0 else pts_small).append(poly)
    big = shapes(W, H, pts_big, smooth=False); small = shapes(W, H, pts_small, smooth=False)
    art = LC(art, rim(big, 6), WHITE, seed=nx(), wear=0.25)
    art = LC(art, big, RED, seed=nx(), wear=0.25)
    art = LC(art, small, WHITE, seed=nx(), wear=0.3)
    art = LC(art, circles(W, H, [(cx, cy, R * 0.2)]), RED, seed=nx(), wear=0.2)
    art = LC(art, circles(W, H, [(cx, cy, R * 0.09)]), WHITE, seed=nx(), wear=0.2)
    dots = circles(W, H, [(cx + math.cos(k * math.tau / 16 + math.pi / 16) * R * 0.8, cy + math.sin(k * math.tau / 16 + math.pi / 16) * R * 0.8, 4) for k in range(16)])
    art = LC(art, dots, WHITE, seed=nx(), wear=0.2)
    preview(art, "gt-lintel", tone="#efe9dd")
    save(art, f"{OUT}/lintel.webp", max_w=880, quality=80)
    clear()

if "desa" in PARTS:
    # standalone desa na ualu emblem (divider / node / closing)
    W = H = 360
    nx = Seq(42100)
    cx = cy = 180; R = 160
    art = blank(W, H)
    art = GP(art, circles(W, H, [(cx, cy, R)]), BLACK, BLACK_L, seed=nx(), rough=1.2, streak=0.8)
    art = LC(art, ring(W, H, cx, cy, R - 6, 8), WHITE, seed=nx(), wear=0.3)
    teeth = []
    for k in range(32):
        a = k * math.tau / 32
        teeth.append([(cx + math.cos(a - 0.09) * (R - 16), cy + math.sin(a - 0.09) * (R - 16)), (cx + math.cos(a + 0.09) * (R - 16), cy + math.sin(a + 0.09) * (R - 16)), (cx + math.cos(a) * (R - 34), cy + math.sin(a) * (R - 34))])
    art = LC(art, shapes(W, H, teeth, smooth=False), RED, seed=nx(), wear=0.3)
    big, small = [], []
    for k in range(8):
        a = k * math.tau / 8 - math.pi / 2
        r = R * 0.74 if k % 2 == 0 else R * 0.54
        w = 0.2 if k % 2 == 0 else 0.27
        poly = [(cx + math.cos(a - w) * R * 0.2, cy + math.sin(a - w) * R * 0.2), (cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + w) * R * 0.2, cy + math.sin(a + w) * R * 0.2)]
        (big if k % 2 == 0 else small).append(poly)
    bm = shapes(W, H, big, smooth=False); sm = shapes(W, H, small, smooth=False)
    art = LC(art, rim(bm, 7), WHITE, seed=nx(), wear=0.25)
    art = LC(art, bm, RED, seed=nx(), wear=0.25)
    art = LC(art, sm, WHITE, seed=nx(), wear=0.3)
    # tiny curls between the points
    curls = [(spiral_pts(cx + math.cos(k * math.tau / 8 - math.pi / 2 + math.pi / 8) * R * 0.6, cy + math.sin(k * math.tau / 8 - math.pi / 2 + math.pi / 8) * R * 0.6, 12, 2, k, 1.2, 24, 1), 3.2, (0.0, 0.5)) for k in range(8)]
    art = LC(art, strokes(W, H, curls), RED, seed=nx(), wear=0.2)
    art = LC(art, circles(W, H, [(cx, cy, R * 0.18)]), RED, seed=nx(), wear=0.2)
    art = LC(art, circles(W, H, [(cx, cy, R * 0.08)]), WHITE, seed=nx(), wear=0.2)
    preview(art, "gt-desa", tone="#efe9dd")
    save(art, f"{OUT}/desa.webp", max_w=220, quality=82)
    clear()

if "ipon" in PARTS:
    # seamless horizontal tooth band (repeat-x): black ground, white teeth with red inner teeth, top/bottom rules
    W, H = 208, 60
    nx = Seq(43100)
    art = solid(W, H, BLACK)
    art = GP(art, np.ones((H, W), np.float32), BLACK, BLACK_L, seed=nx(), rough=0, streak=1.2)
    step = 26
    teeth = [[(i * step, 10), ((i + 1) * step, 10), (i * step + step / 2, 40)] for i in range(-1, W // step + 1)]
    tri2 = [[(i * step + step / 2, 50), (i * step + step * 1.5, 50), (i * step + step, 22)] for i in range(-1, W // step + 1)]
    wm = shapes(W, H, teeth, smooth=False)
    art = LC(art, np.maximum(wm, shapes(W, H, [rect(0, 4, W, 8), rect(0, 52, W, 56)], smooth=False)), WHITE, seed=nx(), wear=0.25, rough=0.6)
    art = LC(art, shapes(W, H, tri2, smooth=False) * (1 - wm), RED, seed=nx(), wear=0.25, rough=0.6)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/ipon.webp", quality=82)
    preview(art, "gt-ipon")
