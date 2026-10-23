"""Pakpak Dairi — original painted art inspired by Pakpak country (Dairi, Sumatera Utara): misty green ridges around
Sidikalang, a Pakpak rumah adat on stilts with an upswept saddle roof of black ijuk and a front gable painted in red,
white and black geometric bands; oles-style striped cloth; a sprig of coffee in white bloom. No figures.
Run: python3 -I pakpak-dairi.py [part ...]   parts: scene oles gable sprig
Assets -> public/themes/art/pakpak-dairi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h1_lib import *  # noqa
import _jw_lib as jw

OUT = outdir("pakpak-dairi")
PARTS = sys.argv[1:] or ["scene", "oles", "gable", "sprig"]
SKY_T, SKY_B = "#e9ede4", "#dfe7dc"
FAR, FAR2 = "#b9c8c0", "#a3b8ae"
MID, MID2 = "#7f9f78", "#5f8a5e"
NEAR, NEAR2 = "#3f6b45", "#2c5236"
IJUK, IJUK2 = "#2a2622", "#1a1715"
WOOD, WOOD_D, WOOD_L = "#7a5434", "#4a321e", "#a87a50"
RED, WHITE, BLACK = "#b2302a", "#f2ece0", "#1d1a1a"


def gable_paint(art, W, H, tri, nx, rng):
    """Painted gable face: horizontal registers of red/white/black triangles, a central lozenge and spirals."""
    (ax, ay), (bx, by), (cx_, cy_) = tri  # apex, bottom-right, bottom-left
    m = poly(W, H, tri)
    art = GP(art, m, "#d9cdb4", "#cbbd9f", seed=nx(), rough=1.0, streak=0.6)
    top_y, bot_y = ay, max(by, cy_)
    regs = 5
    for k in range(regs):
        y0 = top_y + (bot_y - top_y) * (0.18 + 0.82 * k / regs)
        y1 = top_y + (bot_y - top_y) * (0.18 + 0.82 * (k + 1) / regs)
        band = m * rect(W, H, 0, y0, W, y1)
        if k % 2 == 0:
            # row of triangles (tumpal-like teeth) alternating red / black
            polys_r, polys_b = [], []
            n = 10
            for i in range(n):
                x0 = cx_ - 30 + (bx - cx_ + 60) * i / n
                x1 = cx_ - 30 + (bx - cx_ + 60) * (i + 1) / n
                tri_ = [(x0, y1), ((x0 + x1) / 2, y0 + 2), (x1, y1)]
                (polys_r if i % 2 == 0 else polys_b).append(tri_)
            art = GP(art, shapes(W, H, polys_r, smooth=False) * band, RED, "#9a2620", seed=nx(), rough=0.7, streak=0.5)
            art = GP(art, shapes(W, H, polys_b, smooth=False) * band, BLACK, seed=nx(), rough=0.7, streak=0.5)
        else:
            art = GP(art, band, BLACK, "#2a2424", seed=nx(), rough=0.7, streak=0.5)
            # white zig-zag line through the black register
            zz = []
            n = 14
            for i in range(n + 1):
                x = cx_ - 20 + (bx - cx_ + 40) * i / n
                zz.append((x, y0 + (y1 - y0) * (0.25 if i % 2 == 0 else 0.75)))
            art = GP(art, strokes(W, H, [(zz, 1.8, None)]) * band, WHITE, seed=nx(), rough=0.4, streak=0.3)
    # lozenge + spirals near the apex
    lx, ly = ax + (cx_ + bx - 2 * ax) * 0.08, top_y + (bot_y - top_y) * 0.11
    s = (bx - cx_) * 0.07
    loz = shapes(W, H, [[(lx, ly - s * 1.2), (lx + s, ly), (lx, ly + s * 1.2), (lx - s, ly)]], smooth=False)
    art = GP(art, loz * m, RED, seed=nx(), rough=0.5, streak=0.4)
    art = GP(art, circles(W, H, [(lx, ly, s * 0.32)]) * m, WHITE, seed=nx(), rough=0.3, streak=0.3)
    # outline (dark painted edge)
    edge = np.clip(m - gaussian_filter(m, 1.6) * 1.15, 0, 1) * 2.5
    art = G(art, edge, "#2a1c14", seed=nx(), density=0.75, edge=0, rough=0.4, feather=0.5)
    # weathering
    art = G(art, m * np.clip((fbm(W, H, nx(), 30, 3) - 0.55) * 2, 0, 1), "#6e5a40", seed=nx(), density=0.25, edge=0.2, bloom=0.5, rough=2, feather=2)
    return art


def ijuk_roof(art, W, H, mask, nx, rng, x0, x1, top_fn, bot_fn):
    """Black ijuk thatch: dark gouache body plus many fine fibre strokes following the fall line."""
    art = GP(art, mask, IJUK, IJUK2, seed=nx(), rough=1.4, streak=0.9)
    fib = []
    for _ in range(int((x1 - x0) * 2.2)):
        x = rng.uniform(x0, x1)
        yt, yb = top_fn(x), bot_fn(x)
        if yb - yt < 6:
            continue
        a = rng.uniform(0, 0.4)
        y = yt + (yb - yt) * a
        L = (yb - yt) * rng.uniform(0.25, 0.6)
        fib.append(([(x, y), (x + rng.uniform(-3, 3), y + L * 0.5), (x + rng.uniform(-5, 5), y + L)], rng.uniform(0.7, 1.4), (0.1, 0.4)))
    f = strokes(W, H, fib) * mask
    art = G(art, f, "#7d7264", seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    fib2 = [([(p[0][0] + 2, p[0][1] + 3)] + [(q[0] + 2, q[1] + 3) for q in p[1:]], w, t) for p, w, t in fib[::2]]
    art = G(art, strokes(W, H, fib2) * mask, "#0e0c0b", seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.4)
    # lit upper sweep, darker eave
    art = G(art, mask * np.clip(1 - ygrad(W, H, top_fn((x0 + x1) / 2) - 40, bot_fn((x0 + x1) / 2)), 0, 1) * 0.6, "#8e8a7e", seed=nx(), density=0.35, edge=0, bloom=0.4, rough=2, feather=3)
    return art


def house(art, W, H, nx, rng, cx, gy, s=1.0):
    """Rumah adat Pakpak, 3/4 view (front gable on the left). cx = centre of the side wall, gy = ground line."""
    S = lambda x, y: (cx + x * s, gy + y * s)
    # stilts + ladder
    posts = []
    for px in (-150, -112, -60, -5, 50, 105, 140):
        posts.append(([S(px, -70), S(px + rng.uniform(-2, 2), 0)], 9 * s, None))
    pm = strokes(W, H, posts)
    art = GP(art, pm, WOOD_D, "#3a2616", seed=nx(), rough=1.0, streak=0.8)
    beams = [([S(-185, -62), S(150, -62)], 6 * s, None), ([S(-185, -30), S(-110, -30)], 4 * s, None)]
    art = GP(art, strokes(W, H, beams), WOOD, WOOD_D, seed=nx(), rough=0.8, streak=0.7)
    lad = [([S(-205, 2), S(-178, -76)], 4 * s, None), ([S(-180, 4), S(-152, -74)], 4 * s, None)]
    for k in range(5):
        t = (k + 1) / 6
        y = -76 * t
        lad.append(([S(-205 + 27 * t, y), S(-180 + 28 * t, y)], 3 * s, None))
    art = GP(art, strokes(W, H, lad), WOOD_L, WOOD, seed=nx(), rough=0.6, streak=0.6)
    # side wall (planks)
    side = poly(W, H, [S(-110, -150), S(150, -150), S(150, -70), S(-110, -70)])
    art = GP(art, side, WOOD, "#6a4528", seed=nx(), rough=1.0, streak=0.9)
    planks = [([S(-110, -150 + k * 11), S(150, -150 + k * 11)], 1.2 * s, None) for k in range(1, 8)]
    art = G(art, strokes(W, H, planks) * side, WOOD_D, seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    band = poly(W, H, [S(-110, -146), S(150, -146), S(150, -128), S(-110, -128)])
    art = GP(art, band, RED, "#962620", seed=nx(), rough=0.6, streak=0.5)
    dia = []
    for k in range(16):
        x = -104 + k * 16.5
        dia.append([S(x, -137), S(x + 6, -143), S(x + 12, -137), S(x + 6, -131)])
    art = GP(art, shapes(W, H, dia, smooth=False), WHITE, seed=nx(), rough=0.4, streak=0.3)
    win = [poly(W, H, [S(x, -118), S(x + 22, -118), S(x + 22, -88), S(x, -88)]) for x in (-60, 20, 90)]
    for wm in win:
        art = G(art, wm, "#1f150e", seed=nx(), density=0.9, edge=0.4, rough=0.4, feather=0.5)
    # front wall (under the gable), slightly turned
    front = poly(W, H, [S(-195, -156), S(-110, -150), S(-110, -70), S(-195, -66)])
    art = GP(art, front, "#6a4528", WOOD_D, seed=nx(), rough=1.0, streak=0.9)
    fb = poly(W, H, [S(-195, -152), S(-110, -146), S(-110, -128), S(-195, -132)])
    art = GP(art, fb, BLACK, seed=nx(), rough=0.6, streak=0.4)
    art = GP(art, strokes(W, H, [([S(-195, -142), S(-110, -137)], 2.0 * s, None)]), RED, seed=nx(), rough=0.4, streak=0.3)
    door = poly(W, H, [S(-168, -118), S(-138, -116), S(-138, -72), S(-168, -71)])
    art = G(art, door, "#1a120c", seed=nx(), density=0.95, edge=0.4, rough=0.4, feather=0.5)
    art = G(art, front, "#1c140e", seed=nx(), density=0.25, edge=0, rough=1, feather=2)
    # roof: upswept saddle with overhanging horns
    def ridge(x):
        t = (x - (-235)) / (215 - (-235))
        u = abs(t - 0.5) * 2
        return -258 - 62 * u ** 1.9
    def eave(x):
        t = (x - (-235)) / (215 - (-235))
        u = abs(t - 0.5) * 2
        return -150 - 22 * u ** 2.2
    xs = [(-235 + 450 * i / 60) for i in range(61)]
    top = [S(x, ridge(x)) for x in xs]
    bot = [S(x, eave(x)) for x in reversed(xs[4:-4])]
    roof = poly(W, H, top + bot, smooth=False)
    roof = displace(roof, nx(), 1.5, 12)
    top_fn = lambda X: gy + ridge((X - cx) / s) * s
    bot_fn = lambda X: gy + eave((X - cx) / s) * s
    art = ijuk_roof(art, W, H, roof, nx, rng, cx - 235 * s, cx + 215 * s, top_fn, bot_fn)
    # ridge cap (bamboo/zinc line) and the horn tips
    cap = strokes(W, H, [([S(x, ridge(x) - 1) for x in xs[2:-2]], 5 * s, (0.05, 0.05))])
    art = GP(art, cap, "#3d3833", "#59524a", seed=nx(), rough=0.6, streak=0.5)
    tips = strokes(W, H, [([S(-235, ridge(-235)), S(-252, ridge(-235) - 26)], 6 * s, (0.0, 0.6)),
                          ([S(215, ridge(215)), S(233, ridge(215) - 24)], 6 * s, (0.0, 0.6))])
    art = GP(art, tips, "#e8e0cc", "#cbbf9f", seed=nx(), rough=0.5, streak=0.3)
    # front gable face under the left horn
    tri = [S(-226, ridge(-226) + 10), S(-112, -158), S(-205, -160)]
    art = gable_paint(art, W, H, tri, nx, rng)
    # cast shadow under the eave
    sh = poly(W, H, [S(-110, -150), S(150, -150), S(150, -132), S(-110, -128)])
    art = G(art, sh, "#120c08", seed=nx(), density=0.45, edge=0, rough=0.6, feather=2.5)
    # ground shadow
    gs = ellipses(W, H, [(cx - 20 * s, gy + 2, 210 * s, 12 * s, 0)])
    art = G(art, gs, "#22301f", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=3, feather=5)
    return art


def coffee_shrub(art, W, H, x, y, r, nx, rng, dark=NEAR2, mid=NEAR, light="#6f9a5c", flowers=8):
    leaves = []
    for _ in range(int(r * 0.9)):
        a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
        d = rng.uniform(0.1, 1.0) * r
        px, py = x + math.cos(a) * d * 1.25, y + math.sin(a) * d * 0.75
        la = rng.uniform(-0.6, 0.6) + (math.pi if px < x else 0) + rng.uniform(-0.4, 0.4)
        L = rng.uniform(r * 0.14, r * 0.26)
        leaves.append(deform(petal_pts(px, py, L, L * 0.38, la, n=9), rng, 1, L * 0.05))
    m = shapes(W, H, leaves)
    k = len(leaves) // 3
    art = G(art, m, dark, mid, seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=2, feather=1)
    art = G(art, shapes(W, H, leaves[:k]), light, seed=nx(), density=0.55, edge=0.5, bloom=0.3, rough=1.5, feather=0.8)
    for _ in range(flowers):
        a = rng.uniform(math.pi * 1.1, math.pi * 1.9)
        d = rng.uniform(0.2, 0.9) * r
        art = jw.white_flower(art, W, H, x + math.cos(a) * d * 1.2, y + math.sin(a) * d * 0.7, rng.uniform(4.5, 7), rng, nx, petals=5, shade="#8ea08a")
    return art


def part_scene():
    W, H = 780, 1120
    rng = random.Random(11); nx = Seq(100)
    sky = painted_sky(W, H, [(0, "#eef0e6"), (0.35, SKY_T), (0.55, SKY_B), (1, "#d6e0d2")], seed=4, streak=0.5)
    art = sky.copy()
    # far ridges (bluish), three layers with mist between
    for i, (base, amp, c1, c2, dens) in enumerate([(470, 100, "#bccbca", "#a9bcbd", 0.7), (545, 120, "#9fb5ab", "#89a49a", 0.78), (615, 90, "#86a487", "#6f9274", 0.85)]):
        m = poly(W, H, ridge_pts(W, base, amp, rng, step=12, freq=(1.1 + i * 0.4, 2.7 + i)), smooth=True)
        m = displace(m, nx(), 3, 30)
        art = G(art, m, c1, c2, seed=nx(), density=dens, edge=0.35, bloom=0.45, rough=5, feather=2.5, gran=0.15)
        art = over(art, mist(W, H, [(base + 12, 22, -40, W + 40, 0.42), (base - amp * 0.4, 14, rng.uniform(-40, 200), rng.uniform(500, 820), 0.25)], nx, rng, col="#f1f3ee"))
        clear()
    # forest patches on the near ridge: bumpy continuous tree lines in a few groups
    crowns = []
    for gx in (40, 230, 330, 610, 700):
        n = rng.randint(10, 18)
        for k in range(n):
            x = gx + k * rng.uniform(6, 10)
            r = rng.uniform(8, 14)
            yb = 598 + rng.uniform(-6, 8) + 10 * math.sin(gx)
            crowns.append((x, yb - r * 0.4, r, r * 1.2, rng.uniform(-10, 10)))
            crowns.append((x + 3, yb + 6, r * 1.1, r * 0.9, 0))
    art = G(art, ellipses(W, H, crowns), "#5f8467", "#4b7257", seed=nx(), density=0.7, edge=0.45, bloom=0.4, rough=2.5, feather=1)
    art = over(art, mist(W, H, [(618, 24, -40, W + 40, 0.45)], nx, rng, col="#eef1ec"))
    clear()
    # mid green hill where the house stands (rises to the right)
    hp = [(-20, H + 20)]
    for x in range(-20, W + 21, 12):
        y = 742 - 60 * (x / W) - 18 * math.sin(x / W * math.pi * 2.3 + 0.6) + rng.uniform(-1.5, 1.5)
        hp.append((x, y))
    hp.append((W + 20, H + 20))
    hm = displace(poly(W, H, hp, smooth=True), nx(), 2, 26)
    art = G(art, hm, MID, MID2, seed=nx(), density=0.88, edge=0.4, bloom=0.4, rough=4, feather=1.5)
    # coffee hedgerows on the slope: overlapping bush dabs, smaller in the distance, shadow under each row
    for r_ in range(8):
        yy = 752 + r_ * 20 + r_ * r_ * 1.6
        sc = 0.55 + r_ * 0.12
        bl, sh = [], []
        x = -30 + rng.uniform(0, 20)
        while x < W + 30:
            rx = rng.uniform(10, 16) * sc
            yv = yy - 60 * (x / W) - 11 * math.sin(x / W * math.pi * 2.3 + 0.6)
            bl.append((x, yv - rx * 0.3, rx * 1.3, rx * rng.uniform(0.7, 0.95), rng.uniform(-8, 8)))
            sh.append((x, yv + rx * 0.45, rx * 1.4, rx * 0.35, 0))
            x += rx * rng.uniform(1.1, 1.6) if rng.random() > 0.06 else rx * 4
        art = G(art, ellipses(W, H, sh) * hm, "#2f5434", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=1.5, feather=1.5)
        art = G(art, ellipses(W, H, bl) * hm, "#55834f", "#3f6d45", seed=nx(), density=0.62, edge=0.5, bloom=0.35, rough=2, feather=0.8)
    art = G(art, hm * ygrad(W, H, 700, 980), "#355f3c", seed=nx(), density=0.3, edge=0, bloom=0.4, rough=3, feather=3)
    clear()
    # the house
    art = house(art, W, H, nx, rng, cx=545, gy=712, s=0.82)
    clear()
    # low mist drifting in front of the house base
    art = over(art, mist(W, H, [(728, 16, 330, W + 60, 0.4), (800, 26, -60, 380, 0.4)], nx, rng, col="#f2f4ef"))
    clear()
    # foreground: dark coffee shrubs in bloom along the bottom
    fg = [(-20, H + 20)]
    for x in range(-20, W + 21, 10):
        fg.append((x, 960 + 30 * math.sin(x / W * math.pi * 1.6 + 2.1) + rng.uniform(-2, 2)))
    fg.append((W + 20, H + 20))
    fm = displace(poly(W, H, fg, smooth=True), nx(), 2, 22)
    art = G(art, fm, NEAR, NEAR2, seed=nx(), density=0.95, edge=0.4, bloom=0.3, rough=3, feather=1.5)
    for (x, y, r) in [(70, 990, 120), (260, 1010, 110), (470, 1000, 120), (690, 975, 130)]:
        art = coffee_shrub(art, W, H, x, y, r, nx, rng, flowers=7)
        clear()
    # fade the bottom edge into paper
    fade = ygrad(W, H, H - 90, H)
    art[..., 3] *= 1 - fade * 0.0
    preview(art, "pk-scene")
    save_rgb(art, f"{OUT}/scene.webp", size=(780, 1120), quality=74)
    clear()


def part_oles():
    """Seamless (in x) woven band: black ground, red and white stripes, a central row of white/yellow lozenges."""
    W, H = 320, 120
    rgb = cloth(W, H, base=BLACK, seed=5, tile=True, weave=1.6, strength=0.12)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    xx = np.ones((H, 1), np.float32) * np.arange(W, dtype=np.float32)[None, :]
    weave = cloth(W, H, base="#ffffff", seed=6, tile=True, weave=1.6, strength=0.15)

    def band(y0, y1, col, a=1.0):
        nonlocal rgb
        m = ((yy >= y0) & (yy < y1)).astype(np.float32) * a
        c = col_arr(col)[None, None, :] * weave
        rgb = rgb * (1 - m[..., None]) + c * m[..., None]

    for y0, y1, c in [(4, 12, RED), (14, 16, WHITE), (18, 22, RED), (98, 102, RED), (104, 106, WHITE), (108, 116, RED),
                      (30, 33, "#d9a640"), (87, 90, "#d9a640")]:
        band(y0, y1, c)
    band(36, 84, "#2a1c1c", 0.6)
    # supplementary-weft lozenges, period 40px -> 8 per tile
    P = 40
    u = (xx % P) - P / 2
    v = yy - 60
    loz = (np.abs(u) / 16 + np.abs(v) / 20 <= 1) & (np.abs(u) / 16 + np.abs(v) / 20 >= 0.62)
    core = (np.abs(u) / 16 + np.abs(v) / 20 <= 0.3)
    hook = ((np.abs(u) > 13) & (np.abs(v) < 2.2))
    for m, c in [(loz, WHITE), (core, RED), (hook, "#d9a640")]:
        mm = m.astype(np.float32)
        # float-stitch look: break into short horizontal floats
        mm *= (0.65 + 0.35 * (np.sin(xx * math.pi / 2.0) > -0.6))
        rgb = rgb * (1 - mm[..., None]) + (col_arr(c)[None, None, :] * weave) * mm[..., None]
    # small tooth rows near the edges
    t = (np.abs((xx % 20) - 10) / 10)
    teeth = ((yy >= 24) & (yy < 30) & (yy - 24 < (1 - t) * 6)) | ((yy >= 90) & (yy < 96) & (96 - yy < (1 - t) * 6))
    rgb = rgb * (1 - teeth[..., None] * 0.9) + col_arr(WHITE)[None, None, :] * weave * teeth[..., None] * 0.9
    prev_rgb(rgb, "pk-oles")
    rgb_save(rgb, f"{OUT}/oles.webp", quality=80)
    rgb_save(np.ascontiguousarray(np.rot90(rgb, 1)), f"{OUT}/oles-v.webp", quality=80)


def part_gable():
    """Stand-alone gable emblem (front view): the painted triangle under an inverted-V ijuk eave whose ends sweep up
    into horns, for dividers/nodes/emblems."""
    W, H = 440, 320
    rng = random.Random(21); nx = Seq(900)
    art = blank(W, H)
    W, H = 440, 330
    art = blank(W, H)
    tri = [(W / 2, 84), (W - 84, 318), (84, 318)]
    art = gable_paint(art, W, H, tri, nx, rng)
    # roof hood: a flaring inverted-V of ijuk over the triangle, ends sweeping up into horns
    band = poly(W, H, [(W / 2, 30), (W * 0.74, 150), (W - 26, 250), (W - 4, 236), (W - 8, 270), (W - 64, 292), (W / 2, 90),
                       (64, 292), (8, 270), (4, 236), (26, 250), (W * 0.26, 150)], smooth=True)
    band = displace(band, nx(), 1.2, 10)
    art = ijuk_roof(art, W, H, band, nx, rng, 0, W, lambda x: 30 + (abs(x - W / 2) / (W / 2)) * 210, lambda x: 90 + (abs(x - W / 2) / (W / 2)) * 200)
    tips = strokes(W, H, [([(8, 256), (2, 226)], 7, (0, 0.6)), ([(W - 8, 256), (W - 2, 226)], 7, (0, 0.6))])
    art = GP(art, tips, "#e8e0cc", seed=nx(), rough=0.4, streak=0.3)
    preview(art, "pk-gable")
    save(art, f"{OUT}/gable.webp", max_w=240, quality=84)
    clear()


def part_sprig():
    W, H = 640, 360
    rng = random.Random(31); nx = Seq(1400)
    art = blank(W, H)
    stem = curve([(20, 300), (180, 250), (360, 200), (520, 150), (620, 120)], 60)
    art = G(art, stroke_mask(W, H, stem, 7, (0.02, 0.4)), "#6b5a3c", "#4b3e28", seed=nx(), density=0.85, edge=0.5, rough=1, feather=0.6)
    for i, t in enumerate(np.linspace(0.08, 0.92, 9)):
        k = int(t * (len(stem) - 1))
        x, y = stem[k]
        for side in (-1, 1):
            ang = -0.45 + side * rng.uniform(0.75, 1.4) + rng.uniform(-0.25, 0.25)
            L = rng.uniform(70, 125) * (1.1 - t * 0.4)
            lm = shape_mask(W, H, petal_pts(x, y, L, L * 0.26, ang, n=12))
            art = G(art, lm, "#4c7d48", "#24482c", seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=2.5, feather=0.8)
            art = G(art, shape_mask(W, H, petal_pts(x, y, L * 0.95, L * 0.1, ang + 0.06, n=10)), "#1d3a24", seed=nx(), density=0.35, edge=0.2, rough=1.5)
            vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in np.linspace(0.05, 0.9, 8)]
            art = G(art, stroke_mask(W, H, vein, 1.6), "#a9c49a", seed=nx(), density=0.45, edge=0, rough=0.5, feather=0.4)
        if i % 2 == 0:
            clear()
        # clusters of white blossoms and a few green/red cherries at the nodes
        for _ in range(rng.randint(3, 5)):
            art = jw.white_flower(art, W, H, x + rng.uniform(-12, 12), y + rng.uniform(-14, 6), rng.uniform(6, 8.5), rng, nx, petals=5, shade="#7f9481")
        if i % 3 == 1:
            ch = [(x + rng.uniform(-10, 10), y + rng.uniform(4, 14), rng.uniform(4.5, 6)) for _ in range(3)]
            art = G(art, circles(W, H, ch), "#8aa848" if i < 5 else "#b3352a", seed=nx(), density=0.85, edge=0.6, rough=0.6, feather=0.5)
    preview(art, "pk-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=82)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
