"""Banda Neira — the bay of Banda seen from a perkenier verandah: the cone of Gunung Api across blue water, a kora-kora
with raised oars and pennants (watercolour + gouache), white Tuscan columns, an old white perkenier house with green
shutters, a nutmeg branch with a fruit split open on scarlet mace. Original designs, no figures.
Run: python3 -I banda-neira.py [part ...]   parts: view column house nutmeg divider kora
Assets -> public/themes/art/banda-neira/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k2_lib import *

OUT = outdir("banda-neira")
PARTS = sys.argv[1:] or ["view", "column", "house", "nutmeg", "divider", "kora"]
LIME, LIME_D = "#f8f4ea", "#e2dccd"
BAY, BAY_D, BAY_L = "#2f6690", "#1b3f61", "#6fa3c4"
MACE, MACE_D = "#cf2f25", "#8f1d17"
LEAF, LEAF_D, LEAF_L = "#4c7a43", "#2b4a2a", "#86a65e"
HUSK, HUSK_D = "#e8b456", "#c07a32"
SHUTTER, SHUTTER_D = "#4f7a5a", "#2f5240"


def nut_leaf(art, W, H, x, y, L, ang, rng, nx):
    pts = deform(petal_pts(x, y, L, L * 0.3, ang, n=14, cup=0.04), rng, 1, 0.04)
    m = shape_mask(W, H, pts)
    art = G(art, m, LEAF_L, LEAF, seed=nx(), density=0.88, edge=0.7, bloom=0.3, rough=2.0, pad=10)
    half = shape_mask(W, H, [(x, y)] + pts[: len(pts) // 2])
    art = G(art, half * m, LEAF_D, seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=1.5, pad=10)
    vein = strokes(W, H, [(curve([(x, y), (x + math.cos(ang) * L * 0.92, y + math.sin(ang) * L * 0.92)], 10), max(1.0, L * 0.012), (0.0, 0.6))])
    return G(art, vein, "#dfe0b0", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)


def nutmeg_fruit(art, W, H, cx, cy, r, rng, nx, split=True, rot=0.15):
    """Pear-round apricot husk; when split, the seam gapes to show the dark seed laced with scarlet mace."""
    fruit = shape_mask(W, H, deform([(cx + math.cos(t) * r * (1.0 + 0.06 * math.sin(t)), cy + math.sin(t) * r * (1.05 - 0.08 * math.cos(t + 1.6))) for t in [i / 24 * math.tau for i in range(24)]], rng, 1, 0.02))
    art = GP(art, fruit, "#f0c467", "#e3a74c", seed=nx(), rough=1.2, streak=0.6)
    art = G(art, fruit, "#f4cf78", HUSK, seed=nx(), density=0.95, edge=0.6, bloom=0.3, rough=1.6)
    yy, xx = grid(W, H)
    art = G(art, fruit * np.clip(((xx - cx) * 0.5 + (yy - cy) * 0.85) / (r * 1.1), 0, 1), HUSK_D, "#9e6a33", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=2)
    art = OV(art, gaussian_filter(circles(W, H, [(cx - r * 0.4, cy - r * 0.42, r * 0.26)]), r * 0.1) * fruit * 0.7, lambda m: tint(m, "#fcf1d2", 0.9))
    if split:
        sx = cx + r * 0.12
        lens = []
        for side in (1, -1):
            ts = [i / 20 for i in range(21)] if side > 0 else [1 - i / 20 for i in range(21)]
            for t in ts:
                lens.append((sx + side * r * 0.42 * math.sin(t * math.pi) ** 0.9 + rot * (t - 0.5) * r, cy - r * 0.9 + r * 1.8 * t))
        lm = shape_mask(W, H, lens)
        art = GP(art, lm, "#fbf0d8", "#ecd8b0", seed=nx(), rough=0.8)
        inner = shape_mask(W, H, [(sx + (x - sx) * 0.76, cy + (y - cy) * 0.86) for x, y in lens])
        art = GP(art, inner, "#5a2e18", "#341a0c", seed=nx(), rough=0.6, streak=0.4)
        lace = []
        for k in range(6):
            x0 = sx + (k - 2.5) * r * 0.09
            pts = [(x0 + math.sin(t * 8 + k * 1.4) * r * 0.08 + rot * (t - 0.5) * r * 0.8, cy - r * 0.72 + r * 1.44 * t) for t in [i / 40 for i in range(41)]]
            lace.append((pts, r * rng.uniform(0.05, 0.075), (0.25, 0.25)))
            for _ in range(3):
                bx, by = pts[int(rng.uniform(0.15, 0.85) * 40)]
                lace.append(([(bx, by), (bx + rng.uniform(-1, 1) * r * 0.12, by + rng.uniform(0.05, 0.14) * r)], r * 0.04, (0.2, 0.6)))
        art = GP(art, strokes(W, H, lace) * inner, "#e8392a", "#b8261a", seed=nx(), rough=0.5, streak=0.4)
        art = OV(art, gaussian_filter(circles(W, H, [(sx - r * 0.05, cy - r * 0.35, r * 0.07)]), 2) * inner * 0.6, lambda m: tint(m, "#ffd2bf", 0.8))
    art = G(art, edge_of(fruit, 2.5), "#a3692f", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=1, feather=0.8)
    return art


if "nutmeg" in PARTS:
    W, H = 620, 560
    nx = Seq(52100); rng = random.Random(52)
    art = blank(W, H)
    twig = curve([(20, 150), (160, 120), (300, 140), (430, 110), (600, 70)], 60)
    sub = curve([twig[30], (330, 210), (360, 270)], 20)
    sub2 = curve([twig[46], (470, 170), (480, 250)], 20)
    tw = strokes(W, H, [(twig, 9, (0.0, 0.7)), (sub, 5, (0.0, 0.3)), (sub2, 5, (0.0, 0.3))])
    art = G(art, tw, "#7a5a3c", "#4a3424", seed=nx(), density=0.9, edge=0.5, bloom=0.1, rough=1, feather=0.6)
    for (x, y), a, L in [(twig[8], -2.2, 170), (twig[14], 0.9, 190), (twig[24], -1.1, 180), (twig[38], -0.6, 170), (twig[52], 0.4, 150), (twig[20], 2.3, 150), (twig[56], -1.6, 130)]:
        art = nut_leaf(art, W, H, x, y, L, a, rng, nx)
    clear()
    art = nutmeg_fruit(art, W, H, 360, 360, 98, rng, nx, split=True)
    art = nutmeg_fruit(art, W, H, 492, 316, 64, rng, nx, split=False)
    st = strokes(W, H, [(curve([(360, 262), (358, 240), (352, 214)], 8), 6, None), (curve([(492, 252), (486, 240), (482, 238)], 6), 5, None)])
    art = G(art, st, "#6d5a3a", seed=nx(), density=0.9, edge=0.4, rough=0.6)
    show(art, "bn-nutmeg")
    save(art, f"{OUT}/nutmeg.webp", max_w=320, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 560, 110
    nx = Seq(52200); rng = random.Random(53)
    art = blank(W, H)
    for sgn in (-1, 1):
        pts = curve([(W / 2 + sgn * 34, 60), (W / 2 + sgn * 120, 52), (W / 2 + sgn * 200, 62), (W / 2 + sgn * 262, 54)], 40)
        art = G(art, strokes(W, H, [(pts, 3.4, (0.05, 0.8))]), "#7a5a3c", "#4a3424", seed=nx(), density=0.85, edge=0.5, rough=0.8, feather=0.6)
        for t, a in ((0.3, -0.5), (0.55, 0.5), (0.8, -0.4)):
            x, y = pts[int(t * 39)]
            art = nut_leaf(art, W, H, x, y, 46, (a if sgn > 0 else math.pi - a), rng, nx)
    art = nutmeg_fruit(art, W, H, W / 2, 58, 30, rng, nx, split=True)
    show(art, "bn-divider")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()


def cone_mask(W, H, px, py, base_y, half_w, rng, conc=1.45):
    L, R = [], []
    for i in range(41):
        t = i / 40
        hw = half_w * (t ** conc) + 12 * t
        yy_ = py + (base_y - py) * t
        L.append((px - hw * 0.97 + rng.uniform(-1.2, 1.2), yy_)); R.append((px + hw * 1.03 + rng.uniform(-1.2, 1.2), yy_))
    return shapes(W, H, [[(px - 16, py + 2), (px - 4, py - 3), (px + 6, py - 2), (px + 15, py + 3)] + R[2:] + L[::-1][:-2]], smooth=True)


def kora_kora(art, W, H, x0, x1, y, rng, nx, oars=14):
    """Long kora-kora hull with upswept ends, a striped canopy, raised oars and pennants."""
    L = x1 - x0
    top = [(x0 + L * t, y - (abs(t - 0.5) * 2) ** 4 * 34) for t in [i / 50 for i in range(51)]]
    bot = [(x0 + L * (0.06 + 0.88 * t), y + 16 * math.sin(t * math.pi) ** 0.6) for t in [i / 50 for i in range(51)]]
    hull = shapes(W, H, [top + bot[::-1]])
    art = over(art, soft_shadow(hull, "#16324e", blur=3, strength=0.3, dx=0, dy=5))
    art = GP(art, hull, "#7a3a24", "#4a2014", seed=nx(), rough=0.8, streak=0.8)
    band = strokes(W, H, [([(x, yy + 5) for x, yy in top[3:48]], 4.5, (0.05, 0.05))]) * hull
    art = GP(art, band, "#f2e6c8", seed=nx(), rough=0.5)
    zig = []
    for x, yy in top[4:47]:
        zig.append([(x, yy + 9), (x + L / 100, yy + 13), (x + L / 50, yy + 9)])
    art = GP(art, polys(W, H, zig) * hull, "#d8a23c", seed=nx(), rough=0.4)
    # oars raised in a fan, blades up
    om, bm = [], []
    for k in range(oars):
        t = 0.18 + 0.64 * k / (oars - 1)
        bx, by = x0 + L * t, y + 2
        a = -math.pi / 2 - 0.35 + 0.7 * (k / (oars - 1)) + rng.uniform(-0.04, 0.04)
        ex, ey = bx + math.cos(a) * 50, by + math.sin(a) * 50
        om.append(([(bx, by), (ex, ey)], 1.6, None))
        bm.append(deform(ellipse_pts(ex + math.cos(a) * 6, ey + math.sin(a) * 6, 3.2, 9, 8, a + math.pi / 2), rng, 1, 0.02))
    art = GP(art, strokes(W, H, om), "#5a3a22", seed=nx(), rough=0.3)
    art = GP(art, shapes(W, H, bm), "#e8d9b4", "#c89a58", seed=nx(), rough=0.3)
    # canopy (hut) amidships
    cx = x0 + L * 0.5
    can = polys(W, H, [[(cx - L * 0.12, y - 2), (cx - L * 0.1, y - 30), (cx + L * 0.1, y - 30), (cx + L * 0.12, y - 2)]])
    art = GP(art, can, "#efe2c4", "#d8c49c", seed=nx(), rough=0.6)
    stripes = polys(W, H, [rect(cx - L * 0.12 + i * L * 0.04, y - 30, cx - L * 0.12 + i * L * 0.04 + L * 0.02, y - 2) for i in range(6)]) * can
    art = GP(art, stripes, MACE, MACE_D, seed=nx(), rough=0.4)
    roof = polys(W, H, [[(cx - L * 0.13, y - 28), (cx, y - 42), (cx + L * 0.13, y - 28)]])
    art = GP(art, roof, "#2e5a3a", "#1d3d28", seed=nx(), rough=0.5)
    # pennant poles at bow and stern
    for px_, sgn in ((x0 + L * 0.04, -1), (x1 - L * 0.04, 1)):
        py_ = y - 34
        art = GP(art, strokes(W, H, [([(px_, py_ + 4), (px_, py_ - 52)], 2, None)]), "#4a3020", seed=nx(), rough=0.3)
        flag = shapes(W, H, [[(px_, py_ - 52), (px_ + sgn * 34, py_ - 46), (px_ + sgn * 22, py_ - 40), (px_ + sgn * 36, py_ - 33), (px_, py_ - 30)]])
        art = GP(art, flag, MACE if sgn > 0 else "#f2e6c8", MACE_D if sgn > 0 else "#d9c9a4", seed=nx(), rough=0.8)
    return art, hull


if "kora" in PARTS:
    W, H = 640, 200
    nx = Seq(52300); rng = random.Random(54)
    art = blank(W, H)
    art, hull = kora_kora(art, W, H, 30, 610, 140, rng, nx)
    # a little water line under it
    wl = strokes(W, H, [([(x, 160 + rng.uniform(-2, 2)), (x + rng.uniform(30, 70), 160)], 2.2, (0.3, 0.3)) for x in range(10, 600, 40)])
    art = G(art, wl, BAY_L, "#9cc3d8", seed=nx(), density=0.7, edge=0.2, rough=1, feather=0.6)
    show(art, "bn-kora", bg="#2f6690")
    save(art, f"{OUT}/kora.webp", max_w=360, quality=84)
    clear()

if "view" in PARTS:
    W, H = 780, 700
    nx = Seq(52400); rng = random.Random(55)
    yy, xx = grid(W, H)
    HZ = int(H * 0.62)
    art = painted_sky(W, H, [(0, "#a9cbe0"), (0.3, "#c9ddea"), (0.52, "#f0e2cc"), (0.62, "#f6dcb8"), (1, "#f6dcb8")], seed=7, streak=0.8)
    cl = strokes(W, H, [(curve([(x0, y0), (x0 + L * 0.5, y0 - 8), (x0 + L, y0)], 20), w_, (0.3, 0.3)) for x0, y0, L, w_ in
                        [(380, 90, 320, 20), (440, 130, 260, 12), (20, 190, 240, 14), (520, 230, 240, 9)]])
    art = G(art, cl, "#ffffff", "#e9eef2", seed=nx(), density=0.75, edge=0.3, bloom=0.5, rough=7, feather=3)
    clear()
    # Lonthor (Banda Besar) low ridge across the far right
    lon = shapes(W, H, [[(W * 0.48, HZ + 2), (W * 0.58, HZ - 34), (W * 0.72, HZ - 46), (W * 0.86, HZ - 38), (W + 10, HZ - 52), (W + 10, HZ + 2)]])
    art = G(art, lon, "#7d9aa6", "#6b8a91", seed=nx(), density=0.6, edge=0.4, bloom=0.3, rough=4)
    # Gunung Api: tall cone left of centre, bare upper slope, wooded foot, a thin plume
    px, py = W * 0.34, H * 0.15
    cone = cone_mask(W, H, px, py, HZ + 4, W * 0.42, rng, conc=1.25)
    art = G(art, cone, "#8f8a84", "#7b7570", seed=nx(), density=0.82, edge=0.5, bloom=0.35, rough=4)
    lower = cone * np.clip((yy - H * 0.36) / (H * 0.16), 0, 1)
    art = G(art, lower, "#5f7f56", "#456a45", seed=nx(), density=0.75, edge=0.25, bloom=0.5, rough=6)
    shade = cone * np.clip((xx - px - (yy - py) * 0.12) / 110, 0, 1)
    art = G(art, shade, "#4f5f6a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=4)
    gul = []
    for k in range(13):
        f = (k / 12 - 0.5) * 1.6 + rng.uniform(-0.05, 0.05)
        x1 = px + f * W * 0.45 + rng.uniform(-10, 10); y1 = HZ - rng.uniform(40, 140)
        st_ = rng.uniform(0.08, 0.3)
        pts = curve([(px + f * 7 + (x1 - px) * st_, py + 10 + (y1 - py) * st_), ((px + x1) / 2 + rng.uniform(-18, 18), (py + y1) / 2 + rng.uniform(0, 30)), (x1 + rng.uniform(-14, 14), y1)], 30)
        pts = [(x + rng.uniform(-1.5, 1.5), y) for x, y in pts]
        gul.append((pts, rng.uniform(1.8, 3.6), (0.3, 0.6)))
    fade = np.clip(1.1 - (yy - py) / (HZ - py), 0, 1)
    art = G(art, strokes(W, H, gul) * cone * fade, "#57534f", seed=nx(), density=0.4, edge=0.35, bloom=0.1, rough=2, feather=1)
    dab = []
    for _ in range(900):
        y = rng.uniform(H * 0.4, HZ); t = (y - py) / (HZ - py); hw = W * 0.42 * (t ** 1.45)
        dab.append((rng.uniform(px - hw, px + hw), y, rng.uniform(2.5, 5), rng.uniform(1.6, 3), rng.uniform(-20, 20)))
    art = G(art, ellipses(W, H, dab) * cone, "#3f633f", "#2f4f33", seed=nx(), density=0.3, edge=0.4, bloom=0, rough=1.2, feather=0.8)
    plume = strokes(W, H, [(curve([(px, py - 2), (px + 16, py - 34), (px + 60, py - 62), (px + 150, py - 76)], 30), 22, (0.15, 0.0))])
    art = G(art, gaussian_filter(plume, 4), "#f4f1ea", "#c9c6c0", seed=nx(), density=0.7, edge=0.2, bloom=0.5, rough=8, feather=3)
    haze = cone * np.clip((yy - (HZ - 60)) / 60, 0, 1)
    art = OV(art, gaussian_filter(haze, 3) * 0.4, lambda m: tint(m, "#e8dccb", 1.0))
    clear()
    # the bay
    sea = polys(W, H, [rect(-10, HZ, W + 10, H + 10)])
    art = GP(art, sea, "#4f88ad", BAY, seed=nx(), rough=1.2, streak=1.0)
    art = G(art, sea * np.clip((yy - HZ) / (H - HZ), 0, 1), BAY_D, "#173957", seed=nx(), density=0.55, edge=0.1, bloom=0.3, rough=3)
    refl = sea * np.clip(1 - (yy - HZ) / 110, 0, 1) * np.clip(1 - np.abs(xx - px) / (W * 0.34), 0, 1)
    art = G(art, refl, "#355f4a", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=3)
    sw = [([(x, y), (x + rng.uniform(26, 80), y + rng.uniform(-1, 1))], rng.uniform(1.4, 2.6), (0.3, 0.3)) for x, y in [(rng.uniform(-30, W), rng.uniform(HZ + 8, H)) for _ in range(90)]]
    art = OV(art, gaussian_filter(strokes(W, H, sw), 0.5) * sea, lambda m: tint(m, "#cfe3ee", 0.6))
    clear()
    art, _ = kora_kora(art, W, H, W * 0.52, W * 0.94, HZ + 92, rng, nx, oars=12)
    art = add_grain(art, 9, 0.03)
    show(art, "bn-view")
    save_full(art, f"{OUT}/view.webp", size=(780, 700), quality=78)
    clear()

if "column" in PARTS:
    # Tuscan verandah column, lime-washed, light from the left
    W, H = 160, 2200
    nx = Seq(52500); rng = random.Random(56)
    art = blank(W, H)
    cx = W / 2
    shaft = shapes(W, H, [[(cx - 36, 70), (cx + 36, 70), (cx + 42, H - 80), (cx - 42, H - 80)]], smooth=False)
    cap = polys(W, H, [rect(cx - 66, 10, cx + 66, 34), rect(cx - 52, 34, cx + 52, 52), rect(cx - 42, 52, cx + 42, 70)])
    base = polys(W, H, [rect(cx - 52, H - 82, cx + 52, H - 62), rect(cx - 64, H - 62, cx + 64, H - 30), rect(cx - 72, H - 30, cx + 72, H)])
    allm = np.maximum.reduce([shaft, cap, base])
    art = GP(art, allm, LIME, "#efe9dc", seed=nx(), rough=0.8, streak=1.0)
    yy, xx = grid(W, H)
    art = G(art, allm * np.clip((xx - cx + 6) / 46, 0, 1), "#a9b4c0", "#9aa6b5", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=1.5)
    art = G(art, allm * np.clip((cx - 26 - xx) / 14, 0, 1), "#d8d2c3", seed=nx(), density=0.3, edge=0.1, bloom=0.2, rough=1)
    lines = strokes(W, H, [([(cx - 66, 34), (cx + 66, 34)], 2, None), ([(cx - 52, 52), (cx + 52, 52)], 2, None), ([(cx - 42, 70), (cx + 42, 70)], 2.4, None),
                           ([(cx - 52, H - 62), (cx + 52, H - 62)], 2, None), ([(cx - 64, H - 30), (cx + 64, H - 30)], 2, None)])
    art = G(art, lines, "#8c95a0", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.6, feather=0.5)
    # weathering: soft stains and a hairline crack
    st = gaussian_filter((fbm(W, H, 77, 40, 3) > 0.7).astype(np.float32), 4) * allm
    art = G(art, st, "#cfc6b0", seed=nx(), density=0.25, edge=0.3, bloom=0.4, rough=3)
    crack = strokes(W, H, [(curve([(cx - 10, 900), (cx - 4, 1000), (cx - 12, 1080), (cx - 6, 1160)], 20), 1.1, (0.2, 0.4))])
    art = G(art, crack, "#8f8a7e", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
    show(art, "bn-column", bg="#2f6690")
    save(art, f"{OUT}/column.webp", max_w=90, quality=80)
    clear()

if "house" in PARTS:
    W, H = 760, 420
    nx = Seq(52600); rng = random.Random(57)
    art = blank(W, H)
    yy, xx = grid(W, H)
    GY = 360
    lawn = shapes(W, H, [[(-10, GY - 6), (W * 0.3, GY - 14), (W * 0.7, GY - 12), (W + 10, GY - 4), (W + 10, H), (-10, H)]])
    art = G(art, lawn, "#8aa65e", "#5c7f42", seed=nx(), density=0.85, edge=0.5, bloom=0.4, rough=4)
    art = G(art, lawn * np.clip((yy - GY) / 50, 0, 1), "#3f5f33", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=3)
    cx = W / 2
    # kenari trees behind
    for tx, ty, r in [(70, 170, 90), (690, 150, 100)]:
        cr = ellipses(W, H, [(tx + rng.gauss(0, r * 0.45), ty + rng.gauss(0, r * 0.3), rng.uniform(r * 0.3, r * 0.5), rng.uniform(r * 0.22, r * 0.36), rng.uniform(-30, 30)) for _ in range(24)])
        art = G(art, cr, "#6f9152", "#3e6237", seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=3)
        art = G(art, cr * np.clip((yy - ty) / r, 0, 1), "#2c4a2a", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=2)
        art = G(art, strokes(W, H, [([(tx, ty + 40), (tx + 4, GY - 8)], 12, None)]), "#6a5440", seed=nx(), density=0.9, edge=0.4, rough=1)
    clear()
    # house body: long verandah front
    body = polys(W, H, [rect(cx - 290, 196, cx + 290, GY - 22)])
    plinth = polys(W, H, [rect(cx - 304, GY - 26, cx + 304, GY)])
    steps = polys(W, H, [rect(cx - 50, GY - 26 + i * 8, cx + 50 + i * 0, GY - 18 + i * 8) for i in range(3)])
    art = over(art, soft_shadow(np.maximum(body, plinth), "#2d3d22", blur=6, strength=0.4, dx=8, dy=6))
    art = GP(art, body, LIME, "#ece6d8", seed=nx(), rough=1.0, streak=0.6)
    art = GP(art, plinth, "#ddd6c6", "#c9c1ae", seed=nx(), rough=0.8)
    art = GP(art, steps, "#e7e1d3", "#cfc7b5", seed=nx(), rough=0.5)
    # deep verandah shadow behind the columns
    ver = polys(W, H, [rect(cx - 280, 210, cx + 280, GY - 26)])
    art = G(art, ver, "#b8c2c9", "#a6b2bb", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=1.5)
    # tall windows with green louvred shutters, central double door
    win, sh = [], []
    for k in (-4, -3, -2, -1, 1, 2, 3, 4):
        x = cx + k * 62
        win.append(rect(x - 14, 232, x + 14, GY - 44))
        sh.append(rect(x - 27, 232, x - 14, GY - 44)); sh.append(rect(x + 14, 232, x + 27, GY - 44))
    art = GP(art, polys(W, H, win), "#3c4a52", "#28333a", seed=nx(), rough=0.4)
    shm = polys(W, H, sh)
    art = GP(art, shm, SHUTTER, SHUTTER_D, seed=nx(), rough=0.4, streak=0.4)
    lou = strokes(W, H, [([(0, y), (W, y)], 1.0, None) for y in range(236, GY - 44, 5)]) * shm
    art = G(art, lou, "#1f3a2c", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.3, feather=0.4)
    door = polys(W, H, [rect(cx - 24, 226, cx + 24, GY - 26)])
    art = GP(art, door, SHUTTER, SHUTTER_D, seed=nx(), rough=0.4)
    art = G(art, strokes(W, H, [([(cx, 228), (cx, GY - 28)], 1.6, None)]), "#1f3a2c", seed=nx(), density=0.6, rough=0.3)
    # columns
    cols = []
    for k in range(-5, 6):
        x = cx + k * 54 + (27 if k < 0 else -27 if k > 0 else 0)
        if k == 0:
            continue
        cols.append([(x - 7, 204), (x + 7, 204), (x + 8, GY - 26), (x - 8, GY - 26)])
    cm = polys(W, H, cols)
    art = GP(art, cm, "#fbf9f3", "#efebe2", seed=nx(), rough=0.5)
    csh = np.zeros((H, W), np.float32)
    for c in cols:
        csh = np.maximum(csh, polys(W, H, [[(c[1][0] - 4, c[1][1]), c[1], c[2], (c[2][0] - 4, c[2][1])]]))
    art = G(art, csh, "#a9b4c0", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5)
    # big hipped roof, dark weathered tiles
    roof = shapes(W, H, [[(cx - 320, 206), (cx - 230, 92), (cx + 230, 92), (cx + 320, 206)]], smooth=False)
    art = GP(art, roof, "#8c4a32", "#5e2f20", seed=nx(), rough=1.2, streak=1.0)
    art = G(art, roof * np.clip((xx - cx) / 300, 0, 1), "#3e1f16", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=2)
    courses = strokes(W, H, [([(0, y), (W, y)], 1.1, None) for y in range(98, 206, 7)]) * roof
    art = G(art, courses, "#3a1a10", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.4)
    eave = polys(W, H, [rect(cx - 322, 202, cx + 322, 210)])
    art = GP(art, eave, LIME, "#ddd6c6", seed=nx(), rough=0.4)
    for chx in (cx - 150, cx + 150):
        ch = polys(W, H, [rect(chx - 10, 70, chx + 10, 120)])
        art = GP(art, ch, "#efe9dc", "#d8d0bf", seed=nx(), rough=0.4)
    # flowering hedge along the plinth
    bush = ellipses(W, H, [(x + rng.gauss(0, 8), GY - 6 - rng.uniform(0, 12), rng.uniform(8, 14), rng.uniform(5, 8), rng.uniform(-40, 40)) for x in list(np.linspace(cx - 300, cx - 70, 14)) + list(np.linspace(cx + 70, cx + 300, 14))])
    art = G(art, bush, "#6f9152", "#355a33", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.5)
    fl = circles(W, H, [(rng.uniform(cx - 300, cx + 300), GY - rng.uniform(4, 18), rng.uniform(2.2, 3.4)) for _ in range(70)]) * gaussian_filter(bush, 2) * 2
    art = G(art, np.clip(fl, 0, 1), MACE, "#e46a52", seed=nx(), density=0.9, edge=0.3, rough=0.6)
    art = add_grain(art, 11, 0.03)
    show(art, "bn-house")
    save(art, f"{OUT}/house.webp", max_w=640, quality=80)
    clear()
