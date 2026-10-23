"""Asmat Ukir — inspired-by Asmat relief carving (stylised hooks/hornbill, mantis limbs, double spirals, river meanders
painted in lime white, red ochre and charcoal on dark wood) and a misty swamp river at dawn with a long dugout canoe,
mangrove stilt roots and nipah fronds (watercolour + gouache). Original designs, no figures.
Run: python3 -I asmat-ukir.py [part ...]   parts: river panel band medal canoe
Assets -> public/themes/art/asmat-ukir/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k2_lib import *

OUT = outdir("asmat-ukir")
PARTS = sys.argv[1:] or ["river", "panel", "band", "medal", "canoe"]
WOOD, WOOD_D, WOOD_L = "#4a2d1c", "#24150c", "#6a4329"
CHAR = "#1d1410"
LIME, LIME_D = "#efe7d6", "#d9ccb3"
OCHRE, OCHRE_D = "#b0472b", "#7e2e1c"


# ------------------------------------------------------------------ motifs (stroke items, filled polys) in px
def m_spiral(cx, cy, s, d=1):
    """Double (S) spiral: two inward curls joined by a sweep."""
    a = spiral_pts(cx - s * 0.42, cy, s * 0.04, s * 0.42, 0, 1.6, 50, d)[::-1]
    b = spiral_pts(cx + s * 0.42, cy, s * 0.42, s * 0.04, math.pi, 1.6, 50, d)
    return [(a, s * 0.16, (0.0, 0.0)), (b, s * 0.16, (0.0, 0.0))], []


def m_hook(cx, cy, s, flip=1):
    """Hornbill-inspired hook: a long curved beak with a casque bump curling into an eye spiral."""
    P = lambda u, v: (cx + u * s * flip, cy + v * s)
    beak = curve([P(-0.55, 0.55), P(-0.1, 0.5), P(0.35, 0.2), P(0.45, -0.2), P(0.15, -0.45)], 40)
    casque = curve([P(0.15, -0.45), P(-0.15, -0.5), P(-0.3, -0.3)], 20)
    eye = spiral_pts(*P(0.0, -0.05), s * 0.2, s * 0.03, math.pi * (0.5 if flip > 0 else 0.5), 1.2, 30, flip)
    return [(beak, s * 0.2, (0.05, 0.3)), (casque, s * 0.14, (0.0, 0.4)), (eye, s * 0.1, (0.0, 0.5))], []


def m_mantis(cx, cy, s):
    """Mantis-inspired limbs (wenet): a lozenge body with bent arms angling out and down, mirrored."""
    body = [(cx, cy - s * 0.55), (cx + s * 0.12, cy), (cx, cy + s * 0.55), (cx - s * 0.12, cy)]
    items = []
    for sgn in (-1, 1):
        for k, (yy, lift) in enumerate([(-0.3, 0.32), (0.08, 0.26), (0.42, 0.18)]):
            p0 = (cx + sgn * s * 0.1, cy + yy * s)
            p1 = (cx + sgn * s * 0.42, cy + (yy - lift) * s)
            p2 = (cx + sgn * s * 0.6, cy + (yy + 0.08) * s)
            items.append(([p0, p1, p2], s * 0.14, (0.0, 0.3)))
    return items, [body]


def m_meander(x0, x1, cy, amp, s, n=3):
    pts = [(x0 + (x1 - x0) * t, cy + math.sin(t * n * math.tau) * amp) for t in [i / 80 for i in range(81)]]
    return [(pts, s, (0.05, 0.05))], []


def teeth(x0, y0, x1, y1, n, up=True):
    """A row of triangles (sawtooth border)."""
    out = []
    w = (x1 - x0) / n
    for i in range(n):
        a = x0 + i * w
        out.append([(a, y1 if up else y0), (a + w / 2, y0 if up else y1), (a + w, y1 if up else y0)])
    return out


def paint_carving(art, W, H, white_items, white_polys, red_items, red_polys, nx, area):
    """Raised painted relief over charcoal-blackened grooves, all inside `area`."""
    wm = np.maximum(strokes(W, H, white_items) if white_items else 0, shapes(W, H, white_polys) if white_polys else 0)
    rm = np.maximum(strokes(W, H, red_items) if red_items else 0, shapes(W, H, red_polys) if red_polys else 0)
    wm = np.asarray(wm, np.float32) * area if np.ndim(wm) else np.zeros((H, W), np.float32)
    rm = np.asarray(rm, np.float32) * area if np.ndim(rm) else np.zeros((H, W), np.float32)
    allm = np.maximum(wm, rm)
    groove = np.clip(gaussian_filter(allm, 3.0) * 3.6, 0, 1) * area
    art = G(art, groove, CHAR, "#2a1a12", seed=nx(), density=0.85, edge=0.3, bloom=0.1, rough=1.2, feather=0.8)
    if wm.max() > 0:
        art = GP(art, wm, LIME, LIME_D, seed=nx(), rough=1.0, streak=0.8, dry=0.22)
    if rm.max() > 0:
        art = GP(art, rm, OCHRE, OCHRE_D, seed=nx(), rough=1.0, streak=0.8, dry=0.18)
    art = relief(art, W, H, allm, CHAR, CHAR, nx, depth=2, hi_alpha=0.35, lo_alpha=0.55)
    return art


if "panel" in PARTS:
    # vertical carved plank tile (repeat-y): seams fall on a carved groove ring at top/bottom
    W, H = 150, 600
    nx = Seq(41100); rng = random.Random(41)
    art = blank(W, H)
    plank = polys(W, H, [rect(0, 0, W, H)])
    art = WD(art, plank, WOOD_L, WOOD, seed=nx(), vertical=True, rough=0.3)
    # side borders: sawtooth teeth columns
    side_l = polys(W, H, [rect(0, 0, 22, H)]); side_r = polys(W, H, [rect(W - 22, 0, W, H)])
    art = G(art, np.maximum(side_l, side_r), WOOD_D, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.8)
    tl, tr = [], []
    for k in range(20):
        y = k * 30
        tl.append([(3, y + 2), (19, y + 15), (3, y + 28)])
        tr.append([(W - 3, y + 2), (W - 19, y + 15), (W - 3, y + 28)])
    area = plank
    # rings at the seams
    rings_ = [([(0, 4), (W, 4)], 5, None), ([(0, H - 4), (W, H - 4)], 5, None), ([(0, 200), (W, 200)], 4, None), ([(0, 400), (W, 400)], 4, None)]
    art = G(art, strokes(W, H, rings_), CHAR, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    cx = W / 2
    wi, wp, ri, rp = [], [], [], []
    a, b = m_hook(cx - 27, 102, 48, 1); wi += a
    a, b = m_hook(cx + 27, 102, 48, -1); ri += a
    a, b = m_spiral(cx, 300, 50); wi += a
    ri += [([(cx - 36, 250), (cx + 36, 250)], 6, None), ([(cx - 36, 350), (cx + 36, 350)], 6, None)]
    a, b = m_mantis(cx, 500, 96); wi += a; rp += b
    wp += tl; rp += tr
    art = paint_carving(art, W, H, wi, wp, ri, rp, nx, area)
    # dot rows in lime
    dots_ = circles(W, H, [(cx + dx, y, 3.2) for y in (36, 168, 232, 368, 432, 568) for dx in (-18, 0, 18)])
    art = GP(art, dots_, LIME, LIME_D, seed=nx(), rough=0.5, dry=0.1)
    art = add_grain(art, 3, 0.03)
    show(art, "as-panel")
    save_full(art, f"{OUT}/panel.webp", quality=80)
    clear()

if "band" in PARTS:
    # horizontal divider: a carved strip with a river meander, spirals at the ends
    W, H = 640, 96
    nx = Seq(41200); rng = random.Random(42)
    art = blank(W, H)
    strip = shapes(W, H, [[(40, 22), (W - 40, 22), (W - 6, 48), (W - 40, 74), (40, 74), (6, 48)]], smooth=False)
    art = WD(art, strip, WOOD_L, WOOD, seed=nx(), vertical=False, rough=1.2)
    wi, _ = m_meander(110, W - 110, 48, 9, 7, n=4)
    ri = [([(110, 48 + 0), (W - 110, 48)], 0.1, None)]
    dots_ = [(110 + (W - 220) * (i + 0.5) / 8, 48 + (14 if i % 2 else -14), 4) for i in range(8)]
    a, _ = m_spiral(64, 48, 52); sp = a
    b, _ = m_spiral(W - 64, 48, 52, -1); sp += b
    art = paint_carving(art, W, H, wi, [], sp, [], nx, strip)
    art = GP(art, circles(W, H, dots_), OCHRE, OCHRE_D, seed=nx(), rough=0.6)
    show(art, "as-band")
    save(art, f"{OUT}/band.webp", max_w=320, quality=84)
    clear()

if "medal" in PARTS:
    # round carved medallion: paired hooks around a spiral eye, sawtooth rim
    W, H = 360, 360
    nx = Seq(41300); rng = random.Random(43)
    art = blank(W, H)
    cx, cy = 180, 180
    disc = shape_mask(W, H, deform(ellipse_pts(cx, cy, 170, 168, 16, 0.1), rng, 1, 0.01))
    art = WD(art, disc, WOOD_L, WOOD, seed=nx(), vertical=True, rough=1.0)
    yy, xx = grid(W, H)
    art = G(art, disc * np.clip(((xx - cx) + (yy - cy)) / 260, 0, 1), WOOD_D, seed=nx(), density=0.5, edge=0.2, bloom=0.2, rough=1)
    tooth = []
    for k in range(28):
        a0 = k / 28 * math.tau; a1 = (k + 0.5) / 28 * math.tau; a2 = (k + 1) / 28 * math.tau
        tooth.append([(cx + math.cos(a0) * 158, cy + math.sin(a0) * 158), (cx + math.cos(a1) * 134, cy + math.sin(a1) * 134), (cx + math.cos(a2) * 158, cy + math.sin(a2) * 158)])
    wi, ri = [], []
    a, _ = m_hook(cx - 58, cy - 6, 100, 1); wi += a
    a, _ = m_hook(cx + 58, cy - 6, 100, -1); ri += a
    eye = spiral_pts(cx, cy + 74, 22, 3, 0, 1.4, 40, 1)
    wi.append((eye, 9, (0.0, 0.4)))
    art = paint_carving(art, W, H, wi, [], ri, tooth, nx, disc)
    art = G(art, edge_of(disc, 3), CHAR, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1)
    show(art, "as-medal")
    save(art, f"{OUT}/medal.webp", max_w=200, quality=84)
    clear()


def canoe_masks(W, H, x0, x1, y, depth, rng):
    """Long dugout: thin hull, upswept carved prow at right, low stern at left."""
    L = x1 - x0
    top = [(x0 + L * t, y - math.sin(t * math.pi) * 0 - (t ** 6) * depth * 3.2 - ((1 - t) ** 8) * depth * 0.9) for t in [i / 60 for i in range(61)]]
    bot = [(x0 + L * (0.02 + 0.93 * t), y + depth * (0.35 + 0.65 * math.sin(t * math.pi) ** 0.5)) for t in [i / 60 for i in range(61)]]
    hull = shapes(W, H, [top + bot[::-1]], smooth=True)
    return hull, top


if "canoe" in PARTS or "river" in PARTS:
    pass


if "river" in PARTS:
    W, H = 780, 760
    nx = Seq(41400); rng = random.Random(44)
    yy, xx = grid(W, H)
    HZ = int(H * 0.50)
    sky = painted_sky(W, H, [(0, "#efe6d3"), (0.22, "#efe0c4"), (0.40, "#ecc9a0"), (0.5, "#e4b98e"), (1, "#c9a27c")], seed=5, streak=0.9)
    art = fade_alpha(sky, 0, H * 0.16)
    sun = circles(W, H, [(W * 0.70, HZ - 92, 30)])
    art = over(art, glow(sun, "#fbeed4", radius=50, strength=0.9))
    art = G(art, sun, "#f4d2a0", "#eab680", seed=nx(), density=0.7, edge=0.35, bloom=0.2, rough=1)
    cl = strokes(W, H, [(curve([(x0, y0), (x0 + L * 0.5, y0 - 5), (x0 + L, y0 + 2)], 20), w_, (0.3, 0.3)) for x0, y0, L, w_ in
                        [(40, 150, 300, 12), (430, 120, 280, 9), (500, 245, 240, 10), (120, 240, 180, 7), (260, 300, 220, 6)]])
    art = G(art, cl, "#f7ecda", "#e9cfb0", seed=nx(), density=0.6, edge=0.25, bloom=0.4, rough=6, feather=3)
    clear()
    # treeline: three receding layers of rounded jungle crowns with a few nipah/sago spikes
    for k, (base, col, col2, rr, dens) in enumerate([(HZ - 26, "#b7ad93", "#a69e86", 16, 0.55), (HZ - 12, "#8a8c70", "#77805f", 21, 0.72), (HZ + 2, "#52603f", "#3e4c31", 26, 0.9)]):
        cr = []
        x = -30
        while x < W + 30:
            x += rng.uniform(8, 16)
            r_ = rr * rng.uniform(0.6, 1.25)
            hump = 0.5 + 0.5 * math.sin(x / (90 + k * 30) + k)
            cr.append((x, base - r_ * 0.6 - hump * rr * 0.9 - (rr * 1.3 if rng.random() < 0.06 else 0), r_ * 1.1, r_, rng.uniform(-20, 20)))
        tl = np.maximum(ellipses(W, H, cr), polys(W, H, [rect(-10, base - rr * 0.6, W + 10, HZ + 3)]))
        art = G(art, tl, col, col2, seed=nx(), density=dens, edge=0.5, bloom=0.45, rough=3)
        if k == 2:
            fr = []
            for _ in range(26):
                fx = rng.uniform(0, W); fy = base - rng.uniform(40, 62)
                for j in range(7):
                    a = -math.pi / 2 + (j - 3) * 0.42 + rng.uniform(-0.1, 0.1)
                    L = rng.uniform(18, 30)
                    fr.append((curve([(fx, fy + 22), (fx + math.cos(a) * L * 0.6, fy + 22 + math.sin(a) * L * 0.6), (fx + math.cos(a) * L, fy + 22 + math.sin(a) * L + 6)], 8), 2.6, (0.0, 0.8)))
            art = G(art, strokes(W, H, fr), "#45543a", seed=nx(), density=0.75, edge=0.3, bloom=0, rough=1.2)
            dab = ellipses(W, H, [(rng.uniform(0, W), base - rng.uniform(0, 36), rng.uniform(3, 6), rng.uniform(2, 4), rng.uniform(-40, 40)) for _ in range(500)]) * tl
            art = G(art, dab, "#2f3b24", "#5d6c44", seed=nx(), density=0.4, edge=0.3, bloom=0, rough=1)
        mist = strokes(W, H, [(curve([(-20, base + 2), (W * 0.5, base - 4), (W + 20, base + 3)], 30), 14, (0.2, 0.2))])
        art = OV(art, gaussian_filter(mist, 6) * (0.55 if k < 2 else 0.25), lambda m: tint(m, "#f1e3cb", 1.0))
    clear()
    # water: warm silty mirror with the treeline reflected
    water = polys(W, H, [rect(-10, HZ, W + 10, H + 10)])
    band = art[HZ - 130:HZ].copy()
    art = GP(art, water, "#d9b48c", "#b58c66", seed=nx(), rough=1.0, streak=1.4)
    refl = np.zeros_like(art); refl[HZ:HZ + 130] = band[::-1]
    refl[..., 3] *= 0.55
    refl[..., :3] = refl[..., :3] * 0.85
    rr_ = gaussian_filter(refl, (2.2, 1.0, 0))
    wob = (fbm(W, H, 91, 14, 2) - 0.5) * 6
    from scipy.ndimage import map_coordinates
    for c in range(4):
        rr_[..., c] = map_coordinates(rr_[..., c], [yy, xx + wob], order=1, mode="nearest")
    art = over(art, rr_)
    deep = water * np.clip((yy - HZ - 120) / (H - HZ), 0, 1)
    art = G(art, deep, "#7a5a3c", "#5a4129", seed=nx(), density=0.6, edge=0.1, bloom=0.3, rough=4)
    sunr = []
    for k in range(80):
        y = HZ + 6 + (k / 80) ** 1.5 * 230
        x = W * 0.70 + rng.gauss(0, 10 + (y - HZ) * 0.22) - 0
        sunr.append(([(x - rng.uniform(6, 22), y), (x + rng.uniform(6, 22), y)], rng.uniform(2.6, 4.2), (0.3, 0.3)))
    art = OV(art, gaussian_filter(strokes(W, H, sunr), 0.6), lambda m: tint(m, "#fff1d6", 0.8))
    rip = [([(x, y), (x + rng.uniform(30, 90), y + rng.uniform(-1, 1))], 1.4, (0.3, 0.3)) for x, y in [(rng.uniform(-30, W), rng.uniform(HZ + 8, H)) for _ in range(80)]]
    art = G(art, strokes(W, H, rip) * water, "#efdcbc", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.5)
    clear()
    # the long dugout gliding across, carved prow at right, two paddles laid along the hull
    cy_ = HZ + 128
    hull, top = canoe_masks(W, H, 90, 640, cy_, 18, rng)
    shade = soft_shadow(hull, "#3a2618", blur=4, strength=0.3, dx=0, dy=7)
    art = over(art, shade)
    art = WD(art, hull, "#4f301d", "#26160c", seed=nx(), vertical=False, rough=0.8)
    art = G(art, hull * np.clip((yy - cy_) / 22, 0, 1), "#1d120b", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=1)
    gun = strokes(W, H, [([(x, y + 5) for x, y in top[4:54]], 3.4, (0.04, 0.04))]) * hull
    art = GP(art, gun, LIME, LIME_D, seed=nx(), rough=0.5, dry=0.25)
    tri = []
    for x, y in top[6:52:2]:
        tri.append([(x, y + 9), (x + 4.5, y + 15), (x + 9, y + 9)])
    art = GP(art, polys(W, H, tri) * hull, OCHRE, OCHRE_D, seed=nx(), rough=0.5)
    # prow board rising from the bow with a hornbill-inspired hook and spiral
    px, py = top[-1]
    board = shapes(W, H, [[(px - 30, py + 8), (px - 12, py - 40), (px + 6, py - 70), (px + 22, py - 64), (px + 10, py - 20), (px + 4, py + 10)]], smooth=True)
    art = WD(art, board, "#5a3822", "#2a180d", seed=nx(), vertical=True, rough=0.8)
    pr, _ = m_hook(px + 2, py - 36, 40, 1)
    art = paint_carving(art, W, H, pr, [], [([(px - 16, py - 2), (px - 4, py - 6)], 4, None)], [], nx, np.ones((H, W), np.float32))
    stern = shapes(W, H, [[(96, cy_ - 4), (84, cy_ - 22), (92, cy_ - 26), (106, cy_ - 6)]], smooth=True)
    art = WD(art, stern, "#5a3822", "#2a180d", seed=nx(), vertical=True, rough=0.6)
    pad_ = strokes(W, H, [([(200, cy_ - 4), (470, cy_ - 13)], 3.0, None), ([(300, cy_ - 2), (560, cy_ - 10)], 3.0, None)])
    blades = shapes(W, H, [deform(ellipse_pts(484, cy_ - 13.5, 22, 5.5, 10, -0.03), rng, 1, 0.02), deform(ellipse_pts(574, cy_ - 10.5, 22, 5.5, 10, -0.03), rng, 1, 0.02)])
    art = GP(art, np.maximum(pad_, blades), "#3a2417", "#24150c", seed=nx(), rough=0.4)
    art = GP(art, blades * (xx > 480) * (xx < 492), OCHRE, seed=nx(), rough=0.3)
    # canoe reflection + wake lines
    rf = np.zeros((H, W), np.float32)
    seg = hull[cy_ - 40:cy_ + 22]
    rf[cy_ + 22:cy_ + 84] = seg[::-1][:62]
    rf = gaussian_filter(rf, (2.5, 1.2)) * (0.5 + 0.5 * (np.sin(yy * 1.1) > -0.2))
    art = G(art, rf, "#3a2818", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=2)
    wake = strokes(W, H, [(curve([(80, cy_ + 20 + k * 7), (30, cy_ + 26 + k * 11), (-20, cy_ + 30 + k * 15)], 12), 1.6, (0.0, 0.6)) for k in range(3)])
    art = G(art, wake, "#f3e3c6", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6, feather=0.5)
    clear()
    # mangrove at right: trunk, arching stilt roots into the water, small-leaf crown
    rx = W - 70
    trunk = strokes(W, H, [(curve([(rx, H - 230), (rx + 10, H - 380), (rx + 20, HZ - 70)], 30), 22, (0.0, 0.3))])
    roots = []
    for k in range(8):
        end_x = rx - 150 + k * 30 + rng.uniform(-8, 8)
        sy = H - 240 + rng.uniform(-15, 25)
        roots.append((curve([(rx + rng.uniform(-6, 6), sy), (end_x + (rx - end_x) * 0.4, sy - 30), (end_x, H + 10)], 30), rng.uniform(6, 9), (0.0, 0.0)))
    rm_ = np.maximum(strokes(W, H, roots), trunk)
    art = G(art, rm_, "#5a4532", "#30241a", seed=nx(), density=0.95, edge=0.55, bloom=0.1, rough=1.2)
    art = G(art, rm_ * np.clip((xx - rx + 20) / 40, 0, 1), "#1e1610", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=1)
    body = ellipses(W, H, [(rx + 10 + rng.gauss(0, 46), HZ - 120 + rng.gauss(0, 26), rng.uniform(26, 44), rng.uniform(18, 28), rng.uniform(-30, 30)) for _ in range(26)])
    art = G(art, body, "#5f7041", "#34432a", seed=nx(), density=0.85, edge=0.55, bloom=0.4, rough=4)
    lv = []
    for _ in range(300):
        a = rng.uniform(0, math.tau); r_ = min(1.6, abs(rng.gauss(0, 0.7))) * 60
        lx, ly = rx + 10 + math.cos(a) * r_ * 1.3, HZ - 120 + math.sin(a) * r_ * 0.8
        lv.append(petal_pts(lx, ly, rng.uniform(12, 20), rng.uniform(5, 7), rng.uniform(0, math.tau), n=8))
    lm = shapes(W, H, lv)
    art = G(art, lm, "#6e7f4b", "#3b4b2a", seed=nx(), density=0.9, edge=0.6, bloom=0.25, rough=1.2, feather=0.6)
    art = G(art, lm * np.clip((yy - (HZ - 150)) / 110, 0, 1), "#26321b", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1)
    clear()

    def frond(art, base, ang, L, flip, cols=("#5f7444", "#2d3c23")):
        bx, by = base
        rach = curve([(bx, by), (bx + math.cos(ang) * L * 0.5, by + math.sin(ang) * L * 0.5 - L * 0.12), (bx + math.cos(ang) * L, by + math.sin(ang) * L + L * 0.25)], 44)
        lf = [(rach, 4.5, (0.0, 0.5))]
        for j in range(2, 43):
            x, y = rach[j]; x2, y2 = rach[j + 1]
            a = math.atan2(y2 - y, x2 - x)
            ll = L * 0.36 * (1 - abs(j - 15) / 34)
            for sgn in (-1, 1):
                qa = a + sgn * 0.75
                lf.append((curve([(x, y), (x + math.cos(qa) * ll * 0.55, y + math.sin(qa) * ll * 0.55), (x + math.cos(qa) * ll + math.cos(a) * 8, y + math.sin(qa) * ll + ll * 0.45)], 8), 7.5, (0.05, 0.75)))
        m = strokes(W, H, lf)
        art = G(art, m, cols[0], cols[1], seed=nx(), density=0.92, edge=0.65, bloom=0.25, rough=1.2, feather=0.7)
        return G(art, m * np.clip((yy - by + L * 0.3) / (L * 0.6), 0, 1), "#22301a", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1)
    art = frond(art, (-30, H - 10), -0.62, 360, 1)
    art = frond(art, (-40, H - 150), -0.18, 250, 1, ("#7b8a50", "#46582f"))
    art = frond(art, (W + 30, H + 10), math.pi + 0.7, 260, -1)
    art = add_grain(art, 7, 0.03)
    show(art, "as-river")
    save_full(art, f"{OUT}/river.webp", size=(780, 760), quality=78)
    clear()
