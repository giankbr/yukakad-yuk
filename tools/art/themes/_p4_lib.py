"""Agent P4 helpers on top of art.py (arena-legenda, hijau-ojek, pesan-antar, game-retro, marketplace)."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

OUT_ROOT = "/root/w/frontend/public/themes/art"
PREV = "/tmp/pen/nt3-P4"


def outdir(theme):
    d = os.path.join(OUT_ROOT, theme)
    os.makedirs(d, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    return d


class Seeds:
    def __init__(self, s=100):
        self.s = s

    def __call__(self):
        self.s += 17
        return self.s


def preview(arr, path, bg="#f6efe6"):
    h, w = arr.shape[:2]
    base = np.asarray(paper(w, h, bg, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(path)


def shade(layer, mask, light=(-0.7, -0.7), k=0.5, blur=6.0, hi="#ffffff", lo="#000000"):
    """Directional form shading inside an object: lighten towards the light, darken away."""
    m = gaussian_filter(mask, blur)
    gy, gx = np.gradient(m)
    d = -(gx * light[0] + gy * light[1])
    d = d / (np.abs(d).max() + 1e-6)
    out = layer.copy()
    hc = np.array(hex_rgb(hi), np.float32); lc = np.array(hex_rgb(lo), np.float32)
    pos = np.clip(d, 0, 1)[..., None] * k; neg = np.clip(-d, 0, 1)[..., None] * k
    out[..., :3] = out[..., :3] * (1 - pos) + hc * pos
    out[..., :3] = out[..., :3] * (1 - neg) + lc * neg
    return out


def tint(layer, mask, col, amt):
    out = layer.copy()
    c = np.array(hex_rgb(col), np.float32)
    m = (np.clip(mask, 0, 1) * amt)[..., None]
    out[..., :3] = out[..., :3] * (1 - m) + c * m
    return out


def ring_mask(w, h, cx, cy, r, width, rng=None, wob=0.0, n=90):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width)
        pts = [(cx + math.cos(t) * (r + (rng.gauss(0, wob) if rng else 0)), cy + math.sin(t) * (r + (rng.gauss(0, wob) if rng else 0)))
               for t in [i / n * math.tau for i in range(n)]]
        cv.c.drawPath(smooth_path(pts), p)
    return mask_from(w, h, draw)


def path_mask(w, h, build, stroke=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(build(), p)
    return mask_from(w, h, draw)


def poly_mask(w, h, pts):
    return shape_mask(w, h, pts, smooth=False)


def rrect_mask(w, h, x, y, rw, rh, r):
    def draw(cv):
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, rw, rh), r, r), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def dots_mask(w, h, pts):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in pts:
            cv.c.drawCircle(x, y, r, p)
    return mask_from(w, h, draw)


def ink(mask, col, seed, density=0.9, rough=1.6):
    """Ink line: slightly bleeding, uneven."""
    return pigment(mask, col, mix(col, "#000000", .15), seed=seed, density=density, edge=0.35, bloom=0.0, gran=0.25,
                   feather=0.55, rough=rough, mottle=0.25)


def outline(mask, width=3.0, blur=0.8):
    """Edge band of a mask (for ink outlines around gouache shapes)."""
    m = np.clip(mask, 0, 1)
    er = gaussian_filter(m, width * 0.5)
    band = np.clip((m - np.clip((er - 0.5) * 3, 0, 1)) * 1.4, 0, 1)
    return gaussian_filter(band, blur)


def inked(mask, col="#1d1a2c", seed=1, width=3.0, density=0.85, wobble=2.0):
    """Hand-inked outline of a shape (wobbly, uneven pressure)."""
    h, w = mask.shape
    m = displace(np.clip(mask, 0, 1), seed, wobble, 22)
    band = outline(m, width)
    press = 0.6 + 0.4 * fbm(w, h, seed + 4, 30, 2)
    band = band * press
    return pigment(band, col, mix(col, "#000000", .2), seed=seed, density=density, edge=0.1, bloom=0.0, gran=0.15, feather=0.4, rough=0.8, mottle=0.15)


def wrap_noise(w, h, rng, sigma):
    n = gaussian_filter(rng.random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def paper_tile(size, tone, seed=3, mottle=1.0, fiber=1.0, fine=1.0):
    rng = np.random.default_rng(seed)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    v = 1 + wrap_noise(size, size, rng, 38) * 0.02 * mottle + wrap_noise(size, size, rng, 10) * 0.01 * mottle \
        + wrap_noise(size, size, rng, 0.7) * 0.012 * fine + wrap_noise(size, size, rng, (0.5, 6)) * 0.01 * fiber
    out = np.clip(base * v[..., None], 0, 1)
    return out


def canvas_tile(size, tone, seed=3, streak=1.0, grain=1.0):
    """Seamless dark painted-canvas tile: brush streaks + weave grain."""
    rng = np.random.default_rng(seed)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    v = 1 + wrap_noise(size, size, rng, (1.0, 14)) * 0.035 * streak + wrap_noise(size, size, rng, 30) * 0.03 \
        + wrap_noise(size, size, rng, 0.6) * 0.02 * grain + wrap_noise(size, size, rng, (6, 0.8)) * 0.012 * grain
    return np.clip(base * v[..., None], 0, 1)


def save(arr, path, max_w=None, q=82, trim=True):
    if trim:
        size = save_asset(arr, path, max_w=max_w, quality=q)
    else:
        im = to_image(arr)
        if max_w and im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(path, "WEBP", quality=q, method=6); size = im.size
    kb = os.path.getsize(path) / 1024
    print(f"{os.path.basename(path)} {size} {kb:.0f}KB")
    return size


def save_rgb(arr, path, max_w=None, q=82):
    im = Image.fromarray((np.clip(arr[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")
    if max_w and im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    print(f"{os.path.basename(path)} {im.size} {os.path.getsize(path) / 1024:.0f}KB")
    return im.size


def ridge_pts(W, H, base_y, amp, rng, n=9, ph=None):
    pts = [(-20, H + 20)]
    ph = rng.uniform(0, 6) if ph is None else ph
    for i in range(n + 1):
        x = -20 + (W + 40) * i / n
        y = H * base_y - amp * (0.6 * math.sin(i * 0.9 + ph) + 0.4 * math.sin(i * 2.1 + ph * 2))
        pts.append((x, y))
    pts.append((W + 20, H + 20))
    return pts


def wobble_rect(x, y, w, h, rng, amt=1.5):
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    return deform(pts, rng, 2, amt / max(w, h))


def union(*masks):
    out = masks[0]
    for m in masks[1:]:
        out = np.maximum(out, m)
    return out


def sub(a, b, grow=0.0):
    if grow:
        b = np.clip(gaussian_filter(b, grow) * 1.8, 0, 1)
    return np.clip(a - b, 0, 1)


# ---------- pixel-art helpers (game-retro) ----------
def pix_up(arr, k):
    """Nearest-neighbour upscale of an (h,w,4) float array by integer k."""
    return np.repeat(np.repeat(arr, k, axis=0), k, axis=1)


def crt(arr, seed=1, scan=0.10, ink=0.06, bleed=0.6, grain=0.04, period=6):
    """Painted-pixel finish: faint scanlines, slight colour bleed, ink speckle, paper grain (keeps alpha)."""
    h, w = arr.shape[:2]
    out = arr.copy()
    yy = np.arange(h)[:, None]
    lines = 1 - scan * (0.5 + 0.5 * np.cos(yy / period * math.tau)) * np.ones((1, w), np.float32)
    if bleed:
        rgb = out[..., :3]
        rgb = gaussian_filter(rgb, (0.0, bleed, 0.0)) * 0.5 + rgb * 0.5
        out[..., :3] = rgb
    g = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.7)
    g = (g - g.mean()) / (g.std() + 1e-6)
    speck = fbm(w, h, seed + 3, 5, 2)
    speck = np.clip((speck - 0.66) * 5, 0, 1) * ink
    out[..., :3] = np.clip(out[..., :3] * lines[..., None] * (1 + g[..., None] * grain) * (1 - speck[..., None]), 0, 1)
    return out
