"""Toko Roti — a vintage neighbourhood bakery, warm gouache: a scalloped striped awning, the shop window display (wooden
frame, glass reflections, a tiered cake on a stand, macaron stack, bread loaves, croissants, baguettes in a basket,
chalk price tags), a pastry box tied with baker's twine, a two-tier wedding cake with cherries, a croissant and a
bread-and-wheat divider. Original artwork, no brands.
Run: python3 -I toko-roti.py [part ...]   parts: awning window box cake croissant divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o5_lib import *

OUT = outdir("toko-roti")
PARTS = sys.argv[1:] or ["awning", "window", "box", "cake", "croissant", "divider"]
CREAM, CREAM_D = "#fbf1e2", "#ead8bd"
RED, RED_D, RED_L = "#c63d4b", "#962a37", "#de6670"
MINT, MINT_D, MINT_L = "#3f7d6b", "#2b5a4c", "#9cc5a1"
BUTTER = "#f2c75c"
COCOA, COCOA_D = "#5a3826", "#3b2318"
CRUST, CRUST_D, CRUST_L = "#c98a4a", "#94582a", "#e3b27a"
PINK, PINK_L = "#f1a7b3", "#f8cfd5"
WOOD, WOOD_D = "#a8754a", "#7a5232"


def awning():
    Wd, Hd = 800, 170
    nx = Seq(100)
    art = blank(Wd, Hd)
    sw = 50
    top = rect(Wd, Hd, 0, 0, Wd, 112)
    # scalloped lower edge
    sc = circles(Wd, Hd, [(x + sw / 2, 112, sw / 2) for x in range(0, Wd, sw)])
    body = np.clip(top + sc * below(Hd, 100, 1), 0, 1)
    art = P(art, body, CREAM, "#fff7ea", seed=nx(), rough=1.2)
    stripes = np.zeros((Hd, Wd), np.float32)
    xx = np.arange(Wd)
    sel = ((xx // sw) % 2 == 0).astype(np.float32)[None, :] * np.ones((Hd, 1), np.float32)
    art = P(art, body * sel, RED, RED_L, seed=nx(), rough=0.8)
    # folds: each stripe slightly darker on its left
    fold = ((xx % sw) < 10).astype(np.float32)[None, :] * np.ones((Hd, 1), np.float32)
    art = tint(art, body * fold, "#000000", 0.08, blur=3)
    # top rail shadow and the scallop hem shading
    art = tint(art, body * above(Hd, 20, 14), COCOA_D, 0.25)
    art = tint(art, body * below(Hd, 98, 10), "#000000", 0.12)
    rail = rect(Wd, Hd, 0, 0, Wd, 12)
    art = P(art, rail, MINT_D, MINT, seed=nx(), rough=0.4)
    art = tint(art, edge_ring(body, 1.4), RED_D, 0.5)
    # soft cast shadow under the scallops
    sh = np.roll(sc * below(Hd, 112, 1), 12, 0)
    art = over(tint(blank(Wd, Hd), sh, "#3a2a20", 0.25, blur=5), art)
    art = add_grain(art, 3, 0.03)
    save_full(art, f"{OUT}/awning.webp", size=(780, 166), quality=80)
    preview(art, "tr-awning", bg=MINT_L)


def cake_on(art, Wd, Hd, cx, by, s, nx, rng, tiers=2, stand=True, top_col=CREAM, drip=PINK):
    """Tiered cake (front view, slight ellipse tops) with drips, piping beads and cherries; optional pedestal stand."""
    if stand:
        plate = shapes(Wd, Hd, [ellipse_pts(cx, by, s * 1.1, s * 0.16, 20)])
        foot = shapes(Wd, Hd, [[(cx - s * 0.14, by), (cx + s * 0.14, by), (cx + s * 0.3, by + s * 0.42), (cx - s * 0.3, by + s * 0.42)]])
        art = P(art, foot, "#dfe7e4", "#c9d4d0", seed=nx(), rough=0.6)
        art = P(art, plate, "#eef3f1", "#d3dcd8", seed=nx(), rough=0.6)
        art = tint(art, edge_ring(np.maximum(plate, foot), 1.2), "#9aa8a3", 0.7)
        by -= s * 0.06
    y = by
    widths = [s * 0.95, s * 0.68, s * 0.45][:tiers]
    hs = [s * 0.52, s * 0.46, s * 0.4]
    for k, w in enumerate(widths):
        h = hs[k]
        body = shapes(Wd, Hd, [[(cx - w, y), (cx - w, y - h)] + arc_pts(cx, y - h, w, math.pi, 2 * math.pi, 24, 0.22) + [(cx + w, y - h), (cx + w, y)] + arc_pts(cx, y, w, 0, math.pi, 24, 0.22)])
        art = P(art, body, top_col, "#fff8ee", seed=nx(), rough=0.8)
        art = tint(art, body * (1 - right_of(Wd, cx - w * 0.4, w * 0.8)), CREAM_D, 0.55)
        # drips from the top edge
        dr = []
        for t in np.linspace(-0.92, 0.92, 9):
            x = cx + t * w
            L = h * rng.uniform(0.22, 0.5)
            yt = y - h + abs(t) ** 2 * 0 + w * 0.22 * (1 - t * t) ** 0.5
            dr.append(([(x, yt), (x, yt + L)], w * 0.16, (0.0, 0.0)))
        top = shapes(Wd, Hd, [arc_pts(cx, y - h, w, 0, math.tau, 40, 0.22)])
        dm = np.clip(strokes(Wd, Hd, dr) + top * 0 + shapes(Wd, Hd, [[(cx - w, y - h)] + arc_pts(cx, y - h, w, math.pi, 0, 30, -0.22)[::-1] + [(cx + w, y - h + w * 0.05)] + arc_pts(cx, y - h + w * 0.08, w, 0, math.pi, 30, 0.22)]), 0, 1) * body
        art = P(art, np.maximum(dm, top), drip, mix(drip, "#ffffff", 0.25), seed=nx(), rough=0.6)
        art = tint(art, top * above(Hd, y - h - w * 0.05, 6), "#ffffff", 0.35)
        # piping beads along the bottom
        beads = circles(Wd, Hd, [(cx + math.cos(a) * w, y + math.sin(a) * w * 0.22, s * 0.045) for a in np.linspace(0.15, math.pi - 0.15, 14)])
        art = P(art, beads, "#fffaf0", seed=nx(), rough=0.3)
        art = tint(art, beads * below(Hd, y, 4), CREAM_D, 0.6)
        art = tint(art, edge_ring(body, 1.3), "#b89a7a", 0.55)
        y = y - h
    # cherries on top
    for dx in (-0.12, 0.08, 0.22):
        x = cx + dx * s
        cy = y - s * 0.02 - abs(dx) * s * 0.05
        ch = circles(Wd, Hd, [(x, cy, s * 0.075)])
        art = P(art, ch, RED, RED_D, seed=nx(), rough=0.4)
        art = tint(art, circles(Wd, Hd, [(x - s * 0.025, cy - s * 0.025, s * 0.02)]), "#ffffff", 0.8)
        art = tint(art, strokes(Wd, Hd, [(curve([(x, cy - s * 0.06), (x + s * 0.03, cy - s * 0.14), (x + s * 0.08, cy - s * 0.18)], 8), 2.0, None)]), "#4a6a2a", 0.9)
    return art


def loaf_on(art, Wd, Hd, cx, cy, w, h, nx, rng, scores=4, ang=0.0, col=CRUST):
    m = shapes(Wd, Hd, [ellipse_pts(cx, cy, w, h, 22, ang)])
    art = P(art, m, col, CRUST_L, seed=nx(), rough=0.8)
    art = W(art, m * below(Hd, cy, h * 0.8), CRUST_D, seed=nx(), density=0.45, edge=0.25, rough=2)
    art = tint(art, m * above(Hd, cy - h * 0.3, h * 0.6), "#f0c890", 0.35)
    sc = []
    for k in range(scores):
        t = (k + 0.5) / scores * 1.6 - 0.8
        x0 = cx + t * w * math.cos(ang) - h * 0.45 * math.sin(ang)
        y0 = cy + t * w * math.sin(ang) - h * 0.45
        sc.append((curve([(x0 - w * 0.12, y0 + h * 0.3), (x0, y0), (x0 + w * 0.14, y0 - h * 0.12)], 8), h * 0.16, (0.2, 0.3)))
    sm = strokes(Wd, Hd, sc) * m
    art = P(art, sm, "#f3d6a6", "#e9c288", seed=nx(), rough=0.4)
    art = tint(art, edge_ring(sm, 1.0), CRUST_D, 0.6)
    art = tint(art, edge_ring(m, 1.4), "#7a4520", 0.6)
    return art


def croissant_on(art, Wd, Hd, cx, cy, s, nx, rot_=0.0):
    """Crescent croissant: one plump curved body, rolled-layer ridges across it, glossy egg-wash highlight."""
    R = s * 0.62
    ocx, ocy = cx, cy + R * 0.75
    a0, a1 = math.radians(195), math.radians(345)
    outer, inner = [], []
    for i in range(33):
        t = i / 32
        a = a0 + (a1 - a0) * t
        th = s * 0.5 * (math.sin(math.pi * t) ** 0.7) + s * 0.05
        outer.append((ocx + math.cos(a) * (R + th * 0.55), ocy + math.sin(a) * (R + th * 0.55)))
        inner.append((ocx + math.cos(a) * (R - th * 0.45), ocy + math.sin(a) * (R - th * 0.45)))
    body = shapes(Wd, Hd, [rot(outer + inner[::-1], cx, cy, rot_)])
    art = P(art, body, CRUST, CRUST_L, seed=nx(), rough=0.6)
    art = W(art, body * below(Hd, cy + s * 0.05, s * 0.2), CRUST_D, seed=nx(), density=0.5, edge=0.25, rough=1.5)
    ridges = []
    for k in range(1, 6):
        t = k / 6
        a = a0 + (a1 - a0) * t
        th = s * 0.5 * (math.sin(math.pi * t) ** 0.7) + s * 0.05
        p0 = (ocx + math.cos(a - 0.05) * (R + th * 0.6), ocy + math.sin(a - 0.05) * (R + th * 0.6))
        pm = (ocx + math.cos(a + 0.04) * R, ocy + math.sin(a + 0.04) * R)
        p1 = (ocx + math.cos(a - 0.03) * (R - th * 0.5), ocy + math.sin(a - 0.03) * (R - th * 0.5))
        ridges.append((curve(rot([p0, pm, p1], cx, cy, rot_), 10), max(1.5, s * 0.03), (0.15, 0.15)))
    art = tint(art, strokes(Wd, Hd, ridges) * body, "#7a4520", 0.55)
    hl = []
    for k in range(6):
        t0, t1 = k / 6 + 0.03, (k + 1) / 6 - 0.05
        pts = [(ocx + math.cos(a0 + (a1 - a0) * tt) * (R + s * 0.1 * math.sin(math.pi * tt)), ocy + math.sin(a0 + (a1 - a0) * tt) * (R + s * 0.1 * math.sin(math.pi * tt))) for tt in np.linspace(t0, t1, 6)]
        hl.append((rot(pts, cx, cy, rot_), max(1.5, s * 0.05), (0.3, 0.3)))
    art = tint(art, strokes(Wd, Hd, hl) * body, "#f8d9a0", 0.6, blur=0.6)
    art = tint(art, edge_ring(body, 1.2), "#6a3a18", 0.65)
    return art


def macarons_on(art, Wd, Hd, cx, by, s, nx):
    cols = [(PINK, "#e98a9a"), (MINT_L, "#7fb08a"), (BUTTER, "#e0ae3a"), ("#c9a6d9", "#a886bd"), (PINK, "#e98a9a")]
    y = by
    for k, (c1, c2) in enumerate(cols):
        w = s * (1 - k * 0.09)
        for part, dy in (("shell", 0), ("fill", -s * 0.2), ("shell", -s * 0.3)):
            if part == "shell":
                m = shapes(Wd, Hd, [ellipse_pts(cx, y + dy, w, s * 0.17, 18)])
                art = P(art, m, c1, c2, seed=nx(), rough=0.5)
                art = tint(art, m * above(Hd, y + dy - s * 0.04, 4), "#ffffff", 0.25)
                art = tint(art, edge_ring(m, 1.1), c2, 0.8)
            else:
                art = P(art, rect(Wd, Hd, cx - w * 0.92, y + dy - s * 0.05, cx + w * 0.92, y + dy + s * 0.07), "#fff6e8", seed=nx(), rough=0.6)
        y -= s * 0.5
    return art


def tag_on(art, Wd, Hd, x, y, nx, rng, w=46, h=30):
    """Little chalk price tag on a stick: slate board, chalk squiggle numbers (not real text)."""
    art = P(art, strokes(Wd, Hd, [([(x, y + h / 2), (x, y + h / 2 + 26)], 2.6, None)]), WOOD_D, seed=nx(), rough=0.3)
    b = rr_mask(Wd, Hd, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 4)
    art = P(art, b, "#2e3330", "#3a403c", seed=nx(), rough=0.4)
    art = tint(art, edge_ring(b, 1.2), WOOD, 0.9)
    sq = []
    for k in range(3):
        x0 = x - w * 0.32 + k * w * 0.24
        sq.append((curve([(x0, y + 4), (x0 + 4, y - 7), (x0 + 8, y + 1), (x0 + 3, y + 6)], 10), 1.6, None))
    sq.append(([(x - w * 0.34, y + 9), (x + w * 0.34, y + 9)], 1.2, None))
    art = tint(art, strokes(Wd, Hd, sq), "#f3f1ea", 0.85)
    return art


def window():
    Wd, Hd = 720, 600
    nx = Seq(300); rng = random.Random(8)
    art = blank(Wd, Hd)
    fr = rr_mask(Wd, Hd, 0, 0, Wd, Hd, 26)
    glass_m = rr_mask(Wd, Hd, 34, 34, Wd - 34, Hd - 70, 12)
    art = P(art, fr, MINT, MINT_L, seed=nx(), rough=1)
    art = tint(art, fr * (1 - glass_m) * above(Hd, 30, 10), "#ffffff", 0.18)
    art = tint(art, edge_ring(fr, 2), MINT_D, 0.7)
    # warm lit interior behind the glass
    interior = painted_sky(Wd, Hd, [(0, "#f9e7c7"), (0.6, "#f5d9a8"), (1.0, "#e9c08a")], seed=4, streak=0.8)
    interior[..., 3] = glass_m
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
    vig = np.clip(((xx - Wd / 2) / (Wd / 2)) ** 2 * 0.6 + ((yy - Hd * 0.42) / (Hd / 2)) ** 2 * 0.8, 0, 1)
    interior[..., :3] *= (1 - 0.22 * vig)[..., None]
    art = over(art, interior)
    # back wall tiles hint + hanging pendant light
    art = tint(art, glass_m * (np.abs(((np.arange(Wd)[None, :] + 0 * np.arange(Hd)[:, None]) % 40) - 20) < 1).astype(np.float32) * above(Hd, 200, 2), "#e3c08e", 0.6)
    art = P(art, strokes(Wd, Hd, [([(360, 34), (360, 70)], 2, None)]), COCOA, seed=nx(), rough=0.2)
    lamp = shapes(Wd, Hd, [[(330, 92), (390, 92), (376, 70), (344, 70)]], smooth=False)
    art = OV(art, circles(Wd, Hd, [(360, 100, 30)]), lambda m: glow(m, "#fff3cf", 24, 0.45), pad=80)
    art = P(art, lamp, MINT_D, MINT, seed=nx(), rough=0.3)
    # shelves
    for sy in (276, 494):
        sh = rect(Wd, Hd, 34, sy, Wd - 34, sy + 16)
        art = P(art, sh, WOOD, "#bd8a5c", seed=nx(), rough=0.6)
        art = tint(art, rect(Wd, Hd, 34, sy + 12, Wd - 34, sy + 16), WOOD_D, 0.7)
        art = tint(art, rect(Wd, Hd, 34, sy + 16, Wd - 34, sy + 30) * glass_m, "#8a5a32", 0.2, blur=3)
    clear()
    # top shelf: tiered cake on a stand (centre), macaron tower (left), croissant plate (right)
    art = cake_on(art, Wd, Hd, 360, 230, 104, nx, rng, tiers=2)
    art = macarons_on(art, Wd, Hd, 150, 262, 46, nx)
    pl = shapes(Wd, Hd, [ellipse_pts(570, 270, 92, 12, 18)])
    art = P(art, pl, "#ffffff", "#eef0ee", seed=nx(), rough=0.4)
    art = tint(art, edge_ring(pl, 1.2), "#b9c2be", 0.7)
    for cx_, cy_, r_ in ((532, 250, 0.12), (612, 252, -0.15), (574, 226, 0.02)):
        art = croissant_on(art, Wd, Hd, cx_, cy_, 78, nx, r_)
    art = tag_on(art, Wd, Hd, 240, 230, nx, rng)
    art = tag_on(art, Wd, Hd, 470, 236, nx, rng)
    clear()
    # bottom shelf: basket of baguettes (left), loaves (centre), round boule + bun pile (right)
    bask = shapes(Wd, Hd, [[(80, 400), (220, 400), (206, 492), (94, 492)]], smooth=False)
    for k in range(5):
        x = 100 + k * 26
        bag = shapes(Wd, Hd, [rot(ellipse_pts(x, 360, 14, 82, 14), x, 420, -0.18 + k * 0.09)])
        art = loaf_on(art, Wd, Hd, x, 360, 14, 82, nx, rng, scores=0, ang=0) if False else art
        art = P(art, bag, CRUST, CRUST_L, seed=nx(), rough=0.6)
        art = tint(art, bag * (1 - right_of(Wd, x - 4, 10)), CRUST_D, 0.45)
        cuts = strokes(Wd, Hd, [(curve([(x - 8, yy + 8), (x, yy), (x + 8, yy - 6)], 6), 3, (0.2, 0.2)) for yy in (316, 346, 376)]) * bag
        art = tint(art, cuts, "#f3d6a6", 0.9)
        art = tint(art, edge_ring(bag, 1.2), "#7a4520", 0.6)
    art = P(art, bask, "#c7a06a", "#b48c54", seed=nx(), rough=0.6)
    wov = strokes(Wd, Hd, [([(84, y), (216, y)], 2.2, None) for y in range(408, 492, 10)] + [([(x, 400), (x - 2, 492)], 1.6, None) for x in range(96, 210, 12)]) * bask
    art = tint(art, wov, "#8a6a3c", 0.6)
    art = tint(art, edge_ring(bask, 1.3), "#6a4a24", 0.7)
    art = P(art, rect(Wd, Hd, 70, 396, 230, 408), "#d9b47e", "#c7a06a", seed=nx(), rough=0.4)
    art = loaf_on(art, Wd, Hd, 350, 452, 92, 40, nx, rng, scores=4)
    art = loaf_on(art, Wd, Hd, 330, 482, 78, 18, nx, rng, scores=0, col="#b9763c")
    art = loaf_on(art, Wd, Hd, 560, 450, 66, 50, nx, rng, scores=3)
    for bx, by_ in ((636, 476), (660, 478), (648, 456)):
        art = loaf_on(art, Wd, Hd, bx, by_, 22, 18, nx, rng, scores=0, col="#d49a58")
    art = tag_on(art, Wd, Hd, 250, 452, nx, rng)
    art = tag_on(art, Wd, Hd, 470, 444, nx, rng)
    clear()
    # contact shadows on both shelves
    for sy in (276, 494):
        art = tint(art, shapes(Wd, Hd, [ellipse_pts(x, sy - 2, w, 6, 14) for x, w in ((150, 50), (360, 110), (570, 96), (150, 70), (350, 96), (560, 70), (648, 40))]) * glass_m, "#6a4422", 0.0, blur=3)
    # glass reflections: two diagonal soft streaks
    refl = shapes(Wd, Hd, [[(420, 34), (500, 34), (300, Hd - 70), (220, Hd - 70)], [(530, 34), (556, 34), (356, Hd - 70), (330, Hd - 70)]], smooth=False) * glass_m
    art = tint(art, refl, "#ffffff", 0.16, blur=4)
    # inner frame bevel + sill
    art = tint(art, edge_ring(glass_m, 2.4), MINT_D, 0.6)
    sill = rect(Wd, Hd, 16, Hd - 62, Wd - 16, Hd - 40)
    art = P(art, sill, CREAM, "#f3e3c8", seed=nx(), rough=0.5)
    art = tint(art, rect(Wd, Hd, 16, Hd - 44, Wd - 16, Hd - 40), "#c9b090", 0.7)
    art = add_grain(art, 9, 0.03)
    save(art, f"{OUT}/window.webp", max_w=680, quality=78)
    preview(art, "tr-window", bg="#9cc5a1")


def box():
    Wd, Hd = 420, 360
    nx = Seq(500)
    art = blank(Wd, Hd)
    # pastry box in 3/4 view: front face, side face, lid top
    front = shapes(Wd, Hd, [[(40, 160), (260, 190), (260, 340), (40, 310)]], smooth=False)
    side = shapes(Wd, Hd, [[(260, 190), (390, 150), (390, 296), (260, 340)]], smooth=False)
    top = shapes(Wd, Hd, [[(40, 160), (170, 122), (390, 150), (260, 190)]], smooth=False)
    art = P(art, front, "#fdf6ec", "#f6ead8", seed=nx(), rough=0.8)
    art = P(art, side, "#efe0c8", "#e6d3b6", seed=nx(), rough=0.8)
    art = P(art, top, "#fffaf2", seed=nx(), rough=0.8)
    # pink stripes on the front + side faces
    for k in range(6):
        x0 = 52 + k * 36
        st = shapes(Wd, Hd, [[(x0, 162 + (x0 - 40) * 0.136), (x0 + 16, 164 + (x0 - 24) * 0.136), (x0 + 16, 314 + (x0 - 24) * 0.136), (x0, 312 + (x0 - 40) * 0.136)]], smooth=False) * front
        art = P(art, st, "#ec8d9c", PINK, seed=nx(), rough=0.4)
    for k in range(3):
        x0 = 276 + k * 38
        y0 = 190 - (x0 - 260) * 0.31
        st = shapes(Wd, Hd, [[(x0, y0), (x0 + 16, y0 - 5), (x0 + 16, y0 + 144 - 5 - (16 * 0.03)), (x0, y0 + 146)]], smooth=False) * side
        art = P(art, st, "#d97887", "#e88a9a", seed=nx(), rough=0.4)
    art = tint(art, side, "#000000", 0.07)
    # twine: red-white baker's twine across the lid and down the faces, with a bow
    tw_pts = [[(40, 160 + 0), (100, 142), (170, 122)], [(105, 141), (325, 170)], [(215, 135), (148, 176)], [(150, 176), (150, 326)], [(325, 170), (325, 318)]]
    twine = strokes(Wd, Hd, [(curve(p, 12), 4.2, None) for p in tw_pts[1:]])
    art = P(art, twine, "#fffaf2", seed=nx(), rough=0.3)
    dash = strokes(Wd, Hd, [(curve(p, 40), 4.2, None) for p in tw_pts[1:]]) * (np.sin((np.arange(Wd)[None, :] + np.arange(Hd)[:, None]) * 0.55) > 0.2)
    art = tint(art, dash, RED, 0.95)
    bx, by_ = 215, 158
    loops = strokes(Wd, Hd, [(curve([(bx, by_), (bx - 30, by_ - 34), (bx - 50, by_ - 8), (bx, by_)], 20), 5, None), (curve([(bx, by_), (bx + 36, by_ - 30), (bx + 52, by_ - 2), (bx, by_)], 20), 5, None),
                            (curve([(bx, by_), (bx - 16, by_ + 30), (bx - 30, by_ + 52)], 12), 4.4, (0.0, 0.4)), (curve([(bx, by_), (bx + 14, by_ + 34), (bx + 30, by_ + 50)], 12), 4.4, (0.0, 0.4))])
    art = P(art, loops, "#fffaf2", seed=nx(), rough=0.3)
    art = tint(art, loops * (np.sin((np.arange(Wd)[None, :] - np.arange(Hd)[:, None]) * 0.6) > 0.2), RED, 0.95)
    art = P(art, circles(Wd, Hd, [(bx, by_, 7)]), RED_D, seed=nx(), rough=0.3)
    art = tint(art, edge_ring(np.clip(front + side + top, 0, 1), 1.4), "#b49a80", 0.7)
    # soft ground shadow
    sh = shapes(Wd, Hd, [ellipse_pts(220, 330, 190, 18, 20)])
    art = over(tint(blank(Wd, Hd), sh, "#5a3826", 0.25, blur=8), art)
    save(art, f"{OUT}/box.webp", max_w=320, quality=82)
    preview(art, "tr-box")


def cake():
    Wd, Hd = 420, 460
    nx = Seq(600); rng = random.Random(3)
    art = blank(Wd, Hd)
    art = cake_on(art, Wd, Hd, 210, 380, 160, nx, rng, tiers=3, stand=True, drip=PINK)
    save(art, f"{OUT}/cake.webp", max_w=300, quality=82)
    preview(art, "tr-cake")


def croissant():
    Wd, Hd = 220, 150
    nx = Seq(700)
    art = croissant_on(blank(Wd, Hd), Wd, Hd, 110, 70, 120, nx, 0.0)
    save(art, f"{OUT}/croissant.webp", max_w=140, quality=84)
    preview(art, "tr-croissant")


def divider():
    Wd, Hd = 520, 110
    nx = Seq(800); rng = random.Random(5)
    art = blank(Wd, Hd)
    cx = Wd / 2
    # wheat sprigs both sides
    for sgn in (-1, 1):
        stem = curve([(cx + sgn * 60, 64), (cx + sgn * 150, 56), (cx + sgn * 230, 40)], 30)
        art = P(art, strokes(Wd, Hd, [(stem, 2.4, (0.0, 0.4))]), "#c69a4a", seed=nx(), rough=0.3)
        grains = []
        for x, y, a in along(stem, 13)[3:]:
            for side in (-1, 1):
                grains.append(petal_pts(x, y, 15, 5.5, a + (math.pi if sgn < 0 else 0) * 0 + side * 0.55 + (math.pi if sgn < 0 else 0), n=10))
        gm = shapes(Wd, Hd, grains)
        art = P(art, gm, "#e2b45a", "#d39d3c", seed=nx(), rough=0.4)
        art = tint(art, edge_ring(gm, 1.0), "#9a6a24", 0.7)
    art = croissant_on(art, Wd, Hd, cx, 54, 96, nx, 0.0)
    save(art, f"{OUT}/divider.webp", max_w=380, quality=84)
    preview(art, "tr-divider")


for p in PARTS:
    globals()[p]()
    clear()
