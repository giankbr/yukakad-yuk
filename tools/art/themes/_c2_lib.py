"""Agent C2 helpers (peranakan-merah, osing-gajah-oling, istana-maimun, kaftan-ottoman).
Builds on _j1_lib (local-crop G/GP/LC/FO/OV, strokes/shapes/circles) and adds textile media:
  satin()       satin / long-and-short stitch embroidery (thread level, directional sheen, stitch breaks)
  couch()       couched gold thread outline (twisted metallic cord)
  beadwork()    kasut-manik seed beads: a flat design re-rendered as a grid of glass beads
  batik()       canting-wax batik: dyed ground, wax-resist motif with crackle veins and dye bleed
  silk()        silk satin / damask ground (warp sheen, drape bands) - tileable
  lame()        metallic weft floats (brocade / songket gold thread) - tileable
  tile_mask()   draw shapes with wrap-around for seamless tiles
Previews -> /tmp/pen/nb-C2/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-C2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-C2/art"
_j1_lib.PREV = _p1_lib.PREV
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.spatial import cKDTree

PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def C(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col):
    return rgba(np.ones(mask.shape + (3,), np.float32) * C(col), mask)


def wnoise(w, h, seed, sigma):
    """Wrap-around (tileable) smooth noise 0..1."""
    return wrap_noise(w, h, seed, sigma)


def wdisplace(mask, seed, amount=2.0, sigma=6.0, wrap=True):
    h, w = mask.shape
    nx_ = wnoise(w, h, seed, sigma) - 0.5
    ny_ = wnoise(w, h, seed + 1, sigma) - 0.5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return map_coordinates(mask, [yy + ny_ * amount * 4, xx + nx_ * amount * 4], order=1, mode="wrap" if wrap else "constant")


def tile_mask(W, H, draw):
    """draw(canvas) is called for the 9 wrap offsets so shapes crossing an edge reappear on the other side."""
    cv = Canvas(W, H)
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            cv.c.save(); cv.c.translate(dx, dy); draw(cv); cv.c.restore()
    return cv.array()[..., 3]


def paint_white():
    return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)


# ------------------------------------------------------------------ embroidery
def satin(mask, col, col2=None, angle=0.0, spacing=3.0, seed=1, stitch=16.0, sheen=0.55, light=-0.8, radial=None,
          raise_=0.6, fuzz=0.6):
    """Satin / long-and-short stitch fill. angle: thread direction (rad). radial=(cx, cy) makes threads radiate
    from a point (petals, fans). Returns RGBA."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1 = (wnoise(w, h, seed, 5) - 0.5) * 1.4
    if radial is not None:
        cx, cy = radial
        rr = np.hypot(xx - cx, yy - cy) + 1e-3
        ph = np.arctan2(yy - cy, xx - cx)
        v = ph * max(20.0, float(np.percentile(rr[mask > 0.5], 60)) if (mask > 0.5).any() else 40) / spacing + n1
        u = rr / stitch
        ang = ph
    else:
        ca, sa = math.cos(angle), math.sin(angle)
        v = (-xx * sa + yy * ca) / spacing + n1
        u = (xx * ca + yy * sa) / stitch
        ang = np.full((h, w), angle, np.float32)
    row = np.floor(v)
    prof = np.sin(np.pi * (v - row))  # thread cylinder 0..1
    rnd = np.random.default_rng(seed)
    off = rnd.random(4096).astype(np.float32)
    ri = (row.astype(np.int64) % 4096)
    brk = (u + off[ri] * 1.0) % 1.0  # long-and-short: each thread row breaks at its own phase
    gap = np.clip(1 - np.minimum(brk, 1 - brk) / 0.05, 0, 1)
    ca_ = C(col); cb_ = C(col2 or col)
    t = (fbm(w, h, seed + 3, 60, 2) * 0.7 + off[(ri + 7) % 4096] * 0.3)[..., None]
    base = ca_ * (1 - t) + cb_ * t
    dirk = np.abs(np.cos(ang - light))  # threads facing the light shine
    lum = 0.62 + 0.38 * prof ** 0.7
    lum = lum * (1 - 0.35 * gap)
    # raised padding: lighter in the middle of the shape, darker at the rim
    if raise_:
        dist = gaussian_filter(mask, 3.0)
        lum = lum * (0.82 + 0.25 * raise_ * np.clip(dist * 1.3, 0, 1))
    rgb = base * lum[..., None]
    hl = (prof ** 5) * dirk * sheen * (1 - gap)
    rgb = rgb + (1 - rgb) * hl[..., None] * 0.75
    a = mask
    if fuzz:
        a = np.clip(displace(mask, seed + 9, fuzz, 3.0) * 1.15, 0, 1)
    return rgba(rgb, a)


def couch(w, h, items, base="#d6ae55", seed=1, width=3.2, twist=5.0):
    """Couched metallic cord along stroke items [(pts, width?)]: twisted highlights + binding stitches. Returns RGBA."""
    m = strokes(w, h, [(it[0], it[1] if len(it) > 1 else width, None) for it in items])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tw = 0.5 + 0.5 * np.sin((xx + yy) / twist * math.pi)
    tw2 = 0.5 + 0.5 * np.sin((xx - yy) / (twist * 1.3) * math.pi)
    gy, gx = np.gradient(gaussian_filter(m, 1.0))
    light = np.clip(0.5 - (gx + gy) * 4, 0, 1)
    r, g, b = hex_rgb(base)
    lum = 0.55 + 0.35 * np.maximum(tw, tw2 * 0.8) + (light - 0.5) * 0.6
    sp = np.random.default_rng(seed).random((h, w)) > 0.997
    lum = lum + gaussian_filter(sp.astype(np.float32), 0.6) * 3
    rgb = np.stack([r * lum * 1.15, g * lum * 1.12, b * lum], -1)
    return rgba(rgb, np.clip(m * 1.1, 0, 1))


def beadwork(design, pitch=5.0, seed=1, fabric="#f3e9d6", gap=0.12, jitter=0.25):
    """Re-render an RGBA design as kasut-manik seed beads on a square grid. Beads only where design alpha > .45;
    fabric shows between beads only inside the design area. Returns RGBA."""
    h, w = design.shape[:2]
    rng = np.random.default_rng(seed)
    gh, gw = int(h / pitch) + 2, int(w / pitch) + 2
    jx = (rng.random((gh, gw)) - 0.5) * jitter
    jy = (rng.random((gh, gw)) - 0.5) * jitter
    bri = 1 + (rng.random((gh, gw)) - 0.5) * 0.16
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    gi = np.clip(np.round(yy / pitch).astype(int), 0, gh - 1)
    gj = np.clip(np.round(xx / pitch).astype(int), 0, gw - 1)
    cy = gi * pitch + jy[gi, gj] * pitch
    cx = gj * pitch + jx[gi, gj] * pitch
    sy = np.clip(cy.round().astype(int), 0, h - 1)
    sx = np.clip(cx.round().astype(int), 0, w - 1)
    col = design[sy, sx, :3]
    pres = design[sy, sx, 3]
    dx = (xx - cx) / (pitch * 0.5 * (1 - gap))
    dy = (yy - cy) / (pitch * 0.5 * (1 - gap))
    # superellipse bead seen from the side (short cylinder): rounded square
    d = (np.abs(dx) ** 3 + np.abs(dy * 1.08) ** 3) ** (1 / 3)
    inside = np.clip((1 - d) * pitch * 0.7, 0, 1)
    z = np.sqrt(np.clip(1 - dy ** 2, 0, 1))  # cylinder axis horizontal
    lum = (0.5 + 0.5 * z) * bri[gi, gj]
    hole = np.exp(-((dx / 0.16) ** 2 + (dy / 0.5) ** 2))
    spec = np.exp(-(((dx + 0.3) / 0.3) ** 2 + ((dy + 0.42) / 0.2) ** 2)) * 0.45
    rgb = col * lum[..., None] * (1 - 0.22 * hole[..., None]) + spec[..., None] * 0.7
    bead_a = inside * (pres > 0.45)
    area = gaussian_filter((design[..., 3] > 0.45).astype(np.float32), pitch * 0.4)
    area = np.clip(area * 2.2, 0, 1)
    fab = np.ones((h, w, 3), np.float32) * C(fabric) * (0.82 + 0.1 * fbm(w, h, seed + 4, 6, 2))[..., None]
    out_rgb = fab * (1 - bead_a[..., None]) + rgb * bead_a[..., None]
    a = np.maximum(bead_a, area * 0.0 + (area > 0.5) * 0.0)
    a = np.maximum(bead_a, area * (bead_a > -1) * 0.0)
    return rgba(out_rgb, np.maximum(bead_a, area * 0.92))


# ------------------------------------------------------------------ batik
def crackle(w, h, seed, n=260, thick=0.9, wrap=False):
    """Voronoi crack lines 0..1 (wax crackle)."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2)) * [w, h]
    if wrap:
        pts = np.concatenate([pts + [dx, dy] for dx in (-w, 0, w) for dy in (-h, 0, h)])
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    q = np.stack([xx.ravel(), yy.ravel()], -1)
    dd, _ = tree.query(q, k=2)
    e = (dd[:, 1] - dd[:, 0]).reshape(h, w)
    lines = np.clip(1 - e / thick, 0, 1)
    # cracks are broken, not continuous
    brk = wnoise(w, h, seed + 2, 5) if wrap else fbm(w, h, seed + 2, 18, 2)
    return lines * np.clip((brk - 0.32) * 3, 0, 1)


def batik(w, h, wax, ground="#1f1a16", motif="#efe3c8", seed=1, layers=(), tile=False, crack=0.55, bleed=1.2, ncrack=None):
    """Canting-wax batik cloth. wax = mask where wax resisted the first (dark) dye -> motif colour.
    layers = [(mask, colour)] extra colour fields painted (coletan) inside the motif before the dark dye.
    Returns opaque RGBA."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nz = (lambda s, sg: wnoise(w, h, s, sg)) if tile else (lambda s, sg: fbm(w, h, s, sg * 6, 3))
    # fabric weave + dye unevenness
    weave = 0.5 + 0.25 * np.sin(xx * math.pi / 1.5) * np.sin(yy * math.pi / 1.5)
    dye = 0.86 + 0.22 * nz(seed, 30)
    g = C(ground) * (dye * (0.96 + 0.08 * weave))[..., None]
    # wax: slightly bled, hand-drawn edge
    wm = wdisplace(wax, seed + 3, bleed * 0.5, 3.0, wrap=tile) if tile else displace(wax, seed + 3, bleed, 6.0)
    wm = np.clip(gaussian_filter(wm, 0.6) * 1.25, 0, 1)
    mrgb = C(motif) * (0.92 + 0.1 * nz(seed + 5, 20))[..., None] * (0.97 + 0.04 * weave)[..., None]
    for lm, lc in layers:
        lmm = np.clip(gaussian_filter(lm, 0.9), 0, 1)[..., None]
        mrgb = mrgb * (1 - lmm) + C(lc) * (0.9 + 0.12 * nz(seed + 8, 14))[..., None] * lmm
    rgb = g * (1 - wm[..., None]) + mrgb * wm[..., None]
    # halo where dye crept under the wax edge
    halo = np.clip(gaussian_filter(wm, 1.4) - wm, 0, 1) * 0.0 + np.clip(wm - gaussian_filter(wm, 1.2), 0, 1)
    rgb = rgb * (1 - 0.0 * halo[..., None])
    edge = np.clip(gaussian_filter(wm, 1.0) * (1 - wm) * 2, 0, 1)
    rgb = rgb * (1 - 0.18 * edge[..., None]) + C(ground) * 0.0
    if crack:
        cr = crackle(w, h, seed + 11, ncrack or int(w * h / 900), 0.9, wrap=tile)
        cr = cr * wm
        rgb = rgb * (1 - cr[..., None] * crack) + C(ground) * cr[..., None] * crack * 0.9
    return rgba(rgb, np.ones((h, w), np.float32))


# ------------------------------------------------------------------ woven silk / brocade (tileable)
def silk(w, h, col, col2=None, seed=1, pitch=2.0, drape=0.35, bands=2):
    """Satin-weave silk ground: fine warp lines, slub noise, broad sheen bands (integer periods -> tileable)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    warp = 0.5 + 0.5 * np.sin(xx * 2 * math.pi / pitch)
    slub = wnoise(w, h, seed, 1.2)
    slub = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (6, 0.6), mode="wrap")
    slub = (slub - slub.mean()) / (slub.std() + 1e-6)
    sheen = 0.5 + 0.5 * np.sin(2 * math.pi * (xx / w * bands + yy / h * 1) + wnoise(w, h, seed + 2, 40) * 3)
    t = wnoise(w, h, seed + 3, 50)[..., None]
    base = C(col) * (1 - t) + C(col2 or col) * t
    lum = 0.88 + 0.05 * warp + 0.035 * slub + drape * (sheen - 0.5) * 0.5
    return rgba(base * lum[..., None], np.ones((h, w), np.float32))


def lame(mask, base="#d4ad57", seed=1, pitch=2.6, bind=9, sheen_w=None, deep="#8a6326", tile=True):
    """Metallic weft floats: horizontal gold threads with staggered binding points (twill), drape sheen."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = yy / pitch
    row = np.floor(v)
    prof = np.sin(np.pi * (v - row))
    u = (xx / bind + row * 0.37) % 1.0
    bindp = np.clip(1 - np.minimum(u, 1 - u) / 0.07, 0, 1)
    nz = wnoise(w, h, seed, 30) if tile else fbm(w, h, seed, 120, 2)
    sheen = 0.5 + 0.5 * np.sin(2 * math.pi * (xx / (sheen_w or w) + nz * 0.8))
    lum = 0.42 + 0.48 * prof ** 0.8 + 0.32 * sheen * prof ** 2
    lum = lum * (1 - 0.45 * bindp)
    t = np.clip(lum, 0, 1.3)[..., None]
    rgb = C(deep) * (1 - np.clip(t, 0, 1)) + C(base) * np.clip(t, 0, 1)
    rgb = rgb + np.clip(t - 1, 0, 1) * 1.6
    spark = (np.random.default_rng(seed + 1).random((h, w)) > 0.996) * prof
    rgb = rgb + gaussian_filter(spark.astype(np.float32), 0.5)[..., None] * 1.2
    return rgba(rgb, mask)


def over_full(dst, src):
    return over(dst, src)


def drop_shadow(arr, blur=6, dx=0, dy=4, strength=0.45, col="#000000"):
    a = arr[..., 3]
    sh = np.roll(np.roll(gaussian_filter(a, blur), dy, 0), dx, 1) * strength
    return over(rgba(np.ones(a.shape + (3,), np.float32) * C(col), sh), arr)


def SAT(dst, mask, col, col2=None, pad=6, mode="over", **k):
    """satin() computed inside the mask bbox only (radial centre is shifted into the crop)."""
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    if k.get("radial") is not None:
        k = dict(k); k["radial"] = (k["radial"][0] - x0, k["radial"][1] - y0)
    src = satin(np.ascontiguousarray(mask[y0:y1, x0:x1]), col, col2, **k)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    return out


def LOC(dst, mask, fn, pad=8):
    """over: fn(crop_mask, x0, y0) -> RGBA, inside the mask bbox."""
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    src = fn(np.ascontiguousarray(mask[y0:y1, x0:x1]), x0, y0)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    return out


def poly(W, H, pts, smooth=True):
    return shapes(W, H, [pts], smooth=smooth)


def ribbon(path, w0, w1, wf=None):
    """Closed polygon of a tapered ribbon along path (width w0 -> w1, optional width fn(t))."""
    n = len(path); L, R = [], []
    for i in range(n):
        a = path[max(0, i - 1)]; b = path[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; d = math.hypot(tx, ty) or 1
        nx_, ny_ = -ty / d, tx / d
        t = i / (n - 1)
        ww = (wf(t) if wf else w0 + (w1 - w0) * t) / 2
        L.append((path[i][0] + nx_ * ww, path[i][1] + ny_ * ww)); R.append((path[i][0] - nx_ * ww, path[i][1] - ny_ * ww))
    return L + R[::-1]


def tangent(path, i):
    n = len(path); a = path[max(0, i - 1)]; b = path[min(n - 1, i + 1)]
    return math.atan2(b[1] - a[1], b[0] - a[0])


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in [i / (n - 1) for i in range(n)]]
