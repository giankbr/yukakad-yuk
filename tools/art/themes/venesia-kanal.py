"""Venesia Kanal — a Venetian side canal in loose watercolour on paper: pastel facades (rose, ochre, peach, terracotta)
receding to a little stone bridge and a campanile, arched windows with green shutters, striped mooring poles,
broken reflections; an empty moored gondola as a separate piece (it bobs). The painting dissolves into bare paper at
the top and bottom (vignette). Run: python3 -I venesia-kanal.py [part ...]
parts: scene gondola poles houses. Assets -> public/themes/art/venesia-kanal/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m2_lib import *

OUT = outdir("venesia-kanal")
PARTS = sys.argv[1:] or ["scene", "gondola", "poles", "houses"]
PAPER = "#fbf6ee"
WALLS = [("#e7a99a", "#d98d7e"), ("#efc57e", "#e2ad62"), ("#f2c6a8", "#e8ad8a"), ("#cf7a58", "#bb6446"), ("#efd9b4", "#e0c08e"), ("#d9a0a8", "#c98690"), ("#e8b98c", "#d99a68")]
SHUT, SHUT_D = "#5f8a6a", "#3f6a50"
WIN = "#4b3a3a"
WATER, WATER_D, WATER_L = "#5f9a94", "#3f7470", "#9cc6bd"
STONE, STONE_D = "#e6dccb", "#b6a68e"
NAVY = "#22344d"
VX, VY = 390, 520


def proj(xn, yn, u, k=4.0):
    z = 1 + k * u
    return VX + (xn - VX) / z, VY + (yn - VY) / z


def facade_quad(xn, ytop, ybot, u0, u1):
    a = proj(xn, ytop, u0); b = proj(xn, ytop, u1); c = proj(xn, ybot, u1); d = proj(xn, ybot, u0)
    return [a, b, c, d]


def local(xn, ytop, ybot, u, v):
    """point on a facade plane: u depth (0 near), v 0 top .. 1 waterline."""
    return proj(xn, ytop + (ybot - ytop) * v, u)


def arch_window(xn, ytop, ybot, u0, u1, v0, v1, n=10):
    """arched window in facade-local coords (u0..u1 width along depth, v0 top .. v1 bottom)."""
    pts = []
    um = (u0 + u1) / 2; ru = (u1 - u0) / 2
    va = v0 + (v1 - v0) * 0.28
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        uu = um + math.cos(a) * ru
        vv = va + math.sin(a) * (va - v0)
        pts.append(local(xn, ytop, ybot, uu, vv))
    pts.append(local(xn, ytop, ybot, u1, v1)); pts.append(local(xn, ytop, ybot, u0, v1))
    return pts


def lancet_window(xn, ytop, ybot, u0, u1, v0, v1):
    """Venetian gothic ogee-ish window: pointed top."""
    um = (u0 + u1) / 2
    vs = v0 + (v1 - v0) * 0.32
    pts = [local(xn, ytop, ybot, u0, v1), local(xn, ytop, ybot, u0, vs)]
    for t in np.linspace(0, 1, 6)[1:]:
        pts.append(local(xn, ytop, ybot, u0 + (um - u0) * t, vs - (vs - v0) * math.sin(t * math.pi / 2)))
    for t in np.linspace(0, 1, 6)[1:]:
        pts.append(local(xn, ytop, ybot, um + (u1 - um) * t, v0 + (vs - v0) * (1 - math.cos(t * math.pi / 2))))
    pts.append(local(xn, ytop, ybot, u1, v1))
    return pts


def paint_side(art, W, H, xn, buildings, nx, rng, refl_list, lake_y):
    """buildings: list of (u0, u1, ytop_near, wall_idx, style). Painted far to near so near ones overlap."""
    for (u0, u1, yt, wi, style) in sorted(buildings, key=lambda b: -b[0]):
        yb = 900
        q = facade_quad(xn, yt, yb, u0, u1)
        m = shapes(W, H, [q], smooth=False)
        c1, c2 = WALLS[wi % len(WALLS)]
        art = G(art, m, c1, c2, seed=nx(), density=0.85, edge=0.6, bloom=0.45, rough=2.5, feather=1.0)
        # weathering at the waterline (dark damp band) and top shadow under the eaves
        damp = shapes(W, H, [[local(xn, yt, yb, u0, 0.9), local(xn, yt, yb, u1, 0.9), local(xn, yt, yb, u1, 1.0), local(xn, yt, yb, u0, 1.0)]], smooth=False)
        art = G(art, damp, "#6e6a58", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=2)
        eave = shapes(W, H, [[local(xn, yt, yb, u0, -0.02), local(xn, yt, yb, u1, -0.02), local(xn, yt, yb, u1, 0.03), local(xn, yt, yb, u0, 0.03)]], smooth=False)
        art = G(art, eave, "#8a5a44", seed=nx(), density=0.7, edge=0.3, rough=1.5)
        if rng.random() < 0.6:
            cu = u0 + (u1 - u0) * rng.uniform(0.3, 0.7)
            bx, by_ = local(xn, yt, yb, cu, 0.0)
            sc = 1 / (1 + 4 * cu)
            cw, ch = 14 * sc, 46 * sc
            chim = shapes(W, H, [[(bx - cw / 2, by_), (bx - cw / 2, by_ - ch), (bx - cw * 1.2, by_ - ch - 14 * sc), (bx + cw * 1.2, by_ - ch - 14 * sc), (bx + cw / 2, by_ - ch), (bx + cw / 2, by_)]], smooth=False)
            art = G(art, chim, "#b86a4e", "#9a5440", seed=nx(), density=0.85, edge=0.5, rough=1)
        # windows: rows x cols, with shutters
        rows = 3 if yt < 300 else 2
        cols = max(1, int((u1 - u0) / 0.06))
        wins, shut = [], []
        for r in range(rows):
            v0 = 0.12 + r * (0.68 / rows); v1 = v0 + 0.68 / rows * 0.6
            for c in range(cols):
                cu0 = u0 + (u1 - u0) * (c + 0.28) / cols; cu1 = u0 + (u1 - u0) * (c + 0.72) / cols
                if style == "gothic" and r == 1:
                    wins.append(lancet_window(xn, yt, yb, cu0, cu1, v0, v1))
                else:
                    wins.append(arch_window(xn, yt, yb, cu0, cu1, v0, v1))
                if style != "gothic":
                    sw = (cu1 - cu0) * 0.42
                    for (a0, a1) in ((cu0 - sw, cu0), (cu1, cu1 + sw)):
                        shut.append([local(xn, yt, yb, a0, v0 + 0.02), local(xn, yt, yb, a1, v0 + 0.02), local(xn, yt, yb, a1, v1), local(xn, yt, yb, a0, v1)])
        wm = shapes(W, H, wins, smooth=False)
        art = G(art, wm, WIN, "#5a4440", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.0, feather=0.6)
        if shut:
            art = G(art, shapes(W, H, shut, smooth=False), SHUT, SHUT_D, seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1.0, feather=0.6)
        # door / water gate at the base
        du = (u0 + u1) / 2
        door = arch_window(xn, yt, yb, du - 0.02, du + 0.02, 0.8, 0.99)
        art = G(art, shapes(W, H, [door], smooth=False), "#3b3a3a", seed=nx(), density=0.8, edge=0.4, rough=1)
        # reflection quad mirrored about the waterline
        qr = [(x, 2 * proj(xn, yb, (u0 if i in (0, 3) else u1))[1] - y) for i, (x, y) in enumerate(q)]
        refl_list.append((qr, c1))
        clear()
    return art


if "scene" in PARTS:
    W, H = 780, 1080
    nx = Seq(61000)
    rng = random.Random(5)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    # sky
    art = G(art, (yy < 640).astype(np.float32), "#cfe0e6", "#f2dcc6", seed=nx(), density=0.45, edge=0.05, bloom=0.5, rough=8, feather=10, mottle=0.8)
    art = G(art, np.clip((yy - 300) / 260, 0, 1) * (yy < 640), "#f6d2b4", seed=nx(), density=0.35, edge=0.05, bloom=0.4, rough=6, feather=10)
    # distant campanile + domes at the vanishing point
    tower = rects(W, H, [(402, 250, 34, 300)])
    art = G(art, tower, "#c98a6c", "#b5735a", seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=1.5)
    art = G(art, rects(W, H, [(408, 290, 8, 26), (422, 290, 8, 26)]), "#6e4a40", seed=nx(), density=0.8, edge=0.3, rough=0.8)
    art = G(art, shapes(W, H, [[(398, 252), (419, 196), (440, 252)]], smooth=False), "#7f8f7a", seed=nx(), density=0.8, edge=0.5, rough=1)
    far = []
    fx = 290
    for k, (w, t) in enumerate(((44, 470), (52, 486), (40, 462), (60, 480))):
        far.append((fx, t, w, k))
        fx += w
    for (fx0, t, w, k) in far:
        m = rects(W, H, [(fx0, t, w + 1, 600 - t)])
        c1, c2 = WALLS[(k + 3) % len(WALLS)]
        art = G(art, m, c1, c2, seed=nx(), density=0.8, edge=0.5, bloom=0.3, rough=1.5)
        art = G(art, rects(W, H, [(fx0 + w * 0.25 + j * w * 0.3, t + 14 + r * 30, 5, 12) for j in range(2) for r in range(3) if t + 26 + r * 30 < 590]), WIN, seed=nx(), density=0.75, edge=0.3, rough=0.6)
    clear()
    refl = []
    left = [(0.0, 0.16, 140, 0, "arch"), (0.16, 0.3, 210, 1, "gothic"), (0.3, 0.46, 120, 3, "arch"), (0.46, 0.62, 190, 4, "arch"), (0.62, 0.8, 150, 2, "arch"), (0.8, 1.0, 230, 5, "arch")]
    right = [(0.0, 0.14, 180, 2, "arch"), (0.14, 0.32, 100, 5, "gothic"), (0.32, 0.5, 200, 6, "arch"), (0.5, 0.66, 140, 0, "arch"), (0.66, 0.84, 210, 1, "arch"), (0.84, 1.0, 160, 3, "arch")]
    art = paint_side(art, W, H, -90, left, nx, rng, refl, 900)
    art = paint_side(art, W, H, 870, right, nx, rng, refl, 900)
    # flower boxes / balcony on the near left building, laundry line between the sides
    bal = shapes(W, H, [[local(-90, 140, 900, 0.03, 0.42), local(-90, 140, 900, 0.13, 0.42), local(-90, 140, 900, 0.13, 0.46), local(-90, 140, 900, 0.03, 0.46)]], smooth=False)
    art = G(art, bal, "#2f3a3a", seed=nx(), density=0.9, edge=0.3, rough=1)
    fl = circles(W, H, [(x, y, rng.uniform(3, 6)) for _ in range(40) for x, y in [local(-90, 140, 900, rng.uniform(0.03, 0.13), rng.uniform(0.38, 0.42))]])
    art = G(art, fl, "#d0504a", "#e07a70", seed=nx(), density=0.85, edge=0.5, bloom=0.2, rough=1)
    art = G(art, circles(W, H, [(x, y, rng.uniform(3, 5)) for _ in range(20) for x, y in [local(-90, 140, 900, rng.uniform(0.03, 0.13), rng.uniform(0.4, 0.43))]]), "#5f8a4a", seed=nx(), density=0.8, edge=0.4, rough=1)
    clear()
    # water between the two waterlines
    wl = [proj(-90, 900, u) for u in (0, 1)]; wr = [proj(870, 900, u) for u in (1, 0)]
    water = shapes(W, H, [[(-20, 900 + 40), wl[0], wl[1], wr[0], wr[1], (W + 20, 900 + 40), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    water = np.maximum(water, (yy > 900).astype(np.float32))
    art = G(art, water, WATER, "#6fa39b", seed=nx(), density=0.85, edge=0.3, bloom=0.5, rough=3, feather=1.5)
    art = G(art, water * np.clip((yy - 640) / 400, 0, 1), WATER_D, seed=nx(), density=0.4, edge=0.1, bloom=0.4, rough=3)
    # broken reflections: each facade colour mirrored, cut into horizontal ripple strips
    ripple = np.clip(np.sin(yy / 4.0 + fbm(W, H, nx(), 24, 2) * 9) * 1.4 + 0.2, 0, 1)
    for (qr, col) in refl:
        rm = shapes(W, H, [qr], smooth=False) * water
        rm = gaussian_filter(displace(rm, nx(), 3, 14), (5, 0.8))
        art = G(art, rm * (0.35 + 0.65 * ripple), col, seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=1.5, feather=1.2)
        clear()
    glint = strokes(W, H, [([(x0, y), (x0 + rng.uniform(12, 50), y)], rng.uniform(1.4, 2.6), (0.4, 0.4)) for _ in range(90)
                           for x0, y in [(rng.uniform(0, W), rng.uniform(620, 1060))]])
    art = soft(art, glint * water, "#f3f7f0", alpha=0.6, pad=4)
    clear()
    # the little stone bridge (humped, Istrian-stone parapet) across the canal
    ub = 0.2
    lx, wy = proj(-90, 900, ub); rx, _ = proj(870, 900, ub)
    cxb = (lx + rx) / 2
    hump = curve([(lx - 14, wy - 22), (cxb, wy - 96), (rx + 14, wy - 22)], 40)
    under = curve([(rx - 80, wy), (cxb, wy - 50), (lx + 80, wy)], 40)
    body = shapes(W, H, [hump + [(rx + 14, wy + 2), (rx - 80, wy + 2)] + under + [(lx + 80, wy + 2), (lx - 14, wy + 2)]], smooth=False)
    art = knockout(art, body, amount=1.0, grow=1.0)
    art = GP(art, body, "#e9d9c2", "#dcc6a8", seed=nx(), rough=1.5, streak=0.6)
    art = G(art, body, "#e3cdb0", "#d2b896", seed=nx(), density=0.6, edge=0.6, bloom=0.5, rough=1.5)
    art = G(art, body * np.clip((yy - (wy - 40)) / 40, 0, 1), "#9b8a74", seed=nx(), density=0.4, edge=0.1, bloom=0.3, rough=1.5)
    bricks = body * (np.abs(np.sin(xx / 9) * np.sin(yy / 7)) > 0.92)
    art = G(art, bricks, "#c39a7a", seed=nx(), density=0.35, edge=0.1, rough=0.8)
    para = strokes(W, H, [([(x, y - 34) for x, y in hump], 6, None), ([(x, y - 2) for x, y in hump], 7, None)] +
                   [([(x, y - 34), (x, y - 2)], 4, None) for x, y in hump[2:-2:3]])
    art = GP(art, para, "#f4efe6", "#e3dccd", seed=nx(), rough=0.8, streak=0.4)
    art = G(art, para, "#d8cfbf", seed=nx(), density=0.35, edge=0.6, rough=0.8)
    art = G(art, strokes(W, H, [([(x, y + 3) for x, y in hump], 3, None)]), "#9a8670", seed=nx(), density=0.7, edge=0.2, rough=0.6)
    art = G(art, strokes(W, H, [(under, 7, None)]), "#7a6654", seed=nx(), density=0.6, edge=0.2, rough=0.8)
    art = G(art, np.clip(shapes(W, H, [under + [(rx - 80, wy + 2), (lx + 80, wy + 2)]], smooth=False), 0, 1), "#3f5f60", seed=nx(), density=0.35, edge=0.3, rough=1)
    brm = shapes(W, H, [[(lx - 14, wy), (rx + 14, wy), (rx + 14, wy + 70), (lx - 14, wy + 70)]], smooth=False)
    art = G(art, displace(brm * np.clip(np.sin(yy / 4.5) * 1.6, 0, 1) * (1 - shapes(W, H, [[(x, 2 * wy - y) for x, y in under] + [(lx + 80, wy), (rx - 80, wy)]], smooth=False)), nx(), 3, 8), "#d9c2a4", seed=nx(), density=0.4, edge=0.1, rough=1.5)
    clear()
    # mooring poles (pali): blue-white and red-white stripes with reflections
    poles = []
    for (x, y0, y1, c, w) in ((70, 660, 1000, "#3c5f8c", 20), (124, 700, 990, "#3c5f8c", 16), (676, 700, 1000, "#b73a3a", 20)):
        pm = rects(W, H, [(x, y0, w, y1 - y0)])
        art = G(art, pm, "#f6f1e6", "#e8e0d0", seed=nx(), density=0.95, edge=0.4, rough=0.8)
        stripes = pm * (np.floor((yy - y0 - (xx - x) * 0.4) / 26) % 2 == 0)
        art = G(art, stripes, c, seed=nx(), density=0.9, edge=0.3, rough=0.8, feather=0.5)
        art = G(art, rects(W, H, [(x - 2, y0 - 10, w + 4, 12)]), "#2a2a2a", seed=nx(), density=0.85, edge=0.3, rough=0.6)
        art = G(art, pm * np.clip((xx - x - w * 0.55) / (w * 0.45), 0, 1), "#4a4a4a", seed=nx(), density=0.35, edge=0, rough=0.5)
        prf = rects(W, H, [(x, y1, w, 90)]) * ripple
        art = G(art, displace(prf, nx(), 3, 8), c, seed=nx(), density=0.5, edge=0.2, rough=1)
        clear()
    # dissolve into bare paper at the top and bottom with a wet, irregular edge
    edge_n = fbm(W, H, nx(), 60, 3)
    vig = np.clip((yy - 70 - edge_n * 110) / 110, 0, 1) * np.clip((1040 - yy - edge_n * 120) / 120, 0, 1)
    art[..., 3] *= vig
    prev(art, "vk-scene", bg=None)
    save_full(art, f"{OUT}/scene.webp", size=(580, 803), quality=72)

if "gondola" in PARTS:
    W, H = 820, 300
    nx = Seq(62000)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    # long asymmetric hull, curling up at the prow (right) and stern (left)
    top = curve([(40, 120), (120, 170), (300, 186), (520, 182), (690, 160), (760, 110), (786, 60)], 50)
    bot = curve([(786, 60), (770, 130), (700, 200), (520, 222), (300, 224), (140, 214), (60, 170), (40, 120)], 50)
    hull = shapes(W, H, [top + bot], smooth=False)
    art = G(art, hull, "#1d1f24", "#2a2c33", seed=nx(), density=1.0, edge=0.6, bloom=0.2, rough=1.2)
    art = G(art, hull * np.clip(1 - np.abs(yy - 190) / 10, 0, 1), "#5d6470", seed=nx(), density=0.6, edge=0.2, rough=1)
    # ferro (prow comb) in silver
    ferro = strokes(W, H, [([(778, 70), (800, 18)], 7, (0.1, 0.3))] + [([(780 - k * 6, 54 + k * 9), (806 - k * 4, 48 + k * 9)], 4, None) for k in range(5)])
    art = G(art, ferro, "#c8cdd2", "#9aa2aa", seed=nx(), density=0.95, edge=0.4, rough=0.6, feather=0.5)
    # red velvet seat with gold trim, a folded rug
    seat = shapes(W, H, [[(360, 150), (470, 148), (480, 184), (352, 186)]])
    art = G(art, seat, "#b2303a", "#932530", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=1)
    art = G(art, strokes(W, H, [([(356, 152), (476, 150)], 4, None)]), "#d9a940", seed=nx(), density=0.9, edge=0.3, rough=0.6)
    art = G(art, shapes(W, H, [[(230, 168), (330, 170), (332, 186), (226, 186)]]), "#2f4f7a", seed=nx(), density=0.9, edge=0.4, rough=1)
    # forcola (oar rest) with oar laid along
    art = G(art, strokes(W, H, [([(170, 160), (178, 110)], 8, (0.1, 0.2))]), "#7a4a2a", seed=nx(), density=0.95, edge=0.4, rough=0.8)
    art = G(art, strokes(W, H, [([(176, 112), (600, 150)], 5, (0.05, 0.1))]), "#9a6a3a", seed=nx(), density=0.9, edge=0.4, rough=0.8)
    # reflection
    rf = np.flipud(hull)
    rf = np.roll(rf, -(H - 2 * 222) - 4, 0) * (yy > 222)
    rip = np.clip(np.sin(yy / 4.2) * 1.8, 0, 1)
    art = G(art, rf * rip * np.clip(1 - (yy - 222) / 70, 0, 1), "#24363a", seed=nx(), density=0.55, edge=0.1, rough=2)
    prev(art, "vk-gondola", bg=PAPER)
    save(art, f"{OUT}/gondola.webp", max_w=420, quality=84)

if "poles" in PARTS:
    # divider: three striped mooring poles with a ripple, small
    W, H = 360, 200
    nx = Seq(63000)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    water = ellipses(W, H, [(180, 160, 170, 22, 0)])
    art = G(art, water, WATER_L, WATER, seed=nx(), density=0.7, edge=0.6, bloom=0.4, rough=3)
    for (x, y0, c, w) in ((140, 30, "#3c5f8c", 14), (172, 18, "#b73a3a", 16), (206, 40, "#3c5f8c", 12)):
        pm = rects(W, H, [(x, y0, w, 150 - y0)])
        art = G(art, pm, "#f6f1e6", seed=nx(), density=0.95, edge=0.4, rough=0.6)
        art = G(art, pm * (np.floor((yy - y0 - (xx - x) * 0.5) / 18) % 2 == 0), c, seed=nx(), density=0.9, edge=0.3, rough=0.6, feather=0.5)
        art = G(art, rects(W, H, [(x - 2, y0 - 8, w + 4, 10)]), "#2a2a2a", seed=nx(), density=0.85, edge=0.3, rough=0.5)
    prev(art, "vk-poles", bg=PAPER)
    save(art, f"{OUT}/poles.webp", max_w=180, quality=86)

if "houses" in PARTS:
    # frieze of canal-front houses seen straight on (for the countdown and closing): tops dissolve to paper
    W, H = 900, 300
    nx = Seq(64000)
    rng = random.Random(9)
    yy, xx = yy_xx(W, H)
    art = blank(W, H)
    x = -10
    k = 0
    while x < W:
        w = rng.choice([110, 130, 150, 96])
        top = rng.choice([40, 60, 30, 76])
        c1, c2 = WALLS[k % len(WALLS)]
        m = rects(W, H, [(x, top, w + 2, 250 - top)])
        art = G(art, m, c1, c2, seed=nx(), density=0.85, edge=0.6, bloom=0.4, rough=2.5)
        art = G(art, rects(W, H, [(x, top, w + 2, 8)]), "#8a5a44", seed=nx(), density=0.7, edge=0.3, rough=1)
        ws, ss = [], []
        nc = max(1, w // 40)
        for r in range(2):
            y0 = top + 26 + r * 70
            for c in range(nc):
                cx = x + (c + 0.5) * w / nc
                ws.append(arc_pts(cx, y0 + 10, 9, math.pi, 2 * math.pi, 8) + [(cx + 9, y0 + 40), (cx - 9, y0 + 40)])
                ss += [[(cx - 20, y0 + 2), (cx - 10, y0 + 2), (cx - 10, y0 + 40), (cx - 20, y0 + 40)], [(cx + 10, y0 + 2), (cx + 20, y0 + 2), (cx + 20, y0 + 40), (cx + 10, y0 + 40)]]
        art = G(art, shapes(W, H, ws, smooth=False), WIN, seed=nx(), density=0.85, edge=0.5, rough=0.8)
        art = G(art, shapes(W, H, ss, smooth=False), SHUT, SHUT_D, seed=nx(), density=0.85, edge=0.5, rough=0.8)
        art = G(art, rects(W, H, [(x, 230, w + 2, 20)]), "#6e6a58", seed=nx(), density=0.45, edge=0.3, rough=2)
        clear()
        x += w; k += 1
    water = rects(W, H, [(0, 250, W, 50)])
    art = G(art, water, WATER, WATER_L, seed=nx(), density=0.85, edge=0.4, bloom=0.4, rough=3)
    edge_n = fbm(W, H, nx(), 50, 3)
    art[..., 3] *= np.clip((yy - 10 - edge_n * 40) / 40, 0, 1)
    prev(art, "vk-houses", bg=PAPER)
    save_full(art, f"{OUT}/houses.webp", size=(720, 240), quality=80)
