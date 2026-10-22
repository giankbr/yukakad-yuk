"""Pengajian Akbar — a majelis taklim at blue hour (gouache, green & gold, no figures): a mosque courtyard seen from under a
deep arcade, with a reflecting pool, a lit arcaded facade, a sage-tiled dome and two minarets against a teal-to-amber
sky with a thin crescent; brass lanterns (separate, they sway), an eight-point foil rosette, a seamless girih-style
border strip and a small dome-and-minarets skyline for the closing. No calligraphy is drawn (Arabic is typeset in HTML).
Run: python3 -I pengajian-akbar.py [part ...]   parts: scene lantern rosette band skyline
Assets -> public/themes/art/pengajian-akbar/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d6_lib import *

OUT = outdir("pengajian-akbar")
PARTS = sys.argv[1:] or ["scene", "lantern", "rosette", "band", "skyline"]
STONE, STONE2, STONED, STONEL = "#eee2c6", "#e6d7b6", "#b9a37a", "#fff5dc"
GREEN, GREEN2, GREEND = "#1f4d3f", "#285c4b", "#143429"
TILE, TILE2, TILED = "#5e8a74", "#6a9781", "#3d6655"
GOLD, GOLD2, GOLDD, GOLDL = "#c9a24a", "#d8b45c", "#94722c", "#f3dc9c"
WARM, WARM2 = "#f4c97a", "#e09a45"
NIGHT = "#173a3c"


def pointed_arch(cx, base_y, half_w, rise, n=24):
    """Two-centred pointed arch from left springing to right springing, apex at base_y - rise (rise > half_w = pointed)."""
    d = max(0.0, (rise * rise - half_w * half_w) / (2 * half_w))
    R = half_w + d
    t0 = math.acos(-d / R) if R else math.pi / 2
    left = [(cx + d + R * math.cos(t), base_y - R * math.sin(t)) for t in np.linspace(math.pi, t0, n)]
    return left + [(2 * cx - x, y) for x, y in reversed(left[:-1])]


def arch_opening(cx, top_y, bot_y, half_w, rise):
    return pointed_arch(cx, top_y + rise, half_w, rise) + [(cx + half_w, bot_y), (cx - half_w, bot_y)]


if "scene" in PARTS:
    W, H = 780, 980
    nx = Seq(81100); rng = random.Random(811)
    art = painted_sky(W, H, [(0.0, "#10282f"), (0.22, "#183d40"), (0.42, "#2f5f57"), (0.55, "#7f9877"), (0.63, "#d9b978"), (0.70, "#efcf8e"), (1.0, "#efcf8e")], seed=nx(), streak=0.9)
    # stars + crescent
    for _ in range(26):
        x, y = rng.uniform(80, 700), rng.uniform(40, 360)
        r = rng.uniform(1.0, 2.2)
        art = OV(art, circles(W, H, [(x, y, r)]), lambda m: col_arr(m, "#fff3d0", np.clip(gaussian_filter(m, 1.2) * 1.6, 0, 0.9)), pad=6)
    moon = np.clip(circles(W, H, [(560, 186, 30)]) - circles(W, H, [(574, 176, 27)]), 0, 1)
    art = OV(art, moon, lambda m: glow(m, "#f6e3a8", 18, 0.35), pad=60)
    art = GP(art, moon, "#fbeec4", "#f6e3a8", seed=nx(), rough=0.4, pad=6)
    # distant palms (soft silhouettes)
    palms = []
    for x0, hgt in ((70, 230), (118, 180), (690, 210), (735, 250)):
        palms.append((curve([(x0, 660), (x0 + 8, 660 - hgt * 0.5), (x0 + 4, 660 - hgt)], 20), 7, (0.0, 0.3)))
    pm = strokes(W, H, palms)
    fronds = []
    for x0, hgt in ((70, 230), (118, 180), (690, 210), (735, 250)):
        tx, ty = x0 + 4, 660 - hgt
        for k in range(8):
            a = -math.pi / 2 + (k - 3.5) * 0.42
            L = rng.uniform(46, 64)
            fronds.append((curve([(tx, ty), (tx + math.cos(a) * L * 0.6, ty + math.sin(a) * L * 0.6 - 6), (tx + math.cos(a) * L, ty + math.sin(a) * L + 14)], 14), 9, (0.0, 0.8)))
    pm = np.clip(pm + strokes(W, H, fronds), 0, 1)
    art = GP(art, pm, "#3c5d4f", "#45695a", seed=nx(), rough=1.2, density=0.85)
    # minarets
    for mx in (182, 598):
        shaft = shapes(W, H, [[(mx - 17, 640), (mx - 15, 300), (mx + 15, 300), (mx + 17, 640)]], smooth=False)
        art = body_paint(art, shaft, STONE, STONE2, STONED, STONEL, nx, ldir=(8, 0), blur=6, light_amt=0.3)
        bal = shapes(W, H, [[(mx - 28, 372), (mx + 28, 372), (mx + 22, 388), (mx - 22, 388)]], smooth=False)
        art = body_paint(art, bal, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(4, 2), blur=3)
        upper = shapes(W, H, [[(mx - 13, 300), (mx + 13, 300), (mx + 12, 268), (mx - 12, 268)]], smooth=False)
        art = body_paint(art, upper, STONE, STONE2, STONED, STONEL, nx, ldir=(6, 0), blur=4)
        art = GP(art, shapes(W, H, [arch_opening(mx, 276, 296, 5, 8)], smooth=False), "#f5c46e", "#e7a24f", seed=nx(), rough=0.3, pad=6)
        cone = shapes(W, H, [[(mx - 16, 270), (mx + 16, 270), (mx, 214)]], smooth=False)
        art = body_paint(art, cone, TILE, TILE2, TILED, "#8fb5a0", nx, ldir=(5, 0), blur=4)
        art = GP(art, strokes(W, H, [([(mx, 214), (mx, 196)], 2.4, None)]), GOLD, seed=nx(), rough=0.2, pad=6)
        art = GP(art, circles(W, H, [(mx, 194, 3.4)]), GOLD2, seed=nx(), rough=0.2, pad=6)
        for wy in (440, 520):
            art = GP(art, shapes(W, H, [arch_opening(mx, wy, wy + 30, 6, 10)], smooth=False), "#f2c06a", "#d98f3e", seed=nx(), rough=0.3, pad=6)
    # drum + dome
    drum = shapes(W, H, [[(282, 540), (282, 470), (498, 470), (498, 540)]], smooth=False)
    art = body_paint(art, drum, STONE, STONE2, STONED, STONEL, nx, ldir=(12, 0), blur=10, light_amt=0.3)
    for k in range(6):
        wx = 302 + k * 35
        art = GP(art, shapes(W, H, [arch_opening(wx, 484, 526, 8, 12)], smooth=False), "#f2c06a", "#d98f3e", seed=nx(), rough=0.3, pad=6)
    dome_pts = [(274, 474)] + [(390 - 116 * math.cos(t) * (1 - 0.15 * math.sin(t) ** 6), 474 - 150 * math.sin(t) ** 0.92) for t in np.linspace(0, math.pi / 2, 30)][1:]
    dome_pts = dome_pts + [(780 - x, y) for x, y in reversed(dome_pts)]
    dome_pts[len(dome_pts) // 2 - 1:len(dome_pts) // 2 + 1] = [(390, 318)]
    dome = shapes(W, H, [dome_pts])
    art = body_paint(art, dome, TILE, TILE2, TILED, "#9dc0aa", nx, ldir=(26, 6), blur=24, light_amt=0.35)
    ribs = []
    for k in range(-4, 5):
        x_end = 390 + k * 26
        ribs.append((curve([(390, 322), (390 + k * 20, 380), (x_end, 474)], 20), 2.2, (0.1, 0.0)))
    art = tint(art, strokes(W, H, ribs) * dome, TILED, 0.4, seed=nx())
    art = tint(art, gaussian_filter(ellipses(W, H, [(340, 400, 40, 60, 20)]), 18) * dome, "#f3dc9c", 0.35, seed=nx())
    art = GP(art, strokes(W, H, [([(276, 474), (504, 474)], 7, None)]), GOLD, GOLD2, seed=nx(), rough=0.4)
    art = GP(art, strokes(W, H, [([(390, 322), (390, 280)], 3, None)]), GOLD, seed=nx(), rough=0.2, pad=6)
    cres = np.clip(circles(W, H, [(390, 270, 11)]) - circles(W, H, [(396, 266, 9.5)]), 0, 1)
    art = GP(art, cres, GOLD2, GOLDL, seed=nx(), rough=0.2, pad=6)
    art = GP(art, circles(W, H, [(390, 290, 4.6)]), GOLD2, seed=nx(), rough=0.2, pad=6)
    # facade with five lit arches + crenellation
    fac = shapes(W, H, [[(96, 664), (96, 548), (684, 548), (684, 664)]], smooth=False)
    art = body_paint(art, fac, STONE, STONE2, STONED, STONEL, nx, ldir=(16, 0), blur=16, light_amt=0.3)
    cren = shapes(W, H, [[(104 + k * 24, 548), (116 + k * 24, 534), (128 + k * 24, 548)] for k in range(24)], smooth=False)
    art = GP(art, cren, STONE2, STONED, seed=nx(), rough=0.6)
    art = GP(art, strokes(W, H, [([(96, 556), (684, 556)], 4, None)]), GOLD, GOLDD, seed=nx(), rough=0.4)
    arches = []
    for k in range(5):
        ax = 158 + k * 116
        arches.append(arch_opening(ax, 570, 664, 36, 52))
    am = shapes(W, H, arches, smooth=False)
    art = GP(art, am, "#8a5a2a", "#a06a32", seed=nx(), rough=0.6)
    inner = np.zeros_like(am)
    for k in range(5):
        ax = 158 + k * 116
        inner = np.maximum(inner, gaussian_filter(ellipses(W, H, [(ax, 640, 26, 50, 0)]), 10))
    art = OV(art, inner * am, lambda m: col_arr(m, WARM, np.clip(m * 1.4, 0, 0.95)), pad=4)
    for k in range(5):
        ax = 158 + k * 116
        lamp = circles(W, H, [(ax, 600, 5)])
        art = OV(art, lamp, lambda m: glow(m, "#ffe3a0", 10, 0.6), pad=30)
        art = GP(art, lamp, "#fff2c8", seed=nx(), rough=0.2, pad=6)
    art = crayon(art, inner_edge(am, 2.0), GOLDD, seed=nx(), amt=0.7, tooth=0.2)
    # courtyard floor (stone in perspective) + reflecting pool
    floor = shapes(W, H, [[(0, 664), (W, 664), (W, H), (0, H)]], smooth=False)
    art = GP(art, floor, "#d9c9a6", "#cbb991", seed=nx(), rough=0.6, streak=0.8)
    vp = (390, 600)
    lines = []
    for k in range(-9, 10):
        xb = 390 + k * 130
        t0 = (664 - vp[1]) / (H - vp[1])
        lines.append(([(vp[0] + (xb - vp[0]) * t0, 664), (xb, H)], 1.6, None))
    for j in range(1, 9):
        y = 664 + (H - 664) * (j / 8) ** 1.7
        lines.append(([(0, y), (W, y)], 1.4, None))
    art = tint(art, strokes(W, H, lines) * floor, "#a8946c", 0.45, seed=nx())
    art = tint(art, gaussian_filter(floor * np.linspace(1, 0, H, dtype=np.float32)[:, None] ** 0.3, 4) * floor, "#f3d79a", 0.25, seed=nx())
    pool = shapes(W, H, [[(324, 676), (456, 676), (566, H), (214, H)]], smooth=False)
    refl = painted_sky(W, H, [(0.0, "#efcf8e"), (0.7, "#efcf8e"), (0.76, "#7f9877"), (0.86, "#2f5f57"), (1.0, "#183d40")], seed=nx(), streak=1.4)
    refl[..., 3] = pool
    art = over(art, refl)
    streaks = []
    for k in range(5):
        ax = 158 + k * 116
        if 280 < ax < 500:
            streaks.append((curve([(ax + rng.uniform(-3, 3), 690), (ax + (ax - 390) * 0.3, 860)], 10), 7, (0.0, 0.7)))
    streaks.append((curve([(390, 700), (390, 900)], 10), 12, (0.0, 0.8)))
    art = OV(art, gaussian_filter(strokes(W, H, streaks), 3) * pool, lambda m: col_arr(m, "#ffe0a0", m * 0.55), pad=6)
    rip = strokes(W, H, [([(250 + rng.uniform(0, 260), y), (250 + rng.uniform(0, 260) + 40, y)], 1.4, (0.3, 0.3)) for y in np.linspace(720, 960, 14)])
    art = OV(art, rip * pool, lambda m: col_arr(m, "#fff3d6", m * 0.35), pad=4)
    art = GP(art, strokes(W, H, [([(324, 676), (456, 676)], 6, None), ([(324, 676), (214, H)], 7, None), ([(456, 676), (566, H)], 7, None)]), STONE, STONE2, seed=nx(), rough=0.5)
    # foreground arcade framing the view (backlit, deep green-stone) with a gold edge
    frame = np.ones((H, W), np.float32)
    open_ = shapes(W, H, [arch_opening(390, 56, H + 40, 334, 400)], smooth=False)
    frame = np.clip(frame - open_, 0, 1)
    art = GP(art, frame, "#24463d", "#2b5145", seed=nx(), rough=1.2, streak=0.8)
    art = tint(art, side_light(frame, -30, 0, 30), "#183129", 0.5, seed=nx())
    rim_m = np.clip(gaussian_filter(open_, 3.0) - open_, 0, 1) * 3
    art = GP(art, np.clip(rim_m, 0, 1), GOLD, GOLD2, seed=nx(), rough=0.6)
    # eight-point star lattice on the spandrels (soft gold)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    stars = []
    for gy in range(0, 340, 64):
        for gx in range(0, W + 64, 64):
            ox = 32 if (gy // 64) % 2 else 0
            stars.append(rosette_pts(gx + ox, gy + 30, 14, 8, 0.62, rot=math.pi / 8))
    sm = shapes(W, H, stars, smooth=False) * np.clip(frame - gaussian_filter(rim_m, 6) * 2, 0, 1)
    art = tint(art, sm, GOLD, 0.35, seed=nx())
    art = vignette(art, 0.18, 2.0)
    art = add_grain(art, nx(), 0.03)
    preview(art, "pa-scene", bg="#000000")
    save_rgb(art, f"{OUT}/scene.webp", size=(600, 754), quality=76)
    clear()

if "lantern" in PARTS:
    W, H = 200, 520
    nx = Seq(81200); rng = random.Random(812)
    art = blank(W, H)
    cx = 100
    chain = strokes(W, H, [([(cx, 0), (cx, 196)], 2.6, None)])
    links = ellipses(W, H, [(cx, 12 + k * 18, 3.4, 7, 0) for k in range(11)])
    art = GP(art, np.clip(chain * 0.6 + links, 0, 1), GOLDD, GOLD, seed=nx(), rough=0.2, pad=6)
    cap = shapes(W, H, [[(cx - 10, 200), (cx + 10, 200), (cx + 34, 246), (cx - 34, 246)]], smooth=False)
    dome = shapes(W, H, [[(cx - 4, 180), (cx + 4, 180), (cx + 16, 200), (cx - 16, 200)]], smooth=False)
    body_ = shapes(W, H, [[(cx - 40, 248), (cx + 40, 248), (cx + 46, 330), (cx + 26, 384), (cx - 26, 384), (cx - 46, 330)]])
    base = shapes(W, H, [[(cx - 28, 382), (cx + 28, 382), (cx + 14, 410), (cx - 14, 410)]], smooth=False)
    tip = shapes(W, H, [petal_pts(cx, 408, 30, 6, math.pi / 2, n=12)])
    art = OV(art, gaussian_filter(body_, 10), lambda m: glow(m, "#ffd78a", 26, 0.55), pad=60)
    # glass panels glowing
    art = GP(art, body_, "#f9d27c", "#f2b35a", seed=nx(), rough=0.6)
    art = OV(art, gaussian_filter(ellipses(W, H, [(cx, 318, 20, 34, 0)]), 8) * body_, lambda m: col_arr(m, "#fff4cf", np.clip(m * 1.6, 0, 1)), pad=4)
    # brass cut-work lattice over the glass
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lat = []
    for gy in range(256, 384, 22):
        for gx in range(cx - 44, cx + 50, 22):
            lat.append(rosette_pts(gx + (11 if ((gy - 256) // 22) % 2 else 0), gy, 7, 8, 0.55))
    lm = np.clip(body_ - shapes(W, H, lat, smooth=False), 0, 1)
    ribs = strokes(W, H, [([(cx + dx, 250), (cx + dx * 1.15, 330), (cx + dx * 0.6, 382)], 3.2, None) for dx in (-40, -20, 0, 20, 40)])
    frame = np.clip(lm * 0.85 + ribs * body_, 0, 1)
    art = GP(art, frame, GOLDD, GOLD, seed=nx(), rough=0.4)
    art = tint(art, side_light(body_, 10, 0, 10) * frame, "#5a4218", 0.4, seed=nx())
    for m in (dome, cap, base, tip):
        art = body_paint(art, m, GOLD, GOLD2, GOLDD, GOLDL, nx, ldir=(5, 2), blur=4, light_amt=0.4)
    art = crayon(art, inner_edge(np.clip(cap + base + body_, 0, 1), 1.6), "#6a4f1c", seed=nx(), amt=0.6, tooth=0.25)
    preview(art, "pa-lantern", bg="#1f4d3f")
    save(art, f"{OUT}/lantern.webp", max_w=100, quality=84)
    clear()

if "rosette" in PARTS:
    W, H = 240, 240
    nx = Seq(81300); rng = random.Random(813)
    art = blank(W, H)
    outer = shapes(W, H, [rosette_pts(120, 120, 104, 8, 0.74, rot=math.pi / 8)], smooth=False)
    ring = np.clip(outer - shapes(W, H, [rosette_pts(120, 120, 88, 8, 0.74, rot=math.pi / 8)], smooth=False), 0, 1)
    sq1 = shapes(W, H, [[(120 + 62 * math.cos(a), 120 + 62 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 5)[:-1] + math.pi / 4]], smooth=False)
    sq2 = shapes(W, H, [[(120 + 62 * math.cos(a), 120 + 62 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 5)[:-1]]], smooth=False)
    star = np.clip(sq1 + sq2, 0, 1)
    star_in = np.clip(star - gaussian_filter((gaussian_filter(star, 5) > 0.97).astype(np.float32), 0.5), 0, 1)
    art = G(art, outer, "#1f4d3f", "#285c4b", seed=nx(), density=0.95, edge=0.3, bloom=0.1, rough=1.2, feather=0.8)
    art = FO(art, ring, GOLD, seed=nx(), emboss=0.7)
    art = FO(art, star_in, GOLD, seed=nx(), emboss=0.7)
    dot = circles(W, H, [(120, 120, 16)])
    art = FO(art, dot, GOLD2, seed=nx(), emboss=0.8)
    pts8 = circles(W, H, [(120 + 76 * math.cos(a), 120 + 76 * math.sin(a), 4.5) for a in np.linspace(0, 2 * math.pi, 9)[:-1] + math.pi / 8])
    art = FO(art, pts8, GOLD2, seed=nx(), emboss=0.6)
    preview(art, "pa-rosette", bg="#f6f0e1")
    save(art, f"{OUT}/rosette.webp", max_w=120, quality=86)
    clear()

if "band" in PARTS:
    # seamless horizontal strip: alternating 8-point stars and crosses (girih-inspired), gold on deep green
    W, H = 192, 48
    nx = Seq(81400)
    big_w = W * 3
    art = blank(big_w, H)
    bg = shapes(big_w, H, [[(0, 0), (big_w, 0), (big_w, H), (0, H)]], smooth=False)
    art = GP(art, bg, GREEN, GREEN2, seed=nx(), rough=0.0, streak=0.6)
    stars, crosses = [], []
    for k in range(-1, 3 * 4 + 1):
        cx = k * 48 + 24
        if k % 2 == 0:
            stars.append(rosette_pts(cx, 24, 17, 8, 0.66, rot=math.pi / 8))
        else:
            s_ = 9
            crosses.append([(cx - s_, 24 - 3), (cx - 3, 24 - 3), (cx - 3, 24 - s_), (cx + 3, 24 - s_), (cx + 3, 24 - 3), (cx + s_, 24 - 3), (cx + s_, 24 + 3), (cx + 3, 24 + 3), (cx + 3, 24 + s_), (cx - 3, 24 + s_), (cx - 3, 24 + 3), (cx - s_, 24 + 3)])
    st = shapes(big_w, H, stars, smooth=False)
    st_ring = np.clip(st - shapes(big_w, H, [rosette_pts(k * 48 + 24, 24, 11, 8, 0.66, rot=math.pi / 8) for k in range(-1, 13) if k % 2 == 0], smooth=False), 0, 1)
    art = FO(art, st_ring, GOLD, seed=nx(), emboss=0.5)
    art = FO(art, shapes(big_w, H, crosses, smooth=False), GOLD, seed=nx(), emboss=0.5)
    art = FO(art, strokes(big_w, H, [([(0, 3), (big_w, 3)], 2.4, None), ([(0, 45), (big_w, 45)], 2.4, None)]), GOLD, seed=nx(), emboss=0.3)
    tile = art[:, W:2 * W].copy()
    tile[..., 3] = 1
    preview(tile, "pa-band", bg="#000000")
    save_full(tile, f"{OUT}/band.webp", size=(W, H), quality=82)
    clear()

if "skyline" in PARTS:
    W, H = 640, 330
    nx = Seq(81500); rng = random.Random(815)
    art = blank(W, H)
    cx = 320
    for mx in (150, 490):
        shaft = shapes(W, H, [[(mx - 13, 320), (mx - 11, 96), (mx + 11, 96), (mx + 13, 320)]], smooth=False)
        art = body_paint(art, shaft, STONE, STONE2, STONED, STONEL, nx, ldir=(6, 0), blur=5, light_amt=0.3)
        art = body_paint(art, shapes(W, H, [[(mx - 22, 160), (mx + 22, 160), (mx + 17, 172), (mx - 17, 172)]], smooth=False), GOLD, GOLD2, GOLDD, GOLDL, nx, blur=3)
        art = body_paint(art, shapes(W, H, [[(mx - 12, 98), (mx + 12, 98), (mx, 52)]], smooth=False), TILE, TILE2, TILED, "#8fb5a0", nx, ldir=(4, 0), blur=3)
        art = GP(art, strokes(W, H, [([(mx, 52), (mx, 38)], 2.2, None)]), GOLD, seed=nx(), rough=0.2, pad=6)
    drum = shapes(W, H, [[(230, 322), (230, 246), (410, 246), (410, 322)]], smooth=False)
    art = body_paint(art, drum, STONE, STONE2, STONED, STONEL, nx, ldir=(10, 0), blur=8, light_amt=0.3)
    for k in range(5):
        art = GP(art, shapes(W, H, [arch_opening(254 + k * 33, 262, 300, 7, 11)], smooth=False), "#f2c06a", "#d98f3e", seed=nx(), rough=0.3, pad=6)
    dome_pts = [(cx - 98 * math.cos(t), 250 - 128 * math.sin(t) ** 0.92) for t in np.linspace(0, math.pi / 2, 26)]
    dome_pts = dome_pts[:-1] + [(cx, 112)] + [(2 * cx - x, y) for x, y in reversed(dome_pts[:-1])]
    dome = shapes(W, H, [dome_pts])
    art = body_paint(art, dome, TILE, TILE2, TILED, "#9dc0aa", nx, ldir=(20, 4), blur=18, light_amt=0.35)
    art = GP(art, strokes(W, H, [([(224, 250), (416, 250)], 6, None)]), GOLD, GOLD2, seed=nx(), rough=0.4)
    art = GP(art, strokes(W, H, [([(cx, 116), (cx, 80)], 3, None)]), GOLD, seed=nx(), rough=0.2, pad=6)
    cres = np.clip(circles(W, H, [(cx, 70, 10)]) - circles(W, H, [(cx + 5, 66, 8.6)]), 0, 1)
    art = GP(art, cres, GOLD2, GOLDL, seed=nx(), rough=0.2, pad=6)
    wing = shapes(W, H, [[(40, 322), (40, 280), (600, 280), (600, 322)]], smooth=False) * (1 - drum)
    art = body_paint(art, wing, STONE2, STONE, STONED, STONEL, nx, ldir=(10, 0), blur=8, light_amt=0.3)
    arc = [arch_opening(70 + k * 50, 290, 322, 14, 16) for k in range(12) if not (220 < 70 + k * 50 < 420)]
    art = GP(art, shapes(W, H, arc, smooth=False), "#f2c06a", "#d98f3e", seed=nx(), rough=0.3)
    art = crayon(art, inner_edge(np.clip(wing + drum + dome, 0, 1), 1.6), GOLDD, seed=nx(), amt=0.5)
    preview(art, "pa-skyline", bg="#1f4d3f")
    save(art, f"{OUT}/skyline.webp", max_w=420, quality=82)
    clear()
