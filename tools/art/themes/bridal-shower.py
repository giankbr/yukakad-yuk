"""Bridal Shower — loose watercolour with a fine pen line and rose-gold foil (original designs): two champagne flutes
clinking with pink bubbly and a satin bow, a blush silk robe on a wooden hanger with lace lapels, a corner bouquet of
garden roses with trailing ribbons, a satin "Bride to Be" sash (lettering is typeset in CSS), champagne bubbles and a
ribbon-bow divider.
Run: python3 -I bridal-shower.py [part ...]  parts: glasses robe roses sash bubbles bow
Assets -> public/themes/art/bridal-shower/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e6_lib import *

OUT = outdir("bridal-shower")
PARTS = sys.argv[1:] or ["glasses", "robe", "roses", "sash", "bubbles", "bow"]
PEN = "#7a4a5a"
BLUSH, BLUSH2, ROSE, ROSE_D = "#f6c9d0", "#fbe3e6", "#e88aa0", "#b8506e"
CHAMP, CHAMP2 = "#f7c6b8", "#fbe0c8"
RG = "#d29a86"  # rose gold
SAGE_A, SAGE_B = "#a9bf9a", "#6e8c66"


def flute(W, H, bx, by, ang, s=1.0):
    """Champagne flute outline (bowl, stem, foot) as polygons rotated around (bx, by) = foot centre."""
    bowl = [(-26, -150), (-30, -220), (-27, -290), (27, -290), (30, -220), (26, -150), (8, -128), (-8, -128)]
    stem = [(-4, -130), (4, -130), (4, -16), (-4, -16)]
    foot = ellipse_pts(0, -8, 40, 9, 16)
    liquid = [(-25, -160), (-29, -220), (-27, -262), (27, -262), (29, -220), (25, -160), (8, -136), (-8, -136)]
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda pts: [(bx + (x * ca - y * sa) * s, by + (x * sa + y * ca) * s) for x, y in pts]
    return T(bowl), T(stem), T(foot), T(liquid), T


if "glasses" in PARTS:
    W, H = 560, 640
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    for k, (bx, ang) in enumerate(((124, 0.24), (436, -0.24))):
        bowl, stem, foot, liquid, T = flute(W, H, bx, 610, ang, 1.7)
        g = shapes(W, H, [bowl, stem], smooth=False)
        gm = np.maximum(shapes(W, H, [bowl]), np.maximum(shapes(W, H, [stem], smooth=False), shapes(W, H, [foot])))
        art = wash(art, gm, "#eef1f4", "#ffffff", nx=nx, dens=0.35)
        lq = shapes(W, H, [liquid])
        art = G(art, lq, CHAMP, "#f4a9b4", seed=nx(), density=0.75, edge=0.6, bloom=0.45, rough=2.5)
        art = G(art, inner_shade(lq, 8 if k == 0 else -8, 0, 10), ROSE, seed=nx(), density=0.4, edge=0.3, bloom=0.2, rough=2)
        # bubbles inside
        for _ in range(16):
            t = rng.random()
            px, py = T([(rng.uniform(-18, 18), -140 - t * 115)])[0]
            art = bubble(art, W, H, px, py, rng.uniform(3.5, 7), nx, rim="#fffaf4", dens=0.95)
        # glass highlight streak
        hl = strokes(W, H, [(T([(-19, -170), (-22, -230), (-20, -280)]), 5, (0.3, 0.3))])
        art = G(art, hl, "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5)
        art = pen(art, gm, nx, col="#8a7a86", w=1.8, dens=0.55)
        clear()
    # foam splash where the rims meet
    spl = []
    for _ in range(26):
        a = rng.uniform(math.pi * 1.05, math.pi * 1.95); d = rng.uniform(16, 70)
        spl.append((280 + math.cos(a) * d * 1.2, 120 + math.sin(a) * d * 0.9, rng.uniform(2, 7)))
    sp = circles(W, H, spl)
    art = G(art, sp, CHAMP2, "#ffd3dc", seed=nx(), density=0.75, edge=0.6, bloom=0.2, rough=1.5)
    for x, y, r in ((230, 50, 9), (330, 36, 12), (282, 18, 7), (360, 80, 6), (200, 90, 5)):
        art = bubble(art, W, H, x, y, r, nx, rim=ROSE, tint=BLUSH2, dens=0.6)
    # satin bow tying the stems together
    bx, by = 166, 446
    tie = shapes(W, H, [ellipse_pts(bx - 30, by - 8, 32, 15, 14, -0.6), ellipse_pts(bx + 30, by - 8, 32, 15, 14, 0.6)])
    art = satin(art, tie, ROSE, "#f19bb0", nx, angle=0.9, freq=10, sheen=0.55)
    tails = shapes(W, H, [ribbon_band(W, H, curve([(bx - 4, by + 4), (bx - 30, by + 50), (bx - 22, by + 100), (bx - 44, by + 140)], 24), 12), ribbon_band(W, H, curve([(bx + 6, by + 4), (bx + 30, by + 46), (bx + 56, by + 80), (bx + 50, by + 124)], 24), 12)])
    art = satin(art, tails, ROSE, "#f19bb0", nx, angle=1.4, freq=8, sheen=0.5)
    knot = circles(W, H, [(bx, by, 11)])
    art = satin(art, knot, ROSE_D, ROSE, nx, freq=6, sheen=0.4)
    art = pen(art, np.maximum(np.maximum(tie, tails), knot), nx, col=PEN, w=1.6, dens=0.5)
    preview(art, "bs-glasses", tone="#fdf3f1")
    save(art, f"{OUT}/glasses.webp", max_w=360, quality=82)
    clear()

if "robe" in PARTS:
    W, H = 520, 680
    nx = Seq(300); rng = random.Random(3)
    art = blank(W, H)
    # hook + hanger
    hook = strokes(W, H, [(curve([(260, 92), (260, 60), (276, 36), (296, 44), (294, 62)], 20), 5, None)])
    art = FO(art, hook, RG, seed=nx(), emboss=0.6, sparkle=0.2)
    hanger = shapes(W, H, [[(70, 148), (260, 88), (450, 148), (444, 160), (260, 104), (76, 160)]])
    art = wash(art, hanger, "#c79a72", "#a8774f", nx=nx, dens=0.85, shade=(0, 1), k=4)
    art = pen(art, hanger, nx, col="#6a4630", w=1.6)
    # robe body (behind sleeves)
    hem = [(410, 640), (330, 652), (260, 646), (190, 652), (110, 640)]
    body = shapes(W, H, [[(150, 140), (210, 116), (260, 160), (310, 116), (370, 140), (380, 300), (382, 400)] + hem + [(138, 400), (140, 300)]], smooth=False)
    art = wash(art, body, BLUSH, BLUSH2, nx=nx, dens=0.75, shade=(1, 0), k=24, sh_col="#a0506e")
    # silk folds
    folds = strokes(W, H, [(curve([(200, 400), (196, 520), (186, 646)], 20), 7, (0.3, 0.3)), (curve([(320, 410), (330, 530), (344, 646)], 20), 8, (0.3, 0.3)),
                           (curve([(262, 470), (264, 560), (262, 646)], 16), 5, (0.3, 0.3))])
    art = G(art, folds, mix(ROSE, "#ffffff", 0.2), seed=nx(), density=0.45, edge=0.4, bloom=0.3, rough=2)
    shine = strokes(W, H, [(curve([(176, 420), (170, 540), (160, 640)], 16), 6, (0.3, 0.3)), (curve([(292, 430), (300, 550), (304, 640)], 16), 5, (0.3, 0.3))])
    art = G(art, shine, "#ffffff", seed=nx(), density=0.7, edge=0, bloom=0.2, rough=1.5)
    # kimono sleeves
    sl = shapes(W, H, [[(150, 142), (90, 200), (40, 370), (112, 392), (140, 300)], [(370, 142), (430, 200), (480, 370), (408, 392), (380, 300)]])
    art = wash(art, sl, BLUSH, BLUSH2, nx=nx, dens=0.8, shade=(-1, 0), k=16, sh_col="#a0506e")
    cuffs = shapes(W, H, [[(40, 370), (112, 392), (108, 410), (36, 388)], [(480, 370), (408, 392), (412, 410), (484, 388)]], smooth=False)
    art = GP(art, cuffs, "#fffaf6", "#f3e8e2", seed=nx(), rough=1)
    # lace lapels: a scalloped white band down the front
    lap_l = ribbon_band(W, H, curve([(212, 120), (240, 220), (258, 330), (262, 420)], 30), 24)
    lap_r = ribbon_band(W, H, curve([(308, 120), (282, 220), (266, 330), (262, 420)], 30), 24)
    lap = shapes(W, H, [lap_l, lap_r])
    art = GP(art, lap, "#fffaf6", "#f6ece6", seed=nx(), rough=1.2, streak=0.3)
    sc = []
    for side in (curve([(222, 124), (252, 220), (270, 330), (274, 420)], 30), curve([(298, 124), (270, 220), (254, 330), (250, 420)], 30)):
        for (x, y) in side[::2]:
            sc.append((x, y, 4.2))
    lace = circles(W, H, sc)
    art = G(art, lace, "#e9d4cf", seed=nx(), density=0.45, edge=0.6, bloom=0, rough=0.8)
    dotsl = circles(W, H, [(x + rng.uniform(-6, 6), y, 1.4) for (x, y, _) in sc[::2]]) * lap
    art = G(art, dotsl, "#c9a9a6", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    # belt + bow
    belt = shapes(W, H, [[(138, 400), (382, 396), (384, 426), (136, 430)]])
    art = satin(art, belt, ROSE, "#f19bb0", nx, angle=0.2, freq=9, sheen=0.5)
    loops = shapes(W, H, [ellipse_pts(232, 418, 32, 16, 12, -0.4), ellipse_pts(296, 418, 32, 16, 12, 0.4)])
    art = satin(art, loops, ROSE, "#f19bb0", nx, angle=0.8, freq=7, sheen=0.5)
    ends = shapes(W, H, [ribbon_band(W, H, curve([(258, 426), (244, 490), (232, 560)], 14), 15), ribbon_band(W, H, curve([(270, 426), (290, 496), (302, 552)], 14), 15)])
    art = satin(art, ends, ROSE, "#f19bb0", nx, angle=1.4, freq=7, sheen=0.5)
    art = satin(art, circles(W, H, [(264, 418, 11)]), ROSE_D, ROSE, nx, freq=5, sheen=0.4)
    outl = np.maximum.reduce([body, sl, lap, belt, loops, ends])
    art = pen(art, outl, nx, col=PEN, w=1.8, dens=0.55)
    preview(art, "bs-robe", tone="#fdf3f1")
    save(art, f"{OUT}/robe.webp", max_w=320, quality=82)
    clear()

if "roses" in PARTS:
    W, H = 680, 480
    nx = Seq(500); rng = random.Random(5)
    art = blank(W, H)
    # ribbon tails trailing to the right
    rb = shapes(W, H, [ribbon_band(W, H, curve([(200, 170), (330, 230), (440, 200), (560, 260), (660, 236)], 60), 16),
                       ribbon_band(W, H, curve([(190, 200), (290, 300), (380, 330), (470, 390), (560, 400)], 60), 13)])
    art = satin(art, rb, BLUSH, ROSE, nx, angle=0.3, freq=14, sheen=0.5)
    art = pen(art, rb, nx, col=PEN, w=1.4, dens=0.4)
    clear()
    # leaves
    for x, y, L, a in ((70, 240, 96, 2.5), (220, 110, 90, -0.8), (270, 200, 96, 0.15), (80, 130, 86, -2.5), (150, 290, 92, 1.6), (250, 150, 80, -0.35), (200, 260, 84, 0.9), (120, 90, 80, -1.6)):
        art = leaf(art, W, H, x, y, L, a, rng, nx, c=(SAGE_A, SAGE_B))
    clear()
    roses = [(140, 170, 74, "#f9d6dc", "#ef9fb2", ROSE_D), (226, 206, 56, CHAMP2, "#f1b39c", "#c9705a"), (82, 236, 50, "#f6c0cc", "#e88aa0", "#9c3a5a"), (190, 104, 44, "#fff1ee", "#f3b8c4", ROSE), (250, 278, 38, "#f9d6dc", "#ef9fb2", ROSE_D), (72, 132, 36, CHAMP2, "#f1b39c", "#c9705a")]
    for cx, cy, r, l, m_, d in roses:
        art = rose(art, W, H, cx, cy, r, rng, nx, l, m_, d)
        clear()
    # baby's breath sprays
    for cx, cy in ((290, 100), (36, 300), (310, 250), (170, 320), (130, 70)):
        stems = []
        pts = []
        for _ in range(7):
            a = rng.uniform(0, math.tau); d = rng.uniform(10, 34)
            ex, ey = cx + math.cos(a) * d, cy + math.sin(a) * d
            stems.append(([(cx, cy + 20), (ex, ey)], 1.2, None)); pts.append((ex, ey, rng.uniform(4, 6.5)))
        art = G(art, strokes(W, H, stems), SAGE_B, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
        art = GP(art, circles(W, H, pts), "#fffdf8", "#f4ece6", seed=nx(), rough=0.8)
        art = G(art, contour(circles(W, H, pts), 1.2, nx()), "#c9b0b0", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.3)
    # rose-gold foil dots
    fd = circles(W, H, [(rng.uniform(20, 380), rng.uniform(20, 380), rng.uniform(2, 4)) for _ in range(10)])
    art = FO(art, fd, RG, seed=nx(), emboss=0.5, sparkle=0.3)
    preview(art, "bs-roses", tone="#fdf3f1")
    save(art, f"{OUT}/roses.webp", max_w=420, quality=80)
    clear()

if "sash" in PARTS:
    W, H = 900, 200
    nx = Seq(700)
    art = blank(W, H)
    c = curve([(20, 120), (300, 92), (600, 92), (880, 120)], 60)
    band = shapes(W, H, [ribbon_band(W, H, c, 92)])
    art = satin(art, band, "#fbe6ea", "#f6cbd4", nx, angle=0.05, freq=40, sheen=0.4)
    for off in (-36, 36):
        e = shapes(W, H, [ribbon_band(W, H, [(x, y + off) for x, y in c], 6)])
        art = FO(art, e, RG, seed=nx(), emboss=0.5, sparkle=0.3)
    # fringed ends
    art = pen(art, band, nx, col="#b07484", w=1.6, dens=0.45)
    preview(art, "bs-sash", tone="#fdf3f1")
    save(art, f"{OUT}/sash.webp", max_w=640, quality=82)
    clear()

if "bubbles" in PARTS:
    W, H = 220, 340
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    for x, y, r in ((110, 280, 30), (60, 190, 20), (150, 150, 24), (90, 90, 14), (160, 50, 10), (50, 40, 8), (130, 230, 9)):
        art = bubble(art, W, H, x, y, r, nx, rim="#e88aa0", tint="#fbe3e6", dens=0.65)
    preview(art, "bs-bubbles", tone="#fdf3f1")
    save(art, f"{OUT}/bubbles.webp", max_w=110, quality=84)

if "bow" in PARTS:
    W, H = 420, 170
    nx = Seq(1100)
    art = blank(W, H)
    loops = shapes(W, H, [[(210, 70), (130, 20), (96, 40), (110, 96), (210, 82)], [(210, 70), (290, 20), (324, 40), (310, 96), (210, 82)]])
    art = satin(art, loops, ROSE, "#f4a8bb", nx, angle=0.6, freq=9, sheen=0.55)
    tails = shapes(W, H, [ribbon_band(W, H, curve([(204, 82), (170, 120), (60, 140), (10, 128)], 30), 13), ribbon_band(W, H, curve([(216, 82), (250, 120), (360, 140), (410, 128)], 30), 13)])
    art = satin(art, tails, ROSE, "#f4a8bb", nx, angle=0.2, freq=9, sheen=0.5)
    knot = shapes(W, H, [ellipse_pts(210, 76, 15, 17, 12)])
    art = satin(art, knot, ROSE_D, ROSE, nx, freq=5, sheen=0.4)
    art = pen(art, np.maximum.reduce([loops, tails, knot]), nx, col=PEN, w=1.4, dens=0.5)
    preview(art, "bs-bow", tone="#fdf3f1")
    save(art, f"{OUT}/bow.webp", max_w=210, quality=84)

kb(OUT)
