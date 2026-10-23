"""Taman Zen — karesansui dry garden in ink wash and watercolour: raked sand ripples bending around moss-collared stones,
a red maple branch, a stone lantern, single maple leaves, a raked-line divider.
Run: python3 -I taman-zen.py [part ...]   parts: garden maple lantern leaf stone rake
Assets -> public/themes/art/taman-zen/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h5_lib import *
from PIL import ImageFilter

OUT = outdir("taman-zen")
PARTS = sys.argv[1:] or ["garden", "maple", "lantern", "leaf", "stone", "rake"]
SEQ = Seq(700)
SAND, SAND_D = "#e8e1d2", "#b9ae98"
INK, INK2 = "#2f2d2a", "#5b5852"
MOSS, MOSS_D, MOSS_L = "#7d8a4c", "#55602f", "#a4ae6a"
RED, RED_D, RED_L = "#b8361f", "#86210f", "#d9663a"


def stone_layer(W, H, cx, cy, rx, ry, rng, moss=True, rot=0.0):
    """Sumi-ink stone: grey wash body, darker shadow side, dry-brush texture, moss collar at the foot."""
    lay = blank(W, H)
    body = shape_mask(W, H, deform(ellipse_pts(cx, cy, rx, ry, 11, rot), rng, 3, 0.14))
    lay = G(lay, body, "#8d8980", "#a6a197", seed=SEQ(), density=0.7, edge=0.6, bloom=0.45, gran=0.5, rough=4, feather=1.0)
    sh = shape_mask(W, H, deform(ellipse_pts(cx + rx * 0.3, cy + ry * 0.25, rx * 0.8, ry * 0.7, 9, rot), rng, 2, 0.12)) * body
    lay = G(lay, sh, INK2, INK, seed=SEQ(), density=0.5, edge=0.5, bloom=0.3, gran=0.6, rough=3)
    # dry-brush crack strokes
    items = []
    for k in range(5):
        a = rng.uniform(0, math.tau)
        x0, y0 = cx + math.cos(a) * rx * 0.4, cy + math.sin(a) * ry * 0.4
        items.append(([(x0, y0), (x0 + rng.uniform(-rx, rx) * 0.4, y0 + rng.uniform(-ry, ry) * 0.3)], rng.uniform(2, 4), (0.2, 0.6)))
    lay = G(lay, strokes(W, H, items) * body, INK, seed=SEQ(), density=0.55, edge=0.2, bloom=0, gran=0.7, rough=1.2, feather=0.6, holes=0.25)
    # highlight (paper left showing): knock out top-left
    hl = gaussian_filter(shape_mask(W, H, ellipse_pts(cx - rx * 0.35, cy - ry * 0.4, rx * 0.35, ry * 0.22, 8, rot)), 6) * body
    lay[..., 3] *= 1 - hl * 0.55
    if moss:
        dots = []
        for k in range(160):
            a = rng.uniform(0.05 * math.pi, 0.95 * math.pi)
            r = rng.uniform(0.85, 1.12)
            dots.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r * 0.95 + ry * 0.05, rng.uniform(2.5, 6.5)))
        mm = circles(W, H, dots)
        lay = G(lay, mm, MOSS, MOSS_L, seed=SEQ(), density=0.8, edge=0.5, bloom=0.3, gran=0.5, rough=3, feather=0.8)
        dk = circles(W, H, [(x, y + 2, r * 0.6) for x, y, r in dots[::3]])
        lay = G(lay, dk, MOSS_D, seed=SEQ(), density=0.55, edge=0.4, bloom=0, gran=0.5, rough=2, feather=0.6)
    return lay, body


def garden():
    W, H = 780, 900
    rng = random.Random(3)
    stones = [(560, 300, 70, 46, 6), (210, 520, 92, 58, 8), (300, 470, 40, 28, 4), (610, 690, 52, 34, 5)]
    lines, wgt = ripple_field(W, H, [(x, y, rx, ry, n) for x, y, rx, ry, n in stones], spacing=13.0, base_angle=0.0, seed=4, duty=0.34, wob=1.6)
    # sand wash
    sand = np.ones((H, W), np.float32)
    art_ = G(blank(W, H), sand, SAND, "#efe9dc", seed=SEQ(), density=0.55, edge=0.0, bloom=0.4, gran=0.6, rough=1, feather=0.5)
    flush()
    # rake grooves: shadowed lower lip + light upper lip
    groove = lines * (1 - np.clip(sum(ellipses(W, H, [(x, y, rx * 1.06, ry * 1.06, 0)]) for x, y, rx, ry, _ in stones), 0, 1))
    art_ = G(art_, groove, SAND_D, "#a39882", seed=SEQ(), density=0.55, edge=0.3, bloom=0.2, gran=0.55, rough=1.2, feather=0.9)
    flush()
    hi = np.roll(groove, -4, 0) * (1 - groove)
    art_ = OV(art_, gaussian_filter(hi, 1.0), lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#f8f4ea"), np.float32), (np.clip(m, 0, 1) * 0.5)[..., None]], -1))
    for x, y, rx, ry, _ in stones:
        # cast shadow on sand
        shm = shape_mask(W, H, ellipse_pts(x + rx * 0.35, y + ry * 0.55, rx * 1.05, ry * 0.7, 10))
        art_ = G(art_, gaussian_filter(shm, 6), "#8e8676", seed=SEQ(), density=0.35, edge=0.1, bloom=0.2, gran=0.4, rough=3, feather=3)
        lay, body = stone_layer(W, H, x, y, rx, ry, rng, moss=True, rot=rng.uniform(-0.3, 0.3))
        art_ = knockout(art_, body, 0.6, 1.5)
        art_ = glaze(art_, lay)
        flush()
    # soft fade at the bottom so the garden melts into the page
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    fade = np.clip((1 - yy) / 0.22, 0, 1) ** 1.4
    fade = fade * np.clip(yy / 0.02 + 0.98, 0, 1)
    preview(art_, "tz-garden", "#efe9dc")
    # opaque (the page fades it out with a CSS mask) and a touch softer so the fine grooves compress well
    flat = on_paper(art_, "#efe9dc").filter(ImageFilter.GaussianBlur(0.5)).resize((620, 715), Image.LANCZOS)
    flat.save(f"{OUT}/garden.webp", "WEBP", quality=70, method=6)
    print("garden", os.path.getsize(f"{OUT}/garden.webp") // 1024, "KB")


def maple_leaf(W, H, x, y, s, ang, rng, col=RED, deep=RED_D, light=RED_L):
    pts = maple_leaf_pts(x, y, s, ang, rng)
    m = shape_mask(W, H, deform(pts, rng, 1, 0.03))
    lay = pig(m, col, light if rng.random() < 0.5 else col, seed=SEQ(), density=0.72, edge=0.75, bloom=0.4, gran=0.3, rough=2.0, feather=0.8)
    veins = []
    for a, L in [(-math.pi / 2, 0.85), (-math.pi / 2 - .62, .72), (-math.pi / 2 + .62, .72), (-math.pi / 2 - 1.25, .5), (-math.pi / 2 + 1.25, .5)]:
        veins.append(([(x, y), (x + math.cos(a + ang) * s * L, y + math.sin(a + ang) * s * L)], max(1.0, s * 0.03), (0.0, 0.5)))
    lay = glaze(lay, pig(strokes(W, H, veins) * m, deep, seed=SEQ(), density=0.45, edge=0.2, bloom=0, rough=0.6, feather=0.5))
    return lay, m


def maple():
    W, H = 760, 620
    rng = random.Random(17)
    art_ = blank(W, H)
    # sumi branch entering from the top-right, dipping down-left
    main = curve([(770, 40), (600, 92), (430, 120), (300, 190), (150, 230), (60, 300)], 60)
    tw = [curve([(600, 92), (560, 180), (500, 250)], 20), curve([(430, 120), (380, 60), (300, 40)], 20),
          curve([(300, 190), (280, 280), (230, 350)], 20), curve([(150, 230), (110, 170)], 12), curve([(520, 104), (470, 200), (420, 250)], 18)]
    items = [(main, 16, (0.0, 0.85))] + [(t, 7, (0.0, 0.8)) for t in tw]
    bm = strokes(W, H, items)
    art_ = G(art_, bm, INK, INK2, seed=SEQ(), density=0.85, edge=0.6, bloom=0.2, gran=0.6, rough=2.0, feather=0.7, holes=0.12)
    art_ = G(art_, bm, "#1c1b19", seed=SEQ(), density=0.7, edge=0.7, bloom=0.3, gran=0.7, rough=2.0, feather=0.6, holes=0.3)
    flush()
    ends = [main[-1], main[48], main[36], main[28]] + [t[-1] for t in tw] + [main[20], tw[0][10], tw[2][10]]
    for k, (ex, ey) in enumerate(ends):
        for j in range(rng.randint(2, 4)):
            a = rng.uniform(-0.9, 0.9) + (math.pi if rng.random() < 0.2 else 0)
            s = rng.uniform(30, 46)
            lx, ly = ex + rng.gauss(0, 18), ey + rng.gauss(0, 14) + s * 0.6
            # petiole
            art_ = G(art_, strokes(W, H, [([(ex, ey), (lx, ly)], 2.0, (0, .3))]), RED_D, seed=SEQ(), density=0.6, edge=0.2, rough=0.5, feather=0.5)
            pal = rng.random()
            col = RED if pal < 0.6 else ("#c9562a" if pal < 0.85 else "#a8291c")
            lay, m = maple_leaf(W, H, lx, ly, s, a, rng, col)
            art_ = glaze(art_, lay)
        flush()
    preview(art_, "tz-maple", "#efe9dc")
    save(art_, f"{OUT}/maple.webp", max_w=480, quality=80)


def lantern():
    """Kasuga-style stone lantern in ink wash with moss on the cap."""
    W, H = 360, 640
    rng = random.Random(21)
    cx = 180
    parts = [
        ("hoju", [(cx - 14, 92), (cx + 14, 92), (cx + 18, 72), (cx, 40), (cx - 18, 72)], 0.7),
        ("kasa", [(cx - 128, 196), (cx - 108, 178), (cx - 40, 128), (cx, 112), (cx + 40, 128), (cx + 108, 178), (cx + 128, 196), (cx + 108, 210), (cx - 108, 210)], 0.8),
        ("hibukuro", [(cx - 62, 214), (cx + 62, 214), (cx + 62, 318), (cx - 62, 318)], 0.6),
        ("chudai", [(cx - 92, 322), (cx + 92, 322), (cx + 74, 360), (cx - 74, 360)], 0.7),
        ("sao", [(cx - 30, 360), (cx + 30, 360), (cx + 36, 530), (cx - 36, 530)], 0.6),
        ("kiso", [(cx - 96, 534), (cx + 96, 534), (cx + 108, 588), (cx - 108, 588)], 0.75),
    ]
    art_ = blank(W, H)
    for name, pts, d in parts:
        m = shape_mask(W, H, deform(pts, rng, 1, 0.03), smooth=False)
        m = displace(m, SEQ(), 2.0, 20)
        art_ = G(art_, m, "#8f8b83", "#a7a299", seed=SEQ(), density=d, edge=0.65, bloom=0.4, gran=0.6, rough=2.5, feather=0.8)
        # right side shadow
        xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
        sh = m * np.clip((xs * W - cx) / 70, 0, 1)
        art_ = G(art_, sh, INK2, seed=SEQ(), density=0.35, edge=0.2, bloom=0.2, gran=0.6, rough=2)
        flush()
    # fire box opening (dark window with a warm glow)
    win = shape_mask(W, H, [(cx - 28, 236), (cx + 28, 236), (cx + 28, 296), (cx - 28, 296)], smooth=False)
    art_ = G(art_, win, INK, seed=SEQ(), density=0.85, edge=0.5, bloom=0.1, gran=0.5, rough=1.5)
    art_ = over(art_, glow(shape_mask(W, H, ellipse_pts(cx, 270, 14, 18, 8)), "#f0b260", radius=8, strength=0.55))
    # ink outline accents (dry brush) on the cap and base edges
    acc = strokes(W, H, [([(cx - 128, 197), (cx - 40, 130), (cx, 113)], 3.2, (0.1, 0.4)), ([(cx + 128, 197), (cx + 108, 211), (cx - 108, 211)], 3.0, (0.2, 0.3)),
                          ([(cx + 36, 360), (cx + 36, 530)], 2.6, (0.2, 0.4)), ([(cx + 108, 588), (cx - 108, 588)], 3.0, (0.2, 0.2))])
    art_ = G(art_, acc, INK, seed=SEQ(), density=0.75, edge=0.2, bloom=0, gran=0.7, rough=1.0, feather=0.5, holes=0.2)
    # moss on the cap and base
    dots = [(cx + rng.uniform(-110, 110), 180 + rng.uniform(-14, 22) - (110 - abs(rng.uniform(-110, 110))) * 0.4, rng.uniform(3, 6)) for _ in range(70)]
    dots += [(cx + rng.uniform(-110, 110), 590 + rng.uniform(-8, 10), rng.uniform(3, 7)) for _ in range(90)]
    mm = circles(W, H, dots)
    art_ = G(art_, mm, MOSS, MOSS_L, seed=SEQ(), density=0.75, edge=0.5, bloom=0.3, gran=0.5, rough=3, feather=0.8)
    # ground wash
    gm = shape_mask(W, H, deform(ellipse_pts(cx, 600, 170, 26, 10), rng, 2, 0.15))
    art_ = glaze(G(blank(W, H), gm, "#b9ae98", seed=SEQ(), density=0.4, edge=0.3, bloom=0.4, gran=0.5, rough=5), art_)
    preview(art_, "tz-lantern", "#efe9dc")
    save(art_, f"{OUT}/lantern.webp", max_w=220, quality=80)


def leaf():
    W = H = 200
    rng = random.Random(41)
    lay, m = maple_leaf(W, H, 100, 112, 80, 0.15, rng)
    lay = glaze(lay, pig(strokes(W, H, [([(100, 112), (106, 150)], 3, (0, .4))]), RED_D, seed=SEQ(), density=0.6, edge=0.2, rough=0.6))
    preview(lay, "tz-leaf", "#efe9dc")
    save(lay, f"{OUT}/leaf.webp", max_w=96, quality=84)


def stone():
    W, H = 420, 300
    rng = random.Random(51)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lines, _ = ripple_field(W, H, [(210, 146, 70, 46, 6)], spacing=12.0, seed=6, duty=0.32, wob=1.2)
    d = np.hypot(xx - 210, (yy - 150) * 1.2)
    fadem = np.clip((190 - d) / 50, 0, 1)
    art_ = G(blank(W, H), lines * fadem, SAND_D, seed=SEQ(), density=0.5, edge=0.3, bloom=0.2, gran=0.55, rough=1.2, feather=0.9)
    lay, body = stone_layer(W, H, 210, 146, 70, 46, rng, moss=True)
    art_ = knockout(art_, body, 1.0, 3)
    art_ = glaze(art_, lay)
    preview(art_, "tz-stone", "#efe9dc")
    save(art_, f"{OUT}/stone.webp", max_w=210, quality=82)


def rake():
    W, H = 900, 90
    items = []
    for k in range(3):
        y = 30 + k * 15
        pts = [(x, y + math.sin(x / 70 + k * 0.3) * 4) for x in np.linspace(20, 880, 80)]
        items.append((pts, 3.6, (0.12, 0.12)))
    m = strokes(W, H, items)
    lay = G(blank(W, H), m, INK2, "#8a857b", seed=SEQ(), density=0.55, edge=0.3, bloom=0.1, gran=0.7, rough=1.0, feather=0.6, holes=0.15)
    rng = random.Random(61)
    st, body = stone_layer(W, H, 450, 45, 30, 20, rng, moss=False)
    lay = knockout(lay, body, 1.0, 5)
    lay = glaze(lay, st)
    preview(lay, "tz-rake", "#efe9dc")
    save(lay, f"{OUT}/rake.webp", max_w=440, quality=82)


for part in PARTS:
    {"garden": garden, "maple": maple, "lantern": lantern, "leaf": leaf, "stone": stone, "rake": rake}[part]()
    flush()
kb(OUT)
