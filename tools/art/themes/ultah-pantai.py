"""Ultah Pantai — a kids' beach-party birthday in sunny gouache with a warm brown crayon contour (original designs):
a sandcastle with bucket turrets and shells, a pennant flag (the age goes on it), a striped beach umbrella, a beach
ball, a happy crab, a bucket and spade, the sea with a foam edge, and a shell & starfish divider.
Run: python3 -I ultah-pantai.py [part ...]  parts: castle flag umbrella ball crab bucket waves shells
Assets -> public/themes/art/ultah-pantai/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _t3_lib import *

OUT = outdir("ultah-pantai")
PARTS = sys.argv[1:] or ["castle", "flag", "umbrella", "ball", "crab", "bucket", "waves", "shells"]
LINE = "#8a4a2a"
SAND, SAND2, SAND_D = "#f0c983", "#f7dca4", "#c08a48"
CORAL, CORAL2 = "#ff6f5e", "#ff9580"
SUN, SUN2 = "#ffc93c", "#ffe07a"
SEA, SEA2 = "#29b0c2", "#5fd3d6"
CREAM = "#fff4dc"


def tn(art, m, col, col2, nx, k=10, sh=None, line_a=0.7, shade=(-1, -1), hi=True):
    return toon(art, m, col, col2, nx, shade=shade, k=k, sh_col=sh, hi=hi, line=LINE, line_w=2.4, line_a=line_a)


def speckle(art, m, nx, col="#b07a3a", n=0.004, r=1.4):
    h, w = m.shape
    rng = np.random.default_rng(nx())
    sp = (rng.random((h, w)) < n).astype(np.float32)
    sp = np.clip(gaussian_filter(sp, r) * 8, 0, 1) * m
    return G(art, sp, col, seed=nx(), density=0.55, edge=0, bloom=0, rough=0.3, feather=0.3)


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def tower(cx, top, bot, w, merlons=3):
    """Bucket-moulded tower: slightly tapering with a crenellated top."""
    pts = [(cx - w * 0.56, bot), (cx - w * 0.5, top)]
    mw = w / (merlons * 2 - 1)
    x = cx - w * 0.5
    for i in range(merlons * 2 - 1):
        y = top - 16 if i % 2 == 0 else top
        pts += [(x, y), (x + mw, y)]
        x += mw
    pts += [(cx + w * 0.5, top), (cx + w * 0.56, bot)]
    return pts


if "castle" in PARTS:
    W, H = 600, 520
    nx = Seq(100); rng = random.Random(1)
    art = blank(W, H)
    mound = shapes(W, H, [[(10, 510), (60, 440), (200, 420), (420, 420), (560, 440), (595, 510)]])
    towers = [(130, 250, 440, 100, 3), (470, 270, 440, 96, 3), (300, 150, 430, 130, 4)]
    wall = shapes(W, H, [tower(300, 300, 440, 330, 7)], smooth=False)
    art = tn(art, mound, SAND, SAND2, nx, k=12, sh=SAND_D)
    art = tn(art, wall, SAND, SAND2, nx, k=12, sh=SAND_D)
    for cx, top, bot, w, mer in towers:
        tm = shapes(W, H, [tower(cx, top, bot, w, mer)], smooth=False)
        art = tn(art, tm, SAND, SAND2, nx, k=16, sh=SAND_D)
        ridges = strokes(W, H, [([(cx - w * 0.5 + 4, y), (cx + w * 0.5 - 4, y + 2)], 2.4, None) for y in range(top + 30, bot - 10, 34)]) * tm
        art = G(art, ridges, SAND_D, seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6)
        win = shapes(W, H, [[(cx - 10, top + 70), (cx - 10, top + 52)] + arc_pts(cx, top + 52, 10, math.pi, 2 * math.pi, 10) + [(cx + 10, top + 52), (cx + 10, top + 70)]], smooth=False)
        art = tn(art, win, "#6a3c1e", "#8a5530", nx, k=3, hi=False)
    door = shapes(W, H, [[(270, 440), (270, 380)] + arc_pts(300, 380, 30, math.pi, 2 * math.pi, 14) + [(330, 380), (330, 440)]], smooth=False)
    art = tn(art, door, "#6a3c1e", "#8a5530", nx, k=4, hi=False)
    art = speckle(art, np.clip(mound + wall, 0, 1), nx, n=0.006)
    # shells & a starfish pressed into the sand
    for x, y, c in [(200, 360, CORAL), (400, 350, "#ffb3a6"), (90, 470, CREAM), (520, 480, "#ffd0a0"), (300, 470, CORAL)]:
        sh = shapes(W, H, [[(x - 12, y + 6)] + arc_pts(x, y + 6, 12, math.pi, 2 * math.pi, 10) + [(x + 12, y + 6)]])
        art = tn(art, sh, c, mix(c, "#ffffff", 0.3), nx, k=3, line_a=0.5)
        art = G(art, strokes(W, H, [([(x, y + 6), (x + math.cos(a) * 11, y + 6 + math.sin(a) * 11)], 1.2, None) for a in np.linspace(math.pi * 1.15, math.pi * 1.85, 4)]) * sh, LINE, seed=nx(), density=0.5, edge=0, bloom=0)
    st = []
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5
        st.append(petal_pts(440 + math.cos(a) * 3, 470 + math.sin(a) * 3, 24, 7, a, n=8))
    stm = shapes(W, H, st)
    art = tn(art, stm, SUN, SUN2, nx, k=4, line_a=0.6)
    # flag pole on the keep (the flag itself is a separate waving piece)
    pole = strokes(W, H, [([(300, 136), (300, 30)], 4.5, None)])
    art = tn(art, pole, "#a0683a", "#c08a50", nx, k=2, hi=False, line_a=0.5)
    preview(art, "up-castle", tone="#f7e3b8")
    save(art, f"{OUT}/castle.webp", max_w=440, quality=82)
    clear()

if "flag" in PARTS:
    W, H = 260, 170
    nx = Seq(200)
    art = blank(W, H)
    fl = shapes(W, H, [[(10, 14), (120, 28), (240, 70), (120, 112), (10, 128)]])
    art = tn(art, fl, CORAL, CORAL2, nx, k=8)
    stripe = shapes(W, H, [[(10, 100), (130, 92), (200, 82), (130, 108), (10, 118)]]) * fl
    art = GP(art, stripe, CREAM, seed=nx(), rough=0.6)
    preview(art, "up-flag", tone="#bfe8f2")
    save(art, f"{OUT}/flag.webp", max_w=200, quality=84)
    clear()

if "umbrella" in PARTS:
    W, H = 440, 520
    nx = Seq(300)
    art = blank(W, H)
    cx, cy, rx, ry = 220, 190, 200, 150
    pole = strokes(W, H, [([(cx, 120), (cx + 34, 510)], 9, None)])
    art = tn(art, pole, CREAM, "#ffffff", nx, k=3, line_a=0.6)
    bands = strokes(W, H, [([(cx + 34 * t, 120 + 390 * t), (cx + 34 * (t + 0.04), 120 + 390 * (t + 0.04))], 10, None) for t in np.arange(0.1, 0.95, 0.12)]) * pole
    art = GP(art, bands, CORAL, seed=nx(), rough=0.5)
    # canopy: dome with a scalloped hem, split into 6 gores
    top = arc_pts(cx, cy, rx, math.pi, 2 * math.pi, 40, ry / rx)
    hem = []
    n = 6
    for i in range(n):
        x0 = cx + rx - (i) * 2 * rx / n; x1 = cx + rx - (i + 1) * 2 * rx / n
        hem += arc_pts((x0 + x1) / 2, cy, (x0 - x1) / 2, 0, math.pi, 10, 0.4)
    can = shapes(W, H, [top + hem])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2((yy - (cy + 60)), (xx - cx))
    sector = ((ang + math.pi) / math.pi * n).astype(np.int32)
    for i, (c1, c2) in enumerate([(CORAL, CORAL2), (CREAM, "#ffffff"), (SUN, SUN2), (CREAM, "#ffffff"), (CORAL, CORAL2), (CREAM, "#ffffff")]):
        m = can * (sector == i)
        art = GP(art, m, c1, c2, seed=nx(), rough=0.8, streak=0.6)
    art = G(art, inner_shade(can, 22, 16, 18), "#c0503a", seed=nx(), density=0.35, edge=0.2, bloom=0.2, rough=2)
    seams = strokes(W, H, [([(cx, cy - ry + 4), (cx + math.cos(a) * rx * 0.98, cy + 4)], 1.8, None) for a in []])
    gl = []
    for i in range(1, n):
        a = math.pi + i * math.pi / n
        gl.append(([(cx, cy - ry + 6), (cx + math.cos(a) * rx * 0.97, cy + math.sin(a) * 0 + 6)], 1.8, None))
    art = G(art, strokes(W, H, gl) * can, LINE, seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    art = G(art, contour(can, 2.4, nx()), LINE, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.6, feather=0.35)
    knob = circles(W, H, [(cx, cy - ry - 4, 11)])
    art = tn(art, knob, SUN, SUN2, nx, k=3)
    preview(art, "up-umbrella", tone="#f7e3b8")
    save(art, f"{OUT}/umbrella.webp", max_w=300, quality=82)
    clear()

if "ball" in PARTS:
    W, H = 200, 200
    nx = Seq(400)
    art = blank(W, H)
    cx, cy, r = 100, 100, 88
    disc = circles(W, H, [(cx, cy, r)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = (np.arctan2(yy - cy + 30, xx - cx + 18) + math.pi) / math.tau * 6
    cols = [(CORAL, CORAL2), (CREAM, "#ffffff"), ("#2fa6d8", "#5cc2ea"), (CREAM, "#ffffff"), (SUN, SUN2), (CREAM, "#ffffff")]
    for i, (c1, c2) in enumerate(cols):
        art = GP(art, disc * (ang.astype(np.int32) % 6 == i), c1, c2, seed=nx(), rough=0.6, streak=0.4)
    cap = circles(W, H, [(cx - 18, cy - 30, 16)])
    art = GP(art, cap, CREAM, "#ffffff", seed=nx(), rough=0.4)
    art = G(art, inner_shade(disc, 18, 20, 18), "#3a4a7a", seed=nx(), density=0.3, edge=0.1, bloom=0.1, rough=2)
    art = G(art, gaussian_filter(circles(W, H, [(cx - 40, cy - 48, 12)]), 3), "#ffffff", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    art = G(art, contour(disc, 2.6, nx()), LINE, seed=nx(), density=0.75, edge=0, bloom=0, rough=0.6, feather=0.35)
    preview(art, "up-ball", tone="#f7e3b8")
    save(art, f"{OUT}/ball.webp", max_w=120, quality=84)
    clear()

if "crab" in PARTS:
    W, H = 300, 230
    nx = Seq(500)
    art = blank(W, H)
    RED, RED2 = "#f0643c", "#ff8a5c"
    legs = []
    for d in (-1, 1):
        for k in range(3):
            x0 = 150 + d * (40 + k * 12); y0 = 150 + k * 6
            legs.append((curve([(x0, y0), (x0 + d * 36, y0 + 10 - k * 2), (x0 + d * 50, y0 + 40)], 12), 9, (0.0, 0.5)))
    art = tn(art, strokes(W, H, legs), RED, RED2, nx, k=4)
    arms = [(curve([(110, 140), (70, 110), (60, 84)], 10), 12, None), (curve([(190, 140), (230, 110), (240, 84)], 10), 12, None)]
    art = tn(art, strokes(W, H, arms), RED, RED2, nx, k=4)
    for d in (-1, 1):
        x = 150 + d * 92
        claw = shapes(W, H, [[(x - 22 * d, 92), (x - 30 * d, 60), (x - 10 * d, 30), (x + 6 * d, 40), (x - 6 * d, 62), (x + 16 * d, 50), (x + 22 * d, 70), (x + 6 * d, 96)]])
        art = tn(art, claw, RED, RED2, nx, k=8)
    stalks = strokes(W, H, [([(130, 120), (124, 84)], 6, None), ([(170, 120), (176, 84)], 6, None)])
    art = tn(art, stalks, RED, RED2, nx, k=2, hi=False)
    body = shapes(W, H, [ellipse_pts(150, 150, 72, 46, 20)])
    art = tn(art, body, RED, RED2, nx, k=16, sh="#b8402a")
    for x in (124, 176):
        e = circles(W, H, [(x, 78, 13)])
        art = tn(art, e, "#ffffff", "#ffffff", nx, k=2, hi=False, line_a=0.8)
        art = GP(art, circles(W, H, [(x + 3, 80, 6)]), "#3a2418", seed=nx(), rough=0.3)
        art = GP(art, circles(W, H, [(x + 5, 77, 2)]), "#ffffff", seed=nx(), rough=0.2)
    smile = strokes(W, H, [(arc_pts(150, 148, 20, 0.25, math.pi - 0.25, 12), 3.4, (0.2, 0.2))])
    art = G(art, smile, "#6a2a18", seed=nx(), density=0.85, edge=0, bloom=0, rough=0.4)
    cheeks = circles(W, H, [(116, 156, 8), (184, 156, 8)])
    art = G(art, gaussian_filter(cheeks, 2), "#ff9a8a", seed=nx(), density=0.6, edge=0, bloom=0, rough=0.5)
    preview(art, "up-crab", tone="#f7e3b8")
    save(art, f"{OUT}/crab.webp", max_w=180, quality=84)
    clear()

if "bucket" in PARTS:
    W, H = 340, 320
    nx = Seq(600)
    art = blank(W, H)
    # spade leaning behind
    handle = strokes(W, H, [([(250, 40), (200, 230)], 12, None)])
    art = tn(art, handle, SUN, SUN2, nx, k=3)
    grip = shapes(W, H, [ellipse_pts(254, 34, 22, 10, 12, -0.3)])
    art = tn(art, grip, SUN, SUN2, nx, k=3)
    blade = shapes(W, H, [[(184, 220), (220, 232), (214, 296), (190, 312), (168, 292)]])
    art = tn(art, blade, CORAL, CORAL2, nx, k=6)
    # bucket
    body = shapes(W, H, [[(40, 130), (200, 130), (182, 300), (58, 300)]], smooth=False)
    art = tn(art, body, "#2fb3c8", "#5fd0dc", nx, k=14, sh="#1a7f94")
    rim = shapes(W, H, [ellipse_pts(120, 130, 82, 16, 20)])
    art = tn(art, rim, SUN, SUN2, nx, k=4)
    sand = shapes(W, H, [ellipse_pts(120, 128, 70, 11, 20)])
    art = GP(art, sand, SAND, SAND2, seed=nx(), rough=0.8)
    art = speckle(art, sand, nx, n=0.02, r=0.8)
    band = shapes(W, H, [[(48, 210), (192, 210), (189, 236), (51, 236)]], smooth=False) * body
    art = GP(art, band, CREAM, seed=nx(), rough=0.5)
    dots = circles(W, H, [(x, 223, 5) for x in range(66, 180, 22)]) * band
    art = GP(art, dots, CORAL, seed=nx(), rough=0.3)
    handle2 = strokes(W, H, [(arc_pts(120, 140, 88, math.pi * 1.05, math.pi * 1.95, 24, 0.9), 4, None)])
    art = G(art, handle2, LINE, seed=nx(), density=0.85, edge=0, bloom=0, rough=0.5)
    preview(art, "up-bucket", tone="#f7e3b8")
    save(art, f"{OUT}/bucket.webp", max_w=220, quality=84)
    clear()

if "waves" in PARTS:
    W, H = 780, 300
    nx = Seq(700); rng = random.Random(7)
    art = blank(W, H)
    xs = np.arange(-20, W + 40, 10)
    edge = [(x, 228 + 10 * math.sin(x / 46) + 5 * math.sin(x / 17 + 1)) for x in xs]
    sea = shapes(W, H, [[(-20, -30), (W + 40, -30)] + edge[::-1]], smooth=False)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = GP(art, sea, "#1f9fb6", "#2bb3c2", seed=nx(), rough=0.8, streak=1.0)
    art = G(art, sea * np.clip(yy * 1.8 - 0.4, 0, 1), SEA2, "#86e0dc", seed=nx(), density=0.75, edge=0.2, bloom=0.4, rough=3)
    # sparkle dashes on the water
    dashes = []
    for _ in range(46):
        x = rng.uniform(0, W); y = rng.uniform(10, 190); L = rng.uniform(14, 40)
        dashes.append(([(x, y), (x + L, y + rng.uniform(-1, 1))], rng.uniform(2, 3.4), (0.3, 0.3)))
    art = OV(art, strokes(W, H, dashes) * sea, lambda m: solid_rgba(m, "#ffffff", 0.6))
    # rolling wave crest lines
    crests = []
    for y0 in (70, 130, 180):
        x = rng.uniform(-60, 0)
        while x < W:
            L = rng.uniform(80, 150)
            crests.append((curve([(x, y0 + 6), (x + L * 0.4, y0 - 6), (x + L * 0.75, y0 - 2), (x + L, y0 + 8)], 16), 4, (0.2, 0.3)))
            x += L + rng.uniform(40, 90)
    art = OV(art, strokes(W, H, crests) * sea, lambda m: solid_rgba(m, "#e9fbfa", 0.8))
    # foam edge: scalloped white lace with bubbles, and a wet-sand band under it
    wet = shapes(W, H, [edge + [(W + 40, 300), (-20, 300)]], smooth=False) * (yy < 0.94)
    art = G(art, wet * np.clip(1 - (yy - 0.76) * 6, 0, 1), "#d9a865", seed=nx(), density=0.5, edge=0.3, bloom=0.4, rough=4)
    foam = []
    for i, (x, y) in enumerate(edge):
        foam.append((x, y - 2, rng.uniform(9, 16)))
    fm = circles(W, H, foam)
    fm = np.clip(fm + shapes(W, H, [[(x, y - 14) for x, y in edge] + [(x, y + 2) for x, y in edge[::-1]]], smooth=False), 0, 1)
    art = GP(art, fm, "#ffffff", "#f2fbfb", seed=nx(), rough=1.2, streak=0.3)
    art = G(art, contour(fm, 2.0, nx()) * (yy > 0.6), "#6ac0cc", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    bub = circles(W, H, [(rng.uniform(0, W), rng.uniform(180, 215), rng.uniform(2, 5)) for _ in range(60)]) * sea
    art = OV(art, bub, lambda m: solid_rgba(m, "#ffffff", 0.75))
    preview(art, "up-waves", tone="#f7e3b8")
    save_full(art, f"{OUT}/waves.webp", quality=74)
    clear()

if "shells" in PARTS:
    W, H = 420, 110
    nx = Seq(800)
    art = blank(W, H)
    st = []
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5
        st.append(petal_pts(210 + math.cos(a) * 3, 56 + math.sin(a) * 3, 44, 12, a, n=8))
    stm = shapes(W, H, st)
    art = tn(art, stm, SUN, SUN2, nx, k=6)
    art = GP(art, circles(W, H, [(210 + math.cos(-math.pi / 2 + k * math.tau / 5) * 20, 56 + math.sin(-math.pi / 2 + k * math.tau / 5) * 20, 3) for k in range(5)]), "#ffffff", seed=nx(), rough=0.3)
    for x, c, f in [(110, CORAL, 1), (310, "#ffb3a6", -1)]:
        sh = shapes(W, H, [[(x - 30, 70)] + arc_pts(x, 72, 32, math.pi * 1.05, math.pi * 1.95, 14) + [(x + 30, 70), (x + 8, 86), (x - 8, 86)]])
        art = tn(art, sh, c, mix(c, "#ffffff", 0.3), nx, k=5)
        art = G(art, strokes(W, H, [([(x, 84), (x + math.cos(a) * 30, 72 + math.sin(a) * 30)], 1.6, None) for a in np.linspace(math.pi * 1.15, math.pi * 1.85, 6)]) * sh, LINE, seed=nx(), density=0.45, edge=0, bloom=0)
    for x in (30, 390):
        sp = shapes(W, H, [ellipse_pts(x, 62, 14, 22, 12, 0.4)])
        art = tn(art, sp, CREAM, "#ffffff", nx, k=4)
        art = G(art, strokes(W, H, [(spiral_pts(x, 62, 2, 12, 0, 1.5, 30), 1.6, None)]) * sp, LINE, seed=nx(), density=0.5, edge=0, bloom=0)
    preview(art, "up-shells", tone="#f7e3b8")
    save(art, f"{OUT}/shells.webp", max_w=280, quality=84)
    clear()

if "sand" in PARTS or len(sys.argv) == 1:
    W = H = 256
    rng = np.random.default_rng(12)
    def wrapnoise(s):
        n = gaussian_filter(rng.random((H, W)).astype(np.float32), s, mode="wrap")
        return (n - n.min()) / (n.max() - n.min() + 1e-6)
    base = np.array(hex_rgb("#f6d9a0"), np.float32)
    rgb = np.ones((H, W, 3), np.float32) * base
    rgb *= (0.95 + 0.08 * wrapnoise(18) + 0.04 * wrapnoise(5))[..., None]
    for col, thr, s in (("#b07a3a", 0.9965, 0.7), ("#fff6e0", 0.996, 0.6), ("#d9a865", 0.993, 0.9)):
        sp = (rng.random((H, W)) > thr).astype(np.float32)
        sp = np.clip(gaussian_filter(sp, s, mode="wrap") * 5, 0, 1)[..., None]
        rgb = rgb * (1 - sp * 0.8) + np.array(hex_rgb(col), np.float32) * sp * 0.8
    img = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    save_full(img, f"{OUT}/sand.webp", quality=72)
