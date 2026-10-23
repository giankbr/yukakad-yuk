"""Kapas Syari — dried cotton bolls (kapas) on bare brown stems, a wooden embroidery hoop, cream linen.
Soft watercolour + white gouache on linen. Run: python3 -I kapas-syari.py [part ...]
parts: linen boll stem spray sprig hoop -> public/themes/art/kapas-syari/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i5_lib import *

OUT = outdir("kapas-syari")
PARTS = sys.argv[1:] or ["linen", "boll", "stem", "spray", "sprig", "hoop"]
SEQ = Seq(500)
BR_L, BR_M, BR_D = "#b8936b", "#8a6545", "#4e3424"   # dry bracts
STEM_A, STEM_B = "#6e5440", "#3f2e22"
COT, COT_S, COT_D = "#fffcf4", "#d9cdb9", "#a8987f"   # cotton white, shadow, crease
LEAF_A, LEAF_B = "#c2a47a", "#7a5a3c"                 # dried leaf


def boll(lay, W, H, cx, cy, s, ang, rng, lobes=4, open_=1.0):
    """One open cotton boll: curled dry bracts behind, 3-5 fluffy lobes of fibre, creases and wisps."""
    # bracts (star of pointed dry sepals)
    nb = 5
    items = []
    for i in range(nb):
        a = ang + i / nb * math.tau + rng.uniform(-.2, .2)
        L = s * rng.uniform(1.1, 1.4) * (0.75 + 0.35 * open_)
        items.append(deform(petal_pts(cx, cy, L, s * 0.3, a, n=14, cup=rng.choice([-1, 1]) * rng.uniform(.5, 1.0)), rng, 1, .05))
    mb = shapes(W, H, items)
    lay = G(lay, mb, BR_M, BR_L, seed=SEQ(), density=0.8, edge=0.8, bloom=0.3, gran=0.35, rough=3, holes=0.03)
    # darker inner halves / tips
    tips = []
    for pts in items:
        n = len(pts)
        tips.append(pts[n // 2 - 2:n // 2 + 3] + [(cx, cy)])
    lay = G(lay, shapes(W, H, tips) * mb, BR_D, seed=SEQ(), density=0.42, edge=0.5, bloom=0.1, rough=2)
    # lobes
    lob = []
    for i in range(lobes):
        a = ang + math.pi / lobes + i / lobes * math.tau + rng.uniform(-.25, .25)
        d = s * 0.36 * open_
        lx, ly = cx + math.cos(a) * d, cy + math.sin(a) * d
        lob.append((lx, ly, a))
    lob.sort(key=lambda t: t[1])
    allm = np.zeros((H, W), np.float32)
    for lx, ly, a in lob:
        rx = s * rng.uniform(0.46, 0.56)
        bumps = [(lx, ly, rx * 0.78)]
        for k in range(9):
            ba = a + (k - 4) * 0.42 + rng.uniform(-.15, .15)
            bumps.append((lx + math.cos(ba) * rx * 0.42, ly + math.sin(ba) * rx * 0.4, rx * rng.uniform(0.32, 0.5)))
        m = circles(W, H, bumps)
        m = displace(m, SEQ(), 3.5, 7)
        lay = knockout(lay, m, 0.95, 1.5)
        lay = GP(lay, m, COT, "#f6efe2", seed=SEQ(), rough=4.0, streak=0.08, density=0.97)
        sh = shade_field(m, (-0.6, -0.8), soft=s * 0.08, depth=s * 0.12)
        lay = G(lay, m * np.clip(sh * 1.5 - 0.2, 0, 1), COT_S, "#cfc2ab", seed=SEQ(), density=0.75, edge=0.35, bloom=0.4, gran=0.25, rough=2, feather=1.6)
        # cushion shadow cast on the lobe behind
        lay = over(lay, rgba("#8b7a62", np.clip(shift(gaussian_filter(m, s * 0.05), 3, 5) - m, 0, 1) * 0.35))
        allm = np.maximum(allm, m)
    # creases between lobes (towards the centre)
    cr = []
    for lx, ly, a in lob:
        a2 = a + math.pi / lobes
        p0 = (cx + math.cos(a2) * s * 0.05, cy + math.sin(a2) * s * 0.05)
        p1 = (cx + math.cos(a2) * s * 0.5 * open_, cy + math.sin(a2) * s * 0.5 * open_)
        cr.append(([p0, ((p0[0] + p1[0]) / 2 + rng.gauss(0, 2), (p0[1] + p1[1]) / 2 + rng.gauss(0, 2)), p1], s * 0.05, (0.2, 0.6)))
    mc = strokes(W, H, cr) * (1 - allm)
    lay = G(lay, mc, COT_D, seed=SEQ(), density=0.5, edge=0.2, bloom=0, rough=1.2, feather=1.0)
    # wisps of loose fibre at the rim
    ws = []
    for _ in range(int(10 + s * 0.12)):
        a = rng.uniform(0, math.tau)
        r0 = s * rng.uniform(0.62, 0.8)
        x0, y0 = cx + math.cos(a) * r0, cy + math.sin(a) * r0 * 0.95
        ln = s * rng.uniform(0.1, 0.22)
        aa = a + rng.uniform(-.8, .8)
        ws.append(([(x0, y0), (x0 + math.cos(aa) * ln, y0 + math.sin(aa) * ln)], max(1.0, s * 0.018), (0.3, 0.6)))
    mw = strokes(W, H, ws)
    lay = over(lay, rgba("#fffdf8", gaussian_filter(mw, 0.8) * 0.8))
    lay = G(lay, mw * 0.5, COT_S, seed=SEQ(), density=0.25, edge=0.1, bloom=0, rough=1, feather=0.6)
    return lay


def stem(lay, W, H, pts, width, rng):
    m = strokes(W, H, [(curve(pts, 60), width, (0.02, 0.5))])
    lay = G(lay, m, STEM_A, STEM_B, seed=SEQ(), density=0.8, edge=0.7, bloom=0.15, gran=0.3, rough=1.5, feather=0.8)
    # dry bark highlights
    hl = strokes(W, H, [([(x - width * 0.18, y) for x, y in curve(pts, 60)], width * 0.25, (0.1, 0.5))]) * m
    lay = over(lay, rgba("#c9ae8c", hl * 0.35))
    return lay


def dleaf(lay, W, H, x, y, L, a, rng):
    pts = petal_pts(x, y, L, L * 0.28, a, n=14, cup=rng.uniform(-.7, .7))
    m = shape_mask(W, H, deform(pts, rng, 2, 0.08))
    lay = G(lay, m, LEAF_A, LEAF_B, seed=SEQ(), density=0.6, edge=0.75, bloom=0.4, gran=0.3, rough=3, holes=0.05)
    v = [(x + math.cos(a) * L * t, y + math.sin(a) * L * t) for t in np.linspace(0.05, 0.85, 8)]
    lay = G(lay, strokes(W, H, [(v, max(1.2, L * 0.025))]), LEAF_B, seed=SEQ(), density=0.4, edge=0.2, bloom=0, rough=1, feather=.6)
    return lay


def bud(lay, W, H, x, y, s, a, rng):
    """Closed boll: brown pointed capsule with a slit of white."""
    m = shape_mask(W, H, deform(petal_pts(x, y, s * 1.5, s * 0.55, a, n=12), rng, 1, .06))
    lay = G(lay, m, BR_L, BR_D, seed=SEQ(), density=0.7, edge=0.8, bloom=0.2, gran=0.3, rough=2.5)
    sl = strokes(W, H, [([(x + math.cos(a) * s * .35, y + math.sin(a) * s * .35), (x + math.cos(a) * s * 1.2, y + math.sin(a) * s * 1.2)], s * .28, (0.3, 0.4))])
    lay = GP(lay, sl * m, COT, seed=SEQ(), rough=2, streak=0.2)
    return lay


def branch(lay, W, H, base, top, rng, heads, width=9.0, leaves=2, buds=1):
    """A dried cotton stem from base to top with bolls on short side twigs."""
    (bx, by), (tx, ty) = base, top
    mid = ((bx + tx) / 2 + rng.uniform(-30, 30), (by + ty) / 2)
    main = [base, ((bx * 2 + tx) / 3 + rng.gauss(0, 10), (by * 2 + ty) / 3), mid, ((bx + tx * 2) / 3 + rng.gauss(0, 10), (by + ty * 2) / 3), top]
    lay = stem(lay, W, H, main, width, rng)
    path = curve(main, 80)
    for k in range(leaves):
        t = rng.uniform(0.25, 0.7)
        i = int(t * (len(path) - 1))
        px, py = path[i]
        side = -1 if k % 2 else 1
        lay = dleaf(lay, W, H, px, py, rng.uniform(80, 115), (-math.pi / 2 + side * rng.uniform(0.7, 1.2)), rng)
    for (t, side, s, lobes) in heads:
        i = int(t * (len(path) - 1))
        px, py = path[i]
        if t > 0.97:
            hx, hy = px, py
        else:
            L = s * 1.1
            hx, hy = px + side * L, py - L * 0.55
            lay = stem(lay, W, H, [(px, py), ((px + hx) / 2, (py + hy) / 2 + 6), (hx, hy)], width * 0.6, rng)
        lay = boll(lay, W, H, hx, hy, s, rng.uniform(0, math.tau), rng, lobes=lobes)
    for k in range(buds):
        t = rng.uniform(0.45, 0.85)
        i = int(t * (len(path) - 1))
        px, py = path[i]
        side = 1 if k % 2 else -1
        a = -math.pi / 2 + side * 0.7
        ex, ey = px + math.cos(a) * 40, py + math.sin(a) * 40
        lay = stem(lay, W, H, [(px, py), (ex, ey)], width * 0.45, rng)
        lay = bud(lay, W, H, ex, ey, 16, a, rng)
    return lay


def linen():
    """Seamless cream linen weave tile (opaque)."""
    w = h = 512
    base = np.array(hex_rgb("#f1e9da"), np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nw = wrap_noise(w, h, 3, (0.5, 30)) - 0.5   # slubs along warp
    nf = wrap_noise(w, h, 4, (30, 0.5)) - 0.5   # slubs along weft
    warp = 0.5 + 0.5 * np.cos(xx / 512 * math.tau * 128 + nw * 3)
    weft = 0.5 + 0.5 * np.cos(yy / 512 * math.tau * 128 + nf * 3)
    over_ = ((np.floor(xx / 4) + np.floor(yy / 4)) % 2)
    v = 1 + (warp * over_ + weft * (1 - over_) - 0.5) * 0.05 + nw * 0.06 + nf * 0.06
    v += (wrap_noise(w, h, 9, 0.6) - 0.5) * 0.03
    rgb = np.clip(base * v[..., None], 0, 1)
    save_rgb(np.concatenate([rgb, np.ones((h, w, 1), np.float32)], -1), f"{OUT}/linen.webp", quality=72)


def p_boll():
    W = H = 340
    rng = random.Random(11)
    lay = boll(blank(W, H), W, H, 170, 170, 120, 0.4, rng, lobes=4)
    preview(lay, "boll", bg="#f1e9da")
    save(lay, f"{OUT}/boll.webp", max_w=160)


def p_stem():
    W, H = 520, 1320
    rng = random.Random(23)
    lay = blank(W, H)
    lay = branch(lay, W, H, (300, 1310), (210, 150), rng, [(0.99, 0, 92, 4), (0.62, -1, 74, 5), (0.4, 1, 66, 4), (0.8, 1, 58, 3)], width=11, leaves=3, buds=1)
    flush()
    lay = branch(lay, W, H, (330, 1310), (420, 520), rng, [(0.99, 0, 64, 4), (0.55, -1, 50, 4)], width=7, leaves=1, buds=1)
    preview(lay, "stem", bg="#efe6d6")
    save(lay, f"{OUT}/stem.webp", max_w=440)


def p_spray():
    W, H = 900, 520
    rng = random.Random(41)
    lay = blank(W, H)
    # three stems crossing, gathered low centre, tied with a linen strip (painted later in CSS? no: painted here)
    lay = branch(lay, W, H, (470, 510), (150, 150), rng, [(0.99, 0, 70, 4), (0.55, 1, 54, 4)], width=8, leaves=1, buds=1)
    flush()
    lay = branch(lay, W, H, (450, 510), (760, 120), rng, [(0.99, 0, 76, 5), (0.5, -1, 52, 3)], width=8, leaves=1, buds=1)
    flush()
    lay = branch(lay, W, H, (460, 515), (470, 90), rng, [(0.99, 0, 64, 4), (0.62, 1, 46, 4)], width=7, leaves=1, buds=0)
    # linen tie
    wraps = [([(428, 418 + k * 8 + rng.gauss(0, 1)), (466, 414 + k * 8), (504, 419 + k * 8 + rng.gauss(0, 1))], 5.5, None) for k in range(5)]
    tie = strokes(W, H, wraps)
    lay = knockout(lay, tie, 0.9, 1.0)
    lay = G(lay, tie, "#d8c39d", "#a88a5e", seed=SEQ(), density=0.92, edge=0.7, bloom=0.1, gran=0.4, rough=1)
    tails = strokes(W, H, [([(470, 452), (440, 478), (430, 512)], 4, (0.1, 0.4)), ([(474, 452), (508, 470), (530, 500)], 4, (0.1, 0.4))])
    lay = G(lay, tails, "#cdb68e", "#a88a5e", seed=SEQ(), density=0.85, edge=0.6, bloom=0.1, gran=0.4, rough=1)
    preview(lay, "spray", bg="#efe6d6")
    save(lay, f"{OUT}/spray.webp", max_w=720)


def p_sprig():
    W, H = 560, 150
    rng = random.Random(5)
    lay = blank(W, H)
    lay = stem(lay, W, H, [(40, 100), (160, 84), (280, 76), (400, 84), (520, 100)], 5, rng)
    lay = boll(lay, W, H, 280, 66, 46, 0.2, rng, lobes=4)
    lay = dleaf(lay, W, H, 190, 82, 46, math.pi + 0.35, rng)
    lay = dleaf(lay, W, H, 370, 80, 46, -0.35, rng)
    lay = bud(lay, W, H, 470, 92, 11, -0.5, rng)
    lay = bud(lay, W, H, 92, 94, 11, math.pi + 0.5, rng)
    preview(lay, "sprig", bg="#efe6d6")
    save(lay, f"{OUT}/sprig.webp", max_w=340)


def p_hoop():
    """Wooden embroidery hoop (ring + brass screw clasp at the top), watercolour wood grain."""
    W = H = 760
    cx, cy, R = 380, 400, 330
    rng = random.Random(8)
    outer = ring_mask(W, H, cx, cy, R, 30)
    inner = ring_mask(W, H, cx, cy, R - 19, 9)
    lay = G(blank(W, H), outer, "#d9b98c", "#b98d5c", seed=SEQ(), density=0.82, edge=0.55, bloom=0.2, gran=0.3, rough=1.2, feather=0.8)
    # grain
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    rad = np.hypot(xx - cx, yy - cy)
    grain = 0.5 + 0.5 * np.sin(rad * 1.3 + ang * 3 + (fbm(W, H, 77, 60, 3) - .5) * 9)
    lay = G(lay, outer * np.clip((grain - 0.7) * 3, 0, 1), "#a27548", seed=SEQ(), density=0.22, edge=0.1, bloom=0, rough=0.6, feather=0.6)
    sh = outer * np.clip(((xx - cx) * 0.6 + (yy - cy) * 0.8) / R, 0, 1)
    lay = G(lay, sh, "#7a5230", seed=SEQ(), density=0.35, edge=0.1, bloom=0.2, rough=0.6, feather=2)
    lay = G(lay, inner, "#c8a170", "#9a7146", seed=SEQ(), density=0.5, edge=0.4, bloom=0.1, rough=0.8, feather=0.8)
    # brass clasp
    cl = shapes(W, H, [[(cx - 22, cy - R - 20), (cx + 22, cy - R - 20), (cx + 20, cy - R + 14), (cx - 20, cy - R + 14)]], smooth=False)
    lay = knockout(lay, cl, 1.0, 0.8)
    lay = FO(lay, cl, "#8f7a55", seed=SEQ(), emboss=0.6, sparkle=0.0)
    sc = np.clip(strokes(W, H, [([(cx - 5, cy - R - 21), (cx - 5, cy - R - 40)], 7, None), ([(cx + 5, cy - R - 21), (cx + 5, cy - R - 40)], 7, None)]) + ellipses(W, H, [(cx, cy - R - 44, 14, 7, 0)]), 0, 1)
    lay = FO(lay, sc, "#7d6a4a", seed=SEQ(), emboss=0.7, sparkle=0.0)
    preview(lay, "hoop", bg="#efe6d6")
    save(lay, f"{OUT}/hoop.webp", max_w=640, quality=80)


for p in PARTS:
    {"linen": linen, "boll": p_boll, "stem": p_stem, "spray": p_spray, "sprig": p_sprig, "hoop": p_hoop}[p]()
    flush()
kb(OUT)
