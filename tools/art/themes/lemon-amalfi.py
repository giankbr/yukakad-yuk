"""Lemon Amalfi — bright watercolour + glazed maiolica: cliffside village of pastel houses with a tiled dome above lemon
terraces and a turquoise sea; lemon branches; hand-painted blue-yellow maiolica tile.
Run: python3 -I lemon-amalfi.py [part ...]   parts: coast lemons lemon tile band
Assets -> public/themes/art/lemon-amalfi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f4_lib import *

OUT = outdir("lemon-amalfi")
PARTS = sys.argv[1:] or ["coast", "lemons", "lemon", "tile", "band"]

LEMON, LEMON_L, LEMON_D = "#f5cf2e", "#fbe679", "#d9a514"
LEAF_L, LEAF_M, LEAF_D = "#8fb45a", "#5d8a3c", "#3c6430"
COBALT, COBALT_L = "#1f4f9c", "#5b86c8"
SEA, SEA_D, SEA_L = "#2c9bb8", "#1d5f95", "#7fd0d6"
HOUSES = ["#f7c89a", "#f3dc8a", "#f2b8a6", "#fbf3e6", "#e9a77d", "#f6e4c2", "#cfe0d6"]


def lemon_shape(x, y, L, ang, rng):
    """Lemon outline: ellipse with pointed nipple at one end and a stem bump at the other."""
    pts = []
    for i in range(40):
        t = i / 40 * math.tau
        r = 1 + 0.18 * math.exp(-((t % math.tau) / 0.22) ** 2) + 0.18 * math.exp(-(((t - math.tau) % math.tau - math.tau) / 0.22) ** 2) + 0.07 * math.exp(-((t - math.pi) / 0.3) ** 2)
        ex, ey = math.cos(t) * L / 2 * r, math.sin(t) * L * 0.36
        pts.append((x + ex * math.cos(ang) - ey * math.sin(ang), y + ex * math.sin(ang) + ey * math.cos(ang)))
    return deform(pts, rng, 1, 0.01)


def paint_lemon(art, W, H, x, y, L, ang, rng, nx, light=(-1, -1)):
    m = shape_mask(W, H, lemon_shape(x, y, L, ang, rng))
    art = G(art, m, LEMON, LEMON_L, seed=nx(), density=0.88, edge=0.5, bloom=0.25, rough=2.0, gran=0.15)
    # form shadow (lower right), warm reflected light, highlight (left top), pitted peel speckle
    sh = inner_shade(m, int(L * 0.12), int(L * 0.12), blur=L * 0.12)
    art = G(art, sh * 1.2, LEMON_D, "#c98a12", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=2)
    art = G(art, np.clip(sh - 0.6, 0, 1) * 2, "#9a8a2a", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
    hl = ellipses(W, H, [(x - L * 0.16 * math.cos(ang) + L * .1 * math.sin(ang), y - L * 0.16 * math.sin(ang) - L * 0.13, L * 0.16, L * 0.06, math.degrees(ang) - 10)])
    art = OV(art, soft(hl, L * 0.04) * m * 0.55, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb("#fffbe0"), np.float32), mm[..., None]], -1))
    pits = m * (np.random.default_rng(nx()).random(m.shape) > 0.985) * 0.5
    art = OV(art, gaussian_filter(pits.astype(np.float32), 0.6) * 2, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb("#c99a10"), np.float32), np.clip(mm, 0, .5)[..., None]], -1))
    return art, m


def paint_leaf(art, W, H, x, y, L, ang, rng, nx, cols=(LEAF_L, LEAF_M), curl=0.0):
    pts = petal_pts(x, y, L, L * 0.21, ang, n=18, cup=curl)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.02))
    art = G(art, m, cols[0], cols[1], seed=nx(), density=0.82, edge=0.55, bloom=0.35, rough=2.2, gran=0.2)
    # half-leaf shade + midrib left as a lighter line
    ca, sa = math.cos(ang), math.sin(ang)
    half = m * (((np.mgrid[0:H, 0:W][1] - x) * -sa + (np.mgrid[0:H, 0:W][0] - y) * ca) > 0)
    art = G(art, half, LEAF_D, seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1.5)
    rib = strokes(W, H, [([(x + ca * L * .05, y + sa * L * .05), (x + ca * L * .9, y + sa * L * .9)], 1.6, (0.0, 0.5))])
    art = OV(art, rib * m * 0.6, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb("#c9dd8f"), np.float32), mm[..., None]], -1))
    return art


def paint_blossom(art, W, H, x, y, r, rng, nx):
    pet = [petal_pts(x, y, r, r * 0.42, a, n=10) for a in np.linspace(0, math.tau, 6)[:5] + rng.uniform(0, 1)]
    m = shapes(W, H, pet)
    art = G(art, m, "#fbf8f2", "#f6e1e6", seed=nx(), density=0.5, edge=0.7, bloom=0.2, rough=1)
    art = G(art, circles(W, H, [(x, y, r * 0.22)]), "#e9c23a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.6)
    return art


def branch(W, H, nx, rng, lemons, leaves, twig, blossoms=()):
    art = blank(W, H)
    tw = strokes(W, H, [(t, w, (0.02, 0.4)) for t, w in twig])
    art = G(art, tw, "#7a6040", "#5a4632", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1.2, feather=0.8)
    for (x, y, L, a, cur) in leaves:
        art = paint_leaf(art, W, H, x, y, L, a, rng, nx, curl=cur)
    for (x, y, L, a) in lemons:
        art, m = paint_lemon(art, W, H, x, y, L, a, rng, nx)
    for (x, y, r) in blossoms:
        art = paint_blossom(art, W, H, x, y, r, rng, nx)
    return art


if "coast" in PARTS:
    W, H = 720, 900
    nx = Seq(40100)
    rng = random.Random(11)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    edge_f = lambda y: np.interp(y, [0, 230, 330, 470, 620, 780, 900], [0, 120, 230, 360, 470, 540, 580])   # cliff edge x per y
    cliff = (xx < edge_f(yy) + 30 * (fbm(W, H, 3, 50, 2) - .5)).astype(np.float32) * (yy > 150 + 60 * (xx / 400))
    sky = (1 - cliff) * (yy < 430)
    sea = (1 - cliff) * (yy >= 410)
    art = G(art, sky * np.clip(1 - yy / 460, 0, 1), "#8cc7e6", "#b5dcef", seed=nx(), density=0.75, edge=0.15, bloom=0.5, rough=10, holes=0.04)
    # far headland across the bay (hazy)
    far = shapes(W, H, [[(380, 430), (470, 380), (560, 360), (650, 372), (740, 392), (740, 440), (380, 440)]])
    art = G(art, far * (1 - cliff), "#9fb6c4", "#b9c6cf", seed=nx(), density=0.55, edge=0.4, bloom=0.3, rough=4)
    art = G(art, sea, SEA_L, SEA, seed=nx(), density=0.8, edge=0.2, bloom=0.4, rough=8)
    art = G(art, sea * np.clip((yy - 430) / 420, 0, 1) ** 0.8, SEA_D, "#2a6fa4", seed=nx(), density=0.65, edge=0.1, bloom=0.3, rough=8)
    # sparkle: paper-white dashes lifted out of the sea
    sp = strokes(W, H, [([(x, y), (x + L * .5, y - 1), (x + L, y + .5)], rng.uniform(1.2, 2.6), (0.3, 0.3)) for x, y, L in [(rng.uniform(300, 720), rng.uniform(440, 880), rng.uniform(5, 30)) for _ in range(55)]]) * sea
    art = OV(art, sp * 0.8, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#f4fbfb"), np.float32), m[..., None]], -1))
    # boats with wakes
    for bx, by, s in [(560, 560, 1.0), (640, 700, 1.3), (470, 820, 1.5)]:
        art = G(art, lines(W, H, [(bx - 34 * s, by + 3, bx - 4, by + 1)], 3 * s) * sea, "#e9f6f7", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1)
        art = G(art, shapes(W, H, [[(bx - 8 * s, by - 3 * s), (bx + 10 * s, by - 3 * s), (bx + 6 * s, by + 2 * s), (bx - 6 * s, by + 2 * s)]], smooth=False), "#ffffff", "#f6e2b0", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    # cliff body: warm ochre rock with green scrub, darker in the cracks
    art = G(art, cliff, "#d8b98a", "#c6a274", seed=nx(), density=0.75, edge=0.45, bloom=0.4, rough=6, gran=0.35)
    scrub = cliff * np.clip((fbm(W, H, 17, 26, 3) - 0.48) * 3.5, 0, 1)
    art = G(art, scrub, "#7f9f55", "#5d8040", seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=4, gran=0.25)
    rockshade = cliff * np.clip(1 - (edge_f(yy) - xx) / 80, 0, 1)
    art = G(art, rockshade, "#9b7a5c", "#7a6a7c", seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=5)
    # lemon terraces with pergola posts on the lower slope
    terr = []
    for k, ty in enumerate(range(626, 900, 32)):
        x1 = edge_f(ty) - 26
        wall_ = rects(W, H, [(-10, ty + 20, x1, ty + 26)]) * cliff
        art = G(art, wall_, "#c9b08c", "#ad9372", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1.2)
        cans = [(x, ty + 8 + rng.uniform(-3, 3), rng.uniform(11, 16)) for x in np.arange(rng.uniform(0, 14), x1 - 8, rng.uniform(17, 22))]
        cm = circles(W, H, cans) * cliff
        art = G(art, cm, "#7fa64e", "#5b8a3e", seed=nx(), density=0.85, edge=0.55, bloom=0.3, rough=2.5, gran=0.25)
        art = G(art, circles(W, H, [(x + r * .35, y + r * .3, r * .6) for x, y, r in cans]) * cliff, "#3f6a34", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=1.5)
        dots = circles(W, H, [(x + rng.uniform(-r, r) * .7, y + rng.uniform(-r, r) * .6, rng.uniform(2.2, 3.4)) for x, y, r in cans for _ in range(3)]) * cliff
        art = G(art, dots, LEMON, LEMON_L, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    # village: stacked pastel houses on the cliff
    houses = []
    for row, (y0, xa, xb) in enumerate([(300, 40, 200), (360, 10, 280), (420, 0, 340), (480, 0, 380), (540, 20, 430), (590, 60, 440)]):
        x = xa + rng.uniform(-10, 10)
        while x < min(xb, edge_f(y0 + 40) - 30):
            w = rng.uniform(34, 62); h = rng.uniform(44, 70)
            houses.append((x, y0 - h + rng.uniform(-6, 6), x + w, y0 + 18, rng.choice(HOUSES)))
            x += w + rng.uniform(-6, 4)
    houses.sort(key=lambda r: r[3])
    for (x0, y0, x1, y1, c) in houses:
        hm = rects(W, H, [(x0, y0, x1, y1)])
        art = G(art, hm, c, mix(c, "#ffffff", .3), seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=1.2, feather=0.8)
        # shaded side wall (sun from the upper left)
        art = G(art, rects(W, H, [(x1 - (x1 - x0) * 0.22, y0, x1, y1)]), "#b8a2b4", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1)
        wins = []
        for wx in np.arange(x0 + 7, x1 - 10, 13):
            for wy in np.arange(y0 + 10, y1 - 14, 18):
                if rng.random() < 0.7:
                    wins.append((wx, wy, wx + 5, wy + 9))
        art = G(art, rects(W, H, wins), "#3d5a7a", "#5f6f7a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.6, feather=0.5)
        if rng.random() < 0.35:
            art = G(art, rects(W, H, [(x0 - 2, y0 - 6, x1 + 2, y0 + 2)]), "#c9775a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.8)
    # church: nave, bell tower and the maiolica dome (yellow/green/blue segments)
    cx, cy = 160, 318
    nave = rects(W, H, [(cx - 40, cy - 40, cx + 40, cy + 20)])
    tower = rects(W, H, [(cx + 46, cy - 110, cx + 70, cy + 20)])
    art = G(art, np.maximum(nave, tower), "#fbf4e6", "#f1e0c4", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1)
    art = G(art, rects(W, H, [(cx + 50, cy - 100, cx + 66, cy - 84), (cx - 6, cy - 22, cx + 6, cy + 4)]), "#4a5a6a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.5)
    art = G(art, shapes(W, H, [[(cx + 44, cy - 110), (cx + 58, cy - 132), (cx + 72, cy - 110)]], smooth=False), "#2e8a6a", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.6)
    drum = rects(W, H, [(cx - 26, cy - 62, cx + 26, cy - 40)])
    art = G(art, drum, "#fbf4e6", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.6)
    dome = shapes(W, H, [[(cx - 30, cy - 60)] + arc_pts(cx, cy - 60, 30, math.pi, math.tau, 24, 1.15) + [(cx + 30, cy - 60)]], smooth=False)
    segs = np.zeros((H, W), np.float32)
    ang = np.arctan2(yy - (cy - 60), xx - cx)
    seg_id = ((ang + math.pi) / (math.pi / 8)).astype(int) % 3
    art = G(art, dome * (seg_id == 0), LEMON, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    art = G(art, dome * (seg_id == 1), "#2e8a6a", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    art = G(art, dome * (seg_id == 2), COBALT_L, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    art = G(art, inner_shade(dome, 6, 4, 6) * 1.5, "#3a3a5a", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5)
    art = G(art, circles(W, H, [(cx, cy - 98, 4)]), "#d9a514", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.3)
    # a few cypress/pine accents between houses
    for px, py in [(250, 420), (330, 520), (90, 470)]:
        art = G(art, ellipses(W, H, [(px, py, 9, 26, 0)]), "#3f6a3a", "#2e5530", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.5)
    # unfinished soft edge
    e = np.clip((displace(gaussian_filter(rect_m(W, H, 14, 14, W - 14, H - 14), 8), 99, 12, 40) - 0.25) * 1.8, 0, 1)
    art[..., 3] *= e
    preview(art, "la-coast", tone="#fffaf0")
    comp = np.asarray(on_paper(art, "#fffaf0"), np.float32) / 255
    save_rgb(np.concatenate([comp, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/coast.webp", size=(560, 700), quality=78)
    clear()

if "lemons" in PARTS:
    W, H = 640, 460
    nx = Seq(41100)
    rng = random.Random(21)
    twig = [(curve([(10, 60), (160, 90), (300, 110), (460, 96), (620, 70)], 40), 8), (curve([(300, 110), (300, 170), (290, 210)], 12), 5),
            (curve([(160, 90), (170, 150), (180, 200)], 12), 4), (curve([(460, 96), (470, 150), (480, 190)], 12), 4)]
    leaves = [(40, 70, 120, -0.6, 0.1), (80, 80, 130, 0.45, -0.1), (140, 88, 120, -1.2, 0.1), (230, 104, 140, 0.3, 0.1), (260, 104, 120, -0.9, -0.1),
              (360, 110, 130, 0.6, 0.1), (400, 104, 140, -0.4, -0.1), (520, 86, 120, 0.9, 0.1), (560, 80, 130, -0.7, 0.1), (600, 74, 110, 0.2, -0.1),
              (330, 110, 110, 2.1, 0.1), (440, 100, 100, 2.4, -0.1), (110, 86, 100, 2.6, 0.1)]
    lemons = [(182, 262, 150, 1.45), (298, 300, 168, 1.62), (482, 252, 140, 1.35)]
    art = branch(W, H, nx, rng, lemons, leaves, twig, blossoms=[(560, 150, 26), (90, 150, 22)])
    preview(art, "la-lemons", tone="#fffaf0")
    save(art, f"{OUT}/lemons.webp", max_w=480, quality=82)
    clear()

if "lemon" in PARTS:
    W, H = 260, 220
    nx = Seq(42100)
    rng = random.Random(31)
    art = branch(W, H, nx, rng, [(140, 130, 150, 0.2)], [(70, 60, 110, -0.35, 0.1), (80, 64, 100, 0.55, -0.1)], [(curve([(50, 58), (90, 70), (110, 92)], 10), 5)])
    preview(art, "la-lemon", tone="#fffaf0")
    save(art, f"{OUT}/lemon.webp", max_w=150, quality=84)
    clear()


def maiolica_tile(S, nx, rng, seed=1):
    """One glazed tile: tin-white ground, cobalt quarter-rings in the corners (they join into circles when tiled), a
    lemon pair with leaves in the centre, small blue flowers on the edges; painted with brushy pigment, then glazed."""
    art = solid(S, S, "#fbf8ef")
    art[..., :3] *= (0.985 + 0.02 * fbm(S, S, seed, 40, 2))[..., None]
    c = S / 2
    rings = np.zeros((S, S), np.float32)
    for (x, y) in [(0, 0), (S, 0), (0, S), (S, S)]:
        rings = np.maximum(rings, np.clip(circles(S, S, [(x, y, S * 0.36)]) - circles(S, S, [(x, y, S * 0.3)]), 0, 1))
    art = G(art, rings, COBALT, COBALT_L, seed=nx(), density=0.85, edge=0.45, bloom=0.25, rough=1.5, feather=0.7, pad=6)
    inner = np.zeros((S, S), np.float32)
    for (x, y) in [(0, 0), (S, 0), (0, S), (S, S)]:
        inner = np.maximum(inner, circles(S, S, [(x, y, S * 0.24)]))
    art = G(art, inner, LEMON, "#f0b62a", seed=nx(), density=0.8, edge=0.45, bloom=0.2, rough=1.4, feather=0.7, pad=6)
    petals = []
    for (x, y) in [(0, 0), (S, 0), (0, S), (S, S)]:
        for a in np.linspace(0, math.tau, 9)[:8]:
            petals.append(petal_pts(x, y, S * 0.2, S * 0.05, a, n=10))
    art = G(art, shapes(S, S, petals), "#e08a1e", seed=nx(), density=0.55, edge=0.5, bloom=0.1, rough=1, feather=0.6, pad=6)
    # centre diamond frame + lemons + leaves
    dia = [(c, c - S * 0.3), (c + S * 0.3, c), (c, c + S * 0.3), (c - S * 0.3, c)]
    dm = np.clip(shapes(S, S, [dia], smooth=False) - shapes(S, S, [[(c, c - S * 0.26), (c + S * 0.26, c), (c, c + S * 0.26), (c - S * 0.26, c)]], smooth=False), 0, 1)
    art = G(art, dm, COBALT, seed=nx(), density=0.75, edge=0.4, bloom=0.1, rough=1, feather=0.6, pad=6)
    lv = [petal_pts(c, c, S * 0.2, S * 0.055, a, n=12) for a in (-2.6, -0.55)]
    art = G(art, shapes(S, S, lv), LEAF_M, LEAF_L, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1, feather=0.6, pad=6)
    lm = shapes(S, S, [lemon_shape(c - S * 0.06, c + S * 0.06, S * 0.2, 1.25, rng), lemon_shape(c + S * 0.07, c + S * 0.04, S * 0.19, 1.85, rng)])
    art = G(art, lm, LEMON, LEMON_D, seed=nx(), density=0.92, edge=0.55, bloom=0.2, rough=1, feather=0.6, pad=6)
    dots = circles(S, S, [(c, 4, S * 0.03), (c, S - 4, S * 0.03), (4, c, S * 0.03), (S - 4, c, S * 0.03)])
    art = G(art, dots, COBALT, seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5, feather=0.5, pad=4)
    # glaze: soft specular band + grout shadow at the edges
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    sheen = np.exp(-(((xx + yy) - S * 0.7) / (S * 0.18)) ** 2) * 0.12
    art[..., :3] = np.clip(art[..., :3] + sheen[..., None], 0, 1)
    d = np.minimum.reduce([xx, yy, S - 1 - xx, S - 1 - yy])
    art[..., :3] *= (1 - 0.18 * np.exp(-d / 2.2))[..., None]
    return art


if "tile" in PARTS:
    S = 240
    nx = Seq(43100)
    rng = random.Random(41)
    t = maiolica_tile(S, nx, rng)
    preview(t, "la-tile", bg="#ffffff")
    save_rgb(t, f"{OUT}/tile.webp", size=(180, 180), quality=80)
    clear()

if "band" in PARTS:
    # running border: blue-yellow scallop band (repeat-x, 240 wide)
    W, H = 240, 64
    nx = Seq(44100)
    art = solid(W, H, "#fbf8ef")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    top = rect_m(W, H, 0, 0, W, 10) + rect_m(W, H, 0, H - 10, W, H)
    art = G(art, top, COBALT, seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1, feather=0.6, pad=4)
    sc = circles(W, H, [(30 + i * 60, H / 2, 18) for i in range(-1, 5)])
    art = G(art, sc, LEMON, "#f0b62a", seed=nx(), density=0.85, edge=0.45, bloom=0.2, rough=1, feather=0.6, pad=4)
    art = G(art, circles(W, H, [(30 + i * 60, H / 2, 7) for i in range(-1, 5)]), "#e08a1e", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.6, feather=0.5, pad=4)
    lv = [petal_pts(60 * i, H / 2, 22, 7, a, n=10) for i in range(0, 5) for a in (0.0, math.pi)]
    art = G(art, shapes(W, H, lv), LEAF_M, LEAF_L, seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1, feather=0.6, pad=4)
    art = G(art, circles(W, H, [(60 * i, H / 2, 4) for i in range(0, 5)]), COBALT, seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5, feather=0.5, pad=4)
    preview(art, "la-band", bg="#ffffff")
    save_rgb(art, f"{OUT}/band.webp", quality=82)
    clear()

kb(OUT)
