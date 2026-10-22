"""Zanzibar Pintu — a carved Swahili door of oiled teak: lintel frieze of rosettes and vine scrolls, posts carved with
interlocking chain and leafy vines, lotus at the foot, door leaves set with brass spike studs; a lateen-rigged dhow on
a turquoise Indian Ocean (watercolour); lime-washed coral-stone wall texture. No figures (Islamic theme).
Run: python3 -I zanzibar-pintu.py [part ...]   parts: wall frame leaves stud dhow divider lotus
Assets -> public/themes/art/zanzibar-pintu/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _f2_lib import *  # noqa
from _jw_lib import carve

OUT = outdir("zanzibar-pintu")
PARTS = sys.argv[1:] or ["wall", "frame", "leaves", "stud", "dhow", "divider", "lotus"]
TK, TK_D, TK_L = "#5e3b23", "#2c1a0e", "#946640"
BRASS = "#caa451"


def chain_items(x, y0, y1, w, step=None):
    """Interlocking chain links running vertically: alternate open ovals and edge-on bars."""
    step = step or w * 1.15
    items = []
    y = y0 + step / 2
    k = 0
    while y < y1 - step / 2:
        if k % 2 == 0:
            pts = [(x + math.cos(a) * w * 0.42, y + math.sin(a) * step * 0.62) for a in np.linspace(0, math.tau, 26)]
            items.append((pts, w * 0.16, None))
        else:
            items.append(([(x, y - step * 0.55), (x, y + step * 0.55)], w * 0.2, None))
        y += step * 0.78
        k += 1
    return items


def chain_items_h(x0, x1, y, h):
    return [([(py, px) for px, py in pts], wd, tp) for pts, wd, tp in chain_items(y, x0, x1, h)]


def vine_items(x, y0, y1, w, rng, flip=1):
    """Vertical scrolling vine: sinuous stem, alternate leaves and small curled tendrils (as relief strokes + leaf polys)."""
    n = int((y1 - y0) / (w * 1.1))
    stem = [(x + math.sin(i / 60 * n * math.pi) * w * 0.22 * flip, y0 + (y1 - y0) * i / 60) for i in range(61)]
    items = [(stem, w * 0.1, (0.05, 0.05))]
    leaves = []
    for k in range(n):
        t = (k + 0.5) / n
        yy = y0 + (y1 - y0) * t
        side = 1 if k % 2 == 0 else -1
        xx = x + math.sin(t * n * math.pi) * w * 0.22 * flip
        leaves.append(petal_pts(xx, yy, w * 0.42, w * 0.13, (-0.6 if side > 0 else math.pi + 0.6), n=10))
        cur = spiral(xx - side * w * 0.18, yy + w * 0.3, w * 0.03, w * 0.13, 1.1, a0=0, n=20, direction=side)
        items.append((cur, w * 0.06, (0.0, 0.5)))
    return items, leaves


def rosette(cx, cy, r, n=8):
    pets = [petal_pts(cx + math.cos(a) * r * 0.18, cy + math.sin(a) * r * 0.18, r * 0.8, r * 0.26, a, n=10) for a in np.linspace(0, math.tau, n, endpoint=False)]
    ring = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in np.linspace(0, math.tau, 40)]
    return [(ring, r * 0.1, None)], pets + [ellipse_pts(cx, cy, r * 0.18, r * 0.18, 10)]


def lotus(cx, by, w):
    """Carved lotus at the foot of a post: fan of petals rising from a small vase."""
    pets = []
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.32
        L = w * (0.62 if k in (2, 3, 4) else 0.48)
        pets.append(petal_pts(cx, by - w * 0.28, L, w * 0.12, a, n=12))
    vase = [(cx - w * 0.22, by), (cx + w * 0.22, by), (cx + w * 0.14, by - w * 0.14), (cx + w * 0.26, by - w * 0.3), (cx - w * 0.26, by - w * 0.3), (cx - w * 0.14, by - w * 0.14)]
    return pets + [vase]


def lotus_items(cx, by, w):
    """Incised lotus: petal outlines with a centre vein, rising from a small footed vase (relief strokes)."""
    items = []
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.3
        L = w * (0.6 if k in (2, 3, 4) else 0.46)
        pts = petal_pts(cx, by - w * 0.26, L, w * 0.11, a, n=18)
        items.append((pts + [pts[0]], w * 0.03, None))
        items.append(([(cx, by - w * 0.26), (cx + math.cos(a) * L * 0.7, by - w * 0.26 + math.sin(a) * L * 0.7)], w * 0.02, (0.1, 0.5)))
    vase = [(cx - w * 0.2, by), (cx + w * 0.2, by), (cx + w * 0.12, by - w * 0.12), (cx + w * 0.24, by - w * 0.26), (cx - w * 0.24, by - w * 0.26), (cx - w * 0.12, by - w * 0.12), (cx - w * 0.2, by)]
    items.append((vase, w * 0.035, None))
    return items


def teak(art, band, items, leaves, nx):
    return carve(art.shape[1], art.shape[0], band, items, leaves, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0.0) if art is None else over(art, carve(art.shape[1], art.shape[0], band, items, leaves, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0.0))


def oil(art, nx, W, H, mask):
    """Oiled-teak grain and sheen over the carving."""
    grain = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (14, 0.7))
    grain = (grain - grain.mean()) / (grain.std() + 1e-6)
    out = art.copy()
    out[..., :3] = np.clip(out[..., :3] * (1 + grain[..., None] * 0.05 * mask[..., None]), 0, 1)
    return out


def part_wall():
    rgb = coral_stone(512, 512, "#efe6d4", seed=3)
    mean = rgb.mean(axis=(0, 1), keepdims=True)
    rgb = mean + (rgb - mean) * 0.5
    prev_rgb(rgb, "zp-wall")
    rgb_save(rgb, f"{OUT}/wall.webp", quality=72)


def part_frame():
    W, H = 640, 960
    rng = random.Random(4); nx = Seq(300)
    x0, x1, top, bot = 24, W - 24, 24, H - 6
    lin_b = 236
    ox0, ox1 = 154, W - 154
    art = blank(W, H)
    # cornice (projecting crown)
    corn = rect(W, H, x0 - 10, top, x1 + 10, top + 34)
    items = [([(x0 + 4, top + 26), (x1 - 4, top + 26)], 3, None)]
    dent = [[(x, top + 4), (x + 9, top + 4), (x + 9, top + 18), (x, top + 18)] for x in range(int(x0), int(x1) - 8, 16)]
    art = over(art, carve(W, H, corn, items, dent, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0))
    # lintel frieze: rosettes between vine scrolls
    lin = rect(W, H, x0, top + 34, x1, lin_b)
    it, lv = [], []
    it.append(([(x0 + 10, top + 64), (x1 - 10, top + 64)], 3, None)); it.append(([(x0 + 10, lin_b - 44), (x1 - 10, lin_b - 44)], 3, None))
    lv += [ellipse_pts(x, top + 50, 6, 6, 8) for x in np.arange(x0 + 18, x1 - 10, 17)]
    it += chain_items_h(x0 + 12, x1 - 12, lin_b - 24, 28)
    cy = (top + 64 + lin_b - 44) / 2
    for cx in (W / 2, x0 + 90, x1 - 90):
        a, b = rosette(cx, cy, 44 if cx == W / 2 else 34, n=12 if cx == W / 2 else 8)
        it += a; lv += b
    for xa, xb in ((x0 + 140, W / 2 - 66), (W / 2 + 66, x1 - 140)):
        stem = [(xa + (xb - xa) * i / 40, cy + math.sin(i / 40 * math.tau * 1.5) * 18) for i in range(41)]
        it.append((stem, 6, (0.05, 0.05)))
        for k in range(10):
            t = (k + 0.5) / 10
            sx = xa + (xb - xa) * t; sy = cy + math.sin(t * math.tau * 1.5) * 18
            side = 1 if k % 2 == 0 else -1
            lv.append(petal_pts(sx, sy, 24, 7.5, -math.pi / 2 * side + 0.5 * side, n=10))
            it.append((spiral(sx + 5, sy - side * 14, 1.5, 7, 1.1, a0=0, n=16, direction=side), 2.6, (0.0, 0.5)))
    art = over(art, carve(W, H, lin, it, lv, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0))
    clear()
    # posts: outer chain band + vine band + plain inner moulding; lotus at the foot
    for side in (0, 1):
        px0 = x0 if side == 0 else ox1
        px1 = ox0 if side == 0 else x1
        post = rect(W, H, px0, lin_b, px1, bot)
        pw = px1 - px0
        cx_chain = px0 + pw * (0.22 if side == 0 else 0.78)
        cx_vine = px0 + pw * (0.66 if side == 0 else 0.34)
        it = chain_items(cx_chain, lin_b + 12, bot - 150, pw * 0.36)
        a, b = vine_items(cx_vine, lin_b + 16, bot - 156, pw * 0.36, rng, flip=1 if side == 0 else -1)
        it += a; lv = b
        it.append(([(px0 + pw * 0.44, lin_b + 8), (px0 + pw * 0.44, bot - 140)], 3, None))
        bx = px0 + pw * (0.92 if side == 0 else 0.08)
        lv += [ellipse_pts(bx, y, 4.5, 6, 8) for y in np.arange(lin_b + 14, bot - 146, 15)]
        inner_x = px1 - 8 if side == 0 else px0 + 8
        it.append(([(inner_x, lin_b + 2), (inner_x, bot)], 4, None))
        it += lotus_items(px0 + pw / 2, bot - 18, pw * 0.86)
        it.append(([(px0 + 8, bot - 140), (px1 - 8, bot - 140)], 4, None))
        art = over(art, carve(W, H, post, it, lv, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0))
        clear()
    # opening shadow edge (the frame's inner reveal)
    reveal = np.clip(rect(W, H, ox0, lin_b, ox0 + 10, bot) + rect(W, H, ox0, lin_b, ox1, lin_b + 10), 0, 1)
    art = G(art, reveal, "#1c1209", seed=nx(), density=0.6, edge=0.2, rough=1, feather=2)
    m = np.clip(art[..., 3] * 3, 0, 1)
    art = oil(art, nx, W, H, m)
    sh = np.roll(np.roll(gaussian_filter(m, 6), 8, 0), 5, 1) * 0.35
    art = over(np.concatenate([np.zeros((H, W, 3), np.float32), sh[..., None]], -1), art)
    art = keep_pixel(art, 1, 1); art = keep_pixel(art, W - 2, H - 2)
    preview(art, "zp-frame", bg="#ece2cf")
    save_full(art, f"{OUT}/frame.webp", size=(480, 720), quality=80)
    clear()


def part_leaves():
    """The two door leaves: vertical planks, a carved chain mullion down the middle, rows of brass spike studs."""
    W, H = 480, 940
    rng = random.Random(6); nx = Seq(700)
    art = blank(W, H)
    board = rect(W, H, 0, 0, W, H)
    art = GP(art, board, "#4f3019", "#5c3a20", seed=nx(), rough=1, streak=1.6)
    planks = strokes(W, H, [([(x, 0), (x + rng.uniform(-1, 1), H)], 2.2, None) for x in np.arange(40, W, 40) if abs(x - W / 2) > 30])
    art = G(art, planks, TK_D, seed=nx(), density=0.6, edge=0.2, rough=0.6, feather=0.6)
    grain = gaussian_filter(np.random.default_rng(nx()).random((H, W)).astype(np.float32), (22, 0.8))
    grain = (grain - grain.mean()) / (grain.std() + 1e-6)
    art[..., :3] = np.clip(art[..., :3] * (1 + grain[..., None] * 0.07), 0, 1)
    # horizontal battens (rails) holding the studs
    rails = [70, 250, 470, 690, 870]
    rail_m = np.clip(sum(rect(W, H, 0, y - 16, W, y + 16) for y in rails), 0, 1)
    art = over(art, carve(W, H, rail_m, [([(0, y), (W, y)], 3, None) for y in rails], [], nx, base="#5b391f", light=TK_L, dark=TK_D, gold_amt=0))
    # central mullion with chain
    mul = rect(W, H, W / 2 - 26, 0, W / 2 + 26, H)
    art = over(art, carve(W, H, mul, chain_items(W / 2, 6, H - 6, 34) + [([(W / 2 - 22, 0), (W / 2 - 22, H)], 2.5, None), ([(W / 2 + 22, 0), (W / 2 + 22, H)], 2.5, None)], [], nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0))
    clear()
    # brass spike studs on the rails
    studs = []
    for y in rails:
        for x in np.linspace(40, W / 2 - 50, 4):
            studs.append((x, y)); studs.append((W - x, y))
    for y in (160, 360, 580, 780):
        for x in (100, W - 100):
            studs.append((x, y))
    base = circles(W, H, [(x, y, 13) for x, y in studs])
    sh = np.roll(np.roll(gaussian_filter(base, 3), 4, 0), 3, 1) * 0.6
    art = over(art, np.concatenate([np.zeros((H, W, 3), np.float32), sh[..., None]], -1))
    art = FO(art, base, BRASS, seed=nx(), emboss=0.8, sparkle=0.15)
    cone = circles(W, H, [(x, y, 7) for x, y in studs])
    art = FO(art, cone, "#d9b663", seed=nx(), emboss=1.2, sparkle=0.3)
    hi = circles(W, H, [(x - 2.5, y - 2.5, 2.2) for x, y in studs])
    art = OV(art, hi, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * col_arr("#fff3c9"), (m * 0.85)[..., None]], -1))
    ring = circles(W, H, [(x, y, 13) for x, y in studs]) - circles(W, H, [(x, y, 11) for x, y in studs])
    art = G(art, np.clip(ring, 0, 1), "#6d4f1c", seed=nx(), density=0.5, edge=0.1, rough=0.4, feather=0.5)
    # hasp ring on the mullion
    hasp = np.clip(circles(W, H, [(W / 2, 520, 26)]) - circles(W, H, [(W / 2, 520, 20)]), 0, 1)
    art = FO(art, hasp, BRASS, seed=nx(), emboss=0.9)
    preview(art, "zp-leaves")
    save_full(art, f"{OUT}/leaves.webp", size=(330, 646), quality=78)
    clear()


def part_stud():
    W, H = 120, 120
    nx = Seq(900)
    art = blank(W, H)
    base = circles(W, H, [(60, 60, 44)])
    sh = np.roll(np.roll(gaussian_filter(base, 4), 6, 0), 4, 1) * 0.5
    art = over(art, np.concatenate([np.zeros((H, W, 3), np.float32), sh[..., None]], -1))
    art = FO(art, base, BRASS, seed=nx(), emboss=0.8, sparkle=0.15)
    for r, c, e in ((32, "#c49c49", 1.0), (20, "#d9b663", 1.3), (9, "#e8cd84", 1.4)):
        art = FO(art, circles(W, H, [(60 - (44 - r) * 0.08, 60 - (44 - r) * 0.08, r)]), c, seed=nx(), emboss=e, sparkle=0.25)
    hi = circles(W, H, [(52, 51, 5)])
    art = OV(art, gaussian_filter(hi, 1.2), lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * col_arr("#fff6d8"), (m * 0.9)[..., None]], -1))
    preview(art, "zp-stud", tone="#ece2cf")
    save(art, f"{OUT}/stud.webp", max_w=64, quality=86)
    clear()


def part_lotus():
    """Carved rosette plaque (closing emblem / amp): a disc of teak carved with a twelve-petal rosette and a bead ring."""
    W, H = 260, 260
    nx = Seq(1000)
    disc = circles(W, H, [(130, 130, 118)])
    it, lv = rosette(130, 130, 74, n=12)
    lv += [ellipse_pts(130 + math.cos(a) * 100, 130 + math.sin(a) * 100, 5, 5, 8) for a in np.linspace(0, math.tau, 30, endpoint=False)]
    it += [([(130 + math.cos(a) * 112, 130 + math.sin(a) * 112) for a in np.linspace(0, math.tau, 60)], 3, None)]
    art = carve(W, H, disc, it, lv, nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0)
    art = FO(art, circles(W, H, [(130, 130, 14)]), BRASS, seed=nx(), emboss=1.0, sparkle=0.2)
    sh = np.roll(np.roll(gaussian_filter(disc, 5), 6, 0), 4, 1) * 0.4
    art = over(np.concatenate([np.zeros((H, W, 3), np.float32), sh[..., None]], -1), art)
    preview(art, "zp-lotus", tone="#ece2cf")
    save(art, f"{OUT}/rosette.webp", max_w=120, quality=84)
    clear()


def part_divider():
    W, H = 760, 120
    nx = Seq(1100)
    band = rect(W, H, 20, 22, W - 20, 68)
    items = chain_items_h(30, W - 30, 45, 40) + [([(20, 26), (W - 20, 26)], 2, None), ([(20, 64), (W - 20, 64)], 2, None)]
    art = carve(W, H, band, items, [], nx, base=TK, light=TK_L, dark=TK_D, gold_amt=0)
    for x in (20, W - 20, W / 2):
        art = FO(art, circles(W, H, [(x, 45, 13)]), BRASS, seed=nx(), emboss=0.9, sparkle=0.2)
        art = FO(art, circles(W, H, [(x - 1, 44, 6)]), "#e1c274", seed=nx(), emboss=1.2)
    fade = np.clip(xgrad(W, H, 0, 80) * (1 - xgrad(W, H, W - 80, W)), 0, 1) ** 0.5
    art[..., 3] *= np.maximum(fade, circles(W, H, [(20, 45, 15), (W - 20, 45, 15)]))
    preview(art, "zp-divider", tone="#ece2cf")
    save(art, f"{OUT}/divider.webp", max_w=380, quality=84)
    clear()


def part_dhow():
    """A lateen-rigged dhow running before the wind on turquoise water, low green coast behind, wide pale sky."""
    W, H = 900, 640
    rng = random.Random(12); nx = Seq(1300)
    rgb = painted_sky(W, H, [(0, "#a9d5df"), (0.45, "#e6f1ea"), (0.56, "#f6eedd"), (1, "#f6eedd")], seed=nx(), streak=0.3, grain=0.2)[..., :3]
    hz = 372
    cl = blank(W, H)
    lens = [(rng.uniform(0, W), rng.uniform(60, 240), rng.uniform(70, 180), rng.uniform(12, 24), 0) for _ in range(9)]
    cl = G(cl, displace(ellipses(W, H, lens), nx(), 10, 30), "#ffffff", "#f3f7f4", seed=nx(), density=0.75, edge=0.2, bloom=0.5, rough=10, feather=6)
    cl = G(cl, displace(ellipses(W, H, [(x, y + 10, a * 0.8, b * 0.5, 0) for x, y, a, b, _ in lens]), nx(), 8, 24), "#b9cfd6", seed=nx(), density=0.3, edge=0.3, rough=6, feather=4)
    rgb = comp_rgb(rgb, cl)
    coast = poly(W, H, [(-20, hz + 2), (-20, hz - 16), (120, hz - 22), (260, hz - 14), (330, hz - 6), (360, hz + 2)], smooth=True)
    coast2 = poly(W, H, [(620, hz + 2), (700, hz - 10), (820, hz - 14), (W + 20, hz - 8), (W + 20, hz + 2)], smooth=True)
    land = blank(W, H)
    land = G(land, displace(np.maximum(coast, coast2), nx(), 2, 10), "#7aa07c", "#94b58a", seed=nx(), density=0.85, edge=0.5, rough=1.5, feather=0.8)
    rgb = comp_rgb(rgb, land)
    sea = blank(W, H)
    sm = rect(W, H, -10, hz, W + 10, H + 10)
    sea = G(sea, sm, "#3fb2b4", "#2b9ea8", seed=nx(), density=0.95, edge=0.2, bloom=0.08, rough=4, feather=1, gran=0.15)
    sea = G(sea, sm * (1 - ygrad(W, H, hz, hz + 60)), "#1e7f95", seed=nx(), density=0.55, edge=0.1, rough=4, feather=3)
    sea = G(sea, sm * ygrad(W, H, hz + 120, H), "#8edccf", seed=nx(), density=0.55, edge=0.2, bloom=0.1, rough=8, feather=6)
    rip = []
    for _ in range(240):
        t = rng.random() ** 1.3
        y = hz + 6 + (H - hz) * t; x = rng.uniform(-40, W)
        L = (14 + 90 * t) * rng.uniform(0.6, 1.4)
        rip.append(([(x, y), (x + L * 0.5, y - 1.2), (x + L, y)], 0.7 + 2.2 * t, (0.4, 0.4)))
    sea = G(sea, strokes(W, H, rip), "#e9fbf5", seed=nx(), density=0.65, edge=0.1, rough=1, feather=0.5)
    sea = G(sea, strokes(W, H, [([(x, y + 3) for x, y in it[0]], it[1] * 0.7, it[2]) for it in rip[::2]]), "#167089", seed=nx(), density=0.35, edge=0.1, rough=1, feather=0.5)
    rgb = comp_rgb(rgb, sea)
    clear()
    # dhow
    d = blank(W, H)
    wl = 470
    hull = [(330, wl - 36), (360, wl - 30), (600, wl - 30), (640, wl - 46), (660, wl - 56), (626, wl - 12), (590, wl + 6), (380, wl + 6), (348, wl - 10)]
    hm = poly(W, H, hull, smooth=True)
    d = G(d, hm, "#6b4428", "#4f311c", seed=nx(), density=0.97, edge=0.5, rough=1, feather=0.6)
    d = G(d, hm * ygrad(W, H, wl - 30, wl + 6), "#2a180c", seed=nx(), density=0.6, edge=0.2, rough=1, feather=1)
    plank = strokes(W, H, [([(350, wl - 20 + k * 8), (630, wl - 26 + k * 9)], 1.2, (0.2, 0.2)) for k in range(3)]) * hm
    d = G(d, plank, "#2a180c", seed=nx(), density=0.45, edge=0.1, rough=0.6, feather=0.5)
    gun = strokes(W, H, [([(332, wl - 36), (600, wl - 32), (660, wl - 58)], 3.5, None)])
    d = G(d, gun, "#f1e6cf", seed=nx(), density=0.75, edge=0.2, rough=0.6, feather=0.5)
    mast = strokes(W, H, [([(486, wl - 32), (472, wl - 330)], 6, (0.0, 0.3))])
    d = G(d, mast, "#4b2f1a", seed=nx(), density=0.95, edge=0.3, rough=0.8, feather=0.5)
    # lateen sail: long yard angled forward, triangular canvas bellied out
    yard = [(330, wl - 230), (690, wl - 360)]
    sail = [(334, wl - 228), (420, wl - 262), (540, wl - 304), (688, wl - 358), (640, wl - 230), (580, wl - 120), (496, wl - 44), (430, wl - 120), (380, wl - 180)]
    sm2 = poly(W, H, sail, smooth=True)
    d = G(d, sm2, "#fbf3e2", "#f2e4c8", seed=nx(), density=0.97, edge=0.6, bloom=0.3, rough=1.2, feather=0.7, gran=0.2)
    shade = sm2 * np.clip(xgrad(W, H, 520, 680) * 0.7 + ygrad(W, H, wl - 360, wl - 60) * 0.3, 0, 1)
    d = G(d, shade, "#c9b48f", "#b8a586", seed=nx(), density=0.55, edge=0.3, bloom=0.4, rough=2, feather=2)
    seams = strokes(W, H, [([(380 + k * 44, wl - 190 - k * 16), (470 + k * 30, wl - 70 - k * 22)], 1.1, (0.2, 0.2)) for k in range(6)]) * sm2
    d = G(d, seams, "#a08b6a", seed=nx(), density=0.4, edge=0.1, rough=0.6, feather=0.5)
    d = G(d, strokes(W, H, [(yard, 5, (0.05, 0.1))]), "#3b2414", seed=nx(), density=0.95, edge=0.3, rough=0.8, feather=0.5)
    ropes = strokes(W, H, [([(688, wl - 358), (655, wl - 54)], 1.2, None), ([(330, wl - 230), (338, wl - 34)], 1.0, None), ([(496, wl - 44), (560, wl - 34)], 1.0, None)])
    d = G(d, ropes, "#3b2414", seed=nx(), density=0.6, edge=0.1, rough=0.4, feather=0.4)
    flag = poly(W, H, [(472, wl - 330), (472, wl - 312), (440, wl - 318)])
    d = G(d, flag, "#b83a2e", seed=nx(), density=0.9, edge=0.3, rough=0.6, feather=0.5)
    ref = d[::-1].copy()
    ref = np.roll(ref, 2 * wl - H + 4, 0)
    ref[..., 3] *= (np.arange(H)[:, None] > wl + 2) * 0.35
    ref[..., :3] = ref[..., :3] * 0.5 + col_arr("#1f8a98") * 0.5
    yy = np.arange(H, dtype=np.float32)[:, None]
    xx = np.arange(W, dtype=np.float32)[None, :]
    ref = np.stack([map_coordinates(ref[..., c], [np.clip(yy + 0 * xx, 0, H - 1), np.clip(xx + np.sin(yy / 4) * 6 + 0 * yy, 0, W - 1)], order=1) for c in range(4)], -1)
    wake = strokes(W, H, [([(380 - k * 30, wl + 8 + k * 4), (300 - k * 50, wl + 10 + k * 7)], 2.4 - k * 0.3, (0.3, 0.6)) for k in range(5)])
    rgb = comp_rgb(rgb, ref)
    rgb = comp_rgb(rgb, flat(wake, "#ffffff", 0.7))
    rgb = comp_rgb(rgb, d)
    paperk = np.asarray(paper(W, H, "#ffffff", 4), np.float32) / 255
    rgb = rgb * (0.95 + 0.05 * paperk)
    prev_rgb(rgb, "zp-dhow")
    rgb_save(rgb, f"{OUT}/dhow.webp", quality=76, size=(720, 512))
    clear()


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
