"""Cirebon Kasepuhan — original design inspired by the red-brick keraton of Cirebon: a split gate (candi bentar) of
fired red brick with lime mortar, inset with Chinese blue-and-white, polychrome and European blue porcelain plates,
on grotto rocks of a taman sari (wadasan-like layered rock forms). No figures.
Run: python3 -I cirebon-kasepuhan.py [part ...]  parts: plates gate wadas ring brick divider
Assets -> public/themes/art/cirebon-kasepuhan/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d2_lib import *

OUT = outdir("cirebon-kasepuhan")
PARTS = sys.argv[1:] or ["plates", "gate", "wadas", "ring", "brick", "divider"]
BR, BR_D, BR_L, MORT = "#b4482e", "#7f2c1c", "#cf6a45", "#efe3cf"

if "plates" in PARTS:
    for name, style, sd in [("plate-b", "blue", 3), ("plate-p", "poly", 5), ("plate-d", "delf", 7)]:
        W = H = 280
        nx = Seq(sd * 100); rng = random.Random(sd)
        art = plate(blank(W, H), W, H, 140, 140, 128, style, nx, rng)
        preview(art, name, bg="#b4482e")
        save(art, f"{OUT}/{name}.webp", max_w=200, quality=84)
        clear()


def tiers():
    # (y_top, y_bottom, x_left) — the inner edge of the half gate is the straight cut at x = W
    return [(1040, 1100, 0), (700, 1040, 34), (672, 700, 12), (520, 672, 74), (500, 520, 58), (392, 500, 126),
            (376, 392, 114), (292, 376, 176), (280, 292, 166), (222, 280, 222), (212, 222, 214), (162, 212, 262), (120, 162, 296)]


if "gate" in PARTS:
    W, H = 360, 1120
    nx = Seq(700); rng = random.Random(11)
    art = blank(W, H)
    T = tiers()
    rects = [rect(W, H, x0, y0, W, y1) for (y0, y1, x0) in T]
    # rounded mustaka cap on top of the last tier
    cap = shapes(W, H, [[(W, 124), (300, 124)] + [(W - 2 + math.cos(a) * 60, 124 + math.sin(a) * 74) for a in np.linspace(math.pi, math.pi * 1.5, 16)] + [(W, 50)]], smooth=False)
    mass = np.maximum(np.maximum.reduce(rects), cap)
    # stepped antefix notches on the outer top corner of each tier
    notch = []
    for (y0, y1, x0) in T[1:]:
        if y1 - y0 > 60:
            notch.append([(x0, y0), (x0, y0 - 22), (x0 + 10, y0 - 22), (x0 + 10, y0 - 34), (x0 + 22, y0 - 34), (x0 + 22, y0)])
    mass = np.maximum(mass, shapes(W, H, notch, smooth=False))
    bseed = nx()
    art = bricks(art, mass, W, H, BR_L, BR, MORT, seed=bseed, bw=26, bh=9)
    bm, tone = brick_field(W, H, 26, 9, 1.6, bseed)
    tone2 = (tone * 7.31) % 1.0
    art = over(art, flat(mass * bm * (tone2 > 0.86), BR_D, 0.45))
    art = over(art, flat(mass * bm * (tone2 < 0.08), "#e39a72", 0.4))
    # mortar joints read recessed: thin shadow under each brick course
    art = over(art, flat(mass * np.clip(np.roll(bm, 1, 0) - bm, 0, 1), "#4a1a10", 0.35))
    art = over(art, flat(mass * (1 - bm) * np.clip((fbm(W, H, bseed + 9, 6, 2) - 0.5) * 3, 0, 1), "#9b8a74", 0.5))
    art = add_grain(art, bseed, 0.06)
    # weathering: darker fired bricks, soot stains running down, lime bloom
    st = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (18, 1.2))
    st = np.clip((st - 0.5) * 8, 0, 1)
    art = over(art, flat(mass * st, BR_D, 0.28))
    bloom_ = np.clip((fbm(W, H, nx(), 50, 3) - 0.62) * 3, 0, 1)
    art = over(art, flat(mass * bloom_, "#f1e3cf", 0.18))
    # cornice shadows under each projecting band, and highlight on the top lip
    for (y0, y1, x0) in T:
        sh = rect(W, H, x0 + 6, y1, W, y1 + 10) * mass
        art = over(art, flat(gaussian_filter(sh, 2.5), "#3a140c", 0.55))
        lip = rect(W, H, x0, y0, W, y0 + 3) * mass
        art = over(art, flat(lip, "#f0b090", 0.35))
        side = rect(W, H, x0, y0, x0 + 5, y1) * mass
        art = over(art, flat(side, "#ffd0b0", 0.18))
    # the inner cut face catches less light
    art = over(art, flat(mass * rect(W, H, W - 16, 0, W, H), "#5a1e12", 0.3))
    # inset porcelain plates (recessed niches + plate) and small square tiles
    plates_at = [(170, 790, 54, "blue"), (170, 930, 40, "poly"), (90, 1000, 0, ""), (232, 590, 40, "delf"), (232, 445, 30, "blue"),
                 (282, 334, 24, "poly"), (300, 250, 18, "blue"), (320, 186, 14, "delf"), (290, 870, 26, "delf"), (80, 870, 26, "delf"), (125, 590, 26, "poly")]
    for (px, py, pr, style) in plates_at:
        if not pr:
            continue
        niche = circles(W, H, [(px, py, pr + 4)])
        art = over(art, flat(niche, "#e9dcc6", 1.0))
        art = over(art, flat(gaussian_filter(ring_m(W, H, px + 1.5, py + 2, pr - 2, pr + 3), 1.4), "#3a140c", 0.55))
        art = plate(art, W, H, px, py, pr, style, nx, rng)
        clear()
    tiles = []
    for (tx, ty) in [(80, 760), (80, 980), (280, 760), (280, 980), (150, 480), (150, 410)]:
        tiles.append((tx, ty))
    for (tx, ty) in tiles:
        s = 13
        tm = rect(W, H, tx - s, ty - s, tx + s, ty + s)
        art = GP(art, tm, "#f5f1e8", "#e3ddd0", seed=nx(), rough=0.4, pad=6)
        dm = shapes(W, H, [[(tx, ty - s * 0.8), (tx + s * 0.8, ty), (tx, ty + s * 0.8), (tx - s * 0.8, ty)]], smooth=False)
        art = G(art, np.clip(dm - circles(W, H, [(tx, ty, s * 0.32)]), 0, 1), "#2e52a6", seed=nx(), density=0.8, edge=0.6, rough=0.6, feather=0.5, pad=6)
        art = over(art, flat(gaussian_filter(np.clip(rect(W, H, tx - s - 2, ty - s - 2, tx + s + 2, ty + s + 2) - tm, 0, 1), 0.8), "#3a140c", 0.4))
    # light from the upper left over the whole half; ground shadow at the foot
    art = over(art, flat(mass * light_mask(H, W, -120, 300, 900), "#ffcf9e", 0.16))
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = over(art, flat(mass * np.clip((yy - 0.9) / 0.1, 0, 1), "#3a140c", 0.25))
    preview(art, "gate", bg="#f1e8da")
    save(art, f"{OUT}/gate.webp", max_w=300, quality=82)
    clear()


def lobes(rng, W, base, n, x0, x1, hmin, hmax):
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * (i + rng.uniform(0.1, 0.9)) / n
        h = rng.uniform(hmin, hmax)
        out.append((x, base - h * 0.5, rng.uniform(40, 80), h * 0.55, rng.uniform(-14, 14)))
    return out


def paint_rocks(art, W, H, blobs, nx, col, col2, shade, lines=True):
    for (cx, cy, rx, ry, rot) in blobs:
        m = displace(ellipses(W, H, [(cx, cy, rx, ry, rot)]), nx(), 5, 50)
        art = GP(art, m, col, col2, seed=nx(), rough=1.6, streak=0.6)
        # light from upper left; underside in cool shadow
        art = over(art, flat(m * light_mask(H, W, cx - rx * 0.5, cy - ry * 0.8, max(rx, ry) * 1.6), "#fbf3e2", 0.35))
        art = over(art, flat(m * np.clip(1 - light_mask(H, W, cx - rx * 0.3, cy - ry * 0.5, max(rx, ry) * 2.0) * 1.5, 0, 1), shade, 0.45))
        if lines:
            # wadasan-like layered contours following the top of each lobe
            items = []
            for k in range(1, 4):
                s = 1 - k * 0.22
                pts = [(cx + math.cos(a) * rx * s, cy + math.sin(a) * ry * s - ry * (1 - s) * 0.5) for a in np.linspace(math.pi * 1.08, math.pi * 1.92, 16)]
                items.append((pts, 2.2 - k * 0.3, (0.25, 0.25)))
            art = over(art, flat(strokes(W, H, items) * m, shade, 0.55))
        pores = circles(W, H, [(cx + rx * random.uniform(-.7, .7), cy + ry * random.uniform(-.2, .7), random.uniform(1.5, 4)) for _ in range(int(rx / 9))])
        art = over(art, flat(pores * m, "#4c4a4f", 0.5))
        art = over(art, flat(gaussian_filter(np.clip(outline(m, 2.0), 0, 1), 0.6), shade, 0.5))
    return art


def grotto(art, W, H, top, nx, col, col2, shade, terr=7, holes=0.5, seed=1):
    """Taman-sari grotto rock: silhouette from a top profile, terraced height field -> stratified ledges lit from
    the upper left (wadasan-like layered contours), cavities with dark interiors."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    m = (yy > top[None, :]).astype(np.float32)
    m = gaussian_filter(displace(m, seed, 5, 40), 0.8)
    hf = fbm(W, H, seed + 1, 170, 3) * 0.45 + (1 - yy / H) * 0.9 + np.abs(xx - W / 2) / W * 0.25 + fbm(W, H, seed + 2, 40, 2) * 0.05
    q = np.floor(hf * terr) / terr
    qs = gaussian_filter(q, 2.2)
    gy, gx = np.gradient(qs)
    lit = np.clip(-(gx * -0.7 + gy * -0.7) * 45, -1, 1)
    base = gouache_paint(m, col, col2, seed=seed + 3, rough=1.5, streak=0.7)
    base[..., :3] *= (0.92 + 0.12 * (hf[..., None] - 0.5))
    art = over(art, base)
    art = over(art, flat(m * np.clip(lit, 0, 1), "#fff6e6", 0.55))
    art = over(art, flat(m * np.clip(-lit, 0, 1), shade, 0.75))
    moss = np.clip((fbm(W, H, seed + 8, 50, 3) - 0.6) * 4, 0, 1) * m
    art = over(art, flat(moss, "#8a8f5a", 0.25))
    # cool shadow pooling toward the bottom of each terrace
    frac = hf * terr - np.floor(hf * terr)
    art = over(art, flat(m * np.clip(0.35 - frac, 0, 1) * 2, shade, 0.25))
    if holes:
        hm = np.clip((fbm(W, H, seed + 5, 34, 2) - (1 - holes * 0.22)) * 8, 0, 1) * m * (yy > top[None, :] + 30)
        art = over(art, flat(gaussian_filter(hm, 1.0), "#2c2a33", 0.85))
        rim = np.clip(np.roll(gaussian_filter(hm, 1.5), 3, 0) - hm, 0, 1)
        art = over(art, flat(rim, "#fff3de", 0.5))
    art = over(art, flat(gaussian_filter(outline(m, 1.6), 0.6), shade, 0.6))
    return art, m


def profile(W, base, peaks, rng):
    x = np.arange(W, dtype=np.float32)
    y = np.full(W, float(base))
    for (px, ph, pw) in peaks:
        y -= ph * np.exp(-((x - px) / pw) ** 2)
    y += np.array([rng.uniform(-1, 1) for _ in range(W)], np.float32)
    y = gaussian_filter(y, 2)
    jag = np.abs(np.sin(x / 9.0 + rng.uniform(0, 6))) * 6
    return y - jag


if "wadas" in PARTS:
    W, H = 800, 330
    nx = Seq(1500); rng = random.Random(5); random.seed(5)
    art = blank(W, H)
    back = profile(W, 250, [(40, 170, 60), (150, 120, 50), (250, 70, 40), (560, 90, 50), (660, 150, 50), (770, 190, 60)], rng)
    art, _ = grotto(art, W, H, back, nx, "#a99f92", "#bfb4a2", "#5b6176", terr=6, seed=nx())
    clear()
    front = profile(W, 300, [(90, 120, 70), (210, 70, 50), (330, 30, 50), (470, 34, 50), (600, 80, 50), (720, 120, 70)], rng)
    art, _ = grotto(art, W, H, front, nx, "#cbbfa8", "#ddd1b9", "#566079", terr=5, holes=0.7, seed=nx())
    clear()
    # a calm grotto pool along the bottom with floating lotus pads
    pool = rect(W, H, -10, 292, W + 10, H)
    art = knockout(art, pool, 1.0, 1.0)
    art = G(art, pool, "#5d86b8", "#8db0d4", seed=nx(), density=0.95, edge=0.4, bloom=0.4, rough=2, feather=1.2)
    art = over(art, flat(ripple_lines(W, H, 298, H, nx(), 1.2, 20, 70) * pool, "#e9f1f6", 0.7))
    pads = ellipses(W, H, [(x, 312 + rng.uniform(-6, 10), rng.uniform(16, 26), 6, rng.uniform(-6, 6)) for x in (70, 120, 520, 610, 700)])
    art = G(art, pads, "#4f8a55", "#7fae5a", seed=nx(), density=0.9, edge=0.6, rough=1, feather=0.6)
    buds = [petal_pts(x, 306, 20, 8, -1.57 + o, n=10, cup=0.2) for x in (120, 610) for o in (-0.35, 0, 0.35)]
    art = G(art, shapes(W, H, buds), "#e98aa0", "#f6c0c8", seed=nx(), density=0.85, edge=0.7, rough=0.6, feather=0.6)
    # ferns tucked into the rock crevices
    fr = []
    for (fx, fy, ang, L) in [(30, 200, -1.2, 90), (230, 230, -1.9, 70), (760, 190, -2.0, 90), (660, 250, -1.5, 60)]:
        stem = [(fx + math.cos(ang + t * 0.6) * L * t, fy + math.sin(ang + t * 0.6) * L * t) for t in np.linspace(0, 1, 14)]
        fr.append((stem, 2.0, (0.1, 0.5)))
        for i, (sx, sy) in enumerate(stem[2:-1]):
            for sgn in (-1, 1):
                a = ang + 0.6 * i / 12 + sgn * 1.0
                ll = L * 0.22 * (1 - i / 14)
                fr.append(([(sx, sy), (sx + math.cos(a) * ll, sy + math.sin(a) * ll)], 3.2, (0.1, 0.8)))
    art = G(art, strokes(W, H, fr), "#3f7a4a", "#6f9a4a", seed=nx(), density=0.9, edge=0.5, rough=0.8, feather=0.6)
    preview(art, "wadas", bg="#f1e8da")
    save(art, f"{OUT}/wadas.webp", max_w=780, quality=80)
    clear()

if "ring" in PARTS:
    W = H = 520
    nx = Seq(2600); rng = random.Random(9)
    art = plate(blank(W, H), W, H, 260, 260, 250, "blue", nx, rng)
    hole = circles(W, H, [(260, 260, 250 * 0.635)])
    art[..., 3] *= 1 - hole
    # inner shadow cast by the rim onto the photo
    sh = np.clip(gaussian_filter(1 - circles(W, H, [(262, 264, 250 * 0.62)]), 5) * hole, 0, 1)
    art = over(art, flat(sh, "#1d2a4a", 0.6))
    preview(art, "ring", bg="#b4482e")
    save(art, f"{OUT}/ring.webp", max_w=460, quality=82)
    clear()

if "brick" in PARTS:
    W, H = 256, 256
    bm, tone = brick_field(W, H, 32, 8, 1.6, 3)
    ca, cb = col_arr(BR_L), col_arr(BR)
    t2 = (tone * 7.31) % 1.0
    rgb = ca * (1 - tone[..., None]) + cb * tone[..., None]
    rgb = rgb * (0.92 + 0.16 * wrap_noise(W, H, 4, 1.5)[..., None])
    rgb = np.where((t2 > 0.86)[..., None], rgb * 0.78, rgb)
    mc = col_arr(MORT) * (0.85 + 0.15 * wrap_noise(W, H, 6, 1.0)[..., None])
    rgb = rgb * bm[..., None] + mc * (1 - bm[..., None])
    rgb = rgb * (1 - np.clip(np.roll(bm, 1, 0) - bm, 0, 1)[..., None] * 0.35)
    img = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_rgb(img, f"{OUT}/brick.webp", quality=78)

if "divider" in PARTS:
    W, H = 440, 90
    nx = Seq(3100); rng = random.Random(4)
    art = blank(W, H)
    for (x0, x1) in [(10, 150), (290, 430)]:
        band = rect(W, H, x0, 38, x1, 52)
        art = bricks(art, band, W, H, BR_L, BR, MORT, seed=nx(), bw=20, bh=7)
        art = over(art, flat(rect(W, H, x0, 52, x1, 55), "#3a140c", 0.3))
    for tx in (162, 278):
        s = 9
        art = GP(art, rect(W, H, tx - s, 45 - s, tx + s, 45 + s), "#f5f1e8", seed=nx(), rough=0.4, pad=6)
        art = G(art, shapes(W, H, [[(tx, 45 - s * 0.75), (tx + s * 0.75, 45), (tx, 45 + s * 0.75), (tx - s * 0.75, 45)]], smooth=False), "#2e52a6", seed=nx(), density=0.85, rough=0.5, feather=0.5, pad=6)
    art = plate(art, W, H, 220, 45, 40, "delf", nx, rng)
    preview(art, "divider", bg="#f1e8da")
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)
    clear()
