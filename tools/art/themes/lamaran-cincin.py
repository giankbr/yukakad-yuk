"""Lamaran Cincin — watercolour blush roses, eucalyptus & baby's breath; gold-foil interlocking rings.
Run: python3 -I /tmp/pen/art/themes/lamaran-cincin.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentc import *  # noqa

OUT = "/root/w/frontend/public/themes/art/lamaran-cincin"
PRE = "/tmp/pen/nt2-C/lc"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(33)
seed = [900]
def nxt():
    seed[0] += 19
    return seed[0]

BLUSH = ("#f3d3cc", "#e6b0a8", "#b9746f")
PEACH = ("#f6e0cf", "#eac2a6", "#c08a66")
SAGE = [("#b3bfa9", "#8e9d86"), ("#a8b8ad", "#7f9488"), ("#bcc4a8", "#94a083")]
GOLD = "#c9a46a"


def rose(W, H, cx, cy, r, cols, petals=9):
    light, mid, deep = cols
    lay = blank(W, H)
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * .88, 10), rng, 2, .12))
    lay = glaze(lay, pigment(base, light, mid, seed=nxt(), density=.42, edge=.4, bloom=.5, rough=8, holes=.1))
    for k in range(petals):
        rr = r * (.95 - k * (0.85 / petals))
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .04), cy + rng.gauss(0, r * .04), rr, a0, a0 + rng.uniform(1.4, 2.6), 22, .86)
        col = mix(mid, deep, k / petals)
        lay = glaze(lay, pigment(stroke_mask(W, H, pts, r * rng.uniform(.1, .17)), col, mix(col, light, .3), seed=nxt(), density=.38 + k * .035, edge=.6, bloom=.2, rough=3.5, feather=1.0))
    heart = shape_mask(W, H, ellipse_pts(cx, cy, r * .15, r * .12, 8))
    lay = glaze(lay, pigment(heart, deep, seed=nxt(), density=.65, edge=.7, bloom=0, rough=2.5))
    return lay, base


def eucalyptus(W, H, pts, size, cols, every=3, skip_end=1):
    lay = blank(W, H)
    stem = stroke_mask(W, H, pts, 2.6, taper=(.05, .4))
    lay = glaze(lay, pigment(stem, "#8b8a6a", "#6f7a5c", seed=nxt(), density=.6, edge=.2, bloom=0, rough=1.2, feather=.6))
    n = len(pts)
    for i, k in enumerate(range(3, n - skip_end, every)):
        (x0, y0), (x1, y1) = pts[k - 1], pts[min(n - 1, k + 1)]
        d = math.atan2(y1 - y0, x1 - x0)
        side = 1 if i % 2 else -1
        a = d + side * rng.uniform(.6, 1.0)
        s_ = size * (1 - .45 * k / n) * rng.uniform(.85, 1.15)
        lx, ly = pts[k][0] + math.cos(a) * s_ * .8, pts[k][1] + math.sin(a) * s_ * .8
        m = shape_mask(W, H, deform(ellipse_pts(lx, ly, s_, s_ * .82, 10, a), rng, 1, .05))
        ca, cb = cols[i % len(cols)]
        lay = glaze(lay, pigment(m, ca, cb, seed=nxt(), density=.55, edge=.55, bloom=.45, rough=3.5, gran=.25, feather=1.0))
    return lay


def babys_breath(W, H, origin, tips, bloom_r=4.5):
    lay = blank(W, H)
    st = []
    flowers = []
    for (tx, ty) in tips:
        mx, my = (origin[0] + tx) / 2 + rng.uniform(-14, 14), (origin[1] + ty) / 2 + rng.uniform(-14, 14)
        p = curve([origin, (mx, my), (tx, ty)], 24)
        st.append((p, 1.5))
        for j in range(rng.randint(5, 9)):
            flowers.append((tx + rng.gauss(0, 9), ty + rng.gauss(0, 9), bloom_r * rng.uniform(.6, 1.15)))
            if rng.random() < .4:
                k = rng.randint(8, 20)
                flowers.append((p[k][0] + rng.gauss(0, 6), p[k][1] + rng.gauss(0, 6), bloom_r * rng.uniform(.5, .8)))
    lay = glaze(lay, pigment(strokes_mask(W, H, st), "#9c9a7a", "#7f8a68", seed=nxt(), density=.5, edge=.2, bloom=0, rough=1, feather=.5))
    fm = dots_mask(W, H, flowers)
    # white blossoms: pale warm shadow wash with a lighter centre (paper white) + tiny gold eye
    shade = pigment(fm, "#efe3d2", "#e3d2bb", seed=nxt(), density=.85, edge=.8, bloom=.2, rough=1.4, feather=.6)
    inner = dots_mask(W, H, [(x - r * .15, y - r * .15, r * .55) for x, y, r in flowers])
    shade = over(shade, pigment(inner, "#fffdf8", seed=nxt(), density=.95, edge=0, bloom=0, rough=.8, feather=.6))
    eyes = dots_mask(W, H, [(x, y, max(.8, r * .22)) for x, y, r in flowers])
    shade = glaze(shade, pigment(eyes, "#d6b27a", seed=nxt(), density=.7, edge=0, bloom=0, rough=.4, feather=.4))
    return over(lay, shade)


def spatter(W, H, cx, cy, sx, sy, n, col):
    pts = [(cx + rng.gauss(0, sx), cy + rng.gauss(0, sy), rng.uniform(1.2, 4)) for _ in range(n)]
    return pigment(dots_mask(W, H, pts), col, seed=nxt(), density=.45, edge=.3, bloom=0, rough=1, feather=.5)


def bouquet(W, H, roses, euc, breath, buds, sp):
    flowers = blank(W, H); area = np.zeros((H, W), np.float32)
    for (cx, cy, r, cols) in roses:
        lay, base = rose(W, H, cx, cy, r, cols)
        flowers = glaze(flowers, lay); area = np.maximum(area, base)
    greens = blank(W, H)
    for pts, size in euc:
        greens = glaze(greens, eucalyptus(W, H, pts, size, SAGE))
    for (x, y, L, a) in buds.get("leaves", []):
        ca, cb = SAGE[rng.randint(0, 2)]
        m = shape_mask(W, H, petal_pts(x, y, L, L * .3, a, n=10))
        greens = glaze(greens, pigment(m, ca, cb, seed=nxt(), density=.62, edge=.5, bloom=.4, rough=4, holes=.05))
        half = shape_mask(W, H, petal_pts(x, y, L * .95, L * .14, a + .06, n=10))
        greens = glaze(greens, pigment(half, cb, seed=nxt(), density=.3, edge=.3, bloom=.2, rough=2.5))
    greens = knockout(greens, area, amount=.92, grow=4)
    bb = blank(W, H)
    for origin, tips in breath:
        bb = over(bb, babys_breath(W, H, origin, tips))
    bb = knockout(bb, area, amount=.95, grow=3)
    art = glaze(greens, flowers)
    art = over(art, bb)
    for (x, y, s_) in buds.get("buds", []):
        m = shape_mask(W, H, deform(ellipse_pts(x, y, s_ * .72, s_, 8, .5), rng, 2, .1))
        art = glaze(art, pigment(m, "#efc0b8", "#d9948e", seed=nxt(), density=.62, edge=.6, rough=3.5))
    for args in sp:
        art = glaze(art, spatter(W, H, *args))
    return art


# ---------- cover corner, hanging from top-left ----------
W, H = 520, 500
art = bouquet(W, H,
    roses=[(150, 140, 86, BLUSH), (272, 92, 56, PEACH), (92, 262, 50, BLUSH)],
    euc=[(curve([(170, 150), (260, 190), (350, 250), (430, 330), (470, 400)], 50), 18),
         (curve([(140, 160), (130, 260), (150, 360), (190, 450)], 44), 16),
         (curve([(250, 90), (330, 70), (410, 80), (480, 60)], 36), 14)],
    breath=[((200, 160), [(320, 170), (360, 140), (300, 220), (380, 210)]), ((120, 200), [(60, 330), (110, 360), (40, 280)])],
    buds={"buds": [(355, 120, 22), (210, 300, 18)], "leaves": [(60, 140, 120, 2.6), (230, 210, 130, 1.0)]},
    sp=[(260, 200, 120, 90, 26, "#e6b0a8")])
print("corner-top", save_asset(art, f"{OUT}/corner-top.webp", max_w=440, quality=82), round(kb(f"{OUT}/corner-top.webp")))
on_paper(art, "#f8efe4").save(f"{PRE}/corner-top.png")

# ---------- cover corner, rising from bottom-right ----------
W, H = 500, 480
art = bouquet(W, H,
    roses=[(360, 340, 80, PEACH), (250, 392, 50, BLUSH), (420, 220, 44, BLUSH)],
    euc=[(curve([(350, 330), (270, 290), (190, 230), (110, 170), (60, 100)], 50), 17),
         (curve([(380, 320), (400, 230), (390, 140), (360, 50)], 40), 14)],
    breath=[((300, 330), [(180, 300), (150, 260), (220, 250), (130, 330)]), ((400, 260), [(460, 140), (430, 120), (470, 190)])],
    buds={"buds": [(150, 380, 20), (300, 210, 17)], "leaves": [(420, 420, 110, -2.2), (240, 340, 120, -2.7)]},
    sp=[(260, 300, 120, 90, 24, "#eac2a6")])
print("corner-bottom", save_asset(art, f"{OUT}/corner-bottom.webp", max_w=420, quality=82), round(kb(f"{OUT}/corner-bottom.webp")))
on_paper(art, "#f8efe4").save(f"{PRE}/corner-bottom.png")

# ---------- small stem (hero / closing) ----------
W, H = 300, 360
art = blank(W, H)
art = glaze(art, eucalyptus(W, H, curve([(40, 350), (80, 260), (140, 160), (200, 80), (250, 20)], 50), 14, SAGE))
art = over(art, babys_breath(W, H, (90, 250), [(30, 150), (60, 110), (150, 210), (190, 170)], 4))
lay, base = rose(W, H, 196, 96, 34, BLUSH, petals=7)
art = glaze(knockout(art, base, .9, 3), lay)
art = glaze(art, spatter(W, H, 150, 160, 60, 70, 12, "#e6b0a8"))
print("sprig", save_asset(art, f"{OUT}/sprig.webp", max_w=260, quality=82), round(kb(f"{OUT}/sprig.webp")))
on_paper(art, "#f8efe4").save(f"{PRE}/sprig.png")

# ---------- interlocking gold-foil rings + painted solitaire ----------
W, H = 300, 230
def ring_mask(cx, cy, rx, ry, t, tilt):
    def draw(cv):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=t)
        cv.c.save(); cv.c.rotate(math.degrees(tilt), cx, cy)
        cv.c.drawOval(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry), p)
        cv.c.restore()
    return mask_from(W, H, draw)
rA = ring_mask(116, 140, 66, 60, 11, -.18)
rB = ring_mask(186, 140, 66, 60, 9, .16)
# interlock: ring B passes in front of A at the lower crossing, behind at the upper one
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
front_zone = (yy > 140).astype(np.float32)
fa = foil(rA, "#bf9c5e", seed=nxt(), emboss=.8, sparkle=.12)
fb = foil(rB, "#cdb07c", seed=nxt(), emboss=.8, sparkle=.12)
# soft contact shadow under each ring band
shadow = pigment(np.clip(gaussian_filter(np.maximum(rA, rB), 3) * 1.4, 0, 1), "#8e6d3a", seed=nxt(), density=.18, edge=0, bloom=0, rough=1, feather=3)
rings = shadow
behind_b = fb.copy(); behind_b[..., 3] *= (1 - front_zone)
front_b = fb.copy(); front_b[..., 3] *= front_zone
rings = over(rings, behind_b)
rings = over(rings, fa)
gap = np.clip(gaussian_filter(rB * front_zone, 1.2) * 2, 0, 1)
rings[..., 3] *= 1 - gap * .0
rings = over(rings, front_b)
# solitaire on ring A: prongs + facetted stone in pale watercolour
gx, gy = 108, 72
prong = ring_mask(gx, gy + 12, 13, 5, 4, -.18)
rings = over(rings, foil(prong, "#c9a04b", seed=nxt(), emboss=.6, sparkle=0))
stone = shape_mask(W, H, [(gx - 20, gy - 2), (gx - 10, gy - 16), (gx + 10, gy - 16), (gx + 20, gy - 2), (gx, gy + 18)], smooth=False)
st = pigment(stone, "#eef3f6", "#cfdde6", seed=nxt(), density=.8, edge=.8, bloom=.2, rough=.8, feather=.5, gran=.1)
facets = lines_mask(W, H, [[(gx - 20, gy - 2), (gx + 20, gy - 2)], [(gx - 10, gy - 16), (gx - 6, gy - 2), (gx, gy + 18)], [(gx + 10, gy - 16), (gx + 6, gy - 2), (gx, gy + 18)], [(gx - 6, gy - 2), (gx, gy - 16), (gx + 6, gy - 2)]], 1.1)
st = glaze(st, pigment(facets * stone, "#93a9b8", seed=nxt(), density=.6, edge=0, bloom=0, rough=.3, feather=.4))
hl = shape_mask(W, H, [(gx - 12, gy - 6), (gx - 7, gy - 13), (gx - 3, gy - 6)], smooth=False)
st = over(st, pigment(hl, "#ffffff", seed=nxt(), density=.9, edge=0, bloom=0, rough=.3, feather=.5))
rings = over(rings, st)
rings = over(rings, pigment(lines_mask(W, H, [[(gx - 20, gy - 2), (gx - 10, gy - 16), (gx + 10, gy - 16), (gx + 20, gy - 2), (gx, gy + 18), (gx - 20, gy - 2)]], 1.6), "#a8874f", seed=nxt(), density=.75, edge=0, bloom=0, rough=.4, feather=.4))
print("rings", save_asset(rings, f"{OUT}/rings.webp", quality=86), round(kb(f"{OUT}/rings.webp")))
on_paper(rings, "#f8efe4").save(f"{PRE}/rings.png")
on_color(rings, "#3d2f29").save(f"{PRE}/rings-dark.png")

# ---------- soft blush wash (cover/hero background bloom) ----------
W, H = 600, 600
m = shape_mask(W, H, deform(ellipse_pts(300, 300, 230, 200, 12), rng, 3, .12))
wash = pigment(m, "#f1d2c7", "#ecd9c0", seed=nxt(), density=.38, edge=.35, bloom=.6, rough=24, gran=.2, feather=6, mottle=.8)
print("wash", save_asset(wash, f"{OUT}/wash.webp", max_w=480, quality=74), round(kb(f"{OUT}/wash.webp")))
