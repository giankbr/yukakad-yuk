"""Sape Dayak — the carved sape lute (boat-shaped body painted with curling kelawit-style motifs) beside a misty
river forest with a betang/lamin longhouse. Gouache for the sape and motifs, watercolour mist for the scene.
Run: python3 -I sape-dayak.py [scene sape divider curl]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q5_lib import *

OUT = outdir("sape-dayak")
PARTS = sys.argv[1:] or ["scene", "sape", "divider", "curl"]
INK, RED, YEL, CREAM, WOOD, WOOD_D = "#1b1511", "#b0341f", "#d8a43a", "#f1e6cf", "#8c4a25", "#4a2412"


def hooks(path, side, size, every=3, start=2):
    """Little thorn hooks (kelawit tips) sticking out of a curve: list of polygons."""
    out = []
    for i in range(start, len(path) - 2, every):
        (x0, y0), (x1, y1) = path[i - 1], path[i + 1]
        a = math.atan2(y1 - y0, x1 - x0)
        nx_, ny_ = -math.sin(a) * side, math.cos(a) * side
        bx, by = path[i]
        tip = (bx + nx_ * size - math.cos(a) * size * 0.9, by + ny_ * size - math.sin(a) * size * 0.9)
        out.append([(bx - math.cos(a) * size * .35, by - math.sin(a) * size * .35), tip, (bx + math.cos(a) * size * .35, by + math.sin(a) * size * .35)])
    return out


def scurl(x, y, s, flip=1, ang=0.0):
    """An S-curve sweeping out from (x, y) ending in a tight spiral: returns (path, spiral centre, r)."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        u *= flip
        return (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    path = curve([P(0, 0), P(0.35, -0.25), P(0.75, -0.15), P(0.95, 0.2), P(0.8, 0.5)], 30)
    cx, cy = P(0.62, 0.32)
    sp = jw.spiral_pts(cx, cy, s * 0.24, s * 0.04, math.atan2(path[-1][1] - cy, path[-1][0] - cx), 1.15, 34, 1 if flip > 0 else -1)
    return path + sp[1:], (cx, cy), s * 0.24


if "scene" in PARTS:
    W, H = 780, 1560
    nx = Seq(31000); rng = random.Random(31)
    sky = painted_sky(W, H, [(0, "#eef0e8"), (0.32, "#e3e8e0"), (0.5, "#cdd8d0"), (0.66, "#b9c9c2"), (1, "#a9bcb8")], seed=3, streak=0.25, grain=0.3)
    art = sky
    # pale sun disc behind mist
    art = G(art, circles(W, H, [(560, 300, 70)]), "#f7f2df", seed=nx(), density=0.6, edge=0.1, bloom=0.2, rough=3, feather=6)
    layers = [(560, 60, "#c2cec8", "#b4c3bd", 0.55), (640, 70, "#9fb3ad", "#8aa19b", 0.6), (730, 80, "#7b948d", "#6a837d", 0.7), (820, 60, "#566f66", "#4b6259", 0.8)]
    for li, (y, amp, ca, cb, d) in enumerate(layers):
        m = jw.hills(W, H, y, amp, 40 + li, wl=0.7 - li * 0.08)
        # emergent trees on the ridge
        trees = []
        for k in range(14 + li * 6):
            tx = rng.uniform(-20, W + 20)
            col = m[:, int(np.clip(tx, 0, W - 1))]
            ty = int(np.argmax(col > 0.5)) if col.max() > 0.5 else y
            th = rng.uniform(40, 90) * (1 + li * 0.35)
            trees.append((tx, ty, th))
        cv = Canvas(W, H)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for tx, ty, th in trees:
            pp = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=max(1.5, th * 0.04), Style=skia.Paint.kStroke_Style)
            cv.c.drawLine(tx, ty + 6, tx + rng.uniform(-3, 3), ty - th, pp)
            for j in range(rng.randint(3, 5)):
                cv.c.drawOval(skia.Rect.MakeXYWH(tx - th * rng.uniform(.25, .45) + rng.uniform(-8, 8), ty - th - th * .12 + rng.uniform(-6, 10), th * rng.uniform(.4, .7), th * rng.uniform(.14, .22)), p)
        tm = cv.array()[..., 3]
        m = np.maximum(m, tm)
        art = G(art, m, ca, cb, seed=nx(), density=d, edge=0.35, bloom=0.4, rough=5, holes=0.03)
        # mist band in front of each ridge
        mist = np.clip((jw.hills(W, H, y + 70, amp * 0.5, 80 + li) - jw.hills(W, H, y + 160, amp * 0.4, 90 + li)), 0, 1)
        art = over(art, tint(gaussian_filter(mist, 22), "#eef1ea", 0.55))
        clear()
    # longhouse (betang/lamin) on stilts, left-centre on the far bank
    hx0, hx1, hy = 70, 430, 905
    roof = shapes(W, H, [[(hx0 - 18, hy - 32), (hx0 + 30, hy - 74), (hx1 - 30, hy - 74), (hx1 + 18, hy - 32)]], smooth=False)
    wall = shapes(W, H, [rect(hx0, hy - 34, hx1, hy)], smooth=False)
    stilts = strokes(W, H, [([(x, hy), (x + rng.uniform(-1, 1), hy + 46)], 4.5, None) for x in range(hx0 + 8, hx1, 22)])
    ladder = strokes(W, H, [([(hx0 + 160, hy), (hx0 + 150, hy + 48)], 4, None), ([(hx0 + 176, hy), (hx0 + 168, hy + 48)], 4, None)] + [([(hx0 + 152, hy + k), (hx0 + 172, hy + k)], 2.5, None) for k in (12, 24, 36)])
    art = G(art, np.maximum(stilts, ladder), "#3d3a30", seed=nx(), density=0.7, edge=0.4, bloom=0, rough=1.2, feather=0.8)
    art = GP(art, wall, "#8a6a48", "#6e5236", seed=nx(), rough=1.0, streak=1.0, density=0.85)
    planks = strokes(W, H, [([(x, hy - 32), (x, hy - 2)], 1.4, None) for x in range(hx0 + 6, hx1, 9)]) * wall
    art = G(art, planks, "#4d3a26", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.5)
    doors = shapes(W, H, [rect(x, hy - 26, x + 12, hy - 4) for x in range(hx0 + 30, hx1 - 20, 64)], smooth=False)
    art = G(art, doors, "#2a2018", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    art = GP(art, roof, "#5d4b3a", "#3f3227", seed=nx(), rough=1.2, streak=1.6, density=0.9)
    # carved ridge finials (curls at both roof ends)
    fin = strokes(W, H, [(jw.spiral_pts(hx0 + 22, hy - 86, 12, 2, 0, 1.0, 26, -1), 3.4, (0.0, 0.5)), (jw.spiral_pts(hx1 - 22, hy - 86, 12, 2, math.pi, 1.0, 26, 1), 3.4, (0.0, 0.5))])
    art = G(art, fin, "#3a2c20", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    art = over(art, tint(gaussian_filter(np.clip(jw.hills(W, H, hy + 30, 10, 7) - jw.hills(W, H, hy + 120, 8, 8), 0, 1), 16), "#e8ece5", 0.45))
    clear()
    # near bank: dense dark forest + palms/pandan
    bank = jw.hills(W, H, 1000, 26, 55, wl=0.35)
    cv = Canvas(W, H); p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    for k in range(40):
        x = rng.uniform(-20, W + 20); r = rng.uniform(18, 46)
        cv.c.drawCircle(x, 1000 - rng.uniform(0, 40), r, p)
    bank = np.maximum(bank, cv.array()[..., 3]) * (1 - shapes(W, H, [rect(0, 1092, W, H)], smooth=False))
    art = G(art, bank, "#3e5a4b", "#2c4237", seed=nx(), density=0.9, edge=0.5, bloom=0.35, rough=6)
    art = G(art, bank * fbm(W, H, 7, 30, 3), "#22342b", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=3)
    clear()
    # river
    river = shapes(W, H, [rect(-10, 1080, W + 10, H + 10)], smooth=False)
    water = painted_sky(W, H, [(0, "#a9bcb8"), (0.69, "#a9bcb8"), (0.75, "#c3d0cb"), (1, "#8fa6a3")], seed=9, streak=1.6)
    water[..., 3] = river
    art = over(art, water)
    art = over(art, tint(gaussian_filter(shapes(W, H, [rect(0, 1070, W, 1110)], smooth=False), 10), "#dfe6e0", 0.5))
    # reflection of the bank, broken by ripples
    refl = np.flipud(bank)
    refl = np.roll(refl, (1092 * 2) - H, 0)
    ripple = hatch(W, H, 0.0, 7, 0.5, 4, wob=2.0)
    art = G(art, refl * river * (0.5 + 0.5 * ripple), "#5c766a", seed=nx(), density=0.45, edge=0.1, bloom=0.2, rough=4)
    lines = strokes(W, H, [([(x, y), (x + rng.uniform(30, 120), y + rng.uniform(-1, 1))], rng.uniform(1.2, 2.6), (0.3, 0.3)) for x, y in [(rng.uniform(-40, W), rng.uniform(1110, H)) for _ in range(90)]])
    art = over(art, tint(lines * river, "#e9efe9", 0.55))
    # little longboat (perahu) drifting
    bx, by = 520, 1210
    boat = shapes(W, H, [[(bx - 90, by - 10), (bx - 60, by + 6), (bx + 60, by + 6), (bx + 96, by - 14), (bx + 60, by - 2), (bx - 60, by - 2)]])
    art = GP(art, boat, "#3a2a1e", "#22180f", seed=nx(), rough=1.0, density=0.92)
    art = over(art, tint(gaussian_filter(np.roll(boat, 14, 0), 4) * river, "#4b5f58", 0.35))
    pole = strokes(W, H, [([(bx + 10, by - 2), (bx + 70, by - 90)], 3, None)])
    art = G(art, pole, "#2a2018", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    clear()
    # foreground ferns (pakis) framing the bottom corners
    def fern(x, y, L, a, flip):
        spine = [(x + math.cos(a + flip * 0.5 * t * t) * L * t, y + math.sin(a + flip * 0.5 * t * t) * L * t) for t in [j / 30 for j in range(31)]]
        items = [(spine, L * 0.022, (0.0, 0.6))]
        for j in range(2, 28, 2):
            px, py = spine[j]; t = j / 30
            for sd in (-1, 1):
                aa = a + flip * 0.5 * t * t + sd * 1.0
                ll = L * 0.2 * (1 - t * 0.75)
                LEAVES.append(petal_pts(px, py, ll, ll * 0.32, aa + 0.25 * sd * flip, n=10))
        return items
    LEAVES = []
    fm = strokes(W, H, fern(-10, H + 10, 420, -1.2, 1) + fern(30, H + 20, 330, -0.75, 1) + fern(W + 10, H + 10, 380, -1.95, -1) + fern(W - 40, H + 30, 280, -2.4, -1))
    fm = np.maximum(fm, shapes(W, H, LEAVES))
    art = G(art, fm, "#2b4436", "#1a2b22", seed=nx(), density=0.92, edge=0.5, bloom=0.2, rough=2.2, feather=0.9)
    art = add_grain(art, 3, 0.03)
    preview(art, "sd-scene", bg="#000000")
    save_rgb(art, f"{OUT}/scene.webp", size=(560, 1120), quality=74)
    clear()

if "sape" in PARTS:
    W, H = 320, 1320
    nx = Seq(32000); rng = random.Random(32)
    cx = W / 2
    # right half outline (top -> bottom); mirrored
    R = [(cx, 140), (cx + 22, 150), (cx + 22, 300), (cx + 25, 480), (cx + 28, 610), (cx + 60, 660), (cx + 104, 700), (cx + 122, 780), (cx + 126, 900), (cx + 120, 1020), (cx + 100, 1130), (cx + 66, 1215), (cx + 24, 1268), (cx, 1282)]
    body_pts = R + [(2 * cx - x, y) for x, y in reversed(R[1:-1])]
    body = shape_mask(W, H, body_pts)
    face = shape_mask(W, H, [(cx + (x - cx) * 0.9, y) for x, y in body_pts if y >= 600])
    neck = body * (1 - face)
    side = np.clip(np.roll(body, 9, 1) - body, 0, 1)
    art = blank(W, H)
    art = over(art, tint(gaussian_filter(np.roll(np.roll(body, 14, 1), 16, 0), 10), "#000000", 0.35))
    art = GP(art, np.maximum(body, side), WOOD_D, "#2c150a", seed=nx(), rough=1.2, streak=1.2)
    art = GP(art, inset(body, 5), WOOD, "#a35a2c", seed=nx(), rough=1.2, streak=1.6)
    art = GP(art, inset(face, 4), CREAM, "#e3d3b2", seed=nx(), rough=1.4, streak=1.4)
    # motif system on the face (left half, mirrored): spine + S-curls + thorn hooks
    items, fills, thorns = [], [], []
    spine = curve([(cx, 660), (cx, 1240)], 20)
    items.append((spine, 7, None))
    for (y, s, ang) in [(705, 84, 0.35), (835, 108, 0.12), (980, 112, 0.0), (1110, 88, -0.2)]:
        path, (sx, sy), r = scurl(cx, y, s, flip=-1, ang=ang)
        items.append((path, 7.5, (0.0, 0.25)))
        thorns += hooks(path[:28], 1, 11, every=5, start=4)
        fills.append((sx, sy, r * 0.6))
    for (y, s) in [(760, 40), (890, 46), (1035, 46), (1180, 40)]:
        p2 = curve([(cx - 12, y), (cx - s * 0.6, y - s * 0.3), (cx - s, y - s * 0.05)], 16)
        items.append((p2, 4.5, (0.0, 0.4)))
        thorns += hooks(p2, -1, 8, every=6, start=4)
    curls = strokes(W, H, items)
    curls = np.maximum(curls, shapes(W, H, thorns, smooth=False))
    curls = mirror_x(curls)
    redm = mirror_x(circles(W, H, fills))
    redm = np.clip(redm - gaussian_filter(curls, 1.5) * 2, 0, 1)
    dots = mirror_x(circles(W, H, [(cx - rng.uniform(20, 110), rng.uniform(690, 1220), rng.uniform(2.5, 4.5)) for _ in range(40)]))
    dots = np.clip(dots - gaussian_filter(np.maximum(curls, redm), 3) * 3, 0, 1)
    fm = inset(face, 12)
    # red ground zones between curls (lower body)
    teeth = [[(x, 1196), (x + 9, 1172), (x + 18, 1196)] for x in range(int(cx - 120), int(cx + 120), 18)]
    zone = np.maximum(shapes(W, H, [rect(cx - 130, 1196, cx + 130, 1290)], smooth=False), shapes(W, H, teeth, smooth=False)) * fm
    zone = np.maximum(zone, mirror_x(shapes(W, H, [[(cx, 672), (cx - 90, 720), (cx - 110, 700), (cx - 60, 650)]])) * fm)
    art = GP(art, zone, RED, "#8d2716", seed=nx(), rough=1.0, streak=1.0)
    art = GP(art, redm * fm, RED, "#8d2716", seed=nx(), rough=1.0, streak=1.0)
    art = GP(art, curls * fm, INK, "#2c201a", seed=nx(), rough=0.7, streak=0.8, density=0.97)
    art = GP(art, dots * fm, YEL, seed=nx(), rough=0.5, density=0.95)
    # painted border line just inside the face edge
    bl = np.clip(inset(face, 8) - inset(face, 14), 0, 1)
    art = GP(art, bl, INK, seed=nx(), rough=0.6, density=0.95)
    # neck: frets (raised blocks)
    frets = shapes(W, H, [rect(cx - 26, y, cx + 26, y + 9) for y in range(190, 600, 52)], smooth=False) * np.roll(body, 0, 1)
    art = GP(art, np.roll(frets, 3, 0), WOOD_D, seed=nx(), rough=0.4, density=0.8)
    art = GP(art, frets, "#c99a5a", "#a87a40", seed=nx(), rough=0.5, streak=1.2)
    neckmot = mirror_x(strokes(W, H, [(jw.spiral_pts(cx - 14, 640, 12, 2, 0, 1.0, 22, 1), 3.2, (0, .5))]))
    art = GP(art, neckmot, INK, seed=nx(), rough=0.4)
    # head: carved curl scroll + pegs
    head_pts = [(cx - 20, 150), (cx - 34, 110), (cx - 30, 64), (cx - 6, 36), (cx + 26, 34), (cx + 46, 58), (cx + 44, 92), (cx + 22, 108), (cx + 6, 96), (cx + 10, 76), (cx + 22, 82), (cx + 22, 150)]
    head = shape_mask(W, H, deform(head_pts, rng, 1, 0.02))
    art = GP(art, head, WOOD, WOOD_D, seed=nx(), rough=1.0, streak=1.2)
    hs = strokes(W, H, [(jw.spiral_pts(cx + 10, 70, 30, 3, math.pi * 0.9, 1.1, 40, 1), 5, (0.0, 0.5))]) * head
    art = GP(art, hs, INK, seed=nx(), rough=0.5)
    art = GP(art, circles(W, H, [(cx - 12, 116, 6)]), RED, seed=nx(), rough=0.4)
    pegs = strokes(W, H, [([(cx - 18, 200), (cx - 58, 196)], 9, (0.0, 0.3)), ([(cx + 18, 250), (cx + 58, 246)], 9, (0.0, 0.3))])
    art = GP(art, pegs, "#5b3018", "#3a1c0d", seed=nx(), rough=0.6, streak=1.0)
    # bridge + strings
    bridge = shapes(W, H, [rect(cx - 30, 1168, cx + 30, 1180)], smooth=False)
    art = GP(art, bridge, "#2b1b12", seed=nx(), rough=0.4)
    st = strokes(W, H, [([(cx - 8, 200), (cx - 9, 1174)], 1.6, None), ([(cx + 8, 250), (cx + 9, 1174)], 1.6, None)])
    art = over(art, tint(st, "#efe9d8", 0.85))
    art = over(art, tint(np.roll(st, 2, 1) * 0.6, "#2c2018", 0.35))
    # warm light from the upper left
    sh = np.clip(np.roll(gaussian_filter(body, 14), -12, 1) - gaussian_filter(body, 14), 0, 1) * body * 3
    art = G(art, np.clip(sh, 0, 1), "#3a1f10", seed=nx(), density=0.3, edge=0, bloom=0.2, rough=1)
    preview(art, "sd-sape", bg="#c9d4cd")
    save(art, f"{OUT}/sape.webp", max_w=240, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 640, 96
    nx = Seq(33000); rng = random.Random(33)
    cx, cy = W / 2, H / 2
    items, thorns, fills = [], [], []
    items.append((curve([(cx - 300, cy), (cx - 60, cy)], 20), 3.0, (0.3, 0.0)))
    for (x, s, ang) in [(cx - 44, 46, 0.0), (cx - 150, 34, 0.15)]:
        path, (sx, sy), r = scurl(x, cy + 2, s, flip=-1, ang=ang)
        items.append((path, 5.5, (0.0, 0.25)))
        thorns += hooks(path[:28], 1, 7, every=6, start=4)
        fills.append((sx, sy, r * 0.55))
    dia = [(cx, cy - 22), (cx + 14, cy), (cx, cy + 22), (cx - 14, cy)]
    m = mirror_x(np.maximum(strokes(W, H, items), shapes(W, H, thorns, smooth=False)))
    red = np.clip(mirror_x(circles(W, H, fills)) - gaussian_filter(m, 1.2) * 2, 0, 1)
    art = blank(W, H)
    art = GP(art, red, RED, "#8d2716", seed=nx(), rough=0.8)
    art = GP(art, m, INK, "#2c201a", seed=nx(), rough=0.6, density=0.97)
    art = GP(art, shapes(W, H, [dia], smooth=False), RED, seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, [(cx, cy, 5)]), YEL, seed=nx(), rough=0.4)
    preview(art, "sd-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=440, quality=84)
    clear()

if "curl" in PARTS:
    W, H = 260, 260
    nx = Seq(34000)
    cx, cy = W / 2, H / 2
    items, thorns, fills = [], [], []
    for k in range(4):
        a = k * math.pi / 2
        path, (sx, sy), r = scurl(cx + math.cos(a) * 14, cy + math.sin(a) * 14, 70, flip=1, ang=a)
        items.append((path, 7, (0.0, 0.25)))
        thorns += hooks(path[:28], -1, 9, every=6, start=4)
        fills.append((sx, sy, r * 0.55))
    m = np.maximum(strokes(W, H, items), shapes(W, H, thorns, smooth=False))
    red = np.clip(circles(W, H, fills) - gaussian_filter(m, 1.2) * 2, 0, 1)
    art = blank(W, H)
    art = GP(art, red, RED, "#8d2716", seed=nx(), rough=0.8)
    art = GP(art, m, INK, "#2c201a", seed=nx(), rough=0.6, density=0.97)
    art = GP(art, circles(W, H, [(cx, cy, 13)]), RED, seed=nx(), rough=0.5)
    art = GP(art, circles(W, H, [(cx, cy, 6)]), YEL, seed=nx(), rough=0.4)
    preview(art, "sd-curl", bg=CREAM)
    save(art, f"{OUT}/curl.webp", max_w=180, quality=84)
    clear()

kb(OUT)
