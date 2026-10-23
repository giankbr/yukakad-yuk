"""Line Art — one continuous brush-pen line drawing of a couple (profiles, eyes closed, no other features), a loose
cobalt watercolour blob behind them, and single-line flower sprigs. Ink on transparent; the page is the paper.
Run: python3 -I line-art.py [part ...]   parts: pasangan ranting bunga"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o3_lib import *

OUT = outdir("line-art")
PARTS = sys.argv[1:] or ["pasangan", "ranting", "bunga"]
INK = "#1d1b19"
ACC, ACC_L = "#3150c4", "#7d93e3"


def pen(t):
    """Pressure: lighter at the start/end of the stroke, a few heavier passages."""
    return (0.35 + 0.65 * min(1, t * 12) * min(1, (1 - t) * 10)) * (0.75 + 0.25 * math.sin(t * 37))


COUPLE = [
    # her shoulder and back, nape
    (40, 760), (80, 660), (140, 582), (196, 540), (214, 500), (212, 452),
    # back of head, the bun loop at the crown
    (196, 410), (178, 362), (174, 314), (176, 286), (152, 270), (138, 240), (152, 212), (184, 204), (204, 226), (196, 250), (176, 250), (172, 232), (190, 218),
    # crown, forehead
    (214, 196), (250, 174), (292, 172), (322, 194), (338, 230),
    # brow, nose, lips, chin
    (340, 260), (338, 282), (354, 308), (340, 318), (344, 332), (336, 340), (342, 352), (334, 372), (312, 388),
    # throat, chest, the shared dip between them
    (306, 422), (312, 470), (334, 520), (356, 558), (372, 572),
    # his chest up to the throat
    (392, 554), (410, 506), (418, 456), (416, 414),
    # his chin, lips, nose, brow, forehead (a little higher than hers)
    (402, 392), (386, 380), (380, 364), (388, 354), (380, 344), (386, 332), (368, 300), (380, 278), (378, 250), (380, 222),
    # hairline and short hair waves
    (392, 190), (420, 160), (456, 146), (494, 150), (526, 172), (540, 210), (536, 250), (520, 290),
    # back of his head, nape, neck, shoulder
    (506, 322), (500, 362), (508, 416), (546, 470), (606, 520), (656, 590), (680, 670), (692, 760),
]


def flower(cx, cy, r, n=5, rot=0.0):
    """One-line flower: petal loops drawn in a single pass around the centre."""
    pts = []
    for k in range(n * 12 + 1):
        t = k / 12
        a = rot + t * math.tau / n
        rr = r * abs(math.sin(t * math.pi)) ** 0.8
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def leaf_loop(x, y, L, ang, w=0.34):
    """Leaf as a single loop out and back along a stem point."""
    pts = []
    for k in range(25):
        t = k / 24
        u = math.sin(t * math.pi) * L
        v = math.sin(t * math.tau) * L * w * 0.5
        pts.append((x + math.cos(ang) * u - math.sin(ang) * v, y + math.sin(ang) * u + math.cos(ang) * v))
    return pts


if "pasangan" in PARTS:
    W, H = 720, 780
    nx = Seq(50100)
    art = blank(W, H)
    # accent: a loose cobalt wash behind the heads (offset, not centred)
    rng = random.Random(3)
    blob = shape_mask(W, H, deform(ellipse_pts(410, 300, 200, 176, 12, 0.3), rng, 3, 0.1))
    art = G(art, blob, ACC_L, ACC, seed=nx(), density=0.55, edge=0.6, bloom=0.5, rough=10, gran=0.35)
    small = shape_mask(W, H, deform(ellipse_pts(110, 170, 36, 30, 10), rng, 2, 0.12))
    art = G(art, small, ACC, ACC_L, seed=nx(), density=0.5, edge=0.6, bloom=0.3, rough=6, gran=0.3)
    line = sample_curve(COUPLE, 1400)
    m = ink(W, H, line, 5.2, seed=nx(), press=pen, jitter=0.45)
    # closed eyes: two short lash arcs
    eyes = ink(W, H, curve([(318, 266), (325, 272), (332, 270)], 12), 2.8, seed=nx()) + ink(W, H, curve([(400, 246), (393, 252), (386, 250)], 12), 2.8, seed=nx())
    art = over(art, ink_paint(np.clip(m + eyes, 0, 1), INK, seed=nx()))
    preview(art, "la-pasangan", tone="#faf8f3")
    save(art, f"{OUT}/pasangan.webp", max_w=640, quality=82)
    clear()

if "ranting" in PARTS:
    W, H = 340, 520
    nx = Seq(50200)
    stem = curve([(170, 510), (166, 420), (150, 330), (158, 240), (184, 150), (200, 90)], 200)
    pts = list(stem)
    # leaves and blooms threaded on the same line: detours from the stem
    out = []
    marks = {40: ("leaf", 2.5), 70: ("leaf", -0.6), 100: ("leaf", 2.7), 130: ("leaf", -0.4), 160: ("leaf", 2.4)}
    for i, p in enumerate(pts):
        out.append(p)
        if i in marks:
            kind, ang = marks[i]
            out += leaf_loop(p[0], p[1], 70 if i < 120 else 54, ang)[1:]
    out += flower(200, 70, 46, 5, 0.3)[1:]
    art = blank(W, H)
    art = G(art, shape_mask(W, H, deform(ellipse_pts(206, 74, 40, 34, 10), random.Random(5), 2, 0.12)), ACC_L, ACC, seed=nx(), density=0.5, edge=0.6, bloom=0.4, rough=6, gran=0.3)
    m = ink(W, H, out, 3.4, seed=nx(), press=pen, jitter=0.35)
    art = over(art, ink_paint(m, INK, seed=nx()))
    preview(art, "la-ranting", tone="#faf8f3")
    save(art, f"{OUT}/ranting.webp", max_w=200, quality=84)
    clear()

if "bunga" in PARTS:
    # divider: a horizontal stem with two leaves and a small bloom, one line
    W, H = 460, 110
    nx = Seq(50300)
    stem = curve([(10, 66), (120, 60), (230, 52), (340, 58), (450, 64)], 220)
    out = []
    for i, p in enumerate(stem):
        out.append(p)
        if i == 50:
            out += leaf_loop(p[0], p[1], 52, -2.6)[1:]
        if i == 80:
            out += leaf_loop(p[0], p[1], 46, 0.5)[1:]
        if i == 108:
            out += flower(p[0], p[1] - 22, 22, 5, 1.2)[1:] if False else []
        if i == 140:
            out += leaf_loop(p[0], p[1], 46, -0.6)[1:]
        if i == 170:
            out += leaf_loop(p[0], p[1], 52, 2.6)[1:]
    art = blank(W, H)
    c = stem[110]
    art = G(art, shape_mask(W, H, deform(ellipse_pts(c[0] + 4, c[1] - 6, 26, 22, 10), random.Random(6), 2, 0.12)), ACC_L, ACC, seed=nx(), density=0.5, edge=0.6, bloom=0.3, rough=4, gran=0.3)
    fl = flower(c[0], c[1] - 4, 24, 5, 0.9)
    m = ink(W, H, out, 2.8, seed=nx(), press=pen, jitter=0.3) + ink(W, H, fl, 2.6, seed=nx(), press=pen, jitter=0.3)
    art = over(art, ink_paint(np.clip(m, 0, 1), INK, seed=nx()))
    preview(art, "la-bunga", tone="#faf8f3")
    save(art, f"{OUT}/bunga.webp", max_w=300, quality=84)
