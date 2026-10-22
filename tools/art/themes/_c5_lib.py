"""Agent C5 helpers (padang-liar, batik-kontemporer, ultah-unicorn, ultah-bola): builds on _j1_lib (bbox-cropped
G/GP/LC/FO/OV, strokes/shapes/circles/ellipses) and adds wildflowers (cosmos, chamomile, cornflower, grasses),
wax-resist batik dye with crackle, soft gouache shading and crayon lines. Previews -> /tmp/pen/nb-C5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_PV = "/tmp/pen/nb-C5/art"
os.makedirs(_PV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = _PV
_j1_lib.PREV = _PV
import art as _art
PREV = _PV


def clear():
    _art._fbm_cache.clear()


def col_arr(mask, col, alpha):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(alpha, 0, 1)[..., None]], -1)


def tint(dst, soft, col, amt=0.5, seed=1, streak=0.6, clip=True):
    """Soft gouache shading: alpha follows a soft mask with brush-streak breakup, kept inside dst."""
    b = bbox(soft, 4, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    s = soft[y0:y1, x0:x1]
    st = gaussian_filter(np.random.default_rng(seed).random(s.shape).astype(np.float32), (1.2, 2.2))
    st = (st - st.mean()) / (st.std() + 1e-6)
    lo = fbm(x1 - x0, y1 - y0, seed + 3, 26, 3) - 0.5
    a = s * amt * np.clip(1 + st * 0.12 * streak + lo * 0.6 * streak, 0, 2)
    if clip:
        a = a * dst[y0:y1, x0:x1, 3]
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], col_arr(s, col, a))
    return out


def side_light(mask, dx, dy, blur):
    sh = np.roll(np.roll(gaussian_filter(mask, blur), int(dy), 0), int(dx), 1)
    return np.clip(mask - sh, 0, 1) * mask


def inner_edge(mask, px=2.0):
    return np.clip(mask - (gaussian_filter(mask, px) > 0.97).astype(np.float32), 0, 1) * mask


def crayon(dst, mask_line, col, seed=1, amt=0.85, tooth=0.45):
    b = bbox(mask_line, 4, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = mask_line[y0:y1, x0:x1]
    g = gaussian_filter(np.random.default_rng(seed).random(m.shape).astype(np.float32), 0.55)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    a = m * amt * np.clip((g - tooth * 0.6) * 2.4, 0.15, 1)
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], col_arr(m, col, a))
    return out


def body(art, m, col, col2, dark, light, nx, ldir=(-12, -14), line=None, blur=8):
    """Gouache body with soft shadow side + light side + optional crayon outline."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.45)
    art = tint(art, side_light(m, *ldir, blur), dark, 0.7, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .7, -ldir[1] * .7, blur * .8), light, 0.55, seed=nx())
    if line:
        art = crayon(art, inner_edge(m, 2.0), line, seed=nx(), amt=0.75, tooth=0.3)
    return art


def rot(pts, cx, cy, a):
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def squash(pts, cx, cy, k, a=0.0):
    """Foreshorten a flat flower: compress along direction a by k (tilted flower face)."""
    out = []
    ca, sa = math.cos(a), math.sin(a)
    for x, y in pts:
        dx, dy = x - cx, y - cy
        u = dx * ca + dy * sa; v = -dx * sa + dy * ca
        u *= k
        out.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return out


# ---------------- wildflowers (watercolour) ----------------
def cosmos_petal(cx, cy, R, ang, rng, wid=0.44):
    """Broad cosmos petal: narrow at the centre, wide fan with a notched (3-tooth) tip."""
    L = R * rng.uniform(0.9, 1.05)
    half = wid * rng.uniform(0.85, 1.1)
    pts = [(cx + math.cos(ang) * R * 0.08, cy + math.sin(ang) * R * 0.08)]
    for t, side in ((0.3, -0.75), (0.75, -1.05)):
        a = ang + side * half
        pts.append((cx + math.cos(a) * L * t, cy + math.sin(a) * L * t))
    tips = 7
    for i in range(tips):
        u = -1 + 2 * i / (tips - 1)
        rr = L * (0.98 if i % 2 == 0 else 0.9) * (1 - 0.06 * u * u)
        a = ang + u * half * 0.95
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    for t, side in ((0.75, 1.05), (0.3, 0.75)):
        a = ang + side * half
        pts.append((cx + math.cos(a) * L * t, cy + math.sin(a) * L * t))
    return deform(pts, rng, 1, 0.025)


def cosmos(art, W, H, x, y, R, nx, rng, pal, tilt=1.0, tilt_a=0.0, n=8, density=0.62):
    """pal = (light, mid, deep, centre)."""
    a0 = rng.uniform(0, math.tau)
    petals = [squash(cosmos_petal(x, y, R, a0 + k * math.tau / n + rng.uniform(-.08, .08), rng), x, y, tilt, tilt_a) for k in range(n)]
    odd = shapes(W, H, petals[0::2]); even = shapes(W, H, petals[1::2])
    art = G(art, even, pal[0], pal[1], seed=nx(), density=density, edge=0.5, bloom=0.4, rough=2.5, feather=1.0, gran=0.2)
    art = G(art, odd, pal[0], pal[1], seed=nx(), density=density * 0.95, edge=0.55, bloom=0.35, rough=2.5, feather=1.0, gran=0.2)
    # deeper flush near the centre + fine veins
    inner = shapes(W, H, [squash(ellipse_pts(x, y, R * 0.42, R * 0.42, 14), x, y, tilt, tilt_a)])
    art = G(art, inner * np.clip(odd + even, 0, 1), pal[2], seed=nx(), density=0.35, edge=0.15, bloom=0, rough=3, feather=3)
    veins = []
    for k in range(n * 2):
        a = a0 + k * math.tau / (n * 2) + rng.uniform(-.1, .1)
        p = [(x + math.cos(a) * R * t, y + math.sin(a) * R * t) for t in np.linspace(0.18, 0.62, 6)]
        veins.append((squash(p, x, y, tilt, tilt_a), 1.0))
    art = G(art, strokes(W, H, veins) * np.clip(odd + even, 0, 1), pal[2], seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.3, pad=6)
    # centre: golden button with dark seeds
    cpts = squash(deform(ellipse_pts(x, y, R * 0.2, R * 0.2, 12), rng, 1, 0.05), x, y, tilt, tilt_a)
    cm = shapes(W, H, [cpts])
    art = GP(art, cm, pal[3], "#e0a21c", seed=nx(), rough=1.0, pad=8)
    art = tint(art, side_light(cm, -3, -3, 3), "#9a5b12", 0.7, seed=nx())
    dots = [(x + rng.gauss(0, R * 0.08) * tilt, y + rng.gauss(0, R * 0.08), R * 0.025 + 0.4) for _ in range(int(R * 0.6))]
    art = OV(art, circles(W, H, dots) * cm, lambda m: col_arr(m, "#6d3d10", m * 0.75), pad=6)
    return art


def chamomile(art, W, H, x, y, R, nx, rng, tilt=1.0, tilt_a=0.0, n=None, shade="#b9c2cf"):
    n = n or rng.randint(15, 19)
    a0 = rng.uniform(0, math.tau)
    pet = []
    for k in range(n):
        a = a0 + k * math.tau / n + rng.uniform(-.06, .06)
        L = R * rng.uniform(0.85, 1.05)
        p = petal_pts(x + math.cos(a) * R * 0.18, y + math.sin(a) * R * 0.18, L * 0.82, L * 0.13, a, n=10)
        pet.append(squash(deform(p, rng, 1, 0.02), x, y, tilt, tilt_a))
    m = shapes(W, H, pet)
    # white petals = pale grey-blue shadow wash on the paper + soft white body
    art = OV(art, m, lambda mm: col_arr(mm, "#fffdf8", mm * 0.92), pad=8)
    art = G(art, m, shade, "#d8dde4", seed=nx(), density=0.28, edge=0.85, bloom=0.3, rough=1.6, feather=0.8, gran=0.1, pad=8)
    cpts = squash(deform(ellipse_pts(x, y, R * 0.26, R * 0.26, 12), rng, 1, 0.04), x, y, tilt * 0.9 + 0.1, tilt_a)
    cm = shapes(W, H, [cpts])
    art = GP(art, cm, "#f2c230", "#e8a81c", seed=nx(), rough=0.8, pad=8)
    art = tint(art, side_light(cm, -3, -4, 3), "#b07510", 0.75, seed=nx())
    art = tint(art, side_light(cm, 3, 3, 3), "#fff0a0", 0.5, seed=nx())
    return art


def cornflower(art, W, H, x, y, R, nx, rng, pal=("#7f9be0", "#3f63c4", "#25307a"), tilt=1.0, tilt_a=0.0, n=None):
    """Ragged blue cornflower: trumpet florets with serrated tips around a deep centre."""
    n = n or rng.randint(9, 12)
    a0 = rng.uniform(0, math.tau)
    fl = []
    for k in range(n):
        a = a0 + k * math.tau / n + rng.uniform(-.1, .1)
        L = R * rng.uniform(0.8, 1.05)
        half = 0.26
        pts = [(x + math.cos(a) * R * 0.15, y + math.sin(a) * R * 0.15)]
        pts.append((x + math.cos(a - 0.12) * L * 0.55, y + math.sin(a - 0.12) * L * 0.55))
        for i in range(7):
            u = -1 + 2 * i / 6
            rr = L * (1.0 if i % 2 == 0 else 0.84)
            aa = a + u * half
            pts.append((x + math.cos(aa) * rr, y + math.sin(aa) * rr))
        pts.append((x + math.cos(a + 0.12) * L * 0.55, y + math.sin(a + 0.12) * L * 0.55))
        fl.append(squash(deform(pts, rng, 1, 0.02), x, y, tilt, tilt_a))
    m = shapes(W, H, fl)
    art = G(art, m, pal[0], pal[1], seed=nx(), density=0.72, edge=0.6, bloom=0.3, rough=2.0, feather=0.8, gran=0.35)
    inner = shapes(W, H, [squash(deform(ellipse_pts(x, y, R * 0.38, R * 0.38, 12), rng, 1, 0.08), x, y, tilt, tilt_a)])
    art = G(art, inner, pal[2], pal[1], seed=nx(), density=0.8, edge=0.4, bloom=0.1, rough=2.5, feather=1.2, gran=0.4)
    dots = [(x + rng.gauss(0, R * 0.12), y + rng.gauss(0, R * 0.12) * tilt, 1.1) for _ in range(9)]
    art = OV(art, circles(W, H, dots), lambda mm: col_arr(mm, "#1b1f4a", mm * 0.8), pad=6)
    return art


def bud(art, W, H, x, y, L, a, nx, rng, col=("#9db86a", "#5f7f3a"), tip=None):
    pts = deform(petal_pts(x, y, L, L * 0.26, a, n=16), rng, 1, 0.02)
    art = G(art, shapes(W, H, [pts]), col[0], col[1], seed=nx(), density=0.7, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
    if tip:
        tp = deform(petal_pts(x + math.cos(a) * L * 0.45, y + math.sin(a) * L * 0.45, L * 0.62, L * 0.15, a, n=14), rng, 1, 0.02)
        art = G(art, shapes(W, H, [tp]), tip[0], tip[1], seed=nx(), density=0.7, edge=0.5, bloom=0.2, rough=1.2, feather=0.7)
    return art


def stem_pts(x0, y0, x1, y1, bend, n=30):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    return curve([(x0, y0), (mx, my), (x1, y1)], n)


def grass_items(rng, x, y, h, n, spread=0.5, width=(3, 6), lean=0.0, base=14):
    items = []
    for _ in range(n):
        a = -math.pi / 2 + lean + rng.uniform(-spread, spread)
        L = h * rng.uniform(0.45, 1.0)
        bend = rng.uniform(-0.6, 0.6) + lean
        x0 = x + rng.uniform(-base, base)
        p = []
        for t in np.linspace(0, 1, 14):
            aa = a + bend * t * t
            p.append((x0 + math.cos(aa) * L * t + bend * L * 0.18 * t * t, y + math.sin(aa) * L * t))
        items.append((p, rng.uniform(*width), (0.0, 0.85)))
    return items


def seedhead(art, W, H, pts, nx, rng, col=("#d9c27a", "#a98a3c"), size=5.0):
    """Wild oat seed head: spikelets hang on thin pedicels from the top third of the stem, alternating sides."""
    grains, ped = [], []
    k0 = int(len(pts) * 0.62)
    for j, i in enumerate(range(k0, len(pts) - 1)):
        px, py = pts[i]
        side = -1 if j % 2 else 1
        L = size * rng.uniform(1.4, 3.2) * (1 - 0.4 * (i - k0) / max(1, len(pts) - k0))
        a = math.pi / 2 - side * rng.uniform(0.55, 1.0)
        ex, ey = px + math.cos(a - side * 1.2) * L * 0.9, py + math.sin(a - side * 1.2) * L * 0.5
        ped.append(([(px, py), (ex, ey)], 0.9, None))
        grains.append(petal_pts(ex, ey, size * rng.uniform(2.0, 2.8), size * 0.62, a + rng.uniform(-.2, .2), n=12))
    art = G(art, strokes(W, H, ped), col[1], seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.3, pad=6)
    return G(art, shapes(W, H, grains), col[0], col[1], seed=nx(), density=0.62, edge=0.65, bloom=0.2, rough=1.2, feather=0.6, gran=0.3)


def feather_leaf(rng, x, y, L, a, n=7):
    """Fine thread-like cosmos foliage strokes."""
    items = []
    main = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t + 6 * math.sin(t * 3)) for t in np.linspace(0, 1, 14)]
    items.append((main, 2.0, (0.0, 0.7)))
    for i in range(1, n):
        t = i / n
        px, py = main[int(t * 13)]
        for side in (-1, 1):
            aa = a + side * rng.uniform(0.6, 1.0)
            ll = L * 0.32 * (1 - t * 0.6)
            items.append(([(px + math.cos(aa) * ll * u, py + math.sin(aa) * ll * u) for u in np.linspace(0, 1, 6)], 1.6, (0.0, 0.8)))
    return items


# ---------------- batik: dye, wax resist, crackle ----------------
def crackle(w, h, seed, scale=30.0, thick=0.9, density=0.6):
    """Batik crackle: thin branching dye veins where cracked wax let the dye in (0..1 line field)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    for k, sc in enumerate((scale, scale * 0.55)):
        n = fbm(w, h, seed + 31 * k, sc, 3)
        n2 = fbm(w, h, seed + 7 + 31 * k, sc * 1.7, 2)
        f = np.abs(n - 0.5 + (n2 - 0.5) * 0.35)
        ln = np.clip(1 - f / (0.012 * thick * (1.6 - 0.6 * k)), 0, 1)
        out = np.maximum(out, ln * (0.9 if k == 0 else 0.55))
    keep = fbm(w, h, seed + 99, scale * 2.4, 2)
    out *= np.clip((keep - (1 - density)) * 3, 0, 1)
    return gaussian_filter(out, 0.4)


def cloth(w, h, seed, amt=1.0):
    """Woven cotton (primissima) texture multiplier ~1."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    warp = 0.5 + 0.5 * np.sin(xx * 2.2 + gaussian_filter(rng.random((h, w)).astype(np.float32), 3) * 6)
    weft = 0.5 + 0.5 * np.sin(yy * 2.2 + gaussian_filter(rng.random((h, w)).astype(np.float32), 3) * 6)
    slub = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.6, 9))
    slub = (slub - slub.mean()) / (slub.std() + 1e-6)
    return 1 + amt * ((warp * weft - 0.25) * 0.05 + slub * 0.018)


def dye_field(w, h, col, col2, seed, mottle=0.08):
    """Hand-dyed cloth colour (opaque RGB) with uneven dye uptake."""
    t = fbm(w, h, seed, 110, 3)[..., None]
    rgb = np.array(hex_rgb(col), np.float32) * (1 - t) + np.array(hex_rgb(col2), np.float32) * t
    rgb = rgb * (1 - mottle + mottle * 2 * fbm(w, h, seed + 5, 40, 3))[..., None]
    return rgb


def batik(w, h, layers, seed=1, crack=(0.55, 32), crack_col="#0d1640", cloth_amt=1.0, edge_bleed=1.2):
    """Wax-resist batik. layers = [(mask, col, col2)] painted in order (later dye baths over earlier). The first layer
    should be a full field. Edges bleed slightly; crackle veins of crack_col run through all lighter (waxed) areas."""
    rgb = np.zeros((h, w, 3), np.float32)
    alpha = np.zeros((h, w), np.float32)
    for i, (m, c1, c2) in enumerate(layers):
        mm = displace(m, seed + i * 13, edge_bleed, 14)
        mm = np.clip((gaussian_filter(mm, 0.6) - 0.3) * 2.4, 0, 1)
        d = dye_field(w, h, c1, c2, seed + i * 7)
        rgb = rgb * (1 - mm[..., None]) + d * mm[..., None]
        alpha = np.maximum(alpha, mm)
    if crack:
        dens, sc = crack
        cr = crackle(w, h, seed + 501, sc, 0.9, dens)
        lum = rgb.mean(-1)
        cr = cr * np.clip((lum - 0.35) * 2.2, 0.15, 1)
        cc = np.array(hex_rgb(crack_col), np.float32)
        rgb = rgb * (1 - cr[..., None] * 0.55) + cc * cr[..., None] * 0.55
    rgb = rgb * cloth(w, h, seed + 3, cloth_amt)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], -1)


def canting_lines(w, h, items, seed=1):
    """Wax lines drawn with a canting: steady width, small blobs where the pen paused."""
    rng = random.Random(seed)
    m = strokes(w, h, [(p, wd, None) for p, wd in items])
    blobs = []
    for p, wd in items:
        if rng.random() < 0.5:
            blobs.append((*p[0], wd * 0.9))
        if rng.random() < 0.3:
            blobs.append((*p[-1], wd * 0.85))
    if blobs:
        m = np.maximum(m, circles(w, h, blobs))
    return displace(m, seed, 0.7, 8)
