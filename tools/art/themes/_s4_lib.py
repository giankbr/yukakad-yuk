"""Agent S4 helpers (danau-maninjau, bintang-duabelas, film-noir, lomba-layangan).
Builds on _g1_lib (G/GP/LC/FO/OV crops, strokes/shapes/ellipses, brushwork, mist, ygrad/xgrad, rgb_save).
Adds: rgba save with trim, Hankin star construction, ink-wash helpers. Previews -> /tmp/pen/nb-S4/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _g1_lib, _p1_lib, _j1_lib, _d1_lib, _f2_lib
from _g1_lib import *  # noqa
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter

PREV = "/tmp/pen/nb-S4/art"
os.makedirs(PREV, exist_ok=True)
_g1_lib.PREV = _p1_lib.PREV = _j1_lib.PREV = _d1_lib.PREV = _f2_lib.PREV = PREV


def prev_rgb(rgb, name):  # noqa: F811
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def prev_rgba(arr, name, bg="#f4efe4"):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def save_a(arr, path, max_w=None, quality=82):
    size = save_asset(arr, path, max_w=max_w, quality=quality)
    print(os.path.basename(path), size, os.path.getsize(path) // 1024, "KB")
    return size


def save_rgb(rgb, path, size=None, quality=78):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size


def solid_layer(mask, col, alpha=1.0):
    h, w = mask.shape
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def regular_poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + k * math.tau / n), cy + r * math.sin(rot + k * math.tau / n)) for k in range(n)]


def _isect(p, d, q, e):
    """Intersection of p + t d and q + s e."""
    den = d[0] * e[1] - d[1] * e[0]
    if abs(den) < 1e-9:
        return None
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return (p[0] + d[0] * t, p[1] + d[1] * t)


def hankin(poly, theta):
    """Polygons-in-contact (Hankin) construction: for every edge midpoint two rays at `theta` to the edge; ray towards
    vertex v_{i+1} from mid_i meets the mirrored ray from mid_{i+1}. Returns list of polylines [mid_i, P, mid_{i+1}]."""
    n = len(poly)
    cx = sum(p[0] for p in poly) / n; cy = sum(p[1] for p in poly) / n
    out = []
    for i in range(n):
        a, b, c = poly[i], poly[(i + 1) % n], poly[(i + 2) % n]
        m1 = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        m2 = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
        # edge a->b direction, rotate inward by theta (inward = towards centre)
        ex, ey = b[0] - a[0], b[1] - a[1]; L = math.hypot(ex, ey); ex /= L; ey /= L
        nxv, nyv = -ey, ex
        if (cx - m1[0]) * nxv + (cy - m1[1]) * nyv < 0:
            nxv, nyv = -nxv, -nyv
        d1 = (ex * math.cos(theta) + nxv * math.sin(theta), ey * math.cos(theta) + nyv * math.sin(theta))
        fx, fy = c[0] - b[0], c[1] - b[1]; L2 = math.hypot(fx, fy); fx /= L2; fy /= L2
        n2x, n2y = -fy, fx
        if (cx - m2[0]) * n2x + (cy - m2[1]) * n2y < 0:
            n2x, n2y = -n2x, -n2y
        d2 = (-fx * math.cos(theta) + n2x * math.sin(theta), -fy * math.cos(theta) + n2y * math.sin(theta))
        P = _isect(m1, d1, m2, d2)
        if P:
            out.append([m1, P, m2])
    return out
