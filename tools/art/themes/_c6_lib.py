"""Agent C6 helpers (wisuda-tk, syukuran-kelahiran, ultah-sepuh, natal-keluarga): _a6_lib (bbox-local painting,
crayon lines, soft gouache shading) + wax pastel fills, stitched felt, knitted tile, manila paper, gold-leaf strokes,
warm light bulbs. Previews -> /tmp/pen/nb-C6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _a6_lib import *  # noqa
import _a6_lib, _j1_lib
PREV = "/tmp/pen/nb-C6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_a6_lib.PREV = PREV


def _norm(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-6)


def tooth(shape, seed, sigma=0.65):
    """Paper tooth (0..1): fine bumpy grain that breaks dry media."""
    return _norm(gaussian_filter(np.random.default_rng(seed).random(shape).astype(np.float32), sigma))


# ---------------------------------------------------------------- wax pastel / crayon
def wax(dst, mask, col, col2=None, seed=1, angle=0.7, spacing=3.4, density=0.95, rough=2.4, press=0.55, pad=10):
    """Wax pastel / crayon fill: hand-cut wobbly edge, directional strokes, paper tooth showing through."""
    def fn(m):
        h, w = m.shape
        mm = displace(m, seed, rough, 22)
        mm = np.clip((gaussian_filter(mm, 0.8) - 0.3) * 2.2, 0, 1)
        st = hatch(w, h, angle, spacing, 0.62, seed + 1, wob=2.0)
        st2 = hatch(w, h, angle + 0.25, spacing * 1.7, 0.5, seed + 2, wob=3.0)
        t = tooth((h, w), seed + 3)
        pr = fbm(w, h, seed + 4, 40, 3)
        cov = np.clip(0.42 + 0.38 * st + 0.2 * st2 + (pr - 0.5) * press, 0, 1)
        a = mm * np.clip((t - (1 - cov) * 0.9) * 2.6 + 0.25 * cov, 0, 1) * density
        ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
        k = fbm(w, h, seed + 5, 60, 3)[..., None]
        rgb = ca * (1 - k) + cb * k
        rgb = rgb * (1 - 0.12 * (a[..., None] - 0.5))
        return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)
    return OV(dst, mask, fn, pad=pad)


def scribble_line(dst, pts, width, col, seed=1, amt=0.92, tooth_=0.42, passes=2):
    """Crayon line drawn twice with a slight offset (kid-drawing outline)."""
    h, w = dst.shape[:2]
    rng = random.Random(seed)
    items = []
    for p in range(passes):
        off = [(x + rng.gauss(0, width * 0.25), y + rng.gauss(0, width * 0.25)) for x, y in pts]
        items.append((off, width * rng.uniform(0.8, 1.05), (0.06, 0.1)))
    m = strokes(w, h, items)
    return crayon(dst, m, col, seed=seed + 7, amt=amt, tooth=tooth_)


def contour(mask, px=2.6):
    """Outline band straddling the edge of a mask (for crayon outlines)."""
    g = gaussian_filter(mask, px * 0.6)
    return np.clip(1 - np.abs(g - 0.5) * 2 / 0.55, 0, 1) * (g > 0.05)


# ---------------------------------------------------------------- felt
def felt(dst, mask, col, col2=None, seed=1, stitch="#fbf6e9", stitch_in=7.0, puff=0.22, fuzz=0.5, pad=14, dash=7.0):
    """Wool felt cut-out: fuzzy fibrous edge, matted fibre texture, stuffed (puffy) shading, running stitch inset."""
    def fn(m):
        h, w = m.shape
        mm = displace(m, seed, 1.2, 8)
        rng = np.random.default_rng(seed)
        fib = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.5, 2.2))
        fib2 = gaussian_filter(rng.random((h, w)).astype(np.float32), (2.2, 0.5))
        fz = _norm(fib + fib2)
        halo = np.clip(gaussian_filter(mm, 2.0) * 1.6, 0, 1) * np.clip((fz - 0.55) * 4, 0, 1) * fuzz
        a = np.clip(np.maximum(np.clip((gaussian_filter(mm, 0.9) - 0.3) * 2.4, 0, 1), halo), 0, 1)
        ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
        k = fbm(w, h, seed + 2, 50, 3)[..., None]
        rgb = ca * (1 - k) + cb * k
        tex = _norm(gaussian_filter(rng.random((h, w)).astype(np.float32), 1.0)) - 0.5
        rgb = rgb * (1 + tex[..., None] * 0.14 + (fz[..., None] - 0.5) * 0.14)
        inner = gaussian_filter(mm, 9.0)
        rgb = rgb * (1 - puff * np.clip(1 - inner * 1.25, 0, 1)[..., None])
        hi = np.clip(np.roll(np.roll(gaussian_filter(mm, 10), 7, 0), 6, 1) - 0.0, 0, 1)
        rgb = rgb * (1 + 0.06 * (inner - hi)[..., None] * -1)
        out = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
        if stitch:
            g = gaussian_filter(mm, stitch_in * 0.55)
            line = np.clip(1 - np.abs(g - 0.86) / 0.06, 0, 1) * (mm > 0.5)
            yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
            d1 = (np.sin((xx + yy) / dash * math.pi) > 0.05).astype(np.float32)
            d2 = (np.sin((xx - yy) / dash * math.pi) > 0.05).astype(np.float32)
            sm = gaussian_filter(line * d1 * d2, 0.5) * 1.6
            sm = np.clip(sm, 0, 1)
            shadow = np.roll(np.roll(sm, 1, 0), 1, 1) * 0.35
            out = over(out, col_arr(sm, "#000000", shadow * (1 - sm)))
            out = over(out, col_arr(sm, stitch, sm * 0.95))
        return out
    return OV(dst, mask, fn, pad=pad)


def knit_tile(w, h, col, col2, seed=1, cw=16, ch=14):
    """Seamless stockinette knit (rows of V stitches); w multiple of cw, h multiple of ch."""
    cv = Canvas(w, h)
    rng = random.Random(seed)
    loops = []
    for r in range(h // ch + 1):
        for c in range(w // cw + 1):
            x0, y0 = c * cw, r * ch
            for side in (-1, 1):
                for ox in (0, -w, w):
                    for oy in (0, -h, h):
                        loops.append((x0 + ox + cw / 2 + side * cw * 0.24, y0 + oy + ch * 0.5, cw * 0.26, ch * 0.62, side * 28 + rng.gauss(0, 3)))
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for cx, cy, rx, ry, rot in loops:
        cv.c.save(); cv.c.translate(cx, cy); cv.c.rotate(rot); cv.c.drawOval(skia.Rect(-rx, -ry, rx, ry), p); cv.c.restore()
    m = cv.array()[..., 3]
    # per-loop shading: distance-ish from loop centre via blur
    body = gaussian_filter(m, 1.6, mode="wrap")
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rows = 0.5 + 0.5 * np.cos((yy % ch) / ch * math.tau)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2), np.float32)
    nz = wrap_noise(w, h, seed, 18)[..., None]
    base = ca * (1 - nz * 0.5) + cb * nz * 0.5
    lum = 0.66 + 0.42 * body - 0.08 * rows
    fz = wrap_noise(w, h, seed + 3, 0.6)
    lum = lum * (1 + (fz - 0.5) * 0.12)
    rgb = base[None, None] if base.ndim == 1 else base
    rgb = rgb * lum[..., None]
    gap = (1 - np.clip(m * 1.4, 0, 1))[..., None]
    rgb = rgb * (1 - gap * 0.38)
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)


def wrap_paper(w, h, tone, seed=1, fibre=1.0, mottle=1.0, flecks=0.0, fleck_col="#8a6a3a"):
    """Seamless paper tile (manila / ivory / cream)."""
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    big = wrap_noise(w, h, seed, 30) - 0.5
    fine = wrap_noise(w, h, seed + 1, 0.7) - 0.5
    fib = gaussian_filter(np.random.default_rng(seed + 2).random((h, w)).astype(np.float32), (0.5, 5), mode="wrap")
    fib = _norm(fib) - 0.5
    v = 1 + big * 0.07 * mottle + fine * 0.05 + fib * 0.05 * fibre
    rgb = base * v[..., None]
    if flecks:
        f = (np.random.default_rng(seed + 4).random((h, w)) > 1 - flecks * 0.002).astype(np.float32)
        f = gaussian_filter(f, 0.8, mode="wrap") * 3
        fc = np.array(hex_rgb(fleck_col), np.float32)
        rgb = rgb * (1 - np.clip(f, 0, 0.5)[..., None]) + fc * np.clip(f, 0, 0.5)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)


# ---------------------------------------------------------------- lights / gold
def bulb(dst, x, y, r, col="#ffd88a", core="#fff6dc", halo=1.0, seed=1):
    h, w = dst.shape[:2]
    m = circles(w, h, [(x, y, r)])
    dst = OV(dst, m, lambda mm: col_arr(mm, col, np.clip(gaussian_filter(mm, r * 1.6) * 1.8, 0, 1) * 0.55 * halo), pad=int(r * 5))
    dst = OV(dst, m, lambda mm: col_arr(mm, col, np.clip(gaussian_filter(mm, 0.7), 0, 1)), pad=4)
    c = circles(w, h, [(x - r * 0.2, y - r * 0.25, r * 0.45)])
    return OV(dst, c, lambda mm: col_arr(mm, core, np.clip(gaussian_filter(mm, 0.8), 0, 1)), pad=4)


def gold_leaf(dst, mask, base="#c9a24e", seed=1, crack=0.25):
    """Gold leaf: foil sheen with fine cracks/gaps where the leaf broke (not a flat vector gold)."""
    def fn(m):
        h, w = m.shape
        f = foil(m, base, seed=seed, emboss=0.5, sparkle=0.15)
        cr = fbm(w, h, seed + 9, 9, 2)
        brk = np.clip((np.abs(cr - 0.5) < 0.018).astype(np.float32) * crack * 3, 0, 1)
        f[..., 3] *= 1 - brk * 0.7
        return f
    return OV(dst, mask, fn, pad=8)


def bbox_save(arr, name, path, max_w, quality=82, bg=None, tone="#fbf6e4"):
    preview(arr, name, tone=tone, bg=bg)
    return save(arr, path, max_w=max_w, quality=quality)
