"""Marketplace — gouache + ink product 'photos' for the wishlist cards (espresso machine, folded sheets, ceramic pot set),
each sitting on a soft watercolour cast shadow like a studio product shot. UI stays UI.
Run: python3 -I /tmp/pen/art/themes/marketplace.py"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p4_lib import *  # noqa

T = "marketplace"
D = outdir(T)
PREV = "/tmp/pen/nt3-R3"
os.makedirs(PREV, exist_ok=True)
nxt = Seeds(900)
rng = random.Random(23)
INK = "#2a2522"
S = 240


def gp(mask, c1, c2=None, rough=1.6, streak=0.5, density=0.97):
    return gouache_paint(mask, c1, c2, seed=nxt(), rough=rough, streak=streak, density=density)


def inkline(masks, widths):
    m = union(*[outline(mk, w) for mk, w in zip(masks, widths)])
    return pigment(m, INK, seed=nxt(), density=0.72, edge=0.1, bloom=0, feather=0.4, rough=0.8, holes=0.12)


def cast_shadow(cx, cy, rx, ry, col="#8a7f74"):
    m = shape_mask(S, S, deform(ellipse_pts(cx, cy, rx, ry, 14), rng, 2, .03))
    return pigment(gaussian_filter(m, 4), col, seed=nxt(), density=0.32, edge=0.25, bloom=0.2, gran=0.3, feather=2.0, rough=4)


def hilite(mask_pts, a=0.55):
    return gp(shape_mask(S, S, mask_pts), "#ffffff", rough=0.6, density=a)


def espresso():
    art = blank(S, S)
    art = glaze(art, cast_shadow(120, 196, 92, 12))
    body = shape_mask(S, S, wobble_rect(56, 50, 128, 124, rng, 1.8))
    top = shape_mask(S, S, wobble_rect(50, 40, 140, 18, rng, 1.2))
    face = shape_mask(S, S, wobble_rect(68, 66, 104, 26, rng, 1.0))
    drip = shape_mask(S, S, wobble_rect(66, 166, 108, 14, rng, 1.0))
    group = shape_mask(S, S, deform([(96, 92), (144, 92), (140, 106), (100, 106)], rng, 1, .02))
    handle = stroke_mask(S, S, [(140, 100), (168, 106), (198, 112)], 12, (0.05, 0.2))
    cup = shape_mask(S, S, deform([(102, 136), (138, 136), (134, 164), (106, 164)], rng, 1, .02))
    cup_h = sub(shape_mask(S, S, ellipse_pts(140, 148, 9, 8, 14)), shape_mask(S, S, ellipse_pts(140, 148, 4, 4, 12)))
    gauge = dots_mask(S, S, [(86, 79, 8)])
    gauge_in = dots_mask(S, S, [(86, 79, 5)])
    btns = dots_mask(S, S, [(118, 79, 4.5), (132, 79, 4.5), (146, 79, 4.5)])
    wand = stroke_mask(S, S, [(176, 92), (182, 120), (178, 146)], 4, (0.05, 0.3))
    art = over(art, gp(body, "#c8432f", "#b23726"))
    art = over(art, gp(top, "#d9d4ca", "#c6c0b4", rough=1.0))
    art = over(art, gp(face, "#e9e4da", "#d8d2c5", rough=0.9))
    bay = shape_mask(S, S, wobble_rect(88, 98, 66, 70, rng, 1.0))
    art = over(art, gp(bay, "#6e2a1f", "#5a2219", rough=0.8))
    art = over(art, gp(drip, "#8d8a85", "#76736f", rough=0.9))
    art = over(art, gp(wand, "#b9b6b0", rough=0.6))
    art = over(art, gp(handle, "#2f2b28", rough=0.6))
    art = over(art, gp(group, "#c9c6c0", "#a9a6a0", rough=0.8))
    art = over(art, gp(gauge, "#f6f1e6", rough=0.5))
    art = over(art, gp(gauge_in, "#fbf7ee", rough=0.4))
    art = over(art, gp(stroke_mask(S, S, [(86, 79), (90, 75)], 1.6, (0.1, 0.1)), "#c8432f", rough=0.3))
    art = over(art, gp(btns, "#3a3532", rough=0.4))
    art = over(art, gp(cup, "#fbf7ef", "#eee6d8", rough=0.8))
    art = over(art, gp(cup_h, "#fbf7ef", rough=0.5))
    art = over(art, gp(shape_mask(S, S, [(104, 136), (136, 136), (135, 142), (105, 142)]), "#5b3520", rough=0.5, density=0.85))
    art = over(art, hilite([(62, 58), (70, 58), (70, 160), (62, 160)], 0.22))
    art = over(art, inkline([union(body, top), face, drip, cup, cup_h, group, gauge], [2.6, 1.8, 1.8, 1.8, 1.4, 1.6, 1.4]))
    steam = union(stroke_mask(S, S, curve([(112, 130), (108, 120), (114, 112), (110, 104)], 20), 2.0),
                  stroke_mask(S, S, curve([(126, 130), (130, 120), (124, 112), (128, 106)], 20), 2.0))
    art = over(art, pigment(steam, "#9a908a", seed=nxt(), density=0.4, edge=0, bloom=0, feather=0.7, rough=0.6))
    return art


def sheets():
    art = blank(S, S)
    art = glaze(art, cast_shadow(120, 190, 96, 13))
    cols = [("#2e9a6a", "#25855b"), ("#f3efe4", "#e6dfcf"), ("#8fd0b0", "#7cc2a0"), ("#e8e1d0", "#d9d0bc")]
    ys = [148, 118, 90, 64]
    layers = []
    for i, ((c1, c2), y) in enumerate(zip(cols, ys)):
        dx = rng.uniform(-5, 5)
        m = shape_mask(S, S, deform([(36 + dx, y), (204 + dx, y + 2), (206 + dx, y + 30), (34 + dx, y + 32)], rng, 2, .01))
        layers.append(m)
        art = knockout(art, m, 1.0, 0.6)
        art = over(art, gp(m, c1, c2, rough=1.4))
        # folded edge shading along the front
        fold = shape_mask(S, S, [(36 + dx, y + 22), (206 + dx, y + 22), (206 + dx, y + 30), (34 + dx, y + 32)])
        art = over(art, gp(fold * m, mix(c1, "#000000", .14), rough=0.5, density=0.55))
        art = over(art, gp(shape_mask(S, S, [(44 + dx, y + 5), (196 + dx, y + 6), (196 + dx, y + 9), (44 + dx, y + 8)]), "#ffffff", rough=0.4, density=0.28))
    # stitched hem on the green sheet + ribbon band around the stack
    hem = stroke_mask(S, S, [(44, 170), (200, 172)], 1.2, (0.02, 0.02))
    hem *= (np.arange(S)[None, :] // 6 % 2).astype(np.float32)
    art = over(art, gp(hem, "#e9f5ee", rough=0.2, density=0.8))
    band = shape_mask(S, S, deform([(150, 60), (170, 60), (172, 182), (148, 182)], rng, 1, .01))
    art = over(art, gp(band, "#d8b26a", "#c79f55", rough=0.8))
    tag = shape_mask(S, S, deform([(144, 96), (176, 96), (176, 118), (144, 118)], rng, 1, .02))
    art = over(art, gp(tag, "#fffaf0", rough=0.6))
    art = over(art, gp(stroke_mask(S, S, [(150, 104), (170, 104)], 1.6, (0.1, 0.1)), "#2e9a6a", rough=0.3, density=0.8))
    art = over(art, gp(stroke_mask(S, S, [(150, 110), (164, 110)], 1.6, (0.1, 0.1)), "#2e9a6a", rough=0.3, density=0.6))
    art = over(art, inkline(layers + [band, tag], [2.0, 2.0, 2.0, 2.0, 1.4, 1.4]))
    return art


def pots():
    art = blank(S, S)
    art = glaze(art, cast_shadow(120, 194, 100, 13))
    # big casserole (back, left)
    pot = shape_mask(S, S, deform([(28, 104), (148, 104), (144, 178), (122, 188), (54, 188), (32, 178)], rng, 2, .01))
    rim = shape_mask(S, S, deform(ellipse_pts(88, 104, 64, 9, 18), rng, 1, .01))
    lid = shape_mask(S, S, deform(arc_pts(88, 102, 60, math.pi, math.tau, 20, 0.42) + [(148, 102), (28, 102)], rng, 1, .008))
    knob = shape_mask(S, S, deform(ellipse_pts(88, 74, 12, 7, 14), rng, 1, .02))
    ears = union(shape_mask(S, S, ellipse_pts(24, 128, 9, 6, 14)), shape_mask(S, S, ellipse_pts(152, 128, 9, 6, 14)))
    band = shape_mask(S, S, deform([(32, 136), (146, 136), (146, 146), (32, 146)], rng, 1, .01)) * pot
    art = over(art, gp(ears, "#b5523c", rough=0.8))
    art = over(art, gp(pot, "#d8664a", "#c25640"))
    art = over(art, gp(band, "#f3e3cf", rough=0.5, density=0.9))
    dots = dots_mask(S, S, [(42 + i * 14, 141, 2.2) for i in range(8)]) * pot
    art = over(art, gp(dots, "#d8664a", rough=0.3))
    art = over(art, gp(rim, "#a8452f", rough=0.6))
    art = over(art, gp(lid, "#e07558", "#cc6247", rough=1.0))
    art = over(art, gp(knob, "#f3e3cf", "#e6d1b8", rough=0.6))
    art = over(art, hilite([(42, 112), (50, 112), (52, 170), (44, 168)], 0.25))
    art = over(art, hilite([(56, 92), (92, 84), (92, 88), (60, 96)], 0.3))
    # small saucepan (front, right) with long handle
    sp = shape_mask(S, S, deform([(126, 138), (196, 138), (194, 186), (182, 194), (140, 194), (128, 186)], rng, 2, .01))
    sp_rim = shape_mask(S, S, deform(ellipse_pts(161, 138, 36, 6, 16), rng, 1, .01))
    sp_h = stroke_mask(S, S, [(194, 146), (214, 136), (230, 128)], 11, (0.05, 0.1))
    art = knockout(art, union(sp, sp_rim), 1.0, 1.0)
    art = over(art, gp(sp_h, "#6b4a2e", "#5a3c24", rough=0.6))
    art = over(art, gp(sp, "#f1e6d4", "#e2d3bc"))
    art = over(art, gp(sp_rim, "#d8664a", rough=0.5))
    art = over(art, gp(shape_mask(S, S, deform([(126, 150), (196, 150), (196, 156), (126, 156)], rng, 1, .01)) * sp, "#d8664a", rough=0.4, density=0.85))
    art = over(art, hilite([(136, 160), (142, 160), (144, 186), (138, 184)], 0.3))
    art = over(art, inkline([union(pot, lid, ears), knob, rim, union(sp, sp_rim), sp_h], [2.4, 1.6, 1.4, 2.2, 1.6]))
    return art


def main():
    out = {"espresso": espresso(), "sprei": sheets(), "panci": pots()}
    sheet = Image.new("RGB", (S * 3, S), "#ffffff")
    for i, (k, a) in enumerate(out.items()):
        save(a, f"{D}/p-{k}.webp", max_w=200, q=84, trim=False)
        sheet.paste(to_image(a), (i * S, 0), to_image(a))
    sheet.save(f"{PREV}/mp-products.png")


if __name__ == "__main__":
    main()
