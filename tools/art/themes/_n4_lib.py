"""Agent N4 helpers (tenun-troso, malam-gurun, porselen-ming, pelantikan-pengurus): weft-ikat cloth renderer,
handspun weave relief, frayed edges, glaze crackle, cobalt brush wash, star field. Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses, hills, palm, spiral_pts, along ...). Previews -> /tmp/pen/nb-N4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-N4/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art
PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None] * np.ones(rgb.shape[:2] + (1,), np.float32)], -1).astype(np.float32)


def flat(mask, col, k=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask * k)


def dilate(mask, r):
    return np.clip(gaussian_filter(mask, r) * 3.0, 0, 1) if r > 0 else mask


# ---------------------------------------------------------------- cloth
def handspun(w, h, seed, tone="#e6dcc4", warp=3.2, weft=3.0, slub=0.9, dark="#8d7b5f"):
    """Plain weave relief: uneven threads, slubs, tone drift; seamless."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nw = int(round(w / warp)); nf = int(round(h / weft))
    tw = rng.normal(0, 1, nw); tf = rng.normal(0, 1, nf)
    cw = np.floor(xx / w * nw).astype(int) % nw; cf = np.floor(yy / h * nf).astype(int) % nf
    phx = (xx / w * nw) % 1.0; phy = (yy / h * nf) % 1.0
    over_ = ((cw + cf) % 2 == 0)
    ridge_w = np.clip(np.cos((phx - 0.5) * math.pi), 0, 1) ** 1.2
    ridge_f = np.clip(np.cos((phy - 0.5) * math.pi), 0, 1) ** 1.2
    ridge = np.where(over_, ridge_w * (0.75 + 0.25 * ridge_f), ridge_f * (0.75 + 0.25 * ridge_w))
    tone_t = np.where(over_, tw[cw], tf[cf]) * 0.05
    s = wrap_noise(w, h, seed + 3, (0.8, 6)) - 0.5
    s2 = wrap_noise(w, h, seed + 4, (6, 0.8)) - 0.5
    big = wrap_noise(w, h, seed + 5, 30) - 0.5
    v = 0.80 + 0.26 * ridge + tone_t + (s + s2) * 0.18 * slub + big * 0.08
    gap = (1 - ridge_w * ridge_f) ** 6
    base = col3(tone)[None, None, :] * v[..., None]
    base = base * (1 - gap[..., None] * 0.35) + col3(dark) * gap[..., None] * 0.35
    return np.clip(base, 0, 1).astype(np.float32)


def weave_shade(h, w, seed, warp=3.2, weft=3.0, amt=1.0):
    t = handspun(w, h, seed, "#ffffff", warp, weft, dark="#777777")
    lum = t.mean(-1)
    return (1 + (lum / lum.mean() - 1) * amt).astype(np.float32)


def ikat_render(idx, palette, seed, weft=3, shift=3.0, blur=1.4, bundle=4, wrap=True, drift=0.06, warp=3.2):
    """Weft-ikat cloth from a colour-index map (H, W ints into palette list of hex).
    Each weft pass is shifted sideways by a random amount (tie-dye misregistration) and softened along the weft, so
    motif edges get the typical feathered, stepped 'ikat blur'; then thread relief + dye drift."""
    H, W = idx.shape
    rng = np.random.default_rng(seed)
    pal = np.stack([col3(c) for c in palette])
    rgb = pal[idx]
    # bundle stepping is done by the caller's quantised geometry; here: per-pass shift
    out = np.empty_like(rgb)
    passes = int(math.ceil(H / weft))
    offs = gaussian_filter(rng.normal(0, 1, passes), 1.2, mode="wrap" if wrap else "nearest")
    offs = offs / (offs.std() + 1e-6) * shift + rng.normal(0, shift * 0.35, passes)
    for p in range(passes):
        y0, y1 = p * weft, min(H, (p + 1) * weft)
        o = int(round(offs[p]))
        out[y0:y1] = np.roll(rgb[y0:y1], o, axis=1)
    # dye wicks along the weft: anisotropic blur
    out = gaussian_filter(out, (0.4, blur, 0), mode="wrap" if wrap else "nearest")
    # occasional streaks where dye crept (bleed spots)
    n = wrap_noise(W, H, seed + 7, (0.6, 14)) if wrap else fbm(W, H, seed + 7, 20, 2)
    out = out * (1 - drift + drift * 2 * n[..., None])
    out = out * weave_shade(H, W, seed + 9, warp, weft, 1.0)[..., None]
    big = wrap_noise(W, H, seed + 11, 40) if wrap else fbm(W, H, seed + 11, 120, 3)
    out = out * (0.94 + 0.1 * big[..., None])
    return np.clip(out, 0, 1).astype(np.float32)


def fray(mask, seed, amount=5.0, fibres=0.6):
    h, w = mask.shape
    n = fbm(w, h, seed, 6, 2)
    soft = gaussian_filter(mask, amount * 0.6)
    m = np.clip((soft - 0.35 - (n - 0.5) * 0.5) * 6, 0, 1)
    rng = random.Random(seed)
    edge = np.argwhere((soft > 0.2) & (soft < 0.5))
    items = []
    for _ in range(int(len(edge) * 0.004 * fibres)):
        y, x = edge[rng.randrange(len(edge))]
        a = rng.uniform(0, math.tau); L = rng.uniform(4, 12)
        items.append(([(x, y), (x + math.cos(a) * L * 0.5 + rng.gauss(0, 1), y + math.sin(a) * L * 0.5 + rng.gauss(0, 1)), (x + math.cos(a) * L, y + math.sin(a) * L)], 0.9, (0.0, 0.6)))
    if items:
        m = np.maximum(m, strokes(w, h, items) * 0.85)
    return m


# ---------------------------------------------------------------- porcelain
def crackle(w, h, seed, cell=46, wrap=True):
    """Glaze crackle network (0..1 lines), seamless when wrap: jittered Voronoi edges at two scales."""
    out = np.zeros((h, w), np.float32)
    for k, (c, amt) in enumerate([(cell, 1.0), (cell * 0.45, 0.55)]):
        rng = np.random.default_rng(seed + k)
        nx_, ny_ = max(2, int(w / c)), max(2, int(h / c))
        pts = []
        for i in range(nx_):
            for j in range(ny_):
                pts.append(((i + rng.random()) * w / nx_, (j + rng.random()) * h / ny_))
        pts = np.array(pts, np.float32)
        if wrap:
            pts = np.concatenate([pts + [dx, dy] for dx in (-w, 0, w) for dy in (-h, 0, h)])
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        # warp coordinates a bit so edges are not straight
        wx = (wrap_noise(w, h, seed + 30 + k, 8) - 0.5) * c * 0.25
        wy = (wrap_noise(w, h, seed + 40 + k, 8) - 0.5) * c * 0.25
        X = xx + wx; Y = yy + wy
        d1 = np.full((h, w), 1e9, np.float32); d2 = np.full((h, w), 1e9, np.float32)
        for px, py in pts:
            d = (X - px) ** 2 + (Y - py) ** 2
            m = d < d1
            d2 = np.where(m, d1, np.minimum(d2, d))
            d1 = np.where(m, d, d1)
        e = np.sqrt(d2) - np.sqrt(d1)
        line = np.clip(1 - e / 1.1, 0, 1) * amt
        out = np.maximum(out, line * (0.5 + 0.5 * wrap_noise(w, h, seed + 50 + k, 6)))
    return out


def cobalt(mask, seed, dark="#1d3a8a", light="#5a78c0", density=0.9, rough=1.2, heap=0.5, feather=0.8):
    """Cobalt underglaze brushwork: watery wash with darker 'heaped and piled' speckles where the cobalt pooled,
    softened by the glaze on top (slight blur, blue bleed halo)."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 14)
    m = gaussian_filter(m, feather)
    halo = np.clip(gaussian_filter(m, 2.2) - m, 0, 1) * 0.35
    low = fbm(w, h, seed + 2, 40, 3)
    a = np.clip(m * density * (0.75 + 0.35 * low), 0, 1)
    rim = np.clip(m - gaussian_filter(m, 3.0), 0, 1) * 1.2
    a = np.clip(a + rim * 0.5 + halo, 0, 1)
    sp = fbm(w, h, seed + 5, 3, 2)
    heapm = np.clip((sp - 0.62) * 4, 0, 1) * m * heap
    t = np.clip(low * 0.6 + heapm, 0, 1)[..., None]
    rgb = col3(light) * (1 - t) + col3(dark) * t
    rgb = rgb * (1 - heapm[..., None] * 0.45)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a + heapm * 0.3, 0, 1)[..., None]], -1).astype(np.float32)


def CB(dst, mask, *a, pad=14, **k):
    import _j1_lib
    return _j1_lib._apply(dst, mask, lambda m: cobalt(m, *a, **k), "over", pad)


# ---------------------------------------------------------------- night
def star_field(W, H, seed, n=500, ymax=1.0, big=12, col="#f6eed6"):
    """Painted stars: tiny dabs of varying size/brightness, a few larger soft-glow stars (no lens-flare sparkles)."""
    rng = random.Random(seed)
    small = []
    for _ in range(n):
        y = (rng.random() ** 1.4) * H * ymax
        small.append((rng.uniform(0, W), y, rng.choice([0.6, 0.7, 0.8, 0.9, 1.1, 1.3])))
    m = circles(W, H, small)
    m *= (0.45 + 0.55 * fbm(W, H, seed + 1, 3, 1))
    bigs = [(rng.uniform(0, W), (rng.random() ** 1.2) * H * ymax * 0.9, rng.uniform(1.6, 2.4)) for _ in range(big)]
    bm = circles(W, H, bigs)
    return m, bm, bigs


def apply_alpha(art, layer):
    return over(art, layer)
