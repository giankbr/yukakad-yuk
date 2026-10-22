"""Kaili Souraja — gouache + carved wood: the front gable of a Souraja (Banua Mbaso) with its carved panapiri (layered
bands of floral relief, white-and-gold paint on teak) and crossed barge boards; Teluk Palu between the valley hills in
morning light (bay narrowing between the Gawalise range and the eastern hills, palms, small boats); a woven tile
inspired by sarung Donggala (silk check in plum/magenta with gold bomba flowers); a carved flower divider and a gold
bomba emblem.
Run: python3 -I kaili-souraja.py [part ...]   parts: tenun gable bay divider bomba
Assets -> public/themes/art/kaili-souraja/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
import _jw_lib as jw
from _g3_lib import *

OUT = outdir("kaili-souraja")
PARTS = sys.argv[1:] or ["tenun", "gable", "bay", "divider", "bomba"]
IVORY = "#f6efe2"
TEAK, TEAK_D, TEAK_L = "#6b3f24", "#36200f", "#9a6a40"
GOLD = "#c79a3e"
PLUM, MAGENTA, GREEN, CREAM = "#4a1838", "#b23a6e", "#2f6b55", "#efe0c0"


def bomba_cells(n, cy, cx, r):
    """Eight-petal bomba flower in a cell grid: diamond core, four big petals on the axes, four small on diagonals."""
    yy, xx = np.mgrid[0:n, 0:n]
    dy, dx = yy - cy, xx - cx
    d1 = np.abs(dx) + np.abs(dy)
    core = d1 <= r * 0.28
    along = np.maximum(np.abs(dx), np.abs(dy)); perp = np.minimum(np.abs(dx), np.abs(dy))
    petal_ax = (perp <= r * 0.42 * (1 - np.abs(along - r * 0.62) / (r * 0.42))) & (along > r * 0.25) & ~core
    u = (np.abs(dx) + np.abs(dy)) / 2; v = np.abs(np.abs(dx) - np.abs(dy)) / 2
    diag = (v <= 1.0 * (1 - np.abs(u - r * 0.62) / (r * 0.3))) & (u > r * 0.35) & ~petal_ax
    ring_ = (d1 == int(r * 0.45))
    return core, petal_ax, diag, ring_


if "tenun" in PARTS:
    # 60x60 cells, cell 4px -> 240px seamless tile
    n = 60
    pat = np.zeros((n, n), np.int32)          # 0 plum ground
    yy, xx = np.mgrid[0:n, 0:n]
    # check lines (magenta) with gold + green pinstripes
    for k in (0, 30):
        for off, c in [(-3, 1), (-2, 1), (-1, 2), (0, 1), (1, 1), (2, 3)]:
            pat[(yy - k) % n == off % n] = c
            pat[:, (xx[0] - k) % n == off % n] = c
    # small twill pick-lines in the ground
    pat[((yy + xx) % 6 == 0) & (pat == 0)] = 4
    for cy, cx in [(15, 15), (45, 45), (15, 45), (45, 15)]:
        core, pet, diag, ring_ = bomba_cells(n, cy, cx, 9 if (cy + cx) % 60 == 30 else 7)
        pat[pet] = 2
        pat[diag] = 1
        pat[core] = 5
    pal = [PLUM, MAGENTA, "#d4a64a", GREEN, "#5a2246", CREAM]
    art = weave_cells(pat, pal, cell=4, seed=11, metallic=(2,), float_len=3, fibre=0.08)
    show(art, "ks-tenun")
    save_full(art, f"{OUT}/tenun.webp", quality=80)
    clr()

if "gable" in PARTS:
    W, H = 760, 520
    nx = Seq(1100); rng = random.Random(11)
    cx = W / 2
    apex = (cx, 70); bl = (96, 430); br = (W - 96, 430)
    art = blank(W, H)
    # roof flanks behind the gable (sirap shingles), seen beyond the barge boards
    flank = shapes(W, H, [[(cx, 26), (W + 4, 500), (W - 30, 512), (cx, 110), (30, 512), (-4, 500)]], smooth=False)
    flank = flank * (np.mgrid[0:H, 0:W][0] < 470)
    art = GP(art, flank, "#4a3326", "#5d4030", seed=nx(), rough=1.4, streak=1.1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rows = np.clip((np.abs(((yy + np.abs(xx - cx) * 0.25) / 13) % 1.0 - 0.5) * 2 - 0.78) * 5, 0, 1) * flank
    art = wash(art, rows, "#22160f", 0.5, seed=nx())
    art = wash(art, flank * np.clip((fbm(W, H, nx(), 9, 2) - 0.5) * 3, 0, 1), "#8a6a50", 0.25, seed=nx())
    # gable triangle with carved bands
    tri = shapes(W, H, [[apex, br, bl]], smooth=False)
    band_ys = [(330, 420), (240, 322), (160, 232)]
    items, leaves = [], []
    for bi, (y0, y1) in enumerate(band_ys):
        ym = (y0 + y1) / 2
        # half-width of the triangle at ym
        hw = (ym - apex[1]) / (bl[1] - apex[1]) * (cx - bl[0]) - 30
        s_ = (y1 - y0) * 0.5
        step = s_ * 1.05
        k = 0
        x = cx + s_ * 1.3
        vine = [(cx + u, ym + math.sin(u / step * math.pi) * (y1 - y0) * 0.22) for u in np.linspace(-hw, hw, 80)]
        items.append((vine, s_ * 0.09, (0.05, 0.05)))
        while x < cx + hw - s_ * 0.6:
            for sgn in (-1, 1):
                xx_ = cx + sgn * (x - cx)
                fl = sgn * (1 if k % 2 else -1)
                it, lv = jw.lung(xx_, ym + fl * (y1 - y0) * 0.12, s_ * 0.8, 0 if sgn > 0 else math.pi, fl); items += it; leaves += lv
                leaves.append(petal_pts(xx_ + sgn * s_ * 0.5, ym - fl * (y1 - y0) * 0.22, s_ * 0.34, s_ * 0.16, -fl * math.pi / 2 + sgn * 0.4, n=10))
            x += step; k += 1
        # central flower in each band
        leaves += [petal_pts(cx, ym, s_ * 0.85, s_ * 0.34, a, n=10) for a in np.linspace(0, math.tau, 9)[:-1]]
    # top: bunga medallion
    leaves += [petal_pts(cx, 118, 30, 9, a, n=10) for a in np.linspace(0, math.tau, 13)[:-1]]
    art = over(art, jw.carve(W, H, tri, items, leaves, nx, base=TEAK, light=TEAK_L, dark=TEAK_D, gold=GOLD, gold_amt=0.5, seed=13))
    # white lime paint picked on the raised flowers (Kaili carving often carries white/cream accents)
    rel = shapes(W, H, leaves) * tri
    art = wash(art, rel * np.clip((fbm(W, H, nx(), 12, 3) - 0.35) * 2, 0, 1), CREAM, 0.42, seed=nx())
    # moulding rails between bands
    rails = []
    for (y0, y1) in band_ys:
        for y in (y0 - 4, y1 + 2):
            hw = (y - apex[1]) / (bl[1] - apex[1]) * (cx - bl[0])
            rails.append([(cx - hw, y - 4), (cx + hw, y - 4), (cx + hw, y + 4), (cx - hw, y + 4)])
    rm = shapes(W, H, rails, smooth=False) * tri
    art = GP(art, rm, TEAK_L, TEAK, seed=nx(), rough=0.8)
    art = FO(art, rm * np.clip((fbm(W, H, nx(), 30, 3) - 0.3) * 2, 0, 1), GOLD, seed=nx(), sparkle=0.05)
    # barge boards crossing at the apex and extending into horn-like finials (bangko-bangko)
    def board(p0, p1, w):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); nx_, ny_ = -dy / L * w / 2, dx / L * w / 2
        return [(p0[0] + nx_, p0[1] + ny_), (p1[0] + nx_, p1[1] + ny_), (p1[0] - nx_, p1[1] - ny_), (p0[0] - nx_, p0[1] - ny_)]
    ext = 64
    ux, uy = (cx - bl[0]), (apex[1] - bl[1]); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    bL = board((bl[0] - ux * 30, bl[1] - uy * 30), (apex[0] + ux * ext, apex[1] + uy * ext), 26)
    bR = board((br[0] + ux * 30, br[1] - uy * 30), (apex[0] - ux * ext, apex[1] + uy * ext), 26)
    boards = shapes(W, H, [bL, bR], smooth=False)
    art = GP(art, boards, "#5a3420", TEAK, seed=nx(), rough=1.0, streak=1.2)
    art = relief(art, boards, 3, 0.45, light="#c89a68", dark="#1e1008", seed=nx())
    # painted edge line (cream) + small carved notches along the boards
    inner = shapes(W, H, [board((bl[0] - ux * 30, bl[1] - uy * 30), (apex[0] + ux * ext, apex[1] + uy * ext), 6),
                          board((br[0] + ux * 30, br[1] - uy * 30), (apex[0] - ux * ext, apex[1] + uy * ext), 6)], smooth=False)
    art = wash(art, inner, CREAM, 0.75, seed=nx())
    notch = []
    for t in np.linspace(0.05, 0.95, 16):
        for (p0, p1) in [((bl[0], bl[1]), (apex[0] + ux * ext, apex[1] + uy * ext)), ((br[0], br[1]), (apex[0] - ux * ext, apex[1] + uy * ext))]:
            px, py = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
            notch.append((px, py, 3.2))
    art = FO(art, circles(W, H, notch), GOLD, seed=nx(), sparkle=0.1)
    # curls at the finial tips
    for sgn in (-1, 1):
        tx, ty = apex[0] + sgn * ux * ext, apex[1] + uy * ext
        cur = jw.spiral_pts(tx, ty - 8, 16, 3, math.pi / 2, 1.1, 40, sgn)
        art = GP(art, strokes(W, H, [(cur, 7, (0.0, 0.5))]), "#5a3420", seed=nx(), rough=0.6)
        art = FO(art, strokes(W, H, [(cur, 2.2, (0.0, 0.6))]), GOLD, seed=nx(), sparkle=0.1)
    # lintel beam under the gable, with tumpal (triangle) carving
    beam = shapes(W, H, [[(12, 428), (W - 12, 428), (W - 12, 472), (12, 472)]], smooth=False)
    art = GP(art, beam, TEAK, "#5a3420", seed=nx(), rough=0.8, streak=1.2)
    tum = shapes(W, H, [[(x - 14, 466), (x + 14, 466), (x, 436)] for x in range(34, W - 20, 32)], smooth=False)
    art = GP(art, tum, TEAK_L, TEAK, seed=nx(), rough=0.6)
    art = FO(art, tum * np.clip((fbm(W, H, nx(), 8, 3) - 0.4) * 3, 0, 1), GOLD, seed=nx(), sparkle=0.05)
    art = wash(art, np.clip(beam - gaussian_filter(beam, 1.5) * 1.1, 0, 1) * 3, TEAK_D, 0.7, seed=nx())
    show(art, "ks-gable", IVORY)
    save(art, f"{OUT}/gable.webp", max_w=640, quality=80)
    clr()

if "bay" in PARTS:
    W, H = 860, 560
    nx = Seq(1200); rng = random.Random(12)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    HZ = 214
    art = painted_sky(W, H, [(0, "#9ec7d2"), (0.24, "#d6e8e2"), (0.38, "#f8ead0"), (1.0, "#f3e6c8")], seed=nx())
    for cy_, x0, x1 in [(58, 40, 300), (98, 480, 820), (36, 560, 700)]:
        cl = shapes(W, H, [deform(ellipse_pts((x0 + x1) / 2, cy_, (x1 - x0) / 2, 16, 18), rng, 2, 0.08)])
        art = wash(art, gaussian_filter(cl, 5), "#ffffff", 0.65, seed=nx())
    # morning sun low over the eastern hills (right)
    art = wash(art, radial(W, H, W * 0.74, HZ - 70, 170) ** 2, "#fff4dc", 0.7, seed=nx())
    # water first (the ranges overlap it)
    sea = (yy >= HZ).astype(np.float32)
    art = wash(art, sea, "#6aa8b4", 1.0, seed=nx(), col2="#80b8bf")
    art = wash(art, sea * grad(W, H, 0, HZ, 0, H * 0.9), "#3c7d8f", 0.5, seed=nx())
    art = wash(art, sea * np.clip(1 - np.abs(xx - W * 0.6) / 90, 0, 1) * np.clip(1 - (yy - HZ) / 170, 0, 1), "#fbf0d6", 0.55, seed=nx())
    gl = sun_glints(W, H, W * 0.6, HZ + 4, H - 120, 110, rng, spread=46, col="#fff6e0")
    art = wash(art, gl * sea, "#fbf3df", 0.75, seed=nx())

    def range_(side, base_y, peak_h, reach, x_edge, seed, cols, haze):
        """One hill range seen from the shore: rises from the canvas edge, rolls in 2-3 summits and slopes down to the
        water at x=reach. side -1 = west (left)."""
        r = random.Random(seed); top = []
        n = 36
        for i in range(n + 1):
            t = i / n  # 0 at the edge, 1 at the water
            hgt = peak_h * (1 - t ** 1.6) * (0.78 + 0.22 * math.sin(t * 7.5 + seed) + 0.08 * math.sin(t * 19 + seed * 2))
            x = x_edge + (reach - x_edge) * t
            top.append((x, base_y - max(0, hgt) + r.gauss(0, 1.2)))
        poly = top + [(reach + side * -10, base_y + 2), (x_edge, base_y + 2), (x_edge, H + 20)] if False else top + [(reach, base_y + 3), (x_edge, base_y + 3)]
        m = shapes(W, H, [poly], smooth=False)
        nonlocal_art = None
        return m, top

    ranges = [  # far → near
        (-1, HZ + 2, 70, 400, -20, 3, ("#a7bfc0", "#b6c9c6"), 0.0),
        (1, HZ + 2, 64, 470, W + 20, 4, ("#a2bbbd", "#b0c4c2"), 0.0),
        (-1, HZ + 26, 128, 330, -20, 5, ("#86a596", "#93ae9f"), 0.0),
        (1, HZ + 34, 150, 560, W + 20, 6, ("#7f9f8d", "#8daa98"), 0.0),
        (-1, HZ + 78, 170, 240, -20, 7, ("#5f846b", "#6c9077"), 0.0),
        (1, HZ + 96, 186, 690, W + 20, 8, ("#577d62", "#66896e"), 0.0),
    ]
    for side, by, ph, reach, xe, sd, cols, _ in ranges:
        m, top = range_(side, by, ph, reach, xe, sd, cols, 0)
        art = GP(art, m, cols[0], cols[1], seed=nx(), rough=1.8, streak=1.0)
        # morning light from the east: the west-facing slopes (towards the left) stay in shade
        lit = grad(W, H, reach, 0, xe, 0) if side > 0 else grad(W, H, xe, 0, reach, 0)
        art = wash(art, m * (1 - lit) * 0.8, "#3b5f4c", 0.35 if side < 0 else 0.15, seed=nx())
        art = wash(art, m * lit * np.clip((fbm(W, H, nx(), 18, 3) - 0.45) * 2.5, 0, 1), "#d8e2bf", 0.28, seed=nx())
        # ravines: dry strokes running down from the ridge
        cr = []
        for k in range(14):
            i = rng.randint(2, len(top) - 4); x0, y0 = top[i]
            cr.append(([(x0, y0 + 4), (x0 - side * rng.uniform(6, 22), y0 + rng.uniform(30, 80)), (x0 - side * rng.uniform(10, 40), by)], rng.uniform(1.5, 3.5), (0.1, 0.7)))
        art = wash(art, strokes(W, H, cr) * m, "#2f4d3c", 0.25, seed=nx())
        # pale shore line where the slope meets the water
        art = wash(art, strokes(W, H, [([(xe, by + 1), (reach, by + 1)], 2.4, (0.1, 0.1))]), "#efe6cc", 0.6, seed=nx())
    # Palu city specks at the bay head
    specks = [(x, HZ + 2 + rng.uniform(-2, 5), rng.uniform(1.0, 2.2)) for x in np.linspace(380, 500, 26)]
    art = wash(art, circles(W, H, specks), "#f7f0e0", 0.8, seed=nx())
    # boats
    for bx, by_, bs in [(470, 300, 15), (560, 340, 11), (430, 262, 8)]:
        hull = shapes(W, H, [[(bx - bs, by_), (bx + bs, by_), (bx + bs * 0.7, by_ + bs * 0.28), (bx - bs * 0.7, by_ + bs * 0.28)]])
        art = GP(art, hull, "#7a3a2a", seed=nx(), rough=0.4)
        art = GP(art, shapes(W, H, [[(bx - 1, by_), (bx - 1, by_ - bs * 1.4), (bx + bs * 0.8, by_ - 1)]], smooth=False), "#f4ecd8", seed=nx(), rough=0.3)
        art = wash(art, strokes(W, H, [([(bx - bs * 1.4, by_ + bs * 0.45), (bx + bs * 1.4, by_ + bs * 0.45)], 1.4, (0.3, 0.3))]), "#e9f1ee", 0.7, seed=nx())
    # foreground: our own hillside (deep green) with tree crowns, falling to the water on the right
    fg = shapes(W, H, [[(-20, H + 20), (-20, 420), (120, 404), (260, 430), (420, 470), (560, 492), (700, 500), (W + 20, 494), (W + 20, H + 20)]])
    art = GP(art, fg, "#3f6a48", "#4c7752", seed=nx(), rough=2.2, streak=1.1)
    trees = []
    for _ in range(60):
        tx = rng.uniform(-20, W + 20)
        ground = 420 + max(0, (tx - 120)) * 0.13 if tx > 120 else 410
        ty = rng.uniform(ground - 6, H + 10)
        r_ = rng.uniform(12, 26) * (0.7 + (ty - 400) / 300)
        trees.append(deform(ellipse_pts(tx, ty, r_ * 1.2, r_, 10), rng, 1, 0.12))
    tm = shapes(W, H, trees)
    art = GP(art, tm, "#2f5a38", "#3d6a42", seed=nx(), rough=1.6)
    art = relief(art, tm, 3, 0.35, light="#a9c070", dark="#16301c", lx=0.7, ly=-0.7, seed=nx())
    art = wash(art, tm * np.clip((fbm(W, H, nx(), 5, 2) - 0.5) * 3, 0, 1), "#8fb064", 0.35, seed=nx())
    art = wash(art, tm * np.clip((0.45 - fbm(W, H, nx(), 6, 2)) * 3, 0, 1), "#1d3a24", 0.35, seed=nx())
    art = add_grain(art, seed=nx(), amount=0.03)
    show(art, "ks-bay")
    save_rgb(art, f"{OUT}/bay.webp", size=(780, 508), quality=78)
    clr()

if "divider" in PARTS:
    W, H = 420, 110
    nx = Seq(1300)
    cx, cy = W / 2, H / 2
    items, leaves = [], []
    for sgn in (-1, 1):
        for k, u in enumerate([46, 100, 150]):
            it, lv = jw.lung(cx + sgn * u * 1.12, cy + 2, 36 - k * 4, 0 if sgn > 0 else math.pi, sgn * (1 if k % 2 else -1)); items += it; leaves += lv
    leaves += [petal_pts(cx, cy, 30, 11, a, n=10) for a in np.linspace(0, math.tau, 9)[:-1]]
    m = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    art = blank(W, H)
    art = GP(art, m, TEAK, TEAK_D, seed=nx(), rough=1.0, pad=8)
    art = relief(art, m, 1.6, 0.5, light="#d9a874", dark="#1e1008", seed=nx())
    art = FO(art, m * np.clip((fbm(W, H, nx(), 9, 3) - 0.45) * 3, 0, 1), GOLD, seed=nx(), sparkle=0.08)
    art = wash(art, circles(W, H, [(cx, cy, 7)]), CREAM, 0.9, seed=nx())
    show(art, "ks-divider", IVORY)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clr()

if "bomba" in PARTS:
    W = H = 300
    nx = Seq(1400)
    cx = cy = W / 2
    big = [petal_pts(cx, cy, 120, 44, a, n=14) for a in np.linspace(0, math.tau, 5)[:-1] + math.pi / 4 * 0]
    small = [petal_pts(cx, cy, 92, 26, a, n=12) for a in np.linspace(0, math.tau, 5)[:-1] + math.pi / 4]
    m_big = shapes(W, H, big); m_small = shapes(W, H, small)
    core = circles(W, H, [(cx, cy, 30)])
    dots_ = circles(W, H, [(cx + math.cos(a) * 128, cy + math.sin(a) * 128, 5) for a in np.linspace(0, math.tau, 17)[:-1]])
    art = blank(W, H)
    art = GP(art, m_small, MAGENTA, "#9a2c5e", seed=nx(), rough=1.0)
    art = FO(art, np.clip(m_big - gaussian_filter(m_small, 1) * 0, 0, 1) * (1 - core), "#c99a3e", seed=nx(), emboss=0.7, sparkle=0.12)
    inner = shapes(W, H, [petal_pts(cx, cy, 86, 18, a, n=12) for a in np.linspace(0, math.tau, 5)[:-1]])
    art = GP(art, inner, PLUM, seed=nx(), rough=0.6)
    art = GP(art, core, MAGENTA, "#c24b80", seed=nx(), rough=0.6)
    art = FO(art, circles(W, H, [(cx, cy, 12)]), "#d8b060", seed=nx(), sparkle=0.1)
    art = FO(art, dots_, "#c99a3e", seed=nx(), sparkle=0.1)
    show(art, "ks-bomba", IVORY)
    save(art, f"{OUT}/bomba.webp", max_w=200, quality=84)
    clr()
