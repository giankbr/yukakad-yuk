"""Ultah Kereta — original wooden toy train (no faces, no known characters): painted beech locomotive with a red cab,
blue boiler and green funnel, flatcars carrying blank wooden letter blocks (the child's name is typeset on top in
HTML), a cake car with balloons, a little wooden station with a clock, and a seamless track tile. Gouache on wood grain.
Run: python3 -I ultah-kereta.py [part ...]   parts: loco cars cake station track puff
Assets -> public/themes/art/ultah-kereta/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k2_lib import *

OUT = outdir("ultah-kereta")
PARTS = sys.argv[1:] or ["loco", "cars", "cake", "station", "track", "puff"]
RED, RED_D = "#e0483a", "#b02f25"
BLUE, BLUE_D = "#3a7fd0", "#275ea3"
YEL, YEL_D = "#f6c23e", "#d99a1c"
GRN, GRN_D = "#4fb06b", "#2f8a4c"
BEECH, BEECH_D, BEECH_L = "#e8c992", "#c99d5e", "#f4dfb6"
INK = "#3a2a22"


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a0 in [(x1 - r, y0 + r, -math.pi / 2), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, math.pi / 2), (x0 + r, y0 + r, math.pi)]:
        for i in range(n + 1):
            a = a0 + i / n * math.pi / 2
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def paint(art, W, H, m, col, col2, nx, wood_=True, bevel=True):
    """Toy paint on wood: opaque gouache, faint grain showing through, soft bevel light/shadow."""
    art = GP(art, m, col, col2, seed=nx(), rough=0.8, streak=0.9)
    if wood_:
        fig = gaussian_filter(np.random.default_rng(nx()).random(m.shape).astype(np.float32), (0.8, 24))
        fig = (fig - fig.mean()) / (fig.std() + 1e-6)
        art = OV(art, np.clip((fig - 1.0) * 0.5, 0, 1) * m * 0.22, lambda q: tint(q, "#3a2010", 1.0), pad=4)
    if bevel:
        hi = np.clip(m - np.roll(np.roll(gaussian_filter(m, 2.5), 4, 0), 3, 1), 0, 1)
        lo = np.clip(m - np.roll(np.roll(gaussian_filter(m, 2.5), -4, 0), -3, 1), 0, 1)
        art = OV(art, gaussian_filter(lo, 1.2) * 0.35, lambda q: tint(q, "#2a1408", 1.0), pad=6)
        art = OV(art, gaussian_filter(hi, 1.2) * 0.4, lambda q: tint(q, "#fff6e4", 1.0), pad=6)
    return art


def wheel(art, W, H, cx, cy, r, col, col2, nx):
    m = circles(W, H, [(cx, cy, r)])
    art = over(art, soft_shadow(m, "#3a2a22", blur=3, strength=0.35, dx=2, dy=3))
    art = paint(art, W, H, m, col, col2, nx, wood_=False)
    art = GP(art, ring(W, H, cx, cy, r * 0.62, r * 0.12), col2, seed=nx(), rough=0.4)
    hub = circles(W, H, [(cx, cy, r * 0.28)])
    art = paint(art, W, H, hub, BEECH, BEECH_D, nx, wood_=False)
    return art


def grainwood(art, W, H, m, nx, col=BEECH, col2=BEECH_D):
    art = WD(art, m, col, col2, seed=nx(), vertical=False, rough=0.6, grain=0.8)
    hi = np.clip(m - np.roll(np.roll(gaussian_filter(m, 2.5), 4, 0), 3, 1), 0, 1)
    lo = np.clip(m - np.roll(np.roll(gaussian_filter(m, 2.5), -4, 0), -3, 1), 0, 1)
    art = OV(art, gaussian_filter(lo, 1.2) * 0.35, lambda q: tint(q, "#5a3a1a", 1.0), pad=6)
    return OV(art, gaussian_filter(hi, 1.2) * 0.45, lambda q: tint(q, "#fff8e8", 1.0), pad=6)


if "loco" in PARTS:
    W, H = 500, 320
    nx = Seq(71100); rng = random.Random(71)
    art = blank(W, H)
    # chassis
    ch = shapes(W, H, [rrect(40, 200, 470, 238, 10)])
    art = over(art, soft_shadow(ch, "#3a2a22", blur=6, strength=0.3, dx=0, dy=8))
    art = grainwood(art, W, H, ch, nx)
    # cab (left), boiler (right), funnel, dome, lamp
    cab = shapes(W, H, [rrect(60, 70, 210, 206, 14)])
    art = paint(art, W, H, cab, RED, RED_D, nx)
    roof = shapes(W, H, [rrect(44, 52, 226, 80, 12)])
    art = paint(art, W, H, roof, YEL, YEL_D, nx)
    win = shapes(W, H, [rrect(92, 98, 178, 150, 18)])
    art = GP(art, win, "#bfe3f2", "#9fcde4", seed=nx(), rough=0.4)
    art = OV(art, gaussian_filter(polys(W, H, [[(100, 140), (130, 100), (146, 100), (114, 142)]]), 1) * win * 0.6, lambda q: tint(q, "#ffffff", 1.0))
    art = G(art, edge_of(win, 3), INK, seed=nx(), density=0.45, edge=0.2, rough=0.6)
    boil = shapes(W, H, [rrect(204, 112, 452, 204, 40)])
    art = paint(art, W, H, boil, BLUE, BLUE_D, nx)
    bands = shapes(W, H, [rrect(x, 110, x + 16, 206, 6) for x in (262, 342, 418)]) * gaussian_filter(boil, 1)
    art = paint(art, W, H, np.clip(bands * 1.3, 0, 1), YEL, YEL_D, nx, wood_=False)
    fun = shapes(W, H, [[(384, 112), (380, 70), (366, 46), (432, 46), (418, 70), (414, 112)]])
    art = paint(art, W, H, fun, GRN, GRN_D, nx)
    lip = shapes(W, H, [rrect(360, 36, 438, 54, 8)])
    art = paint(art, W, H, lip, RED, RED_D, nx)
    dome = shapes(W, H, [deform(ellipse_pts(300, 110, 26, 22, 14), rng, 1, 0.01)]) * (np.mgrid[0:H, 0:W][0] < 112)
    art = paint(art, W, H, dome, YEL, YEL_D, nx)
    front = shapes(W, H, [rrect(446, 124, 470, 196, 10)])
    art = paint(art, W, H, front, RED, RED_D, nx)
    lamp = circles(W, H, [(458, 104, 14)])
    art = over(art, glow(lamp, "#fff2b0", radius=8, strength=0.5))
    art = paint(art, W, H, lamp, "#fff1b8", YEL, nx, wood_=False)
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = 9 if k % 2 == 0 else 4
        star.append((458 + math.cos(a) * rr, 160 + math.sin(a) * rr))
    art = GP(art, polys(W, H, [star]), YEL, YEL_D, seed=nx(), rough=0.3)
    # cowcatcher pegs + buffers
    peg = shapes(W, H, [rrect(26, 206, 46, 230, 6), rrect(468, 206, 488, 230, 6)])
    art = grainwood(art, W, H, peg, nx)
    # wheels: one big drive wheel under the cab, three under the boiler
    for x, r, c in [(130, 46, GRN), (262, 30, YEL), (334, 30, YEL), (406, 30, YEL)]:
        art = wheel(art, W, H, x, 252, r, c, GRN_D if c == GRN else YEL_D, nx)
    rod = shapes(W, H, [rrect(130, 246, 410, 258, 6)])
    art = paint(art, W, H, rod, "#9aa4ad", "#6f7a84", nx, wood_=False)
    art = add_grain(art, 3, 0.025)
    show(art, "uk-loco")
    save_full(art, f"{OUT}/loco.webp", quality=84)
    clear()

CAR_W, CAR_H = 280, 260
if "cars" in PARTS:
    # flatcars carrying a blank beech block (letter typeset in HTML at 50% / 42%)
    for name, col, col2, wc, wc2, seed in [("carA", YEL, YEL_D, RED, RED_D, 71200), ("carB", GRN, GRN_D, BLUE, BLUE_D, 71300), ("carC", BLUE, BLUE_D, YEL, YEL_D, 71400), ("carD", RED, RED_D, GRN, GRN_D, 71500)]:
        W, H = CAR_W, CAR_H
        nx = Seq(seed); rng = random.Random(seed)
        art = blank(W, H)
        bed = shapes(W, H, [rrect(22, 168, 258, 206, 12)])
        art = over(art, soft_shadow(bed, "#3a2a22", blur=6, strength=0.3, dx=0, dy=8))
        art = paint(art, W, H, bed, col, col2, nx)
        # stake rail
        rail = shapes(W, H, [rrect(30, 160, 250, 172, 5)])
        art = grainwood(art, W, H, rail, nx)
        # the block, slightly rotated, with chamfered edges
        tilt = rng.uniform(-0.05, 0.05)
        blk = [(140 + (x - 140) * math.cos(tilt) - (y - 102) * math.sin(tilt), 102 + (x - 140) * math.sin(tilt) + (y - 102) * math.cos(tilt)) for x, y in rrect(72, 40, 208, 164, 16)]
        bm = shapes(W, H, [blk])
        art = over(art, soft_shadow(bm, "#3a2a22", blur=4, strength=0.3, dx=4, dy=4))
        art = grainwood(art, W, H, bm, nx)
        inner = shapes(W, H, [[(140 + (x - 140) * 0.86, 102 + (y - 102) * 0.86) for x, y in blk]])
        art = G(art, edge_of(inner, 2) * bm, "#b38550", seed=nx(), density=0.35, edge=0.2, rough=0.6)
        # couplers
        cp = shapes(W, H, [rrect(4, 178, 26, 196, 6), rrect(254, 178, 276, 196, 6)])
        art = grainwood(art, W, H, cp, nx)
        for x in (78, 202):
            art = wheel(art, W, H, x, 214, 28, wc, wc2, nx)
        art = add_grain(art, 5, 0.025)
        show(art, f"uk-{name}")
        save_full(art, f"{OUT}/{name}.webp", quality=84)
        clear()

if "cake" in PARTS:
    # caboose-style cake car: a two-tier cake with candles and a balloon bunch tied to it
    W, H = 300, 420
    nx = Seq(71600); rng = random.Random(72)
    art = blank(W, H)
    by = 330
    bed = shapes(W, H, [rrect(26, by, 274, by + 38, 12)])
    art = over(art, soft_shadow(bed, "#3a2a22", blur=6, strength=0.3, dx=0, dy=8))
    art = paint(art, W, H, bed, "#9b6fd0", "#7a52b0", nx)
    # balloons on strings from the back of the car
    for (bx, byy, r, c, c2) in [(70, 70, 34, RED, RED_D), (118, 44, 36, YEL, YEL_D), (46, 128, 30, BLUE, BLUE_D)]:
        art = G(art, strokes(W, H, [(curve([(bx, byy + r), (bx + 8, byy + r + 60), (64, by - 4)], 20), 1.6, None)]), "#7a6a5e", seed=nx(), density=0.7, edge=0, rough=0.3)
        bm = shapes(W, H, [deform(ellipse_pts(bx, byy, r * 0.88, r, 14), rng, 1, 0.01)])
        art = paint(art, W, H, bm, c, c2, nx, wood_=False)
        art = OV(art, gaussian_filter(circles(W, H, [(bx - r * 0.35, byy - r * 0.4, r * 0.2)]), 3) * 0.8, lambda q: tint(q, "#ffffff", 1.0))
        art = GP(art, polys(W, H, [[(bx - 5, byy + r - 2), (bx + 5, byy + r - 2), (bx, byy + r + 8)]]), c2, seed=nx(), rough=0.3)
    t1 = shapes(W, H, [rrect(80, 250, 250, by + 4, 12)])
    art = paint(art, W, H, t1, "#fbe3e8", "#f3c6d0", nx, wood_=False)
    t2 = shapes(W, H, [rrect(112, 194, 218, 254, 12)])
    art = paint(art, W, H, t2, "#fff4e0", "#f3dfbf", nx, wood_=False)
    drip = []
    for x0, x1, y0 in ((80, 250, 250), (112, 218, 194)):
        pts = [(x0, y0 + 4)]
        for k in range(9):
            x = x0 + (x1 - x0) * (k + 0.5) / 9
            pts += [(x - 6, y0 + 12), (x, y0 + 22 + rng.uniform(-3, 6)), (x + 6, y0 + 12)]
        pts += [(x1, y0 + 4), (x1, y0 - 2), (x0, y0 - 2)]
        drip.append(pts)
    art = GP(art, shapes(W, H, drip), "#e86a8a", "#d24f73", seed=nx(), rough=0.5)
    sprinkles = strokes(W, H, [([(x, y), (x + rng.uniform(-5, 5), y + rng.uniform(-3, 3))], 3, None) for x, y in [(rng.uniform(90, 240), rng.uniform(280, 328)) for _ in range(26)]])
    art = GP(art, sprinkles, YEL, BLUE, seed=nx(), rough=0.2)
    candles = shapes(W, H, [rrect(x - 4, 160, x + 4, 196, 3) for x in (138, 165, 192)])
    art = paint(art, W, H, candles, BLUE, BLUE_D, nx, wood_=False)
    fl = shapes(W, H, [[(x, 136), (x + 6, 150), (x, 160), (x - 6, 150)] for x in (138, 165, 192)])
    art = over(art, glow(fl, "#ffd36b", radius=8, strength=0.7))
    art = GP(art, fl, "#ffd25a", "#ff9a3a", seed=nx(), rough=0.3)
    for x in (82, 218):
        art = wheel(art, W, H, x, by + 46, 28, YEL, YEL_D, nx)
    art = add_grain(art, 7, 0.025)
    show(art, "uk-cake")
    save(art, f"{OUT}/cake.webp", max_w=240, quality=84)
    clear()

if "station" in PARTS:
    W, H = 460, 400
    nx = Seq(71700); rng = random.Random(73)
    art = blank(W, H)
    plat = shapes(W, H, [rrect(10, 330, 450, 368, 10)])
    art = over(art, soft_shadow(plat, "#3a2a22", blur=6, strength=0.25, dx=0, dy=8))
    art = grainwood(art, W, H, plat, nx, "#d9b27a", "#b98c52")
    body = shapes(W, H, [rrect(90, 170, 370, 334, 10)])
    art = paint(art, W, H, body, "#fff3dc", "#f3e2c2", nx)
    # vertical plank lines
    pl = strokes(W, H, [([(x, 176), (x, 330)], 1.6, None) for x in range(110, 370, 22)]) * body
    art = G(art, pl, "#d9c4a0", seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.5)
    art = paint(art, W, H, polys(W, H, [[(56, 190), (230, 62), (404, 190)]]), RED, RED_D, nx)
    scallop = np.clip(shapes(W, H, [[(70, 190), (390, 190), (390, 204), (70, 204)]]) - circles(W, H, [(x, 206, 8) for x in range(78, 390, 16)]), 0, 1)
    art = paint(art, W, H, scallop, YEL, YEL_D, nx, wood_=False)
    clock = circles(W, H, [(230, 140, 30)])
    art = paint(art, W, H, clock, "#fffaf0", "#efe6d4", nx, wood_=False)
    art = GP(art, ring(W, H, 230, 140, 30, 5), BLUE, BLUE_D, seed=nx(), rough=0.3)
    hands = strokes(W, H, [([(230, 140), (230, 120)], 3.2, None), ([(230, 140), (244, 146)], 3.2, None)])
    art = GP(art, hands, INK, seed=nx(), rough=0.2)
    ticks = strokes(W, H, [([(230 + math.cos(a) * 22, 140 + math.sin(a) * 22), (230 + math.cos(a) * 25, 140 + math.sin(a) * 25)], 2, None) for a in [k * math.pi / 6 for k in range(12)]])
    art = GP(art, ticks, INK, seed=nx(), rough=0.2)
    door = shapes(W, H, [rrect(196, 230, 264, 334, 30)])
    art = paint(art, W, H, door, GRN, GRN_D, nx)
    knob = circles(W, H, [(252, 286, 4)])
    art = GP(art, knob, YEL, seed=nx(), rough=0.2)
    for x in (118, 286):
        w_ = shapes(W, H, [rrect(x, 222, x + 56, 278, 10)])
        art = paint(art, W, H, w_, "#bfe3f2", "#9fcde4", nx, wood_=False)
        art = GP(art, strokes(W, H, [([(x + 28, 224), (x + 28, 276)], 3, None), ([(x + 2, 250), (x + 54, 250)], 3, None)]), "#fff3dc", seed=nx(), rough=0.2)
        box = shapes(W, H, [rrect(x - 4, 280, x + 60, 296, 6)])
        art = paint(art, W, H, box, BLUE, BLUE_D, nx)
        fl = circles(W, H, [(x + 6 + k * 10, 276 + rng.uniform(-3, 2), 5) for k in range(6)])
        art = GP(art, fl, RED, "#ff8fa3", seed=nx(), rough=0.3)
    # sign board + flag pole with bunting
    pole = shapes(W, H, [rrect(410, 120, 418, 332, 3)])
    art = grainwood(art, W, H, pole, nx)
    flag = shapes(W, H, [[(418, 122), (452, 134), (418, 148)]])
    art = paint(art, W, H, flag, YEL, YEL_D, nx, wood_=False)
    bunt = []
    for k in range(8):
        x0 = 96 + k * 34
        bunt.append([(x0, 214), (x0 + 30, 214), (x0 + 15, 232)])
    cols = [RED, YEL, BLUE, GRN]
    for k, b in enumerate(bunt):
        art = GP(art, polys(W, H, [b]), cols[k % 4], seed=nx(), rough=0.4)
    art = G(art, strokes(W, H, [([(92, 213), (372, 213)], 1.4, None)]), INK, seed=nx(), density=0.6, rough=0.3)
    # bench
    bench = shapes(W, H, [rrect(20, 300, 82, 310, 4), rrect(26, 310, 32, 330, 2), rrect(70, 310, 76, 330, 2), rrect(20, 284, 82, 292, 4)])
    art = grainwood(art, W, H, bench, nx, "#c98a52", "#a86c3a")
    art = add_grain(art, 9, 0.025)
    show(art, "uk-station")
    save(art, f"{OUT}/station.webp", max_w=320, quality=84)
    clear()

if "track" in PARTS:
    # seamless horizontal tile: beech sleepers + two painted rails
    W, H = 240, 64
    nx = Seq(71800); rng = random.Random(74)
    art = blank(W, H)
    sl = []
    for k in range(6):
        x = 6 + k * 40 + rng.uniform(-1, 1)
        sl.append(rrect(x, 10, x + 26, 60, 5))
    art = grainwood(art, W, H, shapes(W, H, sl), nx, "#c98a52", "#a86c3a")
    rails = polys(W, H, [rect(0, 18, W, 26), rect(0, 42, W, 50)])
    art = GP(art, rails, "#7d8a96", "#5d6874", seed=nx(), rough=0.2, streak=0.4)
    hi = polys(W, H, [rect(0, 18, W, 20), rect(0, 42, W, 44)])
    art = OV(art, hi * 0.6, lambda q: tint(q, "#e8eef3", 1.0))
    art = add_grain(art, 11, 0.02)
    save_full(art, f"{OUT}/track.webp", quality=82)
    show(art, "uk-track")
    clear()

if "puff" in PARTS:
    W, H = 220, 160
    nx = Seq(71900); rng = random.Random(75)
    art = blank(W, H)
    m = circles(W, H, [(60, 100, 40), (110, 70, 48), (160, 96, 40), (110, 110, 40)])
    art = paint(art, W, H, m, "#ffffff", "#eef2f6", nx, wood_=False)
    art = G(art, m * np.clip((np.mgrid[0:H, 0:W][0] - 80) / 60, 0, 1), "#c9d6e2", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=2)
    show(art, "uk-puff", bg="#8fd0f0")
    save(art, f"{OUT}/puff.webp", max_w=160, quality=84)
    clear()
