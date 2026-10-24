"""Agent Q6 helpers (sakura-syari, koleksi-kupu, upacara-teh, malam-keakraban). Builds on _jw_lib (G/GP/LC/FO/OV,
strokes, shapes, circles, ellipses, Seq, outdir, save, preview ...). Previews -> /tmp/pen/nb-Q6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
import _p1_lib
from _jw_lib import *  # noqa
import _jw_lib as jw  # noqa
_p1_lib.PREV = "/tmp/pen/nb-Q6/art"
os.makedirs(_p1_lib.PREV, exist_ok=True)
import art as _art


def clear():
    _art._fbm_cache.clear()


def col3(h):
    return np.array(hex_rgb(h), np.float32)


def rgba(rgb, a):
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]], -1).astype(np.float32)


def flat(mask, col, a=1.0):
    return rgba(np.ones(mask.shape + (3,), np.float32) * col3(col), mask * a)


def dilate(mask, r):
    return np.clip(gaussian_filter(mask, r) * 3.0, 0, 1) if r > 0 else mask


def edge_ring(mask, r=1.2):
    return np.clip((mask - gaussian_filter(mask, r)) * 3, 0, 1)


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rotp(pts, cx, cy, a):
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def ramp_y(H, W, y0, y1):
    t = (np.arange(H, dtype=np.float32)[:, None] - y0) / max(1e-6, (y1 - y0))
    return np.clip(t, 0, 1) * np.ones((1, W), np.float32)


def ramp_x(H, W, x0, x1):
    t = (np.arange(W, dtype=np.float32)[None, :] - x0) / max(1e-6, (x1 - x0))
    return np.ones((H, 1), np.float32) * np.clip(t, 0, 1)


def shade(arr, mask, col, a):
    """Tint already-painted pixels inside mask toward col (keeps alpha)."""
    out = arr.copy()
    k = (np.clip(mask, 0, 1) * a)[..., None]
    out[..., :3] = out[..., :3] * (1 - k) + col3(col) * k
    return out


def bez(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / (n - 1) for i in range(n)]]


# ------------------------------------------------------------------ sakura (watercolour)
def sakura_petal_pts(cx, cy, L, ang, notch=0.18, wid=0.62, n=18):
    """One cherry petal: obovate with a notch at the tip; base at (cx, cy) pointing along ang."""
    pts = []
    for i in range(n + 1):
        t = i / n  # 0..1 along one side, base -> tip
        w = L * wid * 0.5 * math.sin(math.pi * min(1, t * 0.95)) ** 0.7 * (0.55 + 0.45 * t)
        pts.append((t * L, w))
    tip = [(L * (1 - notch * 0.9), 0.0)]
    right = [(x, -y) for x, y in pts[::-1]]
    poly = pts + tip + right
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in poly]


def blossom(art, W, H, cx, cy, r, rng, nx, light="#fbe1e6", mid="#f1b3c1", deep="#c96a86", rot=None, tilt=1.0, center="#b8455f"):
    """Five-petal sakura flower, loose watercolour; tilt<1 squashes it (seen at an angle)."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    area = np.zeros((H, W), np.float32)
    for k in range(5):
        a = rot + k * math.tau / 5 + rng.gauss(0, 0.09)
        L = r * rng.uniform(0.9, 1.08)
        pts = sakura_petal_pts(0, 0, L, a, notch=rng.uniform(0.12, 0.22), wid=rng.uniform(0.62, 0.78))
        pts = [(cx + x, cy + y * tilt) for x, y in pts]
        m = shapes(W, H, [deform(pts, rng, 1, 0.05)])
        area = np.maximum(area, m)
        art = G(art, m, light, mid, seed=nx(), density=rng.uniform(0.42, 0.6), edge=0.55, bloom=0.45, rough=2.4, feather=1.0, gran=0.2)
        # flush of colour toward the petal base
        base = shapes(W, H, [[(cx + x * 0.5, cy + y * 0.5 * tilt) for x, y in sakura_petal_pts(0, 0, L, a, wid=0.5)]])
        art = G(art, base, mid, deep, seed=nx(), density=0.5, edge=0.25, bloom=0.2, rough=1.6, feather=2.2)
    heart = circles(W, H, [(cx, cy, r * 0.16)])
    art = G(art, heart, deep, center, seed=nx(), density=0.55, edge=0.4, bloom=0, rough=1.2, feather=1.0)
    st, tips = [], []
    for k in range(11):
        a = rot + k * math.tau / 11 + rng.gauss(0, 0.15)
        L = r * rng.uniform(0.3, 0.46)
        x1, y1 = cx + math.cos(a) * L, cy + math.sin(a) * L * tilt
        st.append(([(cx, cy), (x1, y1)], max(0.8, r * 0.022), (0.0, 0.2)))
        tips.append((x1, y1, max(1.1, r * 0.04)))
    art = OV(art, strokes(W, H, st), lambda q: flat(q, "#a8445e", 0.55))
    art = OV(art, circles(W, H, tips), lambda q: flat(q, "#b9773e", 0.85))
    return art, area


def sakura_bud(art, W, H, x, y, s, ang, rng, nx):
    m = shapes(W, H, [deform(petal_pts(x, y, s, s * 0.6, ang, n=10), rng, 1, 0.06)])
    art = G(art, m, "#f3a6b8", "#d9708e", seed=nx(), density=0.7, edge=0.6, bloom=0.2, rough=2, feather=0.9)
    cal = shapes(W, H, [petal_pts(x, y, s * 0.45, s * 0.5, ang, n=8)])
    art = G(art, cal, "#9a5a4a", "#6e3a34", seed=nx(), density=0.6, edge=0.4, bloom=0, rough=1.5, feather=0.8)
    return art


def bark_branch(art, W, H, pts, width, rng, nx, col="#6e4a4a", col2="#4a2f33"):
    """Watercolour branch: tapered wash + darker dry-brush edge + lenticel ticks."""
    m = strokes(W, H, [(pts, width, (0.0, 0.85))])
    art = G(art, m, col, col2, seed=nx(), density=0.78, edge=0.6, bloom=0.25, rough=2.0, feather=0.9, gran=0.45)
    shadow = strokes(W, H, [([(x + width * 0.18, y + width * 0.2) for x, y in pts], width * 0.45, (0.0, 0.85))]) * m
    art = G(art, shadow, col2, seed=nx(), density=0.5, edge=0.3, bloom=0, rough=1.2, feather=0.8)
    ticks = []
    for i in range(1, len(pts) - 1, 2):
        x, y = pts[i]
        t = i / len(pts)
        w = width * (1 - t * 0.85)
        if w < 3:
            continue
        ticks.append(([(x - w * 0.25, y + rng.uniform(-1, 1)), (x + w * 0.25, y + rng.uniform(-1, 1))], 1.4, None))
    if ticks:
        art = OV(art, strokes(W, H, ticks) * m, lambda q: flat(q, "#d9c0b0", 0.45))
    return art


# ------------------------------------------------------------------ butterflies (gouache + ink)
from scipy.ndimage import distance_transform_edt


def wing_pts(cx, cy, s, sp, side, fore=True):
    """Wing outline (setting-board pose); side = +1 right / -1 left. Units of s, y down."""
    if fore:
        L, Wd, sw = sp["fl"], sp["fw"], sp.get("fs", 0.0)
        ctrl = [(0.0, -0.03), (0.22 * L, -0.2 * Wd - 0.05), (0.55 * L, -0.62 * Wd - sw * 0.6), (0.86 * L, -0.98 * Wd - sw),
                (1.0 * L, -1.08 * Wd - sw), (1.03 * L, -0.92 * Wd - sw * 0.8), (0.96 * L, -0.5 * Wd), (0.86 * L, -0.1 * Wd),
                (0.74 * L, 0.12 * Wd), (0.42 * L, 0.14 * Wd), (0.1 * L, 0.07)]
    else:
        L, Wd, tail = sp["hl"], sp["hw"], sp.get("tail", 0.0)
        ctrl = [(0.03, 0.02), (0.38 * L, -0.04), (0.74 * L, 0.12 * Wd), (0.96 * L, 0.42 * Wd), (0.9 * L, 0.72 * Wd), (0.7 * L, 0.95 * Wd)]
        if tail:
            ctrl += [(0.56 * L, 1.0 * Wd), (0.5 * L, 1.0 * Wd + tail * 0.6), (0.44 * L, 1.0 * Wd + tail), (0.4 * L, 1.0 * Wd + tail * 0.45), (0.38 * L, 0.98 * Wd)]
        ctrl += [(0.3 * L, 0.96 * Wd), (0.12 * L, 0.7 * Wd), (0.02 * L, 0.34 * Wd), (0.0, 0.12)]
    return [(cx + side * x * s, cy + y * s) for x, y in ctrl]


def butterfly(art, W, H, cx, cy, s, sp, rng, nx, ink="#2a221c"):
    """A pinned specimen, wings spread (setting-board pose). Gouache wings with scale streaks, a noisy scalloped
    border band with submarginal spots, ink veins, and a velvety body."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang_field = np.arctan2(yy - cy, np.abs(xx - cx) + 1e-3)
    rad = np.hypot(xx - cx, yy - cy)
    streak = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), 1.0)
    # radial scale streaks: sample noise along angle so streaks run from the body outward
    rays = np.sin(ang_field * 160 + fbm(W, H, nx(), 30, 2) * 6) * 0.5 + 0.5
    allw = np.zeros((H, W), np.float32)
    wings = []
    for fore in (False, True):
        for side in (-1, 1):
            pts = curve(wing_pts(cx, cy, s, sp, side, fore), 80)
            m = shapes(W, H, [deform(pts, rng, 1, 0.012)], smooth=False)
            wings.append((m, fore, side, pts))
    for m, fore, side, pts in wings:
        allw = np.maximum(allw, m)
        c1, c2 = (sp["fore"] if fore else sp["hind"])
        art = GP(art, m, c1, c2, seed=nx(), rough=0.8, streak=0.4)
        art = shade(art, m * rays * 0.6, sp.get("base", ink), 0.10)
        # iridescent / lighter disc
        if sp.get("glow"):
            L = sp["fl"] if fore else sp["hl"]
            gx, gy = cx + side * L * s * 0.45, cy + (-0.35 if fore else 0.35) * s * (sp["fw"] if fore else sp["hw"])
            disc = np.clip(1 - np.hypot(xx - gx, yy - gy) / (s * 0.42), 0, 1) ** 1.5
            art = shade(art, m * disc, sp["glow"], 0.55)
        # basal dusting
        near = np.clip(1 - rad / (s * (0.5 if fore else 0.38)), 0, 1) ** 1.2
        art = shade(art, m * near, sp.get("base", ink), 0.6)
        # pattern
        pat = sp.get("pattern")
        L = sp["fl"] if fore else sp["hl"]
        Wd = sp["fw"] if fore else sp["hw"]
        if pat == "band" and fore:
            bp = curve([(cx + side * L * s * 0.2, cy - Wd * s * 0.08), (cx + side * L * s * 0.55, cy - Wd * s * 0.5), (cx + side * L * s * 0.84, cy - Wd * s * 0.88)], 20)
            bm = strokes(W, H, [(bp, s * sp.get("bandw", 0.1), (0.3, 0.25))]) * m
            bm = displace(bm, nx(), 3, 10)
            art = GP(art, bm, sp["bandc"], mix(sp["bandc"], "#ffffff", 0.25), seed=nx(), rough=1.2, streak=0.6)
        if pat == "band" and not fore and sp.get("hband"):
            bp = curve([(cx + side * L * s * 0.25, cy + Wd * s * 0.1), (cx + side * L * s * 0.5, cy + Wd * s * 0.5), (cx + side * L * s * 0.48, cy + Wd * s * 0.9)], 20)
            bm = displace(strokes(W, H, [(bp, s * 0.07, (0.3, 0.3))]) * m, nx(), 3, 10)
            art = GP(art, bm, sp["hband"], sp["hband"], seed=nx(), rough=1, streak=0.5)
        if pat == "dots" and fore:
            ds = [(cx + side * L * s * u, cy - Wd * s * v, s * r) for u, v, r in ((0.5, 0.45, 0.06), (0.68, 0.66, 0.05), (0.36, 0.2, 0.04))]
            art = GP(art, displace(circles(W, H, ds), nx(), 2, 8) * m, sp["bandc"], mix(sp["bandc"], "#000000", 0.15), seed=nx(), rough=0.8)
        if pat == "eye" and not fore:
            ex, ey = cx + side * L * s * 0.55, cy + Wd * s * 0.55
            for rr, cc in ((0.15, sp["eye"][0]), (0.105, sp["eye"][1]), (0.045, sp["eye"][2])):
                em = shapes(W, H, [deform(ellipse_pts(ex, ey, rr * s, rr * s * 0.92, 14), rng, 1, 0.04)])
                art = GP(art, em * m, cc, mix(cc, "#000000", 0.15), seed=nx(), rough=0.6, streak=0.3)
            art = OV(art, circles(W, H, [(ex - s * 0.02, ey - s * 0.025, s * 0.016)]), lambda q: flat(q, "#ffffff", 0.85))
        if pat == "eye" and fore:
            ex, ey = cx + side * L * s * 0.78, cy - Wd * s * 0.78
            for rr, cc in ((0.06, sp["eye"][0]), (0.035, sp["eye"][1])):
                art = GP(art, circles(W, H, [(ex, ey, rr * s)]) * m, cc, cc, seed=nx(), rough=0.5)
        if pat == "glass" and fore:
            gp = [(cx + side * L * s * 0.4, cy - Wd * s * 0.45), (cx + side * L * s * 0.72, cy - Wd * s * 0.78), (cx + side * L * s * 0.74, cy - Wd * s * 0.4), (cx + side * L * s * 0.52, cy - Wd * s * 0.12)]
            gm = displace(shapes(W, H, [gp]), nx(), 3, 12) * m
            art = shade(art, gm, sp["bandc"], 0.7)
        # scalloped border band from the distance to the wing edge
        if sp.get("border"):
            dist = distance_transform_edt(m > 0.5).astype(np.float32)
            bw = s * sp.get("bw", 0.085) * (0.75 + 0.5 * fbm(W, H, nx(), 18, 2))
            # body side has no border
            far = np.clip((rad - s * 0.28) / (s * 0.12), 0, 1)
            band = np.clip((bw - dist) / 2.0, 0, 1) * m * far
            art = shade(art, band, sp["border"], 0.94)
            if sp.get("spots"):
                pts = wing_pts(cx, cy, s, sp, side, fore)
                pts = curve(pts, 80)
                gx, gy = float((xx * m).sum() / m.sum()), float((yy * m).sum() / m.sum())
                sp_items = []
                for x, y, _ in along(pts, s * (0.115 if fore else 0.125)):
                    if math.hypot(x - cx, y - cy) < s * 0.42 or rng.random() < 0.2:
                        continue
                    dx, dy = gx - x, gy - y
                    d = math.hypot(dx, dy) + 1e-6
                    k = s * sp.get("bw", 0.085) * 0.55
                    sp_items.append((x + dx / d * k, y + dy / d * k, s * rng.uniform(0.01, 0.024)))
                if sp_items:
                    art = OV(art, displace(circles(W, H, sp_items), nx(), 1.2, 6) * band, lambda q: flat(q, sp["spots"], 0.9))
        # veins
        vs = []
        n = 7 if fore else 6
        for k in range(n):
            a = (-1.15 + k * 0.24) if fore else (0.0 + k * 0.27)
            Lr = L * s * (1.05 if fore else 0.95)
            ex, ey = cx + side * math.cos(a) * Lr, cy + math.sin(a) * Lr
            mx, my = cx + side * math.cos(a * 0.9) * Lr * 0.42, cy + math.sin(a * 0.9) * Lr * 0.42
            vs.append((curve([(cx + side * s * 0.04, cy), (mx, my), (ex, ey)], 12), max(0.8, s * 0.01), (0.05, 0.3)))
        cell = curve([(cx + side * s * 0.06, cy - (0.05 if fore else -0.05) * s), (cx + side * L * s * 0.45, cy + (-0.32 if fore else 0.3) * s * Wd), (cx + side * L * s * 0.52, cy + (-0.1 if fore else 0.12) * s * Wd)], 12)
        vs.append((cell, max(0.8, s * 0.009), None))
        art = OV(art, strokes(W, H, vs) * m, lambda q: flat(q, sp.get("vein", ink), 0.45))
    # wing edge: thin dark line + fringe dashes (cilia)
    art = OV(art, edge_ring(allw, 0.9), lambda q: flat(q, ink, 0.6))
    # body: abdomen, thorax (furry), head, palps, antennae with clubs
    abd = shapes(W, H, [deform(ellipse_pts(cx, cy + s * 0.2, s * 0.042, s * 0.27, 14), rng, 1, 0.02)])
    art = GP(art, abd, sp.get("body", "#3a2e24"), "#1d1712", seed=nx(), rough=0.5, streak=0.6)
    th = shapes(W, H, [ellipse_pts(cx, cy - s * 0.04, s * 0.06, s * 0.12, 14)])
    art = GP(art, th, "#2e241c", "#16110c", seed=nx(), rough=0.8, streak=1.0)
    fur = strokes(W, H, [([(cx + rng.uniform(-1, 1) * s * 0.05, cy - s * 0.12 + i * s * 0.02), (cx + rng.uniform(-1, 1) * s * 0.07, cy - s * 0.1 + i * s * 0.02)], 1.0, None) for i in range(10)]) * th
    art = OV(art, fur, lambda q: flat(q, "#6a5a48", 0.5))
    art = OV(art, strokes(W, H, [([(cx, cy + s * 0.0 + k * s * 0.05), (cx + s * 0.03, cy + s * 0.01 + k * s * 0.05)], 1.0, None) for k in range(8)]) * abd, lambda q: flat(q, "#8a7a62", 0.35))
    art = OV(art, circles(W, H, [(cx, cy - s * 0.18, s * 0.045)]), lambda q: flat(q, "#1d1712", 0.95))
    ant = []
    for side in (-1, 1):
        ant.append((bez((cx + side * s * 0.01, cy - s * 0.21), (cx + side * s * 0.07, cy - s * 0.5), (cx + side * s * 0.2, cy - s * 0.62), 16), max(0.9, s * 0.009), None))
    art = OV(art, strokes(W, H, ant), lambda q: flat(q, "#1d1712", 0.85))
    art = OV(art, ellipses(W, H, [(cx + side * s * 0.205, cy - s * 0.625, s * 0.012, s * 0.024, side * 35) for side in (-1, 1)]), lambda q: flat(q, "#1d1712", 0.9))
    return art, allw


def pin(art, W, H, x, y, s):
    """Entomology pin head (seen from above): small glossy black bead with highlight."""
    art = OV(art, circles(W, H, [(x + s * 0.25, y + s * 0.35, s * 1.0)]), lambda q: flat(gaussian_filter(q, s * 0.4), "#000000", 0.25))
    art = OV(art, circles(W, H, [(x, y, s)]), lambda q: flat(q, "#141414", 1))
    art = OV(art, circles(W, H, [(x - s * 0.3, y - s * 0.35, s * 0.35)]), lambda q: flat(q, "#d8d8d8", 0.9))
    return art
