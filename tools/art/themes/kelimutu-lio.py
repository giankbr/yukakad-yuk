"""Kelimutu Lio — the three crater lakes of Kelimutu at dawn above a sea of clouds, and Lio ikat (dark ground,
rust-red and ochre lozenges). Run: python3 -I kelimutu-lio.py [part ...]
parts: scene ikat motif lakes clouds. Assets -> public/themes/art/kelimutu-lio/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _l3_lib import *

OUT = outdir("kelimutu-lio")
PARTS = sys.argv[1:] or ["scene", "ikat", "motif", "lakes", "clouds"]
NIGHT, DUSK = "#151834", "#2b2d58"
TURQ, TURQ_L = "#2fa79b", "#8fe0cc"
MOSS, MOSS_D = "#4d5a2c", "#2a3418"
OXB, OXB_D = "#4a1814", "#1c0b09"
RUST, OCHRE, IKAT_BG = "#a9381f", "#d39a3c", "#1d1512"


def ikat_bleed(mask, seed, amt=3.0):
    """Ikat look: warp threads shift up/down per column and bleed vertically; fine thread streaks."""
    h, w = mask.shape
    rng = np.random.default_rng(seed)
    shift = gaussian_filter(rng.normal(0, 1, w).astype(np.float32), 1.2, mode="wrap")
    shift = shift / (np.abs(shift).max() + 1e-6) * amt
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    m = map_coordinates(mask, [yy + shift[None, :], xx], order=1, mode="wrap")
    m = gaussian_filter(m, (1.6, 0.4), mode="wrap")
    streak = gaussian_filter(rng.random((h, w)).astype(np.float32), (6, 0.35), mode="wrap")
    streak = (streak - streak.min()) / (streak.max() - streak.min() + 1e-6)
    return np.clip(m * (0.78 + 0.32 * streak), 0, 1)


def cloud_rows(art, W, H, rows, nx, rng, lit="#f8d8c0", mid="#d9a8aa", shade="#8f6b8a"):
    """Rows of cumulus: shade wash for the whole puff, then warm light on the sun side (upper right)."""
    for (y, r, step) in rows:
        items = []
        x = -40 + rng.uniform(0, step * 0.5)
        while x < W + 60:
            rr = r * rng.uniform(0.55, 1.4)
            items.append((x, y - rr * 0.4 + rng.uniform(-r * 0.35, r * 0.35), rr)); x += step * rng.uniform(0.45, 1.05)
            if rng.random() < 0.5:
                items.append((x - step * 0.3, y - rr * 0.9, rr * rng.uniform(0.4, 0.7)))
        m = np.maximum(circles(W, H, items), shapes(W, H, [[(-40, y), (W + 40, y), (W + 40, y + 160), (-40, y + 160)]], smooth=False))
        art = G(art, m, shade, mid, seed=nx(), density=0.9, edge=0.3, bloom=0.45, rough=5, feather=2.5)
        shifted = np.roll(np.roll(m, 14, 0), -10, 1)
        litm = np.clip(m - shifted, 0, 1)
        litm = gaussian_filter(litm, 3) * m
        art = G(art, np.clip(litm * 1.6, 0, 1), lit, seed=nx(), density=0.9, edge=0.15, bloom=0.3, rough=4, feather=2)
        clear()
    return art


def lozenge(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


if "scene" in PARTS:
    W, H = 780, 1480
    nx = Seq(31000)
    rng = random.Random(4)
    sky = painted_sky(W, H, [(0, NIGHT), (0.2, "#1c1f44"), (0.33, DUSK), (0.42, "#5c4370"), (0.48, "#a35e6c"), (0.53, "#e2906a"), (0.57, "#f5c88a"), (1, "#f5c88a")], seed=nx(), streak=0.9)
    art = sky
    # stars in the upper sky
    st = circles(W, H, [(rng.uniform(10, W - 10), rng.uniform(10, 420) ** 1.0, rng.choice([0.9, 1.1, 1.4, 1.8])) for _ in range(90)])
    art = soft(art, st, "#f4ead2", alpha=0.75, pad=4)
    art = soft(art, circles(W, H, [(612, 210, 3.2)]), "#fff6dd", alpha=1, pad=6)
    art = soft(art, circles(W, H, [(612, 210, 14)]), "#fff0d0", alpha=0.25, blur=6, pad=6)
    clear()
    # sun glow just under the horizon, right of centre
    art = soft(art, circles(W, H, [(560, 840, 260)]), "#ffd9a0", alpha=0.32, blur=70, pad=10)
    # distant peaks through the clouds (Flores ranges)
    far = shapes(W, H, [[(-20, 840), (60, 800), (130, 770), (190, 790), (260, 760), (320, 795), (380, 812), (430, 800), (-20, 860)],
                         [(470, 830), (540, 790), (600, 740), (650, 726), (700, 748), (760, 780), (800, 800), (800, 860), (470, 860)]])
    art = G(art, far, "#5a4a78", "#7a5f86", seed=nx(), density=0.8, edge=0.3, bloom=0.2, rough=3, feather=1.5)
    # sea of clouds: rows of cumulus puffs, lit warm from the low sun (upper right), lilac in shadow
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = cloud_rows(art, W, H, [(820, 30, 64), (870, 38, 78), (930, 46, 92)], nx, rng)
    # the mountain massif: dark rim with warm-lit crest, rising from the clouds
    rim = [(-20, 960), (60, 934), (150, 906), (250, 888), (330, 880), (420, 884), (520, 874), (610, 884), (700, 902), (800, 930), (800, H), (-20, H)]
    rim_m = shapes(W, H, [rim])
    art = GP(art, rim_m, "#3a2a35", "#24181f", seed=nx(), rough=2.2, streak=1.0, pad=12)
    crest = rim_m * np.clip(1 - (yy - 878) / 50.0, 0, 1)
    art = G(art, crest, "#c9775a", seed=nx(), density=0.55, edge=0.3, bloom=0.2, rough=3)
    art = G(art, rim_m * jw.hatch(W, H, 0.25, 14, 0.1, 5) * np.clip((yy - 890) / 200, 0, 1), "#140c10", seed=nx(), density=0.35, edge=0, bloom=0, rough=2)
    clear()
    # crater bowls: the far inner wall is lit ochre/rose and streaked by erosion gullies
    for i, (cx, cy, rx, ry) in enumerate([(300, 1060, 280, 112), (598, 1000, 176, 70)]):
        bowl = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 18), random.Random(i + 3), 2, 0.04)])
        art = G(art, bowl, "#5b3a34", "#3e2a2a", seed=nx(), density=0.95, edge=0.5, bloom=0.2, rough=3)
        wall = bowl * np.clip(1 - (yy - (cy - ry)) / (ry * 1.25), 0, 1) ** 0.7
        art = soft(art, wall, "#a26c5a", alpha=0.85, blur=1.5)
        art = G(art, bowl * np.clip(1 - (yy - (cy - ry)) / (ry * 0.45), 0, 1), "#6a4038", seed=nx(), density=0.7, edge=0.2, bloom=0.3, rough=3)
        art = G(art, wall * 0.7, "#d9a080", "#c28a78", seed=nx(), density=0.7, edge=0.2, bloom=0.5, rough=3)
        gul = strokes(W, H, [(curve([(gx, cy - ry * 0.95 + abs(gx - cx) / rx * ry * 0.5), (gx + rng.uniform(-6, 6), cy - ry * 0.2), (gx + rng.uniform(-10, 10), cy + ry * 0.3)], 10), rng.uniform(2, 5), (0.1, 0.6))
                             for gx in sorted(rng.uniform(cx - rx * 0.85, cx + rx * 0.85) for _ in range(int(rx / 11)))])
        art = G(art, gul * bowl, "#5a3430", seed=nx(), density=0.6, edge=0.2, bloom=0, rough=1.5)
        clear()
    # the three lakes: Tiwu Nuwa Muri Koo Fai (turquoise) and Tiwu Ata Polo (moss/brown) side by side,
    # Tiwu Ata Mbupu (near-black red) apart
    for k, (cx, cy, rx, ry, base, base2, deep, lit) in enumerate([
            (176, 1096, 134, 50, "#3aa597", "#4fb8a8", "#1d6f6a", "#9ad8c8"),
            (414, 1094, 106, 44, "#4f5a2e", "#5e5a2a", "#262e16", "#8e8a5c"),
            (598, 1022, 124, 40, "#4a1a16", "#3a1310", "#160806", "#8a4a40")]):
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 16), random.Random(11 + k), 2, 0.035)])
        art = G(art, m, base, base2, seed=nx(), density=1.0, edge=0.55, bloom=0.25, rough=2, feather=1.0, mottle=0.2)
        art = G(art, m, base, seed=nx(), density=0.9, edge=0.2, bloom=0.4, rough=2, feather=1.0)
        art = G(art, m * np.clip((yy - cy) / ry, 0, 1), deep, seed=nx(), density=0.75, edge=0.3, bloom=0.2, rough=2)
        art = G(art, m * np.clip(1 - (yy - (cy - ry)) / (ry * 0.8), 0, 1), lit, seed=nx(), density=0.45, edge=0.1, bloom=0.3, rough=2)
        rip = strokes(W, H, [([(cx - rx * 0.6 + j * 23 % (rx * 0.9), cy - ry * 0.35 + j * 9), (cx - rx * 0.6 + j * 23 % (rx * 0.9) + rx * 0.35, cy - ry * 0.35 + j * 9)], 1.6, (0.4, 0.4)) for j in range(6)])
        art = soft(art, rip * m, "#ffe2c0", alpha=0.35, pad=4)
        clear()
    # foreground rim (front lip of the craters) with sparse shrubs, fading to the ikat ground
    fg = shapes(W, H, [[(-20, 1140), (120, 1150), (260, 1162), (420, 1152), (520, 1132), (600, 1062), (700, 1058), (800, 1070), (800, H), (-20, H)]])
    art = GP(art, fg, "#2c2026", "#1d1512", seed=nx(), rough=2, streak=1.0, pad=12)
    lip = fg * np.clip(1 - (yy - 1060) / 30.0, 0, 1) * (yy > 1050)
    art = G(art, fg * np.clip(1 - np.abs(yy - 1150) / 22.0, 0, 1) + lip, "#7a4c3c", seed=nx(), density=0.4, edge=0.2, bloom=0.2, rough=3)
    shrubs = circles(W, H, [(rng.uniform(0, W), rng.uniform(1150, 1240), rng.uniform(4, 11)) for _ in range(60)])
    art = G(art, shrubs, "#33402a", "#4a5233", seed=nx(), density=0.7, edge=0.35, bloom=0.2, rough=3)
    art = soft(art, np.clip((yy - 1210) / 200, 0, 1) * np.ones_like(yy), IKAT_BG, alpha=1, pad=0)
    clear()
    prev(art, "kl-scene", bg=None)
    save_rgb(art, f"{OUT}/scene.webp", size=(640, 1214), quality=78)

if "ikat" in PARTS:
    # seamless Lio ikat field (both directions): bands of lozenge chains with hooks, rust and ochre on near-black
    W, H = 320, 320
    nx = Seq(32000)
    def wrapdraw(polys):
        out = []
        for p in polys:
            for dx in (-W, 0, W):
                out.append([(x + dx, y) for x, y in p])
        return out
    red, och, cream = [], [], []
    for row, cy in enumerate((80, 240)):
        for i in range(4):
            cx = i * 80 + (40 if row else 0)
            red.append(lozenge(cx, cy, 34, 52))
            och.append(lozenge(cx, cy, 20, 32))
            red.append(lozenge(cx, cy, 8, 13))
            for s in (-1, 1):  # hooks off the lozenge flanks
                och.append([(cx + s * 34, cy), (cx + s * 46, cy - 10), (cx + s * 52, cy - 4), (cx + s * 44, cy + 6)])
        # thin stripes between bands
    stripes = [[(0, y), (W, y), (W, y + h), (0, y + h)] for y, h in ((0, 6), (152, 4), (164, 4), (314, 6))]
    stripes2 = [[(0, y), (W, y), (W, y + 2), (0, y + 2)] for y in (12, 146, 172, 306)]
    dots = [(x, y, 3) for x in range(20, W, 40) for y in (160,)]
    mr = shapes(W, H, wrapdraw(red), smooth=False)
    mo = shapes(W, H, wrapdraw(och), smooth=False)
    ms = shapes(W, H, stripes, smooth=False)
    ms2 = shapes(W, H, stripes2, smooth=False)
    md = circles(W, H, dots)
    rgb = np.ones((H, W, 3), np.float32) * np.array(hex_rgb(IKAT_BG), np.float32)
    v = wrap_noise(W, H, 3, 1.0) * 0.5 + wrap_noise(W, H, 4, 22) * 0.5
    thread = wrap_noise(W, H, 9, 0.5)
    rgb *= (0.86 + 0.24 * v)[..., None] * (0.92 + 0.12 * thread)[..., None]
    def lay(rgb, m, col, seed, a=1.0):
        mm = ikat_bleed(np.clip(m, 0, 1), seed) * a
        c = np.array(hex_rgb(col), np.float32) * (0.85 + 0.25 * wrap_noise(W, H, seed, 8))[..., None]
        return rgb * (1 - mm[..., None]) + c * mm[..., None]
    lay_r = np.clip(mr - mo, 0, 1)
    rgb = lay(rgb, np.maximum(lay_r, ms), RUST, nx())
    rgb = lay(rgb, np.maximum(mo * (1 - shapes(W, H, wrapdraw([lozenge(i * 80 + (40 if r else 0), cy, 8, 13) for r, cy in enumerate((80, 240)) for i in range(4)]), smooth=False)), ms2), OCHRE, nx())
    rgb = lay(rgb, md, "#e8d2a6", nx(), 0.9)
    arr = np.concatenate([np.clip(rgb, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    prev(arr, "kl-ikat", bg="#000000")
    save_full(arr, f"{OUT}/ikat.webp", size=(240, 240), quality=76)

if "motif" in PARTS:
    # one ikat lozenge-star (emblem/node), transparent
    W, H = 280, 300
    nx = Seq(33000)
    cx, cy = 140, 150
    outer = shapes(W, H, [lozenge(cx, cy, 96, 110)], smooth=False)
    mid = shapes(W, H, [lozenge(cx, cy, 64, 74)], smooth=False)
    inner = shapes(W, H, [lozenge(cx, cy, 30, 36)], smooth=False)
    hooks = shapes(W, H, [[(cx + s * 90, cy - 6), (cx + s * 108, cy - 26), (cx + s * 124, cy - 18), (cx + s * 110, cy - 4), (cx + s * 92, cy + 8)] for s in (-1, 1)] +
                   [[(cx - 6 * s, cy + s * 104), (cx - 24 * s, cy + s * 124), (cx - 14 * s, cy + s * 140), (cx + 2 * s, cy + s * 124), (cx + 8 * s, cy + s * 106)] for s in (-1, 1)], smooth=False)
    def lay(arr, m, col, seed):
        mm = np.clip(ikat_bleed(np.clip(m, 0, 1), seed, 2.0), 0, 1)
        return over(arr, flat(mm, col) * np.array([1, 1, 1, 1], np.float32))
    art = blank(W, H)
    art = lay(art, np.maximum(outer, hooks), IKAT_BG, nx())
    art = lay(art, np.clip(outer - shapes(W, H, [lozenge(cx, cy, 84, 97)], smooth=False), 0, 1), RUST, nx())
    art = lay(art, np.clip(mid - shapes(W, H, [lozenge(cx, cy, 50, 58)], smooth=False), 0, 1), OCHRE, nx())
    art = lay(art, inner, RUST, nx())
    art = lay(art, shapes(W, H, [lozenge(cx, cy, 10, 12)], smooth=False), "#e8d2a6", nx())
    art = lay(art, hooks, OCHRE, nx())
    prev(art, "kl-motif", bg="#f1e6d2")
    save(art, f"{OUT}/motif.webp", max_w=120, quality=84)

if "lakes" in PARTS:
    # divider: the three lakes in miniature, watercolour on paper
    W, H = 640, 150
    nx = Seq(34000)
    art = blank(W, H)
    rimm = shapes(W, H, [deform(ellipse_pts(250, 80, 210, 52, 16), random.Random(2), 2, 0.05), deform(ellipse_pts(500, 70, 118, 40, 14), random.Random(3), 2, 0.05)])
    art = G(art, rimm, "#a77a5a", "#8b5d45", seed=nx(), density=0.6, edge=0.6, bloom=0.3, rough=4)
    art = G(art, rimm * jw.hatch(W, H, 1.45, 7, 0.15, 3), "#5a3b30", seed=nx(), density=0.45, edge=0, bloom=0, rough=1)
    for (cx, cy, rx, ry, a, b, s) in [(170, 84, 110, 34, TURQ, "#56c6b4", 1), (350, 84, 80, 30, MOSS, "#6a6230", 2), (500, 72, 88, 26, OXB, "#2a0f0c", 3)]:
        m = shapes(W, H, [deform(ellipse_pts(cx, cy, rx, ry, 14), random.Random(s + 20), 2, 0.04)])
        art = G(art, m, a, b, seed=nx(), density=0.95, edge=0.7, bloom=0.3, rough=3)
    prev(art, "kl-lakes", bg=None)
    save(art, f"{OUT}/lakes.webp", max_w=320, quality=84)

if "clouds" in PARTS:
    # sea-of-clouds strip (transparent) for countdown/closing bottoms
    W, H = 900, 300
    nx = Seq(35000)
    rng = random.Random(8)
    art = blank(W, H)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    art = cloud_rows(art, W, H, [(130, 46, 90), (190, 52, 100), (250, 56, 110)], nx, rng)
    prev(art, "kl-clouds", bg="#1d1512")
    save(art, f"{OUT}/clouds.webp", max_w=640, quality=78)
