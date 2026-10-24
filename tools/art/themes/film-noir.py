"""Film Noir — black-and-white gouache/ink-wash night scene: a rain-slick street under a cast-iron lamp, a lit window
with venetian blinds, and two stylised silhouettes (fedora + trench coat, wide-brim hat + belted coat) sharing an
umbrella, their reflections smeared in the wet street. Extra pieces: venetian-blind light (transparent), a painted
lamp glow (flickers), a fedora emblem, the couple silhouette on its own.
Run: python3 -I film-noir.py [part ...]   parts: scene couple blinds glow hat
Assets -> public/themes/art/film-noir/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s4_lib import *  # noqa

OUT = outdir("film-noir")
PARTS = sys.argv[1:] or ["scene", "couple", "blinds", "glow", "hat"]
BLACK, INK, CHAR, SMOKE, FOG, SILVER, WHITE = "#0b0b0c", "#151516", "#2a2a2c", "#4a4a4d", "#7d7c7a", "#b9b7b2", "#efede7"


def couple_masks(W, H, mx, fy, s):
    """Silhouette masks (man, woman, umbrella canopy, umbrella shaft) in figure units of s px."""
    def P(x, y):
        return (mx + (x + y * 0.035) * s, fy - y * s)
    man = shapes(W, H, [
        [P(-0.02, 0.815), P(0.08, 0.81), P(0.125, 0.79), P(0.12, 0.70), P(0.105, 0.58), P(0.13, 0.42), P(0.165, 0.27), P(0.06, 0.255), P(-0.07, 0.262), P(-0.16, 0.285), P(-0.125, 0.42), P(-0.11, 0.58), P(-0.125, 0.70), P(-0.135, 0.785)],  # coat
    ], smooth=True)
    man = np.maximum(man, shapes(W, H, [
        [P(-0.07, 0.29), P(-0.015, 0.29), P(-0.02, 0.02), P(-0.075, 0.02)],  # leg L
        [P(0.015, 0.29), P(0.07, 0.29), P(0.075, 0.02), P(0.02, 0.02)],  # leg R
        [P(-0.09, 0.02), P(-0.01, 0.025), P(-0.005, 0.0), P(-0.1, 0.0)],
        [P(0.015, 0.025), P(0.1, 0.02), P(0.11, 0.0), P(0.01, 0.0)],
        [P(-0.1, 0.80), P(-0.035, 0.80), P(-0.05, 0.86)],  # collar up
        [P(0.03, 0.80), P(0.095, 0.80), P(0.055, 0.86)],
        [P(-0.03, 0.80), P(0.035, 0.80), P(0.03, 0.84), P(-0.025, 0.84)],  # neck
        [P(-0.14, 0.922), P(-0.07, 0.905), P(0.07, 0.903), P(0.145, 0.925), P(0.12, 0.895), P(-0.12, 0.893)],  # brim
        [P(-0.07, 0.9), P(0.07, 0.9), P(0.062, 0.958), P(0.03, 0.968), P(0.0, 0.962), P(-0.03, 0.97), P(-0.062, 0.96)],  # crown with a soft dent
        [P(0.10, 0.79), P(0.14, 0.72), P(0.165, 0.76), P(0.13, 0.82)],  # raised arm to the umbrella
    ], smooth=False))
    man = np.maximum(man, ellipses(W, H, [(mx + 0.01 * s, fy - 0.865 * s, 0.05 * s, 0.062 * s, 0)]))
    wx = mx + 0.27 * s
    def Q(x, y):
        return (wx + (x - y * 0.03) * s, fy - y * s)
    woman = shapes(W, H, [
        [Q(-0.02, 0.755), Q(0.07, 0.75), Q(0.10, 0.73), Q(0.09, 0.64), Q(0.068, 0.56), Q(0.10, 0.42), Q(0.17, 0.27), Q(0.0, 0.255), Q(-0.155, 0.27), Q(-0.10, 0.42), Q(-0.07, 0.56), Q(-0.09, 0.64), Q(-0.11, 0.73)],  # coat
    ], smooth=True)
    woman = np.maximum(woman, shapes(W, H, [
        [Q(-0.045, 0.28), Q(-0.01, 0.28), Q(-0.022, 0.03), Q(-0.045, 0.03)],
        [Q(0.015, 0.28), Q(0.05, 0.28), Q(0.045, 0.03), Q(0.02, 0.03)],
        [Q(-0.06, 0.035), Q(-0.015, 0.03), Q(-0.02, 0.0), Q(-0.04, 0.0)],
        [Q(0.015, 0.03), Q(0.065, 0.035), Q(0.05, 0.0), Q(0.03, 0.0)],
        [Q(-0.025, 0.74), Q(0.03, 0.74), Q(0.025, 0.79), Q(-0.02, 0.79)],
        [Q(-0.085, 0.565), Q(0.075, 0.565), Q(0.073, 0.545), Q(-0.083, 0.545)],  # belt
        [Q(-0.10, 0.73), Q(-0.16, 0.62), Q(-0.135, 0.6), Q(-0.07, 0.68)],  # arm linked through his
    ], smooth=False))
    woman = np.maximum(woman, ellipses(W, H, [(wx, fy - 0.83 * s, 0.045 * s, 0.056 * s, 0), (wx + 0.005 * s, fy - 0.875 * s, 0.15 * s, 0.024 * s, -8),
                                              (wx + 0.01 * s, fy - 0.9 * s, 0.065 * s, 0.035 * s, -8)]))
    ux, uy = mx + 0.13 * s, fy - 1.18 * s
    canopy = []
    for k in range(41):
        t = k / 40
        a = math.pi + t * math.pi
        canopy.append((ux + math.cos(a) * 0.36 * s, uy + 0.16 * s + math.sin(a) * 0.17 * s))
    rib = []
    for k in range(7):
        t0, t1 = k / 7, (k + 1) / 7
        for j in range(6):
            t = t0 + (t1 - t0) * j / 6
            x = ux - 0.36 * s + 0.72 * s * t
            rib.append((x, uy + 0.16 * s + 0.025 * s * math.sin(math.pi * j / 6)))
    rib.append((ux + 0.36 * s, uy + 0.16 * s))
    umb = poly(W, H, canopy + rib[::-1], smooth=False)
    umb = np.maximum(umb, strokes(W, H, [([(ux, uy - 0.03 * s), (ux, uy + 0.02 * s)], 0.012 * s, None)]))
    shaft = strokes(W, H, [([(ux, uy + 0.16 * s), (ux + 0.01 * s, fy - 0.74 * s)], 0.012 * s, None),
                           (arc_pts(ux + 0.03 * s, fy - 0.74 * s, 0.022 * s, math.pi, 0, 10, 1.0), 0.012 * s, None)])
    return man, woman, umb, shaft, (ux, uy)


def paint_couple(art, W, H, mx, fy, s, nx, rim_from="left"):
    man, woman, umb, shaft, (ux, uy) = couple_masks(W, H, mx, fy, s)
    fig = np.clip(man + woman + umb + shaft, 0, 1)
    art = GP(art, fig, INK, BLACK, seed=nx(), rough=1.2, streak=0.6)
    # rim light from the lamp side + wet sheen on the umbrella
    sh = 4 if rim_from == "left" else -4
    rim = np.clip(fig - np.roll(fig, sh, 1), 0, 1) * (1 - ygrad(W, H, fy - 0.5 * s, fy)) * (0.35 + 0.65 * fbm(W, H, nx(), 20, 2))
    rim = gaussian_filter(rim, 0.6)
    art = GP(art, rim * 0.7, FOG, SILVER, seed=nx(), rough=0.6, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = umb * np.clip(1 - np.hypot(xx - (ux - 0.12 * s), yy - (uy + 0.05 * s)) / (0.2 * s), 0, 1)
    art = GP(art, sheen * 0.8, SMOKE, FOG, seed=nx(), rough=1, streak=0.6)
    return art, fig


def rain(W, H, rng, n, L=(20, 60), ang=1.75, wd=(0.8, 1.6), y0=0, y1=None):
    y1 = y1 or H
    items = []
    for _ in range(n):
        x = rng.uniform(-40, W + 40); y = rng.uniform(y0, y1)
        l = rng.uniform(*L)
        items.append(([(x, y), (x + math.cos(ang) * l, y + math.sin(ang) * l)], rng.uniform(*wd), (0.3, 0.3)))
    return strokes(W, H, items)


def part_scene():
    W, H = 760, 1700
    rng = random.Random(7); nx = Seq(300)
    art = painted_sky(W, H, [(0, "#101011"), (0.35, "#1b1b1d"), (0.6, "#26262a"), (0.66, "#3a3a3d"), (1, "#141415")], seed=nx(), streak=1.2, grain=0.8)
    # building on the right: wall with a lit window behind venetian blinds, brick courses barely visible
    wall = rect(W, H, 430, 0, W, 1020)
    art = GP(art, wall, "#1f1f21", "#18181a", seed=nx(), rough=1, streak=1.2)
    bricks, btone = brick_field(W, H, bw=40, bh=14, mortar=1.4, seed=3)
    art = GP(art, bricks * wall * (0.25 + 0.4 * btone), "#2a2a2d", seed=nx(), rough=0.5, streak=0.4)
    win = rect(W, H, 520, 380, 700, 640)
    art = GP(art, win, "#d9d6cf", "#bcb9b2", seed=nx(), rough=0.8, streak=0.6)
    slats = np.zeros((H, W), np.float32)
    for y in range(388, 636, 13):
        slats = np.maximum(slats, rect(W, H, 520, y, 700, y + 6))
    art = GP(art, slats * win, "#3b3b3e", "#2e2e31", seed=nx(), rough=0.4, streak=0.4)
    frame = np.clip(rect(W, H, 510, 370, 710, 650) - rect(W, H, 520, 380, 700, 640), 0, 1)
    frame = np.maximum(frame, rect(W, H, 606, 380, 614, 640))
    art = GP(art, frame, "#0e0e0f", seed=nx(), rough=0.5, streak=0.4)
    # a silhouette leaning on the sill? no: just a potted plant shadow
    art = over(art, glow(win, "#e9e6de", radius=26, strength=0.35))
    # door with a small awning
    door = rect(W, H, 470, 760, 560, 1010)
    art = GP(art, door, "#0f0f10", seed=nx(), rough=0.6, streak=0.5)
    awn = poly(W, H, [(455, 740), (575, 740), (590, 770), (440, 770)])
    art = GP(art, awn, "#2e2e31", "#3a3a3d", seed=nx(), rough=0.8, streak=0.8)
    clear()
    # distant skyline on the left (behind the lamp), very low contrast in the haze
    sky = []
    x = -20
    while x < 440:
        w = rng.uniform(40, 90); h = rng.uniform(200, 480)
        sky.append([(x, 1000 - h), (x + w, 1000 - h), (x + w, 1000), (x, 1000)])
        x += w + rng.uniform(-6, 4)
    skm = shapes(W, H, sky, smooth=False)
    art = GP(art, skm, "#202023", "#25252a", seed=nx(), rough=0.8, streak=1.0)
    lit = []
    for (a, b, c, d) in sky:
        for _ in range(4):
            if rng.random() < 0.18:
                wx = rng.uniform(a[0] + 6, b[0] - 10); wy = rng.uniform(a[1] + 10, 980)
                lit.append([(wx, wy), (wx + 5, wy), (wx + 5, wy + 7), (wx, wy + 7)])
    art = GP(art, shapes(W, H, lit, smooth=False), "#8a8780", "#a19e97", seed=nx(), rough=0.4, streak=0.3)
    # haze band
    art = over(art, mist(W, H, [(960, 40, -40, W + 40, 0.35)], nx, rng, col="#5a5a5e", col2="#4a4a4e"))
    clear()
    # wet street: dark asphalt with long vertical reflections
    street = rect(W, H, -10, 1000, W + 10, H + 10)
    art = GP(art, street, "#121213", "#1a1a1b", seed=nx(), rough=1, streak=1.6)
    curb = strokes(W, H, [([(-10, 1004), (W + 10, 1010)], 6, None)])
    art = GP(art, curb, "#45454a", seed=nx(), rough=0.6, streak=0.4)
    # cobbles hint
    cob = []
    for r in range(18):
        y = 1030 + r * (14 + r * 1.6)
        x = rng.uniform(-20, 0)
        while x < W + 20:
            w = 26 + r * 3 + rng.uniform(-4, 4)
            cob.append(([(x + 2, y), (x + w - 2, y + rng.uniform(-1, 1))], 1.2 + r * 0.06, (0.3, 0.3)))
            x += w
    art = GP(art, strokes(W, H, cob) * street, "#2c2c2f", seed=nx(), rough=0.5, streak=0.4)
    # lamp: cast-iron post on the left, lantern head with a hot glow
    lx = 150
    post = np.maximum(rect(W, H, lx - 7, 620, lx + 7, 1060), poly(W, H, [(lx - 22, 1060), (lx + 22, 1060), (lx + 14, 1000), (lx - 14, 1000)]))
    post = np.maximum(post, poly(W, H, [(lx - 11, 720), (lx + 11, 720), (lx + 9, 760), (lx - 9, 760)]))
    post = np.maximum(post, poly(W, H, [(lx - 16, 618), (lx + 16, 618), (lx + 8, 640), (lx - 8, 640)]))
    arm = strokes(W, H, [(curve([(lx, 640), (lx + 34, 600), (lx + 74, 606), (lx + 90, 632)], 20), 5, None)])
    head = poly(W, H, [(lx - 32, 540), (lx + 32, 540), (lx + 22, 618), (lx - 22, 618)])
    cap = poly(W, H, [(lx - 42, 542), (lx + 42, 542), (lx + 6, 506), (lx, 494), (lx - 6, 506)])
    art = GP(art, np.maximum(np.maximum(post, arm), cap), "#0a0a0b", seed=nx(), rough=0.6, streak=0.4)
    art = GP(art, head, "#f4f1ea", "#e2ded5", seed=nx(), rough=0.5, streak=0.3)
    art = GP(art, strokes(W, H, [([(lx, 540), (lx, 618)], 3, None), ([(lx - 27, 578), (lx + 27, 578)], 2, None)]), "#3a3a3d", seed=nx(), rough=0.3, streak=0.3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    halo = np.clip(1 - np.hypot(xx - lx, (yy - 580) * 1.05) / 340, 0, 1) ** 1.7
    art = over(art, solid_layer(halo, "#ece8de", 0.7))
    # light cone down to the pavement
    cone = poly(W, H, [(lx - 22, 618), (lx + 22, 618), (lx + 280, 1300), (lx - 200, 1300)], smooth=False)
    cone = gaussian_filter(cone, 18) * (1 - ygrad(W, H, 640, 1320) * 0.7)
    art = over(art, solid_layer(cone, "#d8d4ca", 0.26))
    back = np.clip(1 - np.hypot(xx - 380, (yy - 900) * 1.3) / 260, 0, 1) ** 1.5
    art = over(art, solid_layer(back, "#8f8c86", 0.45))
    pool = np.clip(1 - np.hypot(xx - (lx + 60), (yy - 1150) * 3.2) / 300, 0, 1) ** 1.3
    art = over(art, solid_layer(pool * street, "#cfcac0", 0.4))
    clear()
    # the couple under the lamp light, sharing an umbrella
    mx, fy, s = 330, 1140, 290
    art, fig = paint_couple(art, W, H, mx, fy, s, nx, rim_from="left")
    # reflections: lamp, window, couple, smeared down into the wet street
    def reflect(mask, y_axis, strength, col):
        idx = np.clip((2 * y_axis - np.arange(H)).astype(int), 0, H - 1)
        r = mask[idx] * (np.arange(H)[:, None] > y_axis)
        r = gaussian_filter(r, (14, 2.5)) * (1 - ygrad(W, H, y_axis, y_axis + 420)) * strength
        return solid_layer(r, col)
    art = over(art, reflect(fig, fy + 2, 0.75, "#060607"))
    art = over(art, reflect(head, 1004, 0.8, "#e8e4da"))
    art = over(art, reflect(win, 1004, 0.35, "#bdb9b0"))
    streaks = []
    for _ in range(160):
        x = rng.uniform(-10, W + 10); y = rng.uniform(1020, H)
        streaks.append(([(x, y), (x + rng.uniform(-2, 2), y + rng.uniform(14, 40))], rng.uniform(1, 2.2), (0.3, 0.3)))
    art = over(art, solid_layer(strokes(W, H, streaks) * (0.25 + 0.75 * np.clip(pool * 2 + halo, 0, 1)), "#c9c5bb", 0.35))
    # puddle ripples in the light pool
    rip = []
    for _ in range(26):
        cx_, cy_ = rng.uniform(lx - 120, lx + 300), rng.uniform(1170, 1420)
        r = rng.uniform(6, 18)
        rip.append((arc_pts(cx_, cy_, r, 0, math.tau, 20, 0.28), 1.0, None))
    art = over(art, solid_layer(strokes(W, H, rip) * np.clip(pool * 1.6, 0, 1), "#d8d4ca", 0.5))
    clear()
    # rain: fine diagonal streaks, brighter in the lamp light
    rm = rain(W, H, rng, 900, L=(16, 46), ang=1.78, wd=(0.7, 1.4))
    art = over(art, solid_layer(rm * (0.18 + 0.82 * np.clip(halo * 1.6 + cone * 1.5, 0, 1)), "#e9e6de", 0.55))
    # venetian-blind shadow falling across the top of the frame (off-screen window)
    yy2 = yy - xx * 0.32
    bl = (np.sin(yy2 / 13.0 * math.pi) > 0.25).astype(np.float32)
    bl = gaussian_filter(bl, 2.5) * np.clip(1 - np.hypot(xx - 380, (yy - 120) * 1.2) / 520, 0, 1) ** 1.4
    art = over(art, solid_layer(bl, "#9a9892", 0.22))
    rgb = art[..., :3]
    g = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    rgb = np.clip(rgb * (1 + g[..., None] * 0.05), 0, 1)
    v = np.clip(1 - (np.hypot(xx / W - 0.5, ((yy - 140) / (H - 140) - 0.5) * 0.8) * 1.2) ** 2.2, 0.35, 1)
    rgb = rgb * v[..., None]
    lum = rgb.mean(-1, keepdims=True)
    rgb = lum * 0.92 + rgb * 0.08
    rgb = rgb[140:]
    prev_rgb(rgb, "fn-scene")
    save_rgb(rgb, f"{OUT}/scene.webp", quality=72)
    clear()


def part_couple():
    """The couple under the umbrella alone (transparent): closing and hero."""
    W, H = 520, 560
    nx = Seq(800)
    art = blank(W, H)
    art, fig = paint_couple(art, W, H, 210, 540, 400, nx, rim_from="right")
    prev_rgba(art, "fn-couple", bg="#d9d6cf")
    save_a(art, f"{OUT}/couple.webp", max_w=360)
    clear()


def part_blinds():
    """Venetian-blind light falling on a wall: soft-edged slats of light, fading out (white with alpha)."""
    W, H = 900, 900
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = (fbm(W, H, 4, 60, 2) - 0.5) * 6
    u = (yy - xx * 0.36 + n) / 34.0
    sl = np.clip((np.sin(u * math.pi) - 0.05) * 2.5, 0, 1)
    mull = np.clip(np.abs(((xx * 0.94 + yy * 0.34) - 470) / 9) - 1, 0, 1)
    fall = np.clip(1 - np.hypot(xx - 420, (yy - 380) * 1.15) / 470, 0, 1) ** 1.2
    a = gaussian_filter(sl * mull, 2.2) * fall
    dust = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), 0.8)
    a = a * (0.9 + 0.2 * dust)
    arr = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f2efe8"), np.float32), np.clip(a * 0.85, 0, 1)[..., None]], -1)
    prev_rgba(arr, "fn-blinds", bg="#151516")
    save_a(arr, f"{OUT}/blinds.webp", max_w=640, quality=70)


def part_glow():
    """Lamp glow with a few rain streaks caught in it (flicker layer)."""
    W = H = 400
    rng = random.Random(9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip(1 - np.hypot(xx - 200, yy - 200) / 200, 0, 1) ** 2.2
    rm = rain(W, H, rng, 120, L=(14, 34), ang=1.78, wd=(0.8, 1.4)) * g * 1.4
    a = np.clip(g * 0.85 + rm * 0.5, 0, 1)
    arr = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f1ede3"), np.float32), a[..., None]], -1)
    prev_rgba(arr, "fn-glow", bg="#151516")
    save_a(arr, f"{OUT}/glow.webp", max_w=260, quality=70)


def part_hat():
    """A fedora in brush ink with a pale band (divider, timeline node, sent)."""
    W, H = 300, 170
    nx = Seq(1300)
    art = blank(W, H)
    brim = []
    for k in range(41):
        t = k / 40
        x = 20 + 260 * t
        brim.append((x, 120 - 18 * (abs(2 * t - 1) ** 1.6) + 10 * math.sin(math.pi * t)))
    for k in range(41):
        t = 1 - k / 40
        x = 20 + 260 * t
        brim.append((x, 120 - 18 * (abs(2 * t - 1) ** 1.6) - 6 * math.sin(math.pi * t) - 4))
    crown = [(80, 112), (92, 52), (118, 34), (150, 40), (182, 34), (208, 52), (220, 112)]
    m = np.maximum(poly(W, H, brim, smooth=True), poly(W, H, crown, smooth=True))
    art = GP(art, m, INK, BLACK, seed=nx(), rough=1.2, streak=0.8)
    band = np.clip(poly(W, H, [(82, 90), (218, 90), (221, 108), (79, 108)], smooth=False) * m, 0, 1)
    art = GP(art, band, "#cfcbc2", "#e5e2da", seed=nx(), rough=0.6, streak=0.5)
    hi = np.clip(m - np.roll(np.roll(m, 3, 0), 3, 1), 0, 1) * (1 - ygrad(W, H, 40, 110))
    art = GP(art, hi, SMOKE, FOG, seed=nx(), rough=0.5, streak=0.5)
    prev_rgba(art, "fn-hat", bg="#efede7")
    save_a(art, f"{OUT}/hat.webp", max_w=150, quality=84)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
