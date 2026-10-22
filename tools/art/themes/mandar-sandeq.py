"""Mandar Sandeq — coastal light on the Mandar sea: sandeq outrigger sailboats (slender striped hulls, bamboo cross-arms,
long floats, tall triangular sails leaning on the wind) on a watercolour sea with wet-edged wave crests and paper-white
foam; lipaq saqbe silk sarong check woven thread by thread (2/2 twill, warp/weft sheen); a single sandeq emblem and a
wave divider. Run: python3 -I mandar-sandeq.py [part ...]   parts: sea lipaq boat wave
Assets -> public/themes/art/mandar-sandeq/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b1_lib import *

OUT = outdir("mandar-sandeq")
PARTS = sys.argv[1:] or ["sea", "lipaq", "boat", "wave"]
SEA, SEA_D, SEA_L, NAVY = "#2f79a8", "#1d557f", "#7fb8d6", "#163a5c"
SAIL, SAIL_D = "#f7f0e2", "#c9bfae"
MAROON, GOLD, BLACK, GREEN, WHITE = "#7d1f2b", "#c99a3c", "#1d1414", "#2f6b4f", "#f2ead8"


def sandeq(art, W, H, x, y, s, rng, nx, flip=1, hull_col=("#f4efe6", "#d9d0c2"), stripe="#b3302c", lean=0.12):
    """One sandeq at waterline point (x, y), scale s. flip=1 bow to the right."""
    f = flip
    def P(u, v):
        return (x + u * s * f, y + v * s)
    # hull: long, very slim, upswept bow & stern
    hull = shapes(W, H, [[P(-1.0, -0.10), P(-0.7, 0.02), P(0.0, 0.05), P(0.75, 0.02), P(1.08, -0.14), P(0.9, -0.06), P(0.0, -0.03), P(-0.85, -0.05)]])
    # outrigger floats (palatto) on the far and near sides + cross-arms (baratang)
    floats = strokes(W, H, [([P(-0.62, 0.10), P(0.66, 0.10)], max(2.5, s * 0.03), (0.1, 0.1)), ([P(-0.55, -0.02), P(0.58, -0.02)], max(2, s * 0.022), (0.1, 0.1))])
    arms = strokes(W, H, [([P(-0.34, -0.06), P(-0.40, 0.11)], max(2, s * 0.02), None), ([P(0.30, -0.06), P(0.36, 0.11)], max(2, s * 0.02), None),
                          ([P(-0.34, -0.06), P(-0.32, -0.025)], s * 0.012, None), ([P(0.30, -0.06), P(0.32, -0.025)], s * 0.012, None)])
    art = knockout(art, floats, 1.0, 1)
    art = G(art, floats, "#4a3420", seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.6, feather=0.5)
    art = G(art, arms, "#5a4028", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.5, feather=0.4)
    art = knockout(art, hull, 1.0, 1)
    art = G(art, hull, hull_col[0], hull_col[1], seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1.2, feather=0.6)
    st = strokes(W, H, [(curve([P(-0.92, -0.07), P(0.0, -0.0), P(0.95, -0.07)], 20), s * 0.014, None)]) * hull
    art = G(art, st, stripe, seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5, feather=0.4)
    st2 = strokes(W, H, [(curve([P(-0.8, -0.03), P(0.0, 0.025), P(0.7, -0.0)], 20), s * 0.01, None)]) * hull
    art = G(art, st2, "#2a5d8a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.4, feather=0.4)
    # mast, leaning slightly forward, and the tall triangular sail (lete) with a long angled boom
    top = P(0.12 + lean, -1.55)
    base = P(0.05, -0.05)
    mast = strokes(W, H, [([base, top], s * 0.014, (0.0, 0.2))])
    sail_pts = [P(0.10 + lean * 0.95, -1.50), P(0.08, -0.16), P(-0.86, -0.22)]
    sail = shapes(W, H, [deform(sail_pts, rng, 1, 0.01)], smooth=False)
    art = knockout(art, sail, 1.0, 1)
    art = G(art, sail, SAIL, "#efe6d4", seed=nx(), density=0.92, edge=0.55, bloom=0.35, rough=1.6, feather=0.7)
    # belly shadow along the luff, seams
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seams = strokes(W, H, [([P(0.09 + lean * 0.95 * (1 - t), -1.5 + 1.34 * t), P(-0.86 + 0.94 * t * 0.0 + (0.94 * t) * 0, -0.22)], s * 0.004, None) for t in (0.25, 0.5, 0.75)]) * sail
    art = G(art, seams, SAIL_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
    luff = sail * np.clip(1 - np.abs((xx - P(0.08, 0)[0]) / (s * 0.25)), 0, 1)
    art = G(art, luff, "#b9c6cf", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=1, feather=2)
    art = G(art, mast, "#4a3420", seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.4, feather=0.4)
    boom = strokes(W, H, [([P(0.08, -0.16), P(-0.9, -0.23)], s * 0.012, None)])
    art = G(art, boom, "#5a4028", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.4, feather=0.4)
    flag = shapes(W, H, [[top, P(0.12 + lean - 0.22, -1.52), P(0.12 + lean - 0.18, -1.47), P(0.12 + lean, -1.47)]], smooth=False)
    art = G(art, flag, "#c23a2e", seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.5, feather=0.4)
    # reflection
    refl = shapes(W, H, [[P(-0.9, 0.06), P(0.9, 0.06), P(0.2, 0.5)]], smooth=False) * np.clip(fbm(W, H, nx(), 6, 2) * 2 - 0.6, 0, 1)
    art = G(art, refl, SAIL_D, seed=nx(), density=0.25, edge=0.1, bloom=0.2, rough=3, feather=1.2)
    return art


def waves(art, W, H, y0, y1, nx, rng, density=1.0, col=SEA_D):
    """Wave crest strokes: tapered dark arcs with paper-white foam left above them."""
    items = []
    for _ in range(int((y1 - y0) * W / 900 * density)):
        y = rng.uniform(y0, y1); t = (y - y0) / max(1, (y1 - y0))
        L = 16 + 70 * t; x = rng.uniform(-30, W)
        amp = 2 + 6 * t
        items.append((curve([(x, y), (x + L * 0.35, y - amp), (x + L * 0.7, y - amp * 0.3), (x + L, y + amp * 0.2)], 14), 1.2 + 3.0 * t, (0.2, 0.5)))
    m = strokes(W, H, items)
    return G(art, m, col, seed=nx(), density=0.75, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)


if "sea" in PARTS:
    W, H = 800, 760
    nx = Seq(4000)
    rng = random.Random(17)
    art = blank(W, H)
    # sky wash (morning, warm near horizon)
    sky = shapes(W, H, [[(-20, -20), (820, -20), (820, 360), (-20, 360)]], smooth=False)
    art = G(art, sky * np.clip(np.mgrid[0:H, 0:W][0].astype(np.float32) / 360, 0, 1) ** 0.8, "#f3d7b4", seed=nx(), density=0.55, gran=0.06, edge=0.1, bloom=0.5, rough=10, feather=6)
    art = G(art, sky * np.clip(1 - np.mgrid[0:H, 0:W][0].astype(np.float32) / 300, 0, 1), "#a9cfe3", seed=nx(), density=0.5, gran=0.06, edge=0.1, bloom=0.5, rough=10, feather=6)
    cl = shapes(W, H, [deform(ellipse_pts(180, 120, 150, 22, 16), rng, 2, 0.1), deform(ellipse_pts(600, 80, 120, 16, 16), rng, 2, 0.1)])
    art = G(art, cl, "#ffffff", seed=nx(), density=0.0, edge=0, bloom=0, rough=4)
    # distant coast of Majene
    coast = shapes(W, H, [[(-20, 352), (80, 326), (180, 334), (260, 318), (340, 340), (420, 352), (-20, 362)]])
    art = G(art, coast, "#7f9c9a", "#6b8a8c", seed=nx(), density=0.55, edge=0.5, bloom=0.3, rough=5)
    # sea body: light to deep
    sea = shapes(W, H, [deform([(-20, 352), (820, 348), (820, 780), (-20, 780)], rng, 1, 0.005)], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, sea, SEA_L, "#9cc7da", seed=nx(), density=0.75, gran=0.06, edge=0.4, bloom=0.5, rough=6, feather=2)
    art = G(art, sea * np.clip((yy - 380) / 380, 0, 1), SEA, SEA_D, seed=nx(), density=0.8, edge=0.2, gran=0.06, bloom=0.5, rough=8, feather=6)
    art = waves(art, W, H, 370, 740, nx, rng, density=0.7)
    art = waves(art, W, H, 360, 740, nx, rng, density=0.5, col="#4b8db5")
    art = waves(art, W, H, 470, 740, nx, rng, density=0.25, col=NAVY)
    # paper-white glints on the water
    gl = strokes(W, H, [([(x, y), (x + rng.uniform(8, 30), y)], rng.uniform(1, 2.2), (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(370, 700)) for _ in range(70)]])
    art = OV(art, gl, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32), (m * 0.7)[..., None]], -1))
    # boats: far (small), middle, near (large)
    art = sandeq(art, W, H, 640, 392, 70, rng, nx, flip=-1, stripe="#2a7d5a", lean=0.1)
    art = sandeq(art, W, H, 170, 430, 105, rng, nx, flip=1, stripe="#c9a23c", lean=0.12)
    art = sandeq(art, W, H, 470, 600, 210, rng, nx, flip=1, stripe="#b3302c", lean=0.14)
    # foam & spray around the near hull (lifted paper white)
    foam = strokes(W, H, [(curve([(250, 612), (300, 604), (360, 616)], 10), 4, (0.2, 0.4)), (curve([(640, 600), (680, 588), (700, 600)], 10), 5, (0.1, 0.5))])
    art = OV(art, foam, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32), (gaussian_filter(m, 1.2) * 0.85)[..., None]], -1))
    # fade the sky to transparent at the top so the page colour carries through
    art = fade_edges(art, top=140)
    save(art, f"{OUT}/sea.webp", max_w=680, quality=70)
    show(art, "ms-sea", tone="#f6f1e6")
    clear()

if "lipaq" in PARTS:
    pal = [MAROON, GOLD, BLACK, WHITE, GREEN, "#a3303a"]
    seq = [(0, 8), (5, 2), (0, 8), (1, 2), (2, 3), (1, 2), (0, 8), (3, 1), (4, 3), (3, 1)]
    n = sum(k for _, k in seq)  # 38 threads
    t = 3
    W = H = n * t * 3
    tile = silk_plaid(W, H, seq, seq, pal, t=t, seed=3, sheen=0.7, folds=0.4)
    save_rgb(tile, f"{OUT}/lipaq.webp", quality=80)
    show(tile, "ms-lipaq")
    big = np.concatenate([np.concatenate([tile, tile], 1)] * 2, 0)
    show(big, "ms-lipaq-2x2")
    clear()

if "boat" in PARTS:
    W, H = 300, 300
    nx = Seq(5000)
    rng = random.Random(3)
    art = blank(W, H)
    wv = strokes(W, H, [(curve([(20, 262), (70, 254), (120, 264), (170, 254), (220, 264), (280, 256)], 30), 5, (0.1, 0.1))])
    art = G(art, wv, SEA, SEA_D, seed=nx(), density=0.8, edge=0.5, bloom=0.1, rough=1.5, feather=0.6)
    art = sandeq(art, W, H, 160, 248, 120, rng, nx, flip=1, stripe="#b3302c", lean=0.14)
    save(art, f"{OUT}/boat.webp", max_w=240)
    show(art, "ms-boat")
    clear()

if "wave" in PARTS:
    W, H = 420, 60
    nx = Seq(6000)
    rng = random.Random(8)
    art = blank(W, H)
    items = []
    for k in range(3):
        y = 22 + k * 10
        pts = [(x, y + math.sin(x / 34 + k) * 6) for x in range(10, 410, 6)]
        items.append((pts, 3.2 - k * 0.7, (0.12, 0.12)))
    m = strokes(W, H, items)
    art = G(art, m, SEA, SEA_D, seed=nx(), density=0.85, edge=0.6, bloom=0.2, rough=1.2, feather=0.6)
    dots = circles(W, H, [(210, 14, 4.5)])
    art = G(art, dots, GOLD, seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5)
    save(art, f"{OUT}/wave.webp", max_w=360)
    show(art, "ms-wave")
    clear()
