"""Rumi Seljuk — Anatolian Seljuk ornament, no figures, no calligraphy: star-and-cross glazed tile field (cobalt stars
with turquoise rumi rosettes, turquoise crosses), carved limestone rumi-scroll bands, a pointed portal arch, a glazed rumi
medallion and a scroll divider. Run: python3 -I rumi-seljuk.py [part ...]  parts: tile leaftest band arch medallion divider"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _q3_lib import *

OUT = outdir("rumi-seljuk")
PARTS = sys.argv[1:] or ["tile", "band", "arch", "medallion", "divider"]
TURQ, TURQ_D, TURQ_L = "#2f9e9a", "#1f7470", "#7cc9c0"
COB, COB_D = "#1f3c8c", "#13265c"
MANG = "#2b2233"
WHITE = "#f1ece0"
STONE, STONE_L, STONE_D = "#d9c7a6", "#efe3cb", "#9c8460"


def rosette(cx, cy, r, n=4, rot=0.0, flip=1):
    """n rumi leaves whirling round a centre."""
    out = []
    for k in range(n):
        a = rot + k * math.tau / n
        out.append(rumi_leaf(cx + math.cos(a) * r * 0.12, cy + math.sin(a) * r * 0.12, r * 0.86, a, flip, 1.05))
    return out


if "leaftest" in PARTS:
    W, H = 400, 200
    m = shapes(W, H, [rumi_leaf(40, 100, 140, 0.0), rumi_leaf(360, 100, 140, math.pi, 1)], smooth=False)
    art = OV(blank(W, H), m, lambda q: gouache_paint(q, COB))
    preview(art, "rs-leaf", WHITE)

if "tile" in PARTS:
    # star-and-cross field: 8-point stars on a checkerboard lattice (spacing s); the gaps between them are crosses.
    S = 512; s = 128
    nx = Seq(5100)
    rng = np.random.default_rng(7)
    art = np.zeros((S, S, 4), np.float32)
    grout = np.ones((S, S), np.float32)
    stars, centres = [], []
    for i in range(-1, S // s + 2):
        for j in range(-1, S // s + 2):
            if (i + j) % 2 == 0:
                stars.append(star8(i * s, j * s, s * 0.707 - 3, rot=0.0))
                centres.append((i * s, j * s))
    star_m = shapes(S, S, stars, smooth=False)
    big = shapes(S, S, [star8(cx, cy, s * 0.707 + 3, rot=0.0) for cx, cy in centres], smooth=False)
    cross_m = np.clip(1 - big, 0, 1)
    # grout base
    art[...] = np.concatenate([np.ones((S, S, 3), np.float32) * np.array(hex_rgb("#d6cdb8"), np.float32), np.ones((S, S, 1), np.float32)], -1)
    art = OV(art, cross_m, lambda q: gouache_paint(q, TURQ, TURQ_D, seed=nx(), rough=0.8, streak=0.6), pad=0)
    art = OV(art, star_m, lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=0.8, streak=0.6), pad=0)
    # inside each star: a white slip ring + turquoise whirling rumi rosette; crosses get a cobalt quatrefoil dot
    ring = shapes(S, S, [star8(cx, cy, s * 0.6, rot=0.0) for cx, cy in centres], smooth=False) - shapes(S, S, [star8(cx, cy, s * 0.56, rot=0.0) for cx, cy in centres], smooth=False)
    art = OV(art, np.clip(ring, 0, 1), lambda q: gouache_paint(q, WHITE, "#ddd5c2", seed=nx(), rough=0.5), pad=0)
    ros = []
    for cx, cy in centres:
        ros += rosette(cx, cy, s * 0.36, 4, rng.uniform(0, 0.3) + 0.4)
    ros_m = shapes(S, S, ros, smooth=False)
    art = OV(art, ros_m, lambda q: gouache_paint(q, TURQ_L, TURQ, seed=nx(), rough=0.6), pad=0)
    art = OV(art, circles(S, S, [(cx, cy, 6) for cx, cy in centres]), lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.3), pad=0)
    cc = [(i * s, j * s) for i in range(-1, S // s + 2) for j in range(-1, S // s + 2) if (i + j) % 2 == 1]
    quat = []
    for cx, cy in cc:
        for a in range(4):
            ang = a * math.pi / 2
            quat.append(petal_pts(cx, cy, s * 0.3, s * 0.12, ang, n=12))
    art = OV(art, shapes(S, S, quat), lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=0.6), pad=0)
    art = OV(art, circles(S, S, [(cx, cy, 5) for cx, cy in cc]), lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.3), pad=0)
    # glaze: per-tile tone drift, soft gloss, fine crackle, a few chips showing the body
    tiles = np.maximum(star_m, cross_m)
    tone = fbm(S, S, nx(), 60, 3)
    rgb = art[..., :3] * (0.9 + 0.18 * tone[..., None] * tiles[..., None] + (1 - tiles[..., None]) * 0.1)
    gloss = gaussian_filter((fbm(S, S, nx(), 26, 3) > 0.7).astype(np.float32), 4) * tiles
    rgb = rgb + gloss[..., None] * 0.12
    crack = fbm(S, S, nx(), 7, 2)
    crack = np.clip(1 - np.abs(crack - 0.5) * 40, 0, 1) * tiles
    rgb = rgb * (1 - crack[..., None] * 0.18)
    chips = (fbm(S, S, nx(), 4, 2) > 0.86).astype(np.float32) * tiles * (fbm(S, S, nx(), 40, 2) > 0.6)
    rgb = rgb * (1 - chips[..., None]) + np.array(hex_rgb("#cbbfa5"), np.float32) * chips[..., None]
    art = np.concatenate([np.clip(rgb, 0, 1), np.ones((S, S, 1), np.float32)], -1)
    save_rgb(art, f"{OUT}/tile.webp", (320, 320), quality=80)
    Image.fromarray((np.clip(art[..., :3], 0, 1) * 255).astype(np.uint8)).save(f"{PREV}/rs-tile.png")
    clear()

if "band" in PARTS:
    # vertical carved band, seamless top-bottom (period divides H); fillets at both edges
    W, H = 72, 480
    P = 160
    items, leaves = [], []
    for dy in (-H, 0, H):
        it, lv = scroll_along([(36, -40 + dy), (36, H + 40 + dy)], 10, P, 30, phase=math.tau * 40 / P, stem_w=4.6)
        items += it; leaves += lv
    motif = np.clip(strokes(W, H, items) + shapes(W, H, leaves, smooth=False), 0, 1)
    fil = np.maximum(rect(W, H, 2, 0, 8, H), rect(W, H, W - 8, 0, W - 2, H))
    motif = np.maximum(motif * rect(W, H, 11, 0, W - 11, H), fil)
    field = np.ones((H, W), np.float32)
    art = relief(field, motif, 5300, depth=1.6)
    save_rgb(art, f"{OUT}/band.webp", quality=82)
    Image.fromarray((art[..., :3] * 255).astype(np.uint8)).save(f"{PREV}/rs-band.png")
    clear()

if "arch" in PARTS:
    W, H = 680, 540
    Ro, Ri, sp = 500, 432, 520
    nx = Seq(5400)
    def arch_pts(R, c_left, c_right):
        left = [(c_left + math.cos(a) * -R, sp - math.sin(a) * R) for a in np.linspace(0, math.acos((c_left - 340) / R), 60)]
        right = [(c_right + math.cos(a) * R, sp - math.sin(a) * R) for a in np.linspace(math.acos((340 - c_right) / R), 0, 60)]
        return [(float(x), float(y)) for x, y in left + right]
    outer = arch_pts(Ro, 500, 180) + [(680, H), (0, H)]
    inner_line = arch_pts(Ri, 500, 180)
    inner = inner_line + [(612, H), (68, H)]
    o_m = poly(W, H, outer); i_m = poly(W, H, inner)
    band = np.clip(o_m - i_m, 0, 1)
    mid = arch_pts(466, 500, 180)
    items, leaves = scroll_along([(34, H + 20)] + mid + [(646, H + 20)], 10, 160, 30, phase=0.0, stem_w=4.6)
    motif = np.clip(strokes(W, H, items) + shapes(W, H, leaves, smooth=False), 0, 1)
    edge_o = np.clip(o_m - poly(W, H, arch_pts(Ro - 7, 500, 180) + [(673, H), (7, H)]), 0, 1)
    edge_i = np.clip(poly(W, H, arch_pts(Ri + 7, 500, 180) + [(605, H), (75, H)]) - i_m, 0, 1)
    motif = np.maximum(motif * band * np.clip(1 - edge_o * 3, 0, 1), np.maximum(edge_o, edge_i))
    art = relief(band, motif, nx(), depth=1.6)
    # inner: cream limestone panel with a turquoise glazed tile fillet just inside the carving
    panel = OV(blank(W, H), i_m, lambda q: gouache_paint(q, "#f1e8d4", "#e9dfc8", seed=nx(), rough=0.3, streak=0.3, density=1.0))
    art = over(panel, art)
    glz = np.clip(i_m - poly(W, H, arch_pts(Ri - 12, 500, 180) + [(600, H + 30), (80, H + 30)]), 0, 1) * (np.arange(H)[:, None] < H - 4)
    art = OV(art, glz, lambda q: gouache_paint(q, TURQ, TURQ_D, seed=nx(), rough=0.5, streak=0.5))
    dots = [(x, y, 2.6) for (x, y, a) in jw.along(arch_pts(Ri - 6, 500, 180), 16)]
    art = OV(art, circles(W, H, dots), lambda q: gouache_paint(q, COB, seed=nx(), rough=0.3))
    # small glazed knot at the apex keystone
    ks = shapes(W, H, rosette(340, 82, 34, 4, 0.5), smooth=False)
    art = OV(art, circles(W, H, [(340, 82, 32)]) * band, lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=0.5))
    art = OV(art, ks, lambda q: gouache_paint(q, TURQ_L, TURQ, seed=nx(), rough=0.4))
    art = OV(art, np.clip(circles(W, H, [(340, 82, 34)]) - circles(W, H, [(340, 82, 31)]), 0, 1), lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.3))
    preview(art, "rs-arch", "#1f3c8c", bg="#2a5a8a")
    save_full(art[:H - 8], f"{OUT}/arch.webp", quality=82)
    clear()

if "medallion" in PARTS:
    W = H = 440; c = 220
    nx = Seq(5500)
    lobes = [(c + math.cos(a) * 150, c + math.sin(a) * 150, 66) for a in np.linspace(0, math.tau, 8, endpoint=False)]
    body = np.maximum(circles(W, H, [(c, c, 170)]), circles(W, H, lobes))
    rim = np.clip(gaussian_filter(body, 0.5) - np.maximum(circles(W, H, [(c, c, 158)]), circles(W, H, [(x, y, r - 12) for x, y, r in lobes])), 0, 1)
    art = OV(blank(W, H), body, lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=1.0, streak=0.5))
    art = OV(art, rim, lambda q: gouache_paint(q, TURQ, TURQ_D, seed=nx(), rough=0.8))
    inner_ring = np.clip(circles(W, H, [(c, c, 112)]) - circles(W, H, [(c, c, 104)]), 0, 1)
    art = OV(art, inner_ring, lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.4))
    leaves = rosette(c, c, 98, 4, 0.4)
    for k in range(8):
        a = k * math.tau / 8 + 0.2
        x, y = c + math.cos(a) * 130, c + math.sin(a) * 130
        leaves.append(rumi_leaf(x, y, 46, a + math.pi / 2, 1, 1.0))
    lm = shapes(W, H, leaves, smooth=False)
    art = OV(art, lm, lambda q: gouache_paint(q, TURQ_L, TURQ, seed=nx(), rough=0.6))
    a = gaussian_filter(lm, 0.8); gy, gx = np.gradient(a)
    art = G(art, np.clip(np.hypot(gx, gy) * 3, 0, 1), MANG, seed=nx(), density=0.7, edge=0, bloom=0, rough=0.4, feather=0.4)
    art = OV(art, circles(W, H, [(c, c, 12)] + [(c + math.cos(a) * 150, c + math.sin(a) * 150, 5) for a in np.linspace(0, math.tau, 8, endpoint=False)]), lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.3))
    tone = fbm(W, H, nx(), 30, 3)
    art[..., :3] = np.clip(art[..., :3] * (0.92 + 0.14 * tone[..., None]) + gaussian_filter((fbm(W, H, nx(), 30, 2) > 0.72).astype(np.float32), 5)[..., None] * 0.1, 0, 1)
    preview(art, "rs-medallion", "#f1e8d4")
    save(art, f"{OUT}/medallion.webp", max_w=300, quality=82)
    clear()

if "divider" in PARTS:
    W, H = 480, 110
    nx = Seq(5600)
    it1, lv1 = scroll_along([(240, 55), (470, 55)], 14, 130, 36, phase=0.0, stem_w=4.5)
    it2, lv2 = scroll_along([(240, 55), (10, 55)], 14, 130, 36, phase=0.0, stem_w=4.5)
    stem = strokes(W, H, it1 + it2)
    lv = shapes(W, H, lv1 + lv2, smooth=False)
    art = OV(blank(W, H), stem, lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=0.6))
    art = OV(art, lv, lambda q: gouache_paint(q, TURQ, TURQ_D, seed=nx(), rough=0.6))
    knot = shapes(W, H, [star8(240, 55, 26, rot=0.0)], smooth=False)
    art = OV(art, knot, lambda q: gouache_paint(q, COB, COB_D, seed=nx(), rough=0.5))
    art = OV(art, circles(W, H, [(240, 55, 8)]), lambda q: gouache_paint(q, WHITE, seed=nx(), rough=0.3))
    a = gaussian_filter(np.maximum(lv, knot), 0.8); gy, gx = np.gradient(a)
    art = G(art, np.clip(np.hypot(gx, gy) * 3, 0, 1), MANG, seed=nx(), density=0.6, edge=0, bloom=0, rough=0.4, feather=0.4)
    preview(art, "rs-divider", "#f1e8d4")
    save(art, f"{OUT}/divider.webp", max_w=360, quality=82)
    clear()
