"""Agent I5 helpers (kapas-syari, pop-art, flora-gelap, malam-tahun-baru).
Re-exports _j1_lib (crop-local G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, hatch) plus own media:
form shading, Ben-Day halftone, inked outlines with print misregistration, oil-ish impasto, fireworks.
Previews -> /tmp/pen/nb-I5/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib
from _j1_lib import *  # noqa
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt, binary_dilation

PREV = "/tmp/pen/nb-I5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def flush():
    _art._fbm_cache.clear()


def kb(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")


def rgba(col, a):
    """Flat colour layer with alpha field a (HxW)."""
    rgb = np.ones(a.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(a, 0, 1)[..., None].astype(np.float32)], -1)


def shade_field(mask, light=(-0.7, -0.7), soft=10.0, depth=18.0):
    """0..1 'how much in shadow' for a blob mask lit from `light` (unit-ish vector, screen coords).
    Uses the gradient of a blurred mask (surface normal approximation) plus distance from the rim."""
    m = gaussian_filter(mask.astype(np.float32), soft)
    gy, gx = np.gradient(m)
    n = np.hypot(gx, gy) + 1e-6
    # normal points outward = -gradient; facing light when -grad . light > 0
    facing = (-(gx * light[0] + gy * light[1])) / n
    rim = np.clip(1 - gaussian_filter(mask.astype(np.float32), depth) * 1.6, 0, 1)
    s = 0.5 - 0.5 * facing * np.clip(n * 40, 0, 1)
    return np.clip(s * 0.7 + rim * 0.5, 0, 1) * (mask > 0.02)


def halftone(w, h, tone, spacing=9.0, angle=0.26, gain=1.0, seed=1, jitter=0.25):
    """Ben-Day dot field: dot radius follows tone (0..1). Returns 0..1 coverage mask."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ca, sa = math.cos(angle), math.sin(angle)
    u = (xx * ca + yy * sa) / spacing
    v = (-xx * sa + yy * ca) / spacing
    du = (u % 1.0) - 0.5
    dv = (v % 1.0) - 0.5
    d = np.sqrt(du * du + dv * dv)
    # print wobble per dot
    if jitter:
        nz = fbm(w, h, seed, 7, 2) - 0.5
        d = d + nz * 0.08 * jitter * 4
    r = np.sqrt(np.clip(tone, 0, 1) * gain / math.pi) * 1.0
    return np.clip((r - d) * spacing * 0.9 + 0.5, 0, 1)


def outline(mask, width=6.0, seed=1, wob=1.6, inner=False):
    """Thick brush/ink outline around a mask (comic inking): band between dilated and original edge."""
    m = displace(mask, seed, wob, 30)
    b = gaussian_filter(m, width * 0.5)
    if inner:
        band = np.clip((m - np.clip((b - 0.5) * 3 + 0.5, 0, 1)) * 3, 0, 1)
    else:
        band = np.clip(np.clip((b - 0.02) * 4, 0, 1) - np.clip((m - 0.5) * 3 + 0.5, 0, 1), 0, 1)
    # pressure variation along the line
    pres = 0.65 + 0.7 * fbm(*mask.shape[::-1], seed + 3, 60, 2)
    return np.clip(band * pres * 1.4, 0, 1)


def edge_line(mask, width=5.0, seed=1):
    """Contour line centred on the mask edge, varying width (ink brush)."""
    h, w = mask.shape
    m = gaussian_filter(np.clip(mask, 0, 1), 0.8)
    e = 1 - np.abs(m - 0.5) * 2  # 1 at edge
    e = gaussian_filter(e, width * 0.3)
    pres = 0.6 + 0.8 * fbm(w, h, seed + 3, 50, 2)
    return np.clip((e * pres - 0.25) * 3.0, 0, 1)


def ink(mask, col="#121014", seed=1, wear=0.15):
    """Black printing ink, slightly uneven (letterpress/comic print)."""
    return linocut(mask, col, seed=seed, wear=wear, rough=1.2)


def shift(arr, dx, dy):
    return np.roll(np.roll(arr, dy, 0), dx, 1)


def impasto(mask, light, dark, seed=1, lightdir=(-0.7, -0.75), soft=9.0, streak=0.9, rough=2.5, density=0.97,
            ang=None, hi=None):
    """Oil-ish opaque paint: form shading light->dark, directional brush texture, hand edge, optional highlight colour."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 24)
    m = np.clip((gaussian_filter(m, 0.9) - 0.3) * 2.2, 0, 1)
    sh = shade_field(mask, lightdir, soft, soft * 1.8)
    sh = np.clip(sh + (fbm(w, h, seed + 4, 40, 3) - 0.5) * 0.35, 0, 1)
    ca = np.array(hex_rgb(light), np.float32); cb = np.array(hex_rgb(dark), np.float32)
    rgb = ca * (1 - sh[..., None]) + cb * sh[..., None]
    if hi:
        k = np.clip((0.22 - sh) * 4, 0, 1)[..., None]
        rgb = rgb * (1 - k) + np.array(hex_rgb(hi), np.float32) * k
    if streak:
        a = ang if ang is not None else 0.5
        n = np.random.default_rng(seed).random((h, w)).astype(np.float32)
        s = gaussian_filter(n, (0.6, 5.0)) if abs(math.sin(a)) < 0.5 else gaussian_filter(n, (5.0, 0.6))
        s = (s - s.mean()) / (s.std() + 1e-6)
        rgb = rgb * (1 + s[..., None] * 0.05 * streak)
    return np.concatenate([np.clip(rgb, 0, 1), (m * density)[..., None]], -1)


def IM(dst, mask, *a, pad=16, **k):
    return OV(dst, mask, lambda m: impasto(m, *a, **k), pad=pad)


def soft(dst, mask, col, alpha=0.5, blur=6.0):
    """Soft airless tint/glow (glaze-like) — for chiaroscuro shadows and lights."""
    return over(dst, rgba(col, gaussian_filter(mask, blur) * alpha))


def darken(arr, field, amt=0.6):
    out = arr.copy()
    out[..., :3] *= (1 - np.clip(field, 0, 1)[..., None] * amt)
    return out


def burst_pts(cx, cy, R, r, n, rng, jit=0.18, rot=0.0):
    """Comic explosion/starburst outline with irregular spikes."""
    pts = []
    for i in range(n * 2):
        a = rot + i / (n * 2) * math.tau + rng.uniform(-0.08, 0.08)
        rr = (R if i % 2 == 0 else r) * rng.uniform(1 - jit, 1 + jit * 0.5)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def resample(pts, step):
    out = [pts[0]]
    acc = 0.0
    for i in range(1, len(pts)):
        x0, y0 = out[-1]
        x1, y1 = pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        while d >= step:
            t = step / d
            x0, y0 = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            out.append((x0, y0))
            d = math.hypot(x1 - x0, y1 - y0)
    out.append(pts[-1])
    return out


def firework(W, H, cx, cy, R, rng, rays=36, width=3.0, droop=0.25, n=14):
    """Firework burst: radial trails curving down (gravity), each a tapered stroke; returns (trail mask, tip dots)."""
    items = []
    tips = []
    for i in range(rays):
        a = i / rays * math.tau + rng.uniform(-0.06, 0.06)
        L = R * rng.uniform(0.7, 1.05)
        pts = []
        for k in range(n):
            t = k / (n - 1)
            r0 = L * (0.18 + 0.82 * t)
            x = cx + math.cos(a) * r0
            y = cy + math.sin(a) * r0 + droop * R * t * t
            pts.append((x, y))
        items.append((pts, width * rng.uniform(0.7, 1.2), (0.85, 0.05)))
        tips.append((pts[-1][0], pts[-1][1], width * rng.uniform(0.9, 1.6)))
    return strokes(W, H, items), circles(W, H, tips)
