"""Agent E1 helpers (rote-sasando, ternate-gamalama, pinisi-makassar, minang-pandai-sikek).
Builds on _d1_lib (thread-level loom, ikat/songket, local-crop G/GP/LC/FO/OV, strokes/shapes) and adds:
  lontar_frond()   fan-palm leaf (lontar / Borassus) as a mask: radiating pleated segments
  lontar_palm()    whole lontar palm (trunk + crown of fans) mask set
  sea()            painted sea with horizontal ripple strokes and light glints
  sun_disc()       soft watercolour sun with halo
  check_cloth()    Makassar silk check (lipa' sabbe) as a woven design index map
Previews -> /tmp/pen/nb-E1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
import _d1_lib
from _d1_lib import *  # noqa
import _p1_lib, _j1_lib
PREV = "/tmp/pen/nb-E1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_d1_lib.PREV = PREV
import numpy as np
from scipy.ndimage import gaussian_filter


def prev_rgb(rgb, name):  # noqa: F811
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def frond_items(cx, cy, r, a0, a1, n, rng, droop=0.0, width=3.0):
    """Stroke items for a fan leaf: n radiating ribs from (cx,cy) spread a0..a1 (radians), length r."""
    items = []
    for k in range(n):
        t = k / max(1, n - 1)
        a = a0 + (a1 - a0) * t + rng.uniform(-0.03, 0.03)
        L = r * (0.82 + 0.18 * math.sin(math.pi * t)) * rng.uniform(0.92, 1.05)
        pts = []
        for j in range(9):
            u = j / 8
            d = u * L
            sag = droop * u * u * L * 0.25
            pts.append((cx + math.cos(a) * d, cy + math.sin(a) * d + sag))
        items.append((pts, width * rng.uniform(0.8, 1.2), (0.05, 0.35)))
    return items


def lontar_frond(W, H, cx, cy, r, ang, spread, rng, n=26, droop=0.3):
    """Fan blade mask (solid) + rib-stroke mask (pleats) for a lontar fan leaf centred on angle `ang`."""
    a0, a1 = ang - spread / 2, ang + spread / 2
    poly_pts = [(cx, cy)]
    for k in range(n + 1):
        t = k / n
        a = a0 + (a1 - a0) * t
        L = r * (0.84 + 0.16 * math.sin(math.pi * t)) * (0.96 + 0.05 * ((k % 2) == 0)) * rng.uniform(0.97, 1.02)
        u = 1.0
        poly_pts.append((cx + math.cos(a) * L, cy + math.sin(a) * L + droop * L * 0.25))
    blade = shapes(W, H, [poly_pts], smooth=False)
    ribs = strokes(W, H, frond_items(cx, cy, r * 1.04, a0, a1, n, rng, droop, 1.4))
    return blade, ribs


def lontar_palm(W, H, x, by, h, rng, lean=0.05, crown=1.0):
    """Lontar palm: tall straight trunk + dense globe of fan leaves.
    Returns (trunk, fans_back, fans_front, ribs, petioles)."""
    tx = x + lean * h
    trunk = strokes(W, H, [(curve([(x, by), (x + lean * h * 0.5, by - h * 0.5), (tx, by - h)], 30), max(4, h * 0.055), (0.0, 0.5))])
    back = np.zeros((H, W), np.float32); front = np.zeros((H, W), np.float32); ribs = np.zeros((H, W), np.float32)
    pet = []
    cy = by - h
    R = h * 0.17 * crown
    k_list = list(range(20))
    rng.shuffle(k_list)
    for j, k in enumerate(k_list):
        a = -math.pi / 2 + (k - 9.5) * 0.3 + rng.uniform(-0.12, 0.12)
        L = R * rng.uniform(0.7, 1.15)
        px, py = tx + math.cos(a) * L * 0.8, cy + math.sin(a) * L * 0.6 + L * 0.2
        pet.append(([(tx, cy + R * 0.1), (px, py)], max(1.2, h * 0.008), (0.0, 0.2)))
        b, r_ = lontar_frond(W, H, px, py, L * 0.7, a, rng.uniform(1.5, 2.3), rng, n=18, droop=0.25)
        if j < 10:
            back = np.maximum(back, b)
        else:
            front = np.maximum(front, b)
        ribs = np.maximum(ribs, r_)
    for (ox, oy, a) in [(-0.25, 0.05, -2.2), (0.25, 0.0, -0.9), (0.0, -0.2, -1.57)]:
        b, r_ = lontar_frond(W, H, tx + ox * R, cy + oy * R + R * 0.25, R * 0.62, a, 3.6, rng, n=26, droop=0.1)
        front = np.maximum(front, b); ribs = np.maximum(ribs, r_)
    return trunk, back, front, ribs, strokes(W, H, pet)


def paint_palm(art, W, H, x, by, h, rng, nx, lean=0.0, crown=1.0, dry=True):
    trunk, back, front, ribs, pet = lontar_palm(W, H, x, by, h, rng, lean=lean, crown=crown)
    art = G(art, trunk, "#6a5a48", "#857059", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=2, gran=0.5)
    tx = x + lean * h
    rings = strokes(W, H, [([(x - h * 0.05, y), (x + h * 0.05, y + 2)], 1.2, None) for y in np.arange(by - h, by, max(5, h * 0.016))])
    art = G(art, rings * trunk, "#3e342a", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    if dry:
        sk = []
        for k in range(12):
            xx0 = tx + (k - 6) * h * 0.012
            sk.append(([(xx0, by - h + h * 0.02), (xx0 + rng.uniform(-1, 1) * h * 0.03, by - h + h * rng.uniform(0.12, 0.2))], max(2, h * 0.009), (0.0, 0.6)))
        art = G(art, strokes(W, H, sk), "#8f6e44", "#a88758", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=1.5)
    art = G(art, back, "#3f6a3e", "#577f47", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=3, gran=0.25)
    art = G(art, pet, "#4f6a38", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=1)
    art = G(art, front, "#6c9650", "#93ad5f", seed=nx(), density=0.85, edge=0.55, bloom=0.35, rough=3, gran=0.25)
    art = G(art, ribs * np.maximum(back, front), "#2f4d28", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1)
    return art


def sea_strokes(W, H, y0, y1, rng, n=220, length=(20, 90), width=(0.8, 2.4)):
    """Horizontal ripple strokes, longer and thinner toward the horizon (perspective)."""
    items = []
    for _ in range(n):
        t = rng.random() ** 1.4
        y = y0 + (y1 - y0) * t
        x = rng.uniform(-40, W + 40)
        L = (length[0] + (length[1] - length[0]) * (0.3 + 0.7 * t)) * rng.uniform(0.6, 1.3)
        wv = width[0] + (width[1] - width[0]) * t
        items.append(([(x, y), (x + L * 0.5, y + rng.uniform(-0.6, 0.6)), (x + L, y + rng.uniform(-0.8, 0.8))], wv, (0.3, 0.4)))
    return strokes(W, H, items)


def sun_disc(W, H, cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    disc = np.clip((r - d) / 2.0, 0, 1)
    halo = np.exp(-((d / (r * 3.2)) ** 2))
    return disc, halo


def check_design(N, bands, base):
    """Plaid / check index map from a list of (start, end, idx) stripe bands applied to warp AND weft.
    Where warp and weft stripes cross, the later-listed band wins (gives the woven check look)."""
    D = np.full((N, N), base, np.int32)
    for (a, b, k) in bands:
        D[:, a:b] = k
    for (a, b, k) in bands:
        D[a:b, :] = np.where(D[a:b, :] == base, k, D[a:b, :])
    return D
