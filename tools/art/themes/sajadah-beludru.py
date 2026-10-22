"""Sajadah Beludru — Islamic, inspired by velvet prayer-rug design: wine velvet pile (tileable), a gold-embroidered
mihrab niche frame with floral spandrels (satin stitch + couched cord), a hanging kandil lamp, a woven border band,
an embroidered rosette, and a tassel fringe. No figures, no calligraphy.
Run: python3 -I sajadah-beludru.py [part ...]  parts: velvet mihrab lamp border rosette fringe
Assets -> public/themes/art/sajadah-beludru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g2_lib import *

OUT = outdir("sajadah-beludru")
PARTS = sys.argv[1:] or ["velvet", "mihrab", "lamp", "border", "rosette", "fringe"]
WINE, WINE_D, WINE_L = "#5c1124", "#3c0915", "#7d1c33"
TEAL = "#1d4a44"
GOLD = dict(base="#c9a14a", hi="#f8e7ae", lo="#6e4f1f")
IVORY = dict(base="#e8dcc2", hi="#ffffff", lo="#9c8f78")
ROSE = dict(base="#c97a7a", hi="#f2c4b8", lo="#6e3030")
GREEN = dict(base="#4f8a6e", hi="#a9d6b6", lo="#1f4a38")


def velvet(W, H, base, seed, wrap=True):
    pile = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), 0.7, mode="wrap")
    pile = (pile - pile.mean()) / (pile.std() + 1e-6)
    crush = wrapn(W, H, seed + 1, 16) if wrap else fbm(W, H, seed + 1, 90, 3)
    crush2 = wrapn(W, H, seed + 2, 9) if wrap else fbm(W, H, seed + 2, 30, 3)
    nap = lin_field(W, H, seed + 3, (1, 0), 6, 1.2, wrap)
    sheen = np.clip((crush - 0.5) * 2.6 + (crush2 - 0.5) * 0.8, -1, 1)
    b = rgb_of(base)
    rgb = b[None, None] * (1 + sheen[..., None] * 0.17 + pile[..., None] * 0.07 + nap[..., None] * 0.035)
    hi = np.clip(sheen - 0.55, 0, 1)[..., None]
    rgb = rgb + (rgb_of("#a8455c") - rgb) * hi * 0.25
    return opaque(rgb)


def flower(art, W, H, x, y, r, n, rot, petal, center, seed):
    """Embroidered flower: n satin-stitched petals (stitches across each petal), French-knot centre."""
    for k in range(n):
        a = rot + k * math.tau / n
        pm = shapes(W, H, [petal_pts(x + math.cos(a) * r * 0.18, y + math.sin(a) * r * 0.18, r, r * 0.5, a, n=14)])
        art = ST(art, pm, a + math.pi / 2 + 0.25, seed=seed + k, **petal)
    art = ST(art, circles(W, H, [(x, y, r * 0.28)]), rot, seed=seed + 50, spacing=1.6, **center)
    knots = [(x + math.cos(t) * r * 0.16, y + math.sin(t) * r * 0.16, 1.6) for t in np.linspace(0, math.tau, 7)[:-1]]
    art = OV(art, circles(W, H, knots), lambda m: col_arr(m, "#fff4cf", m * 0.8), pad=4)
    return art


def leaf(art, W, H, x, y, L, ang, col, seed):
    pm = shapes(W, H, [petal_pts(x, y, L, L * 0.36, ang, n=12)])
    # fishbone: two halves stitched at opposite diagonals
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = ((xx - x) * math.sin(ang) - (yy - y) * math.cos(ang)) > 0
    art = ST(art, pm * side, ang + 1.0, seed=seed, **col)
    art = ST(art, pm * (~side), ang - 1.0, seed=seed + 1, **col)
    return art


if "velvet" in PARTS:
    P = 384
    v = velvet(P, P, WINE, 11)
    to_image(np.tile(v, (2, 2, 1))).convert("RGB").save(f"{PREV}/velvet-2x2.png")
    save_rgb(v, f"{OUT}/velvet.webp", quality=86)
    vt = velvet(P // 2, P // 2, TEAL, 21)
    save_rgb(vt, f"{OUT}/velvet-teal.webp", quality=86)
    clear()

if "mihrab" in PARTS:
    W, H = 640, 900
    cx, ys, yb, half, rise = 320, 420, 900, 236, 300
    d = (rise ** 2 - half ** 2) / (2 * half)
    r = half + d

    def arch(off, bottom=yb):
        ro = r - off
        pts = [(cx - half + off, bottom), (cx - half + off, ys)]
        th_a = math.acos(-d / ro)
        for k in range(1, 41):
            th = math.pi + (th_a - math.pi) * k / 40
            pts.append((cx + d + ro * math.cos(th), ys - ro * math.sin(th)))
        right = [(2 * cx - x, y) for x, y in pts[::-1]]
        return pts + right[1:]

    def angle_field(xx, yy):
        left = xx < cx
        ax = np.where(left, cx + d, cx - d)
        a = np.arctan2(yy - ys, xx - ax)
        return np.where(yy > ys, 0.0, a)

    art = blank(W, H)
    nx = Seq(50100); rng = random.Random(5)
    outer_rect = [(14, 14), (W - 14, 14), (W - 14, yb), (14, yb)]
    # spandrel floral fill: between the rectangle and the arch
    span = np.clip(shapes(W, H, [outer_rect], smooth=False) - shapes(W, H, [arch(-14)], smooth=False), 0, 1)
    span = span * (np.mgrid[0:H, 0:W][0] < ys + 10)
    tv = velvet(W, H, TEAL, 31, wrap=False)
    art = over(art, np.concatenate([tv[..., :3], span[..., None] * 0.92], -1))
    art = couch(art, [(arch(-22)[1:-1], 2.0)], seed=nx(), **GOLD)
    # vine stems in couched gold
    vines = []
    for sgn in (-1, 1):
        base_x = cx + sgn * 180
        vines.append((curve([(cx + sgn * 30, 40), (cx + sgn * 110, 52), (cx + sgn * 200, 70), (cx + sgn * 262, 140), (cx + sgn * 290, 250)], 40), 3.0))
        vines.append((curve([(cx + sgn * 140, 58), (cx + sgn * 180, 100), (cx + sgn * 240, 110)], 20), 2.4))
        vines.append((curve([(cx + sgn * 262, 140), (cx + sgn * 236, 190), (cx + sgn * 274, 214)], 16), 2.2))
    vm = strokes(W, H, [(v, w, None) for v, w in vines]) * span
    art = couch(art, [(v, w) for v, w in vines], seed=nx(), **{k: GOLD[k] for k in ("base", "hi", "lo")})
    art[..., 3] *= np.clip(span + (1 - np.clip(gaussian_filter(span, 2) * 3, 0, 1)) * 0, 0, 1) if False else 1
    for sgn in (-1, 1):
        for (x, y, rr, n, petal) in ((cx + sgn * 70, 30, 10, 5, ROSE), (cx + sgn * 296, 40, 15, 8, GOLD), (cx + sgn * 160, 90, 9, 5, GOLD), (cx + sgn * 296, 330, 11, 5, IVORY), (cx + sgn * 200, 70, 22, 8, ROSE), (cx + sgn * 262, 140, 18, 6, IVORY), (cx + sgn * 290, 252, 16, 5, ROSE), (cx + sgn * 240, 110, 12, 5, IVORY), (cx + sgn * 118, 46, 13, 6, IVORY), (cx + sgn * 274, 214, 11, 5, GOLD)):
            art = flower(art, W, H, x, y, rr, n, rng.uniform(0, 1), petal, GOLD, nx())
        for (x, y, L, a) in ((cx + sgn * 160, 66, 22, -0.4), (cx + sgn * 226, 92, 20, 0.6), (cx + sgn * 282, 186, 22, 1.9), (cx + sgn * 250, 160, 18, -2.2), (cx + sgn * 70, 44, 18, 0.2)):
            aa = a if sgn > 0 else math.pi - a
            art = leaf(art, W, H, x, y, L, aa, GREEN, nx())
        clear()
    # main arch band: satin-stitched gold, with an ivory couched inner line and a teal ground stripe
    band = np.clip(shapes(W, H, [arch(-12)], smooth=False) - shapes(W, H, [arch(18)], smooth=False), 0, 1)
    def ufn(xx, yy):
        left = xx < cx
        ax = np.where(left, cx + d, cx - d)
        th = np.arctan2(ys - yy, np.abs(xx - ax))   # 0 at spring line, grows toward apex
        arc_u = th * r * np.where(left, 1, -1) + 4000
        side_u = (ys - yy) * np.where(left, 1, -1) + 4000
        return np.where(yy > ys, side_u, arc_u)
    art = ST(art, band, lambda xx, yy: angle_field(xx, yy) + math.pi / 2, ufn=ufn, seed=nx(), spacing=2.2, **GOLD)
    clear()
    # little lozenge studs along the band (counted stitch)
    studs = []
    pts = along(arch(3), 30)
    for p_ in pts:
        x, y = p_[0], p_[1]
        if y < yb - 20:
            studs.append([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)])
    art = ST(art, shapes(W, H, studs, smooth=False), 0.8, seed=nx(), spacing=1.4, **ROSE)
    art = couch(art, [(arch(-16), 2.4), (arch(22), 2.2)], seed=nx(), **IVORY)
    # outer rectangle frame cord + corner knots
    art = couch(art, [(outer_rect + [outer_rect[0]], 3.0)], seed=nx(), **GOLD)
    # crest at the apex: a small finial bud
    apex_y = ys - math.sqrt((r + 12) ** 2 - d ** 2)
    art = flower(art, W, H, cx, apex_y - 18, 15, 8, 0.2, GOLD, IVORY, nx())
    # column capitals at the spring line
    for sgn in (-1, 1):
        x = cx + sgn * (half - 3)
        cap = shapes(W, H, [[(x - 22, ys + 6), (x + 22, ys + 6), (x + 14, ys + 24), (x - 14, ys + 24)]], smooth=False)
        art = ST(art, cap, 1.57, seed=nx(), spacing=1.8, **GOLD)
        art = ST(art, ellipses(W, H, [(x, ys + 34, 10, 7, 0)]), 0.0, seed=nx(), spacing=1.6, **IVORY)
    # fade the bottom of the columns so the frame dissolves into the field
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art[..., 3] *= np.clip((yb - yy) / 240, 0, 1) ** 0.8
    pv = over(velvet(W, H, WINE, 3, wrap=False), art)
    to_image(pv).convert("RGB").save(f"{PREV}/mihrab.png")
    save(art, f"{OUT}/mihrab.webp", max_w=640, quality=80)
    clear()

if "lamp" in PARTS:
    W, H = 240, 460
    nx = Seq(50200)
    cx = 120
    art = blank(W, H)
    # chain: couched oval links
    for k in range(9):
        y = 8 + k * 16
        art = couch(art, [(arc_pts(cx, y + 7, 5 if k % 2 else 3, 0, math.tau, 18, squash=1.6), 2.0)], seed=nx(), **GOLD)
    # glow behind the bowl
    bowl = shapes(W, H, [[(cx - 30, 232), (cx - 70, 270), (cx - 84, 316), (cx - 64, 356), (cx - 26, 372), (cx + 26, 372), (cx + 64, 356), (cx + 84, 316), (cx + 70, 270), (cx + 30, 232)]])
    art = over(art, glow(bowl, "#ffcf7a", radius=26, strength=0.35))
    cap = shapes(W, H, [[(cx - 16, 154), (cx + 16, 154), (cx + 30, 176), (cx + 22, 186), (cx - 22, 186), (cx - 30, 176)]])
    neck = shapes(W, H, [[(cx - 20, 186), (cx + 20, 186), (cx + 34, 236), (cx - 34, 236)]], smooth=False)
    foot = shapes(W, H, [[(cx - 22, 370), (cx + 22, 370), (cx + 32, 392), (cx - 32, 392)]], smooth=False)
    drop = shapes(W, H, [petal_pts(cx, 396, 34, 12, math.pi / 2, n=12)])
    art = ST(art, cap, 0.0, seed=nx(), spacing=2.0, **GOLD)
    art = ST(art, neck, 1.57, seed=nx(), spacing=2.0, **GOLD)
    art = ST(art, bowl, 0.0, ufn=lambda xx, yy: np.arctan2(yy - 300, xx - cx) * 60, seed=nx(), spacing=2.2, **GOLD)
    # bowl panels: ivory glass windows with teal lattice
    wins = []
    for k in range(5):
        x = cx - 56 + k * 28
        wins.append([(x - 8, 290), (x, 274), (x + 8, 290), (x + 8, 336), (x - 8, 336)])
    wm = shapes(W, H, wins, smooth=False) * bowl
    art = ST(art, wm, 1.57, seed=nx(), spacing=1.8, base="#f6dc9c", hi="#fff8e0", lo="#b98a3e")
    art = over(art, glow(wm, "#fff0c0", radius=6, strength=0.5))
    art = couch(art, [(arc_pts(cx, 300, 80, math.pi * 0.95, math.pi * 0.05, 30, squash=0.25), 2.2), (arc_pts(cx, 350, 64, math.pi * 0.92, math.pi * 0.08, 30, squash=0.2), 2.0)], seed=nx(), **IVORY)
    art = ST(art, foot, 0.0, seed=nx(), spacing=2.0, **GOLD)
    art = ST(art, drop, 0.0, seed=nx(), spacing=1.8, **ROSE)
    pv = over(velvet(W, H, WINE, 5, wrap=False), art)
    to_image(pv).convert("RGB").save(f"{PREV}/lamp.png")
    save(art, f"{OUT}/lamp.webp", max_w=180, quality=82)
    clear()

if "border" in PARTS:
    P_, Hh = 480, 76
    nx = Seq(50300)
    art = velvet(P_, Hh, WINE_D, 41)
    tv = velvet(P_, 30, TEAL, 43)
    art[23:53] = tv
    art = couch(art, [([(-10, 6), (P_ + 10, 6)], 3.0), ([(-10, Hh - 6), (P_ + 10, Hh - 6)], 3.0)], seed=nx(), **GOLD)
    art = couch(art, [([(-10, 21), (P_ + 10, 21)], 1.8), ([(-10, Hh - 21), (P_ + 10, Hh - 21)], 1.8)], seed=nx(), **IVORY)
    vine = [(x, 38 + 9 * math.sin(x / P_ * math.tau * 4)) for x in range(-10, P_ + 11, 4)]
    art = couch(art, [(vine, 2.0)], seed=nx(), **GOLD)
    for k in range(4):
        x = 60 + k * 120
        art = flower(art, P_, Hh, x, 38, 12, 6, 0.3 * k, ROSE if k % 2 else IVORY, GOLD, nx())
        lx = x + 60
        loz = [[(lx, 28), (lx + 8, 38), (lx, 48), (lx - 8, 38)]] if lx < P_ else [[(lx - P_, 28), (lx - P_ + 8, 38), (lx - P_, 48), (lx - P_ - 8, 38)]]
        art = ST(art, shapes(P_, Hh, loz, smooth=False), 0.8, seed=nx(), spacing=1.6, **GOLD)
    to_image(np.tile(art, (1, 2, 1))).convert("RGB").save(f"{PREV}/border-2x.png")
    save_rgb(art, f"{OUT}/border.webp", quality=80)
    clear()

if "rosette" in PARTS:
    W, H = 240, 240
    nx = Seq(50400)
    art = blank(W, H)
    c = 120
    for k in range(8):
        a = k * math.tau / 8
        pm = shapes(W, H, [petal_pts(c + math.cos(a) * 18, c + math.sin(a) * 18, 66, 24, a, n=16)])
        art = ST(art, pm, a + math.pi / 2, seed=nx(), spacing=2.2, **GOLD)
        inner = shapes(W, H, [petal_pts(c + math.cos(a) * 30, c + math.sin(a) * 30, 40, 14, a, n=12)])
        art = ST(art, inner, a + math.pi / 2, seed=nx(), spacing=1.8, **(ROSE if k % 2 else IVORY))
    for k in range(8):
        a = (k + 0.5) * math.tau / 8
        art = leaf(art, W, H, c + math.cos(a) * 62, c + math.sin(a) * 62, 22, a, GREEN, nx())
    art = flower(art, W, H, c, c, 20, 6, 0.0, GOLD, IVORY, nx())
    pv = over(velvet(W, H, WINE, 6, wrap=False), art)
    to_image(pv).convert("RGB").save(f"{PREV}/rosette.png")
    save(art, f"{OUT}/rosette.webp", max_w=180, quality=82)
    clear()

if "fringe" in PARTS:
    P_, Hh = 240, 84
    nx = Seq(50500); rng = random.Random(9)
    art = blank(P_, Hh)
    head = velvet(P_, 12, WINE_D, 51)
    art[:12] = head
    art = couch(art, [([(-10, 11), (P_ + 10, 11)], 2.6)], seed=nx(), **GOLD)
    for k in range(20):
        x = 6 + k * 12
        sw = rng.uniform(-2.5, 2.5)
        L = 68 + rng.uniform(-4, 4)
        c = GOLD if k % 2 else IVORY
        threads = [(curve([(x + dx, 12), (x + dx * 1.4 + sw * 0.5, 40), (x + dx * 2 + sw, 12 + L)], 14), 1.4, (0.0, 0.2)) for dx in (-2.4, -1.2, 0, 1.2, 2.4)]
        tm = strokes(P_, Hh, threads)
        art = ST(art, tm, 0.0, seed=nx(), spacing=1.2, **c)
        art = ST(art, ellipses(P_, Hh, [(x + sw * 0.25, 24, 4.6, 3.6, 0)]), 0.0, seed=nx(), spacing=1.2, **GOLD)
    to_image(np.tile(art, (1, 2, 1))).save(f"{PREV}/sfringe-2x.png")
    im = to_image(art); im.save(f"{OUT}/fringe.webp", "WEBP", quality=82, method=6)
    to_image(art[::-1].copy()).save(f"{OUT}/fringe-up.webp", "WEBP", quality=82, method=6)
    print("fringe", im.size, os.path.getsize(f"{OUT}/fringe.webp") // 1024, "KB")
    clear()
