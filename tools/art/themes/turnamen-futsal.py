"""Turnamen Futsal — bold sports-poster gouache: indoor futsal court in steep perspective (blue playing surface, orange
run-off, white lines, far goal and board panels), a futsal ball, a front-view goal with net, a foil-gold trophy, a
whistle on a lanyard and a blank team jersey.
Run: python3 -I turnamen-futsal.py [part ...]  parts: court ball goal trophy whistle jersey
Assets -> public/themes/art/turnamen-futsal/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m6_lib import *

OUT = outdir("turnamen-futsal")
PARTS = sys.argv[1:] or ["court", "ball", "goal", "trophy", "whistle", "jersey"]

COURT, COURT_D, COURT_L = "#2f6db5", "#24548f", "#4b89cf"
RUN, RUN_D = "#e8742c", "#bf5718"
LINE = "#f6f4ec"
NAVY, NAVY_D = "#16233f", "#0d1628"
LIME = "#c6e03a"
RED, RED_D = "#d63a2f", "#a5261e"
STEEL, STEEL_D, STEEL_L = "#b9c3cc", "#7d8a96", "#e4e9ee"


def ellipse_world(cu, cv, ru, rv, a0, a1, n=40):
    return [(cu + math.cos(a0 + (a1 - a0) * i / (n - 1)) * ru, cv + math.sin(a0 + (a1 - a0) * i / (n - 1)) * rv) for i in range(n)]


if "court" in PARTS:
    W, H = 780, 640
    rng = random.Random(3); nx = Seq(300)
    cx, yh, Hc, Wc, D = 390, -100, 800, 608, 2.2

    def P(u, v):
        z = 1 + v * D
        return (cx + u * Wc / z / 1.0, yh + Hc / z)

    def poly(pts_uv):
        return [P(u, v) for u, v in pts_uv]

    art = blank(W, H)
    # far wall: board panels + dark arena behind
    fy = P(0, 1.0)[1]
    wall = shapes(W, H, [rect(-10, fy - 70, W + 10, fy + 4)], smooth=False)
    art = GP(art, wall, NAVY, "#1d2f55", seed=nx(), rough=1.2, streak=1.2)
    panels = []
    for k in range(9):
        x0 = 112 + k * 62
        panels.append(rect(x0, fy - 34, x0 + 56, fy - 4))
    art = GP(art, shapes(W, H, panels[::2], smooth=False), LIME, "#a9c42c", seed=nx(), rough=0.8, streak=0.8)
    art = GP(art, shapes(W, H, panels[1::2], smooth=False), RUN, RUN_D, seed=nx(), rough=0.8, streak=0.8)
    # run-off (orange) and playing surface (blue)
    runm = shapes(W, H, [poly([(-1.35, -0.08), (1.35, -0.08), (1.35, 1.04), (-1.35, 1.04)])], smooth=False)
    art = GP(art, runm, RUN, RUN_D, seed=nx(), rough=1.2, streak=0.8)
    play = shapes(W, H, [poly([(-1, -0.08), (1, -0.08), (1, 1.0), (-1, 1.0)])], smooth=False)
    art = GP(art, play, COURT, COURT_L, seed=nx(), rough=1.0, streak=0.7)
    # depth shading + floodlight sheen
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = play * np.exp(-(((xx - 330) / 200) ** 2 + ((yy - 380) / 160) ** 2))
    art = G(art, sheen * 0.8, "#8fb8e6", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=1)
    far = play * np.clip(1 - (yy - fy) / 200, 0, 1)
    art = G(art, far * 0.7, COURT_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # floor boards hint (perspective seams)
    seams = [([P(u, -0.08), P(u, 1.0)], 1.0, None) for u in np.linspace(-0.9, 0.9, 13)]
    art = G(art, strokes(W, H, seams) * play * 0.5, COURT_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    clear()
    # white lines (width shrinks with depth)
    def wline(pts_uv, w=6.0):
        items = []
        for i in range(len(pts_uv) - 1):
            (u0, v0), (u1, v1) = pts_uv[i], pts_uv[i + 1]
            z = 1 + (v0 + v1) / 2 * D
            items.append(([P(u0, v0), P(u1, v1)], max(1.2, w / z * 1.6), None))
        return items
    L = []
    L += wline([(-1, -0.08), (-1, 1.0), (1, 1.0), (1, -0.08)])
    L += wline([(-1, 0.5), (1, 0.5)])
    L += wline(ellipse_world(0, 0.5, 0.3, 0.075, 0, math.tau, 48))
    L += wline(ellipse_world(0, 1.0, 0.62, 0.15, math.pi, math.tau, 30))
    L += wline(ellipse_world(0, 0.0, 0.62, 0.15, 0.0, math.pi, 30))
    lm = strokes(W, H, L)
    spots = circles(W, H, [(*P(0, 0.5), 4), (*P(0, 0.85), 3), (*P(0, 0.75), 2.6)])
    def chalk(m):
        rgb = np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(LINE), np.float32)
        wear = 1 - 0.35 * np.clip((fbm(m.shape[1], m.shape[0], 77, 8, 2) - 0.6) * 4, 0, 1)
        return np.concatenate([rgb, np.clip(m * wear, 0, 1)[..., None]], -1)
    art = OV(art, np.clip(gaussian_filter(lm, 0.5) + spots, 0, 1), chalk)
    # far goal: frame + net
    gl, gr = P(-0.15, 1.0), P(0.15, 1.0)
    gh = (gr[0] - gl[0]) * 0.67
    net = shapes(W, H, [[(gl[0] + 4, gl[1] - gh + 6), (gr[0] - 4, gr[1] - gh + 6), (gr[0] - 10, gr[1] - 6), (gl[0] + 10, gl[1] - 6)]], smooth=False)
    art = G(art, net, "#dfe6ee", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=0.6)
    mesh = [([(x, gl[1] - gh + 4), (x, gl[1])], 0.8, None) for x in np.arange(gl[0] + 6, gr[0] - 4, 5)]
    mesh += [([(gl[0], y), (gr[0], y)], 0.8, None) for y in np.arange(gl[1] - gh + 6, gl[1], 5)]
    art = G(art, strokes(W, H, mesh) * 0.7, "#ffffff", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3)
    frame = strokes(W, H, [([gl, (gl[0], gl[1] - gh), (gr[0], gr[1] - gh), gr], 4.2, None)])
    art = GP(art, frame, "#ffffff", "#e9e9e9", seed=nx(), rough=0.4)
    stripes_ = strokes(W, H, [([(gl[0], gl[1] - gh * f), (gl[0], gl[1] - gh * (f + 0.12))], 4.2, None) for f in (0.15, 0.45, 0.75)]
                      + [([(gr[0], gr[1] - gh * f), (gr[0], gr[1] - gh * (f + 0.12))], 4.2, None) for f in (0.15, 0.45, 0.75)]
                      + [([(gl[0] + (gr[0] - gl[0]) * f, gl[1] - gh), (gl[0] + (gr[0] - gl[0]) * (f + 0.08), gl[1] - gh)], 4.2, None) for f in (0.1, 0.3, 0.5, 0.7, 0.9)])
    art = GP(art, stripes_, RED, seed=nx(), rough=0.3)
    pv(art, "tf-court", "#0e1726")
    save(art, f"{OUT}/court.webp", max_w=780, quality=76)
    clear()

if "ball" in PARTS:
    W = H = 260
    rng = random.Random(5); nx = Seq(500)
    cx = cy = 130; r = 110
    art = blank(W, H)
    disc = circles(W, H, [(cx, cy, r)])
    art = GP(art, disc, "#f7f5ee", "#e9e6dc", seed=nx(), rough=0.8, streak=0.6)
    # pentagon patches on a sphere-ish projection
    def pent(px, py, s, rot, squash=1.0, ang=0.0):
        pts = []
        for k in range(5):
            a = rot + k / 5 * math.tau
            x, y = math.cos(a) * s, math.sin(a) * s * squash
            pts.append((px + x * math.cos(ang) - y * math.sin(ang), py + x * math.sin(ang) + y * math.cos(ang)))
        return pts
    centre = pent(cx - 6, cy - 8, 34, -math.pi / 2)
    ring = []
    for k in range(5):
        a = -math.pi / 2 + math.pi / 5 + k / 5 * math.tau
        px, py = cx - 6 + math.cos(a) * 88, cy - 8 + math.sin(a) * 88
        ring.append(pent(px, py, 30, a + math.pi, 0.55, a + math.pi / 2))
    pm = shapes(W, H, [centre], smooth=False)
    rm = shapes(W, H, ring, smooth=False) * disc
    art = GP(art, pm, NAVY, "#22345c", seed=nx(), rough=0.8)
    art = GP(art, rm, RUN, RUN_D, seed=nx(), rough=0.8)
    seams = []
    for k in range(5):
        a = -math.pi / 2 + k / 5 * math.tau
        seams.append(([centre[k], (cx - 6 + math.cos(a) * 64, cy - 8 + math.sin(a) * 64)], 2.2, None))
    art = GP(art, strokes(W, H, seams) * disc * 0.7, "#9a978c", seed=nx(), rough=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = disc * np.clip(((xx - cx + 40) ** 2 + (yy - cy + 50) ** 2) ** 0.5 / r - 0.75, 0, 1) * 1.4
    art = G(art, np.clip(shade, 0, 1) * 0.9, "#3a4a6b", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1)
    hl = ellipses(W, H, [(cx - 46, cy - 52, 26, 14, -35)]) * disc
    art = GP(art, gaussian_filter(hl, 2) * 0.8, "#ffffff", seed=nx(), rough=0.5)
    rim = np.clip(disc - np.clip(gaussian_filter(disc, 3) * 1.5 - 0.5, 0, 1), 0, 1)
    art = GP(art, rim * 0.9, NAVY, seed=nx(), rough=0.5)
    pv(art, "tf-ball", "#0e1726")
    save(art, f"{OUT}/ball.webp", max_w=180, quality=84)

if "goal" in PARTS:
    W, H = 560, 340
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    x0, x1, y0, y1 = 40, 520, 40, 320
    net = shapes(W, H, [rect(x0 + 6, y0 + 6, x1 - 6, y1)], smooth=False)
    art = G(art, net, "#cfd8e3", seed=nx(), density=0.22, edge=0.2, bloom=0, rough=0.5)
    mesh = []
    for x in np.arange(x0 + 10, x1, 16):
        mesh.append((curve([(x, y0 + 8), (x + rng.uniform(-2, 2), (y0 + y1) / 2 + 8), (x + rng.uniform(-3, 3), y1)], 10), 1.4, None))
    for y in np.arange(y0 + 18, y1, 16):
        mesh.append((curve([(x0 + 8, y), ((x0 + x1) / 2, y + 6), (x1 - 8, y)], 16), 1.4, None))
    art = GP(art, strokes(W, H, mesh) * 0.85, "#f4f6f8", seed=nx(), rough=0.4)
    frame = strokes(W, H, [([(x0, y1), (x0, y0), (x1, y0), (x1, y1)], 16, None)])
    art = GP(art, frame, "#ffffff", "#ebebeb", seed=nx(), rough=0.6, streak=0.8)
    reds = []
    for f in (0.12, 0.38, 0.64, 0.9):
        reds.append(([(x0, y0 + (y1 - y0) * f), (x0, y0 + (y1 - y0) * (f + 0.12))], 16, None))
        reds.append(([(x1, y0 + (y1 - y0) * f), (x1, y0 + (y1 - y0) * (f + 0.12))], 16, None))
    for f in (0.05, 0.25, 0.45, 0.65, 0.85):
        reds.append(([(x0 + (x1 - x0) * f, y0), (x0 + (x1 - x0) * (f + 0.1), y0)], 16, None))
    art = GP(art, strokes(W, H, reds), RED, RED_D, seed=nx(), rough=0.5)
    shade = strokes(W, H, [([(x0 + 6, y0 + 8), (x1 - 6, y0 + 8)], 4, None), ([(x0 + 6, y0 + 6), (x0 + 6, y1)], 3, None)])
    art = G(art, shade * 0.6, "#6e7c8c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    pv(art, "tf-goal", "#0e1726")
    save(art, f"{OUT}/goal.webp", max_w=360, quality=80)

if "trophy" in PARTS:
    W, H = 300, 380
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    cup = [(64, 40), (236, 40), (226, 110), (196, 168), (166, 190), (134, 190), (104, 168), (74, 110)]
    stem = [(136, 186), (164, 186), (158, 240), (176, 262), (124, 262), (142, 240)]
    hl = strokes(W, H, [(arc_pts(66, 92, 44, math.pi * 0.5, math.pi * 1.5, 24, 1.0), 12, None)])
    hr = strokes(W, H, [(arc_pts(234, 92, 44, -math.pi * 0.5, math.pi * 0.5, 24, 1.0), 12, None)])
    gold = np.clip(shapes(W, H, [cup, stem], smooth=False) + hl + hr, 0, 1)
    art = FO(art, gold, "#d4a338", seed=nx(), emboss=0.8, sparkle=0.15)
    rimm = shapes(W, H, [rect(58, 34, 242, 50)], smooth=False)
    art = FO(art, rimm, "#e4bb55", seed=nx(), emboss=0.9)
    star = []
    for k in range(10):
        a = -math.pi / 2 + k / 10 * math.tau
        rr = 24 if k % 2 == 0 else 10
        star.append((150 + math.cos(a) * rr, 104 + math.sin(a) * rr))
    art = GP(art, shapes(W, H, [star], smooth=False) * 0.85, "#fff1bf", seed=nx(), rough=0.4)
    base = shapes(W, H, [rect(96, 262, 204, 300), rect(84, 300, 216, 350)], smooth=False)
    art = GP(art, base, NAVY, "#24365e", seed=nx(), rough=0.6, streak=1)
    plate = shapes(W, H, [rect(112, 312, 188, 336)], smooth=False)
    art = FO(art, plate, "#cfa23c", seed=nx(), emboss=0.6)
    pv(art, "tf-trophy", "#0e1726")
    save(art, f"{OUT}/trophy.webp", max_w=200, quality=84)

if "whistle" in PARTS:
    W, H = 260, 200
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    cord = strokes(W, H, [(curve([(60, 110), (30, 60), (70, 18), (130, 20), (170, 50)], 30), 7, None)])
    art = GP(art, cord, RUN, RUN_D, seed=nx(), rough=0.6, streak=0.8)
    ring = strokes(W, H, [(arc_pts(66, 112, 12, 0, math.tau, 24), 4, None)])
    art = GP(art, ring, STEEL_D, seed=nx(), rough=0.3)
    body = shape_mask(W, H, ellipse_pts(130, 130, 52, 42, 16))
    mouth = shapes(W, H, [[(150, 92), (238, 96), (238, 124), (150, 128)]], smooth=False)
    m = np.clip(body + mouth, 0, 1)
    art = GP(art, m, STEEL, STEEL_L, seed=nx(), rough=0.5, streak=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, m * np.clip((yy - 120) / 50, 0, 1) * 0.9, STEEL_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6)
    art = GP(art, gaussian_filter(ellipses(W, H, [(110, 110, 20, 9, -25), (200, 102, 30, 4, 0)]), 1.2) * m * 0.8, "#ffffff", seed=nx(), rough=0.3)
    hole = ellipses(W, H, [(164, 104, 12, 6, 0)])
    art = GP(art, hole, "#3b4652", seed=nx(), rough=0.3)
    pv(art, "tf-whistle", "#f2efe6")
    save(art, f"{OUT}/whistle.webp", max_w=120, quality=84)

if "jersey" in PARTS:
    W, H = 360, 360
    rng = random.Random(13); nx = Seq(1300)
    art = blank(W, H)
    shirt = [(120, 40), (150, 52), (180, 56), (210, 52), (240, 40), (320, 82), (296, 150), (262, 136), (262, 330), (98, 330), (98, 136), (64, 150), (40, 82)]
    sm = shapes(W, H, [shirt], smooth=False)
    art = GP(art, sm, RUN, "#f08a43", seed=nx(), rough=1.0, streak=1.2)
    side = sm * np.clip((np.arange(W)[None, :] - 220) / 60, 0, 1)
    art = G(art, side * 0.7, RUN_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    trim = strokes(W, H, [([(40, 82), (64, 150)], 12, None), ([(320, 82), (296, 150)], 12, None), ([(98, 322), (262, 322)], 10, None)])
    art = GP(art, trim * sm, NAVY, seed=nx(), rough=0.5)
    collar = strokes(W, H, [(curve([(124, 42), (152, 72), (180, 80), (208, 72), (236, 42)], 20), 12, None)])
    art = GP(art, collar, NAVY, "#22345c", seed=nx(), rough=0.5)
    band = strokes(W, H, [([(100, 200), (260, 170)], 18, None)])
    art = GP(art, band * sm, LIME, "#a9c42c", seed=nx(), rough=0.6)
    folds = strokes(W, H, [(curve([(130, 150), (140, 230), (128, 310)], 10), 3, (0.2, 0.2)), (curve([(225, 160), (230, 240), (240, 310)], 10), 3, (0.2, 0.2))])
    art = G(art, folds * sm * 0.7, RUN_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.5)
    pv(art, "tf-jersey", "#0e1726")
    save(art, f"{OUT}/jersey.webp", max_w=220, quality=84)

kb(OUT)
