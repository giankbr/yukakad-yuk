"""Selancar Retro — 70s surf poster in screen-print gouache: sliced sunset sun over stripes, a curling wave with cream
foam bands, leaning palms; a two-tone camper van with boards on the roof rack; single striped board; wave-curl
divider; little sun; palm. Run: python3 -I selancar-retro.py [part ...]  parts: poster van board wave sun palm"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n6_lib import *

OUT = outdir("selancar-retro")
PARTS = sys.argv[1:] or ["poster", "van", "board", "wave", "sun", "palm"]
CREAM, CREAM_D = "#f6e8cc", "#e9d3a8"
MUST, ORANGE, CORAL, RED = "#f2b440", "#ee8a35", "#e0603a", "#c8453a"
TEAL, TEAL_D, TEAL_L, DEEP = "#2b8f8c", "#1d6a70", "#5fb5a8", "#17485a"
INK = "#3a2620"
SAND, SAND_D = "#f1cd8f", "#d9a865"


def P(art, mask, col, col2=None, nx=None, rough=2.0, dry=0.0, pad=12):
    """screen-print gouache: opaque, hand-cut edge, faint streak, optional dry wear."""
    return GP(art, mask, col, col2 or col, seed=nx(), rough=rough, streak=0.7, dry=dry, pad=pad)


def wear(arr, seed, amt=0.10):
    """ink-didn't-take speckle + paper grain over an opaque print."""
    h, w = arr.shape[:2]
    sp = fbm(w, h, seed, 5, 2)
    k = np.clip((sp - 0.7) * 4, 0, 1) * amt
    out = arr.copy()
    paperc = np.array(hex_rgb(CREAM), np.float32)
    out[..., :3] = out[..., :3] * (1 - k[..., None]) + paperc * k[..., None]
    return add_grain(out, seed + 1, 0.05)


def palm_tree(W, H, x, by, h, rng, lean):
    """palm silhouette: tapered curved trunk + feathered fronds (leaflets along arching rachises)."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.2, by - h * 0.55), top], 30)
    ms = [strokes(W, H, [(trunk, h * 0.04, (0.0, 0.9))])]
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.1, 0.1)
        L = h * rng.uniform(0.38, 0.5)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5 - h * 0.06),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.5)], 30)
        ms.append(frond(W, H, pts, h * 0.075, h * 0.012, step=1, spread=0.7, droop=0.9, profile=0.5, n=8))
    ms.append(circles(W, H, [(top[0] + rng.uniform(-6, 6), top[1] + 12 + rng.uniform(0, 6), h * 0.018) for _ in range(3)]))
    m = np.maximum.reduce(ms)
    # trunk ring notches
    rings = []
    for i in range(3, len(trunk) - 2, 2):
        px, py = trunk[i]
        rings.append(([(px - h * 0.03, py), (px + h * 0.01, py - h * 0.008)], h * 0.004, None))
    return np.clip(m - strokes(W, H, rings), 0, 1)


def board_mask(W, H, cx, cy, L, wd, ang):
    """surfboard outline (pointed nose, rounded tail)."""
    pts = []
    for i in range(40):
        t = i / 39
        y = -L / 2 + L * t
        k = math.sin(math.pi * min(1, t ** 0.75)) ** 0.6
        pts.append((wd / 2 * k, y))
    pts = pts + [(-x, y) for x, y in pts[::-1]]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def board(art, W, H, cx, cy, L, wd, ang, base, stripe, nx, stripe2=None):
    poly = board_mask(W, H, cx, cy, L, wd, ang)
    m = shapes(W, H, [poly])
    art = P(art, m, base, mix(base, INK, 0.12), nx, rough=1.0)
    ca, sa = math.cos(ang), math.sin(ang)
    def Q(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    st = strokes(W, H, [([Q(0, -L * 0.42), Q(0, L * 0.44)], wd * 0.16, None)]) * m
    art = P(art, st, stripe, None, nx, rough=0.6, pad=6)
    if stripe2:
        b2 = strokes(W, H, [([Q(-wd, L * 0.12), Q(wd, L * 0.12)], wd * 0.12, None), ([Q(-wd, L * 0.2), Q(wd, L * 0.2)], wd * 0.07, None)]) * m
        art = P(art, b2, stripe2, None, nx, rough=0.6, pad=6)
    art = lay(art, edge_hi(m, -3, 0) * 0.8, "#fff7e6", 0.6)
    art = G(art, edge_lo(m, 3, 2), INK, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.5)
    return art


if "poster" in PARTS:
    W, H = 760, 760
    rng = random.Random(61); nx = Seq(6100)
    art = solid(W, H, CREAM)
    HZ = 452
    # sky stripes (top pale -> red at the horizon)
    bands = [(0, "#f7dca2"), (120, MUST), (220, "#f19f3b"), (300, ORANGE), (360, CORAL), (410, RED)]
    for i, (y0, col) in enumerate(bands):
        pts = [(-10, y0 + rng.uniform(-3, 3))] + [(x, y0 + 3 * math.sin(x / 60 + i)) for x in range(0, W + 20, 40)] + [(W + 10, HZ + 10), (-10, HZ + 10)]
        art = P(art, shapes(W, H, [pts], smooth=False), col, mix(col, "#ffffff", 0.06), nx, rough=2.0)
    # sliced sun
    sun = circles(W, H, [(462, HZ - 6, 158)]) * (np.mgrid[0:H, 0:W][0] < HZ).astype(np.float32)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    gaps = np.zeros((H, W), np.float32)
    for k, (y, t) in enumerate([(HZ - 100, 4), (HZ - 74, 7), (HZ - 48, 10), (HZ - 22, 13)]):
        gaps = np.maximum(gaps, ((yy > y) & (yy < y + t)).astype(np.float32))
    art = P(art, np.clip(sun - gaps, 0, 1), "#fbe5ad", "#f9d98e", nx, rough=1.2)
    # sea
    sea = shapes(W, H, [rect(-10, HZ, W + 10, H + 10)], smooth=False)
    art = P(art, sea, TEAL, DEEP, nx, rough=1.5)
    deep = np.clip((yy - HZ) / 300, 0, 1) * sea
    art = G(art, deep, DEEP, seed=nx(), density=0.5, edge=0, bloom=0.2, rough=2)
    # sun glitter on the water
    gl = []
    for k in range(18):
        y = HZ + 12 + k * 13 + rng.uniform(-3, 3)
        wdt = 160 * (1 - k / 22) * rng.uniform(0.6, 1.1)
        cx = 462 + rng.uniform(-30, 30)
        gl.append(([(cx - wdt / 2, y), (cx + wdt / 2, y)], 4 + k * 0.25, (0.3, 0.3)))
    art = P(art, strokes(W, H, gl), "#f9d98e", None, nx, rough=1.0)
    # distant rollers
    rl = []
    for k in range(5):
        y = HZ + 40 + k * 46
        rl.append((curve([(380 + k * 30, y), (520 + k * 20, y - 8), (W + 20, y + 4)], 24), 5, (0.3, 0.0)))
    art = P(art, strokes(W, H, rl), TEAL_L, None, nx, rough=1.0)
    clear()
    # the big curling wave (left)
    outer = curve([(-30, 720), (40, 600), (120, 470), (210, 360), (300, 290), (372, 272), (420, 296), (428, 336)], 80)
    inner = curve([(428, 336), (398, 352), (360, 336), (322, 348), (300, 392), (306, 448), (350, 500), (450, 548), (590, 600), (800, 640)], 80)
    wave_poly = outer + inner + [(800, 800), (-30, 800)]
    wm = shapes(W, H, [wave_poly], smooth=False)
    art = P(art, wm, TEAL, "#2f9e98", nx, rough=1.6)
    barrel = shapes(W, H, [curve([(428, 336), (398, 352), (360, 336), (322, 348), (300, 392), (306, 448), (350, 500)], 40) + [(250, 470), (230, 380), (300, 316), (380, 300)]])
    art = P(art, barrel * wm, TEAL_D, DEEP, nx, rough=1.2)
    # foam bands following the face
    def offset(pts, d):
        out = []
        for i in range(len(pts)):
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
            out.append((pts[i][0] - dy / L * d, pts[i][1] + dx / L * d))
        return out
    foam = []
    for k, (d, wd) in enumerate([(10, 12), (40, 9), (66, 6)]):
        seg = offset(outer[6 + k * 3:-2 - k * 2], d)
        foam.append((seg, wd, (0.15, 0.25)))
    art = P(art, strokes(W, H, foam) * wm, CREAM, None, nx, rough=1.2)
    # lip spray: cream scallops
    lip = [petal_pts(x, y, 26, 9, a, n=10) for x, y, a in [(380, 276, -0.9), (410, 290, -0.3), (430, 318, 0.4), (350, 276, -1.4)]]
    art = P(art, shapes(W, H, lip), CREAM, None, nx, rough=1.0)
    spray = circles(W, H, [(445 + rng.uniform(-18, 22), 300 + rng.uniform(-40, 30), rng.uniform(3, 7)) for _ in range(14)])
    art = P(art, spray, CREAM, None, nx, rough=0.6)
    # foam at the foot
    footf = strokes(W, H, [(curve([(360, 508), (470, 560), (620, 606), (790, 640)], 40), 10, (0.1, 0.4)),
                           (curve([(330, 470), (380, 520)], 10), 7, None)])
    art = P(art, footf, CREAM, None, nx, rough=1.0)
    clear()
    # beach (lower right) and palms
    beach = shapes(W, H, [[(300, H + 10), (380, 700), (520, 668), (680, 650), (W + 10, 640), (W + 10, H + 10)]])
    art = P(art, beach, SAND, SAND_D, nx, rough=1.6)
    wet = strokes(W, H, [(curve([(330, 740), (420, 694), (560, 666), (W + 10, 650)], 40), 6, None)])
    art = P(art, wet, CREAM, None, nx, rough=1.0)
    palms = np.maximum(palm_tree(W, H, 690, 700, 400, rng, -0.2), palm_tree(W, H, 735, 690, 300, rng, -0.06))
    art = P(art, palms, INK, "#4a3028", nx, rough=1.2)
    art = wear(art, 77, 0.12)
    out = art.copy(); out[..., 3] = 1
    im = to_image(out).convert("RGB").resize((680, 680), Image.LANCZOS)
    im.save(f"{OUT}/poster.webp", "WEBP", quality=76, method=6)
    im.save(f"{PREV}/sr-poster.png")
    print("poster", os.path.getsize(f"{OUT}/poster.webp") // 1024, "KB")
    clear()

if "van" in PARTS:
    W, H = 600, 380
    rng = random.Random(9); nx = Seq(6500)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(300, 352, 250, 12, 16)]), INK, seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=5)
    # boards on the rack (behind the rack bars)
    art = board(art, W, H, 300, 92, 430, 46, math.pi / 2 + 0.02, CORAL, CREAM, nx, MUST)
    art = board(art, W, H, 290, 118, 380, 40, math.pi / 2 - 0.03, MUST, TEAL, nx)
    rack = strokes(W, H, [([(150, 140), (450, 140)], 6, None), ([(170, 140), (170, 158)], 5, None), ([(300, 140), (300, 158)], 5, None), ([(430, 140), (430, 158)], 5, None)])
    art = P(art, rack, INK, None, nx, rough=0.6)
    # body: boxy two-tone camper, facing left
    body = [(78, 300), (70, 230), (84, 186), (118, 162), (470, 158), (512, 166), (526, 190), (530, 300)]
    bm = shapes(W, H, [body])
    art = P(art, bm, TEAL, TEAL_D, nx, rough=1.2)
    top = bm * (np.mgrid[0:H, 0:W][0] < 236).astype(np.float32)
    art = P(art, top, CREAM, CREAM_D, nx, rough=0.8)
    # split stripe
    art = P(art, strokes(W, H, [([(72, 238), (530, 238)], 9, None)]) * bm, ORANGE, None, nx, rough=0.6)
    art = P(art, strokes(W, H, [([(72, 252), (530, 252)], 4, None)]) * bm, MUST, None, nx, rough=0.6)
    # windows
    wins = [[(96, 222), (98, 196), (112, 180), (162, 178), (162, 222)]] + [rect(x, 180, x + 74, 222) for x in (184, 274, 364)] + [rect(452, 180, 508, 222)]
    wm = shapes(W, H, wins, smooth=False)
    art = P(art, wm, "#8ccfc6", TEAL_L, nx, rough=0.6)
    art = lay(art, wm * (np.sin((np.mgrid[0:H, 0:W][1] + np.mgrid[0:H, 0:W][0] * 0.7) / 9) > 0.7) * 0.6, "#e9fbf6", 0.7)
    art = G(art, edge_lo(wm, 2, 2) + edge_hi(wm, -2, -2), INK, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    # door line, handle, bumper, lights
    det = strokes(W, H, [([(176, 176), (176, 296)], 2.4, None), ([(266, 176), (266, 296)], 2.4, None), ([(196, 268), (214, 268)], 4, None)])
    art = G(art, det * bm, INK, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    bump = shapes(W, H, [rect(56, 288, 120, 304), rect(500, 288, 546, 304)], smooth=False)
    art = P(art, bump, "#d9d2c3", "#a69f93", nx, rough=0.5)
    art = P(art, circles(W, H, [(80, 266, 9)]), "#fff3c8", None, nx, rough=0.4)
    art = P(art, circles(W, H, [(522, 268, 6)]), RED, None, nx, rough=0.4)
    # wheel arches + wheels
    for wx in (160, 436):
        arch = circles(W, H, [(wx, 304, 46)]) * bm
        art = P(art, arch, "#2a1a16", None, nx, rough=0.5)
        art = P(art, circles(W, H, [(wx, 306, 38)]), "#2a1a16", "#3d2a24", nx, rough=0.5)
        art = P(art, circles(W, H, [(wx, 306, 20)]), CREAM, "#d9cdb6", nx, rough=0.4)
        art = P(art, circles(W, H, [(wx, 306, 7)]), ORANGE, None, nx, rough=0.3)
    art = lay(art, edge_hi(bm, -3, -3) * 0.7, "#fffaf0", 0.6)
    art = wear(art, 99, 0.08)
    prev(art, "sr-van", tone=CREAM)
    save(art, f"{OUT}/van.webp", max_w=480, quality=82)
    clear()

if "board" in PARTS:
    W, H = 140, 460
    nx = Seq(6700)
    art = board(blank(W, H), W, H, 70, 230, 430, 92, 0.0, CREAM, CORAL, nx, TEAL)
    art = wear(art, 5, 0.06)
    prev(art, "sr-board", tone=MUST)
    save(art, f"{OUT}/board.webp", max_w=80, quality=84)

if "wave" in PARTS:
    W, H = 600, 110
    rng = random.Random(4); nx = Seq(6900)
    art = blank(W, H)
    for k in range(3):
        cx = 110 + k * 190
        crest = curve([(cx - 110, 92), (cx - 70, 70), (cx - 20, 40), (cx + 28, 30), (cx + 56, 44), (cx + 54, 66)], 40)
        curl = spiral_pts(cx + 30, 60, 22, 4, -0.3, 0.9, 30, 1)
        body = shapes(W, H, [crest + [(cx + 40, 74), (cx + 14, 70), (cx + 10, 96), (cx + 80, 100), (cx - 120, 100)]])
        art = P(art, body, TEAL, TEAL_D, nx, rough=0.8, pad=6)
        art = P(art, strokes(W, H, [(crest[8:], 6, (0.1, 0.1)), (curl, 5, (0.0, 0.6))]), CREAM, None, nx, rough=0.5, pad=6)
    art = wear(art, 3, 0.05)
    prev(art, "sr-wave", tone=CREAM)
    save(art, f"{OUT}/wave.webp", max_w=300, quality=84)

if "sun" in PARTS:
    W, H = 200, 200
    nx = Seq(7100)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    m = circles(W, H, [(100, 100, 84)])
    gaps = np.zeros((H, W), np.float32)
    for y, t in [(112, 5), (132, 8), (152, 10), (170, 12)]:
        gaps = np.maximum(gaps, ((yy > y) & (yy < y + t)).astype(np.float32))
    art = P(blank(W, H), np.clip(m - gaps, 0, 1), MUST, ORANGE, nx, rough=1.0)
    art = wear(art, 8, 0.06)
    prev(art, "sr-sun", tone=CREAM)
    save(art, f"{OUT}/sun.webp", max_w=100, quality=84)

if "palm" in PARTS:
    W, H = 360, 560
    rng = random.Random(13); nx = Seq(7300)
    art = P(blank(W, H), palm_tree(W, H, 210, 556, 470, rng, -0.18), INK, "#4a3028", nx, rough=1.2)
    art = wear(art, 21, 0.06)
    prev(art, "sr-palm", tone=CREAM)
    save(art, f"{OUT}/palm.webp", max_w=220, quality=82)
