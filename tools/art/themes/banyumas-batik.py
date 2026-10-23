"""Banyumas Batik — batik Banyumasan sogan-hitam with Gunung Slamet, coconut groves and the Serayu river.
Watercolour landscape (indigo-grey volcano, olive sawah, sogan palms), a seamless dark batik tile (lumbon leaves,
jahe srimpang rhizomes, cecek dots, wax crackle), a lumbon leaf ornament, a jahe-srimpang sprig divider and a
single palm. Run: python3 -I banyumas-batik.py [part ...]  parts: slamet batik lumbon jahe palm"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _k1_lib import *  # noqa
from scipy.ndimage import map_coordinates

OUT = outdir("banyumas-batik")
PARTS = sys.argv[1:] or ["slamet", "batik", "lumbon", "jahe", "palm"]
SOGAN, SOGAN_D, SOGAN_L = "#7a4a24", "#4a2a14", "#a8743e"
BLACK = "#1c1612"
CREAM = "#efe3c8"
INDIGO, INDIGO_L = "#3c4658", "#7d8796"
OLIVE, OLIVE_D = "#7d8a4e", "#4f5a2e"
GOLD = "#c49a52"


def palm_masks(W, H, x, by, h, rng, lean):
    """Coconut palm: curved tapering trunk with ring scars, a crown of drooping feathered fronds, coconuts."""
    top = (x + lean * h, by - h)
    trunk = curve([(x, by), (x + lean * h * 0.15, by - h * 0.45), (x + lean * h * 0.6, by - h * 0.8), top], 40)
    tw = max(3.0, h * 0.03)
    tr = strokes(W, H, [(trunk, tw, (0.0, 0.9))])
    rings = []
    for i in range(2, len(trunk) - 2, 2):
        (x0, y0), (x1, y1) = trunk[i - 1], trunk[i + 1]
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        ww = tw * (0.5 + 0.5 * (1 - i / len(trunk)))
        rings.append(([(trunk[i][0] - math.cos(a) * ww * 0.5, trunk[i][1] - math.sin(a) * ww * 0.5), (trunk[i][0] + math.cos(a) * ww * 0.5, trunk[i][1] + math.sin(a) * ww * 0.5)], 1.0, None))
    rib, leaflets, polys = [], [], []
    nf = 9
    for k in range(nf):
        a = -math.pi / 2 + (k - (nf - 1) / 2) * 0.42 + rng.uniform(-0.1, 0.1)
        side_k = abs(k - (nf - 1) / 2) / ((nf - 1) / 2)
        L = h * rng.uniform(0.3, 0.38) * (0.7 + 0.3 * side_k)
        droop = L * (0.15 + 0.9 * side_k ** 1.4)
        pts = curve([top, (top[0] + math.cos(a) * L * 0.4, top[1] + math.sin(a) * L * 0.4 - L * 0.1),
                     (top[0] + math.cos(a) * L * 0.8, top[1] + math.sin(a) * L * 0.8 + droop * 0.45),
                     (top[0] + math.cos(a) * L * 0.92, top[1] + math.sin(a) * L * 0.92 + droop)], 34)
        rib.append((pts, max(1.4, h * 0.008), (0.05, 0.4)))
        # frond silhouette: rib on top, a serrated curtain of leaflets hanging below it
        upper, lower = [], []
        for j in range(1, 34):
            px, py = pts[j]; qx, qy = pts[min(33, j + 1)]
            da = math.atan2(qy - py, qx - px)
            env = math.sin(math.pi * min(1, (j + 1) / 34)) ** 0.6
            ll = L * 0.3 * env * rng.choice([rng.uniform(0.8, 1.05), rng.uniform(0.45, 0.8), rng.uniform(0.25, 0.5)])
            nxn, nyn = -math.sin(da), math.cos(da)
            if nyn < 0:
                nxn, nyn = -nxn, -nyn
            hx, hy = nxn * 0.35 + math.cos(da) * 0.25, nyn * 0.35 + 0.9
            d = math.hypot(hx, hy)
            lower.append((px + hx / d * ll, py + hy / d * ll))
            upper.append((px - nxn * h * 0.006 * env, py - nyn * h * 0.006 * env))
            if j % 3 == 0:
                leaflets.append(([(px, py), (px + hx / d * ll * 0.5, py + hy / d * ll * 0.5 + 1), (px + hx / d * ll * 0.95, py + hy / d * ll * 0.95)], max(1.0, h * 0.004), (0.0, 0.9)))
        polys.append([top] + upper + lower[::-1])
    nuts = circles(W, H, [(top[0] + dx * h * 0.02, top[1] + h * 0.03 + dy * h * 0.015, h * 0.022) for dx, dy in [(-1, 0), (0.6, 0.4), (0.1, 1.1)]])
    fr = np.maximum(shapes(W, H, polys, smooth=False), strokes(W, H, rib + leaflets))
    return tr, strokes(W, H, rings), fr, nuts


def palm_wash(art, W, H, x, by, h, rng, nx, lean, col=SOGAN_D, col2=BLACK, dens=0.8):
    tr, rings, fr, nuts = palm_masks(W, H, x, by, h, rng, lean)
    art = G(art, fr, col, col2, seed=nx(), density=min(1, dens * 1.1), edge=0.3, bloom=0.25, rough=1.8, feather=0.7, mottle=0.35)
    art = G(art, tr, col, col2, seed=nx(), density=dens, edge=0.55, bloom=0.1, rough=1.2, feather=0.6)
    if h > 200:
        art = G(art, rings * tr, BLACK, seed=nx(), density=0.5, edge=0, bloom=0, rough=0.4, feather=0.4)
        art = G(art, nuts, "#5a3a1a", BLACK, seed=nx(), density=0.85, edge=0.5, bloom=0, rough=1)
    return art


# ------------------------------------------------------------------ landscape
if "slamet" in PARTS:
    W, H = 780, 640
    nx = Seq(20100); rng = random.Random(4)
    art = blank(W, H)
    # sky wash (warm cream to pale peach toward the horizon) + a few cloud blooms
    sky = shapes(W, H, [[(-10, -10), (W + 10, -10), (W + 10, 420), (-10, 420)]], smooth=False)
    art = G(art, sky, "#ecdcc0", "#f1d9b4", seed=nx(), density=0.55, edge=0.15, bloom=0.5, rough=10, feather=3)
    for (cx, cy, rx, ry) in [(170, 92, 120, 22), (600, 66, 150, 20), (430, 140, 90, 14)]:
        c = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 12), rng, 3, 0.18)])
        art = G(art, c, "#fbf3e3", seed=nx(), density=0.5, edge=0.2, bloom=0.4, rough=8, feather=4)
    # Gunung Slamet: very broad cone, flattened top; far ridge first
    far = shapes(W, H, [[(-20, 380), (120, 330), (260, 300), (360, 250), (420, 244), (520, 290), (680, 320), (800, 350), (800, 420), (-20, 420)]])
    art = G(art, far, "#b9b6b0", "#a7a9ae", seed=nx(), density=0.45, edge=0.35, bloom=0.3, rough=6)
    mt = [(-20, 420), (60, 392), (170, 330), (270, 250), (330, 186), (366, 150), (396, 140), (432, 142), (462, 156), (500, 196), (560, 262), (650, 330), (740, 374), (800, 392), (800, 440), (-20, 440)]
    mtm = shapes(W, H, [mt])
    art = G(art, mtm, INDIGO_L, INDIGO, seed=nx(), density=0.62, edge=0.55, bloom=0.35, rough=5)
    # shadowed east flank + gullies (dry-brush strokes from the crater down)
    flank = shapes(W, H, [[(400, 142), (432, 142), (462, 156), (500, 196), (560, 262), (650, 330), (740, 374), (800, 392), (800, 440), (470, 440), (440, 300)]]) * mtm
    flank = gaussian_filter(flank, 14) * mtm
    art = G(art, flank, INDIGO, "#2c3444", seed=nx(), density=0.38, edge=0.2, bloom=0.2, rough=4)
    gul = []
    for k in range(13):
        x0 = 370 + k * 6 + rng.uniform(-3, 3)
        ang = math.radians(100 + (k - 6) * 9)
        L = rng.uniform(40, 120)
        gul.append((curve([(x0, 150), (x0 + math.cos(ang) * L * 0.5 + rng.uniform(-6, 6), 150 + math.sin(ang) * L * 0.5), (x0 + math.cos(ang) * L, 150 + math.sin(ang) * L)], 14), rng.uniform(2.2, 4), (0.05, 0.6)))
    art = G(art, gaussian_filter(strokes(W, H, gul), 3.0) * mtm * 1.4, "#2c3444", seed=nx(), density=0.12, edge=0.05, bloom=0, rough=2, feather=1.5)
    # a thin plume from the crater
    plume = shapes(W, H, [deform([(396, 138), (380, 104), (392, 70), (430, 50), (470, 54), (452, 84), (430, 110), (424, 138)], rng, 2, 0.1)])
    art = G(art, plume, "#e9e3d8", "#d8d3cb", seed=nx(), density=0.55, edge=0.3, bloom=0.5, rough=6, feather=3)
    # mid hills and sawah terraces
    hm = jw.hills(W, H, 410, 22, 7, 0.7)
    art = G(art, hm, "#93a067", OLIVE, seed=nx(), density=0.7, edge=0.45, bloom=0.3, rough=5)
    terr = []
    for k in range(5):
        y = 446 + k * 30 + k * k * 3
        terr.append((curve([(-10, y + rng.uniform(-6, 8)), (200, y - 4 + k * 3), (420, y + rng.uniform(0, 10)), (640, y - rng.uniform(0, 8)), (800, y + 4)], 30), 1.6 + k * 0.3, (0.1, 0.1)))
    sawah = shapes(W, H, [[(-10, 430), (800, 420), (800, 640), (-10, 640)]], smooth=False)
    art = G(art, sawah, "#b3b874", "#9aa45c", seed=nx(), density=0.55, edge=0.3, bloom=0.35, rough=5)
    art = G(art, gaussian_filter(strokes(W, H, terr), 1.0), OLIVE_D, seed=nx(), density=0.22, edge=0.2, bloom=0, rough=2, feather=0.8)
    # river Serayu: wide bend from the foreground into the mid distance
    rv_l = curve([(330, 640), (300, 590), (360, 540), (470, 500), (520, 470), (470, 446), (400, 434)], 40)
    rv_r = curve([(520, 640), (470, 590), (510, 548), (590, 514), (600, 480), (530, 450), (412, 432)], 40)
    river = shapes(W, H, [rv_l + rv_r[::-1]])
    art = knockout(art, river, 0.85, 2)
    art = G(art, river, "#c9d2d6", "#aeb9c0", seed=nx(), density=0.5, edge=0.45, bloom=0.3, rough=3)
    refl = np.clip(river - gaussian_filter(river, 8) * 1.1 + 0.25, 0, 1) * river
    art = G(art, refl, "#8f9ca6", seed=nx(), density=0.3, edge=0.2, bloom=0.3, rough=3, feather=2)
    ripples = strokes(W, H, [(curve([(x, y), (x + 26, y + 1)], 6), 1.6, (0.3, 0.3)) for x, y in [(380, 566), (440, 540), (500, 520), (430, 600), (480, 492), (470, 460), (400, 586)]]) * river
    art = G(art, ripples, "#fbf6ec", seed=nx(), density=0.8, edge=0, bloom=0, rough=1, feather=0.5)
    # coconut groves: distant tufts along the river, then tall sogan palms framing the scene
    for x in range(20, 780, 46):
        if 300 < x < 560:
            continue
        art = palm_wash(art, W, H, x + rng.uniform(-10, 10), 440, rng.uniform(70, 96), rng, nx, rng.uniform(-0.15, 0.15), "#6c7148", "#4c5332", 0.6)
    for (x, by, h, lean) in [(70, 660, 470, 0.14), (150, 660, 360, -0.1), (700, 660, 430, -0.18), (640, 650, 300, 0.12)]:
        art = palm_wash(art, W, H, x, by, h, rng, nx, lean)
    # foreground bank
    bank = shapes(W, H, [[(-10, 600), (140, 580), (300, 610), (330, 640), (-10, 640)], [(520, 640), (560, 606), (700, 590), (800, 600), (800, 640)]])
    art = G(art, bank, OLIVE_D, SOGAN_D, seed=nx(), density=0.6, edge=0.4, bloom=0.2, rough=4)
    # fade the bottom into the page
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    art[..., 3] *= np.clip((1 - yy) / 0.14, 0, 1) ** 1.3
    prev(art, "bb-slamet", bg="#efe3c8")
    clear()
    save(art, f"{OUT}/slamet.webp", max_w=680, quality=72)


# ------------------------------------------------------------------ seamless batik tile
def wrap_disp(mask, seed, amt):
    h, w = mask.shape
    nxn = wrap_noise(w, h, seed, 6) - 0.5; nyn = wrap_noise(w, h, seed + 1, 6) - 0.5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return map_coordinates(mask, [yy + nyn * amt * 2, xx + nxn * amt * 2], order=1, mode="wrap")


def wrap_mask(n, draw):
    """draw(cv, ox, oy) at the 9 tile offsets so the geometry is periodic."""
    def d(cv):
        for ox in (-n, 0, n):
            for oy in (-n, 0, n):
                draw(cv, ox, oy)
    return mask_from(n, n, d)


def _lumbon_unit():
    pts = []
    for i in range(72):
        t = i / 72 * math.tau
        hx = 16 * math.sin(t) ** 3
        hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        y = -hy / 17.0          # point down (+1), notch up (~-0.29), lobes ~-0.6
        x = hx / 17.0 * 0.78
        if y > 0:
            y *= 1.55           # long drip tip, like a taro leaf
            x *= 1 - 0.25 * y / 1.55
        pts.append((x, y - 0.25))
    return pts


LUMBON = _lumbon_unit()
LUMBON_HUB = (0.0, -0.42)


def lumbon_veins():
    """Unit vein lines radiating from the petiole hub to the margin (taro leaves are palmately veined)."""
    out = [[LUMBON_HUB, (0.0, 1.15)]]
    for i in range(0, 72, 6):
        x, y = LUMBON[i]
        if y < -0.5 and abs(x) < 0.12:
            continue
        hx, hy = LUMBON_HUB
        out.append([(hx, hy), (hx + (x - hx) * 0.86, hy + (y - hy) * 0.86)])
    return out


def _T(cx, cy, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return lambda u, v: (cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)


def lumbon_poly(cx, cy, s, ang):
    """Taro (lumbu) leaf outline: two rounded basal lobes, notch at the petiole, long drip tip (ang=0: tip down)."""
    P = _T(cx, cy, s, ang)
    return [P(x, y) for x, y in LUMBON]


def jahe_items(cx, cy, s, ang, rng):
    """Jahe srimpang: a branching rhizome of knobby lobes (circles) with short shoots."""
    blobs = []; shoots = []
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)
    chain = [(-1.0, 0.0), (-0.6, -0.12), (-0.2, 0.0), (0.2, -0.1), (0.6, 0.04), (0.95, -0.08)]
    for k, (u, v) in enumerate(chain):
        blobs.append((*P(u, v), s * (0.2 + 0.05 * (k % 2))))
        if k in (1, 3, 4):
            blobs.append((*P(u + 0.1, v - 0.32), s * 0.14))
            shoots.append([P(u + 0.1, v - 0.4), P(u + 0.18, v - 0.75)])
        if k in (2, 5):
            blobs.append((*P(u, v + 0.3), s * 0.13))
    return blobs, shoots


if "batik" in PARTS:
    n = 360
    rng = random.Random(9)
    leaves = [(84, 96, 54, 0.62), (264, 276, 54, 0.62), (276, 80, 38, -2.5), (96, 262, 38, -2.5)]
    def leaf_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for cx, cy, s_, a in leaves:
            cv.c.drawPath(smooth_path(lumbon_poly(cx + ox, cy + oy, s_, a)), p)
    leaf_m = wrap_mask(n, leaf_d)
    def vein_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=1.5, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        for cx, cy, s_, a in leaves:
            P = _T(cx + ox, cy + oy, s_, a)
            for (u0, v0), (u1, v1) in lumbon_veins():
                cv.c.drawLine(*P(u0, v0), *P(u1, v1), p)
            cv.c.drawLine(*P(*LUMBON_HUB), *P(0.06, -1.25), p)
    vein_m = wrap_mask(n, vein_d)
    jahes = [(180, 178, 30, -0.78), (0, 178, 26, -0.78), (180, 358, 26, -0.78)]
    def jahe_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        ps = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=3, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        for cx, cy, s_, a in jahes:
            bl, sh = jahe_items(cx + ox, cy + oy, s_, a, rng)
            for x, y, r in bl:
                cv.c.drawCircle(x, y, r, p)
            for (a0, a1) in sh:
                cv.c.drawLine(*a0, *a1, ps)
    jahe_m = wrap_mask(n, jahe_d)
    motif = np.maximum(leaf_m, jahe_m)
    # klowong outline (cream line just outside each motif) + cecek dots in the ground
    klow = np.clip(gaussian_filter(motif, 1.6, mode="wrap") * 1.0 > 0.06, 0, 1).astype(np.float32)
    klow = np.clip(np.clip((gaussian_filter(motif, 2.6, mode="wrap") > 0.03).astype(np.float32) - (gaussian_filter(motif, 0.8, mode="wrap") > 0.5), 0, 1), 0, 1)
    rr = np.random.default_rng(3)
    dots = []
    for _ in range(420):
        dots.append((rr.uniform(0, n), rr.uniform(0, n), rr.uniform(1.0, 1.7)))
    def dot_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in dots:
            cv.c.drawCircle(x + ox, y + oy, r, p)
    dot_m = wrap_mask(n, dot_d) * (1 - (gaussian_filter(motif, 3, mode="wrap") > 0.02))
    leaf_dots = []
    for cx, cy, s_, a in leaves:
        for _ in range(int(s_ * 0.8)):
            u, v = rr.uniform(-0.5, 0.5), rr.uniform(-0.8, 0.45)
            ca, sa = math.cos(a), math.sin(a)
            leaf_dots.append((cx + (u * ca - v * sa) * s_, cy + (u * sa + v * ca) * s_, 1.2))
    def ld_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        for x, y, r in leaf_dots:
            cv.c.drawCircle(x + ox, y + oy, r, p)
    ldot = wrap_mask(n, ld_d) * leaf_m * (1 - vein_m)
    # wax crackle (remukan): fine random polylines, periodic
    cr = []
    for _ in range(26):
        x, y = rr.uniform(0, n), rr.uniform(0, n); a = rr.uniform(0, math.tau)
        pts = [(x, y)]
        for _k in range(rr.integers(4, 9)):
            a += rr.uniform(-0.8, 0.8); L = rr.uniform(8, 22)
            x += math.cos(a) * L; y += math.sin(a) * L; pts.append((x, y))
        cr.append(pts)
    def cr_d(cv, ox, oy):
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE, StrokeWidth=0.9, Style=skia.Paint.kStroke_Style)
        for pts in cr:
            for i in range(len(pts) - 1):
                cv.c.drawLine(pts[i][0] + ox, pts[i][1] + oy, pts[i + 1][0] + ox, pts[i + 1][1] + oy, p)
    crack = wrap_mask(n, cr_d)
    # colour (periodic noise only, so the tile stays seamless)
    def col(h):
        return np.array(hex_rgb(h), np.float32)
    v1 = wrap_noise(n, n, 11, 14); v2 = wrap_noise(n, n, 12, 1.2)
    rgb = np.ones((n, n, 3), np.float32) * col(BLACK) * (0.85 + 0.3 * v1)[..., None]
    def lay(rgb, m, c, c2=None, amt=1.0, disp=1.2, seed=1):
        m = np.clip(wrap_disp(m, seed, disp), 0, 1) * amt
        t = wrap_noise(n, n, seed + 4, 20)[..., None]
        cc = col(c) * (1 - t) + col(c2 or c) * t
        cc = cc * (0.92 + 0.16 * v2[..., None])
        return rgb * (1 - m[..., None]) + cc * m[..., None]
    rgb = lay(rgb, leaf_m, SOGAN, "#8a5629", seed=21)
    rgb = lay(rgb, jahe_m, SOGAN_L, SOGAN, seed=23)
    rgb = lay(rgb, gaussian_filter(vein_m, 1.5, mode="wrap") * leaf_m, SOGAN_D, amt=0.6, disp=0.8, seed=24)
    rgb = lay(rgb, vein_m * leaf_m, "#d8c08f", amt=0.85, disp=0.8, seed=25)
    rgb = lay(rgb, klow, "#e3d2ad", "#cdb68a", amt=0.92, disp=0.9, seed=27)
    rgb = lay(rgb, dot_m, "#c9b083", amt=0.75, disp=0.4, seed=29)
    rgb = lay(rgb, ldot, "#e9d8b4", amt=0.8, disp=0.3, seed=31)
    rgb = lay(rgb, crack * (1 - motif), SOGAN, amt=0.55, disp=0.5, seed=33)
    rgb = lay(rgb, crack * motif, BLACK, amt=0.45, disp=0.5, seed=35)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    big = np.tile(arr, (2, 2, 1))
    prev(big, "bb-batik")
    save_full(arr, f"{OUT}/batik.webp", quality=78)
    clear()


# ------------------------------------------------------------------ lumbon leaf ornament
if "lumbon" in PARTS:
    W, H = 420, 600
    nx = Seq(20300); rng = random.Random(5)
    cx, cy, s_, ang = 210, 300, 200, 0.12
    lm = shapes(W, H, [lumbon_poly(cx, cy, s_, ang)])
    art = blank(W, H)
    art = GP(art, lm, SOGAN, "#8a5629", seed=nx(), rough=2.5, streak=0.8)
    P = _T(cx, cy, s_, ang)
    veins = []
    for (u0, v0), (u1, v1) in lumbon_veins():
        mid = ((u0 + u1) / 2 + 0.03, (v0 + v1) / 2)
        veins.append((curve([P(u0, v0), P(*mid), P(u1, v1)], 16), 3.4 if u1 == 0 else 2.2, (0.05, 0.6)))
    stem = [(curve([P(*LUMBON_HUB), P(0.05, -0.9), P(0.0, -1.35)], 20), 9, (0.0, 0.5))]
    vm = strokes(W, H, veins) * lm
    art = GP(art, strokes(W, H, stem), SOGAN_D, BLACK, seed=nx(), rough=1.2)
    art = G(art, gaussian_filter(vm, 2.5) * 1.5, SOGAN_D, seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    art = GP(art, vm, "#dcc596", seed=nx(), rough=0.8, pad=8)
    klow = outline(lm, 4)
    art = GP(art, klow, "#e7d6b0", "#d3bb8c", seed=nx(), rough=1.0, pad=8)
    # isen: cecek dots in rows between veins + inner cream line
    dts = [(*P(rng.uniform(-0.6, 0.6), rng.uniform(-0.7, 1.2)), rng.uniform(1.6, 2.4)) for _ in range(260)]
    dm = circles(W, H, dts) * np.clip(gaussian_filter(lm, 2) * 2 - 1, 0, 1) * (1 - gaussian_filter(vm, 2) * 3).clip(0, 1)
    art = GP(art, dm, "#ead9b6", seed=nx(), rough=0.5, pad=6)
    inner = outline(shapes(W, H, [lumbon_poly(cx, cy + 0.06 * s_, s_ * 0.88, ang)]), 1.6) * lm
    art = GP(art, inner, "#d9c193", seed=nx(), rough=0.7, pad=6)
    prev(art, "bb-lumbon", bg=BLACK)
    save(art, f"{OUT}/lumbon.webp", max_w=240, quality=82)
    clear()


# ------------------------------------------------------------------ jahe srimpang sprig divider
if "jahe" in PARTS:
    W, H = 560, 150
    nx = Seq(20400); rng = random.Random(6)
    art = blank(W, H)
    cx = W / 2
    bl, sh = [], []
    for (x, y, s_, a, fl) in [(cx - 130, 84, 52, 0.06, 1), (cx + 130, 84, 52, math.pi - 0.06, -1)]:
        b, s2 = jahe_items(x, y, s_, a, rng)
        bl += b; sh += s2
    knob = circles(W, H, bl)
    shoot = strokes(W, H, [(curve([a, ((a[0] + b[0]) / 2 + 3, (a[1] + b[1]) / 2), b], 8), 4, (0.05, 0.6)) for a, b in sh])
    centre = shapes(W, H, [lumbon_poly(cx, 70, 40, 0.0)])
    allm = np.maximum.reduce([knob, centre])
    art = GP(art, shoot, OLIVE_D, "#3a4222", seed=nx(), rough=0.8, pad=8)
    art = GP(art, knob, SOGAN_L, SOGAN, seed=nx(), rough=1.4, streak=0.8)
    art = GP(art, centre, SOGAN, SOGAN_D, seed=nx(), rough=1.2)
    art = GP(art, strokes(W, H, [(curve([(cx, 96), (cx, 70), (cx, 38)], 10), 2.4, (0.1, 0.4))]), BLACK, seed=nx(), rough=0.5, pad=6)
    # skin rings on the knobs (darker arcs) and cream klowong outline
    rings = []
    for x, y, r in bl:
        rings.append((arc_pts(x, y, r * 0.62, -2.4, -0.7, 10), 1.6, (0.2, 0.2)))
    art = G(art, strokes(W, H, rings) * knob, SOGAN_D, seed=nx(), density=0.7, edge=0.2, bloom=0, rough=0.6, feather=0.5)
    art = GP(art, outline(allm, 3.2), "#3a2210", seed=nx(), rough=0.6, pad=6)
    dts = [(cx + k * 16, 118 + 4 * (k % 2), 2.4 - abs(k) * 0.25) for k in range(-4, 5)]
    art = GP(art, circles(W, H, dts), GOLD, seed=nx(), rough=0.4, pad=6)
    prev(art, "bb-jahe", bg=CREAM)
    save(art, f"{OUT}/jahe.webp", max_w=320, quality=84)
    clear()


if "palm" in PARTS:
    W, H = 460, 760
    nx = Seq(20500); rng = random.Random(12)
    art = blank(W, H)
    art = palm_wash(art, W, H, 170, 770, 600, rng, nx, 0.14)
    art = palm_wash(art, W, H, 320, 770, 400, rng, nx, -0.12, SOGAN, SOGAN_D, 0.7)
    prev(art, "bb-palm", bg=CREAM)
    save(art, f"{OUT}/palm.webp", max_w=220, quality=82)
    clear()
