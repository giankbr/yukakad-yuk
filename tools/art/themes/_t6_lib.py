"""Agent T6 helpers (kamelia-syari, lentera-terbang, kebun-apel, malam-puisi).
Builds on _a2_lib (-> _j1_lib / _p1_lib / art: bbox-cropped G/GP/LC/FO/OV, batched strokes/shapes). Adds gouache
camellias + glossy leaves, sky lanterns, apples/orchard trees, candles and warm-light helpers.
Previews -> /tmp/pen/nb-T6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *  # noqa
import _p1_lib
import art as _art
from scipy.ndimage import map_coordinates  # noqa

PREV = "/tmp/pen/nb-T6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def yx(W, H):
    return np.mgrid[0:H, 0:W].astype(np.float32)


def ell(W, H, cx, cy, rx, ry, rot=0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def poly(W, H, pts, smooth=False):
    return shapes(W, H, [pts], smooth=smooth)


def line(W, H, pts, width, taper=(0.15, 0.25)):
    return strokes(W, H, [(pts, width, taper)])


def prev(arr, name, tone="#fbf6ee", bg=None):
    preview(arr, name, tone=tone, bg=bg)


def soft(mask, s):
    return gaussian_filter(mask, s)


# ---------------------------------------------------------------- camellia (gouache)
def camellia(art, W, H, cx, cy, r, rng, nx, pal, tilt=0.9, rot=None, area=None, rings=(7, 6, 5), open_=1.0, stamens=False):
    """Formal double camellia in gouache: neat rings of broad rounded petals painted back to front; each petal gets a
    deeper base, a lighter turned rim and two or three fine vein strokes. pal = (light, mid, deep, rim)."""
    light, mid, deep, rim = pal
    rot = rng.uniform(0, math.tau) if rot is None else rot
    allm = np.zeros((H, W), np.float32)
    nr = len(rings)
    for ri, n in enumerate(rings):
        t_r = ri / max(1, nr - 1)
        r1 = r * (1.0 - 0.24 * ri) * open_ ** (0.4 * (1 - t_r))
        r0 = r1 * 0.12
        span = math.tau / n * (1.05 + 0.1 * (1 - t_r))
        off = rot + ri * 0.41
        order = list(range(n))
        rng.shuffle(order)
        for k in order:
            a = off + k * math.tau / n + rng.uniform(-.07, .07)
            rr1 = r1 * rng.uniform(0.92, 1.04)
            pts = [(cx + math.cos(a) * r0, cy + math.sin(a) * r0 * tilt)]
            for i in range(25):
                u = i / 24 * 2 - 1
                prof = math.sqrt(max(0.0, 1 - u * u)) ** 0.45
                notch = 1 - 0.05 * math.exp(-(u * 6) ** 2)
                rad = r0 + (rr1 - r0) * prof * notch
                th = a + u * span * 0.62
                pts.append((cx + math.cos(th) * rad, cy + math.sin(th) * rad * tilt))
            m = shape_mask(W, H, pts)
            sh = np.clip(soft(m, r * 0.035) * 1.4 - m, 0, 1)
            art = OV(art, sh * allm, lambda mm: rgba(deep, np.clip(mm, 0, 1) * 0.55))
            np.maximum(allm, m, out=allm)
            c1 = mix(light, mid, 0.15 + 0.6 * t_r + rng.uniform(-.1, .1))
            art = GP(art, m, c1, mix(c1, light, .35), seed=nx(), rough=1.1, streak=0.3)
            base = soft(circles(W, H, [(cx, cy, r1 * 0.55)]), r1 * 0.16) * m
            art = OV(art, base, lambda mm: rgba(deep, mm * (0.55 + 0.2 * t_r)))
            # turned rim catching light on the far edge
            edge = np.clip(m - soft(m, 2.2) * 1.15, 0, 1)
            tip = np.clip(m - circles(W, H, [(cx, cy, r1 * 0.78)]), 0, 1)
            art = OV(art, soft(edge * tip, 0.8) + soft(tip, 3) * 0.25 * m, lambda mm: rgba(rim, np.clip(mm, 0, 1) * 0.7))
            vs = []
            for dv in (-0.22, 0.0, 0.24):
                th = a + dv * span
                vs.append(([(cx + math.cos(th) * r0 * 1.6, cy + math.sin(th) * r0 * 1.6 * tilt),
                            (cx + math.cos(th + dv * .1) * rr1 * .62, cy + math.sin(th + dv * .1) * rr1 * .62 * tilt)], max(0.8, r * 0.011), (0.1, 0.6)))
            art = OV(art, strokes(W, H, vs) * m, lambda mm: rgba(deep, mm * 0.28))
    if stamens:
        fil, anth = [], []
        for k in range(46):
            a = rng.uniform(0, math.tau); d = r * rng.uniform(0.05, 0.27)
            ex, ey = cx + math.cos(a) * d, cy + math.sin(a) * d * tilt - r * 0.04
            fil.append(([(cx + math.cos(a) * d * .2, cy + math.sin(a) * d * .2 * tilt + r * .03), (ex, ey)], max(1.0, r * 0.012), (0.0, 0.3)))
            anth.append((ex, ey, r * rng.uniform(0.022, 0.034)))
        art = OV(art, soft(circles(W, H, [(cx, cy, r * 0.3)]), r * 0.06), lambda mm: rgba(deep, mm * 0.5))
        art = GP(art, strokes(W, H, fil), "#f6ecc9", "#e9d59a", seed=nx(), rough=0.4, streak=0.2)
        am = circles(W, H, anth)
        art = FO(art, am, "#d9a93c", seed=nx(), emboss=0.5, sparkle=0.2)
        art = OV(art, np.clip(am - soft(am, 1) * 1.1, 0, 1), lambda mm: rgba("#8a5a14", mm * .6))
        if area is not None:
            np.maximum(area, allm, out=area)
        return art
    # tight heart
    heart = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * 0.2, r * 0.18 * tilt, 9, rot), rng, 1, 0.08))
    art = GP(art, heart, mid, deep, seed=nx(), rough=0.8, streak=0.6)
    art = OV(art, np.clip(heart - soft(heart, 2) * 1.2, 0, 1), lambda mm: rgba(rim, mm * 0.6))
    if area is not None:
        np.maximum(area, allm, out=area)
    return art


def leaf_outline(x, y, L, ang, wd, n=22, tooth=0.0):
    """Elliptic leaf with an acuminate tip: widest a little below the middle, tapered base."""
    ca, sa = math.cos(ang), math.sin(ang)
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        w = L * wd * 0.5 * (math.sin(math.pi * t) ** 0.75) * (1 - 0.35 * t) * (1 + 0.15 * (1 - t))
        if tooth and 0.15 < t < 0.92 and i % 2:
            w *= 1 + tooth
        px, py = x + ca * L * t, y + sa * L * t
        left.append((px - sa * w, py + ca * w)); right.append((px + sa * w, py - ca * w))
    return left + right[::-1]


def glossy_leaf(art, W, H, x, y, L, ang, rng, nx, pal, wd=0.44, area=None, gloss=0.5, fold=None):
    """Camellia leaf: thick, elliptic, acuminate tip, finely toothed margin, waxy highlight. pal=(light, mid, dark, vein)."""
    light, mid, dark, vein = pal
    m = shape_mask(W, H, deform(leaf_outline(x, y, L, ang, wd, 26, 0.035), rng, 1, 0.012), smooth=False)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, mid, mix(mid, dark, .35), seed=nx(), rough=0.9, streak=0.35)
    fold = rng.choice((-1, 1)) if fold is None else fold
    ca, sa = math.cos(ang), math.sin(ang)
    hp = [(x + ca * L * t, y + sa * L * t) for t in (0, 1)]
    half = leaf_outline(x, y, L, ang, wd, 18)
    half = (half[:19] + [hp[0]]) if fold > 0 else (half[19:] + [hp[0]])
    hm = shape_mask(W, H, half, smooth=False) * m
    art = OV(art, soft(hm, 1.2), lambda mm: rgba(dark, mm * 0.75))
    # waxy shine on the lit half
    ox, oy = -sa * L * wd * 0.17 * -fold, ca * L * wd * 0.17 * -fold
    band = [(x + ca * L * t + ox, y + sa * L * t + oy) for t in (0.15, 0.35, 0.55, 0.72)]
    sh = soft(strokes(W, H, [(band, L * wd * 0.2, (0.4, 0.5))]), L * 0.03) * m
    art = OV(art, sh, lambda mm: rgba(light, np.clip(mm * 1.5, 0, 1) * gloss))
    vs = [([(x + ca * L * t, y + sa * L * t) for t in [j / 10 for j in range(0, 10)]], max(1.0, L * 0.016), (0.02, 0.7))]
    for t in (0.22, 0.38, 0.54, 0.68):
        px, py = x + ca * L * t, y + sa * L * t
        for side in (-1, 1):
            aa = ang + side * 0.8
            q = L * wd * 0.36
            vs.append(([(px, py), (px + math.cos(aa) * q * .55 + ca * q * .3, py + math.sin(aa) * q * .55 + sa * q * .3),
                        (px + math.cos(aa) * q + ca * q * .8, py + math.sin(aa) * q + sa * q * .8)], max(0.6, L * 0.006), (0.1, 0.7)))
    art = OV(art, strokes(W, H, vs) * m, lambda mm: rgba(vein, mm * 0.5))
    rimm = np.clip(m - soft(m, 1.3) * 1.25, 0, 1)
    art = OV(art, rimm, lambda mm: rgba(dark, mm * 0.6))
    return art


def cam_bud(art, W, H, x, y, s, ang, rng, nx, pal, leafpal):
    light, mid, deep, rim = pal
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 1.5, s * 0.85, ang, n=14), rng, 1, 0.05))
    art = GP(art, m, mid, deep, seed=nx(), rough=0.9, streak=0.3)
    art = OV(art, soft(np.clip(m - soft(m, 2) * 1.2, 0, 1), .7), lambda mm: rgba(rim, mm * .6))
    seps = []
    for d in (-0.55, 0.0, 0.55):
        aa = ang + d
        seps.append(petal_pts(x, y, s * 0.8, s * 0.42, aa, n=10))
    sm = shapes(W, H, seps)
    art = GP(art, sm, leafpal[1], leafpal[2], seed=nx(), rough=0.8, streak=0.8)
    return art


def twig(art, W, H, pts, width, nx, col="#4d3527", col2="#6b4b36"):
    m = strokes(W, H, [(curve(pts, 50), width, (0.0, 0.7))])
    return GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.4)


# ---------------------------------------------------------------- light
def radial(W, H, cx, cy, rx, ry=None):
    yy, xx = yx(W, H)
    ry = ry or rx
    return np.clip(1 - np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0, 1)


def add_light(arr, mask, col, amt=1.0):
    """Additive warm light (screen-like) onto an opaque or transparent layer."""
    c = np.array(hex_rgb(col), np.float32)
    out = arr.copy()
    k = np.clip(mask * amt, 0, 1)[..., None]
    out[..., :3] = 1 - (1 - out[..., :3]) * (1 - c * k)
    out[..., 3:4] = np.maximum(out[..., 3:4], k[..., :1] * 0.0 + out[..., 3:4])
    return out


# ---------------------------------------------------------------- orchard (gouache, playful)
def apple(art, W, H, cx, cy, r, rng, nx, red=("#d8342c", "#a81d22"), blush="#f2a23a", leaf=True, ang=0.0, area=None):
    """Gouache apple: round body with a shoulder dimple, streaky yellow-red blush, soft highlight, stem and leaf."""
    pts = []
    for i in range(40):
        a = i / 40 * math.tau
        rr = r * (1 + 0.06 * math.cos(2 * a) - 0.05 * math.exp(-((a - 1.5 * math.pi) % math.tau - 0) ** 2 * 0) )
        dim = 0.2 * math.exp(-(((a - 1.5 * math.pi + math.pi) % math.tau - math.pi) / 0.45) ** 2)
        x = math.cos(a) * rr * 1.04
        y = math.sin(a) * rr * (1 - dim) * 0.96
        if math.sin(a) > 0:
            x *= 1 - 0.08 * math.sin(a)
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    m = shape_mask(W, H, pts)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, red[0], red[1], seed=nx(), rough=1.0, streak=0.6, pad=8)
    # vertical blush streaks
    st = []
    for k in range(7):
        x = cx + rng.uniform(-0.75, 0.75) * r
        st.append(([(x, cy - r * 0.7), (x + rng.uniform(-.1, .1) * r, cy + r * 0.6)], r * rng.uniform(0.08, 0.16), (0.3, 0.3)))
    art = OV(art, soft(strokes(W, H, st), r * 0.06) * m, lambda mm: rgba(blush, mm * 0.32), pad=8)
    art = OV(art, soft(circles(W, H, [(cx + r * 0.25, cy + r * 0.3, r * 0.75)]), r * 0.25) * m, lambda mm: rgba(red[1], mm * 0.55), pad=8)
    hl = strokes(W, H, [(arc_pts(cx, cy, r * 0.66, math.pi * 1.08, math.pi * 1.38, 10), r * 0.13, (0.35, 0.35))]) * m
    art = GP(art, hl, "#ffd9c8", "#ffeede", seed=nx(), rough=0.5, streak=0.3, density=0.75, pad=6)
    sx, sy = cx + math.sin(ang) * r * 0.82, cy - math.cos(ang) * r * 0.82
    stem = strokes(W, H, [([(sx, sy + r * 0.12), (sx + r * 0.08, sy - r * 0.25), (sx + r * 0.2, sy - r * 0.45)], max(1.2, r * 0.1), (0.0, 0.5))])
    art = GP(art, stem, "#5a3a22", "#7a5030", seed=nx(), rough=0.5, streak=0.3, pad=6)
    if leaf:
        lx, ly = sx + r * 0.12, sy - r * 0.3
        lm = shape_mask(W, H, leaf_outline(lx, ly, r * 1.0, -0.5 + rng.uniform(-.3, .3), 0.46, 16))
        art = GP(art, lm, "#6aa140", "#3f7a2e", seed=nx(), rough=0.8, streak=0.4, pad=6)
        art = OV(art, strokes(W, H, [([(lx, ly), (lx + math.cos(-0.5) * r * 0.75, ly + math.sin(-0.5) * r * 0.75)], max(0.8, r * 0.04), (0.1, 0.5))]) * lm, lambda mm: rgba("#d8eaa8", mm * .7), pad=6)
    return art


def dab_canopy(art, W, H, cx, cy, rx, ry, rng, nx, greens=("#4f8a3a", "#346b2f", "#7bb04a", "#25502a"), dabs=260, area=None):
    """Tree canopy painted as a cloudy silhouette + many leaf dabs (short gouache comma strokes)."""
    blobs = [(cx + rng.gauss(0, rx * 0.45), cy + rng.gauss(0, ry * 0.4), rx * rng.uniform(0.35, 0.6), ry * rng.uniform(0.35, 0.6), 0) for _ in range(9)]
    blobs.append((cx, cy, rx * 0.8, ry * 0.8, 0))
    m = ellipses(W, H, blobs)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, greens[1], greens[3], seed=nx(), rough=3.0, streak=0.5)
    yy, xx = yx(W, H)
    for col, frac, shift in ((greens[0], 0.55, -0.2), (greens[2], 0.3, -0.45)):
        items = []
        for _ in range(int(dabs * frac)):
            a = rng.uniform(0, math.tau); d = rng.random() ** 0.6
            x = cx + math.cos(a) * rx * 1.0 * d + shift * rx * 0.3
            y = cy + math.sin(a) * ry * 0.95 * d + shift * ry * 0.5
            L = rx * rng.uniform(0.05, 0.085)
            items.append((x, y, L, L * 0.55, rng.uniform(-60, 60)))
        art = GP(art, ellipses(W, H, items) * m, col, mix(col, greens[3], .2), seed=nx(), rough=0.8, streak=0.3)
    return art
