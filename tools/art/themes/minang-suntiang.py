"""Minang Suntiang — the tall layered gold suntiang bridal headdress as an object (no face) on red velvet, songket
balapak band, a bungo spray divider, a single bungo flower, velvet tile.
Run: python3 -I minang-suntiang.py [part ...]  parts: suntiang songket spray bungo velvet"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k1_lib import *  # noqa
from scipy.ndimage import map_coordinates

OUT = outdir("minang-suntiang")
PARTS = sys.argv[1:] or ["suntiang", "songket", "spray", "bungo", "velvet"]
RED, RED_D, RED_L = "#8e1018", "#4e070c", "#b81d24"
GOLD, GOLD_L, GOLD_D = "#d4a640", "#f0d27e", "#8f6a1e"


def flower_poly(cx, cy, r, n, rot, inner=0.42):
    """n-petal flower outline (rounded petals)."""
    pts = []
    m = n * 6
    for i in range(m):
        t = i / m * math.tau
        k = (math.cos(n * (t + rot) / 1) + 1) / 2
        rr = r * (inner + (1 - inner) * k ** 0.7)
        pts.append((cx + math.cos(t) * rr, cy + math.sin(t) * rr))
    return pts


def gold_layer(art, m, base=GOLD, seed=1, emboss=0.8, sparkle=0.2, shade=0.0):
    art = FO(art, m, base, seed=seed, emboss=emboss, sparkle=sparkle)
    if shade:
        art = OV(art, m, lambda mm: flat(mm, "#3a1206", shade))
    return art


# ------------------------------------------------------------------ the suntiang
if "suntiang" in PARTS:
    W, H = 860, 600
    nx = Seq(30100); rng = random.Random(7)
    art = blank(W, H)
    cx, by = W / 2, 470
    # soft shadow of the whole fan on the velvet
    fan = shapes(W, H, [[(cx + math.cos(a) * 390, by + math.sin(a) * 400) for a in np.linspace(math.pi * 1.02, math.pi * 1.98, 40)] + [(cx + 300, by + 30), (cx - 300, by + 30)]])
    art = G(art, gaussian_filter(fan, 18) * 0.9, "#22040a", seed=nx(), density=0.55, edge=0, bloom=0, rough=4, feather=8)
    tiers = [  # (radius, flowers, flower r, spread start, spread end, shade)
        (380, 23, 20, 1.03, 1.97, 0.38), (340, 21, 22, 1.05, 1.95, 0.3), (296, 19, 23, 1.07, 1.93, 0.22),
        (250, 17, 24, 1.09, 1.91, 0.15), (204, 15, 25, 1.12, 1.88, 0.08), (158, 12, 26, 1.15, 1.85, 0.03), (112, 9, 26, 1.2, 1.8, 0.0),
    ]
    for ti, (R, n, fr, a0, a1, shade) in enumerate(tiers):
        clear()
        stems, petals, leaves, gems = [], [], [], []
        for k in range(n):
            a = math.pi * (a0 + (a1 - a0) * (k + 0.5 * (ti % 2) * 0) / (n - 1))
            a += rng.uniform(-0.012, 0.012)
            rr = R * rng.uniform(0.97, 1.03)
            fx, fy = cx + math.cos(a) * rr, by + math.sin(a) * rr * 0.98
            # spring stem: wavy wire from the base band toward the flower
            sx, sy = cx + math.cos(a) * 40, by + math.sin(a) * 30
            mid = ((sx + fx) / 2 + math.cos(a + 1.57) * rng.uniform(-8, 8), (sy + fy) / 2 + math.sin(a + 1.57) * rng.uniform(-8, 8))
            stems.append((curve([(sx, sy), mid, (fx, fy)], 20), 2.2 if ti < 3 else 2.6, None))
            s_ = fr * rng.uniform(0.9, 1.1)
            petals.append(flower_poly(fx, fy, s_, 5 if (k + ti) % 3 else 6, rng.uniform(0, 1)))
            gems.append((fx, fy, s_ * 0.24))
            # small gold leaves flanking each flower
            for side in (-1, 1):
                la = a + side * 0.5 + math.pi
                leaves.append(petal_pts(fx + math.cos(a + math.pi) * s_ * 0.8, fy + math.sin(a + math.pi) * s_ * 0.8, s_ * 1.1, s_ * 0.36, la, n=10))
        st = strokes(W, H, stems)
        lv = shapes(W, H, leaves)
        pt = shapes(W, H, petals)
        gm = circles(W, H, gems)
        art = gold_layer(art, st, GOLD_D, seed=nx(), emboss=0.4, sparkle=0.05, shade=shade * 0.8)
        art = gold_layer(art, lv, mix(GOLD, GOLD_D, 0.35), seed=nx(), emboss=0.9, sparkle=0.1, shade=shade)
        # petal outline engraving: darker rim gives each bungo its form
        art = gold_layer(art, pt, GOLD, seed=nx(), emboss=1.0, sparkle=0.3, shade=shade * 0.7)
        art = OV(art, inner_edge(pt, 3) * 0.5, lambda mm: flat(mm, GOLD_D, 0.8))
        # petal veins
        vein = []
        for p in petals:
            fx0 = sum(q[0] for q in p) / len(p); fy0 = sum(q[1] for q in p) / len(p)
            for q in p[::6]:
                vein.append(([(fx0, fy0), (fx0 + (q[0] - fx0) * 0.75, fy0 + (q[1] - fy0) * 0.75)], 1.1, (0.1, 0.4)))
        art = OV(art, strokes(W, H, vein) * pt, lambda mm: flat(mm, GOLD_D, 0.55))
        art = GP(art, gm, RED_L, RED_D, seed=nx(), rough=0.4, pad=6) if ti % 2 == 0 else gold_layer(art, gm, GOLD_L, seed=nx(), emboss=1.2, sparkle=0.6)
        art = OV(art, circles(W, H, [(x - r * 0.3, y - r * 0.3, r * 0.3) for x, y, r in gems]), lambda mm: flat(mm, "#fff4d0", 0.75))
    # base band (laca) across the brow with a row of kote-kote dangles
    clear()
    band = shapes(W, H, [[(cx - 300, by - 6), (cx - 150, by - 26), (cx, by - 32), (cx + 150, by - 26), (cx + 300, by - 6), (cx + 300, by + 22), (cx + 150, by + 4), (cx, by - 2), (cx - 150, by + 4), (cx - 300, by + 22)]])
    art = GP(art, band, RED_D, "#2a0306", seed=nx(), rough=0.8, pad=8)
    art = gold_layer(art, np.maximum(outline(band, 4), inner_edge(band, 3)), GOLD, seed=nx(), emboss=0.9, sparkle=0.2)
    bead = []
    for k in range(-14, 15):
        t = k / 14
        x = cx + t * 292; y = by - 30 * (1 - t * t) ** 0.8 + 12
        bead.append((x, y, 5.2))
    art = gold_layer(art, circles(W, H, bead), GOLD_L, seed=nx(), emboss=1.1, sparkle=0.4)
    chains, drops = [], []
    for k in range(-13, 14):
        t = k / 13.5
        x = cx + t * 286; y0 = by + 8 - 22 * (1 - t * t) ** 0.8 + 14
        L = 40 + 22 * (1 - abs(t)) + (8 if k % 2 == 0 else 0)
        chains.append(([(x, y0), (x, y0 + L)], 1.6, None))
        drops.append(petal_pts(x, y0 + L - 4, 18, 7, math.pi / 2, n=10))
    art = gold_layer(art, strokes(W, H, chains), GOLD_D, seed=nx(), emboss=0.4, sparkle=0.05)
    dm = shapes(W, H, drops)
    art = gold_layer(art, dm, GOLD, seed=nx(), emboss=1.1, sparkle=0.35)
    art = OV(art, circles(W, H, [(d[len(d) // 2][0], d[len(d) // 2][1] - 4, 2.4) for d in drops]), lambda mm: flat(mm, "#fff2c8", 0.8))
    # side pendants (long strands falling at the temples)
    for side in (-1, 1):
        x0 = cx + side * 306
        strand = strokes(W, H, [(curve([(x0, by + 8), (x0 + side * 8, by + 60), (x0 + side * 4, by + 118)], 20), 2.2, None)])
        art = gold_layer(art, strand, GOLD_D, seed=nx(), emboss=0.4)
        bl = shapes(W, H, [flower_poly(x0 + side * 4, by + 124, 15, 6, 0.3)])
        art = gold_layer(art, bl, GOLD, seed=nx(), emboss=1.0, sparkle=0.3)
        art = GP(art, circles(W, H, [(x0 + side * 4, by + 124, 4.4)]), RED_L, RED_D, seed=nx(), rough=0.3, pad=6)
    prev(art, "ms-suntiang", bg=RED)
    save(art, f"{OUT}/suntiang.webp", max_w=700, quality=82)
    clear()


# ------------------------------------------------------------------ songket balapak band (horizontally seamless)
if "songket" in PARTS:
    Wt, Ht = 480, 120
    cell = 3  # weave grid: motif edges step like supplementary-weft gold
    def draw(cv):
        p = skia.Paint(AntiAlias=False, Color=skia.ColorWHITE)
        for ox in (-Wt, 0, Wt):
            # border lines
            for y in (6, 12, Ht - 14, Ht - 8):
                cv.c.drawRect(skia.Rect(ox, y, ox + Wt, y + 3), p)
            # pucuak rabuang (bamboo shoot) triangles top and bottom
            for k in range(12):
                x = ox + k * 40
                cv.c.drawPath(poly_path([(x + 2, 18), (x + 38, 18), (x + 20, 44)]), p)
                cv.c.drawPath(poly_path([(x + 2, Ht - 18), (x + 38, Ht - 18), (x + 20, Ht - 44)]), p)
            # central lozenge row (saik galamai) with a star in each
            for k in range(6):
                x = ox + k * 80 + 40
                cv.c.drawPath(poly_path([(x, 46), (x + 26, 60), (x, 74), (x - 26, 60)]), p)
                for k2 in (-1, 1):
                    xx = x + 40 * k2 * 0 + 40 if k2 > 0 else None
                xx = x + 40
                for dx, dy in ((0, -9), (9, 0), (0, 9), (-9, 0)):
                    cv.c.drawRect(skia.Rect(xx + dx - 3, 60 + dy - 3, xx + dx + 3, 60 + dy + 3), p)
                cv.c.drawRect(skia.Rect(xx - 2, 58, xx + 2, 62), p)
    m = mask_from(Wt, Ht, draw)
    # remove lozenge centres (red eye) for a woven look
    def eyes(cv):
        p = skia.Paint(AntiAlias=False, Color=skia.ColorWHITE)
        for ox in (-Wt, 0, Wt):
            for k in range(6):
                x = ox + k * 80 + 40
                cv.c.drawPath(poly_path([(x, 53), (x + 12, 60), (x, 67), (x - 12, 60)]), p)
            for k in range(12):
                x = ox + k * 40
                cv.c.drawPath(poly_path([(x + 12, 22), (x + 28, 22), (x + 20, 34)]), p)
                cv.c.drawPath(poly_path([(x + 12, Ht - 22), (x + 28, Ht - 22), (x + 20, Ht - 34)]), p)
    m = np.clip(m - mask_from(Wt, Ht, eyes), 0, 1)
    # quantize to the weave grid
    small = m[::cell, ::cell]
    m = np.kron(small, np.ones((cell, cell), np.float32))[:Ht, :Wt]
    yy, xx = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    weft = 0.78 + 0.22 * (np.sin(yy / cell * math.pi) ** 2)            # horizontal gold threads
    warp = 0.9 + 0.1 * (np.sin(xx / cell * math.pi * 0.5) ** 2)
    v = wrap_noise(Wt, Ht, 5, 10)
    gold = np.array(hex_rgb(GOLD), np.float32)
    sheen = 0.8 + 0.35 * np.sin(xx / Wt * math.tau * 2 + v * 2)[..., None]
    red = np.array(hex_rgb(RED), np.float32) * (0.85 + 0.25 * v)[..., None] * (0.9 + 0.1 * warp[..., None])
    gm = np.clip(gold * sheen * weft[..., None], 0, 1)
    rgb = red * (1 - m[..., None]) + gm * m[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((Ht, Wt, 1), np.float32)], -1)
    prev(np.concatenate([arr, arr], 1), "ms-songket")
    save_full(arr, f"{OUT}/songket.webp", quality=82)


# ------------------------------------------------------------------ bungo spray divider
if "spray" in PARTS:
    W, H = 520, 120
    nx = Seq(30300); rng = random.Random(3)
    art = blank(W, H)
    cx, cy = W / 2, 60
    stems, leaves, fl = [], [], []
    for side in (-1, 1):
        pts = curve([(cx, cy), (cx + side * 80, cy - 10), (cx + side * 160, cy + 8), (cx + side * 230, cy - 4)], 40)
        stems.append((pts, 2.4, (0.0, 0.6)))
        for j in range(6, 40, 7):
            px, py = pts[j]
            up = -1 if (j // 7) % 2 else 1
            leaves.append(petal_pts(px, py, 22, 7, side * (0.4 if side > 0 else 0) + (math.pi if side < 0 else 0) + up * -0.9, n=10))
            fl.append(flower_poly(px + side * 6, py + up * -14, 8, 5, rng.uniform(0, 1)))
    st = strokes(W, H, stems)
    art = gold_layer(art, st, GOLD_D, seed=nx(), emboss=0.5)
    art = gold_layer(art, shapes(W, H, leaves), mix(GOLD, GOLD_D, 0.3), seed=nx(), emboss=0.9, sparkle=0.1)
    art = gold_layer(art, shapes(W, H, fl), GOLD, seed=nx(), emboss=1.0, sparkle=0.3)
    big = shapes(W, H, [flower_poly(cx, cy, 30, 6, 0.2)])
    art = gold_layer(art, big, GOLD, seed=nx(), emboss=1.1, sparkle=0.4)
    art = OV(art, inner_edge(big, 3) * 0.6, lambda mm: flat(mm, GOLD_D, 0.8))
    art = GP(art, circles(W, H, [(cx, cy, 8)]), RED_L, RED_D, seed=nx(), rough=0.3, pad=6)
    prev(art, "ms-spray", bg=RED)
    save(art, f"{OUT}/spray.webp", max_w=300, quality=84)


if "bungo" in PARTS:
    W, H = 200, 200
    nx = Seq(30400)
    art = blank(W, H)
    lv = shapes(W, H, [petal_pts(100, 100, 92, 22, a, n=10) for a in np.linspace(0, math.tau, 7)[:-1] + 0.26])
    art = gold_layer(art, lv, mix(GOLD, GOLD_D, 0.4), seed=nx(), emboss=0.9)
    f = shapes(W, H, [flower_poly(100, 100, 62, 6, 0.0)])
    art = gold_layer(art, f, GOLD, seed=nx(), emboss=1.1, sparkle=0.35)
    art = OV(art, inner_edge(f, 4) * 0.6, lambda mm: flat(mm, GOLD_D, 0.8))
    vein = [([(100, 100), (100 + math.cos(a) * 52, 100 + math.sin(a) * 52)], 2.0, (0.1, 0.4)) for a in np.linspace(0, math.tau, 13)[:-1]]
    art = OV(art, strokes(W, H, vein) * f, lambda mm: flat(mm, GOLD_D, 0.5))
    art = GP(art, circles(W, H, [(100, 100, 17)]), RED_L, RED_D, seed=nx(), rough=0.4, pad=6)
    art = OV(art, circles(W, H, [(95, 95, 5)]), lambda mm: flat(mm, "#fff2c8", 0.8))
    prev(art, "ms-bungo", bg=RED)
    save(art, f"{OUT}/bungo.webp", max_w=120, quality=84)


if "velvet" in PARTS:
    n = 256
    v = wrap_noise(n, n, 3, 1.6) * 0.45 + wrap_noise(n, n, 4, 14) * 0.55
    base = np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#7a0c14"), np.float32)
    base *= (0.78 + 0.44 * v)[..., None]
    arr = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_full(arr, f"{OUT}/velvet.webp", quality=70)
