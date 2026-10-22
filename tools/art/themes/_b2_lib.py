"""Agent B2 helpers (sasak-lombok, jambi-angso, samarkand-biru, masjid-tajug): builds on _j1_lib (bbox-cropped painting)
with textile + ceramic media: woven cloth, songket supplementary gold weft, canting wax lines + dye on cloth, glazed tile
with glaze pooling/crackle, fired brick, wood grain. Previews -> /tmp/pen/nb-B2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-B2/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-B2/art"
_j1_lib.PREV = _p1_lib.PREV
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-B2/art"


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
    return strokes(W, H, [(pts, width, None) for pts in lines], cap=cap)


def rect(W, H, x0, y0, x1, y1):
    return shapes(W, H, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def poly(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def solid_rgba(w, h, col):
    return np.concatenate([np.ones((h, w, 3), np.float32) * col_arr(col), np.ones((h, w, 1), np.float32)], -1)


# ------------------------------------------------------------------ cloth
def weave(w, h, seed=1, cell=3.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    i = np.floor(xx / cell); j = np.floor(yy / cell)
    o = ((i + j) % 2).astype(np.float32)
    fx = (xx % cell) / cell; fy = (yy % cell) / cell
    shade = o * (0.82 + 0.22 * np.sin(fx * math.pi) ** 0.6) + (1 - o) * (0.82 + 0.22 * np.sin(fy * math.pi) ** 0.6)
    return shade * (0.94 + 0.12 * fbm(w, h, seed, 30, 2))


def cloth_base(w, h, col, seed=1, cell=3.0, var=0.06):
    base = solid_rgba(w, h, col)
    base[..., :3] *= weave(w, h, seed, cell)[..., None] * (1 - var / 2 + var * fbm(w, h, seed + 7, 90, 3))[..., None]
    return np.clip(base, 0, 1)


def songket_weft(mask, base="#c99a3a", seed=1, pitch=2.6, float_len=7.0, emboss=0.6):
    """Songket supplementary weft: horizontal metallic floats (each a short lit cylinder) that dip under the warp in
    a staggered brick rhythm; slight thread-to-thread brightness variation and a tarnished low end."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wob = (fbm(w, h, seed, 22, 2) - 0.5) * 0.9
    v = (yy + wob) / pitch
    f = v % 1.0
    row = np.floor(v)
    cyl = np.sin(f * math.pi) ** 0.8
    u = (xx / float_len + (row % 2) * 0.5) % 1.0
    tie = np.clip(1 - np.abs(u - 0.5) / 0.07, 0, 1)
    tvar = (np.sin(row * 12.9898 + 3.1) * 43758.5453) % 1.0
    sheen = 0.5 + 0.5 * np.sin((xx * 0.6 + yy * 0.3) / max(16, w * 0.05) + fbm(w, h, seed + 2, 46, 2) * 4)
    lum = 0.42 + 0.6 * cyl * (0.5 + 0.5 * sheen) + (tvar - 0.5) * 0.16
    lum *= 1 - tie * 0.55
    r, g, b = hex_rgb(base)
    rgb = np.stack([np.clip(r * lum * 1.22, 0, 1), np.clip(g * lum * 1.16, 0, 1), np.clip(b * lum * 1.0, 0, 1)], -1)
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    gy, gx = np.gradient(gaussian_filter(m, 1.2))
    rgb *= np.clip(1 - (gx + gy) * 4 * emboss, 0.6, 1.3)[..., None]
    a = m * (0.8 + 0.2 * cyl) * (1 - tie * 0.25)
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def silk_weft(mask, col, seed=1, pitch=2.4):
    """Coloured silk supplementary weft (songket accents)."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    f = ((yy + (fbm(w, h, seed, 18, 2) - 0.5)) / pitch) % 1.0
    lum = 0.8 + 0.25 * np.sin(f * math.pi) ** 0.6 + (fbm(w, h, seed + 3, 9, 2) - 0.5) * 0.1
    rgb = col_arr(col)[None, None, :] * lum[..., None]
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def wax_line(W, H, lines, width, seed=1, breaks=0.12):
    """Canting wax line mask: blotchy, varying width, small breaks."""
    m = strokes(W, H, [(pts, width * random.Random(seed + k).uniform(0.8, 1.2), (0.05, 0.05)) for k, pts in enumerate(lines)])
    br = fbm(W, H, seed + 1, 7, 2)
    m *= np.clip((br - breaks) * 6, 0, 1)
    return np.clip(displace(m, seed, 0.8, 6), 0, 1)


def dye(mask, col, seed=1, bleed=1.6, density=0.92, crackle=0.0):
    """Natural dye in cloth: soft capillary edge, uneven take-up, optional wax crackle veins (darker hairlines)."""
    h, w = mask.shape
    m = displace(mask, seed, bleed, 10)
    m = np.clip(gaussian_filter(m, bleed * 0.6) * 1.15, 0, 1)
    a = m * (0.78 + 0.22 * fbm(w, h, seed + 4, 40, 3)) * density
    rgb = col_arr(col)[None, None, :] * (1.04 - 0.18 * fbm(w, h, seed + 6, 70, 3))[..., None]
    if crackle:
        n = fbm(w, h, seed + 9, 14, 3)
        vein = np.clip(1 - np.abs(n - 0.5) * 38, 0, 1) * crackle
        rgb = rgb * (1 - vein[..., None] * 0.45)
        a = np.clip(a + vein * 0.3 * m, 0, 1)
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def tileable(arr):
    h, w = arr.shape[:2]
    sh = np.roll(np.roll(arr, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = np.minimum(xx, w - 1 - xx) / (w / 2); wy = np.minimum(yy, h - 1 - yy) / (h / 2)
    k = np.clip(np.minimum(wx, wy) * 2.4, 0, 1)[..., None]
    return arr * k + sh * (1 - k)


# ------------------------------------------------------------------ ceramics / brick / wood
def glaze_tile(mask, col, col2=None, seed=1, pool=0.5, crackle=0.25, gloss=0.5):
    """Glazed ceramic: glaze thins at the raised edge (lighter), pools in the middle (deeper), tiny pinholes, crackle,
    soft gloss highlight. Opaque within mask."""
    h, w = mask.shape
    m = displace(mask, seed, 0.9, 12)
    m = np.clip((gaussian_filter(m, 0.7) - 0.3) * 2.4, 0, 1)
    inner = gaussian_filter(m, 3.0)
    edge = np.clip(m - inner, 0, 1)
    ca, cb = col_arr(col), col_arr(col2 or col)
    t = fbm(w, h, seed + 2, 26, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    rgb = rgb * (1 - pool * 0.18 * (inner[..., None] - 0.5)) + edge[..., None] * 0.22
    if crackle:
        n = fbm(w, h, seed + 5, 10, 3)
        vein = np.clip(1 - np.abs(n - 0.5) * 40, 0, 1) * crackle
        rgb = rgb * (1 - vein[..., None] * 0.35)
    pin = (np.random.default_rng(seed).random((h, w)) > 0.9985).astype(np.float32)
    rgb = rgb * (1 - gaussian_filter(pin, 0.5)[..., None] * 0.8)
    gl = np.clip(fbm(w, h, seed + 8, 60, 2) - 0.62, 0, 1) * 2.0 * gloss
    rgb = rgb + gl[..., None] * 0.35
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def brick_field(W, H, bw=22, bh=8, mortar=1.6, seed=1, x0=0, y0=0):
    """Running-bond brick mask (1 = brick, 0 = mortar) and a per-brick tone field."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    row = np.floor((yy - y0) / bh)
    xo = xx - x0 + (row % 2) * bw / 2
    col = np.floor(xo / bw)
    fx = xo % bw; fy = (yy - y0) % bh
    m = ((fx > mortar) & (fy > mortar * 0.8)).astype(np.float32)
    tone = (np.sin(row * 17.13 + col * 7.77) * 43758.5453) % 1.0
    return gaussian_filter(m, 0.5), tone.astype(np.float32)


def bricks(dst, area, W, H, light, dark, mortar_col, seed=1, bw=22, bh=8):
    """Paint fired brick (with per-brick tone, chipped edges and mortar) into area."""
    bm, tone = brick_field(W, H, bw, bh, 1.6, seed)
    ca, cb = col_arr(light), col_arr(dark)
    rgb = ca * (1 - tone[..., None]) + cb * tone[..., None]
    rgb *= (0.9 + 0.2 * fbm(W, H, seed + 3, 8, 2))[..., None]
    mc = col_arr(mortar_col)
    rgb = rgb * bm[..., None] + mc * (1 - bm[..., None]) * (0.85 + 0.2 * fbm(W, H, seed + 4, 4, 2))[..., None]
    a = displace(area, seed, 1.0, 10)
    a = np.clip((gaussian_filter(a, 0.6) - 0.3) * 2.4, 0, 1)
    layer = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
    return over(dst, layer)


def wood(mask, col, col2, seed=1, angle=1.5708, grain=6.0):
    """Teak: gouache base + flowing grain lines."""
    h, w = mask.shape
    base = gouache_paint(mask, col, col2, seed=seed, rough=0.8, streak=1.0)
    g = hatch(w, h, angle, grain, 0.12, seed + 1, 3.0) * (0.5 + 0.5 * fbm(w, h, seed + 2, 20, 2))
    base[..., :3] *= (1 - g[..., None] * 0.28)
    return base


def shade_lr(mask, W, col="#1a0f08", strength=0.45, side=1, width=0.5):
    """Watercolour-ish side shadow: darkens one side of a mask's bbox."""
    b = bbox(mask, 0)
    if b is None:
        return blank(W, mask.shape[0])
    y0, y1, x0, x1 = b
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    t = np.clip((xx - x0 / W) / max(1e-3, (x1 - x0) / W), 0, 1)
    k = np.clip((t - (1 - width)) / width, 0, 1) if side > 0 else np.clip((width - t) / width, 0, 1)
    return flat(mask * k, col, strength)


def light_mask(h, w, cx, cy, r):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    return np.clip(1 - d, 0, 1) ** 1.5


def star_pts(cx, cy, r, n=8, inner=0.6, rot=0.0):
    pts = []
    for k in range(2 * n):
        a = rot + k * math.pi / n
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def poly_pts(cx, cy, r, n, rot=0.0):
    return [(cx + math.cos(rot + k * math.tau / n) * r, cy + math.sin(rot + k * math.tau / n) * r) for k in range(n)]


def hills(W, H, y, amp, seed, wl=0.5):
    rng = random.Random(seed)
    pts = [(-20, H + 20)]
    ph = rng.uniform(0, 6)
    for i in range(0, W + 41, 20):
        pts.append((i - 20, y - amp * (0.6 * math.sin(i / (W * wl) * math.pi * 2 + ph) + 0.4 * math.sin(i / (W * wl * 0.37) + ph * 2))))
    pts.append((W + 20, H + 20))
    return shapes(W, H, [pts], smooth=False)


def palm_m(W, H, x, by, h, lean, seed):
    """Coconut palm: tapered curving trunk, crown of long arching fronds that droop past the crown, drooping leaflets."""
    rr = random.Random(seed)
    top = (x + lean * h, by - h)
    items = [(curve([(x, by), (x + lean * h * 0.2, by - h * 0.5), top], 30), max(5, h * 0.045), (0.0, 0.12))]
    for k in range(11):
        a = -math.pi * 0.95 + k * math.pi * 0.9 / 10 + rr.gauss(0, 0.07)
        L = h * rr.uniform(0.42, 0.55)
        lift = math.sin(-a) * L * 0.25
        end = (top[0] + math.cos(a) * L, top[1] + L * 0.35 + rr.uniform(0, L * 0.25))
        mid = (top[0] + math.cos(a) * L * 0.5, top[1] - lift - 4)
        fr = curve([top, mid, end], 26)
        items.append((fr, 3.2, (0.0, 0.5)))
        for j in range(2, len(fr) - 1):
            (x0, y0), (x1, y1) = fr[j - 1], fr[j]
            ang = math.atan2(y1 - y0, x1 - x0)
            ll = (h * 0.13) * (1 - 0.6 * j / len(fr))
            for sg in (-1, 1):
                b2 = ang + sg * 0.75
                items.append(([(x1, y1), (x1 + math.cos(b2) * ll * 0.5, y1 + math.sin(b2) * ll * 0.5 + ll * 0.25), (x1 + math.cos(b2) * ll * 0.8, y1 + math.sin(b2) * ll * 0.8 + ll * 0.7)], 2.2, (0.0, 0.8)))
    return strokes(W, H, items)
