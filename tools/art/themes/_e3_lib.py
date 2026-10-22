"""Agent E3 helpers (bulan-bintang, garis-geometri, mawar-taif, pesantren-teduh).
Builds on _b2_lib/_j1_lib (bbox-cropped painting) and adds: hand-inked geometric line work (Hankin polygons-in-contact
on the 4.8.8 tiling), watercolour crescent / stars / clouds, Taif rose shrubs, dry-stone terraces, frangipani.
Previews -> /tmp/pen/nb-E3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _b2_lib import *  # noqa
import _b2_lib, _j1_lib, _p1_lib
import art as _art

PREV = "/tmp/pen/nb-E3/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_b2_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


# ------------------------------------------------------------------ hand-inked line work
def wobble_line(a, b, rng, amp=0.6, step=6.0):
    """Subdivide a straight segment with a slow, low-amplitude wobble (a steady hand with a technical pen)."""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    n = max(2, int(L / step))
    nx_, ny_ = -(b[1] - a[1]) / (L or 1), (b[0] - a[0]) / (L or 1)
    ph, f = rng.uniform(0, 6.3), rng.uniform(0.6, 1.4)
    pts = []
    for i in range(n + 1):
        t = i / n
        o = amp * (math.sin(t * math.pi * f + ph) * 0.7 + rng.gauss(0, 0.18)) * math.sin(math.pi * t) ** 0.3
        pts.append((a[0] + (b[0] - a[0]) * t + nx_ * o, a[1] + (b[1] - a[1]) * t + ny_ * o))
    return pts


def ink_mask(W, H, segs, width, rng, amp=0.5, press=0.3, blobs=0.0):
    """Many straight segments -> one hand-inked line mask (pressure varies along each line, ink blobs at stops)."""
    cv = Canvas(W, H)
    for a, b in segs:
        pts = wobble_line(a, b, rng, amp)
        w0 = width * rng.uniform(0.85, 1.15)
        for i in range(len(pts) - 1):
            t = i / max(1, len(pts) - 2)
            wd = max(0.4, w0 * (1 - press * 0.5 + press * 0.5 * math.sin(math.pi * t)))
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wd, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
            cv.c.drawLine(*pts[i], *pts[i + 1], p)
        if blobs and rng.random() < blobs:
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
            cv.c.drawCircle(*b, width * rng.uniform(0.6, 0.9), p)
    return cv.array()[..., 3]


def ink(mask, col="#151515", seed=1, alpha=0.95, bleed=0.35):
    """Ink on paper: slight bleed, uneven density (pen running dry in places)."""
    h, w = mask.shape
    m = gaussian_filter(mask, bleed) if bleed else mask
    dens = 0.82 + 0.18 * fbm(w, h, seed, 30, 3)
    rgb = np.ones((h, w, 3), np.float32) * col_arr(col)
    return np.concatenate([rgb, np.clip(m * dens * alpha, 0, 1)[..., None]], -1)


def IK(dst, mask, col="#151515", seed=1, alpha=0.95, bleed=0.35):
    return OV(dst, mask, lambda m: ink(m, col, seed, alpha, bleed), pad=6)


def _isect(p, d, q, e):
    den = d[0] * e[1] - d[1] * e[0]
    if abs(den) < 1e-9:
        return None
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    return (p[0] + d[0] * t, p[1] + d[1] * t)


def hankin(poly_, theta):
    """Polygons-in-contact: every edge midpoint emits two rays at angle theta; rays are paired greedily with the
    partner they meet soonest (Hankin's first-contact rule), and drawn midpoint -> meeting point."""
    n = len(poly_)
    cx = sum(p[0] for p in poly_) / n; cy = sum(p[1] for p in poly_) / n
    rays = []
    c, s_ = math.cos(theta), math.sin(theta)
    for i in range(n):
        a, b = poly_[i], poly_[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        nn = (-d[1], d[0])
        if (cx - m[0]) * nn[0] + (cy - m[1]) * nn[1] < 0:
            nn = (-nn[0], -nn[1])
        rays.append((m, (c * d[0] + s_ * nn[0], c * d[1] + s_ * nn[1]), i, 1))
        rays.append((m, (-c * d[0] + s_ * nn[0], -c * d[1] + s_ * nn[1]), i, -1))
    cand = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            (p, d, ei, _), (q, e, ej, _) = rays[i], rays[j]
            if ei == ej:
                continue
            den = d[0] * e[1] - d[1] * e[0]
            if abs(den) < 1e-9:
                continue
            t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
            u = ((q[0] - p[0]) * d[1] - (q[1] - p[1]) * d[0]) / den
            if t > 1e-6 and u > 1e-6:
                cand.append((t + u, abs(t - u), i, j, (p[0] + d[0] * t, p[1] + d[1] * t)))
    cand.sort()
    used, segs = set(), []
    for _, _, i, j, P in cand:
        if i in used or j in used:
            continue
        used.add(i); used.add(j)
        segs += [(rays[i][0], P), (rays[j][0], P)]
    return segs


def region_at(line_mask, pts, thr=0.25):
    """Fill mask of the cells (enclosed by drawn lines) containing the given points."""
    from scipy.ndimage import label, binary_dilation
    free = line_mask < thr
    lab, _ = label(free)
    out = np.zeros(line_mask.shape, np.float32)
    for x, y in pts:
        v = lab[int(round(y)), int(round(x))]
        if v:
            out[lab == v] = 1
    return np.clip(gaussian_filter(binary_dilation(out > 0, iterations=1).astype(np.float32), 0.6), 0, 1)


def tiling_488(x0, y0, x1, y1, s):
    """4.8.8 tiling (octagons + squares), octagon edge s. Returns (octagons, squares) as vertex lists."""
    k = s / math.sqrt(2)
    step = s + 2 * k
    octs, sqs = [], []
    j = int(y0 // step) - 1
    while j * step < y1 + step:
        i = int(x0 // step) - 1
        while i * step < x1 + step:
            cx, cy = i * step, j * step
            R = s / (2 * math.sin(math.pi / 8))
            octs.append([(cx + R * math.cos(math.pi / 8 + q * math.pi / 4), cy + R * math.sin(math.pi / 8 + q * math.pi / 4)) for q in range(8)])
            qx, qy = cx + step / 2, cy + step / 2
            h = s / math.sqrt(2)
            sqs.append([(qx, qy - h), (qx + h, qy), (qx, qy + h), (qx - h, qy)])
            i += 1
        j += 1
    return octs, sqs


def poly_segs(poly_):
    return [(poly_[i], poly_[(i + 1) % len(poly_)]) for i in range(len(poly_))]


def star_polys(octs, theta=None):
    """Outline of the {8/3} star inside each octagon (tips on the edge midpoints)."""
    out = []
    for o in octs:
        cx = sum(p[0] for p in o) / 8; cy = sum(p[1] for p in o) / 8
        mids = [((o[i][0] + o[(i + 1) % 8][0]) / 2, (o[i][1] + o[(i + 1) % 8][1]) / 2) for i in range(8)]
        r = math.hypot(mids[0][0] - cx, mids[0][1] - cy)
        a0 = math.atan2(mids[0][1] - cy, mids[0][0] - cx)
        out.append(star_pts(cx, cy, r, 8, math.cos(3 * math.pi / 8) / math.cos(math.pi / 4), a0))
    return out


def pattern_488(octs, sqs, theta=math.radians(67.5)):
    """Classic 8-fold star pattern on 4.8.8: interlaced {8/3} chords in octagons, 4-point stars in squares
    (lines run straight through the shared edges)."""
    segs = []
    for o in octs:
        segs += _hankin_pairs(o, theta, 2)
    for q in sqs:
        segs += _hankin_pairs(q, theta)
    return segs


def _hankin_pairs(poly_, theta, skip=1):
    n = len(poly_)
    cx = sum(p[0] for p in poly_) / n; cy = sum(p[1] for p in poly_) / n
    c, s_ = math.cos(theta), math.sin(theta)
    info = []
    for i in range(n):
        a, b = poly_[i], poly_[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        nn = (-d[1], d[0])
        if (cx - m[0]) * nn[0] + (cy - m[1]) * nn[1] < 0:
            nn = (-nn[0], -nn[1])
        info.append((m, d, nn))
    segs = []
    for i in range(n):
        j = (i + skip) % n
        (m1, d1, n1), (m2, d2, n2) = info[i], info[j]
        r1 = (c * d1[0] + s_ * n1[0], c * d1[1] + s_ * n1[1])
        r2 = (-c * d2[0] + s_ * n2[0], -c * d2[1] + s_ * n2[1])
        P = _isect(m1, r1, m2, r2)
        if P:
            segs += [(m1, P), (m2, P)]
    return segs


# ------------------------------------------------------------------ sky things
def crescent_mask(W, H, cx, cy, r, off=0.42, rot=-0.6, inner=0.92):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.drawCircle(cx, cy, r, p)
        p2 = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        p2.setBlendMode(skia.BlendMode.kClear)
        cv.c.drawCircle(cx + math.cos(rot) * r * off, cy + math.sin(rot) * r * off, r * inner, p2)
    return mask_from(W, H, draw)


def soft_star(W, H, cx, cy, r, rng, n=4, inner=0.28, rot=None):
    rot = rng.uniform(0, math.tau) if rot is None else rot
    pts = star_pts(cx, cy, r, n, inner, rot)
    # curved (concave) sides: add points pulled inwards between tip and inner vertex
    cur = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        cur.append(a)
        cur.append(((a[0] + b[0]) / 2 * 0.86 + cx * 0.14, (a[1] + b[1]) / 2 * 0.86 + cy * 0.14))
    return shapes(W, H, [deform(cur, rng, 1, 0.03)])


def cloud_mask(W, H, x, y, w, h, rng, puffs=7):
    """Cumulus bank: flat-ish bottom, lumpy top."""
    polys = [deform(ellipse_pts(x, y, w * 0.5, h * 0.22, 14), rng, 2, 0.05)]
    for k in range(puffs):
        t = (k + 0.5) / puffs
        px = x - w * 0.42 + w * 0.84 * t + rng.gauss(0, w * 0.03)
        ph = h * (0.25 + 0.5 * math.sin(math.pi * t) ** 0.8) * rng.uniform(0.75, 1.15)
        polys.append(deform(ellipse_pts(px, y - ph * 0.35, w * rng.uniform(0.1, 0.16), ph * 0.6, 14), rng, 2, 0.06))
    m = shapes(W, H, polys)
    cut = np.zeros_like(m)
    yy = np.arange(H, dtype=np.float32)[:, None]
    cut = (yy > y + h * 0.12).astype(np.float32)
    return np.clip(m * (1 - gaussian_filter(cut, 2)), 0, 1)
