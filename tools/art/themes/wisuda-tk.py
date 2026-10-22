"""Wisuda TK — kindergarten graduation drawn in wax pastel & crayon on manila paper: a child in a mini toga holding a
rolled certificate, a rayed sun, a red school bag, a grass strip with crayon flowers, a toga cap, three crayons and a
wavy crayon divider with stars. Run: python3 -I wisuda-tk.py [part ...]
Assets -> public/themes/art/wisuda-tk/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c6_lib import *

OUT = outdir("wisuda-tk")
PARTS = sys.argv[1:] or ["paper", "kid", "sun", "bag", "grass", "divider", "cap", "crayons"]
MANILA = "#ecd9a6"
INK = "#2d2a4a"         # dark indigo crayon for outlines
RED, RED_D = "#e0483a", "#b8302a"
BLUE, BLUE_D = "#3a68c2", "#27488f"
YEL, YEL_D = "#f6c431", "#e89a1e"
GRN, GRN_D = "#58a845", "#3a7e33"
SKIN, SKIN_D = "#efbf94", "#d99a6c"
PINK = "#f08b9a"
PURP = "#8a63c4"


def outline(art, m, col=INK, seed=1, px=2.4, amt=0.85):
    return crayon(art, contour(m, px * 1.25), col, seed=seed, amt=min(1, amt * 1.2), tooth=0.28)


if "paper" in PARTS:
    t = wrap_paper(512, 512, MANILA, seed=11, fibre=1.4, mottle=1.2, flecks=1.0, fleck_col="#9c7a45")
    save_full(t, f"{OUT}/paper.webp", quality=74)

if "cap" in PARTS:
    W, H = 260, 220
    nx = Seq(31000); art = blank(W, H)
    board = shapes(W, H, [[(20, 78), (130, 34), (240, 76), (130, 120)]], smooth=False)
    skull = shapes(W, H, [[(70, 96), (190, 96), (186, 150), (130, 166), (74, 150)]])
    art = wax(art, skull, BLUE_D, "#203d7a", seed=nx(), angle=1.2)
    art = outline(art, skull, seed=nx())
    art = wax(art, board, BLUE, BLUE_D, seed=nx(), angle=0.3)
    art = outline(art, board, seed=nx())
    art = wax(art, circles(W, H, [(130, 77, 9)]), YEL, seed=nx())
    tas = strokes(W, H, [(curve([(130, 77), (190, 86), (214, 110), (216, 156)], 20), 6, None)])
    art = wax(art, tas, YEL, YEL_D, seed=nx(), angle=1.5, rough=1.0)
    fr = strokes(W, H, [([(216 + dx, 150), (216 + dx * 1.6, 194)], 3.2, None) for dx in (-6, -2, 2, 6)])
    art = wax(art, fr, YEL_D, YEL, seed=nx(), angle=1.5, rough=0.8)
    bbox_save(art, "tk-cap", f"{OUT}/cap.webp", 200, tone=MANILA)
    clear()

if "kid" in PARTS:
    W, H = 560, 700
    nx = Seq(32000); rng = random.Random(4); art = blank(W, H)
    cx = 280
    # legs + shoes
    legs = strokes(W, H, [([(cx - 34, 560), (cx - 38, 640)], 20, None), ([(cx + 34, 560), (cx + 40, 640)], 20, None)])
    art = wax(art, legs, SKIN, SKIN_D, seed=nx(), angle=1.5)
    shoes = ellipses(W, H, [(cx - 50, 650, 30, 15, -4), (cx + 52, 650, 30, 15, 4)])
    art = wax(art, shoes, "#4a3b33", "#2e2420", seed=nx())
    art = outline(art, shoes, seed=nx())
    # gown: wide trapezoid with sleeves
    gown = shapes(W, H, [[(cx - 70, 300), (cx + 70, 300), (cx + 128, 580), (cx - 128, 580)]], smooth=False)
    gown = displace(gown, 5, 2.5, 30)
    sleeves = shapes(W, H, [[(cx - 66, 304), (cx - 150, 420), (cx - 118, 452), (cx - 52, 360)], [(cx + 66, 304), (cx + 150, 420), (cx + 118, 452), (cx + 52, 360)]])
    art = wax(art, np.clip(gown + sleeves, 0, 1), BLUE, BLUE_D, seed=nx(), angle=1.35, spacing=3.6)
    art = outline(art, np.clip(gown + sleeves, 0, 1), seed=nx(), px=2.8)
    # yellow sash collar
    collar = shapes(W, H, [[(cx - 62, 302), (cx + 62, 302), (cx + 16, 420), (cx - 16, 420)]])
    art = wax(art, collar, YEL, YEL_D, seed=nx(), angle=0.9)
    art = outline(art, collar, col=YEL_D, seed=nx(), amt=0.7)
    # hands + rolled certificate held across the chest
    hands = circles(W, H, [(cx - 112, 452, 20), (cx + 112, 452, 20)])
    art = wax(art, hands, SKIN, SKIN_D, seed=nx())
    roll = shapes(W, H, [[(cx - 150, 432), (cx + 150, 430), (cx + 150, 470), (cx - 150, 472)]])
    art = wax(art, roll, "#fffaf0", "#f6ecd2", seed=nx(), angle=0.05, density=1.0, press=0.2, spacing=2.4)
    art = wax(art, roll, "#fffaf0", seed=nx(), angle=1.2, density=0.7, press=0.1)
    art = outline(art, roll, seed=nx())
    art = wax(art, ellipses(W, H, [(cx + 150, 450, 9, 20, 0)]), "#e9dcb5", seed=nx())
    rib = shapes(W, H, [[(cx - 14, 428), (cx + 14, 428), (cx + 14, 474), (cx - 14, 474)]], smooth=False)
    bow = shapes(W, H, [[(cx, 450), (cx - 34, 424), (cx - 38, 470)], [(cx, 450), (cx + 34, 424), (cx + 38, 470)], [(cx - 6, 456), (cx - 26, 506), (cx - 12, 510)], [(cx + 6, 456), (cx + 24, 508), (cx + 10, 512)]])
    art = wax(art, np.clip(rib + bow, 0, 1), RED, RED_D, seed=nx(), angle=0.8)
    art = outline(art, bow, col=RED_D, seed=nx(), amt=0.7)
    # head
    head = circles(W, H, [(cx, 222, 92)])
    head = displace(head, 7, 2.0, 30)
    art = wax(art, head, SKIN, SKIN_D, seed=nx(), angle=0.6, spacing=3.0)
    neck = shapes(W, H, [[(cx - 20, 300), (cx + 20, 300), (cx + 16, 316), (cx - 16, 316)]])
    art = wax(art, neck * (1 - collar), SKIN_D, seed=nx())
    # hair: scribbled black with bangs and two bunches
    hair = shapes(W, H, [deform([(cx - 96, 222), (cx - 92, 160), (cx - 50, 128), (cx, 120), (cx + 50, 128), (cx + 92, 160), (cx + 96, 222),
                                 (cx + 74, 186), (cx + 40, 172), (cx + 10, 184), (cx - 24, 170), (cx - 60, 184), (cx - 80, 200)], rng, 1, 0.02)])
    buns = circles(W, H, [(cx - 104, 236, 26), (cx + 104, 236, 26)])
    art = wax(art, np.clip(hair + buns, 0, 1), "#2f2622", "#3e2f28", seed=nx(), angle=2.2, spacing=2.6)
    art = wax(art, circles(W, H, [(cx - 98, 212, 9), (cx + 98, 212, 9)]), RED, seed=nx())
    art = outline(art, np.clip(head + buns, 0, 1), seed=nx(), px=2.6)
    # face
    art = wax(art, circles(W, H, [(cx - 32, 232, 8), (cx + 32, 232, 8)]), "#2a2220", seed=nx(), rough=0.5)
    art = wax(art, circles(W, H, [(cx - 56, 262, 15), (cx + 56, 262, 15)]), PINK, seed=nx(), density=0.6, rough=1.2)
    art = scribble_line(art, arc_pts(cx, 250, 30, 0.45, 2.7, 16), 4.5, RED_D, seed=nx(), passes=1)
    # mortarboard cap on top
    skull = shapes(W, H, [[(cx - 76, 150), (cx + 76, 150), (cx + 72, 116), (cx - 72, 116)]])
    board = shapes(W, H, [[(cx - 140, 112), (cx - 4, 64), (cx + 140, 108), (cx + 4, 154)]], smooth=False)
    art = wax(art, skull, BLUE_D, "#203d7a", seed=nx(), angle=1.2)
    art = wax(art, board, BLUE, BLUE_D, seed=nx(), angle=0.3)
    art = outline(art, np.clip(board + skull, 0, 1), seed=nx(), px=2.6)
    art = wax(art, circles(W, H, [(cx, 108, 10)]), YEL, seed=nx())
    tas = strokes(W, H, [(curve([(cx, 108), (cx + 80, 118), (cx + 118, 140), (cx + 124, 196)], 24), 7, None)])
    art = wax(art, tas, YEL, YEL_D, seed=nx(), angle=1.5, rough=1.0)
    fr = strokes(W, H, [([(cx + 124 + dx, 190), (cx + 124 + dx * 1.6, 236)], 3.6, None) for dx in (-7, -2, 3, 8)])
    art = wax(art, fr, YEL_D, YEL, seed=nx(), angle=1.5, rough=0.8)
    bbox_save(art, "tk-kid", f"{OUT}/kid.webp", 440, tone=MANILA)
    clear()

if "sun" in PARTS:
    W, H = 380, 380
    nx = Seq(33000); rng = random.Random(9); art = blank(W, H)
    cx, cy = 190, 190
    rays = []
    for k in range(14):
        a = k / 14 * math.tau + rng.uniform(-.05, .05)
        r0, r1 = 98, 160 + (16 if k % 2 else -6)
        pts = []
        for i in range(9):
            t = i / 8
            rr = r0 + (r1 - r0) * t
            wv = math.sin(t * math.pi * 2.4) * 7
            pts.append((cx + math.cos(a) * rr - math.sin(a) * wv, cy + math.sin(a) * rr + math.cos(a) * wv))
        rays.append((pts, 15 if k % 2 else 19, (0.05, 0.45)))
    rm = strokes(W, H, rays)
    art = wax(art, rm, YEL_D, "#f0b12a", seed=nx(), angle=0.9, rough=1.5)
    disk = displace(circles(W, H, [(cx, cy, 86)]), 3, 2.0, 30)
    art = wax(art, disk, YEL, "#f9d75a", seed=nx(), angle=0.5, spacing=3.0)
    art = wax(art, circles(W, H, [(cx + 26, cy + 30, 50)]) * disk, YEL_D, seed=nx(), density=0.35)
    art = crayon(art, contour(disk, 2.6), "#e07a1e", seed=nx(), amt=0.8)
    # closed happy eyes + smile
    art = scribble_line(art, arc_pts(cx - 30, cy - 10, 12, 3.6, 5.9, 10), 4, "#c8561e", seed=nx(), passes=1)
    art = scribble_line(art, arc_pts(cx + 30, cy - 10, 12, 3.6, 5.9, 10), 4, "#c8561e", seed=nx(), passes=1)
    art = scribble_line(art, arc_pts(cx, cy + 10, 34, 0.5, 2.65, 16), 5, "#c8561e", seed=nx(), passes=1)
    art = wax(art, circles(W, H, [(cx - 50, cy + 18, 12), (cx + 50, cy + 18, 12)]), "#f28a5a", seed=nx(), density=0.6)
    bbox_save(art, "tk-sun", f"{OUT}/sun.webp", 300, tone=MANILA)
    clear()

if "bag" in PARTS:
    W, H = 320, 360
    nx = Seq(34000); art = blank(W, H)
    strap = strokes(W, H, [(arc_pts(160, 92, 52, math.pi * 1.05, math.pi * 1.95, 16), 14, None)])
    art = wax(art, strap, RED_D, seed=nx(), angle=0.2)
    art = outline(art, strap, seed=nx(), px=2.0, amt=0.7)
    body = shapes(W, H, [[(64, 96), (256, 96), (276, 150), (272, 320), (48, 320), (44, 150)]])
    art = wax(art, body, RED, RED_D, seed=nx(), angle=1.2, spacing=3.6)
    art = outline(art, body, seed=nx(), px=2.8)
    flap = shapes(W, H, [[(52, 104), (268, 104), (270, 186), (160, 206), (50, 186)]])
    art = wax(art, flap, "#ea5f48", RED, seed=nx(), angle=0.4)
    art = outline(art, flap, seed=nx(), px=2.4)
    pocket = shapes(W, H, [[(96, 232), (224, 232), (226, 296), (94, 296)]])
    art = wax(art, pocket, BLUE, BLUE_D, seed=nx(), angle=0.9)
    art = outline(art, pocket, seed=nx(), px=2.2)
    art = wax(art, shapes(W, H, [[(144, 180), (176, 180), (176, 214), (144, 214)]], smooth=False), YEL, YEL_D, seed=nx())
    # little star sticker on the pocket
    st = [(160 + math.cos(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9), 264 + math.sin(-math.pi / 2 + k * math.pi / 5) * (22 if k % 2 == 0 else 9)) for k in range(10)]
    art = wax(art, shapes(W, H, [st], smooth=False), YEL, seed=nx(), rough=1.0)
    bbox_save(art, "tk-bag", f"{OUT}/bag.webp", 240, tone=MANILA)
    clear()

if "grass" in PARTS:
    W, H = 1000, 230
    nx = Seq(35000); rng = random.Random(12); art = blank(W, H)
    ground = shapes(W, H, [[(0, 120)] + [(x, 118 + 8 * math.sin(x / 70)) for x in range(0, 1001, 50)] + [(1000, 230), (0, 230)]])
    art = wax(art, ground, GRN, GRN_D, seed=nx(), angle=0.15, spacing=4.0, density=0.85)
    blades = []
    for x in range(-6, 1006, 9):
        hgt = rng.uniform(24, 46)
        lean = rng.uniform(-10, 10)
        blades.append(([(x, 132), (x + lean * 0.4, 132 - hgt * 0.5), (x + lean, 132 - hgt)], 4.5, (0.0, 0.7)))
    art = wax(art, strokes(W, H, blades), GRN_D, "#4f9a3c", seed=nx(), angle=1.5, rough=1.0)
    # crayon flowers on stems
    for i, x in enumerate([70, 210, 330, 520, 640, 790, 930]):
        top = rng.uniform(40, 70)
        art = wax(art, strokes(W, H, [([(x, 134), (x + rng.uniform(-6, 6), top + 12)], 6, None)]), GRN_D, seed=nx(), angle=1.5, rough=0.8)
        col = [RED, YEL, PURP, PINK, BLUE, YEL, RED][i]
        pet = [(x + math.cos(k / 5 * math.tau) * 15, top + math.sin(k / 5 * math.tau) * 15, 11) for k in range(5)]
        art = wax(art, circles(W, H, pet), col, seed=nx(), rough=1.4)
        art = wax(art, circles(W, H, [(x, top, 8)]), YEL_D if col != YEL else RED, seed=nx(), rough=0.8)
    bbox_save(art, "tk-grass", f"{OUT}/grass.webp", 760, tone=MANILA)
    clear()

if "divider" in PARTS:
    W, H = 420, 80
    nx = Seq(36000); art = blank(W, H)
    wave = [(x, 40 + 9 * math.sin(x / 18)) for x in range(12, 409, 6)]
    art = scribble_line(art, wave[:22], 5, BLUE, seed=nx())
    art = scribble_line(art, wave[44:], 5, BLUE, seed=nx())
    for i, (sx, col) in enumerate([(170, YEL), (210, RED), (250, YEL)]):
        r = 17 if i == 1 else 12
        st = [(sx + math.cos(-math.pi / 2 + k * math.pi / 5) * (r if k % 2 == 0 else r * 0.45), 40 + math.sin(-math.pi / 2 + k * math.pi / 5) * (r if k % 2 == 0 else r * 0.45)) for k in range(10)]
        m = shapes(W, H, [st], smooth=False)
        art = wax(art, m, col, seed=nx(), rough=0.8)
        art = outline(art, m, col=YEL_D if col == YEL else RED_D, seed=nx(), px=1.6, amt=0.7)
    bbox_save(art, "tk-divider", f"{OUT}/divider.webp", 300, tone=MANILA)
    clear()

if "crayons" in PARTS:
    W, H = 340, 260
    nx = Seq(37000); art = blank(W, H)
    for k, (col, dark, ang) in enumerate([(BLUE, BLUE_D, -0.5), (RED, RED_D, -0.2), (YEL, YEL_D, 0.12), (GRN, GRN_D, 0.42)]):
        cx, cy = 170 + (k - 1.5) * 38, 150
        ca, sa = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
        px, py = -sa, ca
        L, wd = 170, 16
        def P(u, v):
            return (cx + ca * u + px * v, cy + sa * u + py * v)
        body = shapes(W, H, [[P(-L / 2, -wd), P(L / 2 - 26, -wd), P(L / 2 - 26, wd), P(-L / 2, wd)]], smooth=False)
        tip = shapes(W, H, [[P(L / 2 - 28, -wd * 0.9), P(L / 2 + 6, -3), P(L / 2 + 6, 3), P(L / 2 - 28, wd * 0.9)]], smooth=False)
        art = wax(art, body, col, dark, seed=nx(), angle=ang + 1.57, rough=1.0)
        art = wax(art, tip, dark, seed=nx(), rough=0.8)
        band = shapes(W, H, [[P(-L / 2 + 30, -wd), P(L / 2 - 50, -wd), P(L / 2 - 50, wd), P(-L / 2 + 30, wd)]], smooth=False)
        art = wax(art, band, "#f7f0dc", "#efe4c4", seed=nx(), density=0.75, rough=0.8)
        stripe = shapes(W, H, [[P(-L / 2 + 44, -wd), P(-L / 2 + 54, -wd), P(-L / 2 + 54, wd), P(-L / 2 + 44, wd)], [P(L / 2 - 72, -wd), P(L / 2 - 62, -wd), P(L / 2 - 62, wd), P(L / 2 - 72, wd)]], smooth=False)
        art = wax(art, stripe, dark, seed=nx(), rough=0.6)
        art = outline(art, np.clip(body + tip, 0, 1), col=INK, seed=nx(), px=1.8, amt=0.6)
    bbox_save(art, "tk-crayons", f"{OUT}/crayons.webp", 240, tone=MANILA)
    clear()

kb_total(OUT) if "kb_total" in dir() else None
