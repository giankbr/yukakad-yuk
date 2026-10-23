"""Agent H2 helpers (kotagede-perak, timor-tais, ukir-jepara, ultah-peri): _j1_lib (bbox-local painting) plus
metal-wire filigree shading, carved-relief shading from a height map, woven thread texture. Previews -> /tmp/pen/nb-H2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
from _jw_lib import along, spiral_pts, lung, hills, palm  # noqa
import _p1_lib
import art as _art
PREV = "/tmp/pen/nb-H2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def ramp(t, stops):
    """Map t (HxW 0..1) through colour stops [(t, hex)] -> HxWx3."""
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        k = np.clip((t - t0) / max(1e-6, t1 - t0), 0, 1)[..., None]
        sel = ((t >= t0) & (t <= t1))[..., None]
        col = np.array(hex_rgb(c0), np.float32) * (1 - k) + np.array(hex_rgb(c1), np.float32) * k
        out = np.where(sel, col, out)
    return out


def normals(height, strength=6.0):
    gy, gx = np.gradient(height)
    nx_, ny_ = -gx * strength, -gy * strength
    nz = np.ones_like(height)
    L = np.sqrt(nx_ ** 2 + ny_ ** 2 + nz ** 2)
    return nx_ / L, ny_ / L, nz / L


def shade(height, light=(-0.55, -0.65, 0.55), strength=6.0):
    lx, ly, lz = light
    ll = math.sqrt(lx * lx + ly * ly + lz * lz); lx, ly, lz = lx / ll, ly / ll, lz / ll
    nx_, ny_, nz = normals(height, strength)
    d = nx_ * lx + ny_ * ly + nz * lz
    # specular (Blinn, viewer straight on)
    hx, hy, hz = lx, ly, lz + 1
    hl = math.sqrt(hx * hx + hy * hy + hz * hz)
    spec = np.clip(nx_ * hx / hl + ny_ * hy / hl + nz * hz / hl, 0, 1)
    return np.clip(d, 0, 1), spec


def silver(mask, seed=1, tarnish=0.35, round_=1.6, strength=7.0, warm=0.0):
    """Hand-made silver wire: rounded wire shading, specular glints, soft environment bands, patchy grey tarnish."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.45), 0, 1)
    height = gaussian_filter(m, round_)
    d, spec = shade(height, strength=strength)
    env = fbm(w, h, seed, 60, 3)
    t = 0.18 + 0.55 * d + 0.22 * (env - 0.5) + 0.5 * spec ** 18
    tn = np.clip((fbm(w, h, seed + 4, 26, 3) - (1 - tarnish)) * 2.6, 0, 1)
    crev = np.clip(gaussian_filter(m, 3.0) - height * 0.9, 0, 1) * 1.6
    t = t * (1 - 0.45 * tn) - crev * 0.25
    rgb = ramp(t, [(0, "#1f2628"), (0.3, "#56615f"), (0.58, "#9ea8a7"), (0.82, "#dfe4e2"), (1.0, "#ffffff")])
    if warm:
        rgb = rgb * (1 - warm * tn[..., None]) + np.array(hex_rgb("#7a6a52"), np.float32) * warm * tn[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def SV(dst, mask, pad=12, **k):
    return OV(dst, mask, lambda q: silver(q, **k), pad=pad)


def drop(dst, mask, col="#1d2a2b", blur=3.0, dx=2, dy=3, strength=0.45):
    """Soft cast shadow of an object placed under it (call before painting the object)."""
    return over(dst, soft_shadow(mask, col, blur, strength, dx, dy))


def coil(cx, cy, r, turns=2.6, a0=0.0, n=None, d=1):
    """Flat-wire coil (filigree spiral) points."""
    n = n or max(24, int(r * turns * 2.2))
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * r * (1 - t * 0.92), cy + math.sin(a0 + d * t * turns * math.tau) * r * (1 - t * 0.92)) for t in [i / (n - 1) for i in range(n)]]


def oval_pts(cx, cy, a, b, n=180, a0=0.0):
    return [(cx + math.cos(a0 + i / n * math.tau) * a, cy + math.sin(a0 + i / n * math.tau) * b) for i in range(n + 1)]


def teardrop(cx, cy, L, W, ang, n=28):
    """Closed teardrop outline (tip along ang)."""
    return petal_pts(cx, cy, L, W, ang, n=n) + [petal_pts(cx, cy, L, W, ang, n=n)[0]]


def wood_grain(w, h, seed, angle=0.0, scale=1.0):
    """Stretched-noise wood grain field 0..1."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = fbm(w, h, seed, 90 * scale, 3)
    u = (xx * math.cos(angle) + yy * math.sin(angle)) * 0.0
    v = (-xx * math.sin(angle) + yy * math.cos(angle))
    rings = np.sin((v * 0.18 / scale + n * 14 + u)) * 0.5 + 0.5
    fine = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.4, 6) if abs(math.sin(angle)) < 0.7 else (6, 0.4))
    fine = (fine - fine.min()) / (fine.max() - fine.min() + 1e-6)
    return np.clip(rings * 0.65 + fine * 0.35, 0, 1)


def teak(height, seed, grain_angle=0.0, light=(-0.6, -0.7, 0.5), strength=5.0, stops=None, ao=0.5, gscale=1.0):
    """Carved teak relief: lambert from a height map + ambient occlusion in recesses + grain."""
    h, w = height.shape
    d, spec = shade(height, light, strength)
    occl = np.clip(gaussian_filter(height, 8) - height, 0, 1)
    g = wood_grain(w, h, seed, grain_angle, gscale)
    t = 0.04 + 0.66 * d + 0.12 * (g - 0.5) + 0.2 * spec ** 10 - ao * occl * 2.6 + 0.3 * np.clip(height, 0, 1.2)
    stops = stops or [(0, "#1f0e05"), (0.3, "#5a2f12"), (0.55, "#94562a"), (0.78, "#c88c4f"), (1.0, "#f0c58a")]
    return np.clip(ramp(t, stops), 0, 1)


def serrated_leaf(cx, cy, L, Wd, ang, lobes=4, depth=0.35, curl=0.0, n=8):
    """Acanthus-like carved leaf: lobed/serrated outline (closed polygon); curl bends the tip sideways."""
    ca, sa = math.cos(ang), math.sin(ang)
    left, right = [], []
    N = lobes * n
    for i in range(N + 1):
        t = i / N
        base = math.sin(math.pi * t ** 0.8) * Wd * (1 - 0.15 * t)
        lob = 1 - depth * (0.5 + 0.5 * math.cos((t * lobes) * math.tau))
        wv = base * lob
        u = t * L
        bend = curl * L * t ** 2
        for side, out in ((1, left), (-1, right)):
            v = side * wv + bend
            out.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return left + right[::-1]


def leaf_vein(cx, cy, L, ang, curl=0.0, n=12):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for i in range(n):
        t = i / (n - 1) * 0.86
        u = t * L; v = curl * L * t ** 2
        pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return pts


def relief_rgba(height, alpha, seed, stops=None, light=(-0.6, -0.75, 0.55), strength=5.0, cast=(5, 7), cast_amt=0.55, grain_angle=1.5708, spot=None, gscale=1.0):
    """Shade a carved height map as teak; cast shadow of raised parts onto lower ones; optional spotlight falloff."""
    h, w = height.shape
    rgb = teak(height, seed, grain_angle, light, strength, stops, gscale=gscale)
    if cast_amt:
        dx, dy = cast
        sh = np.roll(np.roll(height, dy, 0), dx, 1)
        cs = np.clip((sh - height) * 2.2, 0, 1)
        cs = gaussian_filter(cs, 2.0)
        rgb = rgb * (1 - cast_amt * cs[..., None])
    if spot is not None:
        sx, sy, r, amt = spot
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / r
        rgb = rgb * (1 - amt * np.clip(d, 0, 1.4)[..., None] ** 1.6)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(alpha, 0, 1)[..., None]], -1)


def wrap_grain(w, h, seed, rings=9, warp=3.0):
    """Seamless teak grain tile (vertical grain) 0..1."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1 = wrap_noise(w, h, seed, 24) - 0.5
    n2 = wrap_noise(w, h, seed + 1, (90, 4)) - 0.5
    g = 0.5 + 0.5 * np.sin(xx / w * math.tau * rings + n1 * warp * 6 + n2 * 4)
    fine = wrap_noise(w, h, seed + 2, (6, 0.5))
    return np.clip(g * 0.7 + fine * 0.3, 0, 1)
