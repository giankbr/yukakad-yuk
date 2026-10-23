"""Ultah Pahlawan — an original kid superhero (round head, domino mask, blue suit, orange-red cape, yellow boots and
gloves, a blank chest shield the page stamps with the child's initial), a comic city skyline with lit windows, an
action burst and a shield emblem. Gouache kids'-book paint with navy ink contours and halftone.
Run: python3 -I ultah-pahlawan.py [part ...]  parts: hero city burst emblem"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k1_lib import *  # noqa

OUT = outdir("ultah-pahlawan")
PARTS = sys.argv[1:] or ["hero", "city", "burst", "emblem"]
NAVY = "#16213e"
BLUE, BLUE_D, BLUE_L = "#2f5bd8", "#1e3d9e", "#5a83f0"
CAPE, CAPE_D = "#ff5a36", "#c23a20"
YEL, YEL_D = "#ffc93c", "#e09a12"
SKIN, SKIN_D = "#eab48c", "#c98a62"
HAIR = "#3b2418"
CREAM = "#fff6e4"


def shield_pts(cx, cy, w, h):
    """Rounded heater shield (point down)."""
    top = curve([(cx - w, cy - h * 0.62), (cx - w * 0.5, cy - h * 0.68), (cx, cy - h * 0.72), (cx + w * 0.5, cy - h * 0.68), (cx + w, cy - h * 0.62)], 20)
    right = curve([(cx + w, cy - h * 0.62), (cx + w * 0.98, cy), (cx + w * 0.6, cy + h * 0.5), (cx, cy + h * 0.82)], 20)
    left = [(2 * cx - x, y) for x, y in right[::-1]]
    return top + right[1:] + left[1:-1]


def ink_outline(art, m, px=2.6, alpha=0.95, seed=1):
    return ink(art, outline(m, px), NAVY, alpha, rough=0.8, seed=seed)


if "hero" in PARTS:
    W, H = 640, 860
    nx = Seq(50100); rng = random.Random(5)
    art = blank(W, H)
    cx = 320
    # ground shadow
    art = G(art, shapes(W, H, [ellipse_pts(cx, 806, 170, 20, 24)]), NAVY, seed=nx(), density=0.3, edge=0.1, bloom=0, rough=3, feather=5)
    # cape (behind), billowing to the right
    cape = shapes(W, H, [[(214, 318), (170, 440), (120, 600), (84, 760), (170, 742), (250, 772), (340, 744), (430, 770), (520, 722), (600, 690), (560, 600), (500, 470), (440, 360), (426, 318)]])
    art = GP(art, cape, CAPE, "#ff7a4a", seed=nx(), rough=1.8, streak=1.0)
    folds = strokes(W, H, [(curve([(250, 360), (220, 560), (170, 740)], 20), 7, (0.2, 0.3)), (curve([(330, 380), (340, 560), (340, 740)], 20), 6, (0.2, 0.3)), (curve([(410, 370), (460, 540), (520, 718)], 20), 7, (0.2, 0.3))])
    art = G(art, gaussian_filter(folds, 3) * cape * 1.4, CAPE_D, seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=1.5)
    art = ink_outline(art, cape, seed=nx())
    # legs + boots
    legs = shapes(W, H, [[(236, 520), (300, 520), (296, 700), (240, 700)], [(340, 520), (404, 520), (400, 700), (344, 700)]], smooth=False)
    art = GP(art, legs, BLUE, BLUE_D, seed=nx(), rough=1.0, streak=0.8)
    boots = shapes(W, H, [[(232, 676), (300, 676), (304, 760), (310, 790), (212, 792), (220, 756)], [(340, 676), (408, 676), (420, 756), (428, 792), (330, 790), (336, 760)]])
    art = GP(art, boots, YEL, YEL_D, seed=nx(), rough=1.0, streak=0.8)
    art = OV(art, strokes(W, H, [([(232, 690), (300, 690)], 6, None), ([(340, 690), (408, 690)], 6, None)]), lambda mm: flat(mm, YEL_D, 0.9))
    art = ink_outline(art, np.maximum(legs, boots), seed=nx())
    # torso (rounded kid body) + belt
    torso = shapes(W, H, [[(222, 312), (418, 312), (436, 360), (424, 450), (412, 530), (228, 530), (216, 450), (204, 360)]])
    art = GP(art, torso, BLUE, BLUE_L, seed=nx(), rough=1.2, streak=0.9)
    shade = torso * np.clip((np.mgrid[0:H, 0:W][1] - 340) / 100.0, 0, 1)
    art = G(art, shade, BLUE_D, seed=nx(), density=0.4, edge=0, bloom=0.3, rough=2)
    belt = shapes(W, H, [[(222, 494), (418, 494), (416, 528), (224, 528)]], smooth=False)
    art = GP(art, belt, YEL, YEL_D, seed=nx(), rough=0.8)
    buckle = shapes(W, H, [[(300, 490), (340, 490), (344, 532), (296, 532)]], smooth=False)
    art = GP(art, buckle, CAPE, CAPE_D, seed=nx(), rough=0.5, pad=6)
    art = ink_outline(art, np.maximum(torso, belt), seed=nx())
    art = ink_outline(art, buckle, 2.0, seed=nx())
    # chest shield (blank: the page sets the initial on top)
    sh = shapes(W, H, [shield_pts(cx, 412, 58, 70)])
    art = GP(art, np.clip(gaussian_filter(sh, 3) * 1.3, 0, 1) * 0 + sh, CAPE, CAPE_D, seed=nx(), rough=0.6, pad=8)
    inner = shapes(W, H, [shield_pts(cx, 412, 46, 58)])
    art = GP(art, inner, YEL, "#ffe07a", seed=nx(), rough=0.6, pad=8)
    art = ink_outline(art, sh, 2.2, seed=nx())
    # arms: elbows out, fists on hips
    for sgn in (-1, 1):
        sxp, sy = cx + sgn * 104, 334
        el = (cx + sgn * 178, 420)
        fist = (cx + sgn * 112, 496)
        arm = strokes(W, H, [(curve([(sxp, sy), (cx + sgn * 150, 360), el], 16), 50, (0.0, 0.0)), (curve([el, (cx + sgn * 160, 470), fist], 16), 44, (0.0, 0.0))])
        art = GP(art, arm, BLUE, BLUE_D, seed=nx(), rough=1.0, streak=0.8)
        glove = np.maximum(circles(W, H, [(fist[0], fist[1], 28)]), strokes(W, H, [([(cx + sgn * 150, 462), fist], 46, None)]))
        art = GP(art, glove, YEL, YEL_D, seed=nx(), rough=0.8)
        art = ink_outline(art, np.maximum(arm, glove), seed=nx())
        art = OV(art, strokes(W, H, [([(cx + sgn * 152, 464), (cx + sgn * 160, 456)], 3, None)]), lambda mm: flat(mm, NAVY, 0.7))
    # neck + head
    neck = shapes(W, H, [[(296, 282), (344, 282), (346, 318), (294, 318)]], smooth=False)
    art = GP(art, neck, SKIN_D, seed=nx(), rough=0.6, pad=6)
    head = shapes(W, H, [deform(ellipse_pts(cx, 196, 104, 98, 30), rng, 1, 0.01)])
    ears = circles(W, H, [(cx - 104, 210, 20), (cx + 104, 210, 20)])
    art = GP(art, np.maximum(head, ears), SKIN, "#f2c49e", seed=nx(), rough=0.8, streak=0.5)
    art = G(art, head * np.clip((np.mgrid[0:H, 0:W][1] - 340) / 70.0, 0, 1), SKIN_D, seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    art = ink_outline(art, np.maximum(head, ears), seed=nx())
    # hair: a cap of tufts + a cowlick
    tufts = [[(cx - 108, 186), (cx - 100, 126), (cx - 60, 96), (cx - 20, 108), (cx - 10, 84), (cx + 30, 100), (cx + 50, 86), (cx + 70, 108), (cx + 100, 128), (cx + 110, 190), (cx + 86, 150), (cx + 40, 146), (cx, 138), (cx - 40, 146), (cx - 80, 152)]]
    hair = shapes(W, H, tufts)
    cow = strokes(W, H, [(curve([(cx - 6, 98), (cx - 4, 72), (cx + 14, 58), (cx + 30, 62)], 16), 14, (0.1, 0.7))])
    art = GP(art, np.maximum(hair, cow), HAIR, "#5a3622", seed=nx(), rough=1.4, streak=0.9)
    art = ink_outline(art, np.maximum(hair, cow), 2.2, seed=nx())
    # domino mask with eye holes
    mask = shapes(W, H, [[(cx - 100, 188), (cx - 60, 166), (cx - 14, 178), (cx, 188), (cx + 14, 178), (cx + 60, 166), (cx + 100, 188), (cx + 92, 226), (cx + 52, 238), (cx + 12, 222), (cx, 214), (cx - 12, 222), (cx - 52, 238), (cx - 92, 226)]])
    art = GP(art, mask, CAPE, CAPE_D, seed=nx(), rough=0.8)
    art = ink_outline(art, mask, 2.4, seed=nx())
    eyes = shapes(W, H, [ellipse_pts(cx - 48, 204, 20, 16, 16, 0.1), ellipse_pts(cx + 48, 204, 20, 16, 16, -0.1)])
    art = GP(art, eyes, "#ffffff", "#f3f6ff", seed=nx(), rough=0.4, pad=6)
    art = OV(art, circles(W, H, [(cx - 44, 206, 8), (cx + 52, 206, 8)]), lambda mm: flat(mm, NAVY, 1))
    art = OV(art, circles(W, H, [(cx - 41, 202, 3), (cx + 55, 202, 3)]), lambda mm: flat(mm, "#ffffff", 1))
    # smile, cheeks, nose
    smile = strokes(W, H, [(arc_pts(cx, 236, 34, 0.35, math.pi - 0.35, 20), 5, (0.15, 0.15))])
    art = OV(art, smile, lambda mm: flat(mm, NAVY, 0.9))
    art = G(art, circles(W, H, [(cx - 70, 250, 15), (cx + 70, 250, 15)]), "#f08a7a", seed=nx(), density=0.45, edge=0.1, bloom=0.2, rough=2, feather=3)
    art = OV(art, strokes(W, H, [(arc_pts(cx, 228, 9, 0.4, math.pi - 0.4, 8), 3, None)]), lambda mm: flat(mm, SKIN_D, 0.9))
    # emblem position (percent of the trimmed image) for the page
    prev(art, "up-hero", bg="#9fd8f0")
    sz = save(art, f"{OUT}/hero.webp", max_w=420, quality=82)
    a = to_image(art).getchannel("A").point(lambda v: 255 if v > 3 else 0).getbbox()
    print("emblem centre %", round((cx - a[0]) / (a[2] - a[0]) * 100, 1), round((415 - a[1]) / (a[3] - a[1]) * 100, 1), "shield w %", round(116 / (a[2] - a[0]) * 100, 1))
    clear()


if "city" in PARTS:
    W, H = 800, 330
    nx = Seq(50200); rng = random.Random(11)
    art = blank(W, H)
    def row(art, y_base, hmin, hmax, wmin, wmax, col, col2, win, seed_off, wdens):
        x = -10
        bl, wins = [], []
        while x < W + 10:
            w = rng.uniform(wmin, wmax); h = rng.uniform(hmin, hmax)
            top = y_base - h
            poly = [(x, y_base), (x, top), (x + w, top), (x + w, y_base)]
            if rng.random() < 0.3:  # stepped roof / antenna
                poly = [(x, y_base), (x, top), (x + w * 0.3, top), (x + w * 0.3, top - 14), (x + w * 0.7, top - 14), (x + w * 0.7, top), (x + w, top), (x + w, y_base)]
            bl.append(poly)
            for yy in np.arange(top + 12, y_base - 10, 18):
                for xx in np.arange(x + 8, x + w - 10, 14):
                    if rng.random() < wdens:
                        wins.append([(xx, yy), (xx + 7, yy), (xx + 7, yy + 9), (xx, yy + 9)])
            x += w + rng.uniform(-4, 6)
        m = shapes(W, H, bl, smooth=False)
        art = GP(art, m, col, col2, seed=nx(), rough=1.0, streak=0.8)
        art = ink(art, outline(m, 2.0), NAVY, 0.8, seed=nx())
        wm = shapes(W, H, wins, smooth=False)
        art = GP(art, wm, win, "#fff3b0", seed=nx(), rough=0.4, pad=6)
        return art, m
    art, back = row(art, 330, 120, 230, 50, 90, "#8fa6e8", "#a7b9f0", "#fff0a6", 1, 0.35)
    # halftone shading on the back row
    ht = halftone(W, H, 8, 2.4) * back * np.clip((np.mgrid[0:H, 0:W][0] - 120) / 200, 0, 1)
    art = OV(art, ht, lambda mm: flat(mm, "#6a82d0", 0.8))
    art, front = row(art, 330, 50, 140, 60, 110, "#3b4f9a", "#2f4088", "#ffd34d", 2, 0.5)
    prev(art, "up-city", bg="#9fd8f0")
    save(art, f"{OUT}/city.webp", max_w=780, quality=80)
    clear()


if "burst" in PARTS:
    W, H = 360, 360
    nx = Seq(50300); rng = random.Random(4)
    cx = cy = 180
    pts = []
    n = 14
    for i in range(n * 2):
        a = i / (n * 2) * math.tau + 0.1
        r = (160 if i % 2 == 0 else 104) * rng.uniform(0.9, 1.05)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    outer = shapes(W, H, [pts], smooth=False)
    pts2 = [(cx + (x - cx) * 0.8, cy + (y - cy) * 0.8) for x, y in pts]
    inner = shapes(W, H, [pts2], smooth=False)
    art = blank(W, H)
    art = GP(art, outer, CAPE, CAPE_D, seed=nx(), rough=1.0)
    art = GP(art, inner, YEL, "#ffe07a", seed=nx(), rough=1.0)
    ht = halftone(W, H, 10, 3.2) * inner * np.clip(1 - gaussian_filter(inner, 30) * 1.2 + 0.4, 0, 1)
    art = OV(art, ht, lambda mm: flat(mm, YEL_D, 0.7))
    art = ink(art, outline(outer, 2.6), NAVY, 0.95, seed=nx())
    prev(art, "up-burst", bg="#9fd8f0")
    save(art, f"{OUT}/burst.webp", max_w=220, quality=84)


if "emblem" in PARTS:
    W, H = 300, 320
    nx = Seq(50400)
    art = blank(W, H)
    sh = shapes(W, H, [shield_pts(150, 150, 120, 140)])
    inner = shapes(W, H, [shield_pts(150, 150, 98, 116)])
    art = GP(art, sh, CAPE, CAPE_D, seed=nx(), rough=1.0)
    art = GP(art, inner, YEL, "#ffe07a", seed=nx(), rough=1.0)
    ht = halftone(W, H, 9, 2.6) * inner * np.clip((np.mgrid[0:H, 0:W][0] - 120) / 160, 0, 1)
    art = OV(art, ht, lambda mm: flat(mm, YEL_D, 0.6))
    art = ink(art, outline(sh, 3), NAVY, 0.95, seed=nx())
    art = ink(art, outline(inner, 1.8), NAVY, 0.6, seed=nx())
    prev(art, "up-emblem", bg="#9fd8f0")
    save(art, f"{OUT}/emblem.webp", max_w=180, quality=84)
