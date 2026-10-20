"""Dompet Digital — painted accents: gouache confetti + foil coins around the 'Transfer Berhasil' check (cover),
and a gouache gift box with coins for the Kirim Kado card. Run: python3 -I /tmp/pen/art/themes/dompet-digital.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p7 import *  # noqa

OUT = "/root/w/frontend/public/themes/art/dompet-digital"
PRE = "/tmp/pen/nt3-P7/dd"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(58)
seed = [2100]
def nxt():
    seed[0] += 9
    return seed[0]

def coin(art, W, H, cx, cy, r, heart=True):
    """gold foil coin with an embossed rim and a small heart stamped in the middle."""
    disc = circle_mask(W, H, cx, cy, r)
    art = over(art, scale_alpha(glow(disc, "#1b4f86", radius=6, strength=.4), .5))  # soft drop shadow
    art = over(art, foil(disc, "#d6a848", seed=nxt(), emboss=.8, sparkle=.15))
    rim = np.clip(circle_mask(W, H, cx, cy, r * .82) - circle_mask(W, H, cx, cy, r * .72), 0, 1)
    art = over(art, scale_alpha(foil(rim, "#9c7424", seed=nxt(), emboss=.3, sparkle=0), .7))
    if heart:
        s_ = r * .34
        pts = []
        for i in range(40):
            t = i / 40 * math.tau
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((cx + x * s_ / 16, cy + 1 + y * s_ / 16))
        art = over(art, scale_alpha(foil(shape_mask(W, H, pts), "#8d6a22", seed=nxt(), emboss=.3, sparkle=0), .85))
    return art

# ---------- cover confetti (transparent, 780x420, the check circle sits at ~ (390, 150))
W, H = 780, 420
art = blank(W, H)
CONF = ["#ffffff", "#ffffff", "#b9e0ff", "#ffd36b", "#ffd36b", "#8fd3c6", "#ffb3c1"]
def avoid(x, y):
    return math.hypot(x - 390, y - 150) < 120 or (abs(x - 390) < 190 and 230 < y < 330)
for _ in range(70):
    x, y = rng.uniform(20, W - 20), rng.uniform(16, H - 30)
    if avoid(x, y):
        continue
    kind = rng.random()
    col = rng.choice(CONF)
    ang = rng.uniform(0, math.pi)
    if kind < .5:  # rectangle flake
        w_, h_ = rng.uniform(12, 24), rng.uniform(6, 11)
        c_, s_ = math.cos(ang), math.sin(ang)
        quad = [(x + c_ * w_ / 2 - s_ * h_ / 2, y + s_ * w_ / 2 + c_ * h_ / 2), (x + c_ * w_ / 2 + s_ * h_ / 2, y + s_ * w_ / 2 - c_ * h_ / 2),
                (x - c_ * w_ / 2 + s_ * h_ / 2, y - s_ * w_ / 2 - c_ * h_ / 2), (x - c_ * w_ / 2 - s_ * h_ / 2, y - s_ * w_ / 2 + c_ * h_ / 2)]
        m = shape_mask(W, H, deform(quad, rng, 1, .03), smooth=False)
    elif kind < .75:  # dot
        m = circle_mask(W, H, x, y, rng.uniform(3.5, 7))
    else:  # curly ribbon
        L = rng.uniform(30, 60)
        pts = [(x + math.cos(ang) * L * t + math.cos(t * 9) * 6, y + math.sin(ang) * L * t + math.sin(t * 9) * 6) for t in np.linspace(-.5, .5, 16)]
        m = stroke_mask(W, H, pts, rng.uniform(3, 5), taper=(.2, .2))
    art = over(art, scale_alpha(gouache_paint(m, col, mix(col, "#7fb6ea", .15), seed=nxt(), rough=1.2, streak=.6), rng.uniform(.75, .95)))
for (cx, cy, r) in [(118, 150, 30), (662, 120, 26), (250, 60, 20), (560, 250, 22), (690, 300, 17), (80, 290, 18)]:
    art = coin(art, W, H, cx, cy, r, heart=r >= 20)
print("confetti", save_full(art, f"{OUT}/confetti.webp", quality=82), round(kb(f"{OUT}/confetti.webp")))
on_color(art, "#0e7ad8").save(f"{PRE}/confetti.png")

# ---------- gift box with coins (transparent, 240x200 → shown ~ 96x80 css)
W, H = 240, 200
g = blank(W, H)
# coins behind the box
for (cx, cy, r) in [(186, 150, 24), (206, 124, 18), (52, 158, 20)]:
    g = coin(g, W, H, cx, cy, r, heart=r >= 20)
# box body with lid (light blue gouache), ribbon in deep blue, bow on top
body = shape_mask(W, H, deform(rrect_pts(70, 96, 104, 86, 5, 3), rng, 2, .015))
g = over(g, gouache_paint(body, "#bfe0ff", "#a9d2f7", seed=nxt(), rough=1.8, streak=.7))
shade = shape_mask(W, H, deform([(70, 96), (120, 96), (120, 182), (70, 182)], rng, 1, .02)) * body
g = over(g, scale_alpha(gouache_paint(shade, "#8fc2f0", seed=nxt(), rough=1.5), .45))
lid = shape_mask(W, H, deform(rrect_pts(60, 74, 124, 30, 5, 3), rng, 2, .015))
g = over(g, gouache_paint(lid, "#d4ebff", "#bfe0ff", seed=nxt(), rough=1.8, streak=.6))
ribbon = np.maximum(shape_mask(W, H, deform([(113, 74), (131, 74), (131, 182), (113, 182)], rng, 1, .02)),
                    shape_mask(W, H, deform([(70, 128), (174, 128), (174, 146), (70, 146)], rng, 1, .02)) * body)
g = over(g, gouache_paint(ribbon, "#1c7fd9", "#0f66b8", seed=nxt(), rough=1.4, streak=.6))
# bow: two loops + knot + tails
for (dx, flip) in [(-26, -1), (26, 1)]:
    loop = shape_mask(W, H, deform(ellipse_pts(122 + dx, 60, 24, 14, 14, flip * .35), rng, 2, .08))
    g = over(g, gouache_paint(loop, "#1c7fd9", "#146fc4", seed=nxt(), rough=1.6, streak=.5))
    inner = shape_mask(W, H, deform(ellipse_pts(122 + dx * .9, 61, 12, 6, 10, flip * .35), rng, 1, .1))
    g = over(g, scale_alpha(gouache_paint(inner, "#0d5aa6", seed=nxt(), rough=1), .6))
    tail = shape_mask(W, H, deform([(122 + dx * .2, 70), (122 + dx * .8, 70), (122 + dx * 1.3, 94), (122 + dx * .5, 90)], rng, 1, .04))
    g = over(g, gouache_paint(tail, "#146fc4", seed=nxt(), rough=1.2))
knot = shape_mask(W, H, deform(ellipse_pts(122, 66, 9, 8, 10), rng, 1, .06))
g = over(g, gouache_paint(knot, "#0f66b8", seed=nxt(), rough=1))
# a heart tag on the box front
pts = []
for i in range(40):
    t = i / 40 * math.tau
    x = 16 * math.sin(t) ** 3; y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    pts.append((96 + x * .7, 162 + y * .7))
g = over(g, gouache_paint(shape_mask(W, H, pts), "#ff8da3", "#f06f8a", seed=nxt(), rough=1))
# soft ground shadow
g = over(scale_alpha(glow(shape_mask(W, H, ellipse_pts(122, 186, 80, 8, 12)), "#2b5f93", radius=5, strength=.5), .35), g)
print("gift", save_asset(g, f"{OUT}/gift.webp", quality=84), round(kb(f"{OUT}/gift.webp")))
on_color(g, "#ffffff").save(f"{PRE}/gift.png")
