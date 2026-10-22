"""Agent G1 helpers (gayo-kerawang, kerinci-danau, menara-kudus, kawin-emas).
Builds on _f2_lib (bbox-cropped G/GP/LC/FO/OV, strokes/shapes/circles/ellipses, Embroidery chain stitch, ygrad/xgrad/radial,
comp_rgb, rgb_save, kb_report). Adds: mist banks, layered hills, cloth texture, brick courses, chrysanthemum.
Previews -> /tmp/pen/nb-G1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
sys.path.insert(0, "/tmp/pen/art")
import _p1_lib, _j1_lib, _d1_lib, _f2_lib
from _f2_lib import *  # noqa
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt

PREV = "/tmp/pen/nb-G1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _d1_lib.PREV = _f2_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def prev_rgb(rgb, name):  # noqa: F811
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def preview(arr, name, tone="#fbf6e4", bg=None):  # noqa: F811
    if bg:
        h, w = arr.shape[:2]
        base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
        a = arr[..., 3:4]
        rgb = base * (1 - a) + arr[..., :3] * a
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")
    else:
        on_paper(arr, tone).save(f"{PREV}/{name}.png")


def mist(W, H, bands, nx, rng, col="#f4f2ee", col2=None):
    """Soft horizontal mist banks: [(y, thickness, x0, x1, density)]."""
    art = blank(W, H)
    for y, th, x0, x1, dens in bands:
        blobs = []
        x = x0
        while x < x1:
            r = th * rng.uniform(1.6, 3.2)
            blobs.append((x, y + rng.uniform(-0.3, 0.3) * th, r, th * rng.uniform(0.45, 0.8), rng.uniform(-3, 3)))
            x += r * 0.9
        m = displace(ellipses(W, H, blobs), nx(), th * 0.4, max(12, th))
        art = G(art, m, col, col2 or mix_hex(col, "#dfe3e6", 0.5), seed=nx(), density=dens, edge=0.05, bloom=0.45,
                rough=th * 0.3, feather=th * 0.35, gran=0.02, pad=int(th * 2))
    return art


def ridge_pts(W, base, amp, rng, step=14, freq=(1.3, 3.1), phase=None, bottom=None):
    phase = phase if phase is not None else (rng.uniform(0, 6), rng.uniform(0, 6))
    pts = []
    x = -20
    while x <= W + 20:
        y = base - amp * (0.5 + 0.35 * math.sin(x / W * math.tau * freq[0] + phase[0]) + 0.15 * math.sin(x / W * math.tau * freq[1] + phase[1]))
        pts.append((x, y + rng.uniform(-1.5, 1.5)))
        x += step
    b = bottom if bottom is not None else base + 2000
    return [(-20, b)] + pts + [(W + 20, b)]


def cloth(W, H, base="#17130f", seed=1, tile=True, weave=2.2, strength=0.10):
    """Plain-woven cotton (black kerawang ground): warp/weft micro-ribs, slub, soft mottling. RGB float."""
    rng = np.random.default_rng(seed)
    md = "wrap" if tile else "nearest"
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wx = 0.5 + 0.5 * np.sin(xx / weave * math.pi)
    wy = 0.5 + 0.5 * np.sin(yy / weave * math.pi)
    checker = np.where((np.floor(xx / weave) + np.floor(yy / weave)) % 2 == 0, wx, wy)
    slubx = gaussian_filter(rng.random((1, W)).astype(np.float32), (0, 1.5), mode=md)
    sluby = gaussian_filter(rng.random((H, 1)).astype(np.float32), (1.5, 0), mode=md)
    slub = (slubx - slubx.mean()) * 2 + (sluby - sluby.mean()) * 2
    mott = gaussian_filter(rng.random((H, W)).astype(np.float32), W / 10, mode=md)
    mott = (mott - mott.mean()) / (mott.std() + 1e-6)
    v = 1 + (checker - 0.5) * strength * 2 + slub * strength * 1.4 + mott * 0.05
    rgb = np.ones((H, W, 3), np.float32) * col_arr(base) * v[..., None]
    lift = np.clip(checker - 0.6, 0, 1)[..., None] * 0.03
    return np.clip(rgb + lift, 0, 1)


def emb_to_arr(emb):
    return emb.array()


def satin_fill(emb, mask, col, ang=0.6, spacing=1.6, light=None, dark=None):
    """Satin stitch: parallel thread strokes across a shape at angle ang, each stroke shaded (sheen in middle)."""
    h, w = mask.shape
    light = light or mix_hex(col, "#fff4dc", 0.5); dark = dark or mix_hex(col, "#140a06", 0.5)
    ys, xs = np.where(mask > 0.5)
    if len(xs) == 0:
        return
    ca, sa = math.cos(ang), math.sin(ang)
    # project to stitch-normal axis
    u = xs * -sa + ys * ca
    umin, umax = u.min(), u.max()
    k = umin
    c = emb.c
    while k <= umax:
        sel = np.abs(u - k) < 0.7
        if sel.sum() >= 2:
            px, py = xs[sel], ys[sel]
            t = px * ca + py * sa
            i0, i1 = t.argmin(), t.argmax()
            p0 = (float(px[i0]), float(py[i0])); p1 = (float(px[i1]), float(py[i1]))
            c.drawLine(*p0, *p1, emb._paint(col, 1.0, width=spacing * 1.25, stroke=True))
            mx, my = (p0[0] * 0.55 + p1[0] * 0.45), (p0[1] * 0.55 + p1[1] * 0.45)
            c.drawLine(p0[0] * 0.8 + mx * 0.2, p0[1] * 0.8 + my * 0.2, mx, my, emb._paint(light, 0.35, width=spacing * 0.5, stroke=True))
            c.drawLine(*p1, p1[0] * 0.85 + mx * 0.15, p1[1] * 0.85 + my * 0.15, emb._paint(dark, 0.3, width=spacing * 0.6, stroke=True))
        k += spacing


def brick_field(W, H, bw=34, bh=12, mortar=2.0, seed=1, x0=0, y0=0):
    """Mask of individual bricks (1 inside a brick, 0 in mortar) in running bond, plus per-brick tone (0..1)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    row = np.floor((yy - y0) / bh)
    off = (row % 2) * bw / 2
    col = np.floor((xx - x0 + off) / bw)
    fx = (xx - x0 + off) - col * bw
    fy = (yy - y0) - row * bh
    m = ((fx > mortar) & (fx < bw - mortar * 0.5) & (fy > mortar) & (fy < bh - mortar * 0.5)).astype(np.float32)
    ids = (row * 997 + col * 131).astype(np.int64) % 4096
    lut = rng.random(4096).astype(np.float32)
    tone = lut[ids]
    return m, tone


def strap_pts(cx, cy, r_in, r_out, wid, ang, tilt=1.0, n=14):
    """Strap petal with a rounded tip, from radius r_in to r_out along ang (ellipse squashed by tilt)."""
    pts = []
    L = (r_out - r_in) / 2
    mx, my = cx + math.cos(ang) * (r_in + L), cy + math.sin(ang) * (r_in + L) * tilt
    for i in range(n):
        t = i / n * math.tau
        u = math.cos(t) * L; v = math.sin(t) * wid * (0.75 + 0.25 * math.cos(t))
        x = mx + u * math.cos(ang) - v * math.sin(ang)
        y = my + (u * math.sin(ang) + v * math.cos(ang)) * tilt
        pts.append((x, y))
    return pts


def chrysanthemum(art, W, H, cx, cy, r, nx, rng, light, mid, deep, centre=None, rot=0.0, tilt=1.0, layers=5):
    """Watercolour decorative chrysanthemum (krisan): dense layers of rounded strap petals, outer ones long and open,
    inner ones short, cupped and darker, building a domed centre."""
    for L in range(layers):
        t = L / max(1, layers - 1)
        n = int(36 - L * 5)
        r_out = r * (1.0 - t * 0.72)
        r_in = r * 0.12 * (1 - t)
        groups = [[], []]
        for k in range(n):
            a = rot + (k + L * 0.37) / n * math.tau + rng.uniform(-0.05, 0.05)
            ro = r_out * rng.uniform(0.82, 1.0)
            wid = r * (0.07 + 0.02 * t) * rng.uniform(0.85, 1.15)
            groups[k % 2].append(strap_pts(cx, cy - r * 0.04 * t, r_in, ro, wid, a, tilt * (1 - 0.15 * t)))
        for gi, g in enumerate(groups):
            pm = shapes(W, H, g)
            art = knockout(art, pm, amount=0.8, grow=0.7)
            c1 = mix_hex(light, mid, t * 0.6 + gi * 0.12); c2 = mix_hex(mid, deep, t * 0.55)
            art = G(art, pm, c1, c2, seed=nx(), density=0.8 + t * 0.1, edge=0.8, bloom=0.25, rough=0.8, feather=0.5, gran=0.25, pad=10)
            base = pm * radial(W, H, cx, cy, r_out * 0.8, sy=tilt)
            art = G(art, base, deep, seed=nx(), density=0.3 + 0.15 * t, edge=0.1, rough=0.8, feather=0.8, pad=10)
    cm = shapes(W, H, [ellipse_pts(cx, cy - r * 0.05, r * 0.12, r * 0.1 * tilt, n=12)])
    art = G(art, cm, centre or deep, seed=nx(), density=0.6, edge=0.6, rough=0.8, feather=0.8, pad=10)
    return art


def brushwork(art, mask, cols, rng, nx, n=300, L=(14, 40), wd=(3, 7), ang=0.0, ang_var=0.25, dir_fn=None, rough=1.4,
              streak=0.9, weight=None):
    """Painterly gouache: many short, tapered, opaque brush dabs inside `mask`, cycling through `cols`.
    dir_fn(x, y) -> angle overrides `ang`; weight (HxW 0..1) biases where dabs land."""
    H, W = mask.shape
    ys, xs = np.where(mask > 0.5)
    if len(xs) == 0:
        return art
    p = None
    if weight is not None:
        p = weight[ys, xs].astype(np.float64) + 1e-6
        p /= p.sum()
    npr = np.random.default_rng(rng.randint(0, 10 ** 6))
    idx = npr.choice(len(xs), size=n, p=p)
    groups = [[] for _ in cols]
    for k, i in enumerate(idx):
        x, y = float(xs[i]), float(ys[i])
        a = (dir_fn(x, y) if dir_fn else ang) + rng.gauss(0, ang_var)
        l = rng.uniform(*L); w = rng.uniform(*wd)
        bend = rng.uniform(-0.15, 0.15) * l
        ca, sa = math.cos(a), math.sin(a)
        pts = [(x - ca * l / 2, y - sa * l / 2), (x - sa * bend, y + ca * bend), (x + ca * l / 2, y + sa * l / 2)]
        groups[k % len(cols)].append((curve(pts, 8), w, (0.3, 0.45)))
    grow = gaussian_filter(mask, 1.2)
    for g, c in zip(groups, cols):
        if not g:
            continue
        sm = strokes(W, H, g) * np.clip(grow * 1.3, 0, 1)
        art = GP(art, sm, c, mix_hex(c, "#000000", 0.08), seed=nx(), rough=rough, streak=streak, pad=10)
    return art
