"""Retro 70an — groovy 1970s poster paint: a dry-brushed rainbow sunrise (mustard, orange, rust, brown) with an open
centre for the photo, a painted sunburst, wavy three-stripe bands, flower-power daisies, a wavy-rayed sun, film grain.
Run: python3 -I retro-70an.py [part ...]   parts: sunrise rays wave daisy sun divider paper grain"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e4_lib import *

OUT = outdir("retro-70an")
PARTS = sys.argv[1:] or ["sunrise", "rays", "wave", "daisy", "sun", "divider", "paper", "grain"]
CREAM, MUSTARD, ORANGE, RUST, BROWN = "#f4e4c1", "#e9a632", "#e06a26", "#b5401d", "#5b3220"
PAPER = "#f3e3c3"


def ring_mask(W, H, cx, cy, r0, r1, rng, a0=math.pi, a1=2 * math.pi, wob=2.0):
    n = 90
    ph = [rng.uniform(0, 6) for _ in range(4)]
    wo = lambda i, k: wob * (math.sin(i * 0.21 + ph[k]) + 0.6 * math.sin(i * 0.53 + ph[k + 1]))
    outer = [(cx + math.cos(a0 + (a1 - a0) * i / (n - 1)) * (r1 + wo(i, 0)), cy + math.sin(a0 + (a1 - a0) * i / (n - 1)) * (r1 + wo(i, 0))) for i in range(n)]
    inner = [(cx + math.cos(a1 - (a1 - a0) * i / (n - 1)) * (r0 + wo(i, 2)), cy + math.sin(a1 - (a1 - a0) * i / (n - 1)) * (r0 + wo(i, 2))) for i in range(n)]
    return shapes(W, H, [outer + inner], smooth=False)


if "sunrise" in PARTS:
    W, H = 1000, 540
    rng = random.Random(7); nx = Seq(7000)
    cx, cy = 500, 528
    u, v = polar_uv(H, W, cx, cy)
    art = blank(W, H)
    bands = [(196, 252, MUSTARD, "#f0b844"), (258, 316, ORANGE, "#e87a30"), (322, 380, RUST, "#c24b22"), (386, 444, BROWN, "#6b3b24")]
    for r0, r1, c1, c2 in bands:
        m = ring_mask(W, H, cx, cy, r0, r1, rng)
        art = DG(art, m, c1, c2, seed=nx(), u=u, v=v, dry=0.62, rough=1.2)
    # thin cream pin-stripe inside each band (hand-pulled)
    for r0, r1, c1, c2 in bands:
        rr = (r0 + r1) / 2 + rng.uniform(-3, 3)
        line = [(cx + math.cos(a) * rr, cy + math.sin(a) * rr) for a in np.linspace(math.pi + 0.03, 2 * math.pi - 0.03, 90)]
        art = DG(art, strokes(W, H, [(line, 4.2, (0.05, 0.05))]), CREAM, seed=nx(), u=u, v=v, dry=0.55, rough=1.0, density=0.8)
    preview(art, "r7-sunrise", tone=PAPER)
    save(art, f"{OUT}/sunrise.webp", max_w=760, quality=80)
    clear()

if "rays" in PARTS:
    W, H = 840, 900
    rng = random.Random(11); nx = Seq(11000)
    cx, cy = 420, 980
    art = solid(W, H, "#a63b1c")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    th = np.arctan2(yy - cy, xx - cx); r = np.hypot(xx - cx, yy - cy)
    u, v = r, th * 300
    polys = []
    N = 22
    for k in range(N):
        a = -math.pi + (k + 0.5) / N * math.pi * 1.0 - 0.0
        a = math.pi + (k / N) * math.pi
        da = math.pi / N * 0.26 * rng.uniform(0.85, 1.1)
        polys.append([(cx, cy), (cx + math.cos(a - da) * 1500, cy + math.sin(a - da) * 1500), (cx + math.cos(a + da) * 1500, cy + math.sin(a + da) * 1500)])
    m = shapes(W, H, polys, smooth=False)
    art = DG(art, m, "#c2552a", "#c9602c", seed=nx(), u=u, v=v, dry=0.45, rough=3, density=0.95)
    art = add_grain(art, 3, 0.05)
    preview(art, "r7-rays")
    save_rgb(art, f"{OUT}/rays.webp", size=(420, 450), quality=70)
    clear()

if "wave" in PARTS:
    W, H = 1200, 210
    rng = random.Random(21); nx = Seq(21000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lam, amp = 400.0, 26.0
    wave = lambda x: amp * np.sin(x / lam * math.tau + 0.6)
    base = 105 + wave(xx)
    for k, (c1, c2) in enumerate([(BROWN, "#6b3b24"), (ORANGE, "#e87a30"), (MUSTARD, "#f0b844")]):
        off = (k - 1) * 46
        m = ((yy - base > off - 21) & (yy - base < off + 21)).astype(np.float32)
        m = gaussian_filter(m, 0.8)
        art = DG(art, m, c1, c2, seed=nx(), u=xx, v=yy - base, dry=0.4, rough=1.6)
    preview(art, "r7-wave", tone=PAPER)
    save_full(art, f"{OUT}/wave.webp", size=(860, 150), quality=80)
    clear()


def daisy(W, H, cx, cy, R, petal, centre, centre2, n, nx, rng, art, tilt=0.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(xx - cx, yy - cy); th = np.arctan2(yy - cy, xx - cx)
    u, v = r * 1.2, th * 190
    pol = []
    for k in range(n):
        a = tilt + k / n * math.tau + rng.uniform(-.05, .05)
        L = R * rng.uniform(0.9, 1.03)
        pol.append(ellipse_pts(cx + math.cos(a) * L * 0.56, cy + math.sin(a) * L * 0.56, L * 0.44, R * (0.17 if n > 11 else 0.21), n=16, rot=a))
    pm = shapes(W, H, pol)
    # brown outline (offset print feel)
    art = DG(art, np.clip(gaussian_filter(pm, 2.2) * 2.4, 0, 1), BROWN, seed=nx(), u=u, v=v, dry=0.25, rough=1.2)
    art = DG(art, pm, petal[0], petal[1], seed=nx(), u=u, v=v, dry=0.35, rough=1.2)
    cm = circles(W, H, [(cx, cy, R * 0.3)])
    art = DG(art, np.clip(gaussian_filter(cm, 2) * 2.2, 0, 1), BROWN, seed=nx(), dry=0.2, rough=1)
    art = DG(art, cm, centre, centre2, seed=nx(), u=u * 0.6, v=v, dry=0.3, rough=1.4)
    dots = [(cx + math.cos(a) * R * 0.17 * rr, cy + math.sin(a) * R * 0.17 * rr, R * 0.025) for a, rr in [(rng.uniform(0, math.tau), rng.uniform(0.2, 1)) for _ in range(9)]]
    art = DG(art, circles(W, H, dots), BROWN, seed=nx(), dry=0.1, rough=0.6, density=0.8)
    return art


if "daisy" in PARTS:
    for name, petal, c1, c2, n, seed in [("daisy", (CREAM, "#fbefd6"), ORANGE, "#e87a30", 12, 31), ("daisy-o", (ORANGE, "#e87a30"), MUSTARD, "#f0b844", 10, 37)]:
        W = H = 360
        rng = random.Random(seed); nx = Seq(seed * 1000)
        art = daisy(W, H, 180, 180, 160, petal, c1, c2, n, nx, rng, blank(W, H), tilt=rng.uniform(0, 1))
        preview(art, f"r7-{name}", tone=PAPER)
        save(art, f"{OUT}/{name}.webp", max_w=180, quality=82)
        clear()

if "sun" in PARTS:
    W = H = 420
    rng = random.Random(41); nx = Seq(41000)
    cx = cy = 210
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(xx - cx, yy - cy); th = np.arctan2(yy - cy, xx - cx)
    rays = []
    for k in range(14):
        a = k / 14 * math.tau
        pts = []
        for t in np.linspace(0, 1, 14):
            rr = 100 + 95 * t
            off = math.sin(t * math.pi * 2.2) * 0.12 * (1 - t * 0.3)
            pts.append((cx + math.cos(a + off) * rr, cy + math.sin(a + off) * rr))
        rays.append((pts, 22, (0.0, 0.55)))
    art = blank(W, H)
    art = DG(art, strokes(W, H, rays), ORANGE, "#e87a30", seed=nx(), u=r, v=th * 200, dry=0.35, rough=1.5)
    art = DG(art, circles(W, H, [(cx, cy, 112)]), RUST, seed=nx(), u=th * 200, v=r, dry=0.2, rough=1.4)
    art = DG(art, circles(W, H, [(cx, cy, 98)]), MUSTARD, "#f0b844", seed=nx(), u=th * 200, v=r, dry=0.35, rough=1.4)
    preview(art, "r7-sun", tone=PAPER)
    save(art, f"{OUT}/sun.webp", max_w=200, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 560, 110
    rng = random.Random(51); nx = Seq(51000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for k, c in enumerate([BROWN, ORANGE, MUSTARD]):
        y0 = 36 + k * 18
        line = [(x, y0 + 13 * math.sin(x / 92 * math.tau)) for x in np.linspace(40, 520, 120)]
        art = DG(art, strokes(W, H, [(line, 11, (0.08, 0.08))]), c, seed=nx(), u=xx, v=yy, dry=0.4, rough=1.0)
    preview(art, "r7-divider", tone=PAPER)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=82)
    clear()

if "paper" in PARTS:
    save_tile(paper_tile(320, PAPER, seed=9, specks=0.3), f"{OUT}/paper.webp", quality=72)

if "grain" in PARTS:
    g = film_grain_tile(200, 5)
    save_full(g, f"{OUT}/grain.webp", quality=70)
