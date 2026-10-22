"""Agent D1 helpers (bali-gringsing, doyo-benuaq, riau-lancang, flores-sikka).
Builds on _j1_lib (local-crop G/GP/LC/FO/OV, strokes/shapes/circles) and adds a thread-level loom:
  design()      draw a motif at thread resolution (1 px = 1 thread) with wrap-around -> palette index map
  ikat()        warp / weft / double ikat: per-thread dye offsets (blurred stepped edges), dye bleed,
                plain or warp-faced weave, round thread profile, fibre streaks, slubs
  songket()     supplementary gold weft floats over a woven ground (tenun Siak)
  cutout()      a woven texture clipped to a frayed motif mask (transparent RGBA)
Previews -> /tmp/pen/nb-D1/art."""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-D1/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
from _j1_lib import *  # noqa
import _j1_lib
_p1_lib.PREV = "/tmp/pen/nb-D1/art"
_j1_lib.PREV = _p1_lib.PREV
import art as _art
import numpy as np
import skia
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates, gaussian_filter1d

PREV = _p1_lib.PREV


def clear():
    _art._fbm_cache.clear()


def C(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def poly(W, H, pts, smooth=True):
    return shapes(W, H, [pts], smooth=smooth)


def wrap_draw(W, H, draw):
    """Mask (0..1) of draw(canvas, paint) repeated at the 9 wrap offsets (seamless tile)."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            cv.c.save(); cv.c.translate(dx, dy); draw(cv.c, p); cv.c.restore()
    return cv.array()[..., 3]


def plain_draw(W, H, draw):
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    draw(cv.c, p)
    return cv.array()[..., 3]


def path_of(pts, closed=True):
    pa = skia.Path()
    pa.moveTo(*pts[0])
    for q in pts[1:]:
        pa.lineTo(*q)
    if closed:
        pa.close()
    return pa


def stroke_paint(width):
    return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                      StrokeJoin=skia.Paint.kMiter_Join, StrokeCap=skia.Paint.kSquare_Cap)


def layer_index(base, layers):
    """layers: [(mask, index)] painted in order over base index -> int map (threshold 0.5 = tied/untied)."""
    D = np.full(layers[0][0].shape, base, np.int32)
    for m, k in layers:
        D[m > 0.5] = k
    return D


def _thread_offsets(n, length, amp, coh, along, rng, seed):
    """Per-thread dye offsets (threads x length): bundle-coherent constant + slow drift along the thread."""
    base = gaussian_filter1d(rng.normal(0, 1, n), coh, mode="wrap")
    base = base / (np.abs(base).max() + 1e-6) * amp
    jit = rng.normal(0, amp * 0.35, n)
    drift = gaussian_filter(rng.normal(0, 1, (n, length)), (coh * 0.6, along), mode="wrap")
    drift = drift / (np.abs(drift).max() + 1e-6) * amp * 0.6
    return base[:, None] + jit[:, None] + drift


def ikat(D, palette, p=4, mode="double", amp=2.0, coh=2.5, along=14, ground=None, seed=1, bleed=0.55,
         face=0.5, slub=0.25, fibre=0.07, thread_var=0.05, coarse=0.0, tile=True):
    """Render a thread-index design D (Ty x Tx ints into palette) as woven cloth, RGB float (Ty*p x Tx*p x 3).
    mode: 'double' (warp + weft both resist-dyed: gringsing), 'warp' (warp ikat, solid weft: Sikka, doyo).
    face: share of the surface showing warp (0.5 plain weave, ~0.8 warp-faced)."""
    rng = np.random.default_rng(seed)
    Ty, Tx = D.shape
    pal = np.stack([C(c) for c in palette])
    yy = np.arange(Ty); xx = np.arange(Tx)
    # warp threads run vertically (along y); each warp thread x reads the design shifted along y
    ow = _thread_offsets(Tx, Ty, amp, coh, along, rng, seed)            # (Tx, Ty)
    wy = np.round(yy[None, :] + ow).astype(int) % Ty                      # (Tx, Ty)
    warp = pal[D[wy.T, xx[None, :]]]                                      # (Ty, Tx, 3)
    if mode == "double":
        of = _thread_offsets(Ty, Tx, amp, coh, along, rng, seed + 5)     # (Ty, Tx)
        fx = np.round(xx[None, :] + of).astype(int) % Tx
        weft = pal[D[yy[:, None], fx]]
    else:
        weft = np.ones((Ty, Tx, 3), np.float32) * C(ground or palette[0])
    md = "wrap" if tile else "nearest"
    if bleed:  # dye creeps along the thread past the binding
        warp = gaussian_filter(warp, (bleed, 0, 0), mode=md)
        weft = gaussian_filter(weft, (0, bleed, 0), mode=md) if mode == "double" else weft
    # thread-to-thread dye/fibre variation
    warp = warp * (1 + rng.normal(0, thread_var, (1, Tx, 1)))
    weft = weft * (1 + rng.normal(0, thread_var, (Ty, 1, 1)))
    # pixel grid
    H, W = Ty * p, Tx * p
    py = np.arange(H); px = np.arange(W)
    iy = py // p; ix = px // p
    fy = ((py % p) + 0.5) / p; fx_ = ((px % p) + 0.5) / p
    if coarse:  # uneven thread widths (hand-spun fibre): jitter the thread lattice
        jx = gaussian_filter1d(rng.normal(0, coarse * p, W), p * 3, mode="wrap")
        jy = gaussian_filter1d(rng.normal(0, coarse * p, H), p * 3, mode="wrap")
        pxj = (px + jx) % W; pyj = (py + jy) % H
        ix = (pxj // p).astype(int) % Tx; iy = (pyj // p).astype(int) % Ty
        fx_ = ((pxj % p) + 0.5) / (p + 1); fy = ((pyj % p) + 0.5) / (p + 1)
    WC = warp[iy[:, None], ix[None, :]]
    FC = weft[iy[:, None], ix[None, :]]
    # interlacing: which thread is on top
    cell = (ix[None, :] + iy[:, None])
    if face <= 0.5:
        top_warp = (cell % 2) == 0
    else:
        k = max(2, int(round(1 / (1 - face))))
        rows = iy[:, None] % k == 0
        top_warp = ~(rows & ((cell % 2) == 0))
    # thread profiles: round across the thread, slightly darker where it dives under its neighbour
    prof_w = np.sin(np.pi * fx_)[None, :] ** 0.55 * (0.86 + 0.14 * np.sin(np.pi * fy)[:, None] ** 0.4)
    prof_f = np.sin(np.pi * fy)[:, None] ** 0.55 * (0.86 + 0.14 * np.sin(np.pi * fx_)[None, :] ** 0.4)
    lw = 0.66 + 0.40 * prof_w
    lf = 0.62 + 0.40 * prof_f
    # fibre streaks along each thread direction
    nz = np.random.default_rng(seed + 9)
    fw = gaussian_filter(nz.random((H, W)).astype(np.float32), (p * 1.4, 0.45), mode="wrap")
    ff = gaussian_filter(nz.random((H, W)).astype(np.float32), (0.45, p * 1.4), mode="wrap")
    fw = (fw - fw.mean()) / (fw.std() + 1e-6); ff = (ff - ff.mean()) / (ff.std() + 1e-6)
    lw = lw * (1 + fw * fibre)
    lf = lf * (1 + ff * fibre)
    # slubs: thicker/lighter bits of hand-spun yarn
    if slub:
        s1 = gaussian_filter((nz.random((H, W)) > 0.9965).astype(np.float32), (p * 2.2, p * 0.5), mode="wrap")
        s2 = gaussian_filter((nz.random((H, W)) > 0.9965).astype(np.float32), (p * 0.5, p * 2.2), mode="wrap")
        lw = lw * (1 + np.clip(s1 * 40, 0, 1) * slub * 0.5)
        lf = lf * (1 + np.clip(s2 * 40, 0, 1) * slub * 0.5)
    rgb = np.where(top_warp[..., None], WC * lw[..., None], FC * lf[..., None])
    # gentle mottling of the whole cloth (uneven dye bath)
    mot = gaussian_filter(np.random.default_rng(seed + 3).random((H, W)).astype(np.float32), W / 10, mode="wrap")
    mot = (mot - mot.mean()) / (mot.std() + 1e-6)
    rgb = rgb * (1 + mot[..., None] * 0.035)
    return np.clip(rgb, 0, 1).astype(np.float32)


def songket(ground_rgb, gold_mask_thr, p=3, base="#d9b04f", deep="#7a5520", seed=1, float_len=4, tile=True):
    """Lay supplementary metallic weft floats (rows of thread height p) over a woven ground.
    gold_mask_thr: thread-resolution mask (Ty x Tx) where the gold weft floats on the face."""
    rng = np.random.default_rng(seed)
    Ty, Tx = gold_mask_thr.shape
    H, W = Ty * p, Tx * p
    py = np.arange(H); px = np.arange(W)
    iy = py // p; ix = px // p
    fy = ((py % p) + 0.5) / p
    M = gold_mask_thr[iy[:, None], ix[None, :]] > 0.5
    # binding points: every float_len warps, staggered per row
    stag = (iy[:, None] * 2 + rng.integers(0, 1, (H, 1))) % float_len
    bind = ((ix[None, :] + stag) % float_len) == 0
    fxw = ((px % p) + 0.5) / p
    bindp = bind * np.sin(np.pi * fxw)[None, :] ** 0.8
    prof = np.sin(np.pi * fy)[:, None] ** 0.7
    sheen_n = wrap_noise(W, H, seed + 2, W / 8) if tile else fbm(W, H, seed + 2, 120, 2)
    sheen = 0.5 + 0.5 * np.sin(2 * math.pi * (px[None, :] / W * 2 + py[:, None] / H + sheen_n * 1.2))
    lum = 0.40 + 0.52 * prof + 0.30 * sheen * prof ** 2
    lum = lum * (1 - 0.55 * bindp)
    t = np.clip(lum, 0, 1.25)[..., None]
    gold = C(deep) * (1 - np.clip(t, 0, 1)) + C(base) * np.clip(t, 0, 1) + np.clip(t - 1, 0, 1) * 1.4
    spark = gaussian_filter(((rng.random((H, W)) > 0.995) * prof).astype(np.float32), 0.5)
    gold = gold + spark[..., None] * 1.1
    out = np.where(M[..., None], gold, ground_rgb)
    # the gold threads cast a hair of shadow on the ground below them
    sh = np.roll(M, 1, 0) & ~M
    out = out * (1 - 0.25 * sh[..., None])
    return np.clip(out, 0, 1).astype(np.float32)


def fray(mask, seed=1, amount=2.5, scale=6.0, p=4):
    """Woven-edge cutout: staircase edge on the thread lattice + a few loose fibres."""
    h, w = mask.shape
    m = displace(mask, seed, amount, scale)
    # snap to threads (stepped ikat/cloth edge)
    small = m[::p, ::p]
    m2 = np.kron(small, np.ones((p, p), np.float32))[:h, :w]
    m2 = np.pad(m2, ((0, max(0, h - m2.shape[0])), (0, max(0, w - m2.shape[1]))))
    m = np.clip(0.55 * m2 + 0.45 * m, 0, 1)
    return np.clip((m - 0.35) * 3, 0, 1)


def cutout(cloth_rgb, mask, shadow=0.35, seed=1):
    """RGBA of a woven cloth (cloth_rgb, same size as mask) clipped to mask with a soft contact shadow."""
    a = mask
    out = rgba(cloth_rgb, a)
    if shadow:
        sh = np.roll(gaussian_filter(a, 3), 3, 0) * shadow
        out = over(rgba(np.zeros_like(cloth_rgb), sh), out)
    return out


def tile_to(rgb, W, H):
    """Repeat a texture to cover W x H."""
    th, tw = rgb.shape[:2]
    reps = (H // th + 2, W // tw + 2, 1)
    return np.tile(rgb, reps)[:H, :W]


def save_rgb_arr(rgb, path, size=None, quality=80):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)
    print(os.path.basename(path), im.size, os.path.getsize(path) // 1024, "KB")
    return im.size


def prev_rgb(rgb, name):
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{PREV}/{name}.png")


def ygrid(W, H):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return yy, xx


# ------------------------------------------------------------------ scene helpers
from scipy.spatial import cKDTree


def edge_field(W, H, box, cell=14, seed=1, squash=0.7):
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    n = int((x1 - x0) * (y1 - y0) / (cell * cell)) + 4
    pts = np.stack([rng.uniform(x0 - cell, x1 + cell, n), rng.uniform(y0 - cell, y1 + cell, n) / squash], 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d, _ = cKDTree(pts).query(np.stack([xx.ravel(), yy.ravel() / squash], 1), k=2)
    return (d[:, 1] - d[:, 0]).reshape(H, W).astype(np.float32)


def mortar(W, H, box, cell=14, seed=1, squash=0.7, width=1.3):
    """Field-stone wall joints: Voronoi cell borders (0..1 lines) inside box=(x0,y0,x1,y1)."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    n = int((x1 - x0) * (y1 - y0) / (cell * cell)) + 4
    pts = np.stack([rng.uniform(x0 - cell, x1 + cell, n), rng.uniform(y0 - cell, y1 + cell, n) / squash], 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    q = np.stack([xx.ravel(), yy.ravel() / squash], 1)
    d, _ = cKDTree(pts).query(q, k=2)
    edge = (d[:, 1] - d[:, 0]).reshape(H, W)
    return np.clip(1 - edge / width, 0, 1).astype(np.float32)


def stone_shade(W, H, box, cell=14, seed=1, squash=0.7):
    """Per-stone tone (0..1) for tonal variety of field stones."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    n = int((x1 - x0) * (y1 - y0) / (cell * cell)) + 4
    pts = np.stack([rng.uniform(x0 - cell, x1 + cell, n), rng.uniform(y0 - cell, y1 + cell, n) / squash], 1)
    tone = rng.random(n)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    _, i = cKDTree(pts).query(np.stack([xx.ravel(), yy.ravel() / squash], 1))
    return tone[i].reshape(H, W).astype(np.float32)


def thatch_strokes(x0, x1, ytop_fn, ybot_fn, rng, dens=1.0, ln=(10, 22), slant=0.0):
    """Short straw strokes filling a roof (list for strokes())."""
    items = []
    n = int((x1 - x0) * 1.6 * dens)
    for _ in range(n):
        x = rng.uniform(x0, x1)
        yt, yb = ytop_fn(x), ybot_fn(x)
        if yb <= yt:
            continue
        y = rng.uniform(yt, yb)
        L = rng.uniform(*ln)
        a = math.pi / 2 + slant * (x - (x0 + x1) / 2) / max(1, (x1 - x0)) + rng.uniform(-0.12, 0.12)
        items.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], rng.uniform(0.9, 1.8), (0.1, 0.4)))
    return items


def blobs(W, H, centers, rng, r=(10, 22), n=6):
    """Foliage clump: clusters of deformed ellipses."""
    polys = []
    for (cx, cy, s) in centers:
        for _ in range(n):
            rr = rng.uniform(*r) * s
            polys.append(deform(ellipse_pts(cx + rng.uniform(-1, 1) * rr * 1.4, cy + rng.uniform(-1, 1) * rr * 0.8, rr, rr * rng.uniform(0.6, 0.9), 12), rng, 2, 0.12))
    return shapes(W, H, polys)


def vignette_mask(W, H, seed=1, inset=26, rough=18, fade=22):
    """Irregular painted-edge mask for a scene that should end in wet, ragged edges rather than a crop."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum.reduce([xx, W - 1 - xx, yy * 3, H - 1 - yy])
    n = (fbm(W, H, seed, 60, 3) - 0.5) * rough * 2
    return np.clip((d + n - inset) / fade, 0, 1).astype(np.float32)


def woven_cut(D, A, pal, p, seed, shadow=0.28, **k):
    """Render a non-tiling design + its alpha through the same loom (identical dye offsets -> feathered edge)."""
    kw = dict(mode="double", amp=1.5, coh=2.0, along=10, seed=seed, tile=False)
    kw.update(k)
    extra = {kk: kw.pop(kk) for kk in ("bleed", "slub", "fibre", "thread_var") if kk in kw}
    cloth = ikat(D, pal, p=p, bleed=extra.get("bleed", 0.55), slub=extra.get("slub", 0.3), fibre=extra.get("fibre", 0.07), **kw)
    if "ground" in kw:
        kw["ground"] = "#000000"
    am = ikat(A, ["#000000", "#ffffff"], p=p, bleed=0, slub=0, fibre=0, thread_var=0, **kw)[..., 0]
    from scipy.ndimage import grey_closing
    alpha = np.clip((grey_closing(am, size=(p + 1, p + 1)) - 0.2) * 3.0, 0, 1)
    return cutout(cloth, alpha, shadow=shadow)


def ribbon_poly(path, w0, w1):
    """Closed polygon of a tapered ribbon along a path (width w0 -> w1)."""
    n = len(path); L, R = [], []
    for i in range(n):
        a = path[max(0, i - 1)]; b = path[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; d = math.hypot(tx, ty) or 1
        nx_, ny_ = -ty / d, tx / d
        ww = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((path[i][0] + nx_ * ww, path[i][1] + ny_ * ww)); R.append((path[i][0] - nx_ * ww, path[i][1] - ny_ * ww))
    return L + R[::-1]
