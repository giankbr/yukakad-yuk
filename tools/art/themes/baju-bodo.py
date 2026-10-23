"""Baju Bodo — the sheer, boxy baju bodo of Makassar/Bugis painted as fabric (transparent watercolour glazes with
crease lines, hung on a wooden rod), lipa' sabbe silk check tile, gold kalung, Losari coastline at dusk.
Run: python3 -I baju-bodo.py [part ...]; parts: bodo hijau sabbe kalung losari kembang.
Assets -> public/themes/art/baju-bodo/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l1_lib import *

OUT = outdir("baju-bodo")
PARTS = sys.argv[1:] or ["bodo", "hijau", "sabbe", "kalung", "losari", "kembang"]
TANG, TANG_L, TANG_D = "#ec5418", "#f98a46", "#a8300c"
EMER, EMER_L, EMER_D = "#159a6a", "#4cc792", "#0b5a3c"
TEAL, TEAL_D = "#12505a", "#0b333a"
GOLD = "#c99a3f"


def blouse(W, H, col, col_l, col_d, seed, rod=True, scale=1.0):
    """Baju bodo on a rod: one wide rectangle (the short sleeves are part of the box) with a shallow round neck,
    puffed shoulders, armhole openings down the sides, crinkled pressed pleats across, gold sequins on the hem."""
    nx = Seq(seed)
    rng = random.Random(seed)
    art = blank(W, H)
    s_ = scale
    cx = W / 2
    top = 96 * s_
    L, R = cx - 380 * s_, cx + 380 * s_
    hem = top + 420 * s_
    sil = [(L + 10 * s_, top + 30 * s_), (L + 60 * s_, top + 4 * s_), (cx - 200 * s_, top - 6 * s_), (cx - 70 * s_, top), (cx + 70 * s_, top), (cx + 200 * s_, top - 6 * s_), (R - 60 * s_, top + 4 * s_), (R - 10 * s_, top + 30 * s_),
           (R + 6 * s_, hem - 30 * s_), (R - 4 * s_, hem), (cx, hem + 8 * s_), (L + 4 * s_, hem), (L - 6 * s_, hem - 30 * s_)]
    m = shape_mask(W, H, deform(sil, rng, 1, 0.006))
    neck = shapes(W, H, [deform(ellipse_pts(cx, top + 4 * s_, 70 * s_, 34 * s_, 16), rng, 1, 0.03)])
    m = np.clip(m - neck, 0, 1)
    m = gaussian_filter(m, 1.0)
    # sheer wash, two layers (front + back) so the sleeves read lighter than the body
    art = G(art, m, col, col_l, seed=nx(), density=0.74, edge=0.7, bloom=0.35, rough=2.2, feather=0.9, gran=0.15)
    body = shape_mask(W, H, [(cx - 230 * s_, top), (cx + 230 * s_, top), (cx + 236 * s_, hem), (cx - 236 * s_, hem)], smooth=False) * m
    art = G(art, body, col, col_d, seed=nx(), density=0.42, edge=0.5, bloom=0.4, rough=1.5, feather=0.8)
    # armhole openings: soft vertical shadow lines where the sleeves fold
    arm = strokes(W, H, [(curve([(cx + d * 236 * s_, top + 20 * s_), (cx + d * 244 * s_, top + 150 * s_), (cx + d * 238 * s_, top + 260 * s_)], 30), 5 * s_, (0.05, 0.6)) for d in (-1, 1)])
    art = G(art, arm, col_d, seed=nx(), density=0.55, edge=0.3, bloom=0, rough=1.5, feather=1.5)
    # crinkled pressed pleats: broken wavy lines, alternating dark crease + light ridge
    dark, light = [], []
    y = top + 26 * s_
    while y < hem - 8 * s_:
        x = L + rng.uniform(-10, 40) * s_
        while x < R - 20 * s_:
            seg = rng.uniform(80, 260) * s_
            x1 = min(R, x + seg)
            amp = rng.uniform(1.5, 4) * s_; ph = rng.uniform(0, 6)
            pts = [(xx, y + amp * math.sin(xx / (24 * s_) + ph) + rng.gauss(0, 0.4)) for xx in np.linspace(x, x1, max(4, int(seg / 8)))]
            dark.append((pts, rng.uniform(0.9, 2.0) * s_, (0.25, 0.25)))
            light.append(([(px, py + 2.5 * s_) for px, py in pts], rng.uniform(1.2, 2.4) * s_, (0.25, 0.25)))
            x = x1 + rng.uniform(10, 50) * s_
        y += rng.uniform(9, 19) * s_
    art = G(art, strokes(W, H, dark) * m, col_d, col, seed=nx(), density=0.5, edge=0.2, bloom=0, rough=1.0, feather=0.5)
    art = OV(art, strokes(W, H, light) * m * 0.32, lambda mm: tint(mm, "#fff3e6"))
    # rolled hems and neck edge
    edge = np.clip(m - gaussian_filter(m, 2.5) * 1.3, 0, 1) * 2.2
    art = G(art, np.clip(edge, 0, 1), col_d, seed=nx(), density=0.6, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    # rod over the shoulders (in front, so the fabric hangs from it)
    if rod:
        rodm = strokes(W, H, [([(40 * s_, top + 14 * s_), (W - 40 * s_, top + 10 * s_)], 20 * s_, None)])
        art = GP(art, rodm, "#9a6a3c", "#6a4222", seed=nx(), rough=0.8, streak=1.2, pad=8)
        art = G(art, np.clip(rodm - lift(rodm, 0, 4), 0, 1), "#3a2410", seed=nx(), density=0.55, edge=0, bloom=0, rough=0.5)
        art = OV(art, np.clip(rodm - lift(rodm, 0, -4), 0, 1) * 0.4, lambda mm: tint(mm, "#f6d7a8"))
        knobs = circles(W, H, [(40 * s_, top + 14 * s_, 13 * s_), (W - 40 * s_, top + 10 * s_, 13 * s_)])
        art = GP(art, knobs, "#7a4a26", "#5a3418", seed=nx(), rough=0.6, pad=6)
    # gold sequins on the hem
    seq = circles(W, H, [(x, hem - 16 * s_ + rng.gauss(0, 1.5), 3.0 * s_) for x in np.linspace(L + 24 * s_, R - 24 * s_, 46)] +
                  [(x, hem - 30 * s_ + rng.gauss(0, 1.5), 2.2 * s_) for x in np.linspace(L + 36 * s_, R - 36 * s_, 23)])
    art = FO(art, seq, GOLD, seed=nx(), emboss=0.6, sparkle=0.2)
    return art


if "bodo" in PARTS:
    W, H = 900, 640
    art = blouse(W, H, TANG, TANG_L, TANG_D, 50100)
    preview(art, "bb-bodo", tone="#f6ecdf")
    save(art, f"{OUT}/bodo.webp", max_w=640, quality=80)
    clear()

if "hijau" in PARTS:
    # a second baju bodo in emerald, without rod (used folded/smaller in sections)
    W, H = 900, 640
    art = blouse(W, H, EMER, EMER_L, EMER_D, 51100, rod=False)
    preview(art, "bb-hijau", tone="#f6ecdf")
    save(art, f"{OUT}/hijau.webp", max_w=420, quality=78)
    clear()

if "sabbe" in PARTS:
    # lipa' sabbe: silk check (balo') — seamless tile, woven warp/weft with sheen
    W = H = 360
    rng = random.Random(3)
    # stripe sequence (same for warp and weft) in px widths
    seq = [("#d8432a", 44), (GOLD, 3), ("#0f4c55", 5), (GOLD, 3), ("#d8432a", 44), ("#f2a33c", 10), ("#d8432a", 44), (GOLD, 3), ("#0f4c55", 5), (GOLD, 3),
           ("#d8432a", 44), ("#0f4c55", 18), ("#1f9a6a", 4), ("#0f4c55", 18)]
    tot = sum(w for _, w in seq); k = W / tot
    band = np.zeros((W, 3), np.float32); pos = 0
    for c, w in seq:
        n = round(w * k); band[pos:pos + n] = hex_rgb(c); pos += n
    band[pos:] = band[pos - 1]
    warp = np.repeat(band[None, :, :], H, 0)   # vertical stripes
    weft = np.repeat(band[:, None, :], W, 1)   # horizontal stripes
    yy, xx = np.mgrid[0:H, 0:W]
    twill = (((xx + yy) // 2) % 2).astype(np.float32)[..., None]
    rgb = warp * twill + weft * (1 - twill)
    rgb = rgb * 0.55 + (warp + weft) / 2 * 0.45
    sheen = wrap_noise(W, H, 4, (2, 20))[..., None]
    rgb = rgb * (0.9 + 0.2 * sheen)
    fine = (np.random.default_rng(5).random((H, W)) - 0.5)[..., None] * 0.05
    rgb = np.clip(rgb * (1 + fine), 0, 1)
    arr = np.concatenate([rgb, np.ones((H, W, 1), np.float32)], -1)
    save_rgb(arr, f"{OUT}/sabbe.webp", quality=82)
    preview(arr, "bb-sabbe")

if "kalung" in PARTS:
    # gold necklace (kalung) laid in a gentle arc: beaded chain, filigree links, a crescent-and-flower pendant
    W, H = 760, 330
    nx = Seq(52100)
    art = blank(W, H)
    arc = [(x, 60 + 140 * (1 - ((x - W / 2) / (W / 2 - 30)) ** 2)) for x in np.linspace(30, W - 30, 120)]
    art = FO(art, strokes(W, H, [(arc, 3, None)]), GOLD, seed=nx(), emboss=0.5)
    beads = [(x, y, 7) for (x, y, _) in along(arc, 22)]
    art = FO(art, circles(W, H, beads), GOLD, seed=nx(), emboss=0.9, sparkle=0.25)
    # filigree links: small rosettes every 4th bead
    ros = []
    for i, (x, y, r) in enumerate(beads):
        if i % 4 == 2:
            for k in range(6):
                a = k * math.tau / 6
                ros.append(petal_pts(x, y, 15, 6, a, n=8))
    art = FO(art, shapes(W, H, ros), "#d9ad52", seed=nx(), emboss=0.8, sparkle=0.2)
    art = GP(art, circles(W, H, [(x, y, 3.2) for i, (x, y, r) in enumerate(beads) if i % 4 == 2]), "#9e1f2d", seed=nx(), rough=0.3, pad=4)
    # pendant at the lowest point
    cx, cy = W / 2, 60 + 140 + 26
    cres = np.clip(circles(W, H, [(cx, cy + 34, 52)]) - circles(W, H, [(cx, cy + 14, 46)]), 0, 1)
    flower = shapes(W, H, [petal_pts(cx, cy + 30, 30, 12, a, n=10) for a in [k * math.tau / 8 for k in range(8)]])
    drops = shapes(W, H, [petal_pts(cx + dx, cy + 86 + abs(dx) * -0.3, 22, 8, math.pi / 2, n=10) for dx in (-40, 0, 40)])
    art = FO(art, np.maximum.reduce([cres, flower, drops, strokes(W, H, [([(cx, cy - 20), (cx, cy + 4)], 4, None)])]), GOLD, seed=nx(), emboss=0.9, sparkle=0.25)
    art = GP(art, circles(W, H, [(cx, cy + 30, 9)]), "#9e1f2d", "#c2394a", seed=nx(), rough=0.3, pad=4)
    art = OV(art, circles(W, H, [(cx - 3, cy + 27, 2.5)]) * 0.8, lambda m: tint(m, "#ffd9dc"))
    preview(art, "bb-kalung", tone="#f6ecdf")
    save(art, f"{OUT}/kalung.webp", max_w=420, quality=80)
    clear()

if "losari" in PARTS:
    # Losari at dusk: apricot sky, low sun, teal sea with a glitter path, promenade railing and lamps, a floating
    # mosque silhouette far right, small lepa-lepa boats
    W, H = 900, 380
    nx = Seq(53100)
    art = painted_sky(W, H, [(0, "#f6b98a"), (0.35, "#f8cf9c"), (0.52, "#fbe2b8"), (1, "#fbe2b8")], seed=nx(), streak=1.0)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    sun = circles(W, H, [(300, 196, 34)])
    art = OV(art, glow(sun, "#ffd9a0", radius=30, strength=0.6), lambda m: m) if False else art
    art = over(art, glow(sun, "#fff0c8", radius=26, strength=0.45))
    art = G(art, sun, "#f7894a", "#f9a85c", seed=nx(), density=0.9, edge=0.3, bloom=0.2, rough=1.5)
    clouds = shapes(W, H, [deform(ellipse_pts(x, y, rx, ry, 12), random.Random(int(x)), 2, 0.1) for x, y, rx, ry in [(140, 80, 120, 12), (560, 60, 160, 10), (760, 120, 110, 9), (420, 140, 90, 7)]])
    art = G(art, clouds, "#e7907a", "#f2a88e", seed=nx(), density=0.55, edge=0.4, bloom=0.4, rough=6, feather=2)
    # far islands (Lae-Lae, Samalona hints)
    isl = shapes(W, H, [[(560, 214), (600, 204), (650, 206), (690, 214)], [(80, 214), (110, 208), (150, 210), (170, 214)]])
    art = G(art, isl, "#6f7f7e", seed=nx(), density=0.6, edge=0.3, rough=2)
    # sea
    sea = shapes(W, H, [rect(-10, 212, W + 10, H + 10)], smooth=False)
    art = G(art, sea * np.clip((yy - 212) / 150, 0.35, 1), "#1f6f78", "#2f8a8c", seed=nx(), density=0.88, edge=0.1, bloom=0.2, rough=2)
    rng = random.Random(8)
    glit = [([(300 + rng.gauss(0, 10 + (y - 212) * 0.35) - L / 2, y), (300 + rng.gauss(0, 10 + (y - 212) * 0.35) + L / 2, y)], rng.uniform(1.2, 3), (0.3, 0.3)) for y, L in [(rng.uniform(216, 330), rng.uniform(8, 46)) for _ in range(70)]]
    art = OV(art, strokes(W, H, glit) * 0.85, lambda m: tint(m, "#ffd7a1"))
    waves = [([(x, y), (x + rng.uniform(30, 90), y)], 1.4, (0.3, 0.3)) for x, y in [(rng.uniform(0, W), rng.uniform(222, 330)) for _ in range(70)]]
    art = G(art, strokes(W, H, waves), "#145059", seed=nx(), density=0.5, edge=0, bloom=0, rough=1)
    # floating mosque silhouette (two small domes and a slim minaret), with reflection
    mos = shapes(W, H, [rect(736, 186, 842, 214), rect(758, 176, 820, 188)], smooth=False)
    def dome(cx_, by, r):
        return [(cx_ + math.cos(a) * r, by - math.sin(a) * r * 1.15) for a in np.linspace(0, math.pi, 20)]
    mos = np.maximum(mos, shapes(W, H, [dome(789, 177, 22), dome(752, 187, 11), dome(826, 187, 11)], smooth=False))
    mos = np.maximum(mos, shapes(W, H, [rect(855, 128, 862, 214), [(853, 130), (858.5, 108), (864, 130)], rect(787, 142, 791, 152)], smooth=False))
    art = G(art, mos, "#47404a", "#5a4f55", seed=nx(), density=0.9, edge=0.3, rough=0.4, feather=0.6, bloom=0)
    art = G(art, np.flipud(np.roll(mos, -(428 - 2 * 214), 0)) * ((yy > 214) & (yy < 250)) * 0.4, "#244f55", seed=nx(), density=0.5, edge=0, bloom=0.3, rough=3, feather=2)
    # boats
    boats = shapes(W, H, [[(440, 262), (490, 262), (498, 256), (484, 268), (448, 268)], [(560, 240), (588, 240), (594, 236), (584, 244), (562, 244)]])
    art = G(art, boats, "#2b2224", seed=nx(), density=0.85, edge=0.3, rough=0.8)
    # promenade: railing and lamps in the foreground
    deck = shapes(W, H, [rect(-10, 336, W + 10, H + 10)], smooth=False)
    art = G(art, deck, "#5a3b38", "#6d4840", seed=nx(), density=0.92, edge=0.3, rough=1.5)
    rail = strokes(W, H, [([(-10, 306), (W + 10, 306)], 4, None), ([(-10, 322), (W + 10, 322)], 3, None)] + [([(x, 304), (x, 338)], 3, None) for x in range(10, W, 36)])
    lamps = strokes(W, H, [([(x, 338), (x, 238)], 4.5, None) for x in (120, 520, 700)] + [([(x - 14, 240), (x + 14, 240)], 3, None) for x in (120, 520, 700)])
    art = G(art, np.maximum(rail, lamps), "#3a2626", seed=nx(), density=0.88, edge=0.3, rough=0.8)
    bulbs = circles(W, H, [(x + dx, 232, 6) for x in (120, 520, 700) for dx in (-12, 12)])
    art = over(art, glow(bulbs, "#ffe3a8", radius=7, strength=0.9))
    art = G(art, bulbs, "#ffe8b0", seed=nx(), density=0.9, edge=0.2, rough=0.5)
    art = add_grain(art, 6, 0.03)
    save_rgb(art, f"{OUT}/losari.webp", size=(780, 329), quality=78)
    preview(art, "bb-losari")
    clear()

if "kembang" in PARTS:
    # small gold rosette with red stone (bunga simpolong-inspired) — node / divider centre
    W = H = 240
    nx = Seq(54100)
    art = blank(W, H)
    cx = cy = 120
    outer = shapes(W, H, [petal_pts(cx, cy, 100, 34, a, n=12) for a in [k * math.tau / 8 for k in range(8)]])
    inner = shapes(W, H, [petal_pts(cx, cy, 64, 22, a + math.pi / 8, n=12) for a in [k * math.tau / 8 for k in range(8)]])
    art = FO(art, outer, GOLD, seed=nx(), emboss=0.9, sparkle=0.2)
    art = G(art, np.clip(outer - gaussian_filter(outer, 4) * 1.1, 0, 1), "#7a5418", seed=nx(), density=0.5, edge=0, bloom=0, rough=0.5)
    art = FO(art, inner, "#dcb45e", seed=nx(), emboss=0.9, sparkle=0.25)
    art = GP(art, circles(W, H, [(cx, cy, 22)]), "#9e1f2d", "#c2394a", seed=nx(), rough=0.4, pad=4)
    art = FO(art, ring(W, H, cx, cy, 26, 5), GOLD, seed=nx(), emboss=0.8)
    art = OV(art, circles(W, H, [(cx - 7, cy - 7, 5)]) * 0.75, lambda m: tint(m, "#ffd9dc"))
    preview(art, "bb-kembang", tone="#f6ecdf")
    save(art, f"{OUT}/kembang.webp", max_w=120, quality=82)
