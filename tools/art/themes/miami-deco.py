"""Miami Deco — a pastel Art Deco beachfront in gouache: a pink stepped hotel with a central fin, eyebrow ledges, porthole
windows and a blank sign wall, flanked by mint and lemon neighbours, palms, a striped beach umbrella and sand; plus a
neon-tube flamingo (glow), a single palm, a porthole window, a pastel eyebrow divider and a terrazzo floor tile.
Original buildings, no names or brands, no text in the art.  Run: python3 -I miami-deco.py [part ...]
parts: facade neon palm porthole divider terrazzo   Assets -> public/themes/art/miami-deco/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l6_lib import *

OUT = outdir("miami-deco")
PARTS = sys.argv[1:] or ["facade", "neon", "palm", "porthole", "divider", "terrazzo"]
PINK, PINK_L, PINK_D = "#f4a9bb", "#fbd0da", "#d97f97"
MINT, MINT_D = "#a6e3cf", "#6fc2a8"
LEMON, LEMON_D = "#f8e189", "#e3bf55"
LAV = "#c9b6ea"
NAVY, TEAL, HOT = "#1f3b5c", "#3fe0d0", "#ff5fa2"
WHITE, SAND, SAND_D = "#fffaf3", "#f3dcb5", "#e2c08c"
LEAF, LEAF_D, TRUNK = "#3f9e7a", "#2b7a5e", "#b98a5e"


def paint(art, mask, c1, c2=None, seed=1, rough=1.6, streak=1.0):
    return GP(art, mask, c1, c2 or c1, seed=seed, rough=rough, streak=streak, pad=10)


def palm_masks(W, H, x, by, h, rng, lean=0.12, fronds=9):
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.25, by - h * 0.5), top], 30)
    tm = strokes(W, H, [(trunk, h * 0.045, (0.02, 0.85))])
    rings = strokes(W, H, [([(px - h * 0.02, py), (px + h * 0.02, py + 2)], 2.0, None) for px, py in trunk[2:-3:2]])
    leaves = []
    for k in range(fronds):
        a = -math.pi / 2 + (k - (fronds - 1) / 2) * 0.44 + rng.uniform(-0.08, 0.08)
        L = h * rng.uniform(0.36, 0.46)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - h * 0.03),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.5)], 24)
        leaves.append((pts, h * 0.018, (0.05, 0.6)))
        for j in range(3, 22, 2):
            px, py = pts[j]; nxp, nyp = pts[j + 1]
            ang = math.atan2(nyp - py, nxp - px)
            for sgn in (1, -1):
                qa = ang + sgn * 1.1
                ll = L * 0.13 * (1 - j / 30)
                leaves.append(([(px, py), (px + math.cos(qa) * ll * 0.6, py + math.sin(qa) * ll * 0.6 + ll * 0.2), (px + math.cos(qa) * ll, py + math.sin(qa) * ll + ll * 0.55)], h * 0.012, (0.0, 0.8)))
    return tm, rings, strokes(W, H, leaves), top


def porthole(art, W, H, cx, cy, r, nx, rim=WHITE, glass="#8fd3f0"):
    art = paint(art, circles(W, H, [(cx, cy, r)]), rim, mix(rim, "#000000", 0.06), seed=nx(), rough=0.6)
    g = circles(W, H, [(cx, cy, r * 0.72)])
    art = paint(art, g, glass, mix(glass, NAVY, 0.25), seed=nx(), rough=0.5)
    hl = strokes(W, H, [(arc_pts(cx, cy, r * 0.5, math.pi * 1.05, math.pi * 1.45, 8), r * 0.12, (0.2, 0.2))])
    art = over(art, flat(hl, "#ffffff", 0.7))
    return art


if "facade" in PARTS:
    W, H = 720, 1320
    nx = Seq(100); rng = random.Random(21)
    art = painted_sky(W, H, [(0, "#7fcdee"), (0.35, "#a9def4"), (0.62, "#d6f1f8"), (1, "#f1f8f2")], seed=5, streak=1.2)
    # sun + puffy gouache clouds
    art = over(art, glow(circles(W, H, [(600, 150, 60)]), "#fff3b0", 30, 0.45))
    art = paint(art, circles(W, H, [(600, 150, 56)]), "#fff1a6", "#ffe680", seed=nx(), rough=1.0)
    for cx, cy, s in ((150, 130, 1.0), (470, 250, 0.7)):
        cl = ellipses(W, H, [(cx, cy, 70 * s, 22 * s, 0), (cx - 40 * s, cy - 10 * s, 36 * s, 26 * s, 0), (cx + 18 * s, cy - 22 * s, 40 * s, 32 * s, 0), (cx + 60 * s, cy - 4 * s, 30 * s, 20 * s, 0)])
        art = paint(art, cl, WHITE, "#eaf6fb", seed=nx(), rough=1.4)
    clear()
    # left mint neighbour
    mint = shapes(W, H, [[(-30, 470), (120, 470), (120, 440), (150, 440), (150, 1160), (-30, 1160)]], smooth=False)
    art = paint(art, mint, MINT, "#b8ead8", seed=nx())
    art = paint(art, shapes(W, H, [rr(-30, 520 + i * 120, 150, 530 + i * 120) for i in range(5)], smooth=False), MINT_D, seed=nx(), rough=0.8)
    for i in range(5):
        for x in (20, 80):
            art = paint(art, rrect(W, H, [(x, 545 + i * 120, x + 40, 610 + i * 120, 4)]), "#7cc6e6", "#5aa9cf", seed=nx(), rough=0.6)
    # right lemon neighbour with a rounded corner tower
    lem = shapes(W, H, [[(575, 400), (700, 400), (760, 430), (760, 1160), (575, 1160)]], smooth=False)
    art = paint(art, lem, LEMON, "#fbe9a6", seed=nx())
    art = paint(art, rrect(W, H, [(575, 360, 660, 420, 30)]), LEMON_D, seed=nx(), rough=0.8)
    art = paint(art, shapes(W, H, [rr(575, 470 + i * 110, 760, 478 + i * 110) for i in range(6)], smooth=False), LEMON_D, seed=nx(), rough=0.8)
    for i in range(6):
        art = paint(art, rrect(W, H, [(600, 492 + i * 110, 700, 548 + i * 110, 26)]), "#7cc6e6", "#5aa9cf", seed=nx(), rough=0.6)
    clear()
    # the pink hotel: stepped crown, central fin, side bays
    body = shapes(W, H, [rr(120, 330, 600, 1170)], smooth=False)
    tier1 = shapes(W, H, [rr(170, 280, 550, 340)], smooth=False)
    tier2 = shapes(W, H, [rr(230, 236, 490, 290)], smooth=False)
    fin = rrect(W, H, [(318, 70, 402, 260, 40)])
    art = over(art, soft_shadow(np.clip(body + tier1 + tier2 + fin, 0, 1), NAVY, 14, 0.25, 8, 6))
    art = paint(art, np.clip(body + tier1 + tier2, 0, 1), PINK, PINK_L, seed=nx(), rough=1.4, streak=1.4)
    art = paint(art, fin, PINK_D, PINK, seed=nx(), rough=1.0)
    # fin ribs + crown eyebrows (lavender & mint accents)
    ribs = shapes(W, H, [rr(332, 100 + i * 34, 388, 110 + i * 34) for i in range(5)], smooth=False)
    art = paint(art, ribs, LAV, "#b7a2e0", seed=nx(), rough=0.6)
    brows = shapes(W, H, [rr(160, 330, 560, 346), rr(222, 284, 498, 298), rr(110, 400, 610, 414)], smooth=False)
    art = paint(art, brows, MINT, MINT_D, seed=nx(), rough=0.7)
    # side bays: vertical window stacks with eyebrow shelves (both sides)
    for bx in (148, 482):
        for i in range(6):
            y = 440 + i * 108
            art = paint(art, rrect(W, H, [(bx, y, bx + 90, y + 66, 6)]), "#7cc6e6", "#4f9ec6", seed=nx(), rough=0.6)
            art = paint(art, shapes(W, H, [rr(bx - 10, y - 12, bx + 100, y - 3)], smooth=False), PINK_D, seed=nx(), rough=0.5)
            art = over(art, flat(gaussian_filter(shapes(W, H, [rr(bx - 6, y - 3, bx + 96, y + 6)], smooth=False), 2.5), NAVY, 0.22))
            art = over(art, flat(shapes(W, H, [rr(bx + 43, y, bx + 47, y + 66)], smooth=False), WHITE, 0.8))
    # porthole row over the sign wall
    for cx in (290, 360, 430):
        art = porthole(art, W, H, cx, 452, 22, nx)
    # blank sign wall (the page lays the neon sign here) with a pale inset
    art = paint(art, rrect(W, H, [(258, 500, 462, 760, 10)]), PINK_L, "#fde2e8", seed=nx(), rough=0.8)
    # central vertical glazing under the sign + canopy entrance
    art = paint(art, rrect(W, H, [(300, 790, 420, 990, 60)]), "#7cc6e6", "#4f9ec6", seed=nx(), rough=0.6)
    art = over(art, flat(shapes(W, H, [rr(357, 792, 363, 990)] + [rr(300, 840 + i * 50, 420, 845 + i * 50) for i in range(3)], smooth=False), WHITE, 0.8))
    canopy = rrect(W, H, [(230, 1012, 490, 1046, 17)])
    art = over(art, soft_shadow(canopy, NAVY, 6, 0.3, 0, 8))
    art = paint(art, canopy, MINT, MINT_D, seed=nx(), rough=0.6)
    door = rrect(W, H, [(318, 1052, 402, 1170, 6)])
    art = paint(art, door, "#2f5f86", NAVY, seed=nx(), rough=0.6)
    clear()
    # sidewalk + sand
    walk = shapes(W, H, [rr(-20, 1160, W + 20, 1200)], smooth=False)
    art = paint(art, walk, "#fbeee0", "#f1dfcc", seed=nx(), rough=0.8)
    sand = wavy_band(W, H, 1196, H + 40, 4, 8, 0.9)
    art = paint(art, sand, SAND, "#f7e5c4", seed=nx(), rough=1.4, streak=1.6)
    speck = dabs(W, H, 260, (0, 1205, W, H), 0.8, 2.0, rng)
    art = over(art, flat(speck, SAND_D, 0.7))
    # palms in front (left tall, right medium)
    for x, by, h, lean in ((92, 1250, 600, 0.05), (632, 1256, 520, -0.06)):
        tm, rings, lv, top = palm_masks(W, H, x, by, h, rng, lean)
        art = paint(art, tm, TRUNK, "#cfa274", seed=nx(), rough=0.8)
        art = over(art, flat(rings, "#8a6240", 0.8))
        art = paint(art, lv, LEAF, LEAF_D, seed=nx(), rough=0.8)
        art = paint(art, circles(W, H, [(top[0] - 8, top[1] + 10, 9), (top[0] + 8, top[1] + 12, 9)]), "#8a6240", seed=nx(), rough=0.5)
        clear()
    # striped beach umbrella (right foreground)
    ux, uy, ur = 560, 1196, 110
    canopy_pts = [(ux + math.cos(a) * ur, uy + math.sin(a) * ur * 0.42) for a in np.linspace(math.pi, math.tau, 24)] + [(ux + ur, uy + 6), (ux - ur, uy + 6)]
    um = shapes(W, H, [canopy_pts], smooth=False)
    art = paint(art, strokes(W, H, [([(ux, uy - 40), (ux + 8, uy + 120)], 5, None)]), WHITE, seed=nx(), rough=0.4)
    art = paint(art, um, WHITE, seed=nx(), rough=0.8)
    stripes = np.zeros((H, W), np.float32)
    for k in range(0, 6, 2):
        a0, a1 = math.pi + k * math.pi / 6, math.pi + (k + 1) * math.pi / 6
        stripes += shapes(W, H, [[(ux, uy - ur * 0.42 + 2)] + [(ux + math.cos(a) * ur * 1.05, uy + 6 + math.sin(a) * ur * 0.42 * 1.05) for a in np.linspace(a0, a1, 6)]], smooth=False)
    art = paint(art, np.clip(stripes, 0, 1) * um, HOT, "#ff7fb4", seed=nx(), rough=0.6)
    art = add_grain(art, 6, 0.035)
    show(art, "miami-facade", bg=WHITE)
    save_rgb(art, f"{OUT}/facade.webp", (720, 1320), quality=76)
    clear()

if "neon" in PARTS:
    W, H = 420, 520
    nx = Seq(300)
    art = blank(W, H)
    # flamingo outline: body, S-neck, head + beak, standing leg with a bent leg
    body = ellipse_pts(200, 250, 92, 52, 40, rot=-0.18)
    body = body + [body[0]]
    neck = curve([(272, 222), (300, 170), (268, 120), (250, 78), (276, 48), (306, 56)], 50)
    beak = [(306, 56), (326, 70), (318, 86), (304, 74)]
    leg = [(196, 300), (194, 380), (196, 470)]
    leg2 = curve([(214, 298), (232, 360), (176, 352), (190, 380)], 20)
    wing = curve([(140, 238), (190, 220), (250, 240)], 20)
    tube = strokes(W, H, [(body, 6, None), (neck, 6, None), (beak, 6, None), (leg, 5, None), (leg2, 5, None), (wing, 5, None), ([(150, 470), (250, 470)], 5, None)])
    art = over(art, glow(tube, HOT, 16, 0.55))
    art = over(art, glow(tube, "#ff9cc8", 5, 0.6))
    art = paint(art, tube, "#ffe3f0", "#ffd0e6", seed=nx(), rough=0.4)
    # wave line under (teal tube)
    wave = [(x, 500 + 9 * math.sin(x / 22)) for x in range(70, 351, 6)]
    wt = strokes(W, H, [(wave, 5, None)])
    art = over(art, glow(wt, TEAL, 12, 0.55))
    art = paint(art, wt, "#d9fffa", seed=nx(), rough=0.4)
    show(art, "miami-neon", bg=NAVY)
    save(art, f"{OUT}/neon.webp", max_w=300, quality=84)
    clear()

if "palm" in PARTS:
    W, H = 560, 720
    nx = Seq(400); rng = random.Random(4)
    art = blank(W, H)
    tm, rings, lv, top = palm_masks(W, H, 250, 710, 480, rng, 0.08)
    art = paint(art, tm, TRUNK, "#cfa274", seed=nx(), rough=0.8)
    art = over(art, flat(rings, "#8a6240", 0.8))
    art = paint(art, lv, LEAF, LEAF_D, seed=nx(), rough=0.8)
    show(art, "miami-palm")
    save(art, f"{OUT}/palm.webp", max_w=240, quality=82)
    clear()

if "porthole" in PARTS:
    W, H = 200, 200
    nx = Seq(500)
    art = blank(W, H)
    art = paint(art, circles(W, H, [(100, 100, 90)]), PINK, PINK_D, seed=nx(), rough=0.8)
    art = porthole(art, W, H, 100, 100, 70, nx)
    show(art, "miami-porthole")
    save(art, f"{OUT}/porthole.webp", max_w=120, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 440, 70
    nx = Seq(600)
    art = blank(W, H)
    for k, (w, c) in enumerate(((150, PINK), (118, MINT), (86, LEMON))):
        y = 18 + k * 13
        art = paint(art, rrect(W, H, [(200 - 30 - w, y, 170, y + 8, 4), (270, y, 270 + w, y + 8, 4)]), c, mix(c, "#000000", 0.08), seed=nx(), rough=0.7)
    art = paint(art, circles(W, H, [(220, 35, 26)]), LAV, "#b7a2e0", seed=nx(), rough=0.6)
    art = porthole(art, W, H, 220, 35, 20, nx)
    show(art, "miami-divider")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()

if "terrazzo" in PARTS:
    W = H = 360
    rng = random.Random(8)
    base = np.asarray(paper(W, H, "#fbf3ec", seed=3, fiber=0.3, mottle=0.6), np.float32) / 255
    art = np.concatenate([base, np.ones((H, W, 1), np.float32)], -1)
    for col, n in ((PINK, 70), (MINT, 60), (LEMON, 40), (LAV, 40), ("#8fd3f0", 30)):
        polys = []
        for _ in range(n):
            cx, cy = rng.uniform(0, W), rng.uniform(0, H)
            r = rng.uniform(2.5, 7)
            pts = [(cx + math.cos(a) * r * rng.uniform(0.6, 1.2), cy + math.sin(a) * r * rng.uniform(0.6, 1.2)) for a in np.linspace(0, math.tau, 6, endpoint=False)]
            polys += [pts] + [[(x + dx, y + dy) for x, y in pts] for dx in (-W, 0, W) for dy in (-H, 0, H) if (dx, dy) != (0, 0)]
        m = shapes(W, H, polys, smooth=False)
        art = over(art, flat(m, col, 0.75))
    save_rgb(art, f"{OUT}/terrazzo.webp", quality=74)
