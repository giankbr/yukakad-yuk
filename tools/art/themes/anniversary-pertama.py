"""Anniversary Pertama — first wedding anniversary (paper anniversary): a kraft envelope opened (back + front pocket with a
coral wax seal), cut-paper roses, folded origami hearts, a strip of washi tape, a thread garland of paper hearts.
Cut-paper medium. Run: python3 -I anniversary-pertama.py [part ...]
parts: envelope flowers hearts tape garland"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q4_lib import *

OUT = outdir("anniversary-pertama")
PARTS = sys.argv[1:] or ["envelope", "flowers", "hearts", "tape", "garland"]
KRAFT, KRAFT_D, KRAFT_L = "#c39a6b", "#9a7148", "#d9b88e"
CORAL, CORAL_D, CORAL_L = "#d66f60", "#a84a40", "#eea08f"
BLUSH, CREAM, INK = "#f2c9bf", "#f8efe2", "#2d3a5c"
SAGE, SAGE_D = "#9bb08a", "#6a8460"


def origami_heart(W, H, ox, oy, s, rot=0.0):
    """Facet polygons of a folded origami heart, centred at (ox,oy), size s (~ width/2). Returns (light, dark, tips, outline)."""
    def P(x, y):
        x, y = (x - 100) / 90 * s, (y - 110) / 90 * s
        c, sn = math.cos(rot), math.sin(rot)
        return (ox + x * c - y * sn, oy + x * sn + y * c)
    left = [P(100, 196), P(8, 104), P(8, 62), P(30, 40), P(64, 40), P(100, 72)]
    right = [P(100, 196), P(100, 72), P(136, 40), P(170, 40), P(192, 62), P(192, 104)]
    tipL = [P(8, 62), P(30, 40), P(36, 66)]
    tipR = [P(192, 62), P(170, 40), P(164, 66)]
    midL = [P(64, 40), P(100, 72), P(80, 74)]
    midR = [P(136, 40), P(100, 72), P(120, 74)]
    return left, right, tipL + [], tipR, midL, midR


def paint_heart(art, W, H, ox, oy, s, rot, col, dark, light, nx, shadow_=True):
    left, right, tipL, tipR, midL, midR = origami_heart(W, H, ox, oy, s, rot)
    whole = shapes(W, H, [left, right], smooth=False)
    if shadow_:
        art = shadow(art, whole, "#5a3a2a", blur=s * 0.08, strength=0.32, dx=int(s * 0.05), dy=int(s * 0.09))
    art = CP(art, shapes(W, H, [left], smooth=False), mix(col, light, 0.25), col, seed=nx(), edge_light=0.25, rough=0.8)
    art = CP(art, shapes(W, H, [right], smooth=False), col, dark, seed=nx(), edge_light=0.2, rough=0.8)
    for tri, c in ((tipL, light), (tipR, mix(col, light, 0.5)), (midL, mix(col, dark, 0.35)), (midR, dark)):
        art = CP(art, shapes(W, H, [tri], smooth=False), c, seed=nx(), edge_light=0.3, rough=0.5)
    # centre fold crease
    crease = lines(W, H, [(left[0], left[-1])], max(1.0, s * 0.012))
    art = T(art, crease, dark, 0.5)
    return art


def paper_rose(art, W, H, cx, cy, r, col, dark, light, rng, nx):
    """Cut-paper rose: rings of curled petals (crescents) from outside in, each with shadow + lit cut edge."""
    for ring_i, (rr, n) in enumerate([(1.0, 7), (0.74, 6), (0.5, 5), (0.3, 4)]):
        tone = mix(col, light if ring_i % 2 else dark, 0.15 + ring_i * 0.08)
        for k in range(n):
            a = k * math.tau / n + ring_i * 0.6 + rng.uniform(-0.2, 0.2)
            px, py = cx + math.cos(a) * r * rr * 0.42, cy + math.sin(a) * r * rr * 0.42 * 0.9
            pet = shape_mask(W, H, deform(ellipse_pts(px, py, r * rr * 0.6, r * rr * 0.44, 12, a), rng, 1, 0.06))
            art = shadow(art, pet, "#4a2018", blur=max(2, r * 0.05), strength=0.28, dx=1, dy=2)
            art = CP(art, pet, tone, mix(tone, dark, 0.3), seed=nx(), edge_light=0.45, rough=0.6)
    spiral = stroke_mask(W, H, jw.spiral_pts(cx, cy, r * 0.05, r * 0.24, 0, 1.4, 40, 1), max(1.4, r * 0.05))
    return T(art, spiral, dark, 0.55, 0.4)


def paper_leaf(art, W, H, x, y, L, ang, rng, nx):
    m = shape_mask(W, H, petal_pts(x, y, L, L * 0.42, ang, n=14))
    art = shadow(art, m, "#3a3020", blur=3, strength=0.25, dx=2, dy=3)
    art = CP(art, m, SAGE, SAGE_D, seed=nx(), edge_light=0.35, rough=0.6)
    p0 = (x, y); p1 = (x + math.cos(ang) * L, y + math.sin(ang) * L)
    art = T(art, fold_shade(m, p0, p1, 1.0, 1.0), SAGE_D, 0.35)
    return T(art, lines(W, H, [(p0, p1)], 1.2) * m, "#5a7250", 0.6)


if "envelope" in PARTS:
    W, H = 800, 600
    nx = Seq(50100)
    rng = random.Random(5)
    # back half: inner panel (with liner paper) + open flap pointing up
    back = blank(W, H)
    body = rect(W, H, 40, 230, 760, 580, 6)
    flap = shapes(W, H, [[(40, 232), (400, 24), (760, 232)]], smooth=False)
    back = shadow(back, np.maximum(body, flap), "#4a3020", blur=10, strength=0.3, dx=0, dy=10)
    back = CP(back, np.maximum(body, flap), KRAFT, KRAFT_D, seed=nx(), edge_light=0.3, rough=0.8)
    liner = np.maximum(shapes(W, H, [[(70, 226), (400, 50), (730, 226)]], smooth=False), rect(W, H, 64, 250, 736, 560, 3))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dots = ((np.sin(xx * 0.31) * np.sin(yy * 0.31)) > 0.86).astype(np.float32)
    back = CP(back, liner, BLUSH, "#ecbcb0", seed=nx(), edge_light=0.1, rough=0.4)
    back = T(back, gaussian_filter(dots, 0.7) * liner, CORAL, 0.55)
    back = T(back, fold_shade(body, (40, 232), (760, 232), 1.0, 2.0) * 0 + np.clip(gaussian_filter(rect(W, H, 40, 222, 760, 242), 4) - 0.3, 0, 1) * body, "#6a4a30", 0.35)
    preview(back, "an-envback", tone=CREAM)
    save_full(back, f"{OUT}/envback.webp", size=(400, 300), quality=82)
    clear()
    # front pocket: side flaps + bottom flap, a coral wax seal
    front = blank(W, H)
    sideL = shapes(W, H, [[(40, 236), (420, 424), (40, 580)]], smooth=False)
    sideR = shapes(W, H, [[(760, 236), (380, 424), (760, 580)]], smooth=False)
    bottom = shapes(W, H, [[(40, 580), (400, 356), (760, 580)]], smooth=False)
    front = CP(front, sideL, mix(KRAFT, KRAFT_L, 0.3), KRAFT, seed=nx(), edge_light=0.3, rough=0.6)
    front = CP(front, sideR, KRAFT, KRAFT_D, seed=nx(), edge_light=0.25, rough=0.6)
    front = shadow(front, bottom, "#4a3020", blur=8, strength=0.35, dx=0, dy=-6)
    front = CP(front, bottom, KRAFT_L, KRAFT, seed=nx(), edge_light=0.4, rough=0.6)
    # wax seal
    blob = shape_mask(W, H, deform(ellipse_pts(400, 400, 50, 48, 18), rng, 2, 0.1))
    front = shadow(front, blob, "#3a1a10", blur=5, strength=0.45, dx=2, dy=5)
    front = SH(front, blob, CORAL_D, "#f0a090", "#6a2018", 400, 400, 50, 48, nx(), light=(-0.5, -0.6), spec=0.35, rough=1.2)
    inner = circles(W, H, [(400, 400, 32)])
    front = T(front, outline(inner, 3) * blob, "#5a1a12", 0.45)
    hl, hr, *_ = origami_heart(W, H, 400, 404, 20)
    hm = shapes(W, H, [hl, hr], smooth=False)
    front = SH(front, hm, "#b24c40", "#f6b0a0", "#6a2018", 396, 396, 24, 24, nx(), light=(-0.4, -0.7), spec=0.2, rough=0.4)
    # twine across the pocket
    tw = strokes(W, H, [(curve([(40, 470), (220, 460), (360, 420)], 20), 3.5, None), (curve([(440, 420), (600, 462), (760, 476)], 20), 3.5, None)])
    front = GP(front, tw, "#e8dcc6", "#b9a888", seed=nx(), rough=0.4, streak=1.4)
    preview(front, "an-envfront", tone=CREAM)
    save_full(front, f"{OUT}/envfront.webp", size=(400, 300), quality=82)
    clear()

if "flowers" in PARTS:
    W, H = 640, 460
    nx = Seq(50500)
    rng = random.Random(8)
    art = blank(W, H)
    for (x, y, L, a) in [(150, 300, 120, 2.6), (210, 220, 110, -2.3), (470, 210, 120, -0.6), (520, 320, 110, 0.4), (330, 360, 100, 1.7), (390, 150, 90, -1.3)]:
        art = paper_leaf(art, W, H, x, y, L, a, rng, nx)
    clear()
    for (x, y, r, c, d, l) in [(250, 260, 112, CORAL, CORAL_D, CORAL_L), (420, 250, 96, BLUSH, "#d8988a", CREAM), (340, 170, 70, CREAM, "#d8c6a8", "#fffaf0"), (170, 330, 62, "#e8a24a", "#b8762a", "#f6cc84")]:
        art = paper_rose(art, W, H, x, y, r, c, d, l, rng, nx)
        clear()
    # small paper buds / berries
    for (x, y) in [(500, 360), (520, 380), (110, 230)]:
        b = circles(W, H, [(x, y, 12)])
        art = shadow(art, b, "#4a2018", blur=2, strength=0.3, dx=1, dy=2)
        art = CP(art, b, CORAL_L, CORAL, seed=nx(), edge_light=0.4)
    preview(art, "an-flowers", tone=CREAM)
    save(art, f"{OUT}/flowers.webp", max_w=400, quality=82)

if "hearts" in PARTS:
    for name, col, dark, light, rot in [("heart", CORAL, CORAL_D, CORAL_L, -0.18), ("heart2", BLUSH, "#cf8f82", CREAM, 0.22), ("heart3", INK, "#1c2440", "#5a6a94", 0.08)]:
        W, H = 260, 260
        nx = Seq(50900 + len(name) * 10 + int(rot * 100))
        art = paint_heart(blank(W, H), W, H, 130, 120, 100, rot, col, dark, light, nx)
        preview(art, f"an-{name}", tone=CREAM)
        save(art, f"{OUT}/{name}.webp", max_w=120, quality=84)

if "tape" in PARTS:
    W, H = 300, 90
    nx = Seq(51300)
    rng = random.Random(2)
    top = [(10 + x, 18 + rng.uniform(-2, 2)) for x in range(0, 281, 20)]
    bot = [(290 - x, 72 + rng.uniform(-2, 2)) for x in range(0, 281, 20)]
    ends = [(290 + rng.uniform(-4, 4), 18 + k * 6) for k in range(10)][::-1]
    m = shapes(W, H, [top + [(296, 30), (288, 45), (298, 60)] + bot + [(4, 60), (14, 46), (4, 30)]], smooth=False)
    art = CP(blank(W, H), m, "#e9b8a8", "#dca290", seed=nx(), edge_light=0.2, rough=0.4)
    art[..., 3] *= 0.82
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    stripes = ((np.sin((xx + yy) * 0.22) > 0.55)).astype(np.float32)
    art = T(art, gaussian_filter(stripes, 0.6) * m, CREAM, 0.55)
    preview(art, "an-tape", tone=CREAM)
    save(art, f"{OUT}/tape.webp", max_w=150, quality=84)

if "garland" in PARTS:
    W, H = 720, 150
    nx = Seq(51500)
    art = blank(W, H)
    thread = stroke_mask(W, H, curve([(10, 30), (180, 70), (360, 84), (540, 70), (710, 30)], 80), 2.0)
    art = T(art, thread, "#9a7f62", 0.85)
    for (x, y, c, d, l, r) in [(200, 74, CORAL, CORAL_D, CORAL_L, -0.15), (360, 86, BLUSH, "#cf8f82", CREAM, 0.0), (520, 74, CORAL, CORAL_D, CORAL_L, 0.15)]:
        art = T(art, lines(W, H, [((x, y - 2), (x, y + 8))], 1.4), "#9a7f62", 0.8)
        art = paint_heart(art, W, H, x, y + 26, 22 if x != 360 else 26, r, c, d, l, nx)
    preview(art, "an-garland", tone=CREAM)
    save(art, f"{OUT}/garland.webp", max_w=360, quality=84)
