"""Geode Biru — sliced blue agate geode: concentric bands following the stone's outline, a sparkling quartz-crystal
cavity, gold-leaf rim; small slice, gold-leaf stroke divider, white-marble tile.
Run: python3 -I geode-biru.py [part ...]  parts: geode slice leaf marble flakes
Assets -> public/themes/art/geode-biru/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l5_lib import *
from scipy.ndimage import distance_transform_edt

OUT = outdir("geode-biru")
PARTS = sys.argv[1:] or ["geode", "slice", "leaf", "marble"]
GOLD = "#caa24c"

# band palette from rim inwards: (distance fraction, colour)
BANDS = [(0.00, "#13234a"), (0.06, "#1d3c78"), (0.10, "#e9f1fa"), (0.12, "#3c6fb7"), (0.20, "#24508f"), (0.26, "#8fb5e2"),
         (0.29, "#f4f8fc"), (0.31, "#5d8ccc"), (0.40, "#1b3a73"), (0.46, "#a9c7ea"), (0.50, "#dfeaf7"), (0.54, "#4a7cc0"),
         (0.62, "#2b5aa0"), (0.70, "#cfe0f3"), (1.00, "#eef5fc")]


def band_rgb(t):
    t = np.clip(t, 0, 1)
    xs = np.array([b[0] for b in BANDS], np.float32)
    cols = np.array([hex_rgb(b[1]) for b in BANDS], np.float32)
    out = np.zeros(t.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(t, xs, cols[:, c])
    return out


def geode(W, H, cx, cy, rx, ry, seed, cavity=0.62, rim=10.0):
    rng = random.Random(seed); nx = Seq(seed * 10)
    outline = deform([(cx + math.cos(k / 16 * math.tau) * rx * rng.uniform(.86, 1.08), cy + math.sin(k / 16 * math.tau) * ry * rng.uniform(.86, 1.08)) for k in range(16)], rng, 3, 0.08)
    m = shapes(W, H, [outline])
    m = (m > 0.5).astype(np.float32)
    d = distance_transform_edt(m).astype(np.float32)
    dmax = d.max()
    # warp the distance field so bands wobble like real agate
    warp = (fbm(W, H, seed + 1, 60, 4) - 0.5) * dmax * 0.16 + (fbm(W, H, seed + 2, 18, 3) - 0.5) * dmax * 0.03
    t = np.clip((d + warp * np.clip(d / (dmax * 0.15), 0, 1)) / dmax, 0, 1)
    rgb = band_rgb(t / cavity * 0.70)
    # fine growth lines inside bands
    fine = 0.5 + 0.5 * np.sin(t * dmax * 0.9 + fbm(W, H, seed + 3, 30, 2) * 4)
    rgb *= (0.94 + 0.06 * fine)[..., None]
    # cavity: quartz druzy crystals
    cav = (t > cavity).astype(np.float32)
    cav = gaussian_filter(cav, 1.2)
    ys, xs = np.nonzero(cav > 0.5)
    ccx, ccy = float(xs.mean()), float(ys.mean())
    cv = Canvas(W, H)
    cv.c.clear(skia.Color4f(0.22, 0.22, 0.22, 1.0))
    items = []
    for _ in range(int(len(xs) / 70) + 60):
        j = rng.randrange(len(xs)); x, y = float(xs[j]), float(ys[j])
        dd = t[int(y), int(x)]
        items.append((dd, x, y))
    items.sort()
    for dd, x, y in items:
        k = np.clip((dd - cavity) / (1 - cavity), 0, 1)
        s_ = rng.uniform(7, 16) * (1.25 - 0.7 * k)
        a = math.atan2(ccy - y, ccx - x) + rng.uniform(-.6, .6)
        ca, sa = math.cos(a), math.sin(a)
        tip = (x + ca * s_ * 1.8, y + sa * s_ * 1.8)
        l = (x - sa * s_ * 0.55, y + ca * s_ * 0.55); r = (x + sa * s_ * 0.55, y - ca * s_ * 0.55)
        mid = (x + ca * s_ * 0.6, y + sa * s_ * 0.6)
        lum = rng.uniform(0.7, 1.0)
        light_side = (ca * -0.6 + sa * -0.8) > 0
        for pts, lv in (([l, mid, tip], lum if light_side else lum * 0.62), ([r, mid, tip], lum * 0.62 if light_side else lum), ([l, r, mid], lum * 0.85)):
            cv.c.drawPath(poly_path(pts), skia.Paint(AntiAlias=True, Color=skia.Color4f(lv, lv, lv, 1.0)))
    crys = cv.array()[..., 0]
    cav_rgb = np.array(hex_rgb("#20437f"), np.float32) * (1 - crys[..., None]) * 1.2 + np.array(hex_rgb("#e4eefa"), np.float32) * crys[..., None]
    cav_rgb = np.clip(cav_rgb, 0, 1)
    lining = np.clip(1 - np.abs(t - cavity) / 0.025, 0, 1)
    rgb = rgb * (1 - lining[..., None] * 0.6) + np.array(hex_rgb("#132a5c"), np.float32) * lining[..., None] * 0.6
    spark = (np.random.default_rng(seed).random((H, W)) > 0.9965).astype(np.float32) * cav
    spark = gaussian_filter(spark, 0.7) * 5 + gaussian_filter(spark, 2.5) * 6
    cav_rgb = np.clip(cav_rgb + spark[..., None], 0, 1)
    rgb = rgb * (1 - cav[..., None]) + cav_rgb * cav[..., None]
    # polished slab: soft sheen + slight edge darkening
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sheen = np.exp(-(((xx - cx + rx * 0.35) / (rx * 0.7)) ** 2 + ((yy - cy + ry * 0.45) / (ry * 0.5)) ** 2))
    rgb = np.clip(rgb + sheen[..., None] * 0.08, 0, 1)
    art = np.concatenate([rgb, m[..., None]], -1)
    art[..., 3] = gaussian_filter(m, 0.7)
    # painterly glaze over bands (watercolour mottle so it doesn't look rendered)
    art = G(art, m * (1 - cav), "#284f92", seed=nx(), density=0.12, edge=0.05, bloom=0.6, rough=3, mottle=0.9)
    # gold-leaf rim: ring + broken flakes spilling onto the stone
    ring_m = np.clip(m - (d > rim).astype(np.float32), 0, 1)
    flk = fbm(W, H, seed + 9, 9, 3)
    flakes = ((d > rim) & (d < rim * 3.2) & (flk > 0.66)).astype(np.float32)
    outer = np.clip(gaussian_filter(m, 2.5) * 3, 0, 1) - m
    outer = (np.clip(outer, 0, 1) * (fbm(W, H, seed + 11, 12, 3) > 0.45)).astype(np.float32)
    gm = np.clip(ring_m + flakes * 0.95 + outer, 0, 1)
    art = FO(art, gm, GOLD, seed=nx(), emboss=0.8, sparkle=0.35)
    return art


if "geode" in PARTS:
    W, H = 760, 700
    art = geode(W, H, 380, 350, 330, 300, 7, cavity=0.6, rim=11)
    preview(art, "geode-main", bg="#0d1a33")
    save(art, f"{OUT}/geode.webp", max_w=700, quality=82)
    clear()

if "slice" in PARTS:
    W, H = 300, 280
    art = geode(W, H, 150, 140, 124, 110, 23, cavity=0.55, rim=6)
    preview(art, "geode-slice", bg="#0d1a33")
    save(art, f"{OUT}/slice.webp", max_w=180, quality=84)
    clear()

if "leaf" in PARTS:
    # gold-leaf brush stroke divider with a ragged, flaking edge
    W, H = 700, 90
    rng = random.Random(3); nx = Seq(300)
    pts = curve([(30, 50), (200, 42), (360, 48), (520, 40), (670, 46)], 60)
    m = strokes(W, H, [(pts, 14, (0.25, 0.3))])
    ragged = displace(m, 5, 4, 10)
    flk = fbm(W, H, 8, 7, 3)
    m2 = np.clip(ragged * (0.4 + flk) - 0.2, 0, 1)
    specks = circles(W, H, [(rng.uniform(40, 660), rng.uniform(26, 68), rng.uniform(1, 3)) for _ in range(40)])
    art = FO(blank(W, H), np.clip(m2 + specks, 0, 1), GOLD, seed=nx(), emboss=0.6, sparkle=0.3)
    preview(art, "geode-leaf", bg="#0d1a33")
    save(art, f"{OUT}/leaf.webp", max_w=340)

if "marble" in PARTS:
    n = 512
    base = paper_tile(n, "#f4f2ee", seed=4, fiber=0.3)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    w1 = wrap_noise(n, n, 11, 40); w2 = wrap_noise(n, n, 12, 12)
    u = (xx + yy * 0.6) / n * math.tau * 2 + (w1 - 0.5) * 9 + (w2 - 0.5) * 2.5
    vein = np.exp(-((np.sin(u) * 6) ** 2) * 0.6)
    vein2 = np.exp(-((np.sin(u * 0.5 + 1.3 + (w2 - 0.5) * 3) * 9) ** 2) * 0.5)
    v = np.clip(vein * 0.55 + vein2 * 0.35, 0, 1) * (0.4 + 0.6 * wrap_noise(n, n, 13, 20))
    rgb = base[..., :3] * (1 - v[..., None] * 0.11) + np.array(hex_rgb("#9aa7bb"), np.float32) * v[..., None] * 0.1
    gold = np.clip(vein2 - 0.7, 0, 1) * 2 * (wrap_noise(n, n, 15, 30) > 0.55)
    rgb = rgb * (1 - gold[..., None] * 0.5) + np.array(hex_rgb("#d2b06a"), np.float32) * gold[..., None] * 0.5
    t = np.concatenate([np.clip(rgb, 0, 1), np.ones((n, n, 1), np.float32)], -1)
    save_texture(t, f"{OUT}/marble.webp", quality=74)
    print("marble", os.path.getsize(f"{OUT}/marble.webp") // 1024, "KB")

kb_total(OUT)
