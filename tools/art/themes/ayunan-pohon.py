"""Ayunan Pohon — storybook gouache at golden hour: a big old tree on a hill with a wooden rope swing on its long
branch, the meadow below, a low sun behind far hills. Pieces: the scene (swing painted separately so it can sway),
the swing, a leafy twig divider, a wildflower posy. Run: python3 -I ayunan-pohon.py [part ...]
parts: bukit ayunan ranting bunga   Assets -> public/themes/art/ayunan-pohon/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s2_lib import *

OUT = outdir("ayunan-pohon")
PARTS = sys.argv[1:] or ["bukit", "ayunan", "ranting", "bunga"]
LINE = "#4a3222"
BARK, BARK_D, BARK_L = "#6e4a32", "#4a2f1f", "#b57d4c"
G_D, G_M, G_L, G_GOLD = "#3d5638", "#5f7f45", "#97a855", "#e0c066"
GRASS_L, GRASS_M, GRASS_D = "#c7b85e", "#93a14f", "#627a3f"
CREAM, CORAL, LAV = "#fbf1dc", "#e9876a", "#b9a3d1"


def canopy(art, W, H, cx, cy, rx, ry, rng, n=60, sun=(-1, -1), rmin=26, rmax=58, ndab=4):
    """Clusters of leaf masses, lit from the sun side, with small leaf dabs on the rims."""
    clusters = []
    for _ in range(n):
        a = rng.uniform(0, math.tau); d = rng.random() ** 0.6
        x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d
        r = rng.uniform(rmin, rmax) * (1.1 - d * 0.4)
        clusters.append((x, y, r))
    clusters.sort(key=lambda c: c[1])
    mass = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 0.82, 12), rng, 2, .14) for x, y, r in clusters])
    art = paint(art, mass, G_D, "#33492f", px=1.4, dens=0.35, lc="#2b3a26")
    # mid-tone tops of each cluster (offset towards the sun)
    mids = shapes(W, H, [deform(ellipse_pts(x + sun[0] * r * .18, y + sun[1] * r * .22, r * .78, r * .6, 12), rng, 2, .14) for x, y, r in clusters])
    art = GP(art, mids * mass, G_M, "#56743f", seed=rs(), rough=1.8, streak=0.8, pad=10)
    # lit tops on the sun side of the whole crown
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = np.clip(((cx - xx) * -sun[0] * 0.6 + (cy - yy) * -sun[1]) / max(rx, ry) + 0.2, 0, 1)
    lits = shapes(W, H, [deform(ellipse_pts(x + sun[0] * r * .32, y + sun[1] * r * .36, r * .5, r * .34, 10), rng, 2, .16) for x, y, r in clusters])
    art = GP(art, lits * mass * np.clip(side * 1.6, 0, 1), G_L, G_GOLD, seed=rs(), rough=1.6, streak=0.8, pad=10)
    art = GP(art, lits * mass * np.clip((side - 0.45) * 2.4, 0, 1), G_GOLD, "#f0d27c", seed=rs(), rough=1.4, streak=0.6, pad=10)
    # leaf dabs around the rim
    dabs = []
    rim = []
    for (x, y, r) in clusters:
        for _ in range(ndab):
            a = rng.uniform(0, math.tau)
            px_, py_ = x + math.cos(a) * r * 0.95, y + math.sin(a) * r * 0.8
            dabs.append(petal_pts(px_, py_, rng.uniform(9, 15), rng.uniform(4, 6), a + rng.uniform(-.5, .5), n=8))
    dm = shapes(W, H, dabs)
    art = paint(art, dm * (1 - mass * 0.0), G_M, G_D, px=0.9, dens=0.3, lc="#2b3a26")
    art = GP(art, dm * np.clip(side * 1.4, 0, 1), G_L, G_GOLD, seed=rs(), rough=1, pad=8)
    return art, mass


def flowers(art, W, H, pts, rng, cols=(CREAM, CORAL, LAV, "#f3cf5a")):
    for k, col in enumerate(cols):
        items = []
        for (x, y, r) in pts[k::len(cols)]:
            items += [(x + math.cos(j * 1.256 + r) * r * .55, y + math.sin(j * 1.256 + r) * r * .45, r * .5) for j in range(5)]
        art = paint(art, circles(W, H, items), col, mix(col, "#000000", .1), px=0.8, dens=0.35, lc=LINE)
    art = GP(art, circles(W, H, [(x, y, r * .25) for x, y, r in pts]), "#7a5a2e", seed=rs(), rough=0.5, pad=6)
    return art


random.seed(5)

if "bukit" in PARTS:
    W, H = 780, 1400
    rng = random.Random(9); nx = Seq(900)
    art = painted_sky(W, H, [(0, "#f2c086"), (0.3, "#f6d49f"), (0.5, "#f7d9a4"), (0.62, "#f1c48c"), (1, "#e9cf96")], seed=4, streak=0.5, grain=0.3)
    # low sun on the left behind far hills, with a warm halo
    sun = (210, 742)
    art = OV(art, circles(W, H, [(sun[0], sun[1], 70)]), lambda m: glow(m, "#fff3cf", 90, 1.2), pad=300)
    art = GP(art, circles(W, H, [(sun[0], sun[1], 54)]), "#fbd98a", "#f6c56c", seed=nx(), rough=1.0, pad=8)
    # soft clouds stroked horizontally
    for (x, y, w_) in [(120, 360, 160), (520, 250, 220), (300, 560, 140), (640, 640, 120)]:
        cm = shapes(W, H, [deform(ellipse_pts(x, y, w_, 16, 14), rng, 2, .1)])
        art = G(art, cm, "#fff3dc", "#fbe2bd", seed=nx(), density=0.55, edge=0.2, bloom=0.4, rough=6)
        art = G(art, cm * light_side(cm, 0, -5, 3), "#e9a98a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3)
    clear()
    # far hills (lavender haze), then mid hills
    art = paint(art, hills(W, H, 820, 34, 3, 0.8), "#c6b3c4", "#b9a6bb", ln=False)
    art = paint(art, hills(W, H, 872, 14, 8, 0.6), "#b5a76e", "#a39a66", ln=False)
    # distant tree line dots on the mid hill
    tl = [deform(ellipse_pts(x, 866 + 5 * math.sin(x / 90) + rng.uniform(-3, 3), rng.uniform(8, 14), rng.uniform(7, 11), 9), rng, 1, .1) for x in range(-10, 330, 18)]
    art = paint(art, shapes(W, H, tl), "#8d9670", ln=False)
    # meadow plain below the far hills: soft field bands and a few distant trees
    plain = np.clip(hills(W, H, 880, 6, 12, 0.6), 0, 1)
    bands = strokes(W, H, [([(-10, 900 + k * 22 + rng.uniform(-3, 3)), (W + 10, 896 + k * 24 + rng.uniform(-3, 3))], 6 + k * 1.5, None) for k in range(8)]) * plain
    art = G(art, bands, "#c9b46c", "#a8a565", seed=nx(), density=0.4, edge=0.2, bloom=0.3, rough=4)
    for (x, y, r) in [(60, 905, 16), (96, 910, 11), (380, 902, 13), (430, 908, 18)]:
        art = paint(art, strokes(W, H, [([(x, y), (x, y + r * 1.4)], 3, None)]), "#6e5640", ln=False)
        cr = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 1.1, 10), rng, 1, .1)])
        art = paint(art, cr, "#7f8a55", "#6b7748", ln=False)
        art = GP(art, light_side(cr, 3, 3, 2), "#c9bb6a", seed=nx(), rough=0.6, pad=6)
    clear()
    # the big hill (rising to the right), golden grass lit from the left
    top = [(x, 1060 - 230 * (1 / (1 + math.exp(-(x - 360) / 120))) + 10 * math.sin(x / 70)) for x in range(-20, W + 40, 20)]
    hill = shapes(W, H, [top + [(W + 20, H + 20), (-20, H + 20)]], smooth=False)
    art = paint(art, hill, GRASS_M, GRASS_D, px=1.4, dens=0.4, lc="#4f5f32", streak=0.9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rim = np.clip(hill - np.roll(gaussian_filter(hill, 14), 18, 0), 0, 1)
    art = GP(art, rim * np.clip(1.2 - xx / W, 0, 1), GRASS_L, "#e1c66a", seed=nx(), rough=2, streak=0.9, pad=10)
    # long tree shadow across the hill to the right
    shd = shapes(W, H, [deform([(560, 840), (800, 900), (800, 980), (600, 900)], rng, 2, .05)])
    art = G(art, shd * hill, "#3f5a35", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=6)
    clear()
    # the old tree: wide trunk with roots, gnarled limbs
    tx = 590
    trunk = [(tx - 130, 908), (tx - 70, 830), (tx - 58, 720), (tx - 72, 620), (tx - 40, 520), (tx + 10, 470), (tx + 60, 520), (tx + 66, 620), (tx + 70, 720), (tx + 90, 826), (tx + 160, 872), (tx + 50, 880), (tx + 10, 890), (tx - 40, 892)]
    tm = shapes(W, H, [deform(trunk, rng, 2, .03)])
    limbs = [
        (curve([(tx - 40, 600), (tx - 150, 520), (tx - 300, 478), (tx - 420, 476), (tx - 470, 468)], 50), 50, (0.02, 0.6)),   # the swing branch
        (curve([(tx + 10, 520), (tx + 50, 400), (tx + 110, 330), (tx + 180, 290)], 40), 52, (0.02, 0.5)),
        (curve([(tx - 6, 520), (tx - 50, 380), (tx - 100, 300), (tx - 170, 250)], 40), 48, (0.02, 0.5)),
        (curve([(tx + 40, 580), (tx + 110, 530), (tx + 190, 520)], 30), 34, (0.02, 0.5)),
    ]
    lm = strokes(W, H, limbs)
    wood = np.maximum(tm, lm)
    art = paint(art, wood, BARK, BARK_D, px=1.6, dens=0.6, lc="#2e1d12")
    # bark grooves + rim light from the sun (left)
    grooves = [(curve([(tx - 70 + k * 16 + rng.uniform(-3, 3), 860), (tx - 50 + k * 12, 700), (tx - 30 + k * 8 + rng.uniform(-4, 4), 520)], 20), 3.0, (0.1, 0.3)) for k in range(9)]
    art = shade(art, strokes(W, H, grooves) * wood, "#33200f", 0.55)
    art = GP(art, light_side(wood, 9, 0, 3) * np.clip(1.3 - (xx - 300) / 500, 0, 1), BARK_L, "#d69a5c", seed=nx(), rough=1.0, streak=0.7, pad=8)
    clear()
    # canopy (two big masses + one over the swing branch)
    art, cm1 = canopy(art, W, H, 600, 330, 260, 170, rng, 34, rmin=48, rmax=96, ndab=7)
    clear()
    art, cm2 = canopy(art, W, H, 300, 400, 170, 90, rng, 18, rmin=40, rmax=78, ndab=7)
    clear()
    # the swing branch must stay visible where the swing hangs: repaint its tip over the foliage
    tip = strokes(W, H, [(curve([(tx - 300, 472), (tx - 420, 476), (tx - 470, 468)], 20), 20, (0.0, 0.5))])
    art = paint(art, tip, BARK, BARK_D, px=1.4, dens=0.6, lc="#2e1d12")
    art = GP(art, light_side(tip, 0, 6, 2), BARK_L, seed=nx(), rough=0.8, pad=6)
    for (x, y, a) in [(tx - 440, 462, -2.0), (tx - 470, 470, 3.0), (tx - 380, 466, -1.4)]:
        art = paint(art, shapes(W, H, [petal_pts(x, y, 22, 9, a, n=10)]), G_M, G_D, px=0.8, dens=0.3, lc="#2b3a26")
    clear()
    # meadow foreground: grass strokes + wildflowers
    gs = []
    for _ in range(420):
        x = rng.uniform(-10, W + 10); y = rng.uniform(980, H)
        if y < top[int(min(len(top) - 1, max(0, (x + 20) / 20)))][1] + 20:
            continue
        L_ = 14 + (y - 980) / 420 * 40
        a = -math.pi / 2 + rng.uniform(-.35, .35)
        gs.append(([(x, y), (x + math.cos(a) * L_ * .5, y + math.sin(a) * L_ * .5), (x + math.cos(a + .2) * L_, y + math.sin(a + .2) * L_)], 2.0 + (y - 980) / 420 * 2, (0, .6)))
    gm = strokes(W, H, gs)
    art = G(art, gm, GRASS_D, "#516a35", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    art = G(art, gm * np.clip(1.1 - xx / W, 0, 1), "#e2c66c", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    fl = [(rng.uniform(0, W), rng.uniform(1000, H - 20), rng.uniform(5, 9)) for _ in range(70)]
    fl = [(x, y, r * (0.7 + (y - 1000) / 400 * 0.6)) for (x, y, r) in fl if y > top[int(min(len(top) - 1, max(0, (x + 20) / 20)))][1] + 30]
    art = flowers(art, W, H, fl, rng)
    clear()
    # fade the top into the CSS sky so the cover can grow on tall phones
    a = np.ones((H, W), np.float32)
    a[:140] = np.linspace(0, 1, 140)[:, None] ** 1.2
    art[..., 3] *= a
    art = add_grain(art, 6, 0.03)
    save_full(art, f"{OUT}/bukit.webp", quality=72)
    prev(art, "ap_bukit", bg="#f2c086")

if "ayunan" in PARTS:
    # rope swing: two ropes knotted to the branch, a weathered plank seat with a sun rim on the left
    W, H = 200, 340
    rng = random.Random(21)
    art = blank(W, H)
    ropes = [(curve([(52, 8), (50, 160), (46, 304)], 30), 4.2, None), (curve([(150, 8), (152, 160), (154, 304)], 30), 4.2, None)]
    rm = strokes(W, H, ropes)
    art = paint(art, rm, "#d6b98a", "#b39466", px=0.8, dens=0.55, lc="#5a4026")
    tw = strokes(W, H, [([(x - 3, y), (x + 3, y + 5)], 1.0, None) for x in (51, 152) for y in range(14, 300, 9)]) * rm
    art = shade(art, tw, "#7a5d3a", 0.5)
    for x in (52, 150):
        art = paint(art, circles(W, H, [(x, 12, 8)]), "#c9a878", px=0.8, dens=0.5, lc="#5a4026")
    seat = shapes(W, H, [[(20, 296), (182, 294), (186, 316), (18, 318)]], smooth=False)
    art = paint(art, seat, "#a06b41", "#7f5232", px=1.0, dens=0.6, lc="#3a2416")
    art = GP(art, strokes(W, H, [([(22, 297), (182, 295)], 3, None)]), "#e3b071", seed=rs(), rough=0.6, pad=6)
    art = shade(art, strokes(W, H, [([(30 + k * 30, 304), (52 + k * 30, 306)], 1.2, None) for k in range(5)]), "#5a3a24", 0.5)
    art = add_grain(art, 2, 0.03)
    save_full(art, f"{OUT}/ayunan.webp", quality=84)
    prev(art, "ap_ayunan", bg="#f6d49f")

if "ranting" in PARTS:
    # leafy twig with two tiny wildflowers: section divider
    W, H = 520, 110
    rng = random.Random(31)
    art = blank(W, H)
    stem = curve([(20, 70), (160, 52), (300, 60), (500, 44)], 60)
    art = paint(art, strokes(W, H, [(stem, 4, (0.05, 0.4))]), BARK, BARK_D, px=0.8, dens=0.5, lc="#2e1d12")
    leaves = []
    for k, (x, y, a) in enumerate(along(stem, 36)):
        side = 1 if k % 2 else -1
        L = rng.uniform(24, 34) * (1 - k / 22)
        leaves.append(petal_pts(x, y, L, L * .38, a + side * 0.9, n=10))
    lm = shapes(W, H, leaves)
    art = paint(art, lm, G_M, G_D, px=0.9, dens=0.4, lc="#2b3a26")
    art = GP(art, light_side(lm, 3, 4, 2), G_L, G_GOLD, seed=rs(), rough=0.8, pad=6)
    art = flowers(art, W, H, [(150, 40, 10), (330, 78, 9), (440, 30, 8)], rng, (CREAM, CORAL, LAV))
    save(art, f"{OUT}/ranting.webp", max_w=400, quality=84)
    prev(art, "ap_ranting")

if "bunga" in PARTS:
    # small wildflower posy (portrait ornament, closing emblem, timeline node)
    W, H = 220, 220
    rng = random.Random(41)
    art = blank(W, H)
    st = [(curve([(110, 210), (110 + rng.uniform(-30, 30), 140), (x, y)], 16), 2.4, None) for (x, y) in [(70, 70), (110, 50), (150, 76), (90, 104), (135, 110)]]
    art = paint(art, strokes(W, H, st), G_M, G_D, px=0.6, dens=0.4, lc="#2b3a26")
    lv = shapes(W, H, [petal_pts(110, 180, 44, 12, -2.2, n=10), petal_pts(112, 176, 44, 12, -0.9, n=10), petal_pts(110, 160, 36, 10, -1.6, n=10)])
    art = paint(art, lv, G_M, G_D, px=0.8, dens=0.4, lc="#2b3a26")
    art = flowers(art, W, H, [(70, 70, 22), (110, 50, 24), (150, 76, 22), (90, 104, 18), (135, 110, 18)], rng, (CREAM, CORAL, "#f3cf5a", LAV, CREAM))
    save(art, f"{OUT}/bunga.webp", max_w=130, quality=84)
    prev(art, "ap_bunga")

kb(OUT)
