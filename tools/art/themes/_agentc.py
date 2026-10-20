"""Agent C helpers on top of art.py (no edits to art.py)."""
import sys, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
import numpy as np


def save_full(arr, path, size=None, quality=82):
    """Save WITHOUT trimming (layout depends on the canvas box)."""
    im = to_image(arr)
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def save_opaque(arr, path, size=None, quality=80):
    im = to_image(arr).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def tileable_x(arr, ov):
    """arr is (h, W+ov, 4) → (h, W, 4) seamless horizontally by cross-fading the overflow into the start."""
    W = arr.shape[1] - ov
    out = arr[:, :W].copy()
    t = np.linspace(0, 1, ov, dtype=np.float32)[None, :, None]
    out[:, :ov] = arr[:, W:W + ov] * (1 - t) + arr[:, :ov] * t
    return out


def tileable_xy(arr, ov):
    a = tileable_x(arr, ov)
    a = np.transpose(a, (1, 0, 2))
    a = tileable_x(a, ov)
    return np.transpose(a, (1, 0, 2))


def on_color(arr, hexcol):
    h, w = arr.shape[:2]
    bg = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(hexcol), np.float32)
    a = arr[..., 3:4]
    return Image.fromarray((np.clip(bg * (1 - a) + arr[..., :3] * a, 0, 1) * 255).astype(np.uint8), "RGB")


def on_bg(arr, bg_rgba):
    out = over(bg_rgba, arr)
    return Image.fromarray((np.clip(out[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")


def scale_alpha(arr, k):
    out = arr.copy()
    out[..., 3] = np.clip(out[..., 3] * k, 0, 1)
    return out


def circle_mask(w, h, cx, cy, r):
    def draw(cv):
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def dots_mask(w, h, pts):
    """pts: [(x, y, r)]"""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in pts:
            cv.c.drawCircle(x, y, r, p)
    return mask_from(w, h, draw)


def strokes_mask(w, h, strokes):
    """strokes: [(pts, width)] tapered brush strokes merged into one mask."""
    def draw(cv):
        for pts, width in strokes:
            n = len(pts)
            for i in range(n - 1):
                t = i / max(1, n - 2)
                k = min(1.0, t / 0.18) if t < 0.18 else (min(1.0, (1 - t) / 0.3) if t > 0.7 else 1.0)
                wdt = max(0.6, width * (0.2 + 0.8 * k))
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style,
                               StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(*pts[i], *pts[i + 1], p)
    return mask_from(w, h, draw)


def lines_mask(w, h, segs, width):
    """even-width polylines (hairlines, hatching)."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        for pts in segs:
            path = skia.Path(); path.moveTo(*pts[0])
            for q in pts[1:]:
                path.lineTo(*q)
            cv.c.drawPath(path, p)
    return mask_from(w, h, draw)


def kb(path):
    import os
    return os.path.getsize(path) / 1024


import art as _art
_pigment_full = _art.pigment


def _bbox(mask, pad):
    ys, xs = np.nonzero(mask > 0.002)
    if len(ys) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def pigment(mask, col_a, col_b=None, seed=1, **kw):
    """Same as art.pigment but computed on the mask's bounding box (fast, low memory) and cache-clearing."""
    pad = int(kw.get("rough", 7.0) * 2 + kw.get("feather", 1.6) * 4 + 14)
    bb = _bbox(mask, pad)
    h, w = mask.shape
    out = np.zeros((h, w, 4), np.float32)
    if bb is None:
        return out
    y0, y1, x0, x1 = bb
    out[y0:y1, x0:x1] = _pigment_full(mask[y0:y1, x0:x1], col_a, col_b, seed=seed, **kw)
    _art._fbm_cache.clear()
    return out


def clear_cache():
    _art._fbm_cache.clear()
