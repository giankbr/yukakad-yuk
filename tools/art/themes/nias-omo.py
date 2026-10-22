"""Nias Omo Sebua — black, red, yellow and gold: the chieftain's house Omo Sebua in gouache (massive vertical ehomo
pillars braced by crossed diagonal driwa on stone footings, hull-like flaring facade with a lattice window bay, a
towering thatched roof with a raised skylight hatch), carved wood relief bands printed like linocut with worn gold,
a carved rosette emblem and a painted ochre sky.
Run: python3 -I nias-omo.py [part ...]   parts: omo sky relief rosette divider
Assets -> public/themes/art/nias-omo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b1_lib import *
import _jw_lib as jw

OUT = outdir("nias-omo")
PARTS = sys.argv[1:] or ["omo", "sky", "relief", "rosette", "divider"]
BLACK, RED, RED_D, YEL, GOLD = "#151010", "#a3241c", "#6e1610", "#e2b02a", "#c99a3c"
WOOD, WOOD_D, WOOD_L = "#5b3a24", "#2e1c11", "#7e5634"


def rosette_items(cx, cy, r, petals=8):
    polys = [petal_pts(cx + math.cos(a) * r * 0.42, cy + math.sin(a) * r * 0.42, r * 0.62, r * 0.26, a, n=10)
             for a in [k * math.tau / petals for k in range(petals)]]
    items = [(arc_pts(cx, cy, r, 0, math.tau, 48), r * 0.12, None), (arc_pts(cx, cy, r * 0.2, 0, math.tau, 20), r * 0.1, None)]
    return items, polys


def band_motif(W, H, period, y, h, x0=0):
    """Carved band: rosettes alternating with stepped double triangles and a rope border."""
    items, polys = [], []
    for k, x in enumerate(np.arange(x0 + period / 2, W + period, period)):
        if k % 2 == 0:
            it, pl = rosette_items(x, y, h * 0.36)
        else:
            it, pl = [], []
            for s_ in (-1, 1):
                pl.append([(x - h * 0.34, y + s_ * h * 0.04), (x + h * 0.34, y + s_ * h * 0.04), (x, y + s_ * h * 0.38)])
            it.append(([(x - h * 0.5, y), (x + h * 0.5, y)], h * 0.05, None))
        items += it; polys += pl
    # rope borders (twisted cord)
    for yy in (y - h * 0.47, y + h * 0.47):
        for x in np.arange(-4, W + 8, h * 0.16):
            items.append(([(x, yy - h * 0.04), (x + h * 0.1, yy + h * 0.04)], h * 0.05, None))
    return items, polys


if "relief" in PARTS:
    W, H = 640, 96
    nx = Seq(900)
    band = np.ones((H, W), np.float32)
    items, polys = band_motif(W, H, 80, H / 2, H * 0.86)
    art = jw.carve(W, H, band, items, polys, nx, base=WOOD, light=WOOD_L, dark=WOOD_D, gold=GOLD, gold_amt=0.5, seed=4)
    # painted accents in the recesses: red and yellow pigment rubbed into the carving (as on Nias house beams)
    relief = np.maximum(strokes(W, H, items), shapes(W, H, polys, smooth=False))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rk = ((xx // 80) % 2 == 0).astype(np.float32)
    art = G(art, relief * rk, RED, seed=nx(), density=0.45, edge=0.2, bloom=0.1, rough=0.6, feather=0.6)
    art = G(art, relief * (1 - rk), YEL, seed=nx(), density=0.35, edge=0.2, bloom=0.1, rough=0.6, feather=0.6)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/relief.webp", quality=80)
    show(art, "no-relief")
    clear()

if "divider" in PARTS:
    W, H = 360, 60
    nx = Seq(1200)
    band = shapes(W, H, [[(20, 8), (340, 8), (356, 30), (340, 52), (20, 52), (4, 30)]], smooth=False)
    items, polys = rosette_items(180, 30, 20)
    for s_ in (-1, 1):
        for k in range(4):
            x = 180 + s_ * (46 + k * 32)
            polys.append([(x - 11, 30), (x, 30 - 13), (x + 11, 30), (x, 30 + 13)])
    art = jw.carve(W, H, band, items, polys, nx, base=WOOD, light=WOOD_L, dark=WOOD_D, gold=GOLD, gold_amt=0.75, seed=3)
    save(art, f"{OUT}/divider.webp", max_w=360)
    show(art, "no-divider")
    clear()

if "rosette" in PARTS:
    W = H = 200
    nx = Seq(1300)
    disc = circles(W, H, [(100, 100, 92)])
    items, polys = rosette_items(100, 100, 70, 10)
    items.append((arc_pts(100, 100, 86, 0, math.tau, 64), 5, None))
    for k in range(20):
        a = k * math.tau / 20
        polys.append([(100 + math.cos(a) * 74, 100 + math.sin(a) * 74), (100 + math.cos(a + .12) * 84, 100 + math.sin(a + .12) * 84), (100 + math.cos(a - .12) * 84, 100 + math.sin(a - .12) * 84)])
    art = jw.carve(W, H, disc, items, polys, nx, base=WOOD, light=WOOD_L, dark=WOOD_D, gold=GOLD, gold_amt=0.9, seed=6)
    save(art, f"{OUT}/rosette.webp", max_w=180)
    show(art, "no-rosette", bg=BLACK)
    clear()

if "sky" in PARTS:
    W, H = 420, 620
    sky = painted_sky(W, H, [(0, "#efc561"), (0.45, "#e9a63a"), (0.78, "#c8682a"), (1, "#8f3a1c")], seed=8, streak=1.0, grain=0.8)
    sun = circles(W, H, [(300, 150, 70)])
    sky = G(sky, sun, "#fbe7a4", seed=21, density=0.75, edge=0.5, bloom=0.3, rough=6, feather=3)
    clouds = shapes(W, H, [deform(ellipse_pts(110, 200, 120, 14, 14), random.Random(2), 2, 0.1), deform(ellipse_pts(330, 250, 110, 10, 14), random.Random(3), 2, 0.1)])
    sky = G(sky, clouds, "#f6d27a", seed=22, density=0.5, edge=0.4, bloom=0.4, rough=8, feather=3)
    # distant hills of Teluk Dalam
    hills = shapes(W, H, [[(-10, 520), (90, 470), (200, 500), (300, 455), (430, 490), (430, 640), (-10, 640)]])
    sky = G(sky, hills, "#6a2a18", seed=23, density=0.55, edge=0.5, bloom=0.3, rough=7)
    sky[..., 3] = 1
    save_rgb(sky, f"{OUT}/sky.webp", quality=74)
    show(sky, "no-sky")
    clear()

if "omo" in PARTS:
    W, H = 760, 900
    nx = Seq(3000)
    rng = random.Random(31)
    art = blank(W, H)
    cx = 380
    # ground shadow + stones
    gs = shapes(W, H, [deform(ellipse_pts(cx, 868, 330, 18, 18), rng, 1, 0.03)])
    art = G(art, gs, "#1d0e08", seed=nx(), density=0.5, edge=0.2, bloom=0.1, rough=4, feather=5)
    px = [130, 205, 280, 345, 415, 480, 555, 630]
    stones = shapes(W, H, [deform(ellipse_pts(x, 858, 26, 13, 12), rng, 1, 0.06) for x in px])
    art = GP(art, stones, "#8a8476", "#5e5a50", seed=nx(), rough=1.6, streak=0.6)
    # crossed diagonal pillars (driwa) behind the verticals
    diag = []
    for i in range(len(px) - 1):
        diag.append(([(px[i], 850), (px[i + 1], 668)], 17, None))
        diag.append(([(px[i + 1], 850), (px[i], 668)], 17, None))
    dm = strokes(W, H, diag)
    art = GP(art, dm, WOOD, WOOD_D, seed=nx(), rough=1.2, streak=1.2)
    art = G(art, np.clip(dm - np.roll(dm, 3, 1), 0, 1), WOOD_L, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    # massive vertical pillars (ehomo)
    vm = strokes(W, H, [([(x, 856), (x + rng.uniform(-1, 1), 650)], 28, None) for x in px])
    art = knockout(art, vm, 1.0, 1)
    art = GP(art, vm, "#4a2e1b", "#2b190e", seed=nx(), rough=1.4, streak=1.4)
    hi = strokes(W, H, [([(x - 8, 852), (x - 8, 654)], 5, None) for x in px])
    art = G(art, hi, "#9a6c42", seed=nx(), density=0.45, edge=0, bloom=0.1, rough=0.6, feather=0.8)
    # floor beams
    fb = quad(W, H, [(96, 626), (664, 626), (672, 662), (88, 662)])
    art = GP(art, fb, WOOD_D, "#1c110a", seed=nx(), rough=1.2)
    # hull-like flaring body: bottom curves like a boat, walls lean out toward the eaves
    body_pts = [(104, 640)] + [(cx + (x - cx), 640 + 26 * (1 - ((x - cx) / 276) ** 2)) for x in np.linspace(104, 656, 24)] + [(656, 640), (706, 452), (54, 452)]
    # build body top->bottom polygon
    hull = [(54, 452), (706, 452), (668, 604)] + [(x, 604 + 34 * (1 - ((x - cx) / 290) ** 2)) for x in np.linspace(668, 92, 28)] + [(92, 604)]
    body = shapes(W, H, [hull], smooth=False)
    art = knockout(art, body, 1.0, 1)
    art = GP(art, body, WOOD, "#4a2e1b", seed=nx(), rough=1.8, streak=1.6)
    planks = strokes(W, H, [([(40, y), (720, y + rng.uniform(-1, 1))], 1.8, None) for y in range(560, 650, 11)]) * body
    art = G(art, planks, WOOD_D, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5, feather=0.6)
    # carved relief band across the hull (linocut-like, painted red/yellow)
    rb = quad(W, H, [(80, 512), (680, 512), (674, 556), (86, 556)])
    items, polys = band_motif(W, H, 60, 534, 44, x0=80)
    relief = np.maximum(strokes(W, H, items), shapes(W, H, polys, smooth=False)) * rb
    art = GP(art, rb, "#3a2416", seed=nx(), rough=0.8)
    art = LC(art, relief, "#d7a43a", seed=nx(), wear=0.4, rough=1.0)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rk = (((xx - 80) // 60) % 2 == 0).astype(np.float32)
    art = G(art, relief * rk, RED, seed=nx(), density=0.6, edge=0.2, bloom=0, rough=0.5, feather=0.5)
    # lattice window bay (tuwu-tuwu) right under the eaves, running the full width
    wb = quad(W, H, [(58, 458), (702, 458), (690, 508), (70, 508)])
    art = GP(art, wb, "#1a0f09", seed=nx(), rough=0.8)
    slats = strokes(W, H, [([(x, 460), (x - 4, 506)], 3.4, None) for x in range(66, 700, 12)]) * wb
    art = GP(art, slats, "#8a5e36", "#6b4528", seed=nx(), rough=0.5, streak=0.8)
    rails = strokes(W, H, [([(56, 458), (704, 458)], 6, None), ([(70, 508), (690, 508)], 5, None)])
    art = GP(art, rails, "#3a2416", seed=nx(), rough=0.6)
    # prow beams sticking out at both sides (like a ship's bow)
    prow = strokes(W, H, [(curve([(92, 604), (58, 590), (30, 560), (22, 530)], 20), 10, (0.0, 0.6)), (curve([(668, 604), (702, 590), (730, 560), (738, 530)], 20), 10, (0.0, 0.6))])
    art = GP(art, prow, WOOD_D, seed=nx(), rough=0.8)
    # towering thatched roof
    roof_pts = [(22, 464), (738, 464), (560, 150), (480, 58), (280, 58), (200, 150)]
    roof = shapes(W, H, [roof_pts], smooth=False)
    art = knockout(art, roof, 1.0, 1)
    art = GP(art, roof, "#4a3a2c", "#2f241b", seed=nx(), rough=2.6, streak=2.0)
    th = []
    for k in range(520):
        x = rng.uniform(40, 720); y = rng.uniform(70, 460)
        L = rng.uniform(22, 48)
        th.append(([(x, y), (x + (x - cx) * 0.04, y + L)], rng.uniform(1.2, 2.4), (0.1, 0.5)))
    thm = strokes(W, H, th[:260]) * roof
    art = G(art, thm, "#7a6650", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.6)
    thm2 = strokes(W, H, th[260:]) * roof
    art = G(art, thm2, "#1e1712", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6, feather=0.6)
    # thatch courses (horizontal bands)
    crs = strokes(W, H, [([(0, y), (W, y)], 2.2, None) for y in range(110, 460, 34)]) * roof
    art = G(art, crs, "#160f0a", seed=nx(), density=0.55, edge=0, bloom=0, rough=1.0, feather=0.8)
    # raised skylight hatch (lawa-lawa) on the front slope
    hatch = quad(W, H, [(318, 300), (442, 300), (452, 366), (308, 366)])
    hcap = quad(W, H, [(300, 302), (460, 302), (380, 246)])
    art = GP(art, hatch, "#1a0f09", seed=nx(), rough=0.6)
    hs = strokes(W, H, [([(x, 304), (x, 364)], 3, None) for x in range(318, 446, 11)]) * hatch
    art = GP(art, hs, "#8a5e36", seed=nx(), rough=0.4)
    art = GP(art, hcap, "#3a2c20", "#2a1f16", seed=nx(), rough=1.2, streak=1.2)
    art = G(art, strokes(W, H, [th_ for th_ in th[:60]]) * hcap, "#7a6650", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
    # ridge with upturned horn ends
    ridge = strokes(W, H, [([(276, 58), (484, 58)], 9, None)])
    horns = strokes(W, H, [(curve([(284, 60), (262, 44), (248, 22), (254, 8)], 16), 8, (0.0, 0.7)), (curve([(476, 60), (498, 44), (512, 22), (506, 8)], 16), 8, (0.0, 0.7))])
    art = GP(art, np.maximum(ridge, horns), WOOD_D, seed=nx(), rough=0.8)
    art = FO(art, horns * np.clip(fbm(W, H, nx(), 10, 2) * 1.6 - 0.3, 0, 1), GOLD, seed=nx(), emboss=0.5)
    # eave edge board with red/yellow painted zigzag
    eb = quad(W, H, [(18, 452), (742, 452), (742, 470), (18, 470)])
    art = GP(art, eb, BLACK, seed=nx(), rough=0.6)
    zz = strokes(W, H, [([(x, 455), (x + 10, 467), (x + 20, 455)], 3, None) for x in range(22, 736, 20)]) * eb
    art = GP(art, zz, YEL, seed=nx(), rough=0.4)
    # light from upper right (sun), shade on the left
    house = np.clip(roof + body + wb, 0, 1)
    art = G(art, house * np.clip((300 - xx) / 300, 0, 1), "#120a06", seed=nx(), density=0.45, edge=0.05, bloom=0.3, rough=3, feather=8)
    art = G(art, roof * np.clip((xx - 420) / 300, 0, 1) * np.clip(1 - (yy - 60) / 400, 0, 1), "#e9b45a", seed=nx(), density=0.35, edge=0.05, bloom=0.3, rough=3, feather=8)
    art = add_grain(art, 7, 0.03)
    save(art, f"{OUT}/omo.webp", max_w=700, quality=80)
    show(art, "no-omo", tone="#e9b45a")
    clear()
