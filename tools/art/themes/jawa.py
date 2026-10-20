"""Jawa Keraton — gold-foil & leather wayang gunungan, kawung/parang batik as linocut, foil ornaments.
Run: python3 -I /tmp/pen/art/themes/jawa.py
Assets → /root/w/frontend/public/themes/art/jawa/
  gunungan.webp  leather + gold-foil gunungan (tatah sungging look)   css 160x220 → 320x440
  kawung.webp    kawung batik tile, gold linocut on transparent        css 180px → 360px (repeat)
  parang.webp    parang batik tile, brown linocut on transparent       css 160px → 320px (repeat)
  lung.webp      lung-lungan scroll corner, gold foil (mirror in CSS)  css 150px → 300px
  divider.webp   gold foil divider ornament                            css 170x26 → 340x52
  paper.webp     cream paper grain tile                                 css 360px (repeat, opaque)
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p1_lib import *

OUT = outdir("jawa")
rng = random.Random(7)
nx = Seq(500)
GOLD, GOLD_L, GOLD_D = "#c9a24b", "#ecd389", "#8d6a22"
LEATHER, LEATHER_D = "#4a2c18", "#2a160c"

# ---------------- gunungan ----------------
W, H = 320, 440
C = W / 2
def profile(t):
    """half-width of the gunungan at height fraction t (0 = tip, 1 = base)."""
    return (0.02 + 0.98 * math.sin(math.pi * min(1, t * 0.78) ** 0.78) ** 0.9) * 0.46 * W * (0.86 + 0.14 * t)
outline = []
N = 60
for i in range(N + 1):
    t = i / N
    outline.append((C + profile(t), 10 + t * (H - 28)))
for i in range(N, -1, -1):
    t = i / N
    outline.append((C - profile(t), 10 + t * (H - 28)))
def scalloped(pts, depth=5.0, step=2):
    out = []
    for i, (x, y) in enumerate(pts):
        k = (i // step) % 2
        dx = (x - C) / max(1e-6, abs(x - C)) if abs(x - C) > 1 else 0
        out.append((x + dx * depth * (1 if k else 0.2) * (0.3 + 0.7 * min(1, (y - 10) / 80)), y))
    return out
leaf = shape_mask(W, H, scalloped(outline), smooth=True)
plinth = poly_mask(W, H, [(C - 0.3 * W, H - 24), (C + 0.3 * W, H - 24), (C + 0.3 * W, H - 6), (C - 0.3 * W, H - 6)])
leaf = np.maximum(leaf, plinth)
# leather body: warm ochre-brown with a lighter heart, worn uneven edge
body = gouache_paint(leaf, "#6b3d1f", "#4a2814", seed=nx(), rough=2.2, streak=0.5)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
heart = np.exp(-(((xx - C) / (0.28 * W)) ** 2 + ((yy - H * 0.5) / (0.32 * H)) ** 2))
body[..., :3] = np.clip(body[..., :3] * (0.82 + 0.4 * heart[..., None]), 0, 1)
rim = np.clip(leaf - gaussian_filter(leaf, 6) * 0.9, 0, 1)
wear = fbm(W, H, nx(), 7, 2)
body[..., 3] *= 1 - np.clip(rim * 2.2, 0, 1) * np.clip((wear - 0.55) * 4, 0, 1) * 0.9
art = body
inner = shape_mask(W, H, [(C + (x - C) * 0.9, 24 + (y - 24) * 0.92) for x, y in outline])
# sisik (scale) tooling filling the body: rows of little arcs, faint foil
sisik = np.zeros((H, W), np.float32)
for row in range(0, 30):
    y = 60 + row * 12.5
    off = (row % 2) * 7
    for col in range(-12, 13):
        x = C + col * 14 + off
        if 0 < x < W and 0 < y < H and inner[int(y), int(x)] > 0.5:
            sisik = np.maximum(sisik, stroke_mask(W, H, arc_pts(x, y, 5.5, math.pi * 1.1, math.pi * 1.9, 10), 1.5, taper=(0.2, 0.2)))
art = over(art, foil(sisik * 0.55, GOLD_D, seed=nx(), emboss=0.5, sparkle=0.05))
# tooled borders: outer thick foil rim + inner thin line
outer_rim = np.clip(leaf - gaussian_filter(leaf, 1.4), 0, 1); outer_rim = np.clip(outer_rim * 3.2, 0, 1)
border = np.clip((inner - gaussian_filter(inner, 2.2)) * 3.0, 0, 1)
art = over(art, foil(np.maximum(outer_rim, border), GOLD, seed=nx(), emboss=0.5, sparkle=0.1))

# tree of life: bold trunk, branches, large leaves
fil = np.zeros((H, W), np.float32)
trunk = curve([(C, H - 30), (C + 5, H - 120), (C - 4, H - 220), (C + 3, 130), (C, 70)], 80)
fil = np.maximum(fil, stroke_mask(W, H, trunk, 13, taper=(0.02, 0.3)))
branches = []
for k, (y0, side, L) in enumerate([(H - 96, -1, 112), (H - 96, 1, 112), (H - 170, -1, 104), (H - 170, 1, 104), (H - 240, -1, 86), (H - 240, 1, 86), (H - 300, -1, 62), (H - 300, 1, 62), (124, -1, 36), (124, 1, 36)]):
    pts = curve([(C, y0), (C + side * L * 0.45, y0 - L * 0.26), (C + side * L * 0.85, y0 - L * 0.55), (C + side * L, y0 - L * 0.98)], 40)
    fil = np.maximum(fil, stroke_mask(W, H, pts, 7, taper=(0.05, 0.4)))
    branches.append((pts, side))
    tip = pts[-1]
    curl = arc_pts(tip[0] + side * 7, tip[1] - 9, 12, math.pi / 2, math.pi / 2 + side * 4.4, 26)
    fil = np.maximum(fil, stroke_mask(W, H, curl, 3.6, taper=(0.1, 0.5)))
leaves = np.zeros((H, W), np.float32)
for pts, side in branches:
    for j in range(4, len(pts) - 2, 8):
        x, y = pts[j]
        ang = -math.pi / 2 + side * rng.uniform(0.45, 1.0)
        leaves = np.maximum(leaves, leaf_mask(W, H, x, y, rng.uniform(20, 30), rng.uniform(6, 8.5), ang, n=10, cup=0.25))
        ang2 = -math.pi / 2 + side * rng.uniform(1.7, 2.3)
        leaves = np.maximum(leaves, leaf_mask(W, H, x, y, rng.uniform(14, 20), rng.uniform(4.5, 6.5), ang2, n=10, cup=0.25))
# flame finial at the tip + small bird/kinara silhouettes replaced by lotus buds along the trunk
flame = shape_mask(W, H, deform(petal_pts(C, 56, 48, 10, -math.pi / 2, n=12), rng, 2, 0.08))
flame = np.maximum(flame, leaf_mask(W, H, C - 8, 70, 26, 6, -math.pi / 2 - 0.6, n=10))
flame = np.maximum(flame, leaf_mask(W, H, C + 8, 70, 26, 6, -math.pi / 2 + 0.6, n=10))
# base gate (kayon door) with lintel and steps
gate = poly_mask(W, H, [(C - 34, H - 24), (C + 34, H - 24), (C + 30, H - 84), (C - 30, H - 84)])
gate_hole = np.maximum(poly_mask(W, H, [(C - 25, H - 29), (C - 3, H - 29), (C - 3, H - 76), (C - 22, H - 76)]),
                       poly_mask(W, H, [(C + 3, H - 29), (C + 25, H - 29), (C + 22, H - 76), (C + 3, H - 76)]))
gate = np.clip(gate - gate_hole, 0, 1)
steps = np.zeros((H, W), np.float32)
for q in range(3):
    steps = np.maximum(steps, stroke_mask(W, H, [(C - 48 - q * 10, H - 22 + q * 5), (C + 48 + q * 10, H - 22 + q * 5)], 2.2, taper=(0.05, 0.05)))
# lar (wings): fans of tapered feather strokes sweeping outward-up from the shoulders
wings = np.zeros((H, W), np.float32)
for side in (-1, 1):
    sx0, sy0 = C + side * 40, H - 112
    for q in range(6):
        a = (-0.1 - q * 0.16) if side > 0 else (math.pi + 0.1 + q * 0.16)
        L = 64 - q * 5
        pts = curve([(sx0, sy0), (sx0 + math.cos(a) * L * 0.5, sy0 + math.sin(a) * L * 0.5 + 3), (sx0 + math.cos(a) * L, sy0 + math.sin(a) * L)], 20)
        wings = np.maximum(wings, stroke_mask(W, H, pts, 7.5 - q * 0.7, taper=(0.1, 0.5)))
# perforation field (tatahan)
holes = np.zeros((H, W), np.float32)
for _ in range(300):
    x = rng.uniform(C - 0.45 * W, C + 0.45 * W); y = rng.uniform(70, H - 40)
    if leaf[int(y), int(x)] < 0.5 or inner[int(y), int(x)] < 0.5:
        continue
    holes = np.maximum(holes, circle_mask(W, H, x, y, rng.uniform(1.3, 2.4)))
gold_all = np.maximum.reduce([fil, leaves, flame, gate, wings, steps])
holes *= (1 - np.clip(gaussian_filter(gold_all, 2.5) * 3, 0, 1))
art[..., 3] *= 1 - holes * 0.85
art = over(art, soft_shadow(gold_all, "#120804", blur=2.5, strength=0.7, dx=1, dy=2))
art = over(art, foil(fil, GOLD, seed=nx(), emboss=0.7, sparkle=0.15))
art = over(art, foil(leaves, mix(GOLD, GOLD_L, 0.45), seed=nx(), emboss=0.8, sparkle=0.12))
art = over(art, foil(flame, GOLD_L, seed=nx(), emboss=0.8, sparkle=0.2))
art = over(art, foil(gate, GOLD, seed=nx(), emboss=0.6, sparkle=0.1))
art = over(art, foil(np.maximum(wings, steps), GOLD_D, seed=nx(), emboss=0.8, sparkle=0.1))
# leaf midribs in dark ink
mid = np.zeros((H, W), np.float32)
for pts, side in branches:
    for j in range(4, len(pts) - 2, 8):
        x, y = pts[j]
        ang = -math.pi / 2 + side * 0.7
        mid = np.maximum(mid, stroke_mask(W, H, [(x + math.cos(ang) * 4, y + math.sin(ang) * 4), (x + math.cos(ang) * 18, y + math.sin(ang) * 18)], 1.3))
art = over(art, gouache_paint(mid, LEATHER_D, seed=nx(), rough=0.4, density=0.6))
# sungging red accents at the plinth and inside the gate doors
ochre = np.zeros((H, W), np.float32)
for k in range(9):
    ochre = np.maximum(ochre, circle_mask(W, H, C - 72 + k * 18, H - 15, 3.2))
art = over(art, gouache_paint(ochre, "#9c3a2a", "#c25a3e", seed=nx(), rough=0.8))
art = over(art, gouache_paint(gate_hole * 0.9, "#7a2a1e", "#a0402c", seed=nx(), rough=0.8, density=0.8))
# worn gold
rub = np.clip((fbm(W, H, nx(), 9, 2) - 0.62) * 5, 0, 1) * gaussian_filter(gold_all, 0.5)
art[..., :3] = art[..., :3] * (1 - rub[..., None] * 0.35) + np.array(hex_rgb(LEATHER), np.float32) * rub[..., None] * 0.35
art = add_grain(art, nx(), 0.03)
save(art, f"{OUT}/gunungan.webp", max_w=320)
preview(art, "jw-gunungan", bg="#2b1a10")

# ---------------- kawung tile (gold linocut) ----------------
T = 360
kaw = np.zeros((T, T), np.float32)
cell = T / 2
for i in range(-1, 3):
    for j in range(-1, 3):
        cx, cy = i * cell + cell / 2, j * cell + cell / 2
        for ang in (0, math.pi / 2):
            for sgn in (-1, 1):
                a = ang + (math.pi / 4 if sgn > 0 else -math.pi / 4) + math.pi / 4 * (1 - sgn) + rng.uniform(-0.02, 0.02)
            # four ellipses pointing diagonally from the cell corner
        for q in range(4):
            a = math.pi / 4 + q * math.pi / 2
            ex, ey = cx + math.cos(a) * cell * 0.34, cy + math.sin(a) * cell * 0.34
            ring = ring_mask(T, T, ex, ey, 1, 1)  # placeholder (unused)
            el = shape_mask(T, T, ellipse_pts(ex, ey, cell * 0.33, cell * 0.17, 18, a))
            inner_el = shape_mask(T, T, ellipse_pts(ex, ey, cell * 0.25, cell * 0.10, 18, a))
            kaw = np.maximum(kaw, np.clip(el - inner_el, 0, 1))
            # seeds: two dots inside each ellipse
            for s_ in (-1, 1):
                kaw = np.maximum(kaw, circle_mask(T, T, ex + math.cos(a) * s_ * cell * 0.12, ey + math.sin(a) * s_ * cell * 0.12, cell * 0.028))
        # four-petal star between the rosettes
        for q in range(4):
            a = q * math.pi / 2
            kaw = np.maximum(kaw, leaf_mask(T, T, cx + math.cos(a) * cell * 0.03, cy + math.sin(a) * cell * 0.03, cell * 0.11, cell * 0.035, a, n=8))
kaw = tile_wrap(kaw)
kawung = linocut(kaw, GOLD, seed=nx(), wear=0.55, rough=1.6)
save_full(kawung, f"{OUT}/kawung.webp", quality=80)
preview(kawung, "jw-kawung", bg="#2b1a10")

# ---------------- parang tile (brown linocut, light) ----------------
T2 = 320
par = np.zeros((T2, T2), np.float32)
# diagonal rows of S-blades (parang rusak inspired), 45 deg
for row in range(-3, 7):
    for k in range(-3, 7):
        ox = k * 80 + row * 32 - 40
        oy = row * 64 - 40
        # blade: an S from (0,0) to (46,-46) along the diagonal
        pts = curve([(ox, oy), (ox + 10, oy - 22), (ox + 26, oy - 28), (ox + 44, oy - 50), (ox + 58, oy - 54)], 30)
        par = np.maximum(par, stroke_mask(T2, T2, pts, 7, taper=(0.3, 0.3)))
        # mlinjon diamond between blades
        d = 40
        par = np.maximum(par, poly_mask(T2, T2, [(ox + d, oy - d + 6), (ox + d + 6, oy - d), (ox + d, oy - d - 6), (ox + d - 6, oy - d)]))
        par = np.maximum(par, circle_mask(T2, T2, ox + 30, oy - 10, 2.2))
par = tile_wrap(par)
parang = linocut(par, "#6a4a2c", seed=nx(), wear=0.4, rough=1.0)
save_full(parang, f"{OUT}/parang.webp", quality=78)
preview(parang, "jw-parang", tone="#efe3ca")

# ---------------- lung-lungan corner (foil scroll) ----------------
W3, H3 = 300, 300
lung = np.zeros((H3, W3), np.float32)
def spiral(cx, cy, r0, r1, a0, turns, n=60, ccw=1):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        a = a0 + ccw * t * turns * math.tau
        r = r0 + (r1 - r0) * t
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts
main = curve([(6, 294), (40, 250), (60, 190), (110, 150), (170, 120), (240, 100), (292, 96)], 90)
lung = np.maximum(lung, stroke_mask(W3, H3, main, 7, taper=(0.02, 0.25)))
main2 = curve([(8, 290), (30, 220), (54, 150), (90, 90), (112, 40), (118, 8)], 80)
lung = np.maximum(lung, stroke_mask(W3, H3, main2, 7, taper=(0.02, 0.25)))
for (cx, cy, r, a0, ccw) in [(258, 108, 22, math.pi, 1), (110, 20, 18, 0.4, -1), (150, 128, 20, 2.6, -1), (80, 170, 16, 1.0, 1), (62, 100, 14, -0.6, 1), (200, 110, 12, 0.3, 1)]:
    sp = spiral(cx, cy, r, 2, a0, 0.85, 40, ccw)
    lung = np.maximum(lung, stroke_mask(W3, H3, sp, 5, taper=(0.05, 0.4)))
lvs = np.zeros((H3, W3), np.float32)
for (x, y, L, Wd, a) in [(140, 140, 44, 11, -2.2), (184, 116, 38, 10, -1.9), (226, 100, 30, 8, -2.4), (96, 162, 36, 10, -2.8), (66, 210, 40, 11, -0.7), (44, 250, 30, 9, -0.9),
                         (104, 72, 38, 10, -0.3), (88, 120, 30, 8, 0.2), (118, 36, 24, 7, 0.9), (170, 134, 26, 7, 0.9), (36, 180, 26, 7, 2.4)]:
    lvs = np.maximum(lvs, leaf_mask(W3, H3, x, y, L, Wd, a, n=10, cup=0.3))
buds = np.zeros((H3, W3), np.float32)
for (x, y, r) in [(258, 108, 6), (110, 20, 5), (150, 128, 5), (80, 170, 4.5), (62, 100, 4), (200, 110, 3.5), (292, 96, 4), (118, 8, 4)]:
    buds = np.maximum(buds, circle_mask(W3, H3, x, y, r))
corner = over(blank(W3, H3), soft_shadow(np.maximum.reduce([lung, lvs, buds]), "#000000", blur=3, strength=0.5, dx=1, dy=2))
corner = over(corner, foil(lung, GOLD, seed=nx(), emboss=0.7, sparkle=0.12))
corner = over(corner, foil(lvs, GOLD_L, seed=nx(), emboss=0.9, sparkle=0.15))
corner = over(corner, foil(buds, GOLD_D, seed=nx(), emboss=0.9, sparkle=0.1))
# leaf midribs (dark, tooled)
mid = np.zeros((H3, W3), np.float32)
for (x, y, L, Wd, a) in [(140, 140, 44, 11, -2.2), (184, 116, 38, 10, -1.9), (96, 162, 36, 10, -2.8), (66, 210, 40, 11, -0.7), (104, 72, 38, 10, -0.3)]:
    mid = np.maximum(mid, stroke_mask(W3, H3, [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in (0.1, 0.4, 0.7, 0.85)], 1.6))
corner = over(corner, gouache_paint(mid, LEATHER_D, seed=nx(), rough=0.5, density=0.7))
save(corner, f"{OUT}/lung.webp", max_w=300)
preview(corner, "jw-lung", bg="#2b1a10")

# ---------------- divider ornament (foil) ----------------
W4, H4 = 340, 52
dv = np.zeros((H4, W4), np.float32)
cy = H4 / 2
for side in (-1, 1):
    line = curve([(W4 / 2 + side * 26, cy), (W4 / 2 + side * 80, cy - 1), (W4 / 2 + side * 130, cy + 1), (W4 / 2 + side * 162, cy)], 40)
    dv = np.maximum(dv, stroke_mask(W4, H4, line, 2.6, taper=(0.02, 0.55)))
    sp = spiral(W4 / 2 + side * 140, cy - 7, 8, 1.5, math.pi / 2 if side > 0 else math.pi / 2, 0.8, 30, side)
    dv = np.maximum(dv, stroke_mask(W4, H4, sp, 2.2, taper=(0.1, 0.5)))
    dv = np.maximum(dv, leaf_mask(W4, H4, W4 / 2 + side * 60, cy - 2, 20, 5, -math.pi / 2 + side * 0.9, n=10))
    dv = np.maximum(dv, leaf_mask(W4, H4, W4 / 2 + side * 100, cy + 1, 16, 4.5, math.pi / 2 - side * 1.1, n=10))
# centre: diamond jewel + two small petals
dv = np.maximum(dv, poly_mask(W4, H4, wobble([(W4 / 2, cy - 12), (W4 / 2 + 11, cy), (W4 / 2, cy + 12), (W4 / 2 - 11, cy)], rng, 0.4)))
dv = np.maximum(dv, leaf_mask(W4, H4, W4 / 2, cy - 6, 14, 4, -math.pi / 2, n=10))
dv = np.maximum(dv, leaf_mask(W4, H4, W4 / 2, cy + 6, 14, 4, math.pi / 2, n=10))
divider = over(blank(W4, H4), soft_shadow(dv, "#000000", blur=1.5, strength=0.35, dx=0, dy=1))
divider = over(divider, foil(dv, GOLD, seed=nx(), emboss=0.8, sparkle=0.15))
save_full(divider, f"{OUT}/divider.webp", quality=84)
preview(divider, "jw-divider", tone="#f5eddc")

# ---------------- paper tile ----------------
P = 360
pap = paper(P, P, "#f5eddc", seed=4, fiber=0.8, mottle=0.9)
pa = np.asarray(pap, np.float32) / 255
# seam blend
pa_rgba = np.concatenate([pa, np.ones((P, P, 1), np.float32)], -1)
for ch in range(3):
    pa_rgba[..., ch] = tile_wrap(pa_rgba[..., ch])
save_rgb(pa_rgba, f"{OUT}/paper.webp", quality=74)
print("total KB:", sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1024)
