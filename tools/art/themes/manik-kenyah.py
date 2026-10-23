"""Manik Kenyah — Dayak Kenyah beadwork (Kalimantan Utara/Timur): bead-by-bead panels with curling aso/kalung vines and
hornbill heads in yellow, black, white, red and blue; a lamin longhouse with painted gable murals on the river.
Run: python3 -I manik-kenyah.py [part ...]  parts: panel strip fringe medal ring lamin divider
Assets -> public/themes/art/manik-kenyah/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _m1_lib import *

OUT = outdir("manik-kenyah")
PARTS = sys.argv[1:] or ["panel", "strip", "fringe", "medal", "ring", "lamin", "divider"]
BLACK, YEL, WHITE, RED, BLUE, GREEN = "#16110e", "#e8b52a", "#efe8d8", "#b5322a", "#2b5ba8", "#2f7a5a"


def scroll(cx, cy, r, a0, d, turns=1.25, n=48):
    return spiral_pts(cx, cy, r, r * 0.16, a0, turns, n, d)


def attach(sp, at):
    return [(px + (at[0] - sp[0][0]), py + (at[1] - sp[0][1])) for px, py in sp]


def aso_half(W, H):
    """Left half of the panel's kalung design (mirrored later): a hornbill head with a red curling casque (beak to the
    left edge), its neck flowing into the centre stem, two big aso vine curls with side hooks and tendrils."""
    S = W / 620
    P = lambda x, y: (x * S, y * S)
    yel, core, red, eyes, blue = [], [], [], [], []
    cx = W / 2
    yel.append((curve([P(310, 90), P(304, 480), P(310, 780)], 40), 26 * S, (0.0, 0.0)))
    # top tier: a smaller curl pair rising from the stem head (vertical mirror of the big curls)
    arm = curve([P(306, 96), P(250, 86), P(150, 92)], 30)
    sp = spiral_pts(150 * S, 176 * S, 84 * S, 84 * S * 0.3, -math.pi / 2, 1.15, 70, -1)
    path = arm + sp[1:]
    yel.append((path, 24 * S, (0.0, 0.3)))
    core.append((path[8:-16], 7 * S, (0.0, 0.2)))
    eyes.append((sp[-1][0], sp[-1][1], 11 * S))
    lp = sp[int(0.217 * (len(sp) - 1))]
    hk = attach(spiral_pts(0, 0, 18 * S, 4 * S, math.pi / 2, 1.1, 28, 1), (lp[0] - 22 * S, lp[1] - 58 * S))
    yel.append((curve([lp, (lp[0] - 20 * S, lp[1] - 28 * S), (lp[0] - 22 * S, lp[1] - 58 * S)], 10) + hk[1:], 13 * S, (0.0, 0.5)))
    red.append((curve([P(306, 40), P(306, 70)], 6), 1, None))
    head = [diamond(310 * S, 300 * S, 34 * S, 40 * S)]
    split = [P(0, 0), P(1, 1)]
    blue.append((P(250, 250)[0], P(250, 250)[1], 12 * S))
    # big curls
    for (sy, rcx, rcy, r) in [(486, 150, 404, 104), (716, 150, 640, 96)]:
        arm = curve([P(306, sy), P(250, sy + 8), P(rcx, (rcy + r))], 30)
        sp = spiral_pts(rcx * S, rcy * S, r * S, r * S * 0.3, math.pi / 2, 1.15, 80, 1)
        path = arm + sp[1:]
        yel.append((path, 26 * S, (0.0, 0.3)))
        core.append((path[8:-18], 7 * S, (0.0, 0.2)))
        eyes.append((sp[-1][0], sp[-1][1], 12 * S))
        def at(frac):
            return sp[int(frac * (len(sp) - 1))]
        # outward hook up-right from the top of the curl (lower tier only)
        if rcy > 500:
            tp = at(0.435)
            end = (tp[0] + 62 * S, tp[1] - 52 * S)
            hk = attach(spiral_pts(0, 0, 22 * S, 5 * S, math.pi, 1.1, 30, 1), end)
            yel.append((curve([tp, (tp[0] + 36 * S, tp[1] - 20 * S), end], 10) + hk[1:], 15 * S, (0.0, 0.5)))
            eyes.append((hk[-1][0], hk[-1][1], 7 * S))
        # hook down-left from the left side
        lp = at(0.217)
        end2 = (lp[0] - 26 * S, lp[1] + 66 * S)
        hk2 = attach(spiral_pts(0, 0, 18 * S, 4 * S, -math.pi / 2, 1.1, 28, -1), end2)
        yel.append((curve([lp, (lp[0] - 22 * S, lp[1] + 30 * S), end2], 10) + hk2[1:], 13 * S, (0.0, 0.5)))
        # tendril from the arm toward the centre space
        ap = arm[len(arm) // 2]
        end3 = (ap[0] + 10 * S, ap[1] + 44 * S)
        hk3 = attach(spiral_pts(0, 0, 14 * S, 4 * S, -math.pi / 2, 1.0, 24, 1), end3)
        yel.append((curve([ap, end3], 6) + hk3[1:], 11 * S, (0.0, 0.5)))
        blue.append((rcx * S + 108 * S, rcy * S - 90 * S, 13 * S))
    blue += [(P(40, 320)[0], P(40, 320)[1], 13 * S), (P(40, 560)[0], P(40, 560)[1], 13 * S), (P(250, 330)[0], P(250, 330)[1], 12 * S)]
    return dict(yel=strokes(W, H, yel), core=strokes(W, H, core), red=strokes(W, H, red), head=shapes(W, H, head, smooth=False),
                split=np.zeros((H, W), np.float32), eyes=eyes, blue=blue)


def panel():
    W, H = 620, 800
    PX, PY = 11.0, 9.2
    m = aso_half(W, H)
    head = mirror_mask(m["head"])
    yel = mirror_mask(np.maximum(m["yel"], m["head"]))
    red = mirror_mask(m["red"])
    core = mirror_mask(m["core"])
    split = mirror_mask(m["split"])
    eye_w = mirror_mask(circles(W, H, [(x, y, r) for x, y, r in m["eyes"]]))
    eye_k = mirror_mask(circles(W, H, [(x, y, r * 0.45) for x, y, r in m["eyes"]]))
    dots = mirror_mask(np.maximum(shapes(W, H, [diamond(x, y, r, r * 1.2) for x, y, r in m["blue"]], smooth=False),
                                  shapes(W, H, [diamond(W * 0.5, y, 20, 24) for y in (330, 560)], smooth=False)))
    body = np.maximum.reduce([yel, red])
    white = outline(np.maximum(body, eye_w), 6)
    frame = np.zeros((H, W), np.float32)
    frame[:20, :] = 1; frame[-20:, :] = 1; frame[:, :20] = 1; frame[:, -20:] = 1
    chain_r, chain_b = [], []
    for i, x in enumerate(np.arange(36, W - 26, 30)):
        (chain_r if i % 2 else chain_b).append(diamond(x, 30, 11, 8))
        (chain_b if i % 2 else chain_r).append(diamond(x, H - 30, 11, 8))
    chain_r = shapes(W, H, chain_r, smooth=False); chain_b = shapes(W, H, chain_b, smooth=False)
    inner_line = np.zeros((H, W), np.float32); inner_line[42:47, 18:-18] = 1; inner_line[-47:-42, 18:-18] = 1
    inner_line[18:-18, 18:23] = 1; inner_line[18:-18, -23:-18] = 1
    layers = [(eye_k, BLACK), (eye_w, WHITE), (chain_r, RED), (chain_b, BLUE), (frame, YEL), (inner_line, WHITE),
              (split * head, BLACK), (red, RED), (core, RED), (yel, YEL), (dots, BLUE), (white, WHITE)]
    arr = bead_pattern(W, H, PX, PY, layers, BLACK, seed=5)
    keep = np.zeros((H, W), np.float32); keep[2:-2, 2:-2] = 1
    arr = over(flat(keep, "#120d0a"), arr)
    arr = add_grain(arr, 7, 0.03)
    preview(arr, "mk-panel", bg="#0e0a08")
    save(arr, f"{OUT}/panel.webp", max_w=580, quality=78)


def strip():
    """Seamless horizontal bead band (repeat-x): yellow edges, diamond chain in red/blue on black, white zigzag."""
    PX, PY = 12.0, 10.0
    N = 24
    W = int(PX * N); H = int(PY * 6)
    Wb = W * 3
    zz = []
    for i in range(N * 3 + 2):
        x = i * PX * 2
        zz.append((x, PY * 1.5 if i % 2 == 0 else PY * 4.5))
    zig = strokes(Wb, H, [(zz, 9, None)])
    dia_r = shapes(Wb, H, [diamond(PX * 2 + i * PX * 4, PY * 3, PX * 1.3, PY * 1.3) for i in range(N)], smooth=False)
    dia_b = shapes(Wb, H, [diamond(i * PX * 4, PY * 3, PX * 1.3, PY * 1.3) for i in range(N)], smooth=False)
    edge = np.zeros((H, Wb), np.float32); edge[:int(PY), :] = 1; edge[-int(PY):, :] = 1
    layers = [(edge, YEL), (dia_r, RED), (dia_b, BLUE), (zig, WHITE)]
    beads = []
    for (x, y, r, c) in bead_grid(Wb, H, PX, PY, True):
        hx = BLACK
        for mm, col in layers:
            if sample(mm, x, y) > 0.5:
                hx = col; break
        beads.append((x, y, PX, PY, hx))
    arr = render_beads(Wb, H, beads, seed=11, ground=True)
    tile = arr[:, W:2 * W].copy()
    save_full(tile, f"{OUT}/strip.webp", quality=82)


def fringe():
    """Hanging bead strands (rumbai) with yellow/white/red/blue repeats ending in a tassel cone; for the cover foot."""
    W, H = 640, 170
    rng = random.Random(4)
    beads = []
    PX = 9.0
    seq = [YEL, YEL, BLACK, WHITE, WHITE, BLACK, RED, BLACK, BLUE, BLACK]
    xs = np.arange(PX, W - PX, PX * 1.12)
    for i, x in enumerate(xs):
        L = 92 + 40 * (0.5 + 0.5 * math.cos(i / len(xs) * math.tau * 3)) + rng.uniform(-6, 6)
        sway = rng.uniform(-3, 3)
        y = 6
        k = i % 3
        while y < L:
            t = y / L
            beads.append((x + sway * t * t, y, PX, PX * 0.95, seq[(int(y // PX) + k) % len(seq)]))
            y += PX * 0.98
        # end bead + small drop
        beads.append((x + sway, y + 3, PX * 1.4, PX * 1.6, RED if i % 2 else YEL))
    arr = render_beads(W, H, beads, seed=12, ground=False, size=(0.9, 0.9))
    # top bar (beaded band)
    save(arr, f"{OUT}/fringe.webp", max_w=640, quality=80)


def radial_beads(W, H, cx, cy, rings, colour_fn, seed):
    beads = []
    for (r, bs) in rings:
        n = max(6, int(math.tau * r / (bs * 1.02)))
        for j in range(n):
            a = j / n * math.tau
            x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            beads.append((x, y, bs, bs * 0.92, colour_fn(r, a, j, n)))
    return render_beads(W, H, beads, seed=seed, ground=False, size=(0.92, 0.92))


def hornbill_masks(W, H, ox, oy, s):
    """Kenyalang (hornbill) head in profile facing right: white head, yellow down-curved beak with a black split,
    red casque curling up at the front, black eye in a yellow ring, a yellow aso curl for the neck feathers."""
    P = lambda x, y: (ox + x * s, oy + y * s)
    head = shapes(W, H, [ellipse_pts(*P(0, 0), 38 * s, 34 * s, 18)])
    beak = shapes(W, H, [curve([P(14, -26), P(70, -22), P(118, 4), P(150, 62)], 30) + curve([P(150, 62), P(110, 30), P(64, 16), P(16, 18)], 30)])
    split = strokes(W, H, [(curve([P(24, -2), P(70, 2), P(108, 20), P(140, 52)], 24), 6 * s, (0.1, 0.3))])
    cas = curve([P(-6, -30), P(40, -46), P(92, -42), P(122, -30)], 24)
    cs = attach(spiral_pts(0, 0, 24 * s, 6 * s, math.pi * 0.5, 1.05, 30, -1), cas[-1])
    casque = strokes(W, H, [(cas + cs[1:], 24 * s, (0.05, 0.4))])
    neck = curve([P(-20, 26), P(-34, 70), P(-20, 104)], 20)
    sp = attach(spiral_pts(0, 0, 40 * s, 10 * s, math.pi, 1.1, 50, -1), neck[-1])
    feather = strokes(W, H, [(neck + sp[1:], 22 * s, (0.0, 0.4)),
                             (attach(spiral_pts(0, 0, 22 * s, 6 * s, 0, 1.0, 30, 1), P(-36, 40)), 12 * s, (0.0, 0.5))])
    eye_r = circles(W, H, [(*P(-2, -6), 13 * s)])
    eye_k = circles(W, H, [(*P(-2, -6), 6 * s)])
    return dict(head=head, beak=beak, split=split, casque=casque, feather=feather, eye_r=eye_r, eye_k=eye_k)


def medal():
    """Round bead medallion with a hornbill head (kenyalang) in profile, white/yellow rims."""
    W = H = 300
    cx = cy = 150
    hb = hornbill_masks(W, H, 108, 126, 0.98)
    body = np.maximum.reduce([hb["head"], hb["beak"], hb["casque"], hb["feather"]])
    wh = outline(body, 5)
    disc = circles(W, H, [(cx, cy, 128)])
    rim = np.clip(disc - circles(W, H, [(cx, cy, 117)]), 0, 1)
    rim2 = np.clip(circles(W, H, [(cx, cy, 117)]) - circles(W, H, [(cx, cy, 109)]), 0, 1)
    dots = circles(W, H, [(cx + math.cos(a) * 95, cy + math.sin(a) * 95, 7) for a in (-2.4, 2.2, 0.9)])
    layers = [(rim, YEL), (rim2, WHITE), (hb["eye_k"], BLACK), (hb["eye_r"], YEL), (hb["split"] * hb["beak"], BLACK),
              (hb["casque"], RED), (hb["beak"], YEL), (hb["head"], WHITE), (hb["feather"], YEL), (wh, WHITE), (dots, BLUE)]
    PX = 8.6

    def fn(r, a, j, n):
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        for mm, col in layers:
            if sample(mm, x, y) > 0.5:
                return col
        return BLACK
    rings = [(r, PX) for r in np.arange(PX * 0.6, 128, PX * 0.9)]
    arr = radial_beads(W, H, cx, cy, rings, fn, 21)
    arr = over(flat(circles(W, H, [(cx, cy, 131)]), "#120d0a"), arr)
    preview(arr, "mk-medal", bg="#efe2c2")
    save(arr, f"{OUT}/medal.webp", max_w=260, quality=82)


def ring():
    """Beaded ring frame for the round portraits: yellow/black/white band with red and blue spacer blocks."""
    W = H = 420
    cx = cy = 210

    def fn(r, a, j, n):
        seg = int(a / math.tau * 24)
        if r > 196 or r < 168:
            return YEL
        if r > 186:
            return WHITE if seg % 2 else BLACK
        if r > 177:
            return (RED if seg % 4 == 0 else BLUE if seg % 4 == 2 else BLACK)
        return WHITE if seg % 2 == 0 else BLACK
    rings = [(r, 10.0) for r in np.arange(162, 204, 9.2)]
    arr = radial_beads(W, H, cx, cy, rings, fn, 31)
    preview(arr, "mk-ring", bg="#efe2c2")
    save(arr, f"{OUT}/ring.webp", max_w=400, quality=82)


def divider():
    """Short bead strand divider: tapering yellow/black string with a small diamond medallion in the middle."""
    W, H = 360, 64
    beads = []
    PX = 10.5
    for i, x in enumerate(np.arange(10, W - 10, PX)):
        d = abs(x - W / 2)
        if d < 26:
            continue
        y = H / 2 + math.sin(x / 40) * 1.2
        col = [YEL, BLACK, WHITE, BLACK][i % 4] if d > 60 else [RED, BLACK, BLUE, BLACK][i % 4]
        s = PX * (1 - 0.35 * (d / (W / 2)) ** 2)
        beads.append((x, y, s, s * 0.9, col))
    # diamond medallion of beads
    for r in range(-3, 4):
        for c in range(-3 + abs(r), 4 - abs(r)):
            x = W / 2 + c * PX * 1.05; y = H / 2 + r * PX * 0.95
            col = RED if (r == 0 and c == 0) else (YEL if abs(r) + abs(c) >= 2 else WHITE)
            beads.append((x, y, PX, PX * 0.9, col))
    arr = render_beads(W, H, beads, seed=41, ground=False, size=(0.92, 0.9))
    save(arr, f"{OUT}/divider.webp", max_w=320, quality=84)


def lamin():
    """Lamin longhouse on stilts by the river at morning: misty forest hills, the gable painted with big aso murals,
    a long wooden canoe on the water. Gouache + watercolour."""
    W, H = 760, 430
    rng = random.Random(9); nx = Seq(900)
    sky = painted_sky(W, H, [(0, "#f1e3c4"), (0.45, "#e9d9b8"), (0.62, "#c9cdb5"), (1, "#8fa39a")], seed=3, streak=0.7)
    art = sky
    # far hills / forest layers
    for k, (y, amp, ca, cb, dens) in enumerate([(0.30, 40, "#9fae98", "#8a9e8c", 0.7), (0.40, 30, "#6f8a72", "#5d7a64", 0.85),
                                                (0.50, 22, "#3f5e47", "#2f4c3a", 0.95)]):
        hl = hills(W, H, H * y, amp, 30 + k, 0.45 + k * 0.1)
        hl = hl * (np.arange(H)[:, None] < H * 0.70)
        art = G(art, hl, ca, cb, seed=nx(), density=dens, edge=0.35, bloom=0.4, rough=9)
        # tree crowns on the ridge
        crowns = []
        for x in range(-10, W + 10, 16):
            yy = H * y - amp * 0.4 + rng.uniform(-12, 6)
            crowns.append(deform(ellipse_pts(x, yy, rng.uniform(10, 18), rng.uniform(8, 14), 9), rng, 1, 0.12))
        cm = shapes(W, H, crowns) * (np.arange(H)[:, None] < H * 0.70)
        art = G(art, cm, cb, mix(cb, "#2a3d2c", 0.3), seed=nx(), density=dens * 0.8, edge=0.5, bloom=0.3, rough=4)
    # mist band
    mist = np.zeros((H, W), np.float32); mist[int(H * 0.5):int(H * 0.62), :] = 1
    mist = gaussian_filter(mist, 14) * (0.6 + 0.4 * fbm(W, H, 5, 60, 3))
    art = over(art, rgba(np.ones((H, W, 3), np.float32) * col3("#efe7d2"), mist * 0.4))
    # tall forest trees behind the longhouse
    trees = []
    for x in [W * 0.05, W * 0.3, W * 0.47, W * 0.66, W * 0.93]:
        th = rng.uniform(H * 0.3, H * 0.4); by = H * 0.6
        trees.append(([(x, by), (x + rng.uniform(-6, 6), by - th)], rng.uniform(7, 10), (0.0, 0.3)))
    art = GP(art, strokes(W, H, trees), "#2d3b2f", seed=nx(), rough=1.2)
    crowns = []
    for (x, y) in [(W * 0.05, H * 0.22), (W * 0.3, H * 0.2), (W * 0.47, H * 0.26), (W * 0.66, H * 0.18), (W * 0.93, H * 0.24)]:
        for _ in range(5):
            crowns.append(deform(ellipse_pts(x + rng.gauss(0, 26), y + rng.gauss(0, 10), rng.uniform(22, 38), rng.uniform(12, 20), 10), rng, 2, 0.12))
    art = G(art, shapes(W, H, crowns), "#3d5a45", "#283e30", seed=nx(), density=0.92, edge=0.55, bloom=0.35, rough=5)
    # river
    river = np.zeros((H, W), np.float32); river[int(H * 0.68):, :] = 1
    art = G(art, river, "#8ea79f", "#5f7f7a", seed=nx(), density=0.85, edge=0.2, bloom=0.3, rough=3)
    ripples = strokes(W, H, [([(x, y), (x + rng.uniform(30, 80), y + rng.uniform(-1, 1))], rng.uniform(1.2, 2.4), (0.3, 0.3))
                             for x, y in [(rng.uniform(-20, W), rng.uniform(H * 0.72, H)) for _ in range(70)]])
    art = OV(art, ripples, lambda mm: rgba(np.ones(mm.shape + (3,), np.float32) * col3("#e9e2cc"), mm * 0.5))
    # lamin
    bx0, bx1 = W * 0.16, W * 0.88
    floor_y, eave_y, ridge_y = H * 0.61, H * 0.44, H * 0.26
    gx0, gx1 = bx0 - 30, bx0 + 120
    stilts = [([(x, floor_y), (x + rng.uniform(-2, 2), H * 0.72)], 7, None) for x in np.arange(bx0 - 10, bx1, 34)]
    st = strokes(W, H, stilts)
    art = GP(art, st, "#4a3424", "#3a2819", seed=nx(), rough=1.5, streak=0.8)
    wall = shapes(W, H, [[(bx0, eave_y), (bx1, eave_y), (bx1, floor_y), (bx0, floor_y)]], smooth=False)
    art = GP(art, wall, "#7a5638", "#5f4029", seed=nx(), rough=1.5, streak=1.0)
    planks = strokes(W, H, [([(x, eave_y + 4), (x, floor_y - 2)], 1.2, None) for x in np.arange(bx0 + 8, bx1, 9)])
    art = G(art, planks * wall, "#3b2818", seed=nx(), density=0.45, edge=0, bloom=0, rough=0.6, feather=0.5)
    # windows
    wins = shapes(W, H, [[(x, eave_y + 16), (x + 22, eave_y + 16), (x + 22, eave_y + 40), (x, eave_y + 40)] for x in np.arange(bx0 + 170, bx1 - 30, 70)], smooth=False)
    art = GP(art, wins, "#22170f", seed=nx(), rough=1.0)
    # mural band along the long wall (white curls on black)
    band = shapes(W, H, [[(bx0 + 150, eave_y + 48), (bx1 - 10, eave_y + 48), (bx1 - 10, floor_y - 6), (bx0 + 150, floor_y - 6)]], smooth=False)
    art = GP(art, band, "#1d1612", seed=nx(), rough=1.0, streak=0.5)
    curls = []
    for k, x in enumerate(np.arange(bx0 + 170, bx1 - 20, 30)):
        d = 1 if k % 2 else -1
        curls.append((spiral_pts(x, eave_y + 56, 8, 2, math.pi / 2 * d, 1.0, 24, d), 3, (0.0, 0.5)))
    art = GP(art, strokes(W, H, curls) * band, "#efe6d4", YEL, seed=nx(), rough=0.6, streak=0.3)
    # long roof (ironwood shingles)
    roof = shapes(W, H, [[(bx0 + 40, ridge_y + 16), (bx1 + 22, ridge_y + 26), (bx1 + 34, eave_y + 6), (bx0 - 6, eave_y + 2)]], smooth=False)
    art = GP(art, roof, "#5b4a3c", "#3e3229", seed=nx(), rough=2, streak=1.2)
    shing = strokes(W, H, [([(bx0, y), (bx1 + 30, y + 8)], 1.0, None) for y in np.arange(ridge_y + 24, eave_y, 7)])
    art = G(art, shing * roof, "#2b221c", seed=nx(), density=0.4, edge=0, bloom=0, rough=0.5, feather=0.5)
    # gable end with mural (facing viewer, left)
    gab = [(gx0, eave_y + 6), ((gx0 + gx1) / 2, ridge_y - 18), (gx1, eave_y + 6), (gx1, floor_y), (gx0, floor_y)]
    gm = shapes(W, H, [gab], smooth=False)
    art = GP(art, gm, "#1d1612", "#2a201a", seed=nx(), rough=1.4, streak=0.7)
    mcx, mcy = (gx0 + gx1) / 2, (eave_y + floor_y) / 2 - 12
    mur = []
    for side in (-1, 1):
        for k, (dy, r) in enumerate([(-26, 20), (12, 24), (40, 14)]):
            sp = scroll(mcx + side * 34, mcy + dy, r, math.pi / 2 * (1 + side), side, 1.2, 34)
            mur.append((sp, 6, (0.0, 0.5)))
    mur.append(([(mcx, ridge_y), (mcx, floor_y - 4)], 6, None))
    mm = strokes(W, H, mur) * gm
    art = GP(art, outline(mm, 2.5) * gm, "#efe6d4", seed=nx(), rough=0.8, streak=0.4)
    art = GP(art, mm, YEL, "#d89f22", seed=nx(), rough=0.8, streak=0.4)
    art = GP(art, circles(W, H, [(mcx, mcy - 52, 7), (mcx - 24, floor_y - 12, 4), (mcx + 24, floor_y - 12, 4)]) * gm, RED, seed=nx(), rough=0.5)
    # gable horns (ridge finials)
    gt = ((gx0 + gx1) / 2, ridge_y - 18)
    horns = strokes(W, H, [([gt, (gt[0] - 14, gt[1] - 26), (gt[0] - 20, gt[1] - 34)], 5, (0.0, 0.5)),
                           ([gt, (gt[0] + 14, gt[1] - 26), (gt[0] + 20, gt[1] - 34)], 5, (0.0, 0.5))])
    art = GP(art, horns, "#1d1612", seed=nx(), rough=1)
    # log stair + landing
    stair = strokes(W, H, [([(gx1 + 40, H * 0.73), (gx1 + 8, floor_y + 2)], 8, None)])
    art = GP(art, stair, "#5a3f29", seed=nx(), rough=1.2)
    # reflections
    refl = np.zeros_like(river)
    sl = art[int(H * 0.40):int(H * 0.68)][::-1]
    hh = min(sl.shape[0], H - int(H * 0.68))
    rr = sl[:hh].copy()
    rr[..., :3] = rr[..., :3] * 0.7 + col3("#6f8c86") * 0.3
    ripple = (fbm(W, hh, 13, (4), 2) - 0.5)
    rr[..., 3] = 0.42 * (1 - np.linspace(0, 1, hh)[:, None]) * (0.8 + ripple * 0.6)
    part = art[int(H * 0.68):int(H * 0.68) + hh]
    art[int(H * 0.68):int(H * 0.68) + hh] = over(part, rr)
    # long canoe
    boat = shapes(W, H, [curve([(W * 0.52, H * 0.84), (W * 0.62, H * 0.865), (W * 0.82, H * 0.86), (W * 0.9, H * 0.83),
                                (W * 0.86, H * 0.875), (W * 0.62, H * 0.885), (W * 0.52, H * 0.84)], 40)])
    art = GP(art, boat, "#3a2a1e", "#5a3f29", seed=nx(), rough=1)
    art = G(art, strokes(W, H, [([(W * 0.55, H * 0.855), (W * 0.86, H * 0.85)], 2.2, None)]), YEL, seed=nx(), density=0.8, edge=0.2, bloom=0, rough=0.5)
    blades = []
    for side, x0 in ((1, -10), (-1, W + 10)):
        for _ in range(26):
            bx = x0 + side * rng.uniform(0, 120); L = rng.uniform(50, 120)
            a = -math.pi / 2 + side * rng.uniform(0.1, 0.8)
            blades.append(([(bx, H + 4), (bx + math.cos(a) * L * 0.5, H - L * 0.55), (bx + math.cos(a) * L, H + math.sin(a) * L * 0.9)], rng.uniform(3, 6), (0.05, 0.6)))
    art = G(art, strokes(W, H, blades), "#3e5a3c", "#26382a", seed=nx(), density=0.9, edge=0.4, bloom=0.2, rough=2)
    art = add_grain(art, 3, 0.03)
    preview(art, "mk-lamin")
    save_rgb(art, f"{OUT}/lamin.webp", size=(720, int(720 * H / W)), quality=78)


for p in PARTS:
    globals()[p]()
    clear()
