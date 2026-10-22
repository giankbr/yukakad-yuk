"""Agent G5 helpers (lengkung-putih, aurora-utara, ladang-tulip, buka-bersama).
Builds on _a2_lib / _j1_lib (bbox-cropped G/GP/LC/FO, batched strokes/shapes, pine_polys, ridge_mask) and adds:
arch geometry in one-point perspective, aurora curtains, tulip heads, lantern + date helpers. Previews -> /tmp/pen/nb-G5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-G5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def arch_pts(cx, floor, half, spring, n=28, pointed=0.0):
    """Round-headed (or slightly pointed) arch opening outline: floor-left -> up -> over -> down -> floor-right.
    spring = height of the straight jamb above floor; pointed in 0..0.4 lifts the crown into a soft point."""
    pts = [(cx - half, floor), (cx - half, floor - spring)]
    top = floor - spring
    for i in range(1, n):
        t = i / n
        a = math.pi * (1 - t)
        x = cx + math.cos(a) * half
        y = top - math.sin(a) * half
        if pointed:
            y -= pointed * half * (1 - abs(2 * t - 1)) ** 2 * 0.9
        pts.append((x, y))
    pts += [(cx + half, floor - spring), (cx + half, floor)]
    return pts


def poly_fill(W, H, polys):
    return shapes(W, H, polys, smooth=False)


def poly_stroke(W, H, polys, width, closed=False):
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                   StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap)
    for pts in polys:
        path = skia.Path(); path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        if closed:
            path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def soften(mask, s=1.0):
    return gaussian_filter(mask, s)


def lighten(arr, mask, col, amt=1.0):
    """Pull colours towards col (paper lifted / light)."""
    out = arr.copy()
    m = np.clip(mask * amt, 0, 1)[..., None]
    out[..., :3] = out[..., :3] * (1 - m) + np.array(hex_rgb(col), np.float32) * m
    return out


def screen_add(arr, mask, col, amt=1.0):
    out = arr.copy()
    c = np.array(hex_rgb(col), np.float32)
    m = np.clip(mask * amt, 0, 1)[..., None]
    out[..., :3] = 1 - (1 - out[..., :3]) * (1 - c * m)
    return out


def tulip_head(cx, cy, s, ang=0.0, rng=None, open_=0.0):
    """Three cupped petals of a tulip, returned as polygons (back petal, left, right). s = head height."""
    rng = rng or random.Random(1)
    ca, sa = math.cos(ang), math.sin(ang)
    def T(pts):
        return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    w = s * 0.42 * (1 + open_ * 0.3)
    back = [(-w * 0.9, -s * 0.15), (-w * 0.55, -s * 0.95), (-w * 0.2, -s * 0.72), (0, -s * 1.02), (w * 0.2, -s * 0.72), (w * 0.55, -s * 0.95), (w * 0.9, -s * 0.15), (w * 0.6, s * 0.2), (0, s * 0.28), (-w * 0.6, s * 0.2)]
    left = [(-w * 1.0, -s * 0.2), (-w * (0.8 + open_ * .3), -s * 0.88), (-w * 0.2, -s * 0.5), (w * 0.15, -s * 0.05), (0, s * 0.3), (-w * 0.65, s * 0.22)]
    right = [(w * 1.0, -s * 0.2), (w * (0.7 + open_ * .3), -s * 0.92), (w * 0.15, -s * 0.55), (-w * 0.2, -s * 0.05), (0, s * 0.3), (w * 0.65, s * 0.22)]
    return [T(wobble(p, rng, s * 0.015)) for p in (back, left, right)]


def crescent_mask(W, H, cx, cy, r, off=(0.38, -0.18), r2=0.86):
    a = circles(W, H, [(cx, cy, r)])
    b = circles(W, H, [(cx + r * off[0], cy + r * off[1], r * r2)])
    return np.clip(a - b, 0, 1)


def star_field(W, H, n, rng, ymax=None, rmin=0.6, rmax=1.8):
    ymax = ymax or H
    return circles(W, H, [(rng.uniform(0, W), rng.uniform(0, ymax) ** 1.0, rng.uniform(rmin, rmax) * (rng.random() ** 2.2 * 0.8 + 0.4)) for _ in range(n)])
