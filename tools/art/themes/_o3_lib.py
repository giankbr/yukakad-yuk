"""Agent O3 helpers (majapahit-bata, tadelakt-maroko, line-art, kelas-workshop): _j1_lib (bbox-local painting) plus
brick masonry, emboss shading, brush-pen ink lines and woven bands. Previews -> /tmp/pen/nb-O3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _j1_lib import *  # noqa
_p1_lib.PREV = "/tmp/pen/nb-O3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art

PREV = "/tmp/pen/nb-O3/art"


def clear():
    _art._fbm_cache.clear()


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def hexarr(h):
    return np.array(hex_rgb(h), np.float32)


def brick_field(W, H, bw, bh, seed=1, wob=1.6, mortar=1.4, wrap=False):
    """Running-bond brick layout -> (brick id hash in [0,1], mortar mask, per-brick bevel 0..1)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if wob and not wrap:
        yy = yy + (fbm(W, H, seed, 30, 2) - 0.5) * wob * 2
        xx = xx + (fbm(W, H, seed + 1, 30, 2) - 0.5) * wob * 2
    row = np.floor(yy / bh)
    off = (row % 2) * bw / 2
    col = np.floor((xx + off) / bw)
    rng = np.random.default_rng(seed)
    tab = rng.random(4096).astype(np.float32)
    idx = ((row.astype(np.int64) * 73 + col.astype(np.int64) * 151) % 4096)
    hid = tab[idx]
    fy = (yy % bh) / bh
    fx = ((xx + off) % bw) / bw
    my, mx = mortar / bh, mortar / bw
    mort = np.clip(np.maximum((my - np.minimum(fy, 1 - fy)) / my, (mx - np.minimum(fx, 1 - fx)) / mx) * 1.5, 0, 1)
    # bevel: bricks catch light on the upper edge, darker lower edge
    bev = np.clip(1 - fy * 1.0, 0, 1)
    return hid, mort, bev, row


def brick_paint(mask, W, H, cols, seed=1, bw=30, bh=11, mort_col="#6b3a2a", wob=1.6, mortar=1.4, light=None):
    """Opaque brick masonry inside mask: per-brick colour from cols (list of hex), mortar joints, mottling, chips."""
    hid, mort, bev, row = brick_field(W, H, bw, bh, seed, wob, mortar)
    pal = np.stack([hexarr(c) for c in cols])
    k = np.clip((hid * (len(cols) - 1)), 0, len(cols) - 1.001)
    i0 = np.floor(k).astype(int); t = (k - i0)[..., None]
    rgb = pal[i0] * (1 - t) + pal[np.minimum(i0 + 1, len(cols) - 1)] * t
    mott = fbm(W, H, seed + 3, 14, 3)
    rgb = rgb * (0.86 + 0.24 * mott[..., None])
    big = fbm(W, H, seed + 5, 120, 3)
    rgb = rgb * (0.9 + 0.18 * big[..., None])
    rgb = rgb * (1.0 + 0.06 * (bev[..., None] - 0.5))
    mc = hexarr(mort_col)
    rgb = rgb * (1 - mort[..., None] * 0.85) + mc * mort[..., None] * 0.85
    # chipped corners / pitting
    pit = fbm(W, H, seed + 9, 5, 2)
    rgb = rgb * (1 - np.clip((pit - 0.7) * 3, 0, 1)[..., None] * 0.35)
    s = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (0.5, 3.0))
    s = (s - s.mean()) / (s.std() + 1e-6)
    rgb = rgb * (1 + s[..., None] * 0.03)
    m = displace(mask, seed + 2, 1.6, 14)
    m = np.clip((gaussian_filter(m, 0.6) - 0.3) * 2.4, 0, 1)
    if light is not None:
        rgb = rgb * light[..., None]
    return rgba(rgb, m)


def shade(arr, mask_or_field, col="#000000", amount=0.5):
    """Multiply-darken (or tint) arr by a 0..1 field."""
    out = arr.copy()
    c = hexarr(col)
    f = np.clip(mask_or_field, 0, 1)[..., None] * amount
    out[..., :3] = out[..., :3] * (1 - f) + out[..., :3] * c * f
    return out


def lighten(arr, field, col="#ffffff", amount=0.4):
    out = arr.copy()
    f = np.clip(field, 0, 1)[..., None] * amount
    out[..., :3] = out[..., :3] * (1 - f) + hexarr(col) * f
    return out


def emboss(mask, blur=2.0, angle=-2.3):
    """Relief light field from a (soft) height mask: >0.5 lit, <0.5 shadow. angle: light direction (radians)."""
    gy, gx = np.gradient(gaussian_filter(mask, blur))
    lx, ly = math.cos(angle), math.sin(angle)
    return np.clip(0.5 + (gx * lx + gy * ly) * 8, 0, 1)


def ink(W, H, pts, width, seed=1, press=None, jitter=0.35, dry=0.0):
    """Brush-pen line mask with pressure variation along the stroke (press(t) -> 0..1) and slight wobble."""
    rng = random.Random(seed)
    n = len(pts)
    nz = OpenSimplex(seed)
    cv = Canvas(W, H)
    for i in range(n - 1):
        t = i / max(1, n - 2)
        p = press(t) if press else (0.55 + 0.45 * (0.5 + 0.5 * nz.noise2(t * 9, 0.3)))
        wd = max(0.5, width * p)
        if dry and rng.random() < dry * (1 - p):
            continue
        a, b = pts[i], pts[i + 1]
        o1 = (nz.noise2(i * 0.05, 1.1) * jitter, nz.noise2(i * 0.05, 2.2) * jitter)
        o2 = (nz.noise2((i + 1) * 0.05, 1.1) * jitter, nz.noise2((i + 1) * 0.05, 2.2) * jitter)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wd, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        cv.c.drawLine(a[0] + o1[0], a[1] + o1[1], b[0] + o2[0], b[1] + o2[1], paint)
    return cv.array()[..., 3]


def ink_paint(mask, col, seed=1, wet=0.35):
    """Ink colour for a line mask: slightly darker where lines are thick/overlap, faint feathering, paper tooth."""
    h, w = mask.shape
    m = np.clip(mask, 0, 1)
    tooth = fbm(w, h, seed, 3, 2)
    a = m * (0.88 + 0.12 * tooth)
    halo = np.clip(gaussian_filter(m, 1.2) * wet, 0, 0.25)
    a = np.maximum(a, halo)
    rgb = np.ones((h, w, 3), np.float32) * hexarr(col)
    rgb = rgb * (1 - 0.15 * np.clip(gaussian_filter(m, 2) - 0.5, 0, 1)[..., None])
    return rgba(rgb, a)


def sample_curve(ctrl, steps=None):
    """Smooth Catmull-Rom polyline through control points with roughly even sampling."""
    steps = steps or max(40, len(ctrl) * 14)
    return curve(ctrl, steps)
