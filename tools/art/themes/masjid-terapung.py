"""Masjid Terapung — an original mosque standing on stilts over a calm sea at dusk: whitewashed prayer hall with lit
arched windows, a broad shallow dome, one slender minaret, a long boardwalk on piles, all mirrored in the water and
broken into long ripples; warm dusk sky. No figures. Run: python3 -I masjid-terapung.py [part ...]
parts: scene mosque water ripple window   Assets -> public/themes/art/masjid-terapung/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d2_lib import *

OUT = outdir("masjid-terapung")
PARTS = sys.argv[1:] or ["scene", "mosque", "water", "ripple", "window"]
SKY = [(0.0, "#24244c"), (0.2, "#41386c"), (0.38, "#7a5584"), (0.5, "#bf7280"), (0.57, "#ea9a6c"), (0.63, "#f7c27a"), (1.0, "#f7c27a")]
WALL, WALL_S, LIT, ROOF = "#f6e6d8", "#9a86a6", "#ffcf7a", "#e8d2c0"


def mosque(W, H, x0, wl, scale, nx, lit_side=-1):
    """Paint the mosque (RGBA, transparent) whose stilts stand in the water at y=wl. x0 = left of the hall."""
    s = scale
    art = blank(W, H)
    deck_y = wl - 34 * s
    hx0, hx1 = x0, x0 + 230 * s
    hall_top = deck_y - 92 * s
    # stilts and cross braces
    piles = []
    for px in np.arange(hx0 - 30 * s, hx1 + 34 * s, 16 * s):
        piles.append(([(px, deck_y), (px, wl + 4)], 4.2 * s, None))
    for px in np.arange(-40, hx0 - 30 * s, 26 * s):  # boardwalk piles
        piles.append(([(px, deck_y + 10 * s), (px, wl + 4)], 3.0 * s, None))
    pm = strokes(W, H, piles)
    art = GP(art, pm, "#4a3a52", "#2f2a3f", seed=nx(), rough=0.6)
    br = []
    for px in np.arange(hx0 - 30 * s, hx1 + 18 * s, 32 * s):
        br.append(([(px, deck_y + 4 * s), (px + 16 * s, wl - 6 * s)], 2.0 * s, None))
        br.append(([(px + 16 * s, deck_y + 4 * s), (px, wl - 6 * s)], 2.0 * s, None))
    art = GP(art, strokes(W, H, br), "#3b3048", seed=nx(), rough=0.5)
    # deck & boardwalk
    deck = rect(W, H, hx0 - 38 * s, deck_y - 6 * s, hx1 + 40 * s, deck_y + 4 * s)
    walk = poly(W, H, [(-40, deck_y + 4 * s), (hx0 - 38 * s, deck_y - 2 * s), (hx0 - 38 * s, deck_y + 6 * s), (-40, deck_y + 13 * s)])
    art = GP(art, np.maximum(deck, walk), "#6a5466", "#4a3a52", seed=nx(), rough=0.6)
    rail = strokes(W, H, [([(-40, deck_y - 6 * s), (hx0 - 38 * s, deck_y - 14 * s)], 1.6 * s, None)] + [([(x, deck_y + 4 * s - (x + 40) / (hx0 - 38 * s + 40) * 8 * s), (x, deck_y - 6 * s - (x + 40) / (hx0 - 38 * s + 40) * 8 * s)], 1.4 * s, None) for x in np.arange(-40, hx0 - 38 * s, 12 * s)])
    art = GP(art, rail, "#5a4658", seed=nx(), rough=0.4)
    # lanterns along the boardwalk
    lamps = [(x, deck_y - 22 * s - (x + 40) / (hx0 - 38 * s + 40) * 8 * s) for x in np.arange(10, hx0 - 50 * s, 46 * s)]
    art = GP(art, strokes(W, H, [([(x, y), (x, y + 18 * s)], 1.6 * s, None) for x, y in lamps]), "#3b3048", seed=nx(), rough=0.3)
    lm = circles(W, H, [(x, y, 3.2 * s) for x, y in lamps])
    art = over(art, glow(lm, "#ffb35a", radius=3 * s, strength=0.35))
    art = GP(art, lm, LIT, seed=nx(), rough=0.3)
    # prayer hall
    hall = rect(W, H, hx0, hall_top, hx1, deck_y - 6 * s)
    art = GP(art, hall, WALL, "#efd8c8", seed=nx(), rough=0.8, streak=0.5)
    # dusk light from the low sun on the left, cool shade on the right
    art = over(art, flat(hall * np.clip((np.arange(W)[None, :] - hx0) / (hx1 - hx0), 0, 1) ** 1.4, WALL_S, 0.55))
    art = over(art, flat(hall * light_mask(H, W, hx0 - 40 * s, hall_top, 200 * s), "#ffc48a", 0.35))
    # cornice band with small crenellations
    cor = rect(W, H, hx0 - 6 * s, hall_top - 8 * s, hx1 + 6 * s, hall_top + 2 * s)
    cren = shapes(W, H, [[(x, hall_top - 8 * s), (x + 3 * s, hall_top - 15 * s), (x + 6 * s, hall_top - 8 * s)] for x in np.arange(hx0 - 4 * s, hx1, 9 * s)], smooth=False)
    art = GP(art, np.maximum(cor, cren), ROOF, "#d8bcb0", seed=nx(), rough=0.5)
    art = over(art, flat(np.maximum(cor, cren) * np.clip((np.arange(W)[None, :] - hx0) / (hx1 - hx0), 0, 1), WALL_S, 0.5))
    # arched windows (lit)
    wins = []
    nwin = 6
    for k in range(nwin):
        cx = hx0 + (k + 0.5) * (hx1 - hx0) / nwin
        ww, wh = 9 * s, 44 * s
        y1 = deck_y - 20 * s
        y0 = y1 - wh
        wins.append([(cx - ww, y1), (cx - ww, y0 + ww)] + [(cx + math.cos(a) * ww, y0 + ww + math.sin(a) * ww * 1.5) for a in np.linspace(math.pi, math.tau, 12)] + [(cx + ww, y1)])
    wm = shapes(W, H, wins, smooth=False)
    art = over(art, glow(wm, "#ffae55", radius=7 * s, strength=0.35))
    art = GP(art, wm, LIT, "#ffb860", seed=nx(), rough=0.4)
    art = over(art, flat(wm * hatch(W, H, 0.0, 5 * s, 0.12, nx(), 0.1), "#c07a3a", 0.5))
    # dome on a drum
    dcx = (hx0 + hx1) / 2
    drum = rect(W, H, dcx - 58 * s, hall_top - 30 * s, dcx + 58 * s, hall_top - 6 * s)
    art = GP(art, drum, WALL, seed=nx(), rough=0.6)
    art = over(art, flat(drum * np.clip((np.arange(W)[None, :] - (dcx - 58 * s)) / (116 * s), 0, 1) ** 1.3, WALL_S, 0.5))
    dwins = shapes(W, H, [[(x - 3 * s, hall_top - 10 * s), (x - 3 * s, hall_top - 22 * s), (x, hall_top - 26 * s), (x + 3 * s, hall_top - 22 * s), (x + 3 * s, hall_top - 10 * s)] for x in np.arange(dcx - 48 * s, dcx + 50 * s, 12 * s)], smooth=False)
    art = GP(art, dwins, LIT, seed=nx(), rough=0.3)
    dome_pts = [(dcx + math.cos(a) * 64 * s, hall_top - 30 * s + math.sin(a) * 58 * s) for a in np.linspace(math.pi, math.tau, 40)]
    dome_pts = [(x, y - max(0, (1 - abs(x - dcx) / (64 * s))) ** 6 * 16 * s) for x, y in dome_pts]
    dome = shapes(W, H, [dome_pts], smooth=True)
    art = GP(art, dome, "#f3dccb", "#e8c8b8", seed=nx(), rough=0.7, streak=0.6)
    art = over(art, flat(dome * np.clip((np.arange(W)[None, :] - (dcx - 64 * s)) / (128 * s), 0, 1) ** 1.2, "#7d6c94", 0.6))
    art = over(art, flat(dome * light_mask(H, W, dcx - 40 * s, hall_top - 70 * s, 70 * s), "#ffd2a0", 0.5))
    ribs = strokes(W, H, [([(dcx + o * 64 * s * math.cos(t) * 0.98, hall_top - 30 * s - 58 * s * math.sin(t) * 0.98) for t in np.linspace(0, math.pi / 2, 14)], 1.2 * s, (0.1, 0.4)) for o in (-0.66, -0.33, 0.33, 0.66)])
    art = over(art, flat(ribs * dome, "#a58aa0", 0.35))
    fin = strokes(W, H, [([(dcx, hall_top - 102 * s), (dcx, hall_top - 124 * s)], 2.0 * s, None)])
    art = FO(art, np.maximum(fin, circles(W, H, [(dcx, hall_top - 108 * s, 4 * s)])), "#d9a84a", seed=nx(), emboss=0.6)
    # minaret at the right end
    mx = hx1 + 22 * s
    shaft = poly(W, H, [(mx - 10 * s, deck_y - 6 * s), (mx - 8 * s, hall_top - 120 * s), (mx + 8 * s, hall_top - 120 * s), (mx + 10 * s, deck_y - 6 * s)])
    art = GP(art, shaft, WALL, seed=nx(), rough=0.5)
    art = over(art, flat(shaft * np.clip((np.arange(W)[None, :] - (mx - 10 * s)) / (20 * s), 0, 1), WALL_S, 0.6))
    for by in (hall_top - 40 * s, hall_top - 120 * s):
        bal = rect(W, H, mx - 15 * s, by - 5 * s, mx + 15 * s, by + 2 * s)
        art = GP(art, bal, ROOF, seed=nx(), rough=0.4)
    lant = rect(W, H, mx - 7 * s, hall_top - 150 * s, mx + 7 * s, hall_top - 124 * s)
    art = GP(art, lant, WALL, seed=nx(), rough=0.4)
    art = over(art, glow(rect(W, H, mx - 4 * s, hall_top - 146 * s, mx + 4 * s, hall_top - 130 * s), "#ffb35a", radius=6 * s, strength=0.6))
    art = GP(art, rect(W, H, mx - 3 * s, hall_top - 146 * s, mx + 3 * s, hall_top - 130 * s), LIT, seed=nx(), rough=0.3)
    cap = shapes(W, H, [[(mx - 10 * s, hall_top - 150 * s)] + [(mx + math.cos(a) * 10 * s, hall_top - 150 * s + math.sin(a) * 14 * s) for a in np.linspace(math.pi, math.tau, 12)] + [(mx + 10 * s, hall_top - 150 * s)]], smooth=False)
    art = GP(art, cap, "#f3dccb", seed=nx(), rough=0.4)
    art = FO(art, strokes(W, H, [([(mx, hall_top - 162 * s), (mx, hall_top - 176 * s)], 1.6 * s, None)]), "#d9a84a", seed=nx(), emboss=0.5)
    sw = strokes(W, H, [([(mx - 2 * s, y), (mx - 2 * s, y + 10 * s)], 2 * s, None) for y in np.arange(hall_top - 108 * s, deck_y - 30 * s, 26 * s)])
    art = GP(art, sw, LIT, seed=nx(), rough=0.3)
    # small pavilion on the left of the deck
    px0 = hx0 - 34 * s
    pav = rect(W, H, px0, deck_y - 40 * s, px0 + 30 * s, deck_y - 6 * s)
    art = GP(art, pav, WALL, seed=nx(), rough=0.4)
    art = GP(art, rect(W, H, px0 + 8 * s, deck_y - 32 * s, px0 + 22 * s, deck_y - 8 * s), LIT, seed=nx(), rough=0.3)
    roofp = shapes(W, H, [[(px0 - 4 * s, deck_y - 40 * s), (px0 + 15 * s, deck_y - 58 * s), (px0 + 34 * s, deck_y - 40 * s)]], smooth=False)
    art = GP(art, roofp, "#e8c8b8", seed=nx(), rough=0.4)
    # soft edge outline in dusk violet
    allm = art[..., 3]
    art = over(art, flat(gaussian_filter(np.clip(outline(allm, 1.0), 0, 1), 0.6), "#4a3a52", 0.25))
    return art


def water_reflect(sky_and_far, layer, hz, wl, W, H, nx):
    """Water below hz: sky mirrored about the horizon + the mosque mirrored about its waterline, with ripples."""
    refl_sky = reflect(sky_and_far, hz, seed=nx(), amp=5, wl=5, fade=0.2, blur=1.6)
    refl_m = reflect(layer, wl, seed=nx(), amp=10, wl=3.5, fade=1.3, blur=1.4)
    return refl_sky, refl_m


if "scene" in PARTS:
    W, H = 600, 1300
    nx = Seq(600)
    HZ, WL = 820, 905
    sky = wet_sky(W, H, SKY + [], seed=51, blooms=0.5)
    # sun disc low on the horizon behind thin cloud bars
    sun = circles(W, H, [(150, HZ - 18, 34)]) * (np.arange(H)[:, None] < HZ - 4)
    sky = over(sky, glow(circles(W, H, [(150, HZ - 18, 60)]), "#ffb560", radius=70, strength=0.45))
    sky = over(sky, flat(gaussian_filter(sun, 1.5), "#ffd27e", 0.97))
    sky = over(sky, flat(gaussian_filter(sun, 1.5) * light_mask(H, W, 150, HZ, 40), "#ffb24a", 0.6))
    for (cy, x0, x1, w_, col) in [(HZ - 40, -40, 300, 7, "#c9707a"), (HZ - 20, 60, 420, 5, "#b8687a"), (HZ - 120, 200, 640, 14, "#a8688a"), (HZ - 260, -60, 360, 22, "#8a5a86"), (HZ - 380, 260, 680, 26, "#6a4f80"), (HZ - 560, -40, 420, 30, "#4e4378")]:
        m = strokes(W, H, [(curve([(x0, cy + 4), ((x0 + x1) / 2, cy - w_ * 0.3), (x1, cy)], 30), w_, (0.3, 0.45))])
        sky = G(sky, m, col, seed=cy, density=0.35, edge=0.25, bloom=0.6, rough=12, feather=6)
        rim = strokes(W, H, [(curve([(x0 + 20, cy + w_ * 0.45), ((x0 + x1) / 2, cy + w_ * 0.2), (x1 - 30, cy + w_ * 0.4)], 30), w_ * 0.25, (0.3, 0.4))])
        sky = over(sky, flat(gaussian_filter(rim, 1.5), "#ffb27a", 0.45 if cy > HZ - 300 else 0.2))
    clear()
    # faint distant coastline on the horizon
    coast = shapes(W, H, [[(-10, HZ + 1)] + [(x, HZ - 6 - 10 * math.exp(-((x - 470) / 70) ** 2) - 4 * math.sin(x / 40)) for x in range(-10, W + 20, 20)] + [(W + 10, HZ + 1)]], smooth=False)
    sky = G(sky, coast, "#6a4f7a", "#7a5f86", seed=nx(), density=0.6, edge=0.3, rough=1.5, feather=1)
    above = sky.copy()
    yy = np.arange(H)[:, None] * np.ones((1, W))
    above[..., 3] = (yy < HZ).astype(np.float32)
    m_layer = mosque(W, H, 250, WL, 1.0, nx)
    clear()
    rs, rm = water_reflect(above, m_layer, HZ, WL, W, H, nx)
    clear()
    water = (yy >= HZ).astype(np.float32)
    art = sky.copy()
    base = flat(water, "#3a3560", 1.0)
    art = over(art, base)
    rs[..., :3] = rs[..., :3] * 0.82 + col_arr("#3a3560") * 0.18
    rs[..., 3] *= 0.85
    art = over(art, rs)
    # darker water toward the viewer, slight cool tint
    art = over(art, flat(water * np.clip((yy - HZ) / (H - HZ), 0, 1) ** 1.2, "#232347", 0.55))
    rm[..., :3] = rm[..., :3] * 0.8 + col_arr("#3a3050") * 0.2
    rm[..., 3] *= 0.6
    art = over(art, rm)
    # long sun glitter path and ripple lines
    glit = ripple_lines(W, H, HZ + 2, H, nx(), 2.2, 10, 50) * light_mask(H, W, 150, HZ + 140, 260) ** 0.5
    art = over(art, flat(glit, "#ffd59a", 0.85))
    art = over(art, flat(ripple_lines(W, H, HZ + 2, H, nx(), 0.9, 30, 120) * water, "#c88a8a", 0.35))
    art = over(art, flat(ripple_lines(W, H, HZ + 40, H, nx(), 0.7, 40, 140) * water, "#1c1c3a", 0.45))
    art = over(art, m_layer)
    # lit window streaks on the water under the mosque
    streaks = []
    rng = np.random.default_rng(3)
    for k in range(6):
        cx = 250 + (k + 0.5) * 230 / 6
        for j in range(10):
            y = WL + 8 + j * 14 + rng.uniform(-3, 3)
            L = rng.uniform(6, 14) * (1 + j * 0.15)
            streaks.append(([(cx - L / 2, y), (cx + L / 2, y)], 1.6 + j * 0.15, (0.4, 0.4)))
    art = over(art, flat(strokes(W, H, streaks), "#ffc06a", 0.7))
    art = add_grain(art, 7, 0.012)
    art[..., 3] = 1
    preview(art, "mscene")
    save_rgb(art, f"{OUT}/scene.webp", quality=88)
    clear()

if "mosque" in PARTS:
    W, H = 640, 580
    nx = Seq(1600)
    WL = 360
    m_layer = mosque(W, H, 250, WL, 1.0, nx)
    clear()
    # crop the boardwalk to a short stub and fade its left end
    xx = np.arange(W)[None, :] * np.ones((H, 1))
    m_layer[..., 3] *= np.clip((xx - 120) / 80, 0, 1)
    rm = reflect(m_layer, WL, seed=nx(), amp=8, wl=3.5, fade=1.4, blur=1.2)
    rm[..., :3] = rm[..., :3] * 0.75 + col_arr("#5a4a70") * 0.25
    rm[..., 3] *= 0.55
    water = ellipses(W, H, [(370, WL + 40, 250, 56, 0)])
    art = G(blank(W, H), water, "#6a5a8a", "#c98a86", seed=nx(), density=0.5, edge=0.4, bloom=0.5, rough=8, feather=6)
    art = over(art, rm)
    art = over(art, flat(ripple_lines(W, H, WL + 2, WL + 100, nx(), 4, 10, 40) * water, "#ffd59a", 0.6))
    art = over(art, m_layer)
    preview(art, "mmosque", bg="#f6ece0")
    save(art, f"{OUT}/mosque.webp", max_w=420, quality=82)
    clear()

if "water" in PARTS:
    W, H = 600, 700
    nx = Seq(2000)
    art = wet_sky(W, H, [(0.0, "#e9a06e"), (0.2, "#b9727e"), (0.55, "#5b4677"), (1.0, "#2b2a52")], seed=61, blooms=0.4)
    art = over(art, flat(ripple_lines(W, H, 0, H, nx(), 1.6, 20, 110), "#ffd59a", 0.45))
    art = over(art, flat(ripple_lines(W, H, 0, H, nx(), 1.0, 30, 140), "#1c1c3a", 0.4))
    save_rgb(art, f"{OUT}/water.webp", quality=74)
    clear()

if "ripple" in PARTS:
    W, H = 460, 80
    nx = Seq(2400)
    art = blank(W, H)
    rings = []
    for k, (rx, ry) in enumerate([(40, 7), (90, 13), (150, 19), (210, 24)]):
        rings.append(([(230 + math.cos(a) * rx, 40 + math.sin(a) * ry) for a in np.linspace(0, math.tau, 80)], 2.6 - k * 0.45, None))
    rm = strokes(W, H, rings)
    art = G(art, rm, "#7a5f96", "#c98a86", seed=nx(), density=0.85, edge=0.5, rough=1.2, feather=0.6)
    art = over(art, glow(circles(W, H, [(230, 40, 8)]), "#ffc06a", radius=8, strength=0.6))
    art = GP(art, circles(W, H, [(230, 40, 5)]), "#ffd27e", seed=nx(), rough=0.3)
    preview(art, "mripple", bg="#f6ece0")
    save(art, f"{OUT}/ripple.webp", max_w=340, quality=84)
    clear()

if "window" in PARTS:
    W, H = 120, 160
    nx = Seq(2800)
    art = blank(W, H)
    cx = 60
    outer = shapes(W, H, [[(16, 150), (16, 56)] + [(cx + math.cos(a) * 44, 56 + math.sin(a) * 50) for a in np.linspace(math.pi, math.tau, 24)] + [(104, 150)]], smooth=False)
    inner = shapes(W, H, [[(28, 140), (28, 60)] + [(cx + math.cos(a) * 32, 60 + math.sin(a) * 38) for a in np.linspace(math.pi, math.tau, 24)] + [(92, 140)]], smooth=False)
    art = GP(art, outer, WALL, "#ecd6c6", seed=nx(), rough=0.6)
    art = over(art, flat(outer * np.clip((np.arange(W)[None, :] - 16) / 88, 0, 1), WALL_S, 0.45))
    art = over(art, glow(inner, "#ffae55", radius=8, strength=0.4))
    art = GP(art, inner, LIT, "#ffb860", seed=nx(), rough=0.4)
    art = over(art, flat(inner * hatch(W, H, 0.0, 9, 0.1, nx(), 0.1), "#c07a3a", 0.55))
    preview(art, "mwindow", bg="#2b2a52")
    save(art, f"{OUT}/window.webp", max_w=60, quality=84)
    clear()
