"""Agent O4 helpers (khatulistiwa, jumputan-syari, tropis-gelap, pesta-bbq). Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses, flora, palm ...). Previews -> /tmp/pen/nb-O4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-O4/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, a=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask * a)


def dilate(mask, r):
    return np.clip(gaussian_filter(mask, r) * 3.0, 0, 1) if r > 0 else mask


def erode(mask, r):
    return np.clip((gaussian_filter(mask, r) - 0.66) * 3.0, 0, 1)


def edge_ring(mask, r=1.2):
    return np.clip((mask - gaussian_filter(mask, r)) * 3, 0, 1)


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rotp(pts, cx, cy, a):
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def ramp_y(H, W, y0, y1):
    """0 at y0 -> 1 at y1 (vertical light/shadow ramps)."""
    t = (np.arange(H, dtype=np.float32)[:, None] - y0) / max(1e-6, (y1 - y0))
    return np.clip(t, 0, 1) * np.ones((1, W), np.float32)


def ramp_x(H, W, x0, x1):
    t = (np.arange(W, dtype=np.float32)[None, :] - x0) / max(1e-6, (x1 - x0))
    return np.ones((H, 1), np.float32) * np.clip(t, 0, 1)


def opaque_bg(W, H, col):
    a = np.zeros((H, W, 4), np.float32)
    a[..., :3] = col3(col)
    a[..., 3] = 1
    return a


def monstera(W, H, cx, cy, L, ang, rng, holes=True, slits=7):
    """Monstera leaf mask: cordate blade with fenestration slits cut in from the margin and oval holes near the rib.
    (cx, cy) = petiole point, ang = tip direction. Returns (mask, rib points)."""
    def wfn(u):
        return L * 0.47 * (math.sin(math.pi * min(1, u ** 0.8)) ** 0.75) * (1 - 0.22 * u) + 1
    top = [(u * L, wfn(u)) for u in [0.04 + i * 0.96 / 30 for i in range(31)]]
    lobe = [(0.0, 0.0), (-0.12 * L, 0.12 * L), (-0.13 * L, 0.27 * L), (-0.06 * L, 0.40 * L)]
    outline = lobe + top + [(L * 1.01, 0)] + [(x, -y) for x, y in top[::-1]] + [(x, -y) for x, y in lobe[::-1][:-1]]
    outline = [(cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)) for x, y in outline]
    m = shape_mask(W, H, deform(outline, rng, 1, 0.02), smooth=True)
    def T(x, y):
        return (cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang))
    cuts, hl = [], []
    for side in (-1, 1):
        for k in range(slits):
            u = 0.08 + k * (0.8 / slits) + rng.uniform(-0.015, 0.015)
            ue = u + 0.13
            inner = T(u * L + L * 0.02, side * L * (0.09 + 0.03 * rng.random()))
            outer = T(ue * L, side * (wfn(min(1, ue)) + L * 0.06))
            midp = T((u + ue) / 2 * L, side * (wfn(min(1, (u + ue) / 2)) * 0.55))
            cuts.append((curve([inner, midp, outer], 10), L * rng.uniform(0.028, 0.04), (0.6, 0.0)))
            if holes and k % 2 == 0 and 0 < k < slits - 1:
                X, Y = T((u + 0.065) * L, side * L * 0.09)
                hl.append((X, Y, L * 0.035, L * 0.016, math.degrees(ang) + side * 40))
    m = np.clip(m - strokes(W, H, cuts) * 1.3, 0, 1)
    if hl:
        m = np.clip(m - ellipses(W, H, hl) * 1.3, 0, 1)
    rib = [T(-0.02 * L, 0), T(0.5 * L, 0.01 * L), T(0.97 * L, 0)]
    return m, rib


def save_q(arr, path, max_w=None, q=80):
    from _p1_lib import save as _save
    return _save(arr, path, max_w=max_w, quality=q)
