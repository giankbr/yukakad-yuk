"""Agent O2 helpers (dieng-telaga, mustard-syari, sketsa-kota, ultah-sains).
Builds on _j1_lib (bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, hatch) and adds small raster utilities
(gradients, rgb compositing, flat fills, previews) plus pen-line helpers for urban-sketch drawing:
  pen()        loose fineliner line along a polyline with pressure, wobble and corner overshoot
  pen_box()    a sketched rectangle whose sides overshoot like a quick urban sketch
Previews -> /tmp/pen/nb-O2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib, _j1_lib
from _j1_lib import *  # noqa
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-O2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def col_arr(h):
    return np.array(hex_rgb(h), np.float32)


def mix_hex(a, b, t):
    c = col_arr(a) * (1 - t) + col_arr(b) * t
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in np.clip(c, 0, 1))


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


def radial(W, H, cx, cy, r, sy=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.clip(1 - np.hypot(xx - cx, (yy - cy) / sy) / r, 0, 1)


def comp_rgb(bg_rgb, layer):
    a = layer[..., 3:4]
    return bg_rgb * (1 - a) + layer[..., :3] * a


def prev_rgb(rgb, name):
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def rgb_save(rgb, path, quality=80, size=None):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im


def kb_report(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)); tot += s
        print(f"  {f:24s} {s // 1024:4d} KB")
    print("  total", tot // 1024, "KB")


def wnoise(w, h, seed, sigma):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def wob_line(a, b, rng, amp=1.2, n=None):
    """Points along a->b with a gentle hand wobble (low-frequency, not jitter)."""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    n = n or max(3, int(L / 10))
    dx, dy = (b[0] - a[0]) / (L or 1), (b[1] - a[1]) / (L or 1)
    ph = rng.uniform(0, 6.28); fr = rng.uniform(1.0, 2.2)
    out = []
    for i in range(n + 1):
        t = i / n
        o = math.sin(t * math.pi * fr + ph) * amp + rng.gauss(0, amp * 0.15)
        out.append((a[0] + (b[0] - a[0]) * t - dy * o, a[1] + (b[1] - a[1]) * t + dx * o))
    return out


def pen_items(segs, rng, width=1.6, over=6.0, amp=1.0):
    """Urban-sketch pen strokes: each segment (a, b) overshoots both ends a little and wobbles; returns stroke items."""
    items = []
    for seg in segs:
        a, b = seg[0], seg[1]
        wd = seg[2] if len(seg) > 2 else width
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        o0 = rng.uniform(0.2, 1.0) * over; o1 = rng.uniform(0.3, 1.2) * over
        a2 = (a[0] - ux * o0, a[1] - uy * o0); b2 = (b[0] + ux * o1, b[1] + uy * o1)
        items.append((wob_line(a2, b2, rng, amp), wd * rng.uniform(0.8, 1.15), (0.06, 0.12)))
    return items


def box_segs(x0, y0, x1, y1):
    return [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]


def ink(mask, col="#2a2724", seed=1, alpha=0.92):
    """Fineliner ink: dense, slightly uneven, tiny dry breaks."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.45) * 1.15, 0, 1)
    dry = fbm(w, h, seed, 7, 2)
    m *= 1 - 0.35 * np.clip((dry - 0.72) * 5, 0, 1)
    rgb = np.ones((h, w, 3), np.float32) * col_arr(col)
    return np.concatenate([rgb, (m * alpha)[..., None]], -1)


def INK(dst, mask, col="#2a2724", seed=1, alpha=0.92, pad=8):
    return OV(dst, mask, lambda m: ink(m, col, seed, alpha), pad=pad)
