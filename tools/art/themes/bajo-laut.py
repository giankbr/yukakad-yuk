"""Bajo Laut — painted pieces: a Bajau stilt village over a turquoise sea (watercolour washes, gouache plank walls,
pole reflections), a lepa boat with a striped sail (separate, bobs), a seagrass-and-coral strip (separate, sways),
a fishing-net tile, a rope-and-float divider and a small coral sprig.
Run: python3 -I bajo-laut.py [part ...]  parts: village lepa reef net divider sprig"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k3_lib import *

OUT = outdir("bajo-laut")
PARTS = sys.argv[1:] or ["village", "lepa", "reef", "net", "divider", "sprig"]
SEA_BOTTOM = "#3fb2b0"
SKY = "#eef6f2"


def house(W, H, x, floor, w, wall, roof, rng, kind=0):
    """Stilt house masks: walls, roof, door/windows, poles (to the water line set later), deck."""
    walls = shapes(W, H, [[(x, floor), (x, floor - wall), (x + w, floor - wall), (x + w, floor)]], smooth=False)
    ov = w * 0.08
    if kind == 0:  # gable facing us
        rf = [(x - ov, floor - wall + 2), (x + w / 2, floor - wall - roof), (x + w + ov, floor - wall + 2)]
    else:  # hip roof seen from the side
        rf = [(x - ov, floor - wall + 2), (x + w * 0.22, floor - wall - roof), (x + w * 0.78, floor - wall - roof), (x + w + ov, floor - wall + 2)]
    roofm = shapes(W, H, [rf], smooth=False)
    holes = []
    dw = max(4, w * 0.14)
    holes.append([(x + w * 0.42, floor), (x + w * 0.42, floor - wall * 0.72), (x + w * 0.42 + dw, floor - wall * 0.72), (x + w * 0.42 + dw, floor)])
    for wx in (x + w * 0.12, x + w * 0.7):
        holes.append([(wx, floor - wall * 0.45), (wx, floor - wall * 0.75), (wx + w * 0.16, floor - wall * 0.75), (wx + w * 0.16, floor - wall * 0.45)])
    openings = shapes(W, H, holes, smooth=False)
    planks = strokes(W, H, [([(x + 1, floor - wall * f), (x + w - 1, floor - wall * f)], 0.9, None) for f in (0.18, 0.36, 0.54, 0.72, 0.9)]) * walls
    return walls, roofm, openings, planks


if "village" in PARTS:
    W, H = 780, 560
    WL = 352  # water line
    nx = Seq(61100); rng = random.Random(5)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # soft clouds
    for (x, y, rx, ry) in [(140, 70, 110, 18), (230, 56, 70, 14), (560, 110, 130, 16), (660, 96, 60, 12)]:
        art = G(art, shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 12), rng, 2, 0.12)]), "#cfe3e4", "#e2eeea", seed=nx(), density=0.35, edge=0.4, bloom=0.4, rough=6)
    # distant island
    isl = shapes(W, H, [[(380, WL + 2), (430, WL - 34), (500, WL - 52), (580, WL - 46), (650, WL - 22), (720, WL + 2)]])
    art = G(art, isl, "#9cc0b7", "#b4cfc4", seed=nx(), density=0.6, edge=0.5, bloom=0.3, rough=4)
    art = G(art, isl * np.clip((yy - (WL - 50)) / 50, 0, 1), "#7aa79c", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=3)
    # water: opaque painted gradient with brush streaks, fades from pale sky-tint at the horizon to turquoise
    water = painted_sky(W, H, [(0, "#bfe7df"), (WL / H, "#bfe7df"), ((WL + 30) / H, "#8fd6cf"), ((WL + 110) / H, "#5ec4c0"), (1, SEA_BOTTOM)], seed=nx(), streak=1.2)
    wm = (yy >= WL).astype(np.float32)
    wm = np.clip(gaussian_filter(wm, 0.8), 0, 1)
    water[..., 3] = wm
    art = over(art, water)
    # sandy shallows patches (lighter) and seagrass darker patches below the surface
    for k in range(9):
        cx_, cy_ = rng.uniform(0, W), rng.uniform(WL + 60, H - 30)
        art = G(art, shapes(W, H, [deform(ellipse_pts(cx_, cy_, rng.uniform(60, 130), rng.uniform(8, 18), 12), rng, 2, 0.2)]), rng.choice(["#d9f1e6", "#2f9a98"]), seed=nx(), density=0.28, edge=0.25, bloom=0.4, rough=6, feather=3)
    clear()
    # houses: back row (smaller) then front row
    rows = [
        # (x, floor, w, wall, roof, kind)
        [(70, WL - 26, 62, 30, 26, 1), (300, WL - 30, 58, 28, 28, 0), (520, WL - 28, 66, 30, 24, 1), (650, WL - 26, 54, 26, 26, 0)],
        [(-10, WL - 44, 120, 56, 46, 0), (150, WL - 40, 104, 50, 40, 1), (370, WL - 46, 116, 58, 48, 0), (560, WL - 42, 104, 52, 36, 1), (690, WL - 46, 110, 56, 46, 0)],
    ]
    wall_cols = [("#e8d2a4", "#d8bb85"), ("#d9e3d6", "#c3d2c4"), ("#e9c9a1", "#d6ad7d"), ("#f1e3c2", "#dcc79a")]
    roof_cols = [("#8a6a48", "#6d5236"), ("#9aa4a6", "#7d888b"), ("#a7744a", "#875a36")]
    for ri, row in enumerate(rows):
        for (x, floor, w, wall, roof, kind) in row:
            depth = 22 if ri == 0 else 64
            pole_items = []
            for px in np.linspace(x + 4, x + w - 4, max(3, int(w / 22))):
                pole_items.append(([(px, floor), (px + rng.uniform(-1, 1), WL + depth * 0.35)], 2.0 if ri else 1.4, None))
            poles = strokes(W, H, pole_items)
            art = GP(art, poles, "#5a4532", "#3f3022", seed=nx(), rough=0.5, pad=6)
            # reflections: wavy, broken pole strokes under the surface
            refl = []
            for (pts, wd, _) in pole_items:
                px = pts[0][0]
                for j in range(4):
                    y0 = WL + depth * 0.35 + j * 9
                    refl.append(([(px + 2 * math.sin(j * 1.7), y0), (px - 2 * math.sin(j * 1.7 + 1), y0 + 6)], wd * 0.9, None))
            art = G(art, strokes(W, H, refl), "#2c6f6e", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1, feather=0.6)
            # deck / floor beam
            art = GP(art, strokes(W, H, [([(x - 6, floor + 1), (x + w + 6, floor + 1)], 4 if ri else 3, None)]), "#6c533b", seed=nx(), rough=0.5, pad=6)
            walls, roofm, openings, planks = house(W, H, x, floor, w, wall, roof, rng, kind)
            c = rng.choice(wall_cols)
            art = GP(art, walls, *c, seed=nx(), rough=1.0, streak=1.0)
            art = G(art, planks, "#9b8058", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.4)
            # shade the right half of each wall (sun from the left)
            art = G(art, walls * np.clip((xx - (x + w * 0.55)) / (w * 0.45), 0, 1), "#a08a6a", seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=1.5)
            art = GP(art, openings, "#3b3a33", "#2c2c27", seed=nx(), rough=0.6, pad=6)
            rc = rng.choice(roof_cols)
            art = GP(art, roofm, *rc, seed=nx(), rough=1.2, streak=1.4)
            # thatch / zinc lines on the roof
            rl = [([(x + w * t, floor - wall - roof * (1 - abs(t - 0.5) * 2) * 0.9 if kind == 0 else floor - wall - roof * 0.95), (x + w * t + (t - 0.5) * 8, floor - wall + 1)], 0.9, None) for t in np.linspace(0.08, 0.92, 9)]
            art = G(art, strokes(W, H, rl) * roofm, "#3e2e20", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.4)
            art = G(art, roofm * np.clip((x + w / 2 - xx) / (w * 0.5), 0, 1), "#f4e3bf", seed=nx(), density=0.3, edge=0, bloom=0.2, rough=1, feather=1.5)
            # house reflection: a soft smear of the wall colour
            art = G(art, shapes(W, H, [[(x, WL + depth * 0.35), (x + w, WL + depth * 0.35), (x + w * 0.96, WL + depth * 0.35 + wall * 0.8), (x + w * 0.04, WL + depth * 0.35 + wall * 0.8)]], smooth=False) * (0.5 + 0.5 * np.sin(yy / 2.6)), c[1], seed=nx(), density=0.22, edge=0, bloom=0.3, rough=3, feather=1.5)
            clear()
    # boardwalk: long plank bridge in the front row
    bw = strokes(W, H, [([(0, WL + 6), (W, WL + 2)], 5, None)])
    art = GP(art, bw, "#7a5e42", "#5c4632", seed=nx(), rough=0.6)
    bposts = strokes(W, H, [([(px, WL + 4), (px, WL + 26)], 2, None) for px in range(10, W, 34)])
    art = GP(art, bposts, "#4c3a28", seed=nx(), rough=0.5)
    # surface sparkle ripples
    rip = []
    for k in range(120):
        y = rng.uniform(WL + 12, H - 6); x0 = rng.uniform(-20, W)
        L = rng.uniform(14, 46) * (0.5 + (y - WL) / (H - WL))
        rip.append(([(x0, y), (x0 + L, y + rng.uniform(-1, 1))], rng.uniform(1.2, 2.6), (0.4, 0.4)))
    rm = strokes(W, H, rip)
    art = G(art, rm, "#e9fbf6", seed=nx(), density=0.65, edge=0.1, bloom=0, rough=1, feather=0.5)
    rip2 = [([(q[0][0][0] + 9, q[0][0][1] + 5), (q[0][1][0] + 9, q[0][1][1] + 5)], 1.6, (0.4, 0.4)) for q in rip[::2]]
    art = G(art, strokes(W, H, rip2), "#2c8f8e", seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=0.5)
    # keep the bottom rows exactly the CSS sea colour so the art melts into the cover
    k = np.clip((yy - (H - 60)) / 60, 0, 1)[..., None]
    art[..., :3] = art[..., :3] * (1 - k) + np.array(hex_rgb(SEA_BOTTOM), np.float32) * k
    art = add_grain(art, seed=3, amount=0.025)
    preview(art, "bj-village", bg=SKY)
    save_full(art, f"{OUT}/village.webp", size=(780, 560), quality=78)
    clear()

if "lepa" in PARTS:
    W, H = 360, 300
    nx = Seq(61200); rng = random.Random(9)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    deck = 236
    # hull: long, low, with raised curved bow and stern
    top = curve([(28, deck - 34), (60, deck - 6), (180, deck + 2), (300, deck - 6), (338, deck - 40)], 60)
    bot = curve([(338, deck - 40), (318, deck + 10), (180, deck + 22), (50, deck + 10), (28, deck - 34)], 60)
    hull = shapes(W, H, [top + bot], smooth=False)
    # mast and sail (rectangular, slightly bellied, striped)
    mast = strokes(W, H, [([(176, deck), (172, 36)], 3.5, None)])
    sail = shapes(W, H, [curve([(176, 44), (236, 46), (292, 62)], 16) + curve([(292, 62), (300, 130), (284, 196)], 16) + [(178, 192)]], smooth=False)
    art = G(art, shapes(W, H, [[(60, deck + 24), (300, deck + 24), (290, deck + 40), (70, deck + 40)]], smooth=False), "#2a8f8d", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=4, feather=3)
    art = GP(art, mast, "#5a4128", seed=nx(), rough=0.5)
    art = GP(art, strokes(W, H, [([(172, 40), (298, 60)], 2.4, None), ([(176, 194), (286, 198)], 2.4, None)]), "#5a4128", seed=nx(), rough=0.5)
    stripes = ["#e8d7b4", "#d9543a", "#e8d7b4", "#e7b844", "#e8d7b4", "#2f8fa0", "#e8d7b4"]
    for i, c in enumerate(stripes):
        t0, t1 = i / len(stripes), (i + 1) / len(stripes)
        band = sail * ((yy >= 44 + t0 * 156) & (yy < 44 + t1 * 156 + 1)).astype(np.float32)
        art = GP(art, band, c, seed=nx(), rough=0.8, streak=1.0)
    art = G(art, sail * np.clip((xx - 230) / 70, 0, 1), "#6a5a48", seed=nx(), density=0.3, edge=0, bloom=0.3, rough=2, feather=3)
    art = G(art, sail, "#ffffff", seed=nx(), density=0.0, edge=0.5, bloom=0, rough=1)
    # cabin (kajang mat roof)
    cabin = shapes(W, H, [curve([(84, deck - 4), (112, deck - 36), (148, deck - 4)], 20)], smooth=False)
    art = GP(art, cabin, "#c9a56a", "#a9844c", seed=nx(), rough=1.0, streak=1.2)
    art = G(art, strokes(W, H, [([(90 + i * 8, deck - 6), (104 + i * 4, deck - 30)], 0.9, None) for i in range(7)]) * cabin, "#6e5232", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = GP(art, hull, "#8b5d3a", "#6b4429", seed=nx(), rough=1.0, streak=1.0)
    # painted bands on the hull
    band = strokes(W, H, [(curve([(40, deck - 20), (180, deck + 6), (326, deck - 24)], 40), 4, None)]) * hull
    art = GP(art, band, "#f2ead8", seed=nx(), rough=0.5)
    band2 = strokes(W, H, [(curve([(48, deck - 12), (180, deck + 12), (318, deck - 14)], 40), 2.5, None)]) * hull
    art = GP(art, band2, "#2f8fa0", seed=nx(), rough=0.5)
    art = G(art, hull * np.clip((yy - deck) / 20, 0, 1), "#3a2416", seed=nx(), density=0.45, edge=0, bloom=0, rough=1, feather=1.5)
    # outrigger float + booms
    art = GP(art, strokes(W, H, [([(120, deck + 2), (110, deck + 30)], 2.5, None), ([(240, deck + 2), (250, deck + 30)], 2.5, None)]), "#5a4128", seed=nx(), rough=0.4)
    art = GP(art, strokes(W, H, [([(70, deck + 32), (300, deck + 30)], 5, (0.1, 0.1))]), "#7a5236", seed=nx(), rough=0.5)
    # waterline foam
    foam = strokes(W, H, [([(30 + i * 22, deck + 40 + rng.uniform(-2, 2)), (44 + i * 22, deck + 40)], 2, (0.4, 0.4)) for i in range(14)])
    art = G(art, foam, "#ffffff", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=1)
    art = add_grain(art, seed=4, amount=0.03)
    preview(art, "bj-lepa", bg="#7fd0c8")
    save(art, f"{OUT}/lepa.webp", max_w=220, quality=84)
    clear()

if "reef" in PARTS:
    W, H = 780, 230
    nx = Seq(61300); rng = random.Random(13)
    art = blank(W, H)
    # sandy bed
    bed = shapes(W, H, [[(-20, H - 40)] + [(x, H - 44 + 8 * math.sin(x / 70)) for x in range(-20, W + 21, 20)] + [(W + 20, H + 10), (-20, H + 10)]], smooth=False)
    art = GP(art, bed, "#f0e2bf", "#e2cf9f", seed=nx(), rough=2, streak=0.8)
    # seagrass blades
    blades = []
    for x in range(0, W, 9):
        if rng.random() < 0.35:
            continue
        L = rng.uniform(60, 150); lean = rng.uniform(-0.35, 0.35)
        blades.append((curve([(x, H - 36), (x + lean * L * 0.4, H - 36 - L * 0.5), (x + lean * L, H - 36 - L)], 18), rng.uniform(3, 5.5), (0.0, 0.6)))
    art = G(art, strokes(W, H, blades), "#3f9a6e", "#6cba7e", seed=nx(), density=0.85, edge=0.55, bloom=0.2, rough=1.5)
    # branching corals (gouache): coral pink, ochre, lilac
    def branch(x, y, ang, L, d, out):
        if d == 0 or L < 6:
            return
        x2, y2 = x + math.cos(ang) * L, y + math.sin(ang) * L
        out.append(([(x, y), ((x + x2) / 2 + rng.uniform(-3, 3), (y + y2) / 2), (x2, y2)], max(2.6, d * 2.0), None))
        for s_ in (-1, 1):
            branch(x2, y2, ang + s_ * rng.uniform(0.3, 0.6), L * rng.uniform(0.6, 0.78), d - 1, out)
    for (x, col, col2) in [(90, "#ef8a72", "#d9604f"), (330, "#e8b45c", "#cf913f"), (520, "#b99ad0", "#9879b6"), (690, "#ef8a72", "#d9604f")]:
        items = []
        for a0 in (-math.pi / 2 - 0.55, -math.pi / 2, -math.pi / 2 + 0.5):
            branch(x + rng.uniform(-6, 6), H - 38, a0 + rng.uniform(-0.1, 0.1), rng.uniform(26, 34), 4, items)
        m = strokes(W, H, items)
        art = GP(art, m, col, col2, seed=nx(), rough=1.4, streak=0.6)
        art = G(art, m * np.clip((np.mgrid[0:H, 0:W][1] - x) / 40, 0, 1), "#6a3d4a", seed=nx(), density=0.3, edge=0, bloom=0, rough=1, feather=1.5)
    # brain / table coral mounds
    for (x, rx, col) in [(210, 46, "#d8c27e"), (430, 38, "#8fc7b5"), (600, 30, "#e7a27e")]:
        mound = shapes(W, H, [deform(ellipse_pts(x, H - 44, rx, rx * 0.55, 14), rng, 2, 0.1)])
        art = GP(art, mound, col, seed=nx(), rough=1.5)
        art = G(art, strokes(W, H, [(curve([(x - rx * 0.8, H - 44 - k * 6), (x, H - 44 - rx * 0.4 - k * 4), (x + rx * 0.8, H - 44 - k * 6)], 20), 1.4, None) for k in range(4)]) * mound, "#5a4a3a", seed=nx(), density=0.35, edge=0, bloom=0, rough=1, feather=0.5)
    # pebbles / shells dots
    art = GP(art, circles(W, H, [(rng.uniform(0, W), H - rng.uniform(8, 30), rng.uniform(2, 4)) for _ in range(40)]), "#fbf4e2", "#d8c49a", seed=nx(), rough=0.6)
    art = add_grain(art, seed=5, amount=0.03)
    preview(art, "bj-reef", bg="#7fd0c8")
    save(art, f"{OUT}/reef.webp", max_w=780, quality=80)
    clear()

if "net" in PARTS:
    W = H = 160
    nx = Seq(61400)
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6)
    step = 40
    for k in range(-6, 6):
        cv.c.drawLine(k * step, 0, k * step + H, H, p)
        cv.c.drawLine(k * step, H, k * step + H, 0, p)
    m = cv.array()[..., 3]
    kn = circles(W, H, [(i * step / 2, j * step / 2, 2.4) for i in range(0, 9) for j in range(0, 9) if (i + j) % 2 == 0])
    m = np.clip(m + kn, 0, 1)
    art = rgba("#1f6f74", m * 0.9)
    art[..., 3] *= 0.75 + 0.25 * wrap_noise(W, H, 3, 4)
    save_full(art, f"{OUT}/net.webp", quality=80)

if "divider" in PARTS:
    W, H = 420, 60
    nx = Seq(61500); rng = random.Random(17)
    art = blank(W, H)
    rope = curve([(6, 26), (110, 34), (210, 28), (310, 34), (414, 26)], 80)
    art = GP(art, strokes(W, H, [(rope, 4.2, (0.05, 0.05))]), "#b99566", "#8f6d45", seed=nx(), rough=0.5)
    twist = []
    for i in range(0, len(rope) - 1):
        x, y = rope[i]
        if i % 2 == 0:
            twist.append(([(x - 2, y - 2), (x + 2, y + 2)], 1.0, None))
    art = G(art, strokes(W, H, twist), "#5a4128", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.3)
    # three floats
    for (x, col) in [(120, "#e8673f"), (210, "#f4efe2"), (300, "#e8673f")]:
        y = 31
        fm = shapes(W, H, [ellipse_pts(x, y, 15, 11, 18)])
        art = GP(art, fm, col, seed=nx(), rough=0.8)
        art = G(art, fm * np.clip((np.mgrid[0:H, 0:W][0] - y) / 10, 0, 1), "#7a3a2a" if col != "#f4efe2" else "#9aa3a0", seed=nx(), density=0.4, edge=0, bloom=0, rough=1, feather=1.5)
        art = G(art, circles(W, H, [(x - 5, y - 4, 3)]), "#ffffff", seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
    preview(art, "bj-divider")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)

if "sprig" in PARTS:
    W, H = 160, 170
    nx = Seq(61600); rng = random.Random(19)
    art = blank(W, H)
    items = []

    def br(x, y, ang, L, d):
        if d == 0:
            return
        x2, y2 = x + math.cos(ang) * L, y + math.sin(ang) * L
        items.append(([(x, y), (x2, y2)], max(3, d * 3.2), None))
        for s_ in (-1, 1):
            br(x2, y2, ang + s_ * rng.uniform(0.35, 0.6), L * 0.72, d - 1)
    br(80, 160, -math.pi / 2, 40, 5)
    m = strokes(W, H, items)
    art = GP(art, m, "#ef8a72", "#d9604f", seed=nx(), rough=1.0)
    art = G(art, m * np.clip((np.mgrid[0:H, 0:W][1] - 80) / 40, 0, 1), "#6a3d4a", seed=nx(), density=0.3, edge=0, bloom=0, rough=1, feather=1.5)
    preview(art, "bj-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=80, quality=84)

kb(OUT)
