"""Agent E5 helpers (kolase-kertas, kebun-teh, ultah-truk, ultah-safari): builds on _d6_lib (gouache bodies, kid
faces, bbox-local painting, crayon) and adds a cut-paper renderer (scissor / torn edge, fibre grain, drop shadow),
watercolour landscape helpers (contour rows, mist bands) and wheels. Previews -> /tmp/pen/nb-E5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _d6_lib import *  # noqa
import _d6_lib, _a6_lib, _j1_lib, _p1_lib
PREV = "/tmp/pen/nb-E5/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_d6_lib, _a6_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def _crop(mask, pad):
    return bbox(mask, pad, 0.01)


def shift(a, dx, dy):
    """Translate a 2-D array with zero fill (no wrap-around)."""
    out = np.zeros_like(a)
    h, w = a.shape
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    out[yd, xd] = a[ys, xs]
    return out


def cutpaper(art, mask, col, seed=1, shadow=0.3, torn=0.0, edge=1.4, grain=1.0, core="#fbf6ea", sdx=3, sdy=5, sblur=3.5, fleck=None):
    """Construction-paper cut-out: scissor-cut edge (low-frequency wobble, crisp), optional torn edge with the white
    fibrous paper core showing, matte fibre texture with flecks, and a soft drop shadow underneath."""
    H, W = mask.shape
    b = _crop(mask, 30)
    if b is None:
        return art
    y0, y1, x0, x1 = b
    m = mask[y0:y1, x0:x1]
    h, w = m.shape
    m = displace(m, seed, edge, 70)
    if torn:
        m = displace(m, seed + 4, torn, 7)
    m = np.clip((gaussian_filter(m, 0.6) - 0.5) * 3.2 + 0.5, 0, 1)
    out = art.copy()
    reg = out[y0:y1, x0:x1]
    if shadow:
        sh = shift(gaussian_filter(m, sblur), sdx, sdy)
        if torn:
            rimm = displace(np.clip(gaussian_filter(m, 1.6) * 2.2, 0, 1), seed + 9, torn * 0.8, 5)
            sh = np.maximum(sh, shift(gaussian_filter(rimm, sblur), sdx, sdy))
        reg = over(reg, col_arr(sh, "#2a1d14", sh * shadow))
    if torn:
        rimm = displace(np.clip(gaussian_filter(m, 1.6) * 2.2, 0, 1), seed + 9, torn * 0.8, 5)
        rimm = np.clip((rimm - 0.5) * 4 + 0.5, 0, 1)
        f = gaussian_filter(np.random.default_rng(seed + 2).random((h, w)).astype(np.float32), 0.7)
        f = (f - f.min()) / (f.max() - f.min() + 1e-6)
        reg = over(reg, col_arr(rimm, core, rimm * np.clip(0.75 + f * 0.4, 0, 1)))
    ca = np.array(hex_rgb(col), np.float32)
    mot = fbm(w, h, seed + 3, 50, 3) - 0.5
    ang = random.Random(seed).uniform(0, math.pi)
    fib = gaussian_filter(np.random.default_rng(seed + 5).random((h, w)).astype(np.float32), (0.45, 2.6))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    fine = gaussian_filter(np.random.default_rng(seed + 6).random((h, w)).astype(np.float32), 0.5)
    fine = (fine - fine.mean()) / (fine.std() + 1e-6)
    lum = 1 + mot * 0.09 * grain + fib * 0.022 * grain + fine * 0.018 * grain
    rgb = ca[None, None, :] * lum[..., None]
    if fleck:
        fl = (np.random.default_rng(seed + 7).random((h, w)) > 0.9975).astype(np.float32)
        fl = gaussian_filter(fl, 0.7) * 3
        fc = np.array(hex_rgb(fleck), np.float32)
        rgb = rgb * (1 - np.clip(fl, 0, 1)[..., None]) + fc * np.clip(fl, 0, 1)[..., None]
    # a faint lighter bevel where the blade cut (top-left) and darker on the far side
    gy, gx = np.gradient(gaussian_filter(m, 1.2))
    bev = np.clip(-(gx + gy) * 2.2, -1, 1)
    rgb = rgb * (1 + bev[..., None] * 0.07)
    reg = over(reg, np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1))
    out[y0:y1, x0:x1] = reg
    return out


def leaf_cut(cx, cy, L, Wd, ang, n=18, bend=0.0):
    """Hand-cut leaf outline (pointed both ends, slight S bend)."""
    pts = []
    for i in range(n):
        t = i / n * math.tau
        u = math.cos(t) * 0.5 + 0.5
        x = u * L
        y = math.sin(t) * Wd * math.sin(math.pi * u) ** 0.85 + bend * Wd * math.sin(u * math.pi * 2) * 0.35
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def blob_pts(cx, cy, r, rng, n=9, var=0.22, rot=0.0):
    pts = []
    for i in range(n):
        a = rot + i / n * math.tau
        rr = r * (1 + rng.uniform(-var, var))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def frond_polys(cx, cy, L, Wd, ang, n=7, stem=0.0, curl=0.25):
    """Palm/fern frond as cut paper: a curved midrib with n narrow leaflets per side (list of polygons)."""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)
    polys = []
    rib = [P(u * L, curl * L * u * u * 0.3) for u in np.linspace(0, 1, 20)]
    # midrib as a thin polygon
    left = [P(u * L, curl * L * u * u * 0.3 - (1 - u) * L * 0.012 - 1.5) for u in np.linspace(0, 1, 20)]
    right = [P(u * L, curl * L * u * u * 0.3 + (1 - u) * L * 0.012 + 1.5) for u in np.linspace(1, 0, 20)]
    polys.append(left + right)
    for k in range(n):
        u = 0.18 + k / (n - 1) * 0.78
        bx, by = u * L, curl * L * u * u * 0.3
        size = Wd * (1.15 - u * 0.75)
        for sd in (1, -1):
            a = sd * (1.0 - u * 0.35) + 0.25
            polys.append([P(*q) for q in [(bx + x * math.cos(a) - y * math.sin(a), by + x * math.sin(a) + y * math.cos(a)) for x, y in leaf_cut(0, 0, size * 1.9, size * 0.32, 0, 14, 0.3)]])
    return polys


def wheel(art, W, H, x, y, r, nx, tyre="#2b2b30", hub="#d9d4c8", hub2="#bdb6a6", bolt="#7a746a"):
    """Chunky toy wheel: gouache tyre with tread hint, painted hub and bolts."""
    t = circles(W, H, [(x, y, r)])
    art = body_paint(art, t, tyre, "#35353b", "#141418", "#5a5a64", nx, ldir=(r * .15, r * .18), blur=max(4, r * .3), light_amt=0.35)
    tread = strokes(W, H, [([(x + math.cos(a) * r * .86, y + math.sin(a) * r * .86), (x + math.cos(a) * r * .98, y + math.sin(a) * r * .98)], max(2, r * .09), None) for a in np.linspace(0, math.tau, 14, endpoint=False)])
    art = crayon(art, tread * t, "#4a4a52", seed=nx(), amt=0.7, tooth=0.3)
    hm = circles(W, H, [(x, y, r * .52)])
    art = body_paint(art, hm, hub, hub2, mix(hub2, "#000000", .3), "#ffffff", nx, ldir=(r * .08, r * .1), blur=max(3, r * .15), light_amt=0.4)
    art = GP(art, circles(W, H, [(x + math.cos(a) * r * .3, y + math.sin(a) * r * .3, max(1.6, r * .06)) for a in np.linspace(0, math.tau, 5, endpoint=False)]), bolt, seed=nx(), rough=0.3, pad=6)
    art = GP(art, circles(W, H, [(x, y, r * .13)]), bolt, seed=nx(), rough=0.3, pad=6)
    return art


def contour(fn, x0, x1, n=60):
    return [(x, fn(x)) for x in np.linspace(x0, x1, n)]


def mist(art, W, H, items, col="#ffffff", seed=1):
    """Soft horizontal mist bands: items = (cx, cy, rx, ry, alpha)."""
    for i, (cx, cy, rx, ry, a) in enumerate(items):
        m = gaussian_filter(ellipses(W, H, [(cx, cy, rx, ry, 0)]), ry * 0.6)
        m = m * (0.7 + 0.6 * fbm(W, H, seed + i, 70, 3))
        art = OV(art, m, lambda mm, a=a: col_arr(mm, col, np.clip(mm * a, 0, 1)), pad=4)
    return art
