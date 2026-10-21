"""Baby Shower Awan — pastel watercolour: a striped hot-air balloon (mint/peach/lilac) with a wicker basket, puffy clouds,
a pale crescent moon, little stars, a wet-in-wet sky wash and a watercolour paper tile.
Run: python3 -I baby-shower-awan.py [part ...]  parts: balloon cloud moon stars divider sky paper
Assets -> public/themes/art/baby-shower-awan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *

OUT = outdir("baby-shower-awan")
PARTS = sys.argv[1:] or ["balloon", "cloud", "moon", "stars", "star", "divider", "sky", "paper"]
MINT, MINT_D = "#a8dcc8", "#6fb9a0"
PEACH, PEACH_D = "#f8c4a4", "#e99a7a"
LILAC, LILAC_D = "#cdbbe6", "#9f88c8"
BUTTER = "#f7dc8e"
SHADOW = "#8f86b8"


def star_pts(cx, cy, r, rot=-math.pi / 2, inner=0.48):
    return [(cx + math.cos(rot + k * math.pi / 5) * (r if k % 2 == 0 else r * inner), cy + math.sin(rot + k * math.pi / 5) * (r if k % 2 == 0 else r * inner)) for k in range(10)]


def cloud_mask(W, H, cx, cy, w, h, rng, n=7):
    items = []
    for k in range(n):
        t = k / (n - 1)
        x = cx - w / 2 + t * w + rng.uniform(-w, w) * 0.03
        r = h * (0.3 + 0.42 * math.sin(math.pi * t) ** 1.2) * rng.uniform(0.8, 1.15)
        items.append((x, cy - r * 0.45, r))
    for k in range(max(2, n // 2 - 1)):  # top puffs
        t = (k + 0.5) / max(2, n // 2 - 1)
        x = cx - w * 0.28 + t * w * 0.56
        r = h * rng.uniform(0.36, 0.5)
        items.append((x, cy - h * 0.48 - r * 0.2, r))
    m = circles(W, H, items)
    base = shapes(W, H, [[(cx - w / 2 + h * 0.05, cy - h * 0.1), (cx + w / 2 - h * 0.05, cy - h * 0.1), (cx + w / 2 - h * 0.1, cy + h * 0.3), (cx - w / 2 + h * 0.1, cy + h * 0.3)]])
    m = np.clip(m + base, 0, 1)
    # flat-ish bottom
    yy = np.arange(H, dtype=np.float32)[:, None]
    m *= np.clip((cy + h * 0.34 - yy) / 6, 0, 1)
    return m


def paint_cloud(art, m, nx):
    def white(mm):
        p_ = pigment(mm, "#ffffff", "#fbf7ff", seed=nx(), density=0.95, edge=0.2, bloom=0.25, rough=6, feather=2.0, gran=0.05)
        p_[..., :3] = 0.25 * p_[..., :3] + 0.75 * np.array(hex_rgb("#fffdfb"), np.float32)
        p_[..., 3] = np.clip(p_[..., 3] * 1.1, 0, 1)
        return p_
    art = OV(art, m, white, pad=24)
    under = side_light(m, 0, -22, 14)
    art = G(art, under, "#c9c0e6", "#b8d8e6", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=5, feather=2.5)
    art = G(art, side_light(m, 0, -9, 5) * 0.6, SHADOW, seed=nx(), density=0.3, edge=0.4, bloom=0.2, rough=3, feather=1.5)
    return art


if "balloon" in PARTS:
    W, H = 520, 720
    nx = Seq(30100); rng = random.Random(3)
    cx, cy, R = 260, 250, 200

    def env_x(y):
        """half-width of the envelope at height y (round top, tapering throat)."""
        if y < cy:
            return math.sqrt(max(0, R * R - (y - cy) ** 2))
        t = min(1.0, (y - cy) / (R * 1.25))
        return max(0, R * (1 - t) ** 1.25 * (1 - 0.1 * t)) + 34 * t ** 3
    ys = list(range(int(cy - R), int(cy + R * 1.25) + 1, 4))
    outline_pts = [(cx + env_x(y), y) for y in ys] + [(cx - env_x(y), y) for y in reversed(ys)]
    env = shapes(W, H, [outline_pts], smooth=False)
    env = gaussian_filter(env, 0.8)
    art = blank(W, H)
    # gores: 7 vertical stripes following the curvature
    cols = [(MINT, MINT_D), (PEACH, PEACH_D), (LILAC, LILAC_D), (MINT, MINT_D), (PEACH, PEACH_D), (LILAC, LILAC_D), (MINT, MINT_D)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    half = np.array([env_x(y) for y in range(H)], np.float32)[:, None]
    u = np.clip((xx - cx) / np.maximum(half, 1), -1, 1)  # -1..1 across
    lon = np.arcsin(u) / (math.pi / 2)  # spherical-ish longitude
    for k, (a, b) in enumerate(cols):
        lo, hi = -1 + 2 * k / 7, -1 + 2 * (k + 1) / 7
        g = env * np.clip((lon - lo) * 60, 0, 1) * np.clip((hi - lon) * 60, 0, 1)
        art = G(art, g, a, mix(a, b, 0.3), seed=nx(), density=0.8, edge=0.5, bloom=0.4, rough=2.2, feather=1.0, gran=0.15)
    # form shading (light from upper left)
    shade = np.clip((lon + 0.1) * 0.9, 0, 1) ** 1.6 * env
    shade = shade * (0.6 + 0.4 * np.clip((yy - cy + 120) / 300, 0, 1))
    art = G(art, shade * 0.85, SHADOW, seed=nx(), density=0.38, edge=0.15, bloom=0.3, rough=3, feather=3)
    hl = np.clip(1 - np.sqrt(((xx - (cx - 80)) / 60) ** 2 + ((yy - (cy - 90)) / 90) ** 2), 0, 1) * env
    art = OV(art, hl, lambda m: col_arr(m, "#ffffff", np.clip(m * 1.2, 0, 1) * 0.45), pad=4)
    # seams: thin watercolour pencil lines between gores
    seams = []
    for k in range(1, 7):
        l = -1 + 2 * k / 7
        pts = [(cx + math.sin(l * math.pi / 2) * env_x(y), y) for y in range(int(cy - R) + 6, int(cy + R * 1.2), 6)]
        seams.append((pts, 1.6, (0.05, 0.1)))
    art = G(art, strokes(W, H, seams) * env, "#7a6aa0", seed=nx(), density=0.42, edge=0.2, bloom=0, rough=1, feather=0.6)
    # scalloped skirt band
    yb = int(cy + R * 1.06)
    band = np.clip(env * np.clip((yy - yb) * 0.5, 0, 1) * np.clip((yb + 22 - yy) * 0.5, 0, 1), 0, 1)
    sc = circles(W, H, [(cx + x, yb + 22, 11) for x in range(-int(env_x(yb + 22)) + 10, int(env_x(yb + 22)) - 4, 22)])
    art = G(art, np.clip(band + sc * (yy > yb + 18), 0, 1), "#f4d9a8", BUTTER, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.6, feather=0.8)
    # ropes + basket
    throat = int(cy + R * 1.25)
    tw = env_x(throat)
    by0, by1 = throat + 92, throat + 150
    ropes = [([(cx - tw + 2, throat - 4), (cx - 44, by0)], 2.2, None), ([(cx + tw - 2, throat - 4), (cx + 44, by0)], 2.2, None),
             ([(cx - tw * 0.35, throat), (cx - 16, by0)], 1.8, None), ([(cx + tw * 0.35, throat), (cx + 16, by0)], 1.8, None)]
    art = G(art, strokes(W, H, ropes), "#8a6a4e", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    basket = shapes(W, H, [[(cx - 52, by0), (cx + 52, by0), (cx + 44, by1), (cx - 44, by1)]])
    art = G(art, basket, "#e2b98a", "#c9935e", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.5, feather=0.8, gran=0.3)
    weave = strokes(W, H, [([(cx - 52, y), (cx + 52, y)], 1.6, None) for y in range(by0 + 12, by1, 12)] +
                    [([(cx + x, by0), (cx + x * 0.85, by1)], 1.4, None) for x in range(-40, 41, 16)]) * basket
    art = G(art, weave, "#9a6a40", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    rimm = strokes(W, H, [([(cx - 58, by0), (cx + 58, by0)], 9, None)])
    art = G(art, rimm, "#c9935e", "#a8754a", seed=nx(), density=0.95, edge=0.6, bloom=0, rough=1, feather=0.6)
    # tiny bunting between ropes
    flags = [[(cx - 40 + i * 20, by0 - 26), (cx - 30 + i * 20, by0 - 26), (cx - 35 + i * 20, by0 - 12)] for i in range(5)]
    for i, f in enumerate(flags):
        c = [MINT_D, PEACH_D, LILAC_D, BUTTER, MINT_D][i]
        art = G(art, shapes(W, H, [f], smooth=False), c, seed=nx(), density=0.8, edge=0.5, bloom=0, rough=1, feather=0.6)
    art = G(art, strokes(W, H, [(curve([(cx - 44, by0 - 28), (cx, by0 - 22), (cx + 44, by0 - 28)], 20), 1.2, None)]), "#8a6a4e", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.4)
    preview(art, "bs-balloon", tone="#fbf3ee")
    save(art, f"{OUT}/balloon.webp", max_w=340, quality=82)
    clear()

if "cloud" in PARTS:
    for name, (W, H, w, h, sd) in {"cloud": (640, 340, 440, 150, 5), "cloud2": (480, 260, 310, 104, 9)}.items():
        nx = Seq(30200 + sd); rng = random.Random(sd)
        m = cloud_mask(W, H, W / 2, H * 0.72, w, h, rng)
        art = paint_cloud(blank(W, H), m, nx)
        preview(art, f"bs-{name}", bg="#d8cfee")
        save(art, f"{OUT}/{name}.webp", max_w=W // 2 + 40, quality=80)
        clear()

if "moon" in PARTS:
    W, H = 320, 320
    nx = Seq(30300)
    full = circles(W, H, [(160, 160, 96)])
    cut = circles(W, H, [(206, 126, 90)])
    m = np.clip(full - cut, 0, 1)
    art = OV(blank(W, H), m, lambda mm: col_arr(mm, "#fff3c4", np.clip(gaussian_filter(mm, 16) * 1.3, 0, 1) * 0.5), pad=60)
    art = G(art, m, "#fae7a6", BUTTER, seed=nx(), density=0.9, edge=0.6, bloom=0.45, rough=3, feather=1.4, gran=0.2)
    art = G(art, side_light(m, 10, -6, 6) * m, "#e8b98a", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=2, feather=1.5)
    preview(art, "bs-moon", tone="#d9d2ee")
    save(art, f"{OUT}/moon.webp", max_w=170, quality=82)
    clear()

if "stars" in PARTS:
    W, H = 420, 260
    nx = Seq(30400); rng = random.Random(21)
    art = blank(W, H)
    for (x, y, r, c) in [(60, 80, 30, BUTTER), (180, 46, 18, PEACH_D), (260, 150, 36, BUTTER), (360, 70, 22, LILAC_D), (120, 190, 16, MINT_D), (370, 200, 14, PEACH_D), (30, 210, 10, LILAC_D)]:
        m = shapes(W, H, [deform(star_pts(x, y, r, rng.uniform(-1.8, -1.3)), rng, 1, 0.03)])
        art = G(art, m, c, mix(c, "#ffffff", 0.3), seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.8, feather=1.0, gran=0.2)
    dots_ = circles(W, H, [(rng.uniform(10, W - 10), rng.uniform(10, H - 10), rng.uniform(2, 4)) for _ in range(14)])
    art = G(art, dots_, BUTTER, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1, feather=0.6)
    preview(art, "bs-stars", tone="#efe6f4")
    save(art, f"{OUT}/stars.webp", max_w=260, quality=82)
    clear()

if "star" in PARTS:
    W, H = 120, 120
    nx = Seq(30450); rng = random.Random(25)
    m = shapes(W, H, [deform(star_pts(60, 62, 46, -1.62), rng, 1, 0.03)])
    art = G(blank(W, H), m, BUTTER, "#f4c98a", seed=nx(), density=0.9, edge=0.6, bloom=0.3, rough=1.8, feather=1.0, gran=0.2)
    preview(art, "bs-star", tone="#efe6f4")
    save(art, f"{OUT}/star.webp", max_w=64, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 420, 150
    nx = Seq(30500); rng = random.Random(23)
    m = cloud_mask(W, H, 210, 106, 120, 50, rng, 5)
    art = paint_cloud(blank(W, H), m, nx)
    for (x, y, r, c) in [(84, 96, 16, BUTTER), (40, 88, 9, PEACH_D), (336, 96, 16, BUTTER), (380, 88, 9, LILAC_D)]:
        sm = shapes(W, H, [deform(star_pts(x, y, r, -1.57 + rng.uniform(-.2, .2)), rng, 1, 0.03)])
        art = G(art, sm, c, seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.4, feather=0.9)
    preview(art, "bs-divider", bg="#d8cfee")
    save(art, f"{OUT}/divider.webp", max_w=210, quality=82)
    clear()

if "sky" in PARTS:
    W, H = 520, 900
    nx = Seq(30600)
    art = blank(W, H)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    for (y0, y1, c) in [(-60, 380, "#cfe9e0"), (220, 640, "#e3d8f1"), (520, 960, "#fbdccb")]:
        band = np.clip((yy - y0) / 80, 0, 1) * np.clip((y1 - yy) / 80, 0, 1)
        art = G(art, band, c, mix(c, "#ffffff", 0.3), seed=nx(), density=0.55, edge=0.12, bloom=0.55, rough=22, feather=10, gran=0.06, pad=0)
    save_full(art, f"{OUT}/sky.webp", size=(390, 675), quality=72)
    preview(art, "bs-sky", tone="#fdfaf6")
    clear()

if "paper" in PARTS:
    im = paper(512, 512, "#fdf8f3", seed=31, fiber=0.6, mottle=0.8)
    a = np.asarray(im, np.float32) / 255
    a = np.concatenate([a, np.ones((512, 512, 1), np.float32)], -1)
    # make seamless by blending with half-offset copy
    sh = np.roll(np.roll(a, 256, 0), 256, 1)
    yy, xx = np.mgrid[0:512, 0:512].astype(np.float32)
    k = np.clip(np.minimum(np.minimum(xx, 511 - xx), np.minimum(yy, 511 - yy)) / 128, 0, 1)[..., None]
    a = a * k + sh * (1 - k)
    save_full(a, f"{OUT}/paper.webp", quality=70)
