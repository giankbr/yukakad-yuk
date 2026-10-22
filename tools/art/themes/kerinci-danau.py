"""Kerinci Danau — Kerinci, Jambi, as a matte gouache poster: Gunung Kerinci's tall grey-violet cone with a thin plume
over Kayu Aro tea slopes (combed rows of round bushes, red-earth paths, shade trees), Danau Kerinci in front with its
far shore; carved wooden boards of the rumah larik (keluk paku fern spirals, four-petal flowers, painted ochre/red on
dark wood); a tea sprig (two leaves and a bud).
Run: python3 -I kerinci-danau.py [part ...]   parts: scene larik sprig wood
Assets -> public/themes/art/kerinci-danau/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _g1_lib import *  # noqa
import _jw_lib as jw

OUT = outdir("kerinci-danau")
PARTS = sys.argv[1:] or ["scene", "larik", "sprig", "wood", "divider"]
WOOD, WOOD_D, WOOD_L = "#5a3420", "#2e1a10", "#7b4a2c"
OCHRE, RED, CREAM = "#d9a441", "#a8352a", "#efe2c4"


def gp(art, mask, c1, c2=None, seed=1, rough=2.5, streak=0.7, pad=16):
    return GP(art, mask, c1, c2, seed=seed, rough=rough, streak=streak, pad=pad)


def part_scene():
    W, H = 780, 1400
    rng = random.Random(31); nx = Seq(900)
    art = painted_sky(W, H, [(0, "#6c7aa6"), (0.12, "#9b98bd"), (0.24, "#e2b9a6"), (0.31, "#f4d6ae"), (0.42, "#f3e4c8"), (1, "#e9dcc0")], seed=nx(), streak=0.9, grain=0.4)
    sky = rect(W, H, 0, 0, W, 640)
    art = brushwork(art, sky * (1 - ygrad(W, H, 0, 260)), ["#7d86b0", "#8f8fb8", "#a8a0c2"], rng, nx, n=260, L=(40, 110), wd=(5, 12), ang=0.0, ang_var=0.05)
    art = brushwork(art, sky * ygrad(W, H, 180, 300) * (1 - ygrad(W, H, 420, 560)), ["#f0c9a8", "#f6dbb6", "#e8bba6"], rng, nx, n=260, L=(40, 120), wd=(5, 11), ang=0.0, ang_var=0.05)
    # cloud banks: lumpy gouache shapes with lit undersides
    cl = []
    for _ in range(7):
        y = rng.uniform(120, 360); x = rng.uniform(-60, W)
        for j in range(6):
            cl.append((x + j * rng.uniform(18, 30), y + rng.uniform(-8, 4), rng.uniform(24, 46), rng.uniform(9, 15), 0))
    cm = displace(ellipses(W, H, cl), nx(), 6, 16)
    art = GP(art, cm, "#c9adc0", "#b8a0b8", seed=nx(), rough=3, streak=1.2)
    art = brushwork(art, cm * ygrad(W, H, 100, 380), ["#f7d9c0", "#f2c7ae"], rng, nx, n=140, L=(16, 40), wd=(3, 6), ang=0.0, ang_var=0.1)
    clear()
    # Gunung Kerinci: broad shoulder on the right, summit at ~(420, 268)
    prof = [(-40, 780), (60, 700), (180, 560), (290, 420), (370, 318), (404, 276), (420, 266), (444, 268), (470, 284), (520, 340), (580, 400), (640, 438), (700, 470), (760, 540), (W + 40, 600), (W + 40, 800), (-40, 800)]
    cone = displace(poly(W, H, prof, smooth=True), nx(), 2, 18)
    art = GP(art, cone, "#6f6a8c", "#5f5c7e", seed=nx(), rough=2.2, streak=1.6)
    summit = (428, 272)
    def radial_dir(x, y):
        return math.atan2(y - summit[1], x - summit[0])
    left = cone * np.clip(1.15 - xgrad(W, H, 150, 470), 0, 1) * (1 - ygrad(W, H, 540, 780) * 0.7)
    art = brushwork(art, cone, ["#5a5677", "#6b6788", "#7b7596"], rng, nx, n=520, L=(26, 70), wd=(3, 7), dir_fn=radial_dir, ang_var=0.06)
    art = brushwork(art, cone * (left > 0.45), ["#c39aa0", "#b28d9c", "#d8aaa4"], rng, nx, n=320, L=(24, 64), wd=(2.5, 6), dir_fn=radial_dir, ang_var=0.06, weight=left)
    gul = []
    for k in range(30):
        t = (k + rng.uniform(0.2, 0.8)) / 30
        bx = -20 + (W + 40) * t
        by = 700 + rng.uniform(-30, 30)
        top = (summit[0] + (bx - summit[0]) * 0.05, summit[1] + 14 + rng.uniform(0, 40))
        mid = ((top[0] + bx) / 2 + rng.uniform(-14, 14), (top[1] + by) / 2 + rng.uniform(-20, 20))
        gul.append((curve([top, mid, (bx, by)], 20), rng.uniform(2.5, 5.5), (0.08, 0.5)))
    gm = strokes(W, H, gul) * cone * (1 - ygrad(W, H, 560, 720))
    art = GP(art, gm, "#45405e", seed=nx(), rough=1.4, streak=0.8)
    pl = []
    for k in range(12):
        t = k / 11
        pl.append((summit[0] + 10 + t * 140 + rng.uniform(-6, 6), summit[1] - 12 - t * 100 + t * t * 30, 8 + t * 30, 6 + t * 13, -15))
    pm = displace(ellipses(W, H, pl), nx(), 6, 14)
    art = GP(art, pm, "#efe5e0", "#d6c9d2", seed=nx(), rough=4, streak=1.0)
    art = brushwork(art, pm, ["#ffffff", "#e3d3d8"], rng, nx, n=60, L=(10, 24), wd=(3, 6), ang=-0.6, ang_var=0.3)
    clear()
    # mist across the lower flank
    mm = displace(ellipses(W, H, [(x + rng.uniform(-20, 20), 600 + rng.uniform(-22, 18), rng.uniform(40, 110), rng.uniform(7, 16), rng.uniform(-4, 4)) for x in range(-40, W + 60, 55) if rng.random() > 0.2]), nx(), 10, 18)
    art = GP(art, mm * 0.85, "#e8dbd4", "#d9cfd2", seed=nx(), rough=5, streak=1.2)
    # forest belt at the foot of the cone
    belt = []
    for _ in range(170):
        x = rng.uniform(-30, W + 30); y = 660 + rng.uniform(-24, 36)
        belt.append((x, y, rng.uniform(14, 28), rng.uniform(10, 18), 0))
    bm = np.maximum(displace(ellipses(W, H, belt), nx(), 3, 10), rect(W, H, -30, 680, W + 30, 920))
    art = GP(art, bm, "#3a563c", "#2c4634", seed=nx(), rough=3, streak=1.0)
    art = brushwork(art, bm * (1 - ygrad(W, H, 640, 720)), ["#5d7d48", "#6f8f50", "#4a6a40"], rng, nx, n=380, L=(8, 16), wd=(4, 8), ang=-0.3, ang_var=0.6)
    clear()
    # Kayu Aro tea slopes: rolling hills combed with lumpy hedgerows that follow the contour
    hills = [(860, 140, "#86b14c", "#6b9c44", 0.0), (1050, 160, "#78a646", "#5a8e3c", 1.7)]
    for hi_, (base, amp, c1, c2, ph) in enumerate(hills):
        xs = np.arange(-20, W + 21, 10)
        ys = base - amp * (0.5 + 0.5 * np.sin(xs / W * math.tau * 0.9 + ph))
        pts = [(-20, H + 20)] + list(zip(xs.tolist(), ys.tolist())) + [(W + 20, H + 20)]
        hm_ = displace(poly(W, H, pts, smooth=True), nx(), 2, 20)
        art = GP(art, hm_, c2, mix_hex(c2, "#2f5a2a", 0.3), seed=nx(), rough=2, streak=1.0)
        gaps, tops = [], []
        for r in range(1, 18):
            off = r * (14 + r * 1.5)
            row = [(x, y + off + 5 * math.sin(x / 80 + r * 0.7)) for x, y in zip(xs.tolist(), ys.tolist())]
            gaps.append(([(x, y + 5 + r * 0.5) for x, y in row], 1.0 + r * 0.22, None))
            for x, y, a in jw.along(row, 9 + r * 0.6):
                rr = 6 + r * 0.6
                tops.append(([(x - math.cos(a) * rr * 0.8, y - math.sin(a) * rr * 0.8 - rr * 0.1), (x, y - rr * 0.4), (x + math.cos(a) * rr * 0.8, y + math.sin(a) * rr * 0.8 - rr * 0.1)], rr * 0.7, (0.4, 0.4)))
        art = GP(art, strokes(W, H, gaps) * hm_, "#365a2a", seed=nx(), rough=1.0, streak=0.6)
        tm = strokes(W, H, tops) * hm_
        art = GP(art, tm * (fbm(W, H, nx(), 30, 2) > 0.35), mix_hex(c1, "#d8e07a", 0.25), seed=nx(), rough=1.2, streak=0.8)
        art = GP(art, tm * (fbm(W, H, nx(), 30, 2) > 0.62), mix_hex(c1, "#f0eaa0", 0.5), seed=nx(), rough=1.0, streak=0.8)
        clear()
        if hi_ == 0:
            # red-earth path winding over the first hill and shade trees
            path = curve([(120, 1080), (230, 1000), (330, 960), (420, 900), (500, 830), (540, 790)], 80)
            items = [(path[i:i + 2], 3 + (80 - i) * 0.14, None) for i in range(len(path) - 1)]
            art = GP(art, strokes(W, H, items) * hm_, "#b4703e", "#9a5a34", seed=nx(), rough=1.5, streak=0.8)
            for x, by, h in [(620, 905, 120), (90, 990, 140)]:
                tr = strokes(W, H, [([(x, by), (x + 4, by - h * 0.6), (x - 6, by - h)], 5, (0.0, 0.4)), ([(x + 2, by - h * 0.6), (x + 40, by - h * 0.85)], 3, (0.0, 0.5))])
                art = GP(art, tr, "#4a3a2e", seed=nx(), rough=1, streak=0.4)
                cr = displace(ellipses(W, H, [(x - 10, by - h, 50, 15, -4), (x + 38, by - h * 0.88, 30, 10, 6), (x - 44, by - h * 0.92, 28, 9, 0)]), nx(), 5, 10)
                art = GP(art, cr, "#46703a", "#3a6032", seed=nx(), rough=2.5, streak=0.8)
                art = brushwork(art, cr, ["#6d9448", "#5a8440"], rng, nx, n=60, L=(8, 16), wd=(3, 6), ang=0.0, ang_var=0.4)
            clear()
    # Danau Kerinci: far shore, water with mirrored cone and horizontal strokes
    shore = displace(poly(W, H, [(-20, 1210), (120, 1192), (300, 1204), (520, 1186), (W + 20, 1198), (W + 20, 1236), (-20, 1236)], smooth=True), nx(), 2, 16)
    art = GP(art, shore, "#4f6884", "#445c78", seed=nx(), rough=2, streak=0.8)
    water = rect(W, H, -20, 1226, W + 20, H + 20)
    art = GP(art, water, "#9ab0c6", "#86a0ba", seed=nx(), rough=1.5, streak=1.4)
    idx = np.clip((800 - (np.arange(H) - 1226) * 2.6).astype(int), 0, H - 1)
    refl = cone[idx] * water * (1 - ygrad(W, H, 1226, 1400) * 0.5) * (np.arange(H)[:, None] > 1240)
    art = GP(art, refl * 0.8, "#7d7c9e", "#6e6e92", seed=nx(), rough=2, streak=1.6)
    art = brushwork(art, water, ["#e9d6bf", "#b9c8d6", "#6f87a4", "#cfdbe4"], rng, nx, n=320, L=(30, 110), wd=(1.5, 4), ang=0.0, ang_var=0.02)
    rgb = art[..., :3]
    paperk = np.asarray(paper(W, H, "#ffffff", 9), np.float32) / 255
    rgb = rgb * (0.93 + 0.07 * paperk)
    prev_rgb(rgb, "kd-scene")
    rgb_save(rgb, f"{OUT}/scene.webp", quality=76)
    clear()


def keluk(cx, cy, s, flip=1):
    """Keluk paku: an S-scroll — two fern-frond spirals curling in opposite directions, joined by a flowing stem,
    with a small sprouting curl and leaf at the waist."""
    T = 1.2
    ra, rb = s * 0.34, s * 0.34
    ax, ay = cx - s * 0.52, cy - s * 0.1 * flip
    bx, by = cx + s * 0.52, cy + s * 0.1 * flip
    # outer end of A at its bottom (angle +pi/2), of B at its top (-pi/2)
    A = jw.spiral_pts(ax, ay, s * 0.03, ra, math.pi / 2 * flip - T * math.tau, T, 60, 1)
    B = jw.spiral_pts(bx, by, s * 0.03, rb, -math.pi / 2 * flip - T * math.tau, T, 60, 1)
    a_out, b_out = A[-1], B[-1]
    stem = curve([a_out, (cx - s * 0.15, a_out[1] + s * 0.02 * flip), (cx, cy), (cx + s * 0.15, b_out[1] - s * 0.02 * flip), b_out], 30)
    items = [(A, s * 0.085, (0.0, 0.05)), (B, s * 0.085, (0.0, 0.05)), (stem, s * 0.095, None)]
    c = jw.spiral_pts(cx + s * 0.08, cy - s * 0.22 * flip, s * 0.02, s * 0.09, 0, 0.9, 24, 1)
    items.append((curve([(cx, cy), (cx + s * 0.02, cy - s * 0.12 * flip), c[-1]], 10), s * 0.04, (0.0, 0.3)))
    items.append((c, s * 0.04, (0.0, 0.2)))
    leaves = [petal_pts(cx, cy, s * 0.24, s * 0.07, math.pi / 2 * flip + 0.6, n=8)]
    return items, leaves


def flower4(cx, cy, r):
    return [petal_pts(cx, cy, r, r * 0.42, k * math.pi / 2 + math.pi / 4, n=10) for k in range(4)]


def part_larik():
    """Carved board (papan ukir) of a rumah larik: tileable strip, keluk paku pairs alternating with four-petal flowers,
    painted ochre and red on dark wood, framed by two raised mouldings."""
    W, H = 1000, 170
    rng = random.Random(4); nx = Seq(1500)
    band = rect(W, H, 0, 0, W, H)
    items, leaves = [], []
    n = 5
    per = W / n
    for k in range(n):
        x = k * per + per / 2
        it, lv = keluk(x, H / 2, 120, 1 if k % 2 == 0 else -1)
        items += it; leaves += lv
    for k in range(n + 1):
        leaves += flower4(k * per, H / 2, 24)
    items += [([(-10, 14), (W + 10, 14)], 7, None), ([(-10, H - 14), (W + 10, H - 14)], 7, None)]
    art = jw.carve(W, H, band, items, leaves, nx, base=WOOD, light=WOOD_L, dark=WOOD_D, gold=OCHRE, gold_amt=0.0, seed=5)
    relief = np.maximum(strokes(W, H, items[:-2]), shapes(W, H, leaves))
    flowers = shapes(W, H, [p for k in range(n + 1) for p in flower4(k * per, H / 2, 24)])
    art = gp(art, np.clip(relief - flowers, 0, 1) * (0.75 + 0.25 * fbm(W, H, nx(), 14, 2)), OCHRE, "#c48f36", seed=nx(), rough=0.8, streak=0.5)
    art = gp(art, flowers, RED, "#8f2b22", seed=nx(), rough=0.8, streak=0.5)
    art = gp(art, circles(W, H, [(k * per, H / 2, 6) for k in range(n + 1)]), CREAM, seed=nx(), rough=0.6, streak=0.4)
    rails = strokes(W, H, items[-2:])
    art = gp(art, rails, "#8a5a34", seed=nx(), rough=0.8, streak=0.6)
    hi = np.clip(relief - np.roll(np.roll(relief, 2, 0), 2, 1), 0, 1)
    art = OV(art, hi, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#fff0d0"), np.float32), (m * 0.4)[..., None]], -1))
    lo = np.clip(relief - np.roll(np.roll(relief, -2, 0), -2, 1), 0, 1)
    art = OV(art, lo, lambda m: np.concatenate([np.ones(m.shape + (3,), np.float32) * np.array(hex_rgb("#1a0e08"), np.float32), (m * 0.5)[..., None]], -1))
    rgb = art[..., :3]
    prev_rgb(rgb, "kd-larik")
    rgb_save(rgb, f"{OUT}/larik.webp", quality=80, size=(600, 102))
    clear()


def part_sprig():
    """Pucuk teh: two leaves and a bud, watercolour (for dividers and timeline nodes)."""
    W, H = 300, 300
    rng = random.Random(8); nx = Seq(1900)
    art = blank(W, H)
    stem = curve([(150, 290), (148, 220), (152, 150), (150, 70)], 40)
    art = G(art, strokes(W, H, [(stem, 6, (0.0, 0.3))]), "#6a8a3a", "#4e6e30", seed=nx(), density=0.9, edge=0.4, rough=0.8, feather=0.5)
    for (x, y, L, a, c1, c2) in [(150, 200, 120, -2.55, "#5f9a3e", "#3d7a34"), (150, 160, 110, -0.6, "#79b04a", "#4f8e3a")]:
        pts = petal_pts(x, y, L, L * 0.3, a, n=18, cup=0.05)
        pts = [(px + math.sin(i * 2.1) * 1.2, py + math.cos(i * 2.1) * 1.2) for i, (px, py) in enumerate(pts)]
        m = shape_mask(W, H, pts)
        art = G(art, m, c1, c2, seed=nx(), density=0.9, edge=0.7, bloom=0.35, rough=1, feather=0.6, gran=0.3)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        art = G(art, strokes(W, H, [([(x, y), (ex, ey)], 1.6, (0.0, 0.7))]) * m, "#2c5a26", seed=nx(), density=0.5, edge=0.1, rough=0.5, feather=0.5)
    bud = shape_mask(W, H, petal_pts(150, 92, 70, 14, -math.pi / 2 + 0.08, n=14))
    art = G(art, bud, "#b6d36a", "#8fbf52", seed=nx(), density=0.92, edge=0.7, bloom=0.2, rough=0.8, feather=0.5, gran=0.3)
    art = G(art, bud * xgrad(W, H, 146, 166), "#5f9a3e", seed=nx(), density=0.4, edge=0.1, rough=0.5, feather=0.6)
    np.save(f"{PREV}/kd-sprig.npy", art)
    preview(art, "kd-sprig", tone="#efe8d6")
    save(art, f"{OUT}/sprig.webp", max_w=140, quality=84)
    clear()


def part_divider():
    """Two tea sprigs lying head to head with a small red four-petal flower between them."""
    sp = np.load(f"{PREV}/kd-sprig.npy")
    im = to_image(sp)
    W, H = 640, 270
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = im.rotate(-90, expand=True, resample=Image.BICUBIC).resize((260, 260))
    b = a.transpose(Image.FLIP_LEFT_RIGHT)
    canvas.alpha_composite(a, (W // 2 - 280, 5))
    canvas.alpha_composite(b, (W // 2 + 20, 5))
    arr = np.asarray(canvas, np.float32) / 255
    rng = random.Random(2); nx = Seq(2200)
    fl = shapes(W, H, flower4(W / 2, H / 2 - 4, 16))
    arr = G(arr, fl, RED, "#8f2b22", seed=nx(), density=0.92, edge=0.6, rough=0.8, feather=0.5)
    arr = G(arr, circles(W, H, [(W / 2, H / 2 - 4, 4.5)]), OCHRE, seed=nx(), density=0.95, edge=0.3, rough=0.4, feather=0.4)
    preview(arr, "kd-divider", tone="#f3ead7")
    save(arr, f"{OUT}/divider.webp", max_w=320, quality=84)


def part_wood():
    W = H = 320
    rng = np.random.default_rng(3)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    n1 = gaussian_filter(rng.random((H, W)).astype(np.float32), (0.8, 30), mode="wrap")
    n1 = (n1 - n1.mean()) / (n1.std() + 1e-6)
    n2 = gaussian_filter(rng.random((H, W)).astype(np.float32), (14, 50), mode="wrap")
    n2 = (n2 - n2.mean()) / (n2.std() + 1e-6)
    grain = np.sin(yy / H * math.tau * 9 + n2 * 1.6) * 0.5 + 0.5
    v = 1 + n1 * 0.05 + (grain - 0.5) * 0.10 + n2 * 0.04
    rgb = np.ones((H, W, 3), np.float32) * col_arr("#4a2a19") * v[..., None]
    prev_rgb(rgb, "kd-wood")
    rgb_save(rgb, f"{OUT}/wood.webp", quality=70)


for p in PARTS:
    globals()["part_" + p]()
kb_report(OUT)
