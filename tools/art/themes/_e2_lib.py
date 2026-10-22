"""Agent E2 helpers (raja-ampat, karo-siwaluh, fes-tembaga, mamluk-kairo). Builds on _j1_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, hatch) and adds rect/poly/flat, gradients, water reflection, weave
and plaster textures. Previews -> /tmp/pen/nb-E2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib, _j1_lib
from _j1_lib import *  # noqa
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-E2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def col_arr(h):
    return np.array(hex_rgb(h), np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * col_arr(col)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def xgrad(W, H, x0, x1):
    return np.clip((np.arange(W, dtype=np.float32)[None, :] - x0) / (x1 - x0), 0, 1) * np.ones((H, 1), np.float32)


def ygrad(W, H, y0, y1):
    return np.clip((np.arange(H, dtype=np.float32)[:, None] - y0) / (y1 - y0), 0, 1) * np.ones((1, W), np.float32)


def radial(W, H, cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1)


def reflect(scene, horizon, seed=1, amp=6.0, wl=7.0, fade=0.75, blur=1.2):
    """Mirror everything above `horizon` into the water below, broken by ripple displacement (RGBA layer)."""
    H, W = scene.shape[:2]
    out = np.zeros_like(scene)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(yy - horizon, 0, None)
    n = fbm(W, H, seed, 30, 3) - 0.5
    rip = np.sin(d / (wl * (0.6 + d / H)) + n * 6) * amp * (0.3 + d / max(1, H - horizon))
    sy = horizon - d + n * 2
    sx = xx + rip
    for c in range(4):
        out[..., c] = map_coordinates(scene[..., c], [np.clip(sy, 0, H - 1), np.clip(sx, 0, W - 1)], order=1)
    out[..., :3] = gaussian_filter(out[..., :3], (blur, blur * 2.5, 0))
    below = (yy > horizon).astype(np.float32)
    k = np.clip(1 - d / max(1, (H - horizon)) * fade, 0, 1)
    out[..., 3] *= below * k
    return out


def ripple_lines(W, H, y0, y1, seed, density=0.5, lmin=10, lmax=60, x0=-20, x1=None):
    rng = np.random.default_rng(seed)
    x1 = W + 20 if x1 is None else x1
    items = []
    n = int((y1 - y0) * (x1 - x0) / 900 * density)
    for _ in range(n):
        t = rng.random() ** 0.8
        y = y0 + (y1 - y0) * t
        x = rng.uniform(x0, x1)
        L = rng.uniform(lmin, lmax) * (0.4 + t)
        wd = 0.6 + 2.2 * t
        items.append(([(x, y), (x + L * 0.5, y + rng.uniform(-0.6, 0.6)), (x + L, y)], wd, (0.4, 0.4)))
    return strokes(W, H, items)


def wnoise(w, h, seed, sigma):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def rgb_save(rgb, path, quality=80, size=None):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im


def comp_rgb(bg_rgb, layer):
    a = layer[..., 3:4]
    return bg_rgb * (1 - a) + layer[..., :3] * a


def prev_rgb(rgb, name):
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def kb_report(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)); tot += s
        print(f"  {f:24s} {s // 1024:4d} KB")
    print("  total", tot // 1024, "KB")


def mix_hex(a, b, t):
    ca, cb = col_arr(a), col_arr(b)
    c = ca * (1 - t) + cb * t
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)
