"""Muna Kaghati — gouache: the kaghati kolope of Muna (a kite of dried kolope leaves stitched with bamboo pins over a
bamboo frame, nanas-fibre string, a bowed kamumu hummer on top), flying over the coral coast and karst hills of Muna;
soft day clouds; tenun Muna weft stripes (thread level) as a tile; a single dried kolope leaf; a string divider.
Run: python3 -I muna-kaghati.py [part ...]  parts: kite coast clouds tenun leaf divider
Assets -> public/themes/art/muna-kaghati/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i2_lib import *  # noqa

OUT = outdir("muna-kaghati")
PARTS = sys.argv[1:] or ["kite", "coast", "clouds", "tenun", "leaf", "divider"]
LEAF_T = ["#c99a5b", "#b78445", "#d6ad6e", "#a9733a", "#c48d4c", "#dcb97f"]
LEAF_D, BAMBOO, BAMBOO_D = "#6e4520", "#d9c08a", "#8c6a34"
STRING = "#efe3c4"
SEA_L, SEA, SEA_D, REEF = "#7fd3cf", "#2ea5b5", "#1b6e8f", "#4e9a8a"
SAND, SAND_D = "#efe0bd", "#cdb88f"
KARST, KARST_D, KARST_L = "#5d8c5a", "#3c6844", "#8db374"
TEN = {"red": "#b3262a", "mar": "#6d1a2a", "ora": "#e0782a", "yel": "#f0c23c", "grn": "#2f7a4f", "ind": "#2c3a6e", "blk": "#1e1716", "wht": "#efe6d2", "pur": "#6b3a73"}


def kite():
    W, H = 720, 980
    rng = random.Random(7); nx = Seq(700)
    cx = W / 2
    top, left, right, bot = (cx, 150), (cx - 300, 430), (cx + 300, 430), (cx, 900)

    def edge(a, b, bulge, n=24):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nxv, nyv = dy / L, -dx / L
        return [(a[0] + dx * t + nxv * bulge * L * math.sin(math.pi * t), a[1] + dy * t + nyv * bulge * L * math.sin(math.pi * t)) for t in np.linspace(0, 1, n)]
    outline = edge(top, right, 0.07) + edge(right, bot, 0.05)[1:] + edge(bot, left, 0.05)[1:] + edge(left, top, 0.07)[1:]
    body = shapes(W, H, [deform(outline, rng, 1, 0.002)], smooth=False)
    art = blank(W, H)
    # soft shadow (kite is a translucent leaf membrane; a faint drop shadow lifts it off the sky)
    sh = np.roll(np.roll(gaussian_filter(body, 10), 14, 0), 10, 1)
    art = twash(art, sh, "#1d4f6b", 0.18, seed=nx())
    # leaf panels: rows of overlapping dried leaves, each its own tan, with curved parallel veins
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for row, y in enumerate(np.arange(130, 930, 62)):
        x = 40 + (row % 2) * 40 - 60
        while x < W:
            wl = rng.uniform(80, 120); hl = rng.uniform(70, 96)
            pts = ellipse_pts(x + wl / 2, y + hl / 2, wl * 0.58, hl * 0.62, 14, rng.uniform(-0.25, 0.25))
            m = shapes(W, H, [deform(pts, rng, 2, 0.04)]) * body
            if m.max() > 0.1:
                col = rng.choice(LEAF_T)
                art = GP(art, m, col, mix(col, "#7a4a22", 0.18), seed=nx(), rough=1.6, streak=1.2)
                # veins: arcs radiating from the leaf base
                items = []
                bx, by = x + wl * 0.5, y + hl * 1.02
                for k in range(-3, 4):
                    a0 = -math.pi / 2 + k * 0.32
                    pts_v = [(bx + math.cos(a0 + 0.12 * k * s_) * hl * s_ * 1.05, by + math.sin(a0 + 0.12 * k * s_) * hl * s_ * 1.05) for s_ in np.linspace(0.05, 1, 10)]
                    items.append((pts_v, 1.4, (0.0, 0.5)))
                vm = strokes(W, H, items) * m
                art = twash(art, vm, "#7a4a22", 0.35, seed=nx())
                # overlapped lower edge: darker rim where the next leaf tucks under
                rim = np.clip(m - gaussian_filter(m, 3), 0, 1) * 2
                art = twash(art, rim, LEAF_D, 0.5, seed=nx())
                # sun through the leaf: warm translucent glow in the middle
                art = twash(art, m * rad(W, H, x + wl * 0.45, y + hl * 0.4, wl * 0.5), "#f6d79a", 0.22, seed=nx())
            x += wl * rng.uniform(0.82, 0.95)
        trim_cache()
    # stitching: short bamboo pins along row seams
    pins = []
    for y in np.arange(150, 930, 62):
        for x in np.arange(60, W - 40, rng.uniform(26, 34)):
            px, py = x + rng.uniform(-4, 4), y + rng.uniform(-3, 3)
            a = rng.uniform(-0.3, 0.3)
            pins.append(([(px - 7 * math.cos(a), py - 7 * math.sin(a)), (px + 7 * math.cos(a), py + 7 * math.sin(a))], 2.0, (0.2, 0.2)))
    pm = strokes(W, H, pins) * body
    art = GP(art, pm, "#eadbb0", seed=nx(), rough=0.4)
    # whole-kite light: lit from the upper left, darker toward the lower right
    art = twash(art, body * lin(W, H, 140, 200, 600, 860), "#5a3618", 0.28, seed=nx())
    art = twash(art, body * (1 - lin(W, H, 140, 200, 520, 700)), "#fbe6b8", 0.18, seed=nx())
    # edge binding (fibre cord around the rim)
    rim = np.clip(body - gaussian_filter(body, 2.2), 0, 1) * 3
    art = twash(art, np.clip(rim, 0, 1), "#5b3a1c", 0.75, seed=nx())
    # bamboo frame: vertical spine and the bowed cross spar
    spine = [(cx + rng.uniform(-1, 1), y) for y in np.linspace(120, 930, 30)]
    spar = [(x, 420 - 60 * (1 - ((x - cx) / 330) ** 2)) for x in np.linspace(cx - 330, cx + 330, 40)]
    fr = strokes(W, H, [(spine, 9, (0.03, 0.05)), (spar, 8, (0.05, 0.05))])
    art = GP(art, fr, BAMBOO, mix(BAMBOO, "#ffffff", 0.2), seed=nx(), rough=0.8)
    art = twash(art, np.clip(fr - np.roll(fr, -3, 1), 0, 1), BAMBOO_D, 0.6, seed=nx())
    nodes = strokes(W, H, [([(cx - 6, y), (cx + 6, y)], 2.2, None) for y in (260, 520, 760)])
    art = twash(art, nodes, BAMBOO_D, 0.8, seed=nx())
    # kamumu hummer: a bow above the top with a taut leaf ribbon
    bow = [(cx + 250 * math.sin(t), 112 - 70 * math.cos(t) + 70) for t in np.linspace(-1.2, 1.2, 40)]
    bw = strokes(W, H, [(bow, 6, (0.05, 0.05))])
    art = GP(art, bw, BAMBOO, seed=nx(), rough=0.6)
    art = twash(art, np.clip(bw - np.roll(bw, -2, 0), 0, 1), BAMBOO_D, 0.5, seed=nx())
    rib = strokes(W, H, [([bow[0], (cx, 88), bow[-1]], 4.0, None)])
    art = GP(art, rib, "#d4a965", seed=nx(), rough=0.6)
    # bridle strings converging below the kite, to the flying line
    knot = (cx + 40, 620)
    br = strokes(W, H, [([(cx, 260), knot], 1.6, None), ([(cx, 820), knot], 1.6, None)])
    art = GP(art, br, STRING, seed=nx(), rough=0.3)
    line = strokes(W, H, [(curve([knot, (cx + 150, 760), (cx + 260, 900), (W - 2, H - 2)], 40), 2.0, None)])
    art = GP(art, line, STRING, seed=nx(), rough=0.3)
    preview(art, "kite", bg="#8fcbe0")
    print("kite", save(art, f"{OUT}/kite.webp", max_w=360, quality=82))
    clear()


def palm(art, W, H, px, py, ph, lean, rng, nx, s=1.0):
    trunk = curve([(px, py), (px + lean * ph * 0.25, py - ph * 0.55), (px + lean * ph, py - ph)], 40)
    tm = strokes(W, H, [(trunk, 13 * s, (0.0, 0.35))])
    art = GP(art, tm, "#8f6f4c", "#b0906a", seed=nx(), rough=1.0, streak=1.2)
    art = twash(art, tm * lin(W, H, px - 10, 0, px + 14, 0), "#4f3a28", 0.35, seed=nx())
    rings = strokes(W, H, [([(x - 7 * s, y), (x + 7 * s, y + 1.5)], 1.4, None) for x, y in trunk[2::2]]) * tm
    art = twash(art, rings, "#4f3a28", 0.55, seed=nx())
    tx, ty = trunk[-1]
    back, front = [], []
    for j, a in enumerate(np.linspace(-math.pi * 1.02, 0.02, 9)):
        a += rng.uniform(-0.08, 0.08)
        L = rng.uniform(95, 135) * s
        droop = 30 + 40 * abs(math.cos(a))
        pts = curve([(tx, ty), (tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.45 - 10 * s), (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.3 + droop * s)], 24)
        items = [(pts, 4.5 * s, (0.0, 0.7))]
        for i in range(2, 23):
            x0, y0 = pts[i]
            x1, y1 = pts[min(i + 1, 23)]
            dx, dy = x1 - x0, y1 - y0
            Ld = math.hypot(dx, dy) + 1e-6
            ln = (26 - i * 0.7) * s
            for sgn in (-1, 1):
                nxv, nyv = -dy / Ld * sgn, dx / Ld * sgn
                items.append(([(x0, y0), (x0 + (nxv * 0.45 + dx / Ld * 0.5) * ln, y0 + (nyv * 0.45 + dy / Ld * 0.5) * ln + ln * 0.55)], 3.2 * s, (0.0, 0.85)))
        (back if j % 2 else front).append(items)
    for grp, cols in ((back, ("#2f6538", "#3f7a44")), (front, ("#4b8a4a", "#6aa457"))):
        fm = strokes(W, H, [it for items in grp for it in items])
        art = GP(art, fm, cols[0], cols[1], seed=nx(), rough=1.2, streak=0.8)
        art = twash(art, fm * rad(W, H, tx - 20, ty - 30, 90 * s), "#9cc56d", 0.3, seed=nx())
    nuts = circles(W, H, [(tx + rng.uniform(-8, 8) * s, ty + rng.uniform(2, 10) * s, 6 * s) for _ in range(4)])
    art = GP(art, nuts, "#6a5a2a", "#8a7a3a", seed=nx(), rough=0.6)
    return art


def coast():
    W, H = 780, 640
    rng = random.Random(11); nx = Seq(1100)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    def karst_ridge(base, amp, cone_w, seed_off):
        """Rolling limestone hills: a row of rounded cones of varying height (Muna karst)."""
        pts = [(-30, base + 400)]
        x = -30
        while x < W + 60:
            w = cone_w * rng.uniform(0.6, 1.4); h = amp * rng.uniform(0.45, 1.0)
            for a in np.linspace(math.pi, 0, 10):
                pts.append((x + w / 2 + math.cos(a) * w / 2, base - h * math.sin(a) ** 0.7))
            x += w * rng.uniform(0.7, 0.95)
        pts.append((W + 60, base + 400))
        return shapes(W, H, [pts])
    # farthest ridge: blue-grey, hazed
    r1 = karst_ridge(215, 70, 90, 1) * (yy < 330)
    art = GP(art, r1, "#9db9b6", "#b3cbc6", seed=nx(), rough=2.2)
    art = twash(art, r1 * lin(W, H, 0, 150, 0, 230), "#dcebea", 0.25, seed=nx())
    haze = np.exp(-((yy - 236) / 14) ** 2) * (0.6 + 0.4 * fbm(W, H, nx(), 60, 3))
    art = twash(art, haze * np.clip(gaussian_filter(r1, 4) * 2, 0, 1), "#eef6f6", 0.6, seed=nx())
    # middle ridge: green-blue forest with texture
    r2 = karst_ridge(268, 85, 120, 2) * (yy < 330)
    art = GP(art, r2, "#6f9a80", "#87ad8c", seed=nx(), rough=2.4)
    art = brushwork(art, r2, ["#6a9579", "#7aa384", "#73a07f"], rng, nx, n=700, L=(5, 10), wd=(2, 4), ang=-0.9, ang_var=0.8)
    art = twash(art, r2 * np.clip(gaussian_filter(np.roll(r2, 10, 1) * 1.0, 6) - gaussian_filter(r2, 6) + 0.5, 0, 1) * 0, "#000000", 0, seed=nx())
    art = twash(art, r2 * lin(W, H, 0, 300, 0, 200), "#dbeae6", 0.28, seed=nx())
    # sea from the horizon (y=300) to the beach
    hz = 300
    sea = rect(W, H, -10, hz, W + 10, 500)
    art = GP(art, sea, "#1d6f92", "#23809f", seed=nx(), rough=0.6)
    art = twash(art, sea * lin(W, H, 0, hz + 20, 0, 470), "#5cc6c6", 0.85, seed=nx(), col2="#78d6cf")
    reef = ellipses(W, H, [(rng.uniform(-20, W), rng.uniform(390, 470), rng.uniform(30, 90), rng.uniform(5, 11), rng.uniform(-6, 6)) for _ in range(18)])
    art = twash(art, displace(reef, nx(), 8, 18) * sea, "#3c8f86", 0.5, seed=nx())
    waves = []
    for _ in range(70):
        y = rng.uniform(hz + 4, 470); t = (y - hz) / 170
        x = rng.uniform(-20, W); L = rng.uniform(10, 40) * (0.4 + t)
        waves.append(([(x, y), (x + L * 0.5, y - 1.2), (x + L, y)], 1.0 + 1.6 * t, (0.3, 0.3)))
    art = twash(art, strokes(W, H, waves) * sea, "#e9fbf8", 0.55, seed=nx())
    art = twash(art, sun_glints(W, H, 220, hz + 3, hz + 60, 40, rng, spread=80) * sea, "#fffbe8", 0.8, seed=nx())
    # coral-limestone headland on the right: raised reef cliff, undercut notch at the waterline, forest on top
    head = [(462, 474), (474, 440), (486, 400), (500, 372), (530, 344), (570, 322), (620, 306), (680, 296), (740, 290), (W + 20, 286), (W + 20, 480)]
    hm = shapes(W, H, [deform(head, rng, 3, 0.012)])
    art = GP(art, hm, "#cfc4a6", "#e2d8bc", seed=nx(), rough=3.0, streak=1.2)
    # light from the upper left: the seaward face is lit, the cliff darkens to the right and toward its foot
    art = twash(art, hm * lin(W, H, 470, 330, 760, 460), "#8d8166", 0.38, seed=nx())
    vdir = lambda x, y: math.pi / 2 + 0.15 * math.sin(x / 23)
    art = brushwork(art, hm, ["#b8ab8c", "#e4dbc2", "#a39678", "#d3c8ab"], rng, nx, n=320, L=(14, 40), wd=(2, 5), dir_fn=vdir, ang_var=0.12)
    crev = np.clip((fbm(W, H, nx(), 9, 3) - 0.62) * 3, 0, 1) * np.clip(gaussian_filter(np.random.default_rng(3).random((H, W)).astype(np.float32), (9, 1.2)) * 6 - 2.6, 0, 1)
    art = twash(art, crev * hm, "#6a604c", 0.5, seed=nx())
    notch_pts = [(462, 470), (520, 464), (600, 460), (700, 458), (W + 20, 456)]
    notch = strokes(W, H, [(curve(notch_pts, 30), 16, (0.1, 0.0))]) * hm
    art = twash(art, displace(notch, nx(), 4, 10), "#3f3a30", 0.7, seed=nx())
    top = [(484, 408), (498, 374), (530, 346), (570, 324), (620, 308), (680, 298), (740, 292), (W + 20, 288), (W + 20, 330), (740, 326), (680, 334), (630, 342), (590, 352), (548, 368), (512, 392)]
    tpm = displace(shapes(W, H, [deform(top, rng, 2, 0.03)]), nx(), 8, 12)
    art = GP(art, tpm, "#3b6a43", "#4c7f4e", seed=nx(), rough=3.0)
    art = brushwork(art, tpm, ["#2c5535", "#4b8050", "#3b6a43", "#6d9c5c"], rng, nx, n=520, L=(5, 10), wd=(3, 6), ang=-0.6, ang_var=1.4)
    art = twash(art, tpm * lin(W, H, 500, 290, 520, 400), "#1f3d26", 0.3, seed=nx())
    # creepers hanging over the cliff lip
    hang = [([(x, 330 + (x - 500) * -0.08), (x + rng.uniform(-3, 3), 330 + (x - 500) * -0.08 + rng.uniform(10, 34))], rng.uniform(2, 4), (0.0, 0.7)) for x in np.arange(500, W, 12)]
    art = GP(art, strokes(W, H, hang) * (1 - tpm * 0.0), "#3f7046", seed=nx(), rough=0.8)
    # little outrigger boat
    hull = shapes(W, H, [[(300, 352), (346, 352), (339, 359), (306, 359)]], smooth=False)
    art = GP(art, hull, "#7a4b2c", seed=nx(), rough=0.5)
    art = GP(art, shapes(W, H, [[(320, 350), (321, 318), (340, 348)]], smooth=False), "#f4ead6", seed=nx(), rough=0.5)
    art = GP(art, strokes(W, H, [([(296, 362), (350, 362)], 1.6, None)]), "#5a3a22", seed=nx(), rough=0.3)
    # beach: white coral sand, foam scallop, rubble and shells
    edge_y = lambda x: 486 + 14 * math.sin(x / 80 + 0.6) + 6 * math.sin(x / 31)
    sand_pts = [(-10, 520)] + [(x, edge_y(x)) for x in np.linspace(-10, 470, 30)] + [(480, 470), (W + 10, 476), (W + 10, H + 10), (-10, H + 10)]
    sm = shapes(W, H, [sand_pts])
    art = GP(art, sm, "#f3e8cf", "#fbf3e0", seed=nx(), rough=1.4)
    art = twash(art, sm * lin(W, H, 0, 490, 0, 640), "#d9c49d", 0.35, seed=nx())
    wet = strokes(W, H, [([(x, edge_y(x) + 5) for x in np.linspace(-10, 480, 50)], 10, None)]) * sm
    art = twash(art, wet, "#d2c3a0", 0.45, seed=nx())
    foam = strokes(W, H, [([(x, edge_y(x) - 1) for x in np.linspace(-10, 480, 60)], 4.5, None), ([(x, edge_y(x) - 9 + 2 * math.sin(x / 13)) for x in np.linspace(60, 420, 40)], 2.2, (0.2, 0.2))])
    art = GP(art, foam, "#ffffff", seed=nx(), rough=1.6, dry=0.25)
    rubble = ellipses(W, H, [(rng.uniform(0, W), rng.uniform(520, 630), rng.uniform(4, 11), rng.uniform(2.5, 6), rng.uniform(-20, 20)) for _ in range(34)])
    art = twash(art, np.roll(rubble, 2, 0) * (1 - rubble) * sm, "#a48d6c", 0.4, seed=nx())
    art = GP(art, rubble * sm, "#ece1cd", "#d6c6aa", seed=nx(), rough=1.2)
    grass = grass_tufts(W, H, 560, 640, 60, rng, hmin=10, hmax=26, lean=0.4, width=1.8) * (xx < 260)
    art = GP(art, grass, "#6f8f4a", "#8aa85a", seed=nx(), rough=0.8)
    psh = ellipses(W, H, [(190, 628, 90, 9, -4), (250, 636, 70, 7, -3)])
    art = twash(art, gaussian_filter(psh, 4) * sm, "#b49f7a", 0.35, seed=nx())
    art = palm(art, W, H, 92, 630, 360, 0.30, rng, nx, 1.1)
    art = palm(art, W, H, 190, 640, 270, 0.16, rng, nx, 0.85)
    preview(art, "coast", bg="#bfe3ee")
    print("coast", save(art, f"{OUT}/coast.webp", max_w=780, quality=78))
    clear()


def clouds():
    W, H = 780, 300
    rng = random.Random(5); nx = Seq(1300)
    art = blank(W, H)
    for cx_, cy_, s in [(170, 130, 1.0), (580, 90, 0.75), (700, 220, 0.5)]:
        blobs = [(cx_ + rng.uniform(-120, 120) * s, cy_ + rng.uniform(-25, 10) * s, rng.uniform(28, 58) * s) for _ in range(11)]
        m = circles(W, H, blobs)
        m = m * np.clip((cy_ + 30 * s - np.mgrid[0:H, 0:W][0]) / (20 * s), 0, 1)
        m = displace(gaussian_filter(m, 3), nx(), 10, 30)
        art = OV(art, m, lambda mm: pigment(mm, "#ffffff", "#f7fbfd", seed=nx(), density=0.95, edge=0.1, bloom=0.5, gran=0.05, feather=4, rough=9), pad=30)
        sh = m * lin(W, H, 0, cy_ + 5 * s, 0, cy_ + 34 * s)
        art = OV(art, sh, lambda mm: pigment(mm, "#d4e4ee", seed=nx(), density=0.35, edge=0.2, bloom=0.4, feather=3, rough=6), pad=30)
    art[..., :3] = 1 - (1 - art[..., :3]) * 0.4
    preview(art, "clouds", bg="#8fcbe0")
    print("clouds", save(art, f"{OUT}/clouds.webp", max_w=780, quality=78))
    clear()


def tenun():
    """Tenun Muna: dense weft stripes in red/maroon with orange-yellow-green-indigo accent bundles, thin white lines.
    Repeats vertically every 120 px; tile 480 x 120 (displayed at 240 x 60)."""
    T = TEN
    seq = [(T["mar"], 10), (T["red"], 16), (T["wht"], 2), (T["ora"], 6), (T["yel"], 4), (T["blk"], 3), (T["grn"], 8),
           (T["blk"], 3), (T["yel"], 4), (T["ora"], 6), (T["wht"], 2), (T["red"], 16), (T["mar"], 6), (T["ind"], 10),
           (T["wht"], 2), (T["pur"], 6), (T["wht"], 2), (T["ind"], 10), (T["mar"], 4)]
    tot = sum(h for _, h in seq)
    W, H = 480, tot
    rgb = weft_stripes(W, H, seq, seed=3, pick=2.0, warp=2.4, fibre=0.07)
    # make it tile horizontally: crossfade edges
    k = 40
    a = np.linspace(0, 1, k)[None, :, None]
    rgb[:, -k:] = rgb[:, -k:] * (1 - a) + rgb[:, :k] * a
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/tenun.png")
    print("tenun", save_rgb(rgb[:, :W - k], f"{OUT}/tenun.webp", quality=82), "period", tot)
    rv = np.ascontiguousarray(np.rot90(rgb[:, :W - k]))
    print("tenunv", save_rgb(rv, f"{OUT}/tenunv.webp", quality=82))
    clear()


def leaf():
    """One dried kolope leaf (heart-shaped yam leaf), tan, with curved veins: nodes, amp, sent."""
    W, H = 300, 340
    rng = random.Random(3); nx = Seq(1500)
    cx = W / 2
    pts = []
    for t in np.linspace(0, math.tau, 60, endpoint=False):
        # cardioid-ish leaf: notch at top (stalk), pointed tip at bottom
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * 8.4, 150 - y * 8.6))
    m = shapes(W, H, [deform(pts, rng, 2, 0.006)])
    art = blank(W, H)
    art = GP(art, m, "#c99a5b", "#dcb97f", seed=nx(), rough=1.6, streak=1.2)
    items = []
    bx, by = cx, 60
    for k in range(-3, 4):
        a0 = math.pi / 2 + k * 0.34
        items.append(([(bx + math.cos(a0 + 0.1 * k * s_) * 260 * s_, by + math.sin(a0 + 0.1 * k * s_) * 250 * s_) for s_ in np.linspace(0.02, 1, 14)], 2.6 if k == 0 else 1.8, (0.0, 0.5)))
    vm = strokes(W, H, items) * m
    art = twash(art, vm, "#7a4a22", 0.45, seed=nx())
    art = twash(art, m * lin(W, H, 60, 60, 260, 300), "#6e4520", 0.3, seed=nx())
    art = twash(art, np.clip(m - gaussian_filter(m, 2), 0, 1) * 3, "#6e4520", 0.6, seed=nx())
    stalk = strokes(W, H, [([(cx, 70), (cx + 4, 40), (cx + 16, 18)], 5, (0.0, 0.3))])
    art = GP(art, stalk, "#8c6a34", seed=nx(), rough=0.5)
    preview(art, "leaf", bg="#f4ecdf")
    print("leaf", save(art, f"{OUT}/leaf.webp", max_w=110, quality=84))
    clear()


def divider():
    """The flying line: a slack nanas-fibre string with a small kolope leaf knot at the centre."""
    W, H = 520, 80
    rng = random.Random(9); nx = Seq(1700)
    art = blank(W, H)
    l = curve([(10, 48), (130, 30), (260, 44), (390, 58), (510, 36)], 60)
    body, plies = rope(W, H, l, 4.2)
    art = GP(art, body, "#c49a5d", seed=nx(), rough=0.4)
    art = twash(art, plies, "#7a5428", 0.6, seed=nx())
    for x, y, a in [(240, 42, -0.6), (280, 46, 0.6)]:
        lm = shapes(W, H, [deform(petal_pts(x, y, 34, 13, a + math.pi / 2), rng, 2, 0.02)])
        art = GP(art, lm, "#c99a5b", "#dcb97f", seed=nx(), rough=1.0)
        art = twash(art, np.clip(lm - gaussian_filter(lm, 1.5), 0, 1) * 3, "#6e4520", 0.6, seed=nx())
    kn = circles(W, H, [(260, 44, 6)])
    art = GP(art, kn, TEN["red"], seed=nx(), rough=0.5)
    preview(art, "divider", bg="#f4ecdf")
    print("divider", save(art, f"{OUT}/divider.webp", max_w=260, quality=84))
    clear()


for p in PARTS:
    globals()[p]()
kb_report(OUT)
