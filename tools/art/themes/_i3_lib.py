"""Agent I3 helpers (lasem-tiga-negeri, sambas-lunggi, sanaa-qamariya, ultah-koki): builds on _a1_lib (bbox-cropped
painting + textile media) with batik dye-on-cloth (wax resist, crackle, layered dye baths), stained glass, gypsum
relief and outlined kids gouache. Previews -> /tmp/pen/nb-I3/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _a1_lib import *  # noqa
import _a1_lib, _j1_lib
PREV = "/tmp/pen/nb-I3/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = _j1_lib.PREV = _a1_lib.PREV = PREV
import art as _art
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt


def prev(arr, name, bg=None, tone="#fbf6e4"):
    """preview() but always into PREV."""
    _p1_lib.PREV = PREV
    preview(arr, name, tone=tone, bg=bg)


# ------------------------------------------------------------------ batik
def crackle(w, h, seed, scale=26.0, width=0.022):
    """Remukan: fine fractured vein lines where wax cracked and dye seeped in (0..1)."""
    n1 = fbm(w, h, seed, scale, 3)
    n2 = fbm(w, h, seed + 9, scale * 0.6, 3)
    v = np.minimum(np.abs(n1 - 0.5), np.abs(n2 - 0.5) * 1.3)
    return np.clip((width - v) / width, 0, 1) ** 1.5


def dye_bath(cloth, mask, col, seed=1, depth=0.9, bleed=1.2, crack=0.5, mott=0.25):
    """Dye `mask` area of opaque cloth with colour (multiply-like), soft capillary edge, crackle veins and mottling."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(displace(mask, seed, bleed, 10), 0.6 + bleed * 0.3), 0, 1)
    c = col_arr(col)
    mot = 1 - mott * 0.5 + mott * fbm(w, h, seed + 4, 40, 3)
    a = np.clip(m * depth * mot, 0, 1)[..., None]
    rgb = cloth[..., :3] * (1 - a) + (cloth[..., :3] ** 0.4 * c) * a
    if crack:
        cr = crackle(w, h, seed + 2) * m * crack
        rgb = rgb * (1 - cr[..., None] * 0.45)
    out = cloth.copy()
    out[..., :3] = np.clip(rgb, 0, 1)
    return out


def batik_cloth(w, h, tone="#efe3c8", seed=1):
    base = cloth_base(w, h, tone, seed=seed, cell=2.2, var=0.08)
    return base


def cut_lines(mask, lines_mask):
    """Remove wax lines (stay cloth colour) from a fill."""
    return np.clip(mask - lines_mask, 0, 1)


def batik_motif(W, H, layers, lines, dots=None, seed=1, crack=0.45):
    """Transparent batik motif (lifted off cream cloth): layers = [(fill_mask, colour)], dyed fills with cream
    canting contour lines left as gaps (lines mask) and cecek dots. Returns RGBA."""
    out = blank(W, H)
    wl = lines
    if dots is not None:
        wl = np.maximum(wl, dots)
    for k, (m, col) in enumerate(layers):
        fill = cut_lines(np.clip(m, 0, 1), wl)
        fill = np.clip(gaussian_filter(displace(fill, seed + k * 7, 0.9, 8), 0.5), 0, 1)
        c = col_arr(col)
        mot = 0.82 + 0.18 * fbm(W, H, seed + k * 3, 36, 3)
        rgb = np.ones((H, W, 3), np.float32) * c * mot[..., None]
        cr = crackle(W, H, seed + k * 11 + 5) * crack
        rgb *= 1 - cr[..., None] * 0.35
        # slight dye pooling at the line edges
        rim = np.clip(fill - gaussian_filter(fill, 2.0), 0, 1)
        rgb *= 1 - rim[..., None] * 0.35
        layer = np.concatenate([np.clip(rgb, 0, 1), fill[..., None] * 0.97], -1)
        out = over(out, layer)
    return out


# ------------------------------------------------------------------ stained glass / gypsum
def glass(mask, col, seed=1, glowc="#fff4c8", lit=0.75):
    """Lit coloured glass: bright core, cloudy cathedral-glass mottling, darker edges."""
    h, w = mask.shape
    m = np.clip(gaussian_filter(mask, 0.6), 0, 1)
    d = gaussian_filter(m, 5)
    core = np.clip(d * 1.4, 0, 1)
    c = col_arr(col); g = col_arr(glowc)
    mot = fbm(w, h, seed, 14, 3)
    t = (core * lit * (0.75 + 0.5 * mot))[..., None]
    rgb = c * (0.65 + 0.35 * mot[..., None]) * (1 - t) + (c * 0.4 + g * 0.6) * t
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def gypsum(mask, col="#f3ece0", shade="#b8a58d", seed=1, depth=1.6):
    """Carved white gypsum/plaster relief: chalky matte with soft emboss (light from top-left)."""
    h, w = mask.shape
    m = displace(mask, seed, 0.8, 10)
    m = np.clip((gaussian_filter(m, 0.6) - 0.3) * 2.4, 0, 1)
    gy, gx = np.gradient(gaussian_filter(m, depth))
    light = np.clip(1 - (gx + gy) * 5, 0.55, 1.3)
    c = col_arr(col); s = col_arr(shade)
    chalk = 0.92 + 0.08 * fbm(w, h, seed + 3, 6, 2)
    k = np.clip((light - 0.55) / 0.75, 0, 1)[..., None]
    rgb = (s * (1 - k) + c * k) * chalk[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


# ------------------------------------------------------------------ kids gouache with hand ink outline
def inked(art, mask, col, col2=None, seed=1, ink="#3a2f4a", lw=3.0, alpha=0.9):
    """Opaque gouache fill + wobbly hand-drawn ink outline (kids picture-book look)."""
    art = GP(art, mask, col, col2, seed=seed, rough=1.6, streak=0.8, pad=10)
    return ink_edge(art, mask, ink, lw, seed, alpha)


def ink_edge(art, mask, ink="#3a2f4a", lw=3.0, seed=1, alpha=0.9):
    m = displace(mask, seed + 1, 1.2, 14)
    inside = (m > 0.5).astype(np.float32)
    dist_out = distance_transform_edt(1 - inside)
    dist_in = distance_transform_edt(inside)
    h, w = mask.shape
    var = 0.6 + 0.8 * fbm(w, h, seed + 5, 30, 2)
    line = np.clip((lw * var * 0.5 - (dist_out + dist_in - 0.5)) + 0.5, 0, 1)
    br = fbm(w, h, seed + 8, 9, 2)
    line *= np.clip((br - 0.08) * 6, 0, 1)
    return over(art, flat(line, ink, alpha))


def shade_side(art, mask, col, side=(1, 1), amt=0.35, blur=10, seed=1):
    """Soft painted shadow inside mask toward one side (light from top-left)."""
    h, w = mask.shape
    sh = np.roll(np.roll(mask, int(-side[1] * blur), 0), int(-side[0] * blur), 1)
    k = np.clip(mask - gaussian_filter(sh, blur * 0.6), 0, 1) * mask
    k = gaussian_filter(k, 2) * (0.8 + 0.4 * fbm(w, h, seed, 20, 2))
    return over(art, flat(k, col, amt))


def highlight(art, mask, col="#ffffff", amt=0.4, blur=8):
    return shade_side(art, mask, col, (-1, -1), amt, blur)
