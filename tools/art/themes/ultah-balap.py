"""Ultah Balap — kids' race-car birthday in gouache: a top-down circuit (mown grass, red-white curbs, start grid,
tyre stacks), original cartoon cars (top-down and side view, helmeted drivers, no brands), gold trophy, crossed
checkered flags, a pit board. Run: python3 -I ultah-balap.py [part ...]
parts: track cartop carside trophy flags board. Assets -> public/themes/art/ultah-balap/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l1_lib import *

OUT = outdir("ultah-balap")
PARTS = sys.argv[1:] or ["track", "cartop", "carside", "trophy", "flags", "board"]
GRASS, GRASS_L, GRASS_D = "#4caf50", "#69c36a", "#2f8a3d"
ASPH, ASPH_L = "#4a4f5c", "#5d6372"
RED, RED_D = "#e63b2e", "#a82218"
BLUE, BLUE_D = "#1f7fd6", "#145a9c"
WHITE, INK = "#fbf8f0", "#22252d"
GOLD = "#e0a82e"


def loop_pts(x0, y0, x1, y1, r, n=360):
    """Rounded-rectangle circuit centreline with a small chicane on the right straight."""
    pts = []
    per = 2 * (x1 - x0 - 2 * r) + 2 * (y1 - y0 - 2 * r) + 2 * math.pi * r
    for i in range(n):
        d = per * i / n
        segs = [("t", x1 - x0 - 2 * r), ("c", math.pi * r / 2), ("r", y1 - y0 - 2 * r), ("c", math.pi * r / 2),
                ("b", x1 - x0 - 2 * r), ("c", math.pi * r / 2), ("l", y1 - y0 - 2 * r), ("c", math.pi * r / 2)]
        k = 0
        while d > segs[k][1]:
            d -= segs[k][1]; k += 1
        t = d / segs[k][1]
        if k == 0: p = (x0 + r + t * (x1 - x0 - 2 * r), y0)
        elif k == 1: a = -math.pi / 2 + t * math.pi / 2; p = (x1 - r + math.cos(a) * r, y0 + r + math.sin(a) * r)
        elif k == 2:
            yy = y0 + r + t * (y1 - y0 - 2 * r)
            p = (x1 - 26 * math.sin(t * math.pi) ** 2 * (1 if 0.3 < t < 0.7 else 0.6), yy)
        elif k == 3: a = t * math.pi / 2; p = (x1 - r + math.cos(a) * r, y1 - r + math.sin(a) * r)
        elif k == 4: p = (x1 - r - t * (x1 - x0 - 2 * r), y1)
        elif k == 5: a = math.pi / 2 + t * math.pi / 2; p = (x0 + r + math.cos(a) * r, y1 - r + math.sin(a) * r)
        elif k == 6: p = (x0, y1 - r - t * (y1 - y0 - 2 * r))
        else: a = math.pi + t * math.pi / 2; p = (x0 + r + math.cos(a) * r, y0 + r + math.sin(a) * r)
        pts.append(p)
    return pts + [pts[0]]


def offset(pts, d):
    out = []
    for i in range(len(pts)):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        out.append((pts[i][0] - dy / L * d, pts[i][1] + dx / L * d))
    return out


def car_top(W, H, cx, cy, body, body_d, stripe, seed, num_col=WHITE):
    """Top-down cartoon racer pointing up: fat tyres, nose cone + front wing, cockpit with a helmet, rear wing."""
    nx = Seq(seed)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(cx + 8, cy + 14, 70, 150, 16), random.Random(seed), 1, 0.03)])
    art = G(art, sh, "#000000", seed=nx(), density=0.28, edge=0.05, bloom=0, rough=3, feather=8)
    tyres = rrect_mask(W, H, cx - 92, cy - 120, cx - 52, cy - 58, 12) + rrect_mask(W, H, cx + 52, cy - 120, cx + 92, cy - 58, 12) + \
        rrect_mask(W, H, cx - 100, cy + 50, cx - 52, cy + 130, 14) + rrect_mask(W, H, cx + 52, cy + 50, cx + 100, cy + 130, 14)
    tyres = np.clip(tyres, 0, 1)
    art = GP(art, tyres, INK, "#383c46", seed=nx(), rough=1.2, streak=0.8)
    tread = tyres * hatch(W, H, math.pi / 2, 9, 0.18, 3, wob=0.5)
    art = G(art, tread, "#5a5f6a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    axles = strokes(W, H, [([(cx - 60, cy - 90), (cx + 60, cy - 90)], 7, None), ([(cx - 60, cy + 92), (cx + 60, cy + 92)], 8, None)])
    art = GP(art, axles, "#6c7280", seed=nx(), rough=0.6, pad=6)
    hull = [(cx, cy - 190), (cx + 22, cy - 150), (cx + 30, cy - 60), (cx + 50, cy - 10), (cx + 52, cy + 110), (cx + 30, cy + 150), (cx - 30, cy + 150), (cx - 52, cy + 110), (cx - 50, cy - 10), (cx - 30, cy - 60), (cx - 22, cy - 150)]
    hm = shape_mask(W, H, hull)
    fw = rrect_mask(W, H, cx - 86, cy - 186, cx + 86, cy - 160, 10)
    rw = rrect_mask(W, H, cx - 80, cy + 142, cx + 80, cy + 176, 8)
    art = GP(art, np.maximum.reduce([hm, fw, rw]), body, body_d, seed=nx(), rough=1.3, streak=0.9)
    st = shape_mask(W, H, [(cx - 9, cy - 186), (cx + 9, cy - 186), (cx + 12, cy + 150), (cx - 12, cy + 150)], smooth=False) * hm
    art = GP(art, st, stripe, seed=nx(), rough=0.8, pad=6)
    sidepod = np.clip(hm - lift(hm, 0, -6), 0, 1)
    art = G(art, gaussian_filter(hm, 6) * hm * (np.mgrid[0:H, 0:W][1] > cx).astype(np.float32) * 0.6, body_d, seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1)
    # cockpit + helmet (top view: round helmet with visor arc)
    cock = shapes(W, H, [deform(ellipse_pts(cx, cy + 14, 30, 50, 14), random.Random(2), 0, 0)])
    art = GP(art, cock, "#20232a", seed=nx(), rough=0.6, pad=6)
    helm = circles(W, H, [(cx, cy + 22, 26)])
    art = GP(art, helm, WHITE, "#e8e2d6", seed=nx(), rough=0.6, pad=6)
    art = GP(art, strokes(W, H, [(arc_pts(cx, cy + 22, 18, -2.6, -0.54, 16), 9, None)]), "#2a3240", seed=nx(), rough=0.4, pad=4)
    art = GP(art, strokes(W, H, [([(cx, cy + 4), (cx, cy + 48)], 6, None)]), body, seed=nx(), rough=0.3, pad=4)
    # number roundel on the nose
    rnd = circles(W, H, [(cx, cy - 104, 20)])
    art = GP(art, rnd, num_col, seed=nx(), rough=0.5, pad=4)
    # highlight
    hi = np.clip(hm - lift(hm, 5, 0), 0, 1)
    art = OV(art, hi * 0.5, lambda m: tint(m, "#ffffff"))
    return art


def car_side(W, H, body, body_d, stripe, seed):
    """Side-view cartoon racer facing right: low wedge body, big rear wing, helmet with dark visor, fat wheels."""
    nx = Seq(seed)
    art = blank(W, H)
    rng = random.Random(seed)
    gy = H - 40
    sh = shapes(W, H, [ellipse_pts(W / 2, gy + 6, W * 0.42, 12, 16)])
    art = G(art, sh, "#000000", seed=nx(), density=0.3, edge=0.05, bloom=0, rough=3, feather=6)
    # speed lines behind
    lines = [([(20, gy - 120 + k * 30), (120 - k * 14, gy - 120 + k * 30)], 6, (0.4, 0.1)) for k in range(4)]
    art = G(art, strokes(W, H, lines), "#9aa3b2", seed=nx(), density=0.55, edge=0.2, rough=1)
    body_pts = [(150, gy - 30), (150, gy - 96), (230, gy - 104), (330, gy - 110), (420, gy - 96), (560, gy - 70), (640, gy - 52), (652, gy - 36), (630, gy - 22), (170, gy - 22)]
    bm = shape_mask(W, H, deform(body_pts, rng, 1, 0.01))
    wing = shapes(W, H, [[(120, gy - 170), (226, gy - 176), (222, gy - 146), (124, gy - 142)], [(160, gy - 150), (182, gy - 150), (196, gy - 96), (170, gy - 96)]], smooth=False)
    nosew = shapes(W, H, [[(600, gy - 40), (676, gy - 40), (680, gy - 22), (596, gy - 22)]], smooth=False)
    art = GP(art, np.maximum.reduce([bm, wing, nosew]), body, body_d, seed=nx(), rough=1.4, streak=0.9)
    stripe_m = shape_mask(W, H, [(160, gy - 70), (640, gy - 46), (646, gy - 36), (160, gy - 54)], smooth=False) * bm
    art = GP(art, stripe_m, stripe, seed=nx(), rough=0.8, pad=6)
    lo = np.clip(bm - lift(bm, 0, -10), 0, 1)
    art = G(art, gaussian_filter(lo, 3) * bm * 2, body_d, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1)
    art = OV(art, np.clip(bm - lift(bm, 0, 6), 0, 1) * 0.5, lambda m: tint(m, "#ffffff"))
    # number roundel
    art = GP(art, circles(W, H, [(470, gy - 70, 28)]), WHITE, seed=nx(), rough=0.6, pad=6)
    art = G(art, ring(W, H, 470, gy - 70, 28, 4), INK, seed=nx(), density=0.8, edge=0.2, rough=0.5)
    # cockpit + helmet (round with a dark visor, no face)
    art = GP(art, shapes(W, H, [[(300, gy - 108), (390, gy - 100), (380, gy - 88), (300, gy - 92)]]), "#20232a", seed=nx(), rough=0.5, pad=4)
    helm = circles(W, H, [(338, gy - 136, 36)])
    art = GP(art, helm, WHITE, "#ece6da", seed=nx(), rough=0.7, pad=6)
    visor = shapes(W, H, [[(342, gy - 150), (376, gy - 146), (372, gy - 126), (346, gy - 126)]])
    art = GP(art, visor, "#2a3a52", "#1c2636", seed=nx(), rough=0.5, pad=4)
    art = OV(art, strokes(W, H, [([(350, gy - 146), (368, gy - 143)], 3, None)]) * 0.8, lambda m: tint(m, "#9fc4ff"))
    art = GP(art, strokes(W, H, [(arc_pts(338, gy - 136, 30, -2.5, -1.1, 14), 7, None)]), body, seed=nx(), rough=0.4, pad=4)
    # wheels
    for wx, r in [(214, 52), (566, 46)]:
        art = GP(art, circles(W, H, [(wx, gy - r + 6, r)]), INK, "#353944", seed=nx(), rough=1.0, pad=6)
        art = GP(art, circles(W, H, [(wx, gy - r + 6, r * 0.5)]), "#c9ced8", "#9aa1ad", seed=nx(), rough=0.5, pad=6)
        art = GP(art, circles(W, H, [(wx, gy - r + 6, r * 0.16)]), body, seed=nx(), rough=0.3, pad=4)
        spokes = strokes(W, H, [([(wx, gy - r + 6), (wx + math.cos(a) * r * 0.45, gy - r + 6 + math.sin(a) * r * 0.45)], 4, None) for a in np.linspace(0, math.tau, 6)[:5]])
        art = G(art, spokes, "#7a8290", seed=nx(), density=0.6, edge=0, rough=0.4)
    return art


if "track" in PARTS:
    W, H = 780, 1060
    nx = Seq(60100)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = solid(W, H, GRASS)
    art = GP(art, np.ones((H, W), np.float32), GRASS, GRASS_L, seed=nx(), rough=0, streak=1.0)
    mow = ((((xx * 0.5 + yy) / 70).astype(int) % 2) == 0).astype(np.float32)
    art = OV(art, gaussian_filter(mow, 2) * 0.14, lambda m: tint(m, "#d8f5b0"))
    # crayon-ish grass tufts
    rng = random.Random(4)
    tufts = []
    for _ in range(220):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        for k in range(3):
            a = -math.pi / 2 + (k - 1) * 0.5 + rng.gauss(0, 0.1)
            tufts.append(([(x, y), (x + math.cos(a) * 10, y + math.sin(a) * 10)], 2.2, (0.0, 0.6)))
    art = G(art, strokes(W, H, tufts), GRASS_D, seed=nx(), density=0.55, edge=0.1, rough=0.6)
    clear()
    cl = loop_pts(110, 120, W - 110, H - 150, 150)
    road = strokes(W, H, [(cl, 112, None)])
    art = GP(art, road, ASPH, ASPH_L, seed=nx(), rough=1.4, streak=1.2)
    grit = road * np.clip(fbm(W, H, 9, 3, 2) - 0.55, 0, 1) * 2
    art = G(art, grit, "#3a3e48", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.4)
    # dashed centre line
    dash = []
    for i in range(0, len(cl) - 6, 8):
        dash.append((cl[i:i + 4], 5, None))
    art = GP(art, strokes(W, H, dash), WHITE, seed=nx(), rough=0.5, pad=4)
    # curbs on both edges (red/white blocks), only round the corners and chicane
    for side in (-1, 1):
        edge = offset(cl, side * 60)
        reds, whites = [], []
        for i in range(0, len(edge) - 3, 3):
            seg = (edge[i:i + 4], 13, None)
            (reds if (i // 3) % 2 else whites).append(seg)
        art = GP(art, strokes(W, H, whites), WHITE, "#efe9dc", seed=nx(), rough=0.6, pad=6)
        art = GP(art, strokes(W, H, reds), RED, RED_D, seed=nx(), rough=0.6, pad=6)
    clear()
    # start/finish checkered line across the bottom straight
    sx = W / 2 - 40; by = H - 150
    sq = 14
    checks = []
    for r in range(-4, 4):
        for c in range(2):
            if (r + c) % 2 == 0:
                checks.append(rect(sx + c * sq, by + r * sq, sx + (c + 1) * sq, by + (r + 1) * sq))
    band = shapes(W, H, [rect(sx, by - 4 * sq, sx + 2 * sq, by + 4 * sq)], smooth=False)
    art = GP(art, band, WHITE, seed=nx(), rough=0.5, pad=4)
    art = GP(art, shapes(W, H, checks, smooth=False), INK, seed=nx(), rough=0.5, pad=4)
    # grid boxes
    gb = strokes(W, H, [([(sx + 60 + k * 70, by - 50), (sx + 60 + k * 70, by - 10), (sx + 100 + k * 70, by - 10)], 4, None) for k in range(3)] +
                 [([(sx + 95 + k * 70, by + 10), (sx + 95 + k * 70, by + 50), (sx + 135 + k * 70, by + 50)], 4, None) for k in range(3)])
    art = GP(art, gb, WHITE, seed=nx(), rough=0.5, pad=4)
    # tyre stacks at the outer corners
    stacks = []
    for (x, y) in [(28, 40), (W - 30, 46), (24, H - 70), (W - 28, H - 66), (W - 22, H / 2 - 40)]:
        for dx, dy in [(-14, 0), (14, 0), (0, -14), (0, 14)]:
            stacks.append((x + dx, y + dy, 13))
    sm = circles(W, H, stacks)
    art = GP(art, sm, INK, "#3a3e48", seed=nx(), rough=0.8, pad=6)
    art = GP(art, circles(W, H, [(x, y, 5) for x, y, _ in stacks]), "#7a8290", seed=nx(), rough=0.3, pad=4)
    # flag posts in the infield corners
    art = add_grain(art, 7, 0.03)
    save_rgb(art, f"{OUT}/track.webp", size=(560, 761), quality=74)
    preview(art, "ub-track")
    clear()

if "cartop" in PARTS:
    W, H = 240, 420
    art = car_top(W, H, 120, 214, RED, RED_D, WHITE, 61100)
    preview(art, "ub-cartop", tone="#5aa65a")
    save(art, f"{OUT}/cartop.webp", max_w=120, quality=82)
    art = car_top(W, H, 120, 214, BLUE, BLUE_D, "#ffd23f", 61500, num_col="#ffd23f")
    save(art, f"{OUT}/cartop2.webp", max_w=120, quality=82)
    clear()

if "carside" in PARTS:
    W, H = 720, 300
    art = car_side(W, H, RED, RED_D, WHITE, 62100)
    preview(art, "ub-carside", tone="#fbf6ea")
    save(art, f"{OUT}/carside.webp", max_w=440, quality=82)
    art = car_side(W, H, BLUE, BLUE_D, "#ffd23f", 62500)
    preview(art, "ub-carside2", tone="#fbf6ea")
    save(art, f"{OUT}/carside2.webp", max_w=440, quality=82)
    clear()

if "trophy" in PARTS:
    W, H = 360, 440
    nx = Seq(63100)
    art = blank(W, H)
    cx = 180
    cup = shape_mask(W, H, [(cx - 110, 60), (cx + 110, 60), (cx + 100, 120), (cx + 60, 200), (cx + 20, 230), (cx - 20, 230), (cx - 60, 200), (cx - 100, 120)])
    handles = strokes(W, H, [(arc_pts(cx - 104, 120, 46, math.pi * 0.5, math.pi * 1.55, 24), 14, None), (arc_pts(cx + 104, 120, 46, -math.pi * 0.55, math.pi * 0.5, 24), 14, None)])
    stem = shapes(W, H, [[(cx - 16, 226), (cx + 16, 226), (cx + 24, 300), (cx - 24, 300)], [(cx - 70, 300), (cx + 70, 300), (cx + 80, 330), (cx - 80, 330)]], smooth=False)
    base = rrect_mask(W, H, cx - 96, 330, cx + 96, 410, 8)
    art = GP(art, base, "#2b2f3a", "#3b404d", seed=nx(), rough=0.8, streak=0.8)
    plate = rrect_mask(W, H, cx - 56, 352, cx + 56, 388, 4)
    art = FO(art, plate, GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    gold = np.maximum.reduce([cup, handles, stem])
    art = GP(art, gold, GOLD, "#f0c24a", seed=nx(), rough=1.0, streak=0.7)
    shade = gaussian_filter(cup, 8) * cup * (np.mgrid[0:H, 0:W][1] > cx + 30).astype(np.float32)
    art = G(art, shade, "#a8741a", seed=nx(), density=0.5, edge=0.2, rough=1.5)
    hi = shapes(W, H, [[(cx - 76, 76), (cx - 52, 76), (cx - 40, 180), (cx - 56, 176)]])
    art = OV(art, gaussian_filter(hi, 2) * 0.8, lambda m: tint(m, "#fff4c8"))
    rim_ = shapes(W, H, [rect(cx - 114, 52, cx + 114, 70)], smooth=False)
    art = GP(art, rim_, "#f4c955", "#e0a82e", seed=nx(), rough=0.6, pad=4)
    star = shapes(W, H, [[(cx + math.cos(-math.pi / 2 + k * math.pi / 5) * (34 if k % 2 == 0 else 15), 140 + math.sin(-math.pi / 2 + k * math.pi / 5) * (34 if k % 2 == 0 else 15)) for k in range(10)]], smooth=False)
    art = GP(art, star, RED, RED_D, seed=nx(), rough=0.6, pad=4)
    sparks = strokes(W, H, [([(x - 10, y), (x + 10, y)], 4, None) for x, y in [(40, 40), (320, 70), (300, 250)]] + [([(x, y - 10), (x, y + 10)], 4, None) for x, y in [(40, 40), (320, 70), (300, 250)]])
    art = GP(art, sparks, "#ffd23f", seed=nx(), rough=0.4, pad=4)
    preview(art, "ub-trophy", tone="#fbf6ea")
    save(art, f"{OUT}/trophy.webp", max_w=200, quality=82)
    clear()

if "flags" in PARTS:
    W, H = 640, 380
    nx = Seq(64100)
    art = blank(W, H)
    for side in (-1, 1):
        px, py = W / 2 + side * 40, 360
        tx, ty = W / 2 - side * 110, 50
        pole = strokes(W, H, [([(px, py), (tx, ty)], 9, None)])
        art = GP(art, pole, "#8a5a32", "#5e3a1e", seed=nx(), rough=0.6, pad=6)
        # flag: a waving quad from the top of the pole outward
        fx = -side
        rows, cols = 4, 5
        cell = 32
        sq_b, sq_w = [], []
        for r in range(rows):
            for c in range(cols):
                def P(u, v):
                    wave = 10 * math.sin(u / cols * math.pi * 1.6 + 0.6)
                    return (tx + fx * u * cell, ty + 4 + v * cell + wave + u * 3)
                q = [P(c, r), P(c + 1, r), P(c + 1, r + 1), P(c, r + 1)]
                (sq_b if (r + c) % 2 == 0 else sq_w).append(q)
        art = GP(art, shapes(W, H, sq_w, smooth=False), WHITE, "#ece6da", seed=nx(), rough=0.6, pad=6)
        art = GP(art, shapes(W, H, sq_b, smooth=False), INK, seed=nx(), rough=0.6, pad=6)
        knob = circles(W, H, [(tx, ty, 9)])
        art = GP(art, knob, GOLD, seed=nx(), rough=0.4, pad=4)
    preview(art, "ub-flags", tone="#fbf6ea")
    save(art, f"{OUT}/flags.webp", max_w=260, quality=82)
    clear()

if "board" in PARTS:
    # pit board: black frame on a pole, white face (number is live text)
    W, H = 360, 420
    nx = Seq(65100)
    art = blank(W, H)
    pole = strokes(W, H, [([(180, 250), (180, 410)], 16, None)])
    art = GP(art, pole, "#8a8f9a", "#5d626d", seed=nx(), rough=0.6, pad=6)
    frame = rrect_mask(W, H, 20, 20, 340, 260, 18)
    art = GP(art, frame, INK, "#30343e", seed=nx(), rough=1.0, streak=0.8)
    face = rrect_mask(W, H, 40, 40, 320, 240, 10)
    art = GP(art, face, WHITE, "#f1ece0", seed=nx(), rough=0.8, streak=0.6)
    bolts = circles(W, H, [(32, 32, 5), (328, 32, 5), (32, 248, 5), (328, 248, 5)])
    art = GP(art, bolts, "#9aa1ad", seed=nx(), rough=0.3, pad=4)
    preview(art, "ub-board", tone="#5aa65a")
    save(art, f"{OUT}/board.webp", max_w=180, quality=82)
