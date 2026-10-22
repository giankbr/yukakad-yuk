"""Ultah Truk — kids birthday with friendly construction vehicles in gouache + crayon (original designs): a yellow dump
truck carrying a dirt heap, an orange excavator scooping, a blue cement mixer with a striped drum (each with smiling
windscreen eyes), road cones, a dirt road with tyre tracks and a gravel pile. Run: python3 -I ultah-truk.py [part ...]
parts: dump digger mixer cone road   Assets -> public/themes/art/ultah-truk/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e5_lib import *  # noqa

OUT = outdir("ultah-truk")
PARTS = sys.argv[1:] or ["dump", "digger", "mixer", "cone", "road"]
INK = "#2b2b33"
YEL, YEL2, YELD, YELL = "#f5b819", "#f8c63c", "#c98a0c", "#ffe08a"
ORA, ORA2, ORAD, ORAL = "#f07c22", "#f48f3c", "#b8561a", "#ffb878"
BLU, BLU2, BLUD, BLUL = "#3b7fc4", "#4b8fd0", "#24588f", "#8fc0ea"
RED, REDD = "#d9473a", "#9e2f26"
CHAR, CHAR2, CHARD = "#3a3b42", "#45464e", "#1e1f24"
DIRT, DIRT2, DIRTD, DIRTL = "#b9824c", "#c8925a", "#7e5530", "#e0b07a"
GLASS, GLASSL = "#bfe3f2", "#eaf7fc"
CREAM = "#fbf4e4"
BG = "#fbf3df"


def outline(art, m, nx, col=INK, amt=0.75):
    return crayon(art, inner_edge(m, 2.4), col, seed=nx(), amt=amt, tooth=0.3)


def part(art, m, c, c2, d, l, nx, ldir=(12, 12), blur=10, line=True):
    art = body_paint(art, m, c, c2, d, l, nx, ldir=ldir, blur=blur, light_amt=0.4, dark_amt=0.55)
    if line:
        art = outline(art, m, nx, mix(d, INK, .5), 0.7)
    return art


def window_face(art, W, H, x0, y0, x1, y1, nx, r=14):
    """Windscreen with a friendly face: two oval eyes with shine, rosy cheek, small smile below the glass."""
    win = shapes(W, H, [[(x0 + r, y0), (x1 - r * .6, y0), (x1, y0 + r), (x1, y1), (x0, y1), (x0, y0 + r)]])
    art = body_paint(art, win, GLASS, "#cdeaf5", "#8cbfd6", GLASSL, nx, ldir=(8, 8), blur=8, light_amt=0.5, dark_amt=0.5)
    art = OV(art, strokes(W, H, [([(x0 + (x1 - x0) * .18, y1 - 6), (x0 + (x1 - x0) * .48, y0 + 6)], 7, None)]) * win, lambda m: col_arr(m, "#ffffff", m * 0.55), pad=4)
    art = outline(art, win, nx, mix("#8cbfd6", INK, .5), 0.7)
    ex = (x0 + x1) / 2
    ey = y0 + (y1 - y0) * .58
    s_ = (x1 - x0) * 0.16
    art = eye(art, W, H, ex - s_, ey, s_ * 0.55, nx)
    art = eye(art, W, H, ex + s_, ey, s_ * 0.55, nx)
    return art


if "dump" in PARTS:
    W, H = 700, 470
    nx = Seq(91100); rng = random.Random(911)
    art = blank(W, H)
    art = soft_ground(art, W, H, 350, 410, 300, 20, "#6a4a30", nx, 0.35)
    # chassis
    ch = shapes(W, H, [[(70, 318), (620, 318), (620, 346), (70, 346)]], smooth=False)
    art = part(art, ch, CHAR, CHAR2, CHARD, "#6a6b72", nx, blur=5)
    # dirt heap in the bed (behind the bed walls)
    heap = shapes(W, H, [deform([(96, 182), (150, 120), (220, 92), (290, 104), (360, 140), (410, 182)], rng, 2, 0.02)])
    art = body_paint(art, heap, DIRT, DIRT2, DIRTD, DIRTL, nx, ldir=(14, 10), blur=14, light_amt=0.45)
    clods = [deform(ellipse_pts(rng.uniform(140, 380), rng.uniform(120, 175), rng.uniform(6, 12), rng.uniform(4, 8), 10, rng.uniform(0, 3)), rng, 1, 0.05) for _ in range(18)]
    art = GP(art, shapes(W, H, clods) * heap, DIRTD, "#6d4828", seed=nx(), rough=0.6, pad=6)
    art = GP(art, shapes(W, H, clods[::3]) * heap, DIRTL, seed=nx(), rough=0.6, pad=6)
    # bed: slightly tapered box with ribs
    bed = shapes(W, H, [[(70, 172), (420, 172), (410, 310), (88, 310)]], smooth=False)
    bed = np.clip(gaussian_filter(bed, 1.2) * 1.3, 0, 1)
    art = part(art, bed, YEL, YEL2, YELD, YELL, nx, ldir=(10, 14), blur=14)
    ribs = strokes(W, H, [([(x, 186), (x - 2, 300)], 9, None) for x in (128, 196, 264, 332, 392)])
    art = tint(art, ribs * bed, YELD, 0.55, seed=nx())
    art = tint(art, side_light(ribs * bed, -3, 0, 2), YELL, 0.5, seed=nx())
    top_rim = strokes(W, H, [([(66, 176), (424, 176)], 14, None)])
    art = part(art, top_rim, YEL2, YEL, YELD, YELL, nx, ldir=(0, 6), blur=4)
    # hinge + hydraulic ram
    art = GP(art, strokes(W, H, [([(380, 300), (430, 256)], 10, None)]), "#9aa0a8", "#c3c8cf", seed=nx(), rough=0.4, pad=6)
    # cab
    cab = shapes(W, H, [[(440, 150), (560, 150), (600, 214), (632, 226), (636, 314), (440, 314)]])
    art = part(art, cab, YEL, YEL2, YELD, YELL, nx, ldir=(10, 12), blur=14)
    art = window_face(art, W, H, 462, 168, 556, 236, nx)
    art = smile(art, W, H, 509, 262, 16, nx, a0=0.5, a1=2.6, w=3.2)
    art = cheek(art, W, H, 474, 262, 9, nx)
    art = cheek(art, W, H, 546, 262, 9, nx)
    # bumper, light, beacon, exhaust
    art = part(art, shapes(W, H, [[(600, 296), (646, 296), (646, 318), (600, 318)]], smooth=False), "#c9cdd3", "#dfe2e6", "#8f949b", "#ffffff", nx, blur=4)
    art = OV(art, circles(W, H, [(624, 248, 10)]), lambda m: glow(m, "#fff1b0", 10, 0.5), pad=30)
    art = part(art, circles(W, H, [(624, 248, 9)]), "#fff6cf", "#ffffff", "#e3c76a", "#ffffff", nx, blur=3)
    art = part(art, shapes(W, H, [[(492, 132), (526, 132), (522, 150), (496, 150)]], smooth=False), ORA, ORA2, ORAD, ORAL, nx, blur=4)
    art = part(art, strokes(W, H, [([(446, 312), (446, 112)], 10, None)]), "#8f949b", "#b5bac1", "#5f646b", "#e3e6ea", nx, blur=3)
    art = crayon(art, strokes(W, H, [(curve([(446, 104), (436, 84), (452, 70), (440, 50)], 20), 5, (0.1, 0.8))]), "#9aa0a8", seed=nx(), amt=0.5)
    # hazard stripe on the cab skirt
    st = stripes(W, H, 0.785, 10, 10, seed=nx()) * shapes(W, H, [[(440, 296), (600, 296), (600, 314), (440, 314)]], smooth=False)
    art = GP(art, st, INK, seed=nx(), rough=0.4)
    clear()
    for x in (160, 330, 548):
        art = wheel(art, W, H, x, 348, 50, nx)
    preview(art, "tr-dump", tone=BG)
    save(art, f"{OUT}/dump.webp", max_w=440, quality=82)
    clear()

if "digger" in PARTS:
    W, H = 680, 560
    nx = Seq(91200); rng = random.Random(912)
    art = blank(W, H)
    art = soft_ground(art, W, H, 300, 510, 260, 18, "#6a4a30", nx, 0.35)
    # tracks
    tr = shapes(W, H, [[(90, 430), (430, 430), (470, 466), (430, 502), (90, 502), (52, 466)]])
    art = part(art, tr, CHAR, CHAR2, CHARD, "#6a6b72", nx, blur=8)
    art = crayon(art, strokes(W, H, [([(x, 432), (x, 500)], 4, None) for x in range(96, 430, 18)]) * tr, "#55565e", seed=nx(), amt=0.7)
    for x in (110, 190, 270, 350, 420):
        art = wheel(art, W, H, x, 466, 22, nx, tyre="#2a2a30", hub="#9aa0a8", hub2="#7a8088", bolt="#4a4e55")
    # turret + counterweight
    tur = shapes(W, H, [[(96, 330), (390, 330), (400, 424), (86, 424)]])
    art = part(art, tur, ORA, ORA2, ORAD, ORAL, nx, ldir=(10, 12), blur=14)
    cw = shapes(W, H, [[(70, 344), (130, 344), (130, 420), (66, 420)]])
    art = part(art, cw, CHAR2, "#55565e", CHARD, "#7a7b84", nx, blur=6)
    st = stripes(W, H, 0.785, 11, 11, seed=nx()) * shapes(W, H, [[(140, 398), (390, 398), (392, 418), (140, 418)]], smooth=False)
    art = GP(art, st, INK, seed=nx(), rough=0.4)
    # cab
    cab = shapes(W, H, [[(200, 196), (320, 196), (340, 220), (344, 336), (196, 336)]])
    art = part(art, cab, ORA, ORA2, ORAD, ORAL, nx, ldir=(10, 12), blur=12)
    art = window_face(art, W, H, 216, 212, 324, 286, nx)
    art = smile(art, W, H, 270, 304, 15, nx, a0=0.5, a1=2.6, w=3.0)
    art = cheek(art, W, H, 228, 306, 8, nx)
    art = cheek(art, W, H, 312, 306, 8, nx)
    art = part(art, shapes(W, H, [[(250, 178), (286, 178), (282, 196), (254, 196)]], smooth=False), YEL, YEL2, YELD, YELL, nx, blur=4)
    clear()
    # boom + stick + bucket (to the right, scooping)
    boom = shapes(W, H, [[(350, 352), (380, 326), (500, 150), (532, 140), (552, 168), (420, 368)]])
    art = part(art, boom, ORA, ORA2, ORAD, ORAL, nx, ldir=(10, 10), blur=10)
    stick = shapes(W, H, [[(520, 150), (552, 146), (616, 330), (588, 340)]])
    art = part(art, stick, ORA2, ORA, ORAD, ORAL, nx, ldir=(10, 8), blur=8)
    rams = strokes(W, H, [([(400, 300), (500, 196)], 9, None), ([(548, 172), (604, 290)], 8, None)])
    art = part(art, rams, "#c9cdd3", "#dfe2e6", "#7f848b", "#ffffff", nx, blur=3)
    art = part(art, circles(W, H, [(536, 160, 12), (602, 330, 11), (386, 342, 12)]), CHAR, CHAR2, CHARD, "#7a7b84", nx, blur=3)
    bucket = shapes(W, H, [[(586, 322), (636, 318), (650, 380), (630, 430), (594, 436), (560, 410), (566, 380)]])
    art = part(art, bucket, CHAR2, "#55565e", CHARD, "#7a7b84", nx, ldir=(8, 8), blur=8)
    teeth = shapes(W, H, [[(566 + i * 18, 412 + i * 6), (576 + i * 18, 428 + i * 6), (584 + i * 18, 414 + i * 6)] for i in range(3)], smooth=False)
    art = GP(art, teeth, "#b5bac1", seed=nx(), rough=0.3, pad=6)
    # scoop of dirt
    sc = shapes(W, H, [deform([(590, 324), (612, 300), (640, 306), (650, 324)], rng, 1, 0.03)])
    art = body_paint(art, sc, DIRT, DIRT2, DIRTD, DIRTL, nx, ldir=(4, 6), blur=5)
    crumbs = circles(W, H, [(rng.uniform(560, 660), rng.uniform(440, 500), rng.uniform(3, 6)) for _ in range(9)])
    art = GP(art, crumbs, DIRTD, DIRT, seed=nx(), rough=0.5, pad=6)
    preview(art, "tr-digger", tone=BG)
    save(art, f"{OUT}/digger.webp", max_w=400, quality=82)
    clear()

if "mixer" in PARTS:
    W, H = 720, 470
    nx = Seq(91300); rng = random.Random(913)
    art = blank(W, H)
    art = soft_ground(art, W, H, 360, 412, 300, 20, "#6a4a30", nx, 0.35)
    ch = shapes(W, H, [[(60, 314), (640, 314), (640, 344), (60, 344)]], smooth=False)
    art = part(art, ch, CHAR, CHAR2, CHARD, "#6a6b72", nx, blur=5)
    # drum support
    art = part(art, shapes(W, H, [[(110, 314), (140, 230), (170, 314)]], smooth=False), "#9aa0a8", "#b5bac1", "#5f646b", "#e3e6ea", nx, blur=4)
    art = part(art, shapes(W, H, [[(380, 314), (400, 210), (430, 314)]], smooth=False), "#9aa0a8", "#b5bac1", "#5f646b", "#e3e6ea", nx, blur=4)
    # drum: tilted barrel with red/white spiral stripes
    cx, cy, a = 270, 196, -0.2
    ca, sa = math.cos(a), math.sin(a)
    P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
    drum_pts = [P(-190, -40), P(-120, -92), P(60, -104), P(170, -76), P(205, 0), P(170, 76), P(60, 104), P(-120, 92), P(-190, 40)]
    drum = shapes(W, H, [drum_pts])
    art = part(art, drum, "#eef0f2", "#f8f9fa", "#9aa3ad", "#ffffff", nx, ldir=(6, 16), blur=20)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - cx) * ca + (yy - cy) * sa
    v = -(xx - cx) * sa + (yy - cy) * ca
    band = ((u * 0.9 + v * 0.75) / 58) % 1.0
    sp = np.clip(np.minimum(band, 0.42 - band) * 40 + 0.5, 0, 1) * (band < 0.44)
    art = GP(art, sp * drum, RED, "#e05a4c", seed=nx(), rough=0.8)
    art = tint(art, side_light(drum, 0, -16, 22), "#4a4f60", 0.38, seed=nx())
    art = tint(art, side_light(drum, 4, 14, 16), "#ffffff", 0.3, seed=nx())
    art = outline(art, drum, nx, "#5f646b", 0.7)
    # drum mouth + chute (rear, left)
    mouth = ellipses(W, H, [(P(-192, 0)[0], P(-192, 0)[1], 16, 40, -11)])
    art = part(art, mouth, CHAR, CHAR2, CHARD, "#6a6b72", nx, blur=4)
    chute = shapes(W, H, [[(70, 210), (96, 214), (64, 300), (36, 292)]])
    art = part(art, chute, ORA, ORA2, ORAD, ORAL, nx, blur=5)
    clear()
    # cab
    cab = shapes(W, H, [[(480, 132), (590, 132), (630, 200), (664, 214), (668, 312), (480, 312)]])
    art = part(art, cab, BLU, BLU2, BLUD, BLUL, nx, ldir=(10, 12), blur=14)
    art = window_face(art, W, H, 500, 150, 590, 220, nx)
    art = smile(art, W, H, 545, 248, 16, nx, a0=0.5, a1=2.6, w=3.2)
    art = cheek(art, W, H, 510, 250, 9, nx)
    art = cheek(art, W, H, 580, 250, 9, nx)
    art = part(art, shapes(W, H, [[(632, 294), (678, 294), (678, 316), (632, 316)]], smooth=False), "#c9cdd3", "#dfe2e6", "#8f949b", "#ffffff", nx, blur=4)
    art = part(art, circles(W, H, [(654, 240, 9)]), "#fff6cf", "#ffffff", "#e3c76a", "#ffffff", nx, blur=3)
    art = part(art, shapes(W, H, [[(524, 114), (556, 114), (552, 132), (528, 132)]], smooth=False), YEL, YEL2, YELD, YELL, nx, blur=4)
    st = stripes(W, H, 0.785, 10, 10, seed=nx()) * shapes(W, H, [[(480, 292), (632, 292), (632, 310), (480, 310)]], smooth=False)
    art = GP(art, st, YEL, seed=nx(), rough=0.4)
    for x in (140, 300, 582):
        art = wheel(art, W, H, x, 346, 48, nx)
    preview(art, "tr-mixer", tone=BG)
    save(art, f"{OUT}/mixer.webp", max_w=440, quality=82)
    clear()

if "cone" in PARTS:
    W, H = 220, 260
    nx = Seq(91400); rng = random.Random(914)
    art = blank(W, H)
    art = soft_ground(art, W, H, 110, 236, 90, 10, "#6a4a30", nx, 0.3)
    base = shapes(W, H, [[(24, 206), (196, 206), (204, 232), (16, 232)]])
    art = part(art, base, ORAD, ORA, "#7a3a12", ORAL, nx, blur=5)
    cone = shapes(W, H, [[(98, 24), (122, 24), (174, 212), (46, 212)]])
    art = part(art, cone, ORA, ORA2, ORAD, ORAL, nx, ldir=(14, 0), blur=16)
    for y0, y1 in ((82, 108), (146, 172)):
        t0, t1 = (y0 - 24) / 188, (y1 - 24) / 188
        bandm = shapes(W, H, [[(98 - 52 * t0, y0), (122 + 52 * t0, y0), (122 + 52 * t1, y1), (98 - 52 * t1, y1)]], smooth=False) * cone
        art = GP(art, bandm, "#f8f6f0", "#ffffff", seed=nx(), rough=0.5)
        art = tint(art, side_light(bandm, 10, 0, 6), "#c8c2b8", 0.5, seed=nx())
    art = outline(art, cone, nx, mix(ORAD, INK, .4), 0.6)
    preview(art, "tr-cone", tone=BG)
    save(art, f"{OUT}/cone.webp", max_w=100, quality=84)
    clear()

if "road" in PARTS:
    W, H = 900, 240
    nx = Seq(91500); rng = random.Random(915)
    art = blank(W, H)
    top = lambda x: 70 + 10 * math.sin(x * 0.012) + 5 * math.sin(x * 0.05)
    g = shapes(W, H, [contour(top, -10, 910) + [(910, 250), (-10, 250)]])
    art = GP(art, g, DIRT2, DIRT, seed=nx(), rough=2.5, streak=0.6)
    art = tint(art, gaussian_filter(g, 20) * (np.arange(H)[:, None] / H), DIRTD, 0.35, seed=nx())
    # tyre tracks
    tracks = []
    for y0 in (130, 178):
        tracks.append(([(x, y0 + 6 * math.sin(x * 0.01)) for x in np.linspace(-10, 910, 60)], 16, None))
    tm = strokes(W, H, tracks) * g
    art = tint(art, tm, DIRTD, 0.42, seed=nx())
    treads = strokes(W, H, [([(x, y0 - 6 + 6 * math.sin(x * 0.01)), (x + 6, y0 + 6 + 6 * math.sin(x * 0.01))], 3, None) for y0 in (130, 178) for x in range(0, 900, 14)]) * g
    art = tint(art, treads, "#6d4828", 0.4, seed=nx())
    # pebbles
    pb = [deform(ellipse_pts(rng.uniform(0, 900), rng.uniform(90, 230), rng.uniform(3, 8), rng.uniform(2, 5), 8, rng.uniform(0, 3)), rng, 1, 0.08) for _ in range(70)]
    art = GP(art, shapes(W, H, pb) * g, "#8d7a66", "#a8957f", seed=nx(), rough=0.5, pad=6)
    art = GP(art, shapes(W, H, pb[::2]) * g, DIRTL, seed=nx(), rough=0.5, pad=6)
    # grass tufts along the top edge
    tufts = []
    for x in np.arange(0, 900, 22) + rng.uniform(-6, 6):
        for k in range(4):
            a = -math.pi / 2 + rng.uniform(-0.6, 0.6)
            L = rng.uniform(12, 26)
            tufts.append(([(x + k * 3, top(x) + 6), (x + k * 3 + math.cos(a) * L, top(x) + 6 + math.sin(a) * L)], 3.2, (0.0, 0.8)))
    art = GP(art, strokes(W, H, tufts), "#6aa84f", "#4f8a3c", seed=nx(), rough=0.6, pad=6)
    # gravel heap on the left
    heap = shapes(W, H, [deform([(40, 100), (90, 40), (150, 22), (210, 46), (250, 100)], rng, 2, 0.02)])
    art = body_paint(art, heap, "#a3927e", "#b5a48f", "#6f604f", "#d6c8b6", nx, ldir=(12, 10), blur=14)
    gp = [deform(ellipse_pts(rng.uniform(70, 230), rng.uniform(40, 96), rng.uniform(3, 6), rng.uniform(2, 4), 8, rng.uniform(0, 3)), rng, 1, 0.08) for _ in range(40)]
    art = GP(art, shapes(W, H, gp) * heap, "#7f705f", "#e1d5c4", seed=nx(), rough=0.5, pad=6)
    preview(art, "tr-road", tone=BG)
    save(art, f"{OUT}/road.webp", max_w=640, quality=78)
    clear()
