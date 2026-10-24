"""Awan Syari — modern syar'i pale-sky theme: a painted sky (powder blue fading to a warm haze), a soft peach-gold sun
glow, a rising cumulus cloud bank, small drifting clouds and a thin cloud wisp for dividers. Watercolour/gouache, no
figures, no calligraphy. Run: python3 -I awan-syari.py [part ...]   parts: sky sun bank cloud wisp"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s6_lib import *

OUT = outdir("awan-syari")
PARTS = sys.argv[1:] or ["sky", "sun", "bank", "cloud", "wisp"]
WHITE, SHADE, SHADE_D, BLUE = "#ffffff", "#c9dbea", "#a9c3da", "#b9d6ec"


def puff(art, W, H, m, nx, light=WHITE, shadow=SHADE, under=0.45, sun=(1.0, -1.0)):
    """Cloud mask -> soft opaque gouache cloud: white body, blue-grey underside and lobe creases, warm lit tops,
    displaced hand-cut edge, faint brush texture. Painted directly (pigment() darkens whites)."""
    ys, xs = np.where(m > 0.1)
    if len(ys) == 0:
        return art
    y0, y1 = ys.min() - 30, ys.max() + 30
    y0 = max(0, y0); y1 = min(H, y1)
    sub = m[y0:y1]
    h = sub.shape[0]
    seed = nx()
    md = displace(sub, seed, 5.0, 26)
    alpha = np.clip(gaussian_filter(md, 2.0) * 1.25, 0, 1)
    yy = np.arange(h, dtype=np.float32)[:, None] + y0
    sy0, sy1 = ys.min(), ys.max()
    low = np.clip((yy - (sy0 + (sy1 - sy0) * 0.35)) / ((sy1 - sy0) * 0.65 + 1), 0, 1) ** 1.4
    g3 = gaussian_filter(md, 3)
    crease = np.clip(g3 - np.roll(np.roll(gaussian_filter(md, 8), -12, 0), 9, 1), 0, 1)
    crease = gaussian_filter(crease, 3) * 1.8
    tex = fbm(W, h, seed + 3, 40, 3)
    t = np.clip((low * under * 1.3 + crease * 1.0) * (0.7 + 0.6 * tex), 0, 1) * np.clip(g3 * 1.4, 0, 1)
    lit = np.clip(md - np.roll(np.roll(gaussian_filter(md, 4), 7, 0), -6, 1), 0, 1)
    lit = gaussian_filter(lit, 2.0) * (1 - low) * 1.2
    cw = np.array(hex_rgb(light), np.float32); cs = np.array(hex_rgb(shadow), np.float32); cd = np.array(hex_rgb(SHADE_D), np.float32)
    rgb = cw * (1 - t[..., None]) + (cs * (1 - t[..., None]) + cd * t[..., None]) * t[..., None]
    rgb = rgb * (1 - lit[..., None] * 0.0) + (np.array(hex_rgb("#fde4c4")) - rgb) * np.clip(lit * 0.45, 0, 0.32)[..., None]
    streak = gaussian_filter(np.random.default_rng(seed).random((h, W)).astype(np.float32), (0.6, 4))
    rgb = rgb * (1 + (streak - streak.mean())[..., None] * 0.12)
    out = art.copy()
    out[y0:y1] = over(art[y0:y1], rgba(rgb.astype(np.float32), alpha))
    return out


def sky():
    W, H = 600, 1100
    rng = random.Random(4); nx = Seq(100)
    art = painted_sky(W, H, [(0, "#a6cbe6"), (0.35, "#c6def0"), (0.7, "#e2edf6"), (1, "#f4eee8")], seed=7, streak=0.05, grain=0.3)
    for (cx, cy, rx, ry, c) in [(160, 160, 300, 160, "#9cc2e0"), (420, 520, 280, 140, "#b5d2ea"), (120, 760, 260, 120, "#c4dbee")]:
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, ry, 10), rng, 3, 0.18))
        art = G(art, m, c, seed=nx(), density=0.22, edge=0.12, bloom=0.6, rough=18, feather=8, gran=0.25)
    # warm haze from the sun (upper right)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - 470) / 1.0) ** 2 + ((yy - 230) / 1.15) ** 2)
    warm = np.clip(1 - d / 520, 0, 1) ** 1.8
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fbe3c4")), warm * 0.55))
    # far soft cloud washes, very pale
    for (cx, cy, w, h) in [(120, 420, 300, 60), (480, 610, 260, 50), (200, 820, 380, 70), (520, 120, 200, 34)]:
        m = cloud_mask(W, H, cx, cy, w, h, rng, lobes=7)
        art = OV(art, soft(m, 6), lambda mm: pigment(mm, "#f7fbff", seed=nx(), density=0.55, edge=0.0, bloom=0.4, rough=10, feather=6), pad=40)
    # streaky cirrus
    cir = []
    for _ in range(14):
        y = rng.uniform(60, 700); x = rng.uniform(-80, W)
        L = rng.uniform(80, 220)
        cir.append(([(x, y), (x + L * .5, y - rng.uniform(2, 8)), (x + L, y + rng.uniform(-3, 3))], rng.uniform(3, 7), (0.45, 0.45)))
    art = OV(art, soft(strokes(W, H, cir), 2.5), lambda mm: pigment(mm, "#ffffff", seed=nx(), density=0.5, edge=0, bloom=0.3, rough=4, feather=2), pad=20)
    show(art, "awan-sky", bg="#ffffff")
    save_rgb(art, f"{OUT}/sky.webp", quality=72)


def sun():
    W, H = 420, 420
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - 210) ** 2 + (yy - 210) ** 2)
    n = fbm(W, H, 33, 30, 3)
    dd = d * (0.94 + 0.12 * n)
    halo = np.clip(1 - dd / 200, 0, 1) ** 2.2 * 0.75
    core = np.clip((70 - dd) / 10, 0, 1)
    a = np.clip(halo + core, 0, 1)
    t = np.clip(dd / 200, 0, 1)
    rgb = ramp_rgb(t, [(0, "#fff8ea"), (0.3, "#ffeccc"), (0.6, "#fcdcb0"), (1, "#f7d2a6")])
    art = rgba(rgb, a)
    show(art, "awan-sun", bg="#c6def0")
    save(art, f"{OUT}/sun.webp", max_w=320, quality=80)


def ramp_rgb(t, stops):
    out = np.zeros(t.shape + (3,), np.float32)
    for i in range(len(stops) - 1):
        a0, c0 = stops[i]; a1, c1 = stops[i + 1]
        k = np.clip((t - a0) / (a1 - a0), 0, 1)[..., None]
        sel = ((t >= a0) & (t <= a1))[..., None]
        out = np.where(sel, np.array(hex_rgb(c0)) * (1 - k) + np.array(hex_rgb(c1)) * k, out)
    return out.astype(np.float32)


def bank():
    W, H = 820, 420
    rng = random.Random(9); nx = Seq(500)
    art = blank(W, H)
    # three rows of cumulus: back (tall), middle, front (flat base filling the bottom)
    back = np.maximum.reduce([cloud_mask(W, H, cx, cy, w, h, rng, lobes=7) for (cx, cy, w, h) in [(150, 170, 330, 170), (640, 150, 360, 190), (400, 210, 280, 120)]])
    art = puff(art, W, H, back, nx, shadow="#cfdcea", under=0.35)
    mid = np.maximum.reduce([cloud_mask(W, H, cx, cy, w, h, rng, lobes=8) for (cx, cy, w, h) in [(60, 280, 300, 150), (420, 290, 420, 160), (760, 270, 280, 150)]])
    art = puff(art, W, H, mid, nx, shadow="#c6d6e7", under=0.4)
    front = np.maximum.reduce([cloud_mask(W, H, cx, cy, w, h, rng, lobes=9) for (cx, cy, w, h) in [(220, 360, 520, 130), (640, 370, 480, 120)]])
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    front = np.maximum(front, np.clip((yy - 360) / 4, 0, 1))
    art = puff(art, W, H, front, nx, shadow="#d4e0ec", under=0.15)
    # warm light on the tops (sun upper right)
    tops = np.clip(np.maximum.reduce([back, mid]) - np.roll(np.roll(np.maximum.reduce([back, mid]), 10, 0), -8, 1), 0, 1)
    art = G(art, tops, "#fbe2c2", seed=nx(), density=0.35, edge=0.2, bloom=0.4, rough=5, feather=2)
    # the bottom stays pure white so text can sit on it
    solid_ = np.clip((yy - 330) / 50, 0, 1)
    art = over(art, rgba(np.ones((H, W, 3), np.float32), solid_))
    art[-2:, :, 3] = 1
    show(art, "awan-bank", bg="#c6def0")
    save(art, f"{OUT}/bank.webp", max_w=780, quality=78)


def cloud():
    W, H = 420, 220
    rng = random.Random(15); nx = Seq(700)
    art = blank(W, H)
    m = circles(W, H, [(110, 150, 50), (170, 112, 66), (250, 98, 78), (320, 138, 54), (360, 168, 30), (60, 176, 26)])
    m = m * (np.arange(H)[:, None] < 196)
    art = puff(art, W, H, m, nx)
    show(art, "awan-cloud", bg="#c6def0")
    save(art, f"{OUT}/cloud.webp", max_w=260, quality=80)


def wisp():
    W, H = 520, 120
    rng = random.Random(21); nx = Seq(900)
    art = blank(W, H)
    m = np.maximum.reduce([cloud_mask(W, H, 260, 64, 300, 56, rng, lobes=9), soft(strokes(W, H, [([(20, 82), (180, 78), (340, 80), (500, 84)], 14, (0.4, 0.4))]), 2)])
    art = puff(art, W, H, m, nx, shadow="#b9cfe3", under=0.6)
    show(art, "awan-wisp", bg="#eaf2f8")
    save(art, f"{OUT}/wisp.webp", max_w=320, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
