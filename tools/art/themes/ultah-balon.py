"""Ultah Balon — gouache picture-book party pieces (balloons, bunting, cake, candle, flame, gifts, paper).
Run: python3 -I /tmp/pen/art/themes/ultah-balon.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _h_common import *

D = outdir("ultah-balon")
INK = "#2d2a4a"
PAL = {  # base, shadow, light
    "coral": ("#f0645c", "#c2404a", "#ffb3a6"),
    "sun": ("#f6c246", "#d9932c", "#fff0b5"),
    "mint": ("#4cbfb3", "#2f8d8c", "#c5f1e8"),
    "grape": ("#8b79e6", "#5d4fb5", "#d7cfff"),
    "orange": ("#f59a45", "#cf6a2b", "#ffd3a1"),
}
ORDER = ["coral", "sun", "mint", "grape", "orange"]
sd = Seeds(300)


def balloon_pts(cx, cy, r, rng):
    pts = []
    for i in range(28):
        t = i / 28 * math.tau
        x = math.cos(t) * r * 0.86
        y = math.sin(t) * r
        if y > 0:  # narrower, pointier bottom
            x *= 1 - 0.32 * (y / r) ** 1.6
            y *= 1.08
        pts.append((cx + x, cy + y))
    return deform(pts, rng, 1, 0.01)


def balloon(name, idx):
    W, H = 170, 330
    rng = random.Random(40 + idx)
    base, shadow, light = PAL[name]
    cx, cy, r = 85, 82, 62
    art = blank(W, H)
    body_pts = balloon_pts(cx, cy, r, rng)
    body = shape_mask(W, H, body_pts)
    by = cy + r * 1.08
    knot = poly_mask(W, H, [(cx - 7, by + 9), (cx + 7, by + 9), (cx + 1, by - 3), (cx - 1, by - 3)])
    # string first (behind)
    sx = [(cx, by + 8), (cx - 6, by + 34), (cx + 6, by + 62), (cx - 4, by + 92), (cx + 1, by + 116)]
    string = stroke_mask(W, H, curve(sx, 90), 2.4, (0.02, 0.4))
    art = ink(art, string, INK, seed=sd(), wear=0.15, alpha=0.55)
    art = gouache_form(art, union(body, knot), base, shadow, seed=sd(), sdx=-0.16, sdy=-0.1)
    # reflected light on the shadow side bottom-right
    refl = stroke_mask(W, H, arc_pts(cx, cy + 4, r * 0.8, 0.1, 1.2, 14), 4)
    rl = gouache_paint(refl * body, mix(base, light, 0.35), seed=sd(), rough=2)
    rl[..., 3] *= 0.45
    art = over(art, rl)
    # highlight: a loose comma stroke top-left plus a small dot
    hl = stroke_mask(W, H, arc_pts(cx - 4, cy - 2, r * 0.62, math.pi * 1.08, math.pi * 1.42, 12), 9, (0.3, 0.45))
    hd = dab(W, H, cx - 20, cy - 46, 4, 3.4, 0, rng)
    h = gouache_paint(union(hl, hd) * body, light, seed=sd(), rough=1.6)
    h[..., 3] *= 0.85
    art = over(art, h)
    # ink contour, slightly off-register
    art = ink(art, outline_mask(W, H, [(x + 1.2, y + 0.8) for x, y in body_pts], 3.0, rng, wob=0.006, breaks=0.03), INK, seed=sd(), wear=0.2, alpha=0.88)
    art = ink(art, outline_mask(W, H, [(cx - 7, by + 9), (cx + 7, by + 9), (cx + 1, by - 2)], 2.2, rng, wob=0), INK, seed=sd(), alpha=0.8)
    return art


def bunting():
    W, H = 840, 120
    rng = random.Random(9)
    art = blank(W, H)
    sag = lambda x: 12 + 50 * 4 * (x / W) * (1 - x / W) * 0.98
    n = 11
    fw = W / n
    flags = []
    for i in range(n):
        x0 = i * fw + 6; x1 = x0 + fw - 12
        y0, y1 = sag(x0) + 2, sag(x1) + 2
        tip = ((x0 + x1) / 2 + rng.uniform(-3, 3), (y0 + y1) / 2 + 44 + rng.uniform(-3, 3))
        flags.append((ORDER[i % 5], [(x0, y0), (x1, y1), tip]))
    for k, (name, tri) in enumerate(flags):
        base, shadow, light = PAL[name]
        pts = []
        for a, b in [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]:
            for t in (0, .33, .66):
                pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        pts = deform(pts, rng, 1, 0.012)
        m = poly_mask(W, H, pts)
        art = over(art, gouache_paint(m, base, mix(base, shadow, .35), seed=sd(), rough=2.4, streak=0.8))
        # small painted dots on alternating flags
        if k % 2 == 0:
            def dots(cv, tri=tri):
                cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3; cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3
                for (dx, dy) in [(-8, -6), (7, -5), (0, 6)]:
                    cv.c.drawCircle(cx + dx, cy + dy, 2.6, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
            dm = mask_from(W, H, dots) * m
            art = over(art, gouache_paint(dm, light, seed=sd(), rough=0.8))
        art = ink(art, outline_mask(W, H, pts, 2.0, rng, wob=0.004, breaks=0.05), INK, seed=sd(), wear=.25, alpha=.8)
    line = [(x, sag(x)) for x in np.linspace(0, W, 60)]
    art = ink(art, stroke_mask(W, H, line, 2.8, (0.01, 0.01)), INK, seed=sd(), wear=.2, alpha=.85)
    return art


def cake():
    W, H = 400, 330
    rng = random.Random(77)
    art = blank(W, H)
    # plate shadow
    sh = dab(W, H, 200, 304, 176, 14, 0, rng)
    s = gouache_paint(sh, "#c9a57e", seed=sd(), rough=3)
    s[..., 3] *= 0.45
    art = over(art, s)
    plate = dab(W, H, 200, 292, 170, 18, 0, rng, n=14, wob=0.04)
    art = gouache_form(art, plate, "#fbf3e6", "#d9c6ae", seed=sd(), sdx=-.0, sdy=-.25)
    art = ink(art, outline_mask(W, H, ellipse_pts(200, 292, 170, 18, 24), 2.2, rng, breaks=0.05), INK, seed=sd(), alpha=.7)
    # bottom tier
    b_pts = deform(rect_pts(52, 178, 296, 110, 6), rng, 2, 0.006)
    bt = shape_mask(W, H, b_pts, smooth=False)
    art = gouache_form(art, bt, "#f58aa0", "#cf5c7a", seed=sd(), sdx=-.2, sdy=0)
    # drippy cream band
    def drip(cv):
        p = skia.Path(); p.moveTo(50, 176)
        x = 50
        while x < 350:
            dx = rng.uniform(26, 40)
            dep = rng.uniform(12, 30)
            p.quadTo(x + dx * .25, 176 + dep * 1.3, x + dx * .5, 176 + dep)
            p.quadTo(x + dx * .75, 176 + dep * .7, x + dx, 182)
            x += dx
        p.lineTo(350, 172); p.lineTo(50, 172); p.close()
        cv.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    cream = mask_from(W, H, drip)
    art = gouache_form(art, cream, "#fff7ee", "#efd9cf", seed=sd(), sdx=-.1, sdy=-.3)
    # sprinkles on bottom tier
    for i in range(16):
        x, y = rng.uniform(70, 330), rng.uniform(222, 276)
        m = dab(W, H, x, y, 6, 2.6, rng.uniform(0, math.pi), rng, n=8, wob=0.05)
        art = over(art, gouache_paint(m, PAL[ORDER[i % 5]][0], seed=sd(), rough=0.6))
    art = ink(art, outline_mask(W, H, b_pts, 2.8, rng, wob=0.003, breaks=0.04), INK, seed=sd(), alpha=.85)
    # top tier
    t_pts = deform(rect_pts(92, 104, 216, 82, 6), rng, 2, 0.006)
    tt = shape_mask(W, H, t_pts, smooth=False)
    art = gouache_form(art, tt, "#ffe08c", "#e5ad49", seed=sd(), sdx=-.2, sdy=0)
    wave = [(92 + i * 6, 126 + math.sin(i * .62) * 6) for i in range(37)]
    art = over(art, gouache_paint(stroke_mask(W, H, wave, 8, (0.02, 0.02)), "#fff6e8", seed=sd(), rough=1.4))
    for i, x in enumerate(np.linspace(118, 282, 6)):
        m = dab(W, H, x, 160 + (i % 2) * 8, 6, 6, 0, rng)
        art = over(art, gouache_paint(m, PAL[ORDER[(i + 2) % 5]][0], seed=sd(), rough=1))
    art = ink(art, outline_mask(W, H, t_pts, 2.8, rng, wob=0.003, breaks=0.04), INK, seed=sd(), alpha=.85)
    return art


def candle():
    W, H = 30, 92
    rng = random.Random(5)
    art = blank(W, H)
    pts = deform(rect_pts(8, 16, 14, 70, 5), rng, 1, 0.01)
    m = shape_mask(W, H, pts, smooth=False)
    art = gouache_form(art, m, "#fff4e2", "#e1cdb2", seed=sd(), sdx=-.3, sdy=0, rough=1)
    for k in range(5):  # candy stripes
        y = 22 + k * 14
        st = stroke_mask(W, H, [(7, y + 6), (23, y)], 5, (0.05, 0.05)) * m
        art = over(art, gouache_paint(st, "#f0645c", seed=sd(), rough=0.6))
    art = ink(art, outline_mask(W, H, pts, 1.8, rng, wob=0), INK, seed=sd(), alpha=.8)
    wick = stroke_mask(W, H, [(15, 17), (15.5, 9)], 2, (0.1, 0.1))
    art = ink(art, wick, INK, seed=sd(), alpha=.9)
    return art


def flame():
    W, H = 60, 84
    rng = random.Random(8)
    art = blank(W, H)
    halo = dab(W, H, 30, 46, 12, 16, 0, rng)
    art = over(art, glow(halo, "#ffd36b", radius=8, strength=0.35))
    fl = shape_mask(W, H, deform(petal_pts(30, 66, 44, 11, -math.pi / 2, n=16), rng, 1, 0.03))
    art = over(art, gouache_paint(fl, "#f7a531", "#f2742c", seed=sd(), rough=1.2))
    core = shape_mask(W, H, petal_pts(30, 66, 24, 6, -math.pi / 2, n=12))
    art = over(art, gouache_paint(core, "#fff1b0", seed=sd(), rough=0.8))
    return art


def gifts():
    """Scene piece: a little pile of wrapped presents, a party hat and a dropped balloon ribbon."""
    W, H = 640, 400
    rng = random.Random(21)
    art = blank(W, H)
    ground = dab(W, H, 320, 372, 290, 22, 0, rng, n=16, wob=0.05)
    g = gouache_paint(ground, "#e9c79c", seed=sd(), rough=4)
    g[..., 3] *= 0.55
    art = over(art, g)

    def box(x, y, w, h, col, ribbon, lid=True, tilt=0.0):
        nonlocal art
        c, s_, l_ = PAL[col]
        cxm, cym = x + w / 2, y + h / 2
        def rot(p):
            dx, dy = p[0] - cxm, p[1] - cym
            return (cxm + dx * math.cos(tilt) - dy * math.sin(tilt), cym + dx * math.sin(tilt) + dy * math.cos(tilt))
        body = [rot(p) for p in deform(rect_pts(x, y + 18, w, h - 18, 5), rng, 1, 0.006)]
        bm = shape_mask(W, H, body, smooth=False)
        art = gouache_form(art, bm, c, s_, seed=sd(), sdx=-.22, sdy=0)
        vr = [rot(p) for p in rect_pts(cxm - 9, y + 18, 18, h - 18, 2)]
        rm = shape_mask(W, H, vr, smooth=False) * bm
        art = over(art, gouache_paint(rm, ribbon, seed=sd(), rough=1.4))
        art = ink(art, outline_mask(W, H, body, 2.6, rng, wob=0.002, breaks=.04), INK, seed=sd(), alpha=.85)
        if lid:
            lp = [rot(p) for p in deform(rect_pts(x - 8, y, w + 16, 24, 5), rng, 1, 0.006)]
            lm = shape_mask(W, H, lp, smooth=False)
            art = gouache_form(art, lm, mix(c, "#ffffff", .1), s_, seed=sd(), sdx=-.2, sdy=0)
            lr = shape_mask(W, H, [rot(p) for p in rect_pts(cxm - 10, y, 20, 24, 2)], smooth=False) * lm
            art = over(art, gouache_paint(lr, ribbon, seed=sd(), rough=1.4))
            art = ink(art, outline_mask(W, H, lp, 2.4, rng, wob=0.002, breaks=.04), INK, seed=sd(), alpha=.85)
            # bow: two loops
            top = rot((cxm, y))
            for side in (-1, 1):
                lp2 = petal_pts(top[0], top[1] - 2, 40, 16, -math.pi / 2 + side * 0.95, n=14)
                bmk = shape_mask(W, H, lp2)
                art = over(art, gouache_paint(bmk, ribbon, mix(ribbon, INK, .2), seed=sd(), rough=1.6))
                art = ink(art, outline_mask(W, H, lp2, 2.0, rng, wob=0.003), INK, seed=sd(), alpha=.8)
            knot = dab(W, H, top[0], top[1] - 3, 7, 6, 0, rng)
            art = over(art, gouache_paint(knot, mix(ribbon, INK, .25), seed=sd(), rough=1))

    box(84, 196, 170, 170, "grape", "#ffd36a", tilt=-0.03)
    box(360, 238, 150, 128, "mint", "#f58aa0", tilt=0.04)
    box(232, 270, 120, 98, "sun", "#8b79e6", tilt=-0.02)
    # party hat leaning on the right
    hat = deform([(520, 362), (604, 352), (548, 214)], rng, 2, 0.01)
    hm = poly_mask(W, H, hat)
    art = gouache_form(art, hm, "#f0645c", "#c2404a", seed=sd(), sdx=-.2, sdy=0)
    for k in range(4):
        y = 250 + k * 30
        st = stroke_mask(W, H, [(520, y + 20), (610, y - 6)], 8, (0.05, 0.05)) * hm
        art = over(art, gouache_paint(st, "#fff0c4", seed=sd(), rough=1))
    art = ink(art, outline_mask(W, H, hat, 2.6, rng, wob=0.002, breaks=.03), INK, seed=sd(), alpha=.85)
    pom = dab(W, H, 548, 212, 13, 12, 0, rng, n=12, wob=0.2)
    art = over(art, gouache_paint(pom, "#f6c246", "#f59a45", seed=sd(), rough=2.5))
    # curly ribbon on the floor
    rib = [(40 + i * 4.2, 352 - math.sin(i * .45) * 12 - i * .2) for i in range(16)]
    art = ink(art, stroke_mask(W, H, rib, 3.4, (.1, .3)), "#f0645c", seed=sd(), wear=.1, alpha=.9)
    # a few confetti dabs
    for i in range(14):
        x, y = rng.uniform(20, 620), rng.uniform(40, 200)
        if 70 < x < 270 and y > 150:
            continue
        m = dab(W, H, x, y, 7, 3.2, rng.uniform(0, math.pi), rng, n=8, wob=0.05)
        art = over(art, gouache_paint(m, PAL[ORDER[i % 5]][0], seed=sd(), rough=0.8))
    return art


if __name__ == "__main__":
    for i, name in enumerate(ORDER):
        a = balloon(name, i)
        print(name, save_asset(a, f"{D}/balloon-{name}.webp", max_w=150, quality=82))
        if i == 0:
            preview(a, "ub-balloon.png", "#ffe9c7")
    a = bunting(); print("bunting", save_asset(a, f"{D}/bunting.webp", max_w=800, quality=80)); preview(a, "ub-bunting.png", "#ffe9c7")
    a = cake(); print("cake", save_asset(a, f"{D}/cake.webp", max_w=380, quality=82)); preview(a, "ub-cake.png", "#ffe9c7")
    a = candle(); print("candle", save_asset(a, f"{D}/candle.webp", quality=84))
    a = flame(); print("flame", save_asset(a, f"{D}/flame.webp", quality=84))
    a = gifts(); print("gifts", save_asset(a, f"{D}/gifts.webp", max_w=620, quality=80)); preview(a, "ub-gifts.png", "#ffe9c7")
    print("paper", paper_tile(f"{D}/paper.webp", "#fdfbf8", seed=11, fiber=0.9, mottle=0.35))
    report(D)
