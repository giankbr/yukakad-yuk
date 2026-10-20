"""Shared helpers for agent P8 (saku-biru, poin-ungu, kantong-oranye): painted app backdrops, small gouache mascots."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa
from PIL import Image
from scipy.ndimage import gaussian_filter

PREV = "/tmp/pen/nt3-P8/art"
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


def circle_mask(w, h, cx, cy, r):
    def draw(cv):
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    return mask_from(w, h, draw)


def ring_mask(w, h, cx, cy, r, width):
    def draw(cv):
        cv.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width))
    return mask_from(w, h, draw)


def path_mask(w, h, build, stroke=None):
    def draw(cv):
        p = skia.Path()
        build(p)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style)
            paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap)
            paint.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(p, paint)
    return mask_from(w, h, draw)


def ink_mask(w, h, pts, width, rng, jitter=0.8, taper=(0.2, 0.2)):
    """Hand-inked polyline mask: jittered points + tapered brush width."""
    jp = [(x + rng.gauss(0, jitter), y + rng.gauss(0, jitter)) for x, y in pts]
    return stroke_mask(w, h, jp, width, taper)


def ink(mask, col="#1a1a1a", seed=1, wear=0.18):
    """Ink line layer with a little dry-brush wear so it doesn't read as vector."""
    return linocut(mask, col, seed=seed, wear=wear, rough=1.2)


def shadow(mask, col="#000000", off=(6, 10), blur=10, a=0.22):
    h, w = mask.shape
    m = np.roll(np.roll(mask, off[1], 0), off[0], 1)
    m = gaussian_filter(m, blur) * a
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, m[..., None]], -1)


def soft_light(w, h, cx, cy, r, col, strength=0.5, seed=5):
    """A brushed, mottled spotlight wash (for painted app backdrops)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 0.8)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 1.6
    a *= 0.7 + 0.6 * fbm(w, h, seed, 120, 4)
    streak = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (2.5, 30))
    streak = (streak - streak.mean()) / (streak.std() + 1e-6)
    a = np.clip(a * (1 + streak * 0.08) * strength, 0, 1)
    rgb = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)


def backdrop(w, h, stops, lights, seed=3, grain=0.9, streak=0.9):
    """Opaque painted app backdrop: brushed vertical gradient + a few soft light washes + paper-ish grain."""
    sky = painted_sky(w, h, stops, seed=seed, streak=streak, grain=grain)
    out = sky
    for i, (cx, cy, r, col, k) in enumerate(lights):
        out = over(out, soft_light(w, h, cx, cy, r, col, k, seed=seed + 11 * (i + 1)))
    # fine paper tooth so flat areas aren't digital-smooth
    g = gaussian_filter(np.random.default_rng(seed + 99).random((h, w)).astype(np.float32), 0.9)
    g = (g - g.mean()) / (g.std() + 1e-6)
    mot = fbm(w, h, seed + 77, 160, 4) - 0.5            # large soft wash blotches
    out[..., :3] = np.clip(out[..., :3] * (1 + g[..., None] * 0.012 + mot[..., None] * 0.1), 0, 1)
    return out


def save_opaque(arr, path, quality=78):
    im = Image.fromarray((np.clip(arr[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(path, "WEBP", quality=quality, method=6)
    return im.size


def kb(path):
    return os.path.getsize(path) / 1024
