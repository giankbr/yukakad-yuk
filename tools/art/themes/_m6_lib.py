"""Agent M6 helpers (biru-syari, provence-lavender, kebun-sayur, turnamen-futsal): _j1_lib bbox-cropped painting +
small motif helpers. Previews -> /tmp/pen/nb-M6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art
PREV = _p1_lib.PREV = "/tmp/pen/nb-M6/art"
os.makedirs(PREV, exist_ok=True)


def clear():
    _art._fbm_cache.clear()


def pv(arr, name, bg="#f7f3ec"):
    """Preview composited on a flat colour."""
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def quad(pts):
    return pts


def wash(dst, mask, col, col2=None, seed=1, dens=0.5, **k):
    """Light flat-ish watercolour shading pass (no blooms)."""
    k.setdefault("edge", 0.15); k.setdefault("bloom", 0.0); k.setdefault("rough", 1.5)
    return G(dst, mask, col, col2, seed=seed, density=dens, **k)


def petal_ring(cx, cy, r, n, w=0.42, rot=0.0, jitter=0.08, rng=None):
    out = []
    for k in range(n):
        a = rot + k / n * math.tau + (rng.uniform(-jitter, jitter) if rng else 0)
        out.append(petal_pts(cx, cy, r * (rng.uniform(0.9, 1.08) if rng else 1), r * w, a, n=12))
    return out


def lerp(a, b, t):
    return a + (b - a) * t


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s_ = os.path.getsize(os.path.join(d, f)); tot += s_
        print(f"  {f}: {s_ // 1024} KB")
    print("  total", tot // 1024, "KB")
