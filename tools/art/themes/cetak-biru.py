"""Cetak Biru — an architect's blueprint of the couple's dream house: diazo-printed white line work (front elevation,
ground-floor plan, dimension strings, hand-lettered labels) on mottled cyan-blue paper, and gouache drafting tools.
Run: python3 -I cetak-biru.py [part ...]   parts: paper elevation plan tools. Assets -> public/themes/art/cetak-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m4_lib import *

OUT = outdir("cetak-biru")
PARTS = sys.argv[1:] or ["paper", "elevation", "plan", "tools"]
BLUE, BLUE_D, BLUE_L = "#1f5fa6", "#174c8a", "#2b6fb8"
INK = "#f3f9ff"
HAND = skia.Typeface.MakeFromFile("/tmp/pen/art/themes/_m4_fonts/ArchitectsDaughter.ttf")


class Draft:
    """Collects precise line work, then prints it like a diazo copy."""
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.cv = Canvas(W, H)
        self.c = self.cv.c

    def p(self, w=2.0, fill=False):
        return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=w,
                          Style=skia.Paint.kFill_Style if fill else skia.Paint.kStroke_Style,
                          StrokeCap=skia.Paint.kSquare_Cap, StrokeJoin=skia.Paint.kMiter_Join)

    def line(self, x0, y0, x1, y1, w=2.0):
        self.c.drawLine(x0, y0, x1, y1, self.p(w))

    def poly(self, pts, w=2.0, closed=True):
        path = skia.Path()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        if closed:
            path.close()
        self.c.drawPath(path, self.p(w))

    def rect(self, x0, y0, x1, y1, w=2.0, fill=False):
        self.c.drawRect(skia.Rect(x0, y0, x1, y1), self.p(w, fill))

    def erase(self, x0, y0, x1, y1):
        self.c.drawRect(skia.Rect(x0, y0, x1, y1), skia.Paint(BlendMode=skia.BlendMode.kClear))

    def circle(self, x, y, r, w=2.0):
        self.c.drawCircle(x, y, r, self.p(w))

    def arc(self, x, y, r, a0, sweep, w=1.4):
        self.c.drawArc(skia.Rect(x - r, y - r, x + r, y + r), a0, sweep, False, self.p(w))

    def text(self, s, x, y, size=18, align="c", rot=0.0):
        font = skia.Font(HAND, size)
        wd = font.measureText(s)
        self.c.save()
        self.c.translate(x, y)
        self.c.rotate(rot)
        dx = -wd / 2 if align == "c" else (-wd if align == "r" else 0)
        self.c.drawString(s, dx, size * 0.35, font, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        self.c.restore()

    def dim_h(self, x0, x1, y, label, size=16, ext=None):
        self.line(x0, y, x1, y, 1.2)
        for x in (x0, x1):
            self.line(x - 6, y + 6, x + 6, y - 6, 1.6)  # architectural tick
            if ext is not None:
                self.line(x, ext, x, y + 8, 0.9)
        self.text(label, (x0 + x1) / 2, y - 12, size)

    def dim_v(self, x, y0, y1, label, size=16, ext=None):
        self.line(x, y0, x, y1, 1.2)
        for y in (y0, y1):
            self.line(x - 6, y + 6, x + 6, y - 6, 1.6)
            if ext is not None:
                self.line(ext, y, x - 8, y, 0.9)
        self.text(label, x - 13, (y0 + y1) / 2, size, rot=-90)

    def hatch_rect(self, x0, y0, x1, y1, step=7, w=0.9):
        self.c.save()
        self.c.clipRect(skia.Rect(x0, y0, x1, y1))
        span = (x1 - x0) + (y1 - y0)
        for k in range(int(span / step) + 2):
            o = k * step
            self.line(x0 + o, y0, x0 + o - (y1 - y0), y1, w)
        self.c.restore()

    def tree(self, x, y, r, rng):
        """Architect's tree: loose overlapping loops + trunk."""
        self.line(x, y + r * 0.6, x, y + r * 2.1, 2.2)
        for k in range(5):
            pts = []
            rr = r * rng.uniform(0.75, 1.0)
            cx, cy = x + rng.uniform(-r * 0.15, r * 0.15), y + rng.uniform(-r * 0.12, r * 0.12)
            for i in range(40):
                a = i / 39 * math.tau * 1.05
                q = rr * (1 + 0.08 * math.sin(a * 7 + k))
                pts.append((cx + math.cos(a) * q, cy + math.sin(a) * q))
            self.poly(pts, 1.1, closed=False)

    def print(self, seed=1, glow=0.25):
        """Diazo print: slight wobble + bleed, uneven ink take, soft halo; returns RGBA (white on transparent)."""
        m = self.cv.array()[..., 3]
        m = displace(m, seed, 0.7, 16)
        m = np.clip(gaussian_filter(m, 0.45) * 1.15, 0, 1)
        h, w = m.shape
        take = 0.78 + 0.22 * fbm(w, h, seed + 3, 30, 3)
        speck = fbm(w, h, seed + 5, 3, 2)
        a = m * take * (1 - 0.3 * np.clip((speck - 0.7) * 5, 0, 1))
        a = np.maximum(a, gaussian_filter(m, 2.4) * glow)
        return flat(np.clip(a, 0, 1), INK)


if "paper" in PARTS:
    # 512 seamless blueprint paper: diazo cyan with mottling, darker fibres, faint printed grid
    S = 512
    nx = Seq(60000)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rgb = np.ones((S, S, 3), np.float32) * np.array(hex_rgb(BLUE), np.float32)
    mot = wrap_noise(S, S, nx(), 40) * 0.6 + wrap_noise(S, S, nx(), 12) * 0.4
    rgb = rgb * (0.9 + 0.2 * mot[..., None])
    fib = gaussian_filter(np.random.default_rng(nx()).random((S, S)).astype(np.float32), (0.5, 3.0), mode="wrap")
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    rgb = rgb * (1 + fib[..., None] * 0.018)
    grain = gaussian_filter(np.random.default_rng(nx()).random((S, S)).astype(np.float32), 0.6, mode="wrap")
    rgb = rgb * (0.97 + 0.06 * grain[..., None])
    grid = np.zeros((S, S), np.float32)
    for k in range(0, S, 32):
        a = 0.16 if k % 128 == 0 else 0.07
        grid[:, k] = np.maximum(grid[:, k], a); grid[k, :] = np.maximum(grid[k, :], a)
    grid = gaussian_filter(grid, 0.5, mode="wrap") * 1.6
    rgb = rgb * (1 - grid[..., None]) + np.array(hex_rgb("#cfe4ff"), np.float32) * grid[..., None]
    art = np.concatenate([np.clip(rgb, 0, 1), np.ones((S, S, 1), np.float32)], -1)
    prev(np.concatenate([art, art], 1), "cb-paper")
    save_rgb(art, f"{OUT}/paper.webp", quality=86)

if "elevation" in PARTS:
    W, H = 800, 580
    rng = random.Random(3)
    d = Draft(W, H)
    G0 = 470
    # ground + earth hatch
    d.line(30, G0, 770, G0, 3.2)
    for x in range(36, 770, 14):
        d.line(x, G0 + 3, x - 9, G0 + 12, 0.9)
    # main block with gable roof
    d.rect(120, 250, 440, G0, 2.6)
    d.poly([(96, 256), (280, 112), (464, 256)], 2.8, closed=False)
    d.poly([(110, 256), (280, 126), (450, 256)], 1.4, closed=False)
    d.line(96, 256, 464, 256, 1.6)
    d.circle(280, 196, 20, 1.8); d.line(260, 196, 300, 196, 1); d.line(280, 176, 280, 216, 1)
    # upper windows (ribbon) + balcony rail
    d.rect(160, 282, 400, 344, 2.0)
    for x in (220, 280, 340):
        d.line(x, 282, x, 344, 1.3)
    d.line(150, 352, 410, 352, 1.6)
    for x in range(156, 410, 10):
        d.line(x, 352, x, 372, 0.8)
    d.line(150, 372, 410, 372, 1.6)
    # floor line, entrance glass door with sidelight, window
    d.line(120, 372, 440, 372, 1.0)
    d.rect(160, 384, 260, G0, 2.0); d.line(210, 384, 210, G0, 1.3)
    d.circle(204, 430, 2.6, 1.2); d.circle(216, 430, 2.6, 1.2)
    d.rect(296, 392, 410, 446, 2.0); d.line(353, 392, 353, 446, 1.3)
    d.line(290, 452, 416, 452, 1.6)
    # steps
    for k in range(3):
        d.line(150 - k * 8, G0 - k * 7 + 0, 270 + k * 8, G0 - k * 7, 1.2)
    # wing with flat roof, canopy, louvred window
    d.rect(440, 318, 690, G0, 2.6)
    d.line(432, 304, 706, 304, 2.6); d.line(432, 318, 706, 318, 1.6); d.line(432, 304, 432, 318, 1.6); d.line(706, 304, 706, 318, 1.6)
    d.rect(470, 356, 660, 430, 2.0)
    for y in range(364, 430, 8):
        d.line(474, y, 656, y, 0.8)
    d.line(464, 436, 666, 436, 1.6)
    # planter + plants
    d.rect(470, 448, 660, G0, 1.4)
    for x in range(480, 660, 22):
        d.poly([(x, 448), (x + 6, 428), (x + 10, 448)], 1.0, closed=False)
    d.tree(735, 330, 46, rng)
    d.tree(66, 360, 30, rng)
    # dimension strings
    d.dim_h(120, 440, 510, "8.000", ext=G0 + 4)
    d.dim_h(440, 690, 510, "6.400", ext=G0 + 4)
    d.dim_h(120, 690, 546, "14.400")
    d.dim_v(30, 112, G0, "7.200", ext=96)
    d.dim_v(760, 304, G0, "4.150", ext=712)
    # level marks
    for y, t in ((G0, "±0.00"), (372, "+3.20"), (256, "+6.40")):
        d.poly([(84, y - 1), (76, y - 11), (92, y - 11)], 1.3)
        d.text(t, 62, y - 22, 14, align="c")
    art = d.print(seed=61)
    prev(art, "cb-elevation", BLUE)
    save(art, f"{OUT}/elevation.webp", max_w=700, quality=80)

if "plan" in PARTS:
    W, H = 800, 700
    rng = random.Random(7)
    d = Draft(W, H)
    T = 14  # wall thickness
    X0, Y0, X1, Y1 = 90, 90, 710, 560

    def wall(x0, y0, x1, y1):
        d.rect(x0, y0, x1, y1, 1.6)
        d.hatch_rect(x0, y0, x1, y1, 6, 0.8)

    # outer walls (with gaps for doors/windows later drawn over)
    wall(X0, Y0, X1, Y0 + T); wall(X0, Y1 - T, X1, Y1); wall(X0, Y0, X0 + T, Y1); wall(X1 - T, Y0, X1, Y1)
    # interior walls
    wall(380, Y0, 380 + T, 330); wall(X0, 316, 380, 330); wall(560, Y0, 560 + T, 300); wall(380, 300, X1, 314)
    # erase openings by painting "paper" over: draw with BLUE later -> instead mark openings with door swings/windows on top
    # openings cut through the walls, then door leaves + swing arcs
    d.erase(316, 315, 372, 331); d.line(316, 316, 316, 330, 1.6); d.line(372, 316, 372, 330, 1.6)
    d.line(316, 330, 316, 386, 1.4); d.arc(316, 330, 56, 0, 90)
    d.erase(559, 238, 575, 292); d.line(560, 238, 574, 238, 1.6); d.line(560, 292, 574, 292, 1.6)
    d.line(574, 292, 626, 292, 1.4); d.arc(574, 292, 52, 270, 90)
    d.erase(404, 299, 470, 315); d.line(404, 300, 404, 314, 1.6); d.line(470, 300, 470, 314, 1.6)
    d.erase(300, Y1 - T - 1, 366, Y1 + 1); d.line(300, Y1 - T, 300, Y1, 1.6); d.line(366, Y1 - T, 366, Y1, 1.6)
    d.line(366, Y1 - T, 366, Y1 - T - 66, 1.4); d.arc(366, Y1 - T, 66, 180, 90)
    # windows (three-line) on the outer walls
    for (x0, x1) in ((150, 320), (430, 530), (600, 680)):
        d.line(x0, Y0 + 4, x1, Y0 + 4, 1); d.line(x0, Y0 + 10, x1, Y0 + 10, 1)
    # bed + nightstands (K. Tidur Utama, top-left)
    d.rect(150, 150, 300, 270, 1.8); d.rect(160, 158, 222, 186, 1.2); d.rect(228, 158, 290, 186, 1.2); d.line(150, 200, 300, 200, 1)
    d.rect(118, 152, 144, 178, 1.2); d.rect(306, 152, 332, 178, 1.2)
    # bath (top-right)
    d.rect(590, 130, 690, 180, 1.6); d.poly([(600, 140), (680, 140), (680, 170), (600, 170)], 1.0)
    d.circle(640, 250, 16, 1.4); d.circle(610, 250, 6, 1.2)
    # kitchen counter + sink (mid-top)
    d.rect(400, 110, 540, 140, 1.6); d.circle(440, 125, 9, 1.2); d.circle(500, 125, 6, 1.0); d.circle(520, 125, 6, 1.0)
    d.rect(420, 200, 520, 260, 1.6)
    for cx, cy in ((440, 190), (500, 190), (440, 270), (500, 270)):
        d.rect(cx - 10, cy - 8, cx + 10, cy + 8, 1.0)
    # living: sofa L, coffee table, rug
    d.rect(130, 380, 330, 420, 1.6); d.rect(130, 420, 170, 500, 1.6)
    d.circle(226, 466, 30, 1.4); d.rect(180, 432, 272, 500, 0.9)
    # dining / study at right
    d.rect(450, 380, 680, 430, 1.4); d.rect(600, 450, 680, 530, 1.4)
    d.circle(520, 480, 30, 1.4)
    # terrace + garden (below)
    d.line(X0, Y1 + 60, X1, Y1 + 60, 1.0)
    for x in range(X0, X1, 22):
        d.line(x, Y1, x, Y1 + 60, 0.6)
    d.tree(744, 600, 28, rng); d.tree(50, 140, 26, rng)
    # labels
    for s_, x, y in (("K. TIDUR UTAMA", 225, 295), ("DAPUR", 470, 165), ("K. MANDI", 640, 210), ("R. KELUARGA", 260, 360),
                     ("R. MAKAN", 520, 360), ("TERAS", 400, Y1 + 32), ("TAMAN", 744, 672)):
        d.text(s_, x, y, 19)
    d.dim_h(X0, 380, 50, "6.300", ext=Y0 - 4)
    d.dim_h(380, X1, 50, "7.200", ext=Y0 - 4)
    d.dim_v(40, 330, Y1, "5.200", ext=X0 - 4)
    # north arrow
    d.circle(740, 60, 22, 1.4); d.poly([(740, 36), (750, 72), (740, 64), (730, 72)], 1.4); d.text("U", 740, 98, 18)
    art = d.print(seed=71)
    prev(art, "cb-plan", BLUE)
    save(art, f"{OUT}/plan.webp", max_w=640, quality=80)

if "tools" in PARTS:
    # gouache drafting tools lying on the sheet: clear set-square, a pencil, a compass — with soft cast shadows
    W, H = 760, 460
    nx = Seq(62000)
    art = blank(W, H)
    # set square (45°) — translucent, with an inner cut-out and printed ticks
    tri = [(60, 400), (420, 400), (60, 60)]
    inner = [(110, 360), (300, 360), (110, 170)]
    tm = shapes(W, H, [tri], smooth=False)
    im_ = shapes(W, H, [inner], smooth=False)
    body = np.clip(tm - im_, 0, 1)
    art = over(art, soft_shadow(body, "#0a2448", blur=6, strength=0.45, dx=10, dy=12))
    art = OV(art, body, lambda m: flat(m, "#d9efff", 0.32))
    edge = np.clip(body - gaussian_filter(body, 1.6) * 0.98, 0, 1) * 3
    art = soft(art, np.clip(edge, 0, 1), "#f4fbff", alpha=0.8, pad=4)
    ticks = lines(W, H, [([(70 + k * 10, 400), (70 + k * 10, 400 - (12 if k % 5 == 0 else 6))], 1.0) for k in range(34)])
    art = soft(art, ticks * tm, "#ffffff", alpha=0.75, pad=4)
    # pencil, diagonal
    p0, p1 = (300, 430), (700, 170)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    def along(t, off):
        return (p0[0] + math.cos(ang) * L * t - math.sin(ang) * off, p0[1] + math.sin(ang) * L * t + math.cos(ang) * off)
    body_p = shapes(W, H, [[along(0.1, -9), along(0.92, -9), along(0.92, 9), along(0.1, 9)]], smooth=False)
    tip_w = shapes(W, H, [[along(0.1, -9), along(0.1, 9), along(0.0, 0)]], smooth=False)
    lead = shapes(W, H, [[along(0.03, -3), along(0.03, 3), along(0.0, 0)]], smooth=False)
    cap = shapes(W, H, [[along(0.92, -9), along(1.0, -9), along(1.0, 9), along(0.92, 9)]], smooth=False)
    allp = np.maximum.reduce([body_p, tip_w, cap])
    art = over(art, soft_shadow(allp, "#0a2448", blur=5, strength=0.5, dx=8, dy=10))
    art = GP(art, body_p, "#243446", "#33475e", seed=nx(), rough=0.6, streak=1.4)
    art = soft(art, body_p * shapes(W, H, [[along(0.1, -9), along(0.92, -9), along(0.92, -3), along(0.1, -3)]], smooth=False), "#6a86a6", alpha=0.45)
    art = GP(art, tip_w, "#e3c79a", "#cfae7c", seed=nx(), rough=0.6, streak=1.0)
    art = GP(art, lead, "#2a2a30", seed=nx(), rough=0.4)
    art = GP(art, cap, "#c9ccd2", "#9aa0aa", seed=nx(), rough=0.5, streak=0.8)
    # compass: two legs from a knurled head, needle + lead tips
    hx, hy = 560, 70
    legA, legB = (500, 330), (640, 320)
    legs = strokes(W, H, [([(hx - 4, hy + 10), legA], 7, (0.0, 0.3)), ([(hx + 4, hy + 10), legB], 7, (0.0, 0.3))])
    head = np.maximum(circles(W, H, [(hx, hy + 6, 14)]), shapes(W, H, [[(hx - 5, hy - 40), (hx + 5, hy - 40), (hx + 5, hy - 6), (hx - 5, hy - 6)]], smooth=False))
    allc = np.maximum(legs, head)
    art = over(art, soft_shadow(allc, "#0a2448", blur=5, strength=0.5, dx=8, dy=10))
    art = GP(art, allc, "#c7ccd4", "#8d96a3", seed=nx(), rough=0.5, streak=1.2)
    shine = strokes(W, H, [([(hx - 6, hy + 14), (legA[0] + 3, legA[1] - 20)], 1.6, (0.1, 0.4)), ([(hx + 2, hy + 14), (legB[0] - 4, legB[1] - 20)], 1.6, (0.1, 0.4))])
    art = soft(art, shine, "#ffffff", alpha=0.75, pad=4)
    knurl = lines(W, H, [([(hx - 5, y), (hx + 5, y)], 0.8) for y in range(hy - 38, hy - 8, 3)])
    art = soft(art, knurl, "#5e6672", alpha=0.6, pad=4)
    art = GP(art, strokes(W, H, [([legA, (legA[0] - 2, legA[1] + 18)], 2.2, (0.0, 0.9))]), "#2a2a30", seed=nx(), rough=0.3)
    art = GP(art, strokes(W, H, [([legB, (legB[0] + 1, legB[1] + 16)], 3.0, (0.0, 0.8))]), "#3a3a40", seed=nx(), rough=0.3)
    prev(art, "cb-tools", BLUE)
    save(art, f"{OUT}/tools.webp", max_w=380, quality=82)
