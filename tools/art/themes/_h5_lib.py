"""Agent H5 helpers (mawar-debu, safir-malam, taman-zen, paskah-keluarga).
Re-exports _j1_lib (crop-local G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, engrave) and _j2_lib botanicals
(rose, leaf, bud, peony). Previews -> /tmp/pen/nb-H5/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib
from _j1_lib import *  # noqa
import _j2_lib
from _j2_lib import rose, peony, bud, local, pig, gou, fl, union  # noqa
from _j2_lib import leaf as leaf2  # noqa
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-H5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def flush():
    _art._fbm_cache.clear()


def kb(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")


def star8_pts(cx, cy, R, r, rot=0.0):
    """8-point star polygon (two overlapped squares' outline): alternating outer R / inner r."""
    pts = []
    for i in range(16):
        a = rot + i * math.pi / 8 - math.pi / 2
        rr = R if i % 2 == 0 else r
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def poly_outline(w, h, polys, width, closed=True):
    """Thin even lines along polygons (for silver/ink line work)."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeJoin=skia.Paint.kMiter_Join)
    for pts in polys:
        path = poly_path(pts) if closed else None
        if path is None:
            path = skia.Path(); path.moveTo(*pts[0])
            for q in pts[1:]:
                path.lineTo(*q)
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def silver(mask, seed=1, base="#c9cfd8", emboss=0.5, sparkle=0.18):
    """Silver foil: cool-neutral version of foil()."""
    out = foil(mask, base, seed=seed, emboss=emboss, sparkle=sparkle)
    lum = out[..., :3].mean(-1, keepdims=True)
    tint = np.array(hex_rgb("#dfe6f0"), np.float32)
    out[..., :3] = np.clip(lum * 0.78 * tint / tint.mean() + out[..., :3] * 0.22, 0, 1)
    return out


def SV(dst, mask, pad=10, **k):
    return OV(dst, mask, lambda m: silver(m, **k), pad=pad)


def ripple_field(w, h, centres, spacing=9.0, base_angle=0.0, seed=1, duty=0.42, wob=1.4):
    """Raked-sand line field: straight rake lines that end against concentric (elliptical) rings around stones.
    centres: (cx, cy, rx, ry, rings) — rings follow the stone's own ellipse. Returns (lines 0..1, ring weight)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = (fbm(w, h, seed, 40, 3) - 0.5) * wob * 0.25
    u = (xx * math.sin(base_angle) + yy * math.cos(base_angle)) / spacing + n
    ph = u.copy()
    weight = np.zeros((h, w), np.float32)
    for c in centres:
        cx, cy, rx, ry, rings = c
        k = (rx + ry) / 2
        d = np.hypot((xx - cx) * k / rx, (yy - cy) * k / ry) + n * spacing * 0.6
        rs = k * 1.12
        edge = rs + (rings + 0.5) * spacing
        inside = (d < edge).astype(np.float32)
        ring_ph = (d - rs) / spacing
        ph = np.where(inside > weight, ring_ph, ph)
        weight = np.maximum(weight, inside)
    f = np.abs((ph % 1.0) - 0.5) * 2
    lines = np.clip((duty - f) / 0.22 + 0.5, 0, 1)
    return lines.astype(np.float32), weight


def maple_leaf_pts(cx, cy, s, ang, rng):
    """Japanese maple (7 lobes, palmate, serrated)."""
    lobes = [(-math.pi / 2, 1.0), (-math.pi / 2 - 0.62, 0.88), (-math.pi / 2 + 0.62, 0.88), (-math.pi / 2 - 1.25, 0.66),
             (-math.pi / 2 + 1.25, 0.66), (-math.pi / 2 - 1.95, 0.38), (-math.pi / 2 + 1.95, 0.38)]
    lobes.sort(key=lambda t: t[0])
    pts = []
    for i, (a, L) in enumerate(lobes):
        a2 = a + ang
        L = L * s * rng.uniform(0.92, 1.06)
        w = 0.3
        # notch between lobes
        pts.append((cx + math.cos(a2 - 0.31) * s * 0.38, cy + math.sin(a2 - 0.31) * s * 0.38))
        for t in np.linspace(0.35, 1.0, 5):
            ww = w * (1 - t) ** 0.8 * 1.0 + 0.03
            pts.append((cx + math.cos(a2 - ww) * L * t, cy + math.sin(a2 - ww) * L * t))
        pts.append((cx + math.cos(a2) * L * 1.04, cy + math.sin(a2) * L * 1.04))
        for t in np.linspace(1.0, 0.35, 5):
            ww = w * (1 - t) ** 0.8 * 1.0 + 0.03
            pts.append((cx + math.cos(a2 + ww) * L * t, cy + math.sin(a2 + ww) * L * t))
    # stem gap at the bottom handled by the notch of outer lobes
    return pts


def lily_bloom(W, H, cx, cy, s, ang, rng, sd, white="#fdfbf4", shade="#b3ad8a", green="#a8b878", stam="#b5772f"):
    """Trumpet lily seen from 3/4: six recurved tepals around a green throat, long stamens. Returns layer."""
    lay = blank(W, H)
    ca, sa = math.cos(ang), math.sin(ang)
    # back tepals then front
    order = [(-1.15, 0.92, 0.0), (1.15, 0.92, 0.0), (-0.5, 1.0, 1.0), (0.5, 1.0, 1.0), (-0.0, 0.84, 0.5), (0.0, 1.05, 1.0)]
    throat = (cx, cy)
    for k, (da, Lf, front) in enumerate(order):
        a = ang + da
        L = s * Lf * rng.uniform(0.94, 1.04)
        # tepal: narrow at throat, widest at 60%, tip curls back
        pts_l, pts_r = [], []
        for t in np.linspace(0, 1, 14):
            wdt = s * 0.17 * math.sin(math.pi * min(1, t * 1.05)) ** 0.8 * (1 - 0.2 * t)
            curl = s * 0.16 * max(0, t - 0.65) ** 2 * 6
            px = cx + math.cos(a) * L * t - math.sin(a) * curl * (1 if da >= 0 else -1) * 0.3
            py = cy + math.sin(a) * L * t + curl * 0.6
            nx_, ny_ = -math.sin(a), math.cos(a)
            pts_l.append((px + nx_ * wdt, py + ny_ * wdt)); pts_r.append((px - nx_ * wdt, py - ny_ * wdt))
        poly = deform(pts_l + pts_r[::-1], rng, 1, 0.04)
        m = shape_mask(W, H, poly)
        dens = 0.18 + 0.12 * front
        lay = glaze(lay, pig(m, white, mix(white, shade, 0.35), seed=sd(), density=dens + 0.4, edge=0.8, bloom=0.4, rough=3.5, feather=1.0))
        rim = np.clip(m - gaussian_filter(m, s * 0.035), 0, 1) * 2.0
        lay = glaze(lay, pig(np.clip(rim, 0, 1), shade, seed=sd(), density=0.45, edge=0.3, bloom=0, rough=1.0, feather=0.7))
        # shading along the midrib and at the throat
        rib = [(cx + math.cos(a) * L * t, cy + math.sin(a) * L * t + s * 0.16 * max(0, t - 0.65) ** 2 * 3.6) for t in np.linspace(0.05, 0.85, 10)]
        lay = glaze(lay, pig(stroke_mask(W, H, rib, s * 0.05), shade, seed=sd(), density=0.32, edge=0.3, bloom=0, rough=1.5, feather=1.2))
        base = shape_mask(W, H, ellipse_pts(cx + math.cos(a) * L * 0.18, cy + math.sin(a) * L * 0.18, L * 0.2, s * 0.08, 8, a)) * m
        lay = glaze(lay, pig(base, green, seed=sd(), density=0.38, edge=0.3, bloom=0, rough=2))
    # stamens
    items = []
    tips = []
    for k in range(6):
        a = ang + rng.uniform(-0.45, 0.45)
        L = s * rng.uniform(0.55, 0.75)
        pts = [(cx + math.cos(a) * L * t + math.sin(a) * s * 0.04 * t * t, cy + math.sin(a) * L * t) for t in np.linspace(0, 1, 8)]
        items.append((pts, max(1.2, s * 0.012), (0.0, 0.1)))
        tips.append((pts[-1][0], pts[-1][1], s * 0.045, s * 0.022, math.degrees(a + math.pi / 2)))
    lay = glaze(lay, pig(strokes(W, H, items), "#a9b46a", seed=sd(), density=0.7, edge=0.2, bloom=0, rough=0.8, feather=0.5))
    lay = over(lay, local(gouache_paint, ellipses(W, H, tips), stam, "#8c4f22", seed=sd(), rough=1.2))
    return lay


def egg_pts(cx, cy, r, ang=0.0):
    pts = []
    for i in range(40):
        t = i / 40 * math.tau
        x = math.sin(t) * r * 0.78
        y = -math.cos(t) * r
        y *= 1.0 if y < 0 else 0.82
        x *= 1.0 if -math.cos(t) < 0 else 1.08
        pts.append((x, y))
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in pts]


def resample(pts, step):
    """Polyline resampled at ~fixed arc length (list of (x, y))."""
    out = [pts[0]]; acc = step
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
            acc += step
        acc -= d
    out.append(pts[-1])
    return out
