"""Agent L6 helpers (sabana-afrika, miami-deco, letterpress, bakti-sosial): _j1_lib (local painting G/GP/LC/FO/OV,
strokes/shapes/circles/ellipses/hatch) + flat/rgba/ramp, emboss shading and a few motif builders. Previews -> /tmp/pen/nb-L6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-L6/art"
os.makedirs(PREV, exist_ok=True)


def show(arr, name, tone="#f4eee3", bg=None):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return rgba(rgb, mask * alpha)


def ramp(t, stops):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float32)
    ps = [p for p, _ in stops]
    cs = [np.array(hex_rgb(c), np.float32) for _, c in stops]
    for i in range(len(stops) - 1):
        k = np.clip((t - ps[i]) / max(1e-6, ps[i + 1] - ps[i]), 0, 1)[..., None]
        sel = ((t >= ps[i]) & (t <= ps[i + 1]))[..., None]
        out = np.where(sel, cs[i] * (1 - k) + cs[i + 1] * k, out)
    return out


def emboss_light(mask, blur=1.6, k=3.0, lx=-1.0, ly=-1.0):
    gy, gx = np.gradient(gaussian_filter(mask, blur))
    return (gx * lx + gy * ly) * k


def rr(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect(w, h, items):
    """Rounded rects: (x0, y0, x1, y1, r)."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for x0, y0, x1, y1, r in items:
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), p)
    return cv.array()[..., 3]


def wavy_band(W, H, y_top, y_bot, amp, seed, wl=0.6):
    """Horizontal band between two hand-cut wavy edges."""
    rng = random.Random(seed)
    ph1, ph2 = rng.uniform(0, 6), rng.uniform(0, 6)
    top = [(x, y_top + amp * math.sin(x / (W * wl) * math.tau + ph1) + rng.uniform(-amp * .25, amp * .25)) for x in range(-20, W + 41, 30)]
    bot = [(x, y_bot + amp * math.sin(x / (W * wl * 0.8) * math.tau + ph2) + rng.uniform(-amp * .25, amp * .25)) for x in range(W + 40, -41, -30)]
    return shapes(W, H, [top + bot], smooth=True)


def dabs(W, H, n, box, rmin, rmax, rng, squash=1.0):
    x0, y0, x1, y1 = box
    return ellipses(W, H, [(rng.uniform(x0, x1), rng.uniform(y0, y1), r, r * squash, rng.uniform(-30, 30)) for r in [rng.uniform(rmin, rmax) for _ in range(n)]])


def acacia(W, H, x, by, h, rng, spread=1.0):
    """Flat-topped umbrella acacia: forked trunk mask + canopy mask (layered flat lobes with a ragged underside)."""
    top = by - h
    cw = h * 0.95 * spread
    items = [(curve([(x, by), (x + rng.uniform(-6, 6), by - h * 0.35), (x + rng.uniform(-10, 10), by - h * 0.55)], 20), h * 0.07, (0.02, 0.35))]
    fx, fy = items[0][0][-1]
    for k in range(5):
        tx = x + (k - 2) / 2 * cw * 0.42 + rng.uniform(-8, 8)
        ty = top + h * rng.uniform(0.12, 0.2)
        mx = fx + (tx - fx) * 0.5 + rng.uniform(-10, 10)
        items.append((curve([(fx, fy), (mx, fy - (fy - ty) * 0.55), (tx, ty)], 16), h * (0.035 if k in (0, 4) else 0.045), (0.05, 0.6)))
    trunk = strokes(W, H, items)
    lobes = []
    for k in range(7):
        cx = x + rng.uniform(-0.42, 0.42) * cw
        cy = top + h * rng.uniform(0.02, 0.14)
        lobes.append((cx, cy, cw * rng.uniform(0.18, 0.3), h * rng.uniform(0.05, 0.085), rng.uniform(-4, 4)))
    lobes.append((x, top + h * 0.08, cw * 0.5, h * 0.07, 0))
    for _ in range(46):
        cx = x + rng.uniform(-0.48, 0.48) * cw
        lobes.append((cx, top + h * rng.uniform(0.1, 0.19), h * rng.uniform(0.02, 0.05), h * rng.uniform(0.012, 0.03), rng.uniform(-20, 20)))
    canopy = ellipses(W, H, lobes)
    return trunk, canopy


def giraffe(W, H, x, by, h, rng, face=1):
    """Silhouette giraffe (side view), standing; h = height to the head top. Sloping back, long tapered legs."""
    s = h / 100.0
    f = face
    X = lambda dx: x + dx * s * f
    body = shapes(W, H, [[(X(-20), by - 50 * s), (X(-12), by - 56 * s), (X(4), by - 61 * s), (X(16), by - 64 * s), (X(22), by - 58 * s),
                          (X(20), by - 48 * s), (X(6), by - 45 * s), (X(-12), by - 44 * s), (X(-21), by - 46 * s)]])
    neck = shapes(W, H, [[(X(12), by - 63 * s), (X(23), by - 91 * s), (X(27), by - 92 * s), (X(23), by - 70 * s), (X(22), by - 57 * s)]])
    head = ellipses(W, H, [(X(29), by - 92 * s, 6.2 * s, 2.8 * s, 28 * f), (X(25), by - 93 * s, 3.4 * s, 3.4 * s, 0)])
    oss = strokes(W, H, [([(X(24), by - 95 * s), (X(23), by - 99.5 * s)], 1.5 * s, None), ([(X(26.5), by - 95 * s), (X(26.5), by - 99.5 * s)], 1.5 * s, None),
                         ([(X(22), by - 93 * s), (X(19), by - 95 * s)], 1.6 * s, (0.0, 0.5))])
    legs = strokes(W, H, [(curve([(X(a), by - top * s), (X(a + m), by - top * s * 0.5), (X(a + d), by)], 12), wd * s, (0.0, 0.6))
                          for a, m, d, top, wd in ((-17, -1, -4, 48, 4.2), (-12, 1, 1, 46, 3.8), (13, 0, 3, 49, 4.2), (18, 1, -1, 52, 3.8))])
    tail = strokes(W, H, [([(X(-20), by - 50 * s), (X(-23), by - 38 * s)], 1.3 * s, (0.0, 0.2))])
    return np.clip(body + neck + head + oss + legs + tail, 0, 1)


def elephant(W, H, x, by, h, rng, face=1):
    s = h / 50.0
    f = face
    body = ellipses(W, H, [(x, by - 27 * s, 26 * s, 17 * s, 0), (x - 8 * s * f, by - 30 * s, 18 * s, 16 * s, 0)])
    head = ellipses(W, H, [(x + 24 * s * f, by - 32 * s, 12 * s, 12 * s, 0), (x + 18 * s * f, by - 30 * s, 10 * s, 13 * s, 10)])
    trunk = strokes(W, H, [([(x + 32 * s * f, by - 30 * s), (x + 36 * s * f, by - 18 * s), (x + 35 * s * f, by - 6 * s), (x + 39 * s * f, by - 3 * s)], 6 * s, (0.0, 0.5))])
    legs = shapes(W, H, [rr(min(x + a * s * f, x + (a + 8) * s * f), by - 20 * s, max(x + a * s * f, x + (a + 8) * s * f), by) for a in (-22, -10, 8, 18)], smooth=False)
    return np.clip(body + head + trunk + legs, 0, 1)


def tile_pad(arr):
    return arr


def hills(W, H, y, amp, seed, wl=0.5):
    rng = random.Random(seed)
    pts = [(-20, H + 20)]
    ph = rng.uniform(0, 6)
    for i in range(0, W + 41, 20):
        pts.append((i - 20, y - amp * (0.6 * math.sin(i / (W * wl) * math.pi * 2 + ph) + 0.4 * math.sin(i / (W * wl * 0.37) + ph * 2))))
    pts.append((W + 20, H + 20))
    return shapes(W, H, [pts], smooth=False)
