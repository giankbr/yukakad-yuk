"""Wisuda Santri — pesantren graduation & khataman in green and white, gouache: a stack of plain-covered kitab topped
with a black velvet peci, a white pesantren gate with green tajug caps between mango trees, a folded kotak-kotak
sarung, a sarung-plaid band divider and a small green eight-point star. No figures, no drawn calligraphy.
Run: python3 -I wisuda-santri.py [part ...]"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f6_lib import *

OUT = outdir("wisuda-santri")
PARTS = sys.argv[1:] or ["kitab", "gapura", "sarung", "band", "bintang"]
GREEN, GREEN_D, GREEN_L = "#2f6b48", "#1d4630", "#5d9a72"
MINT = "#dcebdc"
CREAM, CREAM_D = "#f3ecd8", "#d8ccaa"
WHITE = "#fbfbf6"
PAPER = "#f7f8f2"


def plaid_rgb(w, h, warp, weft, scale=1.0, angle=0.0):
    """Woven check (2/2 twill): warp/weft are lists of (hex, width) stripes; returns float RGB."""
    def seq(stripes):
        out = []
        for col, n in stripes:
            out += [hex_rgb(col)] * max(1, int(n * scale))
        return np.array(out, np.float32)
    A, B = seq(warp), seq(weft)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s_ = math.cos(angle), math.sin(angle)
    u = (xx * c + yy * s_).astype(np.int64); v = (-xx * s_ + yy * c).astype(np.int64)
    ca = A[u % len(A)]; cb = B[v % len(B)]
    tw = (((u + v) // 2) % 2)[..., None]
    rgb = ca * tw + cb * (1 - tw)
    return rgb * 0.94 + (ca + cb) / 2 * 0.06


def textured(mask, rgb, seed, rough=1.2):
    """Paint a ready-made RGB pattern through a mask as gouache (hand-cut edge, brush streaks)."""
    g = gouache_paint(mask, "#808080", seed=seed, rough=rough, streak=1.0)
    k = g[..., :3] / 0.5019
    return np.concatenate([np.clip(rgb * k, 0, 1), g[..., 3:4]], -1)


SARUNG = dict(warp=[(GREEN_D, 7), (WHITE, 3), (GREEN, 10), ("#c9b26a", 2), (GREEN, 10), (WHITE, 3), (GREEN_D, 7), ("#a7c7a8", 5)],
              weft=[(GREEN_D, 7), (WHITE, 3), (GREEN, 10), ("#c9b26a", 2), (GREEN, 10), (WHITE, 3), (GREEN_D, 7), ("#a7c7a8", 5)])


if "kitab" in PARTS:
    W, H = 640, 560
    nx = Seq(81100); rng = random.Random(3)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(320, 520, 260, 20, 18), rng, 1, 0.03)])
    art = G(art, sh, "#55705c", seed=nx(), density=0.3, edge=0.1, bloom=0, rough=3, feather=7)
    books = [(GREEN_D, 92, 520, 70, 0), (CREAM, 104, 506, 60, 8), (GREEN, 86, 516, 58, -6), (WHITE, 116, 496, 52, 10), ("#7d6b3e", 100, 504, 46, -4)]
    y = 512
    for col, x0, x1, th, dx in books:
        x0 += dx; x1 += dx
        top = y - th
        cover = shapes(W, H, [deform(rect(x0, top, x1, y), rng, 1, 0.004)], smooth=False)
        pages = shapes(W, H, [deform(rect(x0 + 14, top + 9, x1 - 6, y - 9), rng, 1, 0.004)], smooth=False)
        dark = mix(col, "#10241a", .35) if col not in (CREAM, WHITE) else "#b9ae8c"
        art = GP(art, cover, col, dark, seed=nx(), rough=1.0, streak=1.2)
        art = mul(art, shade_side(cover, 0, -6, 4), "#3a3a2a", 0.5, seed=nx())
        # page block visible on the right end + fore-edge lines
        fore = shapes(W, H, [rect(x1 - 70, top + 9, x1 - 4, y - 9)], smooth=False) * pages
        art = GP(art, fore, CREAM, CREAM_D, seed=nx(), rough=0.6, streak=0.5, pad=6)
        lines = [([(x1 - 70, yy), (x1 - 6, yy + rng.uniform(-.6, .6))], 0.9, None) for yy in np.arange(top + 13, y - 11, 3.2)]
        art = mul(art, strokes(W, H, lines) * fore, "#9c8f6a", 0.45, seed=nx())
        # cloth spine band near the left: plain, no writing
        band = shapes(W, H, [rect(x0 + 34, top + 2, x0 + 44, y - 2), rect(x0 + 52, top + 2, x0 + 56, y - 2)], smooth=False)
        art = mul(art, band * cover, "#4a3f2a" if col in (CREAM, WHITE) else "#0d1f15", 0.35, seed=nx())
        art = G(art, edge_of(cover, 1.2), "#20261d", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.5)
        y = top
    # a ribbon bookmark hanging from the middle book
    rib = strokes(W, H, [(curve([(420, 404), (428, 448), (418, 500), (426, 540)], 20), 9, (0.0, 0.0))])
    art = GP(art, rib, "#c9b26a", "#a38a44", seed=nx(), rough=0.6, pad=6)
    # peci on top: black velvet, oval crown, soft sheen
    cx, base = 318, y + 4
    peci = shapes(W, H, [[(cx - 116, base), (cx - 112, base - 40), (cx - 106, base - 78), (cx - 92, base - 90), (cx, base - 94), (cx + 92, base - 90), (cx + 106, base - 78), (cx + 112, base - 40), (cx + 116, base)]])
    art = G(art, shapes(W, H, [ellipse_pts(cx + 10, base + 2, 130, 10, 14)]), "#1e2a22", seed=nx(), density=0.4, edge=0, bloom=0, rough=2, feather=4)
    art = GP(art, peci, "#24272a", "#111315", seed=nx(), rough=1.0, streak=2.0)
    nap = gaussian_filter(np.random.default_rng(5).random((H, W)).astype(np.float32), (6, 0.6))
    nap = (nap - nap.min()) / (nap.max() - nap.min())
    art = lift(art, peci * spot(peci, cx - 50, base - 70, 90) * (0.5 + nap), "#6c7377", 0.45, seed=nx())
    topp = shapes(W, H, [ellipse_pts(cx, base - 86, 100, 9, 20)]) * peci
    art = lift(art, gaussian_filter(topp, 1.5), "#4d5357", 0.6, seed=nx())
    top_line = strokes(W, H, [([(cx - 112, base - 12), (cx + 112, base - 12)], 1.4, None)])
    art = mul(art, top_line * peci, "#000000", 0.6, seed=nx())
    preview(art, "ws-kitab", tone=PAPER)
    save(art, f"{OUT}/kitab.webp", max_w=360, quality=82)
    clear()

if "gapura" in PARTS:
    W, H = 800, 620
    nx = Seq(81300); rng = random.Random(5)
    art = blank(W, H)
    ground = shapes(W, H, [deform([(0, 560), (800, 560), (800, 620), (0, 620)], rng, 2, 0.01)])
    # mango trees behind
    for tx, r in ((150, 130), (650, 140)):
        trunk = strokes(W, H, [(curve([(tx, 570), (tx + 8, 470), (tx - 4, 380)], 20), 26, (0.0, 0.3))])
        art = GP(art, trunk, "#6f5a42", "#4a3a29", seed=nx(), rough=1.2)
        blobs = [deform(ellipse_pts(tx + rng.uniform(-r * .7, r * .7), 300 + rng.uniform(-r * .6, r * .4), r * rng.uniform(.38, .55), r * rng.uniform(.32, .45), 12), rng, 2, 0.06) for _ in range(8)]
        cm = shapes(W, H, blobs)
        art = GP(art, cm, "#5f8f67", "#3e6b4b", seed=nx(), rough=3.5, streak=1.0)
        art = mul(art, shade_side(cm, -10, -14, 12), "#1f3a2a", 0.7, seed=nx())
        dabs = [(petal_pts(tx + rng.uniform(-r, r) * .8, 300 + rng.uniform(-r, r) * .6, 26, 9, rng.uniform(-.6, .6) - math.pi / 2), ) for _ in range(40)]
        art = OV(art, shapes(W, H, [d[0] for d in dabs]) * cm, lambda m: gouache_paint(m, "#82b087", "#6c9c74", seed=nx(), rough=1))
    art = GP(art, ground, "#cfdcc6", "#b7c9ad", seed=nx(), rough=2, streak=1.2)
    # wall wings
    wall = shapes(W, H, [rect(150, 460, 300, 562), rect(500, 460, 650, 562)], smooth=False)
    art = GP(art, wall, WHITE, "#e6e8dd", seed=nx(), rough=1.0, streak=0.8)
    cap = shapes(W, H, [rect(144, 450, 306, 466), rect(494, 450, 656, 466)], smooth=False)
    art = GP(art, cap, GREEN, GREEN_D, seed=nx(), rough=0.8)
    vents = shapes(W, H, [deform(ellipse_pts(x, 506, 12, 18, 10), rng, 1, 0.02) for x in (190, 225, 260, 540, 575, 610)])
    art = GP(art, vents, "#c5d6c4", "#a9c0aa", seed=nx(), rough=0.6)
    # pillars + arch lintel
    pil = shapes(W, H, [rect(290, 300, 350, 566), rect(450, 300, 510, 566)], smooth=False)
    arch = shapes(W, H, [[(290, 300), (510, 300), (510, 400)] + [(400 + math.cos(t) * 60, 400 - math.sin(t) * 72) for t in [i / 20 * math.pi for i in range(21)]] + [(290, 400)]], smooth=False)
    body = np.maximum(pil, arch)
    art = GP(art, body, WHITE, "#eef0e6", seed=nx(), rough=1.0, streak=0.8)
    art = mul(art, shade_side(body, 8, 0, 5), "#9fae9c", 0.55, seed=nx())
    trim = strokes(W, H, [([(400 + math.cos(t) * 70, 400 - math.sin(t) * 82) for t in [i / 30 * math.pi for i in range(31)]], 7, None),
                          ([(290, 300), (510, 300)], 6, None), ([(282, 566), (358, 566)], 10, None), ([(442, 566), (518, 566)], 10, None)])
    art = GP(art, trim, GREEN, GREEN_D, seed=nx(), rough=0.6)
    # open wooden gate leaves in the arch
    leaves = shapes(W, H, [[(350, 470), (380, 478), (380, 566), (350, 566)], [(450, 470), (420, 478), (420, 566), (450, 566)]], smooth=False)
    art = GP(art, leaves, "#8a6a45", "#6a4f32", seed=nx(), rough=0.6, streak=1.4)
    slats = strokes(W, H, [([(x, 476), (x, 564)], 1.4, None) for x in (358, 366, 374, 426, 434, 442)])
    art = mul(art, slats * leaves, "#3b2a18", 0.5, seed=nx())
    # tajug caps (stepped pyramid roofs) on each pillar, small gold finial
    for px in (320, 480):
        tiers = [shapes(W, H, [[(px - 46, 300), (px + 46, 300), (px + 34, 270), (px - 34, 270)]], smooth=False),
                 shapes(W, H, [[(px - 34, 268), (px + 34, 268), (px + 22, 238), (px - 22, 238)]], smooth=False),
                 shapes(W, H, [[(px - 22, 236), (px + 22, 236), (px, 196)]], smooth=False)]
        for k, t in enumerate(tiers):
            art = GP(art, t, mix(GREEN, GREEN_L, k * 0.15), GREEN_D, seed=nx(), rough=0.8, streak=1.2)
            art = mul(art, shade_side(t, 6, 0, 3), "#0e2a1b", 0.6, seed=nx())
        fin = np.maximum(circles(W, H, [(px, 190, 6)]), strokes(W, H, [([(px, 196), (px, 176)], 3, None)]))
        art = OV(art, fin, lambda m: foil(m, "#c9a75a", seed=nx()))
    # small central tajug over the arch
    t3 = shapes(W, H, [[(350, 300), (450, 300), (432, 276), (368, 276)]], smooth=False)
    t4 = shapes(W, H, [[(368, 274), (432, 274), (400, 236)]], smooth=False)
    for t in (t3, t4):
        art = GP(art, t, GREEN, GREEN_D, seed=nx(), rough=0.8, streak=1.2)
        art = mul(art, shade_side(t, 6, 0, 3), "#0e2a1b", 0.6, seed=nx())
    fin = np.maximum(circles(W, H, [(400, 230, 6)]), strokes(W, H, [([(400, 236), (400, 214)], 3, None)]))
    art = OV(art, fin, lambda m: foil(m, "#c9a75a", seed=nx()))
    path = shapes(W, H, [[(372, 566), (428, 566), (470, 620), (330, 620)]], smooth=False)
    art = GP(art, path, "#e8e0cc", "#d6ccb2", seed=nx(), rough=1.2)
    art = G(art, edge_of(np.maximum(body, wall), 1.2), "#7d8a7a", seed=nx(), density=0.35, edge=0, bloom=0, rough=0.6)
    preview(art, "ws-gapura", tone=PAPER)
    save(art, f"{OUT}/gapura.webp", max_w=420, quality=80)
    clear()

if "sarung" in PARTS:
    W, H = 560, 340
    nx = Seq(81500); rng = random.Random(7)
    art = blank(W, H)
    sh = shapes(W, H, [deform(ellipse_pts(280, 300, 240, 16, 16), rng, 1, 0.03)])
    art = G(art, sh, "#55705c", seed=nx(), density=0.28, edge=0.1, bloom=0, rough=3, feather=6)
    # three folded layers, each a rounded slab with the check running across
    y = 296
    for k, (x0, x1, th) in enumerate(((60, 500, 62), (74, 488, 58), (86, 476, 56))):
        top = y - th
        slab = shapes(W, H, [[(x0 + 18, top), (x1 - 18, top), (x1, top + th * 0.5), (x1 - 12, y), (x0 + 12, y), (x0, top + th * 0.5)]])
        rgb = plaid_rgb(W, H, SARUNG["warp"], SARUNG["weft"], scale=1.0 + 0.1 * k, angle=0.0)
        art = over(art, textured(slab, rgb, nx()))
        fold = np.clip(1 - np.abs(np.mgrid[0:H, 0:W][0] - (top + th * 0.5)) / (th * 0.5), 0, 1)
        art = mul(art, slab * (1 - fold) ** 1.5, "#0d1f15", 0.55, seed=nx())
        art = lift(art, slab * fold ** 4, "#ffffff", 0.18, seed=nx())
        art = G(art, edge_of(slab, 1.2), "#11261a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5)
        y = top + 4
    preview(art, "ws-sarung", tone=PAPER)
    save(art, f"{OUT}/sarung.webp", max_w=300, quality=82)
    clear()

if "band" in PARTS:
    W, H = 640, 64
    nx = Seq(81700); rng = random.Random(9)
    m = shapes(W, H, [deform([(30, 14), (610, 14), (626, 32), (610, 50), (30, 50), (14, 32)], rng, 1, 0.003)], smooth=False)
    rgb = plaid_rgb(W, H, SARUNG["warp"], SARUNG["weft"], scale=0.8)
    art = over(blank(W, H), textured(m, rgb, nx(), rough=0.8))
    art = G(art, edge_of(m, 1.0), "#11261a", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.4)
    preview(art, "ws-band", tone=PAPER)
    save(art, f"{OUT}/band.webp", max_w=320, quality=84)
    clear()

if "bintang" in PARTS:
    W, H = 200, 200
    nx = Seq(81900); rng = random.Random(11)
    pts = []
    for k in range(16):
        r = 86 if k % 2 == 0 else 62
        a = k * math.pi / 8 - math.pi / 2
        pts.append((100 + math.cos(a) * r, 100 + math.sin(a) * r))
    star = shapes(W, H, [pts], smooth=False)
    art = GP(blank(W, H), star, GREEN, GREEN_D, seed=nx(), rough=1.0, streak=1.0)
    inner = circles(W, H, [(100, 100, 40)])
    art = GP(art, inner, WHITE, "#eef0e6", seed=nx(), rough=0.8)
    dot = circles(W, H, [(100, 100, 13)])
    art = OV(art, dot, lambda m: foil(m, "#c9a75a", seed=nx()))
    preview(art, "ws-bintang", tone=PAPER)
    save(art, f"{OUT}/bintang.webp", max_w=72, quality=86)
    clear()
