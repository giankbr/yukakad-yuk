"""Bali Kuning — watercolour kamboja (frangipani) sprays, gouache candi bentar gate, woven poleng accents.
Run: python3 -I /tmp/pen/art/themes/bali-kuning.py
Assets → /root/w/frontend/public/themes/art/bali-kuning/
  cover.webp    candi bentar gate with kamboja sprays (transparent)   css 390x~400 → 780x800
  spray.webp    kamboja spray corner piece (watercolour)              css 170px → 340px
  flower.webp   single kamboja bloom (watercolour)                    css 60px → 120px
  divider.webp  gold line + kamboja divider                           css 170x30 → 340x60
  poleng.webp   woven poleng check tile (gouache)                     css 24px → 48px (repeat)
  paper.webp    cream paper tile                                      css 360px (repeat, opaque)
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _r1_lib import *

OUT = outdir("bali-kuning")
rng = random.Random(33)
nx = Seq(1300)
GOLD, GOLD_D = "#b8860b", "#8a6508"
CREAM = "#fbf3dc"
PET_W, PET_S, PET_Y, PET_Y2 = "#fffdf4", "#e6d7b4", "#f5c842", "#e8a51c"
GREENS = [("#6f8f5a", "#4d6b3c"), ("#7f9c66", "#587448"), ("#5f7f4c", "#3f5a31")]

# ---------------- kamboja bloom painter ----------------
def bloom(W, H, cx, cy, r, ang0=0.0, tilt=1.0, layer=None, shadow_col=PET_S):
    """Paint a frangipani: 5 overlapping pinwheel petals, white with warm shadow and a yellow throat."""
    layer = blank(W, H) if layer is None else layer
    area = np.zeros((H, W), np.float32)
    petals = []
    for k in range(5):
        a = ang0 + k * math.tau / 5 + rng.uniform(-0.08, 0.08)
        L = r * rng.uniform(0.92, 1.05); Wd = r * 0.46
        pts = petal_pts(cx + math.cos(a) * r * 0.06, cy + math.sin(a) * r * 0.06 * tilt, L, Wd, a, n=14, cup=0.35)
        # pinwheel: skew the petal so one edge is straighter (overlap)
        pts = [(x + math.cos(a + math.pi / 2) * Wd * 0.28, y + math.sin(a + math.pi / 2) * Wd * 0.28 * tilt) for x, y in pts]
        pts = [(cx + (x - cx), cy + (y - cy) * tilt) for x, y in pts]
        m = shape_mask(W, H, deform(pts, rng, 2, 0.05))
        petals.append((m, a))
        area = np.maximum(area, m)
    # whole flower: soft white body first (opaque-ish so it reads on cream)
    body = gouache_paint(area, PET_W, "#fdf8e8", seed=nx(), rough=1.2, streak=0.2, density=0.9)
    layer = over(layer, body)
    # per-petal shading: a warm wash along the trailing edge + a fold line toward the throat
    for m, a in petals:
        edge = np.clip(m - np.roll(np.roll(m, int(math.cos(a + math.pi / 2) * r * 0.16), 1), int(math.sin(a + math.pi / 2) * r * 0.16 * tilt), 0), 0, 1)
        layer = glaze(layer, pigment(edge * m, shadow_col, "#efe3c6", seed=nx(), density=0.5, edge=0.4, bloom=0.3, rough=3, feather=1.2))
        fold = stroke_mask(W, H, [(cx + math.cos(a) * r * 0.1, cy + math.sin(a) * r * 0.1 * tilt), (cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55 * tilt)], r * 0.08, taper=(0.1, 0.6))
        layer = glaze(layer, pigment(fold, "#e3d4ad", seed=nx(), density=0.35, edge=0.2, bloom=0, rough=2, feather=1.5))
    # yellow throat: radial wash that bleeds out along the petals
    throat = circle_mask(W, H, cx, cy, r * 0.42)
    throat = gaussian_filter(throat, r * 0.12) * area
    layer = glaze(layer, pigment(np.clip(throat * 1.3, 0, 1), PET_Y, PET_Y2, seed=nx(), density=0.75, edge=0.3, bloom=0.3, rough=3, feather=1.0))
    core = circle_mask(W, H, cx, cy, r * 0.12)
    layer = glaze(layer, pigment(core, PET_Y2, seed=nx(), density=0.6, edge=0.5, bloom=0, rough=1.5))
    return layer, area

def leaf(W, H, x, y, L, Wd, a, layer, greens):
    ca, cb = greens
    m = shape_mask(W, H, deform(petal_pts(x, y, L, Wd, a, n=12), rng, 2, 0.06))
    layer = glaze(layer, pigment(m, ca, cb, seed=nx(), density=0.7, edge=0.5, bloom=0.4, rough=5, holes=0.05))
    half = shape_mask(W, H, petal_pts(x, y, L * 0.95, Wd * 0.45, a + 0.05, n=10))
    layer = glaze(layer, pigment(half, cb, seed=nx(), density=0.3, edge=0.3, bloom=0.2, rough=3))
    vein = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in (0.08, 0.3, 0.55, 0.8)]
    layer = glaze(layer, pigment(stroke_mask(W, H, vein, 2.2), mix(cb, "#1f2b1d", 0.4), seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1.5, feather=0.6))
    return layer, m

def spray(W, H, origin, direction, n_flowers, scale, leaves):
    """A spray: leaves first (behind), then blooms + buds."""
    lv = blank(W, H); fl = blank(W, H); fl_area = np.zeros((H, W), np.float32)
    ox, oy = origin
    for (dx, dy, L, Wd, a) in leaves:
        lv, _ = leaf(W, H, ox + dx * scale, oy + dy * scale, L * scale, Wd * scale, a, lv, GREENS[rng.randrange(3)])
    for (dx, dy, r, a0, t) in n_flowers:
        fl, m = bloom(W, H, ox + dx * scale, oy + dy * scale, r * scale, a0, t, fl)
        fl_area = np.maximum(fl_area, m)
    # soft shadow of the flowers on the leaves
    lv = glaze(lv, pigment(gaussian_filter(fl_area, 6) * (1 - fl_area), "#8d7a52", seed=nx(), density=0.25, edge=0, bloom=0, rough=2))
    lv = knockout(lv, fl_area, amount=0.95, grow=3)
    return over(lv, fl)

# ---------------- cover: candi bentar + tedung + sprays ----------------
# Light from the upper left. Palette: brick red, paras grey, sage, kamboja white/yellow, prada gold.
W, H = 780, 820
BASE = 610            # ground line of the gate
GAP = 66              # half-gap between the two split faces
BRICK, BRICK2 = "#a9583b", "#b8694a"
PARAS, PARAS2, PARAS_D = "#a39b86", "#b5ad97", "#6e6756"
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cover = blank(W, H)

# -- backdrop: pale sky bloom, distant hills, two coconut palms (all transparent watercolour)
sky = shape_mask(W, H, deform(ellipse_pts(W / 2, 360, 330, 270, 14), rng, 2, 0.08))
cover = glaze(cover, pigment(sky, "#f1e5c2", "#f4ead0", seed=nx(), density=0.42, edge=0.3, bloom=0.55, rough=14, feather=3))
sun = circle_mask(W, H, W / 2 + 6, 330, 74)
cover = glaze(cover, pigment(sun, "#f3d27a", "#f0c860", seed=nx(), density=0.38, edge=0.45, bloom=0.3, rough=4, feather=2.5))
hill = poly_mask(W, H, [(0, 520)] + [(x, 470 - 50 * math.sin(x / W * math.pi * 1.4 + 0.6) - 18 * math.sin(x / 61)) for x in range(0, W + 20, 20)] + [(W, H), (0, H)])
cover = glaze(cover, pigment(hill, "#b9c0a0", "#c9c9a8", seed=nx(), density=0.38, edge=0.4, bloom=0.4, rough=8, feather=2))
hill2 = poly_mask(W, H, [(0, 560)] + [(x, 528 - 22 * math.sin(x / W * math.pi * 2.3 + 2.0)) for x in range(0, W + 20, 20)] + [(W, H), (0, H)])
cover = glaze(cover, pigment(hill2, "#97a77d", "#a8b18a", seed=nx(), density=0.42, edge=0.45, bloom=0.35, rough=8, feather=2))


def palm(px, base_y, top_y, lean, layer, col=("#a3b29a", "#97a893")):
    trunk = curve([(px, base_y), (px + lean * 0.4, (base_y + top_y) / 2), (px + lean, top_y)], 40)
    m = stroke_mask(W, H, trunk, 8, taper=(0.02, 0.3))
    layer = glaze(layer, pigment(m, "#a8a58f", seed=nx(), density=0.5, edge=0.4, bloom=0, rough=2, feather=1))
    tx, ty = px + lean, top_y
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.1, 0.1)
        L = rng.uniform(70, 98)
        droop = 0.55 + abs(k - 4) * 0.12
        pts = curve([(tx, ty), (tx + math.cos(a) * L * 0.55, ty + math.sin(a) * L * 0.55 - 6), (tx + math.cos(a) * L, ty + math.sin(a) * L * (1 - droop) + L * droop * 0.5)], 30)
        fm = stroke_mask(W, H, pts, 17, taper=(0.08, 0.8))
        # leaflets: comb the frond with fine cuts so it reads as a coconut leaf, not a ribbon
        cuts = (np.sin((xx * math.cos(a + 1.1) + yy * math.sin(a + 1.1)) / 2.2) > 0.55).astype(np.float32)
        fm = fm * (1 - cuts * 0.85 * np.clip(fm - stroke_mask(W, H, pts, 3, taper=(0.05, 0.8)), 0, 1))
        layer = glaze(layer, pigment(fm, *col, seed=nx(), density=0.42, edge=0.45, bloom=0.2, rough=2.5, feather=0.8))
    return layer


cover = palm(118, 540, 270, 24, cover)
cover = palm(672, 548, 300, -30, cover)
cover = palm(606, 556, 380, -10, cover, ("#b3bea8", "#a9b5a0"))


# -- candi bentar: two split towers. Profile is built per side as a list of tiers (outer x offset from the cut face).
def tier_poly(side, y0, y1, w0, w1, concave=0.0):
    """Quad from the cut face (x=cut) outward; the outer edge bows inward (concave) a little, hand-wobbled."""
    cut = W / 2 + side * GAP
    pts = [(cut, y0)]
    for i in range(7):
        t = i / 6
        wx = w0 + (w1 - w0) * t - concave * math.sin(math.pi * t)
        pts.append((cut + side * wx, y0 + (y1 - y0) * t))
    pts.append((cut, y1))
    return wobble(pts, rng, 0.7)


def tower(side):
    cut = W / 2 + side * GAP
    body = np.zeros((H, W), np.float32); paras = np.zeros((H, W), np.float32); carve = np.zeros((H, W), np.float32)
    gold = np.zeros((H, W), np.float32); lips = []
    # foot (bebaturan) with a stepped plinth
    body = np.maximum(body, poly_mask(W, H, tier_poly(side, BASE, BASE - 58, 150, 142)))
    p = tier_poly(side, BASE - 58, BASE - 70, 152, 152); paras = np.maximum(paras, poly_mask(W, H, p)); lips.append(p)
    # body (badan) with a carved paras panel
    body = np.maximum(body, poly_mask(W, H, tier_poly(side, BASE - 70, BASE - 196, 132, 126, concave=4)))
    px0, px1 = cut + side * 28, cut + side * 104
    panel = poly_mask(W, H, wobble([(px0, BASE - 84), (px1, BASE - 84), (px1, BASE - 182), (px0, BASE - 182)], rng, 0.8))
    paras = np.maximum(paras, panel)
    pcx = (px0 + px1) / 2
    # patra (leafy scroll) carving in the panel: mirrored swirls
    for k in range(3):
        cy = BASE - 106 - k * 28
        for sgn in (-1, 1):
            sw = [(pcx, cy + 10), (pcx + sgn * 10, cy + 2), (pcx + sgn * 22, cy - 2), (pcx + sgn * 26, cy - 12), (pcx + sgn * 18, cy - 16), (pcx + sgn * 14, cy - 10)]
            carve = np.maximum(carve, stroke_mask(W, H, curve(sw, 24), 3.2, taper=(0.1, 0.4)))
    carve = np.maximum(carve, stroke_mask(W, H, [(pcx, BASE - 90), (pcx, BASE - 176)], 2.2, taper=(0.2, 0.2)))
    gold = np.maximum(gold, circle_mask(W, H, pcx, BASE - 134, 5))
    p = tier_poly(side, BASE - 196, BASE - 210, 140, 144); paras = np.maximum(paras, poly_mask(W, H, p)); lips.append(p)
    # head (kepala): diminishing tiers, each with an upturned horn (ikut celedu) at the outer corner
    y = BASE - 210; wdt = 128; hgt = 40
    for k in range(8):
        y1 = y - hgt
        body = np.maximum(body, poly_mask(W, H, tier_poly(side, y, y1, wdt, wdt * 0.92, concave=3)))
        lip = tier_poly(side, y1 + 3, y1 - 6, wdt * 0.98 + 4, wdt * 0.98 + 6)
        paras = np.maximum(paras, poly_mask(W, H, lip)); lips.append(lip)
        hx = cut + side * (wdt + 5); hy = y1 - 4
        horn = curve([(hx - side * 9, hy), (hx + side * 2, hy - 6 - hgt * 0.12), (hx + side * 6, hy - 14 - hgt * 0.22)], 16)
        paras = np.maximum(paras, stroke_mask(W, H, horn, 5.5 - k * 0.35, taper=(0.05, 0.9)))
        if k % 2 == 0 and wdt > 40:
            # small carved niche
            nx0 = cut + side * wdt * 0.42
            carve = np.maximum(carve, shape_mask(W, H, ellipse_pts(nx0, y - hgt * 0.5, 5, hgt * 0.26, 8)))
        y = y1 - 6; wdt *= 0.8; hgt = max(14, hgt * 0.86)
    # finial (murdha)
    fin = [(cut, y), (cut + side * 16, y), (cut + side * 6, y - 26), (cut, y - 34)]
    paras = np.maximum(paras, shape_mask(W, H, wobble(fin, rng, 0.6)))
    gold = np.maximum(gold, circle_mask(W, H, cut + side * 5, y - 30, 3.6))
    return body, paras, carve, gold, lips


towers = blank(W, H); tmask = np.zeros((H, W), np.float32)
joints, tone = brick_field(W, H, nx())
shade_x = np.clip((xx - W * 0.25) / (W * 0.75), 0, 1)   # light from the left
for side in (-1, 1):
    body, paras, carve, gold, lips = tower(side)
    cut = W / 2 + side * GAP
    tmask = np.maximum(tmask, np.maximum(body, paras))
    stone = gouache_paint(body, BRICK, BRICK2, seed=nx(), rough=1.6, streak=0.9)
    rgb = stone[..., :3]
    rgb *= (0.9 + 0.2 * tone)[..., None]
    rgb[:] = rgb * (1 - joints[..., None] * 0.22) + np.array(hex_rgb("#e3c9a6"), np.float32) * joints[..., None] * 0.22
    # the split face catches light on the right tower, falls in shadow on the left tower
    face = np.clip(1 - np.abs(xx - cut) / 22, 0, 1) * body
    rgb *= (1 - (face * (0.22 if side < 0 else -0.08))[..., None])
    rgb *= (1 - shade_x[..., None] * 0.2)
    towers = over(towers, stone)
    # ambient occlusion under each lip
    lipm = np.zeros((H, W), np.float32)
    for lp in lips:
        lipm = np.maximum(lipm, poly_mask(W, H, lp))
    ao = np.clip(np.roll(gaussian_filter(lipm, 2.5), 5, 0) - lipm, 0, 1) * body
    towers = glaze(towers, pigment(ao, "#5a2e22", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=1.5, feather=1))
    ps = gouache_paint(paras, PARAS, PARAS2, seed=nx(), rough=1.1, streak=0.6)
    ps[..., :3] *= (1 - shade_x[..., None] * 0.18)[...]
    towers = over(towers, ps)
    towers = over(towers, gouache_paint(carve, PARAS_D, "#7d7564", seed=nx(), rough=0.8, density=0.9))
    towers = over(towers, foil(gold, GOLD, seed=nx(), emboss=0.6, sparkle=0.1))
# weathering: lichen + soot washes, kept inside the stone
towers = glaze(towers, pigment(np.clip((fbm(W, H, nx(), 28, 3) - 0.62) * 4, 0, 1) * tmask, "#6f7d4c", seed=nx(), density=0.32, edge=0.2, bloom=0.3, rough=3))
towers = glaze(towers, pigment(np.clip((fbm(W, H, nx(), 46, 3) - 0.55) * 3, 0, 1) * tmask, "#5d5040", seed=nx(), density=0.22, edge=0.1, bloom=0.3, rough=5))
# outline in dark sepia ink, broken (a painter's contour, not a vector stroke)
edge = np.clip(tmask - gaussian_filter(tmask, 1.1) * 1.0, 0, 1) * 3
edge *= np.clip((fbm(W, H, nx(), 9, 2) - 0.3) * 3, 0, 1)
towers = over(towers, linocut(np.clip(edge, 0, 1), "#4a2a1e", seed=nx(), wear=0.3, rough=0.6))

# steps up through the gap + stone path
steps = np.zeros((H, W), np.float32)
for q in range(4):
    yb = BASE + 4 - q * 11
    hw = GAP + 26 - q * 7
    steps = np.maximum(steps, poly_mask(W, H, wobble([(W / 2 - hw, yb), (W / 2 + hw, yb), (W / 2 + hw - 2, yb - 11), (W / 2 - hw + 2, yb - 11)], rng, 0.7)))
path = poly_mask(W, H, wobble([(W / 2 - GAP - 30, BASE + 4), (W / 2 + GAP + 30, BASE + 4), (W / 2 + 150, H - 120), (W / 2 - 150, H - 120)], rng, 1.0))
grass = poly_mask(W, H, [(0, BASE - 6)] + [(x, BASE - 8 + 6 * math.sin(x / 23)) for x in range(0, W + 10, 10)] + [(W, H - 110), (0, H - 110)])
gfade = np.clip((H - 110 - yy) / 90, 0, 1)
cover = glaze(cover, pigment(grass * gfade, "#9aab78", "#b4bc8b", seed=nx(), density=0.42, edge=0.3, bloom=0.5, rough=10, feather=3))
cover = glaze(cover, pigment(path * np.clip((H - 120 - yy) / 120, 0, 1), "#cdbf9f", "#bfb090", seed=nx(), density=0.5, edge=0.3, bloom=0.3, rough=5, feather=2))
cover = over(cover, soft_shadow(tmask, "#5a4a30", blur=12, strength=0.3, dx=16, dy=8) * np.concatenate([np.ones((H, W, 3)), (yy > BASE - 240)[..., None]], -1))
cover = over(cover, towers)
cover = over(cover, gouache_paint(steps, "#a99c86", "#93876f", seed=nx(), rough=1.0, streak=0.5))
stepline = np.clip(steps - np.roll(steps, -2, 0), 0, 1)
cover = glaze(cover, pigment(stepline, "#6d624f", seed=nx(), density=0.5, edge=0, bloom=0, rough=1, feather=0.6))


# -- tedung (ceremonial umbrellas) flanking the gate, yellow with a fringe
def tedung(cx, top, pole_bottom, r=50):
    lay = blank(W, H)
    pole = stroke_mask(W, H, [(cx + 0.02 * t * 50, top + 4 + (pole_bottom - top - 4) * t) for t in np.linspace(0, 1, 12)], 6, taper=(0.01, 0.01))
    lay = over(lay, gouache_paint(pole, "#7a4a2a", "#5f3a22", seed=nx(), rough=0.6))
    can = [(cx - r, top + 28)] + [(cx + math.cos(math.pi + t * math.pi) * r, top + 28 - math.sin(t * math.pi) ** 0.8 * 40) for t in np.linspace(0.05, 0.95, 12)] + [(cx + r, top + 28)]
    cm = shape_mask(W, H, can)
    lay = over(lay, gouache_paint(cm, "#e9b62c", "#f2c84a", seed=nx(), rough=1.2, streak=0.8))
    lay = glaze(lay, pigment(cm * np.clip((xx - cx) / r, 0, 1), "#c48a18", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=2))
    ribs = np.zeros((H, W), np.float32)
    for t in np.linspace(-0.8, 0.8, 5):
        ribs = np.maximum(ribs, stroke_mask(W, H, [(cx + t * r * u, top - 10 + 38 * u) for u in np.linspace(0, 1, 8)], 1.8, taper=(0.1, 0.1)))
    lay = glaze(lay, pigment(ribs * cm, "#b07a14", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.4))
    fringe = np.zeros((H, W), np.float32)
    for k in range(13):
        fx = cx - r + 2 + k * (2 * r - 4) / 12
        fringe = np.maximum(fringe, stroke_mask(W, H, [(fx, top + 29 + 20 * u) for u in np.linspace(0, 1, 6)], 4.6, taper=(0.05, 0.4)))
    band = poly_mask(W, H, [(cx - r - 1, top + 25), (cx + r + 1, top + 25), (cx + r + 1, top + 31), (cx - r - 1, top + 31)])
    lay = over(lay, gouache_paint(fringe, "#d99a22", "#e8b440", seed=nx(), rough=0.6))
    lay = over(lay, foil(band, GOLD, seed=nx(), emboss=0.5, sparkle=0.15))
    lay = over(lay, foil(circle_mask(W, H, cx, top - 12, 5.5), GOLD, seed=nx()))
    return lay


cover = over(cover, tedung(W / 2 - GAP - 200, 400, BASE + 30))
cover = over(cover, tedung(W / 2 + GAP + 200, 396, BASE + 32))

# -- kamboja sprays in the upper corners, drooping over the gate
left_leaves = [(40, 60, 190, 60, 0.35), (10, 150, 170, 52, 0.9), (120, 20, 150, 46, -0.2), (70, 220, 140, 44, 1.3), (190, 90, 130, 40, 0.3), (30, 290, 110, 36, 1.5)]
left_flowers = [(90, 120, 48, 0.3, 0.95), (170, 60, 40, 1.2, 0.85), (40, 210, 44, 2.2, 1.0), (140, 190, 36, 0.8, 0.8), (210, 150, 30, 2.6, 0.9)]
cover = over(cover, spray(W, H, (-10, -10), 1, left_flowers, 1.0, left_leaves))
right_leaves = [(-40, 60, 190, 60, math.pi - 0.35), (-10, 150, 170, 52, math.pi - 0.9), (-120, 20, 150, 46, math.pi + 0.2), (-70, 220, 140, 44, math.pi - 1.3), (-190, 90, 130, 40, math.pi - 0.3), (-30, 290, 110, 36, math.pi - 1.5)]
right_flowers = [(-90, 120, 48, 1.1, 0.95), (-170, 60, 40, 2.0, 0.85), (-40, 210, 44, 0.4, 1.0), (-140, 190, 36, 1.7, 0.8), (-210, 150, 30, 0.9, 0.9)]
cover = over(cover, spray(W, H, (W + 10, -10), -1, right_flowers, 1.0, right_leaves))
# fade the foot of the scene into the paper so the text below sits on calm ground
cover[..., 3] *= np.clip((H - 90 - yy) / 120, 0, 1)
cover_size = save(cover, f"{OUT}/cover.webp", max_w=680, quality=72)
print("COVER_SIZE", cover_size)
preview(cover, "bk-cover", tone=CREAM)
if os.environ.get("ONLY") == "cover":
    raise SystemExit
# ---------------- corner spray (reusable) ----------------
SW = SH = 340
sp_leaves = [(30, 40, 150, 48, 0.4), (10, 120, 130, 42, 0.95), (100, 10, 120, 38, -0.15), (60, 180, 110, 36, 1.3), (150, 70, 100, 32, 0.35)]
sp_flowers = [(70, 90, 40, 0.3, 0.95), (140, 45, 34, 1.3, 0.85), (40, 170, 36, 2.2, 1.0), (120, 150, 28, 0.8, 0.8)]
sp = spray(SW, SH, (-6, -6), 1, sp_flowers, 1.0, sp_leaves)
save(sp, f"{OUT}/spray.webp", max_w=340)
preview(sp, "bk-spray", tone=CREAM)

# ---------------- single flower ----------------
FW = FH = 120
fl, _ = bloom(FW, FH, 60, 60, 44, 0.4, 0.95)
save(fl, f"{OUT}/flower.webp", max_w=120)
preview(fl, "bk-flower", tone=CREAM)

# ---------------- divider ----------------
DW, DH = 340, 60
dv = blank(DW, DH)
line = np.zeros((DH, DW), np.float32)
for side in (-1, 1):
    pts = curve([(DW / 2 + side * 34, 32), (DW / 2 + side * 90, 31), (DW / 2 + side * 140, 33), (DW / 2 + side * 166, 32)], 40)
    line = np.maximum(line, stroke_mask(DW, DH, pts, 2.4, taper=(0.02, 0.6)))
    line = np.maximum(line, circle_mask(DW, DH, DW / 2 + side * 166, 32, 2.6))
dv = over(dv, foil(line, GOLD, seed=nx(), emboss=0.7, sparkle=0.1))
for (x, y, L, Wd, a) in [(DW / 2 - 20, 36, 28, 9, 2.6), (DW / 2 + 20, 36, 28, 9, 0.5)]:
    dv, _ = leaf(DW, DH, x, y, L, Wd, a, dv, GREENS[0])
dv, _ = bloom(DW, DH, DW / 2, 30, 21, 0.6, 0.9, dv)
save_full(dv, f"{OUT}/divider.webp", quality=84)
preview(dv, "bk-divider", tone=CREAM)

# ---------------- poleng tile (woven black/white check) ----------------
T = 48
pol = np.zeros((T, T), np.float32)
pol[:24, :24] = 1; pol[24:, 24:] = 1
yy, xx = np.mgrid[0:T, 0:T].astype(np.float32)
weave = 0.9 + 0.1 * np.sin(xx * math.pi / 2) * np.sin(yy * math.pi / 2)
dark = gouache_paint(np.clip(pol + (wrap_noise(T, T, nx(), 1.0) - 0.5) * 0.3, 0, 1), "#2b2724", "#3a3430", seed=nx(), rough=0.8, streak=0.4)
light = solid(T, T, "#f3ecda")
light[..., :3] *= weave[..., None]
tile = over(light, dark)
tile[..., :3] *= weave[..., None]
# grey (true tridatu-less poleng is just black/white; a soft grey thread at the seam adds the woven look)
seam = np.clip(1 - np.abs(np.roll(pol, 1, 1) - pol) - np.abs(np.roll(pol, 1, 0) - pol), 0, 1)
tile[..., :3] *= (0.92 + 0.08 * seam)[..., None]
save_rgb(tile, f"{OUT}/poleng.webp", quality=82)
Image.fromarray((np.clip(tile[..., :3], 0, 1) * 255).astype(np.uint8)).resize((192, 192), Image.NEAREST).save(f"{PREV}/bk-poleng.png")

# ---------------- paper ----------------
P = 360
pap = np.asarray(paper(P, P, CREAM, seed=5, fiber=0.7, mottle=0.9), np.float32) / 255
pa = np.concatenate([pap, np.ones((P, P, 1), np.float32)], -1)
for ch in range(3):
    pa[..., ch] = tile_wrap(pa[..., ch])
save_rgb(pa, f"{OUT}/paper.webp", quality=74)
print("total KB:", sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT)) // 1024)
