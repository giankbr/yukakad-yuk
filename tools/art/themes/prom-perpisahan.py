"""Prom Perpisahan — SMA farewell night, painted stage-light gouache with silver & gold foil (original designs): a mirror
disco ball on its cord (hand-laid tiles catching magenta/cyan light), a soft stage spotlight beam, a crowd of classmates
cut as a linocut silhouette with rim light (hands up, a cap tossed in the air), a rosette class-year badge (the year is
typeset in CSS), a glitter scatter and a sparkle-string divider.
Run: python3 -I prom-perpisahan.py [part ...]  parts: disco beam crowd badge glitter divider
Assets -> public/themes/art/prom-perpisahan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e6_lib import *

OUT = outdir("prom-perpisahan")
PARTS = sys.argv[1:] or ["disco", "beam", "crowd", "badge", "glitter", "divider"]
NIGHT, VIOLET = "#120b2e", "#2a1650"
MAG, CYAN, SILVER, GOLD = "#e8459a", "#4fd6e8", "#d9dbe6", "#f2c55c"


def sparkle(W, H, x, y, r, thin=0.18):
    """4-point star polygon."""
    pts = []
    for i in range(8):
        a = i * math.pi / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * thin
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    return shapes(W, H, [pts], smooth=False)


def hash01(a, b, seed):
    v = np.sin(a * 12.9898 + b * 78.233 + seed * 3.17) * 43758.5453
    return v - np.floor(v)


if "disco" in PARTS:
    W, H = 480, 600
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    cx, cy, R = 240, 360, 196
    cord = strokes(W, H, [([(240, 0), (240, cy - R + 6)], 4, None)])
    art = G(art, cord, "#b9bccb", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5)
    cap = shapes(W, H, [[(222, cy - R - 14), (258, cy - R - 14), (262, cy - R + 14), (218, cy - R + 14)]], smooth=False)
    art = FO(art, cap, "#c8cad6", seed=nx(), emboss=0.7, sparkle=0.2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = (xx - cx) / R, (yy - cy) / R
    r2 = dx * dx + dy * dy
    inside = (r2 < 1).astype(np.float32)
    dz = np.sqrt(np.clip(1 - r2, 0, 1))
    lat = np.arcsin(np.clip(-dy, -1, 1))
    lon = np.arctan2(dx, dz)
    nl = 16
    li = np.floor((lat + math.pi / 2) / math.pi * nl)
    ncol = np.maximum(4, np.round(np.cos((li + 0.5) / nl * math.pi - math.pi / 2) * 30))
    lj = np.floor((lon + math.pi) / math.tau * ncol)
    fu = ((lat + math.pi / 2) / math.pi * nl) % 1
    fv = ((lon + math.pi) / math.tau * ncol) % 1
    grout = np.clip(np.minimum(np.minimum(fu, 1 - fu) / 0.09, np.minimum(fv, 1 - fv) * ncol / nl / 0.09 / 1.0), 0, 1)
    h1 = hash01(li, lj, 1); h2 = hash01(li, lj, 2)
    light = np.clip(dx * -0.55 + -dy * 0.6 + dz * 0.6, 0, 1)
    base = np.stack([0.62 + 0.25 * h1, 0.63 + 0.24 * h1, 0.72 + 0.2 * h1], -1)
    tint = np.zeros_like(base)
    mag = np.array(hex_rgb(MAG)); cyan = np.array(hex_rgb(CYAN)); gold = np.array(hex_rgb(GOLD)); vio = np.array(hex_rgb("#6a4bd8"))
    pick = np.where(h2[..., None] < 0.18, mag, np.where(h2[..., None] < 0.32, cyan, np.where(h2[..., None] < 0.4, gold, np.where(h2[..., None] < 0.6, vio, base))))
    k = np.where(h2 < 0.6, 0.55, 0.0)[..., None]
    col = base * (1 - k) + pick * k
    shade = (0.35 + 0.85 * light)[..., None]
    col = col * shade
    # specular hits: a few tiles burn white near the light
    hot = (hash01(li, lj, 7) > 0.86) & (light > 0.55)
    col = np.where(hot[..., None], np.array([1.0, 0.98, 1.0]), col)
    col = col * (0.25 + 0.75 * grout[..., None]) + np.array(hex_rgb(NIGHT)) * (1 - grout[..., None]) * 0.6
    # paint texture: brush streak + grain
    s = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (0.6, 4))
    s = (s - s.mean()) / (s.std() + 1e-6)
    col = col * (1 + s[..., None] * 0.04)
    edge = np.clip((1 - np.sqrt(r2)) * R / 1.5, 0, 1)
    ball = np.concatenate([np.clip(col, 0, 1), (inside * edge)[..., None]], -1).astype(np.float32)
    art = over(art, ball)
    # rim light
    rim = np.clip(np.sqrt(r2) - 0.9, 0, 0.1) / 0.1 * inside
    art = G(art, rim * np.clip(dx + 0.3, 0, 1), MAG, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = G(art, rim * np.clip(-dx + 0.3, 0, 1), CYAN, seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    # glints
    for x, y, r in ((cx - 92, cy - 110, 34), (cx + 40, cy - 150, 20), (cx - 30, cy - 40, 16), (cx + 110, cy + 40, 14)):
        sp = sparkle(W, H, x, y, r)
        art = over(art, glow(sp, "#ffffff", 5, 0.6))
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32), sp[..., None]], -1))
    preview(art, "pr-disco", bg=NIGHT)
    save(art, f"{OUT}/disco.webp", max_w=300, quality=82)
    clear()

if "beam" in PARTS:
    W, H = 360, 900
    nx = Seq(300)
    b = beam_mask(W, H, 180, -40, math.pi / 2, 940, 0.27)
    dust = fbm(W, H, 5, 30, 3)
    streak = gaussian_filter(np.random.default_rng(4).random((H, W)).astype(np.float32), (40, 1.5))
    streak = (streak - streak.min()) / (streak.max() - streak.min())
    a = np.clip(b * (0.55 + 0.35 * dust + 0.25 * (streak - 0.5)), 0, 1) * 0.75
    top = np.clip(1 - np.arange(H) / 90, 0, 1)[:, None]
    a = np.clip(a + top * b * 0.4, 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fff1fb"), np.float32)
    art = np.concatenate([rgb, a[..., None]], -1)
    preview(art, "pr-beam", bg=NIGHT)
    save_full(art, f"{OUT}/beam.webp", size=(180, 450), quality=78)

if "crowd" in PARTS:
    W, H = 1100, 330
    nx = Seq(500); rng = random.Random(5)
    polys = []
    circ = []
    rims = []
    x = -20
    while x < W + 20:
        hgt = rng.uniform(150, 230)
        hr = rng.uniform(28, 36)
        hx, hy = x + rng.uniform(-6, 6), H - hgt
        polys.append(ellipse_pts(hx, hy, hr * 0.84, hr, 14))
        sw = rng.uniform(58, 76)
        polys.append([(hx - sw, H + 10), (hx - sw * 0.96, hy + hr * 2.5), (hx - sw * 0.62, hy + hr * 1.75), (hx - hr * 0.42, hy + hr * 1.35), (hx - hr * 0.36, hy + hr * 0.6),
                      (hx + hr * 0.36, hy + hr * 0.6), (hx + hr * 0.42, hy + hr * 1.35), (hx + sw * 0.62, hy + hr * 1.75), (hx + sw * 0.96, hy + hr * 2.5), (hx + sw, H + 10)])
        if rng.random() < 0.45:  # raised arm
            side = rng.choice([-1, 1])
            ax = hx + side * sw * 0.6
            tip = (ax + side * rng.uniform(10, 40), hy - rng.uniform(60, 110))
            polys.append(ribbon_band(W, H, curve([(ax, hy + hr * 2.2), (ax + side * 10, hy + 6), tip], 12), 20))
            circ.append((tip[0], tip[1] - 4, 12))
        if rng.random() < 0.25:  # hair bun / hijab outline variety
            circ.append((hx, hy - hr * 0.7, hr * 0.55))
        x += rng.uniform(78, 104)
    m = np.maximum(shapes(W, H, polys), circles(W, H, circ))
    art = blank(W, H)
    art = LC(art, m, "#0b0720", seed=nx(), wear=0.12, rough=1.6)
    # rim light from the stage (top-left magenta, right cyan)
    e = np.clip(m - np.roll(np.roll(m, 4, 0), 3, 1), 0, 1)
    art = G(art, e, MAG, seed=nx(), density=0.9, edge=0.2, bloom=0, rough=1, feather=0.6)
    e2 = np.clip(m - np.roll(np.roll(m, 4, 0), -3, 1), 0, 1) * (np.arange(W)[None, :] > W * 0.5)
    art = G(art, e2, CYAN, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1, feather=0.6)
    # tossed graduation cap
    capm = shapes(W, H, [[(760, 40), (810, 22), (858, 42), (808, 62)]], smooth=False)
    art = LC(art, capm, "#0b0720", seed=nx(), wear=0.1)
    art = G(art, np.clip(capm - np.roll(capm, 3, 0), 0, 1), MAG, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5)
    tassel = strokes(W, H, [([(808, 42), (826, 60), (830, 84)], 2.5, None)])
    art = FO(art, tassel, GOLD, seed=nx(), emboss=0.3)
    preview(art, "pr-crowd", bg="#3a1f6e")
    save(art, f"{OUT}/crowd.webp", max_w=780, quality=78)
    clear()

if "badge" in PARTS:
    W, H = 400, 460
    nx = Seq(700); rng = random.Random(7)
    art = blank(W, H)
    cx, cy = 200, 180
    tails = shapes(W, H, [[(150, 250), (110, 440), (146, 420), (170, 446), (196, 270)], [(250, 250), (290, 440), (254, 420), (230, 446), (204, 270)]], smooth=False)
    art = satin(art, tails, MAG, "#ff6fb4", nx, angle=1.3, freq=8, sheen=0.5)
    pts = []
    for i in range(48):
        a = i * math.tau / 48
        rr = 158 if i % 2 == 0 else 142
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    ros = shapes(W, H, [pts], smooth=False)
    art = FO(art, ros, "#c8cad6", seed=nx(), emboss=0.8, sparkle=0.35)
    disc = circles(W, H, [(cx, cy, 120)])
    art = GP(art, disc, VIOLET, "#3b1f74", seed=nx(), rough=0.8, streak=0.6)
    art = G(art, inner_shade(disc, -10, -10, 14), MAG, seed=nx(), density=0.35, edge=0, bloom=0.2, rough=1)
    ring = np.clip(circles(W, H, [(cx, cy, 108)]) - circles(W, H, [(cx, cy, 102)]), 0, 1)
    art = FO(art, ring, GOLD, seed=nx(), emboss=0.4)
    for a in np.linspace(math.pi * 1.15, math.pi * 1.85, 5):
        sp = sparkle(W, H, cx + math.cos(a) * 86, cy + math.sin(a) * 86, 8, 0.3)
        art = FO(art, sp, GOLD, seed=nx(), emboss=0.3)
    preview(art, "pr-badge", bg=NIGHT)
    save(art, f"{OUT}/badge.webp", max_w=200, quality=84)
    clear()

if "glitter" in PARTS:
    W, H = 600, 600
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    for _ in range(26):
        x, y, r = rng.uniform(20, W - 20), rng.uniform(20, H - 20), rng.uniform(5, 16)
        col = rng.choice(["#ffffff", GOLD, "#ffd0ea", "#bff4fb"])
        sp = sparkle(W, H, x, y, r, 0.22)
        art = over(art, glow(sp, col, 4, 0.45))
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb(col), np.float32), sp[..., None]], -1))
    dots = []
    for _ in range(70):
        dots.append((rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.4, 3.2)))
    dm = circles(W, H, dots)
    art = FO(art, dm, GOLD, seed=nx(), emboss=0.2, sparkle=0.4)
    preview(art, "pr-glitter", bg=NIGHT)
    save_full(art, f"{OUT}/glitter.webp", size=(300, 300), quality=80)

if "divider" in PARTS:
    W, H = 440, 90
    nx = Seq(1100)
    art = blank(W, H)
    line = strokes(W, H, [([(20, 45), (180, 45)], 2.2, (0.6, 0.0)), ([(260, 45), (420, 45)], 2.2, (0.0, 0.6))])
    art = FO(art, line, "#c8cad6", seed=nx(), emboss=0.3)
    for x, r in ((220, 30), (176, 11), (264, 11), (140, 6), (300, 6)):
        sp = sparkle(W, H, x, 45, r, 0.2)
        art = over(art, glow(sp, MAG if r < 20 else "#ffffff", 5, 0.5))
        art = FO(art, sp, GOLD if r > 20 else "#e6e7ef", seed=nx(), emboss=0.4, sparkle=0.3)
    preview(art, "pr-divider", bg=NIGHT)
    save(art, f"{OUT}/divider.webp", max_w=220, quality=84)

kb(OUT)
