"""Kota Tua Batavia — pen-and-wash watercolour of an (original) colonial town-hall square in warm late-afternoon light,
onthel bicycles, cast-iron street lamp; postage stamp + postmark for the vintage postcard frames.
Run: python3 -I kota-tua-batavia.py [part ...]   parts: scene bike lamp stamp postmark paper
Assets -> public/themes/art/kota-tua-batavia/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f4_lib import *

OUT = outdir("kota-tua-batavia")
PARTS = sys.argv[1:] or ["scene", "bike", "lamp", "stamp", "postmark", "waves", "paper"]

PAPER = "#f4ead6"
SEPIA = "#4a3426"
TERRA, TERRA_L = "#b9573a", "#d98b5f"
CREAM, CREAM_D = "#efdcb6", "#d9bf8f"
SHUTTER, SHUTTER_D = "#5d8676", "#3f5f54"
VIOLET = "#8a83a3"
WARM = "#f0bf73"
BIKES = [("#c4473b", "#e0735f"), ("#6fae9b", "#9fd0bf"), ("#dfa93a", "#f0cd70"), ("#d8879a", "#f0b3bf")]


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def box(pts):
    return [pts + [pts[0]]]


def bike_geom(x, y, r, facing=1):
    """Onthel (step-through, front basket) side view. Returns dict of polylines; (x, y) = rear wheel contact."""
    f = facing
    X = lambda k: x + f * k * r
    R = (x, y - r); F = (X(3.05), y - r)
    B = (X(1.15), y - r * 0.72)
    S = (X(0.78), y - r * 2.05)
    Ht = (X(2.55), y - r * 2.3); Hb = (X(2.72), y - r * 1.72)
    g = {}
    g["frame"] = [
        curve([Hb, (X(2.1), y - r * 1.05), (X(1.5), y - r * 0.8), B], 24),           # curved down tube
        curve([(X(2.6), y - r * 2.05), (X(1.9), y - r * 1.45), (X(1.35), y - r * 1.0), (X(1.2), y - r * 0.85)], 24),  # twin loop tube
        [B, R], [S, R], [S, B], [Ht, Hb],
        curve([Hb, (X(2.92), y - r * 1.35), F], 12),                                 # fork
    ]
    g["bar"] = [curve([Ht, (X(2.5), y - r * 2.62), (X(2.2), y - r * 2.72), (X(1.95), y - r * 2.62)], 14)]
    g["saddle"] = (X(0.72), y - r * 2.12)
    g["wheels"] = [R, F]
    g["fender"] = [arc_pts(R[0], R[1], r * 1.1, math.pi * 1.05, math.pi * 1.95, 22), arc_pts(F[0], F[1], r * 1.1, math.pi * 1.1, math.pi * 1.92, 22)]
    bx0, bx1 = (X(2.75), X(3.45)) if f > 0 else (X(3.45), X(2.75))
    g["basket"] = (bx0, y - r * 2.6, bx1, y - r * 2.05)
    g["stand"] = [B, (X(0.9), y)]
    g["rack"] = [[(X(-0.15), y - r * 1.7), S], [(X(-0.15), y - r * 1.7), R]]
    return g


def paint_bike(art, W, H, x, y, r, cols, nx, facing=1, ink_col=SEPIA, flowers=True):
    g = bike_geom(x, y, r, facing)
    tyre = np.maximum.reduce([ring_m(W, H, cx, cy, r, max(2.2, r * 0.085)) for cx, cy in g["wheels"]])
    art = G(art, tyre, "#2f2a26", "#4a423a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.8, feather=0.6, gran=0.1)
    frame = strokes(W, H, [(p, max(2.4, r * 0.14), None) for p in g["frame"]] + [(p, max(2, r * 0.11), None) for p in g["fender"]])
    art = G(art, frame, cols[0], cols[1], seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=1.0, feather=0.6)
    sad = ellipses(W, H, [(g["saddle"][0], g["saddle"][1], r * 0.32, r * 0.11, -4 * facing)])
    art = G(art, sad, "#5a3a26", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    bx0, by0, bx1, by1 = g["basket"]
    bask = rects(W, H, [(bx0, by0, bx1, by1)], r=2)
    art = G(art, bask, "#c99a5a", "#a87a3e", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=1, feather=0.7)
    if flowers:
        rng = random.Random(nx())
        fl = [((bx0 + bx1) / 2 + rng.uniform(-r * .32, r * .32), by0 - rng.uniform(0, r * .22), r * rng.uniform(.08, .13)) for _ in range(7)]
        art = G(art, circles(W, H, fl), "#f2f0e6", "#f6c6c0", seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1, feather=0.6)
        lv = circles(W, H, [(c[0] + rng.uniform(-4, 4), c[1] + 4, c[2] * .7) for c in fl[:4]])
        art = G(art, lv, "#6d8b55", seed=nx(), density=0.6, edge=0.4, bloom=0, rough=1, feather=0.6)
    # ink
    pl = []
    for cx, cy in g["wheels"]:
        pl.append(arc_pts(cx, cy, r, 0, math.tau, 48))
        pl.append(arc_pts(cx, cy, r * 0.12, 0, math.tau, 12))
        for k in range(14):
            a = k * math.tau / 14
            pl.append([(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12), (cx + math.cos(a + .25) * r * 0.92, cy + math.sin(a + .25) * r * 0.92)])
    art = ink(art, pl, ink_col, width=max(0.6, r * 0.022), seed=nx(), jitter=0.25, alpha=0.75)
    pl = g["frame"] + g["bar"] + g["fender"] + [g["stand"]] + g["rack"]
    pl += box(rect_pts(bx0, by0, bx1, by1)) + [[(bx0, by0 + (by1 - by0) * k / 4), (bx1, by0 + (by1 - by0) * k / 4)] for k in (1, 2, 3)]
    pl += [[(bx0 + (bx1 - bx0) * k / 5, by0), (bx0 + (bx1 - bx0) * k / 5, by1)] for k in (1, 2, 3, 4)]
    art = ink(art, pl, ink_col, width=max(0.8, r * 0.04), seed=nx(), jitter=0.35, alpha=0.85)
    return art


def lamp_geom(x, y, h):
    """Cast-iron lamp post, base at (x, y), height h."""
    s = h / 300
    post = [(x, y), (x, y - h * 0.86)]
    base = [(x - 14 * s, y), (x - 10 * s, y - 34 * s), (x - 6 * s, y - 60 * s), (x + 6 * s, y - 60 * s), (x + 10 * s, y - 34 * s), (x + 14 * s, y)]
    arm = curve([(x, y - h * 0.8), (x - 18 * s, y - h * 0.84), (x - 30 * s, y - h * 0.8), (x - 30 * s, y - h * 0.76)], 14)
    arm2 = curve([(x, y - h * 0.8), (x + 18 * s, y - h * 0.84), (x + 30 * s, y - h * 0.8), (x + 30 * s, y - h * 0.76)], 14)
    top = y - h
    lantern = [(x - 16 * s, top + 10 * s), (x + 16 * s, top + 10 * s), (x + 10 * s, top + 44 * s), (x - 10 * s, top + 44 * s)]
    cap = [(x - 20 * s, top + 12 * s), (x, top - 6 * s), (x + 20 * s, top + 12 * s)]
    return post, base, arm, arm2, lantern, cap, s


def paint_lamp(art, W, H, x, y, h, nx, glow_on=True):
    post, base, arm, arm2, lantern, cap, s = lamp_geom(x, y, h)
    m = np.maximum.reduce([strokes(W, H, [(post, 7 * s, None), (arm, 3.5 * s, None), (arm2, 3.5 * s, None)]), shapes(W, H, [base], smooth=False), shapes(W, H, [cap], smooth=False)])
    art = G(art, m, "#3b3a36", "#2a2b2a", seed=nx(), density=0.92, edge=0.4, bloom=0.05, rough=0.8, feather=0.6)
    glass = shapes(W, H, [lantern], smooth=False)
    if glow_on:
        art = G(art, gaussian_filter(glass, 12 * s) * 1.4, "#ffd98a", seed=nx(), density=0.45, edge=0, bloom=0, rough=0, feather=2)
    art = G(art, glass, "#f6dc9a", "#f0b85c", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=0.8, feather=0.6)
    pl = [post, arm, arm2, base + [base[0]], lantern + [lantern[0]], cap, [((lantern[0][0] + lantern[1][0]) / 2, lantern[0][1]), ((lantern[2][0] + lantern[3][0]) / 2, lantern[2][1])]]
    return ink(art, pl, "#2a2420", width=1.3 * max(1, s), seed=nx(), jitter=0.3, alpha=0.8)


if "scene" in PARTS:
    W, H = 820, 600
    nx = Seq(20100)
    rng = random.Random(7)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    # sky: cool grey-blue high up, warm apricot towards the horizon (paper left white in places)
    sky = (yy < 446).astype(np.float32)
    art = G(art, sky * np.clip(1 - yy / 260, 0, 1) ** 0.8, "#a9bcc4", "#c5d0cf", seed=nx(), density=0.7, edge=0.2, bloom=0.5, rough=10, holes=0.15)
    art = G(art, sky * np.clip((yy - 40) / 260, 0, 1), "#f3c48c", "#f6d9a8", seed=nx(), density=0.7, edge=0.15, bloom=0.4, rough=10)
    sun = np.exp(-(((xx - 60) / 260) ** 2 + ((yy - 300) / 140) ** 2)) * sky
    art = G(art, sun, "#f6b56c", seed=nx(), density=0.45, edge=0, bloom=0.3, rough=6)
    # distant tree masses either side + a neighbouring house (left)
    blobs = []
    for cx0, cy0, sx, sy, n in [(40, 270, 110, 80, 26), (770, 262, 90, 80, 22), (690, 300, 40, 40, 6), (150, 300, 40, 36, 6)]:
        for k in range(n):
            a = rng.uniform(0, math.tau); d = rng.random() ** 0.6
            blobs.append(deform(ellipse_pts(cx0 + math.cos(a) * sx * d, cy0 + math.sin(a) * sy * d * 0.9, rng.uniform(16, 30), rng.uniform(12, 22), 9, rng.uniform(0, 3)), rng, 2, 0.12))
    trees = np.maximum(shapes(W, H, blobs), rect_m(W, H, -10, 300, 130, 440) * 0 + shapes(W, H, [[(-20, 300), (150, 300), (150, 440), (-20, 440)], [(690, 300), (840, 300), (840, 440), (690, 440)]], smooth=False) * (yy > 330))
    art = G(art, trees, "#7f9157", "#a6a764", seed=nx(), density=0.75, edge=0.55, bloom=0.45, rough=6, gran=0.35)
    shade = trees * np.clip((fbm(W, H, 5, 14, 3) - 0.45) * 3, 0, 1) * np.clip((xx - 20) / 140 % 1 + 0.2, 0, 1)
    art = G(art, shade, "#55683f", "#43573a", seed=nx(), density=0.6, edge=0.6, bloom=0.2, rough=4)
    trunks = strokes(W, H, [(curve([(60, 440), (64, 380), (58, 350)], 10), 9, (0, 0.4)), (curve([(780, 440), (774, 380), (782, 350)], 10), 9, (0, 0.4))])
    art = G(art, trunks, "#5a4636", seed=nx(), density=0.75, edge=0.4, bloom=0, rough=1)
    # roof (hipped, terracotta) + cupola
    roof = [(98, 268), (722, 268), (668, 196), (152, 196)]
    roofm = shapes(W, H, [roof], smooth=False)
    art = G(art, roofm, TERRA, TERRA_L, seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=2.5, gran=0.25)
    art = G(art, roofm * np.clip((yy - 196) / 72, 0, 1) * 0.7, "#8e3f2a", seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=2)
    art = G(art, roofm * (fbm(W, H, 61, 9, 2) > 0.62), "#e9a57a", seed=nx(), density=0.4, edge=0.4, bloom=0.2, rough=2)
    # cupola
    drum = rect_m(W, H, 376, 140, 424, 202)
    dome = shapes(W, H, [[(368, 142)] + arc_pts(400, 142, 32, math.pi, math.tau, 20, 0.9) + [(432, 142)]], smooth=False)
    lant = rect_m(W, H, 392, 98, 408, 116)
    art = G(art, drum, CREAM, CREAM_D, seed=nx(), density=0.6, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, np.maximum(dome, lant), "#a4553a", "#7d3f2c", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, rect_m(W, H, 384, 152, 394, 190) + rect_m(W, H, 406, 152, 416, 190), "#4b3d33", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
    # facade walls + central bay with pediment
    wall = rect_m(W, H, 104, 262, 716, 436)
    bay = np.maximum(rect_m(W, H, 344, 236, 456, 436), shapes(W, H, [[(334, 238), (466, 238), (400, 204)]], smooth=False))
    art = G(art, np.maximum(wall, bay), CREAM, "#f5e6c6", seed=nx(), density=0.55, edge=0.45, bloom=0.4, rough=2, gran=0.15)
    # warm raking light glaze + cool eave shadow + shaded right return of the bay
    art = G(art, np.maximum(wall, bay) * np.clip(1 - (xx - 100) / 700, 0.15, 1) * 0.55, WARM, seed=nx(), density=0.5, edge=0.1, bloom=0.3, rough=4)
    eave = rect_m(W, H, 104, 266, 716, 284) * (1 - rect_m(W, H, 344, 230, 456, 290))
    art = G(art, eave, VIOLET, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=2)
    art = G(art, rect_m(W, H, 444, 238, 456, 436) + rect_m(W, H, 700, 262, 716, 436), VIOLET, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1.5)
    plinth = rect_m(W, H, 104, 424, 716, 438)
    art = G(art, plinth, "#9a8a76", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1.5)
    # windows with open shutters (two floors), central door + upper balcony window
    bays = [124 + i * 44 for i in range(5)] + [474 + i * 44 for i in range(5)]
    wins, shut, panes = [], [], []
    for bx in bays:
        for (y0, y1) in [(296, 352), (366, 420)]:
            wins.append((bx + 8, y0, bx + 30, y1))
            shut += [(bx, y0, bx + 8, y1), (bx + 30, y0, bx + 38, y1)]
    winm = rects(W, H, wins)
    art = G(art, winm, "#4f4238", "#6c5a4a", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1)
    art = G(art, winm * np.clip((yy % 37) / 37, 0, 1) * 0.0 + winm * (fbm(W, H, 33, 6, 1) > 0.6) * 0.5, "#e6b56a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    sills = rects(W, H, [(x0 - 10, y1, x1 + 10, y1 + 4) for x0, y0, x1, y1 in wins])
    art = G(art, sills, "#b9a27c", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=0.8)
    art = G(art, rects(W, H, [(x0 - 8, y1 + 4, x1 + 8, y1 + 12) for x0, y0, x1, y1 in wins]), VIOLET, seed=nx(), density=0.3, edge=0.1, bloom=0, rough=1)
    stains = wall * np.clip((fbm(W, H, 71, 30, 3) - 0.55) * 3, 0, 1) * np.clip((yy - 330) / 100, 0, 1)
    art = G(art, stains, "#c9b08a", "#b8a98e", seed=nx(), density=0.35, edge=0.3, bloom=0.5, rough=4, gran=0.4)
    shm = rects(W, H, shut)
    art = G(art, shm, SHUTTER, "#7aa292", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1)
    door = arches(W, H, [(378, 350, 422, 436)])
    upw = arches(W, H, [(384, 270, 416, 336)])
    art = G(art, np.maximum(door, upw), "#4a3a2e", "#6a5040", seed=nx(), density=0.88, edge=0.4, bloom=0.1, rough=1)
    # long cast shadow from the lamp + bikes over the square, sun from the left
    plaza = (yy > 436).astype(np.float32)
    art = G(art, plaza, "#dcc296", "#c9aa7d", seed=nx(), density=0.6, edge=0.1, bloom=0.5, rough=6, gran=0.35)
    art = G(art, plaza * np.clip((yy - 436) / 180, 0, 1) * 0.6, "#b99872", seed=nx(), density=0.5, edge=0.05, bloom=0.4, rough=6, gran=0.3)
    # building shadow band at its foot
    art = G(art, rect_m(W, H, 104, 436, 716, 446), "#9a8aa0", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=2)
    shadows = shapes(W, H, [[(150, 560), (156, 556), (430, 600), (400, 606)],  # lamp
                            [(470, 556), (640, 540), (820, 580), (820, 606), (520, 606)]], smooth=False)
    art = G(art, gaussian_filter(shadows, 2.5), VIOLET, "#9d93b3", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=3)
    # tiny figures strolling by the door (no faces: two dots of colour + shadow)
    figs = []
    for fx, fc in [(300, "#c9564a"), (312, "#3f4f6a"), (540, "#e2b63e"), (552, "#5f7f6c")]:
        figs.append((fx, fc))
    for fx, fc in figs:
        art = G(art, ellipses(W, H, [(fx, 448, 4.2, 10, 0)]), fc, seed=nx(), density=0.85, edge=0.4, bloom=0, rough=0.8, feather=0.6)
        art = G(art, circles(W, H, [(fx, 434, 3.4)]), "#6a4a3a", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.5, feather=0.5)
    # lamp post (left foreground) + onthel bikes (right foreground, parked in a row)
    art = paint_lamp(art, W, H, 150, 560, 280, nx)
    for k, (bx, cols) in enumerate(zip([470, 560, 650], BIKES)):
        art = paint_bike(art, W, H, bx, 560 + k * 3, 30, cols, nx, facing=1, flowers=k != 1)
    # ink drawing of the architecture
    pl = [roof + [roof[0]], [(98, 268), (722, 268)], [(104, 284), (716, 284)], [(104, 262), (104, 436)], [(716, 262), (716, 436)],
          [(344, 238), (344, 436)], [(456, 238), (456, 436)], [(334, 238), (466, 238), (400, 204), (334, 238)], [(104, 424), (716, 424)], [(60, 438), (790, 438)],
          [(376, 202), (376, 140), (424, 140), (424, 202)], [(392, 116), (392, 98), (408, 98), (408, 116)], [(400, 98), (400, 70)], [(400, 72), (412, 76), (400, 80)], arc_pts(400, 142, 32, math.pi, math.tau, 20, 0.9), [(104, 356), (344, 356)], [(456, 356), (716, 356)]]
    for x0, y0, x1, y1 in wins:
        pl += box(rect_pts(x0, y0, x1, y1)) + [[((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)]]
    for x0, y0, x1, y1 in shut:
        pl += box(rect_pts(x0, y0, x1, y1))
    pl += [[(378, 436), (378, 372)] + arc_pts(400, 372, 22, math.pi, math.tau, 14) + [(422, 436)], [(384, 336), (384, 286)] + arc_pts(400, 286, 16, math.pi, math.tau, 12) + [(416, 336)]]
    # roof tile ticks and a few cobbles
    for k in range(70):
        ty = rng.uniform(204, 262); tx = 152 + (ty - 196) / 72 * -54 + rng.uniform(10, 560 + (ty - 196) / 72 * 108)
        pl.append([(tx, ty), (tx + rng.uniform(4, 9), ty + rng.uniform(-1, 1))])
    for k in range(90):
        cy = rng.uniform(452, 596); s_ = 0.5 + (cy - 440) / 140
        cx = rng.uniform(0, W)
        pl.append([(cx, cy), (cx + 9 * s_, cy + rng.uniform(-.4, .4))])
    art = ink(art, pl, SEPIA, width=1.25, seed=nx(), jitter=0.4, alpha=0.75, dry=0.04)
    # unfinished watercolour edge: wash fades into the paper
    edge = rect_m(W, H, 18, 14, W - 18, H - 14)
    edge = np.clip((displace(gaussian_filter(edge, 6), 77, 14, 40) - 0.25) * 1.8, 0, 1)
    art[..., 3] *= edge
    preview(art, "kt-scene", tone=PAPER)
    pap = paper_arr(W, H, PAPER, seed=9)
    comp = np.asarray(on_paper(art, PAPER), np.float32) / 255
    save_rgb(np.concatenate([comp, np.ones((H, W, 1), np.float32)], -1), f"{OUT}/scene.webp", size=(700, 512), quality=78)
    clear()

if "bike" in PARTS:
    W, H = 300, 200
    nx = Seq(21100)
    art = blank(W, H)
    sh = ellipses(W, H, [(150, 182, 120, 7, 0)])
    art = G(art, sh, VIOLET, seed=nx(), density=0.35, edge=0.1, bloom=0, rough=2, feather=3)
    art = paint_bike(art, W, H, 54, 182, 46, BIKES[0], nx, facing=1)
    preview(art, "kt-bike", tone=PAPER)
    save(art, f"{OUT}/bike.webp", max_w=240, quality=84)
    clear()

if "lamp" in PARTS:
    W, H = 140, 420
    nx = Seq(22100)
    art = blank(W, H)
    art = paint_lamp(art, W, H, 70, 410, 380, nx)
    preview(art, "kt-lamp", tone=PAPER)
    save(art, f"{OUT}/lamp.webp", max_w=90, quality=84)
    clear()

if "stamp" in PARTS:
    # postage stamp: perforated paper, framed vignette of the cupola tower against an apricot sky (engraved feel)
    W, H = 220, 260
    nx = Seq(23100)
    art = blank(W, H)
    perf = rect_m(W, H, 10, 10, W - 10, H - 10)
    holes = circles(W, H, [(x, y, 6.2) for x in np.arange(10, W - 9, 17.5) for y in (10, H - 10)] + [(x, y, 6.2) for y in np.arange(10, H - 9, 17.5) for x in (10, W - 10)])
    paperm = np.clip(perf - holes, 0, 1)
    art = OV(art, paperm, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fbf5e8"), np.float32), m[..., None]], -1))
    inner = rect_m(W, H, 28, 28, W - 28, H - 56)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, inner * np.clip((yy - 28) / 180, 0, 1), "#f0b878", "#e99a64", seed=nx(), density=0.75, edge=0.3, bloom=0.3, rough=2)
    art = G(art, inner * np.clip(1 - (yy - 28) / 120, 0, 1), "#a9bcc4", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=2)
    tower = np.maximum.reduce([rect_m(W, H, 84, 120, 136, 204), shapes(W, H, [[(74, 122)] + arc_pts(110, 122, 36, math.pi, math.tau, 20, 0.9) + [(146, 122)]], smooth=False),
                               rect_m(W, H, 102, 72, 118, 92), rect_m(W, H, 40, 186, 180, 204)])
    art = G(art, tower * inner, TERRA, "#8d4430", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1)
    art = G(art, rect_m(W, H, 94, 134, 104, 176) + rect_m(W, H, 116, 134, 126, 176), "#3e2c22", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.8)
    pl = box(rect_pts(28, 28, W - 28, H - 56)) + box(rect_pts(22, 22, W - 22, H - 22))
    pl += [[(110, 72), (110, 48)], [(110, 50), (122, 54), (110, 58)]]
    pl += [[(34, 40 + k * 6), (60 + (k % 3) * 8, 40 + k * 6)] for k in range(6)]
    art = ink(art, pl, "#7b2f22", width=1.3, seed=nx(), jitter=0.25, alpha=0.85)
    # value tablet at the bottom (a small red band)
    art = G(art, rect_m(W, H, 28, H - 50, W - 28, H - 28), "#b8432f", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=1)
    art = ink(art, [[(46 + k * 13, H - 39), (52 + k * 13, H - 39)] for k in range(10)], "#fbe9d8", width=2.2, seed=nx(), jitter=0.2, alpha=0.9)
    preview(art, "kt-stamp", tone=PAPER)
    save(art, f"{OUT}/stamp.webp", max_w=130, quality=84)
    clear()

if "postmark" in PARTS:
    # cancellation: double ring + wavy bars, uneven inked impression
    W, H = 360, 170
    m = np.maximum(ring_m(W, H, 85, 85, 72, 4), ring_m(W, H, 85, 85, 56, 2.4))
    bars = [[(150 + t * 200, 52 + 18 * k + 6 * math.sin(t * 9 + k)) for t in np.linspace(0, 1, 60)] for k in range(5)]
    m = np.maximum(m, strokes(W, H, [(b, 4.2, None) for b in bars]))
    art = LC(blank(W, H), m, "#3b2c3a", seed=4, wear=0.55, rough=1.6)
    art[..., 3] *= 0.85
    preview(art, "kt-postmark", tone=PAPER)
    save(art, f"{OUT}/postmark.webp", max_w=240, quality=84)
    clear()

if "waves" in PARTS:
    # divider: three wavy cancellation bars
    W, H = 380, 60
    bars = [[(10 + t * 360, 16 + 13 * k + 5 * math.sin(t * 12 + k * .8)) for t in np.linspace(0, 1, 80)] for k in range(3)]
    m = strokes(W, H, [(b, 3.4, (0.03, 0.06)) for b in bars])
    art = LC(blank(W, H), m, "#5a3a2c", seed=8, wear=0.5, rough=1.4)
    art[..., 3] *= 0.85
    preview(art, "kt-waves", tone=PAPER)
    save(art, f"{OUT}/waves.webp", max_w=200, quality=84)
    clear()

if "paper" in PARTS:
    S = 384
    n1 = wrap_noise(S, S, 3, 40); n2 = wrap_noise(S, S, 4, 0.8); n3 = wrap_noise(S, S, 5, 8)
    fib = gaussian_filter(np.random.default_rng(6).random((S, S)).astype(np.float32), (0.5, 7), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    v = 0.965 + 0.05 * (n1 - .5) + 0.025 * (n2 - .5) + 0.02 * (n3 - .5) + 0.008 * fib
    rgbv = np.clip(np.array(hex_rgb(PAPER), np.float32) * v[..., None], 0, 1)
    # foxing spots
    spots = np.clip((wrap_noise(S, S, 8, 3) - 0.86) * 9, 0, 1)
    rgbv = rgbv * (1 - spots[..., None] * np.array([0.04, 0.09, 0.16], np.float32))
    save_rgb(np.concatenate([rgbv, np.ones((S, S, 1), np.float32)], -1), f"{OUT}/paper.webp", quality=70)

kb(OUT)
