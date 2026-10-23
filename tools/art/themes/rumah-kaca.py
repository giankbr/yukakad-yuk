"""Rumah Kaca — Victorian glass conservatory at morning light: watercolour palms & ferns behind hazy glass, verdigris
iron glazing bars in gouache, hanging fern basket, potted kentia palm, ironwork divider, fern sprig.
Run: python3 -I rumah-kaca.py [part ...]   parts: house fern palm divider sprig"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n6_lib import *

OUT = outdir("rumah-kaca")
PARTS = sys.argv[1:] or ["house", "fern", "palm", "divider", "sprig"]
IRON, IRON_D, IRON_L = "#2f4a42", "#1a2a25", "#8fb0a2"
GLASS_A, GLASS_B = "#dbe8e1", "#bcd3cc"
LEAF = ["#83b063", "#4f8a50", "#2f6a48", "#1d4734"]
TERRA, TERRA_D = "#b9764f", "#7f4a31"
STONE, STONE_D = "#d9cdb8", "#a99a80"
LIGHT = "#fff3d2"


def iron(art, mask, nx, pad=10):
    art = GP(art, mask, IRON, IRON_D, seed=nx(), rough=1.4, streak=0.8, pad=pad)
    art = lay(art, edge_hi(mask, -1, -1) * mask, IRON_L, 0.55)
    return art


def palm_cluster(W, H, bx, by, n, reach, rng, lean=0.0, leaf=(46, 6.5), up=1.0):
    """Kentia-like palm: long arching rachises with narrow drooping leaflets (tapered strokes)."""
    items = []
    for k in range(n):
        a = -math.pi / 2 + lean + (k - (n - 1) / 2) * (2.3 / max(1, n - 1)) * rng.uniform(0.85, 1.15)
        L = reach * rng.uniform(0.72, 1.05)
        side = math.cos(a)
        tip = (bx + side * L * 1.05, by + math.sin(a) * L * 0.55 * up + L * 0.25)
        mid = (bx + side * L * 0.5, by + math.sin(a) * L * 0.85 * up)
        pts = curve([(bx, by), mid, tip], 40)
        items.append((pts, leaf[1] * 0.55, (0.02, 0.7)))
        for i in range(4, len(pts) - 1, 2):
            t = i / (len(pts) - 1)
            p, q = pts[i - 1], pts[i + 1]
            ang = math.atan2(q[1] - p[1], q[0] - p[0])
            ll = leaf[0] * (0.35 + 0.65 * math.sin(math.pi * min(1, 0.2 + t)) ** 0.7) * rng.uniform(0.85, 1.1)
            for sd in (-1, 1):
                la = ang + sd * 0.75
                la = math.atan2(math.sin(la) + 1.1, math.cos(la))   # gravity
                ex, ey = pts[i][0] + math.cos(la) * ll, pts[i][1] + math.sin(la) * ll
                mx_, my_ = pts[i][0] + math.cos(la) * ll * 0.5 + math.cos(ang) * ll * 0.12, pts[i][1] + math.sin(la) * ll * 0.5
                items.append((curve([pts[i], (mx_, my_), (ex, ey)], 8), leaf[1] * rng.uniform(0.75, 1.0), (0.12, 0.7)))
    return strokes(W, H, items)


def fern_burst(W, H, cx, cy, n, reach, rng, a0=-math.pi, a1=0.0, leaf=(14, 5.0), sag=0.35):
    ms = []
    for k in range(n):
        a = a0 + (a1 - a0) * (k + 0.5) / n + rng.uniform(-0.12, 0.12)
        L = reach * rng.uniform(0.7, 1.0)
        tip = (cx + math.cos(a) * L, cy + math.sin(a) * L + L * sag)
        mid = (cx + math.cos(a) * L * 0.55, cy + math.sin(a) * L * 0.55)
        pts = curve([(cx, cy), mid, tip], 30)
        ms.append(frond(W, H, pts, leaf[0], leaf[1], step=1, spread=1.15, droop=0.35, profile=0.9, n=8))
    return np.maximum.reduce(ms)


def paint_greens(art, mask, nx, shade=0, density=0.66):
    c = LEAF[shade:shade + 2] if shade < 3 else LEAF[2:]
    art = G(art, mask, c[0], c[1], seed=nx(), density=density, edge=0.5, bloom=0.35, rough=3, holes=0.04, feather=1.0)
    dark = mask * np.clip(gaussian_filter(mask, 6) * 1.4 - 0.4, 0, 1)
    return G(art, dark, LEAF[min(3, shade + 2)], seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2, feather=1.2)


def urn(W, H, cx, by, w, h):
    """Classical terracotta urn: rolled lip, swelling bowl, narrow stem, round foot."""
    half = [(w * 0.56, -h), (w * 0.56, -h * 0.9), (w * 0.5, -h * 0.86), (w * 0.5, -h * 0.7), (w * 0.44, -h * 0.42), (w * 0.3, -h * 0.24),
            (w * 0.15, -h * 0.17), (w * 0.14, -h * 0.08), (w * 0.3, -h * 0.03), (w * 0.3, 0)]
    pts = [(cx + x, by + y) for x, y in half] + [(cx - x, by + y) for x, y in half[::-1]]
    rim = rect(cx - w * 0.56, by - h, cx + w * 0.56, by - h * 0.88)
    return shapes(W, H, [pts], smooth=False), shapes(W, H, [rim], smooth=False)


def paint_urn(art, W, H, cx, by, w, h, nx):
    body, rim = urn(W, H, cx, by, w, h)
    m = np.maximum(body, rim)
    art = GP(art, m, TERRA, TERRA_D, seed=nx(), rough=1.0, streak=0.8, pad=10)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = np.clip((xx - cx) / (w * 0.5), 0, 1) * m
    art = G(art, shade, TERRA_D, seed=nx(), density=0.55, edge=0.1, bloom=0.2, rough=1.5)
    art = lay(art, np.clip((cx - xx) / (w * 0.5) - 0.4, 0, 1) * body * 0.5, "#f1c49d", 0.5)
    art = G(art, edge_lo(rim, 0, 3) * 1.0, TERRA_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.5)
    return art


if "house" in PARTS:
    W, H = 780, 1000
    rng = random.Random(41)
    nx = Seq(4100)
    art = blank(W, H)
    CX, AY, R = 390, 430, 146          # central bay arch centre / radius
    BX0, BX1 = CX - R, CX + R
    BASE = 900
    # ---------- geometry
    arch = [(BX0, BASE), (BX0, AY)] + arc_pts(CX, AY, R, math.pi, math.tau, 40) + [(BX1, AY), (BX1, BASE)]
    roofL = curve([(48, 640), (110, 560), (190, 505), (BX0, 486)], 40)
    roofR = [(W - x, y) for x, y in roofL]
    wingL = [(48, BASE)] + roofL + [(BX0, BASE)]
    wingR = [(W - 48, BASE)] + roofR + [(BX1, BASE)]
    cup_glass = rect(CX - 46, AY - R - 74, CX + 46, AY - R + 6)
    cup_dome = [(CX - 56, AY - R - 72)] + arc_pts(CX, AY - R - 72, 56, math.pi, math.tau, 24, 0.62) + [(CX + 56, AY - R - 72)]
    glass = np.maximum.reduce([shapes(W, H, [arch], smooth=False), shapes(W, H, [wingL], smooth=False), shapes(W, H, [wingR], smooth=False),
                               shapes(W, H, [cup_glass], smooth=False)])
    # ---------- shadow on ground
    art = G(art, shapes(W, H, [deform(ellipse_pts(CX, BASE + 52, 380, 22, 20), rng, 1, 0.03)]), "#55665b", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=4, feather=8)
    door = [(CX - 40, BASE), (CX - 40, 810)] + arc_pts(CX, 810, 40, math.pi, math.tau, 20) + [(CX + 40, 810), (CX + 40, BASE)]
    dm = shapes(W, H, [door], smooth=False)
    # ---------- glass interior
    art = G(art, glass, GLASS_A, GLASS_B, seed=nx(), density=0.62, edge=0.35, bloom=0.4, rough=3, feather=1.0, pad=30)
    inner_light = glass * np.clip(1 - (np.mgrid[0:H, 0:W][0].astype(np.float32) - 260) / 700, 0, 1)
    art = lay(art, inner_light * 0.3, "#f6f1dc", 0.5)
    art = G(art, glass * np.clip((np.mgrid[0:H, 0:W][0].astype(np.float32) - 640) / 300, 0, 1), "#5f8a72", seed=nx(), density=0.45, edge=0, bloom=0.3, rough=2, feather=4)
    # back foliage (paler, behind haze)
    back = np.maximum.reduce([palm_cluster(W, H, CX - 10, 900, 11, 460, rng, 0.0, (58, 8), 1.05),
                              palm_cluster(W, H, 150, 880, 6, 230, rng, 0.25, (40, 6)),
                              palm_cluster(W, H, 632, 880, 6, 230, rng, -0.25, (40, 6))]) * glass
    art = paint_greens(art, back, nx, 0, density=0.58)
    clear()
    mid = np.maximum.reduce([palm_cluster(W, H, CX + 40, 900, 7, 250, rng, 0.15, (44, 7)),
                             fern_burst(W, H, 96, 820, 9, 110, rng), fern_burst(W, H, 690, 830, 9, 110, rng),
                             fern_burst(W, H, CX - 90, 860, 8, 120, rng), fern_burst(W, H, CX + 110, 870, 8, 100, rng)]) * glass
    art = paint_greens(art, mid, nx, 1, density=0.72)
    # tiny hanging baskets inside the bay
    for hx, hy in ((CX - 84, 520), (CX + 92, 560)):
        chain = strokes(W, H, [([(hx, AY - 40), (hx, hy - 10)], 1.4, None)]) * glass
        art = G(art, chain, IRON_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.4)
        art = paint_greens(art, fern_burst(W, H, hx, hy, 9, 52, rng, 0.0 - 0.2, math.pi + 0.2, (7, 3), 0.5) * glass, nx, 1)
        art = GP(art, shapes(W, H, [arc_pts(hx, hy - 4, 16, 0, math.pi, 12)]), TERRA, TERRA_D, seed=nx(), rough=0.6, pad=6)
    clear()
    # glass haze + reflections
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cells = np.random.default_rng(5).random((H // 60 + 2, W // 40 + 2)).astype(np.float32)
    pane = gaussian_filter(cells[(yy // 60).astype(int), (xx // 40).astype(int)], 1.5)
    art = lay(art, glass * (0.03 + 0.1 * pane), "#eef4ef", 1.0)
    # plants pressed against the glass (in front of the haze): crisp and dark at the foot
    front = np.maximum.reduce([fern_burst(W, H, 300, 900, 10, 120, rng, -math.pi - 0.1, 0.1, (14, 5.4), 0.3),
                               fern_burst(W, H, 480, 900, 10, 110, rng, -math.pi - 0.1, 0.1, (14, 5.4), 0.3),
                               fern_burst(W, H, 175, 900, 8, 95, rng, -math.pi, 0.0, (12, 5), 0.3),
                               fern_burst(W, H, 610, 900, 8, 95, rng, -math.pi, 0.0, (12, 5), 0.3)]) * glass * (1 - dm)
    art = paint_greens(art, front, nx, 2, density=0.75)
    refl = (np.sin((xx * 0.8 - yy * 0.55) / 26.0) > 0.86).astype(np.float32)
    refl = gaussian_filter(refl, 3) * glass * (fbm(W, H, 77, 120, 2) > 0.45)
    art = lay(art, refl * 0.5, "#ffffff", 0.6)
    # ---------- iron glazing
    bars = []
    T = 7
    for x in [BX0 + (BX1 - BX0) * k / 6 for k in range(1, 6)]:
        bars.append(([(x, AY), (x, BASE)], 3.8, None))
    for y in (AY, 600, 760):
        bars.append(([(BX0, y), (BX1, y)], 3.4, None))
    for k in range(1, 8):
        a = math.pi + math.pi * k / 8
        bars.append(([(CX, AY), (CX + math.cos(a) * R, AY + math.sin(a) * R)], 3.2, None))
    bars.append((arc_pts(CX, AY, R * 0.5, math.pi, math.tau, 24), 3.0, None))
    bars.append((arc_pts(CX, AY, R * 0.82, math.pi, math.tau, 30), 2.2, None))
    # wings: fan roof bars + verticals + transoms
    for side in (-1, 1):
        roof = roofL if side < 0 else roofR
        fx, fy = (BX0, 640) if side < 0 else (BX1, 640)
        for p in roof[3::5]:
            bars.append(([(fx, fy), p], 2.2, None))
        x0, x1 = (48, BX0) if side < 0 else (BX1, W - 48)
        for k in range(1, 6):
            x = x0 + (x1 - x0) * k / 6
            bars.append(([(x, 640), (x, BASE)], 3.4, None))
        for y in (640, 770):
            bars.append(([(x0, y), (x1, y)], 3.0, None))
        bars.append((roof, 5.0, None))
        bars.append(([(x0 if side < 0 else x1, 640), (x0 if side < 0 else x1, BASE)], 6.0, None))
    bars.append((arc_pts(CX, AY, R, math.pi, math.tau, 40), 6.5, None))
    bars += [([(BX0, AY), (BX0, BASE)], 7, None), ([(BX1, AY), (BX1, BASE)], 7, None)]
    for x in (CX - 46 + 23, CX, CX + 23):
        bars.append(([(x, AY - R - 74), (x, AY - R + 6)], 2.2, None))
    bars.append((rect(CX - 46, AY - R - 74, CX + 46, AY - R + 6) + [(CX - 46, AY - R - 74)], 4, None))
    bars.append(([(CX, AY - R - 108), (CX, AY - R - 150)], 3.2, None))
    # cresting: little spear finials along the arch + wing ridges
    crest = []
    for a in [math.pi + math.pi * (k + 0.5) / 12 for k in range(12)]:
        px, py = CX + math.cos(a) * (R + 3), AY + math.sin(a) * (R + 3)
        crest.append(petal_pts(px, py, 13, 3.2, a, n=8))
    for p in roofL[4:-4:4] + roofR[4:-4:4]:
        crest.append(petal_pts(p[0], p[1] + 1, 11, 3, -math.pi / 2, n=8))
    art = G(art, dm, "#a9c3bb", "#7f9f96", seed=nx(), density=0.6, edge=0.4, bloom=0.2, rough=2)
    bars.append((door + [door[0]], 4.0, None))
    bars.append(([(CX, 770), (CX, BASE)], 3.0, None))
    barm = strokes(W, H, bars, cap=True)
    dome = shapes(W, H, [cup_dome], smooth=False)
    finial = circles(W, H, [(CX, AY - R - 152, 7)])
    crest_m = shapes(W, H, crest)
    art = iron(art, np.maximum.reduce([barm, crest_m, finial]), nx)
    art = GP(art, dome, "#3c5c52", IRON_D, seed=nx(), rough=0.8, streak=0.8)
    art = lay(art, np.clip(dome * (1 - np.clip((xx - (CX - 30)) / 50, 0, 1)), 0, 1) * 0.5, IRON_L, 0.5)
    # gilded touches (finial ball, keystone)
    art = FO(art, np.maximum(finial, circles(W, H, [(CX, AY - R + 2, 6)])), "#c8a35a", seed=nx(), emboss=0.6)
    clear()
    # ---------- plinth (stone dwarf wall)
    plinth = shapes(W, H, [rect(30, BASE - 4, W - 30, BASE + 40)], smooth=False)
    art = GP(art, plinth, STONE, STONE_D, seed=nx(), rough=1.2, streak=1.0)
    joints = strokes(W, H, [([(x, BASE + 4 + (0 if (x // 60) % 2 else 20)), (x, BASE + 22 + (0 if (x // 60) % 2 else 18))], 1.2, None) for x in range(60, W - 30, 60)]
                     + [([(30, BASE + 20), (W - 30, BASE + 20)], 1.2, None)])
    art = G(art, joints * plinth, STONE_D, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.6, feather=0.5)
    art = G(art, edge_lo(plinth, 0, 5), "#7d705a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.6)
    cap = shapes(W, H, [rect(22, BASE - 10, W - 22, BASE + 2)], smooth=False)
    art = GP(art, cap, "#e8dfcd", STONE, seed=nx(), rough=0.8)
    # ---------- foreground urns with ferns
    for cx in (92, W - 92):
        art = paint_urn(art, W, H, cx, BASE + 46, 96, 78, nx)
        art = paint_greens(art, fern_burst(W, H, cx, BASE - 40, 13, 120, rng, -math.pi - 0.3, 0.3, (15, 5.5), 0.45), nx, 1, 0.7)
    clear()
    # ---------- morning rays (from the upper left)
    r = rays(W, H, -120, -160, [0.78, 0.9, 1.0, 1.12], [60, 34, 80, 40], 1500)
    art = lay(art, np.clip(r * 1.1, 0, 1), LIGHT, 0.38)
    prev(art, "rk-house", tone="#f1efe6")
    save(art, f"{OUT}/house.webp", max_w=700, quality=66)
    clear()

if "fern" in PARTS:
    # hanging Boston-fern basket on a chain (sways)
    W, H = 300, 470
    rng = random.Random(7); nx = Seq(4500)
    art = blank(W, H)
    ch = strokes(W, H, [([(150, 0), (150, 150)], 2.2, None), ([(150, 150), (100, 214)], 1.6, None), ([(150, 150), (200, 214)], 1.6, None)])
    art = iron(art, ch, nx, 6)
    fr = fern_burst(W, H, 150, 222, 18, 190, rng, -0.35, math.pi + 0.35, (19, 6.4), 0.45)
    up = fern_burst(W, H, 150, 214, 7, 80, rng, -math.pi + 0.3, -0.3, (10, 4), 0.1)
    art = paint_greens(art, np.maximum(fr, up), nx, 1, 0.68)
    basket = shapes(W, H, [arc_pts(150, 212, 56, 0, math.pi, 20, 0.75)])
    art = GP(art, basket, "#8b6a44", "#5e4528", seed=nx(), rough=0.8, streak=1.0)
    weave = strokes(W, H, [(arc_pts(150, 212, rr, 0.15, math.pi - 0.15, 16, 0.75), 1.4, None) for rr in (20, 34, 48)]) * basket
    art = G(art, weave, "#3e2c18", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.4, feather=0.5)
    art = paint_greens(art, fern_burst(W, H, 150, 230, 9, 150, rng, 0.35, math.pi - 0.35, (13, 4.6), 0.4), nx, 2, 0.6)
    prev(art, "rk-fern", tone="#eef1ea")
    save(art, f"{OUT}/fern.webp", max_w=220, quality=82)
    clear()

if "palm" in PARTS:
    W, H = 420, 640
    rng = random.Random(19); nx = Seq(4700)
    art = blank(W, H)
    art = G(art, shapes(W, H, [ellipse_pts(210, 624, 110, 12, 16)]), "#55665b", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=3, feather=5)
    stems = strokes(W, H, [(curve([(210, 470), (200 + d * 0.2, 380), (210 + d, 300)], 20), 4, (0.1, 0.5)) for d in (-60, -20, 30, 70)])
    art = G(art, stems, "#6f7d4a", "#4a5a35", seed=nx(), density=0.7, edge=0.4, rough=1.5)
    back = palm_cluster(W, H, 210, 470, 8, 300, rng, 0.0, (58, 8))
    art = paint_greens(art, back, nx, 1, 0.62)
    front = palm_cluster(W, H, 214, 480, 5, 230, rng, 0.05, (52, 8))
    art = paint_greens(art, front, nx, 0, 0.66)
    art = paint_urn(art, W, H, 210, 626, 190, 150, nx)
    # urn band of moulding
    band = shapes(W, H, [rect(124, 520, 296, 532)], smooth=False)
    art = G(art, band, TERRA_D, seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8)
    prev(art, "rk-palm", tone="#eef1ea")
    save(art, f"{OUT}/palm.webp", max_w=320, quality=82)
    clear()

if "divider" in PARTS:
    # Victorian cast-iron scroll divider (right half drawn, then mirrored)
    W, H = 560, 90
    nx = Seq(4900)
    C = 280
    items = [([(C + 26, 45), (C + 150, 45)], 2.4, None), ([(C + 150, 45), (C + 236, 45)], 2.2, (0.0, 0.5))]
    items.append((curve([(C + 30, 45), (C + 58, 30), (C + 88, 24), (C + 108, 32)], 30) + spiral_pts(C + 100, 40, 9, 2, -math.pi / 4, 0.9, 26, 1), 3.2, (0.0, 0.4)))
    items.append((curve([(C + 30, 45), (C + 58, 60), (C + 88, 66), (C + 108, 58)], 30) + spiral_pts(C + 100, 50, 9, 2, math.pi / 4, 0.9, 26, -1), 3.2, (0.0, 0.4)))
    items.append((curve([(C + 150, 45), (C + 164, 33), (C + 180, 30)], 14) + spiral_pts(C + 178, 36, 6, 1.5, -math.pi / 2, 0.85, 18, 1), 2.4, (0.0, 0.4)))
    m = strokes(W, H, items)
    m = np.maximum(m, m[:, ::-1])
    leafs = shapes(W, H, [petal_pts(C, 45, 24, 8, -math.pi / 2, n=12), petal_pts(C, 45, 24, 8, math.pi / 2, n=12),
                          petal_pts(C, 45, 26, 7, 0, n=10), petal_pts(C, 45, 26, 7, math.pi, n=10)])
    art = blank(W, H)
    art = iron(art, m, nx, 6)
    art = FO(art, np.maximum(leafs, circles(W, H, [(C - 236, 45, 4), (C + 236, 45, 4)])), "#c8a35a", seed=nx(), emboss=0.6)
    art = GP(art, circles(W, H, [(C, 45, 5)]), IRON, IRON_D, seed=nx(), rough=0.4, pad=4)
    prev(art, "rk-divider", tone="#f1efe6")
    save(art, f"{OUT}/divider.webp", max_w=400, quality=84)

if "sprig" in PARTS:
    W, H = 150, 150
    rng = random.Random(3); nx = Seq(5100)
    art = blank(W, H)
    pts = curve([(30, 130), (60, 80), (115, 28)], 24)
    art = paint_greens(art, frond(W, H, pts, 22, 7, step=1, spread=1.0, droop=0.2, n=8), nx, 1, 0.72)
    prev(art, "rk-sprig", tone="#f1efe6")
    save(art, f"{OUT}/sprig.webp", max_w=90, quality=84)
