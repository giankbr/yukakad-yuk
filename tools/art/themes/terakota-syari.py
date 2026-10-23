"""Terakota Syari — earthy modern syari wedding without photos: terracotta arch portal, arcade band, dried fan palms
and pampas in a clay vase, warm lime-plaster cream. Gouache clay with directional light.
Run: python3 -I terakota-syari.py [part ...]  parts: arch arcade vase pampas sprig plaster
Assets -> public/themes/art/terakota-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m1_lib import *

OUT = outdir("terakota-syari")
PARTS = sys.argv[1:] or ["arch", "arcade", "vase", "pampas", "sprig", "emblem", "plaster"]
CREAM, PLASTER = "#f3e9dc", "#eee0cc"
TERRA, TERRA_L, TERRA_D = "#b5532e", "#d4825c", "#7a3218"
PALM, PALM_L, PALM_D = "#c8a36d", "#e2c895", "#8c6a3c"
PAMPAS, PAMPAS_D = "#efe3cb", "#cdb894"


def arch_poly(cx, base, w, h, n=60):
    """Round-headed arch outline (straight jambs + semicircle)."""
    r = w / 2
    top = base - h + r
    pts = [(cx - r, base)]
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        pts.append((cx + math.cos(a) * r, top + math.sin(a) * r))
    pts.append((cx + r, base))
    return pts


def clay(mask, seed, base=TERRA, light=TERRA_L, dark=TERRA_D, depth=7.0, rough=2.0):
    h, w = mask.shape
    rgb = clay_shade(mask, base, light, dark, seed, depth=depth)
    m = displace(mask, seed, rough, 24)
    m = np.clip((gaussian_filter(m, 0.7) - 0.35) * 2.4, 0, 1)
    s = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), (4.0, 0.6))
    s = (s - s.mean()) / (s.std() + 1e-6)
    rgb = rgb * (1 + s[..., None] * 0.025)
    pores = (np.random.default_rng(seed + 1).random((h, w)) > 0.985).astype(np.float32)
    rgb = rgb * (1 - gaussian_filter(pores, 0.6)[..., None] * 0.6)
    return rgba(rgb, m)


def arch():
    """Big portal: a thick clay arch ring with an inner lighter moulding and a keystone-less soft crown."""
    W, H = 640, 900
    outer = shapes(W, H, [arch_poly(W / 2, H - 4, 600, 880)], smooth=False)
    inner = shapes(W, H, [arch_poly(W / 2, H + 40, 500, 830)], smooth=False)
    ring = np.clip(outer - inner, 0, 1)
    art = clay(ring, 3, depth=9)
    mould = np.clip(shapes(W, H, [arch_poly(W / 2, H + 40, 520, 842)], smooth=False) - inner, 0, 1)
    art = over(art, clay(mould, 5, TERRA_L, "#e6a580", TERRA, depth=3, rough=1.2))
    # shadow cast by the ring onto the plaster inside
    sh = np.clip(gaussian_filter(np.roll(np.roll(ring, 14, 1), 18, 0), 9) - ring, 0, 1) * inner * 0.35
    art = over(rgba(np.ones((H, W, 3), np.float32) * col3("#8a5a3c"), sh), art)
    art = add_grain(art, 4, 0.03)
    preview(art, "ts-arch")
    save(art, f"{OUT}/arch.webp", max_w=600, quality=80)


def arcade():
    """Band of five small arches (openings show warm plaster), for section edges and the closing."""
    W, H = 780, 230
    wall = np.zeros((H, W), np.float32); wall[20:, :] = 1
    holes = shapes(W, H, [arch_poly(70 + i * 160, H + 2, 110, 180) for i in range(5)], smooth=False)
    m = np.clip(wall - holes, 0, 1)
    art = clay(m, 11, depth=5)
    cap = np.zeros((H, W), np.float32); cap[10:26, :] = 1
    art = over(art, clay(cap, 12, TERRA_D, "#9a4a2a", "#5a2410", depth=2, rough=1.0))
    inner = np.clip(holes - np.roll(holes, -10, 1), 0, 1) * 0.5
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3("#7a3218"), gaussian_filter(inner, 3) * holes))
    preview(art, "ts-arcade")
    save(art, f"{OUT}/arcade.webp", max_w=720, quality=80)


def fan_leaf(art, W, H, cx, cy, R, a0, a1, n, rng, nx, col=PALM, colL=PALM_L, colD=PALM_D, torn=0.3):
    """Dried fan palm: pleated segments radiating from the hastula; split tips, darker folds."""
    polys, folds = [], []
    for i in range(n):
        a = a0 + (a1 - a0) * (i + 0.5) / n
        L = R * rng.uniform(0.86, 1.06)
        wd = (a1 - a0) / n * 0.5
        tipa = a + rng.uniform(-0.04, 0.04)
        p = [(cx + math.cos(a - wd * 0.3) * R * 0.12, cy + math.sin(a - wd * 0.3) * R * 0.12),
             (cx + math.cos(a - wd) * L * 0.6, cy + math.sin(a - wd) * L * 0.6),
             (cx + math.cos(tipa - wd * 0.5) * L, cy + math.sin(tipa - wd * 0.5) * L),
             (cx + math.cos(tipa) * L * (0.88 if rng.random() < torn else 0.98), cy + math.sin(tipa) * L * (0.88 if rng.random() < torn else 0.98)),
             (cx + math.cos(tipa + wd * 0.5) * L, cy + math.sin(tipa + wd * 0.5) * L),
             (cx + math.cos(a + wd) * L * 0.6, cy + math.sin(a + wd) * L * 0.6),
             (cx + math.cos(a + wd * 0.3) * R * 0.12, cy + math.sin(a + wd * 0.3) * R * 0.12)]
        polys.append(p)
        folds.append(([(cx + math.cos(a) * R * 0.15, cy + math.sin(a) * R * 0.15), (cx + math.cos(tipa) * L * 0.92, cy + math.sin(tipa) * L * 0.92)], 1.6, (0.1, 0.4)))
    m = shapes(W, H, polys, smooth=False)
    art = GP(art, m, col, colL, seed=nx(), rough=1.5, streak=1.4)
    # alternate segments in shade (pleats)
    shade = shapes(W, H, polys[::2], smooth=False)
    art = G(art, shade, colD, seed=nx(), density=0.28, edge=0.2, bloom=0.2, rough=2)
    art = G(art, strokes(W, H, folds), colD, seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.4)
    art = G(art, circles(W, H, [(cx, cy, R * 0.07)]), colD, seed=nx(), density=0.8, edge=0.3, rough=1)
    return art, m


def plume(W, H, base, tip, n, rng, spread=26, length=34):
    """Pampas plume: many fine soft hairs along a curved rachis."""
    rach = curve([base, ((base[0] + tip[0]) / 2 + rng.uniform(-10, 10), (base[1] + tip[1]) / 2), tip], 40)
    items = [(rach, 2.0, (0.0, 0.3))]
    hairs = []
    L = len(rach)
    for k in range(n):
        t = rng.uniform(0.25, 1.0)
        px, py = rach[int(t * (L - 1))]
        j = min(L - 1, int(t * (L - 1)) + 1)
        ang = math.atan2(rach[j][1] - rach[j - 1][1], rach[j][0] - rach[j - 1][0])
        side = rng.choice((-1, 1))
        a = ang + side * rng.uniform(0.15, 0.7)
        ln = length * rng.uniform(0.5, 1.0) * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 1.1)))
        e = (px + math.cos(a) * ln, py + math.sin(a) * ln)
        mid = (px + math.cos(a) * ln * 0.5 + rng.gauss(0, 2), py + math.sin(a) * ln * 0.5 + rng.gauss(0, 2))
        hairs.append(([(px, py), mid, e], rng.uniform(1.8, 3.2), (0.0, 0.7)))
    return strokes(W, H, items), strokes(W, H, hairs)


def paint_plumes(art, W, H, specs, rng, nx):
    for base, tip, n in specs:
        st, hm = plume(W, H, base, tip, n, rng)
        soft = gaussian_filter(hm, 1.2)
        art = G(art, np.clip(gaussian_filter(hm, 3) * 2.2, 0, 1), "#c7ad80", seed=nx(), density=0.55, edge=0.1, bloom=0.4, rough=3, feather=2)
        art = G(art, np.clip(soft * 1.8, 0, 1), "#b39465", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1.5, feather=0.8)
        art = GP(art, hm * (fbm(W, H, nx(), 20, 2) > 0.45), "#efe2c6", "#f8f0e0", seed=nx(), rough=0.6, streak=0.4, density=0.85)
        art = G(art, st, PALM_D, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    return art


def vase():
    """Clay vase with two dried fan palms, a dried palm spear and pampas plumes."""
    W, H = 560, 760
    rng = random.Random(8); nx = Seq(400)
    art = blank(W, H)
    vx, vb = W * 0.44, H - 8
    # stems
    stems = [([(vx - 10, vb - 150), (vx - 70, H * 0.42), (W * 0.22, H * 0.28)], 7, None),
             ([(vx + 6, vb - 150), (vx + 40, H * 0.45), (W * 0.68, H * 0.24)], 7, None),
             ([(vx, vb - 150), (vx - 6, H * 0.4), (vx + 6, H * 0.12)], 6, None)]
    art = GP(art, strokes(W, H, stems), PALM_D, "#76562e", seed=nx(), rough=1)
    # palm spear (feather leaf) up the middle
    sp = curve([(vx, H * 0.4), (vx - 4, H * 0.24), (vx + 10, H * 0.06)], 40)
    leaflets = []
    for k, (px, py, a) in enumerate(along(sp, 9)):
        for side in (-1, 1):
            aa = a + side * 1.15
            L = 50 * math.sin(math.pi * (0.15 + 0.85 * k / 30)) + 10
            leaflets.append(([(px, py), (px + math.cos(aa) * L * 0.6, py + math.sin(aa) * L * 0.6 - 6), (px + math.cos(aa) * L, py + math.sin(aa) * L - 4)], 5.5, (0.05, 0.6)))
    art = GP(art, strokes(W, H, leaflets), "#d9bd8a", PALM, seed=nx(), rough=1.2, streak=1.0)
    art = G(art, strokes(W, H, leaflets[::3]), PALM_D, seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
    art, _ = fan_leaf(art, W, H, W * 0.22, H * 0.28, 170, math.pi * 0.85, math.pi * 1.9, 17, rng, nx)
    art, _ = fan_leaf(art, W, H, W * 0.68, H * 0.24, 150, math.pi * 1.12, math.pi * 2.15, 15, rng, nx, "#c09663", "#dcbf8c", "#866238")
    art = paint_plumes(art, W, H, [((vx - 20, vb - 150), (W * 0.06, H * 0.5), 700), ((vx + 20, vb - 150), (W * 0.92, H * 0.48), 700),
                                   ((vx + 4, vb - 150), (W * 0.58, H * 0.34), 600)], rng, nx)
    # vase
    body = shapes(W, H, [curve([(vx - 40, vb - 170), (vx - 46, vb - 150), (vx - 90, vb - 90), (vx - 70, vb - 10), (vx, vb), (vx + 70, vb - 10),
                                (vx + 90, vb - 90), (vx + 46, vb - 150), (vx + 40, vb - 170)], 50)])
    art = over(art, clay(body, 21, depth=14))
    lip = shapes(W, H, [ellipse_pts(vx, vb - 168, 46, 9, 20)])
    art = over(art, clay(lip, 22, TERRA_D, "#9a4a2a", "#4a1c0a", depth=2, rough=0.8))
    band = shapes(W, H, [[(vx - 88, vb - 92), (vx + 88, vb - 92), (vx + 86, vb - 82), (vx - 86, vb - 82)]], smooth=False) * body
    art = OV(art, band, lambda mm: rgba(np.ones(mm.shape + (3,), np.float32) * col3(CREAM), mm * 0.75))
    art = add_grain(art, 5, 0.025)
    preview(art, "ts-vase")
    save(art, f"{OUT}/vase.webp", max_w=440, quality=80)


def pampas():
    """Loose pampas trio leaning right, for the opposite corner."""
    W, H = 360, 520
    rng = random.Random(14); nx = Seq(600)
    art = paint_plumes(blank(W, H), W, H, [((W * 0.3, H), (W * 0.86, H * 0.1), 800), ((W * 0.25, H), (W * 0.5, H * 0.02), 760),
                                          ((W * 0.2, H), (W * 0.1, H * 0.2), 600)], rng, nx)
    art, _ = fan_leaf(art, W, H, W * 0.22, H * 0.62, 110, math.pi * 1.25, math.pi * 1.95, 11, rng, nx, "#c09663", "#dcbf8c", "#866238")
    preview(art, "ts-pampas")
    save(art, f"{OUT}/pampas.webp", max_w=300, quality=80)


def sprig():
    """Small divider: a single dried palm leaflet spray with two tiny clay beads."""
    W, H = 360, 70
    rng = random.Random(3); nx = Seq(800)
    art = blank(W, H)
    sp = [(30, H * 0.55), (180, H * 0.45), (330, H * 0.55)]
    sp = curve(sp, 40)
    leaflets = []
    for k, (px, py, a) in enumerate(along(sp, 10)):
        d = abs(px - W / 2) / (W / 2)
        if d < 0.1:
            continue
        side = 1 if px < W / 2 else -1
        for s2 in (-1, 1):
            aa = a + math.pi * (0 if side > 0 else 1) + s2 * 0.6 * side
            L = 22 * (1 - d) + 6
            leaflets.append(([(px, py), (px + math.cos(aa + math.pi) * L, py + math.sin(aa + math.pi) * L)], 4.0, (0.05, 0.6)))
    art = GP(art, strokes(W, H, leaflets + [(sp, 2.2, (0.1, 0.1))]), PALM, PALM_D, seed=nx(), rough=0.8, streak=0.8)
    art = over(art, clay(circles(W, H, [(W / 2, H * 0.45, 9)]), 9, depth=3, rough=0.6))
    art = over(art, clay(circles(W, H, [(W / 2 - 22, H * 0.47, 5), (W / 2 + 22, H * 0.47, 5)]), 10, TERRA_L, "#e6a580", TERRA, depth=2, rough=0.5))
    save(art, f"{OUT}/sprig.webp", max_w=320, quality=84)


def emblem():
    """Clay tile medallion: round terracotta disc with a carved eight-point star (two squares) and a ring of dots."""
    W = H = 260
    cx = cy = 130
    disc = circles(W, H, [(cx, cy, 120)])
    art = clay(disc, 41, depth=8)
    sq = lambda r, a: [(cx + math.cos(a + k * math.pi / 2) * r, cy + math.sin(a + k * math.pi / 2) * r) for k in range(4)]
    star = shapes(W, H, [sq(78, 0), sq(78, math.pi / 4)], smooth=False)
    inner = shapes(W, H, [sq(56, 0), sq(56, math.pi / 4)], smooth=False)
    groove = np.clip(star - inner, 0, 1)
    art = over(art, clay(groove, 42, TERRA_D, "#9a4a2a", "#4a1c0a", depth=2, rough=0.8))
    art = over(art, clay(circles(W, H, [(cx, cy, 20)]), 43, TERRA_L, "#eab08a", TERRA, depth=3, rough=0.6))
    dots = circles(W, H, [(cx + math.cos(k * math.tau / 16) * 102, cy + math.sin(k * math.tau / 16) * 102, 4.5) for k in range(16)])
    art = over(art, clay(dots, 44, TERRA_D, "#9a4a2a", "#4a1c0a", depth=1.5, rough=0.5))
    art = add_grain(art, 6, 0.03)
    preview(art, "ts-emblem")
    save(art, f"{OUT}/emblem.webp", max_w=220, quality=82)


def plaster_tile():
    W = H = 384
    rgb = plaster(W, H, PLASTER, 31, 0.55)
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/plaster.webp", quality=74)


plaster_ = plaster
for p in PARTS:
    (plaster_tile if p == "plaster" else globals()[p])()
    clear()
