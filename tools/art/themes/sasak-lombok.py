"""Sasak Lombok — black songket with gold subahnale weft, lumbung padi with its ilalang hood roof, and the Lombok coast
(Rinjani, sea, green hills) in watercolour. Earthy black-gold-red. No figures.
Run: python3 -I sasak-lombok.py [part ...]  parts: songket coast lumbung divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b2_lib import *

OUT = outdir("sasak-lombok")
PARTS = sys.argv[1:] or ["songket", "coast", "lumbung", "divider"]
BLK, BLK2 = "#16100c", "#22170f"
RED, RED_D = "#9a2620", "#6a1712"
GOLD = "#c99a3a"
GRN = "#2f5a3a"
THATCH, THATCH_D, THATCH_L = "#9c7a45", "#5c4322", "#c9a96a"
WOOD, WOOD_D = "#5a3a22", "#2e1c10"


def subahnale(W, H, ox, oy, cw, ch):
    """Subahnale lattice for a period (cw x ch): hexagon cells (gold outline) holding an 8-petal flower; small
    diamonds where cells meet. Returns (gold_lines, gold_flowers, red_hearts, red_diamonds) masks; repeated with
    wrap copies so the tile is seamless."""
    hexes, flowers, hearts, dia = [], [], [], []
    for gx in range(-1, W // cw + 2):
        for gy in range(-1, H // ch + 2):
            for (dx, dy) in ((0, 0), (cw / 2, ch / 2)):
                cx, cy = ox + gx * cw + dx, oy + gy * ch + dy
                r = ch * 0.46
                hx = [(cx + math.cos(k * math.pi / 3) * r * 1.08, cy + math.sin(k * math.pi / 3) * r) for k in range(6)]
                hexes.append(hx + [hx[0]])
                for k in range(8):
                    flowers.append(petal_pts(cx, cy, r * 0.56, r * 0.2, k * math.pi / 4, n=10))
                hearts.append((cx, cy, r * 0.12))
                ex, ey = cx + r * 1.08 * 1.0, cy
                dia.append([(ex, ey - r * 0.16), (ex + r * 0.12, ey), (ex, ey + r * 0.16), (ex - r * 0.12, ey)])
    lines = polyline_mask(W, H, hexes, max(1.6, ch * 0.035), cap=False)
    return lines, shapes(W, H, flowers), circles(W, H, hearts), shapes(W, H, dia, smooth=False)


if "songket" in PARTS:
    # seamless tile 256x224: black cloth, gold subahnale weft, red silk hearts, a thin red stripe row
    W, H = 256, 224
    nx = Seq(71100)
    art = cloth_base(W, H, BLK, seed=nx(), cell=2.0, var=0.1)
    lines, fl, hearts, dia = subahnale(W, H, 0, 0, 128, 112)
    art = over(art, songket_weft(np.maximum(lines, fl * 0.95), GOLD, seed=nx(), pitch=2.2, float_len=6))
    art = over(art, silk_weft(np.maximum(hearts, dia), RED, seed=nx()))
    art[..., 3] = 1
    preview(art, "sl-songket", bg=BLK)
    save_rgb(art, f"{OUT}/songket.webp", quality=80)
    clear()

if "divider" in PARTS:
    W, H = 600, 70
    nx = Seq(71200); cy = 35
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 3, 0, 1)[None, :]
    lines = polyline_mask(W, H, [[(30, cy), (250, cy)], [(350, cy), (570, cy)]], 2.2, cap=False) * fade
    tri = [[(x, cy - 3), (x + 9, cy - 12), (x + 18, cy - 3)] for x in range(40, 240, 18)] + [[(x, cy - 3), (x + 9, cy - 12), (x + 18, cy - 3)] for x in range(352, 560, 18)]
    trb = [[(x + 9, cy + 3), (x + 18, cy + 12), (x + 27, cy + 3)] for x in range(31, 231, 18)] + [[(x + 9, cy + 3), (x + 18, cy + 12), (x + 27, cy + 3)] for x in range(343, 551, 18)]
    art = over(blank(W, H), songket_weft(np.maximum(lines, shapes(W, H, tri, smooth=False) * fade), GOLD, seed=nx(), pitch=2.0))
    art = over(art, silk_weft(shapes(W, H, trb, smooth=False) * fade, RED, seed=nx()))
    fl = shapes(W, H, [petal_pts(300, cy, 26, 10, k * math.pi / 4, n=10) for k in range(8)])
    art = over(art, songket_weft(fl, GOLD, seed=nx(), pitch=2.0))
    art = over(art, silk_weft(circles(W, H, [(300, cy, 6)]), RED, seed=nx()))
    preview(art, "sl-divider", bg="#efe4cc")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()


def lumbung(W, H, cx, base, s, nx, rng, art):
    """Sasak lumbung padi: stone footing, four posts with round jelepeng discs, open bale floor, then the tall ilalang
    hood roof (flared hem, swelling sides, rounded crown) with a small gable hatch."""
    post_top = base - 104 * s
    posts = polyline_mask(W, H, [[(cx + dx * s, base), (cx + dx * s * 0.96, post_top)] for dx in (-70, -26, 26, 70)], 11 * s, cap=False)
    posts = np.maximum(posts, polyline_mask(W, H, [[(cx - 80 * s, post_top + 30 * s), (cx + 80 * s, post_top + 30 * s)]], 6 * s, cap=False))
    stones = shapes(W, H, [deform(ellipse_pts(cx + dx * s, base + 2, 13 * s, 6 * s, 10), rng, 1, 0.1) for dx in (-70, -26, 26, 70)])
    discs = ellipses(W, H, [(cx + dx * s * 0.96, post_top + 4 * s, 19 * s, 6 * s, 0) for dx in (-70, -26, 26, 70)])
    floor = rect(W, H, cx - 92 * s, post_top - 6 * s, cx + 92 * s, post_top + 4 * s)
    hem_y = post_top - 18 * s
    # hood profile: flared skirt at the hem, slight waist, tall body, rounded crown
    prof = []
    for t in np.linspace(0, 1, 40):
        y = hem_y - t * 300 * s
        if t < 0.16:
            k = 0.74 + 0.30 * (1 - t / 0.16) ** 2
        else:
            k = 0.74 - 0.10 * (t - 0.16) / 0.5
        if t > 0.62:
            k *= math.sqrt(max(0.0, 1 - ((t - 0.62) / 0.38) ** 2)) * 0.97 + 0.03
        prof.append((k * 122 * s, y))
    left = [(cx - hx, y) for hx, y in prof]
    right = [(cx + hx, y) for hx, y in reversed(prof)]
    hem = [(cx + 127 * s * math.cos(a), hem_y + 12 * s * math.sin(a)) for a in np.linspace(0, math.pi, 16)]
    roof = shapes(W, H, [left + right + hem])
    # shadow under
    sh = shapes(W, H, [deform(ellipse_pts(cx + 14 * s, base + 4, 120 * s, 12 * s, 14), rng, 1, 0.05)])
    art = G(art, sh, "#2a2010", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=3, feather=4)
    art = GP(art, stones, "#7d7466", "#5b5348", seed=nx(), rough=0.8, pad=6)
    art = GP(art, posts, WOOD, WOOD_D, seed=nx(), rough=0.7, pad=6)
    art = GP(art, np.maximum(discs, floor), WOOD_D, "#4a2e1a", seed=nx(), rough=0.6, pad=6)
    # under-roof shade (bale)
    art = G(art, rect(W, H, cx - 100 * s, hem_y - 4 * s, cx + 100 * s, post_top - 6 * s), "#2b1d10", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=2)
    # thatch
    art = GP(art, roof, THATCH, THATCH_D, seed=nx(), rough=1.6, streak=1.4)
    tone = light_mask(H, W, cx - 60 * s, hem_y - 230 * s, 260 * s)
    art = over(art, flat(roof * tone, THATCH_L, 0.45))
    art = over(art, shade_lr(roof, W, "#3b2a14", 0.5, side=1, width=0.55))
    th = roof * hatch(W, H, 0.0, 3.0 * s + 1.4, 0.2, nx(), 2.2) * (0.4 + 0.6 * fbm(W, H, nx(), 10, 2))
    art = over(art, flat(th, "#4a3418", 0.55))
    hi = roof * hatch(W, H, 0.03, 4.6 * s + 2, 0.1, nx(), 3.0) * tone
    art = over(art, flat(hi, "#e2c98e", 0.5))
    binds = []
    for t in (0.17, 0.45):
        y = hem_y - t * 300 * s
        hx = np.interp(y, [p[1] for p in reversed(prof)], [p[0] for p in reversed(prof)])
        binds.append(curve([(cx - hx, y), (cx, y + 8 * s), (cx + hx, y)], 20))
    art = over(art, flat(polyline_mask(W, H, binds, 2.2 * s + 0.6) * roof, "#3a2812", 0.6))
    fringe = polyline_mask(W, H, [[(cx + 128 * s * math.cos(a), hem_y + 16 * s * math.sin(a)), (cx + 130 * s * math.cos(a), hem_y + (16 * s) * math.sin(a) + 8 * s + rng.uniform(0, 4) * s)] for a in np.linspace(0.05, math.pi - 0.05, 80)], 1.8 * s + 0.6)
    art = over(art, flat(fringe, THATCH_D, 0.8))
    # gable hatch (small wooden door high on the front)
    hy = hem_y - 222 * s
    hatch_m = poly(W, H, [(cx - 20 * s, hy + 26 * s), (cx, hy - 6 * s), (cx + 20 * s, hy + 26 * s)])
    art = GP(art, hatch_m, WOOD_D, seed=nx(), rough=0.5, pad=6)
    art = GP(art, outline(hatch_m, 2.5), GOLD, seed=nx(), rough=0.3, pad=6)
    # ridge tuft
    tuft = strokes(W, H, [([(cx, hem_y - 296 * s), (cx + rng.uniform(-6, 6) * s, hem_y - 314 * s)], 4 * s) for _ in range(5)])
    art = GP(art, tuft, THATCH_D, seed=nx(), rough=0.4, pad=6)
    return art, roof


if "coast" in PARTS:
    # Lombok coast: Rinjani far left, sea, green hills, beach; two lumbung on a grassy rise; palms. Sky transparent.
    W, H = 840, 560
    nx = Seq(71300); rng = random.Random(11)
    art = blank(W, H)
    _land = np.maximum.reduce([
        poly(W, H, [(-30, 340), (60, 250), (150, 176), (196, 152), (214, 162), (236, 150), (300, 196), (420, 280), (520, 330), (-30, 360)]),
        hills(W, H, 300, 30, 4, 0.7) * (np.linspace(0, 1, W)[None, :] > 0.35), rect(W, H, -20, 336, W + 20, H + 10)])
    art = over(art, flat(np.clip(gaussian_filter(_land, 1.2) * 1.4, 0, 1), "#efe4cc", 1.0))
    # Rinjani (distant, cool) — crater rim with a notch, lighter snowless top
    rin = poly(W, H, [(-30, 340), (60, 250), (150, 176), (196, 152), (214, 162), (236, 150), (300, 196), (420, 280), (520, 330), (-30, 360)])
    art = G(art, rin, "#8ea0b4", "#6f8199", seed=nx(), density=0.55, edge=0.35, bloom=0.45, rough=5, feather=2.4)
    art = G(art, rin * light_mask(H, W, 150, 170, 180), "#b7c3cf", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3)
    ridges = strokes(W, H, [(curve([(196 + dx, 160), (180 + dx * 2, 230), (150 + dx * 3, 320)], 16), 3, (0.1, 0.6)) for dx in (-10, 14, 34, 60)])
    art = G(art, ridges * rin, "#5f708a", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=2)
    # far hills right
    fh = hills(W, H, 300, 30, 4, 0.7) * (np.linspace(0, 1, W)[None, :] > 0.35)
    fh = np.maximum(fh * 1.0, 0) * (np.mgrid[0:H, 0:W][0] < 420)
    art = G(art, fh, "#7c9a86", "#5d806e", seed=nx(), density=0.6, edge=0.4, bloom=0.35, rough=6)
    # sea
    sea = rect(W, H, -20, 340, W + 20, 430)
    sea_l = G(blank(W, H), sea, "#3f8fa0", "#2c6f8a", seed=nx(), density=0.75, edge=0.25, bloom=0.3, rough=4)
    mh = shapes(W, H, [[(380, 470), (470, 390), (560, 350), (650, 330), (760, 340), (W + 20, 360), (W + 20, 480)]])
    sea_l = knockout(sea_l, np.maximum(np.maximum(rin, fh), mh), amount=1.0, grow=0.8)
    art = glaze(art, sea_l)
    wav = strokes(W, H, [([(x, y), (x + rng.uniform(20, 60), y + rng.uniform(-0.6, 0.6))], 1.6) for x, y in [(rng.uniform(0, W), rng.uniform(352, 420)) for _ in range(70)]])
    art = over(art, flat(wav * sea, "#d8efee", 0.55))
    # beach
    beach = shapes(W, H, [[(-20, 412), (200, 404), (420, 414), (620, 410), (W + 20, 406), (W + 20, 452), (-20, 452)]])
    art = glaze(art, knockout(G(blank(W, H), beach, "#e6cf9e", "#d4b47a", seed=nx(), density=0.8, edge=0.3, bloom=0.3, rough=4), mh, 1.0, 0.8))
    foam = strokes(W, H, [(curve([(-10, 412), (210, 405), (430, 415), (640, 411), (W + 10, 407)], 40), 2.4, None)])
    art = over(art, flat(foam, "#fbf6ea", 0.75))
    # mid green hill (right) + foreground rise
    art = G(art, mh, "#6a8d4c", "#4b7040", seed=nx(), density=0.85, edge=0.45, bloom=0.4, rough=6)
    fg = shapes(W, H, [[(-20, 470), (120, 440), (300, 452), (480, 470), (640, 462), (W + 20, 448), (W + 20, H + 10), (-20, H + 10)]])
    art = G(art, fg, "#5d7a3c", "#7a8a3e", seed=nx(), density=0.95, edge=0.4, bloom=0.3, rough=5)
    art = G(art, fg * (np.mgrid[0:H, 0:W][0] > 500), "#3c5228", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=4, feather=6)
    grass = strokes(W, H, [([(x, y), (x + rng.uniform(-4, 4), y - rng.uniform(8, 18))], 1.6, (0.0, 0.8)) for x, y in [(rng.uniform(0, W), rng.uniform(462, 555)) for _ in range(260)]])
    art = over(art, flat(grass * fg, "#2e4420", 0.55))
    # palms
    pm = np.maximum(palm_m(W, H, 740, 470, 250, -0.14, 3), palm_m(W, H, 800, 460, 190, -0.04, 7))
    pm = np.maximum(pm, palm_m(W, H, 470, 466, 150, 0.12, 9))
    art = G(art, pm, "#355a33", "#24401f", seed=nx(), density=0.92, edge=0.5, bloom=0.15, rough=2.5)
    # lumbung pair
    art, r1 = lumbung(W, H, 330, 500, 0.62, nx, rng, art)
    art, r2 = lumbung(W, H, 150, 528, 0.92, nx, rng, art)
    shr = shapes(W, H, [deform(ellipse_pts(x, y, rx, 20, 12), rng, 2, 0.14) for x, y, rx in [(30, 520, 60), (250, 532, 50), (560, 520, 70), (680, 540, 80)]])
    art = G(art, shr, "#5a7836", "#3d5a2a", seed=nx(), density=0.6, edge=0.5, bloom=0.35, rough=6)
    preview(art, "sl-coast", "#efe4cc")
    save(art, f"{OUT}/coast.webp", max_w=780, quality=78)
    clear()

if "lumbung" in PARTS:
    W, H = 420, 480
    nx = Seq(71400); rng = random.Random(5)
    art = blank(W, H)
    gr = shapes(W, H, [deform(ellipse_pts(210, 452, 190, 22, 16), rng, 2, 0.08)])
    art = G(art, gr, "#7a8a3e", "#5d7a3c", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=6)
    art, _ = lumbung(W, H, 210, 450, 1.0, nx, rng, art)
    preview(art, "sl-lumbung", "#efe4cc")
    save(art, f"{OUT}/lumbung.webp", max_w=300, quality=82)
    clear()
