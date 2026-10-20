"""Shared helpers for agent G's theme scripts (melayu-songket, toraja-tongkonan, dayak-borneo, palembang-aesan)."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
from scipy.ndimage import gaussian_filter

PREV = "/tmp/pen/nt2-G/art"
os.makedirs(PREV, exist_ok=True)


class Seq:
    def __init__(self, start=100):
        self.v = start

    def __call__(self):
        self.v += 17
        return self.v


def outdir(theme):
    d = f"/root/w/frontend/public/themes/art/{theme}"
    os.makedirs(d, exist_ok=True)
    return d


def poly_mask(w, h, pts):
    return shape_mask(w, h, pts, smooth=False)


def circle_mask(w, h, cx, cy, r):
    def draw(cv):
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def ring_mask(w, h, cx, cy, r, width):
    def draw(cv):
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width))
    return mask_from(w, h, draw)


def path_mask(w, h, build, stroke=None, cap=True):
    """build(path) fills a skia.Path; stroke=width draws it as a stroke."""
    def draw(cv):
        p = skia.Path()
        build(p)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style)
            paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
            paint.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(p, paint)
    return mask_from(w, h, draw)


def svg_path(d):
    """Minimal SVG path parser (M L H V C S Q T Z, abs + rel) into a skia.Path."""
    import re
    toks = re.findall(r"[MmLlHhVvCcSsQqTtZz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    p = skia.Path(); i = 0; cmd = None; x = y = 0.0; sx = sy = 0.0; lc = None
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
            y = (y if rel else 0) + num(); p.lineTo(x, y); lc = None
        elif C == "C":
            x1, y1, x2, y2, x3, y3 = ox + num(), oy + num(), ox + num(), oy + num(), ox + num(), oy + num()
            p.cubicTo(x1, y1, x2, y2, x3, y3); lc = (x2, y2); x, y = x3, y3
        elif C == "S":
            x1, y1 = (2 * x - lc[0], 2 * y - lc[1]) if lc else (x, y)
            x2, y2, x3, y3 = ox + num(), oy + num(), ox + num(), oy + num()
            p.cubicTo(x1, y1, x2, y2, x3, y3); lc = (x2, y2); x, y = x3, y3
        elif C == "Q":
            x1, y1, x2, y2 = ox + num(), oy + num(), ox + num(), oy + num()
            p.quadTo(x1, y1, x2, y2); lc = (x1, y1); x, y = x2, y2
        elif C == "T":
            x1, y1 = (2 * x - lc[0], 2 * y - lc[1]) if lc else (x, y)
            x2, y2 = ox + num(), oy + num(); p.quadTo(x1, y1, x2, y2); lc = (x1, y1); x, y = x2, y2
        else:
            i += 1
    return p


def svg_mask(w, h, d, scale=1.0, tx=0.0, ty=0.0, stroke=None, rot=0.0, cx=0.0, cy=0.0, sx=1.0, wob=0.0, seed=1):
    """Mask from an SVG path string: point -> scale(sx*scale, scale) about origin, rotate rot deg about (cx,cy)
    in source units, then translate (tx, ty) in pixels. wob>0 adds hand-drawn wobble to the outline."""
    def draw(cv):
        p = svg_path(d)
        m = skia.Matrix()
        m.setRotate(rot, cx, cy)
        m.postScale(scale * sx, scale)
        m.postTranslate(tx, ty)
        p.transform(m)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style)
            paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap)
            paint.setStrokeJoin(skia.Paint.kRound_Join)
        if wob:
            paint.setPathEffect(skia.DiscretePathEffect.Make(6.0, wob, seed))
        cv.c.drawPath(p, paint)
    return mask_from(w, h, draw)


def wobble(pts, rng, amt=1.5):
    return [(x + rng.gauss(0, amt), y + rng.gauss(0, amt)) for x, y in pts]


def rot_pts(pts, cx, cy, ang):
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def preview(arr, name, tone="#fbf6e4", bg=None):
    """Save a preview: on paper (light) or composited on a flat dark colour."""
    if bg:
        h, w = arr.shape[:2]
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def keep_pixel(arr, x, y):
    """Plant a near-invisible pixel so save_asset's trim keeps a pivot point/canvas bounds."""
    arr[y, x] = [0, 0, 0, 0.02]
    return arr


def save(arr, path, max_w=None, quality=82):
    size = save_asset(arr, path, max_w=max_w, quality=quality)
    print(os.path.basename(path), size, os.path.getsize(path) // 1024, "KB")
    return size


def save_full(arr, path, size=None, quality=82):
    """Save without trimming (keeps exact canvas, for tiles/positioned pieces)."""
    im = to_image(arr)
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size


def wrap_noise(w, h, seed, sigma):
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)
