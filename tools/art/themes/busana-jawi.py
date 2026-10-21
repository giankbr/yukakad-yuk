"""Busana Jawi — full-bleed photo theme: gold-foil parang band, gold kembang goyang/cundhuk mentul ornament,
dark sogan batik (truntum) texture. Run: python3 -I busana-jawi.py [part ...]  parts: parang ornament batik
Assets -> public/themes/art/busana-jawi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _jw_lib import *
import _jw_lib as jw

OUT = outdir("busana-jawi")
PARTS = sys.argv[1:] or ["parang", "ornament", "batik"]
GOLD = "#c9a45a"

if "parang" in PARTS:
    W, H = 240, 60
    nx = Seq(9100)
    curls, lens, dots_ = [], [], []
    for k in range(-3, 9):
        x0 = k * 40
        for j in range(4):
            t = j / 4
            cx_, cy_ = x0 + 8 + t * 46, H - 6 - t * (H - 12)
            lens.append(petal_pts(cx_ - 7, cy_ + 7, 18, 6.5, -math.pi / 4, n=12))
            curls.append((spiral_pts(cx_ + 2, cy_ - 1, 4.2, 0.8, math.pi * 0.25, 0.9, 16, 1), 1.6, (0.0, 0.5)))
        dots_ += [(x0 + 30 + t * 30, H - 10 - t * (H - 20), 1.8) for t in (0.15, 0.5, 0.85)]
    m = np.clip(shapes(W, H, lens) - strokes(W, H, curls) * 0.9, 0, 1)
    m = np.maximum.reduce([m, circles(W, H, dots_), shapes(W, H, [[(0, 0), (W, 0), (W, 2.5), (0, 2.5)], [(0, H - 2.5), (W, H - 2.5), (W, H), (0, H)]], smooth=False)])
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.4, sparkle=0.08)
    save_full(art, f"{OUT}/parang.webp", quality=84)
    preview(art, "bj-parang", bg="#2a1a10")

if "ornament" in PARTS:
    # kembang goyang / cundhuk mentul inspired: five blossoms on sprung stems fanning from a jewelled base
    W, H = 420, 300
    nx = Seq(9200); cx = W / 2
    items, polys, dots_ = [], [], []
    for i, a in enumerate([-2.55, -2.1, -1.57, -1.04, -0.59]):
        L = 150 if i == 2 else (128 if i in (1, 3) else 104)
        tip = (cx + math.cos(a) * L, 250 + math.sin(a) * L)
        # sprung (coiled) stem
        stem = []
        for k in range(60):
            t = k / 59
            x = cx + (tip[0] - cx) * t; y = 250 + (tip[1] - 250) * t
            px, py = -math.sin(a), math.cos(a)
            w = math.sin(t * math.pi * 7) * 3.2 * (1 - t * 0.6)
            stem.append((x + px * w, y + py * w))
        items.append((stem, 2.0, (0.05, 0.05)))
        r = 26 if i == 2 else 21
        for k in range(6):
            pa = k * math.tau / 6 + a
            polys.append(petal_pts(tip[0] + math.cos(pa) * r * 0.12, tip[1] + math.sin(pa) * r * 0.12, r, r * 0.3, pa, n=12))
        dots_.append((tip[0], tip[1], r * 0.26))
        for k in range(6):
            pa = k * math.tau / 6 + a + 0.52
            dots_.append((tip[0] + math.cos(pa) * r * 1.05, tip[1] + math.sin(pa) * r * 1.05, 2.0))
    polys.append(deform(ellipse_pts(cx, 258, 46, 18, 16), random.Random(3), 1, 0.04))
    for sgn in (-1, 1):
        polys.append(petal_pts(cx + sgn * 30, 262, 56, 13, math.pi / 2 + sgn * 1.25, n=12))
    m = np.maximum.reduce([strokes(W, H, items), shapes(W, H, polys), circles(W, H, dots_)])
    m = np.clip(m - np.clip(gaussian_filter(shapes(W, H, polys), 1.0) - 0.98, 0, 1), 0, 1)
    art = blank(W, H)
    art = G(art, gaussian_filter(m, 8), "#000000", seed=nx(), density=0.25, edge=0, bloom=0, rough=1)
    art = FO(art, m, GOLD, seed=nx(), emboss=0.75, sparkle=0.18)
    gems = circles(W, H, [(cx, 258, 9), (cx - 22, 256, 5), (cx + 22, 256, 5)])
    art = OV(art, gems, lambda q: gouache_paint(q, "#8e1f2a", "#5a0f18", seed=5, rough=0.6))
    art = OV(art, circles(W, H, [(cx - 3, 255, 2.4)]), lambda q: np.concatenate([np.ones(q.shape + (3,), np.float32), (q * 0.8)[..., None]], -1))
    preview(art, "bj-ornament", bg="#2a1a10")
    save(art, f"{OUT}/ornament.webp", max_w=300, quality=84)

if "batik" in PARTS:
    # dark sogan cloth with faint gold truntum (scattered little star-flowers) on a hand-dyed ground — seamless tile
    n = 320
    nx = Seq(9300)
    ground = np.concatenate([np.ones((n, n, 3), np.float32) * np.array(hex_rgb("#2b1b12"), np.float32), np.ones((n, n, 1), np.float32)], -1)
    var = wrap_noise(n, n, 4, 30)
    ground[..., :3] *= (0.85 + 0.3 * var)[..., None]
    polys, dots_ = [], []
    for gy in range(4):
        for gx in range(4):
            x = gx * 80 + (40 if gy % 2 else 0) + 20; y = gy * 80 + 20
            for k in range(8):
                a = k * math.tau / 8
                polys.append(petal_pts(x % n, y, 11, 3.6, a, n=8))
            dots_.append((x % n, y, 2.4))
            for k in range(8):
                a = k * math.tau / 8 + 0.39
                dots_.append(((x + math.cos(a) * 17) % n, y + math.sin(a) * 17, 1.3))
    m = np.maximum(shapes(n, n, polys), circles(n, n, dots_))
    m = np.maximum(m, np.roll(m, n // 2, 1) * 0)  # (tile already wraps by construction)
    art = OV(ground, m, lambda q: np.concatenate([np.ones(q.shape + (3,), np.float32) * np.array(hex_rgb("#a57d45"), np.float32), (q * 0.5)[..., None]], -1))
    save_full(art, f"{OUT}/batik.webp", quality=72)
    preview(art, "bj-batik")
