"""Agent H3 helpers (alor-moko, baliem-honai, ikat-adras, arisan-keluarga): builds on _jw_lib/_j1_lib/_p1_lib and adds
cast-bronze bodies with patina, ikat feathering (warp-shifted edges), soft shading maps, edge fades and thatch/fibre
strokes. Previews -> /tmp/pen/nb-H3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib, _j1_lib, _p1_lib
import art as _art
PREV = "/tmp/pen/nb-H3/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_jw_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def col_arr(mask, col, alpha):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(alpha, 0, 1)[..., None]], -1)


def edge_fade(art, px, sides="lrtb"):
    h, w = art.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    big = 1e6
    d = np.full((h, w), big, np.float32)
    if "l" in sides: d = np.minimum(d, xx)
    if "r" in sides: d = np.minimum(d, w - 1 - xx)
    if "t" in sides: d = np.minimum(d, yy)
    if "b" in sides: d = np.minimum(d, h - 1 - yy)
    out = art.copy()
    out[..., 3] *= np.clip(d / px, 0, 1) ** 1.4
    return out


def shade(dst, mask, factor, keep=True):
    """Multiply dst rgb by a factor map (1 = unchanged) inside mask."""
    out = dst.copy()
    f = 1 + (factor - 1) * mask
    out[..., :3] = np.clip(out[..., :3] * f[..., None], 0, 1)
    return out


def tone_over(dst, mask, col, amt):
    """Soft opaque tint toward col where mask (0..1) * amt."""
    out = dst.copy()
    a = np.clip(mask * amt, 0, 1)[..., None]
    out[..., :3] = out[..., :3] * (1 - a) + np.array(hex_rgb(col), np.float32) * a
    return out


def warp_feather(mask, seed, axis=0, bundle=3, amp=6.0, blur=1.2):
    """Ikat feathering: shift the mask along the warp (axis=0: vertical warp -> each column bundle shifts vertically)."""
    rng = np.random.default_rng(seed)
    h, w = mask.shape
    out = np.zeros_like(mask)
    n = (w if axis == 0 else h)
    for i in range(0, n, bundle):
        s = int(round(rng.normal(0, amp * 0.5)))
        s = max(-int(amp * 1.6), min(int(amp * 1.6), s))
        if axis == 0:
            out[:, i:i + bundle] = np.roll(mask[:, i:i + bundle], s, 0)
        else:
            out[i:i + bundle, :] = np.roll(mask[i:i + bundle, :], s, 1)
    if blur:
        out = gaussian_filter(out, (blur * 1.8, blur * 0.3) if axis == 0 else (blur * 0.3, blur * 1.8))
    return np.clip(out, 0, 1)


def threads(w, h, axis=0, spacing=3.0, seed=1, amt=0.1):
    """Woven thread texture factor map around 1 (warp lines along axis)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx if axis == 0 else yy) / spacing
    n = fbm(w, h, seed, 40, 2)
    f = 1 + amt * (np.sin(u * math.tau + n * 2) * 0.6 + (fbm(w, h, seed + 2, 6, 2) - 0.5))
    return f.astype(np.float32)


def cyl_light(w, h, cx, hw_of_y, lit=-0.45, amb=0.55):
    """Cylindrical lighting map: hw_of_y(y array) -> half-width; light from the left (lit < 0)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    hw = np.maximum(hw_of_y(yy), 1)
    n = np.clip((xx - cx) / hw, -1, 1)
    z = np.sqrt(np.clip(1 - n * n, 0, 1))
    lx, lz = lit, math.sqrt(1 - lit * lit)
    d = np.clip(n * lx + z * lz, 0, 1)
    return amb + (1 - amb) * d, n


def bronze_body(W, H, mask, light, nx, base="#9a6a34", dark="#3e2612", hi="#e6b77a", patina="#5f9e8a", patina_amt=0.5, seed=5):
    """Cast bronze: gouache base, lighting map (0..1) -> dark..hi, verdigris patina blooms, pitting."""
    art = GP(blank(W, H), mask, base, mix(base, dark, 0.3), seed=nx(), rough=1.2, streak=0.8, pad=10)
    lo = np.array(hex_rgb(dark), np.float32); mid = np.array(hex_rgb(base), np.float32); hh = np.array(hex_rgb(hi), np.float32)
    t = np.clip(light, 0, 1)[..., None]
    ramp = np.where(t < 0.6, lo + (mid - lo) * (t / 0.6), mid + (hh - mid) * ((t - 0.6) / 0.4))
    tex = art[..., :3] / np.maximum(np.array(hex_rgb(base), np.float32), 1e-3)
    out = art.copy()
    out[..., :3] = np.clip(ramp * (0.85 + 0.15 * tex), 0, 1)
    if patina_amt:
        f = fbm(W, H, seed, 60, 4)
        pm = mask * np.clip((f - (1 - patina_amt)) * 3.2, 0, 1)
        out = G(out, pm, patina, mix(patina, "#9cc9b4", 0.4), seed=nx(), density=0.75, edge=0.5, bloom=0.4, rough=4, feather=1.2, gran=0.4)
    pits = (np.random.default_rng(seed).random((H, W)) > 0.996).astype(np.float32)
    pits = gaussian_filter(pits, 0.7) * 3 * mask
    out = shade(out, np.clip(pits, 0, 1), 0.55)
    return out


def relief(art, mask, nx, light="#f2d3a0", dark="#2a1a0c", d=2, hi_amt=0.6, lo_amt=0.65):
    """Raised cast relief from a mask: highlight up-left edge, shadow down-right edge."""
    m = gaussian_filter(mask, 0.6)
    hi = np.clip(m - np.roll(np.roll(m, d, 0), d, 1), 0, 1)
    lo = np.clip(m - np.roll(np.roll(m, -d, 0), -d, 1), 0, 1)
    art = OV(art, lo, lambda mm: col_arr(mm, dark, mm * lo_amt), pad=6)
    art = OV(art, hi, lambda mm: col_arr(mm, light, mm * hi_amt), pad=6)
    return art


def fibre_strokes(rng, x0, y0, x1, y1, n, length, ang, jit=0.3, width=(1.5, 3.0)):
    """Random short strokes (thatch, grass, straw) inside a box as items for strokes()."""
    items = []
    for _ in range(n):
        x = rng.uniform(x0, x1); y = rng.uniform(y0, y1)
        a = ang + rng.uniform(-jit, jit); L = length * rng.uniform(0.6, 1.3)
        items.append(([(x, y), (x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5 + rng.uniform(-1, 1)), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(*width), (0.1, 0.5)))
    return items
