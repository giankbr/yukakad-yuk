"""Ultah Pemadam — kids' firefighter birthday in storybook gouache: a friendly red fire truck with a ladder and hose
reel, a brick fire station with an open arched door, bunting and balloons, a red helmet with a gold star badge, a
hose spraying a water arc. No scary fire. Run: python3 -I ultah-pemadam.py [part ...]
parts: station truck helmet water divider   Assets -> public/themes/art/ultah-pemadam/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
import _o1_lib
from _o1_lib import *

OUT = outdir("ultah-pemadam")
PARTS = sys.argv[1:] or ["station", "truck", "helmet", "water", "divider"]
NAVY = "#1f2a44"
_o1_lib.LINE = NAVY
RED, RED_D, RED_L = "#e0352b", "#b0241d", "#f05a48"
YEL, YEL_D = "#ffc93c", "#e8a51e"
SKY, SKY_D = "#a6dcf3", "#7cc6e8"
WATER, WATER_D = "#5bbbea", "#2f93cf"
BRICK, BRICK_D = "#c95a42", "#a8442f"
CREAM = "#fff7ea"
GREY, GREY_D = "#c9ced8", "#9aa2b2"


def PP(art, W, H, m, c1, c2, nx, **k):
    return paint_part(art, W, H, m, c1, c2, nx, line_col=NAVY, **k)


def wheel(art, W, H, x, y, r, nx):
    art = PP(art, W, H, circles(W, H, [(x, y, r)]), "#2c3550", "#1f2740", nx, hi=0.15)
    art = PP(art, W, H, circles(W, H, [(x, y, r * 0.55)]), GREY, GREY_D, nx, hi=0.35)
    art = PP(art, W, H, circles(W, H, [(x, y, r * 0.2)]), RED, RED_D, nx, hi=0.3)
    bolts = circles(W, H, [(x + math.cos(a) * r * 0.38, y + math.sin(a) * r * 0.38, r * 0.05) for a in np.linspace(0, math.tau, 6, endpoint=False)])
    return G(art, bolts, NAVY, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)


def truck():
    W, H = 820, 460
    nx = Seq(100)
    art = blank(W, H)
    gy = 410  # ground line under wheels
    # ladder (behind body): rails + rungs, resting on a turntable at the rear
    rail = [rrect(90, 132, 640, 146, 6), rrect(90, 158, 640, 172, 6)]
    art = PP(art, W, H, shapes(W, H, rail), GREY, GREY_D, nx, shade_dir=(0, 1), hi=0.4)
    rungs = shapes(W, H, [rect(x, 144, x + 8, 160) for x in range(110, 630, 34)], smooth=False)
    art = PP(art, W, H, rungs, "#e3e7ee", GREY_D, nx, hi=0.3, line=False)
    art = PP(art, W, H, shapes(W, H, [rrect(96, 168, 170, 206, 12)]), "#3a4566", "#2c3550", nx, hi=0.2)
    # rear body
    body = shapes(W, H, [rrect(50, 196, 560, 372, 18)])
    art = PP(art, W, H, body, RED, RED_D, nx, shade_dir=(0, 1), shade=0.3, hi=0.25)
    # roller-door compartments
    for (x0, x1) in [(74, 196), (210, 332), (346, 452)]:
        comp = shapes(W, H, [rrect(x0, 214, x1, 300, 8)])
        art = PP(art, W, H, comp, RED_L, RED, nx, shade_dir=(0, 1), hi=0.2)
        lines = strokes(W, H, [([(x0 + 6, y), (x1 - 6, y)], 1.6, None) for y in range(226, 296, 10)]) * comp
        art = G(art, lines, RED_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
        handle = shapes(W, H, [rrect((x0 + x1) / 2 - 12, 288, (x0 + x1) / 2 + 12, 294, 3)])
        art = PP(art, W, H, handle, GREY, GREY_D, nx, hi=0.4, line=False)
    # hose reel with coiled white hose
    art = PP(art, W, H, circles(W, H, [(506, 256, 42)]), GREY, GREY_D, nx, hi=0.35)
    coil = strokes(W, H, [(arc_pts(506, 256, r, 0, math.tau, 40), 5, None) for r in (14, 22, 30, 37)])
    art = G(art, coil, "#f4f1ea", seed=nx(), density=0.95, edge=0.1, bloom=0, rough=0.4)
    art = G(art, edge_ring(coil, 1.0), GREY_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    # cab
    cab = [(560, 372), (560, 150), (640, 136), (700, 150), (744, 214), (760, 272), (760, 372)]
    cm = shapes(W, H, [deform(cab, random.Random(2), 1, 0.005)])
    art = PP(art, W, H, cm, RED, RED_D, nx, shade_dir=(0, 1), shade=0.3, hi=0.3)
    win = shapes(W, H, [[(588, 170), (640, 160), (690, 170), (722, 220), (588, 220)]])
    art = PP(art, W, H, win, "#cdeefc", "#a5dcf3", nx, hi=0.5)
    shine = strokes(W, H, [([(606, 210), (626, 172)], 6, (0.2, 0.2)), ([(632, 210), (644, 186)], 4, (0.2, 0.2))]) * win
    art = OV(art, shine, lambda q: flat(q, "#ffffff", 0.75))
    divider_ = strokes(W, H, [([(652, 164), (652, 220)], 4, None)])
    art = G(art, divider_, NAVY, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)
    door = strokes(W, H, [([(588, 232), (588, 340), (700, 340)], 2.4, None)])
    art = G(art, door, RED_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4)
    art = PP(art, W, H, shapes(W, H, [rrect(600, 246, 628, 254, 3)]), GREY, GREY_D, nx, hi=0.4, line=False)
    # star badge on the cab door
    st = [(664 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 10), 292 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 10)) for k in range(10)]
    art = PP(art, W, H, shapes(W, H, [st], smooth=False), YEL, YEL_D, nx, hi=0.4)
    # stripe, bumper, headlight, beacon
    stripe = shapes(W, H, [rect(50, 318, 760, 334)], smooth=False) * dilate(np.maximum(body, cm), 0.5)
    art = PP(art, W, H, stripe, YEL, YEL_D, nx, hi=0.35, line=False)
    art = PP(art, W, H, shapes(W, H, [rrect(700, 352, 790, 378, 8)]), GREY, GREY_D, nx, hi=0.4)
    art = PP(art, W, H, shapes(W, H, [rrect(40, 356, 120, 378, 8)]), GREY, GREY_D, nx, hi=0.4)
    hl = circles(W, H, [(748, 300, 13)])
    art = over(art, glow(hl, "#fff3b0", 10, 0.5))
    art = PP(art, W, H, hl, "#fff3b0", YEL, nx, hi=0.6)
    beacon = shapes(W, H, [rrect(612, 116, 676, 140, 10)])
    art = PP(art, W, H, beacon, "#ff6f61", RED, nx, hi=0.5)
    art = OV(art, shapes(W, H, [rrect(622, 120, 640, 128, 4)]), lambda q: flat(q, "#ffffff", 0.7))
    # mud flaps + wheels
    for x in (190, 330, 650):
        art = PP(art, W, H, circles(W, H, [(x, 372, 62)]) * (np.arange(H)[:, None] < 372), "#2c3550", "#1f2740", nx, hi=0.1)
    for x in (190, 330, 650):
        art = wheel(art, W, H, x, gy - 52, 52, nx)
    art = add_grain(art, 3, 0.025)
    preview(art, "up-truck", bg="#fff7ea")
    save(art, f"{OUT}/truck.webp", max_w=560, quality=84)


def helmet():
    W, H = 360, 300
    nx = Seq(300)
    art = blank(W, H)
    brim = shapes(W, H, [[(20, 220), (60, 200), (180, 196), (300, 200), (344, 222), (336, 246), (180, 238), (28, 246)]])
    dome = shapes(W, H, [[(60, 214)] + arc_pts(180, 214, 120, math.pi, math.tau, 30, 1.25)[1:] + [(300, 214)]])
    art = PP(art, W, H, brim, RED_D, "#8f1c16", nx, shade_dir=(0, 1), hi=0.3)
    art = PP(art, W, H, dome, RED, RED_D, nx, shade_dir=(1, 1), shade=0.32, hi=0.32)
    comb = strokes(W, H, [(arc_pts(180, 214, 112, math.pi * 1.1, math.pi * 1.9, 20, 1.25), 12, (0.1, 0.1))]) * dome
    art = G(art, comb, RED_D, seed=nx(), density=0.45, edge=0.2, bloom=0, rough=0.5)
    ridge = strokes(W, H, [([(180, 70), (180, 200)], 14, (0.1, 0.1))])
    art = PP(art, W, H, ridge * dome, RED_L, RED, nx, hi=0.4)
    shield = shapes(W, H, [[(140, 120), (220, 120), (226, 170), (180, 200), (134, 170)]])
    art = PP(art, W, H, shield, YEL, YEL_D, nx, hi=0.45)
    st = [(180 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9), 156 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9)) for k in range(10)]
    art = PP(art, W, H, shapes(W, H, [st], smooth=False), RED, RED_D, nx, hi=0.3, line=False)
    shine = strokes(W, H, [(arc_pts(180, 214, 92, math.pi * 1.18, math.pi * 1.42, 12, 1.25), 9, (0.3, 0.3))])
    art = OV(art, shine * dome, lambda q: flat(q, "#ffffff", 0.55))
    preview(art, "up-helmet", bg=SKY)
    save(art, f"{OUT}/helmet.webp", max_w=220, quality=84)


def water():
    """Brass nozzle at the bottom right with a hose tail, and a big friendly water arc of droplets curving up-left."""
    W, H = 640, 420
    nx = Seq(500); rng = random.Random(4)
    art = blank(W, H)
    path = [(560 - 520 * t, 360 - 520 * t * (1 - t) * 1.25 - 40 * t) for t in np.linspace(0, 1, 50)]
    for k, (wd, col, col2, d) in enumerate([(46, "#bfe6f8", "#9ad6f2", 0.7), (24, WATER, WATER_D, 0.9), (8, "#ffffff", "#e8f6fd", 0.9)]):
        m = strokes(W, H, [(path[:44 - k * 3], wd, (0.05, 0.6))])
        art = G(art, m, col, col2, seed=nx(), density=d, edge=0.5, bloom=0.35, rough=2.5)
    drops = []
    for i in range(110):
        t = rng.uniform(0.25, 1.0)
        x, y = path[min(49, int(t * 49))]
        drops.append((x + rng.gauss(0, 16), y + rng.gauss(0, 14) + 8, rng.uniform(2.5, 7)))
    dm = circles(W, H, drops)
    art = G(art, dm, WATER, WATER_D, seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1)
    art = OV(art, circles(W, H, [(x - r * 0.3, y - r * 0.3, r * 0.3) for x, y, r in drops]), lambda q: flat(q, "#ffffff", 0.9))
    hose = strokes(W, H, [(curve([(640, 410), (610, 400), (590, 380), (572, 366)], 20), 18, None)])
    art = PP(art, W, H, hose, "#f4f1ea", "#d9d4c8", nx, hi=0.3)
    nozzle = shapes(W, H, [rot([(548, 348), (590, 348), (594, 374), (544, 374)], 570, 361, -0.75)], smooth=False)
    art = PP(art, W, H, nozzle, YEL, YEL_D, nx, hi=0.45)
    preview(art, "up-water", bg=SKY)
    save(art, f"{OUT}/water.webp", max_w=420, quality=82)


def divider():
    """A short wavy fire hose with a brass nozzle and three water drops."""
    W, H = 480, 90
    nx = Seq(700)
    art = blank(W, H)
    hose = [(30 + t * 340, 46 + 12 * math.sin(t * math.tau * 1.5)) for t in np.linspace(0, 1, 40)]
    hm = strokes(W, H, [(hose, 14, (0.02, 0.0))])
    art = PP(art, W, H, hm, RED, RED_D, nx, shade_dir=(0, 1), hi=0.35, off=5)
    noz = shapes(W, H, [[(366, 36), (410, 40), (410, 52), (366, 56)]], smooth=False)
    art = PP(art, W, H, noz, YEL, YEL_D, nx, hi=0.45, off=5)
    for (x, y, r) in [(430, 46, 7), (452, 40, 5), (468, 50, 4)]:
        d = shapes(W, H, [[(x, y - r * 1.8)] + arc_pts(x, y, r, -0.3, math.pi + 0.3, 14)[::-1]])
        art = PP(art, W, H, d, WATER, WATER_D, nx, hi=0.5, off=3)
    preview(art, "up-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


def station():
    """Cover scene: sky with clouds, brick fire station with a tall arched open door, side tower with a bell,
    bunting across the facade, balloons, driveway."""
    W, H = 720, 1260
    rng = random.Random(8); nx = Seq(900)
    art = painted_sky(W, H, [(0, "#8fd1ef"), (0.45, "#b9e5f6"), (0.62, "#d6f0fa"), (1, "#d6f0fa")], seed=2, streak=0.8)
    for (cx, cy, s) in [(120, 140, 1.0), (560, 260, 1.2), (330, 470, 0.8), (620, 560, 0.7)]:
        cl = shapes(W, H, [ellipse_pts(cx + dx * s, cy + dy * s, r * s, r * 0.8 * s, 16) for dx, dy, r in [(-50, 10, 34), (-10, -8, 46), (40, 6, 36), (0, 20, 40)]])
        art = PP(art, W, H, cl, "#ffffff", "#eaf6fc", nx, shade_dir=(0, 1), shade=0.15, hi=0.2, line=False)
    clear()
    top = 640
    # tower on the left
    tower = shapes(W, H, [rect(20, top - 210, 150, 1120)], smooth=False)
    art = PP(art, W, H, tower, BRICK, BRICK_D, nx, shade_dir=(1, 0), hi=0.18)
    troof = shapes(W, H, [[(6, top - 206), (85, top - 290), (164, top - 206)]], smooth=False)
    art = PP(art, W, H, troof, NAVY, "#2c3a5c", nx, hi=0.25)
    belfry = shapes(W, H, [rrect(46, top - 190, 124, top - 110, 30)])
    art = PP(art, W, H, belfry, "#2c3550", "#1f2740", nx, hi=0.1)
    bell = shapes(W, H, [[(64, top - 128), (70, top - 168), (85, top - 178), (100, top - 168), (106, top - 128)]])
    art = PP(art, W, H, bell, YEL, YEL_D, nx, hi=0.45)
    # main building
    bld = shapes(W, H, [rect(130, top, 700, 1120)], smooth=False)
    art = PP(art, W, H, bld, BRICK, BRICK_D, nx, shade_dir=(1, 0), shade=0.2, hi=0.15)
    # bricks texture on all brick walls
    walls = np.maximum(tower, bld)
    bricks = []
    for j, y in enumerate(range(top - 200, 1120, 22)):
        bricks.append(([(0, y), (W, y)], 1.6, None))
        for x in range((j % 2) * 24, W, 48):
            bricks.append(([(x, y), (x, y + 22)], 1.6, None))
    art = G(art, strokes(W, H, bricks) * walls, BRICK_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    parapet = shapes(W, H, [rect(122, top - 30, 708, top + 16)], smooth=False)
    art = PP(art, W, H, parapet, CREAM, "#f0e4cc", nx, shade_dir=(0, 1), hi=0.2)
    # sign board (blank, the page writes on top)
    sign = shapes(W, H, [rrect(240, top + 40, 590, top + 104, 10)])
    art = PP(art, W, H, sign, CREAM, "#f3e9d2", nx, hi=0.2)
    art = G(art, edge_ring(sign, 4), RED, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.4)
    st = [(415 + math.cos(-math.pi / 2 + k * math.pi / 5) * (20 if k % 2 == 0 else 8), top + 72 + math.sin(-math.pi / 2 + k * math.pi / 5) * (20 if k % 2 == 0 else 8)) for k in range(10)]
    art = PP(art, W, H, shapes(W, H, [st], smooth=False), RED, RED_D, nx, hi=0.3)
    # big arched door, open, dark garage inside
    door = shapes(W, H, [[(226, 1120), (226, 960)] + arc_pts(415, 960, 189, math.pi, math.tau, 30)[1:-1] + [(604, 960), (604, 1120)]])
    frame = dilate(door, 5)
    art = PP(art, W, H, frame, CREAM, "#f0e4cc", nx, hi=0.2)
    art = PP(art, W, H, door, "#2c3550", "#1f2740", nx, shade_dir=(0, -1), shade=0.2, hi=0.08, line=False)
    rollup = strokes(W, H, [([(205, y), (625, y)], 3, None) for y in range(776, 840, 14)]) * door
    art = G(art, rollup, "#3a4566", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4)
    floor_glow = door * np.clip((np.arange(H)[:, None] - 980) / 140, 0, 1)
    art = OV(art, floor_glow, lambda q: flat(q, "#4a5a80", 0.5))
    # bunting across the parapet, from the tower to the right edge
    flags = []
    cols = [RED, YEL, WATER, "#ffffff"]
    pts = [(150 + t * 570, top - 26 + 44 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 13)]
    art = G(art, strokes(W, H, [(pts, 2.4, None)]), NAVY, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    for i in range(12):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        tri = [(x0 + 4, y0), (x1 - 4, y1), ((x0 + x1) / 2, (y0 + y1) / 2 + 40)]
        art = PP(art, W, H, shapes(W, H, [tri], smooth=False), cols[i % 4], mix(cols[i % 4], NAVY, 0.15), nx, hi=0.25, off=5)
    clear()
    # balloons tied to the tower
    for (bx, by, col) in [(170, top - 150, RED), (210, top - 210, YEL), (250, top - 160, WATER)]:
        string = strokes(W, H, [(curve([(bx, by + 46), (bx - 10, by + 100), (150, top - 60)], 16), 1.6, None)])
        art = G(art, string, NAVY, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
        bm = shapes(W, H, [ellipse_pts(bx, by, 36, 44, 20)])
        art = PP(art, W, H, bm, col, mix(col, NAVY, 0.15), nx, hi=0.4)
        art = OV(art, ellipses(W, H, [(bx - 12, by - 16, 7, 12, -20)]), lambda q: flat(q, "#ffffff", 0.7))
    # windows on the tower
    for y in (top + 20, top + 140):
        wm = shapes(W, H, [rrect(56, y, 114, y + 70, 26)])
        art = PP(art, W, H, wm, "#cdeefc", "#a5dcf3", nx, hi=0.4)
    # driveway + curb + painted lines
    drive = shapes(W, H, [rect(0, 1112, W, H)], smooth=False)
    art = PP(art, W, H, drive, "#b9bec9", "#a3a9b6", nx, shade_dir=(0, 1), shade=0.1, hi=0.1, line=False)
    art = PP(art, W, H, shapes(W, H, [rect(0, 1108, W, 1124)], smooth=False), "#e8e4dc", "#d6d0c4", nx, hi=0.2)
    lines = shapes(W, H, [[(300 + k * 120, 1150), (330 + k * 120, 1150), (350 + k * 140, H), (300 + k * 140, H)] for k in range(-2, 4)], smooth=False) * drive
    art = G(art, lines, YEL, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=1)
    # bushes
    for (x, r) in [(160, 40), (676, 44)]:
        bm = shapes(W, H, [ellipse_pts(x + dx, 1106 - r * 0.5 + dy, r * 0.6, r * 0.5, 14) for dx, dy in [(-r * 0.5, 0), (0, -r * 0.3), (r * 0.5, 0)]])
        art = PP(art, W, H, bm, "#6cc05a", "#4f9a48", nx, hi=0.3)
    art = add_grain(art, 5, 0.025)
    preview(art, "up-station")
    save_rgb(art, f"{OUT}/station.webp", size=(600, 1050), quality=76)


for p in PARTS:
    globals()[p]()
    clear()
