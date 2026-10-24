"""Agent Q5 helpers (sape-dayak, monokrom-syari, mawar-merah, ultah-polisi): _j1_lib media (bbox-cropped G/GP/LC/FO)
plus a few motifs of my own. Previews -> /tmp/pen/nb-Q5/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _j1_lib import *  # noqa
import _jw_lib as jw  # noqa  (spiral_pts, hills, along, lung)
import art as _art

PREV = "/tmp/pen/nb-Q5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def tint(mask, col, a=1.0):
    """Flat colour layer (used only for tiny highlights / shadows under other media)."""
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * a, 0, 1)[..., None]], -1)


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.03).astype(np.float32) - mask, 0, 1)


def inset(mask, px):
    """Mask shrunk by ~px."""
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.97).astype(np.float32), 0, 1)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def rpoly(cx, cy, r, n, rot=0.0):
    return [(cx + math.cos(rot + k * math.tau / n) * r, cy + math.sin(rot + k * math.tau / n) * r) for k in range(n)]


def star_pts(cx, cy, r0, r1, n, rot=-math.pi / 2):
    pts = []
    for k in range(n * 2):
        r = r0 if k % 2 == 0 else r1
        a = rot + k * math.pi / n
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect_mask(W, H, x0, y0, x1, y1, r):
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), p)
    return cv.array()[..., 3]


def _ell(W, H, cx, cy, rx, ry, rot=0.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c, s_ = math.cos(rot), math.sin(rot)
    u = ((xx - cx) * c + (yy - cy) * s_) / rx
    v = (-(xx - cx) * s_ + (yy - cy) * c) / ry
    return np.clip((1 - (u * u + v * v)) * min(rx, ry) * 0.5, 0, 1), u, v


def gouache_rose(art, W, H, cx, cy, r, rng, nx, light, mid, deep, tilt=0.88, area=None):
    """Opaque gouache garden rose seen from slightly above: scalloped back petals, a deep cup with a spiralling heart,
    front petals curling over the cup with lit lips, shadow toward the lower right."""
    pad = int(r * 1.3)
    x0, y0 = int(max(0, cx - pad)), int(max(0, cy - pad))
    x1, y1 = int(min(W, cx + pad)), int(min(H, cy + pad))
    w, h = x1 - x0, y1 - y0
    lx, ly = cx - x0, cy - y0
    sub = art[y0:y1, x0:x1].copy()
    def P(m, a, b=None, **k):
        nonlocal sub
        sub = GP(sub, m, a, b, **k)
    base = shape_mask(w, h, deform([(lx + math.cos(t) * r * (1 + 0.06 * math.sin(t * 7 + 1)), ly + math.sin(t) * r * tilt * (1 + 0.06 * math.sin(t * 7 + 1))) for t in [i / 40 * math.tau for i in range(40)]], rng, 1, 0.03))
    if area is not None:
        area[y0:y1, x0:x1] = np.maximum(area[y0:y1, x0:x1], base)
    P(base, mid, deep, seed=nx(), rough=1.8, streak=1.0)
    # back petals: big scallops in the upper half, lit upper-left
    for k in range(6):
        a = math.pi + k / 5 * math.pi + rng.uniform(-.15, .15)
        px, py = lx + math.cos(a) * r * .5, ly + math.sin(a) * r * .5 * tilt
        pm, _, v = _ell(w, h, px, py, r * .55, r * .42, a + math.pi / 2)
        pm = pm * base
        lit = 0.5 + 0.5 * math.cos(a - math.pi * 1.25)
        P(pm, mix(mid, light, 0.05 + 0.5 * lit), mix(deep, mid, 0.5 + 0.4 * lit), seed=nx(), rough=1.4, streak=1.2, density=0.95)
        lip = np.clip(pm - np.roll(pm, int(r * .06), 0) * 1.0, 0, 1) * 1.5
        P(np.clip(lip, 0, 1), mix(light, "#ee8a74", 0.2 * lit), seed=nx(), rough=0.6, dry=0.25, density=0.7 * (0.4 + lit))
    # the cup
    cup, _, _ = _ell(w, h, lx, ly - r * .08, r * .5, r * .38 * tilt / .88)
    P(cup, mix(deep, mid, .35), deep, seed=nx(), rough=1.0, streak=0.8)
    # spiralling heart: arcs with lit tops inside the cup
    for k in range(5):
        rr = r * (0.4 - k * 0.07)
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(lx + rng.gauss(0, r * .02), ly - r * .08, rr, a0, a0 + rng.uniform(2.2, 3.4), 26, 0.8 * tilt)
        P(stroke_mask(w, h, pts, r * 0.085) * cup, mix(mid, light, 0.1 + 0.07 * k), mid, seed=nx(), rough=0.7, streak=1.0, density=0.95)
        P(stroke_mask(w, h, [(x + r * .015, y + r * .04) for x, y in pts], r * 0.04) * cup, mix(deep, "#16030a", .5), seed=nx(), rough=0.4, density=0.8)
    # front petals curling over the cup (bowl shapes with lit lips)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    fronts = [(-r * rng.uniform(.3, .42), r * rng.uniform(.16, .26), r * .52, r * .5, -rng.uniform(.25, .45)), (r * rng.uniform(.3, .42), r * rng.uniform(.14, .24), r * .5, r * .5, rng.uniform(.3, .5))]
    rng.shuffle(fronts)
    if rng.random() < 0.6:
        fronts.append((rng.uniform(-.08, .08) * r, r * rng.uniform(.3, .36), r * .64, r * .52, rng.uniform(-.1, .1)))
    else:
        fronts = fronts[:1] + [(rng.uniform(-.1, .1) * r, r * .3, r * .7, r * .55, 0.0)]
    for k, (dx, dy, rx, ry, rot) in enumerate(fronts):
        e, u, v = _ell(w, h, lx + dx, ly + dy, rx, ry, rot)
        lipy = ly + dy - ry * 0.15 + r * 0.12 * (1 - np.clip(u, -1, 1) ** 2)
        bowl = e * np.clip((yy - lipy) * 0.6, 0, 1) * base
        lit = 0.7 if abs(dx) < r * .15 else (0.5 if dx < 0 else 0.28)
        P(bowl, mix(mid, light, 0.08 + 0.45 * lit), mix(deep, mid, 0.6 + 0.3 * lit), seed=nx(), rough=1.2, streak=1.3, density=0.97)
        lip = bowl * np.clip(1 - (yy - lipy) / (r * .07), 0, 1)
        P(lip, mix(light, "#ee8a74", 0.2), seed=nx(), rough=0.5, dry=0.2, density=0.9)
        fold = bowl * np.clip(1 - np.abs(yy - lipy - r * .14) / (r * .05), 0, 1) * 0.6
        P(fold, deep, seed=nx(), rough=0.5, density=0.45)
    # shadow toward the lower right + rim of light on the upper left edge
    sh = base * np.clip(((xx - lx) * .6 + (yy - ly)) / r - 0.15, 0, 1)
    P(sh, mix(deep, "#16030a", .3), seed=nx(), rough=1.0, density=0.45)
    edge = np.clip(base - gaussian_filter(base, r * .05) , 0, 1) * 3 * base * np.clip(-((xx - lx) + (yy - ly)) / r, 0, 1)
    P(np.clip(edge, 0, 1), light, seed=nx(), rough=0.5, dry=0.3, density=0.8)
    out = art.copy()
    out[y0:y1, x0:x1] = sub
    return out


def gouache_leaf(art, W, H, x, y, L, a, rng, nx, ca, cb, vein="#0d1a12", hi=None, width=0.36):
    pts = deform(petal_pts(x, y, L, L * width, a, n=12, cup=0.08), rng, 1, 0.03)
    m = shape_mask(W, H, pts)
    art = GP(art, m, ca, cb, seed=nx(), rough=1.4, streak=1.1)
    half = shape_mask(W, H, petal_pts(x, y, L * .95, L * width * .45, a + 0.06, n=12))
    art = GP(art, half * m, cb, mix(cb, "#000000", .25), seed=nx(), rough=1.0, streak=1.0, density=0.75)
    v = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in [j / 12 for j in range(1, 11)]]
    art = GP(art, stroke_mask(W, H, v, max(1.4, L * 0.03)) * m, vein, seed=nx(), rough=0.4, density=0.6)
    if hi:
        e = [(x + math.cos(a) * L * t - math.sin(a) * L * width * .32 * math.sin(t * math.pi), y + math.sin(a) * L * t + math.cos(a) * L * width * .32 * math.sin(t * math.pi)) for t in [j / 10 for j in range(1, 9)]]
        art = GP(art, stroke_mask(W, H, e, max(1.2, L * 0.025)) * m, hi, seed=nx(), rough=0.5, dry=0.4, density=0.6)
    return art


def kb(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")


def rose_sprite(r, rng, nx, light, mid, deep, tilt=0.88):
    n = int(r * 2.7)
    return gouache_rose(blank(n, n), n, n, n / 2, n / 2, r, rng, nx, light, mid, deep, tilt=tilt)


def place(art, sprite, cx, cy, ang=0.0, sy=1.0):
    """Composite a sprite rotated by ang (radians) and squashed vertically by sy, centred at (cx, cy)."""
    from scipy.ndimage import rotate, zoom
    sp = sprite.copy()
    sp[..., :3] *= sp[..., 3:4]
    if sy != 1.0:
        sp = zoom(sp, (sy, 1, 1), order=1)
    if ang:
        sp = rotate(sp, math.degrees(ang), axes=(1, 0), reshape=True, order=1)
    a = np.clip(sp[..., 3:4], 0, 1)
    sp = np.concatenate([np.clip(sp[..., :3] / np.maximum(a, 1e-4), 0, 1), a], -1)
    h, w = sp.shape[:2]; H, W = art.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x0 + w), min(H, y0 + h)
    if dx1 <= dx0 or dy1 <= dy0:
        return art
    out = art.copy()
    out[dy0:dy1, dx0:dx1] = over(art[dy0:dy1, dx0:dx1], sp[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0])
    return out
