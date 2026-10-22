"""Boho Pampas — dry-brushed pampas plumes, a rattan hoop arch with a macramé swag, bunny tails and dried palm spears in
sand / oat / cinnamon. Run: python3 -I boho-pampas.py [part ...]
parts: arch plume sprig tail fringe linen. Assets -> public/themes/art/boho-pampas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b4_lib import *

OUT = outdir("boho-pampas")
PARTS = sys.argv[1:] or ["arch", "plume", "sprig", "tail", "fringe", "linen"]
OAT = "#dcc9a8"; OAT_L = "#f4ead8"; SAND = "#c9ac84"; CINN = "#a8673f"; CINN_D = "#7d4527"; RATTAN = "#c08f58"; RATTAN_D = "#8a5e33"
COTTON = "#f3ebdd"; COTTON_S = "#cbbb9f"
BG = "#f1e8da"


def stem_curve(x, y, L, ang, bend, n=40):
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca
    return [(x + ca * L * t + px * bend * L * t * t, y + sa * L * t + py * bend * L * t * t) for t in np.linspace(0, 1, n)]


def rattan(art, W, H, path, width, nx, rng):
    """Rattan cane: honey gouache body, darker node rings, a wrap of thin split cane at intervals, highlight streak."""
    m = strokes(W, H, [(path, width, None)])
    art = GP(art, m, RATTAN, mix(RATTAN, "#d8ae76", 0.5), seed=nx(), rough=1.2, streak=0.9)
    shade = np.clip(m - shift(m, -width * 0.18, -width * 0.25), 0, 1)
    art = G(art, shade, RATTAN_D, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.8, feather=1.2)
    hi = strokes(W, H, [([(x - width * 0.18, y - width * 0.22) for x, y in path], width * 0.16, None)])
    art = GP(art, drybrush(hi * m, nx(), 0.6), "#ecc994", seed=nx(), rough=0.4, streak=0.6, density=0.7)
    pts = resample(path, 2.0)
    wraps, nodes = [], []
    for i in range(0, len(pts), 1):
        x, y, a = pts[i]
        if i % 34 == 0:
            nodes.append(([(x - math.sin(a) * width * 0.5, y + math.cos(a) * width * 0.5), (x + math.sin(a) * width * 0.5, y - math.cos(a) * width * 0.5)], 1.6, None))
    art = G(art, strokes(W, H, nodes), RATTAN_D, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    return art


def macrame(art, W, H, nx, rng, anchors, drop, cords=4):
    """Cotton cord swags between anchor points with square knots, plus tasselled fringe at each anchor."""
    items, knots, fr = [], [], []
    for (x0, y0), (x1, y1) in zip(anchors[:-1], anchors[1:]):
        for c in range(cords):
            sag = drop * (0.55 + c * 0.16)
            p = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + math.sin(t * math.pi) * sag) for t in np.linspace(0, 1, 40)]
            items.append((p, 4.6, None))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + drop * 0.55
        for k in range(3):
            knots.append((mx + rng.uniform(-1, 1), my + drop * 0.16 * k + 4, 8.0 - k * 0.8))
    for (x, y) in anchors[1:-1] + [anchors[0], anchors[-1]]:
        knots.append((x, y + 6, 7))
        for j in range(14):
            sx = x + rng.uniform(-6, 6)
            L = rng.uniform(46, 74)
            fr.append(([(sx, y + 12), (sx + rng.uniform(-6, 6), y + 12 + L * 0.5), (sx + rng.uniform(-10, 10), y + 12 + L)], rng.uniform(1.0, 1.8), (0.02, 0.5)))
    cm = strokes(W, H, items)
    art = GP(art, cm, COTTON, OAT_L, seed=nx(), rough=0.8, streak=1.0)
    # twist shading along cords
    tw = cm * (0.5 + 0.5 * np.sin((np.mgrid[0:H, 0:W][1] + np.mgrid[0:H, 0:W][0]) * 0.9))
    art = G(art, tw * 0.8, COTTON_S, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.6)
    km = circles(W, H, knots)
    art = GP(art, km, COTTON, seed=nx(), rough=1.2, streak=0.6)
    art = G(art, np.clip(km - shift(km, -2, -2), 0, 1), COTTON_S, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.8)
    fm = strokes(W, H, [(curve(p, 12), w, tp) for p, w, tp in fr])
    art = GP(art, drybrush(fm, nx(), 0.35), COTTON, OAT_L, seed=nx(), rough=0.5, streak=0.6, density=0.9)
    return art


if "plume" in PARTS:
    W, H = 340, 860
    nx = Seq(30100); rng = random.Random(31)
    art = blank(W, H)
    art = pampas(art, W, H, stem_curve(W * 0.42, H - 6, H * 0.95, -math.pi / 2 + 0.04, 0.08), rng, nx, base=OAT, light=OAT_L, shade=SAND, length_frac=0.6, scale=1.2)
    preview(art, "bp-plume", tone=BG)
    save(art, f"{OUT}/plume.webp", max_w=170, quality=80)
    clear()

def cluster(art, W, H, nx, rng, bx, by, side, plumes, spears, tails, big=1.0):
    """Organic dried bouquet tied at (bx, by): pampas fanning outward on `side`, palm spears, bunny tails."""
    for k, (L, a, bend, tone) in enumerate(plumes):
        base_, shade_ = (OAT, SAND) if tone == 0 else (("#c69a74", CINN) if tone == 1 else ("#e6d6bb", "#bca17c"))
        art = pampas(art, W, H, stem_curve(bx, by, L * big, a, bend), rng, nx, base=base_, light=OAT_L if tone != 1 else "#ecd6bd",
                     shade=shade_, length_frac=0.55, scale=1.05 * big)
        clear()
    for (L, a, w, col) in spears:
        art = palm_spear(art, W, H, bx, by, L * big, a, rng, nx, col=col, width=w * big)
    for (L, a) in tails:
        art = bunny_tail(art, W, H, bx + math.cos(a) * L * big, by + math.sin(a) * L * big, 16 * big, a, rng, nx, stem_len=L * big)
    return art


if "arch" in PARTS:
    W, H = 1040, 1060
    nx = Seq(30200); rng = random.Random(32)
    art = blank(W, H)
    cx, top, r = W / 2, 120, 300
    U = -math.pi / 2
    def arch_path(rr, y0):
        top_ = [(cx + math.cos(math.pi + t * math.pi) * rr, top + rr + math.sin(math.pi + t * math.pi) * rr) for t in np.linspace(0, 1, 90)]
        return [(cx - rr, y0)] + top_ + [(cx + rr, y0)]
    # rear: tall plumes behind the left leg and the right leg (leaning outward)
    art = cluster(art, W, H, nx, rng, cx - r + 10, H - 110, -1,
                  [(560, U - 0.22, -0.05, 0), (640, U - 0.05, 0.03, 0), (470, U - 0.5, -0.08, 2)], [], [])
    art = cluster(art, W, H, nx, rng, cx + r - 10, H - 110, 1,
                  [(520, U + 0.2, 0.05, 2), (430, U + 0.45, 0.08, 0)], [], [])
    art = rattan(art, W, H, arch_path(r, H - 120), 20, nx, rng)
    art = rattan(art, W, H, arch_path(r - 26, H - 120), 11, nx, rng)
    clear()
    anchors = [(cx + math.cos(math.pi + t * math.pi) * r, top + r + math.sin(math.pi + t * math.pi) * r) for t in (0.2, 0.36, 0.52, 0.68)]
    art = macrame(art, W, H, nx, rng, anchors, 44)
    clear()
    # front: cinnamon pampas + palm spears + bunny tails at the left foot, smaller echo at the right foot
    art = cluster(art, W, H, nx, rng, cx - r + 16, H - 100, -1,
                  [(330, U - 0.7, -0.1, 1), (280, U - 0.25, 0.06, 1)],
                  [(300, U - 0.95, 36, "#c79a68"), (250, U - 0.4, 30, "#d6b083"), (220, U - 1.25, 26, "#b9875a")],
                  [(200, U - 0.15), (170, U - 0.55), (230, U + 0.05), (150, U - 1.0)])
    art = cluster(art, W, H, nx, rng, cx + r - 16, H - 100, 1,
                  [(250, U + 0.55, 0.1, 1)],
                  [(240, U + 0.8, 30, "#c79a68"), (190, U + 0.3, 24, "#d6b083")],
                  [(160, U + 0.15), (190, U + 0.45)], big=0.9)
    # upper-right shoulder spray tied to the hoop
    sx, sy = cx + math.cos(-0.62) * r, top + r + math.sin(-0.62) * r
    art = cluster(art, W, H, nx, rng, sx, sy, 1,
                  [(230, -0.35, 0.08, 0), (200, U + 0.45, -0.05, 2)],
                  [(170, 0.15, 22, "#c79a68"), (150, U + 0.9, 20, "#d6b083")],
                  [(120, -0.75), (110, 0.4)], big=0.85)
    art = art[60:1000]          # fixed crop (CSS aligns the photo to the inner cane: x 252..788, y 92..880 of 1040x940)
    preview(art, "bp-arch", tone=BG)
    save_full(art, f"{OUT}/arch.webp", size=(700, 633), quality=76)
    clear()

if "sprig" in PARTS:
    W, H = 760, 200
    nx = Seq(30300); rng = random.Random(33)
    art = blank(W, H)
    cx, cy = W / 2, H / 2 + 20
    for side in (-1, 1):
        art = pampas(art, W, H, stem_curve(cx + side * 10, cy + 4, 330, math.pi / 2 - side * math.pi / 2 - side * 0.06, side * 0.04), rng, nx,
                     base=OAT, light=OAT_L, shade=SAND, length_frac=0.6, scale=0.85)
        art = palm_spear(art, W, H, cx + side * 6, cy + 8, 170, -side * 0.28 + (math.pi if side < 0 else 0), rng, nx, width=18)
        for k in range(2):
            a = (math.pi if side < 0 else 0) + side * rng.uniform(-0.6, -0.25)
            art = bunny_tail(art, W, H, cx + math.cos(a) * 120, cy + math.sin(a) * 120 - 4, 10, a, rng, nx, stem_len=110)
    art = bunny_tail(art, W, H, cx, cy - 26, 12, -math.pi / 2, rng, nx, stem_len=26)
    preview(art, "bp-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=360, quality=82)
    clear()

if "tail" in PARTS:
    W, H = 150, 240
    nx = Seq(30400); rng = random.Random(34)
    art = blank(W, H)
    art = bunny_tail(art, W, H, W / 2 + 4, 60, 30, -math.pi / 2 + 0.1, rng, nx, stem_len=170, col="#f1e6d2")
    preview(art, "bp-tail", tone=BG)
    save(art, f"{OUT}/tail.webp", max_w=64, quality=84)

if "fringe" in PARTS:
    # macramé fringe band: a horizontal cord with knotted drops (countdown top / closing)
    W, H = 900, 170
    nx = Seq(30500); rng = random.Random(35)
    art = blank(W, H)
    anchors = [(x, 18) for x in np.linspace(-20, W + 20, 8)]
    art = macrame(art, W, H, nx, rng, anchors, 34, cords=3)
    rod = strokes(W, H, [([(0, 16), (W, 18)], 10, None)])
    art = GP(art, rod, "#9b6a3f", "#b98552", seed=nx(), rough=1.0, streak=1.0)
    preview(art, "bp-fringe", tone=BG)
    save(art, f"{OUT}/fringe.webp", max_w=450, quality=80)

if "linen" in PARTS:
    n = 420
    base = rgb_arr(n, n, BG) * (0.97 + 0.06 * wrap_noise(n, n, 1, 40))[..., None] * (1 + (wrap_noise(n, n, 4, 0.7) - 0.5) * 0.06)[..., None]
    wx = wrap_noise(n, n, 2, (0.4, 6)); wy = wrap_noise(n, n, 3, (6, 0.4))
    base *= (1 + (wx - 0.5) * 0.05 + (wy - 0.5) * 0.05)[..., None]
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/linen.webp", quality=70)
