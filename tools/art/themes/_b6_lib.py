"""Agent B6 helpers (khataman-quran, tedak-siten, halal-bihalal, purna-tugas): on top of _jw_lib (flora, carving) +
_j1_lib (bbox-cropped G/GP/LC/FO/OV). Previews -> /tmp/pen/nb-B6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
import _p1_lib
import art as _art

_p1_lib.PREV = "/tmp/pen/nb-B6/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)


def clear():
    _art._fbm_cache.clear()


def star8(cx, cy, ro, ri, rot=0.0):
    """8-point star (two overlapping squares outline) as 16 vertices."""
    pts = []
    for k in range(16):
        r = ro if k % 2 == 0 else ri
        a = rot + k * math.pi / 8
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def inner_line(mask, inset, width):
    """Thin line running `inset` px inside a mask edge."""
    a = (gaussian_filter(mask, inset * 0.5) > 0.98).astype(np.float32)
    b = (gaussian_filter(mask, (inset + width) * 0.5) > 0.98).astype(np.float32)
    return np.clip(a - b, 0, 1)


def wood(art, mask, nx, base="#7a4b2a", dark="#4a2a16", light="#a26f43", angle=0.0, spacing=9, seed=3, grain=0.5):
    """Gouache wood: matte base, wavy grain lines, a soft top light and edge darkening."""
    h, w = mask.shape
    art = GP(art, mask, base, dark, seed=nx(), rough=1.2, streak=1.0, pad=10)
    g = jw.hatch(w, h, angle, spacing, 0.12, seed, wob=14) * mask * (0.35 + 0.65 * fbm(w, h, seed + 2, 40, 3))
    art = G(art, g, dark, seed=nx(), density=0.32 * grain + 0.06, edge=0.1, bloom=0, rough=1, feather=0.5)
    hi = np.clip(np.roll(gaussian_filter(mask, 8), 10, 0) - gaussian_filter(mask, 8) * 0.0, 0, 1) * mask * fbm(w, h, seed + 4, 60, 2)
    art = G(art, hi * 0.6, light, seed=nx(), density=0.35, edge=0, bloom=0.2, rough=1)
    edge = np.clip(mask - gaussian_filter(mask, 3) * 1.08, 0, 1) * 2.5
    return G(art, np.clip(edge, 0, 1), dark, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.6)


def flame(W, H, x, y, h, rng, nx, art, glow_col="#ffd27a", core="#fff4cf", outer="#f29a2e"):
    """Small oil-lamp flame with a warm halo; (x, y) is the flame base."""
    halo = circles(W, H, [(x, y - h * 0.45, h * 0.55)])
    art = over(art, glow(halo, glow_col, radius=h * 0.45, strength=0.45))
    o = shapes(W, H, [deform(petal_pts(x, y, h, h * 0.36, -math.pi / 2 + rng.uniform(-.08, .08), n=14), rng, 1, 0.04)])
    art = GP(art, o, outer, "#e5672a", seed=nx(), rough=0.8, streak=0.3, pad=8)
    c = shapes(W, H, [petal_pts(x, y - h * 0.06, h * 0.62, h * 0.2, -math.pi / 2, n=12)])
    art = OV(art, gaussian_filter(c, 1.2), lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(core), np.float32), m[..., None]], -1))
    blue = ellipses(W, H, [(x, y - h * 0.02, h * 0.09, h * 0.06, 0)])
    return G(art, blue, "#6c7fb8", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.5, pad=6)


def shade_side(mask, dx, dy, blur=8, k=1.0):
    """Shadow field on the side of a mask away from the light (offset difference)."""
    g = gaussian_filter(mask, blur)
    return np.clip((g - np.roll(np.roll(g, dy, 0), dx, 1)) * 3 * k, 0, 1) * mask


def tint(m, col, a=1.0):
    rgb = np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(m, 0, 1) * a)[..., None]], -1)


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s_ = os.path.getsize(os.path.join(d, f)); tot += s_
        print(f"  {f:22s} {s_ // 1024:4d} KB")
    print("  total", tot // 1024, "KB")


def weave_layer(mask, cx, cy, ang, strip, light, mid, dark, seed=1, gap=0.08):
    """Janur weave inside mask: two strand sets crossing at 90deg (rotated by ang), over/under checker, each strand
    shaded across its width (rounded leaf), thin dark gaps between strands, fibre streaks along each strand."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ca, sa = math.cos(ang), math.sin(ang)
    u = ((xx - cx) * ca + (yy - cy) * sa) / strip
    v = (-(xx - cx) * sa + (yy - cy) * ca) / strip
    n = (fbm(w, h, seed, 40, 2) - 0.5) * 0.12
    u = u + n; v = v - n
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = u - iu, v - iv
    top_u = ((iu + iv) % 2) == 0          # strand running along v is on top here
    frac = np.where(top_u, fu, fv)        # position across the top strand
    along = np.where(top_u, fv, fu)       # position along the top strand inside the cell
    shade = np.sin(np.pi * np.clip(frac, 0, 1)) ** 0.6
    dip = 0.78 + 0.22 * np.sin(np.pi * np.clip(along, 0, 1))  # strand dives under its neighbour at cell ends
    g = np.clip(np.minimum(frac, 1 - frac) / gap, 0, 1)
    tone = shade * dip * (0.35 + 0.65 * g)
    fib = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.7)
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    cl, cm, cd = (np.array(hex_rgb(c), np.float32) for c in (light, mid, dark))
    t = tone[..., None]
    rgb = np.where(t > 0.5, cm + (cl - cm) * (t - 0.5) * 2, cd + (cm - cd) * t * 2)
    rgb = rgb * (1 + fib[..., None] * 0.04)
    alt = np.where(top_u, 1.0, 0.93)[..., None]  # the two strand directions catch light differently
    return np.concatenate([np.clip(rgb * alt, 0, 1), mask[..., None]], -1)
