"""Maulid Nabi — original painted ornaments for a Maulid Nabi Muhammad SAW invitation (no figures, no animals, no
drawn calligraphy, no depiction of the Prophet in any form): two hanging lanterns (a brass hexagonal lantern with
green glass and a pierced dome lantern), a janur (young coconut leaf) garland with folded tassels, a kembang endog
arrangement (paper flowers and wrapped eggs on bamboo skewers in a brass pot), a gold-foil eight-point star and a
seamless deep-green ground.
Run: python3 -I maulid-nabi.py [part ...]   parts: lantern lantern2 janur kembang star ground
Assets -> public/themes/art/maulid-nabi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h1_lib import *  # noqa

OUT = outdir("maulid-nabi")
PARTS = sys.argv[1:] or ["lantern", "lantern2", "janur", "kembang", "star", "ground"]
BRASS, BRASS_D, BRASS_L = "#c79a45", "#7d5a22", "#f0d58e"
EMER, EMER_D, EMER_L = "#1f6b4e", "#0f3d2d", "#58a882"
JANUR, JANUR_D, JANUR_L = "#e3d58a", "#b4a457", "#f6efc0"
WARM = "#ffd98a"


def chain(art, W, H, x, y0, y1, nx):
    links = []
    y = y0
    k = 0
    while y < y1:
        links.append((x, y + 5, 3.2 if k % 2 else 2.0, 5.5, 0))
        y += 9; k += 1
    m = ellipses(W, H, links)
    m = np.clip(m - ellipses(W, H, [(a, b, max(0.6, rx - 1.6), ry - 2, 0) for a, b, rx, ry, _ in links]), 0, 1)
    return FO(art, m, BRASS, seed=nx(), emboss=0.5, sparkle=0.1)


def brass(art, W, H, m, nx, x0, x1):
    art = FO(art, m, BRASS, seed=nx(), emboss=0.7, sparkle=0.05)
    art = G(art, m * xgrad(W, H, x0 + (x1 - x0) * 0.5, x1), BRASS_D, seed=nx(), density=0.45, edge=0.2, rough=1, feather=1.5)
    return art


def part_lantern():
    """Hexagonal brass lantern: domed cap with finial, three visible glass faces (green, amber, green) glowing from a
    candle inside, pierced star band, tapered base with a drop."""
    W, H = 280, 520
    rng = random.Random(5); nx = Seq(100)
    art = blank(W, H)
    cx = W / 2
    art = chain(art, W, H, cx, 0, 120, nx)
    # glow halo first (behind)
    art = over(glow(ellipses(W, H, [(cx, 300, 56, 80, 0)]), WARM, radius=24, strength=0.3), art)
    # ring + dome cap
    art = brass(art, W, H, circles(W, H, [(cx, 128, 10)]) - circles(W, H, [(cx, 128, 5)]), nx, cx - 10, cx + 10)
    dome = shape_mask(W, H, [(cx - 58, 210), (cx - 50, 180), (cx - 26, 152), (cx, 138), (cx + 26, 152), (cx + 50, 180), (cx + 58, 210)])
    art = brass(art, W, H, dome, nx, cx - 58, cx + 58)
    holes = circles(W, H, [(cx + dx, 186, 3.2) for dx in (-30, -15, 0, 15, 30)])
    art = over(art, glow(holes, WARM, radius=4, strength=0.8))
    art = G(art, holes, "#fff2c8", seed=nx(), density=0.9, edge=0, rough=0.2, feather=0.4)
    art = brass(art, W, H, rect(W, H, cx - 64, 206, cx + 64, 220), nx, cx - 64, cx + 64)
    # glass faces
    faces = [((cx - 64, 220), (cx - 34, 220), (cx - 34, 380), (cx - 52, 380), EMER_L),
             ((cx - 34, 220), (cx + 34, 220), (cx + 34, 380), (cx - 34, 380), "#f2c46a"),
             ((cx + 34, 220), (cx + 64, 220), (cx + 52, 380), (cx + 34, 380), EMER_L)]
    for a, b, c, d, col in faces:
        fm = poly(W, H, [a, b, c, d])
        art = G(art, fm, col, mix_hex(col, "#ffffff", 0.3), seed=nx(), density=0.85, edge=0.6, bloom=0.5, rough=1, feather=0.8)
    flame = radial(W, H, cx, 300, 40, 1.6)
    art = G(art, flame * poly(W, H, [faces[1][0], faces[1][1], faces[1][2], faces[1][3]]), "#fff6d8", seed=nx(), density=0.9, edge=0, bloom=0.2, rough=1, feather=3)
    # brass mullions + pierced band of small eight-point stars across the middle
    mull = strokes(W, H, [([(cx - 64, 220), (cx - 52, 380)], 5, None), ([(cx - 34, 220), (cx - 34, 380)], 5, None),
                          ([(cx + 34, 220), (cx + 34, 380)], 5, None), ([(cx + 64, 220), (cx + 52, 380)], 5, None)])
    art = brass(art, W, H, mull, nx, cx - 64, cx + 64)
    band = rect(W, H, cx - 62, 284, cx + 62, 306)
    stars = []
    for k in range(5):
        x = cx - 48 + k * 24
        stars += [[(x + math.cos(a) * (7 if j % 2 == 0 else 3.2), 295 + math.sin(a) * (7 if j % 2 == 0 else 3.2)) for j, a in enumerate([i * math.pi / 8 for i in range(16)])]]
    sm = shapes(W, H, stars, smooth=False)
    art = brass(art, W, H, np.clip(band - sm, 0, 1), nx, cx - 62, cx + 62)
    art = G(art, sm * band, "#fff1c4", seed=nx(), density=0.85, edge=0, rough=0.2, feather=0.4)
    # base
    base = shape_mask(W, H, [(cx - 56, 380), (cx + 56, 380), (cx + 40, 400), (cx + 16, 418), (cx, 440), (cx - 16, 418), (cx - 40, 400)])
    art = brass(art, W, H, base, nx, cx - 56, cx + 56)
    drop = shape_mask(W, H, [(cx, 440), (cx + 7, 458), (cx, 472), (cx - 7, 458)])
    art = brass(art, W, H, drop, nx, cx - 7, cx + 7)
    preview(art, "ml-lantern", bg="#123d2f")
    save(art, f"{OUT}/lantern.webp", max_w=130, quality=84)
    clear()


def part_lantern2():
    """Pierced round lantern: brass ball with star-and-lozenge piercings glowing warm, onion top, tassel."""
    W, H = 280, 520
    rng = random.Random(7); nx = Seq(500)
    art = blank(W, H)
    cx, cy, r = W / 2, 290, 72
    art = chain(art, W, H, cx, 0, 150, nx)
    art = over(glow(circles(W, H, [(cx, cy, r * 0.85)]), WARM, radius=26, strength=0.32), art)
    onion = shape_mask(W, H, [(cx - 34, 226), (cx - 30, 206), (cx - 14, 186), (cx, 160), (cx + 14, 186), (cx + 30, 206), (cx + 34, 226)])
    art = brass(art, W, H, onion, nx, cx - 34, cx + 34)
    ball = circles(W, H, [(cx, cy, r)])
    pierce = []
    for ring_, (rr, n, s) in enumerate([(0.0, 1, 9), (0.45, 8, 6), (0.78, 12, 4)]):
        for k in range(n):
            a = k * math.tau / n + ring_ * 0.3
            px, py = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr * 0.92
            pierce.append([(px + math.cos(t) * (s if j % 2 == 0 else s * 0.45), py + math.sin(t) * (s if j % 2 == 0 else s * 0.45)) for j, t in enumerate([i * math.pi / 8 for i in range(16)])])
    pm = shapes(W, H, pierce, smooth=False) * ball
    art = brass(art, W, H, np.clip(ball - pm, 0, 1), nx, cx - r, cx + r)
    art = G(art, ball * radial(W, H, cx + 26, cy + 30, r * 1.1), "#3a2a10", seed=nx(), density=0.4, edge=0, rough=1, feather=3)
    art = over(art, glow(pm, WARM, radius=4, strength=0.9))
    art = G(art, pm, "#fff3cc", seed=nx(), density=0.95, edge=0, rough=0.2, feather=0.4)
    # belt and bottom cap
    art = brass(art, W, H, ellipses(W, H, [(cx, cy, r + 3, 6, 0)]), nx, cx - r, cx + r)
    art = brass(art, W, H, shape_mask(W, H, [(cx - 22, cy + r - 6), (cx + 22, cy + r - 6), (cx + 10, cy + r + 14), (cx - 10, cy + r + 14)]), nx, cx - 22, cx + 22)
    # green silk tassel
    tas = [([(cx, cy + r + 14), (cx + rng.uniform(-14, 14), cy + r + 80 + rng.uniform(-6, 6))], 2.2, (0.0, 0.3)) for _ in range(16)]
    art = G(art, strokes(W, H, tas), EMER, EMER_L, seed=nx(), density=0.9, edge=0.3, rough=0.4, feather=0.4)
    art = brass(art, W, H, ellipses(W, H, [(cx, cy + r + 20, 9, 7, 0)]), nx, cx - 9, cx + 9)
    preview(art, "ml-lantern2", bg="#123d2f")
    save(art, f"{OUT}/lantern2.webp", max_w=130, quality=84)
    clear()


def janur_tassel(art, W, H, x, y, L, nx, rng, sway=0.0):
    """Folded janur strip hanging down: a pointed leaf blade, pale yellow-green with a crease and torn tip."""
    a = math.pi / 2 + sway
    pts = petal_pts(x, y, L, L * 0.12, a, n=10)
    m = shape_mask(W, H, pts)
    art = GP(art, m, JANUR, JANUR_L, seed=nx(), rough=0.7, streak=0.9, pad=6)
    crease = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0.05, 0.9, 8)]
    art = G(art, stroke_mask(W, H, crease, 1.2) * m, JANUR_D, seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4, pad=6)
    art = G(art, m * ygrad(W, H, y, y + L), "#9b8a3e", seed=nx(), density=0.25, edge=0.2, rough=0.6, feather=1, pad=6)
    return art


def part_janur():
    """Janur garland: a woven janur rope swagging across, folded janur tassels hanging from it and small woven knots."""
    W, H = 780, 230
    rng = random.Random(9); nx = Seq(900)
    art = blank(W, H)
    pts = [(x, 30 + 70 * max(0.0, math.sin(math.pi * x / W)) ** 1.2) for x in np.linspace(-10, W + 10, 80)]
    # tassels first (behind the rope)
    for k in range(25):
        t = (k + 0.5) / 25
        i = int(t * (len(pts) - 1))
        x, y = pts[i]
        L = rng.uniform(60, 110) if k % 2 == 0 else rng.uniform(40, 70)
        art = janur_tassel(art, W, H, x, y + 4, L, nx, rng, sway=rng.uniform(-0.12, 0.12))
        if k % 2 == 0:
            art = janur_tassel(art, W, H, x - 6, y + 2, L * 0.7, nx, rng, sway=rng.uniform(0.1, 0.25))
        if k % 5 == 0:
            clear()
    # woven rope: twisted strands
    for side in (-1, 1):
        twist = []
        for j, (x, y) in enumerate(pts):
            twist.append((x, y + side * 4 * math.sin(j * 1.3)))
        art = GP(art, strokes(W, H, [(twist, 10, None)]), JANUR if side < 0 else "#d7c779", JANUR_L, seed=nx(), rough=0.6, streak=0.9)
    hatch_ = [([(x - 5, y - 6), (x + 5, y + 6)], 1.4, None) for x, y in pts[::2]]
    art = G(art, strokes(W, H, hatch_), JANUR_D, seed=nx(), density=0.6, edge=0, rough=0.3, feather=0.4)
    # woven knots (ketupat-free: small rosette knots) at intervals
    for k in range(7):
        t = (k + 0.5) / 7
        x, y = pts[int(t * (len(pts) - 1))]
        art = paper_flower(art, W, H, x, y, 14, nx, rng, JANUR_L, JANUR_D, petals=8, centre=BRASS)
    preview(art, "ml-janur", bg="#123d2f")
    save(art, f"{OUT}/janur.webp", max_w=780, quality=82)
    clear()


def part_kembang():
    """Kembang endog arrangement: a brass pot wrapped in janur, bamboo skewers fanning up carrying crepe-paper
    flowers and eggs wrapped in coloured paper."""
    W, H = 440, 560
    rng = random.Random(13); nx = Seq(1300)
    art = blank(W, H)
    base = (W / 2, 430)
    cols = [("#d9473d", "#8f2420"), ("#f2a4b8", "#c0627c"), ("#f4cf5a", "#b98d1e"), ("#fdf7ee", "#cbb79b"), ("#58a882", "#1f6b4e")]
    tips = []
    n = 19
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * 0.085 + rng.uniform(-0.03, 0.03)
        L = rng.uniform(190, 300) * (1 - abs(k - (n - 1) / 2) / n * 0.6)
        tx, ty = base[0] + math.cos(a) * L, base[1] + math.sin(a) * L
        tips.append((tx, ty, a))
    sk = strokes(W, H, [([base, (base[0] + (tx - base[0]) * 0.5 + rng.uniform(-6, 6), base[1] + (ty - base[1]) * 0.5), (tx, ty)], 2.4, (0.0, 0.2)) for tx, ty, a in tips])
    art = G(art, sk, "#c9b06a", "#9c8442", seed=nx(), density=0.9, edge=0.3, rough=0.4, feather=0.4)
    order = sorted(range(n), key=lambda i: tips[i][1])
    for j, i in enumerate(order):
        tx, ty, a = tips[i]
        col, deep = cols[(i * 3) % len(cols)]
        if i % 3 == 1:
            # wrapped egg: oval with crinkled paper collar
            egg = shapes(W, H, [ellipse_pts(tx, ty, 18, 24, 16, rot=a + math.pi / 2)])
            art = body_egg(art, W, H, egg, tx, ty, col, deep, nx)
            art = paper_flower(art, W, H, tx - math.cos(a) * 24, ty - math.sin(a) * 24, 15, nx, rng, mix_hex(col, "#ffffff", 0.3), deep, petals=7)
        else:
            art = paper_flower(art, W, H, tx, ty, rng.uniform(25, 33), nx, rng, col, deep, petals=rng.choice([5, 6, 7]))
        # a pair of janur leaves on some stems
        if i % 4 == 0:
            for side in (-1, 1):
                lx, ly = base[0] + (tx - base[0]) * 0.62, base[1] + (ty - base[1]) * 0.62
                art = janur_tassel(art, W, H, lx, ly, 46, nx, rng, sway=a - math.pi / 2 + side * 0.9)
        if j % 4 == 3:
            clear()
    # pot
    pot = shape_mask(W, H, [(base[0] - 78, 420), (base[0] + 78, 420), (base[0] + 92, 470), (base[0] + 70, 540), (base[0] - 70, 540), (base[0] - 92, 470)])
    art = FO(art, pot, BRASS, seed=nx(), emboss=0.7, sparkle=0.04)
    art = G(art, pot * xgrad(W, H, base[0], base[0] + 92), BRASS_D, seed=nx(), density=0.5, edge=0.2, rough=1, feather=2)
    # janur band wrapped around the pot with a zigzag weave
    band = rect(W, H, base[0] - 92, 456, base[0] + 92, 486) * pot
    art = GP(art, band, JANUR, JANUR_L, seed=nx(), rough=0.6, streak=0.8)
    zz = [(base[0] - 92 + k * 10, 460 if k % 2 == 0 else 482) for k in range(20)]
    art = G(art, strokes(W, H, [(zz, 2, None)]) * band, JANUR_D, seed=nx(), density=0.7, edge=0, rough=0.3, feather=0.4)
    art = FO(art, ellipses(W, H, [(base[0], 422, 80, 9, 0)]), BRASS_L, seed=nx(), emboss=0.5, sparkle=0.1)
    preview(art, "ml-kembang", bg="#123d2f")
    save(art, f"{OUT}/kembang.webp", max_w=300, quality=82)
    clear()


def body_egg(art, W, H, m, x, y, col, deep, nx):
    art = GP(art, m, col, mix_hex(col, deep, 0.25), seed=nx(), rough=0.6, streak=0.5, pad=6)
    art = G(art, m * radial(W, H, x + 8, y + 8, 22), deep, seed=nx(), density=0.45, edge=0.2, rough=0.5, feather=1.5, pad=6)
    art = G(art, gaussian_filter(m * radial(W, H, x - 6, y - 8, 9), 2), "#ffffff", seed=nx(), density=0.45, edge=0, rough=0.4, feather=1, pad=6)
    foil_ = np.clip(m - gaussian_filter(m, 1.3) * 1.2, 0, 1) * 3
    return FO(art, foil_, BRASS, seed=nx(), emboss=0.4, sparkle=0.2, pad=6)


def part_star():
    """Eight-point star (two interlaced squares) in pressed gold foil with an inner octagon line and a small centre."""
    W = H = 240
    rng = random.Random(15); nx = Seq(1700)
    art = blank(W, H)
    c = W / 2
    def sq(r, rot):
        return [(c + math.cos(rot + k * math.pi / 2) * r, c + math.sin(rot + k * math.pi / 2) * r) for k in range(4)]
    star = shapes(W, H, [sq(110, math.pi / 4), sq(110, 0)], smooth=False)
    inner = shapes(W, H, [sq(84, math.pi / 4), sq(84, 0)], smooth=False)
    outline = np.clip(star - inner, 0, 1)
    oct_ = shapes(W, H, [[(c + math.cos(k * math.pi / 4 + math.pi / 8) * 58, c + math.sin(k * math.pi / 4 + math.pi / 8) * 58) for k in range(8)]], smooth=False)
    oct_line = np.clip(oct_ - shapes(W, H, [[(c + math.cos(k * math.pi / 4 + math.pi / 8) * 50, c + math.sin(k * math.pi / 4 + math.pi / 8) * 50) for k in range(8)]], smooth=False), 0, 1)
    art = G(art, inner, EMER, EMER_D, seed=nx(), density=0.85, edge=0.5, bloom=0.3, rough=1, feather=0.6)
    art = FO(art, np.maximum(outline, oct_line), BRASS, seed=nx(), emboss=0.8, sparkle=0.25)
    petals = shapes(W, H, [petal_pts(c, c, 40, 14, k * math.pi / 4, n=10) for k in range(8)])
    art = FO(art, petals, BRASS_L, seed=nx(), emboss=0.6, sparkle=0.2)
    art = G(art, circles(W, H, [(c, c, 9)]), EMER_D, seed=nx(), density=0.9, edge=0.3, rough=0.4, feather=0.5)
    preview(art, "ml-star", bg="#123d2f")
    save(art, f"{OUT}/star.webp", max_w=120, quality=86)
    clear()


def part_ground():
    """Seamless deep green ground: velvety mottling, soft brush streaks, faint gold flecks (wrap-safe)."""
    T = 320
    rng = np.random.default_rng(17)
    def wn(sig):
        n = gaussian_filter(rng.random((T, T)).astype(np.float32), sig, mode="wrap")
        return (n - n.mean()) / (n.std() + 1e-6)
    base = col_arr("#123d2f")
    v = 1 + wn(28) * 0.06 + wn(8) * 0.035 + wn(1.2) * 0.02
    streak = gaussian_filter(rng.random((T, T)).astype(np.float32), (1.0, 14), mode="wrap")
    streak = (streak - streak.mean()) / (streak.std() + 1e-6)
    rgb = np.ones((T, T, 3), np.float32) * base * (v + streak * 0.025)[..., None]
    fl = (rng.random((T, T)) > 0.9975).astype(np.float32)
    fl = gaussian_filter(fl, 0.7, mode="wrap") * 3
    rgb = rgb * (1 - fl[..., None] * 0.6) + col_arr("#c9a24a")[None, None, :] * fl[..., None] * 0.6
    rgb = np.clip(rgb, 0, 1)
    prev_rgb(np.tile(rgb, (2, 2, 1)), "ml-ground")
    rgb_save(rgb, f"{OUT}/ground.webp", quality=72)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
