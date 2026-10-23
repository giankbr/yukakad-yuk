"""Agent L3 (batch 11) helpers: kelimutu-lio, karavanserai, kristal-syari, ultah-pelangi.
Builds on _jw_lib (G/GP/LC/FO/OV crop painting, strokes/shapes/circles, hatch). Previews -> /tmp/pen/nb-L3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import art as _art

LPREV = "/tmp/pen/nb-L3/art"
os.makedirs(LPREV, exist_ok=True)


def prev(arr, name, bg="#f6efe2"):
    """Composite on a flat colour (or paper when bg is None) and save a PNG preview."""
    h, w = arr.shape[:2]
    if bg is None:
        on_paper(arr, "#f6efe2").save(f"{LPREV}/{name}.png")
        return
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{LPREV}/{name}.png")


def clear():
    _art._fbm_cache.clear()


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def soft(dst, mask, col, alpha=1.0, blur=0.0, pad=20):
    """Plain soft-edged tint (light, glow, haze) composited over."""
    def fn(m):
        mm = gaussian_filter(m, blur) if blur else m
        return flat(mm, col, alpha)
    return OV(dst, mask, fn, pad=pad + int(blur * 3))


def ink(dst, mask, col, alpha=0.9, rough=1.0, seed=1):
    def fn(m):
        mm = displace(m, seed, rough, 14)
        h, w = mm.shape
        a = np.clip(mm * 1.25, 0, 1) * (0.8 + 0.2 * fbm(w, h, seed + 2, 20, 2)) * alpha
        return np.concatenate([flat(mm, col)[..., :3], a[..., None]], -1)
    return OV(dst, mask, fn, pad=8)


def opaque(arr, bg):
    """Flatten an RGBA canvas onto a flat background colour (opaque)."""
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    return np.concatenate([rgb, np.ones((h, w, 1), np.float32)], -1)


def vgrad(h, w, stops):
    """Smooth vertical gradient mask helper returning (h,w,3) colour from [(t,hex)]."""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32)
    rgb = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        k = np.clip((t - t0) / max(1e-6, t1 - t0), 0, 1)[..., None]
        sel = ((t >= t0) & (t <= t1))
        ca = np.array(hex_rgb(c0), np.float32); cb = np.array(hex_rgb(c1), np.float32)
        rgb[sel] = (ca * (1 - k) + cb * k)[sel]
    return rgb


def cloud_pts(cx, cy, w, h, lobes, rng):
    """Puffy cloud outline: bumps along the top, flatter base."""
    pts = []
    for i in range(lobes + 1):
        t = i / lobes
        x = cx - w / 2 + t * w
        bump = math.sin(t * math.pi) * h * (0.7 + 0.3 * rng.random())
        pts.append((x, cy - bump))
    base = [(cx + w / 2, cy + h * 0.12), (cx, cy + h * 0.2), (cx - w / 2, cy + h * 0.12)]
    return pts + base


def puff_cloud(W, H, cx, cy, w, h, rng, n=7):
    """Cloud as union of circles (gouache/fluffy) + flat base."""
    items = []
    for i in range(n):
        t = (i + 0.5) / n
        x = cx - w / 2 + t * w
        r = h * (0.35 + 0.45 * math.sin(t * math.pi)) * (0.85 + 0.3 * rng.random())
        items.append((x, cy - r * 0.55, r))
    m = circles(W, H, items)
    base = shapes(W, H, [[(cx - w / 2 - h * 0.1, cy), (cx + w / 2 + h * 0.1, cy), (cx + w / 2, cy + h * 0.28), (cx - w / 2, cy + h * 0.28)]])
    return np.clip(np.maximum(m, base), 0, 1)
