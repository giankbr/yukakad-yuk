"""Sanaa Qamariya — old Sana'a at dusk: brown brick and basalt tower houses with white gypsum friezes, window frames and
crenellated parapets, every window crowned by a qamariya (gypsum-tracery fanlight of coloured glass) glowing from
inside; a large round qamariya emblem, a half-moon fanlight, a gypsum frieze band and a painted dusk sky with a
crescent. Architecture and geometry only: no figures, no calligraphy.
Run: python3 -I sanaa-qamariya.py [part ...]  parts: sky city qamariya fan frieze"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i3_lib import *

OUT = outdir("sanaa-qamariya")
PARTS = sys.argv[1:] or ["sky", "city", "qamariya", "fan", "frieze", "brick"]
GLASS = ["#e5483a", "#f2c23a", "#36a36a", "#3a78d6", "#ef8a34"]
GYP, GYP_S = "#f4ede1", "#b9a993"


def qamariya_masks(W, H, cx, cy, R, rot=0.0):
    """Round qamariya: glass groups as masks (by colour index) + the circle. Gypsum = circle minus glass."""
    groups = {i: [] for i in range(5)}
    for k in range(8):
        a = rot + k * math.tau / 8
        groups[k % 2].append(petal_pts(cx + math.cos(a) * R * 0.1, cy + math.sin(a) * R * 0.1, R * 0.4, R * 0.17, a, n=14))
    for k in range(16):
        a = rot + (k + 0.5) * math.tau / 16
        r0 = R * 0.56
        groups[2 if k % 2 else 3].append(petal_pts(cx + math.cos(a) * r0, cy + math.sin(a) * r0, R * 0.32, R * 0.115, a, n=12))
    for k in range(8):
        a = rot + k * math.tau / 8
        groups[0 if k % 2 else 1].append(ellipse_pts(cx + math.cos(a) * R * 0.58, cy + math.sin(a) * R * 0.58, R * 0.07, R * 0.07, 10))
    circ = []
    for k in range(28):
        a = rot + k * math.tau / 28
        circ.append(ellipse_pts(cx + math.cos(a) * R * 0.9, cy + math.sin(a) * R * 0.9, R * 0.062, R * 0.062, 10))
    groups[4] += circ
    center = ellipse_pts(cx, cy, R * 0.09, R * 0.09, 12)
    groups[3].append(center)
    masks = {i: shapes(W, H, p) for i, p in groups.items()}
    disc = circles(W, H, [(cx, cy, R)])
    return masks, disc


def paint_qamariya(art, W, H, cx, cy, R, nx, half=False, lit=0.5):
    masks, disc = qamariya_masks(W, H, cx, cy, R)
    if half:
        yy = np.mgrid[0:H, 0:W][0]
        cut = (yy <= cy).astype(np.float32)
        disc = disc * cut
        masks = {i: m * cut for i, m in masks.items()}
    glass_all = np.clip(sum(masks.values()), 0, 1)
    # glass first (lit), then gypsum lattice over the gaps
    for i, m in masks.items():
        art = OV(art, m, lambda mm, c=GLASS[i]: glass(mm, c, seed=nx(), lit=lit), pad=8)
    lattice = np.clip(disc - glass_all, 0, 1)
    art = OV(art, lattice, lambda mm: gypsum(mm, GYP, GYP_S, seed=nx(), depth=1.2), pad=8)
    edge = np.clip(glass_all - (gaussian_filter(glass_all, 1.8) > 0.92).astype(np.float32), 0, 1)
    art = over(art, flat(edge, "#4a3428", 0.45))
    rim = ring(W, H, cx, cy, R + R * 0.06, R * 0.12)
    if half:
        rim = rim * (np.mgrid[0:H, 0:W][0] <= cy)
    art = OV(art, rim, lambda mm: gypsum(mm, GYP, GYP_S, seed=nx(), depth=1.6), pad=8)
    return art, glass_all


if "sky" in PARTS:
    W, H = 420, 760
    nx = Seq(63100)
    sky = painted_sky(W, H, [(0, "#18204a"), (0.3, "#2c2f62"), (0.5, "#5a3f72"), (0.68, "#b8637a"), (0.84, "#ec9a66"), (1.0, "#f6c17e")], seed=nx(), streak=1.0, grain=0.8)
    # thin painted clouds catching the last light
    rng = random.Random(4)
    for (cx, cy, rx, ry, col) in [(110, 420, 160, 12, "#e98a7a"), (330, 470, 140, 10, "#f2a77c"), (220, 360, 120, 8, "#a86a8a")]:
        sky = G(sky, shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 10), rng, 3, 0.1)]), col, seed=nx(), density=0.35, edge=0.3, bloom=0.2)
    # crescent moon + one star (painted, soft)
    moon = np.clip(circles(W, H, [(318, 120, 22)]) - circles(W, H, [(328, 112, 20)]), 0, 1)
    sky = over(sky, glow(moon, "#fff2c8", 10, 0.35))
    sky = over(sky, gouache_paint(moon, "#fff4d6", "#f3dfa8", seed=nx(), rough=0.6))
    star = circles(W, H, [(270, 84, 2.2), (90, 140, 1.6), (150, 70, 1.3), (380, 210, 1.4)])
    sky = over(sky, glow(star, "#fff2c8", 3, 0.6))
    sky[..., 3] = 1
    save_rgb(sky, f"{OUT}/sky.webp", quality=76)
    prev(sky, "sanaa-sky")
    clear()


def tower(W, H, x, w, top, layer, rng, nx, acc):
    """Paint one tower house into acc dict of layer masks (body painted directly), returns art."""
    pass


if "city" in PARTS:
    W, H = 800, 760
    nx = Seq(63200)
    rng = random.Random(9)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lights = np.zeros((H, W), np.float32)
    towers = [
        # x, width, top, depth (0 back .. 1 front)
        (70, 130, 230, 0), (300, 120, 150, 0), (560, 140, 200, 0), (740, 120, 270, 0),
        (185, 160, 320, 1), (430, 176, 240, 1), (668, 160, 350, 1),
    ]
    for li, depth in enumerate((0, 1)):
        gyp_m = np.zeros((H, W), np.float32)
        glass_m = {i: np.zeros((H, W), np.float32) for i in range(5)}
        win_dark = np.zeros((H, W), np.float32)
        win_lit = np.zeros((H, W), np.float32)
        for (x, w, top, d) in towers:
            if d != depth:
                continue
            fl = 58 if depth else 46
            x0, x1 = x - w / 2, x + w / 2
            body = shapes(W, H, [[(x0 + 3, top), (x1 - 3, top), (x1, H + 4), (x0, H + 4)]], smooth=False)
            brick = ("#7c4e36", "#6a3f2b") if depth else ("#5a3e3a", "#4c3436")
            stone = ("#4a3a34", "#3a2c28") if depth else ("#3b2e30", "#30262a")
            art = GP(art, body, *brick, seed=nx(), rough=1.0, streak=1.2)
            split = top + (H - top) * 0.58
            art = GP(art, body * (yy > split), *stone, seed=nx(), rough=0.8, streak=1.0)
            # brick courses + stone blocks texture
            course = ((yy % 6) < 1.1).astype(np.float32) * body * (yy < split)
            art = over(art, flat(course, "#3e2418", 0.25 if depth else 0.18))
            blocks = (((yy % 16) < 1.4) | (((xx + ((yy // 16) % 2) * 14) % 28) < 1.4)).astype(np.float32) * body * (yy > split)
            art = over(art, flat(blocks, "#221816", 0.35))
            # dusk light: warm on left face edge, shadow right
            art = shade_side(art, body, "#1b1020", (1, 0), 0.45 if depth else 0.3, 26, nx())
            art = over(art, flat(body * np.clip(1 - (xx - x0) / 26, 0, 1), "#f0a060", 0.22 if depth else 0.1))
            # parapet: white crenellation steps + corner horns
            par = []
            for cx_ in np.arange(x0 + 8, x1 - 4, 14):
                par.append([(cx_ - 6, top + 2), (cx_ - 6, top - 6), (cx_ - 2, top - 6), (cx_ - 2, top - 12), (cx_ + 2, top - 12), (cx_ + 2, top - 6), (cx_ + 6, top - 6), (cx_ + 6, top + 2)])
            par.append([(x0 + 3, top - 2), (x0 + 3, top - 22), (x0 + 9, top - 14), (x0 + 9, top)])
            par.append([(x1 - 3, top - 2), (x1 - 3, top - 22), (x1 - 9, top - 14), (x1 - 9, top)])
            gyp_m = np.maximum(gyp_m, shapes(W, H, par, smooth=False))
            gyp_m = np.maximum(gyp_m, shapes(W, H, [[(x0 + 3, top + 2), (x1 - 3, top + 2), (x1 - 3, top + 7), (x0 + 3, top + 7)]], smooth=False))
            # floors: frieze lines, windows with gypsum frames, qamariya above
            nwin = max(2, int(w // (46 if depth else 40)))
            ww = 18 if depth else 14
            whh = 26 if depth else 20
            y = top + 30
            f = 0
            while y + whh + 20 < H:
                # frieze band every floor: zigzag + dots in gypsum
                zz = [(x0 + 4 + k * 6, y - 14 + (3 if k % 2 else -3)) for k in range(int((w - 8) / 6) + 1)]
                gyp_m = np.maximum(gyp_m, polyline_mask(W, H, [zz], 1.8 if depth else 1.3))
                gyp_m = np.maximum(gyp_m, polyline_mask(W, H, [[(x0 + 3, y - 20), (x1 - 3, y - 20)]], 2.0 if depth else 1.4, cap=False))
                if f % 2 == 0:
                    gyp_m = np.maximum(gyp_m, circles(W, H, [(x0 + 7 + k * 9, y - 8, 1.4 if depth else 1.0) for k in range(int((w - 10) / 9))]))
                if depth and f == 0:
                    rq = min(w * 0.2, 30)
                    qm, qd = qamariya_masks(W, H, x, y + 14, rq, rot=rng.uniform(0, 0.4))
                    allg = np.clip(sum(qm.values()), 0, 1)
                    for i in qm:
                        glass_m[i] = np.maximum(glass_m[i], qm[i])
                    gyp_m = np.maximum(gyp_m, np.clip(qd - allg, 0, 1))
                    gyp_m = np.maximum(gyp_m, ring(W, H, x, y + 14, rq + 4, 5))
                    y += fl
                    f += 1
                    continue
                for j in range(nwin):
                    wx = x0 + (j + 0.5) * (w / nwin) - ww / 2 + rng.uniform(-2, 2)
                    if y > split and rng.random() < 0.5:
                        continue  # fewer openings in the stone storeys
                    rect = [(wx, y + 8), (wx + ww, y + 8), (wx + ww, y + 8 + whh), (wx, y + 8 + whh)]
                    frame = [(wx - 3, y + 5), (wx + ww + 3, y + 5), (wx + ww + 3, y + 11 + whh), (wx - 3, y + 11 + whh)]
                    gyp_m = np.maximum(gyp_m, np.clip(shapes(W, H, [frame], smooth=False) - shapes(W, H, [rect], smooth=False), 0, 1))
                    lit = rng.random() < (0.45 if depth else 0.3)
                    if lit:
                        win_lit = np.maximum(win_lit, shapes(W, H, [rect], smooth=False))
                    else:
                        win_dark = np.maximum(win_dark, shapes(W, H, [rect], smooth=False))
                    # qamariya fanlight (half-moon) above the window
                    cxq, cyq, rq = wx + ww / 2, y + 5, ww / 2 + 3
                    half = circles(W, H, [(cxq, cyq, rq)]) * (yy <= cyq)
                    inner = circles(W, H, [(cxq, cyq, rq - 2.2)]) * (yy <= cyq - 1.2)
                    gyp_m = np.maximum(gyp_m, np.clip(half - inner, 0, 1))
                    # glass wedges (3 per fan) separated by gypsum spokes
                    for s_ in range(3):
                        a0 = math.pi + s_ * math.pi / 3 + 0.12; a1 = math.pi + (s_ + 1) * math.pi / 3 - 0.12
                        wedge = [(cxq, cyq - 0.5)] + arc_pts(cxq, cyq - 0.5, rq - 2.4, a0, a1, 8)
                        glass_m[(j + s_ + f) % 5] = np.maximum(glass_m[(j + s_ + f) % 5], shapes(W, H, [wedge], smooth=False))
                y += fl
                f += 1
        # media per layer
        art = OV(art, win_dark, lambda m: gouache_paint(m, "#24171c", "#1a1116", seed=nx(), rough=0.5), pad=6)
        art = OV(art, win_lit, lambda m: glass(m, "#d9782a", seed=nx(), glowc="#ffd58a", lit=0.55), pad=6)
        for i, m in glass_m.items():
            art = OV(art, m, lambda mm, c=GLASS[i]: glass(mm, c, seed=nx(), lit=0.9 if depth else 0.7), pad=6)
        gcol, gsh = (GYP, GYP_S) if depth else ("#cfc2c0", "#8f8188")
        art = OV(art, gyp_m, lambda m: gypsum(m, gcol, gsh, seed=nx(), depth=1.0), pad=6)
        lights = np.maximum(lights, np.clip(sum(glass_m.values()) + win_lit, 0, 1) * (1.0 if depth else 0.6))
        if depth == 0:
            # dusk haze between back and front rows
            haze = np.clip(art[..., 3], 0, 1) * np.clip((yy - 200) / 500, 0, 1)
            art = over(art, flat(haze, "#4a3a66", 0.25))
    art = add_grain(art, nx(), 0.03)
    prev(art, "sanaa-city", bg="#2c2f62")
    art = art[110:]
    lights = lights[110:]
    save_full(art, f"{OUT}/city.webp", size=(720, round((H - 110) * 720 / W)), quality=80)
    # separate glow layer (animated flicker in CSS)
    gl = glow(lights, "#ffc46a", 9, 0.55)
    save_full(gl, f"{OUT}/lights.webp", size=(360, round((H - 110) * 360 / W)), quality=70)
    clear()


if "qamariya" in PARTS:
    W = H = 440
    nx = Seq(63300)
    art = blank(W, H)
    halo = glow(circles(W, H, [(220, 220, 190)]), "#ffcf7a", 18, 0.35)
    art = over(art, halo)
    art, _ = paint_qamariya(art, W, H, 220, 220, 186, nx)
    prev(art, "sanaa-qamariya", bg="#2c2f62")
    save(art, f"{OUT}/qamariya.webp", max_w=360, quality=84)
    clear()


if "fan" in PARTS:
    W, H = 400, 230
    nx = Seq(63400)
    art = blank(W, H)
    art, _ = paint_qamariya(art, W, H, 200, 206, 176, nx, half=True)
    bar = shapes(W, H, [[(6, 204), (394, 204), (394, 226), (6, 226)]], smooth=False)
    art = OV(art, bar, lambda m: gypsum(m, GYP, GYP_S, seed=nx(), depth=1.4), pad=6)
    prev(art, "sanaa-fan", bg="#7c4e36")
    save(art, f"{OUT}/fan.webp", max_w=260, quality=84)
    clear()


if "frieze" in PARTS:
    # repeat-x band: brick ground with gypsum zigzag diamonds, dot rows and rails (period 24)
    W, H = 240, 48
    nx = Seq(63500)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = gouache_paint(np.ones((H, W), np.float32), "#7c4e36", "#6a3f2b", seed=nx(), rough=0.0, streak=1.2)
    art = over(art, flat(((yy % 6) < 1.1).astype(np.float32), "#3e2418", 0.25))
    zz1 = [(k * 6, 16 + (5 if k % 2 else -5)) for k in range(-2, W // 6 + 3)]
    zz2 = [(k * 6, 32 + (-5 if k % 2 else 5)) for k in range(-2, W // 6 + 3)]
    m = np.maximum(polyline_mask(W, H, [zz1, zz2], 2.2), polyline_mask(W, H, [[(0, 4), (W, 4)], [(0, 44), (W, 44)]], 3, cap=False))
    m = np.maximum(m, circles(W, H, [(k * 12 + 6, 24, 1.8) for k in range(-1, W // 12 + 1)]))
    art = over(art, gypsum(m, GYP, GYP_S, seed=nx(), depth=0.9))
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/frieze.webp", quality=82)
    prev(art, "sanaa-frieze")
    clear()


if "brick" in PARTS or "brick" in sys.argv[1:]:
    # seamless brick wall tile (courses of fired brick, lime mortar, tonal variation)
    W, H = 256, 256
    nx = Seq(63600)
    rng = random.Random(12)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = gouache_paint(np.ones((H, W), np.float32), "#76482f", "#5f3725", seed=nx(), rough=0.0, streak=1.4)
    bh, bw = 8, 32
    tone = np.zeros((H, W), np.float32)
    for r in range(H // bh):
        off = (bw // 2) * (r % 2)
        for c in range(-1, W // bw + 1):
            v = rng.uniform(-1, 1)
            x0 = c * bw + off
            tone[r * bh:(r + 1) * bh, max(0, x0):max(0, min(W, x0 + bw))] = v
    art[..., :3] *= (1 + tone[..., None] * 0.07)
    mortar = (((yy % bh) < 1.3) | ((((xx + (yy // bh % 2) * (bw // 2)) % bw) < 1.3))).astype(np.float32)
    art = over(art, flat(mortar, "#2e1a12", 0.45))
    art = add_grain(art, nx(), 0.05)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/brick.webp", quality=72)
    clear()
