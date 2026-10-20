"""Mihrab Pastel — watercolour nested mihrab arches (sage / blush / cream), painted 8-point rosettes,
seamless watercolour wash tile for the niche cards and a soft painted star lattice tile.
Run: python3 -I /tmp/pen/art/themes/mihrab-pastel.py
Pigments: sage green (#a9c4b2/#7fa18c), blush (#efc4b8/#d99a8a), lilac (#c9bfe0), raw sienna line (#c3a477).
"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *

OUT = "/root/w/frontend/public/themes/art/mihrab-pastel"
PREV = "/tmp/pen/nt2-E"
os.makedirs(OUT, exist_ok=True)
seed = [300]
def nxt():
    seed[0] += 13
    return seed[0]


def path_mask(w, h, build, stroke=0.0):
    def draw(cv):
        p = skia.Path(); build(p)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style); paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap); paint.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(p, paint)
    return mask_from(w, h, draw)


def star8_lines(cx, cy, r, rng, wob=0.6):
    """Two overlapping squares, each corner nudged by hand."""
    out = []
    for rot in (0, math.pi / 4):
        pts = []
        for k in range(4):
            a = rot + math.pi / 4 + k * math.pi / 2
            pts.append((cx + math.cos(a) * r * 1.414 / 1.414 * 1.0 + rng.gauss(0, wob), cy + math.sin(a) * r + rng.gauss(0, wob)))
        out.append(pts)
    return out


def rosette(W, H, cx, cy, r, col, col2, rng, fill=None):
    art = blank(W, H)
    if fill:
        # soft wash disc behind
        m = shape_mask(W, H, deform(ellipse_pts(cx, cy, r * .78, r * .78, 10), rng, 2, .08))
        art = glaze(art, pigment(m, fill, seed=nxt(), density=0.35, edge=0.5, bloom=0.3, rough=max(1.5, r * .06), feather=1))
    sq = star8_lines(cx, cy, r, rng, wob=r * 0.02)
    for pts in sq:
        def build(p, pts=pts):
            p.moveTo(*pts[0])
            for q in pts[1:]: p.lineTo(*q)
            p.close()
        m = path_mask(W, H, build, stroke=max(2.0, r * 0.11))
        art = glaze(art, pigment(m, col, col2, seed=nxt(), density=0.75, edge=0.6, bloom=0.1, rough=max(1.0, r * .03), feather=0.7))
    ring = mask_from(W, H, lambda cv: cv.c.drawCircle(cx, cy, r * .3, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.0, r * .1))))
    art = glaze(art, pigment(ring, col2, seed=nxt(), density=0.7, edge=0.5, bloom=0, rough=max(.8, r * .02), feather=0.6))
    return art


# ---------------------------------------------------------------- cover arches (hero illustration)
S = 2.2
W, H = int(300 * S), int(420 * S) + 40
OY = 30
rng = random.Random(8)

def arch_path(x0, top, shoulder, bulge):
    """Pointed (ogee-ish) arch from x0..300-x0, apex at top (viewBox units)."""
    def build(p):
        x1 = 300 - x0
        p.moveTo(x0 * S, (420) * S + OY)
        p.lineTo(x0 * S, shoulder * S + OY)
        p.cubicTo(x0 * S, (shoulder - bulge) * S + OY, (150 - (150 - x0) * .3) * S, (top + (shoulder - top) * .35) * S + OY, 150 * S, top * S + OY)
        p.cubicTo((150 + (150 - x0) * .3) * S, (top + (shoulder - top) * .35) * S + OY, x1 * S, (shoulder - bulge) * S + OY, x1 * S, shoulder * S + OY)
        p.lineTo(x1 * S, 420 * S + OY)
        p.close()
    return build

A = path_mask(W, H, arch_path(10, 12, 160, 68))
B = path_mask(W, H, arch_path(34, 46, 170, 58))
C = path_mask(W, H, arch_path(58, 80, 180, 50))
yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
fade = np.clip((H - 40 - yy) / (H * 0.2), 0, 1) ** 1.3        # washes fade into the paper at the bottom
fade = fade * (0.75 + 0.25 * fbm(W, H, 77, 30, 3))

art = blank(W, H)
art = glaze(art, pigment(np.clip(A - B, 0, 1) * fade, "#b9cfbf", "#94b4a0", seed=nxt(), density=0.62, edge=0.55, bloom=0.45, gran=0.18, rough=6, holes=0.04))
art = glaze(art, pigment(np.clip(B - C, 0, 1) * fade, "#f2cfc4", "#e3a999", seed=nxt(), density=0.58, edge=0.55, bloom=0.45, gran=0.16, rough=6))
art = glaze(art, pigment(C * fade, "#f6ead6", "#f1dcc2", seed=nxt(), density=0.22, edge=0.35, bloom=0.5, gran=0.15, rough=6, mottle=0.8))
# wet-in-wet variation: irregular blots dropped into each band while wet
for band, cols in ((np.clip(A - B, 0, 1), ("#9fbea9", "#c3d6c6")), (np.clip(B - C, 0, 1), ("#e9b6a8", "#f4d6cb"))):
    for k in range(7):
        bx, by = rng.uniform(0, W), rng.uniform(OY, H * .8)
        m = shape_mask(W, H, deform(ellipse_pts(bx, by, rng.uniform(40, 90), rng.uniform(60, 140), 10, rng.uniform(0, 3)), rng, 3, .18))
        art = glaze(art, pigment(m * band * fade, cols[k % 2], seed=nxt(), density=rng.uniform(0.18, 0.32), edge=0.45, bloom=0.5, rough=8, feather=3))
# second glaze on the shoulders for depth (light from top-left: shade the right)
sh = shape_mask(W, H, deform(ellipse_pts(W * .8, H * .42, W * .22, H * .3, 10), rng, 2, .1))
art = glaze(art, pigment(np.clip(A - B, 0, 1) * sh * fade, "#8fae9b", seed=nxt(), density=0.3, edge=0.25, bloom=0.3, rough=4, feather=6))
sh2 = shape_mask(W, H, deform(ellipse_pts(W * .74, H * .4, W * .2, H * .28, 10), rng, 2, .1))
art = glaze(art, pigment(np.clip(B - C, 0, 1) * sh2 * fade, "#dc9d8d", seed=nxt(), density=0.22, edge=0.2, bloom=0.3, rough=4, feather=6))
# fine sienna lines tracing each arch (drawn with a rigger, broken here and there)
for x0, top, shoulder, bulge in ((10, 12, 160, 68), (34, 46, 170, 58), (58, 80, 180, 50)):
    m = path_mask(W, H, arch_path(x0, top, shoulder, bulge), stroke=2.6)
    m *= fade * np.clip((fbm(W, H, nxt(), 60, 2) - 0.18) * 3, 0, 1)
    art = glaze(art, pigment(m, "#c3a477", "#b38f63", seed=nxt(), density=0.85, edge=0.2, bloom=0, rough=1.2, feather=0.5))
# apex rosette
art = glaze(art, rosette(W, H, 150 * S, 12 * S + OY - 4, 26, "#d9958a", "#c47e72", rng, fill="#f5d9cf"))
# sprigs at the base of the outer arch (sage leaves + blush buds)
def sprig(bx, by, dirx):
    global art
    stem = curve([(bx, by), (bx + dirx * 24, by - 90), (bx + dirx * 10, by - 190), (bx + dirx * 34, by - 270)], 40)
    art = glaze(art, pigment(stroke_mask(W, H, stem, 3.2), "#7f9f88", seed=nxt(), density=0.6, edge=0.2, bloom=0, rough=1.5, feather=.6))
    for i, t in enumerate([0.2, 0.36, 0.52, 0.68, 0.84]):
        px, py = stem[int(t * (len(stem) - 1))]
        side = 1 if i % 2 else -1
        ang = -math.pi / 2 + side * 0.95 + rng.uniform(-.2, .2)
        L = 62 - i * 6
        m = shape_mask(W, H, petal_pts(px, py, L, L * .34, ang, n=10))
        art = glaze(art, pigment(m, "#a9c4b2", "#7fa18c", seed=nxt(), density=0.62, edge=0.5, bloom=0.35, rough=2.5))
    for j, (t, r) in enumerate([(1.0, 17), (0.6, 12)]):
        px, py = stem[int(t * (len(stem) - 1))]
        m = shape_mask(W, H, deform(ellipse_pts(px + dirx * (6 if j else 0), py - 4, r * .8, r, 8, .3 * dirx), rng, 2, .12))
        art = glaze(art, pigment(m, "#efb9ab", "#d68f80", seed=nxt(), density=0.65, edge=0.6, bloom=0.2, rough=2))
sprig(40, H - 40 - 30, 1)
sprig(W - 40, H - 40 - 30, -1)

print("arches", save_asset(art, f"{OUT}/arches.webp", max_w=640, quality=78), os.path.getsize(f"{OUT}/arches.webp"))
on_paper(art, "#f8f3eb").save(f"{PREV}/mp-arches.png")

# ---------------------------------------------------------------- rosette icon (apex / rule / bullets)
W2 = 120
rng = random.Random(3)
ro = rosette(W2, W2, 60, 60, 40, "#d9958a", "#c47e72", rng, fill="#f6dcd2")
print("star", save_asset(ro, f"{OUT}/star.webp", max_w=96, quality=84), os.path.getsize(f"{OUT}/star.webp"))
on_paper(ro, "#f8f3eb").resize((240, 240)).save(f"{PREV}/mp-star.png")
ro2 = rosette(W2, W2, 60, 60, 40, "#86a893", "#62846f", random.Random(5))
print("star-sage", save_asset(ro2, f"{OUT}/star-sage.webp", max_w=96, quality=84))

# ---------------------------------------------------------------- star lattice tile (transparent, seamless: motifs stay inside)
T = 224
rng = random.Random(21)
lat = blank(T, T)
for (x, y, c) in ((56, 56, "#cdbb9c"), (168, 168, "#b9cdbf")):
    lat = glaze(lat, rosette(T, T, x, y, 21, c, mix(c, "#8f7a5c", .3), rng))
save_texture(lat, f"{OUT}/lattice.webp", quality=80)
print("lattice", os.path.getsize(f"{OUT}/lattice.webp"))

# ---------------------------------------------------------------- seamless watercolour wash tile (multiply over the tone colour)
T = 512
r = np.random.default_rng(9)
def wrapnoise(sig):
    n = gaussian_filter(r.random((T, T)).astype(np.float32), sig, mode="wrap")
    return (n - n.min()) / (n.max() - n.min() + 1e-6)
low = wrapnoise(50); mid = wrapnoise(12); fine = wrapnoise(0.8)
blot = np.clip((mid * 0.55 + low * 0.45 - 0.5) * 5, 0, 1)
blot = gaussian_filter(blot, 1.2, mode="wrap")
rim = np.clip(blot - gaussian_filter(blot, 4, mode="wrap"), 0, 1) * 3.0
dark = 0.018 * low + 0.012 * blot + 0.04 * rim + 0.035 * (fine - 0.5)
v = np.clip(1 - dark, 0, 1)
tex = np.stack([v, v * 0.993, v * 0.982], -1)
Image.fromarray((tex * 255).astype(np.uint8), "RGB").save(f"{OUT}/wash.webp", "WEBP", quality=80, method=6)
print("wash", os.path.getsize(f"{OUT}/wash.webp"))
# preview: wash multiplied on sage tone, tiled 2x2
tone = np.array(hex_rgb("#e4ede6"), np.float32)
big = np.tile(tex, (2, 2, 1)) * tone
Image.fromarray((big * 255).astype(np.uint8)).save(f"{PREV}/mp-wash.png")
