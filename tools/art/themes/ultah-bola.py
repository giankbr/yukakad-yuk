"""Ultah Bola — kids birthday on a painted football pitch (gouache): a seamless grass tile with brush-blade texture (the
mowing stripes are laid over it in CSS so they scale to any height), chalk pitch markings (centre circle + halfway line),
a stitched leather ball, a blank red jersey (the age and name are typeset on it in HTML), a gold cup, a goal with net and
team-colour bunting. No club or brand marks. Run: python3 -I ultah-bola.py [part ...]
parts: grass chalk ball jersey trophy net bunting   Assets -> public/themes/art/ultah-bola/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c5_lib import *

OUT = outdir("ultah-bola")
PARTS = sys.argv[1:] or ["grass", "chalk", "ball", "jersey", "trophy", "net", "bunting"]
INK = "#1d2a4f"
RED, RED2, REDS = "#e2452f", "#ec5a3a", "#a92a22"
NAVY = "#22336b"
GOLD, GOLD2, GOLDS, GOLDL = "#f4bb37", "#f8cd55", "#c0801f", "#fff2b8"
CHALK = "#f7f4ea"
BG = "#3f9a48"


def ell(W, H, cx, cy, rx, ry, rot, rng, n=18, d=0.015):
    return shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, n, rot), rng, 1, d)])


if "grass" in PARTS:
    S = 384
    nx = Seq(80100); rng = random.Random(81)
    base = solid(S, S, "#3f9a48")
    lo = wrap_noise(S, S, 3, 26)
    base[..., :3] *= (0.94 + 0.12 * lo)[..., None]
    # brush blades, drawn three times offset so the tile wraps
    for layer, (cols, n, L, wd) in enumerate([(("#2f8139", "#357f3b"), 900, (10, 22), (1.6, 3.0)), (("#58b05a", "#4ea651", "#6cbf63"), 700, (8, 18), (1.2, 2.4)), (("#86cf72",), 160, (6, 12), (1.0, 1.8))]):
        for col in cols:
            items = []
            for _ in range(n // len(cols)):
                x, y = rng.uniform(0, S), rng.uniform(0, S)
                l = rng.uniform(*L); a = -math.pi / 2 + rng.uniform(-0.45, 0.45)
                pts = [(x, y), (x + math.cos(a) * l * 0.5 + rng.uniform(-1, 1), y + math.sin(a) * l * 0.5), (x + math.cos(a) * l, y + math.sin(a) * l)]
                w = rng.uniform(*wd)
                for ox in (-S, 0, S):
                    for oy in (-S, 0, S):
                        items.append(([(px + ox, py + oy) for px, py in pts], w, (0.0, 0.7)))
            m = strokes(S, S, items)
            base = over(base, col_arr(m, col, m * (0.55 if layer < 2 else 0.4)))
    base = add_grain(base, nx(), 0.05)
    preview(base, "ub-grass", tone=BG)
    save_rgb(base, f"{OUT}/grass.webp", quality=72)
    clear()

if "chalk" in PARTS:
    W, H = 760, 640
    nx = Seq(80200); rng = random.Random(82)
    art = blank(W, H)
    cx, cy, r = W / 2, H / 2, 250
    ring = strokes(W, H, [([(cx + math.cos(t) * r * (1 + rng.uniform(-.004, .004)), cy + math.sin(t) * r) for t in np.linspace(0, 2 * math.pi, 160)], 9, None)])
    line = strokes(W, H, [([(0, cy + 1), (W * .5, cy - 1.5), (W, cy + 2)], 9, None)])
    spot = circles(W, H, [(cx, cy, 11)])
    m = np.clip(ring + line + spot, 0, 1)
    art = crayon(art, m, CHALK, seed=nx(), amt=0.92, tooth=0.55)
    art = crayon(art, m, CHALK, seed=nx(), amt=0.5, tooth=0.2)
    preview(art, "ub-chalk", tone=BG)
    save(art, f"{OUT}/chalk.webp", max_w=560, quality=80)
    clear()

if "ball" in PARTS:
    W, H = 320, 320
    nx = Seq(80300); rng = random.Random(83)
    art = blank(W, H)
    cx, cy, R = 160, 158, 132
    disc = circles(W, H, [(cx, cy, R)])
    art = body(art, disc, "#fbfaf4", "#f1efe6", "#b9bdc7", "#ffffff", nx, ldir=(-18, -22), blur=16)
    # pentagon patches: one central, five cut by the rim (slightly off-centre = turned ball)
    pcx, pcy = cx - 10, cy - 8

    def pent(x, y, rr, a0):
        return [(x + math.cos(a0 + k * 2 * math.pi / 5) * rr, y + math.sin(a0 + k * 2 * math.pi / 5) * rr) for k in range(5)]
    patches = [pent(pcx, pcy, 40, -math.pi / 2)]
    seams = []
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5 + math.pi / 5
        px, py = pcx + math.cos(a) * 112, pcy + math.sin(a) * 112
        patches.append(pent(px, py, 36, a + math.pi))
        # seams from central pentagon corners outwards
        ca = -math.pi / 2 + k * 2 * math.pi / 5
        x0, y0 = pcx + math.cos(ca) * 40, pcy + math.sin(ca) * 40
        seams.append(([(x0, y0), (pcx + math.cos(ca) * 74, pcy + math.sin(ca) * 74)], 2.4, None))
        seams.append(([(pcx + math.cos(ca) * 74, pcy + math.sin(ca) * 74), (pcx + math.cos(ca - 0.36) * 92, pcy + math.sin(ca - 0.36) * 92)], 2.2, None))
        seams.append(([(pcx + math.cos(ca) * 74, pcy + math.sin(ca) * 74), (pcx + math.cos(ca + 0.36) * 92, pcy + math.sin(ca + 0.36) * 92)], 2.2, None))
    pm = shapes(W, H, [deform(p, rng, 1, 0.01) for p in patches], smooth=False)
    pm = np.clip(gaussian_filter(pm, 1.6) * 1.3, 0, 1) * disc
    art = GP(art, pm, "#262a36", "#323748", seed=nx(), rough=1.2, streak=0.5)
    art = tint(art, side_light(disc, -18, -22, 16) * pm, "#000000", 0.35, seed=nx())
    sm = strokes(W, H, seams) * disc * (1 - pm)
    art = crayon(art, sm, "#8a8f9c", seed=nx(), amt=0.75, tooth=0.2)
    # rim + gloss
    art = crayon(art, inner_edge(disc, 2.2), "#2f3546", seed=nx(), amt=0.7, tooth=0.3)
    art = OV(art, ell(W, H, cx - 70, cy - 58, 22, 10, -0.8, rng) * disc * (1 - pm), lambda mm: col_arr(mm, "#ffffff", mm * 0.75), pad=6)
    preview(art, "ub-ball", tone=BG)
    save(art, f"{OUT}/ball.webp", max_w=220, quality=84)
    clear()

if "jersey" in PARTS:
    W, H = 560, 540
    nx = Seq(80400); rng = random.Random(84)
    art = blank(W, H)
    shirt = [(226, 54), (150, 78), (52, 176), (104, 234), (160, 196), (164, 492), (280, 500), (396, 492), (400, 196),
             (456, 234), (508, 176), (410, 78), (334, 54), (280, 74)]
    m = shapes(W, H, [deform(shirt, rng, 1, 0.006)], smooth=False)
    m = np.clip(gaussian_filter(m, 2.2) * 1.25, 0, 1)
    art = GP(art, ell(W, H, 284, 512, 170, 14, 0, rng), "#14532a", seed=nx(), rough=2, density=0.3)
    art = body(art, m, RED, RED2, REDS, "#ff8a64", nx, ldir=(-16, -10), blur=14)
    # side panels + fold shadows
    panels = shapes(W, H, [[(160, 210), (192, 214), (186, 494), (164, 492)], [(400, 210), (370, 214), (374, 494), (396, 492)]], smooth=False) * m
    art = tint(art, gaussian_filter(panels, 2), REDS, 0.55, seed=nx())
    folds = strokes(W, H, [(curve([(230, 300), (250, 380), (238, 470)], 20), 14, (0.3, 0.4)), (curve([(330, 260), (322, 360), (338, 470)], 20), 12, (0.3, 0.4)),
                           (curve([(150, 120), (176, 170), (168, 196)], 12), 10, (0.3, 0.3)), (curve([(410, 120), (384, 170), (392, 196)], 12), 10, (0.3, 0.3))])
    art = tint(art, gaussian_filter(folds, 5) * m, REDS, 0.35, seed=nx())
    art = tint(art, gaussian_filter(strokes(W, H, [(curve([(290, 120), (300, 260), (292, 420)], 20), 18, (0.3, 0.4))]), 7) * m, "#ff9a78", 0.3, seed=nx())
    # navy collar + cuff stripes + hem band
    collar = strokes(W, H, [(curve([(224, 56), (252, 76), (280, 80), (308, 76), (336, 56)], 24), 13, None)])
    cuffs = strokes(W, H, [([(58, 180), (108, 232)], 12, None), ([(502, 180), (452, 232)], 12, None)])
    cuffs2 = strokes(W, H, [([(72, 166), (122, 216)], 5, None), ([(488, 166), (438, 216)], 5, None)]) * m
    hem = strokes(W, H, [([(168, 484), (280, 492), (392, 484)], 7, None)]) * m
    trim = np.clip(collar + cuffs + cuffs2 + hem, 0, 1)
    art = GP(art, trim, NAVY, "#2b3f80", seed=nx(), rough=1.0)
    art = GP(art, strokes(W, H, [(curve([(232, 66), (280, 88), (328, 66)], 20), 3.5, None)]), CHALK, seed=nx(), rough=0.6, pad=6)
    art = crayon(art, inner_edge(m, 2.2), "#7d1f1a", seed=nx(), amt=0.6, tooth=0.3)
    preview(art, "ub-jersey", tone="#e9f3e0")
    save(art, f"{OUT}/jersey.webp", max_w=360, quality=82)
    clear()

if "trophy" in PARTS:
    W, H = 420, 520
    nx = Seq(80500); rng = random.Random(85)
    art = blank(W, H)
    cx = 210
    bowl = shapes(W, H, [[(96, 70), (324, 70), (318, 120), (296, 200), (252, 250), (232, 262), (188, 262), (168, 250), (124, 200), (102, 120)]])
    handles = strokes(W, H, [(arc_pts(98, 136, 48, 1.75, 4.6, 26), 15, None), (arc_pts(322, 136, 48, -1.45, 1.4, 26), 15, None)])
    handles = np.clip(handles - gaussian_filter(bowl, 0.5), 0, 1)
    stem = shapes(W, H, [[(192, 256), (228, 256), (222, 320), (246, 350), (174, 350), (198, 320)]])
    cup = np.clip(bowl + handles + stem, 0, 1)
    plinth = shapes(W, H, [[(132, 352), (288, 352), (300, 470), (120, 470)]], smooth=False)
    art = GP(art, ellipses(W, H, [(cx, 474, 140, 12, 0)]), "#14532a", seed=nx(), rough=2, density=0.3)
    art = body(art, plinth, NAVY, "#2b3f80", "#121c3d", "#4a62a8", nx, ldir=(-12, -6), blur=10)
    plate = shapes(W, H, [[(166, 392), (254, 392), (256, 432), (164, 432)]], smooth=False)
    art = body(art, plate, "#e9d08a", "#f3e1a4", "#b38a3c", "#fff6d4", nx, blur=4)
    art = body(art, cup, GOLD, GOLD2, GOLDS, GOLDL, nx, ldir=(-16, -12), blur=12, line="#9a6416")
    # lip band, star, bright streak
    lip = strokes(W, H, [([(100, 76), (210, 82), (320, 76)], 10, None)])
    art = tint(art, lip * bowl, GOLDS, 0.6, seed=nx())
    sp = [(cx + math.cos(-math.pi / 2 + k * math.pi / 5) * (34 if k % 2 == 0 else 15), 160 + math.sin(-math.pi / 2 + k * math.pi / 5) * (34 if k % 2 == 0 else 15)) for k in range(10)]
    art = GP(art, shapes(W, H, [sp], smooth=False), "#fff1b0", "#ffe58a", seed=nx(), rough=0.6, pad=6)
    streak = strokes(W, H, [(curve([(140, 96), (146, 160), (176, 220)], 16), 10, (0.2, 0.5))]) * bowl
    art = OV(art, gaussian_filter(streak, 1.4), lambda mm: col_arr(mm, "#ffffff", mm * 0.65), pad=6)
    preview(art, "ub-trophy", tone="#e9f3e0")
    save(art, f"{OUT}/trophy.webp", max_w=260, quality=84)
    clear()

if "net" in PARTS:
    W, H = 760, 400
    nx = Seq(80600); rng = random.Random(86)
    art = blank(W, H)
    # net: mesh hanging back from the frame (front frame 60..700 x 40..372; back top 120..640 at y 90, back bottom y 330)
    fx0, fx1, fy0, fy1 = 66, 694, 44, 372
    bx0, bx1, by0 = 126, 634, 96
    shade = shapes(W, H, [[(fx0, fy0), (fx1, fy0), (bx1, by0), (bx1, fy1 - 30), (bx0, fy1 - 30), (bx0, by0)]], smooth=False)
    art = G(art, shade, "#1d5a2c", seed=nx(), density=0.32, edge=0.2, bloom=0.1, rough=3, feather=6)
    lines = []
    for i in range(0, 27):
        t = i / 26
        x = bx0 + (bx1 - bx0) * t
        lines.append(([(x + rng.uniform(-1, 1), by0), (x + math.sin(t * 9) * 2, (by0 + fy1 - 30) / 2), (x, fy1 - 30)], 1.8, None))
        lines.append(([(fx0 + (fx1 - fx0) * t, fy0), (x, by0)], 1.6, None))
    for j in range(0, 12):
        t = j / 11
        y = by0 + (fy1 - 30 - by0) * t
        sag = 4 * math.sin(t * math.pi)
        lines.append(([(bx0, y), (W / 2, y + sag), (bx1, y)], 1.8, None))
        lines.append(([(fx0, fy0 + (fy1 - fy0) * t), (bx0, y)], 1.4, None))
        lines.append(([(fx1, fy0 + (fy1 - fy0) * t), (bx1, y)], 1.4, None))
    for k in range(0, 9):
        t = k / 8
        lines.append(([(fx0 + (bx0 - fx0) * t, fy0 + (by0 - fy0) * t), (fx1 - (fx1 - bx1) * t, fy0 + (by0 - fy0) * t)], 1.5, None))
    def wob(pts, n=6, j=1.6):
        out = []
        for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
            for q in range(n):
                t = q / n
                out.append((xa + (xb - xa) * t + rng.uniform(-j, j), ya + (yb - ya) * t + rng.uniform(-j, j) + 3 * math.sin(t * math.pi)))
        out.append(pts[-1])
        return curve(out, len(out) * 3)
    lines = [(wob(p_), w_ * 1.05, t_) for p_, w_, t_ in lines]
    mesh = strokes(W, H, lines)
    art = crayon(art, mesh, "#f2f4ef", seed=nx(), amt=0.7, tooth=0.4)
    # back stanchions
    art = GP(art, strokes(W, H, [([(bx0, by0), (bx0, fy1 - 30)], 5, None), ([(bx1, by0), (bx1, fy1 - 30)], 5, None)]), "#c9d1d6", seed=nx(), rough=0.6)
    # front frame: posts + crossbar, white with cool shade
    frame = strokes(W, H, [([(fx0, fy1), (fx0, fy0), (fx1, fy0), (fx1, fy1)], 17, None)], cap=True)
    art = body(art, frame, "#fbfbf7", "#f0f1ec", "#aeb7c2", "#ffffff", nx, ldir=(-6, -6), blur=4, line="#6f7a88")
    art = GP(art, ellipses(W, H, [(fx0, fy1 + 4, 26, 6, 0), (fx1, fy1 + 4, 26, 6, 0)]), "#1b5a28", seed=nx(), rough=1, density=0.4)
    preview(art, "ub-net", tone=BG)
    save(art, f"{OUT}/net.webp", max_w=520, quality=70)
    clear()

if "bunting" in PARTS:
    W, H = 820, 200
    nx = Seq(80700); rng = random.Random(87)
    art = blank(W, H)
    rope = curve([(0, 30), (W * .5, 92), (W, 30)], 80)
    cols = [RED, GOLD, NAVY, CHALK, "#6fb7e6"]
    flags = []
    n = 11
    for i in range(n):
        t = (i + 0.5) / n
        idx = int(t * (len(rope) - 1))
        x, y = rope[idx]
        x2, y2 = rope[min(len(rope) - 1, idx + 1)]
        a = math.atan2(y2 - y, x2 - x)
        hw, L = 30, 70
        p = [(x - math.cos(a) * hw, y - math.sin(a) * hw), (x + math.cos(a) * hw, y + math.sin(a) * hw), (x - math.sin(a) * L + rng.uniform(-3, 3), y + math.cos(a) * L)]
        flags.append((p, cols[i % len(cols)]))
    for p, col in flags:
        m = shapes(W, H, [deform(p, rng, 1, 0.01)], smooth=False)
        m = np.clip(gaussian_filter(m, 1.2) * 1.3, 0, 1)
        art = body(art, m, col, mix(col, "#ffffff", 0.12), mix(col, "#000000", 0.28), mix(col, "#ffffff", 0.45), nx, ldir=(-6, -8), blur=6)
    art = crayon(art, strokes(W, H, [(rope, 3, None)]), "#f7f4ea", seed=nx(), amt=0.9, tooth=0.2)
    preview(art, "ub-bunting", tone=BG)
    save(art, f"{OUT}/bunting.webp", max_w=640, quality=82)
    clear()
