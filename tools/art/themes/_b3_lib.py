"""Agent B3 helpers (mashrabiya-kayu, mughal-marmer, oasis-kurma, anyelir-syari): relief shading from distance fields
(turned wood, carved/pierced marble), wood grain, veined marble, polished pietra-dura stones, cast lattice shadow on
plaster, fine ink lines. Built on _j1_lib (bbox-cropped G/GP/LC/FO/OV). Previews -> /tmp/pen/nb-B3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-B3/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
from _j1_lib import trim_cache, bbox
import _a3_lib as _a3
from _a3_lib import star_pts, poly_lines, wob_poly, rgba, noise, smooth01
_p1_lib.PREV = "/tmp/pen/nb-B3/art"
import art as _art
from scipy import ndimage as ndi

PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def C(h):
    return np.array(hex_rgb(h), np.float32)


def lerp3(a, b, t):
    t = t[..., None] if np.ndim(t) else t
    return a * (1 - t) + b * t


def height_of(mask, radius, profile="round"):
    """Height field from a mask's inner distance: round = cylinder/dome profile, flat = bevelled plateau."""
    d = ndi.distance_transform_edt(mask > 0.5).astype(np.float32)
    t = np.clip(d / radius, 0, 1)
    if profile == "round":
        hgt = np.sqrt(1 - (1 - t) ** 2)
    else:
        hgt = smooth01(t)
    hgt = gaussian_filter(hgt, 0.8) * radius
    return hgt


def shade(hgt, light=(-0.55, -0.8), depth=1.0):
    """Lambert-ish shading in 0..1 (0.5 = flat) from a height field."""
    gy, gx = np.gradient(hgt)
    lx, ly = light
    nz = 1.0 / depth
    n = np.sqrt(gx * gx + gy * gy + nz * nz)
    lz = 0.9
    ll = math.sqrt(lx * lx + ly * ly + lz * lz)
    lam = (-gx * lx - gy * ly + nz * lz) / (n * ll)
    return np.clip(lam, 0, 1)


def spec(hgt, light=(-0.55, -0.8), power=18, depth=1.0):
    gy, gx = np.gradient(hgt)
    lx, ly = light
    nz = 1.0 / depth
    n = np.sqrt(gx * gx + gy * gy + nz * nz)
    hx, hy, hz = lx * 0.5, ly * 0.5, 1.0
    hl = math.sqrt(hx * hx + hy * hy + hz * hz)
    d = np.clip((-gx * hx - gy * hy + nz * hz) / (n * hl), 0, 1)
    return d ** power


def wood_grain(w, h, seed, along="x", scale=1.0):
    """0..1 grain field: long fibres + growth-ring waves (direction along x or y)."""
    rng = np.random.default_rng(seed)
    if along == "x":
        f = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.7 * scale, 14 * scale))
    else:
        f = gaussian_filter(rng.random((h, w)).astype(np.float32), (14 * scale, 0.7 * scale))
    f = (f - f.min()) / (f.max() - f.min() + 1e-6)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    warp = fbm(w, h, seed + 3, 60 * scale, 3)
    u = (yy if along == "x" else xx) / (5.5 * scale) + warp * 7
    rings = 0.5 + 0.5 * np.sin(u)
    return np.clip(0.55 * f + 0.45 * rings, 0, 1)


def wood(mask, hgt, light_c="#d9a15c", mid="#9a5f2e", dark="#4a2a15", seed=1, along="x", lightdir=(-0.55, -0.8),
         depth=1.2, gloss=0.18, ao_mask=None):
    """Carved / turned wood: relief shading x grain, warm oiled sheen."""
    h, w = mask.shape
    sh = shade(hgt, lightdir, depth)
    g = wood_grain(w, h, seed, along)
    tone = np.clip(sh * 0.86 - 0.04 + (g - 0.5) * 0.26, 0, 1)
    if ao_mask is not None:
        tone = tone * (1 - 0.35 * np.clip(gaussian_filter(ao_mask, 3) - 0.35, 0, 1))
    rgb = np.where(tone[..., None] > 0.5,
                   lerp3(C(mid), C(light_c), (tone - 0.5) * 2),
                   lerp3(C(dark), C(mid), tone * 2))
    rgb = rgb + spec(hgt, lightdir, 22, depth)[..., None] * gloss * C("#ffe2b0")
    # paint texture
    s = gaussian_filter(np.random.default_rng(seed + 9).random((h, w)).astype(np.float32), 0.6)
    rgb = rgb * (0.96 + 0.08 * s[..., None])
    a = np.clip(gaussian_filter(mask, 0.6), 0, 1)
    return rgba(rgb, a)


def marble_field(w, h, seed, scale=1.0, angle=0.6, turb=5.0, wrap=False):
    """Vein intensity (0..1) and cloud of white marble: ridged turbulence -> soft haze + crisp branching cores whose
    strength drifts in and out along their length."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1 = fbm(w, h, seed, 170 * scale, 5)
    n2 = fbm(w, h, seed + 1, 60 * scale, 4)
    n3 = fbm(w, h, seed + 2, 300 * scale, 2)
    u = (xx * math.cos(angle) + yy * math.sin(angle)) / (260 * scale)
    ph = u + n1 * turb * 0.55 + n2 * 0.6
    ridge = 1 - np.abs(np.sin(ph * math.pi))
    core = ridge ** 60
    haze = ridge ** 9
    ph2 = u * 2.3 + n2 * turb * 0.5 + n1 * 1.5
    ridge2 = 1 - np.abs(np.sin(ph2 * math.pi))
    branch = ridge2 ** 90 * np.clip((n3 - 0.45) * 3, 0, 1)
    strength = np.clip((fbm(w, h, seed + 4, 110 * scale, 3) - 0.3) * 1.8, 0, 1)
    vein = np.clip((core * 0.75 + haze * 0.3) * strength + branch * 0.55, 0, 1)
    cloud = (n3 - 0.5) * 0.6 + (n2 - 0.5) * 0.2
    return vein, cloud


def marble(w, h, seed=1, base="#f6f1e7", vein="#9c9a97", warm="#e9dcc6", scale=1.0, angle=0.6, wrap=False, veins=1.0):
    v, cloud = marble_field(w, h, seed, scale, angle)
    rgb = lerp3(C(base), C(warm), np.clip(0.4 + cloud, 0, 1) * 0.55)
    rgb = lerp3(rgb, C(vein), gaussian_filter(v, 0.6) * 0.6 * veins)
    g = gaussian_filter(np.random.default_rng(seed + 4).random((h, w)).astype(np.float32), 0.6)
    rgb = rgb * (0.99 + 0.02 * g[..., None])
    return rgba(rgb, np.ones((h, w), np.float32))


STONES = {
    "carnelian": ("#c4532f", "#8e2a17", "#e8875a"),
    "coral": ("#d9775a", "#a8442e", "#f0a68a"),
    "lapis": ("#2b4f9a", "#172d66", "#4f75c2"),
    "jade": ("#4c8b62", "#25573a", "#86b98f"),
    "malachite": ("#2f7a57", "#17432f", "#5fae86"),
    "onyx": ("#2a2420", "#100d0b", "#4a4038"),
    "amber": ("#d39a3c", "#9a6418", "#f0c575"),
    "turquoise": ("#4aa3a0", "#257270", "#86cdc5"),
    "mauve": ("#a77a95", "#6f4a62", "#cfaac0"),
}


def stone(mask, kind, seed=1, light=(-0.5, -0.8), polish=0.5):
    """Polished inlay stone set flush into marble: banded/mottled body, thin dark joint, polish glint."""
    base, deep, hi = STONES[kind]
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    n1 = fbm(w, h, seed, 26, 3); n2 = fbm(w, h, seed + 2, 9, 2)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if kind in ("malachite", "carnelian", "amber", "onyx"):
        band = 0.5 + 0.5 * np.sin((xx * 0.7 + yy * 0.4) / 5.0 + n1 * 9)
    else:
        band = n1
    t = np.clip(0.5 + (band * 0.7 + n2 * 0.3 - 0.5) * 0.75, 0, 1)
    rgb = np.where(t[..., None] > 0.5, lerp3(C(base), C(hi), (t - 0.5) * 1.6), lerp3(C(deep), C(base), t * 2))
    if kind == "lapis":
        fl = (np.random.default_rng(seed + 7).random((h, w)) > 0.992).astype(np.float32)
        fl = gaussian_filter(fl, 0.5) * 4
        rgb = lerp3(rgb, C("#e1c27a"), np.clip(fl, 0, 1))
        wv = np.clip((fbm(w, h, seed + 5, 14, 2) - 0.7) * 3, 0, 1)
        rgb = lerp3(rgb, C("#9fb0cf"), wv * 0.35)
    # dark joint at the edge (stone is cut and set) + slightly darker toward edges
    d = ndi.distance_transform_edt(mask > 0.5).astype(np.float32)
    rim = np.clip(1 - d / 1.6, 0, 1) * (mask > 0.5)
    rgb = rgb * (0.86 + 0.14 * np.clip(d / 5, 0, 1))[..., None]
    rgb = lerp3(rgb, C("#2a1f18"), rim * 0.65)
    # polish: soft broad glint across the slab, directional
    gl = np.clip(0.5 + 0.5 * np.sin((xx * 0.5 - yy * 0.85) / 16 + n1 * 2), 0, 1) ** 6
    rgb = rgb + (gl * polish * 0.35)[..., None] * C("#ffffff")
    return rgba(rgb, m)


def ST(dst, mask, kind, seed=1, pad=6, **k):
    return OV(dst, mask, lambda m: stone(m, kind, seed, **k), pad=pad)


def ink(mask, col="#3b2a33", seed=1, alpha=0.92, dry=0.25):
    """Fine dip-pen ink: slightly uneven density, tiny dry breaks."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.45), 0, 1)
    d = fbm(w, h, seed, 7, 2)
    a = m * alpha * (1 - dry * np.clip((d - 0.66) * 4, 0, 1))
    rgb = np.ones((h, w, 3), np.float32) * C(col) * (0.92 + 0.12 * fbm(w, h, seed + 3, 40, 2))[..., None]
    return rgba(rgb, a)


def IK(dst, mask, *a, pad=6, **k):
    return OV(dst, mask, lambda m: ink(m, *a, **k), pad=pad)


def lines_mask(W, H, polylines, width, taper=(0.12, 0.2)):
    return strokes(W, H, [(p, width, taper) for p in polylines])


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1)
        a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t * t; d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def rgb_save(arr, path, quality=80, size=None):
    return save_rgb(arr, path, size=size, quality=quality)


def report(out):
    tot = 0
    for f in sorted(os.listdir(out)):
        k = os.path.getsize(os.path.join(out, f)); tot += k
        print(f"  {f:22s} {k // 1024:4d} KB")
    print(f"  total {tot // 1024} KB")
