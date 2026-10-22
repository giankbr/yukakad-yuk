"""Agent C1 helpers (bengkulu-rafflesia, maluku-tifa, sumbawa-samawa, buton-wolio): builds on _b1_lib (bbox-cropped
painting, weave_cells, silk_plaid) with gouache-scene helpers (soft tonal washes, leaves, grass, stone courses, plank
walls, shingle roofs) and thread-level textiles: warp ikat with dye bleed along the warp (tenun Tanimbar), weft stripes
(tenun Buton). Previews -> /tmp/pen/nb-C1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _b1_lib import *  # noqa
import _b1_lib, _a1_lib, _p1_lib
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-C1/art"
os.makedirs(PREV, exist_ok=True)
_b1_lib.PREV = PREV
_p1_lib.PREV = PREV
_a1_lib.PREV = PREV


def show(arr, name, bg=None, tone="#f4ecdf"):
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * col_arr(bg)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def wash(dst, m, col, amt=0.5, seed=1, streak=0.6, col2=None):
    """Soft opaque tonal wash (gouache shading/glazing): alpha = m*amt, brush-streak texture, no hard threshold."""
    b = bbox(m, 2, 0.002)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    mm = np.ascontiguousarray(m[y0:y1, x0:x1])
    h, w = mm.shape
    ca = col_arr(col); cb = col_arr(col2 or col)
    t = fbm(w, h, seed + 3, 70, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.5, 4.0))
    s = (s - s.mean()) / (s.std() + 1e-6)
    rgb = np.clip(rgb * (1 + s[..., None] * 0.04 * streak), 0, 1)
    src = np.concatenate([rgb, np.clip(mm * amt, 0, 1)[..., None]], -1)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], src)
    return out


def grad(W, H, x0, y0, x1, y1):
    """Linear ramp 0 at (x0,y0) → 1 at (x1,y1)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy + 1e-6
    return np.clip(((xx - x0) * dx + (yy - y0) * dy) / L2, 0, 1)


def radial(W, H, cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1)


def leaf_pts(x, y, L, Wd, ang, n=18, tip=1.0, asym=0.0):
    """Elongated tropical leaf from its base (x,y) along ang: broad middle, drip tip."""
    pts = []
    for i in range(n + 1):
        t = i / n
        w = Wd * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t ** 3 * tip)
        pts.append((t * L, w * (1 + asym)))
    for i in range(n, -1, -1):
        t = i / n
        w = Wd * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t ** 3 * tip)
        pts.append((t * L, -w * (1 - asym)))
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + u * ca - v * sa, y + u * sa + v * ca) for u, v in pts]


def jungle_leaf(art, W, H, x, y, L, Wd, ang, rng, nx, cols=("#2e5a3a", "#21452d"), vein="#173322", light="#6f9a62", bend=0.0):
    """Gouache jungle leaf: body, shaded half, midrib and side veins, lit rim."""
    pts = leaf_pts(x, y, L, Wd, ang, asym=rng.uniform(-0.1, 0.1))
    if bend:
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(px + (-sa) * bend * ((px - x) * ca + (py - y) * sa) ** 2 / L, py + ca * bend * ((px - x) * ca + (py - y) * sa) ** 2 / L) for px, py in pts]
    m = shapes(W, H, [deform(pts, rng, 2, 0.007)])
    art = GP(art, m, cols[0], cols[1], seed=nx(), rough=2.6, streak=1.0)
    art = wash(art, m * np.clip((fbm(W, H, nx(), max(8, L * 0.12), 3) - 0.5) * 2.5, 0, 1), light, 0.25, seed=nx())
    art = wash(art, m * np.clip((0.45 - fbm(W, H, nx(), max(8, L * 0.1), 3)) * 2.5, 0, 1), vein, 0.3, seed=nx())
    art = wash(art, np.clip(m - gaussian_filter(m, max(1.5, Wd * 0.08)), 0, 1) * 2.5, vein, 0.55, seed=nx())
    # half of the leaf turned from the light
    ca, sa = math.cos(ang), math.sin(ang)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = ((xx - x) * (-sa) + (yy - y) * ca) > 0
    art = wash(art, m * side * 0.9, vein, 0.32, seed=nx())
    art = wash(art, m * (1 - side) * grad(W, H, x, y, x + ca * L, y + sa * L), light, 0.22, seed=nx())
    def bp(t, off=0.0):
        u = t * L
        px, py = x + u * ca - off * sa, y + u * sa + off * ca
        if bend:
            px += -sa * bend * u * u / L; py += ca * bend * u * u / L
        return (px, py)
    items = [([bp(t) for t in np.linspace(0, 0.97, 16)], max(1.2, Wd * 0.07), (0.0, 0.6))]
    for k in range(1, 9):
        t = k / 10
        wl = Wd * math.sin(math.pi * t) ** 0.85 * 0.85
        for sgn in (-1, 1):
            items.append(([bp(t), bp(t + 0.07, sgn * wl * 0.5), bp(t + 0.12, sgn * wl)], max(0.6, Wd * 0.025), (0.0, 0.6)))
    v = strokes(W, H, items) * m
    art = wash(art, v, light, 0.45, seed=nx())
    # dry-brush sheen strokes along the blade on the lit half
    dry = []
    for _ in range(int(6 + L / 25)):
        t0 = rng.uniform(0.1, 0.7); off = rng.uniform(-0.6, 0.6) * Wd * math.sin(math.pi * (t0 + 0.1))
        dry.append(([bp(t0, off), bp(t0 + rng.uniform(0.08, 0.2), off * 0.9)], max(0.8, Wd * 0.05), (0.3, 0.5)))
    dm = strokes(W, H, dry) * m * (np.random.default_rng(nx()).random((H, W)) > 0.35)
    art = wash(art, gaussian_filter(dm.astype(np.float32), 0.5), "#a9c48e", 0.3, seed=nx())
    return art


def fern_frond(art, W, H, pts, size, rng, nx, cols=("#3d6b44", "#2a5233")):
    """Pinnate frond (pakis): many tapered leaflets along a curved rachis."""
    items = [(pts, size * 0.08, (0.0, 0.6))]
    n = len(pts)
    for i in range(2, n - 1):
        t = i / n
        x, y = pts[i]
        dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) + 1e-6
        nxv, nyv = -dy / L, dx / L
        ln = size * (1 - t) ** 0.7 * rng.uniform(0.85, 1.1)
        for sgn in (-1, 1):
            items.append(([(x, y), (x + (nxv * sgn * 0.7 + dx / L * 0.5) * ln, y + (nyv * sgn * 0.7 + dy / L * 0.5) * ln)], size * 0.16 * (1 - t * 0.6), (0.05, 0.7)))
    m = strokes(W, H, items)
    return GP(art, m, cols[0], cols[1], seed=nx(), rough=1.2, streak=0.6)


def grass_tufts(W, H, y0, y1, n, rng, hmin=10, hmax=40, lean=0.3, width=2.0):
    items = []
    for _ in range(n):
        x = rng.uniform(-10, W + 10); y = rng.uniform(y0, y1)
        t = (y - y0) / max(1, y1 - y0)
        hgt = hmin + (hmax - hmin) * t * rng.uniform(0.6, 1.2)
        lx = rng.gauss(lean, 0.35) * hgt
        items.append(([(x, y), (x + lx * 0.4, y - hgt * 0.55), (x + lx, y - hgt)], width * (0.6 + t), (0.0, 0.8)))
    return strokes(W, H, items)


def planks(W, H, m, x0, x1, pitch, seed=1, vertical=True):
    """Thin plank seams inside mask m (vertical boards)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = (fbm(W, H, seed, 30, 2) - 0.5) * 1.5
    u = ((xx if vertical else yy) + n) / pitch
    f = np.abs((u % 1.0) - 0.5) * 2
    return np.clip((0.12 - (1 - f)) / 0.08 + 1, 0, 1) * 0 + np.clip(((1 - f) - 0.9) / 0.1, 0, 1) * m


def stone_courses(W, H, m, course=14, brick=34, seed=1, jitter=0.35):
    """Mortar lines of an irregular coursed stone wall inside mask m. Returns (mortar, stone_tone) fields."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nyy = yy + (fbm(W, H, seed, 40, 2) - 0.5) * course * 0.6
    row = np.floor(nyy / course)
    fy = (nyy / course) % 1.0
    off = _b1_lib._hash(row) * brick
    bw = brick * (0.7 + 0.6 * _b1_lib._hash(row * 3.1))
    u = (xx + off + (fbm(W, H, seed + 1, 20, 2) - 0.5) * 6) / bw
    col = np.floor(u)
    fx = u % 1.0
    mort = np.maximum(np.clip((0.12 - np.minimum(fy, 1 - fy)) / 0.08, 0, 1), np.clip((0.06 - np.minimum(fx, 1 - fx)) / 0.05, 0, 1))
    tone = _b1_lib._hash(row * 17.0 + col * 7.3)
    return mort * m, tone * m


def ikat(W, H, motif, palette, seed=1, warp=3, bleed=9.0, base_idx=0):
    """Warp ikat (tenun ikat Tanimbar), thread level. `motif` (H x W ints, palette indices) is the design as tied; dye
    bleeds along the warp (vertical) with a per-thread offset so every motif edge is feathered and stepped; warp-faced
    plain weave: vertical threads with round profiles, fine weft shows only as tiny horizontal ticks. Opaque RGBA."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    th = (xx // warp).astype(np.int32)
    nth = W // warp + 1
    shift = rng.normal(0, bleed * 0.45, nth).astype(np.float32)
    shift = gaussian_filter(shift, 0.6, mode="wrap") + rng.normal(0, bleed * 0.25, nth)
    sy = (yy + shift[th]) % H
    # per-thread wiggle (warp tension)
    sy = (sy + (fbm(W, H, seed + 4, 60, 2) - 0.5) * bleed * 0.6) % H
    sx = (th * warp + warp / 2).astype(np.float32) % W
    pal = np.array([hex_rgb(c) for c in palette], np.float32)
    idx = motif[sy.astype(np.int32) % H, sx.astype(np.int32) % W]
    rgb = pal[idx]
    # dye bleed: soft colour transition at motif boundaries along the warp
    soft = np.zeros_like(rgb)
    for k in range(3):
        soft[..., k] = gaussian_filter(rgb[..., k], (bleed * 0.25, 0.01), mode="wrap")
    rgb = rgb * 0.6 + soft * 0.4
    fx = (xx % warp + 0.5) / warp
    prof = np.sin(fx * math.pi) ** 0.6
    lum = 0.7 + 0.34 * prof
    tick = ((yy.astype(np.int32) + th) % 4 == 0).astype(np.float32)
    lum *= 1 - 0.12 * tick * (1 - prof)
    tv = _b1_lib._hash(th.astype(np.float32) * 1.7)
    lum *= 0.94 + 0.1 * tv
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (3.0, 0.35), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    lum *= 1 + 0.05 * fib
    out = rgb * lum[..., None]
    return np.concatenate([np.clip(out, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def sun_glints(W, H, x, y0, y1, n, rng, spread=60, col="#fff1d0"):
    items = []
    for _ in range(n):
        yy = rng.uniform(y0, y1); t = (yy - y0) / max(1, y1 - y0)
        xx = x + rng.gauss(0, spread * (0.4 + t))
        L = rng.uniform(8, 30) * (0.5 + t)
        items.append(([(xx - L / 2, yy), (xx + L / 2, yy)], rng.uniform(1.2, 2.6) * (0.6 + t), (0.3, 0.3)))
    return strokes(W, H, items)


def relief(art, m, blur, amt=0.5, light="#ffd9b0", dark="#2a0c08", lx=-0.7, ly=-0.7, seed=1):
    """Dome shading of a shape from its blurred mask (height field) lit from (lx, ly)."""
    hgt = gaussian_filter(m, blur)
    gy, gx = np.gradient(hgt)
    sh = -(gx * lx + gy * ly)
    sh = sh / (np.abs(sh).max() + 1e-6)
    art = wash(art, np.clip(sh, 0, 1) * m, light, amt, seed=seed)
    art = wash(art, np.clip(-sh, 0, 1) * m, dark, amt, seed=seed + 1)
    return art
