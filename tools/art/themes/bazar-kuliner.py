"""Bazar Kuliner — night food-bazaar poster in gouache: striped stall tents under string lights, smoke from the sate grill,
a crowd in silhouette; food spot illustrations (sate, martabak manis, es cendol) and a light garland.
Run: python3 -I bazar-kuliner.py [part ...]   parts: stalls lights sate martabak cendol
Assets -> public/themes/art/bazar-kuliner/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o6_lib import *

OUT = outdir("bazar-kuliner")
PARTS = sys.argv[1:] or ["stalls", "lights", "sate", "martabak", "cendol"]
NIGHT, NIGHT2 = "#231a3d", "#2f2552"
RED, RED_D = "#d9463b", "#a8302a"
TEAL, TEAL_D = "#1f8a86", "#16625f"
MUST, MUST_D = "#f0b13a", "#c98a22"
CREAM = "#f6e7c8"
WOOD, WOOD_D = "#9a5f36", "#6e3f22"
BULB = "#ffd36b"
LINE = "#2a1d18"

random.seed(5)


def paint(art, mask, col, col2=None, streak=0.7, ln=0.55, px=1.3):
    art = GP(art, mask, col, col2 or mix(col, "#000000", .14), seed=random.randint(1, 10**6), rough=1.6, streak=streak, pad=10)
    if ln:
        rim = np.clip((mask - gaussian_filter(mask, px)) * 3.2, 0, 1)
        art = G(art, rim, LINE, seed=random.randint(1, 10**6), density=ln, edge=0, bloom=0, rough=0.8, feather=0.35, pad=6)
    return art


def glow_on(art, mask, col, radius, strength):
    g = glow(mask, col, radius, strength)
    return over(art, g)


def string_lights(W, H, art, spans, nx, rng, bulb_r=6.5, glow_r=14):
    wire = []; bulbs = []
    for (x0, y0, x1, y1, sag) in spans:
        pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * math.sin(math.pi * t)) for t in np.linspace(0, 1, 60)]
        wire.append((pts, 1.8, None))
        for (x, y, a) in along(pts, 34):
            bulbs.append((x, y + bulb_r + 2, bulb_r))
    art = G(art, strokes(W, H, wire), "#14101f", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5, pad=6)
    bm = ellipses(W, H, [(x, y, r * 0.8, r, 0) for x, y, r in bulbs])
    art = glow_on(art, bm, BULB, glow_r, 0.55)
    cols = [BULB, "#ffb35c", "#fff0b8", BULB, "#ff8f6b"]
    for k, col in enumerate(cols):
        sub = ellipses(W, H, [(x, y, r * 0.8, r, 0) for x, y, r in bulbs[k::len(cols)]])
        art = GP(art, sub, col, "#fff6d8", seed=nx(), rough=0.6, streak=0.2, pad=6)
    art = GP(art, ellipses(W, H, [(x - r * .25, y - r * .3, r * .22, r * .3, 0) for x, y, r in bulbs]), "#fffdf0", seed=nx(), rough=0.4, pad=4)
    return art


if "stalls" in PARTS:
    W, H = 780, 700
    rng = random.Random(3); nx = Seq(300)
    art = blank(W, H)
    # far silhouettes: rooftops & a tree line, barely lighter than the sky
    sil = shapes(W, H, [[(0, 250), (40, 200), (90, 210), (120, 170), (170, 180), (220, 150), (260, 160), (330, 140), (380, 170), (430, 150), (500, 160), (560, 130), (610, 160), (680, 150), (720, 180), (780, 170), (780, 400), (0, 400)]])
    art = paint(art, sil, "#2d2350", "#251c45", ln=0)
    # stalls: (x0, x1, stripe colour, counter colour)
    specs = [(-20, 270, RED, WOOD), (250, 530, TEAL, "#c9773e"), (510, 800, MUST, WOOD)]
    for i, (x0, x1, sc, cc) in enumerate(specs):
        top, low, ctop, cbot = 200 + (i % 2) * 14, 290 + (i % 2) * 14, 430, 540
        # lit back wall
        back = shapes(W, H, [[(x0 + 14, low - 6), (x1 - 14, low - 6), (x1 - 14, ctop), (x0 + 14, ctop)]], smooth=False)
        art = paint(art, back, "#f7cf86", "#e9a85a", ln=0)
        # wares on the back shelf: jars, hanging bananas/krupuk bags, a menu board (no text: coloured price tags)
        shelf = strokes(W, H, [([(x0 + 24, low + 60), (x1 - 24, low + 60)], 5, None)])
        art = paint(art, shelf, WOOD_D, ln=0)
        jars = [(x0 + 40 + k * 34, low + 40, 12) for k in range(int((x1 - x0 - 80) / 34))]
        jm = ellipses(W, H, [(x, y, r * .8, r * 1.2, 0) for x, y, r in jars])
        art = paint(art, jm, rng.choice(["#e06a4a", "#7fae5a", "#f2c14e", "#c9a0dc"]), ln=0.4)
        board = shapes(W, H, [[(x0 + (x1 - x0) * .3, low + 76), (x0 + (x1 - x0) * .7, low + 76), (x0 + (x1 - x0) * .7, low + 122), (x0 + (x1 - x0) * .3, low + 122)]], smooth=False)
        art = paint(art, board, "#2b2a2e", "#1c1b1f", ln=0.5)
        tags = strokes(W, H, [([(x0 + (x1 - x0) * .34, low + 88 + 11 * k), (x0 + (x1 - x0) * (.5 + .12 * ((k + i) % 2)), low + 88 + 11 * k)], 3.2, None) for k in range(3)])
        art = paint(art, tags, CREAM, ln=0)
        # poles
        poles = strokes(W, H, [([(x0 + 14, top), (x0 + 14, cbot + 30)], 8, None), ([(x1 - 14, top), (x1 - 14, cbot + 30)], 8, None)])
        art = paint(art, poles, "#5a3a26", ln=0.5)
        # striped awning with scalloped hem
        aw = [(x0, low), (x0 + 10, top), (x1 - 10, top), (x1, low)]
        sc_n = 7
        hem = []
        for k in range(sc_n * 8 + 1):
            t = k / (sc_n * 8)
            x = x1 + (x0 - x1) * t
            hem.append((x, low + 16 * abs(math.sin(t * sc_n * math.pi))))
        awm = shapes(W, H, [[(x0 + 10, top), (x1 - 10, top), (x1, low)] + hem + [(x0, low)]], smooth=False)
        art = paint(art, awm, CREAM, "#e8d3a8")
        stripes = shapes(W, H, [[(x0 + 10 + (x1 - x0 - 20) * k / sc_n, top), (x0 + 10 + (x1 - x0 - 20) * (k + .5) / sc_n, top),
                                  (x0 + (x1 - x0) * (k + .5) / sc_n, low + 18), (x0 + (x1 - x0) * k / sc_n, low + 18)] for k in range(sc_n)], smooth=False) * awm
        art = paint(art, stripes, sc, mix(sc, "#000000", .15), ln=0)
        art = soft(art, awm * np.clip((np.mgrid[0:H, 0:W][0] - top) / 90.0, 0, 1), "#3a2440", nx(), 0.3)
        # sign board on top of the awning (blank, with a painted food icon circle)
        sb = shapes(W, H, [[(x0 + (x1 - x0) * .22, top - 46), (x0 + (x1 - x0) * .78, top - 46), (x0 + (x1 - x0) * .78, top - 4), (x0 + (x1 - x0) * .22, top - 4)]], smooth=False)
        art = paint(art, sb, "#fff3d6", "#f1dcb0")
        icon = circles(W, H, [(x0 + (x1 - x0) * .32, top - 25, 12)])
        art = paint(art, icon, sc, ln=0.4)
        bar = strokes(W, H, [([(x0 + (x1 - x0) * .4, top - 30), (x0 + (x1 - x0) * .7, top - 30)], 6, None), ([(x0 + (x1 - x0) * .4, top - 17), (x0 + (x1 - x0) * .62, top - 17)], 4, None)])
        art = paint(art, bar, LINE, ln=0)
        # counter
        ctr = shapes(W, H, [[(x0 + 6, ctop), (x1 - 6, ctop), (x1 - 2, cbot), (x0 + 2, cbot)]], smooth=False)
        art = paint(art, ctr, cc, mix(cc, "#000000", .25))
        planks = strokes(W, H, [([(x0 + 10 + k * 26, ctop + 14), (x0 + 10 + k * 26, cbot - 4)], 2, None) for k in range(int((x1 - x0) / 26))]) * ctr
        art = soft(art, planks, WOOD_D, nx(), 0.45)
        lip = shapes(W, H, [[(x0, ctop - 8), (x1, ctop - 8), (x1, ctop + 8), (x0, ctop + 8)]], smooth=False)
        art = paint(art, lip, "#e9d2a6", "#cdb185")
        # food on the counter
        if i == 0:   # sate grill with skewers + smoke
            grill = shapes(W, H, [[(60, ctop - 30), (210, ctop - 30), (204, ctop - 8), (66, ctop - 8)]], smooth=False)
            art = paint(art, grill, "#3a3a3e", "#26262a")
            art = glow_on(art, strokes(W, H, [([(70, ctop - 26), (200, ctop - 26)], 6, None)]), "#ff7a3a", 8, 0.7)
            sk = []; meat = []
            for k in range(9):
                x = 72 + k * 15
                sk.append(([(x - 6, ctop - 30), (x + 10, ctop - 60)], 2, None))
                for j in range(3):
                    meat.append((x - 3 + j * 4.5, ctop - 36 - j * 8, 4.6))
            art = paint(art, strokes(W, H, sk), "#d8b47a", ln=0)
            art = paint(art, circles(W, H, meat), "#7a3b1e", "#5a2a14", ln=0.3)
            smoke = shapes(W, H, [deform(ellipse_pts(130 + k * 14 + math.sin(k) * 20, ctop - 90 - k * 34, 34 + k * 6, 18 + k * 3, 12), rng, 2, .15) for k in range(5)])
            art = G(art, smoke, "#e9e2f0", "#b9b0cc", seed=nx(), density=0.38, edge=0.3, bloom=0.5, rough=6, pad=16)
        elif i == 1:  # big wok of martabak, stacked wedges
            pan = ellipses(W, H, [(330, ctop - 14, 52, 14, 0)])
            art = paint(art, pan, "#3a3a3e", "#26262a")
            stack = shapes(W, H, [[(410, ctop - 8), (480, ctop - 8), (470, ctop - 40), (418, ctop - 40)]], smooth=False)
            art = paint(art, stack, "#e7a94e", "#c9822e")
            fill = strokes(W, H, [([(414, ctop - 18), (476, ctop - 18)], 5, None), ([(416, ctop - 30), (472, ctop - 30)], 4, None)])
            art = paint(art, fill, "#5a3018", ln=0)
            art = paint(art, circles(W, H, [(x, ctop - 42, 2.5) for x in range(422, 470, 7)]), "#fff1c4", ln=0)
        else:  # es cendol jars + glasses
            for k, x in enumerate([570, 610, 650, 690]):
                g = shapes(W, H, [[(x - 13, ctop - 46), (x + 13, ctop - 46), (x + 10, ctop - 6), (x - 10, ctop - 6)]], smooth=False)
                art = paint(art, g, "#f3efe0", "#e2dcc6", ln=0.45)
                lay = shapes(W, H, [[(x - 11, ctop - 24), (x + 11, ctop - 24), (x + 10, ctop - 8), (x - 10, ctop - 8)]], smooth=False)
                art = paint(art, lay, "#6f9e3c", "#4f7d2a", ln=0)
                art = paint(art, shapes(W, H, [[(x - 10, ctop - 12), (x + 10, ctop - 12), (x + 10, ctop - 6), (x - 10, ctop - 6)]], smooth=False), "#7a4a24", ln=0)
            jar = ellipses(W, H, [(740, ctop - 34, 26, 32, 0)])
            art = paint(art, jar, "#cfe6d8", "#a9cdb9")
            art = paint(art, ellipses(W, H, [(740, ctop - 26, 22, 20, 0)]) * jar, "#7fae4a", ln=0)
        # warm light pooling under the awning
        lm = shapes(W, H, [[(x0 + 30, low + 20), (x1 - 30, low + 20), (x1 - 10, cbot), (x0 + 10, cbot)]], smooth=False)
        art = over(art, glow(lm, "#ffd98a", 30, 0.18))
        clear()
    # string lights criss-crossing above the stalls
    art = string_lights(W, H, art, [(-10, 40, 400, 70, 50), (380, 70, 790, 30, 60), (-10, 120, 790, 110, 70)], nx, rng)
    # crowd in silhouette, two rows (back row lighter), warm rim light from the stalls; one raised hand holds a skewer
    def person(x, hy, hr, hood=False):
        polys = [deform(ellipse_pts(x, hy, hr * 0.88, hr, 14), rng, 1, 0.02)]
        polys.append([(x - hr * 1.9, H + 20), (x - hr * 1.75, hy + hr * 2.0), (x - hr * 1.2, hy + hr * 1.35), (x - hr * .45, hy + hr * 1.05),
                      (x + hr * .45, hy + hr * 1.05), (x + hr * 1.2, hy + hr * 1.35), (x + hr * 1.75, hy + hr * 2.0), (x + hr * 1.9, H + 20)])
        if hood:
            polys.append(deform(ellipse_pts(x, hy + hr * .35, hr * 1.12, hr * 1.18, 14), rng, 1, 0.02))
        return polys
    for row, (y0, hr0, col, col2, step) in enumerate([(548, 17, "#3b2e5e", "#33285a", 62), (604, 25, "#1a1330", "#130e24", 92)]):
        polys = []; rims = []
        x = rng.uniform(-30, 0)
        while x < W + 40:
            hr = hr0 * rng.uniform(0.88, 1.12)
            hy = y0 + rng.uniform(-10, 10)
            polys += person(x, hy, hr, hood=rng.random() < 0.3)
            rims.append(arc_pts(x, hy, hr * 0.92, math.pi * 1.05, math.pi * 1.95, 14))
            x += step * rng.uniform(0.85, 1.15)
        pm = shapes(W, H, polys)
        if row == 1:
            pm = np.maximum(pm, strokes(W, H, [([(612, 640), (626, 560), (636, 520)], 10, None)]))
        art = paint(art, pm, col, col2, ln=0)
        rimm = strokes(W, H, [(r, 3.2 if row else 2.4, (0.25, 0.25)) for r in rims]) * np.clip(gaussian_filter(pm, 2) * 1.6, 0, 1)
        art = G(art, np.clip(rimm, 0, 1), "#ffb15c", seed=nx(), density=0.55 if row else 0.4, edge=0, bloom=0, rough=0.6, pad=6)
    art = paint(art, strokes(W, H, [([(636, 520), (654, 474)], 2.2, None)]), "#d8b47a", ln=0)
    art = paint(art, circles(W, H, [(642, 504, 4.4), (646, 494, 4.4), (650, 484, 4.4)]), "#7a3b1e", ln=0.3)
    art = add_grain(art, 9, 0.03)
    art[:, -8:] = art[:, -9:-8]; art[:, :8] = art[:, 8:9]; art[-6:] = art[-7:-6]
    save(art, f"{OUT}/stalls.webp", max_w=780, quality=78)
    prev(art, "bk_stalls", bg=NIGHT)

if "lights" in PARTS:
    W, H = 560, 110
    rng = random.Random(7); nx = Seq(700)
    art = string_lights(W, H, blank(W, H), [(10, 22, 550, 22, 46)], nx, rng, bulb_r=7, glow_r=12)
    save(art, f"{OUT}/lights.webp", max_w=400, quality=84)
    prev(art, "bk_lights", bg=NIGHT)

if "sate" in PARTS:
    # plate of sate on a banana-leaf, peanut sauce, lontong slices
    W, H = 340, 260
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    plate = ellipses(W, H, [(170, 170, 150, 64, 0)])
    art = paint(art, plate, "#f4efe3", "#ddd4c0")
    leaf = shapes(W, H, [petal_pts(40, 170, 270, 52, -0.05, n=16)])
    art = paint(art, leaf * plate, "#5f9a43", "#3f7a2e", ln=0.4)
    art = soft(art, strokes(W, H, [([(50, 168), (300, 158)], 2, None)]) * leaf, "#2f5e22", nx(), 0.5)
    sauce = ellipses(W, H, [(230, 186, 52, 22, -4)])
    art = paint(art, sauce, "#a8622e", "#7a4318", ln=0.4)
    art = paint(art, circles(W, H, [(210 + rng.uniform(0, 40), 184 + rng.uniform(-8, 8), 2.4) for _ in range(14)]), "#d79a4c", ln=0)
    for x, y in [(96, 196), (124, 202)]:
        lon = ellipses(W, H, [(x, y, 16, 11, 0)])
        art = paint(art, lon, "#f1edd8", "#dcd6b8", ln=0.4)
        art = soft(art, ellipses(W, H, [(x, y, 10, 6, 0)]), "#b9c48a", nx(), 0.4)
    for k in range(6):
        y0 = 120 + k * 9
        stick = strokes(W, H, [([(40 + k * 6, y0 + 40), (300 - k * 4, y0 - 24)], 3, None)])
        art = paint(art, stick, "#d8b47a", "#b8935a", ln=0.3)
        chunks = [(90 + k * 6 + j * 30 + rng.uniform(-2, 2), y0 + 30 - (j * 30 + k * 6) * 0.25 + rng.uniform(-2, 2), 11) for j in range(5)]
        cm = shapes(W, H, [deform(ellipse_pts(x, y, r, r * .82, 10, -0.25), rng, 1, .1) for x, y, r in chunks])
        art = paint(art, cm, "#8a4422", "#5e2a14", ln=0.45)
        art = soft(art, shapes(W, H, [ellipse_pts(x - 3, y - 4, r * .45, r * .3, 8, -0.25) for x, y, r in chunks]) * cm, "#c9783e", nx(), 0.5)
        art = G(art, circles(W, H, [(x + rng.uniform(-5, 5), y + rng.uniform(-4, 4), 1.6) for x, y, r in chunks for _ in range(3)]) * cm, "#2a120a", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, pad=4)
    save(art, f"{OUT}/sate.webp", max_w=240, quality=84)
    prev(art, "bk_sate", tone="#fdf3e0")

if "martabak" in PARTS:
    # stacked wedges of martabak manis: thick honeycomb crumb, chocolate, cheese and peanut layers, on paper
    W, H = 320, 260
    rng = random.Random(13); nx = Seq(1300)
    art = blank(W, H)
    paperm = shapes(W, H, [[(30, 200), (290, 190), (300, 236), (24, 244)]])
    art = paint(art, paperm, "#f4ead2", "#e3d4b2")
    for k, (ox, oy) in enumerate([(70, 150), (150, 120), (196, 168)]):
        top = [(ox, oy), (ox + 90, oy - 22), (ox + 110, oy + 4), (ox + 20, oy + 30)]
        side = [(ox + 20, oy + 30), (ox + 110, oy + 4), (ox + 110, oy + 56), (ox + 20, oy + 82)]
        sm = shapes(W, H, [side], smooth=False)
        art = paint(art, sm, "#e8b65a", "#c98d36")
        holes = circles(W, H, [(ox + 30 + rng.uniform(0, 74), oy + 40 + rng.uniform(0, 34), rng.uniform(1.6, 3)) for _ in range(40)]) * sm
        art = soft(art, holes, "#9a5f22", nx(), 0.6)
        layer = strokes(W, H, [([(ox + 22, oy + 56), (ox + 108, oy + 30)], 7, None)]) * sm
        art = paint(art, layer, "#4a2614", "#341a0c", ln=0)
        cheese = strokes(W, H, [([(ox + 22, oy + 47), (ox + 108, oy + 21)], 3, None)]) * sm
        art = paint(art, cheese, "#f6d65a", ln=0)
        tm = shapes(W, H, [top], smooth=False)
        art = paint(art, tm, "#c97c2e", "#a85f1e")
        art = paint(art, circles(W, H, [(ox + 20 + rng.uniform(0, 80), oy + rng.uniform(-6, 20), 2.6) for _ in range(18)]) * tm, "#f3d9a0", ln=0)
        art = soft(art, strokes(W, H, [([(ox + 14, oy + 14), (ox + 96, oy - 8)], 5, None)]) * tm, "#4a2614", nx(), 0.6)
    save(art, f"{OUT}/martabak.webp", max_w=220, quality=84)
    prev(art, "bk_martabak", tone="#fdf3e0")

if "cendol" in PARTS:
    W, H = 200, 320
    rng = random.Random(17); nx = Seq(1700)
    art = blank(W, H)
    glass = shapes(W, H, [[(36, 60), (164, 60), (148, 290), (52, 290)]], smooth=False)
    # contents: gula aren at the bottom, green cendol worms, coconut milk, ice cubes
    inner = shapes(W, H, [[(42, 92), (158, 92), (146, 284), (54, 284)]], smooth=False)
    art = paint(art, inner, "#f5efe2", "#e9e0cc", ln=0)
    art = paint(art, shapes(W, H, [[(48, 236), (152, 236), (146, 284), (54, 284)]], smooth=False), "#6e3b1a", "#4e2a12", ln=0)
    worms = strokes(W, H, [(curve([(x, y), (x + rng.uniform(-6, 6), y + 9), (x + rng.uniform(-6, 6), y + 18)], 8), 6, (0.2, 0.2)) for x, y in [(rng.uniform(56, 144), rng.uniform(170, 232)) for _ in range(34)]]) * inner
    art = paint(art, worms, "#7fb24a", "#5a8e2e", ln=0.3)
    for (x, y) in [(76, 110), (118, 104), (98, 136)]:
        ice = shapes(W, H, [deform(ellipse_pts(x, y, 20, 16, 4, 0.4), rng, 1, .05)], smooth=False)
        art = G(art, ice, "#ffffff", "#dceaf0", seed=nx(), density=0.75, edge=0.6, bloom=0.2, rough=2, pad=8)
    art = soft(art, strokes(W, H, [([(52, 70), (62, 270)], 7, None)]) * glass, "#ffffff", nx(), 0.5)
    rim = np.clip((glass - gaussian_filter(glass, 2)) * 3, 0, 1)
    art = G(art, rim, "#8aa0a6", seed=nx(), density=0.65, edge=0, bloom=0, rough=0.6, pad=6)
    straw = strokes(W, H, [([(118, 250), (140, 40), (168, 22)], 8, None)])
    art = paint(art, straw * (1 - inner * 0.6), RED, RED_D, ln=0.4)
    save(art, f"{OUT}/cendol.webp", max_w=130, quality=84)
    prev(art, "bk_cendol", tone="#fdf3e0")

kb(OUT)
