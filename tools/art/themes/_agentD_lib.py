"""Agent D helpers (used by kaligrafi-emas / masjid-biru / sakinah-putih / arabesque-marun scripts).
Extends /tmp/pen/art/art.py without editing it: seamless textures, dark-background previews, star geometry."""
import sys, math, os, re
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from scipy.ndimage import gaussian_filter as _gf

OUT_ROOT = "/root/w/frontend/public/themes/art"
PREV = "/tmp/pen/nt2-D"


def outdir(theme):
    d = os.path.join(OUT_ROOT, theme)
    os.makedirs(d, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    return d


def wrap_noise(w, h, seed, sigma):
    """Seamless (wrap-around) normalised noise, zero mean / unit std."""
    n = np.random.default_rng(seed).random((h, w)).astype(np.float32)
    n = _gf(n, sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def wrap_fbm(w, h, seed, scale=60.0, octaves=3):
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0; s = scale
    for i in range(octaves):
        out += wrap_noise(w, h, seed + i * 31, s / 3) * amp
        tot += amp; amp *= 0.5; s /= 2
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def seamless_paper(w, h, tone, seed=3, mottle=1.0, fiber=1.0, fine=1.0):
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    v = (1 + wrap_noise(w, h, seed, 30) * 0.02 * mottle + wrap_noise(w, h, seed + 1, 0.7) * 0.012 * fine
         + wrap_noise(w, h, seed + 2, (0.5, 6)) * 0.01 * fiber)
    out = np.clip(base * v[..., None], 0, 1)
    return np.concatenate([out, np.ones((h, w, 1), np.float32)], -1)


def wrap_draw(w, h, draw):
    """Draw geometry 9 times offset by the tile size so shapes crossing an edge wrap around."""
    def d(cv):
        for ox in (-w, 0, w):
            for oy in (-h, 0, h):
                cv.c.save(); cv.c.translate(ox, oy); draw(cv); cv.c.restore()
    return mask_from(w, h, d)


def preview(arr, bg="#ffffff", path=None, paper_tone=None):
    """Composite RGBA art over a flat colour (dark themes) or paper (light) for viewing."""
    h, w = arr.shape[:2]
    if paper_tone:
        im = on_paper(arr, paper_tone)
    else:
        b = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = b * (1 - a) + arr[..., :3] * a
        im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if path:
        im.save(path)
    return im


def star_pts(cx, cy, outer, inner, n=8, rot=-math.pi / 2):
    return [(cx + math.cos(rot + math.pi / n * i) * (outer if i % 2 == 0 else inner),
             cy + math.sin(rot + math.pi / n * i) * (outer if i % 2 == 0 else inner)) for i in range(2 * n)]


def square_pts(cx, cy, r, rot=0.0):
    return [(cx + math.cos(rot + math.pi / 4 + math.pi / 2 * i) * r * math.sqrt(2),
             cy + math.sin(rot + math.pi / 4 + math.pi / 2 * i) * r * math.sqrt(2)) for i in range(4)]


def outline_mask(w, h, pts_list, width, closed=True, rng=None, wobble=0.0):
    """Stroked outlines (hand wobble optional) → mask."""
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap)
        for pts in pts_list:
            q = pts
            if rng is not None and wobble:
                q = [(x + rng.gauss(0, wobble), y + rng.gauss(0, wobble)) for x, y in pts]
            path = poly_path(q) if closed else _open_path(q)
            cv.c.drawPath(path, p)
    return mask_from(w, h, draw)


def _open_path(pts):
    p = skia.Path(); p.moveTo(*pts[0])
    for x, y in pts[1:]:
        p.lineTo(x, y)
    return p


def parse_svg_path(d):
    """Minimal SVG path parser (M L H V C S Q Z A, abs + rel) → skia.Path."""
    toks = re.findall(r"[MmLlHhVvCcSsQqZzAa]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?", d)
    p = skia.Path(); i = 0; cmd = None; x = y = sx = sy = 0.0; lc = None
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                p.close(); x, y = sx, sy; lc = None; continue
        rel = cmd.islower(); C = cmd.upper()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if C == "M":
            x, y = ox + num(), oy + num(); p.moveTo(x, y); sx, sy = x, y; cmd = "l" if rel else "L"; lc = None
        elif C == "L":
            x, y = ox + num(), oy + num(); p.lineTo(x, y); lc = None
        elif C == "H":
            x = ox + num(); p.lineTo(x, y); lc = None
        elif C == "V":
            y = (y if rel else 0.0) + num(); p.lineTo(x, y); lc = None
        elif C == "C":
            x1, y1, x2, y2, x3, y3 = ox + num(), oy + num(), ox + num(), oy + num(), ox + num(), oy + num()
            p.cubicTo(x1, y1, x2, y2, x3, y3); lc = (x2, y2); x, y = x3, y3
        elif C == "S":
            x1, y1 = (2 * x - lc[0], 2 * y - lc[1]) if lc else (x, y)
            x2, y2, x3, y3 = ox + num(), oy + num(), ox + num(), oy + num()
            p.cubicTo(x1, y1, x2, y2, x3, y3); lc = (x2, y2); x, y = x3, y3
        elif C == "Q":
            x1, y1, x3, y3 = ox + num(), oy + num(), ox + num(), oy + num()
            p.quadTo(x1, y1, x3, y3); lc = None; x, y = x3, y3
        elif C == "A":
            rx, ry, rot, la, sw = num(), num(), num(), num(), num()
            x3, y3 = ox + num(), oy + num()
            p.arcTo(rx, ry, rot, skia.Path.ArcSize.kLarge_ArcSize if la else skia.Path.ArcSize.kSmall_ArcSize,
                    skia.PathDirection.kCW if sw else skia.PathDirection.kCCW, x3, y3)
            x, y = x3, y3; lc = None
    return p


def svg_mask(w, h, ds, scale=1.0, tx=0.0, ty=0.0, stroke=None, fill=True, matrix=None):
    """Rasterise SVG path strings into a mask (fill and/or stroke). matrix: optional (a,b,c,d,e,f) pre-transform."""
    if isinstance(ds, str):
        ds = [ds]
    def draw(cv):
        cv.c.save(); cv.c.translate(tx, ty); cv.c.scale(scale, scale)
        if matrix:
            a, b, c, d_, e, f = matrix
            cv.c.concat(skia.Matrix.MakeAll(a, c, e, b, d_, f, 0, 0, 1))
        for d in ds:
            path = parse_svg_path(d)
            if fill:
                cv.c.drawPath(path, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
            if stroke:
                cv.c.drawPath(path, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=stroke / scale, Style=skia.Paint.kStroke_Style,
                                               StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))
        cv.c.restore()
    return mask_from(w, h, draw)


def circle_mask(w, h, circles, stroke=None):
    """circles: [(cx, cy, r)] filled (stroke=None) or stroked."""
    def draw(cv):
        for cx, cy, r in circles:
            if stroke:
                cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=stroke, Style=skia.Paint.kStroke_Style))
            else:
                cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def save_plain(arr, path, quality=82, size=None):
    """Save without trimming (for border-image / textures where geometry must stay put)."""
    im = to_image(arr)
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def kb(path):
    return round(os.path.getsize(path) / 1024, 1)
