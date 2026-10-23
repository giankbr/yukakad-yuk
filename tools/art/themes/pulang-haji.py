"""Pulang Haji — watercolour pieces for a homecoming tasyakuran: a white ceremonial payung with soft-green fringe and
scalloped valance (mirrored pair on the cover, sways), a still life of dates on a plate with a glass of zamzam and a
small jug, a tasbih (prayer beads) garland in pearl-white and green, a soft-green geometric (khatam) corner, a
sprig divider and a small eight-point star. No figures, no calligraphy, no holy sites.
Run: python3 -I pulang-haji.py [part ...]  parts: payung still tasbih corner divider star"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k3_lib import *

OUT = outdir("pulang-haji")
PARTS = sys.argv[1:] or ["payung", "still", "tasbih", "corner", "divider", "star"]
SAGE, SAGE_D, SAGE_L = "#8fb29a", "#5f8a72", "#cfe0d2"
GOLD = "#c8a45a"


def star8(cx, cy, r, inner=0.72, rot=0.0):
    return [(cx + math.cos(rot + k * math.pi / 8) * (r if k % 2 == 0 else r * inner), cy + math.sin(rot + k * math.pi / 8) * (r if k % 2 == 0 else r * inner)) for k in range(16)]


if "payung" in PARTS:
    W, H = 420, 540
    nx = Seq(81100); rng = random.Random(3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    cx, top, R, rim = 210, 60, 190, 190
    # canopy: shallow dome
    dome = [(cx + math.cos(a) * R, rim - math.sin(a) * (rim - top)) for a in np.linspace(0, math.pi, 50)]
    canopy = shapes(W, H, [dome])
    # pole (slight angle, it is carried)
    pole = strokes(W, H, [([(cx, top - 26), (cx + 6, H - 10)], 6, None)])
    art = G(art, pole, "#b89a6a", "#8f7448", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=1)
    art = FO(art, circles(W, H, [(cx, top - 30, 9)]) + shapes(W, H, [[(cx - 4, top - 30), (cx, top - 52), (cx + 4, top - 30)]], smooth=False), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    art = G(art, canopy, "#fbfaf4", "#eef0e6", seed=nx(), density=0.95, edge=0.9, bloom=0.3, rough=3)
    # alternate gores tinted soft green
    gores = []
    angs = np.linspace(0, math.pi, 11)
    for gi in range(0, 10, 2):
        a0, a1 = angs[gi], angs[gi + 1]
        gores.append([(cx, top + 2)] + [(cx + math.cos(a) * R, rim - math.sin(a) * (rim - top) * 0.2) for a in np.linspace(a0, a1, 8)])
    gm = shapes(W, H, gores, smooth=False) * canopy
    art = G(art, gm, SAGE_L, "#dfe9df", seed=nx(), density=0.75, edge=0.3, bloom=0.4, rough=2.5)
    # shading (light from the upper-left) and ribs
    art = G(art, canopy * np.clip((xx - cx + 40) / 200, 0, 1) * np.clip((yy - top) / 160, 0, 1), "#a9bbb0", seed=nx(), density=0.7, edge=0.1, bloom=0.4, rough=4, feather=4)
    ribs = []
    for a in np.linspace(0.12, math.pi - 0.12, 9):
        ribs.append((curve([(cx, top + 4), (cx + math.cos(a) * R * 0.55, rim - math.sin(a) * (rim - top) * 0.9 + 18), (cx + math.cos(a) * R * 0.98, rim - 2)], 24), 1.6, (0.0, 0.2)))
    art = G(art, strokes(W, H, ribs) * canopy, "#b3c4b9", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.8, feather=0.6)
    # embroidered band near the rim (soft green with gold dots)
    band = np.clip(shapes(W, H, [[(cx + math.cos(a) * R * 0.97, rim - math.sin(a) * (rim - top) * 0.97 + 4) for a in np.linspace(0, math.pi, 50)]]) - shapes(W, H, [[(cx + math.cos(a) * R * 0.88, rim - math.sin(a) * (rim - top) * 0.86 + 10) for a in np.linspace(0, math.pi, 50)]]), 0, 1) * (yy < rim)
    art = G(art, band, SAGE, SAGE_L, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.5)
    dots = [(cx + math.cos(a) * R * 0.925, rim - math.sin(a) * (rim - top) * 0.915 + 7, 2.4) for a in np.linspace(0.08, math.pi - 0.08, 28)]
    art = FO(art, circles(W, H, dots), GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
    # scalloped valance hanging from the rim
    val = []
    n = 12
    for i in range(n):
        x0 = cx - R + i * 2 * R / n; x1 = x0 + 2 * R / n
        val.append([(x0, rim - 2)] + [(x0 + (x1 - x0) * t, rim + 6 + 26 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 12)] + [(x1, rim - 2)])
    vm = shapes(W, H, val)
    art = G(art, vm, "#ffffff", "#eef1ea", seed=nx(), density=0.92, edge=0.45, bloom=0.3, rough=2)
    art = G(art, vm * np.clip((yy - rim - 10) / 20, 0, 1), "#c7d3cc", seed=nx(), density=0.4, edge=0, bloom=0.2, rough=2, feather=2)
    # fringe tassels
    fr = []
    for i in range(n):
        x = cx - R + (i + 0.5) * 2 * R / n
        for k in range(-3, 4):
            fr.append(([(x + k * 1.6, rim + 28), (x + k * 2.2 + rng.uniform(-1, 1), rim + 54 + rng.uniform(-4, 4))], 1.3, (0.0, 0.5)))
    art = G(art, strokes(W, H, fr), SAGE_D, SAGE, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    art = FO(art, circles(W, H, [(cx - R + (i + 0.5) * 2 * R / n, rim + 30, 3.2) for i in range(n)]), GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
    art = add_grain(art, seed=3, amount=0.02)
    preview(art, "ph-payung", tone="#f7f5ee")
    save(art, f"{OUT}/payung.webp", max_w=260, quality=84)
    clear()

if "still" in PARTS:
    W, H = 640, 360
    nx = Seq(81200); rng = random.Random(7)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    # soft table shadow
    art = G(art, ellipses(W, H, [(320, 318, 280, 22, 0)]), "#c9d3c9", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=6, feather=6)
    # jug (small brass-white teko for zamzam) at the back-left
    jug = shapes(W, H, [[(112, 300), (98, 250), (104, 190), (124, 160), (128, 140), (160, 140), (164, 160), (184, 190), (190, 250), (176, 300)]])
    spout = strokes(W, H, [([(186, 210), (214, 180), (226, 162)], 9, (0.0, 0.5))])
    handle = strokes(W, H, [(curve([(108, 180), (78, 200), (84, 246), (104, 262)], 20), 7, None)])
    art = G(art, handle + spout, "#d9d5c6", "#bfbba9", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, jug, "#f4f2ea", "#e2e2d6", seed=nx(), density=0.95, edge=0.5, bloom=0.3, rough=2)
    art = G(art, jug * np.clip((xx - 140) / 50, 0, 1), "#b9c2b6", seed=nx(), density=0.6, edge=0, bloom=0.3, rough=2, feather=2)
    art = G(art, strokes(W, H, [([(104, 236), (186, 236)], 6, None)]) * jug, SAGE, seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
    art = FO(art, shapes(W, H, [[(126, 142), (144, 120), (162, 142)]], smooth=False), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    # glass of zamzam water (clear, pale reflections)
    gl = shapes(W, H, [[(470, 300), (462, 196), (530, 196), (522, 300)]], smooth=False)
    water = shapes(W, H, [[(469, 300), (464, 222), (528, 222), (523, 300)]], smooth=False)
    art = G(art, gl, "#eef4f1", seed=nx(), density=0.35, edge=0.9, bloom=0.2, rough=1.2)
    art = G(art, water, "#cfe4e3", "#bcd9d8", seed=nx(), density=0.55, edge=0.6, bloom=0.4, rough=1.5)
    art = G(art, strokes(W, H, [([(476, 206), (480, 290)], 4, (0.2, 0.2))]), "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5)
    art = G(art, ellipses(W, H, [(496, 222, 32, 4, 0)]), "#a9cbcb", seed=nx(), density=0.6, edge=0.4, bloom=0, rough=0.8)
    # plate (oval, white with green rim)
    plate = ellipses(W, H, [(318, 292, 160, 30, 0)])
    rim_ = np.clip(plate - ellipses(W, H, [(318, 290, 146, 24, 0)]), 0, 1)
    art = G(art, plate, "#fbfbf6", "#eef0e8", seed=nx(), density=0.95, edge=0.4, bloom=0.2, rough=2)
    art = G(art, rim_, SAGE, SAGE_L, seed=nx(), density=0.7, edge=0.4, bloom=0.2, rough=1.2)
    # dates: glossy dark-amber ovals piled
    piles = []
    for row, (y, n_, spread) in enumerate([(282, 9, 120), (262, 7, 92), (244, 5, 64), (228, 3, 36)]):
        for i in range(n_):
            x = 318 - spread + 2 * spread * i / max(1, n_ - 1) + rng.uniform(-5, 5)
            piles.append((x, y + rng.uniform(-4, 4), rng.uniform(18, 22), rng.uniform(10, 12), rng.uniform(-35, 35)))
    for (x, y, rx, ry, rot) in piles:
        m = ellipses(W, H, [(x, y, rx, ry, rot)])
        art = G(art, m, "#7a3b1c", "#5a2810", seed=nx(), density=0.95, edge=0.6, bloom=0.15, rough=1.0, pad=10)
        art = G(art, ellipses(W, H, [(x - rx * 0.25, y - ry * 0.35, rx * 0.45, ry * 0.25, rot)]), "#c9864c", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, pad=8)
        art = G(art, strokes(W, H, [([(x - rx * 0.5, y + ry * 0.1), (x + rx * 0.4, y + ry * 0.3)], 1.0, None)]), "#3a1808", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.3, feather=0.3, pad=8)
    clear()
    # a couple of loose dates + a sprig of leaves at the front right
    for (x, y, rot) in [(560, 314, 20), (590, 306, -15)]:
        art = G(art, ellipses(W, H, [(x, y, 17, 9, rot)]), "#7a3b1c", "#5a2810", seed=nx(), density=0.95, edge=0.6, bloom=0.15, rough=1, pad=10)
        art = G(art, ellipses(W, H, [(x - 4, y - 3, 7, 2.5, rot)]), "#c9864c", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, pad=8)
    art = add_grain(art, seed=5, amount=0.02)
    preview(art, "ph-still", tone="#f7f5ee")
    save(art, f"{OUT}/still.webp", max_w=560, quality=82)
    clear()

if "tasbih" in PARTS:
    W, H = 720, 240
    nx = Seq(81300)
    art = blank(W, H)
    # a drooping loop of 33 beads + an imam bead and tassel at the centre
    pts = [(20 + (W - 40) * t, 40 + 120 * (1 - (2 * t - 1) ** 2)) for t in np.linspace(0, 1, 200)]
    cord = strokes(W, H, [(pts, 1.6, None)])
    art = G(art, cord, "#8e9f93", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    L = sum(math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) for i in range(1, len(pts)))
    beads = along(pts, L / 34)
    for i, bp in enumerate(beads):
        x, y = bp[0], bp[1]
        if abs(i - len(beads) // 2) < 1:
            continue
        r = 9.5
        col = ("#f4f1e8", "#d9d7cc") if i % 11 else (SAGE, SAGE_D)
        m = circles(W, H, [(x, y, r)])
        art = G(art, soft_shadow(m, "#5d6b62", 3, 1.0, 2, 3)[..., 3] * 0.5, "#7d8a80", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.5, pad=10)
        art = G(art, m, *col, seed=nx(), density=0.97, edge=0.55, bloom=0.1, rough=0.6, pad=8)
        art = G(art, circles(W, H, [(x + 2.5, y + 2.8, r * 0.75)]) * m, "#9aa79e", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5, feather=1.2, pad=8)
        art = G(art, circles(W, H, [(x - 2.6, y - 2.8, 2.4)]), "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.2, pad=6)
        if i % 4 == 0:
            clear()
    cx, cy = W / 2, 160
    art = FO(art, shapes(W, H, [[(cx - 6, cy), (cx, cy + 22), (cx + 6, cy)]], smooth=False) + circles(W, H, [(cx, cy, 9)]), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    tas = strokes(W, H, [([(cx + k * 1.2, cy + 22), (cx + k * 2.4, cy + 66)], 1.2, (0.0, 0.4)) for k in range(-5, 6)])
    art = G(art, tas, SAGE_D, SAGE, seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5, feather=0.4)
    preview(art, "ph-tasbih", tone="#f7f5ee")
    save(art, f"{OUT}/tasbih.webp", max_w=600, quality=82)
    clear()

if "corner" in PARTS:
    W = H = 360
    nx = Seq(81400)
    art = blank(W, H)
    # khatam (8-point star) lattice fading from the corner, soft green wash + thin gold
    polys = []
    s = 64
    for j in range(0, 6):
        for i in range(0, 6):
            if i + j > 5:
                continue
            polys.append(star8(i * s + 32, j * s + 32, 26, 0.74, math.pi / 8))
    m = shapes(W, H, polys, smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(1 - (xx + yy) / 400, 0, 1)
    art = G(art, m * fade, SAGE, SAGE_L, seed=nx(), density=0.75, edge=0.6, bloom=0.4, rough=2.5)
    ring = np.clip(gaussian_filter(m, 1.2) - (gaussian_filter(m, 1.2) > 0.98).astype(np.float32), 0, 1)
    art = FO(art, np.clip(ring * 1.5, 0, 1) * fade, GOLD, seed=nx(), emboss=0.3, sparkle=0.05)
    preview(art, "ph-corner", tone="#f7f5ee")
    save(art, f"{OUT}/corner.webp", max_w=220, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 400, 60
    nx = Seq(81500)
    art = blank(W, H)
    art = G(art, strokes(W, H, [([(30, 30), (160, 30)], 1.6, (0.7, 0.0)), ([(240, 30), (370, 30)], 1.6, (0.0, 0.7))]), SAGE_D, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
    for sgn in (-1, 1):
        for k in range(3):
            x = 200 + sgn * (40 + k * 22)
            art = G(art, shape_mask(W, H, petal_pts(x - sgn * 8, 30, 24, 6, (0 if sgn > 0 else math.pi) + (-0.5 if k % 2 else 0.5), n=12)), SAGE, SAGE_D, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.0, pad=18)
    art = FO(art, shapes(W, H, [star8(200, 30, 15, 0.7)], smooth=False), GOLD, seed=nx(), emboss=0.6, sparkle=0.12)
    preview(art, "ph-divider", tone="#f7f5ee")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)

if "star" in PARTS:
    W = H = 140
    nx = Seq(81600)
    art = blank(W, H)
    art = G(art, shapes(W, H, [star8(70, 70, 60, 0.72)], smooth=False), SAGE, SAGE_L, seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.5)
    art = FO(art, np.clip(shapes(W, H, [star8(70, 70, 48, 0.72)], smooth=False) - shapes(W, H, [star8(70, 70, 42, 0.72)], smooth=False), 0, 1), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    art = G(art, circles(W, H, [(70, 70, 12)]), "#ffffff", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.6)
    preview(art, "ph-star", tone="#f7f5ee")
    save(art, f"{OUT}/star.webp", max_w=70, quality=84)

kb(OUT)
