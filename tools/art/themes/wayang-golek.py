"""Wayang Golek — Sundanese rod-puppet stage, gouache on warm paper: two original carved-wood golek puppets (painted
faces, gilt makuta/siger, batik kain, velvet jacket), the gedebog (banana-trunk) stage, a degung gong in a carved
ancak, a kendang, and a fringed stage valance. Run: python3 -I wayang-golek.py [part ...]
parts: putra putri gedebog gong kendang valance tile. Assets -> public/themes/art/wayang-golek/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q3_lib import *

OUT = outdir("wayang-golek")
PARTS = sys.argv[1:] or ["putra", "putri", "gedebog", "gong", "kendang", "valance", "tile"]
CREAM = "#f3e6c8"
GOLD = "#cf9d3c"
WOOD, WOOD_D, WOOD_L = "#8a5a2e", "#4a2a14", "#b07a44"
RED, RED_D = "#b7332a", "#7a1d18"
TEAL, TEAL_D = "#1f5a55", "#123a37"
INK = "#1e130b"


def batik_parang(W, H, area, seed, sp=26):
    """diagonal parang bands with small hooked lobes, clipped to area."""
    items, lobes = [], []
    for k in range(-30, 30):
        x0 = k * sp
        items.append(([(x0, 0), (x0 + H, H)], 2.6, None))
        items.append(([(x0 + 7, 0), (x0 + 7 + H, H)], 1.2, None))
        for t in range(0, H, 20):
            cx, cy = x0 + t + sp * 0.62, t
            lobes.append((cx, cy, 7.5, 3.0, 45 + (35 if (t // 20) % 2 else -35)))
    return strokes(W, H, items) * area, ellipses(W, H, lobes) * area


def batik_flowers(W, H, area, rng, n=60, r=6.5):
    pts = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        for a in range(5):
            ang = a * math.tau / 5
            pts.append((x + math.cos(ang) * r, y + math.sin(ang) * r, r * 0.55))
    dots = [(x, y, 1.6) for x, y, _ in pts]
    return circles(W, H, pts) * area, circles(W, H, dots) * area


def golek(kind):
    W, H = 300, 800
    rng = np.random.default_rng(11 if kind == "putra" else 23)
    nx = Seq(4100 if kind == "putra" else 4300)
    cx = 150
    art = blank(W, H)
    # rods (tuding) behind everything + central rod
    rods = strokes(W, H, [([(cx, 600), (cx + 1, 798)], 11, None),
                          ([(226, 300), (252, 712)] if kind == "putra" else [(176, 352), (214, 712)], 4.2, None), ([(104, 388), (64, 712)], 4.2, None)])
    art = GP(art, rods, WOOD, WOOD_D, seed=nx(), rough=0.6, streak=1.2)
    # kain (skirt)
    hem = [(232, 640), (210, 652), (186, 646), (160, 656), (136, 648), (110, 657), (88, 646), (68, 640)]
    skirt = [(120, 330), (180, 330), (198, 420), (218, 540)] + hem + [(82, 540), (102, 420)]
    sk = smooth(W, H, skirt)
    if kind == "putra":
        art = GP(art, sk, "#2b2f52", "#1c1f3a", seed=nx(), rough=1.2, streak=0.9)
        bands, lobes = batik_parang(W, H, sk, nx())
        art = GP(art, bands, "#c9a25a", "#a77f3a", seed=nx(), rough=0.7, streak=0.4)
        art = GP(art, lobes, CREAM, "#e3cf9f", seed=nx(), rough=0.6)
    else:
        art = GP(art, sk, RED_D, "#5e1512", seed=nx(), rough=1.2, streak=0.9)
        fl, dt = batik_flowers(W, H, sk, rng, 520, 5.5)
        art = GP(art, fl, "#e0b45a", "#c99a3e", seed=nx(), rough=0.6)
        art = GP(art, dt, RED_D, seed=nx(), rough=0.3)
        # wiron (pleated front panel)
        pleat = poly(W, H, [(140, 340), (160, 340), (176, 650), (124, 652)]) * sk
        art = GP(art, pleat, "#3a2a20", "#2a1d15", seed=nx(), rough=0.8)
        art = ink(art, strokes(W, H, [([(146 + k * 6, 350), (136 + k * 9, 648)], 1.4, None) for k in range(4)]) * pleat, "#e0b45a", nx(), 0.7)
    folds = strokes(W, H, [(curve([(130, 360), (118, 480), (104, 640)], 14), 5, (0.3, 0.2)), (curve([(170, 360), (184, 480), (198, 640)], 14), 5, (0.3, 0.2)),
                           (curve([(150, 400), (152, 520), (150, 645)], 14), 4, (0.3, 0.2))])
    art = G(art, folds * sk, "#000000", seed=nx(), density=0.28, edge=0.2, bloom=0, rough=2, feather=2.2)
    hemline = strokes(W, H, [(curve(hem, 40), 3.2, None)])
    art = FO(art, hemline, GOLD, seed=nx(), sparkle=0.05)
    # sampur (sash ends)
    sash_c = ("#d7562a", "#a83a1c") if kind == "putra" else ("#2f7a6c", "#1d544a")
    sash = strokes(W, H, [(curve([(112, 336), (96, 400), (92, 470), (84, 520)], 20), 15, (0.05, 0.3)),
                          (curve([(188, 336), (206, 396), (212, 466), (222, 512)], 20), 15, (0.05, 0.3))])
    art = GP(art, sash, *sash_c, seed=nx(), rough=1.0, streak=1.0)
    art = G(art, strokes(W, H, [(curve([(108, 350), (95, 460)], 10), 3, None), (curve([(194, 350), (210, 450)], 10), 3, None)]), "#000000", seed=nx(), density=0.25, bloom=0, rough=1, feather=1.5)
    # arms (behind torso edge)
    skin, skin_d = ("#e9c49a", "#c99868") if kind == "putra" else ("#f0d0ac", "#d2a47a")
    fh = (226, 300) if kind == "putra" else (176, 352)
    arm_f = strokes(W, H, [(curve([(184, 246), (210, 280), (222, 296), fh] if kind == "putra" else [(184, 246), (204, 292), (200, 330), fh], 24), 18, (0.02, 0.35))])
    arm_b = strokes(W, H, [(curve([(116, 246), (94, 290), (88, 330), (104, 386)], 24), 18, (0.02, 0.35))])
    hands = ellipses(W, H, [(fh[0], fh[1], 8, 11, -30 if kind == 'putra' else 20), (104, 388, 8, 11, 10)])
    arms = np.maximum.reduce([arm_f, arm_b, hands])
    art = GP(art, arms, skin, skin_d, seed=nx(), rough=0.7, streak=0.8)
    art = G(art, strokes(W, H, [(curve([(200, 270), (214, 320)], 8), 4, None), (curve([(100, 270), (88, 320)], 8), 4, None)]) * arms, skin_d, seed=nx(), density=0.45, bloom=0, rough=1, feather=1.6)
    cuffs = strokes(W, H, [([(186, 262), (204, 256)], 5, None), ([(98, 256), (116, 262)], 5, None), ([(fh[0] - 8, fh[1] - 14), (fh[0] + 6, fh[1] - 12)], 4, None), ([(85, 372), (99, 368)], 4, None)])
    art = FO(art, cuffs, GOLD, seed=nx(), sparkle=0.05)
    # torso / jacket
    torso = smooth(W, H, [(112, 236), (150, 228), (188, 236), (192, 262), (180, 334), (120, 334), (108, 262)])
    if kind == "putra":
        art = GP(art, torso, "#1d1a1f", "#2c2430", seed=nx(), rough=0.8, streak=0.7)
        chest = poly(W, H, [(136, 236), (164, 236), (156, 330), (144, 330)])
        art = GP(art, chest, skin, skin_d, seed=nx(), rough=0.6)
    else:
        art = GP(art, torso, TEAL, TEAL_D, seed=nx(), rough=0.8, streak=0.7)
        chest = smooth(W, H, [(126, 234), (174, 234), (166, 262), (134, 262)])
        art = GP(art, chest, skin, skin_d, seed=nx(), rough=0.6)
    belt = rect(W, H, 116, 318, 184, 342, 4)
    art = FO(art, belt, GOLD, seed=nx(), sparkle=0.08)
    art = GP(art, ellipses(W, H, [(150, 330, 9, 8, 0)]), RED, RED_D, seed=nx(), rough=0.4)
    trim = strokes(W, H, [(curve([(112, 238), (136, 236), (144, 330)], 16), 3.2, None), (curve([(188, 238), (164, 236), (156, 330)], 16), 3.2, None)])
    art = FO(art, trim, GOLD, seed=nx(), sparkle=0.05)
    # kalung (crescent collar)
    collar = np.clip(ellipses(W, H, [(150, 236, 40, 26, 0)]) - ellipses(W, H, [(150, 226, 30, 20, 0)]), 0, 1) * (np.arange(H)[:, None] > 228)
    art = FO(art, collar.astype(np.float32), GOLD, seed=nx(), sparkle=0.1)
    beads = circles(W, H, [(150 + math.cos(a) * 35, 238 + math.sin(a) * 22, 2.8) for a in np.linspace(0.35, math.pi - 0.35, 9)])
    art = GP(art, beads, RED, RED_D, seed=nx(), rough=0.3)
    # neck + head
    neck = rect(W, H, 138, 198, 162, 236, 6)
    art = GP(art, neck, skin, skin_d, seed=nx(), rough=0.5)
    head = smooth(W, H, ellipse_pts(cx, 170, 32, 41, 14))
    if kind == "putri":
        bun = smooth(W, H, ellipse_pts(cx - 30, 150, 22, 26, 12, 0.3))
        hair = smooth(W, H, [(116, 160), (120, 128), (150, 120), (182, 130), (186, 168), (176, 150), (150, 140), (124, 152)])
        art = GP(art, np.maximum(bun, hair), "#17120f", "#2a201a", seed=nx(), rough=0.8, streak=0.8)
        flowers = circles(W, H, [(cx - 44, 140, 5), (cx - 36, 128, 4.5), (cx - 22, 134, 4), (cx - 46, 158, 4)])
        art = GP(art, flowers, "#f4efe2", "#e2d6bd", seed=nx(), rough=0.5)
    art = GP(art, head, skin, skin_d, seed=nx(), rough=0.6, streak=0.6)
    shade = smooth(W, H, ellipse_pts(cx - 14, 182, 14, 30, 10))
    art = G(art, shade * head, skin_d, seed=nx(), density=0.35, edge=0.2, bloom=0, rough=3, feather=3)
    cheek = circles(W, H, [(cx - 15, 188, 7), (cx + 15, 188, 7)])
    art = G(art, cheek, "#d97a62", seed=nx(), density=0.28, edge=0.1, bloom=0, rough=2, feather=3)
    if kind == "putra":
        hair = smooth(W, H, [(118, 150), (122, 132), (150, 128), (178, 132), (182, 150), (172, 144), (150, 141), (128, 144)])
        art = GP(art, hair, "#17120f", seed=nx(), rough=0.6)
        sideburn = strokes(W, H, [(curve([(121, 150), (119, 176), (124, 192)], 10), 4, (0.1, 0.6)), (curve([(179, 150), (181, 176), (176, 192)], 10), 4, (0.1, 0.6))])
        art = GP(art, sideburn, "#17120f", seed=nx(), rough=0.4)
    # features: long downcast almond eyes, fine brows, slender nose, small red mouth
    eyes = strokes(W, H, [(curve([(128, 172), (136, 168), (145, 171)], 10), 3.2, (0.2, 0.5)), (curve([(155, 171), (164, 168), (172, 172)], 10), 3.2, (0.5, 0.2))])
    brows = strokes(W, H, [(curve([(124, 162), (134, 155), (146, 158)], 12), 2.2, (0.1, 0.5)), (curve([(154, 158), (166, 155), (176, 162)], 12), 2.2, (0.5, 0.1))])
    nose = strokes(W, H, [(curve([(148, 166), (147, 186), (151, 192), (155, 190)], 12), 1.6, (0.3, 0.2))])
    art = ink(art, np.maximum.reduce([eyes, brows, nose]), INK, nx(), 0.92)
    mouth = ellipses(W, H, [(150, 203, 6.5, 2.6, 0)])
    art = GP(art, mouth, "#b42a24", seed=nx(), rough=0.3)
    if kind == "putra":
        mus = strokes(W, H, [(curve([(150, 197), (140, 198), (133, 194)], 8), 1.8, (0.1, 0.7)), (curve([(150, 197), (160, 198), (167, 194)], 8), 1.8, (0.1, 0.7))])
        art = ink(art, mus, INK, nx(), 0.9)
    # headdress
    if kind == "putra":
        band = smooth(W, H, [(116, 146), (150, 132), (184, 146), (182, 134), (150, 120), (118, 134)])
        tiers = poly(W, H, [(124, 128), (176, 128), (170, 98), (162, 92), (166, 70), (156, 62), (158, 40), (150, 26), (142, 40), (144, 62), (134, 70), (138, 92), (130, 98)])
        back = strokes(W, H, [(spiral_pts(104, 120, 22, 4, -0.4, 1.1, 40, 1), 8, (0.0, 0.6))])
        sumping = smooth(W, H, [(116, 160), (98, 150), (86, 168), (100, 176), (116, 176)])
        sumping2 = smooth(W, H, [(184, 160), (202, 150), (214, 168), (200, 176), (184, 176)])
        gold = np.maximum.reduce([band, tiers, back, sumping, sumping2])
        art = FO(art, gold, GOLD, seed=nx(), sparkle=0.12)
        lines = strokes(W, H, [([(128, 112), (172, 112)], 1.6, None), ([(136, 92), (164, 92)], 1.6, None), ([(140, 74), (160, 74)], 1.4, None), ([(146, 54), (154, 54)], 1.2, None)])
        art = ink(art, lines * gold, "#6a4314", nx(), 0.7)
        gems = ellipses(W, H, [(150, 104, 6, 7, 0), (150, 82, 4.5, 5.5, 0), (150, 62, 3.5, 4.5, 0), (150, 132, 4, 4, 0)])
        art = GP(art, gems, RED, RED_D, seed=nx(), rough=0.4)
        tassel = strokes(W, H, [(curve([(104, 128), (98, 170), (102, 220)], 12), 5, (0.1, 0.4))])
        art = GP(art, tassel, RED, RED_D, seed=nx(), rough=0.6)
    else:
        siger = poly(W, H, [(114, 146), (124, 112), (136, 120), (142, 96), (150, 86), (158, 96), (164, 120), (176, 112), (186, 146), (150, 136)])
        sumping = smooth(W, H, [(116, 164), (104, 158), (98, 172), (108, 180), (118, 178)])
        sumping2 = smooth(W, H, [(184, 164), (196, 158), (202, 172), (192, 180), (182, 178)])
        art = FO(art, np.maximum.reduce([siger, sumping, sumping2]), GOLD, seed=nx(), sparkle=0.14)
        art = ink(art, strokes(W, H, [(curve([(122, 134), (150, 124), (178, 134)], 12), 1.4, None), (curve([(134, 124), (150, 104), (166, 124)], 12), 1.2, None)]) * siger, "#6a4314", nx(), 0.7)
        pins = []
        for x, y in [(130, 100), (150, 74), (170, 100), (140, 84), (160, 84)]:
            pins.append(([(150 + (x - 150) * 0.4, 120), (x, y)], 1.2, None))
        art = ink(art, strokes(W, H, pins), "#8a6526", nx(), 0.8)
        kg = circles(W, H, [(130, 100, 5), (150, 74, 6), (170, 100, 5), (140, 84, 4), (160, 84, 4)])
        art = FO(art, kg, "#e2bd62", seed=nx(), sparkle=0.2)
        gems = ellipses(W, H, [(150, 118, 5, 6, 0), (130, 100, 2, 2, 0), (170, 100, 2, 2, 0)])
        art = GP(art, gems, "#2f7a6c", "#1d544a", seed=nx(), rough=0.3)
        earring = circles(W, H, [(118, 194, 3.5), (182, 194, 3.5)])
        art = FO(art, earring, GOLD, seed=nx())
    # carved edges: ink contour around every shape + wood grain on the skin-coloured carving
    a = gaussian_filter(art[..., 3], 0.8)
    gy, gx = np.gradient(a)
    edge = np.clip(np.hypot(gx, gy) * 3.2, 0, 1)
    art = G(art, edge, "#2a170b", seed=nx(), density=0.55, edge=0.0, bloom=0, rough=0.6, feather=0.5)
    skinm = np.maximum.reduce([arms, head, neck])
    grain = jw.hatch(W, H, 1.45, 5.5, 0.12, nx(), wob=3.0) * skinm
    art = G(art, grain, skin_d, seed=nx(), density=0.22, edge=0, bloom=0, rough=0.5, feather=0.6)
    # light from upper-left: soft shadow on right side of everything
    body = (art[..., 3] > 0.3).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    sh = body * np.clip((xx - cx) / 90, 0, 1) * (yy < 660)
    art = G(art, gaussian_filter(sh.astype(np.float32), 3) * body, "#2a160a", seed=nx(), density=0.22, edge=0.0, bloom=0.3, rough=4, feather=2)
    clear()
    return art


for kind in ("putra", "putri"):
    if kind in PARTS:
        a = golek(kind)
        preview(a, f"wg-{kind}", CREAM)
        save(a, f"{OUT}/{kind}.webp", max_w=260, quality=84)


if "gedebog" in PARTS:
    # banana-trunk stage log, seen from the front: pale green/ochre sheaths with fibre streaks and a cut end
    W, H = 1000, 170
    nx = Seq(4500)
    rng = np.random.default_rng(5)
    art = blank(W, H)
    log = smooth(W, H, [(30, 40), (500, 30), (975, 42), (990, 90), (975, 140), (500, 150), (30, 138), (18, 90)])
    art = GP(art, log, "#9aa35a", "#7d8b45", seed=nx(), rough=1.4, streak=1.2)
    # overlapping sheaths
    for k in range(9):
        x0 = 20 + k * 112 + rng.uniform(-10, 10)
        sh = smooth(W, H, [(x0, 36), (x0 + 150, 32), (x0 + 168, 92), (x0 + 150, 148), (x0, 142), (x0 + 16, 92)]) * log
        col = ["#b4b46a", "#9fa65c", "#c2b878", "#a8ab62"][k % 4]
        art = GP(art, sh, col, mix(col, "#6c7a3a", 0.4), seed=nx(), rough=1.2, streak=1.4)
        art = ink(art, strokes(W, H, [(curve([(x0 + 150, 33), (x0 + 168, 92), (x0 + 150, 147)], 16), 2.2, None)]) * log, "#5a5a2a", nx(), 0.6)
    fib = jw.hatch(W, H, 0.0, 6.0, 0.1, nx(), wob=4) * log
    art = G(art, fib, "#5d6a30", seed=nx(), density=0.28, edge=0, bloom=0, rough=0.6, feather=0.6)
    browns = (fbm(W, H, nx(), 9, 3) > 0.8).astype(np.float32) * log
    art = G(art, browns, "#8a6a32", seed=nx(), density=0.3, edge=0.4, bloom=0.3, rough=1.5)
    top = np.clip(log - np.roll(log, 22, 0), 0, 1)
    art = G(art, gaussian_filter(top, 6) * log, "#f1ecc4", seed=nx(), density=0.35, edge=0, bloom=0, rough=3, feather=3)
    bot = np.clip(log - np.roll(log, -26, 0), 0, 1)
    art = G(art, gaussian_filter(bot, 7) * log, "#3a3a18", seed=nx(), density=0.45, edge=0, bloom=0, rough=3, feather=3)
    preview(art, "wg-gedebog", CREAM)
    save(art, f"{OUT}/gedebog.webp", max_w=800, quality=80)
    clear()

if "gong" in PARTS:
    # degung gong hanging in a carved ancak (two posts, a curved top beam with naga-free lung-lung scrolls)
    W, H = 460, 440
    nx = Seq(4600)
    art = blank(W, H)
    frame = np.maximum.reduce([rect(W, H, 40, 70, 66, 430, 6), rect(W, H, 394, 70, 420, 430, 6),
                               smooth(W, H, [(14, 86), (120, 46), (230, 36), (340, 46), (446, 86), (446, 112), (340, 82), (230, 76), (120, 82), (14, 112)]),
                               rect(W, H, 26, 412, 120, 432, 4), rect(W, H, 340, 412, 434, 432, 4)])
    items, leaves = [], []
    for (x, y, a) in jw.along(curve([(60, 82), (230, 62), (400, 82)], 30), 34):
        it, lv = jw.lung(x, y + 2, 22, a, 1); items += it; leaves += lv
    art = jw.carve(W, H, frame, items, leaves, nx, base="#7a2a1c", light="#a54a30", dark="#3a120b", gold=GOLD, gold_amt=0.6, seed=4)
    ropes = strokes(W, H, [([(180, 72), (196, 150)], 4, None), ([(280, 72), (264, 150)], 4, None)])
    art = GP(art, ropes, "#c8a56a", "#8a6a3a", seed=nx(), rough=0.4)
    disc = circles(W, H, [(230, 270, 120)])
    art = FO(art, disc, "#b8862e", seed=nx(), emboss=0.8, sparkle=0.04)
    ring = np.clip(circles(W, H, [(230, 270, 120)]) - circles(W, H, [(230, 270, 104)]), 0, 1)
    art = G(art, ring, "#5a3a10", seed=nx(), density=0.45, edge=0.4, bloom=0.2, rough=2)
    boss = circles(W, H, [(230, 270, 38)])
    art = FO(art, boss, "#e2b858", seed=nx(), emboss=1.2, sparkle=0.1)
    art = G(art, np.clip(circles(W, H, [(230, 270, 44)]) - boss, 0, 1), "#4a2e0a", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1.5, feather=1.5)
    patina = (fbm(W, H, nx(), 18, 3) > 0.72).astype(np.float32) * disc
    art = G(art, patina * 0.5, "#4f6a4a", seed=nx(), density=0.16, edge=0.2, bloom=0.5, rough=3)
    preview(art, "wg-gong", CREAM)
    save(art, f"{OUT}/gong.webp", max_w=360, quality=82)
    clear()

if "kendang" in PARTS:
    W, H = 420, 240
    nx = Seq(4700)
    art = blank(W, H)
    body = smooth(W, H, [(60, 70), (210, 48), (360, 74), (372, 120), (360, 168), (210, 192), (60, 172), (52, 120)])
    art = GP(art, body, WOOD, WOOD_D, seed=nx(), rough=0.8, streak=1.2)
    grain = jw.hatch(W, H, 0.05, 7, 0.14, nx(), wob=5) * body
    art = G(art, grain, WOOD_D, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.5, feather=0.6)
    hl = smooth(W, H, [(100, 74), (210, 60), (320, 78), (210, 84)])
    art = G(art, hl * body, "#e6b678", seed=nx(), density=0.4, edge=0, bloom=0, rough=3, feather=4)
    heads = ellipses(W, H, [(58, 121, 16, 52, 0), (366, 121, 13, 47, 0)])
    art = GP(art, heads, "#e8d3a6", "#cdb27c", seed=nx(), rough=0.5)
    laces = []
    for k in range(9):
        t = k / 8
        y0 = 74 + t * 94
        laces.append(([(64, y0), (360, 122 + (y0 - 121) * 0.92)], 2.2, None))
        laces.append(([(64, 196 - t * 150 + 2), (360, 168 - t * 94)], 2.2, None))
    lace = strokes(W, H, laces) * body
    art = GP(art, lace, "#d9b778", "#a88446", seed=nx(), rough=0.3)
    rings = strokes(W, H, [([(104, 62), (104, 182)], 7, None), ([(316, 66), (316, 178)], 7, None)]) * body
    art = GP(art, rings, RED, RED_D, seed=nx(), rough=0.5)
    a = gaussian_filter(art[..., 3], 0.8); gy, gx = np.gradient(a)
    art = G(art, np.clip(np.hypot(gx, gy) * 3, 0, 1), "#2a170b", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5, feather=0.5)
    preview(art, "wg-kendang", CREAM)
    save(art, f"{OUT}/kendang.webp", max_w=300, quality=82)
    clear()

if "valance" in PARTS:
    # stage valance: red velvet scallops with gilt braid and a fringe; seamless 2-scallop repeat
    W, H = 480, 150
    nx = Seq(4800)
    art = blank(W, H)
    sc = []
    pts = [(0, 0), (W, 0)]
    path = [(W, 0)]
    for k in range(4, -1, -1):
        x0 = k * 120
        path += arc_pts(x0 + 60, 70, 60, 0, math.pi, 20, 0.7)[::-1][::-1]
    cloth = np.maximum(rect(W, H, 0, 0, W, 72), circles(W, H, []))
    for k in range(5):
        cloth = np.maximum(cloth, ellipses(W, H, [(k * 120 + 60 - 0, 70, 60, 46, 0)]))
    cloth = cloth * (np.arange(H)[:, None] < 118)
    art = GP(art, cloth.astype(np.float32), "#9c2a22", "#6e1a15", seed=nx(), rough=1.0, streak=1.2)
    folds = strokes(W, H, [([(k * 60 + 30, 0), (k * 60 + 30, 110)], 14, (0.0, 0.5)) for k in range(8)])
    art = G(art, folds * cloth, "#3a0a08", seed=nx(), density=0.35, edge=0, bloom=0, rough=2, feather=5)
    braid = np.clip(gaussian_filter(cloth, 1.0) - gaussian_filter(np.roll(cloth, -9, 0) * cloth, 1.0), 0, 1)
    braid = np.maximum(braid, rect(W, H, 0, 8, W, 20))
    art = FO(art, (braid > 0.3).astype(np.float32), GOLD, seed=nx(), sparkle=0.1)
    fr = []
    edge_y = [max([0] + [y for y in range(H) if cloth[y, x] > 0.5]) for x in range(0, W, 7)]
    for i, x in enumerate(range(0, W, 7)):
        y = edge_y[i]
        fr.append(([(x, y), (x, y + 18)], 2.2, (0.0, 0.5)))
    art = GP(art, strokes(W, H, fr), "#e0b04c", "#b8862e", seed=nx(), rough=0.4)
    dots = circles(W, H, [(k * 120 + 60, 92, 6) for k in range(4)] + [(k * 60 + 30, 40, 4) for k in range(8)])
    art = FO(art, dots, "#e2bd62", seed=nx(), sparkle=0.2)
    preview(art, "wg-valance", bg="#1f5a55")
    save_full(art, f"{OUT}/valance.webp", (W // 2 * 2 // 2, H // 2), quality=82) if False else save_full(art, f"{OUT}/valance.webp", quality=80)
    clear()
