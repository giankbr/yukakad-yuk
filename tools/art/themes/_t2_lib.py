"""Agent T2 helpers (keraton-sumenep, dallah-kopi, air-terjun, ultah-anjing): _g2_lib (bbox-local gouache, crayon,
tint, wood grain) + _jw_lib carving, plus a few own helpers (paint body with light/shadow + crayon edge, metal
shading, opaque scene compositing). Previews -> /tmp/pen/nb-T2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _g2_lib import *  # noqa
from _jw_lib import lung, carve, spiral_pts, along, hills, palm  # noqa
import _p1_lib, _j1_lib, _g2_lib
import art as _art
PREV = "/tmp/pen/nb-T2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_g2_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def body(art, m, col, col2, dark, light, nx, ldir=(-12, -14), blur=9, outline=None, line_amt=0.8, rough=1.4):
    """Gouache shape with soft shadow/light sides and an optional crayon outline."""
    art = GP(art, m, col, col2, seed=nx(), rough=rough, streak=0.45)
    art = tint(art, side_light(m, *ldir, blur), dark, 0.7, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .7, -ldir[1] * .7, blur * .8), light, 0.45, seed=nx())
    if outline:
        art = crayon(art, inner_edge(m, 2.0), outline, seed=nx(), amt=line_amt, tooth=0.25)
    return art


def metal(art, m, base, hi, lo, nx, axis_x=None, bands=3.0, amt=0.75):
    """Polished brass/copper: vertical reflection bands across the shape (cylindrical look) + gouache base."""
    b = bbox(m, 2)
    if b is None:
        return art
    y0, y1, x0, x1 = b
    art = GP(art, m, base, mix(base, lo, 0.25), seed=nx(), rough=0.9, streak=0.3)
    sub = m[y0:y1, x0:x1]
    hh, ww = sub.shape
    xs = np.arange(ww, dtype=np.float32)[None, :] * np.ones((hh, 1), np.float32)
    # per-row extent so bands follow the silhouette
    rowmin = np.where(sub > 0.3, xs, 1e9).min(1, keepdims=True)
    rowmax = np.where(sub > 0.3, xs, -1e9).max(1, keepdims=True)
    span = np.maximum(rowmax - rowmin, 1)
    u = np.clip((xs - rowmin) / span, 0, 1)
    wob = (fbm(ww, hh, nx(), 40, 2) - 0.5) * 0.08
    u = np.clip(u + wob, 0, 1)
    shade = np.clip(np.abs(u - 0.38) * 2.2, 0, 1) ** 1.4  # dark at the far edges
    spec = np.exp(-((u - 0.3) / 0.06) ** 2) + 0.5 * np.exp(-((u - 0.72) / 0.05) ** 2)
    full = np.zeros_like(m)
    full[y0:y1, x0:x1] = shade * sub
    art = tint(art, full, lo, amt, seed=nx(), streak=0.3)
    full2 = np.zeros_like(m)
    full2[y0:y1, x0:x1] = np.clip(spec, 0, 1) * sub
    art = tint(art, gaussian_filter(full2, 1.2), hi, 0.85, seed=nx(), streak=0.4)
    return art


def lay(dst, src):
    return over(dst, src)


def paste(dst, src, x, y):
    """Over-composite src (RGBA float) onto dst at integer offset (clipped)."""
    H, W = dst.shape[:2]; h, w = src.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return dst
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src[y0 - y:y1 - y, x0 - x:x1 - x])
    return out


def flat(dst, mask, col, alpha=1.0):
    return over(dst, col_arr(mask, col, mask * alpha))
