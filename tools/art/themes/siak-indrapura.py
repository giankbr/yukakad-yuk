"""Siak Indrapura — gouache dusk scene of the domed Istana Siak (Asserayah Hasyimiah) on the Siak river (architecture
only), a kajang-roofed sampan, and Siak songket in gold weft on deep plum (tile, pucuk rebung band, bunga, divider).
Run: python3 -I siak-indrapura.py [part ...]  parts: scene boat songket pucuk bunga divider
Assets -> public/themes/art/siak-indrapura/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m3_lib import *

OUT = outdir("siak-indrapura")
PARTS = sys.argv[1:] or ["scene", "boat", "songket", "pucuk", "bunga", "divider"]
PLUM, PLUM_D, PLUM_L = "#3b1534", "#240a20", "#5e2350"
GOLD, GOLD_L, GOLD_D = "#d6a74a", "#f0d28a", "#8f6620"
ROSE = "#c2587a"
WALL, WALL_S, WALL_D = "#f3e2cf", "#d4b4a6", "#a8848a"


def weave_q(mask, row=3, col=2):
    """Quantise a motif mask to weft rows / warp columns so it reads as woven supplementary weft."""
    h, w = mask.shape
    m = mask[: h - h % row, : w - w % col]
    q = m.reshape(h // row, row, w // col, col).mean((1, 3))
    q = (q > 0.42).astype(np.float32)
    up = np.repeat(np.repeat(q, row, 0), col, 1)
    out = np.zeros_like(mask)
    out[: up.shape[0], : up.shape[1]] = up
    # thread gaps between weft rows
    yy = np.arange(h)[:, None] % row
    out *= np.where(yy == row - 1, 0.55, 1.0)
    return gaussian_filter(out, 0.45)


def star8(cx, cy, r, inner=0.42, rot=0.0):
    pts = []
    for i in range(16):
        a = rot + i * math.pi / 8
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


def dome(art, W, H, cx, by, w, h, nx, drum=10):
    d = rects(W, H, [(cx - w * 0.44, by - drum, cx + w * 0.44, by)])
    art = GP(art, d, WALL, WALL_S, seed=nx(), rough=0.6, pad=6)
    art = GP(art, strokes(W, H, [([(cx - w * 0.47, by - drum), (cx + w * 0.47, by - drum)], 2.4, None)]), GOLD_D, seed=nx(), rough=0.3, pad=4)
    m = shapes(W, H, [onion_pts(cx, by - drum, w, h)])
    art = GP(art, m, GOLD_L, GOLD, seed=nx(), rough=0.7, streak=0.9, pad=6)
    art = G(art, side_shade(m, cx - w * 0.1, cx + w * 0.55), "#8a4a3c", seed=nx(), density=0.55, edge=0.1, bloom=0.1, rough=1, feather=1.2)
    art = G(art, side_shade(m, cx + w * 0.1, cx - w * 0.6) * 0.8, "#ffe9b0", seed=nx(), density=0.35, edge=0, bloom=0, rough=1)
    ribs = strokes(W, H, [(curve([(cx + o * w * 0.42, by - drum - 2), (cx + o * w * 0.32, by - drum - h * 0.5), (cx, by - drum - h * 0.92)], 14), 1.1, None) for o in (-0.55, 0, 0.55)])
    art = G(art, ribs * m, GOLD_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.3)
    spire = np.maximum(strokes(W, H, [([(cx, by - drum - h * 0.9), (cx, by - drum - h - 16)], 2.0, None)]), circles(W, H, [(cx, by - drum - h - 2, 3.2)]))
    art = GP(art, spire, GOLD_D, seed=nx(), rough=0.3, pad=4)
    return art


def windows(art, W, H, nx, x0, x1, ybot, w, h, step, lit_rng, dark=False):
    wins = []
    x = x0
    while x + w <= x1:
        wins.append(arch_pts(x, ybot, w, h, 10))
        x += step
    frame = shapes(W, H, [[(px + (-2.5 if px < p[0][0] + w / 2 else 2.5), py - 2.5 if py < ybot - 2 else py) for px, py in p] for p in wins], smooth=False)
    art = GP(art, frame, GOLD, GOLD_D, seed=nx(), rough=0.3, pad=4)
    for p in wins:
        m = shapes(W, H, [p], smooth=False)
        lit = lit_rng.random() < 0.62
        art = GP(art, m, ("#f6c867" if lit else "#5a3346"), ("#e79a45" if lit else "#3c2034"), seed=nx(), rough=0.3, pad=4)
    return art


if "scene" in PARTS:
    W, H = 760, 880
    nx = Seq(31000)
    rng = random.Random(11)
    WL = 520
    art = painted_sky(W, H, [(0, "#2c1440"), (0.18, "#4e2257"), (0.36, "#93446c"), (0.5, "#dc8a6c"), (0.59, "#f3c27c"), (0.62, "#f3c27c"), (1, "#f3c27c")], seed=nx(), streak=0.35)
    # sun low on the left, soft glow
    sun = circles(W, H, [(618, WL - 104, 38)])
    art = over(art, glow(sun, "#ffd98f", radius=50, strength=0.55))
    art = GP(art, sun, "#ffe3a0", "#ffd283", seed=nx(), rough=1.2, pad=8)
    # streaky dusk clouds
    cl = ellipses(W, H, [(rng.uniform(-40, W + 40), rng.uniform(170, 350), rng.uniform(60, 140), rng.uniform(8, 16), rng.uniform(-3, 3)) for _ in range(12)])
    art = G(art, cl, "#eaa08a", "#b9628a", seed=nx(), density=0.55, edge=0.35, bloom=0.4, rough=10, feather=4)
    cl2 = ellipses(W, H, [(rng.uniform(-40, W + 40), rng.uniform(70, 200), rng.uniform(50, 120), rng.uniform(6, 12), 0) for _ in range(8)])
    art = G(art, cl2, "#7a3767", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=6, feather=3)
    # far bank: low trees
    bank = shapes(W, H, [[(-20, WL + 4), (-20, WL - 30)] + [(x, WL - 34 - 14 * math.sin(x * 0.03) - rng.uniform(0, 14)) for x in range(0, W + 40, 40)] + [(W + 20, WL - 26), (W + 20, WL + 4)]])
    art = GP(art, bank, "#4b2a46", "#3a2038", seed=nx(), rough=4, streak=0.8, pad=8)
    tufts = circles(W, H, [(x, WL - 40 - rng.uniform(0, 26), rng.uniform(14, 26)) for x in list(range(-10, 170, 22)) + list(range(600, W + 20, 22))])
    art = GP(art, tufts, "#523050", "#3e2240", seed=nx(), rough=3, pad=8)
    art = G(art, v_ramp(tufts, WL - 80, WL - 40) * 0 + tufts * np.clip((np.arange(W)[None, :] - 0) / W, 0, 1), "#2a1430", seed=nx(), density=0.25, edge=0, bloom=0, rough=2)
    cx, BY = 380, WL - 16
    # lawn + terrace
    lawn = shapes(W, H, [[(110, BY + 4), (120, BY - 6), (640, BY - 6), (650, BY + 4)]], smooth=False)
    art = GP(art, lawn, "#5d3a4c", "#4a2c40", seed=nx(), rough=1.0, pad=6)
    terr = rects(W, H, [(140, BY - 18, 620, BY - 4)])
    art = GP(art, terr, "#e5cdbb", "#c7a99c", seed=nx(), rough=0.6, pad=6)
    art = G(art, strokes(W, H, [([(140, BY - 10), (620, BY - 10)], 1.4, None)]), WALL_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3)
    # corner towers (behind wings), domed
    for tx in (178, 582):
        tw = rects(W, H, [(tx - 26, BY - 200, tx + 26, BY - 18)])
        art = GP(art, tw, WALL, WALL_S, seed=nx(), rough=0.6, streak=0.4, pad=6)
        art = G(art, side_shade(tw, tx - 4, tx + 30), WALL_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8)
    # main block: two storeys
    low = rects(W, H, [(196, BY - 96, 564, BY - 18)])
    up = rects(W, H, [(206, BY - 166, 554, BY - 104)])
    art = GP(art, np.maximum(low, up), WALL, WALL_S, seed=nx(), rough=0.7, streak=0.4, pad=6)
    art = G(art, side_shade(np.maximum(low, up), 420, 590), WALL_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    # rosy dusk light on the left faces
    art = G(art, side_shade(np.maximum(low, up), 420, 190) * 0.8, "#f6c2a4", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=1)
    # cornices / balustrades (gold trim)
    trims = [(186, BY - 106, 574, BY - 96), (198, BY - 174, 562, BY - 166)]
    art = GP(art, rects(W, H, trims), GOLD, GOLD_D, seed=nx(), rough=0.3, pad=4)
    posts = rects(W, H, [(x, BY - 184, x + 3.2, BY - 174) for x in range(200, 562, 9)] + [(x, BY - 116, x + 3, BY - 106) for x in range(190, 572, 9)])
    rail = rects(W, H, [(198, BY - 187, 562, BY - 183), (188, BY - 119, 572, BY - 115)])
    art = GP(art, np.maximum(posts, rail), "#efe0cc", "#cdb19f", seed=nx(), rough=0.3, pad=4)
    walls = np.maximum(low, up)
    yy_ = np.arange(H, dtype=np.float32)[:, None]
    for ty in (BY - 96, BY - 166):
        art = G(art, walls * np.clip(1 - np.abs(yy_ - ty - 6) / 8, 0, 1), "#b88f92", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = G(art, walls, "#e9c7b6", seed=nx(), density=0.22, edge=0.3, bloom=0.5, rough=4, holes=0.3)
    # windows: upper and lower rows
    wr = random.Random(5)
    art = windows(art, W, H, nx, 214, 340, BY - 112, 16, 40, 31, wr)
    art = windows(art, W, H, nx, 432, 552, BY - 112, 16, 40, 31, wr)
    art = windows(art, W, H, nx, 206, 336, BY - 24, 18, 52, 32, wr)
    art = windows(art, W, H, nx, 432, 560, BY - 24, 18, 52, 32, wr)
    # tower windows + domes
    for tx in (178, 582):
        art = windows(art, W, H, nx, tx - 8, tx + 9, BY - 128, 16, 40, 30, wr)
        art = windows(art, W, H, nx, tx - 8, tx + 9, BY - 40, 16, 46, 30, wr)
        art = GP(art, rects(W, H, [(tx - 30, BY - 208, tx + 30, BY - 198)]), GOLD, GOLD_D, seed=nx(), rough=0.3, pad=4)
        art = dome(art, W, H, tx, BY - 208, 46, 52, nx, 10)
    # central portico, taller, with the great dome
    cb = rects(W, H, [(326, BY - 206, 434, BY - 18)])
    art = GP(art, cb, "#f7e9d6", WALL, seed=nx(), rough=0.6, streak=0.4, pad=6)
    art = G(art, side_shade(cb, 380, 440), WALL_D, seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    art = GP(art, rects(W, H, [(318, BY - 214, 442, BY - 204), (318, BY - 110, 442, BY - 100)]), GOLD, GOLD_D, seed=nx(), rough=0.3, pad=4)
    cols = rects(W, H, [(x, BY - 98, x + 6, BY - 18) for x in (334, 356, 398, 420)] + [(x, BY - 198, x + 5, BY - 112) for x in (336, 358, 397, 419)])
    art = GP(art, cols, "#fff4e4", "#e4cbb6", seed=nx(), rough=0.3, pad=4)
    door = shapes(W, H, [arch_pts(364, BY - 18, 32, 70, 12)], smooth=False)
    art = GP(art, door, "#f6c867", "#d98b45", seed=nx(), rough=0.3, pad=4)
    art = windows(art, W, H, nx, 368, 400, BY - 118, 24, 60, 40, random.Random(1))
    art = dome(art, W, H, cx, BY - 214, 92, 96, nx, 14)
    # four small finials on the portico corners
    for fx in (322, 438):
        art = GP(art, shapes(W, H, [onion_pts(fx, BY - 214, 14, 22)]), GOLD_L, GOLD, seed=nx(), rough=0.3, pad=4)
    # steps
    st = rects(W, H, [(352 - k * 6, BY - 18 + k * 5, 408 + k * 6, BY - 15 + k * 5) for k in range(3)])
    art = GP(art, st, "#e9d6c6", "#c7a99c", seed=nx(), rough=0.3, pad=4)
    # palms framing the palace
    for x, h_, ln in [(96, 170, 0.12), (140, 120, -0.08), (668, 178, -0.12), (716, 132, 0.1), (626, 96, 0.06)]:
        art = GP(art, jw.palm(W, H, x, WL - 20, h_, rng, ln), "#3b1f3a", "#2b1530", seed=nx(), rough=1.0, pad=6)
    # river
    river = painted_sky(W, H, [(0, "#e7a77d"), (WL / H, "#e7a77d"), (WL / H + 0.05, "#b46a74"), (0.8, "#5c2a52"), (1, "#2c1231")], seed=nx(), streak=1.2)
    water = rect(W, H, -10, WL, W + 10, H + 10)
    art = art * (1 - water[..., None]) + river * water[..., None]
    art = reflect(art, WL, strength=0.34, wave=5.0, fade=1.2)
    art[WL:] = gaussian_filter(art[WL:], (2.4, 1.2, 0))
    art = GP(art, ripples(W, H, rng, WL + 8, WL + 260, 80, 16, 64, 2.6, 4.2), "#f2b98a", seed=nx(), rough=0.6, density=0.55, pad=4)
    art = G(art, ripples(W, H, rng, WL + 40, H, 90, 30, 110, 1.4, 3), "#3a1636", seed=nx(), density=0.4, edge=0, bloom=0, rough=1, feather=0.5)
    # sun path on the water
    path = ripples(W, H, rng, WL + 6, WL + 300, 60, 12, 50, 3, 5, 560, 690)
    art = GP(art, path, "#ffd995", seed=nx(), rough=0.6, density=0.85, pad=4)
    art = add_grain(art, 3, 0.05)
    preview(art, "siak-scene")
    save_rgb(art, f"{OUT}/scene.webp", size=(608, 704), quality=78)
    clear()

if "boat" in PARTS:
    # kajang-roofed sampan (side view, facing left): dark hull, gold & red painted band, palm-leaf kajang hood
    W, H = 420, 180
    nx = Seq(32000)
    art = blank(W, H)
    hull = shapes(W, H, [[(10, 98), (40, 128), (90, 142), (330, 142), (384, 126), (412, 92), (392, 106), (30, 108)]])
    art = GP(art, hull, "#4a2a22", "#331a16", seed=nx(), rough=0.8, streak=1.2, pad=6)
    band = hull * rect(W, H, 0, 110, W, 118)
    art = GP(art, band, GOLD, GOLD_D, seed=nx(), rough=0.4, pad=4)
    band2 = hull * rect(W, H, 0, 121, W, 125)
    art = GP(art, band2, "#a3263c", seed=nx(), rough=0.4, pad=4)
    gun = strokes(W, H, [(curve([(14, 98), (120, 106), (300, 106), (408, 92)], 20), 4, None)])
    art = GP(art, gun, "#7a4a2c", seed=nx(), rough=0.3, pad=4)
    hood = shapes(W, H, [[(150, 104), (152, 74), (176, 54), (230, 46), (284, 54), (306, 74), (308, 104)]])
    art = GP(art, hood, "#b98a4e", "#8f6434", seed=nx(), rough=1.0, streak=1.4, pad=6)
    ribs = strokes(W, H, [(curve([(x, 104), (x + (x - 229) * 0.05, 74), (229 + (x - 229) * 0.6, 50)], 10), 1.4, None) for x in range(160, 300, 14)])
    art = G(art, ribs * hood, "#6d4423", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.3)
    art = G(art, side_shade(hood, 230, 320), "#5a361d", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.6)
    oar = strokes(W, H, [([(330, 100), (370, 170)], 3, None)])
    blade = shapes(W, H, [[(362, 152), (372, 150), (382, 176), (370, 178)]])
    art = GP(art, np.maximum(oar, blade), "#6b3f22", seed=nx(), rough=0.4, pad=4)
    wave = strokes(W, H, [(curve([(0, 140), (40, 136), (90, 146), (160, 148)], 16), 3.6, (0.2, 0.6)), (curve([(280, 148), (340, 144), (420, 150)], 12), 3, (0.2, 0.6))])
    art = GP(art, wave, "#f6cf8d", seed=nx(), rough=1.0, pad=6)
    preview(art, "siak-boat", bg="#7a3a5e")
    save(art, f"{OUT}/boat.webp", max_w=200, quality=84)
    clear()

if "songket" in PARTS:
    # seamless 240px tile: plum ground, fine weave, gold supplementary weft: bunga tabur stars on a wajik lattice
    S = 240
    nx = Seq(33000)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    base = solid(S, S, PLUM)
    tone = fbm(S, S, 5, 60, 3)
    base[..., :3] *= (0.92 + 0.12 * tone)[..., None]
    warp = (np.sin(xx * math.pi) * 0.5 + 0.5) * 0.05
    weft = (np.sin(yy * math.pi * 2 / 3) * 0.5 + 0.5) * 0.06
    base[..., :3] *= (1 - warp - weft)[..., None]
    motifs = []
    for cx_, cy_ in [(0, 0), (S, 0), (0, S), (S, S), (S / 2, S / 2)]:
        motifs.append(star8(cx_, cy_, 26, 0.4, math.pi / 8))
    small = [diamond(cx_, cy_, 7, 9) for cx_, cy_ in [(S / 2, 0), (S / 2, S), (0, S / 2), (S, S / 2)]]
    m = np.maximum(shapes(S, S, motifs, smooth=False), shapes(S, S, small, smooth=False))
    # wajik lattice lines (thin gold diagonal threads)
    lat = []
    for o in (-S, 0, S):
        lat.append(([(o, 0), (o + S, S)], 2.2, None))
        lat.append(([(o + S, 0), (o, S)], 2.2, None))
    lm = strokes(S, S, lat)
    holes = circles(S, S, [(x, y, 6) for x, y in [(0, 0), (S, 0), (0, S), (S, S), (S / 2, S / 2)]])
    mm = np.clip(np.maximum(m, lm * 0.9) - holes, 0, 1)
    wq = weave_q(mm, 3, 2)
    goldl = foil(wq, GOLD, seed=nx(), emboss=0.3, sparkle=0.15)
    goldl[..., 3] *= 0.92
    out = over(base, goldl)
    dots = weave_q(circles(S, S, [(x, y, 3.2) for x, y in [(0, 0), (S, 0), (0, S), (S, S), (S / 2, S / 2)]]), 3, 2)
    out = over(out, foil(dots, "#e86f8e", seed=nx(), emboss=0.2, sparkle=0))
    out[..., 3] = 1
    preview(np.concatenate([np.concatenate([out, out], 1)] * 2, 0), "siak-songket")
    save_rgb(out, f"{OUT}/songket.webp", quality=80)
    clear()

if "pucuk" in PARTS:
    # pucuk rebung band (seamless repeat-x, period 60px at 2x): gold woven triangles with inner shoots on transparent
    W, H = 600, 96
    nx = Seq(34000)
    tri, inner, ln = [], [], []
    for x in range(0, W + 60, 60):
        tri.append([(x - 26, 86), (x, 14), (x + 26, 86)])
        inner.append([(x - 13, 86), (x, 44), (x + 13, 86)])
        inner.append(diamond(x, 30, 4, 6))
        inner.append(diamond(x + 30, 72, 6, 8))
    t = shapes(W, H, tri, smooth=False)
    i = shapes(W, H, inner, smooth=False)
    band = rects(W, H, [(0, 86, W, 94)])
    m = np.clip(t - i * 0.0, 0, 1)
    m = np.clip(np.maximum(m - shapes(W, H, [[(x - 19, 86), (x, 33), (x + 19, 86)] for x in range(0, W + 60, 60)], smooth=False), 0) + shapes(W, H, [[(x - 13, 86), (x, 48), (x + 13, 86)] for x in range(0, W + 60, 60)], smooth=False), 0, 1)
    m = np.maximum(m, band)
    m = np.maximum(m, shapes(W, H, [diamond(x + 30, 66, 6, 9) for x in range(0, W, 60)], smooth=False))
    wq = weave_q(m, 3, 2)
    art = foil(wq, GOLD, seed=nx(), emboss=0.4, sparkle=0.15)
    preview(art, "siak-pucuk", bg=PLUM)
    save_full(art, f"{OUT}/pucuk.webp", size=(300, 48), quality=86)
    clear()

if "bunga" in PARTS:
    # bunga cengkih/tampuk manggis songket flower in gold weft with rose heart
    S = 200
    nx = Seq(35000)
    pet = shapes(S, S, [petal_pts(100, 100, 92, 30, a, n=14) for a in [k * math.pi / 4 for k in range(8)]])
    cut = shapes(S, S, [petal_pts(100, 100, 60, 10, a, n=12) for a in [k * math.pi / 4 for k in range(8)]])
    ring = circles(S, S, [(100, 100, 26)])
    m = np.clip(pet - cut * 0.9, 0, 1)
    m = np.clip(m - ring, 0, 1)
    wq = weave_q(m, 3, 2)
    art = foil(wq, GOLD, seed=nx(), emboss=0.4, sparkle=0.15)
    heart = weave_q(np.clip(ring - circles(S, S, [(100, 100, 12)]) * 0.0, 0, 1) * (1 - circles(S, S, [(100, 100, 21)]) + circles(S, S, [(100, 100, 12)])), 3, 2)
    art = over(art, foil(heart, ROSE, seed=nx(), emboss=0.3, sparkle=0))
    preview(art, "siak-bunga", bg=PLUM)
    save(art, f"{OUT}/bunga.webp", max_w=96, quality=86)
    clear()

if "divider" in PARTS:
    W, H = 560, 70
    nx = Seq(36000)
    line = rects(W, H, [(20, 33, 230, 37), (330, 33, 540, 37)])
    tips = shapes(W, H, [[(10, 35), (40, 31), (40, 39)], [(550, 35), (520, 31), (520, 39)]], smooth=False)
    ds = shapes(W, H, [diamond(280, 35, 34, 30), diamond(232, 35, 12, 14), diamond(328, 35, 12, 14)] + [diamond(x, 35, 5, 6) for x in (90, 150, 410, 470)], smooth=False)
    hole = shapes(W, H, [diamond(280, 35, 22, 19)], smooth=False)
    core = shapes(W, H, [diamond(280, 35, 11, 10)], smooth=False)
    m = np.maximum(np.maximum(line, tips), np.clip(ds - hole, 0, 1))
    wq = weave_q(m, 3, 2)
    art = foil(wq, GOLD, seed=nx(), emboss=0.4, sparkle=0.15)
    art = over(art, foil(weave_q(core, 3, 2), ROSE, seed=nx(), emboss=0.3, sparkle=0))
    preview(art, "siak-divider", bg="#f6ead8")
    save(art, f"{OUT}/divider.webp", max_w=280, quality=86)
    clear()
