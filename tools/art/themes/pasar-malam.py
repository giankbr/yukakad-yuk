"""Pasar Malam — retro gouache poster of an Indonesian night fair: a painted night sky with a warm haze over the fair,
a big bianglala (ferris wheel) with coloured gondolas and bulbs, a komidi putar (carousel) with striped canopy and
wooden horses, a row of lapak stalls with striped awnings and lamps, a string of coloured festoon bulbs, and a gulali
(cotton candy) on a stick.
Run: python3 -I pasar-malam.py [part ...]   parts: langit bianglala komidi lapak lampu gulali
Assets -> public/themes/art/pasar-malam/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t4_lib import *  # noqa
from _p1_lib import ring_mask  # noqa

OUT = outdir("pasar-malam")
PARTS = sys.argv[1:] or ["langit", "bianglala", "komidi", "lapak", "lampu", "gulali"]
NIGHT, NIGHT_2 = "#0f2a36", "#173f4b"
CORAL, MUSTARD, MINT, PINK, CREAM, PLUM = "#e8553f", "#f2b632", "#6cc2a6", "#f39bb5", "#fbefd8", "#5b3a63"
BULB = "#ffd77a"


def bulbs(arr, W, H, pts, r, cols, nx, glow_r=10, glow_s=0.5):
    m = circles(W, H, [(x, y, r) for x, y in pts])
    arr = over(arr, glow(m, "#ffcf70", glow_r, glow_s))
    for i, c in enumerate(cols):
        sub = circles(W, H, [(x, y, r) for k, (x, y) in enumerate(pts) if k % len(cols) == i])
        arr = GP(arr, sub, c, mix(c, "#ffffff", 0.4), seed=nx(), rough=0.4, streak=0.3)
    arr = tint(arr, circles(W, H, [(x - r * 0.3, y - r * 0.3, r * 0.35) for x, y in pts]), "#ffffff", 0.7)
    return arr


def part_langit():
    W, H = 780, 1200
    rng = random.Random(3); nx = Seq(100)
    art = painted_sky(W, H, [(0, "#0b2230"), (0.35, NIGHT), (0.62, "#1d4752"), (0.78, "#7a4a52"), (0.9, "#d9744f"), (1, "#e8955a")], seed=4, streak=0.9)
    # warm haze of the fair lights low in the sky
    haze = gaussian_filter(ellipses(W, H, [(W * 0.5, H * 0.98, W * 0.7, H * 0.2, 0)]), 40)
    art = over(art, flat(haze, "#f3a560", 0.5))
    # stars: small gouache dabs, a few crosses
    st = [(rng.uniform(0, W), rng.uniform(0, H * 0.55), rng.uniform(0.8, 2.0)) for _ in range(140)]
    art = over(art, flat(circles(W, H, st), "#fff4d8", 0.8))
    crosses = []
    for _ in range(9):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, H * 0.45)
        s = rng.uniform(4, 8)
        crosses += [([(x - s, y), (x + s, y)], 1.6, (0.4, 0.4)), ([(x, y - s), (x, y + s)], 1.6, (0.4, 0.4))]
    art = over(art, flat(strokes(W, H, crosses), "#fff4d8", 0.85))
    # a big gouache moon, slightly off-round
    moon = shape_mask(W, H, deform(ellipse_pts(640, 150, 46, 46, 14), rng, 2, 0.02))
    art = over(art, glow(moon, "#fff1c8", 30, 0.35))
    art = GP(art, moon, "#fbeccb", "#f1d49a", seed=nx(), rough=1, streak=0.6)
    art = G(art, circles(W, H, [(626, 140, 9), (652, 168, 6), (660, 132, 5)]), "#d9bf8a", seed=nx(), density=0.4, edge=0.4, rough=1)
    # soft clouds lit from below
    cl = []
    for _ in range(5):
        x, y = rng.uniform(-40, W), rng.uniform(300, 640)
        for j in range(4):
            cl.append((x + j * rng.uniform(30, 44), y + rng.uniform(-5, 5), rng.uniform(40, 70), rng.uniform(6, 11), 0))
    art = over(art, flat(gaussian_filter(displace(ellipses(W, H, cl), nx(), 6, 14), 3), "#2b5a63", 0.55))
    art = add_grain(art, 7, 0.035)
    prev(art, "pasar-langit")
    save_rgb(art, f"{OUT}/langit.webp", quality=72)


def part_bianglala():
    W, H = 680, 760
    rng = random.Random(5); nx = Seq(300)
    art = blank(W, H)
    cx, cy, R = 340, 330, 270
    # A-frame legs
    legs = strokes(W, H, [([(cx, cy), (cx - 190, H - 20)], 18, None), ([(cx, cy), (cx + 190, H - 20)], 18, None),
                          ([(cx - 120, 560), (cx + 120, 560)], 8, None), ([(cx - 160, 680), (cx + 160, 680)], 8, None)])
    cross = strokes(W, H, [([(cx - 120, 560), (cx + 160, 680)], 4, None), ([(cx + 120, 560), (cx - 160, 680)], 4, None)])
    art = GP(art, np.maximum(legs, cross), "#c8d6cf", "#9fb4ad", seed=nx(), rough=0.8, streak=0.6)
    # rim: two circles + zigzag truss, spokes
    rim = np.maximum(ring_mask(W, H, cx, cy, R, 9), ring_mask(W, H, cx, cy, R - 26, 6))
    zz = []
    n = 48
    for i in range(n):
        a0 = i / n * math.tau; a1 = (i + 1) / n * math.tau
        r0, r1 = (R, R - 26) if i % 2 == 0 else (R - 26, R)
        zz.append(([(cx + math.cos(a0) * r0, cy + math.sin(a0) * r0), (cx + math.cos(a1) * r1, cy + math.sin(a1) * r1)], 3, None))
    spokes = [([(cx, cy), (cx + math.cos(i / 16 * math.tau) * (R - 26), cy + math.sin(i / 16 * math.tau) * (R - 26))], 4, None) for i in range(16)]
    frame = np.maximum(rim, strokes(W, H, zz + spokes))
    art = GP(art, frame, "#f6ead2", "#e8d4b0", seed=nx(), rough=0.7, streak=0.5)
    art = GP(art, ring_mask(W, H, cx, cy, R - 13, 4) * 0 + ring_mask(W, H, cx, cy, R + 1, 3), CORAL, seed=nx(), rough=0.4)
    # hub
    art = GP(art, circles(W, H, [(cx, cy, 34)]), CORAL, "#c23f2f", seed=nx(), rough=0.8)
    art = GP(art, circles(W, H, [(cx, cy, 16)]), MUSTARD, seed=nx(), rough=0.5)
    clear()
    # bulbs along the rim and spokes
    bpts = [(cx + math.cos(i / 48 * math.tau) * (R + 2), cy + math.sin(i / 48 * math.tau) * (R + 2)) for i in range(48)]
    bpts += [(cx + math.cos(i / 16 * math.tau) * rr, cy + math.sin(i / 16 * math.tau) * rr) for i in range(16) for rr in (110, 180)]
    art = bulbs(art, W, H, bpts, 4.2, [BULB, "#fff3c8", "#ff9b6a"], nx, glow_r=8, glow_s=0.45)
    clear()
    # gondolas hanging from 10 rim points
    cols = [CORAL, MUSTARD, MINT, PINK, "#4f8fc0"]
    for i in range(10):
        a = i / 10 * math.tau + 0.15
        px, py = cx + math.cos(a) * R, cy + math.sin(a) * R
        hang = strokes(W, H, [([(px, py), (px, py + 18)], 3, None)])
        art = GP(art, hang, "#2a3a40", seed=nx(), rough=0.3)
        gx, gy = px, py + 18
        roof = poly(W, H, [(gx - 26, gy + 10), (gx, gy - 2), (gx + 26, gy + 10)])
        cab = shapes(W, H, [[(gx - 22, gy + 10), (gx + 22, gy + 10), (gx + 20, gy + 40), (gx + 12, gy + 48), (gx - 12, gy + 48), (gx - 20, gy + 40)]])
        c = cols[i % len(cols)]
        art = over(art, soft_shadow(cab, "#000000", 3, 0.35, 2, 3))
        art = GP(art, cab, c, mix(c, "#000000", 0.18), seed=nx(), rough=0.8, streak=0.6)
        art = GP(art, roof, CREAM, seed=nx(), rough=0.6)
        win = rect(W, H, gx - 15, gy + 15, gx + 15, gy + 27)
        art = GP(art, win, "#ffe6a8", "#ffd27a", seed=nx(), rough=0.5)
        band = rect(W, H, gx - 21, gy + 33, gx + 21, gy + 36)
        art = tint(art, band, CREAM, 0.9)
        if i % 3 == 2:
            clear()
    art = add_grain(art, 9, 0.03)
    prev(art, "pasar-bianglala", bg=NIGHT)
    save(art, f"{OUT}/bianglala.webp", max_w=620, quality=80)


def horse(W, H, x, y, s, face=1):
    """Stylised wooden carousel horse (side view) mask: body, neck, head, legs mid-gallop, tail."""
    f = face
    P = lambda u, v: (x + u * s * f, y + v * s)
    body = ellipse_pts(*P(0, 0), s * 0.64, s * 0.34, 16)
    neck = [P(0.3, -0.2), P(0.5, -0.66), P(0.78, -0.74), P(0.7, -0.08)]
    head = [P(0.52, -0.78), P(0.8, -0.9), P(1.12, -0.7), P(1.16, -0.52), P(1.0, -0.46), P(0.7, -0.44)]
    ear = [P(0.6, -0.84), P(0.64, -1.0), P(0.72, -0.86)]
    shapes_ = None
    shapes_ = [body, neck, head, ear]
    legs = [
        ([P(0.4, 0.12), P(0.66, 0.34), P(0.74, 0.58)], s * 0.15, None),
        ([P(0.24, 0.2), P(0.3, 0.5), P(0.24, 0.74)], s * 0.15, None),
        ([P(-0.4, 0.14), P(-0.62, 0.38), P(-0.8, 0.52)], s * 0.15, None),
        ([P(-0.24, 0.22), P(-0.3, 0.5), P(-0.42, 0.72)], s * 0.15, None),
    ]
    tail = [([P(-0.58, -0.06), P(-0.86, 0.02), P(-1.0, 0.3)], s * 0.12, (0.1, 0.6))]
    mane = [([P(0.58, -0.6), P(0.45, -0.38), P(0.32, -0.2)], s * 0.12, (0.1, 0.5))]
    return shapes(W, H, shapes_), strokes(W, H, [(curve(p, 12), w, t) for p, w, t in legs]), strokes(W, H, [(curve(p, 12), w, t) for p, w, t in tail + mane])


def part_komidi():
    W, H = 520, 500
    rng = random.Random(7); nx = Seq(500)
    art = blank(W, H)
    cx = 260
    # platform (ellipse side) + base
    base = shapes(W, H, [ellipse_pts(cx, 430, 230, 34, 40)])
    art = over(art, soft_shadow(base, "#000000", 10, 0.5, 0, 10))
    art = GP(art, base, "#7a3f45", "#5b2c33", seed=nx(), rough=1)
    top_plat = shapes(W, H, [ellipse_pts(cx, 418, 228, 28, 40)])
    art = GP(art, top_plat, "#f2d9a8", "#e3c38a", seed=nx(), rough=0.8)
    skirt = np.clip(base - top_plat, 0, 1)
    # bulbs around the platform edge
    pts = [(cx + math.cos(t) * 228, 432 + math.sin(t) * 30) for t in np.linspace(0.05, math.pi - 0.05, 18)]
    # centre column with mirror panels
    col = rect(W, H, cx - 34, 150, cx + 34, 418)
    art = GP(art, col, "#3d6f6a", "#2f5a56", seed=nx(), rough=0.8)
    pan = shapes(W, H, [[(cx - 24, 170 + k * 62), (cx + 24, 170 + k * 62), (cx + 24, 214 + k * 62), (cx - 24, 214 + k * 62)] for k in range(4)], smooth=False)
    art = GP(art, pan, "#f6d58a", "#e8b65a", seed=nx(), rough=0.5)
    # brass poles + horses (front three)
    for (hx, hy, s, f, c) in ((110, 330, 74, 1, CREAM), (260, 350, 80, -1, "#f6b7a8"), (410, 330, 74, -1, "#cfe8dc")):
        pole = strokes(W, H, [([(hx, 150), (hx, 424)], 6, None)])
        art = GP(art, pole, "#e7c46a", "#b8913a", seed=nx(), rough=0.3)
        art = tint(art, strokes(W, H, [([(hx - 1.5, 150), (hx - 1.5, 424)], 1.5, None)]), "#fff3c4", 0.6)
        b, l, t = horse(W, H, hx, hy, s, f)
        allh = np.maximum(np.maximum(b, l), t)
        art = over(art, soft_shadow(allh, "#000000", 4, 0.35, 3, 4))
        art = GP(art, np.maximum(b, l), c, mix(c, "#000000", 0.12), seed=nx(), rough=0.7, streak=0.6)
        art = GP(art, t, MUSTARD, "#d9962a", seed=nx(), rough=0.6)
        saddle = shapes(W, H, [ellipse_pts(hx - 2 * f, hy - s * 0.24, s * 0.24, s * 0.12, 12)])
        art = GP(art, saddle * b, CORAL, seed=nx(), rough=0.4)
        eye = circles(W, H, [(hx + 0.95 * s * f, hy - 0.64 * s, 2.4)])
        art = tint(art, eye, "#2a1a1a", 0.9)
        clear()
    # canopy: striped cone with scalloped valance and a flag
    cone = poly(W, H, [(cx, 40), (cx + 250, 150), (cx - 250, 150)])
    stripes = []
    for k in range(-6, 7):
        if k % 2 == 0:
            stripes.append([(cx, 40), (cx + k * 42 + 21, 150), (cx + k * 42 - 21, 150)])
    sm = shapes(W, H, stripes, smooth=False) * cone
    art = over(art, soft_shadow(cone, "#000000", 6, 0.4, 0, 8))
    art = GP(art, cone, CREAM, "#ecd8b4", seed=nx(), rough=0.6)
    art = GP(art, sm, CORAL, "#cf4532", seed=nx(), rough=0.5)
    scal = circles(W, H, [(cx - 250 + 25 + k * 50, 152, 25) for k in range(10)]) * ygrad(W, H, 150, 151)
    band = rect(W, H, cx - 252, 140, cx + 252, 158)
    art = GP(art, np.maximum(band, scal), MUSTARD, "#e09a2a", seed=nx(), rough=0.6)
    art = bulbs(art, W, H, [(cx - 225 + k * 50, 150) for k in range(10)], 4.5, [BULB, "#fff3c8"], nx, glow_r=7, glow_s=0.4)
    art = bulbs(art, W, H, pts, 4, [BULB, "#ff9b6a", "#fff3c8"], nx, glow_r=6, glow_s=0.35)
    flagpole = strokes(W, H, [([(cx, 42), (cx, 8)], 3, None)])
    art = GP(art, flagpole, "#e7c46a", seed=nx(), rough=0.3)
    flag = poly(W, H, [(cx + 1, 8), (cx + 30, 15), (cx + 1, 24)])
    art = GP(art, flag, MINT, seed=nx(), rough=0.4)
    art = add_grain(art, 11, 0.03)
    prev(art, "pasar-komidi", bg=NIGHT)
    save(art, f"{OUT}/komidi.webp", max_w=440, quality=80)


def part_lapak():
    W, H = 780, 250
    rng = random.Random(9); nx = Seq(700)
    art = blank(W, H)
    x = -10
    cols = [(CORAL, CREAM), (MINT, CREAM), (MUSTARD, "#fff4dc"), (PINK, CREAM), ("#4f8fc0", CREAM)]
    i = 0
    while x < W:
        w = rng.uniform(140, 190)
        h = rng.uniform(110, 140)
        top = H - h
        body = rect(W, H, x + 6, top + 36, x + w - 6, H)
        art = GP(art, body, "#3a2a3e", "#2b1f30", seed=nx(), rough=1)
        # glowing counter opening
        op = rect(W, H, x + 16, top + 52, x + w - 16, top + 92)
        art = over(art, glow(op, "#ffb860", 12, 0.35))
        art = GP(art, op, "#ffd98a", "#f2a94e", seed=nx(), rough=0.6)
        # goods silhouettes on the counter: jars and hanging snacks
        goods = circles(W, H, [(x + 30 + k * 24, top + 84, 8) for k in range(int((w - 40) / 24))])
        art = GP(art, goods * op, "#c4562f", "#8f3a2a", seed=nx(), rough=0.4)
        hang = strokes(W, H, [([(x + 26 + k * 20, top + 52), (x + 26 + k * 20, top + 66)], 4, (0.0, 0.4)) for k in range(int((w - 36) / 20))])
        art = GP(art, hang * op, "#6b3a2a", seed=nx(), rough=0.3)
        # striped awning with scallops
        a0, a1 = top + 14, top + 44
        aw = poly(W, H, [(x, a1), (x + 8, a0), (x + w - 8, a0), (x + w, a1)])
        sc = circles(W, H, [(x + 10 + k * 20, a1, 10) for k in range(int(w / 20))]) * ygrad(W, H, a1, a1 + 1)
        awm = np.maximum(aw, sc)
        ca, cb = cols[i % len(cols)]
        art = over(art, soft_shadow(awm, "#000000", 4, 0.4, 0, 5))
        art = GP(art, awm, cb, seed=nx(), rough=0.6)
        st = shapes(W, H, [[(x + 8 + k * 20, a0), (x + 18 + k * 20, a0), (x + 20 + k * 20, a1 + 10), (x + 10 + k * 20, a1 + 10)] for k in range(int(w / 20)) if k % 2 == 0], smooth=False) * awm
        art = GP(art, st, ca, seed=nx(), rough=0.4)
        # a hanging lamp
        lx = x + w * 0.5
        art = GP(art, strokes(W, H, [([(lx, a1 + 6), (lx, a1 + 16)], 2, None)]), "#222222", seed=nx(), rough=0.2)
        lamp = circles(W, H, [(lx, a1 + 20, 6)])
        art = over(art, glow(lamp, "#ffd27a", 10, 0.6))
        art = GP(art, lamp, "#fff1c4", seed=nx(), rough=0.3)
        x += w - 4
        i += 1
        if i % 2 == 0:
            clear()
    art = add_grain(art, 13, 0.03)
    prev(art, "pasar-lapak", bg=NIGHT)
    save(art, f"{OUT}/lapak.webp", max_w=780, quality=78)


def part_lampu():
    W, H = 820, 150
    rng = random.Random(11); nx = Seq(900)
    art = blank(W, H)
    wires = []
    pts_all = []
    for seg in range(3):
        x0, x1 = -10 + seg * 280, 270 + seg * 280
        pts = [(x0 + (x1 - x0) * t, 22 + 70 * 4 * t * (1 - t)) for t in np.linspace(0, 1, 40)]
        wires.append((pts, 2.2, None))
        for t in np.linspace(0.08, 0.92, 6):
            pts_all.append((x0 + (x1 - x0) * t, 22 + 70 * 4 * t * (1 - t) + 10))
    art = GP(art, strokes(W, H, wires), "#1b1b22", seed=nx(), rough=0.3)
    caps = strokes(W, H, [([(x, y - 10), (x, y - 4)], 4, None) for x, y in pts_all])
    art = GP(art, caps, "#30303a", seed=nx(), rough=0.2)
    # pear-shaped bulbs
    bm_cols = [CORAL, MUSTARD, MINT, PINK, "#7fb2e0"]
    m_all = shapes(W, H, [deform(petal_pts(x, y - 4, 28, 11, math.pi / 2, n=12), rng, 1, 0.02) for x, y in pts_all])
    art = over(art, glow(m_all, "#ffd27a", 12, 0.55))
    for i, c in enumerate(bm_cols):
        sub = shapes(W, H, [deform(petal_pts(x, y - 4, 28, 11, math.pi / 2, n=12), random.Random(k), 1, 0.02) for k, (x, y) in enumerate(pts_all) if k % len(bm_cols) == i])
        art = GP(art, sub, mix(c, "#fff6d8", 0.35), c, seed=nx(), rough=0.4, streak=0.3)
    art = tint(art, circles(W, H, [(x - 3, y + 6, 3.4) for x, y in pts_all]), "#ffffff", 0.75)
    prev(art, "pasar-lampu", bg=NIGHT)
    save(art, f"{OUT}/lampu.webp", max_w=820, quality=80)


def part_gulali():
    W, H = 220, 340
    rng = random.Random(13); nx = Seq(1100)
    art = blank(W, H)
    stick = strokes(W, H, [([(110, 330), (110, 170)], 7, None)])
    art = GP(art, stick, "#f3e3c0", "#d9c497", seed=nx(), rough=0.3)
    puffs = []
    for _ in range(26):
        a = rng.uniform(0, math.tau); r = rng.uniform(0, 62)
        puffs.append((110 + math.cos(a) * r, 110 + math.sin(a) * r * 1.05, rng.uniform(26, 40)))
    cloud = displace(circles(W, H, puffs), nx(), 4, 10)
    art = GP(art, cloud, "#f7a8c3", "#f08bb0", seed=nx(), rough=1.5, streak=0.4)
    art = G(art, cloud * (1 - ygrad(W, H, 50, 130)) * xgrad(W, H, 180, 40), "#ffd9e6", seed=nx(), density=0.45, edge=0.2, bloom=0.5, rough=3)
    art = G(art, cloud * ygrad(W, H, 120, 180), "#d86a95", seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=3)
    wisps = [(curve([(110 + math.cos(a) * 40, 110 + math.sin(a) * 40), (110 + math.cos(a + 0.6) * 62, 110 + math.sin(a + 0.6) * 60)], 10), 1.4, (0.2, 0.5)) for a in np.linspace(0, math.tau, 14)]
    art = tint(art, strokes(W, H, wisps) * cloud, "#fff0f5", 0.5)
    prev(art, "pasar-gulali", bg=NIGHT)
    save(art, f"{OUT}/gulali.webp", max_w=160, quality=82)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
kb(OUT)
