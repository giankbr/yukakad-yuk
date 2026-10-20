"""Peta Rute — hand-painted watercolour city map for the cover (replaces the stock map screenshot).
Run: python3 -I /tmp/pen/art/themes/peta-rute.py
Canvas 780x1690 = 2x of a 390x845 phone; the heart pin sits at css (195, ~240) → (390, 480) here, the route ends there.
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p7 import *  # noqa

OUT = "/root/w/frontend/public/themes/art/peta-rute"
PRE = "/tmp/pen/nt3-P7/pr"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(7)
seed = [900]
def nxt():
    seed[0] += 11
    return seed[0]

W, H = 780, 1690
PAPER = "#f4f0e7"
BLOCK = [("#e6e1d6", "#ddd7ca"), ("#e9e3d8", "#e0dacd"), ("#e2dccf", "#d6cfc0")]
PARK = ("#c2d8aa", "#a7c48e")
PARK_D = "#86a86e"
WATER = ("#b3d0e0", "#8fb6cf")
WATER_D = "#6f9cbb"
INK = "#6b6557"
ROUTE = "#2f6fd6"
ROUTE_D = "#1f54b0"
PIN = (390, 540)

base = paper_rgba(W, H, PAPER, seed=5, fiber=.6, mottle=.7)

# ---- street grid: slightly rotated, jittered rows/cols; blocks are rounded rects between the roads
ROT = math.radians(-5)
cr, sr = math.cos(ROT), math.sin(ROT)
def R(x, y):  # rotate about canvas centre
    x -= W / 2; y -= H / 2
    return (W / 2 + x * cr - y * sr, H / 2 + x * sr + y * cr)

cols = [-220]
while cols[-1] < W + 240:
    cols.append(cols[-1] + rng.choice([120, 140, 150, 170, 190]))
rows = [-200]
while rows[-1] < H + 220:
    rows.append(rows[-1] + rng.choice([100, 115, 130, 150, 170]))
# avenues: a wider road near the pin (vertical through x≈390) and a horizontal one at y≈530 (route runs along it)
AVE_X = min(cols, key=lambda c: abs(c - 392)); AVE_Y = min(rows, key=lambda r: abs(r - 536))
cols = [c + (0 if c in (AVE_X,) else rng.uniform(-6, 6)) for c in cols]
ROAD = 16
def gap(c):
    return 30 if c in (AVE_X, AVE_Y) else ROAD

cells = []
for i in range(len(cols) - 1):
    for j in range(len(rows) - 1):
        x0, x1 = cols[i] + gap(cols[i]) / 2, cols[i + 1] - gap(cols[i + 1]) / 2
        y0, y1 = rows[j] + gap(rows[j]) / 2, rows[j + 1] - gap(rows[j + 1]) / 2
        cells.append([x0, y0, x1, y1])

# river: a wide meander from top-right to lower-left (in unrotated coords, then rotated)
riv_ctrl = [(W + 80, 120), (640, 300), (560, 560), (610, 820), (420, 1060), (170, 1200), (-60, 1330)]
riv = curve(riv_ctrl, 160)
riv_pts = [R(*p) for p in riv]
river_mask = stroke_mask(W, H, riv_pts, 78, taper=(0.001, 0.001))
river_mask = np.clip(displace(river_mask, nxt(), 5, 70), 0, 1)

# parks: cells that are mostly dry and a bit away from the pin
def cell_center(c):
    return ((c[0] + c[2]) / 2, (c[1] + c[3]) / 2)
park_cells = []
cand = [c for c in cells if 40 < c[0] and c[2] < W - 40 and 120 < c[1] and c[3] < 1050]
rng.shuffle(cand)
for c in cand:
    cx, cy = R(*cell_center(c))
    if math.hypot(cx - PIN[0], cy - PIN[1]) < 150:
        continue
    yi, xi = int(min(H - 1, max(0, cy))), int(min(W - 1, max(0, cx)))
    if river_mask[yi, xi] > 0.1:
        continue
    if any(math.hypot(cx - px, cy - py) < 300 for px, py in park_cells):
        continue
    park_cells.append((cx, cy)); c.append("park")
    if len(park_cells) >= 5:
        break

blocks = blank(W, H); parks = blank(W, H); outlines = []
for c in cells:
    x0, y0, x1, y1 = c[:4]
    is_park = len(c) > 4
    pts = [R(*p) for p in rrect_pts(x0, y0, x1 - x0, y1 - y0, 6, 4)]
    pts = deform(pts, rng, 2, 0.015)
    m = shape_mask(W, H, pts)
    # skip blocks drowned by the river
    if (m * river_mask).sum() > m.sum() * 0.35:
        continue
    m = m * (1 - np.clip(gaussian_filter(river_mask, 3) * 1.6, 0, 1))
    if m.sum() < 400:
        continue
    if is_park:
        parks = glaze(parks, pigment(m, *PARK, seed=nxt(), density=.62, edge=.5, bloom=.45, rough=5, gran=.3, feather=1.3, mottle=.6))
        # tree clusters
        cx, cy = R(*cell_center(c)); dots = []
        for _ in range(int(rng.uniform(14, 26))):
            dots.append((cx + rng.gauss(0, (x1 - x0) * .22), cy + rng.gauss(0, (y1 - y0) * .22), rng.uniform(5, 11)))
        parks = glaze(parks, pigment(dots_mask(W, H, dots), PARK_D, "#6f9460", seed=nxt(), density=.55, edge=.5, bloom=.3, rough=3, feather=1))
    else:
        ca, cb = rng.choice(BLOCK)
        blocks = over(blocks, gouache_paint(m, ca, cb, seed=nxt(), rough=2.2, streak=.6, density=rng.uniform(.8, .95)))
        # building footprints: a few darker gouache rectangles inside the block, aligned to the grid
        if rng.random() < 0.55:
            foots = []
            for k in range(int(rng.uniform(2, 5))):
                bw, bh = rng.uniform(14, 34), rng.uniform(12, 30)
                bx = rng.uniform(x0 + 8, x1 - 8 - bw); by = rng.uniform(y0 + 8, y1 - 8 - bh)
                if bx < x0 + 8 or by < y0 + 8:
                    continue
                foots.append([R(*q) for q in [(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh)]])
            if foots:
                fm = poly_mask(W, H, foots) * (1 - np.clip(gaussian_filter(river_mask, 3) * 1.6, 0, 1))
                blocks = over(blocks, scale_alpha(gouache_paint(fm, "#cdc5b3", "#c3bba8", seed=nxt(), rough=1.4, streak=.5), .75))
    outlines.append(pts)

scene = multiply_onto(base, scale_alpha(blocks, .9))
scene = multiply_onto(scene, parks)
# block outlines: faint broken ink
ol = lines_mask(W, H, outlines, 1.4, closed=True)
ol *= (fbm(W, H, nxt(), 9, 2) > 0.36)
scene = over(scene, scale_alpha(ink(ol, INK, seed=nxt(), bleed=.5), .32))

# river: wash + darker pooled edge + a few current strokes
water = pigment(river_mask, *WATER, seed=nxt(), density=.6, edge=.7, bloom=.4, rough=4, gran=.3, feather=1.4, mottle=.5)
scene = multiply_onto(scene, water)
cur = []
for i in range(14):
    t = rng.uniform(.05, .95); k = int(t * (len(riv_pts) - 12))
    seg = riv_pts[k:k + rng.randint(6, 12)]
    off = rng.uniform(-22, 22)
    seg = [(x + off * .2, y + off) for x, y in seg]
    cur.append((seg, rng.uniform(2, 4)))
scene = multiply_onto(scene, scale_alpha(pigment(strokes_mask(W, H, cur), WATER_D, seed=nxt(), density=.5, edge=.2, bloom=0, rough=1.5, feather=.8), .7))

# bridges where the avenue crosses the river: a short pale plank with ink rails
def bridge_at(px, py, ang):
    L, Wd = 110, 30
    c_, s_ = math.cos(ang), math.sin(ang)
    quad = [(px + c_ * L / 2 - s_ * Wd / 2, py + s_ * L / 2 + c_ * Wd / 2), (px + c_ * L / 2 + s_ * Wd / 2, py + s_ * L / 2 - c_ * Wd / 2),
            (px - c_ * L / 2 + s_ * Wd / 2, py - s_ * L / 2 - c_ * Wd / 2), (px - c_ * L / 2 - s_ * Wd / 2, py - s_ * L / 2 + c_ * Wd / 2)]
    return quad
bridges = blank(W, H); rails = []
for (ux, uy, ang) in [(AVE_X, None, ROT + math.pi / 2), (None, AVE_Y, ROT)]:
    # find the river point closest to the avenue line
    best = None
    for (x, y), (ox, oy) in zip(riv_pts, riv):
        d = abs(ox - ux) if ux is not None else abs(oy - uy)
        if best is None or d < best[0]:
            best = (d, x, y)
    _, bx, by = best
    q = bridge_at(bx, by, ang)
    bridges = over(bridges, gouache_paint(poly_mask(W, H, [q]), "#efe9dc", "#e5dfd0", seed=nxt(), rough=1.5, streak=.4))
    rails += [[q[0], q[3]], [q[1], q[2]]]
scene = over(scene, bridges)
scene = over(scene, scale_alpha(ink(lines_mask(W, H, rails, 2.0), INK, seed=nxt()), .5))

# ---- the route: start lower-left, follow the roads, end at the pin (right-angle-ish turns with hand wobble)
start = R(cols[2] + 2, rows[min(len(rows) - 2, [i for i, r in enumerate(rows) if r > 860][0])] - 1)
cx_ave = [c for c in cols if abs(c - AVE_X) < 1][0]
rt_un = [(cols[2], rows[[i for i, r in enumerate(rows) if r > 860][0]]), (cols[4], rows[[i for i, r in enumerate(rows) if r > 860][0]]),
         (cols[4], rows[[i for i, r in enumerate(rows) if r > 760][0]]), (cx_ave, rows[[i for i, r in enumerate(rows) if r > 760][0]]), (cx_ave, AVE_Y)]
rt = []
for i in range(len(rt_un) - 1):
    (x0, y0), (x1, y1) = rt_un[i], rt_un[i + 1]
    n = max(4, int(math.hypot(x1 - x0, y1 - y0) / 18))
    for k in range(n):
        t = k / n
        rt.append((x0 + (x1 - x0) * t + rng.gauss(0, 1.2), y0 + (y1 - y0) * t + rng.gauss(0, 1.2)))
rt.append(rt_un[-1])
rt = [R(*p) for p in rt]
# bend the last leg so it ends exactly under the pin
ex, ey = rt[-1]
rt = [(x + (PIN[0] - ex) * max(0, (i / len(rt) - .6) / .4), y + (PIN[1] - ey) * max(0, (i / len(rt) - .6) / .4)) for i, (x, y) in enumerate(rt)]
rt = curve(rt, 220)
rm = stroke_mask(W, H, rt, 15, taper=(0.02, 0.02))
route = gouache_paint(rm, ROUTE, "#3a7be0", seed=nxt(), rough=1.8, streak=.5, density=.96)
route = over(scale_alpha(pigment(stroke_mask(W, H, rt, 22, taper=(0.02, 0.02)), ROUTE_D, seed=nxt(), density=.35, edge=.6, bloom=.2, rough=2.5, feather=1.6), .55), route)
scene = over(scene, route)
# start marker: hollow ring in blue, and small pale 'stops' along the way
sx, sy = rt[0]
ring = np.clip(circle_mask(W, H, sx, sy, 15) - circle_mask(W, H, sx, sy, 8), 0, 1)
scene = over(scene, gouache_paint(circle_mask(W, H, sx, sy, 17), "#ffffff", seed=nxt(), rough=1))
scene = over(scene, gouache_paint(ring, ROUTE, seed=nxt(), rough=1.2))
stops = [rt[int(len(rt) * t)] for t in (.3, .62)]
scene = over(scene, gouache_paint(dots_mask(W, H, [(x, y, 6) for x, y in stops]), "#ffffff", seed=nxt(), rough=.8))

# tiny street-name squiggles (illegible ink), giving the map its hand-lettered feel
sq = []
for _ in range(18):
    c = rng.choice(cells); x0, y0, x1, y1 = c[:4]
    if x1 - x0 < 90:
        continue
    ax, ay = x0 + 12, (y0 + y1) / 2
    pts = []
    for k in range(int((x1 - x0 - 24) / 6)):
        pts.append(R(ax + k * 6, ay + rng.uniform(-2.5, 2.5) * (1 if k % 2 else -1)))
    sq.append((pts, 1.3))
scene = over(scene, scale_alpha(ink(strokes_mask(W, H, sq, taper=(.1, .1)), INK, seed=nxt(), bleed=.5), .28))

# vignette: gently lighter toward the top so the white search pill and pin read
yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
scene[..., :3] = np.clip(scene[..., :3] * (1 + (0.04 * (1 - yy))[..., None]), 0, 1)
scene[..., 3] = 1
print("map", save_opaque(scene, f"{OUT}/map.webp", quality=76), round(kb(f"{OUT}/map.webp")))
to_image(scene).convert("RGB").save(f"{PRE}/map.png")
