"""Agent I6 helpers (linocut-bunga, nautika-biru, bunga-matahari, seminar-ilmiah): _a6_lib (bbox-local gouache /
watercolour / linocut, tint, side_light) + relief-print ink with paper tooth and roller drift, gouge cuts,
thick impasto gouache, rope twist and brass shading. Previews -> /tmp/pen/nb-I6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *  # noqa
import _p1_lib, _j1_lib, _a6_lib
import art as _art
PREV = "/tmp/pen/nb-I6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_a6_lib.PREV = PREV


def P(x, y, ang, u, v):
    ca, sa = math.cos(ang), math.sin(ang)
    return (x + u * ca - v * sa, y + u * sa + v * ca)


# ---------------------------------------------------------------- relief print
def print_ink(dst, mask, col, seed=1, wear=0.32, roller=0.22, tooth=0.35, rough=1.6, pad=10):
    """Relief-print ink: linocut() + paper tooth (fine speckle where the paper didn't take ink) + roller drift
    (broad lighter bands) so a flat block never looks like a vector fill."""
    def fn(m):
        h, w = m.shape
        a = linocut(m, col, seed=seed, wear=wear, rough=rough)
        t = gaussian_filter(np.random.default_rng(seed + 31).random((h, w)).astype(np.float32), 0.55)
        t = (t - t.min()) / (t.max() - t.min() + 1e-6)
        cov = 1 - tooth * np.clip((t - 0.62) * 3.2, 0, 1)
        yy = np.mgrid[0:h, 0:w][0].astype(np.float32)
        band = fbm(w, h, seed + 41, 90, 2)
        rol = 1 - roller * np.clip((band - 0.45) * 1.6, 0, 1) * (0.6 + 0.4 * np.sin(yy / 23.0 + band * 4))
        a[..., 3] *= np.clip(cov * rol, 0, 1)
        return a
    return OV(dst, mask, fn, pad=pad)


def gouges(W, H, rng, region, n, L=(10, 22), wd=(2.0, 4.0), ang=0.0, angj=0.5, thr=0.5, curve=0.25):
    """Short crescent V-gouge cuts scattered where region > thr. Returns a mask (to subtract from a block)."""
    items = []
    tries = 0
    while len(items) < n and tries < n * 30:
        tries += 1
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if region[int(min(H - 1, y)), int(min(W - 1, x))] < thr:
            continue
        a = ang + rng.uniform(-angj, angj)
        l = rng.uniform(*L); bend = rng.uniform(-curve, curve) * l
        pts = [P(x, y, a, l * (t - 0.5), bend * (1 - (2 * t - 1) ** 2)) for t in np.linspace(0, 1, 7)]
        items.append((pts, rng.uniform(*wd), (0.4, 0.45)))
    return strokes(W, H, items)


def cut_lines(mask, angle, spacing, duty=0.32, seed=1, wob=1.4):
    """Parallel carved lines inside a mask (hatch from _j1_lib)."""
    h, w = mask.shape
    return hatch(w, h, angle, spacing, duty, seed, wob) * mask


def radial_cuts(W, H, cx, cy, r0, r1, n, wd, rng, a0=0.0, jitter=0.12):
    items = []
    for i in range(n):
        a = a0 + i / n * 2 * math.pi + rng.uniform(-jitter, jitter)
        rr1 = r1 * rng.uniform(0.75, 1.0)
        items.append(([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * (r0 + rr1) / 2, cy + math.sin(a) * (r0 + rr1) / 2),
                       (cx + math.cos(a) * rr1, cy + math.sin(a) * rr1)], wd * rng.uniform(0.7, 1.2), (0.1, 0.6)))
    return strokes(W, H, items)


def paper_rgba(W, H, tone, seed=3):
    a = np.asarray(paper(W, H, tone, seed), np.float32) / 255
    return np.concatenate([a[..., :3], np.ones((H, W, 1), np.float32)], -1)


# ---------------------------------------------------------------- impasto gouache
def impasto(dst, mask, col, col2=None, seed=1, rough=2.4, ridge=0.5, dirn=0.0, pad=16, streak=0.9):
    """Thick gouache: gouache_paint + directional bristle ridges with a lit/shadow side so the paint has body."""
    def fn(m):
        h, w = m.shape
        a = gouache_paint(m, col, col2, seed=seed, rough=rough, streak=streak)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        u = xx * math.cos(dirn) + yy * math.sin(dirn)
        v = -xx * math.sin(dirn) + yy * math.cos(dirn)
        n = fbm(w, h, seed + 17, 14, 2)
        bristle = np.sin(v * 0.9 + n * 9 + np.sin(u * 0.05) * 2)
        b2 = gaussian_filter(np.random.default_rng(seed + 3).random((h, w)).astype(np.float32), (0.6, 3.5) if abs(math.sin(dirn)) < .7 else (3.5, .6))
        b2 = (b2 - b2.mean()) / (b2.std() + 1e-6)
        k = 1 + (bristle * 0.04 + b2 * 0.05) * ridge
        a[..., :3] = np.clip(a[..., :3] * k[..., None], 0, 1)
        return a
    return OV(dst, mask, fn, pad=pad)


def daub(dst, W, H, items, col, col2=None, seed=1, ridge=0.6):
    """Many short loaded-brush dabs (pts, width) in one colour: thick, overlapping strokes."""
    m = strokes(W, H, items)
    return impasto(dst, m, col, col2, seed=seed, rough=1.8, ridge=ridge)


# ---------------------------------------------------------------- brass / rope
def brass(dst, mask, base="#b8893a", seed=1, light=(-1, -1), amt=0.55, pad=10):
    """Polished brass: gouache base + soft specular streak + shaded side (painted, not chrome)."""
    def fn(m):
        h, w = m.shape
        a = gouache_paint(m, base, mix(base, "#e9cf8a", 0.5), seed=seed, rough=1.0, streak=0.5)
        gy, gx = np.gradient(gaussian_filter(m, 3.0))
        sh = np.clip(-(gx * light[0] + gy * light[1]) * 14, -1, 1)
        rgb = a[..., :3]
        hi = np.array(hex_rgb("#fbe9b6"), np.float32); lo = np.array(hex_rgb("#5a3d14"), np.float32)
        pos = np.clip(sh, 0, 1)[..., None] * amt; neg = np.clip(-sh, 0, 1)[..., None] * amt
        rgb = rgb * (1 - pos) + hi * pos
        rgb = rgb * (1 - neg) + lo * neg
        a[..., :3] = np.clip(rgb, 0, 1)
        return a
    return OV(dst, mask, fn, pad=pad)


def rope(dst, W, H, pts, width, seed=1, col="#d9c39a", dark="#8a6a3e", step=None, twist=0.9):
    """Twisted 3-strand rope along a polyline: base stroke + diagonal strand segments with shadows."""
    pts = [(float(p[0]), float(p[1])) for p in along([(float(a), float(b)) for a, b in pts], 1.5)]
    base = strokes(W, H, [(pts, width, None)])
    dst = GP(dst, base, col, mix(col, "#efe2c6", 0.4), seed=seed, rough=0.8, streak=0.5)
    step = step or width * 0.62
    seg, sh = [], []
    acc = 0.0
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        acc += math.hypot(x1 - x0, y1 - y0)
        if acc >= step:
            acc = 0.0
            dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1
            tx, ty = dx / L, dy / L; nx, ny = -ty, tx
            hw = width * 0.5
            a = (x1 + nx * hw - tx * hw * twist, y1 + ny * hw - ty * hw * twist)
            b = (x1 - nx * hw + tx * hw * twist, y1 - ny * hw + ty * hw * twist)
            sh.append(([a, b], max(1.2, width * 0.16), None))
            seg.append(([(a[0] + tx * width * .18, a[1] + ty * width * .18), (b[0] + tx * width * .18, b[1] + ty * width * .18)], max(1.0, width * 0.12), None))
    m1 = strokes(W, H, sh) * base
    dst = OV(dst, m1, lambda m: col_arr(m, dark, m * 0.85), pad=4)
    m2 = strokes(W, H, seg) * base
    dst = OV(dst, m2, lambda m: col_arr(m, "#f6ecd4", m * 0.55), pad=4)
    edge = np.clip(base - gaussian_filter(base, 1.2) * 0 - (gaussian_filter(base, 2.0) > 0.92), 0, 1) * base
    dst = OV(dst, edge, lambda m: col_arr(m, dark, m * 0.5), pad=4)
    return dst


def _resample(pts, n=12):
    if len(pts) >= n:
        return pts
    out = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        k = max(2, n // (len(pts) - 1))
        for j in range(k):
            t = j / k
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    out.append(pts[-1])
    return out


def strokes(w, h, items, cap=True):
    """_j1_lib.strokes with short polylines resampled, so tapers work on 2-3 point strokes too."""
    return _j1_lib.strokes(w, h, [(_resample(list(it[0])),) + tuple(it[1:]) for it in items], cap=cap)
