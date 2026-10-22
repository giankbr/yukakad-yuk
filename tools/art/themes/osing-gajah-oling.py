"""Osing Gajah Oling — Banyuwangi: canting-wax batik gajah oling (the curled '?' trunk motif) with crackle, rumah Osing
(tikel balung roof) among coffee rows at the foot of Ijen in morning mist, watercolour coffee branch.
Run: python3 -I osing-gajah-oling.py [part ...]   parts: batik curl scene kopi divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _c2_lib import *

OUT = outdir("osing-gajah-oling")
PARTS = sys.argv[1:] or ["batik", "curl", "scene", "kopi", "divider"]
INK = "#1d1712"      # sogan-black ground
WAX = "#efe2c6"      # wax-resisted cream
MERAH = "#a5322a"    # Osing red coletan
HIJAU = "#5f7a3c"


def oling(cx, cy, s, flip=1, rot=0.0):
    """Gajah oling motif geometry: returns (body polygon, centre path, inner pattern strokes, rawis strokes, dots).
    Unit design: tail at bottom, stem rising, head arching over and spiralling in (a '?')."""
    def T(u, v):
        u *= flip
        cr, sr = math.cos(rot), math.sin(rot)
        return (cx + (u * cr - v * sr) * s, cy + (u * sr + v * cr) * s)
    # centre line in unit coords
    raw = [(-0.05, 0.95), (-0.12, 0.6), (-0.22, 0.25), (-0.28, -0.1), (-0.2, -0.45), (0.05, -0.68), (0.35, -0.7), (0.58, -0.5),
           (0.62, -0.2), (0.45, 0.02), (0.22, 0.02), (0.12, -0.15), (0.2, -0.32), (0.34, -0.3)]
    cl = curve([T(u, v) for u, v in raw], 120)
    n = len(cl)
    def wf(t):
        return s * (0.05 + 0.2 * math.sin(min(1, t * 1.25) * math.pi * 0.9) ** 0.8) * (1 - 0.7 * max(0, t - 0.7) / 0.3)
    L, R = [], []
    for i in range(n):
        a = tangent(cl, i); t = i / (n - 1); ww = wf(t) / 2
        nx_, ny_ = -math.sin(a), math.cos(a)
        L.append((cl[i][0] + nx_ * ww, cl[i][1] + ny_ * ww)); R.append((cl[i][0] - nx_ * ww, cl[i][1] - ny_ * ww))
    body = L + R[::-1]
    inner = []
    for i in range(6, n - 10, 5):
        t = i / (n - 1)
        a = tangent(cl, i); ww = wf(t) / 2 * 0.72
        nx_, ny_ = -math.sin(a), math.cos(a)
        inner.append(([(cl[i][0] + nx_ * ww, cl[i][1] + ny_ * ww), (cl[i][0] - nx_ * ww, cl[i][1] - ny_ * ww)], max(1.2, s * 0.012)))
    # rawis: little flame-like fringe on the outer edge (L side of the arch)
    rawis = []
    for i in range(14, n - 30, 4):
        t = i / (n - 1); a = tangent(cl, i); ww = wf(t) / 2
        side = -1 if flip > 0 else 1
        nx_, ny_ = -math.sin(a) * side, math.cos(a) * side
        bx, by = cl[i][0] + nx_ * (ww + s * 0.025), cl[i][1] + ny_ * (ww + s * 0.025)
        L_ = s * 0.07
        rawis.append(([(bx, by), (bx + nx_ * L_ + math.cos(a) * L_ * 0.5, by + ny_ * L_ + math.sin(a) * L_ * 0.5)], max(1.2, s * 0.013), (0.0, 0.6)))
    dots = []
    for i in range(10, n - 12, 9):
        a = tangent(cl, i); t = i / (n - 1); ww = wf(t) / 2
        side = 1 if flip > 0 else -1
        nx_, ny_ = -math.sin(a) * side, math.cos(a) * side
        dots.append((cl[i][0] + nx_ * (ww + s * 0.06), cl[i][1] + ny_ * (ww + s * 0.06), max(1.4, s * 0.016)))
    return body, cl, inner, rawis, dots


def flower(cx, cy, r, n=6):
    pet = [petal_pts(cx, cy, r, r * 0.42, k / n * math.tau, n=10) for k in range(n)]
    return pet


def sprig(x, y, s, ang):
    stem = curve([(x, y), (x + math.cos(ang) * s * 0.5 + math.cos(ang + 1.5) * s * 0.1, y + math.sin(ang) * s * 0.5 + math.sin(ang + 1.5) * s * 0.1), (x + math.cos(ang) * s, y + math.sin(ang) * s)], 20)
    leaves = []
    for k, t in enumerate([0.35, 0.6, 0.85]):
        px, py = stem[int(t * 19)]
        leaves.append(petal_pts(px, py, s * 0.32, s * 0.12, ang + (0.9 if k % 2 else -0.9), n=10))
    return stem, leaves


def wax_motif(W, H, motifs, lw=2.2, draw_fn=None, wrap=False):
    """Build (wax mask, red mask) from a list of oling() results + extra flowers/sprigs."""
    def render(cv, things):
        pf = paint_white()
        ps = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        for kind, data, w_ in things:
            if kind == "fill":
                cv.c.drawPath(smooth_path(data), pf)
            elif kind == "line":
                ps.setStrokeWidth(w_)
                cv.c.drawPath(smooth_path(data, closed=False) if len(data) > 2 else poly_path(data), ps)
            elif kind == "ring":
                ps.setStrokeWidth(w_)
                cv.c.drawPath(smooth_path(data), ps)
            elif kind == "dot":
                cv.c.drawCircle(data[0], data[1], data[2], pf)
    return render


if "batik" in PARTS or "curl" in PARTS or "divider" in PARTS:
    pass


def offset_poly(cl, wf, extra):
    n = len(cl); L, R = [], []
    for i in range(n):
        a = tangent(cl, i); t = i / (n - 1); ww = wf(t) / 2 + extra
        nx_, ny_ = -math.sin(a), math.cos(a)
        L.append((cl[i][0] + nx_ * ww, cl[i][1] + ny_ * ww)); R.append((cl[i][0] - nx_ * ww, cl[i][1] - ny_ * ww))
    return L + R[::-1]


def side_band(cl, wf, f0, f1, t0=0.0, t1=1.0):
    """Band between fractions f0..f1 of the half-width (signed: + = L side) along the centre line."""
    n = len(cl); A, B = [], []
    for i in range(int(t0 * (n - 1)), int(t1 * (n - 1)) + 1):
        a = tangent(cl, i); t = i / (n - 1); ww = wf(t) / 2
        nx_, ny_ = -math.sin(a), math.cos(a)
        A.append((cl[i][0] + nx_ * ww * f0, cl[i][1] + ny_ * ww * f0)); B.append((cl[i][0] + nx_ * ww * f1, cl[i][1] + ny_ * ww * f1))
    return A + B[::-1]


def oling_layers(W, H, specs, extras, wrap, lw=2.4, flowers_=(), sprigs=()):
    """specs: [(cx, cy, s, flip, rot)] -> (wax mask, red mask). Canting look: double outline, isen-isen interior
    (cecek dot grid + cross hatching), a solid tembokan band, red coletan band, attached rawis fringe."""
    mk = (lambda fn: tile_mask(W, H, fn)) if wrap else (lambda fn: mask_from(W, H, fn))
    def P(w_):
        return skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=w_, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    geo = []
    for (cx, cy, s, flip, rot) in specs:
        body, cl, inner, rawis, dots = oling(cx, cy, s, flip, rot)
        def wf(t, s=s):
            return s * (0.05 + 0.2 * math.sin(min(1, t * 1.25) * math.pi * 0.9) ** 0.8) * (1 - 0.7 * max(0, t - 0.7) / 0.3)
        geo.append((s, flip, body, cl, wf))
    def d_body(cv):
        for s, flip, body, cl, wf in geo:
            cv.c.drawPath(smooth_path(body), paint_white())
    def d_lines(cv):
        for s, flip, body, cl, wf in geo:
            cv.c.drawPath(smooth_path(body), P(lw))
            cv.c.drawPath(smooth_path(offset_poly(cl, wf, lw * 2.2)), P(lw * 0.8))
            sg = 1 if flip > 0 else -1
            # tembokan (solid) band on the inner side, cut through by short bars
            cv.c.drawPath(smooth_path(side_band(cl, wf, -sg * 0.15, -sg * 0.62, 0.05, 0.93)), paint_white())
            # rawis fringe on the outer arch: fine tapered hairs touching the outline
            n = len(cl)
            for i in range(10, n - 26, 2):
                t = i / (n - 1); a = tangent(cl, i); ww = wf(t) / 2 + lw * 2.2
                nx_, ny_ = -math.sin(a) * sg, math.cos(a) * sg
                bx, by = cl[i][0] + nx_ * ww, cl[i][1] + ny_ * ww
                L_ = s * (0.05 + 0.03 * math.sin(i * 1.7))
                path = skia.Path(); path.moveTo(bx, by)
                path.quadTo(bx + nx_ * L_ * 0.6, by + ny_ * L_ * 0.6, bx + nx_ * L_ + math.cos(a) * L_ * 0.6, by + ny_ * L_ + math.sin(a) * L_ * 0.6)
                cv.c.drawPath(path, P(max(1.1, lw * 0.55)))
        for kind, data, w_ in extras:
            if kind == "line":
                cv.c.drawPath(smooth_path(data, closed=False), P(w_))
            elif kind == "ring":
                cv.c.drawPath(smooth_path(data), P(w_))
            elif kind == "dot":
                cv.c.drawCircle(data[0], data[1], data[2], paint_white())
            elif kind == "fill":
                cv.c.drawPath(smooth_path(data), paint_white())
    def d_cuts(cv):
        for s, flip, body, cl, wf in geo:
            sg = 1 if flip > 0 else -1
            n = len(cl)
            for i in range(8, int(n * 0.93), 4):
                t = i / (n - 1); a = tangent(cl, i); ww = wf(t) / 2
                nx_, ny_ = -math.sin(a) * -sg, math.cos(a) * -sg
                cv.c.drawLine(cl[i][0] + nx_ * ww * 0.2, cl[i][1] + ny_ * ww * 0.2, cl[i][0] + nx_ * ww * 0.58, cl[i][1] + ny_ * ww * 0.58, P(max(1.0, lw * 0.5)))
    def d_red(cv):
        for s, flip, body, cl, wf in geo:
            sg = 1 if flip > 0 else -1
            cv.c.drawPath(smooth_path(side_band(cl, wf, sg * 0.12, sg * 0.5, 0.08, 0.6)), paint_white())
            hx, hy = cl[int(len(cl) * 0.9)]
            cv.c.drawCircle(hx, hy, s * 0.045, paint_white())
    B = mk(d_body); Lm = mk(d_lines); Cu = mk(d_cuts); Rd = mk(d_red)
    inner = np.clip((gaussian_filter(B, 1.6) - 0.75) * 6, 0, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gx, gy = (xx % 8) - 4, (yy % 8) - 4
    cecek = np.clip(1.9 - np.hypot(gx, gy), 0, 1)
    wax = np.maximum(Lm, cecek * inner)
    wax = np.clip(wax - Cu * inner, 0, 1)
    red = np.clip(Rd * inner, 0, 1)
    wax = np.maximum(wax, red)
    return wax, red


def flower5(x, y, r, lw=2.0):
    items = []
    for k in range(5):
        a = k / 5 * math.tau - math.pi / 2
        items.append(("ring", petal_pts(x + math.cos(a) * r * 0.15, y + math.sin(a) * r * 0.15, r, r * 0.55, a, n=12), lw))
        items.append(("line", [(x + math.cos(a) * r * 0.3, y + math.sin(a) * r * 0.3), (x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.75)], lw * 0.6))
    items.append(("dot", (x, y, r * 0.22), 0))
    return items


def leafy(x, y, s_, a, lw=2.0):
    st, lv = sprig(x, y, s_, a)
    items = [("line", st, lw)]
    for l_ in lv:
        items.append(("ring", l_, lw * 0.9))
        m0 = l_[0]; m1 = l_[len(l_) // 2]
        items.append(("line", [m0, ((m0[0] + m1[0]) / 2, (m0[1] + m1[1]) / 2)], lw * 0.5))
    return items


def ukel(x, y, r, lw=1.6):
    return [("line", spiral_pts(x, y, r, r * 0.15, 0, 1.4, 30, 1), lw)]


if "batik" in PARTS:
    S = 400
    nx = Seq(40100); rnd = random.Random(3)
    specs = [(130, 210, 190, 1, -0.25), (330, 400 - 10, 190, -1, 0.3)]
    extras = []
    for (x, y, r) in [(300, 96, 24), (56, 372, 20), (236, 296, 15), (384, 222, 13)]:
        extras += flower5(x, y, r)
    for (x, y, s_, a) in [(250, 36, 84, 0.4), (16, 116, 74, 1.2), (176, 362, 70, -0.6), (352, 300, 60, -2.2)]:
        extras += leafy(x, y, s_, a)
    for (x, y) in [(40, 30), (200, 180), (330, 160), (110, 300), (280, 380)]:
        extras += ukel(x, y, 9)
    for _ in range(70):
        extras.append(("dot", (rnd.uniform(0, S), rnd.uniform(0, S), rnd.uniform(1.0, 1.6)), 0))
    wax, red = oling_layers(S, S, specs, extras, wrap=True)
    art = batik(S, S, wax, INK, WAX, seed=nx(), layers=[(red, MERAH)], tile=True, crack=0.6)
    preview(art, "og-batik")
    save_full(art, f"{OUT}/batik.webp", size=(300, 300), quality=78)
    clear()

if "curl" in PARTS:
    # single motif (transparent around) for the cover: wax-cream + red on a torn dark cloth patch
    W, H = 560, 640
    nx = Seq(40200)
    specs = [(280, 330, 300, 1, -0.12)]
    extras = []
    for (x, y, r) in [(110, 120, 30), (462, 566, 24), (470, 150, 18)]:
        extras += flower5(x, y, r, 2.6)
    for (x, y, s_, a) in [(84, 530, 130, -1.0), (476, 330, 120, 1.6)]:
        extras += leafy(x, y, s_, a, 2.6)
    for (x, y) in [(200, 70), (520, 450), (60, 300)]:
        extras += ukel(x, y, 12, 2.0)
    wax, red = oling_layers(W, H, specs, extras, wrap=False, lw=3.0)
    cloth = batik(W, H, wax, INK, WAX, seed=nx(), layers=[(red, MERAH)], tile=False, crack=0.6)
    # keep only the waxed parts (motif alone, over any dark ground)
    a = np.clip(gaussian_filter(wax, 0.6) * 1.2, 0, 1)
    art = rgba(cloth[..., :3], a)
    preview(art, "og-curl", bg=INK)
    save(art, f"{OUT}/curl.webp", max_w=300, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 600, 150
    nx = Seq(40300)
    specs = [(196, 82, 110, -1, 1.57 + 0.15), (404, 82, 110, 1, -1.57 - 0.15)]
    extras = flower5(300, 75, 20, 2.4)
    extras += [("dot", (300 + k * 30, 75, 3), 0) for k in (-7, -6, 6, 7)]
    wax, red = oling_layers(W, H, specs, extras, wrap=False)
    cloth = batik(W, H, wax, INK, WAX, seed=nx(), layers=[(red, MERAH)], crack=0.5)
    art = rgba(cloth[..., :3], np.clip(gaussian_filter(wax, 0.6) * 1.2, 0, 1))
    preview(art, "og-divider", bg=INK)
    save(art, f"{OUT}/divider.webp", max_w=300, quality=86)
    clear()

if "scene" in PARTS:
    # watercolour: Ijen massif in morning mist, coffee rows under shade trees, a rumah Osing (tikel balung roof)
    W, H = 820, 540
    nx = Seq(40400); rnd = random.Random(21)
    art = blank(W, H)
    # sky wash (fades out at the top)
    sky = np.clip(1 - np.linspace(0, 1, H)[:, None] * 0 - 0, 0, 1) * np.ones((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    skym = np.clip((yy - 10) / 180, 0, 1) * np.clip(1 - (yy - 330) / 80, 0, 1)
    art = G(art, skym, "#f3d8b8", "#d9e2e2", seed=nx(), density=0.55, edge=0.05, bloom=0.4, rough=12, feather=12)
    # sun haze
    art = G(art, circles(W, H, [(250, 150, 60)]), "#f7e2b4", seed=nx(), density=0.6, edge=0.1, bloom=0.2, rough=8, feather=14)
    # Ijen massif: broad flat-topped volcano with a notch
    ridge = [(-20, 330), (60, 300), (160, 250), (250, 190), (330, 150), (380, 140), (430, 146), (450, 140), (500, 150), (570, 190), (650, 240), (740, 270), (840, 290), (840, 400), (-20, 400)]
    art = G(art, poly(W, H, deform(ridge, rnd, 1, 0.01)), "#8fa1b3", "#a6aebd", seed=nx(), density=0.62, edge=0.55, bloom=0.3, rough=5)
    # gullies on the slope
    gul = strokes(W, H, [(curve([(380 + k * 26 + rnd.uniform(-8, 8), 152 + abs(k) * 4), (372 + k * 40 + rnd.uniform(-10, 10), 210), (360 + k * 56, 270 + rnd.uniform(0, 30))], 20), 2.2 + rnd.uniform(0, 2), (0.3, 0.7)) for k in range(-4, 5) if k != 0])
    art = G(art, gul, "#6c7f93", seed=nx(), density=0.22, edge=0.25, bloom=0, rough=3, feather=1.6)
    shadow_side = poly(W, H, [(430, 146), (500, 150), (570, 190), (650, 240), (740, 270), (840, 290), (840, 360), (470, 360)]) 
    art = G(art, shadow_side, "#6d7f99", seed=nx(), density=0.32, edge=0.2, bloom=0.5, rough=10, feather=6)
    crater = poly(W, H, deform([(340, 148), (380, 136), (430, 142), (450, 138), (490, 150), (420, 158)], rnd, 1, 0.02))
    art = G(art, crater, "#5f6f86", seed=nx(), density=0.4, edge=0.4, bloom=0, rough=2)
    # second ridge (closer, bluer green)
    r2 = [(-20, 350), (90, 320), (200, 300), (300, 310), (420, 290), (540, 300), (660, 280), (840, 300), (840, 420), (-20, 420)]
    art = G(art, poly(W, H, deform(r2, rnd, 1, 0.015)), "#7f9c8e", "#93a99a", seed=nx(), density=0.6, edge=0.5, bloom=0.35, rough=6)
    # mist band (lift pigment)
    mist = np.clip(np.exp(-((yy - 320) / 26) ** 2) * (0.6 + 0.4 * fbm(W, H, nx(), 90, 3)), 0, 1)
    art[..., 3] *= 1 - mist * 0.75
    art = G(art, mist * 0.7, "#f4f1ea", seed=nx(), density=0.5, edge=0, bloom=0.3, rough=10, feather=8)
    # near hill with coffee rows
    hill = [(-20, 400), (120, 372), (300, 360), (480, 368), (640, 356), (840, 376), (840, 560), (-20, 560)]
    hm = poly(W, H, deform(hill, rnd, 1, 0.01))
    art = G(art, hm, "#9bb06a", "#7d9a55", seed=nx(), density=0.7, edge=0.45, bloom=0.35, rough=6)
    hx, hy = 590, 448
    sil = poly(W, H, [(hx - 126, hy - 58), (hx - 70, hy - 100), (hx - 26, hy - 174), (hx + 26, hy - 174), (hx + 70, hy - 100), (hx + 126, hy - 58), (hx + 94, hy - 58), (hx + 94, hy + 2), (hx - 94, hy + 2), (hx - 94, hy - 58)], smooth=False)
    rw = blank(W, H)
    for row in range(7):
        y0 = 390 + row * 21 + row * row * 1.6
        r = 7 + row * 2.6
        top = [(x, y0 + 5 * math.sin(x / 140 + row) - r * (0.15 + 1.0 * abs(math.sin(x / (r * 0.85) + row * 1.3)) ** 0.6)) for x in range(-20, W + 21, 3)]
        band = top + [(W + 20, y0 + r * 0.7), (-20, y0 + r * 0.7)]
        bm = poly(W, H, band, smooth=False)
        rw = G(rw, bm, "#55763d", "#365a2f", seed=nx(), density=0.66, edge=0.7, bloom=0.35, rough=3.5)
        dabs = shapes(W, H, [deform(ellipse_pts(x + rnd.uniform(-3, 3), y0 - r * 0.45 + rnd.uniform(-2, 2), r * 0.5, r * 0.28, 8, rnd.uniform(-0.4, 0.4)), rnd, 1, 0.15) for x in range(0, W, int(r * 1.3))]) * bm
        rw = G(rw, dabs, "#86a463", seed=nx(), density=0.4, edge=0.4, bloom=0.2, rough=2)
        rw = G(rw, np.clip(bm - np.roll(bm, -5, 0), 0, 1), "#24401f", seed=nx(), density=0.5, edge=0.3, bloom=0, rough=2)
    art = glaze(art, knockout(rw, sil, amount=0.97, grow=1.0))
    # shade trees (dadap/lamtoro): thin trunks, flat airy canopies
    for (x, y, h_) in [(110, 410, 150), (300, 400, 120), (770, 410, 160)]:
        tr = strokes(W, H, [(curve([(x, y), (x + 4, y - h_ * 0.5), (x - 2, y - h_)], 16), 4, (0.0, 0.4))])
        art = G(art, tr, "#5b4a3a", seed=nx(), density=0.75, edge=0.4, bloom=0, rough=1.5)
        cn = shapes(W, H, [deform(ellipse_pts(x + rnd.uniform(-30, 30), y - h_ + tier * 22 - rnd.uniform(-6, 6), rnd.uniform(18, 34) + tier * 8, rnd.uniform(7, 11), 10), rnd, 2, 0.25) for tier in range(3) for _ in range(3)])
        art = G(art, cn, "#6f8f4c", "#4e6e3a", seed=nx(), density=0.6, edge=0.6, bloom=0.4, rough=5, holes=0.15)
    # rumah Osing (tikel balung): steep central roof + two lower side aprons + front emperan, plank walls
    walls = [(hx - 92, hy), (hx - 92, hy - 64), (hx + 92, hy - 64), (hx + 92, hy)]
    art = G(art, poly(W, H, walls, smooth=False), "#c99c6a", "#b78557", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.6)
    planks = strokes(W, H, [([(hx - 92 + k * 9, hy - 62), (hx - 92 + k * 9, hy - 2)], 1.0, None) for k in range(1, 21)])
    art = G(art, planks, "#7a5534", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.6)
    door = poly(W, H, [(hx - 16, hy), (hx - 16, hy - 48), (hx + 16, hy - 48), (hx + 16, hy)], smooth=False)
    art = G(art, door, "#5a3a22", seed=nx(), density=0.85, edge=0.4, bloom=0, rough=1)
    for wx_ in (hx - 58, hx + 44):
        art = G(art, poly(W, H, [(wx_, hy - 22), (wx_, hy - 46), (wx_ + 16, hy - 46), (wx_ + 16, hy - 22)], smooth=False), "#3d2a1c", seed=nx(), density=0.8, edge=0.3, bloom=0, rough=0.8)
    roof_main = [(hx - 70, hy - 98), (hx - 26, hy - 172), (hx + 26, hy - 172), (hx + 70, hy - 98)]
    roof_side_l = [(hx - 70, hy - 98), (hx - 120, hy - 60), (hx - 60, hy - 60)]
    roof_side_r = [(hx + 70, hy - 98), (hx + 120, hy - 60), (hx + 60, hy - 60)]
    roof_front = [(hx - 124, hy - 58), (hx - 70, hy - 100), (hx + 70, hy - 100), (hx + 124, hy - 58)]
    for sd_ in (roof_side_l, roof_side_r):
        art = G(art, poly(W, H, sd_, smooth=False), "#94452f", seed=nx(), density=0.8, edge=0.5, bloom=0.2, rough=1.4)
    art = G(art, poly(W, H, roof_front, smooth=False), "#a5523a", "#8c4330", seed=nx(), density=0.8, edge=0.55, bloom=0.25, rough=1.6)
    art = G(art, poly(W, H, roof_main, smooth=False), "#b55c3e", "#94452f", seed=nx(), density=0.85, edge=0.55, bloom=0.25, rough=1.6)
    tiles = np.maximum(strokes(W, H, [([(hx - 120 + k * 8, hy - 58), (hx - 66 + k * 5.7, hy - 98)], 1.0, None) for k in range(31)]) * poly(W, H, roof_front, smooth=False),
                       strokes(W, H, [([(hx - 70 + k * 7, hy - 98), (hx - 26 + k * 2.6, hy - 172)], 1.0, None) for k in range(21)]) * poly(W, H, roof_main, smooth=False))
    art = G(art, tiles, "#5e2a1c", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.5)
    art = G(art, strokes(W, H, [([(hx - 26, hy - 172), (hx + 26, hy - 172)], 4, None), ([(hx - 124, hy - 58), (hx + 124, hy - 58)], 3, None)]), "#4a2418", seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.6)
    # banana + foreground grasses
    for (x, y, a, L) in [(470, 452, -2.2, 70), (480, 452, -1.3, 64), (700, 452, -1.9, 80), (712, 450, -0.9, 60)]:
        lf = poly(W, H, petal_pts(x, y, L, 13, a, n=12))
        art = G(art, lf, "#7a9a4c", "#5b7b3b", seed=nx(), density=0.62, edge=0.6, bloom=0.3, rough=3)
    gr = strokes(W, H, [(curve([(x, 540), (x + rnd.uniform(-6, 6), 510), (x + rnd.uniform(-14, 14), 488 - rnd.uniform(0, 26))], 14), 2.4, (0.0, 0.8)) for x in range(0, W, 9)])
    art = G(art, gr, "#5e7a3a", "#3f5a2c", seed=nx(), density=0.55, edge=0.3, bloom=0, rough=1.2)
    # soften the frame: fade the sides and the bottom edge
    fade = np.clip(xx / 60, 0, 1) * np.clip((W - xx) / 60, 0, 1) * np.clip((H - yy) / 40, 0, 1)
    art[..., 3] *= fade
    preview(art, "og-scene", tone="#f4ecdc")
    save(art, f"{OUT}/scene.webp", max_w=720, quality=80)
    clear()

if "kopi" in PARTS:
    # coffee branch: glossy leaves in pairs, clusters of red cherries + a few white blossoms
    W, H = 520, 360
    nx = Seq(40500); rnd = random.Random(31)
    art = blank(W, H)
    stem = curve([(20, 300), (140, 250), (280, 190), (420, 150), (500, 140)], 60)
    art = G(art, strokes(W, H, [(stem, 6, (0.0, 0.7))]), "#6b5034", seed=nx(), density=0.8, edge=0.4, bloom=0, rough=1.5)
    for k, i in enumerate(range(8, 56, 9)):
        x, y = stem[i]; a = tangent(stem, i)
        for sg in (-1, 1):
            L = 120 - k * 10
            aa = a + sg * 0.9
            pts = petal_pts(x, y, L, L * 0.27, aa, n=14, cup=0.15 * sg)
            m = poly(W, H, deform(pts, rnd, 1, 0.03))
            art = G(art, m, "#3f6b3a", "#2c5130", seed=nx(), density=0.75, edge=0.6, bloom=0.3, rough=3)
            hl = poly(W, H, petal_pts(x, y, L * 0.9, L * 0.12, aa - sg * 0.06, n=12)) * m
            art = G(art, hl, "#8fb07a", seed=nx(), density=0.35, edge=0.1, bloom=0.3, rough=2)
            art = G(art, strokes(W, H, [([(x, y), (x + math.cos(aa) * L * 0.9, y + math.sin(aa) * L * 0.9)], 1.4, None)]), "#24402a", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.6, feather=0.6)
        # cherries at the node
        cl_ = [(x + rnd.uniform(-14, 14), y + rnd.uniform(-8, 14), rnd.uniform(9, 12)) for _ in range(5)]
        for (cx, cy, r) in cl_:
            col = rnd.choice(["#b3262a", "#c8352c", "#8e1e24", "#d6603a"])
            art = G(art, circles(W, H, [(cx, cy, r)]), col, mix(col, "#3a0d0d", 0.4), seed=nx(), density=0.85, edge=0.6, bloom=0.15, rough=1.2, pad=10)
            art = G(art, circles(W, H, [(cx - r * 0.35, cy - r * 0.35, r * 0.3)]), "#f6d7c4", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, pad=6)
    for (x, y) in [(300, 130), (450, 110)]:
        for j in range(5):
            a = j / 5 * math.tau
            art = G(art, poly(W, H, petal_pts(x, y, 16, 6, a, n=10)), "#fbf6ea", "#e6ddcc", seed=nx(), density=0.85, edge=0.6, bloom=0, rough=1.2, pad=8)
        art = G(art, circles(W, H, [(x, y, 3)]), "#d9b45a", seed=nx(), density=0.9, edge=0.2, rough=0.5, pad=6)
    preview(art, "og-kopi", tone="#f4ecdc")
    save(art, f"{OUT}/kopi.webp", max_w=320, quality=82)
    clear()

if "divink" in PARTS or "divider" in PARTS:
    # sogan-ink version of the divider for the cream rooms: the cream wax lines become dark sogan ink, red stays red
    from PIL import Image as _I
    src = np.asarray(_I.open(f"{OUT}/divider.webp").convert("RGBA")).astype(np.float32) / 255
    rgb, al = src[..., :3], src[..., 3:]
    red = np.clip((rgb[..., 0] - rgb[..., 2]) * 3.0 - 0.3, 0, 1)[..., None]
    lum = rgb.mean(-1, keepdims=True)
    ink = np.array([0.17, 0.12, 0.08]) * (0.75 + 0.5 * (1 - lum))
    out = rgb * red + ink * (1 - red)
    _I.fromarray((np.concatenate([out, al], -1) * 255).clip(0, 255).astype(np.uint8), "RGBA").save(f"{OUT}/divider-ink.webp", quality=86, method=6)
