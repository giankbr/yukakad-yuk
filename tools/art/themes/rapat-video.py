"""Rapat Video — painted 'virtual backgrounds' for the two avatar tiles on the cover (gouache room / night garden)
plus a subtle screen-grain tile. Run: python3 -I /tmp/pen/art/themes/rapat-video.py
Tiles are 2x of ~176x150 css.
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p7 import *  # noqa

OUT = "/root/w/frontend/public/themes/art/rapat-video"
PRE = "/tmp/pen/nt3-P7/rv"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(12)
seed = [1200]
def nxt():
    seed[0] += 3
    return seed[0]

W, H = 400, 320

# ---------- tile A: evening living room (teal wall, window with dusk sky, plant, frames, shelf)
room = painted_sky(W, H, [(0, "#2f4a4c"), (.6, "#2a4244"), (1, "#22383a")], seed=nxt(), streak=.6, grain=.6)
# wainscot / floor band
floor = shape_mask(W, H, deform([(-10, 262), (W + 10, 258), (W + 10, H + 10), (-10, H + 10)], rng, 2, .01))
room = over(room, gouache_paint(floor, "#5a4636", "#4d3b2d", seed=nxt(), rough=2, streak=.8))
room = over(room, scale_alpha(gouache_paint(lines_mask(W, H, [[(-10, 262), (W + 10, 258)]], 3), "#8a6c52", seed=nxt(), rough=1), .8))
# window: frame + dusk sky with a moon, curtains both sides
wx, wy, ww, wh = 236, 44, 128, 150
sky = painted_sky(ww, wh, [(0, "#1f2a52"), (.55, "#4d3f70"), (1, "#b76a6a")], seed=nxt(), streak=.5)
win = blank(W, H); win[wy:wy + wh, wx:wx + ww] = sky
wm = shape_mask(W, H, deform(rrect_pts(wx, wy, ww, wh, 4, 3), rng, 1, .01))
win[..., 3] *= wm
room = over(room, win)
moon = circle_mask(W, H, wx + 92, wy + 42, 11)
room = over(room, scale_alpha(glow(moon, "#ffe9b8", radius=14, strength=.5), .7))
room = over(room, gouache_paint(moon, "#fff1c9", "#f6dc9c", seed=nxt(), rough=1))
# window muntins + frame
mun = lines_mask(W, H, [[(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], [(wx, wy + wh * .45), (wx + ww, wy + wh * .45)]], 4)
frame = np.clip(shape_mask(W, H, rrect_pts(wx - 8, wy - 8, ww + 16, wh + 16, 5, 3)) - shape_mask(W, H, rrect_pts(wx, wy, ww, wh, 3, 3)), 0, 1)
room = over(room, gouache_paint(np.maximum(mun, frame), "#d9cdb6", "#c9bda4", seed=nxt(), rough=1.4, streak=.5))
# curtains: two soft gouache drapes with vertical fold streaks
for (cx0, side) in [(wx - 34, -1), (wx + ww + 6, 1)]:
    drape = shape_mask(W, H, deform([(cx0, wy - 16), (cx0 + 30, wy - 16), (cx0 + 26 + side * 6, wy + wh + 30), (cx0 + 2 + side * 6, wy + wh + 30)], rng, 2, .02))
    room = over(room, gouache_paint(drape, "#b8865f", "#a5744f", seed=nxt(), rough=2, streak=1.0))
    folds = lines_mask(W, H, [[(cx0 + 8 + k * 8, wy - 10), (cx0 + 6 + k * 8 + side * 5, wy + wh + 24)] for k in range(3)], 2)
    room = over(room, scale_alpha(gouache_paint(folds, "#7f5638", seed=nxt(), rough=1), .45))
# shelf with books + a small frame on the left wall
shelf = shape_mask(W, H, deform([(26, 118), (150, 118), (150, 126), (26, 126)], rng, 1, .02))
room = over(room, gouache_paint(shelf, "#8a6c52", "#75593f", seed=nxt(), rough=1.4))
bx = 36
for k in range(7):
    bw, bh = rng.uniform(9, 15), rng.uniform(28, 44)
    book = shape_mask(W, H, deform([(bx, 118 - bh), (bx + bw, 118 - bh), (bx + bw, 118), (bx, 118)], rng, 1, .03))
    room = over(room, gouache_paint(book, rng.choice(["#c86b5c", "#e0b66a", "#6c9b86", "#a9bfd4", "#d08a74", "#8d7bb0"]), seed=nxt(), rough=1.2, streak=.6))
    bx += bw + rng.uniform(1, 4)
pic = shape_mask(W, H, deform(rrect_pts(52, 160, 60, 48, 2, 3), rng, 1, .01))
room = over(room, gouache_paint(pic, "#d9cdb6", seed=nxt(), rough=1.2))
room = over(room, gouache_paint(shape_mask(W, H, rrect_pts(58, 166, 48, 36, 1, 3)), "#8ba7a0", "#6f8d86", seed=nxt(), rough=1))
room = over(room, gouache_paint(shape_mask(W, H, deform([(58, 196), (74, 182), (86, 190), (96, 178), (106, 190), (106, 202), (58, 202)], rng, 1, .02)), "#4a6b5e", seed=nxt(), rough=1))
# monstera plant in a pot, bottom-left
pot = shape_mask(W, H, deform([(60, 232), (120, 232), (112, 290), (68, 290)], rng, 2, .02))
room = over(room, gouache_paint(pot, "#c9774f", "#b56642", seed=nxt(), rough=1.6, streak=.7))
for (ang, L) in [(-1.9, 70), (-1.35, 86), (-0.9, 66), (-2.35, 60), (-1.6, 50)]:
    stem = curve([(90, 236), (90 + math.cos(ang) * L * .5, 236 + math.sin(ang) * L * .5), (90 + math.cos(ang) * L, 236 + math.sin(ang) * L)], 20)
    room = over(room, gouache_paint(stroke_mask(W, H, stem, 3, taper=(.05, .3)), "#5b8a5a", seed=nxt(), rough=1))
    ex, ey = stem[-1]
    leaf = shape_mask(W, H, deform(ellipse_pts(ex, ey - 10, 22, 17, 12, ang + math.pi / 2), rng, 2, .1))
    # monstera splits: knock out a couple of wedges
    for k in range(3):
        a = ang + math.pi / 2 + rng.uniform(-1.2, 1.2)
        leaf -= stroke_mask(W, H, [(ex + math.cos(a) * 6, ey - 10 + math.sin(a) * 6), (ex + math.cos(a) * 26, ey - 10 + math.sin(a) * 26)], 4, taper=(.1, .5))
    room = over(room, gouache_paint(np.clip(leaf, 0, 1), rng.choice(["#5f9a62", "#4e8a56", "#6ea86a"]), "#3f7246", seed=nxt(), rough=1.6, streak=.5))
# warm lamp glow at right-bottom
room = over(room, scale_alpha(glow(circle_mask(W, H, 350, 250, 30), "#ffcf8a", radius=40, strength=.4), .5))
room[..., 3] = 1
print("bg-room", save_opaque(room, f"{OUT}/bg-room.webp", quality=80), round(kb(f"{OUT}/bg-room.webp")))
to_image(room).convert("RGB").save(f"{PRE}/bg-room.png")

# ---------- tile B: night garden with string lights and palm/leaf silhouettes (bokeh warm bulbs)
gard = painted_sky(W, H, [(0, "#101c2c"), (.5, "#17283a"), (1, "#1b3330")], seed=nxt(), streak=.5, grain=.6)
# distant foliage masses (soft dark green blobs)
fol = blank(W, H)
for i in range(12):
    x, y = rng.uniform(-20, W + 20), rng.uniform(160, 300)
    fol = over(fol, gouache_paint(shape_mask(W, H, deform(ellipse_pts(x, y, rng.uniform(50, 90), rng.uniform(40, 70), 12), rng, 2, .1)), rng.choice(["#1c3a33", "#24483d", "#2a5345", "#183630"]), seed=nxt(), rough=3, streak=.4, density=.9))
gard = over(gard, fol)
# string of lights: a sagging line with warm bulbs
for (y0, sag, n) in [(54, 30, 7), (96, 36, 6)]:
    pts = [(x, y0 + sag * math.sin(math.pi * x / W)) for x in np.linspace(-10, W + 10, 40)]
    gard = over(gard, scale_alpha(gouache_paint(lines_mask(W, H, [pts], 1.6), "#4a4a40", seed=nxt(), rough=.6), .8))
    for k in range(n):
        x = (k + .5) / n * W + rng.uniform(-8, 8); y = y0 + sag * math.sin(math.pi * x / W) + 8
        bulb = circle_mask(W, H, x, y, 5)
        gard = over(gard, scale_alpha(glow(bulb, "#ffcf7a", radius=18, strength=.7), .75))
        gard = over(gard, gouache_paint(bulb, "#fff0c2", "#ffe09a", seed=nxt(), rough=.8))
        gard = over(gard, gouache_paint(shape_mask(W, H, [(x - 2, y - 7), (x + 2, y - 7), (x + 2, y - 3), (x - 2, y - 3)]), "#3a3a30", seed=nxt(), rough=.5))
# palm fronds entering from the corners (silhouettes, slightly lit)
def frond(x, y, ang, L):
    global gard
    pts = [(x, y)]; a = ang; px, py = x, y
    for k in range(14):
        a += 0.05; px += math.cos(a) * L / 14; py += math.sin(a) * L / 14; pts.append((px, py))
    strokes = [(pts, 4)]
    for k in range(2, 14):
        (ax, ay), (bx, by) = pts[k - 1], pts[k]
        d = math.atan2(by - ay, bx - ax)
        for side in (-1, 1):
            la = d + side * 1.0; ll = L * .3 * (1 - k / 16)
            strokes.append(([(bx, by), (bx + math.cos(la) * ll * .6, by + math.sin(la) * ll * .6 + ll * .15), (bx + math.cos(la) * ll, by + math.sin(la) * ll + ll * .35)], 3.2))
    gard = over(gard, gouache_paint(strokes_mask(W, H, strokes), "#2b5a49", "#1e4538", seed=nxt(), rough=1.2, streak=.3))
frond(-20, 300, -0.9, 180); frond(-30, 200, -0.3, 150)
frond(W + 20, 310, math.pi + 1.1, 190); frond(W + 30, 150, math.pi + .5, 140)
# fireflies / bokeh dots
dots = dots_mask(W, H, [(rng.uniform(20, W - 20), rng.uniform(120, 280), rng.uniform(1.5, 3.5)) for _ in range(9)])
gard = over(gard, scale_alpha(glow(dots, "#ffe5a0", radius=6, strength=.6), .6))
gard = over(gard, scale_alpha(gouache_paint(dots, "#fff2c8", seed=nxt(), rough=.5), .8))
gard[..., 3] = 1
print("bg-garden", save_opaque(gard, f"{OUT}/bg-garden.webp", quality=80), round(kb(f"{OUT}/bg-garden.webp")))
to_image(gard).convert("RGB").save(f"{PRE}/bg-garden.png")
