"""Syukuran Kelahiran — newborn welcome in stitched wool felt & knit: a wooden hoop crib mobile with hanging felt moon,
stars and cloud (each hanging piece is its own asset so it can sway), tiny watercolour footprints, a seamless knitted
blanket tile, a watercolour baby's-breath sprig and a running-stitch divider. Palette: sage, cream, butter.
Run: python3 -I syukuran-kelahiran.py [part ...]   Assets -> public/themes/art/syukuran-kelahiran/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c6_lib import *

OUT = outdir("syukuran-kelahiran")
PARTS = sys.argv[1:] or ["knit", "hoop", "moon", "star", "star2", "cloud", "feet", "sprig", "divider"]
CREAM = "#f7f1e1"
SAGE, SAGE_D, SAGE_L = "#9fb592", "#6f8a66", "#c6d4b8"
BUTTER, BUTTER_D = "#f3d98b", "#e2bd5c"
BLUSH = "#efc3b4"
WOOD, WOOD_D, WOOD_L = "#c89b6a", "#9b6e45", "#e0bd8f"
THREAD = "#a68e72"


def string(art, x, y0, y1, seed):
    h, w = art.shape[:2]
    pts = [(x + math.sin(t * 2.1) * 0.8, y0 + (y1 - y0) * t) for t in [i / 20 for i in range(21)]]
    m = strokes(w, h, [(pts, 2.2, None)])
    art = crayon(art, m, THREAD, seed=seed, amt=0.9, tooth=0.15)
    return art


def star_pts(cx, cy, r, inner=0.5, rot=-math.pi / 2):
    return [(cx + math.cos(rot + k * math.pi / 5) * (r if k % 2 == 0 else r * inner), cy + math.sin(rot + k * math.pi / 5) * (r if k % 2 == 0 else r * inner)) for k in range(10)]


def soften_star(pts, rng):
    return deform(pts, rng, 1, 0.015)


if "knit" in PARTS:
    t = knit_tile(256, 252, SAGE, SAGE_L, seed=5, cw=16, ch=14)
    save_full(t, f"{OUT}/knit.webp", quality=72)
    t2 = knit_tile(256, 252, "#f3ead3", "#fbf6ea", seed=6, cw=16, ch=14)
    save_full(t2, f"{OUT}/knit-cream.webp", quality=70)

if "hoop" in PARTS:
    W, H = 620, 300
    nx = Seq(41000); art = blank(W, H)
    cx, cy = 310, 210
    # four hanging strings meeting at the top loop
    for ex in (60, 220, 400, 560):
        pts = curve([(cx, 26), (ex, cy - 6)], 20)
        art = crayon(art, strokes(W, H, [(pts, 2.2, None)]), THREAD, seed=nx(), amt=0.85, tooth=0.15)
    ring = np.clip(ring_mask(W, H, 0, 0, 1, 1) * 0, 0, 1)
    def draw_ring(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=22)
        cv.c.drawOval(skia.Rect(cx - 270, cy - 40, cx + 270, cy + 40), p)
    ring = mask_from(W, H, draw_ring)
    back = ring * (np.mgrid[0:H, 0:W][0] < cy).astype(np.float32)
    front = ring * (np.mgrid[0:H, 0:W][0] >= cy).astype(np.float32)
    for part, dk in ((back, 0.35), (front, 0.0)):
        art = GP(art, part, WOOD, WOOD_L if dk == 0 else WOOD_D, seed=nx(), rough=1.2, streak=1.0)
        art = tint(art, side_light(part, 0, -8, 4), WOOD_D, 0.55 + dk, seed=nx())
        art = tint(art, side_light(part, 0, 7, 4), "#f1d9b3", 0.4, seed=nx())
    # felt ribbon wraps around the front of the hoop
    wraps = []
    for k in range(13):
        t = k / 12
        ang = math.pi * (0.06 + t * 0.88)
        x, y = cx + math.cos(ang) * 270, cy + math.sin(ang) * 40
        wraps.append(([(x - 9, y - 14), (x + 9, y + 14)], 9, None))
    wm = strokes(W, H, wraps)
    art = felt(art, wm, SAGE, SAGE_L, seed=nx(), stitch=None, pad=8)
    loop = ring_mask(W, H, cx, 20, 11, 4.5)
    art = crayon(art, loop, THREAD, seed=nx(), amt=0.9, tooth=0.1)
    # a felt bow at the top knot
    bow = shapes(W, H, [[(cx, 34), (cx - 34, 16), (cx - 36, 52)], [(cx, 34), (cx + 34, 16), (cx + 36, 52)]])
    art = felt(art, bow, BUTTER, BUTTER_D, seed=nx(), stitch=None, pad=8)
    art = felt(art, circles(W, H, [(cx, 34, 9)]), BUTTER_D, seed=nx(), stitch=None, pad=8)
    bbox_save(art, "kl-hoop", f"{OUT}/hoop.webp", 460, tone=CREAM)
    clear()


def hanging(name, W, H, top_y, piece_fn, max_w, seed0):
    nx = Seq(seed0); art = blank(W, H)
    art = string(art, W / 2, 0, top_y + 8, nx())
    art = piece_fn(art, nx)
    keep_pixel(art, 0, 0); keep_pixel(art, W - 1, 0)   # keep the string's top at the asset top, centred
    art[0, 0, 3] = art[0, W - 1, 3] = 0.03
    bbox_save(art, f"kl-{name}", f"{OUT}/{name}.webp", max_w, tone=CREAM)
    clear()


if "moon" in PARTS:
    def moon(art, nx):
        W, H = art.shape[1], art.shape[0]
        a = circles(W, H, [(120, 250, 92)])
        b = circles(W, H, [(170, 268, 80)])
        m = np.clip(a - b, 0, 1)
        art = felt(art, m, BUTTER, "#f7e3a4", seed=nx(), stitch="#fffaf0", stitch_in=9)
        # sleepy eye + cheek embroidered
        art = crayon(art, strokes(W, H, [(arc_pts(62, 250, 10, 0.2, 2.9, 10), 3.0, None)]), "#7a6040", seed=nx(), amt=0.9, tooth=0.1)
        art = G(art, circles(W, H, [(62, 276, 9)]), BLUSH, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1.5, feather=2.5)
        return art
    hanging("moon", 240, 360, 160, moon, 170, 42000)

if "star" in PARTS:
    def star(art, nx):
        W, H = art.shape[1], art.shape[0]
        m = shapes(W, H, [soften_star(star_pts(W / 2, 168, 62, 0.5), random.Random(2))])
        return felt(art, m, BUTTER, BUTTER_D, seed=nx(), stitch="#fffaf0", stitch_in=8, dash=6)
    hanging("star", 180, 250, 110, star, 110, 43000)

if "star2" in PARTS:
    def star2(art, nx):
        W, H = art.shape[1], art.shape[0]
        m = shapes(W, H, [soften_star(star_pts(W / 2, 214, 50, 0.52, -math.pi / 2 + 0.2), random.Random(4))])
        return felt(art, m, SAGE, SAGE_L, seed=nx(), stitch="#fbf6e9", stitch_in=7, dash=6)
    hanging("star2", 150, 280, 164, star2, 92, 44000)

if "cloud" in PARTS:
    def cloud(art, nx):
        W, H = art.shape[1], art.shape[0]
        m = circles(W, H, [(80, 230, 40), (124, 206, 52), (172, 226, 42), (126, 246, 38)])
        m = np.clip(m + shapes(W, H, [[(48, 236), (204, 236), (200, 268), (52, 268)]]), 0, 1)
        m = gaussian_filter(m, 2) > 0.5
        art = felt(art, m.astype(np.float32), "#fbf7ec", "#f2ead6", seed=nx(), stitch=SAGE_D, stitch_in=8, dash=6)
        # dangling felt raindrop hearts under the cloud
        for x, y in ((92, 300), (150, 312)):
            art = crayon(art, strokes(W, H, [([(x, 262), (x, y - 12)], 1.8, None)]), THREAD, seed=nx(), amt=0.85, tooth=0.1)
            hm = shapes(W, H, [[(x, y + 14), (x - 13, y), (x - 11, y - 10), (x - 4, y - 12), (x, y - 6), (x + 4, y - 12), (x + 11, y - 10), (x + 13, y)]])
            art = felt(art, hm, BLUSH, "#f4d2c6", seed=nx(), stitch=None, pad=8)
        return art
    hanging("cloud", 260, 340, 160, cloud, 160, 45000)

if "feet" in PARTS:
    W, H = 300, 260
    nx = Seq(46000); rng = random.Random(8); art = blank(W, H)
    for (fx, fy, rot, col) in ((100, 150, -0.18, SAGE), (196, 118, 0.16, SAGE)):
        ca, sa = math.cos(rot), math.sin(rot)
        def P(u, v):
            return (fx + u * ca - v * sa, fy + u * sa + v * ca)
        sole = [P(u, v) for u, v in [(-4, -50), (16, -46), (27, -30), (26, -8), (20, 14), (20, 34), (16, 52), (2, 62), (-12, 56), (-17, 38), (-12, 18), (-14, 0), (-22, -20), (-20, -40)]]
        m = shapes(W, H, [deform(sole, rng, 1, 0.02)])
        art = G(art, m, col, SAGE_D, seed=nx(), density=0.62, edge=0.7, bloom=0.4, rough=3, gran=0.35)
        toes = [(*P(u, v), r) for u, v, r in [(-18, -62, 9.5), (-2, -70, 8), (12, -66, 7), (22, -58, 6), (29, -48, 5)]]
        art = G(art, circles(W, H, toes), col, SAGE_D, seed=nx(), density=0.66, edge=0.7, bloom=0.2, rough=1.5, gran=0.35)
    bbox_save(art, "kl-feet", f"{OUT}/feet.webp", 160, tone=CREAM)
    clear()

if "sprig" in PARTS:
    W, H = 360, 460
    nx = Seq(47000); rng = random.Random(10); art = blank(W, H)
    stems = [curve([(180, 450), (172, 330), (150, 220), (118, 110)], 30), curve([(180, 450), (196, 320), (232, 210), (262, 120)], 30),
             curve([(176, 360), (120, 300), (70, 260)], 20), curve([(190, 300), (250, 270), (300, 238)], 20)]
    art = G(art, strokes(W, H, [(st, 4.5, (0.0, 0.5)) for st in stems]), SAGE_D, seed=nx(), density=0.6, edge=0.4, bloom=0, rough=1.5, feather=0.8)
    leaves = []
    for st in stems:
        for j in range(4, len(st) - 3, 5):
            x, y = st[j]; a, b = st[j - 1], st[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                if rng.random() < 0.7:
                    leaves.append(petal_pts(x, y, rng.uniform(30, 44), rng.uniform(8, 11), ang + side * 0.9 + math.pi, n=12))
    lm = shapes(W, H, leaves)
    art = G(art, lm, SAGE, SAGE_D, seed=nx(), density=0.6, edge=0.55, bloom=0.4, rough=3)
    # baby's breath clusters (tiny cream/white dots with butter centres) at the stem tips
    for st in stems:
        x, y = st[-1]
        dots = [(x + rng.gauss(0, 16), y + rng.gauss(0, 12), rng.uniform(4.5, 7.5)) for _ in range(16)]
        dm = circles(W, H, dots)
        art = G(art, dm, "#fbf7ec", "#ece2c8", seed=nx(), density=0.95, edge=0.8, bloom=0, rough=1.2, gran=0.2)
        art = G(art, circles(W, H, [(dx, dy, 1.8) for dx, dy, _ in dots]), BUTTER_D, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5, feather=0.6)
    bbox_save(art, "kl-sprig", f"{OUT}/sprig.webp", 220, tone=CREAM)
    clear()

if "divider" in PARTS:
    W, H = 440, 90
    nx = Seq(48000); art = blank(W, H)
    yy = 45
    dashes = []
    for x in range(10, 430, 16):
        if 180 < x < 260:
            continue
        dashes.append(([(x, yy + math.sin(x / 30) * 2), (x + 9, yy + math.sin((x + 9) / 30) * 2)], 3.2, None))
    art = crayon(art, strokes(W, H, dashes), SAGE_D, seed=nx(), amt=0.9, tooth=0.12)
    m = shapes(W, H, [soften_star(star_pts(220, 46, 30, 0.5), random.Random(3))])
    art = felt(art, m, BUTTER, BUTTER_D, seed=nx(), stitch="#fffaf0", stitch_in=6, dash=5)
    bbox_save(art, "kl-divider", f"{OUT}/divider.webp", 300, tone=CREAM)
    clear()
