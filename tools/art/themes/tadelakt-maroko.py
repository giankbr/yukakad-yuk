"""Tadelakt Maroko — polished tadelakt plaster (seamless tile), carved cedar door with brass studs, pierced brass
lantern with warm glow, Berber woven runner and a slim woven band. Geometry and architecture only, no figures.
Run: python3 -I tadelakt-maroko.py [part ...]   parts: dinding pintu lentera permadani anyam"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o3_lib import *

OUT = outdir("tadelakt-maroko")
PARTS = sys.argv[1:] or ["dinding", "pintu", "lentera", "permadani", "anyam"]
WALL = "#d7a38c"
CEDAR, CEDAR_D, CEDAR_L = "#7a4a2e", "#3e2214", "#a86f45"
BRASS = "#b98a40"
WOOL = {"c": "#efe3cf", "k": "#3a2419", "r": "#a8472e", "o": "#c98b3a", "s": "#7c7a5a"}


def wood(W, H, seed, col=CEDAR, dark=CEDAR_D, light=CEDAR_L, vertical=True):
    """Cedar grain: stretched noise rings + fine fibre."""
    g1 = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (40, 2) if vertical else (2, 40))
    g1 = (g1 - g1.min()) / (g1.max() - g1.min() + 1e-6)
    rings = 0.5 + 0.5 * np.sin(g1 * 60 + fbm(W, H, seed + 1, 60, 2) * 8)
    fib = gaussian_filter(np.random.default_rng(seed + 2).random((H, W)).astype(np.float32), (6, 0.5) if vertical else (0.5, 6))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    t = np.clip(rings * 0.7 + fbm(W, H, seed + 3, 90, 3) * 0.3, 0, 1)[..., None]
    rgb = hexarr(dark) * (1 - t) * 0.35 + hexarr(col) * (0.65 + 0.35 * t) + hexarr(light) * t * 0.12
    rgb = rgb * (1 + fib[..., None] * 0.05)
    return np.clip(rgb, 0, 1)


if "dinding" in PARTS:
    n = 512
    base = np.ones((n, n, 3), np.float32) * hexarr(WALL)
    big = wrap_noise(n, n, 11, 60)
    mid = wrap_noise(n, n, 12, 14)
    # trowel strokes: overlapping arcs, burnished (slightly lighter/darker crescents), seamless by drawing with wrap
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    rng = random.Random(5)
    tr = np.zeros((n, n), np.float32)
    for i in range(70):
        cx, cy = rng.uniform(0, n), rng.uniform(0, n)
        r = rng.uniform(50, 150); w_ = rng.uniform(10, 34); a0 = rng.uniform(0, math.tau); sweep = rng.uniform(1.0, 2.2)
        dx = (xx - cx + n / 2) % n - n / 2; dy = (yy - cy + n / 2) % n - n / 2
        d = np.sqrt(dx * dx + dy * dy); ang = (np.arctan2(dy, dx) - a0) % math.tau
        band = np.clip(1 - np.abs(d - r) / w_, 0, 1) * (ang < sweep) * np.sin(np.clip(ang / sweep, 0, 1) * math.pi)
        tr += band * rng.choice([-1, 1]) * rng.uniform(0.4, 1)
    tr = gaussian_filter(tr, 3, mode="wrap")
    rgb = base * (0.9 + 0.16 * big[..., None]) * (0.97 + 0.05 * mid[..., None])
    tr = tr / (np.abs(tr).max() + 1e-6)
    rgb = rgb * (1 + tr[..., None] * 0.07)
    rgb = rgb * (1 - np.clip(tr, 0, 1)[..., None] ** 2 * 0.0) + hexarr('#f6dccb') * (np.clip(tr, 0, 1) ** 3)[..., None] * 0.12
    # warm clay drift: rose to ochre
    drift = wrap_noise(n, n, 13, 80)[..., None]
    rgb = rgb * (1 - drift * 0.12) + hexarr("#d9ad7f") * drift * 0.12
    # fine hairline crazing + pores
    pores = (np.random.default_rng(14).random((n, n)) > 0.9993).astype(np.float32)
    rgb = rgb * (1 - gaussian_filter(pores, 0.7, mode="wrap")[..., None] * 0.4)
    grain = gaussian_filter(np.random.default_rng(15).random((n, n)).astype(np.float32), 0.7, mode="wrap")
    rgb = rgb * (1 + (grain[..., None] - 0.5) * 0.03)
    save_full(rgba(rgb, np.ones((n, n), np.float32)), f"{OUT}/dinding.webp", quality=74)
    Image.fromarray((np.clip(np.tile(rgb, (1, 2, 1)), 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/tm-dinding.png")
    clear()

if "pintu" in PARTS:
    W, H = 420, 760
    nx = Seq(40100)
    cx = W / 2
    # pointed horseshoe arch outline: rectangle below, arch above y=190
    def arch(x0, x1, ytop, yspring, ybot, over=1.12):
        r = (x1 - x0) / 2 * over; c_ = (x0 + x1) / 2
        pts = [(x0, ybot), (x0, yspring)]
        for k in range(1, 30):
            t = k / 30
            a = math.pi + t * math.pi
            # pointed: blend circle with a raised apex
            px = c_ + math.cos(a) * r * (1 - 0.06 * math.sin(t * math.pi))
            px = min(max(px, x0 - r * 0.12), x1 + r * 0.12)
            py = yspring + math.sin(a) * (yspring - ytop) * (1 + 0.08 * (1 - abs(t - .5) * 2) ** 3)
            pts.append((px, py))
        pts += [(x1, yspring), (x1, ybot)]
        return pts
    frame = shapes(W, H, [arch(20, 400, 20, 210, 756)], smooth=False)
    leaf = shapes(W, H, [arch(48, 372, 58, 222, 742)], smooth=False)
    rgbw = wood(W, H, nx())
    L = emboss(gaussian_filter(frame, 2) - leaf * 0.5, 2.0)
    art = rgba(rgbw * (0.55 + 0.8 * L[..., None]) * 0.82, frame)
    art = over(art, rgba(wood(W, H, nx()) * 0.98, leaf))
    # leaf split line, carved panels with 8-point star relief
    panels = []
    star_h = np.zeros((H, W), np.float32)
    for side in (0, 1):
        x0 = 66 if side == 0 else cx + 8
        x1 = cx - 8 if side == 0 else 354
        for (y0, y1) in [(250, 420), (440, 600), (620, 724)]:
            panels.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
            pc = ((x0 + x1) / 2, (y0 + y1) / 2); rr = min(x1 - x0, y1 - y0) * 0.34
            sq1 = [(pc[0] + math.cos(a) * rr, pc[1] + math.sin(a) * rr) for a in [math.pi / 4 + k * math.pi / 2 for k in range(4)]]
            sq2 = [(pc[0] + math.cos(a) * rr, pc[1] + math.sin(a) * rr) for a in [k * math.pi / 2 for k in range(4)]]
            st = shapes(W, H, [sq1, sq2], smooth=False)
            inner = shapes(W, H, [[(pc[0] + (x - pc[0]) * .55, pc[1] + (y - pc[1]) * .55) for x, y in sq1], [(pc[0] + (x - pc[0]) * .55, pc[1] + (y - pc[1]) * .55) for x, y in sq2]], smooth=False)
            star_h = np.maximum(star_h, st * 0.8 - inner * 0.35)
    # arch tympanum lattice (radiating ribs)
    tym = shapes(W, H, [arch(66, 354, 82, 226, 232)], smooth=False)
    ribs = strokes(W, H, [([(cx, 232), (cx + math.cos(a) * 200, 232 + math.sin(a) * 200)], 5, None) for a in np.linspace(math.pi + 0.15, math.tau - 0.15, 9)]) * tym
    pm = shapes(W, H, panels, smooth=False)
    height = leaf * 0.6 - pm * 0.25 + star_h * pm * 0.5 + ribs * 0.35 - tym * 0.2
    L = emboss(height, 1.6)
    art[..., :3] = art[..., :3] * (0.6 + 0.8 * L[..., None])
    split = np.zeros((H, W), np.float32); split[230:742, int(cx) - 2:int(cx) + 2] = 1
    art = shade(art, gaussian_filter(split, 1) * leaf, "#1a0c06", 0.8)
    art = shade(art, tym * (1 - ribs), "#24120a", 0.55)
    # brass studs along the frame edge and between panels, two ring knockers
    studs = []
    for y in range(250, 740, 30):
        studs += [(58, y, 5.5), (362, y, 5.5)]
    for x in range(78, 350, 30):
        studs += [(x, 432, 4.6), (x, 612, 4.6)]
    sm = circles(W, H, studs)
    art = over(art, soft_shadow(sm, "#120804", 1.5, 0.6, 1, 2))
    art = FO(art, sm, BRASS, seed=nx(), emboss=0.9, sparkle=0.2)
    rings = np.clip(circles(W, H, [(cx - 28, 520, 20), (cx + 28, 520, 20)]) - circles(W, H, [(cx - 28, 520, 15), (cx + 28, 520, 15)]), 0, 1)
    rings = np.maximum(rings, circles(W, H, [(cx - 28, 498, 6), (cx + 28, 498, 6)]))
    art = over(art, soft_shadow(rings, "#120804", 2, 0.6, 2, 3))
    art = FO(art, rings, BRASS, seed=nx(), emboss=0.9, sparkle=0.2)
    # threshold shadow at the foot
    art = shade(art, np.clip((np.mgrid[0:H, 0:W][0] - 690) / 70, 0, 1) * frame, "#1a0c06", 0.35)
    preview(art, "tm-pintu", tone=WALL)
    save(art, f"{OUT}/pintu.webp", max_w=320, quality=82)
    clear()

if "lentera" in PARTS:
    W, H = 300, 620
    nx = Seq(40200)
    cx = W / 2
    chain = strokes(W, H, [([(cx, 0), (cx, 96)], 3, None)])
    links = np.clip(ellipses(W, H, [(cx, y, 4, 8, 0) for y in range(6, 96, 14)]) - ellipses(W, H, [(cx, y, 2, 5.5, 0) for y in range(6, 96, 14)]), 0, 1)
    fin = shapes(W, H, [[(cx - 6, 140), (cx, 96), (cx + 6, 140)]], smooth=False) + circles(W, H, [(cx, 112, 8), (cx, 132, 6)])
    dome = shapes(W, H, [[(cx - 76, 252), (cx - 70, 214), (cx - 50, 180), (cx - 22, 156), (cx, 142), (cx + 22, 156), (cx + 50, 180), (cx + 70, 214), (cx + 76, 252)]])
    collar = shapes(W, H, [[(cx - 82, 250), (cx + 82, 250), (cx + 82, 266), (cx - 82, 266)]], smooth=False)
    body = shapes(W, H, [[(cx - 70, 266), (cx + 70, 266), (cx + 58, 450), (cx - 58, 450)]], smooth=False)
    base_ = shapes(W, H, [[(cx - 66, 450), (cx + 66, 450), (cx + 30, 498), (cx, 520), (cx - 30, 498)]])
    drop = shapes(W, H, [petal_pts(cx, 520, 34, 8, math.pi / 2, n=10)])
    metal = np.clip(np.maximum.reduce([fin, dome, collar, body, base_, drop]), 0, 1)
    # pierced pattern: arches on the body (3 visible facets), dots on dome and base
    holes = []
    for fx in (-40, 0, 40):
        holes.append([(cx + fx - 13, 436), (cx + fx - 13, 314), (cx + fx - 6, 296), (cx + fx, 288), (cx + fx + 6, 296), (cx + fx + 13, 314), (cx + fx + 13, 436)])
    hm = shapes(W, H, holes, smooth=False)
    facet_lines = strokes(W, H, [([(cx - 20, 268), (cx - 17, 450)], 3, None), ([(cx + 20, 268), (cx + 17, 450)], 3, None)])
    lattice = hatch(W, H, 0.8, 7, 0.32, 3) * hatch(W, H, -0.8, 7, 0.32, 4)
    open_body = hm * (1 - lattice * 0.0) * np.clip(1 - hatch(W, H, 0.78, 8, 0.25, 5) - hatch(W, H, -0.78, 8, 0.25, 6), 0, 1)
    dots = circles(W, H, [(cx + math.cos(a) * r, 220 + math.sin(a) * r * 0.5, 3.2) for r in (24, 46) for a in np.linspace(0, math.tau, 14 if r > 30 else 9, endpoint=False)] +
                   [(cx + x, 470, 3) for x in (-40, -24, -8, 8, 24, 40)] + [(cx + x, 486, 2.6) for x in (-24, -8, 8, 24)])
    holes_all = np.clip(open_body + dots * (dome + base_), 0, 1)
    # glow behind, then brass, then the lit holes
    halo = glow(np.clip(body + dome * 0.6, 0, 1), "#ffcf7a", radius=40, strength=0.6)
    art = halo
    shine = np.clip(1 - np.abs(np.mgrid[0:H, 0:W][1] - (cx - 26)) / 36, 0, 1) * 0.5
    brass = foil(metal, BRASS, seed=nx(), emboss=0.8, sparkle=0.15)
    brass = shade(brass, np.clip((np.mgrid[0:H, 0:W][1] - cx) / 80, 0, 1), "#3a2208", 0.45)
    brass = lighten(brass, shine * metal, "#f6dfa0", 0.4)
    brass = shade(brass, facet_lines * metal, "#4a2c0a", 0.6)
    brass[..., 3] *= 1 - holes_all
    lit = np.concatenate([np.ones((H, W, 3), np.float32) * hexarr("#ffe3a0") * (0.9 + 0.1 * fbm(W, H, nx(), 20, 2))[..., None], (holes_all * metal * 0.98)[..., None]], -1)
    art = over(art, lit)
    art = over(art, brass)
    ch = np.maximum(chain * 0.0, links)
    art = FO(art, np.maximum(links, strokes(W, H, [([(cx, 92), (cx, 100)], 3, None)])), "#8e6a30", seed=nx(), emboss=0.6)
    preview(art, "tm-lentera", tone=WALL)
    save(art, f"{OUT}/lentera.webp", max_w=200, quality=82)
    clear()


def weave(W, H, grid, cell, seed, fringe=0):
    """Woven wool from a pattern grid (list of strings, one char per knot). Returns RGBA."""
    gh, gw = len(grid), len(grid[0])
    idx = np.array([[ord(ch) for ch in row] for row in grid])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    jy = yy + (fbm(W, H, seed, 40, 2) - 0.5) * cell * 0.6
    jx = xx + (fbm(W, H, seed + 1, 40, 2) - 0.5) * cell * 0.3
    gy = np.clip((jy - fringe) // cell, 0, gh - 1).astype(int)
    gx = np.clip(jx // cell, 0, gw - 1).astype(int) % gw
    ch = idx[gy, gx]
    rgb = np.zeros((H, W, 3), np.float32)
    for k, col in WOOL.items():
        rgb[ch == ord(k)] = hexarr(col)
    rgb = gaussian_filter(rgb, (0.6, 0.6, 0))
    # weft ridges + wool fuzz + dye variation
    ridge = 0.5 + 0.5 * np.sin(yy / cell * math.tau * 1.0 + np.sin(xx / 3.0) * 0.6)
    fuzz = gaussian_filter(np.random.default_rng(seed + 2).random((H, W)).astype(np.float32), (0.6, 1.4))
    fuzz = (fuzz - fuzz.mean()) / (fuzz.std() + 1e-6)
    rgb = rgb * (0.84 + 0.2 * ridge[..., None]) * (1 + fuzz[..., None] * 0.05) * (0.94 + 0.1 * fbm(W, H, seed + 3, 70, 3)[..., None])
    a = np.zeros((H, W), np.float32); a[fringe:H - fringe] = 1
    a = displace(a, seed + 4, 1.5, 12)
    if fringe:
        fr = np.zeros((H, W), np.float32)
        for x in range(2, W, 6):
            ln = fringe * random.Random(x).uniform(0.7, 1.0)
            fr[int(fringe - ln):fringe, x:x + 3] = 1
            fr[H - fringe:int(H - fringe + ln), x:x + 3] = 1
        fr = gaussian_filter(fr, 0.6)
        rgb = rgb * (1 - fr[..., None]) + hexarr("#e8dcc4") * fr[..., None] * (0.85 + 0.15 * fuzz[..., None] * 0.3)
        a = np.maximum(a, fr)
    return rgba(rgb, a)


def berber_grid(cols, rows):
    g = [["c"] * cols for _ in range(rows)]
    mid = rows // 2
    for x in range(cols):
        g[1][x] = g[rows - 2][x] = "k"
        if (x // 2) % 2 == 0:
            g[3][x] = g[rows - 4][x] = "r"
    # diamond chain with a dot heart, zigzag rails
    P = 12
    for x in range(cols):
        u = x % P
        d = abs(u - P // 2)
        for y in range(5, rows - 5):
            dy = abs(y - mid)
            if dy + d == P // 2 - 1 or dy + d == P // 2 - 2:
                g[y][x] = "k"
            elif dy + d < 2:
                g[y][x] = "r"
            elif dy + d == 3 and (x + y) % 2 == 0:
                g[y][x] = "o"
        zz = 6 + (x % 6 if (x // 6) % 2 == 0 else 5 - x % 6) // 3
    return ["".join(r) for r in g]


if "permadani" in PARTS:
    W, H = 800, 170
    cell = 7
    grid = berber_grid(W // cell + 2, (H - 32) // cell)
    art = weave(W, H, grid, cell, 77, fringe=16)
    preview(art, "tm-permadani", tone=WALL)
    save(art, f"{OUT}/permadani.webp", max_w=800, quality=78)
    clear()

if "anyam" in PARTS:
    W, H = 420, 44
    cell = 4
    rows = H // cell
    g = []
    for y in range(rows):
        r = ""
        for x in range(W // cell + 2):
            u = x % 8; d = abs(u - 4)
            if y in (0, rows - 1):
                r += "k"
            elif abs(y - rows // 2) + d == 3:
                r += "r"
            elif abs(y - rows // 2) + d < 2:
                r += "o"
            else:
                r += "c"
        g.append(r)
    art = weave(W, H, g, cell, 88)
    preview(art, "tm-anyam", tone=WALL)
    save(art, f"{OUT}/anyam.webp", max_w=420, quality=82)
