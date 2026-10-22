"""Cyanotype Biru — sun prints: Prussian-blue brush-coated paper with white botanical silhouettes (fern fronds, wild
grasses, Queen Anne's lace) with soft lifted edges, tissue translucency and exposure gradients.
Run: python3 -I cyanotype-biru.py [part ...]
parts: tile edge fern lace grass sprig divider card. Assets -> public/themes/art/cyanotype-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d4_lib import *

OUT = outdir("cyanotype-biru")
PARTS = sys.argv[1:] or ["tile", "edge", "fern", "lace", "grass", "sprig", "divider", "card"]


if "tile" in PARTS:
    n = 384
    rng = np.random.default_rng(11)
    e = 0.9 + 0.1 * wrap_noise(n, n, 12, 30)
    e *= 0.9 + 0.1 * norm(gaussian_filter(rng.random((n, n)).astype(np.float32), (1.2, 30), mode="wrap"))
    e *= 0.97 + 0.03 * wrap_noise(n, n, 13, 0.8)
    col = lerp3(PRUSSIAN_L, PRUSSIAN, np.clip(e * 1.05, 0, 1))
    dark = np.clip((e - 0.9) * 6, 0, 1)[..., None] * 0.35
    col = col * (1 - dark) + np.array(hex_rgb(PRUSSIAN_D), np.float32) * dark
    # tiny unexposed dust specks
    sp = (rng.random((n, n)) > 0.99975).astype(np.float32)
    sp = np.clip(gaussian_filter(sp, 0.9, mode="wrap") * 5, 0, 1)[..., None]
    col = col * (1 - sp * 0.35) + np.array(hex_rgb("#c9d8e8"), np.float32) * sp * 0.35
    save_rgb(np.concatenate([col, np.ones((n, n, 1), np.float32)], -1), f"{OUT}/tile.webp", quality=70)
    clear()

if "edge" in PARTS:
    # brush-coated sheet mask (white = coat). Used as CSS mask-image, stretched 100% 100%.
    W, H = 420, 640
    c = coat_mask(W, H, 21, inset=(26, 26, 26, 30), strokes_n=8, dry=0.75)
    a = np.clip(c / 0.88, 0, 1)
    save_full(rgba(np.ones((H, W, 3), np.float32), a), f"{OUT}/edge.webp", quality=70)
    preview(rgba(lerp3(PRUSSIAN, PRUSSIAN, a), a), "cy-edge", tone=CY_PAPER)
    # tall sheet (cover / closing proportions)
    W, H = 400, 860
    c = coat_mask(W, H, 23, inset=(22, 24, 22, 26), strokes_n=12, dry=0.7)
    a = np.clip(c / 0.88, 0, 1)
    save_full(rgba(np.ones((H, W, 3), np.float32), a), f"{OUT}/sheet.webp", quality=70)
    preview(rgba(lerp3(PRUSSIAN, PRUSSIAN, a), a), "cy-sheet", tone=CY_PAPER)
    clear()

if "fern" in PARTS:
    W, H = 560, 1100
    rng = random.Random(31)
    rach = curve([(330, 1090), (300, 900), (250, 640), (220, 380), (240, 170), (300, 40)], 120)
    polys, st = fern_items(rach, rng, scale=1.05)
    m = np.maximum(shapes(W, H, polys), strokes(W, H, st))
    # a second smaller frond behind (more lifted → softer, paler)
    rach2 = curve([(360, 1090), (400, 900), (460, 720), (500, 560)], 60)
    p2, s2 = fern_items(rach2, rng, scale=0.62, lean=1.15)
    m2 = np.maximum(shapes(W, H, p2), strokes(W, H, s2))
    art = silhouette(W, H, [(m2, 0.62, 5.0), (m, 0.95, 1.6)], 32)
    preview(art, "cy-fern", bg=PRUSSIAN)
    save(art, f"{OUT}/fern.webp", max_w=300, quality=78)
    clear()

if "lace" in PARTS:
    W, H = 620, 1000
    rng = random.Random(41)
    st, dots_ = lace_items(300, 210, 190, rng, stem_to=(250, 995))
    st2, d2 = lace_items(470, 470, 110, rng, stem_to=(270, 900))
    # feathery basal leaves
    lf = []
    for (bx, by, side, L) in [(262, 860, -1, 150), (266, 780, 1, 130), (270, 700, -1, 100)]:
        main = curve([(bx, by), (bx + side * L * 0.55, by - L * 0.35), (bx + side * L, by - L * 0.3)], 20)
        lf.append((main, 2.0, (0.0, 0.6)))
        for (x, y, a) in along(main, 13):
            for sg in (-1, 1):
                aa = a + sg * 0.95
                lf.append(([(x, y), (x + math.cos(aa) * 20, y + math.sin(aa) * 20 - 3)], 2.6, (0.0, 0.7)))
    m = np.maximum(strokes(W, H, st + st2 + lf), circles(W, H, dots_ + d2))
    art = silhouette(W, H, [(m, 0.96, 1.4)], 42)
    preview(art, "cy-lace", bg=PRUSSIAN)
    save(art, f"{OUT}/lace.webp", max_w=320, quality=78)
    clear()

if "grass" in PARTS:
    W, H = 700, 700
    rng = random.Random(51)
    polys, st = [], []
    for k in range(7):
        bx = 300 + rng.uniform(-60, 60)
        top = (90 + k * 85 + rng.uniform(-30, 30), 60 + rng.uniform(0, 220))
        p, s = grass_items((bx, 695), top, rng, width=rng.uniform(2.2, 3.4), seeds=k % 3 != 1)
        polys += p; st += s
    blades = [blade_poly((300 + rng.uniform(-50, 50), 700), (rng.uniform(40, 660), rng.uniform(260, 520)), rng.uniform(9, 16), rng.uniform(-1, 1)) for _ in range(9)]
    m_front = np.maximum(shapes(W, H, polys), strokes(W, H, st))
    m_bl = shapes(W, H, blades)
    art = silhouette(W, H, [(m_bl, 0.7, 4.0), (m_front, 0.95, 1.5)], 52)
    preview(art, "cy-grass", bg=PRUSSIAN)
    save(art, f"{OUT}/grass.webp", max_w=340, quality=78)
    clear()

if "sprig" in PARTS:
    W, H = 300, 300
    rng = random.Random(61)
    st, dots_ = lace_items(150, 120, 100, rng, rays=11, sub=9)
    m = np.maximum(strokes(W, H, st + [([(150, 175), (152, 230), (148, 295)], 3.0, (0, .3))]), circles(W, H, dots_))
    art = silhouette(W, H, [(m, 0.97, 1.2)], 62)
    preview(art, "cy-sprig", bg=PRUSSIAN)
    save(art, f"{OUT}/sprig.webp", max_w=120, quality=80)
    clear()

if "divider" in PARTS:
    # a single brushed stripe of sensitiser on paper with a grass stem printed across it
    W, H = 640, 130
    rng = random.Random(71)
    coat = coat_mask(W, H, 72, inset=(40, 30, 40, 30), strokes_n=1, dry=0.9)
    p, s = grass_items((40, 92), (600, 50), rng, width=2.6, seeds=True, n_spk=18)
    p2, s2 = fern_items(curve([(120, 110), (260, 70), (420, 60)], 30), rng, scale=0.26, lean=1.3)
    m = np.maximum(shapes(W, H, p + p2), strokes(W, H, s + s2))
    rgb = cyanotype(W, H, coat, [(m, 0.95, 1.2)], 73)
    a = np.clip(coat / 0.85, 0, 1)
    art = rgba(rgb, a)
    preview(art, "cy-divider", tone=CY_PAPER)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=80)
    clear()

if "card" in PARTS:
    # small full cyanotype print (brush edges) with a lace head and fern tip: used as closing emblem / sent art
    W, H = 460, 560
    rng = random.Random(81)
    coat = coat_mask(W, H, 82, inset=(30, 34, 30, 34), strokes_n=6, dry=0.7)
    st, dots_ = lace_items(230, 180, 130, rng, stem_to=(220, 560), rays=13, sub=10)
    p2, s2 = fern_items(curve([(60, 560), (90, 430), (150, 330)], 30), rng, scale=0.42)
    m = np.maximum(strokes(W, H, st + s2), circles(W, H, dots_))
    m = np.maximum(m, shapes(W, H, p2))
    rgb = cyanotype(W, H, coat, [(m, 0.96, 1.4)], 83)
    art = rgba(rgb, np.clip(coat / 0.85, 0, 1))
    preview(art, "cy-card", tone=CY_PAPER)
    save(art, f"{OUT}/card.webp", max_w=230, quality=80)
    clear()
