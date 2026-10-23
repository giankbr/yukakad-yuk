"""Agent O5 helpers (muaro-jambi, anyaman-pandan, toko-roti, ultah-balok). Builds on _n3_lib/_jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, tint, edge_ring, below/above, rr_mask ...). Previews -> /tmp/pen/nb-O5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _n3_lib import *  # noqa
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-O5/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)


def P(art, m, c1, c2=None, seed=1, rough=1.6, streak=0.8, density=0.96):
    """Opaque gouache fill, computed inside the mask bbox."""
    return GP(art, m, c1, c2 or c1, seed=seed, rough=rough, streak=streak, density=density)


def W(art, m, c1, c2=None, seed=1, density=0.55, edge=0.35, bloom=0.25, rough=3.0, gran=0.25):
    """Watercolour glaze (shading / washes)."""
    return G(art, m, c1, c2 or c1, seed=seed, density=density, edge=edge, bloom=bloom, rough=rough, gran=gran)


def rect(Wd, Hd, x0, y0, x1, y1):
    return shapes(Wd, Hd, [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], smooth=False)


def brick_field(Wd, Hd, bw, bh, seed=1, mortar=1.6, wob=0.6, jit=0.12):
    """Running-bond brick courses: returns (bricks mask, per-pixel brick tone 0..1)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
    n = (fbm(Wd, Hd, seed + 3, 24, 2) - 0.5) * wob * 2
    row = np.floor((yy + n) / bh)
    off = (row % 2) * bw * 0.5
    col = np.floor((xx + off + n * 0.6) / bw)
    fy = ((yy + n) % bh)
    fx = ((xx + off + n * 0.6) % bw)
    m = ((fy > mortar) & (fy < bh - mortar * 0.4) & (fx > mortar) & (fx < bw - mortar * 0.4)).astype(np.float32)
    ids = (row * 9973 + col * 31).astype(np.int64) % 4096
    lut = rng.random(4096).astype(np.float32)
    tone = lut[ids] * (1 - jit) + jit * fbm(Wd, Hd, seed + 7, 14, 2)
    return gaussian_filter(m, 0.5), tone


def checker_weave(Wd, Hd, cell, seed=1, ang=math.pi / 4):
    """Diagonal over-under plaited strips (tikar): returns (stripA mask, stripB mask, shade) at 45 degrees."""
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
    c, s = math.cos(ang), math.sin(ang)
    u = (xx * c + yy * s) / cell
    v = (-xx * s + yy * c) / cell
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = u - iu, v - iv
    top_a = ((iu + iv) % 2 == 0)
    gap = 0.06
    a = ((fv > gap) & (fv < 1 - gap)).astype(np.float32)
    b = ((fu > gap) & (fu < 1 - gap)).astype(np.float32)
    A = np.where(top_a, a, a * (1 - b))
    B = np.where(top_a, b * (1 - a), b)
    # curvature shade: strips dip under neighbours
    shadeA = np.abs(fu - 0.5) * 2
    shadeB = np.abs(fv - 0.5) * 2
    shade = np.where(A > 0.5, shadeA, shadeB)
    return gaussian_filter(A, 0.6), gaussian_filter(B, 0.6), shade, iu, iv


def weave(Wd, Hd, n_cells, colA, colB, seed=1, fibre=0.5, wrap=True, ang=math.pi / 4, gap=0.07, cell=None):
    """Painted plaited mat (tikar anyaman): two sets of strips at +/-45 deg, over-under checker.
    colA(iv) / colB(iu) -> hex for each strip index (numpy int arrays). n_cells strips per tile width (seamless when
    wrap). Returns opaque RGBA float."""
    cell = cell or Wd / (n_cells * math.sqrt(2))
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
    c, s = math.cos(ang), math.sin(ang)
    u = (xx * c + yy * s) / cell
    v = (-xx * s + yy * c) / cell
    iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    fu, fv = u - iu, v - iv
    top_a = ((iu + iv) % 2 == 0)
    edge = lambda f: np.clip(np.minimum(f - gap, 1 - gap - f) / 0.05, 0, 1)
    inA, inB = edge(fv), edge(fu)
    A = np.where(top_a, inA, inA * (1 - inB))
    B = np.where(top_a, inB * (1 - inA), inB)
    nz = (lambda sg: wrap_noise(Wd, Hd, seed + sg, 1.2)) if wrap else (lambda sg: gaussian_filter(np.random.default_rng(seed + sg).random((Hd, Wd)).astype(np.float32), 1.2))
    def cols(fn, idx):
        uniq = np.unique(idx)
        out = np.zeros(idx.shape + (3,), np.float32)
        for k in uniq:
            out[idx == k] = col3(fn(int(k)))
        return out
    ca, cb = cols(colA, iv), cols(colB, iu)
    # along-strip fibres: streaks stretched along the strip direction
    fa = nz(1); fb = nz(2)
    from scipy.ndimage import map_coordinates as _mc
    # strip shading: ends of each visible segment dip under the crossing strip
    shA = 1 - 0.32 * (np.abs(fu - 0.5) * 2) ** 2.2 - 0.12 * (np.abs(fv - 0.5) * 2) ** 3
    shB = 1 - 0.32 * (np.abs(fv - 0.5) * 2) ** 2.2 - 0.12 * (np.abs(fu - 0.5) * 2) ** 3
    linesA = 0.5 + 0.5 * np.sin((fv * 9 + (fa - 0.5) * 2.5) * math.pi)
    linesB = 0.5 + 0.5 * np.sin((fu * 9 + (fb - 0.5) * 2.5) * math.pi)
    texA = (1 - fibre * 0.12 * linesA) * (0.94 + 0.12 * fa)
    texB = (1 - fibre * 0.12 * linesB) * (0.94 + 0.12 * fb)
    rgbA = ca * (shA * texA)[..., None]
    rgbB = cb * (shB * texB)[..., None] * 0.95
    gapc = col3("#3a2a18") * 0.9
    rgb = gapc * (1 - np.clip(A + B, 0, 1))[..., None] + rgbA * A[..., None] + rgbB * B[..., None]
    if wrap:
        low = wrap_noise(Wd, Hd, seed + 9, 40)
    else:
        low = fbm(Wd, Hd, seed + 9, 120, 2)
    rgb *= (0.95 + 0.1 * low)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((Hd, Wd, 1), np.float32)], -1)
