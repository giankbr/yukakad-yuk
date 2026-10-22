"""Karang Laut — an underwater coral garden in watercolour: branching staghorn corals, a meandering brain coral, a lacy
purple sea fan, sea grass, a small school of reef fish, bubbles; blue water washes with light shafts and caustics.
Run: python3 -I karang-laut.py [part ...]
parts: water caustic reef fan brain fish branch bubble. Assets -> public/themes/art/karang-laut/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d4_lib import *

OUT = outdir("karang-laut")
PARTS = sys.argv[1:] or ["water", "caustic", "reef", "fan", "brain", "fish", "branch", "bubble"]
WATER_T, WATER_M, WATER_D = "#7cc9d0", "#2a86a6", "#0d3a63"
CORAL, PEACH, ROSE, SUN = "#e8735a", "#f2a986", "#cf5a7a", "#efc35a"
FAN, FAN_D = "#9a5aa6", "#6c3a86"
BRAIN, BRAIN_D = "#d9a65e", "#a8733a"
SEA, SEA_D = "#5fa88c", "#357a68"
NIGHT = "#14476e"


def under(art, m, col, a=0.9):
    """Pale opaque underpainting so the watercolour sits on 'paper' even over the blue page."""
    md = displace(m, 7, 2.0, 20)
    return OV(art, md, lambda mm: layer(np.clip(gaussian_filter(mm, 0.8) * 1.1, 0, 1), col, a))


def branch_items(x, y, ang, L, w, depth, rng, out):
    """Staghorn branching: tapering limbs that fork upward, rounded tips."""
    pts = [(x, y)]
    cx, cy, a = x, y, ang
    n = 6
    for i in range(n):
        a += rng.uniform(-0.18, 0.18)
        cx += math.cos(a) * L / n; cy += math.sin(a) * L / n
        pts.append((cx, cy))
    out.append((pts, w, (0.0, 0.0)))
    out.append(([(cx, cy), (cx + math.cos(a) * 1, cy + math.sin(a) * 1)], w * 0.8, None))
    if depth > 0:
        k = 2 if rng.random() < 0.75 else 3
        for j in range(k):
            na = a + (j - (k - 1) / 2) * rng.uniform(0.45, 0.7)
            branch_items(cx, cy, na, L * rng.uniform(0.62, 0.8), w * 0.74, depth - 1, rng, out)


def coral_tree(art, W, H, x, y, s, rng, nx, c1, c2, depth=3, spread=0.0):
    items = []
    for k in range(rng.randint(2, 3)):
        branch_items(x + rng.uniform(-8, 8) * s, y, -math.pi / 2 + (k - 1) * 0.5 + spread + rng.uniform(-.1, .1), 70 * s, 15 * s, depth, rng, items)
    m = strokes(W, H, items)
    art = under(art, m, mix(c1, "#fff4ea", 0.55))
    # polyps: tiny lighter dots along the limbs
    art = G(art, m, c1, c2, seed=nx(), density=0.82, edge=0.7, bloom=0.4, gran=0.3, rough=2.5, feather=1.0)
    shade = m * np.clip(gaussian_filter(np.roll(m, -4, 1), 2) * 1.2 - 0.2, 0, 1)
    art = G(art, shade * 0.8, mix(c2, "#5a2a3a", 0.35), seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=2, feather=1.2)
    pd = [(px + rng.uniform(-3, 3), py + rng.uniform(-3, 3), rng.uniform(1.2, 2.4) * s) for it in items for (px, py) in it[0][1::2]]
    art = G(art, circles(W, H, pd) * m, mix(c1, "#fff4e8", 0.55), seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8, feather=0.5, pad=8)
    return art


def brain_coral(art, W, H, cx, cy, rx, ry, rng, nx):
    dome = ellipses(W, H, [(cx, cy, rx, ry, rng.uniform(-4, 4))])
    dome *= np.clip(((cy + ry * 0.55) - np.mgrid[0:H, 0:W][0]) / 4, 0, 1)
    art = under(art, dome, "#f3dcb0", 0.95)
    art = G(art, dome, BRAIN, mix(BRAIN, PEACH, 0.4), seed=nx(), density=0.8, edge=0.7, bloom=0.35, gran=0.35, rough=3, feather=1.2)
    rn = np.random.default_rng(nx()).random((H, W)).astype(np.float32)
    dog = gaussian_filter(rn, 4.2) - gaussian_filter(rn, 8.4)
    dog /= dog.std() + 1e-6
    grooves = np.clip(1 - np.abs(dog) * 2.6, 0, 1) ** 1.3 * dome
    grooves *= np.clip(gaussian_filter(dome, 6) * 1.6 - 0.4, 0, 1)
    art = G(art, grooves, BRAIN_D, mix(BRAIN_D, "#6e3e28", 0.4), seed=nx(), density=0.6, edge=0.25, bloom=0.1, rough=1, feather=0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lit = dome * np.clip(1 - np.hypot((xx - cx + rx * 0.3) / rx, (yy - cy + ry * 0.5) / ry), 0, 1)
    art = OV(art, lit, lambda mm: layer(mm, "#fff1d6", 0.35))
    low = dome * np.clip((yy - cy) / ry + 0.2, 0, 1) ** 1.3
    art = G(art, low, "#8a5a3a", seed=nx(), density=0.45, edge=0, bloom=0.3, rough=2, feather=4)
    return art


def sea_fan(art, W, H, bx, by, s, rng, nx, c=FAN, cd=FAN_D):
    items = []
    tips = []
    def grow(x, y, a, L, w, d):
        pts = [(x, y)]
        cx, cy = x, y
        for i in range(5):
            a += rng.uniform(-0.12, 0.12)
            cx += math.cos(a) * L / 5; cy += math.sin(a) * L / 5
            pts.append((cx, cy))
        items.append((pts, w, (0.0, 0.5)))
        if d > 0:
            for sg in (-1, 1):
                grow(cx, cy, a + sg * rng.uniform(0.3, 0.55), L * rng.uniform(0.74, 0.88), w * 0.72, d - 1)
        else:
            tips.append((cx, cy))
    grow(bx, by, -math.pi / 2, 58 * s, 8 * s, 6)
    veins = strokes(W, H, items)
    # the lace: a fine mesh only inside the fan's envelope
    env = np.clip(gaussian_filter(veins, 9 * s) * 9, 0, 1)
    env = np.clip(gaussian_filter(env, 3) * 1.4 - 0.2, 0, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wob = (fbm(W, H, nx(), 20, 2) - 0.5) * 6
    sp = 7 * s
    mesh = np.maximum(np.clip(1 - np.abs(((xx + yy * 0.6 + wob) / sp) % 1 - 0.5) * 2 / 0.22, 0, 1), np.clip(1 - np.abs(((xx - yy * 0.6 - wob) / sp) % 1 - 0.5) * 2 / 0.22, 0, 1))
    lace = env * (mesh * 0.85 + 0.2)
    art = under(art, env, mix(c, "#fbeef2", 0.72), 0.5)
    art = G(art, lace, c, mix(c, ROSE, 0.35), seed=nx(), density=0.85, edge=0.3, bloom=0.4, gran=0.3, rough=1.5, feather=0.7)
    art = G(art, veins, cd, mix(cd, "#3a2048", 0.3), seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.2, feather=0.6)
    return art


def seagrass(art, W, H, x, y, h, rng, nx, n=5):
    bl = [blade_poly((x + rng.uniform(-10, 10), y), (x + rng.uniform(-60, 60), y - h * rng.uniform(0.6, 1)), rng.uniform(8, 13), rng.uniform(-1.2, 1.2)) for _ in range(n)]
    m = shapes(W, H, bl)
    return G(art, m, SEA, SEA_D, seed=nx(), density=0.7, edge=0.6, bloom=0.4, gran=0.2, rough=2, feather=0.9)


def anemone(art, W, H, x, y, r, rng, nx):
    items = []
    for k in range(16):
        a = -math.pi + k / 15 * math.pi + rng.uniform(-.08, .08)
        items.append((curve([(x, y), (x + math.cos(a) * r * 0.6, y + math.sin(a) * r * 0.7), (x + math.cos(a + 0.2) * r, y + math.sin(a) * r - r * 0.1)], 12), 4.5, (0.0, 0.4)))
    m = strokes(W, H, items)
    art = G(art, m, "#f39b8c", ROSE, seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=1.5, feather=0.7)
    return G(art, ellipses(W, H, [(x, y + 4, r * 0.4, r * 0.22, 0)]), "#b8486a", seed=nx(), density=0.7, edge=0.5, rough=1.5, feather=0.7)


def fish_poly(x, y, L, d=1):
    pts = [(0, 0), (0.18, -0.2), (0.45, -0.27), (0.7, -0.18), (0.82, -0.04), (1.0, -0.26), (0.97, 0.0), (1.0, 0.26), (0.82, 0.04), (0.7, 0.18), (0.45, 0.25), (0.18, 0.18)]
    return [(x + u * L * d, y + v * L) for u, v in pts]


if "water" in PARTS:
    W, H = 640, 1200
    sky = painted_sky(W, H, [(0, "#9fdbdc"), (0.22, WATER_T), (0.55, WATER_M), (0.85, "#185c86"), (1, WATER_D)], seed=3, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # light shafts fanning from above the surface
    ang = np.arctan2(xx - W * 0.62, yy + H * 0.35)
    rays = np.zeros((H, W), np.float32)
    rr = random.Random(4)
    for k in range(9):
        a0 = rr.uniform(-0.5, 0.45); wd = rr.uniform(0.015, 0.05)
        rays += np.exp(-((ang - a0) / wd) ** 2) * rr.uniform(0.25, 0.6)
    rays *= np.clip(1 - yy / (H * 0.85), 0, 1) ** 1.4 * (0.7 + 0.3 * fbm(W, H, 5, 80, 2))
    sky[..., :3] = sky[..., :3] * (1 - rays[..., None] * 0.4) + np.array(hex_rgb("#e9fbf6"), np.float32) * rays[..., None] * 0.4
    # caustic net near the surface
    n1 = fbm(W, H, 6, 34, 3); n2 = fbm(W, H, 7, 26, 3)
    cau = np.clip(1 - np.abs(n1 - n2) * 14, 0, 1) ** 2 * np.clip(1 - yy / (H * 0.4), 0, 1)
    sky[..., :3] = sky[..., :3] * (1 - cau[..., None] * 0.45) + cau[..., None] * 0.45
    # watercolour blooms in the deep
    bl = blank(W, H)
    bl = G(bl, np.clip(fbm(W, H, 8, 120, 3) * 1.6 - 0.55, 0, 1) * np.clip(yy / H, 0, 1), NIGHT, seed=9, density=0.35, edge=0.4, bloom=0.5, rough=6, feather=4)
    out = over(sky, bl)
    out = add_grain(out, 10, 0.025)
    save_rgb(out, f"{OUT}/water.webp", size=(400, 750), quality=72)
    preview(out, "kl-water")
    clear()

if "caustic" in PARTS:
    n = 384
    a1 = wrap_noise(n, n, 11, 18); a2 = wrap_noise(n, n, 12, 13)
    c = np.clip(1 - np.abs(a1 - a2) * 16, 0, 1) ** 2
    c = c * (0.6 + 0.4 * wrap_noise(n, n, 13, 40))
    save_full(rgba(np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#effffb"), np.float32), c * 0.85), f"{OUT}/caustic.webp", quality=70)
    clear()

if "reef" in PARTS:
    W, H = 900, 520
    rng = random.Random(21); nx = Seq(21000)
    art = blank(W, H)
    # distant reef silhouettes (cool, low contrast)
    far = shapes(W, H, [[(0, H)] + [(x, H - 150 - 40 * math.sin(x / 70) - rng.uniform(0, 30)) for x in range(0, W + 60, 60)] + [(W, H)]])
    art = G(art, far, "#3f8fa6", "#2f7894", seed=nx(), density=0.5, edge=0.5, bloom=0.5, rough=6, feather=2)
    art = seagrass(art, W, H, 90, H - 10, 300, rng, nx, 6)
    art = seagrass(art, W, H, 820, H - 10, 260, rng, nx, 5)
    art = sea_fan(art, W, H, 170, H - 60, 1.15, rng, nx)
    art = coral_tree(art, W, H, 360, H - 40, 1.25, rng, nx, CORAL, ROSE, depth=3)
    art = brain_coral(art, W, H, 560, H - 70, 120, 78, rng, nx)
    art = coral_tree(art, W, H, 740, H - 40, 1.05, rng, nx, SUN, mix(SUN, CORAL, 0.5), depth=3, spread=0.15)
    art = anemone(art, W, H, 455, H - 34, 44, rng, nx)
    art = anemone(art, W, H, 870, H - 30, 36, rng, nx)
    # sandy floor wash
    floor = shapes(W, H, [[(0, H)] + [(x, H - 26 - 10 * math.sin(x / 50)) for x in range(0, W + 50, 50)] + [(W, H)]])
    art = G(art, floor, "#e9d6a8", "#d1b98a", seed=nx(), density=0.75, edge=0.5, bloom=0.4, gran=0.5, rough=4, feather=1.5)
    preview(art, "kl-reef", bg="#2a86a6")
    save(art, f"{OUT}/reef.webp", max_w=560, quality=78)
    clear()

if "fan" in PARTS:
    W, H = 420, 640
    rng = random.Random(31); nx = Seq(31000)
    art = blank(W, H)
    art = sea_fan(art, W, H, 210, 630, 1.45, rng, nx, c="#b06aa8", cd="#7a3f84")
    preview(art, "kl-fan", bg="#2a86a6")
    save(art, f"{OUT}/fan.webp", max_w=230, quality=78)
    clear()

if "brain" in PARTS:
    W, H = 360, 260
    rng = random.Random(41); nx = Seq(41000)
    art = blank(W, H)
    art = brain_coral(art, W, H, 180, 150, 140, 92, rng, nx)
    preview(art, "kl-brain", bg="#2a86a6")
    save(art, f"{OUT}/brain.webp", max_w=150, quality=80)
    clear()

if "fish" in PARTS:
    W, H = 520, 260
    rng = random.Random(51); nx = Seq(51000)
    art = blank(W, H)
    for (x, y, L) in [(60, 90, 120), (230, 150, 96), (330, 60, 84)]:
        body = shapes(W, H, [fish_poly(x, y, L)])
        art = under(art, body, "#fde7b0", 0.95)
        art = G(art, body, SUN, "#f0a94a", seed=nx(), density=0.85, edge=0.7, bloom=0.35, gran=0.25, rough=1.6, feather=0.8, pad=10)
        # vertical stripes (white bands with dark edges) like a reef damselfish
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        u = (xx - x) / L
        band = (np.clip(1 - np.abs(u - 0.3) / 0.05, 0, 1) + np.clip(1 - np.abs(u - 0.55) / 0.045, 0, 1)) * body
        art = OV(art, band, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fffaf0"), np.float32), m * 0.9), pad=6)
        edgeb = np.clip(gaussian_filter(band, 2) - band, 0, 1) * body * 2
        art = G(art, edgeb, "#3a3a52", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.8, feather=0.4, pad=6)
        tail = shapes(W, H, [[(x + L * 0.82, y), (x + L, y - L * 0.26), (x + L * 0.97, y), (x + L, y + L * 0.26)]]) * body
        art = G(art, tail, "#3a3a52", seed=nx(), density=0.5, edge=0.4, bloom=0.2, rough=1, feather=0.6, pad=6)
        eye = circles(W, H, [(x + L * 0.14, y - L * 0.03, L * 0.035)])
        art = G(art, eye, "#1d1d2a", seed=nx(), density=0.9, edge=0.2, rough=0.4, feather=0.4, pad=6)
    preview(art, "kl-fish", bg="#2a86a6")
    save(art, f"{OUT}/fish.webp", max_w=220, quality=80)
    clear()

if "branch" in PARTS:
    W, H = 620, 170
    rng = random.Random(61); nx = Seq(61000)
    art = blank(W, H)
    items = []
    branch_items(310, 165, -math.pi / 2 - 0.9, 70, 10, 3, rng, items)
    branch_items(310, 165, -math.pi / 2 + 0.9, 70, 10, 3, rng, items)
    branch_items(310, 165, -math.pi / 2, 40, 9, 2, rng, items)
    m = strokes(W, H, items)
    art = under(art, m, "#fbe0d6")
    art = G(art, m, CORAL, ROSE, seed=nx(), density=0.8, edge=0.7, bloom=0.4, gran=0.3, rough=2, feather=0.9)
    art = G(art, circles(W, H, [(150, 80, 9), (130, 54, 5), (480, 60, 6)]), "#cfeff0", seed=nx(), density=0.5, edge=0.9, bloom=0.2, rough=0.8, feather=0.5)
    preview(art, "kl-branch", tone="#eaf6f4")
    save(art, f"{OUT}/branch.webp", max_w=300, quality=80)
    clear()

if "bubble" in PARTS:
    W = H = 96
    ring = np.clip(1 - np.abs(np.hypot(*(np.mgrid[0:H, 0:W].astype(np.float32) - 48)) - 40) / 4, 0, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    inner = np.clip(1 - np.hypot(xx - 48, yy - 48) / 42, 0, 1) * 0.18
    hi = np.clip(1 - np.hypot(xx - 34, yy - 32) / 10, 0, 1) ** 1.5
    a = np.clip(ring * (0.55 + 0.45 * np.clip((xx + yy) / 140, 0, 1)) + inner + hi * 0.9, 0, 1)
    a = gaussian_filter(a, 0.8) * (0.88 + 0.12 * fbm(W, H, 71, 10, 2))
    save_full(rgba(np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f2fffd"), np.float32), a), f"{OUT}/bubble.webp", quality=80)
    clear()
