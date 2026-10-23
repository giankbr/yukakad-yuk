"""Bunga Matahari — thick painterly gouache: a sunflower field under a tall summer sky (deep cobalt to pale haze,
big loaded-brush cumulus), heads receding in rows to a blue-green treeline, giant heads and heart leaves in the
foreground; a front-facing head with phyllotaxis seed dabs, a tall stem, a hand-tied bunch, a cloud strip and a
sprig divider. Original composition; warm cadmium yellow, ochre, sap green against cobalt.
Run: python3 -I bunga-matahari.py [part ...]  parts: field head stem bunch clouds sprig"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i6_lib import *  # noqa

OUT = outdir("bunga-matahari")
PARTS = sys.argv[1:] or ["field", "head", "stem", "bunch", "clouds", "sprig"]
YEL, YEL_L, YEL_D, ORA, BRN, BRN_D, BRN_L = "#f2b705", "#fbd75b", "#d98e04", "#c8670a", "#5a3313", "#2e190a", "#8c5a24"
GRN, GRN_D, GRN_L, SKY, COB = "#4f7a24", "#2c4a16", "#8aa83a", "#5d93cf", "#2f63ad"
GOLDEN = math.pi * (3 - math.sqrt(5))


def head(art, W, H, cx, cy, r, rng, seed, squash=1.0, rot=0.0, petals=24, detail=True):
    """Sunflower head: back ring of darker petals, front ring of bright petals, brown disc with spiral seed dabs."""
    def pt(u, v):
        x, y = u, v * squash
        return (cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot))
    rings = [(r * 1.0, YEL_D, ORA, 0.5 / petals, .8), (r * 0.94, YEL, YEL_L, 0.0, 1.0)]
    for k, (L, c1, c2, off, wk) in enumerate(rings):
        polys = []
        for i in range(petals):
            a = (i / petals + off) * 2 * math.pi + rng.uniform(-.05, .05)
            ln = L * rng.uniform(.8, 1.0)
            wd = r * rng.uniform(.085, .11) * wk
            base = r * .4
            bend = rng.uniform(-.1, .1)
            side1, side2 = [], []
            for t in np.linspace(0, 1, 10):
                d = base + (ln - base) * t
                w = wd * (math.sin(math.pi * min(1, t * 1.05 + .04)) ** .6)
                a2 = a + bend * t * t
                side1.append(pt(math.cos(a2) * d - math.sin(a2) * w, math.sin(a2) * d + math.cos(a2) * w))
                side2.append(pt(math.cos(a2) * d + math.sin(a2) * w, math.sin(a2) * d - math.cos(a2) * w))
            polys.append(side1 + side2[::-1])
        if not detail:
            art = impasto(art, shapes(W, H, polys), c1, c2, seed=seed + k, rough=1.0, ridge=.6)
            continue
        for i, q in enumerate(polys):
            m = shapes(W, H, [q])
            cA = mix(c1, c2, rng.uniform(0, .6))
            art = impasto(art, m, cA, c2, seed=seed + k * 50 + i, rough=.9, ridge=.8, pad=6)
            art = tint(art, inner_edge(m, 1.6), "#a8650a", .55, seed=seed + i)
        allm = shapes(W, H, polys)
        ring_in = np.clip(circle_mask(W, H, cx, cy, r * .6) - circle_mask(W, H, cx, cy, r * .38), 0, 1)
        art = tint(art, gaussian_filter(ring_in, r * .05) * allm, ORA, .6, seed=seed + 5)
        art = tint(art, side_light(allm, 4, 4, 2) * allm, "#a8650a", .3, seed=seed + 6)
    disc = shapes(W, H, [[pt(math.cos(a) * r * .46, math.sin(a) * r * .46) for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]])
    art = impasto(art, disc, BRN, BRN_L, seed=seed + 10, rough=1.2, ridge=.8)
    if detail:
        n = int(min(700, 2.6 * (r * .44) ** 2 / max(2.0, r * .028) ** 2))
        dk, lt = [], []
        for i in range(n):
            rr = r * .43 * math.sqrt((i + .5) / n)
            a = i * GOLDEN
            x, y = pt(math.cos(a) * rr + rng.uniform(-.6, .6), math.sin(a) * rr + rng.uniform(-.6, .6))
            sz = max(1.0, r * .026 * (0.55 + 0.6 * i / n)) * rng.uniform(.8, 1.15)
            (lt if (rr > r * .36 and rng.random() < .55) or rng.random() < .08 else dk).append((x, y, sz))
        art = OV(art, circles(W, H, dk) * disc, lambda mm: col_arr(mm, BRN_D, mm * .8), pad=4)
        art = OV(art, circles(W, H, lt) * disc, lambda mm: col_arr(mm, "#b07d34", mm * .85), pad=4)
        core = circle_mask(W, H, *pt(0, 0), r * .07)
        art = impasto(art, core, "#4f4a1c", "#6b5a22", seed=seed + 12, rough=.8)
        art = tint(art, side_light(disc, 6, 6, r * .05) * disc, BRN_D, .55, seed=seed + 13)
        art = tint(art, np.clip(side_light(disc, -5, -5, r * .04), 0, 1) * disc, "#c08a40", .35, seed=seed + 14)
    return art


def leaf(art, W, H, x, y, L, ang, rng, seed, col=GRN, col2=GRN_L):
    """Heart-shaped sunflower leaf with painted veins."""
    top, bot = [], []
    for u in np.linspace(0, 1, 22):
        w = L * .4 * (u ** .45) * ((1 - u) ** .85) * 1.7 + (L * .08 * (1 - u) ** 6 if u > .02 else 0)
        top.append(P(x, y, ang, u * L, w)); bot.append(P(x, y, ang, u * L, -w * .94))
    pts = top + bot[::-1]
    m = shapes(W, H, [deform(pts, rng, 2, .01)])
    art = impasto(art, m, col, col2, seed=seed, rough=1.6, ridge=.8, dirn=ang)
    art = tint(art, side_light(m, 5, 6, 4) * m, GRN_D, .6, seed=seed + 1)
    vs = [([P(x, y, ang, L * .05, 0), P(x, y, ang, L * .5, L * .01), P(x, y, ang, L * .92, 0)], max(1.4, L * .02), (0.05, 0.6))]
    for t in (.22, .42, .62):
        for sg in (-1, 1):
            vs.append(([P(x, y, ang, L * t, 0), P(x, y, ang, L * (t + .12), sg * L * .16), P(x, y, ang, L * (t + .2), sg * L * .26)], max(1.1, L * .013), (0.05, 0.7)))
    art = OV(art, strokes(W, H, vs) * m, lambda mm: col_arr(mm, "#9cbc52", mm * .55), pad=4)
    return art


def stalk(art, W, H, pts, wd, seed):
    m = strokes(W, H, [(curve(pts, 40), wd, (0.0, 0.1))])
    art = impasto(art, m, GRN, "#6a8f2c", seed=seed, rough=1.0, ridge=.6, dirn=math.pi / 2)
    return tint(art, side_light(m, 3, 0, 1.5) * m, GRN_D, .6, seed=seed + 1)


def cloud(art, W, H, cx, cy, sc, rng, seed, shadow="#a9b4cc"):
    """Loaded-brush cumulus modelled in three opaque values: cool shadow mass, white body (smaller, lifted toward
    the light), warm highlight caps; flat-ish base."""
    cs = []
    for k in range(int(14 * sc) + 6):
        t = rng.uniform(-1, 1)
        cs.append((cx + t * 130 * sc, cy - (1 - t * t) * 70 * sc * rng.uniform(.4, 1.2) + rng.uniform(-6, 6), rng.uniform(20, 58) * sc))
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    base = np.clip((cy + 24 * sc - yy) / 5, 0, 1)
    m = circles(W, H, cs) * base
    art = impasto(art, m, shadow, "#bcc4d6", seed=seed, rough=4.0, ridge=.6, dirn=.2, streak=.5)
    body = circles(W, H, [(x - 5 * sc, y - 9 * sc, r * .86) for x, y, r in cs]) * np.clip((cy + 4 * sc - yy) / 14, 0, 1)
    art = impasto(art, body, "#f7f6f0", "#ecebe6", seed=seed + 1, rough=4.0, ridge=.6, dirn=.2, streak=.5)
    caps = circles(W, H, [(x - 9 * sc, y - 16 * sc, r * .55) for x, y, r in cs if rng.random() < .6])
    art = impasto(art, caps * body, "#fffbec", "#fff6dc", seed=seed + 2, rough=3.0, ridge=.6, streak=.5)
    return art


# ------------------------------------------------------------------ cover field
def part_field():
    W, H = 720, 1180
    rng = random.Random(7)
    hz = 790
    art = painted_sky(W, H, [(0, "#2557a0"), (0.22, "#3a78c2"), (0.45, "#79a9d8"), (0.62, "#c6dbe9"), (hz / H, "#edeee4"), (hz / H + .001, "#6e8d3a"), (1, "#3b5a1a")], seed=2, streak=1.2)
    # broad visible sky strokes
    sk = []
    for k in range(70):
        y = rng.uniform(0, hz - 40); x = rng.uniform(-40, W)
        L = rng.uniform(80, 220)
        sk.append(([(x, y), (x + L * .5, y + rng.uniform(-6, 6)), (x + L, y + rng.uniform(-8, 8))], rng.uniform(10, 22), (0.3, 0.3)))
    m = strokes(W, H, sk)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    t = np.clip(yy / hz, 0, 1)
    art = OV(art, m, lambda mm: col_arr(mm, "#ffffff", mm * .045), pad=4)
    art = cloud(art, W, H, 150, 560, 1.25, rng, 11)
    art = cloud(art, W, H, 590, 470, 1.0, rng, 21)
    art = cloud(art, W, H, 680, 680, .7, rng, 31)
    art = cloud(art, W, H, 40, 700, .55, rng, 41)
    clear()
    # treeline + hills
    hill = shape_mask(W, H, [(-10, hz + 4)] + [(x, hz - 26 - 14 * math.sin(x / 120 + 1) - rng.uniform(0, 5)) for x in range(0, W + 40, 40)] + [(W + 10, hz + 4)], smooth=True)
    art = impasto(art, hill, "#7f9fa8", "#93adb0", seed=50, rough=2.0)
    trees = circles(W, H, [(x + rng.uniform(-6, 6), hz - 4 - rng.uniform(0, 10), rng.uniform(8, 16)) for x in range(0, W, 14)])
    trees = trees * (yy < hz + 6)
    art = impasto(art, trees, "#3f5f3a", "#55704a", seed=51, rough=2.0)
    # field: a warm yellow haze band, then rows of heads, small far -> big near (perspective), all turned to the sun
    band = np.clip((yy - hz - 4) / 8, 0, 1) * np.clip((hz + 150 - yy) / 60, 0, 1)
    art = impasto(art, band.astype(np.float32), "#e0b21e", "#c99a1c", seed=60, rough=3.0, ridge=1.0)
    rows = 34
    for ri in range(rows):
        f = ri / (rows - 1)
        y = hz + 4 + (f ** 1.8) * 270
        r = 2.0 + f ** 2.3 * 24
        green, yel, brn = [], [], []
        x = rng.uniform(-r, r)
        while x < W + r:
            rr = r * rng.uniform(.7, 1.3)
            yj = y + rng.uniform(-r * .7, r * .7)
            if f > .15:
                green.append(([(x - rr * 1.2, yj + rr * .7), (x + rr * 1.3, yj + rr * 1.1)], rr * rng.uniform(.6, 1.1), None))
            if rr > 4.5:
                k = 9
                ang0 = rng.uniform(0, 1)
                for j in range(k):
                    aa = ang0 + j / k * 2 * math.pi
                    yel.append(([(x + math.cos(aa) * rr * .3, yj + math.sin(aa) * rr * .24), (x + math.cos(aa) * rr * 1.05, yj + math.sin(aa) * rr * .82)], rr * .42, (0.1, 0.6)))
                brn.append((x + rr * .08, yj, rr * .36, rr * .3, 0))
            else:
                yel.append(([(x - rr * .9, yj), (x + rr * .9, yj + rng.uniform(-1, 1))], rr * 1.1, (0.3, 0.3)))
            x += rr * rng.uniform(1.6, 3.0)
        if green:
            art = impasto(art, strokes(W, H, green), "#3c5c1c", "#668a2a", seed=100 + ri, rough=1.4, ridge=.8)
        art = impasto(art, strokes(W, H, yel), YEL if ri % 3 else "#f4c21c", YEL_L if f > .3 else "#ecc94a", seed=200 + ri, rough=1.2 + f * 1.5, ridge=.9)
        if brn:
            art = impasto(art, ellipses(W, H, brn), BRN, BRN_L, seed=300 + ri, rough=.8, ridge=.6)
        if ri % 6 == 5:
            clear()
    # near foreground: leaves and big heads
    for (x, y, L, a) in [(70, 1120, 190, -2.2), (240, 1150, 170, -1.2), (520, 1150, 200, -1.9), (660, 1080, 170, -0.9), (360, 1170, 160, -2.6)]:
        art = leaf(art, W, H, x, y, L, a, rng, 400 + x)
    clear()
    art = stalk(art, W, H, [(110, H + 10), (104, 1060), (96, 990)], 22, 500)
    art = head(art, W, H, 96, 960, 132, rng, 510, squash=.9, rot=.25)
    clear()
    art = stalk(art, W, H, [(600, H + 10), (612, 1080), (626, 1030)], 18, 520)
    art = head(art, W, H, 628, 1004, 104, rng, 530, squash=.85, rot=-.3)
    clear()
    art = head(art, W, H, 380, 1140, 70, rng, 540, squash=.8, rot=.1, petals=20)
    art = add_grain(art, 4, .03)
    preview(art, "bm-field")
    save_rgb(art, f"{OUT}/field.webp", size=(600, 983), quality=72)


def part_head():
    W = H = 420
    rng = random.Random(3)
    art = head(blank(W, H), W, H, 210, 210, 196, rng, 1, petals=26)
    preview(art, "bm-head", tone="#fbf3df")
    save(art, f"{OUT}/head.webp", max_w=300, quality=80)


def part_stem():
    W, H = 340, 860
    rng = random.Random(5)
    art = blank(W, H)
    art = stalk(art, W, H, [(170, H - 4), (160, 600), (176, 330), (190, 200)], 16, 1)
    for (x, y, L, a) in [(166, 640, 170, -2.7), (170, 520, 150, -0.35), (178, 400, 120, -2.9), (176, 300, 100, -0.5)]:
        art = leaf(art, W, H, x, y, L, a, rng, 10 + y)
    art = head(art, W, H, 196, 140, 124, rng, 40, squash=.92, rot=.2)
    preview(art, "bm-stem", tone="#fbf3df")
    save(art, f"{OUT}/stem.webp", max_w=240, quality=80)


def part_bunch():
    W, H = 620, 560
    rng = random.Random(9)
    art = blank(W, H)
    for (x0, x1, y1) in [(300, 150, 250), (310, 460, 230), (305, 300, 170), (300, 230, 330), (310, 400, 340)]:
        art = stalk(art, W, H, [(x0, 540), ((x0 + x1) / 2, (540 + y1) / 2), (x1, y1)], 9, x1)
    for (x, y, L, a) in [(250, 420, 130, -2.6), (350, 430, 130, -0.5), (300, 470, 100, -1.9)]:
        art = leaf(art, W, H, x, y, L, a, rng, x + y)
    clear()
    # twine bow
    art = rope(art, W, H, [(262, 470), (300, 480), (340, 468)], 7, seed=3, col="#d8b98a", dark="#8a6a3e")
    art = rope(art, W, H, [(300, 478), (262, 500), (250, 528)], 5, seed=4, col="#d8b98a", dark="#8a6a3e")
    art = rope(art, W, H, [(304, 478), (340, 506), (350, 534)], 5, seed=5, col="#d8b98a", dark="#8a6a3e")
    for i, (x, y, r, rot) in enumerate([(150, 250, 92, .3), (460, 230, 96, -.3), (230, 330, 76, .5), (400, 340, 80, -.5), (300, 170, 104, 0)]):
        art = head(art, W, H, x, y, r, rng, 60 + i * 20, squash=.9, rot=rot, petals=22)
        clear()
    preview(art, "bm-bunch", tone="#fbf3df")
    save(art, f"{OUT}/bunch.webp", max_w=460, quality=80)


def part_clouds():
    W, H = 900, 260
    rng = random.Random(13)
    art = blank(W, H)
    for (cx, cy, sc) in [(140, 190, .9), (450, 170, 1.1), (760, 200, .8)]:
        art = cloud(art, W, H, cx, cy, sc, rng, int(cx), shadow="#a9bdd2")
    preview(art, "bm-clouds", bg="#3a78c2")
    save(art, f"{OUT}/clouds.webp", max_w=800, quality=80)


def part_sprig():
    W, H = 460, 110
    rng = random.Random(21)
    art = blank(W, H)
    art = stalk(art, W, H, [(20, 70), (120, 62), (230, 58), (340, 64), (440, 70)], 5, 1)
    for (x, a) in [(100, -2.2), (150, -0.8), (310, -2.3), (360, -0.9)]:
        art = leaf(art, W, H, x, 62, 54, a, rng, x)
    art = head(art, W, H, 230, 54, 46, rng, 80, petals=20)
    preview(art, "bm-sprig", tone="#fbf3df")
    save(art, f"{OUT}/sprig.webp", max_w=420, quality=82)


for p in PARTS:
    globals()[f"part_{p}"]()
    clear()
