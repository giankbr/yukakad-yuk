"""Gathering Kantor — a company family-gathering / outbound day by a pine-forest lake in Lembang, in matte gouache:
the panorama (painted morning sky, misty volcano ridge, pine rows, lake with reflections, meadow, a striped marquee,
dome tents with pennants, a tug-of-war rope and estafet cones), a pennant bunting string, one dome tent, the rope
divider, a charcoal grill with corn and satay, an estafet cone and a small pine pair.
Run: python3 -I gathering-kantor.py [part ...]   parts: scene flags tent rope bbq cone pines
Assets -> public/themes/art/gathering-kantor/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i4_lib import *  # noqa

OUT = outdir("gathering-kantor")
PARTS = sys.argv[1:] or ["scene", "flags", "tent", "rope", "bbq", "cone", "pines"]
SKY, MIST, RIDGE = "#bfe3ef", "#a8c6d3", "#7f9fb2"
PINE, PINE_D, PINE_L = "#2f6b4f", "#1f4a37", "#4c8a63"
GRASS, GRASS_L, GRASS_D = "#8cc265", "#a9d47a", "#5f9a48"
LAKE, LAKE_L = "#5aa6c4", "#9fd3e3"
ORANGE, YELLOW, TEAL, RED, WHITE, INK = "#f28c38", "#f6c945", "#2bb3a3", "#e2483d", "#fff8ee", "#22312b"
WOOD = "#8a5a35"


def pine(art, W, H, x, base, h, nx, rng, col=PINE, dark=PINE_D, light=PINE_L, tiers=4):
    w = h * 0.42
    trunk = shapes(W, H, [[(x - h * 0.025, base), (x + h * 0.025, base), (x + h * 0.02, base - h * 0.2), (x - h * 0.02, base - h * 0.2)]], smooth=False)
    art = GP(art, trunk, WOOD, "#6b4226", seed=nx(), rough=0.8)
    for t in range(tiers):
        k = t / tiers
        ty = base - h * 0.12 - k * h * 0.78
        tw = w * (1 - k * 0.72)
        top = ty - h * 0.36
        pts = [(x - tw, ty), (x - tw * 0.6, ty - h * 0.04), (x, top), (x + tw * 0.6, ty - h * 0.05), (x + tw, ty)]
        jag = [(x - tw + i * tw / 5, ty + (3 if i % 2 else -1) * h * 0.012) for i in range(11)]
        m = shapes(W, H, [pts + list(reversed(jag))], smooth=False)
        art = GP(art, m, col, dark, seed=nx(), rough=1.4, streak=0.6)
        lit = shapes(W, H, [[(x + tw * 0.08, top + h * 0.06), (x + tw * 0.85, ty - h * 0.01), (x + tw * 0.2, ty - h * 0.02)]], smooth=False)
        art = GP(art, lit * m, light, seed=nx(), rough=1.0, streak=0.4, density=0.7)
    return art


def dome_tent(art, W, H, cx, by, w, col, col2, nx, flag=RED, door=True):
    h = w * 0.62
    body = [(cx + math.cos(a) * w / 2, by - math.sin(a) * h) for a in np.linspace(0, math.pi, 40)]
    m = shapes(W, H, [body + [(cx - w / 2, by)]], smooth=False)
    art = OV(art, ellipses(W, H, [(cx + w * 0.08, by + 3, w * 0.62, w * 0.08, 0)]), lambda mm: col_arr(mm, "#2c4a2a", gaussian_filter(mm, 4) * 0.35), pad=20)
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.6)
    # shade the left half (light from the right)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = shade(art, m, 1 - 0.18 * np.clip((cx - xx) / (w / 2), 0, 1))
    # seams / poles
    for k in (-0.5, 0.0, 0.5):
        pole = [(cx + math.cos(a) * w / 2 * (1 - abs(k) * 0.2) + k * w * 0.18 * math.sin(a), by - math.sin(a) * h * (1 - abs(k) * 0.1)) for a in np.linspace(0, math.pi, 30)]
        art = OV(art, strokes(W, H, [(pole, max(1.2, w * 0.012), None)]) * m, lambda mm: col_arr(mm, mix(col2, INK, 0.35), mm * 0.6), pad=6)
    if door:
        dm = shapes(W, H, [[(cx - w * 0.14, by), (cx, by - h * 0.62), (cx + w * 0.14, by)]], smooth=False)
        art = GP(art, dm, mix(col2, INK, 0.45), seed=nx(), rough=0.8)
        flap = shapes(W, H, [[(cx, by - h * 0.62), (cx + w * 0.14, by), (cx + w * 0.22, by - h * 0.06)]], smooth=False)
        art = GP(art, flap, mix(col, WHITE, 0.2), seed=nx(), rough=0.8)
    # pennant on a little pole at the top
    px, py = cx + w * 0.04, by - h
    art = OV(art, strokes(W, H, [([(px, py), (px, py - h * 0.5)], max(1.4, w * 0.014), None)]), lambda mm: col_arr(mm, INK, mm), pad=6)
    fm = shapes(W, H, [[(px, py - h * 0.5), (px + w * 0.22, py - h * 0.42), (px, py - h * 0.32)]], smooth=False)
    art = GP(art, fm, flag, seed=nx(), rough=0.8)
    # guy lines
    gl = strokes(W, H, [([(cx - w * 0.3, by - h * 0.7), (cx - w * 0.68, by + 2)], 1.0, None), ([(cx + w * 0.3, by - h * 0.7), (cx + w * 0.68, by + 2)], 1.0, None)])
    art = OV(art, gl, lambda mm: col_arr(mm, "#f4ecd8", mm * 0.8), pad=4)
    return art


def marquee(art, W, H, cx, by, w, nx):
    h = w * 0.5
    x0, x1 = cx - w / 2, cx + w / 2
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = OV(art, ellipses(W, H, [(cx + 12, by + 4, w * 0.62, 12, 0)]), lambda mm: col_arr(mm, "#2c4a2a", gaussian_filter(mm, 5) * 0.35), pad=20)
    wall = shapes(W, H, [[(x0, by), (x1, by), (x1, by - h * 0.52), (x0, by - h * 0.52)]], smooth=False)
    art = GP(art, wall, WHITE, "#efe6d4", seed=nx(), rough=1.0)
    st = stripes_f(W, H, 0.0, w / 7, 0.5)
    art = GP(art, wall * st, "#3d8fbf", "#357fae", seed=nx(), rough=0.8, density=0.92)
    # open front: dark interior with a table
    inner = shapes(W, H, [[(cx - w * 0.3, by), (cx + w * 0.3, by), (cx + w * 0.3, by - h * 0.42), (cx - w * 0.3, by - h * 0.42)]], smooth=False)
    art = GP(art, inner, "#5b3b2a", "#3e2a1e", seed=nx(), rough=0.8)
    tbl = shapes(W, H, [[(cx - w * 0.24, by - h * 0.14), (cx + w * 0.24, by - h * 0.14), (cx + w * 0.24, by - h * 0.06), (cx - w * 0.24, by - h * 0.06)]], smooth=False)
    art = GP(art, tbl, YELLOW, seed=nx(), rough=0.6)
    # roof
    roof = shapes(W, H, [[(x0 - w * 0.06, by - h * 0.52), (cx, by - h * 1.05), (x1 + w * 0.06, by - h * 0.52)]], smooth=False)
    art = GP(art, roof, WHITE, "#efe6d4", seed=nx(), rough=1.0)
    # roof stripes radiate from the peak
    ang = np.arctan2(yy - (by - h * 1.05), xx - cx)
    rs = (np.sin(ang * 22) > 0).astype(np.float32)
    art = GP(art, roof * rs, "#3d8fbf", "#357fae", seed=nx(), rough=0.8)
    art = shade(art, roof, 1 - 0.14 * np.clip((cx - xx) / (w / 2), 0, 1))
    # scalloped valance
    val = []
    n = 8
    for i in range(n):
        a = x0 - w * 0.06 + i * (w * 1.12) / n
        b = a + w * 1.12 / n
        val.append([(a, by - h * 0.53), (b, by - h * 0.53)] + [((a + b) / 2 + math.cos(t) * (b - a) / 2, by - h * 0.53 + math.sin(t) * h * 0.09) for t in np.linspace(0, math.pi, 12)])
    for i, v in enumerate(val):
        art = GP(art, shapes(W, H, [v], smooth=False), RED if i % 2 else YELLOW, seed=nx(), rough=0.8)
    art = OV(art, strokes(W, H, [([(cx, by - h * 1.05), (cx, by - h * 1.3)], 2.4, None)]), lambda mm: col_arr(mm, INK, mm), pad=6)
    art = GP(art, shapes(W, H, [[(cx, by - h * 1.3), (cx + w * 0.16, by - h * 1.22), (cx, by - h * 1.14)]], smooth=False), TEAL, seed=nx(), rough=0.8)
    return art


def stripes_f(W, H, ang, sp, duty):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx * math.cos(ang) + yy * math.sin(ang)) / sp
    return ((u % 1) < duty).astype(np.float32)


def dots_f(W, H, sp, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fx = (xx % sp) - sp / 2; fy = ((yy + (xx // sp) % 2 * sp / 2) % sp) - sp / 2
    return np.clip(r + 0.5 - np.hypot(fx, fy), 0, 1)


def rope(art, W, H, pts, width, nx, ribbon=None):
    m = strokes(W, H, [(pts, width, None)])
    art = OV(art, np.roll(np.roll(m, 4, 0), 2, 1), lambda mm: col_arr(mm, "#2c4a2a", gaussian_filter(mm, 2.5) * 0.35), pad=10)
    art = GP(art, m, "#d8b47a", "#c49a5e", seed=nx(), rough=0.6, streak=0.3)
    # twist: diagonal darker bands following the path
    u = u_path(W, H, pts, 1.1)
    tw = (np.sin(u / (width * 0.42) * math.pi) * 0.5 + 0.5) ** 2
    art = shade(art, m, 1 - 0.3 * tw)
    if ribbon:
        rx, ry = ribbon
        rm = shapes(W, H, [[(rx - width * 0.5, ry - width * 0.8), (rx + width * 0.5, ry - width * 0.8), (rx + width * 0.9, ry + width * 2.4), (rx, ry + width * 1.6), (rx - width * 0.9, ry + width * 2.4)]], smooth=False)
        art = GP(art, rm, RED, "#c23a30", seed=nx(), rough=0.6)
    return art


def cone(art, W, H, cx, by, h, nx):
    w = h * 0.62
    base = shapes(W, H, [[(cx - w * 0.62, by), (cx + w * 0.62, by), (cx + w * 0.62, by - h * 0.08), (cx - w * 0.62, by - h * 0.08)]], smooth=False)
    art = OV(art, ellipses(W, H, [(cx + 4, by + 2, w * 0.8, h * 0.07, 0)]), lambda mm: col_arr(mm, "#2c4a2a", gaussian_filter(mm, 3) * 0.35), pad=10)
    art = GP(art, base, "#e0702a", seed=nx(), rough=0.6)
    body = shapes(W, H, [[(cx - w * 0.45, by - h * 0.08), (cx + w * 0.45, by - h * 0.08), (cx + w * 0.08, by - h), (cx - w * 0.08, by - h)]], smooth=False)
    art = GP(art, body, ORANGE, "#e87a2c", seed=nx(), rough=0.6)
    band = stripes_f(W, H, math.pi / 2, h, 0.16)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    bm = body * ((yy > by - h * 0.62) & (yy < by - h * 0.46)).astype(np.float32)
    art = GP(art, bm, WHITE, seed=nx(), rough=0.5)
    xx = np.mgrid[0:H, 0:W][1].astype(np.float32)
    art = shade(art, body, 1 - 0.2 * np.clip((cx - xx) / (w * 0.45), 0, 1))
    return art


if "scene" in PARTS:
    W, H = 780, 620
    nx = Seq(100); rng = random.Random(5)
    art = painted_sky(W, H, [(0, "#9fd3ea"), (0.3, "#cdebf2"), (0.45, "#eaf5ef"), (1, "#eaf5ef")], seed=3)
    # soft clouds
    for x, y, r in [(150, 70, 60), (210, 60, 46), (560, 110, 54), (620, 100, 40), (380, 40, 30)]:
        art = OV(art, disc(W, H, x, y, r), lambda mm: col_arr(mm, "#ffffff", gaussian_filter(mm, 10) * 0.75), pad=40)
    # far volcano ridge (flat-topped, like an upturned boat) and a nearer hill line
    ridge = [(x, 228 - 60 * math.exp(-((x - 470) / 210) ** 2) - (14 if 400 < x < 560 else 0) * math.exp(-((x - 480) / 70) ** 4) + 6 * math.sin(x / 33)) for x in range(-10, W + 11, 6)]
    art = GP(art, shape_mask(W, H, ridge + [(W + 10, 300), (-10, 300)], smooth=False), MIST, "#b4cfda", seed=nx(), rough=2, streak=0.5)
    hill = [(x, 262 - 26 * math.sin(x / 140 + 1) - 8 * math.sin(x / 47)) for x in range(-10, W + 11, 6)]
    art = GP(art, shape_mask(W, H, hill + [(W + 10, 320), (-10, 320)], smooth=False), RIDGE, "#88a7b7", seed=nx(), rough=2, streak=0.5)
    # mist band
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    mist = np.exp(-((yy - 262) / 18) ** 2) * (0.6 + 0.4 * fbm(W, H, 9, 120, 3))
    art = OV(art, mist, lambda mm: col_arr(mm, "#eef7f6", mm * 0.65))
    # far pine row on the far shore
    for i in range(46):
        x = -10 + i * 18 + rng.uniform(-5, 5)
        art = pine(art, W, H, x, 306, rng.uniform(42, 64), nx, rng, col="#3f7a63", dark="#2e5f4d", light="#5c947a", tiers=3)
    clear()
    # lake
    lake = shapes(W, H, [[(-10, 304), (W + 10, 304), (W + 10, 380), (-10, 380)]], smooth=False)
    art = GP(art, lake, LAKE, "#4b97b6", seed=nx(), rough=1.2, streak=1.0)
    refl = np.exp(-((yy - 316) / 10) ** 2) * (0.5 + 0.5 * np.sin(xx / 9) ** 2)
    art = OV(art, refl * lake, lambda mm: col_arr(mm, "#2e5f4d", mm * 0.45))
    rip = []
    for k in range(26):
        y = rng.uniform(322, 374); x = rng.uniform(0, W); L = rng.uniform(16, 48)
        rip.append(([(x, y), (x + L, y + rng.uniform(-0.6, 0.6))], rng.uniform(1.2, 2.2), (0.3, 0.3)))
    art = OV(art, strokes(W, H, rip), lambda mm: col_arr(mm, LAKE_L, mm * 0.85), pad=4)
    # meadow
    mead = [(x, 372 + 6 * math.sin(x / 70) + 4 * math.sin(x / 23)) for x in range(-10, W + 11, 6)]
    gm = shape_mask(W, H, mead + [(W + 10, H + 10), (-10, H + 10)], smooth=False)
    art = GP(art, gm, GRASS, "#7fb85a", seed=nx(), rough=2, streak=0.7)
    art = OV(art, gm * np.clip((yy - 380) / 260, 0, 1), lambda mm: col_arr(mm, GRASS_D, mm * 0.5))
    # grass tufts
    tufts = []
    for k in range(120):
        x = rng.uniform(0, W); y = rng.uniform(395, H)
        for d in (-1, 0, 1):
            tufts.append(([(x + d * 2, y), (x + d * 4 + rng.uniform(-1, 1), y - rng.uniform(5, 10))], 1.6, (0.0, 0.6)))
    art = OV(art, strokes(W, H, tufts), lambda mm: col_arr(mm, GRASS_L, mm * 0.8), pad=4)
    clear()
    # near pines at the edges
    for x, h in [(-6, 300), (46, 240), (722, 290), (770, 340), (680, 220)]:
        art = pine(art, W, H, x, 420 + rng.uniform(-6, 6), h, nx, rng, tiers=5)
    clear()
    # tents and marquee
    art = marquee(art, W, H, 330, 446, 230, nx)
    art = dome_tent(art, W, H, 575, 458, 118, ORANGE, "#d9701f", nx, flag=TEAL)
    art = dome_tent(art, W, H, 160, 470, 104, YELLOW, "#e0ae2a", nx, flag=RED)
    art = dome_tent(art, W, H, 660, 500, 84, TEAL, "#21958a", nx, flag=YELLOW)
    clear()
    # tug-of-war rope across the foreground and estafet cones
    rp = curve([(60, 560), (200, 548), (330, 566), (470, 552), (560, 562)], 60)
    art = rope(art, W, H, rp, 11, nx, ribbon=(318, 562))
    for x, y in [(612, 580), (690, 594), (752, 572)]:
        art = cone(art, W, H, x, y, 40, nx)
    save(art, f"{OUT}/scene.webp", quality=80)
    prev(art, "gk-scene")
    clear()

if "flags" in PARTS:
    W, H = 800, 130
    nx = Seq(200)
    art = blank(W, H)
    line = [(x, 20 + 34 * math.sin(math.pi * x / W)) for x in range(0, W + 1, 4)]
    art = OV(art, strokes(W, H, [(line, 2.2, None)]), lambda mm: col_arr(mm, INK, mm), pad=4)
    cols = [RED, YELLOW, TEAL, ORANGE, "#3d8fbf", WHITE]
    for i in range(16):
        x = 18 + i * 49
        y = 20 + 34 * math.sin(math.pi * x / W)
        a = math.atan(34 * math.pi / W * math.cos(math.pi * x / W))
        ca, sa = math.cos(a), math.sin(a)
        pts = [(x - 17 * ca, y - 17 * sa), (x + 17 * ca, y + 17 * sa), (x - sa * 44, y + ca * 44)]
        m = shapes(W, H, [pts], smooth=False)
        art = OV(art, np.roll(m, 3, 0), lambda mm: col_arr(mm, "#000000", gaussian_filter(mm, 2) * 0.18), pad=6)
        art = GP(art, m, cols[i % len(cols)], mix(cols[i % len(cols)], INK, 0.12), seed=nx(), rough=1.0, streak=0.6)
    save(art, f"{OUT}/flags.webp", quality=82)
    prev(art, "gk-flags", "#eaf5ef")

if "tent" in PARTS:
    W, H = 300, 230
    nx = Seq(300)
    art = blank(W, H)
    grass = ellipses(W, H, [(150, 206, 132, 16, 0)])
    art = GP(art, grass, GRASS, GRASS_D, seed=nx(), rough=1.5)
    art = dome_tent(art, W, H, 150, 204, 200, ORANGE, "#d9701f", nx, flag=TEAL)
    save(art, f"{OUT}/tent.webp", quality=82)
    prev(art, "gk-tent", "#eaf5ef")

if "rope" in PARTS:
    W, H = 400, 70
    nx = Seq(400)
    art = blank(W, H)
    rp = curve([(10, 30), (110, 24), (200, 32), (290, 24), (390, 30)], 60)
    art = rope(art, W, H, rp, 10, nx, ribbon=(200, 31))
    save(art, f"{OUT}/rope.webp", quality=82)
    prev(art, "gk-rope", "#fff8ee")

if "bbq" in PARTS:
    W, H = 320, 320
    nx = Seq(500); rng = random.Random(9)
    art = blank(W, H)
    # smoke puffs
    for k in range(6):
        x = 150 + k * 9 + 14 * math.sin(k); y = 120 - k * 20
        art = OV(art, disc(W, H, x, y, 14 + k * 3), lambda mm: col_arr(mm, "#e9ecea", gaussian_filter(mm, 4) * (0.75 - k * 0.09)), pad=20)
    # legs
    legs = strokes(W, H, [([(100, 210), (80, 300)], 7, None), ([(220, 210), (240, 300)], 7, None), ([(160, 214), (160, 300)], 7, None)])
    art = GP(art, legs, "#3a3f3c", seed=nx(), rough=0.6)
    # grill bowl
    bowl = shapes(W, H, [[(70, 170)] + [(160 + math.cos(a) * 92, 170 + math.sin(a) * 60) for a in np.linspace(0, math.pi, 30)][::-1] + [(250, 170)]], smooth=False)
    art = GP(art, bowl, "#2f3432", "#444a47", seed=nx(), rough=0.8, streak=0.5)
    art = OV(art, ellipses(W, H, [(130, 196, 34, 10, -20)]), lambda mm: col_arr(mm, "#8a918d", gaussian_filter(mm, 3) * 0.45), pad=14)
    # embers glow on the rim
    rim = ellipses(W, H, [(160, 170, 92, 14, 0)])
    art = GP(art, rim, "#e2483d", "#f28c38", seed=nx(), rough=0.8)
    art = OV(art, rim, lambda mm: col_arr(mm, "#ffd27a", gaussian_filter(mm, 6) * 0.4), pad=20)
    # grate bars
    bars = strokes(W, H, [([(80 + i * 14, 164), (82 + i * 14, 176)], 2, None) for i in range(12)])
    art = OV(art, bars, lambda mm: col_arr(mm, "#2a2d2c", mm * 0.9), pad=4)
    # corn cobs and satay sticks on top
    for x, a in [(118, -0.12), (176, 0.1)]:
        cob = shapes(W, H, [ellipse_pts(x, 158, 30, 11, 16, a)])
        art = GP(art, cob, "#f6c945", "#e9b234", seed=nx(), rough=0.6)
        kern = dots_f(W, H, 6, 1.8) * cob
        art = OV(art, kern, lambda mm: col_arr(mm, "#d99a22", mm * 0.6), pad=4)
        sc = strokes(W, H, [([(x - 24, 152), (x + 10, 166)], 3.5, None), ([(x - 6, 150), (x + 20, 164)], 3, None)]) * cob
        art = OV(art, sc, lambda mm: col_arr(mm, "#7a4a1e", mm * 0.75), pad=4)
    for k in range(3):
        y = 150 + k * 6
        stick = strokes(W, H, [([(196, y - 14), (296, y - 28)], 2.2, None)])
        art = GP(art, stick, "#c9a06a", seed=nx(), rough=0.4)
        for j in range(4):
            mx = 214 + j * 14; my = y - 16.5 - j * 1.96
            art = GP(art, disc(W, H, mx, my, 6), "#8b3f22", "#6d2f19", seed=nx(), rough=0.5)
    save(art, f"{OUT}/bbq.webp", quality=82)
    prev(art, "gk-bbq", "#fff8ee")
    clear()

if "cone" in PARTS:
    W, H = 100, 110
    nx = Seq(600)
    art = cone(blank(W, H), W, H, 50, 100, 86, nx)
    save(art, f"{OUT}/cone.webp", quality=84)
    prev(art, "gk-cone", "#fff8ee")

if "pines" in PARTS:
    W, H = 220, 260
    nx = Seq(700); rng = random.Random(3)
    art = blank(W, H)
    art = pine(art, W, H, 80, 250, 230, nx, rng, tiers=5)
    art = pine(art, W, H, 160, 254, 160, nx, rng, col="#3f7a63", dark="#2e5f4d", light="#5c947a", tiers=4)
    save(art, f"{OUT}/pines.webp", quality=82)
    prev(art, "gk-pines", "#fff8ee")
