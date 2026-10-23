"""Muaro Jambi — dawn over the red-brick temple ruins of Muaro Jambi on the Batanghari: a terraced brick candi with a
central stair and moss, ruined perimeter walls and a gateway gap, jungle (palms, a big shade tree), the wide brown river
with a wooden perahu (separate, bobbing), a Jambi batik tile (duren pecah pods + kapal sanggat boats), a brick divider,
a brick arch frame for portraits and a jungle-leaf spray. Gouache with watercolour glazes; no statues.
Run: python3 -I muaro-jambi.py [part ...]   parts: sky scene boat batik divider arch leaves"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o5_lib import *

OUT = outdir("muaro-jambi")
PARTS = sys.argv[1:] or ["sky", "scene", "boat", "batik", "divider", "arch", "leaves"]
BRICK, BRICK_L, BRICK_D, BRICK_DD = "#b4532f", "#d67a4c", "#86361f", "#5e2414"
MORTAR = "#e7bf98"
MOSS, MOSS_D = "#7b8f4a", "#566b34"
JUNG, JUNG_D, JUNG_L, JUNG_M = "#2f5a43", "#1d3b2e", "#5d8a55", "#3f6e4c"
RIVER, RIVER_L, RIVER_D = "#a07a5c", "#e2b48e", "#6e5442"
SKY_T, SKY_M, SKY_H = "#f7ead4", "#f4d6ae", "#efb889"
INDIGO, OCHRE, CREAM = "#23305a", "#d9a441", "#f6ead6"


def brickify(art, mask, base, light, dark, seed, bw=26, bh=11, lit=None):
    """Paint a brick mass: gouache base, course lines, per-brick tone, crumbly edge."""
    Wd, Hd = mask.shape[1], mask.shape[0]
    art = P(art, mask, base, light, seed=seed, rough=2.2)
    b, tone = brick_field(Wd, Hd, bw, bh, seed=seed + 1)
    mort = np.clip(1 - b, 0, 1) * mask
    art = tint(art, mort, dark, 0.42)
    art = tint(art, b * mask * np.clip((tone - 0.62) * 3, 0, 1), light, 0.45)
    art = tint(art, b * mask * np.clip((0.3 - tone) * 3, 0, 1), dark, 0.35)
    if lit is not None:
        art = tint(art, mask * lit, "#f6c08e", 0.22)
    return art


def sky():
    Wd, Hd = 300, 520
    art = painted_sky(Wd, Hd, [(0, SKY_T), (0.55, SKY_M), (0.9, SKY_H), (1.0, "#e9a77a")], seed=5, streak=1.0)
    # low sun glow, soft cloud bands
    sun = circles(Wd, Hd, [(222, 400, 26)])
    art = OV(art, sun, lambda m: glow(m, "#fff2d6", 40, 0.55), pad=150)
    art = P(art, sun, "#fff4dc", "#ffe6b8", seed=3, rough=0.8)
    cl = shapes(Wd, Hd, [ellipse_pts(80, 300, 90, 7, 12), ellipse_pts(240, 250, 70, 5, 12), ellipse_pts(150, 352, 110, 6, 12)])
    art = W(art, cl, "#f0c6a2", "#f7d9bd", seed=9, density=0.5, edge=0.2, rough=4)
    art = add_grain(art, 3, 0.03)
    save_rgb(art, f"{OUT}/sky.webp", quality=72)


def palm(art, Wd, Hd, x, by, h, lean, rng, col, seed):
    tx, ty = x + lean * h, by - h
    trunk = curve([(x, by), (x + lean * h * 0.4, by - h * 0.5), (tx, ty)], 30)
    art = P(art, strokes(Wd, Hd, [(trunk, 8, (0.0, 0.3))]), "#5a4634", seed=seed, rough=1)
    art = tint(art, strokes(Wd, Hd, [([(px - 4, py), (px + 4, py + 2)], 1.4, None) for px, py, _ in along(trunk, 9)]), "#3a2c20", 0.6)
    fr, lf = [], []
    for k in range(10):
        a = -math.pi / 2 + (k - 4.5) * 0.4 + rng.uniform(-0.1, 0.1)
        L = h * rng.uniform(0.3, 0.42)
        pts = curve([(tx, ty), (tx + math.cos(a) * L * 0.55, ty + math.sin(a) * L * 0.55 - 8), (tx + math.cos(a) * L, ty + math.sin(a) * L + L * 0.38)], 20)
        fr.append((pts, 3, (0.05, 0.6)))
        for i, (px, py, ang) in enumerate(along(pts, 7)[1:]):
            ll = 20 * (1 - i / 14) + 6
            for sgn in (-1, 1):
                lf.append(([(px, py), (px + math.cos(ang + sgn * 1.15) * ll, py + math.sin(ang + sgn * 1.15) * ll + ll * 0.35)], 3.2, (0.0, 0.7)))
    art = P(art, strokes(Wd, Hd, lf), col, mix(col, JUNG_L, 0.25), seed=seed + 1, rough=0.8)
    art = P(art, strokes(Wd, Hd, fr), JUNG_D, seed=seed + 2, rough=0.5)
    return art


def tree_crown(Wd, Hd, cx, cy, r, rng, n=14):
    blobs = [deform(ellipse_pts(cx + rng.uniform(-r, r), cy + rng.uniform(-r * 0.55, r * 0.4), r * rng.uniform(0.35, 0.6), r * rng.uniform(0.28, 0.45), 12), rng, 2, 0.12) for _ in range(n)]
    return shapes(Wd, Hd, blobs)


def candi(art, Wd, Hd, cx, by, nx, rng):
    """Terraced brick temple (Muaro Jambi type): wide moulded platform, receding terraces with pilaster panels and
    projecting cornices, narrow central stair with side walls, a collapsed bell-shaped crown. No statues."""
    tiers = [(540, 44), (452, 92), (356, 80), (262, 70)]
    y = by
    allm = np.zeros((Hd, Wd), np.float32)
    lit = right_of(Wd, cx - 60, 280)
    for k, (w, h) in enumerate(tiers):
        x0, x1 = cx - w / 2, cx + w / 2
        y0 = y - h
        poly = [(x0, y), (x0, y0 + 4), (x0 + 6, y0 + rng.uniform(-2, 2)), (cx - w * 0.15, y0 + rng.uniform(-3, 2)), (cx + w * 0.3, y0 + rng.uniform(-2, 3)), (x1 - 5, y0 + rng.uniform(-1, 3)), (x1, y0 + 6), (x1, y)]
        m = shapes(Wd, Hd, [poly], smooth=False)
        allm = np.maximum(allm, m)
        art = brickify(art, m, BRICK, BRICK_L, BRICK_D, nx(), bw=22, bh=9, lit=lit)
        if k > 0:
            # pilaster panels: recessed fields between raised strips (shadow on the left of each strip)
            n = 4 + (2 if k == 1 else 0)
            for i in range(n + 1):
                px = x0 + 14 + i * (w - 28) / n
                strip = rect(Wd, Hd, px - 7, y0 + 18, px + 7, y - 10)
                art = tint(art, strip, BRICK_L, 0.32)
                art = tint(art, rect(Wd, Hd, px - 10, y0 + 18, px - 7, y - 10), BRICK_DD, 0.45)
            # recessed panel shading
            art = W(art, m * below(Hd, y0 + 18, 4) * above(Hd, y - 10, 4), BRICK_D, seed=nx(), density=0.22, edge=0.1, rough=2)
        # projecting cornice (top) and plinth (bottom) mouldings
        cor = rect(Wd, Hd, x0 - 9, y0 - 2, x1 + 9, y0 + 12)
        art = brickify(art, cor, BRICK_L, "#e48f5e", BRICK, nx(), bw=16, bh=6, lit=lit)
        art = tint(art, rect(Wd, Hd, x0 - 9, y0 + 9, x1 + 9, y0 + 13), BRICK_DD, 0.55)
        art = W(art, m * below(Hd, y0 + 12, 1) * above(Hd, y0 + 30, 12), BRICK_DD, seed=nx(), density=0.4, edge=0.1, rough=2)
        pl = rect(Wd, Hd, x0 - 5, y - 12, x1 + 5, y)
        art = brickify(art, pl, BRICK, BRICK_L, BRICK_D, nx(), bw=16, bh=6, lit=lit)
        art = tint(art, rect(Wd, Hd, x0 - 5, y - 13, x1 + 5, y - 11), BRICK_L, 0.6)
        allm = np.maximum(allm, np.maximum(cor, pl))
        # moss on the cornice
        moss = cor * np.clip((fbm(Wd, Hd, nx(), 16, 3) - 0.5) * 4, 0, 1)
        art = W(art, moss, MOSS, MOSS_D, seed=nx(), density=0.85, edge=0.4, rough=1.5)
        y = y0 - 2
    top_y = y
    # collapsed bell crown: squat genta body with a broken, ragged top + loose bricks
    bell = [(cx - 92, top_y + 4), (cx - 86, top_y - 22), (cx - 70, top_y - 48), (cx - 50, top_y - 62), (cx - 34, top_y - 58), (cx - 22, top_y - 70),
            (cx - 4, top_y - 66), (cx + 10, top_y - 78), (cx + 30, top_y - 64), (cx + 44, top_y - 66), (cx + 66, top_y - 50), (cx + 86, top_y - 24), (cx + 92, top_y + 4)]
    bm = shapes(Wd, Hd, [bell], smooth=False)
    art = brickify(art, bm, BRICK, BRICK_L, BRICK_D, nx(), bw=18, bh=8, lit=right_of(Wd, cx - 30, 120))
    art = W(art, bm * (1 - right_of(Wd, cx - 40, 90)), BRICK_DD, seed=nx(), density=0.35, edge=0.1, rough=2)
    art = W(art, bm * above(Hd, top_y - 50, 8) * np.clip((fbm(Wd, Hd, nx(), 14, 3) - 0.4) * 4, 0, 1), MOSS, MOSS_D, seed=nx(), density=0.85, rough=1.5)
    allm = np.maximum(allm, bm)
    # a young tree growing out of the ruin (very Muaro Jambi)
    art = P(art, strokes(Wd, Hd, [(curve([(cx + 40, top_y - 60), (cx + 52, top_y - 100), (cx + 70, top_y - 126)], 12), 4, (0.0, 0.3))]), "#4f3a2c", seed=nx(), rough=0.5)
    sap = tree_crown(Wd, Hd, cx + 74, top_y - 140, 34, rng, 7)
    art = P(art, sap, JUNG_M, JUNG_L, seed=nx(), rough=1.5)
    loose = [rot([(x - 7, yy - 3), (x + 7, yy - 3), (x + 7, yy + 3), (x - 7, yy + 3)], x, yy, rng.uniform(-0.5, 0.5)) for x, yy in [(cx + rng.uniform(-260, 260), by + rng.uniform(-4, 14)) for _ in range(9)]]
    art = P(art, shapes(Wd, Hd, loose, smooth=False), BRICK, BRICK_D, seed=nx(), rough=0.6)
    # stair: narrow, with side walls ending in scroll-like curls
    sw0, sw1 = 62, 40
    stair = shapes(Wd, Hd, [[(cx - sw0 / 2, by + 2), (cx - sw1 / 2, top_y + 4), (cx + sw1 / 2, top_y + 4), (cx + sw0 / 2, by + 2)]], smooth=False)
    art = P(art, stair, "#c96b42", "#d98a5c", seed=nx(), rough=1.0)
    steps = []
    yy = by
    while yy > top_y + 8:
        t = (by - yy) / (by - top_y)
        hw = (sw0 * (1 - t) + sw1 * t) / 2
        steps.append(([(cx - hw, yy), (cx + hw, yy)], 2.0, None))
        yy -= 8
    art = tint(art, strokes(Wd, Hd, steps) * stair, BRICK_DD, 0.5)
    art = tint(art, stair * (1 - right_of(Wd, cx - 6, 18)), BRICK_DD, 0.18)
    for sgn in (-1, 1):
        wall = shapes(Wd, Hd, [[(cx + sgn * sw0 / 2, by + 2), (cx + sgn * sw1 / 2, top_y + 6), (cx + sgn * (sw1 / 2 + 10), top_y + 6), (cx + sgn * (sw0 / 2 + 14), by + 2)]], smooth=False)
        curl = circles(Wd, Hd, [(cx + sgn * (sw0 / 2 + 10), by - 8, 12)])
        wm = np.maximum(wall, curl)
        art = brickify(art, wm, BRICK_D, BRICK, BRICK_DD, nx(), bw=12, bh=7)
        art = tint(art, strokes(Wd, Hd, [(arc_pts(cx + sgn * (sw0 / 2 + 10), by - 8, 6, 0, math.tau * 0.8, 14), 2, None)]), BRICK_L, 0.8)
        allm = np.maximum(allm, wm)
    # weathering: dark streaks running down, sun-warmed right side, shadow on the left
    streak = strokes(Wd, Hd, [([(x, y0), (x + rng.uniform(-2, 2), y0 + rng.uniform(20, 60))], rng.uniform(2, 5), (0.0, 0.8)) for x, y0 in [(rng.uniform(cx - 270, cx + 270), rng.uniform(top_y, by - 30)) for _ in range(60)]]) * allm
    art = tint(art, streak, "#4a2a20", 0.28, blur=1)
    art = W(art, allm * (1 - right_of(Wd, cx - 150, 200)), "#5e2f2a", seed=nx(), density=0.3, edge=0.08, bloom=0.3, rough=3)
    art = W(art, allm * right_of(Wd, cx + 60, 200), "#f2a66e", seed=nx(), density=0.22, edge=0.05, bloom=0.3, rough=3)
    art = tint(art, edge_ring(allm, 1.6), BRICK_DD, 0.55)
    return art


def scene():
    Wd, Hd = 800, 1040
    nx = Seq(100); rng = random.Random(7)
    art = blank(Wd, Hd)
    # far jungle: misty blue-green band
    far = shapes(Wd, Hd, [[(-20, 520)] + [(x, 470 + 22 * math.sin(x / 47) + rng.uniform(-14, 10)) for x in range(0, 820, 40)] + [(820, 640), (-20, 640)]])
    art = W(art, far, "#8fa48c", "#a9b69a", seed=nx(), density=0.8, edge=0.3, rough=6)
    # big shade tree behind the candi (left) and palms
    trunk = strokes(Wd, Hd, [(curve([(170, 700), (182, 560), (160, 450)], 20), 22, (0.0, 0.2)), (curve([(178, 560), (240, 470), (300, 430)], 16), 11, (0.0, 0.4))])
    art = P(art, trunk, "#4f3a2c", "#6a4e3a", seed=nx(), rough=1.4)
    crown = tree_crown(Wd, Hd, 190, 400, 150, rng, 16)
    art = P(art, crown, JUNG, JUNG_M, seed=nx(), rough=2.5)
    art = W(art, crown * right_of(Wd, 150, 90) * above(Hd, 400, 80), JUNG_L, seed=nx(), density=0.55, edge=0.3, rough=4)
    art = W(art, crown * below(Hd, 420, 60), JUNG_D, seed=nx(), density=0.5, edge=0.2, rough=4)
    for cm_, cx_, cy_, r_ in ((crown, 190, 400, 150),):
        art = tint(art, shapes(Wd, Hd, [ellipse_pts(cx_ + rng.uniform(-r_, r_), cy_ + rng.uniform(-r_ * 0.6, r_ * 0.3), rng.uniform(8, 16), rng.uniform(5, 9), 8) for _ in range(90)]) * cm_, JUNG_L, 0.5)
        art = tint(art, shapes(Wd, Hd, [ellipse_pts(cx_ + rng.uniform(-r_, r_), cy_ + rng.uniform(-r_ * 0.3, r_ * 0.5), rng.uniform(8, 16), rng.uniform(5, 9), 8) for _ in range(70)]) * cm_, JUNG_D, 0.45)
    crown2 = tree_crown(Wd, Hd, 690, 470, 110, rng, 12)
    art = P(art, crown2, JUNG_M, JUNG, seed=nx(), rough=2.5)
    art = W(art, crown2 * right_of(Wd, 660, 60), JUNG_L, seed=nx(), density=0.5, edge=0.3, rough=4)
    for x, h, lean in ((560, 330, 0.08), (620, 280, -0.05), (90, 300, -0.1), (760, 340, 0.03)):
        art = palm(art, Wd, Hd, x, 690, h, lean, rng, JUNG_D if x in (90, 760) else JUNG, nx())
    clear()
    # mid jungle undergrowth line behind the temple
    und = shapes(Wd, Hd, [[(-20, 700)] + [(x, 610 + rng.uniform(-30, 16)) for x in range(0, 820, 26)] + [(820, 810), (-20, 810)]])
    art = P(art, und, JUNG_M, JUNG, seed=nx(), rough=3)
    art = W(art, und * above(Hd, 640, 30), JUNG_L, seed=nx(), density=0.45, edge=0.3, rough=4)
    dabs = [petal_pts(rng.uniform(0, Wd), rng.uniform(600, 760), rng.uniform(14, 26), rng.uniform(6, 10), rng.uniform(-2.6, -0.6), n=8) for _ in range(120)]
    dm = shapes(Wd, Hd, dabs) * und
    art = tint(art, dm, JUNG_L, 0.55)
    art = tint(art, shapes(Wd, Hd, [petal_pts(rng.uniform(0, Wd), rng.uniform(620, 770), rng.uniform(12, 22), 7, rng.uniform(-2.6, -0.6), n=8) for _ in range(80)]) * und, JUNG_D, 0.5)
    # the candi
    art = candi(art, Wd, Hd, 410, 800, nx, rng)
    clear()
    # ground / grass terrace
    ground = shapes(Wd, Hd, [[(-20, 790), (200, 784), (420, 796), (640, 786), (820, 792), (820, 880), (-20, 880)]])
    art = P(art, ground, "#7e9a52", "#6b8746", seed=nx(), rough=2)
    art = W(art, ground * below(Hd, 820, 40), "#556f38", seed=nx(), density=0.5, edge=0.2, rough=3)
    # ruined perimeter walls with the gateway gap (foreground)
    for (x0, x1, h, sd) in ((-10, 300, 46, 1), (520, 810, 52, 2)):
        top = [(x, 842 - h + rng.uniform(-6, 5) - (14 if (x - x0) % 120 < 30 else 0)) for x in range(int(x0), int(x1) + 1, 14)]
        wm = shapes(Wd, Hd, [[(x0, 846)] + top + [(x1, 846)]], smooth=False)
        art = brickify(art, wm, BRICK, BRICK_L, BRICK_D, nx(), bw=24, bh=10, lit=right_of(Wd, 300, 300))
        art = W(art, wm * above(Hd, 842 - h + 14, 8) * np.clip((fbm(Wd, Hd, nx(), 18, 3) - 0.45) * 4, 0, 1), MOSS, MOSS_D, seed=nx(), density=0.8, rough=2)
        art = tint(art, edge_ring(wm, 1.5), BRICK_DD, 0.55)
    # gate posts
    for gx in (300, 520):
        pm = rect(Wd, Hd, gx - 18 if gx == 300 else gx, 760, gx if gx == 300 else gx + 18, 848)
        art = brickify(art, pm, BRICK_D, BRICK, BRICK_DD, nx(), bw=18, bh=10)
    # grass tufts
    blades = [([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(10, 22))], 2.6, (0.0, 0.7)) for x, y in [(rng.uniform(0, Wd), rng.uniform(842, 880)) for _ in range(150)]]
    art = tint(art, strokes(Wd, Hd, blades), "#5d7a3a", 0.85)
    clear()
    # riverbank + Batanghari
    bank = shapes(Wd, Hd, [[(-20, 870), (300, 862), (560, 874), (820, 864), (820, 900), (-20, 900)]])
    art = P(art, bank, "#8a6a4e", "#a07c5c", seed=nx(), rough=2)
    river = rect(Wd, Hd, -10, 892, 810, 1040)
    art = P(art, river, RIVER, "#b08a68", seed=nx(), rough=1, streak=1.6)
    art = W(art, river * below(Hd, 960, 80), RIVER_D, seed=nx(), density=0.4, edge=0.1, rough=3)
    # sun reflection streaks (right) and ripples
    rip = []
    for _ in range(110):
        y = rng.uniform(900, 1035); x = rng.gauss(560, 120)
        L = rng.uniform(14, 60) * (1.2 - (y - 900) / 200)
        rip.append((curve([(x - L, y), (x, y + rng.uniform(-1, 1)), (x + L, y)], 8), rng.uniform(2.2, 4.0), (0.3, 0.3)))
    art = tint(art, strokes(Wd, Hd, rip), RIVER_L, 0.95)
    rip2 = [(curve([(x - 30, y), (x, y + 1), (x + 30, y)], 8), 2.2, (0.3, 0.3)) for x, y in [(rng.uniform(0, Wd), rng.uniform(905, 1035)) for _ in range(40)]]
    art = tint(art, strokes(Wd, Hd, rip2), RIVER_D, 0.55)
    # temple reflection hint
    refl = strokes(Wd, Hd, [(curve([(x, 898), (x + rng.uniform(-3, 3), 898 + L * 0.5), (x + rng.uniform(-4, 4), 898 + L)], 6), rng.uniform(5, 9), (0.0, 0.6)) for x, L in [(rng.uniform(150, 670), rng.uniform(20, 70)) for _ in range(46)]])
    art = W(art, refl, BRICK, "#9a4a30", seed=nx(), density=0.5, edge=0.1, rough=1.5)
    # foreground reeds (left)
    reeds = [(curve([(x, 1040), (x + rng.uniform(-8, 8), 990), (x + rng.uniform(-24, 24), 930 + rng.uniform(-20, 20))], 16), 5, (0.0, 0.8)) for x in np.linspace(-10, 130, 14)]
    art = P(art, strokes(Wd, Hd, reeds), JUNG_D, JUNG, seed=nx(), rough=1)
    art = add_grain(art, 13, 0.035)
    save(art, f"{OUT}/scene.webp", max_w=780, quality=74)
    preview(art, "mj-scene", bg=SKY_M)


def boat():
    Wd, Hd = 360, 180
    nx = Seq(400)
    art = blank(Wd, Hd)
    hull = shapes(Wd, Hd, [[(20, 100), (60, 118), (300, 118), (340, 96), (300, 132), (60, 134)]])
    art = P(art, hull, "#5a3a26", "#74503a", seed=nx(), rough=1)
    art = tint(art, rect(Wd, Hd, 50, 112, 310, 118) * hull, OCHRE, 0.85)
    art = tint(art, edge_ring(hull, 1.4), "#2e1c12", 0.6)
    # little roof (kajang) cabin
    roof = shapes(Wd, Hd, [[(130, 112), (140, 78), (240, 74), (252, 112)]])
    art = P(art, roof, "#c9a46a", "#b48c54", seed=nx(), rough=1)
    art = tint(art, strokes(Wd, Hd, [([(144 + k * 13, 80), (138 + k * 14, 110)], 1.4, None) for k in range(8)]) * roof, "#8a6a3c", 0.6)
    # boatman's pole + paddle lines
    art = P(art, strokes(Wd, Hd, [([(286, 116), (330, 20)], 4, (0.0, 0.2))]), "#3f2a1c", seed=nx(), rough=0.6)
    # wake
    art = tint(art, strokes(Wd, Hd, [([(30, 142), (110, 146)], 2.2, (0.3, 0.3)), ([(230, 146), (330, 140)], 2.2, (0.3, 0.3)), ([(80, 154), (260, 154)], 1.6, (0.3, 0.3))]), RIVER_L, 0.9)
    save(art, f"{OUT}/boat.webp", max_w=240, quality=82)
    preview(art, "mj-boat", bg=RIVER)


def batik():
    T = 300
    nx = Seq(500); rng = random.Random(9)
    n = wrap_noise(T, T, 3, 18)
    rgb = np.ones((T, T, 3), np.float32) * col3(INDIGO) * (0.92 + 0.16 * n[..., None])
    art = np.concatenate([rgb, np.ones((T, T, 1), np.float32)], -1)
    # isen-isen dots (cecek) on the ground
    dots = circles(T, T, [(x + rng.uniform(-1, 1), y + rng.uniform(-1, 1), 1.2) for x in range(5, T, 10) for y in range(5, T, 10)])
    art = tint(art, dots, "#43568a", 0.7)
    def duren(cx, cy, r, rot0):
        husk = np.zeros((T, T), np.float32); flesh = np.zeros((T, T), np.float32); spikes = []
        for k in range(4):
            a = rot0 + k * math.pi / 2
            ox, oy = cx + math.cos(a) * 13, cy + math.sin(a) * 13
            pp = petal_pts(ox, oy, r * 0.9, r * 0.46, a, n=16, cup=0.15)
            husk = np.maximum(husk, shapes(T, T, [pp]))
            flesh = np.maximum(flesh, shapes(T, T, [ellipse_pts(ox + math.cos(a) * r * 0.5, oy + math.sin(a) * r * 0.5, r * 0.2, r * 0.13, 12, a)]))
            for t in np.linspace(-1.1, 1.1, 7):
                sx, sy = ox + math.cos(a + t * 0.38) * r * (0.5 + 0.3 * math.cos(t)), oy + math.sin(a + t * 0.38) * r * (0.5 + 0.3 * math.cos(t))
                spikes.append((sx, sy, 2.2))
        return husk, flesh, circles(T, T, spikes)
    for cx, cy, r, rr in ((T * .25, T * .25, 58, math.pi / 4), (T * .75, T * .75, 58, math.pi / 4)):
        husk, flesh, sp = duren(cx, cy, r, rr)
        art = P(art, husk, BRICK, "#c4643a", seed=nx(), rough=0.7)
        art = tint(art, edge_ring(husk, 1.6), "#f3dcb0", 0.9)
        art = tint(art, sp, "#f3dcb0", 0.9)
        art = P(art, flesh, OCHRE, "#ecc463", seed=nx(), rough=0.5)
        art = tint(art, circles(T, T, [(cx, cy, 6)]), "#f3dcb0", 0.95)
    # kapal sanggat: small stranded boats with a sail, on the other diagonal
    for bx, by_ in ((T * .75, T * .27), (T * .25, T * .77)):
        hull = shapes(T, T, [[(bx - 38, by_), (bx - 26, by_ + 13), (bx + 26, by_ + 13), (bx + 38, by_), (bx, by_ + 5)]], smooth=False)
        sail = shapes(T, T, [[(bx - 3, by_ - 2), (bx - 3, by_ - 40), (bx + 24, by_ - 6)], [(bx - 7, by_ - 4), (bx - 7, by_ - 30), (bx - 26, by_ - 6)]], smooth=False)
        art = P(art, hull, "#f0dcb4", "#e6cfa0", seed=nx(), rough=0.6)
        art = P(art, sail, OCHRE, "#e8bd5c", seed=nx(), rough=0.6)
        art = tint(art, strokes(T, T, [(curve([(bx - 44, by_ + 20), (bx, by_ + 23), (bx + 44, by_ + 20)], 10), 2, (0.2, 0.2))]), "#8a9ac4", 0.8)
    # wax crackle
    cr = (np.abs(wrap_noise(T, T, 11, 6) - 0.5) < 0.01).astype(np.float32)
    art = tint(art, cr, "#151d3a", 0.3)
    save_rgb(art, f"{OUT}/batik.webp", quality=78)


def divider():
    Wd, Hd = 440, 90
    nx = Seq(600)
    art = blank(Wd, Hd)
    cx = Wd / 2
    # brick lintel courses tapering to both sides
    for sgn in (-1, 1):
        for k in range(7):
            x = cx + sgn * (44 + k * 24)
            wdt = 22 - k * 1.6
            y = 54 + (k % 2) * 0
            m = rr_mask(Wd, Hd, x - wdt / 2, y - 7 + (k % 2) * 4, x + wdt / 2, y + 4 + (k % 2) * 4, 2)
            art = P(art, m, BRICK if k % 2 else BRICK_L, BRICK_D, seed=nx(), rough=0.8)
    # tiny terraced candi centre
    t = shapes(Wd, Hd, [[(cx - 34, 66), (cx - 34, 56), (cx - 26, 56), (cx - 26, 46), (cx - 16, 46), (cx - 16, 34), (cx - 6, 34), (cx - 6, 22), (cx, 14), (cx + 6, 22), (cx + 6, 34), (cx + 16, 34), (cx + 16, 46), (cx + 26, 46), (cx + 26, 56), (cx + 34, 56), (cx + 34, 66)]], smooth=False)
    art = brickify(art, t, BRICK, BRICK_L, BRICK_D, nx(), bw=10, bh=6)
    art = P(art, rect(Wd, Hd, cx - 4, 50, cx + 4, 66), "#3a1a10", seed=nx(), rough=0.4)
    art = tint(art, edge_ring(t, 1.2), BRICK_DD, 0.6)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
    preview(art, "mj-divider")


def arch():
    """Brick arch window frame (transparent opening) placed over the portrait."""
    Wd, Hd = 520, 660
    nx = Seq(700)
    cx = Wd / 2
    outer = shapes(Wd, Hd, [[(30, Hd - 10)] + arc_pts(cx, 250, 230, math.pi, 2 * math.pi, 40) + [(Wd - 30, Hd - 10)]], smooth=False)
    inner = shapes(Wd, Hd, [[(70, Hd - 46)] + arc_pts(cx, 258, 190, math.pi, 2 * math.pi, 40) + [(Wd - 70, Hd - 46)]], smooth=False)
    ring = np.clip(outer - inner, 0, 1)
    art = blank(Wd, Hd)
    art = brickify(art, ring, BRICK, BRICK_L, BRICK_D, nx(), bw=24, bh=12, lit=right_of(Wd, cx, 200))
    # voussoir lines radiating in the arch
    vs = [([(cx + math.cos(a) * 192, 258 + math.sin(a) * 192), (cx + math.cos(a) * 230, 250 + math.sin(a) * 230)], 2.2, None) for a in np.linspace(math.pi, 2 * math.pi, 23)]
    art = tint(art, strokes(Wd, Hd, vs) * ring * above(Hd, 262, 1), BRICK_DD, 0.6)
    # crumbled chunk at top-right + moss
    art = W(art, ring * np.clip((fbm(Wd, Hd, nx(), 26, 3) - 0.55) * 4, 0, 1), MOSS, MOSS_D, seed=nx(), density=0.8, rough=2)
    art = tint(art, edge_ring(ring, 1.6), BRICK_DD, 0.6)
    # base step
    base = rect(Wd, Hd, 14, Hd - 34, Wd - 14, Hd - 4)
    art = brickify(art, base, BRICK_D, BRICK, BRICK_DD, nx(), bw=26, bh=10)
    save_full(art, f"{OUT}/arch.webp", size=(390, 495), quality=80)
    preview(art, "mj-arch")


def gleaf(art, Wd, Hd, x, y, L, ang, col, col2, seed, wid=0.36):
    m = shapes(Wd, Hd, [petal_pts(x, y, L, L * wid, ang, n=12)])
    art = P(art, m, col, col2, seed=seed, rough=1.2)
    half = shapes(Wd, Hd, [petal_pts(x, y, L * 0.96, L * wid * 0.45, ang + 0.08, n=12)]) * m
    art = W(art, half, JUNG_D, seed=seed + 1, density=0.4, edge=0.2, rough=2)
    vein = curve([(x, y), (x + math.cos(ang) * L * 0.5, y + math.sin(ang) * L * 0.5), (x + math.cos(ang) * L * 0.92, y + math.sin(ang) * L * 0.92)], 12)
    art = tint(art, strokes(Wd, Hd, [(vein, 2.4, (0.0, 0.6))]), "#c9d79a", 0.55)
    return art


def leaves():
    Wd, Hd = 520, 440
    nx = Seq(800); rng = random.Random(4)
    art = blank(Wd, Hd)
    # banana blades (gouache) rising from the corner
    for pts, wd, c in ((curve([(30, 440), (120, 300), (300, 150), (470, 110)], 30), 46, (JUNG, JUNG_M)), (curve([(10, 430), (40, 260), (120, 60)], 26), 38, (JUNG_M, JUNG_L))):
        poly = blade(Wd, Hd, pts, wd)
        m = shapes(Wd, Hd, [poly])
        cuts = []
        for j in range(4, len(pts) - 3, 4):
            a, b = pts[j - 1], pts[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                if rng.random() < 0.5:
                    aa = ang + side * 1.1
                    cuts.append(([(pts[j][0] + math.cos(aa) * wd * .4, pts[j][1] + math.sin(aa) * wd * .4), (pts[j][0] + math.cos(aa) * wd * 1.3, pts[j][1] + math.sin(aa) * wd * 1.3)], 2.6, None))
        m = np.clip(m - strokes(Wd, Hd, cuts), 0, 1)
        art = P(art, m, c[0], c[1], seed=nx(), rough=1.2)
        art = W(art, m * shapes(Wd, Hd, [blade(Wd, Hd, pts, wd)[:len(pts)] + pts[::-1]]), JUNG_D, seed=nx(), density=0.4, edge=0.2, rough=2)
        art = tint(art, strokes(Wd, Hd, [(pts[2:-3], 3, (0.05, 0.4))]), "#c9d79a", 0.5)
        ribs = []
        for j in range(3, len(pts) - 3, 2):
            a, b = pts[j - 1], pts[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                aa = ang + side * 1.0
                ribs.append((curve([pts[j], (pts[j][0] + math.cos(aa) * wd * .5, pts[j][1] + math.sin(aa) * wd * .5), (pts[j][0] + math.cos(aa) * wd * .85, pts[j][1] + math.sin(aa) * wd * .85)], 5), 1.4, (0.1, 0.6)))
        art = tint(art, strokes(Wd, Hd, ribs) * m, JUNG_D, 0.35)
    # broad leaves
    for x, y, L, a, c in ((60, 420, 190, -0.55, (JUNG_M, JUNG)), (40, 430, 150, -1.25, (JUNG_L, JUNG_M)), (90, 425, 170, -0.15, (JUNG, JUNG_D)), (20, 400, 120, -1.7, (JUNG_M, JUNG_L))):
        art = gleaf(art, Wd, Hd, x, y, L, a, c[0], c[1], nx())
    clear()
    # jungle flower clusters (red-orange, Jambi batik red)
    for fx, fy in ((210, 300), (150, 360), (260, 250)):
        fl = circles(Wd, Hd, [(fx + rng.uniform(-15, 15), fy + rng.uniform(-12, 12), rng.uniform(4, 6.5)) for _ in range(12)])
        art = P(art, fl, "#d4503a", "#e8784a", seed=nx(), rough=0.6)
        art = tint(art, circles(Wd, Hd, [(fx + rng.uniform(-12, 12), fy + rng.uniform(-10, 10), 2.2) for _ in range(6)]), OCHRE, 0.9)
    save(art, f"{OUT}/leaves.webp", max_w=360, quality=80)
    preview(art, "mj-leaves")


for p in PARTS:
    globals()[p]()
    clear()
