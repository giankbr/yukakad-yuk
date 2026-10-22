"""Agent B5 helpers (delft-biru, origami-bangau, ultah-antariksa, aqiqah-domba): _a6_lib (bbox-local painting, gouache
shading, crayon) + tin-glaze tiles with crackle, cobalt brushwork, faceted folded paper, dry-brush wool.
Previews -> /tmp/pen/nb-B5/art."""
import sys, os
sys.path.insert(0, "/tmp/pen/art/themes")
from _a6_lib import *  # noqa
import _p1_lib, _j1_lib
from scipy.spatial import cKDTree

PREV = "/tmp/pen/nb-B5/art"
os.makedirs(PREV, exist_ok=True)
_p1_lib.PREV = PREV
_j1_lib.PREV = PREV


# ---------------- tin glaze + cobalt (Delft) ----------------
def crackle(w, h, seed, cells=60, width=0.9):
    """Fine craquelure network (0..1 line field) from Voronoi cell borders, wobbled."""
    rng = np.random.default_rng(seed)
    pts = rng.random((cells, 2)) * [w, h]
    # tile the points so cracks wrap nicely
    allp = np.concatenate([pts + [dx * w, dy * h] for dx in (-1, 0, 1) for dy in (-1, 0, 1)])
    tree = cKDTree(allp)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1 = (fbm(w, h, seed + 1, 30, 3) - .5) * 10
    n2 = (fbm(w, h, seed + 2, 30, 3) - .5) * 10
    q = np.stack([(xx + n1).ravel(), (yy + n2).ravel()], -1)
    d, _ = tree.query(q, k=2)
    edge = (d[:, 1] - d[:, 0]).reshape(h, w)
    line = np.clip(1 - edge / width, 0, 1)
    brk = fbm(w, h, seed + 3, 14, 2)
    return (line * np.clip((brk - .25) * 2.5, 0, 1)).astype(np.float32)


def glaze_tile(S, seed, tone="#f7f6f0", cool="#e9edf2", crack=0.16, bevel=True, radius=10):
    """Opaque square tin-glazed tile: milky white with cool pooling, crackle, pinholes, soft bevel at the edge."""
    m = shapes(S, S, [[(radius, 0), (S - radius, 0), (S, radius), (S, S - radius), (S - radius, S), (radius, S), (0, S - radius), (0, radius)]])
    m = np.clip(gaussian_filter(displace(m, seed, 2.2, 30), 0.8) * 1.4 - .2, 0, 1)
    a = np.array(hex_rgb(tone), np.float32); b = np.array(hex_rgb(cool), np.float32)
    t = fbm(S, S, seed + 5, 120, 3)[..., None]
    rgb = a * (1 - t * .7) + b * t * .7
    c = crackle(S, S, seed + 7, cells=int(S * S / 5200) + 12)
    rgb = rgb * (1 - c[..., None] * crack * np.array([1.0, .95, .85], np.float32))
    pin = (np.random.default_rng(seed).random((S, S)) > .9993).astype(np.float32)
    pin = gaussian_filter(pin, .7) * 3
    rgb = rgb * (1 - np.clip(pin, 0, .3)[..., None] * .5)
    if bevel:
        inner = gaussian_filter(m, S * 0.02)
        e = np.clip((1 - inner) * m * 2.2, 0, 1)
        rgb = rgb * (1 - e[..., None] * .16)
        hl = np.clip(np.roll(np.roll(m, 3, 0), 3, 1) - gaussian_filter(m, 3), 0, 1)
        rgb = np.clip(rgb + hl[..., None] * .1, 0, 1)
    g = gaussian_filter(np.random.default_rng(seed + 9).random((S, S)).astype(np.float32), .6)
    rgb = np.clip(rgb * (1 + (g - .5)[..., None] * .025), 0, 1)
    return np.concatenate([rgb, m[..., None]], -1), m


COB = ("#13368a", "#1f48a6")          # trek (outline) cobalt
COB_W = ("#3f66b8", "#5a7cc6")        # wash
COB_D = ("#0f2a6e", "#173584")


def cobalt_wash(dst, mask, seed, density=0.6, col=COB_W, edge=0.7, rough=2.2, bloom=0.25):
    """Diluted cobalt wash with strong pooling at the rim (like blue on raw tin glaze)."""
    return G(dst, mask, col[0], col[1], seed=seed, density=density, edge=edge, bloom=bloom, gran=0.35, feather=0.9,
             rough=rough, mottle=0.55)


def trek(dst, W, H, items, seed, col=COB_D, density=0.92):
    """Delft 'trek' brush outline: tapered strokes in dark cobalt, slightly pooled."""
    m = strokes(W, H, items)
    return G(dst, m, col[0], col[1], seed=seed, density=density, edge=0.35, bloom=0, gran=0.2, feather=0.5, rough=1.0,
             mottle=0.3)


def dab(dst, W, H, pts, seed, col=COB, density=0.85):
    """Filled cobalt shapes (petals, dots) — solid brush loads."""
    return G(dst, shapes(W, H, pts), col[0], col[1], seed=seed, density=density, edge=0.5, bloom=0.1, gran=0.25,
             feather=0.6, rough=1.2, mottle=0.4)


# ---------------- folded paper (origami) ----------------
def paper_fibre(h, w, seed, amt=1.0):
    """Washi fibre field (-1..1-ish): long thin fibres + fine tooth."""
    rng = np.random.default_rng(seed)
    cv = Canvas(w, h, seed)
    p = skia.Paint(AntiAlias=True, Color4f=color("#ffffff", .5), StrokeWidth=.7, Style=skia.Paint.kStroke_Style)
    r = random.Random(seed)
    for _ in range(int(w * h / 900)):
        x, y = r.uniform(0, w), r.uniform(0, h)
        a = r.uniform(0, math.tau); L = r.uniform(6, 26)
        pts = [(x, y)]
        for k in range(4):
            a += r.gauss(0, .5)
            x += math.cos(a) * L / 4; y += math.sin(a) * L / 4
            pts.append((x, y))
        path = skia.Path(); path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        cv.c.drawPath(path, p)
    fib = cv.array()[..., 3]
    tooth = gaussian_filter(rng.random((h, w)).astype(np.float32), .7)
    tooth = (tooth - tooth.mean()) / (tooth.std() + 1e-6)
    return (fib * 1.0 + tooth * .05) * amt


def facet(dst, mask, col, light, seed, fibre=None, shade_grad=None):
    """One flat paper plane: colour * light, paper fibre, tiny tonal grad, crisp edge."""
    b = bbox(mask, 3, 0.01)
    if b is None:
        return dst
    y0, y1, x0, x1 = b
    m = mask[y0:y1, x0:x1]
    h, w = m.shape
    c = np.array(hex_rgb(col), np.float32) * light
    rgb = np.ones((h, w, 3), np.float32) * c
    lo = fbm(w, h, seed, 60, 2) - .5
    rgb = rgb * (1 + lo[..., None] * .05)
    if fibre is not None:
        f = fibre[y0:y1, x0:x1]
        rgb = rgb * (1 + f[..., None] * .06) + f[..., None] * .03
    if shade_grad is not None:
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        rgb = rgb * shade_grad(xx, yy)[..., None]
    out = dst.copy()
    out[y0:y1, x0:x1] = over(dst[y0:y1, x0:x1], np.concatenate([np.clip(rgb, 0, 1), np.clip(m, 0, 1)[..., None]], -1))
    return out


def poly(W, H, pts):
    return shapes(W, H, [pts], smooth=False)


def fold_line(dst, W, H, a, b, col="#ffffff", amt=.35, wd=1.2):
    m = strokes(W, H, [([a, b], wd, None)])
    return OV(dst, m, lambda mm: col_arr(mm, col, mm * amt), pad=4)


def drop_shadow(dst, mask, dx=6, dy=10, blur=7, amt=.22, col="#4a3b4f"):
    """Soft cast shadow placed UNDER what is already painted."""
    sh = np.roll(np.roll(gaussian_filter(mask, blur), dy, 0), dx, 1)
    return over(col_arr(sh, col, np.clip(sh * amt, 0, 1)), dst)


# ---------------- wool (aqiqah) ----------------
def wool(dst, W, H, mask, seed, base="#fbf6ec", shade="#e6dacb", deep="#c9b8a3", hi="#ffffff", curl=11, light=(-12, -14)):
    """Dry-brush fleece: opaque underpaint, soft wash, then many little curl strokes broken by the paper tooth."""
    rng = random.Random(seed)
    nx = Seq(seed)
    dst = GP(dst, mask, base, "#f7efe2", seed=nx(), rough=2.5, streak=.3)
    dst = G(dst, mask, "#f3ebde", "#efe4d2", seed=nx(), density=0.4, edge=0.3, bloom=0.2, gran=0.15, rough=4, feather=1.4, mottle=0.3)
    dst = tint(dst, side_light(mask, -light[0], -light[1], 12) * 1.4, shade, 0.65, seed=nx())
    ys, xs = np.where(mask > .5)
    if len(xs) == 0:
        return dst
    shadow_f = gaussian_filter(side_light(mask, -light[0], -light[1], 14), 4)
    items_d, items_l = [], []
    for _ in range(int(len(xs) / (curl * curl) * 2.2)):
        i = rng.randrange(len(xs))
        x, y = float(xs[i]), float(ys[i])
        r = curl * rng.uniform(.6, 1.1)
        a0 = rng.uniform(0, math.tau)
        arc = [(x + math.cos(a0 + t * 4.2) * r * (1 - t * .45), y + math.sin(a0 + t * 4.2) * r * (1 - t * .45)) for t in np.linspace(0, 1, 9)]
        (items_d if shadow_f[int(y), int(x)] > .12 or rng.random() < .35 else items_l).append((arc, rng.uniform(1.6, 2.6), (0.2, 0.4)))
    md = strokes(W, H, items_d) * gaussian_filter(mask, 1)
    ml = strokes(W, H, items_l) * gaussian_filter(mask, 1)
    dst = crayon(dst, md, deep, seed=nx(), amt=.55, tooth=.55)
    dst = crayon(dst, ml, shade, seed=nx(), amt=.5, tooth=.5)
    # highlights on the lit side
    lit = side_light(mask, light[0], light[1], 10)
    dst = tint(dst, gaussian_filter(lit, 3) * 1.2, hi, 0.7, seed=nx())
    return dst


def scallop_mask(W, H, mask, r, seed, count=None):
    """Fluffy outline: union of circles along/inside the mask edge (cloud/fleece silhouette)."""
    rng = random.Random(seed)
    edge = inner_edge(mask, 2)
    ys, xs = np.where(edge > .3)
    items = []
    n = count or max(8, int(len(xs) / (r * 1.2)))
    for _ in range(n):
        i = rng.randrange(len(xs))
        items.append((float(xs[i]), float(ys[i]), r * rng.uniform(.7, 1.15)))
    return np.clip(np.maximum(mask, circles(W, H, items)), 0, 1)
