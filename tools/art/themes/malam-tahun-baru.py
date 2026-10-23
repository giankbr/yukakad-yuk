"""Malam Tahun Baru — New Year's Eve party: a painted night over a city skyline with fireworks (gold, coral, mint)
and drifting smoke, a gilded clock at midnight (face + separate hands for the countdown motion), firework blooms
for popping, confetti and foil streamers, two champagne coupes. Gouache night scene + gold foil.
Run: python3 -I malam-tahun-baru.py [part ...]
parts: sky clock burst confetti coupes streamer -> public/themes/art/malam-tahun-baru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i5_lib import *

OUT = outdir("malam-tahun-baru")
PARTS = sys.argv[1:] or ["sky", "clock", "burst", "confetti", "coupes", "streamer"]
SEQ = Seq(2027)
GOLD, GOLD_L = "#e6bf6e", "#fff0c4"
CORAL, MINT = "#ff6f61", "#7fe3c8"
NIGHT = [(0, "#041015"), (0.45, "#082029"), (0.8, "#0d3440"), (1, "#123f4a")]


def bloom(lay, W, H, cx, cy, R, col, rng, rays=40, width=3.2, core=GOLD_L, droop=0.2, alpha=1.0):
    """A painted firework: glowing trails curving under gravity, bright tips, a soft halo, and the core."""
    trail, tips = firework(W, H, cx, cy, R, rng, rays=rays, width=width, droop=droop)
    halo = circles(W, H, [(cx, cy + R * 0.08, R * 0.95)])
    lay = over(lay, glow(halo, col, radius=R * 0.35, strength=0.12 * alpha))
    lay = over(lay, glow(trail, col, radius=5, strength=0.5 * alpha))
    lay = OV(lay, trail, lambda m: gouache_paint(m, col, mix(col, "#ffffff", .35), seed=SEQ(), rough=1.2, streak=0.3, density=0.92 * alpha), pad=8)
    lay = over(lay, glow(tips, GOLD_L, radius=3, strength=0.9 * alpha))
    lay = over(lay, rgba("#fffbe8", np.clip(tips * 1.2, 0, 1) * alpha))
    c = circles(W, H, [(cx, cy, R * 0.07)])
    lay = over(lay, glow(c, core, radius=R * 0.08, strength=0.8 * alpha))
    return lay


def sparkle_dust(lay, W, H, rng, n, box, col, rmax=2.2):
    x0, y0, x1, y1 = box
    pts = [(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(0.6, rmax)) for _ in range(n)]
    m = circles(W, H, pts)
    lay = over(lay, glow(m, col, radius=2.5, strength=0.5))
    return over(lay, rgba(col, m * 0.9))


def skyline(W, H, base, rng):
    """Masks: buildings silhouette and lit windows."""
    bl, wins = [], []
    x = -10
    while x < W + 10:
        bw = rng.uniform(34, 78)
        bh = rng.uniform(70, 250) * (1.25 if abs(x - W * 0.62) < 70 else 1.0)
        top = base - bh
        pts = [(x, H + 10), (x, top), (x + bw, top), (x + bw, H + 10)]
        if rng.random() < 0.25:  # stepped / spire tops
            pts = [(x, H + 10), (x, top + 20), (x + bw * 0.3, top + 20), (x + bw * 0.5, top - 30), (x + bw * 0.7, top + 20), (x + bw, top + 20), (x + bw, H + 10)]
        bl.append(pts)
        for wy in np.arange(top + 14, base, 13):
            for wx in np.arange(x + 7, x + bw - 7, 10):
                if rng.random() < 0.28:
                    wins.append([(wx, wy), (wx + 4.5, wy), (wx + 4.5, wy + 6), (wx, wy + 6)])
        x += bw + rng.uniform(-6, 4)
    return shapes(W, H, bl, smooth=False), shapes(W, H, wins, smooth=False)


def p_sky():
    W, H = 780, 1120
    rng = random.Random(31)
    lay = painted_sky(W, H, NIGHT, seed=7, streak=1.0, grain=0.8)
    # smoke haze drifting from earlier bursts
    for (x, y, rx, ry) in [(220, 420, 260, 80), (560, 300, 220, 70), (400, 620, 340, 90)]:
        sm = ellipses(W, H, [(x, y, rx, ry, rng.uniform(-8, 8))])
        lay = over(lay, rgba("#5d8590", gaussian_filter(displace(sm, SEQ(), 30, 80), 30) * 0.16))
    flush()
    lay = sparkle_dust(lay, W, H, rng, 70, (0, 0, W, 700), "#dfeee9", 1.4)
    lay = bloom(lay, W, H, 560, 230, 170, GOLD, rng, rays=46, width=3.4)
    flush()
    lay = bloom(lay, W, H, 190, 330, 130, CORAL, rng, rays=36, width=3.0)
    flush()
    lay = bloom(lay, W, H, 380, 520, 96, MINT, rng, rays=30, width=2.6, alpha=0.85)
    flush()
    lay = bloom(lay, W, H, 700, 520, 70, CORAL, rng, rays=24, width=2.2, alpha=0.7)
    lay = bloom(lay, W, H, 90, 120, 60, MINT, rng, rays=22, width=2.0, alpha=0.6)
    flush()
    # rising rocket trails
    tr = strokes(W, H, [(curve([(470, 900), (480, 760), (500, 640), (520, 590)], 30), 2.2, (0.9, 0.05)), (curve([(150, 900), (140, 760), (160, 640)], 30), 2.0, (0.9, 0.05))])
    lay = over(lay, glow(tr, GOLD, 4, 0.5))
    lay = over(lay, rgba(GOLD_L, tr * 0.6))
    # city: far row lighter teal, near row near-black, warm windows
    far, farw = skyline(W, H, 930, random.Random(5))
    lay = OV(lay, far, lambda m: gouache_paint(m, "#0f2f38", "#14404a", seed=SEQ(), rough=1.0, streak=0.6), pad=4)
    lay = over(lay, rgba("#f3c779", linocut(farw, "#ffffff", seed=SEQ(), wear=0.4)[..., 3] * 0.55))
    near, nearw = skyline(W, H, 1010, random.Random(9))
    lay = OV(lay, near, lambda m: gouache_paint(m, "#061419", "#0a1d23", seed=SEQ(), rough=1.0, streak=0.6), pad=4)
    lay = over(lay, glow(nearw, "#ffcf7a", 3, 0.35))
    lay = over(lay, rgba("#ffd98f", linocut(nearw, "#ffffff", seed=SEQ(), wear=0.3)[..., 3] * 0.85))
    # glow of the city on the low sky
    gl = shapes(W, H, [[(0, 860), (W, 860), (W, 960), (0, 960)]], smooth=False)
    lay = over(lay, rgba("#ff9f6b", gaussian_filter(gl, 50) * 0.12 * (1 - far)))
    flush()
    preview(lay, "mtb-sky")
    save_rgb(lay, f"{OUT}/sky.webp", size=(780, 1120), quality=74)


def p_clock():
    W = H = 620
    cx = cy = 310
    face = circles(W, H, [(cx, cy, 250)])
    bezel = np.clip(circles(W, H, [(cx, cy, 292)]) - circles(W, H, [(cx, cy, 252)]), 0, 1)
    lay = blank(W, H)
    lay = over(lay, soft_shadow(circles(W, H, [(cx, cy, 292)]), "#000000", 16, 0.55, 6, 12))
    lay = OV(lay, face, lambda m: gouache_paint(m, "#f6ecd6", "#ead9b6", seed=SEQ(), rough=0.6, streak=0.5), pad=6)
    sh = shade_field(face, (-0.6, -0.7), 40, 60)
    lay = darken(lay, sh * face * 0.5, 0.35)
    lay = FO(lay, bezel, GOLD, seed=SEQ(), emboss=0.9, sparkle=0.2)
    inner = np.clip(circles(W, H, [(cx, cy, 236)]) - circles(W, H, [(cx, cy, 232)]), 0, 1)
    lay = FO(lay, inner, "#c9a052", seed=SEQ(), emboss=0.5, sparkle=0.0)
    ticks = []
    for i in range(60):
        a = i / 60 * math.tau
        r0, r1 = (198, 228) if i % 5 == 0 else (216, 228)
        w = 7 if i % 5 == 0 else 2.4
        ticks.append(([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], w, None))
    tm = strokes(W, H, ticks, cap=False)
    lay = OV(lay, tm, lambda m: linocut(m, "#1d2a2e", seed=SEQ(), wear=0.15))
    # numerals XII III VI IX
    def draw(cv):
        font = skia.Font(skia.Typeface("serif", skia.FontStyle.Bold()), 54)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for txt, a in (("XII", -math.pi / 2), ("III", 0), ("VI", math.pi / 2), ("IX", math.pi)):
            w = font.measureText(txt)
            x = cx + math.cos(a) * 158 - w / 2
            y = cy + math.sin(a) * 158 + 19
            cv.c.drawString(txt, x, y, font, p)
    nm = mask_from(W, H, draw)
    lay = FO(lay, nm, "#b8883c", seed=SEQ(), emboss=0.7, sparkle=0.1)
    preview(lay, "mtb-clock", bg="#082029")
    save_full(lay, f"{OUT}/clock.webp", size=(310, 310), quality=84)
    # hands: drawn pointing up from the centre of a same-size canvas, so CSS rotates them about 50% 50%
    for name, L, w0, tail in (("hand-h", 128, 22, 30), ("hand-m", 196, 14, 40)):
        hm = shapes(W, H, [[(cx - w0 / 2, cy + tail), (cx - w0 * 0.6, cy - L * 0.55), (cx, cy - L), (cx + w0 * 0.6, cy - L * 0.55), (cx + w0 / 2, cy + tail)]], smooth=False)
        hl = OV(blank(W, H), shift(hm, 4, 6), lambda m: rgba("#000000", gaussian_filter(m, 4) * 0.4))
        hl = FO(hl, hm, GOLD, seed=SEQ(), emboss=1.0, sparkle=0.1)
        if name == "hand-m":
            hub = circles(W, H, [(cx, cy, 20)])
            hl = FO(hl, hub, "#d4a957", seed=SEQ(), emboss=1.0, sparkle=0.15)
        save_full(hl, f"{OUT}/{name}.webp", size=(310, 310), quality=84)


def p_burst():
    for name, col, seed in (("burst-gold", GOLD, 3), ("burst-coral", CORAL, 5), ("burst-mint", MINT, 7)):
        W = H = 420
        rng = random.Random(seed)
        lay = bloom(blank(W, H), W, H, 210, 200, 140, col, rng, rays=34, width=3.6, droop=0.12)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        fade = np.clip((205 - np.hypot(xx - 210, yy - 210)) / 30, 0, 1)
        lay[..., 3] *= fade
        save_full(lay, f"{OUT}/{name}.webp", size=(210, 210), quality=80)
        flush()
    preview(lay, "mtb-burst", bg="#082029")


def p_confetti():
    """Seamless (vertical) confetti scatter: gouache flecks, foil squiggles, a few streamer curls."""
    W, H = 780, 900
    rng = random.Random(77)
    lay = blank(W, H)
    cols = [CORAL, MINT, "#ffffff", "#f3b2c7"]
    for col in cols:
        polys = []
        for _ in range(11):
            x, y = rng.uniform(10, W - 10), rng.uniform(20, H - 20)
            a = rng.uniform(0, math.pi)
            l, w = rng.uniform(9, 18), rng.uniform(5, 9)
            polys.append([(x + math.cos(a) * l - math.sin(a) * w, y + math.sin(a) * l + math.cos(a) * w), (x + math.cos(a) * l + math.sin(a) * w, y + math.sin(a) * l - math.cos(a) * w),
                          (x - math.cos(a) * l + math.sin(a) * w, y - math.sin(a) * l - math.cos(a) * w), (x - math.cos(a) * l - math.sin(a) * w, y - math.sin(a) * l + math.cos(a) * w)])
        m = shapes(W, H, polys, smooth=False)
        lay = OV(lay, m, lambda mm: gouache_paint(mm, col, mix(col, "#000000", .15), seed=SEQ(), rough=1.0, streak=0.4))
    sq = []
    for _ in range(10):
        x, y = rng.uniform(20, W - 20), rng.uniform(30, H - 30)
        a = rng.uniform(0, math.tau)
        pts = [(x + math.cos(a) * t * 10 + math.sin(t * 2.2) * 6 * -math.sin(a), y + math.sin(a) * t * 10 + math.sin(t * 2.2) * 6 * math.cos(a)) for t in np.linspace(0, 3.2, 14)]
        sq.append((pts, 4.0, (0.15, 0.15)))
    lay = FO(lay, strokes(W, H, sq), GOLD, seed=SEQ(), emboss=0.6, sparkle=0.3)
    dots = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.5, 5)) for _ in range(16)])
    lay = FO(lay, dots, GOLD, seed=SEQ(), emboss=0.6, sparkle=0.3)
    save_full(lay, f"{OUT}/confetti.webp", size=(390, 450), quality=78)
    preview(lay, "mtb-confetti", bg="#082029")


def p_coupes():
    """Two champagne coupes clinking, gold foil + glass glints."""
    W, H = 620, 520
    lay = blank(W, H)
    for (cx, tilt, flip) in ((220, 0.22, 1), (400, -0.22, -1)):
        def T(x, y):
            c, s_ = math.cos(tilt), math.sin(tilt)
            return (cx + x * c - y * s_, 300 + x * s_ + y * c)
        bowl = [T(-110, -90), T(110, -90), T(96, -40), T(50, 0), T(10, 8), T(-10, 8), T(-50, 0), T(-96, -40)]
        stem_ = [T(-6, 6), T(6, 6), T(5, 150), T(-5, 150)]
        foot = [T(-62, 150), T(62, 150), T(56, 166), T(-56, 166)]
        wine = [T(-98, -66), T(98, -66), T(88, -38), T(48, -4), T(10, 4), T(-10, 4), T(-48, -4), T(-88, -38)]
        mg = shapes(W, H, [bowl])
        lay = over(lay, rgba("#dff3ef", mg * 0.18))
        mw = shapes(W, H, [wine])
        lay = OV(lay, mw, lambda m: gouache_paint(m, "#f2d38a", "#d7a94e", seed=SEQ(), rough=1.0, streak=0.4, density=0.9))
        bub = circles(W, H, [(*T(random.Random(SEQ()).uniform(-60, 60), random.Random(SEQ()).uniform(-50, -10)), 3) for _ in range(9)])
        lay = over(lay, rgba("#fff7dc", bub * 0.9))
        rim = strokes(W, H, [([T(-110, -90), T(110, -90)], 5, None)])
        out_ = np.clip(edge_line(mg, 3, SEQ()) + rim, 0, 1)
        lay = FO(lay, out_, GOLD, seed=SEQ(), emboss=0.5, sparkle=0.2)
        lay = FO(lay, np.clip(shapes(W, H, [stem_, foot], smooth=False), 0, 1), GOLD, seed=SEQ(), emboss=0.8, sparkle=0.2)
        gl = strokes(W, H, [([T(-80 * flip, -78), T(-60 * flip, -30)], 6, (0.3, 0.3))])
        lay = over(lay, rgba("#ffffff", gaussian_filter(gl, 1.5) * 0.7))
    # clink sparks
    sp = strokes(W, H, [([(310, 150), (310, 100)], 5, (0.2, 0.6)), ([(330, 160), (370, 120)], 5, (0.2, 0.6)), ([(290, 160), (250, 120)], 5, (0.2, 0.6))])
    lay = FO(lay, sp, GOLD_L, seed=SEQ(), emboss=0.3, sparkle=0.3)
    preview(lay, "mtb-coupes", bg="#082029")
    save(lay, f"{OUT}/coupes.webp", max_w=300, quality=82)


def p_streamer():
    """Divider: a curling foil streamer with a few confetti flecks."""
    W, H = 640, 120
    rng = random.Random(3)
    pts = [(20 + t * 600, 60 + math.sin(t * math.tau * 2.0) * 26 + math.sin(t * 17) * 3) for t in np.linspace(0, 1, 90)]
    m = strokes(W, H, [(pts, 7, (0.1, 0.1))])
    lay = FO(blank(W, H), m, GOLD, seed=SEQ(), emboss=0.8, sparkle=0.3)
    for col in (CORAL, MINT):
        c = circles(W, H, [(rng.uniform(40, 600), rng.uniform(15, 105), rng.uniform(4, 6)) for _ in range(5)])
        lay = OV(lay, c, lambda mm: gouache_paint(mm, col, seed=SEQ(), rough=0.8))
    preview(lay, "mtb-streamer", bg="#082029")
    save(lay, f"{OUT}/streamer.webp", max_w=320, quality=82)


for p in PARTS:
    {"sky": p_sky, "clock": p_clock, "burst": p_burst, "confetti": p_confetti, "coupes": p_coupes, "streamer": p_streamer}[p]()
    flush()
kb(OUT)
