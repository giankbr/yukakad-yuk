"""Khitan Ceria — folk-poster gouache: waving boy in peci & baju koko (body + arm layers + chest star for the
existing motion), gouache bunting flags with brush-pen outlines, and a painted paper-confetti tile.
Run: python3 -I /tmp/pen/art/themes/khitan-ceria.py
Paints: navy ink (#17324d), coral (#ff7a59), sun (#ffc93c), teal (#12a594), sky (#4cc3ff), lilac (#a77bf3), skin (#f5c9a0).
"""
import sys, math, random, os
sys.path.insert(0, "/tmp/pen/art")
from art import *

OUT = "/root/w/frontend/public/themes/art/khitan-ceria"
PREV = "/tmp/pen/nt2-E"
os.makedirs(OUT, exist_ok=True)
NAVY = "#17324d"
seed = [700]
def nxt():
    seed[0] += 7
    return seed[0]

def path_mask(W, H, build, stroke=0.0):
    def draw(cv):
        p = skia.Path(); build(p)
        paint = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        if stroke:
            paint.setStyle(skia.Paint.kStroke_Style); paint.setStrokeWidth(stroke)
            paint.setStrokeCap(skia.Paint.kRound_Cap); paint.setStrokeJoin(skia.Paint.kRound_Join)
        cv.c.drawPath(p, paint)
    return mask_from(W, H, draw)

def circ(W, H, x, y, r):
    return mask_from(W, H, lambda cv: cv.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)))

def brush_outline(mask, width, sd, wobble=0.35):
    """Brush-pen contour around a mask: band around the 0.5 level, width breathing with noise."""
    h, w = mask.shape
    g = gaussian_filter(mask, width * 0.45)
    th = 0.5 * (1 - wobble + wobble * 2 * fbm(w, h, sd, 40, 2))
    tw = th * 0.75
    band = np.clip((tw - np.abs(g - 0.5)) / np.maximum(tw, 0.02) * 2.2, 0, 1)
    return gouache_paint(band, NAVY, "#20405f", seed=sd, rough=1.2, streak=0.3)

def save_full(arr, path, size, quality=82):
    to_image(arr).resize(size, Image.LANCZOS).save(path, "WEBP", quality=quality, method=6)

# ---------------------------------------------------------------- boy (body layer + waving arm layer)
S = 2.0
W = H = int(220 * S)
P = lambda x, y: (x * S, y * S)
rng = random.Random(6)
body = blank(W, H)

disc = circ(W, H, *P(110, 118), 96 * S)
body = over(body, gouache_paint(disc, "#dff7ee", "#cdeee2", seed=nxt(), rough=4, streak=0.8, dry=0.08))
# a few lighter dabs on the disc so it isn't a flat sticker
for i in range(5):
    m = shape_mask(W, H, deform(ellipse_pts(*P(rng.uniform(40, 180), rng.uniform(40, 120)), rng.uniform(10, 22) * S, rng.uniform(6, 12) * S, 9, rng.uniform(0, 3)), rng, 2, .15)) * disc
    body = over(body, gouache_paint(m, "#ebfbf4", seed=nxt(), rough=2, streak=0.4, density=0.55))

def torso(p):
    p.moveTo(*P(58, 222)); p.cubicTo(*P(58, 170), *P(78, 146), *P(110, 146)); p.cubicTo(*P(142, 146), *P(162, 170), *P(162, 222)); p.close()
tm = path_mask(W, H, torso)
body = over(body, gouache_paint(tm, "#fbfaf4", "#f3f1ea", seed=nxt(), rough=2.5, streak=1.0))
sh = shape_mask(W, H, deform(ellipse_pts(*P(76, 200), 26 * S, 50 * S, 10, .2), rng, 2, .1)) * tm
body = over(body, gouache_paint(gaussian_filter(sh, 4), "#dfe9ef", seed=nxt(), rough=1, streak=0.6, density=0.75))
body = over(body, brush_outline(tm, 7, nxt()))
collar = path_mask(W, H, lambda p: (p.moveTo(*P(96, 148)), p.lineTo(*P(110, 164)), p.lineTo(*P(124, 148)), p.close()))
body = over(body, gouache_paint(collar, "#12a594", "#0f9384", seed=nxt(), rough=1.5))
body = over(body, brush_outline(collar, 5, nxt()))
lines = np.maximum(stroke_mask(W, H, curve([P(110, 164), P(110.5, 192), P(110, 222)], 30), 7.5, taper=(0.02, 0.02)),
                   stroke_mask(W, H, curve([P(70, 176), P(64, 196), P(62, 220)], 20), 6, taper=(0.05, 0.02)))
body = over(body, gouache_paint(lines, NAVY, seed=nxt(), rough=0.8))
for y in (180, 198):
    body = over(body, gouache_paint(circ(W, H, *P(110, y), 3.2 * S), NAVY, seed=nxt(), rough=0.6))
# ears + head
ears = np.maximum(circ(W, H, *P(72, 104), 9 * S), circ(W, H, *P(148, 104), 9 * S))
head = circ(W, H, *P(110, 100), 40 * S)
SK, SK2 = "#f5c9a0", "#efbb8e"
body = over(body, gouache_paint(ears, SK, SK2, seed=nxt(), rough=1.5))
body = over(body, brush_outline(ears, 6, nxt()))
body = over(body, gouache_paint(head, SK, SK2, seed=nxt(), rough=1.8, streak=0.8))
hs = shape_mask(W, H, deform(ellipse_pts(*P(88, 112), 22 * S, 30 * S, 10, .3), rng, 2, .1)) * head
body = over(body, gouache_paint(gaussian_filter(hs, 5), "#e9ab80", seed=nxt(), rough=1, density=0.45))
body = over(body, brush_outline(head, 7, nxt()))
def peci(p):
    p.moveTo(*P(70, 86)); p.cubicTo(*P(67, 56), *P(84, 44), *P(110, 44)); p.cubicTo(*P(136, 44), *P(153, 56), *P(150, 86)); p.close()
pm = path_mask(W, H, peci)
body = over(body, gouache_paint(pm, "#1d3b5a", NAVY, seed=nxt(), rough=1.8, streak=1.2))
band = stroke_mask(W, H, curve([P(72, 73), P(110, 72), P(148, 73)], 30), 11, taper=(0.02, 0.02)) * pm
body = over(body, gouache_paint(band, "#ffc93c", "#f5b72a", seed=nxt(), rough=0.8, streak=0.4))
shine = stroke_mask(W, H, curve([P(120, 52), P(134, 58), P(142, 68)], 14), 5, taper=(0.3, 0.4)) * pm
body = over(body, gouache_paint(shine, "#3d5f82", seed=nxt(), rough=0.6, density=0.7))
body = over(body, brush_outline(pm, 6, nxt()))
# face
for x in (95, 125):
    body = over(body, gouache_paint(circ(W, H, *P(x, 104), 4.6 * S), NAVY, seed=nxt(), rough=0.7))
    body = over(body, gouache_paint(circ(W, H, *P(x + 1.6, 102.4), 1.5 * S), "#ffffff", seed=nxt(), rough=0.3))
smile = stroke_mask(W, H, curve([P(97, 118), P(104, 124.5), P(110, 126), P(116, 124.5), P(123, 118)], 30), 6.5, taper=(0.18, 0.18))
body = over(body, gouache_paint(smile, NAVY, seed=nxt(), rough=0.7))
for x in (84, 136):
    m = shape_mask(W, H, deform(ellipse_pts(*P(x, 116.5), 6.5 * S, 5 * S, 9), rng, 2, .1))
    body = over(body, gouache_paint(m, "#ff8f73", "#ff7a59", seed=nxt(), rough=1.2, density=0.45))

arm = blank(W, H)
def sleeve(p):
    p.moveTo(*P(152, 172)); p.cubicTo(*P(166, 162), *P(178, 142), *P(182, 116))
am_out = path_mask(W, H, sleeve, stroke=22 * S)
am_in = path_mask(W, H, sleeve, stroke=15 * S)
arm = over(arm, gouache_paint(am_out, NAVY, "#20405f", seed=nxt(), rough=1.5))
arm = over(arm, gouache_paint(am_in, "#fbfaf4", "#eef0ea", seed=nxt(), rough=1.4, streak=0.8))
hand = circ(W, H, *P(183, 106), 12 * S)
arm = over(arm, gouache_paint(hand, SK, SK2, seed=nxt(), rough=1.4))
arm = over(arm, brush_outline(hand, 6.5, nxt()))

save_full(body, f"{OUT}/boy.webp", (440, 440))
save_full(arm, f"{OUT}/boy-arm.webp", (440, 440))
print("boy", os.path.getsize(f"{OUT}/boy.webp"), os.path.getsize(f"{OUT}/boy-arm.webp"))
pv = np.ones((H, W, 4), np.float32); pv[..., :3] = hex_rgb("#ffffff")
to_image(over(over(pv, body), arm)).convert("RGB").save(f"{PREV}/kc-boy.png")

# chest star (twirls on its own)
T = 120
rng = random.Random(2)
pts = [(60 + math.cos(-math.pi / 2 + i * math.pi / 5) * (46 if i % 2 == 0 else 21), 62 + math.sin(-math.pi / 2 + i * math.pi / 5) * (46 if i % 2 == 0 else 21)) for i in range(10)]
sm = gaussian_filter(shape_mask(T, T, deform(pts, rng, 1, 0.02), smooth=False), 1.2)
star = over(gouache_paint(sm, "#ffc93c", "#f7b52a", seed=nxt(), rough=1.2), brush_outline(sm, 7, nxt()))
print("chest-star", save_asset(star, f"{OUT}/chest-star.webp", max_w=48, quality=84))

# ---------------------------------------------------------------- bunting flags (one per colour)
COLORS = ["#ff7a59", "#ffc93c", "#12a594", "#4cc3ff", "#a77bf3"]
for i, c in enumerate(COLORS):
    W, H = 140, 150
    rng = random.Random(40 + i)
    tri = [(10 + rng.uniform(-1, 1), 12), (130 + rng.uniform(-1, 1), 12 + rng.uniform(-1, 1)), (70 + rng.uniform(-3, 3), 140)]
    m = shape_mask(W, H, deform(tri, rng, 2, 0.008), smooth=False)
    f = gouache_paint(m, c, mix(c, "#000000", .1), seed=nxt(), rough=1.6, streak=1.1)
    hem = stroke_mask(W, H, curve([(16, 26), (70, 26.5), (124, 26)], 30), 9, taper=(0.02, 0.02)) * m
    f = over(f, gouache_paint(hem, mix(c, "#ffffff", .35), seed=nxt(), rough=1.0, density=0.85))
    dot = circ(W, H, 70, 66, 10) * m
    f = over(f, gouache_paint(dot, "#fffaf0", seed=nxt(), rough=1.0, density=0.9))
    f = over(f, brush_outline(m, 6.5, nxt(), wobble=0.25))
    save_full(f, f"{OUT}/flag-{i}.webp", (70, 75), quality=84)
print("flags", sum(os.path.getsize(f"{OUT}/flag-{i}.webp") for i in range(5)))

# ---------------------------------------------------------------- confetti tile (transparent)
T = 720
rng = random.Random(77)
tile = blank(T, T)
placed = []
for i in range(9):
    for _ in range(80):
        x, y = rng.uniform(50, T - 50), rng.uniform(50, T - 50)
        if all(math.hypot(x - a, y - b) > 190 for a, b in placed): break
    placed.append((x, y))
    c = COLORS[i % 5]
    kind = i % 3
    ang = rng.uniform(0, math.pi)
    if kind == 0:
        L, Wd = 22, 22
    elif kind == 1:
        L, Wd = 34, 14
    if kind < 2:
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(x + ca * dx - sa * dy, y + sa * dx + ca * dy) for dx, dy in ((-L / 2, -Wd / 2), (L / 2, -Wd / 2), (L / 2, Wd / 2), (-L / 2, Wd / 2))]
        m = gaussian_filter(shape_mask(T, T, deform(pts, rng, 1, 0.03), smooth=False), 1.5)
    else:
        m = mask_from(T, T, lambda cv: cv.c.drawCircle(x, y, 13, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=7)))
    tile = over(tile, gouache_paint(m, c, mix(c, "#000000", .12), seed=nxt(), rough=1.5, streak=0.8, density=0.9))
save_texture(to_image(tile).resize((480, 480), Image.LANCZOS), f"{OUT}/confetti.webp", quality=82)
print("confetti", os.path.getsize(f"{OUT}/confetti.webp"))
