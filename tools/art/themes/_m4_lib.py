"""Agent M4 (batch 12) helpers: sabu-raijua, kenanga-syari, cetak-biru, pameran-seni.
Builds on _jw_lib (G/GP/LC/FO/OV crop painting, strokes/shapes/circles, hatch). Previews -> /tmp/pen/nb-M4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import art as _art
from scipy.ndimage import map_coordinates  # noqa

MPREV = "/tmp/pen/nb-M4/art"
os.makedirs(MPREV, exist_ok=True)


def prev(arr, name, bg="#f6efe2"):
    """Composite on a flat colour (or paper when bg is None) and save a PNG preview."""
    h, w = arr.shape[:2]
    if bg is None:
        on_paper(arr, "#f6efe2").save(f"{MPREV}/{name}.png")
        return
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{MPREV}/{name}.png")


def clear():
    _art._fbm_cache.clear()


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def soft(dst, mask, col, alpha=1.0, blur=0.0, pad=20):
    """Plain soft-edged tint (light, glow, haze, shadow) composited over."""
    def fn(m):
        mm = gaussian_filter(m, blur) if blur else m
        return flat(mm, col, alpha)
    return OV(dst, mask, fn, pad=pad + int(blur * 3))


def opaque(arr, bg):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    return np.concatenate([rgb, np.ones((h, w, 1), np.float32)], -1)


def lines(w, h, items, cap=True):
    """Constant-width polylines into one mask. items: (pts, width)."""
    cv = Canvas(w, h)
    for pts, width in items:
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap, StrokeJoin=skia.Paint.kRound_Join)
        path = skia.Path()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def rings(w, h, items):
    """items: (cx, cy, r, width) stroked circles."""
    cv = Canvas(w, h)
    for cx, cy, r, width in items:
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width))
    return cv.array()[..., 3]


def ikat_bleed(mask, seed, amt=3.0, wrap=True):
    """Ikat look: warp threads shift up/down per column and bleed vertically; fine thread streaks."""
    h, w = mask.shape
    mode = "wrap" if wrap else "nearest"
    rng = np.random.default_rng(seed)
    shift = gaussian_filter(rng.normal(0, 1, w).astype(np.float32), 1.2, mode=mode)
    shift = shift / (np.abs(shift).max() + 1e-6) * amt
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    m = map_coordinates(mask, [yy + shift[None, :], xx], order=1, mode="grid-wrap" if wrap else "nearest")
    m = gaussian_filter(m, (1.5, 0.4), mode=mode)
    streak = gaussian_filter(rng.random((h, w)).astype(np.float32), (6, 0.35), mode=mode)
    streak = (streak - streak.min()) / (streak.max() - streak.min() + 1e-6)
    return np.clip(m * (0.78 + 0.32 * streak), 0, 1)


def weave(h, w, seed, amp=0.05):
    """Woven thread texture multiplier (warp + weft micro stripes)."""
    rng = np.random.default_rng(seed)
    warp = gaussian_filter(rng.random((1, w)).astype(np.float32), (0, 0.6), mode="wrap")
    weft = gaussian_filter(rng.random((h, 1)).astype(np.float32), (0.6, 0), mode="wrap")
    yy, xx = np.mgrid[0:h, 0:w]
    check = ((xx + yy) % 2).astype(np.float32)
    t = (warp - .5) * 1.4 + (weft - .5) * 1.0 + (check - .5) * 0.5
    return 1 + t * amp


def save_rgba_full(arr, path, size=None, quality=82):
    im = to_image(arr)
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size
