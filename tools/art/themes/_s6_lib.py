"""Agent S6 helpers (pantai-kei, awan-syari, pasar-bunga, khitanan-massal): _j1_lib local painting (G/GP/LC/FO/OV,
strokes/shapes/circles/ellipses) + flat/rgba/rrect/show and a few motif builders. Previews -> /tmp/pen/nb-S6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-S6/art"
os.makedirs(PREV, exist_ok=True)


def show(arr, name, tone="#f4eee3", bg=None):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return rgba(rgb, mask * alpha)


def rr(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect(w, h, items):
    """Rounded rects: (x0, y0, x1, y1, r)."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for x0, y0, x1, y1, r in items:
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), p)
    return cv.array()[..., 3]


def paint(art, mask, c1, c2=None, seed=1, rough=1.6, streak=1.0, pad=10):
    """Opaque gouache fill."""
    return GP(art, mask, c1, c2 or c1, seed=seed, rough=rough, streak=streak, pad=pad)


def shade(art, mask, col, seed=1, density=0.45, rough=2.0, feather=1.2):
    """Transparent watercolour/gouache shadow glaze on top of a painted shape."""
    return G(art, mask, col, seed=seed, density=density, edge=0.3, bloom=0.1, rough=rough, feather=feather, gran=0.2)


def cloud_mask(W, H, cx, cy, w, h, rng, lobes=7, flat_base=True):
    """Cumulus: overlapping circles on a flattened base."""
    items = []
    for i in range(lobes):
        t = i / (lobes - 1)
        x = cx - w / 2 + w * t + rng.uniform(-w * .04, w * .04)
        bump = math.sin(math.pi * t) ** 0.8
        r = h * (0.32 + 0.5 * bump) * rng.uniform(0.8, 1.15)
        y = cy + h * 0.5 - r * rng.uniform(0.75, 0.95)
        items.append((x, y, r))
    m = circles(W, H, items)
    if flat_base:
        yy = np.arange(H, dtype=np.float32)[:, None]
        m = m * np.clip((cy + h * 0.5 - yy) / 6 + 0.5, 0, 1)
    return m


def soft(mask, s):
    return gaussian_filter(mask, s)


def mirror(arr):
    return arr[:, ::-1].copy()


def palm_tree(art, W, H, bx, by, top, rng, nx, trunk=("#8a6a4a", "#5e4530"), fr=("#5f8f4e", "#2f5a36"), lean=0.25, nfr=9, flen=170, ring=True):
    """Coconut palm: curved ringed trunk + drooping fronds with leaflets (watercolour)."""
    tx, ty = top
    mid = ((bx + tx) / 2 + (tx - bx) * 0.25 * lean + 18, (by + ty) / 2)
    tr = curve([(bx, by), mid, (tx, ty)], 40)
    items = []
    n = len(tr)
    for i in range(n - 1):
        t = i / (n - 1)
        items.append(([tr[i], tr[i + 1]], 22 * (1 - t) + 11 * t, None))
    tm = strokes(W, H, items)
    art = G(art, tm, trunk[0], trunk[1], seed=nx(), density=0.85, edge=0.55, bloom=0.2, rough=2.5, gran=0.4)
    if ring:
        rings = []
        for i in range(2, n - 2, 2):
            x, y = tr[i]
            a, b = tr[i - 1], tr[i + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
            wd = (22 * (1 - i / n) + 11 * i / n) * 0.5
            rings.append(([(x - math.cos(ang) * wd, y - math.sin(ang) * wd), (x + math.cos(ang) * wd, y + math.sin(ang) * wd)], 1.6, None))
        art = G(art, strokes(W, H, rings) * tm, trunk[1], seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1, feather=0.5)
    # coconuts
    art = G(art, circles(W, H, [(tx - 10, ty + 10, 11), (tx + 8, ty + 14, 10), (tx - 1, ty + 22, 10)]), "#6f7a3a", "#4a4a22", seed=nx(), density=0.85, edge=0.6, rough=1.5)
    # fronds
    for k in range(nfr):
        a = -math.pi / 2 + (k / (nfr - 1) - 0.5) * math.pi * 1.55 + rng.uniform(-.12, .12)
        L = flen * rng.uniform(0.75, 1.1)
        droop = 0.55 + 0.3 * abs(math.cos(a))
        p0 = (tx, ty)
        p1 = (tx + math.cos(a) * L * .45, ty + math.sin(a) * L * .45 - 14)
        p2 = (tx + math.cos(a) * L * .85, ty + math.sin(a) * L * .85 + L * droop * .35)
        p3 = (tx + math.cos(a) * L * 1.0, ty + math.sin(a) * L * 1.0 + L * droop * .7)
        sp = curve([p0, p1, p2, p3], 36)
        rib = strokes(W, H, [(sp, 3.2, (0.02, 0.5))])
        leaflets, back = [], []
        for j in range(2, len(sp) - 1):
            x, y = sp[j]
            a2 = math.atan2(sp[j + 1][1] - sp[j - 1][1], sp[j + 1][0] - sp[j - 1][0])
            ll = 58 * math.sin(math.pi * min(1, j / len(sp) * 1.05)) ** 0.6 + 10
            for side in (-1, 1):
                aa = a2 + side * (0.75 + rng.uniform(-.12, .12)) + 0.35 * (1 if math.cos(a2) > 0 else -1) * 0.0
                aa = aa + 0.5 * (math.pi / 2 - aa) * 0.35  # gravity: leaflets hang
                tip = (x + math.cos(aa) * ll, y + math.sin(aa) * ll + ll * 0.25)
                midp = (x + math.cos(aa) * ll * .5, y + math.sin(aa) * ll * .5 + ll * 0.05)
                (leaflets if (j + (side > 0)) % 2 else back).append(([(x, y), midp, tip], 8.5, (0.05, 0.85)))
        art = G(art, strokes(W, H, back), fr[1], mix(fr[1], "#1d3a24", .4), seed=nx(), density=0.7, edge=0.5, bloom=0.2, rough=2.0, feather=0.7, gran=0.3)
        art = G(art, strokes(W, H, leaflets), fr[0], mix(fr[0], "#a8b85a", .3), seed=nx(), density=0.72, edge=0.55, bloom=0.35, rough=2.2, feather=0.7, gran=0.3)
        art = G(art, rib, fr[1], seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1, feather=0.5)
    return art


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in [i / (n - 1) for i in range(n)]]
