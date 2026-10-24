"""Batik Gentongan — Tanjung Bumi (Madura) batik soaked for months in clay gentong jars: a seamless kain tile on a deep
mengkudu-red ground with pesisir flowers, stylised birds, leafy sprigs and cecek dots resisted in cream, indigo and
soga, all crossed by fine indigo wax-crackle veins; a tumpal + ombak (sea wave) border strip; a clay dye gentong with
a batik cloth draped over its rim; a flower-spray divider; a single batik bird motif.
Run: python3 -I batik-gentongan.py [part ...]   parts: kain tepi gentong sekar burung
Assets -> public/themes/art/batik-gentongan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q1_lib import *  # noqa
from scipy.ndimage import map_coordinates

OUT = outdir("batik-gentongan")
PARTS = sys.argv[1:] or ["kain", "tepi", "gentong", "sekar", "burung"]
RED, RED_D = "#8e1e17", "#5e120e"
INDIGO, INDIGO_D = "#1f2e57", "#131c38"
SOGA = "#8a5428"
CREAM = "#efe2c4"
GREEN = "#3c5a3a"
CLAY, CLAY_D, CLAY_L = "#a5532e", "#5c2a16", "#c97a4c"


# ---------------------------------------------------------------- motif geometry
def flower(cx, cy, R, n=8, rot=0.0):
    petals = [petal_pts(cx, cy, R, R * 0.42, rot + i / n * math.tau, n=14) for i in range(n)]
    return petals, (cx, cy, R * 0.32)


def bird(cx, cy, s, d=1, rot=0.0):
    """Stylised pesisir bird: plump body, small crested head, scalloped wing, three long curling tail plumes."""
    def P(x, y):
        x, y = x * d, y
        c, sn = math.cos(rot), math.sin(rot)
        return (cx + (x * c - y * sn) * s, cy + (x * sn + y * c) * s)
    bodyp = [P(math.cos(t) * 32 + 6, math.sin(t) * 19 + 2) for t in np.linspace(0, math.tau, 24, endpoint=False)]
    head = [P(40 + math.cos(t) * 11, -14 + math.sin(t) * 10) for t in np.linspace(0, math.tau, 16, endpoint=False)]
    beak = [P(49, -18), P(64, -12), P(49, -9)]
    crest = [P(38, -22), P(30, -30), P(18, -32), P(24, -26), P(34, -18)]
    wing = [P(-10, -2), P(4, -30), P(30, -22), P(28, 4), P(8, 10)]
    tails = [[P(-24, -2), P(-46, -26), P(-54, -56), P(-40, -78), P(-26, -70)],
             [P(-24, 4), P(-60, -8), P(-90, -28), P(-102, -52)],
             [P(-22, 10), P(-60, 16), P(-98, 8), P(-120, -8)]]
    scallops = [[P(-2 + k * 9, 4 - k * 3), P(6 + k * 9, -16 - k * 3)] for k in range(3)]
    return dict(body=[bodyp, head, beak, crest], wing=wing, tails=tails, scallops=scallops, eye=P(42, -16))


def sprig(x0, y0, x1, y1, bend, nleaf, L):
    c = curve([(x0, y0), ((x0 + x1) / 2 + bend, (y0 + y1) / 2 - bend), (x1, y1)], 24)
    leaves = []
    for k in range(1, nleaf + 1):
        i = int(k / (nleaf + 1) * (len(c) - 2))
        (ax, ay), (bx, by) = c[i], c[i + 1]
        a = math.atan2(by - ay, bx - ax) + (0.9 if k % 2 else -0.9)
        leaves.append(petal_pts(ax, ay, L, L * 0.36, a, n=12))
    return c, leaves


# ---------------------------------------------------------------- seamless helpers
def wrapped(pts_list, W, H):
    out = []
    for pts in pts_list:
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):
                out.append([(x + dx, y + dy) for x, y in pts])
    return out


def wdisp(mask, seed, amt=1.6, sigma=6):
    h, w = mask.shape
    nx_ = wrap_noise(w, h, seed, sigma) - 0.5
    ny_ = wrap_noise(w, h, seed + 1, sigma) - 0.5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return map_coordinates(mask, [yy + ny_ * amt * 2, xx + nx_ * amt * 2], order=1, mode="wrap")


def dye(shape_mask_, col, seed, var=0.08):
    """Seamless flat dye with a little blotchiness."""
    h, w = shape_mask_.shape
    n = wrap_noise(w, h, seed, 14)
    rgb = np.ones((h, w, 3), np.float32) * col_arr(col) * (1 - var + var * 2 * n)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(shape_mask_, 0, 1)[..., None]], -1)


def grow(m, px):
    return np.clip(gaussian_filter(m, px, mode="wrap") * 3.0, 0, 1)


def batik_layers(W, H, motifs, seed, wrap=True, ground=RED, crack=0.38, dots=True, rng=None):
    """Compose a batik field: cream resist outlines around every motif, coloured dye fills, cream inner lines,
    cecek dots and wax crackle. motifs: list of (mask, colour, inner_lines_mask)."""
    rng = rng or random.Random(seed)
    art = dye(np.ones((H, W), np.float32), ground, seed, 0.1) if ground else blank(W, H)
    allm = np.zeros((H, W), np.float32)
    for m, col, inner in motifs:
        allm = np.maximum(allm, m)
    outline = wdisp(grow(allm, 2.1), seed + 2, 1.2)
    art = over(art, dye(outline, CREAM, seed + 3, 0.05))
    for k, (m, col, inner) in enumerate(motifs):
        art = over(art, dye(wdisp(m, seed + 10 + k, 1.0), col, seed + 20 + k))
        if inner is not None:
            art = over(art, dye(wdisp(inner, seed + 30 + k, 0.8), CREAM, seed + 40 + k, 0.05))
    if dots:
        pts = []
        for _ in range(int(W * H / 150)):
            x, y = rng.uniform(0, W), rng.uniform(0, H)
            pts.append((x, y, rng.uniform(1.0, 1.7)))
        dm = circles(W, H, [(x + dx, y + dy, r) for x, y, r in pts for dx in (-W, 0, W) for dy in (-H, 0, H)]) if wrap else circles(W, H, pts)
        dm = dm * (1 - grow(allm, 3.0))
        art = over(art, dye(dm, CREAM, seed + 5, 0.05))
    cr = crackle(W, H, seed + 7, n=int(W * H / 2600), length=90, width=0.9, wrap=wrap)
    art = over(art, tint(cr, INDIGO_D, crack))
    return art


def motif_set(W, H, rng, wrap=True):
    F = (lambda L: wrapped(L, W, H)) if wrap else (lambda L: L)
    flowers, centres, rings = [], [], []
    for cx, cy, R, rot in ((96, 104, 54, 0.2), (300, 296, 50, 0.6), (318, 70, 22, 0.1), (70, 318, 24, 0.3), (196, 208, 20, 0.0), (214, 34, 15, 0.4), (24, 196, 14, 0.1), (384, 150, 15, 0.5), (238, 372, 15, 0.2), (160, 320, 12, 0.7), (372, 384, 12, 0.3), (176, 92, 11, 0.1)):
        p, (x, y, r) = flower(cx, cy, R, 8 if R > 30 else 6, rot)
        flowers += p
        centres.append([(x + math.cos(t) * r, y + math.sin(t) * r) for t in np.linspace(0, math.tau, 18, endpoint=False)])
        rings.append([(x + math.cos(t) * r * 0.45, y + math.sin(t) * r * 0.45) for t in np.linspace(0, math.tau, 14, endpoint=False)])
    m_flow = shapes(W, H, F(flowers))
    m_cent = shapes(W, H, F(centres))
    m_ring = shapes(W, H, F(rings))
    # petal vein lines (cream)
    veins = []
    for cx, cy, R, rot in ((96, 104, 54, 0.2), (300, 296, 50, 0.6)):
        for i in range(8):
            a = rot + i / 8 * math.tau
            veins.append(([(cx + math.cos(a) * R * 0.4, cy + math.sin(a) * R * 0.4), (cx + math.cos(a) * R * 0.85, cy + math.sin(a) * R * 0.85)], 2.0, (0.1, 0.4)))
    birds = [bird(286, 168, 0.95, -1, 0.15), bird(118, 250, 0.9, 1, -0.2)]
    bodies, wings, tails, scal = [], [], [], []
    for b in birds:
        bodies += b["body"]; wings.append(b["wing"])
        tails += [(t, 9, (0.0, 0.6)) for t in [curve(tt, 24) for tt in b["tails"]]]
        scal += [(sc, 2.0, (0, 0)) for sc in b["scallops"]]
    wrap_items = (lambda items: [([(x + dx, y + dy) for x, y in pts], w_, tp) for pts, w_, tp in items for dx in (-W, 0, W) for dy in (-H, 0, H)]) if wrap else (lambda items: items)
    m_body = shapes(W, H, F(bodies))
    m_tail = strokes(W, H, wrap_items(tails))
    m_wing = shapes(W, H, F(wings))
    m_scal = strokes(W, H, wrap_items(scal))
    eyes = circles(W, H, [(b["eye"][0] + dx, b["eye"][1] + dy, 2.2) for b in birds for dx in ((-W, 0, W) if wrap else (0,)) for dy in ((-H, 0, H) if wrap else (0,))])
    stems, leaves = [], []
    for a in ((150, 70, 230, 20, 20), (20, 170, 60, 220, -14), (210, 260, 250, 380, 18), (340, 200, 390, 250, -10), (150, 150, 180, 120, 10), (240, 120, 210, 160, 8)):
        c, lv = sprig(*a, 4, 18)
        stems.append((c, 2.4, (0, 0)))
        leaves += lv
    m_stem = strokes(W, H, wrap_items(stems))
    m_leaf = shapes(W, H, F(leaves))
    m_veinl = strokes(W, H, wrap_items(veins))
    return [
        (np.maximum(m_leaf, m_stem), GREEN, None),
        (np.clip(m_flow - m_cent, 0, 1), INDIGO, m_veinl * m_flow),
        (np.clip(m_cent - m_ring, 0, 1), SOGA, None),
        (m_ring, RED_D, None),
        (np.maximum(m_body, m_tail), SOGA, eyes),
        (m_wing, INDIGO, m_scal),
    ]


def part_kain():
    W = H = 400
    rng = random.Random(5)
    art = batik_layers(W, H, motif_set(W, H, rng), 300, rng=rng)
    # a gentle dye mottle (seamless) — old gentongan cloth is never flat
    mot = wrap_noise(W, H, 77, 40)
    art[..., :3] *= (0.9 + 0.16 * mot)[..., None]
    rgb = art[..., :3]
    Image.fromarray((np.clip(np.tile(rgb, (2, 2, 1)), 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/bg-kain.png")
    rgb_save(rgb, f"{OUT}/kain.webp", quality=80)
    clear()


def part_tepi():
    """Border strip (repeat-x): indigo band with cream tumpal triangles and a soga sea-wave line, cream edge lines."""
    W, H = 240, 72
    rng = random.Random(8)
    art = dye(np.ones((H, W), np.float32), INDIGO, 801, 0.1)
    edge = rect(W, H, -5, 4, W + 5, 8) + rect(W, H, -5, H - 8, W + 5, H - 4)
    tris = []
    for k in range(-1, 5):
        x = k * 60
        tris.append([(x + 4, 56), (x + 56, 56), (x + 30, 14)])
        tris.append([(x + 30 + 4, 16), (x + 30 + 26, 16), (x + 30 + 15, 36)])
    m_tri = shapes(W, H, tris, smooth=False)
    art = over(art, dye(wdisp(np.clip(gaussian_filter(m_tri, 1.2) * 3, 0, 1), 803, 1.0), CREAM, 804, 0.04))
    inner = shapes(W, H, [[(x + 14, 50), (x + 46, 50), (x + 30, 24)] for x in range(-60, 300, 60)], smooth=False)
    art = over(art, dye(wdisp(inner, 805, 1.0), RED, 806, 0.1))
    wave = [(x, 46 + 4 * math.sin(x / 60 * math.tau)) for x in np.linspace(-10, W + 10, 80)]
    art = over(art, dye(wdisp(strokes(W, H, [(wave, 2.4, None)]), 807, 0.8), SOGA, 808, 0.05))
    art = over(art, dye(np.clip(edge, 0, 1), CREAM, 809, 0.05))
    cr = crackle(W, H, 810, n=14, length=60, width=0.8, wrap=True)
    art = over(art, tint(cr, "#0b1024", 0.4))
    rgb_save(art[..., :3], f"{OUT}/tepi.webp", quality=82)
    Image.fromarray((np.clip(np.tile(art[..., :3], (1, 3, 1)), 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/bg-tepi.png")
    clear()


def part_gentong():
    W, H = 520, 560
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    cx = 250
    # profile: rim, short neck, big belly, narrow foot
    prof = [(0, 0), (12, 6), (10, 28), (60, 70), (78, 150), (70, 240), (48, 320), (36, 352)]
    sc = 2.3
    right = [(cx + x * 1.3, 120 + y) for x, y in [(70, 0), (78, 10), (74, 30), (128, 80), (150, 170), (138, 260), (100, 330), (80, 360)]]
    jar = right + [(2 * cx - x, y) for x, y in right[::-1]]
    jm = poly(W, H, jar, smooth=True)
    shadow = ellipses(W, H, [(cx + 10, 486, 150, 14, 0)])
    art = G(art, shadow, "#2a1a12", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=6)
    art = body(art, jm, CLAY, CLAY_L, seed=nx(), shade=0.55, dark=CLAY_D, light=(0.28, 0.35), rough=1.4)
    # clay speckle + horizontal throwing rings
    sp = circles(W, H, [(rng.uniform(80, 420), rng.uniform(130, 500), rng.uniform(0.8, 1.8)) for _ in range(260)]) * jm
    art = OV(art, sp, lambda m: tint(m, CLAY_D, 0.5))
    rings_ = strokes(W, H, [(curve([(cx - 200, y), (cx, y + 10), (cx + 200, y)], 20), 2.2, (0.2, 0.2)) for y in (200, 236, 400)]) * jm
    art = G(art, rings_, CLAY_D, seed=nx(), density=0.4, edge=0.2, rough=1)
    # rim + indigo dye inside
    rim = ellipses(W, H, [(cx, 124, 100, 20, 0)])
    art = body(art, rim, CLAY_L, CLAY, seed=nx(), shade=0.3, dark=CLAY_D, rough=1)
    inside = ellipses(W, H, [(cx, 125, 86, 13, 0)])
    art = body(art, inside, INDIGO_D, INDIGO, seed=nx(), shade=0.2, rough=0.8)
    art = GP(art, ellipses(W, H, [(cx - 30, 123, 26, 3, -0.05)]), "#3c4f86", seed=nx(), rough=0.6)
    # indigo drips down the side
    drips = strokes(W, H, [(curve([(x, 150), (x + 2, 150 + L * 0.5), (x - 1, 150 + L)], 12), wdt, (0.0, 0.6)) for x, L, wdt in ((300, 80, 9), (330, 120, 8), (268, 50, 7))]) * jm
    art = G(art, drips, INDIGO, seed=nx(), density=0.75, edge=0.5, rough=1.5)
    # batik cloth draped over the left rim, hanging down the belly, edged with a cream line
    cloth = poly(W, H, [(150, 116), (204, 110), (220, 134), (196, 230), (186, 340), (196, 420), (128, 432), (104, 330), (90, 220), (120, 140)], smooth=True)
    tile = np.asarray(Image.open(f"{OUT}/kain.webp").convert("RGB"), np.float32) / 255
    big = np.tile(tile, (3, 3, 1))[:H, :W] if tile.shape[0] * 3 >= H else None
    pat = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).resize((W, H)), np.float32) / 255 if big is not None else None
    pat = np.asarray(Image.fromarray((np.tile(tile, (2, 2, 1)) * 255).astype(np.uint8)).resize((int(W * 0.9), int(H * 0.9))), np.float32) / 255
    canvas = np.zeros((H, W, 3), np.float32); canvas[:pat.shape[0], :pat.shape[1]] = pat
    cm = np.clip((gaussian_filter(displace(cloth, nx(), 2, 20), 0.7) - 0.3) * 2.5, 0, 1)
    # folds: darken vertical bands
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fold = 0.82 + 0.18 * np.sin(xx / 18 + yy / 120)
    clothrgb = canvas * fold[..., None]
    art = over(art, np.concatenate([clothrgb, cm[..., None]], -1))
    art = G(art, cm * np.clip(1 - radial(W, H, 150, 160, 260), 0, 1), RED_D, seed=nx(), density=0.4, edge=0.1, rough=1, feather=3)
    fringe = strokes(W, H, [([(x, 424 + (x - 120) * -0.15), (x + rng.uniform(-2, 2), 446 + (x - 120) * -0.15)], 2.2, (0, 0.4)) for x in range(132, 196, 6)])
    art = GP(art, fringe, CREAM, seed=nx(), rough=0.5)
    art = add_grain(art, seed=12, amount=0.03)
    preview(art, "bg-gentong", tone="#f3e9d6")
    save(art, f"{OUT}/gentong.webp", max_w=300, quality=82)
    clear()


def part_sekar():
    """Flower spray divider for light grounds: motifs filled with dye colours and outlined in indigo canting lines."""
    W, H = 640, 150
    rng = random.Random(11)
    flowers, centres = [], []
    p, (x, y, r) = flower(320, 75, 46, 8, 0.2)
    flowers += p
    centres.append([(x + math.cos(t) * r, y + math.sin(t) * r) for t in np.linspace(0, math.tau, 18, endpoint=False)])
    for cx, cy, R in ((150, 82, 18), (490, 70, 18), (60, 70, 11), (580, 84, 11)):
        p, (x, y, r) = flower(cx, cy, R, 6, rng.uniform(0, 1))
        flowers += p
        centres.append([(x + math.cos(t) * r, y + math.sin(t) * r) for t in np.linspace(0, math.tau, 14, endpoint=False)])
    stems, leaves = [], []
    for a in ((272, 80, 150, 84, -14), (150, 84, 40, 66, 12), (368, 72, 490, 70, 14), (490, 70, 610, 90, -12)):
        c, lv = sprig(*a, 4, 20)
        stems.append((c, 3, (0, 0)))
        leaves += lv
    m_flow = shapes(W, H, flowers)
    m_cent = shapes(W, H, centres)
    m_leaf = np.maximum(shapes(W, H, leaves), strokes(W, H, stems))
    allm = np.maximum(np.maximum(m_flow, m_cent), m_leaf)
    art = blank(W, H)
    nx = Seq(1100)
    art = GP(art, np.clip(gaussian_filter(allm, 1.6) * 3, 0, 1), INDIGO, seed=nx(), rough=1.0)
    art = GP(art, np.clip(m_leaf - 0.0, 0, 1) * (1 - np.clip(gaussian_filter(1 - m_leaf, 0.8) * 2, 0, 1)), GREEN, seed=nx(), rough=0.8)
    inner = lambda m: np.clip(m - np.clip(gaussian_filter(1 - m, 1.0) * 2.4, 0, 1), 0, 1)
    art = GP(art, inner(np.clip(m_flow - m_cent, 0, 1)), RED, seed=nx(), rough=0.8)
    art = GP(art, inner(m_cent), SOGA, seed=nx(), rough=0.6)
    dots = circles(W, H, [(x, y, 1.6) for x, y in [(rng.uniform(20, 620), rng.uniform(20, 130)) for _ in range(60)]]) * (1 - np.clip(gaussian_filter(allm, 4) * 4, 0, 1))
    art = GP(art, dots, SOGA, seed=nx(), rough=0.4)
    cr = crackle(W, H, 1190, n=30, length=40, width=0.8) * allm
    art = OV(art, cr, lambda m: tint(m, INDIGO_D, 0.45))
    preview(art, "bg-sekar", tone="#f3e9d6")
    save(art, f"{OUT}/sekar.webp", max_w=320, quality=84)
    clear()


def part_burung():
    W, H = 420, 300
    b = bird(250, 170, 1.9, 1, -0.12)
    tails = [(curve(t, 30), 18, (0.0, 0.6)) for t in b["tails"]]
    m_body = shapes(W, H, b["body"])
    m_tail = strokes(W, H, tails)
    m_wing = shapes(W, H, [b["wing"]])
    m_scal = strokes(W, H, [(sc, 3.4, (0, 0)) for sc in b["scallops"]])
    eye = circles(W, H, [(b["eye"][0], b["eye"][1], 4)] + [(250 + k * 14 - 30, 196 - k * 2, 2.6) for k in range(5)])
    tail_lines = strokes(W, H, [(curve(t, 30)[2:-6], 2.6, (0.1, 0.3)) for t in b["tails"]])
    allm = np.maximum.reduce([m_body, m_tail, m_wing])
    nx = Seq(1300)
    art = blank(W, H)
    art = GP(art, np.clip(gaussian_filter(allm, 2.2) * 3, 0, 1), INDIGO, seed=nx(), rough=1.0)
    inner = lambda m, k=1.2: np.clip(m - np.clip(gaussian_filter(1 - m, k) * 2.4, 0, 1), 0, 1)
    art = GP(art, inner(np.maximum(m_body, m_tail)), SOGA, "#a0662f", seed=nx(), rough=0.8)
    art = GP(art, inner(m_wing, 1.4), RED, seed=nx(), rough=0.8)
    art = GP(art, np.maximum(m_scal * m_wing, tail_lines * m_tail), CREAM, seed=nx(), rough=0.5)
    art = GP(art, eye, CREAM, seed=nx(), rough=0.3)
    cr = crackle(W, H, 1390, n=26, length=50, width=0.9) * allm
    art = OV(art, cr, lambda m: tint(m, INDIGO_D, 0.45))
    preview(art, "bg-burung", tone="#f3e9d6")
    save(art, f"{OUT}/burung.webp", max_w=240, quality=84)
    clear()


for p in PARTS:
    globals()[f"part_{p}"]()
kb_report(OUT)
