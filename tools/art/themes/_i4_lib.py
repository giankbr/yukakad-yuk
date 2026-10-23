"""Agent I4 helpers (bordir-tasik, latte-syari, memphis-80an, gathering-kantor).
Builds on _jw_lib/_j1_lib/_p1_lib (+ art.py) and adds a thread-level embroidery renderer (padded satin, stem stitch,
buttonhole eyelets, woven voile), plus small gouache/print helpers. Previews -> /tmp/pen/nb-I4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *  # noqa
import _jw_lib, _j1_lib, _p1_lib
import art as _art
from scipy.ndimage import distance_transform_edt, gaussian_filter, map_coordinates
PREV = "/tmp/pen/nb-I4/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_jw_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def col_arr(mask, col, alpha):
    rgb = np.ones(mask.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32)
    return np.concatenate([rgb, np.clip(alpha, 0, 1)[..., None]], -1)


def shade(dst, mask, factor):
    out = dst.copy()
    f = 1 + (factor - 1) * mask
    out[..., :3] = np.clip(out[..., :3] * f[..., None], 0, 1)
    return out


def edge_fade(art, px, sides="lrtb"):
    h, w = art.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.full((h, w), 1e6, np.float32)
    if "l" in sides: d = np.minimum(d, xx)
    if "r" in sides: d = np.minimum(d, w - 1 - xx)
    if "t" in sides: d = np.minimum(d, yy)
    if "b" in sides: d = np.minimum(d, h - 1 - yy)
    out = art.copy()
    out[..., 3] *= np.clip(d / px, 0, 1) ** 1.4
    return out


# ───────────────────────── embroidery ─────────────────────────
_LIGHT = np.array([-0.45, -0.65, 0.62], np.float32)
_LIGHT /= np.linalg.norm(_LIGHT)


def _bb(mask, pad):
    ys, xs = np.where(mask > 0.01)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    return max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)


def u_linear(W, H, ang):
    """Stitches run along `ang` (radians); u counts across them."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return xx * -math.sin(ang) + yy * math.cos(ang)


def u_polar(W, H, cx, cy, R):
    """Radial stitches around (cx, cy) (petals, eyelet rings): u = angle * R."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.arctan2(yy - cy, xx - cx) * R


def u_path(W, H, pts, tilt=0.0):
    """Stitches across a path (satin cord / scallop) or slanted along it (stem stitch, tilt ~0.8)."""
    dense = [(p[0], p[1]) for p in along(pts, 0.5)] if len(pts) > 1 else pts
    L = np.zeros((H, W), np.float32); TX = np.zeros((H, W), np.float32); TY = np.zeros((H, W), np.float32)
    path = np.zeros((H, W), bool)
    acc = 0.0
    for i, (x, y) in enumerate(dense):
        if i:
            acc += math.hypot(x - dense[i - 1][0], y - dense[i - 1][1])
        j = min(i + 1, len(dense) - 1); k = max(i - 1, 0)
        tx, ty = dense[j][0] - dense[k][0], dense[j][1] - dense[k][1]
        n = math.hypot(tx, ty) + 1e-6
        ix, iy = int(round(x)), int(round(y))
        if 0 <= ix < W and 0 <= iy < H:
            path[iy, ix] = True; L[iy, ix] = acc; TX[iy, ix] = tx / n; TY[iy, ix] = ty / n
    _, (iy, ix) = distance_transform_edt(~path, return_indices=True)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = L[iy, ix]
    if tilt:
        across = (xx - ix) * -TY[iy, ix] + (yy - iy) * TX[iy, ix]
        u = u + across * tilt
    return u


def stitch(dst, mask, u, thread="#fbfaf3", gap="#8fa58a", spacing=2.4, pad=1.0, sheen=0.55, seed=1, cast=0.38,
           cast_col="#2f4632", wobble=0.8, raise_=3.5):
    """Padded satin embroidery over dst. mask = stitched region, u = across-stitch coordinate field (px)."""
    b = _bb(mask, 8)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = np.ascontiguousarray(mask[y0:y1, x0:x1]); uu = u[y0:y1, x0:x1]
    h, w = m.shape
    rng = np.random.default_rng(seed)
    if wobble:
        m = displace(m, seed, wobble, 10)
    # stitch rows with tiny irregular spacing
    nz = gaussian_filter(rng.random((h, w)).astype(np.float32), 5)
    nz = (nz - nz.mean()) / (nz.std() + 1e-6)
    nz2 = gaussian_filter(rng.random((h, w)).astype(np.float32), 1.6)
    nz2 = (nz2 - nz2.mean()) / (nz2.std() + 1e-6)
    t = uu / spacing + nz * 0.22 + nz2 * 0.06
    idx = np.floor(t)
    f = t - idx
    prof = np.sqrt(np.clip(1 - (2 * f - 1) ** 2, 0, 1))
    # per-stitch tone (hash of index)
    hsh = (np.sin(idx * 12.9898 + seed * 3.1) * 43758.5453) % 1.0
    # padding dome from distance to the edge
    d = distance_transform_edt(m > 0.5).astype(np.float32)
    dome = 1 - np.exp(-d / raise_)
    hgt = dome * pad * 4.0 + prof * 0.9
    hgt = gaussian_filter(hgt, 0.6)
    gy, gx = np.gradient(hgt)
    n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    lam = np.clip(n @ _LIGHT, 0, 1)
    # thread twist striations along each stitch
    tw = fbm(w, h, seed + 5, 3, 2)
    spec = (prof ** 8) * sheen * (0.55 + 0.45 * tw)
    tc = np.array(hex_rgb(thread), np.float32); gc = np.array(hex_rgb(gap), np.float32)
    k = (0.55 + 0.42 * lam + (hsh - 0.5) * 0.06)[..., None]
    rgb = tc * k + spec[..., None] * 0.35
    g = np.clip(0.5 + 0.5 * prof, 0, 1)[..., None]
    rgb = gc * (1 - g) + rgb * g
    # thin ridge where stitches end (outline) catches light / shadow
    edge = np.clip(gaussian_filter(m, 0.8) - gaussian_filter(m, 2.2), 0, 1)
    rgb = rgb * (1 - 0.18 * edge[..., None])
    alpha = np.clip(m * (0.9 + 0.1 * prof), 0, 1)
    src = np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], -1)
    out = dst.copy()
    region = out[y0:y1, x0:x1]
    if cast:
        sh = np.roll(np.roll(gaussian_filter(m, 1.6), 2, 0), 1, 1) * cast
        region = over(region, col_arr(sh, cast_col, sh))
    out[y0:y1, x0:x1] = over(region, src)
    return out


def ring_mask(W, H, cx, cy, r0, r1, sx=1.0):
    def draw(cv):
        cv.c.save(); cv.c.translate(cx, cy); cv.c.scale(sx, 1)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=r1 - r0)
        cv.c.drawCircle(0, 0, (r0 + r1) / 2, p); cv.c.restore()
    return mask_from(W, H, draw)


def disc(W, H, cx, cy, r, sx=1.0):
    def draw(cv):
        cv.c.save(); cv.c.translate(cx, cy); cv.c.scale(sx, 1)
        cv.c.drawCircle(0, 0, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)); cv.c.restore()
    return mask_from(W, H, draw)


def eyelet(dst, W, H, cx, cy, r, ring=None, thread="#fbfaf3", gap="#8fa58a", hole=None, hole_alpha=1.0, seed=1,
           sx=1.0, cut=True):
    """Buttonhole-stitched eyelet: a cut hole (transparent, or filled with `hole` colour) ringed by radial satin."""
    ring = ring or max(2.5, r * 0.45)
    hm = disc(W, H, cx, cy, r, sx)
    out = dst
    if cut:
        out = out.copy()
        out[..., 3] *= 1 - hm
    if hole:
        depth = np.clip(np.roll(hm, -2, 0) - hm * 0, 0, 1)
        out = over(out, col_arr(hm, hole, hm * hole_alpha))
        # inner shadow at the top rim (thickness of the fabric)
        rim = np.clip(hm - np.roll(hm, 3, 0), 0, 1)
        out = over(out, col_arr(rim, "#2f4632", gaussian_filter(rim, 1.2) * 0.35))
    rm = ring_mask(W, H, cx, cy, r - 0.5, r + ring, sx)
    out = stitch(out, rm, u_polar(W, H, cx, cy, r + ring / 2), thread, gap, spacing=2.1, pad=0.7, seed=seed, raise_=2.0)
    return out


def satin_leaf(dst, W, H, base, tip, width, thread, gap, seed=1, bend=0.0, split=True, cast=0.38, spacing=2.4):
    """Leaf in two satin halves angled toward a central vein (fishbone-like)."""
    bx, by = base; tx, ty = tip
    ang = math.atan2(ty - by, tx - bx)
    L = math.hypot(tx - bx, ty - by)
    pts = petal_pts(bx, by, L, width, ang, n=16)
    if bend:
        pts = [(x + math.sin(i / len(pts) * math.pi) * bend * -math.sin(ang), y + math.sin(i / len(pts) * math.pi) * bend * math.cos(ang)) for i, (x, y) in enumerate(pts)]
    m = shape_mask(W, H, pts)
    if not split:
        return stitch(dst, m, u_linear(W, H, ang + math.pi / 2), thread, gap, seed=seed, cast=cast, spacing=spacing)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = ((xx - bx) * math.sin(ang) - (yy - by) * math.cos(ang)) > 0
    a1 = gaussian_filter((m * side).astype(np.float32), 0.4)
    a2 = gaussian_filter((m * ~side).astype(np.float32), 0.4)
    out = stitch(dst, a1, u_linear(W, H, ang + 0.75), thread, gap, seed=seed, cast=cast, spacing=spacing)
    out = stitch(out, a2, u_linear(W, H, ang - 0.75), thread, gap, seed=seed + 1, cast=cast, spacing=spacing)
    return out


def satin_petal_flower(dst, W, H, cx, cy, r, n, thread, gap, seed=1, rot=0.0, center=None, eyelet_hole=None, cast=0.38,
                       petal_w=0.62):
    """Flower of n padded satin petals with radial stitches and a cut eyelet centre."""
    out = dst
    uf = u_polar(W, H, cx, cy, r * 0.6)
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        pm = shape_mask(W, H, petal_pts(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12, r * 0.9, r * petal_w, a, n=16, cup=0.15))
        out = stitch(out, pm, uf, thread, gap, seed=seed + i * 7, cast=cast, spacing=2.2, raise_=r * 0.12)
    if center is not None or eyelet_hole is not None:
        out = eyelet(out, W, H, cx, cy, r * 0.2, r * 0.13, thread, gap, hole=eyelet_hole, seed=seed + 3, cut=eyelet_hole is None)
    return out


def stem(dst, W, H, pts, width, thread, gap, seed=1, tilt=0.9, cast=0.3):
    m = strokes(W, H, [(pts, width, (0.05, 0.12))])
    return stitch(dst, m, u_path(W, H, pts, tilt), thread, gap, spacing=2.6, pad=0.6, seed=seed, cast=cast, raise_=1.6)


def satin_dot(dst, W, H, x, y, r, thread, gap, seed=1, ang=0.4):
    m = disc(W, H, x, y, r)
    return stitch(dst, m, u_linear(W, H, ang), thread, gap, spacing=1.9, pad=1.0, seed=seed, raise_=r * 0.6, cast=0.3)


def weave(W, H, tone="#fbfaf5", period=2.4, seed=1, contrast=0.04, wrap=True):
    """Plain-weave cotton voile (opaque RGB array): crossing warp/weft threads with slub irregularity."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if wrap:
        px = W / round(W / period); py = H / round(H / period)
    else:
        px = py = period
    rng = np.random.default_rng(seed)
    ns = lambda s: (wrap_noise(W, H, rng.integers(1e6), s) if wrap else fbm(W, H, int(rng.integers(1e6)), s * 8, 3))
    jx = (ns(3) - 0.5) * 0.5; jy = (ns(3) - 0.5) * 0.5
    wx = 0.5 + 0.5 * np.cos(2 * np.pi * (xx / px + jy))
    wy = 0.5 + 0.5 * np.cos(2 * np.pi * (yy / py + jx))
    checker = ((np.floor(xx / px) + np.floor(yy / py)) % 2).astype(np.float32)
    top = checker * wx + (1 - checker) * wy
    slub_x = ns(14); slub_y = ns(14)
    v = 1 - contrast + contrast * (0.55 * top + 0.25 * slub_x + 0.2 * slub_y)
    base = np.array(hex_rgb(tone), np.float32)
    rgb = base * v[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def wrap_noise(w, h, seed, sigma):
    n = gaussian_filter(np.random.default_rng(int(seed)).random((h, w)).astype(np.float32), sigma, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)


def save(arr, path, max_w=None, quality=82):
    size = save_asset(arr, path, max_w=max_w, quality=quality)
    print(os.path.basename(path), size, os.path.getsize(path) // 1024, "KB")
    return size


def save_full(arr, path, size=None, quality=80, rgb=False):
    im = to_image(arr)
    if rgb:
        im = im.convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size


def prev(arr, name, bg="#dfe9d6"):
    h, w = arr.shape[:2]
    base = np.ones((h, w, 3), np.float32) * np.array(hex_rgb(bg), np.float32)
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def round_petal(cx, cy, L, Wd, ang, n=24, notch=0.0):
    """Rounded petal from a narrow base at (cx, cy) to a broad round tip (optional notch at the tip)."""
    side = []
    for i in range(n + 1):
        t = i / n
        x = L * t
        w = Wd * (t ** 0.55) * (1 - t ** 4) ** 0.5
        side.append((x, w))
    pts = [(x, -w) for x, w in side] + [(x, w) for x, w in reversed(side)]
    if notch:
        pts = [(x - (notch * L * max(0, 1 - abs(y) / (Wd * 0.4)) if x > L * 0.9 else 0), y) for x, y in pts]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def flower(dst, W, H, cx, cy, r, n, thread, gap, seed=1, rot=0.0, hole=None, cut=False, cast=0.38, petal_w=0.6, notch=0.1,
           centre=True):
    out = dst
    uf = u_polar(W, H, cx, cy, r * 0.6)
    order = sorted(range(n), key=lambda i: math.sin(rot + i * 2 * math.pi / n))
    for i in order:
        a = rot + i * 2 * math.pi / n
        pm = shape_mask(W, H, round_petal(cx + math.cos(a) * r * 0.1, cy + math.sin(a) * r * 0.1, r * 0.95, r * petal_w, a, notch=notch))
        out = stitch(out, pm, uf, thread, gap, seed=seed + i * 7, cast=cast, spacing=2.2, raise_=max(2.0, r * 0.1))
    if centre:
        out = eyelet(out, W, H, cx, cy, r * 0.19, max(2.2, r * 0.12), thread, gap, hole=hole, seed=seed + 3, cut=cut)
    return out


def cutwork(dst, W, H, cx, cy, L, wd, ang, thread, gap, hole, seed=1, band=4.5):
    """Kerancang cut-out: a teardrop opening (lining shows) edged with buttonhole satin."""
    bx, by = cx - math.cos(ang) * L / 2, cy - math.sin(ang) * L / 2
    outer = shape_mask(W, H, round_petal(bx - math.cos(ang) * band, by - math.sin(ang) * band, L + band * 2, wd + band, ang))
    inner = shape_mask(W, H, round_petal(bx, by, L, wd, ang))
    out = over(dst, col_arr(inner, hole, inner))
    rim = np.clip(inner - np.roll(inner, 3, 0), 0, 1)
    out = over(out, col_arr(rim, "#2f4632", gaussian_filter(rim, 1.2) * 0.3))
    ring = np.clip(outer - inner, 0, 1)
    return stitch(out, ring, u_polar(W, H, cx, cy, L * 0.45), thread, gap, spacing=2.0, pad=0.7, seed=seed, raise_=1.8)


def vine(dst, W, H, pts, rng, seed, th=("#fdfcf6", "#bccab3"), lf=("#d2e4c2", "#8ea782"), every=22, Lf=30, flowers=(),
         fr=24, hole="#d5e5c6", stem_w=3.6, side_bias=0.0):
    """Stem-stitched vine with leaves alternately attached along it; flowers at given fractions."""
    out = stem(dst, W, H, pts, stem_w, lf[0], lf[1], seed=seed)
    dense = along(pts, every)
    for i, (x, y, a) in enumerate(dense[:-1]):
        sd = 1 if i % 2 else -1
        la = a + sd * (0.85 + rng.uniform(-0.15, 0.15)) + side_bias
        L = Lf * rng.uniform(0.8, 1.1)
        c = lf if (i % 3) else th
        out = satin_leaf(out, W, H, (x, y), (x + math.cos(la) * L, y + math.sin(la) * L), L * 0.38, *c, seed=seed + 10 + i,
                         bend=sd * L * 0.1)
    n = len(pts)
    for k, f in enumerate(flowers):
        x, y = pts[min(n - 1, int(f * (n - 1)))]
        out = flower(out, W, H, x, y, fr * (1.0 if k % 2 == 0 else 0.8), 5, th[0], th[1], seed=seed + 200 + k, rot=rng.uniform(0, 6), hole=hole)
    return out
