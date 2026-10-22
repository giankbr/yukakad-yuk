"""Suzani Bukhara — thread-level suzani embroidery on ivory hand-woven cotton: every shape is filled with rows of
chain stitch following its outline (as tambour-worked suzani are), each loop drawn as twisted silk with its own sheen.
Pomegranate red, indigo, saffron, with leaf green and aubergine accents. Original medallion / vine / pomegranate designs.
Run: python3 -I suzani-bukhara.py [part ...]   parts: cloth medallion vine sprig divider pomegranate
Assets -> public/themes/art/suzani-bukhara/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f2_lib import *  # noqa

OUT = outdir("suzani-bukhara")
PARTS = sys.argv[1:] or ["cloth", "medallion", "vine", "sprig", "divider", "pomegranate"]
RED, RED_D, ROSE = "#b0262c", "#86191f", "#d24b4a"
INDIGO, INDIGO_L = "#262f69", "#3f5a9a"
SAFFRON, GREEN, AUBER, IVORY = "#e0a22a", "#4f7a3a", "#5a2741", "#efe3c8"
STEP, WID, SPC = 5.6, 4.4, 4.6


def fill(emb, mask, col, outline=None, rows=None):
    cols = ([outline] if outline else []) + [col] * 400
    chain_fill(emb, mask, col, spacing=SPC, step=STEP, width=WID, cols=cols)


def disc(W, H, cx, cy, r):
    return circles(W, H, [(cx, cy, r)])


def ring(W, H, cx, cy, r0, r1):
    return np.clip(disc(W, H, cx, cy, r1) - disc(W, H, cx, cy, r0), 0, 1)


def serrated_leaf(cx, cy, L, w, ang, teeth=6):
    """Leaf with saw-tooth edges (suzani 'tooth' leaf)."""
    pts = []
    n = teeth * 4
    for side in (1, -1):
        rng_ = range(n + 1) if side == 1 else range(n, -1, -1)
        for i in rng_:
            t = i / n
            ww = w * math.sin(math.pi * t) ** 0.8
            if i % 4 == 2:
                ww *= 1.28
            u = t * L
            pts.append((u, side * ww))
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + u * ca - v * sa, cy + u * sa + v * ca) for u, v in pts]


def lobe_ring(cx, cy, r0, r1, n, phase=0.0):
    """Scalloped ring outline: n rounded lobes between r0 and r1."""
    pts = []
    for i in range(n * 24):
        a = phase + i / (n * 24) * math.tau
        k = abs(math.sin(a * n / 2))
        r = r0 + (r1 - r0) * k ** 0.6
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def finish(arr, W, H, seed):
    """Thread shadow on the cloth + a little fuzz."""
    a = arr[..., 3]
    sh = np.roll(np.roll(gaussian_filter(a, 1.4), 1, 0), 1, 1) * 0.35
    out = over(np.concatenate([np.ones((H, W, 3), np.float32) * col_arr("#3a2410"), sh[..., None]], -1), arr)
    return out


def preview_on_cloth(arr, name):
    H, W = arr.shape[:2]
    cl = cotton(W - W % 3, H - H % 3, seed=2, tile=False)
    cl = np.pad(cl, ((0, H - cl.shape[0]), (0, W - cl.shape[1]), (0, 0)), mode="edge")
    mean = cl.mean(axis=(0, 1), keepdims=True)
    cl = mean + (cl - mean) * 0.45
    rgb = comp_rgb(cl, arr)
    prev_rgb(rgb, name)


def rosette(emb, W, H, cx, cy, r, petals=6, c_pet=RED, c_out=INDIGO, c_mid=SAFFRON):
    pets = [petal_pts(cx + math.cos(a) * r * 0.2, cy + math.sin(a) * r * 0.2, r * 0.85, r * 0.36, a, n=16) for a in np.linspace(0, math.tau, petals, endpoint=False)]
    for p in pets:
        fill(emb, shapes(W, H, [p]), c_pet, outline=c_out)
    fill(emb, disc(W, H, cx, cy, r * 0.3), c_mid, outline=c_out)


def part_cloth():
    rgb = cotton(510, 510, "#f1e7d3", seed=5, tile=True)
    mean = rgb.mean(axis=(0, 1), keepdims=True)
    rgb = mean + (rgb - mean) * 0.45
    prev_rgb(rgb, "sb-cloth")
    rgb_save(rgb, f"{OUT}/cloth.webp", quality=74)


def part_medallion():
    W = H = 640
    cx = cy = 320
    emb = Embroidery(W, H, seed=3)
    # outer serrated leaves pointing out between the lobes, with red buds at the tips
    n_lobe = 12
    for k in range(n_lobe):
        a = (k + 0.5) / n_lobe * math.tau
        leaf = serrated_leaf(cx + math.cos(a) * 214, cy + math.sin(a) * 214, 78, 17, a, teeth=4)
        fill(emb, shapes(W, H, [leaf], smooth=False), GREEN, outline=INDIGO)
        bx, by = cx + math.cos(a) * 300, cy + math.sin(a) * 300
        fill(emb, disc(W, H, bx, by, 13), ROSE, outline=RED_D)
    for k in range(n_lobe):
        a = k / n_lobe * math.tau
        bx, by = cx + math.cos(a) * 236, cy + math.sin(a) * 236
        fill(emb, disc(W, H, bx, by, 10), SAFFRON, outline=RED_D)
    # scalloped indigo lobe ring with saffron edge
    lob = shapes(W, H, [lobe_ring(cx, cy, 166, 224, n_lobe)], smooth=True)
    lob = np.clip(lob - disc(W, H, cx, cy, 162), 0, 1)
    fill(emb, lob, INDIGO, outline=SAFFRON)
    # saffron ring + red field + rose petals
    fill(emb, ring(W, H, cx, cy, 150, 163), SAFFRON)
    pets = [petal_pts(cx + math.cos(a) * 44, cy + math.sin(a) * 44, 92, 30, a, n=18) for a in np.linspace(0, math.tau, 8, endpoint=False) + math.pi / 8]
    pm = shapes(W, H, pets)
    field = np.clip(ring(W, H, cx, cy, 40, 150) - gaussian_filter(pm, 0.6) * 1.3, 0, 1)
    fill(emb, field, RED, outline=RED_D)
    for p in pets:
        fill(emb, shapes(W, H, [p]), ROSE, outline=AUBER)
    fill(emb, ring(W, H, cx, cy, 27, 41), INDIGO)
    fill(emb, disc(W, H, cx, cy, 28), SAFFRON, outline=RED_D)
    # small saffron dots between the rose petals (satin stitch)
    for a in np.linspace(0, math.tau, 8, endpoint=False):
        emb.satin_dot(cx + math.cos(a) * 128, cy + math.sin(a) * 128, 6, SAFFRON)
    art = finish(emb.array(), W, H, 1)
    preview_on_cloth(art, "sb-medallion")
    save(art, f"{OUT}/medallion.webp", max_w=420, quality=82)
    clear()


def part_vine():
    """Repeat-x border: a wavy indigo stem with serrated leaves, rosettes and tulip buds (seamless at the ends)."""
    W, H = 1080, 200
    emb = Embroidery(W, H, seed=7)
    yc = 100
    stem = [(x, yc + math.sin(x / W * math.tau * 2) * 34) for x in range(-20, W + 21, 4)]
    for off in (-2.6, 2.6):
        emb.chain([(x, y + off) for x, y in stem], INDIGO, step=STEP, width=WID)
    for k in range(4):
        x = (k + 0.25) * W / 4
        y = yc + math.sin(x / W * math.tau * 2) * 34
        side = -1 if k % 2 == 0 else 1
        rosette(emb, W, H, x, y + side * 44, 34, petals=6, c_pet=RED if k % 2 else ROSE)
        lx = (k + 0.62) * W / 4
        ly = yc + math.sin(lx / W * math.tau * 2) * 34
        leaf = serrated_leaf(lx, ly, 70, 15, -math.pi / 2 * side + 0.5, teeth=4)
        fill(emb, shapes(W, H, [leaf], smooth=False), GREEN, outline=INDIGO)
        tx = (k + 0.85) * W / 4
        ty = yc + math.sin(tx / W * math.tau * 2) * 34
        bud = petal_pts(tx, ty, 40, 15, math.pi / 2 * side, n=14)
        fill(emb, shapes(W, H, [bud]), SAFFRON, outline=RED_D)
    art = finish(emb.array(), W, H, 2)
    preview_on_cloth(art, "sb-vine")
    save_full(art, f"{OUT}/vine.webp", size=(540, 100), quality=82)
    clear()


def tulip(emb, W, H, x, by, s, col=RED):
    stem = [(x, by), (x + s * 0.05, by - s * 0.5), (x, by - s * 0.9)]
    emb.chain(curve(stem, 20), GREEN, step=STEP, width=WID)
    for side in (-1, 1):
        leaf = serrated_leaf(x, by - s * 0.32, s * 0.55, s * 0.12, -math.pi / 2 + side * 0.9, teeth=3)
        fill(emb, shapes(W, H, [leaf], smooth=False), GREEN, outline=INDIGO)
    cup = [(x - s * 0.34, by - s * 1.32), (x - s * 0.18, by - s * 1.1), (x, by - s * 1.36), (x + s * 0.18, by - s * 1.1), (x + s * 0.34, by - s * 1.32), (x + s * 0.3, by - s * 0.96), (x, by - s * 0.82), (x - s * 0.3, by - s * 0.96)]
    fill(emb, shapes(W, H, [cup], smooth=True), col, outline=INDIGO)


def part_sprig():
    W, H = 220, 240
    emb = Embroidery(W, H, seed=9)
    tulip(emb, W, H, 110, 226, 150)
    art = finish(emb.array(), W, H, 3)
    preview_on_cloth(art, "sb-sprig")
    save(art, f"{OUT}/sprig.webp", max_w=90, quality=84)
    clear()


def part_divider():
    W, H = 640, 120
    emb = Embroidery(W, H, seed=11)
    yc = 60
    for side in (-1, 1):
        stem = [(320 + side * (40 + i * 4), yc + math.sin(i / 60 * math.pi * 2) * 7) for i in range(66)]
        emb.chain(stem, INDIGO, step=STEP, width=WID)
        for j, t in enumerate((0.3, 0.55, 0.8)):
            i = int(t * 65)
            lx, ly = stem[i]
            up = -1 if j % 2 == 0 else 1
            leaf = serrated_leaf(lx, ly, 36, 9, (-math.pi / 2 if up < 0 else math.pi / 2) - side * up * 0.7, teeth=3)
            fill(emb, shapes(W, H, [leaf], smooth=False), GREEN, outline=INDIGO)
        ex, ey = stem[-1]
        fill(emb, disc(W, H, ex + side * 8, ey, 8), SAFFRON, outline=RED_D)
    rosette(emb, W, H, 320, yc, 36, petals=8, c_pet=RED)
    art = finish(emb.array(), W, H, 4)
    preview_on_cloth(art, "sb-divider")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()


def part_pomegranate():
    W, H = 300, 320
    emb = Embroidery(W, H, seed=13)
    cx, cy = 150, 180
    body = [(cx + math.cos(a) * 104 * (1 + 0.04 * math.sin(3 * a)), cy + math.sin(a) * 100) for a in np.linspace(0, math.tau, 60, endpoint=False)]
    bm = shapes(W, H, [body])
    win = shapes(W, H, [ellipse_pts(cx, cy + 6, 52, 58, 24)])
    fill(emb, np.clip(bm - gaussian_filter(win, 0.6) * 1.3, 0, 1), RED, outline=RED_D)
    fill(emb, win, IVORY, outline=SAFFRON)
    for k in range(16):
        a = k * 2.4
        r = 10 + 6.5 * math.sqrt(k + 1) * 1.6
        if r > 48:
            continue
        emb.satin_dot(cx + math.cos(a) * r * 0.85, cy + 6 + math.sin(a) * r, 6.5, ROSE if k % 2 else RED)
    crown = [(cx - 34, cy - 92), (cx - 40, cy - 132), (cx - 18, cy - 112), (cx, cy - 140), (cx + 18, cy - 112), (cx + 40, cy - 132), (cx + 34, cy - 92)]
    fill(emb, shapes(W, H, [crown], smooth=False), SAFFRON, outline=INDIGO)
    for side in (-1, 1):
        leaf = serrated_leaf(cx + side * 30, cy - 96, 64, 13, -math.pi / 2 + side * 1.05, teeth=3)
        fill(emb, shapes(W, H, [leaf], smooth=False), GREEN, outline=INDIGO)
    art = finish(emb.array(), W, H, 5)
    preview_on_cloth(art, "sb-pomegranate")
    save(art, f"{OUT}/pomegranate.webp", max_w=130, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
