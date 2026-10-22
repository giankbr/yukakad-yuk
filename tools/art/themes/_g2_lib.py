"""Agent G2 helpers (priangan-kacapi, sumba-hinggi, sajadah-beludru, ultah-kucing): _a6_lib (bbox-local gouache,
crayon, tint) + tileable weaves (bilik), ikat resist-dye, gold-thread embroidery stitches, velvet pile.
Previews -> /tmp/pen/nb-G2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *  # noqa
from _jw_lib import palm, spiral_pts, along, hills  # noqa
import _p1_lib, _j1_lib
PREV = "/tmp/pen/nb-G2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV


def wrapn(w, h, seed, sigma):
    """Tileable smooth noise in [0,1]."""
    return wrap_noise(w, h, seed, sigma)


def lin_field(w, h, seed, along=(1.0, 0.0), sig_along=12.0, sig_across=0.6, wrap=True):
    """Fibre/streak noise stretched along a direction (axis-aligned: along x if along[0] else y)."""
    r = np.random.default_rng(seed).random((h, w)).astype(np.float32)
    s = (sig_across, sig_along) if along[0] else (sig_along, sig_across)
    n = gaussian_filter(r, s, mode="wrap" if wrap else "reflect")
    return (n - n.mean()) / (n.std() + 1e-6)


def rgb_of(h):
    return np.array(hex_rgb(h), np.float32)


def opaque(rgb):
    return np.concatenate([np.clip(rgb, 0, 1), np.ones(rgb.shape[:2] + (1,), np.float32)], -1)


def ikat(mask, col, seed=1, bleed=5.0, warp_axis=1, wear=0.18):
    """Ikat resist-dye: the motif edge bleeds in feathered streaks along the warp (vertical by default), the colour
    is slightly uneven thread-by-thread, small undyed flecks."""
    h, w = mask.shape
    rng = np.random.default_rng(seed)
    # per-thread offset along the warp: each column (warp thread) shifts a little -> stepped, feathered edges
    if warp_axis == 1:
        off = gaussian_filter(rng.normal(0, 1, w).astype(np.float32), 0.8) * bleed
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        m = map_coordinates(mask, [yy + off[None, :], xx], order=1, mode="constant")
        m = gaussian_filter(m, (bleed * 0.35, 0.5))
    else:
        off = gaussian_filter(rng.normal(0, 1, h).astype(np.float32), 0.8) * bleed
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        m = map_coordinates(mask, [yy, xx + off[:, None]], order=1, mode="constant")
        m = gaussian_filter(m, (0.5, bleed * 0.35))
    m = np.clip((m - 0.25) * 1.8, 0, 1)
    thread = lin_field(w, h, seed + 2, (0, 1) if warp_axis == 1 else (1, 0), 30, 0.5, wrap=False)
    fleck = fbm(w, h, seed + 4, 5, 2)
    a = m * np.clip(0.9 + thread * 0.06, 0, 1) * (1 - wear * np.clip((fleck - 0.66) * 5, 0, 1))
    rgb = np.ones((h, w, 3), np.float32) * rgb_of(col) * (1 + thread[..., None] * 0.05)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def IK(dst, mask, *a, pad=14, **k):
    return OV(dst, mask, lambda m: ikat(m, *a, **k), pad=pad)


def stitch(mask, angle, base="#c9a14a", hi="#f6e3a4", lo="#7a5a24", seed=1, spacing=2.4, gap=0.18, ufield=None):
    """Satin-stitch gold embroidery: parallel threads across the shape at `angle` (radians, float or field), each
    thread a rounded cylinder with a highlight; slight irregular spacing, soft drop shadow ridge at the edge."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ang = angle if np.ndim(angle) else np.full((h, w), angle, np.float32)
    jit = (fbm(w, h, seed, 14, 2) - 0.5) * 1.4
    u = ((xx * np.cos(ang) + yy * np.sin(ang)) if ufield is None else ufield) / spacing + jit
    f = (u % 1.0)
    prof = np.clip(np.sin(f * math.pi), 0, 1)            # 0 at thread gaps, 1 at thread centre
    gapm = np.clip((np.abs(f - 0.5) * 2 - (1 - gap)) * 8, 0, 1)
    shine = prof ** 3
    # light falls from top-left: threads at angles facing light are brighter
    facing = 0.55 + 0.45 * np.cos(ang - 2.3)
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    b, hcol, lcol = rgb_of(base), rgb_of(hi), rgb_of(lo)
    t = (prof * 0.6 + shine * 0.6 * facing)[..., None]
    rgb = lcol * (1 - np.clip(t * 1.6, 0, 1)) + b * np.clip(t * 1.6, 0, 1)
    rgb = rgb * (1 - np.clip(t - 0.62, 0, 1) * 2) + hcol * np.clip(t - 0.62, 0, 1) * 2
    rgb = rgb * (1 - 0.35 * gapm[..., None])
    edge = np.clip(m - gaussian_filter(m, 1.6), 0, 1)
    rgb = rgb * (1 - edge[..., None] * 0.5)
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def ST(dst, mask, angle, ufn=None, **k):
    """Satin stitch locally; angle may be a float or a callable (xx, yy) -> radians in the bbox."""
    b = bbox(mask, 6)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = np.ascontiguousarray(mask[y0:y1, x0:x1])
    if callable(angle):
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        a = angle(xx, yy).astype(np.float32)
    else:
        a = angle
    if ufn is not None:
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        k["ufield"] = ufn(xx, yy).astype(np.float32)
    src = stitch(m, a, **k)
    sh = np.roll(np.roll(gaussian_filter(m, 1.6), 2, 0), 1, 1) * 0.45
    out = dst.copy()
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], col_arr(m, "#1a0508", sh))
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], src)
    return out


def couch(dst, items, base="#c9a14a", hi="#f6e3a4", lo="#6e5020", seed=1, W=None, H=None):
    """Couched gold cord along polylines: a twisted cord (diagonal twist marks) with a soft shadow; items=[(pts,width)]."""
    h, w = dst.shape[:2]
    out = dst
    for k, (pts, wd) in enumerate(items):
        m = strokes(w, h, [(pts, wd, None)])
        b = bbox(m, 4)
        if b is None:
            continue
        y0, y1, x0, x1 = b
        mm = m[y0:y1, x0:x1]
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        tw = 0.5 + 0.5 * np.sin((xx + yy) / (wd * 0.55) * math.pi + seed + k)
        cyl = np.clip(gaussian_filter(mm, wd * 0.25) * 1.2, 0, 1)
        t = (tw * 0.55 + cyl * 0.45)[..., None]
        rgb = rgb_of(lo) * (1 - t) + rgb_of(base) * t
        rgb = rgb + (rgb_of(hi) - rgb) * np.clip((t - 0.75) * 3, 0, 1)
        sh = np.roll(np.roll(gaussian_filter(mm, 1.5), 2, 0), 1, 1) * 0.5
        o = out.copy()
        o[y0:y1, x0:x1] = over(o[y0:y1, x0:x1], col_arr(mm, "#1a0508", sh))
        o[y0:y1, x0:x1] = over(o[y0:y1, x0:x1], np.concatenate([np.clip(rgb, 0, 1), np.clip(mm * 1.1, 0, 1)[..., None]], -1))
        out = o
    return out


def wood(dst, mask, col, col2, dark, seed=1, along=0.0, amt=0.35):
    """Wood grain glaze inside mask: long wavy streaks along `along` (radians)."""
    b = bbox(mask, 2)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = mask[y0:y1, x0:x1]
    hh, ww = m.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    v = -xx * math.sin(along) + yy * math.cos(along)
    wob = (fbm(ww, hh, seed, 60, 3) - 0.5) * 14
    g = 0.5 + 0.5 * np.sin((v + wob) / 2.6)
    g2 = 0.5 + 0.5 * np.sin((v + wob * 1.7) / 7.0)
    a = m * np.clip((g - 0.72) * 3, 0, 1) * amt + m * np.clip((g2 - 0.8) * 3, 0, 1) * amt * 0.7
    out = dst.copy()
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], col_arr(m, dark, a * dst[y0:y1, x0:x1, 3]))
    return out
