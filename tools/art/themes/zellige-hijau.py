"""Zellige Hijau — Moroccan riad: hand-cut zellige mosaic (each glazed piece with uneven glaze, grout lines, chipped
edges) in emerald / teal / white, horseshoe arch, courtyard fountain, orange-tree branch.
Run: python3 -I zellige-hijau.py [part ...]   parts: band star arch fountain orange
Assets -> public/themes/art/zellige-hijau/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a3_lib import *

OUT = outdir("zellige-hijau")
PARTS = sys.argv[1:] or ["band", "star", "arch", "fountain", "orange", "mosaic", "plaster"]
EMERALD, TEAL, WHITE, DEEP, HONEY, BLACK = "#1f6a4f", "#1d7c82", "#f1ece0", "#0f3b31", "#c99a3e", "#1e2a28"
PLASTER = "#f3ede1"


def star_cross_mask(W, H, d, ox, oy, rng, grout=3.2, wob=0.9, inner=True):
    """Grout lines for star-and-cross zellige plus inner 8-point rosettes inside alternate stars."""
    polys, centres = [], []
    for (i, j), pts in star_cross_polys(0, 0, W, H, d, ox, oy, rng, wob):
        polys.append(pts); centres.append((i, j, pts))
    lines = poly_lines(W, H, polys, grout)
    if inner:
        ins = []
        for i, j, pts in centres:
            cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
            ins.append(wob_poly(star_pts(cx, cy, d * 0.26, d * 0.26 * 0.7654, 8, math.pi / 8), rng, wob * 0.6))
            ins.append(wob_poly([(cx + math.cos(a) * d * 0.26 * 0.7, cy + math.sin(a) * d * 0.26 * 0.7) for a in [k * math.pi / 4 + math.pi / 8 for k in range(8)]], rng, 0.3))
            # spokes between rosette and star points split the star into kite pieces
            for k in range(8):
                a = k * math.pi / 4 + math.pi / 8
                ins.append([(cx + math.cos(a) * d * 0.26 * 0.7654, cy + math.sin(a) * d * 0.26 * 0.7654), (cx + math.cos(a) * d * 0.5 * 0.7654, cy + math.sin(a) * d * 0.5 * 0.7654)])
        lines = np.maximum(lines, poly_lines(W, H, ins[0::1], grout * 0.85, closed=True))
    return lines, centres


def zcolour(d, ox, oy):
    def f(i, cx, cy, rng):
        # classify by position relative to nearest star centre
        gi, gj = round((cx - ox) / d), round((cy - oy) / d)
        dx, dy = cx - (ox + gi * d), cy - (oy + gj * d)
        r = math.hypot(dx, dy) / d
        if r < 0.2:
            return HONEY if (gi + gj) % 3 == 0 else WHITE
        if r < 0.45:
            return EMERALD if (gi + gj) % 2 else TEAL
        return WHITE if rng.random() > 0.08 else "#e7dcc2"
    return f


def frame_lines(W, H, x0, y0, x1, y1, t, rng, grout=3.0):
    """Border band of alternating small squares-on-point between two fillets."""
    out = [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)], [(x0 + t, y0 + t), (x1 - t, y0 + t), (x1 - t, y1 - t), (x0 + t, y1 - t)]]
    return poly_lines(W, H, [wob_poly(p, rng, 0.7) for p in out], grout)


if "band" in PARTS:
    # horizontal dado / divider strip: black-white fillets, chevron of small tiles, star-and-cross row
    W, H = 1000, 176
    rng = random.Random(5)
    d = 104; ox, oy = 52, 88
    lines, _ = star_cross_mask(W, H, d, ox, oy, rng, grout=3.2)
    # top + bottom fillet rows of small square tiles
    sq = []
    for row_y, hh in [(6, 18), (H - 24, 18)]:
        x = 0
        while x < W:
            w_ = 24
            sq.append(wob_poly([(x, row_y), (x + w_, row_y), (x + w_, row_y + hh), (x, row_y + hh)], rng, 0.6)); x += w_
    lines = np.maximum(lines, poly_lines(W, H, sq, 3.0))
    lines = np.maximum(lines, poly_lines(W, H, [[(0, 28), (W, 28)], [(0, H - 28), (W, H - 28)], [(0, 2), (W, 2)], [(0, H - 2), (W, H - 2)]], 3.4, closed=False))
    lab, n = label_regions(lines)
    zc = zcolour(d, ox, oy)

    def col(i, cx, cy, r):
        if cy < 28 or cy > H - 28:
            return BLACK if int(cx // 24) % 2 else WHITE
        return zc(i, cx, cy, r)
    art = tile_glaze(lab, n, col, seed=11, bevel=3.4, chip=0.8)
    art[..., 3] = np.clip(art[..., 3] * shapes(W, H, [wob_poly([(1, 1), (W - 1, 1), (W - 1, H - 1), (1, H - 1)], rng, 0.8)], smooth=False), 0, 1)
    preview(art, "z-band")
    save(art, f"{OUT}/band.webp", max_w=760, quality=80)

if "star" in PARTS:
    # single star medallion: a 16-point khatam rosette cut from emerald/teal/white/honey pieces, round-ish outline
    W = H = 420; cx = cy = W / 2
    rng = random.Random(7)
    polys = []
    R = 196
    polys.append(wob_poly(star_pts(cx, cy, R, R * 0.80, 16, 0), rng, 0.8))
    polys.append(wob_poly(star_pts(cx, cy, R * 0.66, R * 0.66 * 0.7654, 8, math.pi / 8), rng, 0.7))
    polys.append(wob_poly(star_pts(cx, cy, R * 0.3, R * 0.3 * 0.7654, 8, 0), rng, 0.6))
    polys.append(wob_poly([(cx + math.cos(a) * R * 0.16, cy + math.sin(a) * R * 0.16) for a in [k * math.pi / 4 for k in range(8)]], rng, 0.3))
    spokes = []
    for k in range(16):
        a = k * math.pi / 8
        r0 = R * 0.66 if k % 2 else R * 0.66 * 0.7654
        spokes.append([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * R, cy + math.sin(a) * R)])
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        spokes.append([(cx + math.cos(a) * R * 0.3 * 0.7654, cy + math.sin(a) * R * 0.3 * 0.7654), (cx + math.cos(a) * R * 0.66, cy + math.sin(a) * R * 0.66)])
        a = k * math.pi / 4
        spokes.append([(cx + math.cos(a) * R * 0.3, cy + math.sin(a) * R * 0.3), (cx + math.cos(a) * R * 0.66 * 0.7654, cy + math.sin(a) * R * 0.66 * 0.7654)])
    lines = np.maximum(poly_lines(W, H, polys, 3.4), poly_lines(W, H, spokes, 3.0, closed=False))
    outer = shapes(W, H, [star_pts(cx, cy, R + 2, (R + 2) * 0.80, 16, 0)], smooth=False)
    lab, n = label_regions(lines, outer)

    def col(i, x, y, r):
        rr = math.hypot(x - cx, y - cy) / R
        ang = (math.atan2(y - cy, x - cx) % (math.pi / 4)) / (math.pi / 4)
        if rr < 0.14: return HONEY
        if rr < 0.27: return WHITE
        if rr < 0.52: return EMERALD
        k = int(math.floor((math.atan2(y - cy, x - cx) + math.tau) / (math.pi / 8))) % 2
        k8 = int(math.floor((math.atan2(y - cy, x - cx) + math.tau) / (math.pi / 8))) % 2
        if rr < 0.55: return EMERALD if k8 else TEAL
        return WHITE if k else DEEP
    art = tile_glaze(lab, n, col, seed=21, bevel=3.6, chip=0.9, inside=gaussian_filter(outer, 0.6))
    preview(art, "z-star")
    save(art, f"{OUT}/star.webp", max_w=200, quality=82)

if "arch" in PARTS:
    # riad wall: horseshoe arch (transparent opening for the photo), voussoir band of narrow tiles, alfiz frame,
    # star-and-cross spandrels. Exact canvas (not trimmed) so CSS can place the photo behind the opening.
    W, H = 780, 900
    cx, cyc, r = 390, 400, 262
    a_spring = math.radians(28)  # horseshoe: arc continues 28 deg below the centre line
    jx = r * math.cos(a_spring); jy = cyc + r * math.sin(a_spring)
    rng = random.Random(9)
    arc = [(cx + math.cos(a) * r, cyc + math.sin(a) * r) for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 90)]
    opening_pts = [(cx - jx, H + 4)] + [(cx - math.cos(a_spring) * r, jy)] + arc[1:-1][::-1][::-1] + [(cx + jx, jy), (cx + jx, H + 4)]
    opening = shapes(W, H, [[(cx - jx, H + 4)] + [(cx + math.cos(a) * r, cyc + math.sin(a) * r) for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 90)] + [(cx + jx, H + 4)]], smooth=False)
    band_w = 46
    outer_arch = shapes(W, H, [[(cx - jx - band_w * 0.95, H + 4)] + [(cx + math.cos(a) * (r + band_w), cyc + math.sin(a) * (r + band_w)) for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 90)] + [(cx + jx + band_w * 0.95, H + 4)]], smooth=False)
    ax0, ay0, ax1 = 46, 70, W - 46
    alfiz_t = 40
    wall = shapes(W, H, [[(ax0, ay0), (ax1, ay0), (ax1, H + 4), (ax0, H + 4)]], smooth=False)
    # voussoirs: radial cuts through the arch band
    vous = []
    for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 37):
        vous.append([(cx + math.cos(a) * (r - 2), cyc + math.sin(a) * (r - 2)), (cx + math.cos(a) * (r + band_w + 2), cyc + math.sin(a) * (r + band_w + 2))])
    for y in np.arange(jy + 40, H, 40):
        vous.append([(cx - jx - band_w, y), (cx - jx, y)]); vous.append([(cx + jx, y), (cx + jx + band_w, y)])
    # inner fillet ring of the band
    mid_arc = [[(cx - jx - band_w * 0.5, H + 4)] + [(cx + math.cos(a) * (r + band_w * 0.5), cyc + math.sin(a) * (r + band_w * 0.5)) for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 90)] + [(cx + jx + band_w * 0.5, H + 4)]]
    lines = poly_lines(W, H, vous, 3.0, closed=False)
    lines = np.maximum(lines, poly_lines(W, H, mid_arc, 3.0, closed=False))
    # edges: band border, alfiz rectangle
    edge_lines = []
    edge_lines.append([(cx - jx - band_w, H + 4)] + [(cx + math.cos(a) * (r + band_w), cyc + math.sin(a) * (r + band_w)) for a in np.linspace(math.pi - a_spring, math.tau + a_spring, 90)] + [(cx + jx + band_w, H + 4)])
    edge_lines.append([(ax0 + alfiz_t, H + 4), (ax0 + alfiz_t, ay0 + alfiz_t), (ax1 - alfiz_t, ay0 + alfiz_t), (ax1 - alfiz_t, H + 4)])
    lines = np.maximum(lines, poly_lines(W, H, [wob_poly(p, rng, 0.5) for p in edge_lines], 3.4, closed=False))
    # alfiz: chain of small square-on-point tiles
    al = []
    for t in np.arange(ay0 + 4, H, alfiz_t * 0.72):
        for xx in (ax0 + alfiz_t / 2, ax1 - alfiz_t / 2):
            s_ = alfiz_t * 0.36
            al.append(wob_poly([(xx, t), (xx + s_, t + s_), (xx, t + 2 * s_), (xx - s_, t + s_)], rng, 0.6))
    for t in np.arange(ax0 + alfiz_t * 0.9, ax1 - alfiz_t * 0.6, alfiz_t * 0.72):
        yy = ay0 + alfiz_t / 2; s_ = alfiz_t * 0.36
        al.append(wob_poly([(t - s_, yy), (t, yy - s_), (t + s_, yy), (t, yy + s_)], rng, 0.6))
    lines = np.maximum(lines, poly_lines(W, H, al, 3.0))
    # spandrel star-and-cross
    d = 92; ox, oy = cx, ay0 + alfiz_t + 46
    sl, _ = star_cross_mask(W, H, d, ox, oy, rng, grout=3.2)
    spandrel = np.clip(wall - outer_arch, 0, 1) * (1 - shapes(W, H, [[(0, 0), (W, 0), (W, ay0 + alfiz_t), (0, ay0 + alfiz_t)]], smooth=False))
    side = np.zeros((H, W), np.float32); side[:, :int(ax0 + alfiz_t)] = 1; side[:, int(ax1 - alfiz_t):] = 1
    spandrel *= 1 - side
    lines = np.maximum(lines, sl * (spandrel > 0.5))
    lines = np.clip(lines, 0, 1)
    inside = np.clip(wall - opening, 0, 1)
    lab, n = label_regions(lines, inside)
    zc = zcolour(d, ox, oy)

    def col(i, x, y, rr):
        rd = math.hypot(x - cx, y - cyc)
        in_band = (y < jy and r - 1 < rd < r + band_w + 2) or (y >= jy and (abs(x - cx) > jx - 1 and abs(x - cx) < jx + band_w + 2))
        if in_band:
            if (y < jy and rd < r + band_w * 0.5) or (y >= jy and abs(x - cx) < jx + band_w * 0.5):
                k = int(round(math.atan2(y - cyc, x - cx) / (math.tau / 36))) if y < jy else int(y // 40)
                return EMERALD if k % 2 else WHITE
            return BLACK if rr.random() > 0.1 else DEEP
        if x < ax0 + alfiz_t or x > ax1 - alfiz_t or y < ay0 + alfiz_t:
            # alfiz: on-point squares teal / honey on white
            dxl = min(abs(x - (ax0 + alfiz_t / 2)), abs(x - (ax1 - alfiz_t / 2)))
            if (dxl < alfiz_t * 0.3 and y > ay0 + alfiz_t * 0.4) or (abs(y - (ay0 + alfiz_t / 2)) < alfiz_t * 0.3 and ax0 + alfiz_t * 0.6 < x < ax1 - alfiz_t * 0.6):
                return TEAL if int(y // 29 + x // 29) % 3 else HONEY
            return WHITE
        return zc(i, x, y, rr)
    art = tile_glaze(lab, n, col, seed=31, bevel=3.4, chip=0.7, inside=gaussian_filter(inside, 0.6))
    # soft shadow of the arch reveal on the photo side (depth) — painted as a translucent dark rim inside the opening
    rim = np.clip(gaussian_filter(1 - opening, 9) * opening * 1.6, 0, 0.55)
    sh = rgba(flat(H, W, "#0b2a22"), rim * (1 - np.clip((np.mgrid[0:H, 0:W][0] - jy) / 400, 0, 1) * 0.5))
    art = over(sh, art)
    preview(art, "z-arch", bg="#c9b9a0")
    save_full(art, f"{OUT}/arch.webp", size=(640, 738), quality=80)

if "fountain" in PARTS:
    clear()
    # courtyard fountain: zellige-clad octagonal basin (front view), white marble bowl, water jet — watercolour water
    W, H = 640, 520
    rng = random.Random(41)
    cx = W / 2
    by, ty = 500, 360  # basin bottom / top
    basin = shapes(W, H, [[(60, ty), (W - 60, ty), (W - 70, by), (70, by)]], smooth=False)
    facets = [[(60, ty), (170, ty), (170, by), (70, by)], [(170, ty), (W - 170, ty), (W - 170, by), (170, by)], [(W - 170, ty), (W - 60, ty), (W - 70, by), (W - 170, by)]]
    lines = poly_lines(W, H, [wob_poly(p, rng, 0.5) for p in facets], 3.2)
    rim_y0 = ty - 18
    rim = shapes(W, H, [[(44, rim_y0), (W - 44, rim_y0), (W - 52, ty + 10), (52, ty + 10)]], smooth=False)
    # small star-and-cross on front facet, diagonal checks on side facets
    sl, _ = star_cross_mask(W, H, 64, cx, (ty + by) / 2, rng, grout=2.8, inner=False)
    front = shapes(W, H, [facets[1]], smooth=False)
    lines = np.maximum(lines, sl * front)
    chk = []
    for x0 in (70, W - 170):
        for i in range(0, 6):
            for j in range(0, 7):
                s_ = 20
                px, py = x0 + 8 + i * s_ * 1.0 + (j % 2) * s_ * 0.5, ty + 12 + j * s_
                chk.append(wob_poly([(px, py - s_ / 2), (px + s_ / 2, py), (px, py + s_ / 2), (px - s_ / 2, py)], rng, 0.4))
    side = np.maximum(shapes(W, H, [facets[0]], smooth=False), shapes(W, H, [facets[2]], smooth=False))
    lines = np.maximum(lines, poly_lines(W, H, chk, 2.6) * side)
    lab, n = label_regions(np.maximum(lines, outline_of(basin, 2)), basin)

    def col(i, x, y, rr):
        if 170 < x < W - 170:
            gi, gj = round((x - cx) / 64), round((y - (ty + by) / 2) / 64)
            if (gi + gj) % 2 == 0 and math.hypot(x - (cx + gi * 64), y - ((ty + by) / 2 + gj * 64)) < 20:
                return EMERALD
            return WHITE
        return TEAL if int((x + y) // 14) % 2 else WHITE
    art = blank(W, H)
    shadow = shapes(W, H, [deform(ellipse_pts(cx, by + 6, 300, 12, 16), rng, 1, 0.05)])
    art = G(art, shadow, "#000000", seed=3, density=0.25, edge=0.1, bloom=0, rough=3, feather=5)
    tiles = tile_glaze(lab, n, col, seed=43, bevel=2.8, chip=0.6, inside=gaussian_filter(basin, 0.6))
    art = over(art, tiles)
    # marble rim
    art = GP(art, rim, "#eee8dc", "#d5ccbb", seed=45, rough=0.8, streak=0.5)
    art = G(art, np.clip(rim - np.roll(rim, -5, 0), 0, 1), "#8f8576", seed=46, density=0.5, edge=0.1, bloom=0, rough=0.6)
    # bowl on a pedestal
    ped = shapes(W, H, [[(cx - 22, rim_y0), (cx - 14, 230), (cx + 14, 230), (cx + 22, rim_y0)]], smooth=False)
    bowl = shapes(W, H, [[(cx - 130, 214), (cx + 130, 214), (cx + 100, 244), (cx + 40, 258), (cx - 40, 258), (cx - 100, 244)]])
    art = GP(art, ped, "#e9e2d4", "#c9bfae", seed=47, rough=0.8)
    art = GP(art, bowl, "#f2ece1", "#cfc5b3", seed=48, rough=0.8, streak=0.5)
    art = G(art, np.clip(bowl * (np.mgrid[0:H, 0:W][0] > 236), 0, 1), "#9c917f", seed=49, density=0.35, edge=0.2, bloom=0, rough=0.8)
    # water: jet + falling sheets + basin surface
    jet = strokes(W, H, [(curve([(cx, 214), (cx + 2, 120), (cx, 70)], 20), 9, (0.0, 0.5))])
    falls = strokes(W, H, [(curve([(cx, 80), (cx - 60 - k * 10, 120 + k * 4), (cx - 112 - k * 6, 214)], 24), 3.2, (0.05, 0.3)) for k in range(3)] +
                    [(curve([(cx, 80), (cx + 60 + k * 10, 120 + k * 4), (cx + 112 + k * 6, 214)], 24), 3.2, (0.05, 0.3)) for k in range(3)])
    sheet = strokes(W, H, [([(cx + x, 242), (cx + x * 1.4 + rng.uniform(-3, 3), rim_y0 - 2)], 2.4, (0.0, 0.3)) for x in np.linspace(-110, 110, 18)])
    art = G(art, np.maximum(jet, falls), "#6fb4b6", "#3f8f95", seed=51, density=0.8, edge=0.6, bloom=0.2, rough=2, feather=1.0)
    art = G(art, sheet, "#8cc3c2", seed=52, density=0.6, edge=0.4, bloom=0, rough=1.5, feather=0.8)
    water = shapes(W, H, [[(64, rim_y0 + 4), (W - 64, rim_y0 + 4), (W - 70, rim_y0 + 12), (70, rim_y0 + 12)]], smooth=False)
    art = G(art, water, "#4f9ea2", "#2f7a7e", seed=53, density=0.6, edge=0.5, bloom=0.3, rough=2)
    drops = circles(W, H, [(cx + rng.gauss(0, 90), rng.uniform(70, 230), rng.uniform(1.2, 2.6)) for _ in range(40)])
    art = G(art, drops, "#7bb8b8", seed=54, density=0.6, edge=0.3, bloom=0, rough=0.5, feather=0.4)
    preview(art, "z-fountain")
    save(art, f"{OUT}/fountain.webp", max_w=420, quality=82)

if "orange" in PARTS:
    clear()
    # bitter-orange branch (riad courtyard tree): glossy elliptic leaves, fruits, white blossoms — gouache + watercolour
    W, H = 640, 520
    rng = random.Random(61); nx = Seq(6100)
    art = blank(W, H)
    main = curve([(630, 30), (520, 96), (400, 176), (270, 262), (140, 352), (20, 450)], 60)
    twigs = [curve([(400, 176), (380, 250), (348, 300)], 20), curve([(270, 262), (250, 196), (214, 150)], 20),
             curve([(520, 96), (536, 170), (512, 236)], 20), curve([(140, 352), (150, 410), (176, 450)], 16)]
    stem = strokes(W, H, [(main, 10, (0.0, 0.5))] + [(t, 5, (0.0, 0.6)) for t in twigs])
    art = G(art, stem, "#6b4a2e", "#3e2a1a", seed=nx(), density=0.8, edge=0.5, bloom=0.1, rough=1.5, feather=0.8)
    LA, LB, LD = "#2f6b3e", "#1b4a2e", "#10301e"
    spots = []
    for pts in [main] + twigs:
        for k, (x, y, a) in enumerate(along(pts, 34)):
            side = 1 if k % 2 else -1
            spots.append((x, y, a + side * rng.uniform(0.7, 1.2), rng.uniform(62, 86)))
    for (x, y, a, L) in spots:
        m = shape_mask(W, H, deform(petal_pts(x, y, L, L * 0.27, a, n=14, cup=0.1), rng, 1, 0.02))
        art = GP(art, m, mix(LA, "#4b8a52", rng.random() * 0.5), LB, seed=nx(), rough=1.4, streak=0.8)
        half = shape_mask(W, H, petal_pts(x, y, L * 0.95, L * 0.12, a + 0.1, n=10)) * m
        art = G(art, half, LD, seed=nx(), density=0.45, edge=0.3, bloom=0.2, rough=1.5)
        vein = strokes(W, H, [([(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in (0.08, 0.5, 0.9)], 1.4, (0.1, 0.5))])
        art = G(art, vein, "#a9c79a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4)
        hl = shape_mask(W, H, petal_pts(x + math.cos(a - 1.3) * 5, y + math.sin(a - 1.3) * 5, L * 0.55, L * 0.06, a - 0.05, n=8)) * m
        art = OV(art, hl, lambda mm: rgba(flat(*mm.shape, "#e6f2dc"), gaussian_filter(mm, 1.2) * 0.5))
    for (x, y, rr) in [(352, 318, 36), (512, 258, 31), (220, 168, 27), (178, 462, 26)]:
        fruit = shape_mask(W, H, deform(ellipse_pts(x, y, rr, rr * 0.95, 14), rng, 1, 0.03))
        art = OV(art, fruit, lambda mm: soft_shadow(mm, "#1b2a1a", 5, 0.35, 3, 5)[..., :] , pad=20)
        art = GP(art, fruit, "#f39a2a", "#e0681a", seed=nx(), rough=1.0, streak=0.6)
        sh = shape_mask(W, H, deform(ellipse_pts(x + rr * 0.35, y + rr * 0.35, rr * 0.75, rr * 0.65, 10), rng, 1, 0.05)) * fruit
        art = G(art, sh, "#b9481a", seed=nx(), density=0.5, edge=0.25, bloom=0.2, rough=2)
        art = OV(art, circles(W, H, [(x - rr * 0.35, y - rr * 0.38, rr * 0.2)]) * fruit, lambda mm: rgba(flat(*mm.shape, "#fff1cf"), gaussian_filter(mm, 2.5) * 0.85))
        pores = circles(W, H, [(x + rng.gauss(0, rr * 0.4), y + rng.gauss(0, rr * 0.4), 0.9) for _ in range(50)]) * fruit
        art = G(art, pores, "#b8561a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.3)
        cap = shapes(W, H, [petal_pts(x + rr * 0.05, y - rr * 0.9, 10, 5, a2, n=8) for a2 in (-2.4, -0.7)])
        art = GP(art, cap, LB, seed=nx(), rough=0.6)
    for (x, y, rr) in [(608, 44, 19), (440, 150, 17), (290, 236, 16), (84, 400, 17), (560, 130, 14), (120, 330, 14)]:
        rot = rng.uniform(0, 1)
        polys = [petal_pts(x, y, rr, rr * 0.48, k * math.tau / 5 + rot, n=12) for k in range(5)]
        m = shapes(W, H, polys)
        art = G(art, np.roll(np.roll(m, 2, 0), 2, 1), "#8e9890", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1, feather=1.2)
        art = GP(art, m, "#fffdf6", "#efe9dc", seed=nx(), rough=0.8, streak=0.3)
        art = G(art, np.clip((m - gaussian_filter(m, 1.2)) * 3, 0, 1), "#a59c8c", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5, feather=0.4)
        art = G(art, circles(W, H, [(x, y, rr * 0.22)]), "#e6c33c", "#b9a53a", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6)
    preview(art, "z-orange")
    save(art, f"{OUT}/orange.webp", max_w=360, quality=82)

if "mosaic" in PARTS:
    clear()
    # seamless texture: on-point square zellige (diagonal checker) — portrait rings, card strips
    n = 240; t = 20
    rng = random.Random(71)
    lines = []
    for k in range(-n // t, 2 * n // t + 1):
        lines.append([(k * t - n, -n), (k * t + n, n)]); lines.append([(k * t - n, n), (k * t + n, -n)])
    # shift so lines hit the texture edges at the same places on both sides
    g = poly_lines(n, n, [[(x + 10, y), (x2 + 10, y2)] for (x, y), (x2, y2) in lines], 2.6, closed=False)
    lab, nl = label_regions(g)

    def col(i, x, y, r):
        u = round(((x - 10) + y) / t); v = round(((x - 10) - y) / t)
        return [EMERALD, TEAL, WHITE, DEEP][(u % 2) * 2 + (v % 2)]
    art = tile_glaze(lab, nl, col, seed=73, bevel=2.6, chip=0.5)
    save_tex(art, f"{OUT}/mosaic.webp", quality=78)
    preview(art, "z-mosaic")

if "plaster" in PARTS:
    # seamless lime plaster (tadelakt-like trowel clouds)
    n = 320
    rgb = flat(n, n, PLASTER) * (0.97 + 0.05 * noise(n, n, 3, 26, True)[..., None] - 0.025 * noise(n, n, 4, 6, True)[..., None] + 0.015 * noise(n, n, 5, 1, True)[..., None])
    save_tex(rgba(rgb, np.ones((n, n), np.float32)), f"{OUT}/plaster.webp", quality=70)

report(OUT)
