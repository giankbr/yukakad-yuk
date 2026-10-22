"""Bulan Bintang — dreamy pastel night (periwinkle -> lilac -> blush) in soft watercolour: a large cream crescent with a
pale halo, hand-painted four-point twinkling stars, cumulus cloud banks with lilac undersides, and monogram medallions
(a painted ring of tiny stars cradled by a crescent). No figures, no calligraphy.
Run: python3 -I bulan-bintang.py [part ...]  parts: sky moon clouds puff star medallion divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e3_lib import *

OUT = outdir("bulan-bintang")
PARTS = sys.argv[1:] or ["sky", "moon", "clouds", "puff", "star", "medallion", "divider"]
PERI, PERI_D, LILAC, BLUSH = "#8f9bd8", "#6f78bd", "#c4b2e2", "#f1d3df"
CREAM, MOON_G, MOON_S = "#fff4d8", "#f0d79c", "#b9a6d6"
CLOUD, CLOUD_U = "#fbf7ff", "#a898d0"


def star_layer(art, W, H, cx, cy, r, rng, nx, warm=True):
    m = soft_star(W, H, cx, cy, r, rng, 4, 0.22, rot=rng.uniform(-0.25, 0.25) - math.pi / 2)
    art = OV(art, m, lambda mm: glow(mm, "#fff1c8", radius=max(2, r * 0.45), strength=0.5), pad=int(r * 1.6) + 4)
    art = OV(art, m, lambda mm: pigment(mm, CREAM, MOON_G if warm else CREAM, seed=nx(), density=0.95, edge=0.35, bloom=0.15, rough=1.2, feather=0.6, gran=0.1), pad=6)
    return art


if "sky" in PARTS:
    W, H = 600, 1040
    nx = Seq(9100); rng = random.Random(4)
    sky = painted_sky(W, H, [(0, "#7d88cc"), (0.35, PERI), (0.62, LILAC), (0.86, "#e6c9e3"), (1, BLUSH)], seed=nx(), streak=0.25, grain=0.7)
    # big soft watercolour blooms so the gradient reads as wet-in-wet, not airbrush
    for k in range(9):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H * 0.8)
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, rng.uniform(90, 200), rng.uniform(50, 110), 12), rng, 3, 0.18)])
        col = rng.choice(["#6d76bd", "#a99bd8", "#b6a3dc", "#8a96d6"])
        sky = G(sky, m, col, seed=nx(), density=rng.uniform(0.08, 0.16), edge=0.35, bloom=0.5, rough=14, feather=6)
    # pinprick stars, denser near the top
    pts = [(rng.uniform(0, W), (rng.random() ** 1.7) * H * 0.75, rng.uniform(0.6, 1.5)) for _ in range(150)]
    d = circles(W, H, pts)
    sky = over(sky, glow(d, "#fff6e0", 2.0, 0.6))
    sky = over(sky, flat(d, "#fffaf0", 0.9))
    sky[..., 3] = 1
    preview(sky, "bb-sky")
    save_rgb(sky, f"{OUT}/sky.webp", quality=72)
    clear()

if "moon" in PARTS:
    W, H = 520, 520
    nx = Seq(9200); rng = random.Random(5)
    cx, cy, r = 260, 260, 150
    art = blank(W, H)
    m = crescent_mask(W, H, cx, cy, r, off=0.5, rot=-0.7, inner=0.86)
    art = over(art, glow(m, "#fff0d0", 40, 0.55))
    art = over(art, glow(m, "#fff6e4", 12, 0.5))
    art = G(art, m, CREAM, "#fbe6b8", seed=nx(), density=0.95, edge=0.35, bloom=0.4, rough=3, gran=0.2)
    # pale gold glaze toward the outer rim, lilac shadow near the horns
    rim = m * np.clip(1 - light_mask(H, W, cx + 30, cy - 30, r * 1.05) * 1.6, 0, 1)
    art = G(art, rim, MOON_G, seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=4, feather=3)
    horn = m * light_mask(H, W, cx + 40, cy + 110, 130)
    art = G(art, horn, MOON_S, seed=nx(), density=0.38, edge=0.2, bloom=0.4, rough=4, feather=3)
    # soft mottled maria
    for k in range(4):
        a = rng.uniform(2.4, 4.2); rr = rng.uniform(0.55, 0.8) * r
        mm = shapes(W, H, [deform(ellipse_pts(cx + math.cos(a) * rr, cy + math.sin(a) * rr, rng.uniform(14, 30), rng.uniform(10, 20), 10, a), rng, 2, 0.15)]) * m
        art = G(art, mm, "#ecd6a8", seed=nx(), density=0.16, edge=0.15, bloom=0.5, rough=5, feather=3)
    preview(art, "bb-moon", bg="#8f9bd8")
    save(art, f"{OUT}/moon.webp", max_w=440, quality=82)
    clear()

if "clouds" in PARTS:
    W, H = 900, 300
    nx = Seq(9300); rng = random.Random(6)
    art = blank(W, H)
    for (x, y, w, h, a) in [(170, 170, 420, 150, 0.85), (700, 150, 480, 170, 0.9), (450, 236, 640, 150, 1.0), (60, 250, 300, 110, 1.0), (860, 250, 340, 120, 1.0)]:
        m = cloud_mask(W, H, x, y, w, h, rng)
        art = OV(art, m, lambda mm, a=a: pigment(mm, CLOUD, "#f6e4f2", seed=nx(), density=a, edge=0.12, bloom=0.35, rough=6, feather=2.2, gran=0.08))
        under = m * np.clip((np.arange(H, dtype=np.float32)[:, None] - (y - h * 0.15)) / (h * 0.3), 0, 1)
        art = G(art, under, CLOUD_U, "#e2b3cf", seed=nx(), density=0.5, edge=0.3, bloom=0.4, rough=7, feather=4)
    art[-40:, :, 3] = np.maximum(art[-40:, :, 3], 0)
    fill = np.zeros((H, W), np.float32); fill[262:, :] = 1
    art = OV(art, fill, lambda mm: pigment(mm, "#f6eefc", "#efe4f8", seed=nx(), density=1, edge=0, bloom=0.2, rough=4, feather=2, gran=0.05))
    preview(art, "bb-clouds", bg="#c4b2e2")
    save_full(art, f"{OUT}/clouds.webp", size=(780, 260), quality=78)
    clear()

if "puff" in PARTS:
    W, H = 420, 170
    nx = Seq(9400); rng = random.Random(7)
    m = cloud_mask(W, H, 210, 110, 360, 130, rng, puffs=5)
    art = OV(blank(W, H), m, lambda mm: pigment(mm, CLOUD, "#efe6fb", seed=nx(), density=0.9, edge=0.25, bloom=0.35, rough=6, feather=2.2))
    under = m * np.clip((np.arange(H, dtype=np.float32)[:, None] - 80) / 40, 0, 1)
    art = G(art, under, CLOUD_U, seed=nx(), density=0.4, edge=0.3, bloom=0.4, rough=6, feather=4)
    preview(art, "bb-puff", bg="#8f9bd8")
    save(art, f"{OUT}/puff.webp", max_w=260, quality=80)
    clear()

if "star" in PARTS:
    W, H = 160, 160
    nx = Seq(9500); rng = random.Random(8)
    art = star_layer(blank(W, H), W, H, 80, 80, 56, rng, nx)
    preview(art, "bb-star", bg="#8f9bd8")
    save_full(art, f"{OUT}/star.webp", size=(80, 80), quality=84)
    clear()

if "medallion" in PARTS:
    W, H = 560, 560
    nx = Seq(9600); rng = random.Random(9)
    cx, cy = 280, 270
    art = blank(W, H)
    disc = shapes(W, H, [deform(ellipse_pts(cx, cy, 196, 196, 20), rng, 2, 0.02)])
    art = G(art, disc, "#eee6fb", "#e4dcf6", seed=nx(), density=0.85, edge=0.45, bloom=0.5, rough=5, gran=0.15)
    art = G(art, disc * (1 - light_mask(H, W, cx - 60, cy - 70, 300)), LILAC, seed=nx(), density=0.35, edge=0.2, bloom=0.4, rough=6, feather=4)
    ring = ring_mask(W, H, cx, cy, 214, 2.6)
    art = G(art, ring, "#d9bf86", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1.2, feather=0.6)
    dots = circles(W, H, [(cx + math.cos(a) * 228, cy + math.sin(a) * 228, 2.4) for a in np.linspace(-0.4, math.pi + 0.4, 16)])
    art = G(art, dots, "#d9bf86", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    # crescent cradling the bottom-left
    cr = crescent_mask(W, H, cx - 12, cy + 18, 236, off=0.16, rot=-1.05, inner=0.97)
    cr *= np.clip((np.arange(H, dtype=np.float32)[:, None] - cy + 40) / 40, 0, 1)
    art = OV(art, cr, lambda mm: glow(mm, "#fff0d0", 10, 0.3))
    art = G(art, cr, CREAM, MOON_G, seed=nx(), density=0.95, edge=0.45, bloom=0.3, rough=2.5)
    art = G(art, cr * light_mask(H, W, cx + 180, cy + 120, 200), MOON_S, seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=3, feather=2)
    for (sx, sy, sr) in [(cx + 168, cy - 170, 30), (cx + 212, cy - 104, 15), (cx + 120, cy - 214, 12), (cx - 214, cy - 124, 18)]:
        art = star_layer(art, W, H, sx, sy, sr, rng, nx)
    preview(art, "bb-medallion", bg="#c4b2e2")
    save_full(art, f"{OUT}/medallion.webp", size=(420, 420), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 640, 80
    nx = Seq(9700); rng = random.Random(10)
    cy = 40
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 2.2, 0, 1)[None, :]
    ln = (rect(W, H, 40, cy - 1.1, 272, cy + 1.1) + rect(W, H, 368, cy - 1.1, 600, cy + 1.1)) * fade
    art = G(blank(W, H), ln, "#a594cf", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1.2, feather=0.6)
    cr = crescent_mask(W, H, 320, cy, 24, off=0.42, rot=-0.5, inner=0.86)
    art = G(art, cr, CREAM, MOON_G, seed=nx(), density=1, edge=0.6, bloom=0.2, rough=1.5, feather=0.7)
    art = G(art, cr * light_mask(H, W, 328, cy + 18, 22), "#b29bd2", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1, feather=0.8)
    for x, r in [(254, 9), (390, 11), (226, 5), (420, 6)]:
        art = star_layer(art, W, H, x, cy, r, rng, nx)
    preview(art, "bb-divider", bg="#f3eefb")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()
