"""Bordir Tasik — Tasikmalaya kerancang embroidery rendered at thread level: padded satin petals and fishbone leaves,
stem-stitched tendrils, buttonhole eyelets cut through white cotton voile (the pale-green lining shows through),
scalloped buttonhole hems. White-on-white with pale hijau pupus thread.
Run: python3 -I bordir-tasik.py [part ...]   parts: voile linen hem oval medal sprig bloom corner
Assets -> public/themes/art/bordir-tasik/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _i4_lib import *  # noqa

OUT = outdir("bordir-tasik")
PARTS = sys.argv[1:] or ["voile", "linen", "hem", "oval", "medal", "sprig", "bloom", "corner"]
FAB = "#fbfaf4"
WH, WG = "#fdfcf6", "#bccab3"          # white thread, its shadow
PG, PGG = "#d2e4c2", "#8ea782"          # pale green thread
DG, DGG = "#a9c597", "#6b8a60"          # deeper green accent thread
HOLE = "#d5e5c6"                        # lining seen through cutwork


def leaf_pair(art, W, H, x, y, ang, L, wd, th, gp, seed, spread=0.55):
    for k, s in enumerate((-1, 1)):
        a = ang + s * spread
        tip = (x + math.cos(a) * L, y + math.sin(a) * L)
        art = satin_leaf(art, W, H, (x, y), tip, wd, th, gp, seed=seed + k * 5, bend=s * L * 0.08)
    return art


def spray(art, W, H, pts, rng, seed, big=(0.5,), leaves=6, th_leaf=(PG, PGG), size=1.0, eyelets=4):
    """A tendril with leaves along it, a flower at the end, eyelets trailing."""
    art = stem(art, W, H, pts, 4.2 * size, PG, PGG, seed=seed)
    L = len(pts)
    for i in range(leaves):
        t = 0.15 + 0.7 * i / max(1, leaves - 1)
        j = int(t * (L - 2))
        (x0, y0), (x1, y1) = pts[j], pts[j + 1]
        a = math.atan2(y1 - y0, x1 - x0) + (0.95 if i % 2 else -0.95)
        Lf = (34 + rng.uniform(-6, 6)) * size * (1.1 - 0.4 * t)
        tip = (x0 + math.cos(a) * Lf, y0 + math.sin(a) * Lf)
        th, gp = th_leaf if i % 3 else (WH, WG)
        art = satin_leaf(art, W, H, (x0, y0), tip, Lf * 0.36, th, gp, seed=seed + 10 + i, bend=(1 if i % 2 else -1) * Lf * 0.12)
    ex, ey = pts[-1]
    art = flower(art, W, H, ex, ey, 30 * size, 5, WH, WG, seed=seed + 40, rot=rng.uniform(0, 6), hole=HOLE)
    for k in range(eyelets):
        t = 0.25 + 0.5 * k / max(1, eyelets - 1)
        j = int(t * (L - 2))
        (x0, y0), (x1, y1) = pts[j], pts[j + 1]
        a = math.atan2(y1 - y0, x1 - x0) + (math.pi / 2 if k % 2 else -math.pi / 2)
        off = 26 * size
        art = eyelet(art, W, H, x0 + math.cos(a) * off, y0 + math.sin(a) * off, (4.5 + rng.uniform(0, 2.5)) * size, None, WH, WG, hole=HOLE, seed=seed + 60 + k, cut=False)
    return art


if "voile" in PARTS:
    t = weave(256, 256, FAB, 256 / 104, seed=3, contrast=0.1)
    save_full(t, f"{OUT}/voile.webp", quality=86, rgb=True)

if "linen" in PARTS:
    t = weave(256, 256, "#dbe8cf", 256 / 72, seed=5, contrast=0.14)
    save_full(t, f"{OUT}/linen.webp", quality=86, rgb=True)

if "hem" in PARTS:
    W, H = 780, 210
    rng = random.Random(11)
    P = 52; base = 150; depth = 30
    def edge(x):
        f = (x % P) / P
        return base + depth * math.sin(math.pi * f) ** 0.7
    contour = [(x, edge(x)) for x in range(-2, W + 3)]
    art = weave(W, H, FAB, 256 / 104, seed=3, contrast=0.045)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ey = np.array([edge(x) for x in range(W)], np.float32)[None, :]
    art[..., 3] = np.clip(ey + 3 - yy, 0, 1)
    band = np.clip(ey + 3 - yy, 0, 1) * np.clip(yy - (ey - 10), 0, 1)
    art = stitch(art, band, u_path(W, H, contour), WH, WG, spacing=2.0, pad=0.9, seed=4, raise_=2.6, cast=0.25)
    purl = strokes(W, H, [([(x, edge(x) - 11) for x in range(-2, W + 3, 2)], 1.6, None)])
    art = stitch(art, purl, u_path(W, H, contour, 0.9), PG, PGG, spacing=2.4, pad=0.5, seed=5, raise_=1.0, cast=0.15)
    for i in range(W // P + 1):
        cx = i * P + P / 2
        art = eyelet(art, W, H, cx, base + 5, 6.0, 3.0, WH, WG, hole=HOLE, seed=30 + i, cut=False)
    # wave tendril above, flowers in the troughs, kerancang cut-outs on the crests
    Q = 156
    wave = [(x, base - 56 + 16 * math.sin(x / Q * math.tau)) for x in range(-20, W + 21, 6)]
    art = vine(art, W, H, wave, rng, 300, every=26, Lf=24, stem_w=3.2)
    for k in range(-1, W // Q + 2):
        fx = k * Q + Q * 0.75
        art = flower(art, W, H, fx, base - 56 - 16, 23, 5, WH, WG, seed=80 + k, rot=rng.uniform(0, 6), hole=HOLE)
        cx = k * Q + Q * 0.25
        art = cutwork(art, W, H, cx - 12, base - 26, 22, 7, math.pi * 0.72, WH, WG, HOLE, seed=140 + k)
        art = cutwork(art, W, H, cx + 12, base - 26, 22, 7, math.pi * 0.28, WH, WG, HOLE, seed=150 + k)
        art = satin_dot(art, W, H, fx, base - 22, 3.4, DG, DGG, seed=170 + k)
    art = edge_fade(art, 40, "t")
    save(art, f"{OUT}/hem.webp", quality=78)
    prev(art, "bt-hem", "#cfe0c3")
    clear()

def frame(W, H, cx, cy, rx, ry, seed, clusters):
    rng = random.Random(seed)
    art = blank(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    th = np.arctan2((yy - cy) / ry, (xx - cx) / rx)
    rr = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    k = 2.0 / (rx + ry)
    sc = 11 * k + 7 * k * np.abs(np.sin(th * round((rx + ry) / 22))) ** 0.7
    band = np.clip((rr - 1.0) / k, 0, 1) * np.clip((1.0 + sc - rr) / k, 0, 1)
    art = stitch(art, band, u_polar(W, H, cx, cy, (rx + ry) / 2), WH, WG, spacing=2.0, pad=1.0, seed=seed + 3, raise_=2.4)
    ring = [(cx + math.cos(a) * rx * (1 + 7 * k), cy + math.sin(a) * ry * (1 + 7 * k)) for a in np.linspace(0, math.tau, 260)]
    art = stem(art, W, H, ring, 2.4, PG, PGG, seed=seed + 7, tilt=0.6, cast=0.12)
    # vine all around, outside the scallops
    vr = 1 + 30 * k
    vpts = [(cx + math.cos(a) * rx * vr, cy + math.sin(a) * ry * vr) for a in np.linspace(-math.pi / 2 + 0.25, math.tau - math.pi / 2 - 0.25, 300)]
    art = vine(art, W, H, vpts, rng, seed + 20, every=30, Lf=27, stem_w=3.2)
    # cut-outs and eyelets radiating outside the vine
    for j, a in enumerate(np.linspace(0, math.tau, 26, endpoint=False)):
        er = 1 + 62 * k
        x, y = cx + math.cos(a) * rx * er, cy + math.sin(a) * ry * er
        if j % 2:
            art = eyelet(art, W, H, x, y, 4.4, None, WH, WG, hole=HOLE, seed=seed + 400 + j, cut=False)
        else:
            art = cutwork(art, W, H, x, y, 20, 7, a, WH, WG, HOLE, seed=seed + 500 + j)
    for (fa, fr, n) in clusters:
        x, y = cx + math.cos(fa) * rx * vr, cy + math.sin(fa) * ry * vr
        art = leaf_pair(art, W, H, x, y, fa, 44 * fr / 40, 16 * fr / 40, PG, PGG, seed=seed + 600, spread=0.9)
        art = flower(art, W, H, x, y, fr, n, WH, WG, seed=seed + 610 + n, rot=fa, hole=HOLE)
    for j, a in enumerate(np.linspace(0.6, math.tau + 0.6, 7, endpoint=False)):
        x, y = cx + math.cos(a) * rx * vr, cy + math.sin(a) * ry * vr
        art = flower(art, W, H, x, y, 19, 5, WH if j % 2 else PG, WG if j % 2 else PGG, seed=seed + 700 + j, rot=a, hole=HOLE)
    return art

if "oval" in PARTS:
    art = frame(620, 780, 310, 390, 206, 282, 21, [(-math.pi / 2, 42, 6), (math.pi / 2, 34, 5)])
    save(art, f"{OUT}/oval.webp", quality=80)
    prev(art, "bt-oval", "#f7f6ef")
    clear()

if "medal" in PARTS:
    art = frame(560, 560, 280, 280, 168, 168, 31, [(-math.pi / 2, 40, 6)])
    save(art, f"{OUT}/medal.webp", quality=80)
    prev(art, "bt-medal", "#f7f6ef")
    clear()

if "sprig" in PARTS:
    W, H = 380, 100
    rng = random.Random(41)
    art = blank(W, H)
    cx, cy = 190, 52
    for side in (-1, 1):
        pts = curve([(cx + side * 16, cy + 2), (cx + side * 70, cy - 16), (cx + side * 120, cy + 6), (cx + side * 166, cy - 6)], 40)
        art = stem(art, W, H, pts, 3.2, PG, PGG, seed=10 + side)
        for i, t in enumerate((0.2, 0.42, 0.64, 0.86)):
            j = int(t * 38)
            (x0, y0), (x1, y1) = pts[j], pts[j + 1]
            a = math.atan2(y1 - y0, x1 - x0) + (-1.0 if i % 2 else 1.0)
            Lf = 26 - 10 * t
            c = (PG, PGG) if i % 2 == 0 else (WH, WG)
            art = satin_leaf(art, W, H, (x0, y0), (x0 + math.cos(a) * Lf, y0 + math.sin(a) * Lf), Lf * 0.38, *c, seed=20 + i + side * 7)
        art = eyelet(art, W, H, cx + side * 172, cy - 7, 3.6, None, WH, WG, hole=HOLE, seed=30 + side, cut=False)
        art = satin_dot(art, W, H, cx + side * 96, cy - 24, 2.8, DG, DGG, seed=33 + side)
    art = flower(art, W, H, cx, cy, 24, 5, WH, WG, seed=50, rot=-0.3, hole=HOLE)
    save(art, f"{OUT}/sprig.webp", quality=82)
    prev(art, "bt-sprig", "#f7f6ef")
    clear()

if "bloom" in PARTS:
    W, H = 150, 150
    art = blank(W, H)
    art = satin_leaf(art, W, H, (75, 80), (130, 118), 18, PG, PGG, seed=5)
    art = satin_leaf(art, W, H, (75, 80), (22, 122), 16, PG, PGG, seed=6)
    art = flower(art, W, H, 75, 70, 52, 6, WH, WG, seed=9, rot=-0.25, hole=HOLE, notch=0.1)
    save(art, f"{OUT}/bloom.webp", quality=82)
    prev(art, "bt-bloom", "#f7f6ef")

if "corner" in PARTS:
    W, H = 320, 320
    rng = random.Random(51)
    art = blank(W, H)
    pts = curve([(8, 312), (40, 220), (110, 150), (200, 90), (290, 60)], 60)
    art = spray(art, W, H, pts, rng, 500, leaves=7, size=1.0, eyelets=5)
    p2 = curve([(60, 200), (40, 130), (60, 60), (100, 24)], 40)
    art = stem(art, W, H, p2, 3.4, PG, PGG, seed=600)
    for i, t in enumerate((0.3, 0.6, 0.85)):
        j = int(t * 38); (x0, y0), (x1, y1) = p2[j], p2[j + 1]
        a = math.atan2(y1 - y0, x1 - x0) + (1.0 if i % 2 else -1.0)
        art = satin_leaf(art, W, H, (x0, y0), (x0 + math.cos(a) * 26, y0 + math.sin(a) * 26), 9.5, WH, WG, seed=610 + i)
    art = flower(art, W, H, 100, 24, 18, 5, WH, WG, seed=620, rot=0.4, hole=HOLE)
    art = flower(art, W, H, 150, 150, 22, 5, PG, PGG, seed=630, rot=1.0, hole=HOLE)
    save(art, f"{OUT}/corner.webp", quality=80)
    prev(art, "bt-corner", "#f7f6ef")
