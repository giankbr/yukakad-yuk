"""Agent E6 helpers (ultah-samudra, bridal-shower, prom-perpisahan, pembaptisan).
Builds on _d5_lib (-> _jw_lib / _j1_lib / _p1_lib / art). Adds: chunky kids gouache with a coloured-pencil contour,
soft watercolour wash on a reserved paper ground, satin ribbon, glass/bubble, mirror-tile ball and light-beam helpers.
Previews -> /tmp/pen/nb-E6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _d5_lib import *  # noqa
import _p1_lib
import _d5_lib
import art as _art

PREV = "/tmp/pen/nb-E6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_d5_lib.PREV = PREV


def preview(arr, name, tone="#fbf6e4", bg=None):
    _p1_lib.PREV = PREV
    return _p1_lib.preview(arr, name, tone=tone, bg=bg)


def clear():
    _art._fbm_cache.clear()


def contour(mask, w=2.4, seed=91):
    """Ring just around/inside a mask edge (pencil/pen contour), with dry breaks."""
    e = np.clip(soft(mask, 0.8) * (1 - soft(mask, 0.8)) * 4, 0, 1)
    e = np.clip(gaussian_filter((e > 0.35).astype(np.float32), w * 0.35) * 2, 0, 1)
    h, ww = mask.shape
    brk = np.clip((fbm(ww, h, seed, 26, 2) - 0.12) * 4, 0, 1)
    return e * brk


def toon(art, m, col, col2=None, nx=None, shade=(-1, -1), k=14, sh_col=None, hi=True, line="#2c3a5a", line_w=2.4, line_a=0.75):
    """Kids-book gouache: opaque fill, crescent shade, a dry highlight and a crayon contour."""
    art = GP(art, m, col, col2 or mix(col, "#ffffff", 0.15), seed=nx(), rough=1.6, streak=0.7)
    if shade is not None:
        sh = inner_shade(m, int(-shade[0] * k), int(-shade[1] * k), blur=k)
        art = G(art, sh, sh_col or mix(col, "#2a3a7a", 0.45), seed=nx(), density=0.55, edge=0.25, bloom=0.2, rough=2)
    if hi:
        hl = inner_shade(m, int(shade[0] * k * 0.6) if shade else -6, int(shade[1] * k * 0.6) if shade else -6, blur=k * 0.6)
        art = G(art, hl * np.clip(fbm(m.shape[1], m.shape[0], nx(), 9, 2) * 2 - 0.4, 0, 1), "#ffffff", seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    if line:
        art = G(art, contour(m, line_w, nx()), line, seed=nx(), density=line_a, edge=0, bloom=0, rough=0.6, feather=0.35)
    return art


def wash(art, m, col, col2=None, nx=None, dens=0.7, shade=None, k=10, base=True, sh_col="#6d5a7a"):
    """Soft watercolour wash with a reserved white ground (covers what lies behind)."""
    if base:
        art = GP(art, m, "#fffdfb", "#fbf6f2", seed=nx(), rough=1.2, streak=0.2)
    art = G(art, m, col, col2 or mix(col, "#ffffff", 0.3), seed=nx(), density=dens, edge=0.55, bloom=0.4, rough=3, holes=0.03)
    if shade is not None:
        sh = inner_shade(m, int(shade[0] * k), int(shade[1] * k), blur=k)
        art = G(art, sh, mix(col, sh_col, 0.5), seed=nx(), density=0.45, edge=0.3, bloom=0.3, rough=2)
    return art


def pen(art, m, nx, col="#6b4a5a", w=2.0, dens=0.6):
    e = contour(m, w, nx())
    e = np.roll(np.roll(e, 1, 0), 1, 1)
    return G(art, e, col, seed=nx(), density=dens, edge=0, bloom=0, rough=0.5, feather=0.3)


def bubble(art, W, H, x, y, r, nx, rim="#ffffff", tint=None, dens=0.8):
    """Painted soap/sea bubble: faint tint, brighter rim, crescent glint."""
    disc = circles(W, H, [(x, y, r)])
    if tint:
        art = G(art, disc, tint, seed=nx(), density=0.18, edge=0.4, bloom=0, rough=0.6, pad=6)
    ring = np.clip(disc - circles(W, H, [(x, y, r * 0.84)]), 0, 1)
    art = G(art, ring, rim, seed=nx(), density=dens, edge=0.2, bloom=0, rough=0.5, pad=6, feather=0.7)
    gl = strokes(W, H, [(arc_pts(x, y, r * 0.62, math.pi * 1.1, math.pi * 1.45, 8), max(1.2, r * 0.16), (0.3, 0.3))])
    return G(art, gl, "#ffffff", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.3, pad=6, feather=0.4)


def ribbon_band(W, H, pts, width):
    """Polygon of constant width around a centre curve (sash / ribbon)."""
    n = len(pts); L = []; R = []
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nxn, nyn = -dy / d * width / 2, dx / d * width / 2
        L.append((pts[i][0] + nxn, pts[i][1] + nyn)); R.append((pts[i][0] - nxn, pts[i][1] - nyn))
    return L + R[::-1]


def satin(art, m, col, col2, nx, angle=0.5, freq=26.0, sheen=0.5):
    """Satin ribbon: base wash + soft sheen bands across the ribbon."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.3)
    h, w = m.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = 0.5 + 0.5 * np.sin((xx * math.cos(angle) + yy * math.sin(angle)) / freq + fbm(w, h, nx(), 60, 2) * 4)
    art = G(art, m * np.clip((band - 0.62) * 3, 0, 1), "#ffffff", seed=nx(), density=sheen, edge=0, bloom=0.1, rough=1)
    art = G(art, m * np.clip((0.35 - band) * 3, 0, 1), mix(col2, "#5a1f3a", 0.35), seed=nx(), density=sheen * 0.7, edge=0, bloom=0.1, rough=1)
    return art


def beam_mask(W, H, ox, oy, ang, length, spread):
    """Cone of light from (ox, oy) along ang (radians) with half-angle spread, fading with distance."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = xx - ox, yy - oy
    d = np.sqrt(dx * dx + dy * dy) + 1e-3
    a = np.arctan2(dy, dx) - ang
    a = (a + math.pi) % math.tau - math.pi
    cone = np.clip(1 - np.abs(a) / spread, 0, 1) ** 1.4
    fall = np.clip(1 - d / length, 0, 1) ** 0.8
    return (cone * fall).astype(np.float32)


def save_q(arr, path, max_w, quality=80):
    return save(arr, path, max_w=max_w, quality=quality)
