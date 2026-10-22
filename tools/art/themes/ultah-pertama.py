"""Ultah Pertama — a first birthday in a calm nursery (soft gouache + watercolour, beige/sage/blush): a plush caramel teddy
with a sage bow, three blank wooden alphabet blocks (the letters are typeset over them in HTML so they spell the child's
initial and age), a tiny smash cake with one candle, a felt-ball garland and a eucalyptus sprig.
Run: python3 -I ultah-pertama.py [part ...]   parts: teddy blocks cake garland sprig
Assets -> public/themes/art/ultah-pertama/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d6_lib import *
import _d6_lib
from _c6_lib import felt
import _p1_lib, _j1_lib
_p1_lib.PREV = _j1_lib.PREV = _d6_lib.PREV

OUT = outdir("ultah-pertama")
PARTS = sys.argv[1:] or ["teddy", "blocks", "cake", "garland", "sprig"]
INK = "#5a4536"
FUR, FUR2, FURD, FURL = "#c79766", "#cfa072", "#9c6c44", "#e2bf92"
MUZ = "#efdcc0"
SAGE, SAGE2, SAGED, SAGEL = "#9fb29a", "#a9bba3", "#6f8569", "#c9d6c3"
BLUSH, BLUSH2, BLUSHD = "#e7bcab", "#edc8b9", "#c48f7d"
SAND, SAND2, SANDD = "#e6cf98", "#ecd9a9", "#b99a5c"
WOOD, WOOD2, WOODD, WOODL = "#e3c79c", "#ead3ae", "#b48d5f", "#f5e6cc"
CREAM = "#fbf6ee"
BG = "#f3ebe0"


def fuzz_edge(m, seed, amt=2.2):
    """Plush outline: displace the mask with fine noise so the silhouette reads as short fur."""
    d = displace(m, seed, amt, 3)
    return np.clip((gaussian_filter(d, 0.6) - 0.25) * 2, 0, 1)


if "teddy" in PARTS:
    W, H = 480, 540
    nx = Seq(71100); rng = random.Random(711)
    art = blank(W, H)
    art = soft_ground(art, W, H, 240, 506, 170, 18, "#8a6a4a", nx, 0.3)
    ears = fuzz_edge(circles(W, H, [(146, 104, 42), (334, 104, 42)]), nx())
    head = fuzz_edge(shapes(W, H, [deform(ellipse_pts(240, 190, 112, 98, 18, 0), rng, 1, 0.01)]), nx())
    body = fuzz_edge(shapes(W, H, [deform(ellipse_pts(240, 380, 118, 116, 18, 0), rng, 1, 0.01)]), nx())
    armL = fuzz_edge(ellipses(W, H, [(132, 356, 40, 74, 28)]), nx())
    armR = fuzz_edge(ellipses(W, H, [(348, 356, 40, 74, -28)]), nx())
    legL = fuzz_edge(ellipses(W, H, [(156, 464, 66, 44, -10)]), nx())
    legR = fuzz_edge(ellipses(W, H, [(324, 464, 66, 44, 10)]), nx())
    for m in (ears, body):
        art = body_paint(art, m, FUR, FUR2, FURD, FURL, nx, ldir=(-12, -14), blur=14, line=None, light_amt=0.45)
    inner = circles(W, H, [(150, 108, 22), (330, 108, 22)])
    art = GP(art, inner, BLUSH, BLUSH2, seed=nx(), rough=0.8, pad=6)
    art = tint(art, side_light(inner, 4, 4, 5), BLUSHD, 0.4, seed=nx())
    belly = shapes(W, H, [deform(ellipse_pts(240, 398, 70, 74, 16, 0), rng, 1, 0.02)])
    art = GP(art, belly, MUZ, "#f4e5cd", seed=nx(), rough=1.2, streak=0.6)
    art = tint(art, side_light(belly, -8, -8, 8), "#d6b98f", 0.35, seed=nx())
    art = body_paint(art, head, FUR, FUR2, FURD, FURL, nx, ldir=(-14, -16), blur=16, light_amt=0.45)
    for m in (armL, armR):
        art = body_paint(art, m, FUR, FUR2, FURD, FURL, nx, ldir=(-10, -12), blur=10, light_amt=0.4)
    for m in (legL, legR):
        art = body_paint(art, m, FUR, FUR2, FURD, FURL, nx, ldir=(-10, -12), blur=10, light_amt=0.4)
    pads = ellipses(W, H, [(126, 470, 28, 30, -14), (354, 470, 28, 30, 14)])
    art = GP(art, pads, MUZ, "#f4e5cd", seed=nx(), rough=0.8, pad=6)
    toes = circles(W, H, [(x + dx, 446, 6) for x, dxs in ((126, (-12, 0, 12)), (354, (-12, 0, 12))) for dx in dxs])
    art = GP(art, toes, BLUSH, BLUSH2, seed=nx(), rough=0.5, pad=6)
    # stitched seam down the tummy + on paws
    seam = strokes(W, H, [([(240, 326 + k * 12), (240, 332 + k * 12)], 2.4, None) for k in range(13)])
    art = crayon(art, seam * belly, "#b8956a", seed=nx(), amt=0.7, tooth=0.2)
    # muzzle, nose, face
    muzzle = shapes(W, H, [deform(ellipse_pts(240, 228, 48, 36, 16, 0), rng, 1, 0.02)])
    art = GP(art, muzzle, MUZ, "#f4e5cd", seed=nx(), rough=1.0, streak=0.6)
    art = tint(art, side_light(muzzle, -6, -6, 6), "#d6b98f", 0.4, seed=nx())
    nose = shapes(W, H, [[(222, 208), (258, 208), (250, 224), (240, 230), (230, 224)]])
    art = body_paint(art, nose, "#5a4033", "#6a4a3a", "#3a281f", "#8a6a5a", nx, ldir=(2, 3), blur=3)
    art = OV(art, ellipses(W, H, [(234, 212, 6, 3, 0)]), lambda m: col_arr(m, "#ffffff", m * 0.55))
    art = crayon(art, strokes(W, H, [([(240, 230), (240, 242)], 2.6, None)]), INK, seed=nx(), amt=0.85)
    art = smile(art, W, H, 228, 236, 12, nx, a0=0.3, a1=1.6, w=2.6)
    art = smile(art, W, H, 252, 236, 12, nx, a0=1.55, a1=2.85, w=2.6)
    art = eye(art, W, H, 196, 186, 8.5, nx, col="#3a281f")
    art = eye(art, W, H, 284, 186, 8.5, nx, col="#3a281f")
    art = cheek(art, W, H, 178, 222, 14, nx, col="#e8a596", amt=0.45)
    art = cheek(art, W, H, 302, 222, 14, nx, col="#e8a596", amt=0.45)
    # sage bow at the neck
    bowL = shapes(W, H, [deform([(240, 290), (196, 268), (186, 296), (196, 320)], rng, 1, 0.02)])
    bowR = shapes(W, H, [deform([(240, 290), (284, 268), (294, 296), (284, 320)], rng, 1, 0.02)])
    tails = shapes(W, H, [[(236, 296), (220, 342), (230, 338), (240, 300)], [(244, 296), (262, 342), (252, 338), (240, 300)]])
    art = body_paint(art, tails, SAGED, SAGE, "#566b52", SAGE, nx, ldir=(4, -4), blur=4)
    art = body_paint(art, np.clip(bowL + bowR, 0, 1), SAGE, SAGE2, SAGED, SAGEL, nx, ldir=(-4, -6), blur=8)
    folds = strokes(W, H, [([(232, 292), (206, 282)], 3, (0.2, 0.5)), ([(232, 298), (206, 310)], 3, (0.2, 0.5)), ([(248, 292), (274, 282)], 3, (0.2, 0.5)), ([(248, 298), (274, 310)], 3, (0.2, 0.5))])
    art = tint(art, gaussian_filter(folds, 1.5), SAGED, 0.6, seed=nx())
    art = body_paint(art, ellipses(W, H, [(240, 294, 13, 15, 0)]), SAGE, SAGE2, SAGED, SAGEL, nx, ldir=(-2, -3), blur=3)
    # gentle contour
    full = np.clip(ears + head + body + armL + armR + legL + legR, 0, 1)
    art = crayon(art, inner_edge(full, 2.0), "#8d6240", seed=nx(), amt=0.45, tooth=0.4)
    preview(art, "up-teddy", tone=BG)
    save(art, f"{OUT}/teddy.webp", max_w=300, quality=82)
    clear()

if "blocks" in PARTS:
    for name, face, face2, faced, sd in (("block-a", SAGE, SAGE2, SAGED, 0), ("block-b", BLUSH, BLUSH2, BLUSHD, 1), ("block-c", SAND, SAND2, SANDD, 2)):
        W, H = 240, 240
        nx = Seq(71200 + sd * 300); rng = random.Random(712 + sd)
        art = blank(W, H)
        front = [(24, 64), (184, 64), (184, 224), (24, 224)]
        top = [(24, 64), (184, 64), (222, 26), (62, 26)]
        side = [(184, 64), (222, 26), (222, 186), (184, 224)]
        fm = shapes(W, H, [deform(front, rng, 1, 0.003)], smooth=False)
        tm = shapes(W, H, [deform(top, rng, 1, 0.003)], smooth=False)
        sm = shapes(W, H, [deform(side, rng, 1, 0.003)], smooth=False)
        art = wood(art, sm, WOODD, "#a98457", "#8a6a44", nx, angle=1.57, ring=10)
        art = wood(art, tm, WOODL, WOOD2, WOODD, nx, angle=0.0, ring=9, grain_amt=0.25)
        art = wood(art, fm, WOOD, WOOD2, WOODD, nx, angle=0.0, ring=12, grain_amt=0.3)
        # coloured inset panels (front blank for HTML letter, top + side small)
        pf = shapes(W, H, [deform([(42, 82), (166, 82), (166, 206), (42, 206)], rng, 1, 0.004)])
        art = GP(art, pf, face, face2, seed=nx(), rough=1.0, streak=0.7)
        art = tint(art, side_light(pf, 5, 5, 6), faced, 0.35, seed=nx())
        pt = shapes(W, H, [[(56, 58), (152, 58), (176, 34), (80, 34)]])
        art = GP(art, pt, mix(face, "#ffffff", 0.2), face, seed=nx(), rough=0.8, pad=6)
        ps = shapes(W, H, [[(194, 72), (212, 52), (212, 168), (194, 190)]])
        art = GP(art, ps, mix(face, "#000000", 0.12), faced, seed=nx(), rough=0.8, pad=6)
        # rounded bevel highlights + shadow
        art = crayon(art, strokes(W, H, [([(26, 66), (182, 66)], 3, None), ([(26, 66), (26, 222)], 3, None)]), "#fff3e0", seed=nx(), amt=0.6, tooth=0.3)
        art = crayon(art, inner_edge(np.clip(fm + tm + sm, 0, 1), 1.6), "#9a7650", seed=nx(), amt=0.55, tooth=0.3)
        preview(art, f"up-{name}", tone=BG)
        save_full(art, f"{OUT}/{name}.webp", size=(132, 132), quality=84)
        clear()

if "cake" in PARTS:
    W, H = 360, 400
    nx = Seq(71300); rng = random.Random(713)
    art = blank(W, H)
    art = soft_ground(art, W, H, 180, 372, 150, 14, "#8a6a4a", nx, 0.3)
    # wooden board
    board = ellipses(W, H, [(180, 350, 150, 26, 0)])
    rim = ellipses(W, H, [(180, 358, 150, 26, 0)])
    art = wood(art, np.clip(rim - board * 0.0, 0, 1), WOODD, "#a98457", "#8a6a44", nx, angle=0, ring=8)
    art = wood(art, board, WOOD, WOOD2, WOODD, nx, angle=0, ring=10)
    # cake body (cylinder)
    cyl = shapes(W, H, [[(82, 200), (278, 200), (278, 330)] + [(180 + 98 * math.cos(t), 330 + 18 * math.sin(t)) for t in np.linspace(0, math.pi, 24)] + [(82, 330)]], smooth=False)
    art = body_paint(art, cyl, CREAM, "#f7efe2", "#d9c6ac", "#ffffff", nx, ldir=(14, 0), blur=14, light_amt=0.3)
    # sage buttercream band + naked-cake stripe
    band = shapes(W, H, [[(82, 262), (278, 262), (278, 286)] + [(180 + 98 * math.cos(t), 286 + 18 * math.sin(t)) for t in np.linspace(0, math.pi, 24)] + [(82, 286)]], smooth=False) * cyl
    art = GP(art, band, SAGE, SAGE2, seed=nx(), rough=1.2, streak=0.9)
    art = tint(art, side_light(cyl, 16, 0, 14) * band, SAGED, 0.4, seed=nx())
    # top + drips
    topm = ellipses(W, H, [(180, 200, 98, 20, 0)])
    drips = []
    for i in range(9):
        x = 90 + i * 22 + rng.uniform(-4, 4)
        L = rng.uniform(16, 42)
        drips.append((curve([(x, 204 + 14 * math.sin((x - 82) / 196 * math.pi)), (x + rng.uniform(-1, 1), 214 + L)], 6), rng.uniform(11, 15), (0.0, 0.0)))
    dm = np.clip(strokes(W, H, drips) * cyl + topm, 0, 1)
    art = body_paint(art, dm, BLUSH, BLUSH2, BLUSHD, "#f8e0d6", nx, ldir=(8, 4), blur=6, light_amt=0.4)
    # sprinkles of dried petals + berries on top
    for _ in range(6):
        x, y = rng.uniform(110, 250), rng.uniform(192, 208)
        art = body_paint(art, circles(W, H, [(x, y, rng.uniform(6, 8))]), "#c86a6a", "#d07a78", "#8e3f45", "#f0a7a0", nx, ldir=(2, 2), blur=2)
    art = G(art, shapes(W, H, [petal_pts(212, 198, 26, 9, -0.4), petal_pts(214, 198, 22, 8, -1.6)]), SAGE, SAGED, seed=nx(), density=0.8, edge=0.4, rough=2, feather=1.2)
    # one candle + flame
    candle = shapes(W, H, [[(172, 120), (188, 120), (188, 200), (172, 200)]], smooth=False)
    art = body_paint(art, candle, "#f6efe3", "#efe4d2", "#cbb796", "#ffffff", nx, ldir=(3, 0), blur=4)
    art = GP(art, strokes(W, H, [([(172, 132 + k * 18), (188, 124 + k * 18)], 4, None) for k in range(4)]) * candle, SAGE, SAGE2, seed=nx(), rough=0.5, pad=6)
    flame = shapes(W, H, [petal_pts(180, 116, 38, 11, -math.pi / 2, n=16)])
    art = OV(art, flame, lambda m: glow(m, "#ffd98a", 14, 0.5), pad=40)
    art = GP(art, flame, "#f6b84f", "#fcd57a", seed=nx(), rough=0.4, pad=6)
    art = GP(art, shapes(W, H, [petal_pts(180, 110, 18, 5, -math.pi / 2, n=12)]), "#fff4d0", seed=nx(), rough=0.3, pad=6)
    art = crayon(art, strokes(W, H, [([(180, 120), (180, 112)], 2.4, None)]), INK, seed=nx(), amt=0.8)
    art = crayon(art, inner_edge(np.clip(cyl + dm, 0, 1), 1.8), "#b89c80", seed=nx(), amt=0.45)
    preview(art, "up-cake", tone=BG)
    save(art, f"{OUT}/cake.webp", max_w=220, quality=82)
    clear()

if "garland" in PARTS:
    W, H = 900, 170
    nx = Seq(71400); rng = random.Random(714)
    art = blank(W, H)
    rope = curve([(0, 26), (W * .5, 92), (W, 26)], 100)
    art = crayon(art, strokes(W, H, [(rope, 2.6, None)]), "#a88a68", seed=nx(), amt=0.9, tooth=0.3)
    cols = [(SAGE, SAGE2), (CREAM, "#f1e8da"), (BLUSH, BLUSH2), (SAND, SAND2), (FURL, FUR)]
    n = 17
    for i in range(n):
        t = (i + 0.5) / n
        x, y = rope[int(t * (len(rope) - 1))]
        c, c2 = cols[i % len(cols)]
        r = 22 if i % 2 == 0 else 17
        m = circles(W, H, [(x, y + 2, r)])
        art = felt(art, m, c, c2, seed=nx(), stitch=None, puff=0.32, fuzz=0.6, pad=10)
        art = tint(art, side_light(m, 6, 6, 8), mix(c, "#5a4536", 0.35), 0.45, seed=nx())
        if i % 4 == 2:
            clear()
    # small wooden star in the middle
    sm = shapes(W, H, [star_pts(W / 2, 128, 26, 12)])
    art = wood(art, sm, WOOD, WOOD2, WOODD, nx, angle=0.3, ring=7)
    art = crayon(art, inner_edge(sm, 1.6), "#9a7650", seed=nx(), amt=0.6)
    art = crayon(art, strokes(W, H, [([(W / 2, 95), (W / 2, 104)], 2, None)]), "#a88a68", seed=nx(), amt=0.9)
    preview(art, "up-garland", tone=BG)
    save(art, f"{OUT}/garland.webp", max_w=640, quality=80)
    clear()

if "sprig" in PARTS:
    W, H = 360, 140
    nx = Seq(71500); rng = random.Random(715)
    art = blank(W, H)
    stem = curve([(20, 92), (120, 70), (230, 62), (340, 76)], 60)
    art = G(art, strokes(W, H, [(stem, 3.2, (0.0, 0.4))]), "#7f8f6e", seed=nx(), density=0.9, edge=0.3, rough=1.5, feather=0.8)
    for k in range(1, 9):
        t = k / 9.5
        x, y = stem[int(t * (len(stem) - 1))]
        for side in (-1, 1):
            r = 15 - abs(t - 0.5) * 8
            cx, cy = x + 4, y + side * (r + 3)
            m = shapes(W, H, [deform(ellipse_pts(cx, cy, r, r * 0.9, 14, 0), rng, 1, 0.04)])
            art = G(art, m, rng.choice([SAGE, "#93a88e", "#a7b8a0"]), SAGED, seed=nx(), density=0.75, edge=0.55, bloom=0.3, rough=2.5, feather=1.2)
    preview(art, "up-sprig", tone=BG)
    save(art, f"{OUT}/sprig.webp", max_w=200, quality=82)
    clear()
