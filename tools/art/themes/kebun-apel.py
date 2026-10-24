"""Kebun Apel — a playful gouache orchard in the Batu highlands: rows of apple trees heavy with red fruit, a wooden
ladder leaning into a tree, bamboo baskets full of apples, and the blue twin-peaked mountains behind (Arjuno-like).
Run: python3 -I kebun-apel.py [part ...]   parts: kebun apel keranjang dahan garis"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t6_lib import *

OUT = outdir("kebun-apel")
PARTS = sys.argv[1:] or ["kebun", "apel", "keranjang", "dahan", "garis"]
CREAM = "#fbf1dc"
REDS = [("#d8342c", "#a81d22"), ("#e2452f", "#b4262a"), ("#c92a33", "#8f1a22")]
WOOD = ("#b07a45", "#8a5a30")


def tree(art, W, H, x, by, s, rng, nx, apples=14, area=None):
    trunk = [(x, by), (x - s * 0.04, by - s * 0.35), (x + s * 0.02, by - s * 0.6)]
    items = [(curve(trunk, 20), s * 0.11, (0.0, 0.6))]
    for d in (-1, 1):
        items.append((curve([(x, by - s * 0.42), (x + d * s * 0.22, by - s * 0.62), (x + d * s * 0.34, by - s * 0.78)], 16), s * 0.05, (0.0, 0.7)))
    tm = strokes(W, H, items)
    art = GP(art, tm, "#7a4e2c", "#5a3820", seed=nx(), rough=1.4, streak=0.8)
    cm = np.zeros((H, W), np.float32)
    art = dab_canopy(art, W, H, x, by - s * 0.88, s * 0.62, s * 0.42, rng, nx, dabs=int(160 + s * 0.4), area=cm)
    if area is not None:
        np.maximum(area, cm, out=area)
    for k in range(apples):
        a = rng.uniform(0, math.tau); d = rng.random() ** 0.5
        ax, ay = x + math.cos(a) * s * 0.5 * d, by - s * 0.85 + math.sin(a) * s * 0.36 * d
        art = apple(art, W, H, ax, ay, s * rng.uniform(0.045, 0.06), rng, nx, red=rng.choice(REDS), leaf=rng.random() < 0.3)
    return art


def basket(art, W, H, cx, by, w, rng, nx, n=18, area=None):
    """Woven bamboo basket brimming with apples."""
    h = w * 0.55
    # apples heap first (behind the rim)
    for k in range(n):
        t = k / max(1, n - 1)
        ax = cx + rng.uniform(-0.42, 0.42) * w
        ay = by - h + rng.uniform(-0.22, 0.04) * w * (1 - abs(ax - cx) / w)
        art = apple(art, W, H, ax, ay, w * rng.uniform(0.1, 0.13), rng, nx, red=rng.choice(REDS), leaf=rng.random() < 0.25)
    body = [(cx - w * 0.5, by - h), (cx + w * 0.5, by - h), (cx + w * 0.4, by), (cx - w * 0.4, by)]
    m = shape_mask(W, H, body, smooth=False)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, "#c99a5b", "#a87a40", seed=nx(), rough=1.2, streak=0.6)
    yy, xx = yx(W, H)
    weave = (np.sin((yy - by) / (h / 6) * math.pi) > 0) ^ (np.sin((xx - cx) / (w / 14) * math.pi) > 0)
    art = OV(art, weave.astype(np.float32) * m, lambda mm: rgba("#8d6332", mm * 0.45))
    rows = strokes(W, H, [([(cx - w * (0.5 - 0.1 * j / 6), by - h + h * j / 6), (cx + w * (0.5 - 0.1 * j / 6), by - h + h * j / 6)], max(1, w * 0.012), None) for j in range(1, 6)]) * m
    art = OV(art, rows, lambda mm: rgba("#6e4a24", mm * 0.5))
    rim = strokes(W, H, [([(cx - w * 0.53, by - h), (cx + w * 0.53, by - h)], w * 0.06, (0.05, 0.05))])
    art = GP(art, rim, "#b3824a", "#8a5f30", seed=nx(), rough=0.8, streak=0.6)
    sh = soft(np.clip(m - shape_mask(W, H, [(cx - w * 0.2, by - h), (cx + w * 0.5, by - h), (cx + w * 0.4, by), (cx - w * 0.1, by)], smooth=False), 0, 1), 3)
    art = OV(art, sh * m, lambda mm: rgba("#e8c58e", mm * 0.25))
    return art


def ladder(art, W, H, x0, y0, x1, y1, wd, nx):
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy); nxv, nyv = -dy / L, dx / L
    rails = [([(x0 + nxv * wd / 2, y0 + nyv * wd / 2), (x1 + nxv * wd / 2, y1 + nyv * wd / 2)], wd * 0.14, None),
             ([(x0 - nxv * wd / 2, y0 - nyv * wd / 2), (x1 - nxv * wd / 2, y1 - nyv * wd / 2)], wd * 0.14, None)]
    rungs = []
    for k in range(1, int(L / (wd * 0.9))):
        t = k * wd * 0.9 / L
        px, py = x0 + dx * t, y0 + dy * t
        rungs.append(([(px + nxv * wd / 2, py + nyv * wd / 2), (px - nxv * wd / 2, py - nyv * wd / 2)], wd * 0.1, None))
    art = GP(art, strokes(W, H, rungs), "#a8733f", "#8a5a30", seed=nx(), rough=0.6, streak=0.5)
    art = GP(art, strokes(W, H, rails), "#c08850", "#94622f", seed=nx(), rough=0.6, streak=0.8)
    return art


if "kebun" in PARTS:
    W, H = 860, 1560
    rng = random.Random(12); nx = Seq(1200)
    sky = painted_sky(W, H, [(0, "#8fc6d9"), (0.35, "#bfe0e3"), (0.5, "#f3ecd2"), (1, "#f3ecd2")], seed=5, streak=0.35)
    art = sky
    # clouds
    for (x, y, rx) in [(160, 210, 120), (650, 330, 150), (420, 120, 90)]:
        cm = ellipses(W, H, [(x + rng.uniform(-.6, .6) * rx, y + rng.uniform(-.2, .2) * rx, rx * rng.uniform(.35, .6), rx * rng.uniform(.25, .35), 0) for _ in range(6)])
        art = GP(art, cm, "#fdfaf0", "#f1ece0", seed=nx(), rough=3, streak=0.5)
    # mountains: far twin peaks (Arjuno-Welirang-like), then nearer hills
    HZ = 800
    pk0 = [(-20, HZ + 40), (60, HZ - 60), (190, HZ - 170), (300, HZ - 300), (340, HZ - 330), (372, HZ - 312), (430, HZ - 250), (520, HZ - 280),
          (580, HZ - 350), (612, HZ - 362), (650, HZ - 330), (760, HZ - 200), (880, HZ - 120), (880, HZ + 40)]
    pk = [(x, HZ - (HZ - y) * 0.68) for x, y in pk0]
    m1 = shape_mask(W, H, pk)
    art = GP(art, m1, "#7d9fc0", "#6a8db2", seed=nx(), rough=3, streak=0.8)
    yy, xx = yx(W, H)
    ridges = strokes(W, H, [([(p[0], p[1] + 6), (p[0] + rng.uniform(-40, 40), p[1] + 140)], 10, (0.1, 0.6)) for p in pk[2:12]])
    art = OV(art, soft(ridges, 4) * m1, lambda mm: rgba("#5d7ea3", mm * 0.5))
    art = OV(art, np.clip((yy - (HZ - 120)) / 160, 0, 1) * m1, lambda mm: rgba("#e8eee8", mm * 0.45))
    m2 = ridge_mask(W, H, HZ, 60, 8, freq=1.4, sharp=0.9)
    art = GP(art, m2, "#8fb46a", "#6f9b52", seed=nx(), rough=3, streak=1.0)
    # distant tree rows (dots)
    dots = []
    for row in range(4):
        yb = HZ + 40 + row * 46
        for k in range(int(W / (40 - row * 6)) + 2):
            dots.append((k * (40 - row * 6) + rng.uniform(-6, 6) + row * 13, yb + rng.uniform(-4, 4), 12 + row * 5, 10 + row * 4, 0))
    dm = ellipses(W, H, dots)
    art = GP(art, dm, "#4f8a3a", "#3b7231", seed=nx(), rough=1.4, streak=0.4)
    rd = circles(W, H, [(d[0] + rng.uniform(-6, 6), d[1] + rng.uniform(-4, 4), 2.2 + 0.6 * (d[1] - HZ) / 60) for d in dots for _ in range(2)])
    art = OV(art, rd * dm, lambda mm: rgba("#d8342c", mm * 0.9))
    # meadow
    gm = ridge_mask(W, H, HZ + 230, 30, 19, freq=1.2, sharp=1.0)
    art = GP(art, gm, "#9cc45f", "#7aa94a", seed=nx(), rough=2, streak=1.2)
    # grass tufts
    tufts = []
    for k in range(220):
        x = rng.uniform(0, W); y = rng.uniform(HZ + 250, H)
        L = rng.uniform(10, 26)
        tufts.append(([(x, y), (x + rng.uniform(-5, 5), y - L)], 3, (0.0, 0.8)))
    art = OV(art, strokes(W, H, tufts) * gm, lambda mm: rgba("#5f9440", mm * 0.6))
    # main trees: two sides framing the centre, with ladder and baskets
    art = tree(art, W, H, 130, 1330, 420, rng, nx, apples=22)
    clear()
    art = tree(art, W, H, 760, 1250, 360, rng, nx, apples=18)
    clear()
    art = ladder(art, W, H, 300, 1420, 205, 1000, 70, nx)
    art = basket(art, W, H, 470, 1440, 200, rng, nx, n=16)
    clear()
    art = basket(art, W, H, 650, 1470, 150, rng, nx, n=11)
    # fallen apples
    for (x, y, r) in [(360, 1470, 14), (560, 1500, 12), (790, 1440, 13), (80, 1480, 14)]:
        art = apple(art, W, H, x, y, r, rng, nx, red=rng.choice(REDS), leaf=False, ang=rng.uniform(-1, 1))
    prev(art, "apel-kebun", bg="#ffffff")
    save_rgb(art, f"{OUT}/kebun.webp", size=(860, 1560), quality=74)
    clear()

if "apel" in PARTS:
    W, H = 300, 320
    rng = random.Random(3); nx = Seq(300)
    a = apple(blank(W, H), W, H, 150, 180, 110, rng, nx)
    prev(a, "apel-apel", tone=CREAM)
    save(a, f"{OUT}/apel.webp", max_w=180, quality=84)

if "keranjang" in PARTS:
    W, H = 640, 520
    rng = random.Random(8); nx = Seq(800)
    a = basket(blank(W, H), W, H, 320, 480, 440, rng, nx, n=20)
    prev(a, "apel-keranjang", tone=CREAM)
    save(a, f"{OUT}/keranjang.webp", max_w=400, quality=82)
    clear()

if "dahan" in PARTS:
    W, H = 900, 380
    rng = random.Random(15); nx = Seq(1500)
    a = blank(W, H)
    br = curve([(-10, 70), (220, 110), (480, 90), (700, 140), (910, 110)], 60)
    a = GP(a, strokes(W, H, [(br, 16, (0.0, 0.6))]), "#7a4e2c", "#5a3820", seed=nx(), rough=1.2, streak=0.6)
    for k in range(22):
        p = br[min(len(br) - 1, int(3 + k * 2.6))]
        ang = rng.choice((-1, 1)) * rng.uniform(0.4, 1.2) + (math.pi / 2 if rng.random() < 0.6 else -math.pi / 2) * 0
        ang = rng.uniform(0.3, 2.8) if k % 3 else rng.uniform(-2.6, -0.5)
        L = rng.uniform(70, 110)
        lm = shape_mask(W, H, leaf_outline(p[0], p[1], L, ang, 0.46, 16, 0.03))
        a = GP(a, lm, rng.choice(["#6aa140", "#4f8a3a", "#7bb04a"]), "#3f7a2e", seed=nx(), rough=0.8, streak=0.4)
        a = OV(a, strokes(W, H, [([(p[0], p[1]), (p[0] + math.cos(ang) * L * .85, p[1] + math.sin(ang) * L * .85)], 2, (0.1, 0.5))]) * lm, lambda mm: rgba("#d8eaa8", mm * .6))
        trim_cache()
    for (x, y, r) in [(170, 200, 46), (250, 230, 40), (520, 190, 50), (600, 240, 42), (780, 230, 46)]:
        a = GP(a, strokes(W, H, [([(x, y - r * 0.8), (x - 4, y - r * 1.9)], 4, None)]), "#5a3a22", seed=nx(), rough=0.4, streak=0.2)
        a = apple(a, W, H, x, y, r, rng, nx, red=rng.choice(REDS), leaf=False)
    prev(a, "apel-dahan", tone=CREAM)
    save(a, f"{OUT}/dahan.webp", max_w=640, quality=82)
    clear()

if "garis" in PARTS:
    W, H = 700, 150
    rng = random.Random(21); nx = Seq(2100)
    a = blank(W, H)
    cx, cy = W / 2, 70
    a = GP(a, strokes(W, H, [(curve([(60, cy + 10), (200, cy), (cx, cy - 6), (500, cy), (640, cy + 10)], 40), 5, (0.1, 0.1))]), "#7a4e2c", seed=nx(), rough=0.6, streak=0.4)
    for side in (-1, 1):
        for (d, L, ang) in [(70, 70, -0.9), (170, 60, 0.7), (250, 48, -0.8)]:
            x = cx + side * d
            aa = ang if side > 0 else math.pi - ang
            lm = shape_mask(W, H, leaf_outline(x, cy - 3, L, aa, 0.46, 16))
            a = GP(a, lm, "#6aa140", "#3f7a2e", seed=nx(), rough=0.6, streak=0.3)
    a = apple(a, W, H, cx - 26, cy + 30, 30, rng, nx, red=REDS[0], leaf=False)
    a = apple(a, W, H, cx + 26, cy + 34, 27, rng, nx, red=REDS[2], leaf=False)
    prev(a, "apel-garis", tone=CREAM)
    save(a, f"{OUT}/garis.webp", max_w=350, quality=84)
