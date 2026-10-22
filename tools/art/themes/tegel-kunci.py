"""Tegel Kunci — vintage Indonesian cement tiles (tegel kunci) from an old house terrace: pressed pigment layers in faded
teal, terracotta and mustard on chalky cream, decades of wear (scuffs, pits, chipped corners, dirt in the grout), plus a
jendela krepyak (louvered shutter) with flaking paint and a kursi rotan. No figures, no calligraphy.
Run: python3 -I tegel-kunci.py [part ...]   parts: tegel ubin lis jendela kursi"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f3_lib import *

OUT = outdir("tegel-kunci")
PARTS = sys.argv[1:] or ["tegel", "ubin", "lis", "jendela", "kursi"]
CREAM, TEAL, TEAL_D, TERRA, MUST, CHAR = "#ece2cc", "#4c8a86", "#2f6664", "#b65a3c", "#cf9d3a", "#4a4440"


def tile_masks(W, H, x0, y0, s):
    """Pattern geometry for one tile whose top-left is (x0, y0), size s."""
    c = (x0 + s / 2, y0 + s / 2)
    corners = [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]
    big = circles(W, H, [(cx, cy, s * 0.4) for cx, cy in corners])
    ring_in = circles(W, H, [(cx, cy, s * 0.31) for cx, cy in corners])
    core = circles(W, H, [(cx, cy, s * 0.17) for cx, cy in corners])
    # scalloped edge on the big corner disc
    sc = []
    for cx, cy in corners:
        for k in range(24):
            a = k * math.tau / 24
            sc.append((cx + math.cos(a) * s * 0.4, cy + math.sin(a) * s * 0.4, s * 0.035))
    big = np.maximum(big, circles(W, H, sc))
    sq = rect(W, H, x0, y0, x0 + s, y0 + s)
    teal = np.clip(big - ring_in, 0, 1) * sq
    cream_ring = np.clip(ring_in - core, 0, 1) * sq
    dots = []
    for cx, cy in corners:
        for k in range(16):
            a = k * math.tau / 16
            dots.append((cx + math.cos(a) * s * 0.245, cy + math.sin(a) * s * 0.245, s * 0.018))
    must_dots = circles(W, H, dots) * sq
    terra_core = core * sq
    # centre flower: 8 petals terracotta, 8 mustard leaves between, teal heart
    petals = [petal_pts(c[0], c[1], s * 0.27, s * 0.1, k * math.tau / 8 + math.pi / 8, n=16) for k in range(8)]
    leaves = [petal_pts(c[0], c[1], s * 0.2, s * 0.05, k * math.tau / 8, n=14) for k in range(8)]
    pet = shapes(W, H, petals)
    lev = np.clip(shapes(W, H, leaves) - pet, 0, 1)
    heart = circles(W, H, [(c[0], c[1], s * 0.06)])
    pet = np.clip(pet - heart, 0, 1)
    # lozenges at edge midpoints (pair up with the neighbour tile)
    mids = [(c[0], y0, 0), (c[0], y0 + s, 0), (x0, c[1], 1), (x0 + s, c[1], 1)]
    loz = []
    for mx, my, o in mids:
        d1, d2 = s * 0.1, s * 0.045
        loz.append([(mx - (d2 if o == 0 else d1), my - (d1 if o == 0 else d2)), (mx + (d2 if o == 0 else d1), my + (d1 if o == 0 else d2))])
    lz = shapes(W, H, [[(mx, my - (s * 0.1 if o == 0 else s * 0.045)), (mx + (s * 0.045 if o == 0 else s * 0.1), my), (mx, my + (s * 0.1 if o == 0 else s * 0.045)), (mx - (s * 0.045 if o == 0 else s * 0.1), my)] for mx, my, o in mids], smooth=False) * sq
    return dict(teal=teal, must=np.clip(must_dots + lev + lz, 0, 1), terra=np.clip(terra_core + pet, 0, 1), heart=heart, cream_ring=cream_ring)


def paint_tiles(W, H, s, nx, rng, grout=3.0, wrap=True):
    art = solid(W, H, CREAM)
    art[..., :3] *= (0.95 + 0.07 * (wrap_noise(W, H, nx(), 30) if wrap else fbm(W, H, nx(), 60, 3)))[..., None]
    for ty in range(0, H, s):
        for tx in range(0, W, s):
            m = tile_masks(W, H, tx, ty, s)
            art = over(art, cement_paint(m["teal"], TEAL, seed=nx(), fade=0.28))
            art = over(art, cement_paint(m["terra"], TERRA, seed=nx(), fade=0.25))
            art = over(art, cement_paint(m["must"], MUST, seed=nx(), fade=0.22))
            art = over(art, cement_paint(m["heart"], TEAL_D, seed=nx(), fade=0.2))
            clear()
    # per-tile tone (some tiles were replaced or sun-faded)
    for ty in range(0, H, s):
        for tx in range(0, W, s):
            k = rng.uniform(-0.05, 0.05)
            art[ty:ty + s, tx:tx + s, :3] *= 1 + k
    N = (lambda sd, sg: wrap_noise(W, H, sd, sg)) if wrap else (lambda sd, sg: fbm(W, H, sd, sg * 3, 3))
    # foot-traffic wear: chalky lightening in broad patches + fine scuffs
    wear = np.clip((N(nx(), 40) - 0.45) * 1.6, 0, 1)
    art[..., :3] = art[..., :3] * (1 - wear[..., None] * 0.22) + col_arr("#efe8d8") * wear[..., None] * 0.22
    g = np.random.default_rng(nx()).random((H, W)).astype(np.float32)
    scuff = gaussian_filter(g, (0.6, 7), mode="wrap") - gaussian_filter(g, 4, mode="wrap")
    scuff2 = gaussian_filter(g, (6, 0.7), mode="wrap") - gaussian_filter(g, 4, mode="wrap")
    art[..., :3] *= (1 + (scuff + scuff2 * 0.6)[..., None] * 0.7)
    pits = gaussian_filter((np.random.default_rng(nx()).random((H, W)) > 0.9988).astype(np.float32), 0.8, mode="wrap") * 1.5
    art[..., :3] *= (1 - np.clip(pits, 0, 0.5)[..., None])
    dirt = np.clip((N(nx(), 22) - 0.6) * 2.5, 0, 1)
    art[..., :3] *= (1 - dirt[..., None] * 0.1)
    # grout lines + bevel + chipped corners
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = np.minimum(xx % s, s - (xx % s)); dy = np.minimum(yy % s, s - (yy % s))
    d = np.minimum(dx, dy)
    jag = (N(nx(), 3) - 0.5) * 1.4
    gr = np.clip((grout / 2 + jag - d) * 1.2, 0, 1)
    bev = np.clip(1 - np.abs(d - grout / 2 - 1.5) / 2.0, 0, 1) * (1 - gr)
    art[..., :3] = art[..., :3] * (1 - bev[..., None] * 0.12)
    chip = np.zeros((H, W), np.float32)
    for ty in range(0, H + 1, s):
        for tx in range(0, W + 1, s):
            if rng.random() < 0.55:
                r = rng.uniform(4, 11)
                ang = rng.uniform(0, math.tau)
                pts = deform(ellipse_pts(tx + math.cos(ang) * 3, ty + math.sin(ang) * 3, r, r * 0.7, 9, ang), rng, 2, 0.25)
                chip = np.maximum(chip, shapes(W, H, [pts], smooth=False))
                for ox in (-W, W):
                    chip = np.maximum(chip, shapes(W, H, [[(px + ox, py) for px, py in pts]], smooth=False))
                for oy in (-H, H):
                    chip = np.maximum(chip, shapes(W, H, [[(px, py + oy) for px, py in pts]], smooth=False))
    gm = np.clip(gr + chip, 0, 1)
    grc = col_arr("#8c8274") * (0.85 + 0.25 * N(nx(), 2)[..., None])
    art[..., :3] = art[..., :3] * (1 - gm[..., None]) + grc * gm[..., None]
    return np.clip(art, 0, 1)


if "tegel" in PARTS:
    nx = Seq(7100); rng = random.Random(71)
    S = 240
    art = paint_tiles(2 * S, 2 * S, S, nx, rng)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/tegel.png")
    save_rgb(art, f"{OUT}/tegel.webp", size=(400, 400), quality=78)

if "ubin" in PARTS:
    nx = Seq(7300); rng = random.Random(73)
    S = 300; W = H = 360
    t = paint_tiles(S, S, S, nx, rng, grout=0.0, wrap=False)
    art = blank(W, H)
    off = 30
    sq = rect(W, H, off, off, off + S, off + S)
    chip = shapes(W, H, [deform([(off + S - 30, off - 4), (off + S + 4, off - 4), (off + S + 4, off + 40), (off + S - 6, off + 22), (off + S - 18, off + 14)], rng, 2, 0.2)], smooth=False)
    face = np.clip(sq - chip, 0, 1)
    art = over(art, soft_shadow(face, "#3a2a20", blur=8, strength=0.35, dx=6, dy=8))
    side = np.clip(np.roll(np.roll(face, 4, 0), 3, 1) - face, 0, 1)
    art = over(art, flat(side, "#a59a88", 1.0))
    layer = np.zeros((H, W, 4), np.float32)
    layer[off:off + S, off:off + S] = t
    layer[..., 3] = face * layer[..., 3]
    art = over(art, layer)
    prev(art, "ubin", tone="#f3ead8")
    save(art, f"{OUT}/ubin.webp", max_w=220, quality=84)

if "lis" in PARTS:
    nx = Seq(7500); rng = random.Random(75)
    s = 180; W, H = 3 * s, s // 2
    art = solid(W, H, CREAM)
    art[..., :3] *= (0.95 + 0.07 * fbm(W, H, nx(), 60, 3))[..., None]
    band_t = rect(W, H, 0, 6, W, 12)
    band_b = rect(W, H, 0, H - 12, W, H - 6)
    scal = []; fl = []; lv = []
    for k in range(6):
        cx = k * s / 2 + s / 4
        scal.append((cx, H - 12, s * 0.2))
        fl.extend(petal_pts(cx, H * 0.46, s * 0.12, s * 0.04, a, n=12) for a in (-math.pi / 2, -math.pi / 2 + 1.1, -math.pi / 2 - 1.1))
        lv.append((cx + s / 4, H * 0.5, s * 0.03))
    arc = np.clip(circles(W, H, scal) - circles(W, H, [(x, y, r - s * 0.05) for x, y, r in scal]), 0, 1) * rect(W, H, 0, 0, W, H - 12)
    art = over(art, cement_paint(np.clip(band_t + band_b, 0, 1), TEAL, seed=nx(), fade=0.25))
    art = over(art, cement_paint(arc, TEAL, seed=nx(), fade=0.3))
    art = over(art, cement_paint(shapes(W, H, fl), TERRA, seed=nx(), fade=0.22))
    art = over(art, cement_paint(circles(W, H, lv), MUST, seed=nx(), fade=0.2))
    wear = np.clip((fbm(W, H, nx(), 50, 3) - 0.45) * 1.6, 0, 1)
    art[..., :3] = art[..., :3] * (1 - wear[..., None] * 0.2) + col_arr("#efe8d8") * wear[..., None] * 0.2
    g = np.random.default_rng(nx()).random((H, W)).astype(np.float32)
    art[..., :3] *= (1 + (gaussian_filter(g, (0.6, 7)) - gaussian_filter(g, 4))[..., None] * 0.6)
    xx = np.arange(W)[None, :].astype(np.float32)
    gr = np.clip(1.6 - np.minimum(xx % s, s - xx % s), 0, 1) * np.ones((H, 1), np.float32)
    art[..., :3] = art[..., :3] * (1 - gr[..., None] * 0.7) + col_arr("#8c8274") * gr[..., None] * 0.7
    # irregular hand-set edges
    m = rect(W, H, 2, 2, W - 2, H - 2)
    art[..., 3] = np.clip((gaussian_filter(displace(m, nx(), 1.2, 8), 0.6) - 0.3) * 2.4, 0, 1)
    prev(art, "lis", tone="#f3ead8")
    save(art, f"{OUT}/lis.webp", max_w=360, quality=82)

if "jendela" in PARTS:
    nx = Seq(7700); rng = random.Random(77)
    W, H = 220, 600
    art = blank(W, H)
    PAINT, PAINT_D, WOODC = "#5f9a8e", "#3c6f66", "#9a7550"
    frame = np.clip(rect(W, H, 10, 10, W - 10, H - 10) - rect(W, H, 34, 34, W - 34, H - 34), 0, 1)
    rail = rect(W, H, 34, H * 0.48, W - 34, H * 0.48 + 26)
    art = over(art, soft_shadow(rect(W, H, 10, 10, W - 10, H - 10), "#2a2018", blur=6, strength=0.35, dx=4, dy=5))
    body = np.clip(frame + rail, 0, 1)
    art = over(art, wood(rect(W, H, 10, 10, W - 10, H - 10), WOODC, "#6e5034", seed=nx(), angle=1.5708, grain=5))
    louvers = rect(W, H, 34, 34, W - 34, H - 34) * (1 - rail)
    art = over(art, gouache_paint(np.clip(body + louvers, 0, 1), PAINT, PAINT_D, seed=nx(), rough=0.6, streak=0.9))
    # louver slats: each slat lit on top, shadowed gap below
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    ph = (yy - 34) % 18 / 18
    slat_shade = np.where(ph < 0.7, 1.04 - ph * 0.25, 0.55 + (ph - 0.7) * 0.6)
    art[..., :3] *= np.where(louvers[..., None] > 0.5, slat_shade[..., None], 1.0)
    edge = np.clip((np.abs(ph - 0.02) < 0.04).astype(np.float32) * louvers, 0, 1)
    art = over(art, flat(edge, "#d7ece2", 0.5))
    # frame bevels
    inner = outline(rect(W, H, 34, 34, W - 34, H - 34), 3) * body
    art = over(art, flat(inner, "#24453f", 0.45))
    # flaking paint revealing wood + old cream undercoat
    flake = np.clip((fbm(W, H, nx(), 14, 3) - 0.72) * 6, 0, 1) * np.clip(art[..., 3], 0, 1)
    flake *= np.clip((fbm(W, H, nx(), 70, 2) - 0.35) * 3, 0, 1)
    under = flake * np.clip((fbm(W, H, nx(), 6, 2) - 0.4) * 4, 0, 1)
    art = over(art, flat(flake, "#e8dfc8", 0.9))
    art = over(art, wood(under, WOODC, "#6e5034", seed=nx(), angle=1.5708, grain=4))
    art = over(art, flat(outline(np.clip(flake * 2, 0, 1), 1.2) * (art[..., 3] > 0.5), "#2a3a34", 0.35))
    # hinge + latch
    for hy in (80, H - 80):
        art = GP(art, rect(W, H, W - 16, hy - 16, W - 4, hy + 16), "#3a3632", "#24211e", seed=nx(), rough=0.3)
    art = GP(art, circles(W, H, [(30, H * 0.48 + 13, 6)]), "#c7a35a", "#8a6a2a", seed=nx(), rough=0.3)
    prev(art, "jendela", tone="#f3ead8")
    save(art, f"{OUT}/jendela.webp", max_w=170, quality=82)

if "kursi" in PARTS:
    nx = Seq(7900); rng = random.Random(79)
    W, H = 520, 560
    art = blank(W, H)
    RAT, RAT_D, RAT_L = "#c58f4e", "#8a5a2a", "#e3b878"
    # floor shadow
    art = G(art, shapes(W, H, [deform(ellipse_pts(260, 520, 210, 22, 16), rng, 2, 0.1)]), "#6a5444", seed=nx(), density=0.35, edge=0.1, bloom=0.2, rough=4)
    # cane webbing (back + seat): woven hexagonal cane = 3 line directions
    back = shapes(W, H, [[(150, 120), (370, 120), (360, 320), (160, 320)]], smooth=True)
    seat = shapes(W, H, [[(110, 330), (410, 330), (440, 392), (80, 392)]], smooth=False)
    web = np.clip(back + seat, 0, 1)
    art = G(art, web, "#e8cf9e", "#d6b47a", seed=nx(), density=0.55, edge=0.2, bloom=0.2, rough=1)
    hx = np.maximum.reduce([hatch(W, H, a, 7.5, 0.26, nx(), 0.4) for a in (0.0, 1.047, 2.094)])
    holes = 1 - hx
    art = over(art, flat(web * hx, RAT_L, 0.9))
    art = over(art, flat(web * hx * hatch(W, H, 0.6, 3, 0.2, nx(), 0.3), RAT, 0.35))
    art = over(art, flat(web * np.clip(holes - 0.3, 0, 1), "#5a4030", 0.5))
    # bentwood rattan frame: thick rounded poles
    poles = [
        ([(150, 330), (138, 220), (150, 118), (200, 92), (260, 86), (320, 92), (370, 118), (382, 220), (370, 330)], 18),
        ([(100, 392), (96, 470), (92, 520)], 16), ([(420, 392), (426, 470), (432, 520)], 16),
        ([(160, 400), (164, 470), (168, 505)], 12), ([(360, 400), (356, 470), (352, 505)], 12),
        ([(80, 392), (440, 392)], 16), ([(110, 330), (410, 330)], 12),
        ([(60, 300), (100, 286), (140, 300)], 14), ([(380, 300), (420, 286), (460, 300)], 14),
        ([(70, 300), (74, 340), (90, 392)], 12), ([(450, 300), (446, 340), (430, 392)], 12),
        ([(98, 470), (164, 470)], 9), ([(356, 470), (424, 470)], 9),
    ]
    pm = strokes(W, H, [(curve(p, 40), w, (0.0, 0.0)) for p, w in poles])
    art = GP(art, pm, RAT, RAT_D, seed=nx(), rough=0.5, streak=1.0)
    # rounded-pole shading + wrapped binding at joints
    sh = np.clip(pm - np.roll(pm, -4, 0), 0, 1)
    art = over(art, flat(gaussian_filter(sh, 1.5), RAT_D, 0.5))
    hi = np.clip(pm - np.roll(pm, 4, 0), 0, 1) * pm
    art = over(art, flat(gaussian_filter(hi, 1.0), "#f2d49c", 0.55))
    for jx, jy in ((150, 330), (370, 330), (100, 392), (420, 392), (80, 300), (440, 300)):
        b = np.clip(circles(W, H, [(jx, jy, 13)]) * hatch(W, H, 1.2, 3.4, 0.45, nx(), 0.2), 0, 1)
        art = over(art, flat(b, "#7a4a22", 0.75))
    art = G(art, pm * light_mask(H, W, 500, 600, 380), "#5a3418", seed=nx(), density=0.3, edge=0, bloom=0.2, rough=1)
    # a batik cushion on the seat (kawung-free, simple stripes)
    cush = shapes(W, H, [deform([(150, 318), (370, 318), (392, 352), (128, 352)], rng, 1, 0.05)])
    art = GP(art, cush, "#2f6664", "#24504e", seed=nx(), rough=0.8)
    art = over(art, flat(cush * hatch(W, H, 0.0, 9, 0.18, nx(), 0.6), "#e8dcc0", 0.55))
    prev(art, "kursi", tone="#f3ead8")
    save(art, f"{OUT}/kursi.webp", max_w=320, quality=82)
