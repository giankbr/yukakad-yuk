"""Agent Q2 helpers (batik-garutan, gading-syari, ukiran-botani, ultah-kebun).
_j1_lib (local bbox painting, strokes/shapes masks) + copperplate engraving, batik dye/crackle, weave, small utils.
Previews -> /tmp/pen/nb-Q2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _j1_lib import *  # noqa
import _j1_lib
from _j1_lib import _apply
_p1_lib.PREV = "/tmp/pen/nb-Q2/art"
_j1_lib.PREV = _p1_lib.PREV
PREV = _p1_lib.PREV
os.makedirs(PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def flat(mask, col, a=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (mask * a)[..., None]], -1)


# ───────────────────────── copperplate engraving ─────────────────────────
def _crop(mask, pad=6):
    b = bbox(mask, pad)
    return b


def hatch_local(h, w, angle, spacing, duty, seed, bend=0.0, ox=0.0, oy=0.0, wob=0.8):
    """Parallel (optionally curved) engraved lines; duty = per-pixel line width fraction (0..1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xx += ox; yy += oy
    c, s_ = math.cos(angle), math.sin(angle)
    u = xx * c + yy * s_
    v = -xx * s_ + yy * c
    rng = np.random.default_rng(seed)
    n = gaussian_filter(rng.random((max(2, h // 12 + 2), max(2, w // 12 + 2))).astype(np.float32), 1.0)
    n = np.asarray(Image.fromarray(((n - n.min()) / (np.ptp(n) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255 - 0.5
    if bend:
        vc = v - v.mean()
        u = u + bend * (vc ** 2) / max(1.0, (np.abs(vc).max()))
    u = (u + n * wob * 2) / spacing
    f = np.abs((u % 1.0) - 0.5) * 2
    return np.clip((duty - f) / 0.22 + 0.5, 0, 1).astype(np.float32)


def engrave_shape(ink, mask, angle, spacing=3.4, base=0.25, edge=0.5, grad=0.4, light=(-0.6, -0.8), seed=1,
                  cross=0.62, bend=0.0, outline=1.7, stipple=0.0, knock=True, fill_white=True, tone_add=None):
    """Engrave one form into the ink layer (float HxW, 0..1).
    tone = base + edge darkening + directional gradient (light from `light`). Lines follow `angle` (curved by `bend`),
    cross-hatching where tone > cross, a hand-cut outline, optional stipple. Forms painted later sit in front (knock)."""
    H, W = ink.shape
    b = bbox(mask, 6)
    if b is None:
        return ink
    y0, y1, x0, x1 = b
    m = mask[y0:y1, x0:x1]
    h, w = m.shape
    inner = gaussian_filter(m, max(2.0, min(h, w) * 0.09))
    edgef = np.clip((m - inner) * 3.2, 0, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    lx, ly = light
    g = (xx / max(1, w) - 0.5) * (-lx) + (yy / max(1, h) - 0.5) * (-ly)
    g = (g - g.min()) / (np.ptp(g) + 1e-6)
    tone = base + edge * edgef + grad * (g - 0.35)
    if tone_add is not None:
        tone = tone + tone_add(xx + x0, yy + y0)
    tone = np.clip(tone, 0, 1)
    l1 = hatch_local(h, w, angle, spacing, 0.08 + 0.7 * tone, seed, bend, x0, y0)
    l1 *= np.clip((tone - 0.2) * 5, 0, 1)
    out = l1
    if cross is not None:
        t2 = np.clip((tone - cross) / (1 - cross + 1e-6), 0, 1)
        l2 = hatch_local(h, w, angle + 1.05, spacing * 1.08, 0.08 + 0.55 * t2, seed + 3, bend * 0.5, x0, y0)
        out = np.maximum(out, l2 * (t2 > 0.02))
    if stipple:
        rng = np.random.default_rng(seed + 9)
        pts = rng.random((h, w)) < stipple * 0.06 * tone
        d = gaussian_filter(pts.astype(np.float32), 0.55) * 4.5
        out = np.maximum(out, np.clip(d, 0, 1))
    out = out * m
    if outline:
        # outline = mask edge band (hand cut: varies a little in width, thicker on the shadow side)
        er = np.clip((m - gaussian_filter(m, outline * 0.9)) * 2.4, 0, 1)
        er = np.clip(er * (0.75 + 0.6 * g), 0, 1)
        out = np.maximum(out, er)
    region = ink[y0:y1, x0:x1]
    if knock:
        region = region * (1 - np.clip(m * 1.4, 0, 1))
    ink = ink.copy()
    ink[y0:y1, x0:x1] = np.maximum(region, out)
    return ink


def engrave_line(ink, pts_list, width=1.6, taper=(0.15, 0.3)):
    """Engraved strokes (stems, veins, outlines) added on top."""
    H, W = ink.shape
    m = strokes(W, H, [(p, width, taper) for p in pts_list])
    return np.maximum(ink, m)


def ink_to_rgba(ink, col="#1d1915", seed=1, wear=0.18):
    """Printed ink: slightly uneven take-up with a few missed specks."""
    h, w = ink.shape
    rng = np.random.default_rng(seed)
    sp = gaussian_filter(rng.random((h, w)).astype(np.float32), 0.8)
    sp = (sp - sp.min()) / (np.ptp(sp) + 1e-6)
    cov = 1 - wear * np.clip((sp - 0.6) * 3.5, 0, 1)
    a = np.clip(ink * cov * 1.05, 0, 1)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)


def frond_pts(x, y, L, ang, curl=0.25, n=40):
    """Curved rachis points."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = ang + curl * t * t * 2.2
        if i == 0:
            px, py = x, y
        else:
            px += math.cos(a) * L / (n - 1); py += math.sin(a) * L / (n - 1)
        pts.append((px, py))
    return pts


# ───────────────────────── batik ─────────────────────────
def weave(h, w, seed=1, amt=0.05):
    """Fine cotton weave multiplier (~1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rng = np.random.default_rng(seed)
    a = np.sin(xx * 1.9) * np.sin(yy * 1.9)
    slub = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.4, 3.0))
    slub = (slub - slub.mean()) / (slub.std() + 1e-6)
    slub2 = gaussian_filter(rng.random((h, w)).astype(np.float32), (3.0, 0.4))
    slub2 = (slub2 - slub2.mean()) / (slub2.std() + 1e-6)
    return 1 + amt * (0.35 * a + 0.4 * slub + 0.4 * slub2)


def crackle(h, w, seed=1, width=0.010, scale=26):
    """Remukan: fine veins where cracked wax let the dye in."""
    out = np.zeros((h, w), np.float32)
    for k in range(2):
        n = fbm(w, h, seed + k * 31, scale * (1 + k * 0.7), 3)
        out = np.maximum(out, np.clip(1 - np.abs(n - 0.5) / width, 0, 1))
    return out


def dye(mask, col, col2=None, seed=1, density=0.92, bleed=0.9, rough=1.2):
    """Batik dye inside a wax-resist edge: tiny bleed, mottled uptake (RGBA)."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 14)
    m = np.clip(gaussian_filter(m, bleed) * 1.15, 0, 1)
    low = fbm(w, h, seed + 4, 50, 3)
    a = m * density * (0.86 + 0.14 * low)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 6, 80, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def D(dst, mask, *a, pad=8, **k):
    return _apply(dst, mask, lambda q: dye(q, *a, **k), "over", pad)


def multiply_rgb(arr, f):
    out = arr.copy()
    out[..., :3] = np.clip(out[..., :3] * f[..., None], 0, 1)
    return out
