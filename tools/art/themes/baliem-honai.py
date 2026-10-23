"""Baliem Honai — the Baliem valley in the Papuan highlands: layered misty ridges, the valley floor of raised
sweet-potato garden beds and drainage ditches with the river winding through, a cluster of round thatched honai with
plank walls and a stake fence, a hand-knotted noken bag with natural and dyed fibre stripes, a sweet-potato vine sprig
and a drifting mist wash. Landscape and objects only (no people). Original, inspired-by drawings.
Run: python3 -I baliem-honai.py [part ...]   parts: valley honai noken ubi mist
Assets -> public/themes/art/baliem-honai/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h3_lib import *  # noqa

OUT = outdir("baliem-honai")
PARTS = sys.argv[1:] or ["valley", "honai", "noken", "ubi", "mist"]
MIST = "#e8ece8"
THATCH, THATCH_D, THATCH_L = "#a9844c", "#5e4524", "#d8bb7e"
WOOD, WOOD_D = "#6a4630", "#3a2418"


def ridge(W, H, y, amp, seed, rough=1.0, peaks=5):
    rng = random.Random(seed)
    pts = [(-20, H + 20)]
    ph = [rng.uniform(0, 6) for _ in range(3)]
    for x in range(-20, W + 21, 8):
        v = (math.sin(x / W * math.pi * peaks * 0.5 + ph[0]) * 0.55 + math.sin(x / W * math.pi * peaks * 1.3 + ph[1]) * 0.3
             + math.sin(x / W * math.pi * peaks * 3.1 + ph[2]) * 0.15 * rough)
        pts.append((x, y - amp * v + rng.uniform(-2, 2) * rough))
    pts.append((W + 20, H + 20))
    return shapes(W, H, [pts], smooth=False)


if "valley" in PARTS:
    W, H = 640, 1100
    nx = Seq(81000); rng = random.Random(810)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#eef0ec"), (0.3, "#e3e8e5"), (0.5, "#d9e0dc"), (1, "#d9e0dc")], seed=811, streak=0.8)
    layers = [(470, 150, "#b9c5c9", "#c6d0d0", 2.4), (550, 120, "#9aacb1", "#aab9b8", 3.0), (625, 85, "#6e8984", "#7e9787", 3.6), (690, 50, "#4b6b55", "#587a56", 4.4)]
    for i, (y, amp, c1, c2, pk) in enumerate(layers):
        m = ridge(W, H, y, amp, 812 + i, rough=1.0, peaks=pk)
        art = G(art, m, c1, c2, seed=nx(), density=0.95, edge=0.45, bloom=0.3, rough=4, feather=1.4)
        if i >= 2:  # forest texture on the nearer ridges
            sh = m * np.clip((fbm(W, H, 820 + i, 26, 4) - 0.5) * 2.2, 0, 1)
            art = G(art, sh, mix(c1, "#1f3a2c", 0.5), seed=nx(), density=0.5, edge=0.5, bloom=0.2, rough=3, feather=1)
        # mist lying in the valleys between ridges
        band = np.exp(-((yy - (y + amp * 0.55)) / (34 + i * 8)) ** 2) * (0.6 + 0.4 * fbm(W, H, 830 + i, 90, 3))
        art = OV(art, band, lambda mm: col_arr(mm, "#f4f6f2", mm * 0.85), pad=0)
        clear()
    # valley floor
    floor = (yy > 712).astype(np.float32)
    art = G(art, floor, "#7a9a58", "#6a8c4e", seed=nx(), density=0.95, edge=0.2, bloom=0.3, rough=3)
    # raised garden beds in perspective: rows of irregular plots, ditches between them
    beds, fallow, ditches = [], [], []
    y = 716.0; row = 0
    while y < 930:
        hgt = (6 + (y - 712) * 0.11) * rng.uniform(0.7, 1.5)
        x = rng.uniform(-60, 0); step = 30 + (y - 712) * 0.5
        while x < W + 40:
            wdt = step * rng.uniform(0.5, 1.8)
            sk = rng.uniform(-0.4, 0.4) * hgt
            poly = [(x + rng.uniform(-2, 2), y + hgt), (x + sk, y + rng.uniform(-1.5, 1.5)), (x + wdt + sk, y + rng.uniform(-1.5, 1.5)), (x + wdt + rng.uniform(-2, 2), y + hgt)]
            r_ = rng.random()
            (fallow if r_ < 0.14 else beds).append(poly)
            if rng.random() < 0.7:
                ditches.append(([(x + wdt, y + hgt), (x + wdt + sk, y)], 0.8 + (y - 712) * 0.008, (0.2, 0.2)))
            x += wdt + 2
        if rng.random() < 0.8:
            ditches.append(([(-10, y + hgt + 1), (W * 0.5, y + hgt + rng.uniform(-2, 2)), (W + 10, y + hgt + 1)], 0.8 + (y - 712) * 0.01, (0.1, 0.1)))
        y += hgt + 2.5; row += 1
    bm = shapes(W, H, beds, smooth=False) * floor
    sel = [b_ for k, b_ in enumerate(beds) if k % 3 == 0]
    art = G(art, bm * np.clip(fbm(W, H, 840, 60, 3) * 1.4, 0, 1), "#9cbd64", "#86ac56", seed=nx(), density=0.55, edge=0.5, bloom=0.3, rough=1.5, feather=0.8)
    art = G(art, shapes(W, H, sel, smooth=False) * floor, "#5f8a44", "#4a7440", seed=nx(), density=0.6, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
    fm = shapes(W, H, fallow, smooth=False) * floor
    art = G(art, fm, "#9a6a44", "#7a5236", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.5, feather=0.8)
    dm = strokes(W, H, ditches) * floor
    art = G(art, dm, "#3f5a34", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1, feather=0.6)
    # leaf texture dabs on beds (sweet potato foliage)
    dabs = [(rng.uniform(0, W), rng.uniform(716, 930), 0, 0, 0) for _ in range(700)]
    dabs = [(x, y, 1.5 + (y - 712) * 0.014, 1 + (y - 712) * 0.009, rng.uniform(-30, 30)) for x, y, *_ in dabs]
    art = G(art, ellipses(W, H, dabs) * bm, "#557d3e", "#6c9248", seed=nx(), density=0.5, edge=0.4, bloom=0, rough=1, feather=0.5)
    clear()
    # the river: a silver ribbon winding through
    rv = curve([(-20, 742), (120, 734), (260, 752), (350, 778), (290, 820), (420, 858), (560, 884), (680, 912)], 80)
    rvm = strokes(W, H, [(rv, 9, (0.4, 0.05))]) * floor
    art = G(art, rvm, "#c8d6d6", "#a9bfc4", seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=2, feather=0.8)
    art = OV(art, strokes(W, H, [(rv[::2], 2, (0.4, 0.1))]) * floor, lambda m: col_arr(m, "#f4f8f6", m * 0.6))
    # low mist over the far valley floor
    lowm = np.exp(-((yy - 722) / 22) ** 2) * (0.5 + 0.5 * fbm(W, H, 850, 80, 3))
    art = OV(art, lowm, lambda mm: col_arr(mm, "#f2f4ef", mm * 0.75), pad=0)
    # foreground: grass bank and red earth path
    fg = shapes(W, H, [[(-20, H + 20), (-20, 940), (120, 920), (300, 930), (480, 912), (W + 20, 925), (W + 20, H + 20)]])
    art = G(art, fg, "#4f7038", "#3d5c30", seed=nx(), density=0.95, edge=0.4, bloom=0.3, rough=5)
    pc = curve([(330, H + 20), (300, 1040), (350, 990), (330, 950), (360, 925)], 40)
    path = strokes(W, H, [(pc, 70, (0.9, 0.0))])
    art = G(art, path * fg, "#a46a44", "#8a5638", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=5)
    grass = fibre_strokes(rng, 0, 920, W, H, 520, 16, -math.pi / 2, 0.45, (1.2, 2.4))
    art = G(art, strokes(W, H, grass) * np.clip(fg - path * 0.8, 0, 1), "#2e4a26", "#6a8f42", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    art = add_grain(art, 852, 0.03)
    preview(art, "bh-valley")
    save_rgb(art, f"{OUT}/valley.webp", size=(640, 1100), quality=76)
    clear()


def honai(art, W, H, cx, base, r, wall_h, nx, rng, light=-1):
    """One honai: round plank wall, low door, domed thatch roof with a hanging fringe."""
    ry = r * 0.28
    wall = shapes(W, H, [[(cx - r, base - wall_h)] + [(cx + math.cos(a) * r, base + math.sin(a) * ry) for a in np.linspace(math.pi, 0, 24)] + [(cx + r, base - wall_h)]], smooth=False)
    art = GP(art, wall, WOOD, "#7a5236", seed=nx(), rough=1.5, streak=0.8)
    n = np.clip((np.mgrid[0:H, 0:W][1] - cx) / r, -1, 1).astype(np.float32)
    art = shade(art, wall, 1 + 0.25 * (-n * light) - 0.12)
    planks = []
    for k in range(-9, 10):
        t = k / 10 * math.pi / 2
        x = cx + math.sin(t) * r
        planks.append(([(x, base - wall_h), (x + rng.uniform(-1, 1), base + math.cos(t) * ry)], 1.4, None))
    art = G(art, strokes(W, H, planks) * wall, WOOD_D, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    door = shapes(W, H, [[(cx - r * 0.13, base + ry * 0.9), (cx - r * 0.12, base - wall_h * 0.55), (cx + r * 0.12, base - wall_h * 0.55), (cx + r * 0.13, base + ry * 0.9)]], smooth=False)
    art = GP(art, door, "#1e130c", "#2a1a10", seed=nx(), rough=1)
    # roof: dome wider than the wall, fringe edge
    rr = r * 1.18; top = base - wall_h - r * 1.05
    eave = base - wall_h + r * 0.12
    pts = [(cx - rr, eave)]
    for a in np.linspace(math.pi, 2 * math.pi, 40):
        pts.append((cx + math.cos(a) * rr, eave + math.sin(a) * (eave - top)))
    fringe = []
    for x in np.linspace(cx + rr, cx - rr, 46):
        fringe.append((x, eave + ry * 0.9 * math.sqrt(max(0, 1 - ((x - cx) / rr) ** 2)) + rng.uniform(-2, 10)))
    roof = shapes(W, H, [pts + fringe], smooth=False)
    roof = np.clip(roof + circles(W, H, [(cx, top + 2, r * 0.1)]), 0, 1)
    art = GP(art, roof, THATCH, "#8a6a3a", seed=nx(), rough=2.5, streak=1.0)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nr = np.clip((xx - cx) / rr, -1, 1)
    vr = np.clip((eave - yy) / (eave - top), 0, 1)
    lit = np.clip(0.8 + nr * 0.45 * light + np.sqrt(vr) * 0.25 - 0.25, 0, 1.2)
    art = shade(art, roof, 0.62 + 0.55 * lit)
    # thatch fibres flowing down the dome
    fib = []
    for _ in range(int(r * 4.2)):
        a = rng.uniform(math.pi * 1.04, math.pi * 1.96)
        t0 = rng.uniform(0.0, 0.85)
        x0 = cx + math.cos(a) * rr * t0; y0 = eave + math.sin(a) * (eave - top) * math.sqrt(max(0, 1 - t0 * t0))
        L = rng.uniform(14, 34) * r / 120
        dx = math.cos(a) * 0.35
        fib.append(([(x0, y0), (x0 + dx * L, y0 + L * 0.6), (x0 + dx * L * 1.4, y0 + L)], rng.uniform(1.0, 2.2), (0.1, 0.6)))
    fm = strokes(W, H, fib) * roof
    half = len(fib) // 2
    art = G(art, strokes(W, H, fib[:half]) * roof, THATCH_D, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    art = OV(art, strokes(W, H, fib[half:]) * roof, lambda m: col_arr(m, THATCH_L, m * 0.5))
    # shadow under the eave onto the wall
    sh = wall * (1 - roof) * np.clip(1 - (yy - eave) / (r * 0.3), 0, 1)
    art = shade(art, sh, 0.55)
    return art


if "honai" in PARTS:
    W, H = 760, 470
    nx = Seq(82000); rng = random.Random(820)
    art = blank(W, H)
    gr = ellipses(W, H, [(380, 430, 380, 34, 0)])
    art = G(art, gr, "#5c7a3e", "#7a6a3e", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=6)
    art = G(art, ellipses(W, H, [(380, 432, 260, 18, 0)]), "#9a6a44", seed=nx(), density=0.5, edge=0.4, bloom=0.3, rough=5)
    art = honai(art, W, H, 170, 392, 88, 70, nx, rng)
    clear()
    art = honai(art, W, H, 600, 388, 84, 66, nx, rng)
    clear()
    art = honai(art, W, H, 385, 420, 128, 96, nx, rng)
    clear()
    # stake fence in front
    stakes = []
    for k, x in enumerate(np.linspace(20, 740, 44)):
        if 300 < x < 470:
            continue
        top = 400 - rng.uniform(0, 14) - (8 if k % 3 == 0 else 0)
        stakes.append(([(x + rng.uniform(-1, 1), 452), (x + rng.uniform(-2, 2), top)], rng.uniform(3.2, 4.6), (0.02, 0.1)))
    bind = [([(20, 424), (300, 428)], 2.0, None), ([(470, 428), (740, 424)], 2.0, None), ([(20, 438), (300, 441)], 1.6, None), ([(470, 441), (740, 438)], 1.6, None)]
    fm = strokes(W, H, stakes)
    art = G(art, fm, "#4a3020", "#6e4a30", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.8, feather=0.5)
    art = G(art, strokes(W, H, bind), "#3a2618", seed=nx(), density=0.85, edge=0.2, bloom=0, rough=0.5, feather=0.4)
    # grass tufts
    gs = fibre_strokes(rng, 0, 436, W, 462, 160, 12, -math.pi / 2, 0.5, (1.2, 2.2))
    art = G(art, strokes(W, H, gs), "#3a5a2a", "#6a8a42", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.4)
    art = add_grain(art, 821, 0.025)
    preview(art, "bh-honai", bg=MIST)
    save(art, f"{OUT}/honai.webp", max_w=560, quality=84)
    clear()

if "noken" in PARTS:
    W, H = 380, 520
    nx = Seq(83000); rng = random.Random(830)
    cx = 190
    # sack outline: narrow mouth at y=150, round belly, bottom 500
    def hw(y):
        return np.interp(y, [150, 220, 320, 420, 470, 500], [110, 140, 158, 150, 120, 40])
    body = shapes(W, H, [[(cx - float(hw(y)), y) for y in range(150, 501, 10)] + [(cx + float(hw(y)), y) for y in range(500, 149, -10)]])
    # knotted loop mesh in coloured rows
    rows = list(range(156, 500, 13))
    cols_by_row = []
    pal = [("#c49a5e", "#a07a44"), ("#c49a5e", "#a07a44"), ("#a8452c", "#86331f"), ("#c49a5e", "#a07a44"), ("#d9a832", "#b88a22"), ("#c49a5e", "#a07a44"), ("#6a3a68", "#4e2a4e")]
    masks = {}
    for i, y in enumerate(rows):
        key = pal[(i // 2) % len(pal)]
        w = float(hw(y))
        n = max(4, int(w * 2 / 13))
        off = 6.5 if i % 2 else 0
        items = []
        for j in range(n + 1):
            x = cx - w + j * (2 * w / n) + off
            if x > cx + w:
                continue
            items.append(([(x - 6, y), (x - 4, y + 8), (x, y + 12), (x + 4, y + 8), (x + 6, y)], 2.6, None))
        masks.setdefault(key, []).extend(items)
    art = blank(W, H)
    # inside of the bag seen through the mesh (dark)
    art = G(art, body, "#3a2a1c", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=3)
    for (c1, c2), items in masks.items():
        m = strokes(W, H, items) * body
        art = GP(art, m, c1, c2, seed=nx(), rough=0.6, streak=0.9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = np.clip((xx - cx) / np.maximum(hw(yy), 1), -1, 1)
    art = shade(art, body, 1.05 - 0.35 * np.clip(n, 0, 1) - 0.15 * np.clip((yy - 380) / 120, 0, 1))
    # rim cord and strap with a wooden peg
    rim = strokes(W, H, [([(cx - 112, 152), (cx, 146), (cx + 112, 152)], 7, None)])
    strap = strokes(W, H, [(curve([(cx - 104, 152), (cx - 120, 90), (cx - 60, 36), (cx, 26), (cx + 60, 36), (cx + 120, 90), (cx + 104, 152)], 50), 8, None)])
    hole = strokes(W, H, [(curve([(cx - 92, 150), (cx - 104, 96), (cx - 54, 50), (cx, 42), (cx + 54, 50), (cx + 104, 96), (cx + 92, 150)], 50), 3, None)])
    cord = np.clip(rim + strap, 0, 1)
    art = GP(art, cord, "#b48a52", "#8a6a3c", seed=nx(), rough=0.8, streak=1.0)
    tw = []
    for k in range(60):
        t = k / 59
        p = curve([(cx - 104, 152), (cx - 120, 90), (cx - 60, 36), (cx, 26), (cx + 60, 36), (cx + 120, 90), (cx + 104, 152)], 60)[k]
        tw.append(([(p[0] - 3, p[1] - 2), (p[0] + 3, p[1] + 2)], 1.2, None))
    art = G(art, strokes(W, H, tw) * strap, "#5a4022", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.4)
    peg = shapes(W, H, [[(cx - 30, 22), (cx + 30, 20), (cx + 30, 30), (cx - 30, 31)]], smooth=False)
    art = GP(art, peg, "#5a3c26", "#6e4a30", seed=nx(), rough=0.8)
    art = add_grain(art, 831, 0.03)
    preview(art, "bh-noken", bg=MIST)
    save(art, f"{OUT}/noken.webp", max_w=190, quality=84)
    clear()

if "ubi" in PARTS:
    W, H = 640, 150
    nx = Seq(84000); rng = random.Random(840)
    vine = curve([(30, 90), (140, 70), (240, 92), (320, 78), (400, 90), (500, 70), (610, 88)], 80)
    art = G(blank(W, H), strokes(W, H, [(vine, 3.2, (0.2, 0.2))]), "#5a6a2c", "#7a5a3a", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    leaves = []
    for i, (x, y, a) in enumerate(along(vine, 48)):
        if x < 60 or x > 590:
            continue
        side = -1 if i % 2 else 1
        ang = a + side * (1.1 + rng.uniform(-0.2, 0.2))
        L = rng.uniform(34, 46) * (1 - abs(x - 320) / 700)
        lx, ly = x + math.cos(ang) * L * 0.55, y + math.sin(ang) * L * 0.55
        # heart-shaped leaf (classic heart curve), tip pointing away from the vine
        pts = []
        for t in np.linspace(0, math.tau, 48):
            hx = 16 * math.sin(t) ** 3
            hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((hx * L / 34, -(hy - 4) * L / 26))
        lx, ly = x + math.cos(ang) * L * 0.15, y + math.sin(ang) * L * 0.15
        ca, sa = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
        poly = [(lx + px * ca - py * sa, ly + px * sa + py * ca) for px, py in pts]
        leaves.append((poly, (x, y), (lx, ly), ang))
    for k, (poly, st, c, ang) in enumerate(leaves):
        m = shape_mask(W, H, poly)
        art = G(art, m, "#6e9a48", "#4c7a3a", seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=1.6, feather=0.8, pad=10)
        if k % 3 == 0:
            art = G(art, m * np.clip(fbm(W, H, 845 + k, 18, 2) - 0.4, 0, 1) * 2, "#7a4a6a", seed=nx(), density=0.35, edge=0.3, bloom=0, rough=1, feather=0.6, pad=10)
        vein = strokes(W, H, [([st, c, (c[0] + math.cos(ang) * 12, c[1] + math.sin(ang) * 12)], 1.2, (0.1, 0.5))])
        art = G(art, vein * m + strokes(W, H, [([st, c], 1.6, None)]) * (1 - m), "#3a5a2a", seed=nx(), density=0.7, edge=0.1, bloom=0, rough=0.4, feather=0.4, pad=6)
        if k % 2:
            clear()
    preview(art, "bh-ubi", tone=MIST)
    save(art, f"{OUT}/ubi.webp", max_w=320, quality=84)
    clear()

if "mist" in PARTS:
    W, H = 900, 220
    nx = Seq(85000); rng = random.Random(850)
    m = ellipses(W, H, [(rng.uniform(60, 840), rng.uniform(80, 140), rng.uniform(80, 190), rng.uniform(26, 50), rng.uniform(-4, 4)) for _ in range(14)])
    m = gaussian_filter(m, 14) * (0.55 + 0.45 * fbm(W, H, 851, 60, 3))
    art = col_arr(m, "#f7f8f4", np.clip(m * 1.1, 0, 0.9))
    art = edge_fade(art, 120, "lr")
    preview(art, "bh-mist", bg="#6f8a86")
    save_full(art, f"{OUT}/mist.webp", size=(450, 110), quality=70)
    clear()
