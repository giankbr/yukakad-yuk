"""Banten Surosowan — original painted art inspired by Banten Lama (architecture only, no figures, no calligraphy):
the five-tier tumpang roof of the Masjid Agung, the white tapering minaret with two balconies, and the low ruined
red-brick walls of Keraton Surosowan in front; soft Banten-batik inspired lattice tile and a pastel rosette.
Run: python3 -I banten-surosowan.py [part ...]   parts: scene wall batik rosette
Assets -> public/themes/art/banten-surosowan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h1_lib import *  # noqa
import _jw_lib as jw

OUT = outdir("banten-surosowan")
PARTS = sys.argv[1:] or ["scene", "wall", "batik", "rosette"]
BRICK = ("#b8674b", "#8f4a33", "#d5926f", "#e4c6ab", "#5e2c1e")
ROOF, ROOF_D, ROOF_L = "#57514f", "#38322f", "#8b8580"
WHITE, WHITE_D = "#f4efe6", "#c9c2c4"
LILAC, TEAL, PEACH, OCHRE = "#b9a9c4", "#7fa3a2", "#e9b99e", "#d2a85a"


def plaster(art, W, H, m, nx, x0, x1, amt=0.6):
    """Whitewashed plaster: warm white, cool lilac shade to the right, a few stains."""
    art = GP(art, m, WHITE, "#ece4da", seed=nx(), rough=1.0, streak=0.6)
    art = G(art, m * xgrad(W, H, x0 + (x1 - x0) * 0.35, x1) * amt, "#a99fb6", seed=nx(), density=0.55, edge=0.15, bloom=0.3, rough=1.5, feather=1.5)
    art = G(art, m * np.clip((fbm(W, H, nx(), 24, 3) - 0.62) * 2.5, 0, 1), "#bfae96", seed=nx(), density=0.3, edge=0.3, bloom=0.4, rough=1.5, feather=1.5)
    return art


def tile_roof(art, W, H, nx, cx, yb, yt, wb, wt):
    """One hipped tier seen in elevation: trapezoid of dark clay tile, tile courses, lit left, eave line."""
    m = poly(W, H, [(cx - wb / 2, yb), (cx - wt / 2, yt), (cx + wt / 2, yt), (cx + wb / 2, yb)])
    m = displace(m, nx(), 0.9, 8)
    art = GP(art, m, ROOF, ROOF_D, seed=nx(), rough=0.9, streak=0.8)
    rows = []
    n = max(3, int((yb - yt) / 5))
    for k in range(1, n):
        t = k / n
        y = yt + (yb - yt) * t
        hw = wt / 2 + (wb - wt) / 2 * t
        rows.append(([(cx - hw, y), (cx + hw, y)], 1.0, None))
    art = G(art, strokes(W, H, rows) * m, "#211c1a", seed=nx(), density=0.5, edge=0, rough=0.4, feather=0.4)
    # hip ridges
    hips = [([(cx - wt / 2, yt), (cx - wb / 2, yb)], 1.8, None), ([(cx + wt / 2, yt), (cx + wb / 2, yb)], 1.8, None)]
    art = G(art, strokes(W, H, hips), "#9a938c", seed=nx(), density=0.6, edge=0, rough=0.4, feather=0.4)
    art = G(art, m * np.clip(1 - xgrad(W, H, cx - wb / 2, cx), 0, 1), ROOF_L, seed=nx(), density=0.4, edge=0, bloom=0.3, rough=1, feather=2)
    art = G(art, m * xgrad(W, H, cx, cx + wb / 2), "#1e1a1a", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=1, feather=2)
    art = G(art, rect(W, H, cx - wb / 2 - 2, yb - 2, cx + wb / 2 + 2, yb + 2), "#2a2422", seed=nx(), density=0.8, edge=0, rough=0.4, feather=0.5)
    return art


def mosque(art, W, H, nx, rng, cx, gy, s=1.0):
    S = lambda v: v * s
    # platform + body
    art = plaster(art, W, H, rect(W, H, cx - S(170), gy - S(32), cx + S(170), gy), nx, cx - S(170), cx + S(170))
    art = G(art, rect(W, H, cx - S(172), gy - S(34), cx + S(172), gy - S(30)), "#8f8a8e", seed=nx(), density=0.5, edge=0, rough=0.4, feather=0.6)
    body = rect(W, H, cx - S(140), gy - S(110), cx + S(140), gy - S(32))
    art = plaster(art, W, H, body, nx, cx - S(140), cx + S(140))
    arches = []
    for k in range(7):
        x = cx - S(120) + k * S(40)
        arches.append([(x - S(11), gy - S(36))] + arc_pts(x, gy - S(78), S(11), math.pi, 2 * math.pi, 10) + [(x + S(11), gy - S(36))])
    art = G(art, shapes(W, H, arches, smooth=False), "#4a3a3a", "#5a4644", seed=nx(), density=0.85, edge=0.4, rough=0.5, feather=0.5)
    # five tiers
    tiers = [(gy - S(108), gy - S(154), S(364), S(246)),
             (gy - S(170), gy - S(206), S(262), S(180)),
             (gy - S(222), gy - S(250), S(192), S(128)),
             (gy - S(264), gy - S(286), S(136), S(86)),
             (gy - S(298), gy - S(330), S(92), S(8))]
    for i, (yb, yt, wb, wt) in enumerate(tiers):
        if i > 0:
            prev_t = tiers[i - 1][1]
            ww = tiers[i - 1][3] * 0.82
            wall = rect(W, H, cx - ww / 2, yb - 2, cx + ww / 2, prev_t + 1)
            art = plaster(art, W, H, wall, nx, cx - ww / 2, cx + ww / 2, amt=0.8)
            nwin = max(3, int(ww / S(26)))
            wins = [(cx - ww / 2 + (k + 0.5) * ww / nwin - S(3), prev_t - S(9), cx - ww / 2 + (k + 0.5) * ww / nwin + S(3), prev_t - S(2)) for k in range(nwin)]
            art = G(art, np.maximum.reduce([rect(W, H, *w_) for w_ in wins]), "#4a3a3a", seed=nx(), density=0.75, edge=0.3, rough=0.3, feather=0.4)
            art = G(art, rect(W, H, cx - ww / 2, prev_t - 2, cx + ww / 2, prev_t + 2), "#3a3030", seed=nx(), density=0.45, edge=0, rough=0.3, feather=1.2)
        art = tile_roof(art, W, H, nx, cx, yb, yt, wb, wt)
    # break the flatness: soft glaze mottling over the whole building, warm light from the left
    allm = art[..., 3] * rect(W, H, cx - S(185), gy - S(330), cx + S(185), gy)
    art = G(art, allm * np.clip((fbm(W, H, nx(), 40, 3) - 0.45) * 1.6, 0, 1), "#8c7a74", seed=nx(), density=0.28, edge=0.2, bloom=0.5, rough=3, feather=3)
    art = G(art, allm * np.clip(1 - xgrad(W, H, cx - S(180), cx), 0, 1), "#ffe6c8", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2, feather=3)
    # mustaka (crown finial)
    mk = shapes(W, H, [ellipse_pts(cx, gy - S(338), S(7), S(10), 12)])
    art = GP(art, mk, "#6b5b4a", "#4a3d32", seed=nx(), rough=0.4, streak=0.3)
    art = G(art, strokes(W, H, [([(cx, gy - S(346)), (cx, gy - S(364))], S(2.2), (0, 0.5))]), "#4a3d32", seed=nx(), density=0.9, edge=0, rough=0.3, feather=0.4)
    return art


def minaret(art, W, H, nx, rng, cx, gy, s=1.0):
    S = lambda v: v * s
    # pedestal
    ped = poly(W, H, [(cx - S(52), gy), (cx - S(46), gy - S(46)), (cx + S(46), gy - S(46)), (cx + S(52), gy)])
    art = plaster(art, W, H, ped, nx, cx - S(52), cx + S(52))
    art = G(art, rect(W, H, cx - S(48), gy - S(50), cx + S(48), gy - S(44)), "#9c9396", seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.5)
    # shaft (tapering, octagonal faces suggested by vertical shade bands)
    y0, y1 = gy - S(46), gy - S(250)
    shaft = poly(W, H, [(cx - S(36), y0), (cx - S(26), y1), (cx + S(26), y1), (cx + S(36), y0)])
    art = plaster(art, W, H, shaft, nx, cx - S(36), cx + S(36), amt=0.75)
    faces = [([(cx + d * S(14), y0), (cx + d * S(10), y1)], 1.2, None) for d in (-1, 1)]
    art = G(art, strokes(W, H, faces) * shaft, "#a59aa8", seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.8)
    # windows
    wins = [(cx - S(4), gy - S(y), cx + S(4), gy - S(y) + S(14)) for y in (90, 150, 210)]
    for (a, b, c, d) in wins:
        art = G(art, rect(W, H, a, b, c, d), "#3a3036", seed=nx(), density=0.85, edge=0.3, rough=0.3, feather=0.4)
    # balconies
    for (yb, ww) in ((gy - S(170), S(82)), (gy - S(250), S(74))):
        deck = rect(W, H, cx - ww / 2, yb - S(5), cx + ww / 2, yb + S(3))
        art = GP(art, deck, "#e9e1d6", "#cfc6c4", seed=nx(), rough=0.5, streak=0.4)
        rail = rect(W, H, cx - ww / 2 + S(3), yb - S(20), cx + ww / 2 - S(3), yb - S(5))
        art = G(art, rail, "#efe8de", seed=nx(), density=0.85, edge=0.3, rough=0.4, feather=0.4)
        bars = [([(cx - ww / 2 + S(6) + k * S(7), yb - S(18)), (cx - ww / 2 + S(6) + k * S(7), yb - S(6))], 1.2, None) for k in range(int((ww - S(12)) / S(7)) + 1)]
        art = G(art, strokes(W, H, bars), "#8e8590", seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
        art = G(art, rect(W, H, cx - ww / 2, yb + S(3), cx + ww / 2, yb + S(7)), "#5c5258", seed=nx(), density=0.4, edge=0, rough=0.3, feather=1)
    # upper drum + small roof + finial
    drum = rect(W, H, cx - S(18), gy - S(290), cx + S(18), gy - S(270))
    art = plaster(art, W, H, drum, nx, cx - S(18), cx + S(18))
    art = G(art, rect(W, H, cx - S(3), gy - S(286), cx + S(3), gy - S(274)), "#3a3036", seed=nx(), density=0.8, edge=0.3, rough=0.3, feather=0.4)
    cap = poly(W, H, [(cx - S(26), gy - S(288)), (cx, gy - S(318)), (cx + S(26), gy - S(288))])
    art = GP(art, cap, ROOF, ROOF_D, seed=nx(), rough=0.6, streak=0.5)
    art = G(art, cap * xgrad(W, H, cx, cx + S(26)), "#1e1a1a", seed=nx(), density=0.4, edge=0, rough=0.4, feather=1)
    art = G(art, strokes(W, H, [([(cx, gy - S(318)), (cx, gy - S(334))], S(2), (0, 0.5))]), "#4a3d32", seed=nx(), density=0.9, edge=0, rough=0.3, feather=0.4)
    return art


def ruins(art, W, H, nx, rng, segs, bottom):
    """Low broken brick walls: segs = [(x0, x1, ytop, amp)]. Lit top faces, shadowed fronts, grass at the foot."""
    for (x0, x1, yt, amp) in segs:
        pts = broken_top(x0, x1, yt, rng, amp=amp, step=10, bottom=bottom)
        m = poly(W, H, pts)
        art = bricks(art, W, H, m, nx, BRICK, bw=22, bh=8, seed=nx(), shade=ygrad(W, H, yt, bottom) * 0.5, weather=0.35)
        # lit crest: a thin light edge along the broken top
        crest = np.clip(m - np.roll(m, 7, 0), 0, 1)
        art = G(art, crest, "#efc2a0", seed=nx(), density=0.8, edge=0.2, rough=0.6, feather=0.7)
        art = G(art, np.clip(np.roll(crest, 7, 0) - crest, 0, 1) * m, "#4e241a", seed=nx(), density=0.35, edge=0, rough=0.5, feather=1)
        # missing bricks: dark recesses scattered over the face
        holes = []
        for _ in range(int((x1 - x0) / 40)):
            hx = rng.uniform(x0, x1); hy = rng.uniform(yt + 20, bottom - 10)
            holes.append([(hx, hy), (hx + 22, hy), (hx + 22, hy + 8), (hx, hy + 8)])
        hm = shapes(W, H, holes, smooth=False) * m
        art = G(art, hm, "#3e1d14", seed=nx(), density=0.7, edge=0.3, rough=0.5, feather=0.6)
        # moss in the cracks of the crest
        moss = crest * np.clip((fbm(W, H, nx(), 12, 2) - 0.6) * 4, 0, 1)
        art = G(art, gaussian_filter(moss, 2) * 2, "#7d8f5a", seed=nx(), density=0.6, edge=0.3, rough=1, feather=1)
        lich = m * np.clip((fbm(W, H, nx(), 30, 3) - 0.62) * 3, 0, 1) * ygrad(W, H, bottom - 80, bottom)
        art = G(art, lich, "#6f7d4c", seed=nx(), density=0.45, edge=0.3, bloom=0.4, rough=2, feather=1.5)
        clear()
    # grass tufts at the foot
    tufts = []
    for _ in range(int(W / 4)):
        x = rng.uniform(0, W)
        y = bottom - rng.uniform(0, 14)
        for _ in range(3):
            a = -math.pi / 2 + rng.uniform(-0.6, 0.6)
            L = rng.uniform(8, 22)
            tufts.append(([(x, y), (x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5), (x + math.cos(a) * L + rng.uniform(-3, 3), y + math.sin(a) * L)], rng.uniform(1.6, 2.6), (0.05, 0.6)))
    art = G(art, strokes(W, H, tufts), "#7f9a5a", "#5d7a45", seed=nx(), density=0.85, edge=0.3, rough=0.8, feather=0.5)
    return art


def part_scene():
    W, H = 780, 640
    rng = random.Random(41); nx = Seq(100)
    art = painted_sky(W, H, [(0, "#d8cfe3"), (0.35, "#e9dde6"), (0.62, "#f4dfd2"), (1, "#f0d6c0")], seed=8, streak=0.45)
    art = G(art, radial(W, H, 610, 330, 260, 0.7), "#fbe4c8", seed=nx(), density=0.5, edge=0, bloom=0.3, rough=4, feather=6)
    # soft clouds
    cl = ellipses(W, H, [(rng.uniform(0, W), rng.uniform(60, 260), rng.uniform(60, 140), rng.uniform(10, 22), 0) for _ in range(9)])
    art = G(art, displace(cl, nx(), 8, 40), "#ffffff", "#f6eef4", seed=nx(), density=0.45, edge=0.15, bloom=0.5, rough=6, feather=5)
    # old trees behind the site: soft rounded canopies, cool and pale with distance
    for (x, y, r, c1, c2, d) in [(60, 440, 90, "#b3b8ad", "#a3aa9f", 0.6), (180, 470, 60, "#a8b2a3", "#97a395", 0.6),
                                 (470, 455, 70, "#aab2a6", "#9ca697", 0.55), (730, 420, 110, "#aeb4a8", "#9aa396", 0.6),
                                 (520, 480, 40, "#9eab98", "#8f9d8a", 0.6)]:
        blobs = [(x + rng.uniform(-r, r) * 0.8, y + rng.uniform(-r, r) * 0.5, r * rng.uniform(0.35, 0.6), r * rng.uniform(0.3, 0.5), rng.uniform(-20, 20)) for _ in range(14)]
        tm = displace(ellipses(W, H, blobs), nx(), 6, 20)
        art = G(art, tm, c1, c2, seed=nx(), density=d, edge=0.45, bloom=0.45, rough=4, feather=1.5)
        art = G(art, tm * ygrad(W, H, y - r * 0.6, y + r * 0.6), "#7d8a7c", seed=nx(), density=0.3, edge=0, bloom=0.4, rough=3, feather=2)
        trunk = strokes(W, H, [([(x + 4, y + r * 0.2), (x - 2, y + r * 0.7), (x + 3, 520)], r * 0.07, (0, 0.1))])
        art = G(art, trunk, "#8b8690", seed=nx(), density=0.55, edge=0.3, rough=1, feather=0.6)
        clear()
    # ground band
    gm = rect(W, H, 0, 500, W, H)
    art = G(art, gm, "#c9c39a", "#b4b080", seed=nx(), density=0.75, edge=0.2, bloom=0.4, rough=3, feather=2)
    art = brushwork(art, gm, ["#b7b27c", "#a9a76f", "#cfc79c", "#9aa06a"], rng, nx, n=420, L=(12, 30), wd=(2, 4), ang=0.0, ang_var=0.15)
    path = poly(W, H, [(250, 640), (300, 515), (350, 515), (470, 640)], smooth=False)
    art = G(art, displace(path, nx(), 3, 20), "#e6d6bd", "#d9c6a8", seed=nx(), density=0.6, edge=0.3, bloom=0.4, rough=3, feather=2)
    shadow = poly(W, H, [(150, 512), (500, 512), (560, 530), (190, 532)], smooth=True)
    art = G(art, shadow, "#6f6a5a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3, feather=4)
    art = G(art, poly(W, H, [(548, 512), (652, 512), (700, 528), (560, 530)], smooth=True), "#6f6a5a", seed=nx(), density=0.35, edge=0.1, rough=3, feather=4)
    clear()
    art = over(art, mosque(blank(W, H), W, H, nx, rng, cx=320, gy=512, s=1.0))
    clear()
    mn = minaret(blank(W, H), W, H, nx, rng, cx=600, gy=512, s=1.0)
    mn = G(mn, mn[..., 3] * np.clip((fbm(W, H, nx(), 40, 3) - 0.45) * 1.6, 0, 1), "#8c7a74", seed=nx(), density=0.25, edge=0.2, bloom=0.5, rough=3, feather=3)
    art = over(art, mn)
    clear()
    # foreground ruined walls of the keraton, an opening framing the mosque
    art = ruins(art, W, H, nx, rng, [(-10, 210, 512, 30), (200, 455, 590, 12), (445, 790, 540, 28)], bottom=H + 6)
    clear()
    preview(art, "bt-scene")
    save_rgb(art, f"{OUT}/scene.webp", size=(780, 640), quality=76)
    clear()


def part_wall():
    """Stand-alone broken brick wall strip (transparent above), for section transitions."""
    W, H = 780, 150
    rng = random.Random(51); nx = Seq(700)
    art = blank(W, H)
    art = ruins(art, W, H, nx, rng, [(-10, 260, 40, 26), (250, 520, 72, 14), (510, 790, 50, 24)], bottom=H)
    preview(art, "bt-wall")
    save_full(art, f"{OUT}/wall.webp", size=(780, 150), quality=80)
    clear()


def part_batik():
    """Seamless soft Banten-batik inspired tile: pale ground, lilac and teal lozenge lattice with cream wax outlines,
    small four-petal flowers in the cells, a fine crackle (remukan)."""
    T = 240
    rng = np.random.default_rng(7)
    yy, xx = np.mgrid[0:T, 0:T].astype(np.float32)
    u = (xx / T) * 4 * math.tau / 2
    v = (yy / T) * 4 * math.tau / 2
    # lozenge lattice from |sin| sums (periodic in the tile)
    d = np.abs(np.sin(u * 0.5 + v * 0.5)) + 0  # placeholder
    a = (xx + yy) % 60
    b = (xx - yy) % 60
    line = np.minimum(np.minimum(a, 60 - a), np.minimum(b, 60 - b))
    cell_id = ((np.floor((xx + yy) / 60) + np.floor((xx - yy) / 60)) % 2)
    ground = np.ones((T, T, 3), np.float32) * col_arr("#f1ebe6")
    tint = np.where(cell_id[..., None] > 0.5, col_arr("#d9cfe0"), col_arr("#cfe0de"))
    ground = ground * 0.35 + tint * 0.65
    # cell centres: four-petal flower
    cx = ((xx + yy) % 60) - 30
    cy = ((xx - yy) % 60) - 30
    r = np.hypot(cx, cy)
    ang = np.arctan2(cy, cx)
    petal = (r < 14 * (0.55 + 0.45 * np.abs(np.cos(2 * ang)))) & (r > 3)
    centre = r <= 3.2
    flower_col = np.where(cell_id[..., None] > 0.5, col_arr("#9b86ad"), col_arr("#6f9997"))
    rgb = ground
    pm = gaussian_filter(petal.astype(np.float32), 0.6, mode="wrap")
    rgb = rgb * (1 - pm[..., None]) + flower_col * pm[..., None]
    cm = gaussian_filter(centre.astype(np.float32), 0.5, mode="wrap")
    rgb = rgb * (1 - cm[..., None]) + col_arr("#d6a865") * cm[..., None]
    # lattice band: brick-rose with cream wax lines either side
    band = np.clip((4.5 - line) / 1.2, 0, 1)
    wax = np.clip((1.2 - np.abs(line - 6.5)) / 0.8, 0, 1)
    rgb = rgb * (1 - band[..., None] * 0.85) + col_arr("#c88a78") * band[..., None] * 0.85
    rgb = rgb * (1 - wax[..., None] * 0.9) + col_arr("#fbf6ef") * wax[..., None] * 0.9
    # crackle + dye mottling (wrap-safe)
    n = gaussian_filter(rng.random((T, T)).astype(np.float32), 9, mode="wrap")
    n = (n - n.mean()) / (n.std() + 1e-6)
    crack = gaussian_filter(rng.random((T, T)).astype(np.float32), 1.6, mode="wrap")
    crack = np.clip((np.abs(crack - crack.mean()) < 0.004).astype(np.float32), 0, 1)
    rgb = rgb * (1 + n[..., None] * 0.025) * (1 - crack[..., None] * 0.18)
    rgb = np.clip(rgb, 0, 1)
    prev_rgb(np.tile(rgb, (2, 2, 1)), "bt-batik")
    rgb_save(rgb, f"{OUT}/batik.webp", quality=80)


def part_rosette():
    """Pastel rosette: eight brick-rose petals, lilac inner ring, ochre centre, cream wax outline (gouache)."""
    W = H = 300
    rng = random.Random(61); nx = Seq(1100)
    art = blank(W, H)
    c = W / 2
    def petals(r, w, off, col, col2, n=8):
        nonlocal art
        for k in range(n):
            m = shape_mask(W, H, petal_pts(c, c, r, w, k * math.tau / n + off, n=14))
            m = displace(m, nx(), 1.2, 10)
            art = GP(art, m, col, col2, seed=nx(), rough=0.8, streak=0.6, pad=6)
            e = np.clip(m - gaussian_filter(m, 1.5) * 1.25, 0, 1) * 3
            art = G(art, e, "#fbf6ee", seed=nx(), density=0.95, edge=0, rough=0.3, feather=0.4, pad=6)
            vein = stroke_mask(W, H, [(c + math.cos(k * math.tau / n + off) * r * t, c + math.sin(k * math.tau / n + off) * r * t) for t in np.linspace(0.45, 0.85, 6)], 2.2)
            art = G(art, vein, mix_hex(col2, "#3a2a2a", 0.3), seed=nx(), density=0.5, edge=0, rough=0.3, feather=0.4, pad=6)
    petals(140, 40, 0, "#cc8f7b", "#b8705d")
    petals(108, 30, math.pi / 8, "#bba9c6", "#a08cb2")
    disk = circles(W, H, [(c, c, 46)])
    art = GP(art, disk, "#7fa3a2", "#6a8f8f", seed=nx(), rough=0.8, streak=0.5)
    art = G(art, np.clip(disk - gaussian_filter(disk, 1.5) * 1.25, 0, 1) * 3, "#fbf6ee", seed=nx(), density=0.95, edge=0, rough=0.3, feather=0.4)
    art = GP(art, circles(W, H, [(c, c, 20)]), OCHRE, "#b88c40", seed=nx(), rough=0.5, streak=0.4)
    dots = [(c + math.cos(k * math.tau / 16) * 33, c + math.sin(k * math.tau / 16) * 33, 2.6) for k in range(16)]
    art = GP(art, circles(W, H, dots), "#fbf6ee", seed=nx(), rough=0.3, streak=0.2)
    preview(art, "bt-rosette")
    save(art, f"{OUT}/rosette.webp", max_w=160, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
