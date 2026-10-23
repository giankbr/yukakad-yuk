"""Dieng Telaga — watercolour of the Dieng plateau on a cold morning: Sindoro's cone far off, a thick mist bank, the
turquoise-green Telaga Warna ringed by dark cemara forest with a sulphur steam vent on its shore, and terraced potato and
cabbage slopes in the foreground. Also a carica (mountain papaya) sprig divider, a single carica fruit, a rising steam wisp
and a terraced-slope band.
Run: python3 -I dieng-telaga.py [part ...]   parts: scene terrace carica fruit steam
Assets -> public/themes/art/dieng-telaga/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _o2_lib import *  # noqa

OUT = outdir("dieng-telaga")
PARTS = sys.argv[1:] or ["scene", "terrace", "carica", "fruit", "steam"]

TEAL_L, TEAL, TEAL_D = "#8fd3c4", "#3e9f95", "#1f5c5a"
FOREST, FOREST_D = "#3d5a45", "#22362c"
SOIL, SOIL_D = "#8a6448", "#5b3f2e"
CABBAGE, CABBAGE_D = "#8fb9a0", "#5f8f7a"
POTATO, POTATO_D = "#5f8a45", "#3e6532"
MIST = "#f4f5f1"


def mist_bank(W, H, bands, nx, rng, col=MIST, art=None):
    art = blank(W, H) if art is None else art
    for y, th, x0, x1, dens in bands:
        blobs = []
        x = x0
        while x < x1:
            r = th * rng.uniform(1.6, 3.0)
            blobs.append((x, y + rng.uniform(-0.35, 0.35) * th, r, th * rng.uniform(0.5, 0.85), rng.uniform(-4, 4)))
            x += r * 0.85
        m = displace(ellipses(W, H, blobs), nx(), th * 0.4, max(12, th))
        art = G(art, m, col, mix_hex(col, "#dfe6e4", 0.6), seed=nx(), density=dens, edge=0.04, bloom=0.45, rough=th * 0.3,
                feather=th * 0.4, gran=0.02, pad=int(th * 2))
    return art


def cemara_line(W, H, base_fn, x0, x1, rng, hmin, hmax, step=(6, 13), wr=(0.2, 0.32)):
    """Ragged silhouette of cemara gunung / pine crowns along a shoreline: narrow spires with drooping tiers."""
    polys = []
    x = x0
    while x < x1:
        by = base_fn(x)
        h = rng.uniform(hmin, hmax)
        w = h * rng.uniform(*wr)
        pts = [(x - w, by + 4)]
        tiers = rng.randint(4, 6) if h < 60 else rng.randint(8, 11)
        for k in range(tiers):
            t = k / tiers
            yy = by - h * t
            ww = w * (1 - t) * rng.uniform(0.9, 1.15)
            pts.append((x - ww, yy)); pts.append((x - ww * 0.45, yy - h / tiers * 0.35))
        pts.append((x + rng.uniform(-1, 1), by - h))
        for k in range(tiers - 1, -1, -1):
            t = k / tiers
            yy = by - h * t
            ww = w * (1 - t) * rng.uniform(0.9, 1.15)
            pts.append((x + ww * 0.45, yy - h / tiers * 0.35)); pts.append((x + ww, yy))
        pts.append((x + w, by + 4))
        polys.append(pts)
        x += rng.uniform(*step)
    return polys


def terraces(W, H, nx, rng, top, bottom, cx, bow, n, art=None, lit=1.0, tilt=0.12):
    """Curved terraces stepping down a slope (contours sag like a hillside bowl and tilt with the slope). Each band is a crop
    (cabbage rosettes on bare earth, bushy potato rows, or freshly hoed soil) with its earth riser under the lip."""
    art = blank(W, H) if art is None else art
    xs = np.arange(-20, W + 24, 6, dtype=np.float32)
    ys_list = []
    acc = 0.0
    weights = [rng.uniform(0.7, 1.35) for _ in range(n)]
    tot = sum(weights)
    for k in range(n + 1):
        t = acc / tot
        y0 = top + (bottom - top) * (t ** 1.15)
        b = bow * (0.5 + 0.9 * t) * rng.uniform(0.8, 1.2)
        ys = y0 - b * ((xs - cx) / W) ** 2 * 3 + tilt * (xs - cx) * (0.6 + t) + np.sin(xs / W * rng.uniform(3, 6) + k * 1.3) * (3 + 7 * t)
        if k == n and bottom >= H:
            ys = np.maximum(ys, H + 30)
        ys_list.append(ys)
        if k < n:
            acc += weights[k]
    crops = ["cab", "pot", "soil", "pot", "cab", "pot", "cab", "soil", "pot", "cab", "pot", "pot"]
    for k in range(n):
        ya, yb = ys_list[k], ys_list[k + 1]
        th = float(np.mean(yb - ya))
        band = poly(W, H, list(zip(xs.tolist(), ya.tolist())) + list(zip(xs[::-1].tolist(), yb[::-1].tolist())), smooth=False)
        band = displace(band, nx(), 1.5, 14)
        crop = crops[(k + 3) % len(crops)]
        base = {"cab": ("#9a7a58", "#8a6a4c"), "pot": ("#7a9a52", "#8cab5c"), "soil": ("#a77d5c", SOIL)}[crop]
        art = G(art, band, base[0], base[1], seed=nx(), density=0.95, edge=0.35, bloom=0.3, rough=1.5, feather=0.9, gran=0.4)
        rz = max(3.0, th * 0.2)
        riser = poly(W, H, list(zip(xs.tolist(), (yb - rz).tolist())) + list(zip(xs[::-1].tolist(), (yb[::-1] + 1).tolist())))
        riser = displace(riser, nx(), 1.2, 10)
        art = G(art, riser, SOIL, SOIL_D, seed=nx(), density=0.9, edge=0.4, rough=1.0, feather=0.6, gran=0.5)
        rows = max(2, int(th / 10))
        if crop == "cab":
            dots = []
            for r in range(rows):
                f = (r + 0.6) / (rows + 0.3)
                yrow = ya + (yb - rz - ya) * f
                x = rng.uniform(-10, 0)
                sz = 1.4 + th * 0.07
                while x < W + 10:
                    yy = float(np.interp(x, xs, yrow)) + rng.uniform(-1, 1)
                    if rng.random() > 0.06:
                        dots.append((x, yy, sz * rng.uniform(1.3, 2.0), sz * rng.uniform(0.9, 1.3), rng.uniform(-15, 15)))
                    x += sz * rng.uniform(3.4, 5.2)
            dm = displace(ellipses(W, H, dots), nx(), 0.8, 4) * band
            art = G(art, dm, "#a8cdb8", "#78a893", seed=nx(), density=0.95, edge=0.6, rough=0.6, feather=0.5)
            hl = ellipses(W, H, [(x - rx * 0.25, y - ry * 0.3, rx * 0.4, ry * 0.35, r0) for x, y, rx, ry, r0 in dots if rng.random() < 0.8]) * band
            art = G(art, hl, "#e8f2e4", seed=nx(), density=0.55 * lit, edge=0.1, rough=0.4, feather=0.6)
        elif crop == "pot":
            dabs = []
            sz0 = 1.6 + th * 0.06
            rows = max(2, int(th / (sz0 * 2.8)))
            for r in range(rows):
                f = (r + 0.55) / (rows + 0.2)
                yrow = ya + (yb - rz - ya) * f
                x = rng.uniform(-12, 0)
                while x < W + 10:
                    sz = sz0 * rng.uniform(0.7, 1.25)
                    yy = float(np.interp(x, xs, yrow))
                    dabs.append((x, yy, sz * 1.5, sz, rng.uniform(-30, 30)))
                    x += sz * rng.uniform(2.6, 3.8)
            pm = displace(ellipses(W, H, dabs), nx(), 1.2, 5) * band
            art = G(art, pm, "#2e4f27", "#3c6a30", seed=nx(), density=0.85, edge=0.45, bloom=0.3, rough=0.8, feather=0.5)
            fl = circles(W, H, [(x + rng.uniform(-2, 2), y - ry, rng.uniform(0.7, 1.5) * (0.7 + th / 60)) for x, y, rx, ry, _ in dabs if rng.random() < 0.06]) * band
            art = G(art, fl, "#f6f2fa", "#e5daf0", seed=nx(), density=0.85, edge=0.1, rough=0.3, feather=0.4)
        else:
            items = []
            for r in range(rows + 1):
                f = (r + 0.5) / (rows + 1)
                yrow = ya + (yb - rz - ya) * f
                items.append((list(zip(xs.tolist(), (yrow + rng.uniform(-1, 1)).tolist())), 0.8 + th * 0.05, (0.0, 0.0)))
            art = G(art, displace(strokes(W, H, items), nx(), 1.5, 12) * band, "#6e4a35", seed=nx(), density=0.45, edge=0.2, rough=1, feather=0.6)
        lip = strokes(W, H, [(list(zip(xs.tolist(), (ya + 1.5).tolist())), 1.4 + th * 0.05, (0.0, 0.0))]) * band
        art = G(art, lip, "#f1e6c4", seed=nx(), density=0.4 * lit, edge=0.1, rough=1, feather=0.6)
        clear()
    return art, ys_list


def part_scene():
    W, H = 780, 1500
    rng = random.Random(31); nx = Seq(500)
    rgb = painted_sky(W, H, [(0, "#a9bccb"), (0.12, "#c8d3d9"), (0.24, "#e9e5dc"), (0.3, "#f6efe2"), (0.52, "#f2f1ea"), (1, "#e6ece6")], seed=nx(), streak=0.05, grain=0.15)[..., :3]
    sun = radial(W, H, 590, 300, 260, sy=0.7)
    rgb = comp_rgb(rgb, flat(sun ** 1.6, "#fff4dc", 0.85))
    # Sindoro + Sumbing, far and cool
    far = blank(W, H)
    sin = poly(W, H, [(-60, 520), (120, 400), (220, 330), (262, 312), (300, 318), (380, 380), (560, 500), (700, 540), (-60, 560)], smooth=True)
    far = G(far, displace(sin, nx(), 2, 18), "#9fadc0", "#b2bccb", seed=nx(), density=0.75, edge=0.35, bloom=0.3, rough=2, feather=1.5)
    sum_ = poly(W, H, [(420, 560), (560, 460), (640, 418), (680, 410), (720, 424), (900, 520), (900, 580), (420, 580)], smooth=True)
    far = G(far, displace(sum_, nx(), 2, 18), "#b6bfcd", seed=nx(), density=0.6, edge=0.3, bloom=0.3, rough=2, feather=1.5)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gul = 0.5 + 0.5 * np.sin(np.arctan2(xx - 270, np.maximum(yy - 300, 1)) * 34 + (fbm(W, H, nx(), 30, 2) - .5) * 3)
    far = G(far, sin * np.clip((gul - 0.72) * 4, 0, 1) * ygrad(W, H, 320, 380) * (1 - ygrad(W, H, 440, 520)), "#7e8ea6", seed=nx(), density=0.35, edge=0.1, rough=1, feather=1)
    rgb = comp_rgb(rgb, far)
    clear()
    # plateau ridges (Prau / Pakuwaja) half drowned in mist
    rid = blank(W, H)
    for k, (base, amp, col) in enumerate([(610, 60, "#8fa3a4"), (690, 50, "#6f8a86")]):
        pts = [(-30, base + 80)]
        for x in range(-30, W + 40, 20):
            pts.append((x, base - amp * (0.5 + 0.5 * math.sin(x / 140 + k * 2.1)) - amp * 0.3 * math.sin(x / 47 + k)))
        pts.append((W + 40, base + 80))
        rid = G(rid, displace(poly(W, H, pts, smooth=True), nx(), 2, 16), col, mix_hex(col, "#a5b3ae", .4), seed=nx(), density=0.7, edge=0.35, bloom=0.4, rough=2, feather=1.4)
    rgb = comp_rgb(rgb, rid)
    clear()
    # the big mist bank where the names sit
    rgb = comp_rgb(rgb, mist_bank(W, H, [(560, 40, -60, W + 60, 0.75), (640, 56, -60, W + 60, 0.92), (730, 46, -60, W + 60, 0.85)], nx, rng))
    clear()
    # the far forested rim around the lake
    def rim(x):
        return 830 + 18 * math.sin(x / 120) - 30 * math.exp(-((x - 640) / 160) ** 2)
    rm = blank(W, H)
    hill = poly(W, H, [(-30, 900)] + [(x, rim(x) - 26 - 40 * math.exp(-((x - 120) / 150) ** 2) - 30 * math.exp(-((x - 660) / 120) ** 2)) for x in range(-30, W + 40, 15)] + [(W + 40, 900)], smooth=True)
    rm = G(rm, displace(hill, nx(), 2, 14), "#5f7d6b", "#6f8b76", seed=nx(), density=0.85, edge=0.35, bloom=0.3, rough=2, feather=1.2)
    trees = shapes(W, H, cemara_line(W, H, lambda x: rim(x) + 14, -20, W + 20, rng, 18, 46, (5, 11)), smooth=False)
    rm = G(rm, displace(trees, nx(), 1.2, 8), FOREST, FOREST_D, seed=nx(), density=0.9, edge=0.45, rough=0.8, feather=0.7)
    rm = G(rm, trees * np.clip(1 - xgrad(W, H, 0, W) * 1.2, 0, 1) * (1 - ygrad(W, H, 800, 860)), "#c9d6b8", seed=nx(), density=0.25, edge=0.05, rough=1, feather=1)
    rgb = comp_rgb(rgb, rm)
    clear()
    rgb = comp_rgb(rgb, mist_bank(W, H, [(812, 16, -40, 420, 0.55), (800, 12, 520, W + 40, 0.45)], nx, rng))
    clear()
    # Telaga Warna: turquoise in the middle, emerald at the edges, milky streaks, reflections of the forest
    lk = blank(W, H)
    lake_pts = [(-40, 860)] + [(x, rim(x) + 22 + rng.uniform(-2, 2)) for x in range(-40, W + 50, 26)] + [(W + 40, 1010), (560, 1040), (300, 1060), (-40, 1050)]
    lake = displace(poly(W, H, lake_pts, smooth=True), nx(), 2, 18)
    lk = G(lk, lake, "#57b8ad", "#7fcfc0", seed=nx(), density=0.97, edge=0.3, bloom=0.35, rough=1.5, feather=1.0)
    edge_t = lake * np.clip(1 - radial(W, H, 380, 950, 330, sy=0.28) * 1.6, 0, 1)
    lk = G(lk, edge_t, "#2f7f6a", "#3f8f5f", seed=nx(), density=0.7, edge=0.25, bloom=0.4, rough=3, feather=4)
    refl = shapes(W, H, [[(x, 2 * (rim(x) + 14) - y + 8) for x, y in p] for p in cemara_line(W, H, lambda x: rim(x) + 14, -20, W + 20, random.Random(31), 18, 46, (5, 11))], smooth=False)
    refl = displace(refl, nx(), 3, 6) * lake
    lk = G(lk, gaussian_filter(refl, 1.2) * 0.8, "#24534a", seed=nx(), density=0.55, edge=0.1, rough=2, feather=1.5)
    milk = []
    for _ in range(16):
        y = rng.uniform(900, 1030); x = rng.uniform(-40, W)
        L = rng.uniform(60, 220)
        milk.append(([(x, y), (x + L * 0.5, y + rng.uniform(-2, 2)), (x + L, y + rng.uniform(-3, 3))], rng.uniform(1.2, 3.2), (0.4, 0.4)))
    lk = G(lk, strokes(W, H, milk) * lake, "#d8f1ea", seed=nx(), density=0.6, edge=0.05, rough=1, feather=0.8)
    rgb = comp_rgb(rgb, lk)
    clear()
    # sulphur vent steam on the right shore
    st = blank(W, H)
    blobs = []
    for k in range(18):
        t = k / 17
        cx = 728 - t * 110 + math.sin(t * 6) * 18
        cy = 846 - t * 250
        r = 12 + t * 46
        blobs.append((cx + rng.uniform(-8, 8), cy, r * rng.uniform(0.9, 1.15), r * rng.uniform(0.7, 0.95), rng.uniform(-20, 20)))
    pm = displace(ellipses(W, H, blobs), nx(), 10, 22)
    st = G(st, pm, "#ffffff", "#eef1ee", seed=nx(), density=0.8, edge=0.1, bloom=0.5, rough=7, feather=5)
    st = G(st, pm * xgrad(W, H, 580, 740) * 0.8, "#c9d0cf", seed=nx(), density=0.4, edge=0.25, bloom=0.5, rough=5, feather=4)
    rgb = comp_rgb(rgb, st)
    clear()
    # near shore: a grassy bank and a few cemara on the left
    sh = blank(W, H)
    bank = poly(W, H, [(-30, 1010), (140, 1000), (330, 1040), (560, 1036), (W + 30, 1000), (W + 30, 1120), (-30, 1120)], smooth=True)
    sh = G(sh, displace(bank, nx(), 3, 18), "#7d9a5a", "#90a865", seed=nx(), density=0.95, edge=0.35, bloom=0.3, rough=2, feather=1, gran=0.3)
    big = shapes(W, H, cemara_line(W, H, lambda x: 1022 - (x / 8), 18, 120, rng, 90, 170, (26, 40), (0.13, 0.18)), smooth=False)
    sh = G(sh, displace(big, nx(), 1.2, 8), "#30493a", FOREST_D, seed=nx(), density=0.95, edge=0.5, rough=0.8, feather=0.7)
    rgb = comp_rgb(rgb, sh)
    clear()
    # terraced potato & cabbage slopes
    tr, _ = terraces(W, H, nx, rng, 1060, H + 40, 260, 120, 9, tilt=0.1)
    rgb = comp_rgb(rgb, tr)
    clear()
    rgb = comp_rgb(rgb, mist_bank(W, H, [(1068, 14, -40, 520, 0.45)], nx, rng))
    paperk = np.asarray(paper(W, H, "#ffffff", 7), np.float32) / 255
    rgb = rgb * (0.95 + 0.05 * paperk)
    prev_rgb(rgb, "dt-scene")
    rgb_save(rgb, f"{OUT}/scene.webp", quality=74)
    clear()


def part_terrace():
    W, H = 1000, 300
    rng = random.Random(8); nx = Seq(1200)
    tr, ys = terraces(W, H, nx, rng, 30, H + 10, 500, 70, 6)
    fade = np.clip(ygrad(W, H, 0, 40), 0, 1)
    tr[..., 3] *= fade
    preview(tr, "dt-terrace", tone="#eef1ea")
    save_full(tr, f"{OUT}/terrace.webp", size=(640, 192), quality=70)
    clear()


def carica(art, W, H, cx, cy, L, ang, nx, rng, ripe=1.0):
    """Carica (Vasconcellea pubescens) fruit: small, 5-ribbed, yellow-orange, pointed tip."""
    ca0, sa0 = math.cos(ang), math.sin(ang)
    side = []
    for t in np.linspace(0, 1, 18):
        w = L * 0.27 * (math.sin(math.pi * min(1, t ** 0.75)) ** 0.85) + L * 0.05 * (1 - t) ** 3
        side.append((t * L, w))
    outline = [(x, -w) for x, w in side] + [(x, w) for x, w in side[::-1]]
    pts = [(cx + x * ca0 - y * sa0, cy + x * sa0 + y * ca0) for x, y in outline]
    m = shape_mask(W, H, pts)
    art = knockout(art, m, amount=1.0, grow=1.0)
    art = G(art, m, mix_hex("#a9b85a", "#f2b640", ripe), mix_hex("#8ea24a", "#e9922c", ripe), seed=nx(), density=0.97, edge=0.6, bloom=0.25, rough=0.8, feather=0.6, gran=0.2)
    ca, sa = math.cos(ang), math.sin(ang)
    ribs = []
    for k in (-0.55, 0, 0.55):
        path = [(cx + ca * L * t - sa * k * L * 0.3 * math.sin(math.pi * t ** 0.8), cy + sa * L * t + ca * k * L * 0.3 * math.sin(math.pi * t ** 0.8)) for t in np.linspace(0.08, 0.95, 12)]
        ribs.append((path, max(1.0, L * 0.035), (0.2, 0.3)))
    art = G(art, strokes(W, H, ribs) * m, "#c4691e", seed=nx(), density=0.5, edge=0.2, rough=0.5, feather=0.6)
    lit = m * radial(W, H, cx + ca * L * 0.45 - sa * L * 0.12, cy + sa * L * 0.45 + ca * L * 0.12 - L * 0.05, L * 0.4)
    art = G(art, lit, "#fff0b0", seed=nx(), density=0.6, edge=0.05, rough=0.5, feather=1.5)
    sh = m * np.clip(1 - radial(W, H, cx + ca * L * 0.4 - sa * L * 0.2, cy + sa * L * 0.4 + ca * L * 0.2 - L * 0.1, L * 0.6) * 1.4, 0, 1)
    art = G(art, sh, "#b85a22", seed=nx(), density=0.35, edge=0.2, rough=0.5, feather=1.5)
    return art


def palm_leaf(W, H, cx, cy, R, ang, rng):
    """Palmate carica leaf: 5-7 lobes, each a broad pointed lobe radiating from the petiole."""
    polys = []
    lobes = rng.randint(5, 7)
    for k in range(lobes):
        a = ang + (k - (lobes - 1) / 2) * 0.42 + rng.uniform(-0.06, 0.06)
        L = R * (1 - abs(k - (lobes - 1) / 2) * 0.16) * rng.uniform(0.9, 1.05)
        polys.append(petal_pts(cx, cy, L, L * 0.17, a, n=16))
    return polys, lobes


def leaf_art(art, W, H, polys, cx, cy, nx):
    lm = shapes(W, H, polys)
    art = knockout(art, lm, amount=1.0, grow=1.0)
    art = G(art, lm, "#7fa36a", "#5d8a58", seed=nx(), density=0.92, edge=0.6, bloom=0.35, rough=1, feather=0.6, gran=0.3)
    art = G(art, lm * np.clip(1 - radial(W, H, cx, cy, 90) * 1.5, 0, 1), "#3f6a48", seed=nx(), density=0.35, edge=0.1, rough=1, feather=1.5)
    return art, lm


def part_carica():
    W, H = 760, 220
    rng = random.Random(14); nx = Seq(1500)
    art = blank(W, H)
    stem = curve([(30, 70), (200, 62), (380, 58), (560, 62), (730, 72)], 80)
    art = G(art, strokes(W, H, [(stem, 4.0, (0.08, 0.08))]), "#7a6a46", "#5f5a3a", seed=nx(), density=0.9, edge=0.4, rough=1, feather=0.6)
    for x0, side in [(110, -1), (240, 1), (520, -1), (650, 1)]:
        y0 = 62
        R = rng.uniform(64, 76)
        a = -math.pi / 2 + side * 0.55
        tip = (x0 + math.cos(a) * 26, y0 + math.sin(a) * 26)
        art = G(art, strokes(W, H, [([(x0, y0), tip], 2.4, (0.1, 0.2))]), "#8a7a4a", seed=nx(), density=0.85, edge=0.3, rough=0.6, feather=0.5)
        p, lobes = palm_leaf(W, H, tip[0], tip[1], R, a, rng)
        art, lm = leaf_art(art, W, H, p, tip[0], tip[1], nx)
        veins = []
        for k in range(lobes):
            aa = a + (k - (lobes - 1) / 2) * 0.42
            veins.append(([tip, (tip[0] + math.cos(aa) * R * 0.85, tip[1] + math.sin(aa) * R * 0.85)], 1.4, (0.05, 0.5)))
        art = G(art, strokes(W, H, veins) * lm, "#d9e3b8", seed=nx(), density=0.5, edge=0.0, rough=0.5, feather=0.5)
    for (x, y, L, a, ripe) in [(318, 62, 62, 1.85, 1.0), (360, 60, 74, 1.6, 1.0), (404, 60, 66, 1.35, 0.85), (282, 64, 46, 2.15, 0.35), (440, 62, 44, 1.05, 0.2)]:
        art = G(art, strokes(W, H, [([(x, y), (x + math.cos(a) * 10, y + math.sin(a) * 10)], 3, (0.1, 0.2))]), "#7a7a40", seed=nx(), density=0.9, edge=0.3, rough=0.5, feather=0.5)
        art = carica(art, W, H, x + math.cos(a) * 8, y + math.sin(a) * 8, L, a, nx, rng, ripe)
    preview(art, "dt-carica", tone="#f1efe8")
    save(art, f"{OUT}/carica.webp", max_w=360, quality=84)
    clear()


def part_fruit():
    W, H = 240, 280
    rng = random.Random(4); nx = Seq(1700)
    art = blank(W, H)
    p, _ = palm_leaf(W, H, 120, 74, 72, -math.pi / 2 - 0.15, rng)
    art, lm = leaf_art(art, W, H, p, 120, 74, nx)
    art = G(art, strokes(W, H, [([(120, 70), (118, 100)], 4, (0.1, 0.2))]), "#6c5d3e", seed=nx(), density=0.9, edge=0.3, rough=0.6, feather=0.5)
    art = carica(art, W, H, 117, 96, 136, 1.6, nx, rng)
    preview(art, "dt-fruit", tone="#f1efe8")
    save(art, f"{OUT}/fruit.webp", max_w=120, quality=84)
    clear()


def part_steam():
    W, H = 300, 560
    rng = random.Random(6); nx = Seq(1900)
    art = blank(W, H)
    blobs = []
    for k in range(22):
        t = k / 21
        cx = 150 + math.sin(t * 7) * 30 * t
        cy = 520 - t * 460
        r = 14 + t * 60
        blobs.append((cx + rng.uniform(-8, 8), cy, r * rng.uniform(0.85, 1.1), r * rng.uniform(0.7, 0.95), rng.uniform(-20, 20)))
    pm = displace(ellipses(W, H, blobs), nx(), 12, 24)
    art = G(art, pm, "#ffffff", "#f3f6f4", seed=nx(), density=0.85, edge=0.08, bloom=0.5, rough=8, feather=6)
    art[..., 3] *= np.clip(ygrad(W, H, 0, 140), 0, 1) * np.clip(1 - ygrad(W, H, 470, 560), 0, 1) * 0.9
    preview(art, "dt-steam", bg="#1f5c5a")
    save_full(art, f"{OUT}/steam.webp", size=(150, 280), quality=78)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
