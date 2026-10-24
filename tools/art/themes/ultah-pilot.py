"""Ultah Pilot — kids' birthday, little-pilot party in opaque gouache (no outlines, shading in a second tone and dry
highlights): a friendly red propeller plane with a yellow wing and round portholes, a cream banner on a tow rope (name is
set in HTML on top of it), fluffy clouds, an airfield strip with runway lights, a striped control tower and an orange
windsock, a pilot cap with a generic wings badge, and the wings badge alone as a divider.
Run: python3 -I ultah-pilot.py [part ...]   parts: pesawat spanduk awan bandara topi sayap"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s1_lib import *

OUT = outdir("ultah-pilot")
PARTS = sys.argv[1:] or ["pesawat", "spanduk", "awan", "bandara", "topi", "sayap"]
RED, RED_D, RED_L = "#e8473c", "#b8302a", "#f4776a"
YEL, YEL_D = "#ffc93c", "#e09a1c"
NAVY, NAVY_D = "#22427a", "#162c55"
CREAM, CREAM_D = "#fff6e5", "#ecd9b8"
SKYL = "#bfe6fb"
GRASS, GRASS_D = "#72c25f", "#4f9a45"
GREY, GREY_D = "#8c97a6", "#5f6a7a"
SKY_BG = "#8fd0f2"


def paint(art, m, c1, c2=None, nx=None, **k):
    return GP(art, m, c1, c2 or c1, seed=nx(), **{"rough": 2.2, "streak": 0.6, **k})


def shade(art, m, col, nx, amt=0.55):
    return OV(art, m, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32),
                                                   (np.clip(gaussian_filter(mm, 1.2), 0, 1) * amt)[..., None]], -1))


if "pesawat" in PARTS:
    W, H = 620, 340
    rng = random.Random(191); nx = Seq(191000)
    art = blank(W, H)
    yy, xx = yx(W, H)
    # far wing (behind the body), darker
    farwing = poly(W, H, [(250, 168), (300, 120), (346, 118), (318, 168)], smooth=True)
    art = paint(art, farwing, YEL_D, "#d08a18", nx)
    # tail fin + stabiliser
    fin = poly(W, H, [(70, 150), (60, 62), (82, 52), (112, 70), (150, 140)], smooth=True)
    art = paint(art, fin, RED, RED_D, nx)
    stab = ell(W, H, 104, 150, 56, 13, -6)
    art = paint(art, stab, YEL, YEL_D, nx)
    # fuselage: plump capsule, nose right
    body = poly(W, H, [(78, 140), (120, 120), (200, 106), (330, 100), (420, 108), (468, 130), (476, 160), (462, 190), (410, 208),
                       (300, 212), (190, 200), (120, 178), (80, 160)], smooth=True)
    art = paint(art, body, RED, RED_L, nx)
    belly = body * np.clip((yy - 168) / 40, 0, 1)
    art = shade(art, belly, RED_D, nx, 0.6)
    top_hl = body * np.clip((130 - yy) / 24, 0, 1) * np.clip((xx - 160) / 80, 0, 1)
    art = shade(art, top_hl, "#ff9a8c", nx, 0.5)
    stripe = np.clip(line(W, H, [(96, 156), (200, 166), (330, 170), (468, 166)], 15, None) * body, 0, 1)
    art = paint(art, stripe, CREAM, CREAM_D, nx)
    # star on the fin
    sp = [(92 + math.cos(-math.pi / 2 + k * math.pi / 5) * (14 if k % 2 == 0 else 6), 96 + math.sin(-math.pi / 2 + k * math.pi / 5) * (14 if k % 2 == 0 else 6)) for k in range(10)]
    art = paint(art, poly(W, H, sp), CREAM, nx=nx)
    # cockpit: windscreen + open seat rim
    screen = poly(W, H, [(286, 104), (300, 66), (322, 64), (336, 102)], smooth=True)
    art = paint(art, screen, SKYL, "#dff3ff", nx, density=0.85)
    art = shade(art, poly(W, H, [(302, 70), (310, 68), (306, 100), (298, 100)]), "#ffffff", nx, 0.7)
    rim = ell(W, H, 270, 104, 40, 7)
    art = paint(art, rim, NAVY, NAVY_D, nx)
    # portholes
    for cx in (210, 250):
        art = paint(art, circles(W, H, [(cx, 140, 13)]), CREAM_D, nx=nx)
        art = paint(art, circles(W, H, [(cx, 140, 9)]), SKYL, "#e8f7ff", nx)
        art = shade(art, circles(W, H, [(cx - 3, 136, 3)]), "#ffffff", nx, 0.9)
    # near wing (in front), with a light leading edge
    wing = poly(W, H, [(222, 186), (300, 168), (402, 170), (380, 200), (300, 224), (240, 218)], smooth=True)
    art = paint(art, wing, YEL, "#ffd968", nx)
    art = shade(art, wing * np.clip((yy - 200) / 22, 0, 1), YEL_D, nx, 0.6)
    # landing gear
    struts = line(W, H, [(300, 214), (290, 262)], 7, None) + line(W, H, [(380, 204), (392, 262)], 7, None)
    art = paint(art, np.clip(struts, 0, 1), NAVY, nx=nx)
    for cx in (290, 392):
        art = paint(art, circles(W, H, [(cx, 268, 22)]), "#2b2b3a", "#3a3a4c", nx)
        art = paint(art, circles(W, H, [(cx, 268, 9)]), GREY, "#b8c0cc", nx)
    tailwheel = circles(W, H, [(96, 182, 8)])
    art = paint(art, tailwheel, "#2b2b3a", nx=nx)
    # nose cone + propeller hub
    cone = ell(W, H, 478, 158, 22, 26)
    art = paint(art, cone, YEL, YEL_D, nx)
    art = shade(art, circles(W, H, [(484, 150, 6)]), "#fff3c8", nx, 0.8)
    # a friendly face on the nose (eye + smile), very simple
    art = paint(art, circles(W, H, [(430, 140, 6)]), NAVY_D, nx=nx)
    art = shade(art, circles(W, H, [(432, 138, 2)]), "#ffffff", nx, 0.9)
    smile = line(W, H, arc_pts(432, 166, 16, math.pi * 0.2, math.pi * 0.75, 12), 4, (0.2, 0.2))
    art = paint(art, smile, NAVY_D, nx=nx)
    art = shade(art, circles(W, H, [(412, 172, 9)]), "#ff9a8c", nx, 0.6)
    preview(art, "up-pesawat", bg=SKY_BG)
    save(art, f"{OUT}/pesawat.webp", max_w=380, quality=84)
    clear()

if "spanduk" in PARTS:
    # banner cloth + tow rope to the right; the name is HTML text laid over the cloth
    W, H = 760, 200
    rng = random.Random(192); nx = Seq(192000)
    art = blank(W, H)
    top = [(x, 40 + 8 * math.sin(x / 70)) for x in range(30, 611, 10)]
    bot = [(x, 160 + 8 * math.sin(x / 70 + 0.4)) for x in range(610, 29, -10)]
    cloth = poly(W, H, top + bot, smooth=True)
    art = paint(art, cloth, CREAM, "#fffaf0", nx, rough=1.6)
    yy, xx = yx(W, H)
    folds = cloth * (0.5 + 0.5 * np.sin(xx / 70 + 1.2)) ** 3
    art = shade(art, folds, CREAM_D, nx, 0.55)
    hem = np.clip(cloth - poly(W, H, [(p[0], p[1] + 12) for p in top] + [(p[0], p[1] - 12) for p in bot], smooth=True), 0, 1)
    art = paint(art, hem, RED, RED_D, nx, rough=1.4)
    # flappy tail end (left), split
    tail = poly(W, H, [(32, 44), (-4, 60), (18, 100), (-6, 142), (32, 156)], smooth=False)
    art = paint(art, tail, RED, RED_D, nx)
    # rope: from the banner's right edge, a bridle to one tow line
    rope = line(W, H, [(610, 46), (700, 96), (756, 98)], 3.4, None) + line(W, H, [(610, 166), (700, 100)], 3.4, None)
    art = paint(art, np.clip(rope, 0, 1), "#7a5a3a", "#5e432a", nx, rough=0.8)
    preview(art, "up-spanduk", bg=SKY_BG)
    save_full(art, f"{OUT}/spanduk.webp", size=(380, 100), quality=84)
    clear()

if "awan" in PARTS:
    W, H = 420, 220
    rng = random.Random(193); nx = Seq(193000)
    art = blank(W, H)
    puffs = [(110, 140, 56), (180, 104, 72), (262, 112, 62), (320, 146, 48), (70, 166, 36), (210, 160, 60), (360, 170, 30)]
    m = circles(W, H, puffs)
    m = np.clip(m * (yx(W, H)[0] < 190), 0, 1)
    art = paint(art, m, "#ffffff", "#f7fbff", nx, rough=3)
    yy = yx(W, H)[0]
    art = shade(art, m * np.clip((yy - 150) / 40, 0, 1), "#cfe4f3", nx, 0.8)
    preview(art, "up-awan", bg=SKY_BG)
    save(art, f"{OUT}/awan.webp", max_w=210, quality=84)
    clear()

if "bandara" in PARTS:
    W, H = 800, 360
    rng = random.Random(194); nx = Seq(194000)
    art = blank(W, H)
    yy, xx = yx(W, H)
    # distant hills
    hills_m = ridge_mask(W, H, 210, 26, 5, freq=2.0, sharp=0.9, bottom=H)
    art = paint(art, hills_m, "#a6dc8c", "#93d27d", nx)
    # hangar with an arched roof (left of the tower)
    hang = poly(W, H, [(440, 250), (440, 196), (470, 168), (520, 158), (570, 168), (600, 196), (600, 250)], smooth=True)
    art = paint(art, hang, "#dfe6ee", "#c9d3df", nx)
    ribs = strokes(W, H, [([(x, 250), (x, 170 + abs(x - 520) * 0.3)], 2.4, None) for x in range(456, 590, 16)]) * hang
    art = paint(art, ribs, "#aab6c4", nx=nx, rough=0.6)
    door = poly(W, H, [(482, 250), (482, 206), (558, 206), (558, 250)], smooth=False)
    art = paint(art, door, NAVY, NAVY_D, nx)
    art = paint(art, strokes(W, H, [([(482 + k * 19, 208), (482 + k * 19, 250)], 2, None) for k in range(1, 4)]), "#3a5a94", nx=nx, rough=0.5)
    # control tower (right): base block, slim shaft, overhanging slanted glass cab, flat roof, antenna + red tip
    base = poly(W, H, [(618, 250), (618, 214), (708, 214), (708, 250)], smooth=False)
    art = paint(art, base, CREAM, CREAM_D, nx)
    art = paint(art, poly(W, H, [(652, 250), (652, 226), (672, 226), (672, 250)], smooth=False), RED, RED_D, nx)
    shaft = poly(W, H, [(640, 214), (646, 112), (680, 112), (686, 214)], smooth=False)
    art = paint(art, shaft, CREAM, "#ffffff", nx)
    art = paint(art, poly(W, H, [(644, 140), (646, 120), (680, 120), (682, 140)], smooth=False), RED, RED_D, nx, rough=1.2)
    art = paint(art, poly(W, H, [(638, 112), (688, 112), (690, 104), (636, 104)], smooth=False), NAVY, nx=nx)
    cab = poly(W, H, [(632, 104), (618, 66), (708, 66), (694, 104)], smooth=False)
    art = paint(art, cab, SKYL, "#e2f5ff", nx)
    mull = strokes(W, H, [([(x0, 68), (x0 + (663 - x0) * 0.25, 102)], 3, None) for x0 in (640, 663, 686)])
    art = paint(art, mull, NAVY, nx=nx)
    art = shade(art, poly(W, H, [(626, 70), (640, 70), (646, 100), (636, 100)]), "#ffffff", nx, 0.6)
    roof = poly(W, H, [(610, 68), (716, 68), (712, 56), (614, 56)], smooth=False)
    art = paint(art, roof, NAVY, NAVY_D, nx)
    art = paint(art, line(W, H, [(690, 56), (690, 24)], 3, None) + circles(W, H, [(690, 22, 5)]), RED, nx=nx)
    dish = ell(W, H, 636, 48, 12, 6, -20)
    art = paint(art, dish + line(W, H, [(636, 56), (636, 50)], 3, None), "#dfe6ee", nx=nx)
    # windsock (left)
    pole = line(W, H, [(110, 250), (110, 150)], 4, None)
    art = paint(art, pole, GREY_D, nx=nx)
    sock = poly(W, H, [(112, 152), (176, 160), (172, 178), (112, 176)], smooth=False)
    art = paint(art, sock, "#ff8a2a", "#f06e18", nx)
    for x0 in (128, 156):
        art = paint(art, poly(W, H, [(x0, 154), (x0 + 12, 156), (x0 + 12, 177), (x0, 176)], smooth=False) * sock, "#ffffff", nx=nx)
    # grass field
    field = (yy > 238).astype(np.float32)
    art = paint(art, field, GRASS, "#82cd6e", nx, rough=3)
    tufts = []
    for _ in range(80):
        x = rng.uniform(0, W); y = rng.uniform(250, H - 6)
        for k in range(3):
            a = -math.pi / 2 + (k - 1) * 0.35
            tufts.append(([(x, y), (x + math.cos(a) * 9, y + math.sin(a) * 9)], 2.2, (0.0, 0.6)))
    art = paint(art, strokes(W, H, tufts), GRASS_D, nx=nx, rough=0.8)
    # runway: a grey band with dashed centre line and edge lights
    rw = poly(W, H, [(-10, 286), (W + 10, 280), (W + 10, 330), (-10, 338)], smooth=False)
    art = paint(art, rw, GREY, "#9aa4b2", nx)
    dash = strokes(W, H, [([(x, 309 - x * 0.0075), (x + 34, 309 - (x + 34) * 0.0075)], 5, None) for x in range(10, W, 70)])
    art = paint(art, dash, "#ffffff", nx=nx, rough=1)
    for x in range(30, W, 60):
        for y, col in ((282 - x * .0075, YEL), (334 - x * .0075, RED)):
            art = paint(art, circles(W, H, [(x, y, 5)]), col, nx=nx, rough=0.6)
            art = over(art, glow(circles(W, H, [(x, y, 4)]), "#fff3b0", radius=5, strength=0.4))
    art[..., 3] *= np.clip((yy - 0) / 1, 0, 1)
    preview(art, "up-bandara", bg=SKY_BG)
    save(art, f"{OUT}/bandara.webp", max_w=560, quality=80)
    clear()

if "topi" in PARTS:
    W, H = 360, 260
    rng = random.Random(195); nx = Seq(195000)
    art = blank(W, H)
    crown = poly(W, H, [(60, 150), (50, 90), (110, 52), (200, 44), (290, 64), (318, 112), (300, 156)], smooth=True)
    art = paint(art, crown, CREAM, "#ffffff", nx)
    yy = yx(W, H)[0]
    art = shade(art, crown * np.clip((yy - 110) / 50, 0, 1), CREAM_D, nx, 0.7)
    band = poly(W, H, [(62, 144), (300, 150), (296, 180), (66, 176)], smooth=False)
    art = paint(art, band, NAVY, NAVY_D, nx)
    cord = line(W, H, [(70, 150), (296, 154)], 5, None)
    art = paint(art, cord, YEL, YEL_D, nx, rough=0.8)
    visor = poly(W, H, [(64, 172), (296, 176), (280, 214), (180, 228), (90, 210)], smooth=True)
    art = paint(art, visor, "#1b2440", "#2a3558", nx)
    art = shade(art, poly(W, H, [(120, 186), (240, 188), (230, 196), (130, 196)]), "#56648a", nx, 0.7)
    # wings badge on the crown
    bx, by = 182, 104
    feathers = []
    for side in (-1, 1):
        for k in range(4):
            L = 54 - k * 9
            y = by - 8 + k * 6
            feathers.append([(bx + side * 12, y), (bx + side * (12 + L), y - 6 + k * 1.5), (bx + side * (16 + L * 0.8), y + 6), (bx + side * 12, y + 6)])
    wm = shapes(W, H, feathers, smooth=True)
    art = FO(art, wm, "#d9a93c", seed=nx(), emboss=0.6, sparkle=0.1)
    art = paint(art, circles(W, H, [(bx, by, 15)]), RED, RED_D, nx)
    sp = [(bx + math.cos(-math.pi / 2 + k * math.pi / 5) * (9 if k % 2 == 0 else 4), by + math.sin(-math.pi / 2 + k * math.pi / 5) * (9 if k % 2 == 0 else 4)) for k in range(10)]
    art = paint(art, poly(W, H, sp), CREAM, nx=nx)
    preview(art, "up-topi", bg=SKY_BG)
    save(art, f"{OUT}/topi.webp", max_w=220, quality=84)
    clear()

if "sayap" in PARTS:
    W, H = 440, 120
    rng = random.Random(196); nx = Seq(196000)
    art = blank(W, H)
    bx, by = 220, 56
    feathers = []
    for side in (-1, 1):
        for k in range(5):
            L = 170 - k * 26
            y = by - 18 + k * 9
            feathers.append([(bx + side * 26, y), (bx + side * (26 + L), y - 12 + k * 2), (bx + side * (32 + L * 0.85), y + 9), (bx + side * 26, y + 9)])
    wm = shapes(W, H, feathers, smooth=True)
    art = FO(art, wm, "#d9a93c", seed=nx(), emboss=0.6, sparkle=0.12)
    art = paint(art, circles(W, H, [(bx, by, 30)]), RED, RED_D, nx)
    art = paint(art, ring(W, H, bx, by, 30, 5), YEL, YEL_D, nx, rough=0.8)
    sp = [(bx + math.cos(-math.pi / 2 + k * math.pi / 5) * (17 if k % 2 == 0 else 7), by + math.sin(-math.pi / 2 + k * math.pi / 5) * (17 if k % 2 == 0 else 7)) for k in range(10)]
    art = paint(art, poly(W, H, sp), CREAM, nx=nx)
    preview(art, "up-sayap", bg=SKY_BG)
    save(art, f"{OUT}/sayap.webp", max_w=220, quality=84)
    clear()
