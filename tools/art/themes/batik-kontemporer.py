"""Batik Kontemporer — contemporary hand-drawn batik in unexpected colours: an oversized parang of tangerine blades on
cobalt with mint lereng stripes, a giant kawung medallion, a mega mendung cloud graded cobalt-to-mint, and a cream isen
(cecek + truntum) cloth tile. Every piece is dyed cloth: wax-resist lines with canting blobs, uneven dye and crackle.
Run: python3 -I batik-kontemporer.py [part ...]  parts: parang kawung row mega isen
Assets -> public/themes/art/batik-kontemporer/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c5_lib import *
from scipy.ndimage import distance_transform_edt

OUT = outdir("batik-kontemporer")
PARTS = sys.argv[1:] or ["parang", "kawung", "row", "mega"]
COBALT, COBALT2 = "#2340b8", "#1c349e"
NAVY = "#121a3a"
TANG, TANG2 = "#f2762e", "#ee6624"
MINT, MINT2 = "#9fe3c8", "#8cd9bb"
CREAM, CREAM2 = "#f6f1e6", "#efe7d6"


def rot_draw(w, h, ang, cx, cy, fn):
    def draw(cv):
        cv.c.save(); cv.c.translate(cx, cy); cv.c.rotate(ang); cv.c.translate(-cx, -cy)
        fn(cv)
        cv.c.restore()
    return mask_from(w, h, draw)


def P(**k):
    return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, **k)


if "parang" in PARTS:
    # seamless tile: with the bands at 45deg and B == L == W / sqrt(2) the pattern repeats every W px on both axes
    T = 640
    W = H = T + 120
    rng = random.Random(61)
    B = T / math.sqrt(2)   # band width (across)
    L = B                  # repeat along the band
    ang = -45
    big = int(math.hypot(W, H)) + 2 * B
    cx, cy = W / 2, H / 2

    def bands(fn):
        def draw(cv):
            for bi in range(-6, 7):
                for li in range(-6, 7):
                    ox = cx + li * L - B * 0.0
                    oy = cy + bi * B
                    fn(cv, ox + (bi % 2) * 0, oy)
        return rot_draw(W, H, ang, cx, cy, draw)

    def blade_path(ox, oy):
        p = skia.Path()
        p.moveTo(ox - L * 0.48, oy + B * 0.12)
        p.cubicTo(ox - L * 0.05, oy + B * 0.06, ox + L * 0.12, oy + B * 0.5, ox - L * 0.06, oy + B * 0.7)
        p.cubicTo(ox - L * 0.2, oy + B * 0.86, ox + L * 0.2, oy + B * 0.95, ox + L * 0.52, oy + B * 0.88)
        p.cubicTo(ox + L * 0.2, oy + B * 0.8, ox + L * 0.26, oy + B * 0.52, ox + L * 0.1, oy + B * 0.34)
        p.cubicTo(ox - L * 0.02, oy + B * 0.2, ox - L * 0.2, oy + B * 0.12, ox - L * 0.48, oy + B * 0.12)
        p.close()
        return p

    blades = bands(lambda cv, ox, oy: cv.c.drawPath(blade_path(ox, oy), P()))
    inner = bands(lambda cv, ox, oy: cv.c.drawPath(blade_path(ox, oy), P(Style=skia.Paint.kStroke_Style, StrokeWidth=7)))
    # mint lereng stripe between the bands + its two wax edge lines
    stripe = bands(lambda cv, ox, oy: cv.c.drawRect(skia.Rect(ox - L / 2, oy - B * 0.06, ox + L / 2, oy + B * 0.06), P()))
    edge = bands(lambda cv, ox, oy: [cv.c.drawLine(ox - L / 2, oy + s_ * B * 0.06, ox + L / 2, oy + s_ * B * 0.06, P(Style=skia.Paint.kStroke_Style, StrokeWidth=5)) for s_ in (-1, 1)])
    # mlinjon: tangerine lozenges on the stripe + cecek dots along it
    mlinjon = bands(lambda cv, ox, oy: cv.c.drawPath(poly_path([(ox - 26, oy), (ox, oy - 15), (ox + 26, oy), (ox, oy + 15)]), P()))
    dots = bands(lambda cv, ox, oy: [cv.c.drawCircle(ox + d, oy + B * 0.17, 5, P()) for d in (-90, -54, 54, 90)])
    # wax line that splits each blade (the "uceng" vein)
    def vein(cv, ox, oy):
        p = skia.Path()
        p.moveTo(ox - L * 0.3, oy + B * 0.15)
        p.cubicTo(ox + L * 0.02, oy + B * 0.2, ox + L * 0.12, oy + B * 0.5, ox + 0, oy + B * 0.66)
        p.cubicTo(ox - L * 0.06, oy + B * 0.8, ox + L * 0.12, oy + B * 0.86, ox + L * 0.34, oy + B * 0.85)
        cv.c.drawPath(p, P(Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap))
    veins = bands(vein)
    field = np.ones((H, W), np.float32)
    wax = np.clip(inner + edge + veins, 0, 1)
    art = batik(W, H, [(field, COBALT, COBALT2), (stripe, MINT, MINT2), (blades, TANG, TANG2), (mlinjon, TANG, TANG2),
                       (np.clip(wax * 1.0, 0, 1), CREAM, CREAM2), (dots, CREAM, CREAM2)], seed=611, crack=(0.6, 36), crack_col=NAVY)
    # blend the (non-periodic) dye/crackle noise across the seams with a half-offset copy; the motif itself is periodic
    art = np.ascontiguousarray(art[60:60 + T, 60:60 + T])
    yy, xx = np.mgrid[0:T, 0:T].astype(np.float32)
    k = np.clip(np.minimum(np.minimum(xx, T - 1 - xx), np.minimum(yy, T - 1 - yy)) / 90, 0, 1)[..., None]
    sh = np.roll(np.roll(art, T // 2, 0), T // 2, 1)
    art = art * k + sh * (1 - k)
    preview(art, "bk-parang")
    save_rgb(art, f"{OUT}/parang.webp", size=(400, 400), quality=80)
    clear()

if "kawung" in PARTS:
    W = H = 640
    cx = cy = W / 2
    R = 300
    disc = circles(W, H, [(cx, cy, R)])
    ring = np.clip(circles(W, H, [(cx, cy, R - 10)]) - circles(W, H, [(cx, cy, R - 18)]), 0, 1)
    pet, out_l, seeds = [], [], []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        px, py = cx + math.cos(a) * 140, cy + math.sin(a) * 140
        pet.append(ellipse_pts(px, py, 116, 78, 40, a))
        out_l.append((px, py, ellipse_pts(px, py, 116, 78, 40, a)))
        seeds.append((cx + math.cos(a) * 150, cy + math.sin(a) * 150, 17))
    petals = shapes(W, H, pet) * disc
    def outl(cv):
        for px, py, pts in out_l:
            cv.c.drawPath(smooth_path(pts), P(Style=skia.Paint.kStroke_Style, StrokeWidth=8))
        for px, py, pts in out_l:
            inner = [((x - px) * 0.72 + px, (y - py) * 0.66 + py) for x, y in pts]
            cv.c.drawPath(smooth_path(inner), P(Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    lines = mask_from(W, H, outl) * disc
    seedm = circles(W, H, seeds)
    centre = shapes(W, H, [[(cx, cy - 34), (cx + 34, cy), (cx, cy + 34), (cx - 34, cy)]], smooth=False)
    cecek = []
    for k in range(4):
        a = k * math.pi / 2
        for t in (200, 232, 262):
            cecek.append((cx + math.cos(a) * t, cy + math.sin(a) * t, 6))
    cec = circles(W, H, cecek)
    art = batik(W, H, [(disc, MINT, MINT2), (petals, TANG, TANG2), (seedm, COBALT, COBALT2), (centre, COBALT, COBALT2),
                       (np.clip(lines + ring + cec, 0, 1), CREAM, CREAM2)], seed=621, crack=(0.6, 30), crack_col="#1a2a6e")
    art[..., 3] *= np.clip(gaussian_filter(disc, 0.8) * 1.2, 0, 1)
    preview(art, "bk-kawung")
    save(art, f"{OUT}/kawung.webp", max_w=320, quality=82)
    clear()

if "row" in PARTS:
    # divider: three small kawung on a thin cobalt line, cut as a cloth strip
    W, H = 640, 150
    cy = 75
    strip = shapes(W, H, [[(0, cy - 8), (W, cy - 8), (W, cy + 8), (0, cy + 8)]], smooth=False)
    pet, lines = [], []
    for cx in (W / 2 - 150, W / 2, W / 2 + 150):
        for k in range(4):
            a = math.pi / 4 + k * math.pi / 2
            pet.append(ellipse_pts(cx + math.cos(a) * 27, cy + math.sin(a) * 27, 25, 16, 30, a))
    pm = shapes(W, H, pet)
    def outl(cv):
        for pts in pet:
            cv.c.drawPath(smooth_path(pts), P(Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    lm = mask_from(W, H, outl)
    dots = circles(W, H, [(x, cy, 4.5) for x in list(range(40, 200, 26)) + list(range(W - 40, W - 200, -26))])
    art = batik(W, H, [(strip, COBALT, COBALT2), (pm, TANG, TANG2), (np.clip(lm + dots, 0, 1), CREAM, CREAM2)], seed=631, crack=(0.5, 18), crack_col=NAVY, edge_bleed=0.8)
    preview(art, "bk-row")
    save(art, f"{OUT}/row.webp", max_w=320, quality=84)
    clear()

if "mega" in PARTS:
    W, H = 820, 520
    rng = random.Random(64)
    # a cloud built from lobes, then graded in concentric bands (the classic 7-step gradasi)
    lobes = [(260, 300, 120), (390, 240, 140), (540, 280, 120), (650, 330, 90), (170, 360, 80), (450, 350, 120), (320, 380, 100)]
    cloud = circles(W, H, lobes)
    tail = strokes(W, H, [(curve([(640, 360), (720, 380), (760, 330), (720, 290), (690, 316)], 40), 40, (0.0, 0.5)),
                          (curve([(190, 400), (110, 420), (70, 370), (110, 330), (140, 352)], 40), 40, (0.0, 0.5))])
    cloud = np.clip(cloud + tail, 0, 1)
    cloud = (gaussian_filter(cloud, 6) > 0.5).astype(np.float32)
    d = distance_transform_edt(cloud > 0.5).astype(np.float32)
    steps = [COBALT, "#2e55c4", "#3f72cf", "#5a95d6", "#78b6d6", MINT, CREAM]
    band = 18
    layers = []
    wax = np.zeros_like(cloud)
    for i, col in enumerate(steps):
        m = (d > i * band).astype(np.float32)
        layers.append((gaussian_filter(m, 0.8), col, col))
        wax = np.maximum(wax, np.clip(1 - np.abs(d - i * band - band + 2.5) / 2.6, 0, 1) * (d > 4))
    layers.append((wax * 0.0, CREAM, CREAM2))
    art = batik(W, H, layers, seed=641, crack=(0.55, 30), crack_col=NAVY, edge_bleed=1.0)
    # thin navy outline (isen garis) between steps
    art = OV(art, wax * (d < band * 6), lambda m: col_arr(m, NAVY, m * 0.55), pad=4)
    preview(art, "bk-mega")
    save(art, f"{OUT}/mega.webp", max_w=420, quality=82)
    clear()

if "isen" in PARTS:
    # seamless cream cloth tile with a faint truntum star + cecek scatter (wax-resist ghost on undyed cotton)
    n = 360
    rng = random.Random(65)
    pts = []
    for gy in range(3):
        for gx in range(3):
            x = (gx + 0.5 + (0.5 if gy % 2 else 0)) * n / 3 % n
            y = (gy + 0.5) * n / 3
            pts.append((x, y))
    def draw(cv):
        for x, y in pts:
            for ox in (-n, 0, n):
                for oy in (-n, 0, n):
                    for k in range(8):
                        a = k * math.pi / 4
                        cv.c.drawCircle(x + ox + math.cos(a) * 13, y + oy + math.sin(a) * 13, 5, P())
                    cv.c.drawCircle(x + ox, y + oy, 4, P())
                    for k in range(6):
                        a = k * math.pi / 3 + 0.3
                        cv.c.drawCircle(x + ox + math.cos(a) * 34, y + oy + math.sin(a) * 34, 2.2, P())
    stars = mask_from(n, n, draw)
    field = np.ones((n, n), np.float32)
    art = batik(n, n, [(field, "#ece4d3", "#e6dcc8"), (stars, CREAM, CREAM2)], seed=651, crack=(0.35, 20), crack_col="#b9ab8f", cloth_amt=1.4, edge_bleed=0.6)
    save_rgb(art, f"{OUT}/isen.webp", quality=72)
    clear()
