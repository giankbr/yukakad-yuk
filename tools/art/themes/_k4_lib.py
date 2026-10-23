"""Agent J4 helpers (renda-putih, kaca-cermin, malakit-hijau, konser-amal): _j1_lib (local painting G/GP/LC/FO/OV,
strokes/shapes/circles/hatch) + lace, mirror-mosaic and malachite generators. Previews -> /tmp/pen/nb-J4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art

PREV = "/tmp/pen/nb-J4/art"
os.makedirs(PREV, exist_ok=True)


def show(arr, name, tone="#f4eee3", bg=None):
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def smooth01(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def ramp(t, stops):
    """Map t (HxW, 0..1) through colour stops [(pos, hex)] -> HxWx3."""
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float32)
    ps = [p for p, _ in stops]
    cs = [np.array(hex_rgb(c), np.float32) for _, c in stops]
    for i in range(len(stops) - 1):
        k = np.clip((t - ps[i]) / max(1e-6, ps[i + 1] - ps[i]), 0, 1)[..., None]
        sel = ((t >= ps[i]) & (t <= ps[i + 1]))[..., None]
        out = np.where(sel, cs[i] * (1 - k) + cs[i + 1] * k, out)
    return out


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, alpha=1.0):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return rgba(rgb, mask * alpha)


def emboss_light(mask, blur=1.6, k=3.0, lx=-1.0, ly=-1.0):
    """Relief shading from a height mask: >0 lit, <0 shaded (light from the upper left by default)."""
    gy, gx = np.gradient(gaussian_filter(mask, blur))
    return (gx * lx + gy * ly) * k


def drop_shadow(mask, col="#000000", blur=4.0, dx=2, dy=3, strength=0.4):
    m = gaussian_filter(np.roll(np.roll(mask, dy, 0), dx, 1), blur) * strength
    return flat(np.clip(m, 0, 1), col)


# ------------------------------------------------------------------ lace
def tulle(W, H, spacing=7.0, width=0.16, seed=1, rot=0.3):
    """Hexagonal bobbinet: three families of fine threads at 60 degrees -> 0..1 thread mask."""
    out = np.zeros((H, W), np.float32)
    for k in range(3):
        out = np.maximum(out, hatch(W, H, rot + k * math.pi / 3, spacing, width, seed + k, wob=0.6))
    return out


def lace_render(W, H, cloth, cord, net, picot=None, seed=1, thread="#fffdf7", shade="#c9bcaa", shadow_col="#5a4a3c",
                shadow=0.28, cloth_spacing=2.6, net_alpha=0.55):
    """Thread-level lace. cloth: dense cloth-stitch areas (motifs), cord: raised cordonnet outlines,
    net: tulle ground region (mask, the mesh is generated here), picot: little loops on the edge.
    Returns RGBA with the soft cast shadow on the satin baked in."""
    rng = np.random.default_rng(seed)
    mesh = tulle(W, H, 7.2, 0.15, seed) * net * net_alpha
    # cloth stitch: fine parallel threads + crossing weft, slightly irregular
    weave = np.maximum(hatch(W, H, 1.05, cloth_spacing, 0.62, seed + 9, wob=0.8), hatch(W, H, 2.62, cloth_spacing * 1.3, 0.4, seed + 11, wob=0.8) * 0.7)
    cl = gaussian_filter(cloth, 0.5)
    clothA = cl * (0.55 + 0.4 * weave)
    # pin holes ("fillings") inside cloth areas
    holes = fbm(W, H, seed + 3, 5, 2)
    clothA *= 1 - np.clip((holes - 0.8) * 6, 0, 1) * 0.6 * (gaussian_filter(cloth, 3) > 0.9)
    co = gaussian_filter(cord, 0.6)
    pi = gaussian_filter(picot, 0.5) if picot is not None else 0
    a = np.clip(np.maximum.reduce([mesh, clothA, co, pi * np.ones_like(co)]), 0, 1)
    # height for relief: cord is highest, cloth middle, mesh low
    height = co * 1.0 + cl * 0.45 + mesh * 0.2 + (pi * 0.7 if picot is not None else 0)
    light = emboss_light(height, 1.2, 5.0)
    tone = np.clip(0.55 + light * 0.9 + (weave - 0.5) * 0.12 * cl, 0, 1)
    tone = tone * (0.86 + 0.14 * (co > 0.3)) + 0.0
    rgb = ramp(tone, [(0, shade), (0.6, thread), (1, "#ffffff")])
    # slight yarn grain
    g = gaussian_filter(rng.random((H, W)).astype(np.float32), 0.6)
    rgb = rgb * (1 + (g[..., None] - 0.5) * 0.06)
    lace = rgba(rgb, a)
    # cast shadow onto the satin (offset to the lower right), only where lace isn't
    sh = gaussian_filter(np.roll(np.roll(np.clip(a * 1.4, 0, 1), 3, 0), 2, 1), 2.2) * shadow
    sh2 = gaussian_filter(np.roll(np.roll(np.clip(a, 0, 1), 6, 0), 4, 1), 7) * shadow * 0.6
    out = over(flat(np.clip(sh + sh2, 0, 1), shadow_col), lace)
    return out


def flower_lace(W, H, cx, cy, r, petals, rng, rot=0.0, cloth=None, cord=None, hollow=0.42):
    """A lace flower: petals as cloth-stitch, cordonnet around each petal and the eye, open (net) centre."""
    cl = []
    co = []
    for i in range(petals):
        a = rot + i * math.tau / petals + rng.uniform(-0.05, 0.05)
        L = r * rng.uniform(0.92, 1.05)
        pts = petal_pts(cx + math.cos(a) * r * 0.18, cy + math.sin(a) * r * 0.18, L, L * 0.62 * 7 / petals, a, n=16, cup=0.15)
        cl.append(pts)
    m = shapes(W, H, cl)
    eye = circles(W, H, [(cx, cy, r * hollow * 0.55)])
    m = np.clip(m - eye, 0, 1)
    edge = np.clip(m - gaussian_filter(m, 1.4) * 0 - np.clip(gaussian_filter(m, 2.2) * 1.0, 0, 1) * 0 , 0, 1)
    rim = np.clip((gaussian_filter(m, 1.2) > 0.08).astype(np.float32) - (gaussian_filter(m, 1.2) > 0.85).astype(np.float32), 0, 1)
    eye_r = ring_mask(W, H, cx, cy, r * hollow * 0.55, 3.2)
    dots = circles(W, H, [(cx + math.cos(t) * r * 0.16, cy + math.sin(t) * r * 0.16, 1.8) for t in np.linspace(0, math.tau, 7)[:-1]])
    if cloth is not None:
        np.maximum(cloth, m, out=cloth)
    if cord is not None:
        np.maximum(cord, np.maximum.reduce([rim, eye_r, dots]), out=cord)
    return m


def leaf_lace(W, H, x, y, L, ang, rng, cloth=None, cord=None):
    pts = petal_pts(x, y, L, L * 0.38, ang, n=14, cup=0.1)
    m = shapes(W, H, [pts])
    rim = np.clip((gaussian_filter(m, 1.2) > 0.08).astype(np.float32) - (gaussian_filter(m, 1.2) > 0.85).astype(np.float32), 0, 1)
    vein = strokes(W, H, [([(x, y), (x + math.cos(ang) * L * 0.85, y + math.sin(ang) * L * 0.85)], 2.2, (0.05, 0.4))])
    # leaf halves: one half left open (net) for the classic Chantilly look
    if cloth is not None:
        np.maximum(cloth, m, out=cloth)
    if cord is not None:
        np.maximum(cord, np.maximum(rim, vein), out=cord)
    return m


def cord_curve(W, H, pts, width=3.0):
    return strokes(W, H, [(curve(pts, 60), width, (0.02, 0.05))])


def scallop_edge(W, H, y0, period, depth, x0=0, x1=None, picot_r=2.2, down=True):
    """Scalloped lace edge region (above the edge = 1) + cord on the edge + picot loops. Returns (region, cord, picot)."""
    x1 = W if x1 is None else x1
    pts = [(x0, -10)]
    xs = np.arange(x0, x1 + 1, 2)
    ys = []
    for x in xs:
        t = ((x - x0) % period) / period
        y = y0 + depth * math.sin(math.pi * t) ** 0.8 * (1 if down else -1)
        ys.append(y)
    pts += list(zip(xs, ys)) + [(x1, -10)]
    region = shapes(W, H, [pts], smooth=False)
    cordm = strokes(W, H, [(list(zip(xs, ys)), 4.0, None)])
    pic = []
    for x, y in zip(xs[::5], ys[::5]):
        pic.append((x, y + picot_r * 1.6 * (1 if down else -1), picot_r))
    picot = np.clip(circles(W, H, pic) - circles(W, H, [(a, b, r * 0.45) for a, b, r in pic]), 0, 1)
    return region, cordm, picot


# ------------------------------------------------------------------ malachite
def malachite(W, H, seed, centers, period=7.0, warp=26.0, stops=None, light_dir=0.7):
    """Polished malachite: concentric bands around botryoidal centres (cx, cy, weight), warped, variable widths.
    Returns opaque RGBA."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wx = (fbm(W, H, seed, 160, 4) - 0.5) * warp * 2
    wy = (fbm(W, H, seed + 1, 160, 4) - 0.5) * warp * 2
    wx += (fbm(W, H, seed + 2, 40, 3) - 0.5) * warp * 0.5
    wy += (fbm(W, H, seed + 3, 40, 3) - 0.5) * warp * 0.5
    X, Y = xx + wx, yy + wy
    k = 18.0
    acc = np.zeros((H, W), np.float64)
    for cx, cy, wgt in centers:
        d = np.hypot(X - cx, Y - cy) / wgt
        acc += np.exp(-d / k)
    d = (-k * np.log(acc + 1e-30)).astype(np.float32)
    phase = d / period
    widths = rng.uniform(0.25, 2.4, 6000) ** 1.3
    cum = np.concatenate([[0], np.cumsum(widths)]) / widths.mean()
    idx = np.clip(np.searchsorted(cum, phase.ravel()).reshape(phase.shape) - 1, 0, len(widths) - 1)
    frac = (phase - cum[idx]) / (cum[idx + 1] - cum[idx] + 1e-6)
    tones = rng.random(6000) ** 0.9
    # bands alternate dark/light with randomness
    tones = np.where(np.arange(6000) % 2 == 0, tones * 0.55, 0.45 + tones * 0.55)
    t = tones[idx]
    # inside each band: darker toward the outer boundary, crisp light edge
    t = t * (0.82 + 0.28 * smooth01(1 - frac)) - 0.12 * (frac > 0.9)
    # fibrous striation across bands
    fib = fbm(W, H, seed + 7, 3, 2)
    t = t + (fib - 0.5) * 0.08 + (fbm(W, H, seed + 8, 90, 3) - 0.5) * 0.18
    stops = stops or [(0, "#03190f"), (0.22, "#08341f"), (0.45, "#11603a"), (0.66, "#1f8a55"), (0.84, "#4cb47d"), (1, "#a6dfbd")]
    rgb = ramp(np.clip(t, 0, 1), stops)
    # polish: broad soft reflection + fine clear-coat sheen
    sheen = smooth01(1 - np.abs((xx / W) * light_dir + (yy / H) * (1 - light_dir) - 0.42) / 0.5)
    rgb = rgb * (0.92 + 0.12 * sheen[..., None]) + 0.05 * (sheen[..., None] ** 4)
    return rgba(rgb, np.ones((H, W), np.float32))


# ------------------------------------------------------------------ mirror mosaic (aineh-kari)
def mirror_facets(W, H, polys, seed=1, env=None, grout="#0e3b40", grout_w=2.0, base=None, colors=None, spec_p=0.42):
    """Each polygon is a small cut mirror piece: it reflects a random patch of the 'environment' (teal room, silver
    light, rose-gold lamps), with bevelled edges, a hard specular streak and dark grout between pieces.
    Returns RGBA (alpha = union of pieces + grout)."""
    rng = random.Random(seed)
    env = env or ["#d9e6e6", "#a9c3c4", "#6f9799", "#2f5f63", "#e9c3ad", "#c98f78", "#f4efe8", "#3d7b7f", "#8fb0b0"]
    sc = skia.Surface(W, H); cv = sc.getCanvas(); cv.clear(skia.ColorTRANSPARENT)
    sp = skia.Surface(W, H); spc = sp.getCanvas(); spc.clear(skia.ColorTRANSPARENT)
    for n_, pts in enumerate(polys):
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        if colors is not None:
            c1, c2 = colors[n_]
        else:
            c1 = rng.choice(env); c2 = rng.choice(env)
        ang = rng.uniform(0, math.tau)
        rr = max(4, max(math.hypot(p[0] - cx, p[1] - cy) for p in pts))
        shader = skia.GradientShader.MakeLinear(
            [skia.Point(cx - math.cos(ang) * rr, cy - math.sin(ang) * rr), skia.Point(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr)],
            [color(c1), color(c2)])
        p = skia.Paint(AntiAlias=True, Shader=shader)
        path = poly_path(pts)
        cv.drawPath(path, p)
        if rng.random() < spec_p:  # specular streak on some pieces
            spc.save(); spc.clipPath(path, skia.ClipOp.kIntersect, True)
            a2 = ang + rng.uniform(-0.5, 0.5)
            w = rr * rng.uniform(0.18, 0.45)
            spc.translate(cx + rng.uniform(-rr, rr) * 0.4, cy + rng.uniform(-rr, rr) * 0.4); spc.rotate(math.degrees(a2))
            spc.drawRect(skia.Rect(-rr * 2, -w / 2, rr * 2, w / 2), skia.Paint(AntiAlias=True, Color=color("#ffffff", rng.uniform(0.35, 0.85))))
            spc.restore()
    arr = np.asarray(sc.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType), np.float32) / 255
    spec = np.asarray(sp.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType), np.float32)[..., 3] / 255
    a = arr[..., 3]
    # pieces separated by grout: shrink each piece's alpha via an edge test
    core = np.clip((gaussian_filter(a, grout_w * 0.5) - 0.55) * 4, 0, 1)
    # bevel: bright on the upper-left edge, dark lower-right
    light = emboss_light(core, 0.9, 6.0)
    rgb = arr[..., :3] * (1 + np.clip(light, -0.35, 0.5)[..., None]) + spec[..., None] * 0.55 * core[..., None]
    # faint silvering wear
    wear = fbm(W, H, seed + 5, 8, 2)
    rgb = rgb * (1 - 0.08 * np.clip((wear - 0.7) * 4, 0, 1))[..., None]
    gr = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(grout), np.float32)
    gr = gr * (0.85 + 0.3 * fbm(W, H, seed + 6, 4, 2))[..., None]
    out_rgb = rgb * core[..., None] + gr * (1 - core[..., None])
    region = np.clip(gaussian_filter(a, 0.6) * 1.3, 0, 1)
    if base is not None:
        region = np.maximum(region, base)
    return rgba(out_rgb, region)


def star_poly(cx, cy, R, r, n=8, rot=0.0):
    pts = []
    for i in range(n * 2):
        a = rot + i * math.pi / n
        rad = R if i % 2 == 0 else r
        pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
    return pts


def poly_reg(cx, cy, R, n, rot=0.0):
    return [(cx + math.cos(rot + i * math.tau / n) * R, cy + math.sin(rot + i * math.tau / n) * R) for i in range(n)]


def split_poly(pts, depth, rng):
    """Recursively cut a polygon into facets (triangles fan + random splits) like hand-cut mirror pieces."""
    if depth <= 0 or len(pts) < 3:
        return [pts]
    cx = sum(p[0] for p in pts) / len(pts) + rng.uniform(-1, 1)
    cy = sum(p[1] for p in pts) / len(pts) + rng.uniform(-1, 1)
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        tri = [(cx, cy), a, b]
        if depth > 1:
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            out += [[(cx, cy), a, m], [(cx, cy), m, b]]
        else:
            out.append(tri)
    return out


def glint(W, H, cx, cy, R, rot=0.0):
    """Four-point light glint mask (thin rays + soft core)."""
    rays = []
    for k in range(4):
        a = rot + k * math.pi / 2
        L = R if k % 2 == 0 else R * 0.62
        rays.append(([(cx, cy), (cx + math.cos(a) * L, cy + math.sin(a) * L)], R * 0.09, (0.0, 0.95)))
    m = strokes(W, H, rays)
    core = gaussian_filter(circles(W, H, [(cx, cy, R * 0.12)]), R * 0.06)
    halo = gaussian_filter(circles(W, H, [(cx, cy, R * 0.25)]), R * 0.18) * 0.6
    return np.clip(np.maximum.reduce([gaussian_filter(m, 0.8), core * 1.5, halo]), 0, 1)


def ray_radius(poly, cx, cy, th):
    """Distance from (cx, cy) along angle th to the polygon boundary."""
    dx, dy = math.cos(th), math.sin(th)
    best = 0.0
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i][0] - cx, poly[i][1] - cy
        bx, by = poly[(i + 1) % n][0] - cx, poly[(i + 1) % n][1] - cy
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = (ax * ey - ay * ex) / den
        u = (ax * dy - ay * dx) / den
        if t > 0 and -1e-6 <= u <= 1 + 1e-6:
            best = max(best, t)
    return best


def morph_rings(cx, cy, inner, outer, M, K, rot=0.0, ease=1.0):
    """Facet grid between two closed polygons (rays at M angles, K rings): returns list of (tri, i, k, half)."""
    out = []
    ths = [rot + i * math.tau / M for i in range(M)]
    ri = [ray_radius(inner, cx, cy, t) for t in ths]
    ro = [ray_radius(outer, cx, cy, t) for t in ths]
    def P(i, k):
        i %= M
        t = (k / K) ** ease
        r = ri[i] + (ro[i] - ri[i]) * t
        return (cx + math.cos(ths[i]) * r, cy + math.sin(ths[i]) * r)
    for k in range(K):
        for i in range(M):
            a, b, c, d = P(i, k), P(i + 1, k), P(i + 1, k + 1), P(i, k + 1)
            if (i + k) % 2:
                out += [([a, b, c], i, k, 0), ([a, c, d], i, k, 1)]
            else:
                out += [([a, b, d], i, k, 0), ([b, c, d], i, k, 1)]
    return out


def outline_paths(W, H, polys, width=3.0, smooth=True):
    """Stroked outlines of many closed polygons in one mask (cordonnet)."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                   StrokeJoin=skia.Paint.kRound_Join)
    for pts in polys:
        cv.c.drawPath(smooth_path(pts) if smooth else poly_path(pts), p)
    return cv.array()[..., 3]


def shrink(pts, k):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]


class LaceSheet:
    """Accumulates lace geometry (as polygon lists, rasterised once) for fast thread-level rendering."""
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.cloth, self.half, self.cords, self.lines = [], [], [], []   # polys, polys, (polys, w), (pts, w)
        self.dots = []

    def flower(self, cx, cy, r, petals, rng, rot=0.0, open_every=0):
        for i in range(petals):
            a = rot + i * math.tau / petals + rng.uniform(-0.06, 0.06)
            L = r * rng.uniform(0.9, 1.06)
            pts = petal_pts(cx + math.cos(a) * r * 0.22, cy + math.sin(a) * r * 0.22, L * 0.86, L * 0.58 * 6.5 / petals, a, n=16, cup=0.2)
            if open_every and i % open_every == 0:
                self.half.append(pts)
            else:
                self.cloth.append(pts)
            self.cords.append((pts, max(2.0, r * 0.075)))
            # inner vein toward the tip
            self.lines.append(([(cx + math.cos(a) * r * 0.4, cy + math.sin(a) * r * 0.4), (cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78)], max(1.2, r * 0.04)))
        if r > 24:  # a second, inner ring of petals
            for i in range(petals):
                a = rot + (i + 0.5) * math.tau / petals
                pts = petal_pts(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12, r * 0.42, r * 0.3, a, n=12, cup=0.2)
                self.half.append(pts)
                self.cords.append((pts, max(1.6, r * 0.05)))
        eye = ellipse_pts(cx, cy, r * 0.2, r * 0.2, 14)
        self.cords.append((eye, max(2.0, r * 0.08)))
        for t in np.linspace(0, math.tau, 6)[:-1]:
            self.dots.append((cx + math.cos(t + rot) * r * 0.11, cy + math.sin(t + rot) * r * 0.11, max(1.2, r * 0.045)))

    def leaf(self, x, y, L, ang, rng):
        pts = petal_pts(x, y, L, L * 0.36, ang, n=16, cup=0.1)
        # half the leaf in cloth stitch, the other half in open half-stitch
        n = len(pts)
        self.cloth.append(pts[: n // 2 + 1] + [(x, y)])
        self.half.append(pts[n // 2:] + [pts[0]])
        self.cords.append((pts, max(1.8, L * 0.06)))
        self.lines.append(([(x, y), (x + math.cos(ang) * L * 0.95, y + math.sin(ang) * L * 0.95)], max(1.4, L * 0.05)))

    def stem(self, pts, w=2.6):
        self.lines.append((curve(pts, 40), w))

    def render(self, net=None, picot=None, extra_cord=None, extra_cloth=None, seed=1, thread="#fffdf7", shade="#cbbcab",
               mesh=None, shadow=0.0):
        W, H = self.W, self.H
        cloth = shapes(W, H, self.cloth) if self.cloth else np.zeros((H, W), np.float32)
        half = shapes(W, H, self.half) if self.half else np.zeros((H, W), np.float32)
        cord = np.zeros((H, W), np.float32)
        by_w = {}
        for pts, w in self.cords:
            by_w.setdefault(round(w, 1), []).append(pts)
        for w, ps in by_w.items():
            cord = np.maximum(cord, outline_paths(W, H, ps, w))
        if self.lines:
            cord = np.maximum(cord, strokes(W, H, [(p, w, (0.1, 0.3)) for p, w in self.lines]))
        if self.dots:
            cloth = np.maximum(cloth, circles(W, H, self.dots))
        if extra_cord is not None:
            cord = np.maximum(cord, extra_cord)
        if extra_cloth is not None:
            cloth = np.maximum(cloth, extra_cloth)
        half = np.clip(half - cloth, 0, 1)
        # half stitch: open diagonal grid, lighter than cloth
        hs = np.maximum(hatch(W, H, 0.78, 3.4, 0.3, seed + 21, wob=0.5), hatch(W, H, 2.36, 3.4, 0.3, seed + 22, wob=0.5))
        weave = np.maximum(hatch(W, H, 1.05, 2.4, 0.66, seed + 9, wob=0.7), hatch(W, H, 2.62, 3.0, 0.42, seed + 11, wob=0.7) * 0.7)
        cl = gaussian_filter(cloth, 0.5)
        hf = gaussian_filter(half, 0.5)
        A_cloth = cl * (0.62 + 0.36 * weave)
        A_half = hf * hs * 0.85
        A_mesh = (mesh if mesh is not None else 0) * (net if net is not None else 0)
        co = gaussian_filter(cord, 0.55)
        pi = gaussian_filter(picot, 0.5) if picot is not None else np.zeros((H, W), np.float32)
        a = np.clip(np.maximum.reduce([np.broadcast_to(A_mesh, (H, W)).astype(np.float32), A_cloth, A_half, co, pi]), 0, 1)
        height = co * 1.0 + cl * 0.45 + hf * 0.25 + pi * 0.7
        light = emboss_light(height, 1.1, 5.0)
        tone = np.clip(0.6 + light * 0.9 + (weave - 0.5) * 0.1 * cl - 0.12 * (1 - co) * cl, 0, 1)
        rgb = ramp(tone, [(0, shade), (0.62, thread), (1, "#ffffff")])
        g = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.6)
        rgb = rgb * (1 + (g[..., None] - 0.5) * 0.05)
        out = rgba(rgb, a)
        if shadow:
            sh = gaussian_filter(np.roll(np.roll(a, 3, 0), 2, 1), 2.0) * shadow
            out = over(flat(np.clip(sh, 0, 1), "#6b5a48"), out)
        return out
