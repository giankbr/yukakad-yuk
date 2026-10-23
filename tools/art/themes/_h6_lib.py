"""Agent H6 helpers (pondok-inggris, poster-wisata, piringan-hitam, kolam-teratai).
Builds on _jw_lib/_j1_lib (bbox-local G/GP/LC/FO, strokes, shapes...). Previews -> /tmp/pen/nb-H6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import _p1_lib
import _j1_lib
import art as _art

PREV = "/tmp/pen/nb-H6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def preview6(arr, name, tone="#fbf6e4", bg=None):
    if bg:
        h, w = arr.shape[:2]
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def clear():
    _art._fbm_cache.clear()


def rect(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def rgba_solid(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


# ------------------------------------------------------------------ broken colour (impressionist dabs)
def dabs(W, H, items, seed=1, soft=0.6):
    """items: (x, y, length, width, angle, hex, alpha). Short tapered brush dabs painted straight with skia (fast);
    each dab gets a slight curve and a loaded-brush alpha. Returns RGBA float."""
    cv = Canvas(W, H, seed)
    rng = random.Random(seed)
    for x, y, L, wd, a, col, al in items:
        ca, sa = math.cos(a), math.sin(a)
        bend = rng.uniform(-0.25, 0.25) * L
        p0 = (x - ca * L / 2, y - sa * L / 2); p2 = (x + ca * L / 2, y + sa * L / 2)
        p1 = (x - sa * bend, y + ca * bend)
        path = skia.Path(); path.moveTo(*p0); path.quadTo(*p1, *p2)
        paint = skia.Paint(AntiAlias=True, Color4f=color(col, al), Style=skia.Paint.kStroke_Style, StrokeWidth=wd,
                           StrokeCap=skia.Paint.kRound_Cap)
        if soft:
            paint.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, soft))
        cv.c.drawPath(path, paint)
    return cv.array()


def bristle(arr, seed=3, amount=0.10, angle_blur=(0.6, 3.0)):
    """Add bristle streak texture + paper grain to painted RGBA."""
    h, w = arr.shape[:2]
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), angle_blur)
    s = (s - s.mean()) / (s.std() + 1e-6)
    out = arr.copy()
    out[..., :3] = np.clip(out[..., :3] * (1 + s[..., None] * amount * 0.5), 0, 1)
    return out


def sample_cols(rng, cols):
    return cols[rng.randrange(len(cols))]


# ------------------------------------------------------------------ lithograph poster ink
def litho(mask, col, seed=1, grain=0.5, rough=1.2):
    """Flat lithograph/screen-print ink: crisp hand-cut edge, faint stone-grain mottling, a few missed specks."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 22)
    m = np.clip((gaussian_filter(m, 0.6) - 0.4) * 3, 0, 1)
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.8)
    g = (g - g.mean()) / (g.std() + 1e-6)
    low = fbm(w, h, seed + 4, 70, 3)
    tone = 1 + g * 0.025 * grain + (low - 0.5) * 0.08 * grain
    speck = fbm(w, h, seed + 9, 5, 2)
    cov = 1 - 0.5 * grain * np.clip((speck - 0.8) * 6, 0, 1)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), (m * cov)[..., None]], -1)


def LI(dst, mask, *a, pad=10, **k):
    return _j1_lib._apply(dst, mask, lambda m: litho(m, *a, **k), "over", pad)


def halftone(W, H, mask, cell=6.0, angle=0.5, amount=None):
    """Dot screen inside mask; amount (0..1 field) sets the dot radius."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ca, sa = math.cos(angle), math.sin(angle)
    u = (xx * ca + yy * sa) / cell; v = (-xx * sa + yy * ca) / cell
    d = np.hypot((u % 1) - 0.5, (v % 1) - 0.5)
    r = 0.42 * (np.ones_like(d) if amount is None else np.sqrt(np.clip(amount, 0, 1)))
    return np.clip((r - d) * cell * 0.9 + 0.5, 0, 1) * mask


def vgrad(H, W, y0, y1):
    t = (np.arange(H, dtype=np.float32)[:, None] - y0) / max(1, (y1 - y0))
    return np.clip(t, 0, 1) * np.ones((1, W), np.float32)


def band_poly(W, y_top_fn, y_bot):
    """Polygon from a top edge function y(x) down to y_bot."""
    pts = [(x, y_top_fn(x)) for x in range(-10, W + 11, 8)]
    return pts + [(W + 10, y_bot), (-10, y_bot)]
