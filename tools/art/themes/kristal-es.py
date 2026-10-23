"""Kristal Es — pernikahan musim dingin: bunga es (frost fern) yang tumbuh dari sudut kaca jendela, kristal salju
heksagonal, ranting bersalju dalam cat air, dan cahaya perak-biru di balik kaca yang buram.
Run: python3 -I kristal-es.py [part ...]   parts: frost flakes branch pane snow     Assets -> public/themes/art/kristal-es/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n5_lib import *
import random

OUT = outdir("kristal-es")
PARTS = sys.argv[1:] or ["frost", "flakes", "branch", "pane", "snow"]
GLASS = "#5d7a96"


def frost():
    W = H = 720
    rng = random.Random(7)
    items = []
    for k in range(13):
        a = (k + rng.uniform(-0.3, 0.3)) / 12 * (math.pi / 2)
        L = rng.uniform(300, 640) * (0.7 + 0.3 * math.sin(a * 2))
        frost_fern(rng.uniform(-10, 30), rng.uniform(-10, 30), a, L, rng.uniform(3.2, 4.4), 2, rng, items)
    for _ in range(9):  # stray small ferns near the corner
        r = rng.uniform(60, 320); a = rng.uniform(0, math.pi / 2)
        frost_fern(math.cos(a) * r, math.sin(a) * r, rng.uniform(0, math.tau), rng.uniform(40, 110), 2.0, 1, rng, items)
    m = strokes(W, H, [(p, w, (0.0, 0.6)) for p, w in items])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx, yy) / 720
    mist = np.clip(1.15 - d * 1.5, 0, 1) ** 1.6 * (0.45 + 0.55 * fbm(W, H, 4, 60, 4))
    art = rgba(flat(H, W, "#f2f7fb"), np.clip(mist * 0.62, 0, 1))
    art = ice(art, m, seed=3, edge="#9db5cc", body="#ffffff", alpha=0.92, halo=0.6)
    preview(art, "frost", bg=GLASS)
    clear()
    return save(art, f"{OUT}/frost.webp", max_w=420, quality=78)


def flakes():
    for name, kind, R, mw, rot in (("flake", 0, 170, 240, 0.0), ("flake2", 1, 120, 130, 0.26), ("flake3", 2, 110, 120, 0.1)):
        W = H = int(R * 2.2)
        m = crystal_masks(W, H, W / 2, H / 2, R, random.Random(kind), kind, rot)
        art = ice(blank(W, H), m, seed=kind + 4, edge="#5f83a8", body="#fbfdff", alpha=1.0, halo=0.7)
        preview(art, name, bg=GLASS)
        save(art, f"{OUT}/{name}.webp", max_w=mw, quality=84)


def branch():
    W, H = 940, 380
    rng = random.Random(12)
    segs = []
    twig(-10, 120, -0.06, 920, 17, 3, rng, segs, droop=1.0)
    twig(-10, 150, 0.2, 520, 10, 2, rng, segs)
    twig(200, 116, -0.55, 300, 7, 2, rng, segs)
    bark = strokes(W, H, [(p, w, (0.0, 0.7)) for p, w in segs])
    nx_ = [100]

    def nx():
        nx_[0] += 17
        return nx_[0]
    art = G(blank(W, H), bark, "#5e5662", "#3b3644", seed=nx(), density=0.88, edge=0.6, bloom=0.2, rough=1.6, feather=0.8)
    art = G(art, strokes(W, H, [(p, w * 0.35, (0.0, 0.7)) for p, w in segs if w > 5]), "#3a3542", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=0.8, feather=0.6)
    snow_items = []
    for pts, w in segs:
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            a = math.atan2(y1 - y0, x1 - x0)
            k = max(0.0, math.cos(a)) ** 2
            if k < 0.25:
                continue
            ww = w * (0.85 + 0.35 * rng.random()) * k
            snow_items.append(([(x0, y0 - w * 0.62), (x1, y1 - w * 0.62)], ww, None))
    snow = displace(strokes(W, H, snow_items), 5, 2.5, 14)
    shadow = np.clip(np.roll(snow, 3, 0) - snow, 0, 1)
    art = OV(art, snow, lambda m: gouache_paint(m, "#fbfdff", "#e8f0f7", seed=8, rough=2.0, streak=0.3))
    art = G(art, shadow * bark.clip(0, 1) + np.clip(snow - gaussian_filter(snow, 2.5), 0, 1) * 0.6, "#9fb3c8", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=0.6, feather=0.7)
    preview(art, "branch", bg="#c9d7e3")
    clear()
    return save(art, f"{OUT}/branch.webp", max_w=760, quality=80)


def pane():
    W, H = 780, 1500
    art = painted_sky(W, H, [(0, "#8ea7bf"), (0.35, "#b7c8d8"), (0.62, "#dbe5ee"), (1, "#eef3f7")], seed=5, streak=0.4)
    rng = random.Random(3)
    # out-of-focus winter pines beyond the glass
    trees = []
    for i in range(16):
        x = rng.uniform(-40, W + 40); base = rng.uniform(H * 0.72, H * 0.92); h = rng.uniform(260, 520); w = h * 0.34
        trees.append([(x, base - h), (x + w, base), (x - w, base)])
    tm = shapes(W, H, trees, smooth=False)
    tm = gaussian_filter(np.maximum(tm, (np.mgrid[0:H, 0:W][0] > H * 0.86).astype(np.float32)), 18)
    art = over(art, rgba(flat(H, W, "#6d86a0"), tm * 0.5))
    # snow ground
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    gm = gaussian_filter((yy > H * 0.88 + 30 * np.sin(np.mgrid[0:H, 0:W][1] / 140.0)).astype(np.float32), 14)
    art = over(art, rgba(flat(H, W, "#f4f8fb"), gm * 0.9))
    # soft bokeh of winter light
    bk = circles(W, H, [(rng.uniform(0, W), rng.uniform(H * 0.1, H * 0.8), rng.uniform(14, 46)) for _ in range(26)])
    art = over(art, rgba(flat(H, W, "#ffffff"), gaussian_filter(bk, 6) * 0.22))
    art = add_grain(art, 4, 0.02)
    save_rgb(art, f"{OUT}/pane.webp", size=(520, 1000), quality=72)


def snow():
    """Seamless 360px tile of falling snow (soft dots + a few tiny crystals) for the animated layer."""
    n = 360
    rng = random.Random(21)
    dots = []
    for _ in range(46):
        x, y, r = rng.uniform(0, n), rng.uniform(0, n), rng.uniform(1.2, 3.6)
        for dx in (-n, 0, n):
            for dy in (-n, 0, n):
                dots.append((x + dx, y + dy, r))
    m = circles(n, n, dots)
    m = np.maximum(gaussian_filter(m, 0.9) * 1.2, gaussian_filter(m, 3) * 0.5)
    art = rgba(flat(n, n, "#ffffff"), np.clip(m, 0, 1) * 0.85)
    for _ in range(4):
        cx, cy = rng.uniform(30, n - 30), rng.uniform(30, n - 30)
        art = ice(art, crystal_masks(n, n, cx, cy, rng.uniform(7, 10), rng, rng.choice((0, 2)), rng.uniform(0, 1)), seed=2, body="#ffffff", edge="#c8d8e8", halo=0.4)
    save_full(art, f"{OUT}/snow.webp", quality=80)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
