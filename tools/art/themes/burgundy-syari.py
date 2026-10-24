"""Burgundy Syari — wine velvet, gold and dried flowers: a crushed-velvet tile, a dried bouquet (dried roses, wheat,
baby's breath, dried eucalyptus) tied with twine, a small dried sprig divider, a single dried rose, and a pressed-gold
eight-point star. Run: python3 -I burgundy-syari.py [part ...]  parts: velvet buket sprig mawar bintang
Assets -> public/themes/art/burgundy-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s2_lib import *

OUT = outdir("burgundy-syari")
PARTS = sys.argv[1:] or ["velvet", "buket", "sprig", "mawar", "bintang"]
WINE, WINE_D, WINE_L = "#5c1626", "#3c0b17", "#8a2f40"
GOLD = "#c9a45a"
ROSE_L, ROSE_M, ROSE_D = "#d49a92", "#93394a", "#4a1020"
WHEAT, WHEAT_D = "#dcb56c", "#a87d3c"
STEM, STEM_D = "#7c6a46", "#574a30"
SAGE, SAGE_D = "#9aa08a", "#6f7764"
TWINE = "#c9a676"
LINE = "#3a1a1c"


def dried_rose(art, W, H, cx, cy, r, rng, tilt=0.86, cols=(ROSE_L, ROSE_M, ROSE_D)):
    """Dried garden rose in gouache: ring of cupped outer petals with crinkled dark edges, folded inner petals,
    tight dark heart; light from the upper left."""
    light, mid, deep = cols
    base = blob(W, H, cx, cy, r, r * tilt, rng, 14, rng.uniform(0, 3), 0.12)
    art = paint(art, base, mix(mid, deep, .45), deep, px=1.0, dens=0.6, lc=LINE)
    for ring, (rf, n, sz) in enumerate([(0.55, 7, 0.52), (0.34, 6, 0.42), (0.16, 5, 0.3)]):
        for k in range(n):
            ang = k / n * math.tau + rng.uniform(-.25, .25) + ring * 0.5
            px_, py_ = cx + math.cos(ang) * r * rf, cy + math.sin(ang) * r * rf * tilt - r * 0.04 * ring
            pts = ellipse_pts(px_, py_, r * sz, r * sz * 0.7, 12, ang + math.pi / 2)
            pm = shapes(W, H, [deform(pts, rng, 2, .1)])
            lit = 0.5 + 0.5 * math.cos(ang + math.pi * 0.75)
            col = mix(mix(mid, light, 0.15 + 0.45 * lit), deep, ring * 0.12)
            art = GP(art, pm, col, mix(col, deep, .25), seed=rs(), rough=1.4, streak=0.6, pad=8)
            edge = np.clip((pm - gaussian_filter(pm, 1.6)) * 3, 0, 1)
            art = G(art, edge, deep, seed=rs(), density=0.75, edge=0, bloom=0, rough=0.8, feather=0.4, pad=6)
            # crinkle lines across the petal
            cr = strokes(W, H, [([(px_ + rng.uniform(-r * sz, r * sz) * .6, py_ + rng.uniform(-r * sz, r * sz) * .4), (px_ + rng.uniform(-r * sz, r * sz) * .6, py_ + rng.uniform(-r * sz, r * sz) * .4)], 1.0, None) for _ in range(2)]) * pm
            art = G(art, cr, deep, seed=rs(), density=0.4, edge=0, bloom=0, rough=0.5, pad=6)
    for k in range(3):
        a0 = rng.uniform(0, math.tau)
        sm = stroke_mask(W, H, arc_pts(cx, cy - r * .06, r * (0.16 - k * 0.04), a0, a0 + 3.4, 20, tilt), r * 0.06)
        art = G(art, sm, deep, seed=rs(), density=0.85, edge=0.3, bloom=0, rough=0.6, feather=0.5, pad=6)
    art = G(art, light_side(base, 7, 8, 6), "#f0cfc4", seed=rs(), density=0.28, edge=0.1, bloom=0.3, rough=2)
    return art


def wheat(art, W, H, root, tip, rng, size=1.0):
    """Wheat stalk + ear with alternating grains and awns."""
    (x0, y0), (x1, y1) = root, tip
    bend = rng.uniform(-0.12, 0.12)
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    stem = curve([(x0, y0), (mx, my), (x1, y1)], 40)
    art = paint(art, strokes(W, H, [(stem[:-8], 3.2 * size, None)]), WHEAT_D, "#8e6a34", px=0.8, dens=0.4, lc=LINE)
    ear = stem[-16:]
    grains, awns = [], []
    for i, (x, y) in enumerate(ear[:-1]):
        nx_, ny_ = ear[i + 1][0] - x, ear[i + 1][1] - y
        a = math.atan2(ny_, nx_)
        for side in (-1, 1):
            ga = a + side * 0.42
            gx, gy = x + math.cos(a + side * 1.57) * 3 * size, y + math.sin(a + side * 1.57) * 3 * size
            grains.append(petal_pts(gx, gy, 17 * size * (1 - i / 34), 6.4 * size, a + side * 0.42, n=12))
            awns.append(([(gx + math.cos(ga) * 10 * size, gy + math.sin(ga) * 10 * size), (gx + math.cos(ga - side * 0.25) * 30 * size, gy + math.sin(ga - side * 0.25) * 30 * size)], 0.9, (0, .7)))
    a = math.atan2(y1 - ear[-2][1], x1 - ear[-2][0])
    awns.append(([(x1, y1), (x1 + math.cos(a) * 34 * size, y1 + math.sin(a) * 34 * size)], 1.0, (0, .7)))
    art = G(art, strokes(W, H, awns), "#c9a462", seed=rs(), density=0.8, edge=0, bloom=0, rough=0.4, feather=0.3, pad=6)
    gm = shapes(W, H, grains)
    art = paint(art, gm, WHEAT, WHEAT_D, px=0.9, dens=0.5, lc="#6b4a22")
    art = G(art, light_side(gm, -2, 2, 1.2), "#f3dca3", seed=rs(), density=0.5, edge=0, bloom=0, rough=0.5, pad=6)
    return art


def babys_breath(art, W, H, root, head, rng, n=36, spread=40):
    """Gypsophila: fine forking stems ending in tiny white puffs."""
    hx, hy = head
    pts = [(hx + rng.gauss(0, spread), hy + rng.gauss(0, spread * 0.7)) for _ in range(n)]
    st = [(curve([root, ((root[0] + hx) / 2, (root[1] + hy) / 2), (hx, hy)], 20), 1.8, None)]
    for (x, y) in pts:
        st.append(([(hx + (x - hx) * 0.2, hy + (y - hy) * 0.2), (x, y)], 0.9, None))
    art = G(art, strokes(W, H, st), "#8b8a66", seed=rs(), density=0.85, edge=0, bloom=0, rough=0.4, feather=0.3, pad=6)
    dots = [(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3), rng.uniform(2.2, 4.0)) for (x, y) in pts for _ in range(2)]
    dm = circles(W, H, dots)
    art = G(art, np.roll(np.roll(dm, 1, 0), 1, 1), "#8c7d78", seed=rs(), density=0.5, edge=0, bloom=0, rough=0.5, pad=6)
    art = GP(art, dm, "#fffaf0", "#efe6da", seed=rs(), rough=0.8, streak=0.2, pad=6)
    return art


def euc(art, W, H, root, tip, rng, n=7):
    """Dried eucalyptus: round silver-sage leaves along a stem."""
    stem = curve([root, ((root[0] + tip[0]) / 2 + 10, (root[1] + tip[1]) / 2 - 8), tip], 30)
    art = paint(art, strokes(W, H, [(stem, 2.2, None)]), STEM, ln=False)
    leaves = []
    for k, (x, y, a) in enumerate(along(stem[8:], (len(stem) - 8) * 3.4 / n)):
        side = 1 if k % 2 else -1
        r = rng.uniform(10, 15) * (1 - k / (n * 1.6))
        leaves.append(deform(ellipse_pts(x + math.cos(a + side * 1.57) * r * .8, y + math.sin(a + side * 1.57) * r * .8, r, r * .86, 12), rng, 1, .06))
    lm = shapes(W, H, leaves)
    art = paint(art, lm, SAGE, SAGE_D, px=0.9, dens=0.5, lc="#3f4436")
    art = G(art, light_side(lm, 2, 3, 2), "#d2d6c4", seed=rs(), density=0.4, edge=0, bloom=0.2, rough=1)
    return art


random.seed(23)

if "velvet" in PARTS:
    W = H = 512
    n1 = wrap_noise(W, H, 3, 34)
    n2 = wrap_noise(W, H, 5, 9)
    n3 = wrap_noise(W, H, 8, (2, 14))   # pile direction streaks
    n4 = wrap_noise(W, H, 11, 0.6)
    crush = np.clip((n1 - 0.5) * 1.3 + (n2 - 0.5) * 0.6, -1, 1)
    sheen = np.clip(crush, 0, 1) ** 1.4
    shadow = np.clip(-crush, 0, 1)
    base = np.array(hex_rgb(WINE), np.float32)
    hi = np.array(hex_rgb("#a33c4f"), np.float32)
    lo = np.array(hex_rgb("#2c0710"), np.float32)
    rgb = base * (1 - sheen[..., None] * 0.9) + hi * sheen[..., None] * 0.9
    rgb = rgb * (1 - shadow[..., None] * 0.55) + lo * shadow[..., None] * 0.55
    rgb = rgb * (1 + (n3[..., None] - 0.5) * 0.16 + (n4[..., None] - 0.5) * 0.14)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_full(arr, f"{OUT}/beludru.webp", quality=70)
    prev(arr, "bs_velvet")

if "buket" in PARTS:
    # bouquet lying across: heads to the upper-left, stems tied with twine, cut ends to the lower-right
    W, H = 780, 520
    rng = random.Random(41)
    art = blank(W, H)
    tie = (500, 330)
    # stems (painted first, under everything)
    heads_w = [(70, 120), (120, 60), (190, 40), (40, 210), (260, 30), (90, 300)]
    ends = [(tie[0] + 150 + rng.uniform(-30, 30), tie[1] + 80 + rng.uniform(-30, 40)) for _ in range(9)]
    st = [(curve([e, tie, ((tie[0] + 260) / 2, (tie[1] + 200) / 2)], 20), 3.0, None) for e in ends]
    art = paint(art, strokes(W, H, st), STEM, STEM_D, px=0.8, dens=0.45, lc=LINE)
    # eucalyptus behind
    art = euc(art, W, H, tie, (130, 380), rng, 8)
    art = euc(art, W, H, tie, (250, 110), rng, 7)
    clear()
    # wheat fan
    for hw in heads_w:
        art = wheat(art, W, H, tie, hw, rng, 1.0)
    clear()
    # baby's breath clouds
    for head in [(300, 190), (170, 250), (360, 120), (230, 330)]:
        art = babys_breath(art, W, H, tie, head, rng, n=30, spread=34)
    clear()
    # dried roses + buds near the centre
    for (x, y, r) in [(250, 175, 44), (395, 210, 40), (330, 278, 54), (190, 290, 36), (420, 300, 32)]:
        art = paint(art, strokes(W, H, [(curve([tie, ((x + tie[0]) / 2, (y + tie[1]) / 2 + 8), (x, y)], 16), 4, None)]), STEM, ln=False)
        art = dried_rose(art, W, H, x, y, r, rng)
        clear()
    for (x, y, a) in [(160, 330, 2.6), (300, 95, -2.0)]:
        bm = shapes(W, H, [deform(petal_pts(x, y, 30, 13, a, n=12), rng, 1, .06)])
        art = paint(art, bm, ROSE_M, ROSE_D, px=0.9, dens=0.5, lc=LINE)
        art = G(art, light_side(bm, 2, 3, 2), ROSE_L, seed=rs(), density=0.4, edge=0, bloom=0, rough=1)
    # twine wraps + bow
    wraps = [([(tie[0] - 16 + k * 7, tie[1] - 26), (tie[0] - 6 + k * 7, tie[1] + 26)], 3.2, None) for k in range(5)]
    art = paint(art, strokes(W, H, wraps), TWINE, "#a88454", px=0.8, dens=0.5, lc="#5a4026")
    bow = [(curve([(tie[0], tie[1]), (tie[0] - 40, tie[1] - 48), (tie[0] - 6, tie[1] - 52), (tie[0], tie[1])], 30), 4, None),
           (curve([(tie[0] + 6, tie[1]), (tie[0] + 52, tie[1] - 30), (tie[0] + 44, tie[1] + 4), (tie[0] + 6, tie[1])], 30), 4, None),
           (curve([(tie[0], tie[1] + 4), (tie[0] - 18, tie[1] + 50), (tie[0] - 34, tie[1] + 92)], 30), 3.2, (0, .3)),
           (curve([(tie[0] + 6, tie[1] + 4), (tie[0] + 20, tie[1] + 56), (tie[0] + 12, tie[1] + 104)], 30), 3.2, (0, .3))]
    bm = strokes(W, H, bow)
    art = paint(art, bm, TWINE, "#a88454", px=0.8, dens=0.55, lc="#5a4026")
    art = paint(art, circles(W, H, [(tie[0] + 3, tie[1] - 2, 7)]), "#b8925e", px=0.8, dens=0.55, lc="#5a4026")
    art = add_grain(art, 3, 0.03)
    save(art, f"{OUT}/buket.webp", max_w=640, quality=80)
    prev(art, "bs_buket", bg=WINE)
    prev(art, "bs_buket_l", bg="#f4e9e1")

if "sprig" in PARTS:
    W, H = 520, 120
    rng = random.Random(51)
    art = blank(W, H)
    # symmetric-ish sprigs meeting at a dried rose in the middle
    for d in (-1, 1):
        root = (260 + d * 16, 64)
        art = wheat(art, W, H, root, (260 + d * 210, 52 + rng.uniform(-6, 6)), rng, 0.62)
        art = babys_breath(art, W, H, root, (260 + d * 120, 50), rng, n=14, spread=16)
    clear()
    art = dried_rose(art, W, H, 260, 60, 26, rng)
    save(art, f"{OUT}/ranting.webp", max_w=420, quality=82)
    prev(art, "bs_sprig", bg="#f4e9e1")

if "mawar" in PARTS:
    W, H = 160, 160
    rng = random.Random(61)
    art = blank(W, H)
    for (x, y, a) in [(40, 120, 2.4), (120, 118, 0.7)]:
        lm = shapes(W, H, [deform(ellipse_pts(x, y, 20, 17, 12), rng, 1, .06)])
        art = paint(art, lm, SAGE, SAGE_D, px=0.9, dens=0.5, lc="#3f4436")
    art = dried_rose(art, W, H, 80, 78, 52, rng)
    save(art, f"{OUT}/mawar.webp", max_w=110, quality=84)
    prev(art, "bs_mawar", bg=WINE)

if "bintang" in PARTS:
    # pressed-gold eight-point star (two interlaced squares) with a rosette, slightly imperfect
    W = H = 240
    rng = random.Random(71)
    c = 120
    def sq(r, rot):
        return [(c + math.cos(rot + k * math.pi / 2) * r, c + math.sin(rot + k * math.pi / 2) * r) for k in range(4)]
    outline = []
    for rot in (math.pi / 4, 0):
        p = sq(100, rot)
        outline.append((p + [p[0]], 7, None))
        p2 = sq(84, rot)
        outline.append((p2 + [p2[0]], 2.4, None))
    ring = [(arc_pts(c, c, 46, 0, math.tau, 60), 3.0, None), (arc_pts(c, c, 30, 0, math.tau, 48), 1.6, None)]
    petals = [petal_pts(c, c, 40, 11, k * math.pi / 4, n=10) for k in range(8)]
    m = np.maximum(strokes(W, H, outline + ring, cap=False), shapes(W, H, petals) * 0.0 + strokes(W, H, [(petal_pts(c, c, 40, 11, k * math.pi / 4, n=12) + [petal_pts(c, c, 40, 11, k * math.pi / 4, n=12)[0]], 2.0, None) for k in range(8)]))
    m = np.maximum(m, circles(W, H, [(c, c, 7)] + [(c + math.cos(k * math.pi / 4 + math.pi / 8) * 64, c + math.sin(k * math.pi / 4 + math.pi / 8) * 64, 3.5) for k in range(8)]))
    m = displace(m, 7, 0.8, 20)
    art = FO(blank(W, H), m, GOLD, seed=7, emboss=0.6, sparkle=0.2)
    save(art, f"{OUT}/bintang.webp", max_w=160, quality=86)
    prev(art, "bs_bintang", bg=WINE)

kb(OUT)
