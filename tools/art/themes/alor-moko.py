"""Alor Moko — a cast-bronze moko drum (hourglass body, relief bands of spirals and tumpal triangles, loop handles,
starred tympanum, verdigris patina), the moko tympanum seen from above as a medallion, a watercolour view of a clear
turquoise bay between steep green islands, and an Alor warp-ikat band (indigo ground, rust and undyed lozenges and
hooks with feathered edges). Original, inspired-by drawings; no copied artefacts.
Run: python3 -I alor-moko.py [part ...]   parts: moko tympanum bay ikat divider
Assets -> public/themes/art/alor-moko/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h3_lib import *  # noqa

OUT = outdir("alor-moko")
PARTS = sys.argv[1:] or ["moko", "tympanum", "bay", "ikat", "divider"]
BRONZE, BR_D, BR_H, PATINA = "#a06c34", "#38220f", "#f0c486", "#4f9a86"
INDIGO, RUST, UNDYED, MADDER = "#1c2440", "#a8462a", "#efe2c6", "#6e2a24"
SAND = "#f4ecdf"


def moko_hw(y):
    """Half-width profile of the drum (canvas 600x940)."""
    ys = np.array([40, 70, 120, 250, 330, 400, 470, 560, 680, 800, 870], np.float32)
    ws = np.array([194, 204, 210, 208, 188, 158, 144, 146, 172, 206, 214], np.float32)
    return np.interp(y, ys, ws)


if "moko" in PARTS:
    W, H = 600, 960
    cx = 300
    nx = Seq(71000); rng = random.Random(710)
    top, bot = 70, 870
    RY = 34  # perspective of the round rims
    # silhouette: profile + bottom arc + top ellipse
    left = [(cx - float(moko_hw(y)), y) for y in range(top, bot + 1, 10)]
    right = [(cx + float(moko_hw(y)), y) for y in range(bot, top - 1, -10)]
    botarc = [(cx + math.cos(a) * moko_hw(bot), bot + math.sin(a) * RY * 0.9) for a in np.linspace(math.pi, 0, 30)][::-1]
    body = shapes(W, H, [left + [(cx - moko_hw(bot), bot)] + [(cx + math.cos(a) * moko_hw(bot), bot + math.sin(a) * RY) for a in np.linspace(math.pi, 0, 30)] + right], smooth=False)
    topell = ellipses(W, H, [(cx, top, moko_hw(top), RY, 0)])
    body = np.clip(body + topell, 0, 1)
    # handles: loop ears on both sides of the shoulder
    ears = []
    for sgn in (-1, 1):
        x0 = cx + sgn * moko_hw(300)
        ears.append((curve([(x0 - sgn * 6, 258), (x0 + sgn * 34, 266), (x0 + sgn * 46, 312), (x0 + sgn * 32, 356), (x0 - sgn * 10, 366)], 30), 22, None))
    earm = strokes(W, H, ears)
    earhole = strokes(W, H, [(curve([(cx + s * moko_hw(300) + s * 8, 286), (cx + s * moko_hw(300) + s * 22, 312), (cx + s * moko_hw(300) + s * 10, 338)], 16), 6, None) for s in (-1, 1)])
    earm = np.clip(earm - earhole, 0, 1)
    # shadow on the ground
    sh = ellipses(W, H, [(cx + 30, bot + 26, 250, 30, 0)])
    art = OV(blank(W, H), sh, lambda m: col_arr(m, "#2b2a22", gaussian_filter(m, 14) * 0.38), pad=40)
    light, n = cyl_light(W, H, cx, moko_hw, lit=-0.55, amb=0.12)
    light = np.clip((light - 0.45) / 0.55, 0, 1) ** 1.4
    # concave waist reads darker under the shoulder, rim lighter
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    light = light * (1 - 0.18 * np.exp(-((yy - 420) / 60) ** 2))
    allm = np.clip(body + earm, 0, 1)
    art = over(art, bronze_body(W, H, allm, light, nx, BRONZE, BR_D, BR_H, PATINA, patina_amt=0.34, seed=711))
    clear()

    # relief bands: drawn in (theta, y) space, projected onto the cylinder
    def P(theta, y):
        hw = float(moko_hw(y))
        return (cx + math.sin(theta) * hw, y + math.cos(theta) * RY * (0.9 if y < 450 else 0.7))

    rid, motif = [], []
    for y in (108, 150, 236, 268, 520, 556, 742, 780, 836):
        rid.append(([P(t, y) for t in np.linspace(-1.5, 1.5, 60)], 4.2, None))
    # spiral row (double spirals) between 108-150 and 742-780
    for yb, cnt in ((129, 13), (761, 13)):
        for k in range(cnt):
            t = -1.4 + 2.8 * k / (cnt - 1)
            for side in (-1, 1):
                pts = spiral_pts(0, 0, 9, 1.5, 0 if side > 0 else math.pi, 1.4, 22, side)
                proj = [P(t + (px + side * 10) / moko_hw(yb), yb + py) for px, py in pts]
                motif.append((proj, 3.0, None))
    # tumpal triangles between 268 and 520 (upward) on the mantle, and between 556 and 742 (downward) on the foot
    tri = []
    for (y0, y1, cnt, up) in ((280, 330, 15, True), (560, 616, 15, False)):
        for k in range(cnt):
            t = -1.45 + 2.9 * k / (cnt - 1)
            dt = 1.2 / cnt
            if up:
                poly = [P(t - dt, y1), P(t, y0), P(t + dt, y1)]
            else:
                poly = [P(t - dt, y0), P(t, y1), P(t + dt, y0)]
            tri.append(poly)
    # zigzag + dot rows on the waist
    zig = [P(t, 470 + (10 if i % 2 else -10)) for i, t in enumerate(np.linspace(-1.45, 1.45, 34))]
    rid.append((zig, 3.2, None))
    dots = [(lambda p: (p[0], p[1], 4.2))(P(t, 650)) for t in np.linspace(-1.4, 1.4, 22)]
    # mantle panel: plain cartouches with a four-petal flower
    flowers = []
    for t in (-0.95, 0, 0.95):
        fx, fy = P(t, 195)
        sx = math.cos(t)
        for a in range(4):
            ang = a * math.pi / 2 + math.pi / 4
            flowers.append(petal_pts(fx, fy, 22, 10, ang, 10))
            flowers[-1] = [(fx + (px - fx) * sx, py) for px, py in flowers[-1]]
    vis = np.clip(1 - np.abs(n) ** 6, 0, 1) * body
    rel = np.clip(strokes(W, H, rid + motif) + shapes(W, H, tri, smooth=False) * 0.95 + circles(W, H, dots) + shapes(W, H, flowers), 0, 1) * vis
    art = shade(art, rel, 1.12)
    art = relief(art, rel, nx, light="#ffdcaa", dark="#24140a", d=2, hi_amt=0.55, lo_amt=0.6)
    clear()
    # tympanum (top ellipse): lighter cast face with rings and a star
    tm = topell
    art = GP(art, tm, "#b98446", "#8c5a2a", seed=nx(), rough=1.0, streak=0.6, pad=8)
    rings = []
    for r in (0.92, 0.66, 0.4):
        rings.append(([(cx + math.cos(a) * moko_hw(top) * r, top + math.sin(a) * RY * r) for a in np.linspace(0, math.tau, 80)], 2.4, None))
    star = []
    for k in range(10):
        a = k * math.tau / 10
        star.append([(cx, top), (cx + math.cos(a - 0.12) * 30, top + math.sin(a - 0.12) * 5), (cx + math.cos(a) * 74, top + math.sin(a) * 12.5), (cx + math.cos(a + 0.12) * 30, top + math.sin(a + 0.12) * 5)])
    trel = np.clip(strokes(W, H, rings) + shapes(W, H, star, smooth=False), 0, 1) * tm
    art = relief(art, trel, nx, light="#ffe2b4", dark="#3a220e", d=1, hi_amt=0.6, lo_amt=0.5)
    art = G(art, tm * np.clip((fbm(W, H, 77, 30, 3) - 0.55) * 3, 0, 1), PATINA, seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=3, feather=1)
    rim = np.clip(topell - ellipses(W, H, [(cx, top + 2, moko_hw(top) - 6, RY - 5, 0)]), 0, 1)
    art = OV(art, rim, lambda m: col_arr(m, "#ffe0ae", m * 0.55))
    # specular streak down the lit side
    spec = body * np.exp(-((n + 0.55) / 0.08) ** 2) * np.clip(fbm(W, H, 79, 20, 3) * 1.6 - 0.3, 0, 1)
    art = OV(art, spec, lambda m: col_arr(m, "#fff0d2", m * 0.45))
    # dark worn edge on the shadow side
    art = shade(art, body * np.clip((n - 0.55) * 2.2, 0, 1), 0.6)
    art = shade(art, body * np.clip((-n - 0.88) * 8, 0, 1), 0.75)
    # patina pooling in the relief grooves
    groove = np.clip(gaussian_filter(rel, 3) * 1.6 - rel, 0, 1) * np.clip((fbm(W, H, 81, 40, 3) - 0.35) * 2, 0, 1)
    art = G(art, groove, '#3f8f7c', '#6fb59f', seed=nx(), density=0.7, edge=0.3, bloom=0.2, rough=2, feather=0.8)
    art = add_grain(art, 712, 0.03)
    preview(art, "am-moko", bg=SAND)
    save(art, f"{OUT}/moko.webp", max_w=400, quality=84)
    clear()

if "tympanum" in PARTS:
    W = H = 520
    c = W / 2
    nx = Seq(72000); rng = random.Random(720)
    disc = circles(W, H, [(c, c, 240)])
    lt = np.mgrid[0:H, 0:W].astype(np.float32)
    lit = np.clip(0.75 - ((lt[1] - c) * 0.6 + (lt[0] - c) * 0.8) / 480, 0, 1)
    art = bronze_body(W, H, disc, 0.35 + 0.6 * lit, nx, "#a87238", BR_D, BR_H, PATINA, patina_amt=0.4, seed=721)
    items = []
    for r in (232, 214, 150, 136, 70):
        items.append((arc_pts(c, c, r, 0, math.tau, 140), 4.0, None))
    polys = []
    for k in range(12):
        a = k * math.tau / 12 - math.pi / 2
        polys.append([(c, c), (c + math.cos(a - 0.2) * 34, c + math.sin(a - 0.2) * 34), (c + math.cos(a) * 128, c + math.sin(a) * 128), (c + math.cos(a + 0.2) * 34, c + math.sin(a + 0.2) * 34)])
    for k in range(24):  # spiral ring between 150 and 214
        a = k * math.tau / 24
        px, py = c + math.cos(a) * 182, c + math.sin(a) * 182
        items.append((spiral_pts(px, py, 14, 2, a, 1.3, 26, 1), 3.4, None))
    dots = [(c + math.cos(k * math.tau / 36) * 223, c + math.sin(k * math.tau / 36) * 223, 4) for k in range(36)]
    rel = np.clip(strokes(W, H, items) + shapes(W, H, polys, smooth=False) + circles(W, H, dots) + circles(W, H, [(c, c, 20)]), 0, 1) * disc
    art = shade(art, rel, 1.14)
    art = relief(art, rel, nx, light="#ffe0ae", dark="#23140a", d=2)
    art = add_grain(art, 722, 0.03)
    preview(art, "am-tympanum", bg=SAND)
    save(art, f"{OUT}/tympanum.webp", max_w=240, quality=84)
    clear()

if "bay" in PARTS:
    W, H = 780, 820
    nx = Seq(73000); rng = random.Random(730)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#f6e2c4"), (0.22, "#f1ead8"), (0.44, "#d6ebe6"), (1, "#d6ebe6")], seed=731, streak=0.7)
    cl = ellipses(W, H, [(200, 120, 120, 16, -2), (300, 100, 80, 12, 0), (600, 70, 110, 13, 2), (520, 180, 70, 9, 0)])
    art = G(art, cl, "#fff8ec", seed=nx(), density=0.6, edge=0.2, bloom=0.4, rough=8)
    far = shapes(W, H, [[(250, 396), (330, 330), (380, 300), (420, 296), (470, 318), (540, 350), (600, 396)]])
    art = G(art, far, "#9cbcb8", "#b4c9c2", seed=nx(), density=0.7, edge=0.45, bloom=0.3, rough=6)
    isl = shapes(W, H, [[(-20, 400), (-20, 160), (30, 128), (78, 74), (118, 56), (150, 84), (190, 140), (250, 220), (310, 300), (370, 370), (420, 404)]])
    isr = shapes(W, H, [[(W + 20, 410), (W + 20, 180), (740, 150), (690, 168), (640, 220), (590, 268), (530, 340), (470, 404)]])
    for m, seed in ((isl, 733), (isr, 734)):
        art = G(art, m, "#6e9e5a", "#3f7648", seed=nx(), density=0.92, edge=0.55, bloom=0.4, rough=7)
        # second glaze: shadowed slopes from fbm
        sh = m * np.clip((fbm(W, H, seed, 50, 4) - 0.45) * 2.4, 0, 1)
        art = G(art, sh, "#2f5e3c", "#24503a", seed=nx(), density=0.7, edge=0.6, bloom=0.3, rough=5, feather=1.4)
        # gullies: tapered vertical strokes
        gl = []
        for _ in range(16):
            ys_, xs_ = np.where(m[100:390:6, ::6] > 0.6)
            if len(xs_) == 0:
                break
            i = rng.randrange(len(xs_)); x0, y0 = xs_[i] * 6, ys_[i] * 6 + 100
            L = rng.uniform(40, 110); a_ = math.pi / 2 + rng.uniform(-0.5, 0.5)
            gl.append((curve([(x0, y0), (x0 + math.cos(a_) * L * 0.5 + rng.uniform(-6, 6), y0 + L * 0.5), (x0 + math.cos(a_) * L, y0 + L)], 12), rng.uniform(4, 9), (0.3, 0.5)))
        art = G(art, gaussian_filter(strokes(W, H, gl) * m, 2), "#1f4630", seed=nx(), density=0.28, edge=0.3, bloom=0.1, rough=3, feather=1.5)
        # tree crowns: small irregular dabs, sparse
        dabs = []
        for _ in range(170):
            ys_, xs_ = np.where(m[60:395:4, ::4] > 0.7)
            i = rng.randrange(len(xs_)); dabs.append((xs_[i] * 4 + rng.uniform(-2, 2), ys_[i] * 4 + 60, rng.uniform(3, 7), rng.uniform(2, 5), rng.uniform(-20, 20)))
        art = G(art, ellipses(W, H, dabs) * m, "#2d5c38", "#4d8a4a", seed=nx(), density=0.45, edge=0.7, bloom=0.1, rough=1.5, feather=0.7)
        lit = np.clip(m - np.roll(m, 14, 1), 0, 1) * (yy < 360)
        art = G(art, gaussian_filter(lit, 6), "#c4d77a", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=3)
        clear()
    # water
    water = (yy >= 392).astype(np.float32)
    t = np.clip((yy - 392) / (H - 392), 0, 1)
    wcol = painted_sky(W, H, [(0, "#a4e2d6"), (0.5, "#a4e2d6"), (0.56, "#55cbc0"), (0.75, "#1fb0b2"), (1, "#0f6c86")], seed=736, streak=1.2)
    art[..., :3] = np.where(water[..., None] > 0, wcol[..., :3], art[..., :3])
    # sandy shallows seen through clear water (light patches) and coral heads
    sandy = ellipses(W, H, [(110, 420, 200, 22, 3), (660, 424, 180, 18, -3)]) * water
    art = G(art, sandy, "#d4f3e2", "#e9f4d2", seed=nx(), density=0.45, edge=0.4, bloom=0.5, rough=10)
    coral = ellipses(W, H, [(rng.uniform(0, W), rng.uniform(470, 800), rng.uniform(14, 40), rng.uniform(5, 12), rng.uniform(-10, 10)) for _ in range(12)]) * water
    art = G(art, coral, "#1c9c9c", "#2a8a7a", seed=nx(), density=0.22, edge=0.5, bloom=0.4, rough=6)
    # island reflections
    src = np.clip(isl + isr + far * 0.5, 0, 1)
    idx = np.clip(2 * 392 - np.arange(H), 0, H - 1)
    refl = src[idx] * water * np.clip(1 - (yy - 392) / 90, 0, 1)
    art = G(art, gaussian_filter(refl, (4, 1)), "#2f6a54", seed=nx(), density=0.55, edge=0.1, bloom=0.1, rough=3)
    shore = ellipses(W, H, [(70, 398, 130, 7, 1), (712, 404, 100, 6, -2), (395, 400, 50, 3, 0)])
    art = G(art, shore, "#f6e8c2", seed=nx(), density=0.95, edge=0.3, bloom=0.1, rough=2)
    rip = []
    for _ in range(170):
        y = rng.uniform(398, H - 6); x = rng.uniform(0, W); L = rng.uniform(8, 30) * (0.5 + (y - 392) / 420)
        rip.append(([(x, y), (x + L / 2, y - 1.0), (x + L, y)], rng.uniform(1.0, 2.2) * (0.6 + (y - 392) / 600), (0.3, 0.3)))
    art = OV(art, strokes(W, H, rip), lambda m: col_arr(m, "#f2fffa", m * 0.6))
    # small outrigger (sampan) painted with a sail
    hull = shapes(W, H, [[(486, 520), (548, 518), (540, 528), (494, 529)]])
    art = G(art, hull, "#6a3420", "#4e2616", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=1, feather=0.6)
    out = strokes(W, H, [([(482, 536), (552, 535)], 1.8, (0.1, 0.1)), ([(498, 522), (495, 536)], 1.4, None), ([(534, 521), (537, 535)], 1.4, None), ([(516, 520), (514, 476)], 1.8, None)])
    art = G(art, out, "#3a2014", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    sail = shapes(W, H, [[(517, 478), (546, 510), (517, 512)]])
    art = G(art, sail, "#fbf1dc", "#e9d6b0", seed=nx(), density=0.95, edge=0.5, bloom=0, rough=1, feather=0.6)
    art = G(art, ellipses(W, H, [(516, 532, 40, 3, 0)]), "#0e6a72", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    art = add_grain(art, 735, 0.03)
    preview(art, "am-bay")
    save_rgb(art, f"{OUT}/bay.webp", size=(780, 820), quality=80)
    clear()


def ikat_band(W, H, nx, seed):
    """Alor warp-ikat band: indigo ground, rust and undyed lozenges with hooks; warp runs horizontally."""
    rng = random.Random(seed)
    art = GP(blank(W, H), np.ones((H, W), np.float32), INDIGO, "#25304f", seed=nx(), rough=0, streak=0.6)
    cy = H / 2
    # side stripes
    st = np.zeros((H, W), np.float32)
    for y0, y1 in ((4, 10), (H - 10, H - 4)):
        st[y0:y1] = 1
    stripe = np.zeros((H, W), np.float32); stripe[14:19] = 1; stripe[H - 19:H - 14] = 1
    period = W / 8
    loz, inner, hooks = [], [], []
    for k in range(8):
        x = period * (k + 0.5)
        hw, hh = period * 0.42, (H - 46) / 2
        loz.append([(x - hw, cy), (x, cy - hh), (x + hw, cy), (x, cy + hh)])
        inner.append([(x - hw * 0.45, cy), (x, cy - hh * 0.45), (x + hw * 0.45, cy), (x, cy + hh * 0.45)])
        for s in (-1, 1):
            hx = x + s * period * 0.5
            hooks.append(([(hx, cy - hh * 0.8), (hx, cy - hh * 0.25), (hx + s * 8, cy - hh * 0.05)], 5, None))
            hooks.append(([(hx, cy + hh * 0.8), (hx, cy + hh * 0.25), (hx - s * 8, cy + hh * 0.05)], 5, None))
    L = shapes(W, H, loz, smooth=False)
    Lin = shapes(W, H, [[(p[0], p[1]) for p in q] for q in loz], smooth=False)
    ring = np.clip(L - shapes(W, H, [[(x + (px - x) * 0.72, cy + (py - cy) * 0.72) for (px, py) in q] for q, x in zip(loz, [period * (k + 0.5) for k in range(8)])], smooth=False), 0, 1)
    I = shapes(W, H, inner, smooth=False)
    hk = strokes(W, H, hooks)
    undyed = warp_feather(np.clip(ring + st + hk, 0, 1), seed, axis=1, bundle=2, amp=5)
    rust = warp_feather(np.clip(I + stripe, 0, 1), seed + 1, axis=1, bundle=2, amp=4)
    art = OV(art, undyed, lambda m: gouache_paint(m, UNDYED, "#dccaa4", seed=nx(), rough=0.8, streak=0.6), pad=0)
    art = OV(art, rust, lambda m: gouache_paint(m, RUST, MADDER, seed=nx(), rough=0.8, streak=0.6), pad=0)
    art = shade(art, np.ones((H, W), np.float32), threads(W, H, axis=1, spacing=2.6, seed=seed, amt=0.12))
    return art


if "ikat" in PARTS:
    W, H = 1024, 112
    nx = Seq(74000)
    art = ikat_band(W, H, nx, 741)
    preview(art, "am-ikat")
    save_rgb(art, f"{OUT}/ikat.webp", size=(512, 56), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 400, 64
    nx = Seq(75000)
    art = ikat_band(W, H, nx, 751)
    art = edge_fade(art, 60, "lr")
    preview(art, "am-divider", tone=SAND)
    save_full(art, f"{OUT}/divider.webp", size=(200, 32), quality=84)
    clear()
