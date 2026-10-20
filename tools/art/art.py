"""Painterly raster toolkit for Rawuh theme illustrations (watercolor, gouache, ink, gold foil, paper).

Everything renders into RGBA numpy canvases with skia for anti-aliased geometry; the look comes from many
low-opacity deformed layers (Tyler Hobbs style watercolor), granulation masks, edge darkening, ink jitter
and paper grain — so results read as painted, not as flat vector shapes.
"""
import math, random
import numpy as np
import skia
from PIL import Image, ImageFilter
from opensimplex import OpenSimplex
from scipy.ndimage import gaussian_filter, map_coordinates

# ---------- canvas helpers ----------
class Canvas:
    def __init__(self, w, h, seed=1):
        self.w, self.h = w, h
        self.surface = skia.Surface(w, h)
        self.c = self.surface.getCanvas()
        self.c.clear(skia.ColorTRANSPARENT)
        self.rng = random.Random(seed)
        self.nrng = np.random.default_rng(seed)
        self.noise = OpenSimplex(seed)

    def array(self):
        img = self.surface.makeImageSnapshot()
        return img.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType).astype(np.float32) / 255.0  # premultiplied? skia gives unpremul for toarray

    def save(self, path, scale=1.0, quality=88):
        a = self.array()
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGBA")
        if scale != 1.0:
            im = im.resize((int(self.w * scale), int(self.h * scale)), Image.LANCZOS)
        if path.endswith(".webp"):
            im.save(path, "WEBP", quality=quality, method=6)
        else:
            im.save(path)
        return im

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def color(h, a=1.0):
    r, g, b = hex_rgb(h)
    return skia.Color4f(r, g, b, a)

def mix(h1, h2, t):
    a, b = hex_rgb(h1), hex_rgb(h2)
    return "#%02x%02x%02x" % tuple(int((a[i] * (1 - t) + b[i] * t) * 255) for i in range(3))

def jitter_hex(h, rng, amt=0.06):
    r, g, b = hex_rgb(h)
    f = lambda v: max(0, min(1, v + rng.uniform(-amt, amt)))
    return "#%02x%02x%02x" % (int(f(r) * 255), int(f(g) * 255), int(f(b) * 255))

# ---------- geometry ----------
def poly_path(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for x, y in pts[1:]:
        p.lineTo(x, y)
    p.close()
    return p

def smooth_path(pts, closed=True):
    """Catmull-Rom through points → cubic path."""
    p = skia.Path()
    n = len(pts)
    if n < 3:
        return poly_path(pts)
    p.moveTo(*pts[0])
    rng_ = range(n) if closed else range(n - 1)
    for i in rng_:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(*c1, *c2, *p2)
    if closed:
        p.close()
    return p

def deform(pts, rng, depth, variance, vdiv=2.0, weights=None):
    """Recursive midpoint displacement (watercolor edge)."""
    for _ in range(depth):
        out = []
        n = len(pts)
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]
            out.append(a)
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            w = weights[i % len(weights)] if weights else 1.0
            off = rng.gauss(0, variance * L * w)
            along = rng.gauss(0, variance * L * 0.25)
            out.append((mx + nx * off + dx / L * along, my + ny * off + dy / L * along))
        pts = out
        variance /= vdiv
    return pts

def ellipse_pts(cx, cy, rx, ry, n=10, rot=0.0):
    pts = []
    for i in range(n):
        t = i / n * math.tau
        x, y = math.cos(t) * rx, math.sin(t) * ry
        cr, sr = math.cos(rot), math.sin(rot)
        pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return pts

def petal_pts(cx, cy, length, width, angle, n=14, cup=0.0):
    """Teardrop/petal outline pointing along angle."""
    pts = []
    for i in range(n):
        t = i / n * math.tau
        x = (math.cos(t) * 0.5 + 0.5) * length
        y = math.sin(t) * width * (math.sin(math.pi * (math.cos(t) * 0.5 + 0.5)) ** 0.8 + 0.08)
        y += cup * width * (x / length) ** 2
        ca, sa = math.cos(angle), math.sin(angle)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts

# ---------- painting primitives ----------
def paint_layer(cv, path, hexcol, alpha, blend=skia.BlendMode.kSrcOver, blur=0.0):
    paint = skia.Paint(AntiAlias=True, Color4f=color(hexcol, alpha))
    paint.setBlendMode(blend)
    if blur > 0:
        paint.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    cv.c.drawPath(path, paint)

def watercolor(cv, base_pts, hexcol, layers=28, alpha=0.045, spread=0.35, depth_base=3, depth_layer=3,
               blur=0.6, edge=0.18, granulate=0.0, vary=0.05):
    """A watercolor wash: deform the base, then stack many further-deformed translucent layers."""
    rng = cv.rng
    weights = [rng.uniform(0.4, 1.6) for _ in range(len(base_pts) * 2 ** depth_base)]
    base = deform(base_pts, rng, depth_base, spread * 0.5, weights=None)
    # paint into an offscreen surface so edge darkening / granulation only affect this wash
    off = Canvas(cv.w, cv.h, seed=rng.randint(0, 10**6))
    for i in range(layers):
        pts = deform(base, rng, depth_layer, spread * 0.22, weights=weights)
        col = jitter_hex(hexcol, rng, vary)
        paint_layer(off, smooth_path(pts), col, alpha, blur=blur)
    a = off.array()
    if edge > 0:   # darker pigment pooling at the edges
        al = a[..., 3]
        inner = gaussian_filter(al, 3.0)
        rim = np.clip(al - inner, 0, 1) * edge * 6
        a[..., :3] = a[..., :3] * (1 - rim[..., None] * 0.6)
        a[..., 3] = np.clip(al + rim * 0.5, 0, 1)
    if granulate > 0:
        g = grain_field(cv.w, cv.h, cv.nrng, scale=1.2)
        a[..., 3] *= (1 - granulate) + granulate * g
    composite(cv, a)

def grain_field(w, h, nrng, scale=1.0):
    n = nrng.random((h, w)).astype(np.float32)
    n = gaussian_filter(n, scale)
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return n

def composite(cv, rgba, mode="over"):
    """Alpha-composite an RGBA float array onto the canvas."""
    dst = cv.array()
    sa = rgba[..., 3:4]
    if mode == "multiply":
        out_rgb = dst[..., :3] * (1 - sa) + (dst[..., :3] * rgba[..., :3]) * sa
        out_a = np.clip(dst[..., 3:4] + sa * (1 - dst[..., 3:4]), 0, 1)
        out_rgb = np.where(dst[..., 3:4] > 0, out_rgb, rgba[..., :3])
    else:
        out_a = sa + dst[..., 3:4] * (1 - sa)
        out_rgb = (rgba[..., :3] * sa + dst[..., :3] * dst[..., 3:4] * (1 - sa)) / np.maximum(out_a, 1e-6)
    out = np.concatenate([out_rgb, out_a], axis=-1)
    img = skia.Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    cv.c.clear(skia.ColorTRANSPARENT)
    cv.c.drawImage(img, 0, 0)

def ink_line(cv, pts, hexcol, width=2.0, alpha=0.9, jitter=0.6, taper=True, dry=0.0, passes=1):
    """Hand-inked line: wobble + pressure taper, optional dry-brush breaks."""
    rng = cv.rng
    for _ in range(passes):
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            pressure = math.sin(math.pi * t) ** 0.6 if taper else 1.0
            wdt = max(0.3, width * (0.35 + 0.65 * pressure) * rng.uniform(0.85, 1.15))
            if dry and rng.random() < dry:
                continue
            a, b = pts[i], pts[i + 1]
            j = lambda p: (p[0] + rng.gauss(0, jitter), p[1] + rng.gauss(0, jitter))
            paint = skia.Paint(AntiAlias=True, Color4f=color(hexcol, alpha), StrokeWidth=wdt, Style=skia.Paint.kStroke_Style,
                               StrokeCap=skia.Paint.kRound_Cap)
            cv.c.drawLine(*j(a), *j(b), paint)

def curve(points, steps=60):
    """Sample a smooth Catmull-Rom curve through control points (open)."""
    out = []
    n = len(points)
    for i in range(n - 1):
        p0 = points[max(0, i - 1)]; p1 = points[i]; p2 = points[i + 1]; p3 = points[min(n - 1, i + 2)]
        for s in range(steps // (n - 1)):
            t = s / (steps // (n - 1))
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out

def gouache(cv, base_pts, hexcol, alpha=0.92, rough=0.12, texture=0.25, shade=None):
    """Opaque matte paint with slightly rough edge and brush texture (folk-art / adat look)."""
    rng = cv.rng
    pts = deform(base_pts, rng, 3, rough * 0.3)
    off = Canvas(cv.w, cv.h, seed=rng.randint(0, 10**6))
    paint_layer(off, smooth_path(pts), hexcol, alpha, blur=0.4)
    a = off.array()
    if texture:
        streak = gaussian_filter(cv.nrng.random((cv.h, cv.w)).astype(np.float32), (0.6, 4.0))
        streak = (streak - streak.mean()) / (streak.std() + 1e-6)
        a[..., :3] = np.clip(a[..., :3] * (1 + streak[..., None] * texture * 0.08), 0, 1)
    if shade:
        # soft inner shading towards one side
        yy, xx = np.mgrid[0:cv.h, 0:cv.w].astype(np.float32)
        sx, sy, k = shade
        d = ((xx - sx) ** 2 + (yy - sy) ** 2) ** 0.5
        f = np.clip(d / (max(cv.w, cv.h) * 0.6), 0, 1)
        a[..., :3] *= (1 - f[..., None] * k)
    composite(cv, a)

def gold_foil(cv, path, base="#c9a14a", shine=0.55, grain=0.5):
    """Metallic gold: anisotropic sheen + noise, masked by path."""
    mask = Canvas(cv.w, cv.h)
    paint_layer(mask, path, "#ffffff", 1.0)
    m = mask.array()[..., 3]
    yy, xx = np.mgrid[0:cv.h, 0:cv.w].astype(np.float32)
    band = 0.5 + 0.5 * np.sin((xx * 0.9 + yy * 0.45) / (cv.w * 0.09))
    band = gaussian_filter(band, 2)
    n = grain_field(cv.w, cv.h, cv.nrng, 0.8)
    r, g, b = hex_rgb(base)
    lum = 0.62 + shine * (band - 0.5) + grain * 0.12 * (n - 0.5)
    rgb = np.stack([np.clip(r * lum * 1.25, 0, 1), np.clip(g * lum * 1.22, 0, 1), np.clip(b * lum * 1.1, 0, 1)], -1)
    composite(cv, np.concatenate([rgb, m[..., None]], -1))

# ---------- surfaces ----------
def paper(w, h, tone="#f6efe6", seed=3, fiber=0.5, mottle=0.5):
    """Paper/linen background texture (opaque)."""
    rng = np.random.default_rng(seed)
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    big = gaussian_filter(rng.random((h, w)).astype(np.float32), 40)
    big = (big - big.mean()) / (big.std() + 1e-6)
    fine = gaussian_filter(rng.random((h, w)).astype(np.float32), 0.7)
    fine = (fine - fine.mean()) / (fine.std() + 1e-6)
    fib = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.5, 6))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    v = 1 + big * 0.018 * mottle + fine * 0.012 + fib * 0.01 * fiber
    out = np.clip(base * v[..., None], 0, 1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGB")

def save_rgba(arr, path, size=None, quality=86):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im

# =====================================================================
# Pixel-based watercolor (v2): geometry → mask → pigment simulation.
# =====================================================================
_fbm_cache = {}
def fbm(w, h, seed, scale=80.0, octaves=4):
    """Fractal value noise in [0,1] (fast: blurred random grids, multi-octave)."""
    key = (w, h, seed, scale, octaves)
    if key in _fbm_cache:
        return _fbm_cache[key]
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    s = scale
    for _ in range(octaves):
        gh, gw = max(2, int(h / s) + 2), max(2, int(w / s) + 2)
        g = rng.random((gh, gw)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, np.float32) / 255 * amp
        tot += amp; amp *= 0.5; s /= 2
    out /= tot
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    _fbm_cache[key] = out
    return out

def mask_from(w, h, draw):
    """draw(canvas) paints white geometry; returns float mask [0,1]."""
    cv = Canvas(w, h)
    draw(cv)
    return cv.array()[..., 3]

def displace(mask, seed, amount=6.0, scale=40.0):
    h, w = mask.shape
    nx = fbm(w, h, seed, scale, 3) - 0.5
    ny = fbm(w, h, seed + 1, scale, 3) - 0.5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return map_coordinates(mask, [yy + ny * amount * 2, xx + nx * amount * 2], order=1, mode="constant")

def pigment(mask, col_a, col_b=None, seed=1, density=0.85, edge=0.55, bloom=0.35, gran=0.25, feather=1.6,
            rough=7.0, mottle=0.5, holes=0.0):
    """Turn a shape mask into a watercolor wash (RGBA float)."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 36)
    m = gaussian_filter(m, feather)
    # wet edge: pigment pools where the mask falls off
    inner = gaussian_filter(m, 5.0)
    rim = np.clip(m - inner, 0, 1)
    rim = gaussian_filter(rim, 0.8) * (0.6 + 0.8 * fbm(w, h, seed + 7, 22, 3))
    low = fbm(w, h, seed + 3, 120, 3)
    a = m * density * (1 - mottle * 0.55 + mottle * 0.55 * low)
    # blooms / back-runs: lighter cauliflower patches inside
    if bloom:
        b = fbm(w, h, seed + 11, 46, 4)
        a *= 1 - bloom * np.clip((b - 0.55) * 3.0, 0, 1)
    if holes:
        hfield = fbm(w, h, seed + 21, 18, 3)
        a *= 1 - np.clip((hfield - (1 - holes)) * 6, 0, 1)
    a += rim * edge * 1.6
    if gran:
        g = gaussian_filter(np.random.default_rng(seed + 5).random((h, w)).astype(np.float32), 0.7)
        g = (g - g.min()) / (g.max() - g.min())
        a *= (1 - gran) + gran * (0.55 + 0.9 * g)
    a = np.clip(a, 0, 1)
    ca = np.array(hex_rgb(col_a), np.float32)
    cb = np.array(hex_rgb(col_b or col_a), np.float32)
    t = fbm(w, h, seed + 13, 70, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    # thicker pigment = slightly darker/more saturated
    rgb = rgb * (1 - 0.25 * (a[..., None] - 0.5))
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)

def over(dst, src):
    """Porter-Duff over for float RGBA arrays (unpremultiplied)."""
    sa = src[..., 3:4]; da = dst[..., 3:4]
    oa = sa + da * (1 - sa)
    rgb = (src[..., :3] * sa + dst[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6)
    return np.concatenate([rgb, oa], -1)

def glaze(dst, src):
    """Watercolor glazing: transparent layers darken like multiply where they overlap."""
    sa = src[..., 3:4]; da = dst[..., 3:4]
    oa = sa + da * (1 - sa)
    mult = dst[..., :3] * src[..., :3]
    rgb_overlap = mult * 0.55 + src[..., :3] * 0.45
    rgb = np.where(da > 0.02, (rgb_overlap * sa * da + src[..., :3] * sa * (1 - da) + dst[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6), src[..., :3])
    return np.concatenate([np.clip(rgb, 0, 1), oa], -1)

def blank(w, h):
    return np.zeros((h, w, 4), np.float32)

def stroke_mask(w, h, pts, width, taper=(0.15, 0.25)):
    """Brush stroke along a polyline: width tapers at both ends (comma / petal strokes)."""
    def draw(cv):
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            k = min(1.0, t / taper[0]) if t < taper[0] else (min(1.0, (1 - t) / taper[1]) if t > 1 - taper[1] else 1.0)
            wdt = max(0.6, width * (0.25 + 0.75 * k))
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
            cv.c.drawLine(*pts[i], *pts[i + 1], p)
    return mask_from(w, h, draw)

def shape_mask(w, h, pts, smooth=True):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.drawPath(smooth_path(pts) if smooth else poly_path(pts), p)
    return mask_from(w, h, draw)

def arc_pts(cx, cy, r, a0, a1, n=24, squash=1.0):
    return [(cx + math.cos(a0 + (a1 - a0) * i / (n - 1)) * r, cy + math.sin(a0 + (a1 - a0) * i / (n - 1)) * r * squash) for i in range(n)]

def to_image(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA")

def on_paper(arr, tone="#fbf5ef", seed=3):
    h, w = arr.shape[:2]
    bg = np.asarray(paper(w, h, tone, seed), np.float32) / 255
    a = arr[..., 3:4]
    # multiply-like so paper texture shows through pigment
    rgb = bg * (1 - a) + (bg * arr[..., :3]) ** 0.85 * a
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")

# ---------- v2 helpers: knock-out, gouache, linocut, foil, glow, sky ----------
def knockout(layer, mask, amount=0.9, grow=6.0):
    """Remove pigment under a (dilated) mask — paint 'behind' an object already on the page."""
    m = np.clip(gaussian_filter(mask, grow) * 2.2, 0, 1)
    out = layer.copy()
    out[..., 3] *= 1 - m * amount
    return out

def gouache_paint(mask, col, col2=None, seed=1, rough=3.5, streak=0.5, dry=0.0, density=0.96):
    """Opaque matte gouache/poster paint: crisp-but-hand-cut edge, brush streak texture, slight tonal drift."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 28)
    m = np.clip((gaussian_filter(m, 0.7) - 0.35) * 2.2, 0, 1)
    if dry:
        d = fbm(w, h, seed + 9, 10, 2)
        m *= 1 - np.clip((d - (1 - dry)) * 5, 0, 1) * (1 - gaussian_filter(mask, 6) > 0.0)
    ca = np.array(hex_rgb(col), np.float32); cb = np.array(hex_rgb(col2 or col), np.float32)
    t = fbm(w, h, seed + 3, 90, 3)[..., None]
    rgb = ca * (1 - t) + cb * t
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.5, 5.0))
    s = (s - s.mean()) / (s.std() + 1e-6)
    rgb = rgb * (1 + s[..., None] * 0.035 * streak)
    return np.concatenate([np.clip(rgb, 0, 1), (m * density)[..., None]], -1)

def linocut(mask, col, seed=1, wear=0.35, rough=2.0):
    """Relief-print ink: slightly uneven coverage, speckles where ink didn't take, soft-crisp edge."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 18)
    m = np.clip((gaussian_filter(m, 0.6) - 0.4) * 3, 0, 1)
    speck = fbm(w, h, seed + 5, 6, 2)
    coverage = 1 - wear * np.clip((speck - 0.62) * 4, 0, 1)
    tone = 0.92 + 0.08 * fbm(w, h, seed + 8, 60, 2)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32) * tone[..., None]
    return np.concatenate([rgb, (m * coverage)[..., None]], -1)

def foil(mask, base="#c8a04b", seed=1, emboss=0.6, sparkle=0.25):
    """Pressed gold foil: metallic sheen bands + emboss highlight/shadow + fine sparkle."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.5), 0, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sheen = 0.5 + 0.5 * np.sin((xx * 0.8 + yy * 0.5) / max(18, w * 0.06) + fbm(w, h, seed, 50, 2) * 3)
    gy, gx = np.gradient(gaussian_filter(m, 1.5))
    light = np.clip(0.5 - (gx + gy) * 6 * emboss, 0, 1)
    spark = (np.random.default_rng(seed).random((h, w)) > 0.995).astype(np.float32)
    spark = gaussian_filter(spark, 0.6) * 6 * sparkle
    r, g, b = hex_rgb(base)
    lum = 0.55 + 0.45 * sheen * 0.8 + (light - 0.5) * 0.7 + spark
    rgb = np.stack([np.clip(r * lum * 1.18, 0, 1), np.clip(g * lum * 1.15, 0, 1), np.clip(b * lum * 1.02, 0, 1)], -1)
    return np.concatenate([rgb, m[..., None]], -1)

def glow(mask, col, radius=24, strength=0.8):
    a = np.clip(gaussian_filter(mask, radius) * strength * 2.5, 0, 1)
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)

def painted_sky(w, h, stops, seed=1, streak=0.6, grain=0.5):
    """Hand-painted gradient (vertical stops [(t, hex)]) with horizontal brush streaks and grain; opaque RGBA."""
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32)
    wob = (fbm(w, h, seed, 140, 3) - 0.5) * 0.08
    t = np.clip(t + wob, 0, 1)
    rgb = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        k = np.clip((t - t0) / max(1e-6, t1 - t0), 0, 1)
        sel = (t >= t0) & (t <= t1)
        ca = np.array(hex_rgb(c0), np.float32); cb = np.array(hex_rgb(c1), np.float32)
        rgb[sel] = (ca * (1 - k[..., None]) + cb * k[..., None])[sel]
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (1.2, 18))
    s = (s - s.mean()) / (s.std() + 1e-6)
    g = gaussian_filter(np.random.default_rng(seed + 1).random((h, w)).astype(np.float32), 0.6)
    g = (g - g.mean()) / (g.std() + 1e-6)
    rgb = rgb * (1 + s[..., None] * 0.02 * streak + g[..., None] * 0.015 * grain)
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1), np.float32)], -1)

def save_asset(arr, path, max_w=None, quality=84):
    """Trim fully transparent margins, optionally downscale, save WebP. Returns (w, h)."""
    im = to_image(arr)
    bbox = im.getchannel("A").point(lambda v: 255 if v > 3 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    if max_w and im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size

def save_texture(img_or_arr, path, quality=80):
    im = img_or_arr if isinstance(img_or_arr, Image.Image) else to_image(img_or_arr)
    im.save(path, "WEBP", quality=quality, method=6)
