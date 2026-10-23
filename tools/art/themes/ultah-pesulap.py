"""Ultah Pesulap — a kids' magic-show birthday in gouache: a top hat with a friendly white rabbit peeking out, a wand
with a gold star, fanned playing cards (plain pips, no faces), violet velvet curtains with gold tassels and a scalloped
valance with fringe. Run: python3 -I ultah-pesulap.py [part ...]
parts: stage curtain valance cards wand star. Assets -> public/themes/art/ultah-pesulap/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m2_lib import *

OUT = outdir("ultah-pesulap")
PARTS = sys.argv[1:] or ["stage", "curtain", "valance", "cards", "wand", "star"]
NIGHT = "#1d1a45"
HAT, HAT_L, HAT_D = "#23202c", "#4a4560", "#121018"
BAND, BAND_D = "#c8324a", "#962238"
GOLD, GOLD_L, GOLD_D = "#eab54a", "#f8dc8a", "#b9842a"
VIOLET, VIOLET_L, VIOLET_D = "#7a2e98", "#9c4cb8", "#45145e"
WHITE, WHITE_S = "#fbf7f2", "#d9d2e4"
PINK = "#f2a3b5"
CARD_R, CARD_K = "#d23a44", "#24222c"


def gp(art, m, c1, c2=None, nx=None, rough=2.0, streak=0.6, pad=14):
    if callable(c2):
        c2, nx = None, c2
    return GP(art, m, c1, c2 or c1, seed=nx(), rough=rough, streak=streak, pad=pad)


def shade(art, m, col, nx, dens=0.5):
    return G(art, m, col, seed=nx(), density=dens, edge=0.2, bloom=0.2, rough=1.5, feather=2.0)


def star_pts(cx, cy, R, r, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        a = rot + i * math.pi / n
        rr = R if i % 2 == 0 else r
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def twinkle(cx, cy, R):
    """four-point twinkle (concave diamond)."""
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.tau / 16
        k = i % 4
        rr = R if k == 0 else (R * 0.18 if k == 2 else R * 0.3)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def paint_star(art, W, H, cx, cy, R, nx, rot=-math.pi / 2):
    sm = shapes(W, H, [star_pts(cx, cy, R, R * 0.46, rot=rot)], smooth=False)
    art = gp(art, sm, GOLD, GOLD_L, nx, rough=1.2)
    yy, xx = yy_xx(W, H)
    art = shade(art, sm * np.clip((xx - cx) / R + (yy - cy) / R, 0, 1), GOLD_D, nx, 0.5)
    hl = shapes(W, H, [star_pts(cx - R * 0.12, cy - R * 0.14, R * 0.42, R * 0.2, rot=rot)], smooth=False)
    art = soft(art, gaussian_filter(hl, 1.5), "#fff4c8", alpha=0.6, pad=6)
    return art


def paint_card(W, H, cx, cy, w, h, ang, suit, nx):
    """one playing card (white, rounded, plain pips in the corners + one big centre pip). Returns RGBA."""
    art = blank(W, H)
    ca, sa = math.cos(ang), math.sin(ang)
    def P(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    r = w * 0.09
    body = []
    for (qx, qy, a0) in ((w / 2 - r, -h / 2 + r, -math.pi / 2), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, math.pi / 2), (-w / 2 + r, -h / 2 + r, math.pi)):
        for t in np.linspace(0, math.pi / 2, 5):
            body.append(P(qx + math.cos(a0 + t) * r, qy + math.sin(a0 + t) * r))
    bm = shapes(W, H, [body], smooth=False)
    sh = np.roll(np.roll(bm, 6, 0), 4, 1)
    art = over(art, flat(gaussian_filter(sh, 4), "#000000", 0.25))
    art = gp(art, bm, WHITE, "#f1ece4", nx, rough=1.0, streak=0.3)
    art = G(art, np.clip(bm - shapes(W, H, [[P(x * 0.9, y * 0.93) for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]], smooth=False), 0, 1), "#c9bfd6", seed=nx(), density=0.6, edge=0.2, rough=0.8)
    col = CARD_R if suit in ("heart", "diamond") else CARD_K
    def pip(x, y, s, flip=False):
        if suit == "heart":
            pts = [(0, 0.35), (-0.5, -0.1), (-0.42, -0.42), (-0.15, -0.48), (0, -0.25), (0.15, -0.48), (0.42, -0.42), (0.5, -0.1)]
            sm = True
        elif suit == "diamond":
            pts = [(0, -0.5), (0.36, 0), (0, 0.5), (-0.36, 0)]; sm = False
        elif suit == "spade":
            pts = [(0, -0.5), (0.5, 0.05), (0.38, 0.32), (0.12, 0.3), (0.2, 0.5), (-0.2, 0.5), (-0.12, 0.3), (-0.38, 0.32), (-0.5, 0.05)]; sm = True
        else:  # club
            return None, [(x, y - s * 0.22, s * 0.24), (x - s * 0.24, y + s * 0.06, s * 0.24), (x + s * 0.24, y + s * 0.06, s * 0.24)], [(x - s * 0.08, y), (x + s * 0.08, y), (x + s * 0.16, y + s * 0.5), (x - s * 0.16, y + s * 0.5)]
        f = -1 if flip else 1
        return ([P(x + px * s, y + py * s * f) for px, py in pts], sm), None, None
    polys_s, polys_p, circ = [], [], []
    for (x, y, s, fl) in ((-w * 0.33, -h * 0.3, w * 0.2, False), (w * 0.33, h * 0.3, w * 0.2, True), (0, 0, w * 0.5, False)):
        a, c, stem = pip(x, y, s, fl)
        if a:
            (polys_s if a[1] else polys_p).append(a[0])
        else:
            circ += [(*P(cx_, cy_), rr) for cx_, cy_, rr in c]
            polys_p.append([P(px, py) for px, py in stem])
    pm = np.zeros((H, W), np.float32)
    if polys_s:
        pm = np.maximum(pm, shapes(W, H, polys_s))
    if polys_p:
        pm = np.maximum(pm, shapes(W, H, polys_p, smooth=False))
    if circ:
        pm = np.maximum(pm, circles(W, H, circ))
    art = gp(art, pm * bm, col, mix(col, "#000000", 0.15), nx, rough=0.8)
    return art


if "stage" in PARTS:
    W, H = 760, 720
    nx = Seq(71000)
    rng = random.Random(3)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    cx = 380
    # spotlight pool on the stage floor
    floor = ellipses(W, H, [(cx, 640, 330, 62, 0)])
    art = G(art, floor, "#5a3c8a", "#3a2a6a", seed=nx(), density=0.85, edge=0.4, bloom=0.4, rough=4)
    art = soft(art, ellipses(W, H, [(cx, 630, 230, 40, 0)]), "#f3d9ff", alpha=0.25, blur=14, pad=10)
    clear()
    # fanned cards on the floor, left
    for k, (dx, ang, suit) in enumerate(((-250, -0.5, "spade"), (-215, -0.25, "heart"), (-178, 0.0, "club"), (-140, 0.25, "diamond"))):
        card = paint_card(W, H, cx + dx, 560, 92, 132, ang, suit, nx)
        art = over(art, card)
        clear()
    # hat brim (back half), crown, band, brim front
    brim = ellipses(W, H, [(cx + 30, 598, 190, 40, -2)])
    art = gp(art, brim, HAT, HAT_D, nx, rough=1.4)
    crown = shapes(W, H, [[(cx + 30 - 128, 596), (cx + 30 - 112, 330), (cx + 30 + 112, 330), (cx + 30 + 128, 596)]], smooth=False)
    crown = np.maximum(crown, ellipses(W, H, [(cx + 30, 596, 128, 28, -2)]))
    art = gp(art, crown, HAT, "#2c2838", nx, rough=1.4)
    # side sheen (light from upper left) and shadow at right
    art = G(art, crown * np.clip(1 - np.abs(xx - (cx - 40)) / 26, 0, 1), HAT_L, seed=nx(), density=0.7, edge=0.2, bloom=0.2, rough=1.2, feather=3)
    art = G(art, crown * np.clip((xx - (cx + 90)) / 60, 0, 1), HAT_D, seed=nx(), density=0.6, edge=0.2, rough=1)
    band = crown * ((yy > 520) & (yy < 566)).astype(np.float32)
    band = np.maximum(band, ellipses(W, H, [(cx + 30, 566, 126, 22, -2)]) * (yy > 540) * crown)
    art = gp(art, band, BAND, BAND_D, nx, rough=1.0)
    art = G(art, band * np.clip(1 - np.abs(xx - (cx - 40)) / 22, 0, 1), "#f07a8a", seed=nx(), density=0.6, edge=0.2, rough=1, feather=2)
    # a gold star pinned on the band
    art = paint_star(art, W, H, cx + 100, 545, 20, nx)
    # top opening
    top = ellipses(W, H, [(cx + 30, 330, 112, 26, -2)])
    art = gp(art, top, "#0c0a10", "#16131c", nx, rough=1.0)
    clear()
    # the rabbit, peeking out: ears, head, cheeks, eyes, nose; clipped to above the front lip of the opening
    rx_, ry_ = cx + 22, 268
    ears = shapes(W, H, [deform(ellipse_pts(rx_ - 34, ry_ - 120, 22, 70, 14, rot=-0.22), random.Random(1), 1, 0.02),
                         deform(ellipse_pts(rx_ + 40, ry_ - 112, 22, 66, 14, rot=0.35), random.Random(2), 1, 0.02)])
    inner = shapes(W, H, [ellipse_pts(rx_ - 34, ry_ - 116, 10, 50, 12, rot=-0.22), ellipse_pts(rx_ + 40, ry_ - 108, 10, 46, 12, rot=0.35)])
    head = ellipses(W, H, [(rx_, ry_, 74, 64, 0)])
    front_lip = ellipses(W, H, [(cx + 30, 330, 112, 26, -2)]) * (yy > 330)
    hat_front = np.maximum(crown * (yy > 330), front_lip)
    rab = np.clip(np.maximum(ears, head) * (1 - hat_front) * ((yy < 336) | (top > 0.5)), 0, 1)
    rab = rab * (1 - (yy > 344))
    art = gp(art, rab, WHITE, "#f2eef4", nx, rough=1.2, streak=0.5)
    art = G(art, rab * np.clip((xx - rx_) / 70, 0, 1) * np.clip((yy - ry_ + 40) / 80, 0, 1), WHITE_S, seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=1.2, feather=3)
    art = gp(art, inner * rab, PINK, "#f7c0cc", nx, rough=0.8)
    # paws on the rim
    paws = ellipses(W, H, [(rx_ - 48, 336, 22, 13, 8), (rx_ + 52, 334, 22, 13, -8)])
    art = gp(art, paws, WHITE, "#efe9f1", nx, rough=1.0)
    art = G(art, strokes(W, H, [([(rx_ - 56 + k * 8, 330), (rx_ - 56 + k * 8, 340)], 1.6, None) for k in range(3)] + [([(rx_ + 44 + k * 8, 328), (rx_ + 44 + k * 8, 338)], 1.6, None) for k in range(3)]), "#b9b0c6", seed=nx(), density=0.7, edge=0.2, rough=0.5, feather=0.5)
    # face
    eyes = ellipses(W, H, [(rx_ - 26, ry_ - 6, 9, 11, 0), (rx_ + 26, ry_ - 6, 9, 11, 0)])
    art = gp(art, eyes, "#1d1a28", nx, rough=0.5)
    art = over(art, flat(circles(W, H, [(rx_ - 29, ry_ - 10, 3.4), (rx_ + 23, ry_ - 10, 3.4)]), "#ffffff", 0.95))
    cheeks = ellipses(W, H, [(rx_ - 44, ry_ + 16, 13, 8, 0), (rx_ + 44, ry_ + 16, 13, 8, 0)])
    art = G(art, cheeks, "#f29aae", seed=nx(), density=0.55, edge=0.1, bloom=0.3, rough=1, feather=3)
    nose = shapes(W, H, [[(rx_ - 8, ry_ + 10), (rx_ + 8, ry_ + 10), (rx_, ry_ + 19)]])
    art = gp(art, nose, "#e57a92", nx, rough=0.5)
    mouth = strokes(W, H, [(curve([(rx_ - 12, ry_ + 25), (rx_ - 5, ry_ + 30), (rx_, ry_ + 22)], 8), 2.4, None), (curve([(rx_, ry_ + 22), (rx_ + 5, ry_ + 30), (rx_ + 12, ry_ + 25)], 8), 2.4, None)])
    art = G(art, mouth, "#5a3a4a", seed=nx(), density=0.85, edge=0.2, rough=0.5, feather=0.4)
    # front lip of the opening (rim highlight)
    lip = np.clip(ellipses(W, H, [(cx + 30, 330, 114, 28, -2)]) - ellipses(W, H, [(cx + 30, 327, 108, 22, -2)]), 0, 1) * (yy > 322)
    art = gp(art, lip, HAT_L, HAT, nx, rough=0.6)
    brim_front = np.clip(brim * (yy > 596) - crown * 0, 0, 1)
    art = gp(art, brim_front * (1 - (crown * (yy < 600))), HAT, HAT_D, nx, rough=1.2)
    art = G(art, np.clip(ellipses(W, H, [(cx + 30, 600, 190, 40, -2)]) - ellipses(W, H, [(cx + 30, 596, 184, 34, -2)]), 0, 1) * (yy > 598), HAT_L, seed=nx(), density=0.6, edge=0.2, rough=1, feather=1)
    clear()
    # the wand, crossing above the hat to the right, with a big gold star at its tip
    wand = strokes(W, H, [([(cx + 160, 470), (cx + 300, 170)], 16, None)])
    art = gp(art, wand, "#1c1a22", nx, rough=0.8)
    tips = strokes(W, H, [([(cx + 160, 470), (cx + 175, 438)], 16, None), ([(cx + 286, 200), (cx + 300, 170)], 16, None)])
    art = gp(art, tips, WHITE, nx=nx, rough=0.6)
    art = G(art, strokes(W, H, [([(cx + 166, 462), (cx + 296, 178)], 3, None)]), "#6a6478", seed=nx(), density=0.6, edge=0.1, rough=0.4, feather=0.4)
    art = paint_star(art, W, H, cx + 312, 140, 54, nx, rot=-math.pi / 2 + 0.2)
    # a few painted twinkles and a curl of "magic" dots from the wand
    tw = shapes(W, H, [twinkle(x, y, r) for x, y, r in ((cx + 236, 92, 18), (cx + 372, 214, 14), (cx - 160, 210, 16), (cx - 220, 330, 11), (cx + 120, 120, 10))], smooth=False)
    art = gp(art, tw, GOLD_L, GOLD, nx, rough=0.6)
    dots = circles(W, H, [(cx + 300 - 46 * t * 6 + math.sin(t * 9) * 20, 140 + t * 150 - math.cos(t * 9) * 26, 4 + 3 * (1 - t)) for t in np.linspace(0.15, 1, 12)])
    art = gp(art, dots, "#f6e7ff", "#d8c0f4", nx, rough=0.5)
    clear()
    prev(art, "up-stage", bg=NIGHT)
    save(art, f"{OUT}/stage.webp", max_w=380, quality=86)

if "curtain" in PARTS:
    # left curtain panel, gathered by a gold tassel rope; folds as vertical gouache strokes
    W, H = 300, 2300
    nx = Seq(72000)
    yy, xx = yy_xx(W, H)
    gather_y = 1250
    def edge_x(y):
        # inner (right) edge: wide at top, pinched at the tie, flares below
        if y < gather_y:
            t = y / gather_y
            return 290 - 200 * t ** 1.6
        t = (y - gather_y) / (H - gather_y)
        return 90 + 120 * t ** 0.8
    pts = [(-10, -10), (300, -10)] + [(edge_x(y), y) for y in range(0, H + 1, 20)] + [(-10, H + 10)]
    m = shapes(W, H, [pts], smooth=False)
    art = blank(W, H)
    art = gp(art, m, VIOLET, VIOLET_D, nx, rough=1.5)
    # folds: stroke lines converging at the tie
    folds_l, folds_d = [], []
    for k in range(9):
        f = (k + 0.5) / 9
        top_x = f * 290
        line = []
        for y in range(0, H, 20):
            ex = edge_x(y)
            line.append((f * ex - 6 + 6 * math.sin(y / 90 + k), y))
        (folds_l if k % 2 else folds_d).append((line, 18 - abs(k - 4), None))
    art = G(art, strokes(W, H, folds_d) * m, VIOLET_D, seed=nx(), density=0.7, edge=0.2, bloom=0.2, rough=1.5, feather=6)
    art = G(art, strokes(W, H, folds_l) * m, VIOLET_L, seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=1.5, feather=6)
    # velvet sheen near the inner edge, dark at the outer
    inner_edge = np.zeros_like(m)
    for y in range(H):
        ex = int(edge_x(y))
        inner_edge[y, max(0, ex - 26):max(0, ex)] = 1
    art = G(art, gaussian_filter(inner_edge, 6) * m, "#c67ddf", seed=nx(), density=0.45, edge=0.1, rough=1, feather=2)
    art = G(art, m * np.clip(1 - xx / 70, 0, 1), "#2a0b3c", seed=nx(), density=0.5, edge=0.1, rough=1)
    # gold trim along the inner edge
    trim = strokes(W, H, [([(edge_x(y) - 4, y) for y in range(0, H, 10)], 8, None)])
    art = gp(art, trim, GOLD, GOLD_D, nx, rough=0.8)
    # tie rope + tassel
    rope = strokes(W, H, [(curve([(-10, gather_y - 18), (60, gather_y + 4), (edge_x(gather_y) + 8, gather_y - 6)], 20), 12, None)])
    art = gp(art, rope, GOLD, GOLD_L, nx, rough=0.8)
    art = G(art, strokes(W, H, [([(x, gather_y - 12 + (x % 14 > 7) * 4), (x + 6, gather_y + 2)], 2, None) for x in range(0, 110, 7)]), GOLD_D, seed=nx(), density=0.6, edge=0.1, rough=0.4, feather=0.4)
    tx = edge_x(gather_y) + 4
    knob = circles(W, H, [(tx, gather_y + 6, 14)])
    tassel = shapes(W, H, [[(tx - 10, gather_y + 14), (tx + 10, gather_y + 14), (tx + 22, gather_y + 96), (tx - 22, gather_y + 96)]])
    art = gp(art, np.maximum(knob, tassel), GOLD, GOLD_D, nx, rough=0.8)
    art = G(art, strokes(W, H, [([(tx + d, gather_y + 24), (tx + d * 1.8, gather_y + 94)], 1.8, None) for d in range(-9, 10, 3)]), GOLD_D, seed=nx(), density=0.7, edge=0.1, rough=0.4, feather=0.4)
    prev(art, "up-curtain", bg=NIGHT)
    save_full(art, f"{OUT}/curtain.webp", size=(150, 1150), quality=80)

if "valance" in PARTS:
    # seamless scalloped valance with gold fringe (period = 2 scallops)
    W, H = 400, 150
    nx = Seq(73000)
    yy, xx = yy_xx(W, H)
    sc = 200
    base = 70
    pts = [(-20, -10), (W + 20, -10)]
    for x in range(W + 20, -21, -5):
        t = ((x % sc) / sc)
        pts.append((x, base + 34 * math.sin(t * math.pi)))
    m = shapes(W, H, [pts], smooth=False)
    m = np.maximum(m, np.roll(m, 0, 1))
    art = blank(W, H)
    art = gp(art, m, VIOLET_D, VIOLET, nx, rough=1.2)
    # pleat shading per scallop
    pleat = m * (0.5 + 0.5 * np.cos((xx % sc) / sc * math.tau))
    art = G(art, pleat, "#2a0b3c", seed=nx(), density=0.45, edge=0.1, rough=1, feather=3)
    art = G(art, m * np.clip(1 - np.abs((xx % sc) - sc / 2) / 30, 0, 1), VIOLET_L, seed=nx(), density=0.45, edge=0.1, rough=1, feather=3)
    # gold trim + fringe following the scallop
    edge_pts = [(x, base + 34 * math.sin(((x % sc) / sc) * math.pi)) for x in range(-10, W + 11, 4)]
    trim = strokes(W, H, [(edge_pts, 9, None), ([(x, 14) for x in range(-10, W + 11, 10)], 7, None)])
    art = gp(art, trim, GOLD, GOLD_D, nx, rough=0.6)
    fr = strokes(W, H, [([(x, y + 3), (x + 1, y + 22)], 2.4, (0.0, 0.3)) for x, y in edge_pts[::1]])
    art = gp(art, fr, GOLD_L, GOLD, nx, rough=0.4)
    beads = circles(W, H, [(x, y + 26, 4) for x, y in edge_pts[::5]])
    art = gp(art, beads, GOLD, GOLD_D, nx, rough=0.4)
    prev(art, "up-valance", bg=NIGHT)
    save_full(art, f"{OUT}/valance.webp", size=(200, 75), quality=84)

if "cards" in PARTS:
    W, H = 420, 330
    nx = Seq(74000)
    art = blank(W, H)
    for k, (ang, suit) in enumerate(((-0.42, "spade"), (-0.14, "heart"), (0.14, "club"), (0.42, "diamond"))):
        a = ang
        cx = 210 + math.sin(a) * 120
        cy = 230 - math.cos(a) * 120 + 40
        art = over(art, paint_card(W, H, cx, cy, 120, 172, a, suit, nx))
        clear()
    prev(art, "up-cards", bg=NIGHT)
    save(art, f"{OUT}/cards.webp", max_w=210, quality=86)

if "wand" in PARTS:
    W, H = 420, 200
    nx = Seq(75000)
    art = blank(W, H)
    art = gp(art, strokes(W, H, [([(30, 150), (300, 92)], 14, None)]), "#1c1a22", nx=nx, rough=0.6)
    art = gp(art, strokes(W, H, [([(30, 150), (62, 143)], 14, None), ([(270, 98), (300, 92)], 14, None)]), WHITE, nx=nx, rough=0.5)
    art = paint_star(art, W, H, 340, 82, 46, nx, rot=-math.pi / 2 + 0.2)
    tw = shapes(W, H, [twinkle(x, y, r) for x, y, r in ((396, 150, 14), (262, 40, 12), (400, 28, 9))], smooth=False)
    art = gp(art, tw, GOLD_L, GOLD, nx, rough=0.5)
    prev(art, "up-wand", bg="#f5effa")
    save(art, f"{OUT}/wand.webp", max_w=180, quality=86)

if "star" in PARTS:
    W = H = 200
    nx = Seq(76000)
    art = paint_star(blank(W, H), W, H, 100, 104, 84, nx)
    prev(art, "up-star", bg=NIGHT)
    save(art, f"{OUT}/star.webp", max_w=96, quality=86)
