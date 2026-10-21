"""Sakura Sumi — sumi-e ink cherry branches with light pink washed blossoms on fibrous washi, a vermilion hanko seal,
distant ink-wash mountains. Run: python3 -I sakura-sumi.py [part ...]
parts: washi branch sprig petal seal wash. Assets -> public/themes/art/sakura-sumi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a5_lib import *

OUT = outdir("sakura-sumi")
PARTS = sys.argv[1:] or ["washi", "branch", "sprig", "petal", "seal", "wash"]
WASHI = "#f4efe4"
INK, INK2 = "#1d1a18", "#3d3834"
PINK, PINK_D, PINK_DD = "#f4ccd3", "#eaa5b4", "#d4768d"
VERMILION = "#c43d26"


def petal_poly(cx, cy, L, Wd, ang, rng):
    loc = [(0, 0), (0.22, -0.34), (0.58, -0.52), (0.9, -0.4), (1.0, -0.14), (0.86, -0.01), (1.0, 0.13), (0.9, 0.4), (0.58, 0.52), (0.22, 0.34)]
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for u, v in loc:
        u *= L * rng.uniform(0.96, 1.04); v *= Wd * 2 * rng.uniform(0.94, 1.06)
        out.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return out


def blossom(art, W, H, x, y, r, rng, nx, rot=None, open_=1.0, side=1.0):
    """Five notched petals in a pale pink wash with a deeper heart, inked stamens and anther dots."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    polys = []
    for k in range(5):
        a = rot + k * math.tau / 5 + rng.uniform(-0.12, 0.12)
        L = r * rng.uniform(0.9, 1.05) * (0.75 + 0.25 * side if k in (1, 2) else 1.0)
        polys.append(petal_poly(x + math.cos(a) * r * 0.08, y + math.sin(a) * r * 0.08, L * open_, r * 0.42, a, rng))
    m = shapes(W, H, polys)
    art = G(art, m, PINK, mix(PINK, "#fbe9ec", 0.4), seed=nx(), density=0.62, edge=0.75, bloom=0.5, gran=0.15, rough=2.2, feather=0.9, pad=12)
    heart = circles(W, H, [(x, y, r * 0.42)]) * m
    art = G(art, gaussian_filter(heart, r * 0.12), PINK_D, PINK_DD, seed=nx(), density=0.6, edge=0.2, bloom=0.2, rough=1.5, feather=1.2, pad=12)
    st = []
    dots_ = []
    for k in range(11):
        a = rng.uniform(0, math.tau); L = r * rng.uniform(0.32, 0.55)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        st.append(([(x, y), ((x + ex) / 2 + rng.gauss(0, 1), (y + ey) / 2 + rng.gauss(0, 1)), (ex, ey)], max(0.9, r * 0.025), (0.0, 0.5)))
        dots_.append((ex, ey, max(1.2, r * rng.uniform(0.04, 0.06))))
    art = G(art, strokes(W, H, st), "#8f4a58", seed=nx(), density=0.55, edge=0.1, bloom=0, rough=0.6, feather=0.4, pad=8)
    art = G(art, circles(W, H, dots_), INK, INK2, seed=nx(), density=0.85, edge=0.3, bloom=0, rough=0.6, feather=0.4, pad=8)
    return art


def bud(art, W, H, x, y, s, ang, rng, nx):
    m = shapes(W, H, [deform(petal_pts(x, y, s * 1.5, s * 0.55, ang, n=12), rng, 1, 0.05)])
    art = G(art, m, PINK_D, PINK_DD, seed=nx(), density=0.7, edge=0.6, bloom=0.2, rough=1.4, feather=0.8, pad=8)
    cal = strokes(W, H, [([(x - math.cos(ang) * s * 0.2, y - math.sin(ang) * s * 0.2), (x + math.cos(ang) * s * 0.4, y + math.sin(ang) * s * 0.4)], s * 0.5, (0.0, 0.6))])
    return ink(art, cal, nx(), density=0.8, bleed=0, dry=0.1, pad=8)


def branch_items(pts, w0, w1):
    """Tapered brush stroke as many short segments (width from w0 to w1)."""
    items = []
    n = len(pts)
    for i in range(n - 1):
        t = i / (n - 1)
        items.append(([pts[i], pts[i + 1]], w0 + (w1 - w0) * t ** 0.8, None))
    return items


if "washi" in PARTS:
    n = 480
    rng = random.Random(41)
    base = rgb_arr(n, n, WASHI)
    cloud = wrap_noise(n, n, 5, 26) - 0.5
    fine = wrap_noise(n, n, 6, 0.8) - 0.5
    base *= (1 + cloud * 0.035 + fine * 0.03)[..., None]
    cv = Canvas(n, n)
    for _ in range(170):
        x, y = rng.uniform(0, n), rng.uniform(0, n)
        a = rng.uniform(0, math.tau); L = rng.uniform(30, 120)
        pts = curve([(x, y), (x + math.cos(a) * L * 0.5 + rng.gauss(0, 10), y + math.sin(a) * L * 0.5 + rng.gauss(0, 10)), (x + math.cos(a + rng.gauss(0, .5)) * L, y + math.sin(a + rng.gauss(0, .5)) * L)], 20)
        wdt = rng.uniform(0.5, 1.3)
        for dx in (-n, 0, n):
            for dy in (-n, 0, n):
                p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=wdt, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
                path = skia.Path(); path.moveTo(pts[0][0] + dx, pts[0][1] + dy)
                for px, py in pts[1:]:
                    path.lineTo(px + dx, py + dy)
                cv.c.drawPath(path, p)
    fib = cv.array()[..., 3]
    light = fib * (wrap_noise(n, n, 7, 4) > 0.45)
    dark = fib * (wrap_noise(n, n, 7, 4) <= 0.45)
    base = base * (1 - dark[..., None] * 0.07) + light[..., None] * 0.05
    art = np.concatenate([np.clip(base, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/washi.webp", quality=74)
    clear()

if "branch" in PARTS:
    W, H = 960, 760
    rng = random.Random(42); nx = Seq(40100)
    art = blank(W, H)
    main = curve([(W + 10, 40), (820, 92), (690, 168), (560, 232), (430, 262), (300, 300), (190, 372), (110, 430)], 90)
    twigs = [
        (curve([(690, 168), (660, 110), (600, 70), (540, 52)], 30), 9, 1.4),
        (curve([(560, 232), (520, 300), (500, 360), (520, 420)], 30), 8, 1.4),
        (curve([(430, 262), (380, 210), (320, 186), (250, 180)], 30), 7, 1.2),
        (curve([(300, 300), (262, 352), (250, 410)], 22), 6, 1.2),
        (curve([(820, 92), (800, 150), (812, 210), (850, 260)], 26), 8, 1.2),
        (curve([(190, 372), (140, 350), (90, 352)], 18), 5, 1.0),
        (curve([(600, 70), (590, 30)], 10), 3, 0.8),
        (curve([(500, 360), (460, 380)], 10), 3, 0.8),
    ]
    def wobbly(pts, w0, w1, seed):
        r_ = random.Random(seed); out = []; n = len(pts)
        for i in range(n - 1):
            t = i / (n - 1)
            knot = 1 + 0.22 * math.sin(t * 23 + seed) * math.sin(t * 7)
            out.append(([pts[i], pts[i + 1]], (w0 + (w1 - w0) * t ** 0.8) * knot, None))
        return out
    items = wobbly(main, 28, 3, 1)
    for k, (pts, w0, w1) in enumerate(twigs):
        items += wobbly(pts, w0, w1, k + 2)
    bm = strokes(W, H, items)
    # one loaded brush: grey body, dark ink pooled along the upper edge and the joints, dry-brush streaks (hihaku)
    st = gaussian_filter(np.random.default_rng(7).random((H, W)).astype(np.float32), (0.7, 9))
    st = (st - st.min()) / (st.max() - st.min() + 1e-6)
    dry = np.clip((st - 0.55) * 5, 0, 1)
    body = bm * (1 - dry * 0.85)
    art = ink(art, body, nx(), col="#4f4a45", col2="#6a645e", density=0.85, bleed=0.16, dry=0.2, rough=2.0)
    upper = np.clip(bm - np.roll(bm, 5, 0), 0, 1) * bm
    dark = np.clip(upper * 1.4 + gaussian_filter(bm, 1) * (fbm(W, H, 77, 60, 3) > 0.6) * 0.8, 0, 1) * (1 - dry * 0.6)
    art = ink(art, dark, nx(), density=0.95, bleed=0, dry=0.3, rough=1.4)
    tenten = []
    for (x, y, a) in along(main[:70], 70):
        for j in range(rng.randint(1, 2)):
            tenten.append((x + rng.gauss(0, 7), y + rng.gauss(0, 5) - 14, rng.uniform(2.2, 3.6)))
    art = ink(art, circles(W, H, tenten), nx(), density=0.95, bleed=0.12, dry=0.0, rough=1.5)
    # blossoms painted on their own sheet, then laid over the branch with the ink knocked out underneath
    fl = blank(W, H)
    spots = [(540, 52, 40), (600, 88, 34), (520, 420, 38), (480, 370, 30), (250, 180, 36), (320, 196, 30), (250, 410, 34), (850, 260, 38),
             (812, 200, 30), (90, 352, 30), (110, 430, 34), (640, 200, 28), (380, 250, 26), (720, 150, 26)]
    for (x, y, r) in spots:
        fl = blossom(fl, W, H, x + rng.gauss(0, 4), y + rng.gauss(0, 4), r * 1.15, rng, nx, side=rng.uniform(0.5, 1))
    for (x, y, s_, a) in [(590, 30, 10, -1.6), (460, 380, 10, 2.6), (150, 340, 9, 3.4), (700, 130, 9, -2.2), (870, 290, 10, 1.0), (290, 160, 9, -2.6)]:
        fl = bud(fl, W, H, x, y, s_, a, rng, nx)
    art = knockout(art, np.clip(fl[..., 3] * 1.6, 0, 1), amount=0.88, grow=0.8)
    art = glaze(art, fl)
    preview(art, "ss-branch", tone=WASHI)
    save(art, f"{OUT}/branch.webp", max_w=760, quality=80)
    clear()

if "sprig" in PARTS:
    W, H = 520, 220
    rng = random.Random(43); nx = Seq(40200)
    art = blank(W, H)
    stem = curve([(20, 150), (140, 128), (270, 120), (400, 96), (500, 70)], 40)
    items = branch_items(stem, 9, 2)
    items += branch_items(curve([(270, 120), (300, 168), (340, 190)], 14), 4, 1)
    art = ink(art, strokes(W, H, items), nx(), density=0.9, bleed=0.15, dry=0.4)
    for (x, y, r) in [(200, 118, 30), (340, 186, 26), (420, 86, 28)]:
        art = blossom(art, W, H, x, y, r, rng, nx)
    art = bud(art, W, H, 498, 66, 9, -0.5, rng, nx)
    art = bud(art, W, H, 110, 124, 8, -2.4, rng, nx)
    preview(art, "ss-sprig", tone=WASHI)
    save(art, f"{OUT}/sprig.webp", max_w=300, quality=82)
    clear()

if "petal" in PARTS:
    W, H = 90, 90
    rng = random.Random(44); nx = Seq(40300)
    m = shapes(W, H, [petal_poly(18, 50, 56, 18, -0.5, rng)])
    art = G(blank(W, H), m, PINK, PINK_D, seed=nx(), density=0.7, edge=0.8, bloom=0.4, rough=1.5, feather=0.8)
    save(art, f"{OUT}/petal.webp", max_w=44, quality=84)

if "seal" in PARTS:
    W, H = 260, 260
    nx = Seq(40400); rng = random.Random(45)
    outer = shapes(W, H, [deform([(22, 24), (238, 20), (240, 236), (20, 240)], rng, 2, 0.01)], smooth=False)
    outer = np.clip(gaussian_filter(outer, 2.2) * 1.3, 0, 1)
    gap = np.clip(shapes(W, H, [[(36, 38), (224, 36), (226, 222), (36, 224)]], smooth=False) - shapes(W, H, [[(44, 46), (216, 44), (218, 214), (44, 216)]], smooth=False), 0, 1)
    m = np.clip(outer - gap, 0, 1)
    art = LC(blank(W, H), m, VERMILION, seed=nx(), wear=0.28, rough=1.6)
    art = G(art, m * 0.5, "#9e2a1a", seed=nx(), density=0.3, edge=0.4, bloom=0.3, rough=2)
    preview(art, "ss-seal", tone=WASHI)
    save(art, f"{OUT}/seal.webp", max_w=160, quality=84)

if "wash" in PARTS:
    W, H = 900, 340
    nx = Seq(40500); rng = random.Random(46)
    art = blank(W, H)
    for k, (yb, amp, col, dens) in enumerate([(150, 60, "#b7b0a8", 0.35), (200, 70, "#8d867f", 0.42), (250, 50, "#5d5752", 0.5)]):
        pts = [(0, H)]
        xs = np.linspace(0, W, 26)
        ph = rng.uniform(0, 6)
        for x in xs:
            y = yb - amp * (0.5 + 0.5 * math.sin(x / W * math.pi * (1.6 + k * 0.7) + ph)) * (0.6 + 0.4 * math.sin(x / 70 + k)) + rng.gauss(0, 6)
            pts.append((x, y))
        pts.append((W, H))
        m = shape_mask(W, H, pts, smooth=False)
        yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
        fade = np.clip(1 - (yy - (yb - amp)) / (amp * 2.2 + 40), 0, 1)  # mist swallows the foot
        art = G(art, m * fade, col, seed=nx(), density=dens, edge=0.55, bloom=0.5, gran=0.25, rough=7, feather=2.5, pad=30)
    preview(art, "ss-wash", tone=WASHI)
    save(art, f"{OUT}/wash.webp", max_w=640, quality=78)
