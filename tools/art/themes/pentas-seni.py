"""Pentas Seni — undangan pentas seni sekolah: panggung aula sekolah dalam gouache (tirai toska diikat pita kuning,
valans koral berumbai, lampu sorot, bendera segitiga), tiga murid tampil (penari berselendang, pemain angklung,
paduan suara), gambar krayon anak-anak, dan properti musik & tari.
Run: python3 -I pentas-seni.py [part ...]
parts: panggung matahari pelangi rumah angklung rebana kipas bintang bendera   Assets -> public/themes/art/pentas-seni/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n5_lib import *
import random

OUT = outdir("pentas-seni")
PARTS = sys.argv[1:] or ["panggung", "matahari", "pelangi", "rumah", "angklung", "rebana", "kipas", "bintang", "bendera"]
TEAL, TEAL_D, TEAL_L = "#2a8c8c", "#1b5f66", "#46aaa4"
MUST, MUST_D = "#eaa93a", "#c4801f"
CORAL, CORAL_D = "#e2574c", "#b63b36"
CREAM = "#fbf3e1"
WOOD, WOOD_D = "#cc8c4c", "#9a6232"
NAVY = "#233a5e"
PINK = "#ef8aa0"
INKC = "#2b2230"

_c = [1000]


def nx():
    _c[0] += 17
    return _c[0]


def P(dst, mask, col, col2=None, rough=2.2, streak=0.5):
    return GP(dst, mask, col, col2, seed=nx(), rough=rough, streak=streak)


def outline(dst, mask, col=INKC, px=1.4, alpha=0.75):
    return K(dst, outline_of(mask, px), col, seed=nx(), alpha=alpha)


# ---------------------------------------------------------------- props (used in the scene and as small assets)
def angklung_masks(W, H, x, y, s):
    """Angklung (bamboo shaken instrument): frame of two posts + bars, two tubes of different heights."""
    frame = strokes(W, H, [([(x - s * 0.5, y), (x - s * 0.5, y - s * 1.5)], s * 0.09, None),
                           ([(x + s * 0.5, y), (x + s * 0.5, y - s * 1.5)], s * 0.09, None),
                           ([(x - s * 0.58, y - s * 1.45), (x + s * 0.58, y - s * 1.45)], s * 0.08, None),
                           ([(x - s * 0.55, y - s * 0.62), (x + s * 0.55, y - s * 0.62)], s * 0.07, None),
                           ([(x - s * 0.6, y), (x + s * 0.6, y)], s * 0.14, None)])
    tubes = shapes(W, H, [[(x - s * 0.36, y - s * 0.08), (x - s * 0.36, y - s * 1.22), (x - s * 0.06, y - s * 1.34), (x - s * 0.06, y - s * 0.08)],
                          [(x + s * 0.06, y - s * 0.08), (x + s * 0.06, y - s * 0.95), (x + s * 0.34, y - s * 1.04), (x + s * 0.34, y - s * 0.08)]], smooth=False)
    return frame, tubes


def paint_angklung(art, W, H, x, y, s):
    frame, tubes = angklung_masks(W, H, x, y, s)
    art = P(art, tubes, "#e7c27a", "#d4a24f")
    art = G(art, strokes(W, H, [([(x - s * 0.21, y - s * 0.2), (x - s * 0.21, y - s * 1.1)], s * 0.05, None), ([(x + s * 0.2, y - s * 0.2), (x + s * 0.2, y - s * 0.86)], s * 0.05, None)]), "#a87532", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=0.6, feather=0.6)
    art = P(art, frame, "#b98443", "#8f5e2b")
    art = outline(art, np.maximum(frame, tubes), px=1.1, alpha=0.6)
    return art


def paint_rebana(art, W, H, x, y, r):
    rim = ring_mask(W, H, x, y, r * 0.92, r * 0.22)
    skin = circles(W, H, [(x, y, r * 0.82)])
    art = P(art, skin, "#f3dcae", "#e8c78c")
    art = P(art, rim, "#c0702f", "#9a5524")
    jingles = circles(W, H, [(x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92, r * 0.13) for a in np.linspace(0, math.tau, 6, endpoint=False) + 0.3])
    art = FO(art, jingles, "#d8b25a", seed=nx(), emboss=0.6, sparkle=0.05)
    art = outline(art, np.maximum.reduce([rim, skin, jingles]), px=1.1, alpha=0.6)
    return art


def paint_kipas(art, W, H, x, y, r, a0=-2.6, a1=-0.5, col=CORAL, col2=MUST):
    """Folding dance fan (kipas) opened as a half disc with alternating pleats."""
    n = 9
    for i in range(n):
        t0 = a0 + (a1 - a0) * i / n; t1 = a0 + (a1 - a0) * (i + 1) / n
        poly = [(x, y)] + [(x + math.cos(t0 + (t1 - t0) * k / 6) * r, y + math.sin(t0 + (t1 - t0) * k / 6) * r) for k in range(7)]
        art = P(art, shapes(W, H, [poly], smooth=False), col if i % 2 == 0 else col2)
    edge = strokes(W, H, [(arc_pts(x, y, r * 0.97, a0, a1, 30), r * 0.05, None)])
    art = P(art, edge, "#fbf3e1")
    art = P(art, strokes(W, H, [([(x, y), (x + math.cos((a0 + a1) / 2 + math.pi) * r * 0.25, y + math.sin((a0 + a1) / 2 + math.pi) * r * 0.25)], r * 0.08, None)]), "#8f5e2b")
    fan = shapes(W, H, [[(x, y)] + arc_pts(x, y, r, a0, a1, 30)], smooth=False)
    return outline(art, fan, px=1.1, alpha=0.55)


# ---------------------------------------------------------------- a performing child (stylised, friendly)
def kid(art, W, H, x, feet, h, skin, hair, outfit, outfit2, pose="dance", girl=True, prop=None):
    r = h * 0.125
    hy = feet - h + r
    ny = hy + r * 0.95
    sy = ny + h * 0.04
    hip = feet - h * 0.42
    hem = feet - h * 0.2 if girl else hip + h * 0.04
    sw = h * 0.1
    if pose == "dance":
        hands = [(x - h * 0.36, sy - h * 0.16), (x + h * 0.34, sy - h * 0.02)]
    elif pose == "angklung":
        hands = [(x - h * 0.1, sy + h * 0.2), (x + h * 0.12, sy + h * 0.2)]
    else:
        hands = [(x - h * 0.08, sy + h * 0.17), (x + h * 0.09, sy + h * 0.17)]
    if pose == "dance":  # selendang behind: draped from the raised hand, looping behind the waist to the other hand
        sl = curve([hands[0], (x - h * 0.3, sy + h * 0.2), (x, hip + h * 0.05), (x + h * 0.28, sy + h * 0.22), hands[1], (x + h * 0.46, sy + h * 0.16)], 60)
        art = P(art, strokes(W, H, [(sl, h * 0.045, (0.05, 0.1))]), MUST, "#f2c35c")
    legs = strokes(W, H, [([(x - sw * 0.35, hip), (x - sw * 0.42, feet - h * 0.03)], h * 0.055, None), ([(x + sw * 0.35, hip), (x + sw * 0.45, feet - h * 0.03)], h * 0.055, None)])
    art = P(art, legs, skin if girl else "#3a3f5c", None)
    shoes = ellipses(W, H, [(x - sw * 0.5, feet - h * 0.02, h * 0.05, h * 0.026, 0), (x + sw * 0.55, feet - h * 0.02, h * 0.05, h * 0.026, 0)])
    art = P(art, shoes, "#2b2230")
    arms = strokes(W, H, [([(x - sw * 0.85, sy + h * 0.02), ((x - sw * 0.85 + hands[0][0]) / 2 - h * 0.03, (sy + hands[0][1]) / 2 + h * 0.03), hands[0]], h * 0.05, None),
                          ([(x + sw * 0.85, sy + h * 0.02), ((x + sw * 0.85 + hands[1][0]) / 2 + h * 0.03, (sy + hands[1][1]) / 2 + h * 0.03), hands[1]], h * 0.05, None)])
    art = P(art, arms, outfit if pose != "dance" else skin, None)
    body = [(x - sw, sy), (x + sw, sy), (x + (h * 0.2 if girl else sw * 1.05), hem), (x - (h * 0.2 if girl else sw * 1.05), hem)]
    bm = shapes(W, H, [body], smooth=False)
    bm = np.maximum(bm, ellipses(W, H, [(x, sy + h * 0.01, sw * 1.02, h * 0.035, 0)]))
    art = P(art, bm, outfit, outfit2)
    if girl:  # waist sash
        art = P(art, strokes(W, H, [([(x - sw * 1.15, hip - h * 0.02), (x + sw * 1.15, hip - h * 0.02)], h * 0.04, None)]), MUST if outfit != MUST else CORAL)
    else:  # batik dots on the shirt + trousers
        art = P(art, shapes(W, H, [[(x - sw, hem - 2), (x + sw, hem - 2), (x + sw * 0.95, feet - h * 0.2), (x - sw * 0.95, feet - h * 0.2)]], smooth=False), "#3a3f5c")
        art = P(art, circles(W, H, [(x + dx * sw * 0.45, sy + dy * h * 0.06, h * 0.012) for dx in (-1, 0, 1) for dy in (1, 2, 3)]), "#f2c35c")
    art = outline(art, np.maximum(bm, arms), px=1.2, alpha=0.5)
    handsm = circles(W, H, [(hx, hy_, h * 0.03) for hx, hy_ in hands])
    art = P(art, handsm, skin)
    neck = strokes(W, H, [([(x, hy + r * 0.6), (x, sy + 1)], h * 0.04, None)])
    art = P(art, neck, skin)
    head = ellipses(W, H, [(x, hy, r * 0.96, r, 0)])
    art = P(art, head, skin, None, rough=1.4)
    # hair
    hm = ellipses(W, H, [(x, hy - r * 0.32, r * 1.04, r * 0.76, 0)])
    hm = np.clip(hm - ellipses(W, H, [(x + r * 0.1, hy + r * 0.25, r * 0.92, r * 0.72, 0)]) * (1.0 if girl else 1.0), 0, 1)
    if girl:
        hm = np.maximum(hm, circles(W, H, [(x, hy - r * 1.05, r * 0.42)]))
        art = P(art, circles(W, H, [(x + r * 0.55, hy - r * 0.8, r * 0.2)]), PINK)
    art = P(art, hm, hair, None, rough=1.4)
    art = outline(art, np.maximum(head, hm), px=1.1, alpha=0.45)
    # face: closed happy eyes, rosy cheeks, smile (or singing mouth)
    eyes = strokes(W, H, [(arc_pts(x + sx * r * 0.36, hy + r * 0.1, r * 0.13, math.pi * 1.1, math.pi * 1.9, 8), max(1.2, r * 0.07), None) for sx in (-1, 1)])
    art = K(art, eyes, INKC, seed=nx(), alpha=0.85)
    art = G(art, circles(W, H, [(x + sx * r * 0.55, hy + r * 0.38, r * 0.16) for sx in (-1, 1)]), "#ee8a86", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1, feather=1.2)
    if pose == "sing":
        art = P(art, ellipses(W, H, [(x, hy + r * 0.52, r * 0.13, r * 0.17, 0)]), "#9b2f3a")
    else:
        art = K(art, strokes(W, H, [(arc_pts(x, hy + r * 0.3, r * 0.3, 0.35, math.pi - 0.35, 10), max(1.2, r * 0.07), None)]), "#8e2f38", seed=nx(), alpha=0.85)
    if pose == "angklung":
        art = paint_angklung(art, W, H, x, sy + h * 0.33, h * 0.17)
    if pose == "sing":
        folder = shapes(W, H, [[(x - h * 0.13, sy + h * 0.1), (x + h * 0.13, sy + h * 0.08), (x + h * 0.14, sy + h * 0.26), (x - h * 0.12, sy + h * 0.28)]], smooth=False)
        art = P(art, folder, CORAL, CORAL_D)
        art = outline(art, folder, px=1.0, alpha=0.5)
        art = P(art, circles(W, H, [(hx, hy_, h * 0.03) for hx, hy_ in hands]), skin)
    return art


# ---------------------------------------------------------------- the stage
def panggung():
    W, H = 800, 700
    art = blank(W, H)
    top, floor_y, front = 92, 540, 610
    # back wall: dark teal, lighter where the spots fall
    wall = shapes(W, H, [[(60, 44), (740, 44), (740, floor_y), (60, floor_y)]], smooth=False)
    art = P(art, wall, "#1d4f58", "#163f47", streak=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    pool = np.exp(-(((xx - 400) / 230) ** 2 + ((yy - 470) / 120) ** 2))
    art = over(art, rgba(flat(H, W, "#fff1b8"), pool * wall * 0.28))
    # hanging paper stars on strings (the kids' craft decoration)
    rng = random.Random(5)
    for sx, sy_, rr, col in ((180, 210, 20, MUST), (300, 170, 15, "#fbf3e1"), (520, 180, 17, PINK), (630, 220, 21, MUST), (420, 150, 13, TEAL_L)):
        art = K(art, strokes(W, H, [([(sx, top), (sx, sy_ - rr)], 1.4, None)]), "#c9c1a8", seed=nx(), alpha=0.7)
        star = [(sx + math.cos(-math.pi / 2 + k * math.pi / 5) * (rr if k % 2 == 0 else rr * 0.45), sy_ + math.sin(-math.pi / 2 + k * math.pi / 5) * (rr if k % 2 == 0 else rr * 0.45)) for k in range(10)]
        art = P(art, shapes(W, H, [star], smooth=False), col)
    # spotlight cones from the top corners
    for lx, tx in ((120, 330), (680, 470)):
        cone = shapes(W, H, [[(lx - 8, top + 4), (lx + 8, top + 4), (tx + 120, floor_y + 20), (tx - 120, floor_y + 20)]], smooth=False)
        art = over(art, rgba(flat(H, W, "#fff3c4"), gaussian_filter(cone, 14) * 0.2))
    # stage floor (planks) and the front apron
    fl = shapes(W, H, [[(60, floor_y), (740, floor_y), (790, front), (10, front)]], smooth=False)
    art = P(art, fl, WOOD, "#d89c5c")
    planks = strokes(W, H, [([(60 + (i / 10) * 680, floor_y), (10 + (i / 10) * 780, front)], 1.6, None) for i in range(1, 10)])
    art = K(art, planks * fl, WOOD_D, seed=nx(), alpha=0.5)
    art = over(art, rgba(flat(H, W, "#fff1b8"), np.exp(-(((xx - 400) / 210) ** 2 + ((yy - 575) / 40) ** 2)) * fl * 0.4))
    apron = shapes(W, H, [[(10, front), (790, front), (790, 660), (10, 660)]], smooth=False)
    art = P(art, apron, "#7c4a26", "#6a3d1f")
    lights = circles(W, H, [(80 + i * 80, 633, 9) for i in range(9)])
    art = over(art, glow(lights, "#ffe08a", radius=8, strength=0.7))
    art = P(art, lights, "#ffe9a8")
    # the three performers
    art = kid(art, W, H, 255, 588, 210, "#c98e64", "#2b1d17", TEAL_L, TEAL, pose="angklung", girl=False)
    art = kid(art, W, H, 405, 572, 236, "#b97a52", "#22160f", CORAL, CORAL_D, pose="dance", girl=True)
    art = kid(art, W, H, 555, 590, 206, "#d9a479", "#3b2618", "#f2c35c", MUST_D, pose="sing", girl=True)
    clear()
    # side curtains: toska with folds, gathered by yellow ties
    for sd in (-1, 1):
        cx0 = 400 + sd * 400
        inner = 400 + sd * 250
        pts = [(cx0, 40), (inner, 40)] + [(inner + sd * (40 * math.sin(t * math.pi) + 10 * t), 40 + t * (floor_y + 40)) for t in np.linspace(0, 1, 20)][1:] + [(cx0, floor_y + 80)]
        if sd < 0:
            pts = [(0, 40), (150, 40), (165, 200), (135, 330), (175, 470), (150, 620), (0, 620)]
        else:
            pts = [(800, 40), (650, 40), (635, 200), (665, 330), (625, 470), (650, 620), (800, 620)]
        cm = shapes(W, H, [pts])
        art = P(art, cm, TEAL, TEAL_D, streak=0.9)
        folds = strokes(W, H, [([(x0, 40), (x0 + sd * rng.uniform(-6, 6), 330), (x0 + sd * rng.uniform(-12, 12), 620)], rng.uniform(6, 11), (0.0, 0.0)) for x0 in (np.linspace(14, 130, 5) if sd < 0 else np.linspace(670, 786, 5))])
        art = G(art, folds * cm, TEAL_D, seed=nx(), density=0.6, edge=0.3, bloom=0, rough=2, feather=3)
        hi = strokes(W, H, [([(x0, 40), (x0, 620)], 4, None) for x0 in (np.linspace(30, 140, 4) if sd < 0 else np.linspace(660, 770, 4))])
        art = G(art, hi * cm, TEAL_L, seed=nx(), density=0.35, edge=0.1, bloom=0, rough=2, feather=2)
        art = outline(art, cm, px=1.3, alpha=0.5)
        tie_y = 350
        ix = 150 if sd < 0 else 650
        ox = 0 if sd < 0 else 800
        tie = strokes(W, H, [([(ox, tie_y - 14), ((ox + ix) / 2, tie_y + 4), (ix + sd * -4, tie_y + 2)], 13, None)])
        art = P(art, tie, MUST, MUST_D)
        art = outline(art, tie, px=1.1, alpha=0.45)
        knot = circles(W, H, [(ix - sd * 2, tie_y + 2, 10)])
        tassel = shapes(W, H, [[(ix - sd * 2 - 6, tie_y + 8), (ix - sd * 2 + 6, tie_y + 8), (ix - sd * 2 + 11, tie_y + 52), (ix - sd * 2 - 11, tie_y + 52)]], smooth=False)
        art = P(art, np.maximum(knot, tassel), "#f6c65a", MUST_D)
        art = K(art, strokes(W, H, [([(ix - sd * 2 + d, tie_y + 22), (ix - sd * 2 + d * 1.6, tie_y + 50)], 1.2, None) for d in (-5, 0, 5)]), MUST_D, seed=nx(), alpha=0.6)
    # proscenium beam + scalloped coral valance with yellow tassels
    beam = shapes(W, H, [[(0, 0), (800, 0), (800, 52), (0, 52)]], smooth=False)
    art = P(art, beam, MUST, MUST_D)
    val = [(0, 40), (800, 40)]
    sc = []
    for i in range(10):
        x0 = i * 80
        sc += [(x0 + 80 - k * 8, 40 + 40 * math.sin(math.pi * (10 - k) / 10)) for k in range(11)]
    vm = shapes(W, H, [[(0, 38), (800, 38)] + sc[::-1][::-1][::-1]], smooth=True) if False else shapes(W, H, [[(0, 38), (800, 38), (800, 46)] + [(800 - i * 8, 46 + 40 * abs(math.sin(math.pi * (i % 10) / 10))) for i in range(101)] + [(0, 46)]])
    art = P(art, vm, CORAL, CORAL_D)
    art = outline(art, vm, px=1.3, alpha=0.5)
    tas = strokes(W, H, [([(i * 80, 48), (i * 80, 72)], 6, (0.0, 0.5)) for i in range(1, 10)])
    art = P(art, np.maximum(tas, circles(W, H, [(i * 80, 48, 6) for i in range(1, 10)])), "#f6c65a")
    # bunting across the top of the beam
    flags = []
    for i in range(14):
        x0 = 10 + i * 56
        flags.append(([(x0, 8 + 6 * math.sin(i)), (x0 + 50, 8 + 6 * math.sin(i + 1)), (x0 + 25, 40)], [CORAL, TEAL_L, "#fbf3e1", PINK][i % 4]))
    art = K(art, strokes(W, H, [([(0, 8), (800, 10)], 2, None)]), INKC, seed=nx(), alpha=0.6)
    for poly, col in flags:
        art = P(art, shapes(W, H, [poly], smooth=False), col)
    preview(art, "panggung", tone=CREAM)
    clear()
    return save(art, f"{OUT}/panggung.webp", max_w=780, quality=82)


# ---------------------------------------------------------------- children's crayon drawings on paper sheets
def sheet(W, H, rot, rng):
    """A sheet of drawing paper with two strips of masking tape. Returns (art, sheet mask)."""
    cx, cy = W / 2, H / 2
    pts = rotp([(cx - W * 0.42, cy - H * 0.42), (cx + W * 0.42, cy - H * 0.42), (cx + W * 0.42, cy + H * 0.42), (cx - W * 0.42, cy + H * 0.42)], cx, cy, rot)
    m = shapes(W, H, [pts], smooth=False)
    art = over(blank(W, H), soft_shadow(m, "#3a2a20", blur=6, strength=0.25, dx=3, dy=5))
    art = OV(art, m, lambda mm: rgba(flat(mm.shape[0], mm.shape[1], "#fffdf6") * (0.97 + 0.03 * noise(mm.shape[1], mm.shape[0], 3, 1.0)[..., None]), mm))
    for tx in (-0.3, 0.3):
        tp = rotp([(cx + W * tx - 28, cy - H * 0.46), (cx + W * tx + 28, cy - H * 0.46), (cx + W * tx + 26, cy - H * 0.37), (cx + W * tx - 30, cy - H * 0.37)], cx, cy, rot + tx * 0.3)
        art = OV(art, shapes(W, H, [tp], smooth=False), lambda mm: rgba(flat(mm.shape[0], mm.shape[1], "#efe0b0"), mm * 0.82))
    return art, m


def matahari():
    W, H = 300, 320
    rng = random.Random(1)
    art, m = sheet(W, H, -0.06, rng)
    cx, cy = 150, 135
    art = CR(art, circles(W, H, [(cx, cy, 44)]) * m, "#f6c037", seed=nx(), tooth=0.6)
    art = CR(art, strokes(W, H, [(arc_pts(cx, cy, 44, 0, math.tau, 40), 4, None)]), "#e08a1e", seed=nx())
    art = CR(art, strokes(W, H, [([(cx + math.cos(a) * 56, cy + math.sin(a) * 56), (cx + math.cos(a) * 82, cy + math.sin(a) * 82)], 5, None) for a in np.linspace(0, math.tau, 12, endpoint=False)]), "#f0a326", seed=nx())
    art = CR(art, strokes(W, H, [(arc_pts(cx - 15, cy - 6, 6, math.pi * 1.1, math.pi * 1.9, 6), 3.5, None), (arc_pts(cx + 15, cy - 6, 6, math.pi * 1.1, math.pi * 1.9, 6), 3.5, None), (arc_pts(cx, cy + 6, 18, 0.4, math.pi - 0.4, 10), 3.5, None)]), "#7a3b1a", seed=nx())
    art = CR(art, scribble_fill(W, H, [(40, 250), (260, 250), (260, 272), (40, 272)], gap=6, ang=0.2, width=4, rng=rng) * m, "#5fae4e", seed=nx())
    preview(art, "matahari", tone="#f1e4c8")
    return save(art, f"{OUT}/matahari.webp", max_w=220, quality=82)


def pelangi():
    W, H = 320, 280
    rng = random.Random(2)
    art, m = sheet(W, H, 0.07, rng)
    for i, col in enumerate(["#e2483f", "#f29a2e", "#f4cf3a", "#5fae4e", "#3f86c6", "#7b55a8"]):
        art = CR(art, strokes(W, H, [(arc_pts(160, 200, 108 - i * 12, math.pi * 1.02, math.pi * 1.98, 40), 9, None)]) * m, col, seed=nx(), tooth=0.55)
    for cx_, cy_ in ((70, 200), (250, 200)):
        art = CR(art, circles(W, H, [(cx_ - 16, cy_, 16), (cx_, cy_ - 10, 20), (cx_ + 18, cy_, 15)]) * m, "#cfe3f2", seed=nx(), tooth=0.5)
        art = CR(art, strokes(W, H, [(arc_pts(cx_, cy_ - 4, 30, math.pi, math.tau, 20), 3, None)]) * m, "#6aa0cf", seed=nx())
    preview(art, "pelangi", tone="#f1e4c8")
    return save(art, f"{OUT}/pelangi.webp", max_w=230, quality=82)


def rumah():
    """A child's drawing of the school with a flag and two little friends."""
    W, H = 320, 300
    rng = random.Random(3)
    art, m = sheet(W, H, -0.04, rng)
    art = CR(art, scribble_fill(W, H, [(70, 150), (240, 150), (240, 240), (70, 240)], gap=6, ang=0.9, width=4, rng=rng), "#ef8a6a", seed=nx())
    art = CR(art, strokes(W, H, [([(70, 150), (240, 150), (240, 240), (70, 240), (70, 150)], 3.5, None)]), "#b8442e", seed=nx())
    art = CR(art, scribble_fill(W, H, [(58, 152), (155, 92), (252, 152)], gap=5, ang=0.1, width=4, rng=rng), "#c9403a", seed=nx())
    art = CR(art, scribble_fill(W, H, [(140, 190), (170, 190), (170, 240), (140, 240)], gap=4, ang=1.6, width=3.5, rng=rng), "#7a4a2a", seed=nx())
    art = CR(art, strokes(W, H, [([(205, 92), (205, 40)], 3.5, None)]), "#555555", seed=nx())
    art = CR(art, shapes(W, H, [[(207, 40), (245, 40), (245, 52), (207, 52)]], smooth=False), "#e2483f", seed=nx())
    art = CR(art, shapes(W, H, [[(207, 52), (245, 52), (245, 64), (207, 64)]], smooth=False), "#fafafa", seed=nx(), density=0.4)
    for fx, col in ((40, "#3f86c6"), (275, "#e2a23a")):
        art = CR(art, strokes(W, H, [(arc_pts(fx, 205, 9, 0, math.tau, 16), 3, None), ([(fx, 214), (fx, 245)], 3, None), ([(fx - 12, 226), (fx + 12, 226)], 3, None), ([(fx, 245), (fx - 9, 262)], 3, None), ([(fx, 245), (fx + 9, 262)], 3, None)]), col, seed=nx())
    art = CR(art, scribble_fill(W, H, [(30, 258), (290, 258), (290, 270), (30, 270)], gap=5, ang=0.1, width=4, rng=rng) * m, "#5fae4e", seed=nx())
    preview(art, "rumah", tone="#f1e4c8")
    return save(art, f"{OUT}/rumah.webp", max_w=230, quality=82)


def angklung():
    W, H = 200, 260
    art = paint_angklung(blank(W, H), W, H, 100, 240, 140)
    preview(art, "angklung", tone=CREAM)
    return save(art, f"{OUT}/angklung.webp", max_w=120, quality=84)


def rebana():
    W = H = 220
    art = paint_rebana(blank(W, H), W, H, 110, 110, 90)
    preview(art, "rebana", tone=CREAM)
    return save(art, f"{OUT}/rebana.webp", max_w=110, quality=84)


def kipas():
    W, H = 300, 200
    art = paint_kipas(blank(W, H), W, H, 150, 180, 140, a0=-math.pi + 0.15, a1=-0.15)
    preview(art, "kipas", tone=CREAM)
    return save(art, f"{OUT}/kipas.webp", max_w=150, quality=84)


def bintang():
    W = H = 120
    star = [(60 + math.cos(-math.pi / 2 + k * math.pi / 5) * (50 if k % 2 == 0 else 22), 62 + math.sin(-math.pi / 2 + k * math.pi / 5) * (50 if k % 2 == 0 else 22)) for k in range(10)]
    art = CR(blank(W, H), scribble_fill(W, H, star, gap=5, ang=0.8, width=4.5), "#f2b630", seed=nx(), tooth=0.65)
    art = CR(art, strokes(W, H, [(star + [star[0]], 3.5, None)]), "#d9861b", seed=nx())
    preview(art, "bintang", tone=CREAM)
    return save(art, f"{OUT}/bintang.webp", max_w=64, quality=84)


def bendera():
    """Seamless strip of hand-painted bunting (umbul-umbul segitiga) for section tops."""
    W, H = 480, 70
    art = blank(W, H)
    art = K(art, strokes(W, H, [([(0, 8), (120, 14), (240, 8), (360, 14), (480, 8)], 2, None)]), INKC, seed=nx(), alpha=0.6)
    for i in range(8):
        x0 = i * 60 + 5
        y0 = 8 + 6 * abs(math.sin(math.pi * ((x0 + 25) % 240) / 240))
        art = P(art, shapes(W, H, [[(x0, y0), (x0 + 50, y0), (x0 + 25, y0 + 46)]], smooth=False), [CORAL, TEAL_L, MUST, PINK][i % 4])
    save_full(art, f"{OUT}/bendera.webp", quality=82)


for p in PARTS:
    globals()[p]()
    clear()
kb(OUT)
