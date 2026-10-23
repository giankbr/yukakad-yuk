"""Batik Betawi — pesisir batik cloth: red ground, kembang kelapa (palm-frond wedding flower) in yellow & green, tiny
ondel-ondel drawn as a batik motif, tumpal (pucuk rebung) triangles of the kain's kepala, a nusa kelapa coastal panel
(palms, perahu, waves). Rendered as wax-resist dye: cream canting outlines left undyed, soaked colour, crackle.
Run: python3 -I batik-betawi.py [part ...]  parts: kain tumpal kembang nusa divider
Assets -> public/themes/art/batik-betawi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o1_lib import *

OUT = outdir("batik-betawi")
PARTS = sys.argv[1:] or ["kain", "tumpal", "kembang", "nusa", "divider"]
CREAM, CREAM_D = "#f7ead0", "#efdcb8"
RED, RED_D = "#c4252c", "#9e1a22"
GREEN, GREEN_D = "#1f7a3e", "#17602f"
YEL, YEL_D = "#f2b62a", "#e09a16"
INDIGO = "#2a2a52"


def cloth(W, H, seed):
    a = solid(W, H, CREAM)
    a = G(a, np.ones((H, W), np.float32) * fbm(W, H, seed, 40, 3), CREAM_D, seed=seed + 1, density=0.35, edge=0, bloom=0.3, rough=1)
    return a


def render(W, H, ground, layers, nx, gap=2.2, dots=None, base=None, alpha=None, crack=0.22):
    """Wax-resist render: cream cloth, ground dyed around motifs (leaving a cream outline gap), each motif layer dyed
    inside its eroded mask. layers: [(mask, col, col2)]. ground: (mask_or_None, col, col2)."""
    art = base if base is not None else cloth(W, H, nx())
    union = np.zeros((H, W), np.float32)
    for m, _, _ in layers:
        union = np.maximum(union, m)
    gm = ground[0] if ground[0] is not None else np.ones((H, W), np.float32)
    gmask = np.clip(gm - dilate(union, gap * 0.8), 0, 1)
    art = dye(art, gmask, ground[1], ground[2], nx, density=0.95, crack=crack)
    art = G(art, gmask * fbm(W, H, nx(), 60, 3), ground[2], seed=nx(), density=0.45, edge=0, bloom=0.3, rough=1)
    for i, (m, c1, c2) in enumerate(layers):
        later = np.zeros((H, W), np.float32)
        for m2, _, _ in layers[i + 1:]:
            later = np.maximum(later, m2)
        mm = np.clip(m - dilate(later, gap * 0.8), 0, 1) if i < len(layers) - 1 else m
        art = dye(art, erode(mm, gap * 0.55), c1, c2, nx, density=0.93, crack=crack * 0.6)
    if dots is not None:
        art = OV(art, dots * gmask, lambda q: flat(q, CREAM, 0.92))
    if alpha is not None:
        art = art.copy(); art[..., 3] = np.clip(alpha, 0, 1) * art[..., 3]
    return art


# ---------------------------------------------------------------- motifs (lists of polygons / stroke items)
def kembang_polys(cx, cy, R, n=18, rot0=0.0):
    """Kembang kelapa: radiating palm-leaf fronds around a round heart. Returns (fronds_a, fronds_b, heart, ring, tips)."""
    fa, fb, tips = [], [], []
    for k in range(n):
        a = rot0 + k * math.tau / n
        L = R * (0.78 if k % 2 else 1.0)
        x0, y0 = cx + math.cos(a) * R * 0.24, cy + math.sin(a) * R * 0.24
        p = petal_pts(x0, y0, L * 0.74, R * (0.1 if k % 2 else 0.13), a, n=12)
        (fa if k % 2 == 0 else fb).append(p)
        tips.append((cx + math.cos(a) * (R * 0.24 + L * 0.74 + R * 0.06), cy + math.sin(a) * (R * 0.24 + L * 0.74 + R * 0.06), R * 0.045))
    heart = ellipse_pts(cx, cy, R * 0.12, R * 0.12, 14)
    ring = [ellipse_pts(cx, cy, R * 0.2, R * 0.2, 18)]
    return fa, fb, heart, ring, tips


def ondel_polys(cx, cy, s):
    """Ondel-ondel as a batik motif: fan crown of kembang kelapa, round face, bell body with a sash. Returns dict."""
    crown = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.28
        crown.append(petal_pts(cx + math.cos(a) * 14 * s, cy - 26 * s + math.sin(a) * 10 * s, 26 * s, 3.6 * s, a, n=8))
    tips = [(cx + math.cos(-math.pi / 2 + (k - 4) * 0.28) * 42 * s, cy - 26 * s + math.sin(-math.pi / 2 + (k - 4) * 0.28) * 38 * s, 3 * s) for k in range(9)]
    face = ellipse_pts(cx, cy - 8 * s, 15 * s, 18 * s, 18)
    body = [(cx - 15 * s, cy + 12 * s), (cx + 15 * s, cy + 12 * s), (cx + 22 * s, cy + 40 * s), (cx + 30 * s, cy + 78 * s),
            (cx - 30 * s, cy + 78 * s), (cx - 22 * s, cy + 40 * s)]
    sash = [(cx - 19 * s, cy + 24 * s), (cx - 13 * s, cy + 18 * s), (cx + 26 * s, cy + 58 * s), (cx + 21 * s, cy + 66 * s)]
    eyes = [(cx - 5.5 * s, cy - 10 * s, 2.0 * s), (cx + 5.5 * s, cy - 10 * s, 2.0 * s)]
    smile = arc_pts(cx, cy - 4 * s, 6 * s, 0.4, math.pi - 0.4, 10)
    hem = [(cx + (t - 0.5) * 56 * s, cy + 70 * s) for t in np.linspace(0.08, 0.92, 6)]
    return dict(crown=crown, tips=tips, face=face, body=body, sash=sash, eyes=eyes, smile=smile, hem=hem)


def small_flower(cx, cy, r, rot0=0.0, n=6):
    return [petal_pts(cx, cy, r, r * 0.34, rot0 + k * math.tau / n, n=10) for k in range(n)]


# ---------------------------------------------------------------- assets
def kain():
    """Seamless 480 tile of the badan kain: kembang kelapa + ondel-ondel motif on red, isen dots."""
    W = H = 480
    nx = Seq(100); rng = random.Random(2)
    fa, fb, heart, tipsA = [], [], [], []
    for (cx, cy) in [(120, 120), (360, 360)]:
        a_, b_, h_, r_, t_ = kembang_polys(cx, cy, 92, 18, 0.1)
        fa += a_; fb += b_; heart += [h_]; tipsA += t_
    rings = [ellipse_pts(cx, cy, 20, 20, 18) for cx, cy in [(120, 120), (360, 360)]]
    on = [ondel_polys(cx, cy - 18, 1.18) for cx, cy in [(360, 120), (120, 360)]]
    flowers = small_flower(0, 0, 18, 0.78) + small_flower(240, 240, 18, 0.78)
    leaves = [petal_pts(240 + dx, 0 + dy, 26, 8, a, n=10) for (dx, dy, a) in [(0, 0, -0.6), (0, 0, math.pi + 0.6)]]
    leaves += [petal_pts(0 + dx, 240 + dy, 26, 8, a, n=10) for (dx, dy, a) in [(0, 0, -0.6), (0, 0, math.pi + 0.6)]]
    T = lambda polys: tile_polys(polys, W, H)
    m_fa = shapes(W, H, T(fa)); m_fb = shapes(W, H, T(fb))
    m_ring = np.clip(shapes(W, H, T(rings)) - shapes(W, H, T(heart)), 0, 1)
    m_heart = shapes(W, H, T(heart))
    m_tip = circles(W, H, [(x + dx, y + dy, r) for x, y, r in tipsA for dx in (-W, 0, W) for dy in (-H, 0, H)])
    m_crown = shapes(W, H, T(sum([o["crown"] for o in on], [])))
    m_face = shapes(W, H, T([o["face"] for o in on]))
    m_body = shapes(W, H, T([o["body"] for o in on]), smooth=False)
    m_sash = shapes(W, H, T([o["sash"] for o in on]), smooth=False) * m_body
    m_body = np.clip(m_body - dilate(m_sash, 1.4), 0, 1)
    m_otip = circles(W, H, [(x, y, r) for o in on for x, y, r in o["tips"]])
    m_fl = shapes(W, H, T(flowers)); m_lv = shapes(W, H, T(leaves))
    # isen-isen: cream dots in a loose grid avoiding motifs
    pts = []
    for y in range(6, H, 16):
        for x in range(6 + (y // 16 % 2) * 8, W, 16):
            pts.append((x + rng.uniform(-1.5, 1.5), y + rng.uniform(-1.5, 1.5)))
    dots = isen_dots(W, H, pts, 1.7)
    layers = [(m_fa, YEL, YEL_D), (m_fb, GREEN, GREEN_D), (m_ring, GREEN, GREEN_D), (m_heart, RED_D, RED_D), (m_tip, YEL, YEL_D),
              (m_crown, YEL, YEL_D), (m_otip, GREEN, GREEN), (m_face, "#f6d9a8", "#f0c98c"), (m_body, GREEN, GREEN_D), (m_sash, YEL, YEL_D),
              (m_fl, YEL, YEL_D), (m_lv, GREEN, GREEN_D)]
    art = render(W, H, (None, RED, RED_D), layers, nx, gap=2.6, dots=dots)
    # faces: friendly eyes + smile in red-brown dye, body isen (cream dots) on the green bell
    for o in on:
        art = G(art, circles(W, H, o["eyes"]), "#7a1a18", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5)
        art = G(art, strokes(W, H, [(o["smile"], 2.2, (0.2, 0.2))]), "#9e1a22", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.4)
        art = OV(art, circles(W, H, [(x, y, 2.2) for x, y in o["hem"]]) , lambda q: flat(q, CREAM, 0.95))
    # frond midribs (cream wax lines)
    ribs = []
    for (cx, cy) in [(120, 120), (360, 360)]:
        for k in range(18):
            a = 0.1 + k * math.tau / 18
            L = 92 * (0.78 if k % 2 else 1.0)
            ribs.append(([(cx + math.cos(a) * 92 * 0.3, cy + math.sin(a) * 92 * 0.3), (cx + math.cos(a) * (92 * 0.24 + L * 0.66), cy + math.sin(a) * (92 * 0.24 + L * 0.66))], 1.3, (0.1, 0.4)))
    art = OV(art, strokes(W, H, tile_items(ribs, W, H)), lambda q: flat(q, CREAM, 0.85))
    art = add_grain(art, 3, 0.035)
    # make seamless: geometry is invariant under the half shift, so blend with the half-offset copy at the edges
    sh = np.roll(np.roll(art, H // 2, 0), W // 2, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    k = np.clip(np.minimum(np.minimum(xx, W - 1 - xx) / (W / 2), np.minimum(yy, H - 1 - yy) / (H / 2)) * 5, 0, 1)[..., None]
    art = art * k + sh * (1 - k)
    preview(art, "bb-kain")
    save_rgb(art, f"{OUT}/kain.webp", quality=78)


def tumpal_art(nx, seed=4):
    """One tumpal (pucuk rebung) triangle pointing right, 120 x 160 tile (no ground outside the triangle)."""
    W, H = 132, 160
    tri = [(0, 2), (122, 80), (0, 158)]
    m_tri = shapes(W, H, [tri], smooth=False)
    inner = [(10, 26), (88, 80), (10, 134)]
    m_in = shapes(W, H, [inner], smooth=False)
    core = [(18, 50), (58, 80), (18, 110)]
    m_core = shapes(W, H, [core], smooth=False)
    m_ring = np.clip(m_in - dilate(m_core, 1.5), 0, 1)
    bud = small_flower(30, 80, 12, 0.0)
    m_bud = shapes(W, H, bud) * m_core
    m_core2 = np.clip(m_core - dilate(m_bud, 1.2), 0, 1)
    m_outer = np.clip(m_tri - dilate(m_in, 1.5), 0, 1)
    # little leaf ticks along the outer band
    ticks = []
    for t in np.linspace(0.12, 0.88, 6):
        for (ax, ay, bx, by) in [(0, 2, 122, 80), (0, 158, 122, 80)]:
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            ticks.append((x - 4, y + (6 if ay < 80 else -6)))
    dots = isen_dots(W, H, ticks, 2.0) * m_outer
    layers = [(m_outer, GREEN, GREEN_D), (m_ring, YEL, YEL_D), (m_core2, RED, RED_D), (m_bud, YEL, YEL_D)]
    art = render(W, H, (np.zeros((H, W), np.float32), RED, RED_D), layers, nx, gap=2.2, alpha=dilate(m_tri, 0.6) , crack=0.18)
    art = OV(art, dots, lambda q: flat(q, CREAM, 0.95))
    return art


def tumpal():
    nx = Seq(400)
    art = tumpal_art(nx)
    preview(art, "bb-tumpal", bg=CREAM)
    save_full(art, f"{OUT}/tumpal.webp", size=(66, 80), quality=84)
    rot = np.ascontiguousarray(np.rot90(art, -1))  # pointing down, for horizontal borders
    preview(rot, "bb-tumpalH", bg=CREAM)
    save_full(rot, f"{OUT}/tumpalH.webp", size=(80, 66), quality=84)


def kembang():
    """Kembang kelapa medallion: red scalloped disc with the radiating fronds, cream wax outline."""
    W = H = 440
    nx = Seq(600)
    cx = cy = W / 2
    disc_pts = [(cx + math.cos(a) * (196 + 9 * math.cos(a * 24)), cy + math.sin(a) * (196 + 9 * math.cos(a * 24))) for a in np.linspace(0, math.tau, 240, endpoint=False)]
    m_disc = shapes(W, H, [disc_pts])
    fa, fb, heart, ring, tips = kembang_polys(cx, cy, 168, 22, -math.pi / 2)
    m_fa = shapes(W, H, fa); m_fb = shapes(W, H, fb)
    m_heart = shapes(W, H, [heart]); m_ring = np.clip(shapes(W, H, ring) - dilate(m_heart, 1.5), 0, 1)
    m_tip = circles(W, H, tips)
    inner_ring = np.clip(circles(W, H, [(cx, cy, 186)]) - circles(W, H, [(cx, cy, 180)]), 0, 1)
    dots = isen_dots(W, H, [(cx + math.cos(a) * 176, cy + math.sin(a) * 176) for a in np.linspace(0, math.tau, 60, endpoint=False)], 2.2)
    layers = [(m_fa, YEL, YEL_D), (m_fb, GREEN, GREEN_D), (m_ring, GREEN, GREEN_D), (m_heart, YEL, YEL_D), (m_tip, YEL, YEL_D)]
    art = render(W, H, (m_disc, RED, RED_D), layers, nx, gap=3.0, dots=dots, alpha=dilate(m_disc, 0.6))
    art = OV(art, inner_ring * 0.0 + edge_ring(m_disc, 2.5), lambda q: flat(q, GREEN_D, 0.9))
    ribs = []
    for k in range(22):
        a = -math.pi / 2 + k * math.tau / 22
        L = 168 * (0.78 if k % 2 else 1.0)
        ribs.append(([(cx + math.cos(a) * 168 * 0.3, cy + math.sin(a) * 168 * 0.3), (cx + math.cos(a) * (168 * 0.24 + L * 0.66), cy + math.sin(a) * (168 * 0.24 + L * 0.66))], 2.0, (0.1, 0.4)))
    art = OV(art, strokes(W, H, ribs), lambda q: flat(q, CREAM, 0.85))
    preview(art, "bb-kembang", bg=CREAM)
    save(art, f"{OUT}/kembang.webp", max_w=320, quality=84)


def palm_polys(x, by, h, lean, rng):
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.4, by - h * 0.5), top], 24)
    fronds = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.08, 0.08)
        L = h * 0.4
        c = curve([top, (top[0] + math.cos(a) * L * 0.55, top[1] + math.sin(a) * L * 0.55 - h * 0.04), (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + L * 0.5)], 20)
        fronds.append(blade(0, 0, c, h * 0.032))
    nuts = [(top[0] + dx, top[1] + 8 + dy, h * 0.035) for dx, dy in [(-6, 4), (6, 5), (0, 10)]]
    return trunk, fronds, nuts


def nusa():
    """Nusa kelapa coastal panel (horizontal): palms, a perahu with a striped sail, islands, tiny ondel-ondel pair on
    the shore and stylised waves; green ground, cream outlines, yellow/red dye."""
    W, H = 760, 300
    nx = Seq(800); rng = random.Random(7)
    sea_y = 200
    # waves: scalloped cream-outlined bands
    waves_a, waves_b = [], []
    for row, y in enumerate([214, 240, 266, 292]):
        for x in np.arange(-40 + (row % 2) * 30, W + 60, 60):
            p = arc_pts(x, y, 30, math.pi, math.tau, 14) + arc_pts(x, y, 18, math.tau, math.pi, 12)
            (waves_a if row % 2 == 0 else waves_b).append(p)
    m_wa = shapes(W, H, waves_a); m_wb = shapes(W, H, waves_b)
    # islands
    isl = [[(380, sea_y + 4), (430, 170), (470, 158), (520, 176), (560, sea_y + 4)], [(560, sea_y + 4), (600, 182), (640, 178), (680, sea_y + 4)]]
    m_isl = shapes(W, H, isl)
    # perahu
    hull = [(420, 196), (560, 196), (540, 222), (444, 222)]
    sail = [(488, 70), (488, 188), (420, 182)]
    sail2 = [(496, 84), (496, 188), (552, 184)]
    m_hull = shapes(W, H, [hull], smooth=False)
    m_sail = shapes(W, H, [sail, sail2], smooth=False)
    stripes = strokes(W, H, [([(410, y), (560, y)], 5, None) for y in (110, 136, 162)]) * m_sail
    m_sail_r = np.clip(m_sail - stripes, 0, 1)
    mast = strokes(W, H, [([(492, 60), (492, 196)], 4, None)])
    # palms
    tr, fr, nuts = [], [], []
    for (x, h, lean) in [(70, 150, 0.12), (150, 118, -0.1), (712, 140, -0.12)]:
        t_, f_, n_ = palm_polys(x, sea_y + 6, h, lean, rng)
        tr.append((t_, 9, (0.0, 0.5))); fr += f_; nuts += n_
    m_tr = strokes(W, H, tr); m_fr = shapes(W, H, fr); m_nut = circles(W, H, nuts)
    # tiny ondel pair on the shore
    on = [ondel_polys(250, 124, 0.8), ondel_polys(316, 126, 0.76)]
    m_crown = shapes(W, H, sum([o["crown"] for o in on], []))
    m_face = shapes(W, H, [o["face"] for o in on])
    m_body = shapes(W, H, [o["body"] for o in on], smooth=False)
    m_sun = circles(W, H, [(600, 64, 30)])
    sand = shapes(W, H, [[(0, 186), (200, 180), (360, 190), (380, 206), (0, 210)]])
    rays = shapes(W, H, [petal_pts(640, 70, 22, 5, a, n=8) for a in []])
    pts = [(x + rng.uniform(-1, 1), y + rng.uniform(-1, 1)) for y in range(10, 200, 18) for x in range(10 + (y // 18 % 2) * 9, W, 18)]
    dots = isen_dots(W, H, pts, 1.6)
    layers = [(m_sun, YEL, YEL_D), (m_isl, "#5b9a4a", "#4a8a3e"), (sand, "#f0c46a", "#e8b450"), (m_wa, "#2f8f86", "#257a72"), (m_wb, YEL, YEL_D), (m_hull, RED, RED_D), (m_sail_r, YEL, YEL_D),
              (stripes, RED, RED_D), (mast, "#6a3a1c", "#6a3a1c"), (m_tr, "#8a5426", "#6a3a1c"), (m_fr, YEL, YEL_D), (m_nut, RED_D, RED_D),
              (m_crown, YEL, YEL_D), (m_face, "#f6d9a8", "#f0c98c"), (m_body, RED, RED_D)]
    art = render(W, H, (None, GREEN, GREEN_D), layers, nx, gap=2.4, dots=dots)
    for o in on:
        art = G(art, circles(W, H, o["eyes"]), "#7a1a18", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5)
        art = OV(art, circles(W, H, [(x, y, 1.8) for x, y in o["hem"]]), lambda q: flat(q, CREAM, 0.95))
    art = add_grain(art, 5, 0.03)
    preview(art, "bb-nusa")
    save_rgb(art, f"{OUT}/nusa.webp", size=(720, int(720 * H / W)), quality=78)


def divider():
    """A stem of kembang kelapa: small medallion between two curling leaf sprays with dots."""
    W, H = 460, 90
    nx = Seq(1000)
    fa, fb, heart, ring, tips = kembang_polys(230, 45, 38, 14, 0.0)
    m_fa = shapes(W, H, fa); m_fb = shapes(W, H, fb); m_h = shapes(W, H, [heart]); m_tip = circles(W, H, tips)
    lv = []
    for d in (-1, 1):
        for k, x in enumerate([290, 330, 370, 405]):
            xx = 230 + d * (x - 230)
            a = (-0.5 if k % 2 else 0.5) + (0 if d > 0 else math.pi)
            ang = (0 if d > 0 else math.pi) + (-0.75 if k % 2 else 0.75) * d
            lv.append(petal_pts(xx, 45, 30 - k * 3, 9 - k, ang, n=12))
    m_lv = shapes(W, H, lv)
    stem = strokes(W, H, [([(30, 45), (430, 45)], 4.0, (0.2, 0.2))])
    m_dot = circles(W, H, [(16, 45, 5), (444, 45, 5)])
    alpha = np.maximum.reduce([m_fa, m_fb, m_h, m_tip, m_lv, stem, m_dot])
    art = blank(W, H)
    art = dye(art, stem, GREEN_D, GREEN_D, nx, density=1.0, crack=0)
    art = dye(art, stem, GREEN_D, GREEN_D, nx, density=1.0, crack=0)
    for m, c1, c2 in [(m_lv, GREEN, GREEN_D), (m_fa, RED, RED_D), (m_fb, YEL, YEL_D), (m_h, GREEN, GREEN_D), (m_tip, RED, RED_D), (m_dot, RED, RED_D)]:
        art = dye(art, m, c1, c2, nx, crack=0.1)
    art = OV(art, edge_ring(np.maximum(m_fa, m_fb), 1.2) * 0.0, lambda q: flat(q, CREAM, 0.0))
    preview(art, "bb-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
