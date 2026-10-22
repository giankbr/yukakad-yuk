"""Zaitun Tuscan — watercolour on cold-press paper: silvery olive branches heavy with green-to-aubergine fruit,
terracotta pots, and a Tuscan villa on a hill reached by a cypress lane at golden hour (original design).
Run: python3 -I zaitun-tuscan.py [part ...]  parts: villa branch sprig pot olive linen"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c4_lib import *

OUT = outdir("zaitun-tuscan")
PARTS = sys.argv[1:] or ["villa", "branch", "sprig", "pot", "olive", "linen"]
CREAM = "#f6efe0"
TERRA, TERRA_D, TERRA_L = "#b8603f", "#8a3f28", "#d98a62"
CYP, CYP_D, CYP_L = "#3f4b2f", "#26301d", "#6f7b45"


def ramp(H, W, y0, y1, a0=1.0, a1=0.0):
    t = np.clip((np.arange(H, dtype=np.float32) - y0) / max(1, y1 - y0), 0, 1)
    return (a0 + (a1 - a0) * t)[:, None] * np.ones((1, W), np.float32)


def cypress(W, H, x, by, h, rng, lean=0.0):
    w = h * rng.uniform(0.11, 0.14)
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        k = math.sin(math.pi * min(1, t * 1.25 + 0.05)) ** 0.7 * (1 - t) ** 0.25
        pts.append((x - w * k * rng.uniform(0.9, 1.08) + lean * h * t, by - h * t))
    for i in range(n, -1, -1):
        t = i / n
        k = math.sin(math.pi * min(1, t * 1.25 + 0.05)) ** 0.7 * (1 - t) ** 0.25
        pts.append((x + w * k * rng.uniform(0.9, 1.08) + lean * h * t, by - h * t))
    return pts


if "villa" in PARTS:
    W, H = 820, 780
    nx = Seq(81000); rng = random.Random(5)
    art = blank(W, H)
    full = np.ones((H, W), np.float32)
    # sky: pale gold wash, apricot towards the horizon, a cool lavender veil high up
    art = G(art, full * ramp(H, W, 0, 420, 0.75, 0.95), "#f3dcae", "#f6e6c2", seed=nx(), density=0.55, edge=0.1, bloom=0.4, rough=4, feather=3)
    art = G(art, ramp(H, W, 120, 400, 0.0, 1.0), "#efb487", "#f2c79a", seed=nx(), density=0.5, edge=0.05, bloom=0.5, rough=5, feather=6)
    art = G(art, ramp(H, W, 0, 200, 1.0, 0.0), "#c9b8c6", "#d9cbd2", seed=nx(), density=0.35, edge=0.05, bloom=0.5, rough=5, feather=8)
    # long evening cloud streaks
    cl = ellipses(W, H, [(200, 170, 180, 22, -2), (350, 204, 130, 15, -1), (570, 140, 200, 20, 1), (650, 236, 110, 12, 0), (120, 256, 100, 11, 0)])
    art = G(art, cl, "#eec2a0", "#f3d6b4", seed=nx(), density=0.38, edge=0.35, bloom=0.5, rough=8, feather=6)
    # low sun, right of centre
    sx, sy = 700, 326
    art = over(art, glow(circles(W, H, [(sx, sy, 34)]), "#fff3cf", radius=46, strength=0.8))
    art = G(art, circles(W, H, [(sx, sy, 30)]), "#fbe3a6", "#fff1c6", seed=nx(), density=0.8, edge=0.3, bloom=0.1, rough=1.2)
    # far ridge (blue-violet haze)
    far = ridge(W, H, 338, 16, 3, 0.9)
    art = G(art, far, "#b3a3b6", "#c7b4bf", seed=nx(), density=0.6, edge=0.45, bloom=0.3, rough=3)
    far2 = ridge(W, H, 362, 12, 8, 0.6)
    art = G(art, far2, "#a49aa8", "#b9a7ad", seed=nx(), density=0.45, edge=0.4, bloom=0.3, rough=3)
    # villa hill (sage + ochre), the villa sits on its crest at the right
    hill = shapes(W, H, [[(-20, H), (-20, 470), (120, 432), (300, 404), (470, 380), (560, 368), (660, 372), (760, 392), (W + 20, 412), (W + 20, H)]])
    art = G(art, hill, "#9fa362", "#c2b46e", seed=nx(), density=0.85, edge=0.55, bloom=0.35, rough=3)
    # vineyard rows on the hill flank (curved, converging)
    rows = []
    for k in range(14):
        y0 = 420 + k * 9
        rows.append(curve([(30 + k * 6, y0 + 40), (220, y0 + 8 - k), (380, y0 - 4 - k * 0.4)], 30))
    fadex = np.clip((420 - np.arange(W, dtype=np.float32)) / 170, 0, 1)[None, :] * (0.75 + 0.5 * fbm(W, H, 77, 40, 2))
    vm = strokes(W, H, [(r, 1.4 + k * 0.08, (0.2, 0.3)) for k, r in enumerate(rows)]) * hill * np.clip(fadex, 0, 1)
    art = G(art, vm, "#6f7a44", seed=nx(), density=0.6, edge=0.3, bloom=0.0, rough=1.2, feather=0.6)
    # front field: wheat gold, sweeping
    field = shapes(W, H, [[(-20, H), (-20, 560), (160, 520), (380, 506), (600, 520), (W + 20, 545), (W + 20, H)]])
    art = G(art, field, "#d9b56a", "#e6c886", seed=nx(), density=0.8, edge=0.5, bloom=0.4, rough=3)
    sweeps = [curve([(x, H), (x + rng.uniform(30, 90), 640), (x + rng.uniform(120, 200), 540 + rng.uniform(0, 20))], 30) for x in range(-200, W, 38)]
    art = G(art, strokes(W, H, [(s_, rng.uniform(2, 5), (0.3, 0.4)) for s_ in sweeps]) * field, "#c49a52", seed=nx(), density=0.4, edge=0.3, bloom=0, rough=1.5)
    # the lane: from the bottom up to the villa gate
    lane_c = bez((430, H + 10), (380, 640), (520, 480), (568, 392), 60)
    lane = []
    for i, (x, y) in enumerate(lane_c):
        t = i / (len(lane_c) - 1)
        lane.append((x, y, 46 * (1 - t) ** 1.2 + 3))
    lp = [(x - w, y) for x, y, w in lane] + [(x + w, y) for x, y, w in reversed(lane)]
    lane_m = shapes(W, H, [lp])
    art = knockout(art, lane_m, 0.75, 1.5)
    art = G(art, lane_m, "#f1dcae", "#f7e8c6", seed=nx(), density=0.85, edge=0.9, bloom=0.2, rough=2)
    lane_edge = strokes(W, H, [([(x - w, y) for x, y, w in lane], 2.4, (0.05, 0.5)), ([(x + w, y) for x, y, w in lane], 2.4, (0.05, 0.5))])
    art = G(art, lane_edge, "#b58d55", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1.2)
    # villa: main block + tower + loggia
    vx, vy = 560, 372
    wall = poly(W, H, [(vx - 60, vy), (vx - 60, vy - 40), (vx + 50, vy - 40), (vx + 50, vy)])
    side = poly(W, H, [(vx + 50, vy), (vx + 50, vy - 40), (vx + 86, vy - 34), (vx + 86, vy + 4)])
    tower = poly(W, H, [(vx - 40, vy - 40), (vx - 40, vy - 74), (vx - 12, vy - 74), (vx - 12, vy - 40)])
    roof = poly(W, H, [(vx - 68, vy - 38), (vx - 44, vy - 54), (vx + 58, vy - 54), (vx + 92, vy - 34), (vx + 52, vy - 38)])
    troof = poly(W, H, [(vx - 46, vy - 72), (vx - 26, vy - 88), (vx - 6, vy - 72)])
    art = G(art, np.maximum(wall, tower), "#ecc995", "#f3d7a8", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=0.8, feather=0.6, pad=8)
    art = G(art, side, "#c99764", "#b98656", seed=nx(), density=0.85, edge=0.5, bloom=0.1, rough=0.8, feather=0.6, pad=8)
    art = G(art, np.maximum(roof, troof), TERRA, TERRA_L, seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=0.8, feather=0.6, pad=8)
    wins = [(vx - 48 + k * 20, vy - 30) for k in range(5)] + [(vx - 30, vy - 64)]
    wm = shapes(W, H, [[(x, y), (x + 6, y), (x + 6, y + 10), (x, y + 10)] for x, y in wins], smooth=False)
    art = G(art, wm, "#5f6a45", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.4, feather=0.4, pad=6)
    door = shapes(W, H, [[(vx - 4, vy), (vx - 4, vy - 12), (vx + 2, vy - 17), (vx + 8, vy - 12), (vx + 8, vy)]])
    art = G(art, door, "#6a4a32", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.4, feather=0.4, pad=6)
    # warm sunlit edge on the villa's front (sun on the right)
    art = G(art, rect(W, H, vx + 30, vy - 40, vx + 50, vy), "#f7d79b", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=0.5, pad=6)
    # cypresses: two rows along the lane, receding; a cluster behind the villa
    trees = []
    for t in (0.1, 0.22, 0.33, 0.43, 0.52, 0.6, 0.67, 0.73, 0.78, 0.83, 0.87):
        i = int(t * (len(lane) - 1))
        x, y, w = lane[i]
        h = 150 * (1 - t) ** 1.35 + 18
        for side_ in (-1, 1):
            trees.append((x + side_ * (w + 8 + h * 0.1), y + 2, h))
    trees += [(vx - 84, vy + 2, 70), (vx - 74, vy + 4, 54), (vx + 104, vy + 6, 62), (vx + 118, vy + 8, 46), (210, 418, 40), (226, 420, 30)]
    trees.sort(key=lambda t: t[1])
    for x, by, h in trees:
        p = cypress(W, H, x, by, h, rng, lean=rng.uniform(-0.03, 0.03))
        m = shapes(W, H, [p])
        # long cast shadow to the left (sun on the right)
        shp = [(x - h * 0.06, by - 1), (x - h * 0.55, by + h * 0.05), (x - h * 0.5, by + h * 0.085), (x + h * 0.06, by + 2)]
        art = G(art, poly(W, H, shp) * (1 - m), "#7c7348", seed=nx(), density=0.3, edge=0.15, bloom=0, rough=1.5, feather=2.2, pad=12)
        art = G(art, m, CYP, CYP_D, seed=nx(), density=0.92, edge=0.6, bloom=0.25, rough=1.2 + h * 0.01, feather=0.6, pad=10)
        lit = m * np.clip((np.arange(W)[None, :] - (x - 2)) / (h * 0.12 + 2), 0, 1)
        art = G(art, lit, CYP_L, "#8a8a4c", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=1.0, pad=10)
    # a few poppies in the near field
    pops = [(rng.uniform(20, W - 20), rng.uniform(640, H - 30), rng.uniform(2.5, 4.5)) for _ in range(40)]
    pops = [p for p in pops if abs(p[0] - np.interp(p[1], [y for x, y, w in lane[::-1]], [x for x, y, w in lane[::-1]])) > 60]
    art = G(art, circles(W, H, pops), "#c4462e", "#d9603e", seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.8)
    # golden hour glaze from the right
    gl = light_mask(H, W, sx, sy, 520)
    art = G(art, gl * full, "#f4b46b", seed=nx(), density=0.28, edge=0.0, bloom=0.4, rough=4, feather=10)
    art[..., 3] *= soft_edge(W, H, nx(), inset=0.02, power=3.0)
    art[..., 3] *= np.clip(ramp(H, W, H - 170, H - 10, 1.0, 0.0) + 0.0, 0, 1)
    preview(art, "zt-villa", tone=CREAM)
    save(art, f"{OUT}/villa.webp", max_w=780, quality=80)
    clear()

if "branch" in PARTS:
    # corner swag: a branch entering from the top-left, arching down to the right, with fruit
    W, H = 820, 520
    nx = Seq(81200); rng = random.Random(21)
    sp1 = bez((-10, 40), (200, 30), (420, 120), (700, 300), 80)
    sp2 = bez((180, 52), (240, 150), (250, 240), (230, 360), 40)
    sp3 = bez((430, 130), (520, 110), (610, 90), (720, 110), 40)
    art = blank(W, H)
    art = olive_branch(W, H, sp2, rng, nx, art, leaf_len=(40, 60), spacing=16, fruit=0.4, scale=1.0, stem_w=3.0)
    art = olive_branch(W, H, sp3, rng, nx, art, leaf_len=(38, 56), spacing=16, fruit=0.3, scale=0.95, stem_w=2.6)
    art = olive_branch(W, H, sp1, rng, nx, art, leaf_len=(50, 74), spacing=15, fruit=0.45, scale=1.05, stem_w=6.0)
    preview(art, "zt-branch", tone=CREAM)
    save(art, f"{OUT}/branch.webp", max_w=640, quality=80)
    clear()

if "sprig" in PARTS:
    W, H = 520, 120
    nx = Seq(81300); rng = random.Random(4)
    art = blank(W, H)
    sp = curve([(20, 70), (200, 58), (340, 60), (500, 46)], 60)
    art = olive_branch(W, H, sp, rng, nx, art, leaf_len=(26, 38), spacing=12, fruit=0.35, scale=0.8, stem_w=2.4)
    preview(art, "zt-sprig", tone=CREAM)
    save(art, f"{OUT}/sprig.webp", max_w=360, quality=82)
    clear()

if "pot" in PARTS:
    # terracotta pot (rolled rim, garland band) with a small olive tree
    W, H = 420, 520
    nx = Seq(81400); rng = random.Random(9)
    art = blank(W, H)
    cx, top, bot = 210, 330, 500
    body = shapes(W, H, [[(cx - 118, top + 22), (cx - 112, top + 80), (cx - 84, bot - 10), (cx - 60, bot), (cx + 60, bot), (cx + 84, bot - 10), (cx + 112, top + 80), (cx + 118, top + 22)]])
    rim = ellipses(W, H, [(cx, top + 14, 128, 20, 0)])
    rimband = rect(W, H, cx - 128, top - 2, cx + 128, top + 26)
    rim = np.maximum(rim, rimband * ellipses(W, H, [(cx, top + 12, 128, 40, 0)]))
    soil = ellipses(W, H, [(cx, top + 2, 112, 12, 0)])
    # trunk + branches first (behind the rim)
    trunk = strokes(W, H, [(curve([(cx + 4, top + 4), (cx - 14, top - 70), (cx + 10, top - 130), (cx - 4, top - 170)], 30), 13, (0.0, 0.4)),
                           (curve([(cx - 4, top - 100), (cx - 60, top - 150), (cx - 110, top - 170)], 20), 6, (0.0, 0.6)),
                           (curve([(cx + 6, top - 120), (cx + 60, top - 170), (cx + 110, top - 190)], 20), 6, (0.0, 0.6))])
    art = G(art, trunk, "#7a6a55", "#5a4c3c", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=1.2)
    for sp, sc in [(curve([(cx - 4, top - 160), (cx - 60, top - 230), (cx - 150, top - 250)], 30), 0.9),
                   (curve([(cx - 4, top - 160), (cx + 50, top - 250), (cx + 150, top - 260)], 30), 0.9),
                   (curve([(cx - 6, top - 168), (cx - 10, top - 250), (cx + 4, top - 320)], 30), 0.85),
                   (curve([(cx - 60, top - 150), (cx - 120, top - 170), (cx - 170, top - 150)], 20), 0.75),
                   (curve([(cx + 60, top - 170), (cx + 120, top - 200), (cx + 175, top - 180)], 20), 0.75)]:
        art = olive_branch(W, H, sp, rng, nx, art, leaf_len=(30, 44), spacing=11, fruit=0.25, scale=sc, stem_w=2.0)
    art = G(art, soil, "#5a4434", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=1)
    art = knockout(art, np.maximum(body, rim), 1.0, 0.8)
    art = G(art, body, TERRA, TERRA_L, seed=nx(), density=0.92, edge=0.6, bloom=0.3, rough=1.5)
    art = G(art, body * np.clip((np.arange(W)[None, :] - (cx + 10)) / 100, 0, 1), TERRA_D, seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1)
    # garland band pressed into the clay
    band = np.zeros((H, W), np.float32)
    swg = []
    for k in range(5):
        x0 = cx - 100 + k * 40
        swg.append(curve([(x0, top + 70), (x0 + 20, top + 88), (x0 + 40, top + 70)], 14))
    band = strokes(W, H, [(s_, 4, None) for s_ in swg]) * body
    art = G(art, band, TERRA_D, seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.6)
    art = over(art, flat(gaussian_filter(np.roll(band, -2, 0), 0.8) * body * 0.6, "#f0b08c", 0.5))
    art = G(art, rim, "#c46e4a", "#dc916a", seed=nx(), density=0.92, edge=0.6, bloom=0.2, rough=1.2)
    art = G(art, rim * np.clip((np.arange(W)[None, :] - (cx + 30)) / 100, 0, 1), TERRA_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    sh = ellipses(W, H, [(cx + 20, bot + 4, 120, 10, 0)])
    art = G(art, sh * (1 - body), "#6b5a48", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=2, feather=3)
    preview(art, "zt-pot", tone=CREAM)
    save(art, f"{OUT}/pot.webp", max_w=300, quality=82)
    clear()

if "olive" in PARTS:
    W, H = 140, 140
    nx = Seq(81500); rng = random.Random(3)
    art = blank(W, H)
    art = G(art, strokes(W, H, [(curve([(70, 18), (66, 50), (52, 78)], 12), 2.2, None), (curve([(68, 40), (84, 62), (92, 84)], 12), 2.0, None)]), "#6d5b46", seed=nx(), density=0.9, edge=0.4, rough=0.6)
    lv = [olive_leaf_poly(70, 22, 46, -2.4, 0.16, 0.05), olive_leaf_poly(70, 24, 50, -0.6, 0.16, -0.05)]
    art = G(art, shapes(W, H, lv[:1]), OLV_UNDER[0], OLV_UNDER[1], seed=nx(), density=0.85, edge=0.6, rough=0.8, feather=0.6)
    art = G(art, shapes(W, H, lv[1:]), OLV_TOP[0], OLV_TOP[1], seed=nx(), density=0.88, edge=0.6, rough=0.8, feather=0.6)
    for (x, y, rx, ry, rot), (ca, cb) in zip([(50, 92, 13, 18, 20), (94, 96, 12, 17, -15)], [OLV_FRUIT[1], OLV_FRUIT[0]]):
        art = G(art, ellipses(W, H, [(x, y, rx, ry, rot)]), ca, cb, seed=nx(), density=0.95, edge=0.6, bloom=0.1, rough=0.6, feather=0.5)
        art = over(art, flat(gaussian_filter(circles(W, H, [(x - 4, y - 6, 3.5)]), 0.8), "#fff6e6", 0.6))
    preview(art, "zt-olive", tone=CREAM)
    save(art, f"{OUT}/olive.webp", max_w=72, quality=84)
    clear()

if "linen" in PARTS:
    # cold-press paper tile, warm cream, seamless
    W = H = 360
    im = paper(W, H, "#f4ecdc", seed=81600, fiber=0.6, mottle=0.5)
    arr = np.asarray(im, np.float32) / 255
    arr = tile_wrap_rgb(arr) if "tile_wrap_rgb" in globals() else arr
    h, w = arr.shape[:2]
    sh = np.roll(np.roll(arr, h // 2, 0), w // 2, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = np.clip(np.minimum(np.minimum(xx, w - 1 - xx) / (w / 2), np.minimum(yy, h - 1 - yy) / (h / 2)) * 2.4, 0, 1)[..., None]
    arr = arr[..., :3] * k + sh[..., :3] * (1 - k)
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB").save(f"{OUT}/linen.webp", "WEBP", quality=72, method=6)
    print("linen", os.path.getsize(f"{OUT}/linen.webp") // 1024, "KB")

kb_total(OUT)
