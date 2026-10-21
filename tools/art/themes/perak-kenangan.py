"""Perak Kenangan — silver/golden wedding anniversary: deckled vintage photo prints (portrait + landscape, photos go
behind the window), dusty-rose & champagne rose garland with silver eucalyptus, silver-leaf laurel wreath for the
anniversary number, silver divider, champagne striped wallpaper tile.
Run: python3 -I perak-kenangan.py [part ...]  parts: frameP frameL garland wreath divider wall"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a4_lib import *

OUT = outdir("perak-kenangan")
PARTS = sys.argv[1:] or ["frameP", "frameL", "garland", "wreath", "divider", "wall"]
EUC_A, EUC_B, EUC_D = "#b7c2bf", "#8b9a98", "#5f6e6d"
jw.LEAF_D = EUC_D


def print_frame(W, H, win, seed, name):
    """Deckled photo print: cream paper with torn edge, a crisp window (transparent), aged edges, soft shadow."""
    nx = Seq(seed)
    x0, y0, x1, y1 = win
    paper_m = deckle_mask(W, H, 16, seed=seed, amp=7.5)
    window = np.zeros((H, W), np.float32); window[y0:y1, x0:x1] = 1
    shadow = np.roll(np.roll(gaussian_filter(paper_m, 7), 6, 0), 3, 1) * 0.35
    art = rgba("#3a3430", shadow)
    rng = np.random.default_rng(seed)
    tone = np.ones((H, W, 3), np.float32) * np.array(hex_rgb("#f8f3e8"), np.float32)
    f = fbm(W, H, seed + 1, 50, 3); fine = gaussian_filter(rng.random((H, W)).astype(np.float32), 0.8)
    tone *= (0.96 + 0.05 * f + 0.03 * (fine - 0.5))[..., None]
    age = np.clip(1 - gaussian_filter(paper_m, 10) * 1.25, 0, 1) + 0.15 * fbm(W, H, seed + 5, 90, 2)
    tone = tone * (1 - age[..., None] * 0.18) + np.array(hex_rgb("#dcc7a1"), np.float32) * age[..., None] * 0.18
    # thin pressed line around the window, like an old studio print
    pl = np.zeros((H, W), np.float32); pl[y0 - 7:y1 + 7, x0 - 7:x1 + 7] = 1
    pl = np.clip(pl - np.pad(np.ones((y1 - y0 + 12, x1 - x0 + 12), np.float32), ((y0 - 6, H - y1 - 6), (x0 - 6, W - x1 - 6))), 0, 1)
    tone *= (1 - gaussian_filter(pl, 0.6) * 0.12)[..., None]
    sheet = np.concatenate([np.clip(tone, 0, 1), paper_m[..., None]], -1)
    art = over(art, sheet)
    # inner shadow at the window edge (photo sits slightly below the paper)
    inner = np.clip(gaussian_filter(1 - window, 2.5) - (1 - window), 0, 1) * window
    art = over(art, rgba("#2a2420", inner * 0.6))
    art[..., 3] *= 1 - window * (1 - inner * 0.6)
    # silver photo corners
    cs = 26
    corners = []
    for (cx, cy, sx, sy) in [(x0 - 4, y0 - 4, 1, 1), (x1 + 4, y0 - 4, -1, 1), (x0 - 4, y1 + 4, 1, -1), (x1 + 4, y1 + 4, -1, -1)]:
        corners.append([(cx, cy), (cx + sx * cs, cy), (cx, cy + sy * cs)])
    cm = shapes(W, H, corners, smooth=False)
    art = SV(art, cm, "#c7ccd2", seed=nx(), emboss=0.8, sparkle=0.15)
    art[..., 3] = np.where(window > 0.5, art[..., 3] * (cm > 0.1) + inner * 0.6 * (cm <= 0.1), art[..., 3])
    preview(art, name, tone="#e9e4dc")
    return art


if "frameP" in PARTS:
    W, H = 380, 480
    art = print_frame(W, H, (34, 34, 346, 400), 50100, "pk-frameP")
    save_full(art, f"{OUT}/frameP.webp", quality=82)
    clear()

if "frameL" in PARTS:
    W, H = 480, 400
    art = print_frame(W, H, (34, 34, 446, 322), 50200, "pk-frameL")
    save_full(art, f"{OUT}/frameL.webp", quality=82)
    clear()


def euc(art, W, H, pts, rng, nx, r=14):
    """Silver-dollar eucalyptus stem: round leaves alternating along a stem."""
    art = G(art, strokes(W, H, [(pts, 2.2, (0.05, 0.3))]), EUC_B, EUC_D, seed=nx(), density=0.6, edge=0.3, bloom=0, rough=1, feather=0.6)
    polys = []
    for j in range(3, len(pts) - 1, 3):
        a, b = pts[j - 1], pts[j + 1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0]) + (1.3 if (j // 3) % 2 else -1.3)
        rr = r * (0.6 + 0.4 * (1 - j / len(pts))) * rng.uniform(0.85, 1.1)
        cx, cy = pts[j][0] + math.cos(ang) * rr * 0.9, pts[j][1] + math.sin(ang) * rr * 0.9
        polys.append(deform(ellipse_pts(cx, cy, rr, rr * 0.9, 10), rng, 1, 0.06))
    m = shapes(W, H, polys)
    return G(art, m, EUC_A, EUC_B, seed=nx(), density=0.62, edge=0.6, bloom=0.4, rough=3, holes=0.03)


def p_rose(art, W, H, x, y, r, rng, nx, kind, area):
    if kind == 0:
        return rose(art, W, H, x, y, r, rng, nx, "#f3dcd6", "#d9a7a3", "#a86f73", area)
    return rose(art, W, H, x, y, r, rng, nx, "#f8efe6", "#e8d2bd", "#b8957f", area)


if "garland" in PARTS:
    W, H = 800, 300
    nx = Seq(50300); rng = random.Random(9)
    back = blank(W, H); flowers = blank(W, H); area = np.zeros((H, W), np.float32)
    # swag: eucalyptus along a shallow catenary, roses clustered at the ends and the centre
    sw = catenary(-20, 40, 820, 40, 150, 120)
    for off, rr in [(0, 22), (-16, 15)]:
        back = euc(back, W, H, [(x, y + off) for x, y in sw[::2]], rng, nx, rr)
    for pts in [curve([(400, 190), (330, 230), (260, 250)], 20), curve([(400, 190), (470, 232), (550, 246)], 20),
                curve([(60, 60), (40, 130), (70, 200)], 16), curve([(740, 60), (760, 130), (730, 200)], 16)]:
        back = sprig_l = back
        for j in range(2, len(pts) - 1, 3):
            a, b = pts[j - 1], pts[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            for sd in (-1, 1):
                back = leaf(back, W, H, pts[j][0], pts[j][1], 34, ang + sd * 0.7, rng, nx, c=("#a9b49b", "#76866c"))
    for (x, y, r, k) in [(400, 182, 52, 0), (348, 166, 34, 1), (454, 168, 36, 1), (400, 132, 26, 1), (60, 46, 40, 0), (110, 70, 26, 1), (740, 46, 40, 0), (690, 72, 26, 1),
                       (200, 148, 30, 0), (236, 162, 20, 1), (600, 148, 30, 0), (564, 162, 20, 1)]:
        flowers = p_rose(flowers, W, H, x, y, r, rng, nx, k, area)
    back = knockout(back, area, amount=0.95, grow=4)
    art = glaze(back, flowers)
    art = draw_pearls(art, string_pearls(catenary(300, 196, 500, 196, 50, 60), 4.2, seed=3), seed=70, base="#eef0f2", shade="#8e95a0")
    art = dots(art, W, H, rng, nx, 400, 200, 120, 40, 14, "#cfa3a0")
    preview(art, "pk-garland", tone="#f2ede4")
    save(art, f"{OUT}/garland.webp", max_w=780, quality=80)
    clear()

if "wreath" in PARTS:
    W = H = 440
    cx = cy = 220
    nx = Seq(50400); rng = random.Random(13)
    items, leaves = [], []
    for side in (-1, 1):
        a0, a1 = math.pi / 2 + side * 0.25, math.pi / 2 + side * 2.75
        stem = [(cx + math.cos(a0 + (a1 - a0) * t) * 176, cy + math.sin(a0 + (a1 - a0) * t) * 176) for t in [i / 59 for i in range(60)]]
        items.append((stem, 4, (0.05, 0.4)))
        for j in range(2, 58, 5):
            a, b = stem[j - 1], stem[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            L = 50 * (1 - j / 120)
            leaves.append(petal_pts(stem[j][0], stem[j][1], L, L * 0.22, ang + 0.85, n=12))
            leaves.append(petal_pts(stem[j][0], stem[j][1], L, L * 0.22, ang - 0.85, n=12))
    m = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    art = SV(blank(W, H), m, "#c7ccd2", seed=nx(), emboss=0.6, sparkle=0.12)
    berries = circles(W, H, [(cx + math.cos(a) * 196, cy + math.sin(a) * 196, 4.5) for a in [math.pi / 2 + sd * (0.6 + 0.5 * k) for sd in (-1, 1) for k in range(4)]])
    art = FO(art, berries, "#d9bf8a", seed=nx(), emboss=0.6)
    # champagne ribbon tie at the bottom
    bow = shapes(W, H, [[(cx, cy + 176), (cx - 34, cy + 156), (cx - 40, cy + 190)], [(cx, cy + 176), (cx + 34, cy + 156), (cx + 40, cy + 190)],
                        [(cx - 4, cy + 178), (cx - 22, cy + 222), (cx - 10, cy + 224)], [(cx + 4, cy + 178), (cx + 22, cy + 222), (cx + 10, cy + 224)]], smooth=True)
    art = FO(art, bow, "#d9bf8a", seed=nx(), emboss=0.7, sparkle=0.1)
    preview(art, "pk-wreath", tone="#f2ede4")
    save(art, f"{OUT}/wreath.webp", max_w=300, quality=84)

if "divider" in PARTS:
    W, H = 460, 70
    nx = Seq(50500); cx, cy = 230, 35
    items, leaves = [], []
    for sd in (-1, 1):
        stem = curve([(cx + sd * 16, cy), (cx + sd * 90, cy - 6), (cx + sd * 200, cy + 2)], 40)
        items.append((stem, 2.2, (0.0, 0.8)))
        for j in range(3, 22, 4):
            a, b = stem[j - 1], stem[j + 1]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            L = 18 * (1 - j / 34)
            leaves.append(petal_pts(stem[j][0], stem[j][1], L, L * 0.34, ang + sd * 0.0 - 0.6, n=10))
            leaves.append(petal_pts(stem[j][0], stem[j][1], L, L * 0.34, ang + 0.6, n=10))
    m = np.maximum(strokes(W, H, items), shapes(W, H, leaves))
    art = SV(blank(W, H), m, "#c7ccd2", seed=nx(), emboss=0.7, sparkle=0.12)
    rng = random.Random(4); area = np.zeros((H, W), np.float32)
    art = p_rose(art, W, H, cx, cy, 16, rng, nx, 0, area)
    preview(art, "pk-divider", tone="#f2ede4")
    save(art, f"{OUT}/divider.webp", max_w=320, quality=86)

if "wall" in PARTS:
    n = 384
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    stripe = 0.5 + 0.5 * np.sin(2 * math.pi * xx / n * 12)
    f = wrap_noise(n, n, 3, 30); fine = wrap_noise(n, n, 5, 0.9)
    base = lerp3("#f3eee6", "#ece5da", f)
    base *= (1 + 0.018 * (stripe[..., None] - 0.5) + 0.03 * (fine[..., None] - 0.5))
    save_rgb(np.concatenate([base, np.ones((n, n, 1), np.float32)], -1), f"{OUT}/wall.webp", quality=72)

kb(OUT)
