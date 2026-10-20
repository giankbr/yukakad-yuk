"""Chat Hijau — ink-doodle chat wallpaper tile (seamless) + watercolour map vignette for the event cards.
Run: python3 -I /tmp/pen/art/themes/chat-hijau.py
Paints: brown-grey ink (#7d7466) on the beige wall, teal/sage/sand watercolour for the map.
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p6_lib import *

OUT = "/root/w/frontend/public/themes/art/chat-hijau"
os.makedirs(OUT, exist_ok=True)
nxt = Seeds(300)
INK = "#6f6657"

# ---------------------------------------------------------------- doodles (each in a 100x100 box, polylines)
def heart(cx, cy, s):
    pts = []
    for i in range(40):
        t = i / 39 * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 17, cy + y * s / 17))
    return [pts]

def rings(cx, cy, s):
    a = arc_pts(cx - s * 0.45, cy, s * 0.8, 0, math.tau * 0.98, 36)
    b = arc_pts(cx + s * 0.45, cy, s * 0.8, math.pi, math.pi + math.tau * 0.98, 36)
    return [a, b]

def envelope(cx, cy, s):
    w, h = s * 1.5, s
    box = [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h), (cx - w, cy - h)]
    flap = [(cx - w, cy - h), (cx, cy + h * 0.15), (cx + w, cy - h)]
    return [box, flap]

def flower(cx, cy, s):
    out = []
    for k in range(5):
        a = k / 5 * math.tau - math.pi / 2
        p = petal_pts(cx + math.cos(a) * s * 0.25, cy + math.sin(a) * s * 0.25, s * 0.95, s * 0.42, a, 16)
        out.append(p + [p[0]])
    out.append(arc_pts(cx, cy, s * 0.22, 0, math.tau, 16) + [arc_pts(cx, cy, s * 0.22, 0, 0.1, 2)[0]])
    out.append(curve([(cx, cy + s * 0.5), (cx + s * 0.15, cy + s * 1.3), (cx - s * 0.1, cy + s * 2.1)], 20))
    return out

def leaf_sprig(cx, cy, s):
    stem = curve([(cx, cy + s * 1.4), (cx + s * 0.15, cy), (cx - s * 0.1, cy - s * 1.4)], 24)
    out = [stem]
    for i in range(5):
        t = 0.2 + i * 0.16
        bx, by = stem[int(t * 23)]
        side = -1 if i % 2 else 1
        a = -math.pi / 2 + side * 1.05
        p = petal_pts(bx, by, s * 0.7, s * 0.28, a, 12)
        out.append(p + [p[0]])
    return out

def cup(cx, cy, s):
    body = curve([(cx - s, cy - s * 0.6), (cx - s * 0.85, cy + s * 0.6), (cx - s * 0.5, cy + s * 0.9), (cx + s * 0.5, cy + s * 0.9), (cx + s * 0.85, cy + s * 0.6), (cx + s, cy - s * 0.6)], 30)
    rim = [(cx - s * 1.05, cy - s * 0.6), (cx + s * 1.05, cy - s * 0.6)]
    handle = arc_pts(cx + s * 1.0, cy, s * 0.45, -math.pi / 2, math.pi / 2, 14)
    steam = [curve([(cx - s * 0.35 + k * s * 0.4, cy - s * 0.9), (cx - s * 0.2 + k * s * 0.4, cy - s * 1.3), (cx - s * 0.4 + k * s * 0.4, cy - s * 1.7)], 14) for k in range(2)]
    return [body, rim, handle] + steam

def star(cx, cy, s):
    pts = [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * (s if i % 2 == 0 else s * 0.45), cy + math.sin(-math.pi / 2 + i * math.pi / 5) * (s if i % 2 == 0 else s * 0.45)) for i in range(10)]
    return [pts + [pts[0]]]

def bubble(cx, cy, s):
    r = arc_pts(cx, cy, s, -2.2, math.tau - 2.6, 36)
    tail = [r[-1], (cx - s * 0.9, cy + s * 1.35), r[0]]
    return [r, tail]

def camera(cx, cy, s):
    w, h = s * 1.3, s * 0.85
    box = [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h), (cx - w, cy - h)]
    lens = arc_pts(cx, cy + s * 0.05, s * 0.48, 0, math.tau, 20); lens.append(lens[0])
    top = [(cx - s * 0.45, cy - h), (cx - s * 0.3, cy - h - s * 0.35), (cx + s * 0.3, cy - h - s * 0.35), (cx + s * 0.45, cy - h)]
    return [box, lens, top]

def sparkle(cx, cy, s):
    return [[(cx, cy - s), (cx, cy + s)], [(cx - s, cy), (cx + s, cy)]]

DOODLES = [heart, rings, envelope, flower, leaf_sprig, cup, star, bubble, camera, sparkle, heart, flower]

T = 512
rng = random.Random(11)
tile = blank(T, T)
# jittered grid placement so density stays even but nothing lines up
cells = [(i, j) for i in range(4) for j in range(4)]
rng.shuffle(cells)
for n, (i, j) in enumerate(cells):
    fn = DOODLES[n % len(DOODLES)]
    s = rng.uniform(17, 22) if fn is not sparkle else 7
    cx, cy = (i + 0.5) * T / 4 + rng.uniform(-28, 28), (j + 0.5) * T / 4 + rng.uniform(-28, 28)
    rot = rng.uniform(-0.5, 0.5)
    layer = blank(T, T)
    for pl in fn(T / 2, T / 2, s):
        cr, sr = math.cos(rot), math.sin(rot)
        pl = [(T / 2 + (x - T / 2) * cr - (y - T / 2) * sr, T / 2 + (x - T / 2) * sr + (y - T / 2) * cr) for x, y in pl]
        pl = [(x + rng.gauss(0, 0.6), y + rng.gauss(0, 0.6)) for x, y in pl]
        m = stroke_mask(T, T, densify(pl, 3.0), rng.uniform(3.0, 3.8), taper=(0.06, 0.08))
        layer = over(layer, linocut(m, INK, seed=nxt(), wear=0.3, rough=1.0))
    layer = np.roll(layer, (int(cy - T / 2), int(cx - T / 2)), axis=(0, 1))  # wraps → seamless
    tile = over(tile, layer)
# a few tiny dots
for _ in range(14):
    m = circ(T, T, rng.uniform(0, T), rng.uniform(0, T), rng.uniform(1.6, 2.6))
    tile = over(tile, linocut(np.roll(m, (0, 0), axis=(0, 1)), INK, seed=nxt(), wear=0.2))
tile[..., 3] *= 0.26
save_texture(tile, f"{OUT}/wallpaper.webp", quality=80)
print("wallpaper", round(kb(f"{OUT}/wallpaper.webp")), "KB")
# preview tiled 2x2 on the wall colour
pv = np.ones((T * 2, T * 2, 4), np.float32); pv[..., :3] = hex_rgb("#e9e2d6")
big = np.tile(tile, (2, 2, 1))
to_image(over(pv, big)).convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{PREV}/ch-wallpaper.png")

# ---------------------------------------------------------------- watercolour map vignette (540x180 → 270x90 css)
W, H = 540, 180
rng = random.Random(5)
mp = blank(W, H)
# ground wash: sage
ground = np.ones((H, W), np.float32)
mp = glaze(mp, pigment(ground, "#d9e8dc", "#cfe2d3", seed=nxt(), density=0.9, edge=0.0, bloom=0.35, gran=0.16, rough=0, mottle=0.7))
# park blobs (greener) and a pond
for (x, y, rx, ry) in [(90, 50, 70, 40), (430, 130, 80, 48), (300, 25, 55, 28)]:
    m = shape_mask(W, H, deform(ellipse_pts(x, y, rx, ry, 10, rng.uniform(0, 3)), rng, 3, .25))
    mp = glaze(mp, pigment(m, "#a9d3b1", "#8fc49c", seed=nxt(), density=0.65, edge=0.6, bloom=0.4, gran=0.2))
pond = shape_mask(W, H, deform(ellipse_pts(470, 40, 40, 22, 10, 0.4), rng, 3, .3))
mp = glaze(mp, pigment(pond, "#9fd0e0", "#7fbdd3", seed=nxt(), density=0.7, edge=0.6, bloom=0.3))
# blocks (sand buildings)
for _ in range(26):
    x, y = rng.uniform(10, W - 40), rng.uniform(8, H - 30)
    w, h = rng.uniform(16, 40), rng.uniform(12, 28)
    if ((x - 470) ** 2 / 45 ** 2 + (y - 40) ** 2 / 26 ** 2) < 1.2:
        continue
    m = shape_mask(W, H, deform([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], rng, 2, .03), smooth=False)
    mp = glaze(mp, pigment(m, "#eadcc4", "#e0cfae", seed=nxt(), density=0.6, edge=0.5, bloom=0.2, gran=0.08, rough=2))
# roads: cream strokes with a faint darker edge
roads = [
    curve([(0, 95), (140, 88), (300, 100), (540, 86)], 40),
    curve([(0, 40), (180, 46), (360, 36), (540, 44)], 40),
    curve([(0, 150), (200, 142), (540, 152)], 30),
    curve([(120, 0), (128, 90), (116, 180)], 24),
    curve([(260, 0), (252, 100), (262, 180)], 24),
    curve([(400, 0), (392, 90), (404, 180)], 24),
]
for i, r in enumerate(roads):
    wdt = [12, 9, 10, 7, 8, 6][i]
    rm = stroke_mask(W, H, r, wdt + 3, taper=(0.01, 0.01))
    mp = over(mp, pigment(rm, "#fbf7ee", "#f5efe2", seed=nxt(), density=0.95, edge=0.25, bloom=0.0, gran=0.1, rough=2))
    edge = stroke_mask(W, H, r, wdt + 5, taper=(0.01, 0.01)) - gaussian_filter(rm, 0.5)
    mp = glaze(mp, pigment(np.clip(edge, 0, 1), "#b9a98e", seed=nxt(), density=0.35, edge=0.0, bloom=0, rough=1.5, feather=0.8))
# a dashed route in teal to the centre
route = curve([(40, 170), (120, 120), (200, 118), (250, 95), (270, 78)], 40)
rm = stroke_mask(W, H, route, 4, taper=(0.02, 0.02))
dash = (np.sin(np.arange(W) * 0.55)[None, :] > 0.1).astype(np.float32)
mp = over(mp, pigment(rm * dash, "#0b8a6e", "#0a7a60", seed=nxt(), density=0.9, edge=0.3, bloom=0, rough=1))
# pin shadow spot (the lucide pin bobs above it)
sp = circ(W, H, 270, 110, 14)
mp = glaze(mp, pigment(gaussian_filter(sp, 4), "#6a8f7d", seed=nxt(), density=0.35, edge=0, bloom=0, rough=0))
mp[..., 3] = 1.0
print("map", save_full(mp, f"{OUT}/map.webp", (540, 180), 80) // 1024, "KB")
to_image(mp).convert("RGB").save(f"{PREV}/ch-map.png")
