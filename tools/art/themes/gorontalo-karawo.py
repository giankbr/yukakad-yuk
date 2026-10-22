"""Gorontalo Karawo — soft lilac / mint / cream: sulaman karawo rendered thread by thread (threads drawn out of the cloth
leaving an open grid of overcast bars, counted darning stitches filling squares into florals), a karawo cloth frame
for the cover photo, a karawo band and divider, and rumah adat Dulohupa in watercolour.
Run: python3 -I gorontalo-karawo.py [part ...]   parts: frame band divider dulohupa
Assets -> public/themes/art/gorontalo-karawo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b1_lib import *

OUT = outdir("gorontalo-karawo")
PARTS = sys.argv[1:] or ["frame", "band", "divider", "dulohupa"]
CREAM = "#f6eedf"
LILAC, LILAC_D, MINT, MINT_D, ROSE, PLUM = "#b49bd0", "#8a6fae", "#98cdb9", "#5c9a86", "#e8a3a0", "#5a4470"
PAL = [LILAC, MINT, ROSE, LILAC_D, MINT_D, "#f3d58a"]   # 1..6


def flower(cells, cy, cx, r, rot=0.0, petal=1, centre=3, edge=4):
    """Counted 5-petal flower: petals (ellipses) + centre, rasterised to the grid; returns nothing (in place)."""
    rows, cols = cells.shape
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for k in range(5):
            a = rot + k * math.tau / 5
            cv.c.save(); cv.c.translate(cx + 0.5 + math.cos(a) * r * 0.55, cy + 0.5 + math.sin(a) * r * 0.55); cv.c.rotate(math.degrees(a))
            cv.c.drawOval(skia.Rect(-r * 0.5, -r * 0.34, r * 0.5, r * 0.34), p); cv.c.restore()
    pet = mask_from(cols, rows, draw) > 0.4
    core = mask_from(cols, rows, lambda cv: cv.c.drawCircle(cx + 0.5, cy + 0.5, max(0.9, r * 0.26), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))) > 0.4
    opened = cells >= 0
    # petal outline in the deeper tone, filled lighter
    from scipy.ndimage import binary_erosion
    inner = binary_erosion(pet)
    cells[pet & opened] = edge
    cells[inner & opened] = petal
    cells[core & opened] = centre


def leaf(cells, cy, cx, L, ang, col=2):
    rows, cols = cells.shape
    pts = petal_pts(cx + 0.5, cy + 0.5, L, L * 0.38, ang, n=12)
    m = shape_mask(cols, rows, pts, smooth=True) > 0.4
    cells[m & (cells == 0)] = col


def vine(cells, pts, col=5):
    rows, cols = cells.shape
    m = strokes(cols, rows, [(curve(pts, 40), 1.0, None)]) > 0.45
    cells[m & (cells == 0)] = col


if "frame" in PARTS:
    S = 1.5
    C, R = 66, 81
    cells = np.full((R, C), -1, np.int32)
    cells[3:R - 3, 3:C - 3] = 0
    def win(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        path = skia.Path(); x0, x1, y0, y1 = 14, C - 14, 14, R - 14
        r = (x1 - x0) / 2
        path.moveTo(x0, y1); path.lineTo(x0, y0 + r); path.arcTo(skia.Rect(x0, y0, x1, y0 + 2 * r), 180, 180, False); path.lineTo(x1, y1); path.close()
        cv.c.drawPath(path, p)
    wm = mask_from(C, R, win) > 0.5
    from scipy.ndimage import binary_dilation
    cells[binary_dilation(wm, iterations=2)] = -1
    cells[wm] = -2
    m = 8.5
    for (y, x) in [(m, m), (m, C - 1 - m), (R - 1 - m, m), (R - 1 - m, C - 1 - m)]:
        flower(cells, int(y), int(x), 7.0, rot=0.3)
    for (y, x) in [(R // 2 - 7, 7), (R // 2 - 7, C - 8), (R // 2 + 9, 7), (R // 2 + 9, C - 8)]:
        flower(cells, y, x, 4.2, rot=0.9, petal=3, centre=6, edge=3)
    for (y, x) in [(7, C // 2), (R - 8, C // 2)]:
        flower(cells, y, x, 4.6, rot=-0.3, petal=1, centre=6, edge=4)
    for side in (1, -1):
        X = (lambda v: v) if side == 1 else (lambda v: C - 1 - v)
        vine(cells, [(X(8), 17), (X(11), 22), (X(6), 27), (X(9), 31)])
        vine(cells, [(X(8), R - 18), (X(11), R - 23), (X(6), R - 28), (X(9), R - 32)])
        leaf(cells, 23, X(10), 4.6, 0.5 if side == 1 else math.pi - 0.5)
        leaf(cells, R - 24, X(10), 4.6, -0.5 if side == 1 else math.pi + 0.5)
    for (x, y, a) in [(C // 2 - 9, 7, 0.1), (C // 2 + 9, 7, math.pi - 0.1), (C // 2 - 9, R - 8, -0.1), (C // 2 + 9, R - 8, math.pi + 0.1)]:
        leaf(cells, y, x, 5.4, a)
    k = karawo(cells, PAL, ground=CREAM, pitch=6, bar=2, seed=3)
    H, W = k.shape[:2]
    pad = 18
    out = np.zeros((H + pad * 2, W + pad * 2, 4), np.float32)
    out[pad:pad + H, pad:pad + W] = k
    edge = np.zeros(out.shape[:2], np.float32); edge[pad:pad + H, pad:pad + W] = 1
    edge = displace(edge, 5, 1.6, 20)
    out[..., 3] *= np.clip(edge * 1.4, 0, 1)
    sh = soft_shadow(np.clip(edge, 0, 1) * (out[..., 3] > 0.5), "#5a4470", blur=7, strength=0.22, dx=3, dy=5)
    out = over(sh, out)
    save_full(out, f"{OUT}/frame.webp", quality=84)
    show(out, "gk-frame", bg="#efe7f4")
    clear()

if "band" in PARTS:
    C, R = 96, 15
    cells = np.full((R, C), -1, np.int32)
    cells[2:R - 2, :] = 0
    for i, x in enumerate(range(8, C, 16)):
        flower(cells, 7, x, 5.0 if i % 2 == 0 else 3.6, rot=0.2 + i, petal=1 if i % 2 == 0 else 3, centre=3 if i % 2 == 0 else 6)
        leaf(cells, 5, x + 7, 3.6, -0.5); leaf(cells, 9, x - 7, 3.6, 2.6)
    k = karawo(cells, PAL, ground=CREAM, pitch=8, bar=3, seed=9)
    # hem-stitch line along the cloth edges
    save_full(k, f"{OUT}/band.webp", quality=82)
    show(k, "gk-band", bg="#efe7f4")
    clear()

if "divider" in PARTS:
    C, R = 33, 9
    cells = np.full((R, C), -1, np.int32)
    cells[1:R - 1, 1:C - 1] = 0
    flower(cells, 4, 16, 3.8, rot=0.3)
    for x in (7, 25):
        flower(cells, 4, x, 2.4, rot=1.0, petal=3, centre=6)
    leaf(cells, 3, 11, 3, -0.4); leaf(cells, 5, 21, 3, 2.7)
    leaf(cells, 5, 3, 2.6, 0.2); leaf(cells, 3, 29, 2.6, 3.0)
    k = karawo(cells, PAL, ground=CREAM, pitch=8, bar=3, seed=5)
    H, W = k.shape[:2]
    edge = np.ones((H, W), np.float32)
    k[..., 3] *= np.clip(displace(np.pad(np.ones((H - 6, W - 6), np.float32), 3), 2, 1.2, 12) * 1.3, 0, 1)
    save_full(k, f"{OUT}/divider.webp", quality=84)
    show(k, "gk-divider", bg="#f7f1ea")
    clear()

if "dulohupa" in PARTS:
    W, H = 900, 600
    nx = Seq(7000)
    rng = random.Random(21)
    art = blank(W, H)
    # soft hills and a pale lake (Danau Limboto) behind
    hill = shapes(W, H, [[(-20, 400), (140, 330), (300, 350), (470, 300), (650, 340), (820, 310), (930, 340), (930, 460), (-20, 460)]])
    art = G(art, hill, "#b9c9d8", "#c9bedc", seed=nx(), density=0.45, edge=0.55, bloom=0.5, rough=9, feather=2.5)
    lake = shapes(W, H, [[(-20, 440), (930, 432), (930, 500), (-20, 506)]])
    art = G(art, lake, "#bfdcd8", seed=nx(), density=0.35, edge=0.4, bloom=0.5, rough=8)
    lawn = shapes(W, H, [deform([(-20, 520), (200, 498), (450, 504), (700, 496), (930, 512), (930, 600), (-20, 600)], rng, 2, 0.02)])
    art = G(art, lawn, "#a9d1b8", "#8cc0a6", seed=nx(), density=0.6, edge=0.5, bloom=0.4, rough=7)
    cx = 450
    WOOD, WOOD_D, WOOD_L = "#a77c5c", "#6e4a36", "#c9a184"
    TRIM = "#f1e4cf"
    # stilts
    xs = [196, 252, 314, 376, 524, 586, 648, 704]
    st = strokes(W, H, [([(x, 392), (x + rng.uniform(-1, 1), 528)], 12, None) for x in xs])
    art = G(art, st, WOOD_D, seed=nx(), density=0.85, edge=0.6, bloom=0.1, rough=1.5, feather=0.8)
    # body
    body = rect(W, H, 170, 268, 730, 388)
    art = knockout(art, body, 1.0, 1)
    art = G(art, body, WOOD, WOOD_L, seed=nx(), density=0.8, edge=0.55, bloom=0.35, rough=2.5, feather=1)
    planks = strokes(W, H, [([(172, y), (728, y + rng.uniform(-.6, .6))], 1.3, None) for y in range(276, 388, 9)]) * body
    art = G(art, planks, WOOD_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.5)
    beam = rect(W, H, 156, 384, 744, 402)
    art = G(art, beam, WOOD_D, seed=nx(), density=0.9, edge=0.4, bloom=0, rough=1.2, feather=0.8)
    # tall windows with cream frames and lattice (khas Gorontalo: kisi-kisi)
    for x in (200, 270, 340, 520, 590, 660):
        fr = rect(W, H, x - 4, 284, x + 44, 372)
        art = G(art, fr, TRIM, seed=nx(), density=0.95, edge=0.3, bloom=0.1, rough=1, feather=0.6)
        pane = rect(W, H, x + 2, 290, x + 38, 366)
        art = G(art, pane, "#6a5a7a", "#4f4262", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=0.8, feather=0.6)
        lat = strokes(W, H, [([(x + 2, 290 + d), (x + 38, 290 + d + 36)], 1.4, None) for d in range(-36, 76, 10)] + [([(x + 38, 290 + d), (x + 2, 290 + d + 36)], 1.4, None) for d in range(-36, 76, 10)]) * pane
        art = G(art, lat, TRIM, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3, feather=0.4)
    # central veranda (serambi) with railing, door behind
    door = rect(W, H, 410, 286, 490, 388)
    art = G(art, rect(W, H, 402, 278, 498, 388), TRIM, seed=nx(), density=0.95, edge=0.3, bloom=0, rough=1, feather=0.6)
    art = G(art, door, "#8a6fae", "#6f5893", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=1, feather=0.6)
    rail = strokes(W, H, [([(392, 350), (508, 350)], 4, None)] + [([(x, 350), (x, 388)], 2.6, None) for x in range(394, 510, 10)])
    art = G(art, rail, WOOD_L, seed=nx(), density=0.95, edge=0.2, bloom=0, rough=0.5, feather=0.5)
    # tolitihu: two stairs coming down the front to both sides
    for side in (-1, 1):
        top = (cx + side * 70, 402); bot = (cx + side * 190, 530)
        tr = strokes(W, H, [([(top[0] + (bot[0] - top[0]) * t - 12, top[1] + (bot[1] - top[1]) * t), (top[0] + (bot[0] - top[0]) * t + 12, top[1] + (bot[1] - top[1]) * t)], 4, None) for t in np.linspace(0.05, 0.97, 9)])
        art = G(art, tr, WOOD_D, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6, feather=0.5)
        hr = strokes(W, H, [([top, bot], 5, None), ([(top[0], top[1] - 30), (bot[0], bot[1] - 30)], 4, None)] + [([(top[0] + (bot[0] - top[0]) * t, top[1] + (bot[1] - top[1]) * t), (top[0] + (bot[0] - top[0]) * t, top[1] + (bot[1] - top[1]) * t - 30)], 2.4, None) for t in np.linspace(0, 1, 6)])
        art = G(art, hr, WOOD_L, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    # two-tier roof: wide lower skirt + tall pointed upper gable, crossed talapua at the ridge ends
    low = quad(W, H, [(116, 276), (784, 276), (700, 206), (200, 206)])
    up = quad(W, H, [(258, 214), (642, 214), (560, 112), (340, 112)])
    gab = quad(W, H, [(372, 214), (528, 214), (450, 84)])
    ROOF, ROOF_D = "#7d6a8f", "#5d4d70"
    for m in (low, up):
        art = knockout(art, m, 1.0, 1)
        art = G(art, m, ROOF, ROOF_D, seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=2.5, feather=1)
    ribs = strokes(W, H, [([(x, 208), (x + (x - 450) * 0.17, 274)], 1.3, None) for x in range(206, 698, 10)] + [([(x, 114), (x + (x - 450) * 0.35, 212)], 1.3, None) for x in range(344, 560, 9)]) * np.clip(low + up, 0, 1)
    art = G(art, ribs, "#3f3352", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4, feather=0.5)
    art = knockout(art, gab, 1.0, 1)
    art = G(art, gab, TRIM, "#efe3d0", seed=nx(), density=0.95, edge=0.4, bloom=0.2, rough=1.2, feather=0.7)
    sun = strokes(W, H, [([(450, 206), (450 + t * 64, 132 + abs(t) * 70)], 2.2, None) for t in np.linspace(-1, 1, 9)]) * gab
    art = G(art, sun, "#9fcfbf", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4, feather=0.5)
    dot = circles(W, H, [(450, 168, 9)])
    art = G(art, dot, "#e8a3a0", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5, feather=0.5)
    fas = strokes(W, H, [([(366, 218), (450, 80), (534, 218)], 6, None), ([(112, 278), (788, 278)], 5, None), ([(254, 216), (646, 216)], 4, None)])
    art = G(art, fas, TRIM, seed=nx(), density=0.95, edge=0.25, bloom=0, rough=0.6, feather=0.5)
    tal = strokes(W, H, [([(450, 84), (424, 46)], 5, (0.0, 0.6)), ([(450, 84), (476, 46)], 5, (0.0, 0.6))])
    art = G(art, tal, WOOD_D, seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6, feather=0.5)
    # soft shade on the right, warm light left
    yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
    house = np.clip(body + low + up + beam, 0, 1)
    art = G(art, house * np.clip((xx_ - 480) / 280, 0, 1) * 0.9, "#5a4470", seed=nx(), density=0.35, edge=0.05, bloom=0.4, rough=3, feather=8)
    art = G(art, rect(W, H, 170, 402, 730, 440) * np.clip(1 - (yy_ - 402) / 40, 0, 1), "#4a3a5c", seed=nx(), density=0.3, edge=0.1, bloom=0.3, rough=3, feather=6)
    # bougainvillea & hibiscus shrubs
    shrubs = [(110, 520, 56), (170, 540, 38), (790, 516, 58), (740, 540, 40)]
    sm = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 0.6, 14), rng, 2, 0.06) for x, y, r in shrubs])
    art = G(art, sm, "#7fb59e", "#5c9a86", seed=nx(), density=0.8, edge=0.6, bloom=0.4, rough=4)
    fl = [(x + rng.uniform(-r, r) * 0.9, y + rng.uniform(-r * 0.5, r * 0.3), rng.uniform(4, 7)) for x, y, r in shrubs for _ in range(10)]
    art = G(art, circles(W, H, fl[::2]) * sm, "#e8a3a0", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.5, feather=0.8)
    art = G(art, circles(W, H, fl[1::2]) * sm, "#c7a6e0", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.5, feather=0.8)
    art = add_grain(art, 4, 0.025)
    save(art, f"{OUT}/dulohupa.webp", max_w=820, quality=76)
    show(art, "gk-dulohupa", tone="#f8f1e8")
    clear()
