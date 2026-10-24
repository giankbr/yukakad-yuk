"""Danau Angsa — a calm lake at a blush morning in romantic watercolour: two white swans whose necks bow into a heart,
weeping willow strands, reeds with cattails, a misty far shore and soft reflections. White swans are opaque body colour
(gouache-white) shaded with lilac-grey glazes. Palette: blush, mist blue, sage, lilac grey, a touch of orange beak.
Run: python3 -I danau-angsa.py [part ...]   parts: danau tirai angsa bulu ilalang"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s1_lib import *
from scipy.ndimage import map_coordinates

OUT = outdir("danau-angsa")
PARTS = sys.argv[1:] or ["danau", "tirai", "angsa", "bulu", "ilalang"]
PAPER = "#fbf5f1"
BLUSH, PEACH = "#f1cfc6", "#f6dfcf"
LAKE, LAKE_D = "#b4c7d1", "#8ea8b6"
SAGE, SAGE_D, SAGE_L = "#93ac8f", "#5f7b66", "#bfd0b3"
SHADE = "#b8b6c9"
WHITE = "#fdfcf8"


def reflect(layer, axis_y, squash=0.9, strength=0.5, seed=1):
    h, w = layer.shape[:2]
    out = blank(w, h)
    yy, xx = yx(w, h)
    d = yy - axis_y
    src_y = axis_y - d / squash
    rip = (fbm(w, h, seed, 12, 2) - 0.5) * 7 * np.clip(d / 40, 0, 1) + np.sin(yy * 0.7) * 1.0
    for c in range(4):
        out[..., c] = map_coordinates(layer[..., c], [src_y, xx + rip], order=1, mode="constant")
    fade = np.clip(1 - d / (h - axis_y + 1), 0, 1) ** 0.8 * (d > 0)
    out[..., 3] *= fade * strength
    return out


def swan(art, W, H, cx, cy, s, face, nx, rng, shade_amt=1.0):
    """White swan floating; face=+1 looks right. cy = waterline. Neck bows forward and down (heart pose)."""
    f = face
    P = lambda x, y: (cx + f * x * s, cy + y * s)
    body = shape_mask(W, H, [P(-74, -4), P(-66, -20), P(-40, -30), P(0, -30), P(30, -24), P(44, -10), P(36, 4), P(-20, 7), P(-66, 3)])
    tail = shape_mask(W, H, [P(-66, -8), P(-92, -22), P(-80, -4)])
    wing = shape_mask(W, H, [P(24, -28), P(10, -46), P(-20, -58), P(-50, -64), P(-84, -74), P(-72, -60), P(-96, -58), P(-80, -46),
                             P(-98, -40), P(-76, -30), P(-44, -24), P(10, -24)])
    neck_pts = curve([P(30, -24), P(36, -60), P(22, -104), P(34, -134), P(58, -138), P(72, -118)], 30)
    neck = strokes(W, H, [(neck_pts, 15 * s, (0.0, 0.1))])
    head = ell(W, H, *P(68, -118), 13 * s, 9.5 * s, 40 * f)
    white = np.clip(body + tail + wing + neck + head, 0, 1)
    art = GP(art, white, WHITE, "#f6f2ea", seed=nx(), rough=2.0, streak=0.3, density=0.98)
    art = G(art, white, "#a7a6be", seed=nx(), density=0.06, edge=1.0, bloom=0, gran=0.1, rough=1.2, feather=0.6)
    # shading: belly and under-wing, back of the neck, a few wing feather scallops
    yy = yx(W, H)[0]
    belly = (body + tail) * np.clip((yy - (cy - 20 * s)) / (26 * s), 0, 1)
    art = G(art, np.clip(belly, 0, 1) * shade_amt, SHADE, "#a9b3c9", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=2, feather=1.5)
    under = np.clip(wing - shape_mask(W, H, [P(28, -34), P(10, -52), P(-20, -64), P(-50, -70), P(-84, -80), P(-60, -40), P(-20, -36)]), 0, 1)
    art = G(art, under * shade_amt, SHADE, seed=nx(), density=0.45, edge=0.4, bloom=0.2, rough=1.5, feather=1)
    scal = []
    for k, (x0, y0) in enumerate([(-30, -44), (-46, -46), (-62, -48), (-40, -34), (-58, -36)]):
        scal.append(([P(x0 + 10, y0 - 4), P(x0, y0), P(x0 - 14, y0 - 6)], 1.3 * s, (0.2, 0.3)))
    art = G(art, strokes(W, H, scal) * shade_amt, "#a9a9bf", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6, feather=0.5)
    nshade = strokes(W, H, [([(p[0] - f * 4 * s, p[1]) for p in neck_pts[3:24]], 5 * s, (0.2, 0.3))]) * neck
    art = G(art, nshade * shade_amt, SHADE, seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=1, feather=1.2)
    # beak (orange with black knob) + eye
    hx, hy = P(70, -116)
    beak = shape_mask(W, H, [P(74, -124), P(94, -104), P(88, -100), P(70, -112)], smooth=True)
    knob = np.clip(ell(W, H, *P(74, -119), 3.6 * s, 3.2 * s, 0) + circles(W, H, [(*P(63, -121), 1.9 * s)]), 0, 1)
    art = G(art, beak, "#ee8a4a", "#dd6d34", seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=0.6, feather=0.5)
    art = G(art, knob, "#2c2a30", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.4, feather=0.4)
    return art


def strand(rng, x, y0, L, sway):
    pts = []
    for k in range(14):
        t = k / 13
        pts.append((x + sway * (t ** 1.6) + math.sin(t * 3 + x) * 3, y0 + L * t))
    return pts


def willow(art, W, H, tops, rng, nx, col=(SAGE, SAGE_D), fade=1.0, leaf=28.0):
    """Weeping-willow strands hanging from given (x, y, length) tops: thin twigs + many narrow lanceolate leaves."""
    twigs, leaves = [], []
    for x, y0, L in tops:
        pts = strand(rng, x, y0, L, rng.uniform(-14, 14))
        twigs.append((curve(pts, 40), 1.3, (0.0, 0.5)))
        cp = curve(pts, 64)
        nn = len(cp)
        for k in range(2, nn, 2):
            px, py = cp[k]
            for side in (-1, 1):
                if rng.random() < 0.25:
                    continue
                a = math.pi / 2 + side * rng.uniform(0.25, 0.85)
                l = leaf * rng.uniform(0.75, 1.2) * (1 - 0.3 * k / nn)
                leaves.append(petal_pts(px, py, l, l * 0.17, a, n=10))
    tm = strokes(W, H, twigs)
    art = G(art, tm * fade, "#8a7a66", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=0.5, feather=0.4)
    rng.shuffle(leaves)
    half = len(leaves) // 2
    soft = np.clip(gaussian_filter(shapes(W, H, leaves), 5) * 3, 0, 1)
    art = G(art, soft * fade, SAGE_L, "#d6e0c6", seed=nx(), density=0.28, edge=0.2, bloom=0.6, rough=4, feather=2)
    art = G(art, shapes(W, H, leaves[:half]) * fade, col[0], SAGE_L, seed=nx(), density=0.72, edge=0.6, bloom=0.3, rough=0.8, feather=0.5)
    art = G(art, shapes(W, H, leaves[half:]) * fade, col[1], col[0], seed=nx(), density=0.62, edge=0.6, bloom=0.3, rough=0.8, feather=0.5)
    return art


def reeds(art, W, H, x0, base, n, hmax, rng, nx, cattails=3, fade=1.0, spread=60):
    blades, tails = [], []
    for k in range(n):
        x = x0 + rng.uniform(-spread / 2, spread / 2)
        h = hmax * rng.uniform(0.5, 1.0)
        lean = rng.uniform(-0.35, 0.35)
        pts = curve([(x, base), (x + lean * h * 0.3, base - h * 0.55), (x + lean * h, base - h)], 16)
        blades.append((pts, rng.uniform(3, 5.5), (0.0, 0.85)))
    for k in range(cattails):
        x = x0 + rng.uniform(-spread / 3, spread / 3); h = hmax * rng.uniform(0.75, 1.05); lean = rng.uniform(-.12, .12)
        top = (x + lean * h, base - h)
        blades.append(([(x, base), (x + lean * h * .5, base - h * .5), top], 2, (0.0, 0.2)))
        tails.append((top[0] - lean * 18, top[1] + 24, 5.5, 18, math.degrees(math.atan2(lean, 1))))
    art = G(art, strokes(W, H, blades) * fade, SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=1.2, feather=0.6)
    if tails:
        art = G(art, ellipses(W, H, tails) * fade, "#8a5d3e", "#6e4630", seed=nx(), density=0.92, edge=0.5, bloom=0.1, rough=0.8, feather=0.5)
    return art


if "danau" in PARTS:
    W, H = 820, 620
    SHORE = 250
    rng = random.Random(181); nx = Seq(181000)
    yy, xx = yx(W, H)
    art = blank(W, H)
    sky = np.clip(yy / 220, 0, 1) * (yy < SHORE + 4)
    art = G(art, sky * np.clip((yy - 10) / 200, 0, 1), PEACH, BLUSH, seed=nx(), density=0.7, edge=0.05, bloom=0.5, rough=12, feather=10)
    sun = circles(W, H, [(560, SHORE - 70, 34)])
    art = over(art, glow(sun, "#fff4e4", radius=34, strength=0.5))
    art = G(art, sun, "#f8d9bd", "#f4c9b2", seed=nx(), density=0.55, edge=0.3, bloom=0.3, rough=2, feather=1.5)
    # far shore: soft rounded trees, blue-sage in mist
    crowns = [(x, SHORE - rng.uniform(16, 50), rng.uniform(26, 50)) for x in np.linspace(-20, W + 20, 30)]
    fm = circles(W, H, crowns) * (yy < SHORE)
    art = G(art, fm, "#a9b8b6", "#9dafb0", seed=nx(), density=0.5, edge=0.35, bloom=0.55, rough=4, feather=2.4)
    near = [(x, SHORE - rng.uniform(4, 24), rng.uniform(18, 34)) for x in np.linspace(80, W - 60, 18)]
    art = G(art, circles(W, H, near) * (yy < SHORE), "#8fa39b", "#82978f", seed=nx(), density=0.5, edge=0.4, bloom=0.4, rough=3, feather=1.6)
    for (y, hh, amt) in [(SHORE - 6, 22, 0.75), (SHORE - 34, 18, 0.4)]:
        b = np.clip(1 - np.abs(yy - y) / hh, 0, 1) ** 1.4 * (0.5 + 0.5 * fbm(W, H, int(y) + 5, 80, 3))
        art[..., 3] *= 1 - b * amt
    land = art.copy()
    water = (yy > SHORE).astype(np.float32)
    lake = G(blank(W, H), water, "#d9e2e4", LAKE, seed=nx(), density=0.5, edge=0.05, bloom=0.3, rough=8, feather=4)
    lake = G(lake, water * np.clip((yy - SHORE - 120) / 260, 0, 1), LAKE, LAKE_D, seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=8, feather=6)
    lake = G(lake, water * np.clip(1 - (yy - SHORE) / 160, 0, 1), BLUSH, seed=nx(), density=0.45, edge=0, bloom=0.4, rough=8, feather=6)
    lake = glaze(lake, reflect(land, SHORE, 0.9, 0.45, nx()))
    streaks = []
    for _ in range(50):
        y = rng.uniform(SHORE + 10, H - 40); x0 = rng.uniform(-40, W); L = rng.uniform(40, 220)
        streaks.append(([(x0, y), (x0 + L, y + rng.uniform(-1, 1))], rng.uniform(1.0, 2.2), (0.3, 0.3)))
    lake[..., 3] *= 1 - strokes(W, H, streaks) * water * 0.5
    art = over(lake, land)
    # swans: reflections first, then the birds (heart pose)
    SW = SHORE + 190
    birds = swan(blank(W, H), W, H, 304, SW, 1.25, 1, nx, rng)
    birds = swan(birds, W, H, 538, SW, 1.25, -1, nx, rng)
    rb = reflect(birds, SW + 4, 1.2, 0.5, nx())
    rb[..., :3] = rb[..., :3] * 0.75 + np.array(hex_rgb("#c9d3dc"), np.float32) * 0.25
    art = over(art, rb)
    art = over(art, birds)
    rip = strokes(W, H, [(arc_pts(410, SW + 8, rr, math.pi * 0.08, math.pi * 0.92, 30, 0.1), 1.6, (0.2, 0.2)) for rr in (150, 190, 236)])
    art = G(art, rip, LAKE_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=1, feather=0.6)
    # reeds at both lower corners
    art = reeds(art, W, H, 60, H - 40, 26, 230, rng, nx, cattails=4, spread=120)
    art = reeds(art, W, H, W - 50, H - 30, 20, 190, rng, nx, cattails=3, spread=100)
    # willow strands entering from the top-left (tree off-canvas)
    tops = [(x, rng.uniform(-10, 30), rng.uniform(180, 330)) for x in np.linspace(-10, 190, 16)]
    art = willow(art, W, H, tops, rng, nx)
    art[..., 3] *= np.clip((H - 4 - yy) / 70, 0, 1)
    preview(art, "da-danau", tone=PAPER)
    save_full(art, f"{OUT}/danau.webp", size=(720, 544), quality=74)
    clear()

if "tirai" in PARTS:
    W, H = 520, 520
    rng = random.Random(182); nx = Seq(182000)
    art = blank(W, H)
    branch = strokes(W, H, [(curve([(-20, 24), (120, 14), (260, 34), (420, 30), (540, 50)], 40), 9, (0.0, 0.7))])
    tops = [(x, 20 + 10 * math.sin(x / 90) + rng.uniform(0, 14), rng.uniform(200, 470) * (1 - x / 900)) for x in np.linspace(0, 500, 34)]
    art = willow(art, W, H, tops, rng, nx, leaf=8)
    art = G(art, branch, "#7a6a58", "#5e5144", seed=nx(), density=0.8, edge=0.4, bloom=0.1, rough=1, feather=0.6)
    preview(art, "da-tirai", tone=PAPER)
    save(art, f"{OUT}/tirai.webp", max_w=360, quality=78)
    clear()

if "angsa" in PARTS:
    W, H = 460, 260
    rng = random.Random(183); nx = Seq(183000)
    art = blank(W, H)
    wl = ell(W, H, 220, 222, 200, 14)
    art = G(art, wl, LAKE, LAKE_D, seed=nx(), density=0.5, edge=0.3, bloom=0.4, rough=4, feather=2)
    art = swan(art, W, H, 136, 216, 1.0, 1, nx, rng)
    art = swan(art, W, H, 322, 216, 1.0, -1, nx, rng)
    preview(art, "da-angsa", tone=PAPER)
    save(art, f"{OUT}/angsa.webp", max_w=300, quality=82)
    clear()

if "bulu" in PARTS:
    W, H = 420, 120
    rng = random.Random(184); nx = Seq(184000)
    art = blank(W, H)
    rach = curve([(30, 70), (160, 56), (300, 50), (390, 58)], 50)
    up, dn = [], []
    NR = len(rach)
    for k in range(3, NR):
        x, y = rach[k]
        t = k / (NR - 1)
        L = 30 * math.sin(math.pi * min(1, (t - 0.04) * 1.08)) ** 0.7 + 2
        up.append((x + 10, y - L))
        dn.append((x + 7, y + L * 0.62))
    vane = shapes(W, H, [up + dn[::-1]])
    gaps = strokes(W, H, [([(rach[k][0], rach[k][1]), (rach[k][0] + 16, rach[k][1] - 40)], 1.6, None) for k in (int(NR * .28), int(NR * .44), int(NR * .66))] +
                   [([(rach[k][0], rach[k][1]), (rach[k][0] + 12, rach[k][1] + 26)], 1.4, None) for k in (int(NR * .36), int(NR * .58))])
    vm = np.clip(vane - gaps, 0, 1)
    art = G(art, vm, "#cdbfd6", BLUSH, seed=nx(), density=0.6, edge=0.8, bloom=0.5, rough=1.5, feather=0.8)
    barbs = strokes(W, H, [([(rach[k][0], rach[k][1]), (rach[k][0] + 12, rach[k][1] - 26)], 0.9, (0.1, 0.6)) for k in range(6, NR - 4, 2)]) * vm
    art = G(art, barbs, "#a99ab8", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = G(art, strokes(W, H, [(rach, 2.4, (0.0, 0.6))]), "#9d93a8", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    preview(art, "da-bulu", tone=PAPER)
    save(art, f"{OUT}/bulu.webp", max_w=220, quality=84)
    clear()

if "ilalang" in PARTS:
    W, H = 200, 360
    rng = random.Random(185); nx = Seq(185000)
    art = blank(W, H)
    art = reeds(art, W, H, 100, 350, 14, 330, rng, nx, cattails=3, spread=70)
    preview(art, "da-ilalang", tone=PAPER)
    save(art, f"{OUT}/ilalang.webp", max_w=120, quality=82)
    clear()
