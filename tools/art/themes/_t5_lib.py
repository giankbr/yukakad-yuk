"""Agent T5 helpers (angklung-saung, lili-syari, stasiun-tua, lomba-masak).
Builds on _a2_lib (-> _j1_lib / _p1_lib / art): bbox-cropped G/GP/LC/FO/OV, batched strokes/shapes.
Adds: bamboo tubes, mask shortcuts, axis-aligned box masks, gradient shading. Previews -> /tmp/pen/nb-T5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-T5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def yx(W, H):
    return np.mgrid[0:H, 0:W].astype(np.float32)


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def ell(W, H, cx, cy, rx, ry, rot=0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def line(W, H, pts, width, taper=(0.15, 0.25)):
    return strokes(W, H, [(pts, width, taper)])


def rect(W, H, x0, y0, x1, y1, r=0.0):
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    if r:
        cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, p)
    else:
        cv.c.drawRect(skia.Rect(x0, y0, x1, y1), p)
    return cv.array()[..., 3]


def rings(W, H, items):
    """items: (cx, cy, r, width) stroked circles into one mask."""
    cv = Canvas(W, H)
    for cx, cy, r, wd in items:
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wd, Style=skia.Paint.kStroke_Style)
        cv.c.drawCircle(cx, cy, r, p)
    return cv.array()[..., 3]


def side_shade(mask, axis_from, axis_to, width):
    """0..1 field across a straight tube: 0 at the left edge (relative to the axis direction), 1 at the right edge."""
    H, W = mask.shape
    yy, xx = yx(W, H)
    (x0, y0), (x1, y1) = axis_from, axis_to
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nxn, nyn = -dy / L, dx / L
    d = ((xx - x0) * nxn + (yy - y0) * nyn) / max(1, width)
    return np.clip(d * 0.5 + 0.5, 0, 1)


def tube_poly(a, b, w0, w1=None):
    w1 = w0 if w1 is None else w1
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    nxn, nyn = -dy / L, dx / L
    return [(a[0] + nxn * w0 / 2, a[1] + nyn * w0 / 2), (b[0] + nxn * w1 / 2, b[1] + nyn * w1 / 2),
            (b[0] - nxn * w1 / 2, b[1] - nyn * w1 / 2), (a[0] - nxn * w0 / 2, a[1] - nyn * w0 / 2)]


def bamboo(art, W, H, a, b, wd, nx, light="#d8c27a", mid="#b39549", dark="#6f5524", nodes=(), medium="gouache", area=None, hi="#f3e6b4"):
    """Straight bamboo tube from a to b: body, shaded far side, light streak, node rings at fractions `nodes`."""
    m = poly(W, H, tube_poly(a, b, wd))
    if area is not None:
        np.maximum(area, m, out=area)
    if medium == "gouache":
        art = GP(art, m, light, mid, seed=nx(), rough=0.9, streak=1.0)
    else:
        art = G(art, m, light, mid, seed=nx(), density=0.9, edge=0.45, bloom=0.15, rough=1.2, feather=0.6)
    sh = side_shade(m, a, b, wd)
    art = OV(art, m * np.clip((sh - 0.55) * 2.2, 0, 1), lambda mm: rgba(dark, mm * 0.55))
    art = OV(art, m * np.clip(1 - abs(sh - 0.3) * 7, 0, 1), lambda mm: rgba(hi, mm * 0.55))
    if nodes:
        items = []
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nxn, nyn = -dy / L, dx / L
        for t in nodes:
            cx, cy = a[0] + dx * t, a[1] + dy * t
            items.append(([(cx + nxn * wd * .56, cy + nyn * wd * .56), (cx - nxn * wd * .56, cy - nyn * wd * .56)], max(1.2, wd * 0.09), None))
        nm = strokes(W, H, items)
        art = OV(art, nm, lambda mm: rgba(dark, mm * 0.75))
        hl = strokes(W, H, [([(p[0][0] + dx / L * wd * .12, p[0][1] + dy / L * wd * .12), (p[1][0] + dx / L * wd * .12, p[1][1] + dy / L * wd * .12)], max(1, wd * 0.06), None) for p, *_ in items]) * m
        art = OV(art, hl, lambda mm: rgba(hi, mm * 0.6))
    return art


def vgrad(W, H, y0, y1):
    yy = yx(W, H)[0]
    return np.clip((yy - y0) / max(1, y1 - y0), 0, 1)


def save_prev(arr, name, tone="#fbf6ee", bg=None):
    preview(arr, name, tone=tone, bg=bg)
