"""Sepeda Tandem — storybook gouache: a tandem bicycle (two simple riders, flower basket) on a country road through
patchwork fields, bunting, balloons tied to the saddle. Run: python3 -I sepeda-tandem.py [part ...]
parts: scene bike balloons bunting flowers wheel   Assets -> public/themes/art/sepeda-tandem/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o6_lib import *

OUT = outdir("sepeda-tandem")
PARTS = sys.argv[1:] or ["scene", "bike", "balloons", "bunting", "flowers", "wheel"]
LINE = "#4a3a32"          # warm brown pencil line
RED, RED_D = "#d4573b", "#a63c28"
MUST, MUST_D = "#e8b64a", "#c48f2a"
SKY, SKY_D = "#8fc3d3", "#5f9db3"
PINK = "#ec9aa0"
NAVY, NAVY_D = "#2f4a6b", "#1f3350"
CREAM = "#fbf3e2"
G1, G2, G3, G4 = "#b7cf78", "#8db35e", "#5f8c48", "#3f6a3a"


def line(art, mask, px=1.4, dens=0.7, col=LINE):
    """Coloured-pencil outline around a painted shape."""
    rim = np.clip((mask - gaussian_filter(mask, px)) * 3.2, 0, 1)
    return G(art, rim, col, seed=random.randint(1, 10**6), density=dens, edge=0, bloom=0, rough=0.8, feather=0.35, pad=6)


def paint(art, mask, col, col2=None, ln=True, streak=0.7, px=1.4, dens=0.7):
    art = GP(art, mask, col, col2 or mix(col, "#000000", .12), seed=random.randint(1, 10**6), rough=1.6, streak=streak, pad=10)
    return line(art, mask, px, dens) if ln else art


def shade(art, mask, col, d=0.35):
    return G(art, mask, col, seed=random.randint(1, 10**6), density=d, edge=0.25, bloom=0.3, rough=3, pad=10)


random.seed(7)

if "scene" in PARTS:
    # landscape from the horizon down (transparent sky): far hills, village roofs, patchwork fields, the winding road,
    # two bunting poles and the strung flags across the road.
    W, H = 780, 820
    rng = random.Random(3); nx = Seq(300)
    art = blank(W, H)
    far = hills(W, H, 120, 34, 4, 0.9)
    art = paint(art, far, "#a9c7c4", "#93b5b6", ln=False)
    mid = hills(W, H, 190, 40, 9, 0.6)
    art = paint(art, mid, "#9fbf73", "#86ad62", ln=False)
    # distant village: little red roofs and white walls on the mid hill
    houses = []
    for k, x in enumerate([120, 150, 186, 560, 596, 640]):
        y = 196 - 8 * math.sin(x / 70) - (k % 2) * 5
        wall = shapes(W, H, [[(x - 13, y), (x + 13, y), (x + 13, y + 16), (x - 13, y + 16)]], smooth=False)
        roof = shapes(W, H, [[(x - 17, y + 2), (x, y - 14), (x + 17, y + 2)]], smooth=False)
        art = paint(art, wall, CREAM, ln=True, px=1.0, dens=0.5)
        art = paint(art, roof, RED, RED_D, px=1.0, dens=0.5)
    # trees on the hills
    for (x, y, r) in [(90, 210, 22), (230, 200, 18), (520, 214, 20), (700, 206, 24), (338, 190, 14)]:
        trunk = strokes(W, H, [([(x, y + r * .6), (x, y + r * 1.6)], 4, None)])
        art = paint(art, trunk, "#7a5638", ln=False)
        crown = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 1.05, 12), rng, 2, .08)])
        art = paint(art, crown, G3, G4, px=1.2, dens=0.5)
        art = shade(art, crown * np.clip(np.roll(gaussian_filter(crown, 5), -6, 1) - 0.2, 0, 1), G4, .35)
    # patchwork fields: three bands with row stripes (sunflower mustard, young rice, lavender)
    bands = [(250, 60, 7, G1, G2, "rows"), (330, 80, 12, MUST, MUST_D, "dots"), (430, 110, 15, "#c3b0dc", "#9f88c2", "rows"), (560, 140, 6, G2, G3, "rows")]
    for (y0, amp, sd, c1, c2, kind) in bands:
        band = hills(W, H, y0, amp * 0.25, sd, 0.8)
        art = paint(art, band, c1, c2, ln=True, px=1.6, dens=0.35)
        # crop rows converge towards the road (perspective-ish diagonal strokes)
        it = []
        for i in range(-6, 22):
            x0 = i * 44
            it.append(([(x0, y0 + 10), (x0 + (x0 - 390) * 0.35, H)], 3.0, None))
        rows = strokes(W, H, it) * band
        art = shade(art, rows, c2, 0.45)
        if kind == "dots":  # sunflower heads
            dots_ = [(rng.uniform(0, W), rng.uniform(y0 + 6, y0 + 70), rng.uniform(3, 5.5)) for _ in range(160)]
            dm = circles(W, H, dots_) * band
            art = GP(art, dm, "#f4c94d", "#e0a630", seed=nx(), rough=0.8, pad=6)
            art = G(art, circles(W, H, [(x, y, r * 0.35) for x, y, r in dots_]) * band, "#6b4a2a", seed=nx(), density=0.8, edge=0.2, rough=0.5, pad=6)
    clear()
    # the road: winds from bottom-left up to the horizon gap
    centre = curve([(250, H + 20), (330, 650), (470, 520), (420, 390), (360, 300), (392, 232)], 120)
    L, R = [], []
    for i, (x, y) in enumerate(centre):
        t = (y - 220) / (H - 200)
        wd = 6 + 190 * max(0, t) ** 1.25
        a, b = centre[max(0, i - 1)], centre[min(len(centre) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        L.append((x - dy / d * wd, y + dx / d * wd)); R.append((x + dy / d * wd, y - dx / d * wd))
    road = shapes(W, H, [L + R[::-1]])
    art = paint(art, road, "#f1dfb6", "#e6cc98", px=1.6, dens=0.5)
    art = shade(art, strokes(W, H, [(centre[10:], 5, (0.1, 0.4))]) * road, "#d9bb83", 0.35)  # wheel ruts
    # grass verge tufts and wild flowers along the road edges
    tufts = []
    for (x, y) in L[20::6] + R[20::6]:
        for k in range(3):
            a = -math.pi / 2 + rng.uniform(-.6, .6)
            tufts.append(([(x, y), (x + math.cos(a) * 14, y + math.sin(a) * 14)], 2.2, (0, .6)))
    art = shade(art, strokes(W, H, tufts), G4, 0.65)
    fl = [(x + rng.uniform(-14, 14), y + rng.uniform(-8, 6), rng.uniform(3, 5)) for (x, y) in (L[30::4] + R[30::4])]
    for k, col in enumerate([CREAM, PINK, "#f4c94d"]):
        art = GP(art, circles(W, H, fl[k::3]), col, seed=nx(), rough=0.6, pad=6)
    # bunting poles + garland across the road
    for (x, y0, y1) in [(150, 300, 470), (640, 300, 470)]:
        pole = strokes(W, H, [([(x, y0), (x + 2, y1)], 6, None)])
        art = paint(art, pole, "#8a6240", "#6b4a2c", px=1.0)
    flags = []; cols = [RED, MUST, SKY, PINK, CREAM, "#9fbf73"]
    garl = [(150 + (640 - 150) * t, 304 + 60 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 60)]
    art = line(art, strokes(W, H, [(garl, 2.0, None)]), 1.2, 0.0)
    art = G(art, strokes(W, H, [(garl, 2.0, None)]), LINE, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.5, pad=6)
    for k, (x, y, a) in enumerate(along(garl, 30)):
        tri = [(x - 11, y), (x + 11, y + 0.5), (x + 1, y + 24)]
        m = shapes(W, H, [tri], smooth=False)
        art = paint(art, m, cols[k % len(cols)], px=1.0, dens=0.5)
    # foreground: tall grass tufts and a few wild flowers in both bottom corners
    fg = []
    for (x0, x1) in [(0, 170), (560, 780)]:
        for _ in range(60):
            x = rng.uniform(x0, x1); y = H - rng.uniform(0, 70)
            a = -math.pi / 2 + rng.uniform(-.5, .5); L_ = rng.uniform(26, 60)
            fg.append((curve([(x, y + 10), (x + math.cos(a) * L_ * .5, y + math.sin(a) * L_ * .5), (x + math.cos(a + .25) * L_, y + math.sin(a + .25) * L_)], 10), 3.4, (0, .6)))
    art = paint(art, strokes(W, H, fg), G3, G4, px=1.0, dens=0.35)
    for k, (x, y) in enumerate([(40, 760), (110, 790), (620, 770), (700, 745), (740, 800), (80, 720)]):
        col = [RED, CREAM, MUST, CREAM, PINK, MUST][k]
        r = rng.uniform(8, 12)
        pet = circles(W, H, [(x + math.cos(j * 1.256) * r * .55, y + math.sin(j * 1.256) * r * .55, r * .5) for j in range(5)])
        art = paint(art, pet, col, px=1.0, dens=0.45)
        art = GP(art, circles(W, H, [(x, y, r * .28)]), "#6b4a2a", seed=nx(), rough=0.5, pad=6)
    art = add_grain(art, 5, 0.03)
    art[:, -8:] = art[:, -9:-8]; art[:, :8] = art[:, 8:9]; art[-8:] = art[-9:-8]
    save(art, f"{OUT}/scene.webp", max_w=780, quality=78)
    prev(art, "st_scene", bg="#d7eaee")

if "bike" in PARTS:
    W, H = 640, 440
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    Rh, Fh, rad = (150, 340), (488, 340), 70
    BB1, BB2 = (240, 336), (372, 336)
    S1, S2 = (210, 228), (342, 228)
    H1, H2 = (452, 214), (462, 262)
    # shadow on the road
    art = G(art, shapes(W, H, [ellipse_pts(320, 414, 270, 14, 20)]), "#5b4a3a", seed=nx(), density=0.28, edge=0, bloom=0, rough=3, feather=3)
    # wheels: tyre, rim, spokes, hub
    for (cx, cy) in (Rh, Fh):
        tyre = np.clip(circles(W, H, [(cx, cy, rad)]) - circles(W, H, [(cx, cy, rad - 9)]), 0, 1)
        art = paint(art, tyre, "#3b3431", "#2a2422", px=1.0, dens=0.6)
        rim = np.clip(circles(W, H, [(cx, cy, rad - 9)]) - circles(W, H, [(cx, cy, rad - 13)]), 0, 1)
        art = GP(art, rim, "#d9d2c4", "#b9b0a0", seed=nx(), rough=0.6, pad=6)
        sp = strokes(W, H, [([(cx, cy), (cx + math.cos(a) * (rad - 11), cy + math.sin(a) * (rad - 11))], 1.4, None) for a in np.linspace(0, math.tau, 17)[:-1]])
        art = G(art, sp, "#8d857a", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.4, pad=6)
        art = paint(art, circles(W, H, [(cx, cy, 8)]), "#cfc6b6", px=1.0)
    # chain + cranks
    art = G(art, strokes(W, H, [([BB1, BB2], 3, None), ([Rh, BB1], 3, None)]), "#5f5650", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.5, pad=6)
    for bb in (BB1, BB2):
        art = paint(art, circles(W, H, [(bb[0], bb[1], 13)]), "#8a8278", px=1.0)
    # frame tubes (red gouache with a pencil line)
    tubes = [(Rh, BB1), (Rh, S1), (S1, BB1), (BB1, BB2), (S1, S2), (S2, BB2), (S2, H1), (BB2, H2), (H1, H2), (H2, Fh)]
    frame = strokes(W, H, [([a, b], 10, None) for a, b in tubes])
    art = paint(art, frame, RED, RED_D, px=1.2, dens=0.8)
    art = G(art, strokes(W, H, [([(a[0], a[1] - 2.5), (b[0], b[1] - 2.5)], 3, None) for a, b in tubes]) * frame, "#f19a7e", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, pad=6)
    # front rack + wicker basket full of flowers
    rack = strokes(W, H, [([(H1[0] + 4, H1[1] + 8), (H1[0] + 54, H1[1] + 8)], 4, None), ([(H1[0] + 50, H1[1] + 8), (Fh[0] + 10, Fh[1] - 40)], 3, None)])
    art = paint(art, rack, "#6b625a", px=1.0)
    bx0, by0 = H1[0] - 4, H1[1] - 50
    basket = shapes(W, H, [[(bx0, by0), (bx0 + 76, by0), (bx0 + 68, by0 + 56), (bx0 + 8, by0 + 56)]], smooth=False)
    # flowers spilling over the basket rim (painted first so the basket front overlaps their stems)
    blooms = [(bx0 + 10, by0 - 4, 13, PINK), (bx0 + 32, by0 - 14, 15, CREAM), (bx0 + 56, by0 - 6, 13, MUST), (bx0 + 74, by0 - 16, 11, PINK), (bx0 + 22, by0 - 26, 10, "#f4c94d"), (bx0 + 48, by0 - 28, 11, RED)]
    leaves = [(bx0 + x, by0 + y, 26, a) for x, y, a in [(0, 2, -2.6), (70, -2, -0.5), (40, -22, -1.4), (86, -6, -0.2)]]
    for (x, y, L, a) in leaves:
        m = shape_mask(W, H, petal_pts(x, y, L, L * 0.35, a, n=12))
        art = paint(art, m, G2, G3, px=1.0, dens=0.5)
    for (x, y, r, col) in blooms:
        pet = circles(W, H, [(x + math.cos(k * 1.256) * r * .55, y + math.sin(k * 1.256) * r * .55, r * .52) for k in range(5)])
        art = paint(art, pet, col, px=1.0, dens=0.45)
        art = GP(art, circles(W, H, [(x, y, r * .3)]), "#7a5a2e" if col != MUST else "#8a4e22", seed=nx(), rough=0.5, pad=6)
    art = paint(art, basket, "#c99a5e", "#a87842", px=1.2)
    weave = strokes(W, H, [([(bx0 + 4, by0 + 12 + 11 * k), (bx0 + 72, by0 + 12 + 11 * k)], 2, None) for k in range(4)] +
                    [([(bx0 + 10 + 13 * k, by0), (bx0 + 14 + 11 * k, by0 + 56)], 1.6, None) for k in range(6)]) * basket
    art = shade(art, weave, "#7a5530", 0.55)
    # saddles + handlebars
    for (x, y) in (S1, S2):
        art = paint(art, shapes(W, H, [deform(ellipse_pts(x - 4, y - 6, 22, 7, 12, -0.08), rng, 1, .04)]), "#5a3a2a", "#3e271c", px=1.0)
    bars = strokes(W, H, [(curve([H1, (H1[0] - 6, H1[1] - 22), (H1[0] - 30, H1[1] - 26)], 12), 6, None), (curve([S2, (S2[0] - 4, S2[1] - 26), (S2[0] - 26, S2[1] - 26)], 12), 5, None)])
    art = paint(art, bars, "#4a423c", px=1.0)
    clear()
    # riders: stylised, no faces (seen from slightly behind: hair covers the head)
    # bride (stoker): long cream dress flowing back, veil streaming in the wind
    veil = shapes(W, H, [curve([(222, 106), (160, 112), (90, 150), (40, 168), (70, 140), (120, 110), (190, 92), (226, 96)], 40)])
    art = G(art, veil, "#ffffff", "#e8edf0", seed=nx(), density=0.62, edge=0.5, bloom=0.3, rough=3, pad=10)
    art = line(art, veil, 1.2, 0.35)
    skirt = shapes(W, H, [[(196, 214), (228, 214), (262, 300), (250, 330), (210, 324), (166, 300), (150, 262)]])
    torso = shapes(W, H, [[(202, 216), (230, 214), (246, 150), (222, 128), (200, 136), (196, 176)]])
    art = paint(art, skirt, "#fbf6ea", "#ece2cc", px=1.4)
    art = shade(art, skirt * np.clip(gaussian_filter(skirt, 6) * 0 + np.linspace(0, 1, W)[None, :] * 0 + 1, 0, 1) * shapes(W, H, [[(150, 262), (196, 214), (214, 260), (190, 320), (166, 300)]]), "#cfc3aa", 0.4)
    art = paint(art, torso, "#fbf6ea", "#ece2cc", px=1.4)
    arm_b = strokes(W, H, [(curve([(236, 150), (262, 180), (300, 196), (318, 202)], 16), 10, (0.05, 0.1))])
    art = paint(art, arm_b, "#f6ecdc", px=1.0)
    art = paint(art, circles(W, H, [(320, 202, 6)]), "#d9a483", px=0.8, dens=0.4)
    head_b = circles(W, H, [(228, 108, 20)])
    art = paint(art, head_b, "#4a3024", "#33201a", px=1.0)       # dark hair (back of the head)
    art = paint(art, circles(W, H, [(210, 104, 10)]), "#3e281e", px=1.0)  # bun
    art = paint(art, circles(W, H, [(232, 134, 5)]), "#d9a483", ln=False)
    crown = circles(W, H, [(214 + k * 6, 92 - math.sin(k) * 3, 4) for k in range(4)])
    art = GP(art, crown, CREAM, seed=nx(), rough=0.5, pad=6)
    art = paint(art, shapes(W, H, [ellipse_pts(256, 330, 12, 5, 10)]), "#e7d9c2", px=0.8)  # shoe on the pedal
    # groom (captain): white shirt, navy waistcoat & trousers, leaning to the bars
    leg = strokes(W, H, [(curve([(340, 226), (392, 258), (378, 300), (382, 334)], 20), 17, (0.0, 0.05))])
    leg2 = strokes(W, H, [(curve([(338, 228), (370, 270), (358, 320), (364, 344)], 20), 15, (0.0, 0.05))])
    art = paint(art, leg2, NAVY_D, px=1.0)
    art = paint(art, leg, NAVY, NAVY_D, px=1.2)
    art = paint(art, shapes(W, H, [ellipse_pts(390, 338, 14, 6, 10)]), "#3a2a22", px=0.8)
    shirt = shapes(W, H, [[(330, 226), (352, 228), (386, 156), (370, 130), (346, 128), (330, 170)]])
    art = paint(art, shirt, "#dcebf2", "#bcd3df", px=1.4)
    braces = strokes(W, H, [([(340, 224), (360, 134)], 3.2, None), ([(350, 226), (372, 138)], 3.2, None)])
    art = paint(art, braces * shirt, NAVY_D, ln=False)
    art = paint(art, strokes(W, H, [([(330, 222), (354, 224)], 8, None)]), NAVY, NAVY_D, px=1.0)  # waistband
    arm_g = strokes(W, H, [(curve([(372, 142), (400, 168), (424, 186), (430, 190)], 16), 11, (0.05, 0.1))])
    art = paint(art, arm_g, "#dcebf2", "#bcd3df", px=1.0)
    art = paint(art, circles(W, H, [(430, 190, 6)]), "#c89272", px=0.8, dens=0.4)
    art = paint(art, circles(W, H, [(372, 108, 19)]), "#2b1d16", "#1d130e", px=1.0)
    art = paint(art, circles(W, H, [(380, 128, 5)]), "#c89272", ln=False)
    art = add_grain(art, 7, 0.03)
    save(art, f"{OUT}/bike.webp", max_w=560, quality=82)
    prev(art, "st_bike", bg="#f1dfb6")

if "balloons" in PARTS:
    W, H = 300, 460
    rng = random.Random(15); nx = Seq(1500)
    art = blank(W, H)
    knot = (150, 450)
    specs = [(96, 110, 46, RED), (188, 80, 50, MUST), (140, 190, 42, SKY), (230, 190, 38, PINK)]
    art = G(art, strokes(W, H, [(curve([(x, y + r * 1.18), ((x + knot[0]) / 2 + rng.uniform(-14, 14), (y + knot[1]) / 2), knot], 30), 1.4, None) for x, y, r, _ in specs]),
            LINE, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.5, pad=6)
    for (x, y, r, col) in specs:
        m = shapes(W, H, [deform(ellipse_pts(x, y, r * 0.88, r * 1.08, 16), rng, 1, .02)])
        art = paint(art, m, col, mix(col, "#000000", .15), px=1.3, dens=0.6)
        sh = m * np.clip(np.roll(np.roll(gaussian_filter(m, 8), 10, 0), 8, 1) * 0 + 1, 0, 1) * shapes(W, H, [ellipse_pts(x + r * .3, y + r * .35, r * .7, r * .8, 14)])
        art = shade(art, sh, mix(col, "#3a2a30", .4), 0.35)
        art = GP(art, shapes(W, H, [ellipse_pts(x - r * .38, y - r * .45, r * .16, r * .26, 10, 0.5)]), "#fffaf0", seed=nx(), rough=0.6, density=0.8, pad=6)
        art = paint(art, shapes(W, H, [[(x - 6, y + r * 1.08 + 7), (x + 6, y + r * 1.08 + 7), (x, y + r * 1.04)]], smooth=False), mix(col, "#000000", .15), px=0.8)
    save(art, f"{OUT}/balloons.webp", max_w=220, quality=84)
    prev(art, "st_balloons", bg="#d7eaee")

if "bunting" in PARTS:
    W, H = 560, 100
    rng = random.Random(19); nx = Seq(1900)
    art = blank(W, H)
    garl = [(20 + 520 * t, 20 + 34 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 60)]
    art = G(art, strokes(W, H, [(garl, 2.0, None)]), LINE, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.5, pad=6)
    cols = [RED, MUST, SKY, PINK, "#9fbf73", CREAM]
    for k, (x, y, a) in enumerate(along(garl, 40)):
        c, s_ = math.cos(a), math.sin(a)
        tri = [(x - 14 * c, y - 14 * s_), (x + 14 * c, y + 14 * s_), (x - 28 * s_ * -1 * 0 + 0, y + 30)]
        tri[2] = (x - s_ * 30 * -1 * 0 + 1, y + 30)
        art = paint(art, shapes(W, H, [tri], smooth=False), cols[k % len(cols)], px=1.0, dens=0.55)
    save(art, f"{OUT}/bunting.webp", max_w=380, quality=84)
    prev(art, "st_bunting")

if "flowers" in PARTS:
    # a little wildflower posy: daisies, a poppy, mustard buttons, grass blades
    W, H = 260, 220
    rng = random.Random(23); nx = Seq(2300)
    art = blank(W, H)
    blades = [(curve([(130, 210), (130 + math.cos(a) * 60, 210 + math.sin(a) * 60), (130 + math.cos(a) * 120, 210 + math.sin(a) * 130)], 20), 4, (0, .5)) for a in np.linspace(-2.6, -0.5, 9)]
    art = paint(art, strokes(W, H, blades), G2, G3, px=1.0, dens=0.4)
    for (x, y, r, col, eye) in [(84, 92, 22, CREAM, MUST), (150, 66, 26, RED, "#3a2a22"), (196, 110, 19, CREAM, MUST), (118, 130, 14, MUST, "#8a4e22"), (170, 150, 12, PINK, MUST)]:
        n = 8 if col == CREAM else 5
        pet = shapes(W, H, [petal_pts(x, y, r, r * (0.3 if n == 8 else 0.6), k / n * math.tau + rng.uniform(-.1, .1), n=10) for k in range(n)])
        art = paint(art, pet, col, px=1.1, dens=0.5)
        art = GP(art, circles(W, H, [(x, y, r * .28)]), eye, seed=nx(), rough=0.5, pad=6)
    save(art, f"{OUT}/flowers.webp", max_w=180, quality=84)
    prev(art, "st_flowers")

if "wheel" in PARTS:
    # bicycle wheel ring for the round portraits: tyre, rim, a few visible spokes peeking out, valve
    W, H = 440, 440
    rng = random.Random(29); nx = Seq(2900)
    cx, cy, R = 220, 220, 206
    art = blank(W, H)
    tyre = np.clip(circles(W, H, [(cx, cy, R)]) - circles(W, H, [(cx, cy, R - 18)]), 0, 1)
    art = paint(art, tyre, "#3b3431", "#2a2422", px=1.2, dens=0.6)
    tread = strokes(W, H, [([(cx + math.cos(a) * (R - 3), cy + math.sin(a) * (R - 3)), (cx + math.cos(a) * (R - 12), cy + math.sin(a) * (R - 12))], 2.2, None) for a in np.linspace(0, math.tau, 73)[:-1]])
    art = G(art, tread * tyre, "#6d625a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, pad=6)
    rim = np.clip(circles(W, H, [(cx, cy, R - 18)]) - circles(W, H, [(cx, cy, R - 26)]), 0, 1)
    art = GP(art, rim, "#e4ddd0", "#bdb3a3", seed=nx(), rough=0.6, pad=6)
    art = line(art, rim, 1.0, 0.4)
    art = paint(art, shapes(W, H, [[(cx - 5, cy - R + 18), (cx + 5, cy - R + 18), (cx + 4, cy - R + 36), (cx - 4, cy - R + 36)]], smooth=False), "#8d857a", px=0.8)
    save(art, f"{OUT}/wheel.webp", max_w=340, quality=84)
    prev(art, "st_wheel")

kb(OUT)
