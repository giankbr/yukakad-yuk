"""Agent A1 helpers (madura-sakera, lampung-tapis, aceh-pintu, banjar-sasirangan): builds on _j1_lib (bbox-cropped
painting) with textile media — couched gold thread, satin-stitch embroidery, woven cloth, tie-dye (jumputan) with dye
bleed, batik canting wax lines. Previews -> /tmp/pen/nb-A1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-A1/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-A1/art"
_j1_lib.PREV = _p1_lib.PREV
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates, binary_dilation, distance_transform_edt

PREV = "/tmp/pen/nb-A1/art"


def clear():
    _art._fbm_cache.clear()


def col_arr(h):
    return np.array(hex_rgb(h), np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * col_arr(col)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def polyline_mask(W, H, lines, width, cap=True):
    """Untapered strokes (list of point lists)."""
    return strokes(W, H, [(pts, width, None) for pts in lines], cap=cap)


# ------------------------------------------------------------------ thread / embroidery media
def couched(mask, base="#d2a849", seed=1, angle=0.0, pitch=2.2, stitch=9.0, stitch_col="#7a1b1b", emboss=0.7):
    """Couched gold thread (tapis): parallel metallic threads at `angle`, each catching light as a cylinder, held down by
    small perpendicular couching stitches in silk. Returns RGBA."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ca, sa = math.cos(angle), math.sin(angle)
    wob = (fbm(w, h, seed, 26, 2) - 0.5) * 1.6
    v = (-xx * sa + yy * ca + wob) / pitch          # across threads
    u = (xx * ca + yy * sa) / stitch                 # along threads
    f = (v % 1.0)
    cyl = np.sin(np.clip(f, 0, 1) * math.pi) ** 0.7  # round thread profile
    groove = np.clip(1 - np.abs(f - 0.5) * 2.4, 0, 1)
    sheen = 0.5 + 0.5 * np.sin((xx * 0.7 + yy * 0.45) / max(14, w * 0.05) + fbm(w, h, seed + 2, 40, 2) * 4)
    thread_id = np.floor(v)
    tvar = (np.sin(thread_id * 12.9898) * 43758.5453) % 1.0
    lum = 0.42 + 0.55 * cyl * (0.55 + 0.45 * sheen) + (tvar - 0.5) * 0.12
    r, g, b = hex_rgb(base)
    rgb = np.stack([np.clip(r * lum * 1.25, 0, 1), np.clip(g * lum * 1.2, 0, 1), np.clip(b * lum * 1.05, 0, 1)], -1)
    # couching stitches: short across-thread ticks, staggered every other pair of threads
    pair = np.floor(v / 2)
    uu = (u + (pair % 2) * 0.5) % 1.0
    tick = np.clip(1 - np.abs(uu - 0.5) / 0.06, 0, 1) * (np.abs(((v / 2) % 1.0) - 0.5) < 0.48)
    sc = col_arr(stitch_col)
    rgb = rgb * (1 - tick[..., None] * 0.85) + sc * 0.9 * tick[..., None] * 0.85
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    gy, gx = np.gradient(gaussian_filter(m, 1.4))
    rgb *= np.clip(1 - (gx + gy) * 4 * emboss, 0.6, 1.25)[..., None]
    a = m * (0.86 + 0.14 * groove)
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def satin(mask, col, seed=1, angle=0.8, pitch=1.6, sheen=0.35):
    """Satin-stitch embroidery (kerawang Gayo): dense parallel silk floss with glossy ridges and small gaps."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wob = (fbm(w, h, seed, 18, 2) - 0.5) * 1.2
    v = (-xx * math.sin(angle) + yy * math.cos(angle) + wob) / pitch
    f = v % 1.0
    ridge = np.sin(f * math.pi) ** 0.5
    n = fbm(w, h, seed + 4, 8, 2)
    lum = 0.78 + 0.22 * ridge + sheen * (n - 0.5) * 0.6
    rgb = col_arr(col)[None, None, :] * lum[..., None]
    m = displace(mask, seed, 1.2, 10)
    m = np.clip((gaussian_filter(m, 0.5) - 0.3) * 2.2, 0, 1)
    gap = (np.abs(f - 0.02) < 0.06).astype(np.float32) * 0.25
    return np.concatenate([np.clip(rgb, 0, 1), (m * (1 - gap))[..., None]], -1)


def weave(w, h, warp, weft, seed=1, cell=3.0):
    """Woven cloth surface: alternating warp/weft float shading (multiplier 0.85..1.1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    i = np.floor(xx / cell); j = np.floor(yy / cell)
    over_ = ((i + j) % 2).astype(np.float32)
    fx = (xx % cell) / cell; fy = (yy % cell) / cell
    warp_sh = np.sin(fx * math.pi) ** 0.6; weft_sh = np.sin(fy * math.pi) ** 0.6
    shade = over_ * (0.82 + 0.22 * warp_sh) + (1 - over_) * (0.82 + 0.22 * weft_sh)
    slub = 0.94 + 0.12 * fbm(w, h, seed, 30, 2)
    return shade * slub


def tie_dye(mask, col, seed=1, bleed=5.0, density=0.92, resist=None):
    """Jumputan/sasirangan dye: colour wicks outward from the shape with feathered capillary edges, deeper where dye
    pooled, white resist where stitched thread (`resist` mask) blocked it."""
    h, w = mask.shape
    m = displace(mask, seed, bleed * 0.8, 14)
    soft = gaussian_filter(m, bleed)
    cap = fbm(w, h, seed + 3, 5, 3)          # capillary fibres
    edge = np.clip((soft - 0.18 - (cap - 0.5) * 0.35) * 3.2, 0, 1)
    core = np.clip(gaussian_filter(m, 1.2) * 1.2, 0, 1)
    a = np.maximum(core * 0.95, edge * 0.8)
    rim = np.clip(gaussian_filter(m, 2.5) - gaussian_filter(m, 7), 0, 1)
    a = np.clip(a + rim * 0.9, 0, 1)
    mott = fbm(w, h, seed + 9, 50, 3)
    a *= 0.82 + 0.18 * mott
    if resist is not None:
        a *= 1 - np.clip(gaussian_filter(resist, 0.8) * 1.4, 0, 1) * 0.92
    c = col_arr(col)
    rgb = c[None, None, :] * (1.05 - 0.25 * a[..., None])
    return np.concatenate([np.clip(rgb, 0, 1), (a * density)[..., None]], -1)


def dye_on(cloth, layer):
    """Dye multiplies into cloth (opaque RGB(A) cloth)."""
    a = layer[..., 3:4]
    out = cloth.copy()
    out[..., :3] = cloth[..., :3] * (1 - a) + cloth[..., :3] * layer[..., :3] * a * 1.02
    return np.clip(out, 0, 1)


def wax_line(W, H, lines, width, seed=1):
    """Canting wax line mask: slightly blotchy, varying width, small breaks."""
    m = strokes(W, H, [(pts, width * random.Random(seed + k).uniform(0.8, 1.2), (0.05, 0.05)) for k, pts in enumerate(lines)])
    br = fbm(W, H, seed + 1, 7, 2)
    m *= np.clip((br - 0.12) * 6, 0, 1)
    return np.clip(displace(m, seed, 0.8, 6), 0, 1)


def isen_dots(W, H, pts, r):
    return circles(W, H, [(x, y, r) for x, y in pts])


def tileable(arr):
    """Blend an RGBA/RGB array into a seamless tile (half-offset crossfade)."""
    h, w = arr.shape[:2]
    sh = np.roll(np.roll(arr, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = np.minimum(xx, w - 1 - xx) / (w / 2); wy = np.minimum(yy, h - 1 - yy) / (h / 2)
    k = np.clip(np.minimum(wx, wy) * 2.4, 0, 1)[..., None]
    return arr * k + sh * (1 - k)


def solid_rgba(w, h, col):
    return np.concatenate([np.ones((h, w, 3), np.float32) * col_arr(col), np.ones((h, w, 1), np.float32)], -1)


def cloth_base(w, h, col, seed=1, cell=3.0, var=0.06):
    base = solid_rgba(w, h, col)
    base[..., :3] *= weave(w, h, None, None, seed, cell)[..., None] * (1 - var / 2 + var * fbm(w, h, seed + 7, 90, 3))[..., None]
    return np.clip(base, 0, 1)


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in [i / (n - 1) for i in range(n)]]
