"""Padang Liar — a breezy wildflower meadow in loose watercolour: pink & magenta cosmos with thread-fine foliage,
chamomile daisies, ragged blue cornflowers, wild oat grasses and a pale brimstone butterfly.
Run: python3 -I padang-liar.py [part ...]  parts: meadow cosmos tuft posy sprig kupu daisy
Assets -> public/themes/art/padang-liar/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c5_lib import *

OUT = outdir("padang-liar")
PARTS = sys.argv[1:] or ["meadow", "cosmos", "tuft", "posy", "sprig", "kupu", "daisy"]
BG = "#fbf8ef"
COS = [("#f9cfe0", "#ec8fb6", "#c8447e", "#f3c43a"), ("#fbe3ea", "#f2a9c4", "#d0608f", "#f3c43a"),
       ("#f4b3cf", "#d9578f", "#a8235f", "#f0b92e"), ("#fdf0f3", "#f6c5d6", "#e07ea4", "#f3c43a")]
CORN = [("#8fa8e8", "#4167c8", "#23307a"), ("#a6b8ee", "#5b7ad3", "#2d3b8a"), ("#b9a8e8", "#6f62c8", "#3a2f86")]
GRASS = [("#b8cc7a", "#6f9a44"), ("#a4c06a", "#55823a"), ("#c9d48e", "#8aa555"), ("#93b663", "#4b7535")]
STEM = ("#86a852", "#4f7a35")


def grass(art, W, H, nx, rng, x, y, h, n, spread=0.45, width=(2.2, 4.6), lean=0.0, base=30, dens=0.5):
    for k in range(2):
        it = grass_items(rng, x, y, h, n // 2, spread, width, lean, base)
        c = GRASS[rng.randrange(len(GRASS))]
        art = G(art, strokes(W, H, it), c[0], c[1], seed=nx(), density=dens, edge=0.45, bloom=0.15, rough=1.4, feather=0.55, gran=0.15)
    return art


def stem(art, W, H, nx, pts, w=2.6, c=STEM):
    return G(art, strokes(W, H, [(pts, w, (0.0, 0.08))]), c[0], c[1], seed=nx(), density=0.75, edge=0.35, bloom=0, rough=0.8, feather=0.45, pad=8)


def foliage(art, W, H, nx, rng, specs):
    items = []
    for x, y, L, a in specs:
        items += feather_leaf(rng, x, y, L, a)
    return G(art, strokes(W, H, items), "#97b65e", "#5b8a3a", seed=nx(), density=0.68, edge=0.3, bloom=0, rough=0.8, feather=0.4)


def flower_on_stem(art, W, H, nx, rng, kind, x0, y0, x, y, R, bend=0.0, tilt=0.8, ta=None, pal=None):
    ta = rng.uniform(0, math.pi) if ta is None else ta
    art = stem(art, W, H, nx, stem_pts(x0, y0, x, y, bend), w=max(1.6, R * 0.05))
    if kind == "cos":
        return cosmos(art, W, H, x, y, R, nx, rng, pal or COS[rng.randrange(len(COS))], tilt=tilt, tilt_a=ta)
    if kind == "cham":
        return chamomile(art, W, H, x, y, R, nx, rng, tilt=tilt, tilt_a=ta)
    return cornflower(art, W, H, x, y, R, nx, rng, pal or CORN[rng.randrange(len(CORN))], tilt=tilt, tilt_a=ta)


if "meadow" in PARTS:
    W, H = 1000, 540
    nx = Seq(50100); rng = random.Random(51)
    art = blank(W, H)
    # soft distant meadow wash
    hill = shapes(W, H, [[(-20, H), (-20, 300), (180, 270), (420, 300), (650, 262), (860, 290), (1020, 270), (1020, H)]])
    art = G(art, hill, "#dfe8b8", "#bcd290", seed=nx(), density=0.45, edge=0.35, bloom=0.5, rough=8, feather=3)
    ground = shapes(W, H, [[(-20, H), (-20, 430), (250, 410), (520, 440), (760, 405), (1020, 425), (1020, H)]])
    art = G(art, ground, "#b7cd7e", "#7ea44c", seed=nx(), density=0.6, edge=0.3, bloom=0.4, rough=8, feather=3)
    # distant dabs of colour (flowers far away)
    far = []
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(300, 430)
        far.append((x, y, rng.uniform(3, 6.5), rng.uniform(2, 4), rng.uniform(0, 180)))
    fm = ellipses(W, H, far[:30]); fm2 = ellipses(W, H, far[30:50]); fm3 = ellipses(W, H, far[50:])
    art = G(art, fm, "#f2a9c4", "#e07ea4", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1.2, feather=0.8)
    art = G(art, fm2, "#8fa8e8", "#5b7ad3", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1.2, feather=0.8)
    art = OV(art, fm3, lambda m: col_arr(m, "#fffdf6", m * 0.85))
    for x in np.linspace(-20, W + 20, 9):
        art = grass(art, W, H, nx, rng, x + rng.uniform(-30, 30), H + 4, rng.uniform(200, 290), 30, lean=rng.uniform(-0.25, 0.1), dens=0.42)
    clear()
    # mid flowers
    for x in np.linspace(40, W - 40, 11):
        kind = rng.choice(["cos", "cham", "corn", "cham", "cos"])
        y = rng.uniform(250, 340)
        R = rng.uniform(22, 32) if kind != "corn" else rng.uniform(18, 24)
        art = flower_on_stem(art, W, H, nx, rng, kind, x + rng.uniform(-20, 20), H, x, y, R, bend=rng.uniform(-30, 30), tilt=rng.uniform(0.55, 0.85))
    clear()
    for x in np.linspace(0, W, 7):
        art = grass(art, W, H, nx, rng, x + rng.uniform(-40, 40), H + 4, rng.uniform(260, 380), 26, lean=rng.uniform(-0.3, 0.1), width=(2.6, 5.4), dens=0.5)
    # oat grasses
    for x in rng.sample(range(30, W - 30), 6):
        sp = stem_pts(x, H, x + rng.uniform(-40, 10), rng.uniform(110, 200), rng.uniform(-30, 30))
        art = stem(art, W, H, nx, sp, w=2, c=("#c9b873", "#93833f"))
        art = seedhead(art, W, H, sp, nx, rng, size=5.5)
    clear()
    # front flowers, bigger, at the two ends (centre stays calmer for text above)
    front = [("cos", 70, 190, 54), ("cham", 175, 250, 40), ("corn", 120, 300, 32), ("cos", 900, 170, 56), ("corn", 820, 250, 34),
             ("cham", 960, 280, 38), ("cos", 300, 330, 40), ("cham", 650, 330, 34), ("corn", 470, 360, 26), ("cos", 720, 230, 44)]
    for kind, x, y, R in front:
        art = flower_on_stem(art, W, H, nx, rng, kind, x + rng.uniform(-30, 30), H, x, y, R, bend=rng.uniform(-40, 40), tilt=rng.uniform(0.6, 0.9))
        if kind == "cos":
            art = foliage(art, W, H, nx, rng, [(x + rng.uniform(-10, 10), y + 140, 70, rng.uniform(-2.8, -2.2)), (x, y + 200, 64, rng.uniform(-0.9, -0.4))])
    clear()
    for x in np.linspace(-30, W + 30, 8):
        art = grass(art, W, H, nx, rng, x, H + 6, rng.uniform(120, 220), 22, lean=rng.uniform(-0.35, 0.1), width=(3, 6), dens=0.55)
    preview(art, "pl-meadow", tone=BG)
    save_full(art, f"{OUT}/meadow.webp", size=(820, 443), quality=72)
    clear()

if "cosmos" in PARTS:
    W, H = 380, 860
    nx = Seq(50200); rng = random.Random(52)
    art = blank(W, H)
    art = foliage(art, W, H, nx, rng, [(180, 560, 110, -2.5), (190, 640, 100, -0.6), (176, 460, 90, -0.9), (172, 720, 90, -2.3)])
    art = flower_on_stem(art, W, H, nx, rng, "bud", 190, H, 120, 340, 0) if False else art
    s2 = stem_pts(190, H, 260, 300, -10)
    art = stem(art, W, H, nx, s2, w=3)
    art = bud(art, W, H, 260, 300, 30, -1.2, nx, rng, tip=("#f4b3cf", "#d9578f"))
    art = flower_on_stem(art, W, H, nx, rng, "cos", 186, H, 140, 150, 96, bend=40, tilt=0.86, ta=0.4, pal=COS[0])
    art = flower_on_stem(art, W, H, nx, rng, "cos", 192, H, 250, 430, 64, bend=-30, tilt=0.6, ta=1.2, pal=COS[2])
    preview(art, "pl-cosmos", tone=BG)
    art = bud(art, W, H, 262, 296, 44, -1.2, nx, rng, tip=("#f4b3cf", "#d9578f"))
    save(art, f"{OUT}/cosmos.webp", max_w=230, quality=82)
    clear()

if "tuft" in PARTS:
    W, H = 420, 620
    nx = Seq(50300); rng = random.Random(53)
    art = blank(W, H)
    for k in range(3):
        sp = stem_pts(200 + k * 20, H, 120 + k * 90, 80 + k * 40, rng.uniform(-30, 30))
        art = stem(art, W, H, nx, sp, w=2, c=("#c9b873", "#93833f"))
        art = seedhead(art, W, H, sp, nx, rng, size=6.5)
    art = grass(art, W, H, nx, rng, 210, H + 4, 460, 40, spread=0.5, base=40, dens=0.55)
    art = flower_on_stem(art, W, H, nx, rng, "cham", 230, H, 300, 250, 44, bend=20, tilt=0.75, ta=1.4)
    art = flower_on_stem(art, W, H, nx, rng, "corn", 190, H, 110, 300, 34, bend=-20, tilt=0.8, ta=0.2)
    art = grass(art, W, H, nx, rng, 210, H + 4, 260, 24, spread=0.6, base=60, dens=0.6, width=(3, 6))
    preview(art, "pl-tuft", tone=BG)
    save(art, f"{OUT}/tuft.webp", max_w=210, quality=82)
    clear()

if "posy" in PARTS:
    W, H = 560, 600
    nx = Seq(50400); rng = random.Random(54)
    art = blank(W, H)
    cx, ty = 280, 430
    blooms = [("corn", 170, 190, 34), ("cham", 380, 150, 46), ("cos", 270, 140, 74), ("cham", 200, 280, 40), ("corn", 360, 270, 32),
              ("cos", 420, 250, 52), ("cham", 300, 250, 34), ("corn", 250, 70, 28), ("cos", 140, 300, 44)]
    for i, (_, x, y, _) in enumerate(blooms):
        bx = cx + (i - 4) * 3
        art = stem(art, W, H, nx, curve([(x, y), ((x + bx) / 2 + rng.uniform(-8, 8), (y + ty) / 2 + 30), (bx, ty + 52), (bx + (bx - x) * 0.25, ty + 160)], 40), w=2.6)
    for x, y, L, a in [(240, 200, 90, -2.6), (330, 210, 90, -0.4)]:
        art = foliage(art, W, H, nx, rng, [(x, y, L, a)])
    art = grass(art, W, H, nx, rng, cx, ty + 50, 300, 18, spread=0.7, base=10, dens=0.5)
    for kind, x, y, R in blooms:
        if kind == "cos":
            art = cosmos(art, W, H, x, y, R, nx, rng, COS[rng.randrange(3)], tilt=rng.uniform(0.7, 0.95), tilt_a=rng.uniform(0, 3))
        elif kind == "cham":
            art = chamomile(art, W, H, x, y, R, nx, rng, tilt=rng.uniform(0.7, 0.95), tilt_a=rng.uniform(0, 3))
        else:
            art = cornflower(art, W, H, x, y, R, nx, rng, CORN[rng.randrange(3)], tilt=0.85, tilt_a=rng.uniform(0, 3))
    clear()
    # twine bow
    twine = [(curve([(cx - 42, ty + 46), (cx, ty + 56), (cx + 42, ty + 44)], 20), 5),
             (curve([(cx, ty + 52), (cx - 50, ty + 20), (cx - 70, ty + 50), (cx, ty + 54)], 30), 4),
             (curve([(cx, ty + 52), (cx + 46, ty + 24), (cx + 66, ty + 56), (cx, ty + 54)], 30), 4),
             (curve([(cx, ty + 54), (cx - 20, ty + 110), (cx - 36, ty + 150)], 20), 3.5),
             (curve([(cx, ty + 54), (cx + 16, ty + 104), (cx + 40, ty + 140)], 20), 3.5)]
    art = G(art, strokes(W, H, [(p, w, (0.05, 0.1)) for p, w in twine]), "#d7b27a", "#a27a3f", seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.6, feather=0.4)
    preview(art, "pl-posy", tone=BG)
    save(art, f"{OUT}/posy.webp", max_w=300, quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 700, 200
    nx = Seq(50500); rng = random.Random(55)
    art = blank(W, H)
    main = curve([(30, 110), (200, 92), (350, 100), (520, 82), (680, 96)], 80)
    art = stem(art, W, H, nx, main, w=3.2)
    items = []
    for i in range(6, 74, 9):
        px, py = main[i]
        for side in (-1, 1):
            a = -math.pi / 2 * side + rng.uniform(-0.6, 0.6) + 0.3
            L = rng.uniform(34, 58)
            items.append(([(px + math.cos(a) * L * t, py + math.sin(a) * L * t * 0.7) for t in np.linspace(0, 1, 8)], 1.6, (0.0, 0.8)))
    art = G(art, strokes(W, H, items), "#a4c06a", "#5c8a3a", seed=nx(), density=0.6, edge=0.3, bloom=0, rough=0.6, feather=0.35)
    art = cornflower(art, W, H, 350, 92, 44, nx, rng, CORN[0], tilt=0.9, tilt_a=0.3)
    art = chamomile(art, W, H, 245, 88, 36, nx, rng, tilt=0.72, tilt_a=1.3)
    art = chamomile(art, W, H, 458, 84, 32, nx, rng, tilt=0.72, tilt_a=1.6)
    art = bud(art, W, H, 150, 90, 30, -2.4, nx, rng, tip=("#f4b3cf", "#d9578f"))
    art = bud(art, W, H, 565, 80, 28, -0.6, nx, rng, tip=("#a6b8ee", "#5b7ad3"))
    preview(art, "pl-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=340, quality=84)
    clear()

if "kupu" in PARTS:
    W, H = 240, 200
    nx = Seq(50600); rng = random.Random(56)
    art = blank(W, H)
    cx, cy = 120, 104
    up = [deform(ellipse_pts(cx - 44, cy - 34, 50, 34, 20, -0.55), rng, 1, 0.015), deform(ellipse_pts(cx + 42, cy - 32, 47, 32, 20, 0.5), rng, 1, 0.015)]
    lo = [deform(ellipse_pts(cx - 28, cy + 28, 32, 24, 18, 0.7), rng, 1, 0.015), deform(ellipse_pts(cx + 27, cy + 27, 30, 23, 18, -0.7), rng, 1, 0.015)]
    art = G(art, shapes(W, H, lo), "#f7d57a", "#f0a94a", seed=nx(), density=0.65, edge=0.6, bloom=0.4, rough=2, feather=0.9)
    art = G(art, shapes(W, H, up), "#fbe39a", "#f2b552", seed=nx(), density=0.65, edge=0.6, bloom=0.4, rough=2, feather=0.9)
    dots = circles(W, H, [(cx - 50, cy - 40, 5), (cx + 46, cy - 38, 4.5), (cx - 30, cy + 34, 3.5), (cx + 28, cy + 32, 3.5)])
    art = G(art, dots, "#e0782e", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=0.8, feather=0.6, pad=6)
    bd = strokes(W, H, [([(cx, cy - 26), (cx, cy + 40)], 6, (0.2, 0.5)), (curve([(cx, cy - 24), (cx - 14, cy - 50), (cx - 24, cy - 62)], 10), 1.4, None),
                        (curve([(cx, cy - 24), (cx + 12, cy - 50), (cx + 22, cy - 62)], 10), 1.4, None)])
    art = G(art, bd, "#6d5a3a", "#4a3a26", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.5, feather=0.4, pad=6)
    preview(art, "pl-kupu", tone=BG)
    save(art, f"{OUT}/kupu.webp", max_w=100, quality=84)
    clear()

if "daisy" in PARTS:
    W, H = 200, 200
    nx = Seq(50700); rng = random.Random(57)
    art = blank(W, H)
    art = chamomile(art, W, H, 100, 100, 80, nx, rng, tilt=0.95, tilt_a=0.5, n=17)
    preview(art, "pl-daisy", tone=BG)
    save(art, f"{OUT}/daisy.webp", max_w=80, quality=86)
    clear()
