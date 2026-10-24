"""Malam Keakraban — a campus welcome night printed like a three/four-drum risograph poster: a mountain villa under a
yellow moon, pine trees, string lanterns, a bonfire ringed by stylised student silhouettes (one with a guitar).
Inks overprint (multiply) on cream paper with halftone tones, slight misregistration and drum grain.
Run: python3 -I malam-keakraban.py [part ...]  parts: scene fire lights guitar lantern divider games
Assets -> public/themes/art/malam-keakraban/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q6_lib import *

OUT = outdir("malam-keakraban")
PARTS = sys.argv[1:] or ["scene", "fire", "lights", "guitar", "lantern", "divider", "games"]
PAPER = "#f3ebd9"
BLUE, PINK, YELLOW, TEAL = "#2f4fa2", "#ff4fa8", "#ffd31a", "#0a9a8e"


def halftone(tone, cell=6.0, angle=0.4, soft=0.9):
    """Tone (0..1) -> dot coverage mask on a rotated grid (round dots that merge in the shadows)."""
    h, w = tone.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s_ = math.cos(angle), math.sin(angle)
    u = (xx * c + yy * s_) / cell
    v = (-xx * s_ + yy * c) / cell
    du = (u - np.floor(u) - 0.5)
    dv = (v - np.floor(v) - 0.5)
    d = np.sqrt(du * du + dv * dv)  # 0 at centre .. 0.707 at corner
    r = np.sqrt(np.clip(tone, 0, 1)) * 0.75
    return np.clip((r - d) * cell / soft + 0.5, 0, 1).astype(np.float32)


def drum(cov, seed, wear=0.18):
    """Riso ink take: uneven density + speckle where ink skipped."""
    h, w = cov.shape
    n = fbm(w, h, seed, 50, 3)
    sp = fbm(w, h, seed + 3, 3, 2)
    k = (0.86 + 0.14 * n) * (1 - wear * np.clip((sp - 0.6) * 4, 0, 1))
    return np.clip(cov * k, 0, 1)


def press(layers, W, H, on=True, seed=1):
    """Multiply ink layers [(cov, hex, (dx, dy))] onto paper (opaque) or onto nothing (transparent print)."""
    if on:
        base = np.asarray(paper(W, H, PAPER, seed), np.float32)[..., :3] / 255
        rgb = base.copy()
        for cov, col, (dx, dy) in layers:
            cv = np.roll(np.roll(cov, dy, 0), dx, 1)
            ink = col3(col)
            rgb = rgb * (1 - cv[..., None] * (1 - ink))
        return np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    rgb = np.ones((H, W, 3), np.float32)
    a = np.zeros((H, W), np.float32)
    for cov, col, (dx, dy) in layers:
        cv = np.roll(np.roll(cov, dy, 0), dx, 1)
        ink = col3(col)
        rgb = rgb * (1 - cv[..., None] * (1 - ink))
        a = 1 - (1 - a) * (1 - cv)
    # unpremultiply-ish: colour where ink is, alpha = total coverage
    lum = rgb
    out = np.where(a[..., None] > 1e-3, 1 - (1 - lum) / np.maximum(a[..., None], 1e-3), 1)
    return np.concatenate([np.clip(out, 0, 1), a[..., None]], -1)


def ridge(W, x0, x1, base, amp, seed, n=40):
    rng = random.Random(seed)
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = base - amp * (0.5 + 0.5 * math.sin(i * 0.45 + seed)) * (0.6 + 0.4 * math.sin(i * 0.17 + seed * 2)) + rng.uniform(-4, 4)
        pts.append((x, y))
    return pts


def pine(W, H, x, by, h, w):
    pts = [(x, by - h)]
    tiers = 4
    for k in range(tiers):
        t = (k + 1) / tiers
        pts += [(x + w * 0.5 * t, by - h + h * t * 0.92), (x + w * 0.18 * t, by - h + h * t * 0.92 - h * 0.08)]
    right = pts[1:]
    left = [(2 * x - px, py) for px, py in right[::-1]]
    poly = [pts[0]] + right + [(x + w * 0.06, by), (x - w * 0.06, by)] + left
    return poly


def student(cx, by, s, pose="sit", face=1):
    """Stylised seated student seen from behind/side: list of polygons (head, torso, arm)."""
    polys = []
    head = ellipse_pts(cx, by - s * 1.45, s * 0.24, s * 0.27, 14)
    torso = [(cx - s * 0.42, by), (cx - s * 0.36, by - s * 0.8), (cx - s * 0.18, by - s * 1.12), (cx + s * 0.18, by - s * 1.12), (cx + s * 0.36, by - s * 0.8), (cx + s * 0.42, by)]
    polys += [head, torso]
    if pose == "wave":
        polys.append([(cx + face * s * 0.2, by - s * 1.05), (cx + face * s * 0.5, by - s * 1.7), (cx + face * s * 0.62, by - s * 1.64), (cx + face * s * 0.36, by - s * 0.95)])
        polys.append(ellipse_pts(cx + face * s * 0.58, by - s * 1.74, s * 0.09, s * 0.09, 8))
    if pose == "hood":
        polys.append([(cx - s * 0.26, by - s * 1.35), (cx - s * 0.3, by - s * 1.7), (cx, by - s * 1.82), (cx + s * 0.3, by - s * 1.7), (cx + s * 0.26, by - s * 1.35)])
    if pose == "bun":
        polys.append(ellipse_pts(cx, by - s * 1.76, s * 0.12, s * 0.1, 10))
    return polys


def guitar_polys(cx, cy, s, ang):
    body = [(x, y) for x, y in ellipse_pts(0, 0, s * 0.42, s * 0.3, 16)] + []
    lower = ellipse_pts(-s * 0.3, 0, s * 0.5, s * 0.38, 18)
    neck = [(s * 0.2, -s * 0.06), (s * 1.25, -s * 0.05), (s * 1.25, s * 0.05), (s * 0.2, s * 0.06)]
    head = [(s * 1.22, -s * 0.09), (s * 1.45, -s * 0.11), (s * 1.45, s * 0.11), (s * 1.22, s * 0.09)]
    out = []
    for poly in (body, lower, neck, head):
        out.append(rotp([(cx + x, cy + y) for x, y in poly], cx, cy, ang))
    hole = rotp([(cx + x, cy + y) for x, y in ellipse_pts(-s * 0.05, 0, s * 0.1, s * 0.1, 10)], cx, cy, ang)
    return out, hole


def scene():
    W, H = 760, 800
    rng = random.Random(5)
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy(); T = B.copy()
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    xx = np.ones((H, 1), np.float32) * np.arange(W, dtype=np.float32)[None, :]
    # sky: blue halftone, deep at the top, fading toward the ridge; teal hint low
    sky = np.clip(0.95 - yy / 520, 0.15, 1)
    B = np.maximum(B, halftone(sky, 5.0, 0.26))
    T = np.maximum(T, halftone(np.clip((yy - 200) / 300, 0, 0.35), 5.5, 1.3) * (yy < 470))
    # moon (yellow, knocked out of the blue)
    moon = circles(W, H, [(590, 130, 52)])
    Y = np.maximum(Y, moon)
    B = B * (1 - dilate(moon, 2))
    P = np.maximum(P, halftone(np.clip(1 - np.hypot(xx - 590, yy - 130) / 140, 0, 1) * 0.5, 5.0, 0.8) * (1 - moon))
    # stars
    stars = circles(W, H, [(rng.uniform(10, 750), rng.uniform(10, 300), rng.uniform(1.2, 2.6)) for _ in range(45)])
    Y = np.maximum(Y, stars)
    B = B * (1 - stars)
    # far ridge: pink + blue tone (purple), near ridge: solid blue
    far = shapes(W, H, [ridge(W, -20, 780, 360, 120, 3) + [(780, 520), (-20, 520)]])
    P = np.maximum(P, halftone(far * 0.55, 5.0, 0.8))
    B = np.maximum(B, far * 0.55 + halftone(far * 0.5, 5.0, 0.26) * 0.45)
    near = shapes(W, H, [ridge(W, -20, 780, 430, 70, 9) + [(780, 560), (-20, 560)]])
    B = np.maximum(B, near)
    Y = Y * (1 - far)
    # ground: teal halftone with yellow glow toward the fire
    ground = shapes(W, H, [[(-20, 470), (200, 458), (420, 466), (780, 452), (780, 820), (-20, 820)]])
    glowt = np.clip(1 - np.hypot((xx - 330) / 1.3, yy - 600) / 300, 0, 1)
    B = B * (1 - ground)
    dark = np.clip(1 - glowt * 1.6, 0, 1)
    T = np.maximum(T, ground * halftone(0.25 + 0.5 * dark, 5.5, 1.3))
    B = np.maximum(B, ground * halftone(0.15 + 0.7 * dark * np.clip((yy - 440) / 360 + 0.4, 0, 1), 5.0, 0.26))
    Y = np.maximum(Y, ground * halftone(glowt ** 1.1 * 0.95, 5.0, 0.0))
    P = np.maximum(P, ground * halftone(glowt ** 1.8 * 0.55, 5.5, 0.8))
    # villa (A-frame) at right
    vx, vy = 590, 462
    roof = shapes(W, H, [[(vx - 130, vy - 40), (vx, vy - 200), (vx + 130, vy - 40), (vx + 108, vy - 40), (vx, vy - 172), (vx - 108, vy - 40)]], smooth=False)
    wall = shapes(W, H, [[(vx - 108, vy - 40), (vx, vy - 172), (vx + 108, vy - 40), (vx + 108, vy), (vx - 108, vy)]], smooth=False)
    deck = shapes(W, H, [rect(vx - 140, vy - 8, vx + 140, vy + 6)], smooth=False)
    B = B * (1 - wall); T = T * (1 - wall)
    P = np.maximum(P, wall * halftone(np.full((H, W), 0.35, np.float32), 4.0, 0.8))
    Y = np.maximum(Y, wall * halftone(np.full((H, W), 0.3, np.float32), 4.5, 0.0))
    B = np.maximum(B, edge_ring(wall, 1.5))
    planks = strokes(W, H, [([(vx - 108, vy - 40 - k * 14), (vx + 108, vy - 40 - k * 14)], 1.2, None) for k in range(-2, 9)]) * wall
    B = np.maximum(B, planks * 0.5)
    B = np.maximum(B, roof); T = np.maximum(T, roof * 0.5); B = np.maximum(B, deck)
    wins = shapes(W, H, [[(vx - 20, vy - 128), (vx, vy - 148), (vx + 20, vy - 128), (vx + 20, vy - 98), (vx - 20, vy - 98)], rect(vx - 78, vy - 76, vx - 38, vy - 34), rect(vx + 38, vy - 76, vx + 78, vy - 34), rect(vx - 16, vy - 70, vx + 16, vy - 10)], smooth=False)
    B = B * (1 - wins); P = P * (1 - wins); T = T * (1 - wins)
    Y = np.maximum(Y, wins)
    B = np.maximum(B, edge_ring(dilate(wins, 1.5), 1.5) * 0.9)
    lightspill = np.clip(1 - np.hypot(xx - vx, (yy - vy) * 2.5) / 160, 0, 1) * (yy > vy)
    Y = np.maximum(Y, halftone(lightspill * 0.7, 5.0, 0.0))
    # pines
    pines = []
    for x, h, w in [(40, 230, 110), (110, 180, 90), (180, 140, 70), (700, 150, 70), (748, 200, 90), (440, 110, 54), (16, 140, 70)]:
        pines.append(pine(W, H, x, 476 + rng.uniform(-6, 6), h, w))
    pm = shapes(W, H, pines, smooth=False)
    B = np.maximum(B, pm); T = np.maximum(T, pm * 0.8)
    Y = Y * (1 - pm); P = P * (1 - pm * 0.8)
    # string lights from the villa to the big pine
    pts = bez((vx - 120, vy - 46), (330, vy - 10), (60, 300), 50)
    wire = strokes(W, H, [(pts, 1.6, None)])
    B = np.maximum(B, wire)
    bulbs = circles(W, H, [(x, y + 7, 5.5) for x, y, _ in along(pts, 26)])
    Y = np.maximum(Y, dilate(bulbs, 1.2)); P = np.maximum(P, halftone(gaussian_filter(bulbs, 6) * 1.6, 3.5, 0.8))
    B = B * (1 - dilate(bulbs, 3))
    # bonfire logs + glow halo (flames are a separate animated asset)
    fx, fy = 330, 606
    halo = np.clip(1 - np.hypot(xx - fx, (yy - fy + 30) * 1.3) / 190, 0, 1)
    P = np.maximum(P, halftone(halo ** 1.5 * 0.85, 4.5, 0.8))
    logs = strokes(W, H, [([(fx - 60, fy + 14), (fx + 50, fy - 6)], 16, None), ([(fx - 50, fy - 6), (fx + 62, fy + 14)], 16, None), ([(fx - 30, fy + 18), (fx + 30, fy + 18)], 14, None)])
    B = np.maximum(B, logs); Y = Y * (1 - logs * 0.6)
    stones = circles(W, H, [(fx + math.cos(a) * 82, fy + 18 + math.sin(a) * 18, 9) for a in np.linspace(0, math.tau, 14, endpoint=False)])
    B = np.maximum(B, stones * 0.75); T = np.maximum(T, stones * 0.5)
    # students around the fire (back row small, front row larger, silhouettes in blue over the glow)
    back = [(fx - 150, fy - 30, 30, "sit", 1), (fx - 92, fy - 46, 28, "bun", 1), (fx + 90, fy - 46, 28, "hood", -1), (fx + 152, fy - 30, 30, "wave", -1)]
    front = [(fx - 190, fy + 120, 52, "hood", 1), (fx - 60, fy + 150, 58, "bun", 1), (fx + 80, fy + 150, 58, "sit", -1), (fx + 200, fy + 116, 52, "wave", -1)]
    sp = []
    for x, y, s, pose, face in back + front:
        sp += student(x, y, s, pose, face)
    sm = shapes(W, H, sp)
    # the guitarist (front right) holds a guitar across his lap
    gpolys, ghole = guitar_polys(fx + 80, fy + 112, 46, -0.35)
    gm = shapes(W, H, gpolys)
    B = np.maximum(B, sm)
    P = np.maximum(P, sm * 0.35)
    Y = Y * (1 - sm)
    Y = np.maximum(Y, gm); P = np.maximum(P, gm * halftone(np.full((H, W), 0.5, np.float32), 3.5, 0.8)); B = B * (1 - gm)
    B = np.maximum(B, shapes(W, H, [ghole]))
    strs = strokes(W, H, [(rotp([(fx + 80 - 20, fy + 112), (fx + 80 + 64, fy + 112)], fx + 80, fy + 112, -0.35), 1.0, None)])
    B = np.maximum(B, strs)
    # rim light on front students from the fire (yellow edge)
    rim = np.clip(sm - np.roll(np.roll(sm, 3, 0), 0, 1), 0, 1) * (np.abs(xx - fx) < 260)
    Y = np.maximum(Y, rim)
    # print
    layers = [(drum(T, 11), TEAL, (0, 0)), (drum(B, 12), BLUE, (0, 0)), (drum(P, 13), PINK, (2, -2)), (drum(Y, 14), YELLOW, (-1, 1))]
    art = press(layers, W, H, True, 4)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save("/tmp/pen/nb-Q6/art/mk-scene.png")
    save_rgb(art, f"{OUT}/scene.webp", size=(560, 589), quality=74)


def fire():
    W, H = 240, 300
    rng = random.Random(8)
    P = np.zeros((H, W), np.float32); Y = P.copy()
    cx, by = 120, 285
    outer = [(cx - 64, by), (cx - 70, by - 70), (cx - 40, by - 150), (cx - 34, by - 105), (cx - 14, by - 230), (cx + 6, by - 140), (cx + 34, by - 200), (cx + 40, by - 110), (cx + 66, by - 140), (cx + 70, by - 60), (cx + 60, by)]
    om = shapes(W, H, [deform(outer, rng, 1, 0.03)])
    inner = [(cx - 36, by), (cx - 40, by - 50), (cx - 16, by - 120), (cx - 4, by - 80), (cx + 16, by - 150), (cx + 24, by - 80), (cx + 40, by - 50), (cx + 34, by)]
    im = shapes(W, H, [deform(inner, rng, 1, 0.03)])
    P = np.maximum(P, om)
    Y = np.maximum(Y, om * halftone(np.full((H, W), 0.45, np.float32), 4.0, 0.0))
    Y = np.maximum(Y, im)
    P = P * (1 - im * 0.85)
    sparks = circles(W, H, [(cx + rng.uniform(-70, 70), by - rng.uniform(170, 290), rng.uniform(1.5, 3)) for _ in range(12)])
    Y = np.maximum(Y, sparks)
    art = press([(drum(P, 21, 0.1), PINK, (0, 0)), (drum(Y, 22, 0.1), YELLOW, (-1, 1))], W, H, False)
    save(art, f"{OUT}/fire.webp", max_w=120, quality=82)


def lights():
    """Repeat-x string of lanterns (transparent): a sagging wire with small paper lanterns."""
    W, H = 480, 110
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy()
    wire_pts = [(x, 14 + 40 * math.sin(math.pi * x / W)) for x in range(0, W + 1, 8)]
    B = np.maximum(B, strokes(W, H, [(wire_pts, 2.0, None)]))
    lan = []
    caps = []
    for i, x in enumerate((40, 120, 200, 280, 360, 440)):
        y = 14 + 40 * math.sin(math.pi * x / W) + 4
        lan.append(ellipse_pts(x, y + 18, 13, 17, 14))
        caps.append(rect(x - 7, y, x + 7, y + 4))
    lm = shapes(W, H, lan)
    cols = [(1, 0), (0, 1), (1, 1)]
    for i, poly in enumerate(lan):
        m = shapes(W, H, [poly])
        a, b = cols[i % 3]
        if a:
            P = np.maximum(P, m)
        Y = np.maximum(Y, m * (1 if b or not a else 0.0))
        if not b:
            Y = np.maximum(Y, m * halftone(np.full((H, W), 0.4, np.float32), 3.5, 0))
    ribs = strokes(W, H, [([(p[0] - 12, p[1]), (p[0] + 12, p[1])], 1.2, None) for p in [(x, 14 + 40 * math.sin(math.pi * x / W) + 4 + 18 + d) for x in (40, 120, 200, 280, 360, 440) for d in (-7, 7)]]) * lm
    B = np.maximum(B, ribs * 0.7)
    B = np.maximum(B, shapes(W, H, caps, smooth=False))
    art = press([(drum(B, 31, 0.1), BLUE, (0, 0)), (drum(P, 32, 0.1), PINK, (1, -1)), (drum(Y, 33, 0.1), YELLOW, (0, 0))], W, H, False)
    save_full(art, f"{OUT}/lights.webp", quality=82)


def guitar():
    W, H = 300, 300
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy()
    gpolys, ghole = guitar_polys(120, 170, 90, -0.75)
    gm = shapes(W, H, gpolys)
    Y = np.maximum(Y, gm)
    P = np.maximum(P, gm * halftone(np.full((H, W), 0.55, np.float32), 4.0, 0.8))
    neck = shapes(W, H, gpolys[2:])
    B = np.maximum(B, neck); Y = Y * (1 - neck)
    B = np.maximum(B, shapes(W, H, [ghole]))
    B = np.maximum(B, strokes(W, H, [(rotp([(120 - 40, 170), (120 + 125, 170)], 120, 170, -0.75), 1.2, None)]))
    B = np.maximum(B, edge_ring(gm, 1.0))
    art = press([(drum(B, 41, 0.1), BLUE, (0, 0)), (drum(P, 42, 0.1), PINK, (2, -1)), (drum(Y, 43, 0.1), YELLOW, (0, 0))], W, H, False)
    save(art, f"{OUT}/guitar.webp", max_w=110, quality=82)


def lantern():
    """Hanging camping lantern (node/emblem)."""
    W, H = 200, 260
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy()
    cx = 100
    handle = strokes(W, H, [(arc_pts(cx, 60, 40, math.pi, math.tau, 20), 5, None)])
    top = shapes(W, H, [[(cx - 50, 90), (cx, 56), (cx + 50, 90)]], smooth=False)
    glass = shapes(W, H, [rect(cx - 38, 92, cx + 38, 196)], smooth=False)
    base = shapes(W, H, [rect(cx - 52, 196, cx + 52, 214)], smooth=False)
    bars = strokes(W, H, [([(cx + d, 92), (cx + d, 196)], 4, None) for d in (-38, 0, 38)])
    B = np.maximum.reduce([B, handle, top, base, bars])
    P = np.maximum(P, top * 0.0 + base)
    Y = np.maximum(Y, glass)
    flame = shapes(W, H, [[(cx, 112), (cx + 14, 150), (cx, 172), (cx - 14, 150)]])
    P = np.maximum(P, flame)
    P = np.maximum(P, glass * halftone(np.clip(1 - np.abs(np.arange(W, dtype=np.float32)[None, :] - cx) / 40, 0, 1) * np.ones((H, 1), np.float32) * 0.5, 4, 0.8))
    art = press([(drum(B, 51, 0.1), BLUE, (0, 0)), (drum(P, 52, 0.1), PINK, (2, -1)), (drum(Y, 53, 0.1), YELLOW, (0, 0))], W, H, False)
    save(art, f"{OUT}/lantern.webp", max_w=90, quality=82)


def divider():
    """Mountain-ridge zigzag in blue with a pink misregistered echo and a yellow moon dot."""
    W, H = 720, 90
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy()
    pts = [(20, 70), (130, 70), (190, 30), (230, 55), (300, 12), (360, 52), (400, 34), (460, 70), (700, 70)]
    B = np.maximum(B, strokes(W, H, [(pts, 5, None)]))
    P = np.maximum(P, strokes(W, H, [([(x + 6, y + 6) for x, y in pts], 5, None)]))
    Y = np.maximum(Y, circles(W, H, [(560, 34, 16)]))
    P = np.maximum(P, circles(W, H, [(560, 34, 16)]) * halftone(np.full((H, W), 0.35, np.float32), 4, 0.8))
    art = press([(drum(B, 61, 0.1), BLUE, (0, 0)), (drum(P, 62, 0.1), PINK, (0, 0)), (drum(Y, 63, 0.1), YELLOW, (0, 0))], W, H, False)
    save(art, f"{OUT}/divider.webp", max_w=240, quality=82)


def games():
    """Group-game props for the hero: a tug-of-war rope knot? -> keep simple: two marshmallow sticks crossed."""
    W, H = 260, 220
    B = np.zeros((H, W), np.float32); P = B.copy(); Y = B.copy()
    st = strokes(W, H, [([(30, 200), (200, 40)], 7, None), ([(230, 200), (60, 40)], 7, None)])
    B = np.maximum(B, st)
    mm = shapes(W, H, [rotp(rect(180, 26, 222, 56), 200, 40, -0.75), rotp(rect(40, 26, 82, 56), 60, 40, 0.75)])
    P = np.maximum(P, mm * halftone(np.full((H, W), 0.35, np.float32), 4, 0.8))
    Y = np.maximum(Y, mm * 0.6)
    B = B * (1 - mm)
    art = press([(drum(B, 71, 0.1), BLUE, (0, 0)), (drum(P, 72, 0.1), PINK, (1, -1)), (drum(Y, 73, 0.1), YELLOW, (0, 0))], W, H, False)
    save(art, f"{OUT}/sticks.webp", max_w=100, quality=82)


for p in PARTS:
    globals()[p]()
    clear()
