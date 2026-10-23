"""Agent I1 helpers (tidore-kadato, mamasa-banua, bata-persia, haul-tahlil): wraps _jw_lib (which brings _j1_lib, _p1_lib,
art) and adds small geometry helpers used by those four scripts. Previews -> /tmp/pen/nb-I1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-I1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def show(arr, name, tone="#f7efe2", bg=None):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def polys(W, H, items):
    """Hard-edged polygons (no smoothing) in one mask."""
    return shapes(W, H, items, smooth=False)


def fade_alpha(arr, y0, y1, top=True):
    """Fade alpha linearly from 0 at y0 to 1 at y1 (top=True) — blends a scene edge into the page."""
    h = arr.shape[0]
    yy = np.arange(h, dtype=np.float32)[:, None]
    k = np.clip((yy - y0) / max(1, (y1 - y0)), 0, 1)
    if not top:
        k = 1 - k
    out = arr.copy()
    out[..., 3] *= (k * k * (3 - 2 * k))
    return out


def tint(mask, col, alpha=1.0):
    """Flat RGBA layer of col with mask alpha (for washes painted via OV)."""
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def edge_of(mask, px=2.0):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def inner_edge(mask, px=1.5):
    return np.clip(mask - gaussian_filter(mask, px) * 1.0, 0, 1) * 2.5


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def lerp(a, b, t):
    return a + (b - a) * t
