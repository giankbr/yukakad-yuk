"""Pesta Kostum — cut-paper collage (gouache-painted paper, torn white edges, soft drop shadows): a rolling dress-up
rack with costumes on hangers (red cape, star robe, yellow tutu, cardboard knight tunic, a crown on a hook, paper masks
clipped on), three stylised kids in home-made costumes on a small wooden stage with a bunting skirt (original
characters), a paper crown, a cat-eared paper mask and a star wand.
Run: python3 -I pesta-kostum.py [part ...]   parts: rak anak mahkota topeng tongkat
Assets -> public/themes/art/pesta-kostum/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t4_lib import *  # noqa

OUT = outdir("pesta-kostum")
PARTS = sys.argv[1:] or ["rak", "anak", "mahkota", "topeng", "tongkat"]
TOMATO, SUN, TEAL, VIOLET, PINK, SKY = "#ef5b3f", "#ffc53a", "#1f9e9a", "#7a4fb5", "#ff8fb1", "#5aa9e6"
KRAFT, CREAM, INK = "#d9b48a", "#fff6e6", "#2d2440"
SKIN = ["#8a5a3c", "#c68e64", "#a9714c"]


def star_pts(cx, cy, r, k=5, inner=0.45, rot=-math.pi / 2):
    pts = []
    for i in range(k * 2):
        rr = r if i % 2 == 0 else r * inner
        a = rot + i / (k * 2) * math.tau
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def crown_pts(cx, by, w, h, k=5):
    pts = [(cx - w / 2, by)]
    for i in range(k * 2 + 1):
        x = cx - w / 2 + w * i / (k * 2)
        y = by - h if i % 2 == 0 else by - h * 0.45
        pts.append((x, y))
    pts.append((cx + w / 2, by))
    return pts


def hanger(W, H, x, y):
    hook = strokes(W, H, [(curve([(x, y + 26), (x, y + 12), (x + 8, y + 4), (x + 4, y - 4), (x - 4, y - 2)], 14), 3, None)])
    bar = strokes(W, H, [([(x - 46, y + 46), (x, y + 24), (x + 46, y + 46)], 5, None)])
    return np.maximum(hook, bar)


def part_rak():
    W, H = 820, 470
    rng = random.Random(3); nx = Seq(100)
    art = blank(W, H)
    # rack: two posts with feet + rail
    posts = strokes(W, H, [([(70, 40), (70, 430)], 12, None), ([(750, 40), (750, 430)], 12, None),
                           ([(30, 432), (110, 432)], 12, None), ([(710, 432), (790, 432)], 12, None)])
    rail = strokes(W, H, [([(60, 44), (760, 44)], 13, None)])
    art = PC(art, np.maximum(posts, rail), "#a8714a", "#8a5a38", seed=nx(), shadow=0.3)
    wheels = circles(W, H, [(36, 446, 11), (104, 446, 11), (716, 446, 11), (784, 446, 11)])
    art = PC(art, wheels, INK, seed=nx(), shadow=0.2)
    clear()
    xs = [150, 270, 400, 530, 650]
    for x in xs:
        art = PC(art, hanger(W, H, x, 34), "#c9a26a", seed=nx(), shadow=0.25, edge_w=1.2)
    # 1. red cape with yellow collar
    cape = shapes(W, H, [[(110, 82), (190, 82), (226, 330), (200, 322), (170, 334), (140, 322), (112, 334), (78, 326)]], smooth=False)
    art = PC(art, cape, TOMATO, "#d9452f", seed=nx())
    collar = shapes(W, H, [[(110, 80), (190, 80), (178, 112), (150, 98), (122, 112)]], smooth=False)
    art = PC(art, collar, SUN, seed=nx(), shadow=0.2)
    art = PC(art, shapes(W, H, [star_pts(150, 190, 26)], smooth=False), SUN, seed=nx(), shadow=0.15, edge_w=1.4)
    clear()
    # 2. violet star robe
    robe = shapes(W, H, [[(236, 80), (304, 80), (334, 120), (320, 132), (316, 360), (224, 360), (220, 132), (206, 120)]], smooth=False)
    art = PC(art, robe, VIOLET, "#6640a0", seed=nx())
    stars = shapes(W, H, [star_pts(x, y, r) for x, y, r in ((248, 170, 12), (292, 214, 15), (256, 280, 10), (298, 320, 11), (276, 128, 9))], smooth=False)
    art = PC(art, stars, SUN, seed=nx(), shadow=0.1, edge_w=1.0)
    sash = strokes(W, H, [([(222, 236), (318, 226)], 12, None)])
    art = PC(art, sash, TEAL, seed=nx(), shadow=0.15, edge_w=1.0)
    clear()
    # 3. yellow tutu dress
    bod = shapes(W, H, [[(372, 84), (428, 84), (432, 190), (368, 190)]], smooth=False)
    straps = strokes(W, H, [([(380, 80), (384, 66)], 5, None), ([(420, 80), (416, 66)], 5, None)])
    art = PC(art, np.maximum(bod, straps), PINK, "#f27ba0", seed=nx())
    tutu = []
    for k in range(9):
        a = math.pi * (0.06 + 0.88 * k / 8)
        tutu.append(deform(petal_pts(400, 186, 96, 34, a, n=12), rng, 1, 0.04))
    art = PC(art, shapes(W, H, tutu), SUN, "#ffd76a", seed=nx())
    art = PC(art, circles(W, H, [(400 + dx, 120 + dy, 6) for dx, dy in ((-14, 0), (14, 10), (0, 30), (-12, 52), (14, 60))]), CREAM, seed=nx(), shadow=0.1, edge_w=0.8)
    clear()
    # 4. cardboard knight tunic with a star shield emblem
    tun = shapes(W, H, [[(486, 82), (574, 82), (584, 116), (572, 120), (580, 330), (480, 330), (488, 120), (476, 116)]], smooth=False)
    art = PC(art, tun, "#b9c3cc", "#9aa6b2", seed=nx())
    shield = shapes(W, H, [[(504, 150), (556, 150), (556, 196), (530, 232), (504, 196)]], smooth=False)
    art = PC(art, shield, SKY, seed=nx(), shadow=0.2)
    art = PC(art, shapes(W, H, [star_pts(530, 186, 14)], smooth=False), CREAM, seed=nx(), shadow=0.1, edge_w=0.8)
    belt = strokes(W, H, [([(482, 268), (578, 268)], 12, None)])
    art = PC(art, belt, "#7a4a2a", seed=nx(), shadow=0.15, edge_w=1.0)
    clear()
    # 5. teal bear/onesie with hood ears
    ones = shapes(W, H, [[(612, 80), (688, 80), (700, 360), (662, 360), (650, 250), (638, 360), (600, 360)]], smooth=False)
    art = PC(art, ones, TEAL, "#178683", seed=nx())
    ears = circles(W, H, [(620, 80, 18), (680, 80, 18)])
    art = PC(art, ears, TEAL, seed=nx(), shadow=0.2)
    art = PC(art, circles(W, H, [(620, 80, 9), (680, 80, 9)]), PINK, seed=nx(), shadow=0.0, edge_w=0.6)
    belly = shapes(W, H, [ellipse_pts(650, 170, 26, 34, 16)])
    art = PC(art, belly, CREAM, seed=nx(), shadow=0.1, edge_w=0.8)
    clear()
    # paper masks pinned to the rail + a crown hanging on a hook at the end
    for (mx, my, c) in ((330, 60, SUN), (590, 62, PINK)):
        m = shapes(W, H, [ellipse_pts(mx - 18, my + 18, 22, 15, 14), ellipse_pts(mx + 18, my + 18, 22, 15, 14)])
        m = np.maximum(m, rect(W, H, mx - 10, my + 10, mx + 10, my + 24))
        holes = shapes(W, H, [ellipse_pts(mx - 17, my + 18, 8, 5.5, 12), ellipse_pts(mx + 17, my + 18, 8, 5.5, 12)])
        art = PC(art, np.clip(m - holes, 0, 1), c, seed=nx(), shadow=0.25)
        art = PC(art, rect(W, H, mx - 3, my - 10, mx + 3, my + 8), "#d0d6dc", seed=nx(), shadow=0.1, edge_w=0.6)
    hook = strokes(W, H, [(curve([(750, 50), (762, 70), (750, 86), (740, 80)], 10), 3, None)])
    art = PC(art, hook, "#9aa6b2", seed=nx(), shadow=0.1, edge_w=0.6)
    cr = shapes(W, H, [crown_pts(752, 136, 64, 46)], smooth=False)
    art = PC(art, cr, SUN, "#f2ad20", seed=nx())
    art = PC(art, circles(W, H, [(736, 124, 5), (752, 120, 5), (768, 124, 5)]), TOMATO, seed=nx(), shadow=0.0, edge_w=0.6)
    art = add_grain(art, 5, 0.03)
    prev(art, "kostum-rak", tone="#fdf3e1")
    save(art, f"{OUT}/rak.webp", max_w=780, quality=80)


def kid(art, W, H, x, by, s, skin, nx, rng, pose="cape"):
    """Stylised child (original): round head, simple features, body block, arms/legs as paper strips."""
    hx, hy = x, by - s * 1.55
    legs = strokes(W, H, [([(x - s * 0.16, by - s * 0.55), (x - s * 0.2, by - s * 0.05)], s * 0.16, None), ([(x + s * 0.16, by - s * 0.55), (x + s * 0.2, by - s * 0.05)], s * 0.16, None)])
    shoes = shapes(W, H, [ellipse_pts(x - s * 0.24, by, s * 0.16, s * 0.08, 12), ellipse_pts(x + s * 0.24, by, s * 0.16, s * 0.08, 12)])
    if pose == "cape":
        cape = shapes(W, H, [[(hx - s * 0.32, hy + s * 0.4), (hx + s * 0.32, hy + s * 0.4), (x + s * 0.72, by - s * 0.3), (x, by - s * 0.2), (x - s * 0.72, by - s * 0.3)]], smooth=False)
        art = PC(art, cape, TOMATO, "#d9452f", seed=nx())
        body_c, leg_c = SKY, INK
    elif pose == "tutu":
        body_c, leg_c = PINK, skin
    else:
        body_c, leg_c = "#b9c3cc", "#5a6b78"
    art = PC(art, legs, leg_c, seed=nx(), shadow=0.25)
    art = PC(art, shoes, INK if pose != "tutu" else TOMATO, seed=nx(), shadow=0.2)
    body = shapes(W, H, [[(x - s * 0.34, hy + s * 0.38), (x + s * 0.34, hy + s * 0.38), (x + s * 0.4, by - s * 0.5), (x - s * 0.4, by - s * 0.5)]], smooth=False)
    # arms: one raised (wand / wave), one down
    up = [(x + s * 0.3, hy + s * 0.5), (x + s * 0.62, hy + s * 0.2), (x + s * 0.72, hy - s * 0.15)]
    dn = [(x - s * 0.3, hy + s * 0.5), (x - s * 0.5, hy + s * 0.85), (x - s * 0.52, hy + s * 1.1)]
    arms = strokes(W, H, [(curve(up, 10), s * 0.15, None), (curve(dn, 10), s * 0.15, None)])
    art = PC(art, arms, body_c if pose != "tutu" else skin, seed=nx(), shadow=0.2)
    art = PC(art, circles(W, H, [(up[-1][0], up[-1][1], s * 0.1), (dn[-1][0], dn[-1][1], s * 0.1)]), skin, seed=nx(), shadow=0.1, edge_w=1.0)
    art = PC(art, body, body_c, mix(body_c, "#000000", 0.1), seed=nx())
    if pose == "tutu":
        tutu = [deform(petal_pts(x, by - s * 0.62, s * 0.7, s * 0.24, math.pi * (0.08 + 0.84 * k / 6), n=12), rng, 1, 0.04) for k in range(7)]
        art = PC(art, shapes(W, H, tutu), SUN, "#ffd76a", seed=nx())
    if pose == "knight":
        shield = shapes(W, H, [[(x - s * 0.62, hy + s * 0.6), (x - s * 0.18, hy + s * 0.6), (x - s * 0.18, hy + s * 1.05), (x - s * 0.4, hy + s * 1.3), (x - s * 0.62, hy + s * 1.05)]], smooth=False)
        art = PC(art, shield, KRAFT, "#c49a6a", seed=nx())
        art = PC(art, shapes(W, H, [star_pts(x - s * 0.4, hy + s * 0.92, s * 0.14)], smooth=False), TOMATO, seed=nx(), shadow=0.05, edge_w=0.8)
    if pose == "cape":
        art = PC(art, shapes(W, H, [star_pts(x, hy + s * 0.78, s * 0.16)], smooth=False), SUN, seed=nx(), shadow=0.05, edge_w=0.8)
    # neck + head
    head = shapes(W, H, [ellipse_pts(hx, hy, s * 0.36, s * 0.38, 20)])
    art = PC(art, head, skin, mix(skin, "#000000", 0.08), seed=nx())
    hair_c = "#2a1b14"
    if pose == "cape":
        hair = shapes(W, H, [[(hx - s * 0.37, hy - s * 0.02), (hx - s * 0.3, hy - s * 0.3), (hx, hy - s * 0.42), (hx + s * 0.3, hy - s * 0.3), (hx + s * 0.37, hy - s * 0.02), (hx + s * 0.2, hy - s * 0.18), (hx - s * 0.1, hy - s * 0.2)]])
        art = PC(art, hair, hair_c, seed=nx(), shadow=0.1, edge_w=1.0)
        art = PC(art, shapes(W, H, [crown_pts(hx, hy - s * 0.3, s * 0.56, s * 0.34)], smooth=False), SUN, "#f2ad20", seed=nx())
    elif pose == "tutu":
        hair = shapes(W, H, [ellipse_pts(hx, hy - s * 0.12, s * 0.42, s * 0.34, 18), ellipse_pts(hx - s * 0.42, hy + s * 0.1, s * 0.14, s * 0.2, 12), ellipse_pts(hx + s * 0.42, hy + s * 0.1, s * 0.14, s * 0.2, 12)])
        hair = np.clip(hair - shapes(W, H, [ellipse_pts(hx, hy + s * 0.08, s * 0.31, s * 0.3, 18)]), 0, 1)
        art = PC(art, hair, hair_c, seed=nx(), shadow=0.1, edge_w=1.0)
    else:
        helm = shapes(W, H, [[(hx - s * 0.4, hy - s * 0.02), (hx - s * 0.36, hy - s * 0.3), (hx, hy - s * 0.46), (hx + s * 0.36, hy - s * 0.3), (hx + s * 0.4, hy - s * 0.02)]])
        art = PC(art, helm, "#b9c3cc", "#9aa6b2", seed=nx(), shadow=0.15)
        plume = shapes(W, H, [deform(petal_pts(hx, hy - s * 0.44, s * 0.4, s * 0.14, -math.pi / 2 - 0.4, n=12), rng, 1, 0.05)])
        art = PC(art, plume, TOMATO, seed=nx(), shadow=0.1)
    # face: eyes, cheeks, smile; the tutu kid wears a cat-eared paper mask
    if pose == "tutu":
        mask = shapes(W, H, [ellipse_pts(hx - s * 0.13, hy, s * 0.17, s * 0.12, 14), ellipse_pts(hx + s * 0.13, hy, s * 0.17, s * 0.12, 14),
                             [(hx - s * 0.3, hy - s * 0.04), (hx - s * 0.24, hy - s * 0.3), (hx - s * 0.12, hy - s * 0.1)],
                             [(hx + s * 0.3, hy - s * 0.04), (hx + s * 0.24, hy - s * 0.3), (hx + s * 0.12, hy - s * 0.1)]])
        holes = shapes(W, H, [ellipse_pts(hx - s * 0.13, hy, s * 0.06, s * 0.045, 10), ellipse_pts(hx + s * 0.13, hy, s * 0.06, s * 0.045, 10)])
        art = PC(art, np.clip(mask - holes, 0, 1), VIOLET, seed=nx(), shadow=0.2, edge_w=1.2)
        art = tint(art, holes, INK, 0.9)
    else:
        art = tint(art, circles(W, H, [(hx - s * 0.13, hy + s * 0.02, s * 0.04), (hx + s * 0.13, hy + s * 0.02, s * 0.04)]), INK, 0.95)
    art = tint(art, gaussian_filter(circles(W, H, [(hx - s * 0.2, hy + s * 0.14, s * 0.07), (hx + s * 0.2, hy + s * 0.14, s * 0.07)]), 2), "#ff7a7a", 0.45)
    smile = strokes(W, H, [(arc_pts(hx, hy + s * 0.12, s * 0.1, 0.4, math.pi - 0.4, 10), s * 0.035, None)])
    art = tint(art, smile, INK, 0.9)
    return art, up[-1]


def part_anak():
    W, H = 780, 520
    rng = random.Random(7); nx = Seq(300)
    art = blank(W, H)
    # stage: plank top + bunting skirt
    top = shapes(W, H, [[(40, 400), (740, 400), (760, 428), (20, 428)]], smooth=False)
    front = rect(W, H, 24, 426, 756, 512)
    art = PC(art, front, "#a8714a", "#8a5a38", seed=nx())
    planks = strokes(W, H, [([(24, 426 + k * 22), (756, 426 + k * 22)], 2, None) for k in range(1, 4)])
    art = tint(art, planks * front, "#6b4228", 0.5)
    flags = []
    cols = [TOMATO, SUN, TEAL, PINK, VIOLET, SKY]
    for k in range(14):
        x0 = 30 + k * 52
        flags.append(([(x0, 432), (x0 + 50, 432), (x0 + 25, 476)], cols[k % len(cols)]))
    for c in cols:
        m = shapes(W, H, [p for p, cc in flags if cc == c], smooth=False)
        art = PC(art, m, c, seed=nx(), shadow=0.2, edge_w=1.2)
    art = PC(art, top, "#c98d5c", "#b47a4a", seed=nx())
    clear()
    art, hand = kid(art, W, H, 400, 402, 150, SKIN[0], nx, rng, "cape")
    # star wand in the raised hand
    wand = strokes(W, H, [([(hand[0] - 6, hand[1] + 14), (hand[0] + 16, hand[1] - 50)], 5, None)])
    art = PC(art, wand, "#f3e3c0", seed=nx(), shadow=0.2, edge_w=1.0)
    art = PC(art, shapes(W, H, [star_pts(hand[0] + 18, hand[1] - 60, 22)], smooth=False), SUN, "#f2ad20", seed=nx())
    clear()
    art, _ = kid(art, W, H, 190, 402, 118, SKIN[1], nx, rng, "tutu")
    clear()
    art, _ = kid(art, W, H, 600, 402, 124, SKIN[2], nx, rng, "knight")
    clear()
    # confetti
    conf = []
    while len(conf) < 40:
        x, y = rng.uniform(20, W - 20), rng.uniform(16, 360)
        if y > 110 and 100 < x < 720:
            continue
        if y > 40 and 330 < x < 480:
            continue
        a = rng.uniform(0, math.pi)
        conf.append(([(x, y), (x + math.cos(a) * 10, y + math.sin(a) * 10)], 5, None, rng.choice(cols)))
    for c in cols:
        m = strokes(W, H, [(p, w, t) for p, w, t, cc in conf if cc == c])
        art = PC(art, m, c, seed=nx(), shadow=0.1, edge_w=0.6)
    art = add_grain(art, 9, 0.03)
    prev(art, "kostum-anak", tone="#fdf3e1")
    save(art, f"{OUT}/anak.webp", max_w=760, quality=80)


def part_mahkota():
    W, H = 300, 200
    rng = random.Random(11); nx = Seq(600)
    art = blank(W, H)
    cr = shapes(W, H, [crown_pts(150, 170, 230, 140, 4)], smooth=False)
    art = PC(art, cr, SUN, "#f2ad20", seed=nx())
    band = rect(W, H, 36, 140, 264, 170)
    art = PC(art, band, TOMATO, seed=nx(), shadow=0.15)
    art = PC(art, circles(W, H, [(80, 155, 8), (150, 155, 10), (220, 155, 8)]), TEAL, seed=nx(), shadow=0.1, edge_w=1)
    art = PC(art, circles(W, H, [(35, 32, 9), (92, 32, 9), (150, 30, 10), (208, 32, 9), (265, 32, 9)]), PINK, seed=nx(), shadow=0.15, edge_w=1)
    prev(art, "kostum-mahkota", tone="#fdf3e1")
    save(art, f"{OUT}/mahkota.webp", max_w=240, quality=82)


def part_topeng():
    W, H = 300, 180
    rng = random.Random(13); nx = Seq(800)
    art = blank(W, H)
    cx, cy = 150, 100
    m = shapes(W, H, [ellipse_pts(cx - 52, cy, 64, 44, 18), ellipse_pts(cx + 52, cy, 64, 44, 18),
                      [(cx - 110, cy - 10), (cx - 92, cy - 82), (cx - 46, cy - 34)], [(cx + 110, cy - 10), (cx + 92, cy - 82), (cx + 46, cy - 34)]])
    holes = shapes(W, H, [ellipse_pts(cx - 48, cy + 2, 24, 15, 14), ellipse_pts(cx + 48, cy + 2, 24, 15, 14)])
    string = strokes(W, H, [(curve([(cx - 112, cy), (cx - 140, cy + 20), (cx - 146, cy + 60)], 10), 2.5, None), (curve([(cx + 112, cy), (cx + 140, cy + 20), (cx + 146, cy + 60)], 10), 2.5, None)])
    art = PC(art, string, TOMATO, seed=nx(), shadow=0.1, edge_w=0.6)
    art = PC(art, np.clip(m - holes, 0, 1), VIOLET, "#6640a0", seed=nx())
    inner_ear = shapes(W, H, [[(cx - 96, cy - 26), (cx - 90, cy - 66), (cx - 60, cy - 36)], [(cx + 96, cy - 26), (cx + 90, cy - 66), (cx + 60, cy - 36)]], smooth=False)
    art = PC(art, inner_ear, PINK, seed=nx(), shadow=0.0, edge_w=0.8)
    dots = circles(W, H, [(cx + dx, cy + dy, 4) for dx, dy in ((-90, 24), (-70, 36), (70, 36), (90, 24), (0, 22))])
    art = PC(art, dots, SUN, seed=nx(), shadow=0.0, edge_w=0.6)
    prev(art, "kostum-topeng", tone="#fdf3e1")
    save(art, f"{OUT}/topeng.webp", max_w=220, quality=82)


def part_tongkat():
    W, H = 160, 300
    rng = random.Random(17); nx = Seq(900)
    art = blank(W, H)
    stick = strokes(W, H, [([(80, 290), (80, 110)], 8, None)])
    art = PC(art, stick, "#f3e3c0", seed=nx(), shadow=0.2)
    rib = shapes(W, H, [deform(petal_pts(80, 112, 60, 14, math.pi / 2 + 0.5, n=12), rng, 1, 0.05), deform(petal_pts(80, 112, 54, 13, math.pi / 2 - 0.5, n=12), rng, 1, 0.05)])
    art = PC(art, rib, PINK, seed=nx(), shadow=0.15)
    art = PC(art, shapes(W, H, [star_pts(80, 70, 62)], smooth=False), SUN, "#f2ad20", seed=nx())
    prev(art, "kostum-tongkat", tone="#fdf3e1")
    save(art, f"{OUT}/tongkat.webp", max_w=110, quality=82)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
kb(OUT)
