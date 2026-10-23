"""Piringan Hitam — analog jazz-club record art in matte gouache: an original album-sleeve painting (spotlit stage,
double bass, saxophone on a stand, microphone, curtain, candle table), a painted vinyl record with grooves and sheen,
a tonearm, and a hand-painted soundwave divider. Deep navy / mustard / cream. Run: python3 -I piringan-hitam.py [part ...]
parts: sleeve vinyl arm wave. Assets -> public/themes/art/piringan-hitam/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h6_lib import *

OUT = outdir("piringan-hitam")
PARTS = sys.argv[1:] or ["sleeve", "vinyl", "arm", "wave"]
NAVY, NAVY_D, NAVY_L = "#16233d", "#0c1426", "#2a3d63"
MUSTARD, MUSTARD_L, MUSTARD_D = "#d9a532", "#f0c95e", "#a5771c"
CREAM, CREAM_D = "#f3e6c8", "#d8c6a0"
RUST = "#b5532f"
WOOD, WOOD_D = "#7a4a2a", "#4a2a16"


def gp(art, m, a, b=None, rough=1.6, streak=0.9, **k):
    return GP(art, m, a, b, seed=k.pop("seed"), rough=rough, streak=streak, **k)


if "sleeve" in PARTS:
    W = H = 760
    nx = Seq(81000); rng = random.Random(81)
    art = solid(W, H, NAVY)
    art = gp(art, shapes(W, H, [rect(0, 0, W, H)], smooth=False), NAVY, NAVY_L, seed=nx(), rough=0.5, streak=1.4)
    # curtain folds at the back (navy, vertical brushy pleats with mustard rim light)
    for i in range(14):
        x = i * 58 - 20
        pleat = [(x, -10), (x + 30, -10), (x + 34 + rng.uniform(-6, 6), 520), (x + 4, 520)]
        art = gp(art, shapes(W, H, [pleat], smooth=False), mix(NAVY_L, NAVY_D, rng.uniform(0.1, 0.7)), NAVY_D, seed=nx(), rough=2.5, streak=1.6, pad=6)
    # mid-century mustard disc (the "sun" of the cover) + spotlight cone
    art = OV(art, circles(W, H, [(470, 290, 210)]), lambda m: gouache_paint(m, MUSTARD, MUSTARD_L, seed=nx(), rough=2.0, streak=1.0))
    cone = shapes(W, H, [[(430, -10), (510, -10), (640, 600), (300, 600)]], smooth=False)
    art = over(art, glow(cone * 0.6, "#fff1c4", radius=18, strength=0.35))
    clear()
    # stage floor boards
    floor = shapes(W, H, [[(-10, 520), (W + 10, 520), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    art = gp(art, floor, WOOD, WOOD_D, seed=nx(), rough=0.8, streak=1.6)
    boards = strokes(W, H, [([(x, 520), (x + (x - 380) * 0.9, H + 10)], 2.2, None) for x in range(-200, 1000, 60)])
    art = G(art, boards * floor, WOOD_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1, feather=0.6)
    pool = circles(W, H, [(470, 590, 1)])
    art = over(art, glow(shapes(W, H, [deform(ellipse_pts(470, 585, 200, 46, 14), rng, 1, 0.05)]), "#f6d27a", radius=16, strength=0.45))
    # double bass (left), leaning
    bx, by_ = 250, 560
    prof = [(0, 0), (52, -6), (78, -40), (80, -90), (58, -130), (50, -150), (60, -190), (56, -232), (34, -262), (12, -270)]
    outline = [(bx + x, by_ + y) for x, y in prof] + [(bx - x, by_ + y) for x, y in prof[::-1]]
    body = [outline]
    bm = shapes(W, H, body)
    art = gp(art, bm, "#8a4a22", "#5e2e12", seed=nx(), rough=1.2)
    hi = np.clip(bm - np.roll(np.roll(gaussian_filter(bm, 8), -14, 1), 6, 0), 0, 1) * bm
    art = G(art, hi, MUSTARD_L, seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=1.5)
    neck = strokes(W, H, [([(bx, by_ - 250), (bx + 4, by_ - 430)], 14, None)])
    scroll = circles(W, H, [(bx + 6, by_ - 438, 13)])
    art = gp(art, np.maximum(neck, scroll), "#2b1a10", seed=nx(), rough=0.8)
    strs = strokes(W, H, [([(bx - 9 + k * 6, by_ - 36), (bx - 4 + k * 3, by_ - 420)], 1.2, None) for k in range(4)])
    art = OV(art, strs, lambda m: rgba_solid(m, CREAM, 0.8))
    fholes = strokes(W, H, [(curve([(bx - 30, by_ - 100), (bx - 22, by_ - 80), (bx - 30, by_ - 60)], 8), 4, None), (curve([(bx + 40, by_ - 100), (bx + 48, by_ - 80), (bx + 40, by_ - 60)], 8), 4, None)])
    art = gp(art, fholes, NAVY_D, seed=nx(), rough=0.5)
    art = gp(art, shapes(W, H, [rect(bx - 22, by_ - 40, 40, 8)], smooth=False), "#2b1a10", seed=nx(), rough=0.5)
    art = gp(art, strokes(W, H, [([(bx, by_ + 18), (bx - 6, by_ + 44)], 5, None)]), "#9a9a9a", seed=nx(), rough=0.5)
    clear()
    # microphone stand in the spotlight (centre-right)
    mx = 470
    art = gp(art, strokes(W, H, [([(mx, 560), (mx, 300)], 6, None), ([(mx - 40, 566), (mx + 40, 566)], 7, None)]), "#2a2a2e", seed=nx(), rough=0.5)
    mic = shapes(W, H, [deform(ellipse_pts(mx, 282, 18, 28, 12), rng, 1, 0.02)])
    art = gp(art, mic, "#cfc8b6", "#8d877a", seed=nx(), rough=0.6)
    grill = strokes(W, H, [([(mx - 14, 270 + k * 8), (mx + 14, 270 + k * 8)], 1.4, None) for k in range(4)])
    art = OV(art, grill * mic, lambda m: rgba_solid(m, "#5a554c", 0.7))
    # saxophone on its stand (right)
    sx, sy = 620, 520
    sax_body = curve([(sx - 10, sy - 270), (sx - 6, sy - 150), (sx, sy - 60), (sx + 30, sy - 20), (sx + 62, sy - 40), (sx + 66, sy - 90)], 40)
    art = FO(art, strokes(W, H, [(sax_body, 24, (0.35, 0.0))]), "#d6a443", seed=nx(), emboss=0.5, sparkle=0.08)
    bell = shapes(W, H, [deform(ellipse_pts(sx + 66, sy - 98, 24, 12, 10, -0.2), rng, 1, 0.03)])
    art = FO(art, bell, "#e0b457", seed=nx(), emboss=0.6)
    art = gp(art, shapes(W, H, [deform(ellipse_pts(sx + 66, sy - 100, 16, 6, 10, -0.2), rng, 1, 0.03)]), "#3a2a12", seed=nx(), rough=0.4)
    keys = circles(W, H, [(sx - 6 + (k % 2) * 6, sy - 220 + k * 22, 5) for k in range(7)])
    art = OV(art, keys, lambda m: rgba_solid(m, "#f6e2a6", 0.9))
    neckp = strokes(W, H, [(curve([(sx - 10, sy - 270), (sx - 22, sy - 296), (sx - 46, sy - 300)], 12), 7, None)])
    art = FO(art, neckp, "#c9973a", seed=nx(), emboss=0.4)
    stand = strokes(W, H, [([(sx + 20, sy - 30), (sx - 20, sy + 40)], 4, None), ([(sx + 20, sy - 30), (sx + 60, sy + 40)], 4, None), ([(sx + 20, sy - 30), (sx + 20, sy + 44)], 4, None)])
    art = gp(art, stand, "#1b1b20", seed=nx(), rough=0.4)
    clear()
    # foreground: round club table with candle + two glasses (dark silhouettes with warm rim)
    tm = shapes(W, H, [deform(ellipse_pts(150, 680, 120, 28, 16), rng, 1, 0.02)])
    art = gp(art, tm, "#1a1310", "#2a1d14", seed=nx(), rough=0.8)
    art = G(art, np.clip(tm - np.roll(tm, 4, 0), 0, 1), MUSTARD, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6)
    art = gp(art, shapes(W, H, [rect(140, 700, 20, 70)], smooth=False), "#1a1310", seed=nx(), rough=0.5)
    art = gp(art, shapes(W, H, [[(140, 668), (162, 668), (160, 630), (142, 630)]], smooth=False), "#c9482a", "#8c2c18", seed=nx(), rough=0.4)
    art = over(art, glow(circles(W, H, [(151, 616, 8)]), "#ffcf6a", radius=14, strength=0.7))
    art = gp(art, shapes(W, H, [petal_pts(151, 628, 18, 6, -math.pi / 2, n=10)]), "#ffe9a8", "#ffb84a", seed=nx(), rough=0.3)
    for gx in (90, 210):
        g = shapes(W, H, [[(gx - 12, 640), (gx + 12, 640), (gx + 3, 662), (gx + 3, 672), (gx + 10, 676), (gx - 10, 676), (gx - 3, 672), (gx - 3, 662)]], smooth=False)
        art = OV(art, g, lambda m: rgba_solid(m, CREAM, 0.55))
    # floating notes in cream gouache
    notes = []
    for nx_, ny_, s_ in [(380, 160, 1.0), (330, 110, 0.8), (560, 140, 0.9), (610, 90, 0.7)]:
        notes.append(deform(ellipse_pts(nx_, ny_, 14 * s_, 10 * s_, 10, -0.4), rng, 1, 0.03))
    nm = np.maximum(shapes(W, H, notes), strokes(W, H, [([(nx_ + 12 * s_, ny_), (nx_ + 12 * s_, ny_ - 50 * s_)], 4.5 * s_, None) for nx_, ny_, s_ in [(380, 160, 1.0), (330, 110, 0.8), (560, 140, 0.9), (610, 90, 0.7)]]))
    art = gp(art, nm, CREAM, CREAM_D, seed=nx(), rough=0.8)
    art = add_grain(vignette(art, 0.45, 1.8), 85, 0.05)
    preview6(art, "ph-sleeve", bg=NAVY)
    save_rgb(art, f"{OUT}/sleeve.webp", size=(600, 600), quality=78)
    clear()

if "vinyl" in PARTS:
    W = H = 600
    nx = Seq(82000); rng = random.Random(82)
    c = W / 2; R = 292
    disc = circles(W, H, [(c, c, R)])
    art = OV(blank(W, H), disc, lambda m: gouache_paint(m, "#141418", "#1e1e24", seed=nx(), rough=0.8, streak=0.6))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(xx - c, yy - c); th = np.arctan2(yy - c, xx - c)
    grooves = (0.5 + 0.5 * np.sin(r * 1.9 + fbm(W, H, 5, 40, 2) * 2)) * (r > 96) * (r < R - 8)
    gaps = ((np.abs(r - 170) < 3) | (np.abs(r - 228) < 3)).astype(np.float32)
    art = OV(art, grooves * disc * 0.28, lambda m: rgba_solid(m, "#3a3a44", 1.0))
    art = OV(art, gaps * disc, lambda m: rgba_solid(m, "#050507", 0.8))
    sheen = (np.cos(2 * (th + 0.7)) ** 60) * (r > 96) * (r < R - 6)
    art = OV(art, gaussian_filter(sheen, 2) * disc * 0.32, lambda m: rgba_solid(m, "#c9c4d6", 1.0))
    warm = (np.cos(2 * (th - 0.9)) ** 80) * (r > 110) * (r < R - 10)
    art = OV(art, gaussian_filter(warm, 3) * disc * 0.35, lambda m: rgba_solid(m, MUSTARD_L, 1.0))
    # label: mustard with a cream ring + rust inner band (original design, no text)
    lab = circles(W, H, [(c, c, 92)])
    art = OV(art, lab, lambda m: gouache_paint(m, MUSTARD, MUSTARD_L, seed=nx(), rough=0.8, streak=0.8))
    ringm = np.clip(circles(W, H, [(c, c, 74)]) - circles(W, H, [(c, c, 66)]), 0, 1)
    art = OV(art, ringm, lambda m: gouache_paint(m, CREAM, seed=nx(), rough=0.5))
    art = OV(art, np.clip(circles(W, H, [(c, c, 50)]) - circles(W, H, [(c, c, 38)]), 0, 1), lambda m: gouache_paint(m, RUST, seed=nx(), rough=0.5))
    star = shapes(W, H, [[(c + math.cos(a) * (30 if k % 2 == 0 else 12), c + math.sin(a) * (30 if k % 2 == 0 else 12)) for k, a in enumerate([-math.pi / 2 + j * math.pi / 5 for j in range(10)])]], smooth=False)
    art = OV(art, star * 0 + circles(W, H, [(c, c, 8)]), lambda m: rgba_solid(m, "#0c0c10", 1.0))
    arc = strokes(W, H, [(arc_pts(c, c, 82, -2.6, -0.6, 30), 3, (0.2, 0.2)), (arc_pts(c, c, 82, 0.6, 2.6, 30), 3, (0.2, 0.2))])
    art = OV(art, arc, lambda m: rgba_solid(m, NAVY, 0.8))
    preview6(art, "ph-vinyl", bg=NAVY)
    save(art, f"{OUT}/vinyl.webp", max_w=420, quality=80)
    clear()

if "arm" in PARTS:
    # tonearm: pivot base + counterweight + long arm + headshell (for the turntable)
    W, H = 260, 560
    nx = Seq(83000); rng = random.Random(83)
    art = blank(W, H)
    art = gp(art, circles(W, H, [(190, 70, 52)]), "#2a2a30", "#3a3a42", seed=nx(), rough=0.6)
    art = FO(art, np.clip(circles(W, H, [(190, 70, 40)]) - circles(W, H, [(190, 70, 30)]), 0, 1), "#c7c2b4", seed=nx(), emboss=0.6)
    art = FO(art, shapes(W, H, [rect(176, 8, 28, 40)], smooth=False), "#bdb7a8", seed=nx(), emboss=0.6)
    arm = curve([(190, 70), (186, 240), (150, 420), (98, 500)], 40)
    art = FO(art, strokes(W, H, [(arm, 9, None)]), "#d9d3c2", seed=nx(), emboss=0.7, sparkle=0.1)
    head = shapes(W, H, [[(84, 486), (114, 500), (96, 544), (66, 530)]], smooth=False)
    art = gp(art, head, "#1b1b20", seed=nx(), rough=0.5)
    art = gp(art, shapes(W, H, [rect(72, 528, 10, 14)], smooth=False), MUSTARD, seed=nx(), rough=0.4)
    preview6(art, "ph-arm", bg=NAVY)
    save(art, f"{OUT}/arm.webp", max_w=160, quality=84)
    clear()

if "wave" in PARTS:
    # hand-painted soundwave bars (mustard / cream), divider
    W, H = 560, 110
    nx = Seq(84000); rng = random.Random(84)
    art = blank(W, H)
    bars_m, bars_c = [], []
    for i in range(38):
        x = 30 + i * 13.2
        t = i / 37
        h = 8 + 70 * (math.sin(t * math.pi) ** 1.5) * (0.45 + 0.55 * abs(math.sin(i * 1.7))) + rng.uniform(0, 6)
        item = ([(x, 55 - h / 2), (x, 55 + h / 2)], 6.5, None)
        (bars_m if i % 3 else bars_c).append(item)
    art = gp(art, strokes(W, H, bars_m), MUSTARD, MUSTARD_L, seed=nx(), rough=0.8)
    art = gp(art, strokes(W, H, bars_c), CREAM, CREAM_D, seed=nx(), rough=0.8)
    preview6(art, "ph-wave", bg=NAVY)
    save(art, f"{OUT}/wave.webp", max_w=300, quality=84)
    clear()
