"""Agent F1 helpers (kutai-erau, bima-mbojo, simalungun-bolon, mandailing-gordang).
Builds on _d1_lib (thread-level loom ikat(), check weave, local-crop G/GP/LC/FO/OV, strokes/shapes, thatch_strokes)
and the adat-Jawa carving helpers in _jw_lib (carve, lung, along, spiral_pts, hills). Adds:
  sea_strokes()   horizontal ripple strokes for calm water (longer toward the viewer)
  check_design()  tartan/check index map (warp + weft stripe bands) for tembe nggoli
  solid_rgba()    flat colour layer helper
  tint()          multiply a coloured wash over a region (shadow / light side)
  posts()         stilt posts mask list
Previews -> /tmp/pen/nb-F1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _d1_lib import *  # noqa
import _d1_lib, _j1_lib
import _jw_lib
from _jw_lib import carve, lung, along, spiral_pts, hills, _trap  # noqa
PREV = "/tmp/pen/nb-F1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_d1_lib.PREV = PREV
import numpy as np
from scipy.ndimage import gaussian_filter


def prev_rgb(rgb, name):  # noqa: F811
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def preview(arr, name, tone="#fbf6e4", bg=None):  # noqa: F811
    if bg:
        h, w = arr.shape[:2]
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def sea_strokes(W, H, y0, y1, rng, n=220, length=(20, 90), width=(0.8, 2.4)):
    items = []
    for _ in range(n):
        t = rng.random() ** 1.4
        y = y0 + (y1 - y0) * t
        x = rng.uniform(-40, W + 40)
        L = (length[0] + (length[1] - length[0]) * (0.3 + 0.7 * t)) * rng.uniform(0.6, 1.3)
        wv = width[0] + (width[1] - width[0]) * t
        items.append(([(x, y), (x + L * 0.5, y + rng.uniform(-0.6, 0.6)), (x + L, y + rng.uniform(-0.8, 0.8))], wv, (0.3, 0.4)))
    return strokes(W, H, items)


def check_design(N, bands, base, M=None):
    """Check index map: (start, end, idx) bands applied to warp and weft; crossings keep the warp band unless base."""
    M = M or N
    D = np.full((M, N), base, np.int32)
    for (a, b, k) in bands:
        if a < N:
            D[:, a:min(b, N)] = k
    for (a, b, k) in bands:
        if a < M:
            D[a:min(b, M), :] = np.where(D[a:min(b, M), :] == base, k, D[a:min(b, M), :])
    return D


def solid_rgba(mask, col, a=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * C(col), mask * a)


def tint(art, mask, col, amt):
    """Lay a thin transparent wash (no wet edge) over mask: shading / glow."""
    return over(art, solid_rgba(np.clip(mask, 0, 1), col, amt))


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def lin(W, H, items, w=1.5):
    """Straight segments [(x0,y0,x1,y1)] as one stroke mask."""
    return strokes(W, H, [([(a, b), (c, d)], w, None) for (a, b, c, d) in items])
