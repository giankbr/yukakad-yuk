"""Agent J3 helpers (wayang-mega, kereta-kencana): re-exports _p1_lib with previews in /tmp/pen/nj-J3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nj-J3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _p1_lib import *  # noqa
from scipy.ndimage import distance_transform_edt, binary_erosion  # noqa
PREV = _p1_lib.PREV

import art as _art
_over, _glaze = over, glaze


def trim_cache():
    if len(_art._fbm_cache) > 10:
        _art._fbm_cache.clear()


def over(dst, src):  # noqa: F811
    trim_cache()
    return _over(dst, src)


def glaze(dst, src):  # noqa: F811
    trim_cache()
    return _glaze(dst, src)


def edge(mask, width=1.6):
    """Contour line of a mask (for ink outlines)."""
    m = np.clip(mask, 0, 1)
    return np.clip((m - gaussian_filter(m, width)) * 3.2, 0, 1)


def outline(mask, width=2.0):
    """Outer contour (just outside+on the edge)."""
    g = gaussian_filter(np.clip(mask, 0, 1), width)
    return np.clip(np.minimum(g, 1 - g) * 4.5, 0, 1) * (g > 0.05)


def ink(mask, col="#2a1a10", seed=1, density=0.9):
    return linocut(np.clip(mask, 0, 1), col, seed=seed, wear=0.25, rough=0.6) * np.array([1, 1, 1, density], np.float32)


def holes_cut(arr, holes, amount=0.92):
    out = arr.copy()
    out[..., 3] *= 1 - np.clip(holes, 0, 1) * amount
    return out


def dots_along(w, h, pts, r, every=1, jit=0.0, rng=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for i, (x, y) in enumerate(pts):
            if i % every:
                continue
            j = (rng.gauss(0, jit) if rng else 0)
            cv.c.drawCircle(x + j, y + j, r, p)
    return mask_from(w, h, draw)


def resample(pts, step):
    """Evenly spaced points along a polyline."""
    out = [pts[0]]; need = step
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        pos = 0.0
        while d - pos >= need:
            pos += need
            t = pos / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
            need = step
        need -= d - pos
    return out


def offset_poly(pts, cx, cy, k):
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]


def spiral(cx, cy, r0, r1, a0, turns, n=60, ccw=1):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + ccw * t * turns * math.tau
        r = r0 + (r1 - r0) * t
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def flip(arr):
    return arr[:, ::-1].copy()
