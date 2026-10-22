"""Ternate Gamalama — Kedaton (istana) Kesultanan Ternate on its hill, the Gamalama cone rising out of the Halmahera sea,
in watercolour; a botanical spray of nutmeg (split fruit with crimson mace) and clove buds; a small clove sprig and a
gold-foil eight-point star. Run: python3 -I ternate-gamalama.py [part ...]   parts: gamalama rempah cengkih bintang"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e1_lib import *

OUT = outdir("ternate-gamalama")
PARTS = sys.argv[1:] or ["gamalama", "rempah", "cengkih", "bintang"]
NAVY, SEA, SEA_L = "#123a63", "#1f5f8f", "#6aa6c8"
MACE, MACE_D = "#c42a2c", "#8a1420"
LEAF, LEAF_D, LEAF_L = "#3f6b3a", "#284a2a", "#7a9a52"


def leaf_poly(x, y, L, Wd, ang, rng):
    return deform(petal_pts(x, y, L, Wd, ang, n=14), rng, 1, 0.04)


def paint_leaf(art, W, H, x, y, L, Wd, ang, rng, nx, light=False):
    m = poly(W, H, leaf_poly(x, y, L, Wd, ang, rng))
    art = G(art, m, LEAF_L if light else LEAF, LEAF if light else LEAF_D, seed=nx(), density=0.9, edge=0.6, bloom=0.35, rough=1.5, gran=0.2)
    # midrib + side light
    ex, ey = x + math.cos(ang) * L, y + math.sin(ang) * L
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#d9e3b0"), strokes(W, H, [([(x, y), ((x + ex) / 2, (y + ey) / 2), (ex, ey)], 1.4, (0.0, 0.6))]) * m * 0.55))
    return art


def nutmeg(art, W, H, cx, cy, r, rng, nx, split=True, ang=0.0):
    """Nutmeg fruit: apricot-yellow husk; split open showing the dark seed laced with crimson mace."""
    husk = poly(W, H, deform(ellipse_pts(cx, cy, r, r * 1.08, 18, ang), rng, 1, 0.02))
    art = knockout(art, husk, 1.0, 1.5)
    art = G(art, husk, "#f0d07a", "#e2a95a", seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=1.5, gran=0.25)
    yy, xx = ygrid(W, H)
    art = G(art, husk * np.clip((xx - cx + r * 0.2) / (r * 1.4), 0, 1), "#b9773a", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=1.5)
    if not split:
        art = G(art, strokes(W, H, [([(cx, cy - r * 1.02), (cx + r * 0.08, cy), (cx, cy + r * 1.02)], 1.6, (0.1, 0.1))]), "#9c6a32", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6)
        return art
    # the opening: an almond-shaped gap showing the seed
    gap = poly(W, H, [(cx - r * 0.1, cy - r * 0.95), (cx + r * 0.42, cy - r * 0.2), (cx + r * 0.32, cy + r * 0.6), (cx - r * 0.05, cy + r * 0.98), (cx - r * 0.38, cy + r * 0.3), (cx - r * 0.42, cy - r * 0.4)])
    art = GP(art, gap, "#4a2a1c", "#2e1a12", seed=nx(), rough=0.6)
    seed_m = poly(W, H, deform(ellipse_pts(cx, cy + r * 0.05, r * 0.36, r * 0.62, 14, 0.1), rng, 1, 0.03)) * gap
    art = G(art, seed_m, "#5a3424", "#3a2016", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=1)
    # mace: branching crimson aril strands over the seed
    lace = []
    for k in range(9):
        x0 = cx + rng.uniform(-r * 0.3, r * 0.3)
        pts = [(x0, cy - r * 0.6)]
        for j in range(5):
            pts.append((pts[-1][0] + rng.uniform(-r * 0.14, r * 0.14), pts[-1][1] + r * 0.26))
        lace.append((pts, rng.uniform(2.2, 3.6) * r / 40, (0.1, 0.2)))
    lm = strokes(W, H, lace) * np.clip(gaussian_filter(gap, 1.5) * 1.4, 0, 1)
    art = G(art, lm, MACE, "#de3b33", seed=nx(), density=0.95, edge=0.4, bloom=0.1, rough=0.6)
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ff9a7a"), np.roll(lm, -1, 1) * lm * 0.25))
    # husk lips catch light
    lip = np.clip(gaussian_filter(gap, 2) - gap, 0, 1) * husk
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#fff0c0"), lip * 1.2))
    return art


def cloves(art, W, H, bx, by, n, spread, length, ang, rng, nx):
    """A cyme of clove buds: thin stalks fanning from (bx,by), each ending in a red-pink bud with a round head."""
    stalks, buds, heads = [], [], []
    for k in range(n):
        a = ang + (k / max(1, n - 1) - 0.5) * spread + rng.uniform(-0.08, 0.08)
        L = length * rng.uniform(0.7, 1.0)
        mx, my = bx + math.cos(a) * L * 0.5, by + math.sin(a) * L * 0.5
        ex, ey = bx + math.cos(a) * L, by + math.sin(a) * L
        stalks.append(([(bx, by), (mx + rng.uniform(-2, 2), my), (ex, ey)], 1.6 * length / 80, (0.0, 0.3)))
        bl = length * 0.26
        buds.append(petal_pts(ex, ey, bl, bl * 0.28, a, n=10))
        heads.append((ex + math.cos(a) * bl * 1.05, ey + math.sin(a) * bl * 1.05, bl * 0.24))
    art = G(art, strokes(W, H, stalks), "#7f8a3c", "#9a7a3a", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6)
    art = knockout(art, np.maximum(shapes(W, H, buds), circles(W, H, heads)), 0.9, 1.0)
    art = G(art, shapes(W, H, buds), "#d0545a", "#a8323a", seed=nx(), density=0.95, edge=0.55, bloom=0.2, rough=0.8, gran=0.2)
    art = G(art, circles(W, H, heads), "#e7807a", "#c4545a", seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=0.6)
    return art


if "rempah" in PARTS:
    W, H = 820, 460
    nx = Seq(9100); rng = random.Random(91)
    art = blank(W, H)
    br = curve([(20, 350), (200, 318), (400, 270), (600, 220), (760, 150)], 60)
    art = G(art, strokes(W, H, [(br, 10, (0.0, 0.5))]), "#6b4a32", "#83603e", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=1.2, gran=0.3)
    twigs = [(curve([(330, 284), (344, 320), (350, 340)], 10), 5, (0.0, 0.4)), (curve([(520, 238), (512, 200), (500, 176)], 10), 4, (0, 0.4))]
    art = G(art, strokes(W, H, twigs), "#6b4a32", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1)
    for (x, y, L, Wd, a_, li) in [(90, 340, 170, 48, -2.6, False), (150, 330, 180, 50, 0.5, True), (250, 306, 190, 54, -1.15, False), (290, 300, 170, 48, 0.95, True),
                                   (430, 262, 190, 52, -2.1, True), (470, 252, 180, 50, 0.45, False), (610, 216, 180, 50, -1.4, True), (650, 200, 170, 46, 0.2, False),
                                   (720, 166, 150, 42, -0.7, True), (560, 232, 150, 42, 1.2, False), (380, 276, 150, 44, -0.5, False)]:
        art = paint_leaf(art, W, H, x, y, L, Wd, a_, rng, nx, li)
    clear()
    art = nutmeg(art, W, H, 352, 392, 58, rng, nx, split=True)
    art = nutmeg(art, W, H, 498, 150, 40, rng, nx, split=False)
    clear()
    art = cloves(art, W, H, 640, 206, 10, 1.5, 84, -2.0, rng, nx)
    art = cloves(art, W, H, 200, 316, 8, 1.3, 70, -1.5, rng, nx)
    preview(art, "rempah", tone="#f4ecdc")
    save(art, f"{OUT}/rempah.webp", max_w=600, quality=80)
    clear()

if "cengkih" in PARTS:
    W, H = 320, 320
    nx = Seq(9300); rng = random.Random(93)
    art = blank(W, H)
    art = G(art, strokes(W, H, [(curve([(160, 300), (162, 220), (160, 170)], 10), 4, (0, 0.3))]), "#6b4a32", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1)
    art = paint_leaf(art, W, H, 160, 250, 110, 30, -2.5, rng, nx, False)
    art = paint_leaf(art, W, H, 160, 240, 110, 30, -0.65, rng, nx, True)
    art = cloves(art, W, H, 160, 172, 9, 1.6, 96, -math.pi / 2, rng, nx)
    preview(art, "cengkih", tone="#f4ecdc")
    save(art, f"{OUT}/cengkih.webp", max_w=180, quality=82)
    clear()

if "bintang" in PARTS:
    W, H = 240, 240
    nx = Seq(9500); rng = random.Random(95)
    c0 = 120
    def star(r, inner, rot=0.0):
        pts = []
        for i in range(16):
            a = i * math.pi / 8 - math.pi / 2 + rot
            rr = r if i % 2 == 0 else r * inner
            pts.append((c0 + math.cos(a) * rr, c0 + math.sin(a) * rr))
        return pts
    outer = poly(W, H, star(104, 0.72), smooth=False)
    inner = poly(W, H, star(80, 0.72), smooth=False)
    ring = np.clip(outer - inner, 0, 1)
    sq1 = poly(W, H, [(c0, c0 - 66), (c0 + 66, c0), (c0, c0 + 66), (c0 - 66, c0)], smooth=False)
    sq2 = poly(W, H, [(c0 - 47, c0 - 47), (c0 + 47, c0 - 47), (c0 + 47, c0 + 47), (c0 - 47, c0 + 47)], smooth=False)
    lattice = np.clip(np.maximum(sq1, sq2) - poly(W, H, star(54, 0.78, math.pi / 8), smooth=False), 0, 1)
    art = blank(W, H)
    art = FO(art, ring, "#d4a64a", seed=nx(), emboss=0.7, sparkle=0.25)
    art = FO(art, lattice, "#c99a42", seed=nx(), emboss=0.7, sparkle=0.2)
    art = G(art, circles(W, H, [(c0, c0, 18)]), MACE, MACE_D, seed=nx(), density=0.95, edge=0.5, bloom=0.1, rough=0.6)
    art = FO(art, np.clip(circles(W, H, [(c0, c0, 22)]) - circles(W, H, [(c0, c0, 18)]), 0, 1), "#d4a64a", seed=nx())
    preview(art, "bintang", bg=NAVY)
    save(art, f"{OUT}/bintang.webp", max_w=120, quality=84)
    clear()


def kedaton(art, W, H, cx, by, s, nx, rng):
    """Kedaton Ternate (inspired): white two-storey palace, central block with a tiered hip roof and a broad stair,
    long wings with dark hip roofs, rows of shuttered windows, yellow trim."""
    yy, xx = ygrid(W, H)
    wing_w, wing_h = 220 * s, 64 * s
    cw, ch = 96 * s, 110 * s
    top_w = by - wing_h
    # wings
    wings = poly(W, H, [(cx - wing_w, by), (cx - wing_w, top_w), (cx + wing_w, top_w), (cx + wing_w, by)], smooth=False)
    art = GP(art, wings, "#f6f1e6", "#e8e0cf", seed=nx(), rough=0.8, streak=0.6)
    art = G(art, wings * np.clip((xx - cx) / (wing_w * 1.6), 0, 1), "#b9b2a8", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
    # wing roofs
    roof = poly(W, H, [(cx - wing_w - 12 * s, top_w + 2), (cx - wing_w + 30 * s, top_w - 34 * s), (cx + wing_w - 30 * s, top_w - 34 * s), (cx + wing_w + 12 * s, top_w + 2)], smooth=False)
    art = GP(art, roof, "#5a3a2e", "#6e4836", seed=nx(), rough=0.8)
    art = G(art, roof * np.clip((top_w - yy) / (34 * s), 0, 1), "#3a241c", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=1)
    eave = poly(W, H, [(cx - wing_w, top_w), (cx + wing_w, top_w), (cx + wing_w, top_w + 10 * s), (cx - wing_w, top_w + 7 * s)], smooth=False)
    art = G(art, eave, "#8a8478", seed=nx(), density=0.55, edge=0.1, bloom=0.2, rough=1)
    tiles = strokes(W, H, [([(cx + k * 9 * s, top_w - 32 * s), (cx + k * 9 * s * 1.08, top_w)], 0.9 * s, None) for k in range(-26, 27)]) * roof
    art = G(art, tiles, "#2a1812", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5)
    # windows (shutters) on wings
    wins = []
    for k in range(-5, 6):
        if abs(k) < 2:
            continue
        x = cx + k * 36 * s
        wins.append([(x - 8 * s, top_w + 16 * s), (x + 8 * s, top_w + 16 * s), (x + 8 * s, top_w + 44 * s), (x - 8 * s, top_w + 44 * s)])
    art = GP(art, shapes(W, H, wins, smooth=False), "#2f5a4a", "#3a6a54", seed=nx(), rough=0.4)
    # yellow trim line under the eaves and at plinth
    art = G(art, strokes(W, H, [([(cx - wing_w, top_w + 5 * s), (cx + wing_w, top_w + 5 * s)], 3 * s, None), ([(cx - wing_w, by - 6 * s), (cx + wing_w, by - 6 * s)], 4 * s, None)]), "#d9a93a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6)
    # central block, taller
    ctop = by - ch
    cb = poly(W, H, [(cx - cw, by), (cx - cw, ctop), (cx + cw, ctop), (cx + cw, by)], smooth=False)
    art = GP(art, cb, "#fbf7ee", "#efe8d8", seed=nx(), rough=0.7)
    art = G(art, cb * np.clip((xx - cx) / (cw * 2), 0, 1), "#bdb6aa", seed=nx(), density=0.3, edge=0.1, bloom=0.2, rough=2)
    art = G(art, poly(W, H, [(cx - cw, ctop), (cx + cw, ctop), (cx + cw, ctop + 10 * s), (cx - cw, ctop + 8 * s)], smooth=False), "#8a8478", seed=nx(), density=0.55, edge=0.1, bloom=0.2, rough=1)
    # tiered roof: two hip tiers + finial
    r1 = poly(W, H, [(cx - cw - 16 * s, ctop + 2), (cx - cw + 20 * s, ctop - 40 * s), (cx + cw - 20 * s, ctop - 40 * s), (cx + cw + 16 * s, ctop + 2)], smooth=False)
    r2 = poly(W, H, [(cx - cw * 0.55, ctop - 38 * s), (cx - cw * 0.25, ctop - 78 * s), (cx + cw * 0.25, ctop - 78 * s), (cx + cw * 0.55, ctop - 38 * s)], smooth=False)
    art = GP(art, r1, "#5a3a2e", "#6e4836", seed=nx(), rough=0.8)
    art = GP(art, r2, "#4e3226", "#62402f", seed=nx(), rough=0.6)
    art = G(art, strokes(W, H, [([(cx, ctop - 78 * s), (cx, ctop - 104 * s)], 3 * s, (0, 0.3))]), "#d9a93a", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.4)
    art = G(art, circles(W, H, [(cx, ctop - 106 * s, 4 * s)]), "#e6b84a", seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.3)
    # central doorway arch + upper windows
    door = poly(W, H, arc_pts(cx, by - 52 * s, 16 * s, math.pi, 2 * math.pi, 12) + [(cx + 16 * s, by - 20 * s), (cx - 16 * s, by - 20 * s)], smooth=False)
    art = GP(art, door, "#2f5a4a", "#244a3c", seed=nx(), rough=0.4)
    uw = [[(cx + k * 34 * s - 7 * s, ctop + 14 * s), (cx + k * 34 * s + 7 * s, ctop + 14 * s), (cx + k * 34 * s + 7 * s, ctop + 40 * s), (cx + k * 34 * s - 7 * s, ctop + 40 * s)] for k in (-2, -1, 0, 1, 2)]
    art = GP(art, shapes(W, H, uw, smooth=False), "#2f5a4a", "#3a6a54", seed=nx(), rough=0.4)
    art = G(art, strokes(W, H, [([(cx - cw, ctop + 6 * s), (cx + cw, ctop + 6 * s)], 3 * s, None), ([(cx - cw, ctop + 52 * s), (cx + cw, ctop + 52 * s)], 2.4 * s, None)]), "#d9a93a", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5)
    # broad front stair spilling down the hill
    st = poly(W, H, [(cx - 30 * s, by - 18 * s), (cx + 30 * s, by - 18 * s), (cx + 70 * s, by + 60 * s), (cx - 70 * s, by + 60 * s)], smooth=False)
    art = GP(art, st, "#efe9dc", "#d9d1c0", seed=nx(), rough=0.6)
    steps = [([(cx - 30 * s - k * 4 * s, by - 18 * s + k * 7.8 * s), (cx + 30 * s + k * 4 * s, by - 18 * s + k * 7.8 * s)], 1.2 * s, None) for k in range(1, 10)]
    art = G(art, strokes(W, H, steps) * st, "#9a9284", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    rails = strokes(W, H, [([(cx - 30 * s, by - 18 * s), (cx - 72 * s, by + 60 * s)], 5 * s, None), ([(cx + 30 * s, by - 18 * s), (cx + 72 * s, by + 60 * s)], 5 * s, None)])
    art = GP(art, rails, "#f8f4ea", "#e0d8c6", seed=nx(), rough=0.4)
    # stair shadow side + shrubs along the plinth
    art = G(art, st * np.clip((xx - cx) / (60 * s), 0, 1), "#a59d8c", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=1)
    sh = blobs(W, H, [(cx + d * s, by + 2 * s, 0.55) for d in list(range(-210, -80, 22)) + list(range(90, 220, 22))], rng, (10, 16), 4)
    art = G(art, sh, "#3f6a3a", "#55804a", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=1.5)
    fl = circles(W, H, [(cx + rng.uniform(-210, 210) * s, by + rng.uniform(-8, 8) * s, 2.2 * s) for _ in range(40)]) * (np.abs(xx - cx) > 80 * s)
    art = G(art, fl, "#c4404a", "#e07a3a", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.4)
    return art


if "gamalama" in PARTS:
    W, H = 760, 900
    nx = Seq(9700); rng = random.Random(97)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    hz = 470
    # morning sky: pale gold low, soft blue high
    sky = poly(W, H, [(0, 0), (W, 0), (W, hz + 4), (0, hz + 4)], smooth=False)
    art = G(art, sky, "#bcd3e3", "#f1dfba", seed=nx(), density=0.75, edge=0.0, bloom=0.15, rough=10, feather=8, mottle=0.2)
    cls = strokes(W, H, [(curve([(x, y), (x + L * 0.5, y - 4), (x + L, y)], 12), rng.uniform(6, 12), (0.3, 0.3)) for (x, y, L) in [(rng.uniform(-60, 700), rng.uniform(40, 330), rng.uniform(80, 220)) for _ in range(16)]])
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#fbf6ee"), gaussian_filter(cls, 3) * 0.7))
    art = G(art, sky * np.clip((yy - 200) / 260, 0, 1), "#f3d7a6", seed=nx(), density=0.45, edge=0.0, bloom=0.4, rough=8)
    # Gamalama: a broad cone out of the sea, summit slightly left, cloud collar
    peak = (330, 150)
    vol = poly(W, H, [(-40, hz + 4), (60, 420), (170, 300), (270, 190), (310, 158), (350, 152), (390, 168), (470, 240), (590, 350), (700, 420), (800, hz + 4)])
    art = G(art, vol, "#5c7a8a", "#6f8a86", seed=nx(), density=0.85, edge=0.45, bloom=0.35, rough=4, gran=0.3)
    # green lower slopes + forest/clove gardens texture
    slope = vol * np.clip((yy - 250) / 160, 0, 1)
    art = G(art, slope, "#56794a", "#6f8a52", seed=nx(), density=0.75, edge=0.2, bloom=0.4, rough=4, gran=0.3)
    gul = strokes(W, H, [([(peak[0] + dx * 0.2, 170), (peak[0] + dx, 300 + abs(dx) * 0.2)], rng.uniform(1.5, 3), (0.1, 0.6)) for dx in np.linspace(-200, 240, 26)])
    art = G(art, gul * vol, "#3e5560", seed=nx(), density=0.35, edge=0.1, bloom=0.1, rough=1.5)
    trees = blobs(W, H, [(rng.uniform(40, 720), rng.uniform(360, hz), rng.uniform(0.3, 0.6)) for _ in range(70)], rng, (8, 14), 3) * vol
    art = G(art, trees, "#3c5e38", "#4f7040", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=2)
    # dark summit + thin smoke plume
    summit = vol * np.clip((230 - yy) / 70, 0, 1)
    art = G(art, summit, "#4a4a52", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=3)
    plume = poly(W, H, deform([(318, 152), (300, 110), (330, 60), (410, 40), (470, 60), (420, 80), (370, 100), (352, 150)], rng, 2, 0.08))
    art = G(art, plume, "#c9c4c0", "#a9a4a2", seed=nx(), density=0.6, edge=0.3, bloom=0.6, rough=6)
    collar = poly(W, H, deform(ellipse_pts(300, 262, 150, 16, 16, -0.05), rng, 2, 0.1))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f8f4ee"), gaussian_filter(collar, 5) * 0.8))
    art = G(art, collar, "#ffffff", "#f1ece6", seed=nx(), density=0.0, edge=0.2, bloom=0.6, rough=8)
    clear()
    # Halmahera sea: deep blue band with long light strokes, a far island (Tidore-like cone) on the right horizon
    isl = poly(W, H, [(600, hz + 2), (660, hz - 40), (690, hz - 52), (720, hz - 40), (790, hz + 2)])
    art = G(art, isl * (xx > 0), "#7d95a8", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=3)
    sea = poly(W, H, [(0, hz), (W, hz), (W, 690), (0, 690)], smooth=False)
    art = G(art, sea, SEA, NAVY, seed=nx(), density=0.9, edge=0.2, bloom=0.3, rough=5)
    art = G(art, sea * np.clip((yy - hz) / 160, 0, 1), "#2a74a8", seed=nx(), density=0.45, edge=0.0, bloom=0.4, rough=5)
    rip = sea_strokes(W, H, hz + 4, 690, rng, n=200, length=(18, 70), width=(0.7, 2.0))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#d6e8f2"), rip * sea * 0.5))
    # coastline town (white specks + roofs) at the foot of the volcano
    town = []
    for _ in range(46):
        x = rng.uniform(40, 720); y = hz - rng.uniform(3, 30) * rng.random()
        w_, h_ = rng.uniform(3, 7), rng.uniform(2.5, 4)
        town.append([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)])
    art = GP(art, shapes(W, H, town, smooth=False) * vol, "#f2ece0", "#d8cfbe", seed=nx(), rough=0.3)
    # a small kora-kora boat on the water
    hull = poly(W, H, [(140, 560), (230, 560), (238, 552), (222, 572), (148, 572), (132, 552)])
    art = GP(art, hull, "#7a3a24", "#934a2e", seed=nx(), rough=0.4)
    art = G(art, strokes(W, H, [([(150 + k * 9, 556), (146 + k * 9, 574)], 1.0, None) for k in range(9)]), "#e9d39a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4)
    # foreground hill with lawn
    hill = poly(W, H, [(-20, 900), (-20, 700), (120, 660), (300, 640), (460, 640), (640, 660), (780, 700), (780, 900)])
    art = G(art, hill, "#7a9a52", "#8faa5c", seed=nx(), density=0.92, edge=0.5, bloom=0.4, rough=4, gran=0.3)
    art = G(art, hill * np.clip((yy - 700) / 160, 0, 1), "#4f7040", seed=nx(), density=0.6, edge=0.1, bloom=0.3, rough=4)
    mow = strokes(W, H, [(curve([(-20, y), (380, y - 14), (780, y)], 20), 10, None) for y in range(730, 900, 26)]) * hill
    art = G(art, mow, "#5e8048", seed=nx(), density=0.25, edge=0.1, bloom=0.2, rough=3)
    path = poly(W, H, [(340, 776), (420, 776), (470, 900), (290, 900)], smooth=False)
    art = G(art, path, "#e6dcc4", "#d8cbac", seed=nx(), density=0.85, edge=0.4, bloom=0.3, rough=2, gran=0.4)
    # the palace
    art = kedaton(art, W, H, 380, 712, 1.08, nx, rng)
    clear()
    # flanking palms and a flag mast
    for (x, by, h, ln) in [(60, 820, 300, 0.06), (700, 830, 280, -0.07)]:
        tr = strokes(W, H, [(curve([(x, by), (x + ln * h * 0.6, by - h * 0.5), (x + ln * h, by - h)], 20), 7, (0.0, 0.3))])
        art = G(art, tr, "#7a6a54", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1.2)
        fr = []
        tx, ty = x + ln * h, by - h
        for k in range(9):
            a = -math.pi + k * math.pi / 8 + rng.uniform(-0.1, 0.1)
            L = rng.uniform(70, 100)
            pts = curve([(tx, ty), (tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.5 - 10), (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.4 + 30)], 16)
            fr.append((pts, 9, (0.0, 0.7)))
        art = G(art, strokes(W, H, fr), "#3e6a3a", "#5c8448", seed=nx(), density=0.88, edge=0.4, bloom=0.3, rough=1.5)
    art[..., 3] *= vignette_mask(W, H, 23, inset=2, rough=18, fade=30)
    preview(art, "gamalama", tone="#f4ecdc")
    save(art, f"{OUT}/gamalama.webp", max_w=540, quality=56)
    clear()
