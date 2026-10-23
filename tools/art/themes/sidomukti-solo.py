"""Sidomukti Solo — batik Sidomukti (wedding batik of Surakarta): a diagonal lattice of lozenges holding kupu
(butterflies) and bunga (blossoms) in sogan brown and cream with fine isen-isen (cecek dots, ukel curls); a sepia
ink-and-wash pendopo; roncean melati. Motifs are redrawn, not copied from a particular cloth; no gurdha.
Run: python3 -I sidomukti-solo.py [part ...]  parts: batik kupu ronce pendopo divider
Assets -> public/themes/art/sidomukti-solo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n1_lib import *

OUT = outdir("sidomukti-solo")
PARTS = sys.argv[1:] or ["batik", "kupu", "ronce", "pendopo", "divider"]
SOGA, SOGA_D, SOGA_L = "#6e4322", "#4f2d16", "#8a5a30"
TUA = "#2b1d14"          # near-black sogan tua / indigo-brown
CREAM = "#efdfbf"
CREAM_D = "#d9c29a"


def ukel(cx, cy, r, a0, d=1, turns=1.1):
    return spiral_pts(cx, cy, r, r * 0.15, a0, turns, 22, d)


def kupu_geo(cx, cy, s):
    """Batik butterfly (top view). Returns (wing polys, body poly, line items, dot centres)."""
    wings, lines, dots = [], [], []
    for d in (-1, 1):
        up = [(cx + d * 4 * s, cy - 6 * s), (cx + d * 18 * s, cy - 30 * s), (cx + d * 40 * s, cy - 40 * s), (cx + d * 50 * s, cy - 28 * s),
              (cx + d * 46 * s, cy - 8 * s), (cx + d * 24 * s, cy + 2 * s), (cx + d * 6 * s, cy + 2 * s)]
        lo = [(cx + d * 5 * s, cy + 4 * s), (cx + d * 30 * s, cy + 6 * s), (cx + d * 38 * s, cy + 22 * s), (cx + d * 28 * s, cy + 38 * s),
              (cx + d * 14 * s, cy + 34 * s), (cx + d * 5 * s, cy + 18 * s)]
        wings += [up, lo]
        lines.append((ukel(cx + d * 30 * s, cy - 22 * s, 9 * s, math.pi * (0 if d > 0 else 1), d), 2.2 * s, (0.0, 0.6)))
        lines.append((ukel(cx + d * 22 * s, cy + 20 * s, 7 * s, math.pi * (0 if d > 0 else 1), -d), 2.0 * s, (0.0, 0.6)))
        lines.append((curve([(cx + d * 2 * s, cy - 18 * s), (cx + d * 8 * s, cy - 34 * s), (cx + d * 16 * s, cy - 40 * s)], 12), 1.8 * s, (0.0, 0.3)))
        lines.append((ukel(cx + d * 17 * s, cy - 42 * s, 3.5 * s, math.pi / 2, d, 0.9), 1.6 * s, (0.0, 0.5)))
        # vein lines across the wings
        for t in (0.35, 0.62):
            lines.append(([(cx + d * 8 * s, cy - 4 * s), (cx + d * (12 + 36 * t) * s, cy - (8 + 30 * t) * s)], 1.4 * s, (0.0, 0.4)))
        dots += [(cx + d * x * s, cy + y * s) for x, y in [(40, -16), (44, -24), (36, -30), (14, -16), (20, -8), (32, -6), (30, 30), (20, 28), (16, 12)]]
    body = ellipse_pts(cx, cy - 2 * s, 4.5 * s, 22 * s, 14)
    return wings, body, lines, dots


def bunga_geo(cx, cy, s, n=8, rot0=0.0):
    outer = [petal_pts(cx, cy, 40 * s, 18 * s, rot0 + k * math.tau / n, n=12) for k in range(n)]
    inner = [petal_pts(cx, cy, 20 * s, 8 * s, rot0 + (k + 0.5) * math.tau / n, n=10) for k in range(n)]
    lines = [(ukel(cx + math.cos(rot0 + k * math.tau / n) * 28 * s, cy + math.sin(rot0 + k * math.tau / n) * 28 * s, 5 * s, rot0 + k * math.tau / n, 1, 0.9), 1.6 * s, (0.0, 0.5)) for k in range(n)]
    leaves = [petal_pts(cx + math.cos(rot0 + (k + 0.5) * math.tau / n) * 30 * s, cy + math.sin(rot0 + (k + 0.5) * math.tau / n) * 30 * s, 16 * s, 5 * s, rot0 + (k + 0.5) * math.tau / n, n=8) for k in range(n)]
    return outer, inner, lines, leaves


def batik_render(W, H, cream, dark, seed, ground=SOGA, ground2=SOGA_D, crackle=0.45, weave=True):
    """Hand-drawn batik tulis: soga ground with uneven dye, dark (sogan tua) blocked areas, cream wax lines with a
    soft brown halo where dye crept under the wax, crackle veins, slight canting wobble."""
    c = displace(cream, seed, 1.2, 8)
    c = np.clip((gaussian_filter(c, 0.7) - 0.3) * 2.6, 0, 1)
    dk = np.clip((gaussian_filter(displace(dark, seed + 1, 1.4, 10), 0.8) - 0.3) * 2.4, 0, 1)
    t = wrap_noise(W, H, seed + 2, 22)[..., None]
    rgb = col3(ground) * (1 - t) + col3(ground2) * t
    rgb = rgb * (0.93 + 0.14 * wrap_noise(W, H, seed + 3, 6)[..., None])
    rgb = rgb * (1 - dk[..., None]) + col3(TUA) * (0.9 + 0.2 * wrap_noise(W, H, seed + 4, 4)[..., None]) * dk[..., None]
    halo = np.clip(gaussian_filter(c, 1.8) - c, 0, 1)[..., None]
    rgb = rgb * (1 - halo * 0.35) + col3(SOGA_L) * halo * 0.35
    wx = col3(CREAM) * (0.94 + 0.08 * wrap_noise(W, H, seed + 5, 10)[..., None])
    rgb = rgb * (1 - c[..., None]) + wx * c[..., None]
    if crackle:
        n = wrap_noise(W, H, seed + 6, 5)
        vein = np.clip(1 - np.abs(n - 0.5) * 36, 0, 1)
        rgb = rgb * (1 - (vein * c * crackle)[..., None]) + col3(SOGA) * (vein * c * crackle)[..., None]
    if weave:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        wv = 1 + 0.025 * np.sin(xx * math.pi / 1.3) + 0.025 * np.sin(yy * math.pi / 1.4)
        rgb = rgb * wv[..., None]
    return np.clip(rgb, 0, 1).astype(np.float32)


def batik():
    """Seamless Sidomukti tile: double-line diagonal lattice with cecek, rosettes at the crossings, lozenges holding
    kupu and bunga in turn, fine cecek isen in the ground."""
    W = H = 320
    rng = random.Random(3)
    cream_items, cream_polys, dark_polys, dots = [], [], [], []
    # lattice lines x+y = 160k and x-y = 160m (two parallel cream lines each)
    for k in range(-3, 6):
        for off in (-5, 5):
            c0 = 160 * k + off
            cream_items.append(([(c0 - (-40), -40), (c0 + 40 - 400, 400 - 40 + 0)], 2.4, None))
    cream_items = []
    L = 520
    for k in range(-4, 6):
        for off in (-5.5, 5.5):
            # x + y = c  -> points (c + 40, -40) to (c - L, L)
            c = 160 * k + off
            cream_items.append(([(c + 60, -60), (c - L, L - 0 + 0)], 2.3, None))
            # x - y = c -> points (c - 60, -60) to (c + L, L)
            cream_items.append(([(c - 60, -60), (c + L, L)], 2.3, None))
        for t in np.arange(-60, L, 9):
            c = 160 * k
            dots.append((c - t, t, 1.6)); dots.append((c + t, t, 1.6))
    # rosettes at crossings: x+y=160k & x-y=160m -> x=80(k+m), y=80(k-m)
    cells = []
    for k in range(-2, 6):
        for m in range(-4, 4):
            x, y = 80 * (k + m), 80 * (k - m)
            if -100 < x < W + 100 and -100 < y < H + 100:
                cream_polys += [petal_pts(x, y, 13, 6, q * math.pi / 2 + math.pi / 4, n=8) for q in range(4)]
                dark_polys.append(ellipse_pts(x, y, 7, 7, 10))
            cx, cy = 80 * (k + m + 1), 80 * (k - m)
            if -100 < cx < W + 100 and -100 < cy < H + 100:
                cells.append((cx, cy, k))
    for cx, cy, k in cells:
        if k % 2 == 0:
            wings, body, lines, kd = kupu_geo(cx, cy + 4, 0.92)
            dark_polys += wings
            cream_items += [(p + [p[0]], 2.6, None) for p in wings] + lines
            cream_polys.append(body)
            dots += [(x, y, 1.7) for x, y in kd]
        else:
            outer, inner, lines, leaves = bunga_geo(cx, cy, 1.0, 8, 0.2)
            dark_polys += outer
            cream_items += [(p + [p[0]], 2.4, None) for p in outer] + lines
            cream_polys += inner + leaves
            cream_polys.append(ellipse_pts(cx, cy, 5, 5, 10))
    # cecek isen scattered in the open ground of each lozenge
    for _ in range(900):
        dots.append((rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.0, 1.5)))
    cream = np.maximum.reduce([strokes(W, H, tile_items(cream_items, W, H)), shapes(W, H, tile_polys(cream_polys, W, H))])
    dark = shapes(W, H, tile_polys(dark_polys, W, H))
    # dots only where not already wax / dark-blocked... keep dots off lines
    dm = circles(W, H, [(x + dx, y + dy, r) for (x, y, r) in dots for dx in (-W, 0, W) for dy in (-H, 0, H) if -10 < x + dx < W + 10 and -10 < y + dy < H + 10])
    occupied = dilate(cream, 2.5)
    cream = np.maximum(cream, dm * (1 - occupied))
    # inside the dark wings: cream cecek stay (they were placed there deliberately)
    rgb = batik_render(W, H, cream, dark * (1 - cream), 7)
    art = rgba(rgb, np.ones((H, W), np.float32))
    preview(art, "ss-batik")
    save_rgb(art, f"{OUT}/batik.webp", quality=80)


def kupu():
    """Single batik kupu as a cut-out motif (cream wax on sogan), used as ornament."""
    W, H = 240, 200
    nx = Seq(400)
    wings, body, lines, kd = kupu_geo(W / 2, H / 2 + 6, 2.1)
    wm = shapes(W, H, wings)
    cream = np.maximum.reduce([strokes(W, H, [(p + [p[0]], 5.0, None) for p in wings] + lines), shapes(W, H, [body]), circles(W, H, [(x, y, 3.2) for x, y in kd])])
    rgb = batik_render(W, H, cream, wm, 9, weave=False)
    a = np.clip(np.maximum(dilate(wm, 1.2), cream), 0, 1)
    a = np.clip((gaussian_filter(displace(a, 4, 1.2, 10), 0.8) - 0.3) * 3, 0, 1)
    art = rgba(rgb, a)
    preview(art, "ss-kupu", bg=CREAM)
    save(art, f"{OUT}/kupu.webp", max_w=200, quality=84)


def ronce():
    """Roncean melati: two strands hanging from a knot of jasmine with a kantil bud at the end, vertical."""
    W, H = 160, 640
    rng = random.Random(5); nx = Seq(700)
    art = blank(W, H)
    for k, (x0, sway, end) in enumerate([(W * 0.42, 14, H * 0.92), (W * 0.6, -10, H * 0.78)]):
        pts = curve([(x0, 30), (x0 + sway, H * 0.35), (x0 - sway * 0.6, H * 0.65), (x0 + sway * 0.3, end)], 160)
        art = melati_string(art, W, H, pts, rng, nx, size=9.5)
        ex, ey = pts[-1]
        # kantil (magnolia) bud tip, cream-ivory with a green calyx
        bud = shapes(W, H, [petal_pts(ex, ey + 4, 30, 9, math.pi / 2, n=12)])
        art = GP(art, bud, "#fbf2dc", "#ead9b4", seed=nx(), rough=1.0)
        art = G(art, edge_ring(bud, 1.2), "#a8906a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
        cal = shapes(W, H, [petal_pts(ex, ey, 12, 6, math.pi / 2 + d * 0.5, n=8) for d in (-1, 1)])
        art = G(art, cal, "#7e8f55", "#4f6236", seed=nx(), density=0.8, edge=0.4, rough=1)
    for _ in range(5):
        art = white_flower(art, W, H, W * 0.5 + rng.uniform(-22, 22), 28 + rng.uniform(-10, 12), 13, rng, nx)
    leaf_l = shapes(W, H, [petal_pts(W * 0.5, 30, 46, 14, math.pi * 0.85, n=12), petal_pts(W * 0.5, 30, 40, 12, math.pi * 0.15, n=12)])
    lv = knockout(G(blank(W, H), leaf_l, "#7a9160", "#4c6640", seed=nx(), density=0.75, edge=0.5, bloom=0.3, rough=3), art[..., 3], 0.9, 2)
    art = over(lv, art)
    preview(art, "ss-ronce", bg=SOGA)
    save(art, f"{OUT}/ronce.webp", max_w=120, quality=84)


def pendopo():
    """A pendopo seen from the courtyard, in sepia ink and soga washes: stone plinth and steps, rows of teak saka with
    the four soko guru inside, layered joglo roof (brunjung, penanggap, penitih) and hanging lamps; sawo trees."""
    W, H = 760, 460
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    INK = "#3a2416"
    WASH = "#9a6a3e"
    cx, gy = W / 2, H * 0.9
    # ground wash and soft shadow
    art = G(art, shapes(W, H, [deform(ellipse_pts(cx, gy + 6, W * 0.48, 20, 16), rng, 2, 0.1)]), "#c9a77a", "#b08a5a", seed=nx(), density=0.45, edge=0.3, bloom=0.4, rough=6)
    # trees behind (sawo kecik), loose washes
    for (tx, r) in [(W * 0.07, 96), (W * 0.94, 104)]:
        tm = shapes(W, H, [deform(ellipse_pts(tx, gy - r * 1.4, r, r * 1.05, 14), rng, 3, 0.22)])
        art = G(art, tm, "#8f8a5e", "#6c6a48", seed=nx(), density=0.55, edge=0.45, bloom=0.5, rough=8)
        art = G(art, tm * fbm(W, H, nx(), 10, 3), "#5a5a3a", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=4)
        art = G(art, strokes(W, H, [([(tx, gy), (tx + rng.uniform(-6, 6), gy - r * 0.9)], 7, (0.0, 0.3))]), "#5a4430", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=1)
    inner_top = gy - 30 - H * 0.36
    eave = inner_top + 6
    bld = shapes(W, H, [rect(cx - W * 0.33, inner_top, cx + W * 0.33, gy - 30), [(cx - W * 0.47, eave + 8), (cx + W * 0.47, eave + 8), (cx + W * 0.045, eave - 190), (cx - W * 0.045, eave - 190)]], smooth=False)
    art = knockout(art, bld, 1.0, 1.5)
    # plinth (umpak bebatur) with steps
    pl = shapes(W, H, [rect(cx - W * 0.36, gy - 30, cx + W * 0.36, gy)], smooth=False)
    art = G(art, pl, "#cdb592", "#b89a72", seed=nx(), density=0.7, edge=0.5, bloom=0.3, rough=2)
    st = shapes(W, H, [rect(cx - 70, gy - 30 + 10 * i, cx + 70, gy - 20 + 10 * i) for i in range(3)], smooth=False)
    art = G(art, st, "#bea07a", seed=nx(), density=0.5, edge=0.6, bloom=0.2, rough=1.5)
    # interior shade under the roof
    inner_top = gy - 30 - H * 0.36
    shade = shapes(W, H, [rect(cx - W * 0.33, inner_top, cx + W * 0.33, gy - 30)], smooth=False)
    art = G(art, shade, "#6e4628", "#4a2e1a", seed=nx(), density=0.9, edge=0.35, bloom=0.25, rough=4)
    art = G(art, shade * np.clip((np.arange(H)[:, None] - inner_top) / (H * 0.36), 0, 1), "#c08a52", seed=nx(), density=0.4, edge=0, bloom=0.3, rough=3)
    # warm lamp glows inside
    lamps = [(cx - 110, inner_top + 60), (cx, inner_top + 50), (cx + 110, inner_top + 60)]
    for (lx, ly) in lamps:
        art = over(art, glow(circles(W, H, [(lx, ly + 18, 14)]), "#ffd88a", 14, 2.6))
    # columns: outer saka + taller soko guru
    cols = []
    for i in range(9):
        x = cx - W * 0.32 + i * (W * 0.64 / 8)
        cols.append(([(x, inner_top + 8), (x, gy - 30)], 7, None))
    for x in (cx - 70, cx + 70):
        cols.append(([(x, inner_top + 8), (x, gy - 30)], 10, None))
    cm = strokes(W, H, cols)
    art = GP(art, cm, "#8a5a32", "#6a4224", seed=nx(), rough=0.8, streak=1.0)
    art = G(art, cm * np.clip((np.arange(W)[None, :] % 80) / 80.0, 0, 1) * 0 + strokes(W, H, [([(c[0][0][0] + 2.5, c[0][0][1]), (c[0][1][0] + 2.5, c[0][1][1])], 2.5, None) for c in cols]), "#3a2416", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    # umpak stone bases
    art = G(art, shapes(W, H, [rect(c[0][0][0] - 8, gy - 40, c[0][0][0] + 8, gy - 30) for c in cols], smooth=False), "#cfc0a4", "#b09a7a", seed=nx(), density=0.75, edge=0.5, bloom=0, rough=1)
    # lamp bodies (hanging robyong)
    for (lx, ly) in lamps:
        art = G(art, strokes(W, H, [([(lx, inner_top), (lx, ly + 8)], 1.2, None)]), INK, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)
        lm = shapes(W, H, [[(lx - 8, ly + 8), (lx + 8, ly + 8), (lx + 5, ly + 26), (lx - 5, ly + 26)]], smooth=False)
        art = G(art, lm, "#e8b860", "#c48a3e", seed=nx(), density=0.85, edge=0.5, bloom=0, rough=0.8)
    # roof tiers: penitih (lowest, widest), penanggap, brunjung (steep top)
    eave = inner_top + 6
    tiers = [
        [(cx - W * 0.47, eave + 8), (cx + W * 0.47, eave + 8), (cx + W * 0.3, eave - 40), (cx - W * 0.3, eave - 40)],
        [(cx - W * 0.33, eave - 34), (cx + W * 0.33, eave - 34), (cx + W * 0.16, eave - 92), (cx - W * 0.16, eave - 92)],
        [(cx - W * 0.17, eave - 88), (cx + W * 0.17, eave - 88), (cx + W * 0.045, eave - 190), (cx - W * 0.045, eave - 190)],
    ]
    for k, t in enumerate(tiers):
        tm = shapes(W, H, [t], smooth=False)
        art = G(art, tm, ["#7c5a3e", "#6a4a32", "#5a3c28"][k], "#4a3020", seed=nx(), density=0.8, edge=0.55, bloom=0.35, rough=2.5)
        # sirap shingle hatching
        y0, y1 = t[2][1], t[0][1]
        rows = [([(cx - W * 0.5, y), (cx + W * 0.5, y)], 1.0, None) for y in np.arange(y0 + 4, y1, 6)]
        art = G(art, strokes(W, H, rows) * tm, INK, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6, feather=0.4)
        # ink outline of the tier, a little broken
        ol = strokes(W, H, [(t + [t[0]], 1.6, None)]) * (fbm(W, H, nx(), 12, 2) > 0.3)
        art = G(art, ol, INK, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.6, feather=0.4)
    # ridge (mustaka) ornaments
    ry = eave - 190
    art = G(art, strokes(W, H, [([(cx - W * 0.045, ry), (cx + W * 0.045, ry)], 4, None)] + [([(x, ry), (x, ry - 12)], 2.4, (0.0, 0.7)) for x in (cx - W * 0.045, cx + W * 0.045)]), INK, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.5)
    # ink linework on columns and plinth
    art = G(art, strokes(W, H, [([(cx - W * 0.36, gy - 30), (cx + W * 0.36, gy - 30)], 1.6, None), ([(cx - W * 0.36, gy), (cx + W * 0.36, gy)], 1.4, None)]), INK, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.5)
    art = G(art, strokes(W, H, [([(cx - W * 0.33, inner_top + 8), (cx + W * 0.33, inner_top + 8)], 5, None)]), "#5a3820", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.8)
    art = add_grain(art, 3, 0.03)
    preview(art, "ss-pendopo", tone="#f4e8d2")
    save(art, f"{OUT}/pendopo.webp", max_w=640, quality=76)


def divider():
    """Canting line: a row of ukel curls and cecek leading to a small kupu, in soga brown wax-line style."""
    W, H = 420, 64
    nx = Seq(1300)
    cx, cy = W / 2, H / 2
    items = []
    dots = []
    for d in (-1, 1):
        items.append(([(cx + d * 40, cy), (cx + d * 196, cy)], 1.8, (0.05, 0.4)))
        for k in range(5):
            x = cx + d * (60 + k * 28)
            items.append((ukel(x, cy - 8, 6, math.pi / 2, d, 1.0), 1.8, (0.0, 0.5)))
            items.append((ukel(x + d * 14, cy + 8, 5, -math.pi / 2, -d, 1.0), 1.6, (0.0, 0.5)))
            dots += [(x + d * 7, cy - 14, 1.6), (x + d * 7, cy + 14, 1.6)]
    wings, body, lines, kd = kupu_geo(cx, cy + 2, 0.55)
    items += [(p + [p[0]], 1.8, None) for p in wings] + [(a, w * 0.8, t) for a, w, t in lines]
    m = np.maximum.reduce([strokes(W, H, items), circles(W, H, dots + [(x, y, 1.2) for x, y in kd]), shapes(W, H, [body])])
    art = G(blank(W, H), shapes(W, H, wings), SOGA_L, seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=1.5)
    art = G(art, m, SOGA_D, SOGA, seed=nx(), density=0.95, edge=0.4, bloom=0, rough=0.8, feather=0.6)
    preview(art, "ss-divider", tone="#f4e8d2")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
