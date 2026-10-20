"""Agent P7 helpers on top of art.py (art.py itself is not edited)."""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
import art as _art
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


def on_color(arr, hexcol):
    h, w = arr.shape[:2]
    bg = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(hexcol), np.float32)
    a = arr[..., 3:4]
    return Image.fromarray((np.clip(bg * (1 - a) + arr[..., :3] * a, 0, 1) * 255).astype(np.uint8), "RGB")


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


def strokes_mask(w, h, strokes, taper=(0.18, 0.3)):
    """strokes: [(pts, width)] tapered brush strokes merged into one mask."""
    def draw(cv):
        for pts, width in strokes:
            n = len(pts)
            for i in range(n - 1):
                t = i / max(1, n - 2)
                k = min(1.0, t / taper[0]) if t < taper[0] else (min(1.0, (1 - t) / taper[1]) if t > 1 - taper[1] else 1.0)
                wdt = max(0.6, width * (0.2 + 0.8 * k))
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style,
                               StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(*pts[i], *pts[i + 1], p)
    return mask_from(w, h, draw)


def lines_mask(w, h, segs, width, closed=False):
    """even-width polylines (hairlines, hatching, ink outlines)."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        for pts in segs:
            path = skia.Path(); path.moveTo(*pts[0])
            for q in pts[1:]:
                path.lineTo(*q)
            if closed:
                path.close()
            cv.c.drawPath(path, p)
    return mask_from(w, h, draw)


def poly_mask(w, h, polys):
    """several straight-edged polygons merged into a mask."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for pts in polys:
            cv.c.drawPath(poly_path(pts), p)
    return mask_from(w, h, draw)


def rrect_pts(x, y, w, h, r, n=6):
    """rounded-rectangle outline as points (for deform / smooth_path)."""
    pts = []
    for cx, cy, a0 in [(x + w - r, y + r, -math.pi / 2), (x + w - r, y + h - r, 0), (x + r, y + h - r, math.pi / 2), (x + r, y + r, math.pi)]:
        for i in range(n):
            a = a0 + (math.pi / 2) * i / (n - 1)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def ink(mask, col, seed=1, alpha=0.9, bleed=0.6):
    """ink line: slight bleed into the paper, uneven density."""
    h, w = mask.shape
    m = gaussian_filter(mask, bleed)
    tone = 0.75 + 0.25 * fbm(w, h, seed + 2, 12, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(m * tone * alpha, 0, 1))[..., None]], -1)


def kb(path):
    return os.path.getsize(path) / 1024


_pigment_full = _art.pigment
_gouache_full = _art.gouache_paint


def _bbox(mask, pad):
    ys, xs = np.nonzero(mask > 0.002)
    if len(ys) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def pigment(mask, col_a, col_b=None, seed=1, **kw):
    """art.pigment computed on the mask's bounding box (fast, low memory), cache-clearing."""
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


def gouache_paint(mask, col, col2=None, seed=1, **kw):
    pad = int(kw.get("rough", 3.5) * 2 + 14)
    bb = _bbox(mask, pad)
    h, w = mask.shape
    out = np.zeros((h, w, 4), np.float32)
    if bb is None:
        return out
    y0, y1, x0, x1 = bb
    out[y0:y1, x0:x1] = _gouache_full(mask[y0:y1, x0:x1], col, col2, seed=seed, **kw)
    _art._fbm_cache.clear()
    return out


def paper_rgba(w, h, tone, seed=3, fiber=0.5, mottle=0.5):
    bg = np.asarray(paper(w, h, tone, seed, fiber, mottle), np.float32) / 255
    return np.concatenate([bg, np.ones((h, w, 1), np.float32)], -1)


def multiply_onto(dst, src):
    """lay a translucent layer with multiply blend (paint on paper)."""
    sa = src[..., 3:4]
    rgb = dst[..., :3] * (1 - sa) + dst[..., :3] * src[..., :3] * sa
    out = dst.copy(); out[..., :3] = np.clip(rgb, 0, 1)
    return out


def clear_cache():
    _art._fbm_cache.clear()
