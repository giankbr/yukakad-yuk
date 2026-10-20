"""Reference: watercolor rose corner spray, rendered with the Rawuh art toolkit.
Run: python3 -I /tmp/pen/art/example_floral_corner.py  → /tmp/pen/art/example_floral_corner.webp
Pattern: paint the hero objects first, then paint things that sit BEHIND them with knockout(), glaze() washes,
vary seeds/colours per element, finish with small accents. Work at 2x the CSS display size.
"""
import sys, math, random
sys.path.insert(0, "/tmp/pen/art")
from art import *

W, H = 1100, 1000
rng = random.Random(4)
seed = [100]
def nxt():
    seed[0] += 17
    return seed[0]

flowers = blank(W, H)
rose_area = np.zeros((H, W), np.float32)

def rose(cx, cy, r, light, mid, deep):
    global flowers, rose_area
    base = shape_mask(W, H, deform(ellipse_pts(cx, cy, r, r * 0.9, 10), rng, 2, 0.12))
    rose_area = np.maximum(rose_area, base)
    flowers = glaze(flowers, pigment(base, light, mid, seed=nxt(), density=0.42, edge=0.35, bloom=0.5, rough=10, holes=0.12))
    for k in range(10):                      # loose comma petals spiralling in, darker toward the heart
        rr = r * (0.95 - k * 0.085)
        a0 = rng.uniform(0, math.tau)
        pts = arc_pts(cx + rng.gauss(0, r * .04), cy + rng.gauss(0, r * .04), rr, a0, a0 + rng.uniform(1.4, 2.7), 26, 0.86)
        sm = stroke_mask(W, H, pts, r * rng.uniform(0.09, 0.17))
        col = mix(mid, deep, k / 10)
        flowers = glaze(flowers, pigment(sm, col, mix(col, light, .3), seed=nxt(), density=0.4 + k * 0.035, edge=0.6, bloom=0.2, rough=4, feather=1.1))
    heart = shape_mask(W, H, ellipse_pts(cx, cy, r * .15, r * .12, 8))
    flowers = glaze(flowers, pigment(heart, deep, seed=nxt(), density=0.7, edge=0.7, bloom=0, rough=3))

rose(480, 470, 200, "#f6d3d3", "#e7a2a8", "#b45a68")
rose(735, 345, 135, "#f7dcd6", "#eeb0a7", "#c4706a")
rose(320, 680, 125, "#f9e1dc", "#f0bcb5", "#c9827a")

leaves = blank(W, H)
greens = [("#9db394", "#6e8b68"), ("#a9bc9c", "#7d9874"), ("#8ca486", "#5f7c5a")]
for i, (x, y, L, a) in enumerate([(300, 380, 330, -2.5), (650, 560, 300, 0.4), (640, 260, 270, -1.1), (200, 600, 250, 2.2),
                                  (820, 470, 230, 0.2), (480, 230, 220, -1.7), (420, 760, 240, 1.2), (900, 300, 160, -0.6)]):
    ca, cb = greens[i % 3]
    m = shape_mask(W, H, petal_pts(x, y, L, L * 0.33, a, n=10))
    leaves = glaze(leaves, pigment(m, ca, cb, seed=nxt(), density=0.68, edge=0.5, bloom=0.4, rough=5, holes=0.06))
    half = shape_mask(W, H, petal_pts(x, y, L * 0.95, L * 0.15, a + 0.06, n=10))      # shadow half for form
    leaves = glaze(leaves, pigment(half, cb, seed=nxt(), density=0.32, edge=0.3, bloom=0.2, rough=3))
    vein = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in [j / 10 for j in range(1, 9)]]
    leaves = glaze(leaves, pigment(stroke_mask(W, H, vein, 3), mix(cb, "#1f2b1d", .5), seed=nxt(), density=0.3, edge=0.1, bloom=0, rough=1.5, feather=0.6))
leaves = knockout(leaves, rose_area, amount=0.92, grow=4)   # leaves tuck behind the roses

art = glaze(leaves, flowers)
for (x, y, s) in [(880, 560, 40), (200, 340, 34), (600, 800, 36)]:     # buds
    m = shape_mask(W, H, deform(ellipse_pts(x, y, s * .75, s, 8, .4), rng, 2, .1))
    art = glaze(art, pigment(m, "#efb3b8", "#d98692", seed=nxt(), density=0.6, edge=0.6, rough=4))
def dots(cv):
    for _ in range(50):
        cv.c.drawCircle(480 + rng.gauss(0, 320), 480 + rng.gauss(0, 280), rng.uniform(1.5, 5), skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
art = glaze(art, pigment(mask_from(W, H, dots), "#e9a7a0", seed=nxt(), density=0.5, edge=0.2, bloom=0, rough=1, feather=0.5))

print(save_asset(art, "/tmp/pen/art/example_floral_corner.webp", max_w=900))
on_paper(art, "#fbf4f0").save("/tmp/pen/art/example_floral_corner_preview.png")
