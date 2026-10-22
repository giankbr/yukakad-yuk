"""Agent F3 helpers (tegel-kunci, daun-embun, chefchaouen-biru, langgar-sawah).
Builds on _e3_lib (-> _b2_lib/_j1_lib bbox-cropped painting) and adds: botanical leaves along a bent midrib
(calathea feather pattern, variegated pothos, fern fronds), refractive dew drops painted into an existing layer,
worn cement-tile (tegel kunci) painting, blue lime-wash walls, woven bamboo (gedek), ijuk thatch.
Previews -> /tmp/pen/nb-F3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _e3_lib import *  # noqa
import _e3_lib, _b2_lib, _j1_lib, _p1_lib
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-F3/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_p1_lib, _j1_lib, _b2_lib, _e3_lib):
    _m.PREV = PREV


def prev(arr, name, tone="#f7f3ea", bg=None):
    _p1_lib.preview(arr, name, tone, bg)


# ------------------------------------------------------------------ leaves
def midrib(x, y, L, ang, bend=0.0, n=40):
    """Points along a gently bent midrib from base (x, y) to tip."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = ang + bend * (t - 0.3)
        d = L * t
        off = bend * L * 0.18 * t * t
        pts.append((x + math.cos(ang) * d - math.sin(ang) * off, y + math.sin(ang) * d + math.cos(ang) * off))
    return pts


def _normals(pts):
    out = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        out.append((-dy / l, dx / l))
    return out


def leaf_poly(x, y, L, Wd, ang, kind="oval", bend=0.0, asym=0.0, n=40):
    """Outline around a bent midrib. kind: oval (calathea), heart (pothos), lance (fern pinna / blade)."""
    rib = midrib(x, y, L, ang, bend, n)
    nr = _normals(rib)
    left, right = [], []
    ca, sa = math.cos(ang), math.sin(ang)
    for i, ((px, py), (nx_, ny_)) in enumerate(zip(rib, nr)):
        t = i / (n - 1)
        back = 0.0
        if kind == "heart":
            w = Wd * math.sin(math.pi * (0.2 + 0.8 * t)) ** 0.65 * (1.12 - 0.45 * t)
            back = Wd * 0.34 * max(0.0, 1 - t / 0.22) ** 1.6
        elif kind == "lance":
            w = Wd * math.sin(math.pi * t) ** 1.1 * (1.1 - 0.4 * t)
        else:
            w = Wd * math.sin(math.pi * t ** 0.85) ** 0.85
        left.append((px + nx_ * w * (1 + asym) - ca * back, py + ny_ * w * (1 + asym) - sa * back))
        right.append((px - nx_ * w * (1 - asym) - ca * back, py - ny_ * w * (1 - asym) - sa * back))
    if kind == "heart":
        return [rib[1]] + left[1:] + right[1:][::-1], rib, nr
    return left + right[::-1], rib, nr


LEAF_COLS = {"calathea": ("#7fb46a", "#2f7a42", "#163f27", "#d4ebb0"),
             "pothos": ("#8cc35c", "#3d8a3a", "#1d5229", "#f3efb8"),
             "plain": ("#86bf70", "#3a8547", "#1b4a2c", "#d8eeb6"),
             "blade": ("#97c97a", "#3f8a4a", "#1d4f2e", "#dcefc0")}


def paint_leaf(art, W, H, x, y, L, Wd, ang, rng, nx, kind="calathea", bend=0.0, light=(-0.5, -0.85), cols=None, shade=0.6):
    """Botanical watercolour leaf. kind: calathea (feathered dark bands), pothos (heart, cream variegation), plain."""
    shape = "heart" if kind == "pothos" else ("lance" if kind == "blade" else "oval")
    pts, rib, nr = leaf_poly(x, y, L, Wd, ang, shape, bend, rng.uniform(-0.08, 0.08))
    m = shapes(W, H, [pts])
    art = art.copy(); art[..., 3] *= 1 - np.clip(m * 1.4, 0, 0.97)
    light_c, mid, dark, pale = cols or LEAF_COLS[kind]
    lx, ly = light
    art = G(art, m, light_c, mid, seed=nx(), density=0.95, edge=0.55, bloom=0.3, rough=1.0, feather=0.8, gran=0.18)
    art = G(art, m, mid, light_c, seed=nx(), density=0.5, edge=0.4, bloom=0.4, rough=1.5, feather=1.2, gran=0.1)
    # fold: the half facing away from the light gets a deeper glaze
    nmid = nr[len(nr) // 2]
    sgn = -1 if (nmid[0] * lx + nmid[1] * ly) > 0 else 1
    side = [(px + sgn * a * Wd * 1.7, py + sgn * b * Wd * 1.7) for (px, py), (a, b) in zip(rib, nr)]
    half = shapes(W, H, [rib + side[::-1]], smooth=False) * m
    art = G(art, half, mid, dark, seed=nx(), density=0.55 * shade + 0.1, edge=0.25, bloom=0.2, rough=1.0, feather=2.0)
    n = len(rib)
    if kind == "calathea":
        polys = []
        for i in range(3, n - 3, 2):
            px, py = rib[i]; a, b = nr[i]
            t = i / (n - 1)
            wd = Wd * math.sin(math.pi * t ** 0.85) ** 0.85
            long = (i // 2) % 2 == 0
            for sg in (-1, 1):
                reach = wd * (0.86 if long else 0.5) * rng.uniform(0.88, 1.04)
                fa = math.atan2(sg * b * 1.0 + math.sin(ang) * 0.75, sg * a * 1.0 + math.cos(ang) * 0.75)
                polys.append(petal_pts(px, py, reach, reach * (0.13 if long else 0.16), fa, n=12))
        bands = shapes(W, H, polys) * m
        art = G(art, bands, dark, "#2a5a34", seed=nx(), density=0.85, edge=0.35, bloom=0.15, rough=0.8, feather=0.9, gran=0.12)
        rim = np.clip(m - gaussian_filter((m > 0.5).astype(np.float32), max(2.0, Wd * 0.07)), 0, 1)
        art = G(art, np.clip(rim * 2.2, 0, 1), dark, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.5, feather=0.8)
    elif kind == "pothos":
        items = []
        for k in range(rng.randint(5, 8)):
            i = rng.randint(3, n - 10); px, py = rib[i]; a, b = nr[i]
            sg = rng.choice((-1, 1)); reach = Wd * rng.uniform(0.3, 0.85)
            items.append(([(px + sg * a * 3, py + sg * b * 3), (px + sg * a * reach * 0.6 + math.cos(ang) * reach * 0.4, py + sg * b * reach * 0.6 + math.sin(ang) * reach * 0.4), (px + sg * a * reach + math.cos(ang) * reach * 0.7, py + sg * b * reach + math.sin(ang) * reach * 0.7)], rng.uniform(1.4, 3.6), (0.3, 0.5)))
        streak = strokes(W, H, items) * m
        art = OV(art, streak, lambda mm: pigment(mm, pale, "#fbf6d0", seed=nx(), density=0.8, edge=0.15, bloom=0, rough=0.8, feather=0.9))
    veins = []
    for i in range(3, n - 4, 3):
        px, py = rib[i]; a, b = nr[i]
        t = i / (n - 1); wd = Wd * math.sin(math.pi * t ** 0.85) ** 0.85
        for sg in (-1, 1):
            e = (px + sg * a * wd * 0.88 + math.cos(ang) * wd * 0.62, py + sg * b * wd * 0.88 + math.sin(ang) * wd * 0.62)
            veins.append(([(px, py), ((px + e[0]) / 2 + sg * a * wd * 0.08, (py + e[1]) / 2 + sg * b * wd * 0.08), e], 0.9, (0.05, 0.8)))
    vm = strokes(W, H, veins) * m
    art = OV(art, vm, lambda mm: flat(mm, pale, 0.3))
    rb = strokes(W, H, [(rib[1:-3], max(1.3, Wd * 0.06), (0.02, 0.75))]) * m
    art = OV(art, rb, lambda mm: flat(mm, pale, 0.75))
    # morning light sheen + cool shade at the far edge
    cx_, cy_ = rib[n // 3]
    art = G(art, m * light_mask(H, W, cx_ + lx * Wd * 0.7, cy_ + ly * Wd * 0.7, Wd * 1.3), "#f0f8cf", seed=nx(), density=0.32, edge=0, bloom=0.3, rough=1)
    if kind in ("calathea", "plain", "pothos"):
        pet = strokes(W, H, [(curve([(x, y), (x - math.cos(ang) * L * 0.14, y - math.sin(ang) * L * 0.14 + L * 0.02), (x - math.cos(ang) * L * 0.28, y - math.sin(ang) * L * 0.28 + L * 0.06)], 12), max(1.6, Wd * 0.07), (0.0, 0.2))])
        art = G(art, pet, mid, dark, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.5, feather=0.6)
    return art, m, rib


def fern(art, W, H, x, y, L, ang, rng, nx, bend=0.25, cols=("#7fbf62", "#2f7a3e"), pin=0.16, rib=None, step=1, dark="#1d4f2c"):
    """Fern frond: bent (or given) rachis with alternating pinnae that shrink toward the tip; painted on top
    (knocks out what is beneath)."""
    rib = rib or midrib(x, y, L, ang, bend, 60)
    nr = _normals(rib)
    n = len(rib)
    Ltot = sum(math.hypot(rib[i + 1][0] - rib[i][0], rib[i + 1][1] - rib[i][1]) for i in range(n - 1))
    polys = []
    for i in range(2, n - 1, step):
        t = i / (n - 1)
        ln = Ltot * pin * (1 - t) ** 0.5 * (0.7 + 0.3 * math.sin(math.pi * min(1, t * 2.4))) * rng.uniform(0.9, 1.08)
        if ln < 2.5:
            continue
        px, py = rib[i]; a, b = nr[i]
        tx, ty = rib[min(n - 1, i + 1)][0] - rib[i - 1][0], rib[min(n - 1, i + 1)][1] - rib[i - 1][1]
        tl = math.hypot(tx, ty) or 1; tx, ty = tx / tl, ty / tl
        for sg in (-1, 1):
            if (i + (sg > 0)) % 2 and step == 1:
                continue
            fa = math.atan2(sg * b + ty * 0.65, sg * a + tx * 0.65)
            polys.append(petal_pts(px, py, ln, ln * 0.25, fa, n=12, cup=sg * 0.25))
    m = shapes(W, H, polys)
    art = art.copy(); art[..., 3] *= 1 - np.clip(m * 1.4, 0, 0.95)
    art = G(art, m, cols[0], cols[1], seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=0.9, feather=0.7, gran=0.2)
    art = G(art, m * np.clip(fbm(W, H, nx(), 60, 2) * 1.6 - 0.5, 0, 1), cols[1], dark, seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=1, feather=1.2)
    rm = strokes(W, H, [(rib[:-1], max(1.2, Ltot * 0.007), (0.02, 0.85))])
    art = G(art, rm, cols[1], dark, seed=nx(), density=0.95, edge=0.2, bloom=0, rough=0.5, feather=0.5)
    return art, m


# ------------------------------------------------------------------ dew drops
def dew(art, x, y, r, rng, elong=1.0, rot=0.0, shadow=0.45, light=(-0.6, -0.75)):
    """Paint a clear water drop sitting on the painted surface (in place): cast shadow, inverted magnified
    refraction of what is under it, dark rim on the light side, bright caustic opposite, specular highlight."""
    H, W = art.shape[:2]
    R = int(r * 2.2) + 4
    x0, y0 = int(max(0, x - R)), int(max(0, y - R))
    x1, y1 = int(min(W, x + R)), int(min(H, y + R))
    if x1 - x0 < 4 or y1 - y0 < 4:
        return art
    sub = art[y0:y1, x0:x1].copy()
    h, w = sub.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = x - x0, y - y0
    ca, sa = math.cos(rot), math.sin(rot)
    u = ((xx - cx) * ca + (yy - cy) * sa) / r
    v = (-(xx - cx) * sa + (yy - cy) * ca) / (r * elong)
    # slight wobble so it is not a perfect ellipse
    wob = 1 + 0.04 * np.sin(np.arctan2(v, u) * 3 + rng.uniform(0, 6))
    d = np.sqrt(u * u + v * v) / wob
    drop = np.clip((1 - d) * r * 0.9, 0, 1)
    lx, ly = light
    # cast shadow (opposite the light), only on painted pixels
    sd = np.sqrt(((xx - cx + lx * r * 0.42) / r) ** 2 + ((yy - cy + ly * r * 0.42) / (r * elong)) ** 2)
    sh = gaussian_filter(np.clip((1.05 - sd) * 3, 0, 1), max(1, r * 0.12)) * (1 - drop) * shadow * (sub[..., 3] > 0.1)
    sub[..., :3] *= (1 - sh[..., None] * np.array([0.65, 0.5, 0.6], np.float32))
    # refraction: inverted, magnified sample of the surface under the drop
    sx = cx - (xx - cx) * 0.55
    sy = cy - (yy - cy) * 0.55
    ref = np.stack([map_coordinates(sub[..., k], [sy, sx], order=1, mode="nearest") for k in range(4)], -1)
    base = ref[..., :3]
    lum = base.mean(-1, keepdims=True)
    base = np.clip(lum + (base - lum) * 1.35, 0, 1)  # more saturated through water
    # inner shading: darker on the light side (top-left), luminous caustic on the far side
    side = (u * lx + v * ly)  # >0 towards light
    dark = np.clip(side * 0.9 + 0.1, 0, 1) * np.clip(d * 1.2, 0, 1)
    caust = np.clip(-side - 0.15, 0, 1) * np.clip(1 - np.abs(d - 0.62) * 3.2, 0, 1)
    inner = base * (1 - dark[..., None] * 0.68) + caust[..., None] * 0.8 * np.array([1.0, 1.0, 0.92], np.float32)
    inner = np.clip(inner * (1.05 + 0.1 * (1 - d))[..., None], 0, 1)
    # thin rim
    rim = np.clip(1 - np.abs(d - 0.93) * 14, 0, 1) * (0.35 + 0.65 * np.clip(side + 0.4, 0, 1))
    inner = inner * (1 - rim[..., None] * 0.6)
    # specular highlights
    hx, hy = lx * 0.42, ly * 0.42
    hs = np.sqrt(((u - hx) / 0.26) ** 2 + ((v - hy) / 0.16) ** 2)
    spec = np.clip(1 - hs, 0, 1) ** 0.6
    hs2 = np.sqrt(((u + lx * 0.5) / 0.1) ** 2 + ((v + ly * 0.52) / 0.07) ** 2)
    spec = np.maximum(spec, np.clip(1 - hs2, 0, 1) ** 0.8 * 0.6)
    inner = inner * (1 - spec[..., None]) + spec[..., None] * np.array([1, 1, 0.97], np.float32)
    a = drop
    sub[..., :3] = sub[..., :3] * (1 - a[..., None]) + inner * a[..., None]
    sub[..., 3] = np.maximum(sub[..., 3], a * 0.96)
    out = art.copy()
    out[y0:y1, x0:x1] = sub
    return out


def drop_on(art, mask, n, rmin, rmax, rng, keep=0.85, tries=400, avoid=None):
    """Scatter n dew drops whose disc sits well inside mask."""
    H, W = mask.shape
    placed = []
    ys, xs = np.where(mask > 0.9)
    if len(xs) == 0:
        return art, placed
    for _ in range(tries):
        if len(placed) >= n:
            break
        k = rng.randrange(len(xs))
        x, y = float(xs[k]), float(ys[k])
        r = rng.uniform(rmin, rmax) if rng.random() > 0.3 else rng.uniform(rmin, (rmin + rmax) / 2)
        ok = True
        for (px, py, pr) in placed:
            if math.hypot(px - x, py - y) < pr + r + 4:
                ok = False; break
        if not ok:
            continue
        # check coverage
        y0, y1, x0, x1 = int(max(0, y - r)), int(min(H, y + r)), int(max(0, x - r)), int(min(W, x + r))
        if mask[y0:y1, x0:x1].mean() < keep:
            continue
        if avoid is not None and avoid[int(y), int(x)] > 0.3:
            continue
        placed.append((x, y, r))
        art = dew(art, x, y, r, rng, elong=rng.uniform(0.92, 1.08), rot=rng.uniform(0, 3))
    return art, placed


# ------------------------------------------------------------------ surfaces
def wrapfbm(w, h, seed, sigma):
    return wrap_noise(w, h, seed, sigma)


def limewash(w, h, base="#5a8fd0", deep="#2f63ad", pale="#bcd6f2", seed=1, wrap=True):
    """Blue lime-wash wall: several translucent coats brushed in different directions, older lighter coat showing
    where the top coat thinned, chalky speckle, faint brush arcs. Opaque RGBA. wrap=True makes it tile."""
    N = (lambda s, sg: wrap_noise(w, h, s, sg)) if wrap else (lambda s, sg: (lambda a: (a - a.min()) / (a.max() - a.min() + 1e-6))(gaussian_filter(np.random.default_rng(s).random((h, w)).astype(np.float32), sg)))
    ca, cb, cp = col_arr(base), col_arr(deep), col_arr(pale)
    t1 = N(seed, 26)
    rgb = ca * (1 - t1[..., None] * 0.6) + cb * (t1[..., None] * 0.6)
    worn = np.clip((N(seed + 1, 14) - 0.58) * 3.2, 0, 1) * np.clip((N(seed + 2, 40) - 0.35) * 2.5, 0, 1)
    rgb = rgb * (1 - worn[..., None] * 0.5) + cp * worn[..., None] * 0.5
    # brush arcs: directional noise
    g = np.random.default_rng(seed + 3).random((h, w)).astype(np.float32)
    st = gaussian_filter(g, (1.0, 9.0), mode="wrap") - gaussian_filter(g, (6.0, 6.0), mode="wrap")
    st2 = gaussian_filter(g, (9.0, 1.2), mode="wrap") - gaussian_filter(g, (6.0, 6.0), mode="wrap")
    k = N(seed + 4, 30)[..., None]
    rgb = rgb * (1 + (st[..., None] * k + st2[..., None] * (1 - k)) * 1.6)
    chalk = gaussian_filter(np.random.default_rng(seed + 5).random((h, w)).astype(np.float32), 0.6, mode="wrap")
    chalk = (chalk - chalk.mean()) / (chalk.std() + 1e-6)
    rgb = rgb * (1 + chalk[..., None] * 0.035)
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)


def cement_paint(mask, col, seed=1, fade=0.3, wear=0.3):
    """Pigmented cement layer of a tegel: matte, even, soft-crisp pressed edge, faded + worn by decades of feet."""
    h, w = mask.shape
    m = displace(mask, seed, 0.7, 10)
    m = np.clip((gaussian_filter(m, 0.6) - 0.3) * 2.4, 0, 1)
    rgb = np.ones((h, w, 3), np.float32) * col_arr(col)
    tone = fbm(w, h, seed + 2, 50, 3)
    rgb = rgb * (0.94 + 0.1 * tone[..., None])
    # fade towards a chalky grey-cream
    f = fade * (0.5 + 0.5 * fbm(w, h, seed + 4, 80, 2))
    rgb = rgb * (1 - f[..., None]) + col_arr("#e7dfcf") * f[..., None]
    pits = (np.random.default_rng(seed).random((h, w)) > 0.997).astype(np.float32)
    pits = gaussian_filter(pits, 0.7) * 3
    a = m * (1 - np.clip(pits, 0, 0.6)) * (1 - wear * np.clip((fbm(w, h, seed + 6, 12, 3) - 0.6) * 3, 0, 1))
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1)


def gedek(w, h, seed=1, cell=18, light="#d9b779", dark="#a77f45"):
    """Woven split-bamboo wall (anyaman bambu, twill 2/2 diagonal): strips with sheen + node marks. Tiles if
    w, h are multiples of 2*cell."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    i = np.floor(xx / cell); j = np.floor(yy / cell)
    # twill: which strip is on top depends on (i + j) mod 4
    top = (((i + j) % 4) < 2).astype(np.float32)
    fx = (xx % cell) / cell; fy = (yy % cell) / cell
    hor = 0.72 + 0.32 * np.sin(fy * math.pi) ** 0.5 - 0.18 * (1 - np.sin(fx * math.pi)) ** 6
    ver = 0.72 + 0.32 * np.sin(fx * math.pi) ** 0.5 - 0.18 * (1 - np.sin(fy * math.pi)) ** 6
    shade = top * hor + (1 - top) * ver
    # fibre streaks along each strip direction
    g = np.random.default_rng(seed).random((h, w)).astype(np.float32)
    fh = gaussian_filter(g, (0.4, 6), mode="wrap"); fv = gaussian_filter(g, (6, 0.4), mode="wrap")
    fh = (fh - fh.mean()) / (fh.std() + 1e-6); fv = (fv - fv.mean()) / (fv.std() + 1e-6)
    fib = top * fh + (1 - top) * fv
    # per-strip tone variation (outer skin vs inner)
    sid = np.where(top > 0.5, j * 7.13, i * 3.71 + 50)
    stone = (np.sin(sid * 12.9898) * 43758.5453) % 1.0
    ca, cb = col_arr(light), col_arr(dark)
    rgb = ca * (1 - stone[..., None] * 0.55) + cb * (stone[..., None] * 0.55)
    rgb = rgb * (shade[..., None] * (1 + fib[..., None] * 0.045))
    gap = np.clip(1 - np.minimum(np.minimum(fx, 1 - fx), np.minimum(fy, 1 - fy)) * cell / 1.2, 0, 1)
    rgb = rgb * (1 - gap[..., None] * 0.35)
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)


def lone_drop(r, tint="#cfe6c8", seed=1):
    """A free-standing water drop (for animated sparkles / falling drops): painted over a pale tint, then cut out."""
    S = int(r * 2.6)
    rng = random.Random(seed)
    base = solid(S, S, tint)
    base[..., :3] *= (0.9 + 0.12 * fbm(S, S, seed, 8, 2))[..., None]
    out = dew(base, S / 2, S / 2, r, rng, shadow=0.0)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.sqrt((xx - S / 2) ** 2 + (yy - S / 2) ** 2) / r
    a = np.clip((1 - d) * r * 0.9, 0, 1)
    rim = np.clip(1 - np.abs(d - 0.9) * 8, 0, 1)
    out[..., 3] = np.clip(a * (0.55 + 0.45 * rim + 0.4 * (out[..., :3].mean(-1) > 0.9)), 0, 1)
    return out


def palm_parts(W, H, x, by, h, lean, seed):
    """Coconut palm split into (trunk, crown) masks so they can be painted in their own colours."""
    rr = random.Random(seed)
    top = (x + lean * h, by - h)
    tpts = curve([(x, by), (x + lean * h * 0.2, by - h * 0.5), top], 40)
    trunk = strokes(W, H, [(tpts, max(5, h * 0.04), (0.0, 0.15))])
    items = []
    for k in range(12):
        a = -math.pi * 0.97 + k * math.pi * 0.94 / 11 + rr.gauss(0, 0.07)
        L = h * rr.uniform(0.38, 0.52)
        lift = math.sin(-a) * L * 0.28
        end = (top[0] + math.cos(a) * L, top[1] + L * 0.38 + rr.uniform(0, L * 0.25))
        mid = (top[0] + math.cos(a) * L * 0.5, top[1] - lift - 4)
        fr = curve([top, mid, end], 26)
        items.append((fr, max(2.0, h * 0.007), (0.0, 0.5)))
        for j in range(2, len(fr) - 1):
            (x0, y0), (x1, y1) = fr[j - 1], fr[j]
            ang = math.atan2(y1 - y0, x1 - x0)
            ll = (h * 0.12) * (1 - 0.55 * j / len(fr))
            for sg in (-1, 1):
                b2 = ang + sg * 0.8
                items.append(([(x1, y1), (x1 + math.cos(b2) * ll * 0.5, y1 + math.sin(b2) * ll * 0.5 + ll * 0.25), (x1 + math.cos(b2) * ll * 0.8, y1 + math.sin(b2) * ll * 0.8 + ll * 0.7)], max(1.4, h * 0.005), (0.0, 0.8)))
    crown = strokes(W, H, items)
    nuts = circles(W, H, [(top[0] + rr.uniform(-h * 0.03, h * 0.03), top[1] + h * 0.03 + rr.uniform(0, h * 0.02), h * 0.018) for _ in range(5)])
    return trunk, crown, nuts, tpts


def paint_palm(art, W, H, x, by, h, rng, nx, lean=0.1, far=0.0, light=(-0.5, -0.8)):
    trunk, crown, nuts, tpts = palm_parts(W, H, x, by, h, lean, nx())
    tc = mix("#8a7a66", "#a8aeb0", far), mix("#4e4236", "#8a9094", far)
    art = G(art, trunk, tc[0], tc[1], seed=nx(), density=0.95, edge=0.4, bloom=0.1, rough=0.6, feather=0.5)
    if far < 0.5:
        rings = trunk * hatch(W, H, 0.05, max(3, h * 0.012), 0.18, nx(), 0.8)
        art = G(art, rings, tc[1], seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
        art = G(art, trunk * light_mask(H, W, x - h * 0.2, by - h * 0.5, h * 0.6), "#e8c890", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.5)
    cc = mix("#5e7f34", "#8fa08a", far), mix("#2e4a1e", "#7a8a78", far)
    art = G(art, crown, cc[0], cc[1], seed=nx(), density=0.92, edge=0.45, bloom=0.2, rough=0.8, feather=0.6, gran=0.15)
    top = tpts[-1]
    art = G(art, crown * light_mask(H, W, top[0] + light[0] * h * 0.3, top[1] + light[1] * h * 0.2, h * 0.45), "#e0c060", seed=nx(), density=0.4 * (1 - far), edge=0, bloom=0.2, rough=1)
    if far < 0.5:
        art = GP(art, nuts, "#7a6a2a", "#4e4418", seed=nx(), rough=0.4)
    return art
