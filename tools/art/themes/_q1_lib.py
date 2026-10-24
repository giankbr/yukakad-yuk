"""Agent Q1 helpers (pacu-jalur, batik-gentongan, iluminasi-emas, ultah-dokter).
Builds on _o2_lib (which builds on _j1_lib: bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, rect/poly,
gradients, previews). Adds: shaded gouache body, outline, crackle (batik wax veins), scroll/vine generators for
illumination, cartouche outlines. Previews -> /tmp/pen/nb-Q1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib, _j1_lib, _o2_lib
from _o2_lib import *  # noqa
import numpy as np
from scipy.ndimage import gaussian_filter

PREV = "/tmp/pen/nb-Q1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _o2_lib.PREV = PREV


def body(art, m, col, col2=None, seed=1, light=(0.3, 0.2), shade=0.35, dark="#2a1a14", rough=2.0, streak=0.8):
    """Gouache shape with soft shading away from a top-left light."""
    art = GP(art, m, col, col2 or mix_hex(col, "#ffffff", 0.1), seed=seed, rough=rough, streak=streak)
    if shade <= 0:
        return art
    h, w = m.shape
    ys, xs = np.where(m > 0.3)
    if len(xs) == 0:
        return art
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    lx, ly = x0 + (x1 - x0) * light[0], y0 + (y1 - y0) * light[1]
    R = max(x1 - x0, y1 - y0)
    d = np.clip(1 - radial(w, h, lx, ly, R * 1.1), 0, 1)
    return G(art, m * d, mix_hex(col, dark, 0.55), seed=seed + 3, density=shade, edge=0.1, bloom=0.2, rough=1, feather=2, gran=0.15)


def line(art, items, seed, col="#2a1a14", rough=0.9):
    m = strokes(art.shape[1], art.shape[0], items)
    return GP(art, m, col, seed=seed, rough=rough, streak=0.4)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def outline_of(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - mask, 0, 1)


def crackle(W, H, seed, n=40, length=60, width=1.1, wrap=False):
    """Batik wax-crackle veins: branching thin random-walk lines (mask)."""
    rng = random.Random(seed)
    items = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a = rng.uniform(0, math.tau)
        pts = [(x, y)]
        L = rng.uniform(length * 0.4, length)
        s = 0
        while s < L:
            a += rng.gauss(0, 0.35)
            st = rng.uniform(3, 7)
            x += math.cos(a) * st; y += math.sin(a) * st; s += st
            pts.append((x, y))
            if rng.random() < 0.05:
                b = a + rng.choice((-1, 1)) * rng.uniform(0.6, 1.2)
                bx, by = x, y; bp = [(bx, by)]
                for _ in range(rng.randint(3, 8)):
                    b += rng.gauss(0, 0.3); bx += math.cos(b) * 5; by += math.sin(b) * 5; bp.append((bx, by))
                items.append((bp, width * 0.8, None))
        items.append((pts, width, None))
    if wrap:
        out = []
        for pts, w_, t in items:
            for dx in (-W, 0, W):
                for dy in (-H, 0, H):
                    out.append(([(px + dx, py + dy) for px, py in pts], w_, t))
        items = out
    return strokes(W, H, items)


def spiral_scroll(cx, cy, r0, a0, turns, d=1, n=40, shrink=0.82):
    """Rumi/islimi spiral: logarithmic-ish inward curl."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + d * t * turns * math.tau
        r = r0 * (1 - shrink * t)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def tint(m, col, a=1.0):
    return flat(m, col, a)
