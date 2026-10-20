"""Shared helpers for agent H's theme render scripts (ultah-balon, syukuran-rumah, wisuda-toga, tujuh-bulanan).
Builds on /tmp/pen/art/art.py without modifying it."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *  # noqa: F401,F403
from art import np, skia, gaussian_filter, Image

OUT_ROOT = "/root/w/frontend/public/themes/art"
PREV_ROOT = "/tmp/pen/nt2-H"


class Seeds:
    def __init__(self, start=100):
        self.v = start

    def __call__(self):
        self.v += 17
        return self.v


def outdir(theme):
    d = os.path.join(OUT_ROOT, theme)
    os.makedirs(d, exist_ok=True)
    os.makedirs(PREV_ROOT, exist_ok=True)
    return d


def path_mask(w, h, path, stroke=0.0):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(stroke)
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(path, p)
    return mask_from(w, h, draw)


def poly_mask(w, h, pts):
    return shape_mask(w, h, pts, smooth=False)


def rect_pts(x, y, w, h, n=4):
    """Rectangle outline sampled densely so deform() wobbles every side."""
    pts = []
    corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        for k in range(n):
            t = k / n
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return pts


def wobble(pts, rng, amt=0.02, depth=2):
    return deform(pts, rng, depth, amt)


def outline_mask(w, h, pts, width, rng, closed=True, wob=0.012, breaks=0.0):
    """Hand-inked contour: a tapered brush line that follows (a wobbled copy of) the outline."""
    q = deform(pts, rng, 1, wob) if wob else pts
    path = smooth_path(q, closed)
    def draw(cv):
        meas = skia.PathMeasure(path, closed)
        L = meas.getLength()
        n = max(8, int(L / 3))
        prev = None
        for i in range(n + 1):
            d = L * i / n
            pos = meas.getPosTan(d)
            if not pos:
                continue
            (x, y), _ = pos
            if prev is not None:
                t = i / n
                pr = 0.55 + 0.45 * math.sin(math.pi * ((t * 2.3 + 0.2) % 1.0))
                if breaks and rng.random() < breaks:
                    prev = (x, y)
                    continue
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=max(0.8, width * pr),
                               Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                cv.c.drawLine(prev[0], prev[1], x, y, p)
            prev = (x, y)
    return mask_from(w, h, draw)


def line_mask(w, h, pts, width, rng=None, taper=(0.12, 0.2)):
    return stroke_mask(w, h, pts, width, taper)


def sub(a, b):
    return np.clip(a - b, 0, 1)


def inter(a, b):
    return a * b


def union(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = np.maximum(out, m)
    return out


def shift(m, dx, dy):
    return np.roll(np.roll(m, int(dy), 0), int(dx), 1)


def gouache_form(dst, mask, base, shadow, light=None, seed=1, sdx=-0.18, sdy=-0.12, size=None, rough=3.0,
                 streak=0.4, shadow_alpha=0.85, light_alpha=0.8):
    """Opaque gouache object with a soft-edged shadow side. Negative sdx/sdy = light from the top-left (shadow lower-right)."""
    h, w = mask.shape
    dst = over(dst, gouache_paint(mask, base, mix(base, shadow, 0.18), seed=seed, rough=rough, streak=streak))
    ys, xs = np.nonzero(mask > 0.5)
    if len(xs) == 0:
        return dst
    bw = (xs.max() - xs.min()) if size is None else size
    bh = (ys.max() - ys.min()) if size is None else size
    lit = shift(mask, int(bw * sdx), int(bh * sdy))
    shade = sub(mask, gaussian_filter(lit, max(2, bw * 0.06)) * 1.15)
    shade = np.clip(shade, 0, 1) * mask
    sh = gouache_paint(shade, shadow, seed=seed + 3, rough=rough * 0.8, streak=streak)
    sh[..., 3] *= shadow_alpha
    dst = over(dst, sh)
    return dst


def ink(dst, mask, col="#2d2a4a", seed=1, wear=0.25, alpha=0.92):
    l = linocut(mask, col, seed=seed, wear=wear, rough=1.2)
    l[..., 3] *= alpha
    return over(dst, l)


def preview(arr, name, tone="#fbf5ef"):
    on_paper(arr, tone).save(os.path.join(PREV_ROOT, name))


def dab(w, h, cx, cy, rx, ry, rot, rng, n=9, wob=0.12):
    return shape_mask(w, h, deform(ellipse_pts(cx, cy, rx, ry, n, rot), rng, 2, wob))


def paper_tile(path, tone, size=512, seed=3, fiber=0.6, mottle=0.35, quality=72):
    """Seamless paper tile: render larger, then cross-fade edges (mirror blend) so it repeats cleanly."""
    big = np.asarray(paper(size * 2, size * 2, tone, seed, fiber, mottle), np.float32) / 255
    a = big[:size, :size]
    b = np.roll(np.roll(big, size // 2, 0), size // 2, 1)[:size, :size]
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    wx = np.minimum(xx, 1 - xx) * 2; wy = np.minimum(yy, 1 - yy) * 2
    wgt = np.clip(np.minimum(wx, wy) * 3, 0, 1)[..., None]
    # make the tile periodic by blending with its own half-shifted version near the seams
    t = a * wgt + np.roll(np.roll(a, size // 2, 0), size // 2, 1) * (1 - wgt)
    im = Image.fromarray((np.clip(t, 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(path, "WEBP", quality=quality, method=6)
    return os.path.getsize(path)


def report(d):
    tot = 0
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        sz = os.path.getsize(p)
        tot += sz
        im = Image.open(p)
        print(f"  {f:28s} {im.size[0]:4d}x{im.size[1]:<4d} {sz/1024:6.1f} KB")
    print(f"  total {tot/1024:.1f} KB")


def foil_matte(mask, base="#c8a04b", seed=1, emboss=0.5, flat=0.5, wear=0.18, tooth=0.10):
    """Pressed foil toned down to read as printed/hot-stamped foil on paper: flattened sheen, paper tooth,
    a few worn specks where the foil didn't take."""
    f = foil(mask, base, seed=seed, emboss=emboss, sparkle=0.0)
    h, w = mask.shape
    m = np.clip(mask, 0, 1)
    tot = (m.sum() + 1e-6)
    mean = (f[..., :3] * m[..., None]).sum((0, 1)) / tot
    rgb = f[..., :3] * (1 - flat) + mean * flat
    t = fbm(w, h, seed + 4, 30, 3)
    g = gaussian_filter(np.random.default_rng(seed + 2).random((h, w)).astype(np.float32), 0.6)
    g = (g - g.mean()) / (g.std() + 1e-6)
    rgb = rgb * (1 - tooth + tooth * (0.6 + 0.8 * t))[..., None] * (1 + g[..., None] * 0.03)
    speck = fbm(w, h, seed + 9, 5, 2)
    a = f[..., 3] * (1 - wear * np.clip((speck - 0.66) * 5, 0, 1))
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)
