"""Opera Beludru — a gilded opera house in gouache: heavy crimson velvet stage curtains (deep pile in the folds, pale
sheen on the crests, gold bullion fringe), a swagged valance with tassels, a crystal chandelier with warm candle bulbs,
a tier of gilded balcony boxes and a single gold tassel.
Run: python3 -I opera-beludru.py [part ...]   parts: curtain valance chandelier balcony tassel
Assets -> public/themes/art/opera-beludru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g6_lib import *  # noqa

OUT = outdir("opera-beludru")
PARTS = sys.argv[1:] or ["curtain", "valance", "chandelier", "balcony", "tassel", "orn"]
RED, RED2, DEEP, LIT = "#86121f", "#981826", "#2a0408", "#d46a70"
GOLD = "#c9a04e"


def fringe(art, W, H, x0, x1, y, L, nx, rng, dense=3.2, col=GOLD):
    """Gold bullion fringe: a braided band and hanging twisted cords."""
    band = shapes(W, H, [rect(x0, y - 8, x1, y + 8)], smooth=False)
    art = gilt(art, band, nx)
    items = []
    x = x0 + 2
    while x < x1 - 1:
        l = L * rng.uniform(0.9, 1.05)
        items.append(([(x, y + 6), (x + rng.uniform(-1, 1), y + 6 + l)], dense * 0.9, (0.0, 0.25)))
        x += dense
    fm = strokes(W, H, items)
    art = gilt(art, fm, nx, base="#b88a3a")
    tw = stripes(W, H, 0.9, 1.0, 3.0, seed=nx()) * fm
    art = tint(art, tw, "#5a3a12", 0.35, seed=nx())
    return art


if "curtain" in PARTS:
    W, H = 460, 1240
    nx = Seq(63100); rng = random.Random(631)
    drape = velvet(W, H, 0, W, 0, H - 40, 4.6, RED, RED2, DEEP, LIT, nx, seed=nx(), sway=0.15)
    art = drape
    yy0 = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = tint(art, np.clip(1 - yy0 / 420, 0, 1) ** 1.5 * art[..., 3], "#14020a", 0.55, seed=nx(), clip=False)
    art = tint(art, np.exp(-((yy0 - 700) / 260) ** 2) * art[..., 3], "#c23040", 0.18, seed=nx(), clip=False)
    # hem: slight shadow above the fringe, fringe along the bottom
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = tint(art, np.exp(-((yy - (H - 60)) / 30) ** 2) * art[..., 3], "#1a0204", 0.45, seed=nx())
    art = fringe(art, W, H, 0, W, H - 44, 34, nx, rng)
    # inner edge (towards stage centre, the right side): a gold galloon trim
    trim = shapes(W, H, [rect(W - 20, 0, W - 8, H - 44)], smooth=False)
    art = gilt(art, trim, nx)
    art = tint(art, stripes(W, H, 0.6, 1.2, 6, seed=nx()) * trim, "#5a3a12", 0.35, seed=nx())
    art = add_grain(art, nx(), 0.03)
    preview(art, "ob-curtain", bg="#14060a")
    save_full(art, f"{OUT}/curtain.webp", size=(230, 620), quality=76)
    clear()

if "valance" in PARTS:
    W, H = 800, 300
    nx = Seq(63200); rng = random.Random(632)
    art = blank(W, H)
    # straight top band
    top = shapes(W, H, [rect(0, 0, W, 70)], smooth=False)
    v = velvet(W, H, 0, W, 0, 70, 40, RED, RED2, DEEP, LIT, nx, seed=nx())
    v[..., 3] *= top
    art = over(art, v)
    # three swags: scalloped, folds following the curve
    n = 3
    for k in range(n):
        x0 = k * W / n - 20; x1 = (k + 1) * W / n + 20
        cx = (x0 + x1) / 2
        pts = [(x0, 50)] + [(x0 + (x1 - x0) * t, 60 + math.sin(math.pi * t) * 150) for t in np.linspace(0, 1, 30)] + [(x1, 50)]
        m = shapes(W, H, [pts])
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        base = 60 + np.sin(math.pi * np.clip((xx - x0) / (x1 - x0), 0, 1)) * 150
        u = np.clip((yy - 40) / np.maximum(1, base - 40), 0, 1.2)
        f = (0.5 + 0.5 * np.cos(u * 5.5 * math.pi + (fbm(W, H, nx(), 80, 2) - 0.5) * 1.5)) ** 1.3
        ca, cd, cl = (np.array(hex_rgb(c), np.float32) for c in (RED2, DEEP, LIT))
        rgb = cd * (1 - f[..., None]) + ca * f[..., None]
        rgb = rgb + (cl - rgb) * (np.clip((f - 0.7) / 0.3, 0, 1)[..., None] ** 2 * 0.28)
        sw = np.concatenate([rgb, gaussian_filter(m, 0.8)[..., None]], -1)
        sh = np.roll(gaussian_filter(m, 8), 10, 0) * 0.6
        art = over(art, col_arr(sh, "#0a0204", sh))
        art = over(art, sw)
        # fringe along the swag's lower curve
        curve_pts = [(x0 + 30 + (x1 - x0 - 60) * t, 60 + math.sin(math.pi * (0.04 + t * 0.92)) * 150 - 2) for t in np.linspace(0, 1, 60)]
        items = [([(px, py), (px, py + 26 * rng.uniform(0.9, 1.05))], 2.8, (0.0, 0.25)) for px, py in curve_pts[::1]]
        fm = strokes(W, H, items)
        art = gilt(art, fm, nx, base="#b88a3a")
        bm = strokes(W, H, [(curve_pts, 9, None)])
        art = gilt(art, bm, nx)
        clear()
    # tassels where swags meet
    for x in [k * W / n for k in range(n + 1)]:
        knot = circles(W, H, [(x, 66, 14)])
        art = gilt(art, knot, nx)
        body = shapes(W, H, [[(x - 8, 78), (x + 8, 78), (x + 20, 168), (x - 20, 168)]])
        art = gilt(art, body, nx, base="#b88a3a")
        art = tint(art, stripes(W, H, math.pi / 2, 1.0, 3.2, seed=nx()) * body, "#5a3a12", 0.4, seed=nx())
        cap = ellipses(W, H, [(x, 92, 12, 10, 0)])
        art = gilt(art, cap, nx)
    preview(art, "ob-valance", bg="#14060a")
    save(art, f"{OUT}/valance.webp", max_w=400, quality=80)
    clear()

if "chandelier" in PARTS:
    W, H = 560, 600
    nx = Seq(63300); rng = random.Random(633)
    art = blank(W, H)
    cx = W / 2
    halo = circles(W, H, [(cx, 300, 170)])
    art = OV(art, halo, lambda mm: col_arr(mm, "#ffcf80", np.clip(gaussian_filter(mm, 70), 0, 1) * 0.32), pad=170)

    def bead(art, x, y, r):
        m = circles(W, H, [(x, y, r)])
        art = OV(art, m, lambda mm: col_arr(mm, "#fbf6ee", np.clip(gaussian_filter(mm, 0.5), 0, 1) * 0.8), pad=3)
        art = tint(art, side_light(m, 1.2, 1.2, 0.8), "#7a6a5a", 0.6, seed=nx())
        return OV(art, circles(W, H, [(x - r * 0.35, y - r * 0.35, max(0.8, r * 0.35))]), lambda mm: col_arr(mm, "#ffffff", np.clip(mm * 1.3, 0, 1)), pad=2)

    def festoon(art, a, b, sag, r=3.2):
        for px, py in catenary(a[0], a[1], b[0], b[1], sag, max(6, int(math.dist(a, b) / (r * 2.3)))):
            art = bead(art, px, py, r)
        return art

    # chain and canopy
    chain = []
    for k in range(9):
        chain.append((cx, 8 + k * 13, 5, 3.6) if k % 2 else (cx, 8 + k * 13, 3.6, 5))
    art = gilt(art, ellipses(W, H, [(x, y, rx, ry, 0) for x, y, rx, ry in chain]), nx)
    # baluster: stacked knops
    knops = [(cx, 128, 26, 10), (cx, 150, 14, 14), (cx, 178, 34, 12), (cx, 214, 18, 22), (cx, 252, 42, 13), (cx, 288, 22, 24), (cx, 332, 58, 16), (cx, 362, 30, 16)]
    stem = shapes(W, H, [rect(cx - 8, 120, cx + 8, 380)], smooth=False)
    art = gilt(art, np.clip(stem + ellipses(W, H, [(x, y, rx, ry, 0) for x, y, rx, ry in knops]), 0, 1), nx)
    # arms: upper tier (4) and lower tier (6), drawn back to front
    tiers = [(250, [(-150, 196), (-70, 186), (70, 186), (150, 196)], 0.75), (334, [(-230, 288), (-150, 304), (-60, 312), (60, 312), (150, 304), (230, 288)], 1.0)]
    tips = []
    for y0, ends, sc in tiers:
        items = []
        for dx, ey in ends:
            pts = [(cx + dx * t, y0 + 6 - math.sin(t * math.pi) * (-26 * sc) + (ey - y0) * t ** 2.2 + 30 * math.sin(t * math.pi * 1.6) * sc * 0.5) for t in np.linspace(0, 1, 30)]
            items.append((pts, 7 * sc, (0.04, 0.08)))
            tips.append((cx + dx, ey, sc))
        art = gilt(art, strokes(W, H, items), nx)
    # festoons between neighbouring tips of the lower tier and from the bowl
    low = [t for t in tips if t[2] == 1.0]
    for a_, b_ in zip(low, low[1:]):
        art = festoon(art, (a_[0], a_[1] + 14), (b_[0], b_[1] + 14), 46)
    for t in low:
        art = festoon(art, (cx + (12 if t[0] > cx else -12), 366), (t[0], t[1] + 14), 30, 2.6)
    # candle cups, candles, flames, pendant drops
    for ex, ey, sc in sorted(tips, key=lambda t: t[2]):
        cup = shapes(W, H, [[(ex - 16 * sc, ey), (ex + 16 * sc, ey), (ex + 9 * sc, ey + 12 * sc), (ex - 9 * sc, ey + 12 * sc)]])
        art = gilt(art, cup, nx)
        cand = shapes(W, H, [rect(ex - 5 * sc, ey - 32 * sc, ex + 5 * sc, ey)], smooth=False)
        art = GP(art, cand, "#f4ead6", "#e8dcc2", seed=nx(), rough=0.3)
        art = tint(art, side_light(cand, 3, 0, 2), "#8a6a4a", 0.5, seed=nx())
        art = candle_flame(art, W, H, ex, ey - 32 * sc, 24 * sc, 6.5 * sc, nx, halo=0.7)
        art = crystal(art, W, H, ex, ey + 28 * sc, 7 * sc, nx, rng)
        art = bead(art, ex, ey + 16 * sc, 2.6)
    # cascade of drops under the bowl and a big pear finial
    for j in range(7):
        x = cx + (j - 3) * 15
        L = 3 - abs(j - 3) // 2
        for t in range(L + 1):
            art = bead(art, x, 384 + t * 11, 2.8)
        art = crystal(art, W, H, x, 384 + (L + 1) * 11 + 8, 7, nx, rng)
    art = gilt(art, ellipses(W, H, [(cx, 400, 10, 8, 0)]), nx)
    art = crystal(art, W, H, cx, 470, 16, nx, rng)
    art = spark(art, cx - 3, 462, 18, col="#ffffff", amt=0.75)
    art = spark(art, low[1][0], low[1][1] + 30, 10, col="#ffffff", amt=0.6)
    preview(art, "ob-chandelier", bg="#14060a")
    save(art, f"{OUT}/chandelier.webp", max_w=280, quality=82)
    clear()

if "balcony" in PARTS:
    W, H = 800, 380
    nx = Seq(63400); rng = random.Random(634)
    art = painted_sky(W, H, [(0, "#2a0a0e"), (1, "#160407")], seed=nx(), streak=0.6)
    n = 3
    bw = W / n
    for k in range(n):
        x0 = k * bw + 16; x1 = (k + 1) * bw - 16
        cx = (x0 + x1) / 2
        # dark box interior with a red drape tied back each side
        inner = shapes(W, H, [rect(x0 + 8, 40, x1 - 8, 230)], smooth=False)
        art = over(art, col_arr(inner, "#3a0a10", inner))
        lamp = circles(W, H, [(cx, 110, 40)])
        art = OV(art, lamp, lambda mm: col_arr(mm, "#ff9a50", np.clip(gaussian_filter(mm, 30), 0, 1) * 0.3), pad=80)
        for side in (-1, 1):
            xa = x0 + 8 if side < 0 else x1 - 8
            if side < 0:
                g = lambda yy, xa=xa: (np.full_like(yy, xa), xa + 44 - 30 * np.sin(np.clip((yy - 40) / 190, 0, 1) * math.pi) ** 2)
            else:
                g = lambda yy, xa=xa: (xa - 44 + 30 * np.sin(np.clip((yy - 40) / 190, 0, 1) * math.pi) ** 2, np.full_like(yy, xa))
            d = velvet(W, H, 0, W, 40, 230, 3, RED, RED2, DEEP, LIT, nx, seed=nx(), gather=g)
            art = over(art, d)
        # arch top
        arch = shapes(W, H, [[(x0, 50), (x0, 20), (cx, 4), (x1, 20), (x1, 50), (cx, 34)]])
        art = gilt(art, arch, nx)
        # balustrade front, bulging
        front = shapes(W, H, [[(x0 - 6, 220), (x1 + 6, 220), (x1 + 2, 300), (cx, 318), (x0 - 2, 300)]])
        art = GP(art, front, "#6a1018", "#7a1620", seed=nx(), rough=0.5)
        art = tint(art, side_light(front, 0, 8, 6), "#1a0204", 0.6, seed=nx())
        rails = strokes(W, H, [([(x0 - 6, 222), (x1 + 6, 222)], 10, None), ([(x0 - 2, 300), (cx, 318), (x1 + 2, 300)], 8, None)])
        art = gilt(art, rails, nx)
        # gilt cartouche + garlands on the front
        cart = ellipses(W, H, [(cx, 266, 22, 28, 0)])
        art = gilt(art, np.clip(cart - ellipses(W, H, [(cx, 266, 15, 21, 0)]), 0, 1), nx)
        art = GP(art, ellipses(W, H, [(cx, 266, 15, 21, 0)]), "#8e1422", seed=nx(), rough=0.3)
        for side in (-1, 1):
            g_pts = [(cx + side * (28 + t * (bw / 2 - 50)), 244 + math.sin(t * math.pi) * 22) for t in np.linspace(0, 1, 16)]
            art = gilt(art, strokes(W, H, [(g_pts, 5, (0.1, 0.1))]), nx)
            for px, py in g_pts[2::3]:
                art = gilt(art, circles(W, H, [(px, py + 2, 4)]), nx)
        # pilasters between boxes
        for px in (x0 - 14, x1 + 14):
            pm = shapes(W, H, [rect(px - 8, 0, px + 8, H)], smooth=False)
            art = gilt(art, pm, nx, base="#b88a3a")
        clear()
    lower = shapes(W, H, [rect(0, 330, W, H)], smooth=False)
    art = GP(art, lower, "#2a0a0e", "#3a0e14", seed=nx(), rough=0.3)
    art = gilt(art, strokes(W, H, [([(0, 332), (W, 332)], 6, None)]), nx)
    art = vignette(art, 0.4, 2.0)
    preview(art, "ob-balcony", bg="#14060a")
    save_rgb(art, f"{OUT}/balcony.webp", size=(400, 190), quality=78)
    clear()

if "tassel" in PARTS:
    W, H = 120, 300
    nx = Seq(63500); rng = random.Random(635)
    art = blank(W, H)
    cord = strokes(W, H, [([(60, 0), (60, 70)], 5, None)])
    art = gilt(art, cord, nx)
    art = tint(art, stripes(W, H, 0.9, 1.0, 3.5, seed=nx()) * cord, "#5a3a12", 0.4, seed=nx())
    head = shapes(W, H, [[(46, 70), (74, 70), (82, 96), (76, 120), (44, 120), (38, 96)]])
    art = gilt(art, head, nx)
    band = shapes(W, H, [rect(40, 120, 80, 130)], smooth=False)
    art = gilt(art, band, nx, base="#b88a3a")
    items = [([(42 + k * 1.6, 130), (32 + k * 2.2 + rng.uniform(-2, 2), 270 + rng.uniform(-8, 6))], 2.2, (0.0, 0.3)) for k in range(26)]
    fm = strokes(W, H, items)
    art = gilt(art, fm, nx, base="#b88a3a")
    art = tint(art, side_light(fm, 6, 0, 4), "#4a2a0a", 0.5, seed=nx())
    preview(art, "ob-tassel", bg="#14060a")
    save(art, f"{OUT}/tassel.webp", max_w=60, quality=84)
    clear()

if "orn" in PARTS:
    # gilt rococo flourish: central shell-oval with two C-scroll arms and leaf tips
    W, H = 440, 110
    nx = Seq(63600); rng = random.Random(636)
    cx, cy = W / 2, 56
    items = []
    for sgn in (-1, 1):
        arm = [(cx + sgn * (26 + t * 150), cy + math.sin(t * math.pi * 1.2) * -16 + t * 6) for t in np.linspace(0, 1, 34)]
        items.append((arm, 5.5, (0.05, 0.6)))
        sp = spiral_pts(cx + sgn * 172, cy + 2, 3, 16, math.pi / 2, 1.3, 30, sgn)
        items.append((sp, 4.0, (0.1, 0.5)))
        sp2 = spiral_pts(cx + sgn * 58, cy + 18, 2, 10, -math.pi / 2, 1.1, 24, -sgn)
        items.append((sp2, 3.2, (0.1, 0.5)))
        for t in (0.3, 0.55, 0.8):
            px, py = cx + sgn * (26 + t * 150), cy + math.sin(t * math.pi * 1.2) * -16 + t * 6
            items.append(([(px, py), (px + sgn * 6, py - 7), (px + sgn * 14, py - 9)], 3.0, (0.0, 0.9)))
    m = strokes(W, H, items)
    shell = []
    for k in range(7):
        a = math.pi + (k + 0.5) * math.pi / 7
        shell.append(petal_pts(cx, cy + 12, 30, 7, a, 12))
    sm = shapes(W, H, shell)
    oval = ellipses(W, H, [(cx, cy + 14, 12, 9, 0)])
    art = gilt(blank(W, H), np.clip(m + sm + oval, 0, 1), nx)
    art = tint(art, inner_edge(sm, 1.5), "#5a3a12", 0.4, seed=nx())
    preview(art, "ob-orn", bg="#f4ead6")
    save(art, f"{OUT}/orn.webp", max_w=220, quality=84)
    clear()
