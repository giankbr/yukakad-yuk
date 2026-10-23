"""Loft Industri — loft industrial: dinding bata ekspos, jendela rangka baja hitam, bohlam Edison di ujung kabel,
pot beton dengan sirih gading menjuntai; gouache hangat dan suram. Run: python3 -I loft-industri.py [part ...]
parts: bata jendela bohlam tanaman beton pipa     Assets -> public/themes/art/loft-industri/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m5_lib import *

OUT = outdir("loft-industri")
PARTS = sys.argv[1:] or ["bata", "jendela", "bohlam", "tanaman", "beton", "pipa"]
STEEL, STEEL_L, RUST = "#1c1d1f", "#4d5054", "#6e3b22"
AMBER, AMBER_L = "#ffb54d", "#fff0c2"
LEAF_A, LEAF_B, LEAF_C, LEAF_L = "#2f5d33", "#467f3d", "#5f9a48", "#a9c77a"


def h2(i, j, k=0):
    v = math.sin(i * 127.1 + j * 311.7 + k * 74.7) * 43758.5453
    return v - math.floor(v)


if "bata" in PARTS:
    clear()
    BW, BH, M = 64, 26, 4
    W, H = BW * 6, BH * 12
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (tile_noise(W, H, 1, 2.0) - 0.5) * 3.2; dy = (tile_noise(W, H, 2, 2.0) - 0.5) * 3.2
    X = (xx + dx) % W; Y = (yy + dy) % H
    row = np.floor(Y / BH).astype(int)
    off = (row % 2) * (BW // 2)
    col = np.floor(((X + off) % W) / BW).astype(int)
    u = (X + off) % BW; v = Y % BH
    brick = ((u >= M) & (v >= M)).astype(np.float32)
    brick = gaussian_filter(brick, 0.7)
    pal = [np.array(hex_rgb(c), np.float32) for c in ("#9a4a33", "#b05b3c", "#86402d", "#a6553a", "#7a3b2b", "#b8664a", "#8e4b36")]
    nrow, ncol = H // BH, W // BW
    cols = np.zeros((nrow, ncol, 3), np.float32); shade = np.zeros((nrow, ncol), np.float32)
    for i in range(nrow):
        for j in range(ncol):
            cols[i, j] = pal[int(h2(i, j) * len(pal))] * (0.9 + 0.2 * h2(i, j, 1))
            shade[i, j] = h2(i, j, 2)
    rgb = cols[row % nrow, col % ncol]
    tex = tile_noise(W, H, 3, 1.2); low = tile_noise(W, H, 4, 9)
    rgb = rgb * (0.82 + 0.22 * tex[..., None]) * (0.9 + 0.16 * low[..., None])
    # bevel: lighter top edge, darker bottom of each brick
    rgb *= (1.06 - 0.16 * np.clip((v - M) / (BH - M), 0, 1))[..., None]
    pits = (tile_noise(W, H, 5, 0.6) > 0.82).astype(np.float32) * 0.25
    rgb *= (1 - pits)[..., None]
    mortar = np.array(hex_rgb("#b3a593"), np.float32) * (0.8 + 0.3 * tile_noise(W, H, 6, 0.8))[..., None]
    out = mortar * (1 - brick[..., None]) + rgb * brick[..., None]
    # whitewash residue + soot from years of use
    ww = np.clip((tile_noise(W, H, 7, 22) - 0.62) * 3.2, 0, 1) * (0.45 + 0.4 * tile_noise(W, H, 8, 1.5))
    out = out * (1 - ww[..., None] * 0.5) + np.array(hex_rgb("#e2d6c6"), np.float32) * ww[..., None] * 0.5
    soot = np.clip((tile_noise(W, H, 9, 30) - 0.55) * 2, 0, 1) * 0.22
    out *= (1 - soot)[..., None]
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGB")
    img.save(f"{OUT}/bata.webp", "WEBP", quality=74, method=6)
    img.save(f"{PREV}/lf-bata.png")
    print("bata", os.path.getsize(f"{OUT}/bata.webp") // 1024, "KB")

if "beton" in PARTS:
    clear()
    S = 320
    base = np.array(hex_rgb("#a7a39c"), np.float32)
    n1 = tile_noise(S, S, 11, 30); n2 = tile_noise(S, S, 12, 5); n3 = tile_noise(S, S, 13, 1.0)
    out = np.ones((S, S, 3), np.float32) * base * (0.86 + 0.14 * n1[..., None] + 0.08 * (n2[..., None] - 0.5) + 0.07 * (n3[..., None] - 0.5))
    pores = (tile_noise(S, S, 14, 0.7) > 0.86).astype(np.float32)
    out *= (1 - gaussian_filter(pores, 0.5, mode="wrap") * 0.35)[..., None]
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGB")
    img.save(f"{OUT}/beton.webp", "WEBP", quality=70, method=6)
    print("beton", os.path.getsize(f"{OUT}/beton.webp") // 1024, "KB")


def steel(dst, mask, seed, rust=0.35):
    out = GP(dst, mask, STEEL, "#2a2b2e", seed=seed, rough=1.2, streak=0.9)
    gy, gx = np.gradient(gaussian_filter(mask, 1.4))
    rim = np.clip(-(gx * 0.6 + gy) * 3.2, 0, 1) * mask
    out = OV(out, rim, lambda m: rgba(flat(*m.shape, STEEL_L), np.clip(m * 0.9, 0, 1)), pad=4)
    if rust:
        h, w = mask.shape
        rs = np.clip((fbm(w, h, seed + 5, 14, 3) - 0.7) * 4, 0, 1) * mask * rust
        out = OV(out, rs, lambda m: rgba(flat(*m.shape, RUST), np.clip(m, 0, 1)), pad=4)
    return out


if "jendela" in PARTS:
    clear()
    W, H = 640, 820
    art = blank(W, H)
    F, MU = 22, 10
    cols, rows = 3, 4
    polys = [[(0, 0), (W, 0), (W, F), (0, F)], [(0, H - F), (W, H - F), (W, H), (0, H)], [(0, 0), (F, 0), (F, H), (0, H)], [(W - F, 0), (W, 0), (W, H), (W - F, H)]]
    for c in range(1, cols):
        x = F + c * (W - 2 * F) / cols
        polys.append([(x - MU / 2, 0), (x + MU / 2, 0), (x + MU / 2, H), (x - MU / 2, H)])
    for r_ in range(1, rows):
        y = F + r_ * (H - 2 * F) / rows
        polys.append([(0, y - MU / 2), (W, y - MU / 2), (W, y + MU / 2), (0, y + MU / 2)])
    # the middle transom row is a heavier rail (pivot window)
    yb = F + 2 * (H - 2 * F) / rows
    polys.append([(0, yb - 9), (W, yb - 9), (W, yb + 9), (0, yb + 9)])
    frame = shapes(W, H, polys, smooth=False)
    # glass: faint grime at the corners + a single soft reflection band
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    glass = 1 - frame
    refl = np.clip(1 - np.abs((xx * 0.8 - yy * 0.55) - 120) / 60, 0, 1) * 0.12 + np.clip(1 - np.abs((xx * 0.8 - yy * 0.55) - 30) / 14, 0, 1) * 0.08
    grime = np.clip(gaussian_filter(frame, 14) * 1.6 - 0.2, 0, 1) * 0.28 * (0.5 + fbm(W, H, 3, 30, 3))
    art = over(art, rgba(flat(H, W, "#fff4dc"), refl * glass))
    art = over(art, rgba(flat(H, W, "#3a3026"), grime * glass))
    art = steel(art, frame, 21)
    riv = []
    for c in range(cols + 1):
        x = F / 2 if c == 0 else (W - F / 2 if c == cols else F + c * (W - 2 * F) / cols)
        for r_ in range(rows + 1):
            y = F / 2 if r_ == 0 else (H - F / 2 if r_ == rows else F + r_ * (H - 2 * F) / rows)
            riv.append((x, y, 3.2))
    art = OV(art, circles(W, H, riv), lambda m: rgba(flat(*m.shape, "#5c5f63"), m), pad=4)
    # small latch handle on the pivot rail
    lat = shapes(W, H, [[(W / 2 - 26, yb - 4), (W / 2 + 26, yb - 4), (W / 2 + 26, yb + 4), (W / 2 - 26, yb + 4)]], smooth=False)
    art = steel(art, lat, 23, 0)
    preview(art, "lf-jendela", bg="#8a7a66")
    save_full(art, f"{OUT}/jendela.webp", size=(320, 410), quality=82)

if "bohlam" in PARTS:
    clear()
    W, H = 320, 1400
    OY = 420
    art = blank(W, H)
    cx = 160
    by = 760 + OY  # bulb centre
    cord = strokes(W, H, [([(cx, 0), (cx + 1, 500), (cx, 600 + OY)], 5, None)])
    sock = shapes(W, H, [[(cx - 20, 600 + OY), (cx + 20, 600 + OY), (cx + 22, 676 + OY), (cx - 22, 676 + OY)]], smooth=False)
    rings = shapes(W, H, [[(cx - 23, 640 + OY + k * 10), (cx + 23, 640 + OY + k * 10), (cx + 23, 644 + OY + k * 10), (cx - 23, 644 + OY + k * 10)] for k in range(3)], smooth=False)
    neck = shapes(W, H, [[(cx - 18, 676 + OY), (cx + 18, 676 + OY), (cx + 24, 700 + OY), (cx - 24, 700 + OY)]], smooth=False)
    bulb_pts = [(cx + math.cos(a) * 62, by + math.sin(a) * 74) for a in np.linspace(-math.pi * 0.28, math.pi * 1.28, 60)]
    bulb_pts = [(cx + 22, 700 + OY)] + bulb_pts + [(cx - 22, 700 + OY)]
    bulb_pts = [(cx - 22, 700 + OY), (cx + 22, 700 + OY)] + [(cx + math.sin(t) * 62, by - math.cos(t) * 74 * 0.95) for t in np.linspace(0.55, math.tau - 0.55, 60)]
    bulb = shape_mask(W, H, bulb_pts)
    # glow
    art = over(art, glow(bulb, AMBER, radius=48, strength=0.36))
    art = over(art, glow(bulb, AMBER_L, radius=18, strength=0.3))
    # glass: warm tint, brighter towards the filament, rim light
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(np.hypot((xx - cx) / 60, (yy - by) / 70), 0, 1)
    gl = np.stack([np.ones_like(d), 0.78 - 0.18 * d, 0.42 - 0.25 * d], -1)
    art = over(art, rgba(gl, bulb * (0.42 + 0.3 * (1 - d))))
    rim = outline_of(bulb, 2.4) * 0.6
    art = OV(art, rim, lambda m: rgba(flat(*m.shape, "#ffe7b0"), m), pad=4)
    # filament: squirrel-cage loops between two posts
    posts = [[(cx - 10, 700 + OY), (cx - 14, by - 4)], [(cx + 10, 700 + OY), (cx + 14, by - 4)]]
    loops = []
    for k in range(5):
        x0 = cx - 26 + k * 13
        loops.append([(x0, by - 34), (x0 + 6, by + 30), (x0 + 13, by - 34)])
    fil = lines(W, H, loops, 2.2, closed=False, smooth=True)
    art = over(art, glow(fil, "#ffd27a", radius=8, strength=0.9))
    art = OV(art, fil, lambda m: rgba(flat(*m.shape, "#fff6d6"), np.clip(m * 1.2, 0, 1)))
    art = OV(art, lines(W, H, posts, 1.4, closed=False, smooth=False), lambda m: rgba(flat(*m.shape, "#8c6a3a"), m * 0.8))
    art = GP(art, cord, "#111111", "#262626", seed=5, rough=0.6, streak=0.4)
    art = FO(art, np.clip(sock + neck, 0, 1), "#9a7a3e", seed=6, emboss=0.9, sparkle=0.05)
    art = OV(art, rings, lambda m: rgba(flat(*m.shape, "#3d2e18"), m * 0.8))
    art = K(art, outline_of(np.clip(sock + neck, 0, 1), 1.2), "#2a1d0c", seed=7)
    preview(art, "lf-bohlam", bg="#3a2a22")
    save(art, f"{OUT}/bohlam.webp", max_w=130, quality=82)


def heart_leaf(x, y, L, ang, rng):
    pts = []
    for t in np.linspace(0, math.tau, 40, endpoint=False):
        # heart curve along +x then rotated
        hx = 16 * math.sin(t) ** 3
        hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((-hy / 17 * L * 0.55 + L * 0.5, hx / 17 * L * 0.5))
    pts = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts]
    return wob(pts, rng, L * 0.02)


if "tanaman" in PARTS:
    clear()
    W, H = 560, 760
    art = blank(W, H)
    rng = random.Random(4)
    nx = Seq(900)
    # concrete pot
    pot = shapes(W, H, [[(170, 150), (390, 150), (372, 330), (188, 330)]], smooth=False)
    lipm = shapes(W, H, [[(160, 134), (400, 134), (400, 162), (160, 162)]], smooth=False)
    soil = shapes(W, H, [ellipse_pts(280, 136, 112, 10, 20)])
    vines = []
    leaves = []
    starts = [(200, 140, -1), (250, 136, -1), (310, 136, 1), (360, 140, 1), (280, 134, 0)]
    for k, (sx, sy, d) in enumerate(starts):
        pts = [(sx, sy)]
        x, y = sx, sy
        if d == 0:
            seg = [(x, y), (x - 10, y - 60), (x + 6, y - 110)]
            vines.append(seg)
            for j, (px, py) in enumerate(seg[1:]):
                leaves.append((px, py, 70 - j * 10, -math.pi / 2 + rng.uniform(-.6, .6)))
            continue
        length = rng.uniform(380, 560)
        steps = 14
        for i in range(steps):
            t = (i + 1) / steps
            x = sx + d * (26 + 34 * t) * min(1, t * 3) + math.sin(t * 6 + k) * 14
            y = sy + 40 + length * t
            pts.append((x, y))
        vines.append(pts)
        for i, (px, py) in enumerate(pts[1:]):
            if i % 2 == 0 or i > steps - 3:
                side = 1 if i % 4 == 0 else -1
                leaves.append((px, py, 64 - i * 2.4, math.pi / 2 + d * 0.2 + side * rng.uniform(0.5, 1.1)))
    # upward leaves over the rim
    for a in (-2.2, -1.9, -1.4, -1.1, -0.8):
        leaves.append((280 + math.cos(a) * 60, 140 + math.sin(a) * 30, 78, a))
    vm = strokes(W, H, [(curve(v, 60), 4.2, (0.0, 0.5)) for v in vines])
    art = GP(art, pot, "#9e9a93", "#86827b", seed=nx(), rough=1.6, streak=0.9)
    art = GP(art, lipm, "#b1ada6", "#99958e", seed=nx(), rough=1.2)
    pores = circles(W, H, [(rng.uniform(175, 385), rng.uniform(140, 325), rng.uniform(1, 2.2)) for _ in range(90)]) * np.clip(pot + lipm, 0, 1)
    art = OV(art, pores, lambda m: rgba(flat(*m.shape, "#5e5a55"), m * 0.7))
    shadow = np.clip(np.linspace(0, 1, W)[None, :] * np.ones((H, 1)), 0, 1).astype(np.float32)
    art = OV(art, pot * shadow * 0.35, lambda m: rgba(flat(*m.shape, "#2b2926"), m))
    art = GP(art, soil, "#3a2a1e", seed=nx())
    art = GP(art, vm, "#4f6d32", "#3c5a2a", seed=nx(), rough=1)
    for (x, y, L, a) in leaves:
        poly = heart_leaf(x, y, L, a, rng)
        m = shape_mask(W, H, poly)
        c1, c2 = rng.choice([(LEAF_A, LEAF_B), (LEAF_B, LEAF_C), (LEAF_C, LEAF_B)])
        art = GP(art, m, c1, c2, seed=nx(), rough=1.4, streak=0.8)
        # pothos variegation streaks + midrib
        ex, ey = x + math.cos(a) * L * 0.95, y + math.sin(a) * L * 0.95
        st = strokes(W, H, [([(x + math.cos(a) * L * 0.15, y + math.sin(a) * L * 0.15), (ex, ey)], 2.0, (0.1, 0.5))] +
                     [([(x + math.cos(a) * L * t, y + math.sin(a) * L * t), (x + math.cos(a + s_ * 0.7) * L * (t + 0.25), y + math.sin(a + s_ * 0.7) * L * (t + 0.25))], 2.6, (0.2, 0.6))
                      for t in (0.3, 0.5) for s_ in (-1, 1) if rng.random() < 0.7]) * m
        art = OV(art, st, lambda mm: rgba(flat(*mm.shape, LEAF_L), np.clip(mm * 0.75, 0, 1)), pad=4)
        gy, gx = np.gradient(gaussian_filter(m, 2))
        lit = np.clip(-(gx + gy) * 2.5, 0, 1) * m
        art = OV(art, lit, lambda mm: rgba(flat(*mm.shape, "#e8c886"), np.clip(mm * 0.45, 0, 1)), pad=4)
    preview(art, "lf-tanaman", bg="#5a3a2c")
    save(art, f"{OUT}/tanaman.webp", max_w=260, quality=82)

if "pipa" in PARTS:
    # divider: a black iron pipe with flanges, a tiny bulb hanging in the middle
    clear()
    W, H = 560, 150
    art = blank(W, H)
    pipe = shapes(W, H, [[(30, 40), (530, 40), (530, 54), (30, 54)]], smooth=False)
    fl = shapes(W, H, [[(x - 9, 32), (x + 9, 32), (x + 9, 62), (x - 9, 62)] for x in (40, 200, 360, 520)], smooth=False)
    cord = strokes(W, H, [([(280, 54), (280, 84)], 3, None)])
    art = steel(art, np.clip(pipe + fl + cord, 0, 1), 31, 0.2)
    bulb = shape_mask(W, H, ellipse_pts(280, 108, 15, 19, 20))
    art = over(art, glow(bulb, AMBER, radius=16, strength=0.5))
    art = OV(art, bulb, lambda m: rgba(flat(*m.shape, "#ffd894"), m * 0.85))
    art = OV(art, lines(W, H, [[(273, 100), (276, 116), (280, 100), (284, 116), (287, 100)]], 1.4, closed=False, smooth=False), lambda m: rgba(flat(*m.shape, "#fff6d6"), m))
    art = FO(art, shapes(W, H, [[(272, 84), (288, 84), (290, 94), (270, 94)]], smooth=False), "#9a7a3e", seed=3)
    preview(art, "lf-pipa", bg="#e7e1d8")
    save(art, f"{OUT}/pipa.webp", max_w=280, quality=84)

kb(OUT)
