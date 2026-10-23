"""Arisan Keluarga — a monthly family arisan at home, in matte gouache: the kocokan glass full of rolled paper slips,
a single rolled slip (it pops out of the glass), an enamel 'blirik' teapot with two glasses of teh manis on a rattan
tray, a plate of kue (klepon with grated coconut, kue lapis, risoles), and the living room/teras where it all happens
(window with lace curtain, rattan chairs, snake plant, tegel floor and a crochet-covered table).
Run: python3 -I arisan-keluarga.py [part ...]   parts: kocokan slip teh kue teras divider
Assets -> public/themes/art/arisan-keluarga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h3_lib import *  # noqa

OUT = outdir("arisan-keluarga")
PARTS = sys.argv[1:] or ["kocokan", "slip", "teh", "kue", "teras", "divider"]
CREAM, MINT, TEAL, TERRA, BUTTER, PINK, RATTAN, INK = "#fbf2df", "#9fd3bd", "#2a7f7a", "#d0643c", "#f3c74e", "#ef9bb0", "#b9824a", "#3a2a22"
SLIP_COLS = [("#fffaf0", "#e8dcc4"), ("#f9d3dc", "#e6a9b8"), ("#fbe7a6", "#e9c55e"), ("#cdebdc", "#9fd3bd"), ("#fffaf0", "#e8dcc4"), ("#d6e6f7", "#a9c5e6")]


def rolled_slip(art, W, H, cx, cy, L, r, ang, nx, cols):
    """A rolled paper slip seen from the side: a rounded cylinder with a darker curled end and a seam line."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    body = shapes(W, H, [[P(-L / 2, -r), P(L / 2, -r), P(L / 2, r), P(-L / 2, r)]], smooth=False)
    endR = ellipses(W, H, [(P(L / 2, 0)[0], P(L / 2, 0)[1], r * 0.45, r, math.degrees(ang))])
    endL = ellipses(W, H, [(P(-L / 2, 0)[0], P(-L / 2, 0)[1], r * 0.45, r, math.degrees(ang))])
    m = np.clip(body + endR + endL, 0, 1)
    art = GP(art, m, cols[0], cols[1], seed=nx(), rough=1.0, streak=0.6, pad=8)
    # cylinder shading: darker along the bottom edge
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = ((xx - cx) * -sa + (yy - cy) * ca) / r
    art = shade(art, m, 1 - 0.22 * np.clip(v, 0, 1) + 0.06 * np.clip(-v, 0, 1))
    art = GP(art, endR * 0.9, cols[1], mix(cols[1], INK, 0.2), seed=nx(), rough=0.6, pad=6)
    spiral = spiral_pts(P(L / 2, 0)[0], P(L / 2, 0)[1], r * 0.6, 1, ang, 1.2, 18)
    sp = [(P(L / 2, 0)[0] + (x - P(L / 2, 0)[0]) * 0.45, y) for x, y in spiral]
    seam = strokes(W, H, [([P(-L / 2 + 2, r * 0.25), P(L / 2 - 2, r * 0.1)], 1.2, None), (sp, 1.0, None)])
    art = OV(art, seam, lambda mm: col_arr(mm, mix(cols[1], INK, 0.35), mm * 0.7), pad=6)
    return art


if "kocokan" in PARTS:
    W, H = 400, 500
    nx = Seq(101000); rng = random.Random(1010)
    cx = 200
    top, bot = 80, 452
    rt, rb = 128, 104
    art = blank(W, H)
    # table shadow
    art = OV(art, ellipses(W, H, [(cx + 14, bot + 16, 150, 18, 0)]), lambda m: col_arr(m, "#5a3a22", gaussian_filter(m, 10) * 0.3), pad=30)
    glass = shapes(W, H, [[(cx - rt, top)] + [(cx + math.cos(a) * rb, bot + math.sin(a) * 18) for a in np.linspace(math.pi, 0, 30)] + [(cx + rt, top)]], smooth=False)
    glass = np.clip(glass + ellipses(W, H, [(cx, top, rt, 22, 0)]), 0, 1)
    # back wall of the glass (faint)
    art = OV(art, glass, lambda m: col_arr(m, "#d8efe9", m * 0.35))
    # slips piled inside: from bottom up
    slips = []
    y = bot - 22
    row = 0
    while y > top + 64:
        hw = rb + (rt - rb) * (bot - y) / (bot - top) - 26
        n = 3 if row % 2 == 0 else 4
        for k in range(n):
            x = cx - hw + (k + 0.5 + (0.25 if row % 2 else 0)) * (2 * hw / (n + 0.4)) + rng.uniform(-8, 8)
            slips.append((x, y + rng.uniform(-6, 6), rng.uniform(56, 72), rng.uniform(11, 14), rng.uniform(-0.7, 0.7), SLIP_COLS[rng.randrange(len(SLIP_COLS))]))
        y -= 30; row += 1
    for i, (x, y_, L, r, a, c) in enumerate(slips):
        art = rolled_slip(art, W, H, x, y_, L, r, a, nx, c)
        if i % 4 == 3:
            clear()
    # keep slips inside the glass
    art[..., 3] *= np.clip(glass * 1.0 + (art[..., 3] > 0) * 0, 0, 1) if False else 1
    inside = gaussian_filter(glass, 1.0)
    art[..., 3] = np.where(inside > 0.02, art[..., 3], 0)
    # glass front: light tint, thick base, highlights, rim
    art = OV(art, glass, lambda m: col_arr(m, "#e6f6f2", m * 0.22))
    base = shapes(W, H, [[(cx - rb + 4, bot - 26)] + [(cx + math.cos(a) * (rb - 4), bot + math.sin(a) * 16) for a in np.linspace(math.pi, 0, 30)] + [(cx + rb - 4, bot - 26)]], smooth=False)
    art = OV(art, base, lambda m: col_arr(m, "#cfe9e3", m * 0.55))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hl = []
    hl.append(([(cx - rt + 26, top + 40), (cx - rb + 22, bot - 40)], 14, (0.15, 0.2)))
    hl.append(([(cx - rt + 52, top + 60), (cx - rb + 44, bot - 90)], 5, (0.2, 0.3)))
    hl.append(([(cx + rt - 30, top + 50), (cx + rb - 26, bot - 60)], 4, (0.2, 0.3)))
    hm = strokes(W, H, hl) * glass
    art = OV(art, hm, lambda m: col_arr(m, "#ffffff", m * 0.72))
    edge = np.clip(glass - gaussian_filter(glass, 3) * 1.15, 0, 1) * 2.5
    art = OV(art, np.clip(edge, 0, 1), lambda m: col_arr(m, "#3f8a80", m * 0.9))
    rim = np.clip(ellipses(W, H, [(cx, top, rt, 22, 0)]) - ellipses(W, H, [(cx, top + 2, rt - 7, 17, 0)]), 0, 1)
    art = OV(art, rim, lambda m: col_arr(m, "#f4fffc", m * 0.85))
    art = OV(art, np.clip(rim - np.roll(rim, -3, 0), 0, 1), lambda m: col_arr(m, "#4f9a90", m * 0.7))
    art = add_grain(art, 1011, 0.025)
    preview(art, "ak-kocokan", bg=CREAM)
    save(art, f"{OUT}/kocokan.webp", max_w=200, quality=86)
    clear()

if "slip" in PARTS:
    W, H = 200, 90
    nx = Seq(102000)
    art = rolled_slip(blank(W, H), W, H, 100, 45, 132, 22, -0.18, nx, ("#fffaf0", "#e8dcc4"))
    # red rubber thread
    art = G(art, strokes(W, H, [([(96, 22), (102, 70)], 3, None)]), "#d0643c", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=0.5, feather=0.5)
    preview(art, "ak-slip", bg=CREAM)
    save(art, f"{OUT}/slip.webp", max_w=100, quality=86)
    clear()

if "teh" in PARTS:
    W, H = 640, 400
    nx = Seq(103000); rng = random.Random(1030)
    art = blank(W, H)
    # rattan tray
    tray = ellipses(W, H, [(320, 330, 300, 56, 0)])
    art = GP(art, tray, RATTAN, "#9a6a3a", seed=nx(), rough=2, streak=0.8)
    weave = []
    for k in range(-30, 31):
        x = 320 + k * 10
        weave.append(([(x - 6, 280), (x + 6, 384)], 1.6, None))
    art = G(art, strokes(W, H, weave) * tray, "#7a4e26", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    inner = ellipses(W, H, [(320, 324, 270, 44, 0)])
    art = shade(art, inner, 0.88)
    rimt = np.clip(tray - ellipses(W, H, [(320, 330, 288, 48, 0)]), 0, 1)
    art = GP(art, rimt, "#c9925a", "#a8743e", seed=nx(), rough=1)
    # teapot (blirik enamel: white body, green speckled band, green rim)
    pcx, pby = 250, 330
    body = shapes(W, H, [[(pcx - 96, pby - 20), (pcx - 112, pby - 80), (pcx - 100, pby - 140), (pcx - 60, pby - 170), (pcx + 60, pby - 170), (pcx + 100, pby - 140), (pcx + 112, pby - 80), (pcx + 96, pby - 20), (pcx + 60, pby - 4), (pcx - 60, pby - 4)]])
    spout = strokes(W, H, [(curve([(pcx + 96, pby - 70), (pcx + 140, pby - 100), (pcx + 162, pby - 150), (pcx + 176, pby - 166)], 20), 22, (0.0, 0.5))])
    handle = np.clip(strokes(W, H, [(curve([(pcx - 98, pby - 130), (pcx - 150, pby - 128), (pcx - 152, pby - 70), (pcx - 104, pby - 54)], 24), 14, None)]), 0, 1)
    lid = np.clip(ellipses(W, H, [(pcx, pby - 170, 64, 14, 0)]) + ellipses(W, H, [(pcx, pby - 186, 16, 12, 0)]), 0, 1)
    green, green_d = "#2f8a5a", "#1f6a44"
    art = GP(art, np.clip(spout + handle, 0, 1), green, green_d, seed=nx(), rough=1.2)
    art = GP(art, body, "#f7f4ea", "#e6e0d0", seed=nx(), rough=1.5, streak=0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n = np.clip((xx - pcx) / 112, -1, 1)
    art = shade(art, body, 1.04 - 0.22 * np.clip(n + 0.2, 0, 1.2))
    band = body * ((yy > pby - 150) & (yy < pby - 112)).astype(np.float32)
    art = GP(art, band, green, green_d, seed=nx(), rough=1.0)
    speck = (np.random.default_rng(1031).random((H, W)) > 0.93).astype(np.float32)
    art = OV(art, gaussian_filter(speck, 0.6) * 2 * band, lambda m: col_arr(m, "#f7f4ea", np.clip(m, 0, 1) * 0.9))
    bot_rim = body * (yy > pby - 22).astype(np.float32)
    art = GP(art, bot_rim, green, green_d, seed=nx(), rough=1)
    art = GP(art, lid, green, green_d, seed=nx(), rough=1)
    art = OV(art, strokes(W, H, [([(pcx - 70, pby - 140), (pcx - 84, pby - 60)], 7, (0.2, 0.3))]), lambda m: col_arr(m, "#ffffff", m * 0.7))
    clear()
    # two glasses of teh manis with white lids
    for gx, gy in ((430, 330), (528, 316)):
        top, h = gy - 120, 116
        g = shapes(W, H, [[(gx - 36, top), (gx + 36, top), (gx + 30, gy), (gx - 30, gy)]], smooth=False)
        tea = shapes(W, H, [[(gx - 34, top + 16), (gx + 34, top + 16), (gx + 30, gy - 4), (gx - 30, gy - 4)]], smooth=False)
        art = OV(art, g, lambda m: col_arr(m, "#e8f3ef", m * 0.55))
        art = GP(art, tea, "#c2702a", "#9a4e1a", seed=nx(), rough=0.8, streak=0.4)
        art = shade(art, tea, 1 + 0.12 * np.clip(-(xx - gx) / 34, 0, 1) - 0.15 * np.clip((xx - gx) / 34, 0, 1))
        art = OV(art, strokes(W, H, [([(gx - 24, top + 24), (gx - 21, gy - 12)], 5, (0.2, 0.2))]), lambda m: col_arr(m, "#fff3dc", m * 0.65))
        lidm = np.clip(ellipses(W, H, [(gx, top - 2, 44, 9, 0)]) + ellipses(W, H, [(gx, top - 12, 10, 7, 0)]), 0, 1)
        art = GP(art, lidm, "#f7f4ea", "#e2dccb", seed=nx(), rough=0.8)
        art = GP(art, np.clip(ellipses(W, H, [(gx, top - 2, 44, 9, 0)]) - ellipses(W, H, [(gx, top - 4, 40, 6, 0)]), 0, 1), green, seed=nx(), rough=0.6)
        sc = ellipses(W, H, [(gx, gy + 4, 50, 10, 0)])
        art = GP(art, np.clip(sc - g, 0, 1), "#f7f4ea", "#e2dccb", seed=nx(), rough=0.8)
        clear()
    # steam
    st = []
    for x0 in (436, 532, 310):
        y0 = 180 if x0 != 310 else 140
        st.append((curve([(x0, y0), (x0 - 10, y0 - 30), (x0 + 8, y0 - 60), (x0 - 4, y0 - 92)], 30), 5, (0.3, 0.6)))
    art = OV(art, gaussian_filter(strokes(W, H, st), 1.5), lambda m: col_arr(m, "#ffffff", m * 0.6))
    art = add_grain(art, 1032, 0.025)
    preview(art, "ak-teh", bg=CREAM)
    save(art, f"{OUT}/teh.webp", max_w=300, quality=86)
    clear()

if "kue" in PARTS:
    W, H = 640, 360
    nx = Seq(104000); rng = random.Random(1040)
    art = blank(W, H)
    plate = ellipses(W, H, [(320, 236, 290, 74, 0)])
    art = OV(art, ellipses(W, H, [(330, 258, 290, 70, 0)]), lambda m: col_arr(m, "#5a3a22", gaussian_filter(m, 10) * 0.25), pad=30)
    art = GP(art, plate, "#fbfaf4", "#ece8dc", seed=nx(), rough=1.5)
    rimm = np.clip(plate - ellipses(W, H, [(320, 236, 276, 66, 0)]), 0, 1)
    art = GP(art, rimm, "#3a6ab0", "#2a5090", seed=nx(), rough=0.8)
    well = ellipses(W, H, [(320, 238, 200, 46, 0)])
    art = shade(art, well, 0.94)
    # banana leaf under the klepon
    leafm = shape_mask(W, H, petal_pts(150, 232, 170, 52, -0.08, 16))
    art = GP(art, leafm, "#5a9a3e", "#3e7a2e", seed=nx(), rough=1.5, streak=0.9)
    vein = strokes(W, H, [([(70, 240), (230, 226)], 2, (0.1, 0.4))])
    art = G(art, vein * leafm, "#2e5a22", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.4, feather=0.4)
    # klepon: green balls with grated coconut
    for x, y, r in ((110, 236, 26), (156, 226, 27), (202, 232, 26), (132, 196, 25), (180, 190, 25)):
        b = circles(W, H, [(x, y, r)])
        art = GP(art, b, "#4fa04a", "#3a8a3e", seed=nx(), rough=1.0, streak=0.4, pad=6)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.clip(((xx - x + r * 0.35) ** 2 + (yy - y + r * 0.4) ** 2) ** 0.5 / (r * 1.6), 0, 1)
        art = shade(art, b, 1.18 - 0.45 * d)
        flakes = []
        for _ in range(26):
            a = rng.uniform(0, math.tau); rr = r * math.sqrt(rng.random()) * 0.95
            fx, fy = x + math.cos(a) * rr, y + math.sin(a) * rr
            fa = rng.uniform(0, math.pi)
            flakes.append(([(fx, fy), (fx + math.cos(fa) * 5, fy + math.sin(fa) * 5)], 2.0, None))
        art = OV(art, strokes(W, H, flakes) * b, lambda m: col_arr(m, "#fffdf6", m * 0.95), pad=4)
        clear()
    # kue lapis: layered pink/white squares
    for x, y in ((330, 208), (378, 222)):
        cube_top = shapes(W, H, [[(x - 30, y - 30), (x + 18, y - 40), (x + 40, y - 24), (x - 8, y - 14)]], smooth=False)
        front = shapes(W, H, [[(x - 30, y - 30), (x - 8, y - 14), (x - 8, y + 30), (x - 30, y + 16)]], smooth=False)
        side = shapes(W, H, [[(x - 8, y - 14), (x + 40, y - 24), (x + 40, y + 20), (x - 8, y + 30)]], smooth=False)
        art = GP(art, cube_top, "#f5b2c2", "#e98ea6", seed=nx(), rough=0.6)
        yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
        stripes = (np.floor((yy - (y - 30)) / 7) % 2).astype(np.float32)
        for msk, k in ((front, 0.86), (side, 1.0)):
            art = GP(art, msk * stripes, "#e7698a", "#d8587a", seed=nx(), rough=0.4)
            art = GP(art, msk * (1 - stripes), "#fbeef0", "#f4dfe4", seed=nx(), rough=0.4)
            art = shade(art, msk, k)
        clear()
    # risoles: golden breaded rolls
    for x, y, a in ((486, 214, -0.18), (500, 252, 0.06)):
        L, r = 116, 19
        ca, sa = math.cos(a), math.sin(a)
        pts = [(x + math.cos(t) * L / 2 * ca - math.sin(t) * r * sa, y + math.cos(t) * L / 2 * sa + math.sin(t) * r * ca) for t in np.linspace(0, math.tau, 40)]
        m = shape_mask(W, H, pts)
        art = GP(art, m, "#d9953e", "#b8742a", seed=nx(), rough=1.4, streak=0.5)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        v = ((xx - x) * -sa + (yy - y) * ca) / r
        art = shade(art, m, 1.1 - 0.3 * np.clip(v, 0, 1))
        cr = (np.random.default_rng(1041 + int(x)).random((H, W)) > 0.9).astype(np.float32)
        art = OV(art, gaussian_filter(cr, 0.7) * 2 * m, lambda mm: col_arr(mm, "#8a4e1a", np.clip(mm, 0, 1) * 0.6))
        art = OV(art, (np.random.default_rng(1042 + int(x)).random((H, W)) > 0.95).astype(np.float32) * m, lambda mm: col_arr(mm, "#f3c77a", mm * 0.8))
        clear()
    # a few chili rawit for the risoles
    ch = strokes(W, H, [(curve([(560, 210), (580, 200), (594, 206)], 12), 7, (0.1, 0.6)), (curve([(548, 222), (570, 218), (586, 226)], 12), 7, (0.1, 0.6))])
    art = GP(art, ch, "#3a8a3e", "#2a6a2e", seed=nx(), rough=0.8)
    art = add_grain(art, 1043, 0.025)
    preview(art, "ak-kue", bg=CREAM)
    save(art, f"{OUT}/kue.webp", max_w=300, quality=86)
    clear()

if "teras" in PARTS:
    W, H = 780, 640
    nx = Seq(105000); rng = random.Random(1050)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = solid(W, H, CREAM)
    art = GP(art, np.ones((H, W), np.float32), "#fbefd6", "#f6e6c6", seed=nx(), rough=0, streak=1.0)
    # mint wainscot with a tile border
    wain = ((yy > 380) & (yy < 520)).astype(np.float32)
    art = GP(art, wain, MINT, "#8cc7ae", seed=nx(), rough=0, streak=0.9, pad=0)
    border = ((yy > 372) & (yy < 386)).astype(np.float32)
    art = GP(art, border, TEAL, "#23706b", seed=nx(), rough=0, pad=0)
    # tegel kunci floor
    floor = (yy >= 520).astype(np.float32)
    art = GP(art, floor, "#e7d2b0", "#dcc29a", seed=nx(), rough=0, pad=0)
    cell = 40
    u = ((xx + (yy - 520) * 0.2) % cell) / cell; v = ((yy - 520) % cell) / cell
    key = ((np.abs(u - 0.5) + np.abs(v - 0.5)) < 0.34).astype(np.float32) * floor
    art = GP(art, key, TERRA, "#b8522e", seed=nx(), rough=0.4, pad=0)
    dot = (((u - 0.5) ** 2 + (v - 0.5) ** 2) < 0.012).astype(np.float32) * floor
    art = GP(art, dot, "#f6ead2", seed=nx(), rough=0.3, pad=0)
    art = shade(art, floor, 1 - 0.18 * np.clip((yy - 520) / 120, 0, 1) * 0 - 0.08)
    lines = np.zeros((H, W), np.float32)
    for y0 in range(520, H, cell):
        lines[y0:y0 + 1] = 1
    art = shade(art, lines * floor, 0.85)
    clear()
    # window with teal frame, lace curtain and a garden outside
    wx0, wx1, wy0, wy1 = 250, 530, 70, 330
    win = ((xx > wx0) & (xx < wx1) & (yy > wy0) & (yy < wy1)).astype(np.float32)
    sky = painted_sky(W, H, [(0, "#cfeaf4"), (0.4, "#e8f4ee"), (1, "#e8f4ee")], seed=1051)
    art[..., :3] = np.where(win[..., None] > 0, sky[..., :3], art[..., :3])
    bush = win * (yy > 250 - 30 * np.sin(xx / 40)).astype(np.float32)
    art = GP(art, bush, "#6aa85a", "#4f8a4a", seed=nx(), rough=3)
    fr = np.zeros((H, W), np.float32)
    for x in (wx0, (wx0 + wx1) // 2, wx1):
        fr[wy0 - 8:wy1 + 8, x - 7:x + 7] = 1
    for y in (wy0, (wy0 + wy1) // 2, wy1):
        fr[y - 7:y + 7, wx0 - 7:wx1 + 7] = 1
    art = GP(art, fr, TEAL, "#23706b", seed=nx(), rough=0.8, streak=0.6)
    sill = ((xx > wx0 - 24) & (xx < wx1 + 24) & (yy > wy1 + 6) & (yy < wy1 + 20)).astype(np.float32)
    art = GP(art, sill, "#f7f1e2", "#e6dcc4", seed=nx(), rough=0.8)
    # lace curtains gathered at the sides
    for side in (-1, 1):
        x0 = wx0 - 30 if side < 0 else wx1 + 30
        xin = wx0 + 60 if side < 0 else wx1 - 60
        pts = [(x0, wy0 - 30), (xin, wy0 - 30), (xin - side * 10, wy0 + 80), (x0 + side * 20, wy0 + 170), (x0 + side * 4, wy1 + 10), (x0 - side * 6, wy1 + 10)]
        cm = shape_mask(W, H, pts)
        art = GP(art, cm, "#fffdf8", "#f1ebde", seed=nx(), rough=1.5, streak=0.8)
        folds = [([(x0 + side * k * 10, wy0 - 28), (x0 + side * (k * 6 + 8), wy1)], 2, (0.2, 0.3)) for k in range(1, 6)]
        art = G(art, strokes(W, H, folds) * cm, "#d8cfbc", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=0.5, feather=0.8)
        holes = (np.sin(xx / 5) * np.sin(yy / 5) > 0.75).astype(np.float32) * cm * (yy > wy1 - 50)
        art = shade(art, holes, 0.9)
    valance = shapes(W, H, [[(wx0 - 40, wy0 - 40), (wx1 + 40, wy0 - 40), (wx1 + 40, wy0 - 14)] + [(wx1 + 40 - k * 20, wy0 - 14 + (8 if k % 2 else 0)) for k in range(1, int((wx1 - wx0 + 80) / 20))] + [(wx0 - 40, wy0 - 14)]], smooth=True)
    art = GP(art, valance, "#fffdf8", "#efe7d6", seed=nx(), rough=1)
    clear()
    # framed family picture (abstract landscape, no faces) and a wall clock
    pf = ((xx > 92) & (xx < 190) & (yy > 120) & (yy < 210)).astype(np.float32)
    art = GP(art, pf, "#8a5a2a", "#6a4220", seed=nx(), rough=0.6)
    pin = ((xx > 102) & (xx < 180) & (yy > 130) & (yy < 200)).astype(np.float32)
    art = GP(art, pin, "#f3d9a4", "#e8c486", seed=nx(), rough=0.4)
    art = GP(art, pin * (yy > 168 - 14 * np.sin((xx - 100) / 16)).astype(np.float32), "#7aa860", seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, [(160, 148, 9)]) * pin, "#f0a13a", seed=nx(), rough=0.4)
    clk = circles(W, H, [(640, 150, 36)])
    art = GP(art, clk, "#8a5a2a", seed=nx(), rough=0.6)
    art = GP(art, circles(W, H, [(640, 150, 28)]), "#fffaf0", seed=nx(), rough=0.4)
    art = G(art, strokes(W, H, [([(640, 150), (640, 130)], 3, None), ([(640, 150), (654, 158)], 3, None)]), INK, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.3, feather=0.4)
    # rattan chairs, left and right
    for side in (-1, 1):
        cx = 390 + side * 285
        back = shapes(W, H, [[(cx - 70, 470), (cx - 78, 330), (cx - 40, 300), (cx + 40, 300), (cx + 78, 330), (cx + 70, 470)]])
        seat = ellipses(W, H, [(cx, 470, 92, 26, 0)])
        legs = strokes(W, H, [([(cx - 70, 476), (cx - 76, 560)], 8, None), ([(cx + 70, 476), (cx + 76, 560)], 8, None), ([(cx - 30, 490), (cx - 32, 572)], 7, None), ([(cx + 30, 490), (cx + 32, 572)], 7, None)])
        arms = strokes(W, H, [(curve([(cx - 80, 400), (cx - 96, 420), (cx - 92, 470)], 16), 12, None), (curve([(cx + 80, 400), (cx + 96, 420), (cx + 92, 470)], 16), 12, None)])
        art = GP(art, legs, "#8a5a2a", "#6a4220", seed=nx(), rough=0.8)
        art = GP(art, np.clip(back + arms, 0, 1), RATTAN, "#a06c38", seed=nx(), rough=1.4, streak=0.8)
        wv = (np.abs(np.sin((xx - cx) / 6) * np.sin((yy - 300) / 6)) > 0.6).astype(np.float32) * back
        art = shade(art, wv, 0.84)
        art = shade(art, back, 1 - 0.18 * np.clip(side * (xx - cx) / 80, 0, 1))
        cush = ellipses(W, H, [(cx, 462, 84, 24, 0)])
        art = GP(art, cush, PINK, "#e07e98", seed=nx(), rough=1)
        flw = circles(W, H, [(cx + dx, 458 + dy, 5) for dx, dy in ((-50, 0), (-20, 6), (10, -4), (40, 4), (64, -2), (-66, 6))])
        art = GP(art, flw * cush, "#fff2f4", seed=nx(), rough=0.4)
        clear()
    # snake plant in a terracotta pot (left corner) and a monstera (right)
    pot = shapes(W, H, [[(20, 520), (100, 520), (90, 600), (30, 600)]], smooth=False)
    art = GP(art, pot, TERRA, "#b8522e", seed=nx(), rough=1)
    lv = []
    for k in range(7):
        bx = 34 + k * 8; h = rng.uniform(150, 230); lean = rng.uniform(-24, 24)
        lv.append([(bx - 8, 522), (bx + lean * 0.5 - 7, 522 - h * 0.6), (bx + lean, 522 - h), (bx + lean * 0.5 + 7, 522 - h * 0.6), (bx + 8, 522)])
    lm = shapes(W, H, lv)
    art = GP(art, lm, "#3f7a4a", "#2e6a3e", seed=nx(), rough=1)
    art = OV(art, lm * (np.sin(yy / 9 + xx / 14) > 0.6).astype(np.float32), lambda m: col_arr(m, "#8cc07a", m * 0.6))
    art = GP(art, lm * np.clip(1 - gaussian_filter(1 - lm, 1.5) * 6, 0, 1) * 0 + np.clip(lm - np.roll(lm, 3, 1), 0, 1), "#d9d27a", seed=nx(), rough=0.4)
    clear()
    pot2 = shapes(W, H, [[(690, 530), (770, 530), (760, 600), (700, 600)]], smooth=False)
    art = GP(art, pot2, "#f3c74e", "#e2b03a", seed=nx(), rough=1)
    mon = []
    for a, L in ((-2.2, 110), (-1.7, 130), (-1.25, 120), (-0.8, 100), (-2.6, 90)):
        tx, ty = 730 + math.cos(a) * L, 530 + math.sin(a) * L
        mon.append(ellipse_pts(tx, ty, 34, 24, 12, a))
    mm_ = shapes(W, H, mon)
    stems = strokes(W, H, [([(730, 532), (730 + math.cos(a) * L * 0.8, 530 + math.sin(a) * L * 0.8)], 4, None) for a, L in ((-2.2, 110), (-1.7, 130), (-1.25, 120), (-0.8, 100), (-2.6, 90))])
    art = GP(art, stems, "#3f7a4a", seed=nx(), rough=0.6)
    art = GP(art, mm_, "#3f8a50", "#2e6a3e", seed=nx(), rough=1.4)
    slits = strokes(W, H, [([(730 + math.cos(a) * L, 530 + math.sin(a) * L), (730 + math.cos(a) * L + math.cos(a + 1.4) * 20, 530 + math.sin(a) * L + math.sin(a + 1.4) * 20)], 2.4, None) for a, L in ((-2.2, 110), (-1.7, 130), (-1.25, 120), (-0.8, 100), (-2.6, 90))])
    art = OV(art, slits * mm_, lambda m: col_arr(m, "#fbefd6", m))
    # the low table with a crochet cloth (items are placed on it in CSS)
    tb = ((xx > 230) & (xx < 550) & (yy > 488) & (yy < 504)).astype(np.float32)
    art = GP(art, tb, "#8a5a2a", "#6a4220", seed=nx(), rough=0.6)
    tlegs = strokes(W, H, [([(250, 500), (246, 600)], 9, None), ([(530, 500), (534, 600)], 9, None)])
    art = GP(art, tlegs, "#7a4e24", seed=nx(), rough=0.6)
    cloth = shapes(W, H, [[(220, 482), (560, 482), (560, 520)] + [(560 - k * 17, 520 + (10 if k % 2 else 0)) for k in range(1, 20)] + [(220, 520)]])
    art = GP(art, cloth, "#fffdf6", "#f0e8d8", seed=nx(), rough=1.0)
    holes = (np.sin(xx / 4) * np.sin(yy / 4) > 0.7).astype(np.float32) * cloth * (yy > 496)
    art = shade(art, holes, 0.86)
    # soft floor shadow under chairs and table
    sh = ellipses(W, H, [(390, 604, 190, 14, 0), (105, 576, 90, 10, 0), (675, 576, 90, 10, 0)])
    art = OV(art, sh, lambda m: col_arr(m, "#5a3a22", gaussian_filter(m, 8) * 0.25), pad=20)
    art = add_grain(art, 1052, 0.03)
    preview(art, "ak-teras")
    save_rgb(art, f"{OUT}/teras.webp", size=(780, 640), quality=80)
    clear()

if "divider" in PARTS:
    W, H = 360, 70
    nx = Seq(106000); rng = random.Random(1060)
    art = blank(W, H)
    for i, (x, a) in enumerate(((92, -0.25), (180, 0.15), (268, -0.1))):
        art = rolled_slip(art, W, H, x, 35, 62, 13, a, nx, SLIP_COLS[[1, 2, 3][i]])
    preview(art, "ak-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=180, quality=86)
    clear()
