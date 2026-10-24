"""Agent S3 helpers (songket-aceh, cintamani, ballroom-kristal, gala-dinner).
- weave(): thread-level woven cloth renderer (ground twill + metallic supplementary-weft floats with tie-downs, glint)
- silk(): satin/silk ground with lustre bands; velvet(): cut-pile velvet shading for a mask
- crystal(): faceted crystal drop; helpers re-exported from _j1_lib (G/GP/LC/FO/OV, strokes, shapes, circles...)
Previews -> /tmp/pen/nb-S3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-S3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _p1_lib import *  # noqa
from _j1_lib import G, GP, LC, FO, OV, strokes, shapes, circles, ellipses, bbox, trim_cache, hatch, mirror  # noqa
import _j1_lib
import art as _art
PREV = "/tmp/pen/nb-S3/art"
_p1_lib.PREV = PREV


def preview(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.PREV = PREV
    return _p1_lib.preview(arr, name, tone, bg)


def ramp(t, stops):
    """t (H,W) in [0,1] -> RGB through [(pos, hex), ...]."""
    out = np.zeros(t.shape + (3,), np.float32)
    t = np.clip(t, 0, 1)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]; p1, c1 = stops[i + 1]
        k = np.clip((t - p0) / max(1e-6, p1 - p0), 0, 1)[..., None]
        sel = ((t >= p0) & (t <= p1))[..., None] if i else (t <= p1)[..., None]
        if i == len(stops) - 2:
            sel = (t >= p0)[..., None]
        col = np.array(hex_rgb(c0), np.float32) * (1 - k) + np.array(hex_rgb(c1), np.float32) * k
        out = np.where(sel, col, out)
    return out


GOLD_RAMP = [(0, "#3a250a"), (0.35, "#8a6020"), (0.62, "#c99a3c"), (0.84, "#efd087"), (1.0, "#fff4cf")]


def weave(motif, ground, pick=5, end=4, maxfloat=7, tie_shift=3, seed=1, metal=None, wrap=True, glint=0.7,
          light_angle=0.6):
    """Thread-level woven cloth.
    motif: (R, C) int array, 0 = ground, k>0 = supplementary weft colour index into `metal` (list of ramps).
    ground: (R, C, 3) float RGB base colour of the ground cloth per cell.
    Returns RGBA float (R*pick, C*end, 4) opaque."""
    metal = metal or [GOLD_RAMP]
    R, C = motif.shape
    H, W = R * pick, C * end
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    r = yy // pick; c = xx // end
    ly = (yy % pick + 0.5) / pick; lx = (xx % end + 0.5) / end
    nz = (lambda s, sg: wrap_noise(W, H, s, sg)) if wrap else (lambda s, sg: fbm(W, H, s, sg * 4, 3))
    # ---- ground: 2/1 twill-ish interlace of warp (vertical) and weft (horizontal) threads
    up = ((c + r * 2) % 3 == 0)  # warp float points
    prof_w = np.sin(np.pi * lx) ** 0.6   # across a warp end
    prof_f = np.sin(np.pi * ly) ** 0.6   # across a weft pick
    gb = ground[r, c]
    jit_r = (rng.random((R, 1)) - 0.5) * 0.10  # per-pick tone drift
    jit_c = (rng.random((1, C)) - 0.5) * 0.08
    shade = np.where(up, 0.62 + 0.5 * prof_w + jit_c[0, c], 0.55 + 0.5 * prof_f + jit_r[r, 0])
    g_rgb = gb * shade[..., None]
    # ---- supplementary weft floats with staggered tie-downs
    m = motif.copy()
    tie = np.zeros_like(m, bool)
    for i in range(R):
        run = 0
        for j in range(C):
            if m[i, j] > 0:
                run += 1
                if run > maxfloat and (j + i * tie_shift) % (maxfloat + 1) == 0:
                    tie[i, j] = True; run = 0
            else:
                run = 0
    on = (m > 0) & ~tie
    onp = on[r, c]
    left = on & ~np.roll(on, 1, 1); right = on & ~np.roll(on, -1, 1)
    if not wrap:
        left[:, 0] = on[:, 0]; right[:, -1] = on[:, -1]
    ex = (lx - 0.5) * 2; ey = (ly - 0.5) * 2
    cap = (ex ** 2 + ey ** 2 * 0.9) <= 1.0
    inside = onp & np.where(left[r, c] & (lx < 0.5), cap, True) & np.where(right[r, c] & (lx > 0.5), cap, True)
    prof = np.sin(np.pi * np.clip(ly, 0, 1))
    a = inside * np.clip(prof * 2.6 - 0.15, 0, 1)
    # metallic shading: thread profile + twist striations + broad glint bands + per-pick variation
    twist = 0.5 + 0.5 * np.sin((xx * 1.0 - yy * 1.7) * (2 * np.pi / 3.2))
    band = nz(seed + 3, 22)
    band2 = nz(seed + 4, 6)
    diag = 0.5 + 0.5 * np.sin((xx * np.cos(light_angle) + yy * np.sin(light_angle)) / max(30, W * 0.09) * np.pi + band * 4)
    pv = (rng.random((R, C)) - 0.5)[r, c]
    lum = 0.18 + 0.62 * prof ** 0.8 + 0.10 * twist + pv * 0.14
    spec = np.clip(prof - 0.72, 0, 1) * 3.6 * np.clip(diag * 1.3 - 0.25 + (band2 - 0.5) * 0.6, 0, 1) * glint
    lum = lum * (0.78 + 0.32 * diag) + spec
    mrgb = np.zeros((H, W, 3), np.float32)
    for k, rp in enumerate(metal):
        sel = (m[r, c] == k + 1)
        if sel.any():
            mrgb = np.where(sel[..., None], ramp(np.clip(lum, 0, 1), rp), mrgb)
    rgb = g_rgb * (1 - a[..., None]) + mrgb * a[..., None]
    # shadow cast by floats onto the ground just below them
    sh = np.roll(onp.astype(np.float32), 1, 0) * (1 - a) * 0.25
    rgb *= (1 - sh)[..., None]
    # global cloth light + soft fold
    rgb *= (0.92 + 0.12 * nz(seed + 9, 40))[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def grid_mask(R, C, draw, thr=0.5):
    """Draw motif geometry with skia at cell resolution (one px per cell); returns bool (R, C)."""
    m = mask_from(C, R, draw)
    return m > thr


def silk(W, H, base="#f2e7d1", seed=1, lustre=0.55, wrap=True):
    """Ivory silk/kemha ground: fine weave grain, warp lines, broad satin lustre bands. Opaque RGBA."""
    nz = (lambda s, sg: wrap_noise(W, H, s, sg)) if wrap else (lambda s, sg: fbm(W, H, s, sg * 4, 3))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    b = np.array(hex_rgb(base), np.float32)
    warp = 0.5 + 0.5 * np.sin(xx * np.pi / 2.0 + nz(seed, 3) * 2)
    weft = 0.5 + 0.5 * np.sin(yy * np.pi / 2.5)
    grain = nz(seed + 1, 0.7)
    lb = nz(seed + 2, 28)
    diag = np.sin((xx / W * 2 + yy / H * 1) * np.pi * 2 + (lb - 0.5) * 1.2)
    sheen = np.clip(diag * 0.8 + (lb - 0.5) * 0.6, -0.6, 1)
    lum = 0.95 + 0.035 * warp + 0.015 * weft + (grain - 0.5) * 0.05 + sheen * 0.06 * lustre
    rgb = b * lum[..., None]
    rgb += np.array([1.0, 0.97, 0.9], np.float32) * np.clip(sheen, 0, 1)[..., None] * 0.05 * lustre
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def velvet(mask, col, deep, hi, seed=1, nap=0.5, wrap=False, rough=1.4, depth_px=6.0):
    """Cut-pile velvet: dense colour, soft fuzzy edge, pile darkens toward the rims, bright grazing sheen on the
    upper-left rims, crushed-nap mottling. Returns RGBA."""
    h, w = mask.shape
    md = "wrap" if wrap else "reflect"
    m = displace(mask, seed, rough, 10) if rough else mask
    m = np.clip(gaussian_filter(m, 0.9, mode=md), 0, 1)
    inner = gaussian_filter(m, depth_px, mode=md)
    depth = np.clip((inner - 0.25) * 1.6, 0, 1)
    b = gaussian_filter(m, 3, mode=md)
    gx = (np.roll(b, -1, 1) - np.roll(b, 1, 1)) * 0.5; gy = (np.roll(b, -1, 0) - np.roll(b, 1, 0)) * 0.5
    rim_light = np.clip((gx * 0.7 + gy * 0.7) * 16, 0, 1) * m
    if wrap:
        crush = wrap_noise(w, h, seed + 4, 5); fib = wrap_noise(w, h, seed + 5, 0.6)
    else:
        crush = fbm(w, h, seed + 4, 22, 3); fib = gaussian_filter(np.random.default_rng(seed + 5).random((h, w)).astype(np.float32), 0.6)
        fib = (fib - fib.min()) / (fib.max() - fib.min() + 1e-6)
    t = np.clip(0.08 + 0.72 * depth ** 1.4 + (crush - 0.5) * 0.6 * nap + (fib - 0.5) * 0.18, 0, 1)
    rgb = ramp(t, [(0, deep), (0.6, col), (1.0, mix(col, hi, 0.22))])
    rgb = rgb + (np.array(hex_rgb(hi), np.float32) - rgb) * rim_light[..., None] * 0.45
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def VV(dst, mask, *a, pad=10, **k):
    return OV(dst, mask, lambda mm: velvet(mm, *a, **k), pad=pad)


def couched(mask, seed=1, base="#c99a3c"):
    """Gold couched-thread outline (metal thread laid on fabric, tacked down): foil + periodic tack marks."""
    h, w = mask.shape
    f = foil(mask, base, seed=seed, emboss=0.7, sparkle=0.12)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tw = 0.5 + 0.5 * np.sin((xx + yy) * np.pi / 2.0)
    f[..., :3] *= (0.86 + 0.2 * tw)[..., None]
    return f


def CO(dst, mask, pad=8, **k):
    return OV(dst, mask, lambda mm: couched(mm, **k), pad=pad)


def crystal_drop(W, H, x, y, s, rng, kind="pear"):
    """Polygon of a crystal drop hanging from (x, y) of size s."""
    if kind == "pear":
        pts = [(x, y), (x + s * .32, y + s * .55), (x + s * .38, y + s * 1.0), (x, y + s * 1.45), (x - s * .38, y + s * 1.0), (x - s * .32, y + s * .55)]
    elif kind == "bead":
        pts = [(x, y), (x + s * .3, y + s * .3), (x, y + s * .6), (x - s * .3, y + s * .3)]
    else:  # prism
        pts = [(x, y), (x + s * .16, y + s * .3), (x + s * .12, y + s * 1.7), (x, y + s * 2.0), (x - s * .12, y + s * 1.7), (x - s * .16, y + s * .3)]
    return pts


def solid_like(arr, col):
    out = arr.copy()
    out[..., :3] = np.array(hex_rgb(col), np.float32)
    return out
