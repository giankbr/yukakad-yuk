"""Agent D4 helpers (cyanotype-biru, shibori-indigo, karang-laut, musim-gugur): builds on _a5_lib (_j1_lib bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, wrap helpers) and adds botanical silhouettes + cyanotype exposure,
indigo cloth / shibori resist, underwater water + caustics, translucent veined leaves.
Previews -> /tmp/pen/nb-D4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-D4/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _a5_lib import *  # noqa
import _a5_lib, _j1_lib
_a5_lib.PREV = _j1_lib.PREV = _p1_lib.PREV = "/tmp/pen/nb-D4/art"
PREV = _p1_lib.PREV


def norm(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-6)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def lerp3(c0, c1, t):
    a = np.array(hex_rgb(c0), np.float32); b = np.array(hex_rgb(c1), np.float32)
    return a * (1 - t[..., None]) + b * t[..., None]


# ───────────────────────── botanical silhouettes (masks) ─────────────────────────

def fern_items(rach, rng, scale=1.0, lean=1.42, pinn=True, w0=4.0):
    """Fern frond: rachis polyline + pinnae made of rounded pinnules. Returns (polys, strokes)."""
    polys, st = [], []
    pts = along(rach, 27 * scale)
    N = len(pts)
    n = len(rach)
    st += [([rach[i], rach[i + 1]], w0 * scale * (1 - 0.7 * i / n), None) for i in range(n - 1)]
    for i, (x, y, a) in enumerate(pts[1:], 1):
        t = i / N
        L = (30 + 95 * math.sin(math.pi * min(1, t * 1.05 + 0.08)) ** 0.9) * (1 - t * 0.5) * scale
        for sg in (-1, 1):
            aa = a + sg * (lean - t * 0.45) + rng.uniform(-.06, .06)
            # pinna midrib slightly curved toward tip
            mid = [(x + math.cos(aa + sg * 0.12 * u) * L * u, y + math.sin(aa + sg * 0.12 * u) * L * u) for u in np.linspace(0, 1, 8)]
            st.append((mid, 1.9 * scale, (0.0, 0.5)))
            if pinn:
                k = max(3, int(L / (10 * scale)))
                for j in range(k):
                    u = (j + 0.5) / (k + 0.2)
                    px, py = x + math.cos(aa) * L * u, y + math.sin(aa) * L * u
                    pl = ((1 - u * 0.7) * L * 0.16 + 3 * scale) * rng.uniform(0.9, 1.1)
                    for s2 in (-1, 1):
                        polys.append(petal_pts(px, py, pl, pl * 0.36, aa + s2 * 1.15 + (1 - u) * 0.1 * s2, n=10))
                polys.append(petal_pts(x + math.cos(aa) * L * 0.92, y + math.sin(aa) * L * 0.92, L * 0.12, L * 0.04, aa, n=10))
            else:
                polys.append(petal_pts(x, y, L, L * 0.13, aa, n=14))
    return polys, st


def grass_items(base, top, rng, width=3.0, seeds=True, n_spk=14):
    """A grass stem (curve base→top) with an oat-like seed head of small spikelets."""
    ctrl = [base, ((base[0] * 2 + top[0]) / 3 + rng.uniform(-14, 14), (base[1] * 2 + top[1]) / 3),
            ((base[0] + top[0] * 2) / 3 + rng.uniform(-18, 18), (base[1] + top[1] * 2) / 3), top]
    stem = curve(ctrl, 40)
    st = [(stem, width, (0.0, 0.35))]
    polys = []
    if seeds:
        head = stem[int(len(stem) * 0.55):]
        for (x, y, a) in along(head, max(6, len(head) * 2.2 / n_spk)):
            for sg in (-1, 1):
                if rng.random() < 0.85:
                    aa = a + sg * rng.uniform(0.35, 0.6)
                    L = rng.uniform(10, 17) * width / 3
                    pend = [(x, y), (x + math.cos(aa) * L * 0.4, y + math.sin(aa) * L * 0.4)]
                    st.append((pend, 0.9, None))
                    polys.append(petal_pts(pend[1][0], pend[1][1], L, L * 0.2, aa, n=10))
    return polys, st


def blade_poly(base, top, width, bend, n=14):
    """A tapered grass blade outline."""
    bx, by = base; tx, ty = top
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy); nx_, ny_ = -dy / L, dx / L
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        cx = bx + dx * t + nx_ * bend * math.sin(t * math.pi * 0.9) * L * 0.18
        cy = by + dy * t + ny_ * bend * math.sin(t * math.pi * 0.9) * L * 0.18
        w = width * (1 - t) ** 0.8 * 0.5
        left.append((cx + nx_ * w, cy + ny_ * w)); right.append((cx - nx_ * w, cy - ny_ * w))
    return left + right[::-1]


def lace_items(cx, cy, r, rng, stem_to=None, rays=15, sub=11):
    """Queen Anne's lace umbel: rays to sub-umbels, each with tiny florets. Returns (strokes, dots)."""
    st, dots_ = [], []
    if stem_to:
        st.append((curve([stem_to, ((stem_to[0] + cx) / 2 + rng.uniform(-20, 20), (stem_to[1] + cy) / 2), (cx, cy + r * 0.55)], 30), 3.4, (0.0, 0.2)))
    hub = (cx, cy + r * 0.55)
    for k in range(rays):
        a = -math.pi / 2 + (k / (rays - 1) - 0.5) * 2.5 + rng.uniform(-.05, .05)
        rr = r * rng.uniform(0.75, 1.0) * (0.85 + 0.15 * math.cos(a + math.pi / 2))
        ex, ey = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.62 + r * 0.1
        st.append(([hub, ((hub[0] + ex) / 2, (hub[1] + ey) / 2 - r * 0.04), (ex, ey)], 1.3, (0.0, 0.3)))
        sr = r * rng.uniform(0.16, 0.22)
        for j in range(sub):
            b = -math.pi / 2 + (j / (sub - 1) - 0.5) * 2.7
            fx, fy = ex + math.cos(b) * sr, ey + math.sin(b) * sr * 0.7 - sr * 0.15
            st.append(([(ex, ey), (fx, fy)], 0.7, None))
            dots_.append((fx, fy, rng.uniform(1.3, 2.3) * r / 90))
        dots_.append((ex, ey - sr * 0.3, 2.2 * r / 90))
    return st, dots_


# ───────────────────────── cyanotype ─────────────────────────
PRUSSIAN, PRUSSIAN_D, PRUSSIAN_L = "#1f4a80", "#102f5c", "#5a83b4"
CY_PAPER = "#eef1ee"


def coat_mask(W, H, seed, inset=(30, 40, 30, 40), strokes_n=9, dry=0.6):
    """Brush-coated sensitiser (horizontal brush passes): bristle fingers at the left/right ends, wavy overlapping pass
    edges at top/bottom, streaky density. Returns coat density 0..1."""
    rng = np.random.default_rng(seed)
    l, t, r_, b = inset
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # per-row bristle length (fingers): noise that varies along y, constant along x
    rows = norm(gaussian_filter(rng.random((H, 1)).astype(np.float32), (2.2, 0)))
    rows2 = norm(gaussian_filter(rng.random((H, 1)).astype(np.float32), (6, 0)))
    reach = (rows * 0.55 + rows2 * 0.45 - 0.5) * 2  # -1..1
    lx = l + reach * l * 0.55 * dry
    rx = W - r_ - ((norm(gaussian_filter(rng.random((H, 1)).astype(np.float32), (2.2, 0))) * 0.55 + rows2[::-1] * 0.45) - 0.5) * 2 * r_ * 0.55 * dry
    fx = np.clip(np.minimum(xx - lx, rx - xx) / 3.0, 0, 1)
    # passes: wavy top/bottom borders
    band = (H - t - b) / max(1, strokes_n)
    wav = (fbm(W, 8, seed + 3, 60, 2)[0] - 0.5) * band * 0.35
    wav2 = (fbm(W, 8, seed + 4, 60, 2)[0] - 0.5) * band * 0.35
    fy = np.clip(np.minimum(yy - (t + wav[None, :]), (H - b + wav2[None, :]) - yy) / 2.5, 0, 1)
    m = fx * fy
    # dry-brush gaps near the ends of each pass
    st = norm(gaussian_filter(rng.random((H, W)).astype(np.float32), (0.7, 18)))
    near = np.clip(1 - np.minimum(xx - lx, rx - xx) / (W * 0.18), 0, 1)
    m *= 1 - np.clip((st - (1 - dry * 0.45)) * 6, 0, 1) * near
    # density: overlapping pass bands + streaks
    pass_ = 0.5 + 0.5 * np.cos((yy - t) / band * math.tau)
    dens = 0.86 + 0.06 * pass_ + 0.08 * norm(gaussian_filter(rng.random((H, W)).astype(np.float32), (1.5, 30)))
    m = displace(m, seed, 1.5, 10)
    return np.clip(gaussian_filter(m, 0.6), 0, 1) * dens


def cyanotype(W, H, coat, objects, seed, paper_col=CY_PAPER, blue=PRUSSIAN, deep=PRUSSIAN_D, light=PRUSSIAN_L, opaque_bg=False):
    """Sun print: coat density × (1 - shadow). objects: list of (mask, opacity, softness_px). Soft edges vary across the
    sheet (parts lifted off the glass), translucent tissue lets some light through (paler blue, not white)."""
    shade = np.zeros((H, W), np.float32)
    lift = fbm(W, H, seed + 4, 160, 2)
    for m, op, soft in objects:
        a = gaussian_filter(m, soft * 0.45)
        b = gaussian_filter(m, soft * 1.6)
        sm = a * (1 - lift) + b * lift
        tissue = op * (0.88 + 0.12 * fbm(W, H, seed + 7, 30, 2))
        shade = 1 - (1 - shade) * (1 - np.clip(sm * tissue, 0, 1))
    expo = coat * (1 - shade)
    # exposure gradient across the sheet + mottled chemistry
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    grad = 0.86 + 0.14 * (1 - (xx / W * 0.4 + yy / H * 0.6))
    mott = 0.9 + 0.1 * fbm(W, H, seed + 9, 60, 3)
    e = np.clip(expo * grad * mott, 0, 1)
    col = lerp3(light, blue, np.clip(e * 1.4, 0, 1))
    col = col * (1 - np.clip((e - 0.7) * 2, 0, 1)[..., None] * 0.35) + np.array(hex_rgb(deep), np.float32) * (np.clip((e - 0.7) * 2, 0, 1)[..., None] * 0.35)
    pap = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(paper_col), np.float32)
    pap *= (1 + (fbm(W, H, seed + 2, 6, 2) - 0.5) * 0.04)[..., None]
    k = np.clip(e * 1.25, 0, 1)[..., None]
    rgb = pap * (1 - k) + col * k
    # faint residual blue staining in highlights (washed sensitiser)
    stain = coat[..., None] * shade[..., None] * 0.08
    rgb = rgb * (1 - stain) + np.array(hex_rgb(light), np.float32) * stain
    g = gaussian_filter(np.random.default_rng(seed + 3).random((H, W)).astype(np.float32), 0.6)
    rgb *= (1 + (g - 0.5) * 0.05)[..., None]
    return rgb


def silhouette(W, H, objects, seed, col="#eef3f6", strength=1.0):
    """White sun-print silhouette alone (RGBA) for laying over CSS blue: soft lifted edges + tissue translucency."""
    shade = np.zeros((H, W), np.float32)
    lift = fbm(W, H, seed + 4, 140, 2)
    for m, op, soft in objects:
        a = gaussian_filter(m, soft * 0.45); b = gaussian_filter(m, soft * 1.6)
        sm = a * (1 - lift) + b * lift
        tissue = op * (0.86 + 0.14 * fbm(W, H, seed + 7, 26, 2))
        shade = 1 - (1 - shade) * (1 - np.clip(sm * tissue, 0, 1))
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    rgb *= (1 - (1 - shade[..., None]) * 0.12)
    return rgba(rgb, shade * strength)


# ───────────────────────── indigo cloth / shibori ─────────────────────────
INDIGO, INDIGO_D, INDIGO_L, UNDYED = "#1f3566", "#14244a", "#5b74a6", "#ecebe4"


def weave(W, H, seed, pitch=3.0, wrap=True):
    """Plain-weave thread texture (−1..1): over/under warp+weft with thread slub."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.default_rng(seed)
    md = "wrap" if wrap else "reflect"
    slub_x = gaussian_filter(rng.random((1, W)).astype(np.float32), (0, 1.2), mode=md)
    slub_y = gaussian_filter(rng.random((H, 1)).astype(np.float32), (1.2, 0), mode=md)
    wx = np.sin(xx / pitch * math.pi) ** 2
    wy = np.sin(yy / pitch * math.pi) ** 2
    cell = ((np.floor(xx / pitch) + np.floor(yy / pitch)) % 2).astype(np.float32)
    t = cell * wy + (1 - cell) * wx
    t = t * 0.7 + 0.3 * (norm(slub_x) * 0.5 + norm(slub_y) * 0.5)
    return (t - 0.5) * 2


def _wn(W, H, rng, sig, md):
    return norm(gaussian_filter(rng.random((H, W)).astype(np.float32), sig, mode=md))


def dye(W, H, resist, seed, wrap=True, bleed=5.0, base=INDIGO, deep=INDIGO_D, light=INDIGO_L, undyed=UNDYED, pitch=2.6, depth=1.0, rough=3.0):
    """Indigo-dyed cloth: resist (0..1, 1 = protected) is roughened by the fibres, bleeds in feathery capillary fingers
    along warp and weft, is only partly protected inside (mottled pale blue), and the dye pools darker at its rim.
    Base dye is uneven (several dips). Returns RGB."""
    md = "wrap" if wrap else "reflect"
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dxn = (_wn(W, H, rng, 7, md) - 0.5) * 2 * rough; dyn = (_wn(W, H, rng, 7, md) - 0.5) * 2 * rough
    r0 = map_coordinates(resist, [(yy + dyn) % H if wrap else yy + dyn, (xx + dxn) % W if wrap else xx + dxn], order=1, mode="wrap" if wrap else "nearest")
    r1 = gaussian_filter(r0, (bleed * 0.2, bleed * 1.2), mode=md)
    r2 = gaussian_filter(r0, (bleed * 1.2, bleed * 0.2), mode=md)
    soft = np.maximum(r1, r2) * 0.55 + gaussian_filter(r0, bleed * 0.6, mode=md) * 0.45
    f = (_wn(W, H, rng, (0.5, 3.0), md) + _wn(W, H, rng, (3.0, 0.5), md)) * 0.5
    blot = _wn(W, H, rng, 10, md)
    res = np.clip((soft - 0.45 + (f - 0.5) * 0.7 + (blot - 0.5) * 0.25) * 2.0 + 0.5, 0, 1)
    res = res * (0.72 + 0.28 * _wn(W, H, rng, 4, md)) * np.clip(gaussian_filter(r0, 1.0, mode=md) * 0.3 + 0.75, 0, 1)
    res = np.clip(res * 1.15, 0, 1)
    # dye pools darker just outside the resist
    rim = np.clip(gaussian_filter(r0, bleed * 1.6, mode=md) - r0 * 0.9, 0, 1) * (1 - res)
    lo = _wn(W, H, rng, 46, md); mid = _wn(W, H, rng, 12, md)
    d = np.clip((0.72 + 0.28 * lo) * (0.9 + 0.1 * mid) * depth + rim * 0.5, 0, 1.2)
    dyed = lerp3(light, base, np.clip((d - 0.42) * 2.4, 0, 1))
    dark = np.clip((d - 0.85) * 3, 0, 1)[..., None]
    dyed = dyed * (1 - dark * 0.6) + np.array(hex_rgb(deep), np.float32) * dark * 0.6
    # slight colour drift between dips (greener / redder indigo)
    drift = (_wn(W, H, rng, 60, md) - 0.5)[..., None] * np.array([-0.02, 0.012, -0.01], np.float32)
    dyed = dyed + drift
    pale = lerp3(undyed, light, np.clip((1 - res) * 0.9 + (1 - _wn(W, H, rng, 5, md)) * 0.12, 0, 1))
    rgb = dyed * (1 - res[..., None]) + pale * res[..., None]
    wv = weave(W, H, seed + 5, pitch, wrap)
    rgb *= (1 + wv[..., None] * (0.05 + 0.05 * (1 - res[..., None])))
    return np.clip(rgb, 0, 1)


def wrap_strokes(W, H, items):
    """strokes() with wrap-around copies for seamless tiles."""
    out = []
    for it in items:
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):
                out.append(([(x + dx, y + dy) for x, y in it[0]],) + tuple(it[1:]))
    return strokes(W, H, out)


# ───────────────────────── leaves ─────────────────────────

def maple_poly(cx, cy, s, ang, rng, lobes=5):
    """Palmate maple leaf outline (5 pointed lobes with small teeth), stem point at (cx, cy) pointing down along ang."""
    pts = []
    # lobe tips: angles relative to leaf axis (up = 0)
    tips = [(-1.65, 0.55), (-0.95, 0.88), (0.0, 1.0), (0.95, 0.88), (1.65, 0.55)] if lobes == 5 else [(-1.1, 0.8), (0.0, 1.0), (1.1, 0.8)]
    sinus = 0.42
    ca, sa = math.cos(ang), math.sin(ang)
    def P(a, r):
        x, y = math.sin(a) * r * s, -math.cos(a) * r * s
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    base_a = [-2.35, 2.35]
    seq = [(base_a[0], 0.2)]
    for i, (a, r) in enumerate(tips):
        r *= rng.uniform(0.93, 1.05)
        prev = tips[i - 1][0] if i else base_a[0]
        if i:
            seq.append(((a + prev) / 2, 0.5 * rng.uniform(0.92, 1.08)))
        w = 0.3 if abs(a) < 1.2 else 0.26
        seq += [(a - w, r * 0.6), (a - w * 0.62, r * 0.8), (a - w * 0.42, r * 0.76), (a - w * 0.2, r * 0.92), (a - w * 0.1, r * 0.9),
                (a, r),
                (a + w * 0.1, r * 0.9), (a + w * 0.2, r * 0.92), (a + w * 0.42, r * 0.76), (a + w * 0.62, r * 0.8), (a + w, r * 0.6)]
    seq.append((base_a[1], 0.2))
    seq.append((math.pi, 0.06))
    return [P(a, r) for a, r in seq]


def oak_poly(cx, cy, s, ang, rng, lobes=4):
    """Rounded-lobed oak leaf, stem at (cx, cy), axis along ang (pointing away from stem)."""
    ca, sa = math.cos(ang), math.sin(ang)
    left, right = [], []
    n = 60
    for i in range(n + 1):
        t = i / n
        env = math.sin(math.pi * min(1, t * 1.05)) ** 0.7 * (0.55 + 0.45 * t)
        lob = 0.62 + 0.38 * abs(math.sin(t * math.pi * (lobes + 0.5)))
        w = env * lob * 0.42 * s
        u = t * s
        for side, lst in ((1, left), (-1, right)):
            wj = w * (1 + rng.uniform(-0.03, 0.03))
            lst.append((u, side * wj))
    pts = [(0, 0)] + left + right[::-1]
    return [(cx + u * ca - v * sa, cy + u * sa + v * ca) for u, v in pts]


def veins(cx, cy, s, ang, kind="maple", rng=None):
    """Vein strokes for a leaf drawn by maple_poly/oak_poly."""
    st = []
    ca, sa = math.cos(ang), math.sin(ang)
    def T(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    if kind == "maple":
        for a, r in [(-1.65, 0.5), (-0.95, 0.8), (0.0, 0.92), (0.95, 0.8), (1.65, 0.5)]:
            main = [(cx + (math.sin(a) * r * s * t) * math.cos(ang - math.pi / 2) * 0 + 0, 0) for t in (0,)]
            pts = []
            for t in np.linspace(0, 1, 10):
                x, y = math.sin(a) * r * s * t, -math.cos(a) * r * s * t
                # leaf axis up(-y) rotated by ang - this mirrors maple_poly's P()
                pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
            st.append((pts, max(1.0, s * 0.022), (0.0, 0.7)))
            for t in (0.35, 0.6):
                x0, y0 = math.sin(a) * r * s * t, -math.cos(a) * r * s * t
                for sg in (-1, 1):
                    b = a + sg * 0.75
                    x1, y1 = x0 + math.sin(b) * r * s * 0.18, y0 - math.cos(b) * r * s * 0.18
                    st.append(([(cx + x0 * math.cos(ang) - y0 * math.sin(ang), cy + x0 * math.sin(ang) + y0 * math.cos(ang)),
                                (cx + x1 * math.cos(ang) - y1 * math.sin(ang), cy + x1 * math.sin(ang) + y1 * math.cos(ang))], max(.6, s * 0.01), (0.0, 0.8)))
    else:
        st.append(([T(u * s, 0) for u in np.linspace(0, 0.95, 10)], max(1.0, s * 0.02), (0.0, 0.6)))
        for k in range(1, 9):
            u = k / 9.5
            side = 1 if k % 2 else -1
            for sg in (-1, 1):
                st.append(([T(u * s, 0), T((u + 0.08) * s, sg * 0.3 * s * math.sin(math.pi * u) ** 0.6)], max(.6, s * 0.01), (0.0, 0.8)))
    return st
