"""Imlek Keluarga — a family reunion dinner for Chinese New Year: glowing red paper lanterns with gold caps and tassels,
an ink-and-wash meihua (plum blossom) branch, mandarin oranges with leaves, a round red papercut window-flower
(jianzhi) medallion, a reunion table seen from above (lazy susan, whole fish, dumplings, noodles, oranges, bowls and
chopsticks), a gold auspicious-cloud ornament and a rice-paper tile. No deities, no zodiac idols.
Run: python3 -I imlek-keluarga.py [part ...]   parts: lantern plum oranges papercut table cloud paper
Assets -> public/themes/art/imlek-keluarga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g6_lib import *  # noqa

OUT = outdir("imlek-keluarga")
PARTS = sys.argv[1:] or ["lantern", "plum", "oranges", "papercut", "table", "cloud", "paper"]
RED, RED2, DEEP, GOLD = "#c4161c", "#d4252a", "#6e0a10", "#d8a640"
CREAM = "#f6eedd"


def cloud_pts(cx, cy, s, flip=1):
    """Xiangyun: a double spiral cloud curl as a polyline (for strokes)."""
    a = spiral_pts(cx - s * 0.9 * flip, cy, 2, s * 0.55, 0, 1.3, 30, flip)
    b = spiral_pts(cx + s * 0.5 * flip, cy - s * 0.25, 2, s * 0.42, math.pi, 1.2, 26, -flip)
    return a, b


if "lantern" in PARTS:
    W, H = 240, 470
    nx = Seq(64100); rng = random.Random(641)
    art = lantern(blank(W, H), W, H, 120, 110, 92, 108, nx, rng, red=RED, red2=RED2, deep=DEEP, gold=GOLD, glow_amt=0.8)
    art = edge_fade(art, 10)
    preview(art, "ik-lantern", bg=CREAM)
    save_full(art, f"{OUT}/lantern.webp", size=(120, 235), quality=82)
    clear()

if "plum" in PARTS:
    W, H = 760, 520
    nx = Seq(64200); rng = random.Random(642)
    art = blank(W, H)
    main = [(-10, 470), (90, 420), (200, 390), (300, 330), (380, 300), (470, 220), (560, 170), (680, 120), (770, 96)]
    art = ink_branch(art, W, H, curve(main, 80), 17, nx)
    twigs = [
        [(200, 390), (230, 330), (250, 270), (300, 230)],
        [(300, 330), (360, 360), (430, 380), (520, 372)],
        [(470, 220), (480, 150), (520, 90)],
        [(560, 170), (620, 200), (700, 210)],
        [(380, 300), (400, 250), (440, 200)],
        [(90, 420), (120, 470), (150, 505)],
    ]
    for tw in twigs:
        art = ink_branch(art, W, H, curve(tw, 30), rng.uniform(5, 8), nx, dry=0.25)
    clear()
    # knots: dark dots of ink
    knots = circles(W, H, [(p[0] + rng.uniform(-3, 3), p[1] + rng.uniform(-3, 3), rng.uniform(3, 5)) for p in main[1:-1:2]])
    art = G(art, knots, "#1a1210", seed=nx(), density=0.95, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    spots = [(300, 230, 22), (250, 270, 18), (520, 372, 20), (430, 380, 17), (520, 90, 20), (480, 150, 16), (700, 210, 19), (620, 200, 15),
             (440, 200, 18), (400, 250, 14), (150, 505, 15), (360, 360, 13), (680, 120, 16), (560, 170, 14), (230, 330, 13), (760, 96, 14)]
    for i, (x, y, r) in enumerate(spots):
        if i % 4 == 3:
            # bud: a small closed round with a red calyx
            b = circles(W, H, [(x, y, r * 0.7)])
            art = G(art, b, "#e7a2aa", "#c84a5a", seed=nx(), density=0.9, edge=0.6, bloom=0, rough=0.8, feather=0.6, pad=8)
        else:
            art = blossom(art, W, H, x, y, r * 1.6, nx, rng, petal="#fbeff0", petal2="#eba8b2", heart="#c23a4a")
        if i % 5 == 4:
            clear()
    preview(art, "ik-plum", tone=CREAM)
    save(art, f"{OUT}/plum.webp", max_w=380, quality=82)
    clear()

if "oranges" in PARTS:
    W, H = 420, 300
    nx = Seq(64300); rng = random.Random(643)
    art = blank(W, H)
    sh = ellipses(W, H, [(210, 268, 180, 18, 0)])
    art = OV(art, sh, lambda mm: col_arr(mm, "#5a2a10", np.clip(gaussian_filter(mm, 10), 0, 1) * 0.35), pad=30)
    for x, y, r in ((128, 196, 70), (292, 200, 66), (210, 140, 64)):
        art = mandarin(art, W, H, x, y, r, nx, rng)
        clear()
    preview(art, "ik-oranges", tone=CREAM)
    save(art, f"{OUT}/oranges.webp", max_w=210, quality=84)
    clear()

if "papercut" in PARTS:
    # red window-flower: a disc with cut-out petals, cloud curls and a plain centre for the typeset 福
    W = H = 560
    nx = Seq(64400); rng = random.Random(644)
    cx = cy = W / 2
    disc = circles(W, H, [(cx, cy, 262)])
    cuts = []
    ring = np.clip(circles(W, H, [(cx, cy, 250)]) - circles(W, H, [(cx, cy, 242)]), 0, 1)
    ring2 = np.clip(circles(W, H, [(cx, cy, 128)]) - circles(W, H, [(cx, cy, 120)]), 0, 1)
    polys = []
    for k in range(12):
        a = k * math.tau / 12
        polys.append(petal_pts(cx + math.cos(a) * 150, cy + math.sin(a) * 150, 70, 18, a, 14))
    for k in range(12):
        a = (k + 0.5) * math.tau / 12
        polys.append(ellipse_pts(cx + math.cos(a) * 214, cy + math.sin(a) * 214, 12, 12, 10))
        # five-petal plum cut in the outer band
        for j in range(5):
            b = a + j * math.tau / 5
            polys.append(ellipse_pts(cx + math.cos(a) * 186 + math.cos(b) * 9, cy + math.sin(a) * 186 + math.sin(b) * 9, 6, 6, 8))
    cm = shapes(W, H, polys)
    curls = []
    for k in range(12):
        a = k * math.tau / 12
        px, py = cx + math.cos(a) * 232, cy + math.sin(a) * 232
        curls.append((spiral_pts(px, py, 1, 8, a, 1.2, 18, 1), 2.6, None))
    clm = strokes(W, H, curls)
    holes = np.clip(cm + ring + ring2 + clm, 0, 1)
    m = np.clip(disc - holes, 0, 1)
    m = np.clip(m + circles(W, H, [(cx, cy, 116)]), 0, 1)  # solid centre
    art = cutpaper(blank(W, H), m, RED, seed=nx(), shadow=0.28, torn=0.0, edge=1.0, grain=1.2, sdx=3, sdy=5, sblur=4)
    # gold foil centre ring
    gr = np.clip(circles(W, H, [(cx, cy, 108)]) - circles(W, H, [(cx, cy, 100)]), 0, 1)
    art = FO(art, gr, GOLD, seed=nx(), emboss=0.5, sparkle=0.05)
    preview(art, "ik-papercut", tone=CREAM)
    save(art, f"{OUT}/papercut.webp", max_w=280, quality=82)
    clear()

if "table" in PARTS:
    # the reunion table from above
    W = H = 680
    nx = Seq(64500); rng = random.Random(645)
    cx = cy = W / 2
    art = blank(W, H)
    sh = circles(W, H, [(cx + 8, cy + 12, 318)])
    art = OV(art, sh, lambda mm: col_arr(mm, "#3a1008", np.clip(gaussian_filter(mm, 14), 0, 1) * 0.4), pad=40)
    cloth = shapes(W, H, [deform(ellipse_pts(cx, cy, 316, 316, 40), rng, 1, 0.004)])
    art = GP(art, cloth, "#b3131b", "#c01c22", seed=nx(), rough=0.8, streak=0.6)
    art = tint(art, side_light(cloth, 10, 12, 30), "#5a0a0e", 0.45, seed=nx())
    # embroidered gold rim on the cloth
    rimm = np.clip(circles(W, H, [(cx, cy, 300)]) - circles(W, H, [(cx, cy, 294)]), 0, 1)
    art = FO(art, rimm, GOLD, seed=nx(), emboss=0.3, sparkle=0.03)
    # lazy susan (glass turntable)
    ls = circles(W, H, [(cx, cy, 170)])
    art = OV(art, ls, lambda mm: col_arr(mm, "#f4e8e0", mm * 0.28), pad=6)
    art = OV(art, np.clip(ls - circles(W, H, [(cx, cy, 166)]), 0, 1), lambda mm: col_arr(mm, "#ffffff", mm * 0.6), pad=4)
    # place settings: 8 bowls + chopsticks + small saucers
    for k in range(8):
        a = k * math.tau / 8 + math.pi / 8
        bx, by = cx + math.cos(a) * 240, cy + math.sin(a) * 240
        plate = circles(W, H, [(bx, by, 38)])
        art = GP(art, plate, "#fbf6ee", "#f1e8da", seed=nx(), rough=0.4)
        art = tint(art, side_light(plate, 3, 4, 3), "#9a8a7a", 0.4, seed=nx())
        bowl = np.clip(circles(W, H, [(bx, by, 24)]) - circles(W, H, [(bx, by, 20)]), 0, 1)
        art = FO(art, np.clip(circles(W, H, [(bx, by, 26)]) - circles(W, H, [(bx, by, 24)]), 0, 1), "#2f6a7a", seed=nx(), emboss=0.2, sparkle=0)
        art = tint(art, circles(W, H, [(bx, by, 20)]), "#e8dccb", 0.6, seed=nx())
        ca, sa = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
        rx, ry = math.cos(a), math.sin(a)
        ox, oy = bx + ca * 50, by + sa * 50
        sticks = [([(ox + rx * 30 + ca * d, oy + ry * 30 + sa * d), (ox - rx * 30 + ca * d * 0.5, oy - ry * 30 + sa * d * 0.5)], 3.6, (0.0, 0.3)) for d in (-4, 4)]
        st = strokes(W, H, sticks)
        art = GP(art, st, "#e9d6b0", "#dcc49a", seed=nx(), rough=0.3)
        art = tint(art, side_light(st, 1, 2, 1), "#7a5a3a", 0.5, seed=nx())
        tips = strokes(W, H, [([(ox + rx * 30 + ca * d, oy + ry * 30 + sa * d), (ox + rx * 16 + ca * d, oy + ry * 16 + sa * d)], 3.8, None) for d in (-4, 4)])
        art = FO(art, tips, GOLD, seed=nx(), emboss=0.2, sparkle=0)
        clear() if k % 3 == 2 else None
    # centre: whole steamed fish on an oval plate
    plate = ellipses(W, H, [(cx, cy - 10, 108, 52, -8)])
    art = GP(art, plate, "#fbf6ee", "#f1e8da", seed=nx(), rough=0.4)
    art = tint(art, side_light(plate, 3, 5, 4), "#9a8a7a", 0.4, seed=nx())
    art = FO(art, np.clip(plate - ellipses(W, H, [(cx, cy - 10, 100, 46, -8)]), 0, 1), "#2f6a7a", seed=nx(), emboss=0.2, sparkle=0)
    fish = rot_poly([(cx - 78, cy - 10), (cx - 50, cy - 34), (cx + 30, cy - 30), (cx + 58, cy - 12), (cx + 86, cy - 32), (cx + 80, cy - 10), (cx + 88, cy + 12), (cx + 58, cy - 6), (cx + 30, cy + 12), (cx - 50, cy + 14)], cx, cy - 10, -0.14)
    fm = shapes(W, H, [fish])
    art = GP(art, fm, "#c8a070", "#b08858", seed=nx(), rough=0.5)
    art = tint(art, side_light(fm, 0, 6, 5), "#5a3a1a", 0.55, seed=nx())
    scales = stripes(W, H, 1.2, 1.0, 5, seed=nx()) * fm
    art = tint(art, scales, "#8a6a40", 0.25, seed=nx())
    eye = circles(W, H, [(cx - 60, cy - 6, 4)])
    art = GP(art, eye, "#2a1a10", seed=nx(), rough=0.2)
    # scallion and chilli shreds on the fish
    sc = [([(cx - 30 + i * 12, cy - 22 + rng.uniform(-4, 4)), (cx - 22 + i * 12, cy - 4 + rng.uniform(-4, 4))], 2.2, None) for i in range(7)]
    art = GP(art, strokes(W, H, sc), "#5a9a3a", "#6aaa44", seed=nx(), rough=0.2)
    art = GP(art, strokes(W, H, [([(cx - 10, cy - 16), (cx + 6, cy - 12)], 2.2, None), ([(cx + 20, cy - 20), (cx + 30, cy - 8)], 2.2, None)]), "#d8301c", seed=nx(), rough=0.2)
    clear()
    # dumplings, noodles, oranges, a soup tureen on the turntable
    dishes = [(cx - 112, cy + 92, "dumpling"), (cx + 112, cy + 92, "noodle"), (cx, cy + 122, "orange"), (cx - 124, cy - 76, "greens"), (cx + 124, cy - 76, "soup")]
    for x, y, kind in dishes:
        p = circles(W, H, [(x, y, 46)])
        art = GP(art, p, "#fbf6ee", "#f1e8da", seed=nx(), rough=0.4)
        art = tint(art, side_light(p, 3, 4, 3), "#9a8a7a", 0.4, seed=nx())
        art = FO(art, np.clip(p - circles(W, H, [(x, y, 41)]), 0, 1), "#2f6a7a", seed=nx(), emboss=0.2, sparkle=0)
        if kind == "dumpling":
            for j in range(5):
                a = j * math.tau / 5
                d = shapes(W, H, [deform(ellipse_pts(x + math.cos(a) * 18, y + math.sin(a) * 18, 15, 10, 10, a + 1.57), rng, 1, 0.02)])
                art = GP(art, d, "#f4ecd8", "#e8dcc0", seed=nx(), rough=0.4)
                art = tint(art, side_light(d, 2, 3, 2), "#a89068", 0.5, seed=nx())
        elif kind == "noodle":
            items = [(spiral_pts(x + rng.uniform(-6, 6), y + rng.uniform(-6, 6), 2, 30, rng.uniform(0, 6), 2.2, 50, rng.choice((1, -1))), 2.4, None) for _ in range(5)]
            art = GP(art, strokes(W, H, items) * circles(W, H, [(x, y, 38)]), "#e8c070", "#d8a850", seed=nx(), rough=0.2)
            art = GP(art, circles(W, H, [(x - 10, y - 8, 6), (x + 12, y + 6, 5)]), "#c84a2a", seed=nx(), rough=0.3)
        elif kind == "orange":
            for j, (ox, oy) in enumerate(((-15, 6), (15, 6), (0, -14))):
                art = mandarin(art, W, H, x + ox, y + oy, 15, nx, rng, leaf=(j == 2))
        elif kind == "greens":
            for j in range(9):
                a = rng.uniform(0, math.tau)
                lm = shapes(W, H, [petal_pts(x + rng.uniform(-10, 10), y + rng.uniform(-10, 10), 26, 9, a, 12)])
                art = GP(art, lm, "#3e7a3a", "#4a8a42", seed=nx(), rough=0.4)
                art = tint(art, side_light(lm, 2, 2, 2), "#1a3a1a", 0.4, seed=nx())
        else:
            soup = circles(W, H, [(x, y, 36)])
            art = GP(art, soup, "#d8a050", "#c89040", seed=nx(), rough=0.3)
            art = tint(art, circles(W, H, [(x - 8, y - 10, 6), (x + 10, y + 4, 4), (x - 2, y + 12, 5)]), "#fff0c0", 0.6, seed=nx())
        clear()
    art = add_grain(art, nx(), 0.03)
    preview(art, "ik-table", tone=CREAM)
    save(art, f"{OUT}/table.webp", max_w=340, quality=82)
    clear()

if "cloud" in PARTS:
    W, H = 420, 110
    nx = Seq(64600); rng = random.Random(646)
    items = []
    for sgn in (-1, 1):
        a, b = cloud_pts(210 + sgn * 120, 58, 34, sgn)
        items += [(a, 5, (0.05, 0.4)), (b, 4.4, (0.05, 0.4))]
        items.append(([(210 + sgn * 22, 58), (210 + sgn * 80, 60), (210 + sgn * 150, 76), (210 + sgn * 196, 72)], 3.4, (0.1, 0.6)))
    dm = shapes(W, H, [[(210, 36), (230, 58), (210, 80), (190, 58)]], smooth=False)
    m = np.clip(strokes(W, H, items) + dm, 0, 1)
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.6, sparkle=0.04)
    art = tint(art, side_light(m, 2, 2, 1.5), "#6a4a12", 0.4, seed=nx())
    preview(art, "ik-cloud", tone=CREAM)
    save(art, f"{OUT}/cloud.webp", max_w=210, quality=84)
    clear()

if "paper" in PARTS:
    n = 256
    nx = Seq(64700)
    base = np.array(hex_rgb(CREAM), np.float32)
    mot = wrap_noise(n, n, nx(), 30)
    fib = wrap_noise(n, n, nx(), 0.7)
    # long rice-paper fibres
    rs = np.random.default_rng(9)
    f = np.zeros((n, n), np.float32)
    for _ in range(90):
        x, y = rs.uniform(0, n, 2); a = rs.uniform(0, math.pi); L = rs.uniform(10, 40)
        for t in np.linspace(0, 1, int(L)):
            f[int(y + math.sin(a) * L * t) % n, int(x + math.cos(a) * L * t) % n] = 1
    f = gaussian_filter(f, 0.5, mode="wrap") * 1.5
    rgb = base[None, None] * (1 + (mot[..., None] - 0.5) * 0.06 + (fib[..., None] - 0.5) * 0.04) * (1 - np.clip(f, 0, 0.6)[..., None] * 0.08)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_texture(arr, f"{OUT}/paper.webp", quality=72)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")
