"""Ultah Antariksa — friendly space birthday in gouache: a cream-and-red rocket (separate flickering flame), a ringed
orange planet, a small mint planet, a smiling moon, an astronaut helmet frame (visor left open for the portrait), a
painted star, and a painted night sky. Original designs, no characters.
Run: python3 -I ultah-antariksa.py [part ...]  parts: sky rocket flame planet planet2 moon helmet star
Assets -> public/themes/art/ultah-antariksa/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b5_lib import *

OUT = outdir("ultah-antariksa")
PARTS = sys.argv[1:] or ["sky", "rocket", "flame", "planet", "planet2", "moon", "helmet", "star"]
INK = "#1d1b3a"
CREAM, CREAM_D = "#f6ecd6", "#d7c6a4"
RED, RED_D = "#e8573f", "#b63a2a"
TEAL, TEAL_D = "#4fb8b0", "#2f8a86"
YEL, YEL_D = "#f7c95a", "#d99a2c"
ORANGE, ORANGE_D = "#f29a52", "#c7672d"
NAVY = "#1b2452"


def paint(art, m, col, col2, dark, light, nx, ld=(-14, -16), line=True, line_col=None):
    art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=.5)
    art = tint(art, side_light(m, -ld[0], -ld[1], 10), dark, .7, seed=nx())
    art = tint(art, side_light(m, ld[0] * .6, ld[1] * .6, 7), light, .45, seed=nx())
    if line:
        art = crayon(art, inner_edge(m, 2.0), line_col or mix(dark, INK, .5), seed=nx(), amt=.7, tooth=.3)
    return art


def star_pts(cx, cy, r, inner=.48, rot=-math.pi / 2, n=5):
    pts = []
    for k in range(n * 2):
        rr = r if k % 2 == 0 else r * inner
        a = rot + k * math.pi / n
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


if "sky" in PARTS:
    W, H = 480, 980
    nx = Seq(50100); rng = random.Random(1)
    sky = painted_sky(W, H, [(0, "#141a3f"), (.45, "#1f2a5e"), (.8, "#30347a"), (1, "#4a3f8c")], seed=50100, streak=.9, grain=.7)
    # soft milky band
    band = strokes(W, H, [(curve([(-40, 760), (160, 520), (330, 330), (520, 120)], 30), 150, None)])
    sky = over(sky, col_arr(band, "#6f7bc4", gaussian_filter(band, 40) * .22))
    # stars: tiny dots + a few gouache sparkles
    dots = [(rng.uniform(0, W), rng.uniform(0, H), rng.choice([1.0, 1.2, 1.5, 2.0])) for _ in range(230)]
    sky = OV(sky, circles(W, H, dots), lambda m: col_arr(m, "#fff6dc", m * .85), pad=2)
    for _ in range(14):
        x, y, r = rng.uniform(20, W - 20), rng.uniform(20, H - 20), rng.uniform(5, 9)
        sky = GP(sky, shapes(W, H, [petal_pts(x, y, r, r * .22, a, n=10) for a in (0, math.pi / 2, math.pi, -math.pi / 2)]), "#fff1c8", seed=nx(), rough=.4, pad=6)
    sky[..., 3] = 1
    save_rgb(sky, f"{OUT}/sky.webp", quality=74)
    clear()

if "rocket" in PARTS:
    W, H = 340, 560
    nx = Seq(50200); rng = random.Random(3)
    c = W / 2
    art = blank(W, H)
    body = shapes(W, H, [[(c, 36), (c + 40, 86), (c + 66, 170), (c + 72, 290), (c + 64, 400), (c + 44, 446), (c - 44, 446), (c - 64, 400), (c - 72, 290), (c - 66, 170), (c - 40, 86)]])
    nose = body * (np.mgrid[0:H, 0:W][0] < 140 + 10 * np.sin(np.mgrid[0:H, 0:W][1] / 20)).astype(np.float32)
    finL = shapes(W, H, [[(c - 62, 320), (c - 116, 400), (c - 124, 470), (c - 92, 452), (c - 52, 430)]])
    finR = shapes(W, H, [[(c + 62, 320), (c + 116, 400), (c + 124, 470), (c + 92, 452), (c + 52, 430)]])
    finC = shapes(W, H, [[(c - 12, 380), (c + 12, 380), (c + 14, 476), (c - 14, 476)]])
    nozzle = shapes(W, H, [[(c - 40, 440), (c + 40, 440), (c + 30, 486), (c - 30, 486)]])
    art = paint(art, nozzle, "#9aa4b8", "#7f8aa0", "#4c5570", "#c7cedb", nx)
    art = paint(art, np.clip(finL + finR, 0, 1), RED, "#ee6a4f", RED_D, "#f59a80", nx)
    art = paint(art, body, CREAM, "#fbf3e2", CREAM_D, "#ffffff", nx, ld=(-18, -6))
    art = paint(art, nose, RED, "#ee6a4f", RED_D, "#f59a80", nx, ld=(-18, -6), line=False)
    stripe = body * strokes(W, H, [([(c - 80, 352), (c + 80, 352)], 18, None)])
    art = paint(art, stripe, TEAL, "#5cc4bb", TEAL_D, "#8fdcd3", nx, line=False)
    art = paint(art, finC, RED, "#ee6a4f", RED_D, "#f59a80", nx)
    # porthole
    ring = np.clip(circles(W, H, [(c, 232, 46)]) - circles(W, H, [(c, 232, 32)]), 0, 1)
    glass = circles(W, H, [(c, 232, 33)])
    art = paint(art, glass, "#2b3a7a", "#3e5aa8", "#1b2452", "#6f8ed8", nx, ld=(10, 10), line=False)
    art = GP(art, shapes(W, H, [petal_pts(c - 14, 214, 22, 6, -.7, n=10)]), "#cfe3ff", seed=nx(), rough=.4, pad=6)
    art = GP(art, circles(W, H, [(c + 12, 246, 4)]), "#cfe3ff", seed=nx(), rough=.3, pad=6)
    art = paint(art, ring, "#c9d1de", "#b3bccd", "#6b7590", "#f2f5fa", nx)
    rivets = circles(W, H, [(c + math.cos(a) * 39, 232 + math.sin(a) * 39, 2.6) for a in np.linspace(0, math.tau, 9)[:-1]])
    art = OV(art, rivets, lambda m: col_arr(m, "#6b7590", m * .9), pad=4)
    # tiny star sticker on the body
    art = GP(art, shapes(W, H, [star_pts(c + 30, 300, 13)]), YEL, seed=nx(), rough=.5, pad=6)
    art = crayon(art, strokes(W, H, [(curve([(c - 54, 150), (c - 62, 240), (c - 58, 320)], 14), 6, (.2, .3))]) * body, "#ffffff", seed=nx(), amt=.7, tooth=.3)
    preview(art, "space-rocket", bg="#1f2a5e")
    save(art, f"{OUT}/rocket.webp", max_w=220, quality=84)
    clear()

if "flame" in PARTS:
    W, H = 200, 260
    nx = Seq(50300)
    c = W / 2
    art = blank(W, H)
    outer = shapes(W, H, [petal_pts(c, 12, 230, 52, math.pi / 2, n=18)])
    mid = shapes(W, H, [petal_pts(c, 10, 170, 34, math.pi / 2, n=16)])
    core = shapes(W, H, [petal_pts(c, 8, 100, 18, math.pi / 2, n=14)])
    art = GP(art, outer, ORANGE, "#f07a3c", seed=nx(), rough=3, streak=.8)
    art = GP(art, mid, YEL, "#f9b84a", seed=nx(), rough=2.5, streak=.8)
    art = GP(art, core, "#fff3cf", seed=nx(), rough=2, streak=.6)
    for x, y, r in ((c - 42, 150, 6), (c + 46, 176, 5), (c - 22, 214, 4), (c + 20, 232, 3.5)):
        art = GP(art, circles(W, H, [(x, y, r)]), YEL, seed=nx(), rough=.5, pad=6)
    preview(art, "space-flame", bg="#1f2a5e")
    save(art, f"{OUT}/flame.webp", max_w=120, quality=84)
    clear()

if "planet" in PARTS:
    W, H = 520, 380
    nx = Seq(50400); rng = random.Random(5)
    cx, cy, r = 260, 190, 118
    art = blank(W, H)
    tilt = -.32

    def ring_mask(front):
        outer = ellipses(W, H, [(cx, cy, 236, 62, math.degrees(tilt))])
        inner = ellipses(W, H, [(cx, cy, 170, 36, math.degrees(tilt))])
        rm = np.clip(outer - inner, 0, 1)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        # front half = below the tilted major axis
        side = ((yy - cy) * math.cos(tilt) - (xx - cx) * math.sin(tilt)) > 0
        return rm * (side if front else ~side)
    art = paint(art, ring_mask(False), "#e7d6b0", "#d6c08f", "#a68c5b", "#f6ead0", nx)
    ball = circles(W, H, [(cx, cy, r)])
    art = paint(art, ball, ORANGE, "#f4ad6a", ORANGE_D, "#f8c08a", nx, ld=(-26, -24))
    bands = []
    for k, (dy, wd) in enumerate(((-62, 16), (-20, 24), (30, 14), (66, 20))):
        bands.append(([(cx - 140, cy + dy + 30), (cx, cy + dy), (cx + 140, cy + dy - 34)], wd, None))
    art = paint(art, strokes(W, H, bands) * ball, "#e9824a", "#f08e55", ORANGE_D, "#f6b27c", nx, line=False)
    spots = circles(W, H, [(cx + 40, cy + 40, 14), (cx - 52, cy - 30, 9)]) * ball
    art = GP(art, spots, "#d86e3a", seed=nx(), rough=.8, pad=6)
    art = tint(art, side_light(ball, 30, 28, 18) * 1.2, "#7a3a2a", .45, seed=nx())
    art = paint(art, ring_mask(True), "#efe0bd", "#e1cc9d", "#a68c5b", "#fffaf0", nx)
    stripes = ring_mask(True) * ellipses(W, H, [(cx, cy, 206, 50, math.degrees(tilt))]) * (1 - ellipses(W, H, [(cx, cy, 196, 46, math.degrees(tilt))]))
    art = GP(art, stripes, TEAL, seed=nx(), rough=.5, pad=6)
    preview(art, "space-planet", bg="#1f2a5e")
    save(art, f"{OUT}/planet.webp", max_w=300, quality=84)
    clear()

if "planet2" in PARTS:
    W, H = 220, 220
    nx = Seq(50500)
    art = blank(W, H)
    ball = circles(W, H, [(110, 110, 88)])
    art = paint(art, ball, "#8fd6c4", "#a5e0cf", "#4f9e8e", "#c8f0e4", nx, ld=(-20, -18))
    craters = [(80, 84, 16), (138, 132, 22), (124, 70, 9), (76, 146, 11)]
    for x, y, rr in craters:
        cm = circles(W, H, [(x, y, rr)]) * ball
        art = GP(art, cm, "#74c0ae", seed=nx(), rough=.6, pad=6)
        art = tint(art, side_light(cm, -5, -5, 2) * 1.6, "#4f9e8e", .6, seed=nx())
    preview(art, "space-planet2", bg="#1f2a5e")
    save(art, f"{OUT}/planet2.webp", max_w=130, quality=84)
    clear()

if "moon" in PARTS:
    W, H = 360, 360
    nx = Seq(50600)
    art = blank(W, H)
    halo = circles(W, H, [(180, 180, 130)])
    art = over(art, glow(halo, "#fff0b8", radius=26, strength=.35))
    ball = circles(W, H, [(180, 180, 124)])
    art = paint(art, ball, "#fbe9a6", "#f8de8a", "#d9b25a", "#fff7d6", nx, ld=(-24, -22))
    for x, y, rr in ((236, 120, 18), (122, 250, 14), (250, 230, 10), (140, 116, 8)):
        cm = circles(W, H, [(x, y, rr)])
        art = GP(art, cm, "#f1d27a", seed=nx(), rough=.6, pad=6)
        art = tint(art, side_light(cm, -4, -4, 2) * 1.5, "#d9b25a", .55, seed=nx())
    # closed happy eyes, smile, cheeks
    eyes = strokes(W, H, [(arc_pts(146, 176, 15, math.pi * 1.1, math.pi * 1.9, 12), 5, (.2, .2)), (arc_pts(214, 176, 15, math.pi * 1.1, math.pi * 1.9, 12), 5, (.2, .2))])
    art = crayon(art, eyes, "#7a5a2a", seed=nx(), amt=.9, tooth=.2)
    smile = strokes(W, H, [(arc_pts(180, 196, 26, .35, math.pi - .35, 16), 5, (.2, .2))])
    art = crayon(art, smile, "#7a5a2a", seed=nx(), amt=.9, tooth=.2)
    art = G(art, circles(W, H, [(124, 214, 16), (236, 214, 16)]), "#f4a08a", seed=nx(), density=.55, edge=.2, bloom=0, rough=2, feather=3)
    preview(art, "space-moon", bg="#1f2a5e")
    save(art, f"{OUT}/moon.webp", max_w=220, quality=84)
    clear()

if "helmet" in PARTS:
    W, H = 520, 560
    nx = Seq(50700)
    cx, cy = 260, 250
    art = blank(W, H)
    shell = circles(W, H, [(cx, cy, 228)])
    visor = ellipses(W, H, [(cx, cy + 14, 168, 162, 0)])
    collar = shapes(W, H, [[(cx - 170, 430), (cx + 170, 430), (cx + 196, 520), (cx - 196, 520)]])
    art = paint(art, collar, "#c9d1de", "#b3bccd", "#6b7590", "#f2f5fa", nx)
    ridges = strokes(W, H, [([(cx - 180 + k * 8, 456 + k * 0), (cx + 180 - k * 8, 456)], 4, None) for k in (0,)] + [([(cx - 188, 488), (cx + 188, 488)], 4, None)]) * collar
    art = OV(art, ridges, lambda m: col_arr(m, "#8a93aa", m * .8), pad=4)
    shell_ring = np.clip(shell - visor, 0, 1)
    art = paint(art, shell_ring, "#f7f4ee", "#ffffff", "#b9bfcc", "#ffffff", nx, ld=(-30, -26))
    # visor rim
    rim_m = np.clip(ellipses(W, H, [(cx, cy + 14, 182, 176, 0)]) - visor, 0, 1)
    art = paint(art, rim_m, YEL, "#f9d77a", YEL_D, "#fff0b8", nx)
    # side lamp + antenna
    art = paint(art, ellipses(W, H, [(cx + 222, cy - 10, 22, 34, 0)]), RED, "#ee6a4f", RED_D, "#f59a80", nx)
    art = paint(art, ellipses(W, H, [(cx - 222, cy - 10, 22, 34, 0)]), RED, "#ee6a4f", RED_D, "#f59a80", nx)
    art = paint(art, strokes(W, H, [([(cx + 150, cy - 170), (cx + 186, cy - 236)], 6, None)]), "#9aa4b8", "#7f8aa0", "#4c5570", "#c7cedb", nx, line=False)
    art = GP(art, circles(W, H, [(cx + 188, cy - 240, 12)]), YEL, seed=nx(), rough=.4, pad=6)
    # a little star sticker
    art = GP(art, shapes(W, H, [star_pts(cx - 150, cy - 160, 18)]), TEAL, seed=nx(), rough=.4, pad=6)
    # gloss on the shell (top-left)
    art = tint(art, gaussian_filter(strokes(W, H, [(arc_pts(cx, cy, 205, math.pi * 1.08, math.pi * 1.42, 16), 12, (.3, .3))]), 2) * shell_ring, "#ffffff", .8, seed=nx())
    # translucent visor glint so the opening reads as glass (kept faint: the portrait shows through)
    glint = strokes(W, H, [(arc_pts(cx, cy + 14, 140, math.pi * 1.15, math.pi * 1.38, 12), 16, (.4, .4))]) * visor
    art = over(art, col_arr(glint, "#ffffff", gaussian_filter(glint, 3) * .45))
    preview(art, "space-helmet", bg="#1f2a5e")
    save_full(art, f"{OUT}/helmet.webp", size=(260, 280), quality=84)
    clear()

if "star" in PARTS:
    W, H = 160, 160
    nx = Seq(50800)
    art = blank(W, H)
    m = shapes(W, H, [star_pts(80, 84, 66, .5)])
    art = paint(art, m, YEL, "#f9d77a", YEL_D, "#fff0b8", nx, ld=(-10, -12))
    preview(art, "space-star", bg="#1f2a5e")
    save(art, f"{OUT}/star.webp", max_w=72, quality=86)
    clear()
