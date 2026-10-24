"""Monokrom Syari — strict black & white: bold khatam (eight-point star) lattice, star frame, banded divider and a
small star, all relief-printed (linocut ink with wear) so the geometry stays crisp but hand-printed.
Run: python3 -I monokrom-syari.py [tile frame divider star]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q5_lib import *

OUT = outdir("monokrom-syari")
PARTS = sys.argv[1:] or ["tile", "frame", "divider", "star"]
BLACK = "#111111"


def star8(cx, cy, r, rot=0.0):
    """Eight-point star outline (two interlaced squares) as one closed polygon."""
    return star_pts(cx, cy, r, r * math.cos(math.pi / 4) / math.cos(math.pi / 8) * 0.92, 8, rot)


def poly_stroke(cv, pts, width):
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=width, Style=skia.Paint.kStroke_Style, StrokeJoin=skia.Paint.kMiter_Join)
    cv.c.drawPath(poly_path(pts), p)


if "tile" in PARTS:
    # seamless 2x2 khatam lattice: stars at grid points, cross-shaped interspaces, octagon cores
    T, c = 480, 240
    cv = Canvas(T, T)
    for i in range(-1, 4):
        for j in range(-1, 4):
            x, y = i * c, j * c
            poly_stroke(cv, star8(x, y, c * 0.52, -math.pi / 2), 9)
            poly_stroke(cv, rpoly(x, y, c * 0.24, 8, math.pi / 8), 5)
            hx, hy = x + c / 2, y + c / 2
            poly_stroke(cv, rpoly(hx, hy, c * 0.18, 4, math.pi / 4), 5)
    m = cv.array()[..., 3]
    # ink with print wear (seamless: wear from a wrapped noise)
    wear = wrap_noise(T, T, 5, 1.2)
    a = np.clip((m - 0.35) * 3, 0, 1) * (1 - 0.35 * np.clip((wear - 0.7) * 5, 0, 1))
    tone = 0.9 + 0.1 * wrap_noise(T, T, 7, 30)
    rgb = np.ones((T, T, 3), np.float32) * np.array(hex_rgb(BLACK), np.float32) * tone[..., None]
    tile = np.concatenate([rgb, a[..., None]], -1)
    preview(tile, "ms-tile", bg="#ffffff")
    save_full(tile, f"{OUT}/tile.webp", size=(240, 240), quality=80)

if "frame" in PARTS:
    W = H = 640
    nx = Seq(41000)
    cx = cy = W / 2
    cv = Canvas(W, H)
    poly_stroke(cv, star8(cx, cy, 300, -math.pi / 2), 22)
    poly_stroke(cv, star8(cx, cy, 266, -math.pi / 2), 5)
    poly_stroke(cv, rpoly(cx, cy, 178, 8, math.pi / 8), 4)
    m = cv.array()[..., 3]
    # notches on the tips (little squares)
    tips = [rpoly(cx + math.cos(-math.pi / 2 + k * math.pi / 4) * 300, cy + math.sin(-math.pi / 2 + k * math.pi / 4) * 300, 13, 4, k * math.pi / 4) for k in range(8)]
    m = np.maximum(m, shapes(W, H, tips, smooth=False))
    art = LC(blank(W, H), m, "#ffffff", seed=nx(), wear=0.22, rough=1.0)
    preview(art, "ms-frame", bg="#111111")
    save(art, f"{OUT}/frame.webp", max_w=560, quality=84)

if "divider" in PARTS:
    W, H = 720, 72
    nx = Seq(42000)
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    cv.c.drawRect(skia.Rect(40, 33, 290, 39), p)
    cv.c.drawRect(skia.Rect(430, 33, 680, 39), p)
    for k, x in enumerate([308, 360, 412]):
        r = 30 if k == 1 else 18
        cv.c.drawPath(poly_path(star8(x, 36, r, -math.pi / 2)), p)
    m = cv.array()[..., 3]
    holes = circles(W, H, [(360, 36, 10), (308, 36, 5), (412, 36, 5)])
    m = np.clip(m - holes, 0, 1)
    sq = shapes(W, H, [rpoly(30, 36, 7, 4, math.pi / 4), rpoly(690, 36, 7, 4, math.pi / 4)], smooth=False)
    m = np.maximum(m, sq)
    art = LC(blank(W, H), m, BLACK, seed=nx(), wear=0.3, rough=0.9)
    preview(art, "ms-divider", bg="#ffffff")
    save(art, f"{OUT}/divider.webp", max_w=440, quality=84)

if "star" in PARTS:
    W = H = 200
    nx = Seq(43000)
    m = shapes(W, H, [star8(100, 100, 92, -math.pi / 2)], smooth=False)
    m = np.clip(m - shapes(W, H, [rpoly(100, 100, 40, 8, math.pi / 8)], smooth=False) + shapes(W, H, [rpoly(100, 100, 24, 4, math.pi / 4)], smooth=False), 0, 1)
    art = LC(blank(W, H), m, BLACK, seed=nx(), wear=0.3, rough=0.9)
    preview(art, "ms-star", bg="#ffffff")
    save(art, f"{OUT}/star.webp", max_w=120, quality=84)

kb(OUT)
