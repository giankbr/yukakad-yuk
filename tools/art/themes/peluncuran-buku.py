"""Peluncuran Buku — modern editorial gouache for a book launch & discussion: a stack of hardbacks with a fountain pen,
a talk stage (two armchairs, side table with water glasses, standing mic, a poster of the book on the backdrop, a tall
plant, empty front-row chairs), a lone fountain pen, an open book and a warm paper tile. Limited palette: ink navy,
terracotta, mustard, sage on warm paper; matte paint with hand-cut edges and soft shading from the top-left.
Run: python3 -I peluncuran-buku.py [part ...]  parts: books stage pen open paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h4_lib import *  # noqa

OUT = outdir("peluncuran-buku")
PARTS = sys.argv[1:] or ["books", "stage", "pen", "open", "paper"]
NAVY, NAVY_D, TERRA, TERRA_D, MUST, MUST_D, SAGE, SAGE_D = "#22304d", "#141d33", "#c4573a", "#93391f", "#e0a73a", "#b07a1f", "#86a183", "#56735a"
CREAM, CREAM_D, PAPER, WOOD, WOOD_D, GOLD = "#f3e9d6", "#d9c8a8", "#f4ede1", "#b9824c", "#8a5a30", "#d6ae5a"


def poly(W, H, pts):
    return shape_mask(W, H, pts, smooth=False)


def rrect(W, H, x0, y0, x1, y1, r, rot=0.0, cx=None, cy=None):
    def draw(cv):
        cv.c.save()
        if rot:
            cv.c.rotate(math.degrees(rot), cx if cx is not None else (x0 + x1) / 2, cy if cy is not None else (y0 + y1) / 2)
        cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        cv.c.restore()
    return mask_from(W, H, draw)


def paint(art, m, col, col2=None, seed=1, shade=0.45, dark=None, light_dx=-6, rough=1.4):
    art = GP(art, m, col, col2 or col, seed=seed, rough=rough, streak=0.7)
    if shade:
        art = tint(art, side_light(m, light_dx, light_dx, 4) * m, dark or NAVY_D, shade * 0.6, seed=seed + 1)
    return art


def pen(art, W, H, x, y, L, ang, seed=1, body=NAVY, cap_col=NAVY_D):
    """Fountain pen lying at angle: nib (gold) at (x, y) pointing toward -ang direction."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (x + u * ca - v * sa, y + u * sa + v * ca)
    r = L * 0.055
    nib = poly(W, H, [P(0, 0), P(L * 0.12, -r * 0.8), P(L * 0.16, -r * 0.85), P(L * 0.16, r * 0.85), P(L * 0.12, r * 0.8)])
    art = paint(art, nib, GOLD, "#f0d28a", seed=seed, shade=0.5, dark="#7a5a20", rough=0.6)
    slit = strokes(W, H, [([P(L * 0.015, 0), P(L * 0.1, 0)], max(1.0, r * 0.12), None)])
    art = OV(art, slit, lambda m: col_arr(m, "#5a4012", m * 0.9), pad=4)
    art = OV(art, circles(W, H, [(*P(L * 0.1, 0), r * 0.18)]), lambda m: col_arr(m, "#5a4012", m), pad=4)
    grip = poly(W, H, [P(L * 0.155, -r * 0.9), P(L * 0.3, -r), P(L * 0.3, r), P(L * 0.155, r * 0.9)])
    art = paint(art, grip, "#2b2b31", seed=seed + 2, shade=0.5, rough=0.6)
    ring = poly(W, H, [P(L * 0.3, -r * 1.05), P(L * 0.33, -r * 1.05), P(L * 0.33, r * 1.05), P(L * 0.3, r * 1.05)])
    art = paint(art, ring, GOLD, seed=seed + 3, shade=0.3, rough=0.4)
    barrel = rrect(W, H, x + L * 0.33, y - r * 1.05, x + L * 1.0, y + r * 1.05, r, rot=ang, cx=x, cy=y)
    art = paint(art, barrel, body, seed=seed + 4, shade=0.55, rough=0.6)
    # cap posted over the end with a clip
    cap = rrect(W, H, x + L * 0.62, y - r * 1.15, x + L * 1.02, y + r * 1.15, r * 1.1, rot=ang, cx=x, cy=y)
    art = paint(art, cap, cap_col, seed=seed + 5, shade=0.5, rough=0.6)
    band = poly(W, H, [P(L * 0.62, -r * 1.16), P(L * 0.66, -r * 1.16), P(L * 0.66, r * 1.16), P(L * 0.62, r * 1.16)])
    art = paint(art, band, GOLD, seed=seed + 6, shade=0.3, rough=0.4)
    clip = strokes(W, H, [([P(L * 0.66, -r * 1.3), P(L * 0.95, -r * 1.3)], r * 0.45, (0.0, 0.2))])
    art = paint(art, clip, GOLD, seed=seed + 7, shade=0.2, rough=0.4)
    hi = strokes(W, H, [([P(L * 0.36, -r * 0.45), P(L * 0.6, -r * 0.45)], r * 0.32), ([P(L * 0.68, -r * 0.5), P(L * 0.98, -r * 0.5)], r * 0.3)])
    art = OV(art, hi, lambda m: col_arr(m, "#ffffff", gaussian_filter(m, 1.2) * 0.35), pad=4)
    return art


def book(art, W, H, x0, y0, w, h, rot, col, band, seed, pages_right=True, label=None):
    """A hardback lying flat, seen from the spine side: spine block, two bands, a label, page edge at one end."""
    cx, cy = x0 + w / 2, y0 + h / 2
    spine = rrect(W, H, x0, y0, x0 + w, y0 + h, h * 0.18, rot=rot, cx=cx, cy=cy)
    art = paint(art, spine, col, seed=seed, shade=0.5, rough=1.0)
    art = tint(art, rrect(W, H, x0 + 4, y0 + 2, x0 + w - 4, y0 + h * 0.28, h * 0.1, rot=rot, cx=cx, cy=cy) * spine, "#ffffff", 0.14, seed=seed + 1)
    for bx in (x0 + w * 0.08, x0 + w * 0.86):
        art = paint(art, rrect(W, H, bx, y0 + 1, bx + w * 0.045, y0 + h - 1, 1, rot=rot, cx=cx, cy=cy) * spine, band, seed=seed + 2, shade=0.2, rough=0.5)
    if label:
        lab = rrect(W, H, x0 + w * 0.3, y0 + h * 0.3, x0 + w * 0.66, y0 + h * 0.7, 2, rot=rot, cx=cx, cy=cy)
        art = paint(art, lab, label, seed=seed + 3, shade=0.15, rough=0.5)
        lines = [([rot_pts([(x0 + w * 0.34, y0 + h * (0.44 + k * 0.14)), (x0 + w * (0.6 - k * 0.08), y0 + h * (0.44 + k * 0.14))], cx, cy, rot)][0], 1.6, None) for k in range(2)]
        art = OV(art, strokes(W, H, lines) * lab, lambda m: col_arr(m, NAVY_D, m * 0.55), pad=3)
    return art


if "books" in PARTS:
    W, H = 560, 600
    art = blank(W, H)
    rng = random.Random(3)
    specs = [  # x0, y0, w, h, rot(deg), col, band, label
        (70, 520, 420, 58, -1.0, NAVY, GOLD, CREAM),
        (96, 466, 372, 52, 1.5, TERRA, CREAM, None),
        (60, 418, 400, 46, -2.0, SAGE, NAVY_D, CREAM),
        (110, 372, 350, 44, 2.2, MUST, TERRA_D, None),
        (84, 326, 382, 44, -0.8, CREAM_D, TERRA, NAVY),
        (128, 278, 330, 46, 1.2, NAVY_D, MUST, None),
    ]
    # soft cast shadow on the table
    sh = rrect(W, H, 70, 566, 520, 590, 12)
    art = OV(art, gaussian_filter(sh, 9), lambda m: col_arr(m, "#3a2a20", m * 0.35), pad=0)
    for k, (x0, y0, w, h, rd, col, band, lab) in enumerate(specs):
        # page block visible on the right end
        cx, cy = x0 + w / 2, y0 + h / 2
        pg = rrect(W, H, x0 + w - 30, y0 + h * 0.1, x0 + w + 8, y0 + h * 0.9, 3, rot=math.radians(rd), cx=cx, cy=cy)
        art = paint(art, pg, CREAM, seed=40 + k, shade=0.25, rough=0.6)
        lines = []
        for j in range(5):
            yy_ = y0 + h * (0.2 + j * 0.15)
            lines.append((rot_pts([(x0 + w - 26, yy_), (x0 + w + 6, yy_)], cx, cy, math.radians(rd)), 0.9, None))
        art = OV(art, strokes(W, H, lines) * pg, lambda m: col_arr(m, CREAM_D, m * 0.9), pad=2)
        art = book(art, W, H, x0, y0, w - 18, h, math.radians(rd), col, band, 10 + k * 7, label=lab)
    # ribbon bookmark hanging from the top book
    rib = strokes(W, H, [([(412, 300), (414, 336), (410, 372), (416, 404)], 7, (0.0, 0.0))])
    art = paint(art, rib, TERRA, seed=90, shade=0.3, rough=0.5)
    art = pen(art, W, H, 120, 268, 380, math.radians(-6), seed=95)
    preview(art, "pb-books", tone=PAPER)
    save(art, f"{OUT}/books.webp", max_w=480, quality=84)
    clear()

if "pen" in PARTS:
    W, H = 520, 90
    art = pen(blank(W, H), W, H, 20, 45, 480, 0.0, seed=7)
    preview(art, "pb-pen", tone=PAPER)
    save(art, f"{OUT}/pen.webp", max_w=260, quality=84)
    clear()

if "open" in PARTS:
    W, H = 420, 240
    art = blank(W, H)
    art = OV(art, gaussian_filter(rrect(W, H, 30, 200, 390, 222, 10), 7), lambda m: col_arr(m, "#3a2a20", m * 0.3), pad=0)
    cover = poly(W, H, [(24, 70), (210, 92), (396, 70), (404, 206), (210, 222), (16, 206)])
    art = paint(art, cover, TERRA, seed=2, shade=0.3, rough=1.0)
    for side in (-1, 1):
        for k in range(3):
            o = k * 5
            pts = [(210, 100 + o * 0.2), (210 + side * 30, 74 + o), (210 + side * 100, 60 + o), (210 + side * (176 - o), 62 + o * 1.2), (210 + side * (180 - o), 196 - o * 0.4), (210 + side * 100, 200), (210 + side * 30, 206), (210, 216 - o * 0.4)]
            pg = shape_mask(W, H, pts, smooth=False)
            art = paint(art, pg, CREAM if k == 2 else CREAM_D, seed=4 + k + (side + 1) * 5, shade=0.18, rough=0.8)
        lines = [([(210 + side * 40, 92 + j * 12), (210 + side * 150, 86 + j * 12)], 1.4, None) for j in range(8)]
        art = OV(art, strokes(W, H, lines), lambda m: col_arr(m, "#9a8a70", m * 0.55), pad=3)
    gut = strokes(W, H, [([(210, 70), (210, 214)], 3, None)])
    art = OV(art, gaussian_filter(gut, 2), lambda m: col_arr(m, "#8a7a60", m * 0.6), pad=3)
    preview(art, "pb-open", tone=PAPER)
    save(art, f"{OUT}/open.webp", max_w=240, quality=84)
    clear()


def chair(art, W, H, cx, base, s, col, col_d, flip, seed):
    """Low modern armchair, 3/4 view, facing the centre (flip=1 faces right)."""
    f = flip
    def X(u):
        return cx + u * s * f
    back = shape_mask(W, H, [(X(-0.62), base - 1.5 * s), (X(-0.2), base - 1.62 * s), (X(0.02), base - 1.4 * s), (X(0.05), base - 0.55 * s), (X(-0.6), base - 0.5 * s)], smooth=True)
    art = paint(art, back, col_d, col, seed=seed, shade=0.35, light_dx=-6 * f)
    seat = shape_mask(W, H, [(X(-0.62), base - 0.62 * s), (X(0.55), base - 0.7 * s), (X(0.7), base - 0.42 * s), (X(-0.5), base - 0.3 * s)], smooth=True)
    art = paint(art, seat, col, seed=seed + 2, shade=0.3)
    arm = shape_mask(W, H, [(X(0.38), base - 0.95 * s), (X(0.72), base - 0.9 * s), (X(0.76), base - 0.42 * s), (X(0.42), base - 0.44 * s)], smooth=True)
    art = paint(art, arm, col_d, col, seed=seed + 4, shade=0.4)
    legs = strokes(W, H, [([(X(-0.45), base - 0.32 * s), (X(-0.5), base)], s * 0.05), ([(X(0.62), base - 0.42 * s), (X(0.68), base - 0.02 * s)], s * 0.05),
                          ([(X(0.1), base - 0.34 * s), (X(0.12), base + 0.02 * s)], s * 0.045)])
    art = paint(art, legs, NAVY_D, seed=seed + 6, shade=0.0, rough=0.5)
    # cushion seam highlight
    art = OV(art, strokes(W, H, [([(X(-0.5), base - 0.55 * s), (X(0.5), base - 0.62 * s)], s * 0.03)]), lambda m: col_arr(m, "#ffffff", gaussian_filter(m, 1.5) * 0.25), pad=4)
    return art


if "stage" in PARTS:
    W, H = 820, 600
    art = blank(W, H)
    rng = random.Random(9)
    # backdrop panel and the book poster on it
    panel = rrect(W, H, 120, 20, 700, 380, 6)
    art = paint(art, panel, NAVY, "#2b3a5c", seed=1, shade=0.0, rough=1.2)
    art = tint(art, side_light(panel, 30, 30, 30) * panel, NAVY_D, 0.4, seed=2)
    poster = rrect(W, H, 300, 56, 520, 338, 3)
    art = paint(art, poster, TERRA, seed=3, shade=0.3, rough=0.8)
    art = paint(art, circles(W, H, [(410, 150, 56)]), MUST, seed=4, shade=0.2, rough=0.8)
    art = paint(art, rrect(W, H, 330, 236, 490, 250, 3), CREAM, seed=5, shade=0.0, rough=0.5)
    art = paint(art, rrect(W, H, 352, 262, 468, 272, 3), CREAM, seed=6, shade=0.0, rough=0.5)
    art = paint(art, rrect(W, H, 380, 300, 440, 307, 2), MUST, seed=7, shade=0.0, rough=0.4)
    # small bunting of book jackets left/right on the panel
    for k, (x, col) in enumerate([(160, SAGE), (212, MUST), (590, CREAM_D), (642, SAGE)]):
        art = paint(art, rrect(W, H, x, 90 + (k % 2) * 16, x + 36, 140 + (k % 2) * 16, 2), col, seed=10 + k, shade=0.2, rough=0.5)
    # warm spot glow over the chairs
    art = over(art, glow(circles(W, H, [(410, 300, 150)]), "#ffd99a", radius=60, strength=0.32))
    # platform
    top = poly(W, H, [(70, 404), (750, 404), (784, 444), (36, 444)])
    front = poly(W, H, [(36, 444), (784, 444), (784, 478), (36, 478)])
    art = paint(art, front, WOOD_D, seed=20, shade=0.0, rough=0.8)
    art = paint(art, top, WOOD, "#c99460", seed=21, shade=0.0, rough=0.8)
    planks = [([(70 + k * 34 - (k * 34 - 340) * 0.05, 404), (36 + k * 37.5, 444)], 1.2, None) for k in range(1, 20)]
    art = OV(art, strokes(W, H, planks) * top, lambda m: col_arr(m, WOOD_D, m * 0.45), pad=0)
    # chairs, table, mic, plant
    art = chair(art, W, H, 278, 432, 110, MUST, MUST_D, 1, 30)
    art = chair(art, W, H, 548, 432, 110, SAGE, SAGE_D, -1, 40)
    tbl_top = shapes(W, H, [ellipse_pts(413, 346, 52, 12, 24)])
    art = paint(art, strokes(W, H, [([(413, 350), (413, 428)], 6)]), NAVY_D, seed=50, shade=0.0, rough=0.4)
    art = paint(art, shapes(W, H, [ellipse_pts(413, 430, 30, 6, 20)]), NAVY_D, seed=51, shade=0.0, rough=0.4)
    art = paint(art, tbl_top, CREAM, CREAM_D, seed=52, shade=0.3, rough=0.6)
    for gx in (396, 430):
        g = rrect(W, H, gx - 7, 314, gx + 7, 344, 2)
        art = OV(art, g, lambda m: col_arr(m, "#cfe2e6", m * 0.55), pad=3)
        art = OV(art, rrect(W, H, gx - 6, 326, gx + 6, 343, 2), lambda m: col_arr(m, "#9cc3cc", m * 0.5), pad=3)
        art = OV(art, strokes(W, H, [([(gx - 4, 316), (gx - 4, 340)], 1.5)]), lambda m: col_arr(m, "#ffffff", m * 0.7), pad=3)
    art = paint(art, rrect(W, H, 404, 334, 446, 342, 1.5), TERRA, seed=53, shade=0.2, rough=0.4)
    # standing mic (front left)
    art = paint(art, strokes(W, H, [([(150, 438), (150, 268)], 5)]), "#a9adb5", seed=60, shade=0.0, rough=0.3)
    art = OV(art, strokes(W, H, [([(149, 436), (149, 272)], 1.6)]), lambda m: col_arr(m, "#ffffff", m * 0.5), pad=3)
    art = paint(art, strokes(W, H, [([(150, 438), (128, 452)], 4), ([(150, 438), (172, 452)], 4), ([(150, 438), (150, 454)], 4)]), NAVY_D, seed=61, shade=0.0, rough=0.3)
    art = paint(art, strokes(W, H, [([(150, 272), (172, 250)], 4)]), "#a9adb5", seed=62, shade=0.0, rough=0.3)
    mic = rrect(W, H, 168, 226, 182, 258, 7, rot=math.radians(45), cx=176, cy=246)
    art = paint(art, mic, "#3b3f4a", seed=63, shade=0.4, rough=0.4)
    art = tint(art, mic * (np.mgrid[0:H, 0:W][0] < 244), "#9aa0aa", 0.5, seed=64)
    cable = curve([(150, 300), (138, 360), (146, 420), (180, 446), (240, 450)], 60)
    art = paint(art, strokes(W, H, [(cable, 2.2, None)]), NAVY_D, seed=65, shade=0.0, rough=0.2)
    # plant in a terracotta pot (right)
    potm = poly(W, H, [(676, 360), (736, 360), (728, 432), (684, 432)])
    art = paint(art, potm, TERRA, TERRA_D, seed=70, shade=0.45, rough=0.8)
    blades = []
    for k in range(9):
        a = math.radians(-90 + rng.uniform(-38, 38))
        L = rng.uniform(110, 200)
        bx = 706 + rng.uniform(-14, 14)
        mid = (bx + math.cos(a) * L * 0.5 + rng.uniform(-10, 10), 360 + math.sin(a) * L * 0.5)
        end = (bx + math.cos(a) * L, 360 + math.sin(a) * L)
        blades.append(([(bx, 362), mid, end], rng.uniform(13, 19), (0.05, 0.6)))
    bm = strokes(W, H, [(curve(p, 24), w, t) for p, w, t in blades])
    art = paint(art, bm, SAGE_D, SAGE, seed=71, shade=0.4, rough=1.0)
    art = OV(art, strokes(W, H, [(curve(p, 24), 1.4, (0.1, 0.5)) for p, w, t in blades]) * bm, lambda m: col_arr(m, "#c9dcb8", m * 0.5), pad=3)
    # empty front-row chairs (backs), cropped by the bottom edge
    for k, x in enumerate([60, 200, 340, 480, 620, 760]):
        back = rrect(W, H, x - 52, 512, x + 52, 600, 16)
        art = paint(art, back, NAVY_D if k % 2 else NAVY, seed=80 + k, shade=0.3, rough=0.8)
        art = OV(art, rrect(W, H, x - 40, 520, x + 40, 528, 4), lambda m: col_arr(m, "#ffffff", m * 0.12), pad=3)
    art = add_grain(art, 3, 0.03)
    preview(art, "pb-stage", tone=PAPER)
    save(art, f"{OUT}/stage.webp", max_w=780, quality=82)
    clear()

if "paper" in PARTS:
    p = paper(256, 256, PAPER, seed=5, fiber=0.5, mottle=0.35)
    save_texture(p.convert("RGB") if hasattr(p, "convert") else p, f"{OUT}/paper.webp", quality=74)
