"""Agent L1 helpers (baju-bodo, gorga-toba, wisteria-syari, ultah-balap). Builds on _jw_lib (G/GP/LC/FO, strokes,
shapes, circles, ellipses, hatch...). Previews -> /tmp/pen/nb-L1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-L1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def tint(mask, col, a=1.0):
    """Flat RGBA layer (for subtle highlights via OV)."""
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * a, 0, 1)[..., None]], -1)


def lift(mask, dx, dy):
    return np.roll(np.roll(mask, dy, 0), dx, 1)


def bezier(p0, p1, p2, n=30):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / (n - 1) for i in range(n)]]


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect_mask(W, H, x0, y0, x1, y1, r):
    def draw(cv):
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def opaque_on(arr, col):
    """Composite onto a flat colour (opaque result)."""
    h, w = arr.shape[:2]
    return over(solid(w, h, col), arr)
