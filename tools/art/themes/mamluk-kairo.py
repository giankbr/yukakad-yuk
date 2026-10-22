"""Mamluk Kairo — painted sandstone architecture after Mamluk Cairo: a recessed portal with ablaq (alternating light/dark
stone) courses, a muqarnas hood of stepped niche cells, a joggled-voussoir lintel over an open doorway (the photo shows
through it); a brass lamp with enamel bands; ablaq wall tile; joggled divider; carved stone rosette. Geometry and
architecture only (no figures, no calligraphy). Run: python3 -I mamluk-kairo.py [part ...]
parts: portal ablaq lamp divider rosette   Assets -> public/themes/art/mamluk-kairo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e2_lib import *

OUT = outdir("mamluk-kairo")
PARTS = sys.argv[1:] or ["portal", "ablaq", "lamp", "divider", "rosette"]
LIME, LIME_D = "#e9d6b0", "#c9b089"
RUST, RUST_D = "#a9583a", "#7e3c26"
BASALT = "#3b302c"
SHADOW = "#6e5640"
BRASS, BRASS_L, BRASS_D = "#b98a3e", "#ecd08a", "#5e4419"
ENAMEL_B, ENAMEL_R = "#2e5d8a", "#a5322a"


def stone(W, H, mask, col, col2, seed, rough=1.2):
    """Opaque sandstone: gouache body + speckle + soft weathering."""
    lay = gouache_paint(mask, col, col2, seed=seed, rough=rough, streak=0.4)
    sp = np.random.default_rng(seed + 1).random((H, W)).astype(np.float32)
    lay[..., :3] *= (1 - (sp > 0.985)[..., None] * 0.18) * (0.95 + 0.1 * fbm(W, H, seed + 2, 30, 3))[..., None]
    return lay


def ablaq_layer(W, H, region, y0, course_h, seed, pattern=(LIME, RUST, LIME, BASALT), joint="#8a7357", block_w=(70, 130)):
    """Horizontal courses alternating light/dark stone, with staggered vertical joints."""
    rng = random.Random(seed)
    art = blank(W, H)
    k = 0
    y = y0
    while y < H:
        col = pattern[k % len(pattern)]
        m = rect(W, H, -10, y, W + 10, y + course_h) * region
        if m.max() > 0:
            art = over(art, stone(W, H, m, col, mix_hex(col, "#000000", 0.08), seed + k * 7))
            # vertical joints
            x = rng.uniform(-60, 0)
            js = []
            tint = np.ones((H, W), np.float32)
            while x < W:
                nxt = x + rng.uniform(*block_w)
                tint[int(max(0, y)):int(min(H, y + course_h)), int(max(0, x)):int(max(0, min(W, nxt)))] = rng.uniform(0.9, 1.06)
                x = nxt
                js.append(([(x, y + 1), (x + rng.uniform(-1, 1), y + course_h - 1)], 1.6, None))
            tint = gaussian_filter(tint, 1.2)
            art[..., :3] = np.where(m[..., None] > 0.5, art[..., :3] * tint[..., None], art[..., :3])
            jm = strokes(W, H, js) * m
            art = over(art, flat(jm, joint, 0.7))
        hz = strokes(W, H, [([(-10, y), (W + 10, y)], 1.8, None)]) * region
        art = over(art, flat(hz, joint, 0.8))
        y += course_h
        k += 1
    return art


def niche(cx, top, w, h):
    """One muqarnas cell outline: straight sides, pointed-arch head."""
    r = w / 2
    pts = [(cx - r, top + h)]
    pts += [(cx - r + (1 - math.cos(a)) * r * 0.0 + (r - r * math.cos(a)) * 0 + (-r + r * (1 - math.cos(a))) * 0 + (cx - r) * 0 + 0, 0) for a in []]
    pts.append((cx - r, top + h * 0.45))
    for t in np.linspace(0, 1, 8):
        pts.append((cx - r + r * t, top + h * 0.45 - math.sin(t * math.pi / 2) * h * 0.45))
    for t in np.linspace(0, 1, 8):
        pts.append((cx + r * t, top + math.sin(t * math.pi / 2) ** 1 * 0 + (1 - math.cos(t * math.pi / 2)) * h * 0.45))
    pts.append((cx + r, top + h * 0.45))
    pts.append((cx + r, top + h))
    return pts


def part_portal():
    W, H = 700, 1100
    rng = random.Random(4); nx = Seq(100)
    full = rect(W, H, 0, 0, W, H)
    # outer face: ablaq courses
    art = ablaq_layer(W, H, full, 0, 40, nx())
    clear()
    # recess (darker, in shadow) with a pointed-arch head
    rx0, rx1 = 92, 608
    apex, spring = 70, 300
    rcx = (rx0 + rx1) / 2
    half = (rx1 - rx0) / 2
    arch = [(rx0, H + 10), (rx0, spring)]
    for t in np.linspace(0, 1, 20):
        a = t * math.pi / 2
        arch.append((rx0 + half * (1 - math.cos(a)) , spring - (spring - apex) * math.sin(a) ** 1.25))
    for t in np.linspace(0, 1, 20):
        a = (1 - t) * math.pi / 2
        arch.append((rx1 - half * (1 - math.cos(a)), spring - (spring - apex) * math.sin(a) ** 1.25))
    arch += [(rx1, spring), (rx1, H + 10)]
    recess = poly(W, H, arch, smooth=False)
    # frame moulding around the recess (a raised roll in pale stone)
    frame = np.clip(gaussian_filter(recess, 0.5) - 0, 0, 1)
    ring = np.clip(np.clip(gaussian_filter(recess, 9) * 2.0, 0, 1) - recess, 0, 1)
    art = over(art, stone(W, H, (ring > 0.08).astype(np.float32), "#f1e2c2", LIME_D, nx()))
    art = over(art, stone(W, H, recess, "#cdb089", "#b89670", nx()))
    # recess inner walls carry ablaq too (smaller courses, in shade)
    inner = ablaq_layer(W, H, recess * ygrad(W, H, 520, 540), 520, 26, nx(), pattern=(LIME_D, RUST_D, LIME_D, BASALT), block_w=(50, 90))
    inner[..., :3] *= 0.86
    art = over(art, inner)
    clear()
    # muqarnas hood: tiers of niche cells stepping down; each cell darker in its head (concave), pale lip below
    tiers = [(apex + 30, 1, 120), (apex + 92, 3, 66), (apex + 152, 5, 62), (apex + 212, 7, 60), (apex + 272, 9, 58), (apex + 330, 11, 56), (apex + 388, 13, 52)]
    cells_dark = np.zeros((H, W), np.float32)
    cells_all = np.zeros((H, W), np.float32)
    cells_lip = np.zeros((H, W), np.float32)
    polys, heads, lips = [], [], []
    for ti, (ty, n, ch) in enumerate(tiers):
        cw = min((rx1 - rx0 - 12) / n, 92)
        x0 = rcx - cw * n / 2
        for k in range(n):
            cx = x0 + cw * (k + 0.5)
            pts = niche(cx, ty, cw - 6, ch)
            polys.append(pts)
            heads.append(niche(cx, ty + 3, cw - 14, ch * 0.62))
            lips.append([(cx - cw / 2 + 3, ty + ch - 6), (cx + cw / 2 - 3, ty + ch - 6), (cx + cw / 2 - 3, ty + ch), (cx - cw / 2 + 3, ty + ch)])
            # hanging pendant between cells
            if k < n - 1:
                px = cx + cw / 2
                lips.append([(px - 6, ty + ch), (px + 6, ty + ch), (px, ty + ch + 14)])
    cells_all = shapes(W, H, polys, smooth=False) * recess
    cells_dark = shapes(W, H, heads, smooth=False) * recess
    cells_lip = shapes(W, H, lips, smooth=False) * recess
    hood = recess * (1 - ygrad(W, H, apex + 440, apex + 450))
    art = over(art, flat(hood * 1.0, "#b79572", 1.0))
    art = over(art, stone(W, H, cells_all * hood, "#dcc39b", "#cfb58d", nx(), rough=0.6))
    yy = ygrad(W, H, 0, H)
    shade = blank(W, H)
    for (ty, n, ch) in tiers:
        g = 1 - ygrad(W, H, ty, ty + ch * 0.62)
        shade = over(shade, flat(cells_dark * hood * g * (ygrad(W, H, ty - 1, ty) > 0) * (1 - ygrad(W, H, ty + ch * 0.62, ty + ch * 0.62 + 1)), "#5a412c", 0.55))
    art = over(art, shade)
    art = over(art, stone(W, H, cells_lip * hood, "#f3e4c4", "#e6d2ab", nx(), rough=0.4))
    # side light: the left half of the hood catches light, right half in shade
    art = over(art, flat(hood * xgrad(W, H, rcx - 40, rx1), "#3a2a20", 0.22))
    clear()
    # geometric frieze under the hood (no script): interlaced lozenges carved in relief
    fy0, fy1 = apex + 452, apex + 492
    fr = rect(W, H, rx0 + 4, fy0, rx1 - 4, fy1)
    art = over(art, stone(W, H, fr, "#d7bd93", "#c9ad83", nx()))
    lz = []
    for x in np.arange(rx0 + 20, rx1 - 10, 32):
        lz.append([(x, (fy0 + fy1) / 2), (x + 14, fy0 + 6), (x + 28, (fy0 + fy1) / 2), (x + 14, fy1 - 6)])
    lzm = shapes(W, H, lz, smooth=False)
    lzi = shapes(W, H, [[(x + 7, (fy0 + fy1) / 2), (x + 14, fy0 + 13), (x + 21, (fy0 + fy1) / 2), (x + 14, fy1 - 13)] for x in np.arange(rx0 + 20, rx1 - 10, 32)], smooth=False)
    art = over(art, flat(np.clip(lzm - lzi, 0, 1) * fr, "#7e5f42", 0.75))
    art = over(art, flat(lzi * fr, "#f1e2c2", 0.8))
    clear()
    # door: joggled lintel (interlocking light/dark voussoirs) over an opening
    dx0, dx1, dy = 168, 532, 640
    ly0, ly1 = 566, dy
    nj = 7
    jw = (dx1 - dx0 + 44) / nj
    ym = (ly0 + ly1) / 2
    pieces = []
    for k in range(nj):
        x = dx0 - 22 + k * jw
        pts = [(x, ly0), (x + jw, ly0), (x + jw, ym - 16)]
        if k < nj - 1:
            pts += [(x + jw + 10, ym - 20), (x + jw + 17, ym), (x + jw + 10, ym + 20)]
        pts += [(x + jw, ym + 16), (x + jw, ly1), (x, ly1), (x, ym + 16)]
        if k > 0:
            pts += [(x + 10, ym + 20), (x + 17, ym), (x + 10, ym - 20)]
        pts += [(x, ym - 16)]
        pieces.append((pts, k))
    for pts, k in pieces:
        m = poly(W, H, pts, smooth=False)
        col = "#f0e0bd" if k % 2 == 0 else BASALT
        art = over(art, stone(W, H, m, col, mix_hex(col, "#000000", 0.1), nx(), rough=0.5))
    edges = strokes(W, H, [([p, pts[(i + 1) % len(pts)]], 1.6, None) for pts, k in pieces for i, p in enumerate(pts)])
    art = over(art, flat(edges, "#6d5640", 0.7))
    # door reveal (jambs in shade) + opening
    jamb = rect(W, H, dx0 - 22, ly1, dx1 + 22, H)
    art = over(art, stone(W, H, jamb, "#a98c6a", "#9a7d5c", nx()))
    door = rect(W, H, dx0, ly1 + 6, dx1, H + 4)
    # cast shadow at the top of the opening
    art[..., 3] = art[..., 3] * (1 - door)
    sh = door * (1 - ygrad(W, H, ly1 + 6, ly1 + 50))
    art = over(art, flat(sh, "#1d140e", 0.45))
    grime = np.clip(fbm(W, H, nx(), 50, 3) - 0.35, 0, 1) * (0.4 + 0.6 * ygrad(W, H, 400, H))
    art[..., :3] *= (1 - grime * 0.22)[..., None]
    art = add_grain(art, nx(), 0.03)
    preview(art, "mk-portal", bg="#7a6a5a")
    save_full(art, f"{OUT}/portal.webp", size=(490, 770), quality=80)
    clear()


def part_ablaq():
    """Seamless ablaq wall tile: four courses (cream, rust, cream, basalt)."""
    W, H = 480, 4 * 44
    art = ablaq_layer(W, H, np.ones((H, W), np.float32), 0, 44, 77, block_w=(90, 160))
    # make horizontally seamless: blend ends
    k = np.clip(np.arange(W) / 60.0, 0, 1)[None, :, None]
    art = art * k + art[:, ::-1] * (1 - k)
    rgb = art[..., :3]
    prev_rgb(rgb, "mk-ablaq")
    rgb_save(rgb, f"{OUT}/ablaq.webp", quality=76)


def brass(mask, W, H, cx, half, seed):
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    u = np.clip((xx - cx) / max(1, half), -1, 1)
    lum = np.clip(0.5 + 0.5 * np.cos((u + 0.3) * 1.45), 0, 1)
    c0, c1, c2 = col_arr(BRASS_D), col_arr(BRASS), col_arr(BRASS_L)
    rgb = np.where((lum < 0.6)[..., None], c0 + (c1 - c0) * (lum / 0.6)[..., None], c1 + (c2 - c1) * ((lum - 0.6) / 0.4)[..., None])
    rgb = rgb * (0.95 + 0.1 * fbm(W, H, seed, 20, 2))[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), mask[..., None]], -1)


def part_lamp():
    W, H = 360, 860
    nx = Seq(500)
    cx = W / 2
    art = blank(W, H)
    # three chains to a cap
    ch = strokes(W, H, [([(cx, 0), (cx, 150)], 3, None), ([(cx, 150), (cx - 96, 420)], 2.4, None), ([(cx, 150), (cx + 96, 420)], 2.4, None), ([(cx, 150), (cx - 30, 410)], 2.0, None)])
    links = strokes(W, H, [([(cx - 4, y), (cx + 4, y + 6)], 2, None) for y in range(4, 140, 12)])
    art = over(art, brass(np.maximum(ch, links), W, H, cx, 100, nx()))
    cap = poly(W, H, [(cx - 30, 160), (cx + 30, 160), (cx + 16, 140), (cx - 16, 140)])
    art = over(art, brass(cap, W, H, cx, 30, nx()))
    # lamp: flaring neck, bulbous body, foot

    def r_of(y):
        if y < 470:  # neck flares outward toward the top rim
            t = (y - 380) / 90
            return 118 - 50 * t ** 0.7
        if y < 650:  # body
            t = (y - 470) / 180
            return 68 + 62 * math.sin(math.pi * t) ** 0.9 - 4 * t
        t = (y - 650) / 70  # foot
        return 64 - 24 * t if t < 0.5 else 52 + 16 * (t - 0.5)
    ys = np.linspace(380, 720, 70)
    pr = [(cx + r_of(y), y) for y in ys]
    pl = [(cx - r_of(y), y) for y in ys[::-1]]
    body = poly(W, H, pr + pl, smooth=True)
    halo = glow(body * ygrad(W, H, 470, 520), "#ffb862", radius=40, strength=0.4)
    art = over(halo, art)
    art = over(art, brass(body, W, H, cx, 130, nx()))
    # inner light glowing through the body's lower part
    lit = body * ygrad(W, H, 480, 560) * (1 - ygrad(W, H, 640, 660))
    art = over(art, flat(lit * radial(W, H, cx - 10, 590, 120), "#ffd27a", 0.35))
    # enamel bands: blue band on the neck with roundels, red band on the body shoulder, gilt dots
    nb = body * ygrad(W, H, 398, 402) * (1 - ygrad(W, H, 446, 450))
    art = over(art, gouache_paint(nb, ENAMEL_B, "#244b72", seed=nx(), rough=0.4))
    rnd = circles(W, H, [(cx + dx, 424, 13) for dx in (-60, -20, 20, 60)]) * nb
    art = over(art, gouache_paint(rnd, ENAMEL_R, seed=nx(), rough=0.3))
    art = over(art, flat(circles(W, H, [(cx + dx, 424, 5) for dx in (-60, -20, 20, 60)]) * nb, BRASS_L))
    sb = body * ygrad(W, H, 520, 524) * (1 - ygrad(W, H, 556, 560))
    art = over(art, gouache_paint(sb, ENAMEL_R, "#8a2a24", seed=nx(), rough=0.4))
    lz = shapes(W, H, [[(x, 540), (x + 9, 526), (x + 18, 540), (x + 9, 554)] for x in np.arange(cx - 130, cx + 130, 22)], smooth=False) * sb
    art = over(art, gouache_paint(lz, ENAMEL_B, seed=nx(), rough=0.3))
    gd = circles(W, H, [(x, 512, 2.6) for x in np.arange(cx - 120, cx + 124, 12)] + [(x, 568, 2.6) for x in np.arange(cx - 120, cx + 124, 12)]) * body
    art = over(art, flat(gd, "#fff0b8", 0.9))
    # handles (small loops) on the body
    hl = np.clip(ellipses(W, H, [(cx + dx, 500, 10, 13, 0) for dx in (-104, -40, 40, 104)]) - ellipses(W, H, [(cx + dx, 500, 6, 9, 0) for dx in (-104, -40, 40, 104)]), 0, 1)
    art = over(art, brass(hl, W, H, cx, 130, nx()))
    # cylindrical shade over enamel to sit on the curved body
    xx = np.abs(np.arange(W)[None, :] - cx) / 130.0 * np.ones((H, 1))
    art[..., :3] *= np.clip(1 - 0.35 * xx ** 2, 0.55, 1)[..., None]
    preview(art, "mk-lamp", bg="#3b302c")
    save(art, f"{OUT}/lamp.webp", max_w=200, quality=84)
    clear()


def part_divider():
    """Joggled voussoir strip: interlocking light/dark stones with a pointed-arch keystone in the centre."""
    W, H = 640, 90
    nx = Seq(700)
    art = blank(W, H)
    n = 9
    jw = 64
    x0 = (W - n * jw) / 2
    for k in range(n):
        x = x0 + k * jw
        col = "#f0e0bd" if k % 2 == 0 else (RUST if k % 4 == 1 else BASALT)
        # jigsaw tab profile on the right edge (bulb shape)
        pts = [(x, 18), (x + jw, 18), (x + jw, 34)]
        if k < n - 1:
            pts += [(x + jw + 10, 30), (x + jw + 16, 45), (x + jw + 10, 60)]
        pts += [(x + jw, 56), (x + jw, 72), (x, 72), (x, 56)]
        if k > 0:
            pts += [(x + 10, 60), (x + 16, 45), (x + 10, 30)]
        pts += [(x, 34)]
        m = poly(W, H, pts, smooth=False)
        art = over(art, stone(W, H, m, col, mix_hex(col, "#000000", 0.1), nx(), rough=0.5))
        e = strokes(W, H, [([p, pts[(i + 1) % len(pts)]], 1.4, None) for i, p in enumerate(pts)])
        art = over(art, flat(e, "#6d5640", 0.6))
    preview(art, "mk-divider", tone="#efe2c8")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=84)
    clear()


def part_rosette():
    """Carved stone roundel: 12-point star with radiating kite cells, raised in relief."""
    W = H = 260
    nx = Seq(900)
    cx = cy = 130
    disc = circles(W, H, [(cx, cy, 118)])
    art = over(blank(W, H), stone(W, H, disc, "#e6d0a6", "#d8bf93", nx()))
    cv = Canvas(W, H)
    p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=5)
    star = [(cx + math.cos(k * math.pi / 12 - math.pi / 2) * (58 if k % 2 == 0 else 38), cy + math.sin(k * math.pi / 12 - math.pi / 2) * (58 if k % 2 == 0 else 38)) for k in range(24)]
    cv.c.drawPath(poly_path(star), p)
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        cv.c.drawLine(cx + math.cos(a) * 58, cy + math.sin(a) * 58, cx + math.cos(a) * 104, cy + math.sin(a) * 104, p)
        a2 = a + math.pi / 12
        cv.c.drawLine(cx + math.cos(a2) * 38, cy + math.sin(a2) * 38, cx + math.cos(a2 + 0.12) * 84, cy + math.sin(a2 + 0.12) * 84, p)
    cv.c.drawCircle(cx, cy, 104, p)
    cv.c.drawCircle(cx, cy, 16, p)
    m = cv.array()[..., 3] * disc
    hgt = gaussian_filter(m, 1.5)
    gy, gx = np.gradient(hgt)
    light = np.clip(0.5 - (gx * 0.8 + gy) * 8, 0, 1)
    art = over(art, flat(np.clip(m, 0, 1) * light, "#fbf0d6", 0.7))
    art = over(art, flat(np.clip(m, 0, 1) * (1 - light), "#7e6040", 0.6))
    recess = disc * (1 - gaussian_filter(m, 2.5) * 2).clip(0, 1) * radial(W, H, cx, cy, 120) * 0.0
    art = over(art, flat(np.clip(gaussian_filter(disc, 2) - circles(W, H, [(cx, cy, 112)]), 0, 1), "#6e5640", 0.6))
    preview(art, "mk-rosette", tone="#efe2c8")
    save(art, f"{OUT}/rosette.webp", max_w=120, quality=84)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
