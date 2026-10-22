"""Pesantren Teduh — a humble pesantren courtyard on a warm afternoon, in watercolour + a little gouache: a wooden
surau raised on stone umpak with a terracotta-tiled kampung (gable) roof, a serambi on teak posts where a bedug hangs on
its stand and a kentongan on a post, a gnarled kamboja (frangipani) tree in bloom, a swept sandy yard with broom marks
and dappled shade, a clay padasan for wudhu and sandals at the steps. No figures.
Run: python3 -I pesantren-teduh.py [part ...]  parts: surau kamboja bunga bedug dapple divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e3_lib import *

OUT = outdir("pesantren-teduh")
PARTS = sys.argv[1:] or ["surau", "kamboja", "bunga", "bedug", "dapple", "divider"]
WOOD, WOOD_D, WOOD_L = "#9a6a3e", "#5e3b20", "#c08f5c"
TILE, TILE_D = "#c0643a", "#8a3e22"
SAND, SAND_D = "#ead8b4", "#cdb588"
BARK, BARK_D = "#9a8a78", "#5e5148"
LEAF, LEAF_D = "#5f8a43", "#2f5128"
SUN = "#ffe6b0"
SHADOW = "#6a5a6e"


def kamboja_flower(art, W, H, x, y, r, rng, nx, rot=None, tilt=1.0):
    """Frangipani: five overlapping obovate petals in a pinwheel, creamy white with a yolk-yellow throat."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    polys = []
    for k in range(5):
        a = rot + k * math.tau / 5
        pts = petal_pts(x, y, r, r * 0.52, a, n=14, cup=0.35)
        pts = [(px, y + (py - y) * tilt) for px, py in pts]
        polys.append(deform(pts, rng, 1, 0.03))
    m = shapes(W, H, polys)
    art = G(art, np.roll(np.roll(m, 2, 0), 2, 1) * 0.8, "#9a8a7e", seed=nx(), density=0.3, edge=0.2, bloom=0, rough=1.2, feather=1.4, pad=8)
    art = GP(art, m, "#fffcf2", "#f6efdf", seed=nx(), rough=0.8, streak=0.4, pad=8)
    art = G(art, np.clip((m - gaussian_filter(m, 1.2)) * 3, 0, 1), "#a8968a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.4, pad=6)
    # petal overlaps: thin grey-violet shading lines along each petal's leading edge
    for k in range(5):
        a = rot + k * math.tau / 5
        e = [(x + math.cos(a + 0.18) * r * t, y + math.sin(a + 0.18) * r * t * tilt) for t in np.linspace(0.15, 0.75, 8)]
        art = G(art, strokes(W, H, [(e, max(1.0, r * 0.06))]) * m, "#b9ab9e", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.8, pad=6)
    throat = m * light_mask(H, W, x, y, r * 0.62)
    art = G(art, throat, "#f6cf4e", "#eeb53a", seed=nx(), density=0.85, edge=0.2, bloom=0.2, rough=1, feather=1.2, pad=6)
    return art


def kamboja_tree(art, W, H, x, by, h, rng, nx, flowers=True, lean=0.0):
    """Gnarled frangipani: short thick trunk forking into blunt branches, leaf rosettes and flower clusters at the tips."""
    items, tips = [], []

    def branch(x0, y0, ang, L, wd, depth):
        x1 = x0 + math.cos(ang) * L; y1 = y0 + math.sin(ang) * L
        mid = (x0 + math.cos(ang) * L * 0.5 + rng.gauss(0, L * 0.08), y0 + math.sin(ang) * L * 0.5 + rng.gauss(0, L * 0.05))
        items.append((curve([(x0, y0), mid, (x1, y1)], 16), wd, (0.0, 0.0)))
        if depth == 0:
            tips.append((x1, y1, ang)); return
        for sgn in (-1, 1):
            branch(x1, y1, ang + sgn * rng.uniform(0.35, 0.6), L * rng.uniform(0.62, 0.8), wd * 0.72, depth - 1)

    trunk_top = (x + lean * h * 0.3, by - h * 0.32)
    items.append((curve([(x, by), (x + rng.gauss(0, 6), by - h * 0.15), trunk_top], 16), h * 0.09, (0.0, 0.0)))
    branch(trunk_top[0], trunk_top[1], -math.pi / 2 - 0.55 + lean, h * 0.26, h * 0.065, 3)
    branch(trunk_top[0], trunk_top[1], -math.pi / 2 + 0.5 + lean, h * 0.24, h * 0.06, 3)
    m = strokes(W, H, items)
    art = G(art, m, BARK, BARK_D, seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=1.6, feather=0.8)
    art = G(art, m * light_mask(H, W, x + h * 0.4, by - h * 0.3, h * 0.6), "#3e342f", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=1.5)
    bands = m * hatch(W, H, 0.1, 9, 0.12, nx(), 2.0)
    art = G(art, bands, BARK_D, seed=nx(), density=0.3, edge=0, bloom=0, rough=1, feather=0.5)
    # leaf rosettes
    leaves = []
    for tx, ty, ang in tips:
        for k in range(7):
            a = ang + rng.uniform(-1.3, 1.3) - 0.2
            L = h * rng.uniform(0.11, 0.16)
            leaves.append(petal_pts(tx, ty, L, L * 0.26, a, n=18))
    lm = shapes(W, H, leaves)
    art = G(art, lm, LEAF, LEAF_D, seed=nx(), density=0.85, edge=0.6, bloom=0.35, rough=1.0, feather=1.0, gran=0.25)
    ribs = strokes(W, H, [([(tx, ty), ((p[0][0] + p[9][0]) / 2 * 0.3 + p[0][0] * 0.7, (p[0][1] + p[9][1]) / 2 * 0.3 + p[0][1] * 0.7) if False else p[len(p) // 2]], 1.2) for p in leaves])
    art = G(art, ribs * lm, "#2a4420", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = G(art, lm * light_mask(H, W, x - h * 0.3, by - h * 1.0, h * 0.8), "#b8c46a", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=2)
    if flowers:
        for tx, ty, ang in tips:
            for k in range(rng.randint(2, 4)):
                art = kamboja_flower(art, W, H, tx + rng.gauss(0, h * 0.03), ty - h * 0.03 + rng.gauss(0, h * 0.025), h * rng.uniform(0.028, 0.038), rng, nx, tilt=rng.uniform(0.7, 1.0))
            clear()
    return art, m, lm


if "surau" in PARTS:
    W, H = 860, 640
    nx = Seq(6100); rng = random.Random(31)
    art = blank(W, H)
    G0 = 520
    # distant greenery behind (bamboo/banana suggestion)
    bush = shapes(W, H, [deform(ellipse_pts(rng.uniform(260, 860), rng.uniform(330, 380), rng.uniform(40, 80), rng.uniform(30, 60), 12), rng, 2, 0.12) for _ in range(9)])
    art = G(art, bush, "#9db07a", "#6f8a55", seed=nx(), density=0.55, edge=0.4, bloom=0.5, rough=6)
    # ---- surau body (raised floor on umpak) ----
    cx = 530
    wall = rect(W, H, 330, 300, 730, 452)
    art = GP(art, wall, WOOD, WOOD_D, seed=nx(), rough=0.5, streak=1.0)
    planks = wall * hatch(W, H, 0.0, 14, 0.1, nx(), 0.6)
    art = over(art, flat(planks, "#3e2614", 0.55))
    # gable roof (kampung): front gable triangle with board + vents, tiles on both slopes
    gable = poly(W, H, [(cx, 150), (cx - 170, 300), (cx + 170, 300)])
    art = GP(art, gable, WOOD_L, WOOD, seed=nx(), rough=0.4, streak=1.0)
    vents = gable * hatch(W, H, 1.5708, 8, 0.28, nx(), 0.4) * (np.arange(H)[:, None] > 210) * (np.arange(H)[:, None] < 280)
    vents *= (np.abs(np.arange(W)[None, :] - cx) < 60)
    art = over(art, flat(vents, "#3e2614", 0.75))
    for side in (-1, 1):
        slope = poly(W, H, [(cx, 140), (cx + side * 26, 140), (cx + side * 236, 318), (cx + side * 200, 318)] if False else [(cx, 136), (cx + side * 230, 316), (cx + side * 230, 330), (cx + side * 196, 330), (cx, 160)])
        # tile courses
        tm = slope * (0.75 + 0.25 * hatch(W, H, side * 0.71 + (math.pi if side < 0 else 0), 9, 0.65, nx(), 0.4))
        art = GP(art, slope, TILE, TILE_D, seed=nx(), rough=0.6, streak=0.8)
        art = over(art, flat(slope * (1 - hatch(W, H, -side * 0.86, 10, 0.75, nx(), 0.6)), "#6e2a14", 0.45))
    art = over(art, flat(slope * 0, "#000000", 0))
    ridge = strokes(W, H, [([(cx - 2, 134), (cx + 2, 134)], 10)])
    art = GP(art, ridge, TILE_D, seed=nx(), rough=0.4)
    art = GP(art, circles(W, H, [(cx, 124, 8)]), "#d08a4a", "#8a4a22", seed=nx(), rough=0.4)
    art = over(art, flat(strokes(W, H, [([(cx, 116), (cx, 92)], 2.4)]), "#5e3b20", 0.9))
    # serambi: lean-to tiled roof, posts, raised floor, rail, steps
    sroof = poly(W, H, [(286, 318), (774, 318), (812, 368), (248, 368)])
    art = GP(art, sroof, TILE, TILE_D, seed=nx(), rough=0.6, streak=0.8)
    art = over(art, flat(sroof * (1 - hatch(W, H, 0.0, 9, 0.75, nx(), 0.5)), "#6e2a14", 0.45))
    art = over(art, flat(rect(W, H, 248, 366, 812, 374), WOOD_D, 0.95))
    shade = rect(W, H, 262, 374, 798, 452)
    art = G(art, shade, "#4a3428", "#3a2a24", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=2)
    door = rect(W, H, cx - 30, 384, cx + 30, 452)
    art = GP(art, door, "#6e4424", "#4a2c18", seed=nx(), rough=0.4)
    art = over(art, flat(outline(door, 2.5), "#2a1a10", 0.7))
    for wx in (400, 660):
        win = rect(W, H, wx - 26, 390, wx + 26, 430)
        art = GP(art, win, "#2a1a10", seed=nx(), rough=0.4)
        art = over(art, flat(win * hatch(W, H, 0.0, 6, 0.4, nx(), 0.3), WOOD, 0.9))
    posts = np.maximum.reduce([rect(W, H, px - 6, 372, px + 6, 470) for px in (270, 400, 660, 790)])
    art = over(art, wood(posts, WOOD, WOOD_D, seed=nx(), angle=1.5708, grain=5))
    floor = rect(W, H, 250, 452, 810, 470)
    art = over(art, wood(floor, WOOD_L, WOOD, seed=nx(), angle=0.0, grain=4))
    rail = np.maximum(rect(W, H, 276, 424, 486, 428), rect(W, H, 574, 424, 784, 428))
    bal = np.maximum.reduce([rect(W, H, bx - 1.5, 428, bx + 1.5, 452) for bx in list(range(282, 486, 12)) + list(range(580, 784, 12))])
    art = over(art, flat(np.maximum(rail, bal), WOOD_L, 0.95))
    umpak = np.maximum.reduce([rect(W, H, px - 10, 470, px + 10, G0 - 2) for px in (270, 400, 530, 660, 790)])
    art = GP(art, umpak, "#a49a8c", "#7a7064", seed=nx(), rough=0.5)
    under = rect(W, H, 250, 470, 810, G0 - 2)
    art = G(art, under * (1 - umpak), "#3a2a24", seed=nx(), density=0.55, edge=0.1, bloom=0.2, rough=2)
    steps = np.maximum(rect(W, H, cx - 36, 470, cx + 36, 488), rect(W, H, cx - 44, 488, cx + 44, 506))
    art = GP(art, steps, "#b6aa98", "#8f8474", seed=nx(), rough=0.5)
    # bedug on its stand in the serambi (left), kentongan on the right post
    bx, byy = 340, 412
    stand = np.maximum.reduce([rect(W, H, bx - 40, byy + 14, bx - 34, 452), rect(W, H, bx + 34, byy + 14, bx + 40, 452), rect(W, H, bx - 44, byy + 18, bx + 44, byy + 23)])
    art = over(art, wood(stand, WOOD_D, "#3a2010", seed=nx(), angle=1.5708))
    drum = shapes(W, H, [[(bx - 34, byy - 18), (bx + 34, byy - 18), (bx + 38, byy), (bx + 34, byy + 18), (bx - 34, byy + 18), (bx - 38, byy)]])
    art = GP(art, drum, "#a8482a", "#6e2a18", seed=nx(), rough=0.4, streak=0.8)
    art = over(art, flat(drum * light_mask(H, W, bx - 10, byy - 14, 40), SUN, 0.35))
    face = shapes(W, H, [ellipse_pts(bx + 36, byy, 7, 19, 14)])
    art = GP(art, face, "#e8d4a8", "#c8ab78", seed=nx(), rough=0.3)
    pegs = circles(W, H, [(bx + 30, byy + dy, 1.3) for dy in range(-14, 16, 5)] + [(bx - 30, byy + dy, 1.3) for dy in range(-14, 16, 5)])
    art = over(art, flat(pegs, "#f2dcb0", 0.9))
    ken = rect(W, H, 783, 388, 797, 436)
    art = GP(art, ken, "#b08a52", "#7a5a30", seed=nx(), rough=0.3)
    art = over(art, flat(rect(W, H, 789, 396, 791, 428), "#2a1a10", 0.9))
    # ---- sandy yard with broom (sapu lidi) arcs ----
    yard = shapes(W, H, [[(-20, G0 - 4), (W + 20, G0 - 4), (W + 20, H + 10), (-20, H + 10)]], smooth=False)
    art = G(art, yard, SAND, SAND_D, seed=nx(), density=0.9, edge=0.15, bloom=0.4, rough=4, gran=0.6)
    broom = []
    for k in range(70):
        ox, oy = rng.uniform(-20, W), rng.uniform(G0 + 10, H)
        rr = rng.uniform(30, 60); a0 = rng.uniform(-0.6, 0.2)
        broom.append(([(ox + math.cos(a0 + t) * rr, oy + math.sin(a0 + t) * rr * 0.25) for t in np.linspace(0, 1.1, 10)], 0.9, (0.2, 0.3)))
    art = G(art, strokes(W, H, broom), "#b49a6c", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.8, feather=0.5)
    # surau shadow on the sand
    sh = shapes(W, H, [[(250, G0 - 2), (810, G0 - 2), (850, G0 + 24), (300, G0 + 24)]], smooth=False)
    art = G(art, sh, SHADOW, seed=nx(), density=0.32, edge=0.2, bloom=0.3, rough=4, feather=3)
    # sandals at the steps
    for k, sx in enumerate([cx - 58, cx - 46, cx + 44, cx + 56, cx - 20]):
        sy = 518 + (k % 2) * 6
        sm = shapes(W, H, [ellipse_pts(sx, sy, 4.5, 2.2, 10, 0.2)])
        art = GP(art, sm, rng.choice(["#3f5f7a", "#2e2e2e", "#7a3a2a", "#4a6a3a"]), seed=nx(), rough=0.2, pad=6)
    # padasan (clay wudhu jar) on a little stand, right
    px, py = 830, 520
    jar = shapes(W, H, [ellipse_pts(px, py - 34, 24, 26, 18)])
    art = GP(art, jar, "#b8653a", "#7e3a20", seed=nx(), rough=0.4, streak=0.6)
    art = over(art, flat(jar * light_mask(H, W, px - 10, py - 46, 26), SUN, 0.45))
    art = GP(art, rect(W, H, px - 18, py - 10, px + 18, py), "#8a7a6a", seed=nx(), rough=0.3)
    art = over(art, flat(strokes(W, H, [([(px - 22, py - 30), (px - 32, py - 26)], 3)]), "#7e3a20", 0.9))
    # ---- kamboja tree, left, overhanging ----
    art, trunk, crown = kamboja_tree(art, W, H, 150, G0 + 14, 470, rng, nx, lean=0.1)
    clear()
    # warm light from the left on the gable + sun patches on the yard
    art = over(art, flat((gable + wall * 0.5) * light_mask(H, W, 380, 200, 320), SUN, 0.22))
    preview(art, "pt-surau", "#fbf2e2")
    save(art, f"{OUT}/surau.webp", max_w=780, quality=78)
    clear()

if "kamboja" in PARTS:
    W, H = 520, 420
    nx = Seq(6200); rng = random.Random(32)
    art = blank(W, H)
    br = strokes(W, H, [(curve([(10, 400), (120, 330), (220, 250), (330, 200)], 30), 18, (0.0, 0.0)), (curve([(220, 250), (300, 300), (400, 290)], 20), 11, (0.0, 0.0))])
    art = G(art, br, BARK, BARK_D, seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=1.5)
    art = G(art, br * hatch(W, H, 0.6, 8, 0.12, nx(), 2), BARK_D, seed=nx(), density=0.3, edge=0, bloom=0, rough=1)
    for tx, ty, ang in [(330, 200, -0.6), (400, 290, 0.1)]:
        leaves = [petal_pts(tx, ty, rng.uniform(90, 130), 24, ang + rng.uniform(-1.4, 1.2), n=18) for _ in range(7)]
        lm = shapes(W, H, leaves)
        art = G(art, lm, LEAF, LEAF_D, seed=nx(), density=0.85, edge=0.6, bloom=0.35, rough=1.0, feather=1.0, gran=0.25)
        veins = strokes(W, H, [([(tx, ty), (tx + (p[len(p) // 2][0] - tx), ty + (p[len(p) // 2][1] - ty))], 1.4) for p in leaves])
        art = G(art, veins * lm, "#2f4a24", seed=nx(), density=0.3, edge=0, bloom=0, rough=0.6, feather=0.5)
    for (x, y, r) in [(330, 180, 30), (300, 214, 26), (362, 214, 24), (400, 270, 26), (430, 300, 22), (366, 168, 20)]:
        art = kamboja_flower(art, W, H, x, y, r, rng, nx, tilt=rng.uniform(0.75, 1.0))
    clear()
    preview(art, "pt-kamboja", "#fbf2e2")
    save_full(art, f"{OUT}/kamboja.webp", size=(390, 315), quality=80)
    clear()

if "bunga" in PARTS:
    W, H = 160, 160
    nx = Seq(6300); rng = random.Random(33)
    art = kamboja_flower(blank(W, H), W, H, 80, 80, 66, rng, nx, rot=0.3)
    preview(art, "pt-bunga", "#e9d6b0")
    save_full(art, f"{OUT}/bunga.webp", size=(72, 72), quality=84)
    clear()

if "bedug" in PARTS:
    W, H = 460, 360
    nx = Seq(6400); rng = random.Random(34)
    art = blank(W, H)
    cx, cy = 230, 160
    legs = np.maximum.reduce([strokes(W, H, [([(cx - 120, cy + 20), (cx - 140, 340)], 16, None), ([(cx + 120, cy + 20), (cx + 140, 340)], 16, None)]),
                              rect(W, H, cx - 150, cy + 10, cx + 150, cy + 26), rect(W, H, cx - 136, 300, cx + 136, 310)])
    art = over(art, wood(legs, WOOD, WOOD_D, seed=nx(), angle=1.2, grain=5))
    drum = shapes(W, H, [[(cx - 130, cy - 70), (cx + 130, cy - 70), (cx + 146, cy), (cx + 130, cy + 70), (cx - 130, cy + 70), (cx - 146, cy)]])
    art = GP(art, drum, "#a8482a", "#7a321c", seed=nx(), rough=0.6, streak=0.8)
    art = G(art, drum, "#b0532e", "#7a321c", seed=nx(), density=0.5, edge=0.5, bloom=0.3, rough=2, gran=0.3)
    art = G(art, drum * hatch(W, H, 1.5708, 22, 0.08, nx(), 1.5), "#5a2414", seed=nx(), density=0.4, edge=0, bloom=0, rough=1)
    art = G(art, drum * light_mask(H, W, cx - 40, cy - 60, 150), SUN, seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
    art = G(art, drum * (1 - light_mask(H, W, cx - 40, cy - 60, 220)), "#3a160c", seed=nx(), density=0.3, edge=0.1, bloom=0.3, rough=2)
    face = shapes(W, H, [ellipse_pts(cx + 138, cy, 22, 70, 20)])
    art = GP(art, face, "#efdcb2", "#cdb080", seed=nx(), rough=0.4, streak=0.5)
    art = G(art, outline(face, 3), "#5a2a14", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.6, feather=0.5)
    pegs = circles(W, H, [(cx + 124 + 6 * math.cos(t), cy + 64 * math.sin(t), 3) for t in np.linspace(-1.4, 1.4, 12)] + [(cx - 128, cy + 64 * math.sin(t), 3) for t in np.linspace(-1.3, 1.3, 11)])
    art = GP(art, pegs, "#f2dcb0", "#c8a870", seed=nx(), rough=0.2, pad=6)
    preview(art, "pt-bedug", "#fbf2e2")
    save_full(art, f"{OUT}/bedug.webp", size=(276, 216), quality=82)
    clear()

if "dapple" in PARTS:
    W, H = 600, 600
    nx = Seq(6500); rng = random.Random(35)
    blobs = []
    for _ in range(46):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        for k in range(rng.randint(3, 6)):
            blobs.append(deform(petal_pts(x, y, rng.uniform(40, 90), rng.uniform(12, 22), rng.uniform(0, 6.3), n=10), rng, 2, 0.1))
    m = shapes(W, H, blobs)
    m = gaussian_filter(m, 5)
    art = np.concatenate([np.ones((H, W, 3), np.float32) * col_arr("#4a3a52"), (np.clip(m, 0, 1) * 0.18)[..., None]], -1)
    art = np.ascontiguousarray(tileable(art))
    save_full(art, f"{OUT}/dapple.webp", size=(300, 300), quality=70)
    clear()

if "divider" in PARTS:
    W, H = 640, 100
    nx = Seq(6600); rng = random.Random(36)
    cy = 50
    fade = np.clip(1 - np.abs(np.linspace(-1, 1, W)) ** 2.2, 0, 1)[None, :]
    ln = strokes(W, H, [(curve([(40, cy + 2), (180, cy - 2), (282, cy)], 30), 2.0, (0.0, 0.0)), (curve([(358, cy), (460, cy + 3), (600, cy - 1)], 30), 2.0, (0.0, 0.0))]) * fade
    art = G(blank(W, H), ln, "#8a6a4a", seed=nx(), density=0.75, edge=0.2, bloom=0, rough=0.8, feather=0.5)
    for (x, y, L, a) in [(300, cy + 4, 46, 2.7), (340, cy + 4, 46, 0.45)]:
        art = G(art, shapes(W, H, [deform(petal_pts(x, y, L, 12, a, n=10), rng, 1, 0.05)]), LEAF, LEAF_D, seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=1.5)
    art = kamboja_flower(art, W, H, 320, cy - 4, 22, rng, nx, rot=0.2)
    preview(art, "pt-divider", "#fbf2e2")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()
