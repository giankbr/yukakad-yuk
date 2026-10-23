"""Mozaik Umayyah — gold-ground glass mosaic in the spirit of early Umayyad wall mosaics (original composition):
a broad fruit tree and tall cypresses, riverside pavilions with arcades and a domed kiosk, a river with pearl ripples,
all on a ground of gold tesserae laid in rows that follow the outlines. No figures, no calligraphy.
Run: python3 -I mozaik-umayyah.py [part ...]   parts: scene tree frieze"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l4_lib import *

OUT = outdir("mozaik-umayyah")
PARTS = sys.argv[1:] or ["scene", "tree", "frieze"]
GRN_D, GRN, GRN_M, GRN_L, GRN_Y = "#173a2a", "#24523a", "#3d6f3f", "#6f9645", "#a7b956"
TEAL_D, TEAL, TEAL_L = "#1f4f57", "#2f6f73", "#6fa9a2"
PEARL, PEARL_D = "#ece6d0", "#cfc5a6"
STONE, STONE_D = "#d9c9a0", "#b39a68"
ROOF, ROOF_D = "#9c4d2c", "#6e3220"
DARK = "#2a2418"


class Design:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.rgb = np.zeros((H, W, 3), np.float32)
        self.gold = np.ones((H, W), np.float32)
        self.objs = np.zeros((H, W), np.float32)
        self.cont = []

    def fill(self, mask, col, obj=True):
        sel = mask > .5
        self.rgb[sel] = np.array(hex_rgb(col), np.float32)
        self.gold[sel] = 0
        if obj:
            self.objs = np.maximum(self.objs, mask)


def tree(D, cx, base, top, crown_r, rng, fruit=True):
    """Broad tree: trunk + clustered round lobes, each lobe dark -> mid -> light (light from top-left)."""
    W, H = D.W, D.H
    tw = max(10, crown_r * .1)
    trunk = shapes(W, H, [[(cx - tw * 1.5, base), (cx - tw * 1.2, base - 14), (cx - tw * .6, top + crown_r), (cx + tw * .6, top + crown_r), (cx + tw * 1.2, base - 14), (cx + tw * 1.6, base)]], smooth=False)
    trunk = np.maximum(trunk, strokes(W, H, [([(cx, top + crown_r * 1.5), (cx - crown_r * .45, top + crown_r * 1.05)], tw * .9, None), ([(cx, top + crown_r * 1.35), (cx + crown_r * .5, top + crown_r * .95)], tw * .8, None)]))
    D.fill(trunk, "#6b4a2c")
    D.fill(shapes(W, H, [[(cx + tw * .1, base), (cx + tw * .1, top + crown_r), (cx + tw * .6, top + crown_r), (cx + tw * 1.6, base)]], smooth=False) * trunk, "#4a3220")
    lobes = []
    for k in range(13):
        a = rng.uniform(0, math.tau); d = crown_r * rng.uniform(.15, .62)
        lobes.append((cx + math.cos(a) * d * 1.1, top + crown_r + math.sin(a) * d * .9 - 6, crown_r * rng.uniform(.34, .46)))
    lobes.sort(key=lambda l: l[1])
    crown = circles(W, H, [(x, y, r) for x, y, r in lobes])
    D.fill(crown, GRN_D)
    for x, y, r in lobes:
        D.fill(circles(W, H, [(x - r * .08, y - r * .1, r * .82)]), GRN)
        D.fill(circles(W, H, [(x - r * .2, y - r * .24, r * .56)]), GRN_M)
        D.fill(circles(W, H, [(x - r * .3, y - r * .36, r * .28)]), GRN_L)
    if fruit:
        D.fill(circles(W, H, [(x + r * .3, y + r * .25, 5.5) for x, y, r in lobes[::2]]), "#e3b24a")
    D.cont += andamento(crown, DARK, 10, (0,), .9)
    D.cont += andamento(trunk, DARK, 10, (0,), .8)
    return np.maximum(crown, trunk)


def cypress(D, cx, base, h, w):
    W, H = D.W, D.H
    body = shapes(W, H, [[(cx, base - h), (cx + w * .55, base - h * .55), (cx + w * .5, base - h * .12), (cx + 6, base - 6), (cx - 6, base - 6), (cx - w * .5, base - h * .12), (cx - w * .55, base - h * .55)]])
    D.fill(body, GRN_D)
    mid = shapes(W, H, [[(cx - 2, base - h * .95), (cx - w * .1, base - h * .5), (cx - w * .35, base - h * .2), (cx - w * .42, base - h * .5)]])
    D.fill(mid, GRN_M)
    hi = shapes(W, H, [[(cx - 3, base - h * .85), (cx - w * .25, base - h * .55), (cx - w * .3, base - h * .35)]])
    D.fill(hi, GRN_Y)
    trunk = shapes(W, H, [[(cx - 5, base - 8), (cx + 5, base - 8), (cx + 6, base + 10), (cx - 6, base + 10)]], smooth=False)
    D.fill(trunk, "#5a3e26")
    D.cont += andamento(body, DARK, 10, (0,), .9)
    return np.maximum(body, trunk)


def pavilion(D, x0, x1, base, h, rng):
    """Two-storey riverside pavilion: arcade below, windows above, red pitched roof, slim columns."""
    W, H = D.W, D.H
    wall = shapes(W, H, [[(x0, base - h), (x1, base - h), (x1, base), (x0, base)]], smooth=False)
    D.fill(wall, STONE)
    D.fill(shapes(W, H, [[(x1 - (x1 - x0) * .28, base - h), (x1, base - h), (x1, base), (x1 - (x1 - x0) * .28, base)]], smooth=False), STONE_D)
    n = 4
    bw = (x1 - x0) / n
    arches = []
    for i in range(n):
        ax0, ax1 = x0 + bw * i + bw * .24, x0 + bw * (i + 1) - bw * .24
        top = base - h * .48
        arches.append([(ax0, base), (ax0, top)] + arc_pts((ax0 + ax1) / 2, top, (ax1 - ax0) / 2, math.pi, math.tau, 10) + [(ax1, base)])
    am = shapes(W, H, arches, smooth=False)
    D.fill(am, "#33465e")
    D.fill(shapes(W, H, [[(p[0] + 3, p[1] + 6) for p in a] for a in arches], smooth=False) * am, "#4e6585")
    wins = shapes(W, H, [[(x0 + bw * i + bw * .32, base - h * .86), (x0 + bw * i + bw * .68, base - h * .86), (x0 + bw * i + bw * .68, base - h * .64), (x0 + bw * i + bw * .32, base - h * .64)] for i in range(n)], smooth=False)
    D.fill(wins, "#33465e")
    band = shapes(W, H, [[(x0 - 4, base - h * .6), (x1 + 4, base - h * .6), (x1 + 4, base - h * .55), (x0 - 4, base - h * .55)]], smooth=False)
    D.fill(band, PEARL)
    roof = shapes(W, H, [[(x0 - 12, base - h), ((x0 + x1) / 2, base - h - h * .36), (x1 + 12, base - h)]], smooth=False)
    D.fill(roof, ROOF)
    D.fill(shapes(W, H, [[((x0 + x1) / 2, base - h - h * .36), (x1 + 12, base - h), ((x0 + x1) / 2 + 4, base - h)]], smooth=False), ROOF_D)
    allm = np.maximum.reduce([wall, roof, band])
    D.cont += andamento(allm, DARK, 10, (0,), .8)
    return allm


def kiosk(D, cx, base, w, h):
    """Domed kiosk on columns (tholos-like)."""
    W, H = D.W, D.H
    plinth = shapes(W, H, [[(cx - w * .6, base - 14), (cx + w * .6, base - 14), (cx + w * .6, base), (cx - w * .6, base)]], smooth=False)
    D.fill(plinth, STONE_D)
    cols = shapes(W, H, [[(cx + dx - 5, base - 14), (cx + dx - 5, base - h), (cx + dx + 5, base - h), (cx + dx + 5, base - 14)] for dx in (-w * .48, -w * .16, w * .16, w * .48)], smooth=False)
    D.fill(cols, PEARL)
    inside = shapes(W, H, [[(cx - w * .43, base - 14), (cx - w * .43, base - h), (cx + w * .43, base - h), (cx + w * .43, base - 14)]], smooth=False) * (1 - cols)
    D.fill(inside, "#3c5a63")
    ent = shapes(W, H, [[(cx - w * .62, base - h - 14), (cx + w * .62, base - h - 14), (cx + w * .62, base - h), (cx - w * .62, base - h)]], smooth=False)
    D.fill(ent, STONE)
    dome = shapes(W, H, [[(cx - w * .5, base - h - 14)] + arc_pts(cx, base - h - 14, w * .5, math.pi, math.tau, 16, squash=1.15) + [(cx + w * .5, base - h - 14)]])
    D.fill(dome, TEAL)
    D.fill(shapes(W, H, [arc_pts(cx - w * .14, base - h - 14 - w * .26, w * .2, 0, math.tau, 12)]) * dome, TEAL_L)
    fin = shapes(W, H, [[(cx - 3, base - h - 14 - w * .56), (cx + 3, base - h - 14 - w * .56), (cx + 3, base - h - 14 - w * .76), (cx - 3, base - h - 14 - w * .76)]], smooth=False)
    D.fill(fin, "#e3b24a")
    allm = np.maximum.reduce([plinth, cols, inside, ent, dome])
    D.cont += andamento(allm, DARK, 10, (0,), .8)
    return allm


def river(D, y0, y1, x0=0, x1=None):
    W, H = D.W, D.H
    x1 = W if x1 is None else x1
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    top = y0 + 6 * np.sin(xx / 60)
    rv = ((yy >= top) & (yy <= y1) & (xx >= x0) & (xx <= x1)).astype(np.float32)
    D.fill(rv, TEAL)
    for k, yk in enumerate(np.linspace(y0 + 14, y1 - 10, 4)):
        rip = (np.abs(yy - (yk + 7 * np.sin(xx / 34 + k * 1.7))) < 4.5).astype(np.float32) * rv
        D.fill(rip, [TEAL_L, PEARL, TEAL_L, TEAL_D][k])
    D.cont += [([(x, float(y0 + 6 * math.sin(x / 60)) + 5) for x in range(int(x0), int(x1), 4)], TEAL_D, .9)]
    return rv


def render(D, name, cell, alpha=None, max_w=None, seed=1, rgb=False, size=None, q=80):
    D.cont += andamento(np.clip(D.objs, 0, 1), "gold", cell, (-1, -2), 1.0)
    art = mosaic(D.rgb, D.W, D.H, cell=cell, seed=seed, gold=D.gold, contours=D.cont, alpha=alpha, grout="#5e4c2e", gap=1.5)
    if rgb:
        save_rgb(art, f"{OUT}/{name}.webp", size=size, quality=q)
    else:
        save(art, f"{OUT}/{name}.webp", max_w=max_w, quality=82)
    prev(art, f"mu-{name}", bg="#123326")
    clear()
    return art


# ---------------------------------------------------------------- scene (cover/hero panel, 720x900 -> 600x750)
if "scene" in PARTS:
    W, H = 900, 1125
    GL = 860
    rng = random.Random(501)
    D = Design(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    bank = (yy >= GL + 4 * np.sin(xx / 50)).astype(np.float32)
    D.fill(bank, GRN, obj=False)
    D.fill(((yy >= GL + 14) & (yy < GL + 30)).astype(np.float32) * bank, GRN_M, obj=False)
    river(D, 918, 1040)
    D.fill(((yy > 1040)).astype(np.float32), GRN_D, obj=False)
    D.fill(circles(W, H, [(x + 30, 1080, 6) for x in range(0, W, 60)]), PEARL, obj=False)
    cypress(D, 338, GL, 470, 66)
    tree(D, 570, GL, 150, 214, rng)
    crag = shapes(W, H, [[(20, 640), (60, 560), (120, 548), (200, 556), (262, 590), (276, 640), (240, 650), (60, 652)]])
    D.fill(crag, STONE_D)
    D.fill(shapes(W, H, [[(40, 600), (70, 566), (130, 556), (150, 580), (100, 600)]]), PEARL)
    D.fill(shapes(W, H, [[(180, 600), (250, 596), (266, 636), (200, 646)]]), "#8f7650")
    D.cont += andamento(crag, DARK, 10, (0,), .8)
    pavilion(D, 70, 230, 560, 140, rng)
    cypress(D, 250, 560, 190, 34)
    pavilion(D, 46, 290, GL, 220, rng)
    kiosk(D, 806, GL, 150, 160)
    for x in (318, 650, 890):
        D.fill(circles(W, H, [(x, GL - 10, 24), (x + 20, GL - 2, 17), (x - 20, GL - 2, 17)]), GRN_D)
        D.fill(circles(W, H, [(x - 5, GL - 18, 12)]), GRN_M)
    render(D, "scene", 11, rgb=True, size=(680, 850), seed=511, q=70)

# ---------------------------------------------------------------- tree (transparent ornament, 300x380)
if "tree" in PARTS:
    W, H = 300, 380
    rng = random.Random(521)
    D = Design(W, H)
    t = tree(D, 150, 330, 40, 118, rng)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ground = shapes(W, H, [[(40, 330), (260, 330), (250, 352), (50, 352)]], smooth=False)
    D.fill(ground, GRN)
    D.fill(shapes(W, H, [[(60, 336), (240, 336), (240, 342), (60, 342)]], smooth=False), GRN_Y)
    shape = np.maximum(t, ground)
    alpha = np.clip(gaussian_filter((shape > .5).astype(np.float32), 1) + 0, 0, 1)
    # a gold halo of two tessera rows around the tree
    from scipy.ndimage import distance_transform_edt
    halo = (distance_transform_edt(shape < .5) <= 22).astype(np.float32)
    render(D, "tree", 9, alpha=halo, max_w=240, seed=531)

# ---------------------------------------------------------------- frieze (horizontal vine-scroll band, 900x110 -> 720x88)
if "frieze" in PARTS:
    W, H = 900, 150
    D = Design(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    CY, P, A = 75, 150, 26
    edge = ((yy < 14) | (yy > H - 14)).astype(np.float32)
    D.fill(edge, GRN_D, obj=False)
    D.fill(((np.abs(yy - 18) < 3) | (np.abs(yy - (H - 18)) < 3)).astype(np.float32), PEARL, obj=False)
    yc = lambda x: CY + A * math.sin(x / P * math.tau)
    stem = strokes(W, H, [([(x, yc(x)) for x in range(-10, W + 12, 6)], 14, None)])
    D.fill(stem, "#5a3e26")
    leaves = []; ros = []
    for i in range(7):
        for half in (0, 1):
            x = P * i + P * (.25 if half == 0 else .75)
            y = yc(x)
            side = -1 if half == 0 else 1          # leaf curls into the hollow of the wave
            leaves.append(petal_pts(x, y, 46, 15, side * math.pi / 2 + .7, n=14))
            leaves.append(petal_pts(x, y, 38, 12, side * math.pi / 2 - .9, n=14))
            ros.append((x + P * .25, CY - side * A * 1.25, 14))
    lm = shapes(W, H, leaves)
    D.fill(lm, GRN_M)
    D.fill(shapes(W, H, [[(p[0] - 3, p[1] - 3) for p in L[: len(L) // 2 + 1]] for L in leaves]) * lm, GRN_Y)
    rm = circles(W, H, ros)
    D.fill(rm, PEARL)
    D.fill(circles(W, H, [(x, y, 6) for x, y, _ in ros]), "#c14f3a")
    D.cont += andamento(lm, GRN_D, 9, (0,), .8)
    render(D, "frieze", 9, rgb=True, size=(720, 120), seed=541)
