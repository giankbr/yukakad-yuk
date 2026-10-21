"""Agent J2 helpers (gebyok-sogan, busana-jawi): _p1_lib re-export + local-crop media + botanical blocks.
Previews go to /tmp/pen/nj-J2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nj-J2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _p1_lib import *  # noqa
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter

PREV = _p1_lib.PREV


def trim_cache():
    if len(_art._fbm_cache) > 10:
        _art._fbm_cache.clear()


def _bbox(mask, pad):
    ys, xs = np.nonzero(mask > 0.01)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def local(fn, mask, *a, pad=40, **k):
    """Run a medium function only on the mask's bbox; returns full-size RGBA."""
    trim_cache()
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


def fl(mask, *a, **k):
    return local(foil, mask, *a, **k)


def union(*ms):
    return np.maximum.reduce(ms)


def spiral(cx, cy, r0, r1, a0, turns, n=60, ccw=1):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + ccw * t * turns * math.tau
        r = r0 + (r1 - r0) * t
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


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


def rose(W, H, cx, cy, r, light, mid, deep, sd, rng, petals=10, tilt=0.86):
    """Loose watercolour garden rose."""
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * tilt, 10), rng, 2, 0.12))
    lay = pig(base, light, mid, seed=sd(), density=0.44, edge=0.38, bloom=0.5, rough=9, holes=0.08)
    for k in range(6):
        ang = k / 6 * math.tau + rng.uniform(-.3, .3)
        px, py = cx + math.cos(ang) * r * .55, cy + math.sin(ang) * r * .5 * tilt
        pm = shape_mask(W, H, deform(ellipse_pts(px, py, r * .5, r * .34, 9, ang + math.pi / 2), rng, 2, .1))
        shade = 0.5 + 0.5 * math.cos(ang - math.pi / 4)
        lay = glaze(lay, pig(pm, mix(light, mid, .3 + .4 * shade), seed=sd(), density=0.22 + 0.14 * shade, edge=0.6, bloom=0.3, rough=5))
    for k in range(petals):
        rr = r * (0.92 - k * (0.8 / petals))
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .035), cy - r * .04 + rng.gauss(0, r * .035), rr, a0, a0 + rng.uniform(1.5, 2.8), 26, tilt)
        sm = stroke_mask(W, H, pts, r * rng.uniform(0.09, 0.16))
        col = mix(mid, deep, k / petals)
        lay = glaze(lay, pig(sm, col, mix(col, light, .3), seed=sd(), density=0.36 + k * 0.035, edge=0.6, bloom=0.15, rough=3.5, feather=1.1))
    heart = shape_mask(W, H, deform(ellipse_pts(cx + r * .02, cy - r * .04, r * .15, r * .12, 8), rng, 1, .1))
    lay = glaze(lay, pig(heart, deep, seed=sd(), density=0.7, edge=0.7, bloom=0, rough=2.5))
    sh = shape_mask(W, H, deform(ellipse_pts(cx + r * .28, cy + r * .42, r * .7, r * .3, 9, -.35), rng, 2, .1)) * base
    lay = glaze(lay, pig(sh, deep, seed=sd(), density=0.18, edge=0.2, bloom=0.4, rough=6))
    return lay, base


def peony(W, H, cx, cy, r, light, mid, deep, sd, rng, tilt=0.8):
    """Ruffled peony: many scalloped petals in rings, cupped at the back, frilly centre."""
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * 1.05, r * tilt, 12), rng, 2, 0.14))
    lay = pig(base, light, light, seed=sd(), density=0.36, edge=0.3, bloom=0.55, rough=10, holes=0.06)
    for ring, (rf, n, dens) in enumerate([(0.78, 9, 0.2), (0.56, 8, 0.26), (0.36, 7, 0.32)]):
        for k in range(n):
            ang = k / n * math.tau + rng.uniform(-.25, .25) + ring * 0.4
            px, py = cx + math.cos(ang) * r * rf * 0.7, cy + math.sin(ang) * r * rf * 0.7 * tilt
            pr = r * (0.42 - ring * 0.08)
            pts = ellipse_pts(px, py, pr, pr * 0.72, 14, ang + math.pi / 2)
            # scalloped ruffle
            pts = [(x + math.cos(i * 2.1) * pr * 0.06, y + math.sin(i * 1.7) * pr * 0.06) for i, (x, y) in enumerate(pts)]
            pm = shape_mask(W, H, deform(pts, rng, 2, .1))
            shade = 0.5 + 0.5 * math.cos(ang - math.pi / 4)
            col = mix(light, mid, 0.25 + 0.35 * shade + ring * 0.12)
            lay = glaze(lay, pig(pm, col, mix(col, light, .4), seed=sd(), density=dens + 0.06 * shade, edge=0.7, bloom=0.3, rough=4.5))
    # frilly centre strokes
    for k in range(9):
        a0 = rng.uniform(0, math.tau)
        rr = r * rng.uniform(0.08, 0.24)
        pts = arc_pts(cx + rng.gauss(0, r * .05), cy - r * .05 + rng.gauss(0, r * .04), rr, a0, a0 + rng.uniform(1.2, 2.2), 18, tilt)
        lay = glaze(lay, pig(stroke_mask(W, H, pts, r * rng.uniform(0.05, 0.09)), mix(mid, deep, rng.uniform(.4, .9)), seed=sd(), density=0.5, edge=0.6, bloom=0, rough=2.5, feather=0.9))
    sh = shape_mask(W, H, deform(ellipse_pts(cx + r * .25, cy + r * .45, r * .8, r * .32, 9, -.3), rng, 2, .1)) * base
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


def preview_dark(arr, name, bg="#1a120c"):
    preview(arr, name, bg=bg)


def kb_total(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")
