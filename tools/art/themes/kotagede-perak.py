"""Kotagede Perak — silver filigree (Kotagede craft): oval brooch medallion of twisted rope + coiled-wire teardrop cells
and granules, filigree corner sprays, filigree divider with rosette, small 8-petal filigree flower, and a grey-teal
watercolour of a Kotagede alley (kalang-house facades). Run: python3 -I kotagede-perak.py [part ...]
parts: bros sudut garis kembang gang. Assets -> public/themes/art/kotagede-perak/"""
import sys
sys.path.insert(0, "/tmp/pen/art/themes")
from _h2_lib import *

OUT = outdir("kotagede-perak")
PARTS = sys.argv[1:] or ["bros", "sudut", "garis", "kembang", "gang"]
PAPER = "#eef0ec"


def rope(items, pts, width, step, twist=0.9):
    """Twisted rope wire: base stroke + short diagonal ticks."""
    items.append((pts, width, None))
    for x, y, a in along(pts, step):
        L = width * 0.9
        items.append(([(x - math.cos(a + twist) * L, y - math.sin(a + twist) * L), (x + math.cos(a + twist) * L, y + math.sin(a + twist) * L)], width * 0.42, None))


def cell(items, cx, cy, L, Wd, ang, wire, flip=1):
    """Teardrop cell outlined in wire and packed with a coil."""
    items.append((teardrop(cx, cy, L, Wd, ang), wire, None))
    # coil sits in the round end of the drop (petal_pts base is at (cx,cy), tip along ang)
    bx, by = cx + math.cos(ang) * L * 0.36, cy + math.sin(ang) * L * 0.36
    items.append((coil(bx, by, Wd * 0.62, 2.4, ang, d=flip), wire * 0.8, None))
    items.append(([(bx + math.cos(ang) * Wd * 0.62, by + math.sin(ang) * Wd * 0.62), (cx + math.cos(ang) * L * 0.92, cy + math.sin(ang) * L * 0.92)], wire * 0.7, None))


def rosette(items, dots, cx, cy, r, petals, wire, rot=0.0):
    for k in range(petals):
        a = rot + k / petals * math.tau
        cell(items, cx + math.cos(a) * r * 0.18, cy + math.sin(a) * r * 0.18, r * 0.9, r * 0.36, a, wire, 1 if k % 2 else -1)
    items.append((oval_pts(cx, cy, r * 0.2, r * 0.2, 40), wire, None))
    dots.append((cx, cy, r * 0.11))
    for k in range(petals):
        a = rot + (k + 0.5) / petals * math.tau
        dots.append((cx + math.cos(a) * r * 0.72, cy + math.sin(a) * r * 0.72, wire * 0.9))


def plate(W, H, region, seed):
    """Oxidised (blackened) silver ground plate the open wirework sits on."""
    art = blank(W, H)
    art = OV(art, region, lambda q: silver(q, seed=seed, tarnish=0.9, round_=3.0, strength=2.0, warm=0.1), pad=8)
    art[..., :3] *= 0.42
    return art


def paint_silver(W, H, items, dots, seed, tarnish=0.35, base=None):
    m = np.maximum(strokes(W, H, items), circles(W, H, dots) if dots else 0)
    art = blank(W, H) if base is None else base
    art = drop(art, m, blur=2.5, dx=2, dy=3, strength=0.5)
    art = SV(art, m, seed=seed, tarnish=tarnish, warm=0.25)
    return art, m


if "bros" in PARTS:
    W, H = 600, 780
    cx, cy, A, B = W / 2, H / 2 + 6, 236, 318
    items, dots = [], []
    rope(items, oval_pts(cx, cy, A, B, 240), 8.0, 8.0)
    items.append((oval_pts(cx, cy, A - 12, B - 12, 240), 4.4, None))
    items.append((oval_pts(cx, cy, A - 64, B - 64, 240), 4.4, None))
    rope(items, oval_pts(cx, cy, A - 73, B - 73, 240), 5.0, 6.0, -0.9)
    # band of radial teardrop cells between the two ovals, alternating in/out
    n = 34
    for k in range(n):
        t = k / n * math.tau
        px, py = cx + math.cos(t) * (A - 38), cy + math.sin(t) * (B - 38)
        nxv, nyv = math.cos(t) / A, math.sin(t) / B
        ang = math.atan2(nyv, nxv)
        if k % 2:
            cell(items, px - math.cos(ang) * 17, py - math.sin(ang) * 17, 36, 15, ang, 3.0, 1)
        else:
            cell(items, px + math.cos(ang) * 17, py + math.sin(ang) * 17, 36, 15, ang + math.pi, 3.0, -1)
        # S-scroll filling the gap to the next cell
        t2 = (k + 0.5) / n * math.tau
        qx, qy = cx + math.cos(t2) * (A - 38), cy + math.sin(t2) * (B - 38)
        tg = math.atan2(math.cos(t2) * B, -math.sin(t2) * A)
        r_ = 8.5
        items.append((coil(qx + math.cos(tg + 1.57) * r_, qy + math.sin(tg + 1.57) * r_, r_, 1.5, tg, d=1), 2.4, None))
        items.append((coil(qx - math.cos(tg + 1.57) * r_, qy - math.sin(tg + 1.57) * r_, r_, 1.5, tg + math.pi, d=1), 2.4, None))
    # granules on the outer rope
    for k in range(68):
        t = (k + 0.5) / 68 * math.tau
        dots.append((cx + math.cos(t) * (A + 11), cy + math.sin(t) * (B + 11), 3.4))
    # crown rosette + leaf scroll sprays at top, smaller rosette at bottom, side buds
    rosette(items, dots, cx, cy - B - 22, 56, 8, 3.2, -math.pi / 2)
    for sgn in (-1, 1):
        for j, (u, v, L, a) in enumerate([(64, -B + 6, 46, -0.35), (104, -B + 26, 40, -0.05), (138, -B + 56, 32, 0.25)]):
            aa = a if sgn > 0 else math.pi - a
            cell(items, cx + sgn * u, cy + v, L, 16, aa, 3.0, sgn)
        items.append((coil(cx + sgn * 40, cy - B + 30, 13, 2.2, 0, d=sgn), 2.0, None))
    rosette(items, dots, cx, cy + B + 4, 36, 6, 3.0, math.pi / 2)
    for sgn in (-1, 1):
        cell(items, cx + sgn * 52, cy + B - 2, 36, 13, math.pi / 2 - sgn * 1.2, 2.0, sgn)
        rosette(items, dots, cx + sgn * (A + 8), cy, 28, 6, 2.6, 0)
    ring = np.clip(shapes(W, H, [oval_pts(cx, cy, A - 10, B - 10, 120)]) - shapes(W, H, [oval_pts(cx, cy, A - 66, B - 66, 120)]), 0, 1)
    art, m = paint_silver(W, H, items, dots, 31, base=plate(W, H, ring, 33))
    preview(art, "kp-bros", PAPER)
    save(art, f"{OUT}/bros.webp", max_w=560, quality=82)
    clear()

if "sudut" in PARTS:
    W, H = 340, 340
    items, dots = [], []
    # two scroll arms along the edges meeting in a corner rosette
    for horiz in (True, False):
        pts = curve([(30, 30), (110, 22), (200, 40), (300, 26)], 60) if horiz else curve([(30, 30), (22, 110), (40, 200), (26, 300)], 60)
        items.append((pts, 4.4, (0.0, 0.4)))
        for j, (x, y, a) in enumerate(along(pts, 46)):
            if j == 0:
                continue
            off = 1 if j % 2 else -1
            ang = a + off * 1.1
            cell(items, x, y, 32 - j * 3, 12 - j * 0.8, ang, 2.8, off)
            dots.append((x, y, 2.6))
        ex, ey = pts[-1]
        items.append((coil(ex, ey, 11, 2.0, 0, d=1), 2.0, None))
    rosette(items, dots, 42, 42, 38, 8, 3.0, math.pi / 4)
    art, m = paint_silver(W, H, items, dots, 41)
    preview(art, "kp-sudut", PAPER)
    save(art, f"{OUT}/sudut.webp", max_w=300, quality=82)
    clear()

if "garis" in PARTS:
    W, H = 760, 110
    cx, cy = W / 2, H / 2
    items, dots = [], []
    for sgn in (-1, 1):
        pts = [(cx + sgn * 48, cy), (cx + sgn * 340, cy)]
        rope(items, pts, 4.4, 6)
        for j, (x, y, a) in enumerate(along(pts, 44)):
            off = 1 if j % 2 else -1
            cell(items, x, y + off * 4, 28, 11, -math.pi / 2 * off, 2.7, off * sgn)
        items.append((coil(cx + sgn * 352, cy, 9, 2, 0, d=sgn), 2.0, None))
    rosette(items, dots, cx, cy, 46, 8, 3.0, 0)
    art, m = paint_silver(W, H, items, dots, 51)
    preview(art, "kp-garis", PAPER)
    save(art, f"{OUT}/garis.webp", max_w=420, quality=82)
    clear()

if "kembang" in PARTS:
    W, H = 260, 260
    items, dots = [], []
    rosette(items, dots, W / 2, H / 2, 108, 8, 3.2, -math.pi / 2)
    for k in range(8):
        a = -math.pi / 2 + (k + 0.5) / 8 * math.tau
        items.append((coil(W / 2 + math.cos(a) * 96, H / 2 + math.sin(a) * 96, 12, 2, a, d=1 if k % 2 else -1), 2.4, None))
    art, m = paint_silver(W, H, items, dots, 61, tarnish=0.4)
    preview(art, "kp-kembang", PAPER)
    save(art, f"{OUT}/kembang.webp", max_w=220, quality=84)
    clear()

if "gang" in PARTS:
    # frontal rumah kalang (Indies-Javanese merchant house) at the end of a Kotagede lane, plaster alley walls,
    # overhanging trees, grey-teal watercolour with a fine ink line
    W, H = 800, 600
    nx = Seq(9100); rng = random.Random(91)
    art = blank(W, H)
    yy = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    # sky wash + trees behind
    art = G(art, np.clip(1 - yy * 2.2, 0, 1), "#c9d8d6", "#e2eae7", seed=nx(), density=0.5, edge=0.05, bloom=0.6, rough=14)
    blobs = []
    for (x, y, r) in [(90, 150, 90), (180, 110, 80), (40, 230, 70), (700, 130, 95), (620, 100, 70), (770, 220, 70), (260, 150, 60), (540, 150, 60)]:
        for _ in range(7):
            blobs.append(deform(ellipse_pts(x + rng.uniform(-r, r) * 0.6, y + rng.uniform(-r, r) * 0.5, r * rng.uniform(0.4, 0.7), r * rng.uniform(0.3, 0.55), 12), rng, 2, 0.12))
    trees = shapes(W, H, blobs)
    cx = 400
    trunks = strokes(W, H, [(curve([(x, 340), (x + d * 6, 270), (x + d * 22, 200), (x + d * 40, 150)], 24), 13, (0.0, 0.7)) for x, d in [(80, 1), (712, -1)]]
                     + [(curve([(x + d * 8, 260), (x + d * 40, 210), (x + d * 70, 190)], 16), 6, (0.0, 0.8)) for x, d in [(80, -1), (712, 1)]])
    tl = G(blank(W, H), trunks, "#5e6b66", "#46524f", seed=nx(), density=0.8, edge=0.5, rough=2)
    tl = G(tl, trees, "#8fa8a0", "#6d8c86", seed=nx(), density=0.55, edge=0.5, bloom=0.5, rough=8)
    tl = G(tl, trees * np.clip((fbm(W, H, 7, 30, 3) - 0.5) * 3, 0, 1), "#4f6f6b", seed=nx(), density=0.5, edge=0.4, bloom=0.4, rough=6)
    dabs = [deform(ellipse_pts(rng.uniform(0, W), rng.uniform(60, 280), rng.uniform(16, 30), rng.uniform(9, 16), 10, rng.uniform(0, 3)), rng, 2, 0.15) for _ in range(90)]
    tl = G(tl, shapes(W, H, dabs) * np.clip(gaussian_filter(trees, 10) * 1.6, 0, 1), "#45655f", seed=nx(), density=0.38, edge=0.65, bloom=0.2, rough=4)
    house = shapes(W, H, [[(cx - 252, 226), (cx - 170, 148), (cx + 170, 148), (cx + 252, 226), (cx + 252, 600), (cx - 252, 600)]], smooth=False)
    art = glaze(art, knockout(tl, house, 1.0, 1.0))
    # roof (hipped, tiled) and facade
    roof = shapes(W, H, [[(cx - 250, 228), (cx - 170, 150), (cx + 170, 150), (cx + 250, 228)]], smooth=False)
    art = G(art, roof, "#58706f", "#3f5756", seed=nx(), density=0.8, edge=0.55, bloom=0.3, rough=2.5)
    tiles = strokes(W, H, [([(cx - 250 + k * 8 * 0.0 + (k / 14) * 80, 228 - (k / 14) * 78), (cx + 250 - (k / 14) * 80, 228 - (k / 14) * 78)], 1.2, None) for k in range(1, 14)])
    art = G(art, tiles * roof, "#2c3e3e", seed=nx(), density=0.5, edge=0.1, bloom=0, rough=0.8, feather=0.5)
    wall = shapes(W, H, [[(cx - 220, 226), (cx + 220, 226), (cx + 220, 470), (cx - 220, 470)]], smooth=False)
    art = G(art, wall, "#e9ece6", "#d6ddd7", seed=nx(), density=0.8, edge=0.5, bloom=0.5, rough=3)
    # pediment over the entrance
    ped = shapes(W, H, [[(cx - 92, 250), (cx, 196), (cx + 92, 250)]], smooth=False)
    art = G(art, ped, "#dfe5e0", "#c7d1cc", seed=nx(), density=0.9, edge=0.6, bloom=0.3, rough=1.6)
    # windows (arched, teal shutters) and double door
    polys = []
    for x0 in (cx - 190, cx - 130, cx + 94, cx + 154):
        polys.append([(x0, 300), (x0 + 36, 300), (x0 + 36, 410), (x0, 410)] )
    door = [(cx - 40, 300), (cx + 40, 300), (cx + 40, 470), (cx - 40, 470)]
    sh = shapes(W, H, polys + [door], smooth=False)
    arches = []
    for x0 in (cx - 190, cx - 130, cx + 94, cx + 154):
        arches.append(arc_pts(x0 + 18, 300, 18, math.pi, math.tau, 16) + [(x0 + 36, 301), (x0, 301)])
    arches.append(arc_pts(cx, 300, 40, math.pi, math.tau, 20) + [(cx + 40, 301), (cx - 40, 301)])
    sh = np.maximum(sh, shapes(W, H, arches, smooth=False))
    art = G(art, sh, "#3f7472", "#2c5c5c", seed=nx(), density=0.85, edge=0.6, bloom=0.3, rough=1.6)
    # columns
    cols = shapes(W, H, [[(x - 7, 262), (x + 7, 262), (x + 8, 470), (x - 8, 470)] for x in (cx - 210, cx - 70, cx + 70, cx + 210)], smooth=False)
    art = G(art, cols, "#f1f3ef", "#cfd8d3", seed=nx(), density=0.9, edge=0.6, rough=1)
    # plinth / terrace steps
    st = shapes(W, H, [[(cx - 236, 470), (cx + 236, 470), (cx + 250, 486), (cx - 250, 486)], [(cx - 60, 486), (cx + 60, 486), (cx + 70, 500), (cx - 70, 500)]], smooth=False)
    art = G(art, st, "#b6c0bb", "#9eaaa5", seed=nx(), density=0.75, edge=0.5, rough=1.5)
    # side alley walls (plaster with stains), lower, both sides in front of the house
    for sgn in (-1, 1):
        x0, x1 = (0, cx - 236) if sgn < 0 else (cx + 236, W)
        sw = shapes(W, H, [[(x0, 330), (x1, 360), (x1, 520), (x0, 600)]] if sgn < 0 else [[(x0, 360), (x1, 330), (x1, 600), (x0, 520)]], smooth=False)
        art = G(art, sw, "#dfe4de", "#c3cdc8", seed=nx(), density=0.85, edge=0.55, bloom=0.6, rough=4)
        stain = sw * np.clip((fbm(W, H, nx(), 22, 3) - 0.55) * 3, 0, 1) * np.clip(yy * 2 - 0.6, 0, 1)
        art = G(art, stain, "#8ea29c", seed=nx(), density=0.5, edge=0.2, bloom=0.5, rough=3)
        cap = shapes(W, H, [[(x0, 322), (x1, 352), (x1, 362), (x0, 334)]] if sgn < 0 else [[(x0, 352), (x1, 322), (x1, 334), (x0, 362)]], smooth=False)
        art = G(art, cap, "#6f8784", seed=nx(), density=0.85, edge=0.4, rough=1.4)
    # lane
    lane = shapes(W, H, [[(cx - 250, 498), (cx + 250, 498), (W, 600), (0, 600)]], smooth=False)
    art = G(art, lane, "#c9cec8", "#aeb7b1", seed=nx(), density=0.6, edge=0.3, bloom=0.5, rough=5)
    # dappled tree shadow across lane and walls
    dap = np.clip((fbm(W, H, 77, 40, 3) - 0.52) * 3.5, 0, 1) * np.clip(yy * 3 - 1.4, 0, 1)
    art = G(art, dap, "#7f9590", seed=nx(), density=0.35, edge=0.3, bloom=0.4, rough=6)
    # ink line drawing over architecture
    L = []
    for x0 in (cx - 190, cx - 130, cx + 94, cx + 154):
        L += [(arc_pts(x0 + 18, 300, 22, math.pi, math.tau, 18), 1.4, None), ([(x0 + 18, 300), (x0 + 18, 410)], 1.0, None), ([(x0 - 4, 414), (x0 + 40, 414)], 1.8, None)]
    L += [(arc_pts(cx, 300, 46, math.pi, math.tau, 24), 1.6, None), ([(cx, 300), (cx, 470)], 1.2, None)]
    L += [([(cx - 250, 228), (cx + 250, 228)], 2.2, None), ([(cx - 92, 250), (cx, 196), (cx + 92, 250), (cx - 92, 250)], 1.5, None)]
    L += [([(cx - 220, 262), (cx + 220, 262)], 1.4, None), ([(cx - 220, 470), (cx + 220, 470)], 1.6, None)]
    for x in (cx - 210, cx - 70, cx + 70, cx + 210):
        L += [([(x - 8, 262), (x - 9, 470)], 1.0, None), ([(x + 8, 262), (x + 9, 470)], 1.0, None), ([(x - 12, 264), (x + 12, 264)], 2.2, None)]
    # carved fanlight scroll in the pediment
    L += [(coil(cx - 22, 236, 12, 1.6, 0, d=1), 1.2, None), (coil(cx + 22, 236, 12, 1.6, math.pi, d=-1), 1.2, None)]
    # lamp
    L += [([(cx + 120, 228), (cx + 120, 252)], 1.4, None)]
    ink = strokes(W, H, L)
    art = G(art, ink, "#2a3a3b", seed=nx(), density=0.75, edge=0.1, bloom=0, rough=0.7, feather=0.4)
    art = G(art, shapes(W, H, [[(cx + 112, 252), (cx + 128, 252), (cx + 125, 268), (cx + 115, 268)]], smooth=False), "#384c4d", seed=nx(), density=0.85, edge=0.3, rough=0.6)
    art = over(art, glow(circles(W, H, [(cx + 120, 262, 6)]), "#f6e9c4", 9, 0.6))
    # potted plants by the door
    for (x, y) in [(cx - 92, 498), (cx + 92, 498)]:
        pot = shapes(W, H, [[(x - 14, y - 22), (x + 14, y - 22), (x + 10, y), (x - 10, y)]], smooth=False)
        art = G(art, pot, "#8a8073", seed=nx(), density=0.75, edge=0.4, rough=1.2)
        lv = [petal_pts(x + rng.uniform(-5, 5), y - 22, rng.uniform(24, 40), 7, -math.pi / 2 + rng.uniform(-1.1, 1.1)) for _ in range(9)]
        art = G(art, shapes(W, H, lv), "#6f8f84", "#4e7068", seed=nx(), density=0.75, edge=0.45, bloom=0.3, rough=1.5)
    art[..., 3] *= np.clip(yy * 7, 0, 1) * np.clip((1 - yy) * 5, 0, 1)
    preview(art, "kp-gang", PAPER)
    save(art, f"{OUT}/gang.webp", max_w=680, quality=70)
    clear()
