"""Angklung Saung — Sundanese open saung: a golden kirai-thatch eave and a lashed bamboo beam from which a row of
dried-bamboo angklung hang (one instrument asset, repeated and swinging in CSS), a misty bamboo grove (rumpun awi)
in wet watercolour below, a woven bilik/sasag twill tile, and a bamboo-leaf twig divider.
Palette: straw bamboo, kirai gold-brown, awi green, wood umber, kabut (mist) blue-grey.
Run: python3 -I angklung-saung.py [part ...]   parts: angklung saung rumpun bilik daun"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t5_lib import *

OUT = outdir("angklung-saung")
PARTS = sys.argv[1:] or ["angklung", "saung", "rumpun", "bilik", "daun"]
STRAW, STRAW_M, STRAW_D, STRAW_H = "#ecd38f", "#c9a457", "#7a5526", "#fcf0c9"
KIRAI, KIRAI_D, KIRAI_L = "#b8853f", "#6d4a22", "#e0b86b"
AWI, AWI_D, AWI_L = "#6f9a4f", "#36592f", "#b9cf86"
RATTAN = "#5a3a1c"


def bamboo_leaf(W, H, x, y, L, ang, w=0.17, cup=0.1):
    return shape_mask(W, H, petal_pts(x, y, L, L * w, ang, n=14, cup=cup))


def angklung():
    W, H = 300, 520
    nx = Seq(11)
    art = blank(W, H)
    # hanging cord (loop to the beam)
    cord = strokes(W, H, [([(150, 4), (146, 30), (128, 66)], 3.2, None), ([(150, 4), (154, 30), (176, 66)], 3.2, None)])
    art = G(art, cord, RATTAN, seed=nx(), density=0.95, edge=0.2, bloom=0, rough=0.4, feather=0.4)
    # frame: posts + top rail
    for x in (44, 256):
        art = bamboo(art, W, H, (x, 62), (x, 474), 21, nx, STRAW, STRAW_M, STRAW_D, nodes=(0.32, 0.7), hi=STRAW_H)
    art = bamboo(art, W, H, (30, 72), (270, 72), 15, nx, STRAW, STRAW_M, STRAW_D, nodes=(0.5,), hi=STRAW_H)
    # sounding tubes: (x, top, bottom, width) — the upper part is cut away leaving the back tongue
    for (x, top, bot, wd) in [(104, 214, 462, 40), (178, 128, 462, 58)]:
        cut = top + (bot - top) * 0.36
        tongue = poly(W, H, [(x - wd * .26, cut + 6), (x - wd * .2, top + wd * .35), (x - wd * .05, top), (x + wd * .1, top + 2), (x + wd * .26, top + wd * .4), (x + wd * .3, cut + 6)], smooth=True)
        art = GP(art, tongue, mix(STRAW, STRAW_M, .4), STRAW_M, seed=nx(), rough=0.8, streak=1.0)
        art = OV(art, tongue * np.clip(side_shade(tongue, (x, top), (x, cut), wd * .6) - .5, 0, 1) * 1.6, lambda mm: rgba(STRAW_D, mm * .45))
        art = bamboo(art, W, H, (x, cut), (x, bot), wd, nx, STRAW, STRAW_M, STRAW_D, nodes=(0.2,), hi=STRAW_H)
        streaks = strokes(W, H, [([(x + dx_, cut + 10), (x + dx_ + 1, bot - 10)], 1.4, (0.2, 0.2)) for dx_ in (-wd * .3, -wd * .12, wd * .18)])
        art = OV(art, streaks * fbm(W, H, nx(), 20, 2), lambda mm: rgba(STRAW_D, mm * .35))
        lip = ell(W, H, x, cut, wd * .5, wd * .17)
        art = GP(art, lip, "#4a2e14", "#6b4520", seed=nx(), rough=0.5, streak=0.4)
        inner = ell(W, H, x + wd * .06, cut + wd * .02, wd * .36, wd * .1)
        art = OV(art, inner, lambda mm: rgba("#2b1a0b", mm * .7))
        # the bottom stub that sits in the base slot
        art = OV(art, rect(W, H, x - wd * .5, bot - 8, x + wd * .5, bot), lambda mm: rgba(STRAW_D, mm * .25))
    # middle rail through the tubes + rattan lashings
    art = bamboo(art, W, H, (36, 372), (264, 372), 12, nx, STRAW, STRAW_M, STRAW_D, hi=STRAW_H)
    lash = []
    for x in (44, 104, 178, 256):
        for k in range(4):
            lash.append(([(x - 11, 364 + k * 4.2), (x + 11, 368 + k * 4.2)], 2.4, None))
        for k in range(3):
            lash.append(([(x - 10, 64 + k * 4.5), (x + 10, 68 + k * 4.5)], 2.0, None)) if x in (44, 256) else None
    art = G(art, strokes(W, H, lash), RATTAN, seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.5, feather=0.4)
    # base tube (front)
    art = bamboo(art, W, H, (18, 472), (282, 472), 34, nx, STRAW, STRAW_M, STRAW_D, nodes=(0.13, 0.87), hi=STRAW_H)
    slots = rect(W, H, 72, 466, 214, 471, 2)
    art = OV(art, slots, lambda mm: rgba(STRAW_D, mm * .5))
    end = ell(W, H, 284, 472, 7, 16)
    art = GP(art, end, "#e7cc86", STRAW_M, seed=nx(), rough=0.4)
    art = OV(art, ring(W, H, 284, 472, 7, 2) * end, lambda mm: rgba(STRAW_D, mm * .6))
    # soft cast shade on the tubes from the rail
    save_prev(art, "angklung", "#f3ead2")
    save(art, f"{OUT}/angklung.webp", max_w=240, quality=84)


def saung():
    W, H = 860, 300
    nx = Seq(31)
    rng = random.Random(4)
    art = blank(W, H)
    # three overlapping thatch tiers, back to front
    for tier, (y0, y1, light, mid) in enumerate([(0, 120, "#a77436", KIRAI_D), (50, 172, KIRAI, "#8d5f2a"), (104, 230, KIRAI_L, KIRAI)]):
        top = [(-10, y0 - 70), (W + 10, y0 - 70)]
        fringe = []
        x = W + 10
        k = 0
        walk = 0.0
        while x > -12:
            k += 1
            walk = walk * 0.85 + rng.uniform(-5, 5)
            if k % 2:
                fringe.append((x, y1 + walk + rng.uniform(2, 12) + (rng.uniform(8, 18) if rng.random() < 0.12 else 0)))
            else:
                fringe.append((x, y1 + walk - rng.uniform(4, 14)))
            x -= rng.uniform(2.5, 9)
        m = poly(W, H, top + fringe)
        art = G(art, m, light, mid, seed=nx(), density=0.95, edge=0.6, bloom=0.2, rough=2.5, feather=0.8)
        # fibre strokes
        fib = []
        for _ in range(820):
            fx = rng.uniform(-10, W + 10)
            fy = y1 - 6 - (y1 - y0 + 10) * rng.random() ** 1.6
            L = rng.uniform(16, 46)
            a = math.pi / 2 + rng.uniform(-0.14, 0.14)
            fib.append(([(fx, fy), (fx + math.cos(a) * L * .5 + rng.uniform(-1, 1), fy + math.sin(a) * L * .5), (fx + math.cos(a) * L, fy + math.sin(a) * L)], rng.uniform(1.0, 2.3), (0.1, 0.5)))
        fm = strokes(W, H, fib) * m
        art = OV(art, fm * (0.4 + 0.6 * fbm(W, H, nx(), 30, 2)), lambda mm: rgba(mix(mid, "#2a1a0a", .45), mm * .6))
        hm = strokes(W, H, fib[::3]) * m
        art = OV(art, hm * (fbm(W, H, nx(), 24, 2) > .5), lambda mm: rgba("#f4d898", mm * .45))
        # shadow under the tier above
        if tier:
            sh = m * np.clip(1 - (yx(W, H)[0] - prev_y1 + 4) / 30, 0, 1) * (yx(W, H)[0] > prev_y1 - 22)
            art = OV(art, gaussian_filter(sh, 2), lambda mm: rgba("#2e1c0a", mm * .6))
        prev_y1 = y1
    # shadow band under the eave on the beam
    beam_y = 252
    art = OV(art, rect(W, H, 0, 220, W, 236) * np.clip(1 - (yx(W, H)[0] - 220) / 18, 0, 1), lambda mm: rgba("#2c1b0c", mm * .35))
    art = bamboo(art, W, H, (-6, beam_y), (W + 6, beam_y), 36, nx, "#cfb46a", "#a9893e", "#5f4219", nodes=(0.18, 0.5, 0.82), hi="#f2e2a6")
    # rattan lashings tying the beam up into the eave every ~140px
    lash = []
    for x in (70, 214, 358, 502, 646, 790):
        for k in range(5):
            lash.append(([(x - 9 + k * 4, 222), (x - 9 + k * 4, beam_y + 18)], 2.6, None))
    art = G(art, strokes(W, H, lash), RATTAN, seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.6, feather=0.4)
    save_prev(art, "saung", "#f3ead2")
    save_full(art, f"{OUT}/saung.webp", size=(860, 300), quality=80)


def rumpun():
    W, H = 860, 640
    nx = Seq(51)
    rng = random.Random(9)
    art = blank(W, H)
    # far stems dissolving in mist
    far = []
    for _ in range(16):
        x = rng.uniform(-20, W + 20)
        far.append(tube_poly((x, H), (x + rng.uniform(-50, 50), -40), rng.uniform(10, 16), rng.uniform(6, 9)))
    art = G(art, shapes(W, H, far, smooth=False), "#c3cfb6", "#a9bba9", seed=nx(), density=0.5, edge=0.4, bloom=0.3, rough=2.0, feather=1.4)
    blobs = [(rng.uniform(0, W), rng.uniform(60, 300), rng.uniform(50, 110), rng.uniform(26, 50), rng.uniform(-15, 15)) for _ in range(18)]
    art = G(art, ellipses(W, H, blobs), "#b5c9a3", "#9ab79e", seed=nx(), density=0.36, edge=0.3, bloom=0.5, rough=6, feather=3)
    clear()
    clumps = [(70, 4, -1), (250, 3, 1), (610, 4, -1), (800, 4, 1)]
    stems = []
    for cx, n, lean in clumps:
        for k in range(n):
            x0 = cx + rng.uniform(-26, 26)
            spread = (k - (n - 1) / 2) * rng.uniform(14, 24) + lean * 30
            stems.append(((x0, H + 10), (x0 + spread * 3.4, rng.uniform(-60, -10)), rng.uniform(16, 24)))
    for (a, b, wd) in stems:
        nodes = tuple(sorted(rng.uniform(0.1, 0.97) for _ in range(5)))
        art = bamboo(art, W, H, a, b, wd, nx, "#a9c27a", AWI, AWI_D, nodes=nodes, medium="water", hi="#e2ecc0")
        clear()
    # drooping leaf sprays from the nodes
    pa, pb, twigs = [], [], []
    for (a, b, wd) in stems:
        for _ in range(rng.randint(2, 4)):
            t = rng.uniform(0.45, 0.95)
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            side = rng.choice([-1, 1])
            ex, ey = px + side * rng.uniform(40, 90), py + rng.uniform(-20, 20)
            twigs.append(([(px, py), ((px + ex) / 2, (py + ey) / 2 - 8), (ex, ey)], 2.2, (0.0, 0.6)))
            for j in range(rng.randint(4, 7)):
                u = 0.3 + 0.7 * j / 6
                lx, ly = px + (ex - px) * u, py + (ey - py) * u - 4 * math.sin(u * math.pi)
                ang = math.pi / 2 + side * rng.uniform(-0.2, 0.9)
                L = rng.uniform(38, 64)
                (pa if rng.random() < 0.45 else pb).append(petal_pts(lx, ly, L, L * 0.14, ang, n=12, cup=0.18))
    art = G(art, strokes(W, H, twigs), "#6d7d3d", seed=nx(), density=0.9, edge=0.3, bloom=0, rough=0.6, feather=0.4)
    art = G(art, shapes(W, H, pb), "#527f3c", AWI_D, seed=nx(), density=0.9, edge=0.6, bloom=0.25, rough=1.2, feather=0.5)
    art = G(art, shapes(W, H, pa), "#a9c66c", "#77a052", seed=nx(), density=0.88, edge=0.55, bloom=0.2, rough=1.1, feather=0.5)
    clear()
    ground = poly(W, H, [(-10, H - 54), (160, H - 70), (360, H - 52), (540, H - 74), (720, H - 56), (W + 10, H - 68), (W + 10, H + 10), (-10, H + 10)], smooth=True)
    art = G(art, ground, "#8aa45c", "#55733a", seed=nx(), density=0.9, edge=0.5, bloom=0.35, rough=4, feather=1.2)
    blades = []
    for _ in range(110):
        x = rng.uniform(0, W); y = H - rng.uniform(30, 74); L = rng.uniform(16, 40); an = -math.pi / 2 + rng.uniform(-0.7, 0.7)
        blades.append(([(x, y + L * .3), (x + math.cos(an) * L * .5, y + math.sin(an) * L * .5), (x + math.cos(an) * L, y + math.sin(an) * L)], rng.uniform(2, 3.6), (0.05, 0.6)))
    art = G(art, strokes(W, H, blades), "#5f8a3e", "#38582a", seed=nx(), density=0.85, edge=0.4, bloom=0.1, rough=1, feather=0.5)
    art[..., 3] *= np.clip((yx(W, H)[0] - 0) / 170, 0, 1) ** 0.8
    save_prev(art, "rumpun", "#efe6cf")
    save(art, f"{OUT}/rumpun.webp", max_w=680, quality=62)


def bilik():
    """Woven bamboo (bilik, 2/2 twill) — seamless 256 tile."""
    W = H = 256
    rng = np.random.default_rng(3)
    s = 16  # strip width; 256/16 = 16 strips -> period divides tile
    yy, xx = yx(W, H)
    i, j = (xx // s).astype(int), (yy // s).astype(int)
    over_h = ((i + j) // 2) % 2 == 0  # 2/2 twill
    u = (xx % s) / s
    v = (yy % s) / s
    tone_h = 0.9 + 0.1 * rng.random(16)[j]
    tone_v = 0.86 + 0.1 * rng.random(16)[i]
    base_h = np.array(hex_rgb("#efdcaa"), np.float32)
    base_v = np.array(hex_rgb("#e2c886"), np.float32)
    fib = wrap_noise(W, H, 4, (0.4, 6))
    fibv = wrap_noise(W, H, 5, (6, 0.4))
    # horizontal strip on top: shaded at its top/bottom edge; vertical: at left/right edge
    edge_h = 1 - 0.28 * (np.abs(v - 0.5) * 2) ** 3
    edge_v = 1 - 0.28 * (np.abs(u - 0.5) * 2) ** 3
    rgb_h = base_h * (tone_h * edge_h * (0.93 + 0.12 * fib))[..., None]
    rgb_v = base_v * (tone_v * edge_v * (0.93 + 0.12 * fibv))[..., None]
    rgb = np.where(over_h[..., None], rgb_h, rgb_v)
    # small shadow where a strip dives under
    gap = ((u < 0.06) | (u > 0.94)) & over_h | ((v < 0.06) | (v > 0.94)) & ~over_h
    rgb = rgb * np.where(gap, 0.82, 1.0)[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_prev(arr, "bilik")
    save_rgb(arr, f"{OUT}/bilik.webp", quality=74)


def daun():
    W, H = 460, 110
    nx = Seq(71)
    rng = random.Random(2)
    art = blank(W, H)
    art = bamboo(art, W, H, (40, 60), (420, 56), 7, nx, "#c7ad62", "#9b7e3a", "#5b4019", nodes=(0.3, 0.5, 0.7), hi="#efdfa6")
    polys_a, polys_b = [], []
    for side, x0 in ((-1, 196), (1, 264)):
        for k in range(7):
            ux = x0 + side * k * 22
            out = (math.pi if side < 0 else 0)
            a = out + side * ((0.55 if k % 2 else -0.5) + rng.uniform(-0.15, 0.15))
            L = rng.uniform(40, 62) * (1 - k * 0.05)
            (polys_a if k % 2 else polys_b).append(petal_pts(ux, 58 + rng.uniform(-2, 2), L, L * .15, a, n=12, cup=0.12))
    art = G(art, shapes(W, H, polys_b), "#5f8f43", AWI_D, seed=nx(), density=0.9, edge=0.55, bloom=0.2, rough=1.0, feather=0.5)
    art = G(art, shapes(W, H, polys_a), "#a5c46b", AWI, seed=nx(), density=0.88, edge=0.5, bloom=0.2, rough=1.0, feather=0.5)
    knot = ell(W, H, 230, 58, 9, 11)
    art = G(art, knot, RATTAN, seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5, feather=0.4)
    save_prev(art, "daun")
    save(art, f"{OUT}/daun.webp", max_w=460, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
