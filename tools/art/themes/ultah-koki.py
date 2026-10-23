"""Ultah Koki — little-chef birthday kitchen, kids picture-book gouache with wobbly ink outlines: a counter with a
mixing bowl of batter and whisk, rolling pin, flour sack, eggs, cupcakes and Kiki (an original cupcake mascot in a chef
hat); a rail of hanging utensils and oven mitt; a chef hat; a candle cupcake; a rolling-pin divider; mint wall tiles.
Run: python3 -I ultah-koki.py [part ...]  parts: counter rail hat cupcake pin tile"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i3_lib import *

OUT = outdir("ultah-koki")
PARTS = sys.argv[1:] or ["counter", "rail", "hat", "cupcake", "pin", "tile"]
INK = "#2f3a5a"
MINT, MINT_D, MINT_L = "#7fcdb4", "#55ad94", "#c3ebdd"
TOMATO, TOMATO_D = "#e5533d", "#c23f2d"
BUTTER, CREAM, PINK, PINK_D = "#f6cf5a", "#fff6e6", "#f6a7bd", "#e47e9b"
WOOD, WOOD_D, WOOD_L = "#dba46b", "#b97d45", "#f0c690"
WHITE = "#fffdf8"


def ell(W, H, cx, cy, rx, ry, rot=0.0):
    return ellipses(W, H, [(cx, cy, rx, ry, rot)])


def rrect(W, H, x0, y0, x1, y1, r, rot=0.0, cx=None, cy=None):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        cv.c.save()
        if rot:
            cv.c.rotate(rot, cx if cx is not None else (x0 + x1) / 2, cy if cy is not None else (y0 + y1) / 2)
        cv.c.drawRoundRect(skia.Rect(x0, y0, x1, y1), r, r, p)
        cv.c.restore()
    return mask_from(W, H, draw)


def shadow(art, W, H, cx, cy, rx, ry, a=0.22):
    return over(art, flat(gaussian_filter(ell(W, H, cx, cy, rx, ry), 6), "#5a4a5a", a))


def cupcake(art, W, H, cx, by, s, nx, wrap=(PINK, PINK_D), frost=CREAM, cherry=True, face=False, sprinkles=True, rng=None):
    """cupcake standing on by; s = scale (wrapper width ~ 80*s)."""
    rng = rng or random.Random(1)
    ww, wh = 78 * s, 54 * s
    wrapm = shapes(W, H, [[(cx - ww / 2, by - wh), (cx + ww / 2, by - wh), (cx + ww * 0.38, by), (cx - ww * 0.38, by)]], smooth=False)
    art = inked(art, wrapm, wrap[0], wrap[1], seed=nx(), ink=INK, lw=2.6)
    pleats = polyline_mask(W, H, [[(cx + t * ww / 2, by - wh + 3), (cx + t * ww * 0.38, by - 3)] for t in np.linspace(-0.75, 0.75, 6)], 2.0 * s)
    art = over(art, flat(pleats * wrapm, wrap[1], 0.75))
    # frosting: three stacked blobs
    fr = np.maximum.reduce([ell(W, H, cx, by - wh - 8 * s, ww * 0.58, 20 * s), ell(W, H, cx, by - wh - 30 * s, ww * 0.42, 17 * s), ell(W, H, cx + 2 * s, by - wh - 48 * s, ww * 0.24, 13 * s)])
    art = inked(art, fr, frost, mix(frost, "#d9c2c0", 0.3) if frost == CREAM else frost, seed=nx(), ink=INK, lw=2.6)
    art = highlight(art, fr, "#ffffff", 0.45, 6)
    if sprinkles:
        cols = [TOMATO, MINT_D, BUTTER, "#7a8ce0"]
        for k in range(10):
            a = rng.uniform(0, math.tau)
            x = cx + rng.uniform(-ww * 0.45, ww * 0.45); y = by - wh - rng.uniform(4, 44) * s
            if fr[int(y), int(x)] < 0.5:
                continue
            m = strokes(W, H, [([(x, y), (x + math.cos(a) * 6 * s, y + math.sin(a) * 6 * s)], 3.2 * s, None)])
            art = GP(art, m, cols[k % 4], seed=nx(), rough=0.3, pad=4)
    if cherry:
        ch = ell(W, H, cx + 4 * s, by - wh - 64 * s, 9 * s, 9 * s)
        art = inked(art, ch, TOMATO, TOMATO_D, seed=nx(), ink=INK, lw=2.2)
        art = GP(art, strokes(W, H, [(curve([(cx + 6 * s, by - wh - 72 * s), (cx + 10 * s, by - wh - 82 * s), (cx + 18 * s, by - wh - 86 * s)], 8), 2.2 * s, None)]), "#5b8a3a", seed=nx(), rough=0.3, pad=4)
        art = over(art, flat(ell(W, H, cx + 1 * s, by - wh - 67 * s, 2.6 * s, 2.2 * s), "#ffffff", 0.8))
    if face:
        eyes = np.maximum(ell(W, H, cx - 14 * s, by - wh * 0.58, 3.6 * s, 4.4 * s), ell(W, H, cx + 14 * s, by - wh * 0.58, 3.6 * s, 4.4 * s))
        art = over(art, flat(eyes, INK, 0.95))
        art = over(art, flat(np.maximum(ell(W, H, cx - 13 * s, by - wh * 0.62, 1.2 * s, 1.2 * s), ell(W, H, cx + 15 * s, by - wh * 0.62, 1.2 * s, 1.2 * s)), "#ffffff", 0.95))
        smile = strokes(W, H, [(arc_pts(cx, by - wh * 0.48, 9 * s, 0.35, math.pi - 0.35, 12), 2.6 * s, None)])
        art = over(art, flat(smile, INK, 0.95))
        cheeks = np.maximum(ell(W, H, cx - 24 * s, by - wh * 0.42, 6 * s, 4 * s), ell(W, H, cx + 24 * s, by - wh * 0.42, 6 * s, 4 * s))
        art = over(art, flat(gaussian_filter(cheeks, 1.5), "#f07a7a", 0.55))
    return art


def chef_hat(art, W, H, cx, by, s, nx, rot=0.0):
    """toque: puffy top (overlapping circles) + pleated band; base centre (cx, by)."""
    band = rrect(W, H, cx - 40 * s, by - 34 * s, cx + 40 * s, by, 7 * s, rot, cx, by)
    puffs = [(cx - 34 * s, by - 52 * s, 26 * s), (cx, by - 66 * s, 32 * s), (cx + 34 * s, by - 52 * s, 26 * s), (cx - 14 * s, by - 44 * s, 26 * s), (cx + 16 * s, by - 44 * s, 26 * s)]
    if rot:
        a = math.radians(rot)
        puffs = [(cx + (x - cx) * math.cos(a) - (y - by) * math.sin(a), by + (x - cx) * math.sin(a) + (y - by) * math.cos(a), r) for x, y, r in puffs]
    top = np.clip(circles(W, H, puffs) - band, 0, 1)
    art = inked(art, top, WHITE, "#eef0f6", seed=nx(), ink=INK, lw=2.8)
    art = shade_side(art, top, "#b8c0d8", (1, 1), 0.45, 14, nx())
    art = inked(art, band, WHITE, "#f1f2f6", seed=nx(), ink=INK, lw=2.8)
    pl = []
    for t in np.linspace(-0.6, 0.6, 5):
        x = cx + t * 40 * s
        p = [(x, by - 30 * s), (x, by - 4 * s)]
        if rot:
            a = math.radians(rot)
            p = [(cx + (px - cx) * math.cos(a) - (py - by) * math.sin(a), by + (px - cx) * math.sin(a) + (py - by) * math.cos(a)) for px, py in p]
        pl.append(p)
    art = over(art, flat(polyline_mask(W, H, pl, 1.6 * s) * band, "#aeb6cc", 0.8))
    return art


if "counter" in PARTS:
    W, H = 900, 440
    nx = Seq(64100); rng = random.Random(8)
    art = blank(W, H)
    top_y = 352
    # counter: wood top + mint front with tile edge
    slab = rrect(W, H, -20, top_y, W + 20, top_y + 30, 8)
    front = shapes(W, H, [[(-10, top_y + 26), (W + 10, top_y + 26), (W + 10, H), (-10, H)]], smooth=False)
    art = GP(art, front, MINT_D, "#4a9d85", seed=nx(), rough=0.6, streak=1.0)
    art = over(art, flat(polyline_mask(W, H, [[(x, top_y + 40), (x, H)] for x in range(150, W, 300)], 3, cap=False), "#3b8270", 0.7))
    art = over(art, flat(circles(W, H, [(x + d, top_y + 64, 6) for x in range(150, W, 300) for d in (-18, 18)]), BUTTER, 1))
    art = inked(art, slab, WOOD, WOOD_D, seed=nx(), ink=INK, lw=3.0)
    art = over(art, flat(polyline_mask(W, H, [[(x, top_y + 6), (x + 60, top_y + 8)] for x in range(10, W, 90)], 1.4) * slab, WOOD_D, 0.5))
    # flour sack (left) + spilled flour
    sack = shapes(W, H, [[(60, top_y), (54, top_y - 70), (70, top_y - 118), (84, top_y - 128), (110, top_y - 132), (134, top_y - 124), (150, top_y - 112), (164, top_y - 70), (160, top_y)]])
    art = shadow(art, W, H, 112, top_y + 4, 70, 8)
    art = inked(art, sack, "#f4e8d2", "#e6d4b4", seed=nx(), ink=INK, lw=3)
    art = shade_side(art, sack, "#c9b28c", (1, 0), 0.4, 18, nx())
    tie = strokes(W, H, [([(80, top_y - 122), (140, top_y - 118)], 7, None)])
    art = GP(art, tie, TOMATO, seed=nx(), rough=0.4, pad=6)
    label = rrect(W, H, 78, top_y - 80, 142, top_y - 36, 8)
    art = inked(art, label, TOMATO, TOMATO_D, seed=nx(), ink=INK, lw=2.2)
    wheat = strokes(W, H, [([(110, top_y - 44), (110, top_y - 72)], 2.4, None)] + [([(110, top_y - 50 - k * 7), (110 + sg * 8, top_y - 56 - k * 7)], 3.4, (0.1, 0.5)) for k in range(3) for sg in (-1, 1)])
    art = GP(art, wheat, BUTTER, seed=nx(), rough=0.3, pad=4)
    puff = circles(W, H, [(178, top_y - 4, 16), (200, top_y - 2, 11), (160, top_y - 2, 10), (215, top_y, 6)])
    art = GP(art, puff, WHITE, "#f2efe8", seed=nx(), rough=2.0, pad=8)
    # rolling pin lying diagonal-ish in front
    pin = rrect(W, H, 210, top_y - 26, 390, top_y - 2, 12, -4, 300, top_y - 14)
    hl = rrect(W, H, 170, top_y - 20, 214, top_y - 8, 6, -4, 300, top_y - 14)
    hr = rrect(W, H, 386, top_y - 33, 432, top_y - 21, 6, -4, 300, top_y - 14)
    art = shadow(art, W, H, 300, top_y + 2, 120, 6)
    art = inked(art, np.maximum(hl, hr), WOOD_D, "#a36a38", seed=nx(), ink=INK, lw=2.4)
    art = inked(art, pin, WOOD_L, WOOD, seed=nx(), ink=INK, lw=2.8)
    art = highlight(art, pin, "#ffffff", 0.35, 5)
    # big mixing bowl (centre) with batter + whisk
    bx, by = 520, top_y - 8
    bowl_body = shapes(W, H, [arc_pts(bx, by - 70, 130, 0, math.pi, 40, squash=0.62)])
    base = rrect(W, H, bx - 46, by - 10, bx + 46, by + 2, 5)
    art = shadow(art, W, H, bx, by + 4, 120, 9)
    art = inked(art, base, MINT_D, seed=nx(), ink=INK, lw=2.4)
    art = inked(art, bowl_body, MINT, MINT_D, seed=nx(), ink=INK, lw=3.0)
    art = shade_side(art, bowl_body, "#3f8f78", (1, 1), 0.4, 26, nx())
    art = highlight(art, bowl_body, "#ffffff", 0.3, 12)
    stripe = np.clip(ell(W, H, bx, by - 50, 118, 40) - ell(W, H, bx, by - 58, 118, 40), 0, 1) * bowl_body
    art = over(art, flat(stripe, WHITE, 0.85))
    rim = ell(W, H, bx, by - 70, 137, 26)
    art = inked(art, rim, MINT_L, MINT, seed=nx(), ink=INK, lw=3.0)
    batter = ell(W, H, bx, by - 70, 114, 18)
    art = GP(art, batter, "#f8dc8a", "#f2cc6e", seed=nx(), rough=1.0, pad=8)
    swirl = strokes(W, H, [(spiral_pts(bx - 20, by - 70, 4, 40, 0, 1.3, 40) , 3.0, None)])
    swirl *= np.clip(batter * 1.2, 0, 1)
    art = over(art, flat(swirl, "#e0b04a", 0.8))
    # batter drip over the rim
    drip = shapes(W, H, [[(bx + 60, by - 60), (bx + 84, by - 58), (bx + 82, by - 36), (bx + 76, by - 30), (bx + 70, by - 36), (bx + 66, by - 50)]])
    art = inked(art, drip, "#f8dc8a", "#f2cc6e", seed=nx(), ink=INK, lw=2.2)
    # whisk standing in the batter, leaning right
    t = 0.42
    d = (math.sin(t), -math.cos(t))
    base_ = (bx + 34, by - 70)
    c = (base_[0] + d[0] * 48, base_[1] + d[1] * 48)
    loops = [ellipse_pts(c[0], c[1], rr, 54, 18, rot=t) for rr in (26, 17, 8)]
    wire = polyline_mask(W, H, [lp + [lp[0]] for lp in loops], 3.2)
    wire *= 1 - batter * (np.mgrid[0:H, 0:W][0] > by - 78)
    art = over(art, flat(gaussian_filter(wire, 0.6), "#8f9bb8", 1.0))
    art = over(art, flat(np.clip(wire - gaussian_filter(wire, 1.2) * 0.6, 0, 1), "#ffffff", 0.6))
    handle = strokes(W, H, [([(c[0] + d[0] * 44, c[1] + d[1] * 44), (c[0] + d[0] * 122, c[1] + d[1] * 122)], 15, None)])
    art = inked(art, handle, TOMATO, TOMATO_D, seed=nx(), ink=INK, lw=2.4)
    # eggs (right of bowl)
    for (ex, ey, r) in [(680, top_y - 4, 24), (718, top_y - 2, 21)]:
        art = shadow(art, W, H, ex, ey + 3, r + 6, 5)
        egg = shapes(W, H, [ellipse_pts(ex, ey - r * 1.1, r * 0.86, r * 1.12, 22)])
        art = inked(art, egg, "#fbf3e6", "#efe0c8", seed=nx(), ink=INK, lw=2.6)
        art = shade_side(art, egg, "#d8c3a2", (1, 1), 0.4, 10, nx())
    # Kiki the cupcake mascot (with chef hat) + two plain cupcakes at right
    art = shadow(art, W, H, 800, top_y + 2, 52, 7)
    art = cupcake(art, W, H, 800, top_y, 1.25, nx, wrap=(MINT, MINT_D), frost=PINK, cherry=False, face=True, rng=rng)
    art = chef_hat(art, W, H, 803, top_y - 64 * 1.25 - 40, 0.74, nx, rot=8)
    art = shadow(art, W, H, 640, top_y + 2, 36, 5)
    art = cupcake(art, W, H, 628, top_y, 0.78, nx, wrap=(PINK, PINK_D), frost=CREAM, rng=rng)
    prev(art, "koki-counter", tone="#dff3ec")
    save(art, f"{OUT}/counter.webp", max_w=720, quality=82)
    clear()


if "rail" in PARTS:
    W, H = 900, 300
    nx = Seq(64200); rng = random.Random(3)
    art = blank(W, H)
    ry = 30
    bar = rrect(W, H, 40, ry - 7, W - 40, ry + 7, 7)
    brackets = np.maximum(rrect(W, H, 52, ry - 22, 70, ry + 14, 4), rrect(W, H, W - 70, ry - 22, W - 52, ry + 14, 4))
    art = inked(art, brackets, "#9aa4c0", "#7f89a8", seed=nx(), ink=INK, lw=2.4)
    art = inked(art, bar, "#c6cede", "#a8b2c8", seed=nx(), ink=INK, lw=2.6)
    items = [
        ("spoon", 150), ("whisk", 270), ("mitt", 410), ("ladle", 555), ("spatula", 680), ("pan", 800),
    ]
    for kind, x in items:
        hook = strokes(W, H, [(curve([(x, ry), (x + 6, ry + 8), (x, ry + 18), (x - 5, ry + 13)], 10), 3, None)])
        art = over(art, flat(hook, INK, 0.9))
        if kind == "spoon":
            h = rrect(W, H, x - 6, ry + 16, x + 6, ry + 150, 6)
            bowl = ell(W, H, x, ry + 176, 20, 30)
            art = inked(art, np.maximum(h, bowl), WOOD, WOOD_D, seed=nx(), ink=INK, lw=2.6)
            art = over(art, flat(ell(W, H, x + 2, ry + 180, 11, 18), WOOD_D, 0.35))
        elif kind == "whisk":
            h = rrect(W, H, x - 8, ry + 16, x + 8, ry + 84, 7)
            art = inked(art, h, BUTTER, "#e2b43c", seed=nx(), ink=INK, lw=2.4)
            loops = [ellipse_pts(x, ry + 140, rr, 58, 18) for rr in (26, 17, 8)]
            wire = polyline_mask(W, H, [lp + [lp[0]] for lp in loops], 3.0) * (np.mgrid[0:H, 0:W][0] > ry + 84)
            art = over(art, flat(wire, "#8f9bb8", 1.0))
            art = over(art, flat(np.clip(wire - gaussian_filter(wire, 1.2) * 0.6, 0, 1), "#ffffff", 0.6))
        elif kind == "mitt":
            loop = strokes(W, H, [(arc_pts(x, ry + 26, 9, math.pi, 0, 10), 3, None)])
            art = over(art, flat(loop, TOMATO_D, 1))
            mitt = shapes(W, H, [[(x - 40, ry + 36), (x + 34, ry + 36), (x + 40, ry + 120), (x + 30, ry + 170), (x - 4, ry + 196), (x - 40, ry + 186), (x - 50, ry + 140), (x - 72, ry + 120), (x - 74, ry + 96), (x - 56, ry + 92), (x - 44, ry + 104)]])
            art = inked(art, mitt, TOMATO, TOMATO_D, seed=nx(), ink=INK, lw=3.0)
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            check = ((((xx // 14) + (yy // 14)) % 2) == 0).astype(np.float32) * mitt
            art = over(art, flat(check, "#ffffff", 0.32))
            cuff = rrect(W, H, x - 44, ry + 34, x + 38, ry + 56, 8)
            art = inked(art, cuff, WHITE, "#eef0f6", seed=nx(), ink=INK, lw=2.6)
        elif kind == "ladle":
            h = rrect(W, H, x - 5, ry + 16, x + 5, ry + 150, 5)
            cup = shapes(W, H, [arc_pts(x, ry + 150, 30, 0, math.pi, 20, squash=0.9)])
            art = inked(art, np.maximum(h, cup), "#c6cede", "#9aa4c0", seed=nx(), ink=INK, lw=2.6)
            art = highlight(art, cup, "#ffffff", 0.45, 6)
        elif kind == "spatula":
            h = rrect(W, H, x - 7, ry + 16, x + 7, ry + 120, 7)
            art = inked(art, h, MINT_D, "#3f8f78", seed=nx(), ink=INK, lw=2.4)
            blade = rrect(W, H, x - 24, ry + 118, x + 24, ry + 190, 10)
            art = inked(art, blade, MINT, MINT_D, seed=nx(), ink=INK, lw=2.6)
            slots = polyline_mask(W, H, [[(x + d, ry + 134), (x + d, ry + 176)] for d in (-10, 0, 10)], 3.4)
            art = over(art, flat(slots, INK, 0.75))
        elif kind == "pan":
            h = rrect(W, H, x - 6, ry + 16, x + 6, ry + 100, 6)
            art = inked(art, h, "#3b4462", "#2c3450", seed=nx(), ink=INK, lw=2.2)
            pan = ell(W, H, x, ry + 150, 52, 52)
            art = inked(art, pan, "#4a5578", "#3b4462", seed=nx(), ink=INK, lw=2.8)
            art = over(art, flat(np.clip(ell(W, H, x, ry + 150, 42, 42) - ell(W, H, x, ry + 150, 38, 38), 0, 1), "#6a7598", 0.9))
            art = highlight(art, pan, "#ffffff", 0.35, 10)
    prev(art, "koki-rail", tone="#dff3ec")
    save(art, f"{OUT}/rail.webp", max_w=720, quality=82)
    clear()


if "hat" in PARTS:
    W, H = 260, 220
    nx = Seq(64300)
    art = chef_hat(blank(W, H), W, H, 130, 204, 1.55, nx)
    prev(art, "koki-hat", tone="#dff3ec")
    save(art, f"{OUT}/hat.webp", max_w=200, quality=84)
    clear()


if "cupcake" in PARTS:
    W, H = 240, 300
    nx = Seq(64400); rng = random.Random(5)
    art = cupcake(blank(W, H), W, H, 120, 286, 1.9, nx, wrap=(TOMATO, TOMATO_D), frost=CREAM, cherry=False, rng=rng)
    # birthday candle with flame on top
    c = rrect(W, H, 112, 18, 128, 92, 4)
    art = inked(art, c, "#7a8ce0", "#6274c8", seed=nx(), ink=INK, lw=2.2)
    art = over(art, flat(polyline_mask(W, H, [[(112, 30 + k * 16), (128, 22 + k * 16)] for k in range(5)], 3) * c, WHITE, 0.9))
    flame = shapes(W, H, [petal_pts(120, 16, 22, 9, -math.pi / 2, n=14)])
    art = over(art, glow(flame, "#ffd36a", 8, 0.5))
    art = inked(art, flame, BUTTER, "#f39a3a", seed=nx(), ink=INK, lw=1.8)
    prev(art, "koki-cupcake", tone="#dff3ec")
    save(art, f"{OUT}/cupcake.webp", max_w=160, quality=84)
    clear()


if "pin" in PARTS:
    # divider: chunky rolling pin + a few sprinkles
    W, H = 420, 96
    nx = Seq(64500); rng = random.Random(2)
    art = blank(W, H)
    body = rrect(W, H, 116, 24, 304, 72, 22)
    hs = np.maximum(rrect(W, H, 64, 38, 120, 58, 10), rrect(W, H, 300, 38, 356, 58, 10))
    art = inked(art, hs, WOOD_D, "#a36a38", seed=nx(), ink=INK, lw=3.0)
    art = inked(art, body, WOOD_L, WOOD, seed=nx(), ink=INK, lw=3.2)
    art = highlight(art, body, "#ffffff", 0.4, 6)
    cols = [TOMATO, MINT_D, BUTTER, PINK_D, "#7a8ce0"]
    for k, (x, y) in enumerate([(22, 40), (40, 62), (382, 36), (400, 60), (366, 74), (34, 80)]):
        a_ = rng.uniform(0, math.pi)
        m = strokes(W, H, [([(x, y), (x + math.cos(a_) * 12, y + math.sin(a_) * 12)], 7, None)])
        art = GP(art, m, cols[k % 5], seed=nx(), rough=0.3, pad=4)
    prev(art, "koki-pin", tone="#dff3ec")
    save(art, f"{OUT}/pin.webp", max_w=300, quality=84)
    clear()


if "tile" in PARTS:
    # seamless 4x4 kitchen wall tiles: mint glaze, white grout, a glossy streak per tile
    W = H = 256
    nx = Seq(64600); rng = random.Random(6)
    art = solid(W, H, "#f7f3ea")
    t = 64
    for j in range(4):
        for i in range(4):
            m = rrect(W, H, i * t + 3, j * t + 3, (i + 1) * t - 3, (j + 1) * t - 3, 6)
            col = mix(MINT_L, "#aee0cf", rng.uniform(0, 1))
            art = GP(art, m, col, mix(col, "#9ed6c3", 0.4), seed=nx(), rough=0.4, streak=0.6, pad=4)
            gl = strokes(W, H, [([(i * t + 14, j * t + 44), (i * t + 40, j * t + 14)], 4, (0.3, 0.3))])
            art = over(art, flat(gaussian_filter(gl, 1.5), "#ffffff", 0.5))
    art = add_grain(art, nx(), 0.03)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/tile.webp", quality=74)
    prev(art, "koki-tile")
    clear()
