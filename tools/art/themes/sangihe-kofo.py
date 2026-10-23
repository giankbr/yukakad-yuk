"""Sangihe Kofo — kofo cloth woven from abaca banana fibre (fine warp stripes, natural fibre sheen), volcanic islands
rising from a deep blue sea, an outrigger boat. Gouache + watercolour, painted sky and sea.
Run: python3 -I sangihe-kofo.py [part ...]  parts: kofo scene boat smoke divider node
Assets -> public/themes/art/sangihe-kofo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n2_lib import *

OUT = outdir("sangihe-kofo")
PARTS = sys.argv[1:] or ["kofo", "scene", "boat", "smoke", "divider", "node"]

ABACA, ABACA_L, ABACA_D = "#cdb383", "#e2cfa4", "#9c7f50"
RUST, BROWN, INDIGO, CREAM, BLACK = "#9f4426", "#5a3a22", "#283f66", "#efe3c4", "#221a14"

WARP = [(ABACA, 10), (BROWN, 2), (ABACA, 3), (RUST, 4), (ABACA_L, 2), (RUST, 4), (ABACA, 3), (BROWN, 2), (ABACA, 8),
        (INDIGO, 3), (CREAM, 1), (INDIGO, 3), (ABACA, 6), (BLACK, 1), (ABACA_L, 4), (BLACK, 1), (ABACA, 7)]
WEFT = [(ABACA, 30), (ABACA_D, 2), (ABACA, 18), (RUST, 1), (ABACA, 13)]


def kofo_rgb(w, h, seed=11, thread=2.6):
    n_warp = sum(n for _, n in WARP)
    # make the stripe repeat fit the tile exactly: w must be multiple of n_warp*thread
    return weave(w, h, WARP, WEFT, seed=seed, warp=thread, weft=thread * 0.9, slub=0.7, sheen=0.25, fibre=0.9)


def kofo():
    n = sum(n for _, n in WARP)  # 64 threads per repeat
    w = int(n * 2.6 * 2)
    h = 360
    rgb = kofo_rgb(w, h)
    save_rgb(opaque(rgb), f"{OUT}/kofo.webp", quality=80)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{PREV}/sk-kofo.png")


def scene():
    W, H = 780, 1500
    nx = Seq(500)
    rng = random.Random(5)
    horizon = 905
    sky = painted_sky(W, horizon + 20, [(0.0, "#f6eedb"), (0.38, "#f3e6cc"), (0.62, "#e6dccb"), (0.82, "#c7d6dc"), (1.0, "#a9c3d2")], seed=3, streak=0.25, grain=0.3)
    art = blank(W, H)
    art[:horizon + 20] = sky
    # soft dawn sun haze low right
    halo = circles(W, H, [(560, 700, 70)])
    art = over(art, glow(halo, "#f9d9a0", radius=60, strength=0.35))
    # far islands (pale, watercolour)
    far = shapes(W, H, [curve([(-20, horizon + 4), (40, horizon - 30), (120, horizon - 52), (190, horizon - 40), (250, horizon - 8), (300, horizon + 4)], 40) + [(300, horizon + 10), (-20, horizon + 10)],
                        curve([(600, horizon + 4), (650, horizon - 22), (720, horizon - 34), (800, horizon - 18), (820, horizon + 4)], 30) + [(820, horizon + 10), (600, horizon + 10)]])
    art = G(art, far, "#9db4c0", "#8aa5b4", seed=nx(), density=0.75, edge=0.4, bloom=0.3, rough=4)
    # soft clouds
    cl = shapes(W, H, [deform(ellipse_pts(cx_, cy_, rx_, ry_, 12), rng, 2, 0.1) for cx_, cy_, rx_, ry_ in [(150, 560, 150, 18), (260, 540, 90, 14), (640, 430, 120, 14), (700, 452, 80, 10)]])
    art = G(art, cl, "#fbf6ea", "#f1e7d6", seed=nx(), density=0.55, edge=0.15, bloom=0.5, rough=8, feather=4)
    # second, broader island on the left (Awu-like), paler: further away
    awu = shape_mask(W, H, wobble(curve([(-40, horizon + 10), (-10, 760), (60, 690), (120, 662), (150, 668), (190, 700), (260, 780), (330, horizon - 10), (360, horizon + 10)], 60), rng, 1.0))
    art = G(art, awu, "#7f97a6", "#8ea3ae", seed=nx(), density=0.85, edge=0.45, bloom=0.3, rough=4)
    art = G(art, awu * np.clip((150 - np.mgrid[0:H, 0:W][1]) / 120, 0, 1), "#6a8494", seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=4)
    # main volcano (Karangetang-like): steep concave cone, summit right of centre
    sx, sy = 470, 520
    left = [(sx - 22, sy + 6), (sx - 70, sy + 90), (sx - 140, sy + 200), (sx - 230, sy + 300), (sx - 340, sy + 370), (sx - 470, sy + 392)]
    right = [(sx + 26, sy + 4), (sx + 80, sy + 100), (sx + 150, sy + 220), (sx + 230, sy + 320), (sx + 330, sy + 375)]
    cone_pts = [(sx - 470, horizon + 12)] + left[::-1] + [(sx - 10, sy - 2), (sx + 2, sy + 10), (sx + 14, sy - 4)] + right + [(sx + 360, horizon + 12)]
    cone = shape_mask(W, H, wobble(cone_pts, rng, 1.2))
    art = GP(art, cone, "#4b6577", "#5d7686", seed=nx(), rough=2.5, streak=0.9)
    # light from the right: lit flank + shadow flank
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lit = cone * np.clip((xx - sx + 10) / 180, 0, 1) * np.clip((yy - sy + 20) / 100, 0, 1)
    art = G(art, lit, "#b7a58e", "#c9b08c", seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=3)
    shade = cone * np.clip((sx - 60 - xx) / 300, 0, 1)
    art = G(art, shade, "#2f4659", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=3)
    # ravines (barranco streaks) down the cone
    items = []
    for k in range(9):
        t = (k - 4) / 4 + rng.uniform(-0.12, 0.12)
        x0 = sx + t * 18
        pts = curve([(x0, sy + 20), (x0 + t * 60 + rng.gauss(0, 8), sy + 120), (x0 + t * 150 + rng.gauss(0, 12), sy + 240), (x0 + t * 250 + rng.gauss(0, 14), sy + 330)], 30)
        items.append((pts[:rng.randint(14, 30)], rng.uniform(2.0, 4.5), (0.05, 0.6)))
    rav = strokes(W, H, items) * cone
    art = G(art, rav, "#2c4152", seed=nx(), density=0.45, edge=0.4, bloom=0, rough=1.5, feather=0.8)
    ridges = strokes(W, H, [([(x + 6, y) for x, y in p], w_ * 0.7, t_) for p, w_, t_ in items[::2]]) * cone * np.clip((xx - sx + 40) / 200, 0, 1)
    art = G(art, ridges, "#c2c7b8", seed=nx(), density=0.4, edge=0.2, bloom=0, rough=1.2, feather=0.8)
    # summit glow + old lava streak
    lava = strokes(W, H, [(curve([(sx + 4, sy + 8), (sx + 20, sy + 70), (sx + 52, sy + 150), (sx + 70, sy + 190)], 20), 5, (0.0, 0.7))])
    art = G(art, lava, "#c8693a", "#e08c4c", seed=nx(), density=0.7, edge=0.5, bloom=0, rough=1.5, feather=0.9)
    art = over(art, glow(circles(W, H, [(sx + 2, sy + 4, 14)]), "#f2a564", radius=12, strength=0.45))
    # forested lower slopes
    forest_pts = [(sx - 470, horizon + 12), (sx - 420, sy + 350), (sx - 300, sy + 318), (sx - 200, sy + 300), (sx - 120, sy + 316), (sx, sy + 300), (sx + 120, sy + 318), (sx + 230, sy + 330), (sx + 330, sy + 362), (sx + 360, horizon + 12)]
    forest = shape_mask(W, H, wobble(curve(forest_pts, 60), rng, 2.5)) * cone
    art = GP(art, forest, "#2f5a4a", "#3d6b52", seed=nx(), rough=3, streak=0.8)
    # tree crowns texture
    crowns = circles(W, H, [(rng.uniform(20, 800), rng.uniform(sy + 300, horizon), rng.uniform(5, 11)) for _ in range(260)]) * forest
    art = G(art, crowns * np.clip((yy - sy - 290) / 30, 0, 1), "#4f8061", seed=nx(), density=0.35, edge=0.5, bloom=0.2, rough=1.5)
    art = G(art, crowns * np.clip((sx - 100 - xx) / 300, 0, 1), "#1d3d33", seed=nx(), density=0.3, edge=0.4, bloom=0.2, rough=1.5)
    # palms along the shore
    for px in [160, 236, 268, 520, 604, 640, 728]:
        px += rng.uniform(-10, 10)
        base_y = horizon + 6
        hgt = rng.uniform(46, 70)
        lean = rng.uniform(-0.25, 0.25)
        top = (px + lean * hgt, base_y - hgt)
        trunk = strokes(W, H, [(curve([(px, base_y), (px + lean * hgt * 0.4, base_y - hgt * 0.5), top], 12), 3, (0.0, 0.5))])
        fr = []
        for j in range(7):
            a = -math.pi / 2 + (j - 3) * 0.55 + rng.gauss(0, .1)
            L = rng.uniform(18, 26)
            fr.append((curve([top, (top[0] + math.cos(a) * L * .6, top[1] + math.sin(a) * L * .6 - 4), (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L + 6)], 10), 3.2, (0.05, 0.6)))
        art = GP(art, np.maximum(trunk, strokes(W, H, fr)), "#1f3a30", seed=nx(), rough=1.0, streak=0.4)
    # sea: deep blue painted gradient with brushed swells
    sea = painted_sky(W, H - horizon, [(0, "#4c7792"), (0.18, "#27557a"), (0.55, "#173d63"), (1, "#0f2c4b")], seed=8, streak=1.4)
    art[horizon:] = over(art[horizon:], sea)
    swell = []
    for k in range(110):
        y = horizon + 8 + (k / 110) ** 1.4 * (H - horizon - 10)
        depth = (y - horizon) / (H - horizon)
        L = 20 + depth * 120 * rng.uniform(.5, 1.2)
        x = rng.uniform(-40, W)
        swell.append((curve([(x, y), (x + L * .5, y - 1.5 - depth * 3), (x + L, y)], 10), 1.2 + depth * 3.4, (0.3, 0.4)))
    sw = strokes(W, H, swell)
    art = G(art, sw * (yy > horizon), "#7ea6bf", "#9fc0d0", seed=nx(), density=0.38, edge=0.4, bloom=0, rough=1.2, feather=0.8)
    dark = strokes(W, H, [([(x, y + 4 + 2) for x, y in p], w_ * 1.1, t_) for p, w_, t_ in swell[::2]])
    art = G(art, dark * (yy > horizon + 30), "#0b2340", seed=nx(), density=0.3, edge=0.3, bloom=0, rough=1.2, feather=0.8)
    # sun glitter path on the water under the haze
    glit = strokes(W, H, [([(560 + rng.gauss(0, 30 + (y - horizon) * 0.25), y), (560 + rng.gauss(0, 30 + (y - horizon) * 0.25) + 18, y)], 1.6, (0.3, 0.3))
                          for y in np.linspace(horizon + 4, horizon + 260, 50)])
    art = G(art, glit, "#f3dcb0", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.8, feather=0.6)
    # shoreline foam
    foam = strokes(W, H, [(curve([(-10, horizon + 6), (200, horizon + 9), (420, horizon + 7), (800, horizon + 10)], 40), 2.5, (0.1, 0.1))])
    art = G(art, foam, "#e9efe9", seed=nx(), density=0.5, edge=0.3, bloom=0.2, rough=2)
    art = add_grain(art, 4, 0.012)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/scene.webp", quality=78)
    preview(art, "sk-scene")


def boat():
    W, H = 520, 300
    nx = Seq(700)
    art = blank(W, H)
    rng = random.Random(9)
    # outrigger floats (bamboo) + booms
    floats = strokes(W, H, [(curve([(30, 238), (130, 242), (240, 244)], 20), 7, (0.15, 0.15)), (curve([(300, 244), (400, 242), (500, 236)], 20), 7, (0.15, 0.15))])
    booms = strokes(W, H, [(curve([(120, 240), (190, 214), (260, 206)], 14), 4.5, (0.0, 0.0)), (curve([(420, 238), (350, 214), (280, 208)], 14), 4.5, (0.0, 0.0)),
                           (curve([(80, 240), (160, 212), (240, 202)], 14), 3.5, (0.0, 0.0)), (curve([(460, 238), (380, 212), (300, 204)], 14), 3.5, (0.0, 0.0))])
    art = GP(art, floats, "#b89a5e", "#d2b77c", seed=nx(), rough=1.0)
    art = GP(art, booms, "#8a6a3c", seed=nx(), rough=0.8)
    # mast + rust sail (woven pandan sail)
    mast = strokes(W, H, [([(262, 212), (258, 40)], 4, (0.0, 0.1))])
    art = GP(art, mast, "#4a3220", seed=nx(), rough=0.6)
    sail = shape_mask(W, H, wobble([(264, 46), (330, 64), (372, 150), (350, 190), (268, 196)], rng, 1.2))
    art = GP(art, sail, RUST, "#b9582f", seed=nx(), rough=2, streak=1.0)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seams = sail * (np.abs(((yy - 40) / 22) % 1 - 0.5) < 0.06)
    art = G(art, seams, "#6a2a17", seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1, feather=0.6)
    art = G(art, sail * np.clip((xx - 300) / 70, 0, 1), "#6a2a17", seed=nx(), density=0.3, edge=0.2, bloom=0.2, rough=2)
    # hull
    hull = shape_mask(W, H, [(150, 200), (200, 214), (330, 214), (392, 196), (378, 222), (330, 238), (200, 238), (162, 222)])
    art = GP(art, hull, "#3b2a1e", "#4c3626", seed=nx(), rough=1.4)
    stripe = strokes(W, H, [(curve([(158, 208), (250, 220), (386, 204)], 20), 4, (0.05, 0.05))]) * hull
    art = GP(art, stripe, CREAM, seed=nx(), rough=0.6)
    dots = circles(W, H, [(180 + k * 26, 228 + (1 if k % 2 else 0), 2.6) for k in range(8)]) * hull
    art = GP(art, dots, RUST, seed=nx(), rough=0.4)
    # small wake
    wake = strokes(W, H, [(curve([(130, 252), (260, 258), (420, 252)], 20), 3, (0.2, 0.2)), (curve([(40, 250), (110, 256)], 8), 2, (0.2, 0.2))])
    art = G(art, wake, "#cfe0ea", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1)
    preview(art, "sk-boat", bg="#1c4469")
    save(art, f"{OUT}/boat.webp", max_w=300, quality=84)


def smoke():
    W, H = 520, 360
    nx = Seq(800)
    rng = random.Random(3)
    art = blank(W, H)
    puffs = []
    for k in range(16):
        t = k / 15
        puffs.append(ellipse_pts(60 + t * 400 + rng.gauss(0, 10), 320 - t * 230 - math.sin(t * 3) * 30 + rng.gauss(0, 8), 26 + t * 50, 18 + t * 30, 12, rng.uniform(-.4, .4)))
    m = shapes(W, H, [deform(p, rng, 2, 0.12) for p in puffs])
    art = G(art, m, "#d9d5cc", "#c3c3bd", seed=nx(), density=0.5, edge=0.3, bloom=0.6, rough=10, feather=4)
    art = G(art, m * np.clip((np.arange(H)[:, None] - 160) / 160, 0, 1), "#9da3a6", seed=nx(), density=0.25, edge=0.2, bloom=0.5, rough=8, feather=4)
    preview(art, "sk-smoke", bg="#e9e0cc")
    save(art, f"{OUT}/smoke.webp", max_w=300, quality=82)


def divider():
    """A short strip of kofo with knotted fringes at both ends."""
    W, H = 520, 70
    rng = random.Random(4)
    cloth = kofo_rgb(W, 40, seed=21, thread=2.2)
    cloth = np.transpose(cloth, (1, 0, 2))  # stripes along the strip
    cloth = np.array(Image.fromarray((cloth * 255).astype(np.uint8)).resize((W, 40)), np.float32) / 255
    art = blank(W, H)
    x0, x1, y0 = 90, 430, 15
    body = np.zeros((H, W), np.float32)
    body[y0:y0 + 40, x0:x1] = 1
    body = fray(body, 3, 1.5, 0.2)
    rgb = np.zeros((H, W, 3), np.float32)
    rgb[y0:y0 + 40, :] = cloth
    art = over(art, rgba(rgb, body))
    items = []
    for side, xa in ((-1, x0), (1, x1)):
        for k in range(14):
            y = y0 + 2 + k * 2.8
            L = rng.uniform(46, 70)
            items.append((curve([(xa, y), (xa + side * L * .5, y + rng.gauss(0, 2)), (xa + side * L, y + rng.gauss(0, 4) + (k - 7) * 1.2)], 10), 1.3, (0.0, 0.5)))
    fr = strokes(W, H, items)
    art = GP(art, fr, ABACA, ABACA_D, seed=31, rough=0.6, streak=0.5)
    knots = circles(W, H, [(x0 - 6, y0 + 8, 4), (x0 - 6, y0 + 20, 4), (x0 - 6, y0 + 32, 4), (x1 + 6, y0 + 8, 4), (x1 + 6, y0 + 20, 4), (x1 + 6, y0 + 32, 4)])
    art = GP(art, knots, ABACA_D, seed=33, rough=0.5)
    preview(art, "sk-divider", bg="#f2e9d6")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)


def node():
    """Woven diamond token (a kofo offcut folded into a lozenge with a rust stitch border)."""
    W = H = 160
    rgb = kofo_rgb(W, H, seed=41, thread=2.0)
    rgb = warp_img(rgb, 0, 0)
    m = shape_mask(W, H, diamond(80, 80, 68, 74), smooth=False)
    m = fray(m, 5, 1.2, 0.15)
    art = rgba(rgb, m)
    rim = np.clip(m - gaussian_filter((m > 0.5).astype(np.float32), 3) * 1.4, 0, 1) * 2
    art = GP(art, np.clip(rim, 0, 1), RUST, seed=43, rough=0.6)
    preview(art, "sk-node", bg="#f2e9d6")
    save(art, f"{OUT}/node.webp", max_w=96, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
kb_total(OUT)
