"""Agent T1 helpers (batik-semarangan, sarung-samarinda, botol-attar, ultah-donat).
Builds on _s2_lib (local-crop media, gouache+pencil paint, woven cloth) and adds: batik dye fill with wax
outline (klowong), crackle (remukan) and canting dots (cecek); silk check cloth; glass bottle shading.
Previews -> /tmp/pen/nb-T1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _s2_lib import *  # noqa
import _s2_lib
import numpy as np
from scipy.ndimage import gaussian_filter, binary_dilation
from PIL import Image

PREV = "/tmp/pen/nb-T1/art"
os.makedirs(PREV, exist_ok=True)
_s2_lib.PREV = PREV


def prev(arr, name, bg=None, tone="#f8f4ea"):
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


# ---------------------------------------------------------------- batik
def crackle(w, h, seed, scale=26.0, thick=0.06):
    """Remukan: fine network of wax-crack lines (0..1)."""
    n = fbm(w, h, seed, scale, 3)
    r = np.abs(n - 0.5)
    lines = np.clip((thick - r) / thick, 0, 1) ** 2
    n2 = fbm(w, h, seed + 4, scale * 0.55, 2)
    lines2 = np.clip((thick * 0.7 - np.abs(n2 - 0.5)) / (thick * 0.7), 0, 1) ** 2
    return np.maximum(lines, lines2 * 0.7)


def dye(mask, col, col2=None, seed=1, mottle=0.12):
    """Batik dye: soaked-in colour, slight tonal drift, cloth weave texture, soft bleeding edge."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(displace(mask, seed, 1.2, 14), 0.6), 0, 1)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 3, 60, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    rgb = rgb * (1 - mottle + mottle * 2 * fbm(w, h, seed + 9, 18, 2)[..., None])
    yy, xx = np.mgrid[0:h, 0:w]
    weave = 1 + 0.03 * (((xx + yy) % 2) - 0.5)
    rgb = rgb * weave[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def D(dst, mask, col, col2=None, pad=8, **k):
    return OV(dst, mask, lambda m: dye(m, col, col2, **k), pad=pad)


def outline(mask, px=2.2):
    """Wax outline ring (klowong) around a mask."""
    inner = gaussian_filter(mask, px * 0.5)
    outer = gaussian_filter(mask, px)
    ring = np.clip((outer - mask) * 4.0, 0, 1)
    return np.clip(ring + np.clip((mask - inner) * 2.5, 0, 1) * 0.6, 0, 1)


def cecek(w, h, pts, r=1.6):
    return circles(w, h, [(x, y, r) for x, y in pts])


def remukan(dst, mask, col, seed=1, strength=0.55, scale=24.0):
    """Crackle lines in dye colour across an area (where wax cracked and dye seeped in)."""
    h, w = mask.shape
    cr = crackle(w, h, seed, scale) * mask
    return tint(dst, cr, col, strength, pad=2)


def fill_dots(mask, step, rng, r=1.6, jit=0.6, margin=0.5):
    """Positions on a jittered grid inside mask (for isen-isen)."""
    h, w = mask.shape
    pts = []
    for y in np.arange(step / 2, h, step):
        off = step / 2 if int(y / step) % 2 else 0
        for x in np.arange(step / 2 + off, w, step):
            xx = x + rng.uniform(-jit, jit); yy = y + rng.uniform(-jit, jit)
            if 0 <= int(yy) < h and 0 <= int(xx) < w and mask[int(yy), int(xx)] > margin:
                pts.append((xx, yy))
    return pts


# ---------------------------------------------------------------- silk check cloth (sarung samarinda)
def check_cloth(W, H, warp, weft, seed=1, sheen=0.18, tight=1):
    """Fine hand-woven silk check: warp stripes (x) and weft stripes (y) as lists of (threads, hex).
    Each thread = `tight` px. Colour at a crossing alternates warp/weft (plain weave) -> true check mixing."""
    rng = np.random.default_rng(seed)
    def seq(st):
        s = []
        for n, c in st:
            s += [c] * int(n)
        return np.array([hex_rgb(c) for c in s], np.float32)
    wx = seq(warp); wy = seq(weft)
    xs = (np.arange(W) // tight) % len(wx); ys = (np.arange(H) // tight) % len(wy)
    cw = wx[xs][None, :, :] * np.ones((H, 1, 1), np.float32)
    cf = wy[ys][:, None, :] * np.ones((1, W, 1), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    over_ = (((xx // tight) + (yy // tight)) % 2).astype(np.float32)[..., None]
    img = cw * over_ + cf * (1 - over_)
    img = img * 0.82 + (cw + cf) * 0.09
    # per-thread tone
    tx = 1 + (rng.random(W) - 0.5) * 0.08; ty = 1 + (rng.random(H) - 0.5) * 0.08
    img = img * tx[None, :, None] * ty[:, None, None]
    # silk sheen: soft diagonal light band + thread relief
    sh = 0.5 + 0.5 * np.sin((xx * 0.6 + yy * 0.25) / 55.0)
    img = img * (1 + sheen * (sh[..., None] - 0.4))
    rel = 0.95 + 0.05 * np.cos((xx % 2) * math.pi) * np.cos((yy % 2) * math.pi)
    img = img * rel[..., None]
    return np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], -1)


# ---------------------------------------------------------------- glass
def glass(mask, col, seed=1, light=(-0.6, -0.8), depth=0.55, alpha=0.9):
    """Coloured glass body: saturated deep rim, light passing through to a bright focused caustic low in the body,
    a soft window reflection on the lit side and slight internal mottling."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(displace(mask, seed, 0.8, 20), 0.7), 0, 1)
    c = np.array(hex_rgb(col), np.float32)
    dist = gaussian_filter(m, 10)                      # 0 at edge .. 1 deep inside
    ys, xs = np.where(m > 0.5)
    if len(xs) == 0:
        return np.zeros((h, w, 4), np.float32)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = np.clip((yy - y0) / max(1, y1 - y0), 0, 1)      # 0 top .. 1 bottom
    u = (xx - (x0 + x1) / 2) / max(1, (x1 - x0) / 2)    # -1 left .. 1 right
    deep = c * 0.22
    mid = c * 0.95
    bright = np.clip(c * 1.35 + 0.18, 0, 1)
    t = np.clip(dist * 1.5, 0, 1)[..., None] ** 0.7
    rgb = deep * (1 - t) + mid * t
    caustic = np.exp(-(((u + 0.15) / 0.55) ** 2 + ((v - 0.8) / 0.16) ** 2))
    rgb = rgb * (1 - caustic[..., None] * 0.6) + bright * caustic[..., None] * 0.6
    shade = np.clip(u * 0.5 + 0.15, 0, 0.5)              # right side darker (light from left)
    rgb = rgb * (1 - shade[..., None] * 0.6)
    mot = fbm(w, h, seed + 5, 26, 3)
    rgb = rgb * (0.93 + 0.14 * mot[..., None])
    a = m * (alpha - 0.18 * caustic)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def highlight(dst, pts, width, col="#fff8e8", alpha=0.85, w=None, h=None):
    H, W = dst.shape[:2]
    m = strokes(W, H, [(pts, width, (0.3, 0.4))])
    m = gaussian_filter(m, 0.8)
    return tint(dst, m, col, alpha, pad=4)
