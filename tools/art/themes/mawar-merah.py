"""Mawar Merah — lush deep-red garden roses with dark foliage and buds in rich opaque gouache on warm cream.
Run: python3 -I mawar-merah.py [rose bank spray divider]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q5_lib import *

OUT = outdir("mawar-merah")
PARTS = sys.argv[1:] or ["rose", "bank", "spray", "divider"]
CREAM = "#f6ecdc"
REDS = [("#c8403f", "#8a1520", "#3d0610"), ("#b83440", "#78111e", "#33050e"), ("#d24c46", "#951c22", "#470a12"), ("#a82c36", "#6a0f1a", "#2c040b")]
LEAF = ("#3a4a33", "#1f2a1c")
LEAF_HI = "#6b7d55"


def bud(art, W, H, x, y, s, ang, rng, nx, red):
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 2.0, s * .7, ang, n=12), rng, 1, .05))
    art = GP(art, m, red[1], red[2], seed=nx(), rough=1.0, streak=1.0)
    hl = stroke_mask(W, H, [(x + math.cos(ang) * s * t - math.sin(ang) * s * .18, y + math.sin(ang) * s * t + math.cos(ang) * s * .18) for t in (0.5, 1.0, 1.5)], s * .18) * m
    art = GP(art, hl, red[0], seed=nx(), rough=0.5, dry=0.3, density=0.8)
    for sd in (-1, 1):
        sep = shape_mask(W, H, petal_pts(x, y, s * 1.3, s * .28, ang + sd * .42, n=10))
        art = GP(art, sep, LEAF[0], LEAF[1], seed=nx(), rough=0.6)
    return art


def stem(art, W, H, pts, wdt, nx):
    return GP(art, strokes(W, H, [(curve(pts, 30), wdt, (0.05, 0.4))]), "#2f3b28", "#1b2418", seed=nx(), rough=0.6)


def cluster(W, H, roses, leaves, buds, stems, seed, backdrop=None, top_leaves=()):
    """Dark foliage backdrop, stems and leaves behind, cast shadow, roses (rotated/foreshortened sprites), buds,
    then a few leaves tucked in front."""
    rng = random.Random(seed); nx = Seq(seed * 10)
    art = blank(W, H)
    if backdrop is not None:
        art = GP(art, backdrop, "#1f2b1c", "#121a10", seed=nx(), rough=3.0, streak=1.0)
    for pts, wdt in stems:
        art = stem(art, W, H, pts, wdt, nx)
    for (x, y, L, a) in leaves:
        dark = rng.random() < 0.45
        art = gouache_leaf(art, W, H, x, y, L, a, rng, nx, "#2c3a28" if dark else LEAF[0], "#141c12" if dark else LEAF[1], hi=None if dark else LEAF_HI)
        trim_cache()
    shadow = np.zeros((H, W), np.float32)
    for rs in roses:
        x, y, r = rs[:3]
        shadow = np.maximum(shadow, circles(W, H, [(x + r * .1, y + r * .16, r * 1.02)]))
    art = over(art, tint(gaussian_filter(shadow, 9), "#120604", 0.5))
    for k, rs in enumerate(roses):
        x, y, r = rs[:3]
        ang = rs[3] if len(rs) > 3 else 0.0
        sy = rs[4] if len(rs) > 4 else 1.0
        sp = rose_sprite(r, rng, nx, *REDS[k % len(REDS)], tilt=rng.uniform(.84, .92))
        art = place(art, sp, x, y, ang, sy)
        clear()
    for (x, y, s_, a) in buds:
        art = bud(art, W, H, x, y, s_, a, rng, nx, REDS[rng.randrange(len(REDS))])
    for (x, y, L, a) in top_leaves:
        art = gouache_leaf(art, W, H, x, y, L, a, rng, nx, LEAF[0], LEAF[1], hi=LEAF_HI)
    return art


def blobs(W, H, items):
    return gaussian_filter(circles(W, H, items), 2)


if "rose" in PARTS:
    W = H = 360
    art = cluster(W, H, [(180, 170, 104)], [(150, 230, 150, 2.3), (220, 240, 140, 0.75)], [], [], 51)
    preview(art, "mm-rose", tone=CREAM)
    save(art, f"{OUT}/rose.webp", max_w=200, quality=84)

if "bank" in PARTS:
    W, H = 900, 600
    rng = random.Random(52)
    roses = [(70, 60, 120, -.3, .9), (300, 40, 116, .2, .92), (540, 70, 130, -.1, .95), (790, 50, 124, .35, .9),
             (190, 220, 96, .25, .85), (420, 230, 104, -.35, .88), (660, 220, 98, .15, .86), (870, 250, 80, -.4, .8), (20, 270, 74, .5, .82),
             (300, 370, 66, -.2, .78), (560, 380, 70, .3, .8)]
    leaves = []
    for (x, y, r, *_ ) in roses:
        for k in range(3):
            a = rng.uniform(0.4, 2.7)
            leaves.append((x + math.cos(a) * r * .55, y + math.sin(a) * r * .55, r * rng.uniform(1.0, 1.35), a + rng.uniform(-.3, .3)))
    for x in range(-10, W + 40, 58):
        a = rng.choice([rng.uniform(0.3, 1.0), rng.uniform(1.2, 1.9), rng.uniform(2.1, 2.8)])
        leaves.append((x + rng.uniform(-20, 20), rng.uniform(300, 400), rng.uniform(80, 135), a))
    bd = displace(blobs(W, H, [(x, y, r * 1.1) for (x, y, r, *_) in roses] + [(x + rng.uniform(-20, 20), rng.uniform(250, 330), rng.uniform(60, 100)) for x in range(0, W + 1, 75)]), 7, 18, 40)
    buds = [(150, 500, 22, 1.4), (420, 455, 20, 1.75), (705, 515, 23, 1.45), (850, 430, 19, 1.9), (250, 430, 17, 1.0), (610, 440, 17, 2.1), (40, 440, 18, 1.6)]
    stems = [([(b[0] - math.cos(b[3]) * 120, b[1] - math.sin(b[3]) * 120), (b[0] - math.cos(b[3]) * 60 + 8, b[1] - math.sin(b[3]) * 60), (b[0], b[1])], 4.5) for b in buds]
    top = [(360, 330, 90, 1.9), (480, 320, 84, 1.1), (110, 330, 86, 1.6), (760, 320, 88, 1.3)]
    art = cluster(W, H, roses, leaves, buds, stems, 52, backdrop=bd, top_leaves=top)
    preview(art, "mm-bank", tone=CREAM)
    save(art, f"{OUT}/bank.webp", max_w=780, quality=80)

if "spray" in PARTS:
    W = H = 560
    rng = random.Random(53)
    roses = [(390, 390, 112, -.2, .92), (220, 455, 80, .4, .85), (455, 215, 76, -.5, .85), (120, 520, 52, .2, .8)]
    leaves = [(330, 320, 150, 3.7), (300, 420, 140, 3.0), (400, 280, 130, 4.4), (180, 400, 120, 3.6), (500, 330, 120, 4.9),
              (360, 500, 110, 2.6), (480, 140, 110, 4.6), (250, 300, 100, 4.0), (90, 470, 90, 3.3)]
    bd = None
    buds = [(130, 380, 20, 3.9), (330, 180, 20, 4.3), (60, 430, 16, 3.5), (520, 80, 17, 4.7)]
    stems = [([(250, 430), (130, 380)], 4), ([(410, 260), (330, 180)], 4), ([(180, 470), (60, 430)], 3.5), ([(470, 180), (520, 80)], 3.5)]
    art = cluster(W, H, roses, leaves, buds, stems, 53, backdrop=bd, top_leaves=[(300, 520, 90, 2.9)])
    preview(art, "mm-spray", tone=CREAM)
    save(art, f"{OUT}/spray.webp", max_w=380, quality=82)

if "divider" in PARTS:
    W, H = 760, 150
    rng = random.Random(54)
    vine = [(30, 92), (180, 70), (380, 84), (580, 70), (730, 92)]
    leaves = [(140, 74, 64, -0.6), (230, 74, 60, 0.5), (300, 80, 56, -0.4), (470, 80, 56, -2.7), (540, 74, 60, 2.6), (630, 74, 64, -2.5)]
    buds = [(70, 86, 13, 3.4), (690, 86, 13, -0.2)]
    art = cluster(W, H, [(380, 78, 50, 0.1, .9)], leaves, buds, [(vine, 4)], 54)
    preview(art, "mm-divider", tone=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=440, quality=84)

kb(OUT)
