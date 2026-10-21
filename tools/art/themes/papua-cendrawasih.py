"""Papua Cendrawasih — gouache bird of paradise (original, Raggiana-inspired) with cascading plumes, Asmat-inspired carved
linocut band (original spirals & hooks), noken knot-mesh texture, earth red / ochre / black / cream.
Run: python3 -I papua-cendrawasih.py [part ...]   parts: bird ukir spiral noken"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _a2_lib import *

OUT = outdir("papua-cendrawasih")
PARTS = sys.argv[1:] or ["bird", "ukir", "spiral", "noken"]
RED, RED_D, OCHRE, BLACK, CREAM = "#9c3b1f", "#6a2412", "#c98a2b", "#1d1410", "#f3e6cf"


if "bird" in PARTS:
    W, H = 760, 1080
    rng = random.Random(41); nx = Seq(41000)
    art = blank(W, H)
    # ---- branch with leaves (the bird perches on it)
    br = curve([(0, 510), (200, 488), (400, 472), (600, 448), (760, 404)], 60)
    bm = strokes(W, H, [(br, 24, (0.0, 0.3)), (curve([(620, 444), (676, 392), (716, 350)], 16), 9, (0.0, 0.5)), (curve([(150, 494), (100, 450), (84, 420)], 14), 7, (0.0, 0.6))])
    art = GP(art, bm, "#5a3a22", "#2e1c10", seed=nx(), rough=1.4, streak=1.2)
    art = OV(art, strokes(W, H, [(offset_curve(br, -7)[2:-8], 3, (0.1, 0.4))]) * bm, lambda m: rgba("#93704a", m * 0.6))
    art = OV(art, strokes(W, H, hair_strokes(bm, 60, 18, 1.6, 0.0, rng, 0.2)) * bm, lambda m: rgba("#1e120a", m * 0.4))
    for (lx, ly, L, a) in [(84, 424, 120, -2.1), (716, 352, 100, -1.0), (560, 452, 90, 1.1), (120, 496, 80, 2.4)]:
        art = g_leaf(art, W, H, lx, ly, L, a, rng, nx, "#617c3c", "#33502a", vein="#b3c283", wd=0.3)
    # ---- flank plumes: bundles of long fine strokes cascading from under the wing, over the branch
    anchor = (440, 440)
    back, front, hi = [], [], []
    for b in range(17):
        t = b / 16
        L = 520 + 120 * math.sin(t * math.pi) + rng.uniform(-30, 30)
        p0 = (anchor[0] + rng.uniform(-22, 18), anchor[1] + rng.uniform(-14, 10))
        sweep = 10 + 230 * t  # rightward reach
        spine = curve([p0, (p0[0] + sweep * .55, p0[1] + L * .16), (p0[0] + sweep * .95, p0[1] + L * .42),
                       (p0[0] + sweep * .85 - 10, p0[1] + L * .72), (p0[0] + sweep * .5 - 40 + rng.uniform(-25, 25), p0[1] + L)], 70)
        for f in range(13):
            off = rng.gauss(0, 7)
            spread = rng.gauss(0, 16)
            n_ = len(spine)
            fl = [(x + nxv * (off + spread * (i / n_) ** 1.6), y + nyv * (off + spread * (i / n_) ** 1.6))
                  for i, ((x, y), (nxv, nyv)) in enumerate(zip(spine, normals(spine)))]
            cut = int(len(fl) * rng.uniform(0.72, 1.0))
            (back if b % 3 == 0 else front).append((fl[:cut], rng.uniform(1.4, 3.6), (0.02, 0.6)))
        for f in range(4):
            fl = offset_curve(spine, rng.gauss(0, 5))
            hi.append((fl[int(len(fl) * .04):int(len(fl) * rng.uniform(.45, .85))], rng.uniform(0.8, 1.5), (0.05, 0.7)))
    art = GP(art, strokes(W, H, back), "#b8441c", "#7a2a12", seed=nx(), rough=0.6, streak=1.2, pad=10)
    m_front = strokes(W, H, front)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    g = np.clip((yy - 430) / 560, 0, 1)
    art = GP(art, m_front * (1 - g * 0.92), "#f2b63c", "#e2942a", seed=nx(), rough=0.5, streak=1.2, pad=10)
    art = GP(art, m_front * np.clip(g * 1.35 - 0.12, 0, 1), "#ea6c2a", "#c44a1e", seed=nx(), rough=0.5, streak=1.2, pad=10, density=0.92)
    art = OV(art, strokes(W, H, hi), lambda m: rgba("#fff1c4", m * 0.7), pad=10)
    # ---- tail wires
    wires = []
    for k, (dx, end) in enumerate([(-40, 1060), (30, 1010)]):
        pts = curve([(456, 468), (476 + dx * .4, 640), (440 + dx, 840), (476 + dx * 1.5, end - 50), (446 + dx * 2, end)], 50)
        wires.append((pts, 2.4, (0.05, 0.1)))
        wires.append((spiral_pts(pts[-1][0] - 11, pts[-1][1] - 2, 11, 2, 0, 1.0, 30, 1 if k else -1), 3.0, (0.0, 0.6)))
    art = GP(art, strokes(W, H, wires), "#2a1a12", "#120a06", seed=nx(), rough=0.5, pad=8)
    # ---- body: maroon-brown, darker breast band, feather texture
    body_pts = [(318, 268), (366, 262), (418, 292), (462, 350), (476, 420), (462, 470), (420, 476), (372, 458), (330, 418), (306, 360), (304, 304)]
    body = shape_mask(W, H, deform(body_pts, rng, 1, 0.015))
    art = GP(art, body, "#6e3418", "#401a0c", seed=nx(), rough=1.0, streak=1.0)
    breast = shape_mask(W, H, [(300, 300), (350, 300), (360, 330), (340, 360), (306, 362)]) * body
    art = OV(art, gaussian_filter(breast, 5), lambda m: rgba("#2a0f08", m * 0.6))
    art = OV(art, strokes(W, H, hair_strokes(body, 140, 22, 2.2, lambda x, y: 1.25 + (x - 380) * 0.003, rng, 0.25)) * body, lambda m: rgba("#9a5a2e", m * 0.45))
    art = OV(art, strokes(W, H, hair_strokes(body, 90, 18, 1.8, 1.3, rng, 0.3)) * body, lambda m: rgba("#26100a", m * 0.35))
    # wing: folded, layered primaries
    wing = shape_mask(W, H, [(372, 300), (428, 296), (470, 330), (494, 396), (502, 468), (480, 484), (444, 450), (408, 392), (384, 340)])
    art = GP(art, wing, "#7c4c26", "#4a2a14", seed=nx(), rough=1.2, streak=1.2)
    prim = []
    for k in range(8):
        sx, sy = 400 + k * 9, 320 + k * 14
        prim.append(((curve([(sx, sy), (sx + 34, sy + 40), (sx + 60 - k * 2, sy + 100 - k * 6)], 14)), 3.0, (0.05, 0.4)))
    art = OV(art, strokes(W, H, prim) * wing, lambda m: rgba("#2a160a", m * 0.5))
    art = OV(art, strokes(W, H, [(curve([(404, 312), (452, 346), (480, 410)], 14), 4, (0.1, 0.5))]) * wing, lambda m: rgba("#b9844c", m * 0.6))
    # ---- head + golden mantle, emerald throat, pale bill
    head = shape_mask(W, H, deform(ellipse_pts(338, 236, 46, 40, 14, -0.3), rng, 1, 0.02))
    mantle = shape_mask(W, H, [(312, 230), (370, 210), (416, 250), (448, 300), (420, 318), (380, 300), (340, 268)])
    hm = np.maximum(head, mantle)
    art = GP(art, hm, "#f2d04c", "#d7a62a", seed=nx(), rough=1.0, streak=0.9)
    art = OV(art, strokes(W, H, hair_strokes(hm, 60, 14, 1.6, 0.6, rng, 0.3)) * hm, lambda m: rgba("#fff3a6", m * 0.5))
    throat = shape_mask(W, H, deform([(292, 240), (324, 250), (350, 274), (344, 306), (314, 312), (294, 288)], rng, 1, 0.02))
    art = GP(art, throat, "#1f6a48", "#0f3b2a", seed=nx(), rough=0.8, streak=0.8)
    art = OV(art, strokes(W, H, hair_strokes(throat, 30, 10, 1.6, 1.2, rng, 0.3)) * throat, lambda m: rgba("#6fc08c", m * 0.55))
    beak = shape_mask(W, H, [(300, 222), (252, 238), (234, 246), (252, 248), (300, 246)], smooth=False)
    art = GP(art, beak, "#bccad2", "#7d8f99", seed=nx(), rough=0.5, pad=8)
    art = OV(art, strokes(W, H, [([(298, 240), (246, 245)], 1.4, None)]), lambda m: rgba("#4b5a62", m * 0.8), pad=6)
    art = GP(art, circles(W, H, [(324, 225, 7.5)]), "#f6e27a", seed=nx(), rough=0.4, pad=6)
    art = GP(art, circles(W, H, [(325, 225, 4.3)]), "#120a06", seed=nx(), rough=0.3, pad=6)
    art = OV(art, circles(W, H, [(326.5, 223.5, 1.4)]), lambda m: rgba("#ffffff", m * 0.9), pad=4)
    art = OV(art, strokes(W, H, [(curve([(306, 206), (338, 196), (370, 210)], 12), 6, (0.1, 0.5))]), lambda m: rgba("#4a2a10", m * 0.5))
    # feet gripping the branch
    claws = []
    for fx in (368, 404):
        fy = 470 - (fx - 380) * 0.1
        claws += [([(fx, fy - 26), (fx + 2, fy - 2)], 5, (0, .3)), ([(fx + 2, fy - 2), (fx - 11, fy + 9)], 3, (0, .6)), ([(fx + 2, fy - 2), (fx + 13, fy + 8)], 3, (0, .6))]
    art = GP(art, strokes(W, H, claws), "#5a5f6a", "#23262c", seed=nx(), rough=0.4, pad=8)
    preview(art, "pc-bird", tone=CREAM)
    preview(art, "pc-bird-red", bg=RED)
    save(art, f"{OUT}/bird.webp", max_w=420, quality=82)
    clear()


def s_spiral(cx, cy, d, turns=1.3, n=60, flip=1):
    """Continuous S double-spiral (two coils joined through the centre), the core of the carved motif (original)."""
    a0 = -turns * math.tau
    s1 = [(cx - d + math.cos(a0 + t * turns * math.tau) * d * (0.12 + 0.88 * t), cy + flip * math.sin(a0 + t * turns * math.tau) * d * (0.12 + 0.88 * t)) for t in [i / (n - 1) for i in range(n)]]
    s2 = [(2 * cx - x, 2 * cy - y) for x, y in s1]
    return s1 + s2[::-1]


def unit_masks(W, H, x0, u, h, flip=1):
    """Asmat-inspired carved unit: bold S-spiral, crescent hooks top/bottom, bar pair at the right edge."""
    cx, cy = x0 + u / 2, h / 2
    d = u * 0.21
    relief = [(s_spiral(cx, cy, d, 1.25, 70, flip), u * 0.085, None)]
    for sgn in (-1, 1):
        hx = cx - sgn * d * 1.05
        relief.append((curve([(hx - d * 0.95, cy + sgn * d * 1.2), (hx, cy + sgn * d * 1.55), (hx + d * 0.95, cy + sgn * d * 1.2), (hx + d * 0.8, cy + sgn * d * 0.92)], 20), u * 0.055, (0.0, 0.45)))
    bars = [([(x0 + u - 4, h * 0.2), (x0 + u - 4, h * 0.8)], u * 0.05, None), ([(x0 + u + 4, h * 0.2), (x0 + u + 4, h * 0.8)], u * 0.05, None)]
    return relief, bars


if "ukir" in PARTS:
    # Horizontal repeat band (painted carved relief): red-ochre ground, lime-white relief with black cut lines, teeth rows.
    U = 140; N = 3; W = U * N; H = 132; PAD = U
    WW = W + 2 * PAD
    nx = Seq(42000)
    relief, bars = [], []
    for k in range(-1, N + 1):
        r_, b_ = unit_masks(WW, H, PAD + k * U, U, H, 1 if k % 2 else -1)
        relief += r_; bars += b_
    teeth = []
    for k in range(-2, 2 * N * 2 + 6):
        x = k * U / 4
        teeth.append([(x, 0), (x + U / 8, 15), (x + U / 4, 0)])
        teeth.append([(x, H), (x + U / 8, H - 15), (x + U / 4, H)])
    ground = shapes(WW, H, [[(0, 3), (WW, 3), (WW, H - 3), (0, H - 3)]], smooth=False)
    rel = strokes(WW, H, relief)
    bar = strokes(WW, H, bars)
    tm = shapes(WW, H, teeth, smooth=False)
    cut = np.clip(gaussian_filter(np.maximum(rel, bar), 1.6) * 2.4 - np.maximum(rel, bar) * 1.6, 0, 1)
    art = blank(WW, H)
    art = GP(art, ground, RED, RED_D, seed=nx(), rough=0.8, streak=1.3)
    art = LC(art, np.maximum(cut, tm), BLACK, seed=nx(), wear=0.25, rough=1.0)
    art = GP(art, rel, "#f1e4c8", "#d9c39a", seed=nx(), rough=0.8, streak=0.8)
    art = GP(art, bar, OCHRE, "#a86c1e", seed=nx(), rough=0.6)
    eyes = [(PAD + k * U + U / 2 + sx * U * 0.21, H / 2, 5) for k in range(-1, N + 1) for sx in (-1, 1)]
    art = LC(art, circles(WW, H, eyes), BLACK, seed=nx(), wear=0.1, rough=0.6)
    rules = strokes(WW, H, [([(0, 17), (WW, 17)], 2.0, None), ([(0, H - 17), (WW, H - 17)], 2.0, None)])
    art = LC(art, rules, BLACK, seed=nx(), wear=0.3, rough=0.8)
    tile = art[:, PAD:PAD + W]
    preview(tile, "pc-ukir", tone=CREAM)
    save_full(tile, f"{OUT}/ukir.webp", quality=82)
    clear()

if "spiral" in PARTS:
    # Divider/ornament: S-spiral medallion with tapering hooked arms (black linocut, red eyes).
    W, H = 520, 130
    nx = Seq(43000)
    items = [(s_spiral(W / 2, H / 2, 26, 1.25, 70, 1), 9, None)]
    for sgn in (-1, 1):
        base = W / 2 + sgn * 62
        items.append((curve([(base, H / 2), (base + sgn * 80, H / 2 - 8), (base + sgn * 160, H / 2 + 3), (base + sgn * 196, H / 2 - 1)], 30), 5, (0.0, 0.75)))
        for j in range(3):
            hx = base + sgn * (26 + j * 46)
            sc = 1 - j * 0.18
            items.append((curve([(hx, H / 2 - 4), (hx + sgn * 12 * sc, H / 2 - 26 * sc), (hx + sgn * 30 * sc, H / 2 - 26 * sc), (hx + sgn * 30 * sc, H / 2 - 13 * sc)], 12), 4.0 * sc, (0.0, 0.55)))
            items.append((curve([(hx + sgn * 8, H / 2 + 3), (hx + sgn * 20 * sc, H / 2 + 22 * sc), (hx + sgn * 36 * sc, H / 2 + 19 * sc)], 12), 3.4 * sc, (0.0, 0.6)))
    ink = strokes(W, H, items)
    art = LC(blank(W, H), ink, BLACK, seed=nx(), wear=0.22, rough=1.1)
    art = LC(art, circles(W, H, [(W / 2 - 26 * 1.0, H / 2, 6.5), (W / 2 + 26, H / 2, 6.5)]), RED, seed=nx(), wear=0.15)
    preview(art, "pc-spiral", tone=CREAM)
    save(art, f"{OUT}/spiral.webp", max_w=260, quality=84)
    clear()

if "noken" in PARTS:
    # Noken knot-mesh: rows of interlocked loops in bark-fibre string, with a dyed red/ochre stripe; seamless tile.
    T = 240
    nx = Seq(44000); rng = random.Random(44)
    WW = T * 2
    loops = []
    cell = 30
    for r in range(-1, T // 20 * 2 + 2):
        y = r * 20
        off = (r % 2) * cell / 2
        for c in range(-1, WW // cell + 2):
            x = c * cell + off
            pts = curve([(x - cell / 2, y), (x - cell * .28, y + 15), (x, y + 21), (x + cell * .28, y + 15), (x + cell / 2, y)], 18)
            loops.append(([(px + rng.gauss(0, .5), py + rng.gauss(0, .5)) for px, py in pts], 3.2, None))
    m = strokes(WW, WW, loops)
    knots = [(c * cell + (r % 2) * cell / 2 + cell / 2, r * 20 + 1, 3.6) for r in range(-1, T // 20 * 2 + 2) for c in range(-1, WW // cell + 2)]
    m = np.maximum(m, circles(WW, WW, knots))
    twist = hatch(WW, WW, 0.9, 3.2, 0.35, 7, 0.4)
    # use the centre T x T of a larger canvas so loops wrap (pattern period divides T)
    yy, xx = np.mgrid[0:WW, 0:WW]
    stripe = (((yy // 20) % 6) == 2).astype(np.float32)
    bg = solid(WW, WW, "#2a1a12")
    bg[..., :3] *= (0.85 + 0.3 * wrap_noise(WW, WW, 3, 6.0))[..., None]
    fib = gaussian_filter(np.random.default_rng(5).random((WW, WW)).astype(np.float32), (0.4, 1.8))
    fib = (fib - fib.mean()) / (fib.std() + 1e-6)
    base_col = np.array(hex_rgb("#b98d5a"), np.float32) * (1 - stripe[..., None]) + np.array(hex_rgb("#a8401e"), np.float32) * stripe[..., None]
    shade = gaussian_filter(m, 1.2)
    col = base_col * (0.75 + 0.35 * shade[..., None]) * (1 + fib[..., None] * 0.08) * (1 - 0.22 * twist[..., None])
    a = np.clip(m * 1.1, 0, 1)[..., None]
    rgb = bg[..., :3] * (1 - a) + col * a
    rgb *= (1 - 0.35 * np.clip(gaussian_filter(m, 2.5) - m, 0, 1))[..., None]  # shadow under strings
    tile = np.concatenate([np.clip(rgb, 0, 1), np.ones((WW, WW, 1), np.float32)], -1)[60:60 + T, 60:60 + T]
    # period check: loops repeat every 2 rows (40px) and every cell (30px) -> 240 divisible by both.
    preview(tile, "pc-noken")
    save_full(tile, f"{OUT}/noken.webp", quality=72)
    clear()
