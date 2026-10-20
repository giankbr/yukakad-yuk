"""Dokumen — painted page cover (gouache hills at golden hour, like a wiki page's cover painting).
Run: python3 -I /tmp/pen/art/themes/dokumen.py
"""
import sys, os, math, random
sys.path.insert(0, "/tmp/pen/art/themes")
from _p7 import *  # noqa

OUT = "/root/w/frontend/public/themes/art/dokumen"
PRE = "/tmp/pen/nt3-P7/dk"
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
rng = random.Random(31)
seed = [300]
def nxt():
    seed[0] += 7
    return seed[0]

W, H = 900, 330
sky = painted_sky(W, H, [(0, "#dfe6ea"), (.45, "#ecebe3"), (.8, "#f3e4cf"), (1, "#f1dcc2")], seed=nxt(), streak=.5, grain=.6)
# pale sun, low on the right
sun = circle_mask(W, H, 640, 150, 46)
sky = over(sky, scale_alpha(glow(sun, "#f6dca8", radius=40, strength=.5), .6))
sky = over(sky, pigment(deform_mask := shape_mask(W, H, deform(ellipse_pts(640, 150, 44, 43, 30), rng, 1, .01)), "#f8e6b8", "#f1cf8e", seed=nxt(), density=.9, edge=.3, bloom=.2, rough=2, gran=.2))
# thin cloud streaks
cl = blank(W, H)
for i in range(5):
    y = rng.uniform(40, 150); x0 = rng.uniform(-80, 500); L = rng.uniform(180, 420)
    pts = curve([(x0, y), (x0 + L * .4, y + rng.uniform(-6, 6)), (x0 + L, y + rng.uniform(-6, 4))], 30)
    cl = glaze(cl, pigment(stroke_mask(W, H, pts, rng.uniform(10, 22), taper=(.35, .4)), "#ffffff", "#f3eadb", seed=nxt(), density=.5, edge=.25, bloom=.4, rough=6, feather=2))
sky = over(sky, cl)

# hills: far (hazy sage) → near (deeper olive); every ridge is a deformed curve
def hill(y_base, amp, cols, phase, dens=.95):
    pts = [(x, y_base + amp * math.sin(x / W * math.pi * 1.6 + phase) + amp * .35 * math.sin(x / W * math.pi * 5 + phase * 2)) for x in range(-20, W + 40, 20)]
    poly = [(-20, H + 80)] + pts + [(W + 40, H + 80)]
    m = shape_mask(W, H, deform(poly, rng, 2, .01))
    return gouache_paint(m, *cols, seed=nxt(), rough=2.5, streak=.7, density=dens)
scene = over(sky, hill(222, 24, ("#cfd1b6", "#c3c8a9"), 0.6, .9))
scene = over(scene, hill(252, 20, ("#a3b187", "#96a77c"), 2.3))
scene = over(scene, hill(286, 16, ("#73885c", "#6a7f55"), 4.1))
# sunlit ridge lines: warm pale dabs along the crests on the sun side
lit = blank(W, H)
for (yb, amp, ph) in [(222, 24, 0.6), (252, 20, 2.3), (286, 16, 4.1)]:
    for i in range(10):
        x0 = rng.uniform(80, W - 60); L = rng.uniform(30, 90)
        pts = [(x, yb + amp * math.sin(x / W * math.pi * 1.6 + ph) + amp * .35 * math.sin(x / W * math.pi * 5 + ph * 2) + 2) for x in np.linspace(x0, x0 + L, 6)]
        lit = over(lit, scale_alpha(gouache_paint(stroke_mask(W, H, pts, rng.uniform(3, 6), taper=(.3, .3)), "#e3dcb0", "#d6cf9f", seed=nxt(), rough=1.2), .55))
scene = over(scene, lit)
# a field strip and a path on the nearest hill (lighter brush dabs)
dabs = blank(W, H)
for i in range(40):
    x = rng.uniform(0, W); y = rng.uniform(262, 320)
    L = rng.uniform(16, 50)
    dabs = over(dabs, scale_alpha(gouache_paint(stroke_mask(W, H, [(x, y), (x + L, y + rng.uniform(-2, 2))], rng.uniform(3, 6), taper=(.3, .3)), rng.choice(["#9fae86", "#b3bf98", "#73845e"]), seed=nxt(), rough=1.2), .7))
scene = over(scene, dabs)

# trees: round gouache crowns with a darker side and a short trunk
def tree(x, y, r, light, dark):
    global scene
    trunk = stroke_mask(W, H, [(x, y + r * .4), (x + rng.uniform(-2, 2), y + r * 1.25)], r * .22, taper=(.05, .2))
    scene = over(scene, gouache_paint(trunk, "#6b5a46", seed=nxt(), rough=1))
    crown = shape_mask(W, H, deform(ellipse_pts(x, y, r, r * .92, 12), rng, 2, .08))
    scene = over(scene, gouache_paint(crown, light, dark, seed=nxt(), rough=2.5, streak=.6))
    shade = shape_mask(W, H, deform(ellipse_pts(x + r * .3, y + r * .2, r * .62, r * .55, 10), rng, 2, .1))
    scene = over(scene, scale_alpha(gouache_paint(shade * crown, dark, seed=nxt(), rough=2), .6))
for (x, y, r) in [(120, 262, 24), (165, 252, 17), (770, 282, 26), (830, 270, 15), (470, 246, 12), (505, 250, 9)]:
    tree(x, y, r, rng.choice(["#8fa36e", "#7f9565"]), rng.choice(["#5f7349", "#56683f"]))
# birds
bl = []
for (bx, by, s_) in [(330, 96, .9), (372, 84, .8), (400, 104, .7)]:
    bl.append(([(bx - 10 * s_, by + 3), (bx - 5 * s_, by - 4 * s_), (bx, by + 1)], 2.2 * s_))
    bl.append(([(bx, by + 1), (bx + 5 * s_, by - 4 * s_), (bx + 10 * s_, by + 2)], 2.2 * s_))
scene = over(scene, scale_alpha(ink(strokes_mask(W, H, bl), "#5a5a52", seed=nxt()), .75))
scene[..., 3] = 1
print("cover", save_opaque(scene, f"{OUT}/cover.webp", quality=78), round(kb(f"{OUT}/cover.webp")))
to_image(scene).convert("RGB").save(f"{PRE}/cover.png")

# ---------- page icon: painted ring (replaces the 💍 emoji page icon) ----------
def ring_icon():
    S = 160
    r2 = random.Random(77)
    cx, cy = 80, 98
    band_o = shape_mask(S, S, deform(ellipse_pts(cx, cy, 46, 44, 40), r2, 1, .004))
    band_i = shape_mask(S, S, deform(ellipse_pts(cx, cy + 2, 35, 33, 40), r2, 1, .004))
    band = np.clip(band_o - band_i, 0, 1)
    gem = shape_mask(S, S, [(cx - 24, 40), (cx - 14, 28), (cx + 14, 28), (cx + 24, 40), (cx, 66)], smooth=False)
    table = shape_mask(S, S, [(cx - 14, 28), (cx + 14, 28), (cx + 8, 40), (cx - 8, 40)], smooth=False)
    facet = shape_mask(S, S, [(cx - 24, 40), (cx - 8, 40), (cx, 66)], smooth=False)
    prong = shape_mask(S, S, [(cx - 16, 58), (cx + 16, 58), (cx + 10, 68), (cx - 10, 68)], smooth=False)
    art = blank(S, S)
    art = over(art, foil(np.clip(band + prong, 0, 1), "#c9a14a", seed=nxt(), emboss=0.7, sparkle=0.15))
    art = over(art, pigment(gem, "#bfe3ee", "#8fcbe0", seed=nxt(), density=0.9, edge=0.6, bloom=0.3, gran=0.2, feather=0.6, rough=1.0))
    art = glaze(art, pigment(facet, "#6fb3cf", seed=nxt(), density=0.55, edge=0.4, bloom=0, feather=0.5, rough=0.8))
    art = over(art, pigment(table, "#ffffff", seed=nxt(), density=0.55, edge=0.2, bloom=0, feather=0.5, rough=0.6))
    art = over(art, ink(strokes_mask(S, S, [([(cx - 24, 40), (cx + 24, 40)], 1.2), ([(cx - 8, 40), (cx, 66)], 1.0), ([(cx + 8, 40), (cx, 66)], 1.0)]), "#4f7f93", seed=nxt()))
    print("ring", save_asset(art, f"{OUT}/ring.webp", max_w=120, quality=86), round(kb(f"{OUT}/ring.webp")))
    on_paper(art, "#ffffff").save(f"{PRE}/ring.png")


ring_icon()
