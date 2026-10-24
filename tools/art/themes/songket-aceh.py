"""Songket Aceh — gold supplementary-weft songket on deep red and black, rendered at thread level (ground twill +
metallic floats with tie-downs and glint): pucuk rebung band, black 'badan' tile with bungong tabur, woven medallion,
woven divider strip, and a gouache Rumoh Aceh gable. Run: python3 -I songket-aceh.py [part ...]
parts: band badan medal divider rumoh. Assets -> public/themes/art/songket-aceh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s3_lib import *

OUT = outdir("songket-aceh")
PARTS = sys.argv[1:] or ["band", "badan", "medal", "divider", "rumoh"]
RED, RED_D, RED_L = "#7a1517", "#4f0c0f", "#9b2422"
BLACK = "#191112"
RED_RGB = np.array(hex_rgb(RED), np.float32)
BLK_RGB = np.array(hex_rgb(BLACK), np.float32)
SILVER = [(0, "#2a2a2c"), (0.4, "#6f6c68"), (0.7, "#bdb7aa"), (1.0, "#f7f2e6")]
PICK, END = 5, 4


def bmp(rows):
    """String bitmap -> int array ('#'=1 gold, 's'=2 silver, '.'=0)."""
    return np.array([[1 if ch == "#" else 2 if ch == "s" else 0 for ch in r] for r in rows], np.int32)


BUNGONG = bmp([
    "......#......",
    "....##.##....",
    "..#..#.#..#..",
    ".###.#.#.###.",
    "####..#..####",
    ".###.#.#.###.",
    "..#..#.#..#..",
    "....##.##....",
    "......#......",
])
GOLD_A = [(0, "#3a250a"), (0.35, "#835a1c"), (0.62, "#c4933a"), (0.84, "#e8c57a"), (1.0, "#fbe7b4")]

if "band" in PARTS:
    # pucuk rebung band (repeat-x). 120 x 40 cells -> 480 x 200 px
    C, R, P = 120, 40, 30
    m = np.zeros((R, C), np.int32)
    gr = np.zeros((R, C, 3), np.float32) + RED_RGB
    for rr in (0, 1, 38, 39):
        m[rr, :] = 1
    m[7, :] = 1
    for j in range(C):  # small diamond chain rows 3-5
        u = (j % 6) - 3
        if abs(u) <= 0: m[3, j] = m[5, j] = 1
        if abs(u) == 1: m[4, j] = 0
        if abs(u) == 2: m[4, j] = 1
    for i in range(9, 37):
        v = 36 - i
        for j in range(C):
            u = (j % P) - (P - 1) / 2
            hw = 14.6 * (1 - v / 28.5)
            ins = abs(u) <= hw
            if ins:
                gr[i, j] = BLK_RGB
            outl = ins and abs(u) > hw - 2.2
            inner_hw = 9.4 * (1 - v / 19.5)
            inner = 0 <= v <= 19 and abs(abs(u) - inner_hw) < 1.1
            spine = abs(u) < 0.6 and v % 3 != 2 and v < 24
            dia = v in range(2, 17) and abs(u) <= 3 and (abs(u) + abs((v % 5) - 2)) == 2
            if outl or inner or spine or (dia and not spine):
                m[i, j] = 1
            # small hook (kait) motif in the red between triangles
            if not ins and v < 9 and (abs(abs(u) - 14.5) + abs(v - 4)) in (2, 2.5):
                m[i, j] = 1
    cloth = weave(m, gr, PICK, END, maxfloat=8, seed=301, metal=[GOLD_A], glint=0.6)
    preview(cloth, "sa-band", bg=BLACK)
    save_full(cloth, f"{OUT}/band.webp", quality=72)

if "badan" in PARTS:
    # black body tile with red stripes and bungong tabur on a half-drop lattice. 120 x 96 cells -> 480 x 480
    C, R = 120, 96
    m = np.zeros((R, C), np.int32)
    gr = np.zeros((R, C, 3), np.float32) + BLK_RGB
    for j in range(C):
        if j % 30 in (0, 1):
            gr[:, j] = RED_RGB * 0.9
    bh, bw = BUNGONG.shape
    for k, (ci, cj) in enumerate([(i, j) for i in range(0, R, 24) for j in range(0, C, 30)]):
        oi = ci + (12 if (cj // 30) % 2 else 0)
        for a in range(bh):
            for b in range(bw):
                if BUNGONG[a, b]:
                    m[(oi + 7 + a) % R, (cj + 9 + b) % C] = 1
    # tiny silver-gold dots between
    for i in range(0, R, 12):
        for j in range(0, C, 15):
            if (i // 12 + j // 15) % 2 == 0 and j % 30 == 0:
                continue
    cloth = weave(m, gr, PICK, END, maxfloat=6, seed=311, glint=0.6, metal=[GOLD_A])
    preview(cloth, "sa-badan", bg=BLACK)
    save_full(cloth, f"{OUT}/badan.webp", quality=70)

if "medal" in PARTS:
    # woven diamond medallion: eight-point star + rosette on red, black field, gold border; diamond-cut (stepped edge)
    C, R = 84, 68
    m = np.zeros((R, C), np.int32)
    gr = np.zeros((R, C, 3), np.float32) + RED_RGB
    cx, cy = (C - 1) / 2, (R - 1) / 2
    sx, sy = 1.0, PICK / END  # make it visually square: a row is taller than a column is wide
    alpha = np.zeros((R, C), np.float32)
    for i in range(R):
        for j in range(C):
            x = (j - cx) * END; y = (i - cy) * PICK  # px offsets
            d = abs(x) / 166 + abs(y) / 166  # diamond metric
            if d <= 1.0:
                alpha[i, j] = 1
            if 0.9 < d <= 1.0 or 0.82 < d <= 0.85:
                m[i, j] = 1
            if d <= 0.8:
                gr[i, j] = BLK_RGB
            # eight point star: union of square and diamond outlines
            sq = max(abs(x), abs(y)); dm = (abs(x) + abs(y)) / 1.414
            star = max(min(sq, dm * 1.0), 0)
            if 62 <= max(sq, 0) <= 70 and dm <= 92: m[i, j] = 1
            if 62 <= dm <= 70 and sq <= 92: m[i, j] = 1
            rr = math.hypot(x, y)
            if 30 <= rr <= 36: m[i, j] = 1
            if rr <= 12: m[i, j] = 1
            ang = math.atan2(y, x)
            if 14 < rr < 30 and abs(math.sin(ang * 4)) > 0.86: m[i, j] = 1
            if 0.82 < d <= 0.9 and ((i + j) % 4 == 0): m[i, j] = 2
            # small rebung shoots pointing into the corners between star and border
            if 96 < sq < 120 and dm < 112 and abs(abs(x) - abs(y)) < 10: m[i, j] = 1
    cloth = weave(m, gr, PICK, END, maxfloat=6, seed=321, metal=[GOLD_RAMP, SILVER], wrap=False)
    a = np.repeat(np.repeat(alpha, PICK, 0), END, 1)
    cloth[..., 3] = gaussian_filter(a, 0.5)
    sh = soft_shadow(a, "#000000", blur=6, strength=0.45, dx=0, dy=5)
    art = over(sh, cloth)
    preview(art, "sa-medal", bg="#2a1414")
    save(art, f"{OUT}/medal.webp", max_w=340, quality=80)

if "divider" in PARTS:
    # narrow woven strip: zigzag (tumpal) + diamonds, frayed ends
    C, R = 90, 9
    m = np.zeros((R, C), np.int32)
    gr = np.zeros((R, C, 3), np.float32) + RED_RGB
    m[0, :] = 1; m[8, :] = 1
    for j in range(C):
        ph = j % 8
        zz = 1 + (ph if ph <= 4 else 8 - ph) * 1.5
        m[int(round(zz)), j] = 1
        if (j % 16) == 8:
            for a in range(1, 8):
                m[a, j] = 1 if a in (3, 4, 5) else m[a, j]
        if j < 4 or j > C - 5:
            gr[:, j] = BLK_RGB
    for i in range(1, 8):
        gr[i, :] *= 0.95
    cloth = weave(m, gr, 4, 4, maxfloat=6, seed=331, wrap=False)
    H, W = cloth.shape[:2]
    # frayed taper ends
    xx = np.arange(W)[None, :].astype(np.float32)
    fade = np.clip(np.minimum(xx, W - 1 - xx) / 14, 0, 1)
    fr = np.random.default_rng(3).random((H, W)) * 0.6 + 0.4
    cloth[..., 3] = np.clip(fade * 1.2 - (1 - fade) * fr, 0, 1)
    preview(cloth, "sa-divider", bg=BLACK)
    save(cloth, f"{OUT}/divider.webp", max_w=360, quality=82)

if "rumoh" in PARTS:
    # Rumoh Aceh gable end (tulak angen) on stilts: steep thatch roof, carved lattice gable, carved wall band, stair
    W, H = 760, 560
    nx = Seq(30500)
    rng = random.Random(5)
    art = blank(W, H)
    ground = shapes(W, H, [deform(ellipse_pts(380, 528, 330, 16), rng, 1, 0.04)])
    art = G(art, ground, "#000000", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=4, feather=6)
    # stilts (tameh)
    st = strokes(W, H, [([(x, 362), (x + rng.uniform(-2, 2), 522)], 15, None) for x in (176, 266, 380, 494, 584)])
    art = GP(art, st, "#3a2316", "#24150c", seed=nx(), rough=1.0, streak=1.0)
    beam = shapes(W, H, [[(140, 446), (620, 446), (620, 458), (140, 458)]], smooth=False)
    art = GP(art, beam, "#4a2c18", seed=nx(), rough=0.8)
    # stair
    stair = strokes(W, H, [([(330, 372), (300, 524)], 7, None), ([(430, 372), (460, 524)], 7, None)] + [([(330 - k * 6, 392 + k * 26), (430 + k * 6, 392 + k * 26)], 5, None) for k in range(5)])
    art = GP(art, stair, "#5a351b", "#3a2212", seed=nx(), rough=0.8)
    # body (wall) with carved band
    wall = shapes(W, H, [[(132, 262), (628, 262), (628, 366), (132, 366)]], smooth=False)
    art = GP(art, wall, "#5c3620", "#3c2214", seed=nx(), rough=1.2, streak=1.2)
    planks = strokes(W, H, [([(x, 300), (x, 364)], 1.6, None) for x in range(150, 620, 22)])
    art = G(art, planks, "#24140b", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    band = shapes(W, H, [[(132, 268), (628, 268), (628, 298), (132, 298)]], smooth=False)
    art = GP(art, band, RED_D, "#3a0a0c", seed=nx(), rough=0.8)
    items = []
    for x in range(140, 624, 24):  # carved triangles + circles band
        items.append(([(x, 296), (x + 12, 272), (x + 24, 296)], 2.4, None))
    carv = np.maximum(strokes(W, H, items), circles(W, H, [(x + 12, 289, 3) for x in range(140, 610, 24)]))
    art = FO(art, carv, "#c7973e", seed=nx(), emboss=0.6, sparkle=0.1)
    win = shapes(W, H, [[(x, 312), (x + 40, 312), (x + 40, 352), (x, 352)] for x in (190, 530)], smooth=False)
    art = GP(art, win, "#1a0e08", seed=nx(), rough=0.6)
    wl = strokes(W, H, [([(x + 20, 312), (x + 20, 352)], 2, None) for x in (190, 530)] + [([(x, 332), (x + 40, 332)], 2, None) for x in (190, 530)])
    art = FO(art, wl, "#b98a38", seed=nx(), emboss=0.5)
    # roof: steep thick thatch (rumbia) with wide eaves; gable triangle in front
    thatch = shapes(W, H, [[(40, 284), (380, 16), (720, 284), (700, 300), (380, 60), (60, 300)]], smooth=False)
    art = GP(art, thatch, "#7a5f3a", "#4a3720", seed=nx(), rough=3.2, streak=1.6)
    rows = []
    for t in np.linspace(0.08, 1.0, 9):  # shingle courses
        for side in (-1, 1):
            x0, y0 = 380 + side * 340 * t, 16 + 268 * t
            for k in range(14):
                u = k / 13
                bx = 380 + side * (340 * t - 30 * u); by = y0 + 12 * u
                rows.append(([(bx, by - 5), (bx + side * rng.uniform(-3, 3), by + 14)], 2.2, None))
    shingle = strokes(W, H, rows) * thatch
    art = G(art, shingle, "#2c1f10", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    eave = strokes(W, H, [([(48, 290), (380, 24)], 6, None), ([(712, 290), (380, 24)], 6, None)])
    art = G(art, eave, "#c9a46a", seed=nx(), density=0.45, edge=0.3, bloom=0.2, rough=1.5)
    under = shapes(W, H, [[(60, 300), (380, 60), (700, 300), (640, 300), (380, 92), (120, 300)]], smooth=False)
    art = G(art, under, "#1a0f08", seed=nx(), density=0.6, edge=0.3, bloom=0.1, rough=2)
    gable = shapes(W, H, [[(150, 266), (380, 76), (610, 266)]], smooth=False)
    art = GP(art, gable, "#6a4024", "#3e2414", seed=nx(), rough=1.2, streak=1.4)
    # openwork carving: courses of pierced triangles and diamonds (dark), ochre-gold painted ridges
    holes, ridges = [], []
    for row in range(7):
        y = 252 - row * 24
        half = (y - 76) / (266 - 76) * 230 - 14
        if half < 24:
            continue
        ridges.append(([(380 - half - 6, y + 6), (380 + half + 6, y + 6)], 3.0, None))
        n = int(half // 20)
        for k in range(-n, n + 1):
            x = 380 + k * 20
            if row % 2 == 0:
                holes.append([(x - 7, y), (x, y - 14), (x + 7, y)])
            else:
                holes.append([(x, y - 15), (x + 6, y - 7), (x, y + 1), (x - 6, y - 7)])
    hm = shapes(W, H, holes, smooth=False)
    art = GP(art, hm, "#140a05", seed=nx(), rough=0.9)
    art = GP(art, strokes(W, H, ridges), "#b8893c", "#8a6226", seed=nx(), rough=0.9, streak=1.0)
    frame = strokes(W, H, [([(150, 266), (380, 76), (610, 266)], 7, None)])
    art = GP(art, frame, "#c0913f", "#8f6526", seed=nx(), rough=1.0)
    sun = circles(W, H, [(380, 128, 13)])
    art = GP(art, sun, "#c99a45", seed=nx(), rough=0.8)
    art = GP(art, circles(W, H, [(380, 128, 6)]), RED, seed=nx(), rough=0.5)
    preview(art, "sa-rumoh", bg=RED_D)
    save(art, f"{OUT}/rumoh.webp", max_w=520, quality=78)
