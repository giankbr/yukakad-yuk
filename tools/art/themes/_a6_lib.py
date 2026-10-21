"""Agent A6 helpers (ultah-dino, baby-shower-awan, reuni-sekolah, sweet-seventeen): _j1_lib (bbox-local painting) +
soft gouache shading, crayon outlines, ballpoint ink, chalk, satin sheen and pearls. Previews -> /tmp/pen/nb-A6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-A6/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-A6/art"
_j1_lib.PREV = _p1_lib.PREV
from _jw_lib import hills, spiral_pts, along  # noqa
import art as _art


def clear():
    _art._fbm_cache.clear()


def col_arr(mask, col, alpha):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(alpha, 0, 1)[..., None]], -1)


def tint(dst, soft, col, amt=0.5, seed=1, streak=0.6, clip=True):
    """Soft opaque-paint shading (gouache glaze): alpha follows a soft mask with brush-streak breakup, kept inside dst."""
    h, w = soft.shape
    b = bbox(soft, 4, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    s = soft[y0:y1, x0:x1]
    st = gaussian_filter(np.random.default_rng(seed).random(s.shape).astype(np.float32), (1.2, 2.2))
    st = (st - st.mean()) / (st.std() + 1e-6)
    lo = fbm(x1 - x0, y1 - y0, seed + 3, 26, 3) - 0.5
    a = s * amt * np.clip(1 + st * 0.12 * streak + lo * 0.6 * streak, 0, 2)
    if clip:
        a = a * dst[y0:y1, x0:x1, 3]
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], col_arr(s, col, a))
    return out


def side_light(mask, dx, dy, blur):
    """Soft shading field: where mask shifted toward the light no longer covers -> shadow side (0..1)."""
    sh = np.roll(np.roll(gaussian_filter(mask, blur), int(dy), 0), int(dx), 1)
    return np.clip(mask - sh, 0, 1) * mask


def rim(mask, px=2.0):
    """Outline band around a mask."""
    d = (gaussian_filter(mask, px * 0.7) > 0.03).astype(np.float32)
    return np.clip(gaussian_filter(d, 0.6) - mask * 0.98, 0, 1)


def inner_edge(mask, px=2.0):
    return np.clip(mask - (gaussian_filter(mask, px) > 0.97).astype(np.float32), 0, 1) * mask


def crayon(dst, mask_line, col, seed=1, amt=0.85, tooth=0.45):
    """Coloured-pencil/crayon line: paper tooth breaks the stroke."""
    b = bbox(mask_line, 4, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = mask_line[y0:y1, x0:x1]
    g = gaussian_filter(np.random.default_rng(seed).random(m.shape).astype(np.float32), 0.55)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    a = m * amt * np.clip((g - tooth * 0.6) * 2.4, 0.15, 1)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], col_arr(m, col, a))
    return out


def ballpoint(dst, items, col="#24357a", seed=1, W=None, H=None):
    """Ballpoint pen: thin line, pressure varies, occasional skip and ink blob; items = [(pts, width)]."""
    h, w = dst.shape[:2]
    rng = random.Random(seed)
    cv = Canvas(w, h)
    for pts, wd in items:
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            pr = 0.55 + 0.45 * math.sin(math.pi * t) ** 0.4
            if rng.random() < 0.025:
                continue
            p = skia.Paint(AntiAlias=True, Color4f=color("#ffffff", min(1, 0.55 + 0.45 * pr * rng.uniform(0.8, 1.1))),
                           StrokeWidth=max(0.6, wd * pr), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
            cv.c.drawLine(*pts[i], *pts[i + 1], p)
        if rng.random() < 0.4:  # blob at stroke start
            cv.c.drawCircle(*pts[0], wd * 0.9, skia.Paint(AntiAlias=True, Color4f=color("#ffffff", 0.9)))
    m = cv.array()[..., 3]
    m = displace(m, seed, 0.8, 8)
    return OV(dst, m, lambda mm: col_arr(mm, col, mm * 0.92), pad=6)


def chalk(dst, items, col="#f4f1e6", seed=1, amt=0.92, grain=0.55):
    """Dry chalk on slate: streaky, broken by the board's tooth, soft dust halo."""
    h, w = dst.shape[:2]
    m = strokes(w, h, items)
    b = bbox(m, 10, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    mm = m[y0:y1, x0:x1]
    mm = displace(mm, seed, 1.2, 10)
    g = gaussian_filter(np.random.default_rng(seed).random(mm.shape).astype(np.float32), (0.5, 1.2))
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    a = mm * np.clip((g - grain * 0.55) * 2.6, 0, 1) * amt
    dust = gaussian_filter(mm, 3.5) * 0.18
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], col_arr(mm, col, np.clip(a + dust, 0, 1)))
    return out


def sheen(dst, mask, along_fn, col_hi="#ffffff", col_lo=None, amt=0.6, seed=1, freq=1.0, warp=0.8):
    """Satin sheen: bands of light along a scalar field (e.g. distance across a ribbon) inside mask."""
    b = bbox(mask, 2, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    f = along_fn(xx, yy)
    band = 0.5 + 0.5 * np.cos(f * freq + (fbm(x1 - x0, y1 - y0, seed, 90, 2) - 0.5) * 2.2 * warp)
    m = mask[y0:y1, x0:x1]
    out = dst.copy()
    hi = np.clip((band - 0.62) * 2.6, 0, 1) ** 1.4 * m * amt
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], col_arr(m, col_hi, hi))
    if col_lo:
        lo = np.clip((0.35 - band) * 2.2, 0, 1) * m * amt * 0.7
        out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], col_arr(m, col_lo, lo))
    return out


def pearl(dst, x, y, r, seed=1, base="#f4ece6", warm="#f2d6d0", cool="#d6dbe8", shadow="#a89a9e"):
    """One painted pearl: soft body, iridescent drift, rim shadow, crisp catchlight."""
    h, w = dst.shape[:2]
    rng = random.Random(seed)
    x0, x1 = int(max(0, x - r * 2)), int(min(w, x + r * 2 + 1))
    y0, y1 = int(max(0, y - r * 2)), int(min(h, y + r * 2 + 1))
    if x1 <= x0 or y1 <= y0:
        return dst
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
    m = np.clip((1 - d) * r * 0.9, 0, 1)
    lx, ly = -0.38, -0.42
    nd = np.sqrt((xx - x - lx * r) ** 2 + (yy - y - ly * r) ** 2) / r
    lum = np.clip(1.05 - nd * 0.42, 0, 1)
    ca, cb, cc, cs = (np.array(hex_rgb(c), np.float32) for c in (base, warm, cool, shadow))
    t = np.clip((xx - x) / r * 0.5 + 0.5 + rng.uniform(-.2, .2), 0, 1)[..., None]
    rgb = ca * (1 - t) * 0.6 + cb * t * 0.6 + cc * (1 - t) * t * 1.6 * 0.4 + ca * 0.4 * 0
    rgb = rgb / np.maximum(rgb.max(), 1e-3) * ca.max()
    rgb = rgb * lum[..., None] + cs * (1 - lum[..., None]) * 0.55
    rgb = np.clip(rgb + np.clip(0.75 - d, 0, 1)[..., None] * 0.02, 0, 1)
    cl = np.clip(1 - np.sqrt((xx - x + r * 0.34) ** 2 + (yy - y + r * 0.38) ** 2) / (r * 0.22), 0, 1) ** 1.2
    rgb = rgb * (1 - cl[..., None]) + cl[..., None]
    out = dst.copy()
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], np.concatenate([rgb, m[..., None]], -1))
    return out


def spark(dst, x, y, r, col="#fff4f8", amt=1.0, rot=0.0, glow_col=None):
    """Hand-painted 4-point glint: four slim concave petals (long vertical pair), tiny core, soft halo."""
    h, w = dst.shape[:2]
    polys = []
    for k in range(4):
        a = rot + k * math.pi / 2 - math.pi / 2
        L = r * (1.0 if k % 2 == 0 else 0.6)
        polys.append(petal_pts(x, y, L, L * 0.17, a, n=14))
    m = shapes(w, h, polys)
    if glow_col:
        dst = OV(dst, m, lambda mm: col_arr(mm, glow_col, np.clip(gaussian_filter(mm, r * 0.3) * 1.5, 0, 1) * 0.5 * amt), pad=int(r))
    return OV(dst, m, lambda mm: col_arr(mm, col, np.clip(gaussian_filter(mm, 0.6), 0, 1) * amt), pad=6)


def lerp_pts(a, b, n):
    return [(a[0] + (b[0] - a[0]) * i / (n - 1), a[1] + (b[1] - a[1]) * i / (n - 1)) for i in range(n)]
