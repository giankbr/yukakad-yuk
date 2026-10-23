"""Agent J6 helpers (peta-bintang, piknik-gingham, kertas-quilling, pesta-piyama): builds on _i3_lib (bbox-cropped
painting, kids ink outlines, textile media) and adds: engraved star-chart pieces (magnitude stars, dashed rings),
paper quilling (coiled on-edge paper strips with lit top edge + cast shadow), gingham weave, fairy-light bulbs.
Previews -> /tmp/pen/nb-J6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _i3_lib import *  # noqa
import _i3_lib, _a1_lib, _j1_lib
PREV = "/tmp/pen/nb-J6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _a1_lib.PREV = _i3_lib.PREV = PREV
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt


def prev(arr, name, bg=None, tone="#fbf6e4"):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def ell(W, H, cx, cy, rx, ry, rot=0.0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def rrect(W, H, x0, y0, x1, y1, r, rot=0.0, cx=None, cy=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.save()
        if rot:
            cv.c.rotate(rot, cx if cx is not None else (x0 + x1) / 2, cy if cy is not None else (y0 + y1) / 2)
        cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, p)
        cv.c.restore()
    return mask_from(W, H, draw)


def dashed(W, H, pts, width, dash=10.0, gap=7.0):
    """Dashed polyline mask."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       StrokeCap=skia.Paint.kRound_Cap)
        p.setPathEffect(skia.DashPathEffect.Make([dash, gap], 0))
        cv.c.drawPath(poly_path(pts) if False else _open_path(pts), p)
    return mask_from(W, H, draw)


def _open_path(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    return p


def circle_line(W, H, cx, cy, r, width, dash=None):
    pts = arc_pts(cx, cy, r, 0, math.tau, max(60, int(r * 0.8)))
    pts.append(pts[0])
    if dash:
        return dashed(W, H, pts, width, *dash)
    return polyline_mask(W, H, [pts], width)


def star_dots(W, H, stars):
    """stars: (x, y, r) -> soft core mask."""
    return circles(W, H, stars)


def fourpoint(W, H, cx, cy, r, thin=0.18, rot=0.0):
    """Four-point star (diffraction sparkle) mask."""
    pts = []
    for k in range(8):
        a = rot + k * math.pi / 4
        rr = r if k % 2 == 0 else r * thin
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return shapes(W, H, [pts], smooth=False)


def ink_tone(arr, mask, col, alpha=1.0, seed=1, wear=0.25):
    """Printed ink line (engraving) with slight wear."""
    return LC(arr, mask, col, seed=seed, wear=wear, rough=0.6)


# ------------------------------------------------------------------ quilling
def quill_strip(W, H, pts, col, seed=1, width=5.0, light=(-0.6, -0.8), shadow=0.45, base=None):
    """A paper strip standing on edge along `pts` (top view): a thin band of colour with a bright lit edge on the light
    side, a darker inner edge, fine paper fibre, and a soft cast shadow on the card below. Returns RGBA layer."""
    m = polyline_mask(W, H, [pts], width)
    return quill_from_mask(m, col, seed, light, shadow)


def quill_from_mask(m, col, seed=1, light=(-0.6, -0.8), shadow=0.45, shadow_col="#3a2a20"):
    h, w = m.shape
    lay = blank(w, h)
    # cast shadow: offset away from the light, blurred
    dx, dy = -light[0] * 4.0, -light[1] * 4.0
    sh = np.roll(np.roll(gaussian_filter(m, 2.6), int(round(dy)), 0), int(round(dx)), 1)
    lay = over(lay, flat(np.clip(sh * 1.4, 0, 1), shadow_col, shadow))
    sh2 = np.roll(np.roll(gaussian_filter(m, 0.9), int(round(dy * 0.4)), 0), int(round(dx * 0.4)), 1)
    lay = over(lay, flat(np.clip(sh2 * 1.2, 0, 1), shadow_col, shadow * 0.6))
    # body colour with slight tonal drift
    c = col_arr(col)
    t = fbm(w, h, seed, 60, 2)[..., None]
    rgb = c * (0.92 + 0.12 * t)
    # edge lighting from gradient of the mask
    gy, gx = np.gradient(gaussian_filter(m, 0.8))
    lit = np.clip(-(gx * light[0] + gy * light[1]) * 4.0, -1, 1)[..., None]
    rgb = np.where(lit > 0, rgb + (1 - rgb) * lit * 0.75, rgb * (1 + lit * 0.45))
    fib = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.4, 0.4))
    rgb = rgb * (0.96 + 0.08 * fib[..., None])
    body = np.concatenate([np.clip(rgb, 0, 1), np.clip(m, 0, 1)[..., None]], -1)
    return over(lay, body)


def coil_pts(cx, cy, r, turns=5.0, shape="round", ang=0.0, pinch=0.0, n=None, r0=1.5, off=0.24, odir=0.8):
    """Loose coil spiral, optionally pinched: shape round | tear | marquise | eye. `ang` orients the pinch. The inner
    turns sit off-centre (`off` * r toward `odir`) the way a released loose coil relaxes."""
    n = n or int(60 + turns * 50)
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = t * turns * math.tau
        rr = r0 + (r - r0) * (t ** 0.85)
        o = (1 - t) ** 1.3 * off * r
        x, y = math.cos(a) * rr + math.cos(odir) * o, math.sin(a) * rr + math.sin(odir) * o
        pts.append((x, y))
    return [_shape_xform(x, y, r, shape, ang, cx, cy) for x, y in pts]


def _shape_xform(x, y, r, shape, ang, cx, cy):
    # local frame: pinch direction along +x
    if shape == "tear":
        # stretch toward +x, narrowing to a point
        u = x / r
        k = 1.0 + 0.9 * max(0.0, u)
        y = y * (1 - 0.55 * max(0.0, u) ** 1.2)
        x = x * k
    elif shape == "marquise":
        u = abs(x) / r
        x = x * 1.35
        y = y * (1 - 0.72 * u ** 1.1) * 0.8
    elif shape == "eye":
        u = abs(x) / r
        x = x * 1.2
        y = y * (1 - 0.45 * u ** 1.4) * 0.85
    elif shape == "square":
        m = max(abs(x), abs(y)) + 1e-6
        l = math.hypot(x, y)
        x, y = x * (l / m) * 0.82, y * (l / m) * 0.82
    ca, sa = math.cos(ang), math.sin(ang)
    return (cx + x * ca - y * sa, cy + x * sa + y * ca)


def outline_pts(cx, cy, r, shape="round", ang=0.0, n=120):
    """The outermost loop of a coil (the wrapping strip)."""
    pts = [(math.cos(a) * r, math.sin(a) * r) for a in np.linspace(0, math.tau, n)]
    return [_shape_xform(x, y, r, shape, ang, cx, cy) for x, y in pts]


def quill_coil(art, W, H, cx, cy, r, col, seed=1, turns=None, shape="round", ang=0.0, width=4.2, light=(-0.6, -0.8), shadow=0.42, off=0.24):
    turns = turns or max(3.0, r / 7.5)
    odir = (seed * 2.399) % math.tau
    pts = coil_pts(cx, cy, r, turns, shape, ang, off=off, odir=odir)
    m = polyline_mask(W, H, [pts, outline_pts(cx, cy, r, shape, ang)], width)
    return _place(art, m, col, seed, light, shadow)


def _place(art, m, col, seed, light, shadow):
    b = bbox(m, 14)
    if b is None:
        return art
    y0, y1, x0, x1 = b
    lay = quill_from_mask(np.ascontiguousarray(m[y0:y1, x0:x1]), col, seed, light, shadow)
    out = art.copy()
    out[y0:y1, x0:x1] = over(art[y0:y1, x0:x1], lay)
    return out


def quill_line(art, W, H, pts, col, seed=1, width=4.2, light=(-0.6, -0.8), shadow=0.42):
    return _place(art, polyline_mask(W, H, [pts], width), col, seed, light, shadow)


def quill_lines(art, W, H, lines, col, seed=1, width=4.2, light=(-0.6, -0.8), shadow=0.42):
    return _place(art, polyline_mask(W, H, lines, width), col, seed, light, shadow)


def quill_leaf(art, W, H, cx, cy, L, ang, col, seed=1, width=4.0, vein=True, folds=5):
    """Leaf: marquise outline + angled zig-zag 'husking' inside (classic quilled leaf)."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    hw = L * 0.32
    outline = [P(L * math.cos(t) * 0.5, hw * math.sin(t) * (abs(math.sin(t)) ** 0.15)) for t in np.linspace(0, math.tau, 90)]
    lines = [outline]
    if vein:
        lines.append([P(-L * 0.5, 0), P(L * 0.5, 0)])
        for k in range(1, folds + 1):
            u = -L * 0.5 + L * k / (folds + 1)
            wv = hw * math.sqrt(max(0.0, 1 - (2 * u / L) ** 2)) * 0.92
            lines.append([P(u - L * 0.06, -wv), P(u + L * 0.05, 0), P(u - L * 0.06, wv)])
    return _place(art, polyline_mask(W, H, lines, width), col, seed, (-0.6, -0.8), 0.4)


def quill_flower(art, W, H, cx, cy, R, cols, center, nx, petals=6, rot=0.0, shape="tear", inner=None):
    """Ring of pinched coils around a tight centre coil."""
    for k in range(petals):
        a = rot + k * math.tau / petals
        pr = R * 0.36
        px, py = cx + math.cos(a) * (R * 0.58), cy + math.sin(a) * (R * 0.58)
        col = cols[k % len(cols)]
        # pinch points outward for 'tear' so petals are round at centre
        art = quill_coil(art, W, H, px, py, pr, col, seed=nx(), shape=shape, ang=a + (0 if shape != "tear" else math.pi), turns=pr / 6.0)

    if inner:
        for k in range(petals):
            a = rot + (k + 0.5) * math.tau / petals
            pr = R * 0.2
            art = quill_coil(art, W, H, cx + math.cos(a) * R * 0.34, cy + math.sin(a) * R * 0.34, pr, inner, seed=nx(), shape="tear", ang=a + math.pi, turns=pr / 5.5)
    art = quill_coil(art, W, H, cx, cy, R * 0.22, center, seed=nx(), turns=R * 0.22 / 3.6, width=4.0, off=0.0)
    return art


def scroll_pts(x0, y0, x1, y1, r, turns=1.6, side=1, n=80):
    """Open scroll: a strip from (x0,y0) that curls into a loose spiral of radius r ending near (x1,y1)."""
    a_in = math.atan2(y0 - y1, x0 - x1)
    pts = [(x0, y0)]
    for i in range(1, n):
        t = i / (n - 1)
        a = a_in + side * t * turns * math.tau
        rr = r * (1 - t * 0.85)
        pts.append((x1 + math.cos(a) * rr, y1 + math.sin(a) * rr))
    return pts


def fringe_flower(art, W, H, cx, cy, R, col, nx, n=40):
    """Fringed flower: many short radial strips (cut fringe rolled) seen from above."""
    lines = []
    rng = random.Random(nx())
    for k in range(n):
        a = k * math.tau / n + rng.uniform(-0.03, 0.03)
        r1 = R * rng.uniform(0.85, 1.0)
        lines.append([(cx + math.cos(a) * R * 0.25, cy + math.sin(a) * R * 0.25), (cx + math.cos(a + 0.05) * r1, cy + math.sin(a + 0.05) * r1)])
    return _place(art, polyline_mask(W, H, lines, 3.2), col, nx(), (-0.6, -0.8), 0.35)


# ------------------------------------------------------------------ gingham + fairy lights
def gingham(w, h, cell, col, base="#fffaf2", seed=1, alpha=0.55, warp_jit=1.0):
    """Woven gingham: semi-opaque dyed stripes both ways (double density where they cross), visible weave."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    jx = (fbm(w, h, seed, 60, 2) - 0.5) * warp_jit * 2
    jy = (fbm(w, h, seed + 1, 60, 2) - 0.5) * warp_jit * 2
    sx = (((xx + jx) / cell) % 2.0) < 1.0
    sy = (((yy + jy) / cell) % 2.0) < 1.0
    a = (sx.astype(np.float32) + sy.astype(np.float32)) * alpha
    a = np.clip(gaussian_filter(a, 0.5), 0, 1.0)
    cloth = cloth_base(w, h, base, seed + 2, 2.2, 0.05)
    c = col_arr(col)
    rgb = cloth[..., :3] * (1 - a[..., None]) + (cloth[..., :3] * c) * a[..., None]
    wv = weave(w, h, None, None, seed + 4, 2.2)
    rgb = rgb * (0.94 + 0.06 * wv[..., None])
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)
