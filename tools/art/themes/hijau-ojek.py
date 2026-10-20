"""Hijau Ojek — gouache city map (cover backdrop), gouache + ink ojek rider on a scooter (mascot, two sizes),
gouache product thumbnails (microwave, sofa, coffee machine).
Run: python3 -I /tmp/pen/art/themes/hijau-ojek.py [map|rider|products]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p4_lib import *  # noqa

T = "hijau-ojek"
D = outdir(T)
nxt = Seeds(500)
rng = random.Random(7)
INK = "#1f2a24"
GREEN, GREEN_D, GREEN_L = "#17a53a", "#0e7f2b", "#5fcf7a"


def gp(mask, c1, c2=None, rough=2.0, streak=0.5, density=0.97):
    return gouache_paint(mask, c1, c2, seed=nxt(), rough=rough, streak=streak, density=density)


# ---------- 1. painted city map ----------
def city_map():
    W, H = 640, 1180
    rng.seed(3)
    base = np.concatenate([paper_tile(W, "#dfe9d6", seed=5, mottle=1.2)[:H] if False else np.zeros((H, W, 3), np.float32), np.ones((H, W, 1), np.float32)], -1)
    pap = np.asarray(paper(W, H, "#e3ecda", seed=5, fiber=0.6, mottle=1.0), np.float32) / 255
    base[..., :3] = pap
    art = base
    # street grid: slightly irregular, two diagonals
    streets = np.zeros((H, W), np.float32)
    xs = [-10, 70, 150, 240, 330, 410, 500, 590, 660]
    ys = [-10, 90, 190, 300, 420, 540, 650, 760, 880, 990, 1100, 1200]
    for x in xs:
        pts = [(x + rng.uniform(-6, 6) + 14 * math.sin(y / 260), y) for y in np.linspace(-20, H + 20, 24)]
        streets = np.maximum(streets, stroke_mask(W, H, pts, rng.choice([14, 18, 22]), (0.02, 0.02)))
    for y in ys:
        pts = [(x, y + rng.uniform(-5, 5) + 10 * math.sin(x / 200)) for x in np.linspace(-20, W + 20, 24)]
        streets = np.maximum(streets, stroke_mask(W, H, pts, rng.choice([14, 18, 24]), (0.02, 0.02)))
    # a curved avenue + river
    ave = curve([(-20, 740), (180, 690), (330, 600), (470, 420), (660, 330)], 70)
    streets = np.maximum(streets, stroke_mask(W, H, ave, 30, (0.02, 0.02)))
    river = curve([(-20, 240), (120, 300), (260, 250), (420, 150), (560, 120), (680, 40)], 70)
    rm = stroke_mask(W, H, river, 44, (0.02, 0.02))
    # blocks = everything not street; paint block fills in cream / pale beige with hand variations
    blocks = np.clip(1 - gaussian_filter(streets, 1.2) * 1.5, 0, 1)
    art = over(art, pigment(blocks, "#eef0e4", "#e6e9d9", seed=nxt(), density=0.55, edge=0.15, bloom=0.2, gran=0.3, feather=1.0, rough=2, mottle=0.5))
    # parks: green watercolour blobs on some blocks
    parks = np.zeros((H, W), np.float32)
    for (x, y, rx, ry) in [(200, 150, 70, 48), (560, 560, 60, 70), (90, 600, 54, 60), (420, 880, 80, 60), (250, 1040, 60, 46), (300, 470, 48, 40), (600, 960, 50, 80)]:
        parks = np.maximum(parks, shape_mask(W, H, deform(ellipse_pts(x, y, rx, ry, 10), rng, 2, .12)))
    parks = parks * blocks
    art = glaze(art, pigment(parks, "#9ccf8e", "#6fb86a", seed=nxt(), density=0.7, edge=0.45, bloom=0.5, gran=0.3, feather=1.2, rough=5, mottle=0.6))
    # trees: small round gouache dabs with darker half
    tree = np.zeros((H, W), np.float32); tree_sh = np.zeros((H, W), np.float32)
    pts_t = []
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if parks[int(min(H - 1, y)), int(min(W - 1, x))] > 0.5 or rng.random() < 0.12:
            r = rng.uniform(5, 9)
            pts_t.append((x, y, r))
    tree = dots_mask(W, H, pts_t)
    tree_sh = dots_mask(W, H, [(x + r * .3, y + r * .3, r * .7) for x, y, r in pts_t])
    art = over(art, gp(tree, "#3f9b4f", "#4faa5a", rough=1.0, density=0.95))
    art = over(art, gp(tree_sh * tree, "#2d7f3d", "#2f8a40", rough=0.6, density=0.75))
    # river
    art = over(art, pigment(rm, "#a9d3e6", "#8dc2dc", seed=nxt(), density=0.8, edge=0.5, bloom=0.4, gran=0.3, feather=1.5, rough=4, mottle=0.5))
    # streets: cream with soft ink edges
    art = over(art, gp(streets, "#fbfbf3", "#f4f3e8", rough=1.2, streak=0.3, density=0.98))
    edge = outline(np.clip(gaussian_filter(streets, 0.6), 0, 1), 2.2)
    art = over(art, pigment(edge, "#b8c2b2", "#a7b3a3", seed=nxt(), density=0.6, edge=0.1, bloom=0, gran=0.2, feather=0.5, rough=1.2, holes=0.2))
    # buildings: small gouache rectangles with coloured roofs scattered on blocks (not on parks/streets)
    bld = np.zeros((H, W), np.float32); roofs = {}
    roof_cols = ["#e07b55", "#d9a441", "#c96a5a", "#8fb0c7", "#d58b6e"]
    rl = {c: np.zeros((H, W), np.float32) for c in roof_cols}
    for _ in range(230):
        x, y = rng.uniform(10, W - 10), rng.uniform(10, H - 10)
        ok = blocks[int(y), int(x)] > 0.9 and parks[int(y), int(x)] < 0.2 and rm[int(y), int(x)] < 0.1
        if not ok:
            continue
        w_, h_ = rng.uniform(14, 26), rng.uniform(12, 22)
        bm = shape_mask(W, H, wobble_rect(x - w_ / 2, y - h_ / 2, w_, h_, rng, 1.0), smooth=False)
        if np.sum(bm * np.clip(gaussian_filter(bld, 2) * 3, 0, 1)) > 2:
            continue
        bld = np.maximum(bld, bm)
        col = rng.choice(roof_cols)
        rl[col] = np.maximum(rl[col], shape_mask(W, H, [(x - w_ / 2 - 1, y - h_ / 2 + h_ * .45), (x, y - h_ / 2 - 3), (x + w_ / 2 + 1, y - h_ / 2 + h_ * .45)], smooth=False))
    art = over(art, gp(bld, "#f3ead9", "#ead9c0", rough=0.8, density=0.96))
    for c, m in rl.items():
        art = over(art, gp(m, c, mix(c, "#000000", .12), rough=0.6, density=0.95))
    art = over(art, inked(bld, "#5d5a4e", seed=nxt(), width=1.6, density=0.5, wobble=0.6))
    # a few landmark pins painted (green) and a faint compass rose top-right
    comp = ring_mask(W, H, W - 70, 70, 26, 2.0, rng, 0.6)
    for a in range(4):
        ang = a * math.pi / 2
        comp = np.maximum(comp, shape_mask(W, H, [(W - 70 + math.cos(ang) * 38, 70 + math.sin(ang) * 38), (W - 70 + math.cos(ang + 1.2) * 8, 70 + math.sin(ang + 1.2) * 8), (W - 70 + math.cos(ang - 1.2) * 8, 70 + math.sin(ang - 1.2) * 8)], smooth=False))
    art = over(art, pigment(comp, "#5a7a5e", seed=nxt(), density=0.55, edge=0.2, bloom=0, feather=0.5, rough=1))
    art[..., 3] = 1
    save_rgb(art, f"{D}/map.webp", q=78)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/ho-map.png")


# ---------- 2. ojek rider on a scooter (gouache + ink) ----------
def rider_art(W=560, H=420, box=True, jacket=(GREEN, GREEN_D), helm=("#19a63f", "#128a33"), gift=False, scooter=("#ececdf", "#dcd9c8")):
    rng.seed(9)
    art = blank(W, H)
    gy = 330   # ground line
    # wheels
    rw, fw = (130, gy - 50), (420, gy - 50)
    R = 50
    tyre = union(shape_mask(W, H, deform(ellipse_pts(*rw, R, R, 24), rng, 1, .01)), shape_mask(W, H, deform(ellipse_pts(*fw, R, R, 24), rng, 1, .01)))
    rim = union(shape_mask(W, H, ellipse_pts(*rw, R * .55, R * .55, 20)), shape_mask(W, H, ellipse_pts(*fw, R * .55, R * .55, 20)))
    hub = union(shape_mask(W, H, ellipse_pts(*rw, R * .18, R * .18, 12)), shape_mask(W, H, ellipse_pts(*fw, R * .18, R * .18, 12)))
    # scooter body: floorboard + rear body + leg shield + front fork + handlebar
    body = shape_mask(W, H, deform([(95, 250), (120, 212), (190, 206), (236, 236), (262, 262), (330, 262), (352, 236), (372, 172), (392, 154), (404, 160), (386, 200), (370, 266), (372, 288), (330, 296), (120, 296), (92, 278)], rng, 2, .012))
    seat = shape_mask(W, H, deform([(104, 214), (120, 190), (176, 182), (236, 190), (240, 206), (190, 212), (116, 220)], rng, 2, .02))
    fork = stroke_mask(W, H, [(392, 158), (424, 276)], 9, (0.05, 0.05))
    bars = stroke_mask(W, H, [(352, 150), (382, 142), (410, 146)], 8, (0.1, 0.1))
    mirror = union(stroke_mask(W, H, [(386, 142), (396, 104)], 3, (0.1, 0.1)), shape_mask(W, H, ellipse_pts(398, 98, 9, 7, 12, 0.3)))
    lamp = shape_mask(W, H, ellipse_pts(402, 176, 11, 13, 14))
    fender = shape_mask(W, H, deform(arc_pts(fw[0], fw[1], R + 14, math.pi * 1.1, math.pi * 1.95, 20) + arc_pts(fw[0], fw[1], R + 3, math.pi * 1.95, math.pi * 1.1, 20), rng, 1, .01))
    # rider: legs, torso, arms, helmet
    leg = shape_mask(W, H, deform([(212, 206), (236, 196), (268, 236), (292, 266), (300, 290), (280, 296), (256, 262), (224, 232)], rng, 2, .02))
    shoe = shape_mask(W, H, deform([(274, 282), (312, 282), (318, 296), (272, 298)], rng, 1, .03))
    torso = shape_mask(W, H, deform([(160, 206), (164, 150), (182, 108), (214, 92), (246, 100), (262, 136), (266, 176), (248, 206)], rng, 2, .015))
    arm = shape_mask(W, H, deform([(236, 120), (254, 110), (330, 142), (360, 148), (356, 162), (322, 160), (248, 140)], rng, 2, .02))
    glove = shape_mask(W, H, ellipse_pts(358, 152, 11, 9, 12))
    neck = shape_mask(W, H, [(200, 100), (236, 100), (236, 116), (200, 116)])
    helmet = shape_mask(W, H, deform(ellipse_pts(222, 72, 40, 36, 24), rng, 1, .012))
    helmet = np.maximum(helmet, shape_mask(W, H, [(186, 72), (258, 72), (254, 94), (196, 96)]))
    visor = shape_mask(W, H, deform([(224, 62), (262, 64), (266, 84), (252, 96), (226, 94)], rng, 1, .02))
    stripe = stroke_mask(W, H, arc_pts(222, 74, 30, math.pi * 1.15, math.pi * 1.75, 16), 5, (0.15, 0.15)) * helmet
    # top box (green) behind the rider on the rear rack
    topbox = shape_mask(W, H, deform([(60, 212), (64, 162), (140, 156), (146, 210)], rng, 2, .015))
    box_lid = shape_mask(W, H, [(56, 170), (146, 164), (146, 176), (58, 182)])
    heart = shape_mask(W, H, [(103, 200), (84, 184), (86, 172), (96, 170), (103, 178), (110, 170), (120, 172), (122, 184)])
    # paint order: back to front
    L = lambda m, c1, c2=None, r=2.0: gp(m, c1, c2, rough=r)
    if gift:   # big red gift box with ribbon + heart on the rear rack
        topbox = shape_mask(W, H, deform([(26, 214), (30, 110), (150, 104), (156, 212)], rng, 2, .012))
        box_lid = shape_mask(W, H, deform([(18, 122), (160, 114), (160, 134), (20, 142)], rng, 1, .02))
        ribbon = union(stroke_mask(W, H, [(88, 118), (92, 212)], 12, (0.02, 0.02)) * topbox, stroke_mask(W, H, [(28, 170), (154, 166)], 11, (0.02, 0.02)) * topbox)
        bow = union(shape_mask(W, H, petal_pts(90, 110, 30, 12, math.pi * 1.15, 10)), shape_mask(W, H, petal_pts(90, 110, 30, 12, -math.pi * 0.15, 10)), shape_mask(W, H, ellipse_pts(90, 110, 7, 7, 10)))
        heart = shape_mask(W, H, [(118, 198), (104, 186), (106, 176), (114, 174), (118, 180), (122, 174), (130, 176), (132, 186)])
        art = over(art, L(topbox, "#d9452f", "#c23a26"))
        art = over(art, shade(L(topbox, "#d9452f", "#c23a26"), topbox, light=(-0.6, -0.7), k=0.18, blur=10, hi="#ff9a86", lo="#7a2316"))
        art = over(art, L(box_lid, "#e4523a", "#d9452f", 1.2))
        art = over(art, L(ribbon, "#fbf5e6", "#efe6d2", 0.8))
        art = over(art, L(bow, "#fbf5e6", "#efe6d2", 0.8))
        art = over(art, L(heart, "#fdfdf5", "#f1e7e5", 1.0))
        box = True
    elif box:
        art = over(art, L(topbox, "#13923a", "#0f7a30"))
        art = over(art, L(box_lid, "#1aa844", "#13923a", 1.2))
        art = over(art, L(heart, "#fdfdf5", "#eef4e8", 1.0))
    art = over(art, L(tyre, "#2b2f33", "#3a3f44", 1.5))
    art = over(art, L(rim, "#c9ccc8", "#b3b7b2", 1.0))
    art = over(art, L(hub, "#6e7378", None, 0.6))
    art = over(art, L(fender, "#e8e4d6", "#d9d4c4", 1.5))
    art = over(art, L(body, *scooter, 2.5))
    art = over(art, shade(L(body, *scooter, 2.5), body, light=(-0.5, -0.8), k=0.18, blur=10, hi="#ffffff", lo=mix(scooter[1], "#000000", .4)))
    art = over(art, L(seat, "#2f3336", "#3d4246", 1.5))
    art = over(art, L(fork, "#9a9ea0", "#7c8083", 0.8))
    art = over(art, L(bars, "#4a4e52", None, 0.8))
    art = over(art, L(mirror, "#4a4e52", None, 0.6))
    art = over(art, L(lamp, "#ffe08a", "#f6c75a", 0.8))
    art = over(art, L(leg, "#2e3b52", "#26324a", 1.5))
    art = over(art, L(shoe, "#3a2d26", "#4a3a30", 1.0))
    art = over(art, L(torso, *jacket, 2.0))
    art = over(art, shade(L(torso, *jacket, 2.0), torso, light=(-0.6, -0.8), k=0.2, blur=8, hi=mix(jacket[0], "#ffffff", .45), lo=mix(jacket[1], "#000000", .4)))
    art = over(art, L(neck, "#e6b58c", "#d9a47b", 0.8))
    art = over(art, L(arm, *jacket, 1.5))
    art = over(art, L(glove, "#2b2f33", None, 0.8))
    art = over(art, L(helmet, *helm, 1.5))
    art = over(art, shade(L(helmet, *helm, 1.5), helmet, light=(-0.6, -0.8), k=0.25, blur=6, hi=mix(helm[0], "#ffffff", .5), lo=mix(helm[1], "#000000", .45)))
    art = over(art, L(stripe, "#f7fbf4", None, 0.6))
    art = over(art, L(visor, "#2a3c5a", "#1d2b44", 1.0))
    art = over(art, shade(L(visor, "#2a3c5a", "#1d2b44", 1.0), visor, light=(-0.7, -0.7), k=0.35, blur=4, hi="#9bb7d8", lo="#101a2c"))
    # ink outlines over everything
    all_m = union(tyre, body, seat, fork, bars, mirror, lamp, leg, shoe, torso, arm, glove, helmet, visor, fender, *(([topbox, box_lid]) if box else []))
    parts = [tyre, body, seat, leg, torso, arm, helmet, visor, fender, shoe] + ([topbox, box_lid, heart] if box else [])
    ink_m = np.zeros((H, W), np.float32)
    for pm in parts:
        ink_m = np.maximum(ink_m, outline(pm, 2.6))
    ink_m = np.maximum(ink_m, outline(all_m, 3.4))
    art = over(art, pigment(ink_m * (0.6 + 0.4 * fbm(W, H, nxt(), 30, 2)), INK, mix(INK, "#000000", .3), seed=nxt(), density=0.8, edge=0.1, bloom=0, gran=0.2, feather=0.4, rough=0.9, mottle=0.2, holes=0.08))
    # spokes hint + motion lines (ink)
    sp = np.zeros((H, W), np.float32)
    for (cx, cy) in (rw, fw):
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            sp = np.maximum(sp, stroke_mask(W, H, [(cx + math.cos(a) * R * .2, cy + math.sin(a) * R * .2), (cx + math.cos(a) * R * .5, cy + math.sin(a) * R * .5)], 2.0, (0.1, 0.1)))
    art = over(art, pigment(sp, "#7a7e80", seed=nxt(), density=0.6, edge=0, bloom=0, feather=0.4, rough=0.6))
    # ground shadow
    sh = gaussian_filter(shape_mask(W, H, ellipse_pts(275, gy + 2, 210, 12, 20)), 6)
    art = over(pigment(sh, "#6b7d6b", seed=nxt(), density=0.3, edge=0, bloom=0.3, feather=4, rough=6), art)
    return art


def rider():
    art = rider_art()
    preview(art, f"{PREV}/ho-rider.png", "#dcebd4")
    save(art, f"{D}/rider.webp", max_w=440, q=82)


# ---------- 3. product thumbnails ----------
def products():
    S = 220
    rng.seed(17)
    out = {}
    # microwave
    art = blank(S, S)
    body = shape_mask(S, S, wobble_rect(30, 60, 160, 100, rng, 2.0))
    door = shape_mask(S, S, wobble_rect(44, 74, 96, 72, rng, 1.5))
    win = shape_mask(S, S, wobble_rect(54, 84, 76, 52, rng, 1.0))
    panel = shape_mask(S, S, wobble_rect(150, 74, 28, 72, rng, 1.0))
    knobs = dots_mask(S, S, [(164, 92, 6), (164, 112, 6), (164, 132, 4)])
    feet = union(shape_mask(S, S, [(40, 160), (56, 160), (56, 168), (40, 168)]), shape_mask(S, S, [(164, 160), (180, 160), (180, 168), (164, 168)]))
    art = over(art, gp(feet, "#4a4a4a"))
    art = over(art, gp(body, "#e9e5dc", "#d8d3c6", rough=1.5))
    art = over(art, gp(door, "#d94f2b", "#c4431f", rough=1.2))
    art = over(art, gp(win, "#3b3f46", "#2d3137", rough=1.0))
    art = over(art, gp(shape_mask(S, S, [(60, 90), (120, 90), (112, 100), (60, 100)]), "#5a6068", rough=0.6, density=0.6))
    art = over(art, gp(panel, "#f5f1e8", rough=0.8))
    art = over(art, gp(knobs, "#6a6a6a", rough=0.5))
    ink_m = union(outline(body, 2.8), outline(door, 2.2), outline(win, 2.0), outline(panel, 1.8))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    out["microwave"] = art
    # sofa
    art = blank(S, S)
    back = shape_mask(S, S, deform([(36, 70), (184, 70), (186, 130), (34, 130)], rng, 2, .015))
    seatc = shape_mask(S, S, deform([(28, 118), (192, 118), (196, 150), (24, 150)], rng, 2, .015))
    armL = shape_mask(S, S, deform(ellipse_pts(34, 134, 16, 22, 14), rng, 1, .02))
    armR = shape_mask(S, S, deform(ellipse_pts(186, 134, 16, 22, 14), rng, 1, .02))
    cushion = union(shape_mask(S, S, wobble_rect(48, 84, 56, 40, rng, 2.0)), shape_mask(S, S, wobble_rect(116, 84, 56, 40, rng, 2.0)))
    legs = union(shape_mask(S, S, [(44, 150), (54, 150), (52, 168), (46, 168)]), shape_mask(S, S, [(166, 150), (176, 150), (174, 168), (168, 168)]))
    art = over(art, gp(legs, "#6b4a2e", rough=0.8))
    art = over(art, gp(back, "#3f7fd4", "#3671bf", rough=1.5))
    art = over(art, gp(cushion, "#5a96e6", "#4b86d6", rough=1.5))
    art = over(art, gp(seatc, "#3f7fd4", "#346cb8", rough=1.5))
    art = over(art, gp(armL, "#4a8be0", "#3f7fd4", rough=1.2))
    art = over(art, gp(armR, "#4a8be0", "#3f7fd4", rough=1.2))
    ink_m = union(outline(union(back, seatc, armL, armR), 2.8), outline(cushion, 2.0), outline(seatc, 1.8))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    out["sofa"] = art
    # coffee machine
    art = blank(S, S)
    base_ = shape_mask(S, S, wobble_rect(50, 150, 120, 22, rng, 1.5))
    tower = shape_mask(S, S, wobble_rect(66, 44, 88, 110, rng, 2.0))
    head = shape_mask(S, S, wobble_rect(58, 44, 104, 34, rng, 1.5))
    spout = shape_mask(S, S, [(102, 78), (118, 78), (116, 96), (104, 96)])
    cup = shape_mask(S, S, deform([(90, 112), (130, 112), (126, 146), (94, 146)], rng, 1, .02))
    handle = sub(shape_mask(S, S, ellipse_pts(132, 128, 12, 11, 14)), shape_mask(S, S, ellipse_pts(132, 128, 6, 6, 12)))
    knob = dots_mask(S, S, [(78, 60, 7), (142, 60, 7)])
    steam = union(stroke_mask(S, S, curve([(104, 104), (100, 96), (106, 88), (102, 80)], 20), 2.2), stroke_mask(S, S, curve([(118, 104), (122, 96), (116, 88), (120, 82)], 20), 2.2))
    art = over(art, gp(base_, "#2e3135", "#3a3e43", rough=1.0))
    art = over(art, gp(tower, "#1f7a3a", "#176430", rough=1.5))
    art = over(art, gp(head, "#2e3135", "#3a3e43", rough=1.2))
    art = over(art, gp(spout, "#c0c4c8", rough=0.6))
    art = over(art, gp(knob, "#d7a94a", rough=0.5))
    art = over(art, gp(cup, "#f7f3ea", "#ebe5d8", rough=1.0))
    art = over(art, gp(handle, "#f7f3ea", rough=0.6))
    art = over(art, gp(shape_mask(S, S, [(94, 112), (126, 112), (124, 120), (96, 120)]), "#6b3f22", rough=0.6, density=0.8))
    ink_m = union(outline(union(base_, tower, head), 2.8), outline(cup, 2.0), outline(handle, 1.6), outline(spout, 1.5))
    art = over(art, pigment(ink_m, INK, seed=nxt(), density=0.75, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.1))
    art = over(art, pigment(steam, "#7a8a80", seed=nxt(), density=0.45, edge=0, bloom=0, feather=0.6, rough=0.6))
    out["coffee"] = art
    sheet = Image.new("RGB", (S * 3, S), "#f6f7f8")
    for i, (k, a) in enumerate(out.items()):
        save(a, f"{D}/p-{k}.webp", max_w=150, q=84, trim=False)
        sheet.paste(to_image(a), (i * S, 0), to_image(a))
    sheet.save(f"{PREV}/ho-products.png")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["map", "rider", "products"]:
        {"map": city_map, "rider": rider, "products": products}[w]()
