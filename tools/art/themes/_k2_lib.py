"""Agent J2 (batch 10) helpers for asmat-ukir, banda-neira, dahlia-syari, ultah-kereta.
Wraps the shared _jw_lib (-> _j1_lib, _p1_lib, art) and adds small geometry/medium helpers.
Previews -> /tmp/pen/nb-J2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-J2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def show(arr, name, tone="#f7efe2", bg=None):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def polys(W, H, items):
    return shapes(W, H, items, smooth=False)


def tint(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def edge_of(mask, px=2.0):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def fade_alpha(arr, y0, y1, top=True):
    h = arr.shape[0]
    yy = np.arange(h, dtype=np.float32)[:, None]
    k = np.clip((yy - y0) / max(1, (y1 - y0)), 0, 1)
    if not top:
        k = 1 - k
    out = arr.copy()
    out[..., 3] *= (k * k * (3 - 2 * k))
    return out


def grid(W, H):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return yy, xx


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def wood(mask, col, col2, seed=1, vertical=True, rough=1.5, grain=1.0):
    """Opaque wood: gouache with long grain streaks (vertical or horizontal) and darker figure lines."""
    m = mask.T.copy() if vertical else mask
    h, w = m.shape
    g = gouache_paint(m, col, col2, seed=seed, rough=rough, streak=2.2 * grain)
    fig = gaussian_filter(np.random.default_rng(seed + 4).random((h, w)).astype(np.float32), (0.8, 30))
    fig = (fig - fig.mean()) / (fig.std() + 1e-6)
    lines = np.clip((fig - 1.2) * 0.9, 0, 1) * 0.35 * grain
    g[..., :3] *= (1 - lines[..., None])
    if vertical:
        g = np.ascontiguousarray(g.transpose(1, 0, 2))
    return g


def WD(dst, mask, *a, pad=8, **k):
    """over: wood locally."""
    from _j1_lib import _apply
    return _apply(dst, mask, lambda m: wood(m, *a, **k), "over", pad)


def relief(art, W, H, m, light, dark, nx, depth=2, hi_alpha=0.5, lo_alpha=0.65, hi_col="#fff3dc"):
    """Give a painted raised shape a carved edge: highlight up-left, shadow down-right."""
    hi = np.clip(m - np.roll(np.roll(m, depth, 0), depth, 1), 0, 1)
    lo = np.clip(m - np.roll(np.roll(m, -depth, 0), -depth, 1), 0, 1)
    art = OV(art, lo * lo_alpha, lambda q: tint(q, dark, 1.0), pad=4)
    art = OV(art, hi * hi_alpha, lambda q: tint(q, hi_col, 1.0), pad=4)
    return art


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------- dahlia (watercolour)
def _sq(pts, cx, cy, tilt, rot):
    c, s_ = math.cos(rot), math.sin(rot)
    out = []
    for x, y in pts:
        dx, dy = x - cx, (y - cy) * tilt
        out.append((cx + dx * c - dy * s_, cy + dx * s_ + dy * c))
    return out


def spoon_pts(bx, by, L, wd, a, n=10):
    """Dahlia ray petal: narrow base widening to a rounded tip (half-width wd at the tip)."""
    hw = wd * 0.5
    x1 = max(L * 0.3, L - hw)
    right = [(x1 * t, hw * (0.28 + 0.72 * t ** 0.8)) for t in [i / n for i in range(n + 1)]]
    tip = [(x1 + math.cos(th) * hw, math.sin(th) * hw) for th in [math.pi / 2 - math.pi * i / n for i in range(1, n)]]
    left = [(x, -y) for x, y in right[::-1]]
    ca, sa = math.cos(a), math.sin(a)
    return [(bx + x * ca - y * sa, by + x * sa + y * ca) for x, y in right + tip + left]


def dahlia(art, W, H, cx, cy, R, rng, nx, light, mid, deep, centre=None, tilt=1.0, rot=0.0, rings=6, area=None, open_=1.0):
    """Decorative dahlia: concentric rings of cupped petals, washed ring by ring (outer pale -> inner deep) so every
    petal keeps a wet edge; a tight incurved centre. tilt < 1 squashes it into a three-quarter view."""
    centre = centre or deep
    union = np.zeros((H, W), np.float32)
    for k in range(rings):
        t = k / max(1, rings - 1)
        f = (1 - t * 0.82) * open_ + (1 - open_) * (1 - t) * 0.6
        n = max(7, int(19 - k * 2))
        L = R * f * 0.64
        wd = L * (0.5 - 0.06 * t)
        a0 = rng.uniform(0, math.tau) if k == 0 else a0 + math.pi / n
        col_a = mix(light, mid, min(1, t * 1.25))
        col_b = mix(mid, deep, max(0, t * 1.2 - 0.2))
        for parity in (0, 1):
            polys_ = []
            for i in range(n):
                if i % 2 != parity:
                    continue
                a = a0 + i / n * math.tau + rng.uniform(-0.06, 0.06)
                bx, by = cx + math.cos(a) * R * f * 0.30, cy + math.sin(a) * R * f * 0.30
                p = spoon_pts(bx, by, L * rng.uniform(0.9, 1.08), wd * rng.uniform(0.95, 1.15), a)
                polys_.append(_sq(p, cx, cy, tilt, rot))
            m = shapes(W, H, polys_)
            if area is not None:
                m = m * area
            union = np.maximum(union, m)
            if k or parity:
                art = knockout(art, m, amount=0.8, grow=0.8)
            art = G(art, m, col_a, col_b, seed=nx(), density=0.8 + 0.15 * t, edge=0.8, bloom=0.3, gran=0.2, rough=1.4, feather=0.8, pad=10)
        lift = []
        for i in range(n):
            a = a0 + i / n * math.tau
            p0 = (cx + math.cos(a) * R * f * 0.62, cy + math.sin(a) * R * f * 0.62)
            p1 = (cx + math.cos(a) * R * f * 0.86, cy + math.sin(a) * R * f * 0.86)
            lift.append((_sq([p0, p1], cx, cy, tilt, rot), max(1.5, R * f * 0.07), (0.3, 0.3)))
        lm_ = gaussian_filter(strokes(W, H, lift), 1.2) * (area if area is not None else 1)
        art = OV(art, lm_ * 0.35, lambda q: tint(q, mix(light, "#ffffff", 0.5), 1.0), pad=6)
        # creases: a short darker stroke at each petal base
        cr = []
        for i in range(n):
            a = a0 + i / n * math.tau
            p0 = (cx + math.cos(a) * R * f * 0.32, cy + math.sin(a) * R * f * 0.32)
            p1 = (cx + math.cos(a) * R * f * 0.62, cy + math.sin(a) * R * f * 0.62)
            cr.append((_sq([p0, p1], cx, cy, tilt, rot), max(1.0, R * 0.018), (0.1, 0.8)))
        art = G(art, strokes(W, H, cr) * (area if area is not None else 1), mix(mid, deep, 0.5), seed=nx(), density=0.35, edge=0.1, bloom=0, rough=0.6, feather=0.6, pad=6)
    # incurved centre
    cm = shapes(W, H, [_sq(deform(ellipse_pts(cx, cy, R * 0.15, R * 0.15, 10), rng, 1, 0.05), cx, cy, tilt, rot)])
    art = G(art, cm, mix(mid, centre, 0.5), centre, seed=nx(), density=0.85, edge=0.6, bloom=0.1, rough=1, pad=6)
    curls = []
    for i in range(7):
        a = i / 7 * math.tau + rng.uniform(-0.2, 0.2)
        curls.append((_sq(arc_pts(cx, cy, R * 0.09, a, a + 1.4, 8), cx, cy, tilt, rot), max(1.0, R * 0.022), (0.2, 0.4)))
    art = G(art, strokes(W, H, curls), centre, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.5, feather=0.5, pad=6)
    # form shading: lower-right half deeper
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    disc = shapes(W, H, [_sq(ellipse_pts(cx, cy, R * 0.98, R * 0.98, 16), cx, cy, tilt, rot)])
    sh = union * disc * np.clip(((xx - cx) * 0.6 + (yy - cy) * 0.8) / (R * 1.2) + 0.15, 0, 1)
    art = G(art, sh * (area if area is not None else 1), deep, seed=nx(), density=0.22, edge=0.1, bloom=0.4, rough=3, pad=10)
    return art


def dahlia_leaf(art, W, H, x, y, L, ang, rng, nx, cols=("#9aa678", "#5d6b43", "#3d4a2e")):
    """Dahlia leaf: a long pointed terminal leaflet with two smaller ones at its base, soft wash with a darker half."""
    for da, fl in ((0, 1.0), (-0.85, 0.55), (0.85, 0.55)):
        a = ang + da + rng.uniform(-0.08, 0.08)
        bx, by = x + math.cos(ang) * L * (0.12 if da else 0.0), y + math.sin(ang) * L * (0.12 if da else 0.0)
        pts = deform(petal_pts(bx, by, L * fl, L * fl * 0.27, a, n=28, cup=rng.uniform(-0.25, 0.25)), rng, 1, 0.012)
        m = shape_mask(W, H, pts)
        art = G(art, m, cols[0], cols[1], seed=nx(), density=0.78, edge=0.7, bloom=0.35, rough=1.4, feather=0.8, pad=10)
        half = shape_mask(W, H, [(bx, by)] + pts[: len(pts) // 2])
        art = G(art, half * m, cols[2], seed=nx(), density=0.28, edge=0.2, bloom=0.2, rough=1.2, pad=10)
        vein = strokes(W, H, [([(bx, by), (bx + math.cos(a) * L * fl * 0.85, by + math.sin(a) * L * fl * 0.85)], max(1.0, L * 0.014), (0.0, 0.6))])
        art = G(art, vein, "#dcdab6", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    return art
