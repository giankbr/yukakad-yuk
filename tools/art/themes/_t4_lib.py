"""Agent T4 helpers (kolintang, kerawang-melayu, pasar-malam, pesta-kostum): _j1_lib (bbox-cropped painting) + a few
local helpers (rects, gradients, wood grain, cut-paper edge, previews). Previews -> /tmp/pen/nb-T4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-T4/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def rect(W, H, x0, y0, x1, y1):
    m = np.zeros((H, W), np.float32)
    m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = 1
    return m


def ygrad(W, H, y0, y1):
    """0 above y0 rising to 1 at y1."""
    y = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    return np.clip((y - y0) / max(1e-6, (y1 - y0)), 0, 1)


def xgrad(W, H, x0, x1):
    x = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    return np.clip((x - x0) / max(1e-6, (x1 - x0)), 0, 1)


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def tint(dst, mask, col, alpha=1.0):
    """over a flat colour through a soft mask (light, shadows)."""
    return over(dst, flat(mask, col, alpha))


def grain_lines(W, H, seed, angle=0.0, scale=3.0, stretch=40.0):
    """Wood grain field 0..1: stretched noise along `angle` (radians) with ring-like bands."""
    n = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (scale * 0.4, stretch) if abs(angle) < 0.8 else (stretch, scale * 0.4))
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    low = fbm(W, H, seed + 2, 90, 3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (yy if abs(angle) < 0.8 else xx) / 7.0 + low * 9
    rings = 0.5 + 0.5 * np.sin(u)
    return np.clip(0.55 * n + 0.45 * rings, 0, 1)


def wood(mask, light, dark, seed=1, angle=0.0, streak=0.8, rough=1.5):
    """Painted timber: gouache body + grain darkening."""
    a = gouache_paint(mask, light, mix(light, dark, .25), seed=seed, rough=rough, streak=streak)
    g = grain_lines(mask.shape[1], mask.shape[0], seed + 4, angle)
    d = np.array(hex_rgb(dark), np.float32)
    k = (np.clip((g - 0.45) * 1.6, 0, 1) * 0.55)[..., None]
    a[..., :3] = a[..., :3] * (1 - k) + d * k
    return a


def W_(dst, mask, *a, pad=10, **k):
    """over: painted wood locally."""
    from _j1_lib import _apply
    return _apply(dst, mask, lambda m: wood(m, *a, **k), "over", pad)


def paper_cut(mask, col, col2=None, seed=1, edge="#fffaf0", edge_w=2.2, shadow=0.35):
    """Cut-paper collage piece: gouache body, a torn white core edge, soft drop shadow (RGBA)."""
    h, w = mask.shape
    m = displace(mask, seed, 1.8, 10)
    m = np.clip((gaussian_filter(m, 0.6) - 0.4) * 3, 0, 1)
    body = gouache_paint(m, col, col2, seed=seed + 1, rough=0.8, streak=0.6)
    grown = np.clip(gaussian_filter(displace(mask, seed + 3, 2.5, 6), edge_w * 0.5) * 2.4, 0, 1)
    rim = np.clip(grown - m, 0, 1)
    out = blank(w, h)
    if shadow:
        sh = np.roll(np.roll(gaussian_filter(grown, 3), 4, 0), 3, 1) * shadow
        out = over(out, flat(sh, "#3a2a1a"))
    out = over(out, flat(rim, edge))
    fib = fbm(w, h, seed + 9, 3, 2)
    b = body.copy()
    b[..., :3] *= (0.94 + 0.08 * fib)[..., None]
    return over(out, b)


def PC(dst, mask, *a, pad=18, **k):
    from _j1_lib import _apply
    return _apply(dst, mask, lambda m: paper_cut(m, *a, **k), "over", pad)


def prev(arr, name, bg=None, tone="#f6efe2"):
    preview(arr, name, tone=tone, bg=bg)
    print("preview", f"{PREV}/{name}.png")


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)); tot += s
        print(f"  {f:24s} {s // 1024:4d} KB")
    print(f"  total {tot // 1024} KB")
