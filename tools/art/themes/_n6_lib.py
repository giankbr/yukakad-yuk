"""Agent N6 helpers (rumah-kaca, selancar-retro, kafe-kopi, isra-miraj): builds on _jw_lib (G/GP/LC/FO/OV, strokes,
shapes, circles, ellipses, Seq, outdir, preview, save). Previews -> /tmp/pen/nb-N6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-N6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def prev(arr, name, tone="#fbf6e4", bg=None):
    """preview() into our folder (the imported one binds its own PREV)."""
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def frond(W, H, pts, leaf_len, leaf_w, step=2, spread=0.95, droop=0.25, both=True, profile=0.8, n=9):
    """Pinnate frond (fern / palm) mask: leaflets on both sides of a rachis curve. Leaflets shrink toward the tip."""
    polys = []
    N = len(pts)
    for i in range(1, N - 1, step):
        t = i / (N - 1)
        a, b = pts[i - 1], pts[i + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        k = (math.sin(math.pi * min(1.0, 0.15 + t * 0.95)) ** profile)
        L = leaf_len * (0.25 + 0.75 * k)
        for side in ((-1, 1) if both else (1,)):
            la = ang + side * spread
            # gravity: rotate leaflet slightly toward +y
            gy = math.atan2(math.sin(la) + droop, math.cos(la))
            polys.append(petal_pts(pts[i][0], pts[i][1], L, leaf_w * (0.4 + 0.6 * k), gy, n=n))
    m = shapes(W, H, polys)
    rach = strokes(W, H, [(pts, max(1.2, leaf_w * 0.35), (0.02, 0.6))])
    return np.maximum(m, rach)


def edge_hi(mask, dx=-2, dy=-2):
    """Thin highlight on the lit side (default light from top-left)."""
    return np.clip(mask - np.roll(np.roll(mask, -dy, 0), -dx, 1), 0, 1)


def edge_lo(mask, dx=2, dy=2):
    return np.clip(mask - np.roll(np.roll(mask, -dy, 0), -dx, 1), 0, 1)


def tint(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


def lay(art, mask, col, alpha=1.0):
    """Plain over of a flat colour through a (soft) mask — for light/haze, never for whole shapes."""
    return over(art, tint(mask, col, alpha))


def rays(W, H, ox, oy, angles, width, length):
    """Soft light shafts from (ox, oy)."""
    polys = []
    for a, wd in zip(angles, width):
        ex, ey = ox + math.cos(a) * length, oy + math.sin(a) * length
        nxp, nyp = -math.sin(a), math.cos(a)
        polys.append([(ox + nxp * wd * 0.15, oy + nyp * wd * 0.15), (ex + nxp * wd, ey + nyp * wd), (ex - nxp * wd, ey - nyp * wd), (ox - nxp * wd * 0.15, oy - nyp * wd * 0.15)])
    return gaussian_filter(shapes(W, H, polys, smooth=False), 14)


def star_pts(cx, cy, r_out, r_in, n=8, rot=0.0):
    pts = []
    for k in range(n * 2):
        r = r_out if k % 2 == 0 else r_in
        a = rot + k * math.pi / n
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
