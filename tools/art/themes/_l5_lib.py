"""Agent L5 helpers (zaitun-syari, alpen-chalet, geode-biru, pesta-teh): _j1_lib local-crop media + own motifs.
Previews -> /tmp/pen/nb-L5/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-L5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def kb_total(d):
    t = sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))
    print("TOTAL", t // 1024, "KB")


def lerp_pts(pts, n):
    """resample a polyline into n points"""
    return curve(pts, n)


def normal_at(pts, i):
    a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1
    return dx / d, dy / d


def ribbon(pts, w0, w1):
    """polygon around a centre polyline with width tapering w0 -> w1"""
    n = len(pts); L = []; R = []
    for i in range(n):
        t = i / (n - 1)
        tx, ty = normal_at(pts, i)
        wd = w0 + (w1 - w0) * t
        L.append((pts[i][0] - ty * wd, pts[i][1] + tx * wd)); R.append((pts[i][0] + ty * wd, pts[i][1] - tx * wd))
    return L + R[::-1]


# ---------------------------------------------------------------- olive
def olive_leaf_pts(x, y, L, ang, width=0.15, bend=0.0):
    """lanceolate olive leaf: long, narrow, pointed; optional bend (curvature)."""
    pts_l, pts_r = [], []
    n = 14
    for i in range(n + 1):
        t = i / n
        hw = L * width * (math.sin(math.pi * t) ** 0.85) * (1.0 - 0.25 * t)
        cx = L * t
        cy = bend * L * (t * t - t) * 0.6
        pts_l.append((cx, cy - hw)); pts_r.append((cx, cy + hw))
    poly = pts_l + pts_r[::-1][1:-1]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in poly]


def olive_leaf(art, W, H, x, y, L, ang, rng, nx, top="#5f7150", under="#a9b59c", silver=None, bend=None, show_under=None):
    """Paint an olive leaf: grey-green top or silvery underside; midrib."""
    bend = rng.uniform(-0.5, 0.5) if bend is None else bend
    show_under = (rng.random() < 0.38) if show_under is None else show_under
    pts = olive_leaf_pts(x, y, L, ang, rng.uniform(0.12, 0.17), bend)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.02))
    if show_under:
        art = G(art, m, under, mix(under, "#d9dfd0", .3), seed=nx(), density=0.62, edge=0.55, bloom=0.3, rough=2.2, feather=0.9)
    else:
        art = G(art, m, top, mix(top, "#2f3b28", .35), seed=nx(), density=0.78, edge=0.6, bloom=0.35, rough=2.2, feather=0.9)
        # silvery sheen half
        half = shape_mask(W, H, olive_leaf_pts(x, y, L * 0.92, ang + (0.05 if bend > 0 else -0.05), 0.07, bend))
        art = G(art, half, silver or "#9fae96", seed=nx(), density=0.28, edge=0.2, bloom=0.2, rough=1.5, feather=1.0)
    rib = [(x + math.cos(ang) * L * t - math.sin(ang) * bend * L * (t * t - t) * 0.6,
            y + math.sin(ang) * L * t + math.cos(ang) * bend * L * (t * t - t) * 0.6) for t in [j / 10 for j in range(1, 10)]]
    art = G(art, stroke_mask(W, H, rib, max(1.0, L * 0.018)), "#e7eadf" if not show_under else "#6f7d63", seed=nx(),
            density=0.4, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    return art, m


def olive_fruit(art, W, H, x, y, r, ang, rng, nx, col="#3a2a35", deep="#1d1620", hi="#8a7a86", ripe=True):
    """oval olive drupe with a soft highlight."""
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r * 1.38, r, 12, ang), rng, 1, 0.03))
    if ripe:
        art = G(art, m, col, deep, seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.6, feather=0.8)
    else:
        art = G(art, m, "#8b9a4e", "#5d6b33", seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.6, feather=0.8)
    hx, hy = x - r * 0.42 * math.cos(ang) + r * 0.25 * math.sin(ang), y - r * 0.42
    hm = shape_mask(W, H, ellipse_pts(hx, hy, r * 0.42, r * 0.2, 10, ang - 0.4))
    art = OV(art, gaussian_filter(hm, 1.6) * 0.65, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb(hi if ripe else "#d5dc9a"), np.float32), (mm)[..., None]], -1))
    return art, m


def olive_branch(art, W, H, spine, rng, nx, leaf_len=(48, 78), every=5, fruit_every=5, fruit_r=11, twig="#6b5a44",
                 stem_w=(6, 1.5), top="#5f7150", under="#a9b59c", fruit=True, side_twigs=True):
    """main twig along spine (control points) with opposite-ish leaf pairs and clustered olives."""
    pts = curve(spine, 80)
    poly = ribbon(pts, stem_w[0], stem_w[1])
    sm = shape_mask(W, H, poly)
    art = G(art, sm, twig, "#4a3e31", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1.2, feather=0.7)
    fruits = []
    n = len(pts)
    k = 0
    for i in range(4, n - 1, every):
        k += 1
        tx, ty = normal_at(pts, i)
        a = math.atan2(ty, tx)
        t = i / n
        L = rng.uniform(*leaf_len) * (1.0 - 0.35 * t)
        for side in (-1, 1):
            if rng.random() < 0.12:
                continue
            la = a + side * rng.uniform(0.3, 0.85)
            off = rng.uniform(0, 6)
            art, _ = olive_leaf(art, W, H, pts[i][0] + tx * off, pts[i][1] + ty * off, L * rng.uniform(.8, 1.15), la, rng, nx, top=top, under=under)
        if rng.random() < 0.3:
            art, _ = olive_leaf(art, W, H, pts[i][0], pts[i][1], L * rng.uniform(.6, .8), a + rng.uniform(-.25, .25), rng, nx, top=top, under=under)
        if fruit and k % fruit_every == 2 and t < 0.85:
            side = rng.choice((-1, 1))
            fa = a + side * 1.2
            fx, fy = pts[i][0] + math.cos(fa) * fruit_r * 1.6, pts[i][1] + abs(math.sin(fa)) * fruit_r * 1.6 + fruit_r * 2.2
            fruits.append((pts[i], fx, fy, rng.randint(1, 3)))
    # tip leaf
    tx, ty = normal_at(pts, n - 1)
    art, _ = olive_leaf(art, W, H, pts[-1][0], pts[-1][1], leaf_len[0] * 0.7, math.atan2(ty, tx), rng, nx, top=top, under=under, show_under=False)
    for (px, py), fx, fy, cnt in fruits:
        for j in range(cnt):
            ox, oy = fx + (j - (cnt - 1) / 2) * fruit_r * 1.9 + rng.uniform(-3, 3), fy + (j % 2) * fruit_r * 0.9 + rng.uniform(-2, 2)
            st = stroke_mask(W, H, curve([(px, py), ((px + ox) / 2 + rng.uniform(-6, 6), (py + oy) / 2 - 4), (ox, oy - fruit_r * 0.8)], 10), 2.0, (0.0, 0.2))
            art = G(art, st, "#7a6a4e", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=0.6, feather=0.5)
            art, _ = olive_fruit(art, W, H, ox, oy, fruit_r * rng.uniform(.85, 1.1), rng.uniform(-.5, .5) + math.pi / 2, rng, nx,
                                 ripe=rng.random() < 0.8)
    return art


# ---------------------------------------------------------------- linen
def linen_tile(n=512, tone="#ece6d8", seed=5, warp=0.08, weft=0.07):
    """seamless woven linen: crossing slub threads + mottle."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    def slub(axis, period, sd):
        r = np.random.default_rng(sd)
        k = n // period
        thick = r.random(k * 4).astype(np.float32)
        base = np.repeat(thick, n // (k * 4) + 1)[:n]
        line = np.sin((xx if axis else yy) / period * math.tau * 1.0) * 0.5 + 0.5
        var = gaussian_filter(r.random((n, n)).astype(np.float32), (40, 1.2) if axis else (1.2, 40), mode="wrap")
        var = (var - var.mean()) / (var.std() + 1e-6)
        idx = (xx if axis else yy).astype(int) % n
        return line * (0.6 + 0.4 * base[idx]) + var * 0.25
    a = slub(1, 3, seed + 1); b = slub(0, 3, seed + 2)
    mott = gaussian_filter(rng.random((n, n)).astype(np.float32), 18, mode="wrap")
    mott = (mott - mott.mean()) / (mott.std() + 1e-6)
    lum = 1 + (a - 0.5) * warp + (b - 0.5) * weft + mott * 0.015
    rgb = np.ones((n, n, 3), np.float32) * np.array(hex_rgb(tone), np.float32) * lum[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)


def paper_tile(n=512, tone="#f4efe4", seed=3, fiber=0.5):
    """seamless watercolour/cotton paper tile."""
    g1 = gaussian_filter(np.random.default_rng(seed).random((n, n)).astype(np.float32), 0.8, mode="wrap")
    g2 = gaussian_filter(np.random.default_rng(seed + 1).random((n, n)).astype(np.float32), 6, mode="wrap")
    g3 = gaussian_filter(np.random.default_rng(seed + 2).random((n, n)).astype(np.float32), 30, mode="wrap")
    nz = lambda g: (g - g.mean()) / (g.std() + 1e-6)
    lum = 1 + nz(g1) * 0.012 * fiber + nz(g2) * 0.012 + nz(g3) * 0.012
    rgb = np.ones((n, n, 3), np.float32) * np.array(hex_rgb(tone), np.float32) * lum[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)


def solid_layer(mask, col):
    return np.concatenate([np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32), np.clip(mask, 0, 1)[..., None]], -1)


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def dabs(art, W, H, mask, col, rng, nx, n=120, size=(6, 14), width=(2.5, 5), ang=None, density=0.55, medium="g", pad=8):
    """short visible brush marks inside a mask (gives gouache/watercolour masses a hand-painted surface)."""
    ys, xs = np.nonzero(mask > 0.5)
    if len(xs) == 0:
        return art
    items = []
    for _ in range(n):
        j = rng.randrange(len(xs))
        x, y = float(xs[j]), float(ys[j])
        a = rng.uniform(-math.pi, math.pi) if ang is None else ang + rng.uniform(-0.35, 0.35)
        L = rng.uniform(*size)
        items.append(([(x - math.cos(a) * L / 2, y - math.sin(a) * L / 2), (x + rng.uniform(-1, 1), y + rng.uniform(-1, 1)), (x + math.cos(a) * L / 2, y + math.sin(a) * L / 2)], rng.uniform(*width), (0.3, 0.4)))
    m = strokes(W, H, items) * np.clip(gaussian_filter(mask, 1.0), 0, 1)
    if medium == "g":
        return GP(art, m * density, col, seed=nx(), rough=0.8, streak=0.6, pad=pad)
    return G(art, m, col, seed=nx(), density=density, edge=0.3, bloom=0.1, rough=1, pad=pad)
