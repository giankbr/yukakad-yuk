"""Agent M3 helpers (siak-indrapura, mutiara-teluk, terarium, ultah-es-krim). Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses...). Previews -> /tmp/pen/nb-M3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-M3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art
from scipy.ndimage import map_coordinates, binary_dilation  # noqa


def clear():
    _art._fbm_cache.clear()


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def rects(W, H, items):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)] for x0, y0, x1, y1 in items], smooth=False)


def arch_pts(x, y_bot, w, h, n=12, pointed=0.0):
    """Round (or slightly pointed) arch window: bottom-left at (x, y_bot), width w, total height h."""
    r = w / 2
    cx = x + r
    spring = y_bot - (h - r)
    pts = [(x, y_bot), (x, spring)]
    for i in range(1, n):
        a = math.pi + math.pi * i / n
        px = cx + math.cos(a) * r
        py = spring + math.sin(a) * r * (1 + pointed * (1 - abs(math.cos(a))))
        pts.append((px, py))
    pts += [(x + w, spring), (x + w, y_bot)]
    return pts


def onion_pts(cx, by, w, h, n=26, bulge=1.0):
    """Onion dome outline (base at by)."""
    right = []
    for i in range(n + 1):
        t = i / n
        y = by - h * t
        r = w / 2 * (math.sin(math.pi * min(1, t * 1.08)) ** 0.7) * (1.1 - 0.55 * t) * bulge
        if t < 0.08:
            r = max(r, w * 0.42)
        if t > 0.84:
            r *= (1 - t) / 0.16 * 0.55
        right.append((cx + r, y))
    left = [(2 * cx - x, y) for x, y in reversed(right)]
    return right + left


def side_shade(mask, x0, x1, power=1.3):
    """0..1 ramp from x0 to x1 multiplied into mask."""
    h, w = mask.shape
    xx = np.arange(w, dtype=np.float32)[None, :]
    return mask * np.clip((xx - x0) / max(1, x1 - x0), 0, 1) ** power


def v_ramp(mask, y0, y1, power=1.0):
    h, w = mask.shape
    yy = np.arange(h, dtype=np.float32)[:, None]
    return mask * np.clip((yy - y0) / max(1, y1 - y0), 0, 1) ** power


def reflect(art, wl, strength=0.45, wave=2.6, fade=1.5, seed=3):
    """Mirror everything above the waterline wl into the water below with ripple distortion."""
    H, W = art.shape[:2]
    n = min(wl, H - wl)
    seg = art[wl - n:wl][::-1].copy()
    gy, gx = np.mgrid[0:n, 0:W].astype(np.float32)
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6)
    shift = np.sin(gy * 0.55 + ph) * wave + np.sin(gy * 0.13 + gx * 0.012) * wave * 1.4
    rr = np.stack([map_coordinates(seg[..., c], [gy, gx + shift], order=1, mode="nearest") for c in range(4)], -1)
    f = (np.clip(1 - gy[:, :1] / n * fade, 0, 1) * strength)
    low = art[wl:wl + n]
    a = f[..., None] * rr[..., 3:4]
    low[..., :3] = low[..., :3] * (1 - a) + rr[..., :3] * a
    art[wl:wl + n] = low
    return art


def ripples(W, H, rng, y0, y1, n, lmin=14, lmax=60, wmin=1.0, wmax=2.4, x0=-20, x1=None):
    x1 = W if x1 is None else x1
    return strokes(W, H, [([(x, y), (x + rng.uniform(lmin, lmax), y + rng.uniform(-0.6, 0.6))], rng.uniform(wmin, wmax), (0.35, 0.35))
                          for x, y in [(rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n)]])


def alpha_fade(art, top=None, bottom=None, left=None, right=None):
    """Fade alpha towards edges: each arg = (start, end) pixel distances."""
    H, W = art.shape[:2]
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    k = np.ones((H, W), np.float32)
    if top:
        k *= np.clip((yy - top[0]) / (top[1] - top[0]), 0, 1)
    if bottom:
        k *= np.clip(((H - yy) - bottom[0]) / (bottom[1] - bottom[0]), 0, 1)
    if left:
        k *= np.clip((xx - left[0]) / (left[1] - left[0]), 0, 1)
    if right:
        k *= np.clip(((W - xx) - right[0]) / (right[1] - right[0]), 0, 1)
    out = art.copy()
    out[..., 3] *= k
    return out


def seamless_x(art, blend=80):
    W = art.shape[1]
    rolled = np.roll(art, W // 2, 1)
    xx1 = np.arange(W, dtype=np.float32)
    wgt = np.clip(1 - np.minimum(xx1, W - xx1) / blend, 0, 1)[None, :, None]
    return art * (1 - wgt) + rolled * wgt


def tile2(art):
    """Make an RGBA tile seamless in both axes (blend with half-offset copy near the edges)."""
    h, w = art.shape[:2]
    sh = np.roll(np.roll(art, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = np.minimum(xx, w - 1 - xx) / (w / 2); wy = np.minimum(yy, h - 1 - yy) / (h / 2)
    k = np.clip(np.minimum(wx, wy) * 2.2, 0, 1)[..., None]
    return art * k + sh * (1 - k)


def highlight_edge(art, mask, col, dx=-2, dy=-2, density=0.6, seed=1):
    lo = np.clip(mask - np.roll(np.roll(mask, -dy, 0), -dx, 1), 0, 1)
    return G(art, lo, col, seed=seed, density=density, edge=0, bloom=0, rough=0.4, feather=0.4)


def glass_shine(W, H, pts, width):
    return strokes(W, H, [(pts, width, (0.3, 0.4))])
