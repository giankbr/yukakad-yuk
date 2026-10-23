"""Agent I2 helpers (muna-kaghati, bali-endek, muqarnas-putih, ultah-bajak-laut).
Builds on _e6_lib (-> _d5_lib / _jw_lib / _j1_lib / _p1_lib / art): bbox-local G/GP/LC/FO/OV, strokes/shapes/circles,
toon (kids gouache + crayon contour), soft/inner_shade. Adds: tonal gouache wash (twash), linear/radial ramps, weft
stripe weave (tenun), weft-ikat feathering (endek), stucco/plaster shading, dotted trail masks, rope, planks.
Previews -> /tmp/pen/nb-I2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _e6_lib import *  # noqa
import _e6_lib, _d5_lib, _p1_lib
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-I2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _d5_lib.PREV = _e6_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def preview(arr, name, tone="#fbf6e4", bg=None):  # noqa: F811
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def carr(h):
    return np.array(hex_rgb(h), np.float32)


def twash(dst, m, col, amt=0.5, seed=1, streak=0.6, col2=None):
    """Soft opaque tonal wash (gouache shading): alpha = m*amt with brush streaks; local to the mask bbox."""
    b = bbox(m, 2, 0.002)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    mm = np.ascontiguousarray(m[y0:y1, x0:x1])
    h, w = mm.shape
    ca = carr(col); cb = carr(col2 or col)
    t = fbm(w, h, seed + 3, 70, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.5, 4.0))
    s = (s - s.mean()) / (s.std() + 1e-6)
    rgb = np.clip(rgb * (1 + s[..., None] * 0.04 * streak), 0, 1)
    src = np.concatenate([rgb, np.clip(mm * amt, 0, 1)[..., None]], -1)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    trim_cache()
    return out


def lin(W, H, x0, y0, x1, y1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy + 1e-6
    return np.clip(((xx - x0) * dx + (yy - y0) * dy) / L2, 0, 1)


def rad(W, H, cx, cy, r, sy=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.clip(1 - np.hypot(xx - cx, (yy - cy) / sy) / r, 0, 1)


def polys(W, H, items, smooth=False):
    return shapes(W, H, items, smooth=smooth)


def dotted(W, H, pts, step, r):
    """Dotted/dashed trail along a polyline: discs every `step` px."""
    out = []
    acc = 0.0
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        L = math.hypot(x1 - x0, y1 - y0)
        t = acc
        while t < L:
            out.append((x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L, r))
            t += step
        acc = t - L
    return circles(W, H, out)


def dashes(pts, step, dash):
    """Split a polyline into dash segments (list of point lists)."""
    res = []
    acc = 0.0; on = True; cur = [pts[0]]
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) or 1e-6
        t = 0.0
        while t < L:
            lim = (dash if on else step - dash) - acc
            if t + lim <= L:
                t += lim
                p = (x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L)
                if on:
                    cur.append(p); res.append(cur)
                else:
                    cur = [p]
                on = not on; acc = 0.0
            else:
                acc += L - t
                if on:
                    cur.append((x1, y1))
                t = L
    return res


def weft_stripes(W, H, seq, seed=1, pick=2.0, warp=2.6, fibre=0.06, sheen=0.0):
    """Plain-weave cloth with horizontal weft stripes (tenun lurik-like). seq: [(hex, px_height)] repeating vertically.
    Thread level: weft picks with round profiles, warp ticks, slubs, per-pick tone drift. Opaque RGB float (H, W, 3)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    total = sum(h for _, h in seq)
    # stripe lookup per row (with slight waviness of the weft)
    wav = (fbm(W, H, seed + 2, 90, 2) - 0.5) * 2.2
    yv = (yy + wav) % total
    pal = np.array([hex_rgb(c) for c, _ in seq], np.float32)
    edges = np.cumsum([h for _, h in seq])
    idx = np.searchsorted(edges, yv, side="right").clip(0, len(seq) - 1)
    rgb = pal[idx]
    # pick structure
    py = (yy / pick) % 1.0
    prof = np.sin(py * math.pi) ** 0.7
    pick_id = (yy // pick).astype(np.int32)
    ptone = (np.sin(pick_id * 12.9898 + seed) * 43758.5453) % 1.0
    lum = 0.78 + 0.26 * prof + (ptone - 0.5) * 0.07
    # warp ticks (warp shows where weft dips)
    wx = (xx / warp) % 1.0
    over_ = ((xx // warp).astype(np.int32) + pick_id) % 2
    lum *= 1 - 0.10 * over_ * (np.abs(wx - 0.5) * 2)
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.35, 3.5), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    lum *= 1 + fibre * fib
    slub = np.clip((fbm(W, H, seed + 5, 14, 2) - 0.78) * 3, 0, 1)
    lum *= 1 + 0.08 * slub
    out = rgb * lum[..., None]
    if sheen:
        out = out + sheen * (prof[..., None] ** 6) * 0.25
    return np.clip(out, 0, 1)


def rgb_to_rgba(rgb, a=None):
    h, w = rgb.shape[:2]
    al = np.ones((h, w, 1), np.float32) if a is None else a[..., None].astype(np.float32)
    return np.concatenate([rgb, al], -1)


def save_rgb(rgb, path, quality=80, size=None):  # noqa: F811
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def kb_report(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        sz = os.path.getsize(os.path.join(d, f)); tot += sz
        try:
            dims = Image.open(os.path.join(d, f)).size
        except Exception:
            dims = "?"
        print(f"  {f:22s} {sz / 1024:7.1f} KB  {dims}")
    print(f"  total {tot / 1024:.1f} KB")


def rope(W, H, pts, width, seed=1):
    """Twisted rope / string mask with diagonal ply marks: returns (body, plies)."""
    body = strokes(W, H, [(pts, width, None)])
    items = []
    acc = 0
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) or 1
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        t = acc
        while t < L:
            cx, cy = x0 + ux * t, y0 + uy * t
            nxv, nyv = -uy, ux
            a = (cx + nxv * width * 0.45 - ux * width * 0.3, cy + nyv * width * 0.45 - uy * width * 0.3)
            b = (cx - nxv * width * 0.45 + ux * width * 0.3, cy - nyv * width * 0.45 + uy * width * 0.3)
            items.append(([a, b], max(0.6, width * 0.16), None))
            t += width * 0.7
        acc = t - L
    plies = strokes(W, H, items) * body if items else body * 0
    return body, plies


def wood(art, m, base, dark, light, nx, grain_ang=0.0, scale=1.0, knots=0, rng=None, plank=None):
    """Painted wood: gouache base, streaky grain along grain_ang, darker seams every `plank` px across the grain."""
    H, W = m.shape
    art = GP(art, m, base, mix(base, light, 0.25), seed=nx(), rough=1.2, streak=1.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ca, sa = math.cos(grain_ang), math.sin(grain_ang)
    u = xx * ca + yy * sa; v = -xx * sa + yy * ca
    n = fbm(W, H, nx(), 40 * scale, 3)
    g = 0.5 + 0.5 * np.sin(v / (3.2 * scale) + n * 9 + np.sin(u / (60 * scale)) * 2)
    art = twash(art, m * np.clip((g - 0.62) * 3, 0, 1), dark, 0.32, seed=nx())
    art = twash(art, m * np.clip((0.3 - g) * 3, 0, 1), light, 0.18, seed=nx())
    if plank:
        f = np.abs(((v + (fbm(W, H, nx(), 50, 2) - 0.5) * 2) / plank) % 1.0 - 0.5) * 2
        seam = np.clip((f - 0.9) / 0.08, 0, 1) * m
        art = twash(art, seam, dark, 0.8, seed=nx())
        hi = np.clip((f - 0.78) / 0.08, 0, 1) * (1 - np.clip((f - 0.9) / 0.08, 0, 1)) * m
        art = twash(art, np.roll(hi, 1, 0) * 0.0 + hi * ((((v / plank) % 1.0) < 0.5)), light, 0.18, seed=nx())
    return art


from _c1_lib import sun_glints, leaf_pts, jungle_leaf, grass_tufts  # noqa: E402
from _g1_lib import brushwork, mist, ridge_pts  # noqa: E402
_p1_lib.PREV = _d5_lib.PREV = _e6_lib.PREV = PREV


def rect(W, H, x0, y0, x1, y1):
    m = np.zeros((H, W), np.float32)
    m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = 1
    return m


def weft_ikat(motif, palette, seed=1, pick=3, bleed=10.0, warp=2.0, fibre=0.06):
    """Weft ikat (endek), thread level and tileable. motif: (H, W) palette indices as tied. Each weft pick is shifted
    horizontally by its own small random offset (the tied bundles slip when woven), dye bleeds along the weft, warp
    threads show as fine vertical ticks. H must be a multiple of `pick`. Returns RGB float (H, W, 3)."""
    H, W = motif.shape
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    pid = yy // pick
    npk = H // pick
    sh = rng.normal(0, bleed * 0.35, npk)
    sh = sh + np.roll(sh, 1) * 0.5  # bundles of neighbouring picks slip together
    sx = ((xx + sh[pid].astype(np.int32)) % W)
    pal = np.array([hex_rgb(c) for c in palette], np.float32)
    rgb = pal[motif[yy, sx]]
    soft = np.zeros_like(rgb)
    for k in range(3):
        soft[..., k] = gaussian_filter(rgb[..., k], (0.01, bleed * 0.22), mode="wrap")
    rgb = rgb * 0.55 + soft * 0.45
    fy = ((yy % pick) + 0.5) / pick
    prof = np.sin(fy * math.pi) ** 0.6
    lum = 0.74 + 0.3 * prof
    tick = (((xx // warp) + pid) % 2 == 0).astype(np.float32)
    lum = lum * (1 - 0.08 * tick * (1 - prof))
    ptone = (np.sin(pid * 12.9898 + seed) * 43758.5453) % 1.0
    lum = lum * (0.95 + 0.08 * ptone)
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.35, 3.0), mode="wrap")
    lum = lum * (1 + 0.06 * (fib - fib.mean()) / (fib.std() + 1e-6))
    return np.clip(rgb * lum[..., None], 0, 1)
