"""Agent S5 helpers (rumah-baloy, bunga-rampai, dermaga-kayu, ultah-hutan).
_j1_lib (local bbox painting, strokes/shapes masks) + small utilities. Previews -> /tmp/pen/nb-S5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-S5/art"
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


def shade(art, mask, col, amt=0.35, dx=1, seed=1, dy=0):
    """Side shading painted as a second, darker gouache pass on one side of a form."""
    sh = np.roll(np.roll(mask, int(dx), 1), int(dy), 0)
    side = np.clip(mask - sh, 0, 1)
    side = gaussian_filter(side, 4) * mask
    return GP(art, np.clip(side * 2.2, 0, 1) * amt * 2.5, col, seed=seed, rough=1.0, streak=0.6, density=0.6)


def lines(w, h, segs, width, cap=True):
    """Untapered polylines into one mask."""
    return strokes(w, h, [(p, width, None) for p in segs], cap=cap)


def eye(art, W, H, x, y, r, seed, ink="#2a1d18"):
    art = GP(art, ellipses(W, H, [(x, y, r * 0.9, r * 1.1, 0)]), ink, seed=seed, rough=0.5, streak=0.1)
    return OV(art, circles(W, H, [(x + r * 0.35, y - r * 0.4, r * 0.34)]), lambda q: flat(q, "#ffffff", 0.95))


def cheeks(art, W, H, pts, r, seed, col="#f29a9a"):
    return G(art, circles(W, H, [(x, y, r) for x, y in pts]), col, seed=seed, density=0.55, edge=0.2, bloom=0.1, rough=1.5, feather=1.5)


def smile(art, W, H, x, y, s, seed, ink="#2a1d18"):
    pts = arc_pts(x, y, s, 0.4, math.pi - 0.4, 12, 0.8)
    return GP(art, strokes(W, H, [(pts, max(1.5, s * 0.28), (0.2, 0.2))]), ink, seed=seed, rough=0.4, streak=0.1)


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s = os.path.getsize(os.path.join(d, f)); tot += s
        print(f"  {f:28s} {s // 1024:4d} KB")
    print(f"  total {tot // 1024} KB")
