"""Lampung Tapis — deep red/black with couched gold: 9-spike siger Lampung (Pepadun) in pressed gold with engraved
lines and red stones, tapis band tile (thread-level couched gold on striped red/black cloth, small mirror sequins),
kain kapal (palepai-inspired ship cloth) rendered as supplementary-weft weaving, couched-gold divider.
Run: python3 -I lampung-tapis.py [part ...]  parts: siger tapis kapal divider. Assets -> public/themes/art/lampung-tapis/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a1_lib import *

OUT = outdir("lampung-tapis")
PARTS = sys.argv[1:] or ["siger", "tapis", "kapal", "divider"]
RED, RED_D, BLK = "#7e1620", "#4a0b12", "#1a0d0c"
GOLD, GOLD_L = "#d1a648", "#f0d38a"
CREAM, OCHRE, INDIGO, RUST = "#efe2c4", "#c7922f", "#1f2433", "#9b3a22"


def spike_poly(bx, by, h, wbase, tilt):
    """Tall siger spike: concave sides rising to a point, tilted outward."""
    tx, ty = bx + math.sin(tilt) * h, by - math.cos(tilt) * h
    pts = []
    for k in range(12):
        t = k / 11
        x = bx - wbase / 2 * (1 - t) ** 0.85 * (1 + 0.25 * math.sin(t * math.pi)) + (tx - bx) * t
        y = by + (ty - by) * t
        pts.append((x - 1.5 * math.sin(t * math.pi), y))
    for k in range(12):
        t = 1 - k / 11
        x = bx + wbase / 2 * (1 - t) ** 0.85 * (1 + 0.25 * math.sin(t * math.pi)) + (tx - bx) * t
        y = by + (ty - by) * t
        pts.append((x + 1.5 * math.sin(t * math.pi), y))
    return pts, (tx, ty)


if "siger" in PARTS:
    W, H = 720, 470
    nx = Seq(40100); rng = random.Random(2)
    cx = W / 2
    # body: boat-like curved band, ends sweeping up
    top = [(cx + u, 300 - 70 * (abs(u) / 300) ** 2.2) for u in range(-300, 301, 20)]
    bot = [(cx + u, 372 - 92 * (abs(u) / 300) ** 2.0) for u in range(300, -301, -20)]
    body = shapes(W, H, [top + bot])
    spikes, tips = [], []
    for i in range(-4, 5):
        u = i * 64
        by = 300 - 70 * (abs(u) / 300) ** 2.2 + 8
        h = 240 - abs(i) * 34 - (8 if abs(i) == 4 else 0)
        pts, tip = spike_poly(cx + u, by, h, 74 - abs(i) * 4, i * 0.12)
        spikes.append(pts); tips.append((tip, 14 - abs(i)))
    sp = shapes(W, H, spikes)
    tip_m = np.zeros((H, W), np.float32)
    tip_items = []
    for (tx, ty), r in tips:
        for k in range(5):
            a = -math.pi / 2 + k * math.tau / 5
            tip_items.append(petal_pts(tx, ty, r * 1.3, r * 0.45, a, n=10))
    tip_m = np.maximum(shapes(W, H, tip_items), circles(W, H, [(t[0][0], t[0][1], t[1] * 0.45) for t in tips]))
    crown = np.clip(np.maximum.reduce([body, sp, tip_m]), 0, 1)
    shadow = soft_shadow(crown, "#000000", 9, 0.55, 3, 8)
    art = over(blank(W, H), shadow)
    art = FO(art, crown, GOLD, seed=nx(), emboss=0.85, sparkle=0.18)
    # engraved detail: spike mid-ribs, body scroll band, beaded rims
    ribs = []
    for pts in spikes:
        n = len(pts) // 2
        base = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
        tip = pts[n - 1]
        ribs.append([base, (base[0] + (tip[0] - base[0]) * 0.82, base[1] + (tip[1] - base[1]) * 0.82)])
    rib = polyline_mask(W, H, ribs, 2.2)
    inlays = []
    for i in range(-4, 5):
        u = i * 64
        by = 300 - 70 * (abs(u) / 300) ** 2.2 + 4
        h = (240 - abs(i) * 34) * 0.42
        p_, _ = spike_poly(cx + u + math.sin(i * 0.12) * 18, by - 18, h, 26 - abs(i), i * 0.12)
        inlays.append(p_)
    inl = shapes(W, H, inlays)
    art = GP(art, inl, "#9e1424", "#5e0a14", seed=nx(), rough=0.6, pad=6)
    art = FO(art, outline(inl, 2.4), GOLD_L, seed=nx(), emboss=0.6)
    inner_sp = np.clip(gaussian_filter(sp, 3.5) > 0.75, 0, 1).astype(np.float32)
    sp_edge = np.clip(sp - inner_sp, 0, 1) * (1 - body)
    art = over(art, flat(np.maximum(rib, sp_edge * 0.8) * (1 - body), "#6b4a14", 0.75))
    band_l = polyline_mask(W, H, [[(cx + u, 312 - 70 * (abs(u) / 300) ** 2.2) for u in range(-286, 287, 13)], [(cx + u, 358 - 90 * (abs(u) / 300) ** 2.0) for u in range(-286, 287, 13)]], 2.4)
    art = over(art, flat(band_l, "#6b4a14", 0.8))
    # scrolls between the band lines
    sc = []
    for k, u in enumerate(range(-250, 251, 40)):
        y = 335 - 80 * (abs(u) / 300) ** 2.1
        sc.append(spiral_pts(cx + u, y, 9, 2, 0 if k % 2 else math.pi, 0.9, 20, 1 if k % 2 else -1))
    art = over(art, flat(polyline_mask(W, H, sc, 2.0), "#6b4a14", 0.7))
    # beads under the body
    beads = circles(W, H, [(cx + u, 380 - 92 * (abs(u) / 300) ** 2.0, 4.2) for u in range(-280, 281, 16)])
    art = FO(art, beads, GOLD_L, seed=nx(), emboss=0.9)
    # red stones in the band + at spike bases
    stones = ellipses(W, H, [(cx + u, 336 - 81 * (abs(u) / 300) ** 2.1, 8, 6, 0) for u in range(-192, 193, 64)])
    art = GP(art, stones, "#b3192a", "#5e0a14", seed=nx(), rough=0.5, pad=6)
    hi = ellipses(W, H, [(cx + u - 2, 333 - 81 * (abs(u) / 300) ** 2.1, 2.5, 1.6, 0) for u in range(-192, 193, 64)])
    art = over(art, flat(hi, "#ffd9d0", 0.8))
    preview(art, "lt-siger", bg=RED)
    save(art, f"{OUT}/siger.webp", max_w=440, quality=84)
    clear()

if "tapis" in PARTS:
    # band tile, repeat-x: woven striped ground + couched gold rows + motif row (diamond hooks) + sequins
    W, H = 360, 200
    nx = Seq(40200)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    cloth = cloth_base(W, H, RED, seed=nx(), cell=2.0, var=0.08)
    blk = ((yy < 18) | (yy > H - 18) | ((yy > 46) & (yy < 54)) | ((yy > H - 54) & (yy < H - 46))).astype(np.float32)
    cloth[..., :3] = cloth[..., :3] * (1 - blk[..., None]) + (cloth[..., :3] * col_arr(BLK) / col_arr(RED).max() * 0.9) * blk[..., None]
    thin = (((yy > 20) & (yy < 23)) | ((yy > H - 23) & (yy < H - 20))).astype(np.float32)
    cloth[..., :3] = cloth[..., :3] * (1 - thin[..., None]) + col_arr(OCHRE) * thin[..., None] * 0.9
    art = cloth
    # straight couched rows
    rows = np.zeros((H, W), np.float32)
    for y0, y1 in [(28, 40), (H - 40, H - 28)]:
        rows[y0:y1] = 1
    art = over(art, couched(rows, GOLD, seed=nx(), angle=0.0, pitch=2.0, stitch=8))
    # motif row: diamonds with hooked ends (centre band y 60..140), period 90px -> 4 per tile
    P = 90; cy = H / 2
    diag_a, diag_b = [], []
    for k in range(-1, W // P + 2):
        x0 = k * P + P / 2
        # outer diamond as 4 thick segments
        L = [(x0 - 34, cy), (x0, cy - 34), (x0 + 34, cy), (x0, cy + 34)]
        diag_a += [[L[0], L[1]], [L[2], L[3]]]
        diag_b += [[L[1], L[2]], [L[3], L[0]]]
        # inner hooks
        diag_a += [[(x0 - 14, cy + 4), (x0 + 2, cy - 12)]]
        diag_b += [[(x0 + 14, cy - 4), (x0 - 2, cy + 12)]]
    ma = polyline_mask(W, H, diag_a, 9, cap=False)
    mb = polyline_mask(W, H, diag_b, 9, cap=False)
    # connecting zigzag between diamonds (small chevrons)
    za, zb = [], []
    for k in range(-1, W // P + 2):
        x = k * P
        za += [[(x - 8, cy - 18), (x + 8, cy - 2)], [(x - 8, cy + 2), (x + 8, cy + 18)]]
        zb += [[(x + 8, cy - 18), (x - 8, cy - 2)], [(x + 8, cy + 2), (x - 8, cy + 18)]]
    ma = np.maximum(ma, polyline_mask(W, H, za, 5, cap=False))
    mb = np.maximum(mb, polyline_mask(W, H, zb, 5, cap=False))
    art = over(art, couched(ma, GOLD, seed=nx(), angle=math.pi / 4, pitch=1.9, stitch=7))
    art = over(art, couched(np.clip(mb - ma, 0, 1), GOLD, seed=nx(), angle=-math.pi / 4, pitch=1.9, stitch=7))
    # silk-filled diamond centres (dark) + mirror sequins
    cen = shapes(W, H, [[(k * P + P / 2 - 8, cy), (k * P + P / 2, cy - 8), (k * P + P / 2 + 8, cy), (k * P + P / 2, cy + 8)] for k in range(-1, W // P + 2)], smooth=False)
    art = over(art, satin(cen, "#e9dcc0", seed=nx(), angle=0.3, pitch=1.4))
    seq = []
    for k in range(-1, W // P + 2):
        seq += [(k * P, cy - 32, 4.2), (k * P, cy + 32, 4.2)]
    sm = circles(W, H, seq)
    art = FO(art, sm, "#c9cdd2", seed=nx(), emboss=0.9, sparkle=0.4)
    art = over(art, flat(circles(W, H, [(x, y, 1.2) for x, y, _ in seq]), "#6b1a1a", 0.9))
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/tapis.webp", quality=80)
    clear()

if "kapal" in PARTS:
    # palepai-inspired ship cloth: long hull with curled prow/stern, tiered house on deck, two tree shrines,
    # rendered as supplementary-weft: shapes quantised to a weave grid, woven shading, slubby dyes.
    W, H = 840, 400
    nx = Seq(40300); rng = random.Random(5)
    G_ = 5  # weave cell

    def q(m):
        """quantise a mask to the weave grid (stepped edges like supplementary weft floats)."""
        small = m[G_ // 2::G_, ::2]
        rows = np.repeat(small > 0.45, G_, 0)[:H]
        full = np.repeat(rows, 2, 1)[:, :W]
        return full.astype(np.float32)

    cloth = cloth_base(W, H, CREAM, seed=nx(), cell=2.5, var=0.1)
    # border stripes
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    band = ((yy < 16) | (yy > H - 16)).astype(np.float32)
    cloth[..., :3] = cloth[..., :3] * (1 - band[..., None]) + cloth[..., :3] * col_arr(RUST) * band[..., None] * 1.1
    tri = []
    for x in range(0, W + 30, 30):
        tri += [[(x - 13, 16), (x + 13, 16), (x, 36)], [(x - 13, H - 16), (x + 13, H - 16), (x, H - 36)]]
    tm = q(shapes(W, H, tri, smooth=False))
    hull_top = [(110, 270), (300, 286), (540, 286), (730, 270)]
    hull = [(70, 236), (110, 270)] + curve(hull_top, 20)[1:-1] + [(730, 270), (770, 236), (720, 316), (130, 316)]
    hull_m = shapes(W, H, [hull], smooth=False)
    prow = polyline_mask(W, H, [spiral_pts(80, 210, 30, 6, math.pi * 0.5, 1.1, 40, 1), spiral_pts(760, 210, 30, 6, math.pi * 0.5, 1.1, 40, -1)], 11)
    deck_house = shapes(W, H, [[(330, 282), (330, 210), (510, 210), (510, 282)], [(306, 214), (420, 150), (534, 214)], [(360, 156), (420, 104), (480, 156)]], smooth=False)
    windows = shapes(W, H, [[(350 + k * 34, 268), (350 + k * 34, 230), (366 + k * 34, 230), (366 + k * 34, 268)] for k in range(5)], smooth=False)
    masts = polyline_mask(W, H, [[(210, 286), (210, 130)], [(630, 286), (630, 130)]], 6)
    trees = []
    for tx in (210, 630):
        for k, (dy, w) in enumerate([(0, 70), (34, 56), (66, 42), (94, 26)]):
            y = 150 + dy
            trees.append([(tx - w, y + 22), (tx, y - 10), (tx + w, y + 22)])
    tree_m = shapes(W, H, trees, smooth=False)
    flags = shapes(W, H, [[(212, 132), (262, 142), (212, 154)], [(632, 132), (682, 142), (632, 154)]], smooth=False)
    wv = []
    for row, y in enumerate((334, 356)):
        pts = [(x, y + (8 if (x // 24 + row) % 2 else -8)) for x in range(60, 790, 24)]
        wv.append(pts)
    oars = polyline_mask(W, H, wv, 6)
    loz = []
    for (x, y) in [(150, 90), (270, 76), (560, 76), (690, 90), (110, 150), (740, 150), (330, 60), (510, 60)]:
        loz += [[(x - 12, y), (x, y - 12), (x + 12, y), (x, y + 12)]]
    loz_q = q(shapes(W, H, loz, smooth=False))
    loz_c = q(circles(W, H, [(x, y, 4) for x, y in [(150, 90), (270, 76), (560, 76), (690, 90), (110, 150), (740, 150), (330, 60), (510, 60)]]))
    hull_q, prow_q, house_q, win_q = q(hull_m), q(prow), q(deck_house), q(windows)
    tree_q, mast_q, flag_q, oar_q = q(tree_m), q(masts), q(flags), q(oars)
    def dye(m, col, k=1.0):
        rgb = col_arr(col) * (0.9 + 0.2 * fbm(W, H, nx(), 18, 2))[..., None]
        return np.concatenate([rgb, (m * k)[..., None]], -1)
    art = cloth
    art = dye_on(art, dye(tm, RUST, 0.95))
    art = dye_on(art, dye(oar_q, INDIGO, 0.9))
    art = dye_on(art, dye(np.clip(loz_q - loz_c, 0, 1), RUST, 0.9))
    art = dye_on(art, dye(loz_c, INDIGO, 0.9))
    art = dye_on(art, dye(np.maximum(hull_q, prow_q), "#8f2a1e", 0.95))
    hull_band = q(shapes(W, H, [[(140, 292), (700, 292), (690, 302), (150, 302)]], smooth=False))
    art = dye_on(art, dye(hull_band, OCHRE, 0.95))
    art = dye_on(art, dye(np.maximum(tree_q, mast_q), INDIGO, 0.92))
    art = dye_on(art, dye(house_q, OCHRE, 0.95))
    art = dye_on(art, dye(win_q, INDIGO, 0.95))
    art = dye_on(art, dye(flag_q, "#8f2a1e", 0.95))
    # woven texture over everything + edge fringe
    art[..., :3] *= weave(W, H, None, None, nx(), 2.5)[..., None] * 0.6 + 0.45
    art = np.clip(art, 0, 1)
    fr = np.zeros((H + 24, W, 4), np.float32)
    fr[12:12 + H] = art
    fringe = np.zeros((H + 24, W), np.float32)
    for x in range(4, W, 7):
        fringe[0:12, x:x + 3] = 1; fringe[H + 12:, x:x + 3] = 1
    fringe = displace(fringe, 3, 1.5, 6)
    fr[..., :3] = np.where(fringe[..., None] > 0.3, col_arr("#e2d2b0"), fr[..., :3])
    fr[..., 3] = np.maximum(fr[..., 3], (fringe > 0.3).astype(np.float32))
    preview(fr, "lt-kapal", bg=RED)
    save(fr, f"{OUT}/kapal.webp", max_w=640, quality=74)
    clear()

if "divider" in PARTS:
    W, H = 640, 80
    nx = Seq(40400); cy = 40
    za, zb = [], []
    for k in range(0, 15):
        x = 40 + k * 40
        za.append([(x, cy + 12), (x + 20, cy - 12)]); zb.append([(x + 20, cy - 12), (x + 40, cy + 12)])
    ma = polyline_mask(W, H, za, 7, cap=False); mb = polyline_mask(W, H, zb, 7, cap=False)
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 3, 0, 1)[None, :]
    art = over(blank(W, H), couched(ma * fade, GOLD, seed=nx(), angle=-0.88, pitch=1.8, stitch=6))
    art = over(art, couched(np.clip(mb - ma, 0, 1) * fade, GOLD, seed=nx(), angle=0.88, pitch=1.8, stitch=6))
    dia = shapes(W, H, [[(320 - 20, cy), (320, cy - 22), (320 + 20, cy), (320, cy + 22)]], smooth=False)
    art = over(art, satin(dia, "#7e1620", seed=nx(), angle=0.2))
    art = FO(art, circles(W, H, [(320, cy, 5.5)]), "#c9cdd2", seed=nx(), emboss=0.9, sparkle=0.4)
    preview(art, "lt-divider", bg=BLK)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
