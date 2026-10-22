"""Jambi Angso Duo — batik Jambi in canting-wax style with natural dyes (sepang red, indigo, kuning): the angso duo
(two geese facing each other), tumpal border, rumah Kajang Leko with its boat-curved roof on the Batanghari at dusk.
Run: python3 -I jambi-angso.py [part ...]  parts: batik tumpal angso river divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b2_lib import *

OUT = outdir("jambi-angso")
PARTS = sys.argv[1:] or ["batik", "tumpal", "angso", "river", "divider"]
SEPANG, SEPANG_D = "#9b3a2a", "#7a2a1f"
INDIGO, INDIGO_D = "#27365e", "#1a2444"
KUNING = "#d9a62e"
WAX = "#f2e4c4"
CLOTH = "#efe0bd"


def goose(W, H, ox, oy, s, face=1):
    """Stylised batik goose (facing right when face=1). Returns (body_mask, wing_mask, wax_lines list, eye)."""
    def P(x, y):
        return (ox + face * x * s, oy + y * s)
    body = shapes(W, H, [[P(-50, -2), P(-30, -8), P(0, -4), P(26, 0), P(36, 14), P(24, 32), P(-6, 38), P(-34, 30), P(-46, 16), P(-62, -14)]])
    neck = strokes(W, H, [([P(22, 6), P(34, -10), P(30, -30), P(24, -46), P(30, -60), P(42, -64)], 13 * s, (0.0, 0.0))])
    head = circles(W, H, [(*P(44, -62), 9 * s)])
    beak = shapes(W, H, [[P(50, -66), P(66, -60), P(50, -56)]], smooth=False)
    wing = shapes(W, H, [[P(-36, 6), P(-14, -1), P(8, 6), P(12, 18), P(-2, 24), P(-24, 20)]])
    lines = []
    for k in range(3):  # scalloped feather rows on the wing
        y = 9 + k * 5
        lines.append(curve([P(-28 + k * 4, y), P(-16 + k * 3, y + 4), P(-4 + k * 2, y), P(6, y + 4)], 14))
    lines.append(curve([P(-60, -12), P(-46, -4), P(-34, 4)], 10))
    lines.append(curve([P(-6, 36), P(10, 30), P(26, 18)], 10))
    eye = (*P(45, -63), 2.6 * s)
    return np.clip(body + neck + head + beak, 0, 1), wing, lines, eye


def bungo(W, H, cx, cy, r):
    """Bungo tagapo-like small flower: 4 petals + 4 small leaves."""
    pet = [petal_pts(cx, cy, r, r * 0.45, k * math.pi / 2 + math.pi / 4, n=10) for k in range(4)]
    lf = [petal_pts(cx, cy, r * 0.75, r * 0.22, k * math.pi / 2, n=8) for k in range(4)]
    return shapes(W, H, pet), shapes(W, H, lf)


def paint_pair(art, W, H, cx, cy, s, nx, wax_w=2.2):
    b1, w1, l1, e1 = goose(W, H, cx - 70 * s, cy + 6 * s, s, 1)
    b2, w2, l2, e2 = goose(W, H, cx + 70 * s, cy + 6 * s, s, -1)
    bodies = np.maximum(b1, b2); wings = np.maximum(w1, w2)
    art = over(art, dye(bodies, INDIGO, seed=nx(), bleed=1.2))
    art = over(art, dye(wings, KUNING, seed=nx(), bleed=1.0))
    wax = wax_line(W, H, l1 + l2, wax_w * s * 0.9, seed=nx())
    wax = np.maximum(wax, outline(bodies, wax_w * s) * 1.0)
    wax = np.maximum(wax, outline(wings, 1.6 * s))
    art = over(art, flat(np.clip(wax, 0, 1), WAX, 0.95))
    art = over(art, flat(circles(W, H, [e1, e2]), WAX, 1.0))
    # heart-shaped space between the necks: kuning drop
    drop = shapes(W, H, [[(cx, cy - 34 * s), (cx + 10 * s, cy - 16 * s), (cx, cy - 2 * s), (cx - 10 * s, cy - 16 * s)]])
    art = over(art, dye(drop, KUNING, seed=nx()))
    return art


if "batik" in PARTS:
    W, H = 320, 320
    nx = Seq(72100)
    art = cloth_base(W, H, SEPANG, seed=nx(), cell=1.6, var=0.14)
    art = over(art, dye(np.ones((H, W), np.float32), SEPANG_D, seed=nx(), density=0.25, crackle=0.9))
    # diamond frames (kapal sanggat) around each pair, plus corner frames for seamless repeat
    def diamond(cx, cy, r):
        return [(cx, cy - r), (cx + r * 1.05, cy), (cx, cy + r), (cx - r * 1.05, cy), (cx, cy - r)]
    lines = [diamond(160, 160, 132), diamond(160, 160, 120)]
    art = paint_pair(art, W, H, 160, 178, 1.05, nx)
    for (x, y) in [(0, 0), (W, 0), (0, H), (W, H)]:
        p, l = bungo(W, H, x, y, 22)
        art = over(art, dye(p, INDIGO, seed=nx()))
        art = over(art, dye(l, KUNING, seed=nx()))
        art = over(art, flat(np.maximum(outline(p, 2.0), outline(l, 1.6)), WAX, 0.95))
        art = over(art, flat(circles(W, H, [(x, y, 4)]), WAX, 1))
    for (x, y) in [(160, 0), (160, H), (0, 160), (W, 160)]:
        p, l = bungo(W, H, x, y, 13)
        art = over(art, dye(p, KUNING, seed=nx()))
        art = over(art, flat(outline(p, 1.6), WAX, 0.9))
    art = over(art, flat(wax_line(W, H, lines, 2.2, seed=nx()), WAX, 0.92))
    # isen cecek: wax dots along the diamond
    pts = []
    for (a, b) in [((160, 22), (298, 160)), ((298, 160), (160, 298)), ((160, 298), (22, 160)), ((22, 160), (160, 22))]:
        for t in np.linspace(0.06, 0.94, 14):
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    art = over(art, flat(circles(W, H, [(x, y, 1.8) for x, y in pts]), WAX, 0.9))
    art[..., 3] = 1
    preview(art, "ja-batik", bg=SEPANG)
    save_rgb(art, f"{OUT}/batik.webp", quality=80)
    clear()

if "tumpal" in PARTS:
    # tumpal (pucuk rebung) band, tile 160 x 90, repeat-x: indigo ground, kuning teeth with wax outline + sepang core
    W, H = 160, 90
    nx = Seq(72200)
    art = cloth_base(W, H, INDIGO, seed=nx(), cell=1.6, var=0.12)
    teeth = [[(x, H - 8), (x + 40, 10), (x + 80, H - 8)] for x in (-80, 0, 80, 160)]
    inner = [[(x + 18, H - 14), (x + 40, 36), (x + 62, H - 14)] for x in (-80, 0, 80, 160)]
    tm = shapes(W, H, teeth, smooth=False); im = shapes(W, H, inner, smooth=False)
    art = over(art, dye(tm, KUNING, seed=nx(), bleed=0.8))
    art = over(art, dye(im, SEPANG, seed=nx(), bleed=0.8))
    art = over(art, flat(np.maximum(outline(tm, 2.2), outline(im, 1.6)), WAX, 0.95))
    art = over(art, flat(rect(W, H, 0, H - 6, W, H - 3), WAX, 0.85))
    art = over(art, flat(circles(W, H, [(x + 80, 22, 2.4) for x in (-80, 0, 80)] + [(x + 40, H - 24, 2) for x in (-80, 0, 80, 160)]), WAX, 0.9))
    art[..., 3] = 1
    preview(art, "ja-tumpal", bg=INDIGO)
    save_rgb(art, f"{OUT}/tumpal.webp", quality=80)
    clear()

if "angso" in PARTS:
    # roundel: the pair inside a sepang roundel on cream cloth edge (transparent outside)
    W, H = 320, 300
    nx = Seq(72300)
    disc = shapes(W, H, [deform(ellipse_pts(160, 150, 150, 140, 40), random.Random(3), 2, 0.01)])
    cloth = cloth_base(W, H, SEPANG, seed=nx(), cell=1.6, var=0.12)
    cloth[..., 3] = np.clip(displace(disc, nx(), 2.0, 10), 0, 1)
    art = cloth
    art = paint_pair(art, W, H, 160, 168, 1.15, nx)
    art = over(art, flat(wax_line(W, H, [ellipse_pts(160, 150, 136, 126, 60) + [ellipse_pts(160, 150, 136, 126, 60)[0]]], 2.4, seed=nx()), WAX, 0.9))
    preview(art, "ja-angso", bg=CLOTH)
    save(art, f"{OUT}/angso.webp", max_w=220, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 600, 64
    nx = Seq(72400); cy = 32
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 3, 0, 1)[None, :]
    l = wax_line(W, H, [curve([(40, cy), (120, cy - 8), (200, cy + 8), (260, cy)], 30), curve([(340, cy), (400, cy + 8), (480, cy - 8), (560, cy)], 30)], 2.6, seed=nx())
    art = over(blank(W, H), dye(l * fade, INDIGO, seed=nx(), bleed=0.5))
    dots = circles(W, H, [(x, cy + (6 if i % 2 else -6), 2.6) for i, x in enumerate(range(60, 250, 16))] + [(x, cy + (6 if i % 2 else -6), 2.6) for i, x in enumerate(range(352, 545, 16))])
    art = over(art, dye(dots * fade, SEPANG, seed=nx(), bleed=0.4))
    p, lf = bungo(W, H, 300, cy, 24)
    art = over(art, dye(p, SEPANG, seed=nx()))
    art = over(art, dye(lf, KUNING, seed=nx()))
    art = over(art, flat(circles(W, H, [(300, cy, 4)]), KUNING, 1))
    preview(art, "ja-divider", bg=CLOTH)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clear()


def kajang_leko(W, H, cx, floor_y, s, nx, rng, art, dusk=True):
    """Rumah Kajang Leko: long stilt house, walls of wood, the roof 'kajang lako' — ridge curving up at both ends like
    an upturned boat, triangular gable (tebar layar) under it, ladder, posts in the water edge."""
    hw = 150 * s
    wall_top = floor_y - 70 * s
    ridge_y = wall_top - 64 * s
    posts = polyline_mask(W, H, [[(cx + dx * s, floor_y), (cx + dx * s, floor_y + 64 * s)] for dx in range(-140, 150, 35)], 6 * s, cap=False)
    wall = rect(W, H, cx - hw + 8 * s, wall_top, cx + hw - 8 * s, floor_y)
    floor = rect(W, H, cx - hw - 4 * s, floor_y - 4 * s, cx + hw + 4 * s, floor_y + 6 * s)
    # roof: boat-curved ridge, eaves straight-ish
    ridge = curve([(cx - hw - 34 * s, ridge_y - 40 * s), (cx - hw * 0.62, ridge_y + 4 * s), (cx + hw * 0.62, ridge_y + 4 * s), (cx + hw + 34 * s, ridge_y - 40 * s)], 40)
    eave = [(cx + hw + 22 * s, wall_top + 6 * s), (cx + hw * 0.5, wall_top + 12 * s), (cx - hw * 0.5, wall_top + 12 * s), (cx - hw - 22 * s, wall_top + 6 * s)]
    roof = shapes(W, H, [ridge + eave])
    gable = poly(W, H, [(cx + hw - 2 * s, wall_top + 2 * s), (cx + hw + 30 * s, ridge_y - 22 * s), (cx + hw + 30 * s, wall_top + 2 * s)])
    ladder = polyline_mask(W, H, [[(cx - 40 * s, floor_y + 4 * s), (cx - 60 * s, floor_y + 64 * s)], [(cx - 18 * s, floor_y + 4 * s), (cx - 38 * s, floor_y + 64 * s)]] + [[(cx - 40 * s - t * 20 * s, floor_y + 4 * s + t * 60 * s), (cx - 18 * s - t * 20 * s, floor_y + 4 * s + t * 60 * s)] for t in (0.25, 0.5, 0.75)], 3 * s)
    wood_c, wood_d = ("#6b3f26", "#3e2214") if dusk else ("#8a5a36", "#5a3820")
    art = GP(art, np.maximum.reduce([posts, ladder]), wood_d, seed=nx(), rough=0.7, pad=6)
    art = over(art, wood(wall, wood_c, wood_d, seed=nx(), angle=0.0, grain=7 * s + 2))
    planks = wall * hatch(W, H, 0.0, 14 * s, 0.06, nx(), 0.5)
    art = over(art, flat(planks, "#24130a", 0.55))
    wins = rect(W, H, 0, 0, 1, 1) * 0
    for dx in (-100, -55, 30, 75):
        wins = np.maximum(wins, rect(W, H, cx + dx * s, wall_top + 18 * s, cx + (dx + 24) * s, floor_y - 18 * s))
    lamp = "#f2b45a" if dusk else "#2b1a10"
    art = GP(art, wins, lamp, "#e08a3a" if dusk else lamp, seed=nx(), rough=0.5, pad=6)
    if dusk:
        art = over(art, glow(wins, "#ffb35a", radius=10, strength=0.25))
    art = GP(art, floor, wood_d, seed=nx(), rough=0.5, pad=6)
    # carved band under the eave (red/indigo painted), then roof
    band = rect(W, H, cx - hw + 8 * s, wall_top, cx + hw - 8 * s, wall_top + 10 * s)
    art = GP(art, band, SEPANG, seed=nx(), rough=0.4, pad=6)
    art = GP(art, gable, "#5a3420", seed=nx(), rough=0.5, pad=6)
    gl = polyline_mask(W, H, [[(cx + hw + 4 * s + k * 6 * s, wall_top), (cx + hw + 4 * s + k * 6 * s, wall_top - (k * 6 + 6) * s * 0.9)] for k in range(5)], 1.4 * s + 0.5)
    art = over(art, flat(gl * gable, KUNING, 0.8))
    rc, rd = ("#3a2a28", "#21181a") if dusk else ("#5a4030", "#3a2618")
    art = GP(art, roof, rc, rd, seed=nx(), rough=1.0, streak=1.2)
    sh = roof * hatch(W, H, 1.5708, 5 * s + 1, 0.12, nx(), 1.0)
    art = over(art, flat(sh, "#120c0c", 0.45))
    art = over(art, flat(polyline_mask(W, H, [ridge], 4 * s, cap=True), "#c98a4a" if dusk else "#7a4a26", 0.75))
    # silang horns at ridge ends
    for sgn in (-1, 1):
        ex, ey = ridge[0] if sgn < 0 else ridge[-1]
        art = over(art, flat(polyline_mask(W, H, [[(ex, ey), (ex + sgn * 14 * s, ey - 16 * s)], [(ex, ey), (ex - sgn * 4 * s, ey - 20 * s)]], 3 * s), "#21181a", 0.9))
    return art


if "river" in PARTS:
    W, H = 840, 560
    nx = Seq(72500); rng = random.Random(21)
    sky = painted_sky(W, H, [(0.0, "#2c3566"), (0.28, "#6a4a72"), (0.5, "#d9805a"), (0.6, "#f0b46a"), (0.62, "#e8a05a"), (1.0, "#3a2c40")], seed=nx(), streak=0.9)
    art = sky
    # clouds
    cl = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 14), rng, 2, 0.2) for x, y, rx, ry in [(160, 160, 150, 14), (600, 120, 190, 16), (420, 220, 120, 10), (740, 230, 100, 9)]])
    art = G(art, cl, "#e7a07a", "#9a6080", seed=nx(), density=0.5, edge=0.4, bloom=0.4, rough=8)
    # sun low over the far bank
    sun = circles(W, H, [(300, 318, 34)])
    art = over(art, glow(sun, "#ffd08a", radius=30, strength=0.4))
    art = GP(art, sun, "#ffe1a0", "#ffc878", seed=nx(), rough=0.6, pad=8)
    # far bank tree line (indigo silhouette)
    bank = hills(W, H, 336, 8, 5, 0.25)
    bank = bank * (np.mgrid[0:H, 0:W][0] < 352)
    trees = shapes(W, H, [deform(ellipse_pts(x, 330, rng.uniform(18, 40), rng.uniform(10, 22), 10), rng, 2, 0.18) for x in range(-10, W + 20, 28)])
    art = G(art, np.maximum(bank, trees * (np.mgrid[0:H, 0:W][0] < 352)), "#3a2f4e", "#2a2440", seed=nx(), density=0.9, edge=0.3, bloom=0.2, rough=4)
    # river
    river = rect(W, H, -10, 348, W + 10, H + 10)
    rv = painted_sky(W, H, [(0.0, "#6a4a72"), (0.6, "#e09a62"), (0.66, "#c07a5a"), (0.8, "#4a3a5a"), (1.0, "#262646")], seed=nx(), streak=1.6)
    rv = rv[::-1].copy()
    rv[..., 3] = river
    art = over(art, rv)
    refl = strokes(W, H, [([(300 + rng.gauss(0, 18) * (1 + (y - 350) / 80), y), (300 + rng.gauss(0, 18) * (1 + (y - 350) / 80) + rng.uniform(18, 50), y)], rng.uniform(1.5, 3)) for y in [rng.uniform(352, 520) for _ in range(70)]])
    art = over(art, flat(refl, "#ffd59a", 0.7))
    rip = strokes(W, H, [([(x, y), (x + rng.uniform(30, 80), y)], 1.2) for x, y in [(rng.uniform(0, W), rng.uniform(360, 550)) for _ in range(90)]])
    art = over(art, flat(rip, "#f6c58e", 0.25))
    # near bank (right) with the house
    nb = shapes(W, H, [[(470, 470), (560, 452), (700, 446), (W + 20, 440), (W + 20, H + 10), (520, H + 10)]])
    art = G(art, nb, "#3a2c34", "#2a2028", seed=nx(), density=0.95, edge=0.3, bloom=0.2, rough=5)
    art = kajang_leko(W, H, 628, 394, 0.8, nx, rng, art)
    # bank trees + palms (silhouettes)
    tr = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 12), rng, 2, 0.16) for x, y, rx, ry in [(470, 462, 26, 12), (826, 446, 40, 16)]])
    pm = np.maximum(palm_m(W, H, 800, 448, 230, -0.06, 5), palm_m(W, H, 476, 462, 150, -0.12, 8))
    art = G(art, np.maximum(tr, pm), "#2a2236", "#1c1828", seed=nx(), density=0.92, edge=0.3, bloom=0.1, rough=2)
    # perahu with a kajang canopy (no people)
    boat = shapes(W, H, [[(140, 452), (280, 450), (262, 466), (160, 467)]])
    art = GP(art, boat, "#2a1e24", seed=nx(), rough=0.6, pad=6)
    canopy = shapes(W, H, [curve([(176, 452), (210, 428), (244, 452)], 12) + [(176, 452)]])
    art = GP(art, canopy, "#5a3a30", "#3a2a30", seed=nx(), rough=0.5, pad=6)
    art = over(art, flat(polyline_mask(W, H, [[(150, 472), (268, 472)], [(170, 478), (250, 478)]], 1.6), "#f0b070", 0.45))
    preview(art, "ja-river")
    save(art, f"{OUT}/river.webp", max_w=780, quality=78)
    clear()
