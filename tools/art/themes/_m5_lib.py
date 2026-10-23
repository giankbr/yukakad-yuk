"""Agent M5 helpers (pekalongan-buketan, fanous-mesir, loft-industri, ultah-musik).
Builds on _j1_lib (bbox-local G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds: batik dye + canting line + cecek
dots, ink outlines, polygon helpers, cloth/brick/concrete texture helpers. Previews -> /tmp/pen/nb-M5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _j1_lib  # noqa
from _j1_lib import *  # noqa
import art as _art

PREV = "/tmp/pen/nb-M5/art"
os.makedirs(PREV, exist_ok=True)
_j1_lib.PREV = PREV
import _p1_lib
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def rgba(rgb, a):
    return np.concatenate([rgb, a[..., None] if a.ndim == 2 else a], -1).astype(np.float32)


def flat(h, w, col):
    return np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)


def noise(w, h, seed, sigma, wrap=False):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap" if wrap else "reflect")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def rotp(pts, cx, cy, ang):
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def wob(pts, rng, amt):
    return [(x + rng.uniform(-amt, amt), y + rng.uniform(-amt, amt)) for x, y in pts]


def lines(W, H, polys, width, closed=True, smooth=True):
    """Stroked outlines of many polygons/polylines into one mask."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    for pts in polys:
        path = smooth_path(pts, closed) if smooth else None
        if path is None:
            path = skia.Path(); path.moveTo(*pts[0])
            for q in pts[1:]:
                path.lineTo(*q)
            if closed:
                path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def outline_of(mask, px=1.6):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.03).astype(np.float32) - (gaussian_filter(mask, 0.6) > 0.5), 0, 1)


def ink(mask, col="#2a1f2a", seed=1, alpha=0.92, bleed=0.0):
    h, w = mask.shape
    m = displace(mask, seed, 0.8, 6)
    if bleed:
        m = np.maximum(m, gaussian_filter(m, 1.6) * bleed)
    a = np.clip(gaussian_filter(m, 0.45) * 1.3, 0, 1) * alpha * (0.72 + 0.28 * noise(w, h, seed + 1, 2.5))
    return rgba(flat(h, w, col), a)


def K(dst, mask, *a, pad=6, **k):
    return OV(dst, mask, lambda m: ink(m, *a, **k), pad=pad)


def dye(mask, col, col2=None, seed=1, density=0.9, mottle=0.35):
    """Batik dye in cotton: soft but contained (wax-resisted) edge, uneven take-up, faint weave streaks."""
    h, w = mask.shape
    m = displace(mask, seed, 1.2, 10)
    m = np.clip((gaussian_filter(m, 0.9) - 0.2) * 1.6, 0, 1)
    low = fbm(w, h, seed + 3, 40, 3)
    a = m * density * (1 - mottle + mottle * (0.4 + 0.6 * low))
    wv = noise(w, h, seed + 4, (0.4, 3.0)) * 0.5 + noise(w, h, seed + 5, (3.0, 0.4)) * 0.5
    a *= 0.86 + 0.28 * wv
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 13, 55, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    return rgba(np.clip(rgb, 0, 1), np.clip(a, 0, 1))


def D(dst, mask, *a, pad=10, **k):
    return OV(dst, mask, lambda m: dye(m, *a, **k), pad=pad)


def offset_poly(pts, d):
    """Offset a closed polygon inward (d>0 shrinks toward centroid-ish via normals)."""
    n = len(pts); out = []
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    for i in range(n):
        x, y = pts[i]
        dx, dy = cx - x, cy - y; L = math.hypot(dx, dy) or 1
        out.append((x + dx / L * d, y + dy / L * d))
    return out


def dots_along(pts, step, r, closed=True, jitter=0.0, rng=None):
    """Circles (x, y, r) spaced along a polyline."""
    c = curve(pts + ([pts[0]] if closed else []), max(40, len(pts) * 10))
    out = []; acc = 0.0
    for i in range(1, len(c)):
        seg = math.hypot(c[i][0] - c[i - 1][0], c[i][1] - c[i - 1][1]); acc += seg
        if acc >= step:
            acc = 0.0
            j = (rng.uniform(-jitter, jitter) if rng else 0)
            out.append((c[i][0] + j, c[i][1] + j, r * (rng.uniform(0.8, 1.15) if rng else 1)))
    return out


def ring(W, H, cx, cy, r, width):
    return ring_mask(W, H, cx, cy, r, width)


def tile_noise(w, h, seed, sigma):
    return wrap_noise(w, h, seed, sigma)


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s_ = os.path.getsize(os.path.join(d, f)); tot += s_
        print(f"  {f}: {s_ // 1024} KB")
    print(f"  total {tot // 1024} KB")


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in np.linspace(0, 1, n)]
