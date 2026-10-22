"""Gurun Kaktus — desert boho in dry-brush gouache: a painted sunset sky, layered mesas with strata and dunes (the photo
sets behind them like the sun), saguaros with ribbed arms and spines, prickly-pear pads with coral fruit, echeveria
rosettes, a dune band, a cactus-and-sun divider and a sandy paper tile.
Run: python3 -I gurun-kaktus.py [part ...]   parts: sky land saguaro pear succulent dunes divider paper"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e4_lib import *

OUT = outdir("gurun-kaktus")
PARTS = sys.argv[1:] or ["sky", "land", "saguaro", "pear", "succulent", "dunes", "divider", "paper"]
SAND = "#efd6b5"
TERRA, TERRA_D, CORAL, PEACH, ROSE = "#c0643c", "#9c4a2c", "#e8875a", "#f2b48a", "#d99a8a"
SAGE, SAGE_D, SAGE_L, PLUM = "#7f9a6e", "#56704f", "#a9bc94", "#4a2a26"


def offset_line(pts, d):
    out = []
    n = len(pts)
    for i in range(n):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        out.append((pts[i][0] - ty / L * d, pts[i][1] + tx / L * d))
    return out


def cactus_limb(art, W, H, pts, w, nx, rng, light=-1):
    """One ribbed cactus column along pts (bottom → top): dry gouache body, a shadow side, rib lines, spine ticks."""
    m = strokes(W, H, [(pts, w, None)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = DG(art, m, SAGE, SAGE_L if light < 0 else SAGE, seed=nx(), u=yy * 1.0, v=xx, dry=0.35, rough=1.4)
    sh = strokes(W, H, [(offset_line(pts, -light * w * 0.28), w * 0.42, None)]) * m
    art = G(art, gaussian_filter(sh, 2), SAGE_D, "#4a6046", seed=nx(), density=0.55, edge=0.2, bloom=0.3, gran=0.4, rough=1.5, feather=1.2)
    hl = strokes(W, H, [(offset_line(pts, light * w * 0.26), w * 0.16, (0.1, 0.2))]) * m
    art = OV(art, gaussian_filter(hl, 1.6), lambda mm: layer(mm, "#d9e2b8", 0.35))
    ribs = []
    for k in (-0.36, -0.12, 0.12, 0.36):
        ribs.append((offset_line(pts, k * w), max(1.2, w * 0.035), (0.04, 0.04)))
    rm = strokes(W, H, ribs) * np.clip(gaussian_filter(m, 1) * 1.2 - 0.1, 0, 1)
    art = G(art, rm, "#4f6a48", seed=nx(), density=0.6, edge=0.1, bloom=0, gran=0.3, rough=0.6, feather=0.4)
    sp = []
    for k in (-0.24, 0.0, 0.24):
        for (x, y, a) in along(offset_line(pts, k * w), max(6, w * 0.22)):
            if rng.random() < 0.8:
                for dd in (-0.7, 0.7):
                    L = w * 0.09
                    sp.append(([(x, y), (x + math.cos(a + math.pi / 2 + dd) * L, y + math.sin(a + math.pi / 2 + dd) * L)], max(0.8, w * 0.018), None))
    art = OV(art, strokes(W, H, sp) * m, lambda mm: layer(mm, "#f3ead0", 0.8))
    return art


def saguaro(art, W, H, x, base, h, w, nx, rng, arms=((0.42, -1, 0.3, 0.32), (0.55, 1, 0.26, 0.28)), light=-1):
    """arms: (height fraction, side, reach fraction of h, rise fraction of h)."""
    for (f, side, reach, rise) in arms:
        y0 = base - h * f
        ax = x + side * w * 0.3
        elbow = (x + side * h * reach, y0 + w * 0.1)
        top = (x + side * h * reach, y0 - h * rise)
        arm = curve([(ax, y0), ((ax + elbow[0]) / 2, y0 + w * 0.25), elbow, ((elbow[0] + top[0]) / 2, (elbow[1] + top[1]) / 2), top], 40)
        art = cactus_limb(art, W, H, arm, w * 0.72, nx, rng, light)
    trunk = curve([(x, base), (x + rng.uniform(-4, 4), base - h * 0.5), (x + rng.uniform(-3, 3), base - h)], 50)
    return cactus_limb(art, W, H, trunk, w, nx, rng, light)


def pear(art, W, H, pads, nx, rng, fruits=True):
    """pads: list of (cx, cy, rx, ry, rot_deg) drawn in order (back → front)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for (cx, cy, rx, ry, rot) in pads:
        m = ellipses(W, H, [(cx, cy, rx, ry, rot)])
        m = displace(m, nx(), 2.0, 30)
        art = knockout(art, m, 0.7, 1.5)
        art = DG(art, np.clip(gaussian_filter(m, 1.0) * 1.3, 0, 1), "#4f6a48", seed=nx(), dry=0.15, rough=1.0)
        art = DG(art, ellipses(W, H, [(cx, cy, rx * 0.94, ry * 0.95, rot)]), "#86a37a", "#9db28a", seed=nx(), u=yy, v=xx, dry=0.35, rough=1.4)
        art = G(art, gaussian_filter(ellipses(W, H, [(cx + rx * 0.35, cy + ry * 0.25, rx * 0.6, ry * 0.7, rot)]), 6) * m, SAGE_D, seed=nx(), density=0.45, edge=0.1, bloom=0.3, gran=0.4, rough=2, feather=2)
        # areoles: dotted grid with tiny spines
        dots, sp = [], []
        r = math.radians(rot)
        for i in range(-3, 4):
            for j in range(-4, 5):
                u, v = i * rx * 0.27 + (j % 2) * rx * 0.13, j * ry * 0.21
                if (u / rx) ** 2 + (v / ry) ** 2 > 0.72:
                    continue
                px, py = cx + u * math.cos(r) - v * math.sin(r), cy + u * math.sin(r) + v * math.cos(r)
                dots.append((px, py, max(1.4, rx * 0.035)))
                for a in (-0.6, 0.0, 0.6):
                    sp.append(([(px, py), (px + math.cos(a - math.pi / 2 + r) * rx * 0.1, py + math.sin(a - math.pi / 2 + r) * rx * 0.1)], 0.9, None))
        art = OV(art, circles(W, H, dots), lambda mm: layer(mm, "#e9d9a8", 0.95))
        art = OV(art, strokes(W, H, sp), lambda mm: layer(mm, "#f4ecd2", 0.7))
    if fruits:
        fr = []
        for (cx, cy, rx, ry, rot) in pads[-3:]:
            r = math.radians(rot)
            for t in (-0.45, 0.0, 0.45):
                if rng.random() < 0.75:
                    px, py = cx + math.sin(r) * ry * 0.98 * -1 + math.cos(r) * rx * t, cy - math.cos(r) * ry * 0.98 + math.sin(r) * rx * t
                    fr.append((px, py - ry * 0.12, rx * 0.17, ry * 0.2, rot + t * 30))
        if fr:
            fm = ellipses(W, H, fr)
            art = DG(art, fm, "#c94c62", "#d9655e", seed=nx(), dry=0.2, rough=1.0)
            art = G(art, gaussian_filter(fm, 3) * fm, "#8f2a40", seed=nx(), density=0.35, edge=0.3, bloom=0.2, rough=1, feather=1.5)
    return art


def echeveria(art, W, H, cx, cy, R, nx, rng, tip=ROSE, tilt=0.55):
    """Rosette seen at an angle: rings of fleshy pointed leaves, outer first."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for ring, (k, n, L) in enumerate([(1.0, 13, 0.55), (0.75, 11, 0.5), (0.5, 9, 0.48), (0.28, 7, 0.5)]):
        polys = []
        off = rng.uniform(0, 1)
        for i in range(n):
            a = (i + off) / n * math.tau
            r0 = R * k * 0.45
            px, py = cx + math.cos(a) * r0, cy + math.sin(a) * r0 * tilt
            ln = R * k * L * 1.25
            polys.append([(px + math.cos(a) * ln * t + math.cos(a + math.pi / 2) * R * k * 0.2 * abs(math.sin(math.pi * min(1, t * 1.1))) ** 0.7 * s_,
                           py + (math.sin(a) * ln * t + math.sin(a + math.pi / 2) * R * k * 0.2 * abs(math.sin(math.pi * min(1, t * 1.1))) ** 0.7 * s_) * tilt - (1 - ring * 0.2) * 0)
                          for s_, ts in ((1, np.linspace(-0.25, 1, 9)), (-1, np.linspace(1, -0.25, 9))) for t in ts])
        m = shapes(W, H, polys)
        art = knockout(art, m, 0.5, 1.2)
        art = DG(art, np.clip(gaussian_filter(m, 1.4) * 1.5, 0, 1), "#5f7f74", seed=nx(), dry=0.1, rough=0.8)
        col = mix("#9fbfb0", "#c4d6c2", ring / 4)
        art = DG(art, m, col, mix(col, "#e0e8d6", 0.3), seed=nx(), u=np.hypot(xx - cx, (yy - cy) / tilt), v=np.arctan2(yy - cy, xx - cx) * 120, dry=0.3, rough=1.0)
        tips = circles(W, H, [(cx + math.cos((i + off) / n * math.tau) * (R * k * 0.45 + R * k * L * 1.2), cy + math.sin((i + off) / n * math.tau) * (R * k * 0.45 + R * k * L * 1.2) * tilt, R * k * 0.1) for i in range(n)])
        art = G(art, gaussian_filter(tips, 3) * m, tip, seed=nx(), density=0.7, edge=0.2, bloom=0.2, rough=1, feather=1.2)
    return art


def mesa(art, W, H, x0, x1, top, base, col, col2, nx, rng, strata=True):
    w = x1 - x0
    ridge = [(x0, base), (x0 + w * 0.12, top + (base - top) * 0.45), (x0 + w * 0.2, top + 6), (x0 + w * 0.5, top + rng.uniform(-4, 4)), (x1 - w * 0.22, top + 4), (x1 - w * 0.1, top + (base - top) * 0.5), (x1, base)]
    m = shapes(W, H, [ridge], smooth=False)
    m = displace(m, nx(), 3, 30)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = DG(art, m, col, col2, seed=nx(), u=xx, v=yy, dry=0.3, rough=2)
    if strata:
        bands = (0.5 + 0.5 * np.sin((yy - top) / (base - top) * math.pi * 5 + fbm(W, H, nx(), 60, 2) * 2)) ** 3
        art = OV(art, bands * m * np.clip((yy - top - 8) / 30, 0, 1), lambda mm: dry_gouache(mm, mix(col2, PLUM, 0.25), seed=nx() % 997, dry=0.5, density=0.3))
    # shadow on the right flank
    sh = shapes(W, H, [[(x1 - w * 0.22, top + 4), (x1, base), (x1 - w * 0.3, base)]], smooth=False) * m
    art = G(art, gaussian_filter(sh, 4), PLUM, seed=nx(), density=0.25, edge=0.1, bloom=0.3, rough=3, feather=3)
    return art


def dune(art, W, H, pts, base, col, col2, nx, shade=PLUM):
    poly = pts + [(pts[-1][0], base), (pts[0][0], base)]
    m = shapes(W, H, [poly])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    art = DG(art, m, col, col2, seed=nx(), u=xx, v=yy, dry=0.25, rough=1.5)
    crest = strokes(W, H, [(curve(pts, 60), 10, (0.2, 0.2))]) * m
    art = G(art, gaussian_filter(crest, 5), shade, seed=nx(), density=0.18, edge=0.1, bloom=0.3, rough=3, feather=3)
    return art


if "sky" in PARTS:
    W, H = 780, 860
    sky = painted_sky(W, H, [(0.0, "#e7b49e"), (0.35, "#f1a37e"), (0.62, "#f6bf8a"), (0.85, "#f7d3a4"), (1.0, SAND)], seed=5, streak=0.6)
    # sun glow behind the photo (centre at 390, 380)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - 390, yy - 380)
    g = np.clip(1 - (d - 220) / 200, 0, 1) ** 2
    sky[..., :3] = sky[..., :3] * (1 - g[..., None] * 0.35) + np.array(hex_rgb("#fbe0b0"), np.float32) * g[..., None] * 0.35
    rng = random.Random(5); nx = Seq(5000)
    clouds = strokes(W, H, [(curve([(x, y), (x + L * 0.5, y - 6), (x + L, y + 2)], 20), rng.uniform(10, 18), (0.3, 0.4)) for (x, y, L) in [(-20, 120, 300), (520, 90, 300), (40, 200, 180), (600, 220, 220), (-30, 560, 160), (640, 520, 170)]])
    sky = DG(sky, clouds, "#e09a8a", "#eaa996", seed=nx(), dry=0.6, rough=2, density=0.6)
    sky = add_grain(sky, 7, 0.03)
    save_rgb(sky, f"{OUT}/sky.webp", quality=74)
    clear()

if "land" in PARTS:
    W, H = 780, 600
    rng = random.Random(9); nx = Seq(9000)
    art = blank(W, H)
    art = mesa(art, W, H, -60, 330, 210, 420, "#d9967c", "#cf8a74", nx, rng)
    art = mesa(art, W, H, 430, 860, 180, 420, "#d38c74", "#c98270", nx, rng)
    art = mesa(art, W, H, 250, 560, 262, 420, "#c97760", "#bd6c58", nx, rng)
    art = dune(art, W, H, [(-20, 330), (160, 300), (380, 340), (600, 300), (800, 320)], 600, CORAL, "#e0794e", nx)
    art = dune(art, W, H, [(-20, 400), (220, 380), (470, 420), (800, 380)], 600, TERRA, "#b85a36", nx)
    art = dune(art, W, H, [(-20, 470), (260, 455), (520, 480), (800, 450)], 600, "#e7c39c", SAND, nx, shade=TERRA_D)
    # fade the bottom into the page sand
    yy = np.arange(H, dtype=np.float32)[:, None]
    f = np.clip((yy - 520) / 70, 0, 1)
    art[..., :3] = art[..., :3] * (1 - f[..., None]) + np.array(hex_rgb(SAND), np.float32) * f[..., None]
    art = saguaro(art, W, H, 92, 560, 470, 46, nx, rng, arms=((0.45, 1, 0.13, 0.22), (0.6, -1, 0.11, 0.2)))
    clear()
    art = saguaro(art, W, H, 650, 548, 230, 30, nx, rng, arms=((0.5, -1, 0.17, 0.2),), light=-1)
    clear()
    art = pear(art, W, H, [(700, 520, 46, 62, 15), (650, 470, 36, 50, -25), (735, 455, 34, 46, 30), (690, 405, 28, 38, -5)], nx, rng)
    clear()
    art = echeveria(art, W, H, 215, 560, 72, nx, rng)
    art = echeveria(art, W, H, 320, 580, 50, nx, rng, tip="#e08a7a")
    art = echeveria(art, W, H, 540, 582, 58, nx, rng)
    preview(art, "gk-land", tone=SAND)
    save_full(art, f"{OUT}/land.webp", size=(780, 600), quality=80)
    clear()

if "saguaro" in PARTS:
    W, H = 360, 700
    rng = random.Random(13); nx = Seq(13000)
    art = saguaro(blank(W, H), W, H, 180, 690, 640, 64, nx, rng, arms=((0.42, -1, 0.17, 0.25), (0.56, 1, 0.15, 0.22)))
    preview(art, "gk-saguaro", tone=SAND)
    save(art, f"{OUT}/saguaro.webp", max_w=150, quality=82)
    clear()

if "pear" in PARTS:
    W, H = 420, 420
    rng = random.Random(17); nx = Seq(17000)
    art = pear(blank(W, H), W, H, [(200, 330, 70, 92, 8), (130, 230, 54, 72, -32), (280, 220, 56, 74, 28), (210, 140, 44, 58, 4)], nx, rng)
    preview(art, "gk-pear", tone=SAND)
    save(art, f"{OUT}/pear.webp", max_w=180, quality=82)
    clear()

if "succulent" in PARTS:
    W, H = 320, 240
    rng = random.Random(19); nx = Seq(19000)
    art = echeveria(blank(W, H), W, H, 160, 125, 112, nx, rng)
    preview(art, "gk-succulent", tone=SAND)
    save(art, f"{OUT}/succulent.webp", max_w=130, quality=84)
    clear()

if "dunes" in PARTS:
    W, H = 1200, 260
    rng = random.Random(23); nx = Seq(23000)
    art = blank(W, H)
    art = dune(art, W, H, [(-20, 70), (300, 30), (640, 90), (940, 40), (1220, 80)], 260, PEACH, "#eda67a", nx)
    art = dune(art, W, H, [(-20, 130), (380, 100), (760, 150), (1220, 110)], 260, "#e7c39c", SAND, nx, shade=TERRA_D)
    yy = np.arange(H, dtype=np.float32)[:, None]
    f = np.clip((yy - 200) / 50, 0, 1)
    art[..., :3] = art[..., :3] * (1 - f[..., None]) + np.array(hex_rgb(SAND), np.float32) * f[..., None]
    preview(art, "gk-dunes", tone="#9c4a2c")
    save_full(art, f"{OUT}/dunes.webp", size=(860, 186), quality=80)
    clear()

if "divider" in PARTS:
    W, H = 600, 150
    rng = random.Random(29); nx = Seq(29000)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun = circles(W, H, [(300, 112, 40)]) * (yy < 112)
    art = DG(art, sun, CORAL, "#ec9a6a", seed=nx(), dry=0.35, rough=1)
    lines = strokes(W, H, [([(60, 112), (250, 112)], 5, (0.05, 0.3)), ([(350, 112), (540, 112)], 5, (0.3, 0.05)), ([(110, 128), (490, 128)], 3, (0.1, 0.1))])
    art = DG(art, lines, TERRA, seed=nx(), u=xx, v=yy, dry=0.45, rough=0.8)
    art = cactus_limb(art, W, H, curve([(300, 112), (300, 70), (301, 40)], 20), 16, nx, rng)
    art = cactus_limb(art, W, H, curve([(306, 88), (322, 86), (324, 60)], 16), 11, nx, rng)
    preview(art, "gk-divider", tone=SAND)
    save(art, f"{OUT}/divider.webp", max_w=240, quality=84)
    clear()

if "paper" in PARTS:
    save_tile(paper_tile(320, SAND, seed=31, fiber=0.5, mottle=0.9, specks=0.6, speck_col="#a8704a"), f"{OUT}/paper.webp", quality=80)
