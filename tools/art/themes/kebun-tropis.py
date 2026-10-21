"""Kebun Tropis — sunny tropical garden in fresh gouache: banana leaves, strelitzia (bird-of-paradise flower), frangipani,
hibiscus, painted sun disc. Bright coral / emerald / sun-yellow palette on warm white.
Run: python3 -I kebun-tropis.py [part ...]   parts: rimbun-a rimbun-b kamboja sprig matahari"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *

OUT = outdir("kebun-tropis")
PARTS = sys.argv[1:] or ["rimbun-a", "rimbun-b", "kamboja", "sprig", "matahari"]
G1, G2, G3 = "#8fd14f", "#2fa05a", "#11683f"   # light / mid / deep leaf greens
EM = "#1f8a5b"


def banana_leaf(art, W, H, root, ang, L, width, bend, rng, nx, tone=0):
    pts = []
    for i in range(22):
        t = i / 21
        a = ang + bend * t * t
        if i == 0:
            pts.append(root)
        else:
            px, py = pts[-1]
            pts.append((px + math.cos(a) * L / 21, py + math.sin(a) * L / 21))
    light, mid, dark = [(G1, G2, G3), ("#b5df5a", "#5dbb4a", "#1f7a43"), ("#6fc26a", "#2c9a62", "#0f5e3d")][tone]
    return g_leaf_blade(art, W, H, pts, width, rng, nx, light, mid, dark, vein="#effad0", tear=0.45)


def palm_frond(art, W, H, root, ang, L, rng, nx, col=("#5dbb4a", "#1f7a43")):
    """Coconut-style frond: arching rachis with paired tapered leaflets (each a painted blade, not a line)."""
    spine = [(root[0] + math.cos(ang + 0.35 * t * t) * L * t, root[1] + math.sin(ang + 0.35 * t * t) * L * t) for t in [i / 26 for i in range(27)]]
    polys = []
    for j in range(2, 26):
        px, py = spine[j]
        a = math.atan2(spine[j][1] - spine[j - 1][1], spine[j][0] - spine[j - 1][0])
        ll = L * 0.34 * math.sin(math.pi * (j / 26) ** 0.8) + 10
        for side in (-1, 1):
            aa = a + side * 0.95 + 0.3
            polys.append(petal_pts(px, py, ll, ll * 0.06, aa, n=10, cup=side * -1.2))
    m = np.maximum(shapes(W, H, polys), strokes(W, H, [(spine, 6, (0.0, 0.6))]))
    art = GP(art, m, col[0], col[1], seed=nx(), rough=1.0, streak=1.0)
    hi = []
    for poly in polys[::2]:
        hi.append((poly[1:5], 1.4, (0.1, 0.6)))
    return OV(art, strokes(W, H, hi) * m, lambda mm: rgba("#d9f5a0", mm * 0.35))


def leaves_small(art, W, H, spots, rng, nx):
    for (x, y, L, a) in spots:
        art = g_leaf(art, W, H, x, y, L, a, rng, nx, rng.choice([G1, "#6cc35a", "#3fae5e"]), rng.choice([G2, G3]))
    return art


if "rimbun-a" in PARTS:
    # top-left corner burst
    W, H = 760, 720
    rng = random.Random(71); nx = Seq(71000)
    art = blank(W, H)
    art = palm_frond(art, W, H, (-20, 60), 0.15, 640, rng, nx, ("#4fae4a", "#17683c"))
    art = banana_leaf(art, W, H, (-30, -10), 0.95, 700, 90, 0.35, rng, nx, 2)
    art = banana_leaf(art, W, H, (-40, 80), 0.25, 560, 78, 0.55, rng, nx, 0)
    art = banana_leaf(art, W, H, (40, -40), 1.45, 520, 70, -0.25, rng, nx, 1)
    # strelitzia stem out of the foliage
    stem = strokes(W, H, [(curve([(180, 420), (260, 320), (330, 260)], 20), 9, (0.0, 0.2))])
    art = GP(art, stem, "#3f8f4a", "#1f6a3a", seed=nx(), rough=0.6)
    art = strelitzia(art, W, H, 326, 262, 120, -0.35, rng, nx, 1)
    art = leaves_small(art, W, H, [(150, 300, 120, 0.5), (210, 200, 110, -0.2), (90, 380, 130, 1.0), (300, 140, 100, 0.2)], rng, nx)
    art = hibiscus(art, W, H, 180, 250, 92, rng, nx, ang=0.4)
    art = hibiscus(art, W, H, 120, 420, 62, rng, nx, ang=2.0, light="#ff8f70", mid="#f2585a", deep="#b31c3a")
    art = frangipani(art, W, H, 92, 160, 52, rng, nx, rot=0.3)
    art = frangipani(art, W, H, 150, 92, 44, rng, nx, rot=1.2, tilt=0.85)
    art = frangipani(art, W, H, 270, 330, 40, rng, nx, rot=2.0, tilt=0.8)
    for (x, y) in [(470, 70), (300, 440), (420, 210)]:
        art = GP(art, circles(W, H, [(x, y, 7), (x + 14, y + 6, 5), (x + 4, y + 16, 4)]), "#ffd23a", "#f6a91c", seed=nx(), rough=0.5, pad=6)
    preview(art, "kt-rimbun-a", tone="#fffaf0")
    save(art, f"{OUT}/rimbun-a.webp", max_w=440, quality=82)
    clear()

if "rimbun-b" in PARTS:
    # bottom-right cluster (different composition, flowers lower)
    W, H = 760, 640
    rng = random.Random(72); nx = Seq(72000)
    art = blank(W, H)
    art = banana_leaf(art, W, H, (790, 660), -2.2, 640, 84, -0.4, rng, nx, 0)
    art = banana_leaf(art, W, H, (800, 560), -2.75, 600, 76, 0.35, rng, nx, 2)
    art = palm_frond(art, W, H, (780, 690), -1.75, 520, rng, nx)
    art = banana_leaf(art, W, H, (720, 700), -1.45, 460, 64, -0.5, rng, nx, 1)
    art = leaves_small(art, W, H, [(560, 520, 120, -2.6), (470, 560, 110, -3.0), (640, 420, 110, -2.0), (420, 620, 120, -2.8)], rng, nx)
    stem = strokes(W, H, [(curve([(560, 640), (500, 520), (430, 450)], 20), 9, (0.0, 0.2))])
    art = GP(art, stem, "#3f8f4a", "#1f6a3a", seed=nx(), rough=0.6)
    art = strelitzia(art, W, H, 436, 452, 112, math.pi + 0.3, rng, nx, -1)
    art = hibiscus(art, W, H, 600, 520, 88, rng, nx, ang=3.6)
    art = frangipani(art, W, H, 500, 600, 50, rng, nx, rot=0.8)
    art = frangipani(art, W, H, 700, 440, 46, rng, nx, rot=2.4, tilt=0.85)
    art = frangipani(art, W, H, 400, 580, 38, rng, nx, rot=0.1, tilt=0.8)
    preview(art, "kt-rimbun-b", tone="#fffaf0")
    save(art, f"{OUT}/rimbun-b.webp", max_w=440, quality=82)
    clear()

if "kamboja" in PARTS:
    W, H = 300, 300
    rng = random.Random(73); nx = Seq(73000)
    art = blank(W, H)
    art = g_leaf(art, W, H, 150, 160, 130, 0.5, rng, nx, G1, G2)
    art = g_leaf(art, W, H, 150, 160, 120, 2.5, rng, nx, "#6cc35a", G3)
    art = frangipani(art, W, H, 150, 140, 78, rng, nx, rot=0.2)
    preview(art, "kt-kamboja", tone="#fffaf0")
    save(art, f"{OUT}/kamboja.webp", max_w=150, quality=84)
    clear()

if "sprig" in PARTS:
    W, H = 640, 170
    rng = random.Random(74); nx = Seq(74000)
    art = blank(W, H)
    for sgn in (-1, 1):
        stem = strokes(W, H, [(curve([(W / 2, H / 2 + 6), (W / 2 + sgn * 120, H / 2 - 4), (W / 2 + sgn * 250, H / 2 + 8)], 24), 4, (0.0, 0.6))])
        art = GP(art, stem, "#3f8f4a", "#1f6a3a", seed=nx(), rough=0.5)
        for k, t in enumerate((0.35, 0.62, 0.85)):
            x = W / 2 + sgn * 250 * t
            y = H / 2 + (-4 if t < 0.5 else 4)
            art = g_leaf(art, W, H, x, y, 70 - k * 12, (-0.6 if k % 2 else 0.5) + (math.pi if sgn < 0 else 0) * 1 + (0 if sgn > 0 else 0), rng, nx, G1 if k % 2 else "#6cc35a", G2)
    art = hibiscus(art, W, H, W / 2 - 48, H / 2, 40, rng, nx, ang=1.1)
    art = frangipani(art, W, H, W / 2 + 40, H / 2 + 2, 36, rng, nx, rot=0.6)
    preview(art, "kt-sprig", tone="#fffaf0")
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=84)
    clear()

if "matahari" in PARTS:
    # painted sun disc: warm yellow gouache laid with broad flat-brush strokes, a second lighter pass, dry orange rim
    W, H = 640, 640
    rng = random.Random(75); nx = Seq(75000)
    art = blank(W, H)
    disc = shape_mask(W, H, deform(ellipse_pts(320, 320, 290, 284, 24), rng, 2, 0.012))
    art = GP(art, disc, "#ffc83a", "#f8b02a", seed=nx(), rough=3.0, streak=0.6)
    sw = []
    for k in range(46):
        y = rng.uniform(40, 600); x0 = rng.uniform(0, 300); L = rng.uniform(120, 340)
        a = rng.uniform(-0.18, 0.1)
        sw.append(([(x0, y), (x0 + L * .5, y + math.sin(a) * L * .5 + rng.uniform(-6, 6)), (x0 + L, y + math.sin(a) * L)], rng.uniform(12, 30), (0.15, 0.35)))
    art = OV(art, strokes(W, H, sw) * disc, lambda m: rgba("#ffe07a", m * 0.4))
    art = OV(art, strokes(W, H, sw[::4]) * disc, lambda m: rgba("#f39a2a", m * 0.18))
    rim = np.clip(disc - gaussian_filter(disc, 10) * 1.05, 0, 1)
    art = OV(art, rim, lambda m: rgba("#f08a2a", m * 0.55))
    preview(art, "kt-matahari", tone="#fffaf0")
    save(art, f"{OUT}/matahari.webp", max_w=320, quality=80)
    clear()
