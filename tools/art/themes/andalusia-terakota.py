"""Andalusia Terakota — Alhambra-inspired: carved plaster (yeseria) triple arcade with lobed arches on marble
colonnettes, muqarnas frieze, sebka lattice relief, terracotta + cobalt cuerda-seca tiles, warm stone.
Run: python3 -I andalusia-terakota.py [part ...]   parts: arcade muqarnas tile rosette
Assets -> public/themes/art/andalusia-terakota/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a3_lib import *

OUT = outdir("andalusia-terakota")
PARTS = sys.argv[1:] or ["arcade", "muqarnas", "tile", "rosette"]
PLASTER, PLASTER_D, DIRT = "#ecdcbf", "#d6c09b", "#8a6a48"
COBALT, TERRA, HONEY, GREEN, MANG, TIN = "#23418f", "#b5532e", "#d39a3a", "#3f7a4f", "#2b1d17", "#f2e8d3"


def lobed_opening(W, H, cx, top, R, lobes, rl, bottom):
    """Multifoil arch opening: discs on a semicircle + inner fill + rectangle to `bottom`. Returns mask."""
    cy = top + R
    items = []
    for k in range(lobes):
        a = math.pi + math.pi * (k + 0.5) / lobes
        items.append((cx + math.cos(a) * (R - rl * 0.55), cy + math.sin(a) * (R - rl * 0.55), rl))
    m = circles(W, H, items + [(cx, cy, R - rl * 0.9)])
    rect = shapes(W, H, [[(cx - R + rl * 0.05, cy), (cx + R - rl * 0.05, cy), (cx + R - rl * 0.05, bottom), (cx - R + rl * 0.05, bottom)]], smooth=False)
    return np.clip(np.maximum(m, rect), 0, 1)


def sebka(W, H, cell, ox, oy, width=3.2):
    """Rhombus lattice of lobed ribs (sebka) as a raised-rib mask + leaf fillers."""
    ribs = []
    n = int(max(W, H) / cell) + 4
    for k in range(-n, n):
        x0 = ox + k * cell
        for sgn in (1, -1):
            pts = []
            for t in np.linspace(-H, 2 * H, 160):
                y = oy + t
                x = x0 + sgn * t * 0.62 + math.sin(t / cell * math.pi * 2) * cell * 0.08
                pts.append((x, y))
            ribs.append((pts, width, None))
    rib = strokes(W, H, ribs)
    leaves = []
    for i in range(-n, n):
        for j in range(-n, n):
            x = ox + i * cell + (j % 2) * cell / 2
            y = oy + j * cell * 0.81
            if -20 < x < W + 20 and -20 < y < H + 20:
                leaves.append(petal_pts(x, y - cell * 0.18, cell * 0.36, cell * 0.12, -math.pi / 2, n=10))
                leaves.append(petal_pts(x, y + cell * 0.02, cell * 0.22, cell * 0.08, math.pi / 2 - 0.9, n=8))
                leaves.append(petal_pts(x, y + cell * 0.02, cell * 0.22, cell * 0.08, math.pi / 2 + 0.9, n=8))
    return rib, shapes(W, H, leaves)


def muqarnas_height(W, H, cols, rows, cell_w, row_h, x0, y0):
    """Rows of stalactite niches: each a little pointed niche, concave (height falls toward its crown)."""
    hgt = np.full((H, W), 0.95, np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for r in range(rows):
        off = (r % 2) * cell_w / 2
        w_ = cell_w * (1 - r * 0.0)
        for c in range(-1, cols + 1):
            cx = x0 + off + c * w_
            yb = y0 + (r + 1) * row_h
            yt = y0 + r * row_h
            # niche outline: vertical sides, pointed top
            u = (xx - cx) / (w_ * 0.46)
            v = (yb - yy) / row_h  # 0 at bottom .. 1 at top
            crown = 0.62 + 0.38 * (1 - np.abs(u) ** 1.4)
            inside = (np.abs(u) < 1) & (v > 0) & (v < crown)
            depth = (1 - np.clip(np.abs(u), 0, 1) ** 2) * np.clip(v / crown, 0, 1) ** 0.7
            hgt = np.where(inside, np.minimum(hgt, 0.95 - depth * 0.85 - 0.05), hgt)
            # mark processed so overlapping rows don't double; default plane 0.95
        # plane where not inside any niche handled below
    return hgt


if "arcade" in PARTS:
    # triple arcade: tall central lobed arch + two smaller side arches on marble colonnettes; carved sebka spandrels,
    # epigraphic-style band replaced by a geometric interlace band (no script), muqarnas frieze on top.
    W, H = 780, 760
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    clear()
    mq_h = 96
    ops = [lobed_opening(W, H, 390, 248, 150, 9, 30, H + 4),
           lobed_opening(W, H, 120, 330, 84, 7, 20, H + 4),
           lobed_opening(W, H, 660, 330, 84, 7, 20, H + 4)]
    opening = np.clip(np.maximum.reduce(ops), 0, 1)
    wall = np.ones((H, W), np.float32)
    # height map
    hgt = np.full((H, W), 0.55, np.float32)
    mq = muqarnas_height(W, H, 12, 2, 68, mq_h / 2, -10, 0)
    top = yy < mq_h
    hgt[top] = mq[top] * 0.9
    # bead moulding under muqarnas
    bead = circles(W, H, [(x, mq_h + 8, 5.5) for x in np.arange(6, W, 15)])
    fillet = shapes(W, H, [[(0, mq_h), (W, mq_h), (W, mq_h + 2), (0, mq_h + 2)], [(0, mq_h + 15), (W, mq_h + 15), (W, mq_h + 19), (0, mq_h + 19)]], smooth=False)
    # geometric interlace band (two interlaced zigzag ribbons)
    band_y0, band_y1 = mq_h + 24, mq_h + 74
    zz = []
    for ph in (0, 1):
        pts = []
        for x in np.arange(-40, W + 40, 4):
            t = (x / 50.0 + ph) % 2
            yv = band_y0 + 6 + (band_y1 - band_y0 - 12) * (t if t < 1 else 2 - t)
            pts.append((x, yv))
        zz.append((pts, 5, None))
    zz.append(([(0, band_y0), (W, band_y0)], 3, None)); zz.append(([(0, band_y1), (W, band_y1)], 3, None))
    knots = circles(W, H, [(x, (band_y0 + band_y1) / 2, 6) for x in np.arange(25, W, 50)])
    band_rib = np.maximum(strokes(W, H, zz), knots)
    bandm = ((yy >= band_y0 - 2) & (yy <= band_y1 + 2)).astype(np.float32)
    # sebka spandrel relief below band
    rib, leaves = sebka(W, H, 54, 390, band_y1 + 40, 3.0)
    spand = ((yy > band_y1 + 4)).astype(np.float32)
    # arch borders: a raised archivolt following each opening, plus a dentil ring
    arch_edge = np.zeros((H, W), np.float32)
    for o in ops:
        dil = (gaussian_filter(o, 7) > 0.05).astype(np.float32)
        dil2 = (gaussian_filter(o, 12) > 0.05).astype(np.float32)
        arch_edge = np.maximum(arch_edge, np.clip(dil - o, 0, 1) * 1.0 + np.clip(dil2 - dil, 0, 1) * 0.35)
    near_arch = (gaussian_filter(opening, 14) > 0.04).astype(np.float32)
    hgt = np.where(top, hgt, hgt)
    relief = np.maximum.reduce([fillet, bead, band_rib * bandm, (rib * 0.85 + leaves * 0.75) * spand * (1 - near_arch)])
    below = yy >= mq_h
    hgt[below] = 0.35 + relief[below] * 0.6
    hgt = np.maximum(hgt, arch_edge * 0.95 * (yy > band_y1))
    # colonnettes (marble) between arches & at the outer edges; capitals
    cols_x = [215, 565, 24, 756]
    col_m = np.zeros((H, W), np.float32); cap_m = np.zeros((H, W), np.float32)
    for x in cols_x:
        col_m = np.maximum(col_m, shapes(W, H, [[(x - 7, 430), (x + 7, 430), (x + 8, H + 4), (x - 8, H + 4)]], smooth=False))
        cap_m = np.maximum(cap_m, shapes(W, H, [[(x - 22, 398), (x + 22, 398), (x + 22, 412), (x + 14, 430), (x - 14, 430), (x - 22, 412)]], smooth=False))
        cap_m = np.maximum(cap_m, shapes(W, H, [[(x - 13, 462), (x + 13, 462), (x + 13, 470), (x - 13, 470)]], smooth=False))
    mask = np.clip(wall - opening, 0, 1)
    mask = np.maximum(mask, np.maximum(col_m, cap_m))
    art = stucco(hgt, mask, PLASTER, seed=5, depth=3.0, ao=0.7, dirt=DIRT)
    # warm wash: aged polychromy traces in recesses (faded blue/red as in the Alhambra)
    rec = np.clip(0.5 - hgt, 0, 1) * 2 * spand * (1 - near_arch)
    trace = noise(W, H, 12, 30)
    art[..., :3] = art[..., :3] * (1 - (rec * (trace > 0.55) * 0.25)[..., None]) + (rec * (trace > 0.55) * 0.25)[..., None] * np.array(hex_rgb("#4a6aa0"), np.float32)
    band_rec = np.clip(0.5 - hgt, 0, 1) * 2 * bandm
    art[..., :3] = art[..., :3] * (1 - (band_rec * 0.35)[..., None]) + (band_rec * 0.35)[..., None] * np.array(hex_rgb("#9a4a2e"), np.float32)
    # marble colonnettes
    col_art = GP(blank(W, H), col_m, "#f1ece2", "#dcd3c3", seed=21, rough=0.4, streak=0.15)
    shade_c = np.zeros((H, W), np.float32)
    for x in cols_x:
        shade_c = np.maximum(shade_c, (np.clip((xx - x) / 8, 0, 1) ** 1.5 * 0.9 + np.clip((x - xx) / 8, 0, 1) ** 2 * 0.3) * col_m)
    col_art = G(col_art, shade_c * col_m, "#8e8574", seed=22, density=0.45, edge=0.1, bloom=0, rough=0.6)
    art = over(art, col_art)
    cap_h = np.clip(gaussian_filter(cap_m, 1.2), 0, 1) * (0.6 + 0.4 * noise(W, H, 31, 2))
    art = over(art, stucco(cap_h, cap_m, "#e9dfcc", seed=33, depth=3.0, ao=0.4, dirt=DIRT))
    # depth: soft shadow cast inside the openings
    rim = np.clip(gaussian_filter(1 - opening, 8) * opening * 1.3, 0, 0.5)
    art = over(rgba(flat(H, W, "#2a160c"), rim), art)
    preview(art, "an-arcade", bg="#6d4a34")
    save_full(art, f"{OUT}/arcade.webp", size=(640, 623), quality=80)

if "muqarnas" in PARTS:
    clear()
    W, H = 900, 150
    hgt = muqarnas_height(W, H, 16, 3, 60, 42, -8, 8)
    hgt[:8] = 0.95
    yy = np.mgrid[0:H, 0:W][0]
    edge = np.ones((H, W), np.float32)
    # stalactite fringe bottom: scalloped pendants
    pend = circles(W, H, [(x, 134, 13) for x in np.arange(22, W, 60)])
    body = (yy < 134).astype(np.float32)
    mask = np.maximum(body, pend)
    hgt = np.where(yy >= 134, 0.7 * pend, hgt)
    art = stucco(hgt, gaussian_filter(mask, 0.6), PLASTER, seed=41, depth=3.0, ao=0.8, dirt=DIRT)
    rec = np.clip(0.6 - hgt, 0, 1) * 1.6
    art[..., :3] = art[..., :3] * (1 - (rec * 0.18)[..., None]) + (rec * 0.18)[..., None] * np.array(hex_rgb("#3c5a96"), np.float32)
    preview(art, "an-muqarnas", bg="#6d4a34")
    save(art, f"{OUT}/muqarnas.webp", max_w=640, quality=80)

if "tile" in PARTS:
    clear()
    # cuerda seca tile (square, tiles seamlessly as a grid): 8-point star with interlaced strapwork,
    # quarter-stars at the corners; dark manganese cord lines, pooled coloured glazes, tin-white ground.
    S = 320
    rng = random.Random(51)
    c = S / 2
    polys = []
    polys.append(wob_poly(star_pts(c, c, 112, 112 * 0.7654, 8, math.pi / 8), rng, 0.8))
    polys.append(wob_poly(star_pts(c, c, 66, 66 * 0.7654, 8, 0), rng, 0.7))
    polys.append(wob_poly([(c + math.cos(a) * 26, c + math.sin(a) * 26) for a in [k * math.pi / 4 for k in range(8)]], rng, 0.4))
    for (qx, qy) in [(0, 0), (S, 0), (0, S), (S, S)]:
        polys.append(wob_poly(star_pts(qx, qy, 70, 70 * 0.7654, 8, math.pi / 8), rng, 0.7))
        polys.append(wob_poly(star_pts(qx, qy, 36, 36 * 0.7654, 8, 0), rng, 0.5))
    # strapwork connecting star points to the tile edges' midpoints
    straps = []
    for k in range(8):
        a = math.pi / 8 + k * math.pi / 4
        straps.append([(c + math.cos(a) * 112, c + math.sin(a) * 112), (c + math.cos(a) * 260, c + math.sin(a) * 260)])
    for (mx, my) in [(c, 0), (c, S), (0, c), (S, c)]:
        straps.append([(mx - 40 if my in (0, S) else mx, my if my in (0, S) else my - 40), (mx + 40 if my in (0, S) else mx, my if my in (0, S) else my + 40)])
    border = [[(1, 1), (S - 1, 1), (S - 1, S - 1), (1, S - 1)]]
    cord = np.maximum.reduce([poly_lines(S, S, polys, 5.2), poly_lines(S, S, straps, 5.2, closed=False), poly_lines(S, S, border, 4)])
    lab, n = label_regions(cord)

    def col(i, x, y, r):
        dc = math.hypot(x - c, y - c)
        dq = min(math.hypot(x - qx, y - qy) for qx, qy in [(0, 0), (S, 0), (0, S), (S, S)])
        if dc < 20: return HONEY
        if dc < 50: return TERRA
        if dc < 92: return COBALT
        if dq < 26: return HONEY
        if dq < 56: return GREEN
        return TERRA if math.cos(4 * math.atan2(y - c, x - c)) > 0 else TIN
    art = tile_glaze(lab, n, col, seed=53, bevel=4.5, chip=0.25, grout_col=MANG, body="#9b5a3a", rim=0.06, mottle=0.18, tilt=0.03, gloss=0.8)
    # cord is raised & glossy (manganese with a sheen)
    hc = gaussian_filter(cord, 1.0)
    gy, gx = np.gradient(hc)
    sheen = np.clip(-(gx + gy) * 3, 0, 1)
    art[..., :3] = art[..., :3] + (sheen * cord * 0.25)[..., None]
    # pooled glaze: thicker (darker, more saturated) next to the cord
    near = np.clip(gaussian_filter(cord, 3) * 1.6, 0, 1) * (1 - cord)
    art[..., :3] = art[..., :3] * (1 - near[..., None] * 0.22)
    preview(art, "an-tile")
    save_full(art, f"{OUT}/tile.webp", size=(160, 160), quality=82)

if "rosette" in PARTS:
    clear()
    # carved stucco lobed medallion (12 lobes) with central 6-petal rosette — for timeline nodes, amp, sent state
    W = H = 300; c = W / 2
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lob = circles(W, H, [(c + math.cos(a) * 104, c + math.sin(a) * 104, 34) for a in [k * math.tau / 12 for k in range(12)]] + [(c, c, 112)])
    ring = np.clip(circles(W, H, [(c, c, 92)]) - circles(W, H, [(c, c, 84)]), 0, 1)
    pet = shapes(W, H, [petal_pts(c, c, 70, 26, k * math.tau / 6, n=12) for k in range(6)])
    pet2 = shapes(W, H, [petal_pts(c, c, 52, 12, k * math.tau / 6 + math.pi / 6, n=10) for k in range(6)])
    beads = circles(W, H, [(c + math.cos(a) * 118, c + math.sin(a) * 118, 6) for a in [k * math.tau / 12 + math.tau / 24 for k in range(12)]])
    hgt = 0.35 + 0.45 * ring + 0.55 * pet - 0.25 * pet2 + 0.3 * circles(W, H, [(c, c, 14)])
    edge_l = np.clip((gaussian_filter(lob, 4) > 0.5).astype(np.float32) - (gaussian_filter(lob, 4) > 0.85), 0, 1)
    hgt = np.clip(hgt + edge_l * 0.4, 0, 1)
    mask = np.maximum(gaussian_filter(lob, 0.7), beads)
    art = stucco(hgt, mask, PLASTER, seed=61, depth=3.4, ao=0.7, dirt=DIRT)
    rec = np.clip(0.42 - hgt, 0, 1) * 3
    art[..., :3] = art[..., :3] * (1 - (rec * 0.35)[..., None]) + (rec * 0.35)[..., None] * np.array(hex_rgb("#2f4f92"), np.float32)
    preview(art, "an-rosette", bg="#6d4a34")
    save(art, f"{OUT}/rosette.webp", max_w=180, quality=82)

report(OUT)
