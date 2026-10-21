"""Tenun NTT — Sumba-style warp ikat rendered at thread level (warp slip blur, plain-weave relief) in indigo/rust/cream with
original geometric horse & rooster motifs; Mbaru Niang conical houses (Wae Rebo) and savanna hills in gouache/watercolour.
Run: python3 -I ntt-tenun.py [part ...]   parts: band col tile kuda ayam scene"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *
from scipy.ndimage import binary_dilation

OUT = outdir("ntt-tenun")
PARTS = sys.argv[1:] or ["band", "col", "tile", "kuda", "ayam", "scene"]
INDIGO, INDIGO_D, RUST, CREAM, OCHRE = "#22305a", "#151d38", "#a8492a", "#efe4cf", "#c99a52"
PAL = [INDIGO, RUST, CREAM, OCHRE, INDIGO_D]

HORSE = [
    "....##..................",
    "...####.................",
    "..##.###................",
    ".##...###...............",
    "......####..............",
    ".......###############..",
    ".......################.",
    ".......#####yyyy#######.",
    "........##############.#",
    ".......###..........##.#",
    "......##.##........##...",
    ".....##...##......##....",
    "....##.....##....##.....",
    "...##.......##..##......",
    "..##.........##.##......",
]
ROOSTER = [
    "...#.#...........##",
    "..#####.........###",
    "..##.##........##.#",
    ".###.##.......##...",
    "#..####......##..##",
    "....#####...##..##.",
    "....###########.#..",
    "....############...",
    ".....##yyyy####....",
    "......########.....",
    ".......######......",
    "........#..#.......",
    "........#..#.......",
    ".......##.##.......",
]


def outline_grid(g, body=1, ring=2):
    m = g == body
    d = binary_dilation(m | (g == 3), iterations=1) & (g == 0)
    out = g.copy(); out[d] = ring
    return out


def put(g, glyph, y, x, flip=False):
    rows = [r[::-1] for r in glyph] if flip else glyph
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                g[y + j, x + i] = 1
            elif ch == "y":
                g[y + j, x + i] = 3


def border_rows(g, y, flip=False):
    """Rust/cream stripes + cream zigzag on indigo (4 + 4 rows)."""
    w = g.shape[1]
    rows = [1, 1, 2, 0, None, None, None, 0] if not flip else [0, None, None, None, 0, 2, 1, 1]
    for k, v in enumerate(rows):
        if v is not None:
            g[y + k, :] = v
    zz = y + (4 if not flip else 1)
    for x in range(w):
        p = x % 6
        hgt = [0, 1, 2, 2, 1, 0][p]
        for j in range(hgt + 1):
            yy = zz + (j if not flip else 2 - j)
            g[yy, x] = 2 if hgt >= 1 else 0
    return g


if "band" in PARTS:
    # Horizontal band: border / horse-rooster-horse-rooster / border. Period 96 cells.
    P = 96; Hc = 8 + 19 + 8
    g = np.zeros((Hc, P), np.int32)
    border_rows(g, 0)
    border_rows(g, Hc - 8, True)
    put(g, HORSE, 10, 2)
    put(g, ROOSTER, 10, 28)
    put(g, HORSE, 10, 50, flip=True)
    put(g, ROOSTER, 10, 76, flip=True)
    g = outline_grid(g)
    art = ikat_render(g, PAL, thread=4, blur=1.1, seed=51)
    preview(art, "nt-band")
    save_full(art, f"{OUT}/band.webp", quality=80)
    clear()

if "col" in PARTS:
    # Vertical column (cover sides): stripes left/right, stacked upright horse / diamond / rooster. Period 58 rows.
    Wc = 30; P = 58
    g = np.zeros((P, Wc), np.int32)
    g[:, 0] = 1; g[:, 1] = 2; g[:, Wc - 1] = 1; g[:, Wc - 2] = 2
    put(g, HORSE, 2, 3)
    # diamond with hooks
    cx, cy = Wc // 2, 24
    for j in range(-5, 6):
        for i in range(-9, 10):
            r = abs(i) / 9 * 5 + abs(j)
            if 4.2 <= r <= 5.2:
                g[cy + j, cx + i] = 1
            elif r < 2.2:
                g[cy + j, cx + i] = 3
    put(g, ROOSTER, 34, 5)
    for x in range(2, Wc - 2):
        if x % 4 < 2:
            g[P - 2, x] = 2
    g = outline_grid(g)
    art = ikat_render(g, PAL, thread=4, blur=1.1, seed=52)
    preview(art, "nt-col")
    save_full(art, f"{OUT}/col.webp", quality=80)
    clear()

if "tile" in PARTS:
    # Seamless background cloth: diamond lattice with hooked arms and small cream crosses (indigo ground). 48x48 cells.
    T = 48
    g = np.zeros((T, T), np.int32)
    for y in range(T):
        for x in range(T):
            u, v = (x % 24) - 12, (y % 24) - 12
            r = abs(u) + abs(v)
            if r in (11, 12):
                g[y, x] = 1
            elif r in (6,):
                g[y, x] = 2
            elif r <= 2:
                g[y, x] = 3
    # stripe pairs every 24 rows (warp-faced bands)
    g[0, :] = 2
    art = ikat_render(g, [INDIGO, RUST, "#d8c9ad", OCHRE, INDIGO_D], thread=3, blur=1.3, seed=53)
    art[..., :3] *= 0.82
    preview(art, "nt-tile")
    save_full(art, f"{OUT}/tile.webp", quality=74)
    clear()

for name, glyph, gw in (("kuda", HORSE, 24), ("ayam", ROOSTER, 19)):
    if name not in PARTS:
        continue
    # standalone woven patch (cut motif with frayed fringe), used as ornament
    pad = 3
    g = np.zeros((len(glyph) + pad * 2, gw + pad * 2), np.int32)
    put(g, glyph, pad, pad)
    g = outline_grid(g)
    art = ikat_render(g, PAL, thread=7, blur=0.8, seed=54 if name == "kuda" else 55)
    h, w = art.shape[:2]
    rng = random.Random(56)
    # torn/fringed edge: alpha mask with ragged border + hanging warp threads at the bottom
    a = np.ones((h, w), np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    rag = fbm(w, h, 57, 6, 2) * 4
    a *= np.clip((np.minimum.reduce([xx, w - 1 - xx, yy]) - rag) / 2, 0, 1)
    art[..., 3] = a
    full = blank(w, h + 26); full[:h] = art
    fr = []
    for x in range(1, w, 6):
        L = 16 + rng.uniform(-4, 8)
        fr.append(([(x + 2, h - 2), (x + 2 + rng.uniform(-1.5, 1.5), h - 2 + L)], 2.2, (0.0, 0.5)))
    full = OV(full, strokes(w, h + 26, fr), lambda m: rgba(INDIGO, m * 0.95), pad=4)
    preview(full, f"nt-{name}")
    save(full, f"{OUT}/{name}.webp", max_w=200 if name == "kuda" else 170, quality=84)
    clear()


def niang(W, H, cx, by, w, h):
    """Mbaru Niang masks: tall, slightly convex conical thatch roof reaching close to the ground, dark door, short posts."""
    L, R = [], []
    for i in range(31):
        u = i / 30  # 0 base .. 1 apex
        half = w / 2 * (1 - u) ** 0.78
        y = by - h * u
        L.append((cx - half, y)); R.append((cx + half, y))
    base = [(cx + w / 2, by), (cx + w * 0.3, by + h * 0.035), (cx, by + h * 0.045), (cx - w * 0.3, by + h * 0.035), (cx - w / 2, by)]
    roof = shapes(W, H, [L + R[::-1] + base])
    door = shapes(W, H, [[(cx - w * 0.06, by + h * 0.04), (cx - w * 0.06, by - h * 0.07), (cx, by - h * 0.095), (cx + w * 0.06, by - h * 0.07), (cx + w * 0.06, by + h * 0.04)]])
    posts = strokes(W, H, [([(cx + w * k, by + h * 0.02), (cx + w * k, by + h * 0.085)], max(2.5, w * 0.022), None) for k in (-0.36, -0.18, 0.18, 0.36)])
    tip = strokes(W, H, [([(cx, by - h * 0.99), (cx, by - h * 1.09)], max(2.5, w * 0.03), None),
                         (curve([(cx - w * 0.08, by - h * 1.13), (cx, by - h * 1.075), (cx + w * 0.08, by - h * 1.13)], 10), max(2.0, w * 0.022), None)])
    return roof, door, posts, tip


if "scene" in PARTS:
    PADX = 40
    W, H = 900 + PADX * 2, 600
    rng = random.Random(61); nx = Seq(61000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # far ridges: violet-grey, two wet washes; dusk glow along the top
    far = ridge_mask(W, H, 230, 70, 3, freq=2.0, sharp=0.75)
    art = G(art, far, "#8a8fb0", "#a6a2b8", seed=nx(), density=0.7, edge=0.45, bloom=0.5, rough=9)
    art = G(art, far * np.clip((yy - 200) / 120, 0, 1), "#6d7699", seed=nx(), density=0.45, edge=0.2, bloom=0.5, rough=6)
    art = OV(art, gaussian_filter(far - ridge_mask(W, H, 238, 70, 3, freq=2.0, sharp=0.75), 3).clip(0, 1) * 2, lambda m: rgba("#f0c68a", m * 0.12))
    # mid hills: green-gold with dark tree clumps
    mid = ridge_mask(W, H, 300, 50, 7, freq=2.8, sharp=0.9)
    art = G(art, mid, "#b89a58", "#8f8a4a", seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=8)
    clumps = [(rng.uniform(0, W), rng.uniform(300, 350), rng.uniform(8, 18)) for _ in range(26)]
    art = G(art, circles(W, H, clumps) * mid, "#4d5a34", "#38452a", seed=nx(), density=0.75, edge=0.6, bloom=0.2, rough=4)
    # savanna: warm gold, wet-in-wet bloom, rows of light dry-brush grass
    sav = ridge_mask(W, H, 372, 38, 11, freq=2.2, sharp=1.0)
    art = G(art, sav, "#e4b864", "#c98f3a", seed=nx(), density=0.9, edge=0.45, bloom=0.45, rough=8)
    art = G(art, sav * np.clip((yy - 380) / 90, 0, 1), "#b5793a", seed=nx(), density=0.4, edge=0.1, bloom=0.5, rough=6)
    gl = hair_strokes(sav * np.clip((480 - yy) / 60, 0, 1), 520, 16, 1.4, -1.5, rng, 0.18)
    art = OV(art, strokes(W, H, gl), lambda m: rgba("#f7dd98", m * 0.5))
    # lontar palms: straight trunks, ball crowns of fan leaves
    for (x, by, hh) in [(150, 360, 150), (188, 366, 110), (760, 352, 140), (812, 362, 96), (560, 340, 80)]:
        trunk = strokes(W, H, [([(x, by), (x + 2, by - hh)], max(3, hh * 0.035), (0.0, 0.15))])
        art = GP(art, trunk, "#4a3a2a", "#2a2018", seed=nx(), rough=0.5, pad=6)
        cx_, cy_ = x + 2, by - hh
        fans = []
        for k in range(30):
            a = rng.uniform(0, math.tau)
            L = hh * rng.uniform(0.16, 0.24)
            ex, ey = cx_ + math.cos(a) * L, cy_ + math.sin(a) * L * 0.85
            for f in range(5):
                fa = a + (f - 2) * 0.12
                fans.append(([(cx_ + math.cos(a) * L * .25, cy_ + math.sin(a) * L * .2), (cx_ + math.cos(fa) * L, cy_ + math.sin(fa) * L * 0.85)], max(1.2, hh * 0.012), (0.1, 0.4)))
        fm = strokes(W, H, fans)
        art = GP(art, fm, "#4f6038", "#2c3a22", seed=nx(), rough=0.6, density=0.95, pad=6)
        art = OV(art, fm * np.clip((cx_ - xx) / (hh * 0.25), 0, 1), lambda m: rgba("#c8b46a", m * 0.45))
    # foreground slope
    fg = ridge_mask(W, H, 470, 24, 19, freq=1.3, sharp=1.0)
    art = G(art, fg, "#8e9150", "#6b7438", seed=nx(), density=0.95, edge=0.35, bloom=0.4, rough=8)
    art = G(art, fg * np.clip((yy - 500) / 100, 0, 1), "#4d5a2a", seed=nx(), density=0.7, edge=0.1, bloom=0.4, rough=6)
    # Mbaru Niang (back to front)
    houses = [(330, 452, 118, 140), (630, 448, 122, 144), (480, 476, 196, 230), (210, 506, 158, 184), (760, 506, 162, 188)]
    for k, (cx, by, w, h) in enumerate(houses):
        roof, door, posts, tip = niang(W, H, cx, by, w, h)
        art = OV(art, gaussian_filter(np.roll(np.roll(roof, 8, 1), 4, 0), 7), lambda m: rgba("#2a2418", m * 0.5))
        art = GP(art, posts, "#3a2a1c", seed=nx(), rough=0.4, pad=6)
        art = GP(art, roof, "#8f7b60", "#6a5640", seed=nx(), rough=1.6, streak=1.3)
        rel = (xx - cx) / (w * 0.5)
        art = OV(art, np.clip(rel * 1.1 + 0.15, 0, 1) ** 0.8 * roof, lambda m: rgba("#2a1f16", m * 0.7))
        art = OV(art, np.clip(-rel, 0, 1) ** 1.5 * roof, lambda m: rgba("#f0cf8e", m * 0.4))
        # thatch: overlapping fringe tiers (short downward strokes along each tier edge) + tier shadow
        fr_d, fr_l, tl = [], [], []
        ntier = 7
        for j in range(ntier):
            u = (j + 0.6) / ntier
            yb = by - h * u * 0.97
            half = w / 2 * (1 - u) ** 0.78
            tl.append((curve([(cx - half, yb), (cx, yb + h * 0.025), (cx + half, yb)], 24), max(1.5, h * 0.012), (0.03, 0.03)))
            n_ = int(half * 0.9) + 4
            for q in range(n_):
                t = q / max(1, n_ - 1) * 2 - 1
                x0 = cx + t * half
                y0 = yb + h * 0.025 * (1 - t * t) - h * 0.045
                L = h * rng.uniform(0.05, 0.085)
                lean = t * 0.25
                it = ([(x0, y0), (x0 + lean * L, y0 + L)], rng.uniform(1.0, 2.0), (0.1, 0.5))
                (fr_l if rng.random() < 0.5 else fr_d).append(it)
        art = OV(art, strokes(W, H, fr_d) * roof, lambda m: rgba("#4a3a2a", m * 0.45))
        art = OV(art, strokes(W, H, fr_l) * roof, lambda m: rgba("#c9b48c", m * 0.35))
        art = OV(art, strokes(W, H, tl) * roof, lambda m: rgba("#3a2c1e", m * 0.55))
        art = GP(art, door, "#2a1d14", "#160f0a", seed=nx(), rough=0.4, pad=6)
        art = GP(art, tip, "#3a2a1c", seed=nx(), rough=0.3, pad=6)
    # foreground grass: long dry-brush blades, gold & olive
    tufts_g, tufts_o = [], []
    for _ in range(120):
        x = rng.uniform(0, W); y = rng.uniform(530, H + 20)
        for q in range(5):
            a = -math.pi / 2 + 0.22 + rng.uniform(-.28, .28)
            L = rng.uniform(26, 56) * (0.6 + (y - 530) / 140)
            x0 = x + rng.uniform(-6, 6)
            (tufts_g if rng.random() < 0.5 else tufts_o).append(([(x0, y), (x0 + math.cos(a) * L * .5, y + math.sin(a) * L * .5), (x0 + math.cos(a + .18) * L, y + math.sin(a + .18) * L)], 2.6, (0.0, 0.85)))
    art = GP(art, strokes(W, H, tufts_o), "#6f7a3a", "#4d5728", seed=nx(), rough=0.5, density=0.9)
    art = GP(art, strokes(W, H, tufts_g), "#d8b866", "#b38b3e", seed=nx(), rough=0.5, density=0.9)
    art = art[:, PADX:PADX + 900]
    preview(art, "nt-scene", bg=INDIGO_D)
    save_full(art, f"{OUT}/scene.webp", size=(720, 480), quality=78)
    clear()
