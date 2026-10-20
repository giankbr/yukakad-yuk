"""Shared helpers for agent P6 themes (chat-hijau, feed-foto, video-vertikal, kencan, repositori)."""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa

PREV = "/tmp/pen/nt3-P6"
os.makedirs(PREV, exist_ok=True)

class Seeds:
    def __init__(self, start):
        self.v = start
    def __call__(self):
        self.v += 7
        return self.v

def path_mask(W, H, build, stroke=0.0):
    def draw(cv):
        p = skia.Path(); build(p)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style); paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap); paint.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(p, paint)
    return mask_from(W, H, draw)

def circ(W, H, x, y, r):
    return mask_from(W, H, lambda cv: cv.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)))

def rrect(W, H, x, y, w, h, r):
    return mask_from(W, H, lambda cv: cv.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), r, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)))

def poly(W, H, pts, rng=None, wob=0.01, smooth=False):
    if rng is not None:
        pts = deform(pts, rng, 2, wob)
    return shape_mask(W, H, pts, smooth=smooth)

def brush_outline(mask, width, sd, col, col2=None, wobble=0.35, density=0.96):
    """Brush-pen contour around a mask: band around the 0.5 level, width breathing with noise."""
    h, w = mask.shape
    g = gaussian_filter(mask, width * 0.45)
    th = 0.5 * (1 - wobble + wobble * 2 * fbm(w, h, sd, 40, 2))
    tw = th * 0.75
    band = np.clip((tw - np.abs(g - 0.5)) / np.maximum(tw, 0.02) * 2.2, 0, 1)
    return gouache_paint(band, col, col2 or col, seed=sd, rough=1.2, streak=0.3, density=density)

def ink_stroke(W, H, pts, width, col, sd, taper=(0.15, 0.25), dry=0.0):
    m = stroke_mask(W, H, pts, width, taper=taper)
    return linocut(m, col, seed=sd, wear=dry, rough=1.2)

def shade(mask, cx, cy, k=0.25, radius=None):
    """Multiply-darken a painted layer away from a light point (returns rgba with alpha = mask)."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
    f = np.clip(d / (radius or max(w, h) * 0.7), 0, 1)
    return f * k

def darken(layer, mask, cx, cy, k=0.25, radius=None):
    out = layer.copy()
    f = shade(mask, cx, cy, k, radius)
    out[..., :3] *= (1 - f[..., None] * mask[..., None])
    return out

def tint_layer(mask, col, alpha=0.5):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, (mask * alpha)[..., None]], -1)

def save_full(arr, path, size, quality=82):
    to_image(arr).resize(size, Image.LANCZOS).save(path, "WEBP", quality=quality, method=6)
    return os.path.getsize(path)

def preview(arr, path, bg="#ffffff"):
    h, w = arr.shape[:2]
    pv = np.ones((h, w, 4), np.float32); pv[..., :3] = hex_rgb(bg)
    to_image(over(pv, arr)).convert("RGB").save(path)

def sheet(arrs, path, bg="#ffffff", pad=12):
    ims = [to_image(a) for a in arrs]
    W = sum(i.width for i in ims) + pad * (len(ims) + 1); H = max(i.height for i in ims) + pad * 2
    out = Image.new("RGB", (W, H), bg)
    x = pad
    for im in ims:
        out.paste(im, (x, pad), im); x += im.width + pad
    out.save(path)

def grain(arr, seed, amt=0.05):
    """Fine pigment grain in the colour (keeps alpha)."""
    h, w = arr.shape[:2]
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    out = arr.copy()
    out[..., :3] = np.clip(out[..., :3] * (1 + g[..., None] * amt), 0, 1)
    return out

def kb(path):
    return os.path.getsize(path) / 1024

def densify(pts, step=3.0):
    """Resample a polyline so every segment is ~step long (stroke_mask tapers per segment)."""
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L / step))
        for k in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    return out
