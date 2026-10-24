"""Gading Syari — ivory card stock with pressed gold-foil hairlines: a small geometric medallion (interlaced
eight-point star with a ring of lozenges), foil corner brackets, a hairline divider, a foil sheen tile for CSS
hairline frames, and a blind-embossed star-lattice ivory paper. Geometry only (no figures, no calligraphy).
Run: python3 -I gading-syari.py [part ...]  parts: medallion corner divider foiltile paper
Assets -> public/themes/art/gading-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q2_lib import *

OUT = outdir("gading-syari")
PARTS = sys.argv[1:] or ["medallion", "corner", "divider", "foiltile", "paper"]
GOLD = "#b8914a"
IVORY = "#f7f1e3"


def star_pts(cx, cy, r, rot=0.0, k=8, inner=None):
    """Two interlaced squares (k=8) as an outline polygon of the star."""
    inner = inner or r * math.cos(math.pi / 4) / math.cos(math.pi / 8) * 0.0 + r * 0.76
    pts = []
    for i in range(k * 2):
        a = rot + i * math.pi / k - math.pi / 2
        rr = r if i % 2 == 0 else inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def square_pts(cx, cy, r, rot):
    return [(cx + math.cos(rot + i * math.pi / 2) * r, cy + math.sin(rot + i * math.pi / 2) * r) for i in range(4)]


def line_mask(W, H, polys, width, closed=True):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                       StrokeJoin=skia.Paint.kMiter_Join)
        for pts in polys:
            path = poly_path(pts) if closed else None
            if not closed:
                path = skia.Path(); path.moveTo(*pts[0])
                for q in pts[1:]:
                    path.lineTo(*q)
            cv.c.drawPath(path, p)
    return mask_from(W, H, draw)


def ring(W, H, cx, cy, r, width):
    return ring_mask(W, H, cx, cy, r, width)


def foil_layer(W, H, mask, seed, base=GOLD):
    return FO(blank(W, H), mask, base, seed=seed, emboss=0.5, sparkle=0.18)


def medallion():
    S = 420
    c = S / 2
    lw = 2.6
    m = np.zeros((S, S), np.float32)
    # outer hairline circles with a dotted ring between
    m = np.maximum(m, ring(S, S, c, c, 196, lw))
    m = np.maximum(m, ring(S, S, c, c, 184, lw * 0.8))
    dots = [(c + math.cos(a) * 190, c + math.sin(a) * 190, 2.2) for a in np.linspace(0, math.tau, 49)[:-1]]
    # ring of 16 lozenges
    loz = []
    for i in range(16):
        a = i * math.tau / 16 - math.pi / 2
        x, y = c + math.cos(a) * 160, c + math.sin(a) * 160
        loz.append([(x + math.cos(a) * 16, y + math.sin(a) * 16), (x + math.cos(a + 1.57) * 6, y + math.sin(a + 1.57) * 6),
                    (x - math.cos(a) * 16, y - math.sin(a) * 16), (x - math.cos(a + 1.57) * 6, y - math.sin(a + 1.57) * 6)])
    m = np.maximum(m, shapes(S, S, loz, smooth=False))
    m = np.maximum(m, circles(S, S, dots))
    # interlaced 8-point star: two squares, hairline, with a parallel inner line (strapwork)
    for rot in (0.0, math.pi / 4):
        m = np.maximum(m, line_mask(S, S, [square_pts(c, c, 138, rot + math.pi / 4)], lw))
        m = np.maximum(m, line_mask(S, S, [square_pts(c, c, 126, rot + math.pi / 4)], lw * 0.8))
    m = np.maximum(m, ring(S, S, c, c, 96, lw))
    # solid foil inner star with a knocked-out hairline and a small ivory centre
    solid_star = shape_mask(S, S, star_pts(c, c, 78, 0.0, 8, 58), smooth=False)
    cut = line_mask(S, S, [star_pts(c, c, 64, 0.0, 8, 47)], 2.0)
    cut = np.maximum(cut, circles(S, S, [(c, c, 14)]))
    m = np.maximum(m, np.clip(solid_star - cut, 0, 1))
    m = np.maximum(m, circles(S, S, [(c, c, 5)]))
    arr = foil_layer(S, S, m, 3)
    preview(arr, "gs-medallion", tone=IVORY)
    save(arr, f"{OUT}/medallion.webp", quality=84)


def corner():
    """Corner bracket: two hairlines meeting in a stepped knot with a small eight-point star."""
    S = 300
    lw = 2.4
    m = np.zeros((S, S), np.float32)
    o1, o2 = 20, 34
    m = np.maximum(m, line_mask(S, S, [[(o1, S - 4), (o1, o1), (S - 4, o1)]], lw, closed=False))
    m = np.maximum(m, line_mask(S, S, [[(o2, S * 0.62), (o2, o2), (S * 0.62, o2)]], lw * 0.8, closed=False))
    # stepped knot at the corner
    st = shape_mask(S, S, star_pts(o1 + 2, o1 + 2, 19, math.pi / 8, 8, 12), smooth=False)
    m = np.maximum(m, st)
    m = np.clip(m - circles(S, S, [(o1 + 2, o1 + 2, 5)]), 0, 1)
    # end diamonds
    for x, y in [(o2, S * 0.62 + 10), (S * 0.62 + 10, o2)]:
        m = np.maximum(m, shapes(S, S, [[(x, y - 6), (x + 4, y), (x, y + 6), (x - 4, y)]], smooth=False))
    m = np.maximum(m, circles(S, S, [(o2 + 14, o2 + 14, 2.6)]))
    arr = foil_layer(S, S, m, 5)
    preview(arr, "gs-corner", tone=IVORY)
    save_full(arr, f"{OUT}/corner.webp", quality=84)


def divider():
    W, H = 520, 60
    c = W / 2
    lw = 2.2
    m = np.zeros((H, W), np.float32)
    m = np.maximum(m, line_mask(W, H, [[(10, 30), (c - 40, 30)], [(c + 40, 30), (W - 10, 30)]], lw, closed=False))
    m = np.maximum(m, line_mask(W, H, [[(c - 150, 36), (c - 46, 36)], [(c + 46, 36), (c + 150, 36)]], 1.4, closed=False))
    m = np.maximum(m, shape_mask(W, H, star_pts(c, 30, 22, 0.0, 8, 15), smooth=False))
    m = np.clip(m - line_mask(W, H, [star_pts(c, 30, 15, 0.0, 8, 10)], 1.6) - circles(W, H, [(c, 30, 3)]), 0, 1)
    for x in (c - 34, c + 34):
        m = np.maximum(m, shapes(W, H, [[(x, 25), (x + 4, 30), (x, 35), (x - 4, 30)]], smooth=False))
    m = np.maximum(m, circles(W, H, [(14, 30, 2.4), (W - 14, 30, 2.4)]))
    arr = foil_layer(W, H, m, 7)
    preview(arr, "gs-divider", tone=IVORY)
    save(arr, f"{OUT}/divider.webp", quality=86)


def foiltile():
    """Seamless 256 foil sheen for CSS hairlines / foil text accents."""
    S = 256
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    n = wrap_noise(S, S, 4, 18)
    sheen = 0.5 + 0.5 * np.sin((xx + yy) / S * math.tau * 2 + n * 4)
    g = wrap_noise(S, S, 5, 0.6)
    r, gg, b = hex_rgb(GOLD)
    lum = 0.7 + 0.42 * sheen + (g - 0.5) * 0.12
    rgb = np.stack([np.clip(r * lum * 1.12, 0, 1), np.clip(gg * lum * 1.1, 0, 1), np.clip(b * lum, 0, 1)], -1)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{OUT}/foil.webp", "WEBP", quality=80, method=6)
    print("foil.webp", os.path.getsize(f"{OUT}/foil.webp") // 1024, "KB")


def paper_tile():
    """Ivory stock with a blind-embossed lattice of small eight-point stars (very subtle relief)."""
    S = 240
    base = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(IVORY), np.float32)
    m = np.zeros((S, S), np.float32)
    for (x, y) in [(0, 0), (S, 0), (0, S), (S, S), (S / 2, S / 2)]:
        m = np.maximum(m, line_mask(S, S, [star_pts(x, y, 26, 0.0, 8, 19)], 1.6))
    for (x, y) in [(S / 2, 0), (S / 2, S), (0, S / 2), (S, S / 2)]:
        m = np.maximum(m, circles(S, S, [(x, y, 2.2)]))
    sm = gaussian_filter(m, 1.0)
    gy, gx = np.gradient(sm)
    relief = -(gx + gy) * 2.2
    fine = wrap_noise(S, S, 8, 0.7) - 0.5
    big = wrap_noise(S, S, 9, 30) - 0.5
    v = 1 + relief * 0.16 + fine * 0.03 + big * 0.025
    rgb = np.clip(base * v[..., None], 0, 1)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{OUT}/paper.webp", "WEBP", quality=84, method=6)
    print("paper.webp", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")
    Image.fromarray((rgb * 255).astype(np.uint8)).resize((S * 2, S * 2)).save(f"{PREV}/gs-paper.png")


for p in PARTS:
    {"medallion": medallion, "corner": corner, "divider": divider, "foiltile": foiltile, "paper": paper_tile}[p]()
    clear()
