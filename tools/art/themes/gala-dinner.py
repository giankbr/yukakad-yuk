"""Gala Dinner — corporate annual gala, black tie: painted stage (navy fluted backdrop panels with gilt trim, lectern,
trophy table, spotlight beams, footlights) above a hall of round banquet tables; gold-foil award trophy; navy banquet
table vignette; star rule divider. Run: python3 -I gala-dinner.py [part ...]. parts: stage trophy table divider.
Assets -> public/themes/art/gala-dinner/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _s3_lib import *

OUT = outdir("gala-dinner")
PARTS = sys.argv[1:] or ["stage", "trophy", "divider"]
NAVY, NAVY_D, NAVY_L, INK = "#14203f", "#0a1128", "#24345e", "#06080f"
GOLD, GOLD_L = "#c8a24f", "#e9cf8e"


def star_pts(cx, cy, r, ri, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else ri
        a = rot + i * math.pi / n
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def trophy(W, H, cx, base_y, s, nx, rng, star=True):
    """Gold cup trophy on a stepped black plinth with a small plaque; s = cup radius."""
    art = blank(W, H)
    # plinth (black lacquer with gold edge)
    pl = [[(cx - s * 1.0, base_y), (cx + s * 1.0, base_y), (cx + s * 0.9, base_y - s * 0.55), (cx - s * 0.9, base_y - s * 0.55)],
          [(cx - s * 0.72, base_y - s * 0.55), (cx + s * 0.72, base_y - s * 0.55), (cx + s * 0.64, base_y - s * 0.95), (cx - s * 0.64, base_y - s * 0.95)]]
    pm = shapes(W, H, pl, smooth=False)
    art = GP(art, pm, "#1b1b22", "#07070b", seed=nx(), rough=0.6, streak=0.8)
    edge = np.clip(gaussian_filter(pm, 1.0) - (gaussian_filter(pm, 1.0) > 0.98), 0, 1)
    art = FO(art, strokes(W, H, [([(cx - s * 1.0, base_y - 2), (cx + s * 1.0, base_y - 2)], 2.4, None), ([(cx - s * 0.9, base_y - s * 0.55), (cx + s * 0.9, base_y - s * 0.55)], 2.4, None), ([(cx - s * 0.64, base_y - s * 0.95), (cx + s * 0.64, base_y - s * 0.95)], 2.4, None)]), GOLD, seed=nx(), emboss=0.4)
    plaque = shapes(W, H, [[(cx - s * 0.4, base_y - s * 0.44), (cx + s * 0.4, base_y - s * 0.44), (cx + s * 0.4, base_y - s * 0.16), (cx - s * 0.4, base_y - s * 0.16)]], smooth=False)
    art = FO(art, plaque, "#b8934a", seed=nx(), emboss=0.5)
    lines = strokes(W, H, [([(cx - s * 0.28, base_y - s * (0.36 - k * 0.08)), (cx + s * 0.28, base_y - s * (0.36 - k * 0.08))], 1.2, None) for k in range(3)])
    art = G(art, lines, "#5a4520", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3, feather=0.4)
    # stem + foot
    y0 = base_y - s * 0.95
    foot = shapes(W, H, [[(cx - s * 0.42, y0), (cx + s * 0.42, y0), (cx + s * 0.18, y0 - s * 0.2), (cx + s * 0.08, y0 - s * 0.62), (cx + s * 0.22, y0 - s * 0.72), (cx - s * 0.22, y0 - s * 0.72), (cx - s * 0.08, y0 - s * 0.62), (cx - s * 0.18, y0 - s * 0.2)]], smooth=False)
    knob = ellipses(W, H, [(cx, y0 - s * 0.42, s * 0.12, s * 0.07, 0)])
    # cup bowl
    cy = y0 - s * 0.72
    bowl = [(cx - s * 0.95, cy - s * 1.25)] + [(cx + math.cos(t) * s * 0.95, cy - s * 1.25 + math.sin(t) * s * 1.3) for t in np.linspace(math.pi, 0, 30)][1:-1] + [(cx + s * 0.95, cy - s * 1.25)]
    bowl = [(cx - s * 0.95, cy - s * 1.25)] + [(cx - math.cos(t) * s * 0.95 * (1 - 0.15 * math.sin(t)), cy - s * 1.25 + math.sin(t) * s * 1.25) for t in np.linspace(0, math.pi, 30)] + [(cx + s * 0.95, cy - s * 1.25)]
    bm = shapes(W, H, [bowl], smooth=False)
    rim = ellipses(W, H, [(cx, cy - s * 1.25, s * 0.97, s * 0.16, 0)])
    handles = strokes(W, H, [(curve([(cx - s * 0.9, cy - s * 1.05), (cx - s * 1.38, cy - s * 1.0), (cx - s * 1.3, cy - s * 0.5), (cx - s * 0.6, cy - s * 0.3)], 24), s * 0.11, None),
                             (curve([(cx + s * 0.9, cy - s * 1.05), (cx + s * 1.38, cy - s * 1.0), (cx + s * 1.3, cy - s * 0.5), (cx + s * 0.6, cy - s * 0.3)], 24), s * 0.11, None)])
    gold = np.maximum.reduce([foot, knob, bm, handles])
    art = FO(art, gold, GOLD, seed=nx(), emboss=0.85, sparkle=0.03)
    # cylindrical shading on the bowl: dark band right, bright streak left
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - cx) / (s * 0.95)
    shade = np.clip(u * 0.9, 0, 1) ** 1.5 * bm
    art = G(art, shade, "#4a3410", seed=nx(), density=0.55, edge=0.05, bloom=0, rough=0.6, feather=2)
    streak = np.clip(1 - np.abs(u + 0.45) * 6, 0, 1) * bm
    art = OV(art, streak, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fff3cf"), np.float32), (m * 0.75)[..., None]], -1), pad=4)
    art = FO(art, rim, "#ddbb6a", seed=nx(), emboss=0.7)
    inner = ellipses(W, H, [(cx, cy - s * 1.23, s * 0.84, s * 0.1, 0)])
    art = GP(art, inner, "#6b4c18", "#3a2808", seed=nx(), rough=0.3, pad=4)
    # engraved bands on the bowl
    bands = strokes(W, H, [([(cx + math.cos(t) * s * 0.78, cy - s * 0.95 + math.sin(t) * s * 0.12) for t in np.linspace(0.15, math.pi - 0.15, 24)], 1.6, None),
                           ([(cx + math.cos(t) * s * 0.84, cy - s * 0.82 + math.sin(t) * s * 0.13) for t in np.linspace(0.15, math.pi - 0.15, 24)], 1.2, None)])
    art = G(art, bands * bm, "#6e5018", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.3, feather=0.5)
    if star:
        st = shapes(W, H, [star_pts(cx, cy - s * 1.62, s * 0.3, s * 0.13)], smooth=False)
        art = FO(art, st, "#e2c174", seed=nx(), emboss=0.8, sparkle=0.2)
    return art


if "trophy" in PARTS:
    W, H = 360, 520
    nx = Seq(8100)
    art = trophy(W, H, 180, 500, 120, nx, random.Random(1))
    preview(art, "gd-trophy", bg=NAVY)
    save(art, f"{OUT}/trophy.webp", max_w=260, quality=82)


def navy_table(art, W, H, cx, cy, s, nx, rng, candles=True, lit=1.0):
    rx, ry = s, s * 0.26
    drop = s * 0.5
    refl = shapes(W, H, [deform(ellipse_pts(cx, cy + drop + ry * 0.4, rx * 1.05, ry * 0.5), rng, 1, 0.04)])
    art = G(art, refl, "#000000", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=3, feather=s * 0.05)
    skirt_pts = [(cx - rx, cy)] + [(cx - rx * 1.04 + rx * 2.08 * u, cy + drop + math.sin(u * 22) * s * 0.02 + math.sin(u * math.pi) * ry * 0.9) for u in np.linspace(0, 1, 30)] + [(cx + rx, cy)]
    skirt = shapes(W, H, [skirt_pts], smooth=False)
    art = GP(art, skirt, "#1c2a52", "#0c142e", seed=nx(), rough=1.0, streak=0.5, pad=8)
    folds = strokes(W, H, [([(cx - rx + rx * 2 * u, cy + ry * 0.6), (cx - rx * 1.03 + rx * 2.06 * u, cy + drop + math.sin(u * math.pi) * ry * 0.8)], s * 0.035, (0.3, 0.1)) for u in np.linspace(0.06, 0.94, 11)])
    art = G(art, folds * skirt, "#050914", seed=nx(), density=0.45, edge=0.2, bloom=0.1, rough=1.5, feather=s * 0.02)
    sheen = strokes(W, H, [([(cx - rx * 0.4 + rx * 0.16 * k, cy + ry * 0.8), (cx - rx * 0.42 + rx * 0.17 * k, cy + drop * 0.95)], s * 0.02, (0.3, 0.3)) for k in range(5)]) * skirt
    art = G(art, sheen, "#4a5f96", seed=nx(), density=0.35 * lit, edge=0, bloom=0, rough=1, feather=s * 0.02)
    top = ellipses(W, H, [(cx, cy, rx, ry, 0)])
    art = GP(art, top, "#26375f", "#18244a", seed=nx(), rough=0.8, pad=8)
    runner = ellipses(W, H, [(cx, cy, rx * 0.5, ry * 0.36, 0)])
    art = GP(art, runner, "#a88a4a", "#7a6030", seed=nx(), rough=0.8, streak=1.0, density=0.8, pad=6)
    plates = ellipses(W, H, [(cx + math.cos(t) * rx * 0.74, cy + math.sin(t) * ry * 0.74, s * 0.09, s * 0.03, 0) for t in np.linspace(0, math.tau, 9)[:-1]])
    art = FO(art, plates, "#d1b06e", seed=nx(), emboss=0.4, sparkle=0.05)
    if candles:
        cand = [(cx - s * 0.16, cy - s * 0.01, 0.2), (cx, cy - s * 0.05, 0.3), (cx + s * 0.16, cy - s * 0.01, 0.2)]
        fl = shapes(W, H, [petal_pts(x, y - s * h - s * 0.01, s * 0.08, s * 0.024, -math.pi / 2, n=10) for x, y, h in cand])
        art = over(art, glow(circles(W, H, [(x, y - s * h - s * 0.05, s * 0.07) for x, y, h in cand]), "#ffcf70", radius=s * 0.12, strength=0.7 * lit))
        wax = shapes(W, H, [[(x - s * .02, y), (x + s * .02, y), (x + s * .018, y - s * h), (x - s * .018, y - s * h)] for x, y, h in cand], smooth=False)
        art = GP(art, wax, "#f6efe0", "#d6c8ae", seed=nx(), rough=0.3, pad=4)
        art = GP(art, fl, "#fff4c8", "#ffb848", seed=nx(), rough=0.3, pad=4)
    return art


if "table" in PARTS:
    W, H = 560, 380
    nx = Seq(8300)
    art = navy_table(blank(W, H), W, H, 280, 210, 220, nx, random.Random(2))
    preview(art, "gd-table", bg=INK)
    save(art, f"{OUT}/table.webp", max_w=420, quality=80)


if "divider" in PARTS:
    W, H = 460, 60
    nx = Seq(8500)
    m = strokes(W, H, [([(20, 30), (196, 30)], 2.0, (0.6, 0.0)), ([(264, 30), (440, 30)], 2.0, (0.0, 0.6))])
    m = np.maximum(m, shapes(W, H, [star_pts(230, 30, 20, 8.5)], smooth=False))
    m = np.maximum(m, circles(W, H, [(204, 30, 3.2), (256, 30, 3.2)]))
    art = FO(blank(W, H), m, GOLD, seed=nx(), emboss=0.8, sparkle=0.15)
    preview(art, "gd-divider", bg=NAVY)
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)


if "stage" in PARTS:
    W, H = 760, 820
    nx = Seq(8700); rng = random.Random(14)
    art = painted_sky(W, H, [(0, "#05070e"), (0.5, "#0a1128"), (1, "#070a15")], seed=nx(), streak=0.9)
    SY = 470  # stage floor front edge (y)
    BY = 150  # top of backdrop
    # backdrop: fluted vertical panels (navy velvet) framed by gilt pilasters, centre arch panel
    panels = []
    for k in range(9):
        x0 = 40 + k * 76
        panels.append([(x0 + 4, BY + 10), (x0 + 72, BY + 10), (x0 + 72, SY - 70), (x0 + 4, SY - 70)])
    pm = shapes(W, H, panels, smooth=False)
    art = GP(art, pm, "#1a2850", "#0e1734", seed=nx(), rough=0.8, streak=1.2)
    flutes = strokes(W, H, [([(x, BY + 14), (x, SY - 74)], 3.0, None) for k in range(9) for x in np.linspace(40 + k * 76 + 12, 40 + k * 76 + 64, 6)]) * pm
    art = G(art, flutes, "#050a1c", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6, feather=1.2)
    fh = strokes(W, H, [([(x + 3, BY + 14), (x + 3, SY - 74)], 1.4, None) for k in range(9) for x in np.linspace(40 + k * 76 + 12, 40 + k * 76 + 64, 6)]) * pm
    art = G(art, fh, "#3e5a9a", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.4, feather=0.8)
    trim = strokes(W, H, [([(40 + k * 76 + 2, BY + 6), (40 + k * 76 + 2, SY - 66)], 3.4, None) for k in range(10)] + [([(36, BY + 6), (728, BY + 6)], 4, None), ([(36, SY - 68), (728, SY - 68)], 4, None)])
    art = FO(art, trim, GOLD, seed=nx(), emboss=0.6, sparkle=0.05)
    # centre emblem medallion on the backdrop (company monogram ring, no text)
    med = np.clip(circles(W, H, [(380, 236, 46)]) - circles(W, H, [(380, 236, 40)]), 0, 1)
    med = np.maximum(med, shapes(W, H, [star_pts(380, 236, 24, 10)], smooth=False))
    art = over(art, glow(circles(W, H, [(380, 236, 44)]), "#e9cf8e", radius=24, strength=0.2))
    art = FO(art, med, "#d7b465", seed=nx(), emboss=0.8, sparkle=0.1)
    # stage platform with front fascia + steps
    plat = shapes(W, H, [[(0, SY - 70), (W, SY - 70), (W, SY), (0, SY)]], smooth=False)
    art = GP(art, plat, "#101a36", "#0a1128", seed=nx(), rough=0.6, streak=0.8)
    fas = shapes(W, H, [[(0, SY), (W, SY), (W, SY + 40), (0, SY + 40)]], smooth=False)
    art = GP(art, fas, "#070b18", seed=nx(), rough=0.5)
    art = FO(art, strokes(W, H, [([(0, SY + 1), (W, SY + 1)], 3, None)]), GOLD, seed=nx(), emboss=0.5)
    steps = shapes(W, H, [[(300 + k * 8, SY + 40 + k * 12 - 12), (460 - k * 8 - 0, SY + 40 + k * 12 - 12), (470 - k * 8 + 10, SY + 40 + k * 12), (290 + k * 8 - 10, SY + 40 + k * 12)] for k in range(1)], smooth=False)
    # spotlight beams from the ceiling (soft, layered) onto lectern and trophy table
    for (x0, x1, w1, strength) in ((210, 220, 120, 0.22), (560, 520, 150, 0.22), (380, 380, 300, 0.08)):
        beam = shapes(W, H, [[(x0 - 8, 0), (x0 + 8, 0), (x1 + w1 / 2, SY - 40), (x1 - w1 / 2, SY - 40)]], smooth=False)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        fall = np.clip(yy / (SY - 40), 0, 1) ** 0.7
        b = gaussian_filter(beam, 14) * (0.4 + 0.6 * fall)
        art = over(art, np.concatenate([np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#fff1cc"), np.float32), (b * strength)[..., None]], -1))
        pool = ellipses(W, H, [(x1, SY - 40, w1 * 0.55, 16, 0)])
        art = over(art, glow(pool, "#fff0c4", radius=12, strength=0.35 * strength / 0.22))
        trim_cache()
    # lectern (left)
    lec = shapes(W, H, [[(186, SY - 40), (254, SY - 40), (246, SY - 150), (194, SY - 150)], [(178, SY - 150), (262, SY - 150), (268, SY - 170), (172, SY - 170)]], smooth=False)
    art = GP(art, lec, "#1e1a1a", "#0a0809", seed=nx(), rough=0.6, streak=0.8)
    art = FO(art, strokes(W, H, [([(194, SY - 100), (246, SY - 100)], 2, None), ([(172, SY - 170), (268, SY - 170)], 2.6, None)]), GOLD, seed=nx(), emboss=0.5)
    art = FO(art, np.clip(circles(W, H, [(220, SY - 120, 11)]) - circles(W, H, [(220, SY - 120, 8)]), 0, 1), GOLD, seed=nx(), emboss=0.6)
    mic = strokes(W, H, [(curve([(232, SY - 170), (236, SY - 190), (226, SY - 206)], 10), 2.2, None)])
    art = GP(art, mic, "#2a2a30", seed=nx(), rough=0.3, pad=4)
    # trophy table (right): draped black table with three trophies
    tt = shapes(W, H, [[(450, SY - 40), (600, SY - 40), (596, SY - 96), (454, SY - 96)]], smooth=False)
    art = GP(art, tt, "#0c0c12", "#1a1a24", seed=nx(), rough=0.6, streak=0.8)
    art = FO(art, strokes(W, H, [([(452, SY - 96), (598, SY - 96)], 2.4, None)]), GOLD, seed=nx(), emboss=0.4)
    for (tx, ts) in ((482, 15), (525, 22), (568, 15)):
        art = over(art, trophy(W, H, tx, SY - 96, ts, nx, rng, star=ts > 18))
        trim_cache()
    # low white floral clusters along the stage front
    pet, lvs = [], []
    for k in range(13):
        x0 = 40 + k * 56 + rng.uniform(-6, 6); y0 = SY - 50
        for q in range(14):
            a = rng.uniform(0, math.tau); r = rng.uniform(0, 16)
            pet.append((x0 + math.cos(a) * r * 1.4, y0 + math.sin(a) * r * 0.55, rng.uniform(3.0, 5.2)))
        for q in range(4):
            lvs.append((x0 + rng.uniform(-24, 24), y0 + rng.uniform(4, 10), 10, 3.4, rng.uniform(-40, 40)))
    art = G(art, ellipses(W, H, lvs), "#2f4a3c", "#1a2a20", seed=nx(), density=0.85, edge=0.3, rough=0.8)
    art = G(art, circles(W, H, pet), "#f1ede6", "#c9c2b6", seed=nx(), density=0.9, edge=0.6, bloom=0.2, rough=1.2, gran=0.15)
    # footlights
    fls = circles(W, H, [(30 + k * 70, SY + 20, 4) for k in range(11)])
    art = over(art, glow(fls, "#ffd788", radius=8, strength=0.6))
    art = GP(art, fls, "#fff1c8", seed=nx(), rough=0.3)
    # hall floor + round tables in the dark foreground
    floor = shapes(W, H, [[(0, SY + 40), (W, SY + 40), (W, H), (0, H)]], smooth=False)
    art = GP(art, floor, "#090e1e", "#04060d", seed=nx(), rough=0.5, streak=0.6)
    for ty, xs, sz, lit in ((SY + 110, [110, 380, 650], 80, 0.8), (SY + 270, [190, 570], 150, 1.0)):
        for x in xs:
            art = navy_table(art, W, H, x + rng.uniform(-6, 6), ty, sz, nx, rng, lit=lit)
            trim_cache()
    art = vignette(art, strength=0.45)
    art = add_grain(art, seed=8, amount=0.035)
    art[..., 3] = 1
    preview(art, "gd-stage")
    save_full(art, f"{OUT}/stage.webp", size=(570, 615), quality=80)
