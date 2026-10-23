"""Fanous Mesir — lentera fanous Kairo: badan kuningan/tembaga berlubang dengan kaca warna (merah delima, zamrud, kobalt,
kuning) yang menyala, tergantung dari balkon mashrabiya kayu berkisi yang diterangi cahaya hangat dari dalam.
Tanpa figur, tanpa kaligrafi. Run: python3 -I fanous-mesir.py [part ...]
parts: fanous fanous2 balkon kisi divider bintang     Assets -> public/themes/art/fanous-mesir/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m5_lib import *

OUT = outdir("fanous-mesir")
PARTS = sys.argv[1:] or ["fanous", "fanous2", "balkon", "kisi", "divider", "bintang"]
BRASS, COPPER, PATINA = "#b88a46", "#b86f3c", "#2a160c"
WOOD, WOOD_D, WOOD_L = "#3d2417", "#22130b", "#6e4429"
LIGHT, LIGHT_D = "#ffd58a", "#f0893a"
RUBY, EMER, COBALT, AMBER, TURQ = "#d6283f", "#17a06c", "#2f5fdc", "#f3a71f", "#1db4b6"
NIGHT = "#141c2e"


def lit_glass(mask, col, cx, cy, rad, seed):
    """Coloured glass lit from inside: hot pale core fading to saturated rim, slight streaky glass texture."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.clip(np.hypot((xx - cx) / rad, (yy - cy) / (rad * 1.6)), 0, 1)
    core = np.array(hex_rgb("#fff1c4"), np.float32); c = np.array(hex_rgb(col), np.float32)
    deep = c * 0.55
    t = d[..., None]
    rgb = core * (1 - t) ** 2 + c * (2 * t * (1 - t)) + deep * t ** 2
    st = noise(w, h, seed, (6.0, 0.8))
    rgb = rgb * (0.92 + 0.16 * st[..., None])
    a = np.clip(gaussian_filter(mask, 0.6), 0, 1) * 0.97
    return rgba(np.clip(rgb, 0, 1), a)


def brass(dst, mask, base=BRASS, seed=1, line=True):
    out = FO(dst, mask, base, seed=seed, emboss=0.8, sparkle=0.15)
    if line:
        out = K(out, outline_of(mask, 1.3), PATINA, seed=seed + 3, alpha=0.85)
    return out


def pierce(W, H, x0, y0, x1, y1, step, kind="star"):
    """Pierced pattern (holes) inside a box: small 4-point stars / dots on a lattice."""
    items = []
    y = y0 + step / 2; row = 0
    while y < y1:
        x = x0 + step / 2 + (step / 2 if row % 2 else 0)
        while x < x1:
            items.append((x, y))
            x += step
        y += step * 0.8; row += 1
    if kind == "dot":
        return circles(W, H, [(x, y, step * 0.18) for x, y in items])
    polys = [star_poly(x, y, step * 0.32, step * 0.12, 4, math.pi / 4) for x, y in items]
    return shapes(W, H, polys, smooth=False)


def star_poly(cx, cy, ro, ri, n=8, rot=0.0):
    pts = []
    for k in range(n * 2):
        r_ = ro if k % 2 == 0 else ri
        a = rot + k * math.pi / n
        pts.append((cx + math.cos(a) * r_, cy + math.sin(a) * r_))
    return pts


def chain(W, H, x, y0, y1, link=14):
    items = []; y = y0; k = 0
    while y < y1:
        items.append(ellipse_pts(x, y + link / 2, (link * 0.28) if k % 2 else link * 0.42, link * 0.55, 12))
        y += link * 0.8; k += 1
    return lines(W, H, items, 2.6)


def fanous(W, H, cx, top, s, glass, seed, chain_len=120, glow_amt=1.0):
    """Classic Cairo fanous, front view of a hexagonal body (3 faces visible)."""
    rng = random.Random(seed)
    nx = Seq(seed)
    art = blank(W, H)
    y = top
    # chain + hanging ring
    ch = chain(W, H, cx, y, y + chain_len)
    y += chain_len
    ringm = ring(W, H, cx, y + 10 * s, 10 * s, 3.2 * s)
    y += 20 * s
    knob = shapes(W, H, [ellipse_pts(cx, y + 10 * s, 9 * s, 11 * s, 16), [(cx - 4 * s, y + 18 * s), (cx + 4 * s, y + 18 * s), (cx + 6 * s, y + 34 * s), (cx - 6 * s, y + 34 * s)]])
    y += 32 * s
    # dome cap with pierced dots
    dome_pts = [(cx + math.cos(a) * 62 * s, y + 70 * s - math.sin(a) * 70 * s) for a in np.linspace(0, math.pi, 40)]
    dome = shape_mask(W, H, dome_pts + [(cx - 62 * s, y + 70 * s), (cx + 62 * s, y + 70 * s)], smooth=False)
    dome_holes = pierce(W, H, cx - 56 * s, y + 18 * s, cx + 56 * s, y + 66 * s, 14 * s, "dot") * dome
    y_dome = y
    y += 70 * s
    # crown band (pierced) + cresting
    band = shapes(W, H, [[(cx - 92 * s, y), (cx + 92 * s, y), (cx + 98 * s, y + 26 * s), (cx - 98 * s, y + 26 * s)]], smooth=False)
    crest = shapes(W, H, [[(cx + k * 30 * s - 9 * s, y + 2), (cx + k * 30 * s, y - 16 * s), (cx + k * 30 * s + 9 * s, y + 2)] for k in range(-3, 4)], smooth=False)
    band_holes = pierce(W, H, cx - 88 * s, y + 4 * s, cx + 88 * s, y + 22 * s, 12 * s, "star") * band
    y += 26 * s
    # roof: glass triangles between brass ribs (trapezoid widening down)
    ry0, ry1 = y, y + 70 * s
    tw, bw = 98 * s, 130 * s
    roof = shapes(W, H, [[(cx - tw, ry0), (cx + tw, ry0), (cx + bw, ry1), (cx - bw, ry1)]], smooth=False)
    roof_glass = []
    for k in range(4):
        xa0 = -tw + k * 2 * tw / 4; xa1 = -tw + (k + 1) * 2 * tw / 4
        xb0 = -bw + k * 2 * bw / 4; xb1 = -bw + (k + 1) * 2 * bw / 4
        m = 7 * s
        roof_glass.append(([(cx + xa0 + m, ry0 + m), (cx + xa1 - m, ry0 + m), (cx + xb1 - m, ry1 - m), (cx + xb0 + m, ry1 - m)], glass[(k + 1) % len(glass)]))
    y = ry1
    # body: three faces; middle face full width, side faces foreshortened
    by0, by1 = y, y + 200 * s
    faces = [(-bw, -bw * 0.5), (-bw * 0.5, bw * 0.5), (bw * 0.5, bw)]
    body = shapes(W, H, [[(cx - bw, by0), (cx + bw, by0), (cx + bw, by1), (cx - bw, by1)]], smooth=False)
    panes = []
    for i, (fx0, fx1) in enumerate(faces):
        m = 9 * s
        x0, x1 = cx + fx0 + m, cx + fx1 - m
        # tall pane with pointed-arch top
        mid = (x0 + x1) / 2; hw = (x1 - x0) / 2
        arch = [(x0, by0 + 46 * s)] + [(mid - hw * math.cos(a), by0 + 46 * s - math.sin(a) * 30 * s - (1 - abs(math.cos(a))) * 0) for a in np.linspace(0, math.pi / 2, 10)][1:]
        arch = [(x0, by0 + 46 * s)]
        for t in np.linspace(0, 1, 10)[1:]:
            arch.append((x0 + hw * t, by0 + 46 * s - (math.sin(t * math.pi / 2) ** 0.8) * 34 * s))
        arch2 = [(2 * mid - px, py) for px, py in arch[::-1]]
        pane = arch + arch2[1:] + [(x1, by1 - m), (x0, by1 - m)]
        panes.append((pane, glass[i % len(glass)], mid))
    y = by1
    # skirt: inverted trapezoid with small glass triangles
    sy0, sy1 = y, y + 60 * s
    skirt = shapes(W, H, [[(cx - bw, sy0), (cx + bw, sy0), (cx + 52 * s, sy1), (cx - 52 * s, sy1)]], smooth=False)
    skirt_glass = []
    for k in range(3):
        xa0 = -bw + k * 2 * bw / 3; xa1 = -bw + (k + 1) * 2 * bw / 3
        xb0 = -52 * s + k * 104 * s / 3; xb1 = -52 * s + (k + 1) * 104 * s / 3
        m = 7 * s
        skirt_glass.append(([(cx + xa0 + m, sy0 + m), (cx + xa1 - m, sy0 + m), (cx + xb1 - m, sy1 - m), (cx + xb0 + m, sy1 - m)], glass[(k + 2) % len(glass)]))
    y = sy1
    bowl = shapes(W, H, [[(cx - 52 * s, y), (cx + 52 * s, y)] + [(cx + math.cos(a) * 52 * s, y + math.sin(a) * 30 * s) for a in np.linspace(0, math.pi, 20)]], smooth=False)
    drop = shapes(W, H, [ellipse_pts(cx, y + 40 * s, 10 * s, 12 * s, 14), [(cx - 4 * s, y + 50 * s), (cx + 4 * s, y + 50 * s), (cx, y + 74 * s)]])
    bottom = y + 74 * s

    # halo behind (the lantern lights the night air)
    halo = np.clip(roof + body + skirt, 0, 1)
    art = over(art, glow(halo, LIGHT_D, radius=46 * s, strength=0.34 * glow_amt))
    art = over(art, glow(halo, LIGHT, radius=20 * s, strength=0.28 * glow_amt))
    # brass carcass first (glass sits in the openings)
    metal = np.clip(dome + band + crest + roof + body + skirt + bowl, 0, 1)
    art = brass(art, metal, BRASS, seed=nx())
    # copper accents on the cap and the bowl
    art = FO(art, np.clip(dome + bowl, 0, 1), COPPER, seed=nx(), emboss=0.9, sparkle=0.1)
    art = K(art, outline_of(np.clip(dome + bowl, 0, 1), 1.3), PATINA, seed=nx())
    # glass panes (glowing)
    for pane, col, mid in panes:
        pm = shape_mask(W, H, pane, smooth=False)
        art = OV(art, pm, lambda m, col=col: lit_glass(m, col, m.shape[1] / 2, m.shape[0] * 0.55, m.shape[1] * 0.5, nx()))
        # pierced brass overlay inside each pane (geometric fretwork)
        x0 = min(p[0] for p in pane); x1 = max(p[0] for p in pane)
        y0 = min(p[1] for p in pane); y1 = max(p[1] for p in pane)
        fret = []
        cell = 16 * s
        for yy in np.arange(y0 + cell, y1 - cell * 0.4, cell * 1.4):
            for xx in np.arange(x0 + cell * 0.6, x1, cell):
                fret.append(star_poly(xx, yy, cell * 0.55, cell * 0.24, 4, 0))
        fm = lines(W, H, fret, 2.0 * s, smooth=False) * gaussian_filter(pm, 1.0)
        art = FO(art, np.clip(fm * 1.4, 0, 1), BRASS, seed=nx(), emboss=0.3, sparkle=0.05)
        art = K(art, outline_of(pm, 1.2), PATINA, seed=nx(), alpha=0.9)
    for pane, col in roof_glass + skirt_glass:
        pm = shape_mask(W, H, pane, smooth=False)
        art = OV(art, pm, lambda m, col=col: lit_glass(m, col, m.shape[1] / 2, m.shape[0] / 2, m.shape[1] * 0.6, nx()))
        art = K(art, outline_of(pm, 1.2), PATINA, seed=nx(), alpha=0.9)
    # holes in dome & band glow
    holes = np.clip(dome_holes + band_holes, 0, 1)
    art = OV(art, holes, lambda m: rgba(flat(*m.shape, "#ffe2a0"), np.clip(gaussian_filter(m, 0.5) * 1.1, 0, 1)))
    art = over(art, glow(holes, LIGHT, radius=5 * s, strength=0.25))
    # rib highlights and small rivets along the edges
    rivets = [(cx + fx, by0 + 6 * s, 2.6 * s) for fx in (-bw + 5 * s, -bw * 0.5, bw * 0.5, bw - 5 * s)] + [(cx + fx, by1 - 6 * s, 2.6 * s) for fx in (-bw + 5 * s, -bw * 0.5, bw * 0.5, bw - 5 * s)]
    art = FO(art, circles(W, H, rivets), "#e8c27a", seed=nx(), emboss=1.0)
    art = brass(art, np.clip(ch + ringm + knob + drop, 0, 1), BRASS, seed=nx())
    return art, bottom


if "fanous" in PARTS:
    clear()
    W, H = 860, 1100
    art, bottom = fanous(W, H, 430, 0, 1.75, [RUBY, EMER, COBALT, AMBER], 3, chain_len=150)
    preview(art, "fm-fanous", bg=NIGHT)
    save(art, f"{OUT}/fanous.webp", max_w=420, quality=82)

if "fanous2" in PARTS:
    clear()
    W, H = 620, 900
    art, bottom = fanous(W, H, 310, 0, 1.2, [EMER, AMBER, TURQ, RUBY], 9, chain_len=260, glow_amt=0.9)
    preview(art, "fm-fanous2", bg=NIGHT)
    save(art, f"{OUT}/fanous2.webp", max_w=240, quality=82)


def lattice_masks(W, H, x0, y0, x1, y1, step, bead=0.42, bar=0.2, diag=True):
    """Mashrabiya turned-wood lattice: thin spindles on a (diagonal) grid, round beads at crossings and a
    small bulge mid-spindle. Openings stay roughly square so it reads as fine woodwork, not a grille."""
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ext = math.hypot(x1 - x0, y1 - y0) / 2 + step * 2
    cv.c.save()
    cv.c.translate(cx, cy)
    if diag:
        cv.c.rotate(45)
    n = int(ext / step) + 1
    for i in range(-n, n + 1):
        u = i * step
        cv.c.drawRect(skia.Rect(u - step * bar / 2, -ext, u + step * bar / 2, ext), p)
        cv.c.drawRect(skia.Rect(-ext, u - step * bar / 2, ext, u + step * bar / 2), p)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = i * step, j * step
            cv.c.drawCircle(u, v, step * bead / 2, p)
            cv.c.drawOval(skia.Rect(u + step / 2 - step * 0.18, v - step * 0.15, u + step / 2 + step * 0.18, v + step * 0.15), p)
            cv.c.drawOval(skia.Rect(u - step * 0.15, v + step / 2 - step * 0.18, u + step * 0.15, v + step / 2 + step * 0.18), p)
    cv.c.restore()
    return cv.array()[..., 3]


def wood(dst, mask, seed, col=WOOD, col2=WOOD_D, light=True):
    out = GP(dst, mask, col, col2, seed=seed, rough=1.0, streak=0.8)
    if light:
        # warm rim light on the upper-left edges of the turned wood
        gy, gx = np.gradient(gaussian_filter(mask, 1.6))
        rim = np.clip(-(gx + gy) * 3.0, 0, 1) * mask
        out = OV(out, rim, lambda m: rgba(flat(*m.shape, "#a8683a"), np.clip(m * 0.7, 0, 1)), pad=4)
    return out


if "balkon" in PARTS:
    # the projecting mashrabiya oriel, lit from inside, seen from the street at night
    clear()
    W, H = 820, 600
    art = blank(W, H)
    nx = Seq(500)
    L, R = 70, 750
    # inner light behind the lattice
    win = shapes(W, H, [[(L + 22, 70), (R - 22, 70), (R - 22, 380), (L + 22, 380)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lamp = np.clip(1 - np.hypot((xx - W / 2) / 380, (yy - 250) / 230), 0, 1)
    light = np.concatenate([np.stack([np.ones_like(lamp) * 1.0, 0.55 + 0.35 * lamp, 0.22 + 0.4 * lamp ** 2], -1), win[..., None]], -1).astype(np.float32)
    light[..., :3] *= (0.45 + 0.55 * lamp)[..., None]
    art = over(art, light)
    # stiles + lattice in three bays
    bays = [(L + 22, 290), (296, 524), (530, R - 22)]
    lat = np.zeros((H, W), np.float32)
    for bx0, bx1 in bays:
        lat = np.maximum(lat, lattice_masks(W, H, bx0, 70, bx1, 380, 20) * shapes(W, H, [[(bx0, 70), (bx1, 70), (bx1, 380), (bx0, 380)]], smooth=False))
    # solid carved medallion in the middle bay (eight-point star window)
    med = circles(W, H, [(410, 225, 70)])
    medwin = shapes(W, H, [star_poly(410, 225, 48, 26, 8, math.pi / 8)], smooth=False)
    lat = np.clip(np.maximum(lat * (1 - med), med - medwin), 0, 1)
    frame = shapes(W, H, [
        [(L, 40), (R, 40), (R, 70), (L, 70)], [(L, 380), (R, 380), (R, 410), (L, 410)],
        [(L, 40), (L + 22, 40), (L + 22, 410), (L, 410)], [(R - 22, 40), (R, 40), (R, 410), (R - 22, 410)],
        [(290, 70), (296, 70), (296, 380), (290, 380)], [(524, 70), (530, 70), (530, 380), (524, 380)],
    ], smooth=False)
    # cornice with dentils + crenellation, corbel tiers below
    cornice = shapes(W, H, [[(L - 26, 14), (R + 26, 14), (R + 14, 40), (L - 14, 40)]], smooth=False)
    cren = shapes(W, H, [[(x, 14), (x + 8, 0), (x + 16, 14)] for x in range(L - 20, R + 20, 24)], smooth=False)
    tiers = shapes(W, H, [
        [(L - 10, 410), (R + 10, 410), (R - 10, 440), (L + 10, 440)],
        [(L + 30, 440), (R - 30, 440), (R - 60, 476), (L + 60, 476)],
        [(L + 100, 476), (R - 100, 476), (R - 150, 512), (L + 150, 512)],
        [(L + 190, 512), (R - 190, 512), (R - 240, 540), (L + 240, 540)],
    ], smooth=False)
    art = wood(art, np.clip(lat, 0, 1), nx())
    ring_m = ring(W, H, 410, 225, 70, 6)
    art = wood(art, ring_m, nx(), "#5a3620", WOOD_D)
    art = wood(art, np.clip(frame + cornice + cren + tiers, 0, 1), nx(), WOOD_D, "#170c06")
    # carved fillets on the tiers (muqarnas-like cells) + dentils
    cells = []
    for (yA, yB, xa, xb, n) in ((410, 440, L - 10, R + 10, 26), (440, 476, L + 30, R - 30, 20), (476, 512, L + 100, R - 100, 15), (512, 540, L + 190, R - 190, 10)):
        stp = (xb - xa) / n
        for k in range(n):
            x = xa + k * stp + 3
            w_ = stp - 6
            arch = [(x, yB - 3), (x, yA + (yB - yA) * 0.45)] + [(x + w_ / 2 - math.cos(t) * w_ / 2, yA + (yB - yA) * 0.45 - math.sin(t) * (yB - yA) * 0.35) for t in np.linspace(0.15, math.pi - 0.15, 9)] + [(x + w_, yA + (yB - yA) * 0.45), (x + w_, yB - 3)]
            cells.append(arch)
    cm = lines(W, H, cells, 1.6, closed=False, smooth=False) * np.clip(gaussian_filter(tiers, 1) * 1.5 - 0.3, 0, 1)
    art = OV(art, cm, lambda m: rgba(flat(*m.shape, "#6a4126"), np.clip(m * 0.6, 0, 1)), pad=4)
    dent = shapes(W, H, [[(x, 46), (x + 10, 46), (x + 10, 62), (x, 62)] for x in range(L + 30, R - 30, 22)], smooth=False)
    art = OV(art, dent, lambda m: rgba(flat(*m.shape, "#120904"), np.clip(m * 0.7, 0, 1)), pad=4)
    # light spill on the tiers and a halo around the windows
    art = over(glow(win, LIGHT_D, radius=40, strength=0.3), art)
    art = add_grain(art, 5, 0.05)
    preview(art, "fm-balkon", bg=NIGHT)
    save(art, f"{OUT}/balkon.webp", max_w=780, quality=80)

if "kisi" in PARTS:
    # seamless dim lattice tile for section backgrounds (warm light through dark wood)
    clear()
    S = 260; st = 26
    base = np.zeros((S, S, 4), np.float32)
    base[..., :3] = np.array(hex_rgb("#5a2c17"), np.float32); base[..., 3] = 1
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    base[..., :3] *= (0.85 + 0.3 * tile_noise(S, S, 2, 30))[..., None]
    lat = np.zeros((S, S), np.float32)
    for ox in (-S, 0):
        lat = np.maximum(lat, lattice_masks(S, S, 0, 0, S, S, st, diag=False))
    lat = np.clip(lat, 0, 1)
    art = wood(base, lat, 7, "#2a170d", "#1a0e07")
    save_full(art, f"{OUT}/kisi.webp", quality=72)

if "divider" in PARTS:
    clear()
    W, H = 520, 120
    art = blank(W, H)
    nx = Seq(700)
    cx, cy = 260, 60
    rule = shapes(W, H, [[(30, cy - 2), (200, cy - 2), (200, cy + 2), (30, cy + 2)], [(320, cy - 2), (490, cy - 2), (490, cy + 2), (320, cy + 2)]], smooth=False)
    beads = circles(W, H, [(x, cy, 4.5) for x in (60, 110, 160, 360, 410, 460)])
    star = shapes(W, H, [star_poly(cx, cy, 44, 20, 8, math.pi / 8)], smooth=False)
    inner = shapes(W, H, [star_poly(cx, cy, 24, 11, 8, 0)], smooth=False)
    gems = [(x, cy, c) for x, c in ((200 + 0, RUBY), (320, EMER))]
    art = over(art, glow(inner, LIGHT_D, 18, 0.5))
    art = brass(art, np.clip(rule + beads + star, 0, 1), BRASS, seed=nx())
    art = OV(art, inner, lambda m: lit_glass(m, AMBER, m.shape[1] / 2, m.shape[0] / 2, m.shape[1] * 0.5, nx()))
    art = K(art, outline_of(inner, 1.2), PATINA, seed=nx())
    for x, y, c in gems:
        gm = shapes(W, H, [[(x - 12, y), (x, y - 12), (x + 12, y), (x, y + 12)]], smooth=False)
        art = OV(art, gm, lambda m, c=c: lit_glass(m, c, m.shape[1] / 2, m.shape[0] / 2, m.shape[1] * 0.5, nx()))
        art = K(art, outline_of(gm, 1.2), PATINA, seed=nx())
    preview(art, "fm-divider", bg=NIGHT)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=84)

if "bintang" in PARTS:
    clear()
    W, H = 160, 160
    art = blank(W, H)
    nx = Seq(800)
    star = shapes(W, H, [star_poly(80, 80, 70, 34, 8, math.pi / 8)], smooth=False)
    win = shapes(W, H, [star_poly(80, 80, 40, 18, 8, 0)], smooth=False)
    art = brass(art, star, BRASS, seed=nx())
    art = OV(art, win, lambda m: lit_glass(m, RUBY, m.shape[1] / 2, m.shape[0] / 2, m.shape[1] * 0.45, nx()))
    holes = circles(W, H, [(80 + math.cos(a) * 54, 80 + math.sin(a) * 54, 3.5) for a in np.linspace(0, math.tau, 8, endpoint=False) + math.pi / 8])
    art = OV(art, holes, lambda m: rgba(flat(*m.shape, "#ffe2a0"), m))
    art = K(art, outline_of(win, 1.2), PATINA, seed=nx())
    preview(art, "fm-bintang", bg=NIGHT)
    save(art, f"{OUT}/bintang.webp", max_w=80, quality=84)

kb(OUT)
