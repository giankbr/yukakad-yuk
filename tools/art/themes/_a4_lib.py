"""Agent A4 helpers (tasbih-mutiara, hijrah-senja, walimatus-safar, perak-kenangan): _jw_lib re-export + pearls,
dunes, lanterns, deckled paper, silver foil. Previews -> /tmp/pen/nb-A4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa  (also brings _j1_lib / _p1_lib / art)
import _jw_lib as jw
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-A4/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(f"{d}/{f}"); tot += s
        print(f"  {f:22s} {s / 1024:6.1f} KB")
    print(f"  total {tot / 1024:.1f} KB")


def rgba(col, a):
    """Solid colour layer with alpha array a."""
    h, w = a.shape
    return np.concatenate([np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32), np.clip(a, 0, 1)[..., None]], -1)


def lerp3(c0, c1, t):
    a = np.array(hex_rgb(c0), np.float32); b = np.array(hex_rgb(c1), np.float32)
    return a * (1 - t[..., None]) + b * t[..., None]


# ---------------------------------------------------------------- pearls
IRIS = ("#eec2cd", "#c3e0cc", "#c6cff0", "#efd8b0")


def pearl(art, cx, cy, r, seed=1, base="#f5f0e7", shade="#8f8a96", iris=IRIS, iris_amt=0.75, light=(-0.55, -0.62), spec=1.0):
    """Paint one pearl in place (local crop): sphere shading, soft iridescent rim, painted specular and reflected light."""
    H, W = art.shape[:2]
    rng = np.random.default_rng(seed)
    pad = int(r * 0.9) + 4
    x0, x1 = max(0, int(cx - r - pad)), min(W, int(cx + r + pad) + 1)
    y0, y1 = max(0, int(cy - r - pad)), min(H, int(cy + r + pad) + 1)
    if x1 <= x0 or y1 <= y0:
        return art
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    # slightly irregular outline (natural pearls are never perfect)
    ang = np.arctan2(yy - cy, xx - cx)
    ph = rng.uniform(0, 6.28, 3)
    rr = r * (1 + 0.025 * np.sin(ang * 2 + ph[0]) + 0.015 * np.sin(ang * 3 + ph[1]))
    d = np.hypot(xx - cx, yy - cy) / rr
    alpha = np.clip((1 - d) * r * 0.9 + 0.5, 0, 1)
    nz = np.sqrt(np.clip(1 - d ** 2, 0, 1))
    nxv = (xx - cx) / rr; nyv = (yy - cy) / rr
    lx, ly = light; lz = math.sqrt(max(0.05, 1 - lx * lx - ly * ly))
    diff = np.clip(nxv * lx + nyv * ly + nz * lz, 0, 1)
    rgb = lerp3(shade, base, np.clip(diff * 1.12, 0, 1) ** 1.1)
    # iridescence: hue drifts with angle, strongest at the rim (fresnel)
    fres = np.clip(1 - nz, 0, 1) ** 1.6
    k = (np.sin(ang * 1.5 + ph[2]) * 0.5 + 0.5)
    ia, ib = iris[int(rng.integers(0, len(iris)))], iris[int(rng.integers(0, len(iris)))]
    tint = lerp3(ia, ib, k)
    rgb = rgb * (1 - fres[..., None] * iris_amt) + tint * fres[..., None] * iris_amt
    # reflected light along the shadow-side rim
    refl = np.clip(-(nxv * lx + nyv * ly), 0, 1) ** 2 * np.clip(d - 0.55, 0, 1) * 2.2
    rgb = rgb + (np.array(hex_rgb(ib), np.float32) - rgb) * (refl[..., None] * 0.55)
    # painted specular: soft wide sheen + small bright dab, slightly smeared
    sx, sy = cx + lx * r * 0.42 + rng.normal(0, r * 0.04), cy + ly * r * 0.42 + rng.normal(0, r * 0.04)
    g1 = np.exp(-(((xx - sx) / (r * 0.42)) ** 2 + ((yy - sy) / (r * 0.30)) ** 2))
    g2 = np.exp(-(((xx - sx) / (r * 0.16)) ** 2 + ((yy - sy) / (r * 0.11)) ** 2))
    g2 = np.exp(-(((xx - sx) / (r * 0.12)) ** 2 + ((yy - sy) / (r * 0.085)) ** 2))
    g3 = np.exp(-(((xx - (cx - lx * r * 0.55)) / (r * 0.22)) ** 2 + ((yy - (cy - ly * r * 0.55)) / (r * 0.12)) ** 2))
    sp = np.clip(g1 * 0.32 + g2 * 1.0 + g3 * 0.22, 0, 1) * spec
    rgb = rgb * (1 - sp[..., None]) + sp[..., None]
    # paint grain
    gr = rng.normal(0, 1, rgb.shape[:2]).astype(np.float32)
    rgb = rgb * (1 + gaussian_filter(gr, 0.7)[..., None] * 0.02)
    src = np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], -1)
    out = art.copy()
    out[y0:y1, x0:x1] = over(art[y0:y1, x0:x1], src)
    return out


def pearl_shadows(art, items, col="#6f6a66", amt=0.32, off=(2, 3)):
    """Soft cast shadows below a set of pearls (x, y, r)."""
    H, W = art.shape[:2]
    m = circles(W, H, [(x + off[0] * r / 8, y + off[1] * r / 8, r * 0.95) for x, y, r in items])
    m = gaussian_filter(m, max(1.5, items[0][2] * 0.35)) * amt
    return over(art, rgba(col, m))


def string_pearls(pts, r, gap=1.02, jitter=0.06, seed=1):
    """Place pearls along a polyline at ~touching spacing. Returns [(x, y, r)]."""
    rng = random.Random(seed)
    out = []
    acc = 0.0; i = 1; px, py = pts[0]
    cur_r = r * (1 + rng.uniform(-jitter, jitter))
    out.append((px, py, cur_r))
    need = cur_r * gap
    while i < len(pts):
        x1, y1 = pts[i]
        dd = math.hypot(x1 - px, y1 - py)
        nr = r * (1 + rng.uniform(-jitter, jitter))
        step = need + nr * gap
        if acc + dd >= step:
            t = (step - acc) / dd
            px, py = px + (x1 - px) * t, py + (y1 - py) * t
            out.append((px, py, nr)); need = nr * gap; acc = 0.0
        else:
            acc += dd; px, py = x1, y1; i += 1
    return out


def draw_pearls(art, items, seed=1, shadow=True, **k):
    if shadow and items:
        art = pearl_shadows(art, items)
    for j, (x, y, r) in enumerate(items):
        art = pearl(art, x, y, r, seed=seed + j * 7, **k)
    return art


def catenary(x0, y0, x1, y1, sag, n=80):
    return [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in [i / (n - 1) for i in range(n)]]


# ---------------------------------------------------------------- deckled paper
def deckle_mask(W, H, inset, seed=1, amp=5.0):
    """Rectangle with a torn/deckled edge: wavy + fibrous."""
    m = np.zeros((H, W), np.float32)
    m[inset:H - inset, inset:W - inset] = 1
    m = displace(m, seed, amp, 9)
    m = displace(m, seed + 3, amp * 0.5, 3)
    return np.clip((gaussian_filter(m, 0.8) - 0.4) * 3, 0, 1)


def silver(mask, base="#c4c8ce", seed=1, emboss=0.6, sparkle=0.15):
    """Silver leaf: cool foil, desaturated sheen."""
    f = foil(mask, base, seed=seed, emboss=emboss, sparkle=sparkle)
    lum = f[..., :3].mean(-1, keepdims=True)
    f[..., :3] = np.clip(f[..., :3] * 0.35 + lum * 0.65 * np.array([0.97, 0.99, 1.04], np.float32), 0, 1)
    return f


def SV(dst, mask, *a, pad=12, **k):
    return OV(dst, mask, lambda m: silver(m, *a, **k), pad=pad)
