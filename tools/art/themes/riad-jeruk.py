"""Riad Jeruk — a Moroccan riad courtyard seen from above: green glazed roof-tile rim, carved plaster cornice, pastel
zellige floor, a lobed marble fountain with a zellige band and still pale water (names float on it), four orange trees
in square planters casting soft shadows. Plus: an orange tree in a pot (side view), a carved-plaster polylobed arch frame,
an orange sprig, a seamless zellige tile and a carved plaster frieze. No figures, no calligraphy.
Run: python3 -I riad-jeruk.py [part ...]  parts: court tree arch sprig tile frieze"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h4_lib import *  # noqa

OUT = outdir("riad-jeruk")
PARTS = sys.argv[1:] or ["court", "tree", "arch", "sprig", "tile", "frieze"]
CREAM, BLUSH, MINT, SKY, SAFF = "#f3ebdd", "#e6b3a2", "#a3cfbd", "#93bcd2", "#e6c477"
LEAF_D, LEAF_M, LEAF_L = "#26472f", "#4f7f45", "#86b161"
ORANGE, ORANGE_L = "#e9852a", "#f6ae47"
TERRA = "#c9785a"
ROOF, ROOF_D = "#6aa58a", "#2e6a55"


def canopy(art, W, H, cx, cy, R, rng, seed, fruit=16, blossom=6, top=True):
    """Orange-tree crown seen from above (or the front when top=False): watercolour leaf dabs lit from the top-left."""
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, R, R * (1 if top else 0.9), 14), rng, 2, 0.07))
    art = G(art, base, "#3d6a3f", "#2a5032", seed=seed, density=0.9, edge=0.5, bloom=0.25, rough=5)
    for tone, col, n, bias in ((0, LEAF_D, 170, 0.5), (1, LEAF_M, 210, -0.15), (2, LEAF_L, 120, -0.55)):
        items = []
        for _ in range(n):
            a = rng.uniform(0, math.tau); r = R * math.sqrt(rng.uniform(0, 1)) * 0.98
            x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            # light side bias: lighter dabs toward top-left, darker toward bottom-right
            d = ((x - cx) + (y - cy)) / (R * 1.41)
            if tone == 2 and d > 0.25 + rng.uniform(-.2, .2):
                continue
            if tone == 0 and d < -0.2 + rng.uniform(-.2, .2):
                continue
            L = rng.uniform(R * 0.1, R * 0.17)
            items.append((x, y, L, L * 0.42, rng.uniform(0, 180)))
        m = ellipses(W, H, items) * (gaussian_filter(base, 2) > 0.2)
        art = G(art, m, col, col, seed=seed + 10 + tone, density=0.85, edge=0.6, bloom=0.15, rough=1.6, feather=0.8)
    fr = []
    for _ in range(fruit):
        a = rng.uniform(0, math.tau); r = R * math.sqrt(rng.uniform(0.05, 0.85))
        fr.append((cx + math.cos(a) * r, cy + math.sin(a) * r, rng.uniform(R * 0.065, R * 0.095)))
    fm = circles(W, H, fr)
    art = GP(art, fm, ORANGE, ORANGE_L, seed=seed + 30, rough=1.2, streak=0.6)
    art = tint(art, side_light(fm, -3, -3, 1.5) * fm, "#b85a1c", 0.55, seed=seed + 31)
    art = tint(art, circles(W, H, [(x - r * 0.35, y - r * 0.35, r * 0.28) for x, y, r in fr]), "#ffe2a4", 0.7, seed=seed + 32)
    bl = []
    for _ in range(blossom):
        a = rng.uniform(0, math.tau); r = R * math.sqrt(rng.uniform(0.1, 0.9))
        bx, by = cx + math.cos(a) * r, cy + math.sin(a) * r
        for k in range(5):
            t = k * math.tau / 5 + rng.uniform(0, 1)
            bl.append((bx + math.cos(t) * 3.2, by + math.sin(t) * 3.2, 2.6))
    if bl:
        art = OV(art, circles(W, H, bl), lambda m: col_arr(m, "#fffaf0", m * 0.95), pad=4)
    return art


if "court" in PARTS:
    W = H = 800
    B = 40
    rng = random.Random(7)
    xx, yy = grid_xy(W, H)
    # floor zellige
    lab, ids = zellige_star(W, H, 58, [CREAM, BLUSH, MINT, SKY, SAFF], ox=400, oy=400, seed=3, wob=1.0)
    art = paint_pieces(lab, [CREAM, BLUSH, MINT, SKY, SAFF], seed=4, jitter=0.06, grout="#efe7d8", cell_ids=ids)
    # roof rim: barrel tiles perpendicular to the nearest edge
    dl, dr, dt, db = xx, W - 1 - xx, yy, H - 1 - yy
    dmin = np.minimum(np.minimum(dl, dr), np.minimum(dt, db))
    along = np.where(dmin == dt, xx, np.where(dmin == db, xx, yy))
    roof = (dmin < B).astype(np.float32)
    ph = (along / 15.0) % 1.0
    ridge = np.sin(ph * math.pi)  # 0 at channel, 1 at ridge top
    rows = (dmin / 15.0) % 1.0
    lap = np.clip((rows - 0.78) * 6, 0, 1)  # tile overlap shadow
    col_id = np.floor(along / 15.0) + np.floor(dmin / 15.0) * 131 + (dmin == dt) * 7 + (dmin == dl) * 13
    cj = (((col_id * 2654435761) % 1000003) / 1000003.0).astype(np.float32)
    rr = (rgb_of(ROOF) * (1 - cj[..., None] * 0.35) + rgb_of("#8fbf8a") * cj[..., None] * 0.35) * (0.62 + 0.5 * ridge[..., None]) * (1 - 0.25 * lap[..., None]) * (0.88 + 0.2 * cj[..., None])
    rr = rr * (0.9 + 0.2 * fbm(W, H, 21, 30, 3)[..., None])
    gl = np.clip((ridge - 0.8) * 5, 0, 1) * (0.5 + 0.5 * fbm(W, H, 22, 12, 2))
    rr = rr + (1 - rr) * gl[..., None] * 0.45
    hip = np.exp(-np.abs(np.abs(xx - W / 2) - np.abs(yy - H / 2)) ** 2 / 6) * (dmin < B)
    rr = rr * (1 - 0.35 * hip[..., None])
    roofl = np.concatenate([np.clip(rr, 0, 1), roof[..., None]], -1)
    roofl[..., 3] = np.clip(gaussian_filter(displace(roof, 23, 1.5, 10), 0.6) * 1.2, 0, 1)
    # cast shadow of roof + cornice onto floor (light from top-left)
    inner = ((dmin >= B) * 1.0).astype(np.float32)
    shadow = np.clip(gaussian_filter((1 - inner), 10) * 1.6, 0, 1)
    sh_dir = np.clip(gaussian_filter(np.roll(np.roll(1 - inner, 16, 0), 16, 1), 8), 0, 1)
    art = OV(art, sh_dir * inner, lambda m: col_arr(m, "#5c4a5a", m * 0.32), pad=0)
    # cornice: carved plaster strip with dentils
    corn = ((dmin >= B - 2) & (dmin < B + 14)).astype(np.float32)
    art = OV(art, corn, lambda m: col_arr(m, "#f6efe2", m), pad=0)
    dent = corn * (((along / 9.0) % 1.0) < 0.42) * ((dmin > B + 3) & (dmin < B + 10))
    art = OV(art, dent.astype(np.float32), lambda m: col_arr(m, "#b9a68c", m * 0.65), pad=0)
    art = over(art, roofl)
    art = tint(art, ((dmin > B + 12) & (dmin < B + 16)).astype(np.float32), "#8a7a6a", 0.35, seed=5, clip=True)

    # four orange trees in square planters
    for k, (cx, cy) in enumerate([(150, 150), (650, 150), (150, 650), (650, 650)]):
        rngk = random.Random(40 + k)
        s = 80
        pl = rect_mask(W, H, cx - s, cy - s, cx + s, cy + s, rot=math.pi / 4)
        art = OV(art, np.roll(np.roll(gaussian_filter(pl, 5), 12, 0), 12, 1) * 0.6, lambda m: col_arr(m, "#4e3c48", m * 0.45))
        art = GP(art, pl, TERRA, "#b8634a", seed=50 + k, rough=1.5)
        soil = rect_mask(W, H, cx - s + 12, cy - s + 12, cx + s - 12, cy + s - 12, rot=math.pi / 4)
        art = GP(art, soil, "#6e4a36", "#5a3a2c", seed=60 + k, rough=1.0)
        R = 90
        crown = circles(W, H, [(cx, cy, R)])
        art = OV(art, np.roll(np.roll(gaussian_filter(crown, 14), 34, 0), 30, 1), lambda m: col_arr(m, "#38304a", m * 0.42))
        art = canopy(art, W, H, cx, cy, R, rngk, 70 + k * 13)
        clear()

    # fountain
    C = 400
    def lobed(R, amp, n=16, rot=0.0):
        return [(C + math.cos(t) * (R + amp * math.cos(n * (t + rot))), C + math.sin(t) * (R + amp * math.cos(n * (t + rot))))
                for t in np.linspace(0, math.tau, 240, endpoint=False)]
    outer = shape_mask(W, H, lobed(226, 5, n=24), smooth=False)
    art = OV(art, np.roll(np.roll(gaussian_filter(outer, 10), 16, 0), 16, 1), lambda m: col_arr(m, "#4c3f52", m * 0.38))
    art = GP(art, outer, "#f7f2e8", "#ece3d3", seed=81, rough=1.0, streak=0.4)
    art = tint(art, side_light(outer, -6, -6, 3), "#b7aa98", 0.6, seed=82)
    band = circles(W, H, [(C, C, 212)])
    blab, bids = zellige_star(W, H, 15, ["#f4ecdf", BLUSH, SKY, MINT, SAFF], ox=C, oy=C, seed=83, wob=0.4)
    bl = paint_pieces(np.where(band > 0.5, blab, -1), ["#f4ecdf", BLUSH, SKY, MINT, SAFF], seed=84, jitter=0.05, grout="#f1e9db", grout_w=0.9, cell_ids=bids)
    bl[..., 3] *= band
    art = over(art, bl)
    lip = circles(W, H, [(C, C, 196)])
    art = GP(art, lip, "#f6f0e4", "#e9e0cf", seed=85, rough=0.8)
    water = circles(W, H, [(C, C, 187)])
    art = OV(art, water, lambda m: col_arr(m, "#cfe6e1", m), pad=4)
    art = G(art, water, "#b4dad6", "#a3cfd0", seed=86, density=0.55, edge=0.3, bloom=0.4, rough=2, mottle=0.6)
    # depth: the lip shades the water on the top-left
    art = tint(art, side_light(water, 14, 14, 9) * water, "#6ea6aa", 0.55, seed=87)
    # ripple rings
    rp = []
    for k, r in enumerate([46, 78, 112, 150]):
        a0 = rng.uniform(0, math.tau)
        for seg in range(3):
            s0 = a0 + seg * math.tau / 3 + rng.uniform(0, .4)
            rp.append((arc_pts(C, C, r, s0, s0 + rng.uniform(1.2, 1.7), 30), 2.4 - k * 0.3))
    art = G(art, strokes(W, H, rp), "#8cbfbf", seed=88, density=0.45, edge=0.2, bloom=0, rough=1, feather=1.2)
    gl = [([(C - 120 + i * 9, C - 92 + i * 3 + j * 16) for i in range(6)], 2.2) for j in range(3)]
    art = OV(art, strokes(W, H, gl) * water, lambda m: col_arr(m, "#ffffff", gaussian_filter(m, 1.2) * 0.55), pad=4)
    # floating blossoms
    fl = []
    for bx, by in [(512, 520), (528, 500), (300, 268), (548, 318)]:
        for k in range(5):
            t = k * math.tau / 5 + rng.uniform(0, 1)
            fl.append((bx + math.cos(t) * 4.5, by + math.sin(t) * 4.5, 3.6))
    art = OV(art, circles(W, H, fl), lambda m: col_arr(m, "#fffbf2", m * 0.95), pad=4)
    art = OV(art, circles(W, H, [(512, 520, 1.8), (528, 500, 1.8), (300, 268, 1.8), (548, 318, 1.8)]), lambda m: col_arr(m, "#e8b24a", m), pad=4)
    # a fallen orange on the floor and loose leaves
    art = GP(art, circles(W, H, [(318, 690, 9)]), ORANGE, ORANGE_L, seed=91)
    lv = shapes(W, H, [petal_pts(300, 704, 16, 7, 2.6), petal_pts(486, 112, 15, 6, 0.9), petal_pts(660, 420, 14, 6, 4.1)])
    art = G(art, lv, LEAF_M, LEAF_D, seed=92, density=0.85)
    art = add_grain(art, 5, 0.035)
    art[..., 3] = 1
    preview(art, "riad-court", bg="#f3ebdd")
    save_rgb(art, f"{OUT}/court.webp", size=(780, 780), quality=80)
    clear()


def carve(art, mask, lines, seed, deep="#a8937a", hi="#fffaf0"):
    """Incised plaster: shadow on the top-left wall of each cut, highlight on the lower-right lip."""
    ln = lines * mask
    art = tint(art, np.clip(ln - np.roll(np.roll(ln, 1, 0), 1, 1) * 0.6, 0, 1), deep, 0.85, seed=seed, streak=0.3)
    art = tint(art, np.clip(np.roll(np.roll(ln, 2, 0), 2, 1) - ln, 0, 1) * mask, hi, 0.7, seed=seed + 1, streak=0.3)
    return art


def zel_edges(W, H, c, ox, oy, seed, wob=0.8):
    lab, ids = zellige_star(W, H, c, ["a"] * 5, ox=ox, oy=oy, seed=seed, wob=wob)
    e = (np.abs(np.diff(ids, axis=0, prepend=ids[:1])) > 0) | (np.abs(np.diff(ids, axis=1, prepend=ids[:, :1])) > 0)
    return np.clip(gaussian_filter(e.astype(np.float32), 0.7) * 2.2, 0, 1)


if "tree" in PARTS:
    W, H = 380, 640
    rng = random.Random(11)
    art = blank(W, H)
    cx = 190
    # pot: tapered terracotta with a painted rim band
    pot = shape_mask(W, H, [(118, 498), (262, 498), (246, 622), (134, 622)], smooth=False)
    art = GP(art, pot, TERRA, "#b9654a", seed=12, rough=1.4)
    art = tint(art, side_light(pot, -14, 0, 6), "#7d3e2c", 0.6, seed=13)
    rimm = shape_mask(W, H, [(108, 478), (272, 478), (268, 506), (112, 506)], smooth=False)
    art = GP(art, rimm, "#d58a6a", "#c47658", seed=14, rough=1.0)
    band = shape_mask(W, H, [(124, 522), (256, 522), (254, 540), (126, 540)], smooth=False)
    art = GP(art, band, "#f2e8d8", seed=15, rough=0.8)
    dots = circles(W, H, [(132 + i * 14, 531, 4.2) for i in range(9)])
    art = GP(art, dots, SKY, MINT, seed=16, rough=0.4)
    art = GP(art, circles(W, H, [(139 + i * 14, 531, 2.0) for i in range(8)]), BLUSH, seed=17, rough=0.3)
    # trunk
    tr = strokes(W, H, [([(190, 482), (186, 420), (192, 360), (188, 300)], 13, (0.0, 0.4)), ([(190, 380), (220, 330), (236, 300)], 6, (0.0, 0.5)), ([(188, 400), (160, 350), (150, 318)], 5, (0.0, 0.5))])
    art = GP(art, tr, "#7a5a40", "#5d4330", seed=18, rough=0.8)
    art = tint(art, side_light(tr, -3, 0, 1.5), "#3e2a1e", 0.6, seed=19)
    art = canopy(art, W, H, cx, 186, 168, rng, 20, fruit=22, blossom=8, top=False)
    preview(art, "riad-tree", tone="#f3ebdd")
    save(art, f"{OUT}/tree.webp", max_w=300, quality=82)
    clear()

if "arch" in PARTS:
    W, H = 640, 860
    art = blank(W, H)
    panel = np.ones((H, W), np.float32)
    C, base, R = 320, 330, 218
    pts = [(C - R + 6, H + 4)]
    for t in np.linspace(math.pi, 2 * math.pi, 300):
        r = R - 22 + 22 * abs(math.sin(5.5 * (t - math.pi)))
        pts.append((C + math.cos(t) * r, base + math.sin(t) * r))
    pts.append((C + R - 6, H + 4))
    win = shape_mask(W, H, pts, smooth=False)
    win_soft = np.clip(displace(win, 31, 1.2, 12), 0, 1)
    plaster = np.clip(panel - win_soft, 0, 1)
    art = GP(art, plaster, "#f5eee2", "#ece2d1", seed=32, rough=0.6, streak=0.4)
    # pastel lime-wash in the spandrels and a mint molding round the window
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    spand = plaster * (yy < base + 10) * np.clip(1 - gaussian_filter(1 - circles(W, H, [(C, base, R + 70)]), 1), 0, 1) * 0 + plaster * (yy < base + 6)
    ring = np.clip(gaussian_filter(win, 9) * 2 - win * 2, 0, 1) * plaster
    art = G(art, spand * (1 - (gaussian_filter(win, 20) > 0.02)), BLUSH, "#efc9b8", seed=33, density=0.35, edge=0.3, bloom=0.4)
    art = G(art, (ring > 0.12).astype(np.float32) * plaster, MINT, SKY, seed=34, density=0.85, edge=0.5, rough=1.5)
    # carved interlace in spandrels + border
    lines = zel_edges(W, H, 30, C, base, 35)
    keep = plaster * (gaussian_filter(win, 14) < 0.02)
    art = carve(art, keep * (yy < base + 20), lines, 36)
    # side panels: vertical carved bands of small arcatures
    xx = np.mgrid[0:H, 0:W][1].astype(np.float32)
    cols = ((xx % 26) < 3).astype(np.float32) * (yy > base + 40)
    art = carve(art, keep, cols * ((xx < C - R - 20) | (xx > C + R + 20)), 37)
    # outer border line pair
    bord = (((xx > 14) & (xx < 18)) | ((xx > W - 18) & (xx < W - 14)) | ((yy > 14) & (yy < 18))).astype(np.float32)
    art = carve(art, plaster, bord, 38)
    # lobed molding edge shadow onto the opening (light top-left)
    art = tint(art, np.clip(gaussian_filter(win, 3) - win, 0, 1) * plaster * 2, "#9c8670", 0.5, seed=39)
    art = add_grain(art, 6, 0.03)
    preview(art, "riad-arch", bg="#7aa0a6")
    save_full(art, f"{OUT}/arch.webp", size=(560, 752), quality=82)
    clear()

if "sprig" in PARTS:
    W, H = 520, 400
    art = blank(W, H)
    st = strokes(W, H, [([(50, 300), (170, 244), (300, 184), (430, 140)], 6, (0.0, 0.5))])
    art = GP(art, st, "#5d4330", seed=2, rough=0.6)
    for k, (x, y, L, Wd, a) in enumerate([(168, 244, 150, 50, -2.5), (300, 184, 132, 46, -0.75), (420, 144, 96, 34, 0.25), (250, 214, 110, 38, 1.1)]):
        lm = shapes(W, H, [petal_pts(x, y, L, Wd, a, n=18)])
        art = G(art, lm, LEAF_M if k % 2 else "#5f8f4c", LEAF_D, seed=3 + k, density=0.95, edge=0.75, bloom=0.25, rough=1.4, feather=1.0)
        art = tint(art, side_light(lm, -6, -6, 4) * lm, LEAF_D, 0.4, seed=20 + k)
        ex, ey = x + math.cos(a) * L * 0.9, y + math.sin(a) * L * 0.9
        art = OV(art, strokes(W, H, [([(x, y), ((x + ex) / 2, (y + ey) / 2), (ex, ey)], 2.2, (0.0, 0.6))]), lambda m: col_arr(m, "#c9dca8", m * 0.7), pad=4)
    fr = circles(W, H, [(250, 268, 62)])
    art = GP(art, fr, ORANGE, ORANGE_L, seed=6, rough=1.2)
    art = tint(art, side_light(fr, -20, -20, 10) * fr, "#b45418", 0.55, seed=7)
    art = tint(art, circles(W, H, [(228, 246, 15)]), "#ffe1a0", 0.75, seed=8)
    art = OV(art, circles(W, H, [(262, 210, 6)]), lambda m: col_arr(m, "#4f6b34", m), pad=3)
    bl = circles(W, H, [(446 + math.cos(k * 1.2566) * 15, 214 + math.sin(k * 1.2566) * 15, 12) for k in range(5)])
    art = OV(art, bl, lambda m: col_arr(m, "#fffaf0", m), pad=3)
    art = tint(art, side_light(bl, -3, -3, 2) * bl, "#d8c8b0", 0.6, seed=9)
    art = OV(art, circles(W, H, [(446, 214, 6)]), lambda m: col_arr(m, "#e7b247", m), pad=3)
    preview(art, "riad-sprig", tone="#f3ebdd")
    save(art, f"{OUT}/sprig.webp", max_w=200, quality=84)
    clear()

if "tile" in PARTS:
    W = H = 256
    lab, ids = zellige_star(W, H, 64, [CREAM, BLUSH, MINT, SKY, SAFF], ox=0, oy=0, seed=3, wob=0)
    t = paint_pieces(lab, ["#2f5f58", "#e6b3a2", "#a3cfbd", SAFF, "#f3ebdd"], seed=4, jitter=0.05, grout="#e9dfcd", cell_ids=ids)
    t[..., 3] = 1
    save_rgb(t, f"{OUT}/tile.webp", quality=82)
    to_image(np.tile(t, (2, 2, 1))).convert("RGB").save(f"{PREV}/riad-tile-2x2.png")

if "frieze" in PARTS:
    W, H = 240, 64
    art = GP(blank(W, H), np.ones((H, W), np.float32), "#f5eee2", "#eee4d4", seed=41, rough=0)
    xx, yy = grid_xy(W, H)
    # blind arcature: little lobed arches every 30px over a dentil row
    ph = (xx % 30) - 15
    arch = (yy > 18 + np.sqrt(np.clip(144 - ph ** 2, 0, None)) * -1 + 12) & (yy < 50) & (np.abs(ph) < 12)
    a_m = arch.astype(np.float32)
    art = G(art, a_m, MINT, SKY, seed=42, density=0.45, edge=0.4, rough=0.8, feather=0.8)
    edge = np.clip(gaussian_filter(a_m, 0.8) - a_m * 0.98, 0, 1) * 3
    art = carve(art, np.ones_like(a_m), np.clip(edge, 0, 1), 43)
    den = (((xx % 10) < 4) & (yy > 54) & (yy < 60)).astype(np.float32)
    art = carve(art, np.ones_like(a_m), den, 44)
    ln = (((yy > 6) & (yy < 8)) | ((yy > 51) & (yy < 53))).astype(np.float32)
    art = carve(art, np.ones_like(a_m), ln, 45)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/frieze.webp", quality=84)
    to_image(np.tile(art, (2, 3, 1))).convert("RGB").save(f"{PREV}/riad-frieze.png")
