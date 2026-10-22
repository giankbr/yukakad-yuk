"""Gayo Kerawang — the Gayo highlands of Aceh Tengah: kerawang Gayo embroidery (chain-stitched pucuk rebung triangles,
emun berangkat cloud scrolls and sarak opat lozenges in red, yellow, green and white on black cotton), a branch of
Gayo arabica with ripe red cherries, and Danau Lut Tawar under morning mist with pines on the ridges.
Run: python3 -I gayo-kerawang.py [part ...]   parts: lake kopi band emblem cloth
Assets -> public/themes/art/gayo-kerawang/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g1_lib import *  # noqa

OUT = outdir("gayo-kerawang")
PARTS = sys.argv[1:] or ["lake", "kopi", "band", "emblem", "cloth", "divider"]
RED, YEL, GRN, WHT, BLK = "#c0322a", "#e7b52c", "#3d8a46", "#f1ead8", "#15120e"


# ---------------------------------------------------------------- embroidery motifs
def pucuk(cx, base, h, w, up=True):
    s = -1 if up else 1
    return [(cx - w / 2, base), (cx, base + s * h), (cx + w / 2, base)]


def tri_mask(W, H, pts):
    return poly(W, H, pts, smooth=False)


def band_emb(W, H, seed, scale=1.0):
    emb = Embroidery(W, H, seed)
    S = scale
    st, wd = 4.6 * S, 3.2 * S
    cy = H / 2
    # outer guide lines (double chain, yellow + red)
    for y, c in [(10 * S, YEL), (17 * S, RED), (H - 17 * S, RED), (H - 10 * S, YEL)]:
        emb.chain([(-10, y), (W + 10, y)], c, step=st, width=wd)
    # pucuk rebung: big triangles alternating up/down, filled with concentric chain rows
    period = 120 * S
    n = int(round(W / period))
    period = W / n
    cols_up = [[RED, YEL, GRN, WHT], [GRN, WHT, RED, YEL]]
    top, bot = 26 * S, H - 26 * S
    for k in range(n):
        x = k * period + period / 2
        up = tri_mask(W, H, [(x - period / 2 + 3, bot), (x, top), (x + period / 2 - 3, bot)])
        chain_fill(emb, up, RED, spacing=4.2 * S, step=st, width=wd * 0.95, cols=cols_up[k % 2])
        # inverted triangles in the gaps hold an emun (cloud) scroll pair
        gx = k * period
        for gx_ in ([gx] + ([W] if k == n - 1 else [])):
            dn = tri_mask(W, H, [(gx_ - period / 2 + 9, top), (gx_, bot - 8 * S), (gx_ + period / 2 - 9, top)])
            emb.chain([p for p in contour_outline(dn)], YEL, step=st, width=wd * 0.9)
            for d in (-1, 1):
                sp = spiral(gx_ + d * 9 * S, top + 20 * S, 2 * S, 9 * S, 1.4, a0=math.pi / 2 * (1 + d), n=40, direction=-d)
                emb.chain(sp[::-1], WHT, step=st * 0.8, width=wd * 0.8)
            emb.satin_dot(gx_, top + 40 * S, 3.4 * S, GRN)
    return emb


def contour_outline(mask):
    from skimage import measure
    cs = measure.find_contours(mask, 0.5)
    if not cs:
        return []
    c = max(cs, key=len)
    return [(float(p[1]), float(p[0])) for p in c[::2]]


def part_band():
    W, H = 960, 150
    base = cloth(W, H, BLK, seed=3, tile=True)
    emb = band_emb(W, H, 5)
    e = emb.array()
    # wrap stitches that ran past the edges
    rgb = comp_rgb(base, e)
    prev_rgb(rgb, "gk-band")
    rgb_save(rgb, f"{OUT}/band.webp", quality=80, size=(640, 100))
    clear()


def part_emblem():
    """Sarak opat lozenge medallion: four pucuk rebung pointing out from a square, emun scrolls between, on a black
    cloth lozenge with a stitched rim (transparent outside)."""
    W = H = 360
    cx = cy = W / 2
    R = 168
    loz = poly(W, H, [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)])
    base = cloth(W, H, BLK, seed=9, tile=False)
    emb = Embroidery(W, H, 11)
    st, wd = 4.4, 3.1
    for d, c in [(0, YEL), (9, RED)]:
        r = R - 8 - d
        emb.chain([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)], c, step=st, width=wd)
    cols = [RED, GRN, YEL, WHT]
    for k in range(4):
        a = k * math.pi / 2 - math.pi / 2
        ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
        b = 30; tip = 128; hw = 40
        tri = poly(W, H, [(cx + ux * b + vx * hw, cy + uy * b + vy * hw), (cx + ux * tip, cy + uy * tip), (cx + ux * b - vx * hw, cy + uy * b - vy * hw)])
        chain_fill(emb, tri, RED, spacing=5.0, step=st, width=wd * 0.95, cols=[cols[k], cols[(k + 2) % 4], cols[(k + 1) % 4]])
        # emun scroll pairs on the diagonals
        a2 = a + math.pi / 4
        px, py = cx + math.cos(a2) * 78, cy + math.sin(a2) * 78
        for d in (-1, 1):
            sp = spiral(px + math.cos(a2 + d * math.pi / 2) * 10, py + math.sin(a2 + d * math.pi / 2) * 10, 2, 11, 1.3,
                        a0=a2 + math.pi + d * 0.8, n=40, direction=d)
            emb.chain(sp[::-1], WHT if k % 2 else YEL, step=3.6, width=2.6)
    sq = poly(W, H, [(cx - 22, cy - 22), (cx + 22, cy - 22), (cx + 22, cy + 22), (cx - 22, cy + 22)])
    chain_fill(emb, sq, YEL, spacing=4.6, step=3.8, width=2.8, cols=[YEL, RED, WHT])
    e = emb.array()
    rgb = comp_rgb(base, e)
    m = np.clip(gaussian_filter(displace(loz, 3, 1.2, 10), 0.6) * 1.4, 0, 1)
    arr = np.concatenate([rgb, m[..., None]], -1)
    preview(arr, "gk-emblem", bg="#e6e4dc")
    save(arr, f"{OUT}/emblem.webp", max_w=220, quality=84)
    clear()


def part_divider():
    """A short stitched line for section heads: double chain line ending in emun scrolls, small pucuk rebung pair and a
    central lozenge, embroidered straight onto the page (transparent ground)."""
    W, H = 520, 90
    cx, cy = W / 2, H / 2
    emb = Embroidery(W, H, 31)
    for d, c in [(-4, YEL), (4, RED)]:
        emb.chain([(60, cy + d), (cx - 46, cy + d)], c, step=4.2, width=3.0)
        emb.chain([(cx + 46, cy + d), (W - 60, cy + d)], c, step=4.2, width=3.0)
    for sx in (-1, 1):
        sp = spiral(cx + sx * (cx - 44), cy, 2, 14, 1.4, a0=math.pi * (0 if sx < 0 else 1), n=50, direction=sx)
        emb.chain(sp[::-1], GRN, step=3.8, width=2.8)
        for k, x in enumerate((cx + sx * 80, cx + sx * 130)):
            t = tri_mask(W, H, [(x - 14, cy - 6), (x, cy - 26), (x + 14, cy - 6)])
            chain_fill(emb, t, RED, spacing=4.0, step=3.6, width=2.6, cols=[RED, WHT] if k else [GRN, YEL])
            t = tri_mask(W, H, [(x - 14, cy + 6), (x, cy + 26), (x + 14, cy + 6)])
            chain_fill(emb, t, RED, spacing=4.0, step=3.6, width=2.6, cols=[YEL, GRN] if k else [WHT, RED])
    loz = poly(W, H, [(cx, cy - 32), (cx + 32, cy), (cx, cy + 32), (cx - 32, cy)])
    chain_fill(emb, loz, RED, spacing=4.2, step=3.8, width=2.8, cols=[RED, YEL, GRN, WHT])
    arr = emb.array()
    preview(arr, "gk-divider", tone="#efeee6")
    save(arr, f"{OUT}/divider.webp", max_w=300, quality=86)
    clear()


def part_cloth():
    W = H = 320
    rgb = cloth(W, H, BLK, seed=21, tile=True, weave=1.6, strength=0.12)
    prev_rgb(rgb, "gk-cloth")
    rgb_save(rgb, f"{OUT}/cloth.webp", quality=70)


# ---------------------------------------------------------------- the lake
def pine(W, H, x, by, h, rng):
    """Sumatran pine (Pinus merkusii) silhouette: tall bare trunk, flat-topped tiered crown."""
    items = [([(x, by), (x + rng.uniform(-3, 3), by - h * 0.6), (x + rng.uniform(-4, 4), by - h)], max(1.5, h * 0.025), (0.0, 0.5))]
    blobs = []
    for k in range(5):
        t = 0.55 + k * 0.1
        yy = by - h * t
        wd = h * (0.24 - k * 0.035) * rng.uniform(0.8, 1.2)
        blobs.append((x + rng.uniform(-wd * 0.3, wd * 0.3), yy, wd, h * 0.05, rng.uniform(-6, 6)))
    return strokes(W, H, items), ellipses(W, H, blobs)


def part_lake():
    W, H = 780, 900
    rng = random.Random(13); nx = Seq(300)
    rgb = painted_sky(W, H, [(0, "#d7d9d2"), (0.18, "#ece4d2"), (0.34, "#f4e7cf"), (0.42, "#e4e2d6"), (1, "#b9c6c4")], seed=nx(), streak=0.3, grain=0.2)[..., :3]
    sun = radial(W, H, 520, 240, 300, sy=0.7)
    rgb = comp_rgb(rgb, flat(sun ** 1.6, "#fff3d6", 0.8))
    cl = blank(W, H)
    lens = [(rng.uniform(-80, W), rng.uniform(40, 250), rng.uniform(90, 220), rng.uniform(10, 20), rng.uniform(-3, 2)) for _ in range(12)]
    cm = displace(ellipses(W, H, lens), nx(), 10, 30)
    cl = G(cl, cm, "#c9c8c0", "#bcbfba", seed=nx(), density=0.45, edge=0.3, bloom=0.5, rough=10, feather=6)
    cl = G(cl, cm * ygrad(W, H, 60, 260), "#f6dcb4", seed=nx(), density=0.35, edge=0.2, bloom=0.4, rough=6, feather=5)
    rgb = comp_rgb(rgb, cl)
    clear()
    # far ridges around the lake: overlapping, bluer and paler with distance
    ridges = [(300, 80, "#b4bcbd", "#a6afb3", 0.7, (1.1, 2.7)), (350, 95, "#94a3a6", "#83959a", 0.85, (1.6, 3.3)),
              (400, 70, "#768c8b", "#66797c", 0.9, (2.2, 4.1))]
    for k, (base, amp, c1, c2, dens, fr) in enumerate(ridges):
        lay = blank(W, H)
        m = displace(poly(W, H, ridge_pts(W, base, amp, rng, freq=fr, bottom=470), smooth=True), nx(), 3, 24)
        lay = G(lay, m, c1, c2, seed=nx(), density=dens, edge=0.35, bloom=0.35, rough=3, feather=1.5)
        lay = G(lay, m * ygrad(W, H, base - amp, base + 30) * 0.8, mix_hex(c2, "#3f5458", 0.3), seed=nx(), density=0.35, edge=0.1, rough=3, feather=3)
        rgb = comp_rgb(rgb, lay)
        rgb = comp_rgb(rgb, mist(W, H, [(base + 8, 14 + k * 4, -40, W + 40, 0.55)], nx, rng))
        clear()
    # near ridge on the right with pines
    lay = blank(W, H)
    nm = displace(poly(W, H, [(330, 490), (420, 430), (520, 385), (610, 350), (700, 330), (W + 20, 325), (W + 20, 490)], smooth=True), nx(), 3, 20)
    lay = G(lay, nm, "#4f6a55", "#3f5a4c", seed=nx(), density=0.95, edge=0.4, bloom=0.3, rough=2, feather=1)
    lay = G(lay, nm * ygrad(W, H, 330, 470), "#2f4a40", seed=nx(), density=0.45, edge=0.1, rough=3, feather=3)
    trunks, crowns = [], []
    for x in [470, 515, 548, 600, 642, 688, 722, 760]:
        by = 382 - (x - 470) * 0.18 + rng.uniform(-4, 4)
        t, c = pine(W, H, x, by + 12, rng.uniform(70, 120), rng)
        trunks.append(t); crowns.append(c)
    tm = np.clip(sum(trunks), 0, 1); cm = displace(np.clip(sum(crowns), 0, 1), nx(), 4, 10)
    lay = G(lay, tm, "#2e3b33", seed=nx(), density=0.8, edge=0.3, rough=1, feather=0.6)
    lay = G(lay, cm, "#2f4a3c", "#3c5a45", seed=nx(), density=0.9, edge=0.5, bloom=0.3, rough=2, feather=1)
    rgb = comp_rgb(rgb, lay)
    clear()
    # the lake: pale silver-teal, horizontal brush strokes, reflections of ridges, a lit path from the sun
    lake = blank(W, H)
    lm = displace(poly(W, H, [(-20, 470), (W + 20, 462), (W + 20, H + 20), (-20, H + 20)], smooth=False), nx(), 2, 30)
    lake = G(lake, lm, "#b8c8c6", "#9fb4b5", seed=nx(), density=0.95, edge=0.15, bloom=0.3, rough=2, feather=1.2)
    lake = G(lake, lm * ygrad(W, H, 490, H), "#6f8f92", "#5f7f86", seed=nx(), density=0.55, edge=0.1, bloom=0.5, rough=4, feather=5)
    idx = np.clip(940 - np.arange(H), 0, H - 1)
    refl = gaussian_filter(nm[idx], (2, 0.5)) * lm
    lake = G(lake, refl * 0.6 * (1 - ygrad(W, H, 470, 610)), "#4d6658", seed=nx(), density=0.45, edge=0.1, bloom=0.2, rough=2, feather=2)
    strokes_ = []
    for _ in range(300):
        t = rng.random() ** 1.2
        y = 478 + (H - 478) * t
        x = rng.uniform(-60, W)
        L = (20 + 160 * t) * rng.uniform(0.5, 1.4)
        strokes_.append(([(x, y), (x + L / 2, y + rng.uniform(-1, 1)), (x + L, y)], 0.6 + 2.6 * t, (0.4, 0.4)))
    sm = strokes(W, H, strokes_) * lm
    lake = G(lake, sm * (0.4 + 0.6 * fbm(W, H, nx(), 60, 2)), "#557479", seed=nx(), density=0.3, edge=0.1, rough=1, feather=0.6)
    glint = sm * radial(W, H, 520, 560, 260, sy=1.6)
    lake = G(lake, glint, "#fff6de", seed=nx(), density=0.85, edge=0.0, rough=1, feather=0.6)
    rgb = comp_rgb(rgb, lake)
    clear()
    rgb = comp_rgb(rgb, mist(W, H, [(475, 22, -40, W + 40, 0.85), (520, 16, -40, 420, 0.55), (570, 12, 200, W + 40, 0.35)], nx, rng, col="#f6f3ea"))
    clear()
    # a perahu (small fishing boat) far out on the lake: just a dark sliver with a pole
    bt = blank(W, H)
    bm = poly(W, H, [(228, 542), (268, 542), (262, 548), (234, 548)], smooth=True)
    bt = G(bt, bm, "#3a3a34", seed=nx(), density=0.85, edge=0.3, rough=0.6, feather=0.5)
    bt = G(bt, strokes(W, H, [([(250, 542), (256, 518)], 1.4)]), "#3a3a34", seed=nx(), density=0.7, edge=0.2, rough=0.4, feather=0.4)
    bt = G(bt, strokes(W, H, [([(218, 552), (280, 552)], 1.4)]), "#8ea2a2", seed=nx(), density=0.5, edge=0.0, rough=0.4, feather=0.5)
    rgb = comp_rgb(rgb, bt)
    paperk = np.asarray(paper(W, H, "#ffffff", 7), np.float32) / 255
    rgb = rgb * (0.95 + 0.05 * paperk)
    prev_rgb(rgb, "gk-lake")
    rgb_save(rgb, f"{OUT}/lake.webp", quality=74)
    clear()


# ---------------------------------------------------------------- coffee branch
def coffee_leaf(art, W, H, x, y, L, ang, nx, rng, dark=False):
    pts = petal_pts(x, y, L, L * 0.23, ang, n=18, cup=0.05)
    # wavy edge (coffee leaves are undulate)
    pts = [(px + math.sin(i * 1.7) * 1.6, py + math.cos(i * 1.7) * 1.6) for i, (px, py) in enumerate(pts)]
    m = shape_mask(W, H, pts)
    art = knockout(art, m, amount=0.7, grow=1.0)
    c1, c2 = ("#1f4a30", "#2c5e3a") if dark else ("#3b7445", "#2d6038")
    art = G(art, m, c1, c2, seed=nx(), density=0.9, edge=0.6, bloom=0.35, rough=1.2, feather=0.7, gran=0.2)
    ex, ey = x + math.cos(ang) * L, y + math.sin(ang) * L
    # glossy highlight along one half
    side = m * radial(W, H, x + math.cos(ang) * L * 0.4 + math.cos(ang - 1.57) * L * 0.08, y + math.sin(ang) * L * 0.4 + math.sin(ang - 1.57) * L * 0.08, L * 0.32)
    art = G(art, side, "#9cc07a", seed=nx(), density=0.45, edge=0.1, rough=1, feather=1.5)
    vein = [(x, y), ((x + ex) / 2 + math.cos(ang + 1.57) * L * 0.02, (y + ey) / 2 + math.sin(ang + 1.57) * L * 0.02), (ex, ey)]
    vs = [(curve(vein, 20), max(1.0, L * 0.018), (0.0, 0.6))]
    for k in range(1, 7):
        t = k / 7
        bx, by = x + math.cos(ang) * L * t, y + math.sin(ang) * L * t
        for d in (-1, 1):
            a2 = ang + d * 0.9
            ll = L * 0.2 * math.sin(t * math.pi)
            vs.append(([(bx, by), (bx + math.cos(a2) * ll, by + math.sin(a2) * ll)], max(0.6, L * 0.008), (0.0, 0.7)))
    art = G(art, strokes(W, H, vs) * m, "#183a26", seed=nx(), density=0.45, edge=0.1, rough=0.5, feather=0.5)
    return art


def cherry(art, W, H, x, y, r, col, nx, rng):
    m = shape_mask(W, H, ellipse_pts(x, y, r, r * 0.92, n=12, rot=rng.uniform(0, 3)))
    art = knockout(art, m, amount=0.95, grow=0.6)
    deep = mix_hex(col, "#3a0a0a", 0.55)
    art = G(art, m, col, deep, seed=nx(), density=0.95, edge=0.7, bloom=0.2, rough=0.5, feather=0.5, pad=8)
    art = G(art, m * radial(W, H, x + r * 0.35, y + r * 0.35, r * 1.0), deep, seed=nx(), density=0.5, edge=0.1, rough=0.4, feather=0.6, pad=8)
    hl = circles(W, H, [(x - r * 0.35, y - r * 0.35, r * 0.22)])
    art = G(art, hl, "#fff1e0", seed=nx(), density=0.75, edge=0.0, rough=0.3, feather=0.6, pad=8)
    art = G(art, circles(W, H, [(x + r * 0.15, y + r * 0.7, r * 0.12)]), "#3a1a10", seed=nx(), density=0.5, edge=0.2, rough=0.2, feather=0.4, pad=8)
    return art


def part_kopi():
    W, H = 900, 600
    rng = random.Random(7); nx = Seq(700)
    art = blank(W, H)
    stem = curve([(-10, 90), (180, 120), (380, 160), (580, 205), (760, 262), (900, 318)], 120)
    nodes = [stem[i] for i in (10, 28, 47, 66, 86, 106)]
    for i, (x, y) in enumerate(nodes):
        s_ = 1.0 - i * 0.05
        art = coffee_leaf(art, W, H, x, y - 2, rng.uniform(150, 200) * s_, -0.45 - rng.uniform(0, 0.55), nx, rng, dark=True)
        clear()
    art = G(art, strokes(W, H, [(stem, 8.0, (0.0, 0.5))]), "#6a4a32", "#4e3424", seed=nx(), density=0.95, edge=0.5, rough=1, feather=0.6)
    art = G(art, strokes(W, H, [([(x, y - 2) for x, y in stem], 2.2, (0.0, 0.5))]), "#a07a56", seed=nx(), density=0.5, edge=0.1, rough=0.6, feather=0.5)
    for i, (x, y) in enumerate(nodes):
        s_ = 1.0 - i * 0.05
        art = coffee_leaf(art, W, H, x + 4, y + 6, rng.uniform(170, 220) * s_, 0.95 + rng.uniform(0, 0.6), nx, rng)
        clear()
    for i, (x, y) in enumerate(nodes):
        cl = []
        for k in range(rng.randint(7, 10)):
            a = rng.uniform(0, math.tau)
            d = rng.uniform(0, 1) ** 0.6 * 24
            cl.append((x + math.cos(a) * d * 1.4, y + 4 + math.sin(a) * d * 0.8, rng.uniform(15, 20)))
        cl.sort(key=lambda c: c[1])
        for cx, cy, r in cl:
            pool = ["#b81f22", "#c72a26", "#a3171f", "#c72a26", "#d2462a"] if i < 4 else ["#b81f22", "#d65a2a", "#c2a63a", "#9aa53a"]
            art = cherry(art, W, H, cx, cy, r, rng.choice(pool), nx, rng)
        clear()
    preview(art, "gk-kopi", tone="#e8e6dc")
    save(art, f"{OUT}/kopi.webp", max_w=560, quality=82)
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
