"""Agent A5 helpers (deco-sampanye, terrazzo-modern, sakura-sumi, herbarium-klasik): builds on _j1_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds sumi ink, emboss/deboss, seamless tile helpers, tape strips.
Previews -> /tmp/pen/nb-A5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-A5/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-A5/art"
_j1_lib.PREV = _p1_lib.PREV
import art as _art
PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def rgb_arr(h, w, col):
    return np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)


def layer(mask, col, alpha=1.0):
    """Flat-colour RGBA from a mask (use only under media textures, never alone)."""
    h, w = mask.shape
    return np.concatenate([rgb_arr(h, w, col), (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def emboss_light(mask, depth=1.0, blur=1.6, ang=(-0.7, -0.7)):
    """Return (highlight, shadow) fields of a pressed shape lit from the upper left."""
    m = gaussian_filter(mask, blur)
    gy, gx = np.gradient(m)
    d = -(gx * ang[0] + gy * ang[1]) * depth * 6
    return np.clip(d, 0, 1), np.clip(-d, 0, 1)


def ink(dst, mask, seed, col="#1b1816", col2="#3b3632", density=0.94, bleed=0.22, dry=0.35, rough=2.5, gran=0.3, pad=26):
    """Sumi ink stroke: dark core with wet-edge pooling, a soft grey bleed halo into the paper fibres, dry-brush breaks."""
    if bleed:
        halo = np.clip(gaussian_filter(mask, 3.5) * 1.4, 0, 1)
        dst = G(dst, halo, mix(col, "#9a948c", 0.55), seed=seed + 3, density=bleed, edge=0.25, bloom=0.4, rough=5, feather=2.0, pad=pad)
    if dry:
        h, w = mask.shape
        st = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.8, 3.0))
        st = (st - st.min()) / (st.max() - st.min() + 1e-6)
        edge = np.clip(mask - gaussian_filter(mask, 2.5), 0, 1) * 2 + 0.25
        mask = mask * (1 - np.clip((st - (1 - dry * 0.5)) * 6, 0, 1) * np.clip(edge, 0, 1))
    return G(dst, mask, col, col2, seed=seed, density=density, edge=0.6, bloom=0.08, gran=gran, rough=rough, feather=0.9, pad=pad)


def wrap_circles(w, h, items):
    """Circles/ellipses drawn with wrap-around (seamless tiles). items: (x, y, rx, ry, rot_deg)."""
    out = []
    for x, y, rx, ry, rot in items:
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                X, Y = x + dx, y + dy
                if -rx - 4 < X < w + rx + 4 and -rx - 4 < Y < h + rx + 4:
                    out.append((X, Y, rx, ry, rot))
    return ellipses(w, h, out)


def wrap_polys(w, h, polys, smooth=True):
    out = []
    for pts in polys:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                if max(xs) + dx < -2 or min(xs) + dx > w + 2 or max(ys) + dy < -2 or min(ys) + dy > h + 2:
                    continue
                out.append([(x + dx, y + dy) for x, y in pts])
    return shapes(w, h, out, smooth=smooth)


def chip_poly(rng, x, y, r, n=None):
    """Irregular angular terrazzo chip."""
    n = n or rng.randint(5, 8)
    a0 = rng.uniform(0, math.tau)
    pts = []
    for k in range(n):
        a = a0 + k * math.tau / n + rng.uniform(-0.35, 0.35)
        rr = r * rng.uniform(0.55, 1.0)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr * rng.uniform(0.7, 1.0)))
    return pts


def tape(W, H, seed, col="#e8dcc0", alpha=0.62):
    """Paper masking tape strip with torn ends, translucent, faint crepe texture."""
    rng = random.Random(seed)
    top = [(12 + i * (W - 24) / 12, 8 + rng.uniform(-1.2, 1.2)) for i in range(13)]
    right = [(W - 12 + rng.uniform(-6, 6), 8 + i * (H - 16) / 8) for i in range(1, 8)]
    bot = [(W - 12 - i * (W - 24) / 12, H - 8 + rng.uniform(-1.2, 1.2)) for i in range(13)]
    left = [(12 + rng.uniform(-6, 6), H - 8 - i * (H - 16) / 8) for i in range(1, 8)]
    m = shape_mask(W, H, top + right + bot + left, smooth=False)
    m = np.clip(gaussian_filter(m, 0.6), 0, 1)
    crepe = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (0.5, 7))
    crepe = (crepe - crepe.mean()) / (crepe.std() + 1e-6)
    rgb = rgb_arr(H, W, col) * (1 + crepe[..., None] * 0.035)
    a = m * alpha * (0.92 + 0.08 * fbm(W, H, seed, 30, 2))
    edge = np.clip(m - gaussian_filter(m, 2.0), 0, 1)
    a = np.clip(a + edge * 0.25, 0, 1)
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def along(pts, step):
    """Resample a polyline at roughly fixed arc length; returns [(x, y, angle)]."""
    out = []; acc = step / 2
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out
