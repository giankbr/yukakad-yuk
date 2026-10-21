"""Banjar Sasirangan — green, yellow and maroon tie-dye on cream: hanging sasirangan cloth strip and band (jelujur
stitch resist lines, gigi haruan zigzags, kulat kurikit dots, dye bleeding across seams), watercolour river scene with
rumah Bubungan Tinggi on stilts, nipah palms and jukung boats laden with fruit (no figures), a lone floating jukung,
and a kembang divider. Run: python3 -I banjar-sasirangan.py [part ...]  parts: kain band sungai jukung divider."""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a1_lib import *

OUT = outdir("banjar-sasirangan")
PARTS = sys.argv[1:] or ["kain", "band", "sungai", "jukung", "divider"]
CREAM = "#f5eedc"
GRN, GRN_D = "#2f6b3a", "#1d4626"
YEL = "#e3b23c"
MAR, MAR_D = "#7a1f2b", "#4c1018"
WOOD, WOOD_D = "#6a4326", "#3c2414"


def sasirangan(W, H, seed, vertical=True, ncols=4, amp=10, period=110, scale=1.0):
    """Tie-dyed cloth (opaque RGBA). Stripes run along the long axis; boundaries are stitched wavy resist lines."""
    nx = Seq(seed)
    L, S = (H, W) if vertical else (W, H)
    cloth = cloth_base(W, H, CREAM, seed=nx(), cell=2.0, var=0.06)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = yy if vertical else xx       # along stripe
    v = xx if vertical else yy       # across
    bounds = [S * k / ncols for k in range(1, ncols)]
    wav = lambda b, k: b + amp * np.sin(u / period * math.tau + k * 1.7)
    region = np.zeros((H, W), np.int32)
    for k, b in enumerate(bounds):
        region += (v > wav(b, k)).astype(np.int32)
    palette = [GRN, YEL, MAR, YEL, GRN, MAR]
    order = [1, 3, 0, 4, 2, 5]  # light dyes first
    art = cloth
    resist = np.zeros((H, W), np.float32)
    # resist lines along boundaries (doubled running stitch), zigzags and dot clusters inside regions
    lines, zz, dots = [], [], []
    for k, b in enumerate(bounds):
        for off in (-4, 4):
            pts = [((b + off + amp * math.sin(t / period * math.tau + k * 1.7)), t) for t in range(-10, L + 11, 6)]
            lines.append([(p[0], p[1]) if vertical else (p[1], p[0]) for p in pts])
    cw = S / ncols
    for c in range(ncols):
        cx = cw * (c + 0.5)
        kind = c % 3
        if kind == 0:   # gigi haruan: zigzag teeth
            for side in (-1, 1):
                pts = []
                for j, t in enumerate(range(-20, L + 21, 14)):
                    pts.append((cx + side * cw * 0.18 + (cw * 0.1 if j % 2 else -cw * 0.02) * side, t))
                zz.append([(p[0], p[1]) if vertical else (p[1], p[0]) for p in pts])
        elif kind == 1:  # kulat kurikit: dot clusters
            for t in range(20, L, 44):
                for (dx, dy) in [(0, 0), (-9, 7), (9, 7), (0, 14)]:
                    p = (cx + dx * scale + (8 if (t // 44) % 2 else -8), t + dy * scale)
                    dots.append(p if vertical else (p[1], p[0]))
        else:            # hiris gagatas: diamond chain
            for t in range(10, L, 40):
                d = [(cx, t - 14), (cx + 9, t), (cx, t + 14), (cx - 9, t)]
                d = d + [d[0]]
                zz.append([(p[0], p[1]) if vertical else (p[1], p[0]) for p in d])
    resist = np.maximum.reduce([wax_line(W, H, lines, 2.2, nx()), wax_line(W, H, zz, 2.6, nx()), circles(W, H, [(x, y, 3.2 * scale) for x, y in dots])])
    # stitch holes: dotted darker pinpricks along the resist lines
    holes = np.clip((np.sin(u * 1.2) > 0.9).astype(np.float32) * resist, 0, 1)
    for idx in order:
        if idx >= ncols:
            continue
        m = (region == idx).astype(np.float32)
        col = palette[idx]
        layer = tie_dye(m, col, seed=nx(), bleed=4.0, density=0.95, resist=resist)
        art = dye_on(art, layer)
    # dye halo around dots (pigment ring where the tied pucker trapped dye)
    ring_m = np.clip(gaussian_filter(circles(W, H, [(x, y, 5.5 * scale) for x, y in dots]), 1.2) - circles(W, H, [(x, y, 3.4 * scale) for x, y in dots]), 0, 1)
    art = dye_on(art, flat(ring_m * 0.6, MAR_D))
    art = dye_on(art, flat(holes * 0.5, "#8a7a62"))
    art[..., :3] *= (0.96 + 0.06 * fbm(W, H, nx(), 70, 3))[..., None]
    art[..., 3] = 1
    return np.clip(art, 0, 1)


if "kain" in PARTS:
    W, H = 200, 1100
    art = sasirangan(W, H, 60100, vertical=True, ncols=3, amp=9, period=120)
    # selvage + fold shading (cloth hanging): soft vertical shadow folds
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    fold = 1 - 0.1 * (np.sin(xx * math.pi * 3 + 0.6) * 0.5 + 0.5)
    art[..., :3] *= fold[..., None]
    # frayed bottom edge
    fr = np.ones((H, W), np.float32)
    edge = (H - 18 + (fbm(W, 40, 7, 4, 2)[0] * 18)).astype(np.int32)
    for x in range(W):
        fr[edge[x]:, x] = 0
    for x in range(2, W, 5):
        fr[H - 30:H - 4, x] = 1
    art[..., 3] = np.clip(gaussian_filter(fr, 0.6), 0, 1)
    save_full(art, f"{OUT}/kain.webp", size=(140, 770), quality=78)
    clear()

if "band" in PARTS:
    W, H = 900, 110
    art = sasirangan(W, H, 60200, vertical=False, ncols=3, amp=6, period=150, scale=0.8)
    save_rgb(art, f"{OUT}/band.webp", size=(780, 95), quality=78)
    clear()

if "sungai" in PARTS:
    W, H = 900, 520
    nx = Seq(60300); rng = random.Random(4)
    art = blank(W, H)
    sky = shapes(W, H, [[(-20, -20), (W + 20, -20), (W + 20, 300), (-20, 300)]], smooth=False)
    art = G(art, sky * np.clip(1 - np.linspace(0, 1, H)[:, None] * 1.6, 0, 1), "#f0d9a6", "#e9c37a", seed=nx(), density=0.5, edge=0.1, bloom=0.4, rough=12, feather=10)
    # distant tree line (rumbia / nipah)
    import _jw_lib as jw
    trees = jw.hills(W, H, 236, 18, 3, 0.25)
    art = G(art, trees * (np.arange(H)[:, None] < 300), "#7f9d6a", "#5e7d50", seed=nx(), density=0.6, edge=0.4, bloom=0.4, rough=8)
    nip = []
    x = 0
    while x < W + 20:
        b = 232 - rng.uniform(0, 18)
        sc_ = rng.uniform(0.6, 1.4)
        for a in (-2.6, -2.2, -1.85, -1.5, -1.2, -0.9, -0.55):
            L = rng.uniform(30, 48) * sc_
            nip.append((curve([(x, b), (x + math.cos(a) * L * 0.6, b + math.sin(a) * L * 0.6), (x + math.cos(a) * L, b + math.sin(a) * L * 0.45 + 12 * sc_)], 12), 4.5 * sc_, (0.0, 0.7)))
        x += rng.uniform(16, 70)
    art = G(art, strokes(W, H, nip), "#5e7d50", "#43603b", seed=nx(), density=0.7, edge=0.4, bloom=0.2, rough=3)
    # river: wide band with horizontal wash streaks
    river = shapes(W, H, [[(-20, 300), (W + 20, 296), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    art = G(art, river, "#8fb0a0", "#6f8f86", seed=nx(), density=0.7, edge=0.2, bloom=0.5, rough=10, feather=4)
    deep = river * np.clip((np.arange(H)[:, None] - 330) / 190, 0, 1) * np.ones((1, W), np.float32)
    art = G(art, deep, "#4f7068", "#3d5a55", seed=nx(), density=0.55, edge=0, bloom=0.5, rough=6, feather=6)
    streak = river * hatch(W, H, 0.0, 9, 0.12, nx(), 4.0) * fbm(W, H, nx(), 50, 3)
    art = G(art, streak, "#4f7068", seed=nx(), density=0.5, edge=0, bloom=0, rough=2)
    # rumah Bubungan Tinggi on stilts at right bank: very steep central roof, lower side wings (anjung), front porch roof
    hx, by = 560, 334
    S_ = 1.32
    body = shapes(W, H, [[(hx - 120 * S_, by - 70 * S_), (hx + 120 * S_, by - 70 * S_), (hx + 120 * S_, by), (hx - 120 * S_, by)]], smooth=False)
    roof_c = shapes(W, H, [[(hx - 70 * S_, by - 64 * S_), (hx, by - 230 * S_), (hx + 70 * S_, by - 64 * S_)]], smooth=False)
    roof_w = shapes(W, H, [[(hx - 150 * S_, by - 58 * S_), (hx - 108 * S_, by - 120 * S_), (hx - 60 * S_, by - 120 * S_), (hx - 48 * S_, by - 58 * S_)], [(hx + 48 * S_, by - 58 * S_), (hx + 60 * S_, by - 120 * S_), (hx + 108 * S_, by - 120 * S_), (hx + 150 * S_, by - 58 * S_)]], smooth=False)
    porch = shapes(W, H, [[(hx - 100 * S_, by - 30 * S_), (hx - 70 * S_, by - 64 * S_), (hx + 70 * S_, by - 64 * S_), (hx + 100 * S_, by - 30 * S_)]], smooth=False)
    stilts = polyline_mask(W, H, [[(x, by), (x, by + 48 * S_)] for x in range(int(hx - 112 * S_), int(hx + 121 * S_), 30)], 5)
    deck = polyline_mask(W, H, [[(hx - 140 * S_, by + 2 * S_), (hx + 140 * S_, by + 2 * S_)]], 6)
    house_all = np.maximum.reduce([body, roof_c, roof_w, porch])
    art = knockout(art, house_all, amount=1.0, grow=1.0)
    art = G(art, np.maximum(stilts, deck), WOOD_D, seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=2)
    art = G(art, body, "#b07444", WOOD, seed=nx(), density=0.98, edge=0.55, bloom=0.3, rough=3)
    boards = body * hatch(W, H, 1.5708, 8, 0.1, nx(), 0.8)
    art = G(art, boards, WOOD_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    wins = shapes(W, H, [[(x, by - 56 * S_), (x + 18 * S_, by - 56 * S_), (x + 18 * S_, by - 22 * S_), (x, by - 22 * S_)] for x in (hx - 100 * S_, hx - 64 * S_, hx + 46 * S_, hx + 82 * S_)] + [[(hx - 14 * S_, by - 58 * S_), (hx + 14 * S_, by - 58 * S_), (hx + 14 * S_, by), (hx - 14 * S_, by)]], smooth=False)
    art = G(art, wins, "#3a2416", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=1.5)
    art = G(art, np.maximum(roof_w, porch), "#7a4a2c", "#5a321c", seed=nx(), density=0.9, edge=0.6, bloom=0.3, rough=3)
    art = G(art, roof_c, "#6a3e24", "#4a2a16", seed=nx(), density=1.0, edge=0.6, bloom=0.25, rough=3)
    shingles = np.maximum(roof_c, np.maximum(roof_w, porch)) * hatch(W, H, 0.0, 6, 0.12, nx(), 1.2)
    art = G(art, shingles, "#2e1a0e", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # ridge ornaments (layang-layang / jamang) on the roof peak and gable ends
    orn = polyline_mask(W, H, [[(hx - 10, by - 222), (hx, by - 248), (hx + 10, by - 222)], [(hx - 108, by - 122), (hx - 112, by - 140)], [(hx + 108, by - 122), (hx + 112, by - 140)]], 3.5)
    art = G(art, orn, "#3a2416", seed=nx(), density=0.9, edge=0.4, rough=1)
    # dye accent: a sasirangan cloth hanging at the porch rail
    cloth_m = shapes(W, H, [[(hx - 46, by - 26), (hx - 20, by - 26), (hx - 22, by + 4), (hx - 44, by + 6)]], smooth=False)
    art = G(art, cloth_m, YEL, GRN, seed=nx(), density=0.85, edge=0.5, rough=1.5)
    # reflection of the house in the river
    refl = np.flipud(np.maximum.reduce([body, roof_c, roof_w, stilts]))
    shift = 2 * int(by + 48 * S_) - H
    refl = np.roll(refl, shift, 0) * river
    refl = refl * hatch(W, H, 0.0, 5, 0.32, nx(), 3.0)
    art = G(art, refl, "#5d4a38", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=4)
    # jukung boats with fruit (pasar terapung) in the foreground
    def jukung(cx, cy, L, col, fruit):
        hull = shapes(W, H, [[(cx - L, cy - 8), (cx - L * 0.7, cy + 10), (cx + L * 0.7, cy + 10), (cx + L, cy - 8), (cx + L * 0.6, cy - 2), (cx - L * 0.6, cy - 2)]])
        load = circles(W, H, [(cx + rng.uniform(-L * 0.45, L * 0.45), cy - 8 - rng.uniform(0, L * 0.1), rng.uniform(4, 7) * L / 80) for _ in range(16)])
        return hull, load
    boats = [(230, 420, 110, "#4a2c18", True), (90, 360, 60, "#5a3820", True), (420, 474, 86, "#4a2c18", True), (800, 440, 70, "#5a3820", True)]
    for (cx, cy, L, col, fr) in boats:
        hull, load = jukung(cx, cy, L, col, fr)
        art = G(art, np.roll(hull, 14, 0) * river, "#3e5650", seed=nx(), density=0.35, edge=0, bloom=0.2, rough=4, feather=3)
        art = GP(art, load, "#e39a2a", "#c4542a", seed=nx(), rough=1.0, pad=8)
        art = GP(art, load * (fbm(W, H, nx(), 9, 2) > 0.5), "#6f9a3c", "#4f7a2a", seed=nx(), rough=1.0, pad=8)
        art = G(art, hull, col, "#2e1a0e", seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=2)
        # tanggui hat shapes left as empty boat? keep only cargo + a paddle resting across
        pad = polyline_mask(W, H, [[(cx + L * 0.2, cy - 4), (cx + L * 0.9, cy + 26)]], 3)
        art = G(art, pad, WOOD_D, seed=nx(), density=0.85, edge=0.3, rough=1)
    # ripples
    rip = polyline_mask(W, H, [[(x, y), (x + rng.uniform(20, 50), y)] for x, y in [(rng.uniform(0, W), rng.uniform(320, 510)) for _ in range(40)]], 2)
    art = G(art, rip, "#e8efe8", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # fade the edges into the paper (vignette in alpha) so it sits softly on the page
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(np.minimum.reduce([xx / 60, (W - xx) / 60, yy / 50, (H - yy) / 30]), 0, 1)
    art[..., 3] *= fade
    preview(art, "bs-sungai", CREAM)
    save_full(art, f"{OUT}/sungai.webp", size=(720, 416), quality=74)
    clear()

if "jukung" in PARTS:
    W, H = 300, 120
    nx = Seq(60400); rng = random.Random(9)
    cx, cy, L = 150, 70, 120
    hull = shapes(W, H, [[(cx - L, cy - 12), (cx - L * 0.7, cy + 16), (cx + L * 0.7, cy + 16), (cx + L, cy - 12), (cx + L * 0.6, cy - 2), (cx - L * 0.6, cy - 2)]])
    load = [(cx + rng.uniform(-60, 60), cy - 12 - rng.uniform(0, 14), rng.uniform(8, 12)) for _ in range(16)]
    art = blank(W, H)
    art = G(art, circles(W, H, load[::2]), "#e0a330", "#c45a2a", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=2)
    art = G(art, circles(W, H, load[1::2]), "#6f9a3c", "#4f7a2a", seed=nx(), density=0.9, edge=0.5, bloom=0.2, rough=2)
    art = G(art, hull, "#5a3820", "#2e1a0e", seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=2.5)
    rim = polyline_mask(W, H, [[(cx - L * 0.9, cy - 8), (cx + L * 0.9, cy - 8)]], 3)
    art = G(art, rim, YEL, seed=nx(), density=0.8, edge=0.3, rough=1)
    wake = polyline_mask(W, H, [[(cx - L * 0.8, cy + 22), (cx - L * 0.2, cy + 24)], [(cx + L * 0.1, cy + 25), (cx + L * 0.75, cy + 22)]], 3)
    art = G(art, wake, "#6f8f86", seed=nx(), density=0.6, edge=0.2, rough=2)
    preview(art, "bs-jukung", CREAM)
    save(art, f"{OUT}/jukung.webp", max_w=220, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 520, 60
    full = sasirangan(W, H, 60500, vertical=False, ncols=2, amp=4, period=90, scale=0.6)
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    shape = np.clip((1 - np.abs(xx) ** 3) * 1.4 - np.abs(yy) * (0.4 + 0.6 * np.abs(xx)), 0, 1)
    m = displace(np.clip(shape * 2.2, 0, 1), 4, 4, 14)
    full[..., 3] = gaussian_filter(m, 1.5)
    preview(full, "bs-divider", CREAM)
    save(full, f"{OUT}/divider.webp", max_w=300, quality=82)
