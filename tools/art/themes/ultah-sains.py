"""Ultah Sains — a little scientist's birthday in kid-friendly gouache: a lab bench with a bubbling Erlenmeyer flask,
a rack of three test tubes, a baking-soda volcano frothing pink foam, a magnifier; a mini rocket; a beaker to hold the
age; an atom doodle; soap-film bubbles. Lab-coat palette: white, mint, teal and navy with bright liquid colours.
Run: python3 -I ultah-sains.py [part ...]   parts: bench rocket beaker atom bubble divider flask
Assets -> public/themes/art/ultah-sains/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o2_lib import *  # noqa

OUT = outdir("ultah-sains")
PARTS = sys.argv[1:] or ["bench", "rocket", "beaker", "atom", "bubble", "divider", "flask"]
NAVY, TEAL, MINT, WHITE = "#24406e", "#2f8f9d", "#bfe8dc", "#fbfcfd"
MAG, ORANGE, LIME, YELLOW, WOOD = "#e2427f", "#f39a2b", "#8fcf3c", "#ffd23f", "#d79b5e"


def paint(art, m, col, col2=None, seed=1, light=(0.3, 0.2), shade=0.35, rough=2.2):
    """Gouache shape with soft shading away from the top-left light and a pale highlight."""
    art = GP(art, m, col, col2 or mix_hex(col, "#ffffff", 0.12), seed=seed, rough=rough, streak=0.8)
    h, w = m.shape
    ys, xs = np.where(m > 0.3)
    if len(xs) == 0:
        return art
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    lx, ly = x0 + (x1 - x0) * light[0], y0 + (y1 - y0) * light[1]
    R = max(x1 - x0, y1 - y0)
    d = np.clip(1 - radial(w, h, lx, ly, R * 1.1), 0, 1)
    art = G(art, m * d, mix_hex(col, NAVY, 0.55), seed=seed + 3, density=shade, edge=0.1, bloom=0.2, rough=1, feather=2, gran=0.15)
    return art


def outline(art, items, seed, col=NAVY, w=None):
    m = strokes(art.shape[1], art.shape[0], items)
    return GP(art, m, col, seed=seed, rough=1.0, streak=0.4)


def glass(art, m, seed):
    """Glass: pale mint, translucent, with a white glint."""
    art = OV(art, m, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * col_arr("#e6f6f2"), (gaussian_filter(mm, 0.7) * 0.55)[..., None]], -1))
    return art


def flask_art(art, W, H, cx, base, h, liquid, nx, rng, bubbles=True):
    """Erlenmeyer flask: narrow neck, conical body, liquid in the lower part, bubbles rising."""
    nw, bw = h * 0.12, h * 0.42
    neck_top = base - h
    shoulder = base - h * 0.55
    body = [(cx - nw, neck_top), (cx + nw, neck_top), (cx + nw, shoulder), (cx + bw, base - h * 0.06), (cx + bw * 0.92, base), (cx - bw * 0.92, base), (cx - bw, base - h * 0.06), (cx - nw, shoulder)]
    m = poly(W, H, body)
    art = glass(art, m, nx())
    lv = base - h * 0.36
    t = (base - lv) / (base - shoulder)
    half = bw - (bw - nw) * (1 - (lv - shoulder) / (base - h * 0.06 - shoulder)) if lv > shoulder else nw
    liq = poly(W, H, [(cx - half, lv), (cx + half, lv), (cx + bw, base - h * 0.06), (cx + bw * 0.92, base), (cx - bw * 0.92, base), (cx - bw, base - h * 0.06)])
    art = paint(art, liq * m, liquid, seed=nx())
    art = GP(art, ellipses(W, H, [(cx, lv, half, h * 0.025, 0)]), mix_hex(liquid, "#ffffff", 0.35), seed=nx(), rough=1)
    art = outline(art, [(body + [body[0]], max(2.5, h * 0.018), (0.0, 0.0)), ([(cx - nw * 1.4, neck_top), (cx + nw * 1.4, neck_top)], max(3, h * 0.025), (0.0, 0.0))], nx())
    art = GP(art, strokes(W, H, [([(cx - bw * 0.55, base - h * 0.12), (cx - nw * 0.7, shoulder + h * 0.05)], max(2, h * 0.03), (0.2, 0.3))]), WHITE, seed=nx(), rough=1)
    if bubbles:
        bs = []
        for k in range(9):
            tt = k / 8
            bs.append((cx + math.sin(k * 2.1) * nw * (0.6 + tt * 2.5), neck_top - h * 0.05 - tt * h * 0.55, h * (0.03 + 0.04 * tt)))
        bm = circles(W, H, bs)
        art = paint(art, bm, mix_hex(liquid, "#ffffff", 0.45), seed=nx(), shade=0.2)
        art = outline(art, [([(x + r * math.cos(a), y + r * math.sin(a)) for a in np.linspace(0, math.tau, 18)], max(1.5, h * 0.01), (0, 0)) for x, y, r in bs], nx())
        art = GP(art, circles(W, H, [(x - r * 0.35, y - r * 0.35, r * 0.25) for x, y, r in bs]), WHITE, seed=nx(), rough=0.5)
    return art


def tube(art, W, H, x, top, bot, r, liquid, lv, nx):
    m = np.maximum(rect(W, H, x - r, top, x + r, bot - r), circles(W, H, [(x, bot - r, r)]))
    art = glass(art, m, nx())
    liq = np.maximum(rect(W, H, x - r, lv, x + r, bot - r), circles(W, H, [(x, bot - r, r)])) * m
    art = paint(art, liq, liquid, seed=nx(), shade=0.3)
    art = GP(art, ellipses(W, H, [(x, lv, r, r * 0.25, 0)]), mix_hex(liquid, "#ffffff", 0.35), seed=nx(), rough=0.8)
    pts = [(x - r, top)] + [(x - r, bot - r)] + [(x - r * math.cos(a), bot - r + r * math.sin(a)) for a in np.linspace(0, math.pi, 12)] + [(x + r, top)]
    art = outline(art, [(pts, 3.0, (0, 0)), ([(x - r * 1.35, top), (x + r * 1.35, top)], 4, (0, 0))], nx())
    art = GP(art, strokes(W, H, [([(x - r * 0.45, top + 14), (x - r * 0.45, bot - r * 1.4)], 2.4, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.6)
    return art


def part_bench():
    W, H = 780, 560
    rng = random.Random(3); nx = Seq(100)
    art = blank(W, H)
    top = 420
    # bench: mint lab counter with a wood edge
    art = paint(art, rect(W, H, -10, top, W + 10, top + 34), "#e9f5f1", seed=nx(), shade=0.15)
    art = paint(art, rect(W, H, -10, top + 30, W + 10, H + 10), TEAL, "#3aa0ad", seed=nx(), shade=0.3)
    art = GP(art, strokes(W, H, [([(-10, top + 32), (W + 10, top + 32)], 5, (0, 0))]), NAVY, seed=nx(), rough=1)
    for x in (170, 520):
        art = GP(art, strokes(W, H, [([(x, top + 60), (x, H)], 3, (0, 0))]), "#24707b", seed=nx(), rough=1)
        art = paint(art, rect(W, H, x + 70, top + 84, x + 120, top + 96), "#f2d36b", seed=nx(), shade=0.2)
    clear()
    # baking-soda volcano (left)
    vm = poly(W, H, [(40, top + 6), (120, 250), (150, 236), (188, 240), (214, 256), (300, top + 6)], smooth=True)
    art = paint(art, vm, "#a7714a", "#bd8656", seed=nx(), shade=0.45)
    stripes = strokes(W, H, [([(70 + k * 30, top - 10 - k * 30), (110 + k * 38, top - 20 - k * 32)], 4, (0.2, 0.2)) for k in range(4)]) * vm
    art = GP(art, stripes, "#8c5a39", seed=nx(), rough=1)
    foam = []
    for k in range(16):
        a = rng.uniform(0, math.pi)
        foam.append((168 + math.cos(a) * rng.uniform(10, 50), 232 - math.sin(a) * rng.uniform(4, 42), rng.uniform(14, 26)))
    fm = circles(W, H, foam)
    rivers = [(curve([(140, 240), (128, 270), (118, 300), (104, 336), (98, 362)], 30), 24, (0.0, 0.7)),
              (curve([(196, 244), (206, 276), (222, 300), (232, 330)], 30), 20, (0.0, 0.75)),
              (curve([(168, 246), (166, 280), (172, 300)], 20), 16, (0.0, 0.8))]
    fm = np.maximum(fm, displace(strokes(W, H, rivers), nx(), 3, 10))
    art = paint(art, fm, "#ff8fb8", "#ffb3cf", seed=nx(), shade=0.25)
    art = GP(art, circles(W, H, [(x - r * 0.3, y - r * 0.35, r * 0.35) for x, y, r in foam[::2]]), "#ffe1ec", seed=nx(), rough=0.8)
    spl = circles(W, H, [(120, 170, 9), (214, 160, 7), (96, 214, 6), (240, 200, 8), (168, 140, 10)])
    art = paint(art, spl, "#ff8fb8", seed=nx(), shade=0.2)
    clear()
    # flask (centre)
    art = flask_art(art, W, H, 395, top + 2, 230, MAG, nx, rng)
    clear()
    # test tube rack (right)
    rx0, rx1 = 520, 730
    art = paint(art, rect(W, H, rx0, top - 60, rx1, top - 40), WOOD, "#e3ad72", seed=nx(), shade=0.3)
    art = paint(art, rect(W, H, rx0 + 6, top - 40, rx0 + 22, top + 4), WOOD, seed=nx(), shade=0.3)
    art = paint(art, rect(W, H, rx1 - 22, top - 40, rx1 - 6, top + 4), WOOD, seed=nx(), shade=0.3)
    art = paint(art, rect(W, H, rx0 - 6, top - 6, rx1 + 6, top + 6), "#c4864a", seed=nx(), shade=0.3)
    for i, (col, lv) in enumerate([(ORANGE, 0.45), (LIME, 0.55), ("#48a8e8", 0.4)]):
        x = rx0 + 52 + i * 54
        art = tube(art, W, H, x, top - 190 + i * 6, top - 8, 17, col, top - 190 + i * 6 + (182 - i * 6) * lv, nx)
    art = outline(art, [([(rx0, top - 60), (rx1, top - 60), (rx1, top - 40), (rx0, top - 40), (rx0, top - 60)], 3, (0, 0))], nx())
    clear()
    # magnifier lying on the bench, front left
    mx, my = 500, top + 6
    gm = circles(W, H, [(mx, my, 34)])
    art = paint(art, poly(W, H, [(mx + 26, my + 22), (mx + 36, my + 12), (mx + 100, my + 52), (mx + 90, my + 64)]), ORANGE, seed=nx(), shade=0.35)
    art = OV(art, gm, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * col_arr("#e4f7ff"), (mm * 0.75)[..., None]], -1))
    art = outline(art, [([(mx + 34 * math.cos(a), my + 34 * math.sin(a)) for a in np.linspace(0, math.tau, 40)], 8, (0, 0))], nx(), col=NAVY)
    art = GP(art, strokes(W, H, [(arc_pts(mx, my, 22, 3.5, 4.5, 8), 5, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.6)
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "us-bench", tone="#f4fbf8")
    save(art, f"{OUT}/bench.webp", max_w=780, quality=82)
    clear()


def part_rocket():
    W, H = 260, 420
    rng = random.Random(4); nx = Seq(900)
    art = blank(W, H)
    cx = 130
    body = [(cx, 30), (cx + 34, 90), (cx + 42, 170), (cx + 38, 270), (cx - 38, 270), (cx - 42, 170), (cx - 34, 90)]
    bm = poly(W, H, body, smooth=True)
    for side in (-1, 1):
        fin = poly(W, H, [(cx + side * 36, 210), (cx + side * 80, 290), (cx + side * 74, 310), (cx + side * 34, 276)], smooth=True)
        art = paint(art, fin, MAG, seed=nx())
    art = paint(art, bm, WHITE, "#eef3f6", seed=nx(), shade=0.3)
    nose = bm * (1 - ygrad(W, H, 84, 96))
    art = paint(art, nose, ORANGE, seed=nx())
    win = circles(W, H, [(cx, 160, 22)])
    art = paint(art, win, "#5cc4d6", seed=nx(), shade=0.4)
    art = outline(art, [([(cx + 25 * math.cos(a), 160 + 25 * math.sin(a)) for a in np.linspace(0, math.tau, 30)], 6, (0, 0))], nx(), col=TEAL)
    art = GP(art, circles(W, H, [(cx - 8, 152, 6)]), WHITE, seed=nx(), rough=0.5)
    art = paint(art, rect(W, H, cx - 26, 270, cx + 26, 290), NAVY, seed=nx(), shade=0.2)
    art = outline(art, [(curve(body + [body[0]], 60), 3.2, (0, 0))], nx())
    art = GP(art, strokes(W, H, [([(cx - 24, 110), (cx - 30, 200)], 4, (0.2, 0.3))]), WHITE, seed=nx(), rough=0.6)
    preview(art, "us-rocket", tone="#f4fbf8")
    save(art, f"{OUT}/rocket.webp", max_w=130, quality=84)
    # flame as its own piece (flickers)
    fl = blank(W, 200)
    fm = poly(W, 200, [(cx - 22, 10), (cx + 22, 10), (cx + 14, 70), (cx, 150), (cx - 14, 70)], smooth=True)
    fl = paint(fl, fm, ORANGE, YELLOW, seed=nx(), shade=0.1)
    fl = paint(fl, poly(W, 200, [(cx - 10, 10), (cx + 10, 10), (cx + 5, 50), (cx, 90), (cx - 5, 50)], smooth=True), YELLOW, "#fff3a8", seed=nx(), shade=0.0)
    save(fl, f"{OUT}/flame.webp", max_w=50, quality=84)
    clear()


def part_beaker():
    W, H = 300, 340
    rng = random.Random(5); nx = Seq(1200)
    art = blank(W, H)
    x0, x1, top, bot = 40, 260, 40, 320
    m = poly(W, H, [(x0, top), (x1, top), (x1 - 6, bot - 16), (x1 - 22, bot), (x0 + 22, bot), (x0 + 6, bot - 16)], smooth=False)
    art = glass(art, m, nx())
    lv = 150
    liq = m * ygrad(W, H, lv - 1, lv)
    art = paint(art, liq, LIME, "#a6dc55", seed=nx(), shade=0.3)
    art = GP(art, ellipses(W, H, [(150, lv, 108, 10, 0)]), "#d4f29a", seed=nx(), rough=1)
    ticks = [([(x0 + 10, y), (x0 + (40 if k % 2 == 0 else 26), y)], 3, (0, 0)) for k, y in enumerate(range(80, 300, 30))]
    art = outline(art, ticks + [([(x0 - 18, top - 8), (x0, top), (x0 + 6, bot - 16), (x0 + 22, bot), (x1 - 22, bot), (x1 - 6, bot - 16), (x1, top), (x1 + 6, top - 6)], 5, (0, 0))], nx())
    bs = [(110, 110, 9), (180, 90, 12), (150, 60, 7), (200, 130, 6)]
    art = paint(art, circles(W, H, bs), "#d4f29a", seed=nx(), shade=0.2)
    art = outline(art, [([(x + r * math.cos(a), y + r * math.sin(a)) for a in np.linspace(0, math.tau, 18)], 2.2, (0, 0)) for x, y, r in bs], nx())
    art = GP(art, strokes(W, H, [([(x1 - 30, 70), (x1 - 34, 270)], 7, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.6)
    preview(art, "us-beaker", tone="#f4fbf8")
    save(art, f"{OUT}/beaker.webp", max_w=150, quality=84)
    clear()


def atom_art(W, H, cx, cy, R, nx, cols=(TEAL, MAG, ORANGE)):
    art = blank(W, H)
    for k, col in enumerate(cols):
        a = k / 3 * math.pi
        pts = []
        for t in np.linspace(0, math.tau, 80):
            x, y = math.cos(t) * R, math.sin(t) * R * 0.36
            pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
        art = outline(art, [(pts, max(3, R * 0.07), (0, 0))], nx(), col=col)
        t = 0.7 + k * 2
        x, y = math.cos(t) * R, math.sin(t) * R * 0.36
        art = paint(art, circles(W, H, [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a), R * 0.11)]), col, seed=nx(), shade=0.3)
    art = paint(art, circles(W, H, [(cx, cy, R * 0.2)]), NAVY, seed=nx(), shade=0.3)
    art = GP(art, circles(W, H, [(cx - R * 0.06, cy - R * 0.06, R * 0.06)]), WHITE, seed=nx(), rough=0.4)
    return art


def part_atom():
    W, H = 260, 260
    nx = Seq(1500)
    art = atom_art(W, H, 130, 130, 110, nx)
    preview(art, "us-atom", tone="#f4fbf8")
    save(art, f"{OUT}/atom.webp", max_w=120, quality=84)
    clear()


def part_bubble():
    W, H = 120, 120
    nx = Seq(1700)
    art = blank(W, H)
    m = circles(W, H, [(60, 60, 50)])
    ring = np.clip(m - circles(W, H, [(60, 60, 44)]), 0, 1)
    art = OV(art, m, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * col_arr("#dff6ff"), (mm * 0.35)[..., None]], -1))
    art = G(art, ring * xgrad(W, H, 10, 110), "#b48bff", seed=nx(), density=0.6, edge=0.2, rough=1, feather=1)
    art = G(art, ring * (1 - xgrad(W, H, 10, 110)), "#6fd6e6", seed=nx(), density=0.6, edge=0.2, rough=1, feather=1)
    art = GP(art, strokes(W, H, [(arc_pts(60, 60, 36, 3.6, 4.6, 10), 6, (0.2, 0.2))]), WHITE, seed=nx(), rough=0.5)
    save(art, f"{OUT}/bubble.webp", max_w=48, quality=84)
    clear()


def part_divider():
    W, H = 720, 140
    rng = random.Random(6); nx = Seq(1900)
    art = atom_art(W, H, 360, 70, 56, nx)
    dots = []
    for side in (-1, 1):
        for k in range(6):
            x = 360 + side * (90 + k * 34)
            dots.append((x, 70 + math.sin(k * 1.3) * 6, 9 - k * 0.9))
    cols = [MAG, ORANGE, LIME, "#48a8e8", YELLOW, TEAL]
    for i, d in enumerate(dots):
        art = paint(art, circles(W, H, [d]), cols[i % 6], seed=nx(), shade=0.25)
    preview(art, "us-divider", tone="#f4fbf8")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()


def part_flask():
    W, H = 240, 330
    rng = random.Random(7); nx = Seq(2100)
    art = flask_art(blank(W, H), W, H, 120, 320, 190, ORANGE, nx, rng)
    preview(art, "us-flask", tone="#f4fbf8")
    save(art, f"{OUT}/flask.webp", max_w=110, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
