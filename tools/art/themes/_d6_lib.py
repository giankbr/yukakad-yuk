"""Agent D6 helpers (ultah-sirkus, ultah-pertama, pengajian-akbar, peresmian-usaha): builds on _a6_lib (bbox-local
painting, crayon, sheen, spark) and adds gouache bodies, kid faces, stripes clipped to a shape, painted balloons,
confetti, wood grain and small lanterns. Previews -> /tmp/pen/nb-D6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _a6_lib import *  # noqa
import _a6_lib, _j1_lib
PREV = "/tmp/pen/nb-D6/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV
_a6_lib.PREV = PREV

INK = "#3a2a24"


def body_paint(art, m, col, col2, dark, light, nx, ldir=(-14, -16), blur=9, line=None, light_amt=0.5, dark_amt=0.72):
    """Opaque gouache body with a shadow side, a lit side and an optional crayon contour."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.5, streak=0.45)
    art = tint(art, side_light(m, *ldir, blur), dark, dark_amt, seed=nx())
    art = tint(art, side_light(m, -ldir[0] * .7, -ldir[1] * .7, blur * .8), light, light_amt, seed=nx())
    if line:
        art = crayon(art, inner_edge(m, 2.2), line, seed=nx(), amt=0.8, tooth=0.25)
    return art


def eye(art, W, H, x, y, r, nx, col="#2a1c18", shine=True):
    art = GP(art, ellipses(W, H, [(x, y, r * 0.86, r, 0)]), col, seed=nx(), rough=0.4, pad=6)
    if shine:
        art = OV(art, circles(W, H, [(x - r * 0.3, y - r * 0.38, r * 0.32)]), lambda m: col_arr(m, "#ffffff", m))
    return art


def closed_eye(art, W, H, x, y, r, nx, col=INK):
    return crayon(art, strokes(W, H, [(arc_pts(x, y - r * 0.4, r, 0.35, math.pi - 0.35, 12), max(2.4, r * 0.34), (0.2, 0.2))]), col, seed=nx(), amt=0.9)


def cheek(art, W, H, x, y, r, nx, col="#f19a96", amt=0.55):
    return G(art, circles(W, H, [(x, y, r)]), col, seed=nx(), density=amt, edge=0.2, bloom=0, rough=2, feather=2.5)


def smile(art, W, H, x, y, r, nx, col=INK, a0=0.45, a1=2.7, w=3.0):
    return crayon(art, strokes(W, H, [(arc_pts(x, y, r, a0, a1, 16), w, (0.2, 0.2))]), col, seed=nx(), amt=0.9)


def stripes(W, H, angle, width, gap, offset=0.0, wob=1.5, seed=1):
    """Band mask (0..1) of parallel stripes (duty = width / (width+gap)); slight hand wobble."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = (fbm(W, H, seed, 40, 2) - 0.5) * wob * 2
    u = (xx * math.cos(angle) + yy * math.sin(angle) + n + offset) / (width + gap)
    f = (u % 1.0) * (width + gap)
    return np.clip(np.minimum(f, width - f) / 1.2 + 0.5, 0, 1).astype(np.float32) * (f < width + 1)


def radial_stripes(W, H, cx, cy, n, duty=0.5, rot=0.0, wob=0.02, seed=1):
    """Fan of n wedges around (cx, cy) (tent canvas panels)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.arctan2(yy - cy, xx - cx) + rot + (fbm(W, H, seed, 60, 2) - 0.5) * wob * 2
    u = (a / (2 * math.pi) * n) % 1.0
    edge = 0.02
    return np.clip(np.minimum(u, duty - u) / edge + 0.5, 0, 1) * (u < duty + edge)


def balloon(art, W, H, x, y, rx, ry, col, col2, dark, light, nx, rng, string=True, tail_len=120, sway=0.0, knot=True, string_col="#8b7d74"):
    """Glossy-but-painted latex balloon: gouache body, cool shadow side, painted highlight, knot and a curly string."""
    m = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 18, rng.uniform(-.05, .05)) + [], rng, 1, 0.012)])
    tip = shapes(W, H, [[(x - rx * 0.12, y + ry * 0.93), (x + rx * 0.12, y + ry * 0.93), (x + rx * 0.09, y + ry * 1.08), (x - rx * 0.09, y + ry * 1.08)]], smooth=False)
    m = np.clip(m + tip * 0.0, 0, 1)
    if string:
        pts = [(x, y + ry * 1.1)]
        for k in range(1, 9):
            t = k / 8
            pts.append((x + math.sin(t * 5.2 + sway) * 9 * (1 - t * 0.3) + sway * 20 * t, y + ry * 1.1 + tail_len * t))
        art = crayon(art, strokes(W, H, [(curve(pts, 60), 2.0, (0.0, 0.3))]), string_col, seed=nx(), amt=0.75, tooth=0.2)
    art = body_paint(art, m, col, col2, dark, light, nx, ldir=(-rx * 0.16, -ry * 0.14), blur=max(8, rx * 0.25), light_amt=0.35)
    hi = shapes(W, H, [petal_pts(x - rx * 0.42, y - ry * 0.38, ry * 0.42, rx * 0.12, -2.0, n=14)])
    art = OV(art, gaussian_filter(hi, 1.6) * m, lambda mm: col_arr(mm, "#ffffff", mm * 0.62), pad=8)
    art = OV(art, circles(W, H, [(x - rx * 0.5, y - ry * 0.02, rx * 0.06)]) * m, lambda mm: col_arr(mm, "#ffffff", mm * 0.45), pad=6)
    if knot:
        k = shapes(W, H, [[(x - 7, y + ry + 10), (x, y + ry - 2), (x + 7, y + ry + 10)]], smooth=False)
        art = GP(art, k, dark, col, seed=nx(), rough=0.6, pad=6)
    return art


def confetti(art, W, H, n, cols, nx, rng, box=None, size=(6, 12), avoid=None):
    """Scatter of paper confetti: little rectangles, curls and dots in gouache."""
    x0, y0, x1, y1 = box or (0, 0, W, H)
    for col in cols:
        rects, curls, dots = [], [], []
        for _ in range(n // len(cols)):
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
            if avoid is not None and avoid[int(min(H - 1, y)), int(min(W - 1, x))] > 0.1:
                continue
            k = rng.random()
            s_ = rng.uniform(*size)
            if k < 0.5:
                a = rng.uniform(0, math.pi)
                c, sn = math.cos(a), math.sin(a)
                w2, h2 = s_ * 0.55, s_ * 0.28 * rng.uniform(0.6, 1)
                rects.append([(x + dx * c - dy * sn, y + dx * sn + dy * c) for dx, dy in ((-w2, -h2), (w2, -h2), (w2, h2), (-w2, h2))])
            elif k < 0.75:
                a = rng.uniform(0, 6.28)
                curls.append((curve([(x + math.cos(a + t * 2.2) * s_ * 0.5 + t * s_ * 0.6, y + math.sin(a + t * 2.2) * s_ * 0.5) for t in np.linspace(0, 1, 6)], 18), s_ * 0.22, (0.1, 0.1)))
            else:
                dots.append((x, y, s_ * 0.3))
        m = np.clip(shapes(W, H, rects, smooth=False) + (strokes(W, H, curls) if curls else 0) + (circles(W, H, dots) if dots else 0), 0, 1)
        art = GP(art, m, col, mix(col, "#ffffff", 0.15), seed=nx(), rough=0.7, pad=6)
    return art


def wood(art, m, col, col2, dark, nx, angle=0.0, ring=18.0, grain_amt=0.35):
    """Gouache wood: base + streaky grain lines along `angle`."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.8)
    b = bbox(m, 2, 0.01)
    if b is None:
        return art
    y0, y1, x0, x1 = b
    h, w = y1 - y0, x1 - x0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = -xx * math.sin(angle) + yy * math.cos(angle)
    n = fbm(w, h, nx(), 50, 3)
    g = 0.5 + 0.5 * np.sin((v + n * ring * 2.4) / ring * math.pi * 2)
    g = np.clip((g - 0.78) * 4, 0, 1)
    full = np.zeros_like(m)
    full[y0:y1, x0:x1] = g
    return tint(art, full * m, dark, grain_amt, seed=nx())


def star_pts(cx, cy, r_out, r_in, n=5, rot=-math.pi / 2):
    return [(cx + math.cos(rot + k * math.pi / n) * (r_out if k % 2 == 0 else r_in), cy + math.sin(rot + k * math.pi / n) * (r_out if k % 2 == 0 else r_in)) for k in range(2 * n)]


def rosette_pts(cx, cy, r, n=8, depth=0.72, rot=0.0):
    """n-point star made of two overlapping squares (8-fold khatam star outline)."""
    pts = []
    for k in range(2 * n):
        a = rot + k * math.pi / n
        rr = r if k % 2 == 0 else r * depth
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def soft_ground(art, W, H, cx, cy, rx, ry, col, nx, amt=0.35):
    return G(art, ellipses(W, H, [(cx, cy, rx, ry, 0)]), col, seed=nx(), density=amt, edge=0.05, bloom=0, rough=3, feather=6)
