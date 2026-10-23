"""Flora Gelap — an original still life in the spirit of Dutch Golden Age flower painting: peonies, flamed tulips,
roses, larkspur and a butterfly in a dark stone urn on a ledge, lit hard from the upper left out of near-black.
Oil-ish opaque paint (form shading, brush texture, glazed shadows), canvas weave and warm varnish.
Run: python3 -I flora-gelap.py [part ...]
parts: still rose tulip sprig butterfly petal -> public/themes/art/flora-gelap/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i5_lib import *

OUT = outdir("flora-gelap")
PARTS = sys.argv[1:] or ["still", "rose", "tulip", "sprig", "butterfly", "petal"]
SEQ = Seq(300)
LD = (-0.72, -0.7)  # light from the upper left
BG = "#0c0908"
PEONY = ("#f6dfd6", "#d79a9a", "#7a3540")
PEONY_W = ("#f7efe0", "#d8c3a4", "#6f5a44")
ROSE = ("#e0504a", "#9a1f26", "#3e0a10")
TULIP_Y, TULIP_R = "#f3cf6a", "#b8222a"
LEAF = ("#5f7a3e", "#2c3d1f", "#0e160b")
BLUE = ("#6f8fcf", "#2e4a8f", "#121d3d")


def _ramp(tone, pal, hi=None):
    """tone 0..1 -> dark..mid..light (..hi)."""
    light, mid, dark = [np.array(hex_rgb(c), np.float32) for c in pal]
    t = np.clip(tone, 0, 1)[..., None]
    lo = dark * (1 - np.clip(t * 2, 0, 1)) + mid * np.clip(t * 2, 0, 1)
    up = mid * (1 - np.clip(t * 2 - 1, 0, 1)) + light * np.clip(t * 2 - 1, 0, 1)
    rgb = np.where(t < 0.5, lo, up)
    if hi:
        k = np.clip((t - 0.86) * 6, 0, 1)
        rgb = rgb * (1 - k) + np.array(hex_rgb(hi), np.float32) * k
    return rgb


def paint(lay, W, H, pts, base, ang, L, pal, fc, fr, hi=None, lit=1.0, fold=0.18, rim=0.5, cast=0.55, rough=1.6,
          tip_light=True, deform_amt=0.04, tone_bias=0.0):
    """One oil-painted petal/leaf/wing: tone grows from a dark base to a lit tip, modulated by where it sits in the
    flower relative to the light; a central fold, a pale lit rim, hair-fine brush striations along the form, and a
    soft cast shadow onto what is already painted."""
    m = shape_mask(W, H, deform(pts, random.Random(SEQ()), 2, deform_amt) if deform_amt > 0.006 else pts, smooth=deform_amt > 0.006)
    bb = bbox(m, 10)
    if bb is None:
        return lay, m
    y0, y1, x0, x1 = bb
    mc = m[y0:y1, x0:x1]
    h, w = mc.shape
    sd = SEQ()
    mc = displace(mc, sd, rough, 18)
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    ca, sa = math.cos(ang), math.sin(ang)
    u = ((xx - base[0]) * ca + (yy - base[1]) * sa) / L
    v = (-(xx - base[0]) * sa + (yy - base[1]) * ca) / L
    t = np.clip(u, 0, 1)
    tone = (0.22 + 0.7 * t ** 0.75) if tip_light else (0.75 - 0.45 * t)
    g = ((xx - fc[0]) * LD[0] + (yy - fc[1]) * LD[1]) / max(fr, 1)
    tone = tone * (0.5 + 0.5 * np.clip(g * 0.9 + 0.55, 0, 1)) * lit + tone_bias
    tone -= fold * np.exp(-(v * 5) ** 2) * (1 - t) * 1.4
    nz = fbm(w, h, sd + 2, 30, 3) - 0.5
    tone += nz * 0.12
    # pale lit rim along the outer edge
    inner = gaussian_filter(mc, 2.2)
    band = np.clip((mc - np.clip((inner - 0.5) * 2.6 + 0.5, 0, 1)) * 2.4, 0, 1)
    tone += band * rim * np.clip(g * 0.8 + 0.6, 0, 1) * (0.4 + 0.6 * t)
    rgb = _ramp(tone, pal, hi)
    stri = np.sin(v * L / 0.55 + nz * 14) * 0.5 + 0.5
    rgb *= (1 + (stri[..., None] - 0.5) * 0.045)
    src = np.concatenate([np.clip(rgb, 0, 1), (np.clip((gaussian_filter(mc, 0.7) - 0.25) * 2.0, 0, 1) * 0.98)[..., None]], -1)
    out = lay.copy()
    if cast:
        sh = gaussian_filter(np.roll(np.roll(mc, 6, 0), 5, 1), 5) * cast
        dst = out[y0:y1, x0:x1].copy()
        dst[..., :3] *= (1 - sh[..., None] * 0.85)
        out[y0:y1, x0:x1] = dst
    out[y0:y1, x0:x1] = over(out[y0:y1, x0:x1], src)
    return out, m


def globe(lay, W, H, cx, cy, r, amt=0.55, squash=0.85, mask=None):
    """Shade a whole flower head as one volume: the side away from the light sinks into shadow."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = (xx - cx) / r, (yy - cy) / (r * squash)
    d = np.sqrt(dx * dx + dy * dy)
    away = np.clip((-(dx * LD[0] + dy * LD[1])) * 0.7 + 0.25, 0, 1) * np.clip(1.3 - d * 0.5, 0, 1)
    rimdark = np.clip((d - 0.75) * 2.5, 0, 1) * 0.5
    f = np.clip(away + rimdark, 0, 1)
    if mask is not None:
        f = f * np.clip(gaussian_filter(mask, 1.0), 0, 1)
    return darken(lay, f, amt)


def peony(lay, W, H, cx, cy, r, pal, rng, tilt=0.75, lit=1.0):
    """Ruffled peony: back skirt petals, rings of cupped scalloped petals, a dense frilly heart."""
    acc = np.zeros((H, W), np.float32)
    for ring, (rf, n, sz, lt) in enumerate([(0.62, 10, 0.55, 0.75), (0.42, 9, 0.44, 0.9), (0.24, 8, 0.32, 1.0), (0.1, 6, 0.22, 1.05)]):
        for k in range(n):
            a = k / n * math.tau + rng.uniform(-.2, .2) + ring * 0.5
            rj = rf + rng.uniform(-0.07, 0.07)
            px, py = cx + math.cos(a) * r * rj, cy - r * 0.06 * ring + math.sin(a) * r * rj * tilt
            pr = r * sz * rng.uniform(0.8, 1.2)
            pts = ellipse_pts(px, py, pr, pr * 0.78, 16, a + math.pi / 2)
            pts = [(x + math.cos(i * 2.3 + k) * pr * 0.07, y + math.sin(i * 1.9 + k) * pr * 0.07) for i, (x, y) in enumerate(pts)]
            base = (cx + math.cos(a) * r * rf * 0.15, cy - r * 0.06 * ring + math.sin(a) * r * rf * 0.15 * tilt)
            lay, pm = paint(lay, W, H, pts, base, a, r * (rf + sz) * 0.95, pal, (cx, cy), r, hi="#fff8f0", lit=lit * lt, fold=0.12, rim=0.3, cast=0.35 + 0.1 * (3 - ring), deform_amt=0.07)
            acc = np.maximum(acc, pm)
    return globe(lay, W, H, cx, cy - r * 0.1, r * 1.05, 0.6, mask=acc)


def rose(lay, W, H, cx, cy, r, pal, rng, lit=1.0):
    acc = np.zeros((H, W), np.float32)
    for k in range(6):
        a = k / 6 * math.tau + rng.uniform(-.2, .2)
        px, py = cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.38
        pts = ellipse_pts(px, py, r * 0.56, r * 0.44, 14, a + math.pi / 2)
        lay, pm = paint(lay, W, H, pts, (cx, cy), a, r * 1.0, pal, (cx, cy), r, hi="#ffd9c8", lit=lit * 0.85, fold=0.1, rim=0.7)
        acc = np.maximum(acc, pm)
    for k in range(6):
        rr = r * (0.58 - k * 0.075)
        a0 = rng.uniform(0, math.tau)
        outer = arc_pts(cx + rng.gauss(0, r * .03), cy - r * 0.08, rr, a0, a0 + rng.uniform(2.4, 3.3), 20, 0.82)
        inner = arc_pts(cx, cy - r * 0.12, rr * 0.55, a0 + 2.8, a0 + 0.3, 12, 0.82)
        mid_a = a0 + 1.4
        lay, _ = paint(lay, W, H, outer + inner, (cx, cy - r * 0.1), mid_a, rr, pal, (cx, cy), r, hi="#ffe0d2", lit=lit * (0.9 + k * 0.03), fold=0.0, rim=0.9, deform_amt=0.02)
    heart = circles(W, H, [(cx + r * 0.02, cy - r * 0.1, r * 0.08)])
    lay = darken(lay, gaussian_filter(heart, r * 0.03), 0.75)
    return globe(lay, W, H, cx, cy, r * 1.05, 0.5, mask=acc)


def tulip(lay, W, H, cx, cy, s, ang, rng, flamed=True, lit=1.0):
    """Tulip head, base at (cx, cy) opening along ang: three cupped petals, flamed red streaks on yellow."""
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda u, v: (cx + v * ca - u * sa, cy + v * sa + u * ca)
    pal = (TULIP_Y, "#d39a3a", "#4a240c") if flamed else ("#f4b3b8", "#c34a5c", "#3e0c16")
    for i, side in enumerate((-1, 1, 0)):
        u0 = side * s * 0.3
        pts = [P(u0 - s * 0.38, 0), P(u0 - s * 0.5, s * 0.6), P(u0 - s * 0.3, s * 1.25), P(u0, s * 1.5), P(u0 + s * 0.3, s * 1.25), P(u0 + s * 0.5, s * 0.6), P(u0 + s * 0.38, 0), P(u0, -s * 0.15)]
        lay, m = paint(lay, W, H, pts, P(u0, -s * 0.1), ang, s * 1.55, pal, P(0, s * 0.8), s, hi="#fff4cc" if flamed else "#ffe0e4", lit=lit * (0.85 if i < 2 else 1.0), fold=0.2, rim=0.6)
        if flamed:
            fl = []
            for k in range(6):
                u = u0 + (k - 2.5) * s * 0.13
                pp = [P(u + math.sin(j * 1.3 + k) * s * 0.04, s * tt) for j, tt in enumerate(np.linspace(0.2, 1.38, 10))]
                fl.append((pp, s * rng.uniform(0.04, 0.09), (0.7, 0.12)))
            fm = strokes(W, H, fl) * m
            sh = np.clip(((np.mgrid[0:H, 0:W][1] - cx) * LD[0] + (np.mgrid[0:H, 0:W][0] - cy) * LD[1]) / s * 0.4 + 0.6, 0.2, 1)
            red = rgba(TULIP_R, fm * 0.92)
            red[..., :3] *= (0.45 + 0.55 * sh[..., None] * lit)
            lay = over(lay, red)
    return lay


def leaf(lay, W, H, x, y, L, a, rng, lit=1.0, cup=0.3):
    pts = petal_pts(x, y, L, L * 0.26, a, n=16, cup=cup)
    fc = (x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5)
    lay, m = paint(lay, W, H, pts, (x, y), a, L, LEAF, fc, L * 0.5, hi="#a9b878", lit=lit, fold=0.3, rim=0.35, cast=0.5)
    v = [(x + math.cos(a) * L * t - math.sin(a) * cup * L * .26 * t * t, y + math.sin(a) * L * t + math.cos(a) * cup * L * .26 * t * t) for t in np.linspace(0.05, 0.9, 9)]
    lay = over(lay, rgba("#a7b47a", strokes(W, H, [(v, max(1.2, L * 0.012))]) * m * 0.35 * lit))
    return lay


def stem(lay, W, H, pts, w, lit=1.0):
    m = strokes(W, H, [(curve(pts, 50), w, (0.05, 0.1))])
    return IM(lay, m, mix(LEAF[1], LEAF[0], lit * 0.8), LEAF[2], seed=SEQ(), lightdir=LD, soft=2.5)


def larkspur(lay, W, H, pts, rng, lit=1.0):
    """Spike of small blue florets along a curved stem."""
    lay = stem(lay, W, H, pts, 4, lit)
    path = curve(pts, 40)
    pp = path[::3]
    for i, (x, y) in enumerate(pp):
        t = i / max(1, len(pp) - 1)
        rr = 17 * (1 - t * 0.55)
        for side in (-1, 1):
            fx, fy = x + side * rr * 0.55, y + rng.uniform(-3, 3)
            for k in range(4):
                a = k / 4 * math.tau + rng.uniform(-.3, .3)
                pts2 = petal_pts(fx, fy, rr * 0.8, rr * 0.4, a, n=10)
                lay, _ = paint(lay, W, H, pts2, (fx, fy), a, rr * 0.8, BLUE, (fx, fy), rr, hi="#c6d4f2", lit=lit * (1 - t * 0.3), fold=0.05, rim=0.5, cast=0.3)
    return lay


def butterfly(lay, W, H, cx, cy, s, rng, ang=-0.3):
    """Small brown-orange butterfly, wings spread (original pattern): dark base, warm field, dark margin, pale spots."""
    c, sn = math.cos(ang), math.sin(ang)
    R = lambda x, y: (cx + x * c - y * sn, cy + x * sn + y * c)
    pal = ("#f0a243", "#b45a18", "#1e0d06")
    for flip in (1, -1):
        F = lambda x, y: R(x * flip, y)
        hw = [F(0, 0.05 * s), F(0.7 * s, 0.12 * s), F(0.9 * s, 0.5 * s), F(0.5 * s, 0.78 * s), F(0.08 * s, 0.4 * s)]
        fw = [F(0, 0), F(0.35 * s, -0.8 * s), F(1.12 * s, -0.98 * s), F(1.15 * s, -0.55 * s), F(0.6 * s, 0.06 * s)]
        lay, mh = paint(lay, W, H, hw, F(0, 0.1 * s), ang + (0.9 if flip > 0 else math.pi - 0.9), s * 0.85, pal, (cx, cy), s, lit=0.9, fold=0.0, rim=0.2, cast=0.4)
        lay, mf = paint(lay, W, H, fw, F(0, 0), ang + (-0.75 if flip > 0 else math.pi + 0.75), s * 1.2, pal, (cx, cy), s, lit=1.0, fold=0.0, rim=0.2, cast=0.4)
        wing = np.clip(mf + mh, 0, 1)
        margin = np.clip(wing - np.clip((gaussian_filter(wing, s * 0.06) - 0.5) * 3 + 0.5, 0, 1), 0, 1)
        lay = darken(lay, gaussian_filter(margin, 1.2) * 1.4, 0.8)
        tip = F(0.95 * s, -0.74 * s)
        spots = circles(W, H, [(tip[0], tip[1], s * 0.07), (F(0.78 * s, -0.68 * s)[0], F(0.78 * s, -0.68 * s)[1], s * 0.05), (F(0.45 * s, -0.5 * s)[0], F(0.45 * s, -0.5 * s)[1], s * 0.1)])
        lay = over(lay, rgba("#efe0bd", gaussian_filter(spots * mf, 0.8) * 0.85))
    body = strokes(W, H, [([R(0, -s * 0.22), R(0, s * 0.5)], s * 0.1, (0.3, 0.4))])
    lay = over(lay, rgba("#1a100a", body))
    ant = strokes(W, H, [([R(0, -s * 0.22), R(-s * 0.22, -s * 0.66)], 1.4, None), ([R(0, -s * 0.22), R(s * 0.22, -s * 0.66)], 1.4, None)])
    lay = over(lay, rgba("#1a100a", ant * 0.8))
    return lay


def canvas_weave(w, h, seed=4):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wv = (np.sin(xx * 1.9) * np.sin(yy * 1.9)) * 0.5 + 0.5
    n = gaussian_filter(np.random.default_rng(seed).random((h, w)).astype(np.float32), 0.7)
    return (wv - 0.5) * 0.05 + (n - 0.5) * 0.06


def finish(arr, light=(0.28, 0.2), radius=0.95, varnish=0.18):
    """Chiaroscuro falloff from the light, warm varnish, canvas texture."""
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot((xx / w - light[0]) * 1.0, (yy / h - light[1]) * 0.75)
    fall = np.clip(d / radius, 0, 1) ** 1.6
    out = arr.copy()
    out[..., :3] *= (1 - fall[..., None] * 0.86)
    warm = np.array(hex_rgb("#e9c48a"), np.float32)
    out[..., :3] = out[..., :3] * (1 - varnish) + out[..., :3] * warm * varnish * 1.15
    out[..., :3] = np.clip(out[..., :3] * (1 + canvas_weave(w, h)[..., None]), 0, 1)
    return out


def snowball(lay, W, H, cx, cy, r, rng, lit=1.0):
    """Cluster of tiny four-petalled white florets (guelder-rose like)."""
    pal = ("#f4f0e2", "#b8b598", "#2e3424")
    for k in range(int(r * 0.9)):
        a = rng.uniform(0, math.tau)
        d = r * math.sqrt(rng.random())
        fx, fy = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.85
        for j in range(4):
            pa = j / 4 * math.tau + rng.uniform(0, 1.5)
            pts = petal_pts(fx, fy, r * 0.16, r * 0.09, pa, n=10)
            lay, _ = paint(lay, W, H, pts, (fx, fy), pa, r * 0.16, pal, (cx, cy), r, hi="#fffdf3", lit=lit, fold=0.0, rim=0.4, cast=0.35, deform_amt=0.06)
    return lay


def p_still():
    W, H = 800, 1160
    rng = random.Random(1627)
    # background: near-black umber, a breath of warmth behind the bouquet
    lay = painted_sky(W, H, [(0, "#14100d"), (0.45, "#0e0b09"), (1, "#080605")], seed=5, streak=0.8)
    lay = soft(lay, ellipses(W, H, [(300, 380, 300, 360, -15)]), "#2e2318", 0.6, 110)
    # stone ledge
    ledge = shapes(W, H, [[(-20, 930), (W + 20, 915), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    lay = IM(lay, ledge, "#54473b", "#120e0b", seed=SEQ(), lightdir=(-0.5, -0.85), soft=50, streak=1.0)
    front = shapes(W, H, [[(-20, 985), (W + 20, 970), (W + 20, H + 20), (-20, H + 20)]], smooth=False)
    lay = IM(lay, front, "#2a221c", "#080605", seed=SEQ(), lightdir=(-0.9, -0.3), soft=70, streak=1.0)
    edge = strokes(W, H, [([(-10, 984), (W + 10, 969)], 3, None)])
    lay = over(lay, rgba("#a08668", edge * np.clip(1.2 - np.mgrid[0:H, 0:W][1] / W, 0, 1) * 0.6))
    flush()
    # urn: cylindrical shading lit from the left, specular streak
    half = curve([(356, 935), (300, 935), (292, 902), (252, 862), (232, 792), (250, 735), (300, 702), (302, 674), (278, 650), (356, 650)], 80)
    urn = half + [(712 - x, y) for x, y in half[::-1]]
    lay, mu = paint(lay, W, H, urn, (226, 800), 0.0, 260, ("#9c8466", "#4a3b2c", "#0b0908"), (260, 760), 160, tip_light=False, fold=0.0, rim=0.25, cast=0.0, deform_amt=0.0, rough=0.8)
    spec = strokes(W, H, [([(262, 760), (258, 800), (268, 850)], 9, (0.3, 0.3)), ([(318, 664), (318, 694)], 5, (0.3, 0.3))])
    lay = over(lay, rgba("#d8c4a0", gaussian_filter(spec, 2.5) * 0.55))
    bands = strokes(W, H, [([(244, 760), (356, 772), (470, 760)], 4, None), ([(262, 846), (356, 858), (452, 846)], 3, None)]) * mu
    lay = over(lay, rgba("#b9a27c", bands * 0.35))
    lay = darken(lay, gaussian_filter(shapes(W, H, [[(412, 935), (600, 928), (560, 965), (400, 965)]], smooth=False), 16), 0.7)
    flush()
    # back leaves fanning up into the dark
    for (x, y, L, a) in [(300, 640, 230, -2.3), (420, 640, 250, -0.7), (350, 600, 300, -1.75), (250, 660, 220, -2.85), (470, 660, 220, -0.3),
                         (380, 610, 200, -1.2), (330, 620, 240, -2.0), (440, 630, 230, -1.0)]:
        lay = leaf(lay, W, H, x, y, L, a, rng, lit=0.4)
    flush()
    lay = larkspur(lay, W, H, [(350, 640), (330, 470), (300, 330), (276, 170)], rng, lit=0.85)
    lay = larkspur(lay, W, H, [(400, 640), (450, 500), (530, 360), (585, 270)], rng, lit=0.55)
    lay = larkspur(lay, W, H, [(320, 640), (230, 520), (150, 450), (96, 420)], rng, lit=0.7)
    flush()
    # tall tulips at the back
    lay = stem(lay, W, H, [(360, 640), (390, 420), (420, 260), (440, 170)], 7)
    lay = tulip(lay, W, H, 441, 182, 58, -1.5, rng, lit=0.95)
    lay = stem(lay, W, H, [(330, 640), (250, 470), (190, 360), (160, 300)], 6)
    lay = tulip(lay, W, H, 160, 304, 52, -2.15, rng, flamed=False, lit=1.0)
    lay = stem(lay, W, H, [(400, 640), (520, 420), (620, 300), (660, 262)], 6)
    lay = tulip(lay, W, H, 660, 268, 50, -0.75, rng, lit=0.55)
    flush()
    lay = snowball(lay, W, H, 565, 350, 64, rng, lit=0.6)
    flush()
    lay = snowball(lay, W, H, 200, 425, 58, rng, lit=1.0)
    flush()
    # main mass
    lay = peony(lay, W, H, 300, 255, 82, PEONY, rng, lit=1.0)
    flush()
    lay = peony(lay, W, H, 500, 470, 116, PEONY, rng, lit=0.62)
    flush()
    lay = rose(lay, W, H, 222, 545, 70, ROSE, rng, lit=0.95)
    flush()
    lay = peony(lay, W, H, 345, 420, 132, PEONY_W, rng, lit=1.05)
    flush()
    lay = rose(lay, W, H, 415, 605, 60, ROSE, rng, lit=0.7)
    lay = rose(lay, W, H, 585, 612, 50, ("#f2b8a0", "#c06a58", "#3a1410"), rng, lit=0.5)
    lay = rose(lay, W, H, 630, 410, 34, ROSE, rng, lit=0.5)
    flush()
    # front leaves spilling over the rim, a drooping tulip over the ledge
    for (x, y, L, a) in [(300, 650, 160, 2.3), (420, 655, 170, 0.6), (250, 620, 140, 2.8), (470, 640, 150, 0.15)]:
        lay = leaf(lay, W, H, x, y, L, a, rng, lit=0.55)
    lay = stem(lay, W, H, [(420, 660), (520, 700), (590, 780), (610, 850)], 6, lit=0.5)
    lay = tulip(lay, W, H, 611, 850, 46, 1.4, rng, lit=0.5)
    flush()
    # fallen petals + a butterfly resting on the ledge
    lay, _ = paint(lay, W, H, petal_pts(150, 962, 58, 24, 0.25, n=14, cup=0.4), (150, 962), 0.25, 58, PEONY, (175, 962), 40, hi="#fff6ee", lit=1.0)
    lay, _ = paint(lay, W, H, petal_pts(215, 992, 42, 17, -0.6, n=14, cup=-0.4), (215, 992), -0.6, 42, ROSE, (230, 980), 30, lit=1.0)
    lay = butterfly(lay, W, H, 128, 636, 30, rng, ang=-0.35)
    flush()
    lay = finish(lay, light=(0.3, 0.24), radius=0.78)
    preview(lay, "flora-still", bg=BG)
    save_rgb(lay, f"{OUT}/still.webp", size=(780, 1131), quality=80)


def p_rose():
    W = H = 300
    rng = random.Random(7)
    lay = blank(W, H)
    lay = leaf(lay, W, H, 150, 160, 120, 0.5, rng, lit=0.8)
    lay = leaf(lay, W, H, 150, 160, 110, 2.5, rng, lit=0.6)
    lay = rose(lay, W, H, 150, 150, 80, ROSE, rng)
    lay = finish(lay, light=(0.2, 0.15), radius=1.4, varnish=0.12)
    preview(lay, "flora-rose", bg=BG)
    save(lay, f"{OUT}/rose.webp", max_w=150)


def p_tulip():
    W, H = 260, 640
    rng = random.Random(9)
    lay = blank(W, H)
    lay = leaf(lay, W, H, 130, 600, 300, -1.95, rng, lit=0.8, cup=0.5)
    lay = stem(lay, W, H, [(130, 630), (128, 400), (140, 200), (138, 160)], 7)
    lay = tulip(lay, W, H, 138, 168, 84, -1.6, rng)
    lay = leaf(lay, W, H, 130, 620, 260, -1.2, rng, lit=0.6, cup=-0.4)
    lay = finish(lay, light=(0.2, 0.1), radius=1.6, varnish=0.12)
    preview(lay, "flora-tulip", bg=BG)
    save(lay, f"{OUT}/tulip.webp", max_w=130)


def p_sprig():
    W, H = 640, 170
    rng = random.Random(13)
    lay = blank(W, H)
    lay = stem(lay, W, H, [(30, 110), (200, 92), (320, 86), (440, 92), (610, 110)], 4)
    for (x, y, L, a) in [(250, 90, 90, math.pi + 0.3), (180, 96, 80, math.pi - 0.25), (390, 90, 90, -0.3), (460, 96, 80, 0.25)]:
        lay = leaf(lay, W, H, x, y, L, a, rng, lit=0.8)
    lay = rose(lay, W, H, 320, 82, 46, ROSE, rng)
    lay = larkspur(lay, W, H, [(70, 108), (110, 100), (150, 96)], rng)
    lay = larkspur(lay, W, H, [(570, 108), (530, 100), (490, 96)], rng)
    lay = finish(lay, light=(0.3, 0.1), radius=1.8, varnish=0.12)
    preview(lay, "flora-sprig", bg=BG)
    save(lay, f"{OUT}/sprig.webp", max_w=320)


def p_butterfly():
    W, H = 260, 220
    rng = random.Random(17)
    lay = butterfly(blank(W, H), W, H, 130, 120, 90, rng, ang=0.0)
    lay = finish(lay, light=(0.2, 0.2), radius=1.8, varnish=0.1)
    preview(lay, "flora-butterfly", bg=BG)
    save(lay, f"{OUT}/butterfly.webp", max_w=120)


def p_petal():
    W, H = 200, 140
    rng = random.Random(19)
    lay = blank(W, H)
    lay, _ = paint(lay, W, H, petal_pts(40, 70, 120, 46, 0.1, n=16, cup=0.5), (40, 70), 0.1, 120, PEONY, (110, 60), 60, hi="#fff6ee", cast=0)
    lay = finish(lay, light=(0.2, 0.2), radius=1.8, varnish=0.1)
    preview(lay, "flora-petal", bg=BG)
    save(lay, f"{OUT}/petal.webp", max_w=70)


for p in PARTS:
    {"still": p_still, "rose": p_rose, "tulip": p_tulip, "sprig": p_sprig, "butterfly": p_butterfly, "petal": p_petal}[p]()
    flush()
kb(OUT)
