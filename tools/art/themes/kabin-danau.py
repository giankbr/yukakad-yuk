"""Kabin Danau — opaque gouache, warm dawn: a log cabin with lit windows and chimney smoke on a pine-forest shore,
a wooden dock with a red canoe, mist lying on still water, layered blue pine ridges. Plus a separate drifting mist band,
a hanging lantern, a canoe ornament and a pine sprig.
Run: python3 -I kabin-danau.py [part ...]   parts: scene mist lantern canoe pine"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l4_lib import *
from scipy.ndimage import map_coordinates

OUT = outdir("kabin-danau")
PARTS = sys.argv[1:] or ["scene", "mist", "lantern", "canoe", "pine"]
PINE_D, PINE, PINE_M = "#1d332c", "#29463b", "#3f5e4d"
AMBER, AMBER_L = "#f0a53c", "#ffd98a"
CANOE, CANOE_D = "#b2452e", "#7e2c1d"
LOG, LOG_D, LOG_L = "#7a5233", "#4f331f", "#a5744a"


def reflect(layer, axis, H, W, squash=.8, fade=.75, seed=1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = yy - axis
    src = axis - d / squash
    rip = (fbm(W, H, seed, 8, 2) - .5) * 8 * np.clip(d / 40, 0, 1) + np.sin(yy * 1.3) * 1.4
    out = blank(W, H)
    for c in range(4):
        out[..., c] = map_coordinates(layer[..., c], [src, xx + rip], order=1, mode="constant")
    k = (d > 0) * np.clip(1 - d / (H - axis + 1), 0, 1) ** .6
    out[..., 3] *= k * fade
    return out


def pines(W, H, specs, rng):
    polys = []
    for x, by, h in specs:
        polys += pine_polys(x, by, h, rng, lean=rng.uniform(-.02, .02))
    return shapes(W, H, polys, smooth=False)


# ---------------------------------------------------------------- scene (cover painting, 800x980 -> 720x882)
if "scene" in PARTS:
    W, H = 800, 980
    WL = 600  # water line
    rng = random.Random(701); nx = Seq(701000)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#b9c6c9"), (.25, "#e9d6c3"), (.5, "#f6d2ac"), (.62, "#f3c8a0"), (1, "#f3c8a0")], seed=nx(), streak=.9)
    # low sun glow behind the far ridge
    sun = circles(W, H, [(560, 470, 46)])
    art = OV(art, sun, lambda m: glow(m, "#fff1d6", radius=40, strength=.6), pad=160)
    art = GP(art, sun, "#fff4de", "#ffe9c8", seed=nx(), rough=2, density=.8)
    # ridges (cool, pale) then far pines
    land = blank(W, H)
    for k, (base, amp, ca, cb) in enumerate([(470, 60, "#a9b4b8", "#9fabaf"), (520, 40, "#8a9ca0", "#80939a")]):
        pts = [(-20, H)] + [(x, base - amp * (.6 * math.sin(x / 140 + k * 2) + .4 * math.sin(x / 53 + k))) for x in range(-20, W + 40, 20)] + [(W + 20, H)]
        m = shapes(W, H, [pts], smooth=False) * (yy < WL + 2)
        land = OV(land, m, lambda mm, ca=ca, cb=cb: gouache_paint(mm, ca, cb, seed=nx(), rough=3, streak=.8))
    far = pines(W, H, [(x, 548 + rng.uniform(-8, 8), rng.uniform(40, 80)) for x in np.linspace(-10, W + 10, 52)], rng) * (yy < WL + 2)
    land = OV(land, far, lambda m: gouache_paint(m, "#6c8287", "#62777d", seed=nx(), rough=1.6))
    mid = pines(W, H, [(x, 600 + rng.uniform(-4, 6), rng.uniform(70, 140)) for x in np.linspace(-20, W + 20, 34)], rng)
    land = OV(land, mid, lambda m: gouache_paint(m, "#4b6560", "#42605a", seed=nx(), rough=1.6))
    # mist between ridges (in the land layer so it reflects)
    for y0, a in [(540, .55), (585, .5)]:
        mm = np.clip(1 - np.abs(yy - y0) / 22, 0, 1) * (0.6 + .4 * fbm(W, H, nx(), 70, 3))
        land = G(land, mm, "#f7ece0", seed=nx(), density=a, edge=0, bloom=.5, rough=10, feather=6)
    # cabin on the left shore
    cx, cb = 210, 606
    front = blank(W, H)
    shore = shapes(W, H, [[(-20, cb - 10), (150, cb - 18), (330, cb - 8), (380, cb + 2), (-20, cb + 16)]])
    front = OV(front, shore, lambda m: gouache_paint(m, "#3c4a35", "#33402e", seed=nx(), rough=3))
    body = shapes(W, H, [[(cx - 96, cb - 92), (cx + 96, cb - 92), (cx + 96, cb), (cx - 96, cb)]], smooth=False)
    land = OV(land, body, lambda m: gouache_paint(m, LOG, "#6c4829", seed=nx(), rough=1.2, streak=1.6))
    logs = strokes(W, H, [([(cx - 96, cb - 92 + i * 9.2), (cx + 96, cb - 92 + i * 9.2)], 2.2, None) for i in range(1, 10)])
    land = OV(land, logs * body, lambda m: gouache_paint(m, LOG_D, seed=nx(), rough=.6, density=.7))
    ends = circles(W, H, [(cx + s_ * 98, cb - 88 + i * 9.2, 4.6) for i in range(10) for s_ in (-1, 1)])
    land = OV(land, ends, lambda m: gouache_paint(m, LOG_L, seed=nx(), rough=.6))
    roof = shapes(W, H, [[(cx - 122, cb - 86), (cx, cb - 176), (cx + 122, cb - 86), (cx + 108, cb - 80), (cx, cb - 160), (cx - 108, cb - 80)]], smooth=False)
    gable = shapes(W, H, [[(cx - 100, cb - 88), (cx, cb - 160), (cx + 100, cb - 88)]], smooth=False)
    land = OV(land, gable, lambda m: gouache_paint(m, "#8b5e3a", "#7d5434", seed=nx(), rough=1, streak=1.5))
    boards = strokes(W, H, [([(cx - 90 + i * 12, cb - 88), (cx - 90 + i * 12, cb - 170)], 1.4, None) for i in range(16)]) * gable
    land = OV(land, boards, lambda m: gouache_paint(m, LOG_D, seed=nx(), rough=.5, density=.55))
    land = OV(land, roof, lambda m: gouache_paint(m, "#3a2c26", "#2e2420", seed=nx(), rough=1.4))
    snowline = strokes(W, H, [([(cx - 122, cb - 86), (cx, cb - 176), (cx + 122, cb - 86)], 2.6, None)])
    land = OV(land, snowline, lambda m: gouache_paint(m, "#d9a46b", seed=nx(), rough=.6, density=.6))
    chim = shapes(W, H, [[(cx + 48, cb - 160), (cx + 70, cb - 160), (cx + 70, cb - 116), (cx + 48, cb - 132)]], smooth=False)
    land = OV(land, chim, lambda m: gouache_paint(m, "#6d6a66", "#5b5856", seed=nx(), rough=1))
    # warm lit windows + door + porch
    wins = shapes(W, H, [[(cx - 76, cb - 66), (cx - 40, cb - 66), (cx - 40, cb - 30), (cx - 76, cb - 30)], [(cx + 40, cb - 66), (cx + 76, cb - 66), (cx + 76, cb - 30), (cx + 40, cb - 30)], [(cx - 14, cb - 140), (cx + 14, cb - 140), (cx + 14, cb - 108), (cx - 14, cb - 108)]], smooth=False)
    land = OV(land, wins, lambda m: glow(m, AMBER, radius=12, strength=.5), pad=50)
    land = OV(land, wins, lambda m: gouache_paint(m, AMBER_L, AMBER, seed=nx(), rough=.8))
    mull = strokes(W, H, [([(cx - 58, cb - 66), (cx - 58, cb - 30)], 2, None), ([(cx - 76, cb - 48), (cx - 40, cb - 48)], 2, None), ([(cx + 58, cb - 66), (cx + 58, cb - 30)], 2, None), ([(cx + 40, cb - 48), (cx + 76, cb - 48)], 2, None), ([(cx, cb - 140), (cx, cb - 108)], 1.6, None)])
    land = OV(land, mull, lambda m: gouache_paint(m, LOG_D, seed=nx(), rough=.4))
    door = shapes(W, H, [[(cx - 16, cb - 70), (cx + 16, cb - 70), (cx + 16, cb), (cx - 16, cb)]], smooth=False)
    land = OV(land, door, lambda m: gouache_paint(m, "#5a3a22", "#4a2f1c", seed=nx(), rough=.8))
    porch = shapes(W, H, [[(cx - 110, cb - 4), (cx + 110, cb - 4), (cx + 110, cb + 6), (cx - 110, cb + 6)]], smooth=False)
    front = OV(front, porch, lambda m: gouache_paint(m, "#5b3d26", seed=nx(), rough=.8))
    # dock: planks running into the water, posts
    dock = shapes(W, H, [[(300, cb + 2), (560, cb + 30), (560, cb + 40), (296, cb + 12)]], smooth=False)
    front = OV(front, dock, lambda m: gouache_paint(m, "#8a6544", "#7a573a", seed=nx(), rough=.8, streak=1.4))
    seams = strokes(W, H, [([(300 + i * 13, cb + 2 + i * 1.4), (298 + i * 13, cb + 12 + i * 1.4)], 1.2, None) for i in range(20)]) * dock
    front = OV(front, seams, lambda m: gouache_paint(m, "#4f3622", seed=nx(), rough=.3, density=.7))
    posts = strokes(W, H, [([(x, cb + 6 + (x - 300) * .108), (x, cb + 34 + (x - 300) * .108)], 4.5, None) for x in (330, 400, 470, 552)])
    front = OV(front, posts, lambda m: gouache_paint(m, "#3e2b1c", seed=nx(), rough=.6))
    # lantern on the dock end
    lp = strokes(W, H, [([(548, cb + 30), (548, cb - 16)], 3, None)])
    front = OV(front, lp, lambda m: gouache_paint(m, "#2b211b", seed=nx(), rough=.4))
    lamp = circles(W, H, [(548, cb - 22, 6)])
    front = OV(front, lamp, lambda m: glow(m, AMBER, radius=16, strength=.9), pad=70)
    front = OV(front, lamp, lambda m: gouache_paint(m, AMBER_L, seed=nx(), rough=.5))
    # near pines at the left edge and right edge
    near = pines(W, H, [(-6, cb + 26, 470), (52, cb + 10, 330), (380, cb + 4, 200), (412, cb + 6, 150), (760, cb + 16, 420), (816, cb + 20, 520), (700, cb + 10, 260)], rng)
    land = OV(land, near, lambda m: gouache_paint(m, PINE_D, PINE, seed=nx(), rough=2, streak=1))
    rim = near * np.clip((xx - 540) / 220, 0, 1) * (fbm(W, H, nx(), 6, 2) > .55)
    land = OV(land, rim, lambda m: gouache_paint(m, "#7a6a4a", seed=nx(), rough=1, density=.35))
    clear()
    # chimney smoke (soft watercolour)
    smoke = strokes(W, H, [(curve([(cx + 59, cb - 162), (cx + 70, cb - 220), (cx + 40, cb - 280), (cx + 80, cb - 350)], 40), 22, (.1, .6))])
    land = G(land, smoke, "#f1ebe4", "#dcd6d1", seed=nx(), density=.75, edge=.1, bloom=.6, rough=10, feather=6)
    art = over(art, land)
    # water: reflected sky + reflection of the land
    water = (yy >= WL).astype(np.float32)
    wat = painted_sky(W, H, [(0, "#f3c8a0"), (.6, "#f3c8a0"), (.66, "#d6c6b6"), (.8, "#93a7ab"), (1, "#6f878d")], seed=nx(), streak=1.6)
    wat[..., 3] = water
    art = over(art, wat)
    land_ref = reflect(land, WL + 4, H, W, seed=nx())
    land_ref[..., :3] = land_ref[..., :3] * .78 + np.array(hex_rgb("#5d7378"), np.float32) * .22
    art = over(art, land_ref)
    art = over(art, front)
    # sun path on the water + ripple highlights
    path = np.clip(1 - np.abs(xx - 560) / (40 + (yy - WL) * .35), 0, 1) * water * (fbm(W, H, nx(), 5, 2) > .55)
    art = GP(art, path, "#ffe6c0", seed=nx(), rough=1, density=.55)
    rip = strokes(W, H, [([(x, y), (x + rng.uniform(16, 60), y)], rng.uniform(1.2, 2.6)) for x, y in [(rng.uniform(0, W), rng.uniform(WL + 30, H)) for _ in range(90)]])
    art = GP(art, rip, "#f6e6d2", seed=nx(), rough=1, density=.55)
    # canoe floating by the dock + its reflection
    def canoe_mask(x, y, L, h):
        hull = [(x - L / 2, y - h * .7)] + [(x - L / 2 + L * t, y + h * math.sin(math.pi * t) * .9 - h * .05) for t in np.linspace(.05, .95, 14)] + [(x + L / 2, y - h * .7), (x + L * .35, y - h * .1), (x - L * .35, y - h * .1)]
        return shapes(W, H, [hull])
    cm = canoe_mask(470, cb + 70, 170, 16)
    cref = canoe_mask(470, cb + 92, 170, -12)
    art = G(art, cref, "#8e4a3a", seed=nx(), density=.4, edge=.1, rough=3)
    art = GP(art, cm, CANOE, "#a33c27", seed=nx(), rough=1)
    gun = strokes(W, H, [([(385, cb + 59), (470, cb + 62), (555, cb + 59)], 3, None)])
    art = GP(art, gun, CANOE_D, seed=nx(), rough=.4)
    pad = strokes(W, H, [([(440, cb + 48), (520, cb + 76)], 3, None)])
    art = GP(art, pad, "#d1a36a", seed=nx(), rough=.4)
    rope = strokes(W, H, [(curve([(396, cb + 62), (380, cb + 54), (352, cb + 40)], 10), 1.4, None)])
    art = GP(art, rope, "#e2cfa8", seed=nx(), rough=.3)
    # foreground reeds bottom-left
    reeds = strokes(W, H, [(curve([(x, H + 4), (x + rng.uniform(-6, 6), H - rng.uniform(60, 120) * .5), (x + rng.uniform(-14, 14), H - rng.uniform(60, 130))], 12), rng.uniform(2.4, 4), (.05, .7)) for x in list(np.linspace(-10, 150, 22)) + list(np.linspace(680, 810, 14))])
    art = GP(art, reeds, "#2d3a2c", "#3b4a36", seed=nx(), rough=1)
    art = add_grain(art, 707, .03)
    save_rgb(art, f"{OUT}/scene.webp", size=(720, 882), quality=76)
    prev(art, "kd-scene", bg="#ffffff")
    clear()

# ---------------------------------------------------------------- mist (drifting band, transparent 1000x220 -> 900)
if "mist" in PARTS:
    W, H = 1000, 220
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = Seq(711000)
    m = np.clip(1 - np.abs(yy - 110) / 80, 0, 1) ** 1.4 * (0.35 + .65 * fbm(W, H, nx(), 90, 4))
    m *= np.clip(np.minimum(xx, W - xx) / 160, 0, 1)
    a = blank(W, H)
    a = G(a, m, "#fbf4ea", "#f3ece6", seed=nx(), density=.9, edge=0, bloom=.6, rough=14, feather=10, gran=0)
    a[..., 3] *= .85
    save(a, f"{OUT}/mist.webp", max_w=900, quality=78)
    prev(a, "kd-mist", bg="#5d7378")
    clear()

# ---------------------------------------------------------------- lantern (hanging, 220x360 -> 160)
if "lantern" in PARTS:
    W, H = 220, 360
    nx = Seq(721000)
    a = blank(W, H)
    cx = 110
    glass = shapes(W, H, [[(cx - 46, 150), (cx + 46, 150), (cx + 40, 290), (cx - 40, 290)]], smooth=False)
    a = OV(a, glass, lambda m: glow(m, AMBER, radius=26, strength=.55), pad=90)
    a = OV(a, glass, lambda m: gouache_paint(m, "#ffd98a", "#f5b551", seed=nx(), rough=1, density=.9))
    flame = shapes(W, H, [petal_pts(cx, 258, 44, 11, -math.pi / 2, n=16)])
    a = OV(a, flame, lambda m: gouache_paint(m, "#fff4d4", "#ffe39a", seed=nx(), rough=.6))
    candle = shapes(W, H, [[(cx - 11, 262), (cx + 11, 262), (cx + 11, 290), (cx - 11, 290)]], smooth=False)
    a = OV(a, candle, lambda m: gouache_paint(m, "#f6ead2", "#e8d6b4", seed=nx(), rough=.5))
    frame = strokes(W, H, [([(cx - 48, 150), (cx - 41, 292)], 6, None), ([(cx + 48, 150), (cx + 41, 292)], 6, None),
                           ([(cx - 50, 148), (cx + 50, 148)], 7, None), ([(cx - 44, 292), (cx + 44, 292)], 8, None)])
    cap = shapes(W, H, [[(cx - 58, 148), (cx, 100), (cx + 58, 148)]], smooth=False)
    base = shapes(W, H, [[(cx - 52, 290), (cx + 52, 290), (cx + 34, 312), (cx - 34, 312)]], smooth=False)
    ring = strokes(W, H, [(arc_pts(cx, 84, 16, 0, math.tau, 24), 5, None), ([(cx, 0), (cx, 68)], 3, None)])
    metal = np.maximum.reduce([frame, cap, base, ring])
    a = OV(a, metal, lambda m: gouache_paint(m, "#2b2622", "#3a332d", seed=nx(), rough=1, streak=1))
    hi = strokes(W, H, [([(cx - 30, 118), (cx - 6, 104)], 2.4, None), ([(cx - 44, 160), (cx - 38, 280)], 1.6, None)])
    a = OV(a, hi, lambda m: gouache_paint(m, "#b9905a", seed=nx(), rough=.4, density=.7))
    save(a, f"{OUT}/lantern.webp", max_w=160)
    prev(a, "kd-lantern", bg="#1d332c")
    clear()

# ---------------------------------------------------------------- canoe (ornament, 420x130 -> 300)
if "canoe" in PARTS:
    W, H = 420, 130
    nx = Seq(731000)
    a = blank(W, H)
    hull = [(20, 52)] + [(20 + 380 * t, 66 + 36 * math.sin(math.pi * t) ** .8) for t in np.linspace(.04, .96, 16)] + [(400, 52), (330, 70), (90, 70)]
    hm = shapes(W, H, [hull])
    a = OV(a, hm, lambda m: gouache_paint(m, CANOE, "#a03a26", seed=nx(), rough=1, streak=1.2))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    shade = hm * np.clip((yy - 80) / 24, 0, 1)
    a = G(a, shade, CANOE_D, seed=nx(), density=.6, edge=.2, rough=2)
    gun = strokes(W, H, [(curve([(18, 50), (120, 68), (300, 68), (402, 50)], 30), 5, None)])
    a = OV(a, gun, lambda m: gouache_paint(m, "#5a2a1c", seed=nx(), rough=.4))
    pad = strokes(W, H, [([(110, 22), (300, 96)], 5, None)])
    blade = shapes(W, H, [petal_pts(290, 92, 70, 13, .37, n=14)])
    a = OV(a, np.maximum(pad, blade), lambda m: gouache_paint(m, "#d3a467", "#c08f55", seed=nx(), rough=.5, streak=1.2))
    water = strokes(W, H, [([(40 + i * 40, 112 + (i % 2) * 6), (70 + i * 40, 112 + (i % 2) * 6)], 3, None) for i in range(9)])
    a = OV(a, water, lambda m: gouache_paint(m, "#7d97a0", seed=nx(), rough=1, density=.8))
    save(a, f"{OUT}/canoe.webp", max_w=300)
    prev(a, "kd-canoe", bg="#f6efe4")
    clear()

# ---------------------------------------------------------------- pine (small tree for nodes / divider, 160x220 -> 110)
if "pine" in PARTS:
    W, H = 160, 220
    nx = Seq(741000)
    rng = random.Random(741)
    a = blank(W, H)
    pm = shapes(W, H, pine_polys(80, 206, 196, rng, tiers=7), smooth=False)
    a = OV(a, pm, lambda m: gouache_paint(m, PINE_M, PINE, seed=nx(), rough=1.4, streak=1.2))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = G(a, pm * (xx > 82), PINE_D, seed=nx(), density=.55, edge=.2, rough=2)
    snow = pm * (xx < 70) * (fbm(W, H, nx(), 5, 2) > .6)
    a = OV(a, snow, lambda m: gouache_paint(m, "#8fa784", seed=nx(), rough=.6, density=.6))
    save(a, f"{OUT}/pine.webp", max_w=110)
    prev(a, "kd-pine", bg="#f6efe4")
    clear()
