"""Kelas Workshop — playful gouache for a pottery class at a made-up studio: workbench with a potter's wheel and a pot
being thrown, glazed pots, tool cup, sponge; a hanging apron; drying shelf; small pot trio; a fan of tools.
Run: python3 -I kelas-workshop.py [part ...]   parts: meja celemek rak guci alat"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o3_lib import *

OUT = outdir("kelas-workshop")
PARTS = sys.argv[1:] or ["meja", "celemek", "rak", "guci", "alat"]
CLAY, CLAY_D, CLAY_L = "#c46a3f", "#8f4325", "#e39468"
WET, WET_D = "#9a5a3c", "#6a3822"
SAGE, SAGE_D = "#7f9c78", "#55704f"
MUST, MUST_D = "#e2aa45", "#b47d22"
CREAM = "#f3e7d3"
INK = "#3a2a22"
WOOD, WOOD_D, WOOD_L = "#b9824f", "#7d5130", "#d7a46e"
DENIM, DENIM_D = "#4f6d8f", "#344b66"


def xg(W, H):
    return np.mgrid[0:H, 0:W][1].astype(np.float32)


def shade_lr(lay, mask, x0, x1, dark="#2a1a12", amt=0.32, lit="#fff4dc", lamt=0.18):
    """Light from the upper left: lighten the left third, darken toward the right edge of [x0, x1]."""
    W = lay.shape[1]; H = lay.shape[0]
    xx = xg(W, H)
    t = np.clip((xx - x0) / max(1, x1 - x0), 0, 1)
    lay = shade(lay, np.clip((t - 0.55) / 0.45, 0, 1) * mask, dark, amt)
    lay = lighten(lay, np.clip((0.38 - np.abs(t - 0.28)) / 0.38, 0, 1) * mask, lit, lamt)
    return lay


def outline(mask, w=2.2):
    m = np.clip(gaussian_filter(mask, w * 0.5) * 1.0, 0, 1)
    edge = np.clip((gaussian_filter(mask, w) > 0.04).astype(np.float32) - (mask > 0.5), 0, 1)
    return gaussian_filter(edge, 0.6)


def pot(art, W, H, cx, yb, prof, hgt, col, col2, nx, stripes=(), rim_col=None, line=True, drip=None):
    """prof: list of half-widths from foot (t=0) to lip (t=1). Gouache body + left light + inner lip + optional bands."""
    n = len(prof)
    L, R = [], []
    for i, w in enumerate(prof):
        y = yb - hgt * i / (n - 1)
        L.append((cx - w, y)); R.append((cx + w, y))
    poly = L + R[::-1]
    m = shape_mask(W, H, poly)
    wmax = max(prof)
    lay = gouache_paint(m, col, col2, seed=nx(), rough=1.2, streak=0.45)
    for (t0, t1, sc) in stripes:
        band = np.zeros((H, W), np.float32)
        band[int(yb - hgt * t1):int(yb - hgt * t0)] = 1
        lay = rgba(lay[..., :3] * (1 - band[..., None] * m[..., None]) + hexarr(sc) * band[..., None] * m[..., None], lay[..., 3])
    if drip:
        rng = random.Random(int(cx))
        dm = strokes(W, H, [([(x, yb - hgt * 0.98), (x + rng.uniform(-2, 2), yb - hgt * rng.uniform(0.6, 0.85))], rng.uniform(6, 10), (0.0, 0.6)) for x in np.linspace(cx - wmax * .8, cx + wmax * .8, 7)])
        top = np.zeros((H, W), np.float32); top[:int(yb - hgt * 0.84)] = 1
        dm = np.clip(np.maximum(dm, top), 0, 1) * m
        lay = rgba(lay[..., :3] * (1 - dm[..., None]) + hexarr(drip) * dm[..., None] * (0.92 + 0.08 * fbm(W, H, nx(), 10, 2)[..., None]), lay[..., 3])
    lay = shade_lr(lay, m, cx - wmax, cx + wmax)
    # inner lip opening
    lw = prof[-1]
    lip = ellipses(W, H, [(cx, yb - hgt, lw * 0.92, max(3, lw * 0.22), 0)])
    lay = over(lay, gouache_paint(lip, rim_col or "#3a2015", seed=nx(), rough=0.6))
    art = over(art, soft_shadow(ellipses(W, H, [(cx + 8, yb, wmax * 1.05, 7, 0)]), "#2a1a12", 4, 0.45, 0, 0))
    art = over(art, lay)
    if line:
        art = over(art, ink_paint(outline(m, 2.2) * 0.85, INK, seed=nx(), wet=0.1))
    return art, m


if "meja" in PARTS:
    W, H = 800, 560
    nx = Seq(60100)
    art = blank(W, H)
    # bench: top plank (front edge) + two legs + stretcher
    top = shapes(W, H, [[(30, 400), (770, 400), (770, 440), (30, 440)]], smooth=False)
    legs = shapes(W, H, [[(70, 440), (110, 440), (106, 556), (74, 556)], [(690, 440), (730, 440), (726, 556), (694, 556)], [(106, 500), (694, 500), (694, 520), (106, 520)]], smooth=False)
    wl = rgba(np.ones((H, W, 3), np.float32) * hexarr(WOOD), np.maximum(top, legs))
    for m_, c1, c2 in [(legs, WOOD_D, WOOD), (top, WOOD, WOOD_L)]:
        g = gouache_paint(m_, c1, c2, seed=nx(), rough=1.0, streak=1.4)
        grain = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (1.0, 30))
        grain = np.clip((grain - grain.mean()) / (grain.std() + 1e-6), -2, 2)
        g = shade(g, np.clip(grain * 0.5, 0, 1) * m_, WOOD_D, 0.35)
        art = over(art, g)
    lip = np.zeros((H, W), np.float32); lip[400:406, 30:770] = 1
    art = lighten(art, lip * top, "#f3d3a4", 0.5)
    art = shade(art, np.clip((xg(W, H) * 0 + np.mgrid[0:H, 0:W][0] - 440) / 20, 0, 1) * legs * (np.mgrid[0:H, 0:W][0] < 470), "#2a1a12", 0.4)
    art = over(art, ink_paint(outline(np.maximum(top, legs), 2.0) * 0.8, INK, seed=nx(), wet=0.1))
    clear()
    # potter's wheel: splash pan, wheel head, clay being thrown
    pan = ellipses(W, H, [(250, 384, 150, 34, 0)])
    pan_in = ellipses(W, H, [(250, 378, 128, 24, 0)])
    pan_wall = shapes(W, H, [[(100, 384), (100, 350), (400, 350), (400, 384)]], smooth=False) * 0 + np.clip(pan, 0, 1)
    art = over(art, soft_shadow(pan, "#2a1a12", 6, 0.4, 4, 6))
    lay = gouache_paint(pan, "#8aa0a8", "#6d8790", seed=nx(), rough=0.8)
    lay = over(lay, gouache_paint(pan_in, "#5d7680", "#4a6069", seed=nx(), rough=0.6))
    # slip splashes in the pan
    spl = circles(W, H, [(random.Random(i).uniform(140, 360), random.Random(i + 50).uniform(370, 392), random.Random(i + 99).uniform(2, 6)) for i in range(26)]) * pan_in
    lay = over(lay, gouache_paint(spl, WET, seed=nx(), rough=0.5))
    art = over(art, lay)
    head = ellipses(W, H, [(250, 362, 96, 16, 0)])
    hl = gouache_paint(head, "#c8ccc8", "#9aa3a2", seed=nx(), rough=0.5)
    art = over(art, hl)
    art = over(art, ink_paint(np.clip(outline(pan, 2) + outline(head, 1.6), 0, 1) * 0.8, INK, seed=nx(), wet=0.1))
    # clay cylinder on the wheel with throwing rings
    prof = [58, 56, 50, 44, 40, 38, 40, 44]
    art, cm = pot(art, W, H, 250, 362, prof, 150, WET, CLAY, nx, rim_col=WET_D)
    rings = strokes(W, H, [([(250 - 46 + k * 0, 362 - 22 - k * 18), (250 + 46, 362 - 22 - k * 18)], 2.0, (0.2, 0.2)) for k in range(6)]) * cm
    art = shade(art, rings, WET_D, 0.45)
    art = lighten(art, np.roll(rings, 2, 0) * cm, "#e7b08c", 0.35)
    clear()
    # finished glazed pots on the right
    art, _ = pot(art, W, H, 470, 400, [26, 34, 44, 50, 48, 40, 28, 20, 22], 120, SAGE, SAGE_D, nx, drip="#e8e1cc")
    art, _ = pot(art, W, H, 568, 400, [30, 34, 36, 37, 37, 36, 38], 82, MUST, MUST_D, nx, stripes=[(0.55, 0.66, "#f4ead2")])
    art, _ = pot(art, W, H, 660, 400, [22, 30, 40, 44, 40, 30, 18, 14, 16, 20], 168, CLAY, CLAY_D, nx, stripes=[(0.4, 0.46, CREAM), (0.52, 0.56, CREAM)])
    clear()
    # tool cup with brushes, loop tool and a needle; a sponge and a wooden rib on the bench
    handles = [((84, 300), (70, 214), "#b8864f"), ((102, 300), (112, 200), "#8f5a32"), ((94, 300), (92, 190), "#c9a06b")]
    hm = strokes(W, H, [([a, b], 7, None) for a, b, _ in handles])
    art = GP(art, hm, WOOD, WOOD_D, seed=nx(), rough=0.6)
    tips = np.maximum(shapes(W, H, [petal_pts(70, 214, 30, 8, -1.73, n=10), petal_pts(112, 200, 26, 7, -1.37, n=10)]), np.clip(ellipses(W, H, [(92, 180, 12, 14, 0)]) - ellipses(W, H, [(92, 180, 8, 10, 0)]), 0, 1))
    art = GP(art, tips, "#3a2a22", "#5a4032", seed=nx(), rough=0.5)
    cup = shapes(W, H, [[(60, 400), (128, 400), (124, 296), (64, 296)]], smooth=False)
    cl = gouache_paint(cup, DENIM, DENIM_D, seed=nx(), rough=0.8)
    cl = shade_lr(cl, cup, 60, 128)
    cl = rgba(cl[..., :3], cl[..., 3])
    band = np.zeros((H, W), np.float32); band[330:342] = 1
    cl = lighten(cl, band * cup, CREAM, 0.85)
    art = over(art, soft_shadow(cup, "#2a1a12", 4, 0.4, 6, 2))
    art = over(art, cl)
    art = over(art, ink_paint(outline(cup, 2) * 0.8, INK, seed=nx(), wet=0.1))
    sponge = shape_mask(W, H, deform(ellipse_pts(386, 392, 30, 14, 12), random.Random(4), 2, 0.06))
    sl = gouache_paint(sponge, MUST, "#d3982f", seed=nx(), rough=1.2)
    pores = circles(W, H, [(386 + random.Random(i).uniform(-22, 22), 392 + random.Random(i + 9).uniform(-8, 8), 2.2) for i in range(14)]) * sponge
    sl = shade(sl, pores, MUST_D, 0.6)
    art = over(art, sl)
    rib = shape_mask(W, H, deform([(720, 396), (742, 380), (770, 384), (766, 398), (740, 400)], random.Random(2), 1, 0.02))
    art = GP(art, rib, WOOD_L, WOOD, seed=nx(), rough=0.6)
    art = over(art, ink_paint(np.clip(outline(sponge, 1.6) + outline(rib, 1.6), 0, 1) * 0.8, INK, seed=nx(), wet=0.1))
    preview(art, "kw-meja", tone=CREAM)
    save(art, f"{OUT}/meja.webp", max_w=720, quality=80)
    clear()

if "celemek" in PARTS:
    W, H = 300, 440
    nx = Seq(60200)
    cx = 150
    art = blank(W, H)
    peg = circles(W, H, [(cx, 22, 13)])
    strap = strokes(W, H, [(curve([(cx - 40, 120), (cx - 30, 60), (cx, 26), (cx + 30, 60), (cx + 40, 120)], 40), 9, None)])
    body = shape_mask(W, H, deform([(cx - 44, 116), (cx + 44, 116), (cx + 50, 176), (cx + 96, 190), (cx + 104, 420), (cx - 104, 420), (cx - 96, 190), (cx - 50, 176)], random.Random(3), 2, 0.012), smooth=False)
    ties = strokes(W, H, [(curve([(cx - 96, 196), (cx - 122, 222), (cx - 116, 290)], 20), 7, (0.0, 0.3)), (curve([(cx + 96, 196), (cx + 126, 226), (cx + 118, 280)], 20), 7, (0.0, 0.3))])
    art = GP(art, np.maximum(strap, ties), DENIM_D, DENIM, seed=nx(), rough=0.6)
    lay = gouache_paint(body, DENIM, DENIM_D, seed=nx(), rough=1.2, streak=1.2)
    # folds: soft vertical darker bands
    xx = xg(W, H)
    fold = (0.5 + 0.5 * np.sin((xx - cx) / 22)) * np.clip((np.mgrid[0:H, 0:W][0] - 200) / 200, 0, 1)
    lay = shade(lay, fold * body, "#1f2f44", 0.25)
    pocket = shapes(W, H, [[(cx - 64, 270), (cx + 64, 270), (cx + 60, 350), (cx - 60, 350)]], smooth=False)
    pl = gouache_paint(pocket, MUST, MUST_D, seed=nx(), rough=0.8)
    stitch = strokes(W, H, [([(cx + x, 276), (cx + x + 6, 276)], 1.6, None) for x in range(-58, 56, 12)] + [([(cx, 272), (cx, 348)], 1.6, None)])
    pl = lighten(pl, stitch * pocket, CREAM, 0.8)
    lay = over(lay, soft_shadow(pocket, "#1f2f44", 2, 0.4, 2, 3))
    lay = over(lay, pl)
    # clay handprints and smudges
    sm = np.zeros((H, W), np.float32)
    for (x, y, r) in [(cx - 40, 220, 16), (cx + 50, 380, 20), (cx + 18, 210, 9)]:
        sm = np.maximum(sm, shape_mask(W, H, deform(ellipse_pts(x, y, r, r * .7, 10), random.Random(x), 2, 0.2)))
    lay = shade(lay, sm * body * 0.9, "#c46a3f", 0.75)
    art = over(art, soft_shadow(body, "#2a1a12", 6, 0.35, 6, 8))
    art = over(art, lay)
    # brush poking out of the pocket
    br = strokes(W, H, [([(cx + 30, 280), (cx + 42, 236)], 6, None)])
    art = GP(art, br, WOOD, WOOD_D, seed=nx(), rough=0.5)
    art = GP(art, shapes(W, H, [petal_pts(cx + 42, 236, 24, 6, -1.32, n=10)]), INK, seed=nx(), rough=0.4)
    art = over(art, soft_shadow(peg, "#2a1a12", 2, 0.5, 2, 3))
    art = GP(art, peg, WOOD_L, WOOD, seed=nx(), rough=0.4)
    art = over(art, ink_paint(np.clip(outline(body, 2) + outline(pocket, 1.6), 0, 1) * 0.8, INK, seed=nx(), wet=0.1))
    preview(art, "kw-celemek", tone=CREAM)
    save(art, f"{OUT}/celemek.webp", max_w=240, quality=82)
    clear()

if "rak" in PARTS:
    # drying shelf: two planks of unfired (pale) and freshly glazed pots
    W, H = 640, 480
    nx = Seq(60300)
    art = blank(W, H)
    for y in (220, 452):
        pl = shapes(W, H, [[(16, y), (624, y), (624, y + 22), (16, y + 22)]], smooth=False)
        g = gouache_paint(pl, WOOD, WOOD_D, seed=nx(), rough=0.8, streak=1.4)
        art = over(art, soft_shadow(pl, "#2a1a12", 5, 0.35, 0, 8))
        art = over(art, g)
        art = over(art, ink_paint(outline(pl, 1.8) * 0.8, INK, seed=nx(), wet=0.1))
    brk = shapes(W, H, [[(40, 242), (60, 242), (60, 300), (40, 262)], [(580, 242), (600, 242), (600, 262), (580, 300)]], smooth=False)
    art = GP(art, brk, WOOD_D, seed=nx(), rough=0.5)
    pale, pale_d = "#e3c7a6", "#c9a681"
    row1 = [(80, [24, 30, 34, 34, 30, 32], 70, pale, pale_d, None, ()), (170, [20, 30, 40, 44, 38, 24, 18, 22], 120, SAGE, SAGE_D, "#efe8d2", ()),
            (268, [34, 36, 37, 37, 38], 54, pale, pale_d, None, ()), (360, [26, 36, 44, 46, 40, 30, 26], 104, MUST, MUST_D, None, [(0.5, 0.6, CREAM)]),
            (458, [18, 24, 30, 32, 26, 14, 10, 14], 130, CLAY, CLAY_D, None, [(0.35, 0.42, CREAM)]), (552, [30, 34, 36, 36], 60, pale, pale_d, None, ())]
    for (x, prof, h, c1, c2, drip, st) in row1:
        art, _ = pot(art, W, H, x, 220, prof, h, c1, c2, nx, stripes=st, drip=drip)
        clear()
    row2 = [(96, [36, 44, 50, 50, 44, 40], 92, DENIM, DENIM_D, None, [(0.7, 0.78, CREAM)]), (210, [22, 26, 28, 30, 30], 70, pale, pale_d, None, ()),
            (310, [30, 40, 52, 58, 54, 42, 30, 26, 30], 176, CLAY, CLAY_D, None, [(0.55, 0.6, CREAM), (0.64, 0.68, CREAM)]), (420, [26, 30, 32, 32, 34], 64, SAGE, SAGE_D, "#efe8d2", ()),
            (520, [20, 30, 38, 40, 34, 22, 16, 20], 128, pale, pale_d, None, ())]
    for (x, prof, h, c1, c2, drip, st) in row2:
        art, _ = pot(art, W, H, x, 452, prof, h, c1, c2, nx, stripes=st, drip=drip)
        clear()
    preview(art, "kw-rak", tone=CREAM)
    save(art, f"{OUT}/rak.webp", max_w=600, quality=80)
    clear()

if "guci" in PARTS:
    W, H = 340, 160
    nx = Seq(60400)
    art = blank(W, H)
    art, _ = pot(art, W, H, 76, 150, [22, 28, 34, 36, 32, 30], 64, MUST, MUST_D, nx, stripes=[(0.6, 0.7, CREAM)])
    art, _ = pot(art, W, H, 170, 150, [18, 26, 34, 38, 34, 22, 14, 18], 120, CLAY, CLAY_D, nx, stripes=[(0.42, 0.48, CREAM)])
    art, _ = pot(art, W, H, 262, 150, [28, 36, 42, 42, 36, 30], 80, SAGE, SAGE_D, nx, drip="#efe8d2")
    preview(art, "kw-guci", tone=CREAM)
    save(art, f"{OUT}/guci.webp", max_w=240, quality=84)
    clear()

if "alat" in PARTS:
    # fan of tools: wooden knife, loop tool, needle tool, brush, kidney rib
    W, H = 340, 240
    nx = Seq(60500)
    art = blank(W, H)
    piv = (170, 226)
    items = [(-0.95, "knife"), (-0.45, "loop"), (0.05, "needle"), (0.5, "brush"), (0.95, "knife")]
    for ang, kind in items:
        a = -math.pi / 2 + ang
        tip = (piv[0] + math.cos(a) * 200, piv[1] + math.sin(a) * 200)
        mid = (piv[0] + math.cos(a) * 120, piv[1] + math.sin(a) * 120)
        handle = strokes(W, H, [([piv, mid], 12, (0.0, 0.0))])
        art = over(art, soft_shadow(handle, "#2a1a12", 2, 0.4, 3, 3))
        art = GP(art, handle, WOOD_L if kind != "brush" else "#c4553a", WOOD, seed=nx(), rough=0.5)
        if kind == "knife":
            bl = shapes(W, H, [petal_pts(mid[0], mid[1], 84, 9, a, n=12)])
            art = GP(art, bl, WOOD, WOOD_D, seed=nx(), rough=0.5)
        elif kind == "loop":
            ferr = strokes(W, H, [([mid, (piv[0] + math.cos(a) * 150, piv[1] + math.sin(a) * 150)], 8, None)])
            art = GP(art, ferr, "#a9aeb0", "#7f8588", seed=nx(), rough=0.4)
            lp = np.clip(ellipses(W, H, [(piv[0] + math.cos(a) * 176, piv[1] + math.sin(a) * 176, 16, 24, math.degrees(a) + 90)]) - ellipses(W, H, [(piv[0] + math.cos(a) * 176, piv[1] + math.sin(a) * 176, 12, 20, math.degrees(a) + 90)]), 0, 1)
            art = GP(art, lp, "#8f9598", seed=nx(), rough=0.3)
        elif kind == "needle":
            nd = strokes(W, H, [([mid, tip], 3.2, (0.0, 0.5))])
            art = GP(art, nd, "#8f9598", "#6f7578", seed=nx(), rough=0.3)
        else:
            fer = strokes(W, H, [([mid, (piv[0] + math.cos(a) * 140, piv[1] + math.sin(a) * 140)], 10, None)])
            art = GP(art, fer, "#c9ccc6", "#9aa09d", seed=nx(), rough=0.3)
            art = GP(art, shapes(W, H, [petal_pts(piv[0] + math.cos(a) * 138, piv[1] + math.sin(a) * 138, 60, 9, a, n=12)]), INK, seed=nx(), rough=0.4)
            art = GP(art, shapes(W, H, [petal_pts(piv[0] + math.cos(a) * 176, piv[1] + math.sin(a) * 176, 22, 5, a, n=10)]), CLAY, seed=nx(), rough=0.4)
    preview(art, "kw-alat", tone=CREAM)
    save(art, f"{OUT}/alat.webp", max_w=220, quality=84)
