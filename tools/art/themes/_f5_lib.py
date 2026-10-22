"""Agent F5 helpers (hutan-bambu, cahaya-lilin, ultah-balerina, pesta-kebun): builds on _e5_lib (gouache bodies,
bbox-local painting, crayon, sheen, spark, cut paper) and adds bamboo culms + leaves, candle flames and light, glass
glints, bokeh, tulle, velvet folds and string lights. Previews -> /tmp/pen/nb-F5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _e5_lib import *  # noqa
import _e5_lib, _d6_lib, _a6_lib, _j1_lib, _p1_lib
PREV = "/tmp/pen/nb-F5/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_e5_lib, _d6_lib, _a6_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def bamboo_leaf_pts(x, y, L, Wd, ang, bend=0.0, n=22):
    """Bamboo leaf: short petiole, widest at ~30%, long tapering tip, slight curve (bend)."""
    pts = []
    ca, sa = math.cos(ang), math.sin(ang)
    side = []
    for i in range(n + 1):
        u = i / n
        wd = Wd * (math.sin(math.pi * min(1, u / 0.32) * 0.5) if u < 0.32 else (1 - (u - 0.32) / 0.68) ** 0.9)
        side.append((u, wd))
    for u, wd in side:
        cx_, cy_ = u * L, bend * L * u * u
        pts.append((cx_, cy_ - wd))
    for u, wd in reversed(side[1:-1]):
        cx_, cy_ = u * L, bend * L * u * u
        pts.append((cx_, cy_ + wd * 0.85))
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]


def leaf_rib(x, y, L, ang, bend=0.0, n=12):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + (u * L) * ca - (bend * L * u * u) * sa, y + (u * L) * sa + (bend * L * u * u) * ca) for u in np.linspace(0.04, 0.85, n)]


def culm(art, W, H, x0, x1, y0, y1, width, nodes, nx, col, col2, dark, light, node_col, wash=False, alpha=1.0,
         lean=0.0, ring="#f4f0d8", seed_ring=1, stripe=None, sheath=0):
    """One bamboo culm from (x0, y0 bottom) to (x1, y1 top): gouache (near) or watercolour wash (far) body with
    cylindrical shading (lit left, shadow right), slight bulge at each node, node rings with a pale powdery band
    below, optional green stripes (golden bamboo) and papery sheaths on the lowest `sheath` nodes."""
    rng = random.Random(seed_ring + int(x0))
    def cx_at(y):
        t = (y - y0) / (y1 - y0)
        return x0 + (x1 - x0) * t + lean * math.sin(t * math.pi)
    def w_at(y):
        b = sum(math.exp(-((y - ny) / (width * 0.12)) ** 2) for ny in nodes)
        return width * (1 + 0.07 * min(1, b))
    ys = np.linspace(y0, y1, 160)
    left = [(cx_at(y) - w_at(y) / 2, y) for y in ys]
    right = [(cx_at(y) + w_at(y) / 2, y) for y in ys[::-1]]
    m = shapes(W, H, [left + right], smooth=False)
    m = np.clip(gaussian_filter(m, 0.6) * 1.2, 0, 1)
    b = bbox(m, 4, 0.01)
    y0b, y1b, x0b, x1b = b
    yy, xx = np.mgrid[y0b:y1b, x0b:x1b].astype(np.float32)
    tt = (yy - y0) / (y1 - y0)
    cxa = x0 + (x1 - x0) * tt + lean * np.sin(tt * math.pi)
    u = np.zeros_like(m)
    u[y0b:y1b, x0b:x1b] = (xx - cxa) / (width / 2)
    shade = np.clip((u - 0.15) / 0.85, 0, 1) ** 1.2 * m
    lit = np.exp(-((u + 0.42) / 0.2) ** 2) * m
    if wash:
        art = G(art, m, col, col2, seed=nx(), density=0.8 * alpha, edge=0.35, bloom=0.2, rough=1.5, feather=0.8, gran=0.2)
        art = G(art, shade, dark, seed=nx(), density=0.5 * alpha, edge=0.0, bloom=0, rough=1.0, feather=1.0, mottle=0.2)
    else:
        art = GP(art, m, col, col2, seed=nx(), rough=0.8, streak=0.6, density=alpha)
        mot = np.zeros_like(m)
        mot[y0b:y1b, x0b:x1b] = fbm(x1b - x0b, y1b - y0b, nx(), 90, 3)
        art = tint(art, np.clip((mot - 0.55) * 2.5, 0, 1) * m, mix(col, "#d9c25a", 0.6), 0.35, seed=nx())
        art = tint(art, shade, dark, 0.85, seed=nx())
        art = tint(art, lit, light, 0.6, seed=nx())
        st = stripes(W, H, math.pi / 2, 1.0, width * 0.18, wob=3.0, seed=nx()) * m
        art = tint(art, gaussian_filter(st, (5, 0.5)), dark, 0.16, seed=nx())
    if stripe:
        band = np.zeros_like(m)
        for c_, wd_ in ((-0.05, 0.13), (0.42, 0.09), (-0.62, 0.06)):
            band += np.exp(-((u - c_ - (fbm(W, H, 77, 60, 2) - 0.5) * 0.2) / wd_) ** 4)
        sel = np.zeros_like(m)
        for i in range(len(nodes) - 1):
            if rng.random() < 0.75:
                a_, b_ = sorted((nodes[i], nodes[i + 1]))
                sel[int(max(0, a_ + 4)):int(min(H, b_ - 4)), :] = 1
        sel = gaussian_filter(sel, (10, 0))
        art = tint(art, np.clip(band, 0, 1) * sel * m, stripe, 0.75, seed=nx())
    items, bands, sheaths = [], [], []
    for k, ny in enumerate(nodes):
        cx = cx_at(ny); wn = w_at(ny)
        tilt = rng.uniform(-2.0, 2.0)
        items.append(([(cx - wn * 0.52, ny + tilt), (cx, ny + rng.uniform(1.5, 3.5)), (cx + wn * 0.52, ny - tilt)], max(1.6, width * 0.075), (0.05, 0.05)))
        bands.append([(cx - wn / 2, ny + 3), (cx + wn / 2, ny + 3), (cx + wn / 2, ny + width * 0.4), (cx - wn / 2, ny + width * 0.4)])
        if k < sheath:
            sh = rng.choice((-1, 1))
            sheaths.append([(cx - wn * 0.54, ny + 3), (cx + wn * 0.56, ny + 3), (cx + sh * wn * 0.5, ny - width * 0.7), (cx + sh * wn * 0.3, ny - width * 1.25), (cx - sh * wn * 0.05, ny - width * 0.5)])
    if bands:
        bm = gaussian_filter(shapes(W, H, bands, smooth=False), width * 0.1) * m
        art = tint(art, bm, ring, 0.45 if not wash else 0.3, seed=nx())
        nm = strokes(W, H, items) * gaussian_filter(m, 0.5)
        if wash:
            art = G(art, nm, node_col, seed=nx(), density=0.7 * alpha, edge=0.2, bloom=0, rough=0.8, feather=0.6)
        else:
            art = crayon(art, nm, node_col, seed=nx(), amt=0.9, tooth=0.25)
            hi = strokes(W, H, [([(px, py - max(2.5, width * 0.08)) for px, py in it[0]], max(1.2, width * 0.04), (0.1, 0.4)) for it in items]) * m
            art = tint(art, hi * np.clip(1 - shade * 1.5, 0, 1), light, 0.7, seed=nx(), clip=True)
            dk = strokes(W, H, [([(px, py + max(3, width * 0.1)) for px, py in it[0]], max(1.2, width * 0.05), (0.1, 0.4)) for it in items]) * m
            art = tint(art, gaussian_filter(dk, 1.2), dark, 0.35, seed=nx())
    if sheaths:
        sm = shapes(W, H, sheaths)
        art = GP(art, sm, "#c9a46a", "#b58a52", seed=nx(), rough=2.4, streak=0.9, density=0.92)
        art = tint(art, side_light(sm, 4, 0, 4), "#7a5530", 0.5, seed=nx())
        fib = stripes(W, H, math.pi / 2 - 0.08, 0.8, 4.5, wob=1.5, seed=nx()) * sm
        art = tint(art, fib, "#8a6236", 0.35, seed=nx())
    return art, m


def leaf_spray(art, W, H, x, y, ang, n, L, Wd, nx, rng, cols, wash=True, droop=0.5, alpha=1.0, twig_col="#6b6a2c"):
    """A fan of bamboo leaves from a thin twig tip at (x, y); ang = mean pointing direction (radians)."""
    twig = []
    tx, ty = x - math.cos(ang) * L * 0.5, y - math.sin(ang) * L * 0.5
    twig.append(([(tx, ty), ((tx + x) / 2, (ty + y) / 2 + 2), (x, y)], max(1.4, Wd * 0.18), (0.0, 0.3)))
    art = G(art, strokes(W, H, twig), twig_col, seed=nx(), density=0.75 * alpha, edge=0.2, bloom=0, rough=0.6, feather=0.5) if wash else GP(art, strokes(W, H, twig), twig_col, seed=nx(), rough=0.4)
    for k in range(n):
        a = ang + (k - (n - 1) / 2) * rng.uniform(0.22, 0.36) + droop * 0.3
        ll = L * rng.uniform(0.75, 1.1)
        ww = Wd * rng.uniform(0.8, 1.1)
        bend = rng.uniform(0.04, 0.12) * (1 if math.cos(a) > 0 else -1)
        pts = deform(bamboo_leaf_pts(x, y, ll, ww, a, bend), rng, 1, 0.004)
        m = shapes(W, H, [pts])
        c = cols[rng.randrange(len(cols))]
        c2 = cols[rng.randrange(len(cols))]
        if wash:
            art = G(art, m, c, c2, seed=nx(), density=rng.uniform(0.7, 0.9) * alpha, edge=0.55, bloom=0.25, rough=1.2, feather=0.6, gran=0.25)
            rib = strokes(W, H, [(leaf_rib(x, y, ll, a, bend), max(0.8, ww * 0.12), (0.1, 0.6))])
            art = OV(art, rib * m, lambda mm: col_arr(mm, "#f6f1c8", mm * 0.35 * alpha), pad=4)
        else:
            art = GP(art, m, c, c2, seed=nx(), rough=0.8, streak=0.4, density=alpha)
            art = tint(art, side_light(m, 0, ww * 0.5, ww * 0.4), mix(c, "#000000", 0.35), 0.4, seed=nx())
    return art


def flame_mask(W, H, x, y, h, w, lean=0.0):
    """Teardrop candle flame with base at (x, y) rising h."""
    pts = []
    for i in range(28):
        t = i / 27 * math.tau
        u = (1 - math.cos(t)) / 2  # 0 at base..1 at tip
        r = w * math.sin(math.pi * u ** 0.6) * (1 - u) ** 0.35
        side = 1 if t < math.pi else -1
        px = x + side * r + lean * h * u * u
        py = y - u * h
        pts.append((px, py))
    return shapes(W, H, [pts])


def candle_flame(art, W, H, x, y, h, w, nx, lean=0.0, halo=1.0):
    """Painted flame: warm halo, orange body, yellow-white core, blue base, dark wick."""
    m = flame_mask(W, H, x, y, h, w, lean)
    if halo:
        hm = circles(W, H, [(x, y - h * 0.45, h * 0.9)])
        art = OV(art, hm, lambda mm: col_arr(mm, "#ffb347", np.clip(gaussian_filter(mm, h * 0.6), 0, 1) * 0.45 * halo), pad=int(h * 1.6))
        art = OV(art, hm, lambda mm: col_arr(mm, "#ffd98a", np.clip(gaussian_filter(mm, h * 0.25), 0, 1) * 0.35 * halo), pad=int(h * 0.8))
    art = OV(art, m, lambda mm: col_arr(mm, "#ff9a2e", np.clip(gaussian_filter(mm, 1.4) * 1.1, 0, 1) * 0.95), pad=8)
    core = flame_mask(W, H, x + lean * h * 0.05, y - h * 0.08, h * 0.72, w * 0.62, lean * 0.8)
    art = OV(art, core, lambda mm: col_arr(mm, "#ffe9a6", np.clip(gaussian_filter(mm, 1.6), 0, 1)), pad=8)
    inner = flame_mask(W, H, x, y - h * 0.12, h * 0.42, w * 0.36, lean * 0.6)
    art = OV(art, inner, lambda mm: col_arr(mm, "#fffaf0", np.clip(gaussian_filter(mm, 1.8), 0, 1) * 0.9), pad=8)
    base = ellipses(W, H, [(x, y - h * 0.06, w * 0.42, h * 0.08, 0)])
    art = OV(art, base, lambda mm: col_arr(mm, "#6f8cff", np.clip(gaussian_filter(mm, 1.5), 0, 1) * 0.55), pad=6)
    wick = strokes(W, H, [([(x, y + h * 0.1), (x + lean * 3, y - h * 0.12)], max(1.5, w * 0.16), None)])
    art = OV(art, wick, lambda mm: col_arr(mm, "#2a160c", mm * 0.95), pad=4)
    return art


def bokeh(art, W, H, items, seed=1):
    """Out-of-focus light discs: items = (x, y, r, col, alpha). Each disc slightly brighter rim, soft edge."""
    rng = random.Random(seed)
    for x, y, r, col, a in items:
        m = shapes(W, H, [deform(ellipse_pts(x, y, r, r * rng.uniform(0.92, 1.0), 12, rng.uniform(0, 3)), rng, 1, 0.01)])
        soft = gaussian_filter(m, max(1.0, r * rng.uniform(0.06, 0.14)))
        rimm = np.clip(soft - gaussian_filter(m, r * 0.35), 0, 1)
        art = OV(art, soft, lambda mm, a=a, col=col, rimm=rimm: col_arr(mm, col, np.clip(mm * a * 0.75 + 0, 0, 1)), pad=int(r * 0.6) + 4)
        art = OV(art, rimm, lambda mm, a=a, col=col: col_arr(mm, mix(col, "#fff0c8", 0.25), np.clip(mm * a * 0.9, 0, 1)), pad=4)
    return art


def tulle(art, mask, col, col2, nx, seed=1, alpha=0.6, mesh=True):
    """Layered tulle: translucent wash with a fine net texture and lighter gathered folds."""
    H, W = mask.shape
    art = G(art, mask, col, col2, seed=nx(), density=alpha, edge=0.45, bloom=0.15, rough=2.0, feather=1.0, gran=0.1)
    if mesh:
        b = bbox(mask, 2, 0.01)
        if b is not None:
            y0, y1, x0, x1 = b
            yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
            net = (np.abs(np.sin((xx + yy) * 0.9)) < 0.18) | (np.abs(np.sin((xx - yy) * 0.9)) < 0.18)
            nm = np.zeros_like(mask)
            nm[y0:y1, x0:x1] = net.astype(np.float32) * mask[y0:y1, x0:x1]
            art = OV(art, nm, lambda mm: col_arr(mm, "#ffffff", mm * 0.12), pad=2)
    return art


def catenary(x0, y0, x1, y1, sag, n=40):
    return [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in np.linspace(0, 1, n)]


def pillar_candle(art, W, H, cx, base_y, top_y, rw, nx, rng, wax="#efe2c8", wax2="#e6d3b0", shadow="#5a2e1e",
                  glowc="#ffc879", drips=6, ry_k=0.28):
    """Pillar candle lit by its own flame: melted concave top, warm translucent glow under the rim, wax drips, dark
    sides falling into the room's shadow. Returns art and the wick (x, y)."""
    ry = rw * ry_k
    body = shapes(W, H, [[(cx - rw, top_y), (cx + rw, top_y), (cx + rw * 0.99, base_y), (cx - rw * 0.99, base_y)]], smooth=False)
    body = np.maximum(body, ellipses(W, H, [(cx, base_y, rw * 0.99, ry, 0)]))
    body = np.maximum(body, ellipses(W, H, [(cx, top_y, rw, ry, 0)]))
    body = displace(body, nx(), 1.2, 30)
    art = GP(art, body, wax, wax2, seed=nx(), rough=0.6, streak=0.25)
    b = bbox(body, 2, 0.01)
    y0, y1, x0, x1 = b
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    u = (xx - cx) / rw
    v = np.clip((yy - top_y) / max(1, base_y - top_y), 0, 1)
    sh = np.zeros_like(body); gl = np.zeros_like(body)
    sh[y0:y1, x0:x1] = np.clip(np.clip(u + 0.15, 0, 2) ** 1.6 * 0.75 + np.clip(-u - 0.55, 0, 1) * 0.9 + v ** 1.3 * 0.7, 0, 1)
    gl[y0:y1, x0:x1] = np.exp(-(v / 0.3) ** 2) * np.clip(1 - np.abs(u) ** 2, 0, 1)
    soft = lambda f: gaussian_filter(f, 2.0)
    mott = 0.9 + 0.2 * fbm(W, H, nx(), 50, 3)
    art = over(art, col_arr(body, shadow, np.clip(soft(sh) * body * 0.82 * mott, 0, 1)))
    art = over(art, col_arr(body, glowc, np.clip(soft(gl) * body * 0.6, 0, 1)))
    # drips
    items = []
    for k in range(drips):
        a = rng.uniform(-0.9, 0.9)
        x = cx + a * rw
        L = rng.uniform(0.05, 0.34) * (base_y - top_y) * (1 - abs(a) * 0.4)
        y = top_y + ry * math.sqrt(max(0, 1 - a * a)) - 2
        items.append(([(x, y - 4), (x + rng.uniform(-1, 1), y + L * 0.5), (x, y + L)], rw * rng.uniform(0.08, 0.13), (0.0, 0.0)))
    dm = strokes(W, H, items)
    bulbs = circles(W, H, [(it[0][-1][0], it[0][-1][1], it[1] * 0.62) for it in items])
    dm = np.clip(dm + bulbs, 0, 1)
    dcol = np.clip(1 - soft(sh) * 0.9, 0, 1)
    art = over(art, col_arr(dm, "#f7e7c6", dm * 0.95))
    art = over(art, col_arr(dm, shadow, np.clip(dm * soft(sh) * 0.75, 0, 1)))
    art = over(art, col_arr(dm, glowc, np.clip(dm * soft(gl) * 0.5, 0, 1)))
    art = over(art, col_arr(dm, "#8a4a26", np.clip(side_light(dm, 3, 1, 2.0) * 0.6, 0, 1)))
    art = over(art, col_arr(dm, "#fff6e2", np.clip(side_light(dm, -2, -1, 1.5) * 0.7 * dcol, 0, 1)))
    # melted top pool + rim lip
    pool = ellipses(W, H, [(cx, top_y + ry * 0.12, rw * 0.84, ry * 0.7, 0)])
    art = tint(art, gaussian_filter(pool, 2), "#f9d590", 0.6, seed=nx())
    art = tint(art, gaussian_filter(pool * side_light(pool, 0, -ry * 0.3, ry * 0.25), 1), "#a8683a", 0.5, seed=nx())
    lip = np.clip(ellipses(W, H, [(cx, top_y, rw, ry, 0)]) - ellipses(W, H, [(cx, top_y + 1.5, rw * 0.9, ry * 0.78, 0)]), 0, 1)
    art = tint(art, gaussian_filter(lip, 0.8), "#fff4dc", 0.7, seed=nx())
    return art, (cx, top_y + ry * 0.1)


def glass_glints(art, mask, nx, col="#fff4dc", amt=0.9):
    """Edge highlights for a clear glass shape: bright rim on the lit side, faint body, dark refraction edge."""
    H, W = mask.shape
    art = OV(art, mask, lambda mm: col_arr(mm, "#f6e8d6", mm * 0.07), pad=4)
    edge = np.clip(mask - (gaussian_filter(mask, 2.2) > 0.96).astype(np.float32), 0, 1) * mask
    art = OV(art, edge, lambda mm: col_arr(mm, col, mm * 0.45 * amt), pad=4)
    return art


def edge_fade(art, px):
    """Fade alpha to zero at the canvas border (glows never show a hard sprite edge)."""
    h, w = art.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    out = art.copy()
    out[..., 3] *= np.clip(d / px, 0, 1) ** 1.5
    return out
