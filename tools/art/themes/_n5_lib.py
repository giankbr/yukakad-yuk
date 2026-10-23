"""Agent N5 helpers (arabesk-perak, anggrek-syari, kristal-es, pentas-seni); base copied from _m5_lib.
Builds on _j1_lib (bbox-local G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds: batik dye + canting line + cecek
dots, ink outlines, polygon helpers, cloth/brick/concrete texture helpers. Previews -> /tmp/pen/nb-N5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _j1_lib  # noqa
from _j1_lib import *  # noqa
import art as _art

PREV = "/tmp/pen/nb-N5/art"
os.makedirs(PREV, exist_ok=True)
_j1_lib.PREV = PREV
import _p1_lib
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def rgba(rgb, a):
    return np.concatenate([rgb, a[..., None] if a.ndim == 2 else a], -1).astype(np.float32)


def flat(h, w, col):
    return np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)


def noise(w, h, seed, sigma, wrap=False):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap" if wrap else "reflect")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def rotp(pts, cx, cy, ang):
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def wob(pts, rng, amt):
    return [(x + rng.uniform(-amt, amt), y + rng.uniform(-amt, amt)) for x, y in pts]


def lines(W, H, polys, width, closed=True, smooth=True):
    """Stroked outlines of many polygons/polylines into one mask."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    for pts in polys:
        path = smooth_path(pts, closed) if smooth else None
        if path is None:
            path = skia.Path(); path.moveTo(*pts[0])
            for q in pts[1:]:
                path.lineTo(*q)
            if closed:
                path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def outline_of(mask, px=1.6):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.03).astype(np.float32) - (gaussian_filter(mask, 0.6) > 0.5), 0, 1)


def ink(mask, col="#2a1f2a", seed=1, alpha=0.92, bleed=0.0):
    h, w = mask.shape
    m = displace(mask, seed, 0.8, 6)
    if bleed:
        m = np.maximum(m, gaussian_filter(m, 1.6) * bleed)
    a = np.clip(gaussian_filter(m, 0.45) * 1.3, 0, 1) * alpha * (0.72 + 0.28 * noise(w, h, seed + 1, 2.5))
    return rgba(flat(h, w, col), a)


def K(dst, mask, *a, pad=6, **k):
    return OV(dst, mask, lambda m: ink(m, *a, **k), pad=pad)


def dye(mask, col, col2=None, seed=1, density=0.9, mottle=0.35):
    """Batik dye in cotton: soft but contained (wax-resisted) edge, uneven take-up, faint weave streaks."""
    h, w = mask.shape
    m = displace(mask, seed, 1.2, 10)
    m = np.clip((gaussian_filter(m, 0.9) - 0.2) * 1.6, 0, 1)
    low = fbm(w, h, seed + 3, 40, 3)
    a = m * density * (1 - mottle + mottle * (0.4 + 0.6 * low))
    wv = noise(w, h, seed + 4, (0.4, 3.0)) * 0.5 + noise(w, h, seed + 5, (3.0, 0.4)) * 0.5
    a *= 0.86 + 0.28 * wv
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 13, 55, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    return rgba(np.clip(rgb, 0, 1), np.clip(a, 0, 1))


def D(dst, mask, *a, pad=10, **k):
    return OV(dst, mask, lambda m: dye(m, *a, **k), pad=pad)


def offset_poly(pts, d):
    """Offset a closed polygon inward (d>0 shrinks toward centroid-ish via normals)."""
    n = len(pts); out = []
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    for i in range(n):
        x, y = pts[i]
        dx, dy = cx - x, cy - y; L = math.hypot(dx, dy) or 1
        out.append((x + dx / L * d, y + dy / L * d))
    return out


def dots_along(pts, step, r, closed=True, jitter=0.0, rng=None):
    """Circles (x, y, r) spaced along a polyline."""
    c = curve(pts + ([pts[0]] if closed else []), max(40, len(pts) * 10))
    out = []; acc = 0.0
    for i in range(1, len(c)):
        seg = math.hypot(c[i][0] - c[i - 1][0], c[i][1] - c[i - 1][1]); acc += seg
        if acc >= step:
            acc = 0.0
            j = (rng.uniform(-jitter, jitter) if rng else 0)
            out.append((c[i][0] + j, c[i][1] + j, r * (rng.uniform(0.8, 1.15) if rng else 1)))
    return out


def ring(W, H, cx, cy, r, width):
    return ring_mask(W, H, cx, cy, r, width)


def tile_noise(w, h, seed, sigma):
    return wrap_noise(w, h, seed, sigma)


def kb(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        s_ = os.path.getsize(os.path.join(d, f)); tot += s_
        print(f"  {f}: {s_ // 1024} KB")
    print(f"  total {tot // 1024} KB")


def spiral_pts(cx, cy, r0, r1, a0, turns, n=40, d=1):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in np.linspace(0, 1, n)]


# ================================================================ N5: arabesque (islimi / rumi) geometry
def spiral_vine(x, y, ang, L, k0, k1, turn=1, ds=2.0):
    """Curve whose curvature grows from k0 to k1 (1/px): an opening sweep that coils into a spiral."""
    pts, hs = [(x, y)], [ang]
    a, s = ang, 0.0
    while s < L:
        t = s / L
        a += turn * (k0 + (k1 - k0) * t ** 2.2) * ds
        x += math.cos(a) * ds; y += math.sin(a) * ds
        pts.append((x, y)); hs.append(a); s += ds
    return pts, hs


def lobe(px, py, h, L, Wd, bend, n=30, inner=0.32, tipk=1.0, belly=1):
    """One pointed, curved lobe: centreline whose curvature grows toward the tip (a hook), width bulging on
    the outside of the curl (belly=1) or the inside (belly=-1)."""
    cl = []
    x, y = px, py
    for i in range(n + 1):
        t = i / n
        a = h + bend * t ** 2.2
        cl.append((x, y, a))
        x += math.cos(a) * L / n; y += math.sin(a) * L / n
    left, right = [], []
    s_ = (1 if bend >= 0 else -1) * belly
    for i, (x, y, a) in enumerate(cl):
        t = i / n
        w = Wd * math.sin(math.pi * min(1.0, t ** 0.62)) ** 1.1
        nxp, nyp = -math.sin(a), math.cos(a)
        left.append((x - nxp * w * s_, y - nyp * w * s_))
        right.append((x + nxp * w * inner * s_, y + nyp * w * inner * s_))
    return left + right[::-1]


def rumi(px, py, h, L, Wd, side=1):
    """Split palmette (rumi): a long lobe sweeping back and a shorter counter-lobe, plus a small eye cut-out."""
    a = lobe(px, py, h + 0.3 * side, L, Wd, bend=2.5 * side, belly=-1, inner=0.2)
    b = lobe(px, py, h - 0.6 * side, L * 0.55, Wd * 0.62, bend=-1.9 * side, belly=-1, inner=0.2)
    ex = px + math.cos(h + 0.7 * side) * L * 0.42; ey = py + math.sin(h + 0.7 * side) * L * 0.42
    eye = ellipse_pts(ex, ey, Wd * 0.22, Wd * 0.12, 10, h + 1.2 * side)
    return [a, b], []


def islimi(x, y, ang, L, turn, depth, rng, out, w0=7.0, kmax=None):
    """Recursive arabesque scroll: a sweeping stem coils into a spiral; side branches (opposite turn) recurse,
    the last generation ends in split palmettes; spiral ends close with a small trefoil bud."""
    kmax = kmax or 6.0 / max(30, L * 0.28)
    pts, hs = spiral_vine(x, y, ang, L, 0.35 / L, kmax, turn)
    n = len(pts)
    out["stems"].append((pts, w0))
    tx, ty = pts[-1]
    out["buds"].append((tx, ty, hs[-1], w0 * 1.9))
    nb = 2 if depth > 0 else 1
    ts = sorted(rng.uniform(0.22, 0.62) for _ in range(nb)) if depth > 0 else [rng.uniform(0.3, 0.55)]
    for t in ts:
        i = max(1, int(t * (n - 1)))
        bx, by = pts[i]
        ca = hs[i] - turn * rng.uniform(0.55, 0.95)
        out["sheaths"].append((bx, by, hs[i], w0 * 2.2, -turn))
        if depth > 0:
            islimi(bx, by, ca, L * rng.uniform(0.48, 0.6), -turn, depth - 1, rng, out, w0 * 0.72)
        else:
            sl = L * 0.18
            sp, sh = spiral_vine(bx, by, ca, sl, 0.002, 0.012, -turn)
            out["stems"].append((sp, w0 * 0.7))
            out["rumi"].append((sp[-1][0], sp[-1][1], sh[-1], L * rng.uniform(0.2, 0.26), w0 * 2.1, -turn))
    return out


def islimi_masks(W, H, items):
    """items: list of dicts from islimi(); returns stem mask, leaf mask, engraving mask."""
    st_items, eng_items, leaves, holes = [], [], [], []
    for out in items:
        for pts, w in out["stems"]:
            st_items.append((pts, w, (0.02, 0.35)))
            eng_items.append((pts, max(0.7, w * 0.2), (0.05, 0.4)))
        for x, y, h, L, wd, side in out["rumi"]:
            ps, es = rumi(x, y, h, L, wd, side)
            leaves += ps; holes += es
        for x, y, h, s_, side in out["sheaths"]:
            leaves.append(lobe(x, y, h + 0.2 * side, s_ * 1.6, s_ * 0.42, bend=0.9 * side))
        for x, y, h, s_ in out["buds"]:
            for d in (-0.9, 0, 0.9):
                leaves.append(petal_pts(x, y, s_ * (1.2 if d == 0 else 0.85), s_ * 0.42, h + d, n=10))
    stem = strokes(W, H, st_items)
    leaf = shapes(W, H, leaves)
    hole = shapes(W, H, holes) if holes else np.zeros((H, W), np.float32)
    eng = strokes(W, H, eng_items)
    return stem, np.clip(leaf - hole, 0, 1), eng, hole


def silver(dst, mask, eng=None, seed=1, base="#a4afc6", shadow=0.75, line="#30343c"):
    """Silver filigree on dark velvet: cast shadow, foil sheen, dark engraved line, cool rim highlight."""
    sh = soft_shadow(mask, "#000000", blur=3.5, strength=shadow, dx=2, dy=3)
    out = over(dst, sh)
    out = FO(out, mask, base, seed=seed, emboss=0.9, sparkle=0.03)
    edge = np.clip(gaussian_filter(mask, 0.8) - gaussian_filter(mask, 2.2), 0, 1) * 1.6
    out = K(out, np.clip(outline_of(mask, 1.0) * 0.8, 0, 1), line, seed=seed + 1, alpha=0.7)
    if eng is not None:
        out = K(out, eng * mask, line, seed=seed + 2, alpha=0.65)
    hi = np.clip(np.roll(np.roll(edge, -1, 0), -1, 1) * mask, 0, 1)
    out = OV(out, hi, lambda m: rgba(flat(m.shape[0], m.shape[1], "#f4f6fa"), m * 0.55), pad=4)
    return out


def resample(pts, step=2.0):
    """Evenly spaced points along a polyline, with headings and arc length."""
    out = [pts[0]]; acc = 0.0
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        while acc + seg >= step and seg > 0:
            t = (step - acc) / seg
            x0, y0 = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            seg = math.hypot(x1 - x0, y1 - y0)
            out.append((x0, y0)); acc = 0.0
        acc += seg
    return out


def rinceau(path, amp, lam, phase=0.0, w0=6.0, rng=None, spirals=True, bay=1.0, leaf=1.0, skip=(), only_side=0, fill=True):
    """Vine scroll along a path: the stem waves about the path; at every crest a branch curls into the bay
    beyond it as a spiral, sprouting a split palmette on its outside; small half-palmettes fill the troughs.
    Returns dict like islimi() plus 'wave' (the stem polyline) for interlacing."""
    rng = rng or random.Random(1)
    P = resample(path, 2.0)
    n = len(P)
    hs = [math.atan2(P[min(n - 1, i + 1)][1] - P[max(0, i - 1)][1], P[min(n - 1, i + 1)][0] - P[max(0, i - 1)][0]) for i in range(n)]
    S = [i * 2.0 for i in range(n)]
    wave = []
    for i in range(n):
        o = amp * math.sin(2 * math.pi * S[i] / lam + phase)
        wave.append((P[i][0] - math.sin(hs[i]) * o, P[i][1] + math.cos(hs[i]) * o))
    out = {"stems": [(wave, w0)], "rumi": [], "sheaths": [], "buds": [], "wave": wave, "crests": []}
    if not spirals:
        return out
    wh = [math.atan2(wave[min(n - 1, i + 1)][1] - wave[max(0, i - 1)][1], wave[min(n - 1, i + 1)][0] - wave[max(0, i - 1)][0]) for i in range(n)]
    k = 0
    while True:
        sk = (k + 0.25 - phase / (2 * math.pi)) * lam / 2 * 2 / 2  # crest positions every lam/2
        sk = ((k + 0.5) * math.pi - phase) / (2 * math.pi) * lam
        k += 1
        if sk < 0:
            continue
        if sk > S[-1] - lam * 0.3:
            break
        if (k - 1) in skip:
            continue
        i = int(sk / 2.0)
        side = 1 if math.sin(2 * math.pi * S[i] / lam + phase) > 0 else -1  # +1: crest on +normal side
        if only_side and side != only_side:
            continue
        out["crests"].append((i, side))
        R = min(lam / 4.6, amp * 1.15) * bay * (1 + 0.16 * math.sin(k * 2.1) + rng.uniform(-0.06, 0.06))
        j = min(n - 1, i + int(lam * 0.06 / 2))
        bx, by = wave[j]
        # +normal of the path in screen coords = (-sin h, cos h); turning toward +normal is turn=+1
        sp, sh = spiral_vine(bx, by, wh[j] + side * 0.25, 2 * math.pi * R * 1.05, 1 / (R * 1.9), 1 / (R * 0.2), turn=side)
        out["stems"].append((sp, w0 * 0.78))
        out["buds"].append((sp[-1][0], sp[-1][1], sh[-1], w0 * 1.5))
        q = int(len(sp) * 0.34)
        out["rumi"].append((sp[q][0], sp[q][1], sh[q] - side * 1.15, R * 0.95 * leaf, w0 * 2.4 * leaf, -side))
        out["sheaths"].append((bx, by, wh[j], w0 * 1.9, side))
        # trough filler: a half palmette on the stem on the opposite side, a quarter wave later
        if not fill:
            continue
        t_i = min(n - 1, i + int(lam * 0.25 / 2))
        tx, ty = wave[t_i]
        out["rumi"].append((tx, ty, wh[t_i] - side * 1.35, R * 0.55 * leaf, w0 * 1.6 * leaf, side))
    return out


def interlace(masks_a, mask_b, wave_a, wave_b, tol=3.0, r=None, gap=2.6, start_over=True):
    """Two stems that cross: find crossings, cut the under-stem around each with a small gap, alternating."""
    A = np.array(wave_a); B = np.array(wave_b)
    from scipy.spatial import cKDTree
    tree = cKDTree(B)
    d, idx = tree.query(A)
    cross = []
    i = 0
    while i < len(A):
        if d[i] < tol:
            j = i
            while j < len(A) and d[j] < tol * 3:
                j += 1
            m = i + int(np.argmin(d[i:j]))
            cross.append(tuple(A[m]))
            i = j + 5
        else:
            i += 1
    return cross


def cut_under(under, over_mask, cx, cy, rad, gap=2.5):
    """Remove the under-strand where the over-strand passes (plus a small dark gap), only near (cx, cy)."""
    H, W = under.shape
    yy, xx = np.ogrid[0:H, 0:W]
    local = (((xx - cx) ** 2 + (yy - cy) ** 2) < rad * rad).astype(np.float32)
    grow = np.clip(gaussian_filter(over_mask, gap) * 3.0, 0, 1)
    return under * (1 - grow * local)


def palmette(px, py, h, L, Wd, asym=0.8, belly=1, bend=2.3, spread=0.3, centre=0.62):
    """Split (bifurcated) palmette: two hooked lobes curling apart and a pointed centre leaf."""
    a = lobe(px, py, h + spread, L, Wd, bend=bend, inner=0.18, belly=belly)
    b = lobe(px, py, h - spread, L * asym, Wd * asym, bend=-bend, inner=0.18, belly=belly)
    c = petal_pts(px, py, L * centre, Wd * 0.42, h, n=12)
    return [a, b, c]


def lobe_line(px, py, h, L, bend, n=24, k=0.8):
    """Engraved midline of a lobe (first k of its length)."""
    pts, x, y = [], px, py
    for i in range(int(n * k) + 1):
        t = i / n
        a = h + bend * t ** 2.2
        pts.append((x, y)); x += math.cos(a) * L / n; y += math.sin(a) * L / n
    return pts


# ================================================================ N5: moth orchid (Phalaenopsis / anggrek bulan) in watercolour
def _blob(cx, cy, rx, ry, rot, rng, n=14, d=1, v=0.05):
    return deform(ellipse_pts(cx, cy, rx, ry, n, rot), rng, d, v)


def phal(art, W, H, x, y, r, rng, nx, rot=0.0, kind="putih", face=1.0):
    """One moth orchid seen from the front: dorsal + two lateral sepals, two broad round petals, a small
    three-lobed lip with a yellow throat. kind 'putih' (white, purple-blushed heart) or 'ungu' (purple, veined).
    face<1 squashes it horizontally (a flower turned a little)."""
    if kind == "putih":
        base, base2, rim, blush, vein = "#fdfbfb", "#f3eef3", "#b3a7c4", "#dca7cf", "#c39ac4"
    else:
        base, base2, rim, blush, vein = "#c47ec0", "#a956a8", "#7a3b80", "#8e3a8c", "#6a2470"

    def P(px, py):  # local -> canvas with rotation & squash
        px *= face
        c, s_ = math.cos(rot), math.sin(rot)
        return (x + px * c - py * s_, y + px * s_ + py * c)

    def poly(pts):
        return [P(px, py) for px, py in pts]
    sep = [poly(petal_pts(0, 0, r * 0.98, r * 0.34, -math.pi / 2, n=14)),
           poly(petal_pts(0, 0, r * 0.95, r * 0.33, math.pi / 2 + 0.62, n=14)),
           poly(petal_pts(0, 0, r * 0.95, r * 0.33, math.pi / 2 - 0.62, n=14))]
    pet = [poly(_blob(sx * r * 0.52, -r * 0.04, r * 0.5, r * 0.46, sx * 0.12, rng, 16, 1, 0.04)) for sx in (-1, 1)]
    sepm = [shapes(W, H, [p]) for p in sep]
    petm = [shapes(W, H, [p]) for p in pet]
    allm = np.maximum.reduce(sepm + petm)
    art = knockout(art, allm, amount=0.96, grow=0.8)
    # cast shadow onto the paper (cool, faint)
    art = G(art, np.roll(np.roll(allm, int(r * 0.05), 0), int(r * 0.04), 1) * 0.6, "#c7bdd2", seed=nx(), density=0.22, edge=0.2, bloom=0, rough=3, feather=3)
    for k, m in enumerate(sepm + petm):
        if k == len(sepm):
            pu = np.maximum.reduce(petm)
            art = knockout(art, pu, amount=0.92, grow=0.6)
        art = G(art, m, base, base2, seed=nx(), density=0.75 if kind == "putih" else 0.62, edge=0.0, bloom=0.25, rough=2.0, feather=1.1, gran=0.15)
        ring = np.clip(m - gaussian_filter(m, r * 0.06), 0, 1) * 2.2
        art = G(art, np.clip(ring, 0, 1), rim, seed=nx(), density=0.3 if kind == "putih" else 0.55, edge=0.5, bloom=0, rough=1.2, feather=0.8)
    # blush from the heart outwards
    heart = circles(W, H, [(*P(0, r * 0.02), r * 0.42)])
    art = G(art, gaussian_filter(heart, r * 0.12) * allm, blush, seed=nx(), density=0.55 if kind == "putih" else 0.5, edge=0, bloom=0.2, rough=2, feather=2)
    # veins on the broad petals
    vs = []
    for sx in (-1, 1):
        for a in np.linspace(-0.7, 0.7, 6):
            L = r * rng.uniform(0.55, 0.78)
            vs.append(([P(sx * r * 0.08, -r * 0.02), P(sx * (r * 0.08 + math.cos(a) * L * 0.5), -r * 0.02 + math.sin(a) * L * 0.35), P(sx * (r * 0.08 + math.cos(a) * L), -r * 0.02 + math.sin(a) * L * 0.62)], max(0.8, r * 0.012), (0.05, 0.6)))
    art = G(art, strokes(W, H, [(curve(p, 10), w, t) for p, w, t in vs]) * allm, vein, seed=nx(), density=0.3 if kind == "putih" else 0.34, edge=0, bloom=0, rough=0.6, feather=0.5)
    # lip: two side lobes + mid lobe with forked tip
    lipc = "#a3266a" if kind == "putih" else "#6a1d63"
    lob = [poly(_blob(sx * r * 0.17, r * 0.05, r * 0.13, r * 0.19, sx * 0.4, rng, 12, 1, 0.05)) for sx in (-1, 1)]
    mid = poly(petal_pts(0, r * 0.04, r * 0.5, r * 0.17, math.pi / 2, n=12))
    lip = shapes(W, H, lob + [mid])
    art = G(art, lip, "#c64a86" if kind == "putih" else "#8f3a8a", lipc, seed=nx(), density=0.82, edge=0.65, bloom=0.1, rough=1.4, feather=0.7)
    tend = strokes(W, H, [(curve([P(sx * r * 0.04, r * 0.5), P(sx * r * 0.12, r * 0.58), P(sx * r * 0.1, r * 0.66)], 10), max(1, r * 0.022), (0.1, 0.6)) for sx in (-1, 1)])
    art = G(art, tend, lipc, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.5, feather=0.5)
    throat = circles(W, H, [(*P(0, r * 0.02), r * 0.075)])
    art = G(art, throat, "#f0c24e", "#e39a35", seed=nx(), density=0.88, edge=0.5, bloom=0, rough=0.8, feather=0.6)
    col = shapes(W, H, [poly(_blob(0, -r * 0.06, r * 0.07, r * 0.12, 0, rng, 10, 1, 0.03))])
    art = G(art, col, "#fbf6f0", "#eadde4", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.6, feather=0.5)
    return art


def phal_bud(art, W, H, x, y, s, ang, rng, nx, kind="putih"):
    col, rim = ("#f5eef4", "#b49dc0") if kind == "putih" else ("#b56aae", "#7a3b80")
    m = shapes(W, H, [deform(ellipse_pts(x, y, s * 1.05, s * 0.74, 18, ang), rng, 1, 0.03)])
    art = G(art, m, col, "#dfe3c8" if kind == "putih" else "#9b4d98", seed=nx(), density=0.75, edge=0.55, bloom=0.1, rough=1.2, feather=0.8)
    art = G(art, np.clip(m - gaussian_filter(m, s * 0.18), 0, 1) * 2, rim, seed=nx(), density=0.5, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    return art


def orchid_spray(W, H, path, flowers, buds, seed, kind="putih", stem_w=7.0, roots=()):
    """An arching flower spike: a green-brown stem along path, flowers [(t, r, rot, face)] and buds [(t, s)]
    placed along it (t in 0..1). Returns RGBA."""
    rng = random.Random(seed)
    cnt = [seed * 100]

    def nx():
        cnt[0] += 17
        return cnt[0]
    art = blank(W, H)
    C = curve(path, 220)
    stem = strokes(W, H, [(C, stem_w, (0.0, 0.35))])
    art = G(art, stem, "#6f7f4a", "#5a4a3a", seed=nx(), density=0.85, edge=0.55, bloom=0.1, rough=1.2, feather=0.7)
    for pts, w in roots:
        art = G(art, strokes(W, H, [(curve(pts, 40), w, (0.1, 0.5))]), "#9aa38a", "#b7b39c", seed=nx(), density=0.6, edge=0.6, bloom=0, rough=1, feather=0.7)

    def at(t):
        i = min(len(C) - 2, int(t * (len(C) - 1)))
        return C[i], math.atan2(C[i + 1][1] - C[i][1], C[i + 1][0] - C[i][0])
    for t, s in buds:
        (bx, by), h = at(t)
        ba = h + (1.1 if len(C) and (t * 100) % 2 < 1 else 0.7)
        ox, oy = bx + math.cos(ba) * s * 0.9, by + math.sin(ba) * s * 0.9
        art = G(art, strokes(W, H, [([(bx, by), (ox, oy)], max(1.2, s * 0.22), None)]), "#7a8a52", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.6, feather=0.5)
        art = phal_bud(art, W, H, ox + math.cos(ba) * s * 0.9, oy + math.sin(ba) * s * 0.9, s * 0.95, ba, rng, nx, kind)
    for t, r, rot, face in flowers:
        (fx, fy), h = at(t)
        side = 1.45 if face > 0 else -1.45
        face = abs(face)
        ox, oy = fx + math.cos(h + side) * r * 0.55, fy + math.sin(h + side) * r * 0.55
        art = G(art, strokes(W, H, [([(fx, fy), ((fx + ox) / 2, (fy + oy) / 2 - r * 0.06), (ox, oy)], max(1.5, r * 0.045), None)]), "#7a8a52", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.6, feather=0.5)
        art = phal(art, W, H, ox, oy, r, rng, nx, rot=rot, kind=kind, face=face)
        clear()
    return art


def leaf_broad(art, W, H, x, y, L, Wd, ang, rng, nx, cols=("#7f9a5e", "#4f6d3c"), bend=0.25):
    """Thick, glossy orchid leaf (broad strap with rounded tip) in watercolour."""
    pts = []
    n = 16
    for i in range(n + 1):
        t = i / n
        a = ang + bend * t
        cx_, cy_ = x + math.cos(ang) * L * t + math.cos(a + math.pi / 2) * bend * L * 0.25 * t * t, y + math.sin(ang) * L * t + math.sin(a + math.pi / 2) * bend * L * 0.25 * t * t
        pts.append((cx_, cy_, a))
    left = [(px - math.sin(a) * Wd * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 0.9 + 0.1))) * (1 - t ** 4), py + math.cos(a) * Wd * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 0.9 + 0.1))) * (1 - t ** 4)) for (px, py, a), t in zip(pts, np.linspace(0, 1, n + 1))]
    right = [(px + math.sin(a) * Wd * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 0.9 + 0.1))) * (1 - t ** 4), py - math.cos(a) * Wd * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 0.9 + 0.1))) * (1 - t ** 4)) for (px, py, a), t in zip(pts, np.linspace(0, 1, n + 1))]
    m = shapes(W, H, [deform(left + right[::-1], rng, 1, 0.02)])
    art = G(art, m, cols[0], cols[1], seed=nx(), density=0.78, edge=0.55, bloom=0.35, rough=2.5, feather=1.0)
    mid = strokes(W, H, [([(p[0], p[1]) for p in pts[:-2]], max(1.0, Wd * 0.06), (0.05, 0.4))])
    return G(art, mid, cols[1], seed=nx(), density=0.45, edge=0.2, bloom=0, rough=0.6, feather=0.6)


# ================================================================ N5: frost, ice crystals, snowy twigs
def frost_fern(x, y, ang, L, w, depth, rng, out, spread=1.05, step=None):
    """Dendritic frost: a slightly wandering spine with alternating side shoots (~60 deg) that recurse."""
    step = step or max(3.0, L / 26)
    pts = [(x, y)]; a = ang; s = 0.0
    while s < L:
        a += rng.gauss(0, 0.05)
        x += math.cos(a) * step; y += math.sin(a) * step; s += step
        pts.append((x, y))
    out.append((pts, w))
    if depth <= 0:
        return out
    n = len(pts)
    k = 0
    for i in range(2, n - 1, max(1, int(rng.uniform(1.0, 2.2)))):
        t = i / n
        side = 1 if k % 2 == 0 else -1
        k += 1
        sl = L * (1 - t) * rng.uniform(0.32, 0.55)
        if sl < 4:
            continue
        frost_fern(pts[i][0], pts[i][1], a + side * spread * rng.uniform(0.85, 1.15), sl, w * 0.62, depth - 1, rng, out, spread)
    return out


def crystal_arm(cx, cy, R, rng, kind=0):
    """One arm of a six-fold snow crystal (pointing up): spine + paired side branches / plates. Returns
    (stroke items, polygons) in absolute coords."""
    items, polys = [], []
    items.append(([(cx, cy), (cx, cy - R)], R * 0.05, (0.0, 0.3)))
    if kind == 0:  # fern-like stellar dendrite
        for t in np.linspace(0.24, 0.88, 5):
            L = (0.42 - 0.38 * (t - 0.22)) * rng.uniform(0.85, 1.1)
            for sd in (-1, 1):
                bx, by = cx, cy - R * t
                ex, ey = bx + sd * math.sin(math.pi / 3) * R * L, by - math.cos(math.pi / 3) * R * L
                items.append(([(bx, by), (ex, ey)], R * 0.034, (0.0, 0.5)))
    elif kind == 1:  # sectored plate with a hex tip
        for t, L in ((0.45, 0.28), (0.7, 0.2)):
            for sd in (-1, 1):
                bx, by = cx, cy - R * t
                polys.append([(bx, by + R * 0.04), (bx + sd * R * L * 0.87, by - R * L * 0.5), (bx + sd * R * L * 0.7, by - R * L * 0.62), (bx, by - R * 0.1)])
        hx, hy = cx, cy - R * 0.92
        polys.append([(hx + math.cos(k * math.pi / 3) * R * 0.11, hy + math.sin(k * math.pi / 3) * R * 0.11) for k in range(6)])
    else:  # broad-branch: wide plate near the centre + long needles
        polys.append([(cx, cy), (cx - R * 0.16, cy - R * 0.3), (cx, cy - R * 0.42), (cx + R * 0.16, cy - R * 0.3)])
        for t, L in ((0.55, 0.3), (0.75, 0.2)):
            for sd in (-1, 1):
                bx, by = cx, cy - R * t
                items.append(([(bx, by), (bx + sd * 0.87 * R * L, by - 0.5 * R * L)], R * 0.05, (0.0, 0.5)))
    return items, polys


def crystal_masks(W, H, cx, cy, R, rng, kind=0, rot=0.0):
    it_all, po_all = [], []
    for k in range(6):
        a = rot + k * math.pi / 3
        items, polys = crystal_arm(cx, cy, R, rng, kind)
        it_all += [([tuple(p) for p in rotp(pts, cx, cy, a)], w, tp) for pts, w, tp in items]
        po_all += [rotp(p, cx, cy, a) for p in polys]
    centre = [(cx + math.cos(rot + k * math.pi / 3 + math.pi / 6) * R * 0.12, cy + math.sin(rot + k * math.pi / 3 + math.pi / 6) * R * 0.12) for k in range(6)]
    po_all.append(centre)
    m = np.maximum(strokes(W, H, it_all), shapes(W, H, po_all, smooth=False))
    return m


def ice(dst, mask, seed=1, edge="#4f74a0", body="#f4f9fd", alpha=0.95, halo=0.5):
    """Clear ice: soft white body, bluish refracted rim, faint glow halo."""
    out = dst
    if halo:
        out = over(out, glow(mask, "#ffffff", radius=3, strength=halo * 0.5))
    H, W = mask.shape
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    inner = gaussian_filter(m, 1.1)
    rim = np.clip(m - inner, 0, 1) * 3.0
    n = noise(W, H, seed, 2.0)
    rgb = flat(H, W, body) * (0.93 + 0.07 * n[..., None])
    e = np.array(hex_rgb(edge), np.float32)
    rgb = rgb * (1 - np.clip(rim, 0, 1)[..., None] * 0.55) + e * np.clip(rim, 0, 1)[..., None] * 0.55
    a = m * (0.55 + 0.45 * np.clip(rim + 0.4 * n, 0, 1)) * alpha
    return over(out, rgba(np.clip(rgb, 0, 1), a))


def twig(x, y, ang, L, w, depth, rng, out, droop=0.0):
    pts = [(x, y)]; a = ang; s = 0.0; step = max(3.0, L / 18)
    while s < L:
        a += rng.gauss(0, 0.09) + droop * 0.01
        x += math.cos(a) * step; y += math.sin(a) * step; s += step
        pts.append((x, y))
    out.append((pts, w))
    if depth > 0:
        n = len(pts)
        for i in range(3, n - 2, max(2, int(n / rng.uniform(2.5, 4)))):
            sd = -1 if rng.random() < 0.72 else 1
            twig(pts[i][0], pts[i][1], a + sd * rng.uniform(0.45, 0.9), L * (1 - i / n) * rng.uniform(0.45, 0.7), w * 0.6, depth - 1, rng, out, droop)
    return out


# ================================================================ N5: kids' art (crayon) + gouache people helpers
def crayon(mask, col, seed=1, tooth=0.55, density=0.95):
    """Wax crayon on drawing paper: colour catches the paper tooth (speckled gaps), slightly waxy edge."""
    h, w = mask.shape
    m = displace(mask, seed, 1.4, 8)
    t = noise(w, h, seed + 3, 0.8) * 0.6 + noise(w, h, seed + 4, (0.6, 2.4)) * 0.4
    cov = np.clip((t - (1 - tooth) * 0.7) * 3.2, 0, 1)
    a = np.clip(m * 1.3, 0, 1) * cov * density
    return rgba(flat(h, w, col) * (0.94 + 0.12 * t[..., None]), np.clip(a, 0, 1))


def CR(dst, mask, *a, pad=8, **k):
    return OV(dst, mask, lambda m: crayon(m, *a, **k), pad=pad)


def scribble_fill(W, H, poly, gap=7.0, ang=0.7, width=4.5, rng=None):
    """Child-like back-and-forth crayon hatching clipped to a polygon."""
    rng = rng or random.Random(1)
    m = shapes(W, H, [poly], smooth=False)
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    R = max(max(xs) - min(xs), max(ys) - min(ys))
    items = []
    d = -R
    while d < R:
        p0 = (cx + math.cos(ang) * -R - math.sin(ang) * d, cy + math.sin(ang) * -R + math.cos(ang) * d)
        p1 = (cx + math.cos(ang) * R - math.sin(ang) * d, cy + math.sin(ang) * R + math.cos(ang) * d)
        items.append(([p0, p1], width * rng.uniform(0.8, 1.2), None))
        d += gap * rng.uniform(0.8, 1.2)
    return strokes(W, H, items) * gaussian_filter(m, 1.0)
