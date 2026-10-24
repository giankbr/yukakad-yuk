"""Bintang Duabelas — a twelve-point star pattern built by the polygons-in-contact (Hankin) method on the 4.6.12
tiling (dodecagons, hexagons, squares; contact angles 75°/60°/45°), cut as zellige: teal 12-point stars, terracotta
6-point stars, ochre squares, ivory fields, with white glazed strapwork; plus a carved-plaster central rosette
(12-point star ringed by petals), a small zellige star for dividers, and a plaster texture.
Run: python3 -I bintang-duabelas.py [part ...]   parts: tile rosette star plaster
Assets -> public/themes/art/bintang-duabelas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s4_lib import *  # noqa
from scipy.ndimage import label, find_objects, binary_dilation

OUT = outdir("bintang-duabelas")
PARTS = sys.argv[1:] or ["tile", "rosette", "star", "plaster"]
IVORY, IVORY_D = "#ebe0c8", "#d9cdb4"
TEAL, TEAL_D, TEAL_L = "#1f6d6a", "#14504e", "#7fb2a6"
TERRA, TERRA_D = "#b4532e", "#8c3b1f"
OCHRE = "#d2a24c"
GROUT = "#5b5248"
TH = {"d": 75, "h": 60, "s": 45}


def tiling(a, ox, oy, nx_, ny_):
    r12 = a * (2 + math.sqrt(3)) / 2
    L = 2 * r12 + a
    R12 = a / (2 * math.sin(math.pi / 12))
    polys = []
    for j in range(-2, ny_ + 2):
        for i in range(-2, nx_ + 2):
            cx = ox + i * L + (j % 2) * L / 2; cy = oy + j * L * math.sqrt(3) / 2
            polys.append(("d", (cx, cy), regular_poly(cx, cy, R12, 12, math.pi / 12)))
            for ang in (0, math.pi / 3, 2 * math.pi / 3):
                mx, my = cx + math.cos(ang) * L / 2, cy + math.sin(ang) * L / 2
                polys.append(("s", (mx, my), regular_poly(mx, my, a / math.sqrt(2), 4, ang + math.pi / 4)))
            for ang in (math.pi / 6, math.pi / 2):
                hx, hy = cx + math.cos(ang) * L / math.sqrt(3), cy + math.sin(ang) * L / math.sqrt(3)
                polys.append(("h", (hx, hy), regular_poly(hx, hy, a, 6, 0)))
    return polys, L


def pattern_lines(polys):
    out = []
    for k, c, p in polys:
        out += hankin(p, math.radians(TH[k]))
    return out


def glaze_piece(W, H, mask, col, rng, seed):
    """Zellige glaze: per-piece tone shift, pooled darker rim, a soft gloss streak; returns RGBA."""
    rim = np.clip(mask - gaussian_filter(mask, 2.2), 0, 1)
    base = np.array(hex_rgb(col), np.float32)
    n = fbm(W, H, seed, 26, 3)
    rgb = base[None, None, :] * (0.93 + 0.12 * n[..., None])
    rgb = rgb * (1 - rim[..., None] * 0.9)
    return np.concatenate([np.clip(rgb, 0, 1), mask[..., None]], -1)


def zellige(W, H, polys, a, band=7.0, seed=1):
    rng = random.Random(seed)
    lines = pattern_lines(polys)
    for k, c, p in polys:
        if k != "d":
            continue
        R0 = a * 0.62; r0 = R0 * 0.55
        st = []
        for q in range(12):
            a0 = q * math.pi / 6
            st += [(c[0] + R0 * math.cos(a0), c[1] + R0 * math.sin(a0)), (c[0] + r0 * math.cos(a0 + math.pi / 12), c[1] + r0 * math.sin(a0 + math.pi / 12))]
        lines.append(st + [st[0]])
    strap = strokes(W, H, [(pl, band, None) for pl in lines])
    strap = np.clip(strap * 1.4, 0, 1)
    grout = np.clip(strokes(W, H, [(pl, band + 3.2, None) for pl in lines]) * 1.4, 0, 1)
    # regions = complement of the grout lines
    lab, n = label(grout < 0.5)
    objs = find_objects(lab)
    centres = {k: [c for kk, c, p in polys if kk == k] for k in "dhs"}
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(GROUT), np.float32)
    piece_tone = np.zeros((H, W), np.float32)
    colmap = np.zeros((H, W, 3), np.float32)
    info = []
    for i, sl in enumerate(objs, 1):
        if sl is None:
            continue
        reg = lab[sl] == i
        ys, xs = np.nonzero(reg)
        touches = sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == H or sl[1].stop == W
        info.append((i, sl, reg, reg.sum(), ys.mean() + sl[0].start, xs.mean() + sl[1].start, touches))
    # shape classes by area (pieces of one shape share an area); edge-cut pieces inherit the class of the nearest
    # whole piece of the same polygon type
    areas = sorted(set(int(round(ar / (a * a) * 20)) for _, _, _, ar, _, _, t in info if not t))
    print("area classes", areas)
    for i, sl, reg, ar, cy, cx, t in info:
        def near(k):
            return min(math.hypot(cx - x, cy - y) for x, y in centres[k])
        dd, dh, ds = near("d"), near("h"), near("s")
        if dd < a * 0.2:
            col = TEAL if ar > a * a * 1.2 else TERRA
        elif dd < a * 1.15:
            col = TEAL
        elif dd < a * 1.75 and ar > a * a * 0.5 and dh > a * 0.35:
            col = TEAL_L
        elif dh < a * 0.35:
            col = TERRA
        elif ar < a * a * 0.12:
            col = OCHRE
        else:
            col = IVORY
        c = np.array(hex_rgb(col), np.float32) * rng.uniform(0.97, 1.03)
        colmap[sl][reg] = c
        piece_tone[sl][reg] = rng.uniform(-1, 1)
    fill = (lab > 0).astype(np.float32)
    # each piece: slight edge pooling (darker rim), fine crackle, gloss streak
    inner = gaussian_filter(fill, 1.6)
    rim = np.clip(fill - inner, 0, 1)
    n = fbm(W, H, seed + 3, 30, 3)
    g = np.clip(colmap * (0.95 + 0.08 * n[..., None]) * (1 - rim[..., None] * 1.1), 0, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gloss = np.clip(np.sin((xx * 0.7 - yy * 0.9) / 9 + piece_tone * 3) * 0.5 + 0.2, 0, 1) ** 3 * 0.12
    g = g + gloss[..., None] * fill[..., None]
    rgb = rgb * (1 - fill[..., None]) + g * fill[..., None]
    # strapwork: white glazed bands on top of the grout
    sb = np.clip(strap - gaussian_filter(strap, 1.2) * 0.25, 0, 1)
    scol = np.array(hex_rgb("#f6f0e2" if seed != 5 else "#f6f0e2"), np.float32) * (0.94 + 0.08 * fbm(W, H, seed + 7, 18, 2))[..., None]
    shade = np.clip(np.roll(strap, 1, 0) - strap, 0, 1)
    scol = scol * (1 - shade[..., None] * 0.25)
    rgb = rgb * (1 - sb[..., None]) + scol * sb[..., None]
    grain = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.6)
    rgb = rgb * (0.97 + 0.06 * grain[..., None])
    return np.clip(rgb, 0, 1)


def part_tile():
    """Seamless tile: two lattice periods across, two down (period L x L*sqrt3); painted on a larger canvas so
    every piece is whole, then cropped."""
    L = 220.0
    a = L / (3 + math.sqrt(3))
    W = int(round(2 * L)); H = int(round(2 * L * math.sqrt(3)))
    m = 200
    polys, L2 = tiling(a, m, m, 5, 7)
    rgb = zellige(W + 2 * m, H + 2 * m, polys, a, band=6.5, seed=5)[m:m + H, m:m + W]
    prev_rgb(rgb, "bd-tile")
    save_rgb(rgb, f"{OUT}/tile.webp", quality=80)
    print("tile period", L, L * math.sqrt(3), "px at", W, H)
    clear()


def rosette_geo(cx, cy, R):
    """Rosette: 12-point star {12/5}-like (tips on R, valleys on r), 12 hexagonal petals around it, outer 24-gon ring."""
    r = R * 0.62
    tips = [(cx + R * math.cos(k * math.pi / 6 - math.pi / 2), cy + R * math.sin(k * math.pi / 6 - math.pi / 2)) for k in range(12)]
    vals = [(cx + r * math.cos(k * math.pi / 6 + math.pi / 12 - math.pi / 2), cy + r * math.sin(k * math.pi / 6 + math.pi / 12 - math.pi / 2)) for k in range(12)]
    star = []
    for k in range(12):
        star += [tips[k], vals[k]]
    petals = []
    for k in range(12):
        a0 = k * math.pi / 6 - math.pi / 2
        P = lambda ang, rad: (cx + rad * math.cos(a0 + ang), cy + rad * math.sin(a0 + ang))
        petals.append([vals[k], tips[k], P(math.radians(6), R * 1.32), P(math.radians(15), R * 1.5), P(math.radians(24), R * 1.32), tips[(k + 1) % 12]])
    ring = [(cx + R * 1.5 * math.cos(k * math.pi / 12 + math.pi / 12 - math.pi / 2), cy + R * 1.5 * math.sin(k * math.pi / 12 + math.pi / 12 - math.pi / 2)) for k in range(24)]
    inner = [(cx + r * 0.62 * math.cos(k * math.pi / 6 - math.pi / 2), cy + r * 0.62 * math.sin(k * math.pi / 6 - math.pi / 2)) for k in range(12)]
    return star, petals, ring, inner, tips


def part_rosette():
    """Carved plaster rosette: ivory relief bands (raised, lit from top-left), recessed fields washed in teal and
    terracotta, fine chisel texture, a small 12-fold centre."""
    W = H = 760
    cx = cy = 380
    rng = random.Random(4); nx = Seq(2100)
    R = 210
    star, petals, ring, inner, tips = rosette_geo(cx, cy, R)
    disc = circles(W, H, [(cx, cy, R * 1.66)])
    ringpoly = shapes(W, H, [ring], smooth=False)
    # band network: star outline, petals, outer ring, inner star, radial ties
    bw = 11
    items = [(star + [star[0]], bw, None), (ring + [ring[0]], bw, None)]
    items += [(p + [p[0]], bw, None) for p in petals]
    items += [(inner + [inner[0]], bw * 0.8, None)]
    items += [([inner[k], (cx + R * 0.62 * math.cos(k * math.pi / 6 + math.pi / 12 - math.pi / 2), cy + R * 0.62 * math.sin(k * math.pi / 6 + math.pi / 12 - math.pi / 2))], bw * 0.6, None) for k in range(12)]
    # outer border: 12-lobed scalloped edge ring
    scal = []
    for k in range(48):
        ang = k / 48 * math.tau
        rr = R * 1.66 - 9 * (0.5 + 0.5 * math.cos(ang * 12))
        scal.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    items += [(scal + [scal[0]], bw, None)]
    bands = np.clip(strokes(W, H, items) * 1.3, 0, 1)
    body = shapes(W, H, [scal], smooth=True)
    # fields
    starm = shapes(W, H, [star], smooth=False)
    petm = shapes(W, H, petals, smooth=False)
    innerm = shapes(W, H, [inner], smooth=False)
    outer = np.clip(body - ringpoly, 0, 1)
    ringf = np.clip(ringpoly - petm - starm, 0, 1)
    # plaster base: ivory with chisel texture, recessed (darker) fields
    base = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#efe5cf"), np.float32)
    tex = hatch(W, H, 0.4, 3.0, 0.3, seed=3) * 0.05 + hatch(W, H, -0.9, 3.4, 0.3, seed=4) * 0.04
    rgb = base * (1 - tex[..., None])
    def tint(rgb, m, col, k):
        c = np.array(hex_rgb(col), np.float32)
        mm = np.clip(gaussian_filter(m, 0.8), 0, 1)[..., None] * k * (0.85 + 0.3 * fbm(W, H, nx(), 30, 2))[..., None]
        return rgb * (1 - mm) + (rgb * c * 1.05) * mm
    rgb = tint(rgb, np.clip(starm - innerm, 0, 1), TEAL, 0.85)
    rgb = tint(rgb, innerm, TERRA, 0.85)
    rgb = tint(rgb, petm, "#c7a46a", 0.45)
    rgb = tint(rgb, ringf, TEAL, 0.55)
    rgb = tint(rgb, outer, TERRA, 0.5)
    # carved relief: recessed fields shaded on their upper-left inner edge; bands raised and lit
    rec = np.clip(body - bands, 0, 1)
    e = gaussian_filter(bands, 2.0)
    gy, gx = np.gradient(e)
    lit = np.clip(-(gx + gy) * 9, -1, 1)
    rgb = rgb * (1 + (lit * bands)[..., None] * 0.22)
    shadow = np.clip(np.roll(np.roll(bands, 3, 0), 3, 1) - bands, 0, 1) * rec
    rgb = rgb * (1 - gaussian_filter(shadow, 1.0)[..., None] * 0.35)
    bandcol = np.array(hex_rgb("#f7f0e0"), np.float32) * (0.95 + 0.07 * fbm(W, H, nx(), 16, 2))[..., None]
    rgb = rgb * (1 - bands[..., None] * 0.75) + bandcol * (1 + lit[..., None] * 0.12) * bands[..., None] * 0.75
    # wear: a few chips in the bands and dust in the recesses
    chips = (fbm(W, H, nx(), 7, 2) > 0.8).astype(np.float32) * bands
    rgb = rgb * (1 - gaussian_filter(chips, 0.6)[..., None] * 0.12)
    alpha = np.clip(gaussian_filter(body, 0.7) * 1.2, 0, 1)
    sh = np.clip(gaussian_filter(np.roll(np.roll(body, 8, 0), 5, 1), 8) - body, 0, 1) * 0.35
    arr = np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], -1)
    shadow_l = np.concatenate([np.zeros((H, W, 3), np.float32) + np.array(hex_rgb("#5b4630"), np.float32), sh[..., None]], -1)
    arr = over(shadow_l, arr)
    prev_rgba(arr, "bd-rosette", bg="#efe7d6")
    save_a(arr, f"{OUT}/rosette.webp", max_w=620, quality=82)
    clear()


def part_star():
    """A single zellige 12-point star piece (teal) with a terracotta centre, for dividers and timeline nodes."""
    W = H = 220
    cx = cy = 110
    R = 100; r = R * 0.62
    pts = []
    for k in range(12):
        a0 = k * math.pi / 6 - math.pi / 2
        pts += [(cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + r * math.cos(a0 + math.pi / 12), cy + r * math.sin(a0 + math.pi / 12))]
    m = shapes(W, H, [pts], smooth=False)
    mi = shapes(W, H, [regular_poly(cx, cy, r * 0.55, 12, math.pi / 12)], smooth=False)
    rgb = np.zeros((H, W, 3), np.float32)
    outer = np.clip(m - gaussian_filter(mi, 0.5) * 1.6, 0, 1)
    for mask, col, sd in ((np.clip(m, 0, 1), TEAL, 3), (mi, TERRA, 4)):
        gp_ = glaze_piece(W, H, mask, col, None, sd)
        rgb = rgb * (1 - mask[..., None]) + gp_[..., :3] * mask[..., None]
    grout = np.clip(strokes(W, H, [(regular_poly(cx, cy, r * 0.55, 12, math.pi / 12) + [regular_poly(cx, cy, r * 0.55, 12, math.pi / 12)[0]], 3.5, None)]), 0, 1) * m
    rgb = rgb * (1 - grout[..., None]) + np.array(hex_rgb("#f6f0e2"), np.float32) * grout[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gloss = np.clip(1 - np.hypot(xx - 80, yy - 70) / 70, 0, 1) ** 2 * 0.25
    rgb = rgb + gloss[..., None]
    alpha = np.clip(gaussian_filter(m, 0.6) * 1.1, 0, 1)
    arr = np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], -1)
    prev_rgba(arr, "bd-star")
    save_a(arr, f"{OUT}/star.webp", max_w=120, quality=86)
    clear()


def part_plaster():
    """Seamless ivory lime-plaster texture (trowel marks, faint mottling)."""
    N = 512
    rgb = np.ones((N, N, 3), np.float32) * np.array(hex_rgb("#f1e9d8"), np.float32)
    n1 = wnoise(N, N, 3, 26); n2 = wnoise(N, N, 5, 4); n3 = wnoise(N, N, 9, 1.2)
    tr = gaussian_filter(np.random.default_rng(2).random((N, N)).astype(np.float32), (2, 22), mode="wrap")
    tr = (tr - tr.min()) / (tr.max() - tr.min())
    rgb = rgb * (0.965 + 0.05 * n1[..., None] + 0.02 * n2[..., None] + 0.018 * n3[..., None] + 0.03 * (tr[..., None] - 0.5))
    prev_rgb(rgb, "bd-plaster")
    save_rgb(rgb, f"{OUT}/plaster.webp", quality=70)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
