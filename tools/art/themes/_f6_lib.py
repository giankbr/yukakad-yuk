"""Agent F6 helpers (siraman-adat, tunangan-modern, wisuda-santri, gender-reveal): on top of _jw_lib (flora) +
_j1_lib (bbox-cropped G/GP/LC/FO/OV). Previews -> /tmp/pen/nb-F6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import _p1_lib
import art as _art

_p1_lib.PREV = "/tmp/pen/nb-F6/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)


def clear():
    _art._fbm_cache.clear()


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def edge_of(mask, px=1.2):
    return np.clip((mask - gaussian_filter(mask, px)) * 3, 0, 1)


def shade_side(mask, dx, dy, blur=8, k=1.0):
    """Shadow field on the side of a mask away from the light."""
    g = gaussian_filter(mask, blur)
    return np.clip((g - np.roll(np.roll(g, dy, 0), dx, 1)) * 3 * k, 0, 1) * mask


def radial(mask, cx, cy, r):
    """0 at (cx,cy) → 1 at distance r, inside mask (for round shading)."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return np.clip(((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 / r, 0, 1) * mask


def spot(mask, cx, cy, r):
    """1 at (cx,cy) fading to 0 at distance r, inside mask (highlights)."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return np.clip(1 - ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 / r, 0, 1) * mask


def tint(m, col, a=1.0):
    rgb = np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(m, 0, 1) * a)[..., None]], -1)


def xf(pts, ox, oy, s=1.0, ang=0.0):
    """Scale, rotate (rad) and translate local points."""
    c, si = math.cos(ang), math.sin(ang)
    return [(ox + (x * c - y * si) * s, oy + (x * si + y * c) * s) for x, y in pts]


def inkline(W, H, pts, width, rng, wob=0.6, taper=(0.08, 0.12)):
    """Fine pen line mask with hand wobble (for fine-line drawings)."""
    p = [(x + rng.gauss(0, wob * 0.3), y + rng.gauss(0, wob * 0.3)) for x, y in pts]
    return strokes(W, H, [(p, width, taper)])


def ink(art, mask, col, nx, density=0.9):
    """Ink/pen line rendered as a slightly uneven wash (not a flat vector line)."""
    return G(art, mask, col, seed=nx(), density=density, edge=0.15, bloom=0, rough=0.6, feather=0.45, gran=0.15, mottle=0.25)


def mul(art, field, col, k=0.6, seed=1, tex=0.35):
    """Multiply-shade art toward `col` by field (0..1), with mottled brush variation (reliable form shading)."""
    h, w = field.shape
    n = fbm(w, h, seed, 40, 3)
    f = np.clip(field * k * (1 - tex + tex * 2 * n), 0, 1)[..., None]
    out = art.copy()
    c = np.array(hex_rgb(col), np.float32)
    out[..., :3] = out[..., :3] * (1 - f) + out[..., :3] * c * f
    return out


def lift(art, field, col, k=0.6, seed=2, tex=0.35):
    """Lighten art toward `col` by field (highlights), mottled."""
    h, w = field.shape
    n = fbm(w, h, seed, 40, 3)
    f = np.clip(field * k * (1 - tex + tex * 2 * n), 0, 1)[..., None]
    out = art.copy()
    c = np.array(hex_rgb(col), np.float32)
    out[..., :3] = out[..., :3] * (1 - f) + c * f
    return out
