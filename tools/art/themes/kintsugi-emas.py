"""Kintsugi Emas — cream crackle-glazed plate (top view) with an iron-brown rim, its gold-mended seams on a separate
aligned layer (for the shimmer), a charcoal tea bowl with nuka drips and gold seams, sumi ink-wash band, a gold-crack
divider and a mended shard. Original art. Run: python3 -I kintsugi-emas.py [part ...]
parts: piring mangkuk tinta retak pecahan kertas"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g4_lib import *
from scipy.spatial import cKDTree

OUT = outdir("kintsugi-emas")
PARTS = sys.argv[1:] or ["piring", "mangkuk", "tinta", "retak", "pecahan", "kertas"]
CREAM = "#f2ede3"
GLAZE, GLAZE_D = "#efe7d6", "#ddd1ba"
CHAR, CHAR_D = "#34312d", "#1f1d1b"
GOLD = "#c49a45"


def crack(p0, p1, rng, n=14, jit=0.12):
    """Jagged crack polyline from p0 to p1 (random perpendicular kinks, sharper near the start)."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    px, py = -(y1 - y0) / L, (x1 - x0) / L
    pts = [p0]
    off = 0.0
    for i in range(1, n):
        t = i / n
        off = off * 0.45 + rng.uniform(-1, 1) * L * jit / math.sqrt(n)
        pts.append((x0 + (x1 - x0) * t + px * off, y0 + (y1 - y0) * t + py * off))
    pts.append(p1)
    return pts


def crack_net(cx, cy, R, rng, mains):
    """mains: list of (angle_start, angle_end) on the rim; each crack wanders across, with 1-2 short branches."""
    lines = []
    for a0, a1, depth in mains:
        p0 = (cx + math.cos(a0) * R * 1.02, cy + math.sin(a0) * R * 1.02)
        if a1 is None:
            p1 = (cx + math.cos(a0) * R * (1 - depth), cy + math.sin(a0) * R * (1 - depth))
            p1 = (p1[0] + rng.uniform(-30, 30), p1[1] + rng.uniform(-30, 30))
        else:
            p1 = (cx + math.cos(a1) * R * 1.02, cy + math.sin(a1) * R * 1.02)
        main = crack(p0, p1, rng, n=16, jit=0.16)
        lines.append((main, 1.0))
        for _ in range(rng.randint(1, 2)):
            k = rng.randint(4, len(main) - 4)
            bx, by = main[k]
            ang = math.atan2(main[k + 1][1] - by, main[k + 1][0] - bx) + rng.choice([-1, 1]) * rng.uniform(0.6, 1.1)
            Lb = rng.uniform(40, 90)
            lines.append((crack((bx, by), (bx + math.cos(ang) * Lb, by + math.sin(ang) * Lb), rng, n=6, jit=0.2), 0.6))
    return lines


def gold_seams(W, H, lines, width, seed):
    items = [(pts, width * k, (0.0, 0.35) if k < 1 else (0.04, 0.04)) for pts, k in lines]
    m = strokes(W, H, items)
    m = np.clip(displace(m, seed, 1.2, 8), 0, 1)
    art = blank(W, H)
    art = FO(art, m, GOLD, seed=seed, emboss=0.9, sparkle=0.2)
    # a little lighter ridge where the lacquer stands proud
    ridge = strokes(W, H, [(pts, max(0.8, width * k * 0.25), None) for pts, k in lines])
    art = OV(art, ridge * m, lambda q: tint(q, "#f3d991", 0.45), pad=6)
    return art, m


def crackle(W, H, mask, seed, n=520, width=0.9):
    """Fine crazing network (Voronoi edges) inside mask."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2)) * [W, H]
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:H, 0:W]
    q = np.stack([xx.ravel(), yy.ravel()], -1)
    d, _ = tree.query(q, k=2)
    edge = (d[:, 1] - d[:, 0]).reshape(H, W).astype(np.float32)
    lines = np.clip(1 - edge / width, 0, 1)
    lines = displace(lines, seed + 1, 2.0, 30)
    return lines * mask


if "piring" in PARTS:
    W = H = 760
    cx, cy, R = 380, 380, 330
    nx = Seq(1100); rng = random.Random(11)
    body = circles(W, H, [(cx, cy, R)])
    well = circles(W, H, [(cx, cy, R * 0.62)])
    rim = np.clip(body - circles(W, H, [(cx, cy, R * 0.9)]), 0, 1)
    art = blank(W, H)
    # soft cast shadow on the table
    sh = np.roll(np.roll(gaussian_filter(body, 18), 14, 0), 10, 1) * 0.35
    art = over(art, tint(sh, "#5b5246"))
    plate = gouache_paint(body, GLAZE, GLAZE_D, seed=nx(), rough=0.8, streak=0.25)
    # glaze pooling: light from the top-left, the well is shaded, the rim has a raised lip
    hgt = gaussian_filter(body, 10) * 0.8 + gaussian_filter(rim, 4) * 0.4 - gaussian_filter(well, 16) * 0.25
    light = emboss_light(hgt, 2.0, k=60)
    mot = fbm(W, H, 33, 70, 4)
    plate[..., :3] *= (0.86 + 0.28 * light[..., None]) * (0.97 + 0.06 * mot[..., None])
    art = over(art, plate)
    # iron-brown rim (kuchibeni) as a soft wash right at the lip
    lip = np.clip(body - circles(W, H, [(cx, cy, R - 7)]), 0, 1)
    art = G(art, lip, "#8a5a36", "#5e3c24", seed=nx(), density=0.85, edge=0.6, bloom=0.2, gran=0.4, rough=2.5, feather=1.2)
    art = G(art, np.clip(body - circles(W, H, [(cx, cy, R - 22)]), 0, 1) * 0.35, "#a98563", seed=nx(), density=0.35, edge=0.1, bloom=0.4, rough=6, feather=5)
    # a pale glaze ring at the well
    art = G(art, np.clip(circles(W, H, [(cx, cy, R * 0.63)]) - circles(W, H, [(cx, cy, R * 0.6)]), 0, 1), "#cdbfa5", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=3, feather=2)
    clear()
    # crazing
    cr = crackle(W, H, body, 7, n=420, width=0.85)
    art = OV(art, cr * 0.2, lambda q: tint(q, "#7c705e"), pad=2)
    # iron speckles
    sp = circles(W, H, [(cx + r * math.cos(a), cy + r * math.sin(a), rng.uniform(0.7, 2.0)) for r, a in [(rng.uniform(0, R - 12), rng.uniform(0, math.tau)) for _ in range(60)]])
    art = OV(art, sp * 0.7, lambda q: tint(q, "#6b4a30"), pad=2)
    # the break lines themselves (a hairline shadow under the gold)
    lines = crack_net(cx, cy, R, rng, [(-2.35, 0.55, 0), (2.5, None, 0.75), (-0.6, None, 0.55)])
    under = strokes(W, H, [(pts, 9 * k, None) for pts, k in lines])
    art = OV(art, gaussian_filter(under, 2) * body * 0.4, lambda q: tint(q, "#4a4036"), pad=4)
    clear()
    preview(art, "ki-piring", tone=CREAM)
    save_full(art, f"{OUT}/piring.webp", size=(380, 380), quality=84)
    gold, gm = gold_seams(W, H, lines, 6.5, nx())
    gold[..., 3] *= body
    preview(over(art.copy(), gold), "ki-piring-emas", tone=CREAM)
    save_full(gold, f"{OUT}/emas.webp", size=(380, 380), quality=86)

if "mangkuk" in PARTS:
    W, H = 640, 470
    nx = Seq(2100); rng = random.Random(21)
    cx = 320
    top, bot = 70, 400
    # chawan silhouette: wide mouth, gently rounded walls, small foot
    left = [(cx - 250, top), (cx - 246, top + 90), (cx - 226, top + 190), (cx - 180, top + 270), (cx - 110, bot - 28)]
    right = [(W - x, y) for x, y in reversed(left)]
    body = shapes(W, H, [left + [(cx, bot - 16)] + right])
    foot = shapes(W, H, [[(cx - 80, bot - 34), (cx + 80, bot - 34), (cx + 72, bot + 4), (cx - 72, bot + 4)]])
    mouth = shapes(W, H, [ellipse_pts(cx, top + 2, 244, 22, 40)])
    inner = shapes(W, H, [ellipse_pts(cx, top + 5, 232, 16, 40)])
    art = blank(W, H)
    art = over(art, tint(np.roll(gaussian_filter(np.maximum(body, foot), 14), 18, 0) * 0.35, "#3a332b"))
    art = GP(art, foot, "#a77e58", "#7f5b3c", seed=nx(), rough=1.2, streak=0.6)
    art = OV(art, foot * fbm(W, H, 5, 6, 2), lambda q: tint(q, "#5c4029", 0.4))
    b = gouache_paint(np.maximum(body, mouth), CHAR, CHAR_D, seed=nx(), rough=1.2, streak=0.9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = np.clip(0.75 + 0.5 * np.cos((xx - cx + 60) / 300 * 1.4), 0.55, 1.2)
    b[..., :3] *= shade[..., None]
    art = over(art, b)
    # nuka glaze drips from the rim (pale blue-grey, translucent)
    drips = []
    for k in range(9):
        x = cx - 220 + k * 55 + rng.uniform(-14, 14)
        ln = rng.uniform(60, 170)
        drips.append(petal_pts(x, top + 10, ln, rng.uniform(26, 44), math.pi / 2, n=12))
    drip = np.clip(shapes(W, H, drips) * body + mouth * 0.0, 0, 1)
    band = np.clip(body * (yy < top + 60), 0, 1)
    art = G(art, np.maximum(drip, band), "#a9b2b0", "#7d8a8c", seed=nx(), density=0.65, edge=0.8, bloom=0.5, gran=0.5, rough=4, feather=2)
    # interior: darker, seen through the mouth
    art = OV(art, inner, lambda q: gouache_paint(q, "#24221f", "#171614", seed=31, rough=0.6, streak=0.4))
    art = G(art, np.clip(mouth - inner, 0, 1), "#c3c8c2", seed=nx(), density=0.55, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
    # highlight
    hl = strokes(W, H, [(curve([(cx - 210, top + 70), (cx - 196, top + 160), (cx - 160, top + 230)], 20), 10, (0.3, 0.5))])
    art = G(art, hl * body, "#f4f1ea", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2, feather=4)
    clear()
    lines = [(crack((cx - 60, top - 2), (cx + 30, bot - 40), rng, n=14, jit=0.25), 1.0),
             (crack((cx + 180, top + 10), (cx + 120, top + 200), rng, n=8, jit=0.25), 0.8),
             (crack((cx - 30, top + 150), (cx - 150, top + 230), rng, n=6, jit=0.3), 0.6)]
    gold, gm = gold_seams(W, H, lines, 7, nx())
    gold[..., 3] *= np.maximum(body, mouth)
    art = over(art, gold)
    preview(art, "ki-mangkuk", tone=CREAM)
    save(art, f"{OUT}/mangkuk.webp", max_w=360, quality=84)

if "tinta" in PARTS:
    W, H = 900, 320
    nx = Seq(3100); rng = random.Random(31)
    art = blank(W, H)
    # layered sumi washes: a low, soft horizon of ink, darker where strokes overlap
    for k, (y, amp, col, den) in enumerate([(150, 40, "#b7b2aa", 0.5), (190, 34, "#8e8982", 0.55), (230, 26, "#5e5a55", 0.6)]):
        pts = [(-20, H + 20)]
        for x in np.linspace(-20, W + 20, 26):
            pts.append((x, y - amp * (0.5 + 0.5 * math.sin(x / (140 + k * 40) + k * 1.7)) - rng.uniform(0, amp * 0.4)))
        pts.append((W + 20, H + 20))
        m = shapes(W, H, [pts])
        fadev = np.clip((np.mgrid[0:H, 0:W][0] - (y - amp)) / 90, 0, 1).astype(np.float32)
        art = G(art, m * (1 - fadev * 0.55), col, seed=nx(), density=den, edge=0.7, bloom=0.6, gran=0.5, rough=8, feather=4)
        clear()
    preview(art, "ki-tinta", tone=CREAM)
    save_full(art, f"{OUT}/tinta.webp", size=(560, 199), quality=76)

if "retak" in PARTS:
    W, H = 640, 90
    nx = Seq(4100); rng = random.Random(41)
    main = crack((30, 46), (610, 44), rng, n=22, jit=0.05)
    br = [(crack(main[7], (main[7][0] + 50, main[7][1] - 26), rng, 5, 0.2), 0.5), (crack(main[14], (main[14][0] + 44, main[14][1] + 24), rng, 5, 0.2), 0.5)]
    gold, gm = gold_seams(W, H, [(main, 1.0)] + br, 5, nx())
    preview(gold, "ki-retak", tone=CREAM)
    save(gold, f"{OUT}/retak.webp", max_w=320, quality=86)

if "pecahan" in PARTS:
    W = H = 160
    nx = Seq(5100); rng = random.Random(51)
    pts = [(30, 40), (110, 22), (140, 90), (96, 138), (34, 118)]
    m = shapes(W, H, [pts], smooth=False)
    art = GP(blank(W, H), m, GLAZE, GLAZE_D, seed=nx(), rough=0.8)
    art = OV(art, crackle(W, H, m, 3, n=30, width=0.8) * 0.3, lambda q: tint(q, "#7c705e"))
    edge = np.clip(gaussian_filter(m, 2.0) * 2 - 1.2, 0, 1)
    edge = np.clip(m - edge, 0, 1)
    art = FO(art, np.clip(edge * 1.6, 0, 1), GOLD, seed=nx(), emboss=0.8)
    preview(art, "ki-pecahan", tone=CREAM)
    save(art, f"{OUT}/pecahan.webp", max_w=64, quality=86)

if "kertas" in PARTS:
    N = 512
    base = np.array(hex_rgb(CREAM), np.float32)
    f1 = wrap_noise(N, N, 5, 1.0); f2 = wrap_noise(N, N, 6, 24); f3 = wrap_noise(N, N, 8, (0.5, 7))
    rgb = base[None, None] * (1 + (f1[..., None] - 0.5) * 0.035 + (f2[..., None] - 0.5) * 0.018 + (f3[..., None] - 0.5) * 0.03)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((N, N, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/kertas.webp", size=(256, 256), quality=74)
