"""Tuban Gedog — tenun gedog Tuban (handspun coarse cotton, natural and indigo) with batik gedog motifs (ganggeng
seaweed, kijing miring shells, a stylised bird), the north-coast sea at Tuban with painted fishing boats.
Run: python3 -I tuban-gedog.py [part ...]  parts: weave indigo laut perahu edge motif divider
Assets -> public/themes/art/tuban-gedog/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m1_lib import *

OUT = outdir("tuban-gedog")
PARTS = sys.argv[1:] or ["weave", "indigo", "laut", "perahu", "edge", "motif", "divider"]
NAT, NAT_D = "#e7dcc3", "#cdbd9c"
IND, IND_D, IND_L = "#22395c", "#152742", "#3d5a82"
MADDER = "#9c3b2a"
SAND = "#d9c49b"


def wrap_items(items, W, H):
    out = []
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            for pts, w, t in items:
                out.append(([(x + dx, y + dy) for x, y in pts], w, t))
    return out


def ganggeng(x, y0, y1, s, d=1):
    """Seaweed: wavy stem with alternating curled fronds."""
    stem = curve([(x, y0), (x + 10 * s * d, y0 + (y1 - y0) * .33), (x - 10 * s * d, y0 + (y1 - y0) * .66), (x, y1)], 40)
    items = [(stem, 5 * s, (0.1, 0.1))]
    for k, (px, py, a) in enumerate(along(stem, 22 * s)):
        side = 1 if k % 2 else -1
        ex, ey = px + side * 22 * s, py - 10 * s
        fr = curve([(px, py), (px + side * 12 * s, py - 2 * s), (ex, ey)], 10)
        cur = spiral_pts(ex, ey - 6 * s, 6 * s, 1.5 * s, math.pi / 2, 0.9, 16, side)
        cur = [(cx + ex - cur[0][0], cy + ey - cur[0][1]) for cx, cy in cur]
        items.append((fr + cur[1:], 3.2 * s, (0.0, 0.5)))
    return items


def batik_cloth(W, H, motif, seed, ground=IND, ground2=IND_D, wax=NAT, crackle=0.5, weave=True):
    """Indigo-dyed gedog: dyed ground with uneven dye take-up, wax-resisted motif in natural cotton with crackle veins
    and soft bleed, coarse thread texture over all."""
    m = displace(motif, seed, 1.6, 10)
    m = np.clip((gaussian_filter(m, 0.8) - 0.3) * 2.6, 0, 1)
    t = fbm(W, H, seed + 1, 70, 3)[..., None]
    rgb = col3(ground) * (1 - t) + col3(ground2) * t
    # dye blotches
    b = fbm(W, H, seed + 2, 24, 3)[..., None]
    rgb = rgb * (0.92 + 0.16 * b)
    wx = col3(wax) * (0.95 + 0.08 * fbm(W, H, seed + 3, 30, 2)[..., None])
    # pale blue halo where indigo crept under the wax
    halo = np.clip(gaussian_filter(m, 2.2) - m, 0, 1)[..., None]
    rgb = rgb * (1 - halo * 0.5) + col3(mix(ground, wax, 0.45)) * halo * 0.5
    rgb = rgb * (1 - m[..., None]) + wx * m[..., None]
    if crackle:
        n = fbm(W, H, seed + 4, 14, 3)
        vein = np.clip(1 - np.abs(n - 0.5) * 40, 0, 1)
        n2 = fbm(W, H, seed + 5, 9, 2)
        vein = np.maximum(vein, np.clip(1 - np.abs(n2 - 0.5) * 50, 0, 1) * 0.7)
        rgb = rgb * (1 - (vein * m * crackle)[..., None]) + col3(ground) * (vein * m * crackle)[..., None]
    if weave:
        rgb = rgb * weave_shade(H, W, seed + 6, 3.4, 3.1, 1.0)[..., None]
    return np.clip(rgb, 0, 1).astype(np.float32)


def weave():
    W = H = 320
    rgb = handspun(W, H, 3, NAT, 4.4, 4.0, slub=2.0, dark="#b4a181")
    rgb = rgb / rgb.reshape(-1, 3).mean(0) * col3(NAT)
    rgb = rgb * 0.6 + col3(NAT) * 0.4
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/weave.webp", quality=74)


def indigo():
    """Seamless indigo batik gedog tile: ganggeng columns between rows of kijing miring shells."""
    W = H = 360
    items = []
    for x in (60, 240):
        items += ganggeng(x, -10, H + 10, 1.25, 1 if x < 100 else -1)
    shells = []
    for (cx, cy) in [(150, 60), (150, 180), (150, 300), (330, 0), (330, 120), (330, 240), (330, 360)]:
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):
                x, y = cx + dx, cy + dy
                shells.append([(x - 26, y + 14), (x - 6, y - 26), (x + 26, y - 14), (x + 6, y + 26)])
    sm = shapes(W, H, shells)
    inner = []
    for p in shells:
        cx = sum(q[0] for q in p) / 4; cy = sum(q[1] for q in p) / 4
        inner.append([(cx + (q[0] - cx) * 0.55, cy + (q[1] - cy) * 0.55) for q in p])
    im = shapes(W, H, inner)
    dots = circles(W, H, [(sum(q[0] for q in p) / 4, sum(q[1] for q in p) / 4, 4.5) for p in shells])
    motif = np.maximum(strokes(W, H, wrap_items(items, W, H)), np.clip(sm - im, 0, 1) + dots)
    # isen-isen: fine dotted fill (cecek)
    rng = random.Random(5)
    cec = circles(W, H, [(rng.uniform(0, W), rng.uniform(0, H), 1.3) for _ in range(260)])
    motif = np.clip(motif + cec * (1 - dilate(motif, 5)), 0, 1)
    rgb = batik_cloth(W, H, motif, 7)
    save_rgb(rgba(rgb, np.ones((H, W), np.float32)), f"{OUT}/indigo.webp", quality=76)


def boat_mask(W, H, x, y, L, flip=1):
    """Pantura fishing boat (perahu) side view: long hull with tall curved prow and stern, cabin and mast.
    Returns dict of part masks."""
    def P(u, v):
        return (x + u * L * flip, y + v * L)
    hull = shapes(W, H, [curve([P(-0.5, -0.06), P(-0.56, -0.22), P(-0.52, -0.28), P(-0.42, -0.08), P(0.0, -0.04), P(0.4, -0.08),
                                P(0.56, -0.32), P(0.62, -0.30), P(0.52, -0.06), P(0.36, 0.06), P(-0.34, 0.06), P(-0.5, -0.06)], 60)])
    stripe1 = shapes(W, H, [[P(-0.48, -0.06), P(0.5, -0.06), P(0.46, -0.02), P(-0.46, -0.02)]], smooth=False) * hull
    stripe2 = shapes(W, H, [[P(-0.44, -0.0), P(0.44, -0.0), P(0.4, 0.03), P(-0.4, 0.03)]], smooth=False) * hull
    cabin = shapes(W, H, [[P(-0.22, -0.05), P(0.06, -0.05), P(0.06, -0.15), P(-0.22, -0.15)]], smooth=False)
    roof = shapes(W, H, [[P(-0.26, -0.15), P(0.1, -0.15), P(0.06, -0.18), P(-0.22, -0.18)]], smooth=False)
    mast = strokes(W, H, [([P(0.2, -0.05), P(0.2, -0.62)], max(2, L * 0.012), None), ([P(0.2, -0.6), P(-0.3, -0.12)], max(1, L * 0.005), None)])
    flag = shapes(W, H, [[P(0.2, -0.62), P(0.34, -0.58), P(0.2, -0.54)]], smooth=False)
    eye = circles(W, H, [(*P(0.5, -0.2), L * 0.018)])
    return dict(hull=hull, s1=stripe1, s2=stripe2, cabin=cabin, roof=roof, mast=mast, flag=flag, eye=eye)


def paint_boat(art, W, H, x, y, L, nx, flip=1, hullc="#2f6b5e", s1="#d8a62c", s2=MADDER, cab="#e9e1cc"):
    b = boat_mask(W, H, x, y, L, flip)
    art = GP(art, b["mast"], "#3a2c22", seed=nx(), rough=0.8)
    art = GP(art, b["hull"], hullc, mix(hullc, "#10201c", 0.35), seed=nx(), rough=1.2, streak=0.8)
    art = GP(art, b["s1"], s1, seed=nx(), rough=0.8)
    art = GP(art, b["s2"], s2, seed=nx(), rough=0.8)
    art = GP(art, b["cabin"], cab, "#cfc4a8", seed=nx(), rough=0.8)
    art = GP(art, b["roof"], "#1f4a7a", seed=nx(), rough=0.6)
    art = GP(art, b["flag"], "#c0392b", seed=nx(), rough=0.5)
    art = GP(art, b["eye"], "#f1ead6", seed=nx(), rough=0.3)
    return art, b["hull"]


def laut():
    """Tuban shore at morning: pale sky, low sun haze, banded north-coast sea, moored perahu, a bamboo drying rack."""
    W, H = 760, 560
    rng = random.Random(3); nx = Seq(300)
    art = painted_sky(W, H, [(0, "#b9c9cb"), (0.22, "#d9ddd0"), (0.42, "#f1d9b0"), (0.5, "#f0c99a"), (0.515, "#7f9ea2"), (0.75, "#3f6b76"), (1, "#2e5560")], seed=8, streak=1.2)
    # sun haze
    sun = circles(W, H, [(W * 0.72, H * 0.43, 34)])
    art = over(art, glow(sun, "#fbe3b4", 60, 0.75))
    art = OV(art, sun, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#fbe9c4"), np.clip(gaussian_filter(m, 1.2), 0, 1) * 0.95))
    # soft clouds
    for (cx, cy, rx) in [(W * 0.2, H * 0.14, 120), (W * 0.55, H * 0.2, 90), (W * 0.9, H * 0.12, 80)]:
        cl = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, rx * 0.18, 12), rng, 3, 0.15)])
        art = G(art, cl, "#efe6d3", "#e2d5bb", seed=nx(), density=0.5, edge=0.25, bloom=0.4, rough=8)
    # far coast hills (kapur limestone of Tuban)
    hl = hills(W, H, H * 0.5, 14, 4, 0.6) * (np.arange(H)[:, None] < H * 0.515)
    art = G(art, hl, "#9aa89a", "#8a9a8e", seed=nx(), density=0.7, edge=0.3, bloom=0.3, rough=5)
    # sea bands
    for k, y in enumerate(np.linspace(H * 0.53, H * 0.98, 14)):
        band = strokes(W, H, [([(x, y + math.sin(x / 50 + k) * 2) for x in np.arange(-20, W + 20, 20)], rng.uniform(2, 5), (0.1, 0.1))])
        art = G(art, band * fbm(W, H, 40 + k, 40, 2) * 1.6, "#2d5560" if k % 2 else "#8fb0ad", seed=nx(), density=0.55, edge=0.2, bloom=0, rough=4)
    crests = strokes(W, H, [([(x, y), (x + rng.uniform(10, 34) * (0.5 + (y - H * 0.5) / H), y - 1)], 1.6 + 2.5 * (y - H * 0.5) / H, (0.3, 0.4))
                             for x, y in [(rng.uniform(-20, W), rng.uniform(H * 0.56, H * 0.86)) for _ in range(150)]])
    art = OV(art, crests, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#e8efe6"), m * 0.75))
    glint = strokes(W, H, [([(W * 0.72 + rng.gauss(0, 30), y), (W * 0.72 + rng.gauss(0, 30) + rng.uniform(14, 40), y)], 2, (0.3, 0.3)) for y in np.linspace(H * 0.54, H * 0.7, 18)])
    art = OV(art, glint, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#f6e7c2"), m * 0.7))
    # boats far and near
    for (bx, by, L, f, hc, c1, c2) in [(0.1, 0.545, 70, 1, "#2c5d8f", "#e9e1cc", MADDER), (0.33, 0.55, 80, -1, "#8a3b2c", "#e1b443", "#2c5d8f"),
                                       (0.9, 0.548, 64, -1, "#2f6b5e", "#e1b443", MADDER), (0.24, 0.66, 150, 1, "#b8452e", "#f0c64a", "#1f4a7a"),
                                       (0.6, 0.63, 120, -1, "#1f4a7a", "#e9e1cc", "#c0392b")]:
        art, _ = paint_boat(art, W, H, W * bx, H * by, L, nx, f, hc, c1, c2)
    # sandy foreground
    beach = np.zeros((H, W), np.float32)
    pts = [(-20, H)] + [(x, H * 0.9 - 22 * math.sin(x / W * math.pi) + rng.uniform(-3, 3)) for x in np.arange(-20, W + 40, 30)] + [(W + 20, H)]
    beach = shapes(W, H, [pts], smooth=False)
    art = GP(art, beach, SAND, "#c9ae7e", seed=nx(), rough=4, streak=1.2)
    art = G(art, beach * fbm(W, H, 77, 30, 3), "#b39367", seed=nx(), density=0.45, edge=0.2, bloom=0.4, rough=5, gran=0.6)
    foam = strokes(W, H, [([(x, H * 0.902 - 22 * math.sin(x / W * math.pi) + 2) for x in np.arange(-20, W + 40, 20)], 4, (0.05, 0.05))])
    art = OV(art, foam, lambda m: rgba(np.ones(m.shape + (3,), np.float32) * col3("#f3eee0"), m * 0.7))
    art = add_grain(art, 9, 0.03)
    preview(art, "tg-laut")
    save_rgb(art, f"{OUT}/laut.webp", size=(720, int(720 * H / W)), quality=78)


def perahu():
    """Near boat, separate so it can bob on the cover."""
    W, H = 420, 260
    nx = Seq(500)
    art = blank(W, H)
    art, hull = paint_boat(art, W, H, W * 0.5, H * 0.8, 340, nx, 1, "#1f5e4c", "#e1b443", MADDER)
    # little reflection shadow
    sh = gaussian_filter(np.roll(hull, 18, 0) * (np.arange(H)[:, None] > H * 0.8), 4) * 0.35
    art = over(rgba(np.ones((H, W, 3), np.float32) * col3("#30505a"), sh), art)
    preview(art, "tg-perahu", bg="#86a3a4")
    save(art, f"{OUT}/perahu.webp", max_w=360, quality=82)


def edge():
    """Frayed top edge of the natural gedog cloth with a woven indigo stripe, seamless repeat-x."""
    W, H = 360, 90
    rgb = handspun(W, H, 21, NAT, 3.4, 3.1)
    st = np.zeros((H, W), np.float32); st[40:48] = 1; st[54:57] = 1
    rgb = rgb * (1 - st[..., None]) + (col3(IND) * weave_shade(H, W, 22, 3.4, 3.1)[..., None]) * st[..., None]
    m = np.zeros((H, W), np.float32); m[18:] = 1
    n = wrap_noise(W, H, 23, (1, 4))
    yy = np.arange(H)[:, None]
    m = np.clip(((yy - 18 + (n - 0.5) * 18) > 0).astype(np.float32), 0, 1)
    # loose warp threads hanging up
    rng = random.Random(4)
    hairs = []
    for x in np.arange(2, W, 5):
        if rng.random() < 0.6:
            L = rng.uniform(4, 16)
            hairs.append(([(x, 22), (x + rng.gauss(0, 1.2), 22 - L * 0.5), (x + rng.gauss(0, 2), 22 - L)], 1.3, (0.0, 0.6)))
    hm = strokes(W, H, hairs)
    a = np.maximum(m, hm * 0.9)
    a = gaussian_filter(a, 0.5)
    save_full(rgba(rgb, a), f"{OUT}/edge.webp", quality=80)


def motif():
    """Stylised bird among ganggeng (batik gedog), indigo with wax crackle, round-cornered square swatch."""
    W, H = 300, 300
    items = ganggeng(60, 40, 270, 1.0, 1) + ganggeng(246, 50, 270, 0.9, -1)
    # bird: body teardrop, long curled tail plumes, crest
    body = shapes(W, H, [petal_pts(150, 140, 92, 30, math.pi * 0.92, n=16)])
    head = circles(W, H, [(74, 136, 18)])
    beak = shapes(W, H, [[(58, 132), (40, 140), (58, 142)]], smooth=False)
    wing = shapes(W, H, [curve([(110, 130), (150, 92), (196, 84), (180, 112), (140, 140)], 30)])
    tail = []
    for k, a in enumerate([0.15, 0.45, 0.75]):
        p = curve([(146, 142), (196, 148 + k * 14), (220, 160 + k * 18), (240, 186 + k * 26), (232, 214 + k * 22)], 30)
        sp = spiral_pts(0, 0, 12, 3, math.pi, 1.0, 20, -1)
        sp = [(x + p[-1][0] - sp[0][0], y + p[-1][1] - sp[0][1]) for x, y in sp]
        tail.append((p + sp[1:], 7 - k, (0.05, 0.5)))
    crest = [(curve([(74, 120), (82, 96), (100, 88)], 12), 3.5, (0.0, 0.5))]
    birdm = np.maximum.reduce([body, head, beak, wing, strokes(W, H, tail + crest)])
    eye = circles(W, H, [(70, 134, 3.5)])
    inner = np.clip(shapes(W, H, [petal_pts(150, 140, 70, 18, math.pi * 0.92, n=16)]) - wing, 0, 1)
    dots = circles(W, H, [(120 + i * 12, 146 + (i % 2) * 4, 2.6) for i in range(4)])
    motif = np.clip(np.maximum(strokes(W, H, items), birdm) - eye - inner * 0.0, 0, 1)
    wax = np.clip(motif - np.clip(inner * 0.0 + dots, 0, 1), 0, 1)
    swatch = np.zeros((H, W), np.float32)
    swatch = shapes(W, H, [[(14, 14), (W - 14, 14), (W - 14, H - 14), (14, H - 14)]], smooth=False)
    rgb = batik_cloth(W, H, wax, 31)
    a = fray(swatch, 32, 3.0, 0.8)
    art = rgba(rgb, a)
    preview(art, "tg-motif", bg="#e7dcc3")
    save(art, f"{OUT}/motif.webp", max_w=240, quality=82)


def divider():
    """Running-stitch line with a small indigo ganggeng sprig in the middle."""
    W, H = 340, 56
    nx = Seq(700)
    art = blank(W, H)
    st = strokes(W, H, [([(x, H / 2 + 0.6 * math.sin(x)), (x + 9, H / 2 + 0.6 * math.sin(x + 9))], 2.4, (0.2, 0.2)) for x in list(np.arange(8, 120, 15)) + list(np.arange(222, W - 12, 15))])
    art = G(art, st, IND, seed=nx(), density=0.95, edge=0.3, bloom=0, rough=0.5, feather=0.4)
    sp = []
    for side in (-1, 1):
        for k in range(3):
            x0 = W / 2 + side * (14 + k * 26)
            fr = curve([(W / 2, H / 2), (x0, H / 2 - 10 + k * 2), (x0 + side * 10, H / 2 - 18 + k * 4)], 14)
            cur = spiral_pts(0, 0, 6, 1.5, math.pi / 2, 0.9, 14, side)
            cur = [(x + fr[-1][0] - cur[0][0], y + fr[-1][1] - cur[0][1]) for x, y in cur]
            sp.append((fr + cur[1:], 3, (0.0, 0.5)))
    sp.append(([(W / 2 - 80, H / 2 + 2), (W / 2 + 80, H / 2 + 2)], 3.4, (0.1, 0.1)))
    art = G(art, strokes(W, H, sp), IND, IND_D, seed=nx(), density=0.92, edge=0.5, bloom=0.1, rough=1.2, feather=0.6)
    art = G(art, circles(W, H, [(W / 2, H / 2 + 2, 5)]), MADDER, seed=nx(), density=0.9, edge=0.4, rough=0.6)
    save(art, f"{OUT}/divider.webp", max_w=340, quality=84)


for p in PARTS:
    globals()[p]()
    clear()
