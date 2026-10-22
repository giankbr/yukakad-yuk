"""Karo Siwaluh — gouache: a rumah siwaluh jabu (eight-family Karo house) on stilts, its huge black ijuk-thatched roof
with woven bamboo gables (ayo-ayo) and horn finials, in front of the Berastagi highlands with Sinabung smoking softly;
plus an uis-Karo inspired weave rendered thread by thread (red / black / gold), and a Berastagi citrus sprig.
Run: python3 -I karo-siwaluh.py [part ...]   parts: scene rumah uis band jeruk divider
Assets -> public/themes/art/karo-siwaluh/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _e2_lib import *

OUT = outdir("karo-siwaluh")
PARTS = sys.argv[1:] or ["scene", "rumah", "uis", "band", "jeruk", "divider"]
RED, RED_D, BLACK, GOLD, WHITE = "#a3201d", "#6e1412", "#1b1514", "#d7a43c", "#efe6d2"
IJUK, IJUK_L = "#231c1a", "#4a3d36"
WOOD, WOOD_D, WOOD_L = "#6b3f26", "#3e2316", "#8e5a37"


# ------------------------------------------------------------------ weave (thread level)
def weave(W, H, warp_cols, weft_col, tw=4, sup=None, sup_col=GOLD, seed=1):
    """Warp threads run along x (one colour per thread row, list over y), plain weave with a weft colour.
    sup(i, j) -> True where a supplementary gold weft floats over the warp (i: thread row, j: column)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    jit = (wnoise(W, H, seed, 6) - 0.5) * 0.9
    i = np.floor((yy + jit) / tw).astype(int)
    j = np.floor(xx / tw).astype(int)
    u = ((yy + jit) / tw) % 1.0
    v = (xx / tw) % 1.0
    nrows = len(warp_cols)
    wc = np.array([col_arr(c) for c in warp_cols], np.float32)[i % nrows]
    weft = np.ones_like(wc) * col_arr(weft_col)
    top_warp = ((i + j) % 2 == 0)
    rgb = np.where(top_warp[..., None], wc * (0.7 + 0.32 * np.sin(np.pi * u))[..., None], weft * (0.62 + 0.3 * np.sin(np.pi * v))[..., None])
    if sup is not None:
        S = np.vectorize(sup)(i % 10000, j % 10000).astype(bool)
        # floats span 3 columns: shade along the float, darker at its ends
        gold = col_arr(sup_col) * (0.68 + 0.34 * np.sin(np.pi * u))[..., None]
        rgb = np.where(S[..., None], gold, rgb)
    # gaps between threads + fibre noise
    gap = np.minimum(np.minimum(u, 1 - u), np.minimum(v, 1 - v))
    rgb *= (0.78 + 0.22 * np.clip(gap * 6, 0, 1))[..., None]
    fib = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.4, 1.4))
    rgb *= (0.93 + 0.14 * fib)[..., None]
    return np.clip(rgb, 0, 1)


def uis_rows():
    """Warp colour per thread row for one band: black edges, red field, white/gold pin stripes."""
    rows = []
    rows += [BLACK] * 3 + [WHITE] + [BLACK] * 2 + [RED] * 2 + [GOLD] + [RED] * 2 + [BLACK]
    rows += [RED] * 4 + [RED_D] + [RED] * 2  # field above motif
    motif0 = len(rows)
    rows += [RED_D] * 9
    rows += [RED] * 2 + [RED_D] + [RED] * 4
    rows += [BLACK] + [RED] * 2 + [GOLD] + [RED] * 2 + [BLACK] * 2 + [WHITE] + [BLACK] * 3
    return rows, motif0


def diamond_sup(motif0, period=18):
    def f(i, j):
        r = i - motif0
        if r < 0 or r > 8:
            return False
        c = j % period
        d = abs(c - period // 2) + abs(r - 4) * 2
        return (d <= 8 and (d % 4 in (0, 1))) or (r == 4 and c in (0, 1))
    return f


def part_uis():
    """Seamless band texture (repeat-x): one uis stripe, 384 x (rows*tw)."""
    rows, m0 = uis_rows()
    tw = 4
    W, H = 18 * tw * 6, len(rows) * tw
    rgb = weave(W, H, rows, "#4a1210", tw, diamond_sup(m0), GOLD, seed=3)
    prev_rgb(rgb, "ks-uis")
    rgb_save(rgb, f"{OUT}/uis.webp", quality=82)


def part_band():
    """Full woven field (tile, repeat both ways) for card backs: red with black/gold pinstripes and small diamonds."""
    tw = 4
    rows = ([RED] * 6 + [BLACK] + [RED] * 6 + [GOLD] + [RED] * 3 + [BLACK] * 2 + [RED] * 3 + [GOLD])
    W, H = 18 * tw * 4, len(rows) * tw
    m0 = 7

    def sup(i, j):
        r = i - 0
        c = j % 18
        return (r % len(rows) in (8, 9, 10)) and (abs(c - 9) + abs(r % len(rows) - 9) * 2 <= 3)
    rgb = weave(W, H, rows, RED_D, tw, sup, GOLD, seed=5)
    prev_rgb(rgb, "ks-band")
    rgb_save(rgb, f"{OUT}/band.webp", quality=80)


# ------------------------------------------------------------------ landscape
def brushwork(art, W, H, mask, cols, n, L, wd, rng, nx, ang=0.0, angj=0.25, slope=None):
    """Short visible gouache strokes inside mask in a few tones (painterly texture over a base fill)."""
    ys, xs = np.where(mask > 0.5)
    if len(xs) == 0:
        return art
    for col in cols:
        items = []
        for _ in range(n):
            k = rng.randrange(len(xs)); x, y = float(xs[k]), float(ys[k])
            a = (slope(x, y) if slope else ang) + rng.uniform(-angj, angj)
            l = L * rng.uniform(0.5, 1.3)
            items.append(([(x, y), (x + math.cos(a) * l * 0.5, y + math.sin(a) * l * 0.5 + rng.uniform(-0.8, 0.8)), (x + math.cos(a) * l, y + math.sin(a) * l)], wd * rng.uniform(0.6, 1.3), (0.3, 0.4)))
        art = GP(art, strokes(W, H, items) * mask, col, seed=nx(), rough=0.8, streak=0.6, density=0.85)
    return art


def part_scene():
    W, H = 780, 980
    rng = random.Random(21); nx = Seq(400)
    skyl = painted_sky(W, H, [(0, "#a9c6d2"), (0.28, "#d5e2df"), (0.5, "#f4e6c8"), (1, "#f4e6c8")], seed=nx(), streak=0.15, grain=0.2)
    rgb = skyl[..., :3]
    sk = blank(W, H)
    wisps = displace(ellipses(W, H, [(140, 120, 150, 16, -3), (300, 150, 120, 10, 2), (620, 90, 170, 14, 4)]), nx(), 10, 30)
    sk = G(sk, wisps, "#ffffff", "#f6efe2", seed=nx(), density=0.6, edge=0.1, bloom=0.4, rough=8, feather=5)
    rgb = comp_rgb(rgb, sk)
    # Sinabung
    cx, peak, base = 480, 300, 690
    cone = [(cx - 470, base + 40)]
    for t in np.linspace(-1, 1, 70):
        x = cx + t * 470
        y = peak + (abs(t) ** 0.72) * (base - peak) + rng.uniform(-1.5, 1.5)
        if abs(t) < 0.06:
            y = peak + 6 + abs(t) * 40
        cone.append((x, y))
    cone.append((cx + 470, base + 40))
    cm = poly(W, H, cone, smooth=True)
    lay = GP(blank(W, H), cm, "#8a8fa4", "#767f97", seed=nx(), rough=1.5, streak=0.8)
    lay = brushwork(lay, W, H, cm * (1 - xgrad(W, H, cx - 120, cx + 40)), ["#a3a8b8", "#b6b4be"], 260, 26, 3.0, rng, nx, slope=lambda x, y: math.atan2(1, (x - cx) / max(1, y - peak) + 1e-3) if True else 0)
    lay = brushwork(lay, W, H, cm * xgrad(W, H, cx - 30, cx + 200), ["#636d86", "#59617a"], 260, 28, 3.0, rng, nx, slope=lambda x, y: math.atan2(1, (x - cx) / max(1, y - peak) + 1e-3))
    gul = []
    for k in range(22):
        t = rng.uniform(-0.75, 0.75)
        pts = [(cx + t * 22 + t * 470 * s ** 1.05 + rng.uniform(-2, 2), peak + 12 + s * (base - peak)) for s in np.linspace(0, 0.85, 14)]
        gul.append((pts, rng.uniform(1.2, 3.2), (0.1, 0.5)))
    lay = GP(lay, strokes(W, H, gul) * cm, "#4e5770", seed=nx(), rough=0.6, density=0.75)
    lay = over(lay, flat(cm * ygrad(W, H, base - 200, base + 20), "#a7b8a8", 0.7))
    rgb = comp_rgb(rgb, lay)
    plume = displace(ellipses(W, H, [(cx + 30 + k * 52, peak - 30 - k * 22 + (k % 2) * 8, 34 + k * 15, 22 + k * 7, -14) for k in range(6)]), nx(), 10, 30)
    pl = G(blank(W, H), plume, "#f4f2ee", "#d8d8dc", seed=nx(), density=0.75, edge=0.15, bloom=0.5, rough=8, feather=4)
    pl = G(pl, plume * ygrad(W, H, peak - 160, peak + 10), "#b9b9c4", seed=nx(), density=0.35, edge=0.2, bloom=0.5, rough=8, feather=5)
    rgb = comp_rgb(rgb, pl)
    clear()
    sib = poly(W, H, [(-60, 760), (20, 600), (90, 560), (150, 572), (240, 640), (380, 740), (-60, 780)], smooth=True)
    lay = GP(blank(W, H), sib, "#7e9893", "#6f8a86", seed=nx(), rough=1.5)
    lay = brushwork(lay, W, H, sib, ["#93aaa2", "#64807a"], 160, 22, 3, rng, nx, ang=0.6)
    rgb = comp_rgb(rgb, lay)
    clear()
    bands = [(700, "#86a687", "#7a9b7c", ["#a9c39c", "#5f8263"], 22), (748, "#6c9764", "#5f8a58", ["#98bd80", "#456f40"], 28), (806, "#55843f", "#4a7637", ["#8fb765", "#335c2c"], 30)]
    for yb, ca, cb, tones, amp in bands:
        ph = rng.uniform(0, 6)
        fy = lambda x, yb=yb, ph=ph, amp=amp: yb + math.sin(x / 120 + ph) * amp * 0.6 + math.sin(x / 47 + ph * 2) * amp * 0.25
        pts = [(-20, H + 10)] + [(x, fy(x)) for x in range(-20, W + 40, 16)] + [(W + 20, H + 10)]
        m = poly(W, H, pts, smooth=True)
        lay = GP(blank(W, H), m, ca, cb, seed=nx(), rough=2.0, streak=0.8)
        lay = brushwork(lay, W, H, m * (1 - ygrad(W, H, yb + 40, yb + 140)), tones, 900, 34, 4.2, rng, nx, ang=0.0, angj=0.2)
        rgb = comp_rgb(rgb, lay)
        clear()
    # field terraces: curved rows following the slope, patchwork colours with dark seams
    plots = blank(W, H)
    cols = ["#86ad5c", "#6a9a4c", "#a7bf6c", "#9a6a43", "#55874a", "#c2c77e", "#77a256"]
    y = 850.0
    r = 0
    while y < H + 10:
        hgt = 10 + r * 2.2
        x = -40
        ph = rng.uniform(0, 6)
        while x < W + 40:
            wdt = rng.uniform(80, 200)
            c = rng.choice(cols)
            def fy(xx, y=y, ph=ph):
                return y + math.sin(xx / 160 + ph) * 8
            top = [(xx, fy(xx)) for xx in np.linspace(x, x + wdt, 8)]
            bot = [(xx, fy(xx) + hgt) for xx in np.linspace(x + wdt, x, 8)]
            m = poly(W, H, top + bot)
            plots = GP(plots, m, c, mix_hex(c, "#2e4a2a", 0.25), seed=nx(), rough=1.4, streak=1.0)
            if c not in ("#9a6a43",):
                rows = strokes(W, H, [([(xx, fy(xx) + kk) for xx in np.linspace(x + 3, x + wdt - 3, 8)], 1.1, None) for kk in np.arange(3, hgt - 1, 3.6)])
                plots = GP(plots, rows * m, mix_hex(c, "#1f3a22", 0.3), seed=nx(), rough=0.6, density=0.7)
            x += wdt + 3
        seam = strokes(W, H, [([(xx, y + hgt + math.sin(xx / 160 + ph) * 8 + 1) for xx in range(-40, W + 40, 20)], 2.0, None)])
        plots = GP(plots, seam, "#3a5a2c", seed=nx(), rough=0.6, density=0.8)
        y += hgt + 3
        r += 1
        if r % 3 == 0:
            clear()
    rgb = comp_rgb(rgb, plots)
    clear()
    pines = []
    for x, yb, h in [(36, 760, 96), (74, 768, 74), (700, 770, 116), (742, 760, 88), (640, 784, 62), (300, 812, 50), (330, 818, 40)]:
        for k in range(8):
            t = k / 7
            yy = yb - h * (1 - t)
            pines.append([(x, yy - h * 0.16), (x - (5 + t * h * 0.2), yy + h * 0.08), (x + (5 + t * h * 0.2), yy + h * 0.08)])
    pm = displace(shapes(W, H, pines, smooth=False), nx(), 1.5, 8)
    lay = GP(blank(W, H), pm, "#2c4d37", "#1f3a2b", seed=nx(), rough=1.2)
    lay = over(lay, flat(pm * (1 - xgrad(W, H, 0, W)) * 0.0, "#000000"))
    rgb = comp_rgb(rgb, lay)
    paperk = np.asarray(paper(W, H, "#ffffff", 7), np.float32) / 255
    rgb = rgb * (0.94 + 0.06 * paperk)
    prev_rgb(rgb, "ks-scene")
    rgb_save(rgb, f"{OUT}/scene.webp", quality=78)
    clear()


# ------------------------------------------------------------------ the house
def ayo_pattern(W, H, cx, top, by, half, nx):
    """Woven bamboo gable face (ayo-ayo): concentric chevron bands in red / white / black on a triangle."""
    tri = poly(W, H, [(cx, top), (cx - half, by), (cx + half, by)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = (by - yy) - np.abs(xx - cx) * (by - top) / half * 0.0
    # chevron coordinate: distance to the sloped sides, measured vertically
    k = (by - top) / half
    dist = (yy - (top + np.abs(xx - cx) * k))
    band = np.floor(dist / 12).astype(int)
    return tri, band, dist


def part_rumah():
    W, H = 900, 900
    rng = random.Random(9); nx = Seq(700)
    art = blank(W, H)
    cx = 450
    ground = 820
    floor_y = 640
    wall_top = 560
    # stone footings + stilts (tiang) + cross beams
    st = []
    feet = []
    for x in np.linspace(190, 710, 8):
        st.append(([(x, floor_y + 12), (x + rng.uniform(-1, 1), ground - 14)], 20, None))
        feet.append((x, ground - 8, 22, 11, 0))
    art = GP(art, ellipses(W, H, feet), "#8e8a80", "#6f6b62", seed=nx(), rough=2)
    art = GP(art, strokes(W, H, st), WOOD, WOOD_D, seed=nx(), rough=1.2, streak=1.0)
    beams = rect(W, H, 170, floor_y + 40, 730, floor_y + 58)
    art = GP(art, beams, WOOD_D, seed=nx(), rough=1.0)
    shade = rect(W, H, 170, floor_y + 12, 730, ground - 20) * 0.0
    # floor sill
    sill = poly(W, H, [(150, floor_y - 6), (750, floor_y - 6), (744, floor_y + 16), (156, floor_y + 16)])
    art = GP(art, sill, WOOD_D, "#2c1a12", seed=nx(), rough=1)
    # walls lean outward (wider at top), dark timber with a red/white/black painted band (geometric)
    wall = poly(W, H, [(176, floor_y - 4), (724, floor_y - 4), (744, wall_top), (156, wall_top)])
    art = GP(art, wall, WOOD, WOOD_D, seed=nx(), rough=1.2, streak=1.0)
    planks = strokes(W, H, [([(x, wall_top + 4), (x, floor_y - 6)], 1.4, None) for x in np.arange(190, 712, 18)])
    art = over(art, flat(planks * wall, WOOD_D, 0.6))
    # painted band: triangles (tutup dadu style geometric), red/white/black
    by0, by1 = wall_top + 12, wall_top + 40
    tri_up, tri_dn = [], []
    for x in np.arange(170, 730, 28):
        tri_up.append([(x, by1), (x + 14, by0), (x + 28, by1)])
        tri_dn.append([(x + 14, by0), (x + 28, by1), (x + 42, by0)])
    bandm = rect(W, H, 166, by0 - 4, 734, by1 + 4)
    art = GP(art, bandm, BLACK, seed=nx(), rough=0.6)
    art = GP(art, shapes(W, H, tri_up, smooth=False) * bandm, RED, seed=nx(), rough=0.8)
    art = GP(art, shapes(W, H, [[(x + 8, by1 - 3), (x + 14, by0 + 9), (x + 20, by1 - 3)] for x in np.arange(170, 730, 28)], smooth=False), WHITE, seed=nx(), rough=0.5)
    # windows (small) and the front terrace (ture) with a ladder
    wins = [rect(W, H, x, wall_top + 50, x + 26, floor_y - 22) for x in (238, 636)]
    art = GP(art, np.maximum(*wins), "#1a100c", seed=nx(), rough=0.6)
    ture = poly(W, H, [(330, floor_y + 6), (570, floor_y + 6), (590, floor_y + 34), (310, floor_y + 34)])
    art = GP(art, ture, "#b48a55", "#8e6a3e", seed=nx(), rough=1.0, streak=1.0)
    slats = strokes(W, H, [([(x, floor_y + 8), (x - 3, floor_y + 32)], 1.2, None) for x in np.arange(318, 590, 9)])
    art = over(art, flat(slats * ture, "#6b4d2a", 0.6))
    lad = strokes(W, H, [([(420, floor_y + 34), (408, ground - 4)], 6, None), ([(480, floor_y + 34), (492, ground - 4)], 6, None)] +
                  [([(416 - k * 0.3, floor_y + 52 + k * 26), (484 + k * 0.3, floor_y + 52 + k * 26)], 4, None) for k in range(5)])
    art = GP(art, lad, "#9c7a4c", "#7a5a34", seed=nx(), rough=0.8)
    door = rect(W, H, 420, wall_top + 44, 480, floor_y - 6)
    art = GP(art, door, "#2a1a12", seed=nx(), rough=0.6)
    clear()
    # the great ijuk roof: wide hipped lower roof with a curved, rising ridge
    eave_y = wall_top + 22
    rl, rr = 70, 830
    lower = [(rl, eave_y)]
    rx0, rx1, ry = 262, 638, 318
    lower += [(rl + (rx0 - rl) * t, eave_y - (eave_y - ry) * t ** 1.7) for t in np.linspace(0, 1, 14)]
    lower += [(rx0 + (rx1 - rx0) * t, ry + math.sin(t * math.pi) * 10) for t in np.linspace(0, 1, 10)]
    lower += [(rr - (rr - rx1) * t, eave_y - (eave_y - ry) * t ** 1.7) for t in np.linspace(1, 0, 14)]
    lower += [(rr, eave_y)]
    lower += [(rr - 30, eave_y + 14), (cx, eave_y + 6), (rl + 30, eave_y + 14)]
    roof = displace(poly(W, H, lower, smooth=False), nx(), 1.5, 18)
    art = GP(art, roof, IJUK, "#2e2421", seed=nx(), rough=2.0, streak=1.0)
    # thatch fibre: long downward strokes, lighter on the lit left
    fib = []
    for _ in range(900):
        x = rng.uniform(rl, rr); y = rng.uniform(300, eave_y)
        L = rng.uniform(16, 50)
        lean = (x - cx) / 420 * 0.55
        fib.append(([(x, y), (x + lean * L, y + L)], rng.uniform(0.8, 1.8), (0.2, 0.4)))
    fm = strokes(W, H, fib) * roof
    art = over(art, flat(fm * (0.4 + 0.6 * (1 - xgrad(W, H, rl, rr))), IJUK_L, 0.75))
    art = over(art, flat(fm * xgrad(W, H, cx, rr), "#0f0b0a", 0.35))
    eave = strokes(W, H, [([(rl + 4, eave_y - 2), (cx, eave_y + 6), (rr - 4, eave_y - 2)], 7, None)])
    art = GP(art, eave * 1.0, "#15100f", seed=nx(), rough=1.0)
    clear()
    # upper gable (ayo-ayo): steep triangle facing us, woven in chevron bands, with a small overhanging ridge roof
    top_y, gby, half = 120, 352, 168
    tri = poly(W, H, [(cx, top_y), (cx - half, gby), (cx + half, gby)])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    kslope = (gby - top_y) / half
    dist = (yy - (top_y + np.abs(xx - cx) * kslope))
    bandi = np.floor(dist / 13).astype(int)
    cyc = [RED, WHITE, BLACK, RED, GOLD, BLACK]
    for ci, col in enumerate(cyc):
        m = tri * (bandi % len(cyc) == ci)
        art = GP(art, m, col, mix_hex(col, "#000000", 0.12), seed=nx(), rough=0.7)
    # woven texture: tiny diagonal ticks (bamboo strips over/under)
    wt = hatch(W, H, 0.78, 5.0, 0.22, nx(), 0.5) * ((np.floor(xx / 5) + np.floor(yy / 5)) % 2) + hatch(W, H, -0.78 + math.pi, 5.0, 0.22, nx(), 0.5) * (1 - (np.floor(xx / 5) + np.floor(yy / 5)) % 2)
    art = over(art, flat(wt * tri, "#000000", 0.22))
    art = over(art, flat(tri * xgrad(W, H, cx - 20, cx + half), "#000000", 0.18))
    # gable frame boards
    frame = strokes(W, H, [([(cx - half - 8, gby + 4), (cx, top_y - 6), (cx + half + 8, gby + 4)], 9, None), ([(cx - half - 4, gby + 2), (cx + half + 4, gby + 2)], 8, None)])
    art = GP(art, frame, WOOD_D, "#2a1a10", seed=nx(), rough=0.8)
    # ridge cap overhanging the gable, thatched
    cap = poly(W, H, [(cx - 40, top_y + 40), (cx, top_y - 20), (cx + 40, top_y + 40), (cx + 30, top_y + 44), (cx, top_y + 4), (cx - 30, top_y + 44)], smooth=True)
    art = GP(art, cap, IJUK, seed=nx(), rough=1.2)
    # horn finial (tanduk): a stylised buffalo head with up-curving horns on the ridge tip
    hx, hy = cx, top_y - 30
    head = ellipses(W, H, [(hx, hy, 15, 18, 0)])
    horns = strokes(W, H, [([(hx - 8, hy - 8), (hx - 30, hy - 14), (hx - 46, hy - 34), (hx - 46, hy - 56)], 9, (0.0, 0.6)),
                           ([(hx + 8, hy - 8), (hx + 30, hy - 14), (hx + 46, hy - 34), (hx + 46, hy - 56)], 9, (0.0, 0.6))])
    art = GP(art, np.maximum(head, horns), "#e9dcc2", "#cdbb98", seed=nx(), rough=0.8)
    art = GP(art, strokes(W, H, [([(hx, hy + 20), (hx, top_y + 2)], 5, None)]), WOOD_D, seed=nx(), rough=0.5)
    # small horn tips on the lower roof ridge ends
    for sx in (-1, 1):
        x0 = cx + sx * 188
        y0 = 322
        hr = strokes(W, H, [([(x0, y0), (x0 + sx * 18, y0 - 18), (x0 + sx * 20, y0 - 40)], 7, (0.0, 0.6))])
        art = GP(art, hr, "#e9dcc2", "#cdbb98", seed=nx(), rough=0.6)
    # soft cast shadow under the house on the ground
    gsh = ellipses(W, H, [(cx, ground - 6, 330, 14, 0)])
    art = over(flat(gaussian_filter(gsh, 6), "#2e3a24", 0.35), art)
    preview(art, "ks-rumah", tone="#f3ead6")
    save(art, f"{OUT}/rumah.webp", max_w=560, quality=82)
    clear()


def part_jeruk():
    W, H = 420, 320
    rng = random.Random(14); nx = Seq(1100)
    art = blank(W, H)
    stem = strokes(W, H, [([(30, 260), (120, 220), (220, 170), (330, 110), (390, 80)], 6, (0.0, 0.5)), ([(220, 170), (250, 120), (262, 80)], 4, (0.0, 0.6))])
    art = GP(art, stem, "#5a3a22", seed=nx(), rough=0.8)
    leaves = []
    for x, y, a, L in [(110, 222, -2.2, 70), (150, 206, 1.0, 64), (200, 180, -2.6, 58), (285, 140, 0.7, 66), (340, 108, -2.0, 60), (380, 84, 0.3, 50), (256, 100, -1.4, 48)]:
        leaves.append(petal_pts(x, y, L, L * 0.38, a, n=14, cup=0.1))
    lm = shapes(W, H, leaves)
    art = GP(art, lm, "#3f7a3a", "#2f5f30", seed=nx(), rough=1.0, streak=1.2)
    veins = strokes(W, H, [([pts[0], pts[len(pts) // 2]], 1.2, None) for pts in leaves])
    art = over(art, flat(veins * lm, "#8fbf6a", 0.6))
    fruits = [(170, 250, 34), (236, 236, 28), (318, 172, 30)]
    fm = circles(W, H, fruits)
    art = GP(art, fm, "#f2a23a", "#e7802a", seed=nx(), rough=1.0, streak=0.6)
    sh = np.clip(circles(W, H, [(x + r * 0.35, y + r * 0.35, r) for x, y, r in fruits]) - circles(W, H, [(x - r * 0.25, y - r * 0.25, r * 0.92) for x, y, r in fruits]), 0, 1) * fm
    art = over(art, flat(gaussian_filter(sh, 2), "#b8541c", 0.6))
    hl = circles(W, H, [(x - r * 0.4, y - r * 0.4, r * 0.22) for x, y, r in fruits])
    art = over(art, flat(gaussian_filter(hl, 2), "#ffe1a8", 0.7))
    dimp = hatch(W, H, 0.3, 3.0, 0.1, nx(), 3.0) * fm
    art = over(art, flat(dimp, "#c8641f", 0.25))
    preview(art, "ks-jeruk", tone="#f3ead6")
    save(art, f"{OUT}/jeruk.webp", max_w=260, quality=82)
    clear()


def part_divider():
    """A short woven uis strip with knotted fringes (rambu) at both ends."""
    rows, m0 = uis_rows()
    tw = 2
    sw, sh = 18 * tw * 7, len(rows) * tw
    strip = weave(sw, sh, rows, BLACK, tw, diamond_sup(m0, 18), GOLD, seed=8)
    W, H = sw + 140, sh + 20
    art = blank(W, H)
    art[10:10 + sh, 70:70 + sw, :3] = strip
    art[10:10 + sh, 70:70 + sw, 3] = 1
    nx = Seq(1300); rng = random.Random(3)
    fr = []
    for side in (-1, 1):
        x0 = 70 if side < 0 else 70 + sw
        for k in range(0, sh, 4):
            L = rng.uniform(36, 50)
            fr.append(([(x0, 10 + k + 2), (x0 + side * L * 0.5, 10 + k + 2 + rng.uniform(-1, 1)), (x0 + side * L, 10 + k + 2 + rng.uniform(-2, 2))], 1.6, (0.0, 0.5)))
    fm = strokes(W, H, fr)
    art = over(art, GP(blank(W, H), fm, RED, RED_D, seed=nx(), rough=0.4))
    knots = circles(W, H, [(70 - 10, 10 + k + 3, 2.6) for k in range(0, sh, 8)] + [(70 + sw + 10, 10 + k + 3, 2.6) for k in range(0, sh, 8)])
    art = over(art, GP(blank(W, H), knots, RED_D, seed=nx(), rough=0.3))
    preview(art, "ks-divider", tone="#f3ead6")
    save(art, f"{OUT}/divider.webp", max_w=W // 2 * 2, quality=84)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
