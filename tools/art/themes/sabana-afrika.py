"""Sabana Afrika — a savanna sunset in bold gouache bands: banded aubergine-to-gold sky, a huge low orange sun crossed by
cloud strips, a far ridge with an elephant herd, giraffes and flat-topped acacias in silhouette, golden grass and a dark
foreground. Plus a horizon strip, a lone acacia, a giraffe, a banded sun emblem, a stripe divider and a paper tile.
Original, no text in the art.  Run: python3 -I sabana-afrika.py [part ...]
parts: scene ridge acacia giraffe sun stripes paper   Assets -> public/themes/art/sabana-afrika/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l6_lib import *

OUT = outdir("sabana-afrika")
PARTS = sys.argv[1:] or ["scene", "ridge", "acacia", "giraffe", "sun", "stripes", "paper"]
AUB, WINE, MADDER, BURNT, ORANGE, GOLD, SUN, SUNL = "#2f1528", "#561d33", "#86283a", "#bb4329", "#e2752c", "#f0a43e", "#f6b54a", "#ffd681"
OCHRE, OCHRE_D, EARTH, SIL, CREAM = "#d4902f", "#a9661f", "#3a1a12", "#200d10", "#fbeed6"


def paint(art, mask, c1, c2=None, seed=1, rough=2.2, streak=1.0):
    return GP(art, mask, c1, c2 or c1, seed=seed, rough=rough, streak=streak, pad=10)


def grass_blades(W, H, y0, y1, n, rng, hmin, hmax, wmin=1.2, wmax=2.6, lean=0.25):
    items = []
    for _ in range(n):
        x = rng.uniform(-10, W + 10); y = rng.uniform(y0, y1)
        L = rng.uniform(hmin, hmax); a = -math.pi / 2 + rng.uniform(-lean, lean)
        items.append(([(x, y), (x + math.cos(a) * L * 0.5 + rng.uniform(-2, 2), y + math.sin(a) * L * 0.5), (x + math.cos(a) * L + rng.uniform(-4, 4), y + math.sin(a) * L)], rng.uniform(wmin, wmax), (0.0, 0.9)))
    return items


if "scene" in PARTS:
    W, H = 720, 1300
    nx = Seq(100); rng = random.Random(11)
    art = solid(W, H, AUB)
    bands = [(250, WINE, "#5e2035"), (400, MADDER, "#8e2c3c"), (535, BURNT, "#c34a2b"), (650, ORANGE, "#e88032"), (760, GOLD, "#f3ad46")]
    for i, (y, c1, c2) in enumerate(bands):
        art = paint(art, wavy_band(W, H, y, H + 40, 7 + i, 30 + i, wl=0.7 + i * 0.1), c1, c2, seed=nx(), rough=3.5, streak=1.6)
    clear()
    # the sun, big and low
    sun = circles(W, H, [(410, 870, 262)])
    art = over(art, glow(sun, "#ffcf70", 40, 0.35))
    art = paint(art, sun, SUN, SUNL, seed=nx(), rough=2.5, streak=1.4)
    # inner warm rim for weight
    rim = np.clip(sun - circles(W, H, [(418, 862, 238)]), 0, 1)
    art = over(art, flat(gaussian_filter(rim, 6), "#e0812e", 0.55))
    # cloud strips across the sun / sky (thin gouache bars with rounded ends)
    strips = [(40, 300, 430, 316), (300, 452, 700, 470), (-20, 640, 300, 656), (430, 700, 760, 716), (90, 772, 520, 786), (380, 812, 690, 824)]
    cols = [WINE, MADDER, MADDER, BURNT, BURNT, "#cf5f2c"]
    for (x0, y0, x1, y1), c in zip(strips, cols):
        m = rrect(W, H, [(x0, y0, x1, y1, (y1 - y0) / 2)])
        art = paint(art, m, c, mix(c, "#000000", 0.08), seed=nx(), rough=2.0)
    clear()
    # far ridge (muted plum) + elephants walking along it
    ridge = hills(W, H, 884, 10, 5, 0.9)
    art = paint(art, ridge, "#8a3b3f", "#7a3340", seed=nx(), rough=2.0)
    herd = np.zeros((H, W), np.float32)
    for i, (x, hh) in enumerate(((520, 26), (556, 30), (588, 22), (612, 17))):
        herd = np.maximum(herd, elephant(W, H, x, 884 - 1, hh, rng, face=1))
    art = paint(art, herd, "#5a2430", seed=nx(), rough=0.8)
    # distant acacia right
    t, c = acacia(W, H, 640, 900, 120, rng, 1.1)
    art = paint(art, np.maximum(t, c), "#5c2530", "#4e1f2b", seed=nx(), rough=1.4)
    clear()
    # golden grass plain
    plain = wavy_band(W, H, 892, H + 40, 4, 77, 1.2)
    art = paint(art, plain, OCHRE, "#e0a040", seed=nx(), rough=2.0, streak=2.0)
    art = over(art, flat(gaussian_filter(wavy_band(W, H, 960, H + 40, 8, 78, 0.9), 18), OCHRE_D, 0.55))
    gb = strokes(W, H, grass_blades(W, H, 900, 1010, 520, rng, 8, 22, 0.8, 1.6))
    art = paint(art, gb, "#b5701f", "#c98328", seed=nx(), rough=0.6)
    gl = strokes(W, H, grass_blades(W, H, 905, 1000, 260, rng, 6, 16, 0.7, 1.3))
    art = paint(art, gl, "#f4c262", seed=nx(), rough=0.5)
    clear()
    # mid giraffes (a tall one and a young one)
    gm = np.maximum(giraffe(W, H, 470, 978, 190, rng, -1), giraffe(W, H, 404, 984, 122, rng, -1))
    art = paint(art, gm, "#3a1518", "#2a1014", seed=nx(), rough=1.0)
    # grass in front of the giraffes' feet
    art = paint(art, strokes(W, H, grass_blades(W, H, 975, 1000, 160, rng, 10, 24, 1.0, 2.0)), "#a9661f", "#b8742a", seed=nx(), rough=0.6)
    clear()
    # dark foreground with tufts
    fg = wavy_band(W, H, 1010, H + 40, 10, 91, 0.5)
    tufts = strokes(W, H, grass_blades(W, H, 1000, 1040, 520, rng, 18, 54, 1.6, 3.4, 0.35))
    art = paint(art, np.maximum(fg, tufts), EARTH, "#2a130e", seed=nx(), rough=2.0, streak=1.2)
    art = over(art, flat(gaussian_filter(wavy_band(W, H, 1090, H + 40, 6, 92, 0.6), 20), SIL, 0.6))
    # big foreground acacia (left), crossing into the sky bands
    t, c = acacia(W, H, 92, 1060, 470, rng, 1.05)
    art = paint(art, t, "#1e0c0f", "#2b1214", seed=nx(), rough=1.6)
    art = paint(art, c, "#1c0b0e", "#2c1216", seed=nx(), rough=2.6, streak=1.4)
    # light catches the canopy top edge
    edge = np.clip(c - np.roll(c, 4, 0), 0, 1) * (np.arange(W)[None, :] > 120)
    art = over(art, flat(gaussian_filter(edge, 1.2), "#b4452c", 0.55))
    clear()
    art = add_grain(art, 4, 0.05)
    show(art, "sabana-scene", bg=AUB)
    save_rgb(art, f"{OUT}/scene.webp", (720, 1300), quality=80)
    clear()

if "ridge" in PARTS:
    W, H = 900, 230
    nx = Seq(300); rng = random.Random(23)
    art = blank(W, H)
    base = wavy_band(W, H, 180, H + 30, 5, 3, 0.8)
    tufts = strokes(W, H, grass_blades(W, H, 176, 196, 420, rng, 10, 30, 1.4, 2.8, 0.3))
    t1, c1 = acacia(W, H, 150, 196, 170, rng, 1.2)
    t2, c2 = acacia(W, H, 760, 194, 118, rng, 1.0)
    gf = np.maximum(giraffe(W, H, 560, 194, 150, rng, 1), giraffe(W, H, 612, 196, 98, rng, 1))
    el = np.maximum(elephant(W, H, 330, 192, 40, rng, -1), elephant(W, H, 380, 192, 32, rng, -1))
    m = np.clip(base + tufts + t1 + c1 + t2 + c2 + gf + el, 0, 1)
    art = paint(art, m, SIL, "#33151a", seed=nx(), rough=1.4)
    show(art, "sabana-ridge", bg=BURNT)
    save(art, f"{OUT}/ridge.webp", max_w=900, quality=82)
    clear()

if "acacia" in PARTS:
    W, H = 420, 300
    nx = Seq(400); rng = random.Random(5)
    art = blank(W, H)
    t, c = acacia(W, H, 210, 290, 260, rng, 1.3)
    gr = strokes(W, H, grass_blades(W, H, 282, 294, 90, rng, 6, 18, 1.0, 2.0) + [([(40, 292), (380, 292)], 3, None)])
    art = paint(art, np.clip(t + gr, 0, 1), "#3a1a16", seed=nx(), rough=1.0)
    art = paint(art, c, "#3a1a16", "#4a2118", seed=nx(), rough=1.8)
    show(art, "sabana-acacia")
    save(art, f"{OUT}/acacia.webp", max_w=360, quality=82)
    clear()

if "giraffe" in PARTS:
    W, H = 260, 300
    nx = Seq(500); rng = random.Random(9)
    art = blank(W, H)
    g = giraffe(W, H, 110, 290, 270, rng, 1)
    art = paint(art, g, "#3a1518", "#2a1014", seed=nx(), rough=1.0)
    show(art, "sabana-giraffe", bg=GOLD)
    save(art, f"{OUT}/giraffe.webp", max_w=220, quality=82)
    clear()

if "sun" in PARTS:
    W, H = 400, 400
    nx = Seq(600); rng = random.Random(3)
    art = blank(W, H)
    sun = circles(W, H, [(200, 200, 180)])
    art = paint(art, sun, ORANGE, SUN, seed=nx(), rough=2.2, streak=1.4)
    for k, y in enumerate((236, 276, 312, 344)):
        cut = shapes(W, H, [rr(0, y, W, y + 10 - k * 1.5)], smooth=False) * sun
        art = paint(art, cut, [MADDER, BURNT, WINE, MADDER][k], seed=nx(), rough=1.2)
    t, c = acacia(W, H, 150, 352, 190, rng, 1.0)
    art = paint(art, np.clip((t + c) * gaussian_filter(sun, 2) * 1.2, 0, 1), SIL, seed=nx(), rough=1.0)
    show(art, "sabana-sun")
    save(art, f"{OUT}/sun.webp", max_w=260, quality=84)
    clear()

if "stripes" in PARTS:
    W, H = 420, 60
    nx = Seq(700)
    art = blank(W, H)
    for k, (x0, x1, y, c) in enumerate(((20, 170, 22, BURNT), (250, 400, 22, BURNT), (60, 168, 36, GOLD), (252, 360, 36, GOLD))):
        art = paint(art, rrect(W, H, [(x0, y - 4, x1, y + 4, 4)]), c, seed=nx(), rough=1.4)
    sun = circles(W, H, [(210, 30, 20)])
    art = paint(art, sun, ORANGE, SUN, seed=nx(), rough=1.2)
    show(art, "sabana-stripes")
    save(art, f"{OUT}/stripes.webp", max_w=340, quality=84)
    clear()

if "paper" in PARTS:
    img = paper(360, 360, "#f5e6cc", seed=12, fiber=0.8, mottle=0.9)
    save_texture(img, f"{OUT}/paper.webp", quality=76)
    print("paper", os.path.getsize(f"{OUT}/paper.webp") // 1024, "KB")
