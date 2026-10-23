"""Sengkang Sutra — shimmering Sengkang silk (lipa' sabbe checks with sheen), a wooden loom, floating houses on Danau
Tempe at dusk, golden silk cocoons. Silk rendered thread by thread, scenes in gouache + watercolour.
Run: python3 -I sengkang-sutra.py [part ...]  parts: silk drape lake loom divider cocoon
Assets -> public/themes/art/sengkang-sutra/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n2_lib import *

OUT = outdir("sengkang-sutra")
PARTS = sys.argv[1:] or ["silk", "drape", "lake", "loom", "divider", "cocoon"]

JADE, JADE_D, JADE_L = "#0f625c", "#093f3e", "#1b7d72"
GOLD, GOLD_L, GOLD_D = "#d6a43e", "#f0cf7a", "#9a6f22"
CREAM, CORAL, PLUM = "#f1e3c2", "#c9573f", "#3b1f33"

# balo' lobang style check: broad jade ground, gold double bars, fine cream + coral pinstripes
SEQ = [(JADE, 14), (JADE_D, 2), (GOLD, 3), (JADE, 2), (GOLD, 3), (JADE_D, 2), (JADE, 14), (CREAM, 1), (JADE, 3), (CORAL, 1), (JADE, 3), (CREAM, 1)]


def silk_rgb(w, h, seed=7, thread=2.0):
    return weave(w, h, SEQ, SEQ, seed=seed, warp=thread, weft=thread, twill=True, slub=0.25, sheen=1.0, fibre=0.0)


def silk():
    n = sum(n for _, n in SEQ)
    w = h = int(n * 2.0 * 4)
    rgb = silk_rgb(w, h)
    save_rgb(opaque(rgb), f"{OUT}/silk.webp", quality=80)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(f"{PREV}/ss-silk.png")


def drape():
    """A silk swag hung across the top: three scallops, vertical folds, sheen on the fold crests, gold fringe."""
    W, H = 780, 330
    n = sum(n for _, n in SEQ)
    tile = silk_rgb(int(n * 1.6 * 3), int(n * 1.6 * 3), seed=9, thread=1.6)
    cloth = tile_to(tile, W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # scallop lower edge: three swags
    sw = 3
    u = (xx / W) * sw
    ph = u % 1.0
    sag = 150 + 120 * np.sin(ph * math.pi) ** 1.2
    # fold field: folds radiate from the hanging points
    fold = np.sin(ph * math.pi * 7 + (yy / H) * 2.0) * (0.4 + 0.6 * np.sin(ph * math.pi))
    # displace the cloth texture along the fold (gives the bunching)
    dx = fold * 6
    dy = (sag - 150) * (yy / np.maximum(sag, 1)) * 0.6
    cl = warp_img(cloth, dx, -dy)
    shade = 0.72 + 0.28 * (0.5 + 0.5 * np.cos(ph * math.pi * 7 + (yy / H) * 2.0 + 0.6))
    shade *= 0.85 + 0.15 * np.sin(ph * math.pi)
    shade *= 1 - 0.25 * np.clip((yy - sag + 50) / 50, 0, 1)  # underside of each swag darker
    crest = np.clip(np.cos(ph * math.pi * 7 + (yy / H) * 2.0 + 0.6), 0, 1) ** 8
    rgb = shade_rgb(cl, shade) + crest[..., None] * 0.22 * np.array([1.0, 0.95, 0.8])
    m = (yy < sag).astype(np.float32)
    m = gaussian_filter(m, 0.8)
    # top hem (a jade band, slightly darker) and gold piping along the swag edge
    art = rgba(rgb, m)
    hem = (yy < 22).astype(np.float32)
    art = over(art, rgba(shade_rgb(cl, 0.6 * np.ones_like(shade)), hem))
    pip_items = []
    for k in range(sw):
        pts = [(x, 150 + 120 * math.sin(((x / W) * sw % 1.0) * math.pi) ** 1.2 - 3) for x in np.linspace(k * W / sw, (k + 1) * W / sw, 60)]
        pip_items.append((pts, 7, None))
    pip = strokes(W, H, pip_items)
    art = OV(art, pip, lambda mm: foil(mm, GOLD, seed=3, emboss=0.8, sparkle=0.3))
    # fringe: gold threads hanging from the edge
    rng = random.Random(2)
    fr = []
    for x in np.arange(2, W, 4.5):
        y0 = 150 + 120 * math.sin(((x / W) * sw % 1.0) * math.pi) ** 1.2
        L = 26 + rng.uniform(-3, 3)
        fr.append(([(x, y0), (x + rng.gauss(0, .6), y0 + L * .5), (x + rng.gauss(0, 1.2), y0 + L)], 1.6, (0.0, 0.3)))
    fm = strokes(W, H, fr)
    art = OV(art, fm, lambda mm: foil(mm, "#c9963a", seed=5, emboss=0.3, sparkle=0.1))
    tassel = circles(W, H, [(k * W / sw, 156, 9) for k in range(sw + 1)])
    art = OV(art, tassel, lambda mm: foil(mm, GOLD, seed=7, emboss=0.9, sparkle=0.3))
    preview(art, "ss-drape", bg=JADE_D)
    save_full(art, f"{OUT}/drape.webp", quality=80)


def house(art, W, H, x, base, w, h, nx, rng, lit=True):
    """Floating house on a bamboo raft: plank walls, Bugis gable (timpa' laja), little porch, warm window."""
    raft = shapes(W, H, [[(x - w * 0.62, base - 6), (x + w * 0.62, base - 6), (x + w * 0.58, base + 6), (x - w * 0.6, base + 6)]], smooth=False)
    art = GP(art, raft, "#5c4a33", "#6b573b", seed=nx(), rough=1.0, streak=0.6)
    poles = strokes(W, H, [([(x - w * 0.62 + k * w * 0.124, base - 5), (x - w * 0.62 + k * w * 0.124 + 3, base + 5)], 1.4, None) for k in range(11)])
    art = G(art, poles * raft, "#2d2318", seed=nx(), density=0.45, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    wall = shapes(W, H, [[(x - w / 2, base - 6), (x + w / 2, base - 6), (x + w / 2, base - h), (x - w / 2, base - h)]], smooth=False)
    art = GP(art, wall, "#8b6b45", "#9c7b52", seed=nx(), rough=1.0, streak=0.8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    planks = wall * (np.abs(((xx - x) / 5.0) % 1 - 0.5) < 0.08)
    art = G(art, planks, "#4a3826", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    art = G(art, wall * np.clip((x - xx) / w + 0.3, 0, 1), "#3a2a1c", seed=nx(), density=0.4, edge=0.1, bloom=0.2, rough=1)
    if lit:
        win = shapes(W, H, [[(x + w * 0.08, base - h * 0.75), (x + w * 0.32, base - h * 0.75), (x + w * 0.32, base - h * 0.35), (x + w * 0.08, base - h * 0.35)]], smooth=False)
        art = over(art, glow(win, "#ffcf7a", radius=8, strength=0.5))
        art = GP(art, win, "#ffcf6e", "#ffe3a0", seed=nx(), rough=0.5)
    door = shapes(W, H, [[(x - w * 0.3, base - 6), (x - w * 0.1, base - 6), (x - w * 0.1, base - h * 0.75), (x - w * 0.3, base - h * 0.75)]], smooth=False)
    art = GP(art, door, "#2e2218", seed=nx(), rough=0.5)
    # roof: steep gable with overhang + crossed ridge horns
    rh = h * 0.95
    roof = shapes(W, H, [[(x - w * 0.66, base - h + 4), (x, base - h - rh), (x + w * 0.66, base - h + 4)]], smooth=False)
    art = GP(art, roof, "#3c2e22", "#4b3a2a", seed=nx(), rough=1.2, streak=0.8)
    thatch = roof * (np.abs(((yy - (base - h)) / 4.0) % 1 - 0.5) < 0.12)
    art = G(art, thatch, "#6e5638", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    gable = shapes(W, H, [[(x - w * 0.36, base - h), (x, base - h - rh * 0.62), (x + w * 0.36, base - h)]], smooth=False)
    art = GP(art, gable, "#a47d4f", seed=nx(), rough=0.8)
    tiers = strokes(W, H, [([(x - w * 0.36 * f, base - h - rh * 0.62 * (1 - f)), (x + w * 0.36 * f, base - h - rh * 0.62 * (1 - f))], 1.6, None) for f in (0.45, 0.7, 0.9)]) * gable
    art = G(art, tiers, "#3c2e22", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.5, feather=0.5)
    horns = strokes(W, H, [([(x, base - h - rh), (x - w * 0.14, base - h - rh - h * 0.28)], 2.2, (0.0, 0.5)), ([(x, base - h - rh), (x + w * 0.14, base - h - rh - h * 0.28)], 2.2, (0.0, 0.5))])
    art = GP(art, horns, "#2a2018", seed=nx(), rough=0.5)
    return art


def lake():
    W, H = 780, 700
    nx = Seq(900)
    rng = random.Random(8)
    hz = 380
    sky = painted_sky(W, hz + 10, [(0, "#3d4f6a"), (0.3, "#7b6c84"), (0.62, "#d08a6e"), (0.86, "#efb072"), (1, "#f6cd8c")], seed=4, streak=0.5, grain=0.25)
    art = blank(W, H)
    art[:hz + 10] = sky
    sun = circles(W, H, [(250, hz - 28, 26)])
    art = over(art, glow(sun, "#ffd998", radius=40, strength=0.5))
    art = G(art, sun, "#ffe2a6", "#fff0c8", seed=nx(), density=0.9, edge=0.2, bloom=0, rough=1)
    clouds = shapes(W, H, [deform(ellipse_pts(cx_, cy_, rx_, ry_, 12), rng, 2, 0.1) for cx_, cy_, rx_, ry_ in [(560, 210, 170, 14), (640, 236, 110, 10), (120, 160, 140, 12), (420, 120, 120, 9)]])
    art = G(art, clouds, "#e7a07e", "#c97f72", seed=nx(), density=0.5, edge=0.2, bloom=0.4, rough=6, feather=3)
    hills = shape_mask(W, H, curve([(-20, hz + 2), (60, hz - 30), (160, hz - 44), (300, hz - 20), (420, hz - 34), (560, hz - 58), (700, hz - 40), (800, hz - 22), (800, hz + 4)], 60) + [(800, hz + 6), (-20, hz + 6)])
    art = G(art, hills, "#6e5a72", "#7c6478", seed=nx(), density=0.8, edge=0.3, bloom=0.3, rough=4)
    # reeds / far shoreline trees
    reeds = strokes(W, H, [([(x, hz + 2), (x + rng.gauss(0, 1.5), hz - rng.uniform(6, 22))], 1.6, (0.0, 0.6)) for x in rng.sample(range(0, 780), 140)])
    art = G(art, reeds, "#4b3d52", seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    # water: mirror the sky/hills about the horizon with ripples
    top = art[:, :, :3].copy()
    water = reflect(top, hz + 3, H - hz - 3, seed=5, ripple=2.5, fade=0.7, tint="#3a3f58", tint_amt=0.5)
    art[hz + 3:] = opaque(water)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # floating houses + lopi, each with its own rippled reflection under its base
    HOUSES = [(110, hz + 46, 120, 50, True), (300, hz + 26, 86, 36, False), (470, hz + 62, 140, 60, True), (660, hz + 36, 100, 42, True)]
    def mirror_under(layer, base):
        n = fbm(W, H, 77, 10, 2) - 0.5
        ys = np.clip(2 * base - yy, 0, H - 1)
        xs = np.clip(xx + np.sin(yy * 0.7 + n * 5) * 2.2, 0, W - 1)
        ref = np.stack([map_coordinates(layer[..., c], [ys, xs], order=1) for c in range(4)], -1)
        ref[..., 3] *= (yy > base) * 0.5 * np.clip(1 - (yy - base) / 90, 0, 1)
        ref[..., :3] = ref[..., :3] * 0.55 + col3("#3a3f58") * 0.45
        return ref
    for (x, b, w, h, lit) in sorted(HOUSES, key=lambda t: t[1]):
        lay = house(blank(W, H), W, H, x, b, w, h, nx, rng, lit)
        art = over(art, mirror_under(lay, b + 6))
        art = over(art, lay)
    bl = blank(W, H)
    boat = shapes(W, H, [[(560, hz + 112), (690, hz + 112), (676, hz + 122), (574, hz + 122)]], smooth=False)
    bl = GP(bl, boat, "#2c221a", seed=nx(), rough=0.8)
    pole = strokes(W, H, [([(600, hz + 112), (648, hz + 40)], 2, (0.0, 0.0)), ([(600, hz + 112), (585, hz + 140)], 2, (0.0, 0.0))])
    bl = GP(bl, pole, "#2c221a", seed=nx(), rough=0.4)
    art = over(art, mirror_under(bl, hz + 122))
    art = over(art, bl)
    rip = []
    for k in range(90):
        y = hz + 20 + (k / 90) ** 1.2 * (H - hz - 20)
        L = rng.uniform(20, 110)
        x = rng.uniform(-30, W)
        rip.append(([(x, y), (x + L, y + rng.gauss(0, .5))], 1.0 + (y - hz) / H * 2.5, (0.3, 0.3)))
    art = G(art, strokes(W, H, rip), "#f3c48a", seed=nx(), density=0.3, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    glint = strokes(W, H, [([(250 + rng.gauss(0, 10 + (y - hz) * 0.12), y), (250 + rng.gauss(0, 10 + (y - hz) * .12) + 14, y)], 1.6, (0.3, 0.3)) for y in np.linspace(hz + 4, H - 20, 60)])
    art = G(art, glint, "#ffe0a0", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=0.6, feather=0.6)
    art = add_grain(art, 6, 0.012)
    art[..., 3] = 1
    save_rgb(art, f"{OUT}/lake.webp", quality=78)
    preview(art, "ss-lake")


def loom():
    """Backstrap/frame loom (walida, beam, warp) with a length of check silk taking shape."""
    W, H = 560, 440
    nx = Seq(1100)
    rng = random.Random(4)
    art = blank(W, H)
    # warp threads fanning from the far beam to the woven cloth
    far_y, near_y = 60, 250
    items = []
    for k in range(70):
        t = k / 69
        xa = 140 + t * 280
        xb = 120 + t * 320
        items.append(([(xa, far_y), (xb, near_y)], 1.0, None))
    wm = strokes(W, H, items)
    art = G(art, wm, "#d9b860", "#e9cf86", seed=nx(), density=0.8, edge=0.1, bloom=0, rough=0.4, feather=0.4)
    # woven cloth (perspective-ish trapezoid of real silk texture)
    n = sum(n for _, n in SEQ)
    tile = silk_rgb(int(n * 1.4 * 3), int(n * 1.4 * 3), seed=13, thread=1.4)
    cloth = tile_to(tile, W, H)
    cm = shapes(W, H, [[(120, near_y), (440, near_y), (470, 380), (90, 380)]], smooth=False)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = 0.8 + 0.2 * np.clip((yy - near_y) / 130, 0, 1)
    art = over(art, rgba(shade_rgb(cloth, shade), gaussian_filter(cm, 0.7)))
    # reed / beater (walida) across the warp
    beater = shapes(W, H, [[(100, near_y - 14), (460, near_y - 14), (462, near_y + 2), (98, near_y + 2)]], smooth=False)
    art = GP(art, beater, "#7a4e2a", "#8d5d33", seed=nx(), rough=1.0, streak=1.0)
    art = G(art, beater * (yy > near_y - 6), "#4a2c16", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=0.5)
    # far beam + breast beam
    fb = shapes(W, H, [[(110, far_y - 12), (450, far_y - 12), (452, far_y + 4), (108, far_y + 4)]], smooth=False)
    art = GP(art, fb, "#6b4426", "#7d5230", seed=nx(), rough=1.0, streak=1.0)
    bb = shapes(W, H, [[(60, 380), (500, 380), (504, 406), (56, 406)]], smooth=False)
    art = GP(art, bb, "#6b4426", "#7d5230", seed=nx(), rough=1.0, streak=1.0)
    art = G(art, bb * (yy > 394), "#3b2312", seed=nx(), density=0.4, edge=0.1, bloom=0, rough=0.5)
    # side posts with carved finials
    for x in (88, 472):
        post = shapes(W, H, [[(x - 10, 30), (x + 10, 30), (x + 12, 420), (x - 12, 420)]], smooth=False)
        art = GP(art, post, "#5a381e", "#6b4426", seed=nx(), rough=1.0, streak=1.0)
        fin = shapes(W, H, [ellipse_pts(x, 24, 15, 18, 12)])
        art = GP(art, fin, "#6b4426", seed=nx(), rough=0.8)
        art = G(art, fin * (xx > x), "#3b2312", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.5)
    # shuttle (taropong) resting across the warp with gold bobbin
    sh = shapes(W, H, [[(170, 214), (300, 202), (380, 212), (300, 226)]])
    art = GP(art, sh, "#8f5b2c", "#a96d36", seed=nx(), rough=0.6)
    bob = shapes(W, H, [ellipse_pts(276, 213, 30, 7, 10, -0.06)])
    art = OV(art, bob, lambda mm: foil(mm, GOLD, seed=4, emboss=0.7, sparkle=0.2))
    preview(art, "ss-loom", bg=CREAM)
    save(art, f"{OUT}/loom.webp", max_w=360, quality=84)


def divider():
    """Golden silk thread unspooling from a small wooden shuttle in a lazy wave."""
    W, H = 600, 80
    art = blank(W, H)
    pts = [(x, 40 + 9 * math.sin((x - 60) / 520 * math.tau * 1.5) * (1 - abs(x - 300) / 330)) for x in np.linspace(40, 560, 120)]
    th = strokes(W, H, [(pts, 3.2, (0.1, 0.25))])
    art = OV(art, th, lambda mm: foil(mm, GOLD, seed=6, emboss=0.6, sparkle=0.2))
    sh = shapes(W, H, [[(246, 40), (276, 31), (324, 31), (354, 40), (324, 49), (276, 49)]], smooth=False)
    art = GP(art, sh, "#6b4426", "#7d5230", seed=12, rough=0.6)
    bob = shapes(W, H, [ellipse_pts(300, 40, 15, 5, 10)])
    art = OV(art, bob, lambda mm: foil(mm, GOLD_L, seed=8, emboss=0.7, sparkle=0.2))
    preview(art, "ss-divider", bg=CREAM)
    save(art, f"{OUT}/divider.webp", max_w=360, quality=84)


def cocoon():
    """A golden silk cocoon with fine wrapped threads (timeline node / emblem)."""
    W, H = 200, 220
    rng = random.Random(6)
    art = blank(W, H)
    body = shapes(W, H, [deform(ellipse_pts(100, 112, 62, 88, 18, 0.2), rng, 1, 0.03)])
    art = GP(art, body, "#e2b754", "#f1d68a", seed=21, rough=0.8, streak=0.3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = G(art, body * np.clip((xx - 110) / 50, 0, 1), "#a8781f", seed=22, density=0.5, edge=0.1, bloom=0.2, rough=1)
    items = []
    for k in range(70):
        a = rng.uniform(0, math.tau)
        cx_, cy_ = 100 + rng.gauss(0, 18), 112 + rng.gauss(0, 30)
        items.append((arc_pts(cx_, cy_, rng.uniform(20, 70), a, a + rng.uniform(0.6, 1.8), 16, rng.uniform(0.3, 1.0)), 0.9, (0.1, 0.1)))
    fib = strokes(W, H, items) * body
    art = G(art, fib, "#fff3c8", seed=23, density=0.5, edge=0.1, bloom=0, rough=0.4, feather=0.4)
    art = G(art, strokes(W, H, items[::2]) * body, "#9a6f22", seed=24, density=0.3, edge=0.1, bloom=0, rough=0.4, feather=0.4)
    hl = shapes(W, H, [ellipse_pts(78, 78, 16, 30, 12, 0.3)])
    art = OV(art, hl, lambda m: rgba(np.ones(m.shape + (3,), np.float32), gaussian_filter(m, 6) * 0.45))
    preview(art, "ss-cocoon", bg=JADE)
    save(art, f"{OUT}/cocoon.webp", max_w=100, quality=86)


for p in PARTS:
    globals()[p]()
    clear()
kb_total(OUT)
