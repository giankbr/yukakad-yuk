"""Ultah Kemah — a kids' backyard camping party, picture-book gouache: starry evening sky, string lights, a big orange
A-frame tent glowing inside, a campfire (flames separate for flicker) with marshmallows on sticks, pines, a friendly
owl on a branch, a flashlight, a hanging wooden camp sign, a toasted-marshmallow divider.
Run: python3 -I ultah-kemah.py [part ...]  parts: sky lights scene flame owl sign marsh pines (flashlight: optional extra)
Assets -> public/themes/art/ultah-kemah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n3_lib import *

OUT = outdir("ultah-kemah")
PARTS = sys.argv[1:] or ["sky", "lights", "scene", "flame", "owl", "sign", "marsh", "pines"]
NIGHT, NIGHT2, DUSK = "#1d2a44", "#2b4160", "#4f6c82"
ORANGE, ORANGE_D, ORANGE_L = "#e8743b", "#b9532a", "#f4a05f"
YEL, YEL_L = "#ffc845", "#ffe7a1"
GRASS, GRASS_D, GRASS_L = "#3e6b3a", "#2a4a2a", "#5d8c4a"
PINE, PINE_D = "#1f3f3a", "#15302c"
WOOD, WOOD_D, WOOD_L = "#c58a52", "#8a5a33", "#e2b07a"
BARK = "#6b4630"
CREAM = "#fff4dc"
INK = "#2a2230"


def P(art, m, c1, c2=None, nx=None, rough=1.6, streak=0.8):
    return GP(art, m, c1, c2 or c1, seed=nx(), rough=rough, streak=streak)


def sky():
    W, H = 480, 860
    nx = Seq(100); rng = random.Random(3)
    art = painted_sky(W, H, [(0, NIGHT), (0.55, NIGHT2), (0.85, DUSK), (1.0, "#8a7f86")], seed=4, streak=0.8)
    # stars: small dots + a few four-point twinkles
    st = stars_field(W, H, 120, 7, 0.6, 1.6, ymax=H * 0.7)
    art = tint(art, st, "#fff6dc", 0.9, blur=0.3)
    tw = []
    for _ in range(9):
        x, y, r = rng.uniform(20, W - 20), rng.uniform(20, H * 0.55), rng.uniform(5, 8)
        tw += [[(x, y - r), (x + r * 0.22, y), (x, y + r), (x - r * 0.22, y)], [(x - r, y), (x, y - r * 0.22), (x + r, y), (x, y + r * 0.22)]]
    art = tint(art, shapes(W, H, tw, smooth=False), "#fff1c4", 0.95, blur=0.4)
    # moon (crescent) with glow
    moon = circles(W, H, [(380, 120, 34)])
    bite = circles(W, H, [(396, 108, 30)])
    cres = np.clip(moon - bite, 0, 1)
    art = OV(art, moon, lambda m: glow(m, "#fff1c4", 30, 0.35), pad=120)
    art = P(art, cres, "#fff3cf", "#f6dd98", nx=nx, rough=1.0)
    art = add_grain(art, 9, 0.03)
    save_rgb(art, f"{OUT}/sky.webp", quality=70)


def lights():
    W, H = 840, 190
    nx = Seq(200); rng = random.Random(5)
    art = blank(W, H)
    wire = curve([(-10, 20), (210, 96), (420, 40), (630, 100), (850, 24)], 120)
    art = P(art, strokes(W, H, [(wire, 3.0, None)]), "#2a2a2a", nx=nx, rough=0.6)
    cols = ["#ffd35a", "#ff8f5a", "#7fd3c4", "#ff9fb5", "#ffd35a", "#b9e36a"]
    bulbs = []
    for k, (x, y, a) in enumerate(along(wire, 58)):
        bulbs.append((x, y, cols[k % len(cols)]))
    gl = circles(W, H, [(x, y + 22, 16) for x, y, c in bulbs])
    art = OV(art, gl, lambda m: glow(m, "#ffd77a", 14, 0.55), pad=60)
    for x, y, c in bulbs:
        cap = rr_mask(W, H, x - 6, y, x + 6, y + 11, 2)
        art = P(art, cap, "#3a3a3a", nx=nx, rough=0.3)
        b = shapes(W, H, [ellipse_pts(x, y + 24, 10.5, 14, 14)])
        art = P(art, b, c, mix(c, "#ffffff", 0.35), nx=nx, rough=0.6)
        art = tint(art, circles(W, H, [(x - 3.5, y + 19, 3.4)]), "#ffffff", 0.75, blur=0.8)
    save(art, f"{OUT}/lights.webp", max_w=780, quality=82)
    preview(art, "uk-lights", bg=NIGHT)


def tent_on(art, W, H, cx, by, w, h, nx, rng):
    """A-frame canvas tent, flaps tied open, warm light inside, poles, guy ropes, pennant."""
    apex = (cx, by - h)
    L, R = (cx - w / 2, by), (cx + w / 2, by)
    body = shapes(W, H, [[apex, (cx + w * 0.54, by + 4), (cx - w * 0.54, by + 4)]], smooth=False)
    art = P(art, body, ORANGE, ORANGE_L, nx=nx)
    # right face shaded
    rf = shapes(W, H, [[apex, (cx + w * 0.54, by + 4), (cx + w * 0.05, by + 4)]], smooth=False)
    art = G(art, rf, ORANGE_D, seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=2)
    # ochre stripe along the bottom hem
    hem = body * (below(H, by - 26, 2))
    art = P(art, hem, YEL, "#f2b632", nx=nx, rough=0.8)
    # doorway glow
    door = shapes(W, H, [[(cx, by - h * 0.78), (cx + w * 0.2, by + 2), (cx - w * 0.2, by + 2)]], smooth=False)
    art = OV(art, door, lambda m: glow(m, "#ffd27a", 18, 0.5), pad=60)
    art = P(art, door, "#ffcf6e", "#ffb54a", nx=nx, rough=0.6)
    art = G(art, door * below(H, by - h * 0.25, 60), "#f08c3a", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=2)
    # flaps tied back
    for sgn in (-1, 1):
        flap = shapes(W, H, [[(cx, by - h * 0.78), (cx + sgn * w * 0.06, by - h * 0.42), (cx + sgn * w * 0.3, by + 2), (cx + sgn * w * 0.2, by + 2)]])
        art = P(art, flap, ORANGE_L if sgn < 0 else ORANGE, nx=nx, rough=0.8)
        art = tint(art, edge_ring(flap, 1.4), ORANGE_D, 0.7)
        art = P(art, circles(W, H, [(cx + sgn * w * 0.12, by - h * 0.34, 5)]), "#7a4a2a", nx=nx, rough=0.3)
    # seams + outline
    art = tint(art, strokes(W, H, [([apex, (cx, by - h * 0.78)], 3, None)]), ORANGE_D, 0.8)
    art = tint(art, edge_ring(body, 1.8), "#8f3f20", 0.8)
    # pole tip + pennant
    art = P(art, strokes(W, H, [([(cx, by - h + 4), (cx, by - h - 34)], 4, None)]), BARK, nx=nx, rough=0.4)
    pen = shapes(W, H, [[(cx + 2, by - h - 34), (cx + 40, by - h - 26), (cx + 2, by - h - 16)]], smooth=False)
    art = P(art, pen, "#7fd3c4", "#5fb8a8", nx=nx, rough=0.6)
    # guy ropes + pegs
    ropes = [([(cx - w * 0.2, by - h * 0.5), (cx - w * 0.8, by + 2)], 1.6, None), ([(cx + w * 0.2, by - h * 0.5), (cx + w * 0.8, by + 2)], 1.6, None)]
    art = tint(art, strokes(W, H, ropes), "#e8dcc0", 0.9)
    return art


def campfire_on(art, W, H, cx, by, s, nx, rng):
    art = OV(art, circles(W, H, [(cx, by - s * 0.1, s * 0.42)]), lambda m: glow(m, "#ffb04a", 26, 0.28), pad=90)
    # ring of stones
    stones = [ellipse_pts(cx + (k - 3.5) * s * 0.28, by - abs(k - 3.5) * s * 0.02, s * 0.17, s * 0.11, 10) for k in range(8)]
    sm = shapes(W, H, [deform(p, rng, 1, 0.08) for p in stones])
    art = P(art, sm, "#8f8c88", "#6f6c6a", nx=nx, rough=0.8)
    art = tint(art, sm * below(H, by - s * 0.02, 6), "#4b4948", 0.5)
    # crossed logs
    logs = [([(cx - s * 0.6, by - s * 0.02), (cx + s * 0.45, by - s * 0.32)], s * 0.16, (0.0, 0.0)), ([(cx + s * 0.6, by - s * 0.02), (cx - s * 0.45, by - s * 0.32)], s * 0.16, (0.0, 0.0))]
    lm = strokes(W, H, logs)
    art = P(art, lm, BARK, "#7d5438", nx=nx, rough=0.8)
    ends = circles(W, H, [(cx - s * 0.6, by - s * 0.02, s * 0.08), (cx + s * 0.6, by - s * 0.02, s * 0.08)])
    art = P(art, ends, WOOD_L, nx=nx, rough=0.4)
    art = tint(art, strokes(W, H, [(arc_pts(cx - s * 0.6, by - s * 0.02, s * 0.04, 0, math.tau, 12), 1.2, None), (arc_pts(cx + s * 0.6, by - s * 0.02, s * 0.04, 0, math.tau, 12), 1.2, None)]), WOOD_D, 0.8)
    # embers between the logs
    emb = circles(W, H, [(cx + rng.uniform(-s * 0.25, s * 0.25), by - s * rng.uniform(0.08, 0.2), rng.uniform(3, 6)) for _ in range(9)])
    art = P(art, emb, "#ff8a3a", "#ffc845", nx=nx, rough=0.4)
    return art


def marsh_stick(art, W, H, x0, y0, x1, y1, nx, toast=True, k_=1.0):
    art = P(art, strokes(W, H, [([(x0, y0), (x1, y1)], 4.2 * k_, (0.0, 0.1))]), "#8a5a33", nx=nx, rough=0.5)
    a = math.atan2(y1 - y0, x1 - x0)
    for k, d in enumerate((0, 26 * k_)):
        mx, my = x1 - math.cos(a) * (d + 10 * k_), y1 - math.sin(a) * (d + 10 * k_)
        poly = [(mx + math.cos(a + t) * 13 * k_ * (1.0 if abs(math.cos(t)) < 0.7 else 0.85), my + math.sin(a + t) * 11 * k_) for t in np.linspace(0, math.tau, 16, endpoint=False)]
        mm = shapes(W, H, [poly])
        art = P(art, mm, "#fffaf0", "#f4ead8", nx=nx, rough=0.6)
        if toast and k == 0:
            art = G(art, mm * right_of(W, mx - 2, 10), "#c98a4a", seed=nx(), density=0.7, edge=0.3, bloom=0.2, rough=1.5)
        art = tint(art, edge_ring(mm, 1.2), "#c9b9a0", 0.6)
    return art


def scene():
    W, H = 820, 480
    nx = Seq(300); rng = random.Random(11)
    art = blank(W, H)
    # back pines silhouettes
    pines = []
    for k, x in enumerate((30, 110, 690, 780, 600)):
        h = rng.uniform(170, 240)
        for t in range(4):
            yy = 330 - h + t * h * 0.22
            ww = 26 + t * 18
            pines.append([(x, yy - 16), (x + ww, yy + h * 0.28), (x - ww, yy + h * 0.28)])
    pm = shapes(W, H, pines, smooth=False)
    art = P(art, pm, PINE, PINE_D, nx=nx, rough=1.4)
    # ground (grass hill)
    ground = shapes(W, H, [[(-20, 330), (200, 312), (420, 322), (640, 306), (840, 326), (840, 500), (-20, 500)]])
    art = P(art, ground, GRASS, GRASS_D, nx=nx)
    art = G(art, ground * below(H, 380, 80), GRASS_D, seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=3)
    blades = [([(x, y), (x + rng.uniform(-5, 5), y - rng.uniform(8, 16))], 2.2, (0.0, 0.7)) for x, y in [(rng.uniform(0, W), rng.uniform(320, 470)) for _ in range(160)]]
    art = tint(art, strokes(W, H, blades) * ground, GRASS_L, 0.7)
    # tent
    art = tent_on(art, W, H, 250, 360, 330, 250, nx, rng)
    clear()
    # campfire (flames come as a separate asset placed at ~ (600, 300))
    art = campfire_on(art, W, H, 600, 372, 120, nx, rng)
    art = marsh_stick(art, W, H, 760, 430, 650, 330, nx)
    art = marsh_stick(art, W, H, 450, 440, 545, 345, nx, toast=False)
    # log seat
    seat = rr_mask(W, H, 330, 404, 470, 438, 16)
    art = P(art, seat, BARK, "#7d5438", nx=nx, rough=0.8)
    art = P(art, shapes(W, H, [ellipse_pts(470, 421, 10, 17, 12)]), WOOD_L, nx=nx, rough=0.4)
    # flashlight in the grass, beam
    beam = shapes(W, H, [[(110, 430), (20, 380), (20, 470)]], smooth=False)
    art = tint(art, beam, "#fff1b8", 0.28, blur=6)
    art = flashlight_on(art, W, H, 112, 432, 0.9, nx, math.pi)
    art = add_grain(art, 13, 0.04)
    save(art, f"{OUT}/scene.webp", max_w=800, quality=80)
    preview(art, "uk-scene", bg=NIGHT2)


def flashlight_on(art, W, H, x, y, s, nx, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda u, v: (x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
    body = shapes(W, H, [[T(0, -12), T(70, -12), T(70, 12), T(0, 12)]], smooth=False)
    art = P(art, body, "#3b8fd0", "#2d74ad", nx=nx, rough=0.6)
    head = shapes(W, H, [[T(-26, -20), T(0, -13), T(0, 13), T(-26, 20)]], smooth=False)
    art = P(art, head, "#d9dcd6", "#b8bcb6", nx=nx, rough=0.5)
    lens = shapes(W, H, [[T(-30, -20), T(-25, -20), T(-25, 20), T(-30, 20)]], smooth=False)
    art = P(art, lens, "#fff3b0", nx=nx, rough=0.4)
    art = P(art, rr_mask(W, H, *T(30, -15), *T(44, -11), 3) if False else circles(W, H, [(*T(36, -12), 5 * s)]), "#e8743b", nx=nx, rough=0.3)
    return art


def flashlight():
    W, H = 200, 80
    nx = Seq(900)
    art = flashlight_on(blank(W, H), W, H, 60, 40, 1.4, nx, 0.0)
    save(art, f"{OUT}/flashlight.webp", max_w=140, quality=84)


def flame():
    W, H = 200, 240
    nx = Seq(400); rng = random.Random(4)
    art = blank(W, H)
    outer = shapes(W, H, [[(100, 10), (132, 80), (160, 120), (164, 170), (140, 220), (100, 232), (60, 220), (36, 170), (42, 120), (70, 84)]])
    art = OV(art, outer, lambda m: glow(m, "#ffb04a", 16, 0.45), pad=60)
    art = P(art, outer, "#f2662e", "#f58a35", nx=nx, rough=2.0)
    mid = shapes(W, H, [[(104, 60), (126, 120), (138, 168), (124, 214), (100, 222), (76, 214), (64, 170), (78, 120)]])
    art = P(art, mid, "#ffa53c", "#ffb84a", nx=nx, rough=1.6)
    core = shapes(W, H, [[(100, 120), (116, 160), (118, 196), (100, 212), (82, 196), (84, 160)]])
    art = P(art, core, YEL_L, YEL, nx=nx, rough=1.2)
    tongues = shapes(W, H, [[(56, 90), (66, 130), (48, 140)], [(150, 70), (152, 120), (136, 118)]], smooth=False)
    art = P(art, tongues, "#f2662e", nx=nx, rough=1.0)
    save(art, f"{OUT}/flame.webp", max_w=140, quality=84)
    preview(art, "uk-flame", bg=NIGHT2)


def owl():
    W, H = 280, 300
    nx = Seq(500); rng = random.Random(6)
    art = blank(W, H)
    # branch
    br = strokes(W, H, [(curve([(-10, 250), (120, 236), (290, 248)], 30), 18, (0.0, 0.0))])
    art = P(art, br, BARK, "#7d5438", nx=nx, rough=1.0)
    leaves = [petal_pts(30, 238, 50, 16, -2.4, n=12), petal_pts(250, 246, 50, 16, -0.6, n=12), petal_pts(262, 252, 44, 14, 0.4, n=12)]
    art = P(art, shapes(W, H, leaves), GRASS, GRASS_L, nx=nx, rough=1.0)
    # body (egg) + ear tufts
    body = shapes(W, H, [[(140, 52), (198, 80), (214, 150), (200, 220), (140, 246), (80, 220), (66, 150), (82, 80)]])
    tufts = shapes(W, H, [[(92, 76), (84, 34), (122, 62)], [(188, 76), (196, 34), (158, 62)]], smooth=False)
    sil = np.maximum(body, tufts)
    art = P(art, sil, "#8b6a52", "#9c7a5e", nx=nx)
    belly = shapes(W, H, [ellipse_pts(140, 182, 48, 58, 20)])
    art = P(art, belly, "#e9d3b0", "#dfc49d", nx=nx, rough=1.0)
    chev = []
    for r in range(3):
        for c in range(4 - r % 2):
            x = 112 + c * 19 + (r % 2) * 9; y = 160 + r * 20
            chev.append(([(x - 6, y), (x, y + 6), (x + 6, y)], 2.2, None))
    art = tint(art, strokes(W, H, chev) * belly, "#a47e5e", 0.85)
    # wings
    for sgn in (-1, 1):
        wing = shapes(W, H, [[(140 + sgn * 48, 120), (140 + sgn * 74, 160), (140 + sgn * 66, 214), (140 + sgn * 46, 196)]])
        art = P(art, wing, "#6f5240", nx=nx, rough=0.8)
    # face disc + big eyes
    disc = shapes(W, H, [ellipse_pts(112, 112, 34, 32, 18), ellipse_pts(168, 112, 34, 32, 18)])
    art = P(art, disc, "#f2e2c4", nx=nx, rough=0.6)
    for ex in (112, 168):
        art = P(art, circles(W, H, [(ex, 114, 22)]), "#ffc845", "#f5b432", nx=nx, rough=0.4)
        art = P(art, circles(W, H, [(ex + 2, 116, 13)]), INK, nx=nx, rough=0.3)
        art = tint(art, circles(W, H, [(ex - 3, 110, 4.5), (ex + 6, 122, 2)]), "#ffffff", 0.95)
    beak = shapes(W, H, [[(132, 134), (148, 134), (140, 152)]], smooth=False)
    art = P(art, beak, ORANGE, nx=nx, rough=0.4)
    feet = circles(W, H, [(122 + k * 7, 240, 5) for k in range(3)] + [(150 + k * 7, 240, 5) for k in range(3)])
    art = P(art, feet, ORANGE_D, nx=nx, rough=0.3)
    # tiny party hat (birthday!)
    hat = shapes(W, H, [[(140, 6), (162, 64), (118, 64)]], smooth=False)
    art = P(art, hat, "#7fd3c4", "#5fb8a8", nx=nx, rough=0.6)
    art = tint(art, strokes(W, H, [([(126, 46), (156, 34)], 4, None), ([(122, 60), (160, 52)], 4, None)]) * hat, "#ff9fb5", 0.95)
    art = P(art, circles(W, H, [(140, 8, 7)]), YEL, nx=nx, rough=0.4)
    art = tint(art, edge_ring(sil, 1.6), "#4e3a2c", 0.6)
    art = add_grain(art, 7, 0.04)
    save(art, f"{OUT}/owl.webp", max_w=200, quality=84)
    preview(art, "uk-owl", bg=NIGHT)


def sign():
    """Hanging camp sign: three pine planks with grain, nail heads, two ropes up to the top."""
    W, H = 700, 500
    nx = Seq(600); rng = random.Random(8)
    art = blank(W, H)
    ropes = strokes(W, H, [([(150, 0), (160, 120)], 6, None), ([(550, 0), (540, 120)], 6, None)])
    art = P(art, ropes, "#d9c39a", "#c4ab7e", nx=nx, rough=0.5)
    planks = []
    for k in range(3):
        y0 = 120 + k * 120
        planks.append(deform([(40, y0 + 4), (660, y0), (664, y0 + 112), (36, y0 + 116)], rng, 1, 0.006))
    for k, pl in enumerate(planks):
        m = shapes(W, H, [pl], smooth=False)
        art = P(art, m, mix(WOOD_L, WOOD, 0.3 + k * 0.15), WOOD_L, nx=nx, rough=1.0, streak=1.6)
        y0 = 120 + k * 120
        gr = []
        for j in range(7):
            yy = y0 + 14 + j * 14 + rng.uniform(-3, 3)
            pts = [(x, yy + math.sin(x / rng.uniform(40, 80) + j) * 3) for x in range(46, 656, 10)]
            gr.append((pts, rng.uniform(1.0, 1.8), (0.2, 0.2)))
        art = tint(art, strokes(W, H, gr) * m, WOOD_D, 0.35)
        knot = ellipse_pts(rng.uniform(120, 580), y0 + rng.uniform(40, 70), 14, 7, 12)
        art = tint(art, strokes(W, H, [(knot + knot[:1], 2.2, None)]) * m, WOOD_D, 0.6)
        art = tint(art, edge_ring(m, 2.0), "#7a4e2c", 0.8)
        art = P(art, circles(W, H, [(62, y0 + 58, 6), (638, y0 + 58, 6)]), "#5a5a5a", nx=nx, rough=0.3)
    art = add_grain(art, 9, 0.04)
    save(art, f"{OUT}/sign.webp", max_w=600, quality=82)
    preview(art, "uk-sign", bg=NIGHT)


def marsh():
    W, H = 640, 120
    nx = Seq(700)
    art = blank(W, H)
    art = marsh_stick(art, W, H, 16, 84, 300, 56, nx, k_=1.8)
    art = marsh_stick(art, W, H, 624, 84, 340, 56, nx, toast=False, k_=1.8)
    save(art, f"{OUT}/marsh.webp", max_w=400, quality=84)


def pines():
    W, H = 820, 230
    nx = Seq(800); rng = random.Random(12)
    art = blank(W, H)
    tri = []
    x = -20
    while x < W + 40:
        h = rng.uniform(110, 210)
        for t in range(4):
            yy = H - h + t * h * 0.2
            ww = 18 + t * 14
            tri.append([(x, yy - 12), (x + ww, yy + h * 0.26), (x - ww, yy + h * 0.26)])
        x += rng.uniform(46, 80)
    m = shapes(W, H, tri, smooth=False)
    art = P(art, m, PINE, PINE_D, nx=nx, rough=1.4)
    ground = shapes(W, H, [[(-10, 200), (W + 10, 196), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    art = P(art, ground, GRASS_D, nx=nx)
    save(art, f"{OUT}/pines.webp", max_w=800, quality=78)


for p in PARTS:
    globals()[p]()
    clear()
