"""Mawar Taif — rose terraces of the Hijaz highlands in loose watercolour: lilac-grey granite ridges, curving dry-stone
terrace walls, rows of damask-rose shrubs speckled pink, big blooms in the foreground, a glass rosewater sprinkler and
drifting petals. Palette: rose pink, stone, sage. No figures.
Run: python3 -I mawar-taif.py [part ...]  parts: valley spray petal bottle divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e3_lib import *
import _jw_lib as jw

OUT = outdir("mawar-taif")
PARTS = sys.argv[1:] or ["valley", "spray", "petal", "bottle", "divider"]
PINK_L, PINK, PINK_D = "#f6cbd3", "#e48aa0", "#b4456a"
STONE_L, STONE, STONE_D = "#d9cbbb", "#ae9c8a", "#6f6156"
RIDGE_A, RIDGE_B = "#c7b4bd", "#a597a6"
SAGE, SAGE_D = "#8fa07e", "#566a4d"
jw.LEAF_A, jw.LEAF_B, jw.LEAF_D = "#93a684", "#5d7552", "#3d5236"


def taif_rose(art, W, H, x, y, r, rng, nx, deep=False):
    return jw.rose(art, W, H, x, y, r, rng, nx, PINK_L, PINK if not deep else "#d9708c", PINK_D)


def leaves(art, W, H, x, y, r, rng, nx, n=4, spread=(0, math.tau)):
    for k in range(n):
        a = rng.uniform(*spread)
        art = jw.leaf(art, W, H, x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.7, r * rng.uniform(0.9, 1.3), a, rng, nx)
    return art


def stone_wall(art, W, H, top, bot, rng, nx, scale=1.0):
    """Dry-stone terrace wall between two curves: irregular rounded stones (jittered Voronoi cells) with dark gaps,
    each stone its own grey-beige wash, shaded toward the foot."""
    from scipy.spatial import cKDTree
    wall = shapes(W, H, [top + bot[::-1]], smooth=False)
    b = bbox(wall, 4)
    y0, y1, x0, x1 = b
    h, w = y1 - y0, x1 - x0
    sx, sy = 20 * scale, 11 * scale
    pts = [(x + rng.uniform(-0.35, 0.35) * sx + (sy if int(y / sy) % 2 else 0), y + rng.uniform(-0.3, 0.3) * sy)
           for y in np.arange(-sy, h + sy, sy) for x in np.arange(-sx, w + sx, sx)]
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    q = np.stack([xx.ravel() * 0.8 + (fbm(w, h, nx(), 8, 2).ravel() - 0.5) * 4, yy.ravel() + (fbm(w, h, nx(), 8, 2).ravel() - 0.5) * 3], -1)
    d, idx = tree.query(q, k=2)
    gap = (d[:, 1] - d[:, 0]).reshape(h, w)
    stone = np.clip((gap - 1.2 * scale) / (1.6 * scale), 0, 1)
    rnd = np.random.default_rng(nx()).random(len(pts)).astype(np.float32)
    tone = rnd[idx[:, 0]].reshape(h, w)
    rgb = col_arr(STONE_L) * (1 - tone[..., None]) + col_arr(STONE) * tone[..., None]
    rgb *= (0.86 + 0.22 * fbm(w, h, nx(), 5, 2))[..., None]
    rgb *= (0.8 + 0.2 * np.clip(gap / (4 * scale), 0, 1))[..., None]  # rounded: darker toward the joints
    rgb = rgb * stone[..., None] + col_arr(STONE_D) * (1 - stone[..., None])
    full = np.zeros((H, W, 3), np.float32); full[y0:y1, x0:x1] = rgb
    a = np.clip((gaussian_filter(displace(wall, nx(), 1.2, 12), 0.7) - 0.3) * 2.4, 0, 1)
    art = over(art, np.concatenate([np.clip(full, 0, 1), (a * 0.9)[..., None]], -1))
    yyf = np.arange(H, dtype=np.float32)[:, None]
    art = G(art, wall * np.clip((yyf - np.array([p[1] for p in top]).mean()) / (30 * scale), 0, 1), "#7b6a73", seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=4, feather=3)
    return art, wall


def shrub_row(art, W, H, pts, size, rng, nx, density=1.0):
    """A row of rose shrubs along a curve: rounded sage mounds dotted with pink blooms."""
    polys = []
    for x, y in pts:
        polys.append(deform(ellipse_pts(x + rng.gauss(0, size * 0.2), y - size * 0.35, size * rng.uniform(0.7, 1.0), size * rng.uniform(0.45, 0.6), 12), rng, 2, 0.12))
    m = shapes(W, H, polys)
    art = G(art, m, SAGE, SAGE_D, seed=nx(), density=0.8, edge=0.5, bloom=0.4, rough=3, gran=0.3)
    sh = shapes(W, H, [deform(ellipse_pts(x + size * 0.25, y - size * 0.1, size * 0.8, size * 0.28, 10), rng, 1, 0.1) for x, y in pts]) * m
    art = G(art, sh, "#3f5138", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2)
    dots = []
    for x, y in pts:
        for _ in range(int(7 * density)):
            dots.append((x + rng.gauss(0, size * 0.55), y - size * 0.4 + rng.gauss(0, size * 0.25), size * rng.uniform(0.09, 0.17)))
    d = circles(W, H, dots) * gaussian_filter(m, 1.5)
    art = G(art, d, PINK, PINK_L, seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=1, feather=0.5)
    d2 = circles(W, H, [(x, y, r * 0.5) for x, y, r in dots[::3]]) * gaussian_filter(m, 1.5)
    return G(art, d2, PINK_D, seed=nx(), density=0.6, edge=0.4, bloom=0, rough=0.6, feather=0.4)


def contour(W, y, amp, ph, n=40, tilt=0.0):
    return [(x, y + amp * math.sin(x / W * math.pi * 1.2 + ph) + tilt * (x - W / 2)) for x in np.linspace(-20, W + 20, n)]


if "valley" in PARTS:
    W, H = 820, 660
    nx = Seq(7100); rng = random.Random(21)
    art = blank(W, H)
    # far granite ridges
    r1 = hills(W, H, 210, 46, 3, 0.7)
    art = G(art, r1, RIDGE_A, "#d8c6cc", seed=nx(), density=0.55, edge=0.45, bloom=0.5, rough=8, feather=2)
    r2 = hills(W, H, 268, 40, 8, 0.45)
    art = G(art, r2, RIDGE_B, RIDGE_A, seed=nx(), density=0.6, edge=0.45, bloom=0.4, rough=7, feather=2)
    # boulders on the slope
    bl = shapes(W, H, [deform(ellipse_pts(rng.uniform(0, W), rng.uniform(270, 320), rng.uniform(10, 26), rng.uniform(7, 14), 10), rng, 2, 0.12) for _ in range(12)])
    art = G(art, bl, "#9b8b92", seed=nx(), density=0.5, edge=0.6, bloom=0.2, rough=2)
    # terraces: field strip then wall, top to bottom, growing with perspective
    y = 300.0
    specs = [(9, 26, 9), (12, 34, 12), (16, 44, 15), (22, 56, 20), (28, 72, 26)]
    for i, (wall_h, field_h, size) in enumerate(specs):
        ph = 0.6 + i * 0.35; amp = 10 + i * 4
        f_top = contour(W, y, amp, ph); f_bot = contour(W, y + field_h, amp, ph)
        field = shapes(W, H, [f_top + f_bot[::-1]], smooth=False)
        art = G(art, field, "#c9bf9e", "#b9b08e", seed=nx(), density=0.75, edge=0.3, bloom=0.4, rough=4, gran=0.5)
        rows = 2 if i > 1 else 1
        for rr in range(rows):
            yy_ = y + field_h * (0.55 + 0.4 * rr / max(1, rows))
            pts = [(x + rng.uniform(-4, 4), yy_ + amp * math.sin(x / W * math.pi * 1.2 + ph)) for x in np.arange(-10 + rr * size, W + 20, size * 1.35)]
            art = shrub_row(art, W, H, pts, size, rng, nx, density=0.8 + 0.1 * i)
        w_top = contour(W, y + field_h, amp, ph); w_bot = contour(W, y + field_h + wall_h, amp, ph)
        art, _ = stone_wall(art, W, H, w_top, w_bot, rng, nx, scale=0.55 + i * 0.22)
        y += field_h + wall_h
        clear()
    # foreground blooms bottom corners
    for (x, yy_, r) in [(70, 600, 54), (150, 640, 40), (20, 520, 34), (760, 610, 50), (690, 650, 36), (810, 520, 30)]:
        art = leaves(art, W, H, x, yy_, r, rng, nx, 4)
    for (x, yy_, r) in [(70, 600, 54), (150, 640, 40), (20, 520, 34), (760, 610, 50), (690, 650, 36), (810, 520, 30)]:
        art = taif_rose(art, W, H, x, yy_, r, rng, nx, deep=r < 40)
        clear()
    preview(art, "mt2-valley", "#fbf1ee")
    save(art, f"{OUT}/valley.webp", max_w=780, quality=78)
    clear()

if "spray" in PARTS:
    W, H = 560, 480
    nx = Seq(7200); rng = random.Random(22)
    art = blank(W, H)
    stems = strokes(W, H, [(curve([(60, 460), (150, 360), (260, 270), (400, 190)], 30), 4), (curve([(150, 360), (110, 250), (140, 140)], 20), 3), (curve([(260, 270), (380, 320), (500, 300)], 20), 3)])
    art = G(art, stems, SAGE_D, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1, feather=0.6)
    for (x, y, L, a) in [(120, 400, 70, -2.4), (200, 320, 64, 0.4), (300, 250, 70, -1.9), (340, 300, 58, 0.9), (130, 200, 56, -2.9), (450, 300, 54, -0.6), (240, 300, 56, 2.6)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx)
    art = taif_rose(art, W, H, 400, 190, 76, rng, nx)
    art = taif_rose(art, W, H, 250, 268, 58, rng, nx, deep=True)
    art = jw.bud(art, W, H, 140, 140, 18, -1.6, rng, nx, PINK, PINK_D)
    art = jw.bud(art, W, H, 500, 300, 15, -0.3, rng, nx, PINK, PINK_D)
    for k in range(5):
        x, y = rng.uniform(60, 520), rng.uniform(40, 440)
        art = G(art, shapes(W, H, [deform(petal_pts(x, y, 22, 12, rng.uniform(0, 6.3)), rng, 1, 0.08)]), PINK_L, PINK, seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=1.5)
    preview(art, "mt2-spray", "#fbf1ee")
    save_full(art, f"{OUT}/spray.webp", size=(420, 360), quality=80)
    clear()

if "petal" in PARTS:
    W, H = 120, 120
    nx = Seq(7300); rng = random.Random(23)
    pm = shapes(W, H, [deform(petal_pts(26, 64, 74, 34, -0.15, n=16, cup=0.25), rng, 1, 0.05)])
    art = G(blank(W, H), pm, PINK_L, PINK, seed=nx(), density=0.85, edge=0.7, bloom=0.4, rough=2)
    art = G(art, pm * light_mask(H, W, 30, 64, 40), PINK_D, seed=nx(), density=0.3, edge=0.2, bloom=0, rough=1, feather=2)
    preview(art, "mt2-petal", "#fbf1ee")
    save_full(art, f"{OUT}/petal.webp", size=(48, 48), quality=84)
    clear()

if "bottle" in PARTS:
    W, H = 320, 640
    nx = Seq(7400); rng = random.Random(24)
    cx = 160
    art = blank(W, H)
    # glass sprinkler: round belly, slim tall neck, flared foot, pierced metal cap
    body = shapes(W, H, [ellipse_pts(cx, 470, 104, 96, 32)])
    neck = shapes(W, H, [[(cx - 15, 400), (cx - 12, 170), (cx - 18, 130), (cx + 18, 130), (cx + 12, 170), (cx + 15, 400)]])
    foot = shapes(W, H, [[(cx - 66, 600), (cx - 46, 562), (cx + 46, 562), (cx + 66, 600), (cx + 60, 610), (cx - 60, 610)]], smooth=False)
    glass = np.maximum.reduce([body, neck, foot])
    art = G(art, glass, "#f4e9ef", "#e7dbe9", seed=nx(), density=0.55, edge=0.8, bloom=0.3, rough=1.5, feather=0.8)
    water = body * (np.arange(H, dtype=np.float32)[:, None] > 445)
    art = G(art, water, "#f2b3c4", "#eaa0b6", seed=nx(), density=0.6, edge=0.6, bloom=0.4, rough=2)
    art = G(art, water * light_mask(H, W, cx + 50, 520, 120), PINK_D, seed=nx(), density=0.25, edge=0.2, bloom=0.3, rough=2, feather=3)
    # glass edges and reflections
    rim = outline(glass, 2.5)
    art = G(art, rim, "#a7909f", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    hl = strokes(W, H, [(arc_pts(cx, 470, 80, 3.5, 4.3, 14), 9), (curve([(cx - 6, 380), (cx - 6, 190)], 12), 3)])
    art = over(art, flat(gaussian_filter(hl, 1.2), "#ffffff", 0.75))
    # silver cap + finial
    cap = shapes(W, H, [[(cx - 20, 136), (cx - 16, 96), (cx, 60), (cx + 16, 96), (cx + 20, 136)]])
    art = GP(art, cap, "#c9c2c4", "#8f8689", seed=nx(), rough=0.6, streak=0.6)
    art = over(art, shade_lr(cap, W, "#4e4649", 0.45))
    holes = circles(W, H, [(cx + dx, 100 + dy, 1.6) for dx, dy in [(-5, 6), (5, 6), (0, -4), (0, 16), (-8, 20), (8, 20)]])
    art = over(art, flat(holes, "#4e4649", 0.8))
    art = GP(art, circles(W, H, [(cx, 56, 7)]), "#d5cfd1", "#9a9194", seed=nx(), rough=0.4)
    # a rose laid at the foot
    art = jw.leaf(art, W, H, 210, 590, 50, -0.4, rng, nx)
    art = taif_rose(art, W, H, 236, 600, 34, rng, nx)
    preview(art, "mt2-bottle", "#fbf1ee")
    save_full(art, f"{OUT}/bottle.webp", size=(180, 360), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 640, 100
    nx = Seq(7500); rng = random.Random(25)
    cy = 56
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 2.2, 0, 1)[None, :]
    stem = strokes(W, H, [(curve([(40, cy + 4), (200, cy - 4), (310, cy + 2)], 30), 2.6, (0.0, 0.0)), (curve([(330, cy + 2), (450, cy + 6), (600, cy - 2)], 30), 2.6, (0.0, 0.0))]) * fade
    art = G(blank(W, H), stem, SAGE_D, seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    for (x, y, L, a) in [(230, cy - 2, 34, -2.6), (410, cy + 4, 34, -0.5), (270, cy + 2, 26, 0.6), (380, cy + 4, 26, 2.5)]:
        art = jw.leaf(art, W, H, x, y, L, a, rng, nx)
    art = taif_rose(art, W, H, 320, cy - 4, 22, rng, nx)
    preview(art, "mt2-divider", "#fbf1ee")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()
