"""Agent O1 helpers (batik-betawi, kampung-naga, abu-syari, ultah-pemadam). Builds on _n1_lib (G/GP/LC/FO/OV, strokes,
shapes, circles, ellipses, flat, dilate, erode, edge_ring ...). Previews -> /tmp/pen/nb-O1/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _n1_lib import *  # noqa
import _p1_lib
_p1_lib.PREV = "/tmp/pen/nb-O1/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)

LINE = "#1f2233"


def capsule(x0, y0, x1, y1, r, n=10):
    a = math.atan2(y1 - y0, x1 - x0)
    pts = []
    for i in range(n + 1):
        t = a + math.pi / 2 + math.pi * i / n
        pts.append((x0 + math.cos(t) * r, y0 + math.sin(t) * r))
    for i in range(n + 1):
        t = a - math.pi / 2 + math.pi * i / n
        pts.append((x1 + math.cos(t) * r, y1 + math.sin(t) * r))
    return pts


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for (cx, cy, a0) in [(x1 - r, y0 + r, -math.pi / 2), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, math.pi / 2), (x0 + r, y0 + r, math.pi)]:
        for i in range(n + 1):
            a = a0 + math.pi / 2 * i / n
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def paint_part(art, W, H, m, col, col2, nx, shade_dir=(1, 1), shade=0.32, hi=0.22, line=True, line_col=None, off=10):
    """Storybook gouache part: opaque body, soft core shadow on one side, lighter rim on the other, soft ink line."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=0.6)
    dx, dy = shade_dir
    g = gaussian_filter(m, 6)
    sh = np.clip(m - np.roll(np.roll(g, -int(off * dy), 0), -int(off * dx), 1) * 1.1, 0, 1) * m
    art = G(art, sh, mix(col2, line_col or LINE, 0.35), seed=nx(), density=shade, edge=0.2, bloom=0.2, rough=2)
    lt = np.clip(m - np.roll(np.roll(g, int(off * dy), 0), int(off * dx), 1) * 1.1, 0, 1) * m
    art = OV(art, lt, lambda q: flat(q, mix(col, "#ffffff", 0.5), hi))
    if line:
        art = G(art, edge_ring(m, 1.4), line_col or LINE, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.8, feather=0.5)
    return art


# ---------------------------------------------------------------- batik (wax resist) media
def crackle(W, H, seed, scale=26.0, width=0.9):
    """Remukan: thin branching crackle veins where the wax cracked and dye crept in."""
    rng = np.random.default_rng(seed)
    n = gaussian_filter(rng.random((H, W)).astype(np.float32), scale / 6)
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    v = np.abs(np.sin(n * 18.0))
    return np.clip((0.06 * width - v) / 0.04, 0, 1).astype(np.float32)


def dye(art, mask, col, col2=None, nx=None, density=0.92, crack=0.25):
    """Dye bath look: soaked colour with slight bleed and blotch, plus faint crackle."""
    H, W = mask.shape
    art = G(art, mask, col, col2 or col, seed=nx(), density=density, edge=0.25, bloom=0.15, gran=0.15, rough=1.2, feather=0.8, mottle=0.35)
    if crack:
        c = crackle(W, H, nx(), 30) * erode(mask, 1)
        art = G(art, c, mix(col2 or col, "#2a1208", 0.45), seed=nx(), density=crack, edge=0, bloom=0, rough=0.4, feather=0.4)
    return art


def wax_line(art, W, H, items, col, nx, density=0.95):
    """Canting outline: cream/white wax-resist line with a slightly beaded, uneven width."""
    m = strokes(W, H, items)
    return G(art, m, col, seed=nx(), density=density, edge=0.1, bloom=0, gran=0.1, rough=0.6, feather=0.4, mottle=0.2)


def isen_dots(W, H, pts, r=1.6):
    return circles(W, H, [(x, y, r) for x, y in pts])
