"""Sentani Kayu — kombouw-inspired bark painting: beaten-bark cloth painted with black outlines and white / red-ochre fills
(original fish, spiral and dotted water motifs, not copies of any specific work), plus a gouache view of Lake Sentani's
islands under the Cycloop range.
Run: python3 -I sentani-kayu.py [part ...]   parts: bark panel lake fish spiral divider
Assets -> public/themes/art/sentani-kayu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f2_lib import *  # noqa

OUT = outdir("sentani-kayu")
PARTS = sys.argv[1:] or ["bark", "panel", "lake", "fish", "spiral", "divider"]
BLACK, WHITE, OCHRE, BARK = "#1d1612", "#eee3cf", "#a9472b", "#8a5a34"


def ink(art, m, nx, col=BLACK, rough=1.6):
    """Natural pigment applied with a chewed-stick brush: opaque, matte, slightly dry at the edges."""
    return GP(art, m, col, mix_hex(col, "#000000" if col != BLACK else "#3a2a20", 0.15), seed=nx(), rough=rough, streak=0.9, dry=0.18)


def fish_geom(cx, cy, L, ang, bend=0.0):
    """Fish outline (body + forked tail) and interior band polygons, in local coords rotated by ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        v = v + bend * (u ** 2)
        return (cx + u * L * ca - v * L * sa, cy + u * L * sa + v * L * ca)
    body = []
    for i in range(24):
        t = i / 23
        u = 0.5 - t  # head at +0.5
        w = 0.19 * math.sin(math.pi * t) ** 0.75
        body.append(P(u, -w))
    for i in range(24):
        t = 1 - i / 23
        u = 0.5 - t
        w = 0.19 * math.sin(math.pi * t) ** 0.75
        body.append(P(u, w))
    tail = [P(-0.44, 0), P(-0.72, -0.2), P(-0.62, 0), P(-0.72, 0.2)]
    bands = []
    for k, (u0, u1) in enumerate([(0.18, 0.28), (0.02, 0.1), (-0.14, -0.06), (-0.28, -0.22)]):
        bands.append([P(u0, -0.25), P(u1, -0.25), P(u1, 0.25), P(u0, 0.25)])
    eye = P(0.33, -0.04)
    fins = [[P(0.05, -0.17), P(-0.12, -0.32), P(-0.18, -0.15)], [P(0.0, 0.17), P(-0.16, 0.3), P(-0.2, 0.14)]]
    spine = [P(0.42 - 0.84 * i / 20, 0) for i in range(21)]
    return body, tail, bands, eye, fins, spine


def paint_fish(art, W, H, cx, cy, L, ang, nx, rng, bend=0.0, body_col=OCHRE):
    body, tail, bands, eye, fins, spine = fish_geom(cx, cy, L, ang, bend)
    bm = shapes(W, H, [body]); tm = shapes(W, H, [tail], smooth=False); fm = shapes(W, H, fins, smooth=False)
    art = ink(art, np.clip(bm + tm + fm, 0, 1), nx, BLACK)
    inner_b = np.clip(bm - gaussian_filter(1 - bm, 1.2) * 4 - (1 - erode(bm, L * 0.03)), 0, 1)
    art = ink(art, erode(bm, L * 0.035), nx, body_col)
    bandm = shapes(W, H, bands, smooth=False) * erode(bm, L * 0.035)
    art = ink(art, bandm, nx, WHITE)
    # black ribs inside white bands + dot rows on the ochre
    ribs = strokes(W, H, [([(b[0][0] * 0.5 + b[1][0] * 0.5, b[0][1] * 0.5 + b[1][1] * 0.5), (b[2][0] * 0.5 + b[3][0] * 0.5, b[2][1] * 0.5 + b[3][1] * 0.5)], L * 0.018, (0.1, 0.1)) for b in bands]) * bandm
    art = ink(art, ribs, nx, BLACK, rough=0.8)
    dots = []
    for x, y in spine[2:-3:2]:
        dots.append((x + rng.uniform(-1, 1), y + rng.uniform(-1, 1), L * 0.014))
    art = ink(art, circles(W, H, dots) * (1 - bandm), nx, WHITE, rough=0.6)
    art = ink(art, erode(tm, L * 0.03), nx, WHITE, rough=1.0)
    art = ink(art, circles(W, H, [(eye[0], eye[1], L * 0.045)]), nx, WHITE, rough=0.6)
    art = ink(art, circles(W, H, [(eye[0], eye[1], L * 0.022)]), nx, BLACK, rough=0.4)
    return art


def erode(m, r):
    from scipy.ndimage import distance_transform_edt
    d = distance_transform_edt(m > 0.5)
    return np.clip(d - r, 0, 1).astype(np.float32)


def spiral_band(cx, cy, r, turns, a0=0.0, direction=1, width=5.0):
    return (spiral(cx, cy, r * 0.08, r, turns, a0, n=int(60 * turns), direction=direction), width, (0.0, 0.15))


def paint_spiral(art, W, H, cx, cy, r, nx, rng, turns=2.4, a0=0.0, direction=1, dots=True):
    pts = spiral(cx, cy, r * 0.06, r, turns, a0, n=int(70 * turns), direction=direction)
    art = ink(art, strokes(W, H, [(pts, r * 0.16, (0.0, 0.12))]), nx, BLACK)
    if dots:
        gap = spiral(cx, cy, r * 0.14 + r * 0.17, r + r * 0.17, turns - 0.25, a0 + 0.0, n=int(70 * turns), direction=direction)
        ds = [(x, y, r * 0.045) for x, y, _ in resample(gap, r * 0.16)][2:]
        art = ink(art, circles(W, H, ds), nx, WHITE, rough=0.5)
    return art


def ragged(W, H, x0, y0, x1, y1, seed, amt=7):
    m = rect(W, H, x0, y0, x1, y1)
    m = displace(m, seed, amt, 10)
    fib = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (6, 0.6))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    return np.clip((gaussian_filter(m, 1.2) + fib * 0.06 - 0.45) * 4, 0, 1)


def part_bark():
    rgb = bark_cloth(512, 512, BARK, seed=4)
    prev_rgb(rgb, "sk-bark")
    rgb_save(rgb, f"{OUT}/bark.webp", quality=72)


def part_panel():
    """The cover's bark painting: two fish circling a spiral 'eye', a border of linked spirals and dotted water lines."""
    W, H = 760, 980
    rng = random.Random(7); nx = Seq(500)
    sheet = ragged(W, H, 30, 26, W - 30, H - 26, nx(), amt=9)
    bark = bark_cloth(W, H, "#93623a", seed=8, tile=False)
    art = np.concatenate([bark, sheet[..., None]], -1)
    sh = np.roll(np.roll(gaussian_filter(sheet, 8), 10, 0), 6, 1) * 0.45
    art = over(np.concatenate([np.zeros((H, W, 3), np.float32), sh[..., None]], -1), art)
    # border: rows of black zig-zag with white dots, ochre band
    bd = []
    for (y, flip) in ((86, 1), (H - 86, -1)):
        pts = [(70 + i * 22, y + (12 if i % 2 else -12) * flip) for i in range(int((W - 140) / 22) + 1)]
        bd.append((pts, 5.0, None))
    art = ink(art, strokes(W, H, bd), nx)
    art = ink(art, rect(W, H, 64, 112, W - 64, 124) + rect(W, H, 64, H - 124, W - 64, H - 112), nx, OCHRE)
    dots = [(70 + i * 22, 86 + 2, 3.4) for i in range(1, int((W - 140) / 22), 2)] + [(70 + i * 22, H - 86 - 2, 3.4) for i in range(0, int((W - 140) / 22), 2)]
    art = ink(art, circles(W, H, dots), nx, WHITE, rough=0.5)
    # side columns of small linked spirals
    for x, d in ((96, 1), (W - 96, -1)):
        for k in range(6):
            y = 196 + k * 118
            art = paint_spiral(art, W, H, x, y, 30, nx, rng, turns=1.7, a0=k * 1.3, direction=d if k % 2 else -d, dots=False)
        link = strokes(W, H, [([(x + 26 * d * (1 if k % 2 else -1), 196 + k * 118 + 20) for k in range(6)], 4.0, None)])
        art = ink(art, link * 0, nx)
    # central motif: concentric 'eye' with spiral core
    cx, cy = W / 2, H / 2
    rings = [(150, BLACK), (138, OCHRE), (112, BLACK), (102, WHITE), (78, BLACK), (70, OCHRE)]
    for r, c in rings:
        art = ink(art, circles(W, H, [(cx + rng.uniform(-1.5, 1.5), cy + rng.uniform(-1.5, 1.5), r)]), nx, c, rough=1.4)
    ring_dots = [(cx + math.cos(a) * 125, cy + math.sin(a) * 125, 4.2) for a in np.linspace(0, math.tau, 46, endpoint=False)]
    art = ink(art, circles(W, H, ring_dots), nx, WHITE, rough=0.5)
    tri = []
    for k in range(18):
        a = k / 18 * math.tau
        tri.append([(cx + math.cos(a - 0.12) * 104, cy + math.sin(a - 0.12) * 104), (cx + math.cos(a) * 82, cy + math.sin(a) * 82), (cx + math.cos(a + 0.12) * 104, cy + math.sin(a + 0.12) * 104)])
    art = ink(art, shapes(W, H, tri, smooth=False), nx, BLACK, rough=0.8)
    art = paint_spiral(art, W, H, cx, cy, 56, nx, rng, turns=2.3, a0=0.4, direction=1, dots=False)
    art = ink(art, circles(W, H, [(cx, cy, 6)]), nx, WHITE, rough=0.4)
    # two fish swimming around the eye
    art = paint_fish(art, W, H, cx - 10, cy - 250, 300, 0.05, nx, rng, bend=0.18)
    art = paint_fish(art, W, H, cx + 10, cy + 250, 300, math.pi + 0.05, nx, rng, bend=0.18, body_col="#7f2f1e")
    # water: dotted wave lines in the corners
    waves = []
    for (x0, y0, s) in ((150, 300, 1), (W - 300, 300, 1), (150, H - 300, -1), (W - 300, H - 300, -1)):
        for j in range(3):
            pts = [(x0 + i * 6, y0 + j * 18 * s + math.sin(i * 0.45 + j) * 5) for i in range(26)]
            waves.append((pts, 3.2, (0.1, 0.1)))
    art = ink(art, strokes(W, H, waves), nx, BLACK)
    wd = [(x, y + 7, 2.2) for it in waves for (x, y) in it[0][::4]]
    art = ink(art, circles(W, H, wd), nx, WHITE, rough=0.4)
    art[..., 3] *= np.clip(sheet + sh, 0, 1)
    preview(art, "sk-panel", bg="#2a1d16")
    save(art, f"{OUT}/panel.webp", max_w=560, quality=80)
    clear()


def part_fish():
    W, H = 360, 200
    rng = random.Random(3); nx = Seq(900)
    art = paint_fish(blank(W, H), W, H, 180, 100, 260, 0.0, nx, rng, bend=0.1)
    preview(art, "sk-fish", tone="#8a5a34")
    save(art, f"{OUT}/fish.webp", max_w=150, quality=84)
    clear()


def part_spiral():
    W, H = 200, 200
    rng = random.Random(5); nx = Seq(1000)
    art = ink(blank(W, H), circles(W, H, [(100, 100, 86)]), nx, OCHRE, rough=1.5)
    art = paint_spiral(art, W, H, 100, 100, 60, nx, rng, turns=2.3, a0=0.3, direction=1, dots=True)
    preview(art, "sk-spiral", tone="#8a5a34")
    save(art, f"{OUT}/spiral.webp", max_w=96, quality=84)
    clear()


def part_divider():
    W, H = 760, 120
    rng = random.Random(6); nx = Seq(1200)
    art = blank(W, H)
    left = [(40 + i * 14, 60 + (9 if i % 2 else -9)) for i in range(20)]
    right = [(W - 40 - i * 14, 60 + (9 if i % 2 else -9)) for i in range(20)]
    art = ink(art, strokes(W, H, [(left, 4.2, None), (right, 4.2, None)]), nx)
    art = ink(art, circles(W, H, [(x, 60 + (-14 if (i % 2) else 14), 3.0) for i, (x, _) in enumerate(left + right)]), nx, WHITE, rough=0.4)
    art = paint_spiral(art, W, H, W / 2 - 46, 60, 34, nx, rng, turns=1.8, a0=0.0, direction=1, dots=False)
    art = paint_spiral(art, W, H, W / 2 + 46, 60, 34, nx, rng, turns=1.8, a0=math.pi, direction=1, dots=False)
    art = ink(art, circles(W, H, [(W / 2, 22, 5), (W / 2, 98, 5)]), nx, OCHRE, rough=0.5)
    preview(art, "sk-divider", tone="#8a5a34")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)
    clear()


def part_lake():
    """Lake Sentani: Cycloop ridges in blue-green haze, forested islands, a stilt village and an empty dugout canoe."""
    W, H = 900, 640
    rng = random.Random(11); nx = Seq(1500)
    rgb = painted_sky(W, H, [(0, "#d9c7a8"), (0.42, "#efdcbc"), (0.5, "#cdd3c2"), (1, "#7e9c94")], seed=nx(), streak=0.5, grain=0.3)[..., :3]
    def layer(pts, c1, c2, rough=2.5):
        m = displace(poly(W, H, pts, smooth=True), nx(), rough, 20)
        return GP(blank(W, H), m, c1, c2, seed=nx(), rough=2.0, streak=0.8), m
    # Cycloop: far and mid ridges
    far = [(-20, 330)] + [(x, 220 - 70 * math.exp(-((x - 560) / 180) ** 2) - 30 * math.sin(x / 70) - rng.uniform(0, 14)) for x in range(0, W + 30, 30)] + [(W + 20, 330)]
    lay, m = layer(far, "#8f9fa6", "#9aa8a6")
    rgb = comp_rgb(rgb, lay)
    vf = 0.5 + 0.5 * np.sin(np.arange(W)[None, :] / 9 + fbm(W, H, nx(), 30, 2) * 6)
    rgb = comp_rgb(rgb, flat(m * np.clip((vf - 0.85) * 5, 0, 1) * (1 - ygrad(W, H, 200, 300)) * fbm(W, H, nx(), 40, 2), "#7a8a92", 0.35))
    mid = [(-20, 360)] + [(x, 285 - 40 * math.sin(x / 120 + 1) - rng.uniform(0, 10)) for x in range(0, W + 30, 26)] + [(W + 20, 360)]
    lay, m = layer(mid, "#4f6b5e", "#5d7863")
    rgb = comp_rgb(rgb, lay)
    tree = []
    for _ in range(260):
        x = rng.uniform(0, W); y = rng.uniform(250, 340)
        if m[int(min(H - 1, y)), int(min(W - 1, x))] > 0.5:
            tree.append((x, y, rng.uniform(6, 12), rng.uniform(4, 8), 0))
    rgb = comp_rgb(rgb, GP(blank(W, H), ellipses(W, H, tree) * m, "#3c5a4c", "#466652", seed=nx(), rough=1.5, streak=0.6))
    clear()
    # lake
    lake = rect(W, H, -10, 338, W + 10, H + 10)
    rgb = comp_rgb(rgb, GP(blank(W, H), lake, "#6f938c", "#5d837f", seed=nx(), rough=1.5, streak=1.0))
    rip = []
    for _ in range(140):
        t = rng.random() ** 1.3
        y = 345 + (H - 345) * t; x = rng.uniform(-40, W)
        L = (20 + 120 * t) * rng.uniform(0.6, 1.4)
        rip.append(([(x, y), (x + L, y + rng.uniform(-1, 1))], 0.8 + 2.4 * t, (0.4, 0.4)))
    rgb = comp_rgb(rgb, flat(strokes(W, H, rip), "#cfe0d4", 0.55))
    rgb = comp_rgb(rgb, flat(strokes(W, H, rip[::3]) * 1, "#3f625f", 0.0))
    # islands with jungle domes and reflections
    isl = blank(W, H)
    for (cx, w, h) in ((170, 220, 52), (520, 150, 36), (760, 120, 28)):
        blobs = [(cx + rng.uniform(-0.45, 0.45) * w, 352 - rng.uniform(0, 1) * h * 0.6, w * rng.uniform(0.08, 0.16), h * rng.uniform(0.35, 0.6), 0) for _ in range(16)]
        im = np.maximum(ellipses(W, H, blobs), poly(W, H, [(cx - w / 2, 356), (cx - w * 0.4, 344), (cx + w * 0.4, 344), (cx + w / 2, 356)], smooth=True))
        im = displace(im, nx(), 2, 10) * (1 - ygrad(W, H, 354, 358))
        isl = GP(isl, im, "#3e6248", "#557a4f", seed=nx(), rough=1.5, streak=0.7)
        lit = im * np.clip(1 - ygrad(W, H, 352 - h, 352) * 1.2, 0, 1) * np.clip(1 - xgrad(W, H, cx - w / 2, cx + w / 2), 0, 1)
        isl = OV(isl, lit, lambda m_: np.concatenate([np.ones(m_.shape + (3,), np.float32) * col_arr("#8fae6a"), (m_ * 0.6)[..., None]], -1))
    # stilt village on the big island's shore
    houses = []
    posts = []
    for k in range(5):
        x = 70 + k * 46; y = 368 + (k % 2) * 6
        houses.append([(x - 18, y), (x + 18, y), (x + 18, y - 16), (x, y - 30), (x - 18, y - 16)])
        posts.append(([(x - 14, y), (x - 14, y + 16)], 2.0, None)); posts.append(([(x + 14, y), (x + 14, y + 16)], 2.0, None))
    isl = GP(isl, strokes(W, H, posts), "#3b2b22", seed=nx(), rough=0.8, streak=0.4)
    hm = shapes(W, H, houses, smooth=False)
    isl = GP(isl, hm, "#b48a5a", "#a27a4e", seed=nx(), rough=1.0, streak=0.7)
    roofs = shapes(W, H, [[(h[4][0] - 3, h[4][1] + 1), (h[3][0], h[3][1] - 2), (h[2][0] + 3, h[2][1] + 1)] for h in houses], smooth=False)
    isl = GP(isl, roofs, "#6b4a2e", seed=nx(), rough=1.0, streak=0.7)
    canoe = poly(W, H, [(540, 470), (700, 470), (690, 478), (552, 478)], smooth=True)
    isl = GP(isl, canoe, "#3b2a20", seed=nx(), rough=0.8)
    isl = GP(isl, strokes(W, H, [([(610, 468), (650, 440)], 2.2, None)]), "#3b2a20", seed=nx(), rough=0.6)
    ref = isl.copy()
    ref = ref[::-1].copy()
    shift = 2 * 356 - H
    ref = np.roll(ref, shift + 2, 0)
    ref[..., 3] *= (np.arange(H)[:, None] > 357) * 0.45
    ref[..., :3] = ref[..., :3] * 0.6 + col_arr("#4f7672") * 0.4
    rgb = comp_rgb(rgb, ref)
    rgb = comp_rgb(rgb, isl)
    paperk = np.asarray(paper(W, H, "#ffffff", 3), np.float32) / 255
    rgb = rgb * (0.95 + 0.05 * paperk)
    prev_rgb(rgb, "sk-lake")
    rgb_save(rgb, f"{OUT}/lake.webp", quality=76, size=(720, 512))
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
