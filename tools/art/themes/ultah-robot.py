"""Ultah Robot — original friendly robots for a kids' birthday (gouache, poster-paint feel; no known characters):
"Bip", a big teal-and-orange robot waving with a blank chest screen (the age is typeset over it in HTML), a little
yellow propeller drone, two cog wheels and a robot-head birthday cake with candles.
Run: python3 -I ultah-robot.py [part ...]   parts: robot drone gears cake
Assets -> public/themes/art/ultah-robot/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h1_lib import *  # noqa

OUT = outdir("ultah-robot")
PARTS = sys.argv[1:] or ["robot", "drone", "gears", "cake"]
TEAL, TEAL_D, TEAL_L = "#38b2a6", "#23857c", "#7fd8cc"
ORANGE, ORANGE_D, ORANGE_L = "#f28a4a", "#c9622a", "#ffb27e"
YELLOW, YELLOW_D = "#f7c948", "#d29a1e"
NAVY, NAVY_D = "#2c3a5e", "#1c2642"
STEEL, STEEL_D, STEEL_L = "#aab4c0", "#7a8594", "#dfe5ec"
CREAM, PINK, CYAN = "#fff6e6", "#f59bb0", "#9ef2ff"


def body(art, W, H, m, col, col2, deep, light, nx, lx0, lx1, ly0=None, ly1=None, hi=True):
    """Rounded painted volume: gouache base, shade to the lower right, a dry-brush highlight upper left, dark rim."""
    art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=0.8)
    sh = xgrad(W, H, lx0 + (lx1 - lx0) * 0.45, lx1)
    if ly0 is not None:
        sh = np.maximum(sh, ygrad(W, H, ly0 + (ly1 - ly0) * 0.55, ly1) * 0.8)
    art = G(art, m * sh, deep, seed=nx(), density=0.5, edge=0.25, bloom=0.3, rough=2, feather=3)
    if hi:
        hl = m * np.clip(1 - xgrad(W, H, lx0, lx0 + (lx1 - lx0) * 0.35), 0, 1)
        if ly0 is not None:
            hl *= np.clip(1 - ygrad(W, H, ly0, ly0 + (ly1 - ly0) * 0.5), 0, 1)
        art = G(art, gaussian_filter(hl, 4), light, seed=nx(), density=0.55, edge=0, bloom=0.3, rough=2, feather=3)
    rim = np.clip(m - gaussian_filter(m, 2.2) * 1.12, 0, 1) * 2.2
    art = G(art, rim, deep, seed=nx(), density=0.7, edge=0, rough=0.6, feather=0.6)
    return art


def rivets(art, W, H, pts, r, nx, col=STEEL_L, deep=STEEL_D):
    m = circles(W, H, [(x, y, r) for x, y in pts])
    art = GP(art, m, col, seed=nx(), rough=0.4, streak=0.2, pad=6)
    art = G(art, circles(W, H, [(x + r * 0.35, y + r * 0.35, r * 0.6) for x, y in pts]) * m, deep, seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.6, pad=6)
    return art


def tube(art, W, H, pts, wd, nx, col=STEEL, deep=STEEL_D, light=STEEL_L, rings=6):
    """Flexible arm: a thick stroke with ribbed rings."""
    path = curve(pts, 40)
    m = strokes(W, H, [(path, wd, None)])
    art = GP(art, m, col, mix_hex(col, deep, 0.3), seed=nx(), rough=1.0, streak=0.6)
    rg = []
    for k in range(1, rings * 3):
        i = int(k / (rings * 3) * (len(path) - 2))
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        rg.append(([(x0 - math.cos(a) * wd * 0.48, y0 - math.sin(a) * wd * 0.48), (x0 + math.cos(a) * wd * 0.48, y0 + math.sin(a) * wd * 0.48)], 1.6, None))
    art = G(art, strokes(W, H, rg) * m, deep, seed=nx(), density=0.55, edge=0, rough=0.4, feather=0.5)
    off = [(x - 3, y - 3) for x, y in path]
    art = G(art, strokes(W, H, [(off, wd * 0.25, (0.1, 0.1))]) * m, light, seed=nx(), density=0.55, edge=0, rough=0.4, feather=1.5)
    return art


def claw(art, W, H, x, y, r, ang, nx):
    """C-shaped gripper hand."""
    pts = arc_pts(x, y, r, ang + 0.75, ang + math.tau - 0.75, 24)
    m = strokes(W, H, [(pts, r * 0.55, (0.1, 0.1))])
    art = body(art, W, H, m, NAVY, "#34446c", NAVY_D, "#6a7ba8", nx, x - r, x + r, y - r, y + r)
    art = body(art, W, H, circles(W, H, [(x, y, r * 0.38)]) * 0 + circles(W, H, [(x - math.cos(ang) * r * 0.9, y - math.sin(ang) * r * 0.9, r * 0.45)]), STEEL, STEEL, STEEL_D, STEEL_L, nx, x - r, x + r)
    return art


def eye(art, W, H, x, y, r, nx, look=(0.12, 0.05)):
    art = over(art, glow(circles(W, H, [(x, y, r)]), CYAN, radius=r * 0.5, strength=0.35))
    art = GP(art, circles(W, H, [(x, y, r)]), "#e9fdff", "#bff3fb", seed=nx(), rough=0.8, streak=0.4, pad=8)
    art = GP(art, circles(W, H, [(x + r * look[0], y + r * look[1], r * 0.52)]), NAVY_D, "#202d50", seed=nx(), rough=0.6, streak=0.3, pad=8)
    art = GP(art, circles(W, H, [(x - r * 0.08, y - r * 0.18, r * 0.18), (x + r * 0.3, y + r * 0.25, r * 0.08)]), "#ffffff", seed=nx(), rough=0.3, streak=0.2, pad=8)
    return art


def part_robot():
    W, H = 660, 820
    rng = random.Random(71); nx = Seq(100)
    art = blank(W, H)
    # floor shadow
    art = G(art, ellipses(W, H, [(330, 752, 220, 22, 0)]), "#2c3a5e", seed=nx(), density=0.22, edge=0.1, bloom=0.3, rough=3, feather=6)
    # legs + feet
    for x in (245, 395):
        lm = rrect(W, H, x - 30, 590, x + 30, 700, 14)
        art = body(art, W, H, lm, STEEL, "#9aa5b2", STEEL_D, STEEL_L, nx, x - 30, x + 30)
        art = G(art, rect(W, H, x - 30, 640, x + 30, 648), STEEL_D, seed=nx(), density=0.55, edge=0, rough=0.4, feather=0.6)
        fm = rrect(W, H, x - 58, 690, x + 58, 748, 26)
        art = body(art, W, H, fm, NAVY, "#34446c", NAVY_D, "#6a7ba8", nx, x - 58, x + 58, 690, 748)
        art = rivets(art, W, H, [(x - 34, 720), (x, 722), (x + 34, 720)], 5, nx)
        clear()
    # left arm waving (behind body), right arm down
    art = tube(art, W, H, [(190, 400), (120, 370), (96, 300), (104, 236)], 30, nx)
    art = claw(art, W, H, 106, 206, 30, -math.pi / 2, nx)
    art = tube(art, W, H, [(470, 400), (532, 450), (552, 530), (548, 580)], 30, nx)
    art = claw(art, W, H, 548, 606, 30, math.pi / 2, nx)
    clear()
    # torso
    tm = rrect(W, H, 172, 330, 488, 610, 56)
    art = body(art, W, H, tm, ORANGE, "#f49a5e", ORANGE_D, ORANGE_L, nx, 172, 488, 330, 610)
    # chest screen (blank: the age is set in HTML on top)
    sm = rrect(W, H, 230, 372, 430, 524, 26)
    art = GP(art, displace(rrect(W, H, 222, 364, 438, 532, 32), nx(), 1, 10), "#e9e2d2", "#d6cfbf", seed=nx(), rough=0.8, streak=0.5)
    art = GP(art, sm, NAVY, "#243256", seed=nx(), rough=0.8, streak=0.6)
    art = G(art, sm * radial(W, H, 330, 448, 120, 0.8), "#2f5f7a", seed=nx(), density=0.6, edge=0, bloom=0.3, rough=2, feather=4)
    scan = [([(236, y), (424, y)], 1.1, None) for y in range(380, 520, 6)]
    art = G(art, strokes(W, H, scan) * sm, "#3a7d92", seed=nx(), density=0.25, edge=0, rough=0.3, feather=0.4)
    art = G(art, gaussian_filter(rrect(W, H, 244, 382, 300, 400, 8), 2), "#ffffff", seed=nx(), density=0.3, edge=0, rough=0.5, feather=1)
    # buttons + dial
    art = rivets(art, W, H, [(186, 350), (474, 350), (186, 590), (474, 590)], 6, nx)
    for (x, c, d) in [(262, YELLOW, YELLOW_D), (312, TEAL, TEAL_D), (362, "#ef5b5b", "#b83a3a")]:
        bm = circles(W, H, [(x, 562, 15)])
        art = body(art, W, H, bm, c, c, d, "#ffffff", nx, x - 15, x + 15, 547, 577)
    knob = circles(W, H, [(412, 562, 20)])
    art = body(art, W, H, knob, STEEL, STEEL, STEEL_D, STEEL_L, nx, 392, 432, 542, 582)
    art = G(art, strokes(W, H, [([(412, 562), (424, 550)], 3.5, None)]), NAVY_D, seed=nx(), density=0.85, edge=0, rough=0.3, feather=0.4)
    clear()
    # neck
    nm = rect(W, H, 296, 292, 364, 336)
    art = body(art, W, H, nm, STEEL, "#9aa5b2", STEEL_D, STEEL_L, nx, 296, 364)
    art = G(art, strokes(W, H, [([(296, y), (364, y)], 2, None) for y in (304, 316, 326)]), STEEL_D, seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    # ears (discs) + antenna stalk (ball left for CSS blink, a painted base ball under it)
    for x in (172, 488):
        em = circles(W, H, [(x, 196, 30)])
        art = body(art, W, H, em, YELLOW, YELLOW, YELLOW_D, "#fff1b8", nx, x - 30, x + 30, 166, 226)
        art = rivets(art, W, H, [(x, 196)], 9, nx)
    art = GP(art, strokes(W, H, [([(330, 100), (326, 70), (334, 46)], 7, None)]), STEEL_D, STEEL, seed=nx(), rough=0.5, streak=0.4)
    ball = circles(W, H, [(334, 34, 17)])
    art = body(art, W, H, ball, "#ef5b5b", "#f27272", "#b83a3a", "#ffc2c2", nx, 317, 351, 17, 51)
    # head
    hm = rrect(W, H, 188, 92, 472, 300, 64)
    art = body(art, W, H, hm, TEAL, "#45bdb0", TEAL_D, TEAL_L, nx, 188, 472, 92, 300)
    fm = rrect(W, H, 222, 128, 438, 268, 44)
    art = GP(art, fm, NAVY, "#26345a", seed=nx(), rough=0.8, streak=0.6)
    art = G(art, gaussian_filter(rrect(W, H, 236, 140, 330, 158, 9), 3), "#ffffff", seed=nx(), density=0.22, edge=0, rough=0.5, feather=1)
    art = eye(art, W, H, 284, 194, 30, nx)
    art = eye(art, W, H, 376, 194, 30, nx)
    smile = arc_pts(330, 222, 34, 0.35, math.pi - 0.35, 18)
    art = over(art, glow(strokes(W, H, [(smile, 6, (0.15, 0.15))]), CYAN, radius=5, strength=0.5))
    art = GP(art, strokes(W, H, [(smile, 6, (0.15, 0.15))]), "#c9f7ff", seed=nx(), rough=0.4, streak=0.2)
    art = G(art, circles(W, H, [(246, 240, 11), (414, 240, 11)]), PINK, seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=1, feather=2)
    art = rivets(art, W, H, [(212, 112), (448, 112), (212, 280), (448, 280)], 5, nx)
    preview(art, "rb-robot", tone="#fdf3e3")
    save(art, f"{OUT}/robot.webp", max_w=440, quality=84)
    clear()


def part_drone():
    W, H = 340, 340
    rng = random.Random(81); nx = Seq(800)
    art = blank(W, H)
    # propeller
    art = GP(art, strokes(W, H, [([(170, 104), (170, 70)], 8, None)]), STEEL_D, STEEL, seed=nx(), rough=0.4, streak=0.3)
    blades = ellipses(W, H, [(118, 64, 56, 10, -4), (222, 64, 56, 10, 4)])
    art = body(art, W, H, blades, "#ef5b5b", "#f27272", "#b83a3a", "#ffc2c2", nx, 62, 278, 54, 74)
    art = rivets(art, W, H, [(170, 64)], 10, nx, col=STEEL)
    # arms
    art = tube(art, W, H, [(104, 200), (66, 226), (58, 262)], 16, nx, rings=3)
    art = tube(art, W, H, [(236, 200), (274, 226), (282, 262)], 16, nx, rings=3)
    art = claw(art, W, H, 58, 276, 16, math.pi / 2, nx)
    art = claw(art, W, H, 282, 276, 16, math.pi / 2, nx)
    # body sphere
    bm = circles(W, H, [(170, 192, 86)])
    art = body(art, W, H, bm, YELLOW, "#f9d465", YELLOW_D, "#fff4c2", nx, 84, 256, 106, 278)
    band = rect(W, H, 84, 216, 256, 230) * bm
    art = G(art, band, YELLOW_D, seed=nx(), density=0.5, edge=0.2, rough=0.6, feather=0.8)
    art = rivets(art, W, H, [(110, 223), (140, 223), (200, 223), (230, 223)], 4, nx)
    vis = ellipses(W, H, [(170, 180, 58, 40, 0)])
    art = GP(art, vis, NAVY, "#26345a", seed=nx(), rough=0.6, streak=0.4)
    art = eye(art, W, H, 170, 180, 26, nx, look=(0.15, -0.05))
    art = G(art, circles(W, H, [(116, 210, 9), (224, 210, 9)]), PINK, seed=nx(), density=0.6, edge=0.2, rough=1, feather=2)
    preview(art, "rb-drone", tone="#fdf3e3")
    save(art, f"{OUT}/drone.webp", max_w=200, quality=84)
    clear()


def part_gears():
    for name, (col, col2, deep, light), teeth, sp, seed in [("gear", (ORANGE, "#f49a5e", ORANGE_D, ORANGE_L), 12, 5, 91),
                                                            ("gear2", (TEAL, "#45bdb0", TEAL_D, TEAL_L), 9, 0, 93)]:
        W = H = 300
        nx = Seq(seed * 10)
        art = blank(W, H)
        m = gear_mask(W, H, 150, 150, 136, teeth, hole=0.2, spokes=0, depth=0.2)
        if sp:
            m = np.clip(m - circles(W, H, [(150 + math.cos(k * math.tau / sp) * 78, 150 + math.sin(k * math.tau / sp) * 78, 20) for k in range(sp)]), 0, 1)
        m = displace(m, nx(), 1.4, 12)
        art = body(art, W, H, m, col, col2, deep, light, nx, 14, 286, 14, 286)
        ringm = ring(W, H, 150, 150, 62, 12) * m
        art = G(art, ringm, deep, seed=nx(), density=0.35, edge=0.3, rough=0.6, feather=0.8)
        hub = ring(W, H, 150, 150, 44, 16)
        art = body(art, W, H, hub, STEEL, STEEL, STEEL_D, STEEL_L, nx, 106, 194, 106, 194)
        preview(art, "rb-" + name, tone="#fdf3e3")
        save(art, f"{OUT}/{name}.webp", max_w=160 if name == "gear" else 120, quality=84)
        clear()


def part_cake():
    W, H = 520, 520
    rng = random.Random(101); nx = Seq(1500)
    art = blank(W, H)
    # plate
    pm = ellipses(W, H, [(260, 470, 230, 30, 0)])
    art = body(art, W, H, pm, STEEL_L, "#eef2f6", STEEL_D, "#ffffff", nx, 30, 490, 440, 500)
    # bottom tier: teal with orange bolt stripe and yellow frosting drips
    bt = rrect(W, H, 70, 330, 450, 474, 28)
    art = body(art, W, H, bt, TEAL, "#45bdb0", TEAL_D, TEAL_L, nx, 70, 450, 330, 474)
    drip = [(70, 330)]
    for k in range(13):
        x = 70 + (k + 0.5) * 380 / 13
        drip += [(x - 12, 350), (x - 6, 362 + rng.uniform(0, 18)), (x + 6, 362 + rng.uniform(0, 18)), (x + 12, 350)]
    drip += [(450, 330), (450, 318), (70, 318)]
    dm = poly(W, H, drip, smooth=True) * rect(W, H, 60, 300, 460, 400)
    art = body(art, W, H, np.clip(dm, 0, 1), CREAM, "#fbeedb", "#d9c4a4", "#ffffff", nx, 70, 450, 318, 380)
    art = rivets(art, W, H, [(110 + k * 60, 430) for k in range(6)], 9, nx, col=YELLOW, deep=YELLOW_D)
    clear()
    # top tier: a robot head cake
    hm = rrect(W, H, 140, 176, 380, 330, 40)
    art = body(art, W, H, hm, ORANGE, "#f49a5e", ORANGE_D, ORANGE_L, nx, 140, 380, 176, 330)
    fm = rrect(W, H, 170, 204, 350, 304, 30)
    art = GP(art, fm, NAVY, "#26345a", seed=nx(), rough=0.8, streak=0.5)
    for x in (222, 298):
        art = GP(art, circles(W, H, [(x, 244, 18)]), "#e9fdff", "#bff3fb", seed=nx(), rough=0.5, streak=0.3, pad=6)
        art = GP(art, circles(W, H, [(x + 2, 246, 9)]), NAVY_D, seed=nx(), rough=0.3, streak=0.2, pad=6)
        art = GP(art, circles(W, H, [(x - 3, 240, 3.5)]), "#ffffff", seed=nx(), rough=0.2, streak=0.1, pad=6)
    sm = arc_pts(260, 262, 26, 0.4, math.pi - 0.4, 14)
    art = GP(art, strokes(W, H, [(sm, 5, (0.15, 0.15))]), "#c9f7ff", seed=nx(), rough=0.3, streak=0.2)
    for x in (140, 380):
        em = circles(W, H, [(x, 252, 20)])
        art = body(art, W, H, em, YELLOW, YELLOW, YELLOW_D, "#fff1b8", nx, x - 20, x + 20, 232, 272)
    clear()
    # candles + flames
    for k, x in enumerate((196, 236, 284, 324)):
        c = [PINK, YELLOW, TEAL_L, PINK][k]
        cm = rrect(W, H, x - 7, 120, x + 7, 180, 4)
        art = body(art, W, H, cm, c, c, mix_hex(c, "#5a3a3a", 0.35), "#ffffff", nx, x - 7, x + 7)
        stripes = [([(x - 7, y), (x + 7, y - 8)], 2.2, None) for y in range(132, 182, 12)]
        art = G(art, strokes(W, H, stripes) * cm, "#ffffff", seed=nx(), density=0.65, edge=0, rough=0.3, feather=0.4, pad=6)
        fl = shape_mask(W, H, [(x, 86), (x + 8, 104), (x + 6, 114), (x, 118), (x - 6, 114), (x - 8, 104)])
        art = over(art, glow(fl, "#ffd36b", radius=10, strength=0.5))
        art = GP(art, fl, "#ffb238", "#ff8a2a", seed=nx(), rough=0.5, streak=0.3, pad=6)
        art = GP(art, shape_mask(W, H, [(x, 98), (x + 4, 108), (x, 116), (x - 4, 108)]), "#fff3c2", seed=nx(), rough=0.3, streak=0.2, pad=6)
    # sprinkles
    spr = []
    for _ in range(40):
        x, y = rng.uniform(90, 430), rng.uniform(372, 468)
        a = rng.uniform(0, math.pi)
        spr.append(([(x, y), (x + math.cos(a) * 7, y + math.sin(a) * 7)], 3, None))
    cols = [YELLOW, PINK, "#ffffff", ORANGE_L]
    for i, c in enumerate(cols):
        art = GP(art, strokes(W, H, spr[i::4]) * bt, c, seed=nx(), rough=0.3, streak=0.2)
    preview(art, "rb-cake", tone="#fdf3e3")
    save(art, f"{OUT}/cake.webp", max_w=320, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
