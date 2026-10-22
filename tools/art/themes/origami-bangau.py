"""Origami Bangau — paper craft: folded paper cranes (flat faceted planes, washi fibre, crisp folds, soft cast shadow),
senbazuru strings of cranes, layered paper-cut hills, a thread garland divider and a washi paper tile.
Run: python3 -I origami-bangau.py [part ...]  parts: cranes string garland layers washi
Assets -> public/themes/art/origami-bangau/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b5_lib import *

OUT = outdir("origami-bangau")
PARTS = sys.argv[1:] or ["cranes", "string", "garland", "layers", "washi"]
PAPERS = {"blush": "#f0b5ae", "mint": "#b9e0cf", "butter": "#f5e0a0", "lilac": "#cbbdec", "sky": "#bcd6ef", "coral": "#f2a99a"}
SHADOW = "#5d4a5e"

# crane facets in a 400x300 design space: (points, light), back to front
CRANE = [
    ([(180, 152), (138, 26), (238, 150)], .80),                      # far wing
    ([(252, 180), (348, 64), (266, 194)], .74),                      # tail, lower plane
    ([(150, 182), (70, 82), (174, 198)], .74),                       # neck, lower plane
    ([(150, 180), (200, 140), (206, 224)], .88),                     # body left
    ([(200, 140), (264, 182), (206, 224)], 1.0),                     # body right
    ([(246, 178), (348, 64), (232, 162)], .96),                      # tail, upper plane
    ([(152, 178), (70, 82), (180, 164)], .98),                       # neck, upper plane
    ([(70, 82), (46, 110), (84, 94)], .84),                          # head (inside-reverse fold)
    ([(166, 174), (250, 10), (214, 170)], 1.06),                     # near wing, inner plane
    ([(214, 170), (250, 10), (262, 180)], .9),                       # near wing, outer plane
]
FOLDS = [((200, 140), (206, 224)), ((70, 82), (164, 180)), ((348, 64), (250, 178)), ((250, 10), (214, 170))]


def crane(dst, W, H, ox, oy, s, col, seed, rot=0.0, flip=False, shadow=True, fibre=None):
    def T(p):
        x, y = (p[0] - 200) * s, (p[1] - 150) * s
        if flip:
            x = -x
        c, sn = math.cos(rot), math.sin(rot)
        return (ox + x * c - y * sn, oy + x * sn + y * c)
    if fibre is None:
        fibre = paper_fibre(H, W, seed)
    full = np.zeros((H, W), np.float32)
    masks = []
    for pts, lt in CRANE:
        m = poly(W, H, [T(p) for p in pts])
        masks.append((m, lt))
        full = np.maximum(full, m)
    if shadow:
        sh = np.roll(np.roll(gaussian_filter(full, 6 * max(s, .4)), int(14 * s) + 2, 0), int(8 * s) + 1, 1)
        dst = over(col_arr(sh, SHADOW, np.clip(sh * .22, 0, 1)), dst)
    for i, (m, lt) in enumerate(masks):
        # light falls from top-left: a gentle gradient across each plane
        dst = facet(dst, m, col, lt, seed + i * 7, fibre=fibre,
                    shade_grad=lambda xx, yy: 1 - np.clip((xx - ox + yy - oy) / (500 * s), -1, 1) * .05)
    for a, b in FOLDS:
        dst = fold_line(dst, W, H, T(a), T(b), "#ffffff", .28, max(.8, 1.2 * s))
    # crisp edge: a hair of darker paper edge
    edge = inner_edge(full, max(.8, 1.1 * s))
    dst = OV(dst, edge, lambda mm: col_arr(mm, mix(col, "#5d4a5e", .35), mm * .35), pad=4)
    return dst


if "cranes" in PARTS:
    W, H = 420, 320
    for k, name in enumerate(["blush", "mint", "butter", "lilac"]):
        art = blank(W, H)
        art = crane(art, W, H, 205, 150, 1.0, PAPERS[name], 40100 + k * 31)
        preview(art, f"ori-crane-{name}", tone="#faf6ef")
        save(art, f"{OUT}/crane-{name}.webp", max_w=240, quality=84)
        clear()

if "string" in PARTS:
    # senbazuru: one thread, six small cranes and paper beads, a tassel
    for v, order in enumerate((["blush", "mint", "butter", "lilac", "sky", "coral"], ["mint", "lilac", "coral", "butter", "blush", "sky"])):
        W, H = 180, 1040
        rng = random.Random(40500 + v)
        fib = paper_fibre(H, W, 40500 + v)
        art = blank(W, H)
        cx = W / 2
        thread = strokes(W, H, [([(cx + math.sin(y / 160 + v) * 3, y) for y in range(0, 990, 10)], 1.6, None)])
        art = OV(art, thread, lambda m: col_arr(m, "#8b7a86", m * .85), pad=4)
        y = 90
        for i, name in enumerate(order):
            art = crane(art, W, H, cx + rng.uniform(-6, 6), y, .36, PAPERS[name], 40600 + v * 50 + i, rot=rng.uniform(-.18, .18), flip=(i + v) % 2 == 1, fibre=fib)
            # bead below each crane
            art = GP(art, circles(W, H, [(cx + math.sin((y + 64) / 160 + v) * 3, y + 70, 5)]), mix(PAPERS[name], "#ffffff", .2), seed=40700 + i, rough=.4, pad=6)
            y += 148
        # tassel
        ty = 960
        tass = strokes(W, H, [([(cx, ty), (cx + dx * .25, ty + 40), (cx + dx, ty + 72)], 1.6, (0, .3)) for dx in np.linspace(-12, 12, 9)])
        art = OV(art, tass, lambda m: col_arr(m, "#e58f83", m * .9), pad=4)
        art = GP(art, ellipses(W, H, [(cx, ty, 9, 7, 0)]), "#e58f83", seed=40800, rough=.4, pad=6)
        preview(art, f"ori-string-{v}", tone="#faf6ef")
        save(art, f"{OUT}/string-{v}.webp", max_w=120, quality=82)
        clear()

if "garland" in PARTS:
    W, H = 640, 120
    rng = random.Random(40900)
    fib = paper_fibre(H, W, 40900)
    art = blank(W, H)
    pts = [(x, 34 + 18 * math.sin(math.pi * x / W)) for x in range(10, W - 9, 8)]
    art = OV(art, strokes(W, H, [(pts, 1.6, None)]), lambda m: col_arr(m, "#8b7a86", m * .85), pad=4)
    # little folded diamonds hanging from the thread + a crane in the middle
    for i, x in enumerate([90, 180, 460, 550]):
        y = 34 + 18 * math.sin(math.pi * x / W)
        name = ["blush", "butter", "mint", "lilac"][i]
        col = PAPERS[name]
        art = OV(art, strokes(W, H, [([(x, y), (x, y + 12)], 1.2, None)]), lambda m: col_arr(m, "#8b7a86", m * .8), pad=4)
        top, mid, bot = (x, y + 12), y + 30, (x, y + 50)
        art = facet(art, poly(W, H, [top, (x - 12, mid), bot]), col, .86, 41000 + i, fibre=fib)
        art = facet(art, poly(W, H, [top, (x + 12, mid), bot]), col, 1.02, 41010 + i, fibre=fib)
        art = fold_line(art, W, H, top, bot, "#ffffff", .3, 1)
    art = crane(art, W, H, W / 2, 62, .34, PAPERS["coral"], 41100, fibre=fib)
    preview(art, "ori-garland", tone="#faf6ef")
    save(art, f"{OUT}/garland.webp", max_w=420, quality=84)
    clear()

if "layers" in PARTS:
    # layered paper-cut hills for the bottom of the cover/closing; each sheet casts a soft shadow on the one behind
    W, H = 800, 340
    rng = random.Random(41200)
    fib = paper_fibre(H, W, 41200)
    art = blank(W, H)
    sheets = [("#f6dcd6", 120, 26, 1.3, .0), ("#cfe8dc", 170, 22, 1.9, 1.3), ("#d9d2f1", 220, 20, 1.5, 2.6), ("#bcd6ef", 262, 16, 2.4, .7), ("#fbf4e8", 300, 12, 1.2, 3.3)]
    for i, (col, y0, amp, freq, ph) in enumerate(sheets):
        top = [(x, y0 + amp * math.sin(x / W * math.pi * freq + ph) + 10 * math.sin(x / 47 + i)) for x in range(-10, W + 11, 10)]
        m = shapes(W, H, [top + [(W + 10, H + 10), (-10, H + 10)]])
        sh = np.roll(gaussian_filter(m, 7), -8, 0)
        art = over(art, col_arr(sh, SHADOW, np.clip(sh * .2, 0, 1) * (1 - m)))
        art = facet(art, m, col, 1.0, 41300 + i * 11, fibre=fib,
                    shade_grad=lambda xx, yy, y0=y0: 1 - np.clip((yy - y0) / 400, 0, 1) * .05)
        art = OV(art, inner_edge(m, 1.2), lambda mm: col_arr(mm, "#ffffff", mm * .35), pad=4)
    preview(art, "ori-layers", tone="#faf6ef")
    save(art, f"{OUT}/layers.webp", max_w=640, quality=80)
    clear()

if "washi" in PARTS:
    T = 384
    rng = random.Random(41500)
    cv = Canvas(T, T, 41500)
    p = skia.Paint(AntiAlias=True, Color4f=color("#ffffff", .55), StrokeWidth=.8, Style=skia.Paint.kStroke_Style)
    for _ in range(260):
        x, y = rng.uniform(0, T), rng.uniform(0, T)
        a = rng.uniform(0, math.tau); L = rng.uniform(10, 40)
        pts = [(x, y)]
        for k in range(5):
            a += rng.gauss(0, .45); x += math.cos(a) * L / 5; y += math.sin(a) * L / 5; pts.append((x, y))
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                path = skia.Path(); path.moveTo(pts[0][0] + dx, pts[0][1] + dy)
                for q in pts[1:]:
                    path.lineTo(q[0] + dx, q[1] + dy)
                cv.c.drawPath(path, p)
    fib = cv.array()[..., 3]
    base = np.ones((T, T, 3), np.float32) * np.array(hex_rgb("#f8f3ea"), np.float32)
    mot = wrap_noise(T, T, 41501, 26) - .5
    tooth = wrap_noise(T, T, 41502, .7) - .5
    rgb = base * (1 + mot[..., None] * .035 + tooth[..., None] * .03) + fib[..., None] * .03
    rgb = rgb - (1 - fib[..., None]) * 0
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((T, T, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/washi.webp", quality=72)
    clear()
