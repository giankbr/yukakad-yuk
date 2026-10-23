"""Paisley Kashmir — kani-woven Kashmir shawl: a chand-dar layout (round central medallion, quarter medallions in the
corners), a dense boteh border, a single elaborate boteh, and an ivory pashmina twill with tiny buti. Everything is
painted flat, then snapped to a 7-thread palette on a weft grid and given 2/2 twill relief (kani()) so it reads woven.
Run: python3 -I paisley-kashmir.py [part ...]  parts: boteh medallion corner border weave"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h4_lib import *  # noqa

OUT = outdir("paisley-kashmir")
PARTS = sys.argv[1:] or ["boteh", "medallion", "corner", "border", "weave", "hero"]
IVORY, SAFF, SAFF_L, MADDER, MADDER_D, GREEN, GREEN_L, INDIGO, ROSE = (
    "#f2e7cf", "#d9962c", "#efc56c", "#a3302a", "#6e1d1b", "#1f4b3a", "#5f8a52", "#2c3b5c", "#d77a68")
PAL = [IVORY, SAFF, SAFF_L, MADDER, MADDER_D, GREEN, GREEN_L, INDIGO, ROSE]

# boteh outline in unit space: round base at (0, 0.55), body rising to a tip that curls to the left
_B = [(0.0, 1.0), (0.62, 0.86), (0.98, 0.42), (1.0, -0.12), (0.84, -0.62), (0.56, -1.06), (0.22, -1.42), (-0.12, -1.72),
      (-0.42, -1.9), (-0.62, -1.86), (-0.6, -1.66), (-0.42, -1.5), (-0.5, -1.2), (-0.72, -0.78), (-0.92, -0.28),
      (-0.96, 0.26), (-0.74, 0.74)]


def bpts(cx, cy, s, rot=0.0, flip=1, inset=0.0):
    pts = []
    for x, y in _B:
        # inset toward the body centre (0, -0.1) keeping the curl
        x2, y2 = x * (1 - inset), -0.1 + (y + 0.1) * (1 - inset * 0.92)
        pts.append((cx + x2 * s * flip, cy + y2 * s))
    return rot_pts(pts, cx, cy, rot)


def bpts_s(x, y, s, rot, inset=0.0):
    return [bpts(x, y, s, rot, 1, inset)]


def layer(dst, mask, col):
    return over(dst, col_arr(mask, col, mask))


def rosette(W, H, x, y, r, n=6, rot=0.0):
    pet = [petal_pts(x, y, r, r * 0.55, rot + k * math.tau / n, n=10) for k in range(n)]
    return shapes(W, H, pet)


def boteh(dst, W, H, cx, cy, s, rot=0.0, flip=1, scheme=0, detail=1.0):
    """Woven boteh: dark outline, madder band, saffron dotted band, ivory field with a flowering stem."""
    c = [(GREEN, MADDER, SAFF, IVORY, ROSE), (MADDER_D, SAFF, GREEN, IVORY, MADDER), (INDIGO, MADDER, SAFF_L, IVORY, GREEN)][scheme % 3]
    rng = random.Random(int(cx * 7 + cy * 13 + s))
    # outer serrated halo (small leaf teeth around the boteh)
    halo = shapes(W, H, [bpts(cx, cy, s * 1.1, rot, flip)])
    teeth = []
    out = bpts(cx, cy, s * 1.1, rot, flip)
    dense = along(curve(out + out[:2], 12 * len(out)), max(4, s * 0.16))
    for x0, y0, a0 in dense:
        a = a0 - math.pi / 2 * flip
        teeth.append(petal_pts(x0, y0, s * 0.16, s * 0.06, a, n=8))
    dst = layer(dst, np.clip(shapes(W, H, teeth) + halo, 0, 1), c[2] if detail > 0.6 else c[0])
    dst = layer(dst, shapes(W, H, [bpts(cx, cy, s, rot, flip)]), c[0])
    dst = layer(dst, shapes(W, H, [bpts(cx, cy, s, rot, flip, 0.1)]), c[1])
    dst = layer(dst, shapes(W, H, [bpts(cx, cy, s, rot, flip, 0.2)]), c[2])
    if detail > 0.6:
        band = bpts(cx, cy, s, rot, flip, 0.25)
        dd = along(curve(band + band[:2], 12 * len(band)), max(3, s * 0.11))
        dst = layer(dst, circles(W, H, [(x, y, max(1.2, s * 0.028)) for x, y, _ in dd]), c[0])
    fm = shapes(W, H, [bpts(cx, cy, s, rot, flip, 0.32)])
    dst = layer(dst, fm, c[3])
    # flowering stem in the field
    base = rot_pts([(cx, cy + s * 0.6)], cx, cy, rot)[0]
    top = rot_pts([(cx - s * 0.18 * flip, cy - s * 1.0)], cx, cy, rot)[0]
    mid = rot_pts([(cx + s * 0.12 * flip, cy - s * 0.2)], cx, cy, rot)[0]
    stem = curve([base, mid, top], 20)
    dst = layer(dst, strokes(W, H, [(stem, max(1.4, s * 0.035), (0.0, 0.3))]), c[0])
    lv = []
    for k, t in enumerate([0.3, 0.5, 0.7]):
        x, y = stem[int(t * (len(stem) - 1))]
        for side in (-1, 1):
            a = rot - math.pi / 2 + side * 1.0
            lv.append(petal_pts(x, y, s * 0.22 * (1 - t * 0.4), s * 0.07, a, n=8))
    dst = layer(dst, shapes(W, H, lv), GREEN_L if c[0] != GREEN_L else GREEN)
    if detail > 0.8:
        inner = shapes(W, H, [bpts(cx, cy, s, rot, flip, 0.4)])
        ys, xs = np.where(inner > 0.5)
        pts_ = []
        for _ in range(400 if len(xs) else 0):
            k = rng.randrange(len(xs))
            x, y = float(xs[k]), float(ys[k])
            if min(math.hypot(x - px, y - py) for px, py in stem) < s * 0.16:
                continue
            if all(math.hypot(x - qx, y - qy) > s * 0.15 for qx, qy, _ in pts_):
                pts_.append((x, y, rng.random()))
        for x, y, r_ in pts_:
            col = [MADDER, INDIGO, SAFF, ROSE][int(r_ * 4)]
            dst = layer(dst, rosette(W, H, x, y, s * 0.06, 4, r_ * 3), col)
            dst = layer(dst, circles(W, H, [(x, y, max(1.0, s * 0.018))]), SAFF_L if col != SAFF_L else MADDER)
    fx, fy = rot_pts([(cx, cy + s * 0.18)], cx, cy, rot)[0]
    dst = layer(dst, rosette(W, H, fx, fy, s * 0.24, 6, rng.uniform(0, 1)), c[4])
    dst = layer(dst, circles(W, H, [(fx, fy, s * 0.08)]), SAFF_L if c[4] != SAFF_L else SAFF)
    tx, ty = top
    dst = layer(dst, rosette(W, H, tx, ty, s * 0.13, 5, 0.3), c[1])
    dst = layer(dst, circles(W, H, [(tx, ty, s * 0.045)]), c[2])
    return dst


def weave_finish(arr, cell, seed):
    out = kani(arr, cell=cell, seed=seed, palette=PAL)
    out[..., :3] *= (0.94 + 0.08 * fbm(out.shape[1], out.shape[0], seed + 3, 90, 3))[..., None]
    return out


if "boteh" in PARTS:
    W, H = 320, 470
    art = blank(W, H)
    art = boteh(art, W, H, 160, 282, 112, rot=0.12, flip=1, scheme=0)
    art = weave_finish(art, 3, 5)
    preview(art, "pk-boteh", tone=IVORY)
    save(art, f"{OUT}/boteh.webp", max_w=220, quality=84)
    clear()


def medallion(W, H, cx, cy, R, r_in, n=12, seed=1):
    art = blank(W, H)
    lob = [(cx + math.cos(t) * (R + R * 0.035 * abs(math.cos(8 * t))), cy + math.sin(t) * (R + R * 0.035 * abs(math.cos(8 * t))))
           for t in np.linspace(0, math.tau, 400, endpoint=False)]
    art = layer(art, shapes(W, H, [lob], smooth=False), GREEN)
    # serrated rim of tiny leaves
    rim_ = [petal_pts(cx + math.cos(t) * R * 0.975, cy + math.sin(t) * R * 0.975, R * 0.05, R * 0.02, t, n=8) for t in np.linspace(0, math.tau, 140, endpoint=False)]
    art = layer(art, shapes(W, H, rim_), SAFF)
    art = layer(art, circles(W, H, [(cx, cy, R * 0.93)]), MADDER_D)
    # vine guard band
    vb = circles(W, H, [(cx, cy, R * 0.9)])
    art = layer(art, vb, MADDER)
    ring_r = (R * 0.9 + r_in) / 2
    vine = [(cx + math.cos(t) * (ring_r + (R - r_in) * 0.16 * math.sin(n * 2 * t)), cy + math.sin(t) * (ring_r + (R - r_in) * 0.16 * math.sin(n * 2 * t))) for t in np.linspace(0, math.tau, 600)]
    art = layer(art, strokes(W, H, [(vine, max(1.5, R * 0.007), None)]), GREEN_L)
    vl = []
    for x, y, a in along(vine, R * 0.045):
        vl.append(petal_pts(x, y, R * 0.03, R * 0.011, a + 0.9, n=8))
    art = layer(art, shapes(W, H, vl), GREEN_L)
    for k in range(n):
        a = k * math.tau / n
        x, y = cx + math.cos(a) * ring_r, cy + math.sin(a) * ring_r
        art = boteh(art, W, H, x, y, (R * 0.9 - r_in) * 0.38, rot=a + math.pi / 2 + 0.25, flip=1, scheme=k % 3, detail=0.9)
        a2 = a + math.tau / n / 2
        x2, y2 = cx + math.cos(a2) * (ring_r + (R - r_in) * 0.12), cy + math.sin(a2) * (ring_r + (R - r_in) * 0.12)
        art = layer(art, rosette(W, H, x2, y2, (R - r_in) * 0.09, 6, a2), SAFF_L)
        art = layer(art, circles(W, H, [(x2, y2, (R - r_in) * 0.03)]), MADDER_D)
        x3, y3 = cx + math.cos(a2) * (r_in + (R - r_in) * 0.14), cy + math.sin(a2) * (r_in + (R - r_in) * 0.14)
        art = layer(art, shapes(W, H, [petal_pts(x3, y3, (R - r_in) * 0.12, (R - r_in) * 0.04, a2 + 0.6, n=8),
                                       petal_pts(x3, y3, (R - r_in) * 0.12, (R - r_in) * 0.04, a2 - 0.6 + math.pi, n=8)]), GREEN_L)
    # sprinkle tiny flowers on the bare madder ground
    rng = random.Random(seed)
    mad = rgb_of(MADDER)
    bare = (np.abs(art[..., :3] - mad).sum(-1) < 0.05) & (art[..., 3] > 0.9)
    er = gaussian_filter(bare.astype(np.float32), R * 0.012) > 0.97
    ys, xs = np.where(er)
    fl = []
    for _ in range(3000):
        if len(xs) == 0:
            break
        i = rng.randrange(len(xs)); x, y = float(xs[i]), float(ys[i])
        if all((x - a) ** 2 + (y - b) ** 2 > (R * 0.04) ** 2 for a, b, _ in fl):
            fl.append((x, y, rng.random()))
    for col_i, col in enumerate([SAFF_L, IVORY, ROSE]):
        sel = [(x, y) for x, y, r_ in fl if int(r_ * 3) == col_i]
        if sel:
            art = layer(art, shapes(W, H, [p for x, y in sel for p in [petal_pts(x, y, R * 0.016, R * 0.008, a, n=6) for a in (0, 1.57, 3.14, 4.71)]]), col)
    # inner guard: saffron band with green dots, then a thin green line; centre left open (transparent)
    art = layer(art, circles(W, H, [(cx, cy, r_in + R * 0.05)]), SAFF)
    dd = [(cx + math.cos(t) * (r_in + R * 0.025), cy + math.sin(t) * (r_in + R * 0.025), R * 0.011) for t in np.linspace(0, math.tau, 72, endpoint=False)]
    art = layer(art, circles(W, H, dd), GREEN)
    art = layer(art, circles(W, H, [(cx, cy, r_in + R * 0.006)]), GREEN)
    hole = circles(W, H, [(cx, cy, r_in - R * 0.004)])
    art[..., 3] *= 1 - hole
    return art


if "medallion" in PARTS:
    W = H = 720
    art = medallion(W, H, 360, 360, 340, 206, n=12, seed=3)
    art = weave_finish(art, 3, 9)
    preview(art, "pk-medallion", tone=IVORY)
    save_full(art, f"{OUT}/medallion.webp", size=(640, 640), quality=82)
    clear()

if "corner" in PARTS:
    W = H = 640
    art = medallion(W, H, 0, 0, 600, 380, n=16, seed=5)
    art = weave_finish(art, 3, 11)
    preview(art, "pk-corner", tone=IVORY)
    save_full(art, f"{OUT}/corner.webp", size=(320, 320), quality=82)
    clear()

if "border" in PARTS:
    W, H = 480, 150
    art = layer(blank(W, H), np.ones((H, W), np.float32), MADDER)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    xx = np.mgrid[0:H, 0:W][1].astype(np.float32)
    for y0, y1, col in [(0, 14, GREEN), (14, 20, SAFF), (130, 136, SAFF), (136, 150, GREEN)]:
        art = layer(art, ((yy >= y0) & (yy < y1)).astype(np.float32), col)
    # guard vine: little saffron dots + ivory zigzag in the green stripes
    dots = circles(W, H, [(x + 6, 7, 2.6) for x in range(0, W, 12)] + [(x, 143, 2.6) for x in range(0, W, 12)])
    art = layer(art, dots, SAFF_L)
    # alternating botehs (wrap: draw extra copies at both ends)
    for k in range(-1, 9):
        x = 30 + k * 60
        up = k % 2 == 0
        art = boteh(art, W, H, x, 82 if up else 70, 30, rot=(0.25 if up else math.pi + 0.25), flip=1, scheme=k % 3, detail=0.7)
        art = layer(art, rosette(W, H, x + 30, 40 if up else 108, 8, 6, 0.2), SAFF_L)
        art = layer(art, circles(W, H, [(x + 30, 40 if up else 108, 2.6)]), MADDER_D)
    art = weave_finish(art, 3, 13)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/border.webp", size=(240, 75), quality=86)
    save_rgb(np.ascontiguousarray(np.rot90(art, -1)), f"{OUT}/border-v.webp", size=(75, 240), quality=86)
    to_image(np.tile(art, (1, 3, 1))).convert("RGB").save(f"{PREV}/pk-border.png")
    clear()

if "weave" in PARTS:
    W = H = 240
    xx, yy = grid_xy(W, H)
    base = rgb_of(IVORY)
    tw = np.sin(((xx + yy) / 3.0) * math.pi) * 0.5 + 0.5
    fib = gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (0.4, 2.5), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    slub = wrapn(W, H, 4, 18)
    rgb = base[None, None] * (0.95 + 0.04 * tw + 0.02 * fib + (slub - 0.5) * 0.05)[..., None]
    art = opaque(rgb)
    # tiny buti: a three-leaf sprig with a madder bud, two per tile (staggered)
    sp = blank(W, H)
    for (x, y, a) in [(60, 70, -0.3), (180, 190, 0.3)]:
        sp = layer(sp, shapes(W, H, [petal_pts(x, y, 20, 6, a - math.pi / 2 + 0.8, n=8), petal_pts(x, y, 20, 6, a - math.pi / 2 - 0.8, n=8)]), GREEN_L)
        sp = layer(sp, shapes(W, H, bpts_s(x, y + 4, 11, a)), MADDER)
        sp = layer(sp, shapes(W, H, bpts_s(x, y + 4, 11, a, 0.45)), SAFF_L)
    sp = kani(sp, cell=2, seed=7, palette=PAL)
    sp[..., 3] *= 0.26
    art = over(art, sp)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/weave.webp", quality=80)
    to_image(np.tile(art, (2, 2, 1))).convert("RGB").save(f"{PREV}/pk-weave.png")

if "hero" in PARTS:
    W, H = 600, 900
    cx, cy, S = 300, 570, 212
    art = blank(W, H)
    outl = bpts(cx, cy, S * 1.17, 0.1, 1)
    trail = along(curve(outl + outl[:2], 12 * len(outl)), 40)
    vine = curve(outl + outl[:2], 12 * len(outl))
    art = layer(art, strokes(W, H, [(vine, 3, None)]), GREEN)
    for k, (x, y, a) in enumerate(trail):
        art = layer(art, shapes(W, H, [petal_pts(x, y, 15, 5, a - 2.2, n=8), petal_pts(x, y, 15, 5, a + 2.2 - math.pi, n=8)]), GREEN_L)
    for k, (x, y, a) in enumerate(trail):
        if k % 2:
            art = boteh(art, W, H, x, y, 17, rot=a - 1.2, flip=1, scheme=k % 3, detail=0.7)
        else:
            art = layer(art, rosette(W, H, x, y, 10, 6, a), [SAFF, ROSE, MADDER][k % 3])
            art = layer(art, circles(W, H, [(x, y, 3.4)]), SAFF_L)
    art = boteh(art, W, H, cx, cy, S, rot=0.1, flip=1, scheme=1, detail=0.7)
    field = shapes(W, H, [bpts(cx, cy, S, 0.1, 1, 0.32)])
    art[..., 3] *= 1 - field
    for ins, col, step, r in [(0.05, SAFF_L, 16, 3.2), (0.15, MADDER, 13, 2.6)]:
        pp = bpts(cx, cy, S, 0.1, 1, ins)
        dd = along(curve(pp + pp[:2], 12 * len(pp)), step)
        art = layer(art, circles(W, H, [(x, y, r) for x, y, _ in dd]), col)
    # extra woven guard: a ring of tiny rosettes on the saffron band
    band = bpts(cx, cy, S, 0.1, 1, 0.26)
    for x, y, _ in along(curve(band + band[:2], 12 * len(band)), 22):
        art = layer(art, rosette(W, H, x, y, 7, 5, x * 0.1), IVORY)
        art = layer(art, circles(W, H, [(x, y, 2.2)]), MADDER)
    art = weave_finish(art, 3, 17)
    art[..., 3] *= 1 - field
    preview(art, "pk-hero", bg="#7a8a70")
    save_full(art, f"{OUT}/frame.webp", size=(480, 720), quality=84)
    m = shapes(W, H, [bpts(cx, cy, S, 0.1, 1, 0.29)])
    mk = np.zeros((H, W, 4), np.float32); mk[..., 3] = m; mk[..., :3] = 0
    to_image(mk).resize((480, 720), Image.LANCZOS).save(f"{OUT}/mask.webp", "WEBP", quality=70, method=6)
    print("mask", os.path.getsize(f"{OUT}/mask.webp") // 1024, "KB")
    clear()
