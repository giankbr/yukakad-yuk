"""Belitung Granit — original watercolour of a Belitung-like coast: giant smooth granite boulders on white sand, clear
turquoise shallows over pale sand, a small island with a white lighthouse on the horizon, wind-blown clouds.
No figures. Run: python3 -I belitung-granit.py [part ...]  parts: scene rocks isle sea foam pebble
Assets -> public/themes/art/belitung-granit/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d2_lib import *

OUT = outdir("belitung-granit")
PARTS = sys.argv[1:] or ["scene", "rocks", "isle", "sea", "foam", "pebble"]
GR, GR_W, GR_C, GR_D = "#a8a39e", "#c9b7a6", "#7f8a99", "#5d5f68"
TQ, TQ_D, TQ_L, SAND = "#3fb8bf", "#1f7f9e", "#8fdcd2", "#f3ece0"


def boulder(art, W, H, cx, cy, rx, ry, rot, nx, wet=False, light=(-0.6, -0.8)):
    """One smooth granite boulder in watercolour: warm/grey wash, cool shadow side, reserved highlight, granulated
    speckle, dark contact shadow; returns (art, mask)."""
    r_ = random.Random(int(cx * 7 + cy))
    lumps = [(cx, cy, rx, ry, rot)]
    for _ in range(2):
        a = r_.uniform(-2.6, -0.5)
        lumps.append((cx + math.cos(a) * rx * 0.45, cy + math.sin(a) * ry * 0.4, rx * r_.uniform(0.5, 0.7), ry * r_.uniform(0.45, 0.65), rot + r_.uniform(-20, 20)))
    m = ellipses(W, H, lumps)
    m = m * (1 - rect(W, H, -9999, cy + ry * 0.82, 9999, cy + ry * 2))
    m = gaussian_filter(m, max(2, rx * 0.06))
    m = np.clip((m - 0.5) * 3 + 0.5, 0, 1)
    m = displace(m, nx(), max(2.0, rx * 0.025), max(30, rx * 0.8))
    art = over(art, flat(m, "#efe9df", 1.0))
    art = G(art, m, GR, GR_W, seed=nx(), density=0.62, edge=0.55, bloom=0.35, gran=0.55, rough=1.2, feather=0.8)
    lx, ly = cx + light[0] * rx * 0.55, cy + light[1] * ry * 0.55
    hl = light_mask(H, W, lx, ly, max(rx, ry) * 1.25)
    sh = m * np.clip(1 - hl * 1.6, 0, 1)
    art = G(art, sh, GR_C, GR_D, seed=nx(), density=0.85, edge=0.4, bloom=0.4, gran=0.6, rough=2, feather=3)
    deep = m * np.clip(1 - light_mask(H, W, lx, ly, max(rx, ry) * 2.0) * 1.7, 0, 1) ** 1.5
    art = G(art, deep, "#454a58", seed=nx(), density=0.8, edge=0.3, bloom=0.2, gran=0.5, rough=2, feather=3)
    # pale warm lichen patches and granite speckle
    lich = m * np.clip((fbm(W, H, nx(), 26, 3) - 0.62) * 4, 0, 1)
    art = G(art, lich, "#d9b98a", "#e6cfa0", seed=nx(), density=0.35, edge=0.4, rough=1, feather=0.6)
    sp = (np.random.default_rng(nx()).random((H, W)) > 0.985).astype(np.float32)
    art = over(art, flat(gaussian_filter(sp, 0.5) * 2.2 * m * (0.4 + sh), "#3f4048", 0.45))
    # reserved highlight: lift pigment (paper shows through)
    lift = m * np.clip(hl * 1.6 - 0.8, 0, 1)
    art = over(art, flat(gaussian_filter(lift, 4), "#fff7ea", 0.7))
    warm = m * np.clip(hl * 1.3 - 0.3, 0, 1)
    art = G(art, warm, "#e3b99a", seed=nx(), density=0.28, edge=0.3, rough=2, feather=4)
    # weathered fracture lines (sheeting joints) wrapping the boulder
    cracks = []
    for k in range(r_.randint(1, 2)):
        yc = cy + ry * r_.uniform(-0.3, 0.4)
        pts = [(cx + rx * t, yc + ry * 0.12 * math.sin(t * 2.2 + k) + abs(t) * ry * 0.1) for t in np.linspace(-0.95, 0.95, 18)]
        cracks.append((pts, max(1.2, rx * 0.018), (0.3, 0.3)))
    art = G(art, strokes(W, H, cracks) * m, "#4a4e5a", seed=nx(), density=0.45, edge=0.6, rough=0.8, feather=0.5)
    rim = m * np.clip(light_mask(H, W, cx + rx * 0.9, cy + ry * 0.3, rx * 0.8) * 1.4, 0, 1) * (1 - hl)
    art = G(art, rim, "#8fc9c4", seed=nx(), density=0.35, edge=0.3, rough=1, feather=2)
    art = over(art, flat(gaussian_filter(outline(m, 1.4), 0.7), "#4c5260", 0.35))
    if wet:
        band = m * np.clip((ellipses(W, H, [(cx, cy + ry * 0.92, rx * 1.1, ry * 0.18, rot)])), 0, 1)
        art = G(art, band, "#4f6f7c", seed=nx(), density=0.45, edge=0.5, rough=2, feather=2)
    return art, m


if "scene" in PARTS:
    W, H = 600, 1300
    nx = Seq(400); rng = random.Random(4)
    HZ = 690  # horizon
    sky = wet_sky(W, H, [(0.0, "#a9cfe6"), (0.28, "#cfe5ef"), (0.5, "#eef4f2"), (0.56, "#f7f3ea"), (1.0, "#f7f3ea")], seed=31, blooms=0.4)
    art = sky
    # wind-blown cloud washes (soft wet-in-wet, lifted centres)
    for (cy, x0, x1, w_, col) in [(140, -60, 330, 46, "#b9d3e4"), (220, 260, 680, 38, "#c3dae6"), (330, -40, 260, 26, "#d0e2ea"), (430, 330, 660, 22, "#d6e6ec"), (520, 40, 380, 16, "#dfeaee")]:
        m = strokes(W, H, [(curve([(x0, cy + 10), ((x0 + x1) / 2, cy - w_ * 0.4), (x1, cy - 4)], 30), w_, (0.35, 0.45))])
        art = G(art, m, col, "#e9f1f4", seed=cy, density=0.5, edge=0.35, bloom=0.6, rough=10, feather=5)
        top = strokes(W, H, [(curve([(x0 + 30, cy - w_ * 0.3), ((x0 + x1) / 2, cy - w_ * 0.75), (x1 - 40, cy - w_ * 0.35)], 30), w_ * 0.5, (0.4, 0.4))])
        art = over(art, flat(gaussian_filter(top, 4), "#ffffff", 0.5))
    clear()
    # sea: deep far band to bright turquoise shallows; pale sand showing through the shallows
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    sea = rect(W, H, -10, HZ, W + 10, 1010)
    art = G(art, sea * np.clip(1 - (yy * H - HZ) / 140, 0, 1), "#2a7fa8", "#2f8fb2", seed=nx(), density=0.8, edge=0.15, bloom=0.2, rough=1.5, feather=1.5)
    art = G(art, sea * np.clip((yy * H - HZ - 40) / 160, 0, 1), TQ, "#55c7c2", seed=nx(), density=0.75, edge=0.2, bloom=0.45, rough=3, feather=3)
    shallow = sea * np.clip((yy * H - 880) / 130, 0, 1)
    art = over(art, flat(shallow, "#bfe9dc", 0.55))
    # sand bars glimpsed through the water (light ribbons)
    bars = strokes(W, H, [(curve([(-20, 905), (200, 880), (420, 915), (640, 890)], 40), 16, (0.3, 0.3)), (curve([(80, 960), (330, 940), (620, 970)], 40), 22, (0.3, 0.3))])
    art = over(art, flat(gaussian_filter(bars, 6) * sea, "#e9f4e6", 0.5))
    # glints and ripple strokes
    art = over(art, flat(ripple_lines(W, H, HZ + 6, 1000, nx(), 1.1, 8, 50) * sea, "#f2fbfa", 0.75))
    art = over(art, flat(ripple_lines(W, H, HZ + 40, 1000, nx(), 0.6, 20, 70) * sea, "#1f7f9e", 0.35))
    clear()
    # distant island with lighthouse at right of the horizon
    isl = displace(ellipses(W, H, [(470, HZ + 2, 95, 22, 0), (420, HZ + 4, 50, 14, 0), (530, HZ + 2, 46, 18, 0)]), nx(), 3, 30) * (yy * H < HZ + 3)
    art = G(art, isl, "#5f8a6a", "#7fa27a", seed=nx(), density=0.8, edge=0.5, rough=1.2, feather=0.8)
    for (bx, by, br) in [(400, HZ - 2, 12), (418, HZ - 4, 9), (548, HZ - 3, 13), (565, HZ, 9)]:
        art, _ = boulder(art, W, H, bx, by, br, br * 0.75, 0, nx)
    lh = poly(W, H, [(476, HZ - 18), (481, HZ - 92), (491, HZ - 92), (496, HZ - 18)])
    art = GP(art, lh, "#fbfaf6", "#e8e6e0", seed=nx(), rough=0.5, streak=0.3)
    art = over(art, flat(lh * rect(W, H, 486, 0, 500, H), "#9aa7b4", 0.45))
    art = GP(art, rect(W, H, 478, HZ - 100, 494, HZ - 92), "#2f5d7a", seed=nx(), rough=0.4)
    art = GP(art, poly(W, H, [(476, HZ - 100), (486, HZ - 112), (496, HZ - 100)]), "#b8483a", seed=nx(), rough=0.4)
    art = over(art, glow(rect(W, H, 481, HZ - 99, 491, HZ - 94), "#fff2b0", radius=5, strength=0.5))
    art = GP(art, rect(W, H, 472, HZ - 18, 500, HZ - 12), "#e8e6e0", seed=nx(), rough=0.4)
    # house of the keeper
    art = GP(art, rect(W, H, 452, HZ - 22, 470, HZ - 10), "#efe9de", seed=nx(), rough=0.4)
    art = GP(art, poly(W, H, [(449, HZ - 22), (461, HZ - 30), (473, HZ - 22)]), "#b8483a", seed=nx(), rough=0.4)
    clear()
    # white sand beach rising in a gentle curve; wet sand line and foam
    beach_top = lambda x: 1000 + 40 * math.sin(x / W * math.pi * 1.1 + 0.4) - 10
    bpts = [(-20, H + 20)] + [(x, beach_top(x)) for x in range(-20, W + 30, 20)] + [(W + 20, H + 20)]
    beach = shapes(W, H, [bpts], smooth=False)
    beach = displace(beach, nx(), 3, 30)
    art = knockout(art, beach, 1.0, 0.8)
    art = over(art, flat(beach, SAND, 1.0))
    art = G(art, beach, "#eadfca", "#f2e9d6", seed=nx(), density=0.35, edge=0.3, bloom=0.5, gran=0.5, rough=3, feather=3)
    wet = beach * np.clip(1 - np.abs(yy * H - np.array([beach_top(x) for x in range(W)])[None, :] - 14) / 14, 0, 1)
    art = G(art, wet, "#d9cdb4", seed=nx(), density=0.4, edge=0.5, rough=3, feather=2)
    foam = strokes(W, H, [(curve([(-20, beach_top(0) - 4), (W * 0.3, beach_top(W * 0.3) - 6), (W * 0.7, beach_top(W * 0.7) - 3), (W + 20, beach_top(W) - 5)], 50), 5, (0.1, 0.1))])
    art = over(art, flat(gaussian_filter(foam, 1.5), "#ffffff", 0.9))
    # footprints-free beach texture: few shells/pebbles
    peb = ellipses(W, H, [(rng.uniform(0, W), rng.uniform(1060, 1290), rng.uniform(2, 5), rng.uniform(1.5, 3), rng.uniform(0, 180)) for _ in range(12)])
    art = G(art, peb, "#b7aa98", "#9a9590", seed=nx(), density=0.6, rough=0.5, feather=0.5)
    clear()
    # giant granite boulders framing left and right (back to front), partly standing in the shallows
    left = [(60, 880, 130, 120, -8, True), (-20, 1010, 170, 160, 6, False), (175, 1030, 80, 52, 10, False), (60, 1215, 140, 80, -4, False)]
    right = [(560, 850, 120, 110, 10, True), (455, 945, 72, 52, -8, True), (640, 1000, 160, 170, -4, False), (520, 1170, 95, 58, 6, False)]
    rocks_m = np.zeros((H, W), np.float32)
    for (bx, by, rx, ry, rot, wet_) in left + right:
        art, m = boulder(art, W, H, bx, by, rx, ry, rot, nx, wet=wet_)
        rocks_m = np.maximum(rocks_m, m)
        clear()
    # contact shadows on the sand
    cs = ellipses(W, H, [(30, 1265, 170, 26, 0), (560, 1190, 150, 24, 0)]) * (1 - rocks_m)
    art = G(art, cs, "#b8a990", seed=nx(), density=0.45, edge=0.2, rough=4, feather=6)
    # wind-blown sea grass tufts at the rock feet
    tufts = []
    for (tx, ty) in [(160, 1062), (190, 1070), (430, 1000), (455, 1010), (600, 1195)]:
        for k in range(7):
            a = -1.57 + rng.uniform(-0.5, 0.5) + 0.35
            L = rng.uniform(20, 42)
            tufts.append(([(tx, ty), (tx + math.cos(a) * L * 0.5 + 4, ty + math.sin(a) * L * 0.5), (tx + math.cos(a) * L + 10, ty + math.sin(a) * L)], 2.4, (0.05, 0.8)))
    art = G(art, strokes(W, H, tufts), "#6f9a5a", "#9bb46a", seed=nx(), density=0.8, edge=0.4, rough=0.6, feather=0.5)
    preview(art, "bscene")
    save_rgb(art, f"{OUT}/scene.webp", quality=84)
    clear()

if "rocks" in PARTS:
    W, H = 560, 320
    nx = Seq(900); random.seed(2)
    art = blank(W, H)
    water = ellipses(W, H, [(280, 292, 290, 26, 0)])
    art = G(art, water, TQ_L, TQ, seed=nx(), density=0.55, edge=0.5, bloom=0.5, rough=6, feather=4)
    for (bx, by, rx, ry, rot) in [(180, 170, 120, 110, -6), (370, 190, 110, 96, 8), (270, 240, 80, 50, 0), (470, 250, 70, 46, -6), (80, 255, 64, 40, 4)]:
        art, _ = boulder(art, W, H, bx, by, rx, ry, rot, nx, wet=True)
        clear()
    art = over(art, flat(ripple_lines(W, H, 280, 316, nx(), 3, 10, 40) * water, "#ffffff", 0.7))
    preview(art, "brocks")
    save(art, f"{OUT}/rocks.webp", max_w=460, quality=82)
    clear()

if "isle" in PARTS:
    W, H = 420, 260
    nx = Seq(1300)
    art = blank(W, H)
    HZ = 200
    sea = ellipses(W, H, [(210, 214, 210, 26, 0)])
    art = G(art, sea, TQ, "#2f8fb2", seed=nx(), density=0.6, edge=0.5, bloom=0.4, rough=6, feather=4)
    isl = displace(ellipses(W, H, [(210, HZ, 130, 30, 0), (150, HZ + 2, 70, 20, 0), (290, HZ, 70, 24, 0)]), nx(), 3, 30) * rect(W, H, 0, 0, W, HZ + 4)
    art = G(art, isl, "#5f8a6a", "#8aa77a", seed=nx(), density=0.85, edge=0.5, rough=1.2, feather=0.8)
    for (bx, by, br) in [(110, HZ - 4, 22), (140, HZ - 2, 16), (300, HZ - 5, 24), (330, HZ, 16)]:
        art, _ = boulder(art, W, H, bx, by, br, br * 0.75, 0, nx)
    tx = 220
    lh = poly(W, H, [(tx - 13, HZ - 28), (tx - 7, HZ - 150), (tx + 7, HZ - 150), (tx + 13, HZ - 28)])
    art = GP(art, lh, "#fbfaf6", "#ebe7de", seed=nx(), rough=0.6, streak=0.3)
    art = G(art, lh * rect(W, H, tx + 1, 0, W, H), "#8fa0b2", seed=nx(), density=0.5, rough=0.6, feather=0.6)
    art = GP(art, rect(W, H, tx - 18, HZ - 154, tx + 18, HZ - 148), "#e8e6e0", seed=nx(), rough=0.4)
    art = GP(art, rect(W, H, tx - 10, HZ - 172, tx + 10, HZ - 154), "#2f5d7a", seed=nx(), rough=0.4)
    art = over(art, glow(rect(W, H, tx - 7, HZ - 170, tx + 7, HZ - 157), "#fff2b0", radius=8, strength=0.6))
    art = GP(art, rect(W, H, tx - 6, HZ - 170, tx + 6, HZ - 157), "#fff3c2", seed=nx(), rough=0.3)
    art = GP(art, poly(W, H, [(tx - 13, HZ - 172), (tx, HZ - 190), (tx + 13, HZ - 172)]), "#b8483a", seed=nx(), rough=0.4)
    art = GP(art, rect(W, H, tx - 1, HZ - 198, tx + 1, HZ - 188), "#3a3a3a", seed=nx(), rough=0.2)
    art = GP(art, rect(W, H, tx + 30, HZ - 40, tx + 66, HZ - 16), "#efe9de", seed=nx(), rough=0.4)
    art = GP(art, poly(W, H, [(tx + 26, HZ - 40), (tx + 48, HZ - 54), (tx + 70, HZ - 40)]), "#b8483a", seed=nx(), rough=0.4)
    art = GP(art, rect(W, H, tx + 42, HZ - 32, tx + 50, HZ - 16), "#7a5a40", seed=nx(), rough=0.3)
    art = over(art, flat(ripple_lines(W, H, HZ + 4, 238, nx(), 3, 8, 30) * sea, "#ffffff", 0.7))
    preview(art, "bisle")
    save(art, f"{OUT}/isle.webp", max_w=300, quality=82)
    clear()

if "sea" in PARTS:
    W, H = 600, 700
    nx = Seq(1700)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = wet_sky(W, H, [(0.0, "#2a86ad"), (0.35, "#34a9b8"), (0.75, "#5cc8c0"), (1.0, "#9fe0d3")], seed=41, blooms=0.8)
    caust = np.clip(1 - np.abs(fbm(W, H, nx(), 34, 3) - 0.5) * 14, 0, 1)
    art = over(art, flat(caust * (0.3 + yy), "#e6fbf5", 0.28))
    art = over(art, flat(ripple_lines(W, H, 0, H, nx(), 1.4, 16, 80), "#f2fbfa", 0.55))
    art = over(art, flat(ripple_lines(W, H, 0, H, nx(), 0.7, 20, 90), "#1f6f8e", 0.3))
    save_rgb(art, f"{OUT}/sea.webp", quality=72)
    clear()

if "foam" in PARTS:
    W, H = 440, 70
    nx = Seq(2100)
    art = blank(W, H)
    wave = strokes(W, H, [(curve([(10, 40), (110, 26), (220, 42), (330, 28), (430, 38)], 60), 12, (0.3, 0.3))])
    art = G(art, wave, TQ, TQ_L, seed=nx(), density=0.7, edge=0.7, bloom=0.5, rough=3, feather=1.5)
    lace = strokes(W, H, [(curve([(30, 32), (120, 20), (215, 34), (320, 22), (410, 30)], 60), 3, (0.2, 0.2))])
    art = over(art, flat(gaussian_filter(lace, 0.8), "#ffffff", 0.9))
    for (bx, by, r) in [(220, 44, 13), (238, 49, 8)]:
        art, _ = boulder(art, W, H, bx, by, r, r * 0.72, 0, nx)
    preview(art, "bfoam")
    save(art, f"{OUT}/foam.webp", max_w=340, quality=84)
    clear()

if "pebble" in PARTS:
    W, H = 160, 160
    nx = Seq(2500)
    art = blank(W, H)
    for (bx, by, r) in [(80, 112, 56), (84, 60, 34), (78, 26, 18)]:
        art, _ = boulder(art, W, H, bx, by, r, r * 0.66, 0, nx)
    preview(art, "bpebble")
    save(art, f"{OUT}/pebble.webp", max_w=100, quality=84)
    clear()
