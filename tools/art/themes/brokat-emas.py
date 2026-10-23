"""Brokat Emas — woven gold brocade: a seamless damask repeat (pomegranate bloom in an ogee, acanthus scrolls, corner
rosettes) in raised gold weft floats on an oxblood twill ground; the same cloth hung as two drapes with folds and
gold tassels; gold galon trim; a damask medallion. No figures, no calligraphy.
Run: python3 -I brokat-emas.py [part ...]  parts: tile drape tassel galon medallion divider
Assets -> public/themes/art/brokat-emas/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l2_lib import *

OUT = outdir("brokat-emas")
PARTS = sys.argv[1:] or ["tile", "drape", "tassel", "galon", "medallion", "divider"]
GROUND, GROUND_D, GROUND_L = "#4a0d1c", "#2c0610", "#651a2a"
GOLD, GOLD_L, GOLD_D = "#c99a3e", "#f3d78e", "#7a5520"
N = 480


def ring_in(n, polys_inner):
    inner = shapes(n, n, polys_inner)
    return np.clip((gaussian_filter(inner, 1.1, mode="wrap") > 0.12).astype(np.float32) - inner, 0, 1)


def damask_mask(n=N, scale=1.0):
    """Seamless damask motif mask (n x n): main bloom at the centre, rosettes at the corners (wrap).
    Returns (gold, detail, tonal) masks; tonal = tone-on-tone satin ground pattern."""
    s = n / 480 * scale
    c = n / 2
    items, polys, cuts_inner = [], [], []
    # double ogee frame with leaflets
    def ogee(off):
        pts = []
        for i in range(41):
            t = i / 40
            y = 58 + t * 362
            w = (140 + off) * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t)
            pts.append((w, y))
        return pts
    for sg in (-1, 1):
        items.append(([(c + sg * w * s, y * s) for w, y in ogee(0)], 7 * s, (0.05, 0.05)))
        items.append(([(c + sg * w * s, y * s) for w, y in ogee(-16)][3:-3], 3.2 * s, (0.05, 0.05)))
        for k, (w, y) in enumerate(ogee(0)[5:38:4]):
            x0, y0 = c + sg * w * s, y * s
            polys.append(petal_pts(x0, y0, 34 * s, 11 * s, (0 if sg > 0 else math.pi) - sg * 0.0 - 0.55 * (1 if sg > 0 else -1), n=12))
    # big acanthus scrolls outside the ogee rising from the base
    for sg in (-1, 1):
        sp = curve([(c + sg * 30 * s, 430 * s), (c + sg * 150 * s, 420 * s), (c + sg * 200 * s, 330 * s), (c + sg * 186 * s, 240 * s), (c + sg * 214 * s, 170 * s)], 60)
        items.append((sp, 6 * s, (0.05, 0.4)))
        for k, (x, y, a) in enumerate(along(sp, 30)):
            sz = 0.6 + 0.5 * math.sin(math.pi * min(1, k / 8))
            d = 1 if k % 2 else -1
            pp = petal_pts(x, y, 40 * s * sz, 14 * s * sz, a + d * 0.9, n=14, cup=d * 0.4)
            polys.append(pp)
            cuts_inner.append(petal_pts(x + math.cos(a + d * 0.9) * 6 * s, y + math.sin(a + d * 0.9) * 6 * s, 26 * s * sz, 6 * s * sz, a + d * 0.9, n=12))
        tip = sp[-1]
        items.append((spiral_pts(tip[0] - sg * 16 * s, tip[1] - 4 * s, 16 * s, 2 * s, 0 if sg > 0 else math.pi, 1.2, 40, -sg), 5 * s, (0.0, 0.5)))
    # stem + calyx
    items.append(([(c, 412 * s), (c, 300 * s)], 9 * s, None))
    for sg in (-1, 1):
        polys.append(petal_pts(c, 316 * s, 80 * s, 22 * s, math.pi / 2 + sg * 1.05, n=14, cup=sg * 0.5))
        cuts_inner.append(petal_pts(c + sg * 10 * s, 322 * s, 56 * s, 8 * s, math.pi / 2 + sg * 1.05, n=12, cup=sg * 0.5))
        items.append((spiral_pts(c + sg * 80 * s, 378 * s, 22 * s, 3 * s, -math.pi / 2, 1.1, 34, sg), 7 * s, (0.0, 0.5)))
    # bloom: outer 9 petals + inner 5
    for k, a in enumerate(np.linspace(-math.pi + 0.3, -0.3, 9)):
        L = (104 if k % 2 == 0 else 84) * s
        x0, y0 = c + math.cos(a) * 16 * s, 254 * s + math.sin(a) * 16 * s
        polys.append(petal_pts(x0, y0, L, 24 * s, a, n=16))
        cuts_inner.append(petal_pts(x0 + math.cos(a) * 18 * s, y0 + math.sin(a) * 18 * s, L * 0.68, 11 * s, a, n=14))
    gold = np.maximum(strokes(n, n, items), shapes(n, n, polys))
    podm = shapes(n, n, [ellipse_pts(c, 254 * s, 38 * s, 46 * s, 24)])
    gold = np.maximum(gold, podm)
    cut = ring_in(n, cuts_inner)
    pod_gap = np.clip(podm - shapes(n, n, [ellipse_pts(c, 254 * s, 31 * s, 39 * s, 24)]), 0, 1)
    pod_gap = np.clip((gaussian_filter(shapes(n, n, [ellipse_pts(c, 254 * s, 31 * s, 39 * s, 24)]), 1.0) > 0.1).astype(np.float32) - shapes(n, n, [ellipse_pts(c, 254 * s, 31 * s, 39 * s, 24)]), 0, 1)
    seeds = [(c + dx * s, 254 * s + dy * s, 4.6 * s) for dx in (-15, 0, 15) for dy in (-24, -8, 8, 24)] + [(c + dx * s, 254 * s + dy * s, 3.4 * s) for dx in (-8, 8) for dy in (-16, 0, 16)]
    cut = np.maximum.reduce([cut, circles(n, n, seeds), pod_gap])
    gold = np.clip(gold - cut * 0.98, 0, 1)
    # corner rosettes (wrap) with cut petals, mid-edge sprigs
    rp, rcut = [], []
    corners = [(0, 0), (n, 0), (0, n), (n, n)]
    for (x0, y0) in corners:
        for k in range(8):
            a = k * math.pi / 4 + math.pi / 8
            L = (62 if k % 2 == 0 else 44) * s
            rp.append(petal_pts(x0, y0, L, (18 if k % 2 == 0 else 12) * s, a, n=14))
            rcut.append(petal_pts(x0 + math.cos(a) * 16 * s, y0 + math.sin(a) * 16 * s, L * 0.55, 5 * s, a, n=12))
    rose = np.clip(shapes(n, n, rp) - ring_in(n, rcut), 0, 1)
    rc = circles(n, n, [(x0, y0, 15 * s) for x0, y0 in corners])
    rose = np.clip(np.maximum(rose, rc) - circles(n, n, [(x0, y0, 7 * s) for x0, y0 in corners]), 0, 1)
    sprig_items, sprig_p = [], []
    for (x0, y0) in [(0, c), (n, c)]:
        sprig_items.append((curve([(x0, y0 + 70 * s), (x0 + 6 * s, y0), (x0, y0 - 70 * s)], 16), 5 * s, (0.1, 0.1)))
        for k in range(-2, 3):
            for sg in (-1, 1):
                sprig_p.append(petal_pts(x0, y0 + k * 24 * s, 34 * s, 9 * s, (0 if sg > 0 else math.pi) - sg * 0.6, n=10))
    sprig = np.maximum(strokes(n, n, sprig_items), shapes(n, n, sprig_p))
    gold = np.maximum.reduce([gold, rose, sprig])
    detail = np.maximum(rc, podm * 0)
    # tone-on-tone ground: small trefoil sprigs on a diagonal grid
    tp, ti = [], []
    for gy in range(0, n + 1, 60):
        for gx in range(0, n + 1, 60):
            ox = 30 if (gy // 60) % 2 else 0
            x0, y0 = (gx + ox) % (n + 1), gy
            for k in range(3):
                a = -math.pi / 2 + (k - 1) * 0.9
                tp.append(petal_pts(x0 * s, y0 * s, 16 * s, 5 * s, a, n=10))
            ti.append(([(x0 * s, y0 * s), (x0 * s, y0 * s + 10 * s)], 2 * s, None))
    tonal = np.maximum(shapes(n, n, tp), strokes(n, n, ti))
    tonal = np.clip(tonal - gaussian_filter(gold, 6, mode="wrap") * 3, 0, 1)
    return gold, detail, tonal


def weave(mask, detail, seed, n_h, n_w, sheen=None, wrap=True, tonal=None):
    """Render brocade: twill ground + raised gold weft floats with emboss and metallic sheen."""
    h, w = mask.shape
    rng = np.random.default_rng(seed)
    mode = "wrap" if wrap else "reflect"
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # ground: oxblood twill (diagonal ribs) + slub
    tw = 0.5 + 0.5 * np.cos((xx + yy) / 3.0 * math.tau)
    slub = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.6, 2.5), mode=mode)
    slub = (slub - slub.mean()) / (slub.std() + 1e-6)
    tone = gaussian_filter(rng.random((h, w)).astype(np.float32), 30, mode=mode)
    tone = (tone - tone.min()) / (tone.max() - tone.min() + 1e-6)
    g = col3(GROUND)[None, None] * (1 - tone[..., None] * 0.5) + col3(GROUND_L)[None, None] * tone[..., None] * 0.5
    g = g * (0.9 + 0.1 * tw[..., None]) * (1 + slub[..., None] * 0.03)
    if tonal is not None:
        tm = np.clip(gaussian_filter(tonal, 0.6, mode=mode), 0, 1)
        sat = 0.5 + 0.5 * np.cos(xx / 2.0 * math.tau)
        g = g * (1 + tm[..., None] * (0.22 + 0.1 * sat[..., None]))
    # gold: weft floats (horizontal ridges) + thread breaks
    m = np.clip(gaussian_filter(mask, 0.7, mode=mode), 0, 1)
    ridge = 0.5 + 0.5 * np.cos(yy / 2.4 * math.tau)
    brk = gaussian_filter(rng.random((h, w)).astype(np.float32), (0.5, 6), mode=mode)
    brk = (brk - brk.min()) / (brk.max() - brk.min() + 1e-6)
    blur = gaussian_filter(m, 2.2, mode=mode)
    gy, gx = np.gradient(blur)
    light = np.clip(0.5 - (gx * 0.8 + gy) * 7, 0, 1)
    if sheen is None:
        sheen = 0.5 + 0.5 * np.sin((xx * 0.7 + yy * 0.45) / (w * 0.11))
    lum = 0.5 + 0.25 * ridge + 0.45 * (light - 0.5) + 0.4 * (sheen - 0.5) + (brk - 0.5) * 0.14
    gold = col3(GOLD_D)[None, None] * (1 - lum[..., None]) + col3(GOLD_L)[None, None] * lum[..., None]
    gold = np.clip(gold * (0.9 + 0.25 * lum[..., None]), 0, 1)
    d = np.clip(gaussian_filter(detail, 0.6, mode=mode), 0, 1) * m
    gold = gold * (1 - d[..., None] * 0.5) + col3("#f7ead0")[None, None] * d[..., None] * 0.5 * (0.6 + 0.4 * ridge[..., None])
    # cast shadow of the raised float on the ground (down-right)
    sh = np.clip(np.roll(np.roll(blur, 2, 0), 2, 1) - m, 0, 1)
    g = g * (1 - sh[..., None] * 0.55)
    rgb = g * (1 - m[..., None]) + gold * m[..., None]
    return rgb


if "tile" in PARTS:
    mask, detail, tonal = damask_mask()
    rgb = weave(mask, detail, 3101, N, N, tonal=tonal)
    save_full(rgba(rgb, np.ones((N, N), np.float32)), f"{OUT}/tile.webp", size=(360, 360), quality=80)
    big = np.tile(rgb, (2, 2, 1))
    preview(rgba(big, np.ones(big.shape[:2], np.float32)), "be-tile")
    clear()

if "drape" in PARTS:
    # left drape: cloth hanging from the top, gathered to a tie-back, folds converging; mirrored in CSS
    W, H = 420, 900
    TIE = 520
    ys = np.arange(H, dtype=np.float32)
    def edge(y):
        t1 = np.clip(y / TIE, 0, 1)
        top = 360 - 230 * (t1 ** 1.3)
        after = 130 + 120 * np.clip((y - TIE) / (H - TIE), 0, 1) ** 0.7
        return np.where(y < TIE, top, after)
    bx = edge(ys)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = xx / bx[:, None]
    shape = (u <= 1).astype(np.float32)
    # soft wavy inner edge
    bxw = bx[:, None] * (1 + 0.04 * np.cos(u * 5.5 * math.tau))
    shape = np.clip((bxw - xx) / 2.0 + 0.5, 0, 1)
    folds = 5.5
    ph = u * folds * math.tau + np.sin(ys / 140)[:, None] * 0.6
    fold = np.cos(ph)
    # texture coordinates: across-drape position compresses toward the tie
    tx = (u * 520 + np.sin(ph) * 10) % N
    ty = (yy + fold * 6) % N
    mask, detail, tonal = damask_mask()
    flat = weave(mask, detail, 3101, N, N, tonal=tonal)
    tex = np.stack([map_coordinates(flat[..., ch], [ty, tx], order=1, mode="wrap") for ch in range(3)], -1)
    shade = 0.5 + 0.68 * (0.5 + 0.5 * fold) ** 1.4 + 0.12 * np.clip(np.sin(ph - 0.9), 0, 1) ** 6
    shade = shade * (1 - 0.25 * np.clip((u - 0.85) / 0.15, 0, 1))  # inner edge turns away
    rgb = tex * shade[..., None]
    # gather pinch at the tie: darken a band
    pinch = np.exp(-((ys - TIE) / 26) ** 2)[:, None]
    rgb *= (1 - 0.35 * pinch)[..., None]
    # top valance shadow
    rgb *= (1 - 0.3 * np.exp(-ys / 50))[:, None, None]
    art = rgba(rgb, shape)
    # gold cord around the gather
    cord = strokes(W, H, [(curve([(-6, TIE - 10), (70, TIE + 6), (140, TIE - 2)], 24), 12, None)])
    art = FO(art, cord, GOLD, seed=3201, emboss=0.8, sparkle=0.2)
    twist = strokes(W, H, [([(x, TIE - 4 + 0.08 * x - 9), (x + 6, TIE + 6 + 0.08 * x - 9)], 2, None) for x in range(0, 136, 9)])
    art = G(art, twist * cord, GOLD_D, seed=3202, density=0.6, edge=0, bloom=0, rough=0.4)
    preview(art, "be-drape", bg=GROUND_D)
    save(art, f"{OUT}/drape.webp", max_w=230, quality=80)
    clear()

if "tassel" in PARTS:
    W, H = 160, 300
    nx = Seq(3300)
    art = blank(W, H)
    cordm = strokes(W, H, [(curve([(80, 0), (82, 40), (80, 70)], 12), 6, None)])
    knob = shapes(W, H, [ellipse_pts(80, 86, 22, 20, 20)]) + shapes(W, H, [[(64, 100), (96, 100), (90, 120), (70, 120)]])
    neck = shapes(W, H, [[(66, 118), (94, 118), (98, 130), (62, 130)]], smooth=False)
    threads = []
    rng = random.Random(4)
    for k in range(34):
        x0 = 64 + k * 1.0
        x1 = 40 + k * 2.4 + rng.uniform(-2, 2)
        threads.append((curve([(x0, 128), ((x0 + x1) / 2, 200), (x1, 292 - abs(k - 17) * 1.2)], 18), 2.6, (0.0, 0.2)))
    th = strokes(W, H, threads)
    art = FO(art, th, "#b98b36", seed=nx(), emboss=0.4, sparkle=0.15)
    art = G(art, th * gaussian_filter(rng.random() + np.zeros((H, W), np.float32), 1), GOLD_D, seed=nx(), density=0.2, edge=0, bloom=0, rough=0.4)
    art = FO(art, np.clip(np.maximum.reduce([cordm, knob, neck]), 0, 1), GOLD, seed=nx(), emboss=0.85, sparkle=0.2)
    bands = strokes(W, H, [([(60, 104), (100, 104)], 2, None), ([(62, 124), (98, 124)], 2.4, None)])
    art = G(art, bands * np.clip(knob + neck, 0, 1), GOLD_D, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.3)
    art = GP(art, circles(W, H, [(80, 86, 7)]), "#6e1426", seed=nx(), rough=0.3, pad=4)
    preview(art, "be-tassel", bg=GROUND)
    save(art, f"{OUT}/tassel.webp", max_w=80, quality=84)
    clear()

if "galon" in PARTS:
    # gold galon (passementerie trim) band, repeat-x period 32
    W, H = 512, 44
    nx = Seq(3400)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    band = shapes(W, H, [[(0, 8), (W, 8), (W, 36), (0, 36)]], smooth=False)
    scal = []
    for x in range(0, W + 1, 32):
        scal.append(ellipse_pts(x, 22, 13, 10, 16))
    sc = shapes(W, H, scal)
    holes = circles(W, H, [(x, 22, 4.2) for x in range(0, W + 1, 32)])
    beads = circles(W, H, [(x + 16, 22, 3.2) for x in range(0, W, 32)])
    edges = shapes(W, H, [[(0, 6), (W, 6), (W, 10), (0, 10)], [(0, 34), (W, 34), (W, 38), (0, 38)]], smooth=False)
    m = np.clip(np.maximum.reduce([sc, edges, beads]) - holes, 0, 1)
    art = GP(blank(W, H), band, GROUND_D, seed=nx(), rough=0.3, pad=2)
    rope = 0.5 + 0.5 * np.cos((xx - yy * 0.8) / 3.2 * math.tau)
    art = FO(art, m, GOLD, seed=nx(), emboss=0.9, sparkle=0.15)
    art[..., :3] *= (0.86 + 0.18 * rope[..., None] * m[..., None] + (1 - m[..., None]) * 0.14)
    art[..., 3] = np.maximum(band, m)
    save_full(art, f"{OUT}/galon.webp", size=(256, 22), quality=86)
    preview(art, "be-galon", bg=GROUND)
    clear()

if "medallion" in PARTS:
    # single damask bloom cut from the cloth (no ground), gold weave on transparent
    n = 480
    mask, detail, _ = damask_mask(n)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    og = []
    for i in range(41):
        t = i / 40
        og.append((n / 2 + 178 * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t), 40 + t * 390))
    og = og + [(n - x, y) for x, y in reversed(og)]
    keep = shapes(n, n, [og], smooth=False) * (yy < 414)
    mm = mask * keep
    rgb = weave(mm, detail * keep, 3501, n, n, wrap=False)
    art = rgba(rgb, np.clip(gaussian_filter(mm, 0.7), 0, 1))
    preview(art, "be-medallion", bg=GROUND)
    save(art, f"{OUT}/medallion.webp", max_w=170, quality=84)
    clear()

if "divider" in PARTS:
    W, H = 460, 80
    items, polys = [], []
    for sg in (-1, 1):
        X = lambda u: 230 + sg * u
        vine = curve([(X(30), 40), (X(80), 30), (X(140), 48), (X(200), 34), (X(222), 40)], 60)
        items.append((vine, 4, (0.0, 0.4)))
        for k, (x, y, a) in enumerate(along(vine, 34)):
            d = 1 if k % 2 else -1
            polys.append(petal_pts(x, y, 20, 6.5, (0 if sg > 0 else math.pi) + d * 0.8, n=12))
    for k in range(8):
        a = k * math.pi / 4
        polys.append(petal_pts(230, 40, 26 if k % 2 == 0 else 17, 8 if k % 2 == 0 else 5.5, a, n=12))
    m = np.maximum(strokes(W, H, items), shapes(W, H, polys))
    m = np.clip(m - circles(W, H, [(230, 40, 4)]), 0, 1)
    art = FO(blank(W, H), m, GOLD, seed=3601, emboss=0.8, sparkle=0.2)
    preview(art, "be-divider", bg=GROUND)
    save(art, f"{OUT}/divider.webp", max_w=260, quality=86)
    clear()
