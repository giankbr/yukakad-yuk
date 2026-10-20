"""Surel — watercolour e-mail header banner: eucalyptus/olive sprigs in both lower corners with blush buds,
transparent so the names can sit on a pale wash in the middle. Also a small sprig for the attachment 'pdf' tile.
Run: python3 -I /tmp/pen/art/themes/surel.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p7 import *  # noqa

OUT = "/root/w/frontend/public/themes/art/surel"
PRE = "/tmp/pen/nt3-P7/sr"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(44)
seed = [700]
def nxt():
    seed[0] += 5
    return seed[0]

W, H = 860, 300
GREENS = [("#b9c6a8", "#8fa37f"), ("#a9bb9a", "#7d9470"), ("#c4ccb0", "#98a886")]
BLUSH = ("#f1c9c4", "#dd9aa0")
BLUSH_D = "#c27a86"

def sprig(art, x0, y0, ang, L, n_leaves, scale=1.0, flip=False):
    """a stem from (x0,y0) heading `ang` with alternating rounded leaves (eucalyptus-ish)."""
    stem = curve([(x0, y0), (x0 + math.cos(ang) * L * .5 + rng.uniform(-10, 10), y0 + math.sin(ang) * L * .5 + rng.uniform(-10, 10)), (x0 + math.cos(ang) * L, y0 + math.sin(ang) * L)], 40)
    art = glaze(art, pigment(stroke_mask(W, H, stem, 4.0 * scale, taper=(.05, .4)), "#6f7f5e", "#56654a", seed=nxt(), density=.75, edge=.3, bloom=0, rough=1.5, feather=.7))
    for k in range(n_leaves):
        t = 0.1 + 0.85 * k / max(1, n_leaves - 1)
        i = int(t * (len(stem) - 2)); px, py = stem[i]
        (ax, ay), (bx, by) = stem[max(0, i - 1)], stem[min(len(stem) - 1, i + 1)]
        d = math.atan2(by - ay, bx - ax)
        side = 1 if (k % 2 == 0) != flip else -1
        la = d + side * rng.uniform(.85, 1.25)
        ll = (46 - 22 * t) * scale * rng.uniform(.85, 1.15); lw = ll * rng.uniform(.5, .66)
        ca, cb = rng.choice(GREENS)
        m = shape_mask(W, H, deform(ellipse_pts(px + math.cos(la) * ll * .55, py + math.sin(la) * ll * .55, ll * .55, lw * .5, 12, la), rng, 2, .05))
        art = glaze(art, pigment(m, ca, cb, seed=nxt(), density=.68, edge=.55, bloom=.4, rough=4, gran=.25, feather=1.2, holes=.05))
    return art

def bud(art, x, y, r):
    m = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * .95, 10), rng, 2, .1))
    art = glaze(art, pigment(m, *BLUSH, seed=nxt(), density=.55, edge=.6, bloom=.5, rough=4, feather=1.1))
    for k in range(3):
        a0 = rng.uniform(0, math.tau)
        art = glaze(art, pigment(stroke_mask(W, H, arc_pts(x, y, r * rng.uniform(.4, .7), a0, a0 + rng.uniform(1.6, 2.6), 16, .9), r * .28), BLUSH_D, seed=nxt(), density=.45, edge=.5, bloom=.2, rough=2, feather=.8))
    return art

art = blank(W, H)
# left corner cluster (stems fan up-right from the bottom-left)
for (ang, L, n, sc) in [(-1.05, 210, 8, 1.0), (-0.5, 240, 9, 1.0), (-1.5, 150, 6, .8), (-0.15, 180, 6, .75), (-0.8, 120, 5, .7)]:
    art = sprig(art, rng.uniform(-10, 30), H + rng.uniform(0, 20), ang, L, n, sc)
for (x, y, r) in [(92, 214, 15), (150, 262, 12), (62, 160, 10)]:
    art = bud(art, x, y, r)
# right corner cluster (mirrored feel, slightly smaller)
for (ang, L, n, sc) in [(-2.1, 200, 8, .95), (-2.65, 230, 9, 1.0), (-1.65, 140, 6, .8), (-3.0, 170, 6, .75), (-2.35, 120, 5, .7)]:
    art = sprig(art, W - rng.uniform(-10, 30), H + rng.uniform(0, 20), ang, L, n, sc, flip=True)
for (x, y, r) in [(W - 100, 226, 14), (W - 150, 266, 11), (W - 66, 170, 9)]:
    art = bud(art, x, y, r)
# a few gold flecks
fl = dots_mask(W, H, [(rng.uniform(40, 260), rng.uniform(120, 290), rng.uniform(1.6, 3.2)) for _ in range(6)] + [(rng.uniform(W - 260, W - 40), rng.uniform(120, 290), rng.uniform(1.6, 3.2)) for _ in range(6)])
art = over(art, foil(fl, "#c9a85a", seed=nxt(), emboss=.3, sparkle=.1))
# soft blush wash across the top (very light), so the banner has a painted ground
wash = shape_mask(W, H, deform([(-30, -30), (W + 30, -30), (W + 30, 90), (W * .72, 150), (W * .5, 120), (W * .25, 160), (-30, 100)], rng, 3, .1))
art = over(scale_alpha(pigment(wash, "#f6e7e2", "#f1dad6", seed=nxt(), density=.4, edge=.3, bloom=.6, rough=16, gran=.2, feather=6, mottle=.8), .7), art)
print("banner", save_full(art, f"{OUT}/banner.webp", quality=82), round(kb(f"{OUT}/banner.webp")))
on_color(art, "#fbf7f2").save(f"{PRE}/banner.png")

# small sprig for the pdf attachment tile (100x100, transparent)
SW = 120
sp = blank(SW, SW)
stem = curve([(28, 104), (52, 70), (84, 24)], 30)
spm = stroke_mask(SW, SW, stem, 2.6, taper=(.05, .4))
sp = glaze(sp, pigment(spm, "#6f7f5e", seed=nxt(), density=.8, edge=.3, bloom=0, rough=1, feather=.6))
for k in range(6):
    t = .15 + .75 * k / 5; i = int(t * 28); px, py = stem[i]
    la = math.atan2(-46, 56) + (1 if k % 2 else -1) * 1.05
    ll = 18 - 7 * t
    m = shape_mask(SW, SW, deform(ellipse_pts(px + math.cos(la) * ll * .5, py + math.sin(la) * ll * .5, ll * .55, ll * .3, 10, la), rng, 2, .05))
    ca, cb = GREENS[k % 3]
    sp = glaze(sp, pigment(m, ca, cb, seed=nxt(), density=.65, edge=.55, bloom=.4, rough=3, feather=1))
print("sprig", save_full(sp, f"{OUT}/sprig.webp", quality=84), round(kb(f"{OUT}/sprig.webp")))
on_color(sp, "#fce8e6").save(f"{PRE}/sprig.png")
