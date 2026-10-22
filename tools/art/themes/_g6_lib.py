"""Agent G6 helpers (perpustakaan-tua, film-analog, opera-beludru, imlek-keluarga): builds on _f5_lib (gouache
bodies, bbox-local painting, tint/side_light, cut paper, flames, bokeh) and adds leather book spines, wooden shelves,
velvet curtain folds, gilt mouldings, crystal drops, paper lanterns, plum blossoms, mandarin oranges, light leaks and
film grain. Previews -> /tmp/pen/nb-G6/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _f5_lib import *  # noqa
import _f5_lib, _e5_lib, _d6_lib, _a6_lib, _j1_lib, _p1_lib
PREV = "/tmp/pen/nb-G6/art"
os.makedirs(PREV, exist_ok=True)
for _m in (_f5_lib, _e5_lib, _d6_lib, _a6_lib, _j1_lib, _p1_lib):
    _m.PREV = PREV


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rot_poly(pts, ox, oy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]


def cyl_shade(mask, x0, x1, lit=-0.45):
    """Field across a vertical cylinder between x0..x1: returns (shadow, highlight) fields inside mask."""
    H, W = mask.shape
    xx = np.arange(W, dtype=np.float32)[None, :] * np.ones((H, 1), np.float32)
    u = (xx - (x0 + x1) / 2) / max(1, (x1 - x0) / 2)
    sh = np.clip((u - 0.1) / 0.9, 0, 1) ** 1.3 + np.clip(-u - 0.82, 0, 1) * 2.5
    hi = np.exp(-((u - lit) / 0.22) ** 2)
    return np.clip(sh, 0, 1) * mask, hi * mask


def book(art, W, H, x, base, w, h, col, col2, nx, rng, lean=0.0, gold="#c9a04e", bands=None, label=None, dark="#1a0f0a"):
    """One leather/cloth book spine standing on `base`, width w, height h, optionally leaning (radians, pivot at the
    bottom corner). Rounded-spine shading, raised bands with gilt lines, an optional paper/leather label."""
    pts = rect(x, base - h, x + w, base)
    piv = (x + w, base) if lean > 0 else (x, base)
    P = lambda p: rot_poly(p, piv[0], piv[1], lean)
    m = shapes(W, H, [P(pts)], smooth=False)
    art = GP(art, m, col, col2, seed=nx(), rough=0.7, streak=0.7)
    if abs(lean) < 0.02:
        sh, hi = cyl_shade(m, x, x + w)
        art = tint(art, gaussian_filter(sh, 1.2), dark, 0.62, seed=nx())
        art = tint(art, gaussian_filter(hi, 1.5), mix(col, "#fff2d8", 0.45), 0.35, seed=nx())
    else:
        art = tint(art, side_light(m, 5, 0, 3), dark, 0.55, seed=nx())
        art = tint(art, side_light(m, -3, 0, 2), mix(col, "#fff2d8", 0.4), 0.3, seed=nx())
    # wear: scuffed lighter patches at the head/tail
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    ends = m * (np.exp(-((yy - (base - h)) / 6) ** 2) + np.exp(-((yy - base) / 5) ** 2))
    art = tint(art, gaussian_filter(ends, 1), mix(col, "#d8c4a0", 0.5), 0.35, seed=nx())
    bands = bands if bands is not None else rng.choice([2, 3, 4, 0])
    gl = []
    if bands:
        top, bot = base - h + h * 0.09, base - h * 0.1
        ys = [top + (bot - top) * k / (bands + 1) for k in range(1, bands + 1)] if bands > 2 else [base - h + h * 0.12, base - h * 0.12]
        for yb in ys:
            gl.append((P([(x + 1, yb - 3), (x + w - 1, yb - 3)]), 1.3, None))
            gl.append((P([(x + 1, yb + 3), (x + w - 1, yb + 3)]), 1.3, None))
            band = shapes(W, H, [P(rect(x, yb - 2.2, x + w, yb + 2.2))], smooth=False)
            art = tint(art, band, mix(col, "#000000", 0.35), 0.5, seed=nx())
    if gl:
        gm = strokes(W, H, gl) * gaussian_filter(m, 0.5)
        art = FO(art, gm, gold, seed=nx(), emboss=0.3, sparkle=0.1)
    if label:
        ly0 = base - h * rng.uniform(0.62, 0.72)
        lm = shapes(W, H, [P(rect(x + w * 0.16, ly0, x + w * 0.84, ly0 + max(10, h * 0.13)))], smooth=False)
        art = GP(art, lm, label, mix(label, "#7a5a3a", 0.2), seed=nx(), rough=0.5)
        art = tint(art, side_light(lm, 2, 2, 1.5), "#3a2414", 0.4, seed=nx())
        # faint gilt title ticks on the label
        tm = strokes(W, H, [(P([(x + w * 0.3, ly0 + h * 0.045), (x + w * 0.7, ly0 + h * 0.045)]), 1.1, None), (P([(x + w * 0.36, ly0 + h * 0.085), (x + w * 0.64, ly0 + h * 0.085)]), 1.0, None)])
        art = OV(art, tm * lm, lambda mm: col_arr(mm, "#e8c97a" if label not in ("#e9dcc0", "#efe3c6") else "#4a3020", mm * 0.8), pad=3)
    return art, m


LEATHER = [("#6b1f1f", "#7c2a22"), ("#24503a", "#2e5e44"), ("#1f3550", "#28425e"), ("#7a4a1e", "#8a5626"),
           ("#4a2a1a", "#5a3420"), ("#8a6a3a", "#9a7846"), ("#3a2a3e", "#46324a"), ("#a0522d", "#b0623a"),
           ("#c9b48a", "#d6c29a"), ("#5e1a2c", "#6e2436")]


def book_row(art, W, H, x0, x1, base, hmin, hmax, nx, rng, palette=LEATHER, gap=(0, 2), leans=0.12, labels=0.45):
    """Fill a shelf from x0 to x1 with books of varied size; occasionally a leaning book or a gap."""
    x = x0
    while x < x1 - 12:
        w = rng.uniform(13, 30)
        h = rng.uniform(hmin, hmax)
        if x + w > x1:
            w = x1 - x
            if w < 10:
                break
        c, c2 = palette[rng.randrange(len(palette))]
        lean = 0.0
        if rng.random() < leans and x + w + 30 < x1:
            lean = rng.choice([-1, 1]) * rng.uniform(0.12, 0.22)
            if lean < 0:
                lean = abs(lean)
        lab = rng.choice(["#e9dcc0", "#2a1a12", "#6b1f1f", "#efe3c6"]) if rng.random() < labels else None
        art, _ = book(art, W, H, x, base, w, h if not lean else min(h, hmax * 0.92), c, c2, nx, rng, lean=lean, label=lab)
        x += w + rng.uniform(*gap) + (h * math.sin(lean) if lean else 0)
        clear() if rng.random() < 0.2 else None
    return art


def plank(art, W, H, x0, x1, y, t, nx, col="#5a3620", col2="#6a4128", dark="#24140c"):
    """Front edge of a shelf board: wood grain, lit top edge, soft shadow below."""
    m = shapes(W, H, [rect(x0, y, x1, y + t)], smooth=False)
    shadow = shapes(W, H, [rect(x0, y + t, x1, y + t + 14)], smooth=False)
    art = OV(art, shadow, lambda mm: col_arr(mm, "#120a06", gaussian_filter(mm, 5) * 0.55), pad=10)
    art = wood(art, m, col, col2, dark, nx, angle=0.0, ring=7, grain_amt=0.4)
    yy = np.arange(H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    art = tint(art, m * np.exp(-((yy - y - 1.5) / 2) ** 2), "#c08a58", 0.5, seed=nx())
    art = tint(art, m * np.exp(-((yy - y - t + 2) / 3) ** 2), dark, 0.5, seed=nx())
    return art


def velvet(W, H, x0, x1, y0, y1, folds, col, col2, deep, lit, nx, seed=1, gather=None, sway=0.0):
    """Velvet drape mask area filled with vertical folds: deep pile shadows in the troughs and a soft sheen on the
    crests (velvet reflects at grazing angles, so crests carry a pale rim). gather(y)->(xl, xr) narrows the panel
    towards a tie-back. Returns an RGBA painted drape."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if gather is None:
        xl = np.full_like(yy, x0); xr = np.full_like(yy, x1)
    else:
        xl, xr = gather(yy)
    u = (xx - xl) / np.maximum(1, xr - xl)
    inside = ((u >= 0) & (u <= 1) & (yy >= y0) & (yy <= y1)).astype(np.float32)
    hs = max(8, H // 12)
    n1 = np.asarray(Image.fromarray(((fbm(W, hs, seed, 40, 3)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - 0.5
    n2 = fbm(W, H, seed + 9, 300, 2) - 0.5
    ph = u * folds * math.tau + n1 * 3.0 + n2 * 1.2 + sway * (yy - y0) / max(1, y1 - y0) * 3
    f = 0.5 + 0.5 * np.cos(ph + 0.5 * np.sin(ph))  # 1 crest .. 0 trough, asymmetric folds
    ca, cb, cd, cl = (np.array(hex_rgb(c), np.float32) for c in (col, col2, deep, lit))
    t = fbm(W, H, seed + 3, 90, 3)[..., None]
    base = ca * (1 - t) + cb * t
    sh = f[..., None] ** 0.85
    rgb = cd * (1 - sh) + base * sh
    hi = np.clip((f - 0.72) / 0.28, 0, 1) ** 2
    rgb = rgb + (cl - rgb) * (hi[..., None] * 0.3)
    pile = gaussian_filter(np.random.default_rng(seed).random((H, W)).astype(np.float32), (2.5, 0.6))
    pile = (pile - pile.mean()) / (pile.std() + 1e-6)
    rgb = rgb * (1 + pile[..., None] * 0.035)
    m = gaussian_filter(inside, 0.8)
    return np.concatenate([np.clip(rgb, 0, 1), m[..., None]], -1)


def light_leak(W, H, items, seed=1):
    """Film light leak: soft orange/red/yellow blooms bleeding in from the frame edge (RGBA, alpha carries it)."""
    art = blank(W, H)
    for x, y, r, col, a in items:
        m = circles(W, H, [(x, y, r)])
        art = over(art, col_arr(m, col, np.clip(gaussian_filter(m, r * 0.6) * a * 1.6, 0, 1)))
    n = fbm(W, H, seed, 120, 3)
    art[..., 3] *= 0.75 + 0.5 * n
    return np.clip(art, 0, 1)


def film_grain_tile(n, seed=1, tone=(0.5, 0.5, 0.5), amt=0.55):
    """Seamless grain tile (RGBA, mostly transparent): clumped silver grains, light and dark."""
    g = wrap_noise(n, n, seed, 0.6)
    g2 = wrap_noise(n, n, seed + 1, 1.4)
    v = (g - 0.5) * 0.8 + (g2 - 0.5) * 0.6
    a = np.clip(np.abs(v) * 2.2 * amt, 0, 1)
    rgb = np.where(v[..., None] > 0, np.array([1.0, 0.97, 0.9], np.float32), np.array([0.08, 0.05, 0.03], np.float32)) * np.ones((n, n, 3), np.float32)
    return np.concatenate([rgb, a[..., None]], -1)


def blossom(art, W, H, x, y, r, nx, rng, petal="#f6e6e4", petal2="#e9b3b8", heart="#b8323c", stamen="#e7b84a", rot=None, open_=1.0):
    """Five-petal plum blossom (meihua) in watercolour: rounded petals, pink heart, radiating stamens with pollen dots."""
    rot = rng.uniform(0, math.tau) if rot is None else rot
    polys = []
    for k in range(5):
        a = rot + k * math.tau / 5
        cx, cy = x + math.cos(a) * r * 0.52 * open_, y + math.sin(a) * r * 0.52 * open_
        polys.append(deform(ellipse_pts(cx, cy, r * 0.5, r * 0.46, 12, a), rng, 1, 0.03))
    m = shapes(W, H, polys)
    art = G(art, m, petal, petal2, seed=nx(), density=0.9, edge=0.7, bloom=0.2, rough=1.2, feather=0.6, gran=0.15, pad=10)
    hm = circles(W, H, [(x, y, r * 0.32)])
    art = G(art, hm, petal2, heart, seed=nx(), density=0.55, edge=0.4, bloom=0, rough=1.0, feather=1.5, pad=8)
    st = []
    dots = []
    for k in range(11):
        a = rng.uniform(0, math.tau); L = r * rng.uniform(0.35, 0.55)
        st.append(([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], 0.9, None))
        dots.append((x + math.cos(a) * L, y + math.sin(a) * L, max(1.1, r * 0.06)))
    art = OV(art, strokes(W, H, st), lambda mm: col_arr(mm, "#9a3a2a", mm * 0.7), pad=4)
    art = OV(art, circles(W, H, dots), lambda mm: col_arr(mm, stamen, np.clip(mm * 1.2, 0, 1)), pad=4)
    return art


def ink_branch(art, W, H, pts, width, nx, col="#2a1e1a", col2="#4a3a32", dry=0.35):
    """Sumi-style branch: one loaded brush stroke with dry-brush breaks and a darker knotted edge."""
    m = strokes(W, H, [(pts, width, (0.02, 0.5))])
    art = G(art, m, col2, col, seed=nx(), density=0.95, edge=0.9, bloom=0.1, rough=2.2, feather=0.6, gran=0.45, holes=dry, pad=10)
    return art


def mandarin(art, W, H, x, y, r, nx, rng, leaf=True, ldir=(-0.5, -0.6)):
    """Gouache mandarin orange: dimpled peel, warm shadow, specular dot, small stem cap with one or two leaves."""
    m = shapes(W, H, [deform(ellipse_pts(x, y, r * 1.04, r * 0.92, 16, rng.uniform(-.2, .2)), rng, 1, 0.012)])
    art = GP(art, m, "#f08a1c", "#f59a2a", seed=nx(), rough=0.6, streak=0.3)
    art = tint(art, side_light(m, -ldir[0] * r * 0.35, -ldir[1] * r * 0.35, r * 0.3), "#b0400e", 0.75, seed=nx())
    art = tint(art, side_light(m, ldir[0] * r * 0.25, ldir[1] * r * 0.25, r * 0.2), "#ffc46a", 0.55, seed=nx())
    b = bbox(m, 2, 0.01)
    if b:
        y0, y1, x0, x1 = b
        d = np.zeros_like(m)
        d[y0:y1, x0:x1] = fbm(x1 - x0, y1 - y0, nx(), 3, 2)
        art = tint(art, np.clip((d - 0.6) * 3, 0, 1) * m, "#c2560f", 0.35, seed=nx())
    sp = circles(W, H, [(x + ldir[0] * r * 0.45, y + ldir[1] * r * 0.45, r * 0.11)])
    art = OV(art, sp, lambda mm: col_arr(mm, "#fff1d0", np.clip(gaussian_filter(mm, r * 0.05) * 1.3, 0, 1) * 0.85), pad=8)
    cap = circles(W, H, [(x + r * 0.05, y - r * 0.84, r * 0.1)])
    art = GP(art, cap, "#5a6a2a", seed=nx(), rough=0.4)
    if leaf:
        for a, L in ((-2.1 + rng.uniform(-.2, .2), r * 1.15), (-0.7 + rng.uniform(-.2, .2), r * 0.85)):
            lm = shapes(W, H, [petal_pts(x + r * 0.05, y - r * 0.86, L, L * 0.34, a, 16, cup=0.1)])
            art = GP(art, lm, "#2f6a3a", "#3e7c42", seed=nx(), rough=0.6, streak=0.5)
            art = tint(art, side_light(lm, 0, 3, 2.5), "#163a22", 0.5, seed=nx())
            rib = strokes(W, H, [([(x + r * 0.05 + math.cos(a) * L * t, y - r * 0.86 + math.sin(a) * L * t) for t in np.linspace(0.05, 0.8, 8)], 1.2, (0.1, 0.5))])
            art = OV(art, rib * lm, lambda mm: col_arr(mm, "#9fc48a", mm * 0.5), pad=3)
    return art


def lantern(art, W, H, cx, top, rw, rh, nx, rng, red="#c4161c", red2="#d6262a", deep="#6e0a10", gold="#d8a640", tassel=True, glow_amt=0.6):
    """Round Chinese paper lantern: ribbed red body glowing from inside, gold caps, hanging cord and tassel."""
    cy = top + rh
    body = shapes(W, H, [deform(ellipse_pts(cx, cy, rw, rh, 28), rng, 1, 0.006)])
    if glow_amt:
        art = OV(art, body, lambda mm: col_arr(mm, "#ff9a3a", np.clip(gaussian_filter(mm, rw * 0.5), 0, 1) * 0.45 * glow_amt), pad=int(rw * 1.2))
    art = GP(art, body, red, red2, seed=nx(), rough=0.6, streak=0.4)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - cx) / rw; v = (yy - cy) / rh
    inner = np.clip(1 - (u ** 2 + v ** 2), 0, 1)
    art = tint(art, body * inner ** 0.8, "#ff8a3a", 0.55 * (glow_amt + 0.3), seed=nx())
    art = tint(art, body * np.clip((u ** 2 + v ** 2) - 0.45, 0, 1) * 1.6, deep, 0.7, seed=nx())
    ribs = []
    for k in range(-4, 5):
        s = k / 4.6
        pts = [(cx + s * rw * math.sqrt(max(0, 1 - t * t)), cy + t * rh * 0.98) for t in np.linspace(-0.98, 0.98, 26)]
        ribs.append((pts, 1.4, None))
    rm = strokes(W, H, ribs) * body
    art = tint(art, gaussian_filter(rm, 0.6), deep, 0.45, seed=nx())
    capw = rw * 0.42
    for y_, hh in ((top + rh * 0.04, rh * 0.16), (cy + rh * 0.86, rh * 0.16)):
        cm = shapes(W, H, [rect(cx - capw, y_ - hh / 2, cx + capw, y_ + hh / 2)], smooth=False)
        art = FO(art, cm, gold, seed=nx(), emboss=0.5, sparkle=0.15)
        art = tint(art, side_light(cm, 0, 2, 1.5), "#5a3a10", 0.45, seed=nx())
    cord = strokes(W, H, [([(cx, 0), (cx, top - rh * 0.04)], 2.2, None)])
    art = OV(art, cord, lambda mm: col_arr(mm, "#7a1010", mm * 0.95), pad=3)
    if tassel:
        ty = cy + rh * 0.94
        knot = circles(W, H, [(cx, ty + rh * 0.1, rw * 0.07)])
        art = FO(art, knot, gold, seed=nx(), emboss=0.4)
        threads = [([(cx + rng.uniform(-1.5, 1.5), ty + rh * 0.16), (cx + rng.uniform(-rw * 0.12, rw * 0.12), ty + rh * 0.62 + rng.uniform(-4, 4))], 1.3, (0.0, 0.4)) for _ in range(26)]
        tm = strokes(W, H, threads)
        art = GP(art, tm, red, "#a80f16", seed=nx(), rough=0.3)
        art = tint(art, tm, deep, 0.25, seed=nx())
    return art


def gilt(art, mask, nx, base="#c9a04e", dark="#5a3a12", light="#ffe7a8", ldir=(-3, -4)):
    """Gilded moulding: foil body + shading from a soft light direction + bright edge catch."""
    art = FO(art, mask, base, seed=nx(), emboss=0.8, sparkle=0.03)
    art = tint(art, side_light(mask, -ldir[0], -ldir[1], 2.5), dark, 0.6, seed=nx())
    art = tint(art, side_light(mask, ldir[0] * 0.6, ldir[1] * 0.6, 1.5), light, 0.5, seed=nx())
    return art


def crystal(art, W, H, x, y, r, nx, rng, col="#f4f1ea"):
    """Faceted crystal drop: pale glassy body, dark facet line, bright catchlight, faint spectral tint."""
    pts = [(x, y - r * 1.2), (x + r * 0.62, y), (x, y + r * 1.05), (x - r * 0.62, y)]
    m = shapes(W, H, [pts], smooth=False)
    art = OV(art, m, lambda mm: col_arr(mm, col, np.clip(gaussian_filter(mm, 0.6), 0, 1) * 0.55), pad=4)
    art = tint(art, side_light(m, 2, 1, 1.2), "#8a7a6a", 0.6, seed=nx())
    art = OV(art, strokes(W, H, [([(x, y - r * 1.1), (x, y + r * 0.95)], 0.8, None)]) * m, lambda mm: col_arr(mm, "#ffffff", mm * 0.6), pad=3)
    tint_c = rng.choice(["#ffd6a0", "#c8e0ff", "#ffe8f0", "#fff6c0"])
    art = tint(art, m * 0.6, tint_c, 0.3, seed=nx())
    art = OV(art, circles(W, H, [(x - r * 0.18, y - r * 0.3, max(0.9, r * 0.16))]), lambda mm: col_arr(mm, "#ffffff", np.clip(mm * 1.2, 0, 1)), pad=3)
    return art
