"""Gender Reveal — playful gouache in cream, baby blue and candy pink with a navy ink accent: a bunch of blue balloons,
a bunch of pink balloons, a big two-tone question mark, question-mark confetti, and baby things (onesie, booties,
rattle). Run: python3 -I gender-reveal.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f6_lib import *

OUT = outdir("gender-reveal")
PARTS = sys.argv[1:] or ["balon-biru", "balon-pink", "tanya", "konfeti", "bayi"]
BLUE, BLUE_D, BLUE_L = "#7db4e0", "#3f78b3", "#cfe5f6"
PINK, PINK_D, PINK_L = "#f2a0bc", "#cf5f88", "#fbd9e5"
NAVY = "#2c3459"
YEL, YEL_D = "#ffd56b", "#e0a92e"
CREAM = "#fff7ee"


def qmark_items(x, y, s):
    """Question mark as stroke items (hook + stem) and the dot centre, size s = height."""
    hook = [(x + math.cos(t) * s * 0.26, y + s * 0.28 + math.sin(t) * s * 0.26) for t in [math.pi * (1.05 + 1.25 * i / 24) for i in range(25)]]
    end = hook[-1]
    stem = curve([end, (x + s * 0.02, y + s * 0.6), (x, y + s * 0.72)], 14)
    return [(hook + stem[1:], s * 0.13, (0.02, 0.02))], (x, y + s * 0.92), s * 0.085


def balloon(art, W, H, cx, cy, r, col, col_d, col_l, nx, rng, tilt=0.0, string_to=None):
    pts = [(math.cos(t) * r * (0.92 + 0.06 * -math.sin(t)), math.sin(t) * r * (1.12 if math.sin(t) > 0 else 1.0)) for t in [i / 32 * math.tau for i in range(32)]]
    body = shapes(W, H, [xf(pts, cx, cy, 1, tilt)])
    bx, by = xf([(0, r * 1.12)], cx, cy, 1, tilt)[0]
    knot = shapes(W, H, [xf([(-r * .1, r * 1.22), (r * .1, r * 1.22), (0, r * 1.08)], cx, cy, 1, tilt)], smooth=False)
    if string_to:
        sx, sy = string_to
        st = curve([(bx, by + r * 0.1), (bx + (sx - bx) * 0.3 + 14, by + (sy - by) * 0.35), (bx + (sx - bx) * 0.7 - 12, by + (sy - by) * 0.7), (sx, sy)], 40)
        art = G(art, strokes(W, H, [(st, 2.0, None)]), NAVY, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    m = np.maximum(body, knot)
    art = GP(art, m, col, mix(col, col_d, 0.25), seed=nx(), rough=1.4, streak=1.0)
    art = mul(art, gaussian_filter(np.clip((radial(m, cx - r * .4, cy - r * .5, r * 2.0) - .35) / .65, 0, 1) * m, 3), col_d, 0.9, seed=nx())
    art = lift(art, spot(body, cx - r * .35, cy - r * .45, r * .5) ** 1.3, col_l, 0.7, seed=nx())
    sheen = strokes(W, H, [(xf(arc_pts(0, 0, r * 0.68, math.pi * 1.12, math.pi * 1.42, 12), cx, cy, 1, tilt), r * 0.1, (0.3, 0.3))])
    art = lift(art, gaussian_filter(sheen * body, 1.5), "#ffffff", 0.75, seed=nx())
    return G(art, edge_of(m, 1.4), col_d, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)


def bunch(name, col, col_d, col_l, seed, flip=False):
    W, H = 420, 760
    nx = Seq(seed); rng = random.Random(seed)
    art = blank(W, H)
    knot = (210, 720)
    specs = [(140, 170, 104, -0.15), (292, 210, 96, 0.18), (206, 330, 92, 0.02)]
    for k, (x, y, r, t) in enumerate(specs):
        c = col if k != 1 else mix(col, "#ffffff", 0.15)
        art = balloon(art, W, H, x, y, r, c, col_d, col_l, nx, rng, tilt=t, string_to=knot)
    bow = shapes(W, H, [petal_pts(knot[0], knot[1], 34, 14, -2.6, n=12), petal_pts(knot[0], knot[1], 34, 14, -0.5, n=12)])
    art = GP(art, bow, YEL, YEL_D, seed=nx(), rough=0.8, pad=8)
    tails = strokes(W, H, [(curve([knot, (knot[0] - 10, knot[1] + 20), (knot[0] - 4, knot[1] + 34)], 10), 5, (0, 0.5)), (curve([knot, (knot[0] + 12, knot[1] + 20), (knot[0] + 8, knot[1] + 34)], 10), 5, (0, 0.5))])
    art = GP(art, tails, YEL, YEL_D, seed=nx(), rough=0.6, pad=8)
    if flip:
        art = mirror(art)
    preview(art, f"gr-{name}", tone=CREAM)
    save(art, f"{OUT}/{name}.webp", max_w=220, quality=82)
    clear()


if "balon-biru" in PARTS:
    bunch("balon-biru", BLUE, BLUE_D, BLUE_L, 91100)

if "balon-pink" in PARTS:
    bunch("balon-pink", PINK, PINK_D, PINK_L, 91300, flip=True)

if "tanya" in PARTS:
    W, H = 420, 560
    nx = Seq(91500); rng = random.Random(5)
    items, (dx, dy), dr = qmark_items(210, 40, 470)
    q = np.maximum(strokes(W, H, items), circles(W, H, [(dx, dy, dr * 1.25)]))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    left = ((xx - 210) * 0.9 + (yy - 280) * 0.45 < 0).astype(np.float32)
    left = gaussian_filter(left, 1.2)
    shadow = np.roll(np.roll(q, 12, 0), 10, 1)
    art = G(blank(W, H), shadow, NAVY, seed=nx(), density=0.35, edge=0.2, bloom=0, rough=2, feather=1.5)
    art = GP(art, q * left, BLUE, mix(BLUE, BLUE_D, .25), seed=nx(), rough=1.5, streak=1.2)
    art = GP(art, q * (1 - left), PINK, mix(PINK, PINK_D, .2), seed=nx(), rough=1.5, streak=1.2)
    art = mul(art, shade_side(q, 6, 6, 6), "#3a2f5a", 0.5, seed=nx())
    hl_items = [([(x - 10, y - 8) for x, y in items[0][0][3:16]], 12, (0.3, 0.3))]
    art = lift(art, gaussian_filter(strokes(W, H, hl_items) * q, 2), "#ffffff", 0.55, seed=nx())
    art = G(art, edge_of(q, 1.4), NAVY, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6)
    preview(art, "gr-tanya", tone=CREAM)
    save(art, f"{OUT}/tanya.webp", max_w=220, quality=84)
    clear()

if "konfeti" in PARTS:
    W, H = 720, 720
    nx = Seq(91700); rng = random.Random(7)
    art = blank(W, H)
    cols = [(BLUE, BLUE_D), (PINK, PINK_D), (YEL, YEL_D), ("#9fd6c2", "#5fae92")]
    groups = {i: ([], [], []) for i in range(4)}
    placed = []
    for _ in range(46):
        for _t in range(40):
            x, y = rng.uniform(24, W - 24), rng.uniform(24, H - 24)
            if all(math.hypot(x - px, y - py) > 70 for px, py in placed):
                break
        placed.append((x, y))
        ci = rng.randrange(4); kind = rng.random()
        if kind < 0.3:
            s = rng.uniform(34, 52)
            it, (ddx, ddy), ddr = qmark_items(0, 0, s)
            ang = rng.uniform(-.5, .5)
            groups[ci][0].extend([(xf(p[0], x, y - s / 2, 1, ang), p[1], p[2]) for p in it])
            groups[ci][1].append((*xf([(ddx, ddy)], x, y - s / 2, 1, ang)[0], ddr * 1.2))
        elif kind < 0.6:
            groups[ci][1].append((x, y, rng.uniform(4, 8)))
        elif kind < 0.82:
            a = rng.uniform(0, math.tau); L = rng.uniform(14, 22)
            groups[ci][2].append(xf(rect(-L, -4, L, 4), x, y, 1, a))
        else:
            a = rng.uniform(0, math.tau)
            sq = [(x + math.cos(a) * i * 4 + math.sin(i * 1.4) * 6 * math.sin(a), y + math.sin(a) * i * 4 - math.sin(i * 1.4) * 6 * math.cos(a)) for i in range(-6, 7)]
            groups[ci][0].append((sq, 4, (0.1, 0.1)))
    for ci, (strk, dots_, rects) in groups.items():
        m = np.zeros((H, W), np.float32)
        if strk:
            m = np.maximum(m, strokes(W, H, strk))
        if dots_:
            m = np.maximum(m, circles(W, H, dots_))
        if rects:
            m = np.maximum(m, shapes(W, H, rects, smooth=False))
        art = GP(art, m, cols[ci][0], cols[ci][1], seed=nx(), rough=1.0, streak=0.8)
    preview(art, "gr-konfeti", tone=CREAM)
    save(art, f"{OUT}/konfeti.webp", max_w=360, quality=80)
    clear()

if "bayi" in PARTS:
    W, H = 760, 420
    nx = Seq(91900); rng = random.Random(9)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(380, 392, 330, 18, 18), rng, 1, 0.03)])
    art = G(art, sh, "#8a7f9a", seed=nx(), density=0.25, edge=0.1, bloom=0, rough=3, feather=7)
    # onesie (centre): white with a split blue/pink heart-free pocket of stripes
    ox, oy = 380, 70
    on = [(ox - 46, oy), (ox - 24, oy + 14), (ox + 24, oy + 14), (ox + 46, oy), (ox + 120, oy + 40), (ox + 100, oy + 100), (ox + 70, oy + 86),
          (ox + 72, oy + 230), (ox + 40, oy + 300), (ox + 14, oy + 312), (ox - 14, oy + 312), (ox - 40, oy + 300), (ox - 72, oy + 230), (ox - 70, oy + 86), (ox - 100, oy + 100), (ox - 120, oy + 40)]
    om = shapes(W, H, [deform(on, rng, 1, 0.006)], smooth=False)
    om = gaussian_filter(om, 1.2)
    art = GP(art, om, "#fffdf8", "#f1ebe2", seed=nx(), rough=1.2, streak=1.0)
    art = mul(art, shade_side(om, 6, 0, 7), "#b4aec4", 0.6, seed=nx())
    stripes = strokes(W, H, [([(ox - 80, oy + 140 + k * 26), (ox + 80, oy + 140 + k * 26)], 9, None) for k in range(4)]) * om
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lft = (xx < ox).astype(np.float32)
    art = GP(art, stripes * lft, BLUE, BLUE_D, seed=nx(), rough=0.6, pad=6)
    art = GP(art, stripes * (1 - lft), PINK, PINK_D, seed=nx(), rough=0.6, pad=6)
    neck = strokes(W, H, [(arc_pts(ox, oy - 4, 46, math.pi * 0.08, math.pi * 0.92, 20, 0.4), 5, None)])
    art = GP(art, neck, YEL, YEL_D, seed=nx(), rough=0.5, pad=6)
    art = G(art, edge_of(om, 1.4), NAVY, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
    # booties (left): one blue, one pink
    for bx, col, cd in ((96, BLUE, BLUE_D), (196, PINK, PINK_D)):
        b = shapes(W, H, [deform([(bx - 40, 300), (bx - 34, 250), (bx + 14, 246), (bx + 18, 300), (bx + 64, 318), (bx + 70, 362), (bx - 40, 366)], rng, 1, 0.01)])
        art = GP(art, b, col, mix(col, cd, .3), seed=nx(), rough=1.2, streak=1.0)
        art = mul(art, shade_side(b, 6, 4, 6), cd, 0.6, seed=nx())
        cuff = shapes(W, H, [rect(bx - 42, 244, bx + 20, 266)], smooth=False)
        art = GP(art, cuff, "#fffdf8", "#efe8de", seed=nx(), rough=1.0)
        sole = strokes(W, H, [([(bx - 40, 362), (bx + 68, 362)], 6, None)])
        art = GP(art, sole, "#fffdf8", "#efe8de", seed=nx(), rough=0.6)
        art = G(art, edge_of(np.maximum(b, cuff), 1.3), NAVY, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    # rattle (right)
    rx, ry = 610, 170
    handle = strokes(W, H, [([(rx + 10, ry + 60), (rx + 62, ry + 190)], 20, None)])
    art = GP(art, handle, YEL, YEL_D, seed=nx(), rough=0.8, streak=1.0)
    ringm = ring(W, H, rx + 70, ry + 214, 26, 11)
    art = GP(art, ringm, "#9fd6c2", "#5fae92", seed=nx(), rough=0.8)
    head = circles(W, H, [(rx, ry, 74)])
    art = GP(art, head, "#fffdf8", "#f3ece2", seed=nx(), rough=1.0)
    lft = (xx < rx).astype(np.float32)
    art = GP(art, head * circles(W, H, [(rx, ry, 58)]) * lft, BLUE, BLUE_D, seed=nx(), rough=0.8)
    art = GP(art, head * circles(W, H, [(rx, ry, 58)]) * (1 - lft), PINK, PINK_D, seed=nx(), rough=0.8)
    art = mul(art, gaussian_filter(np.clip((radial(head, rx - 30, ry - 30, 150) - .3) / .7, 0, 1) * head, 3), "#6d6890", 0.7, seed=nx())
    art = lift(art, spot(head, rx - 26, ry - 30, 30), "#ffffff", 0.7, seed=nx())
    it, (qdx, qdy), qdr = qmark_items(rx, ry - 40, 72)
    qm = np.maximum(strokes(W, H, it), circles(W, H, [(qdx, qdy, qdr)]))
    art = GP(art, qm, "#fffdf8", "#ffffff", seed=nx(), rough=0.5, pad=6)
    art = G(art, edge_of(np.maximum(head, handle), 1.4), NAVY, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
    preview(art, "gr-bayi", tone=CREAM)
    save(art, f"{OUT}/bayi.webp", max_w=380, quality=82)
    clear()
