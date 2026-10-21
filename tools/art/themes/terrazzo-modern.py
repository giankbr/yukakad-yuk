"""Terrazzo Modern — polished terrazzo slab (real chips of sage, terracotta, sand, marble and charcoal in cream cement)
plus Bauhaus-ish gouache shapes: tall arch, disc, half-moon, and a little shape row divider.
Run: python3 -I terrazzo-modern.py [part ...]   parts: slab arch disc half row. Assets -> public/themes/art/terrazzo-modern/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a5_lib import *

OUT = outdir("terrazzo-modern")
PARTS = sys.argv[1:] or ["slab", "arch", "disc", "half", "row"]
CREAM = "#efe8dc"
SAGE, SAGE_D = "#9fb19a", "#7d927a"
TERRA, TERRA_D = "#c77653", "#a95b3d"
SAND, SAND_D = "#e0bf98", "#c9a179"
CHAR = "#4b4642"
MARBLE = "#faf7f1"


if "slab" in PARTS:
    n = 520
    rng = random.Random(31)
    nx = Seq(30100)
    cement = rgb_arr(n, n, CREAM)
    mot = wrap_noise(n, n, 3, 22) - 0.5
    fine = wrap_noise(n, n, 4, 0.7) - 0.5
    cement *= (1 + mot * 0.05 + fine * 0.05)[..., None]
    art = np.concatenate([np.clip(cement, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    # fine aggregate: grey & dark sand grains
    grains = []
    for _ in range(900):
        grains.append((rng.uniform(0, n), rng.uniform(0, n), rng.uniform(0.6, 1.6), rng.uniform(0.5, 1.4), rng.uniform(0, 180)))
    gm = wrap_circles(n, n, grains)
    art = over(art, layer(gm, "#a49c91", 0.55))
    dark = wrap_circles(n, n, [(rng.uniform(0, n), rng.uniform(0, n), rng.uniform(0.7, 1.8), rng.uniform(0.6, 1.4), 0) for _ in range(260)])
    art = over(art, layer(dark, "#5b544e", 0.7))
    # chips, by colour family: (colours, count, size range)
    fams = [((SAGE, SAGE_D), 6, (18, 27)), ((TERRA, TERRA_D), 5, (17, 25)), ((MARBLE, "#e7e0d4"), 4, (16, 22)),
            ((MARBLE, "#ece6dc"), 70, (4, 11)), ((SAGE, SAGE_D), 50, (5, 15)), ((TERRA, TERRA_D), 42, (5, 16)), ((SAND, SAND_D), 40, (4, 12)),
            ((CHAR, "#2f2b28"), 34, (2.5, 7)), (("#d6dccf", "#b9c3b2"), 30, (3, 8))]
    occupied = []
    for (c1, c2), cnt, (r0, r1) in fams:
        polys = []
        for _ in range(cnt):
            for _try in range(30):
                r = rng.uniform(r0, r1); x = rng.uniform(0, n); y = rng.uniform(0, n)
                ok = all(min(abs(x - ox), n - abs(x - ox)) ** 2 + min(abs(y - oy), n - abs(y - oy)) ** 2 > (r + orr + 2) ** 2 for ox, oy, orr in occupied)
                if ok:
                    break
            occupied.append((x, y, r))
            polys.append(chip_poly(rng, x, y, r))
        m = wrap_polys(n, n, polys, smooth=False)
        m = np.clip(gaussian_filter(m, 0.5), 0, 1)
        chip = gouache_paint(m, c1, c2, seed=nx(), rough=0.8, streak=0.3)
        art = over(art, chip)
        # polished cut face: faint lighter rim on one side, darker on the other (stone depth)
        hi, lo = emboss_light(m, 0.5, 0.8)
        art = over(art, layer(hi * m, "#ffffff", 0.18))
        art = over(art, layer(lo * m, "#2a2420", 0.12))
        rim = np.clip(gaussian_filter(m, 0.9) - m * 0.85, 0, 1) * 1.5
        art = over(art, layer(np.clip(rim, 0, 1), "#8c8378", 0.22))
    # hairline veins in marble-ish chips + overall micro pores
    pores = wrap_circles(n, n, [(rng.uniform(0, n), rng.uniform(0, n), 0.7, 0.7, 0) for _ in range(500)])
    art = over(art, layer(pores, "#c9bfb2", 0.5))
    save_rgb(art, f"{OUT}/slab.webp", quality=78)
    clear()


def arch_poly(x0, x1, y_top, y_bot, n=40):
    r = (x1 - x0) / 2; cx = x0 + r
    pts = [(x0, y_bot)]
    for k in range(n + 1):
        a = math.pi + k * math.pi / n
        pts.append((cx + math.cos(a) * r, y_top + r + math.sin(a) * r))
    pts.append((x1, y_bot))
    return pts


if "arch" in PARTS:
    W, H = 460, 640
    nx = Seq(30200)
    m = shape_mask(W, H, arch_poly(20, 440, 20, 620), smooth=False)
    art = GP(blank(W, H), m, SAGE, SAGE_D, seed=nx(), rough=2.8, streak=1.0)
    inner = strokes(W, H, [(arch_poly(70, 390, 70, 620, 40)[1:-1], 3.2, None)])
    inner = np.maximum(inner, strokes(W, H, [([(70, 280), (70, 612)], 3.2, None), ([(390, 280), (390, 612)], 3.2, None)]))
    art = GP(art, inner, "#e9e3d6", seed=nx(), rough=1.0, streak=0.4, density=0.85)
    preview(art, "tz-arch", tone=CREAM)
    save(art, f"{OUT}/arch.webp", max_w=300, quality=80)

if "disc" in PARTS:
    W, H = 340, 340
    nx = Seq(30300)
    m = circles(W, H, [(170, 170, 150)])
    art = GP(blank(W, H), m, TERRA, TERRA_D, seed=nx(), rough=2.6, streak=1.0)
    preview(art, "tz-disc", tone=CREAM)
    save(art, f"{OUT}/disc.webp", max_w=220, quality=80)

if "half" in PARTS:
    W, H = 420, 230
    nx = Seq(30400)
    m = circles(W, H, [(210, 214, 190)]); m[214:] = 0
    art = GP(blank(W, H), m, SAND, SAND_D, seed=nx(), rough=2.4, streak=1.0)
    # bauhaus stripe arcs inside
    arcs = np.maximum.reduce([np.clip(circles(W, H, [(210, 214, r)]) - circles(W, H, [(210, 214, r - 7)]), 0, 1) for r in (150, 110, 70)])
    arcs[214:] = 0
    art = GP(art, arcs, "#f3ead9", seed=nx(), rough=1.0, streak=0.4, density=0.8)
    preview(art, "tz-half", tone=CREAM)
    save(art, f"{OUT}/half.webp", max_w=260, quality=80)

if "row" in PARTS:
    # divider: disc, half-moon, small arch, dot — gouache, laid on a baseline
    W, H = 420, 90
    nx = Seq(30500)
    art = blank(W, H)
    base = 78
    d = circles(W, H, [(138, base - 22, 22)])
    hm = circles(W, H, [(204, base, 28)]); hm[base:] = 0
    ar = shape_mask(W, H, arch_poly(248, 284, base - 52, base), smooth=False)
    dot = circles(W, H, [(312, base - 8, 8)])
    art = GP(art, d, TERRA, TERRA_D, seed=nx(), rough=1.2, streak=0.8)
    art = GP(art, hm, SAND, SAND_D, seed=nx(), rough=1.2, streak=0.8)
    art = GP(art, ar, SAGE, SAGE_D, seed=nx(), rough=1.2, streak=0.8)
    art = GP(art, dot, CHAR, seed=nx(), rough=0.8, streak=0.5)
    line = strokes(W, H, [([(40, base + 1), (100, base + 1)], 2.4, None), ([(338, base + 1), (380, base + 1)], 2.4, None)])
    art = GP(art, line, CHAR, seed=nx(), rough=0.6, streak=0.3)
    preview(art, "tz-row", tone=CREAM)
    save(art, f"{OUT}/row.webp", max_w=260, quality=82)
