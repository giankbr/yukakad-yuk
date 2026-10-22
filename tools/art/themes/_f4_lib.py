"""Agent F4 helpers (abstrak-sapuan, kota-tua-batavia, balkon-paris, lemon-amalfi).
Adds: flat acrylic brush sweeps + palette-knife blocks on top of the D5 impasto canvas, pen-and-wash ink helpers,
majolica/gouache helpers. Previews -> /tmp/pen/nb-F4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *  # noqa  (Impasto, fill, vgrad, soft, ragged, kb, rect_m, ...; _jw_lib/_j1_lib/_p1_lib/art)
import _d5_lib, _p1_lib
import art as _art

PREV = "/tmp/pen/nb-F4/art"
os.makedirs(PREV, exist_ok=True)


def preview(arr, name, tone="#fbf6ee", bg=None):
    _p1_lib.PREV = PREV
    return _p1_lib.preview(arr, name, tone=tone, bg=bg)


def rgb(c):
    return list(hex_rgb(c)) if isinstance(c, str) else list(c)


def _normals(pts):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        out.append((-dy / d, dx / d))
    return out


def _blit(P, x0, y0, rgba, hgt):
    """Draw a local RGBA float patch into the colour canvas and its height (grey, same alpha) into the height map."""
    a = np.clip(rgba, 0, 1)
    img = skia.Image.fromarray((a * 255).astype(np.uint8), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    P.col.c.drawImage(img, x0, y0)
    hh = np.concatenate([np.repeat(np.clip(hgt, 0, 1)[..., None], 3, -1), a[..., 3:4]], -1)
    img = skia.Image.fromarray((hh * 255).astype(np.uint8), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    P.hgt.c.drawImage(img, x0, y0)


def _noise1(n, seed, sigma):
    v = gaussian_filter(np.random.default_rng(seed).random(n).astype(np.float32), sigma)
    return (v - v.min()) / (v.max() - v.min() + 1e-6)


def sweep(P, pts, width, col, seed=1, dry=0.45, hv=0.55, streak=0.12, col2=None, alpha=1.0, swell=0.25, taper0=0.06,
          rough=1.0, hvar=0.18):
    """Wide flat-brush sweep along `pts`: per-pixel stroke coords (u along, v across) drive bristle streaks, a colour
    drag from col to col2 across the brush, ragged edges and a broken dry-brush tail; ridges go into the height map."""
    from scipy.spatial import cKDTree
    rng = random.Random(seed)
    pts = np.array(curve(pts, max(60, len(pts))) if len(pts) < 40 else pts, np.float32)
    seg = np.diff(pts, axis=0); sl = np.hypot(seg[:, 0], seg[:, 1]); cum = np.concatenate([[0], np.cumsum(sl)])
    Ltot = cum[-1]
    # resample densely
    m = max(80, int(Ltot / 1.5))
    s = np.linspace(0, Ltot, m)
    pts = np.stack([np.interp(s, cum, pts[:, 0]), np.interp(s, cum, pts[:, 1])], -1)
    d = np.gradient(pts, axis=0); d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-6)[:, None]
    nrm = np.stack([-d[:, 1], d[:, 0]], -1)
    pad = width * (1 + swell) * 0.7 + 6
    x0 = int(max(0, pts[:, 0].min() - pad)); x1 = int(min(P.W, pts[:, 0].max() + pad))
    y0 = int(max(0, pts[:, 1].min() - pad)); y1 = int(min(P.H, pts[:, 1].max() + pad))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    tree = cKDTree(pts)
    dist, idx = tree.query(np.stack([xx.ravel(), yy.ravel()], -1))
    idx = idx.reshape(xx.shape)
    u = idx / (m - 1)
    rel = np.stack([xx - pts[idx, 0], yy - pts[idx, 1]], -1)
    vv = (rel * nrm[idx]).sum(-1)
    prof = np.minimum(1, u / taper0) ** 0.5 * (1 + swell * np.sin(np.pi * u)) * (1 - 0.3 * np.clip((u - 0.8) / 0.2, 0, 1))
    hw = width / 2 * prof
    h_, w_ = xx.shape
    # ragged edge
    edge_n = (fbm(w_, h_, seed + 1, 22, 2) - 0.5) * 2 * rough + (fbm(w_, h_, seed + 7, 6, 1) - 0.5) * 0.5 * rough
    v = vv / np.maximum(hw, 1e-3)
    inside = np.clip((1 - np.abs(v) + edge_n * 0.06) * hw / 1.2, 0, 1)
    # bristles: 1D noise across the brush
    nb = 512
    vi = np.clip(((v + 1) / 2 * (nb - 1)).astype(int), 0, nb - 1)
    br = _noise1(nb, seed + 2, 1.2)            # fine bristle tone
    br2 = _noise1(nb, seed + 3, 6)             # paint load per bristle group
    blen = 1 - dry * (_noise1(nb, seed + 4, 2.0) ** 0.8) * (0.55 + 0.45 * np.abs(np.linspace(-1, 1, nb)))
    # dry-brush: alpha falls off past each bristle's length, broken into dashes
    dash = fbm(w_, h_, seed + 5, 5, 2)
    ul = blen[vi]
    tail = np.clip((ul - u) / 0.06, 0, 1)
    dryness = np.clip((u - (ul - dry * 0.35)) / (dry * 0.35 + 1e-3), 0, 1)
    cover = tail * (1 - dryness * np.clip((dash - 0.35 + 0.4 * br[vi]) * 2.2, 0, 1))
    cover *= 0.82 + 0.18 * br2[vi]
    a = np.clip(inside * cover, 0, 1) * alpha
    c1 = np.array(rgb(col), np.float32); c2 = np.array(rgb(col2 or col), np.float32)
    k = np.clip(0.5 + 0.38 * v + (br2[vi] - 0.5) * 0.7 + (fbm(w_, h_, seed + 6, 40, 2) - 0.5) * 0.4, 0, 1)[..., None]
    c = c1 * (1 - k) + c2 * k
    tone = 1 + (br[vi] - 0.5) * 2 * streak
    c = np.clip(c * tone[..., None] + (tone[..., None] - 1) * 0.15, 0, 1)
    hgt = hv + (br[vi] - 0.5) * 2 * hvar - dryness * 0.15
    pile = np.exp(-((u - (ul - 0.04)) / 0.03) ** 2) * 0.18
    hgt = np.clip(hgt + pile * inside, 0, 1)
    _blit(P, x0, y0, np.concatenate([c, a[..., None]], -1), hgt)


def knife(P, quad, col, seed=1, drag=0.0, hv=0.6, col2=None, scrape=0.35, ridges=14, alpha=1.0, skip=0.25):
    """Palette-knife plane: flat paint with fine drag streaks along `drag`, skips where the colour beneath shows,
    a raised ridge where the knife lifted (trailing edge) and a thinner leading edge."""
    rng = random.Random(seed)
    pts = deform(quad, rng, 3, 0.012)
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    x0 = int(max(0, min(xs) - 8)); x1 = int(min(P.W, max(xs) + 8)); y0 = int(max(0, min(ys) - 8)); y1 = int(min(P.H, max(ys) + 8))
    w_, h_ = x1 - x0, y1 - y0
    if w_ <= 2 or h_ <= 2:
        return
    msk = shape_mask(w_, h_, [(x - x0, y - y0) for x, y in pts], smooth=False)
    msk = np.clip((displace(msk, seed, 1.2, 30) - 0.3) * 2.4, 0, 1)
    yy, xx = np.mgrid[0:h_, 0:w_].astype(np.float32)
    ca, sa = math.cos(drag), math.sin(drag)
    sc = xx * ca + yy * sa                       # along drag
    pc = -xx * sa + yy * ca                      # across
    smin, smax = sc[msk > .5].min() if (msk > .5).any() else 0, sc[msk > .5].max() if (msk > .5).any() else 1
    su = np.clip((sc - smin) / max(1, smax - smin), 0, 1)
    n = int(pc.max() - pc.min()) + 4
    pi = np.clip((pc - pc.min()).astype(int), 0, n - 1)
    st = _noise1(n, seed + 1, 0.9); st2 = _noise1(n, seed + 2, 5)
    c1 = np.array(rgb(col), np.float32); c2 = np.array(rgb(col2 or col), np.float32)
    k = np.clip(st2[pi] * 0.8 + (fbm(w_, h_, seed + 3, 30, 2) - .5) * .6 + su * 0.15, 0, 1)[..., None]
    c = c1 * (1 - k) + c2 * k
    c = np.clip(c * (1 + (st[pi] - .5)[..., None] * 0.12), 0, 1)
    # skips: thin paint near the leading edge + random scrapes
    hn = (fbm(w_, h_, seed + 4, 14, 2) * 0.5 + _noise1(n, seed + 9, 1.5)[pi] * 0.5)
    holes = np.clip((hn - (1 - skip * (1 - su) * 1.3)) * 4, 0, 1)
    scr = np.zeros(n, np.float32)
    for _ in range(int(ridges * scrape)):
        j = rng.randint(0, n - 3); scr[j:j + rng.randint(1, 3)] = rng.uniform(.5, 1)
    scrape_m = scr[pi] * (su > rng.uniform(.1, .5))
    a = msk * (1 - holes * 0.85) * (1 - scrape_m * 0.6) * alpha
    rim = np.clip(msk - gaussian_filter(msk, 2.0), 0, 1) * 2
    trail = np.exp(-((su - 1) / 0.05) ** 2)
    hgt = hv + (st[pi] - .5) * 0.12 + rim * 0.25 + trail * 0.22 * msk - holes * 0.2
    _blit(P, x0, y0, np.concatenate([c, a[..., None]], -1), np.clip(hgt, 0, 1))


def oilstick(P, pts, width, col, seed=1, hv=0.7, skip=0.25):
    """Oil-stick / charcoal scribble line: broken, waxy, slightly raised."""
    rng = random.Random(seed)
    c = rgb(col)
    for i in range(len(pts) - 1):
        if rng.random() < skip * 0.3:
            continue
        w = width * rng.uniform(0.6, 1.2)
        pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap,
                        Color4f=skia.Color4f(*c, rng.uniform(.6, .95)))
        P.col.c.drawLine(*pts[i], *pts[i + 1], pp)
        pp.setColor4f(skia.Color4f(hv, hv, hv, 1))
        P.hgt.c.drawLine(*pts[i], *pts[i + 1], pp)


def ink(arr, pts_list, col="#3a2a20", width=1.6, seed=1, jitter=0.35, alpha=0.9, dry=0.0, taper=True):
    """Pen line(s) drawn onto an RGBA float array (over), via ink_line on a temp canvas."""
    h, w = arr.shape[:2]
    cv = Canvas(w, h, seed)
    for pts in pts_list:
        ink_line(cv, pts, col, width=width, alpha=alpha, jitter=jitter, taper=taper, dry=dry)
    return over(arr, cv.array())


def lines(w, h, segs, width, cap=True):
    """Mask of straight segments [(x0,y0,x1,y1)]."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                   StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
    for x0, y0, x1, y1 in segs:
        cv.c.drawLine(x0, y0, x1, y1, p)
    return cv.array()[..., 3]


def rects(w, h, items, r=0):
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for x0, y0, x1, y1 in items:
        if r:
            cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, p)
        else:
            cv.c.drawRect(skia.Rect(x0, y0, x1, y1), p)
    return cv.array()[..., 3]


def arches(w, h, items):
    """Round-topped windows [(x0, y0, x1, y1)] (semicircle top)."""
    cv = Canvas(w, h)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for x0, y0, x1, y1 in items:
        r = (x1 - x0) / 2
        path = skia.Path()
        path.moveTo(x0, y1); path.lineTo(x0, y0 + r)
        path.arcTo(skia.Rect(x0, y0, x1, y0 + 2 * r), 180, 180, False)
        path.lineTo(x1, y1); path.close()
        cv.c.drawPath(path, p)
    return cv.array()[..., 3]


def deckle(arr, seed=1, amt=5, scale=10, inset=6):
    """Torn/deckled paper edge on an opaque RGBA rectangle."""
    h, w = arr.shape[:2]
    m = rect_m(w, h, inset, inset, w - inset, h - inset)
    m = np.clip((displace(m, seed, amt, scale) - 0.3) * 2.5, 0, 1)
    out = arr.copy()
    out[..., 3] *= m
    return out


def paper_arr(w, h, tone, seed=3, fiber=0.6, mottle=0.8):
    im = paper(w, h, tone, seed, fiber, mottle)
    a = np.asarray(im, np.float32) / 255
    return np.concatenate([a, np.ones((h, w, 1), np.float32)], -1)


def wash(dst, mask, col, col2=None, seed=1, density=0.7, **k):
    """Shortcut: local watercolour glaze."""
    return G(dst, mask, col, col2, seed=seed, density=density, **k)
