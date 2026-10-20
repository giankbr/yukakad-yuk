"""Arena Legenda — painted fantasy arena backdrop (gouache + ink, warm lit colosseum, ember sky), spinning rune ring,
gold-foil laurel crest (rank), foil shield (season badges), seamless dark canvas tile.
Run: python3 -I /tmp/pen/art/themes/arena-legenda.py [cover|rune|crest|shield|canvas]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _p4_lib import *  # noqa

T = "arena-legenda"
D = outdir(T)
nxt = Seeds(300)
rng = random.Random(11)
GOLD, GOLD_L, GOLD_D = "#c9a24b", "#f0d48a", "#8f6b2a"
CYAN = "#39c5f3"


def tower(W, H, x, base_y, wd, ht, rng, roof=True):
    """Castle tower silhouette with crenellations + pennant."""
    m = shape_mask(W, H, deform([(x - wd / 2, base_y), (x - wd / 2, base_y - ht), (x + wd / 2, base_y - ht), (x + wd / 2, base_y)], rng, 2, .01), smooth=False)
    # crenellations
    n = max(3, int(wd / 10))
    for i in range(n):
        if i % 2 == 0:
            cx = x - wd / 2 + wd * (i + 0.5) / n
            m = np.maximum(m, shape_mask(W, H, [(cx - wd / n / 2, base_y - ht + 2), (cx - wd / n / 2, base_y - ht - 8), (cx + wd / n / 2, base_y - ht - 8), (cx + wd / n / 2, base_y - ht + 2)], smooth=False))
    if roof:
        m = np.maximum(m, shape_mask(W, H, deform([(x - wd * .6, base_y - ht - 6), (x, base_y - ht - wd * 1.1), (x + wd * .6, base_y - ht - 6)], rng, 2, .02), smooth=False))
        m = np.maximum(m, stroke_mask(W, H, [(x, base_y - ht - wd * 1.1), (x, base_y - ht - wd * 1.1 - 26)], 2.0, (0.1, 0.1)))
    return m


def cover():
    W, H = 640, 1400
    rng.seed(5)
    art = painted_sky(W, H, [(0, "#05091a"), (0.16, "#0b1535"), (0.3, "#142457"), (0.4, "#2b2e5e"), (0.45, "#4a3a52"), (0.49, "#1a1f3f"), (0.62, "#0c1230"), (1, "#060a1c")], seed=nxt(), streak=1.0, grain=0.7)
    # warm horizon haze (arena fire-light) + cool portal glow higher up behind the VS block
    hz = shape_mask(W, H, ellipse_pts(W * .5, H * .455, 420, 70, 24))
    art = over(art, glow(hz, "#c9843c", radius=60, strength=0.42))
    pg = shape_mask(W, H, ellipse_pts(W * .5, H * .26, 260, 200, 24))
    art = over(art, glow(pg, "#2a4f8f", radius=90, strength=0.3))
    # drifting cloud / smoke bands
    for (y, x0, x1, th, col, d) in [(0.14, -0.1, 0.55, 16, "#1e3266", 0.22), (0.2, 0.5, 1.1, 12, "#1b2d5e", 0.2), (0.34, -0.1, 0.5, 14, "#2c3570", 0.22),
                                    (0.38, 0.45, 1.1, 18, "#3a3a6b", 0.22), (0.43, 0.0, 1.0, 26, "#6a4e4e", 0.2)]:
        pts = curve([(W * x0, H * y + rng.uniform(-8, 8)), (W * (x0 + x1) / 2, H * y - rng.uniform(4, 14)), (W * x1, H * y + rng.uniform(-8, 8))], 50)
        m = gaussian_filter(stroke_mask(W, H, pts, th, (0.4, 0.4)), 2)
        art = over(art, pigment(m, col, mix(col, "#7f8bc0", .25), seed=nxt(), density=d, edge=0.2, bloom=0.5, gran=0.2, feather=3, rough=14, mottle=0.8))
    # stars
    dots = [(rng.uniform(0, W), rng.uniform(0, H * 0.4), rng.choice([0.7, 0.9, 1.1, 1.4])) for _ in range(90)]
    dm = dots_mask(W, H, dots)
    art = over(art, gouache_paint(dm, "#e9eefc", "#bfd0f5", seed=nxt(), rough=0.5, streak=0.1, density=0.8))
    # far mountains
    for k, (by, amp, c1, c2) in enumerate([(0.445, 52, "#1b2452", "#2a3270"), (0.47, 34, "#141b45", "#1b2352")]):
        m = shape_mask(W, H, ridge_pts(W, H, by, amp, rng, n=10))
        layer = gouache_paint(m, c1, c2, seed=nxt(), rough=3, streak=0.7)
        rim = np.clip(m - np.roll(gaussian_filter(m, 2.0), 5, axis=0), 0, 1)
        layer = tint(layer, gaussian_filter(rim, 1.5), "#8a5a4a", 0.35 - k * 0.1)
        art = over(art, layer)
    # the arena: a wide ring of walls with arched openings, flanked by towers; warm light in the arches
    base = H * 0.515
    wall = np.zeros((H, W), np.float32)
    # back curve of the ring (lower, lighter) then front wall (taller)
    back = shape_mask(W, H, deform([(-10, base - 20), (-10, base - 96), (W * .2, base - 118), (W * .5, base - 126), (W * .8, base - 118), (W + 10, base - 96), (W + 10, base - 20)], rng, 2, .01))
    front = shape_mask(W, H, deform([(-10, base + 6), (-10, base - 70), (W * .25, base - 84), (W * .5, base - 88), (W * .75, base - 84), (W + 10, base - 70), (W + 10, base + 6)], rng, 2, .01))
    layer_b = gouache_paint(back, "#1d2659", "#262f6a", seed=nxt(), rough=2.5, streak=0.6)
    art = over(art, layer_b)
    # lit arches on the back ring
    arch_b = np.zeros((H, W), np.float32)
    for i in range(21):
        x = W * (0.02 + 0.96 * i / 20) + rng.uniform(-2, 2)
        y = base - 108
        arch_b = np.maximum(arch_b, shape_mask(W, H, [(x - 4, y + 12), (x - 4, y - 1), (x, y - 6), (x + 4, y - 1), (x + 4, y + 12)]))
    art = over(art, glow(arch_b, "#e8a35a", radius=6, strength=0.5))
    art = over(art, gouache_paint(arch_b, "#f1b25f", "#d98a3a", seed=nxt(), rough=0.8, density=0.9))
    layer_f = gouache_paint(front, "#121a44", "#1a2255", seed=nxt(), rough=2.5, streak=0.6)
    # stone courses in the front wall as faint ink lines
    courses = np.zeros((H, W), np.float32)
    for j in range(5):
        y = base - 70 + j * 15
        pts = [(x, y - 14 * math.sin((x / W - 0.5) * math.pi) ** 2 + rng.uniform(-1, 1)) for x in np.linspace(-10, W + 10, 30)]
        courses = np.maximum(courses, stroke_mask(W, H, pts, 1.2, (0.05, 0.05)))
    layer_f = over(layer_f, pigment(courses * front, "#0a1030", seed=nxt(), density=0.35, edge=0, bloom=0, rough=1, feather=0.5))
    art = over(art, layer_f)
    arch_f = np.zeros((H, W), np.float32)
    for i in range(15):
        x = W * (0.04 + 0.92 * i / 14) + rng.uniform(-2, 2)
        y = base - 52 + 6 * math.sin((i / 14 - 0.5) * math.pi) ** 2
        arch_f = np.maximum(arch_f, shape_mask(W, H, [(x - 7, y + 24), (x - 7, y - 1), (x, y - 9), (x + 7, y - 1), (x + 7, y + 24)]))
    # crenellated top edge on the front wall + warm rim light on it
    cren = np.zeros((H, W), np.float32)
    for i in range(30):
        x = W * (i + 0.5) / 30
        if i % 2 == 0:
            y = base - 88 + 4 * math.sin((x / W - 0.5) * math.pi) ** 2
            cren = np.maximum(cren, shape_mask(W, H, [(x - 8, y + 4), (x - 8, y - 8), (x + 8, y - 8), (x + 8, y + 4)], smooth=False))
    art = over(art, gouache_paint(cren, "#121a44", "#1a2255", seed=nxt(), rough=1.5, streak=0.4))
    top_rim = np.clip(np.maximum(front, cren) - np.roll(gaussian_filter(np.maximum(front, cren), 1.5), 4, axis=0), 0, 1)
    art = over(art, pigment(gaussian_filter(top_rim, 1.2), "#b97a45", "#e0a060", seed=nxt(), density=0.5, edge=0, bloom=0, rough=1, feather=0.6))
    art = over(art, glow(arch_f, "#f0a650", radius=10, strength=0.55))
    art = over(art, gouache_paint(arch_f, "#f6c270", "#e0903c", seed=nxt(), rough=0.8, density=0.95))
    # central gatehouse: a wide block with a big lit portal and two small turrets
    gx = W * .5
    gate = shape_mask(W, H, deform([(gx - 58, base + 4), (gx - 58, base - 118), (gx + 58, base - 118), (gx + 58, base + 4)], rng, 2, .008), smooth=False)
    for i in range(7):
        if i % 2 == 0:
            cx_ = gx - 58 + 116 * (i + 0.5) / 7
            gate = np.maximum(gate, shape_mask(W, H, [(cx_ - 8, base - 116), (cx_ - 8, base - 128), (cx_ + 8, base - 128), (cx_ + 8, base - 116)], smooth=False))
    gl_ = gouache_paint(gate, "#0f1740", "#182050", seed=nxt(), rough=2, streak=0.6)
    gl_ = shade(gl_, gate, light=(-0.6, -0.4), k=0.22, blur=5, hi="#4a4d86", lo="#06091c")
    art = over(art, gl_)
    portal = shape_mask(W, H, [(gx - 22, base + 2), (gx - 22, base - 50), (gx, base - 74), (gx + 22, base - 50), (gx + 22, base + 2)])
    art = over(art, glow(portal, "#f0a650", radius=18, strength=0.7))
    art = over(art, gouache_paint(portal, "#ffd98a", "#f0b05a", seed=nxt(), rough=0.8, density=0.97))
    gwin = np.zeros((H, W), np.float32)
    for (dx, dy) in [(-38, -92), (38, -92), (-38, -70), (38, -70), (0, -100)]:
        gwin = np.maximum(gwin, shape_mask(W, H, [(gx + dx - 3, base + dy + 7), (gx + dx - 3, base + dy - 3), (gx + dx, base + dy - 6), (gx + dx + 3, base + dy - 3), (gx + dx + 3, base + dy + 7)]))
    art = over(art, gouache_paint(gwin, "#ffd27a", seed=nxt(), rough=0.4, density=0.95))
    # towers with pennants
    tw = np.zeros((H, W), np.float32)
    for (x, wd, ht) in [(W * .08, 58, 120), (W * .92, 58, 120), (W * .31, 36, 84), (W * .69, 36, 84)]:
        tw = np.maximum(tw, tower(W, H, x, base - 40, wd, ht, rng))
    tl = gouache_paint(tw, "#0e1538", "#161d4c", seed=nxt(), rough=2, streak=0.6)
    tl = shade(tl, tw, light=(-0.6, -0.4), k=0.25, blur=5, hi="#4a4d86", lo="#06091c")
    art = over(art, tl)
    win = np.zeros((H, W), np.float32)
    for (x, ht) in [(W * .08, 120), (W * .92, 120), (W * .31, 84), (W * .69, 84)]:
        for j in range(3):
            y = base - 40 - ht * (0.25 + 0.25 * j)
            win = np.maximum(win, shape_mask(W, H, [(x - 3, y + 7), (x - 3, y - 3), (x, y - 6), (x + 3, y - 3), (x + 3, y + 7)]))
    art = over(art, glow(win, "#f3b35f", radius=4, strength=0.4))
    art = over(art, gouache_paint(win, "#ffd27a", seed=nxt(), rough=0.4, density=0.95))
    pen = np.zeros((H, W), np.float32)
    for (x, wd, ht) in [(W * .08, 58, 120), (W * .92, 58, 120), (W * .31, 36, 84), (W * .69, 36, 84)]:
        top = base - 40 - ht - wd * 1.1 - 24
        pen = np.maximum(pen, shape_mask(W, H, deform([(x, top), (x + 22 + rng.uniform(-4, 6), top + 6), (x, top + 13)], rng, 2, .05), smooth=False))
    art = over(art, gouache_paint(pen, "#c9a24b", "#a87f33", seed=nxt(), rough=1, density=0.95))
    # arena floor: dark flagstone plane with perspective lines + a faint glowing crack ring
    floor = shape_mask(W, H, [(-10, base), (W + 10, base), (W + 10, H + 10), (-10, H + 10)], smooth=False)
    fl = gouache_paint(floor, "#0a0f2a", "#121a3e", seed=nxt(), rough=1.5, streak=1.0)
    grid = np.zeros((H, W), np.float32)
    for j in range(14):   # receding rows
        t = j / 13
        y = base + 10 + (H - base) * t ** 1.7
        grid = np.maximum(grid, stroke_mask(W, H, [(-10, y + rng.uniform(-2, 2)), (W / 2, y + rng.uniform(-2, 2)), (W + 10, y + rng.uniform(-2, 2))], 1.3 + t * 1.5, (0.02, 0.02)))
    for i in range(11):   # converging columns
        x0 = W * (-0.4 + 1.8 * i / 10)
        grid = np.maximum(grid, stroke_mask(W, H, [(W * .5 + (x0 - W * .5) * 0.12, base + 10), (x0, H + 20)], 1.4, (0.02, 0.02)))
    fl = over(fl, pigment(grid * floor, "#263371", "#1a2558", seed=nxt(), density=0.35, edge=0, bloom=0, rough=1.5, feather=0.6, holes=0.25))
    art = over(art, fl)
    pool = gaussian_filter(shape_mask(W, H, ellipse_pts(W * .5, base + 30, 360, 40, 20)), 16)
    art = over(art, pigment(pool, "#b87a3a", "#e0a050", seed=nxt(), density=0.3, edge=0, bloom=0.5, gran=0.3, feather=5, rough=16, mottle=0.9))
    # embers / drifting sparks (gold) with glow
    emb = [(rng.uniform(0, W), rng.uniform(H * .2, H * .6), rng.choice([1.0, 1.3, 1.6, 2.2])) for _ in range(60)]
    em = dots_mask(W, H, emb)
    art = over(art, glow(em, "#f0a650", radius=5, strength=0.45))
    art = over(art, gouache_paint(em, "#ffd27a", "#f0a650", seed=nxt(), rough=0.4, density=0.9))
    # low mist over the floor front
    mist = gaussian_filter(shape_mask(W, H, ellipse_pts(W * .5, H * .56, 420, 40, 20)), 18)
    art = over(art, pigment(mist, "#2a3b7a", "#3a4a8f", seed=nxt(), density=0.4, edge=0, bloom=0.6, gran=0.2, feather=6, rough=20, mottle=1.0))
    art[..., 3] = 1
    save_rgb(art, f"{D}/cover.webp", q=80)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/al-cover.png")


def rune():
    S = 520
    c = S / 2
    rng.seed(21)
    art = blank(S, S)
    outer = ring_mask(S, S, c, c, 240, 5, rng, 1.2)
    inner = ring_mask(S, S, c, c, 196, 2.2, rng, 0.8)
    inner2 = ring_mask(S, S, c, c, 150, 1.6, rng, 0.8)
    # rune ticks between the two outer rings
    ticks = np.zeros((S, S), np.float32)
    for i in range(36):
        a = i / 36 * math.tau
        r0, r1 = (204, 232) if i % 3 == 0 else (212, 224)
        ticks = np.maximum(ticks, stroke_mask(S, S, [(c + math.cos(a) * r0, c + math.sin(a) * r0), (c + math.cos(a) * r1, c + math.sin(a) * r1)], 2.2 if i % 3 == 0 else 1.4, (0.1, 0.1)))
    # rune glyphs around the inner band: small angular strokes
    gl = np.zeros((S, S), np.float32)
    for i in range(16):
        a = i / 16 * math.tau + 0.1
        r = 173
        px, py = c + math.cos(a) * r, c + math.sin(a) * r
        ca, sa = math.cos(a), math.sin(a)
        segs = rng.randint(2, 4)
        pts = [(0, -11)]
        for _ in range(segs):
            pts.append((pts[-1][0] + rng.uniform(-8, 8), pts[-1][1] + rng.uniform(5, 9)))
        pts = [(px + x * -sa + y * ca, py + x * ca + y * sa) for x, y in pts]
        gl = np.maximum(gl, stroke_mask(S, S, pts, 2.6, (0.1, 0.1)))
    # hexagram-ish inner geometry
    geo = np.zeros((S, S), np.float32)
    for k in range(2):
        tri = [(c + math.cos(k * math.pi / 4 + j * math.pi / 2 - math.pi / 2) * 150, c + math.sin(k * math.pi / 4 + j * math.pi / 2 - math.pi / 2) * 150) for j in range(4)]
        for a, b in zip(tri, tri[1:] + tri[:1]):
            geo = np.maximum(geo, stroke_mask(S, S, [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for t in np.linspace(0, 1, 12)], 1.5, (0.05, 0.05)))
    goldm = np.maximum(outer, ticks)
    cyanm = union(inner, inner2, gl, geo)
    art = over(art, glow(goldm, GOLD, radius=10, strength=0.25))
    art = over(art, foil(goldm, GOLD, seed=nxt(), emboss=0.5, sparkle=0.1))
    art = over(art, glow(cyanm, CYAN, radius=8, strength=0.4))
    art = over(art, pigment(cyanm, "#9bebff", CYAN, seed=nxt(), density=0.75, edge=0.25, bloom=0.15, rough=0.8, feather=0.5, holes=0.12))
    preview(art, f"{PREV}/al-rune.png", "#0a1128")
    save(art, f"{D}/rune.webp", max_w=440, q=80, trim=False)


def laurel(W, H, cx, cy, r, side, rng, n=8):
    """One laurel branch: leaves along an arc on one side (side=-1 left, 1 right)."""
    m = np.zeros((H, W), np.float32)
    a0, a1 = (math.pi * 0.95, math.pi * 1.95) if side < 0 else (math.pi * 0.05, math.pi * -0.95)
    # stem
    arc = arc_pts(cx, cy, r, math.pi / 2 + (0.08 if side < 0 else -0.08), math.pi / 2 + side * math.pi * 0.95, 40)
    stem = stroke_mask(W, H, arc, 2.6, (0.05, 0.25))
    m = np.maximum(m, stem)
    for i in range(n):
        t = (i + 0.5) / n
        a = math.pi / 2 + side * math.pi * 0.9 * t
        px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
        tangent = a + side * math.pi / 2       # direction of travel along the branch (towards the top)
        L = r * (0.3 - 0.08 * t)
        for sgn in (-1, 1):
            ang = tangent + sgn * 0.55 + rng.gauss(0, 0.07)
            rr = r + sgn * 2
            qx, qy = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            m = np.maximum(m, shape_mask(W, H, petal_pts(qx, qy, L, L * 0.3, ang, n=12)))
    return m


def crest():
    W, H = 400, 230
    rng.seed(33)
    cx, cy = W / 2, H * 0.52
    wreath = np.maximum(laurel(W, H, cx, cy, 92, -1, rng), laurel(W, H, cx, cy, 92, 1, rng))
    # shield with a star in the middle
    sh = shape_mask(W, H, deform([(cx - 36, cy - 44), (cx + 36, cy - 44), (cx + 36, cy), (cx, cy + 46), (cx - 36, cy)], rng, 2, .01))
    sh_in = shape_mask(W, H, [(cx - 27, cy - 35), (cx + 27, cy - 35), (cx + 27, cy - 3), (cx, cy + 33), (cx - 27, cy - 3)])
    star = shape_mask(W, H, [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * (18 if i % 2 == 0 else 8), cy - 4 + math.sin(-math.pi / 2 + i * math.pi / 5) * (18 if i % 2 == 0 else 8)) for i in range(10)], smooth=False)
    chevrons = np.zeros((H, W), np.float32)
    for k in range(2):
        y = cy + 12 + k * 9
        chevrons = np.maximum(chevrons, stroke_mask(W, H, [(cx - 16, y), (cx, y + 7), (cx + 16, y)], 2.2, (0.1, 0.1)))
    rim = sub(sh, sh_in)
    foilm = union(wreath, rim, star, chevrons)
    art = blank(W, H)
    # dark enamel inside the shield
    art = over(art, gouache_paint(sh_in, "#0d1736", "#152052", seed=nxt(), rough=1, density=0.92))
    art = over(art, glow(foilm, GOLD, radius=6, strength=0.2))
    f = foil(foilm, GOLD, seed=nxt(), emboss=0.7, sparkle=0.2)
    # leaf veins as slightly darker lines
    art = over(art, f)
    preview(art, f"{PREV}/al-crest.png", "#13204a")
    save(art, f"{D}/crest.webp", max_w=320, q=82)


def shield():
    W = H = 120
    rng.seed(44)
    cx, cy = 60, 58
    sh = shape_mask(W, H, deform([(cx - 40, cy - 44), (cx + 40, cy - 44), (cx + 40, cy + 2), (cx, cy + 50), (cx - 40, cy + 2)], rng, 2, .012))
    sh_in = shape_mask(W, H, [(cx - 30, cy - 34), (cx + 30, cy - 34), (cx + 30, cy - 2), (cx, cy + 36), (cx - 30, cy - 2)])
    band = stroke_mask(W, H, [(cx - 30, cy - 10), (cx + 30, cy - 10)], 5, (0.05, 0.05)) * sh_in
    star = shape_mask(W, H, [(cx + math.cos(-math.pi / 2 + i * math.pi / 5) * (12 if i % 2 == 0 else 5), cy + 10 + math.sin(-math.pi / 2 + i * math.pi / 5) * (12 if i % 2 == 0 else 5)) for i in range(10)], smooth=False)
    art = blank(W, H)
    art = over(art, gouache_paint(sh_in, "#0d1736", "#1a2a66", seed=nxt(), rough=0.8, density=0.95))
    art = over(art, foil(union(sub(sh, sh_in), band, star), GOLD, seed=nxt(), emboss=0.7, sparkle=0.15))
    preview(art, f"{PREV}/al-shield.png", "#0a1128")
    save(art, f"{D}/shield.webp", max_w=80, q=84)


def items():
    """Loot icons for the wishlist shop: gouache body + ink line + rarity glow (fridge EPIC, washer ELITE, TV LEGEND)."""
    S = 140
    INK = "#0b0f24"
    out = {}

    def gp(m, a, b=None, rough=1.0, density=0.97):
        return gouache_paint(m, a, b, seed=nxt(), rough=rough, streak=0.6, density=density)

    def lines(ms, ws):
        m = union(*[outline(mk, w) for mk, w in zip(ms, ws)])
        return pigment(m, INK, seed=nxt(), density=0.8, edge=0.1, bloom=0, feather=0.4, rough=0.7, holes=0.08)

    rng.seed(61)
    # fridge (purple enamel)
    body = shape_mask(S, S, wobble_rect(42, 20, 56, 100, rng, 1.2))
    split = shape_mask(S, S, [(42, 54), (98, 54), (98, 58), (42, 58)], smooth=False)
    handles = union(rrect_mask(S, S, 84, 32, 6, 16, 3), rrect_mask(S, S, 84, 64, 6, 26, 3))
    art = blank(S, S)
    art = over(art, glow(body, "#b06bff", radius=10, strength=0.35))
    art = over(art, gp(body, "#8f55d9", "#6f3fb8"))
    art = over(art, gp(shape_mask(S, S, [(48, 26), (52, 26), (52, 50), (48, 50)]), "#d9bfff", rough=0.4, density=0.3))
    art = over(art, gp(shape_mask(S, S, [(48, 62), (52, 62), (52, 112), (48, 112)]), "#d9bfff", rough=0.4, density=0.3))
    art = over(art, gp(split, "#3b1f6e", rough=0.4))
    art = over(art, foil(handles, GOLD, seed=nxt(), emboss=0.6, sparkle=0.1))
    art = over(art, lines([body], [2.4]))
    out["item-fridge"] = art
    # washing machine (cyan)
    body = shape_mask(S, S, wobble_rect(30, 28, 80, 88, rng, 1.2))
    panel = shape_mask(S, S, wobble_rect(30, 28, 80, 18, rng, 0.8))
    door = shape_mask(S, S, ellipse_pts(70, 80, 25, 25, 24))
    glass = shape_mask(S, S, ellipse_pts(70, 80, 17, 17, 22))
    water = shape_mask(S, S, [(53, 84), (62, 80), (72, 86), (82, 80), (88, 84), (86, 92), (70, 98), (55, 92)]) * glass
    knobs = dots_mask(S, S, [(42, 37, 3.6), (54, 37, 2.4)])
    art = blank(S, S)
    art = over(art, glow(body, "#39c5f3", radius=10, strength=0.35))
    art = over(art, gp(body, "#e9eef6", "#cfd8e6"))
    art = over(art, gp(panel, "#2aa4d4", "#1f86b3", rough=0.6))
    art = over(art, gp(door, "#9aa6b8", rough=0.6))
    art = over(art, gp(glass, "#173b6b", "#1d4c86", rough=0.5))
    art = over(art, gp(water, "#39c5f3", "#7fdcfa", rough=0.4, density=0.9))
    art = over(art, gp(stroke_mask(S, S, [(60, 70), (66, 66)], 2.4, (0.1, 0.1)), "#ffffff", rough=0.3, density=0.6))
    art = over(art, gp(knobs, "#f0d48a", rough=0.3))
    art = over(art, lines([body, panel, door, glass], [2.4, 1.4, 1.8, 1.4]))
    out["item-washer"] = art
    # smart tv (gold frame, painted dusk screen)
    frame = shape_mask(S, S, wobble_rect(16, 30, 108, 68, rng, 1.0))
    screen = shape_mask(S, S, wobble_rect(23, 36, 94, 56, rng, 0.8))
    stand = union(shape_mask(S, S, [(64, 98), (76, 98), (80, 110), (60, 110)], smooth=False), shape_mask(S, S, wobble_rect(48, 108, 44, 6, rng, 0.5)))
    art = blank(S, S)
    art = over(art, glow(frame, "#f0c96e", radius=10, strength=0.35))
    art = over(art, gp(stand, "#8f6b2a", rough=0.5))
    art = over(art, foil(frame, GOLD, seed=nxt(), emboss=0.6, sparkle=0.1))
    sky = painted_sky(S, S, [(0, "#1a2a66"), (0.42, "#4a3a72"), (0.62, "#c9843c"), (1, "#2b2e5e")], seed=nxt(), streak=0.8)
    sky[..., 3] = screen
    art = over(art, sky)
    hill = shape_mask(S, S, [(23, 92), (23, 78), (44, 70), (66, 76), (90, 66), (117, 74), (117, 92)]) * screen
    art = over(art, gp(hill, "#0d1736", "#152052", rough=0.6))
    art = over(art, gp(dots_mask(S, S, [(84, 52, 6)]) * screen, "#f0d48a", rough=0.3))
    art = over(art, lines([frame, screen], [2.2, 1.2]))
    out["item-tv"] = art
    sheet = Image.new("RGB", (S * 3, S), "#0d1736")
    for i, (k, a) in enumerate(out.items()):
        save(a, f"{D}/{k}.webp", max_w=104, q=84)
        sheet.paste(to_image(a), (i * S, 0), to_image(a))
    sheet.save(f"{PREV}/al-items.png")


def canvas():
    S = 360
    t = canvas_tile(S, "#0a1128", seed=7, streak=1.0, grain=1.0)
    save_rgb(np.concatenate([t, np.ones((S, S, 1), np.float32)], -1), f"{D}/canvas.webp", q=72)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["cover", "rune", "crest", "shield", "items", "canvas"]:
        {"cover": cover, "rune": rune, "crest": crest, "shield": shield, "items": items, "canvas": canvas}[w]()
