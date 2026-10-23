"""Agent J3 helpers (manggarai-lingko, bajo-laut, jali-merah, pulang-haji): _jw_lib re-export (+_j1/_p1/art) plus
periodic weave rendering, local helpers. Previews -> /tmp/pen/nb-J3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa  (also brings _j1_lib / _p1_lib / art)
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-J3/art"
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
    h, w = a.shape
    return np.concatenate([np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32), np.clip(a, 0, 1)[..., None]], -1)


def threads(w, h, period_y=3.0, period_x=4.0, seed=1, amt=0.22):
    """Periodic woven-thread luminance field (~1.0 mean) for tileable textiles."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = wrap_noise(w, h, seed, 1.2)
    weft = 0.5 + 0.5 * np.cos(2 * math.pi * yy / period_y)
    warp = 0.5 + 0.5 * np.cos(2 * math.pi * xx / period_x)
    over_under = ((np.floor(xx / period_x) + np.floor(yy / period_y)) % 2).astype(np.float32)
    f = np.where(over_under > 0, weft, warp) * 0.6 + 0.4 * n
    return 1 - amt + amt * 2 * f * 0.9


def periodic_blur(mask, sigma):
    return gaussian_filter(mask, sigma, mode="wrap")


def cone_house(W, H, cx, by, h, w, rng):
    """mbaru niang-like cone: returns (roof, roof_bands, door, posts, finial) masks."""
    top = (cx, by - h)
    L, R = [], []
    n = 22
    for i in range(n + 1):
        t = i / n
        y = by - h + h * t
        bulge = t ** 0.62
        half = w / 2 * min(1.0, bulge)
        L.append((cx - half + rng.uniform(-0.6, 0.6), y)); R.append((cx + half + rng.uniform(-0.6, 0.6), y))
    # flared hem
    hem_y = by - h * 0.04
    roof = shapes(W, H, [L + [(cx - w * 0.55, hem_y + h * 0.03), (cx + w * 0.55, hem_y + h * 0.03)] + R[::-1]], smooth=False)
    bands = []
    for k, t in enumerate([0.22, 0.42, 0.6, 0.76, 0.9]):
        y = by - h + h * t
        half = w / 2 * min(1.0, t ** 0.62)
        bands.append(([(cx - half, y + 1.5), (cx, y + 3.5 + h * 0.01), (cx + half, y + 1.5)], max(1.2, h * 0.012), None))
    roof_bands = strokes(W, H, bands) * roof
    door = shapes(W, H, [[(cx - w * 0.06, by - h * 0.02), (cx - w * 0.06, by - h * 0.15), (cx + w * 0.06, by - h * 0.15), (cx + w * 0.06, by - h * 0.02)]], smooth=False)
    posts = strokes(W, H, [([(cx + dx * w * 0.36, by - 2), (cx + dx * w * 0.36, by + h * 0.05)], max(1.5, w * 0.03), None) for dx in (-1, -0.4, 0.4, 1)])
    fin = strokes(W, H, [([top, (top[0] - h * 0.035, top[1] - h * 0.07)], max(1.2, h * 0.016), (0.0, 0.7)),
                         ([top, (top[0] + h * 0.035, top[1] - h * 0.07)], max(1.2, h * 0.016), (0.0, 0.7))])
    return roof, roof_bands, door, posts, fin
