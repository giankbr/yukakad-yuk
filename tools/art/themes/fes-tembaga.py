"""Fes Tembaga — a pierced, hammered copper lantern glowing from within, the star-dot light it throws across a polished
tadelakt wall (saffron and rose), and a carved cedar strapwork frieze. Geometry and lanterns only (no figures, no
calligraphy). Run: python3 -I fes-tembaga.py [part ...]   parts: lantern dots tadelakt rose cedar divider medal
Assets -> public/themes/art/fes-tembaga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e2_lib import *

OUT = outdir("fes-tembaga")
PARTS = sys.argv[1:] or ["lantern", "dots", "tadelakt", "rose", "cedar", "divider", "medal"]
COPPER, COPPER_L, COPPER_D = "#8a4421", "#d58a52", "#3a1a0c"
BRASS = "#c9a04e"
EMBER, EMBER_L = "#ffb54a", "#fff0c4"


def metal_shade(mask, W, H, cx, half, base=COPPER, light=COPPER_L, dark=COPPER_D, seed=1, hammer=True):
    """Cylindrical metal shading across x (highlight left of centre, dark rims) + hammered dimples."""
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    u = np.clip((xx - cx) / max(1, half), -1, 1)
    lum = np.clip(0.55 + 0.45 * np.cos((u + 0.35) * 1.5), 0, 1)
    c0, c1, c2 = col_arr(dark), col_arr(base), col_arr(light)
    rgb = np.where((lum < 0.6)[..., None], c0 + (c1 - c0) * (lum / 0.6)[..., None], c1 + (c2 - c1) * ((lum - 0.6) / 0.4)[..., None])
    spec = np.exp(-((u + 0.42) / 0.08) ** 2)
    rgb = rgb + spec[..., None] * 0.25
    if hammer:
        d = fbm(W, H, seed, 9, 2)
        gy, gx = np.gradient(gaussian_filter(d, 1.8))
        rgb = rgb * (1 + (-gx - gy)[..., None] * 1.6)
    return np.concatenate([np.clip(rgb, 0, 1), mask[..., None]], -1)


def part_lantern():
    W, H = 420, 1060
    rng = random.Random(3); nx = Seq(100)
    cx = W / 2
    art = blank(W, H)
    # chain + ring
    links = []
    for k in range(9):
        y = 12 + k * 19
        links.append((cx, y, 5 if k % 2 else 3, 10, 0))
    lm = np.clip(ellipses(W, H, links) - ellipses(W, H, [(x, y, max(0.1, a - 2.4), b - 2.6, 0) for x, y, a, b, _ in links if a > 3]), 0, 1)
    art = over(art, metal_shade(lm, W, H, cx, 8, seed=nx(), hammer=False))
    ring = np.clip(ellipses(W, H, [(cx, 196, 18, 16, 0)]) - ellipses(W, H, [(cx, 196, 12, 10, 0)]), 0, 1)
    art = over(art, metal_shade(ring, W, H, cx, 18, BRASS, "#f1d48a", "#6e5420", seed=nx(), hammer=False))
    # crown: finial ball, small dome, flared pierced skirt
    ball = ellipses(W, H, [(cx, 222, 11, 11, 0)])
    dome = poly(W, H, [(cx, 232)] + [(cx + math.sin(a) * 62, 300 - math.cos(a) * 66) for a in np.linspace(-math.pi / 2, math.pi / 2, 24)][::-1], smooth=True)
    dome = np.maximum(dome, poly(W, H, [(cx - 62, 300)] + [(cx + math.sin(a) * 62, 300 - math.cos(a) * 66) for a in np.linspace(-math.pi / 2, math.pi / 2, 24)] + [(cx + 62, 300)], smooth=True))
    skirt = poly(W, H, [(cx - 60, 298), (cx + 60, 298), (cx + 130, 346), (cx + 124, 358), (cx - 124, 358), (cx - 130, 346)])
    art = over(art, metal_shade(np.maximum(ball, dome), W, H, cx, 64, seed=nx()))
    art = over(art, metal_shade(skirt, W, H, cx, 130, seed=nx()))
    # skirt scallop holes
    sk_holes = circles(W, H, [(cx + x, 336, 3.2) for x in np.arange(-108, 112, 14)])
    # body profile: an ogee lantern, widest a third of the way down
    y0, y1 = 360, 820

    def rad(y):
        t = (y - y0) / (y1 - y0)
        return 54 + 92 * math.sin(math.pi * min(1, t * 1.15)) ** 0.85 * (1 - 0.25 * t)
    prof_r = [(cx + rad(y), y) for y in np.linspace(y0, y1, 50)]
    prof_l = [(cx - rad(y), y) for y in np.linspace(y1, y0, 50)]
    body = poly(W, H, prof_r + prof_l, smooth=True)
    # bottom cone + drop finial
    cone = poly(W, H, [(cx - rad(y1) - 2, y1 - 2), (cx + rad(y1) + 2, y1 - 2), (cx + 12, 900), (cx - 12, 900)])
    drop = poly(W, H, [(cx, 900), (cx + 14, 930), (cx + 9, 962), (cx, 1000), (cx - 9, 962), (cx - 14, 930)], smooth=True)
    # inner glow behind everything (the light seen through the holes and around)
    halo = glow(np.maximum(body, cone), "#ff9a3a", radius=60, strength=0.35)
    # fade the halo to zero before the canvas edge so it never shows a hard rectangle
    _ex = np.minimum(np.arange(W), W - 1 - np.arange(W)).astype(np.float32)
    _ey = np.minimum(np.arange(H), H - 1 - np.arange(H)).astype(np.float32)
    halo[..., 3] *= np.clip(np.minimum(_ex[None, :], _ey[:, None]) / 70, 0, 1) ** 1.5
    art = over(halo, art)
    art = over(art, metal_shade(body, W, H, cx, 146, seed=nx()))
    art = over(art, metal_shade(np.maximum(cone, drop), W, H, cx, 60, seed=nx()))
    # brass bands
    bands = np.zeros((H, W), np.float32)
    for yb, th in [(y0 + 6, 7), (y0 + 150, 5), (y1 - 8, 7)]:
        r = rad(yb)
        bands = np.maximum(bands, poly(W, H, [(cx - r - 3, yb - th), (cx + r + 3, yb - th), (cx + r + 3, yb + th), (cx - r - 3, yb + th)]))
    art = over(art, metal_shade(bands * np.maximum(body, cone), W, H, cx, 150, BRASS, "#f3d68e", "#6e5420", seed=nx(), hammer=False))
    # piercings: a lattice on the cylinder, 8-point star rosettes of dots + dotted diagonals; foreshortened toward rims
    holes = []
    for y in np.arange(y0 + 24, y1 - 18, 13):
        r = rad(y)
        row = int(round((y - y0) / 13))
        for k in range(-40, 41):
            th = k * 0.1 + (0.05 if row % 2 else 0)
            if abs(th) > 1.38:
                continue
            # pattern on (th, y): rosettes every 0.6 rad / 76 px, plus diagonal chains
            pu = (th / 0.8) % 1.0 - 0.5
            pv = ((y - y0) / 104.0) % 1.0 - 0.5
            dist = math.hypot(pu * 1.3, pv)
            ang = math.atan2(pv, pu)
            star = 0.3 + 0.08 * math.cos(ang * 8)
            on = (abs(dist - star) < 0.09) or dist < 0.1 or (abs(abs(pu * 1.3) - abs(pv)) < 0.07 and dist > 0.42)
            if (y - y0) > 130 and (y - y0) < 170:
                on = (k % 2 == 0)
            if not on:
                continue
            fx = math.cos(th)
            x = cx + r * math.sin(th)
            sz = 3.8 * (0.35 + 0.65 * fx)
            holes.append((x, y, sz * 1.0, sz * 1.05, 0))
    hm = ellipses(W, H, holes)
    hm = np.maximum(hm, sk_holes)
    art = over(art, glow(hm, "#ffb04a", radius=4, strength=0.5))
    art = over(art, flat(hm, EMBER))
    core = ellipses(W, H, [(x, y, a * 0.55, b * 0.55, 0) for x, y, a, b, _ in holes])
    art = over(art, flat(core, EMBER_L, 0.9))
    art = add_grain(art, nx(), 0.03)
    preview(art, "fe-lantern", bg="#c98a52")
    save(art, f"{OUT}/lantern.webp", max_w=260, quality=82)
    clear()


def part_dots():
    """The light thrown by the lantern: star rosettes of warm dots radiating outward on the wall (transparent)."""
    W, H = 780, 1000
    rng = random.Random(7); nx = Seq(400)
    cx, cy = 390, 330
    items = []
    for ring in range(1, 13):
        R = 40 + ring * 46
        n = 16 + ring * 8
        for k in range(n):
            a = k / n * math.tau + (ring % 2) * (math.pi / n)
            mod = 1 + 0.14 * math.cos(a * 8)
            x = cx + math.cos(a) * R * mod * 1.05
            y = cy + math.sin(a) * R * mod * 0.92 + R * 0.12
            if x < -20 or x > W + 20 or y < -20 or y > H + 20:
                continue
            if rng.random() < 0.12:
                continue
            s = 2.2 + ring * 0.55
            items.append((x, y, s * 1.25, s, math.degrees(a)))
    m = ellipses(W, H, items)
    m = gaussian_filter(m, 1.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fall = np.clip(1.1 - np.hypot(xx - cx, yy - cy) / 640, 0, 1)
    rgb = np.ones((H, W, 3), np.float32) * col_arr("#ffd690")
    a = np.clip(m * 1.2 * fall, 0, 1)
    pool = radial(W, H, cx, cy + 40, 420) ** 1.6 * 0.35
    a = np.clip(a + pool, 0, 1)
    art = np.concatenate([rgb, a[..., None]], -1)
    preview(art, "fe-dots", bg="#b8743c")
    save_full(art, f"{OUT}/dots.webp", size=(468, 600), quality=70)
    clear()


def plaster(seed, c_lo, c_hi, c_spot):
    """Seamless polished tadelakt tile: soft cloudy mottling, darker burnished trowel arcs, faint lime spots."""
    W = H = 512
    n1 = wnoise(W, H, seed, 40)
    n2 = wnoise(W, H, seed + 1, 12)
    n3 = wnoise(W, H, seed + 2, 3)
    t = np.clip(n1 * 0.7 + n2 * 0.3, 0, 1)
    rgb = col_arr(c_lo) * (1 - t[..., None]) + col_arr(c_hi) * t[..., None]
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    arcs = np.zeros((H, W), np.float32)
    for _ in range(26):
        ax, ay, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(60, 180)
        for ox in (-W, 0, W):
            for oy in (-H, 0, H):
                d = np.abs(np.hypot(xx - ax - ox, yy - ay - oy) - r)
                arcs = np.maximum(arcs, np.exp(-(d / 1.6) ** 2) * (np.hypot(xx - ax - ox, yy - ay - oy) < r + 4) * rng.uniform(0.3, 1.0) * ((yy - ay - oy) > -r * 0.2))
    arcs = gaussian_filter(arcs, 2.5, mode="wrap")
    rgb = rgb * (1 - arcs[..., None] * 0.035)
    deep = wnoise(W, H, seed + 7, 80)
    rgb = rgb * (0.94 + 0.12 * deep[..., None])
    spots = np.clip((n3 - 0.82) * 6, 0, 1)
    rgb = rgb * (1 - spots[..., None] * 0.35) + col_arr(c_spot) * spots[..., None] * 0.35
    sheen = np.clip((wnoise(W, H, seed + 4, 60) - 0.55) * 3, 0, 1)
    rgb = rgb + sheen[..., None] * 0.05
    return np.clip(rgb, 0, 1)


def part_tadelakt():
    rgb = plaster(11, "#c97b3c", "#e3a25c", "#f4cf96")
    prev_rgb(rgb, "fe-tadelakt")
    rgb_save(rgb, f"{OUT}/tadelakt.webp", quality=72, size=(384, 384))


def part_rose():
    rgb = plaster(23, "#cf8a7a", "#e8b2a0", "#f6dccd")
    prev_rgb(rgb, "fe-rose")
    rgb_save(rgb, f"{OUT}/rose.webp", quality=72, size=(384, 384))


def star_pts(cx, cy, R, r, n=8, rot=0.0):
    return [(cx + math.cos(rot + k * math.pi / n) * (R if k % 2 == 0 else r), cy + math.sin(rot + k * math.pi / n) * (R if k % 2 == 0 else r)) for k in range(2 * n)]


def relief(mask, wood_lo, wood_hi, seed, depth=1.0):
    """Carved wood: raised where mask, recessed elsewhere; light from upper left; grain along x."""
    H, W = mask.shape
    h = gaussian_filter(mask, 1.6)
    gy, gx = np.gradient(h)
    light = np.clip(0.5 - (gx * 0.8 + gy) * 9 * depth, 0, 1)
    rng = np.random.default_rng(seed)
    grain = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.6, 14), mode="wrap")
    grain = (grain - grain.mean()) / (grain.std() + 1e-6)
    t = np.clip(0.35 + 0.5 * h + 0.06 * grain, 0, 1)
    rgb = col_arr(wood_lo) * (1 - t[..., None]) + col_arr(wood_hi) * t[..., None]
    rgb = rgb * (0.7 + 0.6 * light[..., None])
    rgb = rgb * (1 - (1 - h)[..., None] * 0.35)
    return np.clip(rgb, 0, 1)


def part_cedar():
    """Repeat-x carved cedar frieze: interlaced 8-point stars on a strapwork band."""
    P, H = 160, 96
    W = P * 4
    cv = Canvas(W, H)
    st = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=6)
    for k in range(-1, 5):
        x = k * P + P / 2
        cv.c.drawPath(poly_path(star_pts(x, H / 2, 34, 26, 8, math.pi / 8)), st)
        cv.c.drawPath(poly_path(star_pts(x, H / 2, 14, 10, 8, 0)), st)
        xm = x + P / 2
        cv.c.drawPath(poly_path([(xm, H / 2 - 22), (xm + 22, H / 2), (xm, H / 2 + 22), (xm - 22, H / 2)]), st)
        cv.c.drawLine(x + 30, H / 2 - 14, xm - 12, H / 2 - 30, st)
        cv.c.drawLine(x + 30, H / 2 + 14, xm - 12, H / 2 + 30, st)
        cv.c.drawLine(xm + 12, H / 2 - 30, x + P - 30, H / 2 - 14, st)
        cv.c.drawLine(xm + 12, H / 2 + 30, x + P - 30, H / 2 + 14, st)
    cv.c.drawLine(0, 8, W, 8, st)
    cv.c.drawLine(0, H - 8, W, H - 8, st)
    m = cv.array()[..., 3]
    rgb = relief(m, "#4a2414", "#b8743f", 5)
    prev_rgb(rgb, "fe-cedar")
    rgb_save(rgb, f"{OUT}/cedar.webp", quality=80, size=(480, 72))


def part_divider():
    W, H = 520, 120
    nx = Seq(800)
    art = blank(W, H)
    cx, cy = W / 2, H / 2
    s = poly(W, H, star_pts(cx, cy, 44, 30, 8, math.pi / 8))
    s2 = poly(W, H, star_pts(cx, cy, 20, 14, 8, 0))
    art = over(art, glow(s, "#ffb04a", radius=14, strength=0.25))
    art = over(art, metal_shade(s, W, H, cx, 44, seed=nx(), hammer=False))
    holes = circles(W, H, [(cx + math.cos(a) * 30, cy + math.sin(a) * 30, 2.4) for a in np.linspace(0, math.tau, 16, endpoint=False)] + [(cx, cy, 3)])
    art = over(art, metal_shade(s2, W, H, cx, 20, BRASS, "#f3d68e", "#6e5420", seed=nx(), hammer=False))
    art = over(art, flat(holes, EMBER_L))
    lines = strokes(W, H, [([(30, cy), (cx - 54, cy)], 2.2, (0.5, 0.05)), ([(cx + 54, cy), (W - 30, cy)], 2.2, (0.05, 0.5))])
    art = over(art, metal_shade(lines, W, H, cx, W / 2, seed=nx(), hammer=False))
    dots = circles(W, H, [(x, cy, 2.6) for x in (cx - 70, cx - 84, cx + 70, cx + 84)])
    art = over(art, glow(dots, "#ffb04a", 3, 0.6))
    art = over(art, flat(dots, EMBER))
    preview(art, "fe-divider", bg="#e3a25c")
    save(art, f"{OUT}/divider.webp", max_w=300, quality=84)


def part_medal():
    W = H = 240
    nx = Seq(900)
    cx = cy = 120
    disc = circles(W, H, [(cx, cy, 100)])
    art = over(blank(W, H), glow(disc, "#ffb04a", 12, 0.2))
    art = over(art, metal_shade(disc, W, H, cx, 100, seed=nx(), hammer=False))
    rim = np.clip(circles(W, H, [(cx, cy, 100)]) - circles(W, H, [(cx, cy, 90)]), 0, 1)
    art = over(art, metal_shade(rim, W, H, cx, 100, BRASS, "#f3d68e", "#6e5420", seed=nx(), hammer=False))
    holes = []
    for ring, (R, n, s) in enumerate([(0, 1, 6), (24, 8, 4.2), (44, 16, 3.6), (64, 16, 4.2), (78, 32, 2.4)]):
        for k in range(n):
            a = k / n * math.tau + (math.pi / n if ring == 3 else 0)
            holes.append((cx + math.cos(a) * R, cy + math.sin(a) * R, s))
    hm = circles(W, H, holes)
    art = over(art, glow(hm, "#ffb04a", 3, 0.5))
    art = over(art, flat(hm, EMBER))
    art = over(art, flat(circles(W, H, [(x, y, s * 0.5) for x, y, s in holes]), EMBER_L, 0.9))
    preview(art, "fe-medal", bg="#e3a25c")
    save(art, f"{OUT}/medal.webp", max_w=110, quality=84)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
