"""Khatulistiwa — Pontianak at noon on the equator: an original equator obelisk crowned by a gilded globe ring and
arrow, the wide Kapuas with speedboats and their wakes, Malay stilt houses on the far bank, corak insang cloth.
Gouache on warm paper. Run: python3 -I khatulistiwa.py [part ...]  parts: scene insang tugu divider rumah boat
Assets -> public/themes/art/khatulistiwa/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o4_lib import *

OUT = outdir("khatulistiwa")
PARTS = sys.argv[1:] or ["scene", "insang", "tugu", "divider", "rumah", "boat"]
CREAM = "#f4ead2"
TEAL, TEAL_D = "#1d5b5e", "#123c40"
RED, RED_D, RED_L = "#a8322b", "#6e1d1a", "#c8503c"
GOLD, GOLD_L, GOLD_D = "#d6a53a", "#f0d27a", "#946a1e"
STONE, STONE_D, STONE_L = "#efe7d8", "#b9ad98", "#fffaf0"
LEAF, LEAF_D, LEAF_L = "#4b7a4c", "#2c4f34", "#7ea566"
RIVER, RIVER_D, RIVER_L = "#7c9a8e", "#4d6e69", "#b9cfc4"


def monument(art, W, H, cx, by, h, nx, rng, gloss=True):
    """Original equator obelisk: stepped plinth, slender tapering shaft with a fluted face, a gilded globe with a tilted
    ring and an east-pointing arrow. Light from straight above (noon): lit top faces, shaded right face."""
    w0 = h * 0.075
    top_y = by - h * 0.78
    # plinth steps
    for k, (ww, hh) in enumerate([(0.36, 0.035), (0.28, 0.03), (0.2, 0.03)]):
        y1 = by - sum(x[1] for x in [(0.36, 0.035), (0.28, 0.03), (0.2, 0.03)][:k]) * h
        y0 = y1 - hh * h
        m = shapes(W, H, [rect(cx - ww * h / 2, y0, cx + ww * h / 2, y1)], smooth=False)
        art = GP(art, m, STONE, STONE_D, seed=nx(), rough=1.0, streak=0.6)
        sh = shapes(W, H, [rect(cx + ww * h * 0.22, y0, cx + ww * h / 2, y1)], smooth=False)
        art = OV(art, sh, lambda q: flat(q, "#8f846f", 0.35))
        art = OV(art, strokes(W, H, [([(cx - ww * h / 2, y0 + 1), (cx + ww * h / 2, y0 + 1)], 1.6, None)]), lambda q: flat(q, STONE_L, 0.9))
    base_y = by - 0.095 * h
    # shaft (two faces: lit left, shaded right)
    left = [(cx - w0, base_y), (cx, base_y), (cx, top_y), (cx - w0 * 0.45, top_y)]
    right = [(cx, base_y), (cx + w0, base_y), (cx + w0 * 0.45, top_y), (cx, top_y)]
    art = GP(art, shapes(W, H, [left], smooth=False), STONE_L, STONE, seed=nx(), rough=0.8, streak=0.3)
    art = GP(art, shapes(W, H, [right], smooth=False), "#c8bba2", "#b0a388", seed=nx(), rough=0.8, streak=0.3)
    fl = [([(cx - w0 * 0.5 * (1 - t) - w0 * 0.22 * t, base_y - 6), (cx - w0 * 0.24 * (1 - t) - w0 * 0.1 * t, top_y + 8)], 1.0, None) for t in (0.2, 0.6)]
    art = OV(art, strokes(W, H, fl), lambda q: flat(q, "#bfb29a", 0.7))
    art = OV(art, strokes(W, H, [([(cx, base_y), (cx, top_y)], 1.2, None)]), lambda q: flat(q, "#9a8e77", 0.6))
    # band of gold and a small capital
    cap = shapes(W, H, [rect(cx - w0 * 0.62, top_y - h * 0.018, cx + w0 * 0.62, top_y + 2)], smooth=False)
    art = FO(art, cap, GOLD, seed=nx(), emboss=0.8, sparkle=0.1)
    band = shapes(W, H, [rect(cx - w0 * 0.88, base_y - h * 0.05, cx + w0 * 0.88, base_y - h * 0.035)], smooth=False)
    art = FO(art, band, GOLD, seed=nx(), emboss=0.6, sparkle=0.1)
    # globe + ring + arrow
    gr = h * 0.085
    gy = top_y - h * 0.018 - gr * 0.95
    rod = strokes(W, H, [([(cx, top_y - h * 0.01), (cx, gy + gr * 0.6)], 3.0, None)])
    art = FO(art, rod, GOLD_D, seed=nx(), emboss=0.4)
    ring_back = path_mask(W, H, lambda p: p.addArc(skia.Rect(cx - gr * 1.45, gy - gr * 0.42, cx + gr * 1.45, gy + gr * 0.42), 180, 180), stroke=gr * 0.13)
    art = FO(art, ring_back, GOLD_D, seed=nx(), emboss=0.5)
    globe = circles(W, H, [(cx, gy, gr)])
    art = GP(art, globe, "#2e7a7a", TEAL_D, seed=nx(), rough=0.6, streak=0.5)
    # meridians and the equator line on the globe (gilt)
    mer = []
    for k in (-0.55, 0, 0.55):
        mer.append((arc_pts(cx + k * gr * 0.2, gy, gr * 0.98, -math.pi / 2, math.pi / 2, 20, 1.0) if k == 0 else
                    [(cx + k * gr * math.cos(t) * 0.95, gy + gr * math.sin(t) * 0.98) for t in np.linspace(-math.pi / 2, math.pi / 2, 20)], 1.4, None))
    mer.append(([(cx - gr * 0.98, gy), (cx + gr * 0.98, gy)], 2.2, None))
    art = FO(art, strokes(W, H, mer) * globe, GOLD_L, seed=nx(), emboss=0.3, sparkle=0.2)
    hl = circles(W, H, [(cx - gr * 0.35, gy - gr * 0.4, gr * 0.32)])
    art = OV(art, gaussian_filter(hl, 3) * globe, lambda q: flat(q, "#d6efe6", 0.45))
    art = OV(art, edge_ring(globe, 1.5), lambda q: flat(q, TEAL_D, 0.9))
    ring_front = path_mask(W, H, lambda p: p.addArc(skia.Rect(cx - gr * 1.45, gy - gr * 0.42, cx + gr * 1.45, gy + gr * 0.42), 0, 180), stroke=gr * 0.15)
    art = FO(art, ring_front, GOLD, seed=nx(), emboss=0.8, sparkle=0.25)
    arrow = strokes(W, H, [([(cx - gr * 1.9, gy - gr * 0.02), (cx + gr * 1.75, gy - gr * 0.02)], gr * 0.08, None)])
    head = shapes(W, H, [[(cx + gr * 1.65, gy - gr * 0.22), (cx + gr * 2.15, gy - gr * 0.02), (cx + gr * 1.65, gy + gr * 0.18)]], smooth=False)
    tail = shapes(W, H, [[(cx - gr * 1.95, gy - gr * 0.2), (cx - gr * 1.7, gy - gr * 0.02), (cx - gr * 1.95, gy + gr * 0.16), (cx - gr * 2.15, gy + gr * 0.16), (cx - gr * 1.9, gy - gr * 0.02), (cx - gr * 2.15, gy - gr * 0.2)]], smooth=False)
    art = FO(art, np.maximum(np.maximum(arrow, head), tail), GOLD, seed=nx(), emboss=0.8, sparkle=0.2)
    return art, gy, gr


def malay_house(art, W, H, x, by, w, nx, rng, wall=("#e9c46a", "#d4a548"), roof=("#8d3b2b", "#6a2a20"), trim=CREAM):
    """Rumah Melayu panggung: stilts, plank walls with louvred windows, a steep gable (perabung) with crossed ornamental
    finials and a fringed eave board, front stair. Returns art."""
    hh = w * 0.42
    floor = by - w * 0.22
    posts = [([(x + w * t, floor), (x + w * t + rng.uniform(-1, 1), by)], max(1.4, w * 0.022), None) for t in np.linspace(0.05, 0.95, 7)]
    art = GP(art, strokes(W, H, posts), "#5a3b26", "#3a2616", seed=nx(), rough=0.6)
    body = shapes(W, H, [rect(x, floor - hh, x + w, floor)], smooth=False)
    art = GP(art, body, wall[0], wall[1], seed=nx(), rough=0.8, streak=1.0)
    planks = strokes(W, H, [([(x + w * t, floor - hh), (x + w * t, floor)], 0.8, None) for t in np.linspace(0.04, 0.96, 18)]) * body
    art = OV(art, planks, lambda q: flat(q, "#7a5a2a", 0.25))
    for t in (0.14, 0.42, 0.7):
        win = shapes(W, H, [rect(x + w * t, floor - hh * 0.78, x + w * (t + 0.15), floor - hh * 0.2)], smooth=False)
        art = GP(art, win, "#3f2a1c", "#2a1a10", seed=nx(), rough=0.5)
        louv = strokes(W, H, [([(x + w * t, y), (x + w * (t + 0.15), y)], 0.9, None) for y in np.linspace(floor - hh * 0.74, floor - hh * 0.24, 5)])
        art = OV(art, louv * win, lambda q: flat(q, "#8a6238", 0.8))
        art = OV(art, strokes(W, H, [(rect(x + w * t, floor - hh * 0.78, x + w * (t + 0.15), floor - hh * 0.2) + [(x + w * t, floor - hh * 0.78)], 1.2, None)]), lambda q: flat(q, trim, 0.9))
    # eave shade
    art = OV(art, shapes(W, H, [rect(x, floor - hh, x + w, floor - hh * 0.82)], smooth=False), lambda q: flat(q, "#4a2e18", 0.35))
    # steep gable roof facing the river, with a slatted gable panel (tebar layar), fringed barge boards and crossed
    # finials (silang) at the apex
    ry = floor - hh
    apex = (x + w * 0.5, ry - w * 0.62)
    rf = shapes(W, H, [[(x - w * 0.1, ry + 4), apex, (x + w * 1.1, ry + 4)]], smooth=False)
    art = GP(art, rf, roof[0], roof[1], seed=nx(), rough=1.0, streak=0.6)
    panel = [(x + w * 0.1, ry - 1), (apex[0], apex[1] + w * 0.13), (x + w * 0.9, ry - 1)]
    pm_ = shapes(W, H, [panel], smooth=False)
    art = GP(art, pm_, wall[0], wall[1], seed=nx(), rough=0.6)
    sl = strokes(W, H, [([(x + w * t, ry), (x + w * t, apex[1])], 0.9, None) for t in np.linspace(0.18, 0.82, 11)]) * pm_
    art = OV(art, sl, lambda q: flat(q, "#6a4520", 0.5))
    art = OV(art, shapes(W, H, [[(apex[0] - w * 0.06, ry - w * 0.22), (apex[0], ry - w * 0.3), (apex[0] + w * 0.06, ry - w * 0.22), (apex[0], ry - w * 0.14)]], smooth=False), lambda q: flat(q, "#3f2a1c", 0.8))
    bb = []
    for (p0, p1) in [((x - w * 0.1, ry + 4), apex), (apex, (x + w * 1.1, ry + 4))]:
        bb.append(([p0, p1], 2.6, None))
        for t in np.linspace(0.06, 0.94, 12):
            px, py = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
            bb.append(([(px, py), (px, py + 5)], 1.3, None))
    art = OV(art, strokes(W, H, bb), lambda q: flat(q, trim, 0.95))
    art = OV(art, strokes(W, H, [([(x - w * 0.1, ry + 5), (x + w * 1.1, ry + 5)], 2.0, None)]), lambda q: flat(q, trim, 0.9))
    fin = strokes(W, H, [([(apex[0] - w * 0.02, apex[1] + w * 0.03), (apex[0] + w * 0.1, apex[1] - w * 0.1)], 2.2, None), ([(apex[0] + w * 0.02, apex[1] + w * 0.03), (apex[0] - w * 0.1, apex[1] - w * 0.1)], 2.2, None)])
    art = OV(art, fin, lambda q: flat(q, trim, 0.95))
    # stair
    st = strokes(W, H, [([(x + w * 0.46, floor), (x + w * 0.4, by)], 1.6, None), ([(x + w * 0.56, floor), (x + w * 0.5, by)], 1.6, None)] +
                 [([(x + w * 0.46 - 0.06 * w * t, floor + (by - floor) * t), (x + w * 0.56 - 0.06 * w * t, floor + (by - floor) * t)], 1.0, None) for t in (0.25, 0.5, 0.75)])
    art = OV(art, st, lambda q: flat(q, "#5a3b26", 0.95))
    return art


def speedboat(art, W, H, x, y, s, nx, d=1, hull="#f7f2e6", stripe=RED, canopy="#2e6f78"):
    """Small river speedboat with canopy, stripe, and a V-shaped wake trailing behind (d=1 heads right)."""
    def X(u):
        return x + d * u * s
    wake = strokes(W, H, [([(X(-0.2), y + s * 0.06), (X(-2.4), y - s * 0.12)], s * 0.05, (0.0, 0.9)), ([(X(-0.2), y + s * 0.1), (X(-2.6), y + s * 0.36)], s * 0.06, (0.0, 0.9)),
                          ([(X(-0.4), y + s * 0.09), (X(-1.6), y + s * 0.1)], s * 0.08, (0.0, 0.9))])
    foam = gaussian_filter(wake, s * 0.03) * np.clip(fbm(W, H, nx(), 5, 2) * 1.8 - 0.25, 0, 1)
    art = OV(art, gaussian_filter(wake, s * 0.06) * 0.35, lambda q: flat(q, "#e9f0e8", 1))
    art = OV(art, np.clip(foam * 1.4, 0, 1), lambda q: flat(q, "#fbfaf2", 0.9))
    hull_m = shapes(W, H, [[(X(-0.5), y - s * 0.02), (X(0.62), y - s * 0.04), (X(0.8), y - s * 0.12), (X(0.5), y + s * 0.13), (X(-0.45), y + s * 0.12)]], smooth=False)
    art = GP(art, hull_m, hull, "#e4ddcc", seed=nx(), rough=0.6)
    art = OV(art, strokes(W, H, [([(X(-0.45), y + s * 0.05), (X(0.62), y + s * 0.04)], s * 0.05, None)]) * hull_m, lambda q: flat(q, stripe, 0.95))
    can = shapes(W, H, [[(X(-0.35), y - s * 0.02), (X(-0.3), y - s * 0.28), (X(0.25), y - s * 0.3), (X(0.38), y - s * 0.03)]], smooth=False)
    art = GP(art, can, canopy, mix(canopy, "#000000", 0.25), seed=nx(), rough=0.5)
    art = OV(art, strokes(W, H, [([(X(-0.28), y - s * 0.2), (X(0.28), y - s * 0.21)], s * 0.05, None)]) * can, lambda q: flat(q, "#cfe7e4", 0.7))
    art = OV(art, strokes(W, H, [([(X(-0.5), y + s * 0.14), (X(0.5), y + s * 0.15)], s * 0.04, None)]), lambda q: flat(q, "#3b5754", 0.45))
    return art


def treeline(art, W, H, y, nx, rng, col=(LEAF, LEAF_D), amp=24):
    pts = [(-10, H)]
    for xx in range(-10, W + 20, 14):
        pts.append((xx, y - amp * (0.5 + 0.5 * math.sin(xx / 37 + rng.random())) - rng.uniform(0, amp * 0.4)))
    pts.append((W + 20, H))
    m = shapes(W, H, [pts])
    m = m * (np.arange(H)[:, None] < y + 30)
    art = GP(art, m.astype(np.float32), col[0], col[1], seed=nx(), rough=3, streak=0.8)
    return art


def scene():
    """Opaque cover painting 720x1240: cream noon sky (kept plain at top for text), the obelisk at right, far bank with
    nipah, palms and Malay houses, the wide Kapuas, two speedboats, a near jetty post."""
    W, H = 720, 1240
    rng = random.Random(11); nx = Seq(300)
    art = painted_sky(W, H, [(0, CREAM), (0.42, "#f2e6c8"), (0.6, "#dfe6d2"), (0.66, "#cfe0d6"), (1, "#cfe0d6")], seed=7, streak=0.2, grain=0.8)
    sun = circles(W, H, [(W * 0.76, 70, 34)])
    art = OV(art, glow(sun, "#fff4cf", 60, 0.6), lambda q: q, pad=0) if False else over(art, glow(sun, "#fff3c8", 70, 0.55))
    art = GP(art, sun, "#fff6d8", "#ffeebb", seed=nx(), rough=0.8)
    horizon = int(H * 0.665)
    # far bank: low trees, nipah palms, coconut palms, houses
    art = treeline(art, W, H, horizon - 4, nx, rng, ("#86a487", "#6f9077"), amp=18)
    for x in (40, 130, 470, 640):
        pm = palm(W, H, x, horizon + 4, rng.uniform(110, 150), rng, lean=rng.uniform(-0.15, 0.15))
        art = GP(art, pm, "#5f8a5e", "#4a7350", seed=nx(), rough=1.2, streak=0.8)
    art = treeline(art, W, H, horizon + 6, nx, rng, (LEAF, LEAF_D), amp=12)
    houses = [(20, 82, ("#e9c46a", "#d4a548"), ("#8d3b2b", "#6a2a20")), (118, 74, ("#8fb59a", "#6f9a7e"), ("#2f4a4a", "#203636")),
              (205, 88, ("#f1dfb8", "#d9c493"), ("#8d3b2b", "#6a2a20")), (430, 70, ("#e9c46a", "#d4a548"), ("#3d5550", "#2a3d3a")), (520, 80, ("#c9d9c0", "#a9c0a0"), ("#8d3b2b", "#6a2a20"))]
    for x, w, wall, roof in houses:
        art = malay_house(art, W, H, x, horizon + 18, w, nx, rng, wall, roof)
    clear()
    # river
    rv = shapes(W, H, [rect(0, horizon + 16, W, H)], smooth=False)
    art = GP(art, rv, RIVER, RIVER_D, seed=nx(), rough=1.0, streak=0.6)
    deep = rv * ramp_y(H, W, horizon + 20, H)
    art = OV(art, deep * 0.55, lambda q: flat(q, "#3f5e5b", 1))
    refl = []
    for k in range(70):
        yy = rng.uniform(horizon + 22, H - 20)
        xx = rng.uniform(-40, W)
        L = rng.uniform(20, 110) * (0.6 + (yy - horizon) / H)
        refl.append(([(xx, yy), (xx + L, yy + rng.uniform(-1, 1))], rng.uniform(1.2, 3.2), (0.3, 0.3)))
    art = OV(art, strokes(W, H, refl) * rv, lambda q: gouache_paint(q, RIVER_L, "#dbe6d8", seed=nx(), rough=1.0, streak=0.8, density=0.55))
    # house reflections (soft, broken)
    for x, w, wall, roof in houses:
        rm = shapes(W, H, [rect(x, horizon + 20, x + w, horizon + 20 + w * 0.5)], smooth=False) * np.clip(fbm(W, H, nx(), 6, 2) * 1.6 - 0.3, 0, 1)
        art = OV(art, gaussian_filter(rm, 1.2), lambda q: flat(q, wall[1], 0.35))
    clear()
    # obelisk on the near bank at right
    bank = shapes(W, H, [[(W * 0.5, H * 0.79), (W * 0.62, H * 0.765), (W + 10, H * 0.75), (W + 10, H * 0.86), (W * 0.5, H * 0.84)]])
    art = GP(art, bank, "#9c8a5e", "#7d6c45", seed=nx(), rough=2.0, streak=1.0)
    grass = shapes(W, H, [[(W * 0.52, H * 0.792), (W * 0.62, H * 0.768), (W + 10, H * 0.752), (W + 10, H * 0.79), (W * 0.52, H * 0.806)]])
    art = GP(art, grass, LEAF_L, LEAF, seed=nx(), rough=2.5, streak=1.0)
    art = OV(art, shapes(W, H, [[(W * 0.5, H * 0.84), (W + 10, H * 0.86), (W + 10, H * 0.88), (W * 0.5, H * 0.855)]]), lambda q: flat(q, "#3f5e5b", 0.6))
    art, gy, gr = monument(art, W, H, W * 0.8, H * 0.775, H * 0.66, nx, rng)
    clear()
    # speedboats
    art = speedboat(art, W, H, W * 0.3, H * 0.8, 92, nx, d=1)
    art = speedboat(art, W, H, W * 0.56, H * 0.705, 50, nx, d=-1, stripe="#2e6f78", canopy=RED)
    art = speedboat(art, W, H, W * 0.22, H * 0.93, 124, nx, d=-1, stripe=GOLD_D, canopy="#2e6f78")
    # equator hint: a dotted gilt line across the river
    preview(art, "kh-scene")
    save_rgb(art, f"{OUT}/scene.webp", quality=78)


def insang():
    """Seamless tenun corak insang tile (256x256): madder-red ground woven with gold weft rows of 'gill' arcs and
    small diamonds, framed by teal pick stripes."""
    W = H = 256
    rng = random.Random(4); nx = Seq(700)
    base = np.ones((H, W, 4), np.float32)
    base[..., :3] = col3(RED)
    # woven texture: horizontal and vertical threads
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = 0.5 + 0.25 * np.sin(yy * math.pi / 2) + 0.25 * np.sin(xx * math.pi / 2)
    wn = wrap_noise(W, H, 3, 6)
    base[..., :3] *= (0.86 + 0.14 * weave[..., None]) * (0.92 + 0.12 * wn[..., None])
    art = base
    # teal stripes at rows 0 and 128 (tileable)
    for y0 in (0, 128):
        st = shapes(W, H, [rect(-2, y0 + 2, W + 2, y0 + 12)], smooth=False)
        art = over(art, rgba(np.ones((H, W, 3)) * col3("#1f5e60") * (0.85 + 0.15 * weave[..., None]), st))
        st2 = shapes(W, H, [rect(-2, y0 + 14, W + 2, y0 + 16)], smooth=False)
        art = over(art, rgba(np.ones((H, W, 3)) * col3(GOLD), st2 * 0.9))
    # insang motif: rows of nested arcs (gills), alternating with small diamonds
    items = []
    for row, y in enumerate((44, 92, 172, 220)):
        off = 32 if row % 2 else 0
        for x in range(-64, W + 64, 64):
            cx = x + off
            for r in (16, 11, 6):
                items.append((arc_pts(cx, y + 10, r, math.pi * 1.1, math.pi * 1.9, 14), 2.2, None))
            items.append(([(cx - 18, y + 12), (cx + 18, y + 12)], 1.6, None))
    dia = []
    for y in (68, 196):
        for x in range(0, W + 32, 32):
            dia.append([(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)])
    gm = np.maximum(strokes(W, H, items, cap=False), shapes(W, H, dia, smooth=False))
    gm = np.clip(gm, 0, 1)
    thread = gm * (0.75 + 0.25 * np.sin(xx * math.pi / 1.5) ** 2)
    gold = np.ones((H, W, 3), np.float32) * col3(GOLD) * (0.85 + 0.3 * wn[..., None])
    art = over(art, rgba(gold, thread))
    hi = np.clip(gm - np.roll(gm, 1, 0), 0, 1)
    art = over(art, flat(hi, GOLD_L, 0.6))
    save_texture(art, f"{OUT}/insang.webp", quality=78)
    print("insang", os.path.getsize(f"{OUT}/insang.webp") // 1024, "KB")
    big = np.tile(art, (2, 2, 1))
    preview(big, "kh-insang")


def tugu():
    W, H = 300, 520
    rng = random.Random(2); nx = Seq(1100)
    art = blank(W, H)
    art, _, _ = monument(art, W, H, W * 0.5, H - 10, H * 0.92, nx, rng)
    preview(art, "kh-tugu")
    save(art, f"{OUT}/tugu.webp", max_w=200, quality=84)


def divider():
    """The equator: a gilt line with a tiny globe-ring at its centre and two ripples."""
    W, H = 720, 90
    rng = random.Random(9); nx = Seq(1500)
    art = blank(W, H)
    line = strokes(W, H, [([(20, 45), (290, 45)], 2.2, (0.4, 0.0)), ([(430, 45), (700, 45)], 2.2, (0.0, 0.4))])
    art = FO(art, line, GOLD, seed=nx(), emboss=0.4, sparkle=0.1)
    rip = strokes(W, H, [([(x, 60 + 3 * math.sin(x / 9)) for x in np.arange(150, 300, 3)], 1.6, (0.3, 0.1)), ([(x, 60 + 3 * math.sin(x / 9)) for x in np.arange(420, 570, 3)], 1.6, (0.1, 0.3))])
    art = OV(art, rip, lambda q: gouache_paint(q, TEAL, seed=nx(), rough=0.6, density=0.8))
    g = circles(W, H, [(360, 45, 16)])
    art = GP(art, g, "#2e7a7a", TEAL_D, seed=nx(), rough=0.5)
    art = FO(art, strokes(W, H, [([(344, 45), (376, 45)], 2.0, None), (arc_pts(360, 45, 15.5, -math.pi / 2, math.pi / 2, 16), 1.2, None)]) * g, GOLD_L, seed=nx())
    ring = path_mask(W, H, lambda p: p.addOval(skia.Rect(332, 37, 388, 53)), stroke=3)
    art = FO(art, ring * (1 - g * (np.arange(H)[:, None] < 45)), GOLD, seed=nx(), emboss=0.6)
    arr = strokes(W, H, [([(318, 45), (404, 45)], 2.0, None)]) * (1 - g)
    art = FO(art, np.maximum(arr, shapes(W, H, [[(400, 39), (414, 45), (400, 51)]], smooth=False)), GOLD, seed=nx())
    preview(art, "kh-divider")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)


def rumah():
    """A single Malay stilt house with a palm and its river reflection (hero / closing)."""
    W, H = 520, 500
    rng = random.Random(14); nx = Seq(1900)
    art = blank(W, H)
    pm = palm(W, H, 420, 430, 260, rng, lean=-0.12)
    art = GP(art, pm, LEAF, LEAF_D, seed=nx(), rough=1.2, streak=0.8)
    pm = palm(W, H, 70, 430, 200, rng, lean=0.1)
    art = GP(art, pm, "#5f8a5e", LEAF_D, seed=nx(), rough=1.2, streak=0.8)
    art = malay_house(art, W, H, 120, 440, 280, nx, rng)
    wat = shapes(W, H, [[(20, 440), (500, 440), (480, 490), (40, 492)]])
    art = GP(art, wat, RIVER, RIVER_D, seed=nx(), rough=2.0, streak=1.6)
    refl = strokes(W, H, [([(x0, y), (x0 + rng.uniform(30, 90), y)], 2.0, (0.3, 0.3)) for x0, y in [(rng.uniform(40, 420), rng.uniform(446, 486)) for _ in range(18)]])
    art = OV(art, refl * wat, lambda q: gouache_paint(q, "#e9c46a", RIVER_L, seed=nx(), rough=0.8, density=0.6))
    preview(art, "kh-rumah")
    save(art, f"{OUT}/rumah.webp", max_w=420, quality=82)


def boat():
    W, H = 360, 120
    nx = Seq(2300)
    art = blank(W, H)
    art = speedboat(art, W, H, 270, 60, 90, nx, d=1)
    preview(art, "kh-boat", bg="#7c9a8e")
    save(art, f"{OUT}/boat.webp", max_w=220, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
