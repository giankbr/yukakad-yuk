"""Ikat Adras — Central Asian adras/atlas silk warp ikat: a seamless silk tile of bold blurred-edge motifs (combs,
clouds, almond 'bodom' forms and hooked lozenges) in magenta, saffron, emerald and indigo on ivory, with warp-shifted
feathered edges, colour bleed and a silk sheen; a single large almond medallion, a lozenge divider band and a small
lozenge node. Geometry only: no figures, no calligraphy.
Run: python3 -I ikat-adras.py [part ...]   parts: tile medallion band node
Assets -> public/themes/art/ikat-adras/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h3_lib import *  # noqa

OUT = outdir("ikat-adras")
PARTS = sys.argv[1:] or ["tile", "medallion", "band", "node"]
MAG, MAG_D = "#c0185e", "#8e0f45"
SAF, SAF_D = "#eba51e", "#c98410"
EME, EME_D = "#0f7a52", "#0a5a3c"
IND, IND_D = "#23306e", "#161f4e"
IVO = "#f6eedd"


def vesica(cx, cy, w, h, n=40):
    """Almond (bodom) outline: pointed top and bottom."""
    pts = []
    for t in np.linspace(0, math.tau, n, endpoint=False):
        x = math.sin(t) * w / 2 * (1 - 0.15 * math.cos(t) ** 2)
        y = -math.cos(t) * h / 2
        x *= abs(math.sin(t)) ** 0.25
        pts.append((cx + x, cy + y))
    return pts


def comb(cx, cy, w, h, teeth, up=True):
    """Comb (taroq): a bar with rectangular teeth."""
    polys = [[(cx - w / 2, cy), (cx + w / 2, cy), (cx + w / 2, cy + h * 0.28), (cx - w / 2, cy + h * 0.28)]]
    tw = w / (teeth * 2 - 1)
    for k in range(teeth):
        x0 = cx - w / 2 + k * 2 * tw
        if up:
            polys.append([(x0, cy), (x0 + tw, cy), (x0 + tw, cy - h * 0.72), (x0, cy - h * 0.72)])
        else:
            polys.append([(x0, cy + h * 0.28), (x0 + tw, cy + h * 0.28), (x0 + tw, cy + h), (x0, cy + h)])
    return polys


def cloud(cx, cy, s, rng):
    """Stepped 'cloud' blob (bulut) made of lobes."""
    items = []
    for a in np.linspace(0, math.tau, 7, endpoint=False):
        items.append((cx + math.cos(a) * s * 0.55, cy + math.sin(a) * s * 0.8, s * rng.uniform(0.42, 0.52), s * rng.uniform(0.5, 0.62), 0))
    items.append((cx, cy, s * 0.7, s * 0.95, 0))
    return items


def ikat_layer(art, mask, col, col2, nx, seed, amp=7.0, bleed=0.35):
    """Paint a feathered ikat colour: warp-shifted edges + a faint bleed halo."""
    fm = warp_feather(mask, seed, axis=0, bundle=3, amp=amp, blur=1.0)
    if bleed:
        halo = np.clip(gaussian_filter(fm, (6, 1.5)) - fm, 0, 1)
        art = OV(art, halo, lambda m: col_arr(m, col, m * bleed), pad=10)
    art = OV(art, fm, lambda m: gouache_paint(m, col, col2, seed=nx(), rough=0.6, streak=0.4, density=0.97), pad=10)
    return art


def wrap_copies(fn, W, H):
    """Call fn(dx, dy) for the 9 wrap offsets so tiled motifs stay seamless."""
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            fn(dx, dy)


def sheen(art, seed, amt=0.12):
    H, W = art.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    s = 1 + amt * (np.sin(yy / H * math.tau * 2 + 0.6) * 0.6 + np.sin(yy / H * math.tau * 5 + 1.3) * 0.25)
    s = s * threads(W, H, axis=0, spacing=2.4, seed=seed, amt=0.07)
    return shade(art, np.ones((H, W), np.float32), s)


if "tile" in PARTS:
    W, H = 512, 768
    nx = Seq(91000); rng = random.Random(910)
    art = col_arr(np.ones((H, W), np.float32), IVO, np.ones((H, W), np.float32))
    # ground: three vertical warp bands (magenta | ivory | indigo | ivory) with saffron pin stripes
    bands = [(0, 128, MAG, MAG_D), (256, 384, IND, IND_D)]
    for x0, x1, c1, c2 in bands:
        m = np.zeros((H, W), np.float32); m[:, x0:x1] = 1
        art = OV(art, m, lambda mm: gouache_paint(mm, c1, c2, seed=nx(), rough=0, streak=0.5), pad=0)
    for x in (124, 132, 252, 260, 380, 388, 508, 4):
        m = np.zeros((H, W), np.float32); m[:, max(0, x - 2):x + 2] = 1
        art = ikat_layer(art, m, SAF, SAF_D, nx, 911 + x, amp=2, bleed=0)
    # column A (magenta band, x 0-128): ivory almonds with emerald hearts, stacked
    alm, almc, combs_ivo, combs_saf, clouds_e, clouds_s, loz_m, loz_s = [], [], [], [], [], [], [], []

    def placeA(dx, dy):
        for cy in (128, 512):
            alm.append([(x + dx, y + dy) for x, y in vesica(64, cy, 92, 220)])
            almc.append([(x + dx, y + dy) for x, y in vesica(64, cy, 44, 120)])
        for cy in (320, 704):
            combs_saf.extend([[(x + dx, y + dy) for x, y in p] for p in comb(64, cy, 84, 54, 5, True)])
            combs_saf.extend([[(x + dx, y + dy) for x, y in p] for p in comb(64, cy + 6, 84, 54, 5, False)])
    wrap_copies(placeA, W, H)
    # column B (ivory, x 128-256): emerald clouds and saffron clouds alternating
    cl_e, cl_s = [], []

    def placeB(dx, dy):
        for i, cy in enumerate((96, 288, 480, 672)):
            (cl_e if i % 2 == 0 else cl_s).extend([(x + dx, y + dy, a, b, r) for x, y, a, b, r in cloud(192, cy, 44, random.Random(i))])
    wrap_copies(placeB, W, H)
    # column C (indigo, x 256-384): magenta hooked lozenges with saffron cores
    lz, lzc, hk = [], [], []

    def placeC(dx, dy):
        for cy in (192, 576):
            lz.append([(320 + dx - 56, cy + dy), (320 + dx, cy + dy - 150), (320 + dx + 56, cy + dy), (320 + dx, cy + dy + 150)])
            lzc.append([(320 + dx - 24, cy + dy), (320 + dx, cy + dy - 66), (320 + dx + 24, cy + dy), (320 + dx, cy + dy + 66)])
        for cy in (0, 384, 768):
            for s_ in (-1, 1):
                hk.append(([(320 + dx + s_ * 52, cy + dy - 30), (320 + dx + s_ * 52, cy + dy), (320 + dx, cy + dy), (320 + dx, cy + dy + 30)], 14, None))
    wrap_copies(placeC, W, H)
    # column D (ivory, x 384-512): indigo combs facing each other + magenta dots
    cd, dots = [], []

    def placeD(dx, dy):
        for cy in (192, 576):
            cd.extend([[(x + dx, y + dy) for x, y in p] for p in comb(448, cy - 40, 92, 70, 6, True)])
            cd.extend([[(x + dx, y + dy) for x, y in p] for p in comb(448, cy + 20, 92, 70, 6, False)])
        for cy in (0, 384):
            dots.append((448 + dx, cy + dy, 22, 34, 0))
    wrap_copies(placeD, W, H)

    clipA = np.zeros((H, W), np.float32); clipA[:, 8:120] = 1
    clipB = np.zeros((H, W), np.float32); clipB[:, 136:248] = 1
    clipC = np.zeros((H, W), np.float32); clipC[:, 264:376] = 1
    clipD = np.zeros((H, W), np.float32); clipD[:, 392:504] = 1
    A1 = np.clip(shapes(W, H, alm), 0, 1) * clipA
    A2 = np.clip(shapes(W, H, almc), 0, 1) * clipA
    A3 = shapes(W, H, combs_saf, smooth=False) * clipA
    art = ikat_layer(art, A1, IVO, "#efe2c4", nx, 921)
    art = ikat_layer(art, A2, EME, EME_D, nx, 922)
    art = ikat_layer(art, A3, SAF, SAF_D, nx, 923)
    clear()
    art = ikat_layer(art, ellipses(W, H, cl_e) * clipB, EME, EME_D, nx, 924)
    art = ikat_layer(art, ellipses(W, H, cl_s) * clipB, SAF, SAF_D, nx, 925)
    clear()
    art = ikat_layer(art, shapes(W, H, lz, smooth=False) * clipC, MAG, MAG_D, nx, 926)
    art = ikat_layer(art, shapes(W, H, lzc, smooth=False) * clipC, SAF, SAF_D, nx, 927)
    art = ikat_layer(art, strokes(W, H, hk) * clipC, IVO, "#efe2c4", nx, 928, bleed=0.2)
    clear()
    art = ikat_layer(art, shapes(W, H, cd, smooth=False) * clipD, IND, IND_D, nx, 929)
    art = ikat_layer(art, ellipses(W, H, dots) * clipD, MAG, MAG_D, nx, 930)
    art = sheen(art, 931)
    art = add_grain(art, 932, 0.025)
    preview(art, "ia-tile")
    save_rgb(art, f"{OUT}/adras.webp", size=(256, 384), quality=82)
    clear()

if "medallion" in PARTS:
    W, H = 420, 620
    nx = Seq(92000); rng = random.Random(920)
    cx, cy = 210, 310
    art = blank(W, H)
    outer = shape_mask(W, H, vesica(cx, cy, 300, 560))
    # comb teeth around the outer almond
    teeth = []
    for k in range(-5, 6):
        y = cy + k * 44
        hw = 150 * (1 - (abs(y - cy) / 280) ** 2) ** 0.62 * 0.98
        if hw < 30:
            continue
        for s_ in (-1, 1):
            x0 = cx + s_ * hw
            teeth.append([(x0 - 2 * s_, y - 9), (x0 + s_ * 26, y - 9), (x0 + s_ * 26, y + 9), (x0 - 2 * s_, y + 9)])
    T = shapes(W, H, teeth, smooth=False)
    art = ikat_layer(art, T, SAF, SAF_D, nx, 940, amp=5)
    art = ikat_layer(art, outer, MAG, MAG_D, nx, 941, amp=8)
    r2 = shape_mask(W, H, vesica(cx, cy, 224, 440))
    art = ikat_layer(art, r2, IVO, "#efe2c4", nx, 942, amp=7, bleed=0.15)
    r3 = shape_mask(W, H, vesica(cx, cy, 170, 340))
    art = ikat_layer(art, r3, EME, EME_D, nx, 943, amp=6)
    r4 = shape_mask(W, H, vesica(cx, cy, 104, 220))
    art = ikat_layer(art, r4, SAF, SAF_D, nx, 944, amp=5)
    core = shapes(W, H, comb(cx, cy - 10, 70, 70, 4, True) + comb(cx, cy - 4, 70, 70, 4, False), smooth=False) * r4
    art = ikat_layer(art, core, IND, IND_D, nx, 945, amp=4)
    clear()
    m = np.clip(outer + T, 0, 1)
    sh = sheen(art, 946, 0.14)
    art = sh
    art = add_grain(art, 947, 0.025)
    preview(art, "ia-medallion", bg=IVO)
    save(art, f"{OUT}/medallion.webp", max_w=210, quality=84)
    clear()

if "band" in PARTS:
    W, H = 640, 72
    nx = Seq(93000)
    art = blank(W, H)
    cols = [(MAG, MAG_D), (SAF, SAF_D), (EME, EME_D), (IND, IND_D), (SAF, SAF_D), (MAG, MAG_D)]
    loz = {}
    xs = np.linspace(110, 530, 7)
    for i, x in enumerate(xs):
        s_ = 30 if i == 3 else 22
        loz.setdefault(cols[i % len(cols)], []).append([(x - s_, 36), (x, 36 - s_ * 1.3), (x + s_, 36), (x, 36 + s_ * 1.3)])
    line = np.zeros((H, W), np.float32); line[34:38, 20:620] = 1
    art = ikat_layer(art, line * np.clip(np.abs(np.arange(W) - 320)[None, :] / 300 * -1 + 1.1, 0, 1), IND, IND_D, nx, 950, amp=2, bleed=0)
    for (c1, c2), polys in loz.items():
        art = ikat_layer(art, shapes(W, H, polys, smooth=False), c1, c2, nx, 951 + len(polys), amp=4, bleed=0.2)
    cores = shapes(W, H, [[(x - 7, 36), (x, 27), (x + 7, 36), (x, 45)] for x in xs], smooth=False)
    art = ikat_layer(art, cores, IVO, "#efe2c4", nx, 958, amp=2, bleed=0)
    art = sheen(art, 959, 0.1)
    preview(art, "ia-band", bg=IVO)
    save(art, f"{OUT}/band.webp", max_w=320, quality=84)
    clear()

if "node" in PARTS:
    W = H = 120
    nx = Seq(94000)
    art = blank(W, H)
    art = ikat_layer(art, shapes(W, H, [[(10, 60), (60, 6), (110, 60), (60, 114)]], smooth=False), MAG, MAG_D, nx, 960, amp=4)
    art = ikat_layer(art, shapes(W, H, [[(32, 60), (60, 30), (88, 60), (60, 90)]], smooth=False), SAF, SAF_D, nx, 961, amp=3)
    art = ikat_layer(art, shapes(W, H, [[(48, 60), (60, 47), (72, 60), (60, 73)]], smooth=False), EME, EME_D, nx, 962, amp=2)
    art = sheen(art, 963, 0.1)
    preview(art, "ia-node", bg=IVO)
    save(art, f"{OUT}/node.webp", max_w=60, quality=86)
    clear()
