"""Agent L2 helpers (pua-kumbu, pulau-penyengat, brokat-emas, ultah-putri-duyung): warp-ikat bleed, woven thread
texture, brocade weave, plus small geometry helpers. Builds on _jw_lib (G/GP/LC/FO/OV, strokes, shapes...).
Previews -> /tmp/pen/nb-L2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-L2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def lerp_rgb(rgb, colhex, m):
    return rgb * (1 - m[..., None]) + col3(colhex) * m[..., None]


def ikat(mask, seed, col_w=4, shift=4.0, bleed=5.0, flame=0.55):
    """Warp-ikat look: every warp bundle (column of col_w px) is shifted vertically by its own small offset (the
    tied bundles never line up perfectly), and dye bleeds along the warp into ragged vertical 'flames'."""
    h, w = mask.shape
    rng = np.random.default_rng(seed)
    cols = w // col_w + 2
    off = rng.normal(0, shift, cols)
    off = 0.6 * off + 0.4 * gaussian_filter(off, 2.0) * 2
    xx = np.arange(w)
    oy = off[xx // col_w][None, :] * np.ones((h, 1), np.float32)
    yy, xg = np.mgrid[0:h, 0:w].astype(np.float32)
    m = map_coordinates(mask, [yy + oy, xg], order=1, mode="constant")
    # vertical bleed with per-column strength; threshold against streak noise -> flame edges
    b = gaussian_filter(m, (bleed, 0.4))
    colnoise = rng.random(cols)[xx // col_w][None, :]
    streak = gaussian_filter(rng.random((h, w)).astype(np.float32), (6.0, 0.5))
    streak = (streak - streak.min()) / (streak.max() - streak.min() + 1e-6)
    t = 0.5 + (colnoise - 0.5) * 0.35 + (streak - 0.5) * flame
    out = np.clip((b - t) * 5 + 0.5, 0, 1)
    out = np.maximum(out * np.clip(b * 1.6, 0, 1), m * 0.0)
    return out.astype(np.float32)


def weave_mod(h, w, seed, col_w=4, weft=2.6, amt=1.0):
    """Multiplicative thread texture: warp columns with per-thread tone, fine weft ridges, slub noise."""
    rng = np.random.default_rng(seed)
    xx = np.arange(w)
    cols = w // col_w + 2
    ct = (rng.random(cols) - 0.5) * 0.10
    warp = ct[xx // col_w][None, :]
    ph = (xx % col_w) / col_w
    warp = warp + (np.cos(ph * math.tau) * 0.035)[None, :]
    yy = np.arange(h)
    wf = (np.cos(yy / weft * math.tau) * 0.045)[:, None]
    slub = (gaussian_filter(rng.random((h, w)).astype(np.float32), (0.6, 3)) - 0.5) * 0.12
    return (1 + (warp + wf + slub) * amt).astype(np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


def ring_poly(W, H, outer, inner):
    return np.clip(shapes(W, H, [outer], smooth=False) - shapes(W, H, [inner], smooth=False), 0, 1)


def hook(cx, cy, r, a0, d=1, turns=1.15, n=36):
    """Spiral hook (curl) starting at radius r, winding inward."""
    return spiral_pts(cx, cy, r, r * 0.12, a0, turns, n, d)


def mirror_mask(m):
    return np.maximum(m, m[:, ::-1])


def shade_v(arr, top, bottom, k=0.25):
    """Darken towards top/bottom (simple light falloff)."""
    h = arr.shape[0]
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    f = 1 - k * (top * (1 - t) ** 2 + bottom * t ** 2)
    out = arr.copy()
    out[..., :3] *= f[..., None]
    return out
