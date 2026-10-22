"""Buka Bersama — a Ramadan iftar at maghrib: painted dusk sky (plum to rose to amber) with a thin crescent and a far
mosque skyline, brass lanterns with glowing panes (separate, they sway), a long table dressed in cream cloth with plates
of dates, kolak bowls, glasses of iced tea and a teapot, and a small dish of dates for ornaments. No figures.
Run: python3 -I buka-bersama.py [part ...]   parts: langit lentera meja kurma"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g5_lib import *

OUT = outdir("buka-bersama")
PARTS = sys.argv[1:] or ["langit", "lentera", "meja", "kurma"]
BRASS = "#d4a243"
DATE, DATE_D = "#7a3b1e", "#4a2010"


def date_fruit(art, W, H, cx, cy, L, ang, nx, rng):
    m = shapes(W, H, [deform(ellipse_pts(cx, cy, L, L * 0.46, 14, ang), rng, 1, 0.04)])
    art = GP(art, m, DATE, DATE_D, seed=nx(), rough=0.6, streak=1.0, pad=6)
    # wrinkles + glossy highlight
    wr = strokes(W, H, [([(cx - math.cos(ang) * L * 0.6 + math.sin(ang) * L * 0.1 * k, cy - math.sin(ang) * L * 0.6 - math.cos(ang) * L * 0.1 * k),
                         (cx + math.cos(ang) * L * 0.5 + math.sin(ang) * L * 0.14 * k, cy + math.sin(ang) * L * 0.5 - math.cos(ang) * L * 0.14 * k)], 1.0, (0.3, 0.3)) for k in (-2, 0, 2)])
    art = G(art, wr * m, "#2e1206", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.4)
    hl = strokes(W, H, [([(cx - math.cos(ang) * L * 0.4 - math.sin(ang) * L * -0.22, cy - math.sin(ang) * L * 0.4 + math.cos(ang) * L * -0.22),
                         (cx + math.cos(ang) * L * 0.2 - math.sin(ang) * L * -0.24, cy + math.sin(ang) * L * 0.2 + math.cos(ang) * L * -0.24)], max(1.2, L * 0.14), (0.3, 0.4))])
    art = GP(art, hl * m, "#e8a36a", seed=nx(), rough=0.4, density=0.55, pad=4)
    return art


def plate(art, W, H, cx, cy, rx, ry, nx, rng, rim="#3d6e9e"):
    m = shapes(W, H, [ellipse_pts(cx, cy, rx, ry, 30)])
    art = GP(art, m, "#f6f1e6", "#e7ddcc", seed=nx(), rough=0.6, pad=6)
    ring_m = np.clip(m - shapes(W, H, [ellipse_pts(cx, cy + ry * 0.04, rx * 0.86, ry * 0.8, 30)]), 0, 1)
    art = GP(art, ring_m, rim, seed=nx(), rough=0.5, density=0.85, pad=6)
    return art


if "langit" in PARTS:
    W, H = 780, 1300
    rng = random.Random(81); nx = Seq(81000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#25183a"), (0.22, "#3b2346"), (0.45, "#7a3a5e"), (0.62, "#c8607a"), (0.76, "#ec9a6a"), (0.88, "#f6bf7a"), (1, "#f9d699")], seed=81, streak=1.1, grain=0.9)
    # long thin dusk clouds catching light
    for y, x0, L, col in [(540, -40, 420, "#e47e86"), (600, 360, 460, "#f0a07c"), (700, -60, 380, "#f7b77c"), (470, 420, 300, "#b45a78")]:
        st = strokes(W, H, [(curve([(x0, y), (x0 + L * 0.5, y - 8), (x0 + L, y + 4)], 30), rng.uniform(10, 18), (0.4, 0.5))])
        art = G(art, displace(st, int(y), 6, 30), col, seed=nx(), density=0.55, edge=0.3, bloom=0.5, rough=6, feather=3)
    # stars in the upper (darker) sky
    st = star_field(W, H, 140, rng, ymax=520, rmin=0.6, rmax=1.6)
    art = over(art, rgba("#fff3d6", st * np.clip(1 - yy / 560, 0, 1)))
    # crescent moon: pale gold, soft glow
    cm = crescent_mask(W, H, 600, 250, 46, off=(0.34, -0.22), r2=0.9)
    art = over(art, glow(cm, "#ffe9b0", radius=26, strength=0.45))
    art = GP(art, cm, "#fff2c8", "#f3d891", seed=nx(), rough=0.6)
    # far skyline: mosque domes + minarets + low town roofs, dark plum silhouettes at the foot
    HY = 1140
    sil = []
    x = -20
    while x < W + 20:
        w = rng.uniform(30, 70); h = rng.uniform(12, 40)
        sil.append([(x, HY + 30), (x, HY - h), (x + w, HY - h), (x + w, HY + 30)]); x += w - 4
    mosque_x = 250
    sil.append(arc_pts(mosque_x, HY - 60, 48, math.pi, 2 * math.pi, 28) + [(mosque_x + 48, HY + 20), (mosque_x - 48, HY + 20)])
    sil.append([(mosque_x - 70, HY - 54), (mosque_x + 70, HY - 54), (mosque_x + 70, HY + 20), (mosque_x - 70, HY + 20)])
    for mx in (mosque_x - 110, mosque_x + 110):
        sil.append([(mx - 7, HY + 20), (mx - 7, HY - 150), (mx - 10, HY - 152), (mx, HY - 178), (mx + 10, HY - 152), (mx + 7, HY - 150), (mx + 7, HY + 20)])
    sil.append(arc_pts(560, HY - 34, 26, math.pi, 2 * math.pi, 20) + [(586, HY + 20), (534, HY + 20)])
    sm = shapes(W, H, sil, smooth=False)
    finials = strokes(W, H, [([(mosque_x, HY - 108), (mosque_x, HY - 128)], 2.4, None), ([(560, HY - 60), (560, HY - 72)], 2, None)])
    art = GP(art, np.maximum(sm, finials), "#5b2c4a", "#4a2440", seed=nx(), rough=1.2, streak=0.6)
    lights = circles(W, H, [(rng.uniform(0, W), rng.uniform(HY - 20, HY + 10), rng.uniform(1.2, 2.2)) for _ in range(40)]) * sm
    art = over(art, rgba("#ffd27a", lights))
    ground = (yy > HY + 10).astype(np.float32)
    art = GP(art, ground, "#4a2440", "#3b1d35", seed=nx(), rough=1, streak=0.6)
    art[..., 3] = 1
    art = add_grain(art, 2, 0.02)
    preview(art, "bb-langit", bg="#000000")
    save_rgb(art, f"{OUT}/langit.webp", size=(560, 933), quality=76)
    clear()

if "lentera" in PARTS:
    # brass lantern (fanous-inspired): ring, domed cap, three visible glass panes with pierced frames, tapered base
    W, H = 300, 600
    rng = random.Random(82); nx = Seq(82000)
    art = blank(W, H)
    C = 150
    ring_m = np.clip(circles(W, H, [(C, 26, 16)]) - circles(W, H, [(C, 26, 10)]), 0, 1)
    cap = shapes(W, H, [[(C - 6, 42), (C + 6, 42), (C + 20, 70), (C + 64, 120), (C + 74, 138), (C - 74, 138), (C - 64, 120), (C - 20, 70)]])
    collar = poly_fill(W, H, [[(C - 82, 136), (C + 82, 136), (C + 78, 150), (C - 78, 150)]])
    panes_c = poly_fill(W, H, [[(C - 38, 152), (C + 38, 152), (C + 32, 400), (C - 32, 400)]])
    panes_l = poly_fill(W, H, [[(C - 78, 152), (C - 42, 152), (C - 36, 400), (C - 64, 400)]])
    panes_r = poly_fill(W, H, [[(C + 42, 152), (C + 78, 152), (C + 64, 400), (C + 36, 400)]])
    base = shapes(W, H, [[(C - 70, 398), (C + 70, 398), (C + 56, 430), (C + 20, 470), (C + 8, 520), (C - 8, 520), (C - 20, 470), (C - 56, 430)]])
    drop = shapes(W, H, [petal_pts(C, 520, 34, 12, math.pi / 2, n=12)])
    glass = np.maximum(panes_c, np.maximum(panes_l, panes_r))
    # glow behind + inside
    art = over(art, glow(glass, "#ffb347", radius=30, strength=0.4))
    art = GP(art, glass, "#ffd277", "#f3a640", seed=nx(), rough=0.6, streak=0.8)
    art = G(art, panes_l + panes_r, "#c46a2a", seed=nx(), density=0.4, edge=0.2, bloom=0.3, rough=1)
    flame = shapes(W, H, [petal_pts(C, 360, 70, 22, -math.pi / 2, n=14)])
    art = over(art, glow(flame, "#fff2c0", radius=14, strength=0.7))
    # pierced frame: verticals + star/arch cutouts drawn as brass over the glass
    frame = strokes(W, H, [([(C - 40, 152), (C - 34, 400)], 5, None), ([(C + 40, 152), (C + 34, 400)], 5, None),
                           ([(C - 79, 152), (C - 65, 400)], 5, None), ([(C + 79, 152), (C + 65, 400)], 5, None),
                           ([(C - 80, 196), (C + 80, 196)], 4, None), ([(C - 72, 360), (C + 72, 360)], 4, None)])
    arches = poly_stroke(W, H, [arch_pts(C, 350, 24, 90, 24), arch_pts(C - 57, 350, 10, 90, 16), arch_pts(C + 57, 350, 10, 90, 16)], 3)
    stars = []
    for cx, cy, r in [(C, 174, 12), (C - 58, 174, 7), (C + 58, 174, 7)]:
        stars += [[(cx + math.cos(a + k * math.pi / 2) * r, cy + math.sin(a + k * math.pi / 2) * r) for k in range(4)] for a in (0, math.pi / 4)]
    brass = np.maximum.reduce([ring_m, cap, collar, base, drop, frame, arches])
    art = FO(art, brass, BRASS, seed=nx(), emboss=0.7, sparkle=0.15)
    art = G(art, np.maximum(cap, base) * (np.mgrid[0:H, 0:W][1] > C + 10), "#6a4214", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1)
    art = GP(art, shapes(W, H, stars, smooth=False), "#fff0c2", seed=nx(), rough=0.4)
    preview(art, "bb-lentera", bg="#3b2346")
    save(art, f"{OUT}/lentera.webp", max_w=130, quality=86)
    clear()

if "meja" in PARTS:
    W, H = 900, 420
    rng = random.Random(83); nx = Seq(83000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    TOP, FRONT = 120, 250
    top = poly_fill(W, H, [[(80, TOP), (820, TOP), (900, FRONT), (0, FRONT)]])
    cloth = shapes(W, H, [[(0, FRONT - 2), (900, FRONT - 2), (900, H - 10)] + [(900 - k * 30, H - 10 + 8 * math.sin(k * 1.3)) for k in range(31)] + [(0, H - 10)]])
    art = GP(art, cloth, "#efe3cf", "#e3d3ba", seed=nx(), rough=1.2, streak=0.4)
    folds = strokes(W, H, [([(x, FRONT + 6), (x + rng.uniform(-6, 6), H - 14)], rng.uniform(10, 18), (0.1, 0.4)) for x in range(40, 900, 90)])
    art = G(art, folds * cloth, "#c2a682", seed=nx(), density=0.3, edge=0.2, bloom=0.4, rough=3, feather=5)
    art = G(art, cloth * np.clip((yy - FRONT - 60) / 120, 0, 1), "#a98a66", seed=nx(), density=0.3, edge=0.1, bloom=0.4, rough=4, feather=4)
    runner = poly_fill(W, H, [[(0, FRONT + 8), (900, FRONT + 8), (900, FRONT + 40), (0, FRONT + 40)]])
    art = GP(art, runner, "#2f6b5a", "#245548", seed=nx(), rough=0.8, streak=0.6)
    dia = poly_fill(W, H, [[(x, FRONT + 24), (x + 10, FRONT + 14), (x + 20, FRONT + 24), (x + 10, FRONT + 34)] for x in range(6, 900, 30)])
    art = GP(art, dia, "#e6b85c", seed=nx(), rough=0.5, density=0.9)
    art = GP(art, top, "#f6ecdb", "#ecdcc2", seed=nx(), rough=1.0, streak=0.4)
    art = G(art, top * np.clip((yy - TOP) / 120, 0, 1), "#dcc6a4", seed=nx(), density=0.3, edge=0.1, bloom=0.4, rough=3)
    art = G(art, gaussian_filter(top, 30) * top * np.clip(1 - np.abs(xx - 450) / 500, 0, 1), "#f7c27a", seed=nx(), density=0.25, edge=0, bloom=0.3, rough=4)
    def shadow(cx, cy, rx, ry):
        global art
        art = G(art, shapes(W, H, [ellipse_pts(cx + 6, cy + 4, rx, ry, 20)]), "#8a6a48", seed=nx(), density=0.3, edge=0, bloom=0.2, rough=2, feather=4)
    def teapot(cx, cy, k=1.0):
        global art
        shadow(cx, cy + 30 * k, 46 * k, 9 * k)
        body = shapes(W, H, [ellipse_pts(cx, cy, 44 * k, 36 * k, 24)])
        spout = strokes(W, H, [(curve([(cx + 34 * k, cy + 8 * k), (cx + 64 * k, cy - 8 * k), (cx + 74 * k, cy - 30 * k)], 12), 9 * k, (0.0, 0.5))])
        lid = shapes(W, H, [ellipse_pts(cx, cy - 34 * k, 24 * k, 10 * k, 16), ellipse_pts(cx, cy - 44 * k, 7 * k, 7 * k, 10)])
        handle = poly_stroke(W, H, [arc_pts(cx - 42 * k, cy, 20 * k, math.pi * 0.5, math.pi * 1.5, 16)], 7 * k)
        art = GP(art, np.maximum.reduce([body, spout, lid, handle]), "#b2552f", "#8f3e20", seed=nx(), rough=0.6, streak=0.6)
        art = G(art, body * (xx > cx + 8), "#6e2c14", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=1)
        art = GP(art, strokes(W, H, [([(cx - 24 * k, cy - 14 * k), (cx - 14 * k, cy + 16 * k)], 7 * k, (0.3, 0.4))]), "#eaa784", seed=nx(), rough=0.3, density=0.6)
    def dates_plate(cx, cy):
        global art
        art = plate(art, W, H, cx, cy, 70, 22, nx, rng)
        for k in range(9):
            art = date_fruit(art, W, H, cx - 44 + k * 11 + rng.uniform(-3, 3), cy - 8 - (k % 2) * 8 + rng.uniform(-2, 2), 17, rng.uniform(-0.5, 0.5), nx, rng)
    def kolak(cx, cy):
        global art
        shadow(cx, cy + 14, 50, 8)
        bowl = shapes(W, H, [[(cx - 52, cy - 18), (cx + 52, cy - 18), (cx + 40, cy + 14), (cx - 40, cy + 14)]])
        art = GP(art, bowl, "#f2ece0", "#ddd2bf", seed=nx(), rough=0.6)
        art = G(art, bowl * (xx > cx + 10), "#b9ab95", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=1)
        art = GP(art, poly_fill(W, H, [[(cx - 52, cy - 18), (cx + 52, cy - 18), (cx + 49, cy - 9), (cx - 49, cy - 9)]]), "#3d6e9e", seed=nx(), rough=0.4)
        soup = shapes(W, H, [ellipse_pts(cx, cy - 19, 49, 9, 24)])
        art = GP(art, soup, "#c8884a", "#a86a32", seed=nx(), rough=0.6)
        art = GP(art, shapes(W, H, [ellipse_pts(cx + rng.uniform(-30, 30), cy - 20 + rng.uniform(-3, 3), 7, 4, 10, rng.uniform(0, 3)) for _ in range(7)]), "#f0c766", "#e0a840", seed=nx(), rough=0.4)
    def glass(cx, cy):
        global art
        shadow(cx, cy + 10, 24, 6)
        g = poly_fill(W, H, [[(cx - 22, cy - 74), (cx + 22, cy - 74), (cx + 18, cy + 10), (cx - 18, cy + 10)]])
        tea = poly_fill(W, H, [[(cx - 20, cy - 54), (cx + 20, cy - 54), (cx + 18, cy + 8), (cx - 18, cy + 8)]])
        art = G(art, g, "#e9eef0", seed=nx(), density=0.4, edge=0.6, bloom=0, rough=0.6, feather=0.6)
        art = G(art, tea, "#c0561e", "#9c3f12", seed=nx(), density=0.82, edge=0.4, bloom=0.2, rough=0.6, feather=0.6)
        ice = shapes(W, H, [[(cx - 13, cy - 50), (cx - 1, cy - 54), (cx + 1, cy - 40), (cx - 11, cy - 37)], [(cx + 3, cy - 42), (cx + 15, cy - 46), (cx + 16, cy - 32), (cx + 4, cy - 29)]], smooth=False)
        art = GP(art, ice, "#f4d9c2", seed=nx(), rough=0.3, density=0.6)
        art = GP(art, strokes(W, H, [([(cx - 15, cy - 68), (cx - 12, cy + 2)], 3.2, None)]), "#ffffff", seed=nx(), rough=0.3, density=0.55)
    teapot(250, TOP + 22, 0.9); teapot(668, TOP + 20, 0.8)
    glass(150, TOP + 70); glass(395, TOP + 58); glass(545, TOP + 58); glass(780, TOP + 70)
    dates_plate(300, TOP + 96); kolak(470, TOP + 100); dates_plate(640, TOP + 96)
    kolak(110, TOP + 112); dates_plate(810, TOP + 110)
    art[..., 3] *= np.clip((H - yy) / 20, 0, 1)
    preview(art, "bb-meja", bg="#4a2440")
    save(art, f"{OUT}/meja.webp", max_w=640, quality=80)
    clear()

if "kurma" in PARTS:
    W, H = 300, 170
    rng = random.Random(84); nx = Seq(84000)
    art = blank(W, H)
    art = plate(art, W, H, 150, 110, 120, 40, nx, rng)
    for k, (x, y, a) in enumerate([(92, 96, 0.4), (128, 88, -0.2), (166, 90, 0.25), (204, 98, -0.35), (110, 112, -0.1), (150, 110, 0.15), (190, 114, -0.15)]):
        art = date_fruit(art, W, H, x, y, 26, a, nx, rng)
    preview(art, "bb-kurma")
    save(art, f"{OUT}/kurma.webp", max_w=150, quality=86)
    clear()
