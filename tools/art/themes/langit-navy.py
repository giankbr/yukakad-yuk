"""Langit Navy — painted night: gouache sky with hills and cloud wisps (cover), painted crescent moon, gold-gouache
star, constellation in gold ink, seamless star-speckle tile.
Run: python3 -I /tmp/pen/art/themes/langit-navy.py [sky|moon|star|const|stars]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _b_common import *  # noqa

T = "langit-navy"
D = outdir(T)
nxt = Seeds(900)
rng = random.Random(3)
GOLD, GOLD_L, GOLD_D = "#d6b46a", "#f1dca4", "#b08d45"
CREAM = "#f6e7bd"


def star_shape(cx, cy, r, inner=0.22, rot=0.0, wob=0.0):
    pts = []
    for i in range(8):
        a = rot + i * math.pi / 4
        rr = r if i % 2 == 0 else r * inner
        rr *= 1 + (rng.gauss(0, wob) if wob else 0)
        pts.append((cx + math.cos(a - math.pi / 2) * rr, cy + math.sin(a - math.pi / 2) * rr))
    return pts


# ---------- 1. cover sky ----------
def sky():
    W, H = 640, 1386
    rng.seed(4)
    art = painted_sky(W, H, [(0, "#0d1a3a"), (0.18, "#162c5a"), (0.42, "#1d3a72"), (0.62, "#173061"), (0.8, "#0f2048"), (1, "#081430")], seed=nxt(), streak=1.2, grain=0.8)
    # moon-glow wash high up (where the moon sits)
    gl = np.zeros((H, W), np.float32)
    gl = shape_mask(W, H, ellipse_pts(W * .5, H * .17, 170, 150, 20))
    art = over(art, glow(gl, "#3b5c9c", radius=70, strength=0.35))
    # cloud wisps: thin, transparent watercolour bands lit from the moon side
    for (y, x0, x1, th, col, d) in [(0.35, -0.1, 0.5, 18, "#4a68a6", 0.22), (0.375, 0.42, 1.1, 12, "#4664a0", 0.2),
                                    (0.57, -0.1, 0.38, 10, "#3d5a94", 0.16), (0.61, 0.62, 1.1, 16, "#3d5a94", 0.18),
                                    (0.74, 0.05, 0.95, 22, "#304c86", 0.2)]:
        pts = curve([(W * x0, H * y + rng.uniform(-8, 8)), (W * (x0 + x1) / 2, H * y - rng.uniform(4, 16)), (W * x1, H * y + rng.uniform(-8, 8))], 50)
        m = gaussian_filter(stroke_mask(W, H, pts, th, (0.4, 0.4)), 2)
        art = over(art, pigment(m, col, mix(col, "#6d86bb", .3), seed=nxt(), density=d, edge=0.25, bloom=0.5, gran=0.2, feather=3, rough=14, mottle=0.8))
    # stars: gouache dabs of different sizes; a few 4-point glints
    dots = []
    for _ in range(70):   # sparse field
        dots.append((rng.uniform(0, W), rng.uniform(0, H * 0.8), rng.choice([0.8, 1.0, 1.2, 1.5, 1.9])))
    for _ in range(170):  # a faint diagonal band of tiny stars (milky way)
        t = rng.random()
        x = W * (-0.1 + 1.2 * t) + rng.gauss(0, 46)
        y = H * (0.62 - 0.5 * t) + rng.gauss(0, 46)
        dots.append((x, y, rng.choice([0.9, 1.0, 1.1, 1.3])))
    for _ in range(6):
        dots.append((rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(2.2, 2.8)))
    band = np.zeros((H, W), np.float32)
    band = stroke_mask(W, H, [(W * (-0.1 + 1.2 * t), H * (0.62 - 0.5 * t)) for t in np.linspace(0, 1, 20)], 90, (0.3, 0.3))
    art = over(art, pigment(gaussian_filter(band, 30), "#3a5794", "#4f6aa3", seed=nxt(), density=0.3, edge=0.0, bloom=0.6, gran=0.3, feather=8, rough=30, mottle=1.0))
    dm = dots_mask(W, H, dots)
    art = over(art, glow(dm, "#f1dca4", radius=3, strength=0.25))
    art = over(art, gouache_paint(dm, "#fbf3d8", "#f1dca4", seed=nxt(), rough=0.8, streak=0.2, density=0.9))
    big = np.zeros((H, W), np.float32)
    for (x, y, r) in [(0.08, 0.14, 13), (0.86, 0.1, 10), (0.9, 0.58, 12), (0.07, 0.72, 9), (0.74, 0.3, 7)]:
        big = np.maximum(big, shape_mask(W, H, star_shape(W * x, H * y, r, 0.2, rng.uniform(-0.15, .15), 0.06), smooth=False))
    art = over(art, glow(big, GOLD_L, radius=8, strength=0.4))
    art = over(art, gouache_paint(big, GOLD_L, GOLD, seed=nxt(), rough=1.0, streak=0.3))
    # hills: three layered gouache ridges at the bottom, darkest in front
    for k, (base_y, amp, col, col2) in enumerate([(0.83, 40, "#132a58", "#18326a"), (0.88, 34, "#0d1f45", "#112653"), (0.93, 26, "#08142f", "#0a1838")]):
        pts = [(-20, H + 20)]
        n = 9
        ph = rng.uniform(0, 6)
        for i in range(n + 1):
            x = -20 + (W + 40) * i / n
            y = H * base_y - amp * (0.6 * math.sin(i * 0.9 + ph) + 0.4 * math.sin(i * 2.1 + ph * 2))
            pts.append((x, y))
        pts.append((W + 20, H + 20))
        m = shape_mask(W, H, pts)
        if k == 2:  # small stylised trees on the front ridge
            for tx in [0.06, 0.1, 0.15, 0.78, 0.83, 0.9, 0.95]:
                x = W * tx + rng.uniform(-6, 6)
                i = min(n, max(0, int(round((x + 20) / (W + 40) * n))))
                yb = np.interp(x, [p_[0] for p_ in pts[1:-1]], [p_[1] for p_ in pts[1:-1]]) + 6
                hgt = rng.uniform(34, 58)
                for tier in range(3):
                    top = yb - hgt + tier * hgt * 0.26
                    bot = top + hgt * 0.5
                    wd = hgt * (0.13 + tier * 0.06)
                    m = np.maximum(m, shape_mask(W, H, deform([(x, top), (x + wd, bot), (x - wd, bot)], rng, 2, .04), smooth=False))
                m = np.maximum(m, stroke_mask(W, H, [(x, yb - hgt * .3), (x, yb + 4)], 2.4))
        layer = gouache_paint(m, col, col2, seed=nxt(), rough=3, streak=0.8)
        rim = np.clip(m - np.roll(gaussian_filter(m, 2.0), 5, axis=0), 0, 1)
        layer = tint(layer, gaussian_filter(rim, 1.5), "#4c6aa8", 0.32 - k * 0.08)
        art = over(art, layer)
        if k == 1:  # a few warm village lights on the middle ridge
            lights = [(W * rng.uniform(0.15, 0.9), H * (base_y + 0.025) + rng.uniform(0, 14), rng.uniform(1.3, 2.0)) for _ in range(9)]
            lm = dots_mask(W, H, lights)
            art = over(art, glow(lm, "#f3c46b", radius=4, strength=0.5))
            art = over(art, gouache_paint(lm, "#ffd98a", seed=nxt(), rough=0.5, density=0.95))
    art[..., 3] = 1
    im = Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")
    im.save(f"{D}/sky.webp", "WEBP", quality=84, method=6)
    im.save(f"{PREV}/ln-sky.png")
    print("sky.webp", os.path.getsize(f"{D}/sky.webp") // 1024, "KB")


# ---------- 2. painted crescent moon ----------
def moon():
    W = H = 360
    c = 180
    R = 104
    disc = shape_mask(W, H, deform(ellipse_pts(c, c, R, R, 40), rng, 1, .004))
    bite = shape_mask(W, H, ellipse_pts(c + 52, c - 40, R * 0.9, R * 0.9, 40))
    cres = np.clip(disc - gaussian_filter(bite, 1.2) * 1.05, 0, 1)
    art = blank(W, H)
    art = over(art, glow(cres, "#f1dca4", radius=22, strength=0.22))
    body = gouache_paint(cres, "#f6e3ae", "#e8ca88", seed=nxt(), rough=1.8, streak=0.2)
    body = glaze(body, pigment(cres, "#f3dca0", "#e6c27a", seed=nxt(), density=0.35, edge=0.35, bloom=0.5, gran=0.3, feather=1.2, rough=3, mottle=0.9))
    body = shade(body, cres, light=(-0.6, -0.5), k=0.22, blur=14, hi="#fff6dc", lo="#b88f48")
    # craters / maria as soft watercolour glazes
    cr = np.zeros((H, W), np.float32)
    for (x, y, r) in [(c - 60, c + 18, 22), (c - 34, c + 66, 14), (c - 76, c - 22, 10)]:
        cr = np.maximum(cr, shape_mask(W, H, deform(ellipse_pts(x, y, r, r * .8, 10), rng, 2, .15)))
    body = glaze(body, pigment(cr * cres, "#d9b673", "#c9a35c", seed=nxt(), density=0.22, edge=0.35, bloom=0.4, rough=4, feather=2))
    art = over(art, body)
    preview(art, f"{PREV}/ln-moon.png", "#13254a")
    save(art, f"{D}/moon.webp", max_w=240, q=84, trim=False)


# ---------- 3. gold gouache star ----------
def star():
    W = H = 96
    rng.seed(9)
    m = shape_mask(W, H, star_shape(48, 48, 36, 0.2, 0.04, 0.04), smooth=False)
    m = gaussian_filter(m, 0.6)
    art = blank(W, H)
    art = over(art, glow(m, GOLD_L, radius=5, strength=0.35))
    body = gouache_paint(m, GOLD_L, GOLD, seed=nxt(), rough=0.8, streak=0.4)
    body = shade(body, m, light=(-0.6, -0.7), k=0.25, blur=2, hi="#fff3cf", lo="#9c7a38")
    art = over(art, body)
    preview(art, f"{PREV}/ln-star.png", "#13254a")
    save(art, f"{D}/star.webp", max_w=48, q=86, trim=False)


# ---------- 4. constellation (gold ink) ----------
def const():
    W, H = 640, 180
    pts = [(24, 144), (138, 66), (276, 102), (384, 30), (510, 90), (618, 54)]
    line = np.zeros((H, W), np.float32)
    for a, b in zip(pts, pts[1:]):
        seg = [(a[0] + (b[0] - a[0]) * t + rng.gauss(0, .4), a[1] + (b[1] - a[1]) * t + rng.gauss(0, .4)) for t in np.linspace(0.06, 0.94, 14)]
        line = np.maximum(line, stroke_mask(W, H, seg, 2.4, (0.2, 0.2)))
    art = blank(W, H)
    art = over(art, pigment(line, "#e8cf8e", "#cfb06a", seed=nxt(), density=0.7, edge=0.3, bloom=0, gran=0.4, feather=0.6, rough=1.2, holes=0.08))
    dots = np.zeros((H, W), np.float32)
    for i, (x, y) in enumerate(pts):
        r = 9 if i % 2 == 0 else 6.5
        dots = np.maximum(dots, shape_mask(W, H, deform(ellipse_pts(x, y, r, r, 10), rng, 1, .05)))
    art = over(art, glow(dots, GOLD_L, radius=9, strength=0.32))
    art = over(art, shade(gouache_paint(dots, "#fbefc6", GOLD_L, seed=nxt(), rough=0.8), dots, k=0.3, blur=2, hi="#ffffff", lo="#b08d45"))
    preview(art, f"{PREV}/ln-const.png", "#13254a")
    save(art, f"{D}/constellation.webp", max_w=428, q=84, trim=False)


# ---------- 5. seamless star speckle tile (transparent) ----------
def stars():
    S = 520
    r2 = random.Random(31)
    dots = []
    for _ in range(46):
        x, y = r2.uniform(0, S), r2.uniform(0, S)
        r = r2.choice([0.9, 1.1, 1.3, 1.5, 1.8]) if r2.random() < 0.88 else r2.uniform(2.0, 2.6)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                dots.append((x + ox, y + oy, r))
    m = dots_mask(S, S, dots)
    art = blank(S, S)
    art = over(art, glow(m, "#f1dca4", radius=2.5, strength=0.2))
    a = gouache_paint(m, "#fbf3dc", "#efd9a2", seed=nxt(), rough=0.4, streak=0.1, density=0.85)
    # vary brightness per star a little
    v = fbm(S, S, 5, 40, 2)
    a[..., 3] *= 0.55 + 0.45 * v
    art = over(art, a)
    save(art, f"{D}/stars.webp", q=80, trim=False)


if __name__ == "__main__":
    for w in sys.argv[1:] or ["sky", "moon", "star", "const", "stars"]:
        {"sky": sky, "moon": moon, "star": star, "const": const, "stars": stars}[w]()
