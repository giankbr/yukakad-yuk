"""Kaca Cermin — Persian aineh-kari: hand-cut mirror facets set in geometric patterns (khatam star medallion, a
mosaic frieze, a seamless mirror lattice tile, a small rosette), reflecting silver, deep teal and rose-gold lamp light.
No figures, no calligraphy. Glints are a separate asset (animated in CSS).
Run: python3 -I kaca-cermin.py [part ...]   parts: star frieze tile rosette glint divider wall
Assets -> public/themes/art/kaca-cermin/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k4_lib import *

OUT = outdir("kaca-cermin")
PARTS = sys.argv[1:] or ["star", "frieze", "tile", "rosette", "glint", "divider", "wall"]
ENV = ["#eef4f3", "#c9dbda", "#9db9b8", "#6c9596", "#3a6f72", "#24555a", "#f0cdb9", "#d49c84", "#b97a64", "#fbf7f1", "#7fa6a6"]
ROSE = ["#f2d1bf", "#e0ac94", "#c98a73", "#a9654f", "#f7e3d6"]
GROUT = "#0a2c30"


def polar_facets(cx, cy, r0, r1, step, base_n, rng, jitter=0.6):
    """Concentric rings of quads split into triangles (diamond facets), n per ring a multiple of base_n."""
    out = []
    r = r0
    k = 0
    while r < r1:
        r2 = min(r1, r + step)
        n = base_n * max(1, round(2 * math.pi * r2 / (step * 1.15) / base_n))
        off = (math.pi / n) * (k % 2)
        for i in range(n):
            a0 = off + i * math.tau / n; a1 = off + (i + 1) * math.tau / n
            p = [(cx + math.cos(a0) * r, cy + math.sin(a0) * r), (cx + math.cos(a1) * r, cy + math.sin(a1) * r),
                 (cx + math.cos(a1) * r2, cy + math.sin(a1) * r2), (cx + math.cos(a0) * r2, cy + math.sin(a0) * r2)]
            p = [(x + rng.uniform(-jitter, jitter), y + rng.uniform(-jitter, jitter)) for x, y in p]
            if (i + k) % 2:
                out += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
            else:
                out += [[p[0], p[1], p[3]], [p[1], p[2], p[3]]]
        r = r2; k += 1
    return out


def outline(mask, px):
    return np.clip((gaussian_filter(mask, px * 0.6) > 0.02).astype(np.float32) - (mask > 0.5), 0, 1)


if "star" in PARTS:
    W = H = 780
    cx = cy = W / 2
    rng = random.Random(4)
    R, r_in = 372, 236
    star = shapes(W, H, [star_poly(cx, cy, R, R * 0.80, 8, -math.pi / 2)], smooth=False)
    octa = shapes(W, H, [poly_reg(cx, cy, r_in, 8, -math.pi / 2 + math.pi / 8)], smooth=False)
    oct_a = poly_reg(cx, cy, r_in, 8, -math.pi / 2 + math.pi / 8)
    oct_b = poly_reg(cx, cy, r_in + 30, 8, -math.pi / 2 + math.pi / 8)
    starp = star_poly(cx, cy, R - 2, R * 0.80, 8, -math.pi / 2)
    M = 96
    SIL = ["#f6faf9", "#2c5e62", "#97b8b8", "#d3e3e2", "#467b7e", "#ffffff", "#1d4a4e", "#bcd3d2", "#6f9a9b"]
    def col_main(i, k, h):
        j = i % 12; j = min(j, 11 - j)
        if (j + k) % 6 == 0 and h == 0:
            return ("#f0cdb9", "#c98a73")
        n = (j * 2 + k * 3 + h * 5) % len(SIL)
        return (SIL[n], SIL[(n + 4) % len(SIL)])
    fm = morph_rings(cx, cy, oct_b, starp, M, 7, rot=-math.pi / 2 + 1e-3, ease=0.9)
    m1 = mirror_facets(W, H, [f[0] for f in fm], seed=7, grout=GROUT, grout_w=2.0, colors=[col_main(*f[1:]) for f in fm], spec_p=0.3)
    ROSEP = ["#f7e3d6", "#e8b9a2", "#c98a73", "#f2d1bf", "#a9654f"]
    fr = morph_rings(cx, cy, oct_a, oct_b, M, 2, rot=-math.pi / 2 + 1e-3)
    m2 = mirror_facets(W, H, [f[0] for f in fr], seed=9, grout=GROUT, grout_w=1.8,
                       colors=[(ROSEP[(f[1] + f[2] * 2 + f[3]) % 5], ROSEP[(f[1] + 2) % 5]) for f in fr], spec_p=0.35)
    octa = shapes(W, H, [oct_a], smooth=False)
    ring_rose = np.clip(shapes(W, H, [oct_b], smooth=False) - octa, 0, 1)
    art = blank(W, H)
    art = over(art, drop_shadow(star, "#000000", 10, 0, 10, 0.55))
    art = over(art, m1)
    art = over(art, m2)
    # eight silver ray lozenges pointing to the star tips
    loz = []
    for i in range(8):
        a = -math.pi / 2 + i * math.tau / 8
        c0 = (cx + math.cos(a) * (r_in + 52), cy + math.sin(a) * (r_in + 52)); c1 = (cx + math.cos(a) * (R - 22), cy + math.sin(a) * (R - 22))
        mid = ((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2)
        nx_, ny_ = -math.sin(a) * 15, math.cos(a) * 15
        loz += [[c0, (mid[0] + nx_, mid[1] + ny_), mid], [c0, mid, (mid[0] - nx_, mid[1] - ny_)],
                [c1, (mid[0] + nx_, mid[1] + ny_), mid], [c1, mid, (mid[0] - nx_, mid[1] - ny_)]]
    m3 = mirror_facets(W, H, loz, seed=11, grout=GROUT, grout_w=1.6, colors=[("#ffffff", "#c6d7d6"), ("#e6efee", "#ffffff"), ("#c6d7d6", "#ffffff"), ("#f3d9cc", "#ffffff")] * 8)
    lozm = shapes(W, H, [[l[0], l[1], l[2]] for l in loz], smooth=False)
    art = over(art, m3)
    # raised plaster bead edges: star outline + octagon outline in rose-gold foil
    star_edge = np.clip((gaussian_filter(star, 2.2) > 0.05).astype(np.float32) - (gaussian_filter(star, 2.2) > 0.95).astype(np.float32), 0, 1)
    oct_edge = np.clip((gaussian_filter(octa, 2.4) > 0.05).astype(np.float32) - (gaussian_filter(octa, 2.4) > 0.95).astype(np.float32), 0, 1)
    rose_edge = np.clip((gaussian_filter(ring_rose + octa, 1.6) > 0.05).astype(np.float32) - (gaussian_filter(ring_rose + octa, 1.6) > 0.95).astype(np.float32), 0, 1)
    art = FO(art, np.maximum.reduce([star_edge, oct_edge, rose_edge * 0.8]), "#d9a48c", seed=3, emboss=0.9, sparkle=0.4)
    # the octagon itself: deep teal lacquer, a soft reflected sheen
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = smooth01(1 - np.hypot(xx - cx + 60, yy - cy + 90) / 300)
    rgb = ramp(0.25 + 0.5 * sheen + (fbm(W, H, 5, 60, 3) - 0.5) * 0.1, [(0, "#071f22"), (0.5, "#0d3a3f"), (1, "#1a5a5e")])
    core = rgba(rgb, np.clip(octa - oct_edge, 0, 1))
    art = over(core, art) if False else over(art, core)
    show(art, "kc-star", bg="#0d3a3f")
    save(art, f"{OUT}/star.webp", max_w=720, quality=80)
    clear()

if "frieze" in PARTS:
    # repeat-x band: small 8-point stars alternating with silver crosses, rose-gold border rows
    TW, H = 240, 96
    rng = random.Random(12)
    polys = []
    cy = H / 2
    # border rows of small triangles
    for row_y, h_, flip in ((0, 14, 0), (H - 14, 14, 1)):
        for i in range(0, TW, 12):
            a = (i, row_y + (h_ if not flip else 0)); b = (i + 12, row_y + (h_ if not flip else 0)); c = (i + 6, row_y + (0 if not flip else h_))
            polys.append(("r", [a, b, c]))
            polys.append(("r", [c, (i + 18, row_y + (0 if not flip else h_)), b]))
    for k in range(2):
        sx = 60 + k * 120
        st = star_poly(sx, cy, 30, 22, 8, -math.pi / 2)
        for i in range(16):
            polys.append(("s", [(sx, cy), st[i], st[(i + 1) % 16]]))
        # cross between stars
        xx = sx + 60
        cr = [(xx - 26, cy), (xx - 8, cy - 8), (xx, cy - 26), (xx + 8, cy - 8), (xx + 26, cy), (xx + 8, cy + 8), (xx, cy + 26), (xx - 8, cy + 8)]
        for i in range(8):
            polys.append(("c", [(xx, cy), cr[i], cr[(i + 1) % 8]]))
    W = TW * 3
    allp = {"r": [], "s": [], "c": []}
    for kind, p in polys:
        for o in (-TW, 0, TW, 2 * TW):
            allp[kind].append([(x + o + TW, y) for x, y in p])
    bg = shapes(W, H, [[(0, 0), (W, 0), (W, H), (0, H)]], smooth=False)
    art = over(blank(W, H), flat(bg, GROUT))
    # field between motifs: tiny silver triangles
    fill = []
    for i in range(0, W, 10):
        for j, y in enumerate(range(16, H - 16, 11)):
            o = 5 * (j % 2)
            fill.append([(i + o, y), (i + o + 10, y), (i + o + 5, y + 11)])
    mf = mirror_facets(W, H, fill, seed=21, env=["#2f6266", "#3e777a", "#1f4e52", "#5e8f90"], grout=GROUT, grout_w=1.4)
    art = over(art, mf)
    keep = shapes(W, H, allp["s"] + allp["c"], smooth=False)
    art[..., 3] = np.maximum(art[..., 3], 0)
    ms = mirror_facets(W, H, allp["s"], seed=23, env=ENV, grout=GROUT, grout_w=1.6)
    mc = mirror_facets(W, H, allp["c"], seed=25, env=["#ffffff", "#e6efee", "#c6d7d6"], grout=GROUT, grout_w=1.4)
    mr = mirror_facets(W, H, allp["r"], seed=27, env=ROSE, grout=GROUT, grout_w=1.4)
    for m in (ms, mc, mr):
        art = over(art, m)
    art = art[:, TW:2 * TW]
    show(np.concatenate([art] * 3, 1), "kc-frieze", bg="#0d3a3f")
    save_full(art, f"{OUT}/frieze.webp", size=(160, 64), quality=82)
    clear()

if "tile" in PARTS:
    # seamless mirror lattice: 45-degree diamonds each cut in four triangles; colours repeat with the tile period
    T = 240
    s_ = 30
    polys, cols = [], []
    PAL = ["#f6faf9", "#2c5e62", "#bcd3d2", "#6f9a9b", "#ffffff", "#467b7e", "#d3e3e2", "#1d4a4e"]
    for gy in range(-2, 2 * T // s_ + 3):
        for gx in range(-2, T // s_ + 3):
            cx = gx * s_ + (s_ / 2 if gy % 2 else 0); cy = gy * s_ / 2
            d = [(cx, cy - s_ / 2), (cx + s_ / 2, cy), (cx, cy + s_ / 2), (cx - s_ / 2, cy)]
            u, v = gx % (T // s_), gy % (2 * T // s_)
            ring = (abs(u - 4) + abs(v - 8) // 2) % 4
            for i in range(4):
                polys.append([(cx, cy), d[i], d[(i + 1) % 4]])
                if ring == 0 and i % 2 == 0:
                    cols.append(("#f0cdb9", "#c98a73"))
                else:
                    n = (ring * 2 + i) % len(PAL)
                    cols.append((PAL[n], PAL[(n + 3) % len(PAL)]))
    W = H = T
    art = over(blank(W, H), flat(np.ones((H, W), np.float32), GROUT))
    m = mirror_facets(W, H, polys, seed=33, grout=GROUT, grout_w=1.6, colors=cols, spec_p=0.0)
    art = over(art, m)
    show(np.tile(art, (2, 2, 1)), "kc-tile", bg="#0d3a3f")
    save_rgb(art, f"{OUT}/tile.webp", size=(160, 160), quality=82)
    clear()

if "rosette" in PARTS:
    W = H = 240
    cx = cy = W / 2
    rng = random.Random(41)
    st = star_poly(cx, cy, 108, 80, 8, -math.pi / 2)
    polys = []
    for i in range(16):
        mid = ((st[i][0] + st[(i + 1) % 16][0]) / 2 * 0.5 + cx * 0.5, (st[i][1] + st[(i + 1) % 16][1]) / 2 * 0.5 + cy * 0.5)
        polys += [[mid, st[i], st[(i + 1) % 16]]]
    inner = poly_reg(cx, cy, 52, 16, 0)
    mids = [(((st[i][0] + st[(i + 1) % 16][0]) / 2 * 0.5 + cx * 0.5), ((st[i][1] + st[(i + 1) % 16][1]) / 2 * 0.5 + cy * 0.5)) for i in range(16)]
    for i in range(16):
        polys.append([(cx, cy), mids[i], mids[(i + 1) % 16]])
        polys.append([mids[i], st[(i + 1) % 16], mids[(i + 1) % 16]])
    star = shapes(W, H, [st], smooth=False)
    art = over(blank(W, H), drop_shadow(star, "#000000", 5, 0, 5, 0.5))
    art = over(art, flat(star, GROUT))
    m = mirror_facets(W, H, polys[:16], seed=43, env=ENV, grout=GROUT, grout_w=1.8)
    m2 = mirror_facets(W, H, polys[16:], seed=45, env=ROSE + ["#ffffff", "#e6efee"], grout=GROUT, grout_w=1.8)
    art = over(over(art, m), m2)
    e = np.clip((gaussian_filter(star, 1.8) > 0.05).astype(np.float32) - (gaussian_filter(star, 1.8) > 0.95).astype(np.float32), 0, 1)
    art = FO(art, e, "#d9a48c", seed=5, emboss=0.9)
    show(art, "kc-rosette", bg="#0d3a3f")
    save(art, f"{OUT}/rosette.webp", max_w=120, quality=84)

if "glint" in PARTS:
    W = H = 128
    g = glint(W, H, 64, 64, 60, 0.0)
    art = flat(g, "#ffffff")
    halo = gaussian_filter(circles(W, H, [(64, 64, 20)]), 10) * 0.35
    art = over(flat(halo, "#ffe3d3"), art)
    show(art, "kc-glint", bg="#0d3a3f")
    save_full(art, f"{OUT}/glint.webp", size=(64, 64), quality=86)

if "divider" in PARTS:
    W, H = 720, 72
    cy = H / 2
    polys_c = []; polys_s = []
    for i, x in enumerate(range(120, 601, 40)):
        big = (i == 6)
        s_ = 26 if big else (14 if abs(i - 6) < 3 else 9)
        d = [(x, cy - s_), (x + s_ * 0.8, cy), (x, cy + s_), (x - s_ * 0.8, cy)]
        tgt = polys_s if big or i % 2 == 0 else polys_c
        for k in range(4):
            tgt.append([(x, cy), d[k], d[(k + 1) % 4]])
    line = strokes(W, H, [([(40, cy), (W - 40, cy)], 2.0, (0.25, 0.25))])
    art = blank(W, H)
    art = FO(art, line, "#d9a48c", seed=7, emboss=0.6)
    art = over(art, mirror_facets(W, H, polys_s, seed=51, env=ENV, grout=GROUT, grout_w=1.4))
    art = over(art, mirror_facets(W, H, polys_c, seed=53, env=ROSE, grout=GROUT, grout_w=1.4))
    show(art, "kc-divider", bg="#0d3a3f")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)

if "wall" in PARTS:
    # seamless deep-teal lacquered plaster for the page background
    W = H = 384
    a = wrap_noise(W, H, 61, 30); b = wrap_noise(W, H, 62, 6); c = wrap_noise(W, H, 63, 0.8)
    t = np.clip(0.5 + (a - 0.5) * 0.9 + (b - 0.5) * 0.3 + (c - 0.5) * 0.12, 0, 1)
    rgb = ramp(t, [(0, "#0a3034"), (0.5, "#0e3a3f"), (1, "#14474c")])
    w = rgba(rgb, np.ones((H, W), np.float32))
    show(w, "kc-wall")
    save_rgb(w, f"{OUT}/wall.webp", quality=72)
