"""Isra Mi'raj — night commemoration: painted indigo night sky with a rising band of stars and a crescent, a mosque
silhouette (domes + minarets) with warm lit arcades, a pierced-brass hanging lantern, a foil eight-point star.
No figures, no Buraq, no calligraphy drawn. Run: python3 -I isra-miraj.py [part ...]  parts: sky masjid lantern star"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n6_lib import *

OUT = outdir("isra-miraj")
PARTS = sys.argv[1:] or ["sky", "masjid", "lantern", "star"]
NIGHT, NIGHT_D = "#191b46", "#0e1030"
RIM = "#8f8fd0"
AMBER, AMBER_L = "#f0a94a", "#ffd890"
SILVER = "#e9e4f2"
GOLD = "#d9b46a"


if "sky" in PARTS:
    W, H = 720, 1200
    rng = np.random.default_rng(7); prng = random.Random(7)
    art = painted_sky(W, H, [(0, "#090c26"), (0.35, "#151a4a"), (0.68, "#2a2766"), (0.86, "#463a80"), (1.0, "#6b4f8e")], seed=3, streak=0.8, grain=0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # soft nebula washes
    neb = fbm(W, H, 11, 220, 4)
    art = lay(art, np.clip((neb - 0.55) * 2.2, 0, 1) * 0.35, "#5a4c9a", 1.0)
    # rising band of stars: a gentle S from the bottom centre to the upper left
    def band_x(y):
        t = 1 - y / H
        return W * (0.52 - 0.22 * t + 0.08 * math.sin(t * 3.2))
    bx = np.array([band_x(y) for y in range(H)], np.float32)[:, None]
    bw = 70 + (1 - yy / H) * 90
    band = np.exp(-((xx - bx) ** 2) / (2 * bw ** 2))
    art = lay(art, band * 0.26 * np.clip(1.2 - yy / H, 0, 1), "#b9b2e6", 1.0)
    # stars: dense in the band, sparse elsewhere
    stars = np.zeros((H, W), np.float32)
    big = []
    for k in range(1400):
        if k < 800:
            y = rng.uniform(0, H * 0.92); x = band_x(y) + rng.normal(0, 70 + (1 - y / H) * 90)
        else:
            y = rng.uniform(0, H * 0.85); x = rng.uniform(0, W)
        if not (0 <= x < W and 0 <= y < H):
            continue
        r = rng.random() ** 3
        stars[int(y), int(x)] += 0.4 + 0.6 * r
        if r > 0.9:
            big.append((x, y, 1.2 + r * 1.6))
    st = np.clip(gaussian_filter(stars, 0.55) * 3.0, 0, 1)
    art = lay(art, st, "#f4f0ff", 1.0)
    for x, y, r in big:
        m = circles(W, H, [(x, y, r)])
        art = lay(art, np.clip(gaussian_filter(m, r * 2.5) * 1.4, 0, 1) * 0.5, "#d9d3ff", 1.0)
        art = lay(art, m, "#ffffff", 1.0)
    # a few eight-point stars (geometric, not flares)
    for x, y, r in ((120, 210, 9), (560, 470, 7), (90, 640, 6), (420, 120, 6)):
        m = shapes(W, H, [star_pts(x, y, r, r * 0.45, 8, 0.0)], smooth=False)
        art = lay(art, np.clip(gaussian_filter(m, 4) * 1.2, 0, 1) * 0.45, "#e7deff", 1.0)
        art = lay(art, m, "#fffaf0", 0.95)
    # crescent moon (upper right) with halo
    moon = np.clip(circles(W, H, [(560, 190, 58)]) - circles(W, H, [(584, 172, 52)]), 0, 1)
    art = lay(art, np.clip(gaussian_filter(circles(W, H, [(560, 190, 60)]), 40) * 1.5, 0, 1) * 0.35, "#cfc4f0", 1.0)
    art = over(art, pigment(moon, "#fff4d6", "#f2dfae", seed=5, density=0.98, edge=0.15, bloom=0.15, gran=0.2, rough=1.2, feather=0.6))
    # warm glow at the horizon (from the town's lamps)
    art = lay(art, np.clip((yy - H * 0.8) / (H * 0.2), 0, 1) ** 1.5 * 0.4, "#c77d6a", 1.0)
    art = add_grain(art, 9, 0.03)
    im = to_image(art).convert("RGB")
    im.save(f"{OUT}/sky.webp", "WEBP", quality=70, method=6)
    im.save(f"{PREV}/im-sky.png")
    print("sky", os.path.getsize(f"{OUT}/sky.webp") // 1024, "KB")
    clear()

if "masjid" in PARTS:
    W, H = 780, 440
    nx = Seq(9500); prng = random.Random(21)
    art = blank(W, H)
    G0 = 404

    def dome(cx, by, r, h):
        """onion-ish dome: semi-ellipse swelling, pointed top."""
        pts = []
        for i in range(25):
            t = i / 24
            a = math.pi * t
            x = cx - math.cos(a) * r * (1.06 - 0.06 * math.sin(a))
            y = by - math.sin(a) * h * 0.82
            pts.append((x, y))
        top = [(cx + r * 0.06, by - h * 0.9), (cx, by - h * 1.12), (cx - r * 0.06, by - h * 0.9)]
        return pts[:13] + top + pts[13:]

    polys = []
    polys.append(rect(40, 340, 740, G0 + 40))                    # outer arcade walls
    polys.append(rect(196, 248, 584, G0 + 40))                    # prayer hall
    polys.append(rect(300, 206, 480, 252))                        # drum
    polys.append(dome(390, 210, 102, 150))                        # main dome
    for cx in (246, 534):
        polys.append(rect(cx - 40, 222, cx + 40, 252))
        polys.append(dome(cx, 226, 44, 74))
    # minarets
    def minaret(cx, top, w):
        p = [rect(cx - w / 2, top + 60, cx + w / 2, G0 + 40),
             rect(cx - w * 0.85, top + 150, cx + w * 0.85, top + 164), rect(cx - w * 0.78, top + 70, cx + w * 0.78, top + 82),
             rect(cx - w * 0.42, top + 20, cx + w * 0.42, top + 72),
             [(cx - w * 0.55, top + 24), (cx, top - 30), (cx + w * 0.55, top + 24)]]
        return p
    polys += minaret(668, 60, 34)
    polys += minaret(112, 150, 26)
    sil = shapes(W, H, polys, smooth=False)
    # finials + crescents on top of domes/minarets
    fin = strokes(W, H, [([(390, 42), (390, 22)], 3, None), ([(668, 30), (668, 14)], 2.6, None), ([(246, 144), (246, 132)], 2.4, None), ([(534, 144), (534, 132)], 2.4, None)])
    cres = np.clip(circles(W, H, [(390, 16, 9), (668, 9, 7)]) - circles(W, H, [(394, 13, 8), (671, 7, 6)]), 0, 1)
    sil = np.maximum(sil, fin)
    # date palms at the edges
    palms = np.maximum(palm(W, H, 18, G0 + 30, 210, prng, 0.08), palm(W, H, 760, G0 + 30, 180, prng, -0.1))
    art = GP(art, palms, "#14163a", NIGHT_D, seed=nx(), rough=1.0, streak=0.6)
    art = GP(art, sil, NIGHT, NIGHT_D, seed=nx(), rough=0.8, streak=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, sil * np.clip((yy - 200) / 240, 0, 1), NIGHT_D, seed=nx(), density=0.5, edge=0, bloom=0.2, rough=1)
    # moonlight rim (moon is upper right)
    gy, gx = np.gradient(gaussian_filter(sil, 1.6))
    rim = np.clip(-(gx * 0.75 - gy * 0.66) * 3.2, 0, 1) * sil
    art = lay(art, rim * 0.7, RIM, 1.0)
    dome_sheen = shapes(W, H, [dome(390, 210, 102, 150)], smooth=False) * np.clip((xx - 390) / 100, 0, 1) * np.clip((230 - yy) / 140, 0, 1)
    art = lay(art, dome_sheen * 0.32, "#5b5ca0", 1.0)
    art = FO(art, np.maximum(cres, circles(W, H, [(390, 40, 4.5), (668, 32, 3.5), (246, 142, 3.5), (534, 142, 3.5)])), GOLD, seed=nx(), emboss=0.5, sparkle=0.1)
    # lit pointed-arch windows
    def arch_win(cx, by, w, h):
        return [(cx - w / 2, by), (cx - w / 2, by - h * 0.62)] + [(cx + math.cos(a) * w / 2, by - h * 0.62 - math.sin(a) * h * 0.38 * (1 - abs(math.cos(a)) * 0.0)) for a in [math.pi - i / 10 * math.pi for i in range(11)]] + [(cx + w / 2, by)]
    wins = []
    for k in (0, 1, 2, 5, 6, 7):
        wins.append(arch_win(222 + k * 48.5 + 3, 388, 24, 64))
    for k in range(4):
        wins.append(arch_win(326 + k * 42.5, 248, 14, 30))
    for x in list(range(56, 186, 30)) + list(range(600, 740, 30)):
        wins.append(arch_win(x + 8, 392, 16, 38))
    wins.append(arch_win(668, 206, 10, 22)); wins.append(arch_win(668, 300, 10, 22))
    for cx in (246, 534):
        wins.append(arch_win(cx, 248, 12, 20))
    door = arch_win(390, G0 + 6, 46, 96)
    wm = shapes(W, H, wins, smooth=False)
    dm = shapes(W, H, [door], smooth=False)
    lit = np.maximum(wm, dm)
    art = over(art, glow(lit, AMBER, radius=9, strength=0.45))
    art = GP(art, lit, AMBER_L, AMBER, seed=nx(), rough=0.5, streak=0.4, pad=6)
    # lamp light spilling on the ground
    spill = np.exp(-((xx - 390) ** 2) / (2 * 220 ** 2)) * np.clip((yy - (G0 - 6)) / 30, 0, 1) * (yy < G0 + 40)
    art = lay(art, spill * sil * 0.45, "#7a4f4a", 1.0)
    # little hanging lamps string along the arcade top
    sx = list(range(60, 740, 26))
    string = curve([(40, 336), (200, 350), (390, 336), (584, 350), (740, 336)], 60)
    art = G(art, stroke_mask(W, H, string, 1.2), "#efe7d4", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.4)
    bulbs = circles(W, H, [(p[0], p[1] + 4, 2.6) for p in string[::3]])
    art = over(art, glow(bulbs, AMBER_L, radius=4, strength=0.7))
    art = lay(art, bulbs, "#fff1c4", 1.0)
    # ground
    ground = shapes(W, H, [rect(0, G0 + 30, W, H)], smooth=False)
    art = GP(art, ground, "#120f2e", "#0a0a22", seed=nx(), rough=1.0)
    prev(art, "im-masjid", bg="#2a2766")
    save(art, f"{OUT}/masjid.webp", max_w=720, quality=80)
    clear()

if "lantern" in PARTS:
    W, H = 200, 460
    nx = Seq(9700)
    art = blank(W, H)
    cx = 100
    chain = strokes(W, H, [([(cx, 0), (cx, 96)], 2.4, None)])
    cap = shapes(W, H, [[(cx - 10, 96), (cx + 10, 96), (cx + 34, 140), (cx - 34, 140)], rect(cx - 44, 140, cx + 44, 152)], smooth=False)
    body = [(cx - 44, 152), (cx + 44, 152), (cx + 56, 230), (cx + 44, 316), (cx - 44, 316), (cx - 56, 230)]
    bm = shapes(W, H, [body], smooth=False)
    foot = shapes(W, H, [rect(cx - 46, 316, cx + 46, 328), [(cx - 30, 328), (cx + 30, 328), (cx + 8, 368), (cx - 8, 368)]], smooth=False)
    tip = strokes(W, H, [([(cx, 368), (cx, 396)], 3, (0.0, 0.6))])
    ball = circles(W, H, [(cx, 400, 5), (cx, 92, 6)])
    art = over(art, glow(bm, AMBER, radius=26, strength=0.55))
    # glass panes glowing
    art = GP(art, bm, AMBER_L, AMBER, seed=nx(), rough=0.6, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = lay(art, bm * np.exp(-((xx - cx) ** 2 + (yy - 236) ** 2) / (2 * 30 ** 2)), "#fff6d8", 0.9)
    # pierced brass lattice over the glass: ribs + star cut pattern
    ribs = strokes(W, H, [([(cx - 44, 152), (cx - 56, 230), (cx - 44, 316)], 5, None), ([(cx + 44, 152), (cx + 56, 230), (cx + 44, 316)], 5, None),
                          ([(cx - 15, 152), (cx - 19, 230), (cx - 15, 316)], 4, None), ([(cx + 15, 152), (cx + 19, 230), (cx + 15, 316)], 4, None),
                          ([(cx - 56, 230), (cx + 56, 230)], 4, None)])
    pierced = np.zeros((H, W), np.float32)
    for y in (186, 272):
        for x in (cx - 32, cx, cx + 32):
            pierced = np.maximum(pierced, shapes(W, H, [star_pts(x, y, 10, 5, 8, 0.0)], smooth=False))
    lattice = np.clip(bm - pierced - gaussian_filter(bm, 1) * 0, 0, 1) * (1 - np.clip(gaussian_filter(pierced, 0.6) * 1.0, 0, 1))
    brass = np.clip(lattice * 0.0 + ribs, 0, 1)
    art = GP(art, np.clip(bm - pierced, 0, 1) * 0.55, "#7a5520", "#4a3012", seed=nx(), rough=0.4, pad=6)
    art = FO(art, np.maximum.reduce([brass, cap, foot, tip, ball, chain]), "#c89a4a", seed=nx(), emboss=0.6, sparkle=0.12)
    art = lay(art, np.clip(gaussian_filter(pierced, 1.5) * 1.3, 0, 1) * bm, "#fff2c6", 0.95)
    prev(art, "im-lantern", bg="#191b46")
    save(art, f"{OUT}/lantern.webp", max_w=130, quality=82)
    clear()

if "star" in PARTS:
    W, H = 220, 220
    nx = Seq(9900)
    sq1 = shapes(W, H, [[(110 + math.cos(a) * 90, 110 + math.sin(a) * 90) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]], smooth=False)
    sq2 = shapes(W, H, [[(110 + math.cos(a) * 90, 110 + math.sin(a) * 90) for a in [k * math.pi / 2 for k in range(4)]]], smooth=False)
    st = np.maximum(sq1, sq2)
    inner = np.maximum(shapes(W, H, [[(110 + math.cos(a) * 70, 110 + math.sin(a) * 70) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]], smooth=False),
                       shapes(W, H, [[(110 + math.cos(a) * 70, 110 + math.sin(a) * 70) for a in [k * math.pi / 2 for k in range(4)]]], smooth=False))
    ring = np.clip(st - inner, 0, 1)
    art = FO(blank(W, H), ring, GOLD, seed=nx(), emboss=0.7, sparkle=0.16)
    core = shapes(W, H, [star_pts(110, 110, 44, 22, 8, math.pi / 8)], smooth=False)
    art = FO(art, core, "#e8e1f2", seed=nx(), emboss=0.6, sparkle=0.2)
    art = FO(art, circles(W, H, [(110, 110, 10)]), GOLD, seed=nx(), emboss=0.6)
    prev(art, "im-star", bg="#191b46")
    save(art, f"{OUT}/star.webp", max_w=110, quality=84)
