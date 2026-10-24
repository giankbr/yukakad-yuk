"""Rumah Baloy — the Baloy hall of the Tidung people on stilts over the calm sea of Tarakan, painted in matte gouache:
green walls, yellow carved trim, red accents, a sirap (ironwood shingle) roof with a carved sunburst gable, mangroves
with arched prop roots on both sides, reflections in the water. Plus a seamless carved trim band, a carved flower
divider, a mangrove clump and a carved node emblem.
Run: python3 -I rumah-baloy.py [part ...]  parts: baloy band divider bakau kembang
Assets -> public/themes/art/rumah-baloy/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s5_lib import *

OUT = outdir("rumah-baloy")
PARTS = sys.argv[1:] or ["baloy", "band", "divider", "bakau", "kembang"]
GREEN, GREEN_D, GREEN_L = "#2f7d4f", "#1f5a39", "#4f9a63"
YEL, YEL_D, YEL_L = "#f0c234", "#c8961c", "#f8dc6c"
RED, RED_D = "#c4372c", "#93261f"
ROOF, ROOF_D, ROOF_L = "#5a3324", "#3b2017", "#7a4a33"
WOOD, WOOD_D = "#7b5636", "#553a24"
SEA, SEA_D, SEA_L = "#2f8c8a", "#1d5f62", "#7cc0b6"
MANG, MANG_D, MANG_L = "#2c5a32", "#1b3d22", "#4f7f45"
WHITE = "#f7f0dc"


def mangrove(art, W, H, x, y, s, seed, flip=1):
    """Mangrove clump: arched prop roots into the water, layered round leaf masses."""
    rng = random.Random(seed)
    roots = []
    for i in range(9):
        rx = x + flip * rng.uniform(-0.9, 0.9) * s
        top = (x + flip * rng.uniform(-0.3, 0.3) * s, y - s * 0.55)
        roots.append(curve([top, ((top[0] + rx) / 2 + rng.uniform(-10, 10), y - s * 0.62 + rng.uniform(-8, 8)), (rx, y + rng.uniform(-4, 6))], 18))
    art = GP(art, strokes(W, H, [(r, s * 0.045, (0.0, 0.1)) for r in roots]), WOOD_D, "#3e2a1a", seed=seed, rough=0.8, streak=0.5)
    trunk = [((x, y - s * 0.5), (x + flip * s * 0.06, y - s * 1.1))]
    art = GP(art, strokes(W, H, [(list(t), s * 0.09, (0.0, 0.2)) for t in trunk]), WOOD_D, seed=seed + 1, rough=0.8)
    blobs = []
    for i in range(16):
        a = rng.uniform(math.pi, math.tau)
        rr = rng.uniform(0.15, 1.0)
        blobs.append((x + math.cos(a) * s * 1.05 * rr, y - s * 1.15 + math.sin(a) * s * 0.55 * rr, s * rng.uniform(0.28, 0.42), s * rng.uniform(0.2, 0.3), rng.uniform(-20, 20)))
    m = ellipses(W, H, blobs)
    art = GP(art, m, MANG, MANG_D, seed=seed + 2, rough=3.0, streak=0.7)
    hi = ellipses(W, H, [(bx - s * 0.06, by - s * 0.07, rx * 0.6, ry * 0.5, r) for bx, by, rx, ry, r in blobs[::2]])
    art = GP(art, hi * m, MANG_L, seed=seed + 3, rough=2.0, density=0.75)
    # leaf dabs
    dabs = [petal_pts(x + rng.uniform(-1.05, 1.05) * s, y - s * 1.15 + rng.uniform(-0.6, 0.3) * s, s * 0.07, s * 0.025, rng.uniform(0, math.tau), n=8) for _ in range(90)]
    art = GP(art, shapes(W, H, dabs) * gaussian_filter(m, 2), "#5f8d4a", seed=seed + 4, rough=0.4, density=0.8)
    dk = [petal_pts(x + rng.uniform(-1.05, 1.05) * s, y - s * 1.0 + rng.uniform(-0.4, 0.3) * s, s * 0.06, s * 0.022, rng.uniform(0, math.tau), n=8) for _ in range(60)]
    art = GP(art, shapes(W, H, dk) * gaussian_filter(m, 2), MANG_D, seed=seed + 5, rough=0.4, density=0.7)
    return art


def sunburst(W, H, cx, cy, r, n, a0=math.pi, a1=math.tau):
    rays = []
    for i in range(n):
        a = a0 + (a1 - a0) * (i + 0.5) / n
        rays.append(petal_pts(cx, cy, r, r * 0.11, a, n=10))
    return shapes(W, H, rays)


def house(W, H, cx, floor, s, seed):
    """Baloy hall: returns painted RGBA layer (no background)."""
    art = blank(W, H)
    rng = random.Random(seed)
    X = lambda u: cx + u * s
    Y = lambda v: floor + v * s
    water = Y(0.62)
    # stilts
    posts = []
    for u in np.linspace(-1.55, 1.55, 15):
        posts.append([(X(u) - s * 0.018, Y(0.02)), (X(u) + s * 0.018, Y(0.02)), (X(u) + s * 0.02, water + 6), (X(u) - s * 0.02, water + 6)])
    art = GP(art, shapes(W, H, posts, smooth=False), WOOD, WOOD_D, seed=seed, rough=1.0, streak=0.8)
    braces = [[(X(u), Y(0.08)), (X(u + 0.21), Y(0.5))] for u in (-1.55, -1.05, 0.62, 1.12)]
    art = GP(art, lines(W, H, braces, s * 0.014), WOOD_D, seed=seed + 1, rough=0.6, density=0.8)
    # jetty + stairs
    jetty = rect(X(-0.32), Y(0.36), X(0.32), Y(0.41))
    art = GP(art, shape_mask(W, H, jetty, smooth=False), WOOD, WOOD_D, seed=seed + 2, rough=0.8, streak=0.8)
    for k in range(6):
        t = k / 6
        st = rect(X(-0.17), Y(0.02 + t * 0.34), X(0.17), Y(0.02 + t * 0.34 + 0.022))
        art = GP(art, shape_mask(W, H, st, smooth=False), "#9a7048", WOOD, seed=seed + 3 + k, rough=0.5, streak=0.6)
    rails = [[(X(d * 0.19), Y(-0.05)), (X(d * 0.19), Y(0.38))] for d in (-1, 1)] + [[(X(d * 0.19), Y(-0.05)), (X(d * 0.27), Y(0.38))] for d in (-1, 1)]
    art = GP(art, lines(W, H, rails, s * 0.016), YEL_D, seed=seed + 10, rough=0.4)
    # floor beam
    beam = rect(X(-1.62), Y(-0.04), X(1.62), Y(0.03))
    art = GP(art, shape_mask(W, H, beam, smooth=False), YEL, YEL_D, seed=seed + 11, rough=0.8, streak=0.7)
    # wings (lower)
    for d in (-1, 1):
        wall = rect(X(d * 0.95), Y(-0.42), X(d * 1.58), Y(-0.04))
        if d < 0:
            wall = rect(X(-1.58), Y(-0.42), X(-0.95), Y(-0.04))
        else:
            wall = rect(X(0.95), Y(-0.42), X(1.58), Y(-0.04))
        mw = shape_mask(W, H, wall, smooth=False)
        art = GP(art, mw, GREEN_L, GREEN, seed=seed + 12 + d, rough=0.8, streak=0.8)
        # wing windows
        xs = np.linspace(min(X(d * 1.05), X(d * 1.48)), max(X(d * 1.05), X(d * 1.48)), 3)
        wins = [rect(x - s * 0.055, Y(-0.33), x + s * 0.055, Y(-0.12)) for x in xs]
        art = GP(art, shapes(W, H, [rect(x0 - 4, y0 - 4, x1 + 4, y1 + 4) for (x0, y0), _, (x1, y1), _ in wins], smooth=False), YEL, YEL_D, seed=seed + 14 + d, rough=0.5)
        art = GP(art, shapes(W, H, wins, smooth=False), "#2a2a20", "#3a3226", seed=seed + 16 + d, rough=0.5)
        # wing roof (hip, sloping out)
        x_in, x_out = X(d * 0.88), X(d * 1.7)
        roof = [(x_in, Y(-0.72)), (X(d * 1.42), Y(-0.72)), (x_out, Y(-0.4)), (x_in, Y(-0.4))]
        mr = shape_mask(W, H, roof, smooth=False)
        art = GP(art, mr, ROOF, ROOF_D, seed=seed + 18 + d, rough=1.0, streak=0.9)
        sh = lines(W, H, [[(min(x_in, x_out) - 4, Y(-0.72 + k * 0.064)), (max(x_in, x_out) + 4, Y(-0.72 + k * 0.064))] for k in range(1, 5)], 1.6) * mr
        art = GP(art, sh, ROOF_D, seed=seed + 20 + d, rough=0.4, density=0.7)
        eave = rect(min(x_in, x_out), Y(-0.43), max(x_in, x_out), Y(-0.385))
        art = GP(art, shape_mask(W, H, eave, smooth=False), YEL, YEL_D, seed=seed + 22 + d, rough=0.6)
        dots = [(x, Y(-0.408), s * 0.011) for x in np.arange(min(x_in, x_out) + 8, max(x_in, x_out) - 4, s * 0.06)]
        art = GP(art, circles(W, H, dots), RED, seed=seed + 24 + d, rough=0.3)
    # main hall wall
    wall = rect(X(-0.95), Y(-0.6), X(0.95), Y(-0.04))
    mw = shape_mask(W, H, wall, smooth=False)
    art = GP(art, mw, GREEN, GREEN_D, seed=seed + 30, rough=0.8, streak=0.9)
    art = GP(art, shape_mask(W, H, rect(X(-0.95), Y(-0.6), X(0.95), Y(-0.53)), smooth=False), GREEN_D, "#173f29", seed=seed + 29, rough=0.6, density=0.7)
    planks = lines(W, H, [[(X(u), Y(-0.6)), (X(u), Y(-0.04))] for u in np.arange(-0.92, 0.95, 0.075)], 1.2) * mw
    art = GP(art, planks, GREEN_D, seed=seed + 31, rough=0.3, density=0.45)
    # door + windows on the main hall
    wins = []
    for u in (-0.72, -0.48, 0.48, 0.72):
        wins.append(rect(X(u) - s * 0.07, Y(-0.5), X(u) + s * 0.07, Y(-0.16)))
    door = rect(X(-0.15), Y(-0.52), X(0.15), Y(-0.04))
    frames = [rect(x0 - 5, y0 - 5, x1 + 5, y1 + 5) for (x0, y0), _, (x1, y1), _ in wins + [door]]
    art = GP(art, shapes(W, H, frames, smooth=False), YEL, YEL_D, seed=seed + 32, rough=0.5, streak=0.5)
    art = GP(art, shapes(W, H, wins, smooth=False), "#262619", "#3b3324", seed=seed + 33, rough=0.4)
    art = GP(art, shape_mask(W, H, door, smooth=False), RED, RED_D, seed=seed + 34, rough=0.5, streak=0.7)
    art = GP(art, lines(W, H, [[(X(0), Y(-0.5)), (X(0), Y(-0.06))]], 2.0), RED_D, seed=seed + 35, rough=0.3)
    # window crosses (lattice)
    lat = []
    for (x0, y0), _, (x1, y1), _ in wins:
        lat += [[((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)]]
    art = GP(art, lines(W, H, lat, 2.2), YEL_D, seed=seed + 36, rough=0.3)
    # carved apron band under the gable
    band = rect(X(-1.0), Y(-0.7), X(1.0), Y(-0.6))
    art = GP(art, shape_mask(W, H, band, smooth=False), YEL, YEL_D, seed=seed + 37, rough=0.6, streak=0.6)
    sc = []
    for u in np.arange(-0.96, 0.97, 0.12):
        sc.append(arc_pts(X(u + 0.03), Y(-0.65), s * 0.03, math.pi * 0.1, math.pi * 1.6, 10))
        sc.append(arc_pts(X(u + 0.09), Y(-0.65), s * 0.03, math.pi * 1.1, math.pi * 2.6, 10))
    art = GP(art, strokes(W, H, [(p, 2.4, (0.2, 0.3)) for p in sc]), GREEN_D, seed=seed + 38, rough=0.4)
    art = GP(art, circles(W, H, [(X(u + 0.06), Y(-0.65), s * 0.012) for u in np.arange(-0.96, 0.97, 0.12)]), RED, seed=seed + 39, rough=0.3)
    # main roof: big front gable
    apex = (X(0), Y(-1.55))
    roof = [apex, (X(1.18), Y(-0.66)), (X(-1.18), Y(-0.66))]
    mr = shape_mask(W, H, roof, smooth=False)
    art = GP(art, mr, ROOF, ROOF_D, seed=seed + 40, rough=1.0, streak=1.0)
    sh = lines(W, H, [[(X(-1.3), Y(-1.5 + k * 0.07)), (X(1.3), Y(-1.5 + k * 0.07))] for k in range(14)], 1.5) * mr
    art = GP(art, sh, ROOF_D, seed=seed + 41, rough=0.4, density=0.65)
    art = shade(art, mr, ROOF_D, 0.5, -s * 0.12, seed + 42)
    # gable face (inset triangle) yellow with carved sunburst
    g = [(X(0), Y(-1.36)), (X(0.86), Y(-0.73)), (X(-0.86), Y(-0.73))]
    mg = shape_mask(W, H, g, smooth=False)
    art = GP(art, mg, YEL, YEL_L, seed=seed + 43, rough=0.6, streak=0.6)
    rays = sunburst(W, H, X(0), Y(-0.75), s * 0.5, 13) * mg
    art = GP(art, rays, GREEN, GREEN_D, seed=seed + 44, rough=0.5, streak=0.4)
    art = GP(art, sunburst(W, H, X(0), Y(-0.75), s * 0.3, 13) * mg, RED, RED_D, seed=seed + 45, rough=0.4)
    art = GP(art, circles(W, H, [(X(0), Y(-0.75), s * 0.12)]) * mg, YEL_L, YEL, seed=seed + 46, rough=0.4)
    # small diamond window in gable
    dm = [(X(0), Y(-1.2)), (X(0.07), Y(-1.1)), (X(0), Y(-1.0)), (X(-0.07), Y(-1.1))]
    art = GP(art, shape_mask(W, H, dm, smooth=False), RED, RED_D, seed=seed + 47, rough=0.3)
    # bargeboards (yellow edge) + crossed curling horns at apex
    barge = [[apex, (X(1.2), Y(-0.64))], [apex, (X(-1.2), Y(-0.64))]]
    art = GP(art, lines(W, H, barge, s * 0.035), YEL, YEL_D, seed=seed + 48, rough=0.6)
    horns = []
    for d in (-1, 1):
        p = curve([(X(-d * 0.1), Y(-1.42)), (X(d * 0.05), Y(-1.62)), (X(d * 0.2), Y(-1.78)), (X(d * 0.3), Y(-1.74)), (X(d * 0.27), Y(-1.66))], 30)
        horns.append((p, s * 0.04, (0.05, 0.35)))
    art = GP(art, strokes(W, H, horns), YEL, YEL_D, seed=seed + 49, rough=0.6)
    # eave fringe of carved tips along both rakes
    tips = []
    for t in np.linspace(0.12, 0.96, 12):
        for d in (-1, 1):
            px, py = X(d * 1.18 * t), Y(-1.55 + 0.89 * t)
            tips.append(petal_pts(px + d * 3, py + 6, s * 0.06, s * 0.02, math.pi / 2 + d * 0.3, n=8))
    art = GP(art, shapes(W, H, tips), RED, RED_D, seed=seed + 50, rough=0.4)
    # pennant pole
    art = GP(art, lines(W, H, [[(X(1.45), Y(-0.72)), (X(1.45), Y(-1.25))]], 2.4), WOOD_D, seed=seed + 51, rough=0.3)
    flag = [(X(1.45), Y(-1.25)), (X(1.66), Y(-1.2)), (X(1.45), Y(-1.13))]
    art = GP(art, shape_mask(W, H, flag), YEL, seed=seed + 52, rough=0.6)
    return art, water


def perahu(art, W, H, x, y, s, seed):
    hull = curve([(x - s, y - s * 0.18), (x - s * 0.5, y + s * 0.12), (x + s * 0.5, y + s * 0.12), (x + s * 1.05, y - s * 0.22)], 30)
    hull = hull + [(x + s * 0.9, y - s * 0.12), (x - s * 0.85, y - s * 0.1)]
    m = shape_mask(W, H, hull)
    art = GP(art, m, RED, RED_D, seed=seed, rough=0.8, streak=0.7)
    stripe = curve([(x - s * 0.95, y - s * 0.12), (x, y + s * 0.0), (x + s, y - s * 0.15)], 20)
    art = GP(art, strokes(W, H, [(stripe, s * 0.06, (0.1, 0.1))]) * m, YEL, seed=seed + 1, rough=0.3)
    return art


def baloy():
    W, H = 780, 920
    clear()
    sky = painted_sky(W, H, [(0, "#a9d3cf"), (0.22, "#d4e2c4"), (0.42, "#f6dfa4"), (0.6, "#f3c98e"), (0.62, "#cfd8c0"), (1, "#bfe0d2")], seed=5, streak=0.9)
    art = sky
    horizon = 600
    # sun low behind, with a warm halo
    art = over(art, glow(circles(W, H, [(565, 330, 60)]), "#fff3c8", radius=40, strength=0.5))
    art = G(art, circles(W, H, [(565, 330, 58)]), "#fff0b8", "#fbd877", seed=7, density=1.0, edge=0.25, bloom=0.0, rough=1.5)
    # soft cloud strokes
    cl = [(curve([(x, y), (x + L * 0.5, y - 5), (x + L, y + 2)], 20), w_, (0.3, 0.3)) for x, y, L, w_ in [(40, 150, 220, 16), (90, 175, 160, 10), (470, 120, 240, 14), (520, 142, 180, 9), (300, 230, 150, 8)]]
    art = G(art, strokes(W, H, cl), "#fbf3df", "#f6e6c8", seed=6, density=0.75, edge=0.2, bloom=0.2, rough=4, feather=3)
    # far islands
    far = [(x, horizon - 18 - 22 * math.exp(-((x - 120) / 120) ** 2) - 12 * math.exp(-((x - 700) / 90) ** 2)) for x in range(-10, W + 20, 10)]
    art = GP(art, shape_mask(W, H, far + [(W + 10, horizon + 4), (-10, horizon + 4)], smooth=False), "#8fae9c", "#9fb8a4", seed=8, rough=2.0, density=0.8)
    # sea
    sea = rect(-10, horizon, W + 10, H + 10)
    msea = shape_mask(W, H, sea, smooth=False)
    art = GP(art, msea, SEA_L, SEA, seed=9, rough=0.5, streak=1.0)
    yy = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    deep = np.clip((yy * H - horizon) / (H - horizon), 0, 1) * msea
    art = GP(art, deep * 0.9, SEA, SEA_D, seed=10, rough=0.4, streak=1.0, density=0.85)
    # sun glitter
    rng = random.Random(4)
    gl = [[(560 + rng.gauss(0, 30 + (y - horizon) * 0.25) - 14, y), (560 + rng.gauss(0, 30 + (y - horizon) * 0.25) + rng.uniform(6, 26), y)] for y in np.arange(horizon + 6, H - 40, 9)]
    art = GP(art, lines(W, H, gl, 2.2), "#fbe8b0", seed=11, rough=0.3, density=0.7)
    clear()
    # house layer
    hs, water = house(W, H, 390, 520, 200, 21)
    # reflection
    wl = int(water)
    ref = np.zeros_like(hs)
    hgt = H - wl
    src = hs[max(0, wl - hgt):wl][::-1]
    ref[wl:wl + src.shape[0]] = src
    ref = ref.copy()
    ref[..., :3] = ref[..., :3] * 0.55 + np.array(hex_rgb(SEA_D)) * 0.45
    fade = np.clip(1 - (np.arange(H) - wl) / 260.0, 0, 1)[:, None]
    ref[..., 3] = gaussian_filter(ref[..., 3], (5, 9)) * 0.6 * fade
    ny = fbm(W, H, 33, 8, 2) - 0.5
    yi, xi = np.mgrid[0:H, 0:W].astype(np.float32)
    for c in range(4):
        ref[..., c] = map_coordinates(ref[..., c], [yi, xi + ny * 30], order=1, mode="constant")
    art = over(art, ref)
    ripples = [[(x0, y), (x0 + rng.uniform(30, 90), y)] for y in np.arange(wl + 8, H - 20, 11) for x0 in [rng.uniform(80, 640)]]
    art = GP(art, lines(W, H, ripples, 2.0), "#d9efe6", seed=34, rough=0.4, density=0.6)
    art = over(art, hs)
    clear()
    # mangroves left and right (in front)
    art = mangrove(art, W, H, 40, 650, 150, 41, 1)
    art = mangrove(art, W, H, 745, 670, 135, 51, -1)
    clear()
    art = mangrove(art, W, H, 160, 700, 80, 61, 1)
    art = perahu(art, W, H, 560, 720, 70, 71)
    art = GP(art, lines(W, H, [[(560 - 40, 712), (452, 640)]], 1.6), "#4a3a2a", seed=72, rough=0.3, density=0.8)
    # birds
    birds = []
    for bx, by, bs in [(180, 250, 13), (215, 230, 10), (250, 262, 9)]:
        birds += [(arc_pts(bx - bs * 0.5, by, bs * 0.55, math.pi * 1.15, math.pi * 1.9, 8), 2.0, (0.3, 0.3)), (arc_pts(bx + bs * 0.5, by, bs * 0.55, math.pi * 1.1, math.pi * 1.85, 8), 2.0, (0.3, 0.3))]
    art = GP(art, strokes(W, H, birds), "#4a3a32", seed=80, rough=0.3)
    art = add_grain(art, 3, 0.035)
    preview(art, "baloy")
    save_rgb(art, f"{OUT}/baloy.webp", (780, 920), quality=76)


def band():
    """Seamless carved trim: green ground, yellow interlocking scrolls, red buds (repeat-x)."""
    W, H = 240, 56
    clear()
    art = solid(W * 3, H, GREEN)
    art = GP(art, shape_mask(W * 3, H, rect(-4, 0, W * 3 + 4, H), smooth=False), GREEN, GREEN_D, seed=3, rough=0.3, streak=1.0)
    edges = lines(W * 3, H, [[(-4, 5), (W * 3 + 4, 5)], [(-4, H - 5), (W * 3 + 4, H - 5)]], 4)
    art = GP(art, edges, YEL, YEL_D, seed=4, rough=0.3)
    sc, buds, lv = [], [], []
    for k in range(9):
        cx = k * 80 + 40
        sc.append((spiral_pts(cx - 18, H / 2, 3, 14, math.pi, 1.1), 3.4, (0.05, 0.4)))
        sc.append((spiral_pts(cx + 18, H / 2, 3, 14, 0, 1.1), 3.4, (0.05, 0.4)))
        sc.append((curve([(cx - 40, H / 2 + 10), (cx - 20, H / 2 + 14), (cx, H / 2 + 6), (cx + 20, H / 2 + 14), (cx + 40, H / 2 + 10)], 20), 2.6, (0.0, 0.0)))
        buds.append((cx, H / 2 - 2, 5))
        lv += [petal_pts(cx, H / 2 - 2, 12, 4, -math.pi / 2 + d, n=8) for d in (-0.6, 0.6)]
    art = GP(art, strokes(W * 3, H, sc), YEL, YEL_D, seed=5, rough=0.4)
    art = GP(art, shapes(W * 3, H, lv), YEL_L, YEL, seed=6, rough=0.3)
    art = GP(art, circles(W * 3, H, buds), RED, RED_D, seed=7, rough=0.3)
    art = add_grain(art, 2, 0.04)
    tile = art[:, W:W * 2]
    preview(tile, "band")
    save_rgb(tile, f"{OUT}/band.webp", quality=80)


def spiral_pts(cx, cy, r0, r1, a0, turns, n=30):
    return [(cx + math.cos(a0 + t * turns * math.tau) * (r1 - (r1 - r0) * t), cy + math.sin(a0 + t * turns * math.tau) * (r1 - (r1 - r0) * t)) for t in np.linspace(0, 1, n)]


def carved_flower(art, W, H, cx, cy, s, seed):
    """Four-petal carved flower (bunga) with curling leaves — painted wood carving."""
    pet = [petal_pts(cx, cy, s, s * 0.42, a, n=14) for a in (0, math.pi / 2, math.pi, -math.pi / 2)]
    m = shapes(W, H, pet)
    art = GP(art, m, YEL, YEL_D, seed=seed, rough=0.6, streak=0.5)
    inner = shapes(W, H, [petal_pts(cx, cy, s * 0.6, s * 0.22, a, n=12) for a in (0, math.pi / 2, math.pi, -math.pi / 2)])
    art = GP(art, inner, RED, RED_D, seed=seed + 1, rough=0.4)
    art = GP(art, shapes(W, H, [petal_pts(cx, cy, s * 0.62, s * 0.2, a, n=12) for a in (math.pi / 4, 3 * math.pi / 4, -math.pi / 4, -3 * math.pi / 4)]), GREEN, GREEN_D, seed=seed + 2, rough=0.4)
    art = GP(art, circles(W, H, [(cx, cy, s * 0.16)]), YEL_L, YEL, seed=seed + 3, rough=0.3)
    return art


def divider():
    W, H = 520, 80
    clear()
    art = blank(W, H)
    cx, cy = W / 2, H / 2
    sc = []
    for d in (-1, 1):
        sc.append((curve([(cx + d * 34, cy), (cx + d * 90, cy - 14), (cx + d * 150, cy + 6), (cx + d * 210, cy - 6), (cx + d * 250, cy)], 40), 3.2, (0.05, 0.5)))
        for k, u in enumerate((80, 140, 200)):
            sc.append((spiral_pts(cx + d * u, cy + (10 if k % 2 == 0 else -10), 2, 10, (0 if d > 0 else math.pi) + (math.pi / 2 if k % 2 else -math.pi / 2), 1.0), 2.6, (0.05, 0.5)))
    art = GP(art, strokes(W, H, sc), GREEN, GREEN_D, seed=3, rough=0.4)
    lv = []
    for d in (-1, 1):
        for u in (60, 115, 175, 228):
            lv.append(petal_pts(cx + d * u, cy - 4, 13, 4.5, -math.pi / 2 - d * 0.7, n=8))
    art = GP(art, shapes(W, H, lv), YEL, YEL_D, seed=4, rough=0.3)
    art = GP(art, circles(W, H, [(cx + d * u, cy + 6, 3.6) for d in (-1, 1) for u in (105, 165)]), RED, seed=5, rough=0.2)
    art = carved_flower(art, W, H, cx, cy, 30, 6)
    preview(art, "divider")
    save(art, f"{OUT}/divider.webp", max_w=520)


def kembang():
    W, H = 160, 160
    clear()
    art = blank(W, H)
    art = carved_flower(art, W, H, 80, 80, 66, 11)
    preview(art, "kembang")
    save(art, f"{OUT}/kembang.webp", max_w=120)


def bakau():
    W, H = 420, 360
    clear()
    art = blank(W, H)
    art = mangrove(art, W, H, 200, 330, 175, 91, 1)
    preview(art, "bakau", tone="#e7f1ea")
    save(art, f"{OUT}/bakau.webp", max_w=360)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
