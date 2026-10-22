"""Agent G4 helpers (sage-syari, girih-emas, kintsugi-emas, lomba-17an).
Builds on _j1_lib (bbox-cropped G/GP/LC/FO/OV painting, batched strokes/shapes) and adds: eucalyptus + dried leaves
(watercolour), wax-seal relief, girih geometry (decagon + bowtie tiling, Hankin strapwork at 54 deg), ceramic glaze +
crackle + kintsugi seams, simple gouache figures. Previews -> /tmp/pen/nb-G4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _j1_lib import *  # noqa
import _j1_lib, _p1_lib
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates, binary_dilation

PREV = "/tmp/pen/nb-G4/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV


def prev(arr, name, tone="#f3f1ea", bg=None):
    _p1_lib.preview(arr, name, tone, bg)


def clear():
    _art._fbm_cache.clear()


def lum(arr, k):
    out = arr.copy()
    out[..., :3] = np.clip(out[..., :3] * k, 0, 1)
    return out


def emboss_light(height, sigma=2.0, az=(-0.7, -0.7), k=6.0):
    """Lambert-ish light (0..1, 0.5 = flat) from a height field, light from the top-left."""
    hgt = gaussian_filter(height, sigma)
    gy, gx = np.gradient(hgt)
    return np.clip(0.5 - (gx * az[0] + gy * az[1]) * k, 0, 1)


def tint(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(mask * alpha, 0, 1)[..., None]], -1)


# ------------------------------------------------------------------ botanicals (sage)
def bez(p0, p1, p2, n=30):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]


def euca_leaf(art, W, H, x, y, r, ang, rng, nx, cols=("#9fb3a6", "#6f8a7c"), squash=0.82, vein=True, bloom=0.4):
    """Silver-dollar eucalyptus leaf: a rounded, slightly pointed disc on a short petiole, chalky blue-sage."""
    cx, cy = x + math.cos(ang) * r * 0.95, y + math.sin(ang) * r * 0.95
    pts = []
    for k in range(18):
        a = k / 18 * math.tau
        rr = r * (1 + 0.08 * math.cos(a) + rng.uniform(-0.03, 0.03))
        px, py = math.cos(a) * rr, math.sin(a) * rr * squash
        if a < 0.35 or a > math.tau - 0.35:
            px *= 1.08
        pts.append((cx + px * math.cos(ang) - py * math.sin(ang), cy + px * math.sin(ang) + py * math.cos(ang)))
    m = shapes(W, H, [pts])
    a_, b_ = jitter_hex(cols[0], rng, 0.05), jitter_hex(cols[1], rng, 0.05)
    art = G(art, m, a_, b_, seed=nx(), density=0.88, edge=0.7, bloom=bloom, gran=0.35, rough=3.0, feather=1.2)
    # shadow side glaze
    sh = m * np.clip(np.roll(gaussian_filter(m, r * 0.35), (-int(r * 0.35), int(r * 0.25)), (0, 1)) * 0, 0, 1)
    half = shapes(W, H, [[(cx + math.cos(a + ang) * r * 1.05, cy + math.sin(a + ang) * r * 1.05 * squash) for a in np.linspace(0.2, math.pi - 0.2, 10)] + [(cx, cy)]])
    art = G(art, half * m * 0.8, cols[1], seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=2, feather=3)
    if vein:
        v = strokes(W, H, [([(x, y), (cx + math.cos(ang) * r * 0.8, cy + math.sin(ang) * r * 0.8)], 1.6, (0.0, 0.6))])
        art = G(art, v, "#5b6e5f", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    return art, m


def dried_leaf(art, W, H, x, y, L, wd, ang, rng, nx, cols=("#d1b183", "#a57a48"), curl=0.0, veins=True):
    """Dried lanceolate leaf (tan/ochre), midrib + side veins, a slightly curled edge."""
    pts = petal_pts(x, y, L, wd, ang, n=16, cup=curl)
    pts = deform(pts, rng, 1, 0.02)
    m = shapes(W, H, [pts])
    art = G(art, m, jitter_hex(cols[0], rng, 0.05), jitter_hex(cols[1], rng, 0.05), seed=nx(), density=0.95, edge=0.8, bloom=0.3, gran=0.4, rough=2.5, feather=1.0)
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    # one half darker (curl shadow)
    half = shapes(W, H, [[(x, y)] + [(x + ca * L * t + px * wd * 0.5 * math.sin(t * math.pi) * 1.1, y + sa * L * t + py * wd * 0.5 * math.sin(t * math.pi) * 1.1) for t in np.linspace(0, 1, 14)]])
    art = G(art, half * m, cols[1], seed=nx(), density=0.55, edge=0.25, bloom=0.1, rough=1.5, feather=1.5)
    if veins:
        items = [([(x - ca * 10, y - sa * 10), (x + ca * L * 0.92, y + sa * L * 0.92)], 1.8, (0.0, 0.5))]
        for t in np.linspace(0.18, 0.8, 6):
            bx, by = x + ca * L * t, y + sa * L * t
            for sg in (-1, 1):
                ln = wd * 0.42 * math.sin(t * math.pi) + 2
                ex, ey = bx + (ca * 0.6 + px * sg) * ln, by + (sa * 0.6 + py * sg) * ln
                items.append(([(bx, by), (ex, ey)], 0.9, (0.0, 0.7)))
        v = strokes(W, H, items)
        art = G(art, v, "#7a5530", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    return art, m


def stem(art, W, H, pts, width, rng, nx, col=("#8a8a6a", "#6b6a4c")):
    m = strokes(W, H, [(pts, width, (0.02, 0.5))])
    art = G(art, m, col[0], col[1], seed=nx(), density=0.75, edge=0.4, bloom=0.1, gran=0.3, rough=1.2, feather=0.6)
    return art, m


def berries(art, W, H, items, rng, nx, cols=("#7d8c6c", "#4e5b43")):
    """Seeded-eucalyptus seed pods: small cups with a darker crown."""
    m = circles(W, H, items)
    art = G(art, m, cols[0], cols[1], seed=nx(), density=0.8, edge=0.7, bloom=0.1, gran=0.3, rough=1.2, feather=0.6)
    crowns = circles(W, H, [(x + r * 0.15, y - r * 0.2, r * 0.42) for x, y, r in items])
    art = G(art, crowns, "#3f4a35", seed=nx(), density=0.55, edge=0.3, bloom=0, rough=0.8, feather=0.5)
    return art


# ------------------------------------------------------------------ wax seal
def wax_seal(W, H, cx, cy, R, rng, base="#7f9271", deep="#56684b", hi="#c7d3b6", ring_items=None, seed=1):
    """Opaque wax seal: irregular poured blob, raised rim, recessed centre, optional pressed ring motif."""
    pts = []
    for k in range(40):
        a = k / 40 * math.tau
        rr = R * (1 + 0.05 * math.sin(a * 3 + 1) + 0.04 * math.sin(a * 7) + rng.uniform(-0.015, 0.015))
        # a couple of poured lobes
        rr += R * 0.09 * max(0, math.cos(a - 0.6)) ** 8 + R * 0.07 * max(0, math.cos(a - 3.7)) ** 10
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    blob = shapes(W, H, [pts])
    inner = circles(W, H, [(cx, cy, R * 0.7)])
    ringm = np.clip(circles(W, H, [(cx, cy, R * 0.8)]) - circles(W, H, [(cx, cy, R * 0.74)]), 0, 1)
    height = gaussian_filter(blob, R * 0.08) * 1.0 - gaussian_filter(inner, 2.0) * 0.35 + gaussian_filter(ringm, 1.0) * 0.25
    if ring_items is not None:
        height += gaussian_filter(ring_items, 1.6) * 0.3
    light = emboss_light(height, 1.2, k=R * 0.09)
    out = gouache_paint(blob, base, deep, seed=seed, rough=1.2, streak=0.35)
    L = light[..., None]
    mot = (fbm(W, H, seed + 31, 26, 4)[..., None] - 0.5)
    rgb = out[..., :3] * (0.6 + 0.8 * L) * (1 + mot * 0.22)
    spec = np.clip((light - 0.72) * 4, 0, 1)[..., None]
    rgb = rgb * (1 - spec * 0.5) + np.array(hex_rgb(hi), np.float32) * spec * 0.5
    # slightly translucent darker pooling at the edge
    edge = np.clip(blob - gaussian_filter(blob, 3), 0, 1)[..., None]
    rgb = rgb * (1 - edge * 0.4)
    out[..., :3] = np.clip(rgb, 0, 1)
    return out, blob


# ------------------------------------------------------------------ girih geometry
GA = 0.5 / math.tan(math.radians(18))  # decagon apothem (edge 1)
GR = 0.5 / math.sin(math.radians(18))  # decagon circumradius
GV1 = (2 * GA, 0.0)
GV2 = (2 * GA * math.cos(math.radians(72)), 2 * GA * math.sin(math.radians(72)))


def g_dec(cx, cy):
    return [(cx + GR * math.cos(math.radians(18 + 36 * k)), cy + GR * math.sin(math.radians(18 + 36 * k))) for k in range(10)]


def _inter(p, d, q, e):
    den = d[0] * e[1] - d[1] * e[0]
    if abs(den) < 1e-9:
        return None
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    u = ((q[0] - p[0]) * d[1] - (q[1] - p[1]) * d[0]) / den
    return t, u


def _rays(poly, th):
    n = len(poly); out = []
    A = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sg = 1 if A > 0 else -1
    c, s = math.cos(th), math.sin(th)
    for i in range(n):
        p0, p1 = poly[i], poly[(i + 1) % n]
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        ex, ey = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(ex, ey); ex /= L; ey /= L
        nx_, ny_ = -ey * sg, ex * sg
        out.append((m, (ex * c + nx_ * s, ey * c + ny_ * s), (-ex * c + nx_ * s, -ey * c + ny_ * s)))
    return out


def _inside(poly, pt):
    x, y = pt; n = len(poly); ins = False
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            ins = not ins
    return ins


def g_hankin(poly, th=math.radians(54)):
    """Hankin strapwork: rays from each edge midpoint at th; mutually-nearest forward intersections inside."""
    r = _rays(poly, th); R_ = []
    for i, (m, f, b) in enumerate(r):
        R_ += [(i, m, f), (i, m, b)]
    used = set(); segs = []
    cands = []
    # straight runs: a ray passing exactly through another edge midpoint whose ray points straight back
    for a_ in range(len(R_)):
        for b_ in range(a_ + 1, len(R_)):
            i, m, d = R_[a_]; j, m2, e = R_[b_]
            if i == j:
                continue
            vx, vy = m2[0] - m[0], m2[1] - m[1]
            t = vx * d[0] + vy * d[1]
            if t > 0 and abs(vx * d[1] - vy * d[0]) < 1e-6 and abs(d[0] + e[0]) + abs(d[1] + e[1]) < 1e-6:
                cands.append((t / 2, a_, b_, ((m[0] + m2[0]) / 2, (m[1] + m2[1]) / 2)))
    for a_ in range(len(R_)):
        for b_ in range(a_ + 1, len(R_)):
            i, m, d = R_[a_]; j, m2, e = R_[b_]
            if i == j:
                continue
            res = _inter(m, d, m2, e)
            if not res or res[0] <= 1e-6 or res[1] <= 1e-6:
                continue
            P = (m[0] + d[0] * res[0], m[1] + d[1] * res[0])
            if not _inside(poly, P):
                continue
            cands.append((max(res[0], res[1]) + 0.01 * abs(res[0] - res[1]), a_, b_, P))
    cands.sort()
    for _, a_, b_, P in cands:
        if a_ in used or b_ in used:
            continue
        used |= {a_, b_}
        segs.append((R_[a_][1], P)); segs.append((R_[b_][1], P))
    return segs


def _edge_pts(c, n):
    return [(c[0] + GR * math.cos(math.radians(n - 18)), c[1] + GR * math.sin(math.radians(n - 18))),
            (c[0] + GR * math.cos(math.radians(n + 18)), c[1] + GR * math.sin(math.radians(n + 18)))]


def g_bowtie(o):
    cs = {0: o, 1: (o[0] + GV1[0], o[1] + GV1[1]), 2: (o[0] + GV1[0] + GV2[0], o[1] + GV1[1] + GV2[1]), 3: (o[0] + GV2[0], o[1] + GV2[1])}
    pts = []
    for ci, ns in ((0, [36]), (1, [108, 144]), (2, [216]), (3, [288, 324])):
        for n in ns:
            pts += _edge_pts(cs[ci], n)
    uniq = []
    for p in pts:
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-6 for q in uniq):
            uniq.append(p)
    cx = sum(p[0] for p in uniq) / len(uniq); cy = sum(p[1] for p in uniq) / len(uniq)
    uniq.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return uniq


def girih_field(x0, y0, x1, y1, S, ox=0.0, oy=0.0):
    """All (tile polygons, strap segments) in px covering the rect, decagon lattice scaled by S (px per edge)."""
    tiles, segs = [], []
    rng_i = int((x1 - x0) / (S * GV1[0])) + 6
    rng_j = int((y1 - y0) / (S * GV2[1])) + 6
    for j in range(-3, rng_j):
        for i in range(-rng_i - 3, rng_i + 3):
            o = (ox / S + i * GV1[0] + j * GV2[0], oy / S + i * GV1[1] + j * GV2[1])
            if not (x0 / S - 6 < o[0] < x1 / S + 6 and y0 / S - 6 < o[1] < y1 / S + 6):
                continue
            for kind, poly in (("dec", g_dec(*o)), ("bow", g_bowtie(o))):
                tiles.append((kind, [(x * S, y * S) for x, y in poly]))
                for m, P in g_hankin(poly):
                    segs.append(((m[0] * S, m[1] * S), (P[0] * S, P[1] * S)))
    return tiles, segs


# ------------------------------------------------------------------ simple gouache figures (lomba)
def fig_masks(W, H, x, y, s, pose="stand", flip=1, rng=None):
    """Stylised child figure (no face), feet at (x, y), height ~ s. Returns dict of masks: skin, shirt, pants, hair."""
    f = flip
    P = lambda dx, dy: (x + dx * s * f, y + dy * s)
    head = (x + 0.0 * s * f, y - 0.86 * s, 0.11 * s)
    if pose == "climb":
        head = (x + 0.04 * s * f, y - 0.86 * s, 0.11 * s)
    d = {}
    d["skin"] = circles(W, H, [head])
    d["hair"] = shapes(W, H, [[(head[0] + math.cos(a) * head[2] * 1.04, head[1] + math.sin(a) * head[2] * 1.04) for a in np.linspace(math.pi * 0.92, math.tau * 1.02, 12)] + [(head[0] + head[2] * 0.6 * f, head[1] - head[2] * 0.1)]])
    torso = [P(-0.12, -0.72), P(0.12, -0.72), P(0.14, -0.42), P(-0.14, -0.42)]
    d["shirt"] = shapes(W, H, [torso], smooth=False)
    return d, head
