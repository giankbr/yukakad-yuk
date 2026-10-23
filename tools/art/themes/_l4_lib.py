"""Agent L4 helpers (bangka-cual, mozaik-umayyah, kabin-danau, dies-natalis): _j1_lib (bbox-cropped painting) plus
seamless-tile drawing, songket thread floats, a glass-tessera mosaic renderer and small scene helpers.
Previews -> /tmp/pen/nb-L4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _j1_lib import *  # noqa
import art as _art
from _jw_lib import along

PREV = "/tmp/pen/nb-L4/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def prev(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.preview(arr, name, tone=tone, bg=bg)


def wrapped(W, H, draw_one, items):
    """Draw each item at its position and the 8 wrapped copies so the mask tiles seamlessly.
    draw_one(canvas, x, y, item)."""
    cv = Canvas(W, H)
    for it in items:
        x, y = it[0], it[1]
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):
                draw_one(cv, x + dx, y + dy, it)
    return cv.array()[..., 3]


def floats(W, H, period=3.0, duty=0.62, seed=1, wob=0.6, vertical=False):
    """Woven thread floats: parallel lines (horizontal weft by default) with per-thread brightness drift.
    Returns (line mask 0..1, per-thread tone 0..1). Seamless when H (or W) is a multiple of period."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx if vertical else yy) / period
    v = xx if not vertical else yy
    f = np.abs((u % 1.0) - 0.5) * 2
    line = np.clip((duty - f) / 0.25 + 0.5, 0, 1)
    rng = np.random.default_rng(seed)
    n = int(np.ceil((W if vertical else H) / period)) + 1
    tone = rng.random(n).astype(np.float32)
    idx = np.floor(u).astype(int) % n
    t = tone[idx]
    # slub: slow variation along the thread
    t = t * 0.6 + 0.4 * (0.5 + 0.5 * np.sin(v / (23 + 7 * tone[idx]) + tone[idx] * 9))
    return line.astype(np.float32), t.astype(np.float32)


def rect_poly(cx, cy, w, h, ang, rng, jit):
    c, s_ = math.cos(ang), math.sin(ang)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x = sx * w / 2 + rng.uniform(-jit, jit); y = sy * h / 2 + rng.uniform(-jit, jit)
        pts.append((cx + x * c - y * s_, cy + x * s_ + y * c))
    return pts


def mosaic(design, W, H, cell=10, seed=1, gold=None, gold_cols=("#d9b45a", "#c99a3e", "#e8c978", "#b88a33"),
           contours=(), grout="#3a2d1c", gap=1.6, alpha=None, var=0.07, emboss=0.5, sizes=None):
    """Glass-tessera mosaic.
    design: (H,W,3) float RGB design to sample colours from; gold: (H,W) mask where tesserae are gold glass;
    contours: list of (polyline, hex colour, cell scale) laid first as tiles following the outline (andamento);
    alpha: (H,W) coverage mask (tiles only where > .5); sizes: optional (H,W) cell-scale field.
    Returns RGBA float."""
    rng = random.Random(seed)
    cv = Canvas(W, H, seed)
    occ = np.zeros((H, W), bool)
    paint = skia.Paint(AntiAlias=True)
    tiles = []

    def put(pts, col):
        paint.setColor(skia.Color4f(float(col[0]), float(col[1]), float(col[2]), 1.0))
        cv.c.drawPath(poly_path(pts), paint)

    def vary(rgb, amt):
        k = 1 + rng.uniform(-amt, amt)
        return np.clip(np.array(rgb) * k + np.array([rng.uniform(-.02, .02) for _ in range(3)]), 0, 1)

    gcols = [np.array(hex_rgb(c), np.float32) for c in gold_cols]
    for poly, col, sc in contours:
        cs = cell * sc
        base = np.array(hex_rgb(col), np.float32) if col not in (None, "gold") else None
        for x, y, a in along(poly, cs):
            if not (0 <= x < W and 0 <= y < H):
                continue
            iy, ix = int(y), int(x)
            if occ[iy, ix] or (alpha is not None and alpha[iy, ix] < .5):
                continue
            if col == "gold":
                if gold is not None and gold[iy, ix] < .5:
                    continue
                c = vary(gcols[rng.randrange(len(gcols))], .16)
            elif col is None:
                c = vary(design[iy, ix], var)
            else:
                c = vary(base, var)
            put(rect_poly(x, y, cs - gap, cs * rng.uniform(.8, 1.0) - gap, a + rng.uniform(-.12, .12), rng, cs * .1), c)
            r = int(cs * .42)
            occ[max(0, int(y) - r):int(y) + r + 1, max(0, int(x) - r):int(x) + r + 1] = True
    y = cell / 2
    row = 0
    while y < H + cell:
        x = rng.uniform(0, cell) + (cell / 2 if row % 2 else 0) - cell
        while x < W + cell:
            sc = 1.0 if sizes is None else float(sizes[int(min(H - 1, max(0, y))), int(min(W - 1, max(0, x)))])
            cs = cell * sc
            cx, cy = x + rng.uniform(-cs * .08, cs * .08), y + rng.uniform(-cs * .08, cs * .08)
            ix, iy = int(min(W - 1, max(0, cx))), int(min(H - 1, max(0, cy)))
            x += cs * rng.uniform(.96, 1.06)
            if occ[iy, ix] or (alpha is not None and alpha[iy, ix] < .5):
                continue
            if gold is not None and gold[iy, ix] > .5:
                g = gcols[rng.randrange(len(gcols))]
                col = vary(g, .16)
                if rng.random() < .04:
                    col = np.clip(col * 1.25, 0, 1)
            else:
                col = vary(design[iy, ix], var)
            put(rect_poly(cx, cy, cs - gap, cs * rng.uniform(.86, 1.0) - gap, rng.uniform(-.1, .1), rng, cs * .1), col)
        y += cell * rng.uniform(.97, 1.03)
        row += 1
    a = cv.array()
    m = a[..., 3]
    rgb = a[..., :3]
    # bevel: light from the top-left on each tessera, darker rims
    bl = gaussian_filter(m, 1.2)
    gy, gx = np.gradient(bl)
    shade = np.clip(1 + (-(gx + gy)) * 2.2 * emboss, .7, 1.35)
    rim = np.clip(m - gaussian_filter(m, 1.0), 0, 1)
    rgb = rgb * shade[..., None] * (1 - rim[..., None] * .25)
    # glass grain
    g = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), .8)
    g = (g - g.mean()) / (g.std() + 1e-6)
    rgb = np.clip(rgb * (1 + g[..., None] * .03), 0, 1)
    gr = np.array(hex_rgb(grout), np.float32)
    gn = fbm(W, H, seed + 5, 30, 3)[..., None]
    grout_rgb = gr * (0.85 + 0.3 * gn)
    out_rgb = rgb * m[..., None] + grout_rgb * (1 - m[..., None])
    if alpha is None:
        A = np.ones((H, W), np.float32)
    else:
        A = np.clip(gaussian_filter((alpha > .5).astype(np.float32), 1.5) * 1.6 - .1, 0, 1)
        A = np.maximum(A * (0.55 + 0.45 * np.clip(gaussian_filter(m, 2) * 1.5, 0, 1)), m)
    return np.concatenate([np.clip(out_rgb, 0, 1), A[..., None]], -1)


def paint_flat(design, mask, col):
    """Paint a flat colour into an RGB design array where mask > .5 (for mosaic sampling)."""
    c = np.array(hex_rgb(col), np.float32)
    sel = mask > .5
    design[sel] = c
    return design


def pine_polys(x, by, h, rng, lean=0.0, tiers=None):
    """Spruce silhouette as stacked jagged tiers (polygons)."""
    tiers = tiers or max(4, int(h / 22))
    polys = []
    w = h * 0.36
    for i in range(tiers):
        t0 = i / tiers
        top = by - h * (1 - t0 * 0.92)
        bot = by - h * (1 - (i + 1.6) / tiers * 0.92)
        bot = min(bot, by)
        ww = w * (0.25 + 0.75 * ((i + 1) / tiers)) * rng.uniform(.88, 1.1)
        cx = x + lean * (by - top)
        polys.append([(cx, top), (cx + ww * .5 + rng.uniform(-2, 2), bot), (cx + ww * .15, bot - rng.uniform(1, 4)),
                      (cx - ww * .15, bot - rng.uniform(1, 4)), (cx - ww * .5 + rng.uniform(-2, 2), bot)])
    polys.append([(x - h * .02, by - h * .2), (x + h * .02, by - h * .2), (x + h * .025, by + 2), (x - h * .025, by + 2)])
    return polys


def outlines(mask, offset=0.0, min_len=12, step=1):
    """Contour polylines (x, y) of a mask; offset < 0 insets (erode), > 0 grows (dilate), in px."""
    from skimage import measure
    from scipy.ndimage import distance_transform_edt
    m = mask > .5
    if offset:
        if offset < 0:
            d = distance_transform_edt(m)
            m = d > -offset
        else:
            d = distance_transform_edt(~m)
            m = d <= offset
    out = []
    for c in measure.find_contours(m.astype(np.float32), .5):
        if len(c) < min_len:
            continue
        out.append([(float(p[1]), float(p[0])) for p in c[::step]])
    return out


def andamento(mask, col, cell, rows=(0,), sc=1.0):
    """Contour rows for mosaic(): rows of tesserae following the outline (row 0 = just inside the edge;
    negative rows lie outside, in the ground)."""
    res = []
    for r in rows:
        off = -(cell * (r + .5)) if r >= 0 else cell * (-r - .5)
        for poly in outlines(mask, off):
            res.append((poly, col, sc))
    return res
