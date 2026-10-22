"""Aqiqah Domba — soft woolly lambs in dry-brush + watercolour: a standing lamb and a resting lamb (fleece of broken
curl strokes over a soft wash), a green watercolour meadow with small daisies, pastel clouds, a daisy sprig divider and a
single daisy. Run: python3 -I aqiqah-domba.py [part ...]  parts: lamb rest meadow cloud sprig daisy
Assets -> public/themes/art/aqiqah-domba/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b5_lib import *

OUT = outdir("aqiqah-domba")
PARTS = sys.argv[1:] or ["lamb", "rest", "meadow", "cloud", "sprig", "daisy"]
INK = "#5b4a3e"
FACE, FACE_D = "#f1dccb", "#d8b8a2"
EAR_IN = "#f4b9b4"
LEG, LEG_D = "#cdb7a3", "#9e8672"
GREEN, GREEN_D, GREEN_L = "#9fcf8c", "#6aa865", "#c8e6b3"


def face(art, W, H, nx, cx, cy, rx, ry, rot, rng, sleepy=True):
    head = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 14, rot), rng, 1, .02)])
    art = G(art, head, FACE, "#f6e4d6", seed=nx(), density=.92, edge=.35, bloom=.15, gran=.15, rough=2.5, feather=1.2)
    art = tint(art, side_light(head, 8, 10, 6) * 1.4, FACE_D, .55, seed=nx())
    art = crayon(art, inner_edge(head, 1.6), mix(FACE_D, INK, .4), seed=nx(), amt=.5, tooth=.4)
    # closed eyes (gentle arcs) + nose + cheek
    ex = cx - rx * .28
    eyes = strokes(W, H, [(arc_pts(ex, cy - ry * .12, rx * .16, .3, math.pi - .3, 10), 2.6, (.2, .2)),
                          (arc_pts(cx + rx * .3, cy - ry * .14, rx * .15, .3, math.pi - .3, 10), 2.4, (.2, .2))])
    art = crayon(art, eyes, INK, seed=nx(), amt=.85, tooth=.25)
    nose = strokes(W, H, [([(cx - rx * .62, cy + ry * .34), (cx - rx * .52, cy + ry * .44), (cx - rx * .42, cy + ry * .36)], 2.4, (.2, .2))])
    art = crayon(art, nose, "#8c6b5c", seed=nx(), amt=.8, tooth=.25)
    art = G(art, circles(W, H, [(cx - rx * .1, cy + ry * .3, rx * .17)]), "#f4a7a0", seed=nx(), density=.45, edge=.1, bloom=0, rough=1.5, feather=2.5)
    return art, head


def ear(art, W, H, nx, x, y, L, ang, rng):
    m = shapes(W, H, [petal_pts(x, y, L, L * .34, ang, n=12)])
    art = G(art, m, FACE, "#f2d6c6", seed=nx(), density=.9, edge=.35, bloom=.1, rough=2, feather=1)
    inner = shapes(W, H, [petal_pts(x + math.cos(ang) * L * .12, y + math.sin(ang) * L * .12, L * .72, L * .16, ang, n=10)])
    art = G(art, inner, EAR_IN, seed=nx(), density=.7, edge=.2, bloom=0, rough=1.5, feather=1)
    art = crayon(art, inner_edge(m, 1.4), mix(FACE_D, INK, .4), seed=nx(), amt=.45, tooth=.4)
    return art


def legs(art, W, H, nx, items):
    for x, y0, y1, wd in items:
        m = strokes(W, H, [([(x, y0), (x + 1, (y0 + y1) / 2), (x, y1)], wd, None)])
        art = G(art, m, LEG, "#d7c3b0", seed=nx(), density=.92, edge=.3, bloom=0, rough=1.5, feather=.8)
        art = tint(art, side_light(m, -4, 0, 3) * 1.4, LEG_D, .5, seed=nx())
        hoof = ellipses(W, H, [(x, y1 + 2, wd * .58, wd * .4, 0)])
        art = G(art, hoof, "#8c7563", seed=nx(), density=.9, edge=.3, bloom=0, rough=1, feather=.6)
    return art


if "lamb" in PARTS:
    W, H = 560, 460
    nx = Seq(60100); rng = random.Random(3)
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(300, 420, 190, 16, 20)])
    art = G(art, shadow, "#6aa865", seed=nx(), density=.32, edge=.05, bloom=0, rough=3, feather=6)
    art = legs(art, W, H, nx, [(232, 300, 404, 24), (380, 300, 400, 24)])
    body0 = shapes(W, H, [deform(ellipse_pts(310, 250, 150, 98, 18, -.04), rng, 1, .02)])
    body = scallop_mask(W, H, body0, 26, 60110)
    art = legs(art, W, H, nx, [(268, 300, 412, 26), (416, 300, 408, 26)])
    art = wool(art, W, H, body, 60120, curl=12)
    tail = scallop_mask(W, H, circles(W, H, [(462, 222, 22)]), 12, 60130, count=10)
    art = wool(art, W, H, tail, 60140, curl=8)
    art = ear(art, W, H, nx, 196, 150, 56, 2.55, rng)
    art, head = face(art, W, H, nx, 160, 186, 58, 50, -.18, rng)
    tuft = scallop_mask(W, H, shapes(W, H, [deform(ellipse_pts(182, 138, 40, 24, 12, -.2), rng, 1, .03)]), 13, 60150, count=12)
    art = wool(art, W, H, tuft, 60160, curl=8)
    art = ear(art, W, H, nx, 128, 152, 44, 3.3, rng)
    # tiny bow? keep it plain and gentle: a small daisy tucked in the wool
    preview(art, "domba-lamb", tone="#f2f8ec")
    save(art, f"{OUT}/lamb.webp", max_w=340, quality=84)
    clear()

if "rest" in PARTS:
    W, H = 460, 300
    nx = Seq(60200); rng = random.Random(5)
    art = blank(W, H)
    shadow = shapes(W, H, [ellipse_pts(240, 266, 170, 14, 20)])
    art = G(art, shadow, "#6aa865", seed=nx(), density=.3, edge=.05, bloom=0, rough=3, feather=6)
    body0 = shapes(W, H, [deform(ellipse_pts(250, 196, 150, 70, 18, 0), rng, 1, .02)])
    body = scallop_mask(W, H, body0, 22, 60210)
    art = wool(art, W, H, body, 60220, curl=11)
    # tucked front legs
    art = G(art, ellipses(W, H, [(176, 258, 12, 7, 0), (214, 262, 12, 7, 0)]), "#8c7563", seed=nx(), density=.9, edge=.3, bloom=0, rough=1, feather=.6)
    art = ear(art, W, H, nx, 140, 150, 46, 2.7, rng)
    art, head = face(art, W, H, nx, 112, 178, 50, 42, -.05, rng)
    tuft = scallop_mask(W, H, shapes(W, H, [deform(ellipse_pts(128, 134, 34, 20, 12, -.1), rng, 1, .03)]), 11, 60230, count=11)
    art = wool(art, W, H, tuft, 60240, curl=7)
    art = ear(art, W, H, nx, 82, 148, 38, 3.4, rng)
    preview(art, "domba-rest", tone="#f2f8ec")
    save(art, f"{OUT}/rest.webp", max_w=260, quality=84)
    clear()


def daisy(art, W, H, nx, x, y, r, rng, col="#ffffff", heart="#f6c85a"):
    pet = [petal_pts(x, y, r, r * .3, a + rng.uniform(-.1, .1), n=10) for a in np.linspace(0, math.tau, 10)[:-1]]
    m = shapes(W, H, pet)
    art = G(art, m, col, "#fbf6ee", seed=nx(), density=.95, edge=.35, bloom=0, gran=.1, rough=1.2, feather=.6)
    art = tint(art, side_light(m, 2, 3, 2) * 1.2, "#d9d2e6", .5, seed=nx())
    art = G(art, circles(W, H, [(x, y, r * .3)]), heart, "#eeb24a", seed=nx(), density=.95, edge=.4, bloom=0, rough=1, feather=.5)
    return art


if "meadow" in PARTS:
    W, H = 800, 300
    nx = Seq(60300); rng = random.Random(7)
    art = blank(W, H)
    back = shapes(W, H, [[(x, 90 + 30 * math.sin(x / 150 + .6)) for x in range(-10, W + 11, 20)] + [(W + 10, H + 10), (-10, H + 10)]])
    art = G(art, back, GREEN_L, "#b6ddb0", seed=nx(), density=.75, edge=.5, bloom=.4, gran=.25, rough=6, feather=1.4)
    front = shapes(W, H, [[(x, 150 + 26 * math.sin(x / 120 + 2.2)) for x in range(-10, W + 11, 20)] + [(W + 10, H + 10), (-10, H + 10)]])
    art = G(art, front, GREEN, "#8cc27a", seed=nx(), density=.85, edge=.55, bloom=.35, gran=.25, rough=6, feather=1.4)
    art = G(art, front * np.clip((np.mgrid[0:H, 0:W][0] - 200) / 100, 0, 1), GREEN_D, seed=nx(), density=.5, edge=.1, bloom=.3, rough=5, feather=2)
    # grass flicks
    flicks = []
    for _ in range(70):
        x = rng.uniform(0, W)
        y0 = 150 + 26 * math.sin(x / 120 + 2.2) + rng.uniform(4, 130)
        h = rng.uniform(8, 18)
        flicks.append(([(x, y0), (x + rng.uniform(-4, 4), y0 - h)], rng.uniform(1.5, 2.6), (0, .8)))
    m = strokes(W, H, flicks) * front
    art = G(art, m, GREEN_D, "#5b9a58", seed=nx(), density=.45, edge=.2, bloom=0, rough=1, feather=.5)
    for _ in range(16):
        x = rng.uniform(20, W - 20)
        y = 150 + 26 * math.sin(x / 120 + 2.2) + rng.uniform(26, 120)
        art = daisy(art, W, H, nx, x, y, rng.uniform(6, 9), rng, heart=rng.choice(["#f6c85a", "#f6c85a", "#f4a7a0"]))
    preview(art, "domba-meadow", tone="#eaf5fb")
    save(art, f"{OUT}/meadow.webp", max_w=640, quality=80)
    clear()

if "cloud" in PARTS:
    W, H = 360, 200
    for k, (ca, cb) in enumerate((("#fbe3ea", "#f6d3e0"), ("#e3e6fb", "#d6dcf6"))):
        nx = Seq(60400 + k * 40); rng = random.Random(9 + k)
        art = blank(W, H)
        base = shapes(W, H, [deform(ellipse_pts(180, 118, 140, 40, 16), rng, 1, .02)])
        puff = np.clip(base + circles(W, H, [(120, 98, 46), (196, 78, 60), (262, 104, 40)]), 0, 1)
        art = G(art, puff, ca, cb, seed=nx(), density=.8, edge=.55, bloom=.5, gran=.15, rough=7, feather=2)
        art = G(art, puff * np.clip((np.mgrid[0:H, 0:W][0] - 100) / 60, 0, 1), cb, seed=nx(), density=.5, edge=.1, bloom=.3, rough=5, feather=3)
        preview(art, f"domba-cloud{k}", tone="#eaf5fb")
        save(art, f"{OUT}/cloud-{k}.webp", max_w=220, quality=82)
        clear()

if "sprig" in PARTS:
    W, H = 520, 110
    nx = Seq(60500); rng = random.Random(11)
    art = blank(W, H)
    stem = strokes(W, H, [(curve([(40, 70), (160, 58), (260, 64), (360, 56), (480, 66)], 40), 3, (.1, .1))])
    art = G(art, stem, GREEN_D, seed=nx(), density=.85, edge=.3, bloom=0, rough=1, feather=.5)
    lv = [petal_pts(x, y, 30, 9, a, n=12, cup=.3) for x, y, a in ((120, 62, -2.6), (200, 60, -.5), (320, 60, -2.7), (400, 58, -.4), (90, 66, .5), (430, 62, 2.8))]
    art = G(art, shapes(W, H, lv), GREEN, GREEN_D, seed=nx(), density=.85, edge=.5, bloom=.2, rough=2, feather=.8)
    for x, y, r in ((260, 54, 20), (160, 54, 13), (360, 50, 13)):
        art = daisy(art, W, H, nx, x, y, r, rng)
    preview(art, "domba-sprig", tone="#f2f8ec")
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=84)
    clear()

if "daisy" in PARTS:
    W, H = 120, 120
    nx = Seq(60600); rng = random.Random(13)
    art = blank(W, H)
    art = daisy(art, W, H, nx, 60, 60, 46, rng)
    preview(art, "domba-daisy", tone="#f2f8ec")
    save(art, f"{OUT}/daisy.webp", max_w=72, quality=86)
    clear()
