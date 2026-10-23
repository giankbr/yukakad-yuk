"""Arabesk Perak — filigri perak arabesk (sulur islimi bercabang, palmet terbelah/rumi, dua batang yang saling
menganyam atas-bawah) di atas beludru hitam; kartusy lengkung runcing untuk sampul. Tanpa figur, tanpa kaligrafi.
Run: python3 -I arabesk-perak.py [part ...]   parts: arch band rosette finial velvet
Assets -> public/themes/art/arabesk-perak/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n5_lib import *
import random

OUT = outdir("arabesk-perak")
PARTS = sys.argv[1:] or ["arch", "band", "rosette", "finial", "velvet"]
VEL = "#0c0b0e"


def offset_path(P, d):
    n = len(P); out = []
    for i in range(n):
        x0, y0 = P[max(0, i - 1)]; x1, y1 = P[min(n - 1, i + 1)]
        h = math.atan2(y1 - y0, x1 - x0)
        out.append((P[i][0] - math.sin(h) * d, P[i][1] + math.cos(h) * d))
    return out


def heading_at(P, x, y):
    A = np.array(P); i = int(np.argmin(((A[:, 0] - x) ** 2 + (A[:, 1] - y) ** 2)))
    x0, y0 = P[max(0, i - 1)]; x1, y1 = P[min(len(P) - 1, i + 1)]
    return math.atan2(y1 - y0, x1 - x0), P[i]


def band_masks(W, H, path, amp, lam, w0, seed, fringe=-1, bay=2.2, border=True, beads=True, lens_k=1.0, leaf=1.0):
    """Interlaced double-stem rinceau along path, with lens palmettes, border lines, bead row and an
    outward fringe of spiral scrolls. Returns (mask, engraving)."""
    rng = random.Random(seed)
    P = resample(path, 2.0)
    a = rinceau(P, amp, lam, 0.0, w0=w0, rng=rng, bay=bay, leaf=leaf, only_side=fringe, fill=False) if fringe is not None else rinceau(P, amp, lam, 0.0, w0=w0, rng=rng, spirals=False)
    b = rinceau(P, amp, lam, math.pi, w0=w0, rng=rng, spirals=False)
    sA, lA, eA, _ = islimi_masks(W, H, [a])
    sB, lB, eB, _ = islimi_masks(W, H, [b])
    cr = interlace(None, None, a["wave"], b["wave"])
    for k, (x, y) in enumerate(cr):
        if k % 2 == 0:
            sB = cut_under(sB, sA, x, y, amp * 1.1, gap=w0 * 0.55)
        else:
            sA = cut_under(sA, sB, x, y, amp * 1.1, gap=w0 * 0.55)
    lens = []
    for k in range(len(cr) - 1):
        mx, my = (cr[k][0] + cr[k + 1][0]) / 2, (cr[k][1] + cr[k + 1][1]) / 2
        h, p = heading_at(P, mx, my)
        L = lam * 0.27 * lens_k
        lens += palmette(p[0] - math.cos(h) * L * 0.55, p[1] - math.sin(h) * L * 0.55, h, L, L * 0.21, belly=-1, bend=2.8, spread=0.45, asym=1)
    parts = [sA, lA, sB, lB]
    if lens:
        parts.append(shapes(W, H, lens))
    if border:
        lines_ = [(offset_path(P, d), w) for d, w in ((amp + w0 * 1.7, w0 * 0.55), (-(amp + w0 * 1.7), w0 * 0.55))]
        parts.append(strokes(W, H, [(pp, ww, None) for pp, ww in lines_]))
    if beads:
        bp = offset_path(P, -(amp + w0 * 3.6))
        parts.append(circles(W, H, [(x, y, w0 * 0.5) for x, y in resample(bp, w0 * 2.6)[2:-2]]))
    return np.maximum.reduce(parts), np.maximum(eA, eB)


def render(W, H, M, E, seed, name, max_w, bg=VEL):
    art = silver(blank(W, H), np.clip(M, 0, 1), E, seed=seed)
    preview(art, name, bg=bg)
    return save(art, f"{OUT}/{name}.webp", max_w=max_w, quality=82)


# ---------------------------------------------------------------- cover cartouche: pointed (lancet) arch
def arch():
    W, H = 780, 1290
    cx, r, ys, bot = 390, 268, 610, 1250
    R = 1.5 * r
    dy = math.sqrt(R * R - (R - r) ** 2)
    ya = ys - dy
    c0 = (cx - r + R, ys)
    a_end = math.atan2(ya - ys, cx - c0[0]) + 2 * math.pi
    left = [(cx - r, bot), (cx - r, ys)] + [(c0[0] + math.cos(t) * R, c0[1] + math.sin(t) * R) for t in np.linspace(math.pi, a_end, 120)[1:]]
    M, E = band_masks(W, H, left, 15, 118, 4.6, 11, fringe=-1, bay=2.3, leaf=1.15)
    M = np.maximum(M, M[:, ::-1]); E = np.maximum(E, E[:, ::-1])
    # apex finial (slender lancet palmette on a bead) + two small coils, base terminals
    polys = palmette(cx, ya - 30, -math.pi / 2, 70, 13, belly=-1, bend=3.1, spread=0.75, asym=1, centre=1.55)
    polys.append(petal_pts(cx, ya - 150, 26, 8, -math.pi / 2, n=10))
    polys.append(ellipse_pts(cx, ya - 26, 9, 9, 10))
    for sx in (-1, 1):
        polys += palmette(cx - r + 0 if sx < 0 else cx + r, bot + 6, math.pi / 2, 54, 11, belly=-1, bend=2.8, spread=0.45, asym=1)
    coil, _ = spiral_vine(cx - 8, ya - 24, math.pi * 0.92, 120, 1 / 60, 1 / 9, turn=1)
    st = strokes(W, H, [(coil, 4.4, (0.05, 0.4))])
    sc = np.maximum(st, st[:, ::-1]); en = np.zeros_like(sc)
    M = np.maximum.reduce([M, shapes(W, H, polys), sc]); E = np.maximum(E, en)
    # inner hanging rosette under the apex
    rp = []
    for k in range(8):
        a = k * math.pi / 4 - math.pi / 2
        rp.append(petal_pts(cx, ya + 70, 20, 6.5, a, n=10))
    M = np.maximum.reduce([M, shapes(W, H, rp), strokes(W, H, [([(cx, ya + 22), (cx, ya + 50)], 2.4, None)]), circles(W, H, [(cx, ya + 70, 4)])])
    clear()
    return render(W, H, M, E, 21, "arch", 680)


def band():
    W, H = 760, 150
    M, E = band_masks(W, H, [(20, 75), (740, 75)], 17, 140, 5.0, 3, fringe=None, border=False, beads=False, lens_k=1.1)
    rng = random.Random(9)
    # end palmettes pointing outward
    polys = palmette(28, 75, math.pi, 46, 10, belly=-1, bend=2.8, spread=0.45, asym=1) + palmette(732, 75, 0, 46, 10, belly=-1, bend=2.8, spread=0.45, asym=1)
    M = np.maximum(M, shapes(W, H, polys))
    clear()
    return render(W, H, M, E, 5, "band", 520)


def rosette():
    W = H = 360
    cx = cy = 180
    parts = []
    # interlaced 8-point strap star (two squares) with over/under
    sq = []
    for rot in (0, math.pi / 4):
        pts = [(cx + math.cos(rot + k * math.pi / 2) * 158, cy + math.sin(rot + k * math.pi / 2) * 158) for k in range(4)]
        sq.append(resample(pts + [pts[0]], 2.0))
    s1 = strokes(W, H, [(sq[0], 7.0, None)]); s2 = strokes(W, H, [(sq[1], 7.0, None)])
    cr = interlace(None, None, sq[0], sq[1], tol=3.5)
    for k, (x, y) in enumerate(cr):
        if k % 2 == 0:
            s2 = cut_under(s2, s1, x, y, 12, gap=3.4)
        else:
            s1 = cut_under(s1, s2, x, y, 12, gap=3.4)
    parts += [s1, s2]
    polys = []
    for k in range(8):
        a = k * math.pi / 4
        polys += palmette(cx + math.cos(a) * 68, cy + math.sin(a) * 68, a, 46, 9.5, belly=-1, bend=2.9, spread=0.55, asym=1, centre=1.3)
        polys.append(petal_pts(cx + math.cos(a) * 166, cy + math.sin(a) * 166, 13, 5, a, n=10))
        polys.append(petal_pts(cx, cy, 40, 10, a + math.pi / 8, n=10))
    parts.append(shapes(W, H, polys))
    parts.append(ring_mask(W, H, cx, cy, 60, 3.4))
    parts.append(ring_mask(W, H, cx, cy, 12, 3.0))
    M = np.maximum.reduce(parts)
    clear()
    return render(W, H, M, None, 8, "rosette", 240)


def finial():
    W, H = 300, 230
    cx = 150
    polys = palmette(cx, 176, -math.pi / 2, 66, 13, belly=-1, bend=3.1, spread=0.75, asym=1, centre=1.55)
    polys.append(petal_pts(cx, 52, 24, 8, -math.pi / 2, n=10))
    polys.append(ellipse_pts(cx, 180, 9, 9, 10))
    coil, _ = spiral_vine(cx - 8, 182, math.pi * 0.92, 120, 1 / 60, 1 / 9, turn=1)
    st = strokes(W, H, [(coil, 4.6, (0.05, 0.4))])
    M = np.maximum.reduce([st, st[:, ::-1], shapes(W, H, polys)])
    return render(W, H, M, None, 13, "finial", 220)


def velvet():
    n = 384
    a = wrap_noise(n, n, 3, 22); b = wrap_noise(n, n, 4, 5); f = wrap_noise(n, n, 5, (0.5, 2.2)); g = wrap_noise(n, n, 6, 0.6)
    tone = 0.75 + 0.35 * a + 0.12 * b + 0.10 * f + 0.06 * g
    base = np.array(hex_rgb("#0d0c10"), np.float32)
    rgb = np.clip(base[None, None] * tone[..., None] + np.array([0.008, 0.008, 0.014]) * (a[..., None] - 0.5), 0, 1)
    arr = np.concatenate([rgb, np.ones((n, n, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/velvet.webp", quality=76)


for p in PARTS:
    globals()[p]()
kb(OUT)
