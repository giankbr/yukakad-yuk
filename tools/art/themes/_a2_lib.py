"""Agent A2 helpers (papua-cendrawasih, ntt-tenun, kebun-tropis, telaga-kabut).
Builds on _j1_lib (bbox-cropped G/GP/LC/FO, batched strokes/shapes) and adds: gouache tropical flora, woven-cloth
renderer (ikat with warp blur, noken knot mesh), ridge/reflection helpers. Previews -> /tmp/pen/nb-A2/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _j1_lib import *  # noqa
import _p1_lib
import art as _art
from _jw_lib import blade, along, spiral_pts  # noqa  (read-only use)

PREV = "/tmp/pen/nb-A2/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV


def clear():
    _art._fbm_cache.clear()


def rgba(col, a):
    """Flat colour layer with alpha map a (for OV / glaze of tints)."""
    return np.concatenate([np.ones(a.shape + (3,), np.float32) * np.array(hex_rgb(col), np.float32), np.clip(a, 0, 1)[..., None]], -1)


def tint(dst, mask, col, amt=1.0):
    return over(dst, rgba(col, mask * amt))


def ring(W, H, cx, cy, r, w):
    return np.clip(circles(W, H, [(cx, cy, r)]) - circles(W, H, [(cx, cy, r - w)]), 0, 1)


def offset_curve(pts, d):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        out.append((pts[i][0] - dy / L * d, pts[i][1] + dx / L * d))
    return out


# ---------------------------------------------------------------- gouache flora (kebun-tropis)
def g_leaf_blade(art, W, H, pts, width, rng, nx, light, mid, dark, vein="#e9f5c8", tear=0.5, area=None):
    """Banana/strelitzia leaf in fresh gouache: two-tone halves, pale midrib, lighter side-vein strokes, torn margins."""
    poly = blade(W, H, pts, width)
    m = shape_mask(W, H, poly)
    if tear:
        cuts = []
        for j in range(4, len(pts) - 3, rng.randint(2, 4)):
            a, b = pts[j - 1], pts[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for side in (-1, 1):
                if rng.random() < tear:
                    aa = ang + side * 1.15
                    cuts.append(([(pts[j][0] + math.cos(aa) * width * .35, pts[j][1] + math.sin(aa) * width * .35),
                                  (pts[j][0] + math.cos(aa) * width * 1.4, pts[j][1] + math.sin(aa) * width * 1.4)], 3.2, None))
        if cuts:
            m = np.clip(m - strokes(W, H, cuts), 0, 1)
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, light, mid, seed=nx(), rough=2.0, streak=1.0)
    half = shape_mask(W, H, poly[:len(pts)] + pts[::-1]) * m
    art = GP(art, half, mid, dark, seed=nx(), rough=1.2, streak=1.0, density=0.9)
    veins = []
    for j in range(2, len(pts) - 2):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for side in (-1, 1):
            aa = ang + side * 1.05
            L = width * rng.uniform(0.75, 0.95)
            veins.append(([pts[j], (pts[j][0] + math.cos(aa) * L * .5 + math.cos(ang) * L * .1, pts[j][1] + math.sin(aa) * L * .5 + math.sin(ang) * L * .1),
                           (pts[j][0] + math.cos(aa) * L + math.cos(ang) * L * .35, pts[j][1] + math.sin(aa) * L + math.sin(ang) * L * .35)], 1.3, (0.1, 0.6)))
    vm = strokes(W, H, veins) * m
    art = OV(art, vm, lambda mm: rgba(vein, mm * 0.32))
    mid_r = strokes(W, H, [(pts[1:-1], width * 0.09, (0.02, 0.6))]) * m
    art = GP(art, mid_r, vein, mix(vein, light, .4), seed=nx(), rough=0.6, streak=0.6, density=0.85)
    return art


def g_leaf(art, W, H, x, y, L, ang, rng, nx, light, mid, vein="#e6f3c0", wd=0.36, area=None):
    m = shape_mask(W, H, deform(petal_pts(x, y, L, L * wd, ang, n=14), rng, 1, 0.04))
    if area is not None:
        np.maximum(area, m, out=area)
    art = GP(art, m, light, mid, seed=nx(), rough=1.4, streak=0.9)
    half = shape_mask(W, H, petal_pts(x, y, L * 0.98, L * wd * 0.48, ang + 0.1, n=12)) * m
    art = GP(art, half, mid, mix(mid, "#0d3020", .35), seed=nx(), rough=1.0, streak=0.8, density=0.75)
    vein_ = [(x + math.cos(ang) * L * t, y + math.sin(ang) * L * t) for t in [j / 12 for j in range(1, 11)]]
    return OV(art, strokes(W, H, [(vein_, max(1.4, L * 0.025), (0.05, 0.5))]) * m, lambda mm: rgba(vein, mm * 0.7))


def hibiscus(art, W, H, cx, cy, r, rng, nx, ang=None, light="#ff7a62", mid="#e8434e", deep="#a4142f", area=None):
    """Kembang sepatu: 5 broad fan petals painted one over the next (visible overlaps), gently ruffled rims,
    dark throat with radiating veins, long stamen column with yellow pollen."""
    ang = rng.uniform(0, math.tau) if ang is None else ang
    allm = np.zeros((H, W), np.float32)
    for k in range(5):
        a = ang + k * math.tau / 5 + rng.uniform(-.06, .06)
        pts = [(cx, cy)]
        for i in range(31):
            t = i / 30 * 2 - 1  # -1..1 across the petal
            rr = r * (0.9 + 0.1 * math.cos(t * 1.6)) * (1 + 0.035 * math.sin((t + 1) * math.pi * 3 + k))
            th = a + t * 0.78
            pts.append((cx + math.cos(th) * rr, cy + math.sin(th) * rr * 0.93))
        m = shape_mask(W, H, pts)
        np.maximum(allm, m, out=allm)
        art = GP(art, m, mix(light, "#ffb39a", rng.uniform(0, .25)), mix(light, mid, .5), seed=nx(), rough=1.0, streak=1.0)
        inner = gaussian_filter(circles(W, H, [(cx, cy, r * 0.55)]), r * 0.18) * m
        art = OV(art, inner, lambda mm: rgba(mid, mm * 0.75))
        side = [(cx, cy)] + [(cx + math.cos(a - 0.8 + q * 0.03) * r * 1.1, cy + math.sin(a - 0.8 + q * 0.03) * r * 1.1) for q in range(16)]
        sm = gaussian_filter(shape_mask(W, H, side), r * 0.06) * m
        art = OV(art, sm, lambda mm: rgba(deep, mm * 0.3))
        fold = strokes(W, H, [([(cx, cy), (cx + math.cos(a + .05) * r * .55, cy + math.sin(a + .05) * r * .55), (cx + math.cos(a) * r * .85, cy + math.sin(a) * r * .85)], r * 0.05, (0.1, 0.6))]) * m
        art = OV(art, gaussian_filter(fold, 1.5), lambda mm: rgba("#ffd0bc", mm * 0.4))
        rim = np.clip(m - gaussian_filter(m, 1.6) * 1.1, 0, 1)
        art = OV(art, rim, lambda mm: rgba(deep, mm * 0.6))
    if area is not None:
        np.maximum(area, allm, out=area)
    throat = circles(W, H, [(cx, cy, r * 0.26)])
    art = OV(art, gaussian_filter(throat, r * 0.08) * allm, lambda mm: rgba(deep, np.clip(mm * 1.3, 0, 0.95)))
    vs = []
    for k in range(30):
        a = ang + k * math.tau / 30 + rng.uniform(-.05, .05)
        L = r * rng.uniform(0.4, 0.72)
        vs.append(([(cx, cy), (cx + math.cos(a + .06) * L * .5, cy + math.sin(a + .06) * L * .5), (cx + math.cos(a) * L, cy + math.sin(a) * L)], 1.2, (0.0, 0.75)))
    art = OV(art, strokes(W, H, vs) * allm, lambda mm: rgba(deep, mm * 0.4))
    sa = ang + rng.uniform(-.6, .6) + 0.3
    ex, ey = cx + math.cos(sa) * r * 0.95, cy + math.sin(sa) * r * 0.95
    col = strokes(W, H, [(curve([(cx, cy), ((cx + ex) / 2 + 3, (cy + ey) / 2 - 3), (ex, ey)], 14), r * 0.07, (0.0, 0.2))])
    art = GP(art, col, "#fbd8c6", "#e88f86", seed=nx(), rough=0.6, pad=8)
    dots_ = [(ex + rng.gauss(0, r * .06), ey + rng.gauss(0, r * .06), r * 0.03) for _ in range(9)]
    dots_ += [(ex + math.cos(sa) * r * .06, ey + math.sin(sa) * r * .06, r * 0.035)]
    art = GP(art, circles(W, H, dots_), "#ffd23a", "#f0a51c", seed=nx(), rough=0.5, pad=6)
    art = GP(art, circles(W, H, [(ex + math.cos(sa) * r * .08, ey + math.sin(sa) * r * .08, r * 0.04)]), "#c2183a", seed=nx(), rough=0.4, pad=6)
    return art


def frangipani(art, W, H, cx, cy, r, rng, nx, rot=None, tilt=1.0, edge="#f5b0a2", area=None):
    """Kamboja: five oblong pinwheel petals (each skewed off-axis and painted over the previous one), warm yellow heart."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    allm = np.zeros((H, W), np.float32)
    for k in range(5):
        a = rot + k * math.tau / 5
        ox, oy = math.cos(a + math.pi / 2) * r * 0.16, math.sin(a + math.pi / 2) * r * 0.16
        p = petal_pts(cx + ox * 0.4, cy + oy * 0.4, r, r * 0.36, a + 0.12, n=18, cup=0.6)
        p = [(cx + (x - cx), cy + (y - cy) * tilt) for x, y in p]
        m = shape_mask(W, H, p)
        np.maximum(allm, m, out=allm)
        art = OV(art, np.roll(np.roll(m, 3, 0), 2, 1), lambda mm: rgba("#7d8a6a", gaussian_filter(mm, 3) * 0.3), pad=10)
        art = GP(art, m, "#fffef8", "#f7f0e0", seed=nx(), rough=0.7, streak=0.6, pad=8)
        rim = np.clip(m - gaussian_filter(m, 1.8) * 1.12, 0, 1)
        art = OV(art, rim, lambda mm: rgba("#c9b9a2", mm * 0.6), pad=6)
        tipm = m * np.clip(gaussian_filter(circles(W, H, [(cx + math.cos(a + .12) * r * .95, cy + math.sin(a + .12) * r * .95 * tilt, r * 0.3)]), r * .1) * 1.5, 0, 1)
        art = OV(art, tipm, lambda mm: rgba(edge, mm * 0.35), pad=6)
    if area is not None:
        np.maximum(area, allm, out=area)
    heart = gaussian_filter(circles(W, H, [(cx, cy, r * 0.4)]), r * 0.16) * allm
    art = OV(art, heart, lambda mm: rgba("#f7c430", np.clip(mm * 1.7, 0, 0.95)), pad=8)
    spokes = [([(cx, cy), (cx + math.cos(rot + k * math.tau / 5 + .3) * r * .45, cy + math.sin(rot + k * math.tau / 5 + .3) * r * .45 * tilt)], 1.2, (0, .7)) for k in range(5)]
    return OV(art, strokes(W, H, spokes) * allm, lambda mm: rgba("#e39a1e", mm * 0.5), pad=6)


def strelitzia(art, W, H, x, y, s, ang, rng, nx, flip=1):
    """Bird-of-paradise flower: green-magenta beak spathe, fan of orange sepals, blue tongue; (x,y) = spathe base."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        v *= flip
        return (x + u * s * ca - v * s * sa, y + u * s * sa + v * s * ca)
    spathe = [P(0, 0), P(0.35, -0.12), P(0.8, -0.16), P(1.25, -0.08), P(1.42, 0.02), P(1.2, 0.08), P(0.75, 0.1), P(0.3, 0.08)]
    m = shape_mask(W, H, spathe)
    art = GP(art, m, "#3f8f5a", "#7b3d73", seed=nx(), rough=1.0, streak=1.0, pad=10)
    top = shape_mask(W, H, spathe[:5] + [P(1.0, -0.06), P(0.4, -0.04)]) * m
    art = OV(art, top, lambda mm: rgba("#b04a6a", mm * 0.55))
    art = OV(art, strokes(W, H, [([P(0.1, 0.0), P(0.7, -0.08), P(1.3, -0.03)], s * 0.025, (0.1, .4))]), lambda mm: rgba("#e7f0c0", mm * 0.6))
    # orange sepals fanning up/back from the top of the spathe
    for k, (u, va, L) in enumerate([(0.55, -2.1, 0.95), (0.62, -1.75, 1.05), (0.7, -1.45, 0.92), (0.78, -1.2, 0.75)]):
        bx, by = P(u, -0.12)
        a = ang + flip * va + rng.uniform(-.05, .05)
        p = petal_pts(bx, by, s * L, s * 0.11, a, n=12)
        mm = shape_mask(W, H, p)
        art = GP(art, mm, "#ffb22a", "#f2701d", seed=nx(), rough=0.8, streak=0.9, pad=8)
        art = OV(art, strokes(W, H, [([(bx, by), (bx + math.cos(a) * s * L * .8, by + math.sin(a) * s * L * .8)], s * 0.018, (0.1, .5))]) * mm, lambda q: rgba("#ffe08a", q * 0.6))
    # blue tongue (arrow)
    bx, by = P(0.66, -0.12)
    a = ang + flip * -1.0
    tp = [(bx, by), (bx + math.cos(a - .12) * s * .5, by + math.sin(a - .12) * s * .5), (bx + math.cos(a) * s * .72, by + math.sin(a) * s * .72),
          (bx + math.cos(a + .14) * s * .5, by + math.sin(a + .14) * s * .5)]
    art = GP(art, shape_mask(W, H, tp, smooth=False), "#3c5bd6", "#24318f", seed=nx(), rough=0.6, pad=8)
    return art


# ---------------------------------------------------------------- woven cloth
def ikat_render(motif, palette, thread=3, blur=2.2, seed=1, weft=2):
    """Render a motif index map (h x w ints into palette) as woven ikat cloth.
    Each motif cell = `thread` warp threads wide. Ikat blur: every warp thread shifts the dyed pattern up/down by a
    random amount (resist-dyed threads slip before weaving), so colour edges feather into ragged vertical streaks.
    Then thread relief: rounded warp threads, fine weft ticks, fibre noise. Returns opaque RGBA float."""
    rng = np.random.default_rng(seed)
    mh, mw = motif.shape
    W, H = mw * thread, mh * thread
    pal = np.array([hex_rgb(c) for c in palette], np.float32)
    # upsample in thread space
    big = np.repeat(np.repeat(motif, thread, 0), thread, 1)
    # per-warp shift (smooth-ish along x, larger near pattern edges)
    shift = gaussian_filter(rng.normal(0, 1, W).astype(np.float32), 1.2) * blur * thread
    shift += rng.normal(0, 0.6, W).astype(np.float32) * thread * 0.5
    yy, xx = np.mgrid[0:H, 0:W]
    # streak (bleed) of dye along the thread: small random length per pixel
    sy = (yy + np.round(shift[None, :] + gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), (2.0, 0.3)) * thread * 0.5).astype(int)) % H
    idx = big[sy, xx]
    rgb = pal[idx]
    # dye unevenness per thread
    rgb *= (0.9 + 0.12 * rng.random(W).astype(np.float32))[None, :, None]
    # warp thread relief (rounded): darker at thread borders
    u = (np.arange(W) % thread) / thread
    rel = 0.78 + 0.28 * np.sin(u * math.pi) ** 0.8
    rgb *= rel[None, :, None]
    # weft crossings: tiny horizontal ticks every `weft` px, alternating per thread (plain weave)
    wv = (((yy // weft) + (xx // thread)) % 2).astype(np.float32)
    rgb *= (0.92 + 0.08 * wv)[..., None]
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (1.2, 0.3))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    rgb *= (1 + fib * 0.04)[..., None]
    return np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)


def stamp(grid, glyph, y, x, val=None):
    """Place an ASCII glyph (list of strings) into an int grid: chars map via dict or '#'->val."""
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch == " " or ch == ".":
                continue
            v = val if val is not None and ch == "#" else ({"#": 1, "o": 2, "x": 3, "c": 4, "r": 1, "y": 3}.get(ch, 1) if val is None else val)
            yy, xx = y + j, x + i
            if 0 <= yy < grid.shape[0] and 0 <= xx < grid.shape[1]:
                grid[yy, xx] = v


def mirror_glyph(g):
    return [row[::-1] for row in g]


# ---------------------------------------------------------------- landscape (telaga, ntt)
def ridge_mask(W, H, base, amp, seed, freq=3.0, sharp=0.6, bottom=None):
    rng = random.Random(seed)
    ph = [rng.uniform(0, 6.28) for _ in range(4)]
    pts = [(-30, (bottom if bottom is not None else H) + 30)]
    for i in range(0, W + 61, 6):
        x = i - 30
        t = x / W
        v = (0.55 * math.sin(t * freq * math.pi + ph[0]) + 0.3 * math.sin(t * freq * 2.3 * math.pi + ph[1]) + 0.15 * math.sin(t * freq * 5.1 * math.pi + ph[2]))
        v = math.copysign(abs(v) ** sharp, v)
        pts.append((x, base - amp * v + rng.gauss(0, amp * 0.015)))
    pts.append((W + 30, (bottom if bottom is not None else H) + 30))
    return shapes(W, H, [pts], smooth=False)


def pine_items(x, by, h, rng, lean=0.0):
    """A fir/pine silhouette as stroke items: trunk + drooping tiered branch strokes."""
    items = [([(x, by), (x + lean * h, by - h)], max(1.0, h * 0.03), (0.0, 0.9))]
    tiers = int(8 + h / 18)
    for k in range(tiers):
        t = k / (tiers - 1)
        yy = by - h * (0.12 + 0.88 * t)
        cx = x + lean * h * (0.12 + 0.88 * t)
        L = h * (0.32 * (1 - t) ** 1.05 + 0.03) * rng.uniform(0.8, 1.15)
        for side in (-1, 1):
            items.append(([(cx, yy), (cx + side * L * 0.5, yy + L * 0.12), (cx + side * L, yy + L * 0.32)], max(1.2, h * 0.035 * (1 - t * .6)), (0.05, 0.6)))
    return items


def hair_strokes(mask, n, L, width, ang, rng, jitter=0.35, curve_amt=0.15, thr=0.5):
    """Short tapered brush strokes scattered inside mask, flowing along `ang` (float or fn(x,y)->ang)."""
    ys, xs = np.where(mask > thr)
    if len(xs) == 0:
        return []
    items = []
    for _ in range(n):
        i = rng.randrange(len(xs))
        x, y = float(xs[i]), float(ys[i])
        a = (ang(x, y) if callable(ang) else ang) + rng.gauss(0, jitter)
        l = L * rng.uniform(0.6, 1.3)
        bend = rng.gauss(0, curve_amt)
        pts = [(x + math.cos(a + bend * t) * l * t, y + math.sin(a + bend * t) * l * t) for t in [k / 7 for k in range(8)]]
        items.append((pts, width * rng.uniform(0.7, 1.3), (0.1, 0.6)))
    return items


def normals(pts):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        out.append((-dy / L, dx / L))
    return out


def pine_polys(x, by, h, rng, lean=0.0):
    """Fir/pine silhouette as overlapping drooping tier polygons (fill), plus a short trunk polygon."""
    polys = [[(x - h * 0.012, by), (x + lean * h - h * 0.006, by - h * 0.9), (x + lean * h + h * 0.006, by - h * 0.9), (x + h * 0.012, by)]]
    tiers = int(7 + h / 22)
    for k in range(tiers):
        t = k / (tiers - 1)
        yy = by - h * (0.1 + 0.9 * t)
        cx = x + lean * h * (0.1 + 0.9 * t)
        L = h * (0.24 * (1 - t) ** 0.95 + 0.025) * rng.uniform(0.82, 1.18)
        top = h * 0.11 * (1 - t * 0.5)
        polys.append([(cx, yy - top), (cx - L * 0.35, yy + L * 0.05), (cx - L * rng.uniform(.9, 1.1), yy + L * 0.42), (cx - L * 0.5, yy + L * 0.3),
                      (cx, yy + L * 0.36), (cx + L * 0.5, yy + L * 0.3), (cx + L * rng.uniform(.9, 1.1), yy + L * 0.42), (cx + L * 0.35, yy + L * 0.05)])
    polys.append([(x + lean * h, by - h * 1.04), (x + lean * h - h * 0.03, by - h * 0.9), (x + lean * h + h * 0.03, by - h * 0.9)])
    return polys
