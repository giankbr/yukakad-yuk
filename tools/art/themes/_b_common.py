"""Agent B helpers on top of art.py (shared by surat-vintage, marmer-rosegold, langit-navy, boho-terakota)."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

OUT_ROOT = "/root/w/frontend/public/themes/art"
PREV = "/tmp/pen/nt2-B"


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
    """Composite RGBA over a flat/paper colour for review."""
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
    m = (mask * amt)[..., None]
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


def text_mask(w, h, txt, x, y, size, family="DejaVu Serif"):
    def draw(cv):
        f = skia.Font(skia.Typeface(family), size)
        cv.c.drawString(txt, x, y, f, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def dots_mask(w, h, pts):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in pts:
            cv.c.drawCircle(x, y, r, p)
    return mask_from(w, h, draw)


def ink(mask, col, seed, density=0.9, rough=1.6):
    """Brown/black ink line: slightly bleeding, uneven."""
    return pigment(mask, col, mix(col, "#000000", .15), seed=seed, density=density, edge=0.35, bloom=0.0, gran=0.25,
                   feather=0.55, rough=rough, mottle=0.25)


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


def wrap_noise(w, h, rng, sigma):
    n = gaussian_filter(rng.random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-6)


def paper_tile(size, tone, seed=3, mottle=1.0, fiber=1.0, fine=1.0, grain_col=None):
    """Seamless paper texture (all filters wrap around)."""
    rng = np.random.default_rng(seed)
    base = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(tone), np.float32)
    v = 1 + wrap_noise(size, size, rng, 38) * 0.02 * mottle + wrap_noise(size, size, rng, 10) * 0.01 * mottle \
        + wrap_noise(size, size, rng, 0.7) * 0.012 * fine + wrap_noise(size, size, rng, (0.5, 6)) * 0.01 * fiber
    out = np.clip(base * v[..., None], 0, 1)
    return out


def grain_overlay(size, col="#5a3c1e", seed=3, base=0.05, k=2.6, cap=0.22, laid=0.0, fox=0, fox_col=None, fiber=1.0, mottle=1.0):
    """Seamless transparent paper-grain overlay tile (RGBA) — drop-in for an SVG noise layer."""
    rng = np.random.default_rng(seed)
    v = wrap_noise(size, size, rng, 30) * 0.018 * mottle + wrap_noise(size, size, rng, 6) * 0.01 * mottle \
        + wrap_noise(size, size, rng, 0.6) * 0.016 + wrap_noise(size, size, rng, (0.5, 7)) * 0.012 * fiber
    a = np.clip(base + v * k, 0, cap)
    if laid:
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
        a += (np.sin(yy / size * math.tau * (size // 4)) * 0.5 + 0.5) * laid + np.exp(-((xx % (size // 4)) - size // 8) ** 2 / 5) * laid * 1.5
    rgb = np.ones((size, size, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    if fox:
        f = np.zeros((size, size), np.float32)
        for _ in range(fox):
            x, y = rng.integers(0, size, 2)
            f[y, x] = rng.uniform(.5, 1)
        f = np.clip(gaussian_filter(f, 2.4, mode="wrap") * 30, 0, 1)
        fc = np.array(hex_rgb(fox_col or "#9a6a35"), np.float32)
        rgb = rgb * (1 - f[..., None]) + fc * f[..., None]
        a = np.maximum(a, f * 0.28)
    return np.concatenate([rgb, a[..., None]], -1)
