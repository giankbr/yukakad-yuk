"""Ultah Samudra — kids' under-the-sea birthday in chunky gouache with a crayon contour (original designs): a round
yellow submarine with brass portholes and a red propeller, a friendly coral octopus, a clown-striped fish and a spotted
teal fish, a bubble, a tall kelp frond, a seabed strip (sand, round sponge corals, seaweed, starfish, shells, little
treasure chest) and a starfish-and-shell divider.
Run: python3 -I ultah-samudra.py [part ...]  parts: sub octopus fish fish2 bubble kelp seabed divider
Assets -> public/themes/art/ultah-samudra/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e6_lib import *

OUT = outdir("ultah-samudra")
PARTS = sys.argv[1:] or ["sub", "octopus", "fish", "fish2", "bubble", "kelp", "seabed", "divider"]
NAVY = "#1f3550"
YEL, YEL2 = "#f8c93c", "#ffe07a"
RED, RED2 = "#e8573f", "#f27a5a"
BRASS = "#d8973a"
GLASS, GLASS2 = "#2a7d92", "#64c3cf"
CORAL, CORAL2 = "#f2836b", "#f9a58b"
SEAW, SEAW2 = "#3f9d6a", "#7cc47a"
SAND, SAND2 = "#f1d79b", "#e6c27a"


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rrect(x0, y0, x1, y1, r):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -math.pi / 2), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, math.pi / 2), (x0 + r, y0 + r, math.pi)):
        pts += arc_pts(cx, cy, r, a0, a0 + math.pi / 2, 6)
    return pts


def porthole(art, W, H, x, y, r, nx):
    ring = circles(W, H, [(x, y, r)])
    art = toon(art, ring, BRASS, "#f0b85a", nx, k=6, line=NAVY)
    glass = circles(W, H, [(x, y, r * 0.72)])
    art = toon(art, glass, GLASS, GLASS2, nx, shade=(1, 1), k=8, hi=False, line=NAVY, line_w=1.8)
    gl = strokes(W, H, [(arc_pts(x, y, r * 0.48, math.pi * 1.05, math.pi * 1.5, 8), r * 0.16, (0.3, 0.3))])
    art = G(art, gl, "#ffffff", seed=nx(), density=0.9, edge=0, bloom=0, rough=0.3, pad=6)
    riv = circles(W, H, [(x + math.cos(a) * r * 0.86, y + math.sin(a) * r * 0.86, 2.6) for a in np.linspace(0, math.tau, 8, endpoint=False)])
    return G(art, riv, "#8a5a1e", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3, pad=4)


def tentacle(W, H, x0, y0, pts_rel, width):
    pts = curve([(x0 + dx, y0 + dy) for dx, dy in pts_rel], 40)
    n = len(pts); L = []; R = []
    for i in range(n):
        t = i / (n - 1)
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        wd = width * (1 - t * 0.85)
        L.append((pts[i][0] - dy / d * wd, pts[i][1] + dx / d * wd)); R.append((pts[i][0] + dy / d * wd, pts[i][1] - dx / d * wd))
    return L + R[::-1], pts


if "sub" in PARTS:
    W, H = 700, 460
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    # tail fins (behind body)
    fin_t = shapes(W, H, [[(150, 220), (92, 150), (70, 160), (100, 236)]])
    fin_b = shapes(W, H, [[(150, 320), (92, 392), (70, 382), (100, 306)]])
    for f in (fin_t, fin_b):
        art = toon(art, f, RED, RED2, nx, k=8, line=NAVY)
    # propeller
    hub = circles(W, H, [(70, 271, 16)])
    blades = shapes(W, H, [ellipse_pts(70, 271 - 44, 13, 34, 10), ellipse_pts(70, 271 + 44, 13, 34, 10)])
    art = toon(art, blades, "#f6a03a", "#ffc25e", nx, k=6, line=NAVY)
    art = toon(art, hub, "#9aa7b8", "#c9d3df", nx, k=5, line=NAVY)
    # periscope behind tower
    peri = strokes(W, H, [([(392, 130), (392, 52), (436, 52)], 16, None)], cap=False)
    art = toon(art, peri, "#9aa7b8", "#c9d3df", nx, k=5, line=NAVY)
    lens = shapes(W, H, [rect(430, 40, 452, 64)], smooth=False)
    art = toon(art, lens, GLASS, GLASS2, nx, k=4, hi=False, line=NAVY, line_w=1.6)
    # conning tower
    tower = shapes(W, H, [rrect(270, 116, 420, 200, 26)], smooth=False)
    art = toon(art, tower, YEL, YEL2, nx, k=12, line=NAVY)
    # hull
    body = shapes(W, H, [ellipse_pts(355, 272, 250, 104, 40)])
    art = toon(art, body, YEL, YEL2, nx, k=26, sh_col="#c0702a", line=NAVY, line_w=3.0)
    # red belly stripe
    band = shapes(W, H, [[(120, 300), (590, 300), (600, 324), (110, 324)]], smooth=False) * body
    art = GP(art, band, RED, RED2, seed=nx(), rough=1, streak=0.6)
    art = G(art, contour(band, 1.8, nx()), NAVY, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.3)
    # seams + rivets
    seam = strokes(W, H, [(curve([(250, 182), (240, 272), (252, 362)], 20), 2.2, None), (curve([(470, 184), (482, 272), (470, 360)], 20), 2.2, None)])
    art = G(art, seam * body, "#b0782a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    riv = []
    for sx, sgn in ((250, -1), (470, 1)):
        for yy in np.linspace(200, 350, 7):
            riv.append((sx + sgn * 10 * math.sin((yy - 272) / 120) * -1 + sgn * 9, yy, 3.2))
    art = G(art, circles(W, H, riv) * body, "#b0782a", seed=nx(), density=0.75, edge=0, bloom=0, rough=0.3)
    for x in (300, 400):
        art = porthole(art, W, H, x, 254, 36, nx)
    art = porthole(art, W, H, 530, 256, 30, nx)
    # tower window + little flag pole with star
    art = porthole(art, W, H, 345, 158, 20, nx)
    pole = strokes(W, H, [([(300, 118), (300, 64)], 4, None)])
    art = G(art, pole, NAVY, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4)
    flag = shapes(W, H, [[(302, 64), (346, 74), (302, 90)]])
    art = toon(art, flag, RED, RED2, nx, k=4, hi=False, line=NAVY, line_w=1.6)
    # headlight
    hl = circles(W, H, [(598, 262, 13)])
    art = OV(art, hl, lambda m: glow(m, "#fff3b0", 8, 0.7))
    art = toon(art, hl, "#fff3b0", "#ffffff", nx, k=4, hi=False, line=NAVY, line_w=1.6)
    preview(art, "sam-sub", tone="#bfe6ee")
    save(art, f"{OUT}/sub.webp", max_w=560, quality=82)
    clear()

if "octopus" in PARTS:
    W, H = 560, 560
    nx = Seq(400); rng = random.Random(4)
    art = blank(W, H)
    cx, cy = 280, 200
    tents = [
        (232, 290, [(0, 0), (-60, 60), (-150, 70), (-200, 20), (-170, -30), (-130, -6)], 30),
        (262, 300, [(0, 0), (-20, 90), (-80, 170), (-140, 190), (-150, 150)], 30),
        (300, 300, [(0, 0), (16, 100), (0, 190), (40, 236), (80, 214)], 30),
        (330, 290, [(0, 0), (70, 70), (150, 100), (196, 70), (176, 30), (146, 50)], 30),
        (250, 290, [(0, 0), (-40, 110), (-24, 200), (12, 214)], 26),
        (318, 296, [(0, 0), (60, 130), (130, 170), (150, 140)], 26),
    ]
    order = [4, 5, 0, 1, 2, 3]
    for i in order:
        x0, y0, rel, wd = tents[i]
        poly, cl = tentacle(W, H, x0, y0, rel, wd)
        m = shapes(W, H, [poly])
        dark = i in (4, 5)
        art = toon(art, m, mix(CORAL, "#b8455a", 0.25) if dark else CORAL, CORAL2, nx, k=10, line=NAVY)
        # suckers along the inner side
        suck = []
        for j in range(6, len(cl) - 6, 5):
            t = j / len(cl)
            a, b = cl[j - 1], cl[j + 1]
            dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
            off = wd * (1 - t * 0.85) * 0.45
            suck.append((cl[j][0] + dy / d * off, cl[j][1] - dx / d * off, max(2.5, wd * 0.24 * (1 - t * 0.8))))
        sm = circles(W, H, suck) * m
        art = G(art, sm, "#ffd9c8", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5)
        clear()
    head = shapes(W, H, [deform(ellipse_pts(cx, cy, 128, 138, 16), rng, 1, 0.04)])
    art = toon(art, head, CORAL, CORAL2, nx, k=30, sh_col="#a8405a", line=NAVY, line_w=3.0)
    spots = circles(W, H, [(220, 120, 12), (334, 104, 9), (356, 150, 7), (196, 168, 7), (300, 76, 6)])
    art = G(art, spots, "#e0606a", seed=nx(), density=0.55, edge=0.4, bloom=0, rough=0.6)
    for ex in (236, 324):
        eye = circles(W, H, [(ex, 214, 32)])
        art = toon(art, eye, "#ffffff", "#f2f4f6", nx, shade=(1, 1), k=6, hi=False, line=NAVY)
        pup = circles(W, H, [(ex + 6, 222, 18)])
        art = GP(art, pup, NAVY, "#2b4a6e", seed=nx(), rough=0.6)
        art = G(art, circles(W, H, [(ex + 12, 214, 6), (ex, 230, 3)]), "#ffffff", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2)
    cheeks = ellipses(W, H, [(198, 262, 22, 13, 0), (362, 262, 22, 13, 0)])
    art = G(art, cheeks, "#e9506e", seed=nx(), density=0.45, edge=0.2, bloom=0.2, rough=1.5)
    smile = strokes(W, H, [(curve([(258, 266), (280, 284), (302, 266)], 16), 4.5, (0.2, 0.2))])
    art = G(art, smile, NAVY, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4)
    # little party hat
    hat = shapes(W, H, [[(244, 82), (290, -2 + 10), (318, 76)]])
    art = toon(art, hat, "#5ab0e8", "#8fd0f4", nx, k=6, line=NAVY)
    dots = circles(W, H, [(278, 52, 5), (292, 30, 4), (300, 62, 4), (268, 70, 4)]) * hat
    art = G(art, dots, YEL, seed=nx(), density=0.9, edge=0, bloom=0, rough=0.3)
    pom = circles(W, H, [(290, 10, 11)])
    art = toon(art, pom, YEL, YEL2, nx, k=4, hi=False, line=NAVY, line_w=1.6)
    preview(art, "sam-octopus", tone="#bfe6ee")
    save(art, f"{OUT}/octopus.webp", max_w=420, quality=82)
    clear()

if "fish" in PARTS:
    W, H = 300, 200
    nx = Seq(700); rng = random.Random(7)
    art = blank(W, H)
    tail = shapes(W, H, [[(70, 100), (20, 52), (34, 100), (20, 150)]])
    art = toon(art, tail, "#f58b2e", "#ffad55", nx, k=5, line=NAVY)
    fin = shapes(W, H, [[(120, 56), (160, 30), (200, 58)]])
    art = toon(art, fin, "#f58b2e", "#ffad55", nx, k=4, hi=False, line=NAVY, line_w=1.8)
    body = shapes(W, H, [ellipse_pts(160, 102, 98, 56, 24)])
    art = toon(art, body, "#f58b2e", "#ffa04a", nx, k=14, line=NAVY)
    for x0, wd in ((118, 20), (178, 22)):
        st = shapes(W, H, [[(x0, 40), (x0 + wd, 42), (x0 + wd + 8, 102), (x0 + wd, 162), (x0, 160), (x0 + 8, 102)]]) * body
        art = GP(art, st, "#ffffff", "#f6f1ea", seed=nx(), rough=0.8)
        art = G(art, contour(st, 1.6, nx()), NAVY, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.3)
    eye = circles(W, H, [(222, 92, 12)])
    art = toon(art, eye, "#ffffff", None, nx, shade=None, hi=False, line=NAVY, line_w=1.6)
    art = GP(art, circles(W, H, [(225, 94, 6.5)]), NAVY, seed=nx(), rough=0.4)
    art = G(art, circles(W, H, [(227, 91, 2.2)]), "#ffffff", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2)
    smile = strokes(W, H, [(curve([(236, 118), (246, 124), (254, 116)], 8), 2.6, (0.2, 0.2))])
    art = G(art, smile, NAVY, seed=nx(), density=0.8, edge=0, bloom=0, rough=0.3)
    pf = shapes(W, H, [[(150, 120), (176, 150), (190, 128)]])
    art = toon(art, pf, "#ffad55", None, nx, k=3, hi=False, line=NAVY, line_w=1.5)
    preview(art, "sam-fish", tone="#bfe6ee")
    save(art, f"{OUT}/fish.webp", max_w=150, quality=84)

if "fish2" in PARTS:
    W, H = 280, 220
    nx = Seq(900); rng = random.Random(9)
    art = blank(W, H)
    tail = shapes(W, H, [[(64, 110), (16, 66), (30, 110), (16, 156)]])
    art = toon(art, tail, "#f8c93c", "#ffe07a", nx, k=5, line=NAVY)
    fins = shapes(W, H, [[(110, 60), (150, 22), (196, 64)], [(110, 160), (150, 196), (190, 158)]])
    art = toon(art, fins, "#f8c93c", "#ffe07a", nx, k=4, hi=False, line=NAVY, line_w=1.8)
    body = shapes(W, H, [ellipse_pts(150, 110, 92, 66, 24)])
    art = toon(art, body, "#3aa8c8", "#6fd0de", nx, k=16, line=NAVY)
    spots = circles(W, H, [(110, 90, 7), (132, 128, 6), (100, 130, 5), (150, 80, 5), (170, 140, 6), (126, 104, 4)]) * body
    art = G(art, spots, "#e9f7fb", seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.5)
    eye = circles(W, H, [(200, 98, 13)])
    art = toon(art, eye, "#ffffff", None, nx, shade=None, hi=False, line=NAVY, line_w=1.6)
    art = GP(art, circles(W, H, [(203, 100, 7)]), NAVY, seed=nx(), rough=0.4)
    art = G(art, circles(W, H, [(206, 97, 2.4)]), "#ffffff", seed=nx(), density=0.95, edge=0, bloom=0, rough=0.2)
    mouth = circles(W, H, [(238, 120, 6)])
    art = GP(art, mouth, "#e96a7a", seed=nx(), rough=0.4)
    preview(art, "sam-fish2", tone="#bfe6ee")
    save(art, f"{OUT}/fish2.webp", max_w=140, quality=84)

if "bubble" in PARTS:
    W, H = 140, 140
    nx = Seq(1100)
    art = blank(W, H)
    art = bubble(art, W, H, 70, 70, 56, nx, rim="#ffffff", tint="#bff0f6", dens=0.75)
    preview(art, "sam-bubble", bg="#2f8aa6")
    save(art, f"{OUT}/bubble.webp", max_w=72, quality=84)

if "kelp" in PARTS:
    W, H = 240, 620
    nx = Seq(1300); rng = random.Random(13)
    art = blank(W, H)
    for k, (x0, lean, col, col2) in enumerate(((76, 26, SEAW, SEAW2), (168, -22, "#2f8a6a", "#5fb78a"))):
        pts = curve([(x0, 620), (x0 + lean * 0.4, 470), (x0 - lean * 0.3, 320), (x0 + lean, 170), (x0 + lean * 0.5, 30 + k * 60)], 60)
        stem = blade(W, H, pts, 26 - k * 4)
        m = shapes(W, H, [stem])
        art = toon(art, m, col, col2, nx, k=8, line=NAVY, line_w=2.0, line_a=0.6)
        bl = []
        for j in range(8, len(pts) - 4, 9):
            px, py = pts[j]
            for sgn in (-1, 1):
                if rng.random() < 0.75:
                    bl.append(ellipse_pts(px + sgn * 15, py - 6, 13, 6, 8, sgn * 0.6))
        bm = shapes(W, H, bl)
        art = toon(art, bm, col2, mix(col2, "#ffffff", 0.2), nx, k=4, hi=False, line=NAVY, line_w=1.5, line_a=0.5)
        clear()
    preview(art, "sam-kelp", tone="#bfe6ee")
    save(art, f"{OUT}/kelp.webp", max_w=120, quality=82)

if "seabed" in PARTS:
    W, H = 1040, 340
    nx = Seq(1500); rng = random.Random(15)
    art = blank(W, H)
    # seaweed behind
    for x0 in (60, 140, 420, 640, 900, 980):
        h = rng.uniform(150, 230)
        pts = curve([(x0, 340), (x0 + rng.uniform(-20, 20), 340 - h * 0.5), (x0 + rng.uniform(-30, 30), 340 - h)], 30)
        m = shapes(W, H, [blade(W, H, pts, 16)])
        art = toon(art, m, SEAW, SEAW2, nx, k=6, line=NAVY, line_w=1.8, line_a=0.55)
    clear()
    # round sponge corals
    for x, y, r, col in ((210, 230, 52, "#f07a9a"), (262, 250, 36, "#ff9fb4"), (770, 222, 58, "#9b7fe0"), (826, 250, 34, "#c0a8f2")):
        m = shapes(W, H, [deform(ellipse_pts(x, y, r, r * 0.95, 14), rng, 2, 0.06)])
        art = toon(art, m, col, mix(col, "#ffffff", 0.25), nx, k=10, line=NAVY, line_w=2.0)
        holes = circles(W, H, [(x + rng.uniform(-r, r) * 0.6, y + rng.uniform(-r, r) * 0.6, rng.uniform(3, 6)) for _ in range(9)]) * m
        art = G(art, holes, mix(col, "#3a2a5a", 0.45), seed=nx(), density=0.7, edge=0.3, bloom=0, rough=0.4)
    clear()
    # sand
    top = [(-20, 280)] + [(x, 268 + 14 * math.sin(x / 90) + rng.uniform(-4, 4)) for x in range(60, 1040, 60)] + [(1060, 276), (1060, 380), (-20, 380)]
    sand = shapes(W, H, [top])
    art = toon(art, sand, SAND, "#f7e3b0", nx, shade=(0, -1), k=18, sh_col="#c9a058", hi=False, line=NAVY, line_w=2.0, line_a=0.5)
    specks = circles(W, H, [(rng.uniform(0, W), rng.uniform(290, 336), rng.uniform(1.2, 2.6)) for _ in range(140)]) * sand
    art = G(art, specks, "#c9a058", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    clear()
    # treasure chest
    chest = shapes(W, H, [rrect(560, 226, 660, 290, 8)], smooth=False)
    lid = shapes(W, H, [[(556, 230), (556, 206)] + arc_pts(610, 210, 54, math.pi, math.tau, 12)[1:-1] + [(664, 206), (664, 230)]])
    art = toon(art, lid, "#b06a3a", "#c98654", nx, k=8, line=NAVY)
    art = toon(art, chest, "#a45f32", "#c07a48", nx, k=8, line=NAVY)
    straps = shapes(W, H, [rect(580, 196, 592, 290), rect(628, 196, 640, 290)], smooth=False) * np.maximum(chest, lid)
    art = GP(art, straps, BRASS, "#f0b85a", seed=nx(), rough=0.6)
    lock = shapes(W, H, [rrect(600, 222, 620, 244, 4)], smooth=False)
    art = toon(art, lock, "#f0c24a", None, nx, k=3, hi=False, line=NAVY, line_w=1.5)
    coins = circles(W, H, [(548, 290, 9), (566, 296, 8), (672, 292, 9)])
    art = toon(art, coins, "#f6c94a", "#ffe07a", nx, k=3, hi=False, line=NAVY, line_w=1.4)
    # starfish + shells
    def star(cx, cy, r, rot, col):
        pts = []
        for i in range(10):
            a = rot + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        return shapes(W, H, [pts])
    for cx, cy, r, rot, col in ((120, 300, 30, -0.3, "#f6873a"), (470, 304, 24, 0.2, "#f2b23a"), (930, 300, 28, 0.5, "#ef6f5a")):
        m = star(cx, cy, r, rot, col)
        art = toon(art, m, col, mix(col, "#ffffff", 0.3), nx, k=5, line=NAVY, line_w=1.8)
        art = G(art, circles(W, H, [(cx + rng.uniform(-r, r) * 0.5, cy + rng.uniform(-r, r) * 0.5, 2) for _ in range(8)]) * m, "#ffe1b8", seed=nx(), density=0.8, edge=0, bloom=0, rough=0.2)
    for cx, cy in ((330, 302), (720, 306)):
        fan = shapes(W, H, [[(cx - 26, cy - 4)] + arc_pts(cx, cy + 6, 28, math.pi * 1.05, math.pi * 1.95, 10) + [(cx + 26, cy - 4), (cx + 6, cy + 16), (cx - 6, cy + 16)]])
        art = toon(art, fan, "#fbe2d6", "#ffffff", nx, k=5, line=NAVY, line_w=1.6)
        ribs = strokes(W, H, [([(cx, cy + 14), (cx + math.cos(a) * 26, cy + 4 + math.sin(a) * 26)], 1.4, None) for a in np.linspace(math.pi * 1.15, math.pi * 1.85, 6)]) * fan
        art = G(art, ribs, "#e09a88", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.3)
    preview(art, "sam-seabed", bg="#5fbccc")
    save(art, f"{OUT}/seabed.webp", max_w=780, quality=80)
    clear()

if "divider" in PARTS:
    W, H = 420, 110
    nx = Seq(1900); rng = random.Random(19)
    art = blank(W, H)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = 40 if i % 2 == 0 else 18
        pts.append((210 + math.cos(a) * rr, 58 + math.sin(a) * rr))
    m = shapes(W, H, [pts])
    art = toon(art, m, "#f6873a", "#ffb15a", nx, k=6, line=NAVY, line_w=2.0)
    art = G(art, circles(W, H, [(210 + rng.uniform(-14, 14), 58 + rng.uniform(-14, 14), 2.4) for _ in range(9)]) * m, "#ffe1b8", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.2)
    for x, y, r in ((150, 60, 12), (118, 50, 8), (92, 62, 6), (70, 54, 4), (270, 60, 12), (302, 50, 8), (328, 62, 6), (350, 54, 4)):
        art = bubble(art, W, H, x, y, r, nx, rim="#3aa8c8", tint="#bff0f6", dens=0.85)
    preview(art, "sam-divider", tone="#f4fbfb")
    save(art, f"{OUT}/divider.webp", max_w=210, quality=84)

kb(OUT)
