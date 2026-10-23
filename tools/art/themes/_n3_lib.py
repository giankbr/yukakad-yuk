"""Agent N3 helpers (batang-garing, delima-merah, mesin-ketik, ultah-kemah). Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses, spiral_pts, along ...). Previews -> /tmp/pen/nb-N3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-N3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, a=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask * a)


def tint(dst, mask, col, a=1.0, blur=0.0, pad=16):
    """Soft opaque-ish colour layer (shadows / highlights) composited over."""
    m = gaussian_filter(mask, blur) if blur else mask
    return OV(dst, m, lambda mm: flat(mm, col, a), pad=pad + int(blur * 3))


def below(H, y, soft=40.0):
    return np.clip((np.arange(H, dtype=np.float32)[:, None] - y) / soft, 0, 1)


def above(H, y, soft=40.0):
    return 1 - below(H, y, soft)


def right_of(W, x, soft=30.0):
    return np.clip((np.arange(W, dtype=np.float32)[None, :] - x) / soft, 0, 1)


def edge_ring(mask, r=1.5):
    """Thin dark outline from a mask (inner rim)."""
    return np.clip((mask - gaussian_filter(mask, r)) * 3.0, 0, 1)


def outline_out(mask, r=2.0):
    g = (gaussian_filter((mask > 0.5).astype(np.float32), r) > 0.06).astype(np.float32)
    return np.clip(g - (mask > 0.5), 0, 1)


def ink(dst, mask, col="#1b1510", seed=1, wear=0.2, rough=1.2):
    return LC(dst, mask, col, seed=seed, wear=wear, rough=rough)


def poly_mask(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def rr_mask(W, H, x0, y0, x1, y1, r):
    def draw(cv):
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def rot(pts, cx, cy, a):
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def stars_field(W, H, n, seed, rmin=0.6, rmax=1.8, ymax=None):
    rng = random.Random(seed)
    items = []
    for _ in range(n):
        items.append((rng.uniform(0, W), rng.uniform(0, ymax or H), rng.uniform(rmin, rmax) ** 1.0))
    return circles(W, H, items)


def wrap_tile(arr_rgb):
    """Blend an RGB float tile with its half-offset copy so it repeats seamlessly."""
    h, w = arr_rgb.shape[:2]
    sh = np.roll(np.roll(arr_rgb, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = np.minimum(xx, w - 1 - xx) / (w / 2); wy = np.minimum(yy, h - 1 - yy) / (h / 2)
    k = np.clip(np.minimum(wx, wy) * 1.8, 0, 1)[..., None]
    return arr_rgb * k + sh * (1 - k)
