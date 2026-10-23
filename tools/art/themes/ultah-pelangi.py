"""Ultah Pelangi — kids' birthday in soft gouache: a big rainbow arch with fluffy clouds at its feet, a smiling sun
(face + separate rays), a balloon bunch and single balloons, drifting clouds, a mini-rainbow divider.
Run: python3 -I ultah-pelangi.py [part ...]   parts: rainbow sun balloons balloon cloud divider
Assets -> public/themes/art/ultah-pelangi/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l3_lib import *

OUT = outdir("ultah-pelangi")
PARTS = sys.argv[1:] or ["rainbow", "sun", "balloons", "balloon", "cloud", "divider"]
BANDS = [("#ef6f6c", "#e85d5f"), ("#f59a5b", "#f2874a"), ("#f7cd5a", "#f3bf45"), ("#8fcf8a", "#79c27a"), ("#6fb6e6", "#5ca7dd"), ("#a58ad8", "#9478cf")]
CLOUD, CLOUD_S = "#fdfbf6", "#c9d9ee"


def fluffy(art, W, H, cx, cy, w, h, rng, nx, shade=CLOUD_S, base=CLOUD):
    """Cumulus of overlapping round puffs: big ones in the middle, small at the ends, flat-ish base."""
    items = []
    n = max(4, int(w / (h * 0.62)))
    for i in range(n):
        t = (i + 0.5) / n
        x = cx - w / 2 + t * w + rng.uniform(-6, 6)
        r = h * (0.2 + 0.42 * math.sin(t * math.pi) ** 0.8) * rng.uniform(0.8, 1.2)
        items.append((x, cy - r * 0.45 - h * 0.12 * math.sin(t * math.pi), r))
    for i in range(max(2, n // 2)):
        t = rng.uniform(0.25, 0.75)
        r = h * rng.uniform(0.25, 0.38)
        items.append((cx - w / 2 + t * w, cy - h * 0.42 - r * 0.3, r))
    m = circles(W, H, items)
    m = np.maximum(m, ellipses(W, H, [(cx, cy - h * 0.02, w * 0.5, h * 0.16, 0)]))
    m = m * (np.mgrid[0:H, 0:W][0] < cy + h * 0.12)
    art = GP(art, m, base, "#f6f2ea", seed=nx(), rough=2.6, streak=0.25, pad=14)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    sh = m * np.clip((yy - (cy - h * 0.25)) / (h * 0.4), 0, 1)
    art = G(art, sh, shade, seed=nx(), density=0.55, edge=0.15, bloom=0.5, rough=3, feather=3)
    # each puff gets its own lower-right crescent of shadow so the lobes read separately
    cres = np.zeros((H, W), np.float32)
    order = sorted(items, key=lambda it: it[2])  # big puffs in front of small ones
    for k, (x, y, r) in enumerate(order):
        c = np.clip(circles(W, H, [(x, y, r)]) - circles(W, H, [(x - r * 0.16, y - r * 0.2, r * 0.97)]), 0, 1)
        front = circles(W, H, order[k + 1:]) if k + 1 < len(order) else 0
        cres = np.maximum(cres, c * (1 - front))
    art = G(art, gaussian_filter(cres, 1.5) * m, "#a9bfdc", seed=nx(), density=0.6, edge=0.15, bloom=0.2, rough=2, feather=1.5)
    return art


def arc_band(W, H, cx, cy, r0, r1, a0=math.pi, a1=2 * math.pi):
    pts = arc_pts(cx, cy, r1, a0, a1, 60) + arc_pts(cx, cy, r0, a1, a0, 60)
    return shapes(W, H, [pts], smooth=False)


if "rainbow" in PARTS:
    W, H = 820, 500
    nx = Seq(61000)
    rng = random.Random(3)
    art = blank(W, H)
    cx, cy = 410, 440
    R, bw = 380, 40
    for i, (c1, c2) in enumerate(BANDS):
        m = arc_band(W, H, cx, cy, R - (i + 1) * bw - 6, R - i * bw)
        art = GP(art, m, c1, c2, seed=nx(), rough=2.6, streak=1.0, pad=10)
        # curved brush streaks inside the band (lighter, paint dragged along the arc)
        st = strokes(W, H, [(arc_pts(cx, cy, R - i * bw - bw * rng.uniform(0.25, 0.7), math.pi + rng.uniform(0.05, 0.4), 2 * math.pi - rng.uniform(0.05, 0.5), 40), rng.uniform(2, 4), (0.3, 0.3)) for _ in range(2)])
        art = G(art, st * m, "#ffffff", seed=nx(), density=0.35, edge=0.1, bloom=0, rough=1.5)
        clear()
    art = fluffy(art, W, H, 110, 470, 230, 110, rng, nx)
    art = fluffy(art, W, H, 715, 474, 220, 104, rng, nx)
    clear()
    prev(art, "up-rainbow", bg="#bfe3f5")
    save(art, f"{OUT}/rainbow.webp", max_w=640, quality=82)

if "sun" in PARTS:
    # face (static) + rays (separate asset, slow spin)
    W = H = 360
    nx = Seq(62000)
    cx = cy = 180
    face = blank(W, H)
    disc = circles(W, H, [(cx, cy, 104)])
    face = GP(face, disc, "#f9c94c", "#f6b53a", seed=nx(), rough=2.4, streak=0.8, pad=10)
    face = G(face, disc * np.clip((np.mgrid[0:H, 0:W][0] - 120) / 160, 0, 1), "#f29a3a", seed=nx(), density=0.35, edge=0.3, bloom=0.3, rough=2)
    face = G(face, ellipses(W, H, [(cx - 34, cy - 40, 30, 16, -30)]), "#fff0b0", seed=nx(), density=0.5, edge=0.1, bloom=0.2, rough=2)
    # gentle closed eyes (smiling arcs), rosy cheeks, small smile
    eyes = strokes(W, H, [(arc_pts(cx - 36, cy - 4, 15, math.pi * 1.1, math.pi * 1.9, 14), 5, (0.2, 0.2)), (arc_pts(cx + 36, cy - 4, 15, math.pi * 1.1, math.pi * 1.9, 14), 5, (0.2, 0.2))])
    face = GP(face, eyes, "#7a4a2a", seed=nx(), rough=0.6, pad=6)
    cheeks = circles(W, H, [(cx - 58, cy + 22, 17), (cx + 58, cy + 22, 17)])
    face = G(face, cheeks, "#f2847a", seed=nx(), density=0.55, edge=0.2, bloom=0.3, rough=3, feather=2.5)
    smile = strokes(W, H, [(arc_pts(cx, cy + 14, 24, math.pi * 0.2, math.pi * 0.8, 16), 5, (0.2, 0.2))])
    face = GP(face, smile, "#7a4a2a", seed=nx(), rough=0.6, pad=6)
    prev(face, "up-sun", bg="#bfe3f5")
    save(face, f"{OUT}/sun.webp", max_w=180, quality=84)
    W = H = 520
    cx = cy = 260
    rays = blank(W, H)
    rp = []
    for k in range(14):
        a = k * math.tau / 14
        L = 86 if k % 2 else 110
        rp.append(petal_pts(cx + math.cos(a) * 140, cy + math.sin(a) * 140, L, 22 if k % 2 else 28, a, n=12))
    rays = GP(rays, shapes(W, H, rp), "#f7cd5a", "#f5b046", seed=nx(), rough=2.6, streak=0.8, pad=10)
    prev(rays, "up-rays", bg="#bfe3f5")
    save_full(rays, f"{OUT}/rays.webp", size=(260, 260), quality=82)

if "balloons" in PARTS:
    W, H = 420, 660
    nx = Seq(63000)
    art = blank(W, H)
    knot = (220, 560)
    specs = [(140, 210, 82, "#ef6f6c", "#d85458"), (290, 170, 88, "#6fb6e6", "#4f97cf"), (215, 320, 78, "#f7cd5a", "#eab23a"), (330, 330, 66, "#a58ad8", "#8a6fc6")]
    strs = [(curve([(x + 2, y + r * 1.18 + 10), ((x + knot[0]) / 2 + 14, (y + knot[1]) / 2 + 30), knot], 30), 2.2, None) for x, y, r, _, _ in specs]
    art = GP(art, strokes(W, H, strs + [(curve([knot, (230, 600), (214, 650)], 16), 2.2, None)]), "#8a7c74", seed=nx(), rough=0.6, pad=6)
    for (x, y, r, c1, c2) in specs:
        body = shapes(W, H, [deform([(x + math.cos(a) * r * (1 - 0.12 * math.sin(a)), y + math.sin(a) * r * 1.18) for a in np.linspace(0, math.tau, 26, endpoint=False)], random.Random(int(x)), 1, 0.02)])
        tie = shapes(W, H, [[(x - 8, y + r * 1.18 + 12), (x + 8, y + r * 1.18 + 12), (x, y + r * 1.18 - 2)]], smooth=False)
        art = GP(art, np.clip(body + tie, 0, 1), c1, c2, seed=nx(), rough=2.2, streak=0.8, pad=10)
        sh = body * np.clip(((np.mgrid[0:H, 0:W][1] - x) + (np.mgrid[0:H, 0:W][0] - y)) / (r * 2.2), 0, 1)
        art = G(art, sh, c2, seed=nx(), density=0.5, edge=0.2, bloom=0.3, rough=2)
        hi = strokes(W, H, [(arc_pts(x, y, r * 0.66, math.pi * 1.08, math.pi * 1.42, 12), r * 0.13, (0.3, 0.3))])
        art = G(art, hi, "#ffffff", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=1)
        clear()
    prev(art, "up-balloons", bg="#bfe3f5")
    save(art, f"{OUT}/balloons.webp", max_w=260, quality=82)

if "balloon" in PARTS:
    W, H = 160, 300
    nx = Seq(64000)
    art = blank(W, H)
    x, y, r = 80, 84, 58
    art = GP(art, strokes(W, H, [(curve([(x, y + r * 1.18 + 10), (x + 14, 210), (x - 6, 292)], 20), 2.4, None)]), "#8a7c74", seed=nx(), rough=0.6, pad=6)
    body = shapes(W, H, [[(x + math.cos(a) * r * (1 - 0.12 * math.sin(a)), y + math.sin(a) * r * 1.18) for a in np.linspace(0, math.tau, 26, endpoint=False)]])
    tie = shapes(W, H, [[(x - 7, y + r * 1.18 + 11), (x + 7, y + r * 1.18 + 11), (x, y + r * 1.18 - 2)]], smooth=False)
    art = GP(art, np.clip(body + tie, 0, 1), "#ef6f6c", "#d85458", seed=nx(), rough=2, streak=0.8, pad=10)
    art = G(art, body * np.clip(((np.mgrid[0:H, 0:W][1] - x) + (np.mgrid[0:H, 0:W][0] - y)) / (r * 2.2), 0, 1), "#c94a50", seed=nx(), density=0.45, edge=0.2, bloom=0.3, rough=2)
    art = G(art, strokes(W, H, [(arc_pts(x, y, r * 0.66, math.pi * 1.08, math.pi * 1.42, 12), r * 0.13, (0.3, 0.3))]), "#ffffff", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=1)
    prev(art, "up-balloon", bg="#bfe3f5")
    save(art, f"{OUT}/balloon.webp", max_w=80, quality=84)

if "cloud" in PARTS:
    W, H = 520, 240
    nx = Seq(65000)
    rng = random.Random(9)
    art = fluffy(blank(W, H), W, H, 260, 180, 400, 150, rng, nx)
    prev(art, "up-cloud", bg="#bfe3f5")
    save(art, f"{OUT}/cloud.webp", max_w=320, quality=82)

if "divider" in PARTS:
    W, H = 420, 170
    nx = Seq(66000)
    rng = random.Random(12)
    art = blank(W, H)
    cx, cy = 210, 150
    R, bw = 140, 16
    for i, (c1, c2) in enumerate(BANDS):
        art = GP(art, arc_band(W, H, cx, cy, R - (i + 1) * bw - 4, R - i * bw), c1, c2, seed=nx(), rough=1.8, streak=0.8, pad=8)
    art = fluffy(art, W, H, 76, 156, 120, 56, rng, nx)
    art = fluffy(art, W, H, 344, 158, 114, 52, rng, nx)
    prev(art, "up-divider", bg="#fff8ec")
    save(art, f"{OUT}/divider.webp", max_w=240, quality=84)
