"""Agent T3 helpers (taman-sari, sadu-tenun, rumah-pohon, ultah-pantai).
Builds on _e6_lib (-> _d5_lib / _jw_lib / _j1_lib / _p1_lib / art). Adds: lit plaster relief (emboss), caustic water,
a coarse warp-faced wool weave renderer (sadu), string-light glow, and small shape helpers.
Previews -> /tmp/pen/nb-T3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _e6_lib import *  # noqa
import _p1_lib
import _d5_lib
import _e6_lib
import art as _art

PREV = "/tmp/pen/nb-T3/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_d5_lib.PREV = PREV
_e6_lib.PREV = PREV


def preview(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.PREV = PREV
    return _p1_lib.preview(arr, name, tone=tone, bg=bg)


def solid_rgba(mask, col, a=1.0):
    return np.concatenate([np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32), (np.clip(mask, 0, 1) * a)[..., None]], -1)


def emboss(art, relief, nx, light="#fffaf0", dark="#7a6648", s=1.6, k=9.0, hi_a=0.75, lo_a=0.7, cast=3):
    """Light a raised relief (mask) from the top-left: highlight rims, shaded rims and a short cast shadow."""
    h = gaussian_filter(relief, s)
    gy, gx = np.gradient(h)
    L = -(gx + gy) * k
    hi = np.clip(L, 0, 1) * np.clip(h * 3, 0, 1)
    lo = np.clip(-L, 0, 1)
    if cast:
        sh = np.clip(np.roll(np.roll(gaussian_filter(relief, 1.2), cast, 0), cast, 1) - relief, 0, 1)
        art = G(art, sh, dark, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.8)
    art = G(art, lo, dark, seed=nx(), density=lo_a, edge=0, bloom=0, rough=0.5, feather=0.4)
    art = OV(art, hi, lambda m: solid_rgba(m, light, hi_a))
    return art


def stucco(art, m, nx, base="#efe3c8", base2="#e6d6b4", grime="#9c8a68", moss="#8d9a6a", wear=0.5):
    """Old lime plaster: matte gouache, mottled weathering streaks running down, a little moss in the low parts."""
    art = GP(art, m, base, base2, seed=nx(), rough=1.4, streak=0.5)
    h, w = m.shape
    streak = gaussian_filter(np.random.default_rng(nx()).random((h, w)).astype(np.float32), (14, 1.2))
    streak = np.clip((streak - streak.mean()) / (streak.std() + 1e-6) * 0.5, 0, 1)
    mott = fbm(w, h, nx(), 60, 3)
    g = m * np.clip(mott * 1.4 - 0.55, 0, 1) * (0.5 + streak) * wear
    art = G(art, g, grime, seed=nx(), density=0.38, edge=0.25, bloom=0.4, rough=3, feather=1.5)
    if moss:
        yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
        mm = m * np.clip(fbm(w, h, nx(), 30, 3) * 1.6 - 0.95, 0, 1) * np.clip(yy * 2 - 0.9, 0, 1)
        art = G(art, mm, moss, seed=nx(), density=0.35, edge=0.3, bloom=0.3, rough=2)
    return art


def caustics(w, h, seed, scale=46.0, sharp=10.0):
    """Ridge network (0..1) like sun caustics on a pool floor."""
    a = fbm(w, h, seed, scale, 3)
    b = fbm(w, h, seed + 9, scale * 0.6, 3)
    r1 = 1 - np.abs(a * 2 - 1)
    r2 = 1 - np.abs(b * 2 - 1)
    return np.clip(np.maximum(r1, r2) ** sharp * 1.4, 0, 1).astype(np.float32)


def bulb(art, W, H, x, y, r, nx, col="#ffe6a0", core="#fffaf0", halo=2.6):
    m = circles(W, H, [(x, y, r)])
    art = OV(art, circles(W, H, [(x, y, r * halo)]), lambda mm: glow(mm, col, r * 0.9, 0.35))
    art = GP(art, m, col, core, seed=nx(), rough=0.4, streak=0.2)
    return art


# ---------------------------------------------------------------- sadu weave
def weave(grid, palette, cell=(8, 12), seed=1, fuzz=0.6, gap=0.9):
    """Render a warp-faced weave: grid[r][c] -> palette index. Each cell is one wool float (tall rounded stitch)
    with fibre streaks, uneven yarn tone and a soft dark gap between floats. Returns opaque RGBA."""
    rng = np.random.default_rng(seed)
    g = np.asarray(grid)
    rows, cols = g.shape
    cw, ch = cell
    W, H = cols * cw, rows * ch
    pal = np.array([hex_rgb(p) for p in palette], np.float32)
    base = pal[np.repeat(np.repeat(g, ch, 0), cw, 1)]
    # per-yarn tone drift (each warp thread slightly different) + per-float tone
    thread = 1 + (rng.random(cols) - 0.5) * 0.10
    flt = 1 + (rng.random((rows, cols)) - 0.5) * 0.10
    tone = np.repeat(np.repeat(flt * thread[None, :], ch, 0), cw, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # alternate rows offset half a cell to read as interlaced floats
    off = ((yy // ch) % 2) * (cw * 0.0)
    u = ((xx + off) % cw) / cw - 0.5
    v = (yy % ch) / ch - 0.5
    d = np.sqrt((u / 0.5) ** 2 + (v / 0.5) ** 4 * 0.9)
    body = np.clip(1.15 - d, 0, 1)
    shade = 0.55 + 0.45 * body ** 0.6
    # fibre streaks along the warp (vertical)
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (2.2, 0.35))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    slant = gaussian_filter(rng.random((H, W)).astype(np.float32), (1.6, 0.4))
    slant = (slant - slant.mean()) / (slant.std() + 1e-6)
    rgb = base * (tone * shade)[..., None] * (1 + fib[..., None] * 0.05 * fuzz + slant[..., None] * 0.025)
    # dark gaps between floats
    gapm = np.clip((d - 0.95) * 4, 0, 1) * gap
    rgb = rgb * (1 - gapm[..., None] * 0.45)
    # halo fuzz: blur a little and add stray hairs
    rgb = gaussian_filter(rgb, (0.5, 0.5, 0))
    hair = (rng.random((H, W)) > 0.9985).astype(np.float32)
    hair = gaussian_filter(hair, (0.4, 3.0)) * 3
    rgb = rgb * (1 - hair[..., None] * 0.25) + hair[..., None] * 0.08
    # large-scale handspun unevenness
    low = fbm(W, H, seed + 4, 90, 3)
    rgb = rgb * (0.93 + 0.12 * low)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
