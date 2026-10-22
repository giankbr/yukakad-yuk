"""Agent B1 helpers (minahasa-kawanua, gorontalo-karawo, nias-omo, mandar-sandeq): builds on _a1_lib/_j1_lib
(bbox-cropped painting) with thread-level textile renderers — supplementary-weft weave from a cell pattern (bentenan),
drawn-thread open-work with counted darning stitches (karawo), silk twill plaid with anisotropic sheen (lipaq saqbe)
— plus watercolour sea helpers. Previews -> /tmp/pen/nb-B1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a1_lib import *  # noqa
import _a1_lib
import _p1_lib
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates

PREV = "/tmp/pen/nb-B1/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_a1_lib.PREV = PREV


def show(arr, name, bg=None, tone="#f4ecdf"):
    """Preview PNG (composited on a flat colour or on paper)."""
    h, w = arr.shape[:2]
    if bg:
        base = np.ones((h, w, 3), np.float32) * col_arr(bg)
    else:
        base = np.asarray(paper(w, h, tone, 3), np.float32) / 255
    a = arr[..., 3:4]
    rgb = base * (1 - a) + arr[..., :3] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/{name}.png")


def _hash(v, k=12.9898):
    return (np.sin(v * k + 1.7) * 43758.5453) % 1.0


# ------------------------------------------------------------------ weave from a cell pattern (bentenan)
def weave_cells(pattern, palette, cell=6, seed=1, metallic=(), float_len=None, fibre=0.07):
    """Render an int pattern (rows x cols, one cell = one weft pick over one warp group) as woven cloth, thread level.
    Weft-faced: each pick is a horizontal thread with a round profile; it dips under the warp at staggered points
    (twill-ish float rhythm), fibres streak along the thread, every pick varies slightly in tone, `metallic` palette
    indices get a gold-thread sheen. Tileable when the pattern tiles. Returns opaque RGBA (h, w, 4)."""
    ph, pw = pattern.shape
    H, W = ph * cell, pw * cell
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cy = (yy // cell).astype(np.int32); cx = (xx // cell).astype(np.int32)
    fy = (yy % cell + 0.5) / cell; fx = (xx % cell + 0.5) / cell
    pal = np.array([hex_rgb(c) for c in palette], np.float32)
    idx = pattern[cy % ph, cx % pw]
    rgb = pal[idx]
    prof = np.sin(fy * math.pi) ** 0.55
    lum = 0.66 + 0.40 * prof
    # interlacing: weft passes under a warp end every `float_len` cells, staggered per pick
    fl = float_len or 3
    dip = ((cx + cy * 2) % fl == 0).astype(np.float32)
    lum *= 1 - dip * 0.32 * np.exp(-((fx - 0.5) / 0.18) ** 2) * (0.6 + 0.4 * prof)
    # warp ends peek between picks (thin darker lines at pick boundaries)
    lum *= 1 - 0.18 * np.exp(-(np.minimum(fy, 1 - fy) / 0.12) ** 2)
    pick = _hash(cy.astype(np.float32))
    lum *= 0.95 + 0.1 * pick
    rng = np.random.default_rng(seed)
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.35, cell * 0.9), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    lum *= 1 + fib * fibre
    slub = gaussian_filter(rng.random((ph * 2, pw * 2)).astype(np.float32), 2, mode="wrap")
    slub = np.asarray(Image.fromarray(((slub - slub.min()) / (np.ptp(slub) + 1e-6) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    lum *= 0.95 + 0.08 * slub
    out = rgb * lum[..., None]
    if metallic:
        met = np.isin(idx, list(metallic)).astype(np.float32)
        sheen = 0.5 + 0.5 * np.sin((xx * 0.9 + yy * 0.35) / (W / 6) * math.tau / 6 + slub * 4)
        spec = (prof ** 6) * (0.4 + 0.6 * sheen)
        gold = rgb * (0.55 + 0.55 * prof[..., None]) + np.array([1.0, 0.92, 0.7], np.float32) * spec[..., None] * 0.45
        out = out * (1 - met[..., None]) + gold * met[..., None]
    return np.concatenate([np.clip(out, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def manhattan_ring(ph, pw, cy, cx, r0, r1):
    yy, xx = np.mgrid[0:ph, 0:pw]
    d = np.abs(yy - cy) + np.abs(xx - cx)
    return (d >= r0) & (d <= r1)


# ------------------------------------------------------------------ karawo: drawn-thread open-work + darning
def karawo(cells, palette, ground="#f4eadb", pitch=9, bar=3, seed=1, hem=None):
    """Drawn-thread embroidery (sulaman karawo). `cells` (rows x cols ints): -1 = plain cloth (not drawn), 0 = open
    grid (threads pulled: square holes with overcast thread bars), k>0 = grid square filled with counted darning in
    palette[k-1]. Every pixel is thread: fine cloth weave, wrapped bars with a spiral twist, darning floss (3–4 passes
    per square, glossy, tiny gaps). Holes are transparent so the page shows through. Returns RGBA."""
    rows, cols = cells.shape
    H, W = rows * pitch, cols * pitch
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = (yy // pitch).astype(np.int32); c = (xx // pitch).astype(np.int32)
    fy = (yy % pitch) / pitch; fx = (xx % pitch) / pitch
    cl = cells[np.clip(r, 0, rows - 1), np.clip(c, 0, cols - 1)]
    g = col_arr(ground)
    rng = np.random.default_rng(seed)
    # fine plain-weave cloth (2px threads)
    i2 = (xx // 2); j2 = (yy // 2)
    ov = ((i2 + j2) % 2).astype(np.float32)
    cloth_l = 0.9 + 0.08 * np.where(ov > 0, np.sin(((xx % 2) + .5) / 2 * math.pi), np.sin(((yy % 2) + .5) / 2 * math.pi))
    n = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.4, 1.6))
    cloth_l *= 0.96 + 0.08 * (n - n.mean()) / (n.std() + 1e-6) * 0.5
    rgb = g[None, None, :] * cloth_l[..., None]
    a = np.ones((H, W), np.float32)
    # open grid: bars at the start of each square (bar px wide) in both directions
    bw = bar / pitch
    inbar_x = fx < bw; inbar_y = fy < bw
    bar_m = (inbar_x | inbar_y)
    hole = (~bar_m)
    opened = cl >= 0
    # overcast bars: spiral twist shading
    tw_y = np.sin((yy * 0.9 + xx * 0.0) * 1.6) * 0.5 + 0.5
    tw_x = np.sin((xx * 0.9) * 1.6) * 0.5 + 0.5
    prof_x = np.clip(np.sin(np.clip(fx / bw, 0, 1) * math.pi), 0, 1) ** 0.6
    prof_y = np.clip(np.sin(np.clip(fy / bw, 0, 1) * math.pi), 0, 1) ** 0.6
    bar_l = np.where(inbar_x, 0.72 + 0.3 * prof_x * (0.7 + 0.3 * tw_y), 0.72 + 0.3 * prof_y * (0.7 + 0.3 * tw_x))
    bar_rgb = g[None, None, :] * bar_l[..., None]
    sel = opened & bar_m
    rgb = np.where(sel[..., None], bar_rgb, rgb)
    # holes transparent (soft-ish edge), a thin shadow on bars next to holes
    hole_open = opened & hole & (cl == 0)
    a = np.where(hole_open, 0.0, a)
    # darning: filled squares — horizontal floss passes inside the hole, slight overshoot onto bars
    fill = opened & (cl > 0) & hole
    pal = np.array([hex_rgb(p) for p in palette], np.float32)
    fcol = pal[np.clip(cl - 1, 0, len(palette) - 1)]
    inner = (fy - bw) / (1 - bw)
    passes = 3
    u = (inner * passes) % 1.0
    floss = np.sin(np.clip(u, 0, 1) * math.pi) ** 0.5
    gloss = 0.5 + 0.5 * np.sin(xx * 0.5 + _hash(r * 31.0 + c) * 6)
    fl = 0.70 + 0.28 * floss + 0.08 * gloss * floss
    gap = (u < 0.08).astype(np.float32)
    shade = _hash(r * 7.0 + c * 13.0)  # each square stitched a touch differently
    f_rgb = fcol * (fl * (0.94 + 0.1 * shade))[..., None]
    rgb = np.where(fill[..., None], f_rgb, rgb)
    a = np.where(fill, 1 - gap * 0.55, a)
    # floss also wraps the bars around filled squares (counted stitches cross bars)
    cross = opened & (cl > 0) & inbar_x & ~inbar_y
    rgb = np.where(cross[..., None], fcol * (0.78 + 0.2 * prof_x)[..., None], rgb)
    # soft shadow at hole rims (depth)
    am = gaussian_filter(a, 0.8)
    rim = np.clip(a - gaussian_filter(a, 1.6), 0, 1) * 0
    dark = np.clip(1 - gaussian_filter(a, 1.4), 0, 1) * a
    rgb = rgb * (1 - dark[..., None] * 0.35)
    cut = (cl == -2)
    a = np.where(cut, 0.0, a)
    am = np.where(cut, 0.0, am)
    # rolled hem around cut-outs: a raised, slightly darker cord
    if cut.any():
        cutf = cut.astype(np.float32)
        near = np.clip(gaussian_filter(cutf, 1.6) * 3, 0, 1) * (1 - cutf)
        cord = 0.8 + 0.25 * np.sin(xx * 1.3 + yy * 1.3)
        rgb = rgb * (1 - near[..., None] * 0.25) + g * cord[..., None] * near[..., None] * 0.25 * 0
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(am * 0.5 + a * 0.5, 0, 1)[..., None]], -1)


def raster_cells(rows, cols, draw, thr=0.45):
    """Draw shapes with skia into a rows x cols grid (1 px = 1 cell) and threshold -> bool array."""
    m = mask_from(cols, rows, draw)
    return m > thr


# ------------------------------------------------------------------ silk twill plaid (lipaq saqbe)
def stripe_index(seq, n):
    """seq [(colour_index, threads)], returns colour index per thread for n threads (repeating)."""
    out = []
    while len(out) < n:
        for ci, k in seq:
            out += [ci] * k
    return np.array(out[:n], np.int32)


def silk_plaid(W, H, warp_seq, weft_seq, palette, t=3, seed=1, sheen=0.5, folds=0.5):
    """Silk 2/2 twill check: warp colour stripes × weft colour stripes; each pixel shows the warp or weft thread
    depending on the twill step, both with round thread profiles; warp and weft catch the light differently
    (anisotropic sheen) and soft fabric folds modulate it. Tileable when the stripe repeats divide W/t and H/t."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    i = (xx // t).astype(np.int32); j = (yy // t).astype(np.int32)
    wi = stripe_index(warp_seq, W // t + 1)[i]
    we = stripe_index(weft_seq, H // t + 1)[j]
    pal = np.array([hex_rgb(p) for p in palette], np.float32)
    warp_on = ((i + j) % 4) < 2
    fx = (xx % t + 0.5) / t; fy = (yy % t + 0.5) / t
    pw = np.sin(fx * math.pi) ** 0.5; pf = np.sin(fy * math.pi) ** 0.5
    fold = (fbm(W, H, seed, 160, 3) - 0.5) * 2 * folds
    sh_w = 0.5 + 0.5 * np.sin((xx / W) * math.tau * 2 + fold * 2.5)
    sh_f = 0.5 + 0.5 * np.sin((yy / H) * math.tau * 2 + fold * 2.5 + 1.3)
    lw = 0.72 + 0.26 * pw + sheen * 0.32 * sh_w * pw ** 3
    lf = 0.70 + 0.26 * pf + sheen * 0.22 * sh_f * pf ** 3
    rgb = np.where(warp_on[..., None], pal[wi] * lw[..., None], pal[we] * lf[..., None])
    n = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.6, mode="wrap")
    rgb *= (0.97 + 0.06 * (n - n.min()) / (np.ptp(n) + 1e-6))[..., None]
    # white sheen lift (silk) where both sheens high
    lift = np.clip(sh_w * sh_f - 0.55, 0, 1) * sheen * 0.35
    rgb = rgb + (1 - rgb) * lift[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


# ------------------------------------------------------------------ misc
def hband(W, H, y0, y1):
    m = np.zeros((H, W), np.float32); m[int(y0):int(y1)] = 1
    return m


def rect(W, H, x0, y0, x1, y1):
    m = np.zeros((H, W), np.float32); m[int(max(0, y0)):int(y1), int(max(0, x0)):int(x1)] = 1
    return m


def quad(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def tint(arr, col, amt):
    out = arr.copy(); out[..., :3] = out[..., :3] * (1 - amt) + col_arr(col) * amt
    return out


def alpha_mul(arr, m):
    out = arr.copy(); out[..., 3] *= m
    return out


def fade_edges(arr, top=0, bottom=0, left=0, right=0):
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = np.ones((h, w), np.float32)
    if top: k *= np.clip(yy / top, 0, 1)
    if bottom: k *= np.clip((h - 1 - yy) / bottom, 0, 1)
    if left: k *= np.clip(xx / left, 0, 1)
    if right: k *= np.clip((w - 1 - xx) / right, 0, 1)
    return alpha_mul(arr, k ** 1.2)
