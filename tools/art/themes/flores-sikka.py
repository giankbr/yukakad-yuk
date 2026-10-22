"""Flores Sikka — tenun ikat Sikka (Maumere) at thread level: dark indigo-brown warp ikat with fine cream/rust/ochre
motifs and plain warp stripes; Kelimutu tri-colour crater lakes and the Flores hills in watercolour; woven star medallion
and a woven band. Run: python3 -I flores-sikka.py [part ...]   parts: ikat pita bintang kelimutu bukit"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _d1_lib import *
from _jw_lib import hills as jw_hills

OUT = outdir("flores-sikka")
PARTS = sys.argv[1:] or ["ikat", "pita", "bintang", "kelimutu", "bukit"]
PAL = ["#2b2130", "#e3d3b0", "#a24a27", "#c58b3a", "#3d4a70", "#4a2a22"]
GND, CRM, RUST, OCH, BLU, BRN = range(6)


def star8(c, p, cx, cy, r, inner=0.45):
    pts = []
    for i in range(16):
        a = i * math.pi / 8 - math.pi / 2
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    c.drawPath(path_of(pts), p)


def design(N=144):
    lay = lambda f: wrap_draw(N, N, f)
    L = []
    def stripes(spec):
        for (x0, x1, col) in spec:
            L.append((lay(lambda c, p, x0=x0, x1=x1: c.drawRect(skia.Rect(x0, -N, x1, 2 * N), p)), col))
    stripes([(0, 2, RUST), (2, 3, OCH), (4, 6, RUST), (64, 66, BLU), (66, 68, RUST), (68, 69, OCH), (70, 72, BLU), (138, 140, RUST), (140, 141, OCH), (142, 144, BRN)])
    # column A: chain of stepped diamonds, each holding an 8-point star
    cx = 35
    ys = [0, 36, 72, 108, 144]
    def stepd(c, p, r, w):
        sp = stroke_paint(w)
        for y in ys:
            pts = []
            st = r / 4
            for i in range(4):
                pts += [(cx + i * st, y - r + i * st), (cx + (i + 1) * st, y - r + i * st)]
            pts += [(cx + r, y)]
            for i in range(4):
                pts += [(cx + r - i * st, y + i * st), (cx + r - i * st, y + (i + 1) * st)]
            pts += [(cx, y + r)]
            for i in range(4):
                pts += [(cx - i * st, y + r - i * st), (cx - (i + 1) * st, y + r - i * st)]
            pts += [(cx - r, y)]
            for i in range(4):
                pts += [(cx - r + i * st, y - i * st), (cx - r + i * st, y - (i + 1) * st)]
            c.drawPath(path_of(pts), sp)
    L.append((lay(lambda c, p: stepd(c, p, 24, 2.2)), CRM))
    L.append((lay(lambda c, p: stepd(c, p, 19, 1.4)), RUST))
    L.append((lay(lambda c, p: [star8(c, p, cx, y, 11, 0.42) for y in ys]), CRM))
    L.append((lay(lambda c, p: [c.drawCircle(cx, y, 2.6, p) for y in ys]), RUST))
    L.append((lay(lambda c, p: [c.drawCircle(x, y + 18, 1.2, p) for y in ys for x in (cx - 26, cx + 26, cx - 20, cx + 20)]), OCH))
    # hooks (kait) linking the diamonds
    def kait(c, p):
        sp = stroke_paint(1.6)
        for y in ys:
            for sx in (-1, 1):
                pts = [(cx + sx * 4, y + 18), (cx + sx * 10, y + 18), (cx + sx * 10, y + 13), (cx + sx * 7, y + 13)]
                c.drawPath(path_of(pts, closed=False), sp)
    L.append((lay(kait), OCH))
    # column B: alternating small stars and paired crosses in fine cream / ochre, rows of dots
    bx = 104
    def smallstars(c, p):
        for k, y in enumerate(range(0, N, 24)):
            if k % 2 == 0:
                star8(c, p, bx, y, 9, 0.4)
            else:
                for sx in (-1, 1):
                    x = bx + sx * 14
                    c.drawRect(skia.Rect(x - 1.2, y - 6, x + 1.2, y + 6), p)
                    c.drawRect(skia.Rect(x - 6, y - 1.2, x + 6, y + 1.2), p)
    L.append((lay(smallstars), CRM))
    L.append((lay(lambda c, p: [c.drawCircle(bx, y, 2.0, p) for y in range(0, N, 48)]), RUST))
    L.append((lay(lambda c, p: [c.drawCircle(x, y, 0.9, p) for y in range(6, N, 6) for x in (bx - 28, bx + 28)]), OCH))
    L.append((lay(lambda c, p: [c.drawRect(skia.Rect(bx - 30, y, bx + 30, y + 1), p) for y in range(12, N, 48)]), RUST))
    return layer_index(GND, L)


def loom(D, p=3, seed=7, tile=True):
    return ikat(D, PAL, p=p, mode="warp", ground="#1d1622", face=0.8, amp=1.4, coh=1.4, along=8, seed=seed, bleed=0.6,
                slub=0.2, fibre=0.07, thread_var=0.05, tile=tile)


if "ikat" in PARTS:
    D = design(144)
    cloth = loom(D, 3, 7)
    prev_rgb(tile_to(cloth, 864, 600), "ikat-rep")
    save_rgb_arr(cloth, f"{OUT}/ikat.webp", quality=80)
    clear()

if "pita" in PARTS:
    D = design(144)
    cloth = loom(D, 3, 17)
    band = np.rot90(cloth[:, 0:70 * 3]).copy()
    prev_rgb(np.concatenate([band, band], 1), "pita")
    save_rgb_arr(band, f"{OUT}/pita.webp", quality=80)
    clear()

if "bintang" in PARTS:
    N = 64
    c0 = N / 2
    pd = lambda f: plain_draw(N, N, f)
    lays = [(pd(lambda c, p: c.drawPath(path_of([(c0, 1), (N - 1, c0), (c0, N - 1), (1, c0)]), p)), GND),
            (pd(lambda c, p: c.drawPath(path_of([(c0, 5), (N - 5, c0), (c0, N - 5), (5, c0)]), stroke_paint(2.2))), CRM),
            (pd(lambda c, p: c.drawPath(path_of([(c0, 10), (N - 10, c0), (c0, N - 10), (10, c0)]), stroke_paint(1.4))), RUST),
            (pd(lambda c, p: star8(c, p, c0, c0, 15, 0.44)), CRM),
            (pd(lambda c, p: star8(c, p, c0, c0, 7, 0.5)), OCH),
            (pd(lambda c, p: c.drawCircle(c0, c0, 2.2, p)), RUST)]
    D = layer_index(9, lays)
    A = (D != 9).astype(np.int32); D[D == 9] = GND
    med = woven_cut(D, A, PAL, 5, 51, mode="warp", ground="#1d1622", face=0.8, amp=1.0, coh=1.4, along=8, slub=0.2, fibre=0.07)
    preview(med, "bintang")
    save(med, f"{OUT}/bintang.webp", max_w=180, quality=82)
    clear()


def lake(cx, cy, rx, ry, rng, rot=0.0):
    return deform(ellipse_pts(cx, cy, rx, ry, 16, rot), rng, 2, 0.08)


if "kelimutu" in PARTS:
    W, H = 900, 600
    nx = Seq(40100); rng = random.Random(12)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    # morning sky wash
    sky = poly(W, H, [(0, 0), (W, 0), (W, 260), (0, 260)], smooth=False) * np.clip((280 - yy) / 120, 0, 1)
    art = G(art, sky, "#f2dcc0", "#cfe0dc", seed=nx(), density=0.45, edge=0.0, bloom=0.5, rough=10, feather=10)
    # far blue ridges of Flores
    art = G(art, jw_hills(W, H, 170, 30, 21, 0.7) * np.clip((330 - yy) / 120, 0, 1), "#8fa2b4", "#a7b2bf", seed=nx(), density=0.55, edge=0.4, bloom=0.4, rough=6)
    art = G(art, jw_hills(W, H, 205, 26, 23, 0.45) * np.clip((360 - yy) / 120, 0, 1), "#6f8798", "#7f8c8a", seed=nx(), density=0.6, edge=0.4, bloom=0.35, rough=5)
    # volcanic massif: ochre-brown crater walls
    mass = poly(W, H, [(-20, 600), (-20, 300), (120, 258), (300, 236), (460, 250), (640, 232), (800, 250), (920, 280), (920, 600)])
    art = G(art, mass, "#9b7a55", "#b49468", seed=nx(), density=0.75, edge=0.4, bloom=0.4, rough=6, gran=0.45)
    tex = fbm(W, H, 77, 18, 3)
    art = G(art, mass * np.clip((tex - 0.55) * 3, 0, 1), "#7d6046", seed=nx(), density=0.35, edge=0.2, bloom=0.3, rough=3, gran=0.5)
    # scrub and grass on the outer slopes
    scrub = blobs(W, H, [(rng.uniform(0, W), rng.uniform(440, 600), rng.uniform(0.4, 0.8)) for _ in range(60)] + [(rng.uniform(0, W), rng.uniform(262, 300), rng.uniform(0.3, 0.5)) for _ in range(26)], rng, (8, 16), 3)
    art = G(art, scrub * mass, "#5f7a45", "#82904f", seed=nx(), density=0.65, edge=0.45, bloom=0.4, rough=3)
    # crater bowls: shadowed far wall with cliff streaks, sunlit near slope, lake sitting low inside
    bowls = [(300, 398, 168, 64, -0.04, "#25b0a3", "#5ccbbb", "#147a76"), (602, 388, 130, 52, 0.05, "#2f8f5c", "#58aa6e", "#1d5a3a"), (772, 304, 78, 24, 0.0, "#2b2626", "#3e3430", "#120f0f")]
    for (cx, cy, rx, ry, rot, a, b2, d) in bowls:
        bm = poly(W, H, lake(cx, cy - 14, rx + 30, ry + 34, rng, rot))
        far = bm * np.clip((cy + 4 - yy) / (ry * 0.9), 0, 1)
        art = G(art, bm, "#8a6847", "#9c7a54", seed=nx(), density=0.55, edge=0.55, bloom=0.3, rough=3, gran=0.5)
        art = G(art, far, "#5a4030", "#6a4a34", seed=nx(), density=0.6, edge=0.2, bloom=0.3, rough=3, gran=0.5)
        cl = strokes(W, H, [([(x, cy - ry - 40 + rng.uniform(0, 20)), (x + rng.uniform(-4, 4), cy - rng.uniform(0, ry * 0.6))], rng.uniform(1.4, 3), (0.2, 0.4)) for x in np.linspace(cx - rx, cx + rx, int(rx / 7))])
        art = G(art, cl * far, "#3c2b22", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=1.5, gran=0.4)
        m = poly(W, H, lake(cx, cy, rx, ry, rng, rot))
        art = G(art, m, a, b2, seed=nx(), density=0.92, edge=0.65, bloom=0.45, rough=3, gran=0.2)
        art = G(art, m * np.clip((cy + ry * 0.2 - yy) / (ry * 0.8), 0, 1), d, seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=3)
        milky = m * np.clip((fbm(W, H, cx, 30, 3) - 0.5) * 3, 0, 1) * np.clip((yy - cy + ry * 0.2) / ry, 0, 1)
        art = G(art, milky, "#d9efe6", seed=nx(), density=0.35, edge=0.0, bloom=0.5, rough=4)
        shore = np.clip(gaussian_filter(m, 2.5) * 2.2, 0, 1) - m
        art = G(art, np.clip(shore, 0, 1) * (yy > cy - ry * 0.2), "#e9dcc0", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # the ridge between the twin lakes
    ridge = strokes(W, H, [(curve([(462, 300), (474, 370), (460, 440)], 16), 22, (0.2, 0.3))])
    art = G(art, ridge, "#8a6a48", seed=nx(), density=0.6, edge=0.3, bloom=0.2, rough=3)
    # drifting morning mist
    for (y, x0, x1) in [(300, 0, 520), (460, 380, 900), (340, 600, 900)]:
        mist = poly(W, H, deform([(x0, y - 10), (x1, y - 24), (x1, y + 12), (x0, y + 22)], rng, 2, 0.15))
        art = over(art, rgba(np.ones((H, W, 3), np.float32) * C("#f7f3ea"), gaussian_filter(mist, 9) * 0.75 * fbm(W, H, y, 50, 3)))
    art[..., 3] *= vignette_mask(W, H, 17, inset=6, rough=26, fade=34)
    art[..., 3] *= np.clip((yy - 40 + (fbm(W, H, 5, 50, 3) - 0.5) * 60) / 110, 0, 1)
    preview(art, "kelimutu", tone="#f5eee0")
    save(art, f"{OUT}/kelimutu.webp", max_w=740, quality=74)
    clear()

if "bukit" in PARTS:
    W, H = 900, 300
    nx = Seq(45100); rng = random.Random(14)
    art = blank(W, H)
    yy, xx = ygrid(W, H)
    layers = [(110, 34, 31, "#9aaec0", "#b1bcc4", 0.5), (150, 30, 33, "#7f9a86", "#8fa58a", 0.6), (190, 26, 35, "#5f8158", "#71905a", 0.7), (232, 20, 37, "#4b6a3f", "#5a7a44", 0.8)]
    for (y, amp, sd, a, b, d) in layers:
        art = G(art, jw_hills(W, H, y, amp, sd, 0.6), a, b, seed=nx(), density=d, edge=0.45, bloom=0.35, rough=5, gran=0.3)
    # lontar palms and a small whitewashed chapel among the hills
    palms = []
    for (x, y, h) in [(120, 220, 70), (160, 230, 54), (700, 210, 76), (760, 226, 58), (820, 236, 44)]:
        palms.append(([(x, y), (x + 3, y - h)], 3.2, None))
        for k in range(9):
            a = -math.pi / 2 + (k - 4) * 0.34
            palms.append((curve([(x + 3, y - h), (x + 3 + math.cos(a) * 16, y - h + math.sin(a) * 16 - 2), (x + 3 + math.cos(a) * 24, y - h + math.sin(a) * 24 + 6)], 8), 2.6, (0.0, 0.6)))
    art = G(art, strokes(W, H, palms), "#3c5233", "#4c6438", seed=nx(), density=0.85, edge=0.2, bloom=0.1, rough=1)
    ch = poly(W, H, [(470, 178), (470, 160), (482, 150), (494, 160), (494, 178)], smooth=False)
    art = GP(art, ch, "#f3eee2", "#e2dccb", seed=nx(), rough=0.6)
    art = GP(art, poly(W, H, [(468, 161), (482, 148), (496, 161), (494, 163), (482, 152), (470, 163)], smooth=False), "#a24a27", seed=nx(), rough=0.4)
    art = GP(art, poly(W, H, [(479, 178), (479, 168), (485, 168), (485, 178)], smooth=False), "#4a3a32", seed=nx(), rough=0.3)
    art[..., 3] *= np.clip((yy - 60) / 60, 0, 1) * np.clip(np.minimum(xx, W - 1 - xx) / 30, 0, 1)
    preview(art, "bukit", tone="#f5eee0")
    save(art, f"{OUT}/bukit.webp", max_w=820, quality=80)
    clear()
