"""Poster Wisata — vintage lithograph travel poster of an original Indonesian coast: stepped sky bands, a smoking
volcano, a two-funnel steamship, an outrigger sail, palm silhouettes; plus a steam train on a viaduct over rice
terraces. Flat stone-litho inks with grain and slight misregistration. Run: python3 -I poster-wisata.py [part ...]
parts: poster train waves palm. Assets -> public/themes/art/poster-wisata/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h6_lib import *

OUT = outdir("poster-wisata")
PARTS = sys.argv[1:] or ["poster", "train", "waves", "palm"]
CREAM = "#f6e7c8"
TEAL_D, TEAL, TEAL_L = "#1d4f5c", "#2f7480", "#5fa3a3"
GOLD, ORANGE, CORAL = "#f3c46e", "#ee8a4a", "#d4573a"
VIOLET, VIOLET_L, VIOLET_D = "#7a5a86", "#a3809e", "#4f3a5e"
JUNGLE, JUNGLE_D = "#2e5d45", "#1b3a2e"
NAVY = "#1c2a3e"
SAND = "#e9b979"


def wavy(W, y, amp, seed, wl=180):
    rng = random.Random(seed); ph = rng.uniform(0, 6)
    return lambda x: y + amp * math.sin(x / wl * math.tau + ph) + amp * 0.4 * math.sin(x / (wl * 0.37) + ph * 1.7)


def band(W, H, top_fn, bot):
    return shapes(W, H, [band_poly(W, top_fn, bot)], smooth=False)


def finish(art, seed, paper_tone="#f3e6c9", amount=0.07):
    """Print finish: paper grain multiplied through, faint mottling."""
    h, w = art.shape[:2]
    pap = np.asarray(paper(w, h, paper_tone, seed), np.float32) / 255
    pap = pap / pap.mean(axis=(0, 1))
    out = art.copy()
    out[..., :3] = np.clip(out[..., :3] * (1 - amount + amount * pap), 0, 1)
    return add_grain(out, seed + 1, 0.03)


def palm_sil(W, H, x, by, h, rng, lean=0.12, fronds=9):
    """Strong poster palm silhouette: tapered curved trunk + arching fronds made of many tapered leaflets."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.15, by - h * 0.5), top], 30)
    items = [(trunk, h * 0.04, (0.0, 0.7))]
    for k in range(fronds):
        a = -math.pi / 2 + (k - (fronds - 1) / 2) * (3.3 / fronds) + rng.uniform(-0.08, 0.08)
        L = h * rng.uniform(0.36, 0.48)
        side = math.cos(a)
        tip = (top[0] + side * L, top[1] + math.sin(a) * L * 0.5 + L * (0.35 + 0.3 * abs(side)))
        mid = (top[0] + side * L * 0.55, top[1] + math.sin(a) * L * 0.75 - L * 0.05)
        spine = curve([top, mid, tip], 30)
        items.append((spine, h * 0.012, (0.0, 0.6)))
        n = len(spine)
        for i in range(2, n - 1):
            t = i / (n - 1)
            px, py = spine[i]
            dx, dy = spine[i + 1][0] - spine[i - 1][0], spine[i + 1][1] - spine[i - 1][1]
            d = math.hypot(dx, dy) or 1
            ux, uy = dx / d, dy / d
            ll = L * 0.24 * math.sin(math.pi * min(1, t * 1.05)) ** 0.7
            for sgn in (-1, 1):
                nxn, nyn = -uy * sgn, ux * sgn
                ex = px + (nxn * 0.8 + ux * 0.55) * ll; ey = py + (nyn * 0.8 + uy * 0.55) * ll + ll * 0.35
                items.append(([(px, py), ((px + ex) / 2, (py + ey) / 2 + ll * 0.06), (ex, ey)], h * 0.011, (0.0, 0.8)))
    m = strokes(W, H, items)
    nuts = circles(W, H, [(top[0] + rng.uniform(-8, 8) * h / 300, top[1] + rng.uniform(4, 12) * h / 300, h * 0.022) for _ in range(4)])
    return m, nuts, trunk


if "poster" in PARTS:
    W, H = 720, 960
    nx = Seq(71000); rng = random.Random(71)
    art = solid(W, H, TEAL_D)
    # stepped sky bands (top -> horizon)
    bands = [(0, "#1f5866"), (120, "#2b6f7b"), (220, "#4f938f"), (300, "#9fbf9c"), (360, "#f3d7a0"), (410, GOLD), (452, "#f2a75e")]
    for i, (y, col) in enumerate(bands):
        art = LI(art, band(W, H, wavy(W, y, 5 if i else 0, 700 + i, 260), 560), col, seed=nx(), grain=0.6)
    clear()
    # sun disc with halo rings
    art = LI(art, circles(W, H, [(470, 400, 118)]), "#f9e2ad", seed=nx(), grain=0.4)
    art = LI(art, circles(W, H, [(470, 400, 92)]), "#fbecc7", seed=nx(), grain=0.3)
    # birds
    birds = []
    for bx, by_, s in [(140, 170, 1.0), (176, 150, 0.8), (205, 186, 0.7), (600, 120, 0.9)]:
        birds.append((curve([(bx - 12 * s, by_), (bx - 5 * s, by_ - 6 * s), (bx, by_)], 8), 2.6 * s, None))
        birds.append((curve([(bx, by_), (bx + 5 * s, by_ - 6 * s), (bx + 12 * s, by_)], 8), 2.6 * s, None))
    art = LI(art, strokes(W, H, birds), NAVY, seed=nx(), grain=0.2)
    # far island ridge (cool violet)
    art = LI(art, band(W, H, wavy(W, 470, 10, 33, 140), 560), "#9c8aa6", seed=nx())
    # volcano: shadow side + lit side + crater plume
    cone = [(60, 520), (210, 380), (300, 286), (340, 262), (372, 262), (420, 300), (520, 410), (690, 520)]
    art = LI(art, shapes(W, H, [cone + [(690, 560), (60, 560)]], smooth=False), VIOLET, seed=nx())
    lit = [(356, 264), (372, 262), (420, 300), (520, 410), (690, 520), (690, 560), (470, 560), (420, 440), (390, 340)]
    art = LI(art, shapes(W, H, [lit], smooth=False), VIOLET_L, seed=nx())
    gul = []
    for gx in [250, 300, 340, 380, 430, 490]:
        gul.append([(gx, 520), (gx + (356 - gx) * 0.55 + rng.uniform(-6, 6), 330 + abs(gx - 356) * 0.4), (gx + 8, 520)])
    art = LI(art, shapes(W, H, gul, smooth=False), VIOLET_D, seed=nx(), grain=0.5)
    plume = [deform(ellipse_pts(x, y, r, r * 0.7, 10), rng, 2, 0.06) for x, y, r in
             [(352, 236, 22), (338, 206, 28), (360, 176, 34), (330, 146, 36), (300, 122, 30), (262, 108, 26), (226, 100, 20)]]
    art = LI(art, shapes(W, H, plume), "#efe1c6", seed=nx(), grain=0.4)
    art = LI(art, shapes(W, H, [deform(ellipse_pts(x + 6, y + 8, r * 0.6, r * 0.35, 10), rng, 1, 0.05) for x, y, r in [(352, 236, 22), (338, 206, 28), (360, 176, 34), (330, 146, 36)]]), "#d9c3ad", seed=nx(), grain=0.3)
    # jungle foothills
    art = LI(art, band(W, H, wavy(W, 512, 12, 44, 120), 580), "#4b7a5b", seed=nx())
    clear()
    # sea with ripple dashes + sun glitter
    sea = shapes(W, H, [rect(-10, 548, W + 20, 420)], smooth=False)
    art = LI(art, sea, TEAL, seed=nx(), grain=0.5)
    art = LI(art, shapes(W, H, [rect(-10, 640, W + 20, 330)], smooth=False), TEAL_D, seed=nx(), grain=0.5)
    rip = []
    for _ in range(120):
        y = rng.uniform(556, 860); x = rng.uniform(-10, W)
        L = rng.uniform(10, 40) * (0.6 + (y - 550) / 300)
        rip.append(([(x, y), (x + L, y)], rng.uniform(2.4, 3.6), None))
    art = LI(art, strokes(W, H, rip), TEAL_L, seed=nx(), grain=0.3)
    glit = []
    for i in range(26):
        y = 556 + i * 9 + rng.uniform(-2, 2); wdt = 50 - i * 1.2 + rng.uniform(-10, 10)
        glit.append(([(470 - wdt + rng.uniform(-8, 8), y), (470 + wdt + rng.uniform(-8, 8), y)], rng.uniform(3, 4.5), None))
    art = LI(art, strokes(W, H, glit), "#f7cf86", seed=nx(), grain=0.3)
    clear()
    # steamship (right, sailing left)
    sx, sy = 330, 640
    hull = [(sx, sy), (sx + 250, sy), (sx + 268, sy - 34), (sx + 6, sy - 34), (sx - 26, sy - 46)]
    art = LI(art, shapes(W, H, [hull], smooth=False), NAVY, seed=nx())
    art = LI(art, shapes(W, H, [[(sx + 2, sy - 2), (sx + 250, sy - 2), (sx + 254, sy - 12), (sx - 2, sy - 12)]], smooth=False), CORAL, seed=nx())
    sup = [rect(sx + 40, sy - 62, 180, 28), rect(sx + 70, sy - 84, 120, 22), rect(sx + 96, sy - 100, 50, 16)]
    art = LI(art, shapes(W, H, sup, smooth=False), "#f6ead2", seed=nx(), grain=0.3)
    port = circles(W, H, [(sx + 52 + k * 15, sy - 48, 3) for k in range(11)] + [(sx + 82 + k * 14, sy - 73, 2.6) for k in range(7)])
    art = LI(art, port, NAVY, seed=nx(), grain=0.2)
    for fx in (sx + 108, sx + 162):
        art = LI(art, shapes(W, H, [[(fx, sy - 84), (fx + 26, sy - 84), (fx + 30, sy - 150), (fx + 4, sy - 150)]], smooth=False), CORAL, seed=nx())
        art = LI(art, shapes(W, H, [[(fx + 3, sy - 136), (fx + 29, sy - 136), (fx + 30, sy - 150), (fx + 4, sy - 150)]], smooth=False), NAVY, seed=nx())
        art = LI(art, shapes(W, H, [[(fx + 1, sy - 104), (fx + 27, sy - 104), (fx + 28, sy - 114), (fx + 2, sy - 114)]], smooth=False), "#f6ead2", seed=nx())
    smoke = [deform(ellipse_pts(sx + 150 + k * 36, sy - 168 - k * 8 + rng.uniform(-4, 4), 16 + k * 4, 11 + k * 2.4, 10), rng, 2, 0.06) for k in range(6)]
    art = LI(art, shapes(W, H, smoke), "#e7dccb", seed=nx(), grain=0.5)
    masts = strokes(W, H, [([(sx + 30, sy - 40), (sx + 30, sy - 140)], 3, None), ([(sx + 236, sy - 40), (sx + 236, sy - 128)], 3, None),
                           ([(sx + 30, sy - 138), (sx + 120, sy - 152), (sx + 236, sy - 126)], 1.4, None)])
    art = LI(art, masts, NAVY, seed=nx(), grain=0.2)
    wake = strokes(W, H, [([(sx - 30 + k * 40, sy + 6 + k % 2 * 4), (sx + 10 + k * 40, sy + 6 + k % 2 * 4)], 3, (0.3, 0.3)) for k in range(8)])
    wake = strokes(W, H, [([(sx - 30 + k * 40, sy + 6 + k % 2 * 4), (sx + 10 + k * 40, sy + 6 + k % 2 * 4)], 3.5, None) for k in range(8)])
    art = LI(art, wake, "#f6ead2", seed=nx(), grain=0.3)
    # outrigger sail boat (left)
    bx, by_ = 150, 712
    art = LI(art, shapes(W, H, [[(bx - 54, by_ - 8), (bx + 58, by_ - 8), (bx + 40, by_ + 6), (bx - 40, by_ + 6)]], smooth=False), "#7a3b24", seed=nx())
    art = LI(art, shapes(W, H, [[(bx - 4, by_ - 12), (bx - 4, by_ - 118), (bx + 64, by_ - 22)]], smooth=False), ORANGE, seed=nx())
    art = LI(art, shapes(W, H, [[(bx - 8, by_ - 12), (bx - 8, by_ - 96), (bx - 52, by_ - 18)]], smooth=False), "#f2c56e", seed=nx())
    art = LI(art, strokes(W, H, [([(bx - 70, by_ + 14), (bx + 70, by_ + 14)], 3, None), ([(bx - 30, by_ + 2), (bx - 40, by_ + 14)], 2, None), ([(bx + 30, by_ + 2), (bx + 40, by_ + 14)], 2, None)]), NAVY, seed=nx(), grain=0.2)
    clear()
    # foreground: beach + framing palms (left big, right small) + flowering shrub
    beach = band(W, H, lambda x: 856 - 40 * math.exp(-((x - 120) / 260) ** 2) + 6 * math.sin(x / 40), 980)
    art = LI(art, beach, SAND, seed=nx())
    art = LI(art, band(W, H, lambda x: 884 - 30 * math.exp(-((x - 120) / 260) ** 2) + 4 * math.sin(x / 26), 980), "#d8a465", seed=nx())
    foam = strokes(W, H, [(curve([(x, 856 - 40 * math.exp(-((x - 120) / 260) ** 2) + 6 * math.sin(x / 40) - 3) for x in range(-10, W + 10, 20)], 60), 4, None)])
    art = LI(art, foam, "#f8efda", seed=nx(), grain=0.3)
    m, nuts, _ = palm_sil(W, H, 30, 940, 800, rng, lean=0.12, fronds=10)
    art = LI(art, m, JUNGLE_D, seed=nx(), grain=0.4)
    art = LI(art, nuts, "#6a4a2a", seed=nx())
    m2, nuts2, _ = palm_sil(W, H, 716, 930, 400, rng, lean=-0.08, fronds=8)
    art = LI(art, m2, JUNGLE, seed=nx(), grain=0.4)
    shrub = [deform(ellipse_pts(x, y, r, r * 0.75, 9), rng, 2, 0.1) for x, y, r in [(560, 900, 60), (630, 880, 70), (700, 900, 60), (500, 930, 50)]]
    art = LI(art, shapes(W, H, shrub), JUNGLE, seed=nx())
    flowers = []
    for _ in range(26):
        x, y = rng.uniform(470, 720), rng.uniform(840, 930)
        for k in range(5):
            a = k * math.tau / 5 + rng.uniform(0, 1)
            flowers.append(petal_pts(x, y, 9, 4, a, n=8))
    art = LI(art, shapes(W, H, flowers), "#f4e2c4", seed=nx(), grain=0.3)
    art = LI(art, circles(W, H, [(rng.uniform(470, 720), rng.uniform(840, 930), 2.4) for _ in range(26)]), GOLD, seed=nx())
    art = finish(art, 79)
    preview6(art, "pw-poster")
    save_rgb(art, f"{OUT}/poster.webp", size=(600, 800), quality=80)
    clear()

if "train" in PARTS:
    # steam train on a stone viaduct over rice terraces (wide band piece)
    W, H = 1000, 420
    nx = Seq(72000); rng = random.Random(72)
    art = solid(W, H, "#f2a75e")
    for i, (y, col) in enumerate([(0, "#ef9450"), (70, "#f2b36a"), (130, "#f6cf8c"), (180, "#f8e2b2")]):
        art = LI(art, band(W, H, wavy(W, y, 4 if i else 0, 900 + i, 300), H + 10), col, seed=nx(), grain=0.5)
    art = LI(art, band(W, H, wavy(W, 200, 30, 55, 300), H + 10), "#a3809e", seed=nx())
    art = LI(art, band(W, H, wavy(W, 250, 22, 56, 200), H + 10), "#6f8f6a", seed=nx())
    # terraces: stepped curved bands
    for k in range(6):
        y = 300 + k * 22
        col = ["#8db06b", "#7aa15e", "#9cbf74", "#6f9a55", "#a6c47b", "#7aa15e"][k]
        art = LI(art, band(W, H, lambda x, y=y, k=k: y + 10 * math.sin(x / 130 + k), H + 10), col, seed=nx(), grain=0.4)
        art = LI(art, strokes(W, H, [(curve([(x, y + 10 * math.sin(x / 130 + k) + 2) for x in range(-10, W + 20, 20)], 80), 2, None)]), "#e8dca0", seed=nx(), grain=0.2)
    clear()
    # viaduct: deck + arches
    deck_y = 238
    vi = [rect(-10, deck_y, W + 20, 22)]
    for k in range(-1, 12):
        x = k * 92 + 20
        vi.append([(x, deck_y + 20), (x + 24, deck_y + 20), (x + 30, H + 10), (x - 6, H + 10)])
    art = LI(art, shapes(W, H, vi, smooth=False), "#7b5a52", seed=nx())
    art = LI(art, shapes(W, H, [rect(-10, deck_y, W + 20, 6)], smooth=False), "#4f3a3a", seed=nx())
    arch_hi = strokes(W, H, [(arc_pts(k * 92 + 20 + 58, deck_y + 64, 34, math.pi, math.tau, 20), 4, None) for k in range(-1, 12)])
    art = LI(art, arch_hi * (np.arange(H)[:, None] > deck_y + 18), "#9a7568", seed=nx(), grain=0.3)
    # steam locomotive + 3 carriages
    tx, ty = 560, deck_y
    loco = [rect(tx, ty - 46, 120, 34), rect(tx + 92, ty - 74, 46, 62), [(tx + 120, ty - 12), (tx + 160, ty - 12), (tx + 140, ty - 30)]]
    art = LI(art, shapes(W, H, loco, smooth=False), NAVY, seed=nx())
    art = LI(art, shapes(W, H, [rect(tx + 14, ty - 76, 16, 30), rect(tx + 52, ty - 60, 18, 14)], smooth=False), NAVY, seed=nx())
    art = LI(art, shapes(W, H, [rect(tx, ty - 46, 92, 6), rect(tx + 92, ty - 80, 52, 8)], smooth=False), CORAL, seed=nx())
    art = LI(art, shapes(W, H, [rect(tx + 100, ty - 66, 18, 16)], smooth=False), "#f6d68a", seed=nx())
    wheels = circles(W, H, [(tx + 18 + k * 30, ty - 8, 10) for k in range(4)])
    art = LI(art, wheels, "#2d2228", seed=nx())
    art = LI(art, circles(W, H, [(tx + 18 + k * 30, ty - 8, 3) for k in range(4)]), CORAL, seed=nx())
    cars = []
    for c in range(3):
        cx = tx - 150 - c * 148
        cars.append(rect(cx, ty - 56, 136, 44))
    art = LI(art, shapes(W, H, cars, smooth=False), "#2f6f60", seed=nx())
    art = LI(art, shapes(W, H, [rect(tx - 150 - c * 148, ty - 62, 136, 8) for c in range(3)], smooth=False), "#5a3a30", seed=nx())
    wins = []
    for c in range(3):
        cx = tx - 150 - c * 148
        wins += [rect(cx + 10 + k * 25, ty - 48, 16, 14) for k in range(5)]
    art = LI(art, shapes(W, H, wins, smooth=False), "#f6d68a", seed=nx())
    art = LI(art, circles(W, H, [(tx - 150 - c * 148 + d, ty - 8, 8) for c in range(3) for d in (22, 114)]), "#2d2228", seed=nx())
    smoke = [deform(ellipse_pts(tx + 22 - k * 58, ty - 104 - k * 9 + rng.uniform(-5, 5), 22 + k * 5, 15 + k * 3, 10), rng, 2, 0.06) for k in range(9)]
    art = LI(art, shapes(W, H, smoke), "#f8efdc", seed=nx(), grain=0.4)
    art = LI(art, shapes(W, H, [deform(ellipse_pts(tx + 22 - k * 58 + 6, ty - 98 - k * 9, (22 + k * 5) * 0.6, (15 + k * 3) * 0.4, 10), rng, 1, 0.05) for k in range(9)]), "#e4d3bb", seed=nx(), grain=0.3)
    # framing palms
    m, nuts, _ = palm_sil(W, H, 960, 440, 380, rng, lean=-0.15, fronds=8)
    art = LI(art, m, JUNGLE_D, seed=nx(), grain=0.4)
    m, nuts, _ = palm_sil(W, H, 50, 440, 300, rng, lean=0.12, fronds=8)
    art = LI(art, m, JUNGLE_D, seed=nx(), grain=0.4)
    art = finish(art, 81)
    preview6(art, "pw-train")
    save_rgb(art, f"{OUT}/train.webp", size=(820, 344), quality=78)
    clear()

if "waves" in PARTS:
    # divider: three stylised litho waves + a small sun
    W, H = 520, 120
    nx = Seq(73000); rng = random.Random(73)
    art = blank(W, H)
    sun = circles(W, H, [(260, 62, 30)]) * (np.arange(H)[:, None] < 64)
    art = LI(art, sun, ORANGE, seed=nx())
    rays = strokes(W, H, [([(260 + math.cos(a) * 38, 62 + math.sin(a) * 38), (260 + math.cos(a) * 50, 62 + math.sin(a) * 50)], 3.4, None) for a in [math.pi + k * math.pi / 8 for k in range(1, 8)]])
    art = LI(art, rays, GOLD, seed=nx())
    for row, (y, col) in enumerate([(70, TEAL_L), (84, TEAL), (98, TEAL_D)]):
        pts = [(x, y + 6 * math.sin(x / 26 + row)) for x in range(20, 501, 6)]
        art = LI(art, strokes(W, H, [(pts, 5, (0.08, 0.08))]), col, seed=nx(), grain=0.3)
    preview6(art, "pw-waves")
    save(art, f"{OUT}/waves.webp", max_w=320, quality=84)
    clear()

if "palm" in PARTS:
    W, H = 420, 640
    nx = Seq(74000); rng = random.Random(74)
    art = blank(W, H)
    m, nuts, _ = palm_sil(W, H, 120, 640, 560, rng, lean=0.25, fronds=9)
    art = LI(art, m, JUNGLE_D, seed=nx(), grain=0.4)
    art = LI(art, nuts, "#6a4a2a", seed=nx())
    preview6(art, "pw-palm")
    save(art, f"{OUT}/palm.webp", max_w=240, quality=82)
    clear()
