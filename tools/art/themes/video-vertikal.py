"""Video Vertikal — gouache gift stickers (mawar, boneka, singa, galaxy) replacing emoji, and painted
series thumbnails (night street, cyan sea, galaxy, final-premiere) replacing flat CSS gradients.
Run: python3 -I /tmp/pen/art/themes/video-vertikal.py
Paints: pink (#fe2c55), cyan (#25f4ee), violet (#b06bff), cream (#fff3e0), ink (#1b1216).
"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p6_lib import *

OUT = "/root/w/frontend/public/themes/art/video-vertikal"
os.makedirs(OUT, exist_ok=True)
nxt = Seeds(800)
INK = "#1b1216"
S = 136

def outline(m, w=4.0, wob=0.3, col=INK):
    return brush_outline(m, w, nxt(), col, mix(col, "#ffffff", .12), wobble=wob, density=0.9)

def paint(m, c, c2=None, light=None, k=0.25, rough=2.0, streak=0.8, R=S):
    g = gouache_paint(m, c, c2 or mix(c, "#000000", .1), seed=nxt(), rough=rough, streak=streak)
    if light:
        g = darken(g, m, light[0], light[1], k, radius=R * 0.9)
    return g

def sticker(layer, mask, grow=5):
    """Cream die-cut sticker edge under the painted shape."""
    edge = np.clip(gaussian_filter(mask, grow) * 3.0, 0, 1)
    return over(gouache_paint(edge, "#fff3e0", "#f6e6cf", seed=nxt(), rough=1.5, streak=0.3), layer)

# ---------------------------------------------------------------- mawar (rose)
rng = random.Random(1)
rose = blank(S, S)
petals = np.zeros((S, S), np.float32)
for i in range(7):
    a = i / 7 * math.tau
    m = shape_mask(S, S, deform(ellipse_pts(68 + math.cos(a) * 14, 58 + math.sin(a) * 12, 24, 17, 12, a), rng, 2, .1))
    rose = over(rose, paint(m, "#fe2c55", "#c91f44", light=(50, 30), k=0.35))
    rose = over(rose, brush_outline(m, 2.2, nxt(), "#8f1530", wobble=0.4, density=0.55))
    petals = np.maximum(petals, m)
inner = shape_mask(S, S, deform(ellipse_pts(70, 58, 18, 15, 12, .3), rng, 2, .1))
rose = over(rose, paint(inner, "#ff5c7c", "#fe2c55", light=(55, 40), k=0.3))
core = shape_mask(S, S, deform(ellipse_pts(72, 58, 8, 7, 10), rng, 2, .1))
rose = over(rose, paint(core, "#c91f44", "#9e1734"))
spiral = curve([(72, 58), (80, 56), (78, 64), (66, 64), (62, 54), (74, 46), (88, 58)], 40)
rose = over(rose, linocut(stroke_mask(S, S, spiral, 2.6, taper=(0.05, 0.3)), INK, seed=nxt(), wear=0.3))
stem = stroke_mask(S, S, curve([(70, 86), (72, 104), (68, 126)], 20), 5, taper=(0.02, 0.1))
leaf = shape_mask(S, S, deform(petal_pts(72, 106, 30, 11, 0.5, 14), rng, 2, .08))
rose = over(rose, paint(stem, "#3e9c5a", "#2f7a46"))
rose = over(rose, paint(leaf, "#4fb36b", "#3e9c5a", light=(60, 90), k=0.3))
rose = over(rose, linocut(stroke_mask(S, S, curve([(74, 106), (88, 102), (100, 98)], 12), 1.8, taper=(0.1, 0.4)), "#2f7a46", seed=nxt()))
rose = over(rose, outline(np.maximum(petals, inner), 3.6))
rose = over(rose, outline(leaf, 3.0))
rose = sticker(rose, np.maximum(np.maximum(petals, leaf), stem))

# ---------------------------------------------------------------- boneka (teddy bear)
rng = random.Random(2)
bear = blank(S, S)
BR, BR2 = "#d7975a", "#b97a40"
ears = np.maximum(circ(S, S, 44, 42, 14), circ(S, S, 94, 42, 14))
head = circ(S, S, 69, 60, 32)
body = shape_mask(S, S, deform(ellipse_pts(69, 108, 30, 26, 14), rng, 2, .05))
arms = np.maximum(shape_mask(S, S, deform(ellipse_pts(40, 100, 13, 9, 10, -0.6), rng, 2, .05)), shape_mask(S, S, deform(ellipse_pts(98, 100, 13, 9, 10, 0.6), rng, 2, .05)))
for m in (ears, body, arms, head):
    bear = over(bear, paint(m, BR, BR2, light=(45, 40), k=0.3))
bear = over(bear, outline(ears, 3.2)); bear = over(bear, outline(arms, 3.2))
bear = over(bear, paint(head, BR, BR2, light=(45, 40), k=0.3))
inner_ears = np.maximum(circ(S, S, 44, 42, 7), circ(S, S, 94, 42, 7))
muzzle = shape_mask(S, S, deform(ellipse_pts(69, 70, 15, 11, 12), rng, 2, .05))
belly = shape_mask(S, S, deform(ellipse_pts(69, 112, 17, 14, 12), rng, 2, .05))
for m in (inner_ears, muzzle, belly):
    bear = over(bear, paint(m, "#f3d7b1", "#e8c596", light=(50, 40), k=0.2))
nose = shape_mask(S, S, deform(ellipse_pts(69, 66, 5.5, 4, 10), rng, 2, .05))
bear = over(bear, paint(nose, INK, "#2b1f24"))
for x in (58, 80):
    bear = over(bear, paint(circ(S, S, x, 56, 3.4), INK))
    bear = over(bear, paint(circ(S, S, x + 1, 55, 1.1), "#ffffff", rough=0.4))
bear = over(bear, linocut(stroke_mask(S, S, curve([(63, 73), (67, 77), (71, 77), (75, 73)], 14), 2.2, taper=(0.2, 0.2)), INK, seed=nxt()))
bow = np.maximum(shape_mask(S, S, deform([(69, 88), (54, 80), (56, 96)], rng, 2, .03), smooth=False), shape_mask(S, S, deform([(69, 88), (84, 80), (82, 96)], rng, 2, .03), smooth=False))
bear = over(bear, paint(bow, "#fe2c55", "#c91f44"))
bear = over(bear, paint(circ(S, S, 69, 88, 4), "#c91f44"))
bear = over(bear, outline(np.maximum(head, body), 3.6))
bear = over(bear, outline(bow, 2.6))
bear = sticker(bear, np.maximum(np.maximum(ears, head), np.maximum(body, arms)))

# ---------------------------------------------------------------- singa (lion face)
rng = random.Random(3)
lion = blank(S, S)
mane = np.zeros((S, S), np.float32)
for i in range(12):
    a = i / 12 * math.tau
    r = 44 + rng.uniform(-4, 6)
    m = shape_mask(S, S, deform(petal_pts(68 + math.cos(a) * 26, 68 + math.sin(a) * 26, r - 20, 13, a, 12), rng, 2, .1))
    mane = np.maximum(mane, m)
mane = np.maximum(mane, circ(S, S, 68, 68, 44))
lion = over(lion, paint(mane, "#e0792e", "#b85a1c", light=(40, 30), k=0.35))
face = circ(S, S, 68, 70, 30)
lion = over(lion, paint(face, "#f2b85c", "#dd9c3e", light=(50, 50), k=0.3))
ears = np.maximum(circ(S, S, 46, 46, 9), circ(S, S, 90, 46, 9))
lion = over(lion, paint(ears, "#f2b85c", "#dd9c3e"))
muzzle = shape_mask(S, S, deform(ellipse_pts(68, 82, 16, 11, 12), rng, 2, .05))
lion = over(lion, paint(muzzle, "#fbe3b4", "#f0d095"))
nose = shape_mask(S, S, deform([(68, 84), (60, 76), (76, 76)], rng, 2, .03), smooth=False)
lion = over(lion, paint(nose, "#5a3a2a", "#3f2820"))
for x in (58, 78):
    lion = over(lion, paint(circ(S, S, x, 64, 3.6), INK))
    lion = over(lion, paint(circ(S, S, x + 1, 63, 1.2), "#ffffff", rough=0.4))
lion = over(lion, linocut(stroke_mask(S, S, curve([(60, 88), (64, 92), (68, 90), (72, 92), (76, 88)], 16), 2.2, taper=(0.2, 0.2)), INK, seed=nxt()))
for (x0, x1) in [(36, 48), (34, 48), (100, 88), (102, 88)]:
    y0 = 78 + (4 if x0 in (34, 102) else -2)
    lion = over(lion, linocut(stroke_mask(S, S, densify([(x0, y0), (x1, 80)], 2), 1.8, taper=(0.1, 0.2)), "#5a3a2a", seed=nxt()))
lion = over(lion, outline(mane, 3.6, wob=0.45))
lion = over(lion, outline(face, 3.0))
lion = sticker(lion, mane)

# ---------------------------------------------------------------- galaxy (planet + ring + stars)
rng = random.Random(4)
gal = blank(S, S)
disc = circ(S, S, 68, 68, 40)
gal = over(gal, paint(disc, "#4a2580", "#2b1250", light=(45, 40), k=0.3))
swirl = np.zeros((S, S), np.float32)
for i in range(3):
    swirl = np.maximum(swirl, stroke_mask(S, S, curve([(40, 60 + i * 12), (60, 52 + i * 12), (90, 60 + i * 12), (104, 70 + i * 12)], 24), 5 - i, taper=(0.3, 0.3)) * disc)
gal = over(gal, tint_layer(gaussian_filter(swirl, 1.0), "#b06bff", 0.6))
gal = over(gal, tint_layer(gaussian_filter(circ(S, S, 52, 56, 12) * disc, 5), "#ff7ab6", 0.35))
ring_m = np.clip(shape_mask(S, S, ellipse_pts(68, 70, 60, 16, 40, -0.35)) - shape_mask(S, S, ellipse_pts(68, 70, 48, 10, 40, -0.35)), 0, 1)
front = np.ones((S, S), np.float32); front[:70, :] = 0  # lower half of the ring passes in front
ring_back = ring_m * (1 - front) * (1 - disc)
gal = over(gal, paint(ring_back, "#25f4ee", "#17b5b0"))
gal = over(gal, paint(ring_m * front, "#25f4ee", "#17b5b0", light=(50, 60), k=0.25))
stars = np.zeros((S, S), np.float32)
for (x, y, r) in [(22, 24, 4), (112, 30, 3), (20, 108, 2.6), (118, 112, 3.5), (100, 14, 2)]:
    pts = [(x + math.cos(-math.pi / 2 + i * math.pi / 4) * (r * 2.2 if i % 2 == 0 else r * 0.8), y + math.sin(-math.pi / 2 + i * math.pi / 4) * (r * 2.2 if i % 2 == 0 else r * 0.8)) for i in range(8)]
    stars = np.maximum(stars, shape_mask(S, S, pts, smooth=False))
gal = over(gal, glow(stars, "#fff3e0", 5, 0.5))
gal = over(gal, paint(stars, "#fff3e0", "#ffd98a", rough=0.8))
gal = over(gal, outline(disc, 3.4))
gal = over(gal, outline(ring_m, 2.4))
gal = sticker(gal, np.maximum(disc, ring_m), 4)

for name, arr in [("mawar", rose), ("boneka", bear), ("singa", lion), ("galaxy", gal)]:
    print(name, save_full(arr, f"{OUT}/gift-{name}.webp", (S, S), 84) // 1024, "KB")
sheet([rose, bear, lion, gal], f"{PREV}/vv-gifts.png", bg="#161616")

# ---------------------------------------------------------------- series thumbnails 128x172 (css 64x86)
TW, TH = 128, 172

def night_street():
    sky = painted_sky(TW, TH, [(0, "#2a0b16"), (0.55, "#7a1230"), (1, "#fe2c55")], seed=nxt(), streak=0.8)
    rng = random.Random(11)
    # buildings silhouettes
    sil = np.zeros((TH, TW), np.float32)
    x = -4
    while x < TW:
        w = rng.uniform(14, 30); h = rng.uniform(40, 90)
        sil = np.maximum(sil, poly(TW, TH, [(x, TH), (x, TH - h), (x + w, TH - h), (x + w, TH)], rng, .01))
        x += w - 2
    sky = over(sky, gouache_paint(sil, "#1b0a10", "#2b0f18", seed=nxt(), rough=1.5))
    # lantern string + glowing lanterns
    string = curve([(0, 40), (40, 56), (90, 52), (128, 36)], 30)
    sky = over(sky, linocut(stroke_mask(TW, TH, string, 1.6, taper=(0.01, 0.01)), "#0d0508", seed=nxt()))
    lamps = np.zeros((TH, TW), np.float32)
    for t in (0.12, 0.32, 0.52, 0.72, 0.9):
        bx, by = string[int(t * 29)]
        lamps = np.maximum(lamps, circ(TW, TH, bx, by + 7, 5.5))
    sky = over(sky, glow(lamps, "#ffb347", 10, 0.9))
    sky = over(sky, gouache_paint(lamps, "#ffd166", "#ffb347", seed=nxt(), rough=1.0))
    # lit windows
    win = (np.random.default_rng(5).random((TH, TW)) > 0.994).astype(np.float32) * sil
    sky = over(sky, tint_layer(gaussian_filter(win, 0.6), "#ffd166", 0.8))
    return sky

def cyan_sea():
    sky = painted_sky(TW, TH, [(0, "#06303a"), (0.45, "#0e6e8c"), (0.5, "#25f4ee"), (1, "#0a4a58")], seed=nxt(), streak=0.9)
    rng = random.Random(12)
    sun = circ(TW, TH, 64, 78, 22)
    sky = over(sky, glow(sun, "#c9fffb", 14, 0.7))
    sky = over(sky, gouache_paint(sun, "#eafffd", "#bdfaf6", seed=nxt(), rough=1.2))
    for i in range(6):
        y = 96 + i * 12
        w = stroke_mask(TW, TH, curve([(rng.uniform(-10, 10), y + rng.uniform(-2, 2)), (64, y + rng.uniform(-3, 3)), (138, y + rng.uniform(-2, 2))], 20), 3.5 - i * 0.3, taper=(0.4, 0.4))
        sky = over(sky, tint_layer(w, "#c9fffb", 0.5 - i * 0.05))
    # a hand-cut cloud
    cl = np.zeros((TH, TW), np.float32)
    for (x, y, r) in [(24, 34, 10), (36, 30, 13), (50, 34, 9)]:
        cl = np.maximum(cl, circ(TW, TH, x, y, r))
    sky = over(sky, gouache_paint(cl, "#eafffd", "#bdfaf6", seed=nxt(), rough=2.0, density=0.85))
    return sky

def galaxy_sky():
    sky = painted_sky(TW, TH, [(0, "#1a0b3a"), (0.5, "#4a2580"), (1, "#b06bff")], seed=nxt(), streak=0.7)
    rng = random.Random(13)
    neb = np.zeros((TH, TW), np.float32)
    for _ in range(3):
        neb = np.maximum(neb, shape_mask(TW, TH, deform(ellipse_pts(rng.uniform(30, 100), rng.uniform(40, 130), rng.uniform(26, 44), rng.uniform(14, 24), 12, rng.uniform(0, 3)), rng, 3, .25)))
    sky = over(sky, tint_layer(gaussian_filter(neb, 8), "#ff7ab6", 0.4))
    st = (np.random.default_rng(6).random((TH, TW)) > 0.988).astype(np.float32)
    sky = over(sky, glow(st, "#ffffff", 2, 0.6))
    sky = over(sky, tint_layer(gaussian_filter(st, 0.5), "#ffffff", 0.9))
    big = np.zeros((TH, TW), np.float32)
    for (x, y, r) in [(30, 40, 4), (96, 120, 3.4), (80, 30, 2.6)]:
        pts = [(x + math.cos(-math.pi / 2 + i * math.pi / 4) * (r * 2.2 if i % 2 == 0 else r * 0.7), y + math.sin(-math.pi / 2 + i * math.pi / 4) * (r * 2.2 if i % 2 == 0 else r * 0.7)) for i in range(8)]
        big = np.maximum(big, shape_mask(TW, TH, pts, smooth=False))
    sky = over(sky, glow(big, "#fff3e0", 5, 0.5))
    sky = over(sky, gouache_paint(big, "#fff3e0", seed=nxt(), rough=0.6))
    return sky

def final_card():
    sky = painted_sky(TW, TH, [(0, "#25060f"), (0.6, "#7a1230"), (1, "#fe2c55")], seed=nxt(), streak=0.8)
    rng = random.Random(14)
    h = []
    for i in range(40):
        t = i / 39 * math.tau
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        h.append((64 + x * 2.0, 84 + y * 2.0))
    hm = shape_mask(TW, TH, deform(h, rng, 1, .02))
    sky = over(sky, glow(hm, "#fe2c55", 12, 0.8))
    sky = over(sky, gouache_paint(hm, "#fe2c55", "#ff5c7c", seed=nxt(), rough=2.0))
    sky = over(sky, brush_outline(hm, 3.0, nxt(), "#fff3e0", wobble=0.3, density=0.8))
    sp = np.zeros((TH, TW), np.float32)
    for _ in range(14):
        sp = np.maximum(sp, circ(TW, TH, rng.uniform(8, 120), rng.uniform(10, 160), rng.uniform(1, 2.4)))
    sky = over(sky, tint_layer(sp, "#fff3e0", 0.85))
    return sky

for name, fn in [("thumb-0", night_street), ("thumb-1", cyan_sea), ("thumb-2", galaxy_sky), ("thumb-final", final_card)]:
    arr = fn(); arr[..., 3] = 1
    print(name, save_full(arr, f"{OUT}/{name}.webp", (TW, TH), 82) // 1024, "KB")
sheet([night_street(), cyan_sea(), galaxy_sky(), final_card()], f"{PREV}/vv-thumbs.png", bg="#000000")
