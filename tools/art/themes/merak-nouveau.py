"""Merak Nouveau — art nouveau peacock: train feathers with iridescent eye spots (indigo heart, turquoise, foil-bronze
ring, emerald, golden fringe) and fine wispy barbs, a fan of feathers, a gilded whiplash arch frame with coup-de-fouet
scrolls, a whiplash divider, a single eye medallion, and dark teal silk / cream paper tiles.
Run: python3 -I merak-nouveau.py [part ...]   parts: feather eye fan frame divider corner paper silk"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e4_lib import *

OUT = outdir("merak-nouveau")
PARTS = sys.argv[1:] or ["feather", "eye", "fan", "frame", "divider", "corner", "paper", "silk"]
TEAL_BG = "#0f3436"
GOLD = "#c9a24a"


def spiral(cx, cy, r0, r1, a0, turns, d=1, n=40):
    return [(cx + math.cos(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t), cy + math.sin(a0 + d * t * turns * math.tau) * (r0 + (r1 - r0) * t)) for t in np.linspace(0, 1, n)]


def local_uv(W, H, ex, ey, ang):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = xx - ex, yy - ey
    s_ = dx * math.cos(ang) + dy * math.sin(ang)        # along the shaft (toward the tip)
    n_ = -dx * math.sin(ang) + dy * math.cos(ang)       # across
    return s_, n_


def chevrons(s_, n_, period, lean=0.85, sharp=8, seed=1):
    """Barb lines leaving the shaft and leaning toward the tip (V pattern), as a 0..1 line field."""
    W = s_.shape[1]; H = s_.shape[0]
    wob = (fbm(W, H, seed, 26, 2) - 0.5) * period * 1.2
    u = (s_ - np.abs(n_) * lean + wob) / period
    return np.clip(1 - np.abs((u % 1.0) - 0.5) * 2, 0, 1) ** sharp


def eye_spot(art, W, H, ex, ey, rx, ang, nx, rng, fringe=True):
    """Peacock eye centred at (ex, ey); ang = direction from the shaft base toward the tip (radians)."""
    ry = rx * 1.22
    rot = math.degrees(ang + math.pi / 2)
    back = (-math.cos(ang), -math.sin(ang))
    s_, n_ = local_uv(W, H, ex, ey, ang)
    def E(k, shift=0.0, sq=1.0):
        return (ex + back[0] * rx * shift, ey + back[1] * rx * shift, rx * k * sq, ry * k, rot)
    if fringe:
        # loose golden-green vane around the eye: ragged soft wash + wispy V barbs fading outward
        r_ = np.sqrt((n_ / (rx * 1.5)) ** 2 + ((s_ + rx * 0.05) / (ry * 1.42)) ** 2)
        rag = (fbm(W, H, nx(), 14, 3) - 0.5) * 0.35
        vane = np.clip((1 - r_ + rag) * 4, 0, 1)
        art = G(art, vane, "#8e8a36", "#5e7d3c", seed=nx(), density=0.38, edge=0.15, bloom=0.5, gran=0.35, rough=4, feather=2.5)
        ch = chevrons(s_, n_, rx * 0.075, 0.9, 6, nx()) * vane * np.clip(r_ * 1.4 - 0.2, 0, 1)
        art = G(art, ch, "#b39a3c", "#7f9a3e", seed=nx(), density=0.85, edge=0.05, bloom=0, gran=0.1, rough=0.4, feather=0.35)
    e0 = ellipses(W, H, [E(1.0, 0.0, 0.96)])
    art = G(art, e0, "#a28f34", "#6f8a36", seed=nx(), density=0.78, edge=0.55, bloom=0.4, gran=0.35, rough=3.0, feather=1.4)
    e1 = ellipses(W, H, [E(0.83, 0.07, 0.95)])
    art = G(art, e1, "#3f8a44", "#2c7a58", seed=nx(), density=0.86, edge=0.65, bloom=0.35, gran=0.25, rough=2.2, feather=1.0)
    e2 = ellipses(W, H, [E(0.64, 0.17, 0.93)])
    art = FO(art, e2, "#b07a34", seed=nx(), emboss=0.4, sparkle=0.12)
    art = G(art, e2, "#a8662c", "#7e4e22", seed=nx(), density=0.4, edge=0.5, bloom=0.3, rough=1.6, feather=0.7)
    e3 = ellipses(W, H, [E(0.555, 0.2, 0.92)])
    art = G(art, e3, "#2fb0a6", "#1e8aa8", seed=nx(), density=0.92, edge=0.55, bloom=0.4, gran=0.2, rough=1.6, feather=0.7)
    hcx, hcy = ex + back[0] * rx * 0.34, ey + back[1] * rx * 0.34
    heart = ellipses(W, H, [(hcx, hcy, rx * 0.34, ry * 0.36, rot)])
    notch = circles(W, H, [(hcx + back[0] * ry * 0.42, hcy + back[1] * ry * 0.42, rx * 0.12)])
    heart = np.clip(heart - gaussian_filter(notch, 1.5) * 1.3, 0, 1)
    art = G(art, heart, "#24388e", "#1a2a6c", seed=nx(), density=0.95, edge=0.75, bloom=0.3, gran=0.25, rough=1.2, feather=0.7)
    art = G(art, gaussian_filter(heart, rx * 0.08) * heart, "#101a48", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=1.0, feather=1.5)
    # fine V barbs running through the whole eye, then an iridescent sheen
    ch = chevrons(s_, n_, rx * 0.06, 0.8, 5, nx()) * e0
    art = G(art, ch, "#0e2a28", seed=nx(), density=0.3, edge=0, bloom=0, gran=0, rough=0.3, feather=0.3)
    gl = chevrons(s_ + rx * 0.03, n_, rx * 0.06, 0.8, 9, nx()) * e1 * (1 - heart)
    art = OV(art, gl, lambda m: layer(m, "#d9f2c8", 0.22))
    sx_, sy_ = ex - math.cos(ang) * rx * 0.05 + math.sin(ang) * rx * 0.3, ey - math.sin(ang) * rx * 0.05 - math.cos(ang) * rx * 0.3
    sheen = ellipses(W, H, [(sx_, sy_, rx * 0.16, ry * 0.42, rot + 18)])
    art = OV(art, gaussian_filter(sheen, rx * 0.1) * e1, lambda m: layer(m, "#c8f0e0", 0.3))
    return art


def feather(art, W, H, base, eye, rx, nx, rng, barbs=1.0, wisp=0.5):
    bx, by = base; ex, ey = eye
    ang = math.atan2(ey - by, ex - bx)
    L = math.hypot(ex - bx, ey - by)
    nxv, nyv = -math.sin(ang), math.cos(ang)
    bend = rng.uniform(-0.06, 0.06) * L
    tipx, tipy = ex + math.cos(ang) * rx * 0.9, ey + math.sin(ang) * rx * 0.9
    shaft = curve([(bx, by), ((bx * 2 + ex) / 3 + nxv * bend, (by * 2 + ey) / 3 + nyv * bend), ((bx + ex * 2) / 3 + nxv * bend * 0.6, (by + ey * 2) / 3 + nyv * bend * 0.6), (ex, ey), (tipx, tipy)], 80)
    items = []
    pts = along(shaft, 6.5 / barbs)
    for (x, y, a) in pts:
        d_eye = math.hypot(x - ex, y - ey)
        if d_eye < rx * 1.05:
            continue
        t = 1 - min(1, (d_eye - rx) / max(1, L - rx))  # 0 at base .. 1 near the eye
        if t < 0.05:
            continue
        for sgn in (-1, 1):
            if rng.random() < (1 - t) * wisp * 0.75:
                continue
            spread = 0.9 - 0.45 * t + rng.uniform(-.08, .08)
            bl = rx * (0.55 + 1.15 * t ** 0.8) * rng.uniform(0.7, 1.15)
            pts_b = []
            for u in np.linspace(0, 1, 7):
                aa = a + sgn * spread * (1 - 0.55 * u)
                pts_b.append((x + math.cos(aa) * bl * u, y + math.sin(aa) * bl * u))
            # accumulate as a smooth curve from the base point
            acc = [(x, y)]
            for i in range(1, len(pts_b)):
                aa = a + sgn * spread * (1 - 0.55 * i / 6)
                px, py = acc[-1]
                acc.append((px + math.cos(aa) * bl / 6, py + math.sin(aa) * bl / 6))
            items.append((acc, rng.uniform(1.0, 1.6), (0.0, 0.55)))
    bm = strokes(W, H, items)
    art = G(art, np.clip(gaussian_filter(bm, 5) * 2.2, 0, 1), "#6f7d36", "#3f6f4f", seed=nx(), density=0.28, edge=0.2, bloom=0.5, gran=0.3, rough=4, feather=2)
    art = G(art, bm, "#a39a3c", "#5f8a4a", seed=nx(), density=0.72, edge=0.25, bloom=0.15, gran=0.2, rough=0.6, feather=0.4)
    # a few teal-gold glints on the barbs
    art = G(art, bm * (fbm(W, H, nx(), 60, 2) > 0.62), "#2f8a7a", seed=nx(), density=0.45, edge=0.1, bloom=0, rough=0.5, feather=0.4)
    art = eye_spot(art, W, H, ex, ey, rx, ang, nx, rng)
    sh = strokes(W, H, [(shaft[:int(len(shaft) * 0.93)], 4.2, (0.0, 0.5))])
    art = G(art, sh, "#d8c48a", "#b8a26a", seed=nx(), density=0.9, edge=0.4, bloom=0, rough=0.5, feather=0.4)
    return art


if "feather" in PARTS:
    W, H = 420, 1200
    rng = random.Random(3); nx = Seq(3000)
    art = feather(blank(W, H), W, H, (226, 1180), (196, 230), 92, nx, rng)
    preview(art, "mk-feather", bg=TEAL_BG)
    save(art, f"{OUT}/feather.webp", max_w=170, quality=82)
    clear()

if "eye" in PARTS:
    W, H = 360, 400
    rng = random.Random(5); nx = Seq(5000)
    art = eye_spot(blank(W, H), W, H, 180, 196, 118, -math.pi / 2, nx, rng)
    preview(art, "mk-eye", bg=TEAL_BG)
    save(art, f"{OUT}/eye.webp", max_w=120, quality=84)
    clear()

if "fan" in PARTS:
    W, H = 1300, 760
    rng = random.Random(9); nx = Seq(9000)
    art = blank(W, H)
    base = (650, 1040)
    order = [-4, 4, -3, 3, -2, 2, -1, 1, 0]
    for k in order:
        a = -math.pi / 2 + k * 0.205 + rng.uniform(-.02, .02)
        R = 860 - abs(k) * 28
        eye = (base[0] + math.cos(a) * R, base[1] + math.sin(a) * R)
        art = feather(art, W, H, (base[0] + math.cos(a) * 330, base[1] + math.sin(a) * 330), eye, 72 - abs(k) * 2.5, nx, rng, barbs=0.9, wisp=0.3)
        clear()
    preview(art, "mk-fan", bg=TEAL_BG)
    save(art, f"{OUT}/fan.webp", max_w=640, quality=80)
    clear()


def whiplash(x0, y0, sx, sy, s, d=1):
    """A coup-de-fouet line: long S-curve ending in a tight spiral. Returns points."""
    body = curve([(x0, y0), (x0 + sx * 0.35 * s + d * 30, y0 + sy * 0.2 * s), (x0 + sx * 0.6 * s - d * 20, y0 + sy * 0.55 * s), (x0 + sx * 0.82 * s, y0 + sy * 0.78 * s)], 50)
    ex, ey = body[-1]
    ang = math.atan2(ey - body[-4][1], ex - body[-4][0])
    r = s * 0.14
    cx, cy = ex + math.cos(ang + d * math.pi / 2) * r, ey + math.sin(ang + d * math.pi / 2) * r
    a0 = math.atan2(ey - cy, ex - cx)
    return body + spiral(cx, cy, r, r * 0.25, a0, 1.15, d=d, n=40)[1:]


def gild(art, W, H, items, nx, base="#c9a24a"):
    m = strokes(W, H, items)
    m = displace(m, nx(), 0.8, 14)
    art = OV(art, gaussian_filter(m, 3), lambda mm: layer(mm, "#06201f", 0.35))
    return FO(art, m, base, seed=nx(), emboss=0.8, sparkle=0.3)


if "frame" in PARTS:
    W, H = 900, 1220
    rng = random.Random(13); nx = Seq(13000)
    art = blank(W, H)
    x0, x1, top, bot = 170, 730, 340, 1150
    cx = (x0 + x1) / 2; r = (x1 - x0) / 2
    # peacock feathers rising behind the lower sides
    for (bx, ex_, ey_, rr) in [(x0 + 30, x0 - 105, bot - 420, 34), (x0 + 10, x0 - 40, bot - 560, 30), (x1 - 30, x1 + 105, bot - 420, 34), (x1 - 10, x1 + 40, bot - 560, 30)]:
        art = feather(art, W, H, (bx, bot + 40), (ex_, ey_), rr, nx, rng, barbs=0.8, wisp=0.35)
        clear()
    art = knockout(art, shapes(W, H, [[(x0 - 30, bot + 40), (x0 - 30, top), (x1 + 30, top), (x1 + 30, bot + 40)]], smooth=False), 1.0, 2)
    def arch(off):
        pts = [(x0 - off, bot + off)]
        pts += [(x0 - off, top + r * 0.55)]
        for t in np.linspace(math.pi, 2 * math.pi, 60):
            k = abs(math.cos(t))
            pts.append((cx + math.cos(t) * (r + off), top + r * 0.55 + math.sin(t) * (r + off) * (1.0 + 0.18 * (1 - k) ** 2)))
        pts += [(x1 + off, top + r * 0.55), (x1 + off, bot + off)]
        return curve(pts, 260)
    items = [(arch(14), 9, None), (arch(30), 3.4, None), (curve([(x0 - 30, bot + 30), (x1 + 30, bot + 30)], 10), 3.4, None)]
    for d, sx in ((1, -1), (-1, 1)):
        xs = x0 - 30 if sx < 0 else x1 + 30
        items.append((whiplash(xs, 640, sx * 0.4, 1.0, 250, d=d), 6, (0.0, 0.35)))
        items.append((whiplash(xs, 520, sx * 0.36, -0.95, 210, d=-d), 4.5, (0.0, 0.3)))
        items.append((whiplash(xs, bot + 30, sx * 0.9, -0.25, 160, d=d), 5, (0.0, 0.3)))
    apex = top + r * 0.55 - (r + 30) * 1.18
    for k, dx in enumerate((-50, 0, 50)):
        items.append((curve([(cx + dx * 0.3, apex + 6), (cx + dx * 0.8, apex - 34), (cx + dx * 1.1, apex - 58 + abs(dx) * 0.5)], 20), 4 if dx else 5, (0.0, 0.4)))
    for d in (1, -1):
        items.append((whiplash(cx + d * 30, apex + 2, d * 0.9, 0.18, 150, d=-d), 4, (0.0, 0.3)))
    art = gild(art, W, H, items, nx)
    art = eye_spot(art, W, H, cx, apex - 110, 40, -math.pi / 2, nx, rng)
    keep_pixel(art, 0, 0); keep_pixel(art, W - 1, H - 1)
    preview(art, "mk-frame", bg=TEAL_BG)
    save_full(art, f"{OUT}/frame.webp", size=(450, 610), quality=82)
    clear()

if "divider" in PARTS:
    W, H = 640, 150
    rng = random.Random(17); nx = Seq(17000)
    art = blank(W, H)
    items = []
    for d in (1, -1):
        line = curve([(320 + d * 40, 80), (320 + d * 120, 64), (320 + d * 210, 96), (320 + d * 270, 74)], 40)
        ex, ey = line[-1]
        items.append((line + spiral(ex - d * 0, ey - 16, 16, 4, math.pi / 2, 1.1, d=-d, n=30)[1:], 4.5, (0.0, 0.2)))
        items.append((curve([(320 + d * 46, 92), (320 + d * 130, 104), (320 + d * 190, 98)], 20), 2.2, (0.0, 0.6)))
    art = gild(art, W, H, items, nx)
    art = eye_spot(art, W, H, 320, 76, 26, -math.pi / 2, nx, rng, fringe=True)
    preview(art, "mk-divider", tone="#f3ecdc")
    save(art, f"{OUT}/divider.webp", max_w=280, quality=84)
    clear()

if "corner" in PARTS:
    # whiplash corner with a lily-like bud for cards and the closing
    W, H = 520, 520
    rng = random.Random(19); nx = Seq(19000)
    art = blank(W, H)
    items = [(curve([(20, 20), (480, 20)], 10), 3, None), (curve([(20, 20), (20, 480)], 10), 3, None),
             (whiplash(40, 40, 1.0, 0.25, 360, d=1), 5, (0.0, 0.3)), (whiplash(40, 40, 0.25, 1.0, 360, d=-1), 5, (0.0, 0.3)),
             (curve([(40, 40), (120, 110), (170, 190)], 20), 3, (0.0, 0.4))]
    art = gild(art, W, H, items, nx)
    art = feather(art, W, H, (60, 60), (190, 200), 40, nx, rng, barbs=0.8, wisp=0.3)
    preview(art, "mk-corner", bg=TEAL_BG)
    save(art, f"{OUT}/corner.webp", max_w=200, quality=82)
    save(art[::-1, ::-1].copy(), f"{OUT}/corner-br.webp", max_w=200, quality=82)
    clear()

if "paper" in PARTS:
    save_tile(paper_tile(320, "#f3ecdc", seed=21, mottle=0.5), f"{OUT}/paper.webp", quality=74)

if "silk" in PARTS:
    S = 320
    base = paper_tile(S, TEAL_BG, seed=23, fiber=0.0, mottle=1.4)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    weave = wrap_noise(S, S, 25, 0.6)
    sheen = 0.5 + 0.5 * np.sin((xx + yy) / S * math.tau * 2 + wrap_noise(S, S, 27, 18) * 6)
    rgb = base * (1 + (weave[..., None] - 0.5) * 0.08 + (sheen[..., None] - 0.5) * 0.06)
    save_tile(rgb, f"{OUT}/silk.webp", quality=92)
