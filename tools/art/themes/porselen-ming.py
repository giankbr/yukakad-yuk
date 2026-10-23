"""Porselen Ming — original blue-and-white porcelain in a Ming-inspired manner: cobalt underglaze brushwork (outlines
plus graded washes, 'heaped and piled' dark specks) under a glassy white glaze with fine crackle. Peony sprays,
ruyi clouds, crashing-wave borders, lotus-panel bands; a charger plate and a meiping vase.
Run: python3 -I porselen-ming.py [part ...]  parts: glaze plate vase wave cloud ring
Assets -> public/themes/art/porselen-ming/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _n4_lib import *

OUT = outdir("porselen-ming")
PARTS = sys.argv[1:] or ["glaze", "plate", "vase", "wave", "cloud", "ring"]
DARK, MID, LIGHT = "#1b3480", "#2f56a6", "#7d9bd6"
WHITE, WHITE_D = "#f6f7f3", "#e3e7e6"


def line_items(pts, w):
    return (pts, w, (0.08, 0.12))


def ink(art, W, H, items, seed, col=DARK, light=MID, density=0.95):
    if not items:
        return art
    return CB(art, strokes(W, H, items), seed, dark=col, light=light, density=density, rough=0.8, heap=0.6, feather=0.5)


def wash(art, mask, seed, density=0.55, light=LIGHT, dark=MID):
    return CB(art, mask, seed, dark=dark, light=light, density=density, rough=1.6, heap=0.35, feather=1.0)


def glaze_white(W, H, seed, mask=None, tint=WHITE):
    """Glassy white body with faint blue-grey pooling and crackle."""
    rgb = np.ones((H, W, 3), np.float32) * col3(tint)
    n = fbm(W, H, seed, 90, 3)
    rgb = rgb * (0.985 + 0.03 * n[..., None]) - (1 - n[..., None]) * 0.02 * np.array([0.5, 0.3, 0.0], np.float32)
    cr = crackle(W, H, seed + 1, 60, wrap=False) if mask is not None else crackle(W, H, seed + 1, 60)
    rgb = rgb * (1 - cr[..., None] * 0.09) + col3("#b9c2c8") * cr[..., None] * 0.04
    a = np.ones((H, W), np.float32) if mask is None else mask
    return rgba(rgb, a)


def glaze():
    W = H = 384
    rgb = np.ones((H, W, 3), np.float32) * col3("#f3f4f0")
    n = wrap_noise(W, H, 3, 50)
    rgb = rgb * (0.985 + 0.025 * n[..., None])
    cr = crackle(W, H, 7, 70)
    rgb = rgb * (1 - cr[..., None] * 0.1) + col3("#a9b3bb") * cr[..., None] * 0.05
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/glaze.webp", quality=74)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/pm-glaze.png")


# ---------------------------------------------------------------- motifs
def peony(art, W, H, cx, cy, r, nx, tilt=0.78, rot=0.0):
    """Side-view peony bloom: back fan of large scalloped petals, a darker heart, cupped front petals. Each petal gets
    a graded cobalt wash (deeper at the base, white reserve at the scalloped edge) and a dark brush outline."""
    rng = random.Random(nx())
    bx, by = cx, cy + r * 0.42
    rows = [(5, -2.75, -0.39, 1.0, 0.56, 0.0), (4, -2.45, -0.69, 0.8, 0.5, 0.1), (3, -2.05, -1.09, 0.56, 0.52, 0.35)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - bx) ** 2 + (yy - by) ** 2) / r
    for k, (n, a0, a1, L, wd, cup) in enumerate(rows):
        if k == 2:
            heart = shapes(W, H, [ellipse_pts(bx, by - r * 0.5, r * 0.34, r * 0.18, 14)])
            art = wash(art, heart, nx(), density=0.95, light=MID, dark=DARK)
        for i in range(n):
            a = a0 + (a1 - a0) * (i / max(1, n - 1)) + rng.uniform(-0.05, 0.05) + rot
            LL = r * L * rng.uniform(0.92, 1.06)
            px = bx + math.cos(a) * LL * 0.5; py = by + math.sin(a) * LL * 0.5 * (1 if k < 2 else 0.8)
            pts = petal_pts(px, py, LL * 0.58, LL * wd, a, n=22, cup=cup)
            # scalloped outer edge: bumps on the half of the outline away from the base
            out = []
            for j, (x, y) in enumerate(pts):
                d = math.hypot(x - bx, y - by) / (LL + 1e-6)
                bump = math.sin(j * 2.3 + i) * r * 0.045 * max(0, d - 0.55) * 2
                nxv, nyv = (x - px), (y - py); nl = math.hypot(nxv, nyv) + 1e-6
                out.append((x + nxv / nl * bump, y + nyv / nl * bump))
            out = deform(out, rng, 1, 0.04)
            pm = shapes(W, H, [out])
            grad = np.clip(1.05 - dist / (L * 1.05), 0, 1) ** 0.8
            reserve = np.clip(gaussian_filter(pm, r * 0.035) * 1.6 - 0.45, 0, 1)
            art = wash(art, pm * reserve * (0.25 + 0.75 * grad), nx(), density=0.75)
            # vein strokes from the base
            vs = [line_items([(bx + (px - bx) * 0.2, by + (py - by) * 0.2), (px + math.cos(a) * LL * 0.25, py + math.sin(a) * LL * 0.25)], max(1, r * 0.012))]
            art = ink(art, W, H, [line_items(out + [out[0]], max(1.3, r * 0.022))] + vs, nx())
    return art


def leaf(art, W, H, x, y, L, a, nx, curl=0.2):
    """Peony leaf: three slender pointed lobes from one point, graded wash with a white-reserved midrib, toothed
    edge, dark outline."""
    rng = random.Random(nx())
    polys = []; ribs = []
    for da, sc in [(0, 1.0), (-0.75, 0.7), (0.75, 0.7)]:
        aa = a + da + rng.uniform(-0.08, 0.08)
        pts = petal_pts(x, y, L * sc, L * sc * 0.17, aa, n=28, cup=curl * (1 if da >= 0 else -1))
        pts = [(px + math.cos(j * 3.1) * L * 0.012, py + math.sin(j * 3.1) * L * 0.012) for j, (px, py) in enumerate(pts)]
        polys.append(deform(pts, rng, 1, 0.02))
        ribs.append(line_items([(x, y), (x + math.cos(aa) * L * sc * 0.85, y + math.sin(aa) * L * sc * 0.85)], max(1.2, L * 0.028)))
    m = shapes(W, H, polys)
    vm = strokes(W, H, ribs)
    art = wash(art, np.clip(m - vm, 0, 1), nx(), density=0.8, light=MID, dark=DARK)
    art = ink(art, W, H, [line_items(p + [p[0]], max(1.2, L * 0.022)) for p in polys], nx())
    return art


def ruyi(W, H, x, y, s, flip=1):
    """Ruyi cloud: three-lobed head curling into a spiral, with a trailing double tail. Returns stroke items."""
    items = []
    def P(u, v):
        return (x + u * s * flip, y + v * s)
    head = [P(-0.1, 0.1), P(-0.35, 0.0), P(-0.38, -0.25), P(-0.2, -0.4), P(0.0, -0.32), P(0.1, -0.5), P(0.32, -0.48), P(0.42, -0.28), P(0.62, -0.25), P(0.7, -0.02), P(0.5, 0.14), P(0.2, 0.16), P(-0.1, 0.1)]
    items.append(line_items(curve(head, 60), s * 0.045))
    sp = spiral_pts(0, 0, s * 0.14, s * 0.02, 0, 1.2, 30, flip)
    hx, hy = P(0.16, -0.12)
    items.append(line_items([(px + hx, py + hy) for px, py in sp], s * 0.035))
    for k in range(2):
        tail = curve([P(0.6, 0.06 + k * 0.08), P(0.95, 0.12 + k * 0.1), P(1.25, 0.0 + k * 0.1), P(1.6, 0.08 + k * 0.08)], 30)
        items.append(line_items(tail, s * (0.04 - k * 0.012)))
    return items, head


def waves(W, H, y0, y1, period, nx_seed, x0=0, x1=None):
    """Crashing-wave border lines: rows of crests curling into small spirals, with parallel trough lines."""
    x1 = x1 if x1 is not None else W
    items = []
    hgt = y1 - y0
    for xc in np.arange(x0 - period, x1 + period, period):
        base = y1
        crest = curve([(xc, base), (xc + period * 0.25, base - hgt * 0.55), (xc + period * 0.55, base - hgt * 0.92), (xc + period * 0.8, base - hgt * 0.7)], 30)
        sp = spiral_pts(0, 0, hgt * 0.22, hgt * 0.04, -math.pi / 2, 0.9, 20, 1)
        ex, ey = crest[-1]
        crest += [(px + ex - sp[0][0], py + ey - sp[0][1]) for px, py in sp]
        items.append((crest, max(1.3, hgt * 0.06), (0.05, 0.3)))
        for k in range(1, 4):
            off = k * hgt * 0.16
            par = curve([(xc + period * 0.1 + off * 0.4, base), (xc + period * 0.3 + off * 0.3, base - hgt * 0.5 + off), (xc + period * 0.55, base - hgt * 0.85 + off * 1.2)], 20)
            items.append((par, max(1.0, hgt * 0.035), (0.1, 0.3)))
    return items


def lotus_panels(W, H, cx, cy, r0, r1, n):
    """Ring of lotus-petal panels (lianban) between radii r0<r1: outlines + inner line + small ruyi tip."""
    items = []
    for i in range(n):
        a0 = i * math.tau / n; a1 = (i + 1) * math.tau / n; am = (a0 + a1) / 2
        pts = []
        for t in np.linspace(0, 1, 14):
            a = a0 + (a1 - a0) * t
            pts.append((cx + math.cos(a) * r0, cy + math.sin(a) * r0))
        tip = (cx + math.cos(am) * r1, cy + math.sin(am) * r1)
        c1 = (cx + math.cos(a1) * (r0 + (r1 - r0) * 0.55), cy + math.sin(a1) * (r0 + (r1 - r0) * 0.55))
        c0 = (cx + math.cos(a0) * (r0 + (r1 - r0) * 0.55), cy + math.sin(a0) * (r0 + (r1 - r0) * 0.55))
        outline = curve([pts[-1], c1, tip, c0, pts[0]], 30)
        items.append((outline, 2.0, None))
        inner = [((cx + (x - cx) * 0.0 + (x - cx)) , y) for x, y in []]
        k = 0.78
        rm = r0 + (r1 - r0) * 0.12
        ic = curve([(cx + math.cos(a1 - 0.08) * rm, cy + math.sin(a1 - 0.08) * rm), (cx + math.cos(a1 - 0.05) * (r0 + (r1 - r0) * 0.5), cy + math.sin(a1 - 0.05) * (r0 + (r1 - r0) * 0.5)),
                    (cx + math.cos(am) * (r0 + (r1 - r0) * k), cy + math.sin(am) * (r0 + (r1 - r0) * k)),
                    (cx + math.cos(a0 + 0.05) * (r0 + (r1 - r0) * 0.5), cy + math.sin(a0 + 0.05) * (r0 + (r1 - r0) * 0.5)), (cx + math.cos(a0 + 0.08) * rm, cy + math.sin(a0 + 0.08) * rm)], 30)
        items.append((ic, 1.3, (0.1, 0.1)))
    return items


def ring_line(W, H, cx, cy, r, w):
    return ring_mask(W, H, cx, cy, r, w)


# ---------------------------------------------------------------- pieces
def plate():
    """Charger plate seen from above: wave rim, lotus-panel cavetto, peony spray with garden rock and ruyi cloud."""
    W = H = 700
    cx = cy = 350
    R = 330
    nx = Seq(4100)
    body = circles(W, H, [(cx, cy, R)])
    art = blank(W, H)
    # drop shadow
    art = over(art, soft_shadow(body, "#1b2a4a", 14, 0.35, 6, 12))
    art = over(art, glaze_white(W, H, 11, body))
    # rim shading (the well is slightly lower)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    well = np.clip(1 - np.abs(rr - 262) / 14, 0, 1) * body
    art = over(art, flat(well, "#9aa6b3", 0.18))
    # --- rim: crashing waves between 270..322
    rim = np.clip(body - circles(W, H, [(cx, cy, 272)]), 0, 1)
    wv = []
    for k in range(52):
        a = k * math.tau / 52
        # build one wave unit in local coords then rotate around centre
        unit = waves(80, 60, 6, 52, 52, 0, 0, 52)
        for pts, w, t in unit[:4]:
            out = []
            for px, py in pts:
                ang = a + (px - 26) / 296
                rad = 320 - py
                out.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
            wv.append((out, w * 0.9, t))
    art = wash(art, rim * np.clip((rr - 300) / 20, 0, 1) * 0 + np.clip(1 - np.abs(rr - 314) / 7, 0, 1) * body, nx(), density=0.5)
    art = ink(art, W, H, wv, nx())
    art = ink(art, W, H, [], nx())
    lines = np.clip(ring_line(W, H, cx, cy, 324, 2.6) + ring_line(W, H, cx, cy, 270, 3.0) + ring_line(W, H, cx, cy, 262, 1.6), 0, 1)
    art = CB(art, lines, nx(), dark=DARK, light=MID, density=0.95, rough=0.5, heap=0.5, feather=0.5)
    # --- cavetto: lotus panels 196..256
    lp = lotus_panels(W, H, cx, cy, 200, 254, 12)
    art = ink(art, W, H, lp, nx())
    band = np.clip(circles(W, H, [(cx, cy, 254)]) - circles(W, H, [(cx, cy, 200)]), 0, 1)
    art = wash(art, band * 0.55, nx(), density=0.35)
    lines2 = np.clip(ring_line(W, H, cx, cy, 196, 2.6) + ring_line(W, H, cx, cy, 188, 1.4), 0, 1)
    art = CB(art, lines2, nx(), dark=DARK, light=MID, density=0.95, rough=0.5, heap=0.5, feather=0.5)
    # --- centre medallion
    clip = circles(W, H, [(cx, cy, 182)])
    med = blank(W, H)
    # stems
    stems = [line_items(curve([(cx - 60, cy + 175), (cx - 30, cy + 100), (cx - 6, cy + 40), (cx + 4, cy + 10)], 30), 3.2),
             line_items(curve([(cx - 30, cy + 110), (cx - 90, cy + 60), (cx - 120, cy - 10)], 20), 2.6),
             line_items(curve([(cx - 10, cy + 60), (cx + 60, cy + 70), (cx + 120, cy + 40)], 20), 2.4)]
    med = ink(med, W, H, stems, nx())
    for (x, y, L, a) in [(cx - 40, cy + 120, 70, 2.5), (cx + 30, cy + 90, 72, 0.4), (cx - 100, cy + 40, 64, 3.6), (cx + 100, cy + 52, 60, -0.3), (cx - 10, cy + 150, 54, 1.4)]:
        med = leaf(med, W, H, x, y, L, a, nx)
    med = peony(med, W, H, cx + 6, cy - 40, 104, nx)
    med = peony(med, W, H, cx - 118, cy - 40, 46, nx, rot=-0.35)
    # bud on the right
    med = peony(med, W, H, cx + 126, cy + 2, 36, nx, rot=0.4)
    # small ruyi cloud top-left
    ci, chead = ruyi(W, H, cx - 112, cy - 118, 58, 1)
    med = wash(med, shapes(W, H, [curve(chead, 50)]), nx(), density=0.4)
    med = ink(med, W, H, ci, nx())
    med[..., 3] *= clip
    art = over(art, med)
    # glaze: softens the cobalt slightly, adds sheen
    sheen = np.exp(-(((xx - cx + 110) / 140) ** 2 + ((yy - cy + 150) / 60) ** 2)) * body
    art = over(art, flat(sheen, "#ffffff", 0.35))
    cr = crackle(W, H, 19, 70, wrap=False) * body
    art[..., :3] = art[..., :3] * (1 - cr[..., None] * 0.06)
    art[..., 3] = np.where(art[..., 3] < 0.04, 0, art[..., 3])
    preview(art, "pm-plate", tone="#eef0ee")
    save(art, f"{OUT}/plate.webp", max_w=640, quality=80)


def vase():
    """Meiping vase: small mouth, broad shoulder with ruyi collar, peony scroll belly, lotus panels at the foot."""
    W, H = 420, 680
    cx = W / 2
    nx = Seq(5200)
    prof = [(0, 30), (22, 30), (24, 48), (36, 58), (90, 80), (150, 120), (178, 190), (176, 290), (150, 430), (118, 560), (104, 630), (108, 650)]
    right = [(cx + x, y) for x, y in prof]
    left = [(cx - x, y) for x, y in reversed(prof)]
    body = shapes(W, H, [right + left], smooth=True)
    art = blank(W, H)
    art = over(art, soft_shadow(body, "#1b2a4a", 12, 0.3, 8, 10))
    art = over(art, glaze_white(W, H, 21, body))
    # roundness: darker towards the sides
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    half = np.interp(yy[:, 0], [p[1] for p in prof], [p[0] for p in prof])[:, None]
    u = np.clip(np.abs(xx - cx + 20) / np.maximum(half, 1), 0, 1)
    art = over(art, flat(body * u ** 3, "#7f8ea3", 0.35))
    # --- shoulder band: ruyi collar lappets 80..170
    items = []
    for k in range(-3, 4):
        x0 = cx + k * 52
        hx = x0
        lap = curve([(hx - 26, 92 + abs(k) * 6), (hx - 30, 130 + abs(k) * 4), (hx - 10, 150), (hx, 168 - abs(k) * 3), (hx + 10, 150), (hx + 30, 130 + abs(k) * 4), (hx + 26, 92 + abs(k) * 6)], 40)
        items.append(line_items(lap, 2.2))
        lapm = shapes(W, H, [lap]) * body
        art = wash(art, lapm * np.clip(gaussian_filter(lapm, 4) * 1.5 - 0.3, 0, 1), nx(), density=0.55)
        art = ink(art, W, H, [line_items(spiral_pts(hx, 128 + abs(k) * 3, 7, 1.5, -math.pi / 2, 1.0, 16, 1), 1.6)], nx())
    collar_m = shapes(W, H, [[(x, y) for x, y, _ in []]]) if False else None
    sh = np.clip((yy > 84) * (yy < 170), 0, 1) * body
    art = wash(art, sh * 0.0 + np.clip(1 - np.abs(yy - 126) / 34, 0, 1) * body * 0.3, nx(), density=0.3)
    tmpc = ink(blank(W, H), W, H, items, nx())
    tmpc[..., 3] *= body
    art = over(art, tmpc)
    lines = []
    for y in (82, 176, 534, 546):
        hw = float(np.interp(y, [p[1] for p in prof], [p[0] for p in prof]))
        lines.append(line_items([(cx - hw + 3, y), (cx - hw * 0.5, y + 3), (cx, y + 4), (cx + hw * 0.5, y + 3), (cx + hw - 3, y)], 2.4))
    art = ink(art, W, H, lines, nx())
    # --- belly: peony scroll
    med = blank(W, H)
    scroll = [line_items(curve([(cx - 190, 380), (cx - 110, 300), (cx - 30, 360), (cx + 50, 420), (cx + 130, 330), (cx + 200, 300)], 60), 3.0)]
    med = ink(med, W, H, scroll, nx())
    for (x, y, L, a) in [(cx - 120, 310, 52, -2.4), (cx - 70, 370, 50, 1.6), (cx + 30, 430, 50, 1.0), (cx + 120, 352, 52, -0.8), (cx - 160, 370, 44, 2.2), (cx + 160, 312, 42, -1.6)]:
        med = leaf(med, W, H, x, y, L, a, nx)
    med = peony(med, W, H, cx - 30, 300, 74, nx)
    med = peony(med, W, H, cx + 100, 420, 56, nx)
    ci, chead = ruyi(W, H, cx - 140, 230, 40, 1)
    med = wash(med, shapes(W, H, [curve(chead, 40)]), nx(), density=0.4)
    med = ink(med, W, H, ci, nx())
    med[..., 3] *= body * ((yy > 182) & (yy < 528))
    art = over(art, med)
    # --- foot: lotus panels
    fp = []
    for k in range(-3, 4):
        x0 = cx + k * 40
        fp.append(line_items(curve([(x0 - 18, 628), (x0 - 18, 590), (x0, 556), (x0 + 18, 590), (x0 + 18, 628)], 30), 2.0))
        fp.append(line_items(curve([(x0 - 9, 624), (x0 - 9, 598), (x0, 576), (x0 + 9, 598), (x0 + 9, 624)], 20), 1.2))
    fm = body * ((yy > 548) & (yy < 640))
    tmp = ink(blank(W, H), W, H, fp, nx())
    tmp[..., 3] *= fm
    art = over(art, tmp)
    # mouth rim
    art = ink(art, W, H, [line_items([(cx - 22, 34), (cx + 22, 34)], 3.2), line_items([(cx - 24, 50), (cx + 24, 50)], 2.0)], nx())
    # glaze sheen: long vertical highlight on the left shoulder
    sheen = np.exp(-(((xx - cx + 70) / 18) ** 2 + ((yy - 250) / 120) ** 2)) * body
    art = over(art, flat(sheen, "#ffffff", 0.55))
    sheen2 = np.exp(-(((xx - cx + 40) / 40) ** 2 + ((yy - 120) / 22) ** 2)) * body
    art = over(art, flat(sheen2, "#ffffff", 0.45))
    art[..., 3] = np.where(art[..., 3] < 0.04, 0, art[..., 3])
    preview(art, "pm-vase", tone="#eef0ee")
    save(art, f"{OUT}/vase.webp", max_w=360, quality=80)


def wave():
    """Seamless repeat-x border of crashing waves between two cobalt lines, 384x64."""
    W, H = 384, 64
    art = blank(W, H)
    nx = Seq(6100)
    items = waves(W, H, 12, 54, 48, 0, 0, W)
    items = [(pts, w, t) for pts, w, t in items]
    wrapped = []
    for pts, w, t in items:
        for dx in (-W, 0, W):
            wrapped.append(([(x + dx, y) for x, y in pts], w, t))
    art = ink(art, W, H, wrapped, nx())
    bl = strokes(W, H, [([(-10, 5), (W + 10, 5)], 3, None), ([(-10, 59), (W + 10, 59)], 3, None)])
    art = CB(art, bl, nx(), dark=DARK, light=MID, density=0.95, rough=0.3, heap=0.4, feather=0.4)
    save_full(art, f"{OUT}/wave.webp", quality=82)
    preview(art, "pm-wave", tone="#f3f4f0")


def cloud():
    W, H = 300, 170
    nx = Seq(7100)
    art = blank(W, H)
    ci, chead = ruyi(W, H, 70, 110, 120, 1)
    art = wash(art, shapes(W, H, [curve(chead, 50)]), nx(), density=0.45)
    art = ink(art, W, H, ci, nx())
    preview(art, "pm-cloud", tone="#f3f4f0")
    save(art, f"{OUT}/cloud.webp", max_w=220, quality=84)


def ring():
    """Plate rim as a frame: glazed ring with wave border and double lines; the centre is transparent for a photo."""
    W = H = 600
    cx = cy = 300
    nx = Seq(8100)
    outer = circles(W, H, [(cx, cy, 292)])
    hole = circles(W, H, [(cx, cy, 236)])
    body = np.clip(outer - hole, 0, 1)
    art = blank(W, H)
    art = over(art, glaze_white(W, H, 31, body))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    wv = []
    for k in range(44):
        a = k * math.tau / 44
        unit = waves(80, 60, 6, 46, 46, 0, 0, 46)
        for pts, w, t in unit[:4]:
            out = []
            for px, py in pts:
                ang = a + (px - 23) / 262
                rad = 284 - py * 0.95
                out.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
            wv.append((out, w * 0.9, t))
    art = ink(art, W, H, wv, nx())
    lines = np.clip(ring_line(W, H, cx, cy, 288, 2.6) + ring_line(W, H, cx, cy, 240, 3.0) + ring_line(W, H, cx, cy, 248, 1.4), 0, 1)
    art = CB(art, lines, nx(), dark=DARK, light=MID, density=0.95, rough=0.5, heap=0.5, feather=0.5)
    art[..., 3] *= np.clip(outer, 0, 1)
    art[..., 3] *= np.clip(rr - 236, 0, 1)
    sheen = np.exp(-(((xx - cx + 120) / 90) ** 2 + ((yy - cy + 200) / 40) ** 2)) * body
    art = over(art, flat(sheen, "#ffffff", 0.4))
    preview(art, "pm-ring", tone="#d8dee8")
    save(art, f"{OUT}/ring.webp", max_w=480, quality=80)


for p in PARTS:
    globals()[p]()
    clear()
