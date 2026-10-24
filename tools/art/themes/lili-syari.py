"""Lili Syari — white calla lilies and a Madonna lily in clean watercolour on cream: opaque white body with cool
grey-green shadow glazes, chartreuse throats, gold spadix, long jade stems tied with a pressed-gold ribbon.
Parts: tangkai (tall bouquet for the cover column), lili (Madonna lily bloom emblem), kuncup (single calla head),
daun (stem + bud divider). Run: python3 -I lili-syari.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t5_lib import *

OUT = outdir("lili-syari")
PARTS = sys.argv[1:] or ["tangkai", "lili", "kuncup", "daun"]
WHITE, WHITE2 = "#fffdf6", "#f4f1e6"
SHADE, SHADE_D = "#c7cfc0", "#98a693"
GREEN_L, GREEN, GREEN_D = "#9dbb7c", "#5f8c52", "#35603a"
GOLD = "#c49a45"


def loc(bx, by, ang, L, Wd):
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca  # perpendicular

    def f(u, v):
        return (bx + ca * u * L + px * v * Wd, by + sa * u * L + py * v * Wd)
    return f


def calla(art, W, H, bx, by, ang, L, Wd, nx, flip=1, rng=None):
    """Side/front view calla: funnel body rising from the stem, a wide oval mouth with the front lip rolled out,
    the back of the spathe rising to a pointed tip that curls back; chartreuse throat and a gold spadix."""
    f = loc(bx, by, ang, L, Wd)
    F = lambda u, v: f(u, v * flip)
    rot = math.degrees(ang) + 90
    # silhouette: funnel + back flag + lower half of the mouth
    funnel = [F(0, -0.07), F(0.2, -0.1), F(0.42, -0.2), F(0.6, -0.34), F(0.7, -0.44), F(0.86, -0.5), F(1.0, -0.42),
              F(1.12, -0.2), F(1.26, 0.06), F(1.34, 0.2), F(1.18, 0.2), F(1.02, 0.34), F(0.82, 0.46), F(0.66, 0.42),
              F(0.56, 0.3), F(0.4, 0.17), F(0.2, 0.09), F(0, 0.07)]
    fm = shape_mask(W, H, funnel)
    mc = F(0.7, 0.0)
    mouth = ellipses(W, H, [(mc[0], mc[1], Wd * 0.45, L * 0.13, rot)])
    m = np.maximum(fm, mouth)
    # body paint: soft white with very light streak
    art = GP(art, m, WHITE, WHITE2, seed=nx(), rough=1.0, streak=0.12)
    # outside shadow on the far side of the funnel, under the lip
    sh = side_shade(m, F(0, 0), F(1, 0), Wd * 0.7)
    sh = sh if flip > 0 else 1 - sh
    below = fm * np.clip((L * 0.66 - np.hypot(yx(W, H)[1] - F(0, 0)[0], yx(W, H)[0] - F(0, 0)[1])) / (L * 0.25), 0, 1)
    art = G(art, below * np.clip((sh - 0.35) * 1.6, 0.15, 1), SHADE, SHADE_D, seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=1.0, feather=1.2)
    # inside of the back flag: lighter top, cool shade low
    inner_back = fm * np.clip((np.hypot(yx(W, H)[1] - F(0, 0)[0], yx(W, H)[0] - F(0, 0)[1]) - L * 0.7) / (L * 0.2), 0, 1)
    art = G(art, inner_back * np.clip(1.2 - (np.hypot(yx(W, H)[1] - F(0, 0)[0], yx(W, H)[0] - F(0, 0)[1]) - L * 0.7) / (L * 0.4), 0, 1), "#dfe5d6", SHADE, seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=1.0, feather=1.6)
    # green base fading up the funnel
    base_t = np.clip(1 - np.hypot(yx(W, H)[1] - F(0.0, 0)[0], yx(W, H)[0] - F(0.0, 0)[1]) / (L * 0.48), 0, 1)
    art = G(art, m * base_t ** 1.3, GREEN_L, GREEN, seed=nx(), density=0.85, edge=0.2, bloom=0.2, rough=1.0, feather=1.5)
    # throat: chartreuse well inside the mouth, deepest at the back
    tc = F(0.68, 0.02)
    thr = ellipses(W, H, [(tc[0], tc[1], Wd * 0.3, L * 0.075, rot)])
    art = G(art, thr, "#e8edbb", "#b9cc78", seed=nx(), density=0.75, edge=0.55, bloom=0.2, rough=0.6, feather=1.0)
    sp0, sp1 = F(0.64, 0.02), F(0.86, 0.06)
    art = GP(art, line(W, H, [sp0, ((sp0[0] + sp1[0]) / 2, (sp0[1] + sp1[1]) / 2), sp1], Wd * 0.085, (0.05, 0.5)), "#f2c654", "#c9962f", seed=nx(), rough=0.4, streak=0.2)
    # rolled front lip: bright roll + shadow line beneath it
    lip = [F(0.7 + 0.13 * math.sin(t), 0.45 * math.cos(t)) for t in np.linspace(0.12, math.pi - 0.12, 26)]
    lip = [F(0.7 - 0.13 * math.sin(t), 0.45 * math.cos(t)) for t in np.linspace(0.05, math.pi - 0.05, 26)]
    shadow = [(x + (F(-0.04, 0)[0] - F(0, 0)[0]), y + (F(-0.04, 0)[1] - F(0, 0)[1])) for x, y in lip]
    art = OV(art, gaussian_filter(line(W, H, shadow, Wd * 0.05, (0.15, 0.15)), 1.5) * m, lambda mm: rgba(SHADE_D, mm * 0.45))
    art = OV(art, line(W, H, lip, Wd * 0.06, (0.2, 0.2)) * m, lambda mm: rgba("#ffffff", mm * 0.95))
    # outline: grey-green wet edge so white reads on cream
    edge = np.clip(m - gaussian_filter(m, 1.5) * 1.04, 0, 1)
    art = OV(art, edge, lambda mm: rgba(SHADE_D, mm * 0.7))
    vs = [(curve([F(0.1, v * 0.25), F(0.4, v * 0.6), F(0.62, v)], 16), 1.1, (0.1, 0.5)) for v in (-0.22, 0.12, 0.26)]
    art = OV(art, strokes(W, H, vs) * fm, lambda mm: rgba(SHADE, mm * 0.4))
    return art


def stem(art, W, H, pts, wd, nx):
    m = line(W, H, curve(pts, 50), wd, (0.0, 0.08))
    art = G(art, m, GREEN_L, GREEN, seed=nx(), density=0.9, edge=0.5, bloom=0.15, rough=0.8, feather=0.6)
    hl = line(W, H, [(x - wd * 0.18, y) for x, y in curve(pts, 50)], wd * 0.25, (0.05, 0.3)) * m
    return OV(art, hl, lambda mm: rgba("#d6e6b6", mm * 0.5))


def leaf(art, W, H, x, y, L, ang, nx, wd=0.22, cup=0.2):
    m = shape_mask(W, H, petal_pts(x, y, L, L * wd, ang, n=16, cup=cup))
    art = G(art, m, GREEN_L, GREEN, seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.2, feather=0.6)
    half = shape_mask(W, H, petal_pts(x, y, L * 0.97, L * wd * 0.45, ang + 0.05, n=12, cup=cup)) * m
    art = G(art, half, GREEN, GREEN_D, seed=nx(), density=0.6, edge=0.3, bloom=0.2, rough=1, feather=0.8)
    vein = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [j / 12 for j in range(1, 11)]]
    return OV(art, line(W, H, vein, max(1.2, L * 0.012), (0.05, 0.5)) * m, lambda mm: rgba("#e4efcc", mm * 0.6))


def madonna(art, W, H, cx, cy, r, nx, rot=0.0, squash=0.82):
    """Madonna lily (Lilium candidum) seen from the front: six recurved white tepals, green nectary lines, gold anthers."""
    allm = np.zeros((H, W), np.float32)
    for k in range(6):
        a = rot + k * math.tau / 6 + (0.08 if k % 2 else -0.04)
        L = r * (1.0 if k % 2 == 0 else 0.92)
        pts = petal_pts(cx, cy, L, L * 0.3, a, n=18, cup=0.22)
        pts = [(cx + (px - cx), cy + (py - cy) * squash) for px, py in pts]
        m = shape_mask(W, H, pts)
        np.maximum(allm, m, out=allm)
        art = GP(art, m, WHITE, WHITE2, seed=nx(), rough=1.0, streak=0.12)
        sh = np.clip(1 - np.hypot(yx(W, H)[1] - cx, yx(W, H)[0] - cy) / (r * 0.75), 0, 1) * m
        art = G(art, sh, SHADE, "#b5c4b0", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=0.8, feather=1)
        side = shape_mask(W, H, [(cx, cy)] + [(cx + math.cos(a + 0.02 * q) * L * 1.05, cy + math.sin(a + 0.02 * q) * L * 1.05 * squash) for q in range(14)]) * m
        art = G(art, gaussian_filter(side, 3) * m, SHADE, seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=0.6, feather=1)
        tip = (cx + math.cos(a) * L * 0.92, cy + math.sin(a) * L * 0.92 * squash)
        vein = line(W, H, [(cx, cy), ((cx + tip[0]) / 2, (cy + tip[1]) / 2), tip], r * 0.022, (0.0, 0.6)) * m
        art = OV(art, vein, lambda mm: rgba("#b7cf8c", mm * 0.75))
        edge = np.clip(m - gaussian_filter(m, 1.3) * 1.05, 0, 1)
        art = OV(art, edge, lambda mm: rgba(SHADE_D, mm * 0.65))
    art = G(art, circles(W, H, [(cx, cy, r * 0.16)]) * allm, "#d7e3a2", "#a9c06b", seed=nx(), density=0.75, edge=0.3, bloom=0.2, rough=0.6, feather=1.2)
    fil = []
    rng = random.Random(int(cx + cy))
    anth = []
    for k in range(6):
        a = rot + 0.5 + k * math.tau / 6 + rng.uniform(-.2, .2)
        L = r * rng.uniform(0.42, 0.55)
        ex, ey = cx + math.cos(a) * L, cy + math.sin(a) * L * squash
        fil.append(([(cx, cy), ((cx + ex) / 2, (cy + ey) / 2 - 2), (ex, ey)], max(1.2, r * 0.018), None))
        anth.append((ex, ey, r * 0.07, r * 0.035, math.degrees(a) + 90))
    art = OV(art, strokes(W, H, fil), lambda mm: rgba("#c4d49a", mm * 0.9))
    art = GP(art, ellipses(W, H, anth), "#e6a93a", "#b9781f", seed=nx(), rough=0.5, streak=0.3)
    return art


def ribbon(art, W, H, cx, cy, nx):
    band = line(W, H, [(cx - 22, cy - 4), (cx, cy - 7), (cx + 22, cy - 3)], 9, None)
    loops = strokes(W, H, [(curve([(cx, cy), (cx - 30, cy - 26), (cx - 58, cy - 20), (cx - 50, cy + 4), (cx, cy)], 40), 6, None),
                           (curve([(cx, cy), (cx + 28, cy - 30), (cx + 56, cy - 26), (cx + 50, cy + 2), (cx, cy)], 40), 6, None)])
    tails = strokes(W, H, [(curve([(cx, cy), (cx - 12, cy + 40), (cx - 28, cy + 92), (cx - 22, cy + 140)], 30), 6.5, (0.05, 0.1)),
                           (curve([(cx, cy), (cx + 14, cy + 44), (cx + 32, cy + 84), (cx + 50, cy + 118)], 30), 6, (0.05, 0.1))])
    for m in (tails, loops, band):
        art = FO(art, m, GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    return FO(art, ell(W, H, cx, cy, 8, 7), "#b88d3c", seed=nx(), emboss=0.9, sparkle=0.1)


def tangkai():
    W, H = 420, 1420
    nx = Seq(7)
    art = blank(W, H)
    tie = (204, 1090)
    art = leaf(art, W, H, 200, 1150, 360, -math.pi / 2 - 0.46, nx, wd=0.2)
    art = leaf(art, W, H, 210, 1130, 320, -math.pi / 2 + 0.4, nx, wd=0.18)
    art = leaf(art, W, H, 206, 1240, 210, -math.pi / 2 + 0.95, nx, wd=0.22)
    clear()
    heads = [  # (base x, base y, angle, length, width, flip)
        (132, 420, -math.pi / 2 - 0.2, 195, 146, -1),
        (276, 300, -math.pi / 2 + 0.1, 205, 150, 1),
        (300, 660, -math.pi / 2 + 0.4, 160, 118, 1),
    ]
    for bx, by, a, L, Wd, fl in heads:
        art = stem(art, W, H, [(tie[0], H - 26), tie, ((tie[0] + bx) / 2 + fl * 8, (tie[1] + by) / 2), (bx, by)], 15, nx)
    art = stem(art, W, H, [(206, H - 30), tie, (120, 820), (76, 712)], 10, nx)
    clear()
    for bx, by, a, L, Wd, fl in heads:
        art = calla(art, W, H, bx, by, a, L, Wd, nx, flip=fl)
        clear()
    bud = shape_mask(W, H, petal_pts(76, 716, 130, 32, -math.pi / 2 - 0.3, n=16, cup=0.1))
    art = GP(art, bud, WHITE, WHITE2, seed=nx(), rough=1, streak=0.12)
    art = G(art, bud * np.clip((yx(W, H)[0] - 640) / 80, 0, 1), GREEN_L, GREEN, seed=nx(), density=0.7, edge=0.3, bloom=0.2, rough=1, feather=1.2)
    art = OV(art, np.clip(bud - gaussian_filter(bud, 1.5) * 1.04, 0, 1), lambda mm: rgba(SHADE_D, mm * 0.7))
    art = stem(art, W, H, [(200, H - 30), tie, (232, 940), (238, 880)], 12, nx)
    art = madonna(art, W, H, 236, 868, 104, nx, rot=0.3)
    clear()
    art = leaf(art, W, H, 210, 1030, 150, -math.pi / 2 - 1.0, nx, wd=0.2)
    art = ribbon(art, W, H, *tie, nx)
    save_prev(art, "tangkai", "#f6efe0")
    save(art, f"{OUT}/tangkai.webp", max_w=360, quality=82)


def lili():
    W, H = 420, 420
    nx = Seq(41)
    art = blank(W, H)
    art = leaf(art, W, H, 210, 230, 190, math.pi * 0.86, nx, wd=0.2)
    art = leaf(art, W, H, 210, 230, 190, math.pi * 0.14, nx, wd=0.2)
    art = madonna(art, W, H, 210, 200, 150, nx, rot=-0.25)
    save_prev(art, "lili", "#f6efe0")
    save(art, f"{OUT}/lili.webp", max_w=300, quality=84)


def kuncup():
    W, H = 300, 380
    nx = Seq(61)
    art = blank(W, H)
    art = stem(art, W, H, [(120, 352), (124, 280), (128, 220)], 12, nx)
    art = calla(art, W, H, 128, 230, -math.pi / 2 + 0.1, 150, 130, nx, flip=1)
    save_prev(art, "kuncup", "#f6efe0")
    save(art, f"{OUT}/kuncup.webp", max_w=160, quality=84)


def daun():
    W, H = 520, 120
    nx = Seq(81)
    art = blank(W, H)
    art = stem(art, W, H, [(20, 70), (160, 62), (300, 64), (390, 58)], 6, nx)
    art = leaf(art, W, H, 150, 64, 120, math.pi + 0.28, nx, wd=0.16)
    art = leaf(art, W, H, 230, 64, 110, -0.25, nx, wd=0.16)
    art = calla(art, W, H, 384, 62, -0.1, 90, 78, nx, flip=1)
    gold = line(W, H, curve([(30, 82), (200, 80), (330, 84)], 30), 2.2, (0.1, 0.3))
    art = FO(art, gold, GOLD, seed=nx(), emboss=0.4)
    save_prev(art, "daun", "#f6efe0")
    save(art, f"{OUT}/daun.webp", max_w=420, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
