"""Agent H1 helpers (pakpak-dairi, banten-surosowan, ultah-robot, maulid-nabi).
Builds on _g1_lib (bbox-local G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, rect/poly/xgrad/ygrad/radial, mist,
ridge_pts, brick_field, brushwork, kb_report). Adds: brick masses with weathering, ruined wall tops, gear masks,
rounded rectangles, lantern bodies, paper flowers and simple light/shade passes. Previews -> /tmp/pen/nb-H1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib, _j1_lib, _d1_lib, _f2_lib, _g1_lib
from _g1_lib import *  # noqa
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter

PREV = "/tmp/pen/nb-H1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _d1_lib.PREV = _f2_lib.PREV = _g1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def preview(arr, name, tone="#fbf6e4", bg=None):  # noqa: F811
    if bg:
        h, w = arr.shape[:2]
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def rrect(W, H, x0, y0, x1, y1, r):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), p)
    return mask_from(W, H, draw)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def gear_pts(cx, cy, r, teeth, depth=0.18, rot=0.0, n_per=10):
    """Outline of a cog wheel: rounded trapezoid teeth."""
    pts = []
    for k in range(teeth):
        for j in range(n_per):
            t = j / n_per
            a = rot + (k + t) * math.tau / teeth
            # tooth profile: high plateau for the middle 40%, ramps either side
            u = abs(t - 0.5) * 2
            h = 1.0 if u < 0.38 else (0.0 if u > 0.72 else 1 - (u - 0.38) / 0.34)
            rr = r * (1 - depth) + r * depth * h
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def gear_mask(W, H, cx, cy, r, teeth, hole=0.28, spokes=0, depth=0.18, rot=0.0):
    m = shapes(W, H, [gear_pts(cx, cy, r, teeth, depth, rot)], smooth=False)
    m = np.clip(m - circles(W, H, [(cx, cy, r * hole)]), 0, 1)
    if spokes:
        rin = r * (1 - depth) * 0.72
        cut = circles(W, H, [(cx, cy, rin)])
        keep = circles(W, H, [(cx, cy, r * hole * 1.6)])
        sp = []
        for k in range(spokes):
            a = rot + k * math.tau / spokes
            sp.append(([(cx, cy), (cx + math.cos(a) * rin * 1.05, cy + math.sin(a) * rin * 1.05)], r * 0.16, None))
        keep = np.maximum(keep, strokes(W, H, sp))
        m = np.clip(m - cut + keep * cut, 0, 1)
        m = np.clip(m - circles(W, H, [(cx, cy, r * hole)]), 0, 1)
    return m


def bricks(art, W, H, mask, nx, cols, bw=26, bh=9, shade=None, seed=1, mortar=1.6, weather=0.3):
    """Brick mass: gouache base, per-brick tone drift, mortar courses, shade field, chips and stains.
    cols = (base, deep, light, mortar, dark)"""
    base, deep, lite, mort_c, dark = cols
    mask = displace(mask, nx(), 1.6, 14)
    art = GP(art, mask, base, deep, seed=nx(), rough=1.6, streak=0.9)
    bm, tone = brick_field(W, H, bw, bh, mortar, seed)
    art = G(art, bm * mask * np.clip((tone - 0.55) * 2.5, 0, 1), lite, seed=nx(), density=0.55, edge=0.15, rough=0.6, feather=0.5)
    art = G(art, bm * mask * np.clip((0.35 - tone) * 2.5, 0, 1), dark, seed=nx(), density=0.4, edge=0.15, rough=0.6, feather=0.5)
    mort = (1 - bm) * mask * (0.5 + 0.5 * fbm(W, H, nx(), 20, 2))
    art = G(art, mort, mort_c, seed=nx(), density=0.45, edge=0.0, rough=0.4, feather=0.4)
    if shade is not None:
        art = G(art, mask * shade, dark, seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=2, feather=2)
    if weather:
        stain = mask * np.clip((fbm(W, H, nx(), 60, 3) - 0.55) * 2.5, 0, 1) * weather * 2
        art = G(art, stain, "#4f4a3e", seed=nx(), density=0.35, edge=0.3, bloom=0.5, rough=3, feather=3)
    return art


def broken_top(x0, x1, y, rng, amp=26, step=12, bottom=None, stepped=True):
    """Polygon of a ruined wall: jagged, stepped broken crest between x0..x1 at height ~y."""
    pts = [(x0, bottom)]
    x = x0
    yy = y + rng.uniform(-amp, amp) * 0.5
    while x < x1:
        pts.append((x, yy))
        x2 = min(x1, x + rng.uniform(step, step * 3))
        if stepped:
            pts.append((x2, yy))
            yy = min(y + amp, max(y - amp, yy + rng.choice([-1, 1]) * rng.uniform(4, amp * 0.6)))
        else:
            yy = y + rng.uniform(-amp, amp)
        x = x2
    pts.append((x1, yy))
    pts.append((x1, bottom))
    return pts


def side_light(art, W, H, nx, x0, x1, warm="#fff1d6", cool="#2a3a4a", amt=0.5):
    """Light from the left: warm wash on the left of x0..x1, cool shade to the right, only where paint exists."""
    m = art[..., 3]
    art = G(art, m * np.clip(1 - xgrad(W, H, x0, x1), 0, 1) * amt, warm, seed=nx(), density=0.5, edge=0, bloom=0.3, rough=2, feather=3)
    art = G(art, m * xgrad(W, H, x0, x1) * amt, cool, seed=nx(), density=0.5, edge=0, bloom=0.3, rough=2, feather=3)
    return art


def paper_flower(art, W, H, cx, cy, r, nx, rng, col, deep, petals=6, centre="#f3d36b", rot=None):
    """Crinkled crepe-paper flower (kembang kertas): ruffled petals, darker creases, small centre."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    pet = []
    for k in range(petals):
        a = rot + k * math.tau / petals
        pet.append(petal_pts(cx, cy, r, r * 0.62, a, n=12))
    m = displace(shapes(W, H, pet), rng.randint(0, 9999), max(1.0, r * 0.08), max(6, r * 0.5))
    art = GP(art, m, col, mix_hex(col, deep, 0.35), seed=nx(), rough=1.0, streak=0.7, pad=6)
    cr = []
    for k in range(petals):
        a = rot + k * math.tau / petals + rng.uniform(-0.15, 0.15)
        cr.append(([(cx + math.cos(a) * r * 0.25, cy + math.sin(a) * r * 0.25), (cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 0.85)], max(0.8, r * 0.06), (0.2, 0.4)))
    art = G(art, strokes(W, H, cr) * m, deep, seed=nx(), density=0.6, edge=0.2, rough=0.4, feather=0.5, pad=6)
    inner = circles(W, H, [(cx, cy, r * 0.48)])
    art = G(art, inner, deep, seed=nx(), density=0.35, edge=0.5, rough=0.6, feather=0.8, pad=6)
    art = GP(art, circles(W, H, [(cx, cy, r * 0.2)]), centre, mix_hex(centre, "#a0701e", 0.4), seed=nx(), rough=0.5, streak=0.3, pad=4)
    return art


def lantern_glow(art, W, H, cx, cy, r, col, strength=0.6):
    return over(glow(circles(W, H, [(cx, cy, r)]), col, radius=r * 0.8, strength=strength), art)
