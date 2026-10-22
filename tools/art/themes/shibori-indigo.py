"""Shibori Indigo — indigo-dyed cotton with shibori resist: itajime (fold & clamp) diamonds, arashi (pole wrap)
diagonal wrinkle stripes, kumo (spider binding) bursts, ori-nui stitched dashes; capillary dye bleed and plain weave.
Run: python3 -I shibori-indigo.py [part ...]
parts: itajime arashi kumo stitch cotton swatch. Assets -> public/themes/art/shibori-indigo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d4_lib import *

OUT = outdir("shibori-indigo")
PARTS = sys.argv[1:] or ["itajime", "arashi", "kumo", "stitch", "cotton", "swatch"]


def opaque(rgb):
    return np.concatenate([rgb, np.ones(rgb.shape[:2] + (1,), np.float32)], -1)


if "itajime" in PARTS:
    n, c = 448, 112
    rng = random.Random(5)
    polys = []
    for i in range(4):
        for j in range(4):
            cx, cy = i * c + c / 2, j * c + c / 2
            d = c * rng.uniform(0.24, 0.3)
            # the clamp block: a diamond, its corners slightly rounded by the press
            pts = [(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)]
            polys.append(deform([(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3)) for x, y in pts], rng, 2, 0.05))
    m = wrap_polys(n, n, polys, smooth=False)
    m = np.clip(gaussian_filter(m, 1.2, mode="wrap") * 1.1, 0, 1)
    # fold lines: pressed layers resist a little along every fold (cell borders + diagonals of the accordion)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    fx = np.abs(((xx / c) % 1) - 0.5) * 2; fy = np.abs(((yy / c) % 1) - 0.5) * 2
    folds = np.clip((fx - 0.965) * 30, 0, 1) + np.clip((fy - 0.965) * 30, 0, 1)
    wob = wrap_noise(n, n, 6, 6)
    folds = np.clip(folds, 0, 1) * (0.35 + 0.35 * wob)
    # small resist dots at the cell corners (pin of the clamp)
    dots_ = wrap_circles(n, n, [(i * c, j * c, 7, 7, 0) for i in range(4) for j in range(4)])
    res = np.clip(np.maximum(m, folds) + gaussian_filter(dots_, 1.5, mode="wrap") * 0.8, 0, 1)
    rgb = dye(n, n, res, 7, wrap=True, bleed=7.0, pitch=2.4, rough=4)
    save_rgb(opaque(rgb), f"{OUT}/itajime.webp", quality=68)
    preview(opaque(rgb), "si-itajime")
    clear()

if "arashi" in PARTS:
    n = 512
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    warp = (wrap_noise(n, n, 21, 14) - 0.5) * 2.6 + (wrap_noise(n, n, 22, 40) - 0.5) * 3.0
    ph = 2 * math.pi * (5 * xx / n + 14 * yy / n) + warp
    ph2 = 2 * math.pi * (5 * xx / n + 14 * yy / n) * 3 + warp * 2.2
    lines = np.clip((np.cos(ph) - 0.72) * 4, 0, 1) * (0.55 + 0.45 * wrap_noise(n, n, 23, 5))
    fine = np.clip((np.cos(ph2) - 0.86) * 5, 0, 1) * 0.45 * wrap_noise(n, n, 24, 8)
    # thread binding: perpendicular faint breaks
    res = np.clip(lines + fine, 0, 1)
    rgb = dye(n, n, res, 25, wrap=True, bleed=3.5, pitch=2.4, depth=1.03)
    save_rgb(opaque(rgb), f"{OUT}/arashi.webp", quality=66)
    preview(opaque(rgb), "si-arashi")
    clear()

if "kumo" in PARTS:
    W = H = 520
    rng = np.random.default_rng(31)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = cy = W / 2
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy) / (W / 2); a = np.arctan2(dy, dx)
    k = 26
    wob = (fbm(W, H, 33, 40, 3) - 0.5) * 0.5
    # radial creases: pinched cloth folds into points → white rays that fade outward
    thr = 0.45 + 0.45 * fbm(W, H, 37, 18, 3)
    rays = np.clip((np.cos(a * k + wob * 9 + r * 2.5) - thr) * 2.5, 0, 1) * np.clip(1 - r * 1.15, 0, 1) ** 0.7
    # binding thread rings
    rings = np.zeros_like(r)
    for rr in (0.18, 0.3, 0.44, 0.58):
        rings += np.clip(1 - np.abs(r + wob * 0.16 - rr) / (0.014 + 0.02 * fbm(W, H, int(rr * 90), 20, 2)), 0, 1) * np.clip((fbm(W, H, int(rr * 100), 14, 2) - 0.25) * 2.5, 0, 1)
    core = np.clip((0.1 + wob * 0.1 - r) * 25, 0, 1)
    res = np.clip(rays * 0.9 + rings * 0.85 + core, 0, 1)
    rgb = dye(W, H, res, 35, wrap=False, bleed=4.0, pitch=2.4, rough=4)
    alpha = np.clip((0.98 - r) * 6, 0, 1) * (0.85 + 0.15 * fbm(W, H, 36, 30, 2))
    alpha = gaussian_filter(alpha, 2)
    art = rgba(rgb, alpha)
    preview(art, "si-kumo", tone=UNDYED)
    save(art, f"{OUT}/kumo.webp", max_w=260, quality=76)
    clear()

if "stitch" in PARTS:
    # ori-nui strip: a band of indigo cloth with wavy stitched resist dashes, frayed ends
    W, H = 680, 96
    rng = random.Random(41)
    st = []
    for row in range(3):
        y0 = 30 + row * 18
        x = 40
        while x < W - 40:
            L = rng.uniform(9, 13)
            y = y0 + math.sin(x / 46 + row * 1.3) * 6
            y2 = y0 + math.sin((x + L) / 46 + row * 1.3) * 6
            st.append(([(x, y), (x + L, y2)], 3.2, None))
            x += L + rng.uniform(6, 9)
    m = strokes(W, H, st)
    rgb = dye(W, H, m, 42, wrap=False, bleed=2.6, pitch=2.2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fray = norm(gaussian_filter(np.random.default_rng(43).random((H, W)).astype(np.float32), (0.5, 9)))
    ends = np.minimum(xx - 14 - fray * 30, W - 14 - fray * 30 - xx)
    top = np.minimum(yy - 12 - fbm(W, H, 44, 50, 2) * 6, H - 12 - fbm(W, H, 45, 50, 2) * 6 - yy)
    a = np.clip(np.minimum(ends / 3, top / 1.5), 0, 1)
    art = rgba(rgb, a)
    preview(art, "si-stitch", tone=UNDYED)
    save(art, f"{OUT}/stitch.webp", max_w=320, quality=80)
    clear()

if "cotton" in PARTS:
    n = 320
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#efede6"), np.float32)
    wv = weave(n, n, 51, 2.6, True)
    base *= (1 + wv[..., None] * 0.035 + (wrap_noise(n, n, 52, 30) - 0.5)[..., None] * 0.03)
    # faint indigo haze from the dye bath
    haze = np.clip((wrap_noise(n, n, 53, 50) - 0.6) * 2, 0, 1)[..., None] * 0.02
    base = base * (1 - haze) + np.array(hex_rgb(INDIGO_L), np.float32) * haze
    save_rgb(opaque(np.clip(base, 0, 1)), f"{OUT}/cotton.webp", quality=66)
    clear()

if "swatch" in PARTS:
    # a folded square of itajime cloth (one clamp diamond) with soft frayed edge: portrait / emblem piece
    W = H = 420
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = cy = W / 2
    d = np.abs(xx - cx) + np.abs(yy - cy)
    dia = np.clip((96 - d) / 3, 0, 1)
    ring = np.clip(1 - np.abs(d - 140) / 4, 0, 1) * 0.5
    fold = (np.clip(1 - np.abs(xx - cx) / 4, 0, 1) + np.clip(1 - np.abs(yy - cy) / 4, 0, 1)) * 0.22
    res = np.clip(dia + ring + fold, 0, 1)
    rgb = dye(W, H, res, 61, wrap=False, bleed=8, pitch=2.4, rough=5)
    fr = norm(gaussian_filter(np.random.default_rng(62).random((H, W)).astype(np.float32), (4, 0.5)))
    fr2 = norm(gaussian_filter(np.random.default_rng(63).random((H, W)).astype(np.float32), (0.5, 4)))
    e = np.minimum(np.minimum(xx - 18 - fr * 10, W - 18 - fr * 10 - xx), np.minimum(yy - 18 - fr2 * 10, H - 18 - fr2 * 10 - yy))
    art = rgba(rgb, np.clip(e / 2, 0, 1))
    preview(art, "si-swatch", tone=UNDYED)
    save(art, f"{OUT}/swatch.webp", max_w=220, quality=78)
    clear()
