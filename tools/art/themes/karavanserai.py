"""Karavanserai — a Silk Road caravanserai courtyard at dusk: brick iwan portal and two-storey arcades, carpets laid
on the courtyard floor, pierced copper lanterns. Architecture and objects only (no figures, no calligraphy).
Run: python3 -I karavanserai.py [part ...]   parts: court lantern carpet arch brick
Assets -> public/themes/art/karavanserai/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l3_lib import *

OUT = outdir("karavanserai")
PARTS = sys.argv[1:] or ["court", "lantern", "carpet", "arch", "brick"]
BRICK, BRICK_L, BRICK_D = "#b5653a", "#d08a5a", "#7a3c22"
PLUM, DUSK = "#2a1a34", "#4b2a45"
COPPER, COPPER_L = "#b8693a", "#e0a06a"
MADDER, MADDER_D, INDIGO, IVORY, SAFF = "#8c2a22", "#5e1a16", "#26305a", "#efe2c6", "#d89a3a"


def pointed_arch(cx, base, w, h, n=18):
    """Persian pointed arch outline (closed, jambs down to base). rise of the curved part = 0.62 w."""
    rise = w * 0.62
    spring = base - max(0.0, h - rise)
    a = math.pi / 2 - 0.2
    left = [(cx - w / 2 + (w / 2) * (1 - math.cos(t * a)) / (1 - math.cos(a)), spring - rise * math.sin(t * a) / math.sin(a)) for t in [i / n for i in range(n + 1)]]
    right = [(2 * cx - x, y) for x, y in reversed(left[:-1])]
    return [(cx - w / 2, base)] + left + right + [(cx + w / 2, base)]


def brick_field(W, H, bw=18, bh=7, seed=1):
    """Running-bond mortar lines (1 = mortar)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    row = np.floor(yy / bh)
    off = (row % 2) * bw / 2
    fy = (yy % bh) / bh
    fx = ((xx + off) % bw) / bw
    m = np.maximum((fy < 0.16).astype(np.float32), (fx < 0.07).astype(np.float32))
    return gaussian_filter(m, 0.5)


def brick_tone(W, H, bw=18, bh=7, seed=1):
    """Per-brick tonal variation 0..1."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    row = (yy // bh).astype(int)
    col = ((xx + (row % 2) * bw // 2) // bw).astype(int)
    tab = rng.random((row.max() + 2, col.max() + 2)).astype(np.float32)
    return tab[row, col]


def paint_brick(art, m, W, H, nx, base=BRICK, lite=BRICK_L, dark=BRICK_D, bw=18, bh=7, mortar="#e3c49a", shade=None):
    t = brick_tone(W, H, bw, bh, nx())
    ca, cb, cd = (np.array(hex_rgb(c), np.float32) for c in (base, lite, dark))
    rgb = ca * (1 - t[..., None] * 0.6) + cb * (t[..., None] * 0.6)
    rgb = np.where(t[..., None] < 0.15, cd, rgb)
    mo = brick_field(W, H, bw, bh)
    mo = mo * (0.45 + 0.55 * fbm(W, H, nx(), 30, 3))
    rgb = rgb * (1 - mo[..., None] * 0.45) + np.array(hex_rgb(mortar), np.float32) * mo[..., None] * 0.45
    if shade is not None:
        rgb = rgb * (1 - shade[..., None])
    layer = np.concatenate([rgb, m[..., None]], -1)
    art = over(art, layer)
    art = G(art, m, base, lite, seed=nx(), density=0.4, edge=0.45, bloom=0.5, rough=2, mottle=0.8)
    return art


if "court" in PARTS:
    W, H = 780, 980
    nx = Seq(41000)
    rng = random.Random(5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = painted_sky(W, H, [(0, "#1f1430"), (0.18, PLUM), (0.34, "#6a3550"), (0.46, "#c2664a"), (0.55, "#efae62"), (1, "#efae62")], seed=nx(), streak=0.9)
    art = soft(art, circles(W, H, [(390, 520, 300)]), "#ffd59a", alpha=0.3, blur=60, pad=10)
    st = circles(W, H, [(rng.uniform(10, W - 10), rng.uniform(10, 260), rng.choice([0.9, 1.2, 1.5])) for _ in range(40)])
    art = soft(art, st, "#f6e6c8", alpha=0.6, pad=4)
    clear()
    ground = 760
    # side arcades (two storeys), receding slightly toward the portal
    for side in (-1, 1):
        x0 = 390 + side * 150
        x1 = 390 + side * 420
        top = 400
        wall = shapes(W, H, [[(x0, top + 20), (x1, top - 30), (x1, ground + 40), (x0, ground)]], smooth=False)
        shade = np.clip(0.12 + 0.18 * (np.abs(xx - 390) - 150) / 270, 0, 0.4) * (side == -1)
        art = paint_brick(art, wall, W, H, nx, shade=shade + 0.08)
        clear()
        # arches: 2 storeys x 3 bays
        for k in range(3):
            t0, t1 = k / 3, (k + 1) / 3
            ax0 = x0 + (x1 - x0) * (t0 + 0.04); ax1 = x0 + (x1 - x0) * (t1 - 0.04)
            for (yb, hh) in ((ground - 6 + (t0 + t1) / 2 * 30, 150), (ground - 186 + (t0 + t1) / 2 * 24, 120)):
                cx = (ax0 + ax1) / 2; w = abs(ax1 - ax0) * 0.78
                hole = shapes(W, H, [pointed_arch(cx, yb, w, hh)], smooth=False)
                frame = shapes(W, H, [pointed_arch(cx, yb + 2, w + 14, hh + 12)], smooth=False)
                art = G(art, np.clip(frame - hole, 0, 1), BRICK_D, seed=nx(), density=0.45, edge=0.4, bloom=0.2, rough=1)
                art = GP(art, hole, "#3b1f22", "#24131a", seed=nx(), rough=0.8, pad=6)
                art = soft(art, hole * np.clip((yy - (yb - hh * 0.5)) / (hh * 0.6), 0, 1), "#e08a3e", alpha=0.4, pad=6)
                art = G(art, hole * np.clip(1 - (yy - (yb - hh)) / (hh * 0.5), 0, 1), "#140a10", seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1)
                if rng.random() < 0.75:
                    ly = yb - hh * 0.55
                    art = soft(art, circles(W, H, [(cx, ly, w * 0.3)]), "#ffb860", alpha=0.35, blur=6, pad=8)
                    art = soft(art, ellipses(W, H, [(cx, ly, 3.2, 5, 0)]), "#ffe0a0", alpha=1, pad=4)
                    art = soft(art, strokes(W, H, [([(cx, yb - hh * 0.95), (cx, ly - 5)], 0.8, None)]), "#2a1410", alpha=0.8, pad=4)
        clear()
    # central iwan portal (pishtaq): tall rectangular frame with the great pointed arch
    pish = shapes(W, H, [[(230, 250), (550, 250), (550, ground + 10), (230, ground + 10)]], smooth=False)
    art = paint_brick(art, pish, W, H, nx, bw=16, bh=6)
    # glazed-brick band around the portal frame (turquoise and cobalt pattern) + inner frame
    band = np.clip(pish - shapes(W, H, [[(250, 270), (530, 270), (530, ground + 10), (250, ground + 10)]], smooth=False), 0, 1)
    art = GP(art, band, "#2f7f86", "#245f72", seed=nx(), rough=0.8, pad=6)
    dots = circles(W, H, [(x, 260, 3) for x in range(240, 545, 14)] + [(240, y, 3) for y in range(274, ground, 14)] + [(540, y, 3) for y in range(274, ground, 14)])
    art = GP(art, dots, IVORY, seed=nx(), rough=0.5, pad=4)
    big = shapes(W, H, [pointed_arch(390, ground + 10, 214, 410)], smooth=False)
    bigf = shapes(W, H, [pointed_arch(390, ground + 10, 240, 430)], smooth=False)
    art = GP(art, np.clip(bigf - big, 0, 1), BRICK_D, "#5e2c18", seed=nx(), rough=0.8, pad=6)
    # the deep iwan: shadowed vault with a stepped muqarnas hood suggested by tiers of small niches
    art = GP(art, big, "#3a1d22", "#1e1016", seed=nx(), rough=0.8, pad=6)
    for tier in range(4):
        yb = 420 + tier * 34
        n = 3 + tier
        ww = 170 - tier * 6
        for j in range(n):
            cx = 390 - ww / 2 + (j + 0.5) * ww / n
            niche = shapes(W, H, [pointed_arch(cx, yb, ww / n * 0.82, 26)], smooth=False)
            art = G(art, niche, "#a0583a", seed=nx(), density=0.8, edge=0.7, bloom=0.1, rough=0.8)
            art = G(art, niche * np.clip(1 - (yy - (yb - 26)) / 16, 0, 1), "#2a1410", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.6)
    clear()
    # doorway inside the iwan, lamp-lit
    door = shapes(W, H, [pointed_arch(390, ground + 4, 92, 150)], smooth=False)
    art = GP(art, door, "#f0a24a", "#c86a2a", seed=nx(), rough=0.8, pad=6)
    art = soft(art, door, "#ffd28a", alpha=0.45, blur=18, pad=8)
    # parapet line against the sky
    par = shapes(W, H, [[(0, 360), (230, 392), (230, 404), (0, 374)], [(550, 392), (780, 360), (780, 374), (550, 404)]], smooth=False)
    art = GP(art, par, BRICK_D, seed=nx(), rough=0.6, pad=4)
    clear()
    # courtyard floor: worn brick paving in perspective
    floor = shapes(W, H, [[(-20, ground), (800, ground), (800, H), (-20, H)]], smooth=False)
    art = GP(art, floor, "#9c5a36", "#7a4228", seed=nx(), rough=1, streak=1.0, pad=6)
    lines = strokes(W, H, [([(390 + (x - 390) * 0.18, ground), (x, H)], 1.4, None) for x in range(-400, 1200, 60)] +
                    [([(-20, y), (800, y)], 1.2, None) for y in [ground + 12, ground + 30, ground + 56, ground + 92, ground + 140, ground + 204]])
    art = G(art, lines * floor, "#4a2416", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.8)
    art = soft(art, floor * np.clip(1 - (yy - ground) / 120, 0, 1), "#f1a858", alpha=0.25, pad=4)
    clear()
    # carpets laid on the floor: a runner toward the iwan + a wide carpet in front, seen in perspective
    def quad(a, b, c, d):
        return [a, b, c, d]
    runner = shapes(W, H, [quad((350, ground + 6), (430, ground + 6), (470, ground + 120), (310, ground + 120))], smooth=False)
    rug = shapes(W, H, [quad((150, ground + 128), (630, ground + 128), (740, H - 6), (40, H - 6))], smooth=False)
    for m, s0 in ((runner, 1), (rug, 2)):
        art = GP(art, m, MADDER, MADDER_D, seed=nx(), rough=0.8, streak=0.6, pad=6)
    border_r = np.clip(rug - shapes(W, H, [quad((176, ground + 142), (604, ground + 142), (700, H - 22), (80, H - 22))], smooth=False), 0, 1)
    art = GP(art, border_r, INDIGO, "#1b2244", seed=nx(), rough=0.6, pad=6)
    guard = np.clip(shapes(W, H, [quad((186, ground + 148), (594, ground + 148), (688, H - 28), (92, H - 28))], smooth=False) - shapes(W, H, [quad((192, ground + 152), (588, ground + 152), (680, H - 32), (100, H - 32))], smooth=False), 0, 1)
    art = GP(art, guard, IVORY, seed=nx(), rough=0.5, pad=4)
    medal = shapes(W, H, [[(390, ground + 160), (470, ground + 186), (390, H - 40), (310, ground + 186)]], smooth=False)
    art = GP(art, medal, INDIGO, seed=nx(), rough=0.5, pad=4)
    art = GP(art, shapes(W, H, [[(390, ground + 168), (440, ground + 186), (390, ground + 204), (340, ground + 186)]], smooth=False), SAFF, seed=nx(), rough=0.5, pad=4)
    rb = np.clip(runner - shapes(W, H, [quad((360, ground + 10), (420, ground + 10), (454, ground + 116), (326, ground + 116))], smooth=False), 0, 1)
    art = GP(art, rb, INDIGO, seed=nx(), rough=0.5, pad=4)
    art = G(art, np.maximum(rug, runner) * jw.hatch(W, H, 0.0, 3, 0.2, 3), "#3a0e0c", seed=nx(), density=0.25, edge=0, bloom=0, rough=0.5)
    # fringe on the front carpet
    fr = strokes(W, H, [([(x, H - 6), (x + 1, H)], 1.6, None) for x in range(46, 736, 6)])
    art = GP(art, fr, IVORY, seed=nx(), rough=0.4, pad=3)
    # dusk light: warm from the right, the left arcade in shade, a soft vignette; watercolour mottling over all
    art = G(art, np.clip((390 - xx) / 390, 0, 1) * (yy > 330) * 0.9, "#3a2340", seed=nx(), density=0.45, edge=0, bloom=0.3, rough=4)
    art = soft(art, np.clip((xx - 520) / 260, 0, 1) * (yy > 330) * (yy < ground), "#ffb066", alpha=0.18, pad=0)
    mot = fbm(W, H, nx(), 60, 4)
    art[..., :3] *= (0.9 + 0.16 * mot)[..., None]
    clear()
    prev(art, "kv-court", bg=None)
    save_rgb(art, f"{OUT}/court.webp", size=(640, 804), quality=80)

if "lantern" in PARTS:
    W, H = 260, 620
    nx = Seq(42000)
    cx = 130
    art = blank(W, H)
    chain = strokes(W, H, [([(cx, 0), (cx, 170)], 3, None)])
    links = ellipses(W, H, [(cx, y, 4, 8, 0) for y in range(8, 170, 16)])
    art = FO(art, np.clip(links - ellipses(W, H, [(cx, y, 2, 5.5, 0) for y in range(8, 170, 16)]), 0, 1), "#8a5530", seed=nx(), emboss=0.6)
    art = FO(art, chain * 0.5, "#6a3e22", seed=nx())
    # glow halo first
    body = shapes(W, H, [[(cx - 52, 290), (cx - 74, 340), (cx - 70, 420), (cx - 40, 470), (cx + 40, 470), (cx + 70, 420), (cx + 74, 340), (cx + 52, 290)]])
    art = over(art, glow(body, "#ffbf6a", radius=34, strength=0.32))
    dome = shapes(W, H, [[(cx - 56, 292), (cx - 50, 250), (cx - 26, 214), (cx, 196), (cx + 26, 214), (cx + 50, 250), (cx + 56, 292)]])
    fin = shapes(W, H, [deform(ellipse_pts(cx, 184, 10, 14, 10), random.Random(1), 0, 0)]) + shapes(W, H, [[(cx - 4, 170), (cx + 4, 170), (cx + 5, 186), (cx - 5, 186)]], smooth=False)
    base = shapes(W, H, [[(cx - 42, 468), (cx + 42, 468), (cx + 18, 510), (cx, 530), (cx - 18, 510)]])
    tip = shapes(W, H, [deform(ellipse_pts(cx, 540, 7, 10, 8), random.Random(2), 0, 0)])
    rings = shapes(W, H, [[(cx - 60, 286), (cx + 60, 286), (cx + 60, 298), (cx - 60, 298)], [(cx - 46, 462), (cx + 46, 462), (cx + 46, 474), (cx - 46, 474)]], smooth=False)
    art = FO(art, np.clip(dome + fin + base + tip, 0, 1), COPPER, seed=nx(), emboss=0.8, sparkle=0.1)
    art = G(art, dome * np.clip((xx := np.mgrid[0:H, 0:W][1].astype(np.float32)) - cx, 0, 60) / 60, "#4a2410", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1)
    # pierced body: copper with glowing star/teardrop holes
    art = FO(art, body, "#a65a2e", seed=nx(), emboss=0.5, sparkle=0.08)
    art = G(art, body * np.clip((xx - cx) / 70, 0, 1), "#3e1e0e", seed=nx(), density=0.6, edge=0.1, bloom=0, rough=1)
    holes = []
    for row, y in enumerate(range(312, 462, 26)):
        half = 60 if 330 < y < 430 else 44
        for j in range(-3, 4):
            x = cx + j * 18 + (9 if row % 2 else 0)
            if abs(x - cx) < half - 6:
                holes.append(petal_pts(x, y + 8, 16, 6, -math.pi / 2, n=10))
    hm = shapes(W, H, holes)
    stars = []
    for y in (250, 270):
        for j in range(-2, 3):
            x = cx + j * 16
            if abs(x - cx) < (40 if y == 250 else 50):
                stars.append((x, y, 3.2))
    hm = np.clip(hm + circles(W, H, stars), 0, 1)
    art = over(art, glow(hm, "#ffc56a", radius=4, strength=0.6))
    art = GP(art, hm, "#ffe2a0", "#ffb850", seed=nx(), rough=0.4, pad=4)
    art = FO(art, rings, COPPER_L, seed=nx(), emboss=0.7)
    tas = strokes(W, H, [([(cx + d, 546), (cx + d * 1.6, 610)], 2.2, (0, 0.4)) for d in (-6, -3, 0, 3, 6)])
    art = GP(art, tas, MADDER, seed=nx(), rough=0.5, pad=4)
    prev(art, "kv-lantern", bg="#2a1a34")
    save(art, f"{OUT}/lantern.webp", max_w=150, quality=84)

if "carpet" in PARTS:
    # seamless horizontal carpet border band: indigo border with ivory guards, madder field with stepped lozenges & rosettes
    W, H = 320, 96
    nx = Seq(43000)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(MADDER), np.float32)
    def paint(rgb, m, col, k=0.9):
        m = np.clip(m, 0, 1)
        c = np.array(hex_rgb(col), np.float32) * (0.9 + 0.18 * wrap_noise(W, H, nx(), 6))[..., None]
        return rgb * (1 - m[..., None] * k) + c * m[..., None] * k
    def wrapped(polys):
        return [[(x + dx, y) for x, y in p] for p in polys for dx in (-W, 0, W)]
    rgb = paint(rgb, shapes(W, H, [[(0, 0), (W, 0), (W, 14), (0, 14)], [(0, H - 14), (W, H - 14), (W, H), (0, H)]], smooth=False), INDIGO, 1)
    rgb = paint(rgb, shapes(W, H, [[(0, 16), (W, 16), (W, 20), (0, 20)], [(0, H - 20), (W, H - 20), (W, H - 16), (0, H - 16)]], smooth=False), IVORY)
    loz, inn, ros = [], [], []
    for i in range(4):
        cx = i * 80 + 40; cy = H / 2
        loz.append([(cx, cy - 22), (cx + 8, cy - 22), (cx + 8, cy - 14), (cx + 16, cy - 14), (cx + 16, cy - 6), (cx + 24, cy - 6), (cx + 24, cy + 6), (cx + 16, cy + 6), (cx + 16, cy + 14), (cx + 8, cy + 14), (cx + 8, cy + 22), (cx - 8, cy + 22), (cx - 8, cy + 14), (cx - 16, cy + 14), (cx - 16, cy + 6), (cx - 24, cy + 6), (cx - 24, cy - 6), (cx - 16, cy - 6), (cx - 16, cy - 14), (cx - 8, cy - 14), (cx - 8, cy - 22)])
        inn.append([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)])
        ros += [(i * 80 + dx, cy, 4) for dx in (0,)]
    rgb = paint(rgb, shapes(W, H, wrapped(loz), smooth=False), INDIGO)
    rgb = paint(rgb, shapes(W, H, wrapped(inn), smooth=False), SAFF)
    rgb = paint(rgb, circles(W, H, [(x + dx, y, r) for x, y, r in ros for dx in (-W, 0, W)]), IVORY)
    rgb = paint(rgb, circles(W, H, [(x + dx, y, 8) for x, y, r in ros for dx in (-W, 0, W)]) - circles(W, H, [(x + dx, y, 5.5) for x, y, r in ros for dx in (-W, 0, W)]), SAFF, 0.8)
    pile = wrap_noise(W, H, 5, 0.6)
    knot = (np.mgrid[0:H, 0:W][1] % 3 == 0).astype(np.float32) * 0.04
    rgb *= (0.9 + 0.16 * pile - knot)[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    prev(arr, "kv-carpet", bg="#000000")
    save_full(arr, f"{OUT}/carpet.webp", size=(240, 72), quality=80)

if "arch" in PARTS:
    # brick pointed-arch frame with a transparent opening (hero photo sits behind it)
    W, H = 600, 800
    nx = Seq(44000)
    outer = shapes(W, H, [[(10, 120), (590, 120), (590, 790), (10, 790)]], smooth=False)
    hole = shapes(W, H, [pointed_arch(300, 760, 440, 610)], smooth=False)
    frame = np.clip(outer - hole, 0, 1)
    art = blank(W, H)
    art = paint_brick(art, frame, W, H, nx, bw=26, bh=10)
    lip = np.clip(shapes(W, H, [pointed_arch(300, 764, 470, 628)], smooth=False) - hole, 0, 1)
    art = GP(art, lip, BRICK_D, "#5e2c18", seed=nx(), rough=0.8, pad=6)
    dots = shapes(W, H, [pointed_arch(300, 766, 456, 619)], smooth=False)
    art = GP(art, np.clip(dots - shapes(W, H, [pointed_arch(300, 766, 450, 615)], smooth=False), 0, 1), COPPER_L, seed=nx(), rough=0.5, pad=4)
    band = np.clip(outer - shapes(W, H, [[(30, 140), (570, 140), (570, 790), (30, 790)]], smooth=False), 0, 1)
    art = GP(art, band, BRICK_D, "#5e2c18", seed=nx(), rough=0.8, pad=6)
    art = G(art, frame * np.clip((np.mgrid[0:H, 0:W][1] - 300) / 300, 0, 1), "#3a1a14", seed=nx(), density=0.35, edge=0, bloom=0.3, rough=2)
    prev(art, "kv-arch", bg="#efe2c6")
    save_full(art[110:800, :], f"{OUT}/arch.webp", size=(400, 460), quality=82)

if "brick" in PARTS:
    n = 256
    nx = Seq(45000)
    W = H = n
    t = brick_tone(W, H, 32, 12, 4)
    t = t  # rows wrap: 256/12 not integer, so use 16px rows
    t = brick_tone(W, H, 32, 16, 4)
    ca, cb = np.array(hex_rgb("#efdcc0"), np.float32), np.array(hex_rgb("#e6cba6"), np.float32)
    rgb = ca * (1 - t[..., None]) + cb * t[..., None]
    mo = brick_field(W, H, 32, 16)
    rgb = rgb * (1 - mo[..., None] * 0.08) + np.array(hex_rgb("#f7ead6"), np.float32) * mo[..., None] * 0.08
    rgb *= (0.97 + 0.05 * wrap_noise(W, H, 3, 1.0))[..., None]
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_full(arr, f"{OUT}/brick.webp", quality=72)
