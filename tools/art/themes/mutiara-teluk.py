"""Mutiara Teluk — Gulf pearl-diving heritage at golden dusk: painted dusk sea with coral-stone wind-tower town on the
horizon (architecture only, no figures), a wooden dhow with lateen sail, an open oyster with its pearl, a pearl strand
divider and single pearls. Gouache + watercolour glazes.
Run: python3 -I mutiara-teluk.py [part ...]  parts: dusk dhow oyster barjeel pearls pearl
Assets -> public/themes/art/mutiara-teluk/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m3_lib import *

OUT = outdir("mutiara-teluk")
PARTS = sys.argv[1:] or ["dusk", "dhow", "oyster", "barjeel", "pearls", "pearl"]
NAVY, NAVY_D, TEAL = "#14304a", "#0b1d30", "#1f5f6b"
GOLD, GOLD_L, AMBER = "#e2a64b", "#f6d79a", "#d98b3c"
STONE, STONE_S, STONE_D = "#e8d3ae", "#c9ab80", "#9c7b54"
TEAK, TEAK_D = "#7a4a28", "#4a2a16"
PEARL = "#f5efe4"


def pearl_art(W, H, cx, cy, r, nx, warm=0.0):
    """Glossy pearl: soft body shading, pink/green orient, crisp highlight, rim light."""
    art = blank(W, H)
    body = circles(W, H, [(cx, cy, r)])
    art = GP(art, body, PEARL, "#efe5d6", seed=nx(), rough=0.25, streak=0.2, pad=4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx + r * 0.35) / r) ** 2 + ((yy - cy + r * 0.4) / r) ** 2)
    shade = body * np.clip((d - 0.55) / 0.9, 0, 1)
    art = G(art, shade, "#b9a9a4", "#a89fb0", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.5, feather=1.0, gran=0.05)
    orient = body * np.clip(1 - np.abs(d - 0.95) / 0.3, 0, 1)
    art = G(art, orient, "#f2c6c8", "#cfe3d6", seed=nx(), density=0.45, edge=0, bloom=0.2, rough=0.6, feather=1.4, gran=0.05)
    if warm:
        art = G(art, body * np.clip((xx - cx) / r, 0, 1), "#f3c07c", seed=nx(), density=0.35 * warm, edge=0, bloom=0, rough=0.5)
    hi = ellipses(W, H, [(cx - r * 0.34, cy - r * 0.38, r * 0.26, r * 0.16, -35)])
    art = over(art, glow(hi, "#ffffff", radius=max(1, r * 0.08), strength=0.9))
    art = over(art, glow(ellipses(W, H, [(cx - r * 0.36, cy - r * 0.4, r * 0.1, r * 0.06, -35)]), "#ffffff", radius=0.8, strength=1.6))
    return art


if "dusk" in PARTS:
    W, H = 640, 1120
    nx = Seq(41000)
    rng = random.Random(21)
    HZ = 700
    art = painted_sky(W, H, [(0, "#0f2440"), (0.18, "#1f3558"), (0.34, "#5b4b72"), (0.46, "#b0697a"), (0.56, "#e79a68"), (0.615, "#f6c77c"), (0.625, "#f8d590"), (1, "#f8d590")], seed=nx(), streak=0.4)
    # thin dusk clouds
    cl = ellipses(W, H, [(rng.uniform(-60, W + 60), rng.uniform(380, 590), rng.uniform(70, 170), rng.uniform(5, 11), rng.uniform(-2, 2)) for _ in range(14)])
    art = G(art, cl, "#f0a77e", "#c86f78", seed=nx(), density=0.5, edge=0.35, bloom=0.4, rough=10, feather=4)
    cl2 = ellipses(W, H, [(rng.uniform(-60, W + 60), rng.uniform(250, 380), rng.uniform(60, 150), rng.uniform(4, 9), 0) for _ in range(8)])
    art = G(art, cl2, "#8a5a7c", seed=nx(), density=0.4, edge=0.25, bloom=0.3, rough=8, feather=4)
    # stars at the very top
    st = circles(W, H, [(rng.uniform(0, W), rng.uniform(10, 260), rng.uniform(0.7, 1.6)) for _ in range(46)])
    art = over(art, glow(st, "#fff6dc", radius=0.7, strength=1.2))
    # low sun on the horizon
    sx, sy = 420, HZ - 18
    sun = circles(W, H, [(sx, sy, 54)])
    art = over(art, glow(sun, "#ffd98e", radius=70, strength=0.5))
    art = GP(art, sun, "#ffe8ad", "#ffd88a", seed=nx(), rough=1.2, pad=8)
    # coral-stone town on the far shore (left) and a low headland (right), silhouetted warm
    town = []
    x = -10
    while x < 300:
        w = rng.uniform(26, 50)
        h = rng.uniform(16, 34)
        town.append([(x, HZ + 2), (x, HZ - h), (x + w, HZ - h), (x + w, HZ + 2)])
        x += w - 2
    towers = []
    for tx, th in [(40, 70), (128, 84), (210, 64), (268, 58)]:
        towers.append([(tx - 9, HZ), (tx - 9, HZ - th), (tx + 9, HZ - th), (tx + 9, HZ)])
    tm = shapes(W, H, town + towers, smooth=False)
    art = GP(art, tm, "#9a6a62", "#7e5258", seed=nx(), rough=0.6, pad=6)
    slots = rects(W, H, [(tx - 6 + k * 4.2, HZ - th + 6, tx - 4 + k * 4.2, HZ - th + 26) for tx, th in [(40, 70), (128, 84), (210, 64), (268, 58)] for k in range(3)])
    art = GP(art, slots, "#5a3644", seed=nx(), rough=0.2, pad=4)
    lit = rects(W, H, [(rng.uniform(0, 290), HZ - rng.uniform(8, 20), 0, 0) for _ in range(0)])
    wins = rects(W, H, [(x0, HZ - y0, x0 + 4, HZ - y0 + 5) for x0, y0 in [(rng.uniform(4, 290), rng.uniform(8, 22)) for _ in range(16)]])
    art = GP(art, wins * tm, "#ffcf7a", seed=nx(), rough=0.2, pad=4)
    head = shapes(W, H, [[(470, HZ + 2), (520, HZ - 10), (580, HZ - 16), (W + 20, HZ - 12), (W + 20, HZ + 2)]])
    art = GP(art, head, "#8a5c60", seed=nx(), rough=1.5, pad=6)
    palms = np.zeros((H, W), np.float32)
    for px, ph, ln in [(552, 54, 0.1), (596, 66, -0.08), (624, 46, 0.12)]:
        palms = np.maximum(palms, jw.palm(W, H, px, HZ - 10, ph, rng, ln))
    art = GP(art, palms, "#6e4652", seed=nx(), rough=0.8, pad=6)
    # sea
    sea = painted_sky(W, H, [(0, "#f2b276"), (HZ / H, "#f2b276"), (HZ / H + 0.04, "#c9806a"), (0.75, "#3e4f6c"), (0.88, NAVY), (1, NAVY_D)], seed=nx(), streak=1.4)
    water = rect(W, H, -10, HZ, W + 10, H + 10)
    art = art * (1 - water[..., None]) + sea * water[..., None]
    art = reflect(art, HZ, strength=0.3, wave=4.0, fade=2.2)
    art[HZ:] = gaussian_filter(art[HZ:], (2.0, 1.0, 0))
    # sun path: broken gold strokes narrowing towards the horizon
    path = []
    for _ in range(90):
        y = rng.uniform(HZ + 4, HZ + 300)
        spread = 26 + (y - HZ) * 0.42
        x0 = sx + rng.gauss(0, spread * 0.5)
        path.append(([(x0, y), (x0 + rng.uniform(10, 28 + (y - HZ) * 0.1), y)], rng.uniform(2.2, 4.4), (0.35, 0.35)))
    art = over(art, glow(strokes(W, H, path), "#ffdc9a", radius=0.7, strength=0.75))
    art = over(art, glow(ripples(W, H, rng, HZ + 20, H, 120, 20, 80, 1.8, 3.2), "#7186a3", radius=0.8, strength=0.45))
    art = over(art, glow(ripples(W, H, rng, HZ + 120, H, 70, 30, 90, 2, 3.6), "#0b1c30", radius=0.8, strength=0.5))
    art = add_grain(art, 3, 0.035)
    preview(art, "mt-dusk")
    save_rgb(art, f"{OUT}/dusk.webp", size=(480, 840), quality=74)
    clear()

if "dhow" in PARTS:
    # boom/sambuk-style dhow facing left: curved teak hull, raked bow, high square stern, lateen sail lit by the sun
    W, H = 520, 460
    nx = Seq(42000)
    art = blank(W, H)
    mast = strokes(W, H, [([(262, 360), (244, 70)], 6, None)])
    art = GP(art, mast, TEAK, TEAK_D, seed=nx(), rough=0.5, pad=4)
    sail = shapes(W, H, [[(50, 140)] + curve([(50, 140), (250, 66), (460, 18)], 16)[1:] + curve([(460, 18), (400, 190), (312, 342)], 16)[1:] + curve([(312, 342), (190, 336), (86, 312)], 10)[1:]], smooth=False)
    art = GP(art, sail, "#f6e2bd", "#efd2a2", seed=nx(), rough=1.0, streak=0.3, pad=8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, sail * np.clip((260 - xx) / 220, 0, 1) * np.clip((yy - 60) / 260, 0, 1), "#c98a5c", seed=nx(), density=0.45, edge=0.25, bloom=0.4, rough=4, feather=3)
    art = G(art, sail * np.clip((xx - 260) / 180, 0, 1), "#ffd48a", seed=nx(), density=0.4, edge=0, bloom=0.3, rough=3, feather=3)
    seams = strokes(W, H, [(curve([(50 + k * 46, 140 - k * 14), (150 + k * 24, 240), (100 + k * 26, 330)], 10), 1.2, None) for k in range(1, 9)])
    art = G(art, seams * sail, "#c79a68", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5)
    yard = strokes(W, H, [(curve([(40, 136), (240, 62), (470, 12)], 20), 5.5, (0.05, 0.2))])
    art = GP(art, yard, TEAK, TEAK_D, seed=nx(), rough=0.5, pad=4)
    rig = strokes(W, H, [([(462, 22), (488, 300)], 1.2, None), ([(130, 334), (110, 362)], 1.2, None), ([(282, 346), (300, 362)], 1.2, None)])
    art = G(art, rig, "#5a3a26", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3, feather=0.3)
    hull = shapes(W, H, [[(20, 330), (60, 352), (110, 362), (440, 362), (488, 330), (500, 300), (470, 334), (40, 346)]])
    hullb = shapes(W, H, [[(24, 338), (70, 372), (130, 400), (400, 404), (470, 384), (500, 300), (494, 360), (40, 350)]])
    hull = np.maximum(hull, shapes(W, H, [[(14, 322), (60, 350), (140, 368), (420, 368), (476, 352), (506, 292), (514, 288), (500, 372), (452, 404), (150, 406), (80, 388)]]))
    art = GP(art, hull, "#8c5a32", "#6e4122", seed=nx(), rough=0.8, streak=1.2, pad=6)
    planks = strokes(W, H, [(curve([(30 + k * 6, 340 + k * 10), (250, 372 + k * 9), (480, 350 + k * 8)], 18), 1.1, None) for k in range(5)])
    art = G(art, planks * hull, TEAK_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4)
    art = G(art, v_ramp(hull, 360, 410), "#2f1a10", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6)
    rail = strokes(W, H, [(curve([(14, 322), (140, 352), (400, 352), (512, 286)], 20), 5, None)])
    art = GP(art, rail, "#c98f4e", "#a8703a", seed=nx(), rough=0.3, pad=4)
    stern = shapes(W, H, [[(440, 352), (446, 318), (500, 296), (506, 330)]], smooth=False)
    art = GP(art, stern, "#a06a3a", seed=nx(), rough=0.4, pad=4)
    rope = strokes(W, H, [(curve([(470, 300), (476, 330), (468, 352)], 8), 1.8, None)])
    art = G(art, rope, "#e9cf9a", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    wave = strokes(W, H, [(curve([(0, 404), (40, 396), (100, 410), (200, 414)], 16), 4.2, (0.2, 0.6)), (curve([(330, 414), (420, 406), (520, 414)], 12), 3.6, (0.2, 0.6))])
    art = GP(art, wave, "#f9dba6", seed=nx(), rough=0.8, pad=6)
    preview(art, "mt-dhow", bg="#c9806a")
    save(art, f"{OUT}/dhow.webp", max_w=240, quality=84)
    clear()

if "oyster" in PARTS:
    W, H = 420, 340
    nx = Seq(43000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    # upper valve, opened back (behind)
    lid = shapes(W, H, [[(110, 190), (80, 120), (110, 60), (180, 26), (260, 24), (330, 52), (356, 110), (320, 188)]])
    art = GP(art, lid, "#7c6f62", "#5e544c", seed=nx(), rough=2.4, streak=1.0, pad=8)
    ridges = strokes(W, H, [(curve([(110 + k * 22, 190), (140 + k * 18, 120), (110 + k * 28, 40)], 12), 2, None) for k in range(10)])
    art = G(art, ridges * lid, "#3f3830", seed=nx(), density=0.5, edge=0, bloom=0, rough=1.5)
    inner = shapes(W, H, [[(132, 188), (112, 128), (138, 76), (192, 50), (256, 50), (310, 74), (330, 120), (306, 186)]])
    art = GP(art, inner, "#e9e2d6", "#d7cfc6", seed=nx(), rough=1.2, pad=6)
    nac = fbm(W, H, nx(), 40, 3)
    art = G(art, inner * np.clip(nac - 0.35, 0, 1) * 1.6, "#cfe0dc", "#e8c9d0", seed=nx(), density=0.55, edge=0.2, bloom=0.5, rough=3)
    art = G(art, inner * np.clip(0.6 - nac, 0, 1) * 1.6, "#d9cfe6", seed=nx(), density=0.45, edge=0.1, bloom=0.4, rough=3)
    art = G(art, v_ramp(inner, 120, 196), "#8f8a8c", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # lower valve (front), cupped, rough exterior rim + nacre bowl
    low = shapes(W, H, [[(40, 196), (110, 180), (210, 176), (320, 180), (392, 196), (370, 262), (300, 312), (210, 326), (120, 310), (60, 264)]])
    art = GP(art, low, "#6f665b", "#544c44", seed=nx(), rough=2.8, streak=1.0, pad=8)
    lr = strokes(W, H, [(curve([(60 + k * 30, 200), (90 + k * 26, 260), (210, 324)], 12), 2.2, None) for k in range(11)])
    art = G(art, lr * low, "#3a332c", seed=nx(), density=0.5, edge=0, bloom=0, rough=1.5)
    bowl = shapes(W, H, [[(70, 200), (130, 188), (210, 186), (300, 188), (362, 200), (330, 240), (270, 262), (210, 268), (150, 262), (92, 240)]])
    art = GP(art, bowl, "#efe8de", "#dcd3cb", seed=nx(), rough=1.2, pad=6)
    art = G(art, bowl * np.clip(nac - 0.4, 0, 1) * 1.8, "#c8e0dc", "#efc7cf", seed=nx(), density=0.6, edge=0.2, bloom=0.5, rough=3)
    art = G(art, bowl * np.clip((yy - 186) / 80, 0, 1) ** 2, "#9a93a0", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = over(art, pearl_art(W, H, 212, 212, 38, nx, warm=0.6))
    # shadow of pearl in the bowl
    preview(art, "mt-oyster", bg="#f3e6cf")
    save(art, f"{OUT}/oyster.webp", max_w=210, quality=86)
    clear()

if "barjeel" in PARTS:
    # coral-stone houses with wind towers, warm afternoon light from the left, for the closing
    W, H = 760, 300
    nx = Seq(44000)
    rng = random.Random(4)
    art = blank(W, H)
    GY = 290
    blocks = [(10, 150, 170), (150, 300, 120), (280, 470, 150), (450, 600, 110), (590, 750, 160)]
    towers = [(70, 64, 260), (370, 70, 286), (660, 60, 266)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for x0, x1, h in blocks:
        m = rects(W, H, [(x0, GY - h, x1, GY)])
        art = GP(art, m, STONE, STONE_S, seed=nx(), rough=1.0, streak=0.6, pad=6)
        art = G(art, side_shade(m, (x0 + x1) / 2, x1 + 20), STONE_D, seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=2)
        par = shapes(W, H, [[(x, GY - h), (x + 6, GY - h - 9), (x + 12, GY - h)] for x in np.arange(x0 + 2, x1 - 10, 13)], smooth=False)
        art = GP(art, par, STONE, STONE_S, seed=nx(), rough=0.4, pad=4)
        art = G(art, rects(W, H, [(x0, GY - h, x1, GY - h + 6)]), STONE_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
        # coral texture specks
        sp = circles(W, H, [(rng.uniform(x0 + 4, x1 - 4), rng.uniform(GY - h + 10, GY - 4), rng.uniform(1, 2.6)) for _ in range(int((x1 - x0) * h / 300))])
        art = G(art, sp, "#b7966c", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.5, feather=0.5)
        # door + windows
        dx = (x0 + x1) / 2 - 16
        art = GP(art, shapes(W, H, [arch_pts(dx, GY, 32, 66, 10)], smooth=False), "#6c3f22", "#53301b", seed=nx(), rough=0.4, pad=4)
        art = G(art, strokes(W, H, [([(dx + 16, GY - 50), (dx + 16, GY)], 1.4, None)]), "#3a2010", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
        for wx in (x0 + 18, x1 - 36):
            if wx + 18 < dx or wx > dx + 34:
                wm = rects(W, H, [(wx, GY - h + 30, wx + 18, GY - h + 58)])
                art = GP(art, wm, "#2f5e66", "#244a52", seed=nx(), rough=0.3, pad=4)
                art = G(art, strokes(W, H, [([(wx + 6, GY - h + 30), (wx + 6, GY - h + 58)], 1, None), ([(wx + 12, GY - h + 30), (wx + 12, GY - h + 58)], 1, None)]), "#d9c8a4", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.2)
    for tx, tw, th in towers:
        m = rects(W, H, [(tx - tw / 2, GY - th, tx + tw / 2, GY - 100)])
        art = GP(art, m, "#efdcba", STONE, seed=nx(), rough=0.8, streak=0.6, pad=6)
        art = G(art, side_shade(m, tx, tx + tw / 2 + 10), STONE_D, seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1.5)
        sl = rects(W, H, [(tx - tw / 2 + 8 + k * (tw - 16) / 4, GY - th + 22, tx - tw / 2 + 8 + k * (tw - 16) / 4 + (tw - 16) / 4 - 5, GY - th + 92) for k in range(4)])
        art = GP(art, sl, "#4c3426", "#3a281c", seed=nx(), rough=0.3, pad=4)
        cap = rects(W, H, [(tx - tw / 2 - 4, GY - th - 6, tx + tw / 2 + 4, GY - th + 4)])
        art = GP(art, cap, "#d8bf96", seed=nx(), rough=0.4, pad=4)
        cren = shapes(W, H, [[(x, GY - th - 6), (x + 5, GY - th - 16), (x + 10, GY - th - 6)] for x in np.arange(tx - tw / 2 - 2, tx + tw / 2 - 6, 11)], smooth=False)
        art = GP(art, cren, "#d8bf96", seed=nx(), rough=0.3, pad=4)
        beams = strokes(W, H, [([(tx - tw / 2 - 6, GY - th + 100 - k * 34), (tx - tw / 2 + 2, GY - th + 100 - k * 34)], 3, None) for k in range(3)] + [([(tx + tw / 2 - 2, GY - th + 100 - k * 34), (tx + tw / 2 + 6, GY - th + 100 - k * 34)], 3, None) for k in range(3)])
        art = GP(art, beams, TEAK, seed=nx(), rough=0.3, pad=4)
    # date palm tucked between houses
    pm = jw.palm(W, H, 528, GY - 104, 120, rng, -0.1)
    art = GP(art, pm, "#5d7a4e", "#46603c", seed=nx(), rough=1.0, pad=6)
    ground = rects(W, H, [(-10, GY - 2, W + 10, GY + 10)])
    art = GP(art, ground, "#d7bf96", seed=nx(), rough=1.5, pad=6)
    preview(art, "mt-barjeel")
    save(art, f"{OUT}/barjeel.webp", max_w=640, quality=82)
    clear()

if "pearls" in PARTS:
    W, H = 560, 90
    nx = Seq(45000)
    art = blank(W, H)
    thread = strokes(W, H, [(curve([(10, 30), (140, 58), (280, 66), (420, 58), (550, 30)], 60), 1.4, None)])
    art = G(art, thread, "#b08a54", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    pts = curve([(10, 30), (140, 58), (280, 66), (420, 58), (550, 30)], 200)
    for i in range(0, 200, 9):
        x, y = pts[i]
        if abs(x - 280) < 30:
            continue
        r = 5.5 + 3.2 * (1 - abs(x - 280) / 270)
        art = over(art, pearl_art(W, H, x, y, r, nx))
    art = over(art, pearl_art(W, H, 280, 68, 15, nx, warm=0.4))
    preview(art, "mt-pearls", bg="#f3e6cf")
    save(art, f"{OUT}/pearls.webp", max_w=280, quality=86)
    clear()

if "pearl" in PARTS:
    W, H = 120, 120
    nx = Seq(46000)
    art = pearl_art(W, H, 60, 60, 50, nx, warm=0.5)
    preview(art, "mt-pearl", bg=NAVY)
    save(art, f"{OUT}/pearl.webp", max_w=60, quality=88)
    clear()
