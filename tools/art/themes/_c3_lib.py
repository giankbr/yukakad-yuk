"""Agent C3 helpers (lampu-mosaik, hadramaut-tanah, melati-syari, langit-subuh): builds on _b2_lib/_j1_lib
(bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, rect/poly/flat, bricks, wood, light_mask) and adds
glass tesserae (Voronoi mosaic set in grout, lit from inside), brass chains, emissive bloom, mud plaster,
wet-on-wet sky washes. Previews -> /tmp/pen/nb-C3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _b2_lib import *  # noqa
import _b2_lib, _j1_lib
from scipy import ndimage
from scipy.spatial import cKDTree
import art as _art

PREV = "/tmp/pen/nb-C3/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _b2_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1); u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def resample(pts, step):
    """Polyline -> [(x, y, angle)] at fixed arc length."""
    out = []; acc = 0.0
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out


def prev_dark(arr, name, bg="#140e22"):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def add_layer(dst, src):
    """Additive light (for bloom) onto an RGBA layer: brightens colour and raises alpha."""
    sa = src[..., 3:4]
    out = dst.copy()
    da = dst[..., 3:4]
    oa = np.clip(da + sa * (1 - da), 0, 1)
    rgb = (dst[..., :3] * da + src[..., :3] * sa) / np.maximum(oa, 1e-6)
    rgb = np.where(da > 0.05, np.clip(dst[..., :3] + src[..., :3] * sa * 0.6, 0, 1), rgb)
    out[..., :3] = np.clip(rgb, 0, 1); out[..., 3:4] = oa
    return out


def tesserae(mask, cell, seed, jitter=0.45, x0=0, y0=0):
    """Voronoi mosaic inside mask: returns (labels HxW int, seed points Nx2, grout mask)."""
    H, W = mask.shape
    rng = np.random.default_rng(seed)
    ys = np.arange(y0 % cell - cell, H + cell, cell * 0.87)
    pts = []
    for j, y in enumerate(ys):
        off = (j % 2) * cell / 2
        for x in np.arange(-cell + off, W + cell, cell):
            pts.append((x + rng.uniform(-jitter, jitter) * cell, y + rng.uniform(-jitter, jitter) * cell))
    pts = np.array(pts, np.float32)
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:H, 0:W]
    d, lab = tree.query(np.stack([xx.ravel(), yy.ravel()], -1), k=2)
    lab1 = lab[:, 0].reshape(H, W)
    gap = (d[:, 1] - d[:, 0]).reshape(H, W)
    grout = np.clip(1.6 - gap, 0, 1).astype(np.float32)
    return lab1, pts, grout


def chain(W, H, x, y0, y1, link=9.0, sway=0.0):
    """Mask of a brass chain (alternating face-on ovals and edge-on bars) from y0 down to y1."""
    items_o, bars = [], []
    n = int((y1 - y0) / link)
    for i in range(n):
        y = y0 + i * link + link / 2
        xx = x + sway * ((y - y0) / max(1, y1 - y0)) ** 2
        if i % 2 == 0:
            items_o.append((xx, y, link * 0.36, link * 0.62, 0))
        else:
            bars.append(([(xx, y - link * 0.55), (xx, y + link * 0.55)], link * 0.26, None))
    ring_o = ellipses(W, H, items_o)
    inner = ellipses(W, H, [(a, b, rx * 0.45, ry * 0.62, r) for a, b, rx, ry, r in items_o])
    m = np.clip(ring_o - inner, 0, 1)
    if bars:
        m = np.maximum(m, strokes(W, H, bars))
    return m


def plaster(mask, col, col2, seed, straw=0.5):
    """Mud plaster / adobe: gouache base, trowel swirls, straw flecks, pitting."""
    h, w = mask.shape
    base = gouache_paint(mask, col, col2, seed=seed, rough=1.2, streak=0.8)
    sw = fbm(w, h, seed + 2, 26, 3)
    pit = fbm(w, h, seed + 4, 3, 2)
    lum = 0.9 + 0.18 * sw - 0.12 * np.clip((pit - 0.7) * 4, 0, 1)
    rng = np.random.default_rng(seed + 9)
    fl = np.zeros((h, w), np.float32)
    nfl = int(w * h * 0.0009 * straw)
    if nfl:
        cv = Canvas(w, h)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=1.0, Style=skia.Paint.kStroke_Style)
        for _ in range(nfl):
            xx, yy = rng.uniform(0, w), rng.uniform(0, h); a = rng.uniform(0, math.pi); L = rng.uniform(3, 8)
            cv.c.drawLine(xx, yy, xx + math.cos(a) * L, yy + math.sin(a) * L, p)
        fl = cv.array()[..., 3]
    base[..., :3] = np.clip(base[..., :3] * lum[..., None] * (1 + fl[..., None] * 0.22), 0, 1)
    return base


def wet_sky(w, h, stops, seed=1, blooms=0.5):
    """Wet-on-wet dawn sky: soft bands that bleed into each other, cauliflower blooms, granulation (opaque)."""
    sky = painted_sky(w, h, stops, seed=seed, streak=0.25, grain=0.3)
    rng = np.random.default_rng(seed)
    # bleed: displace colours along soft noise (wet paint moving)
    nx_ = (fbm(w, h, seed + 3, 160, 3) - 0.5) * 60
    ny_ = (fbm(w, h, seed + 4, 120, 3) - 0.5) * 90
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for c in range(3):
        sky[..., c] = map_coordinates(sky[..., c], [np.clip(yy + ny_, 0, h - 1), np.clip(xx + nx_, 0, w - 1)], order=1)
    # blooms: lighter centres with darker rims
    b = fbm(w, h, seed + 7, 70, 4)
    bl = np.clip((b - 0.58) * 4, 0, 1)
    rim = np.clip(gaussian_filter(bl, 2) - gaussian_filter(bl, 7), 0, 1)
    sky[..., :3] = sky[..., :3] * (1 + bl[..., None] * 0.05 * blooms) * (1 - rim[..., None] * 0.18 * blooms)
    g = gaussian_filter(rng.random((h, w)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    sky[..., :3] *= (1 + g[..., None] * 0.012)
    sky[..., :3] = np.clip(sky[..., :3], 0, 1)
    return sky


def emboss_l(mask, depth=1.0, blur=1.6, ang=(-0.7, -0.7)):
    """Highlight / shadow fields for a raised (carved) mask, light from the upper left."""
    m = gaussian_filter(mask, blur)
    gy, gx = np.gradient(m)
    d = -(gx * ang[0] + gy * ang[1]) * depth * 6
    return np.clip(d, 0, 1), np.clip(-d, 0, 1)
