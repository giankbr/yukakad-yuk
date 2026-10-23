"""Agent H4 helpers (riad-jeruk, paisley-kashmir, bauhaus-primer, peluncuran-buku): _a6_lib (bbox-local gouache /
watercolour, tint, side_light) + zellige piece shading, kani-weave quantised textile, screen-print ink with halftone and
misregistration, and editorial gouache helpers. Previews -> /tmp/pen/nb-H4/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *  # noqa
import _p1_lib, _j1_lib, _a6_lib
PREV = "/tmp/pen/nb-H4/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_a6_lib.PREV = PREV


def rgb_of(h):
    return np.array(hex_rgb(h), np.float32)


def opaque(rgb):
    return np.concatenate([np.clip(rgb, 0, 1), np.ones(rgb.shape[:2] + (1,), np.float32)], -1)


def wrapn(w, h, seed, sigma):
    return wrap_noise(w, h, seed, sigma)


def grid_xy(w, h):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return xx, yy


def paint_pieces(label, colors, seed=1, jitter=0.07, gloss=0.35, grout="#efe6d6", grout_w=1.4, cell_ids=None):
    """Zellige: label = int piece-colour index per pixel (-1 = none); every connected piece (cell_ids) gets its own
    glaze tone drift, a darker pooled rim and a soft gloss; grout lines where labels/cells change. Returns RGBA."""
    h, w = label.shape
    rng = np.random.default_rng(seed)
    pal = np.array([rgb_of(c) for c in colors], np.float32)
    rgb = pal[np.clip(label, 0, len(colors) - 1)]
    ids = cell_ids if cell_ids is not None else label
    # per-piece tone jitter (hash the id)
    hsh = ((ids.astype(np.int64) * 2654435761) % 1000003).astype(np.float32) / 1000003.0
    tone = 1 + (hsh - 0.5) * 2 * jitter
    rgb = rgb * tone[..., None]
    # boundaries
    edge = np.zeros((h, w), np.float32)
    for a in (ids, label):
        e = (np.abs(np.diff(a, axis=0, prepend=a[:1])) > 0) | (np.abs(np.diff(a, axis=1, prepend=a[:, :1])) > 0)
        edge = np.maximum(edge, e.astype(np.float32))
    edge = np.clip(gaussian_filter(edge, grout_w * 0.55) * 2.6, 0, 1)
    # glaze pools darker toward each piece edge, gloss in the middle
    inner = np.clip(1 - gaussian_filter(edge, 3.0) * 2.2, 0, 1)
    rgb = rgb * (0.86 + 0.14 * inner[..., None])
    lo = fbm(w, h, seed + 4, 50, 3)
    rgb = rgb * (1 + (lo[..., None] - 0.5) * 0.12)
    gl = np.clip(inner * (fbm(w, h, seed + 9, 16, 2) - 0.45) * 2.5, 0, 1) * gloss
    rgb = rgb + (1 - rgb) * gl[..., None] * 0.5
    # pitting: tiny unglazed specks
    sp = (np.random.default_rng(seed + 2).random((h, w)) > 0.9975).astype(np.float32)
    sp = gaussian_filter(sp, 0.6) * 3
    rgb = rgb * (1 - np.clip(sp, 0, 0.5)[..., None] * 0.6)
    g = rgb_of(grout)
    gn = 0.92 + 0.08 * fbm(w, h, seed + 12, 8, 2)
    rgb = rgb * (1 - edge[..., None]) + (g * gn[..., None]) * edge[..., None]
    a = (label >= 0).astype(np.float32)
    return np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1)


def zellige_star(w, h, c, colors, ox=0.0, oy=0.0, seed=1, wob=1.2, a=0.37, inner=0.17, dia=0.15):
    """8-point stars (square + rotated square) on a c-grid, inner octagon, small diamonds between, cream crosses.
    colors: [cross, starA, starB, inner, diamond]. Returns (label, ids)."""
    xx, yy = grid_xy(w, h)
    if wob:
        xx = xx + (fbm(w, h, seed, 30, 2) - 0.5) * wob * 2
        yy = yy + (fbm(w, h, seed + 1, 30, 2) - 0.5) * wob * 2
    X = (xx - ox) / c; Y = (yy - oy) / c
    i = np.floor(X + 0.5); j = np.floor(Y + 0.5)
    u = (X - i); v = (Y - j)
    au, av = np.abs(u), np.abs(v)
    star = (np.maximum(au, av) < a) | ((au + av) / math.sqrt(2) < a)
    octa = np.maximum(np.maximum(au, av), (au + av) / math.sqrt(2)) < inner
    i2 = np.floor(X); j2 = np.floor(Y)
    u2 = X - i2 - 0.5; v2 = Y - j2 - 0.5
    diam = (np.abs(u2) + np.abs(v2)) < dia
    label = np.zeros((h, w), np.int32)
    ids = (i2 * 7919 + j2 * 104729 + 5).astype(np.int64)  # cross pieces: per cell
    par = ((i + j) % 2 == 0)
    label[star] = np.where(par, 1, 2)[star]
    ids[star] = (i * 7919 + j * 104729 + 1)[star].astype(np.int64)
    label[octa] = 3
    ids[octa] = (i * 7919 + j * 104729 + 2)[octa].astype(np.int64)
    label[diam] = 4
    ids[diam] = (i2 * 7919 + j2 * 104729 + 3)[diam].astype(np.int64)
    return label, ids


def kani(mask_rgba, cell=3, twill=True, seed=1, palette=None):
    """Kani-weave look: downsample to a weft grid (cell px), snap to a small palette, upsample nearest, then add a
    2/2 twill relief and thread fuzz. mask_rgba: painted RGBA at full size."""
    h, w = mask_rgba.shape[:2]
    sh, sw = h // cell, w // cell
    im = to_image(mask_rgba).resize((sw, sh), Image.BOX)
    a = np.asarray(im, np.float32) / 255
    if palette is not None:
        pal = np.array([rgb_of(c) for c in palette], np.float32)
        d = ((a[..., None, :3] - pal[None, None]) ** 2).sum(-1)
        a = np.concatenate([pal[d.argmin(-1)], a[..., 3:4]], -1)
    a[..., 3] = (a[..., 3] > 0.45).astype(np.float32)
    big = np.asarray(to_image(a).resize((sw * cell, sh * cell), Image.NEAREST), np.float32) / 255
    out = np.zeros((h, w, 4), np.float32); out[:sh * cell, :sw * cell] = big
    xx, yy = grid_xy(w, h)
    if twill:
        t = np.sin(((xx + yy) / cell) * math.pi) * 0.5 + 0.5
        cx = np.abs(((xx % cell) / cell) - 0.5) * 2
        rel = 0.9 + 0.1 * t - 0.06 * cx
        fuzz = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (0.4, 1.2))
        fuzz = (fuzz - fuzz.mean()) / (fuzz.std() + 1e-6)
        out[..., :3] *= (rel + fuzz * 0.03)[..., None]
    out[..., :3] = np.clip(out[..., :3], 0, 1)
    # soften the alpha edge a touch (thread ends)
    out[..., 3] = np.clip(gaussian_filter(out[..., 3], 0.5), 0, 1)
    return out


def halftone(w, h, tone, cell=6.0, angle=0.4):
    """Halftone dot field: tone 0..1 -> dot coverage."""
    xx, yy = grid_xy(w, h)
    ca, sa = math.cos(angle), math.sin(angle)
    u = (xx * ca + yy * sa) / cell; v = (-xx * sa + yy * ca) / cell
    du = u - np.floor(u) - 0.5; dv = v - np.floor(v) - 0.5
    r = np.sqrt(du * du + dv * dv)
    rad = np.sqrt(np.clip(tone, 0, 1)) * 0.62
    return np.clip((rad - r) * cell * 0.9 + 0.5, 0, 1)


def screen(mask, col, seed=1, wear=0.22, rough=1.6, starve=0.0):
    """Screen-print ink: flat colour, slightly bumpy edge, mesh texture, uneven pull (starved streak), pinholes."""
    h, w = mask.shape
    m = displace(mask, seed, rough, 14)
    m = np.clip((gaussian_filter(m, 0.6) - 0.4) * 3.2, 0, 1)
    xx, yy = grid_xy(w, h)
    mesh = 0.97 + 0.03 * (np.sin(xx * 1.9) * np.sin(yy * 1.9))
    pull = fbm(w, h, seed + 2, 140, 2)
    cov = 1 - starve * np.clip((pull - 0.55) * 2.5, 0, 1)
    pin = fbm(w, h, seed + 5, 5, 2)
    cov = cov * (1 - wear * np.clip((pin - 0.66) * 5, 0, 1))
    tone = 0.95 + 0.07 * fbm(w, h, seed + 7, 40, 2)
    rgb = np.ones((h, w, 3), np.float32) * rgb_of(col) * (tone * mesh)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), (m * np.clip(cov, 0, 1))[..., None]], -1)


def SC(dst, mask, *a, pad=10, **k):
    return OV(dst, mask, lambda m: screen(m, *a, **k), pad=pad)


def multiply(dst, src):
    """Overprint (ink multiply) for screen-print overlaps; keeps alpha union."""
    sa = src[..., 3:4]; da = dst[..., 3:4]
    oa = sa + da * (1 - sa)
    both = dst[..., :3] * src[..., :3]
    mixd = both * sa + dst[..., :3] * (1 - sa)
    k = np.clip(da * 4, 0, 1)
    rgb = mixd * k + src[..., :3] * (1 - k)
    return np.concatenate([np.clip(rgb, 0, 1), oa], -1)


def SCM(dst, mask, *a, pad=10, **k):
    """screen-print with multiply overprint."""
    b = bbox(mask, pad)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    src = screen(np.ascontiguousarray(mask[y0:y1, x0:x1]), *a, **k)
    out = dst.copy()
    out[y0:y1, x0:x1] = multiply(dst[y0:y1, x0:x1], src)
    return out


def rect_mask(w, h, x0, y0, x1, y1, rot=0.0):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pts = rot_pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], cx, cy, rot)
    return shape_mask(w, h, pts, smooth=False)


def comp_preview(arr, name, bg):
    preview(arr, name, bg=bg)
