"""Ultah Hutan — kids' woodland birthday in matte gouache: original cute woodland friends (fox, fawn, hedgehog, owl),
red-capped mushrooms, ferns, tall tree trunks, a bunting garland and a tree-ring log slice for the age.
Assets: hutan (forest-floor scene with fox, fawn, hedgehog), batang (tall trunk, mirrored in CSS), bendera (bunting),
burung (owl on a branch, sways), irisan (log slice), jamur (mushroom node), pakis (fern divider).
Run: python3 -I ultah-hutan.py [part ...]
Assets -> public/themes/art/ultah-hutan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s5_lib import *

OUT = outdir("ultah-hutan")
PARTS = sys.argv[1:] or ["hutan", "batang", "bendera", "burung", "irisan", "jamur", "pakis"]
FOX, FOX_D, FOX_L = "#e57a35", "#c25d22", "#f29a5a"
CREAM, CREAM_D = "#fbf1df", "#e6d6bb"
BARK, BARK_D, BARK_L = "#7a5236", "#553823", "#9a6c48"
DEER, DEER_D = "#b9814f", "#93613a"
MOSS, MOSS_D, MOSS_L = "#6e9a4a", "#4c7434", "#9cc06a"
FOREST, FOREST_D = "#3d6b3f", "#2a4d2d"
RED, RED_D = "#d2483a", "#a83429"
INK = "#2a1d18"
OCHRE, OCHRE_D = "#c99a4e", "#a3783a"


def P(pts):
    return shape_mask(*P.wh, pts)


def mushroom(art, W, H, x, y, s, seed, cap=RED, capd=RED_D, dots=True, tilt=0.0):
    stem = [(x - s * 0.22, y), (x - s * 0.17, y - s * 0.75), (x + s * 0.17, y - s * 0.75), (x + s * 0.22, y)]
    stem = rot_pts(stem, x, y, tilt)
    ms = shape_mask(W, H, stem)
    art = GP(art, ms, CREAM, CREAM_D, seed=seed, rough=0.8, streak=0.5)
    art = shade(art, ms, "#cdb894", 0.4, s * 0.08, seed + 1)
    cx, cy = rot_pts([(x, y - s * 0.72)], x, y, tilt)[0]
    capp = [(cx + math.cos(a) * s * 0.62, cy + min(0, math.sin(a)) * s * 0.55 + max(0, math.sin(a)) * s * 0.08) for a in np.linspace(0, math.tau, 40)[:-1]]
    capp = rot_pts(capp, cx, cy, tilt)
    mc = shape_mask(W, H, capp)
    art = GP(art, mc, cap, capd, seed=seed + 2, rough=1.0, streak=0.6)
    art = shade(art, mc, capd, 0.5, s * 0.12, seed + 3)
    if dots:
        rng = random.Random(seed)
        d = [(cx + rng.uniform(-0.45, 0.45) * s, cy - rng.uniform(0.08, 0.42) * s, s * rng.uniform(0.05, 0.09)) for _ in range(6)]
        d = [p for p in d if ((p[0] - cx) / (s * 0.55)) ** 2 + ((p[1] - cy) / (s * 0.5)) ** 2 < 0.8]
        art = GP(art, circles(W, H, d), "#fff8ea", seed=seed + 4, rough=0.4, streak=0.2)
    return art


def fern(art, W, H, x, y, L, ang, seed, col=MOSS, col2=MOSS_D):
    pts = curve([(x, y), (x + math.cos(ang) * L * 0.5 + 12, y + math.sin(ang) * L * 0.5), (x + math.cos(ang) * L, y + math.sin(ang) * L + 10)], 30)
    lv = []
    for i in range(3, len(pts) - 1, 2):
        t = i / len(pts)
        (px, py), (qx, qy) = pts[i], pts[i + 1]
        a = math.atan2(qy - py, qx - px)
        ll = L * 0.2 * (1 - t * 0.75)
        for d in (-1, 1):
            lv.append(petal_pts(px, py, ll, ll * 0.3, a + d * 1.1, n=10))
    art = GP(art, strokes(W, H, [(pts, 3.0, (0.0, 0.6))]), col2, seed=seed, rough=0.4)
    return GP(art, shapes(W, H, lv), col, col2, seed=seed + 1, rough=0.8, streak=0.5)


def grass(art, W, H, x0, x1, y, h, seed, col=MOSS, col2=MOSS_D, n=40):
    rng = random.Random(seed)
    bl = []
    for _ in range(n):
        x = rng.uniform(x0, x1)
        hh = h * rng.uniform(0.5, 1.1)
        bl.append(curve([(x, y + 4), (x + rng.uniform(-4, 4), y - hh * 0.5), (x + rng.uniform(-12, 12), y - hh)], 8))
    return GP(art, strokes(W, H, [(b, 4.5, (0.0, 0.9)) for b in bl]), col, col2, seed=seed, rough=0.5, streak=0.4)


def happy_eyes(art, W, H, pts, r, seed):
    st = [(arc_pts(x, y + r * 0.4, r, math.pi * 1.1, math.pi * 1.9, 10), max(2.0, r * 0.4), (0.2, 0.2)) for x, y in pts]
    return GP(art, strokes(W, H, st), INK, seed=seed, rough=0.3, streak=0.1)


def fox(art, W, H, x, y, s, seed):
    """Sitting fox, front view, tail curled round to the right. (x, y) = bottom centre."""
    # tail
    tail = curve([(x + s * 0.3, y - s * 0.12), (x + s * 0.9, y - s * 0.2), (x + s * 1.1, y - s * 0.7), (x + s * 0.85, y - s * 1.05)], 30)
    mt = strokes(W, H, [(tail, s * 0.42, (0.35, 0.45))])
    art = GP(art, mt, FOX, FOX_D, seed=seed, rough=1.2, streak=0.6)
    tip = strokes(W, H, [(tail[-9:], s * 0.36, (0.0, 0.7))]) * mt
    art = GP(art, tip, CREAM, seed=seed + 1, rough=0.8)
    # body
    body = [(x - s * 0.42, y), (x - s * 0.36, y - s * 0.6), (x - s * 0.18, y - s * 0.95), (x + s * 0.18, y - s * 0.95), (x + s * 0.36, y - s * 0.6), (x + s * 0.42, y)]
    mb = shape_mask(W, H, body)
    art = GP(art, mb, FOX, FOX_D, seed=seed + 2, rough=1.2, streak=0.6)
    art = shade(art, mb, FOX_D, 0.45, s * 0.12, seed + 3)
    chest = [(x - s * 0.2, y - s * 0.15), (x - s * 0.18, y - s * 0.7), (x, y - s * 0.92), (x + s * 0.18, y - s * 0.7), (x + s * 0.2, y - s * 0.15)]
    art = GP(art, shape_mask(W, H, chest), CREAM, CREAM_D, seed=seed + 4, rough=0.8)
    # front paws
    paws = ellipses(W, H, [(x - s * 0.17, y - s * 0.04, s * 0.13, s * 0.07, 0), (x + s * 0.17, y - s * 0.04, s * 0.13, s * 0.07, 0)])
    art = GP(art, paws, "#5a3626", seed=seed + 5, rough=0.5)
    # head
    hy = y - s * 1.22
    ears = [[(x - s * 0.42, hy - s * 0.05), (x - s * 0.36, hy - s * 0.55), (x - s * 0.1, hy - s * 0.2)], [(x + s * 0.42, hy - s * 0.05), (x + s * 0.36, hy - s * 0.55), (x + s * 0.1, hy - s * 0.2)]]
    art = GP(art, shapes(W, H, ears, smooth=False), FOX, FOX_D, seed=seed + 6, rough=0.8)
    inner = [[(x - s * 0.35, hy - s * 0.12), (x - s * 0.34, hy - s * 0.42), (x - s * 0.18, hy - s * 0.2)], [(x + s * 0.35, hy - s * 0.12), (x + s * 0.34, hy - s * 0.42), (x + s * 0.18, hy - s * 0.2)]]
    art = GP(art, shapes(W, H, inner, smooth=False), "#5a3626", seed=seed + 7, rough=0.5)
    head = [(x - s * 0.5, hy + s * 0.02), (x - s * 0.3, hy - s * 0.26), (x + s * 0.3, hy - s * 0.26), (x + s * 0.5, hy + s * 0.02), (x + s * 0.12, hy + s * 0.32), (x, hy + s * 0.36), (x - s * 0.12, hy + s * 0.32)]
    mh = shape_mask(W, H, head)
    art = GP(art, mh, FOX_L, FOX, seed=seed + 8, rough=1.0, streak=0.5)
    cheeks_ = [[(x - s * 0.5, hy + s * 0.02), (x - s * 0.18, hy + s * 0.04), (x - s * 0.04, hy + s * 0.3), (x - s * 0.12, hy + s * 0.32)], [(x + s * 0.5, hy + s * 0.02), (x + s * 0.18, hy + s * 0.04), (x + s * 0.04, hy + s * 0.3), (x + s * 0.12, hy + s * 0.32)]]
    art = GP(art, shapes(W, H, cheeks_), CREAM, CREAM_D, seed=seed + 9, rough=0.6)
    art = GP(art, ellipses(W, H, [(x, hy + s * 0.31, s * 0.06, s * 0.045, 0)]), INK, seed=seed + 10, rough=0.3)
    art = happy_eyes(art, W, H, [(x - s * 0.18, hy - s * 0.04), (x + s * 0.18, hy - s * 0.04)], s * 0.07, seed + 11)
    art = cheeks(art, W, H, [(x - s * 0.28, hy + s * 0.1), (x + s * 0.28, hy + s * 0.1)], s * 0.06, seed + 12)
    return art


def fawn(art, W, H, x, y, s, seed):
    """Standing fawn, side view facing left. (x, y) = ground under the body centre."""
    legs = []
    for lx, d in ((-0.42, 0), (-0.28, 0.03), (0.3, 0), (0.44, 0.03)):
        legs.append(([(x + lx * s, y - s * 0.62), (x + (lx + d) * s, y - s * 0.3), (x + (lx + d) * s, y - s * 0.02)], s * 0.075, (0.0, 0.0)))
    art = GP(art, strokes(W, H, legs[1::2]), DEER_D, seed=seed, rough=0.5)
    art = GP(art, strokes(W, H, legs[0::2]), DEER, DEER_D, seed=seed + 1, rough=0.5)
    hooves = circles(W, H, [(x + (lx + d) * s, y - s * 0.02, s * 0.045) for lx, d in ((-0.42, 0), (-0.28, 0.03), (0.3, 0), (0.44, 0.03))])
    art = GP(art, hooves, "#4a3224", seed=seed + 2, rough=0.3)
    body = ellipse_pts(x, y - s * 0.74, s * 0.56, s * 0.3, 30)
    mb = shape_mask(W, H, body)
    art = GP(art, mb, DEER, DEER_D, seed=seed + 3, rough=1.0, streak=0.6)
    art = shade(art, mb, DEER_D, 0.4, 0, seed + 4, dy=-s * 0.1)
    belly = ellipse_pts(x + s * 0.02, y - s * 0.55, s * 0.3, s * 0.08, 20)
    art = GP(art, shape_mask(W, H, belly) * mb, CREAM, seed=seed + 5, rough=0.6)
    rng = random.Random(seed)
    spots = [(x + rng.uniform(-0.35, 0.4) * s, y - s * rng.uniform(0.84, 0.94), s * rng.uniform(0.025, 0.04)) for _ in range(8)]
    art = GP(art, circles(W, H, spots), CREAM, seed=seed + 6, rough=0.3)
    tail = ellipse_pts(x + s * 0.58, y - s * 0.86, s * 0.08, s * 0.05, 10, 0.5)
    art = GP(art, shape_mask(W, H, tail), CREAM, seed=seed + 7, rough=0.4)
    neck = [(x - s * 0.52, y - s * 0.78), (x - s * 0.66, y - s * 1.2), (x - s * 0.42, y - s * 1.26), (x - s * 0.24, y - s * 0.9)]
    art = GP(art, shape_mask(W, H, neck), DEER, DEER_D, seed=seed + 8, rough=0.8)
    hx, hy = x - s * 0.62, y - s * 1.32
    ears = [petal_pts(hx + s * 0.1, hy - s * 0.08, s * 0.3, s * 0.12, -0.5, n=12), petal_pts(hx + s * 0.05, hy - s * 0.1, s * 0.28, s * 0.11, -2.3, n=12)]
    art = GP(art, shapes(W, H, ears), DEER, DEER_D, seed=seed + 9, rough=0.6)
    art = GP(art, shape_mask(W, H, petal_pts(hx + s * 0.12, hy - s * 0.1, s * 0.2, s * 0.06, -0.5, n=10)), "#e9b9a0", seed=seed + 10, rough=0.4)
    head = ellipse_pts(hx, hy, s * 0.2, s * 0.17, 20)
    art = GP(art, shape_mask(W, H, head), DEER, DEER_D, seed=seed + 11, rough=0.8)
    snout = ellipse_pts(hx - s * 0.18, hy + s * 0.06, s * 0.12, s * 0.09, 16, -0.3)
    art = GP(art, shape_mask(W, H, snout), CREAM, CREAM_D, seed=seed + 12, rough=0.5)
    art = GP(art, circles(W, H, [(hx - s * 0.28, hy + s * 0.02, s * 0.035)]), INK, seed=seed + 13, rough=0.2)
    art = eye(art, W, H, hx - s * 0.04, hy - s * 0.03, s * 0.045, seed + 14, INK)
    art = cheeks(art, W, H, [(hx + s * 0.02, hy + s * 0.08)], s * 0.045, seed + 15)
    return art


def hedgehog(art, W, H, x, y, s, seed):
    """Hedgehog facing left. (x, y) = ground under the body."""
    rng = random.Random(seed)
    spk = []
    for a in np.linspace(math.pi * 0.98, math.pi * 2.08, 26):
        r = s * (0.62 + rng.uniform(-0.03, 0.05))
        spk.append((x + math.cos(a) * s * 0.55, y - s * 0.3 + math.sin(a) * s * 0.42))
        spk.append((x + math.cos(a + 0.06) * (r + s * 0.18), y - s * 0.3 + math.sin(a + 0.06) * (r * 0.75 + s * 0.12)))
    spk += [(x + s * 0.6, y - s * 0.05), (x - s * 0.3, y - s * 0.05)]
    ms = shape_mask(W, H, spk, smooth=False)
    art = GP(art, ms, "#7a5a40", "#5c4130", seed=seed, rough=1.0, streak=0.8)
    quills = [([(x + math.cos(a) * s * 0.3, y - s * 0.3 + math.sin(a) * s * 0.22), (x + math.cos(a) * s * 0.66, y - s * 0.3 + math.sin(a) * s * 0.5)], 2.2, (0.0, 0.8)) for a in np.linspace(math.pi * 1.05, math.pi * 1.95, 14)]
    art = GP(art, strokes(W, H, quills) * ms, "#c9a37a", seed=seed + 1, rough=0.3, density=0.8)
    face = [(x - s * 0.3, y - s * 0.05), (x - s * 0.34, y - s * 0.42), (x - s * 0.62, y - s * 0.2), (x - s * 0.8, y - s * 0.12), (x - s * 0.62, y - s * 0.02)]
    art = GP(art, shape_mask(W, H, face), "#e3c49c", "#d0ab80", seed=seed + 2, rough=0.6)
    art = GP(art, circles(W, H, [(x - s * 0.8, y - s * 0.13, s * 0.06)]), INK, seed=seed + 3, rough=0.2)
    art = eye(art, W, H, x - s * 0.48, y - s * 0.25, s * 0.05, seed + 4, INK)
    art = cheeks(art, W, H, [(x - s * 0.44, y - s * 0.12)], s * 0.05, seed + 5)
    feet = ellipses(W, H, [(x - s * 0.25, y - s * 0.02, s * 0.08, s * 0.04, 0), (x + s * 0.3, y - s * 0.02, s * 0.08, s * 0.04, 0)])
    art = GP(art, feet, "#c99a72", seed=seed + 6, rough=0.3)
    # a little apple on its back
    art = GP(art, circles(W, H, [(x + s * 0.08, y - s * 0.78, s * 0.14)]), RED, RED_D, seed=seed + 7, rough=0.5)
    art = GP(art, shape_mask(W, H, petal_pts(x + s * 0.1, y - s * 0.9, s * 0.14, s * 0.06, -0.6, n=10)), MOSS, seed=seed + 8, rough=0.3)
    return art


def ground(art, W, H, y, seed):
    top = [(x, y + 8 * math.sin(x / 60) + 4 * math.sin(x / 17)) for x in range(-10, W + 20, 10)]
    m = shape_mask(W, H, top + [(W + 10, H + 10), (-10, H + 10)], smooth=False)
    art = GP(art, m, MOSS, MOSS_D, seed=seed, rough=1.5, streak=0.8)
    yy = np.arange(H)[:, None] * np.ones((1, W))
    art = GP(art, m * np.clip((yy - y - 30) / 80, 0, 1), FOREST, FOREST_D, seed=seed + 1, rough=1, streak=0.8, density=0.85)
    rng = random.Random(seed)
    dabs = [petal_pts(rng.uniform(0, W), rng.uniform(y + 10, H - 4), rng.uniform(6, 12), 2.5, rng.uniform(-2.0, -1.1), n=8) for _ in range(90)]
    art = GP(art, shapes(W, H, dabs) * m, MOSS_L, seed=seed + 2, rough=0.4, density=0.7)
    return art


def hutan():
    W, H = 780, 430
    clear()
    art = blank(W, H)
    gy = 330
    # back ferns and grass
    for i, (x, L, a) in enumerate([(30, 150, -1.9), (70, 130, -1.3), (250, 110, -1.7), (520, 120, -1.5), (700, 150, -1.25), (760, 120, -1.9)]):
        art = fern(art, W, H, x, gy + 10, L, a, 10 + i, MOSS_D, FOREST)
    art = ground(art, W, H, gy, 20)
    clear()
    art = grass(art, W, H, 0, W, gy + 8, 30, 21, MOSS, MOSS_D, 60)
    # mushrooms (back)
    art = mushroom(art, W, H, 255, gy + 34, 70, 30, tilt=-0.1)
    art = mushroom(art, W, H, 292, gy + 40, 44, 31, cap="#c47b45", capd="#9a5a2e", dots=False, tilt=0.15)
    art = mushroom(art, W, H, 735, gy + 40, 92, 32, tilt=0.06)
    clear()
    art = fawn(art, W, H, 150, gy + 50, 150, 40)
    clear()
    art = fox(art, W, H, 455, gy + 56, 130, 50)
    clear()
    art = hedgehog(art, W, H, 640, gy + 66, 92, 60)
    clear()
    # front mushrooms and flowers
    art = mushroom(art, W, H, 335, gy + 80, 52, 33, tilt=0.1)
    art = mushroom(art, W, H, 40, gy + 86, 56, 34, tilt=-0.12)
    art = mushroom(art, W, H, 560, gy + 90, 38, 35, cap="#c47b45", capd="#9a5a2e", dots=False)
    rng = random.Random(70)
    fl = []
    for _ in range(14):
        fx, fy = rng.uniform(10, W - 10), rng.uniform(gy + 40, H - 14)
        fl.append((fx, fy))
    pet = [petal_pts(fx, fy, 7, 3.2, a, n=8) for fx, fy in fl for a in np.linspace(0, math.tau, 6)[:-1] + rng.uniform(0, 1)]
    art = GP(art, shapes(W, H, pet), "#fff6e6", "#f3dfc8", seed=71, rough=0.4)
    art = GP(art, circles(W, H, [(fx, fy, 2.6) for fx, fy in fl]), "#f2b632", seed=72, rough=0.3)
    art = grass(art, W, H, 0, W, H - 2, 26, 73, MOSS_L, MOSS, 40)
    preview(art, "hutan", tone="#eef3e0")
    save(art, f"{OUT}/hutan.webp", max_w=780)


def batang():
    """Tall birch-ish trunk with bark marks, one branch stub, ivy; left-hand trunk (mirror for the right)."""
    W, H = 200, 1100
    clear()
    art = blank(W, H)
    rng = random.Random(4)
    edge_l = [(40 + 10 * math.sin(y / 140) + (y / H) * -10, y) for y in range(-10, H + 20, 20)]
    edge_r = [(132 + 8 * math.sin(y / 120 + 1) - (y / H) * -26, y) for y in range(H + 10, -20, -20)]
    m = shape_mask(W, H, edge_l + edge_r, smooth=False)
    art = GP(art, m, BARK, BARK_L, seed=3, rough=1.5, streak=1.0)
    art = shade(art, m, BARK_D, 0.6, 26, 4)
    # roots flare
    root = [(10, H), (34, H - 70), (60, H - 120), (150, H - 120), (176, H - 60), (200, H)]
    art = GP(art, shape_mask(W, H, root), BARK, BARK_D, seed=5, rough=1.2, streak=0.8)
    marks = []
    for _ in range(46):
        y = rng.uniform(0, H - 40)
        x = rng.uniform(52, 125)
        L = rng.uniform(10, 30)
        marks.append(curve([(x, y), (x + L * 0.5, y + rng.uniform(-3, 3)), (x + L, y + rng.uniform(-2, 4))], 8))
    art = GP(art, strokes(W, H, [(p, rng.uniform(2.0, 3.5), (0.3, 0.4)) for p in marks]) * m, BARK_D, seed=6, rough=0.4, density=0.8)
    hl = strokes(W, H, [(curve([(58, 0), (54, 300), (60, 600), (56, 900), (50, H)], 40), 6, (0.05, 0.05))]) * m
    art = GP(art, hl, BARK_L, seed=7, rough=0.6, density=0.55)
    # knot hole
    art = GP(art, ellipses(W, H, [(92, 520, 14, 20, 0)]), "#3e2718", seed=8, rough=0.5)
    art = GP(art, np.clip(ellipses(W, H, [(92, 520, 19, 25, 0)]) - ellipses(W, H, [(92, 520, 13, 19, 0)]), 0, 1), BARK_L, seed=9, rough=0.4, density=0.8)
    # branch to the right (into the page) near the top
    br = [(120, 250), (200, 214), (200, 236), (126, 284)]
    art = GP(art, shape_mask(W, H, br), BARK, BARK_D, seed=10, rough=1.0, streak=0.6)
    lv = [petal_pts(180 + rng.uniform(-30, 16), 214 + rng.uniform(-30, 26), rng.uniform(16, 24), 7, rng.uniform(-2.8, 0.4), n=10) for _ in range(9)]
    art = GP(art, shapes(W, H, lv), MOSS, MOSS_D, seed=11, rough=0.6)
    # ivy winding up
    ivy = curve([(70, H - 100), (120, H - 260), (60, H - 420), (118, H - 590), (66, H - 760)], 80)
    art = GP(art, strokes(W, H, [(ivy, 2.6, (0.0, 0.1))]), FOREST, seed=12, rough=0.3)
    il = []
    for i in range(4, len(ivy), 6):
        px, py = ivy[i]
        for d in (-1, 1):
            il.append([(px, py), (px + d * 13, py - 4), (px + d * 8, py - 14), (px + d * 2, py - 8)])
    art = GP(art, shapes(W, H, il), MOSS, FOREST, seed=13, rough=0.5)
    # moss at the foot
    moss = ellipses(W, H, [(rng.uniform(20, 180), H - rng.uniform(0, 40), rng.uniform(12, 24), rng.uniform(6, 12), 0) for _ in range(14)])
    art = GP(art, moss, MOSS, MOSS_L, seed=14, rough=1.0)
    preview(art, "batang", tone="#eef3e0")
    save(art, f"{OUT}/batang.webp", max_w=150)


def bendera():
    """Bunting garland sagging across the page with triangular flags in woodland colours."""
    W, H = 780, 150
    clear()
    art = blank(W, H)
    rope = curve([(-10, 20), (390, 70), (790, 20)], 80)
    art = GP(art, strokes(W, H, [(rope, 3.0, (0.0, 0.0))]), "#8a6a4a", seed=3, rough=0.3)
    cols = [(RED, RED_D), (OCHRE, OCHRE_D), (MOSS, MOSS_D), (FOX, FOX_D), (CREAM, CREAM_D), ("#8fb0c8", "#6f90a8")]
    flags = []
    n = 13
    for i in range(n):
        t = (i + 0.5) / n
        idx = int(t * (len(rope) - 1))
        (x0, y0), (x1, y1) = rope[max(0, idx - 3)], rope[min(len(rope) - 1, idx + 3)]
        a = math.atan2(y1 - y0, x1 - x0)
        cx, cy = rope[idx]
        w = 25
        p1 = (cx - math.cos(a) * w, cy - math.sin(a) * w)
        p2 = (cx + math.cos(a) * w, cy + math.sin(a) * w)
        tip = (cx - math.sin(a) * 58 * -1 * -1 + 0, cy + 58)
        tip = (cx + math.sin(-a) * 0 , cy + 58)
        m = shape_mask(W, H, [p1, p2, tip], smooth=False)
        c1, c2 = cols[i % len(cols)]
        art = GP(art, m, c1, c2, seed=10 + i, rough=1.0, streak=0.6)
        art = shade(art, m, c2, 0.35, 8, 30 + i)
        flags.append((cx, cy + 14))
    dots = [(x + d * 7, y + 6, 3) for x, y in flags[::2] for d in (-1, 1)]
    art = GP(art, circles(W, H, dots), "#fff8ea", seed=50, rough=0.3, density=0.85)
    preview(art, "bendera", tone="#eef3e0")
    save(art, f"{OUT}/bendera.webp", max_w=780)


def owl(art, W, H, x, y, s, seed):
    """Round owl sitting; (x, y) = feet."""
    body = ellipse_pts(x, y - s * 0.62, s * 0.5, s * 0.62, 34)
    mb = shape_mask(W, H, body)
    tufts = [[(x - s * 0.42, y - s * 1.0), (x - s * 0.48, y - s * 1.32), (x - s * 0.2, y - s * 1.12)], [(x + s * 0.42, y - s * 1.0), (x + s * 0.48, y - s * 1.32), (x + s * 0.2, y - s * 1.12)]]
    art = GP(art, shapes(W, H, tufts), OCHRE, OCHRE_D, seed=seed, rough=0.6)
    art = GP(art, mb, OCHRE, "#b98a44", seed=seed + 1, rough=1.0, streak=0.6)
    art = shade(art, mb, OCHRE_D, 0.5, s * 0.12, seed + 2)
    belly = ellipse_pts(x, y - s * 0.45, s * 0.3, s * 0.36, 24)
    art = GP(art, shape_mask(W, H, belly), CREAM, CREAM_D, seed=seed + 3, rough=0.6)
    vs = []
    for r, xs in ((0.62, (-0.12, 0.0, 0.12)), (0.45, (-0.18, -0.06, 0.06, 0.18)), (0.28, (-0.12, 0.0, 0.12))):
        for dx in xs:
            vs.append(([(x + (dx - 0.04) * s, y - r * s - 0.03 * s), (x + dx * s, y - r * s), (x + (dx + 0.04) * s, y - r * s - 0.03 * s)], 2.0, None))
    art = GP(art, strokes(W, H, vs), OCHRE_D, seed=seed + 4, rough=0.3)
    wings = [ellipse_pts(x - s * 0.44, y - s * 0.55, s * 0.14, s * 0.36, 20, 0.2), ellipse_pts(x + s * 0.44, y - s * 0.55, s * 0.14, s * 0.36, 20, -0.2)]
    art = GP(art, shapes(W, H, wings), "#a3783a", "#8a6230", seed=seed + 5, rough=0.6, streak=0.5)
    # eye discs
    for d in (-1, 1):
        ex, ey = x + d * s * 0.19, y - s * 0.92
        art = GP(art, circles(W, H, [(ex, ey, s * 0.2)]), CREAM, "#fff7e6", seed=seed + 6 + d, rough=0.5)
        art = GP(art, np.clip(circles(W, H, [(ex, ey, s * 0.22)]) - circles(W, H, [(ex, ey, s * 0.19)]), 0, 1), OCHRE_D, seed=seed + 8 + d, rough=0.3, density=0.8)
        art = eye(art, W, H, ex, ey + s * 0.01, s * 0.085, seed + 10 + d, INK)
    beak = [(x - s * 0.06, y - s * 0.8), (x + s * 0.06, y - s * 0.8), (x, y - s * 0.67)]
    art = GP(art, shape_mask(W, H, beak), "#f2b632", "#d9952a", seed=seed + 12, rough=0.3)
    art = cheeks(art, W, H, [(x - s * 0.3, y - s * 0.72), (x + s * 0.3, y - s * 0.72)], s * 0.06, seed + 13)
    feet = [([(x + d * s * 0.14 + k * s * 0.04, y - s * 0.06), (x + d * s * 0.14 + k * s * 0.05, y + s * 0.03)], 3.0, None) for d in (-1, 1) for k in (-1, 0, 1)]
    art = GP(art, strokes(W, H, feet), "#e09a3a", seed=seed + 14, rough=0.3)
    return art


def burung():
    W, H = 260, 250
    clear()
    art = blank(W, H)
    branch = [(0, 200), (260, 186), (260, 204), (0, 222)]
    art = GP(art, shape_mask(W, H, branch), BARK, BARK_D, seed=3, rough=1.0, streak=0.8)
    art = GP(art, strokes(W, H, [([(10, 211), (250, 195)], 2.0, (0.1, 0.1))]), BARK_D, seed=4, rough=0.3, density=0.7)
    lv = [petal_pts(x, y, 22, 8, a, n=10) for x, y, a in [(30, 200, 2.4), (44, 214, 1.6), (228, 192, -0.7), (240, 202, 0.4)]]
    art = GP(art, shapes(W, H, lv), MOSS, MOSS_D, seed=5, rough=0.5)
    art = owl(art, W, H, 130, 200, 150, 10)
    preview(art, "burung", tone="#eef3e0")
    save(art, f"{OUT}/burung.webp", max_w=200)


def irisan():
    """Log slice: bark ring, pale wood with concentric growth rings and a crack."""
    W, H = 340, 340
    clear()
    art = blank(W, H)
    cx, cy, R = 170, 170, 150
    rng = random.Random(5)
    outer = [(cx + math.cos(a) * R * (1 + rng.uniform(-0.02, 0.02)), cy + math.sin(a) * R * (1 + rng.uniform(-0.02, 0.02))) for a in np.linspace(0, math.tau, 48)[:-1]]
    art = GP(art, shape_mask(W, H, outer), BARK, BARK_D, seed=3, rough=1.2, streak=0.8)
    inner = [(cx + math.cos(a) * R * 0.88 * (1 + rng.uniform(-0.015, 0.015)), cy + math.sin(a) * R * 0.88 * (1 + rng.uniform(-0.015, 0.015))) for a in np.linspace(0, math.tau, 48)[:-1]]
    mi = shape_mask(W, H, inner)
    art = GP(art, mi, "#f1d6a8", "#e6c48e", seed=4, rough=0.8, streak=0.6)
    rings = []
    for k, r in enumerate(np.linspace(0.12, 0.8, 8)):
        rings.append(([(cx + 4 + math.cos(a) * R * r * (1 + 0.03 * math.sin(a * 3 + k)), cy + 2 + math.sin(a) * R * r * (1 + 0.03 * math.cos(a * 2 + k))) for a in np.linspace(0, math.tau, 90)], 2.2, None))
    art = GP(art, strokes(W, H, rings) * mi, "#c89a62", seed=5, rough=0.4, density=0.75)
    crack = [(cx + 10, cy + 4), (cx + 40, cy + 30), (cx + 70, cy + 44), (cx + 110, cy + 70)]
    art = GP(art, strokes(W, H, [(crack, 3.0, (0.1, 0.6))]) * mi, "#a3783a", seed=6, rough=0.3)
    preview(art, "irisan", tone="#eef3e0")
    save(art, f"{OUT}/irisan.webp", max_w=260)


def jamur():
    W, H = 160, 180
    clear()
    art = mushroom(blank(W, H), W, H, 80, 166, 120, 7)
    art = grass(art, W, H, 40, 120, 168, 18, 8, MOSS, MOSS_D, 10)
    preview(art, "jamur", tone="#eef3e0")
    save(art, f"{OUT}/jamur.webp", max_w=90)


def pakis():
    """Divider: two ferns reaching out from a small mushroom pair."""
    W, H = 520, 110
    clear()
    art = blank(W, H)
    art = fern(art, W, H, W / 2 - 24, 86, 200, math.pi + 0.18, 3)
    art = fern(art, W, H, W / 2 + 24, 86, 200, -0.18, 4)
    art = mushroom(art, W, H, W / 2 - 6, 96, 64, 5, tilt=-0.08)
    art = mushroom(art, W, H, W / 2 + 22, 98, 38, 6, cap="#c47b45", capd="#9a5a2e", dots=False, tilt=0.15)
    preview(art, "pakis", tone="#eef3e0")
    save(art, f"{OUT}/pakis.webp", max_w=400)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
