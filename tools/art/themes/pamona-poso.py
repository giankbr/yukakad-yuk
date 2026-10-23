"""Pamona Poso — Danau Poso at morning, Tentena: clear turquoise water over white sand (Siuri), blue ranges, the long
wooden bridge where the lake becomes the Poso river, V-shaped bamboo eel traps (wayamasapi) in the current, and a
Pamona house on stilts (steep straight gable, ijuk thatch, plank walls). Watercolour on paper; Pamona beadwork
(manik merah, kuning, hitam, putih) as gouache beads. Run: python3 -I pamona-poso.py [part ...]
parts: scene beads emblem house water. Assets -> public/themes/art/pamona-poso/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m2_lib import *

OUT = outdir("pamona-poso")
PARTS = sys.argv[1:] or ["scene", "beads", "emblem", "house", "water"]
TEAL, TEAL_D, TURQ, SHALLOW = "#1f6f78", "#0f4652", "#3aa7a4", "#9fd8cf"
SAND, SAND_D = "#f3ecdd", "#d9c9a8"
WOOD, WOOD_D, WOOD_L, IJUK = "#7a4a2a", "#3e2416", "#a8744a", "#2b211c"
RANGE1, RANGE2, RANGE3 = "#9db4c2", "#6f8fa5", "#4d6f7c"
BEAD = {"r": "#b8322a", "y": "#e0a52a", "k": "#1f1a18", "w": "#f4efe6", "t": "#2a8c8a"}


def house_masks(W, H, cx, by, s):
    """Pamona house on stilts, three-quarter-ish front view. by = ground line, s = scale (house width)."""
    m = {}
    fl = by - 0.42 * s          # floor level (raised)
    wall_top = fl - 0.34 * s
    apex = wall_top - 0.78 * s  # steep straight gable
    hw = 0.5 * s
    eave = 0.66 * s
    m["roof"] = shapes(W, H, [[(cx - eave, wall_top + 0.06 * s), (cx, apex), (cx + eave, wall_top + 0.06 * s), (cx + eave * 0.94, wall_top + 0.12 * s), (cx - eave * 0.94, wall_top + 0.12 * s)]], smooth=False)
    # gable board (lighter wood triangle inside the roof front) with crossed finials
    m["gable"] = shapes(W, H, [[(cx - 0.36 * s, wall_top + 0.02 * s), (cx, apex + 0.16 * s), (cx + 0.36 * s, wall_top + 0.02 * s)]], smooth=False)
    m["finial"] = strokes(W, H, [([(cx - 0.02 * s, apex + 0.03 * s), (cx + 0.12 * s, apex - 0.12 * s)], 0.025 * s, (0.0, 0.4)),
                                 ([(cx + 0.02 * s, apex + 0.03 * s), (cx - 0.12 * s, apex - 0.12 * s)], 0.025 * s, (0.0, 0.4))])
    m["wall"] = shapes(W, H, [[(cx - hw, wall_top), (cx + hw, wall_top), (cx + hw, fl), (cx - hw, fl)]], smooth=False)
    m["door"] = shapes(W, H, [[(cx - 0.08 * s, wall_top + 0.08 * s), (cx + 0.08 * s, wall_top + 0.08 * s), (cx + 0.08 * s, fl - 0.01 * s), (cx - 0.08 * s, fl - 0.01 * s)]], smooth=False)
    m["win"] = shapes(W, H, [[(cx + sg * 0.3 * s - 0.06 * s, wall_top + 0.1 * s), (cx + sg * 0.3 * s + 0.06 * s, wall_top + 0.1 * s), (cx + sg * 0.3 * s + 0.06 * s, wall_top + 0.2 * s), (cx + sg * 0.3 * s - 0.06 * s, wall_top + 0.2 * s)] for sg in (-1, 1)], smooth=False)
    planks = [([(cx - hw, wall_top + k * 0.045 * s), (cx + hw, wall_top + k * 0.045 * s)], max(1, 0.006 * s), None) for k in range(1, 8)]
    m["planks"] = strokes(W, H, planks)
    m["beam"] = shapes(W, H, [[(cx - hw - 0.06 * s, fl), (cx + hw + 0.06 * s, fl), (cx + hw + 0.06 * s, fl + 0.05 * s), (cx - hw - 0.06 * s, fl + 0.05 * s)]], smooth=False)
    posts = []
    for f in (-0.46, -0.24, 0.0, 0.24, 0.46):
        x = cx + f * s
        posts.append([(x - 0.022 * s, fl + 0.05 * s), (x + 0.022 * s, fl + 0.05 * s), (x + 0.026 * s, by), (x - 0.026 * s, by)])
    m["posts"] = shapes(W, H, posts, smooth=False)
    m["brace"] = strokes(W, H, [([(cx - 0.46 * s, fl + 0.2 * s), (cx + 0.46 * s, fl + 0.2 * s)], 0.014 * s, None)])
    m["ladder"] = strokes(W, H, [([(cx + 0.1 * s, fl + 0.05 * s), (cx + 0.2 * s, by)], 0.016 * s, None), ([(cx + 0.18 * s, fl + 0.05 * s), (cx + 0.28 * s, by)], 0.016 * s, None)] +
                          [([(cx + 0.1 * s + 0.1 * s * t + 0.004 * s, fl + 0.05 * s + (by - fl - 0.05 * s) * t), (cx + 0.18 * s + 0.1 * s * t, fl + 0.05 * s + (by - fl - 0.05 * s) * t)], 0.012 * s, None) for t in (0.2, 0.42, 0.64, 0.86)])
    thatch = []
    for k in range(26):
        t = k / 25
        x = cx - eave + 2 * eave * t
        thatch.append(([(cx + (x - cx) * 0.12, apex + 0.1 * s), (x, wall_top + 0.11 * s)], max(1, 0.006 * s), (0.2, 0.1)))
    m["thatch"] = strokes(W, H, thatch)
    return m


def paint_house(art, W, H, cx, by, s, nx, d=1.0):
    m = house_masks(W, H, cx, by, s)
    art = G(art, np.maximum(m["posts"], m["brace"]), WOOD, WOOD_D, seed=nx(), density=0.85 * d, edge=0.5, bloom=0.1, rough=1.5, feather=0.8)
    art = G(art, m["ladder"], WOOD_L, WOOD, seed=nx(), density=0.8 * d, edge=0.4, bloom=0, rough=1, feather=0.6)
    art = G(art, m["beam"], WOOD_D, seed=nx(), density=0.9 * d, edge=0.4, bloom=0, rough=1.5)
    art = G(art, m["wall"], WOOD_L, WOOD, seed=nx(), density=0.85 * d, edge=0.55, bloom=0.4, rough=2)
    art = G(art, m["planks"] * m["wall"], WOOD_D, seed=nx(), density=0.4 * d, edge=0.1, bloom=0, rough=1, feather=0.5)
    art = G(art, np.maximum(m["door"], m["win"]), "#2a1810", seed=nx(), density=0.9 * d, edge=0.3, bloom=0.1, rough=1.2)
    art = G(art, m["roof"], IJUK, "#4a3a2e", seed=nx(), density=0.95 * d, edge=0.6, bloom=0.3, rough=2.5)
    art = G(art, m["thatch"] * m["roof"], "#6d5a48", seed=nx(), density=0.35 * d, edge=0.1, bloom=0, rough=1, feather=0.5)
    art = G(art, m["gable"], "#c89058", WOOD_L, seed=nx(), density=0.85 * d, edge=0.5, bloom=0.3, rough=2)
    # gable ornament: beaded triangle bands (red/yellow) painted on the board
    yy, xx = yy_xx(W, H)
    tri_r, tri_y = [], []
    top = by - 0.42 * s - 0.34 * s
    for row in range(5):
        yb = top - row * 0.075 * s
        half = 0.34 * s * (1 - (row * 0.075 * s + 0.02 * s) / (0.78 * s - 0.16 * s))
        n = max(1, int(half * 2 / (0.06 * s)))
        for i in range(n):
            x0 = cx - half + i * (2 * half / n)
            tri = [(x0, yb), (x0 + half / n, yb - 0.05 * s), (x0 + 2 * half / n, yb)]
            (tri_r if (i + row) % 2 else tri_y).append(tri)
    art = G(art, shapes(W, H, tri_r, smooth=False) * m["gable"], BEAD["r"], seed=nx(), density=0.85 * d, edge=0.3, bloom=0, rough=1, feather=0.6)
    art = G(art, shapes(W, H, tri_y, smooth=False) * m["gable"], "#e8b640", seed=nx(), density=0.85 * d, edge=0.3, bloom=0, rough=1, feather=0.6)
    art = G(art, strokes(W, H, [([(cx - 0.36 * s + 0.36 * s * row * 0.12, top - row * 0.075 * s), (cx + 0.36 * s - 0.36 * s * row * 0.12, top - row * 0.075 * s)], 0.012 * s, None) for row in range(5)]) * m["gable"], IJUK, seed=nx(), density=0.7 * d, edge=0.2, rough=1, feather=0.5)
    art = G(art, m["finial"], WOOD_D, seed=nx(), density=0.95 * d, edge=0.3, rough=1, feather=0.6)
    return art, m


def canopy(W, H, cx, cy, rx, ry, rng, n=26):
    """Cluster of leafy puffs (tree crowns) as one mask."""
    items = []
    for _ in range(n):
        a = rng.uniform(0, math.tau); d = rng.uniform(0, 1) ** 0.6
        items.append((cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d, rng.uniform(0.22, 0.42) * min(rx, ry) * 1.3))
    return circles(W, H, items)


def palm2(W, H, x, by, h, rng, lean=0.1):
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.25, by - h * 0.5), top], 30)
    items = [(trunk, h * 0.035, (0.02, 0.5))]
    fr = []
    for k in range(10):
        a = -math.pi / 2 + (k - 4.5) * 0.36 + rng.uniform(-0.08, 0.08)
        L = h * rng.uniform(0.36, 0.48)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - h * 0.04),
                     (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.5)], 22)
        fr.append((pts, h * 0.026, (0.05, 0.75)))
        for j in range(3, 21, 2):
            px, py = pts[j]
            for sg in (-1, 1):
                qa = a + sg * 0.9
                ll = L * 0.22 * (1 - j / 28)
                fr.append(([(px, py), (px + math.cos(qa) * ll * 0.5, py + math.sin(qa) * ll * 0.5 + ll * 0.3), (px + math.cos(qa) * ll, py + math.sin(qa) * ll + ll * 0.75)], h * 0.007, (0.1, 0.7)))
    return strokes(W, H, items), strokes(W, H, fr)


if "scene" in PARTS:
    W, H = 780, 1500
    nx = Seq(51000)
    rng = random.Random(7)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    # sky: soft blue from the top fading to a warm morning band at the horizon (still light enough for dark text)
    art = G(art, (yy < 640).astype(np.float32), "#d6e7ee", "#e4eef1", seed=nx(), density=0.55, edge=0.02, bloom=0.5, rough=8, feather=10, mottle=0.8)
    art = G(art, np.clip((yy - 330) / 260, 0, 1) * (yy < 650), "#f5dcb8", "#f2e2c8", seed=nx(), density=0.5, edge=0.05, bloom=0.4, rough=6, feather=12)
    # lifted cloud shapes (paper showing) as faint warm-grey undersides
    cl = np.zeros((H, W), np.float32)
    for (cx, cy, w, h) in ((170, 250, 260, 50), (560, 160, 300, 60), (640, 400, 200, 36), (260, 470, 220, 30)):
        cl = np.maximum(cl, jw.circles(W, H, [(cx - w / 2 + w * t, cy - math.sin(t * math.pi) * h * 0.5, h * (0.4 + 0.5 * math.sin(t * math.pi))) for t in np.linspace(0, 1, 7)]))
    art = knockout(art, cl, amount=0.75, grow=3)
    art = G(art, cl * np.clip((yy - 0) / 1, 0, 1) * 0.35 * np.roll(cl, -14, 0), "#e7d9cc", seed=nx(), density=0.4, edge=0.05, bloom=0.5, rough=5, feather=5)
    birds = strokes(W, H, [(curve([(bx - 7, by - 2), (bx, by + 2), (bx + 7, by - 3)], 6), 1.6, (0.2, 0.2)) for bx, by in ((470, 520), (492, 508), (520, 530), (300, 560))])
    art = G(art, birds, "#4a4a4a", seed=nx(), density=0.7, edge=0.2, rough=0.6, feather=0.4)
    clear()
    # far ranges (three layers, cool to warm) with a band of morning mist between them
    for k, (y, amp, col, col2, dens) in enumerate([(560, 50, RANGE1, "#b7c7cf", 0.6), (606, 36, RANGE2, RANGE1, 0.65), (646, 20, RANGE3, RANGE2, 0.7)]):
        hm = hills(W, H, y, amp, 300 + k, 0.55 - k * 0.1) * (yy < 700)
        art = G(art, hm, col, col2, seed=nx(), density=dens, edge=0.5, bloom=0.35, rough=4)
        art = soft(art, hm * np.clip(1 - np.abs(yy - (y + 18)) / 16, 0, 1), "#eef3f2", alpha=0.45, blur=4, pad=10)
        clear()
    lake_top = 660
    shore = [(-20, 1010)]
    for x in range(-20, W + 41, 30):
        shore.append((x, 1000 + 26 * math.sin(x / 140 + 0.6) + 14 * math.sin(x / 47)))
    lake = shapes(W, H, [[(-20, lake_top), (W + 20, lake_top)] + shore[::-1]], smooth=False)
    art = G(art, lake * np.clip(1 - (yy - lake_top) / 300, 0, 1), TEAL_D, TEAL, seed=nx(), density=0.95, edge=0.15, bloom=0.25, rough=3, feather=1.5)
    art = G(art, lake * np.clip(1 - np.abs(yy - 790) / 160, 0, 1), TEAL, TURQ, seed=nx(), density=0.8, edge=0.15, bloom=0.4, rough=4, feather=2)
    art = G(art, lake * np.clip((yy - 800) / 200, 0, 1), TURQ, SHALLOW, seed=nx(), density=0.7, edge=0.3, bloom=0.5, rough=4, feather=2)
    # sandy bottom seen through clear shallows: warm patches + caustic web
    cw = fbm(W, H, nx(), 9, 2)
    caus = np.clip(1 - np.abs(cw - 0.5) * 10, 0, 1) * lake * np.clip((yy - 880) / 100, 0, 1)
    art = soft(art, caus, "#e9fbf4", alpha=0.22, blur=1.2, pad=6)
    art = G(art, lake * np.clip((yy - 940) / 60, 0, 1), "#e6dcc2", seed=nx(), density=0.35, edge=0.1, bloom=0.5, rough=4)
    refl = strokes(W, H, [([(x0, y), (x0 + rng.uniform(30, 120), y)], rng.uniform(2, 4), (0.3, 0.3)) for _ in range(80)
                          for x0, y in [(rng.uniform(-40, W), rng.uniform(lake_top + 4, lake_top + 100))]])
    art = G(art, refl * lake, "#2f5560", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1.5)
    glint = strokes(W, H, [([(x0, y), (x0 + rng.uniform(10, 50), y)], rng.uniform(1.2, 2.4), (0.4, 0.4)) for _ in range(110)
                           for x0, y in [(rng.uniform(-20, W), rng.uniform(lake_top + 30, 990))]])
    art = soft(art, glint * lake, "#f6fbf6", alpha=0.65, pad=4)
    clear()
    trees = strokes(W, H, [([(x, lake_top + 2), (x, lake_top - rng.uniform(3, 11))], rng.uniform(5, 10), (0.1, 0.6)) for x in range(-10, W + 10, 6)])
    art = G(art, np.maximum(trees, rects(W, H, [(-20, lake_top - 2, W + 40, 6)])), "#2f5d4f", "#3f6b55", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=2)
    clear()
    # the long wooden bridge where the lake narrows into the Poso river (right, mid distance)
    by0, bx0, bx1 = 760, 330, 800
    deck = rects(W, H, [(bx0, by0, bx1 - bx0, 9)])
    rail = rects(W, H, [(bx0, by0 - 16, bx1 - bx0, 3)])
    piles = rects(W, H, [(x, by0 + 8, 4, 26) for x in range(bx0 + 6, bx1, 26)] + [(x, by0 - 16, 3, 16) for x in range(bx0 + 6, bx1, 13)])
    art = G(art, np.maximum.reduce([deck, rail, piles]), WOOD, WOOD_D, seed=nx(), density=0.95, edge=0.4, bloom=0.1, rough=1.2, feather=0.6)
    pv = 600
    art = G(art, shapes(W, H, [[(pv - 52, by0 - 14), (pv, by0 - 72), (pv + 52, by0 - 14)]], smooth=False), IJUK, "#4a3a2e", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, shapes(W, H, [[(pv - 22, by0 - 20), (pv, by0 - 52), (pv + 22, by0 - 20)]], smooth=False), "#c89058", seed=nx(), density=0.8, edge=0.4, rough=1)
    art = G(art, rects(W, H, [(pv - 40, by0 - 16, 4, 16), (pv + 36, by0 - 16, 4, 16)]), WOOD_D, seed=nx(), density=0.9, edge=0.3, rough=1)
    brefl = rects(W, H, [(x, by0 + 36 + rng.uniform(0, 8), rng.uniform(8, 22), 2.5) for x in range(bx0, bx1, 16)])
    art = G(art, brefl * lake, WOOD_D, seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1.5)
    clear()
    # V-shaped eel traps (wayamasapi) in the current
    stakes = []
    for (ax, ay, w2) in ((470, 870, 80), (690, 905, 64)):
        for k in range(18):
            t = k / 17
            for sg in (-1, 1):
                x = ax + sg * (1 - t) * w2; y = ay - (1 - t) * 34
                stakes.append(([(x, y), (x + rng.uniform(-1, 1), y - rng.uniform(18, 28))], 3.0, (0.05, 0.3)))
    sm = strokes(W, H, stakes)
    art = G(art, sm, "#5d4a30", "#3e2f1e", seed=nx(), density=0.95, edge=0.3, bloom=0, rough=1)
    art = G(art, np.roll(sm, 30, 0) * lake * 0.6, "#2e5a5c", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1)
    clear()
    # forested headland on the left: layered tree crowns, darker towards the water
    head = shapes(W, H, [[(-20, 660), (30, 626), (110, 612), (190, 634), (250, 680), (300, 740), (318, 800), (300, 880), (240, 930), (-20, 960)]])
    art = G(art, head, "#5f8a5c", "#4f7f52", seed=nx(), density=0.95, edge=0.5, bloom=0.4, rough=4)
    for (cx, cy, rx, ry, c1) in ((100, 650, 130, 40, "#7f9f6c"), (200, 720, 110, 60, "#4b7a4e"), (240, 830, 70, 70, "#2f5a3e")):
        cm = canopy(W, H, cx, cy, rx, ry, rng, 30)
        art = G(art, cm, c1, seed=nx(), density=0.75, edge=0.7, bloom=0.4, rough=3)
        clear()
    art = G(art, head * np.clip((xx - 150) / 170, 0, 1) * np.clip((yy - 700) / 200, 0, 1), "#22402e", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=2)
    clear()
    art, hm = paint_house(art, W, H, 160, 915, 220, nx)
    sh = strokes(W, H, [([(160 + dx, 924 + j * 8), (160 + dx + 34, 924 + j * 8)], 3, (0.3, 0.3)) for j in range(9) for dx in (-110, -66, -22, 22, 66) if rng.random() < 0.8])
    art = G(art, sh * lake, WOOD_D, seed=nx(), density=0.4, edge=0.1, bloom=0, rough=1.5)
    clear()
    # right-edge tree clump framing the bridge end
    for (cx, cy, rx, ry, c1, c2) in ((770, 700, 70, 120, "#5f8a5c", "#3f6b48"), (790, 800, 60, 110, "#3e6c48", "#2e5a3e")):
        cm = canopy(W, H, cx, cy, rx, ry, rng, 30)
        art = G(art, cm, c1, c2, seed=nx(), density=0.9, edge=0.6, bloom=0.4, rough=3)
        art = G(art, cm * np.clip((yy - cy + ry * 0.2) / ry, 0, 1), "#22402e", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=2)
        clear()
    canoe = shapes(W, H, [[(470, 1032), (640, 1030), (664, 1016), (632, 1048), (490, 1050), (452, 1020)]])
    art = G(art, canoe, WOOD, WOOD_D, seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, strokes(W, H, [([(498, 1030), (640, 1027)], 3.5, None)]), "#3e2416", seed=nx(), density=0.8, edge=0.2, rough=1)
    art = G(art, np.roll(canoe, 22, 0) * 0.5, "#a08a66", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=2, feather=4)
    clear()
    # white sand, wet margin, clear-water ripple lines, grass tufts and stones at the edges (centre left open)
    sand = np.clip((yy - 990) / 30, 0, 1)
    art = G(art, sand * (1 - lake), SAND, "#efe2c8", seed=nx(), density=0.4, edge=0.05, bloom=0.5, rough=6, feather=4)
    wet = np.clip(1 - np.abs(yy - (1014 + 26 * np.sin(xx / 140 + 0.6) + 14 * np.sin(xx / 47))) / 12, 0, 1)
    art = G(art, wet, "#c9b88f", seed=nx(), density=0.45, edge=0.3, bloom=0.2, rough=3)
    foam = np.clip(1 - np.abs(yy - (1002 + 26 * np.sin(xx / 140 + 0.6) + 14 * np.sin(xx / 47))) / 4, 0, 1)
    art = soft(art, foam, "#ffffff", alpha=0.8, blur=1, pad=4)
    rip = strokes(W, H, [([(x0, y), (x0 + rng.uniform(40, 110), y + rng.uniform(-2, 2))], 1.6, (0.4, 0.4)) for _ in range(70)
                         for x0, y in [(rng.uniform(-20, W), rng.uniform(880, 1000))]])
    art = G(art, rip * lake, "#4fa9a2", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1)
    tufts = []
    for (gx, gy) in ((40, 1100), (90, 1130), (700, 1090), (740, 1150), (20, 1220), (760, 1260)):
        for k in range(12):
            a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
            L = rng.uniform(18, 46)
            tufts.append((curve([(gx, gy), (gx + math.cos(a) * L * 0.5, gy + math.sin(a) * L * 0.6), (gx + math.cos(a) * L, gy + math.sin(a) * L + 6)], 8), 3, (0.05, 0.8)))
    art = G(art, strokes(W, H, tufts), "#7c9a5a", "#4f7a45", seed=nx(), density=0.85, edge=0.4, bloom=0.2, rough=1)
    stones = ellipses(W, H, [(30, 1170, 34, 18, -8), (74, 1180, 20, 12, 6), (730, 1210, 30, 16, 10), (690, 1220, 16, 9, 0)])
    art = G(art, stones, "#a59a88", "#7d7466", seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=2)
    art = G(art, stones * np.clip((yy - 1170) / 20, 0, 1), "#5b544a", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1)
    clear()
    prev(art, "pp-scene", bg=None)
    out = on_paper(art, "#f6f0e2")
    arr = np.asarray(out, np.float32) / 255
    arr = np.concatenate([arr, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/scene.webp", size=(640, 1231), quality=78)

if "house" in PARTS:
    W, H = 520, 560
    nx = Seq(52000)
    art = blank(W, H)
    art, _ = paint_house(art, W, H, 260, 520, 300, nx)
    ground = shapes(W, H, [[(40, 516), (480, 512), (490, 530), (30, 534)]])
    art = G(art, ground, "#9fd8cf", "#3aa7a4", seed=nx(), density=0.6, edge=0.5, bloom=0.4, rough=4)
    prev(art, "pp-house", bg=None)
    save(art, f"{OUT}/house.webp", max_w=300, quality=82)


def bead_layer(W, H, beads, r, seed=1):
    """beads: (x, y, key). Gouache-glossy round beads: body, darker lower rim, small highlight, hole hint."""
    art = blank(W, H)
    by = {}
    for x, y, k in beads:
        by.setdefault(k, []).append((x, y))
    for k, pts in by.items():
        m = circles(W, H, [(x, y, r) for x, y in pts])
        art = over(art, gouache_paint(m, BEAD[k], mix(BEAD[k], "#000000", 0.18), seed=seed + len(pts), rough=0.8, streak=0.3))
        sh = circles(W, H, [(x + r * 0.25, y + r * 0.3, r * 0.78) for x, y in pts]) * m
        art = over(art, flat(gaussian_filter(np.clip(m - sh, 0, 1), 0.6), "#000000", 0.0))
        dark = np.clip(m - circles(W, H, [(x - r * 0.15, y - r * 0.2, r * 0.85) for x, y in pts]), 0, 1)
        art = over(art, flat(gaussian_filter(dark, 0.8), "#000000", 0.28))
        hl = circles(W, H, [(x - r * 0.35, y - r * 0.38, r * 0.26) for x, y in pts])
        art = over(art, flat(gaussian_filter(hl, 0.7), "#ffffff", 0.6 if k != "w" else 0.9))
    return art


if "beads" in PARTS:
    # seamless beaded band (period 24 beads): white ground row, red/yellow triangles meeting black lozenges
    per, rows = 24, 7
    r = 5.0; step = 2 * r + 0.6
    W, H = int(per * step), int(rows * step + 2)
    pat = []
    for row in range(rows):
        for c in range(per):
            p = c % 12
            dd = abs(p - 6) + abs(row - 3)
            de = min(p, 12 - p) + abs(row - 3)
            if row in (0, 6):
                k = "k" if c % 2 else "r"
            elif dd <= 1:
                k = "y"
            elif dd == 2:
                k = "r"
            elif dd == 3:
                k = "k"
            elif de <= 1:
                k = "t"
            else:
                k = "w"
            pat.append((c * step + step / 2, row * step + step / 2 + 1, k))
    # wrap duplicates so edge beads are whole
    pat += [(x + W, y, k) for x, y, k in pat if x < step] + [(x - W, y, k) for x, y, k in pat if x > W - step]
    art = bead_layer(W, H, pat, r, seed=11)
    thread = rects(W, H, [(0, row * step + step / 2 + 0.5, W, 1) for row in range(rows)])
    art = over(flat(thread, "#6b5a44", 0.5), art)
    prev(art, "pp-beads", bg="#f3ecdd")
    save_full(art, f"{OUT}/beads.webp", quality=86)

if "emblem" in PARTS:
    # round beaded rosette (Pamona necklace medallion): concentric rings with an eight-petal star
    W = H = 300
    cx = cy = 150
    r = 6.2
    beads = []
    for ring_i, (rad, keys) in enumerate([(0, "y"), (14, "r"), (27, "k"), (40, "y"), (53, "r"), (66, "w"), (79, "k"), (92, "t"), (105, "r"), (118, "k")]):
        if rad == 0:
            beads.append((cx, cy, "y")); continue
        n = max(6, int(2 * math.pi * rad / (2 * r + 0.8)))
        for i in range(n):
            a = i / n * math.tau
            k = keys
            if rad in (53, 66, 79):
                seg = (i * 8 // n) % 2
                k = ("r" if rad == 53 else "w" if rad == 66 else "k") if seg else ("y" if rad != 79 else "r")
            beads.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad, k))
    art = bead_layer(W, H, beads, r, seed=21)
    prev(art, "pp-emblem", bg="#f3ecdd")
    save(art, f"{OUT}/emblem.webp", max_w=150, quality=86)

if "water" in PARTS:
    # seamless lake-water tile (turquoise over white sand, caustic light lines) for the countdown band
    W = H = 360
    nx = Seq(53000)
    base = vgrad = None
    t = wrap_noise(W, H, 3, 30)
    rgb = np.array(hex_rgb(TEAL), np.float32) * (1 - t[..., None]) + np.array(hex_rgb("#2a8f92"), np.float32) * t[..., None]
    c1 = wrap_noise(W, H, 5, 6); c2 = wrap_noise(W, H, 6, 9)
    caus = np.clip(1 - np.abs(c1 - 0.5) * 9, 0, 1) * 0.6 + np.clip(1 - np.abs(c2 - 0.5) * 10, 0, 1) * 0.4
    rgb = rgb * (1 - caus[..., None] * 0.35) + np.array(hex_rgb("#bfeee2"), np.float32) * caus[..., None] * 0.35
    g = wrap_noise(W, H, 8, 0.8)
    rgb = rgb * (0.96 + 0.08 * g[..., None])
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    prev(arr, "pp-water", bg="#000000")
    save_full(arr, f"{OUT}/water.webp", size=(300, 300), quality=72)
