"""Ladang Tulip — spring tulip fields in gouache: pale spring sky with soft cumulus, a tree line, a Dutch-style windmill
on the horizon (sails are a separate layer that turns), striped tulip rows (red, pink, yellow, white, violet) running
to the horizon with individual tulip heads in the foreground. Single tulip + small bunch for ornaments.
Run: python3 -I ladang-tulip.py [part ...]   parts: ladang wiek tulip buket"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g5_lib import *

OUT = outdir("ladang-tulip")
PARTS = sys.argv[1:] or ["ladang", "wiek", "tulip", "buket"]
SKY = "#cfe5f3"
LEAF, LEAF_D, LEAF_L = "#4f8a3c", "#356a2a", "#7fb25a"
TULIPS = [("#e0453a", "#b62a24"), ("#f08bb0", "#d4618c"), ("#f4c542", "#e09c22"), ("#fbf4ea", "#e6d8c4"), ("#9a6cc4", "#74479f"), ("#ef7a3a", "#cf5522")]


def tulip_paint(art, W, H, cx, cy, s, cols, nx, rng, ang=0.0):
    back, left, right = tulip_head(cx, cy, s, ang, rng)
    art = GP(art, shapes(W, H, [back]), cols[1], cols[1], seed=nx(), rough=0.8, streak=0.6, pad=6)
    art = GP(art, shapes(W, H, [left]), cols[0], cols[1], seed=nx(), rough=0.8, streak=0.8, pad=6)
    art = GP(art, shapes(W, H, [right]), cols[0], cols[0], seed=nx(), rough=0.8, streak=0.8, pad=6)
    hl = strokes(W, H, [([(cx - s * 0.18, cy - s * 0.55), (cx - s * 0.12, cy - s * 0.1)], max(1.0, s * 0.07), (0.3, 0.4))])
    art = GP(art, hl, "#ffffff", seed=nx(), rough=0.4, density=0.35, pad=4)
    return art


if "ladang" in PARTS:
    W, H = 780, 1180
    HY = 520                       # horizon
    VX = 300                       # vanishing point x
    rng = random.Random(71); nx = Seq(71000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, SKY), (0.3, "#d7eaf4"), (0.44, "#e8f1ee"), (1, "#eef3e6")], seed=71, streak=0.5, grain=0.8)
    # cumulus clouds: white gouache with blue-grey bellies
    for (cx, cy, sc) in [(140, 250, 1.0), (560, 170, 1.25), (690, 380, 0.7), (330, 420, 0.6)]:
        puffs = [deform(ellipse_pts(cx + dx * sc, cy + dy * sc, r * sc, r * sc * 0.8, 14), rng, 1, 0.05) for dx, dy, r in
                 [(-60, 10, 40), (-20, -14, 52), (30, -6, 46), (70, 14, 34), (0, 22, 44), (-100, 24, 26), (100, 26, 24)]]
        m = shapes(W, H, puffs)
        art = GP(art, m, "#fbfcfa", "#f1f5f4", seed=nx(), rough=2.6, streak=1.0)
        belly = m * np.clip((yy - (cy + 4 * sc)) / (34 * sc), 0, 1)
        art = G(art, belly, "#b9cbd8", seed=nx(), density=0.55, edge=0.2, bloom=0.4, rough=3, feather=2)
    # far tree line + farm on the horizon
    trees = []
    for x in range(-20, W + 20, 14):
        r = rng.uniform(10, 20)
        trees.append(deform(ellipse_pts(x, HY - r * 0.6 + rng.uniform(-3, 3), r, r * 0.9, 10), rng, 1, 0.08))
    tm = np.maximum(shapes(W, H, trees), poly_fill(W, H, [[(-10, HY - 8), (W + 10, HY - 8), (W + 10, HY + 4), (-10, HY + 4)]]))
    tm *= (np.abs(xx - 560) > 40) * 1.0 + (np.abs(xx - 560) <= 40) * (yy > HY - 10)
    art = GP(art, tm, "#7f9e78", "#6d8c6a", seed=nx(), rough=2.0, streak=0.6)
    # windmill tower (sails painted separately): tapered body, cap, gallery, door
    WX, WB, WT = 560, HY + 6, HY - 210
    body = poly_fill(W, H, [[(WX - 46, WB), (WX - 26, WT + 18), (WX + 26, WT + 18), (WX + 46, WB)]])
    art = GP(art, body, "#7a4a3a", "#5e3628", seed=nx(), rough=1.2, streak=1.0)
    art = G(art, body * (xx > WX + 6), "#3e2219", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1.5)
    cap = shapes(W, H, [[(WX - 34, WT + 22), (WX - 30, WT + 2), (WX, WT - 16), (WX + 30, WT + 2), (WX + 34, WT + 22)]])
    art = GP(art, cap, "#3f3a36", "#2d2926", seed=nx(), rough=1.0)
    gal = poly_fill(W, H, [[(WX - 62, WB - 92), (WX + 62, WB - 92), (WX + 62, WB - 84), (WX - 62, WB - 84)]])
    rails = strokes(W, H, [([(WX - 60 + k * 12, WB - 92), (WX - 60 + k * 12, WB - 106)], 1.4, None) for k in range(11)] + [([(WX - 62, WB - 106), (WX + 62, WB - 106)], 1.8, None)])
    art = GP(art, np.maximum(gal, rails), "#f4efe6", "#ddd4c6", seed=nx(), rough=0.6)
    door = poly_fill(W, H, [[(WX - 9, WB), (WX - 9, WB - 26), (WX + 9, WB - 26), (WX + 9, WB)]])
    win = poly_fill(W, H, [[(WX - 6, WB - 130), (WX - 6, WB - 144), (WX + 6, WB - 144), (WX + 6, WB - 130)]])
    art = GP(art, np.maximum(door, win), "#2b3b34", seed=nx(), rough=0.6)
    # tulip stripes: rays from the vanishing point, alternating colour bands and thin green rows
    field = (yy > HY).astype(np.float32)
    art = GP(art, field, LEAF, LEAF_D, seed=nx(), rough=1.0, streak=1.2)
    SW = 78.0                                        # stripe width at the bottom edge
    X0 = -5000.0
    angle_x = VX + (xx - VX) * (H - HY) / np.maximum(yy - HY, 1)   # project each pixel to the bottom edge
    u = (angle_x - X0) / SW
    idx = np.floor(u).astype(np.int64)
    frac = u - idx
    order = [0, 2, 1, 4, 3, 5, 0, 1, 2, 4, 0, 3, 1, 5, 2, 0, 4, 1, 2, 3, 0, 5]
    cidx = np.array(order)[idx % len(order)]
    depth = np.clip((yy - HY) / (H - HY), 0, 1)
    brk = fbm(W, H, 200, 5, 2)
    dens = np.clip(1.0 - depth * 1.05 + (brk - 0.5) * 0.7, 0, 1)
    inband = ((frac > 0.15) & (frac < 0.85)).astype(np.float32) * field * (dens > 0.32)
    for c, (ca, cb) in enumerate(TULIPS):
        band = inband * (cidx == c)
        if band.max() > 0:
            art = GP(art, band, ca, cb, seed=nx(), rough=1.0, streak=1.0)
        clear()
    # foreground tulip heads + leaves along the near stripes
    heads = []
    for i in range(int((-1400 - X0) / SW), int((W + 1400 - X0) / SW)):
        ca, cb = TULIPS[order[i % len(order)]]
        a0 = X0 + i * SW
        for k in range(34):
            t = rng.uniform(0.15, 0.85)
            y = HY + (H - HY) * (rng.uniform(0.26, 1.04) ** 0.85)
            ax = a0 + SW * t
            x = VX + (ax - VX) * (y - HY) / (H - HY)
            if -20 < x < W + 20:
                heads.append((y, x, (y - HY) / (H - HY), (ca, cb)))
    heads.sort()
    for y, x, d, cols in heads:
        s = 4 + 34 * d ** 1.5
        if s < 9:
            art = GP(art, circles(W, H, [(x, y, s * 0.42)]), cols[0], cols[1], seed=nx(), rough=0.4, pad=4)
            continue
        stem = strokes(W, H, [([(x, y), (x + rng.uniform(-2, 2), y + s * 1.6)], max(1.0, s * 0.12), None)])
        lv = shapes(W, H, [petal_pts(x + s * 0.1, y + s * 1.7, s * 1.3, s * 0.32, -math.pi / 2 + rng.uniform(-0.6, 0.6), n=10)])
        art = GP(art, np.maximum(stem, lv), LEAF_L, LEAF_D, seed=nx(), rough=0.6, pad=6)
        art = tulip_paint(art, W, H, x, y, s, cols, nx, rng, ang=rng.uniform(-0.15, 0.15))
    # haze on the horizon
    haze = np.clip(1 - np.abs(yy - HY) / 50, 0, 1) ** 2
    art = lighten(art, haze, "#eef3ee", 0.45)
    art[..., 3] = 1
    art = add_grain(art, 3, 0.02)
    preview(art, "lt-ladang", bg="#ffffff")
    save_rgb(art, f"{OUT}/ladang.webp", size=(620, 938), quality=76)
    clear()

if "wiek" in PARTS:
    # windmill sails: four lattice blades around a hub, cream canvas on dark frames
    W = H = 520
    nx = Seq(72000)
    art = blank(W, H)
    C = 260
    frames, canv, lat = [], [], []
    for k in range(4):
        a = k * math.pi / 2 + 0.3
        ca, sa = math.cos(a), math.sin(a)
        def P(u, v):
            return (C + ca * u - sa * v, C + sa * u + ca * v)
        frames.append(([P(10, 0), P(250, 0)], 7, None))
        canv.append([P(40, 4), P(246, 4), P(246, 50), P(40, 42)])
        for u in range(50, 250, 22):
            lat.append(([P(u, 2), P(u, 48 - (250 - u) * 0.02)], 2.0, None))
        lat.append(([P(40, 26), P(246, 28)], 1.6, None))
    cm = shapes(W, H, canv, smooth=False)
    art = GP(art, cm, "#f3ead8", "#e2d3b8", seed=nx(), rough=1.0, streak=1.2, density=0.9)
    art = GP(art, np.maximum(strokes(W, H, lat), strokes(W, H, frames)), "#4a3426", "#3a281c", seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, [(C, C, 16)]), "#3f3a36", seed=nx(), rough=0.6)
    preview(art, "lt-wiek", bg="#cfe5f3")
    save_full(art, f"{OUT}/wiek.webp", size=(260, 260), quality=84)
    clear()

if "tulip" in PARTS:
    W, H = 220, 420
    rng = random.Random(73); nx = Seq(73000)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(110, 120), (106, 260), (114, 400)], 30), 7, (0.0, 0.1))])
    lv1 = shapes(W, H, [[(112, 400), (60, 330), (40, 220), (70, 250), (100, 330)]])
    lv2 = shapes(W, H, [[(114, 400), (160, 300), (180, 200), (150, 240), (124, 330)]])
    art = GP(art, np.maximum(stem, np.maximum(lv1, lv2)), LEAF_L, LEAF_D, seed=nx(), rough=1.0, streak=1.0)
    art = G(art, lv1 * 0.8, LEAF_D, seed=nx(), density=0.35, edge=0.4, bloom=0.2, rough=1.5)
    art = tulip_paint(art, W, H, 110, 120, 110, TULIPS[0], nx, rng)
    preview(art, "lt-tulip")
    save(art, f"{OUT}/tulip.webp", max_w=110, quality=86)
    clear()

if "buket" in PARTS:
    # a loose row of tulips (closing / countdown foot)
    W, H = 900, 360
    rng = random.Random(74); nx = Seq(74000)
    art = blank(W, H)
    picks = [0, 1, 2, 4, 3, 1, 0, 5, 2, 1, 4, 0, 3, 2]
    xs = np.linspace(40, 860, len(picks))
    lv = []
    for i, x in enumerate(xs):
        top = 120 + rng.uniform(-40, 50)
        st = strokes(W, H, [(curve([(x, top), (x + rng.uniform(-10, 10), (top + H) / 2), (x + rng.uniform(-6, 6), H)], 20), 6, (0.0, 0.1))])
        lv.append([(x, H), (x - 50, H - 90), (x - 64, H - 170 + rng.uniform(-20, 20)), (x - 30, H - 110), (x - 4, H - 40)])
        art = GP(art, st, LEAF_L, LEAF_D, seed=nx(), rough=0.8, pad=8)
    art = GP(art, shapes(W, H, lv), LEAF, LEAF_D, seed=nx(), rough=1.2, streak=1.0)
    for i, x in enumerate(xs):
        top = 120 + random.Random(74 * 100 + i).uniform(-40, 50)
    rng2 = random.Random(74)
    for i, x in enumerate(xs):
        top = 120 + rng2.uniform(-40, 50)
        rng2.uniform(-10, 10); rng2.uniform(-6, 6); rng2.uniform(-20, 20)
        art = tulip_paint(art, W, H, x, top, 70 + (i % 3) * 8, TULIPS[picks[i]], nx, rng, ang=rng.uniform(-0.2, 0.2))
    art[..., 3] *= np.clip((H - np.mgrid[0:H, 0:W][0]) / 30, 0, 1) * 0 + 1
    preview(art, "lt-buket")
    save(art, f"{OUT}/buket.webp", max_w=620, quality=82)
    clear()
