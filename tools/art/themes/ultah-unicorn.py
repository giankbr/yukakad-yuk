"""Ultah Unicorn — kids birthday with Lulu, an original chubby pastel unicorn (gouache): pearly body with lilac shade,
a six-colour pastel mane and tail, a candy-striped horn, a happy closed-eye smile. Plus a soft pastel rainbow, cotton-candy
clouds and puffy butter stars. Run: python3 -I ultah-unicorn.py [part ...]  parts: unicorn rainbow cloud star
Assets -> public/themes/art/ultah-unicorn/ (unicorn.webp + head.webp crop)"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c5_lib import *

OUT = outdir("ultah-unicorn")
PARTS = sys.argv[1:] or ["unicorn", "rainbow", "cloud", "star"]
INK = "#6a4f8c"
BODY, BODY2, SHADE, LIGHT = "#fffaf7", "#fbf2f6", "#d9cdf0", "#ffffff"
MANE = ["#f7a8c8", "#ffc6a5", "#fff0a6", "#bdeed8", "#b9dcff", "#d4c1f5"]
HOOF = ("#c7b3ef", "#a891e0")
BG = "#fdf6fb"


def ell(W, H, cx, cy, rx, ry, rot, rng, n=18, d=0.015):
    return shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, n, rot), rng, 1, d)])


def lock(c0, c1, c2, n=30):
    return curve([c0, c1, c2], n)


if "unicorn" in PARTS:
    W, H = 640, 620
    nx = Seq(70100); rng = random.Random(71)
    art = blank(W, H)
    # ground shadow
    art = G(art, ell(W, H, 330, 588, 200, 16, 0, rng), "#b9a6dc", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=5)
    # tail: rainbow locks curling up behind the rump
    tail = []
    for i, col in enumerate(MANE):
        o = (i - 2.5) * 14
        tail.append((curve([(470, 384 + o * 0.3), (536 + o * 0.4, 356 + o), (586 + o * 0.5, 420 + o * 0.6), (566 + o * 0.6, 494 + o * 0.4), (520 + o * 0.5, 520 + o * 0.3)], 40), 20, col))
    for pts, w, col in tail:
        m = strokes(W, H, [(pts, w, (0.05, 0.55))])
        art = body(art, m, col, mix(col, "#ffffff", 0.25), mix(col, INK, 0.25), "#ffffff", nx, ldir=(-6, -6), blur=4)
    # far legs (shaded)
    legs_b = strokes(W, H, [([(x, 440), (x + 2, 552)], 46, None) for x in (282, 450)])
    art = body(art, legs_b, "#efe6f7", "#e9def5", "#c6b6ea", BODY, nx, line=INK)
    art = body(art, strokes(W, H, [([(x - 6, 560), (x + 8, 560)], 44, None) for x in (284, 452)]), HOOF[1], HOOF[1], "#8f78cf", HOOF[0], nx, line=INK)
    # near legs (behind the belly line)
    legs = strokes(W, H, [([(x, 450), (x + 2, 556)], 50, None) for x in (318, 488)])
    art = body(art, legs, BODY, BODY2, SHADE, LIGHT, nx, line=INK)
    hooves = strokes(W, H, [([(x - 8, 566), (x + 10, 566)], 46, None) for x in (320, 490)])
    art = body(art, hooves, HOOF[0], HOOF[0], HOOF[1], "#e6dbfb", nx, line=INK)
    # body + neck + head
    torso = ell(W, H, 370, 420, 150, 100, -0.05, rng)
    neck = shapes(W, H, [[(222, 300), (300, 250), (330, 380), (262, 430), (226, 400)]])
    head = ell(W, H, 210, 230, 92, 82, -0.25, rng)
    snout = ell(W, H, 150, 286, 64, 48, -0.35, rng)
    full = np.clip(torso + neck + head + snout, 0, 1)
    art = body(art, full, BODY, BODY2, SHADE, LIGHT, nx, ldir=(-14, -16), line=INK, blur=10)
    # muzzle blush + nostril
    art = G(art, ell(W, H, 132, 300, 30, 22, -0.3, rng), "#f8c3d6", seed=nx(), density=0.45, edge=0.15, bloom=0, rough=2, feather=3)
    art = OV(art, ell(W, H, 116, 286, 4.5, 3.2, -0.4, rng), lambda m: col_arr(m, INK, m * 0.75), pad=6)
    # happy closed eye with lashes, cheek
    eye = strokes(W, H, [(arc_pts(214, 222, 17, 0.25, 2.9, 16), 4.2, (0.1, 0.1))])
    lashes = strokes(W, H, [([(199, 230), (190, 238)], 3, None), ([(207, 236), (202, 246)], 3, None), ([(218, 239), (217, 250)], 3, None)])
    art = crayon(art, np.clip(eye + lashes, 0, 1), INK, seed=nx(), amt=0.95, tooth=0.15)
    art = G(art, ell(W, H, 232, 262, 20, 13, 0, rng), "#f6a7c4", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=2, feather=3)
    smile = strokes(W, H, [(arc_pts(148, 300, 18, 0.35, 1.7, 12), 3.2, (0.2, 0.2))])
    art = crayon(art, smile, INK, seed=nx(), amt=0.85)
    # ear
    ear = shapes(W, H, [[(244, 168), (282, 128), (276, 186)]])
    art = body(art, ear, BODY, BODY2, SHADE, LIGHT, nx, line=INK, blur=4)
    art = GP(art, shapes(W, H, [[(254, 168), (276, 142), (272, 178)]]), "#f8c3d6", seed=nx(), rough=0.6, pad=6)
    # horn: candy spiral, butter + peach stripes
    horn = shapes(W, H, [[(182, 162), (214, 152), (176, 46)]], smooth=False)
    art = body(art, horn, "#fff0b8", "#ffe7a0", "#f2c46e", "#fffbe6", nx, line="#c99a45", blur=4)
    stripes = strokes(W, H, [([(178 + t * 0.9, 150 - t * 3.2), (204 + t * 0.2, 142 - t * 3.2)], 3.5, None) for t in (0, 9, 18, 26)]) * horn
    art = GP(art, stripes, "#ffb59a", seed=nx(), rough=0.4, pad=6)
    # mane: rainbow locks flowing down the neck
    for i, col in enumerate(MANE):
        o = i * 13
        pts = curve([(250 - o * 0.2, 150 + o * 0.6), (300 + o * 0.5, 170 + o * 0.9), (318 + o * 0.6, 240 + o), (296 + o * 0.3, 312 + o * 0.6), (318 + o * 0.4, 360 + o * 0.3)], 40)
        m = strokes(W, H, [(pts, 26 - i * 1.2, (0.08, 0.55))])
        art = body(art, m, col, mix(col, "#ffffff", 0.3), mix(col, INK, 0.22), "#ffffff", nx, ldir=(-6, -6), blur=4)
    # forelock over the brow
    for i, col in enumerate(MANE[:3]):
        pts = curve([(236 + i * 6, 150 + i * 2), (206 - i * 4, 158 + i * 6), (190 - i * 6, 190 + i * 4)], 24)
        m = strokes(W, H, [(pts, 16 - i * 2, (0.05, 0.6))])
        art = body(art, m, col, mix(col, "#ffffff", 0.3), mix(col, INK, 0.22), "#ffffff", nx, ldir=(-4, -4), blur=3)
    # little star on the hip
    sp = [(420 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 10), 400 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 10)) for k in range(10)]
    art = GP(art, shapes(W, H, [sp]), "#ffd6e6", "#ffc6dc", seed=nx(), rough=0.6, pad=6)
    preview(art, "uu-unicorn", tone=BG)
    save(art, f"{OUT}/unicorn.webp", max_w=420, quality=82)
    # head crop for the portrait peek
    crop = np.ascontiguousarray(art[30:420, 70:360])
    save(crop, f"{OUT}/head.webp", max_w=200, quality=84)
    clear()

if "rainbow" in PARTS:
    W, H = 900, 500
    nx = Seq(70200); rng = random.Random(72)
    art = blank(W, H)
    cx, cy = W / 2, 470
    cols = ["#f7a8c8", "#ffc6a5", "#fff0a6", "#bdeed8", "#b9dcff", "#d4c1f5"]
    r0, bw = 400, 34
    for i, col in enumerate(cols):
        r = r0 - i * bw
        band = np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - bw + 1)]), 0, 1)
        band[int(cy):] = 0
        art = GP(art, band, col, mix(col, "#ffffff", 0.2), seed=nx(), rough=2.2, streak=0.9)
        art = tint(art, side_light(band, 0, 6, 4), mix(col, "#ffffff", 0.6), 0.45, seed=nx())
    clear()
    # cotton clouds hiding both feet
    for bx in (cx - r0 + 80, cx + r0 - 80):
        lobes = [(bx - 70, 440, 54), (bx - 10, 410, 70), (bx + 66, 436, 56), (bx + 20, 456, 60), (bx - 40, 462, 50)]
        m = circles(W, H, lobes)
        art = body(art, m, "#fffafd", "#fdf0f7", "#ead9f3", "#ffffff", nx, ldir=(0, -14), blur=10)
    preview(art, "uu-rainbow", tone=BG)
    save(art, f"{OUT}/rainbow.webp", max_w=760, quality=80)
    clear()

if "cloud" in PARTS:
    W, H = 480, 280
    nx = Seq(70300); rng = random.Random(73)
    art = blank(W, H)
    lobes = [(130, 170, 70), (210, 120, 86), (300, 140, 74), (370, 180, 56), (240, 190, 80), (90, 200, 44)]
    m = circles(W, H, lobes)
    art = body(art, m, "#ffd9ea", "#e8d6fb", "#d6b9ef", "#fff3fa", nx, ldir=(4, -16), blur=12)
    # candy floss wisps: soft lighter swirls
    wisps = strokes(W, H, [(arc_pts(200, 150, 40, 3.4, 5.4, 20), 6, (0.3, 0.3)), (arc_pts(300, 160, 30, 3.6, 5.6, 16), 5, (0.3, 0.3)), (arc_pts(140, 185, 26, 3.3, 5.2, 14), 4, (0.3, 0.3))])
    art = tint(art, gaussian_filter(wisps, 1.5) * m, "#ffffff", 0.55, seed=nx())
    preview(art, "uu-cloud", tone=BG)
    save(art, f"{OUT}/cloud.webp", max_w=220, quality=84)
    clear()

if "star" in PARTS:
    W, H = 200, 200
    nx = Seq(70400); rng = random.Random(74)
    art = blank(W, H)
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 84 if k % 2 == 0 else 42
        pts.append((100 + math.cos(a) * r, 106 + math.sin(a) * r))
    # round the points: smooth path through them gives a puffy star
    m = shapes(W, H, [pts])
    m = np.clip((gaussian_filter(m, 4) - 0.35) * 3, 0, 1)
    art = body(art, m, "#ffe28a", "#ffd56e", "#f2b04e", "#fff6c8", nx, ldir=(-8, -8), line="#d9963a", blur=6)
    art = OV(art, ell(W, H, 80, 84, 9, 5, -0.6, rng), lambda mm: col_arr(mm, "#ffffff", mm * 0.8), pad=6)
    preview(art, "uu-star", tone=BG)
    save(art, f"{OUT}/star.webp", max_w=64, quality=86)
    clear()
