"""Sumbawa Samawa — gouache: Istana Dalam Loka (the long timber palace on rows of stilts, twin gables under one great
shingled roof, the front ramp) on golden savanna with the Moyo island blues behind; kre alang songket woven thread by
thread (maroon/black silk ground, gold supplementary weft: pucuk rebung teeth, lonto engal diamonds), a woven songket
border band and a diamond medallion with frayed edges. Run: python3 -I sumbawa-samawa.py [part ...]
parts: istana kre band medal    Assets -> public/themes/art/sumbawa-samawa/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c1_lib import *

OUT = outdir("sumbawa-samawa")
PARTS = sys.argv[1:] or ["istana", "kre", "band", "medal"]
MAROON, BLACK, GOLD, TEAL, CREAM = "#6e1424", "#24090d", "#d4a640", "#1f6f6a", "#efe2c4"
WOOD, WOOD_D, WOOD_L = "#5e3a22", "#2f1b10", "#8c5a35"
ROOF, ROOF_D = "#4a3a34", "#2a201e"
SAV, SAV_D, SAV_L = "#d8b25a", "#a7833a", "#f0d48a"
SEA, SEA_D, MOYO = "#3f86b8", "#245d8e", "#5f8fb0"


def palace(art, W, H, cx, by, s, rng, nx):
    """Istana Dalam Loka seen at three-quarter front: long body on stilts, two gables side by side, a ramp at front-left."""
    def P(u, v):
        return (cx + u * s, by + v * s)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # under-floor shadow + stilts (many rows)
    under = shapes(W, H, [[P(-1.5, -0.02), P(1.5, -0.02), P(1.5, -0.5), P(-1.5, -0.5)]], smooth=False)
    art = wash(art, under, "#3a2a1a", 0.55, seed=nx())
    st = []
    for row, (dy, w) in enumerate([(-0.04, 0.032), (-0.1, 0.026)]):
        for u in np.linspace(-1.45, 1.45, 13 if row == 0 else 12):
            st.append(([P(u + row * 0.1, dy + 0.02), P(u + row * 0.1, -0.52)], s * w, None))
    stm = strokes(W, H, st)
    art = GP(art, stm, WOOD_D, "#3d2414", seed=nx(), rough=0.6)
    art = wash(art, stm * grad(W, H, cx - s * 1.5, 0, cx + s * 1.5, 0), "#1a0e08", 0.35, seed=nx())
    # floor beam
    beam = shapes(W, H, [[P(-1.58, -0.5), P(1.58, -0.5), P(1.58, -0.58), P(-1.58, -0.58)]], smooth=False)
    art = GP(art, beam, WOOD_D, seed=nx(), rough=0.6)
    # walls: vertical planks, a row of tall shuttered windows
    wall = shapes(W, H, [[P(-1.5, -0.58), P(1.5, -0.58), P(1.5, -1.12), P(-1.5, -1.12)]], smooth=False)
    art = GP(art, wall, WOOD, "#6a4228", seed=nx(), rough=1.0, streak=1.0)
    seams = np.clip((np.abs(((xx - cx) / (s * 0.06)) % 1.0 - 0.5) * 2 - 0.86) * 7, 0, 1) * wall
    art = wash(art, seams, WOOD_D, 0.55, seed=nx())
    art = wash(art, wall * grad(W, H, cx - s * 1.5, 0, cx + s * 1.5, 0), "#2a170c", 0.4, seed=nx())
    art = wash(art, wall * (1 - grad(W, H, cx - s * 1.5, 0, cx, 0)), WOOD_L, 0.35, seed=nx())
    wins = [[P(u - 0.07, -0.66), P(u + 0.07, -0.66), P(u + 0.07, -1.0), P(u - 0.07, -1.0)] for u in np.linspace(-1.25, 1.25, 9)]
    wm = shapes(W, H, wins, smooth=False)
    art = GP(art, wm, "#2a1810", seed=nx(), rough=0.5)
    shut = shapes(W, H, [[P(u - 0.07, -0.66), P(u - 0.01, -0.66), P(u - 0.01, -1.0), P(u - 0.07, -1.0)] for u in np.linspace(-1.25, 1.25, 9)], smooth=False)
    art = GP(art, shut, "#7a4c2c", seed=nx(), rough=0.5)
    rail = strokes(W, H, [([P(-1.5, -0.62), P(1.5, -0.62)], s * 0.018, None)])
    art = GP(art, rail, "#c9a35a", seed=nx(), rough=0.4)
    # roof: one great hipped roof broken into twin gables at the front
    roof = shapes(W, H, [[P(-1.75, -1.08), P(-1.05, -1.95), P(1.05, -1.95), P(1.75, -1.08), P(1.6, -1.02), P(-1.6, -1.02)]], smooth=False)
    art = GP(art, roof, ROOF, "#5a4840", seed=nx(), rough=1.2, streak=1.2)
    rows = np.clip((np.abs(((yy - by) / (s * 0.055)) % 1.0 - 0.5) * 2 - 0.8) * 5, 0, 1) * roof
    art = wash(art, rows, ROOF_D, 0.45, seed=nx())
    art = wash(art, roof * grad(W, H, cx, by - s * 1.95, cx, by - s * 1.0), ROOF_D, 0.3, seed=nx())
    for gx in (-0.55, 0.55):
        gable = shapes(W, H, [[P(gx - 0.5, -1.1), P(gx, -2.12), P(gx + 0.5, -1.1)]], smooth=False)
        art = knockout(art, gable, 1.0, 0.6)
        art = GP(art, gable, "#6a4228", WOOD, seed=nx(), rough=0.8, streak=0.8)
        gs = np.clip((np.abs(((xx - cx) / (s * 0.05)) % 1.0 - 0.5) * 2 - 0.84) * 7, 0, 1) * gable
        art = wash(art, gs, WOOD_D, 0.5, seed=nx())
        tri = shapes(W, H, [[P(gx - 0.18, -1.36), P(gx, -1.72), P(gx + 0.18, -1.36)]], smooth=False)
        art = GP(art, tri, "#c9a35a", "#a98440", seed=nx(), rough=0.5)
        barge = strokes(W, H, [([P(gx - 0.56, -1.06), P(gx, -2.14), P(gx + 0.56, -1.06)], s * 0.05, None)])
        art = GP(art, barge, ROOF_D, seed=nx(), rough=0.5)
        horns = strokes(W, H, [(curve([P(gx, -2.12), P(gx - 0.1, -2.26), P(gx - 0.2, -2.3)], 10), s * 0.03, (0.0, 0.7)), (curve([P(gx, -2.12), P(gx + 0.1, -2.26), P(gx + 0.2, -2.3)], 10), s * 0.03, (0.0, 0.7))])
        art = GP(art, horns, ROOF_D, seed=nx(), rough=0.4)
    eave = strokes(W, H, [([P(-1.76, -1.07), P(1.76, -1.07)], s * 0.04, None)])
    art = GP(art, eave, ROOF_D, seed=nx(), rough=0.5)
    # ramp (tangga) at the front-left
    ramp = shapes(W, H, [[P(-1.2, -0.56), P(-0.95, -0.56), P(-0.3, 0.12), P(-0.62, 0.12)]], smooth=False)
    art = GP(art, ramp, "#7a5030", "#6a4428", seed=nx(), rough=0.6)
    slats = np.clip((np.abs(((yy - by) / (s * 0.05)) % 1.0 - 0.5) * 2 - 0.8) * 5, 0, 1) * ramp
    art = wash(art, slats, WOOD_D, 0.5, seed=nx())
    rr = strokes(W, H, [([P(-1.22, -0.72), P(-0.64, 0.0)], s * 0.018, None), ([P(-0.97, -0.72), P(-0.32, 0.0)], s * 0.018, None)])
    art = GP(art, rr, WOOD_D, seed=nx(), rough=0.4)
    return art


if "istana" in PARTS:
    W, H = 860, 640
    nx = Seq(100)
    rng = random.Random(31)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = blank(W, H)
    HZ = 280
    art[:HZ + 4] = painted_sky(W, HZ + 4, [(0, "#7fb1d8"), (0.75, "#c6dcea"), (1.0, "#f1e6cc")], seed=nx())
    for cy_, x0, x1 in [(80, 40, 360), (130, 500, 820)]:
        cl = shapes(W, H, [deform(ellipse_pts((x0 + x1) / 2, cy_, (x1 - x0) / 2, 20, 18), rng, 2, 0.08)])
        art = wash(art, gaussian_filter(cl, 4), "#ffffff", 0.7, seed=nx())
    # sea and Pulau Moyo on the horizon
    sea = ((yy >= HZ) & (yy < 360)).astype(np.float32)
    art = wash(art, sea, SEA, 1.0, seed=nx(), col2="#4a92c0")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, 360), SEA_D, 0.4, seed=nx())
    gl = strokes(W, H, [([(x, y), (x + rng.uniform(10, 30), y)], 1.4, (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(HZ + 4, 350)) for _ in range(60)]]) * sea
    art = wash(art, gl, "#e8f3fa", 0.7, seed=nx())
    moyo = shapes(W, H, [deform([(420, HZ + 2), (500, HZ - 30), (600, HZ - 46), (720, HZ - 34), (820, HZ - 14), (880, HZ + 2)], rng, 2, 0.02)])
    art = GP(art, moyo, MOYO, "#527fa0", seed=nx(), rough=2.0)
    art = wash(art, moyo * grad(W, H, 0, HZ - 46, 0, HZ), "#a8c6da", 0.4, seed=nx())
    # savanna hills, three layers, golden with blue-green shadows
    for y0, amp, c1, c2, seedk in [(318, 40, "#8fa08a", "#7d9283", 1), (372, 46, "#bfa25a", "#ad9150", 2), (452, 34, "#e2bc62", SAV, 3)]:
        pts = [(-20, H + 20)] + [(x, y0 + math.sin(x / 140 + seedk) * amp * 0.6 + math.sin(x / 61 + seedk * 2) * amp * 0.3) for x in range(-20, W + 40, 30)] + [(W + 20, H + 20)]
        hill = shapes(W, H, [pts])
        art = GP(art, hill, c1, c2, seed=nx(), rough=2.5, streak=1.0)
        art = wash(art, hill * np.clip((fbm(W, H, nx(), 40, 3) - 0.5) * 2.5, 0, 1), "#8a7a4a", 0.25, seed=nx())
        gm = grass_tufts(W, H, y0 - 10, y0 + 120, int(W / 5), rng, 6, 18, 0.25, 1.4) * hill
        art = wash(art, gm, SAV_D, 0.45, seed=nx())
        art = wash(art, grass_tufts(W, H, y0 - 10, y0 + 120, int(W / 7), rng, 6, 16, 0.2, 1.2) * hill, SAV_L, 0.5, seed=nx())
    # lontar palms on the savanna
    for px, ph, by_ in [(80, 190, 500), (160, 130, 470), (790, 170, 490), (700, 90, 430)]:
        trunk = strokes(W, H, [([(px, by_), (px + 4, by_ - ph)], max(4, ph * 0.04), (0.0, 0.3))])
        art = GP(art, trunk, "#5a4632", seed=nx(), rough=0.5)
        tx, ty = px + 4, by_ - ph
        R = ph * 0.26
        fans = []
        for a in np.linspace(-math.pi * 1.05, math.pi * 0.05, 16):
            ex, ey = tx + math.cos(a) * R, ty + math.sin(a) * R * 0.8 + R * 0.25 * (math.sin(a) > -0.3)
            fans.append(deform([(tx, ty), (ex + math.cos(a + 1.3) * R * 0.32, ey + math.sin(a + 1.3) * R * 0.32), (ex + math.cos(a) * R * 0.12, ey + math.sin(a) * R * 0.12), (ex + math.cos(a - 1.3) * R * 0.32, ey + math.sin(a - 1.3) * R * 0.32)], rng, 1, 0.05))
        fm = shapes(W, H, fans, smooth=False)
        art = GP(art, fm, "#4f6a3a", "#5f7a42", seed=nx(), rough=1.4)
        art = wash(art, fm * grad(W, H, tx - R, ty - R, tx + R, ty + R), "#2e4426", 0.45, seed=nx())
        dead = strokes(W, H, [([(tx, ty + 4), (tx + math.cos(a) * R * 0.7, ty + R * 0.9)], 4, (0.1, 0.5)) for a in (-2.2, -1.6, -1.0)])
        art = GP(art, dead, "#8a6a3a", seed=nx(), rough=0.6)
    shadow = shapes(W, H, [ellipse_pts(500, 528, 290, 26, 30)])
    art = wash(art, gaussian_filter(shadow, 8), "#6a5428", 0.5, seed=nx())
    art = palace(art, W, H, 450, 520, 150, rng, nx)
    # foreground grass over the stilts' feet
    fg = grass_tufts(W, H, 520, 640, 520, rng, 14, 46, 0.2, 2.2)
    art = GP(art, fg, "#c9a350", "#e0bd66", seed=nx(), rough=0.8)
    art = wash(art, grass_tufts(W, H, 540, 640, 240, rng, 16, 40, 0.3, 2.0), SAV_D, 0.6, seed=nx())
    art = fade_edges(art, top=60)
    save(art, f"{OUT}/istana.webp", max_w=720, quality=76)
    show(art, "ss-istana")
    clear()


def kre_pattern(rows, cols):
    """Cell pattern for one repeat of kre alang: gold teeth bands top/bottom, lonto engal diamonds in the field."""
    p = np.zeros((rows, cols), np.int32)
    yy, xx = np.mgrid[0:rows, 0:cols]
    # black bands with gold pucuk rebung (triangle teeth)
    p[:7] = 1; p[rows - 7:] = 1
    tooth = (np.abs((xx % 10) - 4.5) <= (6 - yy) * 0.9) & (yy < 6) & (yy >= 1)
    p[tooth] = 2
    tooth2 = (np.abs((xx % 10) - 4.5) <= (yy - (rows - 7)) * 0.9) & (yy > rows - 7) & (yy < rows - 1)
    p[tooth2] = 2
    p[7] = 2; p[rows - 8] = 2
    # field: lonto engal — diamond flower of concentric rings, small cross-flowers between
    cy, cx = rows // 2, cols // 2
    d = np.abs(yy - cy) + np.abs(xx - cx)
    field = (yy > 8) & (yy < rows - 9)
    p[field & (d == 15)] = 2; p[field & (d == 12)] = 2
    p[field & (d <= 9) & (d >= 8)] = 2
    p[field & (d <= 5) & (d >= 4)] = 3
    p[field & (d <= 2)] = 2
    p[field & (d == 0)] = 4
    # petals on the diamond axes
    for dy, dx in [(-11, 0), (11, 0), (0, -11), (0, 11)]:
        dd = np.abs(yy - (cy + dy)) + np.abs(xx - (cx + dx))
        p[field & (dd <= 1)] = 4
    # corner quarter flowers (complete across tiles)
    for oy, ox in [(cy, 0), (cy, cols)]:
        dd = np.abs(yy - oy) + np.abs(xx - ox)
        p[field & (dd <= 6) & (dd >= 5)] = 2
        p[field & (dd <= 2)] = 3
    return p


if "kre" in PARTS:
    pat = kre_pattern(56, 40)
    pal = [MAROON, BLACK, GOLD, TEAL, CREAM]
    tile = weave_cells(pat, pal, cell=5, seed=3, metallic=(2,), float_len=3, fibre=0.07)
    save_rgb(tile, f"{OUT}/kre.webp", quality=82)
    show(tile, "ss-kre")
    big = np.concatenate([np.concatenate([tile, tile], 1)] * 2, 0)
    show(big, "ss-kre-2x2")
    clear()

if "band" in PARTS:
    # a woven border strip (tumpal teeth between gold lines) with a slightly frayed, uneven selvedge
    rows, cols = 12, 96
    p = np.ones((rows, cols), np.int32)
    yy, xx = np.mgrid[0:rows, 0:cols]
    p[1] = 2; p[rows - 2] = 2
    tooth = (np.abs((xx % 8) - 3.5) <= (yy - 2) * 0.75) & (yy >= 3) & (yy <= rows - 4)
    p[tooth] = 2
    p[(yy == rows // 2) & (xx % 8 == 4)] = 4
    cloth = weave_cells(p, [MAROON, BLACK, GOLD, TEAL, CREAM], cell=4, seed=7, metallic=(2,), float_len=3)
    h, w = cloth.shape[:2]
    m = np.ones((h, w), np.float32)
    fr = np.tile(fbm(w // 2, h, 5, 6, 2), (1, 2))
    m *= np.clip((np.minimum(np.arange(h)[:, None], h - 1 - np.arange(h)[:, None]) + fr * 2.5 - 0.6) / 1.2, 0, 1)
    cloth[..., 3] = m
    save_full(cloth, f"{OUT}/band.webp", quality=84)
    show(cloth, "ss-band")
    clear()

if "medal" in PARTS:
    n = 33
    p = np.zeros((n, n), np.int32)
    yy, xx = np.mgrid[0:n, 0:n]
    d = np.abs(yy - n // 2) + np.abs(xx - n // 2)
    p[:] = 0
    p[d >= 15] = 1
    p[(d == 13) | (d == 10)] = 2
    p[(d <= 7) & (d >= 6)] = 2
    p[(d <= 4) & (d >= 3)] = 3
    p[d <= 1] = 2
    p[d == 0] = 4
    cloth = weave_cells(p, [MAROON, BLACK, GOLD, TEAL, CREAM], cell=6, seed=9, metallic=(2,), float_len=3)
    h, w = cloth.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dd = np.abs(yy - h / 2) + np.abs(xx - w / 2)
    edge = h / 2 - 2 + (fbm(w, h, 3, 4, 2) - 0.5) * 6
    a = np.clip((edge - dd) / 1.5, 0, 1)
    # fringe: loose weft ends at the four tips
    cloth[..., 3] = a
    sh = soft_shadow(a, "#1a0a0a", 4, 0.45, 3, 5)
    out = over(sh, cloth)
    save(out, f"{OUT}/medal.webp", max_w=160, quality=84)
    show(out, "ss-medal")
    clear()
