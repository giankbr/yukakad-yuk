"""Wisuda Toga — gouache mortarboard (+ separate foil tassel), foil seal medallion, foil laurel wreath,
gouache diploma scroll, soft-light brush-grain tile for navy panels.
Run: python3 -I /tmp/pen/art/themes/wisuda-toga.py"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _h_common import *

D = outdir("wisuda-toga")
GOLD = "#c8a24a"
NAVY, NAVY_D, NAVY_L = "#2f5289", "#122648", "#5679b0"
MAROON = "#8a1c2b"
sd = Seeds(700)

CW, CH = 300, 230  # mortarboard canvas (2.5x the old 120x92 viewBox) — shared by cap + tassel layers


def save_full(arr, path, quality=84):
    to_image(arr).save(path, "WEBP", quality=quality, method=6)
    return to_image(arr).size


def cap():
    rng = random.Random(3)
    art = blank(CW, CH)
    # skull cap
    sk = [(72, 98)] + [(150 + math.cos(t) * 80, 150 + math.sin(t) * 38) for t in np.linspace(math.pi, 0, 18)][0:1]
    pts = [(72, 98), (70, 150)]
    pts += [(150 - math.cos(t) * 80, 150 + math.sin(t) * 38) for t in np.linspace(0.05, math.pi - 0.05, 20)]
    pts += [(230, 150), (228, 98), (150, 132)]
    pts = deform(pts, rng, 1, 0.004)
    skm = shape_mask(CW, CH, pts, smooth=False)
    art = gouache_form(art, skm, "#203b68", "#0c1b36", seed=sd(), sdx=-.22, sdy=0, rough=2)
    # rim light along the skull's left edge
    rl = stroke_mask(CW, CH, [(74, 104), (73, 150), (92, 172), (120, 183)], 3.2, (.1, .4)) * skm
    r_ = gouache_paint(rl, "#5a79ab", seed=sd(), rough=.8); r_[..., 3] *= .6
    art = over(art, r_)
    # board thickness (darker underside)
    under = deform([(10, 80), (150, 137), (290, 80), (290, 88), (150, 146), (10, 88)], rng, 1, 0.003)
    art = over(art, gouache_paint(poly_mask(CW, CH, under), "#0c1a33", "#162a4d", seed=sd(), rough=1.4))
    # board top face
    top = deform([(150, 22), (290, 78), (150, 136), (10, 78)], rng, 1, 0.004)
    tm = poly_mask(CW, CH, top)
    art = gouache_form(art, tm, NAVY, "#1d3a66", seed=sd(), sdx=-.12, sdy=-.14, rough=2, streak=0.7)
    # soft lit edge on the far (top-left) edge
    hl = stroke_mask(CW, CH, [(16, 78), (84, 50), (150, 25), (210, 48)], 5, (.15, .3)) * tm
    h_ = gouache_paint(hl, "#9db4da", seed=sd(), rough=.6); h_[..., 3] *= .6
    art = over(art, h_)
    # faint stitched inner diamond
    inner = [(150, 40), (250, 78), (150, 118), (50, 78)]
    st = outline_mask(CW, CH, inner, 1.3, rng, wob=0, breaks=0.45)
    s_ = gouache_paint(st, "#8aa2c9", seed=sd(), rough=.2); s_[..., 3] *= .35
    art = over(art, s_)
    # foil button
    art = over(art, foil_matte(dab(CW, CH, 150, 78, 8.5, 6.5, 0, rng), GOLD, seed=sd(), emboss=.8))
    return art


def tassel():
    rng = random.Random(5)
    art = blank(CW, CH)
    cord = curve([(152, 79), (200, 86), (238, 96), (246, 112), (246, 150)], 60)
    art = over(art, foil_matte(stroke_mask(CW, CH, cord, 4.0, (.02, .05)), GOLD, seed=sd(), emboss=.5))
    knot = dab(CW, CH, 246, 154, 7, 7, 0, rng)
    art = over(art, foil_matte(knot, GOLD, seed=sd(), emboss=.7))
    body = deform([(238, 160), (254, 160), (262, 204), (230, 204)], rng, 1, 0.01)
    bm = poly_mask(CW, CH, body)
    art = over(art, gouache_paint(bm, "#d3ad55", "#a8822f", seed=sd(), rough=1.2, streak=1.2))
    for x in np.linspace(233, 259, 8):  # threads
        th = stroke_mask(CW, CH, [(246 + (x - 246) * .45, 162), (x, 205)], 1.3, (.02, .02)) * bm
        art = over(art, gouache_paint(th, "#8a6a26", seed=sd(), rough=.2))
    art = over(art, foil_matte(stroke_mask(CW, CH, [(238, 164), (254, 164)], 4, (.02, .02)), GOLD, seed=sd(), emboss=.5))
    return art


def seal():
    S = 240
    rng = random.Random(9)
    art = blank(S, S)
    c = S / 2
    pts = []
    for i in range(96):
        t = i / 96 * math.tau
        r = 112 + 6 * math.cos(t * 24)
        pts.append((c + math.cos(t) * r, c + math.sin(t) * r))
    rosette = shape_mask(S, S, deform(pts, rng, 1, 0.002))
    art = over(art, foil_matte(rosette, GOLD, seed=sd(), emboss=.8))
    # pressed rings
    for rr, wdt, col, al in [(103, 1.6, "#6e5520", .55), (72, 1.4, "#6e5520", .5)]:
        ring = outline_mask(S, S, ellipse_pts(c, c, rr, rr, 48), wdt, rng, wob=0)
        art = ink(art, ring, col, seed=sd(), wear=.2, alpha=al)
    # navy enamel centre
    cen = shape_mask(S, S, ellipse_pts(c, c, 68, 68, 40))
    art = gouache_form(art, cen, "#13294b", "#0b1a33", seed=sd(), sdx=-.06, sdy=-.06, rough=1.2, streak=.6)
    # foil star
    star = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = 33 if i % 2 == 0 else 14
        star.append((c + math.cos(a) * r, c + 2 + math.sin(a) * r))
    art = over(art, foil_matte(poly_mask(S, S, deform(star, rng, 1, 0.004)), GOLD, seed=sd(), emboss=.7))
    return art


def laurel():
    LW, LH = 460, 270
    rng = random.Random(14)
    art = blank(LW, LH)
    cx, cy, R = 230, 44, 186
    for side in (-1, 1):
        a0, a1 = math.pi / 2 + side * -0.14, (math.pi + 0.22) if side < 0 else (-0.22)
        # sample the arc from bottom towards the tip
        n = 60
        arc = [(cx + math.cos(a0 + (a1 - a0) * i / (n - 1)) * R, cy + math.sin(a0 + (a1 - a0) * i / (n - 1)) * R * 0.98) for i in range(n)]
        art = over(art, foil_matte(stroke_mask(LW, LH, arc, 4.2, (.02, .5)), GOLD, seed=sd(), emboss=.5))
        for k in range(1, 12):
            i = int(k / 12 * (n - 4)) + 2
            (x0, y0), (x1, y1) = arc[i], arc[i + 1]
            tang = math.atan2(y1 - y0, x1 - x0)
            sz = 1.0 - k * 0.035
            for out in (1, -1):
                ang = tang + out * 0.55
                L, Wd = 44 * sz, 9.5 * sz
                lp = petal_pts(x0, y0, L, Wd, ang + rng.uniform(-.08, .08), n=14)
                lm = shape_mask(LW, LH, deform(lp, rng, 1, 0.01))
                art = over(art, foil_matte(lm, rng.choice([GOLD, "#bf973f", "#d1ac55"]), seed=sd(), emboss=.55))
                vein = [(x0, y0), (x0 + math.cos(ang) * L * .82, y0 + math.sin(ang) * L * .82)]
                art = ink(art, stroke_mask(LW, LH, vein, 1.1, (.1, .3)) * lm, "#7a5f22", seed=sd(), alpha=.45)
        tip = arc[-1]
        lm = shape_mask(LW, LH, petal_pts(tip[0], tip[1], 40, 12, math.atan2(arc[-1][1] - arc[-3][1], arc[-1][0] - arc[-3][0]), n=14))
        art = over(art, foil_matte(lm, GOLD, seed=sd(), emboss=.55))
    # maroon ribbon knot at the base
    knot = dab(LW, LH, cx, cy + R - 4, 12, 10, 0, rng)
    for side in (-1, 1):
        loop = petal_pts(cx, cy + R - 4, 30, 12, (math.pi + 0.25) if side < 0 else -0.25, n=14)
        art = over(art, gouache_paint(shape_mask(LW, LH, loop), "#a02536", MAROON, seed=sd(), rough=1))
        tail = deform([(cx - side * 2, cy + R - 2), (cx + side * 20, cy + R + 26), (cx + side * 32, cy + R + 22), (cx + side * 8, cy + R - 4)], rng, 1, 0.01)
        art = over(art, gouache_paint(poly_mask(LW, LH, tail), MAROON, "#6a1420", seed=sd(), rough=1.2))
    art = over(art, gouache_paint(knot, "#a02536", MAROON, seed=sd(), rough=1))
    return art


def diploma():
    DW, DH = 380, 210
    rng = random.Random(21)
    art = blank(DW, DH)
    body = deform(rect_pts(50, 70, 270, 64, 6), rng, 1, 0.003)
    bm = shape_mask(DW, DH, body, smooth=False)
    art = gouache_form(art, bm, "#f4ecd9", "#cbbb98", seed=sd(), sdx=0, sdy=-.35, rough=1.6)
    hi = stroke_mask(DW, DH, [(56, 84), (314, 82)], 5, (.05, .1)) * bm
    h_ = gouache_paint(hi, "#fffaf0", seed=sd(), rough=.5); h_[..., 3] *= .7
    art = over(art, h_)
    for ex in (50, 320):  # rolled ends
        e = dab(DW, DH, ex, 102, 13, 33, 0, rng, n=14, wob=.03)
        art = gouache_form(art, e, "#ece1c8" if ex > 100 else "#e3d6b9", "#b9a780", seed=sd(), sdx=-.25, sdy=-.1, rough=1)
        sp = arc_pts(ex + 1, 103, 7, -1.2, 4.2, 20, 2.2)
        art = ink(art, stroke_mask(DW, DH, sp, 1.6, (.1, .2)), "#9c8a64", seed=sd(), alpha=.7)
    art = ink(art, outline_mask(DW, DH, body, 1.4, rng, wob=0, breaks=.2), "#8f7d58", seed=sd(), alpha=.5)
    # ribbon band + bow + tails
    band = deform(rect_pts(176, 68, 22, 68, 3), rng, 1, 0.01)
    art = gouache_form(art, shape_mask(DW, DH, band, smooth=False), "#a02536", "#5e1019", seed=sd(), sdx=0, sdy=-.3, rough=1)
    for side in (-1, 1):
        loop = petal_pts(187, 100, 46, 20, math.pi / 2 + side * 1.9, n=14)
        art = gouache_form(art, shape_mask(DW, DH, loop), "#a02536", "#6a1420", seed=sd(), sdx=-.2, sdy=-.2, rough=1.2)
        tail = deform([(187, 104), (187 + side * 16, 176), (187 + side * 30, 168), (187 + side * 6, 104)], rng, 1, 0.01)
        art = gouache_form(art, poly_mask(DW, DH, tail), MAROON, "#5e1019", seed=sd(), sdx=-.2, sdy=0, rough=1.2)
    art = over(art, gouache_paint(dab(DW, DH, 187, 102, 9, 8, 0, rng), "#b02d40", "#8a1c2b", seed=sd(), rough=.8))
    # small foil seal on the scroll's right half
    art = over(art, foil_matte(shape_mask(DW, DH, [(272 + math.cos(t) * (13 + 2 * math.cos(t * 12)), 104 + math.sin(t) * (13 + 2 * math.cos(t * 12))) for t in np.linspace(0, math.tau, 48, endpoint=False)]), GOLD, seed=sd(), emboss=.6))
    return art


def grain_tile(path, size=512, seed=31, quality=74):
    """Neutral (mid-grey) gouache brush grain for `background-blend-mode: soft-light` over navy."""
    rng = np.random.default_rng(seed)
    big = size * 2
    st = gaussian_filter(rng.random((big, big)).astype(np.float32), (1.0, 14))
    st = (st - st.mean()) / (st.std() + 1e-6)
    fine = gaussian_filter(rng.random((big, big)).astype(np.float32), 0.7)
    fine = (fine - fine.mean()) / (fine.std() + 1e-6)
    mot = gaussian_filter(rng.random((big, big)).astype(np.float32), 50)
    mot = (mot - mot.mean()) / (mot.std() + 1e-6)
    v = 0.5 + st * 0.016 + fine * 0.014 + mot * 0.02
    a = v[:size, :size]
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    wgt = np.clip(np.minimum(np.minimum(xx, 1 - xx), np.minimum(yy, 1 - yy)) * 6, 0, 1)
    t = a * wgt + np.roll(np.roll(a, size // 2, 0), size // 2, 1) * (1 - wgt)
    Image.fromarray((np.clip(t, 0, 1) * 255).astype(np.uint8), "L").convert("RGB").save(path, "WEBP", quality=quality, method=6)
    return os.path.getsize(path)


if __name__ == "__main__":
    c, t = cap(), tassel()
    print("cap", save_full(c, f"{D}/cap.webp")); print("tassel", save_full(t, f"{D}/tassel.webp"))
    navy = np.ones((CH, CW, 4), np.float32); navy[..., :3] = np.array(hex_rgb("#13294b"))
    to_image(over(over(navy, c), t)).save(f"{PREV_ROOT}/wt-cap.png")
    s_ = seal(); print("seal", save_asset(s_, f"{D}/seal.webp", quality=84))
    to_image(over(np.concatenate([np.ones((240, 240, 3), np.float32) * .96, np.ones((240, 240, 1), np.float32)], -1), s_)).save(f"{PREV_ROOT}/wt-seal.png")
    l = laurel(); print("laurel", save_asset(l, f"{D}/laurel.webp", max_w=420, quality=82))
    nv = np.ones(l.shape, np.float32); nv[..., :3] = np.array(hex_rgb("#13294b"))
    to_image(over(nv, l)).save(f"{PREV_ROOT}/wt-laurel.png")
    d = diploma(); print("diploma", save_asset(d, f"{D}/diploma.webp", max_w=340, quality=82)); preview(d, "wt-diploma.png", "#ffffff")
    print("grain", grain_tile(f"{D}/grain.webp"))
    report(D)
