"""Editorial Monokrom — sparing relief-print (linocut) accents + newsprint paper tile. Keeps the crisp magazine look.
Run: python3 -I /tmp/pen/art/themes/editorial-monokrom.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _agentc import *  # noqa

OUT = "/root/w/frontend/public/themes/art/editorial-monokrom"
PRE = "/tmp/pen/nt2-C/em"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(7)
INK = "#121211"
PAPER = "#f5f5f2"

# ---------- newsprint paper tile (seamless) ----------
T, OV = 512, 64
pp = np.asarray(paper(T + OV, T + OV, PAPER, seed=11, fiber=1.0, mottle=.15), np.float32) / 255
flat = np.array(hex_rgb(PAPER), np.float32)
pp = flat + (pp - flat) * .55  # keep it crisp: barely-there tooth
# sparse dark fibres / flecks like recycled stock
fl = np.zeros((T + OV, T + OV), np.float32)
def fib(cv):
    for _ in range(26):
        x, y = rng.uniform(0, T + OV), rng.uniform(0, T + OV)
        a = rng.uniform(0, math.tau); L = rng.uniform(3, 11)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=rng.uniform(.5, .9), Style=skia.Paint.kStroke_Style)
        cv.c.drawLine(x, y, x + math.cos(a) * L, y + math.sin(a) * L, p)
fl = mask_from(T + OV, T + OV, fib)
pp = pp * (1 - fl[..., None] * .10)
rgba = np.concatenate([pp, np.ones((T + OV, T + OV, 1), np.float32)], -1)
tile = tileable_xy(rgba, OV)
save_opaque(tile, f"{OUT}/paper.webp", quality=72)
print("paper", round(kb(f"{OUT}/paper.webp")))


def gouges(w, h, lines, width):
    return lines_mask(w, h, lines, width)


# ---------- linocut: lily of the valley sprig (closing page) ----------
W, H = 340, 500
shapes = []
# two broad leaves sweeping up from the base
leafL = deform(curve([(150, 492), (96, 400), (78, 280), (100, 150), (128, 92), (138, 160), (150, 300), (166, 420), (168, 492)], 40), rng, 1, .006)
leafR = deform(curve([(176, 492), (204, 410), (248, 300), (296, 200), (318, 168), (300, 250), (262, 360), (214, 450), (192, 492)], 40), rng, 1, .006)
leaves = np.maximum(shape_mask(W, H, leafL), shape_mask(W, H, leafR))
# arching flower stem
stem_pts = curve([(170, 492), (178, 380), (196, 250), (226, 150), (262, 92), (292, 70)], 60)
stem = stroke_mask(W, H, stem_pts, 7, taper=(.02, .35))
# bells hanging off the stem
bells = np.zeros((H, W), np.float32)
pedicels = []
for i, t in enumerate([.42, .52, .61, .69, .77, .84, .9]):
    k = int(t * (len(stem_pts) - 1))
    sx, sy = stem_pts[k]
    side = -1 if i % 2 == 0 else 1
    drop = 34 - i * 2.0
    bx, by = sx + side * (22 - i * 1.5), sy + drop
    pedicels.append(([(sx, sy), (sx + side * 8, sy + 6), (bx, by - 8)], 2.6))
    r = 21 - i * 1.6
    pts = []
    for j in range(16):
        a = math.pi + j / 15 * math.pi  # dome top
        pts.append((bx + math.cos(a) * r, by - 4 + math.sin(a) * r * .95))
    # scalloped lip
    for j in range(5):
        x = bx + r - (j + .5) * (2 * r / 5)
        pts.append((x + r / 5, by + 3)); pts.append((x, by + 7 + (1 if j % 2 else 0)))
    bells = np.maximum(bells, shape_mask(W, H, pts, smooth=False))
ped = strokes_mask(W, H, pedicels)
ink = np.clip(leaves + stem + bells + ped, 0, 1)
# carved gouges: white cut lines inside the leaves (follow the leaf direction) and on the bells
cuts = []
for k in range(5):
    o = k * 9 - 18
    cuts.append(curve([(150 + o * .3, 470), (124 + o, 360), (114 + o * .8, 250), (124 + o * .5, 160)], 30))
for k in range(4):
    o = k * 9 - 13
    cuts.append(curve([(190 + o * .3, 470), (224 + o, 380), (262 + o * .8, 290), (296 + o * .4, 210)], 30))
cutm = gouges(W, H, cuts, 2.1)
cutm = cutm * leaves  # gouges only inside leaves
hl = []
for i, t in enumerate([.42, .52, .61, .69, .77, .84, .9]):
    k = int(t * (len(stem_pts) - 1)); sx, sy = stem_pts[k]
    side = -1 if i % 2 == 0 else 1
    bx, by = sx + side * (22 - i * 1.5), sy + 34 - i * 2.0
    r = 21 - i * 1.6
    hl.append(arc_pts(bx - side * 1, by - 4, r * .55, math.pi * 1.15, math.pi * 1.55, 8))
cutm = np.maximum(cutm, gouges(W, H, hl, 1.8) * bells)
# break the cuts a little (hand-carved, not machine)
br = fbm(W, H, 77, 14, 2)
cutm *= (br > .32).astype(np.float32)
ink = np.clip(ink - cutm, 0, 1)
# ground line: short carved strip
ground = shape_mask(W, H, deform([(40, 488), (310, 486), (316, 498), (36, 499)], rng, 2, .01), smooth=False)
ink = np.maximum(ink, ground)
lily = linocut(ink, INK, seed=41, wear=.45, rough=1.6)
print("lily", save_asset(lily, f"{OUT}/linocut-lily.webp", quality=84), round(kb(f"{OUT}/linocut-lily.webp")))
on_paper(lily, PAPER).save(f"{PRE}/lily.png")

# ---------- linocut: small olive twig divider (letter sign-off) ----------
W, H = 300, 70
twig = curve([(10, 42), (90, 36), (170, 34), (250, 30), (292, 22)], 40)
m = stroke_mask(W, H, twig, 3.4, taper=(.05, .3))
cuts = []
for i, t in enumerate([.12, .22, .32, .42, .52, .62, .72, .82, .9]):
    k = int(t * (len(twig) - 1)); x, y = twig[k]
    side = -1 if i % 2 == 0 else 1
    ang = (-0.55 if side < 0 else 0.55) + rng.uniform(-.12, .12)
    L = 40 - i * 1.8
    lp = petal_pts(x, y, L, L * .3, ang - (0.0 if side > 0 else 0.0) + (0 if side > 0 else 0), n=12)
    if side < 0:
        lp = petal_pts(x, y, L, L * .3, -0.6 + rng.uniform(-.1, .1), n=12)
    else:
        lp = petal_pts(x, y, L, L * .3, 0.55 + rng.uniform(-.1, .1), n=12)
    m = np.maximum(m, shape_mask(W, H, lp))
    a = -0.6 if side < 0 else 0.55
    cuts.append([(x + math.cos(a) * L * .2, y + math.sin(a) * L * .2), (x + math.cos(a) * L * .78, y + math.sin(a) * L * .78)])
for (bx, by) in [(120, 48), (214, 44)]:
    m = np.maximum(m, circle_mask(W, H, bx, by, 6))
m = np.clip(m - lines_mask(W, H, cuts, 1.4), 0, 1)
twig_a = linocut(m, INK, seed=43, wear=.4, rough=1.2)
print("twig", save_asset(twig_a, f"{OUT}/linocut-twig.webp", quality=84), round(kb(f"{OUT}/linocut-twig.webp")))
on_paper(twig_a, PAPER).save(f"{PRE}/twig.png")
