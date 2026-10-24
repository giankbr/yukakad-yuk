"""Lurik Klaten — hand-woven lurik (ATBM) stripes and rural Klaten: Merapi at dawn over terraced sawah, a bamboo
jemuran with three lurik cloths drying, a woven-tape divider, a wooden shuttle (teropong) and thread spool.
Run: python3 -I lurik-klaten.py [part ...]   parts: tile desa kain pita teropong kelos
Assets -> public/themes/art/lurik-klaten/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s2_lib import *

OUT = outdir("lurik-klaten")
PARTS = sys.argv[1:] or ["tile", "desa", "kain", "pita", "teropong", "kelos"]
INDIGO, INDIGO_D = "#2d3b5e", "#1c2742"
SOGA, SOGA_D = "#7a4e2c", "#563420"
CREAM, CREAM_D = "#ece0c4", "#d8c7a2"
BLACK = "#211c19"
RUST = "#a4512e"
LINE = "#3a2c22"

# stripe recipes (thread counts, colour). Lurik names are evocative only.
TELUH = [(6, CREAM), (2, BLACK), (3, CREAM), (2, BLACK), (6, CREAM), (14, INDIGO), (2, CREAM), (4, INDIGO), (2, CREAM), (14, INDIGO)]
SOGAN = [(10, SOGA), (2, CREAM), (2, SOGA), (2, CREAM), (10, SOGA), (3, BLACK), (5, CREAM_D), (3, BLACK)]
KLASIK = [(3, BLACK), (9, CREAM), (1, RUST), (2, CREAM), (1, RUST), (9, CREAM), (3, BLACK), (6, INDIGO)]


def up2(arr):
    """Thread-level detail: each thread = 2 px (render at half size, nearest-upscale, soften a touch)."""
    a = np.repeat(np.repeat(arr, 2, 0), 2, 1)
    a[..., :3] = gaussian_filter(a[..., :3], (0.45, 0.45, 0))
    return a


random.seed(11)

if "tile" in PARTS:
    # seamless page/band tile: indigo-cream lurik (period of the stripe recipe divides the width)
    per = sum(w for w, _ in TELUH)          # 55 threads
    cloth = lurik_cloth(per * 4, 128, TELUH, seed=5, weft="#e6d8b8")
    tile = up2(cloth)
    save_full(tile, f"{OUT}/lurik.webp", quality=80)
    per2 = sum(w for w, _ in SOGAN)
    c2 = lurik_cloth(per2 * 5, 120, SOGAN, seed=9, weft="#d9c39a")
    save_full(up2(c2), f"{OUT}/sogan.webp", quality=78)
    prev(tile, "lk_tile")

if "pita" in PARTS:
    # woven tape divider: narrow strip of klasik lurik with frayed thread fringes at both ends
    rng = random.Random(4)
    W, H = 460, 44
    per = sum(w for w, _ in KLASIK)
    PITA = [(2, BLACK), (3, CREAM), (4, INDIGO), (1, CREAM), (2, RUST), (1, CREAM), (4, INDIGO), (3, CREAM), (2, BLACK)]
    cloth = up2(lurik_cloth(H // 2, W // 2, PITA, seed=12, weft="#efe3c8"))  # rotated: stripes run along the tape
    cloth = np.ascontiguousarray(np.transpose(cloth, (1, 0, 2)))[:H, :W]
    Hh, Ww = cloth.shape[:2]
    m = shapes(Ww, Hh, [[(40, 6), (Ww - 40, 7), (Ww - 38, Hh - 7), (42, Hh - 6)]], smooth=False)
    m = np.clip(gaussian_filter(displace(m, 3, 1.5, 12), 0.6) * 1.3, 0, 1)
    art = cloth.copy(); art[..., 3] = m
    # fringes: loose threads
    fr = []
    for side in (0, 1):
        for k in range(16):
            y = 8 + k * 1.8
            x0 = 42 if side == 0 else Ww - 40
            L = rng.uniform(14, 34)
            d = -1 if side == 0 else 1
            fr.append((curve([(x0, y), (x0 + d * L * .5, y + rng.uniform(-3, 3)), (x0 + d * L, y + rng.uniform(-6, 6))], 8), 1.3, (0, .4)))
    fm = strokes(Ww, Hh, fr)
    art = OV(art, fm, lambda mm: np.concatenate([np.ones(mm.shape + (3,), np.float32) * np.array(hex_rgb("#d9c7a3"), np.float32), mm[..., None] * 0.95], -1), pad=4)
    art = G(art, fm, "#8c7552", seed=rs(), density=0.35, edge=0, bloom=0, rough=0.3, feather=0.3, pad=4)
    # soft shadow under the tape edges
    art = G(art, np.clip(m - np.roll(m, -2, 0), 0, 1), BLACK, seed=rs(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.4, pad=4)
    save(art, f"{OUT}/pita.webp", quality=84)
    prev(art, "lk_pita")

if "desa" in PARTS:
    # cover scene: Merapi at dawn, foothills, terraced sawah with water, palms + a small limasan roof, path
    W, H = 780, 700
    rng = random.Random(21); nx = Seq(2100)
    art = painted_sky(W, H, [(0, "#d3dcdf"), (0.28, "#ece1c8"), (0.42, "#f3dcb2"), (1, "#efe0c0")], seed=3, streak=0.35, grain=0.25)
    # sun haze behind the mountain
    art = OV(art, circles(W, H, [(560, 150, 44)]), lambda m: glow(m, "#fff3d2", 30, 0.9), pad=90)
    art = GP(art, circles(W, H, [(560, 150, 30)]), "#f8e7bf", "#f3d9a4", seed=nx(), rough=1.0, pad=8)
    # Merapi: broad cone, slightly lopsided summit with a lava-dome notch
    mer = [(-20, 400), (120, 330), (250, 250), (330, 186), (366, 160), (378, 152), (392, 158), (404, 150), (420, 160), (462, 196),
           (540, 262), (660, 330), (800, 380), (800, 470), (-20, 470)]
    mm = shapes(W, H, [deform(mer, rng, 2, 0.02)])
    art = paint(art, mm, "#8f9cad", "#7b889c", ln=False, streak=0.9)
    # ridges/ravines (barranco) washes down the flanks
    rid = []
    for k in range(9):
        x0 = 340 + k * 9; a = 0.9 + (k - 4) * 0.14
        rid.append((curve([(x0, 170 + abs(k - 4) * 4), (x0 + math.cos(a) * 90 * (k - 4) / 4 + rng.uniform(-10, 10), 260), (x0 + (k - 4) * 48, 360)], 20), 6, (0.1, 0.5)))
    art = shade(art, strokes(W, H, rid) * mm, "#69768c", 0.4)
    # light side (sun from the right)
    art = G(art, light_side(mm, -14, 0, 6) * (np.linspace(0, 1, W)[None, :] > 0.48), "#c9cbd0", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=3)
    # summit smoke plume drifting left
    plume = shapes(W, H, [curve([(388, 150), (370, 120), (330, 96), (270, 84), (230, 92), (262, 104), (320, 112), (360, 130), (392, 152)], 30)])
    art = G(art, plume, "#fbf8f2", "#e2ded8", seed=nx(), density=0.85, edge=0.25, bloom=0.5, rough=7)
    art = G(art, plume * light_side(plume, 0, 6, 4), "#b9b9bd", seed=nx(), density=0.3, edge=0.1, bloom=0.4, rough=5)
    clear()
    # Merbabu-ish far hill on the left in haze
    art = shade(art, hills(W, H, 360, 40, 7, 0.9) * (np.linspace(1, 0, W)[None, :] ** 1.5), "#a9b2b5", 0.35)
    # foothills band
    fh = hills(W, H, 410, 18, 13, 0.7)
    art = paint(art, fh, "#7d9268", "#6a8259", ln=False)
    # tree lines on foothills
    trees = []
    for k in range(48):
        x = rng.uniform(-10, W + 10); y = 404 - 16 * math.sin(x / 120) + rng.uniform(-4, 8)
        trees.append(deform(ellipse_pts(x, y, rng.uniform(9, 16), rng.uniform(8, 13), 10), rng, 1, .1))
    tm = shapes(W, H, trees)
    art = paint(art, tm, "#58704c", "#46603f", ln=False)
    art = G(art, light_side(tm, -3, 3, 2), "#93a77a", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=1)
    # palms
    for (x, by, h, ln_) in [(90, 470, 150, 0.12), (138, 474, 120, -0.08), (700, 476, 170, -0.1), (650, 480, 110, 0.1)]:
        pm = np.clip(gaussian_filter(palm(W, H, x, by, h, rng, ln_), 1.2) * 2.2, 0, 1)
        art = paint(art, pm, "#4b5f3e", "#3b4e33", ln=False)
    # a small limasan roof among the trees (village)
    roof = shapes(W, H, [[(214, 446), (240, 426), (290, 426), (316, 446)]], smooth=False)
    wall = shapes(W, H, [[(224, 446), (306, 446), (306, 466), (224, 466)]], smooth=False)
    art = paint(art, wall, "#d8c39b", px=1.0, dens=0.4)
    art = paint(art, roof, "#9a5a38", "#7d4529", px=1.0, dens=0.5)
    art = shade(art, strokes(W, H, [([(226 + k * 9, 446), (242 + k * 6.5, 428)], 1.2, None) for k in range(10)]) * roof, "#5d3220", 0.4)
    clear()
    # terraced sawah: curved bands with water sheen and rice rows
    ys = [470, 500, 536, 580, 634, 700]
    greens = [("#9fb36d", "#8aa35c"), ("#b6c47c", "#9fb36d"), ("#8faa5e", "#7a964e"), ("#a8be70", "#93ab60"), ("#86a257", "#6f8c47")]
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]
        top = [(x, y0 + 8 * math.sin(x / 140 + i) + 4 * math.sin(x / 47 + i * 2)) for x in range(-20, W + 30, 20)]
        band = shapes(W, H, [top + [(W + 20, H + 20), (-20, H + 20)]], smooth=False)
        c1, c2 = greens[i]
        art = paint(art, band, c1, c2, ln=False, streak=0.9)
        # pematang (dike) line along the top edge
        art = G(art, strokes(W, H, [(top, 3.2, None)]), "#5f6b3a", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=1.2, pad=6)
        # rows of young rice: short vertical ticks in perspective
        ticks = []
        gap = 6 + i * 3
        for x in range(-10, W + 10, gap):
            for j in range(2 + i):
                yy = y0 + 10 + j * (y1 - y0 - 10) / (2 + i) + 8 * math.sin(x / 140 + i)
                if yy < y1 - 4:
                    ticks.append(([(x + rng.uniform(-1, 1), yy), (x + rng.uniform(-1.5, 1.5), yy - 3 - i * 1.6)], 1.2 + i * 0.35, (0, .5)))
        art = shade(art, strokes(W, H, ticks) * band, mix(c2, "#3f5a2c", .5), 0.55)
        # flooded patch reflecting the sky in the second and third terrace
        if False:
            wat = shapes(W, H, [deform([(120 + i * 230, y0 + 14), (300 + i * 230, y0 + 16), (290 + i * 230, y1 - 8), (130 + i * 230, y1 - 10)], rng, 2, 0.06)])
            wat = wat * band
            art = G(art, wat, "#dfe3d8", "#f0e6cc", seed=nx(), density=0.7, edge=0.4, bloom=0.3, rough=4)
            art = shade(art, strokes(W, H, [([(130 + i * 230 + k * 16, y0 + 18 + (k % 3) * 6), (150 + i * 230 + k * 16, y0 + 18 + (k % 3) * 6)], 1.4, None) for k in range(10)]) * wat, "#8ea07a", 0.4)
    clear()
    # foot path curving through the fields
    pth = curve([(330, H + 10), (360, 650), (420, 590), (400, 540), (430, 500)], 60)
    Lp, Rp = [], []
    for k, (x, y) in enumerate(pth):
        wd = 2 + (y - 490) / 210 * 22
        Lp.append((x - wd, y)); Rp.append((x + wd, y))
    path = shapes(W, H, [Lp + Rp[::-1]])
    art = paint(art, path, "#d9c49a", "#c9ae7e", ln=False)
    # fade the bottom into the page cream
    a = np.ones((H, W), np.float32)
    a[-120:] = np.linspace(1, 0, 120)[:, None] ** 1.3
    art[..., 3] *= a
    art = add_grain(art, 5, 0.035)
    save_full(art, f"{OUT}/desa.webp", size=(780, 700), quality=74)
    prev(art, "lk_desa", bg="#efe4cc")

if "kain" in PARTS:
    # bamboo jemuran (pole on two crossed posts) with three lurik cloths drying, hanging over the pole
    W, H = 560, 520
    rng = random.Random(31); nx = Seq(3100)
    art = blank(W, H)
    pole_y = lambda x: 58 + (x - 20) * 0.035
    # posts (crossed bamboo X at both ends)
    posts = strokes(W, H, [([(10, 500), (54, 30)], 10, None), ([(66, 500), (22, 30)], 10, None),
                           ([(510, 500), (548, 44)], 10, None), ([(556, 500), (520, 44)], 10, None)])
    art = paint(art, posts, "#b89a5a", "#9c7f45", px=1.2, dens=0.6, lc=LINE)
    nodes = strokes(W, H, [([(x - 6, y), (x + 6, y)], 2.4, None) for (x, y) in [(28, 300), (46, 180), (40, 420), (530, 300), (536, 170), (528, 420)]])
    art = shade(art, nodes * posts, "#6d5530", 0.6)
    cloths = [  # x0, x1, hang length, recipe, seed, extra fold count
        (78, 214, 380, TELUH, 41, 5),
        (226, 352, 300, SOGAN, 42, 4),
        (366, 500, 420, KLASIK, 43, 5),
    ]
    for (x0, x1, L, recipe, sd, folds) in cloths:
        w = x1 - x0
        # cloth texture: stripes vertical (warp hangs down)
        tex = up2(lurik_cloth(w // 2 + 2, L // 2 + 4, recipe, seed=sd, weft="#e6d6b4"))
        tex = tex[:L + 4, :w + 2]
        th, tw = tex.shape[:2]
        # place into canvas with a soft sag/folds displacement
        canvas = blank(W, H)
        yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
        wave = np.sin(xx / tw * math.pi * folds + sd) * 6 * (yy / th)
        src = np.stack([map_coordinates(tex[..., c], [yy, np.clip(xx + wave, 0, tw - 1)], order=1) for c in range(4)], -1)
        # fold shading: vertical light/dark bands
        fold = 1 + 0.27 * np.sin(xx / tw * math.pi * folds * 2 + sd * 1.3) * (0.4 + 0.6 * yy / th)
        # front layer slightly darker near the pole (shadow of the over-fold)
        fold *= 1 - 0.18 * np.exp(-yy / 18)
        src[..., :3] = np.clip(src[..., :3] * fold[..., None], 0, 1)
        ty0 = int(pole_y((x0 + x1) / 2)) - 4
        canvas[ty0:ty0 + th, x0:x0 + tw] = src[: H - ty0, : W - x0]
        # silhouette: slightly uneven hem, narrower over the pole
        hem = [(x0 + 2, ty0 + 4)] + [(x0 + w * t, ty0 + L - 6 + 8 * math.sin(t * 7 + sd) + rng.uniform(-2, 2)) for t in np.linspace(0, 1, 14)] + [(x1 - 2, ty0 + 4)]
        sil = shapes(W, H, [[(x0 + 4, ty0), (x1 - 4, ty0)] + hem[::-1][1:-1] + []], smooth=False)
        sil = shapes(W, H, [[(x0 + 4, ty0)] + hem[1:-1] + [(x1 - 4, ty0)]], smooth=False)
        sil = np.clip(gaussian_filter(displace(sil, sd, 1.4, 14), 0.6) * 1.4, 0, 1)
        canvas[..., 3] = sil * canvas[..., 3]
        # short back layer peeking above the pole (cloth folded over)
        back = shapes(W, H, [[(x0 + 6, ty0 - 2), (x1 - 6, ty0 - 2), (x1 - 8, ty0 + 30), (x0 + 8, ty0 + 30)]], smooth=False)
        art = GP(art, back * 0, CREAM, seed=nx())
        art = over(art, canvas)
        # outline + side shadow
        art = line(art, sil, 1.2, 0.55, LINE)
        art = G(art, sil * light_side(sil, 10, 0, 6), BLACK, seed=nx(), density=0.22, edge=0.1, bloom=0.3, rough=3)
        # fringe at the hem (warp ends)
        fr = []
        for t in np.linspace(0.04, 0.96, 26):
            x = x0 + w * t; y = ty0 + L - 6 + 8 * math.sin(t * 7 + sd)
            fr.append(([(x, y - 2), (x + rng.uniform(-2, 2), y + rng.uniform(10, 18))], 1.6, (0, .5)))
        fm = strokes(W, H, fr)
        art = G(art, fm, "#6d5a44", "#a08b6a", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.6, feather=0.4, pad=6)
    # bamboo pole on top
    pole = strokes(W, H, [([(4, pole_y(4)), (W - 4, pole_y(W - 4))], 13, None)])
    art = paint(art, pole, "#c9ab68", "#a98b4c", px=1.2, dens=0.65, lc=LINE)
    art = G(art, strokes(W, H, [([(4, pole_y(4) - 3), (W - 4, pole_y(W - 4) - 3)], 3, None)]), "#efdca6", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    art = shade(art, strokes(W, H, [([(x, pole_y(x) - 6), (x, pole_y(x) + 6)], 2.2, None) for x in (120, 290, 440)]), "#6d5530", 0.6)
    art = add_grain(art, 9, 0.03)
    save(art, f"{OUT}/kain.webp", max_w=560, quality=80)
    prev(art, "lk_kain", bg="#efe4cc")

if "teropong" in PARTS:
    # ATBM shuttle (teropong): boat-shaped wooden shuttle with a bobbin of indigo thread and a trailing thread
    W, H = 400, 150
    rng = random.Random(51); nx = Seq(5100)
    art = blank(W, H)
    body = shapes(W, H, [[(30, 76), (90, 52), (200, 46), (310, 52), (370, 76), (310, 98), (200, 104), (90, 98)]])
    art = paint(art, body, "#b07a45", "#8a5a30", px=1.3, dens=0.7, lc=LINE)
    art = G(art, light_side(body, 0, -6, 4), "#5d3a1e", seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=2)
    art = G(art, strokes(W, H, [(curve([(60, 70), (200, 58), (340, 70)], 20), 3, None)]) * body, "#e7c08a", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.8)
    # wood grain
    gr = [(curve([(70, 68 + k * 6), (200, 60 + k * 7 + rng.uniform(-2, 2)), (330, 68 + k * 6)], 20), 0.9, None) for k in range(5)]
    art = shade(art, strokes(W, H, gr) * body, "#6e4424", 0.4)
    # cavity with bobbin
    cav = shapes(W, H, [deform(ellipse_pts(200, 75, 74, 17, 16), rng, 1, .03)])
    art = paint(art, cav, "#3c2412", "#2a180c", px=1.0, dens=0.4)
    bob = shapes(W, H, [[(140, 66), (260, 66), (262, 86), (138, 86)]])
    art = paint(art, bob, INDIGO, INDIGO_D, px=1.0, dens=0.5)
    wraps = strokes(W, H, [([(142 + k * 4, 66), (146 + k * 4, 86)], 1.1, None) for k in range(30)]) * bob
    art = shade(art, wraps, "#5a6b94", 0.55)
    # metal tips
    for (x, d) in ((30, 1), (370, -1)):
        tip = shapes(W, H, [[(x, 76), (x + d * 26, 66), (x + d * 26, 86)]], smooth=False)
        art = paint(art, tip, "#c8c2b2", "#9a9384", px=1.0, dens=0.5)
    # trailing thread
    th = strokes(W, H, [(curve([(262, 76), (300, 112), (350, 128), (396, 118)], 30), 1.8, (0, .3))])
    art = G(art, th, INDIGO, seed=nx(), density=0.85, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    art = add_grain(art, 3, 0.03)
    save(art, f"{OUT}/teropong.webp", max_w=300, quality=84)
    prev(art, "lk_teropong")

if "kelos" in PARTS:
    # thread spool (kelos) with brown soga thread
    W, H = 120, 150
    rng = random.Random(61); nx = Seq(6100)
    art = blank(W, H)
    for y in (22, 128):
        art = paint(art, shapes(W, H, [ellipse_pts(60, y, 40, 11, 18)]), "#c49a62", "#a07a48", px=1.0, dens=0.6, lc=LINE)
    core = shapes(W, H, [[(30, 26), (90, 26), (90, 124), (30, 124)]], smooth=False)
    art = paint(art, core, SOGA, SOGA_D, px=1.2, dens=0.6, lc=LINE)
    wr = strokes(W, H, [([(30, 28 + k * 3.2), (90, 30 + k * 3.2)], 1.2, None) for k in range(30)]) * core
    art = shade(art, wr, "#3e2414", 0.5)
    art = G(art, core * (np.linspace(1, 0, W)[None, :] < 0.35), "#b9845a", seed=nx(), density=0.4, edge=0, bloom=0.2, rough=2)
    art = paint(art, shapes(W, H, [ellipse_pts(60, 22, 40, 11, 18)]), "#d6b07a", "#b89060", px=1.0, dens=0.6, lc=LINE)
    art = paint(art, shapes(W, H, [ellipse_pts(60, 22, 8, 3, 10)]), "#4a3018", ln=False)
    art = add_grain(art, 4, 0.03)
    save(art, f"{OUT}/kelos.webp", max_w=90, quality=84)
    prev(art, "lk_kelos")

kb(OUT)
