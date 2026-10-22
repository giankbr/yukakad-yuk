"""Pandai Sikek — Minang: Pandai Sikek songket with dense supplementary gold weft (thread level), Ngarai Sianok canyon in
watercolour (sheer ochre cliff walls, green valley, river, Singgalang behind), and carved Minang ukiran: kaluak paku
fern-frond spirals in gilt relief on a red ground, framed by black borders of itiak pulang patang hooks (abstract,
geometric). Run: python3 -I minang-pandai-sikek.py [part ...]   parts: songket ukiran kaluak ngarai"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e1_lib import *
from _jw_lib import carve, spiral_pts, hills as jw_hills

OUT = outdir("minang-pandai-sikek")
PARTS = sys.argv[1:] or ["songket", "ukiran", "kaluak", "ngarai"]
RED, RED_D, RED_L = "#9a1f1c", "#5e0f10", "#c0382a"
BLACK, BLACK_L = "#1c1412", "#3a2a24"
GILT = "#d6a83e"


def songket_tile(N=96):
    """Dense Pandai Sikek gold: the gold weft covers most of the cloth; the red ground only draws the motif outlines
    (diamond lattice of balah kacang with an eight-point bintang in each, small stars between)."""
    yy, xx = np.mgrid[0:N, 0:N]
    c = 24
    u = (xx % (2 * c)) - c + 0.5; v = (yy % (2 * c)) - c + 0.5
    u2 = ((xx + c) % (2 * c)) - c + 0.5; v2 = ((yy + c) % (2 * c)) - c + 0.5
    d = np.abs(u) + np.abs(v)
    d2 = np.abs(u2) + np.abs(v2)
    ground = ((d >= 9) & (d < 10.6)) | ((d >= 14) & (d < 15.6)) | ((d >= 19.5) & (d < 21))
    star = ((np.abs(u) < 1.2) | (np.abs(v) < 1.2) | (np.abs(np.abs(u) - np.abs(v)) < 1.0)) & (d < 7) & (d > 2)
    ground |= star
    ground |= (d2 < 5) & ((np.abs(u2) < 1) | (np.abs(v2) < 1)) & (d2 > 1.4)
    ground |= (np.abs(d2 - 7) < 0.7)
    gold = ~ground
    # every 8th pick a red binding line shows across (horizontal rhythm of the hand loom)
    gold &= ~((yy % 16) == 0)
    return gold.astype(np.float32)


if "songket" in PARTS:
    N = 96
    D = np.zeros((N, N), np.int32)
    D[:, :] = 0
    # ground: deep red with fine darker warp stripes
    for k in range(0, N, 12):
        D[:, k:k + 1] = 1
    ground = ikat(D, [RED_D, "#4a0a0e"], p=4, mode="warp", ground=RED_D, face=0.5, amp=0.2, coh=1, along=4, seed=41, bleed=0.2, slub=0.15, fibre=0.06, thread_var=0.04)
    gm = songket_tile(N)
    cloth = songket(ground, gm, p=4, base="#e3b955", deep="#7a5418", seed=43, float_len=4)
    prev_rgb(tile_to(cloth, 768, 768), "songket")
    save_rgb_arr(cloth, f"{OUT}/songket.webp", quality=74)
    clear()


def kaluak(cx, cy, s, flip=1, rot=0.0):
    """Kaluak paku: a fern fiddlehead — a stem rising into a big inward spiral with small back-curls budding off
    its outer edge. Returns stroke items (all lines, carved as relief)."""
    ca, sa = math.cos(rot), math.sin(rot)
    def T(x, y):
        x *= flip
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    items = []
    # stem from bottom-left sweeping up into the spiral centre region
    stem = curve([T(-0.9, 0.85), T(-0.55, 0.55), T(-0.35, 0.05), T(-0.05, -0.4)], 30)
    items.append((stem, s * 0.12, (0.1, 0.0)))
    # main spiral (in local units, centred at (0.15,-0.05))
    sp = spiral_pts(0, 0, 0.62, 0.06, math.pi * 1.05, 1.3, 70, 1)
    sp = [T(0.15 + x, -0.05 + y) for x, y in sp]
    items.append((sp, s * 0.11, (0.0, 0.5)))
    # back-curls: small spirals on the outside of the frond
    for (bx, by, r, a0, d) in [(-0.45, -0.55, 0.2, 0.0, -1), (0.2, -0.85, 0.18, 1.2, -1), (0.85, -0.45, 0.16, 2.6, -1), (-0.75, 0.25, 0.17, -1.2, -1)]:
        cs = spiral_pts(0, 0, r, 0.03, a0, 1.1, 30, d)
        items.append(([T(bx + x, by + y) for x, y in cs], s * 0.07, (0.0, 0.6)))
    return [([(px * s if False else px, py) for px, py in pts], w, tp) for pts, w, tp in [(_scale(p, cx, cy, s), w, tp) for p, w, tp in items]]


def _scale(pts, cx, cy, s):
    return [(cx + (x - cx) * s, cy + (y - cy) * s) for x, y in pts]


def hooks_row(x0, x1, y, h, step):
    """Itiak pulang patang (abstracted): a procession of leaning hook strokes, purely geometric."""
    items = []
    x = x0
    while x < x1:
        pts = curve([(x, y + h * 0.45), (x + step * 0.25, y + h * 0.1), (x + step * 0.55, y - h * 0.15), (x + step * 0.7, y - h * 0.4), (x + step * 0.55, y - h * 0.5)], 14)
        items.append((pts, h * 0.18, (0.0, 0.3)))
        x += step
    return items


if "ukiran" in PARTS:
    W, H = 960, 240
    nx = Seq(13100); rng = random.Random(131)
    art = blank(W, H)
    top_b = poly(W, H, [(0, 0), (W, 0), (W, 46), (0, 46)], smooth=False)
    bot_b = poly(W, H, [(0, H - 46), (W, H - 46), (W, H), (0, H)], smooth=False)
    mid = poly(W, H, [(0, 50), (W, 50), (W, H - 50), (0, H - 50)], smooth=False)
    # middle red panel: mirrored pairs of kaluak paku
    items = []
    for k in range(6):
        cx = 80 + k * 160
        items += kaluak(cx - 40, 126, 50, flip=1)
        items += kaluak(cx + 40, 126, 50, flip=-1)
        # small diamond between pairs
    leaves = [[(160 * k, 120 - 12), (160 * k + 10, 120), (160 * k, 132), (160 * k - 10, 120)] for k in range(0, 7)]
    art = over(art, carve(W, H, mid, items, leaves, nx, base=RED, light=RED_L, dark=RED_D, gold=GILT, gold_amt=0.92, seed=17))
    clear()
    # black borders with gilt hook processions (one row walks right, the other walks left)
    for band, y, flipx in ((top_b, 26, False), (bot_b, H - 22, True)):
        it = hooks_row(-10, W + 20, y, 30, 34)
        if flipx:
            it = [([(W - px, py) for px, py in pts], w, tp) for pts, w, tp in it]
        art = over(art, carve(W, H, band, it, [], nx, base=BLACK, light=BLACK_L, dark="#0a0606", gold=GILT, gold_amt=0.85, seed=19))
        clear()
    # thin gilt fillets between bands
    fil = strokes(W, H, [([(0, 48), (W, 48)], 3, None), ([(0, H - 48), (W, H - 48)], 3, None)])
    art = FO(art, fil, GILT, seed=nx(), emboss=0.5, sparkle=0.1)
    preview(art, "ukiran", tone="#f3ead8")
    save(art, f"{OUT}/ukiran.webp", max_w=720, quality=78)
    clear()

if "kaluak" in PARTS:
    W, H = 300, 300
    nx = Seq(13500); rng = random.Random(135)
    art = blank(W, H)
    sq = poly(W, H, [(150, 8), (292, 150), (150, 292), (8, 150)], smooth=False)
    inner = poly(W, H, [(150, 30), (270, 150), (150, 270), (30, 150)], smooth=False)
    rim = np.clip(sq - inner, 0, 1)
    art = over(art, carve(W, H, rim, hooks_row(0, 300, 150, 0, 300)[:0], [], nx, base=BLACK, light=BLACK_L, dark="#0a0606", gold=GILT, gold_amt=0.0, seed=21))
    items = []
    for k in range(4):
        a = k * math.pi / 2
        items += kaluak(150 + 36 * math.cos(a - 0.6), 150 + 36 * math.sin(a - 0.6), 34, flip=1, rot=a)
    leaves = [[(150, 138), (162, 150), (150, 162), (138, 150)]]
    art = over(art, carve(W, H, inner, items, leaves, nx, base=RED, light=RED_L, dark=RED_D, gold=GILT, gold_amt=0.92, seed=23))
    rimline = np.clip(poly(W, H, [(150, 22), (278, 150), (150, 278), (22, 150)], smooth=False) - poly(W, H, [(150, 27), (273, 150), (150, 273), (27, 150)], smooth=False), 0, 1)
    art = FO(art, rimline, GILT, seed=nx(), emboss=0.5, sparkle=0.1)
    preview(art, "kaluak", tone="#f3ead8")
    save(art, f"{OUT}/kaluak.webp", max_w=150, quality=82)
    clear()

if "ngarai" in PARTS:
    W, H = 900, 600
    nx = Seq(14100); rng = random.Random(141)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    sky = poly(W, H, [(0, 0), (W, 0), (W, 320), (0, 320)], smooth=False)
    art = G(art, sky * np.clip((330 - yy) / 320, 0, 1) ** 0.5, "#cfe0e2", "#f1eedc", seed=nx(), density=0.6, edge=0.0, bloom=0.4, rough=10, feather=8)
    # Singgalang behind, blue-violet, cloud collar
    mt = poly(W, H, [(-20, 280), (150, 230), (300, 140), (380, 112), (450, 128), (600, 210), (720, 220), (800, 200), (920, 240), (920, 320), (-20, 320)])
    art = G(art, mt, "#8ea0b8", "#a4b0c4", seed=nx(), density=0.75, edge=0.45, bloom=0.4, rough=4)
    art = G(art, mt * np.clip((yy - 170) / 140, 0, 1), "#7f9a9a", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=4)
    cl = poly(W, H, deform(ellipse_pts(390, 170, 170, 14, 14), rng, 2, 0.1))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#ffffff"), gaussian_filter(cl, 6) * 0.75))
    # distant plateau + far canyon walls (aerial perspective: cool and pale)
    far = poly(W, H, [(-20, 300), (300, 296), (600, 292), (920, 300), (920, 372), (-20, 372)], smooth=False)
    art = G(art, far, "#c9b9a0", "#bfb8a6", seed=nx(), density=0.8, edge=0.3, bloom=0.3, rough=2, gran=0.3)
    art = G(art, far * np.clip((312 - yy) / 14, 0, 1), "#7f9a66", seed=nx(), density=0.85, edge=0.2, bloom=0.3, rough=2)
    fs = strokes(W, H, [([(x, 312), (x + rng.uniform(-2, 2), 312 + rng.uniform(20, 56))], rng.uniform(0.8, 2), (0.2, 0.5)) for x in np.linspace(300, 620, 60)])
    art = G(art, fs * far, "#8f7a64", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    clear()
    # valley floor between the walls: paddies + river
    floor = poly(W, H, [(280, 340), (640, 340), (920, 540), (920, 620), (-20, 620), (-20, 540)], smooth=False)
    floor = floor * (yy > 340)
    art = G(art, floor, "#8fb05a", "#a6bf62", seed=nx(), density=0.92, edge=0.3, bloom=0.4, rough=3, gran=0.3)
    terr = strokes(W, H, [(curve([(0, y), (450, y + 8 * (1 if (y // 20) % 2 else -1)), (900, y)], 16), 1.2 + (y - 340) / 150, None) for y in range(352, 610, 18)]) * floor
    art = G(art, terr, "#5f8a3c", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8)
    river = strokes(W, H, [(curve([(452, 345), (440, 380), (470, 420), (430, 480), (480, 540), (440, 610)], 50), 10, (0.6, 0.0))])
    art = G(art, river * (yy > 342), "#9cc6cf", "#c2ddd8", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=2)
    # near cliff walls: flat green plateau tops, sheer vertical faces with gullies and strata
    walls = [([(-20, 256), (160, 266), (300, 288), (336, 300), (352, 336), (330, 392), (300, 450), (276, 520), (-20, 560)], 318, 1),
             ([(920, 246), (740, 258), (600, 286), (566, 300), (574, 344), (598, 410), (622, 470), (650, 530), (920, 560)], 585, -1)]
    for pts, edge_x, side in walls:
        m = poly(W, H, deform(pts, rng, 2, 0.02), smooth=True)
        lit = side > 0
        art = GP(art, m, "#e6c696" if lit else "#d0aa80", "#ecd3a6" if lit else "#d8b48a", seed=nx(), rough=1.2, streak=0.6)
        art = G(art, m, "#d6aa72" if lit else "#b98a5e", "#e2bd86" if lit else "#c69a6a", seed=nx(), density=0.7, edge=0.5, bloom=0.35, rough=2, gran=0.45)
        # the face (near the valley edge) vs. plateau body: darken the far body slightly
        art = G(art, m * np.clip((yy - 300) / 240, 0, 1), "#7e5434" if lit else "#5e3e2a", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=3)
        xs = [p[0] for p in pts]
        gl = []
        for _ in range(110):
            x = rng.uniform(min(xs), max(xs))
            y0 = rng.uniform(290, 380)
            gl.append(([(x, y0), (x + rng.uniform(-3, 3), y0 + rng.uniform(50, 200))], rng.uniform(1.0, 3.0), (0.2, 0.5)))
        art = G(art, strokes(W, H, gl) * m, "#6e4a2e", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1, gran=0.4)
        strata = strokes(W, H, [(curve([(min(xs), y), (max(xs), y + rng.uniform(-6, 6))], 12), rng.uniform(1, 2.2), (0.3, 0.3)) for y in range(320, 520, 26)])
        art = G(art, strata * m, "#9a6a40", seed=nx(), density=0.3, edge=0, bloom=0, rough=1)
        cap = m * np.clip((300 - yy) / 26 + 0.4, 0, 1)
        art = G(art, cap, "#4f7a3c", "#6a8f46", seed=nx(), density=0.9, edge=0.45, bloom=0.35, rough=3)
        veg = m * np.clip((fbm(W, H, nx(), 34, 4) - 0.5) * 3, 0, 1) * (yy > 300)
        art = G(art, veg, "#4a7038", "#5f8642", seed=nx(), density=0.75, edge=0.45, bloom=0.3, rough=2)
        # sunlit rim along the valley edge of the face, shadow under the plateau lip
        ex = np.array([p[0] for p in pts[2:7]]); ey = np.array([p[1] for p in pts[2:7]])
        edge_line = strokes(W, H, [(list(zip(ex, ey)), 14, None)]) * m
        art = G(art, edge_line, "#f2cf98" if lit else "#d9a878", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=2)
        lip = m * np.clip(1 - np.abs(yy - 312) / 14, 0, 1)
        art = G(art, lip, "#5a3a24", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=2)
        talus = blobs(W, H, [(x, 0, 0) for x in []], rng)
        base_pts = [(pts[-2][0] * (1 - t) + (pts[-1][0] if side > 0 else 920) * t, pts[-2][1] + (40 * t)) for t in np.linspace(0, 1, 10)]
        tb = blobs(W, H, [(x + rng.uniform(-10, 10), y - rng.uniform(0, 12), rng.uniform(0.6, 1.0)) for x, y in base_pts], rng, (12, 22), 4)
        art = G(art, tb, "#36603a", "#4a7040", seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=2)
        clear()
    mist = poly(W, H, deform([(250, 360), (650, 352), (660, 380), (240, 392)], rng, 2, 0.1))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f6f3ea"), gaussian_filter(mist, 10) * 0.55))
    # foreground trees framing the bottom corners
    fg = blobs(W, H, [(rng.uniform(-20, 200), rng.uniform(530, 610), rng.uniform(0.8, 1.4)) for _ in range(12)] + [(rng.uniform(720, 920), rng.uniform(530, 610), rng.uniform(0.8, 1.4)) for _ in range(12)], rng, (16, 30), 4)
    art = G(art, fg, "#2f5a30", "#46703a", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=3)
    art[..., 3] *= vignette_mask(W, H, 29, inset=2, rough=22, fade=36)
    art[..., 3] *= np.clip((yy - 8 + (fbm(W, H, 5, 50, 3) - 0.5) * 60) / 110, 0, 1)
    preview(art, "ngarai", tone="#f3ead8")
    save(art, f"{OUT}/ngarai.webp", max_w=720, quality=60)
    clear()
