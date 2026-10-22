"""Girih Emas — Persian girih strapwork (decagon + bowtie tiling, Hankin lines at 54 deg) pressed as worn gold foil
on deep midnight blue painted ground; a girih rosette medallion, a four-centred iwan arch frame, a frieze band.
No figures, no calligraphy. Run: python3 -I girih-emas.py [part ...]
parts: panel frieze rosette iwan divider bintang"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g4_lib import *
from _jw_lib import along

OUT = outdir("girih-emas")
PARTS = sys.argv[1:] or ["panel", "frieze", "rosette", "iwan", "divider", "bintang"]
NIGHT = "#0b1633"
NIGHT_D = "#060d22"
LAPIS = "#16285a"
GOLD = "#caa553"
IVORY = "#efe3c4"
PERIOD_EDGE = 1 / GV1[0]  # px-per-edge so that one horizontal lattice period == given px


def strap_masks(W, H, S, ox, oy, lw, gap):
    """Interlaced-looking strapwork: a band of width lw with a dark core line (gap) down the middle."""
    tiles, segs = girih_field(0, 0, W, H, S, ox, oy)
    items = [([a, b], lw, None) for a, b in segs]
    band = strokes(W, H, items, cap=True)
    core = strokes(W, H, [([a, b], gap, None) for a, b in segs], cap=True) if gap else np.zeros((H, W), np.float32)
    return tiles, segs, band, core


def stars_fill(W, H, tiles, S, kind="dec", shrink=0.93):
    """Filled 10-point star centres of decagons (lapis inlay)."""
    polys = []
    for k, poly in tiles:
        if k != kind:
            continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        pts = []
        for i in range(20):
            a = math.radians(i * 18)
            r = (S * GA * shrink) if i % 2 == 0 else (S * 1.1180 * shrink)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        polys.append(pts)
    return shapes(W, H, polys, smooth=False)


def ground(W, H, seed):
    sky = painted_sky(W, H, [(0, "#0d1a3c"), (0.5, NIGHT), (1, NIGHT_D)], seed=seed, streak=0.5, grain=0.7)
    mot = fbm(W, H, seed + 3, 120, 3)[..., None]
    sky[..., :3] *= 0.9 + 0.2 * mot
    return sky


def gild(art, band, core, seed, W, H, wear=0.18):
    """Gold foil strap with worn spots + a fine dark incised core line."""
    worn = fbm(W, H, seed + 5, 9, 2)
    b = band * (1 - wear * np.clip((worn - 0.6) * 5, 0, 1))
    art = FO(art, b, GOLD, seed=seed, emboss=0.7, sparkle=0.12, pad=8)
    if core is not None and core.max() > 0:
        art = OV(art, core, lambda m: tint(m, "#5b4318", 0.75), pad=4)
    return art


def htile(W, H, period_px):
    """Width W must be an integer multiple of period_px so the image tiles horizontally."""
    return period_px / GV1[0]


if "panel" in PARTS:
    # tall horizontally-seamless panel (repeat-x): 2 lattice periods wide
    P = 230
    S = htile(0, 0, P)
    W, H = P * 2, 1760
    nx = Seq(1100)
    art = ground(W, H, nx())
    # render the strap wider than the tile then crop, so the seam is identical
    PAD = P
    WW = W + PAD * 2
    tiles, segs, band, core = strap_masks(WW, H, S, PAD + P * 0.5, 60, 9, 3.4)
    inlay = stars_fill(WW, H, tiles, S)
    sl = slice(PAD, PAD + W)
    band, core, inlay = band[:, sl], core[:, sl], inlay[:, sl]
    art = G(art, inlay, LAPIS, "#1f3a78", seed=nx(), density=0.75, edge=0.4, bloom=0.3, gran=0.5, rough=1.5, feather=0.8)
    clear()
    art = gild(art, band, core, nx(), W, H)
    clear()
    save_rgb(art, f"{OUT}/panel.webp", quality=74)
    preview(art[:900], "ge-panel", bg=NIGHT)

if "frieze" in PARTS:
    P = 160
    S = htile(0, 0, P)
    W, H = P * 3, 200
    nx = Seq(2100)
    art = ground(W, H, nx())
    PAD = P
    WW = W + PAD * 2
    tiles, segs, band, core = strap_masks(WW, H, S, PAD, 40, 7, 2.6)
    inlay = stars_fill(WW, H, tiles, S)
    sl = slice(PAD, PAD + W)
    band, core, inlay = band[:, sl], core[:, sl], inlay[:, sl]
    art = G(art, inlay, LAPIS, "#1f3a78", seed=nx(), density=0.75, edge=0.4, bloom=0.3, gran=0.5, rough=1.2, feather=0.6)
    art = gild(art, band, core, nx(), W, H, wear=0.1)
    # gold rules top and bottom
    rules = np.zeros((H, W), np.float32); rules[2:8] = 1; rules[H - 8:H - 2] = 1
    art = FO(art, rules, GOLD, seed=nx(), emboss=0.5, pad=2)
    save_rgb(art, f"{OUT}/frieze.webp", quality=78)
    preview(art, "ge-frieze", bg=NIGHT)

if "rosette" in PARTS:
    # circular medallion cut from the field, centred on a decagon, with a double gold ring
    W = H = 760
    cx = cy = 380
    S = 64
    nx = Seq(3100)
    disc = circles(W, H, [(cx, cy, 330)])
    tiles, segs, band, core = strap_masks(W, H, S, cx, cy, 10, 3.6)
    inlay = stars_fill(W, H, tiles, S)
    art = blank(W, H)
    base = gouache_paint(disc, "#0e1c43", "#0a1534", seed=nx(), rough=0.8, streak=0.4)
    art = over(art, base)
    art = G(art, inlay * disc, LAPIS, "#21408a", seed=nx(), density=0.8, edge=0.5, bloom=0.3, gran=0.5, rough=1.5)
    # central star: ivory wash
    cpts = []
    for i in range(20):
        a = math.radians(i * 18)
        r = S * GA * 0.86 if i % 2 == 0 else S * 1.118 * 0.86 * 0.82
        cpts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    cstar = shapes(W, H, [cpts], smooth=False)
    art = OV(art, cstar, lambda m: gouache_paint(m, IVORY, "#dccb9f", seed=77, rough=0.8, streak=0.5))
    art = FO(art, np.clip(gaussian_filter(cstar, 1.2) - gaussian_filter(shapes(W, H, [[(cx + (x - cx) * 0.8, cy + (y - cy) * 0.8) for x, y in cpts]], smooth=False), 1.2), 0, 1) * 1.6, GOLD, seed=78, emboss=0.6)
    clear()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip((330 - np.hypot(xx - cx, yy - cy)) / 14, 0, 1)
    art = gild(art, band * fade, core * fade, nx(), W, H, wear=0.12)
    rings = np.clip(circles(W, H, [(cx, cy, 346)]) - circles(W, H, [(cx, cy, 332)]), 0, 1)
    rings = np.maximum(rings, np.clip(circles(W, H, [(cx, cy, 362)]) - circles(W, H, [(cx, cy, 356)]), 0, 1))
    beads = circles(W, H, [(cx + math.cos(a) * 351, cy + math.sin(a) * 351, 2.6) for a in np.linspace(0, math.tau, 80, endpoint=False)])
    art = FO(art, np.maximum(rings, beads * 0), GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    art = FO(art, beads, "#e2c27a", seed=nx(), emboss=0.8, sparkle=0.1)
    preview(art, "ge-rosette", bg=NIGHT)
    save(art, f"{OUT}/rosette.webp", max_w=440, quality=82)

if "iwan" in PARTS:
    # four-centred (Persian) pointed arch frame: gold double line, girih-filled spandrels, open centre
    W, H = 640, 820
    nx = Seq(4100)
    ox, oy = 50, 50  # outer frame rect
    def arch(inset, spring=330, top=60):
        L, Rr = ox + inset, W - ox - inset
        cxm = W / 2; half = (Rr - L) / 2
        y_s = spring
        apex = (cxm, top + inset * 0.9)
        # four-centred approximation: a quarter-ish circle from the springing, then a straighter run to the apex
        pts = [(L, H - oy - inset)]
        pts += [(L, y_s)]
        r1 = half * 0.62
        c1 = (L + r1, y_s)
        for a in np.linspace(math.pi, math.pi * 1.32, 14):
            pts.append((c1[0] + math.cos(a) * r1, c1[1] + math.sin(a) * r1))
        sx, sy = pts[-1]
        for t in np.linspace(0, 1, 10)[1:]:
            q = (sx + (apex[0] - sx) * t, sy + (apex[1] - sy) * t - math.sin(t * math.pi) * half * 0.07)
            pts.append(q)
        right = [(W - x, y) for x, y in reversed(pts[:-1])]
        return pts + right
    outer_rect = shapes(W, H, [[(ox, oy), (W - ox, oy), (W - ox, H - oy), (ox, H - oy)]], smooth=False)
    a0 = shapes(W, H, [arch(0)], smooth=False)
    a1 = shapes(W, H, [arch(16)], smooth=False)
    a2 = shapes(W, H, [arch(24)], smooth=False)
    spandrel = np.clip(outer_rect - a0, 0, 1)
    # spandrel ground + girih
    art = blank(W, H)
    art = over(art, gouache_paint(spandrel, "#0e1c43", "#0a1534", seed=nx(), rough=0.6, streak=0.3))
    tiles, segs, band, core = strap_masks(W, H, 30, W / 2, 40, 3.2, 0.0)
    inlay = stars_fill(W, H, tiles, 30)
    art = G(art, inlay * spandrel, LAPIS, "#21408a", seed=nx(), density=0.75, edge=0.4, bloom=0.2, gran=0.4, rough=1)
    art = gild(art, band * gaussian_filter(spandrel, 0.6), None, nx(), W, H, wear=0.15)
    clear()
    # gold mouldings: outer rect line, arch double line
    ring1 = np.clip(a0 - a1, 0, 1) * 0 + np.clip(gaussian_filter(a0, 0.6) - gaussian_filter(shapes(W, H, [arch(6)], smooth=False), 0.6), 0, 1)
    ring2 = np.clip(a1 - a2, 0, 1)
    frame = np.clip(outer_rect - shapes(W, H, [[(ox + 7, oy + 7), (W - ox - 7, oy + 7), (W - ox - 7, H - oy - 7), (ox + 7, H - oy - 7)]], smooth=False), 0, 1)
    art = FO(art, np.maximum.reduce([ring1, ring2, frame]), GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    # lapis band between the arch lines
    art = over(art, gouache_paint(np.clip(a0 - a1, 0, 1) * np.clip(1 - ring1 * 3, 0, 1), "#17306a", "#122658", seed=nx(), rough=0.4, streak=0.3))
    art = FO(art, circles(W, H, [(x, y, 2.4) for x, y, *_ in along(arch(10.5), 18)]) * np.clip(a0 - a1, 0, 1), "#e6c77e", seed=nx(), emboss=0.6)
    preview(art, "ge-iwan", bg="#2a3556")
    save_full(art, f"{OUT}/iwan.webp", size=(W // 2, H // 2), quality=84)
    # also export the inner opening path (for the CSS clip-path of the photo), in the 320x410 output space
    inner = arch(24)
    with open(f"{PREV}/iwan-path.txt", "w") as f:
        f.write("M " + " L ".join(f"{x / 2:.1f} {y / 2:.1f}" for x, y in inner) + " Z")

if "divider" in PARTS:
    W, H = 640, 110
    nx = Seq(5100)
    art = blank(W, H)
    cx, cy = W / 2, H / 2
    pts = []
    for i in range(20):
        a = math.radians(i * 18 - 90)
        r = 40 if i % 2 == 0 else 24
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    star = shapes(W, H, [pts], smooth=False)
    inner = shapes(W, H, [[(cx + (x - cx) * 0.62, cy + (y - cy) * 0.62) for x, y in pts]], smooth=False)
    star_line = np.clip(star - inner, 0, 1)
    lines = strokes(W, H, [([(40, cy), (cx - 50, cy)], 3, (0.3, 0.0)), ([(cx + 50, cy), (W - 40, cy)], 3, (0.0, 0.3)),
                           ([(110, cy - 9), (cx - 60, cy - 9)], 1.4, (0.5, 0.05)), ([(cx + 60, cy - 9), (W - 110, cy - 9)], 1.4, (0.05, 0.5)),
                           ([(110, cy + 9), (cx - 60, cy + 9)], 1.4, (0.5, 0.05)), ([(cx + 60, cy + 9), (W - 110, cy + 9)], 1.4, (0.05, 0.5))])
    dots = circles(W, H, [(cx - 66, cy, 4), (cx + 66, cy, 4), (cx - 80, cy, 2.5), (cx + 80, cy, 2.5)])
    art = over(art, gouache_paint(inner, "#17306a", seed=nx(), rough=0.4))
    art = FO(art, np.maximum.reduce([star_line, lines, dots]), GOLD, seed=nx(), emboss=0.7, sparkle=0.15)
    preview(art, "ge-divider", bg=NIGHT)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)

if "bintang" in PARTS:
    W = H = 140
    nx = Seq(6100)
    cx = cy = 70
    pts = []
    for i in range(20):
        a = math.radians(i * 18 - 90)
        r = 60 if i % 2 == 0 else 37
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    star = shapes(W, H, [pts], smooth=False)
    inner = shapes(W, H, [[(cx + (x - cx) * 0.66, cy + (y - cy) * 0.66) for x, y in pts]], smooth=False)
    art = blank(W, H)
    art = over(art, gouache_paint(inner, "#17306a", "#21408a", seed=nx(), rough=0.4))
    art = FO(art, np.clip(star - inner, 0, 1), GOLD, seed=nx(), emboss=0.8)
    art = FO(art, circles(W, H, [(cx, cy, 9)]), "#e2c27a", seed=nx(), emboss=0.8)
    preview(art, "ge-bintang", bg=NIGHT)
    save(art, f"{OUT}/bintang.webp", max_w=64, quality=86)
