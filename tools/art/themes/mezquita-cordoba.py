"""Mezquita Cordoba — gouache in warm golden light: the hypostyle hall seen down one aisle (double arches — a horseshoe
arch braced under a round arch — with voussoirs alternating red brick and cream stone, slender columns receding into
a gold haze, timber ceiling); a single horseshoe arch inside its alfiz as the cover photo frame (spandrels carved with
ataurique palmettes); a repeating arcade frieze; a palmette divider; a small voussoir arch emblem.
Architecture, geometry and flora only.
Run: python3 -I mezquita-cordoba.py [part ...]   parts: hall frame frieze divider emblem
Assets -> public/themes/art/mezquita-cordoba/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g3_lib import *

OUT = outdir("mezquita-cordoba")
PARTS = sys.argv[1:] or ["hall", "frame", "frieze", "divider", "emblem"]
BRICK, BRICK_D, BRICK_L = "#a8432c", "#6e2616", "#c86a48"
STONE, STONE_D, STONE_L = "#ecdcbc", "#b9a079", "#fbf1dc"
UMBER, UMBER_D = "#3a2416", "#1f130b"
GOLD, GOLD_L = "#d9a441", "#f4d488"
COL, COL_D = "#7a6a5c", "#3a3028"


def horseshoe(cx, cy, r, d):
    """Angles (y-down) of a horseshoe arc whose impost lies d below the centre."""
    t = math.asin(min(0.95, d / r))
    return math.pi - t, 2 * math.pi + t


def voussoirs(W, H, cx, cy, r0, r1, a0, a1, n):
    red, white = [], []
    for i in range(n):
        p = ann(cx, cy, r0, r1, a0 + (a1 - a0) * i / n, a0 + (a1 - a0) * (i + 1) / n, 6)
        (red if i % 2 == 0 else white).append(p)
    return shapes(W, H, red, smooth=False), shapes(W, H, white, smooth=False)


def double_arch(W, H, x0, x1, by, s):
    """One bay between columns at x0 and x1 (floor at by, scale s = column height in px). Returns masks."""
    w = x1 - x0; cx = (x0 + x1) / 2
    colw = max(1.5, w * 0.075)
    top = by - s
    m = {}
    m["cols"] = shapes(W, H, [[(x - colw / 2, by), (x + colw / 2, by), (x + colw / 2 * 0.85, top), (x - colw / 2 * 0.85, top)] for x in (x0, x1)], smooth=False)
    m["caps"] = shapes(W, H, [[(x - colw * 0.9, top + s * 0.02), (x + colw * 0.9, top + s * 0.02), (x + colw * 1.2, top - s * 0.06), (x - colw * 1.2, top - s * 0.06)] for x in (x0, x1)], smooth=False)
    imp = top - s * 0.06
    # lower horseshoe arch
    r = w * 0.5; d = r * 0.26; cy = imp - d
    a0, a1 = horseshoe(cx, cy, r, d)
    ring = w * 0.11
    m["lr"], m["lw"] = voussoirs(W, H, cx, cy, r * 0.93, r * 0.93 + ring, a0, a1, 17)
    # piers rising over the columns to the upper arches
    pw = colw * 1.8
    up = imp - s * 1.0
    m["piers"] = shapes(W, H, [[(x - pw / 2, imp), (x + pw / 2, imp), (x + pw / 2, up), (x - pw / 2, up)] for x in (x0, x1)], smooth=False)
    # upper round arch
    ur = w * 0.5 - pw * 0.1
    m["ur"], m["uw"] = voussoirs(W, H, cx, up, ur - ring * 0.9, ur, math.pi, 2 * math.pi, 15)
    # wall above the upper arch up to the beams
    wall_top = up - ur - s * 0.26
    wall = shapes(W, H, [[(x0 - pw / 2, up + 1), (x1 + pw / 2, up + 1), (x1 + pw / 2, wall_top), (x0 - pw / 2, wall_top)]], smooth=False)
    hole = shapes(W, H, [ellipse_pts(cx, up, ur - 0.5, ur - 0.5, 60)])
    m["wall"] = np.clip(wall - hole, 0, 1)
    m["beam"] = shapes(W, H, [[(x0 - pw, wall_top + 2), (x1 + pw, wall_top + 2), (x1 + pw, wall_top - s * 0.12), (x0 - pw, wall_top - s * 0.12)]], smooth=False)
    m["top"] = wall_top - s * 0.12
    return m


def paint_layer(art, W, H, m, depth, nx, lit_side=1):
    """depth 0 = far (pale gold haze) .. 1 = near (full colour, deep shade)."""
    k = depth
    haze = "#f0c676"
    def c(col, amt=1.0):
        return mix(haze, col, 0.25 + 0.75 * k * amt)
    art = GP(art, m["beam"], c(UMBER), c(UMBER_D), seed=nx(), rough=0.8, streak=1.2)
    art = GP(art, m["wall"], c(STONE), c(STONE_D, 0.6), seed=nx(), rough=0.8, streak=0.3)
    art = GP(art, np.maximum(m["cols"], m["piers"]), c(COL), c("#6a5a4c"), seed=nx(), rough=0.6, streak=0.3)
    art = wash(art, m["cols"] * np.clip((fbm(W, H, nx(), 8, 3) - 0.5) * 2.5, 0, 1), c("#4a5058"), 0.35, seed=nx())
    art = GP(art, m["caps"], c(STONE_L), c(STONE), seed=nx(), rough=0.5)
    for key_r, key_w in (("ur", "uw"), ("lr", "lw")):
        art = GP(art, m[key_r], c(BRICK), c(BRICK_L), seed=nx(), rough=0.6, streak=0.4)
        art = GP(art, m[key_w], c(STONE_L), c(STONE), seed=nx(), rough=0.6, streak=0.3)
    # shade on the side away from the light, brick texture flecks
    solid = np.maximum.reduce([m[x] for x in ("beam", "wall", "cols", "piers", "caps", "lr", "lw", "ur", "uw")])
    edge = np.clip(solid - np.roll(solid, 3 * lit_side, 1), 0, 1)
    art = wash(art, edge, "#2a170c", 0.35 * k, seed=nx())
    art = wash(art, np.clip(solid - np.roll(solid, -3 * lit_side, 1), 0, 1), "#ffe6a8", 0.4, seed=nx())
    art = wash(art, m["lr"] * np.clip((fbm(W, H, nx(), 4, 2) - 0.55) * 3, 0, 1), BRICK_D, 0.3 * k, seed=nx())
    # nearer layers stand in shadow against the lit depth; a little mottling so they read as painted
    art = wash(art, solid * (0.7 + 0.3 * fbm(W, H, nx(), 40, 2)), "#2a170c", 0.5 * k ** 1.6, seed=nx())
    return art, solid


if "hall" in PARTS:
    W, H = 760, 980
    nx = Seq(3100); rng = random.Random(31)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    VX, VY = W * 0.5, H * 0.56
    # deep golden haze at the end of the aisle
    art = painted_sky(W, H, [(0, "#1f130b"), (0.3, "#4a2c18"), (0.5, "#c88a44"), (0.56, "#f6d590"), (0.66, "#a8743e"), (1.0, "#2a1a10")], seed=nx())
    art = wash(art, radial(W, H, VX, VY, 240) ** 1.6, "#fff0c4", 0.8, seed=nx())
    # floor: polished stone catching the glow
    floor = (yy > VY).astype(np.float32)
    art = wash(art, floor * grad(W, H, 0, VY, 0, H), "#4a2c18", 0.8, seed=nx())
    # layers from far to near: bays get wider and taller, the aisle centre stays on VX
    depths = [0.08, 0.15, 0.26, 0.42, 0.66, 1.0]
    for i, f in enumerate(depths):
        k = i / (len(depths) - 1)
        bw = 120 + 520 * f            # central bay width
        s = bw * 0.78                  # column height
        by = VY + (H * 0.62 - 0) * f * 0.62
        xs = [VX - bw * 1.5, VX - bw * 0.5, VX + bw * 0.5, VX + bw * 1.5]
        # reflections of the columns on the floor (soft)
        for x0, x1 in zip(xs[:-1], xs[1:]):
            m = double_arch(W, H, x0, x1, by, s)
            art, solid = paint_layer(art, W, H, m, 0.15 + 0.85 * k, nx, lit_side=1 if x0 < VX else -1)
            refl = np.roll(m["cols"], int(s * 0.05), 0) * (yy > by) * np.clip(1 - (yy - by) / (s * 0.25), 0, 1)
            art = wash(art, gaussian_filter(refl, 2), "#2a170c", 0.25 * k, seed=nx())
        # gold light pooling between layers
        art = wash(art, radial(W, H, VX, VY, 160 + 260 * f) ** 2 * (1 - k) * 0.6, "#ffe3a0", 0.35, seed=nx())
        clr()
    # light shafts from high windows (right), very soft
    shaft = shapes(W, H, [[(W * 0.62, 0), (W * 0.78, 0), (W * 0.58, H * 0.72), (W * 0.48, H * 0.72)]], smooth=False)
    art = wash(art, gaussian_filter(shaft, 30), "#fff1c8", 0.22, seed=nx())
    dust = circles(W, H, [(rng.uniform(W * 0.45, W * 0.75), rng.uniform(40, H * 0.7), rng.uniform(0.6, 1.6)) for _ in range(70)]) * gaussian_filter(shaft, 30)
    art = wash(art, dust, "#fff7e0", 0.8, seed=nx())
    art = add_grain(art, seed=nx(), amount=0.035)
    art = vignette(art, 0.35, 1.8)
    show(art, "mc-hall")
    save_rgb(art, f"{OUT}/hall.webp", size=(720, 928), quality=76)
    clr()

if "frame" in PARTS:
    W, H = 600, 820
    nx = Seq(3200); rng = random.Random(32)
    cx, cy, r, d = 300, 330, 200, 40
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    full = np.ones((H, W), np.float32)
    opening = np.clip(shapes(W, H, [ellipse_pts(cx, cy, r, r, 90)]) + shapes(W, H, [[(cx - 184, cy + d - 4), (cx + 184, cy + d - 4), (cx + 184, H + 4), (cx - 184, H + 4)]], smooth=False), 0, 1)
    # alfiz panel (stone) around the arch, with carved spandrels
    art = GP(blank(W, H), full, STONE, STONE_L, seed=nx(), rough=0.4, streak=0.8)
    art = wash(art, np.clip((fbm(W, H, nx(), 30, 3) - 0.5) * 2, 0, 1), STONE_D, 0.25, seed=nx())
    # alfiz border (brick + gold line)
    border = np.clip(full - shapes(W, H, [[(26, 26), (W - 26, 26), (W - 26, H + 10), (26, H + 10)]], smooth=False), 0, 1)
    art = GP(art, border, BRICK, BRICK_L, seed=nx(), rough=0.4)
    gl = np.clip(shapes(W, H, [[(30, 30), (W - 30, 30), (W - 30, H + 10), (30, H + 10)]], smooth=False) - shapes(W, H, [[(36, 36), (W - 36, 36), (W - 36, H + 10), (36, H + 10)]], smooth=False), 0, 1)
    art = FO(art, gl, GOLD, seed=nx(), sparkle=0.08)
    # ataurique: palmette scrolls in the two spandrels (relief + gold)
    items, leaves = [], []
    for sgn in (-1, 1):
        bx, by_ = cx + sgn * 205, 120
        sp = spiral_pts(bx, by_, 50, 8, 0 if sgn > 0 else math.pi, 1.2, 50, -sgn)
        items.append((sp, 5, (0.0, 0.5)))
        for t in (0.15, 0.35, 0.55):
            px, py = sp[int(t * 49)]
            a = math.atan2(py - by_, px - bx)
            leaves.append(petal_pts(px, py, 30, 10, a + sgn * 0.6, n=10))
            leaves.append(petal_pts(px, py, 22, 7, a - sgn * 1.2, n=10))
    for sgn in (-1, 1):
        for (px, py, L, a) in [(cx + sgn * 150, 70, 34, -0.3), (cx + sgn * 230, 210, 30, 1.4), (cx + sgn * 236, 290, 26, 1.7), (cx + sgn * 90, 56, 26, 0.1)]:
            a = a if sgn > 0 else math.pi - a
            leaves += [petal_pts(px, py, L, L * 0.3, a + k * 0.5, n=10) for k in (-1, 0, 1)]
            items.append((spiral_pts(px, py, L * 0.5, 3, a + math.pi, 0.8, 20, sgn), 3, (0.0, 0.5)))
    rel = np.clip(strokes(W, H, items) + shapes(W, H, leaves), 0, 1) * (1 - gaussian_filter(opening, 3) * 1.2).clip(0, 1)
    art = GP(art, rel, STONE_L, STONE, seed=nx(), rough=0.5)
    art = wash(art, np.clip(rel - np.roll(np.roll(rel, -2, 0), -2, 1), 0, 1), "#7a5a36", 0.6, seed=nx())
    art = FO(art, rel * np.clip((fbm(W, H, nx(), 16, 3) - 0.4) * 2.5, 0, 1), GOLD, seed=nx(), sparkle=0.1)
    # voussoir ring of the horseshoe arch (red brick / cream stone, alternating)
    a0, a1 = horseshoe(cx, cy, r, d)
    red, white = voussoirs(W, H, cx, cy, r, r + 64, a0, a1, 21)
    art = GP(art, red, BRICK, BRICK_L, seed=nx(), rough=0.7, streak=1.2)
    art = wash(art, red * np.clip((fbm(W, H, nx(), 5, 2) - 0.5) * 3, 0, 1), BRICK_D, 0.35, seed=nx())
    art = GP(art, white, STONE_L, STONE, seed=nx(), rough=0.7, streak=0.8)
    joints = np.clip(np.maximum(red, white) - gaussian_filter(np.maximum(red, white), 0.1) * 0, 0, 1)
    seams = np.clip(red * np.roll(white, 2, 1) + white * np.roll(red, 2, 1) + red * np.roll(white, -2, 0) + white * np.roll(red, -2, 0), 0, 1)
    art = wash(art, gaussian_filter(seams, 0.8), "#5a3a22", 0.6, seed=nx())
    # thin gold rims
    rim = np.clip(shapes(W, H, [ellipse_pts(cx, cy, r + 70, r + 70, 120)]) - shapes(W, H, [ellipse_pts(cx, cy, r + 64, r + 64, 120)]), 0, 1) * (yy < cy + d + 12)
    rim2 = np.clip(shapes(W, H, [ellipse_pts(cx, cy, r + 4, r + 4, 120)]) - shapes(W, H, [ellipse_pts(cx, cy, r, r, 120)]), 0, 1) * (yy < cy + d)
    art = FO(art, np.clip(rim + rim2, 0, 1), GOLD, seed=nx(), sparkle=0.1)
    # columns with capitals (marble, with slight sheen) flanking the opening
    for sgn in (-1, 1):
        x = cx + sgn * 196
        col = shapes(W, H, [[(x - 14, cy + d + 30), (x + 14, cy + d + 30), (x + 16, H + 4), (x - 16, H + 4)]], smooth=False)
        art = GP(art, col, "#9a8a76", "#b8a890", seed=nx(), rough=0.5, streak=1.4)
        art = relief(art, col, 4, 0.5, light="#f0e4cc", dark="#3a2e22", lx=-0.8, ly=0, seed=nx())
        cap = shapes(W, H, [[(x - 26, cy + d + 34), (x + 26, cy + d + 34), (x + 34, cy + d - 2), (x - 34, cy + d - 2)]], smooth=False)
        art = GP(art, cap, STONE_L, STONE, seed=nx(), rough=0.4)
        art = FO(art, cap * np.clip((fbm(W, H, nx(), 6, 2) - 0.45) * 3, 0, 1), GOLD, seed=nx(), sparkle=0.1)
        art = wash(art, np.clip(cap - np.roll(cap, -3, 0), 0, 1), "#6a4a2a", 0.6, seed=nx())
    # cut the opening: fully transparent inside (the photo shows through), soft shadow on its rim
    shadow = np.clip(gaussian_filter(opening, 6) - opening, 0, 1)
    art = wash(art, shadow * 2.2, "#2a170c", 0.4, seed=nx())
    art[..., 3] *= (1 - opening)
    show(art, "mc-frame", bg="#3a2416")
    save_full(art, f"{OUT}/frame.webp", size=(480, 656), quality=82)
    clr()

if "frieze" in PARTS:
    W, H = 360, 270
    nx = Seq(3300)
    art = blank(W, H)
    for x0 in (0, 180):
        m = double_arch(W, H, x0, x0 + 180, H - 2, 80)
        art, _ = paint_layer(art, W, H, m, 1.0, nx)
    # wrap: the column at x=360 is the column at x=0
    art[:, -2:] = art[:, :2]
    show(art, "mc-frieze", bg="#f3e7d3")
    save_full(art, f"{OUT}/frieze.webp", size=(240, 180), quality=82)
    clr()

if "divider" in PARTS:
    W, H = 460, 90
    nx = Seq(3400)
    cx, cy = W / 2, H / 2
    items, leaves = [], []
    for sgn in (-1, 1):
        stem = curve([(cx + sgn * 26, cy), (cx + sgn * 80, cy - 14), (cx + sgn * 140, cy + 10), (cx + sgn * 200, cy - 4)], 50)
        items.append((stem, 3, (0.0, 0.6)))
        for t, up in ((0.2, -1), (0.45, 1), (0.7, -1), (0.92, 1)):
            px, py = stem[int(t * (len(stem) - 1))]
            leaves.append(petal_pts(px, py, 26 * (1 - t * 0.4), 8, -math.pi / 2 * up + sgn * 0.9, n=10))
            sp = spiral_pts(px + sgn * 10, py + up * 12, 9, 2, 0, 0.9, 20, sgn)
            items.append((sp, 2, (0.0, 0.5)))
    # central palmette (five fingers) over a little horseshoe arch
    leaves += [petal_pts(cx, cy + 8, 34, 8, -math.pi / 2 + a, n=12) for a in (-0.9, -0.45, 0, 0.45, 0.9)]
    m = np.clip(strokes(W, H, items) + shapes(W, H, leaves), 0, 1)
    art = blank(W, H)
    art = G(art, gaussian_filter(m, 4), "#8a5a2a", seed=nx(), density=0.18, edge=0.1, bloom=0, rough=1)
    art = FO(art, m, GOLD, seed=nx(), emboss=0.7, sparkle=0.1)
    art = GP(art, circles(W, H, [(cx, cy + 12, 6)]), BRICK, seed=nx(), rough=0.3)
    show(art, "mc-divider", bg="#f3e7d3")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)
    clr()

if "emblem" in PARTS:
    W, H = 220, 240
    nx = Seq(3500)
    cx, cy, r, d = 110, 110, 64, 16
    a0, a1 = horseshoe(cx, cy, r, d)
    red, white = voussoirs(W, H, cx, cy, r, r + 30, a0, a1, 13)
    art = blank(W, H)
    inner = np.clip(shapes(W, H, [ellipse_pts(cx, cy, r, r, 60)]) + shapes(W, H, [[(cx - 60, cy + d), (cx + 60, cy + d), (cx + 60, 230), (cx - 60, 230)]], smooth=False), 0, 1)
    art = G(art, inner, "#f4d488", "#e8b860", seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=1.5)
    art = GP(art, red, BRICK, BRICK_L, seed=nx(), rough=0.5)
    art = GP(art, white, STONE_L, STONE, seed=nx(), rough=0.5)
    cols = shapes(W, H, [[(x - 7, cy + d + 6), (x + 7, cy + d + 6), (x + 8, 232), (x - 8, 232)] for x in (cx - 66, cx + 66)], smooth=False)
    art = GP(art, cols, "#9a8a76", "#b8a890", seed=nx(), rough=0.4)
    caps = shapes(W, H, [[(x - 13, cy + d + 8), (x + 13, cy + d + 8), (x + 16, cy + d - 4), (x - 16, cy + d - 4)] for x in (cx - 66, cx + 66)], smooth=False)
    art = FO(art, caps, GOLD, seed=nx(), sparkle=0.1)
    show(art, "mc-emblem", bg="#f3e7d3")
    save(art, f"{OUT}/emblem.webp", max_w=140, quality=84)
    clr()
