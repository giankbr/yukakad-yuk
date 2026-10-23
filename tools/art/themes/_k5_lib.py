"""Agent J5 helpers (batik-syari, hujan-kota, pesawat-kertas, kenduri-panen).
Builds on _i4_lib (-> _jw_lib/_j1_lib/_p1_lib + art.py): local bbox painting (G/GP/LC/FO/OV), col_arr, disc,
ring_mask, save/prev. Adds: seamless vertical tiles via crossfade, polygon helpers in rotated frames, paper-fold
shading, wet-reflection smear, rain streaks. Previews -> /tmp/pen/nb-J5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _i4_lib import *  # noqa
import _i4_lib, _jw_lib, _j1_lib, _p1_lib
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates, zoom

PREV = "/tmp/pen/nb-J5/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_i4_lib, _jw_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def seam_y(arr, H, O):
    """arr has height H+O and geometry periodic in H: crossfade the first O rows with rows H..H+O -> seamless H tile."""
    out = arr[:H].copy()
    t = (np.arange(O, dtype=np.float32) / O)[:, None, None]
    out[:O] = arr[H:H + O] * (1 - t) + arr[:O] * t
    return out


def seam_x(arr, W, O):
    return np.transpose(seam_y(np.transpose(arr, (1, 0, 2)), W, O), (1, 0, 2))


def poly(W, H, pts, smooth=True):
    return shape_mask(W, H, pts, smooth=smooth)


def polys(W, H, items, smooth=True):
    return shapes(W, H, items, smooth=smooth)


def rot_frame(ang, ox=0.0, oy=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    return lambda u, v: (ox + u * ca - v * sa, oy + u * sa + v * ca)


def lines_mask(W, H, segs, width, cap=True):
    """segs: list of point lists; constant-width polylines into one mask."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap, StrokeJoin=skia.Paint.kRound_Join)
    for pts in segs:
        path = skia.Path()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def rects(W, H, items, radius=0.0):
    """items: (x, y, w, h[, rot_deg]) filled (rounded) rects."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for it in items:
        x, y, w, h = it[:4]
        rot = it[4] if len(it) > 4 else 0
        cv.c.save(); cv.c.translate(x + w / 2, y + h / 2); cv.c.rotate(rot)
        cv.c.drawRoundRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), radius, radius, p)
        cv.c.restore()
    return cv.array()[..., 3]


def tint(mask, col, alpha=1.0, blur=0.0):
    m = gaussian_filter(mask, blur) if blur else mask
    return col_arr(m, col, m * alpha)


def lin_grad(W, H, x0, y0, x1, y1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = x1 - x0, y1 - y0
    return np.clip(((xx - x0) * dx + (yy - y0) * dy) / (dx * dx + dy * dy + 1e-6), 0, 1)


def flat_fill(W, H, col):
    return solid(W, H, col)


def reflect_smear(arr, y_line, strength=0.85, stretch=1.0, wob=6.0, seed=3, fade=0.75):
    """Mirror the part of `arr` above y_line below it, smeared vertically like wet asphalt reflections."""
    h, w = arr.shape[:2]
    out = arr.copy()
    n = h - y_line
    if n <= 0:
        return out
    yy = np.arange(n, dtype=np.float32)
    src_y = np.clip(y_line - 1 - yy / stretch, 0, h - 1)
    nx = (fbm(w, n, seed, 20, 3) - 0.5) * wob * 2
    YY = np.repeat(src_y[:, None], w, 1)
    XX = np.clip(np.arange(w, dtype=np.float32)[None, :] + nx, 0, w - 1)
    refl = np.stack([map_coordinates(arr[..., c], [YY, XX], order=1) for c in range(4)], -1)
    refl = gaussian_filter(refl, (6, 0.8, 0))
    k = (strength * (1 - fade * yy / n))[:, None, None]
    sub = out[y_line:]
    a = refl[..., 3:4] * k
    sub[..., :3] = sub[..., :3] * (1 - a) + refl[..., :3] * a
    out[y_line:] = sub
    return out


def rain_streaks(W, H, n, seed, length=(18, 40), width=1.1, ang=0.12):
    rng = np.random.default_rng(seed)
    segs = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        L = rng.uniform(*length)
        segs.append([(x, y), (x + math.sin(ang) * L, y + math.cos(ang) * L)])
    return lines_mask(W, H, segs, width)
