"""Sarung Samarinda — hand-woven silk sarung on a gedokan (back-strap) loom and the wide Mahakam river at dusk.
Parts: kotak (seamless silk check tile), kepala (denser head-panel check tile), gedokan (loom: carved beam, warp
threads, reed, half-woven check cloth, shuttle), mahakam (river panorama: far bank, stilt houses, a domed mosque
silhouette, a tug pulling a coal barge, ketinting boats), ces (small long boat), benang (silk skein).
Run: python3 -I sarung-samarinda.py [part ...]  Assets -> public/themes/art/sarung-samarinda/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t1_lib import *

OUT = outdir("sarung-samarinda")
PARTS = sys.argv[1:] or ["kotak", "kepala", "gedokan", "mahakam", "ces", "benang"]
MAROON, MAROON_D, OX = "#5a1420", "#3e0c16", "#7a1f2b"
BLACK = "#16100f"
GOLD, GOLD_L = "#c8973a", "#e6c178"
TEAL = "#1e5f5e"
CREAM = "#efe2c4"
WOOD, WOOD_D, WOOD_L = "#7b4a2a", "#4e2c18", "#a9714a"
LINE = "#2a1612"

# sarung check recipe (threads): maroon ground, black bars, fine gold and teal lines
CHECK = [(10, MAROON), (2, GOLD), (2, MAROON), (6, BLACK), (2, MAROON), (1, TEAL), (1, TEAL), (2, MAROON), (6, BLACK), (2, MAROON), (2, GOLD), (10, MAROON), (4, OX)]
HEAD = [(3, BLACK), (2, GOLD), (3, BLACK), (4, OX), (1, CREAM), (4, OX), (3, BLACK), (2, TEAL), (3, BLACK), (4, MAROON)]

random.seed(41)

if "kotak" in PARTS:
    per = sum(n for n, _ in CHECK)  # 50 threads
    T = per * 2 * 2   # two repeats, 2 px per thread
    cl = check_cloth(T, T, CHECK, CHECK, seed=3, sheen=0.0, tight=2)
    save_full(cl, f"{OUT}/kotak.webp", quality=80)
    prev(cl, "ss_kotak")

if "kepala" in PARTS:
    per = sum(n for n, _ in HEAD)  # 29
    T = per * 2 * 3
    cl = check_cloth(T, T, HEAD, HEAD[::-1], seed=5, sheen=0.0, tight=2)
    save_full(cl, f"{OUT}/kepala.webp", quality=80)
    prev(cl, "ss_kepala")


def wood(art, mask, seed, col=WOOD, col2=WOOD_D, grain_dir=0):
    H, W = mask.shape
    art = paint(art, mask, col, col2, lc=LINE, px=1.2, dens=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = fbm(W, H, seed, 40, 3)
    u = (yy if grain_dir == 0 else xx) / 3.0 + n * 9
    g = np.clip((0.18 - np.abs((u % 1.0) - 0.5)) * 4, 0, 1) * mask
    art = tint(art, g, WOOD_D, 0.35, pad=2)
    return art


if "gedokan" in PARTS:
    W, H = 780, 560
    rng = random.Random(3)
    art = blank(W, H)
    # warp threads: from the beam (y=86) down to the cloth (y=340), converging slightly
    seq = []
    for n, c in CHECK * 3:
        seq += [c] * n
    xs_top = np.linspace(70, 710, 150); xs_bot = np.linspace(96, 684, 150)
    cols = {}
    for i in range(150):
        c = seq[(i * 2) % len(seq)]
        cols.setdefault(c, []).append(([(xs_top[i], 92), ((xs_top[i] + xs_bot[i]) / 2 + rng.uniform(-0.6, 0.6), 220), (xs_bot[i], 344)], 1.7, None))
    for c, items in cols.items():
        m = strokes(W, H, items)
        art = tint(art, m, mix(c, "#ffffff", 0.12) if c in (BLACK,) else c, 0.95, pad=2)
    clear()
    # shed: alternate threads lifted -> faint lighter sheen on every other thread near the reed
    sheen = strokes(W, H, [([(xs_top[i], 120), (xs_bot[i], 330)], 0.8, None) for i in range(0, 150, 2)])
    art = tint(art, sheen, "#ffffff", 0.12, pad=2)
    # reed (sisir): thin wooden frame with fine teeth
    reed = shapes(W, H, [[(82, 236), (698, 236), (698, 246), (82, 246)], [(82, 270), (698, 270), (698, 280), (82, 280)]], smooth=False)
    art = wood(art, reed, 7, WOOD_L, WOOD, 1)
    teeth = strokes(W, H, [([(x, 246), (x, 270)], 0.9, None) for x in np.arange(86, 696, 4.2)])
    art = tint(art, teeth, WOOD_D, 0.6, pad=2)
    # woven cloth (rotate slightly as if pulled toward the weaver)
    ch = check_cloth(640, 230, CHECK, CHECK, seed=9, sheen=0.22, tight=2)
    cloth = blank(W, H)
    cloth[336:336 + 230, 70:710] = ch[:H - 336, :640]
    cm = shapes(W, H, [[(96, 340), (684, 340), (710, 560), (70, 560)]], smooth=False)
    cm = np.clip(gaussian_filter(displace(cm, 4, 1.2, 10), 0.5), 0, 1)
    cloth[..., 3] = cm
    # fold shading across the cloth (soft drape)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fold = 0.85 + 0.15 * np.sin(xx / 46 + 0.6) * np.clip((yy - 340) / 200, 0, 1)
    cloth[..., :3] *= fold[..., None]
    art = over(art, cloth)
    # fell line: beaten edge where weaving stopped
    art = tint(art, strokes(W, H, [([(96, 341), (684, 341)], 3.0, None)]), BLACK, 0.55, pad=2)
    # shuttle (teropong) resting on the cloth
    sh = shapes(W, H, [[(250, 420), (300, 402), (520, 398), (580, 410), (520, 424), (300, 428)]])
    art = OV(art, sh, lambda m: soft_shadow(m, "#000000", 6, 0.45, 4, 8), pad=30)
    art = wood(art, sh, 11, WOOD_L, WOOD, 1)
    bob = shapes(W, H, [[(360, 405), (460, 404), (460, 418), (360, 419)]], smooth=False)
    art = paint(art, bob, GOLD, GOLD_L, lc=LINE, px=1.0)
    art = tint(art, strokes(W, H, [([(360 + k * 6, 405), (360 + k * 6, 418)], 0.8, None) for k in range(17)]), "#9b6f24", 0.6, pad=2)
    # breast beam: carved wood with end knobs, sits over the warp tops
    beam = shapes(W, H, [[(38, 64), (742, 64), (750, 78), (742, 100), (38, 100), (30, 82)]])
    knobs = circles(W, H, [(28, 82, 22), (752, 82, 22)])
    art = OV(art, np.maximum(beam, knobs), lambda m: soft_shadow(m, "#000000", 8, 0.5, 0, 10), pad=40)
    art = wood(art, beam, 13)
    art = wood(art, knobs, 15, WOOD_D, "#3a2010")
    # carved band on the beam: small lozenges in gold
    loz = shapes(W, H, [[(x, 82), (x + 9, 74), (x + 18, 82), (x + 9, 90)] for x in range(70, 700, 30)], smooth=False)
    art = paint(art, loz, GOLD, GOLD_L, lc=LINE, px=0.8, dens=0.6)
    art = G(art, light_side(beam, 0, 5, 3), "#ffffff", seed=rs(), density=0.25, edge=0, bloom=0, rough=1)
    art = add_grain(art, 2, 0.02)
    save(art, f"{OUT}/gedokan.webp", max_w=780, quality=76)
    prev(art, "ss_gedokan", bg=MAROON_D)
    clear()

if "mahakam" in PARTS:
    W, H = 780, 460
    rng = random.Random(9)
    art = painted_sky(W, H, [(0, "#3d2140"), (0.22, "#8b3b45"), (0.42, "#e08a52"), (0.5, "#f3c27a"), (1, "#f3c27a")], seed=4, streak=0.9, grain=0.12)
    # sun low on the horizon
    art = OV(art, circles(W, H, [(520, 212, 50)]), lambda m: glow(m, "#ffd99a", 40, 0.8), pad=120)
    art = GP(art, circles(W, H, [(520, 214, 26)]), "#fff0c4", "#ffdf98", seed=rs(), rough=0.8)
    # soft clouds
    cl = []
    for (x, y, L) in [(140, 70, 220), (330, 112, 160), (650, 58, 240), (700, 150, 120), (60, 130, 120)]:
        for k in range(4):
            yy_ = y + k * 5 + rng.uniform(-2, 2); xx_ = x + rng.uniform(-20, 20)
            cl.append(([(xx_ - L / 2 + k * 14, yy_), (xx_, yy_ - 2), (xx_ + L / 2 - k * 10, yy_ + 1)], 7 - k, (0.4, 0.4)))
    art = G(art, gaussian_filter(strokes(W, H, cl), 1.2), "#ef9f78", seed=rs(), density=0.5, edge=0.25, bloom=0.2, rough=4)
    clear()
    horizon = 236
    # far hills
    hill = shapes(W, H, [[(-10, horizon)] + [(x, horizon - 18 - 10 * math.sin(x / 70) - 6 * math.sin(x / 23)) for x in range(0, W + 20, 20)] + [(W + 10, horizon)]])
    art = GP(art, hill, "#7a4a5e", "#6a3f55", seed=rs(), rough=2)
    # far bank: stilt houses, trees, mosque silhouette (dome + 4 slim minarets)
    bank = []
    for x in range(-10, W + 20, 34):
        bank.append(ellipse_pts(x + rng.uniform(-6, 6), horizon - 8, rng.uniform(16, 26), rng.uniform(10, 18), 10))
    bm = shapes(W, H, bank + [[(-10, horizon - 6), (W + 10, horizon - 6), (W + 10, horizon + 4), (-10, horizon + 4)]])
    art = GP(art, bm, "#4a2a3e", "#3d2236", seed=rs(), rough=2)
    hx = 170
    houses = []
    stilts = []
    for k in range(6):
        x = 40 + k * 46 + rng.uniform(-4, 4); w_ = rng.uniform(30, 40); y = horizon - 14
        houses.append([(x, y), (x + w_, y), (x + w_, y - 16), (x + w_ / 2, y - 28), (x, y - 16)])
        stilts += [([(x + 4, y), (x + 4, horizon + 6)], 1.4, None), ([(x + w_ - 4, y), (x + w_ - 4, horizon + 6)], 1.4, None)]
    mx = 650
    mosque = [[(mx - 44, horizon - 6), (mx + 44, horizon - 6), (mx + 44, horizon - 26), (mx - 44, horizon - 26)],
              ellipse_pts(mx, horizon - 30, 24, 24, 18)]
    minarets = [[(mx + dx - 1.8, horizon - 6), (mx + dx + 1.8, horizon - 6), (mx + dx + 1.8, horizon - 74), (mx + dx, horizon - 82), (mx + dx - 1.8, horizon - 74)] for dx in (-60, -38, 38, 60)]
    sil = np.maximum(shapes(W, H, houses + minarets, smooth=False), shapes(W, H, mosque))
    sil = np.maximum(sil, strokes(W, H, stilts))
    art = GP(art, sil, "#3a1f30", "#2e1828", seed=rs(), rough=1.2)
    # warm windows
    win = circles(W, H, [(40 + k * 46 + 14, horizon - 20, 2.2) for k in range(6)] + [(mx + dx, horizon - 16, 1.8) for dx in (-24, -8, 8, 24)])
    art = OV(art, win, lambda m: glow(m, "#ffcf7a", 3, 1.2), pad=10)
    clear()
    # river: wide, reflecting the sky
    river = shapes(W, H, [[(-10, horizon + 2), (W + 10, horizon + 2), (W + 10, H + 10), (-10, H + 10)]], smooth=False)
    water = painted_sky(W, H, [(0, "#f0b878"), (0.55, "#e5a067"), (0.62, "#b56a5a"), (1, "#5a3045")], seed=7, streak=1.2, grain=0.3)
    water[..., 3] = river
    art = over(art, water)
    # sun path glitter + horizontal ripple strokes
    rip = []
    for k in range(140):
        y = rng.uniform(horizon + 6, H - 10)
        d = (y - horizon) / (H - horizon)
        x = 520 + rng.gauss(0, 30 + 120 * d) if k < 80 else rng.uniform(-20, W)
        L = rng.uniform(10, 40) * (0.6 + d)
        rip.append(([(x - L / 2, y), (x + L / 2, y + rng.uniform(-0.6, 0.6))], 1.1 + 1.5 * d, (0.4, 0.4)))
    rm = strokes(W, H, rip[:80])
    art = tint(art, rm, "#fff0c8", 0.8, pad=2)
    art = tint(art, strokes(W, H, rip[80:]), "#7a3c48", 0.35, pad=2)
    # reflection of far bank
    refl = np.roll(sil[::-1], 2 * horizon - H + 6, 0) * (np.mgrid[0:H, 0:W][0] > horizon + 2)
    refl = gaussian_filter(refl, (2, 1)) * 0.35
    art = tint(art, refl, "#3a1f30", 1.0, pad=4)
    clear()

    def tug_barge(art):
        # coal barge (ponton) + tugboat in the middle distance
        y = horizon + 52
        barge = shapes(W, H, [[(180, y), (410, y), (402, y + 12), (188, y + 12)]], smooth=False)
        coal = shapes(W, H, [[(196, y)] + [(196 + k * 14, y - 9 - 4 * math.sin(k * 1.3)) for k in range(16)] + [(398, y)]])
        tug = shapes(W, H, [[(436, y + 2), (494, y + 2), (488, y + 12), (442, y + 12)], [(450, y + 2), (480, y + 2), (480, y - 12), (452, y - 12)], [(458, y - 12), (476, y - 12), (476, y - 20), (460, y - 20)]], smooth=False)
        rope = strokes(W, H, [([(410, y + 2), (436, y + 4)], 1.0, None)])
        m = np.maximum(np.maximum(barge, tug), rope)
        art = GP(art, m, "#2c1a24", "#3a2230", seed=rs(), rough=1)
        art = GP(art, coal, "#1c1418", "#2a2026", seed=rs(), rough=1.6)
        art = tint(art, circles(W, H, [(470, y - 6, 1.6)]), "#ffd27a", 1, pad=4)
        wake = strokes(W, H, [([(150 - k * 30, y + 13 + k * 0.5), (180 - k * 30, y + 13 + k * 0.5)], 1.4, (0.3, 0.3)) for k in range(4)])
        return tint(art, wake, "#ffe6b8", 0.6, pad=2)

    art = tug_barge(art)

    def ces(art, x, y, s, flip=False):
        f = -1 if flip else 1
        P = lambda pts: [(x + f * px * s, y + py * s) for px, py in pts]
        hull = P([(-120, -8), (-100, 6), (100, 8), (132, -12), (110, -4), (-100, -2)])
        roof = P([(-40, -26), (40, -28), (46, -22), (-46, -20)])
        posts = [(P([(-38, -21), (-38, -4)]), 1.6 * s, None), (P([(38, -23), (38, -4)]), 1.6 * s, None)]
        m = np.maximum(shapes(W, H, [hull, roof]), strokes(W, H, posts))
        art = GP(art, m, "#2a1822", "#3b2230", seed=rs(), rough=0.8)
        art = tint(art, strokes(W, H, [(P([(-96, -3), (104, -2)]), 1.4 * s, None)]), "#c8973a", 0.8, pad=2)
        wake = strokes(W, H, [(P([(-150 - k * 26, 10 + k), (-120 - k * 26, 10 + k)]), 1.6 * s, (0.3, 0.3)) for k in range(3)])
        art = tint(art, wake, "#ffe6b8", 0.65, pad=2)
        refl = np.roll(m[::-1], int(2 * y - H + 14 * s), 0)
        return tint(art, gaussian_filter(refl, (1.5, 0.5)) * 0.3, "#2a1822", 1, pad=2)

    art = ces(art, 620, horizon + 120, 0.75, True)
    art = ces(art, 230, horizon + 186, 1.05)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/mahakam.webp", quality=80)
    prev(art, "ss_mahakam")
    clear()

if "ces" in PARTS:
    W, H = 300, 80
    art = blank(W, H)
    x, y, s = 150, 46, 1.0
    hull = [(x - 120, y - 8), (x - 100, y + 6), (x + 100, y + 8), (x + 132, y - 12), (x + 110, y - 4), (x - 100, y - 2)]
    roof = [(x - 40, y - 26), (x + 40, y - 28), (x + 46, y - 22), (x - 46, y - 20)]
    posts = [([(x - 38, y - 21), (x - 38, y - 4)], 1.8, None), ([(x + 38, y - 23), (x + 38, y - 4)], 1.8, None)]
    hm = shapes(W, H, [hull]); rm = shapes(W, H, [roof]); pm = strokes(W, H, posts)
    art = paint(art, hm, MAROON, MAROON_D, lc=LINE, px=1.0)
    art = paint(art, rm, GOLD, "#b07f2c", lc=LINE, px=1.0)
    art = tint(art, pm, LINE, 0.9, pad=2)
    art = tint(art, strokes(W, H, [([(x - 96, y - 3), (x + 104, y - 2)], 1.6, None)]), GOLD_L, 0.9, pad=2)
    wave = strokes(W, H, [([(x - 140 + k * 40, y + 12), (x - 120 + k * 40, y + 9), (x - 100 + k * 40, y + 12)], 2.0, (0.3, 0.3)) for k in range(7)])
    art = G(art, wave, TEAL, seed=rs(), density=0.9, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    save(art, f"{OUT}/ces.webp", quality=86)
    prev(art, "ss_ces")

if "benang" in PARTS:
    # woven swatch: a diamond of head-panel check with a gold selvage and two silk tassels
    W, H = 150, 190
    art = blank(W, H)
    ch = check_cloth(150, 190, HEAD, HEAD[::-1], seed=7, sheen=0.25, tight=1)
    dm = shapes(W, H, [[(75, 10), (138, 82), (75, 154), (12, 82)]], smooth=False)
    dm = np.clip(gaussian_filter(displace(dm, 3, 1.0, 10), 0.5), 0, 1)
    sw = ch.copy(); sw[..., 3] = dm
    art = OV(art, dm, lambda m: soft_shadow(m, "#000000", 5, 0.35, 2, 5), pad=20)
    art = over(art, sw)
    art = tint(art, np.clip(outline(dm, 2.6) * 1.3, 0, 1), GOLD, 1, pad=4)
    tas = strokes(W, H, [([(75, 154), (75 + dx * 0.5, 168), (75 + dx, 184)], 1.4, (0, 0.5)) for dx in np.linspace(-8, 8, 9)])
    art = paint(art, tas, GOLD, GOLD_L, lc="#6b4a1a", px=0.6, dens=0.4)
    art = paint(art, circles(W, H, [(75, 156, 5)]), OX, MAROON, lc=LINE, px=0.8)
    save(art, f"{OUT}/benang.webp", quality=86)
    prev(art, "ss_benang")

kb(OUT)
