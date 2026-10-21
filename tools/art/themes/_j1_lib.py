"""Agent J1 helpers (joglo-marun, kawung-biru): _p1_lib + local (bbox-cropped) painting, batched stroke masks,
hatching, bounded fbm cache. Previews -> /tmp/pen/nj-J1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nj-lead"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _p1_lib import *  # noqa
import art as _art
PREV = _p1_lib.PREV


def trim_cache():
    if len(_art._fbm_cache) > 10:
        _art._fbm_cache.clear()


def bbox(mask, pad=24, thr=0.004):
    ys, xs = np.where(mask > thr)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def _apply(dst, mask, fn, mode, pad):
    trim_cache()
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    src = fn(np.ascontiguousarray(mask[y0:y1, x0:x1]))
    out = dst.copy()
    out[y0:y1, x0:x1] = (glaze if mode == "glaze" else over)(dst[y0:y1, x0:x1], src)
    return out


def G(dst, mask, *a, pad=24, **k):
    """glaze a watercolour pigment(mask, *a, **k) onto dst, computed only inside the mask bbox."""
    return _apply(dst, mask, lambda m: pigment(m, *a, **k), "glaze", pad)


def GP(dst, mask, *a, pad=16, **k):
    """over: gouache_paint locally."""
    return _apply(dst, mask, lambda m: gouache_paint(m, *a, **k), "over", pad)


def LC(dst, mask, *a, pad=12, **k):
    return _apply(dst, mask, lambda m: linocut(m, *a, **k), "over", pad)


def FO(dst, mask, *a, pad=12, **k):
    return _apply(dst, mask, lambda m: foil(m, *a, **k), "over", pad)


def OV(dst, mask, fn, pad=16):
    return _apply(dst, mask, fn, "over", pad)


def strokes(w, h, items, cap=True):
    """items: list of (pts, width[, taper]) tapered brush strokes drawn into ONE mask (fast)."""
    cv = Canvas(w, h)
    for it in items:
        pts, width = it[0], it[1]
        taper = it[2] if len(it) > 2 else (0.15, 0.25)
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            if taper is None:
                kk = 1.0
            else:
                kk = min(1.0, t / taper[0]) if (taper[0] and t < taper[0]) else (min(1.0, (1 - t) / taper[1]) if (taper[1] and t > 1 - taper[1]) else 1.0)
            wd = max(0.5, width * (0.25 + 0.75 * kk))
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wd, Style=skia.Paint.kStroke_Style,
                           StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
            cv.c.drawLine(*pts[i], *pts[i + 1], p)
    return cv.array()[..., 3]


def shapes(w, h, polys, smooth=True):
    """Many filled polygons into one mask."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for pts in polys:
        cv.c.drawPath(smooth_path(pts) if smooth else poly_path(pts), p)
    return cv.array()[..., 3]


def circles(w, h, items):
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for x, y, r in items:
        cv.c.drawCircle(x, y, r, p)
    return cv.array()[..., 3]


def ellipses(w, h, items):
    """items: (cx, cy, rx, ry, rot_deg)"""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for cx, cy, rx, ry, rot in items:
        cv.c.save(); cv.c.translate(cx, cy); cv.c.rotate(rot)
        cv.c.drawOval(skia.Rect(-rx, -ry, rx, ry), p)
        cv.c.restore()
    return cv.array()[..., 3]


def hatch(w, h, angle=0.6, spacing=4.0, width=0.42, seed=1, wob=1.2):
    """Line field (0..1) of parallel engraved lines; width = duty (0..1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = (fbm(w, h, seed, 30, 2) - 0.5) * wob * 2
    u = (xx * math.cos(angle) + yy * math.sin(angle) + n) / spacing
    f = np.abs((u % 1.0) - 0.5) * 2  # 0 at line centre
    return np.clip((width - f) / 0.18 + 0.5, 0, 1).astype(np.float32)


def engrave(mask, tone, angle=0.6, spacing=4.0, seed=1, cross=0.6):
    """Engraved shading: line duty follows tone (0 light .. 1 dark); cross-hatch where tone > cross."""
    h, w = mask.shape
    l1 = hatch(w, h, angle, spacing, 0.15 + 0.55 * tone, seed)
    out = l1
    if cross is not None:
        l2 = hatch(w, h, angle + 1.2, spacing * 1.1, 0.12 + 0.6 * np.clip((tone - cross) / (1 - cross + 1e-6), 0, 1), seed + 3)
        out = np.maximum(l1, l2 * (tone > cross))
    return out * mask * np.clip(tone * 3, 0, 1)


def mirror(arr):
    return arr[:, ::-1].copy()
