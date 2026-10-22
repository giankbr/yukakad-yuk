"""Langit Subuh — the calm minute before sunrise, painted wet-on-wet: a pastel dawn sky (powder blue, lilac, rose,
apricot) whose bands bleed into each other, a low skyline of distant domes and minarets in two soft lilac-grey washes
dissolving into morning mist, and the first fan of light rising behind them. Original design, no figures.
Run: python3 -I langit-subuh.py [part ...]  parts: sky skyline rays divider sun paper
Assets -> public/themes/art/langit-subuh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c3_lib import *

OUT = outdir("langit-subuh")
PARTS = sys.argv[1:] or ["sky", "skyline", "rays", "divider", "sun", "paper"]
SKY = [(0.0, "#a9b9da"), (0.22, "#c3c5e2"), (0.42, "#e3cbdc"), (0.58, "#f4d2cb"), (0.7, "#fbdfc0"), (0.8, "#fcebd3"), (1.0, "#f8f1e8")]
FAR, FAR2 = "#bdb4d3", "#d1bccf"
NEAR, NEAR2 = "#8f8db5", "#a395b6"
PAPER = "#f8f2ea"


def dome_pts(cx, base, r, peak=1.38, n=36):
    """Onion-ish dome outline sitting on `base` (a slight swell, then a soft point)."""
    L = bez((cx - r, base), (cx - r * 1.12, base - r * 0.85), (cx - r * 0.28, base - r * 1.02), (cx, base - r * peak), n)
    R = [(2 * cx - x, y) for (x, y) in reversed(L)]
    return L + R[1:]


def crescent(W, H, x, y, r):
    return np.clip(circles(W, H, [(x, y, r)]) - circles(W, H, [(x + r * 0.45, y - r * 0.2, r * 0.86)]), 0, 1)


def minaret(W, H, x, base, h, w):
    """Slender minaret: tapering shaft, two balconies, a pencil cone, a finial and a small crescent."""
    items = []
    items.append([(x - w * 0.5, base), (x - w * 0.42, base - h * 0.72), (x + w * 0.42, base - h * 0.72), (x + w * 0.5, base)])
    for (t, ww, hh) in [(0.5, 0.78, 0.022), (0.72, 0.8, 0.026)]:
        yb = base - h * t
        items.append([(x - w * ww, yb), (x - w * ww * 0.7, yb - h * hh), (x + w * ww * 0.7, yb - h * hh), (x + w * ww, yb)])
    items.append([(x - w * 0.34, base - h * 0.72), (x - w * 0.3, base - h * 0.86), (x + w * 0.3, base - h * 0.86), (x + w * 0.34, base - h * 0.72)])
    items.append([(x - w * 0.36, base - h * 0.86), (x, base - h * 0.995), (x + w * 0.36, base - h * 0.86)])
    m = np.zeros((H, W), np.float32)
    for p in items:
        m = np.maximum(m, poly(W, H, p))
    m = np.maximum(m, strokes(W, H, [([(x, base - h * 0.99), (x, base - h * 1.04)], max(1.0, w * 0.06), None)]))
    m = np.maximum(m, crescent(W, H, x, base - h * 1.06, max(2.2, w * 0.16)))
    return m


def mosque(W, H, cx, base, r, mh, mw, side=1.6, small=True):
    """A domed prayer hall on a low base with flanking minarets and smaller side domes."""
    m = rect(W, H, cx - r * 2.3, base - r * 0.55, cx + r * 2.3, base + 40)
    m = np.maximum(m, rect(W, H, cx - r * 0.82, base - r * 0.95, cx + r * 0.82, base))
    m = np.maximum(m, shapes(W, H, [dome_pts(cx, base - r * 0.95, r * 0.86)]))
    m = np.maximum(m, strokes(W, H, [([(cx, base - r * 2.12), (cx, base - r * 2.3)], 1.4, None)]))
    m = np.maximum(m, crescent(W, H, cx, base - r * 2.36, max(2.4, r * 0.09)))
    if small:
        for s_ in (-1, 1):
            sx = cx + s_ * r * 1.45
            m = np.maximum(m, shapes(W, H, [dome_pts(sx, base - r * 0.55, r * 0.42, peak=1.3)]))
    for s_ in ((-1, 1) if mh else ()):
        m = np.maximum(m, minaret(W, H, cx + s_ * r * side * 1.4, base, mh, mw))
    return m


def mist_fade(arr, y0, y1):
    h = arr.shape[0]
    t = np.clip((np.arange(h, dtype=np.float32) - y0) / max(1, y1 - y0), 0, 1)
    f = 1 - t ** 1.4
    out = arr.copy()
    out[..., 3] *= f[:, None]
    return out


if "sky" in PARTS:
    W, H = 540, 960
    sky = wet_sky(W, H, SKY, seed=31, blooms=0.8)
    # wet-on-wet cloud bands: wide soft strokes of lilac and apricot laid into the damp sky
    for (cy, x0, x1, wd, col, dens) in [(250, -60, 380, 34, "#b8b3d8", 0.28), (330, 200, 620, 26, "#d9b5cf", 0.3),
                                        (430, -60, 300, 22, "#efb9b4", 0.26), (500, 260, 620, 18, "#f6c4a8", 0.3),
                                        (130, 220, 620, 30, "#a8b2d6", 0.22)]:
        m = strokes(W, H, [(curve([(x0, cy), ((x0 + x1) / 2, cy - 12), (x1, cy + 8)], 30), wd, (0.4, 0.5))])
        sky = G(sky, gaussian_filter(m, 6), col, seed=cy, density=dens, edge=0.12, bloom=0.6, rough=14, feather=7, mottle=0.7)
    # the brightening at the horizon
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((xx - W * 0.56) / (W * 0.62)) ** 2 + ((yy - H * 0.72) / (H * 0.16)) ** 2))
    warm = np.array(hex_rgb("#fff0d6"), np.float32)
    sky[..., :3] = sky[..., :3] * (1 - g[..., None] * 0.55) + warm * g[..., None] * 0.55
    preview(sky, "ls-sky")
    save_rgb(sky, f"{OUT}/sky.webp", quality=72)
    clear()

if "skyline" in PARTS:
    W, H = 780, 300
    base = 236
    art = blank(W, H)
    nx = Seq(300)
    # far layer: a wide hall with a big dome in the centre-right, scattered small minarets and domes
    far = mosque(W, H, 470, base - 6, 46, 150, 11, side=1.7)
    for (x, h_, w_) in [(96, 96, 7), (168, 70, 6), (676, 108, 7), (742, 74, 6)]:
        far = np.maximum(far, minaret(W, H, x, base, h_, w_))
    for (x, r) in [(214, 22), (610, 26), (40, 18)]:
        far = np.maximum(far, shapes(W, H, [dome_pts(x, base - 20, r, peak=1.3)]))
        far = np.maximum(far, rect(W, H, x - r * 1.6, base - 20, x + r * 1.6, base + 40))
    far = np.maximum(far, rect(W, H, -10, base - 14, W + 10, H))
    art = G(art, displace(far, 5, 1.2, 20), FAR, FAR2, seed=nx(), density=0.6, edge=0.4, bloom=0.35, rough=2.2, feather=1.4, mottle=0.6, gran=0.3)
    clear()
    # near layer, lower and to the left: a smaller mosque with one tall minaret
    near = rect(W, H, -10, base + 8, W + 10, H)
    near = np.maximum(near, mosque(W, H, 200, base + 12, 30, 0, 0, small=True) * 1.0)
    near = np.maximum(near, minaret(W, H, 288, base + 12, 150, 10))
    near = np.maximum(near, minaret(W, H, 560, base + 14, 58, 6))
    near = np.maximum(near, shapes(W, H, [dome_pts(520, base + 10, 20, peak=1.3)]))
    near = np.maximum(near, rect(W, H, 470, base + 10, 600, H))
    near = np.maximum(near, rect(W, H, 120, base - 8, 290, H))
    art = G(art, displace(near, 9, 1.2, 20), NEAR, NEAR2, seed=nx(), density=0.62, edge=0.45, bloom=0.3, rough=2.0, feather=1.2, mottle=0.5, gran=0.35)
    clear()
    art = mist_fade(art, base - 6, H - 10)
    preview(art, "ls-skyline", bg="#f6d9c4")
    save_full(art, f"{OUT}/skyline.webp", size=(780, 300), quality=80)
    clear()

if "rays" in PARTS:
    W, H = 780, 560
    art = blank(W, H)
    cx, cy = 430, 540
    rng = random.Random(5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    dist = np.hypot(xx - cx, yy - cy)
    field = np.zeros((H, W), np.float32)
    for k in range(9):
        a = -math.pi / 2 + rng.uniform(-1.05, 1.05)
        wd = rng.uniform(0.03, 0.075)
        field = np.maximum(field, np.exp(-((ang - a) / wd) ** 2) * rng.uniform(0.5, 1.0))
    field *= np.clip(1 - dist / 560, 0, 1) ** 1.3
    field = gaussian_filter(field, 3)
    halo = np.exp(-(dist / 170) ** 2)
    a = np.clip(field * 0.62 + halo * 0.6, 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fff3dc"), np.float32)
    rgb = rgb * (1 - halo[..., None] * 0.2) + np.array(hex_rgb("#ffd9a8"), np.float32) * halo[..., None] * 0.2
    art = np.concatenate([rgb, a[..., None]], -1).astype(np.float32)
    preview(art, "ls-rays", bg="#e7c6cf")
    save_full(art, f"{OUT}/rays.webp", size=(780, 560), quality=74)
    clear()

if "divider" in PARTS:
    W, H = 700, 110
    art = blank(W, H)
    nx = Seq(900)
    for (x0, x1, col, y, wd) in [(30, 330, "#c9bfdc", 78, 7), (370, 670, "#f0c3ad", 78, 7)]:
        m = strokes(W, H, [(curve([(x0, y + 2), ((x0 + x1) / 2, y - 3), (x1, y + 1)], 30), wd, (0.6, 0.6))])
        art = G(art, m, col, seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=3, feather=1.4)
    m = shapes(W, H, [dome_pts(350, 80, 20, peak=1.36)])
    m = np.maximum(m, rect(W, H, 326, 80, 374, 86))
    m = np.maximum(m, minaret(W, H, 312, 86, 54, 5))
    m = np.maximum(m, minaret(W, H, 388, 86, 54, 5))
    m = np.maximum(m, strokes(W, H, [([(350, 52), (350, 46)], 1.2, None)]))
    m = np.maximum(m, crescent(W, H, 350, 42, 3))
    art = G(art, m, "#a7a3c8", NEAR2, seed=nx(), density=0.75, edge=0.45, bloom=0.2, rough=1.4, feather=0.9)
    preview(art, "ls-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()

if "sun" in PARTS:
    # small rising sun over a wash of horizon, used for timeline nodes and the countdown
    W, H = 220, 160
    art = blank(W, H)
    nx = Seq(1300)
    art = G(art, circles(W, H, [(110, 100, 46)]), "#fbd3a6", "#f6b99a", seed=nx(), density=0.75, edge=0.55, bloom=0.4, rough=2.5, feather=1.6)
    hz = strokes(W, H, [(curve([(10, 104), (110, 98), (210, 104)], 20), 12, (0.5, 0.5))])
    art = knockout(art, rect(W, H, 0, 104, W, H), amount=1.0, grow=1)
    art = G(art, hz, "#c9bfdc", seed=nx(), density=0.6, edge=0.4, bloom=0.2, rough=3, feather=1.6)
    preview(art, "ls-sun")
    save(art, f"{OUT}/sun.webp", max_w=110, quality=84)
    clear()

if "paper" in PARTS:
    W = H = 320
    n1 = wrap_noise(W, H, 18, 12); n2 = wrap_noise(W, H, 19, 1.4)
    base = col_arr(PAPER)[None, None] * (0.975 + 0.03 * n1[..., None] + 0.035 * (n2[..., None] - 0.5))
    img = np.concatenate([np.clip(base, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/paper.webp", quality=84)
