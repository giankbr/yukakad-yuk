"""Botol Attar — an Arabian perfume shop: coloured-glass attar bottles with gold filigree caps on a carved shelf,
a brass mabkhara with glowing oud chips and a separate smoke wisp (animated in CSS), scattered rose petals, a single
tall bottle and a gold filigree divider. No figures, no calligraphy.
Run: python3 -I botol-attar.py [part ...]   parts: rak mabkhara asap botol kelopak filigri
Assets -> public/themes/art/botol-attar/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t1_lib import *
from _jw_lib import spiral_pts

OUT = outdir("botol-attar")
PARTS = sys.argv[1:] or ["rak", "mabkhara", "asap", "botol", "kelopak", "filigri"]
GOLD, GOLD_D = "#c9a052", "#8a6424"
BRASS = "#b8862f"
WOOD, WOOD_D = "#4a2416", "#2e140c"
LINE = "#2a120c"
GLASS = {"emerald": "#1f7a5a", "ruby": "#a8243a", "sapphire": "#2a4ea0", "amber": "#d48a2a", "rose": "#c45a7a", "amethyst": "#6a3a8a"}

PROFILES = {
    "tear": ([(0, 20), (6, 32), (30, 40), (70, 34), (108, 18), (126, 8), (142, 6)], True),
    "globe": ([(0, 22), (4, 40), (30, 52), (60, 46), (80, 22), (88, 8), (116, 6)], True),
    "facet": ([(0, 26), (8, 36), (62, 36), (80, 20), (86, 8), (104, 7)], False),
    "amphora": ([(0, 14), (16, 26), (50, 34), (76, 30), (96, 14), (104, 7), (124, 6)], True),
    "small": ([(0, 16), (4, 26), (22, 30), (38, 22), (46, 7), (60, 6)], True),
}


def profile_poly(cx, by, prof, s=1.0):
    right = [(cx + w * s, by - h * s) for h, w in prof]
    left = [(cx - w * s, by - h * s) for h, w in prof[::-1]]
    return right + left


def bottle(art, W, H, cx, by, kind, col, s=1.0, seed=1, finial=1.0):
    prof, smooth = PROFILES[kind]
    top = prof[-1][0] * s
    neckw = prof[-1][1] * s
    body = shapes(W, H, [profile_poly(cx, by, prof, s)], smooth=smooth)
    # shadow + coloured light thrown on the shelf
    sh = ellipses(W, H, [(cx + 6 * s, by + 2, prof[2][1] * s * 1.2, 6 * s, 0)])
    art = OV(art, sh, lambda m: soft_shadow(m, "#000000", 4, 0.55, 0, 0), pad=20)
    art = OV(art, ellipses(W, H, [(cx - 4 * s, by + 4, prof[2][1] * s * 1.5, 7 * s, 0)]), lambda m: glow(m, mix(col, "#ffffff", 0.2), 8, 0.45), pad=30)
    art = OV(art, body, lambda m: glass(m, col, seed=seed), pad=10)
    # liquid line (attar oil sits lower, more saturated)
    lv = by - prof[2][0] * s * 1.2
    liq = body * (np.mgrid[0:H, 0:W][0] > lv)
    art = tint(art, gaussian_filter(liq, 1.0), mix(col, "#000000", 0.3), 0.35, pad=4)
    art = tint(art, strokes(W, H, [([(cx - prof[2][1] * s * 0.9, lv), (cx + prof[2][1] * s * 0.9, lv + 1)], 1.2, None)]), mix(col, "#ffffff", 0.5), 0.5, pad=2)
    # light: rim light on the right edge, window reflection on the left, caustic pool at the base, shoulder glint
    wmax = max(w for _, w in prof) * s
    art = tint(art, gaussian_filter(light_side(body, -3, 0, 1.2), 0.6), mix(col, "#ffffff", 0.65), 0.75, pad=3)
    art = tint(art, gaussian_filter(light_side(body, 0, -3, 1.2), 0.6) * (np.mgrid[0:H, 0:W][0] > by - 8 * s), mix(col, "#ffffff", 0.5), 0.6, pad=3)
    wx = cx - wmax * 0.52
    win = shapes(W, H, [[(wx - wmax * 0.08, by - prof[3][0] * s), (wx + wmax * 0.1, by - prof[3][0] * s + 6 * s), (wx + wmax * 0.12, by - 16 * s), (wx - wmax * 0.06, by - 22 * s)]]) * body
    art = tint(art, gaussian_filter(win, 2.5), "#fff6e8", 0.32, pad=6)
    art = highlight(art, [(wx - wmax * 0.02, by - prof[3][0] * s + 4 * s), (wx + wmax * 0.02, by - prof[2][0] * s), (wx + wmax * 0.04, by - 26 * s)], 2.0 * s, "#ffffff", 0.75)
    pool = ellipses(W, H, [(cx + wmax * 0.12, by - 12 * s, wmax * 0.5, 7 * s, 0)]) * body
    art = tint(art, gaussian_filter(pool, 4), mix(col, "#fff2c8", 0.55), 0.6, pad=8)
    # gold filigree: a band at the shoulder and a lace of small scallops hanging from it, dots below
    wy = by - prof[2][0] * s
    sy = by - prof[3][0] * s + 4 * s
    sw = [w for h_, w in prof if abs(by - h_ * s - sy) < 999][3] * s * 0.98
    band = strokes(W, H, [([(cx - sw, sy), (cx, sy + 3 * s), (cx + sw, sy)], 2.6 * s, None)])
    lace = []
    n = max(4, int(sw * 2 / (9 * s)))
    for k in range(n):
        xa = cx - sw * 0.92 + k * (sw * 1.84 / n); xb = xa + sw * 1.84 / n
        lace.append(([(xa + (xb - xa) * t, sy + 2 * s + math.sin(t * math.pi) * 7 * s) for t in np.linspace(0, 1, 8)], 1.3 * s, None))
    drops = circles(W, H, [(cx - sw * 0.92 + (k + 0.5) * (sw * 1.84 / n), sy + 13 * s, 1.5 * s) for k in range(n)])
    wb = strokes(W, H, [([(cx - wmax * 0.96, wy + 14 * s), (cx, wy + 18 * s), (cx + wmax * 0.96, wy + 14 * s)], 2.0 * s, None)])
    fil = np.clip((band + strokes(W, H, lace) + drops + wb) * np.clip(body * 1.2, 0, 1), 0, 1)
    art = FO(art, fil, GOLD, seed=seed + 1, emboss=0.4, sparkle=0.05)
    # collar + filigree cap + finial stopper
    ny = by - top
    collar = shapes(W, H, [[(cx - neckw - 3 * s, ny + 6 * s), (cx + neckw + 3 * s, ny + 6 * s), (cx + neckw + 4 * s, ny - 4 * s), (cx - neckw - 4 * s, ny - 4 * s)]], smooth=False)
    cap_h = 30 * s * finial
    capm = shapes(W, H, [[(cx - neckw - 5 * s, ny - 4 * s), (cx + neckw + 5 * s, ny - 4 * s), (cx + 3 * s, ny - cap_h * 0.55), (cx + 8 * s, ny - cap_h * 0.7), (cx + 1.5 * s, ny - cap_h), (cx, ny - cap_h - 8 * s), (cx - 1.5 * s, ny - cap_h), (cx - 8 * s, ny - cap_h * 0.7), (cx - 3 * s, ny - cap_h * 0.55)]])
    knob = circles(W, H, [(cx, ny - cap_h * 0.7, 6.5 * s)])
    gm = np.clip(collar + capm + knob, 0, 1)
    art = FO(art, gm, GOLD, seed=seed + 2, emboss=0.7, sparkle=0.06)
    art = tint(art, np.clip(outline(gm, 0.8) * 0.9, 0, 1), GOLD_D, 0.7, pad=2)
    # cap jewel
    art = OV(art, circles(W, H, [(cx, ny - cap_h * 0.7, 3.2 * s)]), lambda m: glass(m, col, seed=seed + 3, alpha=1), pad=4)
    art = highlight(art, [(cx - 1.4 * s, ny - cap_h * 0.7 - 1.5 * s), (cx - 0.6 * s, ny - cap_h * 0.7 - 2 * s)], 1.2 * s, "#ffffff", 0.9)
    # filigree hatch on cap
    art = tint(art, strokes(W, H, [([(cx - neckw - 3 * s + k * 3 * s, ny - 3 * s), (cx - neckw - 1 * s + k * 3 * s, ny + 5 * s)], 0.8 * s, None) for k in range(int((2 * neckw + 6 * s) / (3 * s)))]) * collar, GOLD_D, 0.5, pad=2)
    clear()
    return art


random.seed(51)

if "rak" in PARTS:
    W, H = 800, 440
    art = blank(W, H)
    shelf_y = 336
    # warm lamplight behind the bottles
    art = OV(art, ellipses(W, H, [(400, 250, 300, 120, 0)]), lambda m: glow(m, "#f3b86a", 60, 0.38), pad=200)
    # shelf board with carved scalloped apron
    board = shapes(W, H, [[(20, shelf_y), (780, shelf_y), (786, shelf_y + 22), (14, shelf_y + 22)]], smooth=False)
    apron = shapes(W, H, [[(30, shelf_y + 22)] + [(40 + k * 40 + 20 + 20 * math.cos(a), shelf_y + 22 + 22 * math.sin(a)) for k in range(18) for a in np.linspace(math.pi, 0, 7)[::-1][::-1]][:0] + [(770, shelf_y + 22)]], smooth=False)
    scal = []
    for k in range(19):
        x0 = 30 + k * 39.5
        scal.append([(x0, shelf_y + 20)] + [(x0 + 19.75 - 19.75 * math.cos(a), shelf_y + 20 + 26 * math.sin(a)) for a in np.linspace(0, math.pi, 10)] + [(x0 + 39.5, shelf_y + 20)])
    apron = shapes(W, H, scal)
    wm = np.clip(board + apron, 0, 1)
    art = OV(art, wm, lambda m: soft_shadow(m, "#000000", 10, 0.55, 0, 12), pad=40)
    art = paint(art, wm, WOOD, WOOD_D, lc=LINE, px=1.2, dens=0.8)
    art = G(art, light_side(board, 0, 4, 2), "#e8b070", seed=rs(), density=0.4, edge=0, bloom=0, rough=1)
    # inlay of brass dots in each scallop
    art = FO(art, circles(W, H, [(30 + k * 39.5 + 19.75, shelf_y + 34, 3.2) for k in range(19)]), BRASS, seed=3)
    art = FO(art, strokes(W, H, [([(24, shelf_y + 3), (776, shelf_y + 3)], 2.0, None)]), BRASS, seed=4)
    clear()
    lineup = [(92, "small", "amber", 1.15), (196, "tear", "emerald", 1.25), (318, "globe", "ruby", 1.3), (452, "amphora", "sapphire", 1.25),
              (568, "facet", "amethyst", 1.25), (680, "tear", "rose", 1.0), (748, "small", "emerald", 0.9)]
    for i, (x, kind, c, sc) in enumerate(lineup):
        art = bottle(art, W, H, x, shelf_y + 1, kind, GLASS[c], sc, seed=10 + i * 7, finial=1.0 + 0.2 * (i % 2))
    save(art, f"{OUT}/rak.webp", max_w=780, quality=80)
    prev(art, "ba_rak", bg="#3a1530")

if "botol" in PARTS:
    W, H = 160, 330
    art = blank(W, H)
    art = OV(art, ellipses(W, H, [(80, 200, 60, 90, 0)]), lambda m: glow(m, "#f3b86a", 30, 0.3), pad=60)
    art = bottle(art, W, H, 80, 310, "tear", GLASS["emerald"], 1.45, seed=71, finial=1.2)
    save(art, f"{OUT}/botol.webp", quality=84)
    prev(art, "ba_botol", bg="#3a1530")

if "mabkhara" in PARTS:
    W, H = 300, 360
    art = blank(W, H)
    cx = 150
    # silhouette parts (brass): feet, square base, pedestal, cup with flared rim
    feet = shapes(W, H, [[(cx - 70, 330), (cx - 54, 330), (cx - 56, 350), (cx - 68, 350)], [(cx + 54, 330), (cx + 70, 330), (cx + 68, 350), (cx + 56, 350)]], smooth=False)
    base = shapes(W, H, [[(cx - 78, 270), (cx + 78, 270), (cx + 74, 332), (cx - 74, 332)]], smooth=False)
    ped = shapes(W, H, [[(cx - 30, 272), (cx + 30, 272), (cx + 18, 230), (cx + 22, 214), (cx - 22, 214), (cx - 18, 230)]], smooth=False)
    cup = shapes(W, H, [[(cx - 80, 150), (cx + 80, 150), (cx + 70, 162), (cx + 50, 200), (cx + 26, 216), (cx - 26, 216), (cx - 50, 200), (cx - 70, 162)]])
    rim = shapes(W, H, [[(cx - 88, 140), (cx + 88, 140), (cx + 82, 154), (cx - 82, 154)]], smooth=False)
    brass = np.clip(feet + base + ped + cup + rim, 0, 1)
    art = OV(art, brass, lambda m: soft_shadow(m, "#000000", 8, 0.5, 4, 8), pad=30)
    art = FO(art, brass, BRASS, seed=5, emboss=0.8, sparkle=0.03)
    # shading: brass darker on the right, lit from upper left
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dark = brass * np.clip((xx - cx) / 90, 0, 1)
    art = tint(art, gaussian_filter(dark, 2), "#3a240c", 0.45, pad=4)
    art = tint(art, gaussian_filter(brass * np.clip((cx - 30 - xx) / 60, 0, 1) * (yy > 150), 3), "#fff0c0", 0.18, pad=4)
    # pierced filigree on the base face: rows of little arches + lozenges (dark holes with a warm glow inside)
    holes = []
    for row, y0 in enumerate([284, 306]):
        for k in range(7):
            x0 = cx - 60 + k * 20 + (row % 2) * 10
            holes.append([(x0 - 5, y0 + 12), (x0 - 5, y0 + 4), (x0, y0 - 2), (x0 + 5, y0 + 4), (x0 + 5, y0 + 12)])
    hm = shapes(W, H, holes) * base
    art = tint(art, hm, "#2a1206", 0.95, pad=2)
    art = OV(art, hm, lambda m: glow(m, "#ff9a3a", 2, 0.5), pad=6)
    loz = shapes(W, H, [[(x, 182), (x + 6, 175), (x + 12, 182), (x + 6, 189)] for x in range(cx - 52, cx + 46, 16)], smooth=False) * cup
    art = tint(art, loz, "#3a1a08", 0.85, pad=2)
    art = FO(art, strokes(W, H, [([(cx - 76, 160), (cx + 76, 160)], 1.6, None), ([(cx - 74, 276), (cx + 74, 276)], 1.6, None)]), "#e2b85a", seed=8)
    # glowing coal bed + oud chips heaped above the rim
    heap = shapes(W, H, [[(cx - 76, 142), (cx - 54, 124), (cx - 20, 114), (cx + 16, 112), (cx + 50, 120), (cx + 76, 140)]])
    art = OV(art, heap, lambda m: glow(m, "#ff7a2a", 12, 0.6), pad=40)
    art = paint(art, heap, "#3a1c12", "#20100a", lc=LINE, px=1.0, dens=0.6)
    rng = random.Random(4)
    chips = []
    for k in range(16):
        x = rng.uniform(cx - 60, cx + 58); y = rng.uniform(116, 138) + abs(x - cx) * 0.12
        a = rng.uniform(0, 3.14)
        L = rng.uniform(9, 16); w_ = rng.uniform(4, 7)
        chips.append([(x + math.cos(a) * L, y + math.sin(a) * L * 0.4), (x + math.cos(a + 1.6) * w_, y + math.sin(a + 1.6) * w_ * 0.5), (x - math.cos(a) * L, y - math.sin(a) * L * 0.4), (x - math.cos(a + 1.6) * w_, y - math.sin(a + 1.6) * w_ * 0.5)])
    cm = shapes(W, H, chips, smooth=False)
    art = paint(art, cm, "#5a3220", "#3e2014", lc=LINE, px=0.8, dens=0.7)
    ember = circles(W, H, [(rng.uniform(cx - 56, cx + 56), rng.uniform(124, 140), rng.uniform(1.5, 3)) for _ in range(14)])
    art = OV(art, ember, lambda m: glow(m, "#ffb347", 3, 1.2), pad=8)
    art = tint(art, ember, "#ffd27a", 1, pad=2)
    save(art, f"{OUT}/mabkhara.webp", quality=84)
    prev(art, "ba_mabkhara", bg="#3a1530")
    clear()

if "asap" in PARTS:
    W, H = 220, 420
    art = blank(W, H)
    rng = random.Random(9)
    items = []
    for k in range(5):
        x0 = 110 + rng.uniform(-14, 14)
        pts = [(x0 + 30 * math.sin(t * 5.5 + k * 1.3) * t + 16 * math.sin(t * 13 + k) * t, 410 - t * 400) for t in np.linspace(0, 1, 60)]
        items.append((pts, 12 + k * 3, (0.05, 0.6)))
    m = gaussian_filter(strokes(W, H, items[:3]), 7) * 1.1
    fade = np.clip(np.linspace(0.2, 1.0, H)[:, None] ** 0.8, 0, 1) * np.clip(np.linspace(0, 1, H)[:, None] * 2.5, 0, 1)
    fade = fade[::-1]
    m = m * fade
    sm = np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f4e6d8"), np.float32), np.clip(m * 0.75, 0, 1)[..., None]], -1)
    art = over(art, sm)
    save(art, f"{OUT}/asap.webp", quality=80)
    prev(art, "ba_asap", bg="#3a1530")

if "kelopak" in PARTS:
    W, H = 380, 220
    art = blank(W, H)
    rng = random.Random(6)
    spots = [(70, 150, 30, 0.4), (130, 110, 34, -0.8), (200, 160, 28, 1.6), (260, 100, 32, 2.6), (320, 160, 26, -2.0), (170, 70, 22, 0.9), (40, 80, 20, 2.0), (350, 70, 18, 1.0)]
    for i, (x, y, r, a) in enumerate(spots):
        pts = []
        for t in np.linspace(0, 2 * math.pi, 26)[:-1]:
            rr = r * (1 + 0.18 * math.cos(2 * t) - 0.22 * max(0, math.cos(t - math.pi)) ** 6 + rng.uniform(-0.03, 0.03))
            pts.append((x + math.cos(t + a) * rr, y + math.sin(t + a) * rr * 0.78))
        pm = shapes(W, H, [pts])
        col = ["#9e1c34", "#b8304a", "#8a1630", "#c44a62"][i % 4]
        art = G(art, pm, col, mix(col, "#5a0a1c", .4), seed=rs(), density=0.95, edge=0.6, bloom=0.3, rough=1.5)
        # curled lighter rim + a couple of veins
        art = G(art, light_side(pm, int(math.cos(a) * 4), int(math.sin(a) * 4), 2), "#f5b2b8", seed=rs(), density=0.45, edge=0, bloom=0, rough=0.8)
        vein = strokes(W, H, [([(x, y), (x + math.cos(a + d) * r * 0.7, y + math.sin(a + d) * r * 0.55)], 0.9, (0.1, 0.6)) for d in (-0.5, 0, 0.5)])
        art = tint(art, vein * pm, "#5a0a1c", 0.35, pad=2)
        clear()
    save(art, f"{OUT}/kelopak.webp", quality=82)
    prev(art, "ba_kelopak", bg="#3a1530")

if "filigri" in PARTS:
    W, H = 440, 64
    art = blank(W, H)
    cx, cy = 220, 32
    items = [([(cx - 200, cy), (cx - 40, cy)], 1.6, (0.3, 0)), ([(cx + 40, cy), (cx + 200, cy)], 1.6, (0, 0.3))]
    for k in (-1, 1):
        items.append((curve([(cx + k * 22, cy), (cx + k * 50, cy - 14), (cx + k * 80, cy - 4), (cx + k * 104, cy - 16)], 30), 2.2, (0, 0.3)))
        items.append((curve([(cx + k * 22, cy), (cx + k * 50, cy + 14), (cx + k * 80, cy + 4), (cx + k * 104, cy + 16)], 30), 2.2, (0, 0.3)))
        items.append((spiral_pts(cx + k * 110, cy - 12, 1.5, 9, math.pi if k > 0 else 0, 1.2, 30, -k), 1.8, (0, 0.2)))
        items.append((spiral_pts(cx + k * 110, cy + 12, 1.5, 9, math.pi if k > 0 else 0, 1.2, 30, k), 1.8, (0, 0.2)))
    m = strokes(W, H, items)
    m = np.maximum(m, shapes(W, H, [[(cx, cy - 16), (cx + 13, cy), (cx, cy + 16), (cx - 13, cy)]], smooth=False))
    m = np.maximum(m, circles(W, H, [(cx + k * d, cy, 2.4) for k in (-1, 1) for d in (140, 160, 180)]))
    art = FO(art, m, GOLD, seed=4, emboss=0.6, sparkle=0.05)
    art = OV(art, shapes(W, H, [[(cx, cy - 8), (cx + 6, cy), (cx, cy + 8), (cx - 6, cy)]], smooth=False), lambda mm: glass(mm, GLASS["ruby"], seed=2, alpha=1), pad=4)
    save(art, f"{OUT}/filigri.webp", quality=86)
    prev(art, "ba_filigri", bg="#3a1530")

kb(OUT)
