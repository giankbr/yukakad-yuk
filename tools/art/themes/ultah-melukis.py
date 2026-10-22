"""Ultah Melukis — gouache on cold-press paper, a kids' painting party: a wooden easel holding a blank canvas (the
child's name is set over it in the page), a kidney-shaped palette with fat blobs of paint and a brush, a jar of
brushes, a row of wax crayons, paint splatters in three colours, a crayon squiggle divider and a paper tile.
Run: python3 -I ultah-melukis.py [part ...]   parts: paper easel palette jar crayons splats squiggle
Assets -> public/themes/art/ultah-melukis/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g3_lib import *

OUT = outdir("ultah-melukis")
PARTS = sys.argv[1:] or ["paper", "easel", "palette", "jar", "crayons", "splats", "squiggle"]
RED, YEL, BLUE, GRN, PINK, ORA, PUR = "#e84a3c", "#f6c234", "#3a7bd5", "#4caf6a", "#ef6fa6", "#f39237", "#8e5bd0"
WOOD, WOOD_D, WOOD_L = "#c98b52", "#8a5a30", "#e2ad72"
NAVY = "#2b2d5c"
PAPER = "#fdf6e9"


def blob(W, H, x, y, r, rng, k=0.18):
    return shapes(W, H, [deform(ellipse_pts(x, y, r, r * rng.uniform(0.75, 0.95), 12, rng.uniform(0, 3)), rng, 2, k)])


def thick_paint(art, m, col, nx, light=None):
    """Fat gouache blob: opaque body, a lighter wet highlight up-left, darker rim down-right."""
    light = light or mix(col, "#ffffff", 0.45)
    art = GP(art, m, col, mix(col, "#000000", 0.08), seed=nx(), rough=1.2, streak=0.8)
    art = relief(art, m, 2.5, 0.45, light=light, dark=mix(col, "#000000", 0.45), seed=nx())
    hi = np.clip(np.roll(np.roll(gaussian_filter(m, 2), -3, 0), -3, 1) - (1 - m) * 2, 0, 1) * np.clip(gaussian_filter(m, 6) * 2 - 1.2, 0, 1)
    return wash(art, hi, "#ffffff", 0.5, seed=nx())


if "paper" in PARTS:
    im = paper(320, 320, PAPER, seed=41, fiber=0.6, mottle=0.6)
    arr = np.asarray(im, np.float32) / 255
    arr = np.concatenate([arr, np.ones((320, 320, 1), np.float32)], -1)
    # cold-press tooth (tileable)
    tooth = wrap_noise(320, 320, 42, 1.2)
    arr[..., :3] *= (0.96 + 0.08 * tooth)[..., None]
    arr = tileable(arr) if "tileable" in globals() else arr
    save_rgb(arr, f"{OUT}/paper.webp", quality=82)

if "easel" in PARTS:
    W, H = 560, 700
    nx = Seq(4100); rng = random.Random(41)
    art = blank(W, H)
    # legs (A-frame) + back leg
    legs = strokes(W, H, [([(150, 690), (250, 40)], 22, None), ([(410, 690), (310, 40)], 22, None)])
    back = strokes(W, H, [([(280, 60), (280, 670)], 16, None)])
    art = GP(art, back, WOOD_D, "#7a4e28", seed=nx(), rough=1.2)
    art = GP(art, legs, WOOD, WOOD_L, seed=nx(), rough=1.4, streak=1.4)
    art = wash(art, np.clip(legs - np.roll(legs, -4, 1), 0, 1), WOOD_D, 0.6, seed=nx())
    top = shapes(W, H, [[(236, 30), (324, 30), (330, 56), (230, 56)]], smooth=False)
    art = GP(art, top, WOOD_L, WOOD, seed=nx(), rough=0.8)
    # canvas: stretched, cream, with a soft shadow and a few test dabs at the edges
    cv = shapes(W, H, [[(96, 92), (464, 84), (470, 440), (90, 446)]], smooth=False)
    art = over(art, soft_shadow(cv, "#5a3a20", 10, 0.45, 8, 10))
    art = GP(art, cv, "#fffaf0", "#f7efe0", seed=nx(), rough=0.8, streak=0.12)
    art = wash(art, np.clip(cv - gaussian_filter(cv, 4), 0, 1) * 3, "#d8c8a8", 0.6, seed=nx())
    for (x, y, r, c) in [(118, 112, 12, RED), (444, 104, 9, YEL), (452, 420, 14, BLUE), (112, 426, 8, GRN), (136, 118, 6, PINK)]:
        art = thick_paint(art, blob(W, H, x, y, r, rng) * cv, c, nx)
    # brush stroke swooshes peeking from the canvas corners
    for pts, c, w in [([(108, 160), (150, 132), (196, 120)], ORA, 12), ([(440, 360), (452, 392), (432, 424)], PUR, 10)]:
        art = GP(art, strokes(W, H, [(curve(pts, 20), w, (0.05, 0.5))]) * cv, c, seed=nx(), rough=1.0, streak=1.6)
    # ledge
    ledge = shapes(W, H, [[(60, 446), (500, 440), (504, 474), (56, 480)]], smooth=False)
    art = GP(art, ledge, WOOD, WOOD_L, seed=nx(), rough=0.8, streak=1.3)
    art = wash(art, np.clip(ledge - np.roll(ledge, -5, 0), 0, 1), WOOD_D, 0.6, seed=nx())
    # drips of paint running down the ledge
    for x, c in [(150, RED), (330, BLUE), (420, YEL)]:
        e = 500 + rng.uniform(0, 30)
        d = np.clip(strokes(W, H, [([(x, 462), (x + 1, e)], 7, None)]) + circles(W, H, [(x + 1, e + 2, 6.5)]), 0, 1)
        art = thick_paint(art, d, c, nx)
    art = keep_pixel(art, 0, 0); art = keep_pixel(art, W - 1, H - 1)
    show(art, "um-easel")
    save_full(art, f"{OUT}/easel.webp", size=(400, 500), quality=82)
    clr()

if "palette" in PARTS:
    W, H = 520, 380
    nx = Seq(4200); rng = random.Random(42)
    art = blank(W, H)
    pts = [(40, 200), (70, 90), (190, 40), (340, 44), (470, 110), (490, 220), (430, 320), (300, 350), (210, 300), (150, 330), (70, 300)]
    pal = shapes(W, H, [deform(pts, rng, 1, 0.01)])
    hole = shapes(W, H, [ellipse_pts(150, 250, 34, 28, 20)])
    pal = np.clip(pal - hole, 0, 1)
    art = over(art, soft_shadow(pal, "#5a3a20", 8, 0.4, 6, 9))
    art = GP(art, pal, WOOD_L, WOOD, seed=nx(), rough=1.0, streak=1.6)
    grain = strokes(W, H, [(curve([(60, 120 + k * 22), (260, 100 + k * 22 + rng.uniform(-8, 8)), (470, 130 + k * 20)], 30), 1.2, (0.2, 0.2)) for k in range(10)]) * pal
    art = wash(art, grain, WOOD_D, 0.35, seed=nx())
    art = relief(art, pal, 6, 0.35, light="#f6d6a6", dark="#6a4020", seed=nx())
    for (x, y, r, c) in [(120, 130, 30, RED), (205, 88, 28, YEL), (300, 82, 30, GRN), (390, 120, 28, BLUE), (430, 215, 26, PUR), (350, 280, 26, PINK), (250, 200, 24, ORA), (260, 284, 18, "#ffffff")]:
        art = thick_paint(art, blob(W, H, x, y, r, rng), c, nx)
    # a mixed smear
    sm = strokes(W, H, [(curve([(300, 190), (340, 200), (380, 186)], 20), 14, (0.1, 0.5))])
    art = GP(art, sm, mix(BLUE, YEL, 0.5), seed=nx(), rough=1.0, streak=2.0)
    # brush lying across
    handle = strokes(W, H, [([(80, 360), (300, 228)], 13, (0.0, 0.6))])
    art = GP(art, handle, RED, "#c83a2e", seed=nx(), rough=0.6)
    art = wash(art, np.clip(handle - np.roll(handle, 3, 0), 0, 1), "#ffffff", 0.4, seed=nx())
    ferrule = strokes(W, H, [([(300, 228), (330, 210)], 13, None)])
    art = GP(art, ferrule, "#c8c8d0", "#9a9aa8", seed=nx(), rough=0.4)
    tip = shapes(W, H, [[(328, 202), (336, 218), (372, 196), (366, 186)]])
    art = GP(art, tip, "#3a2a20", seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, [[(356, 192), (372, 196), (368, 186)]]), BLUE, seed=nx(), rough=0.4)
    show(art, "um-palette")
    save(art, f"{OUT}/palette.webp", max_w=360, quality=82)
    clr()

if "jar" in PARTS:
    W, H = 300, 420
    nx = Seq(4300); rng = random.Random(43)
    art = blank(W, H)
    # brushes behind
    for (x0, x1, y1, c, tipc) in [(130, 80, 40, YEL, RED), (150, 160, 20, BLUE, YEL), (168, 230, 50, GRN, PINK), (140, 120, 70, PUR, BLUE)]:
        h = strokes(W, H, [([(x0, 300), (x1, y1 + 40)], 11, (0.0, 0.3))])
        art = GP(art, h, c, mix(c, "#000000", 0.1), seed=nx(), rough=0.6)
        ang = math.atan2(y1 + 40 - 300, x1 - x0)
        fx, fy = x1 + math.cos(ang) * 18, y1 + 40 + math.sin(ang) * 18
        art = GP(art, strokes(W, H, [([(x1, y1 + 40), (fx, fy)], 11, None)]), "#c8c8d0", seed=nx(), rough=0.4)
        tip = shapes(W, H, [petal_pts(fx, fy, 34, 8, ang, n=12)])
        art = GP(art, tip, tipc, mix(tipc, "#000000", 0.2), seed=nx(), rough=0.8)
    jar = shapes(W, H, [[(70, 240), (230, 240), (240, 400), (60, 400)]], smooth=True)
    water = shapes(W, H, [[(66, 300), (234, 296), (240, 400), (60, 400)]], smooth=True)
    art = wash(art, jar, "#cfe6f2", 0.55, seed=nx())
    art = wash(art, water * jar, "#7ab0d8", 0.55, seed=nx(), col2="#9a8ad0")
    art = wash(art, np.clip(jar - gaussian_filter(jar, 3), 0, 1) * 3, "#ffffff", 0.8, seed=nx())
    art = wash(art, strokes(W, H, [([(88, 260), (84, 380)], 7, (0.2, 0.3))]), "#ffffff", 0.6, seed=nx())
    rim = strokes(W, H, [([(66, 242), (234, 242)], 8, None)])
    art = wash(art, rim, "#e8f4fa", 0.9, seed=nx())
    show(art, "um-jar")
    save(art, f"{OUT}/jar.webp", max_w=220, quality=82)
    clr()

if "crayons" in PARTS:
    W, H = 620, 120
    nx = Seq(4400); rng = random.Random(44)
    art = blank(W, H)
    cols = [RED, ORA, YEL, GRN, BLUE, PUR, PINK]
    for i, c in enumerate(cols):
        x = 40 + i * 82; y = 60 + rng.uniform(-6, 6); a = rng.uniform(-0.12, 0.12)
        body = shapes(W, H, [rot_pts([(x - 32, y - 11), (x + 22, y - 11), (x + 22, y + 11), (x - 32, y + 11)], x, y, a)], smooth=False)
        tip = shapes(W, H, [rot_pts([(x + 22, y - 10), (x + 40, y - 3), (x + 42, y + 3), (x + 22, y + 10)], x, y, a)], smooth=False)
        art = GP(art, body, c, mix(c, "#000000", 0.1), seed=nx(), rough=0.6)
        art = GP(art, tip, mix(c, "#000000", 0.08), seed=nx(), rough=0.5)
        wrap = shapes(W, H, [rot_pts([(x - 22, y - 11), (x + 10, y - 11), (x + 10, y + 11), (x - 22, y + 11)], x, y, a)], smooth=False)
        art = GP(art, wrap, mix(c, "#ffffff", 0.25), seed=nx(), rough=0.4)
        art = wash(art, strokes(W, H, [(rot_pts([(x - 18, y - 4), (x + 6, y - 4)], x, y, a), 1.6, None), (rot_pts([(x - 18, y + 4), (x + 6, y + 4)], x, y, a), 1.6, None)]), mix(c, "#000000", 0.35), 0.7, seed=nx())
        art = wash(art, np.clip(body - np.roll(body, 3, 0), 0, 1), "#ffffff", 0.35, seed=nx())
        art = wash(art, np.clip(body - np.roll(body, -3, 0), 0, 1), "#000000", 0.2, seed=nx())
    show(art, "um-crayons")
    save(art, f"{OUT}/crayons.webp", max_w=320, quality=84)
    clr()

if "splats" in PARTS:
    for name, c, seed in [("splatPink", PINK, 51), ("splatBlue", BLUE, 52), ("splatYellow", YEL, 53)]:
        W = H = 260
        nx = Seq(4500 + seed); rng = random.Random(seed)
        m = splat(W, H, 130, 130, 58, rng, drops=12, spikes=8)
        art = GP(blank(W, H), m, c, mix(c, "#000000", 0.08), seed=nx(), rough=2.0, streak=0.6)
        art = wash(art, np.clip(m - gaussian_filter(m, 3), 0, 1) * 2, mix(c, "#000000", 0.25), 0.4, seed=nx())
        art = wash(art, np.clip(gaussian_filter(m, 8) * 2 - 1.1, 0, 1) * np.clip((fbm(W, H, nx(), 20, 2) - 0.4) * 2, 0, 1), mix(c, "#ffffff", 0.35), 0.4, seed=nx())
        show(art, f"um-{name}")
        save(art, f"{OUT}/{name}.webp", max_w=150, quality=84)
        clr()

if "squiggle" in PARTS:
    W, H = 520, 80
    nx = Seq(4600)
    art = blank(W, H)
    for k, (c, off) in enumerate([(RED, -8), (YEL, 0), (BLUE, 8)]):
        pts = [(x, H / 2 + off + math.sin(x / 26 + k) * 12) for x in np.linspace(20, W - 20, 120)]
        m = crayon(W, H, pts, 7, seed=60 + k, grain=0.5)
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * col_arr(c), (m * 0.92)[..., None]], -1))
    show(art, "um-squiggle")
    save(art, f"{OUT}/squiggle.webp", max_w=300, quality=84)
    clr()
