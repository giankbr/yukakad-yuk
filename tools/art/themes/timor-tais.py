"""Timor Tais — tais cloth of West Timor (warp ikat + supplementary weft, deep red / black / orange / white), round
ume kbubu houses, lontar palms on a savanna under a blue sky. Run: python3 -I timor-tais.py [part ...]
parts: tais band rumbai padang ume. Assets -> public/themes/art/timor-tais/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h2_lib import *
from scipy.ndimage import map_coordinates

OUT = outdir("timor-tais")
PARTS = sys.argv[1:] or ["tais", "band", "rumbai", "padang", "ume"]
RED, RED_D, BLACK, ORANGE, YEL, WHITE, INDIGO = "#9b2319", "#6e150f", "#1c1412", "#e0782a", "#efb247", "#efe3cc", "#27304a"
CREAM = "#f4ecdf"


def tais_tile(W=240, H=480, seed=5):
    """Seamless (vertical) tais strip, warp running vertically. Returns RGB float array HxWx3."""
    rng = random.Random(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lay = np.zeros((H, W), np.int32)  # colour index map
    cols = [RED, BLACK, ORANGE, WHITE, YEL, RED_D, INDIGO]
    # warp stripes (x ranges -> colour)
    stripes = [(0, 7, 1), (7, 10, 2), (10, 12, 3), (12, 15, 2), (15, 44, 0), (44, 47, 1), (47, 50, 4), (50, 53, 1), (53, 62, 5),
               (62, 66, 1), (66, 69, 2), (69, 72, 1)]
    for a, b, c in stripes:
        lay[:, a:b] = c
        lay[:, W - b:W - a] = c
    lay[:, 72:W - 72] = 1  # black ikat panel ground
    # warp-ikat motifs in the centre panel: stacked hooked diamonds (kaif) and arrow rows, period 120px
    cx = W / 2
    P = 120
    ik = np.zeros((H, W), np.float32); ik2 = np.zeros((H, W), np.float32); dots = np.zeros((H, W), np.float32)
    for k in range(-1, H // P + 2):
        y0 = k * P + P / 2
        d = np.abs(xx - cx) / 40 + np.abs(yy - y0) / 54
        ring = ((d > 0.62) & (d < 1.0)).astype(np.float32)
        core = (d < 0.3).astype(np.float32)
        ik = np.maximum(ik, ring); ik2 = np.maximum(ik2, core)
        # hooks off the diamond tips (left/right)
        for sgn in (-1, 1):
            hx = cx + sgn * 40
            hook = ((np.abs(xx - (hx + sgn * 6)) < 4) & (np.abs(yy - y0 - 8) < 12)) | ((np.abs(yy - (y0 + 18)) < 4) & (np.abs(xx - (hx - sgn * 2)) < 10))
            ik = np.maximum(ik, hook.astype(np.float32))
        # chevron rows between diamonds
        yc = y0 + P / 2
        chev = (np.abs((yy - yc) + np.abs(xx - cx) * 0.45) < 3.2) & (np.abs(xx - cx) < 44)
        ik2 = np.maximum(ik2, chev.astype(np.float32))
    # ikat blur: each warp column is shifted slightly (threads slide when tied/dyed) -> feathered vertical edges
    off = (wrap_noise(W, 1, seed, 0)[0] - 0.5) * 10
    off2 = gaussian_filter(np.random.default_rng(seed + 1).random(W).astype(np.float32), 1.0) * 6
    shift = (off + off2)[None, :] * np.ones((H, 1), np.float32)
    def ikat(m):
        return map_coordinates(m, [(yy + shift) % H, xx], order=1, mode="wrap")
    ik, ik2 = ikat(ik), ikat(ik2)
    inner = (np.abs(xx - cx) < W / 2 - 74).astype(np.float32)
    # supplementary weft (buna) small motifs on the red side stripes: little stepped lozenges every 24px
    for k in range(H // 24 + 1):
        y0 = k * 24 + 12
        for x0 in (29.5, W - 29.5):
            dd = np.abs(xx - x0) / 9 + np.abs(yy - y0) / 7
            dots = np.maximum(dots, ((dd < 1.0) & (dd > 0.45)).astype(np.float32))
    rgb = np.zeros((H, W, 3), np.float32)
    for i, c in enumerate(cols):
        rgb[lay == i] = hex_rgb(c)
    def put(m, c, a=1.0):
        nonlocal rgb
        m = np.clip(m, 0, 1)[..., None] * a
        rgb = rgb * (1 - m) + np.array(hex_rgb(c), np.float32) * m
    put(ik * inner, RED)
    put(ik2 * inner, ORANGE)
    # white highlight dashes inside the diamond cores (weft floats)
    put(ikat(((np.abs(np.sin(yy / H * math.tau * 16)) > 0.85) & (np.abs(xx - cx) < 5)).astype(np.float32)) * ik2 * inner, WHITE, 0.9)
    put(dots, YEL, 0.95)
    # weave texture: warp threads (vertical) + weft picks (horizontal) + mottle, all periodic in y
    warp = 0.5 + 0.5 * np.sin(xx * math.tau / 2.6)
    weft = 0.5 + 0.5 * np.sin(yy * math.tau / (H / 160))
    mott = wrap_noise(W, H, seed + 3, 6) - 0.5
    slub = wrap_noise(W, H, seed + 4, (14, 0.8)) - 0.5
    k = 1 - 0.13 * warp * weft - 0.06 * (1 - warp) + mott * 0.10 + slub * 0.08
    rgb = np.clip(rgb * k[..., None], 0, 1)
    return rgb


if "tais" in PARTS:
    W, H = 240, 480
    rgb = tais_tile(W, H)
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/tais.webp", quality=82)
    Image.fromarray((np.vstack([rgb, rgb]) * 255).astype(np.uint8)).save(f"{PREV}/tt-tais.png")
    clear()

if "band" in PARTS:
    # a short horizontal tais strip (rotated) with tied tassels on both ends: section divider
    rgb = tais_tile(240, 480, seed=9)
    rgb = np.rot90(rgb[:480], 1)[:, :]  # 240 tall x 480 wide
    rgb = rgb[60:180, :]  # keep the ikat panel + side stripes (120 tall)
    rgb = np.array(Image.fromarray((rgb * 255).astype(np.uint8)).resize((480, 76), Image.LANCZOS), np.float32) / 255
    W, H = 640, 96
    art = blank(W, H)
    x0 = 80
    art[10:86, x0:x0 + 480, :3] = rgb
    art[10:86, x0:x0 + 480, 3] = 1
    # slightly ragged cloth edges
    edge = np.ones((H, W), np.float32)
    art[..., 3] *= displace(art[..., 3], 3, 1.2, 8)
    # tassels: bundles of threads gathered and bound
    items_r, items_k, items_o = [], [], []
    rng = random.Random(4)
    for side in (-1, 1):
        bx = x0 if side < 0 else x0 + 480
        for j in range(5):
            y = 16 + j * 16
            tip = (bx + side * rng.uniform(56, 74), y + rng.uniform(-4, 4))
            for t in range(6):
                pts = curve([(bx, y - 4 + t * 1.6), (bx + side * 20, y - 2 + t * 0.8), tip], 14)
                (items_r if t % 3 == 0 else items_k if t % 3 == 1 else items_o).append((pts, 1.3, (0.0, 0.5)))
    art = GP(art, strokes(W, H, items_r), RED, RED_D, seed=21, rough=0.6, pad=6)
    art = GP(art, strokes(W, H, items_k), BLACK, seed=22, rough=0.6, pad=6)
    art = GP(art, strokes(W, H, items_o), ORANGE, seed=23, rough=0.6, pad=6)
    binds = shapes(W, H, [[(x0 - 20, 6), (x0 - 12, 6), (x0 - 12, 90), (x0 - 20, 90)], [(x0 + 492, 6), (x0 + 500, 6), (x0 + 500, 90), (x0 + 492, 90)]], smooth=False)
    art = GP(art, binds * 0, BLACK, seed=24, pad=6)
    preview(art, "tt-band", CREAM)
    save(art, f"{OUT}/band.webp", max_w=420, quality=82)
    clear()

if "rumbai" in PARTS:
    # fringe at the end of the hanging tais (matches the strip width 240)
    W, H = 240, 120
    rng = random.Random(7)
    items = {RED: [], BLACK: [], ORANGE: [], WHITE: []}
    seq = [BLACK, BLACK, ORANGE, WHITE, ORANGE] + [RED] * 6 + [BLACK, YEL if False else ORANGE, BLACK, RED, RED] + [BLACK] * 4
    for i, x in enumerate(np.arange(2, W - 1, 2.2)):
        col = RED if 15 <= x <= 44 or W - 44 <= x <= W - 15 else BLACK if (x < 8 or x > W - 8 or 72 <= x <= W - 72) else ORANGE if (x < 15 or x > W - 15) else RED_D
        col = col if col != RED_D else RED
        L = 70 + rng.uniform(-14, 22)
        sway = rng.uniform(-4, 4)
        items.setdefault(col, []).append((curve([(x, 0), (x + sway * 0.3, L * 0.5), (x + sway, L)], 10), 1.5, (0.0, 0.25)))
    art = blank(W, H)
    for col, it in items.items():
        if it:
            art = GP(art, strokes(W, H, it), col, mix(col, "#000000", 0.25), seed=len(it), rough=0.5, streak=0.8, pad=4)
    # knotted band at the top
    knot = shapes(W, H, [[(0, 0), (W, 0), (W, 7), (0, 7)]], smooth=False)
    art = GP(art, knot, BLACK, seed=31, rough=0.6, pad=4)
    preview(art, "tt-rumbai", CREAM)
    save_full(art, f"{OUT}/rumbai.webp", quality=82)
    clear()


def ume_mask(W, H, x, by, w, h):
    """Ume kbubu: thatched cone-dome reaching (almost) to the ground, low doorway, knob on top. -> (thatch, door, eave)"""
    pts = [(x - w / 2, by)] + [(x - w / 2 * (1 - t) ** 0.9 * (1 + 0.06 * math.sin(t * 3.1)) , by - h * (1 - (1 - t) ** 1.6)) for t in np.linspace(0.02, 0.98, 18)] + [(x, by - h - h * 0.04)]
    right = [(2 * x - px, py) for px, py in reversed(pts[:-1])]
    thatch = shapes(W, H, [pts + right], smooth=True)
    door = shapes(W, H, [[(x - w * 0.07, by), (x - w * 0.07, by - h * 0.2), (x, by - h * 0.25), (x + w * 0.07, by - h * 0.2), (x + w * 0.07, by)]], smooth=False)
    knob = shapes(W, H, [deform(ellipse_pts(x, by - h - h * 0.06, w * 0.035, h * 0.06, 10), random.Random(int(x)), 1, 0.1)])
    return np.clip(thatch, 0, 1), door, knob


def thatch_strokes(W, H, x, by, w, h, rng):
    items = []
    for k in range(int(w * 1.3)):
        u = rng.uniform(-0.5, 0.5)
        t0 = rng.uniform(0.0, 0.85)
        yb = by - h * (1 - (1 - t0) ** 1.6)
        xb = x + u * w * (1 - t0) ** 0.9
        L = h * rng.uniform(0.1, 0.22)
        items.append(([(xb - u * L * 0.25, yb - L), (xb + u * L * 0.15, yb)], rng.uniform(0.9, 1.8), (0.1, 0.4)))
    return strokes(W, H, items)


def lontar_paint(art, W, H, x, by, h, rng, nx, lean=0.0, tone=0.0):
    """Lontar (borassus) palm: tall straight grey trunk, dense globe of stiff fan leaves (painted fan by fan)."""
    top = (x + lean * h, by - h)
    trunk = strokes(W, H, [(curve([(x, by), (x + lean * h * 0.5, by - h * 0.5), top], 20), h * 0.042, (0.0, 0.12))])
    art = GP(art, trunk, mix("#4a3e34", "#8b8478", tone), mix("#2e2620", "#6f685e", tone), seed=nx(), rough=1.0, pad=8)
    # ring scars on the trunk
    rings = strokes(W, H, [([(x + lean * h * (1 - (by - y) / h * 0) - h * 0.02 + lean * (by - y), y), (x + lean * (by - y) + h * 0.02, y + 1)], 1.0, None) for y in np.arange(by - h * 0.9, by, h * 0.04)]) * trunk
    art = GP(art, rings, mix("#2a221c", "#5f584f", tone), seed=nx(), rough=0.4, density=0.6, pad=6)
    R = h * 0.2
    dark, mid, light = mix("#2f3b1f", "#6f7a5a", tone), mix("#55663a", "#8f9a74", tone), mix("#8a9a5a", "#b7bf98", tone)
    order = sorted(range(22), key=lambda k: rng.random())
    for layer, col in ((0, dark), (1, mid), (2, light)):
        fans = []
        for k in order[layer * 7:(layer + 1) * 7 + 1]:
            a = -math.pi * 1.15 + (k / 21) * math.pi * 1.3 + rng.uniform(-0.2, 0.2)
            L = R * rng.uniform(0.15, 0.55) * (1 - 0.2 * layer)
            ex, ey = top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.75 - R * 0.08 * layer
            rr = R * rng.uniform(0.5, 0.72)
            span = rng.uniform(1.8, 2.5)
            pts = [(ex - math.cos(a) * rr * 0.2, ey - math.sin(a) * rr * 0.2)]
            for jj in range(17):
                aa = a + (jj / 16 - 0.5) * span
                rad = rr * (0.78 + 0.22 * (jj % 2))
                pts.append((ex + math.cos(aa) * rad, ey + math.sin(aa) * rad))
            fans.append(pts)
        fm = shapes(W, H, fans, smooth=False)
        art = GP(art, fm, col, mix(col, "#1d2412", 0.25), seed=nx(), rough=1.6, streak=1.2, pad=8)
    dead = [([(top[0] + u * R * 0.3, top[1] + R * 0.1), (top[0] + u * R * 0.42, top[1] + R * rng.uniform(0.5, 0.75))], R * 0.07, (0.0, 0.6)) for u in np.linspace(-1, 1, 7)]
    art = GP(art, strokes(W, H, dead), mix("#6a5232", "#a39377", tone), mix("#3f3020", "#857a62", tone), seed=nx(), rough=1.2, streak=1.0, pad=6)
    return art


def ume_paint(art, W, H, x, by, w, h, rng, nx):
    th, door, knob = ume_mask(W, H, x, by, w, h)
    sh = shapes(W, H, [deform(ellipse_pts(x + w * 0.12, by + 2, w * 0.62, h * 0.06, 14), rng, 1, 0.08)])
    art = G(art, sh, "#6b4a22", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=3)
    art = GP(art, th, "#c9a466", "#a98348", seed=nx(), rough=2.2, streak=1.0, pad=10)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # layered thatch tiers: darker bands under each tier lip
    tiers = np.zeros((H, W), np.float32)
    for t in np.linspace(0.1, 0.7, 4):
        yt = by - h * (1 - (1 - t) ** 1.6)
        tiers = np.maximum(tiers, np.clip((yy - yt) / (h * 0.09), 0, 1) * np.clip((yt + h * 0.1 - yy) / (h * 0.02), 0, 1))
    art = G(art, np.clip(tiers, 0, 1) * th, "#6c4e26", seed=nx(), density=0.45, edge=0.15, bloom=0, rough=2.5, feather=1.4)
    side = th * np.clip((xx - x) / (w * 0.5), 0, 1) ** 1.3
    art = G(art, side, "#5a4024", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=2)
    art = GP(art, thatch_strokes(W, H, x, by, w, h, rng) * th, "#ecd39b", "#7a5a30", seed=nx(), rough=0.5, density=0.8, pad=6)
    art = GP(art, door, "#2b1b10", seed=nx(), rough=0.8, pad=6)
    art = GP(art, knob, "#5a4024", seed=nx(), rough=0.6, pad=6)
    return art


if "padang" in PARTS:
    W, H = 820, 560
    nx = Seq(7100); rng = random.Random(71)
    art = blank(W, H)
    # far blue hills, golden savanna slopes
    art = GP(art, hills(W, H, 300, 26, 3, 0.9), "#7d97b3", "#6c88a6", seed=nx(), rough=3, streak=0.6)
    art = GP(art, hills(W, H, 330, 30, 5, 0.6), "#c2a75e", "#a9934e", seed=nx(), rough=3, streak=0.7)
    # lontar palms (behind huts), various heights
    for (x, by, h, ln, tone) in [(300, 352, 150, 0.02, 0.55), (520, 350, 170, 0.0, 0.5), (165, 360, 230, 0.03, 0.3), (640, 362, 260, 0.02, 0.2), (80, 384, 310, -0.02, 0.0), (738, 384, 330, -0.03, 0.0)]:
        art = lontar_paint(art, W, H, x, by, h, rng, nx, ln, tone)
    # near savanna ground
    ground = hills(W, H, 400, 22, 8, 1.2)
    art = GP(art, ground, "#dcae58", "#c08f3c", seed=nx(), rough=3, streak=1.0)
    grass = strokes(W, H, [([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(10, 28))], rng.uniform(1.0, 2.0), (0.0, 0.6)) for x, y in [(rng.uniform(0, W), rng.uniform(395, H)) for _ in range(900)]])
    art = GP(art, grass * ground, "#9c6f2a", "#e2bd6c", seed=nx(), rough=0.5, density=0.8, pad=6)
    # ume kbubu cluster with a stone fence
    for (x, by, w, h) in [(250, 440, 170, 150), (590, 446, 160, 140), (420, 462, 220, 200)]:
        art = ume_paint(art, W, H, x, by, w, h, rng, nx)
    stones = []
    for x in np.arange(60, 780, 22):
        y = 500 + 8 * math.sin(x / 90)
        stones.append(deform(ellipse_pts(x + rng.uniform(-3, 3), y + rng.uniform(-2, 2), rng.uniform(11, 14), rng.uniform(7, 9), 9), rng, 1, 0.15))
        stones.append(deform(ellipse_pts(x + 11 + rng.uniform(-3, 3), y - 13 + rng.uniform(-2, 2), rng.uniform(9, 12), rng.uniform(6, 8), 9), rng, 1, 0.15))
    st = shapes(W, H, stones)
    art = GP(art, st, "#d9cdb4", "#a89a80", seed=nx(), rough=0.4, density=1.0, pad=8)
    art = G(art, st * np.clip((fbm(W, H, 5, 6, 2) - 0.5) * 3, 0, 1), "#6e6658", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8)
    preview(art, "tt-padang", "#9cc3e3")
    save(art, f"{OUT}/padang.webp", max_w=720, quality=78)
    clear()

if "ume" in PARTS:
    W, H = 300, 260
    nx = Seq(7300); rng = random.Random(73)
    art = blank(W, H)
    base = shapes(W, H, [deform(ellipse_pts(150, 236, 130, 14, 16), rng, 1, 0.08)])
    art = GP(art, base, "#c89a48", "#a97c34", seed=nx(), rough=2)
    th, door, knob = ume_mask(W, H, 150, 236, 200, 196)
    art = GP(art, th, "#b08a52", "#8a6a3c", seed=nx(), rough=2.5, streak=1.0)
    sh = th * np.clip((np.mgrid[0:H, 0:W][1] - 150) / 100, 0, 1)
    art = G(art, sh, "#5a4024", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=2)
    art = GP(art, thatch_strokes(W, H, 150, 236, 200, 196, rng) * th, "#e0c387", "#6c4f2a", seed=nx(), rough=0.5, density=0.75)
    # a strip of tais tied around (as at ceremonies)
    band = th * ((np.mgrid[0:H, 0:W][0] > 150) & (np.mgrid[0:H, 0:W][0] < 166))
    art = GP(art, band, RED, RED_D, seed=nx(), rough=0.8)
    art = GP(art, th * ((np.mgrid[0:H, 0:W][0] > 155) & (np.mgrid[0:H, 0:W][0] < 160)), ORANGE, seed=nx(), rough=0.6)
    art = GP(art, door, "#2b1b10", seed=nx(), rough=0.8)
    art = GP(art, knob, "#5a4024", seed=nx(), rough=0.6)
    preview(art, "tt-ume", CREAM)
    save(art, f"{OUT}/ume.webp", max_w=240, quality=84)
    clear()
