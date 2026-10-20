"""Agent P2 helpers on top of /tmp/pen/art/art.py: local-crop media, ink/pencil, halftone, seamless tiles."""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

OUT = "/root/w/frontend/public/themes/art"
PREV = "/tmp/pen/nt3-P2"


def _bbox(mask, pad):
    ys, xs = np.nonzero(mask > 0.01)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def local(fn, mask, *a, pad=40, **k):
    """Run a medium function only on the mask's bbox; returns full-size RGBA."""
    h, w = mask.shape
    out = np.zeros((h, w, 4), np.float32)
    bb = _bbox(mask, pad)
    if bb is None:
        return out
    y0, y1, x0, x1 = bb
    out[y0:y1, x0:x1] = fn(mask[y0:y1, x0:x1], *a, **k)
    return out


def pig(mask, *a, **k):
    return local(pigment, mask, *a, **k)


def gou(mask, *a, **k):
    return local(gouache_paint, mask, *a, **k)


def lino(mask, *a, **k):
    return local(linocut, mask, *a, **k)


class Seeds:
    def __init__(self, s=100):
        self.s = s

    def __call__(self):
        self.s += 17
        return self.s


def preview(arr, path, tone="#fbf5ef"):
    on_paper(arr, tone).save(path)


def preview_on(arr, path, bg):
    h, w = arr.shape[:2]
    b = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = b * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(path)


def flip_h(arr):
    return arr[:, ::-1].copy()


def rot(pt, cx, cy, a):
    x, y = pt[0] - cx, pt[1] - cy
    return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))


# ---------- seamless tiles ----------
def _wrapnoise(size, rng, s):
    a = gaussian_filter(rng.random((size, size)).astype(np.float32), s, mode="wrap")
    return (a - a.mean()) / (a.std() + 1e-6)


def paper_tile(size=512, tone="#fbf8f6", seed=3, mottle=1.0, fine=1.0, fiber=1.0, strength=1.0):
    r = np.random.default_rng(seed)
    v = 1 + strength * (_wrapnoise(size, r, 36) * 0.02 * mottle + _wrapnoise(size, r, 0.7) * 0.016 * fine + _wrapnoise(size, r, (0.5, 5)) * 0.012 * fiber)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    return Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB")


def linen_tile(size=512, tone="#f4f0ea", seed=5, pitch=4.0, strength=1.0, slub=0.6):
    """Seamless linen weave: warp/weft threads with slubs and a soft mottle (multiply tile)."""
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    n = round(size / pitch)
    pitch = size / n
    warp = 0.5 + 0.5 * np.cos(xx / pitch * math.tau)
    weft = 0.5 + 0.5 * np.cos(yy / pitch * math.tau)
    # over/under: checkerboard of which thread is on top
    cx = np.floor(xx / pitch).astype(int); cy = np.floor(yy / pitch).astype(int)
    top = ((cx + cy) % 2).astype(np.float32)
    weave = top * warp + (1 - top) * weft
    thick_x = 1 + slub * 0.5 * _wrapnoise(size, r, (0.6, 14))
    thick_y = 1 + slub * 0.5 * _wrapnoise(size, r, (14, 0.6))
    v = 1 + strength * ((weave - 0.5) * 0.05 + (thick_x - 1) * 0.03 + (thick_y - 1) * 0.03 + _wrapnoise(size, r, 30) * 0.015 + _wrapnoise(size, r, 0.6) * 0.012)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    return Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB")


def newsprint_tile(size=512, tone="#f3eddf", seed=9, strength=1.0):
    """Newsprint: fibrous, speckled, with faint ink show-through blotches."""
    r = np.random.default_rng(seed)
    v = 1 + strength * (_wrapnoise(size, r, 24) * 0.02 + _wrapnoise(size, r, 0.6) * 0.022 + _wrapnoise(size, r, (0.5, 4)) * 0.012)
    speck = (r.random((size, size)) > 0.9985).astype(np.float32)
    speck = gaussian_filter(speck, 0.7, mode="wrap") * 4
    v -= speck * 0.35
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    return Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB")


def halftone_tile(size=64, pitch=6.0, dot=0.42, angle=0.3, seed=2):
    """Seamless halftone dot screen (RGBA: black dots, use as multiply/overlay at low opacity)."""
    n = max(1, round(size / pitch)); pitch = size / n
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    # rotated grid approximated as orthogonal (angle only jitters phase) so it tiles
    fx = xx / pitch * math.tau; fy = yy / pitch * math.tau
    field = (0.5 + 0.5 * np.cos(fx)) * (0.5 + 0.5 * np.cos(fy))
    r = np.random.default_rng(seed)
    field = field + _wrapnoise(size, r, 1.0) * 0.03
    a = np.clip((field - (1 - dot)) * 5, 0, 1)
    rgb = np.zeros((size, size, 3), np.float32) + np.array(hex_rgb("#1d1a14"), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)


# ---------- ink / pencil ----------
def ink_mask(W, H, polylines, width=2.2, jitter=0.5, seed=1, taper=(0.1, 0.1), wobble=1.2):
    """Hand-inked polylines → mask (variable pressure, wobble)."""
    rng = random.Random(seed)
    def draw(cv):
        for pts in polylines:
            pts = [(x + rng.gauss(0, jitter), y + rng.gauss(0, jitter)) for x, y in pts]
            n = len(pts)
            for i in range(n - 1):
                t = i / max(1, n - 2)
                k = min(1.0, t / taper[0]) if (taper[0] and t < taper[0]) else (min(1.0, (1 - t) / taper[1]) if (taper[1] and t > 1 - taper[1]) else 1.0)
                wdt = max(0.5, width * (0.35 + 0.65 * k) * rng.uniform(0.8, 1.2))
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(*pts[i], *pts[i + 1], p)
    m = mask_from(W, H, draw)
    if wobble:
        m = displace(m, seed + 3, wobble, 14)
    return m


def ink(mask, col="#2a2622", seed=1, dry=0.25, bleed=0.35, density=0.92):
    """Fountain-pen ink: slight bleed into paper fibres, dry-brush gaps, tonal variation."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    halo = np.clip(gaussian_filter(mask, 1.6) * 0.5, 0, 1) * bleed
    a = np.clip(m + halo * (1 - m), 0, 1)
    if dry:
        d = fbm(w, h, seed + 9, 5, 2)
        a *= 1 - dry * np.clip((d - 0.6) * 3, 0, 1)
    tone = 0.85 + 0.15 * fbm(w, h, seed + 8, 30, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), (a * density)[..., None]], -1)


def pencil(mask, col="#4a443d", seed=1, grain=0.6, density=0.7):
    """Graphite: paper-tooth grain breaks the stroke, soft tonal edges."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.6), 0, 1)
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.6)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    a = m * ((1 - grain) + grain * np.clip((g - 0.3) * 1.8, 0, 1))
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (a * density)[..., None]], -1)


def hatch_mask(W, H, region_mask, spacing=7, angle=-0.7, width=1.0, seed=1, jitter=0.8):
    """Pencil hatching lines clipped to a region mask."""
    rng = random.Random(seed)
    lines = []
    diag = math.hypot(W, H)
    ca, sa = math.cos(angle), math.sin(angle)
    cx, cy = W / 2, H / 2
    k = -diag
    while k < diag:
        pts = []
        for t in np.linspace(-diag, diag, 24):
            x = cx + t * ca - k * sa; y = cy + t * sa + k * ca
            pts.append((x + rng.gauss(0, jitter), y + rng.gauss(0, jitter)))
        lines.append(pts)
        k += spacing * rng.uniform(0.8, 1.25)
    m = ink_mask(W, H, lines, width=width, jitter=0.2, seed=seed, taper=(0, 0), wobble=0.6)
    return m * np.clip(region_mask, 0, 1)


# ---------- botanical building blocks (watercolour) ----------
def leaf(W, H, x, y, L, a, ca, cb, sd, rng, width=0.33, vein=True, density=0.66, curl=0.0):
    pts = petal_pts(x, y, L, L * width, a, n=12, cup=curl)
    pts = deform(pts, rng, 1, 0.04)
    m = shape_mask(W, H, pts)
    lay = pig(m, ca, cb, seed=sd(), density=density, edge=0.5, bloom=0.35, rough=4, holes=0.04)
    half = shape_mask(W, H, petal_pts(x, y, L * 0.94, L * width * 0.48, a + 0.07, n=12, cup=curl))
    lay = glaze(lay, pig(half, cb, seed=sd(), density=0.3, edge=0.3, bloom=0.2, rough=3))
    if vein:
        v = [(x + math.cos(a) * L * t - math.sin(a) * curl * L * width * t * t, y + math.sin(a) * L * t + math.cos(a) * curl * L * width * t * t)
             for t in [j / 12 for j in range(1, 10)]]
        lay = glaze(lay, pig(stroke_mask(W, H, v, max(1.5, L * 0.012)), mix(cb, "#1f2b1d", .45), seed=sd(), density=0.28, edge=0.1, bloom=0, rough=1.2, feather=0.6))
    return lay, m


def stem(W, H, pts, width, col, sd, density=0.55):
    m = stroke_mask(W, H, curve(pts, 80), width, taper=(0.05, 0.35))
    return pig(m, col, mix(col, "#2a3324", .3), seed=sd(), density=density, edge=0.4, bloom=0, rough=1.6, feather=0.7), m


def dots(W, H, cx, cy, sx, sy, n, rmin, rmax, rng):
    def draw(cv):
        for _ in range(n):
            cv.c.drawCircle(cx + rng.gauss(0, sx), cy + rng.gauss(0, sy), rng.uniform(rmin, rmax), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def kb(path):
    return os.path.getsize(path) // 1024
