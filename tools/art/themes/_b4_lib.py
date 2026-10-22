"""Agent B4 helpers (boho-pampas, hydrangea-biru, riso-cetak, kaca-patri): builds on _j1_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds dry-brush plumes, hydrangea florets, painted silk ribbon,
risograph halftone plates and leaded stained-glass rendering. Previews -> /tmp/pen/nb-B4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_PV = "/tmp/claude-0/-home-claude/321caf49-05cb-50f3-a5dd-72a951b968c9/scratchpad/art"
os.makedirs(_PV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = _PV
_j1_lib.PREV = _PV
import art as _art
from scipy import ndimage
PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def rgb_arr(h, w, col):
    return np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)


def layer(mask, col, alpha=1.0):
    h, w = mask.shape
    return np.concatenate([rgb_arr(h, w, col), (np.clip(mask, 0, 1) * alpha)[..., None]], -1)


def emboss_light(mask, depth=1.0, blur=1.6, ang=(-0.7, -0.7)):
    m = gaussian_filter(mask, blur)
    gy, gx = np.gradient(m)
    d = -(gx * ang[0] + gy * ang[1]) * depth * 6
    return np.clip(d, 0, 1), np.clip(-d, 0, 1)


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1); u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def resample(pts, step):
    """Polyline -> [(x, y, angle)] at fixed arc length."""
    out = []; acc = 0.0
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.atan2(y1 - y0, x1 - x0)))
            acc += step
        acc -= d
    return out


def drybrush(mask, seed, amount=0.5, along=(0.6, 6.0)):
    """Break a stroke mask with streaky gaps like a half-loaded bristle brush."""
    h, w = mask.shape
    st = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), along)
    st = (st - st.min()) / (st.max() - st.min() + 1e-6)
    return mask * (1 - np.clip((st - (1 - amount * 0.6)) * 5, 0, 1))


# ---------- boho: pampas plumes, bunny tails, palm spears ----------
def _plume_frame(stem, length_frac):
    pts = resample(stem, 2.0)
    n0 = int(len(pts) * (1 - length_frac))
    return pts[n0:]


def plume_halfwidth(t, wmax):
    return wmax * (math.sin(min(1.0, t * 1.1 + 0.04) * math.pi) ** 0.6) * (1 - 0.5 * t) + wmax * 0.06


def plume_items(rng, seg, wmax, n, fib=(14, 40), width=(0.7, 1.8), side_bias=0.0, curl=0.35):
    """Fibre strokes scattered inside the plume silhouette, combed along the stem and fanning outward at the sides."""
    items = []
    m = len(seg)
    for _ in range(n):
        t = rng.random() ** 0.9
        i = min(m - 1, int(t * (m - 1)))
        x, y, a = seg[i]
        hw = plume_halfwidth(t, wmax)
        u = max(-1.0, min(1.0, rng.gauss(side_bias, 0.55)))
        nxv, nyv = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
        sx, sy = x + nxv * u * hw * 0.9, y + nyv * u * hw * 0.9
        ang = a + u * 0.75 + rng.gauss(0, 0.14)
        L = rng.uniform(*fib) * (0.55 + 0.6 * (1 - abs(u) * 0.3)) * (1 - 0.4 * t)
        k = u * rng.uniform(0, curl)
        p = [(sx, sy)]
        for j in range(1, 6):
            s_ = j / 5
            aa = ang + k * s_
            p.append((p[-1][0] + math.cos(aa) * L / 5, p[-1][1] + math.sin(aa) * L / 5))
        items.append((p, rng.uniform(*width), (0.05, 0.75)))
    return items


def pampas(art, W, H, stem, rng, nx, base="#d8c4a4", light="#f3e9d7", shade="#a98763", stemcol="#9a7b55", scale=1.0, length_frac=0.6, wmax=None):
    """Dry-brushed pampas plume: a fluffy body wash, shaded under-fibres, oat fibres, light gouache wisps; cane stem."""
    seg = _plume_frame(stem, length_frac)
    wmax = wmax or 42 * scale
    stem_m = strokes(W, H, [(stem[: int(len(stem) * (1 - length_frac * 0.5))], 2.4 * scale, (0.02, 0.2))])
    art = G(art, stem_m, stemcol, mix(stemcol, "#6e5235", 0.4), seed=nx(), density=0.8, edge=0.4, bloom=0, rough=1.0, feather=0.5)
    left, right = [], []
    for i, (x, y, a) in enumerate(seg):
        t = i / max(1, len(seg) - 1); hw = plume_halfwidth(t, wmax) * 0.9
        nxv, nyv = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
        left.append((x + nxv * hw, y + nyv * hw)); right.append((x - nxv * hw, y - nyv * hw))
    sil = shapes(W, H, [left[::3] + right[::-3]])
    art = G(art, sil, mix(shade, base, 0.55), base, seed=nx(), density=0.52, edge=0.3, bloom=0.55, gran=0.45, rough=6 * scale, feather=3 * scale)
    L = int(len(seg) * 2.2 * (wmax / 30))
    sc = lambda it: [(p, w * scale, tp) for p, w, tp in it]
    f = lambda a_, b_: (a_ * scale, b_ * scale)
    under = strokes(W, H, sc(plume_items(rng, seg, wmax, L, fib=f(20, 54), width=(1.2, 2.6), side_bias=-0.35)))
    art = G(art, drybrush(under, nx(), 0.45), shade, mix(shade, base, 0.4), seed=nx(), density=0.5, edge=0.35, bloom=0.2, gran=0.45, rough=1.3, feather=0.7)
    mid = strokes(W, H, sc(plume_items(rng, seg, wmax, int(L * 1.4), fib=f(18, 50), width=(0.8, 1.9))))
    art = G(art, drybrush(mid, nx(), 0.5), base, mix(base, light, 0.35), seed=nx(), density=0.7, edge=0.45, bloom=0.15, gran=0.45, rough=1.0, feather=0.5)
    top = strokes(W, H, sc(plume_items(rng, seg, wmax * 0.9, int(L * 0.8), fib=f(14, 40), width=(0.6, 1.3), side_bias=0.3)))
    art = GP(art, drybrush(top, nx(), 0.55), light, "#fffaf0", seed=nx(), rough=0.6, streak=0.6, density=0.8)
    return art


def bunny_tail(art, W, H, x, y, s, ang, rng, nx, stem_len=None, col="#efe3cc", shade="#b59a72", stemcol="#9a7b55"):
    """Lagurus 'bunny tail': soft ovoid fluff head on a fine wiry stem."""
    if stem_len:
        p = curve([(x, y), (x - math.cos(ang) * stem_len * 0.5 + rng.uniform(-8, 8), y - math.sin(ang) * stem_len * 0.5),
                   (x - math.cos(ang) * stem_len, y - math.sin(ang) * stem_len)], 20)
        art = G(art, strokes(W, H, [(p, 1.6 * s / 14, (0.02, 0.3))]), stemcol, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.8, feather=0.4)
    items = []
    ca_, sa_ = math.cos(ang), math.sin(ang)
    for _ in range(int(260 * s / 14)):
        while True:
            u, v = rng.uniform(-1, 1), rng.uniform(-1, 1)
            if u * u + v * v < 1:
                break
        cx = x + ca_ * u * s * 1.05 - sa_ * v * s * 0.55
        cy = y + sa_ * u * s * 1.05 + ca_ * v * s * 0.55
        a = math.atan2(v * 0.55, u * 1.05) + ang + rng.gauss(0, 0.5)
        L = rng.uniform(0.15, 0.45) * s
        items.append(([(cx, cy), (cx + math.cos(a) * L, cy + math.sin(a) * L)], rng.uniform(0.6, 1.1), (0.1, 0.7)))
    body = ellipses(W, H, [(x, y, s * 1.1, s * 0.58, math.degrees(ang))])
    art = G(art, body, shade, mix(shade, col, 0.55), seed=nx(), density=0.6, edge=0.15, bloom=0.4, gran=0.5, rough=2.5, feather=2.2)
    fm = strokes(W, H, items)
    art = G(art, drybrush(fm, nx(), 0.4), shade, seed=nx(), density=0.45, edge=0.1, bloom=0, gran=0.4, rough=0.6, feather=0.4)
    art = GP(art, drybrush(shift(fm, -1.2, -1.2), nx(), 0.5), col, "#fffaf0", seed=nx(), rough=0.4, streak=0.4, density=0.8)
    return art


def palm_spear(art, W, H, x, y, L, ang, rng, nx, col="#c79a68", deep="#8c6239", width=None):
    """Dried palm spear: a long narrow pleated blade, pleat lines darker, papery tip splits."""
    width = width or L * 0.12
    ca, sa = math.cos(ang), math.sin(ang)
    nxv, nyv = -sa, ca
    left, right = [], []
    for i in range(21):
        t = i / 20
        wd = width * (math.sin(min(1, t * 1.6) * math.pi / 2) * (1 - t) ** 0.8 + 0.02)
        bx, by = x + ca * L * t, y + sa * L * t
        bend = math.sin(t * math.pi) * L * 0.04
        left.append((bx + nxv * (wd + bend), by + nyv * (wd + bend)))
        right.append((bx - nxv * (wd - bend), by - nyv * (wd - bend)))
    blade = shapes(W, H, [left + right[::-1]])
    art = G(art, blade, col, mix(col, "#e3c8a0", 0.4), seed=nx(), density=0.95, edge=0.6, bloom=0.3, gran=0.35, rough=1.6, feather=0.8)
    pleats = []
    for k in range(-3, 4):
        f = k / 3.6
        p = [(left[i][0] * (0.5 + f / 2) + right[i][0] * (0.5 - f / 2), left[i][1] * (0.5 + f / 2) + right[i][1] * (0.5 - f / 2)) for i in range(1, 19)]
        pleats.append((p, 1.0, (0.1, 0.5)))
    art = G(art, drybrush(strokes(W, H, pleats), nx(), 0.5), deep, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    stalk = strokes(W, H, [([(x - ca * L * 0.06, y - sa * L * 0.06), (x + ca * 4, y + sa * 4)], 3.0, (0.0, 0.3))])
    art = G(art, stalk, deep, seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.8, feather=0.5)
    return art


# ---------- hydrangea ----------
def floret_polys(cx, cy, r, rot, rng, tilt=1.0):
    """Four rounded petals (+ small notch) of one hydrangea floret."""
    polys = []
    for k in range(4):
        a = rot + k * math.pi / 2 + rng.gauss(0, 0.12)
        L = r * rng.uniform(0.85, 1.1)
        ox, oy = cx + math.cos(a) * r * 0.1, cy + math.sin(a) * r * 0.1
        pts = petal_pts(ox, oy, L, L * 0.5, a, n=14, cup=0.0)
        pts = [(cx + (px - cx), cy + (py - cy) * tilt) for px, py in pts]
        polys.append(pts)
    return polys


def hydrangea(art, W, H, cx, cy, R, rng, nx, palette, n=None, tilt=0.82, fr=None):
    """Mophead cluster: a shadow wash for the dome, then densely packed florets in three glazed layers (overlaps read
    as petal edges), paler at the crown, deeper at the rim; dark eyes; knocks out whatever was painted beneath."""
    fr = fr or R * 0.2
    dome = ellipses(W, H, [(cx, cy, R * 1.0, R * tilt + R * 0.06, 0)])
    art = knockout(art, dome, amount=0.85, grow=4)
    art = G(art, dome, palette[2], palette[3], seed=nx(), density=0.55, edge=0.45, bloom=0.5, gran=0.3, rough=5, feather=3)
    shade_ = dome * np.clip((np.mgrid[0:H, 0:W][0] - cy) / (R * tilt) + 0.2, 0, 1)
    art = G(art, shade_, palette[-1], seed=nx(), density=0.35, edge=0.1, bloom=0.4, gran=0.3, rough=4, feather=4)
    lumps = [(cx, cy, R * 0.86)]
    for k in range(7):
        a = k * math.tau / 7 + rng.uniform(-0.3, 0.3)
        lumps.append((cx + math.cos(a) * R * 0.55, cy + math.sin(a) * R * 0.55 * tilt, R * rng.uniform(0.38, 0.5)))
    pts = []
    for _ in range(7000):
        a = rng.uniform(0, math.tau); d = R * math.sqrt(rng.random()) * 1.08
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * tilt
        if any((x - lx) ** 2 + ((y - ly) / tilt) ** 2 < lr * lr for lx, ly, lr in lumps):
            pts.append((x, y, min(1.0, d / R)))
    keep = []
    sp = (fr * 0.95) ** 2
    for p in pts:
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > sp for q in keep):
            keep.append(p)
    keep.sort(key=lambda p: -p[2])
    # light from upper-left: florets on the lower right sit in shadow
    groups = {}
    for (x, y, d) in keep:
        lit = ((cx - x) * 0.6 + (cy - y) * 0.8) / R
        tone = d * 0.75 - lit * 0.35 + rng.uniform(-0.25, 0.25)
        ci = min(len(palette) - 1, max(0, int((tone + 0.25) * (len(palette) - 1))))
        groups.setdefault((rng.randrange(3), ci), []).append((x, y, d))
    for key in sorted(groups, key=lambda k: (k[0], -k[1])):
        lay, ci = key
        polys, centres = [], []
        for (x, y, d) in groups[key]:
            r = fr * rng.uniform(0.9, 1.25) * (1 - 0.2 * d)
            polys += floret_polys(x, y, r, rng.uniform(0, math.tau), rng, tilt=rng.uniform(0.7, 1.0))
            centres.append((x, y, max(1.0, r * 0.11)))
        m = shapes(W, H, polys)
        col = palette[ci]
        art = G(art, m, col, mix(col, palette[max(0, ci - 1)], 0.6), seed=nx(), density=0.52, edge=1.1, bloom=0.35, gran=0.25, rough=1.2, feather=0.6, pad=8)
        art = G(art, circles(W, H, centres), mix(col, "#262a55", 0.55), seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.4, feather=0.3, pad=6)
    return art


def serrated_leaf(art, W, H, x, y, L, ang, rng, nx, ca="#7f9c8f", cb="#5a7d78", vein="#3f5d5a", width=0.3):
    pts = petal_pts(x, y, L, L * width, ang, n=44, cup=0.0)
    sp = []
    for i, (px, py) in enumerate(pts):
        k = 1.0 + (0.022 if i % 2 else -0.006)
        sp.append((x + (px - x) * k, y + (py - y) * k))
    m = shapes(W, H, [sp], smooth=False)
    m = gaussian_filter(m, 0.6)
    art = G(art, m, ca, cb, seed=nx(), density=0.72, edge=0.6, bloom=0.4, gran=0.3, rough=1.2, feather=0.7)
    ca_, sa_ = math.cos(ang), math.sin(ang)
    mid = [(x + ca_ * L * t, y + sa_ * L * t) for t in np.linspace(0.02, 0.9, 10)]
    items = [(mid, 1.4, (0.05, 0.4))]
    for t in np.linspace(0.18, 0.75, 5):
        bx, by = x + ca_ * L * t, y + sa_ * L * t
        for s_ in (-1, 1):
            a2 = ang + s_ * 0.75
            items.append(([(bx, by), (bx + math.cos(a2) * L * 0.2, by + math.sin(a2) * L * 0.2)], 0.9, (0.05, 0.6)))
    art = G(art, strokes(W, H, items), vein, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    return art


def ribbon_band(W, H, spine, width, twist_freq=1.0, phase=0.0):
    """Ribbon as a polygon strip along a spine whose apparent width oscillates (twists). Returns (mask, facing, sheen)."""
    pts = resample(spine, 2.0)
    n = len(pts)
    left, right, fac = [], [], []
    for i, (x, y, a) in enumerate(pts):
        t = i / max(1, n - 1)
        c = math.cos(t * math.pi * 2 * twist_freq + phase)
        wd = width * (0.18 + 0.82 * abs(c))
        nxv, nyv = -math.sin(a), math.cos(a)
        left.append((x + nxv * wd, y + nyv * wd)); right.append((x - nxv * wd, y - nyv * wd))
        fac.append(c)
    mask = shapes(W, H, [left + right[::-1]], smooth=False)
    # sheen: a highlight streak along the spine, strongest where ribbon faces the light (c>0)
    sheen_items, shade_items = [], []
    for i in range(1, n):
        x0, y0 = pts[i - 1][:2]; x1, y1 = pts[i][:2]
        c = fac[i]
        if c > 0.25:
            off = width * 0.25 * abs(c)
            a = pts[i][2]
            sheen_items.append(([(x0 - math.sin(a) * off, y0 + math.cos(a) * off), (x1 - math.sin(a) * off, y1 + math.cos(a) * off)], width * 0.35 * c, None))
        if abs(c) < 0.45:
            shade_items.append(([(x0, y0), (x1, y1)], width * 0.9, None))
    sheen = strokes(W, H, sheen_items) * mask if sheen_items else np.zeros((H, W), np.float32)
    shade = strokes(W, H, shade_items) * mask if shade_items else np.zeros((H, W), np.float32)
    return mask, gaussian_filter(sheen, 2.0), gaussian_filter(shade, 2.5)


def silk(art, mask, sheen, shade, nx, col="#9fb3d9", deep="#5f74a8", light="#f2f5fc"):
    art = G(art, mask, col, mix(col, deep, 0.25), seed=nx(), density=0.8, edge=0.55, bloom=0.25, gran=0.15, rough=1.0, feather=0.6)
    art = G(art, shade, deep, seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1.0, feather=1.2)
    art = GP(art, np.clip(sheen * 1.6, 0, 1), light, "#ffffff", seed=nx(), rough=0.4, streak=0.8, density=0.7)
    return art


# ---------- risograph ----------
def halftone(tone, cell=7.0, angle=0.26, gain=1.0, rough=0.0, seed=1):
    """AM halftone dots for a tone field (0 = no ink .. 1 = full). Returns ink coverage 0..1."""
    h, w = tone.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s_ = math.cos(angle), math.sin(angle)
    u = (xx * c + yy * s_) / cell; v = (-xx * s_ + yy * c) / cell
    fu = (u - np.floor(u)) - 0.5; fv = (v - np.floor(v)) - 0.5
    d = np.sqrt(fu * fu + fv * fv)                  # 0 centre .. 0.707 corner
    if rough:
        d = d + (fbm(w, h, seed, 3, 2) - 0.5) * rough
    r = np.sqrt(np.clip(tone * gain, 0, 1) / math.pi) * 1.0   # dot radius in cell units for area = tone
    r = np.where(tone > 0.78, r + (tone - 0.78) * 1.2, r)
    return np.clip((r - d) * cell * 1.2 + 0.5, 0, 1).astype(np.float32)


def riso_ink(cov, col, seed, grain=0.35, starve=0.25):
    """Soy ink on uncoated stock: speckled grain, roller starvation streaks, slightly translucent."""
    h, w = cov.shape
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.55)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    st = fbm(w, h, seed + 4, 60, 2)
    band = gaussian_filter(np.random.default_rng(seed + 9).random((1, w)).astype(np.float32), (0, 18))
    band = (band - band.min()) / (band.max() - band.min() + 1e-6)
    a = cov * (1 - grain * np.clip((g - 0.55) * 3, 0, 1)) * (1 - starve * np.clip(st * 0.7 + band * 0.6 - 0.55, 0, 1))
    a = np.clip(a * 0.94, 0, 1)
    return np.concatenate([rgb_arr(h, w, col), a[..., None]], -1)


def multiply_stack(layers, w, h):
    """Composite riso plates as multiply over white, returning RGBA where alpha = darkness (for CSS mix-blend multiply)."""
    rgb = np.ones((h, w, 3), np.float32)
    for L in layers:
        a = L[..., 3:4]
        rgb = rgb * (1 - a + a * L[..., :3])
    # convert to RGBA over white: choose alpha = 1 - min channel ratio, colour = solved
    dark = 1 - rgb.min(-1, keepdims=True)
    a = np.clip(dark * 1.25, 0, 1)
    col = 1 - (1 - rgb) / np.maximum(a, 1e-4)
    return np.concatenate([np.clip(col, 0, 1), a], -1)


def shift(mask, dx, dy):
    return ndimage.shift(mask, (dy, dx), order=1, mode="constant")


# ---------- stained glass ----------
def glass_panes(lead, colour_of, seed, W, H, bubbles=0.0006, tint=0.1, streak=0.7):
    """Fill every enclosed region of the (binary-ish) lead mask with cathedral glass.
    colour_of(cx, cy, area) -> (hex, hex2) chooses the pane colour from its centroid."""
    free = lead < 0.35
    lab, n = ndimage.label(free)
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rgb = np.zeros((H, W, 3), np.float32)
    alpha = np.zeros((H, W), np.float32)
    objs = ndimage.find_objects(lab)
    cents = ndimage.center_of_mass(free, lab, range(1, n + 1))
    areas = ndimage.sum(free, lab, range(1, n + 1))
    tex = fbm(W, H, seed + 1, 40, 4)
    tex2 = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.8, 9.0))
    tex2 = (tex2 - tex2.min()) / (tex2.max() - tex2.min() + 1e-6)
    for i, sl in enumerate(objs):
        if sl is None or sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == H or sl[1].stop == W:
            continue
        cy, cx = cents[i]
        reg = lab[sl] == i + 1
        try:
            res = colour_of(cx, cy, areas[i], sl, reg)
        except TypeError:
            res = colour_of(cx, cy, areas[i])
        if res is None:
            continue
        ca, cb = res
        A = np.array(hex_rgb(ca), np.float32); B = np.array(hex_rgb(cb), np.float32)
        # each pane: its own gradient direction + mottled density (hand-rolled glass)
        ang = rng.uniform(0, math.tau)
        gy, gx = yy[sl] - cy, xx[sl] - cx
        span = max(8.0, math.sqrt(areas[i]))
        g = np.clip(0.5 + (gx * math.cos(ang) + gy * math.sin(ang)) / span * 0.6, 0, 1)
        t = np.clip(g * 0.75 + tex[sl] * 0.35 - 0.05, 0, 1)[..., None]
        c = A * (1 - t) + B * t
        lum = 1 + (tex[sl] - 0.5) * tint * 2 + (tex2[sl] - 0.5) * 0.16 * streak
        # edge darkening towards the came (thicker glass at the rim)
        rgb[sl][reg] = 0
        sub = rgb[sl]; sub[reg] = (c * lum[..., None])[reg]
        alpha[sl][reg] = 1
    # rim darkening and inner glow
    dist = ndimage.distance_transform_edt(free)
    rim = np.clip(1 - dist / 9.0, 0, 1)
    rgb *= (1 - rim * 0.35)[..., None]
    # bubbles / seeds
    nb = int(W * H * bubbles)
    bub = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.7, 2.2)) for _ in range(nb)])
    ring_ = np.clip(gaussian_filter(bub, 0.9) * 1.3 - bub, 0, 1)
    rgb = rgb * (1 - ring_[..., None] * 0.35) + bub[..., None] * 0.07
    return np.clip(rgb, 0, 1), alpha * (free > 0)


def lead_render(lead, seed, col="#2b2724", hi="#8a8379"):
    """Lead came: dark matte strip with a soft rounded highlight and solder blobs."""
    h, w = lead.shape
    m = np.clip(gaussian_filter(lead, 0.6), 0, 1)
    hi_, lo_ = emboss_light(m, 1.2, 1.2, ang=(-0.6, -0.8))
    tone = fbm(w, h, seed, 14, 2)
    rgb = rgb_arr(h, w, col) * (0.85 + 0.3 * tone)[..., None]
    rgb = rgb * (1 - lo_[..., None] * 0.3) + np.array(hex_rgb(hi), np.float32) * hi_[..., None] * 0.55
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)
