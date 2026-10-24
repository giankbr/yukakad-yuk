"""Agent Q4 helpers (gamelan, orosi-kashan, ikebana, anniversary-pertama).
Builds on _jw_lib (-> _j1_lib -> _p1_lib -> art). Previews -> /tmp/pen/nb-Q4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-Q4/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
_p1_lib.PREV = "/tmp/pen/nb-Q4/art"

PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def rect(W, H, x0, y0, x1, y1, r=0.0):
    def draw(cv):
        cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def lines(W, H, segs, width, cap=True):
    """Straight segments ((x0,y0),(x1,y1)) at one width, one mask."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kSquare_Cap)
    for a, b in segs:
        cv.c.drawLine(a[0], a[1], b[0], b[1], p)
    return cv.array()[..., 3]


def streaks(h, w, seed, sx=0.6, sy=6.0):
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (sy, sx))
    return (s - s.mean()) / (s.std() + 1e-6)


def shaded(mask, base, lit, dark, cx, cy, rx, ry, seed=1, light=(-0.55, -0.7), spec=0.0, spec_col="#fff3d0",
           streak=0.6, rough=1.6, hammer=0.0):
    """Opaque painted volume: colour follows a lit-sphere normal over an ellipse (cx,cy,rx,ry) inside mask.
    Gouache-like edge + brush streaks; `hammer` adds hand-hammered bronze dimples; `spec` a soft painted highlight."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 24)
    m = np.clip((gaussian_filter(m, 0.7) - 0.3) * 2.4, 0, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx - cx) / max(rx, 1); v = (yy - cy) / max(ry, 1)
    d2 = np.clip(u * u + v * v, 0, 1)
    nz = np.sqrt(1 - d2)
    lx, ly = light; lz = math.sqrt(max(0.05, 1 - lx * lx - ly * ly))
    lam = np.clip(u * lx + v * ly + nz * lz, 0, 1)
    if hammer:
        hm = fbm(w, h, seed + 31, 7, 2) - 0.5
        lam = np.clip(lam + hm * hammer, 0, 1)
    cb, cl, cd = (np.array(hex_rgb(c), np.float32) for c in (base, lit, dark))
    t = lam[..., None]
    rgb = np.where(t > 0.5, cb + (cl - cb) * ((t - 0.5) * 2), cd + (cb - cd) * (t * 2))
    drift = fbm(w, h, seed + 5, 60, 3)[..., None] - 0.5
    rgb = rgb * (1 + drift * 0.12)
    if streak:
        rgb = rgb * (1 + streaks(h, w, seed + 9)[..., None] * 0.03 * streak)
    if spec:
        sp = np.clip(lam - 0.86, 0, 1) / 0.14
        sp = gaussian_filter(sp, 2.0) * spec
        sc = np.array(hex_rgb(spec_col), np.float32)
        rgb = rgb * (1 - sp[..., None]) + sc * sp[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def SH(dst, mask, *a, pad=10, **k):
    """over: shaded() computed in the mask bbox (cx, cy are given in full-canvas coords)."""
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    k = dict(k)
    args = list(a)
    # shift centre into the crop
    base, lit, dark, cx, cy, rx, ry = args[:7]
    src = shaded(np.ascontiguousarray(mask[y0:y1, x0:x1]), base, lit, dark, cx - x0, cy - y0, rx, ry, *args[7:], **k)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    trim_cache()
    return out


def tint(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def T(dst, mask, col, alpha=1.0, blur=0.0):
    m = gaussian_filter(mask, blur) if blur else mask
    return over(dst, tint(m, col, alpha))


def _shift(a, dx, dy):
    out = np.zeros_like(a)
    h, w = a.shape
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    out[yd, xd] = a[ys, xs]
    return out


def shadow(dst, mask, col="#000000", blur=8, strength=0.45, dx=4, dy=6):
    """Soft drop shadow (no wrap-around, unlike soft_shadow)."""
    m = _shift(gaussian_filter(mask, blur), int(dx), int(dy)) * strength
    return over(dst, tint(np.clip(m, 0, 1), col, 1.0))


def under(dst, src):
    """Composite src *behind* dst."""
    return over(src, dst)


def cutpaper(mask, col, col2=None, seed=1, edge_light=0.35, rough=1.2, fibre=0.5):
    """Cut/folded paper: matte flat colour with paper fibre, a slightly lighter cut edge, tiny edge wobble."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 14)
    m = np.clip((gaussian_filter(m, 0.6) - 0.35) * 2.6, 0, 1)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 3, 120, 2)[..., None]
    rgb = ca * (1 - t) + cb * t
    fib = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.5, 2.2))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    rgb = rgb * (1 + fib[..., None] * 0.025 * fibre)
    e = np.clip(m - gaussian_filter(m, 1.6), 0, 1) * 2.5
    rgb = rgb + (1 - rgb) * (e[..., None] * edge_light)
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def CP(dst, mask, *a, pad=8, **k):
    return OV(dst, mask, lambda m: cutpaper(m, *a, **k), pad=pad)


def fold_shade(mask, p0, p1, side_dark=0.18, soft=1.0):
    """Darken one side of a fold line p0->p1 inside mask (returns alpha mask for a dark glaze)."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    s = (xx - p0[0]) * dy - (yy - p0[1]) * dx
    side = (s > 0).astype(np.float32)
    return gaussian_filter(side, soft) * mask * side_dark


def sumi(dst, pts, width, col="#2a2724", seed=1, alpha=0.92, dry=0.35, taper=(0.12, 0.3)):
    """Sumi-e brush stroke: tapered stroke with dry-brush streaking along its length."""
    h, w = dst.shape[:2]
    m = stroke_mask(w, h, pts, width, taper)
    def f(mm):
        hh, ww = mm.shape
        md = displace(mm, seed, 1.4, 12)
        md = np.clip((gaussian_filter(md, 0.5) - 0.3) * 2.2, 0, 1)
        if dry:
            n = fbm(ww, hh, seed + 2, 5, 2)
            edge = np.clip(1 - gaussian_filter(mm, 2.0) * 1.6, 0, 1)
            md = md * (1 - dry * np.clip((n - 0.62) * 4, 0, 1) * (0.35 + 0.65 * edge))
        rgb = np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
        tone = 0.85 + 0.3 * fbm(ww, hh, seed + 4, 30, 2)
        rgb = rgb * tone[..., None]
        return np.concatenate([np.clip(rgb, 0, 1), (md * alpha)[..., None]], -1)
    return OV(dst, m, f, pad=8)


def rgb_bg(w, h, col):
    return solid(w, h, col)


def save_opaque(arr, path, size=None, quality=74):
    return save_rgb(arr, path, size=size, quality=quality)
