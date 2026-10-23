"""Agent J1 (batch 10) helpers: banyumas-batik, minang-suntiang, cheng-ho, ultah-pahlawan.
Builds on _jw_lib (G/GP/LC/FO/OV crop painting, strokes/shapes/circles, lung, palm, hatch). Previews -> /tmp/pen/nb-J1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import art as _art

KPREV = "/tmp/pen/nb-J1/art"
os.makedirs(KPREV, exist_ok=True)


def prev(arr, name, bg="#f6efe2"):
    """Composite on a flat colour (or paper when bg is None) and save a PNG preview."""
    h, w = arr.shape[:2]
    if bg is None:
        on_paper(arr, "#f6efe2").save(f"{KPREV}/{name}.png")
        return
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{KPREV}/{name}.png")


def clear():
    _art._fbm_cache.clear()


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def inner_edge(mask, px):
    """A band just inside the mask edge (for rims/frames)."""
    return np.clip(mask - (gaussian_filter(mask, px * 0.6) > 0.98).astype(np.float32), 0, 1) * mask


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def ink(dst, mask, col, alpha=0.9, rough=1.0, seed=1):
    """Hand-inked contour: displaced mask, slightly uneven darkness."""
    def fn(m):
        mm = displace(m, seed, rough, 14)
        h, w = mm.shape
        a = np.clip(mm * 1.25, 0, 1) * (0.8 + 0.2 * fbm(w, h, seed + 2, 20, 2)) * alpha
        return np.concatenate([flat(mm, col)[..., :3], a[..., None]], -1)
    return OV(dst, mask, fn, pad=8)


def tile_noise(n, seed, sigma):
    return wrap_noise(n, n, seed, sigma)


def halftone(W, H, spacing=9, rmax=3.6, tone=None, angle=0.5):
    """Halftone dot mask; tone (H,W) 0..1 scales dot radius."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    ca, sa = math.cos(angle), math.sin(angle)
    R = int(math.hypot(W, H) / spacing) + 2
    for i in range(-R, R):
        for j in range(-R, R):
            x = W / 2 + (i * ca - j * sa) * spacing
            y = H / 2 + (i * sa + j * ca) * spacing
            if -6 < x < W + 6 and -6 < y < H + 6:
                t = 1.0 if tone is None else float(tone[min(H - 1, max(0, int(y))), min(W - 1, max(0, int(x)))])
                r = rmax * t
                if r > 0.35:
                    cv.c.drawCircle(x, y, r, p)
    return cv.array()[..., 3]
