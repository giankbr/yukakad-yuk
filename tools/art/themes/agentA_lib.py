"""Agent A helpers on top of /tmp/pen/art/art.py (local-crop pigment for speed, botanical building blocks)."""
import sys, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
import numpy as np
from scipy.ndimage import gaussian_filter

OUT = "/root/w/frontend/public/themes/art"


def _bbox(mask, pad):
    ys, xs = np.nonzero(mask > 0.01)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def local(fn, mask, *a, pad=40, **k):
    """Run a medium function (pigment/gouache_paint/linocut/foil/glow) only on the mask's bbox; returns full-size RGBA."""
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


class Seeds:
    def __init__(self, s=100):
        self.s = s

    def __call__(self):
        self.s += 17
        return self.s


def leaf(W, H, x, y, L, a, ca, cb, sd, rng, width=0.33, vein=True, density=0.66, curl=0.0):
    """Watercolour leaf (two-tone: light wash + shadow half + faint vein). Returns (rgba, mask)."""
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


def rose(W, H, cx, cy, r, light, mid, deep, sd, rng, petals=10, tilt=0.86):
    """Loose watercolour rose: base wash, cupped outer petals, comma strokes spiralling to a deep heart, shadow at lower right."""
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * tilt, 10), rng, 2, 0.12))
    lay = pig(base, light, mid, seed=sd(), density=0.42, edge=0.38, bloom=0.5, rough=9, holes=0.1)
    # outer cupped petals (light from top-left: lower-right petals a touch deeper)
    for k in range(5):
        ang = k / 5 * math.tau + rng.uniform(-.3, .3)
        px, py = cx + math.cos(ang) * r * .55, cy + math.sin(ang) * r * .5 * tilt
        pm = shape_mask(W, H, deform(ellipse_pts(px, py, r * .5, r * .34, 9, ang + math.pi / 2), rng, 2, .1))
        shade = 0.5 + 0.5 * math.cos(ang - math.pi / 4)
        lay = glaze(lay, pig(pm, mix(light, mid, .3 + .4 * shade), seed=sd(), density=0.22 + 0.12 * shade, edge=0.55, bloom=0.3, rough=5))
    for k in range(petals):
        rr = r * (0.92 - k * (0.8 / petals))
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .035), cy - r * .04 + rng.gauss(0, r * .035), rr, a0, a0 + rng.uniform(1.5, 2.8), 26, tilt)
        sm = stroke_mask(W, H, pts, r * rng.uniform(0.09, 0.16))
        col = mix(mid, deep, k / petals)
        lay = glaze(lay, pig(sm, col, mix(col, light, .3), seed=sd(), density=0.36 + k * 0.035, edge=0.6, bloom=0.15, rough=3.5, feather=1.1))
    heart = shape_mask(W, H, deform(ellipse_pts(cx + r * .02, cy - r * .04, r * .15, r * .12, 8), rng, 1, .1))
    lay = glaze(lay, pig(heart, deep, seed=sd(), density=0.66, edge=0.7, bloom=0, rough=2.5))
    sh = shape_mask(W, H, deform(ellipse_pts(cx + r * .28, cy + r * .42, r * .7, r * .3, 9, -.35), rng, 2, .1)) * base
    lay = glaze(lay, pig(sh, deep, seed=sd(), density=0.16, edge=0.2, bloom=0.4, rough=6))
    return lay, base


def bud(W, H, x, y, s, ang, col, deep, green, sd, rng):
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 2.0, s * .62, ang, n=12), rng, 1, .06))
    lay = pig(m, col, deep, seed=sd(), density=0.58, edge=0.6, rough=3)
    sp = stroke_mask(W, H, [(x + math.cos(ang) * s * .2, y + math.sin(ang) * s * .2), (x + math.cos(ang) * s * 1.2, y + math.sin(ang) * s * 1.2)], s * .5)
    lay = glaze(lay, pig(sp, deep, seed=sd(), density=0.3, edge=0.4, rough=2))
    for side in (-1, 1):
        sep = shape_mask(W, H, petal_pts(x, y, s * 1.1, s * .25, ang + side * .5, n=10))
        lay = glaze(lay, pig(sep, green, seed=sd(), density=0.55, edge=0.5, rough=2))
    return lay, m


def dots(W, H, cx, cy, sx, sy, n, rmin, rmax, rng):
    def draw(cv):
        for _ in range(n):
            cv.c.drawCircle(cx + rng.gauss(0, sx), cy + rng.gauss(0, sy), rng.uniform(rmin, rmax), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(W, H, draw)


def preview(arr, path, tone):
    on_paper(arr, tone).save(path)


def preview_dark(arr, path, bg="#0b0b0c"):
    h, w = arr.shape[:2]
    b = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = b * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(path)


def flip_h(arr):
    return arr[:, ::-1].copy()


def paper_tile(size=512, tone="#fbf8f6", seed=3, mottle=1.0, fine=1.0, fiber=1.0, strength=1.0):
    """Seamless paper grain tile (gaussian filters with wrap) — use with mix-blend-mode/background-blend multiply."""
    r = np.random.default_rng(seed)
    g = lambda s: (lambda a: (a - a.mean()) / (a.std() + 1e-6))(gaussian_filter(r.random((size, size)).astype(np.float32), s, mode="wrap"))
    v = 1 + strength * (g(36) * 0.02 * mottle + g(0.7) * 0.016 * fine + g((0.5, 5)) * 0.012 * fiber)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    return Image.fromarray((np.clip(base * v[..., None], 0, 1) * 255).astype(np.uint8), "RGB")
