"""Samarkand Biru — Timurid architecture: an iwan portal (pishtaq) faced with glazed-brick geometry whose pointed arch
is an opening for the photo, ribbed turquoise melon domes on tiled drums, star-and-cross glazed tile field, small
star tiles. Glaze variation, crackle, pinholes. No figures, no drawn calligraphy.
Run: python3 -I samarkand-biru.py [part ...]  parts: girih iwan domes star divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b2_lib import *

OUT = outdir("samarkand-biru")
PARTS = sys.argv[1:] or ["girih", "iwan", "domes", "star", "divider"]
TQ, TQ_L, TQ_D = "#2b9fa3", "#58c4bd", "#1d7377"
CB, CB_L = "#1f4a9e", "#2f66bf"
WH = "#eee8d8"
LAP = "#182a6a"
BRICK, BRICK_D, BRICK_L = "#c49a62", "#9a7044", "#d9b783"
YEL = "#ddb04a"
GRN = "#3f8a5a"


def star_cross(W, H, step, ox=0, oy=0, r_frac=0.5):
    """Star-and-cross: 8-point stars at lattice points, crosses at cell centres. Returns (stars, crosses, centres)."""
    st, cr, cs = [], [], []
    R = step * r_frac
    for i in range(-int(ox // step) - 2, int((W - ox) // step) + 3):
        for j in range(-int(oy // step) - 2, int((H - oy) // step) + 3):
            cx, cy = ox + i * step, oy + j * step
            st.append(star_pts(cx, cy, R, 8, 0.72, math.pi / 8))
            cs.append((cx, cy))
            mx, my = cx + step / 2, cy + step / 2
            a = step * 0.5 - R * 0.66
            b = R * 0.27
            cr.append([(mx - b, my - a), (mx + b, my - a), (mx + b, my - b), (mx + a, my - b), (mx + a, my + b), (mx + b, my + b),
                       (mx + b, my + a), (mx - b, my + a), (mx - b, my + b), (mx - a, my + b), (mx - a, my - b), (mx - b, my - b)])
    return shapes(W, H, st, smooth=False), shapes(W, H, cr, smooth=False), cs


def tile_field(art, W, H, area, step, nx, ox=0, oy=0, star_col=CB, cross_col=TQ, ground=WH, inner=True):
    """Paint a glazed star-and-cross field inside `area` (mask)."""
    stars, crosses, cs = star_cross(W, H, step, ox, oy)
    grout = area.copy()
    art = over(art, flat(grout, "#b9a58a", 1.0))
    gnd = np.clip(area - gaussian_filter(np.maximum(stars, crosses), 0.8) * 1.6, 0, 1)
    gnd = np.clip(gnd - outline(np.maximum(stars, crosses), 1.4), 0, 1)
    art = over(art, glaze_tile(gnd * area, ground, "#e2dbc6", seed=nx(), crackle=0.35))
    art = over(art, glaze_tile(stars * area, star_col, CB_L if star_col == CB else star_col, seed=nx(), crackle=0.3))
    art = over(art, glaze_tile(crosses * area, cross_col, TQ_L if cross_col == TQ else cross_col, seed=nx(), crackle=0.3))
    if inner:
        small = shapes(W, H, [star_pts(x, y, step * 0.17, 8, 0.6, math.pi / 8) for x, y in cs], smooth=False)
        art = over(art, glaze_tile(small * area, YEL, "#e8c46a", seed=nx(), crackle=0.2))
    return art


if "girih" in PARTS:
    W, H = 240 + 120, 240 + 120
    nx = Seq(73100)
    art = solid_rgba(W, H, "#b9a58a")
    art = tile_field(art, W, H, np.ones((H, W), np.float32), 120, nx)
    art = np.ascontiguousarray(art[60:300, 60:300])
    art[..., 3] = 1
    preview(art, "sb-girih", bg=LAP)
    save_rgb(art, f"{OUT}/girih.webp", quality=80)
    clear()


def banna(art, W, H, area, nx, unit=10, seed=0):
    """Banna'i glazed-brick geometry: brick ground with glazed bricks set in a stepped-diamond (no lettering)."""
    bm, tone = brick_field(W, H, unit * 2, unit, 1.4, nx())
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    row = np.floor(yy / unit); colm = np.floor((xx + (row % 2) * unit) / (unit * 2))
    d = (np.abs(((colm * 2 + row % 2) % 8) - 4) + np.abs((row % 8) - 4))
    glazed = ((d == 4) | (d == 0)).astype(np.float32)
    ca, cb = col_arr(BRICK_L), col_arr(BRICK_D)
    rgb = ca * (1 - tone[..., None]) + cb * tone[..., None]
    g1 = col_arr(TQ) * (0.85 + 0.3 * tone[..., None])
    g2 = col_arr(CB) * (0.85 + 0.3 * tone[..., None])
    rgb = np.where((glazed * (d == 4))[..., None] > 0, g1, np.where((glazed * (d == 0))[..., None] > 0, g2, rgb))
    rgb = rgb * bm[..., None] + col_arr("#a89070") * (1 - bm[..., None])
    rgb *= (0.92 + 0.14 * fbm(W, H, nx(), 6, 2))[..., None]
    return over(art, np.concatenate([np.clip(rgb, 0, 1), area[..., None]], -1))


def arch_pts(cx, x0, x1, spring, apex, bottom, n=24):
    """Pointed (four-centred-ish) arch outline from bottom-left up and around to bottom-right."""
    hw = (x1 - x0) / 2
    pts = [(x0, bottom), (x0, spring)]
    for k in range(1, n + 1):
        t = k / n
        a = t * math.pi / 2
        x = x0 + hw * (1 - math.cos(a)) ** 1.0
        y = spring - (spring - apex) * math.sin(a) ** 1.35
        pts.append((x, y))
    right = [(2 * cx - x, y) for x, y in reversed(pts[2:-1])]
    return pts + [(cx, apex)] + right + [(x1, spring), (x1, bottom)]


def melon_dome(art, W, H, cx, base, rx, h, nx, ribs=16, col=TQ, col_d=TQ_D, col_l=TQ_L, drum_h=None):
    """Ribbed Timurid melon dome on a tiled drum, gold finial."""
    drum_h = drum_h if drum_h is not None else h * 0.45
    dt = base - drum_h
    drum = rect(W, H, cx - rx * 0.86, dt, cx + rx * 0.86, base)
    art = banna(art, W, H, drum, nx, unit=max(5, int(rx * 0.09)))
    band = rect(W, H, cx - rx * 0.86, dt + drum_h * 0.18, cx + rx * 0.86, dt + drum_h * 0.46)
    art = over(art, glaze_tile(band, CB, CB_L, seed=nx(), crackle=0.2))
    stars = shapes(W, H, [star_pts(x, dt + drum_h * 0.32, drum_h * 0.1, 8, 0.6, math.pi / 8) for x in np.arange(cx - rx * 0.8, cx + rx * 0.8, drum_h * 0.3)], smooth=False)
    art = over(art, glaze_tile(stars * band, WH, seed=nx(), crackle=0.1))
    art = over(art, flat(rect(W, H, cx - rx * 0.9, dt - 4, cx + rx * 0.9, dt + 3), "#e8dcc0", 0.9))
    # bulb profile: neck at the drum, swelling to 1.0 at ~35%, then pointed top
    prof = []
    for t in np.linspace(0, 1, 40):
        y = dt - t * h
        if t < 0.3:
            k = 0.86 + 0.14 * math.sin(t / 0.3 * math.pi / 2)
        else:
            u = (t - 0.3) / 0.7
            k = math.cos(u * math.pi / 2) ** 0.85
        prof.append((k * rx, y))
    outline_pts = [(cx - k, y) for k, y in prof] + [(cx + k, y) for k, y in reversed(prof)]
    dome = shapes(W, H, [outline_pts])
    art = over(art, glaze_tile(dome, col, col_l, seed=nx(), crackle=0.25, gloss=0.8))
    # ribs: meridians; shade each gore by its facing angle (light from upper left)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ys = np.array([p[1] for p in prof])[::-1]; ks = np.array([p[0] for p in prof])[::-1]
    rad = np.interp(yy, ys, ks)
    sx = np.clip((xx - cx) / np.maximum(rad, 1), -1, 1)
    theta = np.arcsin(sx)
    g = (theta / math.pi * ribs + 0.5) % 1.0
    gore_shade = np.sin(g * math.pi)
    face = np.cos(theta + 0.6)
    lum = 0.7 + 0.25 * face + 0.12 * gore_shade
    dark = col_arr(col_d)
    tint = np.clip(1 - lum, 0, 1)
    art[..., :3] = np.where(dome[..., None] > 0.5, art[..., :3] * (0.75 + 0.35 * lum[..., None]) * (1 - tint[..., None] * 0.2) + dark * tint[..., None] * 0.2, art[..., :3])
    seam = np.clip(1 - np.abs(g - 0.0) * 14, 0, 1) + np.clip(1 - np.abs(g - 1.0) * 14, 0, 1)
    art = over(art, flat(seam * dome * (np.abs(sx) < 0.97), col_d, 0.55))
    hl = dome * light_mask(H, W, cx - rx * 0.35, dt - h * 0.45, rx * 0.5)
    art = over(art, flat(hl, "#d8f4ee", 0.35))
    fin = polyline_mask(W, H, [[(cx, dt - h + 2), (cx, dt - h - h * 0.22)]], max(2.0, rx * 0.04))
    art = FO(art, np.maximum(fin, circles(W, H, [(cx, dt - h - h * 0.08, max(3, rx * 0.06))])), YEL, seed=nx())
    return art


if "iwan" in PARTS:
    W, H = 600, 800
    nx = Seq(73200); cx = W / 2
    art = blank(W, H)
    # dome behind the portal
    art = melon_dome(art, W, H, cx, 150, 104, 96, nx, ribs=18, drum_h=30)
    # guldasta corner minarets
    for x in (52, W - 52):
        sh = rect(W, H, x - 26, 64, x + 26, H)
        art = banna(art, W, H, sh, nx, unit=9)
        for y0 in (120, 360, 600):
            b = rect(W, H, x - 26, y0, x + 26, y0 + 30)
            art = over(art, glaze_tile(b, CB, CB_L, seed=nx(), crackle=0.2))
            art = over(art, glaze_tile(shapes(W, H, [star_pts(x, y0 + 15, 10, 8, 0.6, math.pi / 8)], smooth=False), WH, seed=nx()))
        cap = shapes(W, H, [[(x - 30, 66), (x - 28, 50), (x - 16, 34), (x, 22), (x + 16, 34), (x + 28, 50), (x + 30, 66)]])
        art = over(art, glaze_tile(cap, TQ, TQ_L, seed=nx(), crackle=0.2, gloss=0.8))
        art = over(art, flat(rect(W, H, x - 32, 64, x + 32, 72), "#e8dcc0", 0.95))
    # portal face
    face = rect(W, H, 78, 140, W - 78, H)
    art = banna(art, W, H, face, nx, unit=10)
    # outer border band of star-and-cross
    inner_face = rect(W, H, 112, 174, W - 112, H)
    border = np.clip(face - inner_face, 0, 1)
    art = tile_field(art, W, H, border, 34, nx, ox=95, oy=157, inner=False)
    # cornice
    cor = rect(W, H, 70, 128, W - 70, 146)
    art = over(art, glaze_tile(cor, TQ_D, TQ, seed=nx(), crackle=0.2))
    mer = shapes(W, H, [[(x, 128), (x + 8, 116), (x + 16, 128)] for x in range(74, W - 80, 18)], smooth=False)
    art = over(art, glaze_tile(mer, TQ, TQ_L, seed=nx()))
    # top panel: cobalt with white star row (geometric, no lettering)
    panel = rect(W, H, 112, 174, W - 112, 236)
    art = over(art, glaze_tile(panel, CB, CB_L, seed=nx(), crackle=0.3))
    ps = shapes(W, H, [star_pts(x, 205, 15, 8, 0.6, math.pi / 8) for x in np.arange(140, W - 120, 40)], smooth=False)
    art = over(art, glaze_tile(ps, WH, seed=nx(), crackle=0.1))
    art = over(art, glaze_tile(circles(W, H, [(x, 205, 4) for x in np.arange(140, W - 120, 40)]), TQ, seed=nx()))
    art = over(art, glaze_tile(np.clip(rect(W, H, 112, 236, W - 112, 244), 0, 1), YEL, seed=nx()))
    # arch opening + rope band + spandrels
    outer_arch = shape_mask(W, H, arch_pts(cx, 136, W - 136, 430, 262, H + 10), smooth=False)
    hole = shape_mask(W, H, arch_pts(cx, 166, W - 166, 446, 296, H + 10), smooth=False)
    spand = np.clip(rect(W, H, 112, 244, W - 112, H) - outer_arch, 0, 1)
    art = tile_field(art, W, H, spand, 44, nx, ox=cx, oy=268)
    band = np.clip(outer_arch - hole, 0, 1)
    art = over(art, glaze_tile(band, TQ, TQ_L, seed=nx(), crackle=0.3, gloss=0.7))
    # twisted rope: diagonal ticks along the band
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    tw = (np.sin((xx + yy) * 0.45) > 0.55).astype(np.float32)
    art = over(art, flat(gaussian_filter(tw, 0.6) * band, TQ_D, 0.55))
    art = over(art, flat(outline(outer_arch, 2.0), "#e8dcc0", 0.9))
    # depth: shadow just inside the hole edge (painted on band inner side)
    rim = np.clip(gaussian_filter(hole, 6) - hole * 0.0, 0, 1) * (1 - hole) * band
    art = over(art, flat(rim, "#0b1030", 0.4))
    art[..., 3] *= (1 - hole)
    preview(art, "sb-iwan", bg=LAP)
    save_full(art, f"{OUT}/iwan.webp", quality=80)
    clear()

if "domes" in PARTS:
    W, H = 840, 400
    nx = Seq(73300)
    art = blank(W, H)
    # minarets
    for x, top in ((96, 60), (W - 96, 60)):
        sh = poly(W, H, [(x - 22, H), (x - 16, top + 40), (x + 16, top + 40), (x + 22, H)])
        art = banna(art, W, H, sh, nx, unit=8)
        for y0 in (top + 90, top + 180):
            art = over(art, glaze_tile(rect(W, H, x - 21, y0, x + 21, y0 + 16), CB, CB_L, seed=nx()))
        gal = rect(W, H, x - 28, top + 30, x + 28, top + 44)
        art = over(art, glaze_tile(gal, TQ_D, TQ, seed=nx()))
        cap = shapes(W, H, [[(x - 16, top + 32), (x - 12, top + 14), (x, top), (x + 12, top + 14), (x + 16, top + 32)]])
        art = over(art, glaze_tile(cap, TQ, TQ_L, seed=nx(), gloss=0.8))
    # side domes then central dome
    art = melon_dome(art, W, H, 236, 330, 82, 112, nx, ribs=14, drum_h=50)
    art = melon_dome(art, W, H, W - 236, 330, 82, 112, nx, ribs=14, drum_h=50)
    art = melon_dome(art, W, H, W / 2, 316, 150, 196, nx, ribs=20, drum_h=78)
    # arcade base wall with small pointed niches
    wall = rect(W, H, 130, 316, W - 130, H)
    art = banna(art, W, H, wall, nx, unit=9)
    niches = shapes(W, H, [arch_pts(x, x - 22, x + 22, 362, 334, 400, 12) for x in np.arange(170, W - 150, 62)], smooth=False)
    art = over(art, glaze_tile(niches, LAP, CB, seed=nx(), crackle=0.1))
    art = over(art, flat(outline(niches, 2.0), TQ_L, 0.9))
    art = over(art, glaze_tile(rect(W, H, 130, 316, W - 130, 326), TQ, TQ_L, seed=nx()))
    preview(art, "sb-domes", bg=LAP)
    save(art, f"{OUT}/domes.webp", max_w=780, quality=80)
    clear()

if "star" in PARTS:
    W, H = 240, 240
    nx = Seq(73400); c = 120
    outer = shapes(W, H, [star_pts(c, c, 112, 8, 0.72, math.pi / 8)], smooth=False)
    art = glaze_tile(outer, CB, CB_L, seed=nx(), crackle=0.35)
    mid = shapes(W, H, [star_pts(c, c, 82, 8, 0.66, math.pi / 8)], smooth=False)
    art = over(art, flat(outline(mid, 3), "#e8dcc0", 1))
    art = over(art, glaze_tile(mid, TQ, TQ_L, seed=nx(), crackle=0.3))
    fl = shapes(W, H, [petal_pts(c, c, 52, 18, k * math.pi / 4, n=10) for k in range(8)])
    art = over(art, glaze_tile(fl, WH, seed=nx(), crackle=0.2))
    art = over(art, glaze_tile(circles(W, H, [(c, c, 14)]), YEL, seed=nx()))
    preview(art, "sb-star", bg=WH)
    save(art, f"{OUT}/star.webp", max_w=160, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 600, 60
    nx = Seq(73500); cy = 30
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 2.5, 0, 1)[None, :]
    chips = []
    for x in list(range(40, 262, 16)) + list(range(346, 568, 16)):
        chips.append([(x, cy - 5), (x + 6, cy), (x, cy + 5), (x - 6, cy)])
    cm = shapes(W, H, chips, smooth=False) * fade
    art = glaze_tile(cm, TQ, TQ_L, seed=nx(), crackle=0.1)
    ln = rect(W, H, 30, cy - 1, 270, cy + 1) + rect(W, H, 330, cy - 1, 570, cy + 1)
    art = over(art, flat(np.clip(ln * fade - cm, 0, 1), "#c49a62", 0.8))
    st = shapes(W, H, [star_pts(300, cy, 26, 8, 0.7, math.pi / 8)], smooth=False)
    art = over(art, glaze_tile(st, CB, CB_L, seed=nx(), crackle=0.2))
    art = over(art, glaze_tile(shapes(W, H, [star_pts(300, cy, 13, 8, 0.6, math.pi / 8)], smooth=False), WH, seed=nx()))
    preview(art, "sb-divider", bg=WH)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()
