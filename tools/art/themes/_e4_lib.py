"""Agent E4 helpers (retro-70an, merak-nouveau, shan-shui, gurun-kaktus): builds on _d4_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, sumi ink, layer, save...) and adds directional dry-brush gouache,
film grain, ink-wash mountains (cun texture strokes), peacock-eye rings and cactus rib shading.
Previews -> /tmp/pen/nb-E4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _d4_lib import *  # noqa
import _d4_lib, _a5_lib, _j1_lib, _p1_lib
PREV = "/tmp/pen/nb-E4/art"
os.makedirs(PREV, exist_ok=True)
_d4_lib.PREV = _a5_lib.PREV = _j1_lib.PREV = _p1_lib.PREV = PREV
from scipy.ndimage import map_coordinates as _mc, gaussian_filter as _gf

_NOISE = {}


def streak_tex(seed, along=14.0, across=0.7, size=(384, 1536)):
    key = (seed, along, across, size)
    if key not in _NOISE:
        n = _gf(np.random.default_rng(seed).random(size).astype(np.float32), (across, along), mode="wrap")
        _NOISE[key] = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return _NOISE[key]


def streaks_uv(u, v, seed, along=14.0, across=0.7):
    """Sample an anisotropic streak noise at stroke coordinates u (along the brush) and v (across)."""
    t = streak_tex(seed, along, across)
    return _mc(t, [v % t.shape[0], u % t.shape[1]], order=1, mode="wrap").astype(np.float32)


def dry_gouache(mask, col, col2=None, seed=1, u=None, v=None, dry=0.45, streak=1.0, rough=2.5, density=0.97, edge_dry=0.6):
    """Opaque gouache laid with a fairly dry brush: streaks follow (u, v) stroke coords (default horizontal);
    bristle gaps open up near the edges and where the paint runs out."""
    h, w = mask.shape
    if u is None:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        u, v = xx, yy
    m = displace(mask, seed, rough, 24)
    m = np.clip((_gf(m, 0.6) - 0.35) * 2.4, 0, 1)
    s = streaks_uv(u, v, seed)
    s2 = streaks_uv(u * 0.5 + 77, v * 2.0, seed + 1, 30, 0.6)
    edge = np.clip(1 - _gf(mask, 5.0) * 1.6, 0, 1)  # 1 near the edges
    thr = 1 - dry * (0.35 + edge_dry * edge)
    gaps = np.clip((s - thr) * 7, 0, 1)
    a = m * (1 - gaps) * density
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 3, 90, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    rgb = rgb * (1 + (s2[..., None] - 0.5) * 0.12 * streak + (s[..., None] - 0.5) * 0.06 * streak)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def polar_uv(h, w, cx, cy, scale=1.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.hypot(xx - cx, yy - cy)
    th = np.arctan2(yy - cy, xx - cx)
    return th * 260 * scale, r  # u along the arc, v across


def DG(dst, mask, *a, pad=14, **k):
    """over: dry_gouache computed inside the mask bbox (u/v given as full-size arrays are cropped too)."""
    trim_cache()
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    if k.get("u") is not None:
        k = dict(k); k["u"] = k["u"][y0:y1, x0:x1]; k["v"] = k["v"][y0:y1, x0:x1]
    src = dry_gouache(np.ascontiguousarray(mask[y0:y1, x0:x1]), *a, **k)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    return out


def film_grain_tile(size=256, seed=5, amount=1.0):
    """Grey film grain with alpha (overlay on photos)."""
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (size, size)).astype(np.float32)
    g = _gf(g, 0.55, mode="wrap") * 2.2 + _gf(rng.normal(0, 1, (size, size)).astype(np.float32), 1.4, mode="wrap") * 1.2
    g = np.clip(0.5 + g * 0.22 * amount, 0, 1)
    rgb = np.repeat(g[..., None], 3, -1)
    a = np.clip(np.abs(g - 0.5) * 2.2, 0, 1) * 0.9
    return np.concatenate([rgb, a[..., None]], -1)


def paper_tile(size, tone, seed=3, fiber=0.6, mottle=0.6, specks=0.0, speck_col="#6b4a2a"):
    """Seamless paper tile (RGB float)."""
    rng = np.random.default_rng(seed)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    big = wrap_noise(size, size, seed, 28) - 0.5
    fine = wrap_noise(size, size, seed + 1, 0.7) - 0.5
    fib = _gf(rng.random((size, size)).astype(np.float32), (0.5, 5), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    v = 1 + big * 0.1 * mottle + fine * 0.09 + fib * 0.02 * fiber
    out = base * v[..., None]
    if specks:
        sp = (rng.random((size, size)) > 1 - specks * 0.002).astype(np.float32)
        sp = _gf(sp, 0.7, mode="wrap") * 3
        c = np.array(hex_rgb(speck_col), np.float32)
        out = out * (1 - np.clip(sp, 0, 0.7)[..., None]) + c * np.clip(sp, 0, 0.7)[..., None]
    return np.clip(out, 0, 1)


def save_tile(rgb, path, quality=84):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")


def mountain_profile(x0, x1, base_y, peak_y, rng, n=9, sharp=1.4, jag=0.18):
    """Hand-drawn mountain ridge from x0..x1, peaking at ~peak_y; returns list of points (top ridge only)."""
    pts = []
    xs = np.linspace(x0, x1, n)
    px = rng.uniform(0.35, 0.65)
    for i, x in enumerate(xs):
        t = i / (n - 1)
        d = abs(t - px) / max(px, 1 - px)
        y = base_y - (base_y - peak_y) * (1 - d ** sharp) * rng.uniform(1 - jag, 1 + jag * 0.4)
        if i in (0, n - 1):
            y = base_y
        pts.append((x, y))
    return pts
